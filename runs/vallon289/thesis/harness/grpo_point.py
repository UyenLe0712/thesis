# -*- coding: utf-8 -*-
"""GRPO với phần thưởng kiểm chứng được trên ô <point> — nối tiếp từ MIN-DESC/101.

Đăng ký trước: report/106 mục (x19). Debate: report/143 §4.

    # máy nhà, 0 GPU — kiểm hàm thưởng + dựng tập câu nhắc trên ảnh có sẵn
    python3 harness/grpo_point.py --selftest

    # Colab A100 — thăm dò 20 bước trên 50 câu nhắc DÀI NHẤT (luật P10)
    python harness/grpo_point.py --probe --adapter <MIN adapter> --out <thư mục Drive>

    # Colab A100 — lượt thật
    python harness/grpo_point.py --train --adapter <MIN adapter> --out <thư mục Drive>

Phần thưởng (khoá ở (x19), tổng tối đa 1,3):
  r_point  = 1,0  nếu <desc> phân tách được VÀ |x−gx| ≤ 140 VÀ |y−gy| ≤ 140 (lưới 0–1000,
                  đúng dung sai của cổng khai báo gate_desc_acc.TAU);
  r_format = 0,2  nếu đúng MỘT khối <desc>…</desc> tách được 4 ô (neo vào ô <point>; tên được
                  chứa "|"), sau đó "\\n" rồi câu 2–40 từ, không còn thẻ nào khác;
  r_name   = 0,1  nếu ô tên trong khai báo có ≥1 token (không phải từ dừng) xuất hiện trong câu.
Câu nhắc lấy NGUYÊN VĂN từ branches/s2.json (trùng byte với lúc dạy S2/MIN); chuỗi người dùng
bỏ "<image>" và giữ "\\n" đầu vì TRL chèn khối ảnh TRƯỚC khối chữ (prepare_multimodal_messages).
Vàng lấy từ train_ac/descriptors.jsonl (point_norm). Loại 9 bước point_norm ngoài [0,1000].
⛔ Tập thưởng CHỈ từ train_ac. Tập kiểm không được đụng.
"""
import os, re, json, math, random, argparse, time, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TR = os.path.join(HERE, "dg1_cache", "train_ac")
TE = os.path.join(HERE, "dg1_cache", "test_ac")
BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
TOL = 140                        # = gate_desc_acc.TAU * 1000
SEED = 101
N_PROMPT = 2000                  # (x19)
IMG = re.compile(r"ep(\d+)_s(\d+)\.png$")
DESC = re.compile(r"<desc>(.*?)</desc>", re.S)
PT = re.compile(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>")
TAG = re.compile(r"<[^>]+>")
STOP = set("the a an to on of in at and or for with your you this that it is be tap click "
           "press select open go button icon option screen".split())

# ───────────────────────────── phần thưởng ─────────────────────────────
def chuan(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tach(text):
    """→ (desc_fields | None, point (x,y) | None, sentence | None, well_formed: bool)."""
    text = text or ""
    ds = DESC.findall(text)
    if len(ds) != 1:
        return None, None, None, False
    d = ds[0]
    raw = [p.strip() for p in d.split("|")]
    # neo vào ô chứa <point>: role | tên (có thể chứa "|") | <point> | dấu hiệu — 67/41.090 tên vàng có "|"
    ip = [i for i, p in enumerate(raw) if "<point>" in p]
    o = None
    if len(ip) == 1 and ip[0] >= 2 and ip[0] == len(raw) - 2:
        o = [raw[0], " | ".join(raw[1:ip[0]]), raw[ip[0]], raw[-1]]
    m = PT.search(d)
    pt = (int(m.group(1)), int(m.group(2))) if m else None
    tail = text.split("</desc>", 1)[1]
    sent = tail.strip()
    well = (o is not None and pt is not None and tail.startswith("\n")
            and not TAG.search(sent) and 2 <= len(sent.split()) <= 40)
    return o, pt, (sent or None), well


def _content(c):
    return c[0]["content"] if isinstance(c, list) else c


def r_point(completions, gold_x, gold_y, **kw):
    out = []
    for c, gx, gy in zip(completions, gold_x, gold_y):
        _, pt, _, _ = tach(_content(c))
        out.append(1.0 if pt and abs(pt[0] - gx) <= TOL and abs(pt[1] - gy) <= TOL else 0.0)
    return out


def r_format(completions, **kw):
    return [0.2 if tach(_content(c))[3] else 0.0 for c in completions]


def r_name(completions, **kw):
    out = []
    for c in completions:
        o, _, sent, _ = tach(_content(c))
        if not o or not sent:
            out.append(0.0); continue
        toks = [t for t in chuan(o[1]).split() if t not in STOP]
        st = set(chuan(sent).split())
        out.append(0.1 if toks and any(t in st for t in toks) else 0.0)
    return out


REWARDS = [r_point, r_format, r_name]

# ───────────────────────────── tập câu nhắc ─────────────────────────────
def nap_vang():
    D = {}
    for l in open(os.path.join(TR, "descriptors.jsonl"), encoding="utf-8"):
        d = json.loads(l)
        D[(str(d["episode_id"]), str(d["step_id"]))] = d
    return D


def dung_hang(img_root=None, n=N_PROMPT, seed=SEED, chi_anh_co_san=False, dai_nhat=0):
    """Trả về list[dict] hàng dữ liệu cho GRPOTrainer (chưa decode ảnh).
    img_root: thư mục images (mặc định TR/images). dai_nhat>0: lấy k câu nhắc dài nhất (probe)."""
    img_root = img_root or os.path.join(TR, "images")
    D = nap_vang()
    s2 = json.load(open(os.path.join(TR, "branches", "s2.json"), encoding="utf-8"))
    rows, bo = [], {"khong_desc": 0, "ngoai_luoi": 0, "thieu_vang": 0, "thieu_anh": 0}
    for e in s2:
        tgt = e["messages"][-1]["content"]
        if "<desc>" not in tgt:
            bo["khong_desc"] += 1; continue          # bước không chạm
        m = IMG.search(e["images"][0]); k = (m.group(1), m.group(2))
        g = D.get(k)
        if not g:
            bo["thieu_vang"] += 1; continue
        gx, gy = g["point_norm"]
        if not (0 <= gx <= 1000 and 0 <= gy <= 1000):
            bo["ngoai_luoi"] += 1; continue
        user = e["messages"][1]["content"]
        assert user.startswith("<image>\n"), user[:40]
        user = user[len("<image>"):]                 # giữ "\n" đầu — TRL đặt khối ảnh trước
        p = os.path.join(img_root, os.path.basename(e["images"][0]))
        if chi_anh_co_san and not os.path.exists(p):
            bo["thieu_anh"] += 1; continue
        rows.append(dict(
            key=f"{k[0]}_{k[1]}", image=p,
            prompt=[{"role": "system", "content": e["messages"][0]["content"]},
                    {"role": "user", "content": user}],
            gold_x=int(gx), gold_y=int(gy), gold_name=g.get("name") or "",
            gold_desc=g["desc"], n_char=len(user)))
    eps_kiem = _test_eps()
    assert not any(r["key"].split("_")[0] in eps_kiem for r in rows), "⛔ rò rỉ: episode tập kiểm trong tập thưởng"
    rng = random.Random(seed); rng.shuffle(rows)
    if dai_nhat:
        rows = sorted(rows, key=lambda r: -r["n_char"])[:dai_nhat]
    else:
        rows = rows[:n]
    return rows, bo


def _test_eps():
    p = os.path.join(TE, "test.jsonl")
    if not os.path.exists(p):
        return set()
    return {str(json.loads(l)["episode_id"]) for l in open(p, encoding="utf-8")}


def to_hf(rows):
    from datasets import Dataset, Image
    ds = Dataset.from_list(rows)
    return ds.cast_column("image", Image())          # decode PIL lúc truy cập


# ───────────────────────────── selftest (0 GPU) ─────────────────────────────
def selftest():
    fake = ["<desc>item | Search here | <point>440,91</point> | above “Coffee”</desc>\nTap the search bar",
            "<desc>item | MEN | <point>334,238</point> | below “Fashion”</desc>\nTap MEN at the top",
            "Tap the search bar",
            "<desc>item | Search | <point>440,91</point></desc>\nTap Search",
            "<desc>a|b|<point>440,91</point>|c</desc>\n<desc>x|y|<point>1,1</point>|z</desc>\nTap b",
            "<desc>item | Search here | <point>440,91</point> | above</desc>\n"]
    gx, gy = [440] * 6, [91] * 6
    print("r_point :", r_point(fake, gx, gy), "← kỳ vọng [1,0,0,1,0,1]")
    print("r_format:", r_format(fake), "← kỳ vọng [0.2,0.2,0,0,0,0]")
    print("r_name  :", r_name(fake), "← kỳ vọng [0.1,0.1,0,0,0,0] (ô 3 chỉ có 3 trường ⇒ không thưởng tên)")
    assert r_point(fake, gx, gy) == [1.0, 0.0, 0.0, 1.0, 0.0, 1.0]
    assert r_format(fake) == [0.2, 0.2, 0.0, 0.0, 0.0, 0.0]
    assert r_name(fake) == [0.1, 0.1, 0.0, 0.0, 0.0, 0.0]
    # dạng hội thoại (TRL đưa list[dict])
    assert r_point([[{"role": "assistant", "content": fake[0]}]], [440], [91]) == [1.0]
    rows, bo = dung_hang(chi_anh_co_san=True)
    print(f"hàng dựng được trên ảnh có sẵn: {len(rows)} · bỏ: {bo}")
    rows_all, bo_all = dung_hang(n=10**9)
    print(f"toàn tập (không cần ảnh): {len(rows_all)} · bỏ: {bo_all}  ← kỳ vọng 41.090 = 41.099 − 9")
    assert len(rows_all) == 41099 - 9, len(rows_all)
    assert len({r["key"] for r in rows_all}) == len(rows_all)
    r0 = rows_all[0]
    assert r0["prompt"][1]["content"].startswith("\nMục tiêu:"), r0["prompt"][1]["content"][:30]
    # phần thưởng của chính khai báo vàng phải = 1,3 (đích dạy là mẫu hoàn hảo)
    gold_full = [r["gold_desc"] + "\nTap it now" for r in rows_all[:500]]
    rp = r_point(gold_full, [r["gold_x"] for r in rows_all[:500]], [r["gold_y"] for r in rows_all[:500]])
    print(f"r_point trên khai báo vàng: {sum(rp)}/500 (phải 500) · r_format: {sum(r_format(gold_full)):.1f} (phải 100.0)")
    assert sum(rp) == 500 and abs(sum(r_format(gold_full)) - 100.0) < 1e-6
    try:
        ds = to_hf(rows[:3])
        im = ds[0]["image"]; print("HF Dataset + Image OK:", type(im).__name__, im.size)
    except ImportError:
        print("(không có `datasets` trên máy này — bỏ qua phép HF)")
    print("✅ selftest ĐẠT")


# ───────────────────────────── train / probe (GPU) ─────────────────────────────
def train(a):
    import torch
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration, BitsAndBytesConfig
    from peft import PeftModel
    from trl import GRPOConfig, GRPOTrainer
    import trl, transformers, peft
    print(f"trl {trl.__version__} · transformers {transformers.__version__} · peft {peft.__version__} · torch {torch.__version__}")

    proc = AutoProcessor.from_pretrained(BASE, min_pixels=200704, max_pixels=1003520,
                                         padding_side="left", truncation_side="left")
    proc.tokenizer.padding_side = "left"; proc.tokenizer.truncation_side = "left"
    ip = proc.image_processor
    print("image_processor:", {k: getattr(ip, k, None) for k in ("min_pixels", "max_pixels", "size")})
    assert proc.tokenizer.padding_side == "left"

    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        BASE, quantization_config=bnb, torch_dtype=torch.bfloat16, device_map={"": 0})
    model = PeftModel.from_pretrained(model, a.adapter, is_trainable=True)
    model.enable_input_require_grads()
    for n_, p_ in model.named_parameters():        # LoRA của tháp thị giác không tồn tại (đã freeze), kiểm cho chắc
        if p_.requires_grad and "visual" in n_:
            raise SystemExit(f"⛔ tham số tháp thị giác đang huấn luyện: {n_}")
    model.print_trainable_parameters()
    cfg = json.load(open(os.path.join(a.adapter, "adapter_config.json")))
    print("adapter:", {k: cfg.get(k) for k in ("r", "lora_alpha", "lora_dropout", "target_modules")})

    rows, bo = dung_hang(img_root=a.images, n=a.n_prompt, dai_nhat=(50 if a.probe else 0))
    print(f"câu nhắc: {len(rows)} · bỏ: {bo} · n_char trung vị {sorted(r['n_char'] for r in rows)[len(rows)//2]} max {max(r['n_char'] for r in rows)}")
    thieu = [r["image"] for r in rows if not os.path.exists(r["image"])]
    assert not thieu, f"⛔ thiếu {len(thieu)} ảnh, vd {thieu[:2]}"
    ds = to_hf(rows)
    json.dump([r["key"] for r in rows], open(os.path.join(a.out, "prompt_keys.json"), "w"))

    args = GRPOConfig(
        output_dir=a.out, seed=SEED, bf16=True, gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        num_generations=a.G, per_device_train_batch_size=a.G,
        gradient_accumulation_steps=a.accum,          # steps_per_generation mặc định = accum ⇒ mỗi lượt sinh = accum câu nhắc × G
        max_completion_length=128, temperature=a.temp, beta=a.beta,
        learning_rate=a.lr, lr_scheduler_type="constant_with_warmup", warmup_steps=10,
        max_steps=(20 if a.probe else a.max_steps), num_train_epochs=1,
        mask_truncated_completions=True, log_completions=a.probe, num_completions_to_print=2,   # bảng mẫu chỉ ở probe
        logging_steps=1, save_steps=(10**9 if a.probe else 50), save_total_limit=3,
        report_to="none", remove_unused_columns=False, dataloader_num_workers=2,
        disable_tqdm=True,                            # in log dạng dict ra stdout (PrinterCallback), không ngập log kiểu tqdm
        max_grad_norm=1.0,
    )
    print("GRPOConfig:", {k: getattr(args, k) for k in (
        "num_generations", "per_device_train_batch_size", "gradient_accumulation_steps",
        "generation_batch_size", "steps_per_generation", "max_completion_length", "temperature",
        "beta", "learning_rate", "loss_type", "scale_rewards", "epsilon", "num_iterations",
        "max_steps", "mask_truncated_completions")})
    trainer = GRPOTrainer(model=model, reward_funcs=REWARDS, args=args, train_dataset=ds,
                          processing_class=proc)
    t0 = time.time()
    trainer.train(resume_from_checkpoint=a.resume)
    dt = time.time() - t0
    print(f"xong {args.max_steps} bước · {dt/60:.1f} phút · {dt/args.max_steps:.1f} s/bước")
    trainer.save_model(os.path.join(a.out, "final"))
    json.dump(trainer.state.log_history, open(os.path.join(a.out, "log_history.json"), "w"), indent=1)
    print("→", a.out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--train", action="store_true")
    ap.add_argument("--adapter"); ap.add_argument("--out")
    ap.add_argument("--images", default=None)
    ap.add_argument("--n-prompt", type=int, default=N_PROMPT)
    ap.add_argument("--G", type=int, default=4)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--temp", type=float, default=1.0)
    ap.add_argument("--beta", type=float, default=0.04)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--max-steps", type=int, default=500)
    ap.add_argument("--resume", default=None)
    a = ap.parse_args()
    if a.selftest:
        selftest(); return
    assert a.adapter and a.out, "cần --adapter và --out"
    os.makedirs(a.out, exist_ok=True)
    train(a)


if __name__ == "__main__":
    main()
