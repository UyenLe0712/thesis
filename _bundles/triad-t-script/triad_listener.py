# -*- coding: utf-8 -*-
"""Listener độc lập cho TRIAD-T (action 273 §2.3): ShowUI-2B đọc một câu trên toàn màn và trả điểm.

python triad_listener.py --calls calls_poa.jsonl --img-root C1DATA --out listener_showui.jsonl [--n 10]

· Câu nhắc + min/max_pixels + bộ xử lý BÊ NGUYÊN thẻ mô hình `showlab/ShowUI-2B`
  (processor lấy từ `Qwen/Qwen2-VL-2B-Instruct`). Đầu ra [x, y] thang 0–1 ⇒ nhân 1000.
· ⛔ fp32: ShowUI-2B ở fp16 trên T4 từng ra NaN (CLAUDE.md, mục bộ trỏ thứ hai). 2B fp32 ≈ 9 GB, vừa T4.
· Giải mã greedy ⇒ tất định ⇒ (bước, câu) trùng chỉ gọi một lần.
· Ghi dần + flush; chạy lại tự bỏ qua (bước, câu) đã có. In nhịp mỗi 50 lời gọi.
· Luật đọc toạ độ khoá trước: hai số đầu, cả hai trong [0, 1] ⇒ ok; còn lại ⇒ parse lỗi (giữ raw).
"""

import os, re, sys, json, time, argparse

os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

MODEL = "showlab/ShowUI-2B"
PROC = "Qwen/Qwen2-VL-2B-Instruct"
MIN_PIX, MAX_PIX = 256 * 28 * 28, 1344 * 28 * 28
SYSTEM = ("Based on the screenshot of the page, I give a text description and you give its corresponding "
          "location. The coordinate represents a clickable location [x, y] for an element, which is a "
          "relative coordinate on the screenshot, scaled from 0 to 1.")
SO = re.compile(r"-?\d+(?:\.\d+)?")


def doc(raw):
    m = SO.findall(raw or "")
    if len(m) < 2:
        return None
    x, y = float(m[0]), float(m[1])
    if not (0 <= x <= 1 and 0 <= y <= 1):
        return None
    return [round(x * 1000, 2), round(y * 1000, 2)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calls", required=True)
    ap.add_argument("--img-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--dtype", default="float32", choices=["float32", "bfloat16", "float16"])
    a = ap.parse_args()

    import torch
    from PIL import Image
    from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

    calls = [json.loads(l) for l in open(a.calls, encoding="utf-8")]
    if a.n:
        calls = calls[:a.n]
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out, encoding="utf-8"):
            try:
                d = json.loads(l)
                done.add((d["episode_id"], d["step_id"], d["sent"]))
            except ValueError:
                pass
    viec = [c for c in calls if (c["episode_id"], c["step_id"], c["sent"]) not in done]
    print(f"[listener] {MODEL} · dtype {a.dtype} · {len(calls)} lời gọi · đã có {len(done)} · còn {len(viec)}",
          flush=True)
    if not viec:
        return

    proc = AutoProcessor.from_pretrained(PROC, min_pixels=MIN_PIX, max_pixels=MAX_PIX)
    ip = proc.image_processor            # transformers mới nuốt min/max_pixels im lặng (bài học UI-Venus 20/8)
    if isinstance(getattr(ip, "size", None), dict):
        ip.size = {"shortest_edge": MIN_PIX, "longest_edge": MAX_PIX}
    ip.min_pixels, ip.max_pixels = MIN_PIX, MAX_PIX
    print(f"[listener] image_processor min={ip.min_pixels} max={ip.max_pixels} size={getattr(ip, 'size', None)}",
          flush=True)
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL, torch_dtype=getattr(torch, a.dtype), device_map="cuda", attn_implementation="sdpa").eval()
    print(f"[listener] dtype thật {next(model.parameters()).dtype} · GPU {torch.cuda.get_device_name(0)}",
          flush=True)

    t0, n_ok, anh = time.time(), 0, {}
    with open(a.out, "a", encoding="utf-8") as fo:
        for j, c in enumerate(viec):
            p = os.path.join(a.img_root, c["image"])
            if p not in anh:
                anh = {p: Image.open(p).convert("RGB")}      # calls xếp theo bước ⇒ giữ một ảnh
            img = anh[p]
            msg = [{"role": "user", "content": [
                {"type": "text", "text": SYSTEM},
                {"type": "image"},
                {"type": "text", "text": c["sent"]}]}]
            text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
            inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
            t1 = time.time()
            with torch.no_grad():
                g = model.generate(**inp, max_new_tokens=32, do_sample=False, use_cache=True)
            raw = proc.decode(g[0][len(inp["input_ids"][0]):], skip_special_tokens=True)
            xy = doc(raw)
            n_ok += xy is not None
            fo.write(json.dumps({**{k: c[k] for k in ("episode_id", "step_id", "nguon", "sent")},
                                 "raw": raw, "xy01": [v / 1000 for v in xy] if xy else None, "xy": xy,
                                 "ok": xy is not None, "sec": round(time.time() - t1, 3)},
                                ensure_ascii=False) + "\n")
            fo.flush()
            if j < 3 or (j + 1) % 50 == 0 or j + 1 == len(viec):
                dt = time.time() - t0
                print(f"[listener] {j + 1}/{len(viec)} · đọc được {n_ok}/{j + 1} · {dt / (j + 1):.2f} s/lời gọi · "
                      f"còn ~{dt / (j + 1) * (len(viec) - j - 1) / 60:.0f} phút · VRAM đỉnh "
                      f"{torch.cuda.max_memory_allocated() / 2**30:.2f} GiB · raw={raw[:40]!r}", flush=True)
    print(f"[listener] XONG · đọc được {n_ok}/{len(viec)} lời gọi mới", flush=True)


if __name__ == "__main__":
    main()
