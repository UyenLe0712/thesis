# -*- coding: utf-8 -*-
"""GRPO thưởng SPICE cho S1/101 — nhánh "S1 + GRPO, tắt đầu khe" của phương pháp file 250.

python grpo_spice.py --selftest --bundle B
python grpo_spice.py --merge --bundle B --merged M
python grpo_spice.py --gen --bundle B --merged M --c1 C --n 20 --out kiem_hoa.jsonl
python grpo_spice.py --probe --bundle B --merged M --out O
python grpo_spice.py --train --bundle B --merged M --out O --resume auto
python grpo_spice.py --gen --bundle B --merged M --c1 C --ckpt O/checkpoint-250 --out p.jsonl
"""

import os, re, sys, json, time, glob, random, argparse, dataclasses, collections

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")  # T4 ×2 trên Kaggle: Trainer thấy 2 GPU thì n_gpu=2, lô lệch
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_branch_data import prompt_body, SYS  # noqa: E402

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
SEED = 101
SEED_C1 = 20260927
MU = 0.02
N_PROMPT = 1000
PIX = dict(min_pixels=200704, max_pixels=1003520)
WORD = re.compile(r"[A-Za-z0-9'-]+")
STAT = {"n": 0, "t": 0.0}


def nwords(s):
    return len(WORD.findall(s or ""))


def _text(c):
    if isinstance(c, list):
        return (c[0].get("content") if c else "") or ""
    return c or ""


def spice_batch(cands, refs):
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.spice.spice import Spice

    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(refs)})
    c = tk.tokenize({i: [{"caption": s}] for i, s in enumerate(cands)})
    _, sc = Spice().compute_score(g, c)

    out = []
    for x in sc:
        f = x["All"]["f"]
        out.append(0.0 if f is None or f != f else float(f))
    return out


def r_spice(completions, gold, **kw):
    t0 = time.time()
    sents = [_text(c).strip() for c in completions]
    f = spice_batch([s if s else "none" for s in sents], list(gold))
    out = [0.0 if not s else x - MU * max(0, nwords(s) - nwords(g) - 3)
           for s, g, x in zip(sents, gold, f)]
    dt = time.time() - t0
    STAT["n"] += 1
    STAT["t"] += dt
    print(f"[spice] lần {STAT['n']} · {len(sents)} câu · {dt:.1f}s · thưởng TB {sum(out)/len(out):.3f}"
          f" · số từ TB {sum(map(nwords, sents))/len(sents):.1f} · rỗng {sum(not s for s in sents)}",
          flush=True)
    return out


def nap_ocr(bundle):
    return {o["image"]: o for o in map(
        json.loads, open(os.path.join(bundle, "ocr.jsonl"), encoding="utf-8")
    )}


def body_of(r, ocr):
    return prompt_body({"goal": r["goal"], "history": r.get("history") or []},
                       ocr.get(r["image"]))


def dung_hang(bundle, n=N_PROMPT, dai_nhat=0):
    tr = [json.loads(l) for l in open(os.path.join(bundle, "p1_train_rows.jsonl"), encoding="utf-8")]
    va = [json.loads(l) for l in open(os.path.join(bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    assert len(tr) == 4000 and len(va) == 1567, (len(tr), len(va))

    kv = {(r["episode_id"], r["step_id"]) for r in va}
    ev = {r["episode_id"] for r in va}
    ocr = nap_ocr(bundle)
    rows, bo = [], collections.Counter(
        trung_val=0, trung_episode_val=0, thieu_anh=0, thieu_ocr=0, rong=0
    )

    for r in tr:
        k = (r["episode_id"], r["step_id"])
        if k in kv:
            bo["trung_val"] += 1
            continue
        if r["episode_id"] in ev:
            bo["trung_episode_val"] += 1
            continue

        p = os.path.join(bundle, r["image"])
        if not os.path.exists(p):
            bo["thieu_anh"] += 1
            continue
        if r["image"] not in ocr:
            bo["thieu_ocr"] += 1
            continue

        gold = (r.get("target_instruction") or "").strip()
        if not gold:
            bo["rong"] += 1
            continue

        body = body_of(r, ocr)
        rows.append(dict(
            key=f"{k[0]}_{k[1]}",
            image=p,
            prompt=[
                {"role": "system", "content": SYS},
                {"role": "user", "content": "\n" + body},
            ],
            gold=gold,
            action_type=(r.get("action") or {}).get("action_type") or "",
            n_char=len(body),
        ))

    assert bo["trung_val"] == 0 and bo["trung_episode_val"] == 0, f"⛔ tập câu nhắc chạm val: {dict(bo)}"

    random.Random(SEED).shuffle(rows)
    rows = sorted(rows, key=lambda r: -r["n_char"])[:dai_nhat] if dai_nhat else rows[:n]
    return rows, dict(bo)


def selftest(a):
    gold = [
        "Click on the search bar",
        "Open the Clock app",
        "Click on the Settings icon at the top right corner",
    ]
    cand = [
        "Click on the search bar",
        "",
        "Click on the Settings icon at the top right corner of the screen and then wait for it to open fully",
    ]
    r = r_spice(cand, gold)
    print("thưởng:", [round(x, 3) for x in r], "← kỳ vọng [~1.0, 0.0, < câu 1]")
    assert r[0] > 0.99 and r[1] == 0.0 and r[2] < r[0]

    rows, bo = dung_hang(a.bundle, n=10 ** 9)
    print(f"tập câu nhắc dùng được: {len(rows)} · bỏ: {bo}")
    print("loại thao tác:", dict(collections.Counter(x["action_type"] for x in rows)))
    assert len(rows) >= N_PROMPT, len(rows)
    print("ví dụ câu nhắc:", json.dumps(rows[0]["prompt"], ensure_ascii=False)[:600])
    print("vàng:", rows[0]["gold"])
    print("✅ selftest ĐẠT")


def _dtype():
    import torch
    return torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16


def _kw(dt):
    import transformers
    return {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): dt}


def merge(a):
    if os.path.exists(os.path.join(a.merged, "config.json")):
        print("[hoà] đã có", a.merged, flush=True)
        return

    from transformers import Qwen2_5_VLForConditionalGeneration
    from peft import PeftModel

    dt = _dtype()
    m = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        BASE, device_map={"": 0}, **_kw(dt)
    )
    m = PeftModel.from_pretrained(m, a.adapter).merge_and_unload()
    m.save_pretrained(a.merged, safe_serialization=True)
    print(f"[hoà] xong → {a.merged} · dtype {dt}", flush=True)


def nap(a):
    import torch
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration, BitsAndBytesConfig

    dt = _dtype()
    kw = _kw(dt)

    if a.q4:
        kw["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=dt,
            bnb_4bit_use_double_quant=True,
        )

    proc = AutoProcessor.from_pretrained(BASE, **PIX)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        a.merged, device_map={"": 0}, **kw
    )
    print(f"[nạp] {a.merged} · dtype {dt} · 4-bit {a.q4} · {torch.cuda.get_device_name(0)}",
          flush=True)
    return proc, model, dt


def gen(a):
    import torch
    from PIL import Image

    proc, model, _ = nap(a)

    if a.ckpt:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.ckpt)
        print("[điểm lưu]", a.ckpt, flush=True)

    model.eval()
    va = [json.loads(l) for l in open(
        os.path.join(a.bundle, "p1_val_rows.jsonl"), encoding="utf-8"
    )]
    rows = random.Random(SEED_C1).sample(va, 400)
    C1 = [json.loads(l) for l in open(a.c1, encoding="utf-8")]

    assert [(r["episode_id"], r["step_id"]) for r in rows] == \
           [(d["episode_id"], d["step_id"]) for d in C1], \
           "⛔ thứ tự 400 bước lệch c1_mau.jsonl"

    rows = C1 = rows[:a.n], C1[:a.n]
    rows, C1 = rows
    ocr = nap_ocr(a.bundle)
    done = set()

    if os.path.exists(a.out):
        done = {
            (d["episode_id"], d["step_id"])
            for d in map(json.loads, open(a.out, encoding="utf-8"))
        }

    fo = open(a.out, "a", encoding="utf-8")
    t0 = time.time()

    for i, r in enumerate(rows):
        if (r["episode_id"], r["step_id"]) in done:
            continue

        msg = [
            {"role": "system", "content": SYS},
            {"role": "user", "content": [
                {"type": "image"},
                {"type": "text", "text": "\n" + body_of(r, ocr)},
            ]},
        ]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]

        with torch.no_grad():
            g = model.generate(
                **inp,
                max_new_tokens=96,
                do_sample=False,
                use_cache=True,
                temperature=None,
                top_p=None,
                top_k=None,
            )

        s = proc.decode(g[0][L:], skip_special_tokens=True).strip()
        fo.write(json.dumps({
            "episode_id": r["episode_id"],
            "step_id": r["step_id"],
            "pred": s,
        }, ensure_ascii=False) + "\n")
        fo.flush()

        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{len(rows)} · {(time.time()-t0)/60:.1f} phút · {s[:60]!r}",
                  flush=True)

    fo.close()
    P = {
        (d["episode_id"], d["step_id"]): d["pred"]
        for d in map(json.loads, open(a.out, encoding="utf-8"))
    }
    assert all(P.get((d["episode_id"], d["step_id"])) for d in C1), "⛔ có câu rỗng hoặc thiếu bước"
    same = sum(P[(d["episode_id"], d["step_id"])] == d["greedy"] for d in C1)
    tag = "[kiểm hoà]" if not a.ckpt else "[so với S1]"
    print(f"{tag} {same}/{len(C1)} câu trùng greedy S1 của c1_mau", flush=True)


def _n_s1(adapter):
    from safetensors import safe_open
    with safe_open(os.path.join(adapter, "adapter_model.safetensors"), "pt") as f:
        return sum(f.get_tensor(k).numel() for k in f.keys())


def train(a):
    import torch, trl, transformers, peft
    from peft import LoraConfig, get_peft_model
    from trl import GRPOConfig, GRPOTrainer
    from datasets import Dataset, Image as HFImage

    print(f"trl {trl.__version__} · transformers {transformers.__version__} · "
          f"peft {peft.__version__} · torch {torch.__version__}", flush=True)

    proc, model, dt = nap(a)
    proc.tokenizer.padding_side = "left"

    s1 = json.load(open(os.path.join(a.adapter, "adapter_config.json"), encoding="utf-8"))
    lc = LoraConfig(
        r=s1["r"],
        lora_alpha=s1["lora_alpha"],
        lora_dropout=0.0,
        bias="none",
        target_modules=s1["target_modules"],
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lc)
    model.enable_input_require_grads()

    ntr = 0
    for n, p_ in model.named_parameters():
        if p_.requires_grad:
            if "visual" in n:
                raise SystemExit(f"⛔ tháp thị giác đang học: {n}")
            if p_.dtype != torch.float32:
                p_.data = p_.data.float()
            ntr += p_.numel()

    ns1 = _n_s1(a.adapter)
    print(f"[LoRA mới] tham số học {ntr:,} · S1 có {ns1:,}", flush=True)
    assert ntr == ns1, "⛔ LoRA mới không cùng cỡ S1"

    rows, bo = dung_hang(
        a.bundle,
        n=a.n_prompt,
        dai_nhat=(50 if a.probe else 0),
    )
    print(f"[câu nhắc] {len(rows)} · bỏ {bo} · n_char max {max(r['n_char'] for r in rows)}",
          flush=True)

    os.makedirs(a.out, exist_ok=True)
    json.dump(
        [r["key"] for r in rows],
        open(os.path.join(a.out, "prompt_keys.json"), "w"),
    )

    ds = Dataset.from_list(rows).cast_column("image", HFImage())

    bf = dt == torch.bfloat16
    want = dict(
        output_dir=a.out,
        seed=SEED,
        bf16=bf,
        fp16=not bf,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        num_generations=a.G,
        per_device_train_batch_size=a.bs,
        gradient_accumulation_steps=a.accum,
        max_completion_length=96,
        temperature=1.0,
        top_p=1.0,
        top_k=0,
        repetition_penalty=1.0,
        beta=a.beta,
        learning_rate=a.lr,
        lr_scheduler_type="constant_with_warmup",
        warmup_steps=10,
        max_steps=(20 if a.probe else a.max_steps),
        num_train_epochs=1,
        mask_truncated_completions=True,
        log_completions=a.probe,
        num_completions_to_print=2,
        logging_steps=1,
        save_steps=(10 ** 9 if a.probe else 25),
        save_total_limit=None,
        report_to="none",
        remove_unused_columns=False,
        dataloader_num_workers=2,
        disable_tqdm=True,
        max_grad_norm=1.0,
    )

    F = {f.name for f in dataclasses.fields(GRPOConfig)}
    thieu = sorted(set(want) - F)
    print("⚠️ GRPOConfig không có khoá (đã bỏ):", thieu, flush=True)
    assert not {"beta", "num_generations", "temperature", "max_completion_length"} & set(thieu)

    args = GRPOConfig(**{k: v for k, v in want.items() if k in F})
    gb = getattr(args, "generation_batch_size", None)

    print("GRPOConfig:", {
        k: getattr(args, k, None)
        for k in (
            "num_generations",
            "per_device_train_batch_size",
            "gradient_accumulation_steps",
            "generation_batch_size",
            "steps_per_generation",
            "max_completion_length",
            "temperature",
            "top_p",
            "top_k",
            "beta",
            "learning_rate",
            "loss_type",
            "scale_rewards",
            "max_steps",
            "bf16",
            "fp16",
        )
    }, flush=True)

    print(f"[lô] mỗi lượt sinh {gb} câu = {gb // a.G if gb else '?'} câu nhắc × {a.G}",
          flush=True)

    trainer = GRPOTrainer(
        model=model,
        reward_funcs=[r_spice],
        args=args,
        train_dataset=ds,
        processing_class=proc,
    )

    resume = a.resume
    if resume == "auto":
        # chỉ lấy điểm lưu ghi trọn: bị dừng lúc đang lưu thì thư mục cuối có thể thiếu tệp
        ck = sorted(
            (p for p in glob.glob(os.path.join(a.out, "checkpoint-*"))
             if all(os.path.exists(os.path.join(p, f)) for f in
                    ("trainer_state.json", "optimizer.pt", "adapter_model.safetensors"))),
            key=lambda p: int(p.rsplit("-", 1)[1]),
        )
        co = glob.glob(os.path.join(a.out, "checkpoint-*"))
        assert ck or not co, f"DỪNG: có {len(co)} điểm lưu mà không cái nào đủ tệp, xem {co[:3]}"
        resume = ck[-1] if ck else None

    print("[tiếp từ]", resume, flush=True)
    if resume:
        # transformers (trainer.py, nhánh adapter_subdirs): điểm lưu có thư mục con `ref/` thì
        # CHỈ nạp thư mục con, bỏ qua adapter `default` ở gốc ⇒ chạy tiếp từ S1 mà không báo gì
        # (lỗi đã xảy ra ở commit 2 ngày 30/9). Nạp tay `default` trước khi train.
        from safetensors.torch import load_file
        from peft import set_peft_model_state_dict
        nB = lambda: sum(p.float().norm().item() for n, p in trainer.model.named_parameters()
                         if "lora_B" in n and ".default." in n)
        truoc = nB()
        sd = load_file(os.path.join(resume, "adapter_model.safetensors"))
        kq = set_peft_model_state_dict(trainer.model, sd, adapter_name="default")
        la = [k for k in getattr(kq, "unexpected_keys", []) if "lora" in k]
        sau = nB()
        print(f"[nạp default] {len(sd)} tensor · |lora_B| {truoc:.4f} → {sau:.4f} · khoá lạ {len(la)}",
              flush=True)
        assert sau > 0 and not la, "DỪNG: không nạp được adapter default từ điểm lưu"
    torch.cuda.reset_peak_memory_stats()
    t0 = time.time()

    trainer.train(resume_from_checkpoint=resume)

    el = time.time() - t0
    buoc = max(
        trainer.state.global_step - (int(resume.rsplit("-", 1)[1]) if resume else 0),
        1,
    )

    print(
        f"[xong] {buoc} bước · {el/60:.1f} phút · {el/buoc:.1f} s/bước · "
        f"đỉnh VRAM {torch.cuda.max_memory_allocated()/2**30:.2f} GiB · "
        f"SPICE {STAT['t']/max(STAT['n'], 1):.1f} s/lần",
        flush=True,
    )

    trainer.save_model(os.path.join(a.out, "final"))
    json.dump(
        trainer.state.log_history,
        open(os.path.join(a.out, "log_history.json"), "w"),
        indent=1,
    )


def main():
    ap = argparse.ArgumentParser()

    for f in ("--selftest", "--merge", "--gen", "--probe", "--train"):
        ap.add_argument(f, action="store_true")

    ap.add_argument("--bundle", required=True)
    ap.add_argument("--merged", default="/kaggle/working/s1_merged")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--c1")
    ap.add_argument("--ckpt")
    ap.add_argument("--out")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--n-prompt", type=int, default=N_PROMPT)
    ap.add_argument("--G", type=int, default=8)
    ap.add_argument("--bs", type=int, default=8)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--beta", type=float, default=0.04)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--max-steps", type=int, default=500)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--no-q4", dest="q4", action="store_false")

    a = ap.parse_args()
    a.adapter = a.adapter or os.path.join(a.bundle, "adapter_s1_seed101")

    if a.selftest:
        selftest(a)
    elif a.merge:
        merge(a)
    elif a.gen:
        assert a.c1 and a.out, "cần --c1 và --out"
        gen(a)
    elif a.probe or a.train:
        assert a.out, "cần --out"
        train(a)
    else:
        ap.error("chọn một chế độ")


if __name__ == "__main__":
    main()
