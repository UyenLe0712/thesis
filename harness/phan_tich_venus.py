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


def phan_2_s1_s2(lat):
    """Δ(S2−S1) theo UI-Venus, và cùng đại lượng đó theo UGround trên ĐÚNG các bước ấy."""
    V1 = nap_tho(os.path.join(VEN, f"score_venus_s1_{lat}_raw.jsonl"))
    V2 = nap_tho(os.path.join(VEN, f"score_venus_s2_{lat}_raw.jsonl"))
    if not (V1 and V2):
        return False
    U1 = nap("score_s1_seed101_raw.jsonl")
    U2 = nap("score_s2_seed101_raw.jsonl")
    khoa = sorted(set(V1) & set(V2) & set(U1) & set(U2))
    print("\n" + "=" * 78)
    print(f"② S2 − S1 TRÊN LÁT {lat} BƯỚC CÂU KHÁC NHAU — hai dụng cụ cạnh nhau")
    print("=" * 78)
    print(f"  ghép cặp trên {len(khoa)} bước\n")
    # hệ số quy về mẫu số toàn tập: bước hai nhánh viết GIỐNG hệt đóng góp đúng 0 vào
    # tử số nhưng VẪN nằm trong mẫu số 4.463
    he_so = N_KHAC / N_TOAN
    print(f"  {'dụng cụ':<12}{'S1':>7}{'S2':>7}{'Δ trên lát':>13}"
          f"{'Δ quy về 4.463':>17}   b / c      p")
    print("  " + "-" * 74)
    ket = {}
    for ten, A, B in (("UGround", U1, U2), ("UI-Venus", V1, V2)):
        ea = sum(A[k]["exec"] for k in khoa) / len(khoa) * 100
        eb = sum(B[k]["exec"] for k in khoa) / len(khoa) * 100
        b, c, chi, p = mcnemar(A, B, khoa)
        pt, (lo, hi) = boot_hieu([(cum(A[k]), A[k]["exec"], B[k]["exec"]) for k in khoa])
        # quy về toàn tập: nhân hệ số, cả điểm lẫn hai mép KTC
        q, qlo, qhi = pt * he_so * 100, lo * he_so * 100, hi * he_so * 100
        print(f"  {ten:<12}{ea:>6.1f}%{eb:>6.1f}%{pt*100:>+9.2f}pp"
              f"{q:>+10.2f} [{qlo:+.2f},{qhi:+.2f}]  {b:>4}/{c:<4} {p:.2g}")
        ket[ten] = (q, qlo, qhi)
    print(f"\n  (Δ trên lát nhân {he_so:.4f} = {N_KHAC}/{N_TOAN}. Bước hai nhánh viết giống"
          f"\n   hệt đóng góp đúng 0 — đã kiểm bằng UGround: 1.931 bước, 0 bất đồng.)")
    print(f"\n  Mốc đối chiếu — Δ đo trên TOÀN BỘ 4.463 bước bằng UGround: −1,93 pp"
          f" [−3,06 · −0,75]")
    return ket


def phan_3_phan_quyet(ket):
    print("\n" + "=" * 78)
    print("③ PHÁN QUYẾT theo bảng bốn ô đã khoá TRƯỚC khi chạy")
    print("=" * 78)
    if not ket or "UI-Venus" not in ket:
        print("  ⏳ chưa đủ dữ liệu")
        return
    q, lo, hi = ket["UI-Venus"]
    if hi < 0:
        print(f"  Δ = {q:+.2f} pp, KTC95 [{lo:+.2f},{hi:+.2f}] — mép trên DƯỚI 0.")
        print("  ⇒ S2 vẫn THUA dưới bộ trỏ sạch AndroidControl.")
        print("  ⇒ Kết luận vững: thành phần khai báo không có ích. Bỏ nhánh S2 được, sạch sẽ.")
        print("     Bài viết: 'kết quả âm, tái lập qua hai dụng cụ đo độc lập'.")
    elif lo > 0:
        print(f"  Δ = {q:+.2f} pp, KTC95 [{lo:+.2f},{hi:+.2f}] — mép dưới TRÊN 0.")
        print("  ⇒ ĐẢO DẤU khi đổi dụng cụ. Đây là phát hiện về THƯỚC, không phải về S2.")
        print("  ⛔ ĐỪNG báo 'S2 thắng'. Phải chạy thêm trước khi khẳng định:")
        print("     · lát lớn hơn để loại nhiễu lấy mẫu")
        print("     · kiểm câu của S1 có thật sự 'giống văn phong AC' hơn không (đo được offline)")
    else:
        print(f"  Δ = {q:+.2f} pp, KTC95 [{lo:+.2f},{hi:+.2f}] — KTC CHỨA 0.")
        print("  ⇒ Dưới bộ trỏ sạch, chênh lệch S2−S1 KHÔNG còn ý nghĩa thống kê.")
        print("  ⇒ Không đọc thành 'S2 tốt'. Đọc thành: một phần chênh lệch đo bằng UGround")
        print("     có thể do bộ trỏ quen văn phong AndroidControl. Cả hai số phải vào bài.")
    u = ket.get("UGround")
    if u:
        print(f"\n  Trên cùng lát này: UGround {u[0]:+.2f} pp · UI-Venus {q:+.2f} pp"
              f" · chênh {q-u[0]:+.2f} pp")


def phan_0_tu_kiem():
    """Chứng minh phép rút gọn còn đúng, bằng chính dữ liệu UGround đã có.

    Chấm 2.532 bước rồi nhân 2532/4463 phải tái tạo ĐÚNG hiệu ghép cặp của cả 4.463 bước.
    Nếu ai đó đổi danh sách bước, đổi mẫu số, hay đổi cách nạp tệp, phép kiểm này rớt
    ngay — thay vì âm thầm cho ra một con số trông hợp lý."""
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
