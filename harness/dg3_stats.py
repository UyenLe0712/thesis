# -*- coding: utf-8 -*-
"""
dg3_stats.py — THONG KE cho tru chinh (pre-register report/56 §4-§6).
THUAN TOAN, KHONG goi API/GPU/mang. Dung chung cho dg3_eval_no_vh.py + tinh MDE pilot.

Cung cap:
  - exact_sign_flip(d)      : test dau chinh xac, liet ke 2^G to hop dau (G<=~13). report/56 §4.
  - ci_sign_flip(d, alpha)  : CI bang test-inversion tren chinh phan phoi exact do.
  - mde(sd, G)              : Minimum Detectable Effect (report/56 §6, cong thuc Julious xap xi lien tuc).
  - sd_upper_bound(vT, vS)  : can tren than trong SD(d) ~ sqrt(Var(f_teacher)+Var(f_student_proxy)).

Chay tu-kiem (khong can mang):  python dg3_stats.py
"""
import itertools, math

# (t_{0.025,df} + t_{0.20,df}) — tra bang t 1 phia, hardcode vi khong co scipy.
#   G=12 -> df=11 : 2.2010 + 0.8755 = 3.0765  (~3.077, khop report/56 §6)
#   G=15 -> df=14 : 2.1448 + 0.8681 = 3.0129  (phuong an du phong 15/15)
_T_SUM = {11: 3.0765, 14: 3.0129}


def _t_stat(d):
    """t = mean(d) / (std(d, ddof=1)/sqrt(G)). Tra 0.0 neu std=0 (tranh chia 0)."""
    G = len(d)
    if G < 2:
        return 0.0
    mean = sum(d) / G
    var = sum((x - mean) ** 2 for x in d) / (G - 1)
    if var <= 0:
        return 0.0
    return mean / (math.sqrt(var) / math.sqrt(G))


def exact_sign_flip(d):
    """
    Test dau chinh xac (exact randomization/sign-flip). report/56 §4.
    H0: phan phoi d_j doi xung quanh 0 (khong co hieu ung).
    Liet ke TOAN BO 2^G to hop dau s in {+1,-1}^G, tinh t cho moi lat, p 2-phia.
    Tra: (t_obs, p_value, null_stats). Yeu cau G<=~13 (2^13=8192, con nhanh).
    """
    G = len(d)
    if G == 0:
        return (0.0, 1.0, [])
    if G > 16:
        raise ValueError(f"G={G} qua lon cho exact enumerate (2^G). Dung wild-bootstrap thay the.")
    t_obs = _t_stat(d)
    null_stats = []
    for signs in itertools.product((1, -1), repeat=G):
        flipped = [s * x for s, x in zip(signs, d)]
        null_stats.append(_t_stat(flipped))
    at = abs(t_obs)
    p = sum(1 for x in null_stats if abs(x) >= at - 1e-12) / len(null_stats)
    return (t_obs, p, null_stats)


def ci_sign_flip(d, alpha=0.05, grid=801):
    """
    CI (1-alpha) bang TEST-INVERSION tren phan phoi sign-flip exact (report/56 §4).
    CI = { mu0 : p 2-phia cua sign-flip test tren (d - mu0) >= alpha }.
    Quet luoi mu0 quanh mean +/- 6*se, tra (lo, hi). Tra (mean,mean) neu G<2.
    """
    G = len(d)
    if G < 2:
        m = d[0] if d else 0.0
        return (m, m)
    mean = sum(d) / G
    var = sum((x - mean) ** 2 for x in d) / (G - 1)
    se = math.sqrt(var) / math.sqrt(G) if var > 0 else 0.0
    if se == 0:
        return (mean, mean)
    lo_edge, hi_edge = mean - 6 * se, mean + 6 * se
    accepted = []
    for k in range(grid):
        mu0 = lo_edge + (hi_edge - lo_edge) * k / (grid - 1)
        _, p, _ = exact_sign_flip([x - mu0 for x in d])
        if p >= alpha:
            accepted.append(mu0)
    if not accepted:
        return (mean, mean)          # suy bien: tra diem uoc luong
    return (min(accepted), max(accepted))


def mde(sd, G=12, alpha=0.05, power=0.80):
    """
    Minimum Detectable Effect (report/56 §6). Xap xi lien tuc kieu Julious:
        MDE = (t_{alpha/2,df} + t_{beta,df}) * SD(d_j) / sqrt(G),  df = G-1.
    Chi ho tro alpha=0.05, power=0.80 (df da hardcode). G in {12,15}.
    """
    if (alpha, power) != (0.05, 0.80):
        raise ValueError("Chi hardcode t cho alpha=0.05, power=0.80 (df=11 va df=14).")
    df = G - 1
    if df not in _T_SUM:
        raise ValueError(f"Chua hardcode t-sum cho df={df} (G={G}). Chi co G=12,15.")
    return _T_SUM[df] * sd / math.sqrt(G)


def sd_upper_bound(var_teacher, var_student_proxy):
    """Can tren than trong SD(d) ~ sqrt(Var(f_teacher)+Var(f_student_proxy)) (gia dinh doc lap)."""
    return math.sqrt(max(0.0, var_teacher) + max(0.0, var_student_proxy))


def variance(xs, ddof=1):
    """Phuong sai mau (ddof=1 mac dinh). Tien ich cho pilot MDE."""
    n = len(xs)
    if n <= ddof:
        return 0.0
    m = sum(xs) / n
    return sum((x - m) ** 2 for x in xs) / (n - ddof)


# ----------------------------- TU KIEM (fake data, khong mang) -----------------------------
def _selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    # 1) Truong hop tay tinh duoc: d=[1,2,3] toan duong, KHONG suy bien (var>0).
    #    |t|=|mean|/sqrt(var) dat cuc dai khi tat ca cung dau (mean max, var min)
    #    -> chi +++ va --- co |t_flip|>=|t_obs| trong 2^3=8 to hop -> p 2-phia = 2/8 = 0.25.
    t_obs, p, nulls = exact_sign_flip([1.0, 2.0, 3.0])
    chk("exact: d=[1,2,3] -> 8 to hop", len(nulls) == 8)
    chk("exact: d=[1,2,3] -> p=0.25", abs(p - 0.25) < 1e-9)
    chk("exact: t_obs>0", t_obs > 0)

    # 2) Doi xung quanh 0 -> khong bac bo (p lon).
    _, p_sym, _ = exact_sign_flip([2.0, -2.1, 1.9, -1.8, 2.05, -1.95])
    chk("exact: doi xung -> p>=0.30", p_sym >= 0.30)

    # 3) Hieu ung manh, dong nhat duong -> p nho nhat co the (2/2^G).
    d_big = [0.3, 0.28, 0.35, 0.31, 0.29, 0.33, 0.27, 0.34, 0.30, 0.32, 0.31, 0.29]  # G=12
    _, p_big, nb = exact_sign_flip(d_big)
    chk("exact: G=12 -> 4096 to hop", len(nb) == 4096)
    chk("exact: toan duong tach bach -> p=2/4096", abs(p_big - 2 / 4096) < 1e-9)

    # 4) CI cho d toan duong lon phai NAM TREN 0 (lo>0).
    lo, hi = ci_sign_flip(d_big)
    chk("CI: d toan duong -> lo>0", lo > 0)
    chk("CI: lo<=mean<=hi", lo <= sum(d_big) / 12 <= hi)

    # 5) CI cho d doi xung quanh 0 phai CHUA 0.
    lo2, hi2 = ci_sign_flip([0.2, -0.19, 0.21, -0.2, 0.18, -0.22, 0.2, -0.19])
    chk("CI: doi xung -> chua 0", lo2 <= 0 <= hi2)

    # 6) MDE khop vi du report/56 (SD=0.15, G=12 -> ~0.1332).
    m = mde(0.15, G=12)
    chk("MDE: SD=0.15,G=12 -> ~0.133", abs(m - 0.15 * 3.0765 / math.sqrt(12)) < 1e-9 and abs(m - 0.1332) < 1e-3)
    chk("MDE: G=15 co ho tro", mde(0.15, G=15) > 0)

    # 7) sd_upper_bound + variance.
    chk("sd_upper_bound", abs(sd_upper_bound(0.01, 0.02) - math.sqrt(0.03)) < 1e-12)
    chk("variance ddof=1", abs(variance([1, 2, 3]) - 1.0) < 1e-12)

    print("\n=> " + ("TAT CA PASS" if ok else "CO FAIL — xem tren"))
    return ok


if __name__ == "__main__":
    _selftest()
