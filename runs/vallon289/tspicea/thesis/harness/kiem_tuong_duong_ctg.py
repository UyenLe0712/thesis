"""Kiểm (CPU, ~1 phút): đổi micro-batch (bs×accum=16) và tắt gradient checkpointing KHÔNG đổi kết quả train CTG-GRPO.
Mô hình tí hon, CPU fp32, SGD (Adam che khác biệt gradient), 2 bước cập nhật, so trọng số LoRA sau train.
Chạy: PYTHONPATH=<thư mục có trl 0.29.1> ~/.venvs/thesis/bin/python harness/kiem_tuong_duong_ctg.py
Kết quả 4/10: bs8×2, bs16×1 lệch 6e-9 (làm tròn) · tắt gradient checkpointing lệch 0 · A2 (tắt CTG) lệch 4,5e-3."""
import os, sys, json, shutil, hashlib
sys.path.insert(0, "/mnt/d/Master/Thesis/harness")
import torch, transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from trl import GRPOConfig
from datasets import Dataset
import ctg_grpo as C

M = "trl-internal-testing/tiny-Qwen2ForCausalLM-2.5"
GOLD = {"Swipe up to see more": "scroll", "Type hello in the box": "type"}
def lop_gia(s):            # vàng theo bảng; câu sinh (chữ ngẫu nhiên) chia đôi theo tổng mã ký tự ⇒ std(c) > 0
    return GOLD.get(s) or ("scroll" if sum(map(ord, s)) % 2 else "tap")
C.lop = lop_gia
C.CID["m"] = C.CiderD(list(GOLD) + ["Click on the search bar", "Open the Clock app"])
def r_len(completions, gold, **kw):   # thưởng tất định, khác nhau giữa các câu
    return [len(C._text(c)) % 7 / 7.0 for c in completions]

rows = [dict(key=f"k{i}", prompt=[{"role": "user", "content": p}], gold=g, action_type="")
        for i, (p, g) in enumerate([("Describe step A", "Swipe up to see more"), ("Describe step B", "Type hello in the box"),
                                     ("Describe step C", "Swipe up to see more"), ("Describe step D", "Type hello in the box")])]

def chay(ten, bs, acc, gc, arm="A3"):
    out = f"/tmp/claude-1000/kt_{ten}"; shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    transformers.set_seed(101)
    tok = AutoTokenizer.from_pretrained(M); tok.padding_side = "left"
    m = AutoModelForCausalLM.from_pretrained(M, dtype=torch.float32)
    m = get_peft_model(m, LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0, target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM"))
    args = GRPOConfig(output_dir=out, seed=101, num_generations=8, per_device_train_batch_size=bs,
                      gradient_accumulation_steps=acc, steps_per_generation=acc, max_completion_length=12,
                      temperature=1.0, top_p=1.0, top_k=0, beta=0.04, learning_rate=1.0, max_steps=2, optim="sgd", max_grad_norm=1e9,
                      gradient_checkpointing=gc, gradient_checkpointing_kwargs={"use_reentrant": False},
                      scale_rewards="group", loss_type="dapo", num_iterations=1, logging_steps=1, save_steps=10**6,
                      report_to="none", remove_unused_columns=False, use_cpu=True, bf16=False, fp16=False,
                      lr_scheduler_type="constant", disable_tqdm=True)
    assert args.generation_batch_size == 16
    T = C.lam_ctg_trainer(arm, out)
    tr = T(model=m, reward_funcs=[r_len], args=args, train_dataset=Dataset.from_list(rows), processing_class=tok)
    tr.train()
    sd = {k: v.detach().clone() for k, v in tr.model.named_parameters() if "lora" in k}
    log = [json.loads(l) for l in open(f"{out}/ctg_log.jsonl")]
    return sd, log, tr.ctg.lam

kq = {}
for ten, bs, acc, gc, arm in [("bs4_acc4_gc", 4, 4, True, "A3"), ("bs8_acc2_gc", 8, 2, True, "A3"),
                              ("bs16_acc1_gc", 16, 1, True, "A3"), ("bs4_acc4_nogc", 4, 4, False, "A3"),
                              ("bs4_acc4_gc_A2", 4, 4, True, "A2")]:
    kq[ten] = chay(ten, bs, acc, gc, arm)
    print(ten, "· nhóm CTG có std>0:", sum(r.get("std_pos", False) for r in kq[ten][1]), "· λ", kq[ten][2], flush=True)

goc = kq["bs4_acc4_gc"][0]
def lech(a, b): return max((a[k] - b[k]).abs().max().item() for k in a)
def doi(a): return max((a[k]).abs().max().item() for k in a if "lora_B" in k)
print("\n|lora_B| sau train (mốc):", f"{doi(goc):.3e}")
for ten in kq:
    if ten != "bs4_acc4_gc":
        print(f"{ten:16} lệch tối đa so với mốc: {lech(kq[ten][0], goc):.3e}")
print("ctg_log trùng nhau (A3 các cấu hình):",
      all([ (r['key'], r.get('day_sau')) for r in kq[t][1]] == [(r['key'], r.get('day_sau')) for r in kq['bs4_acc4_gc'][1]]
          for t in ("bs8_acc2_gc", "bs16_acc1_gc", "bs4_acc4_nogc")))
