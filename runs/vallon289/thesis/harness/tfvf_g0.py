# -*- coding: utf-8 -*-
"""G0 của TFVF (report/237) — S1/101 đóng băng sinh greedy trên ảnh đã làm nét vùng đích.

Chạy trên Kaggle T4 (0 đồng) với dataset `fgrb-p1-bundle`, cùng 400 bước val của C1
(`random.Random(20260927).sample(val, 400)`). Chỉ biến đổi ảnh của bước click (249 bước). Ba chế độ:
  G  gold focus    tâm = điểm chạm vàng (x, y)
  F  false focus   tâm = ((x + W/2) mod W, (y + H/2) mod H), cùng renderer
  C  center focus  tâm = (W/2, H/2), cùng renderer
Chế độ O (ảnh gốc) KHÔNG sinh lại: dùng câu greedy của `runs/c1/c1_mau.jsonl`.

Renderer (hằng số khoá trong report/237 §3, không đổi sau khi thấy số):
  M(u,v) = 0.35 + 0.65·exp(−½((u−x)/(0.18W))² − ½((v−y)/(0.12H))²)
  I'     = M ⊙ I + (1 − M) ⊙ Blur₈(I)        Blur₈ = PIL GaussianBlur(radius=8) trên ảnh gốc
Ảnh giữ nguyên kích thước, lời nhắc dựng y hệt C1 (`build_branch_data.prompt_body` + `SYS`), cùng ngân
sách điểm ảnh và `max_new_tokens=96`. Toạ độ vàng chỉ dùng để chẩn đoán, không phải đầu vào hệ thống.

    python tfvf_g0.py --bundle <BUNDLE> --out /kaggle/working/tfvf_g0_thu.jsonl --n 5
    python tfvf_g0.py --bundle <BUNDLE> --out /kaggle/working/tfvf_g0.jsonl --n 400
    python tfvf_g0.py --bundle <BUNDLE> --chi-ve <THƯ_MỤC> --n 5     # chỉ vẽ ảnh G/F/C, không nạp model

`--n` cắt tiền tố của 400 bước đã chọn rồi mới lọc click. Ghi dần, nối tiếp được. Không mở test.
"""
import os, sys, json, time, random, argparse, hashlib

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
SEED_CHON = 20260927
SAN, BIEN = 0.35, 0.65          # sàn mặt nạ · biên độ
SX, SY = 0.18, 0.12             # σ theo bề ngang W và bề dọc H
BLUR = 8                        # bán kính GaussianBlur của PIL, đơn vị pixel ảnh gốc
CHE_DO = [("gold_focus", "G"), ("false_focus", "F"), ("center_focus", "C")]


def tam(mode, x, y, W, H):
    if mode == "G":
        return x, y
    if mode == "F":
        return (x + 0.5 * W) % W, (y + 0.5 * H) % H
    return 0.5 * W, 0.5 * H


def ve(img, cx, cy):
    """img: PIL RGB. Trả ảnh PIL RGB cùng cỡ, vùng quanh (cx, cy) giữ nét, ngoài vùng trộn ảnh mờ."""
    import numpy as np
    from PIL import ImageFilter, Image
    W, H = img.size
    u = np.arange(W, dtype=np.float32)[None, :]
    v = np.arange(H, dtype=np.float32)[:, None]
    M = SAN + BIEN * np.exp(-0.5 * ((u - cx) / (SX * W)) ** 2 - 0.5 * ((v - cy) / (SY * H)) ** 2)
    a = np.asarray(img, dtype=np.float32)
    b = np.asarray(img.filter(ImageFilter.GaussianBlur(radius=BLUR)), dtype=np.float32)
    o = M[..., None] * a + (1.0 - M[..., None]) * b
    return Image.fromarray(np.clip(np.rint(o), 0, 255).astype(np.uint8), "RGB")


def chon(bundle, n):
    va = [json.loads(l) for l in open(os.path.join(bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    assert len(va) == 1567, f"val phải 1.567 dòng, đang {len(va)}"
    r400 = random.Random(SEED_CHON).sample(va, 400)
    khoa = [(r["episode_id"], r["step_id"]) for r in r400]
    h400 = hashlib.sha256(json.dumps(khoa).encode()).hexdigest()[:16]
    ck = [r for r in r400[:n] if (r.get("action") or {}).get("action_type") == "click"]
    hck = hashlib.sha256(json.dumps([(r["episode_id"], r["step_id"]) for r in r400
                                     if r["action"]["action_type"] == "click"]).encode()).hexdigest()[:16]
    n_ck400 = sum(r["action"]["action_type"] == "click" for r in r400)
    print(f"[dữ liệu] val={len(va)} · 400 bước seed {SEED_CHON} · hash400={h400} · click trong 400 = "
          f"{n_ck400} (kỳ vọng 249) · hash_click={hck} · lượt này: tiền tố {n} ⇒ {len(ck)} click", flush=True)
    assert n_ck400 == 249, "DỪNG: số click trong 400 bước lệch 249"
    return ck


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--max-new", type=int, default=96)
    ap.add_argument("--chi-ve", help="chỉ vẽ ảnh G/F/C của các bước click rồi thoát, không nạp model")
    a = ap.parse_args()
    assert os.path.isdir(os.path.join(a.bundle, "adapter_s1_seed101")), "DỪNG: thiếu adapter_s1_seed101"
    print(f"[renderer] M = {SAN} + {BIEN}·exp(−½((u−x)/({SX}W))² − ½((v−y)/({SY}H))²) · "
          f"Blur = GaussianBlur(radius={BLUR}) · F = tâm dời nửa màn (mod W,H) · C = tâm màn", flush=True)
    rows = chon(a.bundle, a.n)
    from PIL import Image

    if a.chi_ve:
        os.makedirs(a.chi_ve, exist_ok=True)
        for r in rows:
            img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
            W, H = img.size
            assert (W, H) == (r["w"], r["h"]), (r["image"], img.size, r["w"], r["h"])
            x, y = r["action"]["x"], r["action"]["y"]
            for _, m in CHE_DO:
                cx, cy = tam(m, x, y, W, H)
                ve(img, cx, cy).save(os.path.join(a.chi_ve, f"ep{r['episode_id']}_s{r['step_id']}_{m}.png"))
            print(f"  vẽ ep{r['episode_id']}_s{r['step_id']} · ({x},{y}) trên {W}×{H}", flush=True)
        print("XONG (chỉ vẽ)", flush=True)
        return

    assert a.out, "cần --out"
    from build_branch_data import prompt_body, SYS
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
    print(f"[tiến độ] đã có {len(done)} · còn {len(todo)} · ocr_keys={len(ocr)} · "
          f"thiếu OCR {sum(r['image'] not in ocr for r in rows)}", flush=True)
    if not todo:
        print("Xong sẵn.", flush=True)
        return

    import torch
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from peft import PeftModel
    import transformers

    dt = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): dt}
    proc = AutoProcessor.from_pretrained(BASE, min_pixels=200704, max_pixels=1003520)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(BASE, device_map={"": 0}, **kw)
    model = PeftModel.from_pretrained(model, os.path.join(a.bundle, "adapter_s1_seed101"))
    model.eval()
    gc = model.generation_config
    print(f"[cấu hình] dtype={dt} · greedy do_sample=False · max_new={a.max_new} · "
          f"repetition_penalty(mặc định model)={getattr(gc, 'repetition_penalty', None)} · "
          f"pixels [200704, 1003520] · transformers {transformers.__version__}", flush=True)

    out = open(a.out, "a", encoding="utf-8")
    t0 = time.time()
    for i, r in enumerate(todo):
        rr = {"goal": r["goal"], "history": r.get("history") or []}
        body = prompt_body(rr, ocr.get(r["image"]))
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        W, H = img.size
        assert (W, H) == (r["w"], r["h"]), (r["image"], img.size, r["w"], r["h"])
        x, y = r["action"]["x"], r["action"]["y"]
        rec = {"episode_id": r["episode_id"], "step_id": r["step_id"], "action_type": "click",
               "gold": r["target_instruction"]}
        for ten, m in CHE_DO:
            cx, cy = tam(m, x, y, W, H)
            inp = proc(text=[text], images=[ve(img, cx, cy)], return_tensors="pt").to(model.device)
            L = inp["input_ids"].shape[1]
            with torch.no_grad():
                g = model.generate(**inp, max_new_tokens=a.max_new, use_cache=True, do_sample=False,
                                   temperature=None, top_p=None, top_k=None)
            rec[ten] = proc.decode(g[0][L:], skip_special_tokens=True).strip()
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        out.flush()
        if (i + 1) % 20 == 0 or i == len(todo) - 1:
            el = time.time() - t0
            print(f"  {i+1}/{len(todo)} · {el/60:.1f} phút · còn ~{el/(i+1)*(len(todo)-i-1)/60:.1f} phút · "
                  f"G: {rec['gold_focus'][:50]!r} · F: {rec['false_focus'][:50]!r}", flush=True)
    out.close()
    print("XONG", flush=True)


if __name__ == "__main__":
    main()
