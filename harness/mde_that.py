# -*- coding: utf-8 -*-
"""FREE · offline — MDE THẬT từ cặp hạt giống, và ngưỡng để khoá vào `report/106`.

## Vì sao không dùng thẳng "59,6 vs 59,1 ⇒ nhiễu 0,5 pp"

Hai con số đó là **micro trên toàn tập**. Cái cần cho việc khoá ngưỡng là **sai số chuẩn của
HIỆU**, mà hiệu ở đây là hiệu **ghép cặp**: hai hạt giống chấm trên cùng 4.462 bước, nên phần
lớn biến thiên (bước nào dễ, bước nào khó, app nào rắc rối) **triệt tiêu** trong hiệu số. Đọc
như hai mẫu độc lập là tự làm sai số phồng lên.

Và có **HAI nguồn nhiễu**, phải cộng cả hai:

  (a) nhiễu của THƯỚC trên một cặp nhánh — bootstrap cụm trên hiệu ghép cặp
  (b) nhiễu GIỮA HẠT GIỐNG — chính là thứ cặp 101/202 sinh ra để đo

Bỏ (b) là đúng lỗi mà giao thức hai hạt giống được lập ra để chặn: so S2 một hạt giống với S1
một hạt giống rồi tưởng chênh lệch là hiệu ứng, trong khi nó có thể chỉ là hai lượt train khác
nhau.

⚠️ (b) ước từ **một** quan sát (1 bậc tự do) nên rất thô. Script in cả bản thô lẫn bản thận
trọng; **khoá ngưỡng theo bản thận trọng**.

Chạy: python3 harness/mde_that.py
"""
import os, json, math, random

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "runs"))
B = 10000
SEED = 20260805
Z = 2.8   # z(0,975) + z(0,80) — phát hiện được với lực 80% ở mức 5%


def nap(p):
    """Nạp ĐỦ quần thể 4.463. Bước bị pipeline chấm bỏ qua (cờ `bo_qua`) tính là
    `executable = 0`, KHÔNG loại khỏi mẫu số.

    Sửa 23/8/2026: bản cũ `if "bo_qua" not in o` là **complete-case analysis** — nó xoá
    khỏi cả tử số lẫn mẫu số đúng những bước mà chính model làm hỏng, tức làm đẹp số theo
    hướng có lợi. report/106 khoá đối tượng chấm là toàn bộ 4.463 bước chạm."""
    d = {}
    for l in open(p, encoding="utf-8"):
        o = json.loads(l)
        o.setdefault("executable", 0)          # dòng `bo_qua` không có trường này
        d[(o["episode_id"], o["step_id"])] = o
    return d


def cum(o):
    """Cụm = ứng dụng; **TÁC VỤ** không gán được app tự thành một cụm.

    Sửa 23/8/2026: bản cũ trả `__don__{episode}_{step}`, tức mỗi BƯỚC một cụm — cho 2.906
    cụm. report/106 sửa đổi (e) khoá luật *"mỗi TÁC VỤ không-rõ-app là một cụm"* và ghi
    **G = 1.091**, đúng con số bài báo đang trích (`main.tex:411`). Chia nhỏ cụm hơn hồ sơ
    cho phép làm SE nhỏ đi, tức nới ngưỡng theo hướng có lợi.
    Đo được sau khi sửa: SE 0,386 → 0,375 pp (~3%), không đổi kết luận nào — vẫn phải sửa
    vì đây là lệch hồ sơ đăng ký, không phải vì nó cứu được con số."""
    a = (o.get("app") or "").strip().lower()
    return a if a else f"__don__{o['episode_id']}"


def boot_hieu(K, A, Bn, b=B):
    """Bootstrap CỤM trên hiệu ghép cặp: lấy lại cụm, tính lại hiệu trên mẫu đó."""
    theo = {}
    for k in K:
        theo.setdefault(cum(A[k]), []).append(k)
    ten = list(theo)
    rng = random.Random(SEED)
    out = []
    for _ in range(b):
        m = [theo[ten[rng.randrange(len(ten))]] for _ in range(len(ten))]
        n = sum(len(x) for x in m)
        s = sum(Bn[k]["executable"] - A[k]["executable"] for x in m for k in x)
        out.append(s / n * 100)
    out.sort()
    return out


def mcnemar(K, A, Bn):
    b = sum(1 for k in K if A[k]["executable"] == 1 and Bn[k]["executable"] == 0)
    c = sum(1 for k in K if A[k]["executable"] == 0 and Bn[k]["executable"] == 1)
    n = b + c
    chi = (abs(b - c) - 1) ** 2 / n if n else 0.0
    return b, c, n, chi, (math.erfc(math.sqrt(chi / 2)) if n else 1.0)


def main():
    s1 = nap(f"{R}/score_s1_seed101_raw.jsonl")
    s2 = nap(f"{R}/score_s1_seed202_raw.jsonl")
    ba = nap(f"{R}/score_base_raw.jsonl")
    ce = nap(f"{R}/score_ceiling_human_raw.jsonl")
    K = sorted(set(s1) & set(s2))
    print(f"ghép cặp trên {len(K)} bước (s1/101 {len(s1)} · s1/202 {len(s2)})\n")

    # ── 1. null thực nghiệm: hai hạt giống, KHÔNG can thiệp gì ──────────────────────
    e1 = sum(s1[k]["executable"] for k in K) / len(K) * 100
    e2 = sum(s2[k]["executable"] for k in K) / len(K) * 100
    b, c, nd, chi, p = mcnemar(K, s1, s2)
    d = boot_hieu(K, s1, s2)
    se = (sum((x - sum(d) / len(d)) ** 2 for x in d) / (len(d) - 1)) ** 0.5
    print("═" * 70)
    print("1. NULL THỰC NGHIỆM — s1/202 trừ s1/101 (chỉ khác HẠT GIỐNG)")
    print("═" * 70)
    print(f"  {e1:.2f}% → {e2:.2f}%   hiệu {e2-e1:+.2f} pp")
    print(f"  KTC95 bootstrap cụm [{d[int(.025*B)]:+.2f}, {d[int(.975*B)]:+.2f}]  SE {se:.2f} pp")
    print(f"  McNemar: 101 trúng/202 trượt {b} · ngược lại {c} · bất đồng {nd}"
          f" = {nd/len(K):.1%} · χ²={chi:.2f} p={p:.3f}")
    print(f"  {'✔ KTC chứa 0' if d[int(.025*B)] < 0 < d[int(.975*B)] else '⚠ KTC KHÔNG chứa 0'}"
          f" — dưới null thì phải chứa 0, và nó {'chứa' if d[int(.025*B)]<0<d[int(.975*B)] else 'KHÔNG chứa'}")
    se_hat = abs(e2 - e1) / 1.128   # E|X−Y| = 1,128·σ khi X,Y ~ N(μ, σ²) độc lập
    print(f"  ⇒ σ giữa hạt giống ước thô: {se_hat:.2f} pp  ⚠ từ MỘT quan sát, 1 bậc tự do")

    # ── 2. mốc đối chiếu: cặp có can thiệp thật (S1 vs Base) ────────────────────────
    print("\n" + "═" * 70)
    print("2. ĐỐI CHIẾU — cặp có can thiệp thật, để thấy null trông khác thế nào")
    print("═" * 70)
    for ten, A, Bn in [("S1/101 − Base", ba, s1), ("S1/202 − Base", ba, s2),
                       ("Trần − S1/101", s1, ce)]:
        KK = sorted(set(A) & set(Bn))
        bb, cc, nn, ch, pp = mcnemar(KK, A, Bn)
        dd = boot_hieu(KK, A, Bn)
        h = sum(Bn[k]["executable"] - A[k]["executable"] for k in KK) / len(KK) * 100
        print(f"  {ten:16s} {h:+6.2f} pp  KTC95 [{dd[int(.025*B)]:+.2f}, {dd[int(.975*B)]:+.2f}]"
              f"  bất đồng {nn/len(KK):5.1%}  p={pp:.4f}")

    # ── 3. MDE để khoá ngưỡng ───────────────────────────────────────────────────────
    print("\n" + "═" * 70)
    print("3. NGƯỠNG CHO S2 — cộng cả hai nguồn nhiễu")
    print("═" * 70)
    print(f"  (a) nhiễu THƯỚC, ghép cặp có cụm     SE = {se:.2f} pp")
    print(f"  (b) nhiễu GIỮA HẠT GIỐNG (ước thô)   σ = {se_hat:.2f} pp")
    for nhan, k in [("1 hạt giống mỗi nhánh", 1), ("2 hạt giống mỗi nhánh (đã đăng ký)", 2)]:
        se_tong = math.sqrt(se ** 2 + 2 * se_hat ** 2 / k)
        print(f"  {nhan:36s} SE tổng {se_tong:.2f} ⇒ MDE {Z*se_tong:.2f} pp")
    se_than = math.sqrt(se ** 2 + 2 * (2 * se_hat) ** 2 / 2)
    print(f"  {'THẬN TRỌNG (σ hạt giống ×2)':36s} SE tổng {se_than:.2f} ⇒ "
          f"MDE {Z*se_than:.2f} pp  ← khoá theo dòng này")

    room = sum(ce[k]["executable"] - s1[k]["executable"] for k in K) / len(K) * 100
    print(f"\n  dư địa tới trần: {room:.1f} pp ⇒ S2 phải lấy "
          f"{Z*se_than/room:.0%} dư địa mới đọc được")


if __name__ == "__main__":
    main()
