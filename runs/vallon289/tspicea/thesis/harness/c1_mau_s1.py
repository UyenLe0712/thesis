# -*- coding: utf-8 -*-
"""Cổng C1 (report/208 §4) — S1/101 sinh 1 câu greedy + K câu lấy mẫu cho N bước val cố định.

Chạy trên Kaggle T4 (0 đồng), dùng lại dataset `fgrb-p1-bundle` (adapter S1/101 + ảnh + OCR + 1.567
bước val). Đọc kết quả trên máy nhà bằng `harness/c1_doc.py` (CPU).

    python c1_mau_s1.py --bundle <BUNDLE> --out /kaggle/working/c1_mau.jsonl
    python c1_mau_s1.py --bundle <BUNDLE> --out /kaggle/working/c1_thu.jsonl --n 5   # thử nhanh

Lời nhắc dựng bằng ĐÚNG `build_branch_data.prompt_body` + `SYS` (đóng kèm trong dataset script),
cùng ngân sách điểm ảnh và `max_new_tokens=96` như `infer_branch.py` ⇒ câu greedy là câu S1 thật.
Câu lấy mẫu dùng cấu hình gần với lượt GRPO sẽ chạy: nhiệt độ 1,0, top_p 1,0, top_k 0,
repetition_penalty 1,0 — script IN RA cấu hình sinh thật sự dùng (bài học 20/8: kiểm dòng in, đừng
kiểm mã nguồn). Không mở test.jsonl hay tệp điểm test nào. Ghi dần, nối tiếp được.
"""
import os, sys, json, time, random, argparse

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_branch_data import prompt_body, SYS  # noqa: E402

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
SEED_CHON = 20260927


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--temp", type=float, default=1.0)
    ap.add_argument("--max-new", type=int, default=96)
    a = ap.parse_args()

    va = [json.loads(l) for l in open(os.path.join(a.bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    assert len(va) == 1567, f"val phải 1.567 dòng, đang {len(va)}"
    rows = random.Random(SEED_CHON).sample(va, 400)[: a.n]
    ocr = {}
    for l in open(os.path.join(a.bundle, "ocr.jsonl"), encoding="utf-8"):
        o = json.loads(l)
        ocr[o["image"]] = o
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out, encoding="utf-8"):
            d = json.loads(l)
            done.add((d["episode_id"], d["step_id"]))
    todo = [r for r in rows if (r["episode_id"], r["step_id"]) not in done]
    print(f"[dữ liệu] val={len(va)} · chọn {len(rows)} bước (seed {SEED_CHON}) · đã có {len(done)} · "
          f"còn {len(todo)} · ocr_keys={len(ocr)}", flush=True)
    if not todo:
        print("Xong sẵn.", flush=True)
        return

    import torch
    from PIL import Image
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from peft import PeftModel
    import transformers

    dt = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): dt}
    proc = AutoProcessor.from_pretrained(BASE, min_pixels=200704, max_pixels=1003520)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(BASE, device_map={"": 0}, **kw)
    model = PeftModel.from_pretrained(model, os.path.join(a.bundle, "adapter_s1_seed101"))
    model.eval()

    samp = dict(do_sample=True, temperature=a.temp, top_p=1.0, top_k=0, repetition_penalty=1.0,
                num_return_sequences=a.k, max_new_tokens=a.max_new, use_cache=True)
    gc = model.generation_config
    print(f"[cấu hình] dtype={dt} · greedy: do_sample=False, repetition_penalty(mặc định model)="
          f"{getattr(gc, 'repetition_penalty', None)}, max_new={a.max_new} · lấy mẫu: {samp}", flush=True)

    out = open(a.out, "a", encoding="utf-8")
    t0 = time.time()
    torch.manual_seed(101)
    for i, r in enumerate(todo):
        rr = {"goal": r["goal"], "history": r.get("history") or []}
        body = prompt_body(rr, ocr.get(r["image"]))
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=a.max_new, use_cache=True, do_sample=False,
                               temperature=None, top_p=None, top_k=None)
            s = model.generate(**inp, **samp)
        greedy = proc.decode(g[0][L:], skip_special_tokens=True).strip()
        mau = [proc.decode(x[L:], skip_special_tokens=True).strip() for x in s]
        out.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"],
                              "action_type": (r.get("action") or {}).get("action_type"),
                              "gold": r["target_instruction"], "greedy": greedy, "mau": mau},
                             ensure_ascii=False) + "\n")
        out.flush()
        if (i + 1) % 20 == 0 or i == len(todo) - 1:
            el = time.time() - t0
            print(f"  {i+1}/{len(todo)} · {el/60:.1f} phút · còn ~{el/(i+1)*(len(todo)-i-1)/60:.1f} phút"
                  f" · ví dụ greedy: {greedy[:60]!r}", flush=True)
    out.close()
    print("XONG", flush=True)


if __name__ == "__main__":
    main()
