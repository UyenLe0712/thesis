# Dựng G1 (trang: val + test shard 0-3/10) và G2 (uyenle: kiểm 20 bước + test shard 4-9/10)
# từ notebook cw-ra-g-309 (giữ ô 0-4), thay ô sinh bằng ô chia shard. 11/10/2026.
import json, copy, os
K = os.path.dirname(os.path.abspath(__file__))
nb = json.load(open(f"{K}/nb309g/cw-ra-g-309.ipynb"))
GOC = nb["cells"][:5]

def o(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}

SINH = r'''# Ô sinh chia shard: mỗi GPU chạy tuần tự các việc của nó; nối tiếp được (cw_gen bỏ qua dòng đã có)
VIEC = __VIEC__
def lenh(v):
    ten, k, n = v
    if ten == "val":
        a = [f"{BUNDLE}/p1_val_rows.jsonl", f"{BUNDLE}/ocr.jsonl", f"{BUNDLE}/images", f"{SRC}/ex_val_k4.jsonl", "1002"]
    else:
        a = [f"{TEST}/test.jsonl", f"{TEST}/ocr.jsonl", f"{TEST}/images", f"{SRC}/ex_test_k4.jsonl", "4463"]
    return ["python", f"{RA}/cw_gen.py", "--mode", "cw", "--merged", M, "--ckpt", CWA, "--recs", a[0], "--ocr", a[1],
            "--images", a[2], "--ra", a[3], "--chi-cham", "--expect", a[4],
            "--out", f"{W}/cw_{ten}_s{k}of{n}.jsonl", "--shard", f"{k}/{n}"]
import shlex
ps, logs = [], []
for g in (0, 1):
    cmd = " && ".join(" ".join(map(shlex.quote, lenh(v))) for v in VIEC[g])
    log = f"{W}/sinh_gpu{g}.log"; logs.append(log)
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(g), PYTHONUNBUFFERED="1")
    ps.append(subprocess.Popen(cmd, shell=True, stdout=open(log, "w"), stderr=subprocess.STDOUT,
                               env=env, cwd=RA, start_new_session=True))
    time.sleep(60)
doi(ps, logs)
for g in (0, 1):
    for ten, k, n in VIEC[g]:
        f = f"{W}/cw_{ten}_s{k}of{n}.jsonl"
        print(f, sum(1 for _ in open(f)), flush=True)
'''

DONG = r'''# Ô đóng gói: xoá thứ nặng, zip riêng kết quả
for d in ("s1_merged", "ra"):
    shutil.rmtree(f"{W}/{d}", ignore_errors=True)
import zipfile
with zipfile.ZipFile(f"/tmp/__TEN__.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(W)):
        if f.startswith(("cw_", "sinh_", "kiem20")) and f.endswith((".jsonl", ".log")):
            z.write(f"{W}/{f}", f)
shutil.move("/tmp/__TEN__.zip", f"{W}/__TEN__.zip")
print(sorted(os.listdir(W)), f"{(time.time()-T0)/3600:.2f} h")
'''

KIEM = r'''# Ô kiểm đường sinh trên tài khoản này: 20 bước val chế độ tu phải trùng câu ck500 (~3 phút)
p = chay("cw_gen.py", ["--mode", "tu", "--merged", M, "--ckpt", CK500, "--recs", f"{BUNDLE}/p1_val_rows.jsonl",
                       "--ocr", f"{BUNDLE}/ocr.jsonl", "--images", f"{BUNDLE}/images", "--chi-cham", "--n", "20",
                       "--out", f"{W}/kiem20.jsonl"], f"{W}/kiem20.log", 0)
doi([p], [f"{W}/kiem20.log"])
A = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{W}/kiem20.jsonl"))}
B = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{SRC}/pred_ck500_vallon.jsonl"))}
trung = sum(A[k] == B[k] for k in A)
print(f"[kiểm ck500] {trung}/{len(A)}")
assert trung >= 18, "⛔ đường sinh lệch ck500 — dừng"
'''

def dung(ten, viec, kiem, meta):
    n2 = copy.deepcopy(nb)
    cells = copy.deepcopy(GOC) + ([o(KIEM)] if kiem else []) + [o(SINH.replace("__VIEC__", repr(viec))), o(DONG.replace("__TEN__", f"ket_qua_{ten}"))]
    n2["cells"] = cells
    d = f"{K}/nb_{ten}"; os.makedirs(d, exist_ok=True)
    json.dump(n2, open(f"{d}/{ten}.ipynb", "w"), ensure_ascii=False, indent=1)
    meta = dict(meta, id=meta["id"], title=ten, code_file=f"{ten}.ipynb", language="python", kernel_type="notebook",
                is_private=True, enable_gpu=True, enable_tpu=False, enable_internet=True, competition_sources=[], model_sources=[])
    json.dump(meta, open(f"{d}/kernel-metadata.json", "w"), indent=1)
    print(d)

V1 = {0: [("val", 0, 2), ("test", 0, 10), ("test", 1, 10)], 1: [("val", 1, 2), ("test", 2, 10), ("test", 3, 10)]}
V2 = {0: [("test", 4, 10), ("test", 5, 10), ("test", 6, 10)], 1: [("test", 7, 10), ("test", 8, 10), ("test", 9, 10)]}
dung("cw-ra-g1-309", V1, False, {"id": "trangphngngc/cw-ra-g1-309",
     "dataset_sources": ["trangphngngc/fgrb-p1-bundle", "trangphngngc/grpo-spice-ck500", "trangphngngc/ra-sft-script",
                         "trangphngngc/cw-ra-309", "trangphngngc/thesis-score"],
     "kernel_sources": ["trangphngngc/cw-ra-t-309"]})
dung("cw-ra-g2-309", V2, True, {"id": "uyenle0712/cw-ra-g2-309",
     "dataset_sources": ["uyenle0712/fgrb-p1-bundle", "uyenle0712/grpo-spice-ck500", "uyenle0712/cw-ra-309-u",
                         "uyenle0712/thesis-score"], "kernel_sources": []})
