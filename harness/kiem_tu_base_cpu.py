# -*- coding: utf-8 -*-
"""Kiểm lượt `tu=base` (grpo_tu_base.py) bằng mô hình THẬT trên Kaggle CPU, 7/11/2026 — 0 GPU.

Selftest cũ chỉ nạp giả. Ở đây đi đúng đường GL.train dùng, dừng trước GRPOTrainer:
  1. GS.nap qua bọc của grpo_tu_base: phải in `[xuất phát] Base …`, nạp đúng Qwen/Qwen2.5-VL-3B-Instruct
     dù --merged trỏ s1_merged (fp32 trên CPU thay cho fp16 T4; mọi thứ khác như cũ).
  2. LoRA mới cấu hình như grpo_luoi.train (r/alpha/target của S1): số tham số học = S1, không tham số thị giác,
     lora_B toàn 0.
  3. Với 2 câu nhắc thật (ảnh + OCR): logits khi bật adapter = khi tắt adapter ⇒ KL tới tham chiếu = 0 ở bước 0,
     và tham chiếu đúng là Base (so với một lần nạp Base thứ hai không qua bọc, không LoRA).
  4. GS.dung_hang(seed 101) ra đúng tập câu nhắc của ck500 (prompt_keys_ck500.json) nếu có tệp.
  5. Greedy 2 câu từ Base (mốc độ dài câu, Base trung vị ~71 ký tự trên test).
  python kiem_tu_base_cpu.py --bundle B --adapter A [--keys prompt_keys_ck500.json]
"""
import argparse, json, os, sys, time, types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch, transformers  # noqa: E402
import grpo_spice as GS     # noqa: E402
import grpo_tu_base as TB   # noqa: E402

t0 = time.time()
log = lambda *a: print(f"[{time.time() - t0:6.0f} s]", *a, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--keys", default="")
    a = ap.parse_args()
    assert not torch.cuda.is_available(), "phép kiểm này dành cho CPU"
    GS._dtype = lambda: torch.float32
    torch.cuda.get_device_name = lambda i=0: "CPU"
    M = transformers.Qwen2_5_VLForConditionalGeneration
    goc = M.from_pretrained.__func__

    def fp(cls, path, *x, **kw):
        kw["device_map"] = "cpu"
        return goc(cls, path, *x, **kw)
    M.from_pretrained = classmethod(fp)

    TB.cai()
    ns = types.SimpleNamespace(merged="/kaggle/working/s1_merged", q4=False)
    proc, model, dt = GS.nap(ns)
    assert ns.merged == GS.BASE and model.config._name_or_path == GS.BASE, (ns.merged, model.config._name_or_path)
    log("✅ 1. nạp Base qua bọc tu=base", model.config._name_or_path, dt)

    from peft import LoraConfig, get_peft_model
    s1 = json.load(open(os.path.join(a.adapter, "adapter_config.json"), encoding="utf-8"))
    lc = LoraConfig(r=s1["r"], lora_alpha=s1["lora_alpha"], lora_dropout=0.0, bias="none",
                    target_modules=s1["target_modules"], task_type="CAUSAL_LM")
    model = get_peft_model(model, lc)
    ntr = sum(p.numel() for n, p in model.named_parameters() if p.requires_grad)
    vis = [n for n, p in model.named_parameters() if p.requires_grad and "visual" in n]
    nb = [n for n, p in model.named_parameters() if "lora_B" in n and p.abs().max().item() != 0]
    ns1 = GS._n_s1(a.adapter)
    log(f"[LoRA mới] r {s1['r']} · alpha {s1['lora_alpha']} · học {ntr:,} · S1 {ns1:,} · thị giác học {len(vis)} · lora_B≠0 {len(nb)}")
    assert ntr == ns1 and not vis and not nb
    log("✅ 2. LoRA mới cùng cỡ S1, không học thị giác, B = 0")

    rows, bo = GS.dung_hang(a.bundle, n=GS.N_PROMPT, seed=101)
    keys = [r["key"] for r in rows]
    log(f"[câu nhắc] {len(rows)} · bỏ {dict(bo)}")
    if a.keys and os.path.exists(a.keys):
        k0 = json.load(open(a.keys))
        assert keys == k0, f"⛔ tập câu nhắc khác ck500 ({len(keys)} vs {len(k0)}, trùng {len(set(keys) & set(k0))})"
        log("✅ 4. tập câu nhắc trùng thứ tự ck500")
    else:
        log("⚠️ 4. không có prompt_keys_ck500.json, bỏ qua")

    from PIL import Image
    model.eval()
    proc.tokenizer.padding_side = "left"
    inps = []
    for r in rows[:2]:
        msg = [{"role": "system", "content": GS.SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": r["prompt"][1]["content"]}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(r["image"]).convert("RGB")
        inps.append((r, proc(text=[text], images=[img], return_tensors="pt")))
    lg_on, lg_off = [], []
    with torch.no_grad():
        for r, inp in inps:
            lg_on.append(model(**inp).logits[0, -8:].clone())
            with model.disable_adapter():
                lg_off.append(model(**inp).logits[0, -8:].clone())
            log(f"  {r['key']}: {inp['input_ids'].shape[1]} token · max|Δlogit| bật−tắt adapter "
                f"{(lg_on[-1] - lg_off[-1]).abs().max().item():.3e}")
    assert all(torch.equal(x, y) for x, y in zip(lg_on, lg_off)), "⛔ adapter mới làm đổi logits ở bước 0"
    log("✅ 3a. logits bật = tắt adapter (KL = 0 ở bước 0)")

    with torch.no_grad():
        for r, inp in inps:
            L = inp["input_ids"].shape[1]
            g = model.generate(**inp, max_new_tokens=48, do_sample=False, temperature=None, top_p=None, top_k=None)
            s = proc.decode(g[0][L:], skip_special_tokens=True).strip()
            log(f"  greedy Base {r['key']}: {s!r} ({len(s)} ký tự) · câu chuẩn {r['gold']!r}")
    log("✅ 5. sinh được câu từ Base")
    import gc
    del model; gc.collect()   # hai bản fp32 3B không vừa 30 GB RAM
    ref = M.from_pretrained(GS.BASE, device_map="cpu", **GS._kw(torch.float32))
    ref.eval()
    with torch.no_grad():
        d = max((ref(**inp).logits[0, -8:] - x).abs().max().item() for (_, inp), x in zip(inps, lg_off))
    log(f"  Base nạp thẳng (không bọc, không LoRA) − tham chiếu: max|Δlogit| {d:.3e}")
    assert d < 1e-3, "⛔ tham chiếu KL không phải Base"
    log("✅ 3b. tham chiếu KL = Base")
    del ref

    log("TONG: tu=base ĐẠT trên mô hình thật (CPU, fp32)")


if __name__ == "__main__":
    main()
