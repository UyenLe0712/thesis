# -*- coding: utf-8 -*-
"""
dg3_pilot_mde.py — TINH MDE tu PILOT BASELINE (report/56 §6, report/53 §5.5).
Doc f_teacher theo tung app (chi do PHUONG SAI NEN — KHONG lo huong/do-lon hieu ung
-> KHONG pha pre-registration). Suy SD(d) can-tren than trong -> MDE cho G=12 (va G=15 du phong).
THUAN TOAN, KHONG goi API/GPU/mang (goi dg3_stats).

Input: JSON {app: [f_man_1, f_man_2, ...]}  (hoac {app: f_app}) — f_teacher pilot cham tren vai app.
Cong thuc SD(d): luc pilot chi co teacher -> gia dinh Var(f_student_proxy) ~ Var(f_teacher)
   => SD(d) ~ sqrt(2*Var(f_teacher))  (than trong; report/56 §6 cho phep can-tren).
   (Neu sau co checkpoint student -> truyen --var-student de thay proxy that.)

Chay tu-kiem:  python dg3_pilot_mde.py --selftest
Chay that   :  python dg3_pilot_mde.py --pilot dg3_cache/pilot_f_teacher.json
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(__file__))
import dg3_stats


def f_app_from_pilot(pilot):
    """pilot: {app: [f_man...]} hoac {app: f_app}. Tra {app: f_app} (trung binh theo man)."""
    out = {}
    for app, v in pilot.items():
        if isinstance(v, (list, tuple)):
            vals = [x for x in v if x is not None]      # loai man 0-nhac (f=None), vá A1-2
            if vals:
                out[app] = sum(vals) / len(vals)
        else:
            out[app] = float(v)
    return out


def compute_mde(pilot, var_student=None):
    """
    Tra dict: n_app, var_teacher, sd_d, mde_G12, mde_G15, suggest_1515(bool).
    var_student=None -> gia dinh = var_teacher (than trong). >0 -> dung so do that.
    """
    f_app = f_app_from_pilot(pilot)
    vals = list(f_app.values())
    var_t = dg3_stats.variance(vals, ddof=1)
    var_s = var_t if var_student is None else var_student
    sd_d = dg3_stats.sd_upper_bound(var_t, var_s)
    mde12 = dg3_stats.mde(sd_d, G=12)
    mde15 = dg3_stats.mde(sd_d, G=15)
    return {"n_app": len(vals), "var_teacher": var_t, "sd_d": sd_d,
            "mde_G12": mde12, "mde_G15": mde15,
            "suggest_1515": mde12 > 0.15}      # report/56 §6: >15-20pp -> can nhac 15/15


def _report(res):
    print("=" * 64)
    print(f"PILOT MDE  |  {res['n_app']} app  |  Var(f_teacher)={res['var_teacher']:.4f}")
    print(f"SD(d) can-tren = sqrt(Var_teacher + Var_student_proxy) = {res['sd_d']:.4f}")
    print(f"MDE (G=12, power=80%, alpha=5%) = {res['mde_G12']*100:.1f} pp")
    print(f"MDE (G=15 du phong)             = {res['mde_G15']*100:.1f} pp")
    print("-" * 64)
    if res["suggest_1515"]:
        print("⚠  MDE_G12 > 15pp -> CAN NHAC tang split len 15/15 TRUOC khi khoa nguong (report/56 §6).")
    else:
        print("✓  MDE_G12 <= 15pp -> giu split 18/12. Dien so nay vao report/56 §6 roi commit lan 2.")
    print(f"\n=> Dien vao report/56 §6:  [MDE = {res['mde_G12']*100:.1f} pp]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--pilot", help="JSON {app: [f_man...]}")
    ap.add_argument("--var-student", type=float, default=None)
    args = ap.parse_args()
    if args.selftest:
        return 0 if _selftest() else 1
    if not args.pilot:
        print("Thieu --pilot <file.json>. Xem --selftest de kiem logic.")
        return 0
    pilot = json.load(open(args.pilot, encoding="utf-8"))
    _report(compute_mde(pilot, args.var_student))
    return 0


# ----------------------------- TU KIEM (fake data, khong mang) -----------------------------
def _selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    # 1) f_app_from_pilot: trung binh theo man, loai None.
    fa = f_app_from_pilot({"a": [1.0, 0.0], "b": [0.5, None, 0.5], "c": 0.8})
    chk("f_app: a=0.5", abs(fa["a"] - 0.5) < 1e-9)
    chk("f_app: b bo None -> 0.5", abs(fa["b"] - 0.5) < 1e-9)
    chk("f_app: c scalar giu nguyen", abs(fa["c"] - 0.8) < 1e-9)

    # 2) MDE khop cong thuc: var thap -> MDE nho; var cao -> MDE lon + goi y 15/15.
    low = compute_mde({f"app{i}": [0.9 + 0.01 * (i % 3)] for i in range(8)})   # phuong sai rat nho
    chk("MDE: var nho -> MDE nho (<15pp)", low["mde_G12"] < 0.15 and not low["suggest_1515"])

    hi_vals = {f"app{i}": [0.1 if i % 2 else 0.9] for i in range(8)}            # var lon
    hi = compute_mde(hi_vals)
    chk("MDE: var lon -> MDE lon (>15pp)", hi["mde_G12"] > 0.15 and hi["suggest_1515"])

    # 3) MDE_G15 < MDE_G12 (nhieu app -> power cao hon -> MDE nho hon) voi cung SD.
    chk("MDE: G15 < G12", hi["mde_G15"] < hi["mde_G12"])

    # 4) Khop dg3_stats truc tiep: SD(d)=sqrt(2*var).
    import math
    vals = [0.4, 0.6, 0.5, 0.7]
    r = compute_mde({f"a{i}": [v] for i, v in enumerate(vals)})
    var_t = dg3_stats.variance(vals)
    chk("SD(d)=sqrt(2*var_teacher)", abs(r["sd_d"] - math.sqrt(2 * var_t)) < 1e-9)
    chk("MDE=3.0765*SD/sqrt(12)", abs(r["mde_G12"] - 3.0765 * r["sd_d"] / math.sqrt(12)) < 1e-9)

    # 5) var-student truyen tay ghi de proxy.
    r2 = compute_mde({f"a{i}": [v] for i, v in enumerate(vals)}, var_student=0.0)
    chk("var_student=0 -> SD(d)=SD(teacher)", abs(r2["sd_d"] - math.sqrt(var_t)) < 1e-9)

    print("\n=> " + ("TAT CA PASS" if ok else "CO FAIL — xem tren"))
    return ok


if __name__ == "__main__":
    sys.exit(main() or 0)
