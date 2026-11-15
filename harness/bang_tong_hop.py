# -*- coding: utf-8 -*-
"""Sinh report/334_BANG_KET_QUA_TONG_HOP.md — MỘT report chứa mọi bảng kết quả (15/11/2026). 0 GPU.

    cd harness && python3 bang_tong_hop.py            # ~5–10 phút (bootstrap B = 10.000)
    cd harness && python3 bang_tong_hop.py --nhanh    # B = 1.000, để thử

Cập nhật khi có kết quả mới:
  · nhánh test mới có tệp thô 4.463 dòng  → thêm một dòng vào TEST (tên, đường dẫn trong runs/, nhóm).
  · độ đo văn bản test mới                → thêm vào CHU (giá trị lấy từ JSON của kernel chu_*).
  · bước không chạm test mới              → thêm vào NONTAP.
  · DEV-v3 nhánh mới                      → thêm vào DEV + chạy lại harness/chu_sa3_dev_15_11.py.
  · bảng không tính được từ tệp thô (dụng cụ khác, AitZ, ACU…) → sửa chuỗi TINH ở cuối file.
Tiêu chí vị trí tính đúng bằng luat_d3.py + luat_aitw_day_du.py; so ghép cặp dùng score_run.cluster_bootstrap (cụm app)
+ McNemar chính xác, cùng hàm với doc_luoi.py. Tự kiểm: ck500 − S1/101 exec phải ra +1,55 [+0,80; +2,33].
"""
import json, os, sys, math, time

from scipy.stats import binomtest

import luat_d3 as L
from luat_aitw_day_du import aitw_full
import score_run as S

B = 1000 if "--nhanh" in sys.argv else 10000
R = L.RUNS
OUT = os.path.join(L.ROOT, "report", "334_BANG_KET_QUA_TONG_HOP.md")
v = lambda x, d=2: ("-" if x is None else f"{x:.{d}f}".replace(".", ","))
sg = lambda x, d=2: ("-" if x is None else (("+" if x > 0 else "") + f"{x:.{d}f}".replace(".", ",")).replace("-", "−"))

# ---------------- 1. tập kiểm: (tên, tệp thô trong runs/, nhóm) ----------------
TEST = [
    ("Câu chuẩn (trần dụng cụ)", "score_ceiling_human_raw.jsonl", "mốc"),
    ("ACE (R3)", "ra304_luat/score_R3_test_raw.jsonl", "chính"),
    ("ck500 (GRPO + SPICE)", "grpo_spice/score_ck500_test_raw.jsonl", "chính"),
    ("ck500 hạt 202", "grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl", "chính"),
    ("GRPO + ROUGE-L", "luoi/test_2_11/score_grpo_rougel_101_test_raw.jsonl", "lưới RL"),
    ("SCST + SPICE", "luoi/test_2_11/score_scst_spice_101_test_raw.jsonl", "lưới RL"),
    ("GRPO + METEOR", "luoi/test_2_11/score_grpo_meteor_101_test_raw.jsonl", "lưới RL"),
    ("GRPO + CIDEr-D", "luoi/test_2_11/score_grpo_cider_101_test_raw.jsonl", "lưới RL"),
    ("GRPO + CIDEr-D (A2, 500 bước)", "a2_test299/score_A2_500_test_raw.jsonl", "lưới RL"),
    ("GRPO + CIDEr-D (A2, 1000 bước)", "a2_test299/score_A2_1000_test_raw.jsonl", "lưới RL"),
    ("SFT tiếp (= SFT-cont)", "luoi/7_11/test_u_3/score_sft_tiep_101_test_raw.jsonl", "lưới RL"),
    ("PPO λ=1 (1000 bước)", "luoi/14_11/test_c_ppo/score_ppo_l1_101_test_raw.jsonl", "lưới RL"),
    ("PPO λ=0,95 (1000 bước)", "luoi/14_11/test_c_ppo/score_ppo_l95_101_test_raw.jsonl", "lưới RL"),
    ("REINFORCE + SPICE", "luoi/7_11/test_u_3/score_reinforce_spice_101_test_raw.jsonl", "lưới RL"),
    ("GRPO + SPICE chạy lại (A/A)", "luoi/8_11/test_u_4/score_grpo_spice_aa_101_test_raw.jsonl", "lưới RL"),
    ("RLOO + SPICE", "luoi/7_11/test_u_3/score_rloo_spice_101_test_raw.jsonl", "lưới RL"),
    ("xao101 (SPICE ghép ngẫu nhiên)", "xao101/test/score_ck500_xao101_test_raw.jsonl", "lưới RL"),
    ("SA-SPICE-v3 ck400", "sa_spice_v3/test/score_sa_ck400_test_raw.jsonl", "lưới RL"),   # chờ kernel sa3-test-ck400
    ("TAGE", "tage_test/score_tage_gop_raw.jsonl", "hướng đã thử"),
    ("RAFT", "rd314/E/exec_raft/score_raft_gop_raw.jsonl", "hướng đã thử"),
    ("GRPO-point (chặng ba)", "grpo_point/score_grpo_point_seed101_raw.jsonl", "hướng đã thử"),
    ("MIN-DESC", "score_min_desc_seed101_raw.jsonl", "hướng đã thử"),
    ("CE2-S2", "score_ce2_s2_seed101_raw.jsonl", "hướng đã thử"),
    ("CW-RA", "cw309/G3b/exec_out/score_cw_gop_raw.jsonl", "hướng đã thử"),
    ("ra_k4", "ra304_G/exec_out/exec_out/score_ra_k4_gop_raw.jsonl", "hướng đã thử"),
    ("S2", "score_s2_seed101_raw.jsonl", "hướng đã thử"),
    ("gui_sel", "sel/score_gui_sel_seed101_raw.jsonl", "hướng đã thử"),
    ("S1/202", "score_s1_seed202_raw.jsonl", "mốc"),
    ("S1/101", "score_s1_seed101_raw.jsonl", "mốc"),
    ("Qwen2.5-VL-7B prompting", "qwen7b/test_25_10/score_qwen7b_test_raw.jsonl", "mốc"),
    ("Base 3B", "score_base_raw.jsonl", "mốc"),
]
MOC_SO = [("ck500 (GRPO + SPICE)", "ck500"), ("S1/101", "S1/101"), ("SFT tiếp (= SFT-cont)", "SFT tiếp")]

# ---------------- 2. độ đo văn bản test (4.463 bước chạm, mức kho) ----------------
# BLEU-4 · METEOR · ROUGE-L · CIDEr-D · SPICE · chrF · BERTScore — nguồn ghi ở cột cuối
CHU = {
    "Câu chuẩn (trần dụng cụ)": (100.0, 100.0, 100.0, 988.74, 98.61, 100.0, 100.0, "text_metrics_coco/them.json"),
    "ACE (R3)": (53.47, 38.37, 69.11, 442.02, 47.13, 63.45, 67.73, "ktc_chu_27_10.json"),
    "ck500 (GRPO + SPICE)": (52.36, 37.92, 68.36, 430.05, 45.79, 62.87, 67.07, "ktc_chu_27_10.json"),
    "ck500 hạt 202": (52.94, 37.53, 68.48, 431.22, 45.69, 62.37, 67.12, "ktc_chu_27_10.json"),
    "GRPO + ROUGE-L": (52.59, 38.20, 69.27, 432.81, 45.57, 63.42, 67.57, "chu_luoi_8_11b.json"),
    "SCST + SPICE": (51.97, 38.15, 68.70, 430.89, 45.93, 63.31, 67.25, "chu_luoi_8_11b.json"),
    "GRPO + METEOR": (50.76, 38.63, 69.14, 426.61, 45.13, 64.19, 67.35, "chu_luoi_8_11b.json"),
    "GRPO + CIDEr-D": (51.59, 37.78, 68.47, 424.52, 44.43, 62.90, 67.03, "chu_luoi_8_11b.json"),
    "GRPO + CIDEr-D (A2, 500 bước)": (52.38, 37.24, 68.59, 428.27, 45.27, 61.76, None, "report/299 §3"),
    "GRPO + CIDEr-D (A2, 1000 bước)": (52.82, 37.37, 68.46, 427.98, 44.45, 61.92, None, "report/299 §3"),
    "SFT tiếp (= SFT-cont)": (52.07, 37.75, 68.55, 425.79, 45.33, 62.64, 67.05, "chu_luoi_8_11b.json"),
    "PPO λ=1 (1000 bước)": (50.70, 37.86, 68.25, 420.72, 44.98, 63.00, 66.78, "chu_ppo_du (14/11)"),
    "PPO λ=0,95 (1000 bước)": (50.67, 37.89, 67.96, 419.53, 44.81, 62.85, 66.54, "chu_ppo_du (14/11)"),
    "REINFORCE + SPICE": (52.52, 37.37, 67.97, 426.11, 45.27, 62.06, 66.76, "chu_luoi_8_11b.json"),
    "GRPO + SPICE chạy lại (A/A)": (52.97, 37.55, 68.44, 430.92, 46.00, 62.39, 67.09, "chu_luoi_8_11b.json"),
    "RLOO + SPICE": (52.00, 37.00, 67.33, 422.10, 45.26, 61.65, 66.31, "chu_luoi_8_11b.json"),
    "xao101 (SPICE ghép ngẫu nhiên)": (51.32, 36.95, 67.36, 418.13, 44.40, 61.52, 66.40, "ktc_chu_27_10.json"),
    "TAGE": (None, None, None, None, 45.74, None, None, "report/269 §2"),
    "RAFT": (51.65, 37.52, 67.79, 423.21, 44.89, 62.37, 66.62, "report/314 §2"),
    "GRPO-point (chặng ba)": (49.86, 37.31, 68.54, 402.91, 42.50, 61.88, 66.85, "text_metrics_coco/them.json"),
    "MIN-DESC": (49.92, 37.26, 68.47, 401.01, 42.24, 61.79, 66.73, "text_metrics_coco/them.json"),
    "CE2-S2": (50.12, 37.31, 68.62, 402.24, 42.27, 61.85, 66.83, "text_metrics_coco/them.json"),
    "CW-RA": (49.72, 35.79, 65.05, 406.8, 43.71, 60.04, 64.53, "report/310"),
    "S2": (48.68, 35.75, 65.97, 387.68, 41.28, 59.94, 65.07, "text_metrics_coco/them.json"),
    "gui_sel": (46.89, 34.23, 63.32, 370.62, 39.28, 57.66, 62.75, "text_metrics_coco/them.json"),
    "S1/202": (51.66, 37.17, 67.71, 419.19, 44.23, 61.92, 66.75, "ktc_chu_27_10.json"),
    "S1/101": (51.56, 36.79, 67.35, 416.12, 44.37, 61.26, 66.33, "ktc_chu_27_10.json"),
    "Qwen2.5-VL-7B prompting": (14.48, 21.90, 39.79, 100.71, 18.74, 36.22, 39.70, "ktc_chu_27_10.json"),
    "Base 3B": (15.34, 24.58, 42.31, 88.01, 18.48, 40.18, 40.10, "text_metrics_coco/them.json"),
}

# ---------------- 3. bước không chạm test (2.495 bước, noharm: đúng loại thao tác %) ----------------
NONTAP_COT = ("toàn bộ", "scroll", "wait", "input_text", "open_app", "navigate_back")
NONTAP_N = (2495, 755, 505, 494, 469, 270)
NONTAP = {   # report/279 §4g (ctg_nontap_doc.json)
    "S1/101": (85.97, 83.97, 90.69, 81.58, 96.16, 72.96),
    "ck500 (GRPO + SPICE)": (84.29, 77.75, 95.25, 79.55, 97.87, 67.04),
    "CTG A2 (CIDEr-D, 1000 bước)": (84.45, 77.62, 94.46, 81.38, 98.72, 65.56),
    "CTG A3 (CIDEr-D + CTG, 1000 bước)": (84.25, 78.68, 94.46, 80.36, 98.72, 62.59),
    # "SA-SPICE-v3 ck400": (...),  "SFT-cont": (...),   ← chờ kernel sa3-test-ck400
}

# ---------------- 4. DEV-v3 ----------------
DEV = [("SFT-cont", "sa_spice_v3/dev/a/score/score_dev_sftcont_raw.jsonl"),
       ("SA-SPICE-v3 ck500", "sa_spice_v3/dev/a/score/score_dev_sa_ck500_raw.jsonl"),
       ("SA-SPICE-v3 ck400", "sa_spice_v3/dev/b/score/score_dev_sa_ck400_raw.jsonl"),
       ("chrF ck400", "sa_spice_v3/dev/b/score/score_dev_chrf_ck400_raw.jsonl")]
DEV_CHU = os.path.join(R, "sa_spice_v3/dev/chu/chu_sa3_dev_15_11.json")
DEV_DOC = os.path.join(R, "sa_spice_v3/dev/doc_dev.json")
DESC_TR = os.path.join(L.HERE, "dg1_cache", "train_ac", "descriptors.jsonl")


def nap_test(f):
    p = os.path.join(R, f)
    if not os.path.exists(p):
        return None
    out = {}
    for k, r in L.nap(p).items():
        out[k] = dict(L.luat(r, k), aitwf=aitw_full(r, k), aok=int(r["action_ok"] and r["toggle_ok"]),
                      cum=r.get("app") or f"ep{r['episode_id']}")
    return out


def tb(X, c):
    return 100 * sum(x[c] for x in X.values()) / len(X)


def so(A, Bn, c="vor"):
    K = [k for k in A if k in Bn]
    cum = {k: Bn[k]["cum"] for k in K}
    pt, (lo, hi), _, _ = S.cluster_bootstrap([(k, A[k][c] - Bn[k][c]) for k in K], lambda u: cum[u[0]],
                                             lambda u: u[1], B=B, seed=S.SEED)
    cu = sum(A[k][c] > Bn[k][c] for k in K); ph = sum(A[k][c] < Bn[k][c] for k in K)
    return dict(d=100 * pt, lo=100 * lo, hi=100 * hi, cu=cu, ph=ph, n=len(K),
                p=binomtest(cu, cu + ph).pvalue if cu + ph else 1.0)


def fp(p):
    return (f"{p:.2g}" if p < 0.001 else f"{p:.3f}").replace(".", ",")


def main():
    t0 = time.time()
    md = []
    w = md.append
    w("# 334 — Bảng kết quả tổng hợp (tự sinh)\n")
    w(f"> **Tệp này do `harness/bang_tong_hop.py` sinh ra — đừng sửa tay.** Cập nhật: thêm nhánh vào danh sách trong script "
      f"rồi `cd harness && python3 bang_tong_hop.py`. Lần sinh gần nhất: {time.strftime('%d/%m/%Y %H:%M', time.localtime())} (giờ máy WSL, UTC). "
      f"Bootstrap B = {B}.\n")
    w("Quy ước: số **test** = tập kiểm AndroidControl của dự án (4.463 bước chạm + 2.495 bước không chạm), trích được. "
      "Số **DEV/val** chỉ để chọn nhánh, cấm trích ra bài. Mọi nhánh một hạt giống (101) trừ chỗ ghi khác. "
      "KTC95 bootstrap cụm app (test) hoặc cụm episode (DEV-v3); p là McNemar chính xác; * = KTC loại 0.\n")

    # ===== 1. tiêu chí vị trí =====
    D = {}
    for ten, f, nhom in TEST:
        X = nap_test(f)
        if X is not None:
            D[ten] = X
    w("## 1. Tập kiểm — tiêu chí xác định vị trí (4.463 bước chạm)\n")
    w("Tính lại từ tệp thô `*_raw.jsonl` bằng `luat_d3.py` + `luat_aitw_day_du.py`. Cột *đúng loại thao tác* gồm cả điều kiện bật/tắt.\n")
    w("| nhóm | nhánh | n | exec | D.3 | D.3∧14% | ±14% từng trục | AitW khoảng cách | AitW đầy đủ | đúng loại thao tác |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for ten, f, nhom in TEST:
        if ten not in D:
            w(f"| {nhom} | {ten} | - | **đang chấm / chưa có** | | | | | | |"); continue
        X = D[ten]
        w(f"| {nhom} | {ten} | {len(X)} | {v(tb(X,'vor'))} | {v(tb(X,'d3'))} | {v(tb(X,'d3_gate'))} | {v(tb(X,'d14_truc'))} | "
          f"{v(tb(X,'aitw'))} | {v(tb(X,'aitwf'))} | {v(tb(X,'aok'))} |")
    w("")

    # ===== 1b. so ghép cặp exec =====
    w("### 1b. So ghép cặp exec với ba mốc (test)\n")
    w("Δ [KTC95] (hơn / kém), p McNemar chính xác chưa hiệu chỉnh. Holm cho từng họ phép so xem report/320.\n")
    tk = so(D["ck500 (GRPO + SPICE)"], D["S1/101"])
    assert abs(tk["d"] - 1.55) < 0.01 and abs(tk["lo"] - 0.80) < 0.06 and abs(tk["hi"] - 2.33) < 0.06 or B < 10000, f"⛔ tự kiểm lệch {tk}"
    w(f"Tự kiểm: ck500 − S1/101 = {sg(tk['d'])} [{sg(tk['lo'])}; {sg(tk['hi'])}] (đã công bố +1,55 [+0,80; +2,33]).\n")
    w("| nhánh | " + " | ".join(f"− {m}" for _, m in MOC_SO) + " |")
    w("|---|" + "---|" * len(MOC_SO))
    for ten, f, nhom in TEST:
        if ten not in D or ten.startswith("Câu chuẩn"):
            continue
        o = []
        for mt, _ in MOC_SO:
            if mt == ten:
                o.append("-"); continue
            r = so(D[ten], D[mt])
            st = "*" if (r["lo"] > 0 or r["hi"] < 0) else ""
            o.append(f"{sg(r['d'])}{st} [{sg(r['lo'])}; {sg(r['hi'])}] ({r['cu']}/{r['ph']}) p={fp(r['p'])}")
        w(f"| {ten} | " + " | ".join(o) + " |")
    w("")
    print(f"  so ghép cặp xong {time.time()-t0:.0f} s", flush=True)

    # ===== 2. độ đo văn bản =====
    w("## 2. Tập kiểm — độ đo văn bản (4.463 bước chạm, mức kho)\n")
    w("COCO (BLEU-4, METEOR 1.5, ROUGE-L, CIDEr-D, SPICE) + chrF + BERTScore (roberta-large L17, rescaled). Giá trị chép từ JSON của các kernel chấm (cột nguồn). `-` = chưa tính.\n")
    w("| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore | nguồn |")
    w("|---|---|---|---|---|---|---|---|---|")
    for ten, f, nhom in TEST:
        c = CHU.get(ten)
        if not c:
            w(f"| {ten} | chưa có | | | | | | | |"); continue
        w(f"| {ten} | " + " | ".join(v(x) for x in c[:7]) + f" | {c[7]} |")
    w("")
    w("Phép so ghép cặp có KTC cho độ đo văn bản: report/320 §3.2 (ck500, ACE, S1, xao101, ck500/202), §14.3 (lưới đợt đầu), "
      "§19 (SFT tiếp, REINFORCE, RLOO), §21 (A/A), §28 (PPO).\n")

    # ===== 3. không chạm =====
    w("## 3. Tập kiểm — bước không chạm (2.495 bước, tỉ lệ câu đúng loại thao tác, %)\n")
    w("| nhánh | " + " | ".join(f"{c} (n={n:,})".replace(",", ".") for c, n in zip(NONTAP_COT, NONTAP_N)) + " |")
    w("|---|" + "---|" * len(NONTAP_COT))
    for ten, row in NONTAP.items():
        w(f"| {ten} | " + " | ".join(v(x) for x in row) + " |")
    w("| SA-SPICE-v3 ck400 | **đang chấm** (kernel `sa3-test-ck400`) | | | | | |")
    w("| SFT-cont | **đang chấm** (kernel `sa3-test-ck400`) | | | | | |\n")
    w("Phép so có KTC: ck500 − S1 toàn bộ −1,68 (cận dưới −2,76), scroll **−6,23 [−8,30; −4,31]**, back −5,93 (report/261 §6); "
      "A3 − S1 toàn bộ −1,72 [−2,82; −0,63], scroll −5,30 [−7,19; −3,53] (report/279 §4g).\n")

    # ===== 4. DEV-v3 =====
    w("## 4. DEV-v3 (SA-SPICE-v3) — số dev, cấm trích\n")
    w("2.223 bước (1.338 chạm · 885 không chạm, 667 bước có gold tin được), tách khỏi tập dạy GRPO theo episode; pool lấy từ tập dạy SFT nên S1/SFT-cont đã thấy. "
      "Một hạt giống (101).\n")
    DT = {(str(d["episode_id"]), str(d["step_id"])): d for d in map(json.loads, open(DESC_TR, encoding="utf-8"))}
    L.D.update(DT)
    DV = {}
    for ten, f in DEV:
        X = nap_test(f)
        if X is not None:
            for k in X:
                X[k]["cum"] = f"ep{k[0]}"
            DV[ten] = X
    w("### 4a. Tiêu chí xác định vị trí (1.338 bước chạm; hộp phần tử từ `train_ac/descriptors.jsonl`)\n")
    w("| nhánh | exec | D.3 | D.3∧14% | ±14% từng trục | AitW khoảng cách | AitW đầy đủ | đúng loại thao tác |")
    w("|---|---|---|---|---|---|---|---|")
    for ten, X in DV.items():
        w(f"| {ten} | {v(tb(X,'vor'))} | {v(tb(X,'d3'))} | {v(tb(X,'d3_gate'))} | {v(tb(X,'d14_truc'))} | {v(tb(X,'aitw'))} | {v(tb(X,'aitwf'))} | {v(tb(X,'aok'))} |")
    w("")
    w("### 4b. So ghép cặp DEV-v3 (exec, cụm episode, B như trên)\n")
    w("| phép so | exec | D.3 | AitW đầy đủ |")
    w("|---|---|---|---|")
    for a, b in (("SA-SPICE-v3 ck500", "SFT-cont"), ("SA-SPICE-v3 ck400", "SFT-cont"), ("chrF ck400", "SFT-cont"),
                 ("SA-SPICE-v3 ck400", "chrF ck400"), ("SA-SPICE-v3 ck500", "SA-SPICE-v3 ck400")):
        if a in DV and b in DV:
            o = []
            for c in ("vor", "d3", "aitwf"):
                r = so(DV[a], DV[b], c)
                st = "*" if (r["lo"] > 0 or r["hi"] < 0) else ""
                o.append(f"{sg(r['d'])}{st} [{sg(r['lo'])}; {sg(r['hi'])}] p={fp(r['p'])}")
            w(f"| {a} − {b} | " + " | ".join(o) + " |")
    w("")
    if os.path.exists(DEV_DOC):
        dd = json.load(open(DEV_DOC))
        w("### 4c. Bước không chạm DEV-v3 (667 bước có gold tin được, verifier v3)\n")
        w("| nhánh | đúng loại | % | câu trùng nguyên văn gold (/2.223) |")
        w("|---|---|---|---|")
        for k, x in dd["nontap"].items():
            w(f"| {k} | {x['dung_loai']}/{x['n_trusted']} | {v(100*x['dung_loai']/x['n_trusted'])} | {x['trung_gold']} |")
        w("")
        w("| phép so (không chạm) | Δ [KTC95] | cứu / phá | p |")
        w("|---|---|---|---|")
        for k, x in dd["pairs"].items():
            if k.startswith("nontap_"):
                w(f"| {k[7:]} | {sg(x['d'])} [{sg(x['ci'][0])}; {sg(x['ci'][1])}] | {x['cuu']}/{x['pha']} | {fp(x['p'])} |")
        w("")
        w("Theo loại (đúng/tổng): input_text SFT-cont 88/111 · ck500 78 · ck400 88 · chrF 75 — navigate_back 84/104 · 56 · 60 · 57 — "
          "open_app 161/169 · 154 · 159 · 156 — scroll 227/283 · 235 · 237 · 226 (`sa3_dev_doc.py`).\n")
    if os.path.exists(DEV_CHU):
        dc = json.load(open(DEV_CHU))
        ME = dc["meteor"]
        for pv, nh in (("toan_bo", "toàn bộ 2.223 bước"), ("cham", "1.338 bước chạm")):
            w(f"### 4d. Độ đo văn bản DEV-v3 — {nh}\n")
            w("| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |")
            w("|---|---|---|---|---|---|---|---|")
            for ten, x in dc[pv]["diem"].items():
                w(f"| {ten} | {v(x['bleu4']['diem'])} | {v(ME.get(f'{ten} · {pv}'))} | {v(x['rougeL']['diem'])} | {v(x['cider_d']['diem'])} | "
                  f"{v(x['spice']['diem'])} | {v(x['chrf']['diem'])} | {v(x['bert']['diem'])} |")
            w("")
            w("| phép so | BLEU-4 | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |")
            w("|---|---|---|---|---|---|---|")
            for k, x in dc[pv]["so"].items():
                cs = []
                for m in ("bleu4", "rougeL", "cider_d", "spice", "chrf", "bert"):
                    y = x[m]; st = "*" if (y["lo"] > 0 or y["hi"] < 0) else ""
                    cs.append(f"{sg(y['delta'])}{st} [{sg(y['lo'])}; {sg(y['hi'])}]")
                w(f"| {k} | " + " | ".join(cs) + " |")
            w("")

    w(TINH)
    open(OUT, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"ghi {OUT} · {time.time()-t0:.0f} s", flush=True)


# ---------------- các bảng không tính được từ tệp thô (chép từ report gốc, sửa tay khi có số mới) ----------------
TINH = """## 5. Đổi dụng cụ chấm (test, report/320 §4)

| nhánh | UGround exec | UI-Venus-7B exec | Phi-Ground-4B exec | Phi-4 người nghe (chọn đúng) |
|---|---|---|---|---|
| S1/101 | 59,11 | 54,51 | 46,96 | 44,63 [42,88; 46,37] |
| ck500 | 60,65 | 56,06 | 47,75 | 45,33 [43,59; 47,11] |
| ACE (R3) | 60,68 | 56,20 | 47,73 | 45,33 [43,57; 47,12] |

| phép so | UI-Venus-7B | Phi-Ground-4B | Phi-4 người nghe |
|---|---|---|---|
| ck500 − S1/101 | +1,55 [+0,82; +2,30] p=8,7e−6 | +0,78 [+0,05; +1,51] p=0,034 | +0,69 [+0,02; +1,40] p=0,039 |
| ACE − S1/101 | +1,68 [+0,97; +2,42] | +0,76 [+0,02; +1,49] | +0,69 p=0,043 |
| ACE − ck500 | +0,13 [−0,11; +0,39] | −0,02 [−0,33; +0,29] | 0,00 [−0,24; +0,23] |

## 6. Lịch sử tự sinh (câu bước trước do mô hình viết, report/320 §7)

| | lịch sử chuẩn | lịch sử tự sinh | tự sinh − chuẩn |
|---|---|---|---|
| S1/101 exec | 59,11 | 54,96 | −4,15 [−5,35; −2,99] |
| ck500 exec | 60,65 | 56,44 | −4,21 [−5,33; −3,13] |
| ck500 − S1 | +1,55 [+0,80; +2,33] | +1,48 [+0,54; +2,43] | |

| | S1 chuẩn | S1 tự sinh | ck500 chuẩn | ck500 tự sinh |
|---|---|---|---|---|
| đúng loại thao tác, bước chạm | 92,54 | 89,16 | 94,42 | 92,67 |
| đúng loại thao tác, không chạm | 85,97 | 81,32 | 84,29 | 76,83 |

| nhánh (tự sinh) | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| S1 | 43,44 | 31,73 | 59,78 | 331,42 | 34,97 | 53,71 | 59,11 |
| ck500 | 43,50 | 32,37 | 60,39 | 333,58 | 35,10 | 54,54 | 59,23 |

## 7. Ngoài miền: AitZ zero-shot (report/320 §6)

| nhánh | exec | hit_disk | đúng loại thao tác | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|---|---|---|
| câu chuẩn | 66,26 | - | - | | | | | | | |
| Base | 34,50 | 47,51 | 94,08 | 18,68 | 18,56 | 39,11 | 86,98 | 15,66 | 35,24 | 38,81 |
| S1/101 | 37,79 | 50,00 | 93,46 | 21,01 | 20,83 | 46,84 | 120,24 | 15,27 | 35,66 | 49,69 |
| ck500 | 37,28 | 49,56 | 92,40 | 21,48 | 21,08 | 46,92 | 123,38 | 16,37 | 36,28 | 49,68 |
| ck500/202 | 36,62 | 48,90 | 92,62 | 19,76 | 19,99 | 45,44 | 117,26 | 15,63 | 34,43 | 48,47 |
| ACE (R3) | 37,28 | - | - | 21,45 | 21,05 | 46,91 | 123,29 | 16,40 | 36,24 | 49,63 |
| ra_k4 | 37,02 | - | - | 19,94 | 20,04 | 45,39 | 117,42 | 15,70 | 34,24 | 48,27 |

ck500 − S1 exec trên AitZ: −0,51 (KTC phủ 0); SPICE +1,10 [+0,53; +1,66].

## 8. ACU: phần AndroidControl S1 chưa thấy (report/320 §8)

| nhánh | exec [KTC95] | AitW khoảng cách | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|---|---|
| câu chuẩn | 71,70 [69,14; 74,19] | 83,29 | | | | | | | |
| Base | 49,80 [47,04; 52,57] | 57,95 | 15,01 | - | 42,04 | 93,25 | 19,28 | 39,61 | 40,10 |
| S1/101 | 52,16 [49,33; 54,99] | 61,79 | 47,53 | 34,47 | 63,45 | 385,99 | 39,74 | 57,20 | 62,76 |
| ra_k4 | 52,56 [49,69; 55,40] | 61,93 | 48,60 | 35,12 | 64,73 | 405,68 | 41,65 | 58,19 | 64,21 |
| ck500/202 | 56,20 [53,47; 58,91] | 66,37 | 50,07 | 36,08 | 66,30 | 414,32 | 42,15 | 59,40 | 64,59 |
| ck500 | 56,74 [53,98; 59,49] | 66,91 | 49,85 | 36,64 | 66,38 | 412,72 | 42,25 | 60,06 | 64,64 |
| ACE | 57,01 [54,21; 59,75] | 66,98 | 50,88 | 37,03 | 67,11 | 425,71 | 43,21 | 60,59 | 65,32 |

ck500 − S1/101 exec trên ACU: **+4,58 [+3,17; +6,05]** p=2,1e−10 · ACE − S1/101 +4,85 · ACE − ck500 +0,27 (phủ 0).

## 9. Số dev/val trước đây so với test (cấm trích số dev)

| tập dev | cỡ | nhánh | dev exec | test exec | dev − test |
|---|---|---|---|---|---|
| val C1 | 249 click | S1/101 | 63,45 | 59,11 | +4,3 |
| val C1 | 249 click | ck500 | 66,27 | 60,65 | +5,6 |
| val C1 | 249 click | TAGE | 67,47 | 60,23 | +7,2 |
| val400 | 262 chạm | MIN-DESC | 67,56 | 60,05 | +7,5 |
| val400 | 262 chạm | GRPO-point | 68,32 | 60,07 | +8,3 |
| DEV-v3 | 1.338 chạm | SFT-cont | 62,93 | 60,16 | +2,8 |
| DEV-v3 | 1.338 chạm | SA-SPICE-v3 ck400 | 64,28 | đang chấm | |

| phép so | dev | test |
|---|---|---|
| ck500 − S1/101 | +2,81 (val C1) | +1,55 |
| GRPO-point − MIN-DESC | +0,76 (val400) | +0,02 |
| SA-SPICE-v3 ck400 − SFT-cont | +1,35 (DEV-v3) | đang chấm |

## 10. Nhánh chưa có số test

| nhánh | trạng thái | ghi chú |
|---|---|---|
| SA-SPICE-v3 ck400 | đang chấm (`trangphngngc/sa3-test-ck400`, đẩy 15/11 06:55) | chọn theo tiêu chí khả thi DEV-v3, report/333 §13 |
| chrF ck400 (SA-SPICE-v3 baseline) | không chấm test | trượt tiêu chí khả thi DEV (không chạm −6,90) |
| Dr.GRPO | treo ở checkpoint-475 | report/320 §20 |
| VIS-SFT | dừng ở điểm kiểm K1 | không có số test |
| CTG A3 bước chạm | xem report/279 | chỉ ghi bước không chạm ở §3 |
"""

if __name__ == "__main__":
    main()
