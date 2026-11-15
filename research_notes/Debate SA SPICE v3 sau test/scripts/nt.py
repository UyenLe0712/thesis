import sys, json, collections; sys.path.insert(0, ".")
import metric_exec as M, score_run as S
recs = [json.loads(l) for l in open("dg1_cache/test_ac/test.jsonl")]
nt = [r for r in recs if r["action"].get("action_type") not in ("click","long_press") or "x" not in r["action"]]
P = {k: S.load_preds(v) for k, v in {
 "SA": "../runs/sa_spice_v3/test/pred_sa_ck400_test_nontap.jsonl",
 "SFTc": "../runs/sa_spice_v3/test/pred_sftcont_test_nontap.jsonl",
 "ck500": "../runs/grpo_spice/pred_ck500_test_nontap.jsonl",
 "S1": sys.argv[1]}.items()}
def ok(s, g): return int(bool(s) and M.canon_action(s, strict_back=True) == M.canon_action(g, strict_back=True))
U = []
for r in nt:
    k = (r["episode_id"], r["step_id"])
    if all(k in p for p in P.values()):
        U.append(dict(k=k, t=r["action"].get("action_type"), app=r.get("app") or f"ep{r['episode_id']}", g=r["gold_instruction"], **{n: ok(P[n][k], r["gold_instruction"]) for n in P}, sa=P["SA"][k], sf=P["SFTc"][k]))
print("n", len(U))
for b in ["SFTc", "ck500", "S1"]:
    for t in [None, "navigate_back", "scroll", "input_text", "wait", "open_app"]:
        V = [u for u in U if t is None or u["t"] == t]
        pt, ci, _, _ = S.cluster_bootstrap(V, lambda u: u["app"], lambda u: u["SA"] - u[b], B=2000)
        cu = sum(u["SA"] > u[b] for u in V); ph = sum(u["SA"] < u[b] for u in V)
        print(f"SA − {b:5s} {str(t):14s} n={len(V):4d} {100*pt:+6.2f} [{100*ci[0]:+.2f}; {100*ci[1]:+.2f}] cứu {cu} phá {ph}")
bk = [u for u in U if u["t"] == "navigate_back" and u["sf"] and u["SFTc"] and not u["SA"]]
c = collections.Counter(M.canon_action(u["sa"], strict_back=True) for u in bk); print(c)
for u in bk[:25]: print(repr(u["g"]), "|SFT:", repr(u["sf"]), "|SA:", repr(u["sa"]))
