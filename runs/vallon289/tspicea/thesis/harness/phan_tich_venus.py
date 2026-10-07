# -*- coding: utf-8 -*-
"""
FREE · offline — PHÉP B: đổi bộ trỏ sang UI-Venus-Ground-7B.

Trả lời một câu: điểm S2 thấp hơn S1 có phải do DỤNG CỤ ĐO không?

Không gọi bộ trỏ lần nào — chỉ đọc lại vết thô đã lưu, chạy bao nhiêu lần cũng miễn phí.
Dùng đúng hàm bootstrap gom cụm và đúng hạt giống của `phan_tich_s2.py` để hai lượt
phân tích so được với nhau.

Chạy:  python3 harness/phan_tich_venus.py
"""
import os, sys, json, math, statistics, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from phan_tich_s2 import nap, cum, boot_hieu, mcnemar          # tái dùng, không chép lại
RUNS = os.path.join(os.path.dirname(HERE), "runs")
VEN = os.path.join(RUNS, "venus")
N_TOAN = 4463          # mẫu số headline của mọi nhánh (score_run.py:516)
N_KHAC = 2532          # số bước S1/101 và S2/101 viết KHÁC nhau


def nap_tho(p):
    d = {}
    if not os.path.exists(p):
        return d
    for l in open(p, encoding="utf-8"):
        o = json.loads(l)
        o["exec"] = int(o.get("executable", 0))
        d[(o["episode_id"], o["step_id"])] = o
    return d


def phan_1_cong_a():
    """Sai số hai dụng cụ trên ĐÚNG 300 bước như nhau, câu chuẩn của người."""
    U = nap_tho(os.path.join(RUNS, "gate_a", "gate_A_raw.jsonl"))
    V = nap_tho(os.path.join(VEN, "venus_gate_raw.jsonl"))
    print("\n" + "=" * 78)
    print("① CỔNG A — sai số của chính DỤNG CỤ (đầu vào là câu chuẩn của người)")
    print("=" * 78)
    if not V:
        print("  ⏳ chưa có runs/venus/venus_gate_raw.jsonl — chạy ô 2/ô 4 của runbook trước")
        return None
    khoa = sorted(set(U) & set(V) & {k for k in V if "err_frac" in V[k]})
    print(f"  ghép cặp trên {len(khoa)} bước (UGround {len(U)} · UI-Venus {len(V)})")
    if not khoa:
        return None
    eu = [U[k]["err_frac"] for k in khoa]
    ev = [V[k]["err_frac"] for k in khoa]
    print(f"\n  {'':22}{'UGround':>10}{'UI-Venus':>11}")
    for ten, f in (("trung vị", statistics.median),
                   ("p75", lambda x: sorted(x)[int(.75 * len(x))]),
                   ("p90", lambda x: sorted(x)[int(.90 * len(x))]),
                   ("tỉ lệ ≤ 3%", lambda x: sum(1 for v in x if v <= .03) / len(x))):
        print(f"  {ten:<22}{f(eu):>9.2%}{f(ev):>10.2%}")
    tot = sum(1 for a, b in zip(eu, ev) if b < a)
    print(f"\n  UI-Venus trỏ sát hơn ở {tot}/{len(khoa)} bước ({tot/len(khoa):.1%})")
    med = statistics.median(ev)
    print(f"\n  ⇒ ngưỡng cổng A là 3%. UI-Venus {'ĐẠT' if med <= .03 else 'RỚT'} ({med:.2%}).")
    if med > .15:
        print("  ⛔ > 15% ⇒ gần chắc chắn GIẢI MÃ SAI HỆ TOẠ ĐỘ, không phải bộ trỏ dở.")
        print("     Mở venus_gate_raw.jsonl xem pred_xy có nằm ngoài khung ảnh không.")
    return med


def _so(ten, A, B, khoa, he_so=1.0):
    ea = sum(A[k]["exec"] for k in khoa) / len(khoa) * 100
    eb = sum(B[k]["exec"] for k in khoa) / len(khoa) * 100
    b, c, chi, p = mcnemar(A, B, khoa)
    pt, (lo, hi) = boot_hieu([(cum(A[k]), A[k]["exec"], B[k]["exec"]) for k in khoa])
    q, qlo, qhi = pt * he_so * 100, lo * he_so * 100, hi * he_so * 100
    print(f"  {ten:<26}{ea:>6.1f}%{eb:>6.1f}%{q:>+9.2f} [{qlo:+6.2f},{qhi:+6.2f}]"
          f"  {b:>4}/{c:<4} {p:.2g}")
    return q, qlo, qhi


def phan_2_s1_s2(lat):
    """Hai phép so, hai dụng cụ, trên cùng một lát:
       · S2 − S1  = câu hỏi chính
       · S1 − Base = CHỨNG NHÂN chống bẫy pha loãng."""
    V = {n: nap_tho(os.path.join(VEN, f"score_venus_{n}_{lat}_raw.jsonl"))
         for n in ("base", "s1", "s2")}
    if not (V["s1"] and V["s2"]):
        return None
    U = {"s1": nap("score_s1_seed101_raw.jsonl"),
         "s2": nap("score_s2_seed101_raw.jsonl"),
         "base": nap("score_base_raw.jsonl")}
    khoa = sorted(set(V["s1"]) & set(V["s2"]) & set(U["s1"]) & set(U["s2"]))
    he = N_KHAC / N_TOAN
    print("\n" + "=" * 78)
    print(f"② LÁT {lat} BƯỚC CÂU KHÁC NHAU — hai dụng cụ cạnh nhau (n={len(khoa)})")
    print("=" * 78)
    print(f"  {'phép so':<26}{'A':>6}{'B':>6}{'Δ (pp)':>10}{'KTC95':>16}  b / c      p")
    print("  " + "-" * 76)
    r = {}
    print("  ── S2 − S1, quy về mẫu số 4.463 ──")
    r["s2s1_U"] = _so("UGround", U["s1"], U["s2"], khoa, he)
    r["s2s1_V"] = _so("UI-Venus", V["s1"], V["s2"], khoa, he)
    if V["base"]:
        kb = sorted(set(khoa) & set(V["base"]) & set(U["base"]))
        print(f"  ── S1 − Base (CHỨNG NHÂN), trên lát, n={len(kb)} ──")
        r["base_U"] = _so("UGround", U["base"], U["s1"], kb)
        r["base_V"] = _so("UI-Venus", V["base"], V["s1"], kb)
    else:
        print("  ⏳ chưa có nhánh Base — KHÔNG đọc được phần ③ (xem mục Bẫy pha loãng)")
    print(f"\n  (Δ của S2−S1 nhân {he:.4f} = {N_KHAC}/{N_TOAN}: bước hai nhánh viết giống hệt"
          f"\n   đóng góp đúng 0 vào tử số nhưng vẫn nằm trong mẫu số. S1−Base không quy đổi"
          f"\n   — lát này không phải lát 'câu khác nhau' của cặp đó.)")
    return r


def phan_3_phan_quyet(r):
    print("\n" + "=" * 78)
    print("③ PHÁN QUYẾT — bảng đã khoá TRƯỚC khi chạy")
    print("=" * 78)
    if not r or "s2s1_V" not in r:
        print("  ⏳ chưa đủ dữ liệu"); return
    if "base_V" not in r:
        print("  ⛔ THIẾU NHÁNH BASE ⇒ KHÔNG kết luận được.")
        print("     Δ(S2−S1) co về 0 dưới UI-Venus khớp với CẢ HAI cách giải thích:")
        print("     'UGround thiên vị văn phong AC'  và  'UI-Venus đo kém hơn nên pha loãng'.")
        print("     Chứng nhân S1−Base là thứ duy nhất tách được hai cái đó."); return
    q, lo, hi = r["s2s1_V"]
    bU, bV = r["base_U"][0], r["base_V"][0]
    giu = bV / bU if bU else 0
    print(f"  Chứng nhân S1−Base: UGround {bU:+.2f} pp → UI-Venus {bV:+.2f} pp"
          f"  (giữ được {giu:.0%})")
    if giu < 0.6:
        print(f"\n  ⛔ PHA LOÃNG: chứng nhân chỉ còn {giu:.0%}. Dụng cụ mới nén cả thang đo,")
        print("     nên Δ(S2−S1) nhỏ đi là chuyện cơ học. KHÔNG kết luận gì về S2.")
        print("     Việc phải làm: đọc trần của UI-Venus (gate_a_ceiling.py) để đo mức nén.")
        return
    print(f"  ✅ chứng nhân giữ được {giu:.0%} ⇒ thang đo không bị nén, Δ dưới đây đọc được.\n")
    if hi < 0:
        print(f"  Δ(S2−S1) = {q:+.2f} pp [{lo:+.2f},{hi:+.2f}] — mép trên DƯỚI 0.")
        print("  ⇒ S2 vẫn THUA dưới bộ trỏ sạch AndroidControl. Kết luận vững:")
        print("     thành phần khai báo không có ích. Bỏ nhánh S2 được, sạch sẽ.")
        print("     Câu cho bài: 'kết quả âm, tái lập qua hai dụng cụ đo độc lập'.")
    elif lo > 0:
        print(f"  Δ(S2−S1) = {q:+.2f} pp [{lo:+.2f},{hi:+.2f}] — mép dưới TRÊN 0. ĐẢO DẤU.")
        print("  ⇒ Phát hiện về THƯỚC, không phải về S2. ⛔ ĐỪNG báo 'S2 thắng' vội —")
        print("     chạy lát lớn hơn, và đo xem câu S1 có thật giống văn phong AC hơn không.")
    else:
        print(f"  Δ(S2−S1) = {q:+.2f} pp [{lo:+.2f},{hi:+.2f}] — KTC CHỨA 0.")
        print("  ⇒ Dưới bộ trỏ sạch, chênh lệch S2−S1 không còn ý nghĩa thống kê, mà thang")
        print("     đo KHÔNG bị nén (chứng nhân còn nguyên) ⇒ một phần chênh lệch đo bằng")
        print("     UGround có thể do bộ trỏ quen văn phong AndroidControl.")
        print("     Cả hai con số phải vào bài, không chọn một.")
    print(f"\n  Trên cùng lát: UGround {r['s2s1_U'][0]:+.2f} pp · UI-Venus {q:+.2f} pp"
          f" · chênh {q - r['s2s1_U'][0]:+.2f} pp")


def phan_0_tu_kiem():
    """Chứng minh phép rút gọn còn đúng, bằng chính dữ liệu UGround đã có.

    Chấm 2.532 bước rồi nhân 2532/4463 phải tái tạo ĐÚNG hiệu ghép cặp của cả 4.463 bước.
    Ai đổi danh sách bước, đổi mẫu số, hay đổi cách nạp tệp thì phép kiểm này rớt ngay —
    thay vì âm thầm cho ra một con số trông hợp lý."""
    U1, U2 = nap("score_s1_seed101_raw.jsonl"), nap("score_s2_seed101_raw.jsonl")
    src = os.path.join(VEN, f"preds_venus_s1_{N_KHAC}.jsonl")
    if not os.path.exists(src):
        return
    khac = set()
    for l in open(src, encoding="utf-8"):
        r = json.loads(l); khac.add((r["episode_id"], r["step_id"]))
    lat = sorted(khac & set(U1) & set(U2))
    full = sorted(set(U1) & set(U2))
    cap = lambda ks: [(cum(U1[k]), U1[k]["exec"], U2[k]["exec"]) for k in ks]
    pl, _ = boot_hieu(cap(lat), B=200)
    pf, _ = boot_hieu(cap(full), B=200)
    quy = pl * N_KHAC / N_TOAN
    b1, c1, _, _ = mcnemar(U1, U2, lat)
    b2, c2, _, _ = mcnemar(U1, U2, full)
    print("=" * 78)
    print("⓪ TỰ KIỂM phép rút gọn (dữ liệu UGround đã có, không tốn gì)")
    print("=" * 78)
    print(f"  lát {len(lat)} bước → quy về {N_TOAN}: {quy*100:+.4f} pp")
    print(f"  tính thẳng trên {len(full)} bước      : {pf*100:+.4f} pp")
    print(f"  b/c: lát {b1}/{c1}  ·  toàn tập {b2}/{c2}")
    assert (b1, c1) == (b2, c2), "⛔ b/c lệch — lát KHÔNG chứa đủ cặp bất đồng"
    assert abs(quy - pf) < 1e-9, "⛔ phép quy đổi sai"
    print("  ✅ trùng tuyệt đối — chấm lát rút gọn tái tạo đúng hiệu của cả tập\n")


def main():
    phan_0_tu_kiem()
    med = phan_1_cong_a()
    ket = None
    for lat in (2532, 1266, 633):
        r = phan_2_s1_s2(lat)
        if r:
            ket = r
            break
    else:
        print("\n  ⏳ chưa có runs/venus/score_venus_s{1,2}_*_raw.jsonl — chạy ô 5 của runbook")
    if med is not None and med > .03:
        print("\n⛔ CỔNG A RỚT ⇒ mọi số ở phần ② không đọc được. Dụng cụ chưa dùng được"
              "\n   trên ảnh này; sửa dụng cụ trước, đừng kết luận gì về S2.")
        return
    phan_3_phan_quyet(ket)


if __name__ == "__main__":
    main()
