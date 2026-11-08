"""Kernel CPU kiểm nguyên nhân lượt A/A lệch ck500 từ bước 1 (8/11/2026).

Hai giả thuyết: (1) grpo_spice.py và grpo_luoi.py rút số ngẫu nhiên khác nhau trước lần sinh đầu;
(2) phiên bản thư viện khác (ck500 gốc: transformers 5.17.0 · peft 0.21.1 · torch 2.10.0; lưới: 5.20.2 · 0.21.2 · 2.11.0).
Chạy cả hai script × hai bộ thư viện trên Qwen2.5-VL tí hon (CPU), cùng cờ như ck500 (G 8, bs 4, accum 4, seed 101),
móc vào lần gọi generate đầu tiên: in md5 trạng thái RNG CPU, md5 input_ids, md5 chuỗi sinh, rồi thoát.
Mỗi cấu hình chạy hai lần để kiểm tính tất định. Giới hạn: CPU, không phải nhân CUDA của T4.

python make_rng_nb.py   # dựng k_kiem-rng-aa-cpu cho trangphngngc
"""
import os, re
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "make_cpu_nb.py"), encoding="utf-8").read()
cut = src.index("C2 = f'''")
head = src[:cut]
head = head.replace("user, name, *RUNS = sys.argv[1:]", "user, name, RUNS = 'trangphngngc', 'kiem-rng-aa-cpu', []")

WRAP_RNG = r'''"""python thu_rng.py <grpo_spice.py|grpo_luoi.py> <cờ...>"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch, trl, transformers, peft
import grpo_spice as GS
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
TINY = "trl-internal-testing/tiny-Qwen2_5_VLForConditionalGeneration"
class AnyEq(int):
    def __eq__(self, o): return True
    __hash__ = int.__hash__
def nap(a):
    return AutoProcessor.from_pretrained(TINY), Qwen2_5_VLForConditionalGeneration.from_pretrained(TINY, dtype=torch.float32), torch.float32
GS.nap = nap
GS._n_s1 = lambda p: AnyEq(0)
torch.cuda.reset_peak_memory_stats = lambda *a, **k: None   # grpo_spice.py in VRAM, CPU không có
torch.cuda.max_memory_allocated = lambda *a, **k: 0
torch.cuda.get_device_name = lambda *a, **k: "cpu"
torch.cuda.get_device_capability = lambda *a, **k: (0, 0)
_C = trl.GRPOConfig
class Cfg(_C):               # grpo_spice.py đặt fp16 = not bf, CPU không nhận fp16
    def __post_init__(self):
        self.fp16 = False; self.bf16 = False; super().__post_init__()
trl.GRPOConfig = Cfg
md5 = lambda t: hashlib.md5(t.detach().cpu().contiguous().numpy().tobytes()).hexdigest()
_g = Qwen2_5_VLForConditionalGeneration.generate
def gen(self, *a, **k):
    rs = hashlib.md5(torch.get_rng_state().numpy().tobytes()).hexdigest()
    ids = k.get("input_ids", a[0] if a else None)
    out = _g(self, *a, **k)
    seq = out.sequences if hasattr(out, "sequences") else out
    rec = dict(script=os.path.basename(sys.argv[1]), versions=[trl.__version__, transformers.__version__, peft.__version__, torch.__version__],
               rng_truoc=rs, input=md5(ids) if ids is not None else None, out=md5(seq), shape=list(seq.shape),
               duoi_chuoi_0=seq[0, -12:].tolist(), duoi_chuoi_1=seq[1, -12:].tolist() if seq.shape[0] > 1 else None)
    print("[rng]", json.dumps(rec), flush=True)
    json.dump(rec, open(os.environ["RNG_OUT"], "w"))
    os._exit(0)
Qwen2_5_VLForConditionalGeneration.generate = gen
f = sys.argv[1]; sys.argv = sys.argv[1:]
if f == "grpo_spice.py":
    GS.main()
else:
    import grpo_luoi as GL; GL.main()
print("[rng] KHÔNG gặp lần sinh nào", flush=True); sys.exit(3)
'''

C2 = f'''open(f"{{S}}/thu_rng.py", "w").write({WRAP_RNG!r})
# bộ thư viện cũ của ck500 gốc, venv riêng
r = sh(f"{{sys.executable}} -m pip install -q --no-deps --target /tmp/oldlib 'torch==2.10.0' 'torchvision==0.25.0' 'transformers==5.17.0' 'peft==0.21.1' 'trl==0.29.1' --extra-index-url https://download.pytorch.org/whl/cpu 2>&1 | tail -3")
OLD = {{**os.environ, "PYTHONPATH": "/tmp/oldlib"}}
r2 = subprocess.run([sys.executable, "-c", "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__)"], capture_output=True, text=True, env=OLD)
print("venv cu:", r2.stdout, r2.stderr[-400:], flush=True)
PY = {{"moi": sys.executable}}
if r2.returncode == 0 and r2.stdout.split()[:3] == ["0.29.1", "5.17.0", "0.21.1"] and r2.stdout.split()[3].startswith("2.10.0"): PY["cu"] = sys.executable
KQ = {{}}
for env, py in PY.items():
    for scr in ("grpo_spice.py", "grpo_luoi.py"):
        for lan in (1, 2):
            tag = f"{{env}}_{{scr[:-3]}}_{{lan}}"; o = f"{{OUT}}/{{tag}}"; shutil.rmtree(o, ignore_errors=True)
            cmd = [py, "thu_rng.py", scr, "--train", "--no-q4", "--bs", "4", "--accum", "4", "--G", "8", "--reward", "spice",
                   "--seed", "101", "--bundle", B, "--merged", "x", "--out", o, "--max-steps", "2"]
            if scr == "grpo_luoi.py": cmd += ["--algo", "grpo"]
            t = time.time()
            with open(f"{{OUT}}/{{tag}}.log", "w") as lg:
                p = subprocess.run(cmd, cwd=S, stdout=lg, stderr=subprocess.STDOUT, text=True,
                                   env={{**os.environ, "CUDA_VISIBLE_DEVICES": "", "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "RNG_OUT": f"{{OUT}}/{{tag}}.json", **({{"PYTHONPATH": "/tmp/oldlib"}} if env == "cu" else {{}})}})
            L = open(f"{{OUT}}/{{tag}}.log", errors="ignore").read()
            KQ[tag] = json.load(open(f"{{OUT}}/{{tag}}.json")) if os.path.exists(f"{{OUT}}/{{tag}}.json") else dict(loi=L[-1500:])
            print(f"{{(time.time()-T0)/60:5.1f}} ph · {{tag}} · ma {{p.returncode}} · {{round(time.time()-t)}} s", flush=True)
            print("   ", json.dumps(KQ[tag], ensure_ascii=False)[:600], flush=True)
def k(t, f): return KQ.get(t, {{}}).get(f)
TOM = {{}}
for env in PY:
    for scr in ("grpo_spice", "grpo_luoi"):
        TOM[f"tat_dinh {{env}} {{scr}}"] = k(f"{{env}}_{{scr}}_1", "out") == k(f"{{env}}_{{scr}}_2", "out") is not None
    for f in ("rng_truoc", "input", "out"):
        TOM[f"{{env}}: spice == luoi ({{f}})"] = k(f"{{env}}_grpo_spice_1", f) == k(f"{{env}}_grpo_luoi_1", f)
if "cu" in PY:
    for scr in ("grpo_spice", "grpo_luoi"):
        for f in ("rng_truoc", "input", "out"):
            TOM[f"{{scr}}: cu == moi ({{f}})"] = k(f"cu_{{scr}}_1", f) == k(f"moi_{{scr}}_1", f)
print(json.dumps(TOM, indent=1, ensure_ascii=False), flush=True)
json.dump(dict(KQ=KQ, TOM=TOM), open(f"{{OUT}}/ket_qua.json", "w"), indent=1, ensure_ascii=False)
shutil.make_archive(f"{{W}}/kiem_rng", "zip", OUT)
'''
ns = {"__file__": os.path.join(H, "make_cpu_nb.py")}
tail = src[src.index("cells = ["):]
tail = tail.replace("(C1, C2)", "(C1, C2)")
exec(head + "\nC2 = " + repr(C2) + "\n" + tail.replace('print("đã dựng", d, "·", len(RUNS), "lượt")', 'print("đã dựng", d)'), ns)
