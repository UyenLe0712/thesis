# -*- coding: utf-8 -*-
"""SA-SPICE-v3 — sinh greedy trên DEV-v3 (2.223 bước, mọi loại thao tác) cho SFT-cont hoặc SFT-cont + adapter GRPO.

Mô hình: sft_cont_merged (sa3_grpo.py --hoa, fp16 trên T4, đã kiểm greedy trùng kernel 1) [+ adapter GRPO ở gốc điểm lưu,
base_model_name_or_path = /tmp/sft_cont_merged]. Câu nhắc, ảnh, độ dài, cách giải mã giống hệt sa3_mau.py (greedy, max_new 96).
In cấu hình thật sự dùng và |lora_B| của adapter đã nạp (phải > 0). Ghi dần, nối tiếp được.

  python sa3_dev.py --data D --merged /tmp/sft_cont_merged --out dev_sftcont.jsonl
  python sa3_dev.py --data D --merged /tmp/sft_cont_merged --adapter D/ad/sa_ck500 --out dev_sa_ck500.jsonl [--n 3]
"""
import os, sys, json, time, argparse

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_branch_data import prompt_body, SYS  # noqa: E402

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="thư mục có dev_v3.jsonl, ocr_dev.jsonl, images/")
    ap.add_argument("--merged", required=True); ap.add_argument("--adapter", default="")
    ap.add_argument("--out", required=True); ap.add_argument("--n", type=int, default=0)
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(os.path.join(a.data, "dev_v3.jsonl"), encoding="utf-8")]
    assert len(rows) == 2223, len(rows)
    if a.n:
        rows = rows[: a.n]
    ocr = {}
    for l in open(os.path.join(a.data, "ocr_dev.jsonl"), encoding="utf-8"):
        o = json.loads(l); ocr[o["image"]] = o
    miss = [r["image"] for r in rows if r["image"] not in ocr or not os.path.exists(os.path.join(a.data, r["image"]))]
    assert not miss, f"⛔ thiếu ảnh/OCR: {miss[:3]} ({len(miss)})"
    done = set()
    if os.path.exists(a.out):
        done = {(d["episode_id"], d["step_id"]) for d in map(json.loads, open(a.out, encoding="utf-8"))}
    todo = [r for r in rows if (r["episode_id"], r["step_id"]) not in done]
    print(f"[dữ liệu] {a.data}/dev_v3.jsonl · {len(rows)} bước · đã có {len(done)} · còn {len(todo)}", flush=True)
    if not todo:
        print("Xong sẵn.", flush=True); return

    import torch, transformers
    from PIL import Image
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor

    dt = torch.float16
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): dt}
    proc = AutoProcessor.from_pretrained(BASE, min_pixels=200704, max_pixels=1003520)
    m = Qwen2_5_VLForConditionalGeneration.from_pretrained(a.merged, device_map={"": 0}, **kw)
    if a.adapter:
        from peft import PeftModel
        cfg = json.load(open(os.path.join(a.adapter, "adapter_config.json")))
        assert cfg["base_model_name_or_path"].endswith("sft_cont_merged"), cfg["base_model_name_or_path"]
        m = PeftModel.from_pretrained(m, a.adapter)
        B = [p.float().norm().item() for n, p in m.named_parameters() if "lora_B" in n]
        print(f"[nạp adapter] {a.adapter} · {len(B)} lora_B · |lora_B| TB {sum(B) / len(B):.4f}", flush=True)
        assert len(B) == 252 and sum(B) > 0, "⛔ adapter không nạp đúng"
    m.eval()
    gen = dict(max_new_tokens=96, do_sample=False, temperature=None, top_p=None, top_k=None, use_cache=True, remove_invalid_values=True)
    print(f"[cấu hình] dtype {dt} · torch {torch.__version__} · transformers {transformers.__version__} · adapter {a.adapter or 'không'} · {gen}", flush=True)

    out = open(a.out, "a", encoding="utf-8"); t0 = time.time()
    for i, r in enumerate(todo):
        body = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.data, r["image"])).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to("cuda:0")
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = m.generate(**inp, **gen)
        y = g[0][L:]
        cut = int(len(y) >= 96 and (y != proc.tokenizer.eos_token_id).all().item())
        out.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "action_type": r["action"]["action_type"],
                              "package": r.get("package", ""), "gold": r["target_instruction"],
                              "pred": proc.decode(y, skip_special_tokens=True).strip(), "cut96": cut}, ensure_ascii=False) + "\n")
        out.flush()
        if (i + 1) % 25 == 0 or i == len(todo) - 1:
            el = time.time() - t0
            print(f"  {i + 1}/{len(todo)} · {el / 60:.1f} phút · {el / (i + 1):.2f} s/bước · còn ~{el / (i + 1) * (len(todo) - i - 1) / 60:.0f} phút", flush=True)
    out.close(); print("XONG", flush=True)


if __name__ == "__main__":
    main()
