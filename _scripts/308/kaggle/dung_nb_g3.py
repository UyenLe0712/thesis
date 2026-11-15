# Dựng G3 (uyenle): gộp shard của G1 + G2 → ô C2-3…C2-7 gốc (kiểm thẻ, chốt τ trên val, chấm 7 thước, exec). 11/10/2026.
import json, copy, os
K = os.path.dirname(os.path.abspath(__file__))
nb = json.load(open(f"{K}/nb309g/cw-ra-g-309.ipynb"))
C = nb["cells"]
GOM = r'''# Ô gộp shard từ G1 (dataset cw-ra-g1-out) và G2 (output notebook cw-ra-g2-309)
for ten, n, sn in (("val", 1002, 2), ("test", 4463, 10)):
    S = {}
    for k in range(sn):
        g = sorted(set(glob.glob(f"/kaggle/input/**/cw_{ten}_s{k}of{sn}.jsonl", recursive=True)))
        assert g, f"⛔ thiếu shard {ten} {k}/{sn}"
        R = [json.loads(l) for l in open(g[0])]
        S[k] = R
        print(ten, k, len(R), g[0])
    rows = [r for k in range(sn) for r in S[k]]
    keys = {(r["episode_id"], r["step_id"]) for r in rows}
    assert len(rows) == len(keys) == n, (ten, len(rows), len(keys))
    with open(f"{W}/cw_{ten}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[gộp] {ten}: {len(rows)} dòng", flush=True)
'''
o = lambda s: {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s}
nb["cells"] = copy.deepcopy([C[0], C[1], C[3], C[4]]) + [o(GOM)] + copy.deepcopy(C[6:])
d = f"{K}/nb_cw-ra-g3-309"; os.makedirs(d, exist_ok=True)
json.dump(nb, open(f"{d}/cw-ra-g3-309.ipynb", "w"), ensure_ascii=False, indent=1)
json.dump({"id": "uyenle0712/cw-ra-g3-309", "title": "cw-ra-g3-309", "code_file": "cw-ra-g3-309.ipynb",
           "language": "python", "kernel_type": "notebook", "is_private": True, "enable_gpu": True, "enable_tpu": False,
           "enable_internet": True,
           "dataset_sources": ["uyenle0712/fgrb-p1-bundle", "uyenle0712/grpo-spice-ck500", "uyenle0712/cw-ra-309-u",
                               "uyenle0712/thesis-score", "uyenle0712/cw-ra-g1-out"],
           "kernel_sources": ["uyenle0712/cw-ra-g2-309"], "competition_sources": [], "model_sources": []},
          open(f"{d}/kernel-metadata.json", "w"), indent=1)
print(d, [c["source"][:40] for c in nb["cells"]])
