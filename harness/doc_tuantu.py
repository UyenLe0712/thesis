# -*- coding: utf-8 -*-
"""Đọc kết quả việc #5 (report/322): sinh câu tuần tự, lịch sử là câu mô hình tự sinh — 0 giây GPU.

    ~/.venvs/thesis/bin/python harness/doc_tuantu.py      # ghi runs/tuantu/ket_qua_tuantu.json

Nguồn:
  runs/tuantu/out/pred_{s1,ck500}_tuantu.jsonl        câu sinh tuần tự (kernel tuantu-lichsu-tusinh)
  runs/tuantu/cham/out/score_moi_{s1,ck500}_raw.jsonl điểm UGround của các câu chạm khác lượt cũ (kernel tuantu-cham)
  runs/score_s1_seed101_raw.jsonl · runs/grpo_spice/score_ck500_test_raw.jsonl   lượt cũ (lịch sử = câu chuẩn)
Câu chạm giống hệt lượt cũ dùng lại điểm cũ (thước tất định). Bootstrap = `score_run.cluster_bootstrap`, cụm như d3_ktc.
"""
import json, os, collections
import score_run as S
import metric_exec as M

H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, "..", "runs")
TAPT = ("click", "long_press")
key = lambda d: (d["episode_id"], d["step_id"])
JL = lambda p: [json.loads(l) for l in open(p, encoding="utf-8")]
CU = {"s1": "score_s1_seed101_raw.jsonl", "ck500": "grpo_spice/score_ck500_test_raw.jsonl"}


def main():
    recs = JL(os.path.join(H, "dg1_cache", "test_ac", "test.jsonl"))
    rec = {key(r): r for r in recs}
    tap = [key(r) for r in recs if r["action"].get("action_type") in TAPT and "x" in r["action"]]
    assert len(tap) == 4463
    co = collections.defaultdict(set)
    for r in recs:
        co[r["episode_id"]].add(r["step_id"])
    du = {e for e, v in co.items() if v == set(range(max(v) + 1))}       # tác vụ đủ ảnh
    tap_du = [k for k in tap if k[0] in du]

    E, cum = {}, {}
    for nh in ("s1", "ck500"):
        cu = {key(d): d for d in JL(os.path.join(R, CU[nh]))}
        P = {key(d): d for d in JL(os.path.join(R, "tuantu", "out", f"pred_{nh}_tuantu.jsonl"))}
        moi = {key(d): d for d in JL(os.path.join(R, "tuantu", "cham", "out", f"score_moi_{nh}_raw.jsonl"))}
        assert len(P) == 6958
        tf, tu = {}, {}
        for k in tap:
            tf[k] = int(cu[k].get("executable", 0))
            p = P[k]["pred"]
            if p == cu[k].get("sent"):
                tu[k] = tf[k]
            else:
                assert k in moi and moi[k].get("sent", p) == p, f"⛔ thiếu điểm câu mới {nh} {k}"
                tu[k] = int(moi[k].get("executable", 0))
            cum[k] = cu[k].get("app") or f"ep{k[0]}"
        nontap = [k for k in rec if k not in set(tap)]
        tl = lambda k: int(bool(P[k]["pred"]) and M.canon_action(P[k]["pred"], strict_back=True)
                           == M.canon_action(rec[k]["gold_instruction"], strict_back=True))
        E[nh] = dict(tf=tf, tu=tu, doi=sum(P[k]["pred"] != cu[k].get("sent") for k in tap),
                     nontap_tu=100 * sum(tl(k) for k in nontap) / len(nontap),
                     n_chuan=sum(P[k].get("n_chuan", 0) > 0 for k in tap))

    def ktc(K, f):
        pt, (lo, hi), G, _ = S.cluster_bootstrap([(k, f(k)) for k in K], lambda u: cum[u[0]], lambda u: u[1],
                                                 B=10000, seed=S.SEED)
        return [round(100 * pt, 2), round(100 * lo, 2), round(100 * hi, 2)]

    def tac_vu(d):
        ep = collections.defaultdict(list)
        for k in tap_du:
            ep[k[0]].append(d[k])
        return round(100 * sum(all(v) for v in ep.values()) / len(ep), 2), len(ep)

    out = {"n_tap": len(tap), "n_tap_du": len(tap_du), "n_tac_vu_du": len(du)}
    for nh in ("s1", "ck500"):
        e = E[nh]
        out[nh] = {
            "cau_cham_doi": e["doi"], "buoc_cham_co_cau_chuan_thay": e["n_chuan"],
            "exec_chuan": ktc(tap, lambda k: e["tf"][k]), "exec_tusinh": ktc(tap, lambda k: e["tu"][k]),
            "tusinh_tru_chuan": ktc(tap, lambda k: e["tu"][k] - e["tf"][k]),
            "du_exec_chuan": ktc(tap_du, lambda k: e["tf"][k]), "du_exec_tusinh": ktc(tap_du, lambda k: e["tu"][k]),
            "du_tusinh_tru_chuan": ktc(tap_du, lambda k: e["tu"][k] - e["tf"][k]),
            "tac_vu_chuan": tac_vu(e["tf"]), "tac_vu_tusinh": tac_vu(e["tu"]),
            "nontap_thao_tac_tusinh": round(e["nontap_tu"], 2),
        }
    a, b = E["ck500"], E["s1"]
    out["ck500_tru_s1_chuan"] = ktc(tap, lambda k: a["tf"][k] - b["tf"][k])
    out["ck500_tru_s1_tusinh"] = ktc(tap, lambda k: a["tu"][k] - b["tu"][k])
    out["du_ck500_tru_s1_tusinh"] = ktc(tap_du, lambda k: a["tu"][k] - b["tu"][k])
    print(json.dumps(out, ensure_ascii=False, indent=1))
    json.dump(out, open(os.path.join(R, "tuantu", "ket_qua_tuantu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
