# -*- coding: utf-8 -*-
"""Phụ lục B — tái lập các số MỚI của bản 8/9. Chạy từ GỐC kho, 0 giây GPU, ~2 phút CPU.

    PYTHONIOENCODING=utf-8 python3 harness/phu_luc_b.py

Thi hành P8 của `report/151`. Bốn mục:
  A. chẩn đoán hai kênh          → luận văn ch6 §sec:haikenh, Bảng tab:haikenh
  B. hệ số truyền nhân quả       → cùng mục, Bảng tab:ocheokenh
  C. trần cho ORPO tầng câu      → mục 2.1 của 151 (hướng đã bị cắt)
  D. sàn và độ phân giải từng luật → lập luận giữ thước tiêu đề, mục 6.1

⚠️ Ba chỗ dễ vấp, đã trả giá khi dựng lại:
 · Điểm mô hình TỰ KHAI nằm ở trường `raw` của `runs/preds_*.jsonl`, KHÔNG có trong
   `runs/score_*_raw.jsonl`. Phải nạp cả hai tệp rồi ghép theo `(episode_id, step_id)`.
 · Thang toạ độ trong `<point>` là **0–1000**, không phải điểm ảnh. Chia 1000 cho sai số chuẩn
   hoá trung vị 0,0194; coi là điểm ảnh cho 0,3478 — lệch 18 lần, không thể nhầm.
 · Mục D phải lấy giao RỘNG HƠN mục A–C (mục D không cần `<desc>`), nếu không n rơi xuống 796
   và mọi số lệch ~0,3 pp so với lát 800 chuẩn.
"""
import json, math, os, re, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda p: os.path.join(HERE, "..", "runs", p)
CHIA = 1000.0          # thang toạ độ tự khai trong <desc>
DUNG_SAI = 0.14        # cửa sổ ±14% của cả hai kênh, để hai kênh so được với nhau


def nap(p, khoa="episode_id"):
    o = {}
    for l in open(R(p), encoding="utf-8"):
        l = l.strip()
        if l:
            r = json.loads(l)
            o[(r[khoa], r["step_id"])] = r
    return o


def d14(p, g, wh):
    """Cửa sổ ±14% theo TỪNG TRỤC — trùng đúng hàm hit_disk của thước."""
    if not p or not g or not wh:
        return 0
    return int(abs(p[0] - g[0]) <= DUNG_SAI * wh[0] and abs(p[1] - g[1]) <= DUNG_SAI * wh[1])


def tu_khai(rec_preds, wh):
    """Toạ độ mô hình TỰ KHAI trong <desc> của trường `raw`, đổi về điểm ảnh."""
    if not rec_preds:
        return None
    m = re.search(r"<point>\s*([\d.]+)\s*,\s*([\d.]+)\s*</point>", rec_preds.get("raw", "") or "")
    if not m:
        return None
    return (float(m.group(1)) / CHIA * wh[0], float(m.group(2)) / CHIA * wh[1])


def main():
    D = {"MIN": nap("score_min_desc_seed101_raw.jsonl"),
         "S1": nap("score_s1_seed101_raw.jsonl"),
         "GRPO": nap("grpo_point/score_grpo_point_seed101_raw.jsonl"),
         "nguoi": nap("score_ceiling_human_raw.jsonl")}
    P = {"MIN": nap("preds_min_desc_seed101.jsonl"),
         "GRPO": nap("grpo_point/preds_grpo_point_seed101.jsonl")}
    REF = D["MIN"]
    EX = lambda n, x: int(D[n][x].get("executable", 0) or 0)

    # ── HAI quần thể, khác nhau đúng ở chỗ có cần GRPO hay không ─────────────────
    # Mục A và C chỉ đọc <point> của MIN nên quần thể rộng hơn (4.442). Mục B so MIN với
    # GRPO nên phải đòi cả hai đọc được (4.437). Gộp làm một là siết nhầm mục A và C, và
    # mọi con số của chúng lệch nhẹ so với bản đã công bố.
    CO = sorted(set.intersection(*[set(v) for v in D.values()]))
    G = lambda x: (REF[x]["gold_xy"], REF[x]["wh"])
    K = [x for x in CO if REF[x].get("gold_xy") and tu_khai(P["MIN"].get(x), REF[x]["wh"])]
    KB = [x for x in K if tu_khai(P["GRPO"].get(x), REF[x]["wh"])]
    A = {x: d14(tu_khai(P["MIN"][x], REF[x]["wh"]), *G(x)) for x in K}    # kênh A của MIN
    AG = {x: d14(tu_khai(P["GRPO"][x], REF[x]["wh"]), *G(x)) for x in KB}  # kênh A của GRPO
    B = {x: d14(REF[x].get("pred_xy"), *G(x)) for x in K}                  # kênh B (UGround)

    print("=" * 78)
    print("A. CHẨN ĐOÁN HAI KÊNH")
    print("=" * 78)
    print(f"  n = {len(K)}")
    print(f"  kênh A (mô hình tự khai) = {100*st.mean(A.values()):.2f}%"
          f"      kênh B (UGround đọc câu) = {100*st.mean(B.values()):.2f}%")
    du = [x for x in K if A[x]]
    sa = [x for x in K if not A[x]]
    print(f"\n  {'lát':<10}{'n':>7}{'MIN':>9}{'S1':>9}{'người':>9}")
    for ten, L in (("A ĐÚNG", du), ("A SAI", sa)):
        print(f"  {ten:<10}{len(L):>7}" + "".join(
            f"{100*st.mean([EX(n, x) for x in L]):>9.2f}" for n in ("MIN", "S1", "nguoi")))
    tong = 100 * st.mean([EX("nguoi", x) - EX("MIN", x) for x in K])
    print(f"\n  khoảng cách người − MIN toàn tập = {tong:+.2f} pp, phân bố:")
    for ten, L in (("A ĐÚNG", du), ("A SAI", sa)):
        g = 100 * (len(L) / len(K)) * st.mean([EX("nguoi", x) - EX("MIN", x) for x in L])
        print(f"    lát {ten:<8} tỉ trọng {100*len(L)/len(K):5.1f}%  góp {g:+6.2f} pp "
              f"({100*g/tong:5.1f}%)")
    gn = 100 * (st.mean([EX("nguoi", x) for x in du]) - st.mean([EX("nguoi", x) for x in sa]))
    gm = 100 * (st.mean([EX("MIN", x) for x in du]) - st.mean([EX("MIN", x) for x in sa]))
    print(f"  ⭐ thiếu hụt riêng của mô hình = {gm:.2f} − {gn:.2f} = {gm-gn:+.2f} pp")

    print("\n" + "=" * 78)
    print("B. HỆ SỐ TRUYỀN NHÂN QUẢ (dùng chính can thiệp GRPO đã chạy)")
    print("=" * 78)
    dA = 100 * (st.mean(AG.values()) - st.mean([A[x] for x in KB]))
    dE = 100 * st.mean([EX("GRPO", x) - EX("MIN", x) for x in KB])
    print(f"  n = {len(KB)}   d(kênh A) = {dA:+.2f} pp   d(exec) = {dE:+.3f} pp")
    print(f"  ⭐ hệ số truyền THỰC NGHIỆM = {dE/dA if dA else float('nan'):.3f}"
          f"   (so với tương quan mặt cắt ngang 0,739)")
    print(f"\n  {'ô chéo A(MIN) × A(GRPO)':<26}{'n':>7}{'MIN':>9}{'GRPO':>9}{'chênh':>9}")
    for ten, f in (("giữ ĐÚNG", lambda x: A[x] and AG[x]),
                   ("giữ SAI", lambda x: not A[x] and not AG[x]),
                   ("SAI -> ĐÚNG", lambda x: not A[x] and AG[x]),
                   ("ĐÚNG -> SAI", lambda x: A[x] and not AG[x])):
        Z = [x for x in KB if f(x)]
        if not Z:
            continue
        m, g = (100 * st.mean([EX(n, x) for x in Z]) for n in ("MIN", "GRPO"))
        print(f"  {ten:<26}{len(Z):>7}{m:>9.2f}{g:>9.2f}{g-m:>+9.2f}")
    sach = [x for x in KB if not A[x] and AG[x]]
    nguoc = [x for x in KB if A[x] and not AG[x]]
    hieu = 100 * st.mean([EX("GRPO", x) - EX("MIN", x) for x in sach]) if sach else 0
    can = 2.2 * len(KB) / hieu if hieu else float("nan")
    print(f"  ⭐ cần {can:.0f} lần lật SẠCH (= {100*can/len(sa):.1f}% lát A-sai), KHÔNG kèm lật "
          f"ngược, để vượt MDE 2,2")
    print(f"     GRPO lật được {len(sach)} bước = {100*len(sach)/len(sa):.1f}% lát A-sai "
          f"nhưng kèm {len(nguoc)} lần lật ngược")

    print("\n" + "=" * 78)
    print("C. TRẦN CHO ORPO TẦNG CÂU (thay CÂU trên lát A-sai, giữ nguyên lát A-đúng)")
    print("=" * 78)
    mT = 100 * st.mean([EX("MIN", x) for x in K])
    print(f"  MIN/101 toàn tập = {mT:.2f}")
    for ten, ngu in (("thay S1 trên TOÀN lát A-sai", "S1"),
                     ("thay CÂU NGƯỜI trên lát A-sai", "nguoi")):
        v = 100 * st.mean([EX(ngu, x) if not A[x] else EX("MIN", x) for x in K])
        print(f"  {ten:<34} = {v:6.2f}   ({v-mT:+.2f} pp)")
    n1 = [x for x in sa if not EX("MIN", x) and EX("nguoi", x)]
    n2 = [x for x in du if EX("MIN", x) and not EX("S1", x)]
    print(f"\n  tín hiệu cấp  : {len(n1):4d} bước A-sai có MIN=0 và người=1 = "
          f"{100*len(n1)/len(K):.2f} pp")
    print(f"  rủi ro xáo trộn: {len(n2):4d} bước A-đúng có MIN=1 và S1=0  = "
          f"{100*len(n2)/len(K):.2f} pp")

    print("\n" + "=" * 78)
    print("D. SÀN VÀ ĐỘ PHÂN GIẢI TỪNG LUẬT   (sàn = câu rỗng nghĩa 'Tap the button.')")
    print("=" * 78)
    F = {"tran": D["nguoi"], "san": nap("floor/score_f1_trong_raw.jsonl")}
    KF = [x for x in sorted(set(D["GRPO"]) & set(F["tran"]) & set(F["san"]))
          if REF.get(x, {}).get("gold_xy")]
    LUAT = [("exec Voronoi", lambda r: int(r.get("executable", 0) or 0)),
            ("AO x d14", lambda r: int(r.get("action_ok", 0) or 0) * int(r.get("toggle_ok", 0) or 0)
             * d14(r.get("pred_xy"), REF[(r["episode_id"], r["step_id"])]["gold_xy"],
                   REF[(r["episode_id"], r["step_id"])]["wh"]))]
    print(f"  n = {len(KF)}")
    print(f"  {'luật':<16}{'GRPO':>8}{'trần':>8}{'SÀN':>8}{'DẢI':>8}{'sàn/trần':>10}")
    goc = None
    for ten, f in LUAT:
        g, t, s = (100 * st.mean([f(src[x]) for x in KF])
                   for src in (D["GRPO"], F["tran"], F["san"]))
        if goc is None:
            goc = (g, s, t - s)
        print(f"  {ten:<16}{g:>8.2f}{t:>8.2f}{s:>8.2f}{t-s:>8.2f}{100*s/t:>9.1f}%")
        if ten != "exec Voronoi":
            print(f"      -> điểm {g-goc[0]:+.2f} pp nhưng SÀN {s-goc[1]:+.2f} pp  ==> "
                  f"{100*(s-goc[1])/(g-goc[0]):.0f}% mức tăng là thứ CÂU RỖNG NGHĨA cũng lấy được"
                  f"  | dải {t-s-goc[2]:+.2f} pp")


if __name__ == "__main__":
    main()
