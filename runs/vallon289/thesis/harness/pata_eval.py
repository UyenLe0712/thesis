# -*- coding: utf-8 -*-
"""
PATA · đánh giá một điểm lưu (report/185 §6 Stage H, §7b mốc 800, §8 cổng cuối). ⛔ Chỉ eval +
no_grad, tuyệt đối không cập nhật trọng số (§3).

  --mode diag   teacher-forced trên val400 (mặc định): CE_val · KL_val · Hit-in-box · mass trong
                box · lift so với CENTER prior và TRAIN-LOCATION prior · prompt ĐÚNG so với
                goal/history XÁO. In quyết định cổng H:
                    đi tiếp ⇔ cận dưới KTC MỘT PHÍA 90% của lift(mass) so với CẢ HAI prior > 0
                             VÀ cận dưới của mass(đúng) − mass(xáo) > 0
                (bootstrap cụm theo episode, 10.000 lần). Chạy cho điểm lưu S (chỉ CE), H, J.
  --mode gen    sinh câu tham lam trên probe40 / val600 với các biến thể bridge:
                    on   bridge bật (C1 bình thường)            off  tắt bridge trên CHÍNH điểm lưu
                Ghi preds_<variant>.jsonl đúng định dạng infer_branch.py (kèm gold_instruction)
                để score_run.py chấm `exec`. In: % câu đổi on↔off (không tính TARGET, §7b điều 2),
                tỉ lệ format hợp lệ, độ dài, lặp.
                swapD / swapR: ép α của bridge vào hộp phần tử gây nhiễu / hộp ngẫu nhiên
                (pata/val600_swap.jsonl, dựng bằng pata_swap.py) — §8 điều 5.

Chạy (GPU):
  python harness/pata_eval.py --ckpt <out>/ckpt-00800 --mode diag --split val400 --out <dir>
  python harness/pata_eval.py --ckpt <out>/ckpt-00800 --mode gen --split probe40 --variants on,off --out <dir>
Thử trên CPU với mô hình tí hon: thêm --tiny.
"""
import os, sys, json, math, time, random, argparse, collections
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pata_model as PM

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
SEED = 20260923


def load(a):
    from transformers import AutoProcessor
    from peft import PeftModel
    has_heads = os.path.exists(os.path.join(a.ckpt, "pata_heads.pt"))
    proc, m, inject, d_k, cdt = PM.load_base(a.tiny)
    m = PeftModel.from_pretrained(m, a.ckpt)
    m.eval()
    pata = None
    if has_heads:
        pata = PM.Pata(m, proc.tokenizer, inject=inject, d_k=d_k)
        pata.load_state_dict(torch.load(os.path.join(a.ckpt, "pata_heads.pt"), map_location="cpu"))
        pata.heads.eval()
    print(f"[điểm lưu] {a.ckpt} · đầu PATA: {'có' if pata else 'KHÔNG (điểm lưu S)'}", flush=True)
    return proc, m, pata, cdt


def records(a, split):
    p = os.path.join(a.data_root, "pata", f"{split}.jsonl")
    recs = [json.loads(l) for l in open(p, encoding="utf-8")]
    if a.tiny or a.only_local:
        recs = [r for r in recs if os.path.exists(os.path.join(a.data_root, r["image"]))]
    if a.limit:
        recs = recs[: a.limit]
    ocr = {}
    for l in open(os.path.join(a.data_root, "ocr.jsonl"), encoding="utf-8"):
        o = json.loads(l); ocr[o["image"]] = o
    for r in recs:
        r["_ocr"] = ocr.get(r["image"])
    print(f"[dữ liệu] {p} — {len(recs)} bước", flush=True)
    return recs


# ─────────────────────────────────────────────────────────────── prior
def train_location_prior(a, nb=32):
    """Histogram phủ box của Train-proper trên lưới nb×nb toạ độ chuẩn hoá (0 GPU)."""
    H = torch.zeros(nb, nb, dtype=torch.float64)
    for l in open(os.path.join(a.data_root, "pata", "train_proper.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if not r["kl_ok"]:
            continue
        x1, y1, x2, y2 = r["box"]
        c1, c2 = int(x1 / r["w"] * nb), min(int(math.ceil(x2 / r["w"] * nb)), nb)
        r1, r2 = int(y1 / r["h"] * nb), min(int(math.ceil(y2 / r["h"] * nb)), nb)
        c2, r2 = max(c2, c1 + 1), max(r2, r1 + 1)
        H[r1:r2, c1:c2] += 1.0 / ((r2 - r1) * (c2 - c1))
    return H / H.sum()


def prior_on_cells(kind, grid_thw, TL=None):
    _, gh, gw = [int(x) for x in grid_thw]
    mh, mw = gh // 2, gw // 2
    ys = (torch.arange(mh, dtype=torch.float64) + 0.5) / mh
    xs = (torch.arange(mw, dtype=torch.float64) + 0.5) / mw
    if kind == "center":
        s = 0.25
        p = torch.exp(-((ys[:, None] - 0.5) ** 2 + (xs[None, :] - 0.5) ** 2) / (2 * s * s))
    else:
        nb = TL.shape[0]
        p = TL[(ys * nb).long().clamp(max=nb - 1)][:, (xs * nb).long().clamp(max=nb - 1)]
    p = p.flatten()
    return p / p.sum()


def lower90(pairs, B=10000):
    """Cận dưới KTC MỘT PHÍA 90% của trung bình, bootstrap cụm theo episode. pairs = [(ep, v)]."""
    cl = collections.defaultdict(list)
    for e, v in pairs:
        cl[e].append(v)
    g = list(cl.values())
    rnd = random.Random(SEED)
    bs = []
    for _ in range(B):
        pick = [g[rnd.randrange(len(g))] for _ in range(len(g))]
        bs.append(sum(sum(x) for x in pick) / sum(len(x) for x in pick))
    bs.sort()
    mean = sum(v for _, v in pairs) / len(pairs)
    return mean, bs[int(0.10 * B)]


# ─────────────────────────────────────────────────────────────── diag
def diag(a, proc, model, pata, cdt):
    recs = records(a, a.split)
    dev = PM.parts(model)[2].embed_tokens.weight.device
    wt = pata is not None
    TL = train_location_prior(a) if wt else None
    # xáo goal/history: hoán vị cố định, mỗi bước nhận prompt của một episode KHÁC
    rnd = random.Random(SEED)
    perm = list(range(len(recs)))
    for _ in range(100):
        rnd.shuffle(perm)
        if all(recs[i]["episode_id"] != recs[perm[i]]["episode_id"] for i in range(len(recs))):
            break
    rows = []
    ce_s, tok = 0.0, 0
    for i0 in range(0, len(recs), a.bs):
        chunk = list(range(i0, min(i0 + a.bs, len(recs))))
        its = [PM.make_item(proc, recs[i], a.data_root, wt, pata.tid if wt else None) for i in chunk]
        b = PM.collate(its, proc.tokenizer.pad_token_id)
        with torch.no_grad(), torch.autocast(dev.type, dtype=cdt, enabled=dev.type == "cuda"):
            ce, nt, kl, nk, ex = PM.forward_losses(model, pata, b, need_ce=not a.no_ce, need_kl=wt,
                                                     truncate=(wt and a.no_ce))
            ce_s += float(ce); tok += nt
            las = [r["logalpha"].float().cpu() if r else None for r in (pata.last if wt else [])]
            if wt:
                sh = []
                for i in chunk:
                    r2 = dict(recs[i]); o = recs[perm[i]]
                    r2["goal"], r2["history"] = o["goal"], o["history"]
                    sh.append(PM.make_item(proc, r2, a.data_root, True, pata.tid))
                PM.forward_losses(model, pata, PM.collate(sh, proc.tokenizer.pad_token_id),
                                  need_ce=False, need_kl=False, truncate=True)
                las_sh = [r["logalpha"].float().cpu() if r else None for r in pata.last]
        if not wt:
            continue
        for j, i in enumerate(chunk):
            p = its[j]["ptarget"]
            if p is None or las[j] is None:
                continue
            pos = p > 0
            a_ = las[j].exp()
            pc = prior_on_cells("center", its[j]["image_grid_thw"])
            pt = prior_on_cells("train", its[j]["image_grid_thw"], TL)
            rows.append({"ep": recs[i]["episode_id"],
                         "kl": float(PM.kl_target_alpha(p, las[j])),
                         "mass": float(a_[pos].sum()), "hit": float(pos[int(a_.argmax())]),
                         "mass_center": float(pc[pos].sum()), "mass_train": float(pt[pos].sum()),
                         "hit_center": float(pos[int(pc.argmax())]), "hit_train": float(pos[int(pt.argmax())]),
                         "mass_shuf": float(las_sh[j].exp()[pos].sum()),
                         "hit_shuf": float(pos[int(las_sh[j].argmax())])})
        print(f"  {min(i0 + a.bs, len(recs))}/{len(recs)}", flush=True)

    res = {"ckpt": a.ckpt, "split": a.split, "n": len(recs)}
    if not a.no_ce:
        res["CE_val"] = ce_s / max(tok, 1)
    if rows:
        m = lambda k: sum(r[k] for r in rows) / len(rows)
        res.update({k: m(k) for k in ("kl", "mass", "hit", "mass_center", "mass_train", "hit_center",
                                      "hit_train", "mass_shuf", "hit_shuf")})
        res["KL_val"] = res.pop("kl")
        L = {}
        for name, k in (("lift_center", "mass_center"), ("lift_train", "mass_train"),
                        ("dung_vs_xao", "mass_shuf")):
            L[name] = lower90([(r["ep"], r["mass"] - r[k]) for r in rows])
            res[name] = {"mean": L[name][0], "lower90": L[name][1]}
        res["cong_H_dat"] = all(L[k][1] > 0 for k in L)
    os.makedirs(a.out, exist_ok=True)
    tag = a.tag or os.path.basename(os.path.normpath(a.ckpt))
    json.dump(res, open(os.path.join(a.out, f"diag_{tag}_{a.split}.json"), "w"), indent=1)
    with open(os.path.join(a.out, f"diag_{tag}_{a.split}_rows.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print("=" * 70)
    for k, v in res.items():
        print(f"  {k:14} {v}")
    if rows:
        print("⇒ CỔNG H:", "ĐẠT — đi tiếp C1" if res["cong_H_dat"] else
              "KHÔNG ĐẠT — dừng (bridge không cứu được localizer chỉ học prior)")


# ─────────────────────────────────────────────────────────────── gen
def fmt_ok(s):
    w = s.split()
    return (0 < len(w) <= 40 and "\n" not in s and "<" not in s
            and max(collections.Counter(w).values()) <= 4)


def gen(a, proc, model, pata, cdt):
    """Sinh câu tham lam. Biến thể:
         on     bridge bật (C1 bình thường)        off    tắt bridge trên CHÍNH điểm lưu
         swapD  bridge bật, α ÉP = đích patch của hộp phần tử gây nhiễu (pata/val600_swap.jsonl)
         swapR  bridge bật, α ÉP = đích patch của hộp ngẫu nhiên lấy từ bước khác (cùng tệp)
       swapD/swapR chỉ chạy trên các bước có trong val600_swap.jsonl (§8 điều 5).
       Ghi DẦN từng lô + nối tiếp được (mất máy giữa lượt không mất phần đã sinh)."""
    from build_branch_data import prompt_body, SYS
    from PIL import Image
    recs_all = records(a, a.split)
    dev = PM.parts(model)[2].embed_tokens.weight.device
    wt = pata is not None
    proc.tokenizer.padding_side = "left"
    swap = {}
    sp = os.path.join(a.data_root, "pata", f"{a.split}_swap.jsonl")
    if os.path.exists(sp):
        for l in open(sp, encoding="utf-8"):
            x = json.loads(l); swap[(x["episode_id"], x["step_id"])] = x
    os.makedirs(a.out, exist_ok=True)
    tag = a.tag or os.path.basename(os.path.normpath(a.ckpt))
    out = {}
    for var in a.variants.split(","):
        if var not in ("on", "off", "swapD", "swapR"):
            sys.exit(f"biến thể chưa hỗ trợ: {var}")
        if var.startswith("swap"):
            assert wt, "swap cần điểm lưu có đầu PATA (C1)"
            assert swap, f"thiếu {sp} — chạy harness/pata_swap.py rồi dựng lại gói"
            recs = [r for r in recs_all if (r["episode_id"], r["step_id"]) in swap]
        else:
            recs = recs_all
        if wt:
            pata.bridge_enabled = (var != "off")
        fp = os.path.join(a.out, f"preds_{tag}_{a.split}_{var}.jsonl")
        xong = {}
        if os.path.exists(fp):
            for l in open(fp, encoding="utf-8"):
                try:
                    x = json.loads(l); xong[(x["episode_id"], x["step_id"])] = x
                except Exception:
                    pass
        todo = [r for r in recs if (r["episode_id"], r["step_id"]) not in xong]
        print(f"[{var}] {len(recs)} bước · đã có {len(xong)} · còn {len(todo)}", flush=True)
        # ⛔ MỞ–GHI–ĐÓNG TỪNG LÔ: --out nằm trên Drive (FUSE chỉ đẩy lên cloud khi tệp ĐÓNG). Mở một lần
        #    cho cả biến thể thì mất máy giữa chừng là mất trọn tệp (đã trả giá 24/8, lượt CE2).
        for i0 in range(0, len(todo), a.bs):
            ch = todo[i0: i0 + a.bs]
            texts, imgs = [], []
            for r in ch:
                imgs.append(Image.open(os.path.join(a.data_root, r["image"])).convert("RGB"))
                body = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, r["_ocr"])
                texts.append(PM.prompt_only(proc, SYS, body, None, wt))
            inp = proc(text=texts, images=imgs, return_tensors="pt", padding=True).to(dev)
            if var.startswith("swap"):
                k = "box_D" if var == "swapD" else "box_R"
                pata.alpha_override = [
                    PM.patch_target(swap[(r["episode_id"], r["step_id"])][k], r["w"], r["h"],
                                    im.width, im.height, inp["image_grid_thw"][j].cpu())
                    for j, (r, im) in enumerate(zip(ch, imgs))]
            with torch.no_grad(), torch.autocast(dev.type, dtype=cdt, enabled=dev.type == "cuda"):
                g = model.generate(**inp, max_new_tokens=a.max_new, do_sample=False, use_cache=True,
                                   temperature=None, top_p=None)
            if wt:
                pata.alpha_override = None
            with open(fp, "a", encoding="utf-8") as f:
                for r, seq in zip(ch, g):
                    txt = proc.decode(seq[inp["input_ids"].shape[1]:], skip_special_tokens=True).strip()
                    x = {"episode_id": r["episode_id"], "step_id": r["step_id"], "image": r["image"],
                         "app": "", "gold_instruction": r["target_instruction"], "action": r["action"],
                         "raw": txt, "pred": txt.split("\n")[0].strip(), "variant": var, "ckpt": a.ckpt}
                    f.write(json.dumps(x, ensure_ascii=False) + "\n")
                    xong[(r["episode_id"], r["step_id"])] = x
            print(f"  [{var}] {len(xong)}/{len(recs)}", flush=True)
        out[var] = xong
    print("=" * 70)
    for var, rows in out.items():
        n = len(rows)
        ok = sum(fmt_ok(x["pred"]) for x in rows.values())
        ln = sum(len(x["pred"].split()) for x in rows.values()) / max(n, 1)
        print(f"  {var:5} format hợp lệ {ok}/{n} = {ok / max(n, 1):.1%} · độ dài TB {ln:.1f} từ")
    if "on" in out and "off" in out:
        ks = set(out["on"]) & set(out["off"])
        d = sum(out["on"][k]["pred"] != out["off"][k]["pred"] for k in ks)
        print(f"  câu ĐỔI khi tắt bridge: {d}/{len(ks)} = {d / max(len(ks), 1):.1%}  "
              f"(§7b điều 2 cần ≥ 30% ở mốc 800)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--mode", choices=["diag", "gen"], default="diag")
    ap.add_argument("--split", default="val400", help="val400 · val600 · probe40")
    ap.add_argument("--variants", default="on,off")
    ap.add_argument("--data-root", default=os.path.join(HERE, "dg1_cache", "train_ac"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--bs", type=int, default=4)
    ap.add_argument("--max-new", type=int, default=96)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-ce", action="store_true", help="bỏ CE (điểm lưu H: CE không có nghĩa)")
    ap.add_argument("--tiny", action="store_true")
    ap.add_argument("--only-local", action="store_true")
    ap.add_argument("--tag", default=None, help="tên trong tệp ra (S/H/J/C1). Mặc định = tên thư mục điểm "
                    "lưu — mà S, H, J đều là 'final' ⇒ ĐÈ nhau nếu cùng --out. Luôn truyền --tag.")
    a = ap.parse_args()
    if a.split == "val600" and a.mode == "gen":
        print("⚠️  val600 = tập CỔNG CUỐI. Chỉ chạy MỘT lần sau khi hết epoch C1 (§7b).", flush=True)
    proc, model, pata, cdt = load(a)
    (diag if a.mode == "diag" else gen)(a, proc, model, pata, cdt)


if __name__ == "__main__":
    main()
