# -*- coding: utf-8 -*-
"""GRPO thưởng người nghe (B.6 của 288) — gọi đúng `grpo_spice.train`, chỉ thay hàm thưởng (và tuỳ chọn
khởi LoRA từ adapter ck500 bằng --tu). Mọi siêu tham số khác trùng ck500 bởi cấu tạo.

    python grpo_nghe.py --selftest                                              # CPU, ~1 phút
    python grpo_nghe.py --dung-bang --som g0_som.jsonl --nghe g0_phi4.jsonl --out bang_nghe.json
    python grpo_nghe.py --merge --bundle B --merged M
    python grpo_nghe.py --train --arm nghev --seed 101 --bang bang_nghe.json --bundle B --merged M --out O \
                        --tu ck500/ --max-steps 250 --bs 4 --accum 4 --resume auto --no-q4

Thưởng ở câu nhắc click có trong bảng (§6.1):  r = r_spice + W·h,  W = 1,0
  nghev  (A)      h chỉ tính ở màn có v = 1 (Phi-4 trỏ trúng câu chuẩn)
  nghe   (B1)     h ở mọi màn có ô đáp án
  nghern (B-rand) h ở màn có v_rand = 1 (Bernoulli(TB v), hạt 288)
  spicea (B0′)    không bao giờ gọi người nghe (r = r_spice)
  nghevm / nghem  như nghev / nghe nhưng W = 2,0 (liều mạnh, thêm 6/10)
h = 1 ⇔ câu qua dang_ok ∧ ô Phi-4 chọn ∈ dap_an. Câu nhắc khác: r = r_spice như ck500.
Người nghe chạy ở tiến trình riêng (nghe_server.py) qua TCP 127.0.0.1:<cong>.
Viết lại 6/10/2026 từ bản mô tả B.6 (mã gốc ở máy Mac) ⇒ md5 khác bản gốc.
"""
import argparse, hashlib, json, os, random, re, socket, subprocess, sys, tempfile, time, types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

W_NGHE = 1.0
CONG = 47288
HAT_RAND = 288
ARMS = ("nghev", "nghe", "nghern", "spicea", "nghevm", "nghem")
W_ARM = {"nghevm": 2.0, "nghem": 2.0}         # nhánh "m" = liều mạnh (W = 2), thêm 6/10 theo quyết định chủ luận văn
TAPT = ("click", "long_press")


class Dung(Exception):
    pass


def dang_ok(s):
    w = (s or "").split()
    return 3 <= len(w) <= 20 and not re.search(r"\d+\s*[,;]\s*\d+", s) and not re.search(r"\d{3,}", s)


def _text(c):
    if isinstance(c, list):
        return (c[0].get("content") if c else "") or ""
    return c or ""


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


# ─────────────────────────── client máy chủ ───────────────────────────
def hoi_may_chu(viec, cong, het_gio):
    """→ (danh sách ô chọn | phản hồi ping, None) hoặc (None, lỗi). Không bao giờ ném lỗi ra ngoài."""
    try:
        with socket.create_connection(("127.0.0.1", cong), timeout=het_gio) as s:
            s.settimeout(het_gio)
            s.sendall((json.dumps({"viec": viec}, ensure_ascii=False) + "\n").encode("utf-8"))
            buf = b""
            while not buf.endswith(b"\n"):
                x = s.recv(65536)
                if not x:
                    break
                buf += x
        q = json.loads(buf.decode("utf-8"))
        if "loi" in q:
            return None, q["loi"]
        if viec and len(q.get("chon") or []) != len(viec):
            return None, "lệch số câu"
        return (q["chon"] if "chon" in q else q), None
    except (OSError, ValueError) as e:
        return None, repr(e)


def cho_may_chu(cong, toi_da=1800):
    t0 = time.time()
    while time.time() - t0 < toi_da:
        q, loi = hoi_may_chu([], cong, 15)
        if loi is None and isinstance(q, dict) and q.get("ok"):
            return q.get("ten")
        time.sleep(15)
    sys.exit(f"DỪNG: máy chủ người nghe không trả lời ở cổng {cong} sau {toi_da} s")


# ─────────────────────────── hàm thưởng ───────────────────────────
def lam_thuong(arm, bang, spice_fn, out, cong, het_gio=None, thoat=True):
    assert arm in ARMS, arm
    os.makedirs(out, exist_ok=True)
    LOG = os.path.join(out, "nghe_log.jsonl")
    H = {"sp": [], "vp": [], "loi": 0, "hoi": 0, "lan": 0}
    if os.path.exists(LOG):                       # chạy tiếp sau mất máy: luật dừng vẫn so với 50 lần đầu thật
        for l in open(LOG, encoding="utf-8"):
            try:
                o = json.loads(l)
            except json.JSONDecodeError:
                continue
            H["sp"].append(o["sp_tb"]); H["vp"].append((o["vi_pham"], o["n_cham"]))
            H["loi"] += int(bool(o.get("loi"))); H["hoi"] += int(o["n_hoi"] > 0); H["lan"] = o["lan"]
    CACHE = {}
    cong_man = {"nghev": lambda b: b["v"], "nghe": lambda b: 1, "nghern": lambda b: b["v_rand"], "spicea": lambda b: 0,
                "nghevm": lambda b: b["v"], "nghem": lambda b: 1}[arm]
    W = W_ARM.get(arm, W_NGHE)

    def dung(ly_do):
        json.dump({"ly_do": ly_do, "lan": H["lan"]}, open(os.path.join(out, "DUNG.json"), "w", encoding="utf-8"),
                  ensure_ascii=False)
        print(f"⛔ [nghe] DỪNG theo luật: {ly_do}", flush=True)
        if thoat:
            sys.stdout.flush(); os._exit(3)
        raise Dung(ly_do)

    def r_nghe(completions, gold, action_type=None, key=None, **kw):
        t0 = time.time()
        n = len(completions)
        action_type = action_type or [""] * n
        key = key or [""] * n
        sp = list(spice_fn(completions, gold))
        cau = [_text(c).strip() for c in completions]
        cham = [action_type[i] in TAPT and key[i] in bang for i in range(n)]
        bat = [cham[i] and cong_man(bang[key[i]]) != 0 and bool(bang[key[i]]["dap_an"]) for i in range(n)]
        ok = [bool(cau[i]) and dang_ok(cau[i]) for i in range(n)]
        viec = sorted({(key[i], cau[i]) for i in range(n) if bat[i] and ok[i] and (key[i], cau[i]) not in CACHE})
        loi = None
        if viec:
            q, loi = hoi_may_chu([{"key": k, "sent": s} for k, s in viec], cong,
                                 het_gio if het_gio is not None else 60 + 5 * len(viec))
            if loi is None:
                for kk, c in zip(viec, q):
                    CACHE[kk] = c
        h = [int(bat[i] and ok[i] and loi is None and CACHE.get((key[i], cau[i])) in bang[key[i]]["dap_an"])
             for i in range(n)]
        r = [sp[i] + W * h[i] for i in range(n)]
        vi_pham = sum(cham[i] and not ok[i] for i in range(n))
        H["lan"] += 1; H["sp"].append(sum(sp) / max(n, 1)); H["vp"].append((vi_pham, sum(cham)))
        H["hoi"] += int(bool(viec)); H["loi"] += int(loi is not None)
        o = {"lan": H["lan"], "n": n, "n_cham": sum(cham), "n_bat": sum(bat), "n_hoi": len(viec), "n_trung": sum(h),
             "vi_pham": vi_pham, "sp_tb": H["sp"][-1], "dt": round(time.time() - t0, 2), "loi": loi}
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
        print(f"[nghe] lần {o['lan']} · chạm {o['n_cham']}/{n} · bật {o['n_bat']} · hỏi {o['n_hoi']} · trúng {o['n_trung']}"
              f" · định dạng {vi_pham} · SPICE TB {o['sp_tb']:.3f} · {o['dt']:.1f}s" + (f" · ⚠️ lỗi máy chủ: {loi}" if loi else ""),
              flush=True)
        # luật dừng khoá trước (§6.4): không bộ trỏ, không val/test
        if H["lan"] >= 100:
            dau, cuoi = sum(H["sp"][:50]) / 50, sum(H["sp"][-50:]) / 50
            if cuoi < 0.80 * dau:
                dung(f"SPICE TB 50 lần cuối {cuoi:.3f} < 0,80 × 50 lần đầu {dau:.3f}")
        if arm != "spicea" and H["lan"] >= 50:
            v, c = sum(x for x, _ in H["vp"][-50:]), sum(y for _, y in H["vp"][-50:])
            if c and v / c > 0.10:
                dung(f"vi phạm định dạng {v}/{c} = {v / c:.3f} > 0,10 ở 50 lần cuối")
        if arm != "spicea" and H["hoi"] >= 50 and H["loi"] / H["hoi"] > 0.05:
            dung(f"máy chủ lỗi {H['loi']}/{H['hoi']} lần có hỏi > 5% (kỹ thuật: sửa hạ tầng, chạy lại từ đầu)")
        return r

    r_nghe.__name__ = "r_spice" if arm == "spicea" else "r_nghe"
    r_nghe.H, r_nghe.CACHE = H, CACHE
    return r_nghe


# ─────────────────────────── dựng bảng ───────────────────────────
def dung_bang(a):
    som = [json.loads(l) for l in open(a.som, encoding="utf-8")]
    tr = {(o["episode_id"], o["step_id"]): o for o in som if o["tap"] == "train"}
    kq = {}
    for l in open(a.nghe, encoding="utf-8"):
        try:
            o = json.loads(l)
        except json.JSONDecodeError:
            continue
        if o["tap"] == "train":
            kq[(str(o["episode_id"]), str(o["step_id"]))] = o
    assert len(tr) == 630 and len(kq) == 630, f"DỪNG: màn train {len(tr)}, kết quả người nghe train {len(kq)} (cần 630)"
    v = {f"{e}_{s}": int(kq[(e, s)]["h"]) for (e, s) in tr}
    p = sum(v.values()) / len(v)
    rr = random.Random(HAT_RAND)
    v_rand = {k: int(rr.random() < p) for k in sorted(v)}
    bang = {f"{e}_{s}": {"image": o["image_goc"], "w": o["w"], "h": o["h"], "boxes": o["boxes"], "dap_an": o["dap_an"],
                         "v": v[f"{e}_{s}"], "v_rand": v_rand[f"{e}_{s}"]} for (e, s), o in tr.items()}
    meta = {"n": len(bang), "tb_v": p, "tb_v_rand": sum(v_rand.values()) / len(v_rand),
            "co_dap_an": sum(bool(b["dap_an"]) for b in bang.values()), "som_md5": md5(a.som), "nghe_md5": md5(a.nghe),
            "hat_rand": HAT_RAND}
    json.dump({"meta": meta, "bang": bang}, open(a.out, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"[bảng] {meta['n']} màn · TB v {p:.3f} · TB v_rand {meta['tb_v_rand']:.3f} · có đáp án {meta['co_dap_an']}"
          f" → {a.out} · md5 {md5(a.out)}", flush=True)


# ─────────────────────────── merge / train ───────────────────────────
def ep_fp16():
    import torch
    import grpo_spice as GS
    GS._dtype = lambda: torch.float16          # ck500 train fp16 trên T4; A100 tự chọn bf16 nên phải ép


def train(a):
    import torch, peft
    import grpo_spice as GS
    ep_fp16()
    bang = {}
    if a.arm != "spicea":
        B = json.load(open(a.bang, encoding="utf-8"))
        bang = B["bang"]
        print(f"[bảng] {len(bang)} màn · TB v {B['meta']['tb_v']:.3f} · md5 {md5(a.bang)}", flush=True)
        ten = cho_may_chu(a.cong, 1800)
        print(f"[nghe] máy chủ sẵn sàng · {ten} · cổng {a.cong}", flush=True)
    if not hasattr(GS, "_r_spice_goc"):          # giữ bản gốc MỘT lần ⇒ gọi train() nhiều lần không bọc lồng nhau
        GS._r_spice_goc, GS._dung_hang_goc = GS.r_spice, GS.dung_hang
    if not hasattr(peft, "_gpm_goc"):
        peft._gpm_goc = peft.get_peft_model
    R = lam_thuong(a.arm, bang, GS._r_spice_goc, a.out, a.cong)
    json.dump({"arm": a.arm, "seed": a.seed, "w": W_ARM.get(a.arm, W_NGHE), "bang": a.bang, "nguoi_nghe": "Phi-4-multimodal (giao thức 14/9)",
               "bs": a.bs, "accum": a.accum, "tu": a.tu, "max_steps": a.max_steps},
              open(os.path.join(a.out, "nghe_meta.json"), "w", encoding="utf-8"), ensure_ascii=False)
    GS.r_spice = R

    def dh(*x, **k):                             # 1.000 câu nhắc LUÔN là của ck500, bất kể hạt cấu hình
        cu = GS.SEED; GS.SEED = 101
        try:
            return GS._dung_hang_goc(*x, **k)
        finally:
            GS.SEED = cu
    GS.dung_hang = dh
    GS.SEED = a.seed

    def gpm(model, *x, **k):
        if a.seed != 101:
            torch.manual_seed(a.seed)
        if a.tu:
            print(f"[train tiếp] LoRA khởi từ {a.tu} (is_trainable)", flush=True)
            return peft.PeftModel.from_pretrained(model, a.tu, is_trainable=True)
        return peft._gpm_goc(model, *x, **k)
    peft.get_peft_model = gpm
    print(f"[nhánh] {a.arm} · hạt {a.seed} · W {W_ARM.get(a.arm, W_NGHE)} · thưởng {R.__name__} · bs {a.bs}×{a.accum}"
          + (f" · tiếp từ {a.tu}" if a.tu else " · LoRA mới"), flush=True)
    GS.train(a)


# ─────────────────────────── tự kiểm ───────────────────────────
def selftest():
    from PIL import Image
    d = tempfile.mkdtemp()
    os.makedirs(f"{d}/images")
    bang = {}
    for k, v, vr, bx in (("90_1", 1, 0, True), ("91_1", 0, 1, True), ("92_1", 1, 1, True), ("99_1", 0, 0, False)):
        Image.new("RGB", (540, 1200), "white").save(f"{d}/images/{k}.png")
        bang[k] = {"image": f"images/{k}.png", "w": 540, "h": 1200,
                   "boxes": [[20, 20, 200, 120], [20, 300, 500, 420]] if bx else [], "dap_an": [2] if bx else [],
                   "v": v, "v_rand": vr}
    json.dump({"meta": {"tb_v": 0.5}, "bang": bang}, open(f"{d}/bang.json", "w"))
    C = 47999
    SV = subprocess.Popen([sys.executable, os.path.join(HERE, "nghe_server.py"), "--backend", "gia", "--bang", f"{d}/bang.json",
                           "--img-root", d, "--cong", str(C)], stdout=open(f"{d}/sv.log", "w"), stderr=subprocess.STDOUT,
                          start_new_session=True)
    spice05 = lambda comp, gold, **kw: [0.5] * len(comp)
    ok_all = []

    def kiem(ten, dk):
        ok_all.append(dk); print(("✅ " if dk else "⛔ ") + ten, flush=True)

    try:
        cho_may_chu(C, 60)
        CAU = [("Click on the TRUNG button", "90_1", "click", (1.5, 1.5, 0.5, 0.5)),
               ("TRUNG", "90_1", "click", (0.5,) * 4),
               ("Click at 540, 1200 TRUNG", "90_1", "click", (0.5,) * 4),
               ("Click on the wrong button", "90_1", "click", (0.5,) * 4),
               ("Click on the TRUNG button", "91_1", "click", (1.5, 0.5, 1.5, 0.5)),
               ("Click on the TRUNG button", "92_1", "click", (1.5, 1.5, 1.5, 0.5)),
               ("Scroll down TRUNG please", "90_1", "scroll", (0.5,) * 4),
               ("Click on the TRUNG item", "99_1", "click", (0.5,) * 4)]
        comp, key, at = [c[0] for c in CAU], [c[1] for c in CAU], [c[2] for c in CAU]
        for j, arm in enumerate(("nghe", "nghev", "nghern", "spicea")):
            R = lam_thuong(arm, bang, spice05, f"{d}/t1_{arm}", C, thoat=False)
            r1 = R(comp, ["x"] * 8, action_type=at, key=key)
            hoi1 = sum(json.loads(l)["n_hoi"] for l in open(f"{d}/t1_{arm}/nghe_log.jsonl"))
            r2 = R(comp, ["x"] * 8, action_type=at, key=key)
            hoi2 = sum(json.loads(l)["n_hoi"] for l in open(f"{d}/t1_{arm}/nghe_log.jsonl"))
            kiem(f"1. bảng thưởng nhánh {arm}: {r1} · gọi lại cùng kết quả, không hỏi thêm ({hoi1}→{hoi2})",
                 r1 == [c[3][j] for c in CAU] and r1 == r2 and hoi1 == hoi2)

        for arm, mong in (("nghem", [2.5, 0.5, 0.5, 0.5, 2.5, 2.5, 0.5, 0.5]), ("nghevm", [2.5, 0.5, 0.5, 0.5, 0.5, 2.5, 0.5, 0.5])):
            R = lam_thuong(arm, bang, spice05, f"{d}/t1_{arm}", C, thoat=False)
            r1 = R(comp, ["x"] * 8, action_type=at, key=key)
            kiem(f"1b. nhánh liều mạnh {arm} (W = 2): {r1}", r1 == mong)

        R = lam_thuong("nghe", bang, spice05, f"{d}/t2", C, het_gio=3, thoat=False)
        r = R(["Click on the TREO TRUNG button"], ["x"], action_type=["click"], key=["90_1"])
        kiem(f"2. câu TREO, hết giờ 3 s: thưởng {r} · lỗi {R.H['loi']}", r == [0.5] and R.H["loi"] == 1)
        time.sleep(30)

        sp_lan = {"n": 0}

        def spice_rot(comp, gold, **kw):
            sp_lan["n"] += 1
            return [0.5 if sp_lan["n"] <= 60 else 0.3] * len(comp)
        R = lam_thuong("spicea", bang, spice_rot, f"{d}/t3", C, thoat=False)
        ly = None
        try:
            for _ in range(200):
                R(["Click on the search bar"], ["x"], action_type=["click"], key=["90_1"])
        except Dung as e:
            ly = str(e)
        kiem(f"3. luật dừng SPICE ở lần {R.H['lan']}: {ly}",
             R.H["lan"] == 100 and ly and "SPICE" in ly and os.path.exists(f"{d}/t3/DUNG.json"))

        R = lam_thuong("nghe", bang, spice05, f"{d}/t4", C, thoat=False)
        ly = None
        try:
            for i in range(200):
                s, k = ("Click on the search bar", "99_1") if i < 6 else ("Tap", "90_1")
                R([s], ["x"], action_type=["click"], key=[k])
        except Dung as e:
            ly = str(e)
        kiem(f"4. luật dừng định dạng ở lần {R.H['lan']}: {ly}", ly is not None and "định dạng" in ly)

        R = lam_thuong("nghe", bang, spice05, f"{d}/t4", C, thoat=False)
        kiem(f"5. tạo lại trên cùng thư mục nạp nhật ký cũ: lần {R.H['lan']}", R.H["lan"] > 0)

        os.killpg(SV.pid, 15); SV.wait(); time.sleep(1)
        R = lam_thuong("nghe", bang, spice05, f"{d}/t6", C, thoat=False)
        r = R(["Click on the TRUNG button"], ["x"], action_type=["click"], key=["90_1"])
        kiem(f"6. tắt máy chủ: thưởng {r} · lỗi {R.H['loi']}", r == [0.5] and R.H["loi"] == 1)

        dk = [dang_ok("Click on the search bar"), dang_ok("Select 2 adults in the list"),
              not dang_ok("Tap 12, 40"), not dang_ok("Click 1200"), not dang_ok("Click")]
        kiem(f"7. dang_ok {dk}", all(dk))

        kiem("8. nối dây train() bằng module giả", kiem_noi_day(d))
    finally:
        try:
            os.killpg(SV.pid, 15)
        except Exception:
            pass
    print(f"{'✅ selftest ĐẠT' if all(ok_all) else '⛔ selftest RỚT'} ({sum(ok_all)}/{len(ok_all)})", flush=True)
    sys.exit(0 if all(ok_all) else 1)


def kiem_noi_day(d):
    goc = {m: sys.modules.get(m) for m in ("torch", "peft", "grpo_spice")}
    ghi = []
    T = types.ModuleType("torch"); T.float16 = "fp16"; T.manual_seed = lambda s: ghi.append(("manual_seed", s))
    P = types.ModuleType("peft")
    P.get_peft_model = lambda model, cfg=None, *x, **k: ghi.append(("gpm_goc",)) or "lora_moi"

    class PeftModel:
        @staticmethod
        def from_pretrained(model, path, is_trainable=False):
            ghi.append(("from_pretrained", path, is_trainable)); return "lora_ck500"
    P.PeftModel = PeftModel
    G = types.ModuleType("grpo_spice"); G.SEED = 101; G._dtype = lambda: "bf16"
    G.r_spice = lambda comp, gold, **kw: [0.5] * len(comp)
    G.r_spice.__name__ = "r_spice"

    def dung_hang(bundle, n=1000, dai_nhat=0):
        ghi.append(("dung_hang_seed", G.SEED)); return [], {}
    G.dung_hang = dung_hang

    def gtrain(a):
        rows, _ = G.dung_hang(a.bundle, n=a.n_prompt)
        import peft as PP
        m = PP.get_peft_model("model", "cfg")
        r = G.r_spice(["Click on the search bar"], ["Click on the search bar"], action_type=["scroll"], key=["x"])
        ghi.append(("train", G.SEED, G._dtype(), G.r_spice.__name__, r, m))
    G.train = gtrain
    try:
        sys.modules.update({"torch": T, "peft": P, "grpo_spice": G})
        ok = True
        for seed, tu, mong in ((202, None, "lora_moi"), (101, None, "lora_moi"), (101, "/ck500", "lora_ck500")):
            ghi.clear()
            out = f"{d}/t8_{seed}_{bool(tu)}"
            a = argparse.Namespace(arm="spicea", seed=seed, tu=tu, bang=None, cong=47999, out=out, bundle="B", n_prompt=1000,
                                   bs=4, accum=4, max_steps=250)
            train(a)
            tr = [x for x in ghi if x[0] == "train"][0]
            meta = json.load(open(f"{out}/nghe_meta.json"))
            dk = [("dung_hang_seed", 101) in ghi,
                  tr[1] == seed, tr[2] == "fp16", tr[3] == "r_spice", tr[4] == [0.5], tr[5] == mong,
                  (("manual_seed", seed) in ghi) == (seed != 101),
                  (("from_pretrained", "/ck500", True) in ghi) == bool(tu), (("gpm_goc",) in ghi) == (not tu),
                  meta["arm"] == "spicea" and meta["tu"] == tu and meta["max_steps"] == 250]
            print(f"   nối dây (spicea, hạt {seed}, tu {tu}): {dk}", flush=True)
            ok &= all(dk)
        return ok
    finally:
        for m, v in goc.items():
            if v is None:
                sys.modules.pop(m, None)
            else:
                sys.modules[m] = v


def main():
    ap = argparse.ArgumentParser()
    for f in ("--selftest", "--dung-bang", "--merge", "--train", "--probe"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--arm", choices=ARMS)
    ap.add_argument("--seed", type=int, default=101)
    ap.add_argument("--bang"); ap.add_argument("--som"); ap.add_argument("--nghe")
    ap.add_argument("--cong", type=int, default=CONG)
    ap.add_argument("--bundle"); ap.add_argument("--merged", default="/content/s1_merged")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--out"); ap.add_argument("--tu", default=None)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--n-prompt", type=int, default=1000)
    ap.add_argument("--G", type=int, default=8)
    ap.add_argument("--bs", type=int, default=8)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--beta", type=float, default=0.04)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--max-steps", type=int, default=500)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--no-q4", dest="q4", action="store_false")
    ap.add_argument("--gen-chunk", type=int, default=0)
    a = ap.parse_args()
    if a.bundle:
        a.adapter = a.adapter or os.path.join(a.bundle, "adapter_s1_seed101")
    if a.selftest:
        selftest()
    elif a.dung_bang:
        assert a.som and a.nghe and a.out, "cần --som --nghe --out"
        dung_bang(a)
    elif a.merge:
        assert a.bundle and a.merged, "cần --bundle --merged"
        ep_fp16()
        import grpo_spice as GS
        GS.merge(a)
    elif a.train or a.probe:
        assert a.arm and a.out and a.bundle, "train cần --arm --out --bundle"
        assert a.arm == "spicea" or a.bang, "nhánh người nghe cần --bang"
        train(a)
    else:
        ap.error("chọn một chế độ")


if __name__ == "__main__":
    main()
