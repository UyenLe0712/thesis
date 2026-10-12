# G3b (uyenle, 12/10/2026): G2 treo >16 h ⇒ gộp việc còn lại vào một commit:
# hoà S1 → kiểm 20 câu ck500 → kiểm 2 GPU → sinh test shard 4,5,6/10 (nửa k/20 + (k+10)/20) → gộp với
# G1 (cw-ra-g1-out: val + test 0-3) và G2b (cw-ra-g2b-out: test 7-9) → ô C2-3…C2-7 gốc.
import json, copy, os
K = os.path.dirname(os.path.abspath(__file__))
exec(open(f"{K}/dung_nb_chia.py").read().split("V1 = ")[0])
C = nb["cells"]
GPU = r'''# Ô kiểm phần cứng: G2 trên tài khoản này treo không rõ lý do ⇒ đòi đủ 2 GPU trước khi sinh
import torch
print(torch.cuda.device_count(), [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())], flush=True)
assert torch.cuda.device_count() == 2, "⛔ không đủ 2 GPU — dừng"
'''
V = {0: [("test", 4, 20), ("test", 14, 20), ("test", 5, 20)], 1: [("test", 15, 20), ("test", 6, 20), ("test", 16, 20)]}
NOI = r'''# Ô nối nửa shard → cw_test_s{k}of10 trong /kaggle/working
for k in (4, 5, 6):
    L = [l for f in (f"{W}/cw_test_s{k}of20.jsonl", f"{W}/cw_test_s{k+10}of20.jsonl") for l in open(f)]
    assert len(L) == len({(json.loads(l)["episode_id"], json.loads(l)["step_id"]) for l in L}) == 446, (k, len(L))
    open(f"{W}/cw_test_s{k}of10.jsonl", "w").writelines(L); print(k, len(L), flush=True)
'''
GOM = r'''# Ô gộp shard: val + test 0-3 (G1), 4-6 (sinh ở trên), 7-9 (G2b)
for ten, n, sn in (("val", 1002, 2), ("test", 4463, 10)):
    S = {}
    for k in range(sn):
        g = sorted(set(glob.glob(f"/kaggle/input/**/cw_{ten}_s{k}of{sn}.jsonl", recursive=True)
                       + glob.glob(f"{W}/cw_{ten}_s{k}of{sn}.jsonl")))
        assert len(g) == 1, f"⛔ shard {ten} {k}/{sn}: {g}"
        S[k] = [json.loads(l) for l in open(g[0])]
        print(ten, k, len(S[k]), g[0])
    rows = [r for k in range(sn) for r in S[k]]
    keys = {(r["episode_id"], r["step_id"]) for r in rows}
    assert len(rows) == len(keys) == n, (ten, len(rows), len(keys))
    with open(f"{W}/cw_{ten}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[gộp] {ten}: {len(rows)} dòng", flush=True)
'''
nb["cells"] = copy.deepcopy(C[:5]) + [o(KIEM), o(GPU), o(SINH.replace("__VIEC__", repr(V))), o(NOI), o(GOM)] + copy.deepcopy(C[6:])
d = f"{K}/nb_cw-ra-g3b-309"; os.makedirs(d, exist_ok=True)
json.dump(nb, open(f"{d}/cw-ra-g3b-309.ipynb", "w"), ensure_ascii=False, indent=1)
json.dump({"id": "uyenle0712/cw-ra-g3b-309", "title": "cw-ra-g3b-309", "code_file": "cw-ra-g3b-309.ipynb",
           "language": "python", "kernel_type": "notebook", "is_private": True, "enable_gpu": True, "enable_tpu": False,
           "enable_internet": True,
           "dataset_sources": ["uyenle0712/fgrb-p1-bundle", "uyenle0712/grpo-spice-ck500", "uyenle0712/cw-ra-309-u",
                               "uyenle0712/thesis-score", "uyenle0712/cw-ra-g1-out", "uyenle0712/cw-ra-g2b-out"],
           "kernel_sources": [], "competition_sources": [], "model_sources": []},
          open(f"{d}/kernel-metadata.json", "w"), indent=1)
for i, c in enumerate(nb["cells"]): print(i, "".join(c["source"])[:70].replace("\n", " | "))
