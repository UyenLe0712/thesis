# -*- coding: utf-8 -*-
"""Tiến trình train GIẢ in log giống grpo_luoi.py: [tiếp từ], [nạp default], dòng {'loss': ...}, điểm lưu mỗi SAVE bước
(ghi adapter + trainer_state trước, optimizer.pt sau cùng như Trainer), [xong] với s/bước + đỉnh VRAM.
Cờ: --train|--probe --out O --max-steps N --resume auto [--hong-nap] [--ngu S]. Mọi cờ khác bị bỏ qua."""
import os, sys, glob, json, time, argparse
ap = argparse.ArgumentParser()
ap.add_argument("--out"); ap.add_argument("--max-steps", type=int, default=500); ap.add_argument("--resume")
ap.add_argument("--probe", action="store_true"); ap.add_argument("--train", action="store_true")
ap.add_argument("--hong-nap", action="store_true"); ap.add_argument("--ngu", type=float, default=0.3)
ap.add_argument("--save", type=int, default=5)
ap.add_argument("--ppo", action="store_true")   # ghi value_head.pt SAU ba tệp chính, như grpo_ppo.py
a, _ = ap.parse_known_args()
N = 20 if a.probe else a.max_steps
os.makedirs(a.out, exist_ok=True)
print("[main] nạp mô hình giả", flush=True); time.sleep(1)
ck = sorted((p for p in glob.glob(f"{a.out}/checkpoint-*") if all(os.path.exists(f"{p}/{f}") for f in
            ("trainer_state.json", "optimizer.pt", "adapter_model.safetensors"))), key=lambda p: int(p.rsplit("-", 1)[1]))
r = ck[-1] if ck else None
print("[tiếp từ]", r, flush=True)
g = int(r.rsplit("-", 1)[1]) if r else 0
if r:
    print(f"[nạp default] 504 tensor · |lora_B| 0.0000 → {0.0 if a.hong_nap else 5.7831:.4f} · khoá lạ 0", flush=True)
    if a.ppo:
        assert os.path.exists(f"{r}/value_head.pt"), f"DỪNG: điểm lưu thiếu đầu giá trị {r}/value_head.pt"
        print(f"[đầu giá trị] nạp từ {r}/value_head.pt", flush=True)
    if a.hong_nap:
        time.sleep(30)   # bản thật assert ⇒ ở đây để xem theo_doi có tự dừng không
t0 = time.time()
for s in range(g + 1, N + 1):
    time.sleep(a.ngu)
    print({"loss": "0.001", "grad_norm": "0.5", "reward": f"{0.4 + 0.001 * s:.4f}", "kl": "0.004", "step_time": f"{a.ngu:.3f}"}, flush=True)
    if not a.probe and s % a.save == 0:
        d = f"{a.out}/checkpoint-{s}"; os.makedirs(d, exist_ok=True)
        open(f"{d}/adapter_model.safetensors", "wb").write(os.urandom(2000))
        json.dump({"global_step": s}, open(f"{d}/trainer_state.json", "w"))
        time.sleep(0.05)
        open(f"{d}/optimizer.pt", "wb").write(os.urandom(4000))
        if a.ppo:
            time.sleep(0.6)      # cửa sổ: ba tệp chính đã đủ mà value_head.pt chưa có
            open(f"{d}/value_head.pt", "wb").write(os.urandom(1000))
el = time.time() - t0
b = max(N - g, 1)
print(f"[xong] {b} bước · {el/60:.1f} phút · {el/b:.1f} s/bước · đỉnh VRAM 14.20 GiB · thưởng 0.1 s/lần", flush=True)
