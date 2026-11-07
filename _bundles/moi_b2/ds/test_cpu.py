# -*- coding: utf-8 -*-
"""Chạy grpo_moi_b2.main() trên CPU với mô hình tí hon: vá GS.nap (mô hình), GS.dung_hang (câu nhắc giả) và
GS.spice_batch (thưởng giả từ băm câu, để nhóm có thưởng khác nhau, không cần Java). Các thưởng khác (bcmr, cider, ...)
chạy thật. Chỉ để kiểm đường chạy.

  python test_cpu.py W <cờ của grpo_moi_b2.py>
"""
import os, sys, json, hashlib
os.environ["CUDA_VISIBLE_DEVICES"] = ""
W = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch                                              # noqa: E402
import grpo_moi_b2 as MB                                  # noqa: E402
GS = MB.GS


def nap(a):
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
    proc = AutoProcessor.from_pretrained(f"{W}/tiny_proc")
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(f"{W}/tiny", dtype=torch.float32)
    print(f"[nạp] mô hình tí hon CPU · {sum(p.numel() for p in model.parameters()):,} tham số", flush=True)
    return proc, model, torch.float32


def dung_hang(bundle, n=1000, dai_nhat=0, seed=101):
    rows = json.load(open(f"{W}/rows.json"))[:n]
    return rows, {"gia": 1}


def spice_gia(cands, refs):
    return [int(hashlib.md5((c + "|" + r).encode()).hexdigest()[:6], 16) / 0xFFFFFF for c, r in zip(cands, refs)]


GS.nap, GS.dung_hang, GS.spice_batch = nap, dung_hang, spice_gia
MB.main(sys.argv[2:])
