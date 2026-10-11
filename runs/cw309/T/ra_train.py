# -*- coding: utf-8 -*-
"""304 — SFT ngắn TIẾP TỪ adapter ck500 (một nhánh mỗi lần gọi).

Nền: S1 đã hoà (`s1_merged`) nạp 4-bit như lúc GRPO train ck500 (grpo_spice.nap, q4).
Adapter học: CHÍNH adapter ck500 (is_trainable) → cùng cỡ LoRA, cùng chỗ gắn; lúc sinh gắn adapter mới lên
`s1_merged` fp16 đúng như đã sinh ck500 (gen_test_grpo / ra_gen).
Đích = câu chuẩn; chỉ tính loss trên token của câu đích + <|im_end|>. Tháp thị giác không học.
Câu nhắc lúc dạy dựng CÙNG cách với lúc sinh: SYS + [ảnh, "\\n" + body].

  python ra_train.py --merged M --ckpt CK500 --data train_ra.jsonl --out O/ra_sft
  python ra_train.py ... --n 32 --out O/thu_ra      # chạy thử: 2 bước tối ưu
Nối tiếp: chạy lại đúng lệnh; script tự nạp O/last nếu có.
"""
import os, sys, json, math, time, argparse

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

N_CK500 = 14966784


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged", required=True)
    ap.add_argument("--ckpt", required=True, help="thư mục adapter ck500")
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--accum", type=int, default=16)
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--warmup", type=int, default=10)
    ap.add_argument("--n", type=int, default=0, help="chỉ lấy N hàng đầu (chạy thử)")
    ap.add_argument("--save-every", type=int, default=25)
    ap.add_argument("--max-hours", type=float, default=10.5)
    ap.add_argument("--seed", type=int, default=101)
    a = ap.parse_args()
    a.q4 = True

    import torch
    from PIL import Image
    from peft import PeftModel, set_peft_model_state_dict
    from safetensors.torch import load_file
    import grpo_spice as GS
    from build_branch_data import SYS

    torch.manual_seed(a.seed)
    rows = [json.loads(l) for l in open(a.data, encoding="utf-8")]
    if a.n:
        rows = rows[:a.n]
    n_step = math.ceil(len(rows) * a.epochs / a.accum)
    order = [i % len(rows) for i in range(n_step * a.accum)]
    print(f"[dữ liệu] {a.data} · {len(rows)} hàng · {n_step} bước tối ưu × lô {a.accum} · lr {a.lr}", flush=True)

    proc, model, dt = GS.nap(a)
    model.config.use_cache = False
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    model = PeftModel.from_pretrained(model, a.ckpt, is_trainable=True)

    params, ntr = [], 0
    for n, p in model.named_parameters():
        if p.requires_grad:
            if "visual" in n:
                raise SystemExit(f"⛔ tháp thị giác đang học: {n}")
            if p.dtype != torch.float32:
                p.data = p.data.float()
            params.append(p)
            ntr += p.numel()
    print(f"[adapter] {a.ckpt} · tham số học {ntr:,} (ck500 {N_CK500:,}) · dtype tính {dt}", flush=True)
    assert ntr == N_CK500, "⛔ adapter không cùng cỡ ck500 — sai thư mục --ckpt?"

    opt = torch.optim.AdamW(params, lr=a.lr, betas=(0.9, 0.999), weight_decay=0.0)

    def lam(s):
        if s < a.warmup:
            return (s + 1) / a.warmup
        return 0.5 * (1 + math.cos(math.pi * (s - a.warmup) / max(1, n_step - a.warmup)))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lam)
    use_scaler = dt == torch.float16
    scaler = torch.amp.GradScaler("cuda", enabled=use_scaler)

    os.makedirs(a.out, exist_ok=True)
    last = os.path.join(a.out, "last")
    step = 0
    if os.path.exists(os.path.join(last, "state.pt")):
        sd = load_file(os.path.join(last, "adapter_model.safetensors"))
        kq = set_peft_model_state_dict(model, sd, adapter_name="default")
        la = [k for k in getattr(kq, "unexpected_keys", []) if "lora" in k]
        assert not la, f"⛔ nạp last lỗi: {la[:3]}"
        S = torch.load(os.path.join(last, "state.pt"), map_location="cpu", weights_only=False)
        opt.load_state_dict(S["opt"])
        sched.load_state_dict(S["sched"])
        if use_scaler and S.get("scaler"):
            scaler.load_state_dict(S["scaler"])
        step = S["step"]
        print(f"[nối tiếp] từ bước {step}/{n_step}", flush=True)

    def luu(path):
        model.save_pretrained(path)
        torch.save(dict(opt=opt.state_dict(), sched=sched.state_dict(),
                        scaler=scaler.state_dict() if use_scaler else None, step=step,
                        lr=a.lr, data=a.data), os.path.join(path, "state.pt"))

    tok_end = proc.tokenizer("<|im_end|>", add_special_tokens=False).input_ids

    def mau(r):
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + r["body"]}]}]
        ptext = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(r["image"]).convert("RGB")
        inp = proc(text=[ptext + r["gold"] + "<|im_end|>"], images=[img], return_tensors="pt")
        tail = proc.tokenizer(r["gold"], add_special_tokens=False).input_ids + tok_end
        ids = inp["input_ids"][0].tolist()
        if ids[-len(tail):] != tail:
            pid = proc(text=[ptext], images=[img], return_tensors="pt")["input_ids"][0].tolist()
            assert ids[:len(pid)] == pid, "⛔ token câu nhắc đổi khi nối câu đích"
            n_lab = len(ids) - len(pid)
        else:
            n_lab = len(tail)
        lab = inp["input_ids"].clone()
        lab[:, : lab.shape[1] - n_lab] = -100
        inp = {k: v.to(model.device) for k, v in inp.items()}
        if "pixel_values" in inp:
            inp["pixel_values"] = inp["pixel_values"].to(dt)
        return inp, lab.to(model.device), n_lab

    inp0, lab0, n0 = mau(rows[0])
    nhan = proc.tokenizer.decode(inp0["input_ids"][0][-n0:])
    print(f"[kiểm nhãn] mẫu đầu: {inp0['input_ids'].shape[1]} token, tính loss {n0} token: {nhan!r} · đích {rows[0]['gold']!r}",
          flush=True)
    assert nhan.replace("<|im_end|>", "").strip() == rows[0]["gold"].strip(), "⛔ nhãn không đúng câu đích"
    del inp0, lab0

    model.train()
    t0 = time.time()
    torch.cuda.reset_peak_memory_stats()
    run_loss, run_n, b0 = 0.0, 0, step
    while step < n_step:
        if (time.time() - t0) / 3600 > a.max_hours:
            luu(last)
            print(f"[dừng giờ] lưu ở bước {step}/{n_step} — chạy lại đúng lệnh để nối tiếp", flush=True)
            return
        for j in range(a.accum):
            inp, lab, n_lab = mau(rows[order[step * a.accum + j]])
            with torch.autocast("cuda", dtype=dt):
                out = model(**inp, labels=lab)
            loss = out.loss
            if not torch.isfinite(loss):
                raise SystemExit(f"⛔ loss không hữu hạn ở bước {step}, mẫu {j}")
            scaler.scale(loss / a.accum).backward()
            run_loss += loss.item()
            run_n += 1
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(params, 1.0).item()
        scaler.step(opt)
        scaler.update()
        opt.zero_grad(set_to_none=True)
        sched.step()
        step += 1
        if step % 5 == 0 or step == 1 or step == n_step:
            el = time.time() - t0
            print(f"  bước {step}/{n_step} · loss {run_loss / run_n:.4f} · |g| {gn:.3f} · "
                  f"lr {sched.get_last_lr()[0]:.2e} · {el / max(step - b0, 1):.1f} s/bước · "
                  f"VRAM {torch.cuda.max_memory_allocated() / 2**30:.1f} GiB", flush=True)
            run_loss, run_n = 0.0, 0
        if step % a.save_every == 0 and step < n_step:
            luu(last)

    fin = os.path.join(a.out, "final")
    luu(fin)
    luu(last)
    print(f"[xong] {step} bước · {(time.time() - t0) / 60:.1f} phút → {fin}", flush=True)


if __name__ == "__main__":
    main()
