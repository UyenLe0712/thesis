# -*- coding: utf-8 -*-
"""Đọc kết quả chấm TEST một lần của GRPO SPICE checkpoint-500 (action 258, 2/10/2026) — 0 GPU.

    ~/.venvs/thesis/bin/python harness/grpo_spice_test_doc.py      # cần Java 8 cho SPICE

So ck500 với S1/101 trên cùng 4.463 bước click, ghép cặp theo (episode_id, step_id).
Dùng lại đúng hàm luật/bootstrap của `d3_ktc.py` (cụm = app, G = 1.091, như mọi KTC trong luận văn);
thêm bản cụm = episode làm độ nhạy (258 nói bootstrap theo episode).

Tự kiểm TRƯỚC khi in số ck500 (lệch là dừng):
  · S1 exec 59,11 và KTC khớp `score_s1_seed101.json`; S1 SPICE 44,37 khớp `text_metrics_coco.json`
  · ck500 KTC exec khớp `score_ck500_test.json` của Kaggle
  · câu trong tệp thô ck500 trùng `pred_ck500_test.jsonl` từng ký tự
Luật đọc khoá trước ở 258 §0, in nguyên văn hàng rơi vào.
"""
import collections, glob, json, math, os, sys

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]

import luat_d3 as L
import score_run as S
from d3_ktc import ktc, mcnemar
from luat_aitw_day_du import aitw_full

G = os.path.join(L.RUNS, "grpo_spice")
NHANH = {"S1/101": "score_s1_seed101_raw.jsonl", "ck500": "grpo_spice/score_ck500_test_raw.jsonl"}
DONG_TU_KHONG_CHAM = ("swipe", "scroll", "go back", "navigate", "press back", "type", "enter", "open", "wait")


def nap(ten):
    R = L.nap(os.path.join(L.RUNS, NHANH[ten]))
    return R, {k: dict(L.luat(r, k), aitwf=aitw_full(r, k), aok=int(bool(r.get("action_ok"))),
                       sent=(r.get("sent") or "").strip(), gold=(r.get("gold_instruction") or "").strip(),
                       cum=r.get("app") or f"ep{r['episode_id']}", ep=f"ep{r['episode_id']}")
               for k, r in R.items()}


def spice_tung_cau(hyp, ref):
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.spice.spice import Spice
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
    c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
    tb, ds = Spice().compute_score(g, c)
    return 100 * tb, [100 * d["All"]["f"] if not math.isnan(d["All"]["f"]) else 0.0 for d in ds]


def mo_dau(s):
    s = s.lower()
    return next((v for v in DONG_TU_KHONG_CHAM if s.startswith(v)), "click/tap/khác")


def main():
    loi = []
    R0, A = nap("S1/101")
    R1, B = nap("ck500")
    K = list(A)
    assert len(K) == 4463 and set(K) == set(B), "quần thể phải là 4.463 bước chung"
    cum_app = {k: A[k]["cum"] for k in K}
    cum_ep = {k: A[k]["ep"] for k in K}

    # ── tự kiểm ──
    P = {(str(d["episode_id"]), str(d["step_id"])): d["pred"].strip()
         for d in map(json.loads, open(os.path.join(G, "pred_ck500_test.jsonl"), encoding="utf-8"))}
    lech = [k for k in K if P.get(k, None) != B[k]["sent"]]
    if lech:
        loi.append(f"{len(lech)} bước câu tệp thô ≠ pred_ck500_test")
    for ten, X, f in (("S1/101", A, "score_s1_seed101.json"), ("ck500", B, "grpo_spice/score_ck500_test.json")):
        p, lo, hi, g = ktc(K, lambda k, c: X[k][c], "vor", cum_app)
        ci = json.load(open(os.path.join(L.RUNS, f)))["ci_voronoi"]
        print(f"[tự kiểm] {ten:7s} exec {p:.2f} [{lo:.2f}; {hi:.2f}] · {f} [{100*ci[0]:.2f}; {100*ci[1]:.2f}] · G {g}")
        if abs(lo - 100 * ci[0]) > 0.006 or abs(hi - 100 * ci[1]) > 0.006:
            loi.append(f"KTC exec {ten} lệch {f}")
    if abs(100 * sum(A[k]["vor"] for k in K) / 4463 - 59.11) > 0.006:
        loi.append("S1 exec ≠ 59,11")

    print("\n[SPICE] chạy Java, ~vài phút mỗi nhánh …", flush=True)
    sp = {}
    for ten, X in (("S1/101", A), ("ck500", B)):
        tb, ds = spice_tung_cau([X[k]["sent"] for k in K], [X[k]["gold"] for k in K])
        sp[ten] = (tb, dict(zip(K, ds)))
        print(f"  {ten:7s} SPICE {tb:.2f}", flush=True)
    s1_ref = json.load(open(os.path.join(L.RUNS, "text_metrics_coco.json")))["S1/101"]["spice"]
    if abs(sp["S1/101"][0] - s1_ref) > 0.006:
        loi.append(f"S1 SPICE {sp['S1/101'][0]:.2f} ≠ {s1_ref}")
    if loi:
        sys.exit("⛔ DỪNG, đường đọc sai — KHÔNG đọc số ck500: " + " · ".join(loi))
    print("✅ tự kiểm đạt: S1 exec 59,11 · SPICE 44,37 · KTC khớp Kaggle · câu khớp tệp dự đoán\n")

    for ten, X in (("S1/101", A), ("ck500", B)):
        X_sp = sp[ten][1]
        for k in K:
            X[k]["spice"] = X_sp[k] / 100      # ktc() tự nhân 100
    out = {"diem": {}, "so": {}}
    print(f"{'thước':12s} {'S1/101':>8s} {'ck500':>8s} {'Δ':>7s} {'KTC95 Δ (cụm app)':>20s} {'KTC95 Δ (cụm episode)':>23s} {'b':>4s} {'c':>4s} {'p McNemar':>10s}")
    for cot, ten in (("vor", "exec"), ("spice", "SPICE"), ("aok", "action_ok"), ("d3", "D.3"), ("aitwf", "AitW đầy đủ")):
        a = 100 * sum(A[k][cot] for k in K) / 4463
        b_ = 100 * sum(B[k][cot] for k in K) / 4463
        d, lo, hi, _ = ktc(K, lambda k, c: B[k][c] - A[k][c], cot, cum_app)
        _, elo, ehi, _ = ktc(K, lambda k, c: B[k][c] - A[k][c], cot, cum_ep)
        if cot == "spice":
            b = c = 0; p = float("nan")
        else:
            b, c, _, p = mcnemar(K, A, B, cot)     # b = S1 trúng ck500 trượt (phá), c = ngược lại (cứu)
        out["diem"][ten] = dict(S1=round(a, 2), ck500=round(b_, 2))
        out["so"][ten] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2), lo_ep=round(elo, 2),
                              hi_ep=round(ehi, 2), pha=b, cuu=c, p=p)
        print(f"{ten:12s} {a:8.2f} {b_:8.2f} {d:+7.2f}   [{lo:+6.2f}; {hi:+6.2f}]      [{elo:+6.2f}; {ehi:+6.2f}]"
              f"   {b:4d} {c:4d} {p:10.2e}")

    # ── phân rã Δexec theo action_ok ──
    cuu = [k for k in K if A[k]["vor"] == 0 and B[k]["vor"] == 1]
    pha = [k for k in K if A[k]["vor"] == 1 and B[k]["vor"] == 0]
    cuu_aok = [k for k in cuu if A[k]["aok"] == 0]
    pha_aok = [k for k in pha if B[k]["aok"] == 0]
    print(f"\n[phân rã exec] cứu {len(cuu)} (trong đó S1 sai loại thao tác: {len(cuu_aok)}) · "
          f"phá {len(pha)} (trong đó ck500 sai loại thao tác: {len(pha_aok)})")
    rong_aok = len(cuu_aok) - len(pha_aok)
    rong_dv = (len(cuu) - len(cuu_aok)) - (len(pha) - len(pha_aok))
    print(f"  ròng từ sửa loại thao tác: {rong_aok:+d} bước ({100*rong_aok/4463:+.2f} pp) · "
          f"ròng từ đổi phần tử (cả hai đúng loại thao tác): {rong_dv:+d} bước ({100*rong_dv/4463:+.2f} pp)")
    ca2 = [k for k in K if A[k]["aok"] and B[k]["aok"]]
    print(f"  exec trên {len(ca2)} bước cả hai đúng loại thao tác: S1 {100*sum(A[k]['vor'] for k in ca2)/len(ca2):.2f}"
          f" · ck500 {100*sum(B[k]['vor'] for k in ca2)/len(ca2):.2f}")
    out["phan_ra"] = dict(cuu=len(cuu), pha=len(pha), cuu_aok=len(cuu_aok), pha_aok=len(pha_aok),
                          rong_aok=rong_aok, rong_dinh_vi=rong_dv, n_ca2_dung=len(ca2))
    print("  câu mở đầu (bước click):",
          "S1", dict(collections.Counter(mo_dau(A[k]["sent"]) for k in K).most_common(5)),
          "· ck500", dict(collections.Counter(mo_dau(B[k]["sent"]) for k in K).most_common(5)))
    print(f"  câu trùng S1: {sum(A[k]['sent'] == B[k]['sent'] for k in K)}/4463 · câu rỗng S1 "
          f"{sum(not A[k]['sent'] for k in K)} · ck500 {sum(not B[k]['sent'] for k in K)} · số từ TB "
          f"S1 {sum(len(A[k]['sent'].split()) for k in K)/4463:.2f} · ck500 {sum(len(B[k]['sent'].split()) for k in K)/4463:.2f}")

    # ── kiểm hoà: 20 câu S1 hoà vs S1 đã công bố ──
    H = [json.loads(l) for l in open(os.path.join(G, "kiem_hoa_test.jsonl"), encoding="utf-8")]
    print("\n[kiểm hoà] câu S1 hoà khác câu S1 đã công bố:")
    for h in H:
        k = (str(h["episode_id"]), str(h["step_id"]))   # khoá luat_d3 là chuỗi
        if h["pred"].strip() != A[k]["sent"]:
            print(f"  {k}: công bố {A[k]['sent']!r} · exec {A[k]['vor']}\n  {' '*len(str(k))}  hoà     {h['pred']!r}"
                  f" · ck500 {B[k]['sent']!r} exec {B[k]['vor']}")

    # ── luật 258 §0 ──
    e, s = out["so"]["exec"], out["so"]["SPICE"]
    if e["delta"] > 0 and e["lo"] > 0 and s["delta"] > 0:
        hang = "Hàng 1: giữ checkpoint 500, được báo là hơn S1 trên cả hai metric của lượt này."
    elif e["delta"] > 0 and e["lo"] > 0 and s["delta"] < 0:
        hang = "Hàng 2: đánh đổi — bấm hơn, câu xa câu người hơn. Không gọi là GRPO thưởng SPICE đã đạt."
    else:
        hang = "Hàng 3: Δexec ≤ 0 hoặc KTC chứa 0 ⇒ không hơn S1 trên tập kiểm. Dừng. Giữ bảng luận văn."
    print("\n[luật 258 §0]", hang)
    out["hang_258"] = hang
    p = os.path.join(G, "test_ck500_doc.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", os.path.relpath(p))


if __name__ == "__main__":
    main()
