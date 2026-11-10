# -*- coding: utf-8 -*-
"""Vì sao GRPO + CIDEr-D thấp CIDEr-D trên test (8/11/2026) — 0 GPU, CPU + Java 8.

    python -u cider_thuong_8_11.py --runs <thư mục có rows_*.jsonl, score_*_raw.jsonl> --train <p1_train_rows.jsonl> \
        --out ../runs/luoi/8_11/cider_thuong/cider_thuong_8_11.json [--B 2000]

Chấm lại câu test đã sinh của mọi lượt bằng năm biến thể CIDEr-D, tách hai chỗ khác giữa lúc thưởng và lúc chấm:
  coco          pycocoevalcap Cider, PTBTokenizer, df từ câu chuẩn TẬP KIỂM (số đã báo; tự kiểm 100·TB trùng chu_luoi_8_11)
  ptb_df_kiem   lớp CiderD của grpo_luoi.py trên chuỗi đã PTB (tách theo khoảng trắng), df tập kiểm
                (tự kiểm: phải trùng coco từng bước ⇒ công thức CiderD đúng, mọi khác biệt còn lại là df và tách từ)
  tok_df_kiem   tách từ của thưởng, df tập kiểm          (chỉ đổi cách tách từ so với coco)
  ptb_df_day    PTB, df câu chuẩn tập dạy                (chỉ đổi df so với coco)
  thuong        tách từ của thưởng, df tập dạy = đúng hàm thưởng lúc train (thang ×100 như coco)
  thuong_du     thưởng đầy đủ lúc train: CIDEr-D/10 − 0,02·max(0, số từ câu − số từ câu chuẩn − 3), câu trống 0 (×100)
Mỗi biến thể: điểm từng lượt + KTC95 bootstrap cụm app (B, hạt 20261027) cho mọi lượt so A/A và so ck500, hạng các lượt.
Kèm mô tả: số từ TB, tỉ lệ câu trùng câu chuẩn. Một hạt giống, hậu kiểm.
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_luoi as GL                     # noqa: E402  đúng lớp CiderD và hàm tách từ lúc thưởng
from grpo_luoi import CiderD, tok          # noqa: E402
from grpo_spice import MU, nwords          # noqa: E402
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer   # noqa: E402
from pycocoevalcap.cider.cider import Cider                     # noqa: E402

AA = "GRPO + SPICE (A/A)"
AC = {"S1/101": "score_s1_seed101_raw.jsonl", "ck500": "score_ck500_test_raw.jsonl",
      "ck500/202": "score_ck500_s202_test_raw.jsonl", "xao101": "score_ck500_xao101_test_raw.jsonl",
      "SCST + SPICE": "rows_scst_spice_101.jsonl", "GRPO + CIDEr-D": "rows_grpo_cider_101.jsonl",
      "GRPO + METEOR": "rows_grpo_meteor_101.jsonl", "GRPO + ROUGE-L": "rows_grpo_rougel_101.jsonl",
      "SFT tiếp": "rows_sft_tiep_101.jsonl", "REINFORCE + SPICE": "rows_reinforce_spice_101.jsonl",
      "RLOO + SPICE": "rows_rloo_spice_101.jsonl", AA: "rows_grpo_spice_aa_101.jsonl"}
# 100·TB CIDEr-D đã báo (chu_luoi_8_11.json, chu_luoi_8_11b.json)
DA = {"S1/101": 416.12, "ck500": 430.05, "xao101": 418.13, "SCST + SPICE": 430.89, "GRPO + CIDEr-D": 424.52,
      "GRPO + METEOR": 426.61, "GRPO + ROUGE-L": 432.81, "SFT tiếp": 425.79, "REINFORCE + SPICE": 426.11,
      "RLOO + SPICE": 422.1, AA: 430.92, "ck500/202": 431.22}
BIEN = ("coco", "ptb_df_kiem", "tok_df_kiem", "ptb_df_day", "thuong", "thuong_du")


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def kh(r):
    return (str(r["episode_id"]), str(r["step_id"]))


class TachTrang:
    """Tạm thay hàm tách từ trong grpo_luoi bằng tách theo khoảng trắng (chuỗi đã qua PTB): CiderD.score gọi tok() bên trong."""
    def __enter__(self):
        GL.tok = str.split

    def __exit__(self, *a):
        GL.tok = tok


def ptb(xs):
    g = PTBTokenizer().tokenize({i: [{"caption": x}] for i, x in enumerate(xs)})
    return [g[i][0] for i in range(len(xs))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--train", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--B", type=int, default=2000)
    a = ap.parse_args()
    R = Path(a.runs)
    out = {"B": a.B, "ghi_chu": "bootstrap cụm app; một hạt giống; hậu kiểm"}

    tr = [json.loads(l) for l in open(a.train, encoding="utf-8")]
    refs_day = [(r.get("target_instruction") or "").strip() for r in tr]
    refs_day = [r for r in refs_day if r]
    out["train"] = dict(md5=hashlib.md5(open(a.train, "rb").read()).hexdigest(), n_dong=len(tr), n_cau=len(refs_day))
    log("tập dạy", out["train"])

    goc = [json.loads(l) for l in open(R / AC["S1/101"], encoding="utf-8")]
    thu_tu = [kh(r) for r in goc]
    app = [r.get("app") or f"ep{r['episode_id']}" for r in goc]
    rows = {}
    for t, f in AC.items():
        D = {kh(r): r for r in map(json.loads, open(R / f, encoding="utf-8"))}
        assert set(D) == set(thu_tu), f"⛔ {t}: tập bước khác S1/101"
        rows[t] = [D[k] for k in thu_tu]
    ref = [(r.get("gold_instruction") or "").strip() for r in rows["S1/101"]]
    for t in AC:
        assert [(r.get("gold_instruction") or "").strip() for r in rows[t]] == ref, f"⛔ {t}: câu chuẩn khác"

    ref_ptb = ptb(ref)
    day_ptb = ptb(refs_day)
    with TachTrang():
        C = {"ptb_df_kiem": CiderD(ref_ptb), "ptb_df_day": CiderD(day_ptb)}
    C.update(tok_df_kiem=CiderD(ref), thuong=CiderD(refs_day))
    S = {}
    for t in AC:
        t0 = time.time()
        hyp = [(r.get("sent") or "").strip() for r in rows[t]]
        hp = ptb(hyp)
        g = {i: [ref_ptb[i]] for i in range(len(ref))}
        h = {i: [hp[i]] for i in range(len(ref))}
        d = {"coco": np.array(Cider().compute_score(g, h)[1], float)}
        with TachTrang():
            d["ptb_df_kiem"] = np.array([C["ptb_df_kiem"].score(x, y) for x, y in zip(hp, ref_ptb)])
            d["ptb_df_day"] = np.array([C["ptb_df_day"].score(x, y) for x, y in zip(hp, ref_ptb)])
        d["tok_df_kiem"] = np.array([C["tok_df_kiem"].score(x, y) for x, y in zip(hyp, ref)])
        d["thuong"] = np.array([C["thuong"].score(x, y) if x else 0.0 for x, y in zip(hyp, ref)])
        d["thuong_du"] = np.array([0.0 if not x else s / 10.0 - MU * max(0, nwords(x) - nwords(y) - 3)
                                   for x, y, s in zip(hyp, ref, d["thuong"])]) * 10.0
        S[t] = d
        out.setdefault("mo_ta", {})[t] = dict(
            so_tu=float(np.mean([nwords(x) for x in hyp])), trung_chuan=float(np.mean([x == y for x, y in zip(hyp, ref)])),
            trong=int(sum(not x for x in hyp)),
            lech_ptb_df_kiem_vs_coco=float(np.max(np.abs(d["ptb_df_kiem"] - d["coco"]))))
        log(t, {b: round(100 * d[b].mean(), 2) for b in BIEN}, f"{time.time()-t0:.0f}s")

    # tự kiểm
    loi = [f"{t} coco {100*S[t]['coco'].mean():.2f} ≠ {v}" for t, v in DA.items() if abs(100 * S[t]["coco"].mean() - v) > 0.1]
    loi += [f"{t} ptb_df_kiem lệch coco từng bước tới {out['mo_ta'][t]['lech_ptb_df_kiem_vs_coco']:.2e}"
            for t in AC if out["mo_ta"][t]["lech_ptb_df_kiem_vs_coco"] > 1e-6]
    out["tu_kiem"] = loi or "đạt"
    log("tự kiểm:", out["tu_kiem"])
    if loi:
        json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        sys.exit("⛔ DỪNG: " + " · ".join(loi))

    cl = {}
    for i, c in enumerate(app):
        cl.setdefault(c, []).append(i)
    cum = [np.array(v) for v in cl.values()]
    G = len(cum)
    so = [(t, AA) for t in AC if t != AA] + [(t, "ck500") for t in AC if t not in ("ck500", AA)]
    rng = np.random.default_rng(20261027)
    bs = {b: {t: [] for t in AC} for b in BIEN}
    t0 = time.time()
    for k in range(a.B):
        idx = np.concatenate([cum[j] for j in rng.integers(0, G, G)])
        for b in BIEN:
            for t in AC:
                bs[b][t].append(100 * S[t][b][idx].mean())
        if (k + 1) % 500 == 0:
            log(f"bootstrap {k+1}/{a.B} · {time.time()-t0:.0f}s")
    out["diem"], out["so"], out["hang"] = {}, {}, {}
    for b in BIEN:
        out["diem"][b] = {t: dict(diem=round(100 * S[t][b].mean(), 2), lo=round(float(np.percentile(bs[b][t], 2.5)), 2),
                                  hi=round(float(np.percentile(bs[b][t], 97.5)), 2)) for t in AC}
        out["so"][b] = {}
        for x, y in so:
            dd = np.array(bs[b][x]) - np.array(bs[b][y])
            p = 2 * min((dd <= 0).mean(), (dd >= 0).mean())
            out["so"][b][f"{x} − {y}"] = dict(delta=round(100 * (S[x][b].mean() - S[y][b].mean()), 2),
                                             lo=round(float(np.percentile(dd, 2.5)), 2),
                                             hi=round(float(np.percentile(dd, 97.5)), 2), p=round(float(min(1.0, p)), 4))
        out["hang"][b] = sorted(AC, key=lambda t: -S[t][b].mean())
        log(b, "hạng:", " > ".join(out["hang"][b][:5]), "| GRPO+CIDEr-D − A/A:", out["so"][b][f"GRPO + CIDEr-D − {AA}"])
    # tương quan từng bước giữa thưởng và số báo, trên GRPO + CIDEr-D
    x = S["GRPO + CIDEr-D"]
    out["tuong_quan_thuong_coco"] = float(np.corrcoef(x["thuong"], x["coco"])[0, 1])
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log("[xong] ghi", a.out)


if __name__ == "__main__":
    main()
