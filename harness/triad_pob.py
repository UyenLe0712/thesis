# -*- coding: utf-8 -*-
"""TRIAD-T pha POB (action 273 §6): ứng viên là mẫu của ck500 thật, không phải mẫu S1.

Kaggle (T4):
  python triad_pob.py --sample --bundle B --merged M --ckpt CK500 --c1 C1 --temp 0.7 --out mau_t07.jsonl [--kiem-greedy P]
  python triad_pob.py --lop --dir D        (CPU: câu duy nhất ⇒ calls cho listener + các lớp preds cho UGround)
  python triad_pob.py --chon --dir D       (CPU: bộ chọn §4 + luật §5.3 ⇒ preds UI-Venus cho C2 tốt nhất mỗi nhiệt độ)
Máy nhà:
  python triad_pob.py --bao-cao --dir runs/triad_t/pob --out runs/triad_t/pob_ket_qua.json

Thư mục D chứa: score_ck500_l4_raw.jsonl · loc_val_{g,d}.jsonl · listener_showui_poa.jsonl ·
score_venus_ck500_raw.jsonl · c1_recs.jsonl · mau_t07.jsonl · mau_t10.jsonl, rồi các tệp chạy sinh ra.

Luật chọn câu, lưới r × r_trust, luật chọn cấu hình: NHẬP NGUYÊN từ triad_t.py (đã khoá ở POA, không
chọn lại listener). Câu chuẩn / điểm vàng / executable chỉ được đọc ở phần đánh giá, sau khi đã chọn.
"""

import os, re, sys, json, time, random, argparse, collections, statistics

os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NHIET = {"t07": 0.7, "t10": 1.0}
SEED_MAU = 20261004
TAPT = ("click", "long_press")
VIET = re.compile(r"[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]", re.I)


def K(d):
    return (d["episode_id"], d["step_id"])


def nap(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


# ───────────────────────────── 1. lấy mẫu ck500 (GPU) ─────────────────────────────

def sample(a):
    import torch
    from PIL import Image
    from peft import PeftModel
    import grpo_spice as G

    va = [json.loads(l) for l in open(os.path.join(a.bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    rows = random.Random(G.SEED_C1).sample(va, 400)
    C1 = nap(a.c1)
    assert [K(r) for r in rows] == [K(d) for d in C1], "⛔ thứ tự 400 bước lệch c1_mau.jsonl"
    rows = [r for r in rows if (r.get("action") or {}).get("action_type") in TAPT and "x" in r["action"]]
    assert len(rows) == 249, len(rows)
    if a.n:
        rows = rows[:a.n]
    ocr = G.nap_ocr(a.bundle)
    done = {K(d) for d in nap(a.out)} if os.path.exists(a.out) else set()
    print(f"[mẫu] T={a.temp} · k={a.k} · {len(rows)} bước click · đã có {len(done)} · seed gốc {SEED_MAU}",
          flush=True)
    if len(done) >= len(rows):
        print("[mẫu] xong sẵn", flush=True)
        return

    a.q4 = False                                   # ck500 greedy đã sinh bằng --no-q4
    proc, model, dt = G.nap(a)
    model = PeftModel.from_pretrained(model, a.ckpt)
    model.eval()
    print("[điểm lưu]", a.ckpt, flush=True)
    samp = dict(do_sample=True, temperature=a.temp, top_p=1.0, top_k=0, repetition_penalty=1.0,
                num_return_sequences=a.k, max_new_tokens=96, use_cache=True)
    print(f"[cấu hình lấy mẫu] {samp}", flush=True)
    G0 = {K(d): d["pred"] for d in nap(a.kiem_greedy)} if a.kiem_greedy else {}
    trung = n_kg = 0

    fo = open(a.out, "a", encoding="utf-8")
    t0, n_moi = time.time(), 0
    for i, r in enumerate(rows):
        if K(r) in done:
            continue
        msg = [{"role": "system", "content": G.SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + G.body_of(r, ocr)}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]
        seed = SEED_MAU + i                        # theo vị trí bước ⇒ nối tiếp vẫn tất định
        with torch.no_grad():
            if G0:
                g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                                   temperature=None, top_p=None, top_k=None)
                gs = proc.decode(g[0][L:], skip_special_tokens=True).strip()
                trung += gs == G0.get(K(r), "").strip()
                n_kg += 1
            torch.manual_seed(seed)
            s = model.generate(**inp, **samp)
        mau = [proc.decode(x[L:], skip_special_tokens=True).strip() for x in s]
        fo.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "temp": a.temp,
                             "seed": seed, "mau": mau}, ensure_ascii=False) + "\n")
        fo.flush()
        n_moi += 1
        if n_moi <= 2 or n_moi % 20 == 0:
            el = time.time() - t0
            con = len(rows) - len(done) - n_moi
            print(f"  [mẫu T={a.temp}] {n_moi + len(done)}/{len(rows)} · {el / n_moi:.1f} s/bước · còn ~{el / n_moi * con / 60:.0f} phút"
                  + (f" · kiểm greedy trùng ck500 {trung}/{n_kg}" if G0 else "") + f" · {mau[0][:50]!r}", flush=True)
    fo.close()
    if G0:
        print(f"[kiểm hoà ck500] greedy sinh lại trùng pred_ck500: {trung}/{n_kg}", flush=True)
    print(f"[mẫu T={a.temp}] XONG", flush=True)


# ───────────────────────────── 2. dựng lớp câu duy nhất (CPU) ─────────────────────────────

def nap_mau(D):
    M = {}
    for ten in NHIET:
        p = f"{D}/mau_{ten}.jsonl"
        M[ten] = {K(d): d["mau"] for d in nap(p)} if os.path.exists(p) else {}
    return M


def lop(a):
    D = a.dir
    recs = {K(d): d for d in nap(f"{D}/c1_recs.jsonl")}
    ck = {K(d): d for d in nap(f"{D}/score_ck500_l4_raw.jsonl")}
    keys = sorted(ck)
    M = nap_mau(D)
    if a.thu:                                      # lượt thử: chỉ các bước đã có mẫu ở mọi nhiệt độ
        keys = [k for k in keys if all(k in m for m in M.values())]
    for ten, m in M.items():
        assert set(m) >= set(keys) and (a.thu or len(keys) == 249), f"⛔ mẫu {ten}: {len(m)}/249 bước"
    cu = {(K(d), d["sent"].strip()) for d in nap(f"{D}/listener_showui_poa.jsonl")}
    # câu duy nhất ở mỗi bước, khác greedy ck500 (greedy đã có UGround L4 + ShowUI + UI-Venus từ POA)
    U = {}
    for k in keys:
        d0 = ck[k]["sent"].strip()
        seen = []
        for ten in NHIET:
            for s in M[ten][k]:
                s = (s or "").strip()
                if s and s != d0 and s not in seen:
                    seen.append(s)
        U[k] = seen
    n_lop = max(map(len, U.values()))
    os.makedirs(f"{D}/ug_lop", exist_ok=True)
    tong = 0
    for j in range(n_lop):
        with open(f"{D}/ug_lop/lop{j:02d}.jsonl", "w", encoding="utf-8") as f:
            for k in keys:
                if j < len(U[k]):
                    f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": U[k][j]},
                                       ensure_ascii=False) + "\n")
                    tong += 1
    n_call = 0
    with open(f"{D}/calls_pob.jsonl", "w", encoding="utf-8") as f:
        for k in keys:
            for s in U[k]:
                if (k, s) in cu:
                    continue
                f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "nguon": "pob", "sent": s,
                                    "image": recs[k]["image"], "w": recs[k]["w"], "h": recs[k]["h"]},
                                   ensure_ascii=False) + "\n")
                n_call += 1
    print(f"[lớp] {tong} câu duy nhất khác greedy · {n_lop} lớp UGround · {n_call} lời gọi listener mới "
          f"(đã có từ POA {tong - n_call})", flush=True)


# ───────────────────────────── 3. chọn câu + đánh giá ─────────────────────────────

def nap_tat_ca(D, can_venus=False):
    import triad_t as T
    recs = {K(d): d for d in nap(f"{D}/c1_recs.jsonl")}
    ck = {K(d): d for d in nap(f"{D}/score_ck500_l4_raw.jsonl")}
    keys = sorted(ck)
    assert len(keys) == 249 and sum(ck[k]["executable"] for k in keys) == 166
    lg = {K(d): d["xy"] for d in nap(f"{D}/loc_val_g.jsonl")}
    ld = {K(d): d["xy"] for d in nap(f"{D}/loc_val_d.jsonl")}
    M = nap_mau(D)
    L = {}
    for p in [f"{D}/listener_showui_poa.jsonl"] + sorted(
            f"{D}/{x}" for x in os.listdir(D) if x.startswith("listener_pob")):
        for d in nap(p):
            L[(K(d), d["sent"].strip())] = tuple(d["xy"]) if d.get("xy") else None
    UG = {(k, ck[k]["sent"].strip()): ck[k]["executable"] for k in keys}
    for p in sorted(os.listdir(f"{D}/ug_lop")) if os.path.isdir(f"{D}/ug_lop") else []:
        if p.endswith("_raw.jsonl"):
            for d in nap(f"{D}/ug_lop/{p}"):
                UG[(K(d), d["sent"].strip())] = int(d["executable"])
    V = {}
    for p in [f"{D}/score_venus_ck500_raw.jsonl"] + (
            [f"{D}/venus_lop/{x}" for x in sorted(os.listdir(f"{D}/venus_lop")) if x.endswith("_raw.jsonl")]
            if os.path.isdir(f"{D}/venus_lop") else []):
        for d in nap(p):
            V[(K(d), d["sent"].strip())] = int(d["executable"])
    return T, recs, ck, keys, lg, ld, M, L, UG, V


def luoi(T, keys, ck, M_t, L, lg, ld, UG, co_cong):
    """Chạy lưới §5.2 trên mẫu của một nhiệt độ. Trả {(r, rt): {chon: {k: câu}, ...}}."""
    Lfn = lambda k, s: L.get((k, (s or "").strip()))
    R = {}
    for r in T.R_LUOI:
        for rt in (T.RT_LUOI if co_cong else (10 ** 9,)):
            chon, ly = {}, collections.Counter()
            for k in keys:
                d0 = ck[k]["sent"]
                cands = list(enumerate(M_t[k], 1))
                buoc = {"d0": d0, "cands": cands, "t": lg[k], "tp": ld[k],
                        "L": {s: Lfn(k, s) for s in [d0] + M_t[k]}}
                i, why = T.chon(buoc, r, rt)
                chon[k] = d0 if i == 0 else M_t[k][i - 1]
                ly[why] += 1
            R[(r, rt)] = {"chon": chon, "ly_do": dict(ly)}
    return R


def danh_gia(keys, ck, chon, UG, V=None, T=None):
    cuu = pha = doi = 0
    D = []
    for k in keys:
        d0 = ck[k]["sent"].strip()
        s = chon[k].strip()
        e0 = ck[k]["executable"]
        e1 = e0 if s == d0 else UG[(k, s)]
        doi += s != d0
        cuu += e1 > e0
        pha += e1 < e0
        D.append((k, e1 - e0))
    o = {"dung": 166 + cuu - pha, "exec": round(100 * (166 + cuu - pha) / 249, 2), "cuu": cuu, "pha": pha,
         "net": cuu - pha, "doi": doi, "coverage": round(100 * doi / 249, 2)}
    if T:
        m, lo, hi = T.boot_episode(D)
        o["delta_pp"], o["ktc95"] = round(m, 2), [round(lo, 2), round(hi, 2)]
    if V is not None:
        try:
            v0 = sum(V[(k, ck[k]["sent"].strip())] for k in keys)
            v1 = sum(V[(k, chon[k].strip())] for k in keys)
            o["venus_ck500"], o["venus_chon"], o["venus_delta"] = v0, v1, v1 - v0
        except KeyError:
            pass
    return o


def chon_tot(T, R):
    """Luật §5.3 của triad_t trên kết quả đã đánh giá."""
    tot_r = {}
    for (r, rt), o in sorted(R.items()):
        if r not in tot_r or T.khoa_chon(o) > T.khoa_chon(R[tot_r[r]]):
            tot_r[r] = (r, rt)
    best = None
    for r in sorted(tot_r):
        if best is None or T.khoa_chon(R[tot_r[r]]) > T.khoa_chon(R[best]):
            best = tot_r[r]
    return best


def chay_mot_nhiet(T, keys, ck, M_t, L, lg, ld, UG, V):
    out = {}
    for nhanh, cong in (("C1", False), ("C2", True)):
        R = luoi(T, keys, ck, M_t, L, lg, ld, UG, cong)
        E = {}
        for kk, x in R.items():
            E[kk] = {**danh_gia(keys, ck, x["chon"], UG, V, T), "ly_do": x["ly_do"]}
        best = chon_tot(T, E)
        out[nhanh] = {"luoi": {f"{r}_{'inf' if rt > 10**8 else rt}": o for (r, rt), o in E.items()},
                      "tot": list(best), "chon_tot": R[best]["chon"]}
    return out


def chon(a):
    """Trên Kaggle sau listener + UGround: chọn C2 tốt nhất mỗi nhiệt độ ⇒ preds cho UI-Venus."""
    T, recs, ck, keys, lg, ld, M, L, UG, V = nap_tat_ca(a.dir)
    thieu_L = sum(1 for t in NHIET for k in keys for s in M[t][k] if (s or "").strip() and (k, s.strip()) not in L)
    thieu_U = sum(1 for t in NHIET for k in keys for s in M[t][k]
                  if (s or "").strip() and s.strip() != ck[k]["sent"].strip() and (k, s.strip()) not in UG)
    assert thieu_L == 0 and thieu_U == 0, f"⛔ thiếu listener {thieu_L} · thiếu UGround {thieu_U}"
    can = {}
    for t in NHIET:
        o = chay_mot_nhiet(T, keys, ck, M[t], L, lg, ld, UG, None)
        b = o["C2"]["tot"]
        print(f"[chọn {t}] C2 tốt nhất r={b[0]} r_trust={b[1]} · "
              f"{ {x: y for x, y in o['C2']['luoi'][f'{b[0]}_{b[1]}'].items() if x != 'ly_do'} }", flush=True)
        for k, s in o["C2"]["chon_tot"].items():
            if s.strip() != ck[k]["sent"].strip():
                can.setdefault(k, [])
                if s.strip() not in can[k]:
                    can[k].append(s.strip())
    os.makedirs(f"{a.dir}/venus_lop", exist_ok=True)
    n = max([len(v) for v in can.values()] or [0])
    for j in range(n):
        with open(f"{a.dir}/venus_lop/vlop{j}.jsonl", "w", encoding="utf-8") as f:
            for k in sorted(can):
                if j < len(can[k]):
                    f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": can[k][j]},
                                       ensure_ascii=False) + "\n")
    print(f"[chọn] {sum(map(len, can.values()))} câu cần UI-Venus · {n} lớp", flush=True)


def da_dang(keys, ck, M_t):
    from metric_exec import canon_action
    import triad_t as T
    ds = [s for k in keys for s in M_t[k]]
    khac = sum((s or "").strip() != ck[k]["sent"].strip() for k in keys for s in M_t[k])
    uniq = [len({(s or "").strip() for s in M_t[k]}) for k in keys]
    dai = [len((s or "").split()) for s in ds]
    return {"n_cau": len(ds), "khac_greedy": khac, "khac_greedy_pct": round(100 * khac / len(ds), 1),
            "duy_nhat_trong_8_trung_vi": statistics.median(uniq), "duy_nhat_tb": round(sum(uniq) / len(uniq), 2),
            "cau_cham_hop_le_pct": round(100 * sum(canon_action(s) in ("tap", "long_press") and bool((s or "").strip())
                                                   and not T.lap_bat_thuong(s) for s in ds) / len(ds), 1),
            "so_tu_trung_vi": statistics.median(dai), "so_tu_max": max(dai),
            "rong": sum(not (s or "").strip() for s in ds), "tieng_viet": sum(bool(VIET.search(s or "")) for s in ds),
            "lap": sum(T.lap_bat_thuong(s) for s in ds),
            "khong_cham": sum(canon_action(s) not in ("tap", "long_press") for s in ds)}


def bao_cao(a):
    T, recs, ck, keys, lg, ld, M, L, UG, V = nap_tat_ca(a.dir, True)
    res = {}
    for t in NHIET:
        o = chay_mot_nhiet(T, keys, ck, M[t], L, lg, ld, UG, V)
        orc = sum(max([ck[k]["executable"]] + [UG.get((k, (s or "").strip()), 0) if (s or "").strip() != ck[k]["sent"].strip()
                                                else ck[k]["executable"] for s in M[t][k]]) for k in keys)
        o["C3_oracle"] = {"dung": orc, "headroom": orc - 166}
        o["da_dang"] = da_dang(keys, ck, M[t])
        b = tuple(o["C2"]["tot"])
        doi = []
        for k in keys:
            s = o["C2"]["chon_tot"][k]
            if s.strip() != ck[k]["sent"].strip():
                doi.append({"episode_id": k[0], "step_id": k[1], "ck500": ck[k]["sent"], "chon": s,
                            "L_ck500": L.get((k, ck[k]["sent"].strip())), "L_chon": L.get((k, s.strip())),
                            "loc_g": lg[k], "loc_d": ld[k], "ug_ck500": ck[k]["executable"], "ug_chon": UG[(k, s.strip())],
                            "venus_ck500": V.get((k, ck[k]["sent"].strip())), "venus_chon": V.get((k, s.strip()))})
        o["doi_cau_C2"] = doi
        del o["C1"]["chon_tot"], o["C2"]["chon_tot"]
        res[t] = o
        print(f"\n══ T={NHIET[t]} ══ đa dạng {o['da_dang']}")
        print(f"   C3 oracle {orc}/249 (headroom {orc - 166:+d})")
        for nh in ("C1", "C2"):
            print(f"   {nh}  r   r_trust cov%  đổi cứu phá  net  exec  Δpp [KTC95]  Venus")
            for kk, x in sorted(o[nh]["luoi"].items(), key=lambda z: tuple(int(v) if v != "inf" else 10**9 for v in z[0].split("_"))):
                dau = "◀" if kk == f"{o[nh]['tot'][0]}_{'inf' if o[nh]['tot'][1] > 10**8 else o[nh]['tot'][1]}" else ""
                print(f"       {kk:<10} {x['coverage']:5.1f} {x['doi']:3} {x['cuu']:3} {x['pha']:3} {x['net']:+4} "
                      f"{x['exec']:5.2f} {x['delta_pp']:+.2f} {x['ktc95']} {x.get('venus_delta', '—')} {dau}")
    if a.out:
        json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nĐã lưu {a.out}")


def main():
    ap = argparse.ArgumentParser()
    for f in ("--sample", "--lop", "--chon", "--bao-cao"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--bundle")
    ap.add_argument("--merged", default="/kaggle/working/s1_merged")
    ap.add_argument("--ckpt")
    ap.add_argument("--c1")
    ap.add_argument("--temp", type=float)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--kiem-greedy")
    ap.add_argument("--dir")
    ap.add_argument("--thu", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.sample:
        sample(a)
    elif a.lop:
        lop(a)
    elif a.chon:
        chon(a)
    elif a.bao_cao:
        bao_cao(a)


if __name__ == "__main__":
    main()
