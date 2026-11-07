# -*- coding: utf-8 -*-
"""Dựng mô hình Qwen2.5-VL tí hon (khởi tạo ngẫu nhiên, cùng kiến trúc + processor thật), bộ dữ liệu giả và adapter S1 giả
để kiểm đường chạy của grpo_moi_b2.py trên CPU. Không dùng được để đọc số.

  python prep_tihon.py W
"""
import os, sys, json, random
import torch
from PIL import Image
from transformers import AutoConfig, AutoProcessor, Qwen2_5_VLForConditionalGeneration
from peft import LoraConfig, get_peft_model

W = sys.argv[1]
BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
torch.manual_seed(0)
cfg = AutoConfig.from_pretrained(BASE)
tc, vc = cfg.text_config, cfg.vision_config
tc.hidden_size, tc.num_hidden_layers, tc.num_attention_heads, tc.num_key_value_heads, tc.intermediate_size = 64, 2, 4, 2, 128
tc.layer_types = ["full_attention"] * 2
tc.max_window_layers = 2
rp = dict(tc.rope_parameters)
rp["mrope_section"] = [2, 3, 3]                      # head_dim 16 ⇒ tổng = 8
tc.rope_parameters = rp
vc.depth, vc.hidden_size, vc.num_heads, vc.intermediate_size, vc.out_hidden_size = 2, 32, 2, 64, 64
vc.fullatt_block_indexes = [1]
model = Qwen2_5_VLForConditionalGeneration(cfg)
model.save_pretrained(f"{W}/tiny")
print("[tí hon] tham số", sum(p.numel() for p in model.parameters()), flush=True)
proc = AutoProcessor.from_pretrained(BASE, min_pixels=3136, max_pixels=12544)
proc.save_pretrained(f"{W}/tiny_proc")

B = f"{W}/bundle"
os.makedirs(f"{B}/img", exist_ok=True)
rd = random.Random(0)
GOLD = ["Click on the search bar", "Open the Clock app", "Click on the Settings icon at the top right corner",
        "Scroll down", "Click on the play button", "Type hello in the message box", "Go back", "Click on Save"]
rows = []
for i in range(16):
    p = f"{B}/img/{i}.png"
    Image.new("RGB", (112, 112), tuple(rd.randrange(256) for _ in range(3))).save(p)
    body = f"\nGoal: test {i}. Screen text: OK | Cancel | Settings | Search. Write the next step instruction."
    rows.append(dict(key=f"{i}_0", image=p, prompt=[{"role": "system", "content": "You write one GUI instruction."},
                                                     {"role": "user", "content": body}],
                     gold=GOLD[i % len(GOLD)], action_type="click", n_char=len(body)))
json.dump(rows, open(f"{W}/rows.json", "w"))
with open(f"{B}/p1_train_rows.jsonl", "w") as f:
    for g in GOLD * 3:
        f.write(json.dumps({"target_instruction": g}) + "\n")
lc = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0, bias="none", task_type="CAUSAL_LM",
                target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "layers.0.mlp.gate_proj", "layers.1.mlp.up_proj",
                                "layers.1.mlp.down_proj"])
pm = get_peft_model(Qwen2_5_VLForConditionalGeneration.from_pretrained(f"{W}/tiny", dtype=torch.float32), lc)
assert not [n for n, p in pm.named_parameters() if p.requires_grad and "visual" in n], "LoRA giả chạm tháp thị giác"
pm.save_pretrained(f"{B}/adapter_s1_seed101")
print("[xong] tí hon + bộ giả ở", W, flush=True)
