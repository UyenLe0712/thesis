"""Đọc kết quả DEV-v3 lượt đầu (14/11): exec ghép cặp (bootstrap cụm như score_run) + bước không chạm (verifier v3).
Chạy: python3 -I harness/sa3_dev_doc.py"""
import json, sys, os, math, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from score_run import cluster_bootstrap
from sa3_action_verify import score_action, classify, CANON

R = "runs/sa_spice_v3/dev"
NH = {"sftcont": "a", "sa_ck500": "a", "sa_ck400": "b", "chrf_ck400": "b", "match_ck400": "match", "match_ck500": "match"}  # match thêm 16/11
def raw(n):
    return {(r["episode_id"], r["step_id"]): r for r in map(json.loads, open(f"{R}/{NH[n]}/score/score_dev_{n}_raw.jsonl"))}
def preds(n):
    return {(r["episode_id"], r["step_id"]): r for r in map(json.loads, open(f"{R}/{NH[n]}/dev_{n}.jsonl"))}
key = lambda u: u["app"] or f"ep{u['episode_id']}"
S = {n: raw(n) for n in NH}; P = {n: preds(n) for n in NH}
ks = sorted(S["sftcont"]); assert all(sorted(S[n]) == ks for n in NH)
out = {"exec": {}, "pairs": {}, "nontap": {}}
for n in NH:
    pt, ci, g, _ = cluster_bootstrap(list(S[n].values()), key, lambda u: u["executable"])
    out["exec"][n] = [round(100*pt, 2), round(100*ci[0], 2), round(100*ci[1], 2)]
    print(f"exec {n:11s} {100*pt:6.2f} [{100*ci[0]:.2f}; {100*ci[1]:.2f}]  n={len(ks)} cụm={g}")
def mcn(b, c):
    # McNemar chính xác hai phía
    m = b + c; k = min(b, c)
    p = sum(math.comb(m, i) for i in range(k+1)) / 2**m * 2 if m else 1.0
    return min(1.0, p)
for x, y in [("sa_ck500", "sftcont"), ("sa_ck400", "sftcont"), ("chrf_ck400", "sftcont"), ("sa_ck400", "chrf_ck400"), ("sa_ck500", "sa_ck400"),
             ("match_ck400", "sftcont"), ("match_ck500", "sftcont"), ("sa_ck400", "match_ck400"), ("sa_ck500", "match_ck500"), ("match_ck500", "match_ck400")]:
    D = [{"app": S[x][k]["app"], "episode_id": k[0], "d": S[x][k]["executable"] - S[y][k]["executable"]} for k in ks]
    pt, ci, _, _ = cluster_bootstrap(D, key, lambda u: u["d"])
    b = sum(u["d"] == 1 for u in D); c = sum(u["d"] == -1 for u in D)
    p = mcn(b, c)
    out["pairs"][f"{x}-{y}"] = dict(d=round(100*pt, 2), ci=[round(100*ci[0], 2), round(100*ci[1], 2)], cuu=b, pha=c, p=round(p, 4))
    print(f"Δexec {x}−{y}: {100*pt:+.2f} [{100*ci[0]:+.2f}; {100*ci[1]:+.2f}] cứu {b} phá {c} p={p:.3f}")
# bước không chạm: verifier v3 (A ∈ {0, .5, 1}) + đúng loại thao tác theo classify, chỉ bước gold trusted
tapk = set(ks)
nk = sorted(k for k in P["sftcont"] if k not in tapk)
print(f"bước không chạm: {len(nk)} (tổng {len(P['sftcont'])})")
for n in NH:
    rows = [P[n][k] for k in nk]
    A = [score_action(r["pred"], r["gold"], r["action_type"])[0] for r in rows]
    tr = [r for r in rows if score_action(r["gold"], r["gold"], r["action_type"])[1] != "untrusted"]
    ok = sum(classify(r["pred"]) == CANON[r["action_type"]] for r in tr)
    em = sum(r["pred"].strip() == r["gold"].strip() for r in P[n].values())
    out["nontap"][n] = dict(A_tb=round(sum(A)/len(A), 4), dung_loai=ok, n_trusted=len(tr), trung_gold=em)
    print(f"{n:11s} A TB {sum(A)/len(A):.4f} · đúng loại {ok}/{len(tr)} ({100*ok/len(tr):.2f}%) · câu trùng gold {em}/{len(P[n])}")
    for at in sorted({r['action_type'] for r in tr}):
        t = [r for r in tr if r["action_type"] == at]
        print(f"   {at:10s} {sum(classify(r['pred']) == CANON[at] for r in t)}/{len(t)}")
for x, y in [("sa_ck500", "sftcont"), ("sa_ck400", "sftcont"), ("chrf_ck400", "sftcont"), ("match_ck400", "sftcont"), ("match_ck500", "sftcont"), ("sa_ck400", "match_ck400")]:
    D = []
    for k in nk:
        r = P[x][k]
        if score_action(r["gold"], r["gold"], r["action_type"])[1] == "untrusted": continue
        D.append({"app": r.get("package", ""), "episode_id": k[0], "d": int(classify(r["pred"]) == CANON[r["action_type"]]) - int(classify(P[y][k]["pred"]) == CANON[r["action_type"]])})
    pt, ci, _, _ = cluster_bootstrap(D, key, lambda u: u["d"])
    b = sum(u["d"] == 1 for u in D); c = sum(u["d"] == -1 for u in D)
    out["pairs"][f"nontap_{x}-{y}"] = dict(d=round(100*pt, 2), ci=[round(100*ci[0], 2), round(100*ci[1], 2)], cuu=b, pha=c, p=round(mcn(b, c), 4))
    print(f"Δđúng loại không chạm {x}−{y}: {100*pt:+.2f} [{100*ci[0]:+.2f}; {100*ci[1]:+.2f}] cứu {b} phá {c} p={mcn(b,c):.3f}")
json.dump(out, open(f"{R}/doc_dev.json", "w"), ensure_ascii=False, indent=1)
