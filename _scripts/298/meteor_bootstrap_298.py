# 298b: KTC95 ĐÚNG cho Δ METEOR tổng (RAF − ck500) trên test 4.463 click.
# Script 298 in KTC của TRUNG BÌNH ĐIỂM TỪNG CÂU, trong khi METEOR tổng của pycocoevalcap do Java gộp từ
# thống kê khớp của cả kho (không phải trung bình câu) ⇒ KTC đó không chứa Δ số tổng (+0,17 nằm ngoài [+0,28; +1,03]).
# Ở đây: lấy thống kê khớp từng câu MỘT lần (lệnh SCORE), rồi mỗi lượt bootstrap gửi lại các dòng thống kê của
# mẫu lấy lại cho Java gộp (lệnh EVAL) ⇒ đúng đại lượng, không phải căn khớp lại.
# Mẫu bootstrap y hệt script 298 (theo tác vụ, random.Random(0), B=2000).
# Chạy từ GỐC KHO:  ~/.venvs/thesis/bin/python _scripts/298/meteor_bootstrap_298.py --raf _scripts/296/lai_test/raw_G4g_test.jsonl
import argparse, glob, json, os, random, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("--raf", required=True)
ap.add_argument("--goc", default="runs/grpo_spice/score_ck500_test_raw.jsonl")
ap.add_argument("--B", type=int, default=2000)
ap.add_argument("--out", default="runs/raf298/meteor_bootstrap_298.json")
a = ap.parse_args()
J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
os.environ["JAVA_HOME"] = J[-1]; os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.meteor.meteor import Meteor


def nap(p):
    return {(int(r["episode_id"]), int(r["step_id"])): r for r in map(json.loads, open(p, encoding="utf-8"))}


F = {"RAF": nap(a.raf), "ck500": nap(a.goc)}
K = sorted(F["ck500"])
assert set(F["RAF"]) == set(K) and len(K) == 4463
REF = [(F["ck500"][k].get("gold_instruction") or "").strip() for k in K]
assert [(F["RAF"][k].get("gold_instruction") or "").strip() for k in K] == REF
tk = PTBTokenizer()
G = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(REF)})
M = Meteor()


def eval_stats(stats):
    M.meteor_p.stdin.write(("EVAL ||| " + " ||| ".join(stats) + "\n").encode())
    M.meteor_p.stdin.flush()
    for _ in range(len(stats)):
        M.meteor_p.stdout.readline()
    return 100 * float(M.meteor_p.stdout.readline().strip())


ST, tong = {}, {}
for t in F:
    C = tk.tokenize({i: [{"caption": (F[t][k].get("sent") or "").strip()}] for i, k in enumerate(K)})
    ST[t] = [M._stat(C[i][0], G[i]) for i in range(len(K))]
    tong[t] = eval_stats(ST[t])
    ref_tong = M.compute_score(G, C)[0] * 100
    assert abs(tong[t] - ref_tong) < 1e-9, (t, tong[t], ref_tong)
    print(f"{t}: METEOR tổng {tong[t]:.4f} (khớp compute_score)", flush=True)

by = {}
for i, k in enumerate(K):
    by.setdefault(k[0], []).append(i)
eps = sorted(by)
rnd = random.Random(0)
samp = [[i for e in (rnd.choice(eps) for _ in eps) for i in by[e]] for _ in range(a.B)]
d, t0 = [], time.time()
for b, s in enumerate(samp):
    d.append(eval_stats([ST["RAF"][i] for i in s]) - eval_stats([ST["ck500"][i] for i in s]))
    if (b + 1) % 100 == 0:
        print(f"  bootstrap {b + 1}/{a.B} · {time.time() - t0:.0f} s", flush=True)
bs = sorted(d)
D = tong["RAF"] - tong["ck500"]
lo, hi = bs[int(.025 * a.B)], bs[int(.975 * a.B)]
p = 2 * min(sum(x <= 0 for x in d), sum(x >= 0 for x in d)) / a.B
print(f"\nRAF − ck500 METEOR tổng: {D:+.2f} [{lo:+.2f}; {hi:+.2f}]  p(bootstrap, hai phía) ≈ {min(p, 1):.4f}")
json.dump({"tong": tong, "delta": D, "ktc95": [lo, hi], "p_boot": min(p, 1.0), "B": a.B,
           "so_mau_le_0": sum(x <= 0 for x in d)}, open(a.out, "w"), ensure_ascii=False, indent=1)
print(f"→ {a.out}")
