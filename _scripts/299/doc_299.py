# -*- coding: utf-8 -*-
"""299 - đọc kết quả chấm TEST bước chạm của A2 (GRPO thưởng CIDEr-D) so với ck500 (GRPO thưởng SPICE) và S1/101.

0 GPU. Thước vị trí chạy được trên Mac (_scripts/_venv) lẫn WSL. Thước chữ (--chu) cần pycocoevalcap + Java 8.
  python doc_299.py --kho <thesis-master> --a2 <thư mục kết quả Kaggle>          # thước vị trí
  python doc_299.py --kho <thesis-master> --a2 <thư mục kết quả Kaggle> --chu    # thêm thước chữ
  python doc_299.py --kho <thesis-master> --gia                                  # chạy khô: ck500 giả làm A2_500, S1 giả làm A2_1000
Tự kiểm trước khi in số A2 (lệch là dừng): S1 và ck500 ra đúng sáu số vị trí đã công bố; ck500 - S1 exec ra
+1,55 [+0,80; +2,33]; KTC exec từng nhánh khớp tệp json của Kaggle; câu trong tệp thô trùng tệp dự đoán.
"""
import argparse, glob, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--kho", default=None, help="thư mục kho thesis-master (có harness/ và runs/)")
ap.add_argument("--a2", default=None, help="thư mục chứa tệp Kaggle của lượt 299 (đã giải nén)")
ap.add_argument("--chu", action="store_true", help="tính thêm thước chữ (cần pycocoevalcap + Java 8)")
ap.add_argument("--bert", action="store_true", help="cùng --chu: thêm BERTScore (chậm)")
ap.add_argument("--gia", action="store_true", help="chạy khô bằng tệp đã có")
a = ap.parse_args()

KHO = a.kho or next((p for p in ("thesis-master", ".", "..") if os.path.isdir(os.path.join(p, "harness"))), None)
assert KHO and os.path.isdir(os.path.join(KHO, "harness")), "🔴 không thấy kho: truyền --kho <thư mục có harness/ và runs/>"
KHO = os.path.abspath(KHO)
RUNS = os.path.join(KHO, "runs")
sys.path.insert(0, os.path.join(KHO, "harness"))
J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]

import luat_d3 as L
from d3_ktc import ktc, mcnemar                    # đúng hàm bootstrap cụm app đã sinh mọi KTC trong luận văn
from luat_aitw_day_du import aitw_full
from luat_aitw_moi_hop import aitw_moi_hop

GOC = {"S1/101": ("score_s1_seed101_raw.jsonl", "score_s1_seed101.json", "preds_s1_seed101.jsonl"),
       "ck500": ("grpo_spice/score_ck500_test_raw.jsonl", "grpo_spice/score_ck500_test.json",
                 "grpo_spice/pred_ck500_test.jsonl")}
TEP = {t: tuple(os.path.join(RUNS, x) for x in v) for t, v in GOC.items()}
A2 = None
if a.gia:
    TEP["A2_500"], TEP["A2_1000"] = TEP["ck500"], TEP["S1/101"]
else:
    A2 = os.path.abspath(a.a2 or os.path.join(os.path.dirname(KHO), "_kaggle_out", "299"))
    for t in ("A2_500", "A2_1000"):
        TEP[t] = (f"{A2}/score_{t}_test_raw.jsonl", f"{A2}/score_{t}_test.json", f"{A2}/pred_{t}_test.jsonl")
    thieu = [p for t in ("A2_500", "A2_1000") for p in TEP[t] if not os.path.exists(p)]
    assert not thieu, f"🔴 thiếu tệp Kaggle: {thieu}"

NH = ["S1/101", "ck500", "A2_500", "A2_1000"]
MOC = {"S1/101": dict(vor=59.11, d3=65.49, aitwf=74.37, moi=81.04, d14_truc=67.24, aok=94.35),
       "ck500": dict(vor=60.65, d3=67.02, aitwf=76.25, moi=82.90, d14_truc=68.90, aok=95.97)}
COT = [("vor", "Executability"), ("d3", "Hộp phần tử (D.3)"), ("aitwf", "AitW"), ("moi", "AitW cận trên"),
       ("d14_truc", "+14% theo trục"), ("aok", "Đúng loại thao tác")]
SO = [("A2_500", "ck500"), ("A2_1000", "ck500"), ("A2_500", "S1/101"), ("A2_1000", "S1/101"),
      ("A2_1000", "A2_500"), ("ck500", "S1/101")]

def nap(t):
    R = L.nap(TEP[t][0])
    return {k: dict(L.luat(r, k), aitwf=aitw_full(r, k), moi=aitw_moi_hop(r, k), aok=int(bool(r.get("action_ok"))),
                    sent=(r.get("sent") or "").strip(), gold=(r.get("gold_instruction") or "").strip(),
                    cum=r.get("app") or f"ep{r['episode_id']}") for k, r in R.items()}

X = {t: nap(t) for t in NH}
K = list(X["S1/101"])                         # thứ tự dòng tệp thô S1: tái lập đúng mọi KTC ghép cặp đã công bố
cum = {k: X["S1/101"][k]["cum"] for k in K}
pct = lambda t, c: 100 * sum(X[t][k][c] for k in K) / len(K)
loi = []
assert len(K) == 4463, len(K)
for t in NH:
    if len(X[t]) != 4463 or set(X[t]) != set(K):
        loi.append(f"{t}: quần thể khác 4.463 bước chung")

# — tự kiểm —
for t, m in MOC.items():
    for c, ten in COT:
        if abs(pct(t, c) - m[c]) > 0.006:
            loi.append(f"{t} {ten} {pct(t, c):.2f} ≠ công bố {m[c]}")
d, lo, hi, _ = ktc(K, lambda k, c: X["ck500"][k][c] - X["S1/101"][k][c], "vor", cum)
print(f"[tự kiểm] ck500 - S1 exec {d:+.2f} [{lo:+.2f}; {hi:+.2f}] · công bố +1,55 [+0,80; +2,33]")
if abs(d - 1.55) > 0.006 or abs(lo - 0.80) > 0.006 or abs(hi - 2.33) > 0.006:
    loi.append("ck500 - S1 exec không ra +1,55 [+0,80; +2,33]")
for t in NH:
    raw, js, pred = TEP[t]
    p, lo, hi, g = ktc(list(X[t]), lambda k, c: X[t][k][c], "vor", cum)
    ci = json.load(open(js, encoding="utf-8"))["ci_voronoi"]
    P = {(str(o["episode_id"]), str(o["step_id"])): (o.get("pred") or "").strip()
         for o in map(json.loads, open(pred, encoding="utf-8"))}
    lech = sum(P.get(k) != X[t][k]["sent"] for k in K)
    print(f"[tự kiểm] {t:8s} exec {p:.2f} [{lo:.2f}; {hi:.2f}] · json [{100*ci[0]:.2f}; {100*ci[1]:.2f}] · "
          f"câu lệch tệp dự đoán {lech} · rỗng {sum(not X[t][k]['sent'] for k in K)} · G {g}")
    if abs(lo - 100 * ci[0]) > 0.006 or abs(hi - 100 * ci[1]) > 0.006:
        loi.append(f"{t}: KTC exec lệch {os.path.basename(js)}")
    if lech:
        loi.append(f"{t}: {lech} câu trong tệp thô khác tệp dự đoán")
if loi:
    sys.exit("🔴 DỪNG, đường đọc sai — KHÔNG đọc số A2: " + " · ".join(loi))
print("✅ tự kiểm đạt\n")

# — điểm —
out = {"diem": {}, "so": {}, "phan_ra": {}, "mo_ta": {}}
print("## Điểm trên 4.463 bước chạm\n")
print("| thước | " + " | ".join(NH) + " |")
print("|---|" + "---:|" * len(NH))
for c, ten in COT:
    out["diem"][ten] = {t: round(pct(t, c), 2) for t in NH}
    print(f"| {ten} | " + " | ".join(f"{pct(t, c):.2f}" for t in NH) + " |")
for t in NH:
    out["mo_ta"][t] = dict(so_tu_tb=round(sum(len(X[t][k]["sent"].split()) for k in K) / len(K), 2),
                            trung_ck500=sum(X[t][k]["sent"] == X["ck500"][k]["sent"] for k in K),
                            trung_S1=sum(X[t][k]["sent"] == X["S1/101"][k]["sent"] for k in K),
                            rong=sum(not X[t][k]["sent"] for k in K))
for m, ten in (("so_tu_tb", "số từ TB"), ("trung_ck500", "câu trùng ck500"), ("trung_S1", "câu trùng S1"), ("rong", "câu rỗng")):
    print(f"| {ten} | " + " | ".join(str(out["mo_ta"][t][m]) for t in NH) + " |")

# — so ghép cặp —
print("\n## So ghép cặp (KTC95 bootstrap cụm app, B = 10.000 · cứu = nhánh trái đúng mà nhánh phải sai, phá = ngược lại)\n")
print("| phép so | thước | Δ | KTC95 | cứu / phá | p McNemar |")
print("|---|---|---:|---|---:|---:|")
for x, y in SO:
    o = out["so"][f"{x} - {y}"] = {}
    for c, ten in COT:
        d, lo, hi, _ = ktc(K, lambda k, cc: X[x][k][cc] - X[y][k][cc], c, cum)
        b, cu, _, p = mcnemar(K, X[y], X[x], c)
        o[ten] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2), cuu=cu, pha=b, p=p)
        print(f"| {x} - {y} | {ten} | {d:+.2f} | [{lo:+.2f}; {hi:+.2f}] | {cu} / {b} | {p:.2g} |")

# — phân rã cứu/phá so với ck500 theo loại thao tác —
print()
for x in ("A2_500", "A2_1000"):
    y = "ck500"
    cuu = [k for k in K if X[y][k]["vor"] == 0 and X[x][k]["vor"] == 1]
    pha = [k for k in K if X[y][k]["vor"] == 1 and X[x][k]["vor"] == 0]
    cuu_aok = sum(X[y][k]["aok"] == 0 for k in cuu)
    pha_aok = sum(X[x][k]["aok"] == 0 for k in pha)
    r_aok, r_dv = cuu_aok - pha_aok, (len(cuu) - cuu_aok) - (len(pha) - pha_aok)
    out["phan_ra"][f"{x} - {y}"] = dict(cuu=len(cuu), pha=len(pha), cuu_aok=cuu_aok, pha_aok=pha_aok,
                                            rong_aok=r_aok, rong_dinh_vi=r_dv)
    print(f"[phân rã {x} - ck500] cứu {len(cuu)} (ck500 sai loại thao tác {cuu_aok}) · phá {len(pha)} "
          f"({x} sai loại thao tác {pha_aok}) · ròng từ loại thao tác {r_aok:+d} · ròng từ đổi phần tử {r_dv:+d}")

# — luật 299 §4 (chốt trước khi có số) —
e = out["so"]["A2_500 - ck500"]["Executability"]
hang = "C" if e["lo"] > 0 else ("S" if e["hi"] < 0 else "H")
TXT = {"S": "cận trên < 0 → giữ ck500; ghi: ở cùng 500 bước, thưởng SPICE hơn thưởng CIDEr-D.",
       "H": "KTC chứa 0 → giữ ck500; A2_500 vào luận văn như phép so phần thưởng; câu đóng góp: thưởng bằng một thước so câu.",
       "C": "cận dưới > 0 → A2_500 hơn ck500 có ý nghĩa; DỪNG, người dùng quyết theo mục 8 (đổi phương pháp kéo theo nhiều việc)."}
out["hang"] = hang
print(f"\n[luật 299 §4] A2_500 - ck500 exec {e['delta']:+.2f} [{e['lo']:+.2f}; {e['hi']:+.2f}] → hàng {hang}: {TXT[hang]}")
print("  A2_1000 chỉ đọc thêm, không đổi hàng.")

# — thước chữ (WSL, cần Java 8) —
if a.chu:
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.bleu.bleu import Bleu
    from pycocoevalcap.meteor.meteor import Meteor
    from pycocoevalcap.rouge.rouge import Rouge
    from pycocoevalcap.cider.cider import Cider
    from pycocoevalcap.spice.spice import Spice
    import text_metrics_them as TM
    REF = json.load(open(os.path.join(RUNS, "grpo_spice", "text_metrics_ck500.json"), encoding="utf-8"))
    CH = ["bleu4", "meteor15", "rougeL", "cider_d", "spice", "chrf"] + (["bertscore_f1_rescaled"] if a.bert else [])
    chu = {}
    print("\n[thước chữ] chạy Java, vài phút mỗi nhánh ...", flush=True)
    for t in NH:
        hyp, ref = [X[t][k]["sent"] for k in K], [X[t][k]["gold"] for k in K]
        tk = PTBTokenizer()
        g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
        c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
        b, _ = Bleu(4).compute_score(g, c, verbose=0)
        sp, ds = Spice().compute_score(g, c)
        o = dict(bleu4=round(100 * b[3], 2), meteor15=round(100 * Meteor().compute_score(g, c)[0], 2),
                 rougeL=round(100 * Rouge().compute_score(g, c)[0], 2),
                 cider_d=round(100 * Cider().compute_score(g, c)[0], 2), spice=round(100 * sp, 2))
        tm = TM.tinh(hyp, ref, bert=a.bert)
        o["chrf"] = tm["chrf"]
        if a.bert:
            o["bertscore_f1_rescaled"] = tm["bertscore_f1_rescaled"]
        for k, dd in zip(K, ds):
            f = dd["All"]["f"]
            X[t][k]["spice"] = 0.0 if f is None or f != f else float(f)
        chu[t] = o
        print(f"  {t:8s} " + " · ".join(f"{m} {o[m]}" for m in CH), flush=True)
        if t in REF:
            for m in CH:
                if m in REF[t] and abs(o[m] - REF[t][m]) > 0.025:
                    loi.append(f"{t} {m} {o[m]} ≠ đã lưu {REF[t][m]}")
    if loi:
        sys.exit("🔴 DỪNG, thước chữ không tái lập S1/ck500 — KHÔNG dùng số chữ của A2: " + " · ".join(loi))
    print("✅ S1 và ck500 tái lập số chữ đã lưu (±0,025)\n")
    out["chu"] = chu
    print("| thước | " + " | ".join(NH) + " | A2_500 - ck500 | A2_1000 - ck500 |")
    print("|---|" + "---:|" * (len(NH) + 2))
    for m in CH:
        print(f"| {m} | " + " | ".join(f"{chu[t][m]:.2f}" for t in NH)
              + f" | {chu['A2_500'][m] - chu['ck500'][m]:+.2f} | {chu['A2_1000'][m] - chu['ck500'][m]:+.2f} |")
    out["so_spice"] = {}
    for x, y in SO:
        d, lo, hi, _ = ktc(K, lambda k, cc: X[x][k][cc] - X[y][k][cc], "spice", cum)
        out["so_spice"][f"{x} - {y}"] = dict(delta=round(d, 2), lo=round(lo, 2), hi=round(hi, 2))
        print(f"  ΔSPICE {x} - {y}: {d:+.2f} [{lo:+.2f}; {hi:+.2f}]")

if A2:
    p = os.path.join(A2, "doc_299.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n→", p)
