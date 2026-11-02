"""SFT tiếp từ S1 (report/329 đợt 1, Behavior Cloning): mốc "chỉ là học thêm" cho ck500.

Giữ như ck500: S1 hoà + LoRA mới cùng cỡ, đúng 1.000 câu nhắc, 500 bước tối ưu, mỗi bước 2 câu nhắc, lr 1e-5, warmup 10 bước rồi
hằng số, cắt gradient 1,0, AdamW không weight decay. Khác duy nhất: đích là câu chuẩn với cross-entropy, không lấy mẫu, không thưởng,
không KL. Thứ tự câu nhắc xáo theo hạt giống nên có thể khác thứ tự của sampler TRL.

  python sft_tiep.py --train --bundle B --merged M --out O --resume auto --keys-ck500 prompt_keys_ck500.json
  python sft_tiep.py --probe ...      # 20 bước trên 50 câu nhắc dài nhất, in đỉnh VRAM
Log cùng dạng lưới ({'loss': ...} mỗi bước, [tiếp từ], [xong]) để notebook đọc chung một cách.
"""
import os, sys, json, glob, time, random, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_spice as GS                                   # noqa: E402


def train(a):
    import torch
    from PIL import Image
    from peft import LoraConfig, get_peft_model, set_peft_model_state_dict
    from safetensors.torch import load_file
    from transformers import get_constant_schedule_with_warmup

    torch.manual_seed(a.seed)
    rows, bo = GS.dung_hang(a.bundle, n=a.n_prompt, dai_nhat=(50 if a.probe else 0), seed=a.seed)
    print(f"[câu nhắc] {len(rows)} · bỏ {bo}", flush=True)
    os.makedirs(a.out, exist_ok=True)
    keys = [r["key"] for r in rows]
    json.dump(keys, open(os.path.join(a.out, "prompt_keys.json"), "w"))
    if a.keys_ck500:
        assert keys == json.load(open(a.keys_ck500)), "⛔ tập câu nhắc khác ck500"
        print("[câu nhắc] trùng thứ tự với ck500 ✓", flush=True)

    tong = 20 if a.probe else a.max_steps
    can = tong * a.moi_buoc
    order = []
    rd = random.Random(a.seed)
    while len(order) < can:
        p = list(range(len(rows)))
        rd.shuffle(p)
        order += p
    order = order[:can]
    if not a.probe:
        assert len(set(order)) == len(rows) and can == len(rows), f"⛔ không dùng đúng một lượt {len(rows)} câu nhắc: {can}"

    proc, model, dt = GS.nap(a)
    gpu = torch.cuda.is_available()
    model.config.use_cache = False
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    s1 = json.load(open(os.path.join(a.adapter, "adapter_config.json"), encoding="utf-8"))
    model = get_peft_model(model, LoraConfig(r=s1["r"], lora_alpha=s1["lora_alpha"], lora_dropout=0.0, bias="none",
                                             target_modules=s1["target_modules"], task_type="CAUSAL_LM"))
    params, ntr = [], 0
    for n, p in model.named_parameters():
        if p.requires_grad:
            if "visual" in n:
                raise SystemExit(f"⛔ tháp thị giác đang học: {n}")
            if p.dtype != torch.float32:
                p.data = p.data.float()
            params.append(p)
            ntr += p.numel()
    ns1 = GS._n_s1(a.adapter)
    print(f"[LoRA mới] tham số học {ntr:,} · S1 có {ns1:,}", flush=True)
    assert ntr == ns1, "⛔ LoRA mới không cùng cỡ S1"

    opt = torch.optim.AdamW(params, lr=a.lr, weight_decay=0.0)
    sched = get_constant_schedule_with_warmup(opt, 10)
    scaler = torch.amp.GradScaler("cuda", enabled=gpu and dt == torch.float16)
    tok_end = proc.tokenizer("<|im_end|>", add_special_tokens=False).input_ids

    def mau(r):
        msg = [r["prompt"][0], {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": r["prompt"][1]["content"]}]}]
        ptext = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(r["image"]).convert("RGB")
        inp = proc(text=[ptext + r["gold"] + "<|im_end|>"], images=[img], return_tensors="pt")
        pid = proc(text=[ptext], images=[img], return_tensors="pt")["input_ids"][0].tolist()
        ids = inp["input_ids"][0].tolist()
        assert ids[:len(pid)] == pid, "⛔ token câu nhắc đổi khi nối câu đích"
        n_lab = len(ids) - len(pid)
        lab = inp["input_ids"].clone()
        lab[:, :-n_lab] = -100
        inp = {k: v.to(model.device) for k, v in inp.items()}
        if "pixel_values" in inp:
            inp["pixel_values"] = inp["pixel_values"].to(dt)
        return inp, lab.to(model.device), n_lab

    inp0, _, n0 = mau(rows[order[0]])
    nhan = proc.tokenizer.decode(inp0["input_ids"][0][-n0:])
    print(f"[kiểm nhãn] tính loss {n0} token: {nhan!r} · đích {rows[order[0]]['gold']!r}", flush=True)
    assert nhan.replace("<|im_end|>", "").strip() == rows[order[0]]["gold"].strip() or not gpu, "⛔ nhãn không đúng câu đích"

    step = 0
    ck = sorted((p for p in glob.glob(os.path.join(a.out, "checkpoint-*"))
                 if all(os.path.exists(os.path.join(p, f)) for f in ("state.pt", "adapter_model.safetensors"))),
                key=lambda p: int(p.rsplit("-", 1)[1]))
    assert ck or not glob.glob(os.path.join(a.out, "checkpoint-*")), "DỪNG: có điểm lưu mà không cái nào đủ tệp"
    if a.resume and ck:
        sd = load_file(os.path.join(ck[-1], "adapter_model.safetensors"))
        kq = set_peft_model_state_dict(model, sd, adapter_name="default")
        assert not [k for k in getattr(kq, "unexpected_keys", []) if "lora" in k], "DỪNG: khoá lạ khi nạp điểm lưu"
        S = torch.load(os.path.join(ck[-1], "state.pt"), map_location="cpu", weights_only=False)
        opt.load_state_dict(S["opt"])
        sched.load_state_dict(S["sched"])
        if scaler.is_enabled() and S.get("scaler"):
            scaler.load_state_dict(S["scaler"])
        step = S["step"]
        nb = sum(p.float().norm().item() for n, p in model.named_parameters() if "lora_B" in n)
        print(f"[nạp default] {len(sd)} tensor · |lora_B| {nb:.4f}", flush=True)
        assert nb > 0, "DỪNG: không nạp được adapter từ điểm lưu"
    print("[tiếp từ]", ck[-1] if (a.resume and ck) else None, flush=True)

    def luu(path):
        model.save_pretrained(path)
        torch.save(dict(opt=opt.state_dict(), sched=sched.state_dict(), scaler=scaler.state_dict() if scaler.is_enabled() else None,
                        step=step), os.path.join(path, "state.pt"))

    if gpu:
        torch.cuda.reset_peak_memory_stats()
    model.train()
    b0, t0 = step, time.time()
    while step < tong:
        t1, tl = time.time(), 0.0
        for j in range(a.moi_buoc):
            inp, lab, _ = mau(rows[order[step * a.moi_buoc + j]])
            with torch.autocast("cuda", dtype=dt, enabled=gpu):
                loss = model(**inp, labels=lab).loss
            if not torch.isfinite(loss):
                raise SystemExit(f"⛔ loss không hữu hạn ở bước {step}, mẫu {j}")
            scaler.scale(loss / a.moi_buoc).backward()
            tl += loss.item() / a.moi_buoc
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(params, 1.0).item()
        scaler.step(opt)
        scaler.update()
        opt.zero_grad(set_to_none=True)
        sched.step()
        step += 1
        print({"loss": round(tl, 4), "grad_norm": round(gn, 4), "learning_rate": sched.get_last_lr()[0],
               "step_time": round(time.time() - t1, 2), "step": step}, flush=True)
        if step % a.save_every == 0 and step < tong and not a.probe:
            luu(os.path.join(a.out, f"checkpoint-{step}"))
    el = time.time() - t0
    print(f"[xong] {step - b0} bước · {el/60:.1f} phút · {el/max(step-b0,1):.1f} s/bước · "
          f"đỉnh VRAM {(torch.cuda.max_memory_allocated()/2**30 if gpu else 0):.2f} GiB", flush=True)
    luu(os.path.join(a.out, "final"))


def main():
    ap = argparse.ArgumentParser()
    for f in ("--probe", "--train"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--merged", default="/kaggle/working/s1_merged")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--keys-ck500", default="")
    ap.add_argument("--n-prompt", type=int, default=GS.N_PROMPT)
    ap.add_argument("--moi-buoc", type=int, default=2)
    ap.add_argument("--save-every", type=int, default=25)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--max-steps", type=int, default=500)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--no-q4", dest="q4", action="store_false")
    ap.add_argument("--seed", type=int, default=GS.SEED)
    a, la = ap.parse_known_args()
    print("[bỏ qua cờ của GRPO]", la, flush=True)
    a.adapter = a.adapter or os.path.join(a.bundle, "adapter_s1_seed101")
    train(a)


if __name__ == "__main__":
    main()
