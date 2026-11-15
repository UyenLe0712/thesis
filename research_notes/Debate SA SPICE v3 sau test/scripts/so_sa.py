import sys; sys.argv.append("--nhanh"); sys.path.insert(0, ".")
import bang_tong_hop as T
T.B = 2000
f = {n: p for n, p, _ in T.TEST}
names = ["SA-SPICE-v3 ck400", "SFT tiếp (= SFT-cont)", "ck500 (GRPO + SPICE)", "S1/101", "GRPO + SPICE chạy lại (A/A)", "GRPO + ROUGE-L", "SCST + SPICE", "ACE (R3)", "ck500 hạt 202"]
D = {n: T.nap_test(f[n]) for n in names}
A = D["SA-SPICE-v3 ck400"]
for c in ["vor", "d3", "aitwf", "aok"]:
    try:
        print(c, "SA=%.2f" % T.tb(A, c))
    except Exception as e:
        print(c, e)
for b in names[1:]:
    for c in ["vor", "d3", "aitwf"]:
        try:
            r = T.so(A, D[b], c)
            print(f"{c:6s} SA − {b}: {r['d']:+.2f} [{r['lo']:+.2f}; {r['hi']:+.2f}] cứu {r['cu']} phá {r['ph']} p={r['p']:.3g}  (mốc {T.tb(D[b], c):.2f})")
        except Exception as e:
            print(c, b, e)
