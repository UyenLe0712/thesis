# Offline diagnostics on SA-SPICE-v3 level-1 screen data (TRAIN-v3, 622 tap groups, 8 SFT-cont samples).
# Recovers per-sample SPICE s, chrF c, ROUGE-L rl, alpha (K_g) from the 9 stored arm rewards + length penalty d.
import json, re, sys, random, collections, math
R = "/mnt/d/Master/Thesis/runs/sa_spice_v3/"
WORD = re.compile(r"[A-Za-z0-9'-]+")
nw = lambda s: len(WORD.findall(s or ""))
pen = lambda y, g: min(0.05, 0.02 * max(0, nw(y) - nw(g) - 3))
clip = lambda x: min(1.0, max(0.0, x))

rows = [json.loads(l) for l in open(R + "split/train_v3.jsonl")]
M = {}
for i in (0, 1):
    for l in open(R + f"mau_k1/mau_{i}.jsonl"):
        d = json.loads(l); M[(d["episode_id"], d["step_id"])] = d
assert len(M) == 1000
EX = [{} for _ in range(9)]
for k in range(9):
    sub = "k0123" if k <= 3 else "k45678"
    for l in open(R + f"cham_k2/{sub}/score/score_k{k}_raw.jsonl"):
        o = json.loads(l); EX[k][(o["episode_id"], o["step_id"])] = int(o.get("executable", 0))
BU = {(o["episode_id"], o["step_id"]): o["R"] for o in map(json.loads, open(R + "screen/out/sa3_screen_buoc.jsonl"))}

G = []; maxerr = 0; n_rl_clip = 0
for r in rows:
    key = (r["episode_id"], r["step_id"])
    if not (r["action"]["action_type"] in ("click", "long_press") and "x" in r["action"]):
        continue
    m = M[key]; g = r["target_instruction"]; ys = m["mau"]
    S = []
    for k in range(1, 9):
        y = ys[k - 1]; rec = BU[key][k]; a = rec["R"]; A = rec["A"]
        if not (y or "").strip():
            S.append(None); continue
        d = pen(y, g)
        s = (a["SPICE-MATCH"] - 0.1 + d) / 0.8
        c = (a["FIXED"] - 0.1 + d - 0.64 * s) / 0.16
        rl = a["ROUGE-L"] + d if a["ROUGE-L"] > 0 else 0.0
        if a["ROUGE-L"] == 0: n_rl_clip += 1
        # check reconstruction
        maxerr = max(maxerr, abs(clip(c - d) - a["chrF"]), abs(clip(0.8 * s + 0.2 * A - d) - a["Action-SPICE"]))
        al = None
        if abs(s - c) > 0.03:
            al = ((a["Sparse-SPICE"] - 0.1 + d) / 0.8 - c) / (s - c)
        S.append(dict(s=s, c=c, rl=rl, d=d, A=A, al=al, arms=a, cid=None))
    # alpha per step -> K bucket
    als = [x["al"] for x in S if x and x["al"] is not None]
    if als:
        a0 = sorted(als)[len(als) // 2]
        K = min([0, 1, 2, 3], key=lambda k: abs(0.8 * min(1, k / 3) - a0))
    else:
        K = None
    # cider recover from SPIDEr-like: clip(0.5s+0.5cid-d)
    for x in S:
        if x:
            sp = x["arms"]["SPIDEr-like"]
            x["cid"] = (sp + x["d"] - 0.5 * x["s"]) / 0.5 if sp > 0 else None
    E = [EX[k][key] for k in range(1, 9)]
    G.append(dict(pkg=r["package"], E=E, S=S, K=K))
print("groups", len(G), "max reconstruction err", maxerr, "ROUGE clipped samples", n_rl_clip, file=sys.stderr)
print("K bucket counts (tap)", collections.Counter(g["K"] for g in G), file=sys.stderr)


def rankavg(vals_list):
    # within-group: average of ranks for each component list
    n = len(vals_list[0]); tot = [0.0] * n
    for v in vals_list:
        order = sorted(range(n), key=lambda i: v[i])
        rk = [0.0] * n; i = 0
        while i < n:
            j = i
            while j + 1 < n and abs(v[order[j + 1]] - v[order[i]]) < 1e-12: j += 1
            for t in range(i, j + 1): rk[order[t]] = (i + j) / 2
            i = j + 1
        tot = [a + b for a, b in zip(tot, rk)]
    return [t / len(vals_list) for t in tot]


def mk(f):
    def R(g):
        return [0.0 if x is None else f(x, g) for x in g["S"]]
    return R

CAND = collections.OrderedDict()
for arm in ("SPICE-MATCH", "Action-SPICE", "FIXED", "FIXED+A", "Sparse-SPICE", "SA-SPICE-v3", "chrF", "SPIDEr-like", "ROUGE-L"):
    CAND[arm] = mk(lambda x, g, arm=arm: x["arms"][arm])
CAND["N1 0.5s+0.5c"] = mk(lambda x, g: clip(0.5 * x["s"] + 0.5 * x["c"] - x["d"]))
CAND["N2 0.8(0.5s+0.5c)+0.2A"] = mk(lambda x, g: clip(0.8 * (0.5 * x["s"] + 0.5 * x["c"]) + 0.2 * x["A"] - x["d"]))
CAND["N3 chrF+A 0.8c+0.2A"] = mk(lambda x, g: clip(0.8 * x["c"] + 0.2 * x["A"] - x["d"]))
CAND["N4 SPICE lex-tiebreak chrF"] = mk(lambda x, g: 0.8 * x["s"] + 0.1 - x["d"] + 1e-4 * x["c"])
CAND["N5 s*A"] = mk(lambda x, g: clip(x["s"] * x["A"] - x["d"]))
CAND["N6 c*A"] = mk(lambda x, g: clip(x["c"] * x["A"] - x["d"]))
CAND["N7 sqrt(s*c)"] = mk(lambda x, g: clip(math.sqrt(max(0, x["s"]) * max(0, x["c"])) - x["d"]))
CAND["N8 0.5s+0.5rl"] = mk(lambda x, g: clip(0.5 * x["s"] + 0.5 * x["rl"] - x["d"]))
CAND["N9 chrF only if K=0 else FIXED(0.8s+0.2c)"] = mk(lambda x, g: clip((x["c"] if g["K"] == 0 else 0.8 * x["s"] + 0.2 * x["c"]) - x["d"]))
CAND["N10 0.5c+0.5rl"] = mk(lambda x, g: clip(0.5 * x["c"] + 0.5 * x["rl"] - x["d"]))
CAND["N11 (s+c+rl)/3"] = mk(lambda x, g: clip((x["s"] + x["c"] + x["rl"]) / 3 - x["d"]))
def rank_rs(g):
    idx = [i for i, x in enumerate(g["S"])]
    sv = [(-1 if x is None else x["arms"]["SPICE-MATCH"]) for x in g["S"]]
    cv = [(-1 if x is None else x["arms"]["chrF"]) for x in g["S"]]
    return rankavg([sv, cv])
CAND["N12 rank-avg(SPICE,chrF) in group"] = rank_rs
for w in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    CAND[f"W s-weight={w:.1f} (no A)"] = mk(lambda x, g, w=w: clip(w * x["s"] + (1 - w) * x["c"] - x["d"]))
for w in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    CAND[f"WA s-weight={w:.1f} +0.2A"] = mk(lambda x, g, w=w: clip(0.8 * (w * x["s"] + (1 - w) * x["c"]) + 0.2 * x["A"] - x["d"]))


def gstat(Rv, E):
    pos = [r for r, e in zip(Rv, E) if e]; neg = [r for r, e in zip(Rv, E) if not e]
    win = sum((p > n) + 0.5 * (abs(p - n) < 1e-12) for p in pos for n in neg)
    ties = sum(abs(p - n) < 1e-12 for p in pos for n in neg)
    zs = max(Rv) - min(Rv) < 1e-12
    m = max(Rv); top = [e for r, e in zip(Rv, E) if abs(r - m) < 1e-12]
    return len(pos) * len(neg), win, ties, zs, sum(top) / len(top) - sum(E) / len(E)

CACHE = {name: [f(g) for g in G] for name, f in CAND.items()}
def agg(idx, name):
    n = w = t = z = up = 0
    for i in idx:
        a, b, c, dd, e = gstat(CACHE[name][i], G[i]["E"])
        n += a; w += b; t += c; z += dd; up += e
    return dict(conc=w / n if n else float("nan"), tie=t / n if n else float("nan"), zs=z / len(idx), up=100 * up / len(idx), pairs=n)

ALL = list(range(len(G)))
res = {name: agg(ALL, name) for name in CAND}
cl = collections.defaultdict(list)
for i, g in enumerate(G): cl[g["pkg"]].append(i)
ks = sorted(cl); rd = random.Random(20261115); B = 1000
BS = {name: [] for name in CAND}
for _ in range(B):
    idx = [i for k in (rd.choice(ks) for _ in ks) for i in cl[k]]
    for name in CAND:
        BS[name].append(agg(idx, name)["conc"])
def ci(a, b):
    v = sorted(x - y for x, y in zip(BS[a], BS[b])); return (res[a]["conc"] - res[b]["conc"], v[int(.025 * B)], v[int(.975 * B) - 1])
out = {"n_groups": len(G), "n_pkg": len(ks), "B": B, "arms": res,
       "minus_chrF": {n: ci(n, "chrF") for n in CAND if n != "chrF"},
       "minus_SA": {n: ci(n, "SA-SPICE-v3") for n in CAND if n != "SA-SPICE-v3"}}
# K strata
strata = {}
for kb in (0, 1, 2, 3, None):
    idx = [i for i, g in enumerate(G) if g["K"] == kb]
    if not idx: continue
    strata[str(kb)] = {"n_groups": len(idx), **{n: agg(idx, n) for n in ("SPICE-MATCH", "chrF", "FIXED", "Sparse-SPICE", "SA-SPICE-v3", "N3 chrF+A 0.8c+0.2A", "ROUGE-L")}}
out["K_strata"] = strata
json.dump(out, open("/tmp/claude-1000/-mnt-d-Master-Thesis/a826d459-2edf-44cb-b931-82b4bcbff84c/scratchpad/screen_extra.json", "w"), indent=1)
for n, v in res.items():
    c1 = out["minus_chrF"].get(n); c2 = out["minus_SA"].get(n)
    f = lambda t: "-" if t is None else f"{t[0]:+.4f} [{t[1]:+.4f};{t[2]:+.4f}]"
    print(f"{n:42s} conc {v['conc']:.4f} tie {v['tie']:.3f} zs {v['zs']:.4f} up {v['up']:+.2f} | -chrF {f(c1)} | -SA {f(c2)}")
for kb, d in strata.items():
    print("K=", kb, "n", d["n_groups"], {n: round(d[n]["conc"], 4) for n in d if n != "n_groups"}, "ties SPICE", round(d["SPICE-MATCH"]["tie"], 3))
