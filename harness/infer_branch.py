# -*- coding: utf-8 -*-
"""
Chạy một nhánh đã huấn luyện trên TẬP KIỂM, sinh câu hướng dẫn để đem chấm.

Mắt xích giữa huấn luyện và chấm điểm: nạp mô hình gốc + bộ trọng số LoRA của một
nhánh, chạy qua toàn bộ tập kiểm, cắt bỏ phần khai báo, lưu câu ra tệp cho
`metric_exec.py` chấm.

BA ĐIỀU KIỆN PHẢI GIỮ, nếu phá là hỏng cả phép so:

  1. Đầu vào lúc chấm phải GIỐNG HỆT lúc dạy. Mã dựng câu nhắc ở đây import thẳng
     từ `build_branch_data.py` chứ không chép lại, để không có đường nào lệch nhau.
  2. Cắt bỏ phần `<desc>…</desc>` trước khi chấm — người dùng không bao giờ thấy nó,
     và bộ trỏ cũng không được thấy, kẻo thành đưa đáp án cho giám khảo.
  3. Mọi nhánh sinh với cùng tham số sinh (greedy, cùng độ dài tối đa). Sinh ngẫu
     nhiên sẽ thêm một nguồn nhiễu nữa vào giữa hai nhánh.

Chạy trên máy có GPU:
  python harness/infer_branch.py --adapter /workspace/ckpt/s1_seed101 --out preds_s1_seed101.jsonl
  python harness/infer_branch.py --adapter ... --limit 50        # thử nhanh trước
  python harness/infer_branch.py --no-adapter --out preds_base.jsonl   # mô hình gốc, chưa huấn luyện
"""
import os, sys, json, re, argparse, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_branch_data import prompt_of, SYS      # dùng chung mã dựng câu nhắc

TEST = os.path.join(HERE, "dg1_cache", "test_ac")
BASE = "Qwen/Qwen2.5-VL-3B-Instruct"


def strip_desc(s):
    """Bỏ phần khai báo, chỉ giữ câu hướng dẫn.

    Ba dạng phải xử: khai báo đóng thẻ đủ; khai báo bị cắt cụt do chạm trần độ dài
    (thẻ mở mà không có thẻ đóng — khi đó coi như mô hình chưa kịp viết câu);
    và mô hình không sinh khai báo nào.
    """
    if "</desc>" in s:
        s = s.split("</desc>", 1)[1]
    elif "<desc>" in s:
        s = re.sub(r"<desc>.*", "", s, flags=re.S)
    return s.strip().split("\n")[0].strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", default=None, help="thư mục LoRA của nhánh")
    ap.add_argument("--no-adapter", action="store_true", help="chạy mô hình gốc, chưa huấn luyện")
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--max-new", type=int, default=96)
    ap.add_argument("--batch", type=int, default=8)
    a = ap.parse_args()
    if not a.adapter and not a.no_adapter:
        sys.exit("Phải cho --adapter, hoặc --no-adapter nếu cố ý chạy mô hình gốc.")

    import torch
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from PIL import Image

    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")]
    ocr = {}
    op = os.path.join(TEST, "ocr.jsonl")
    if os.path.exists(op):
        with open(op, encoding="utf-8") as f:
            for line in f:
                o = json.loads(line)
                ocr[o["image"]] = o
    else:
        print("CẢNH BÁO: chưa có ocr.jsonl của tập kiểm — đầu vào sẽ THIẾU phần chữ đọc "
              "được, khác lúc dạy. Chạy prep_ocr_train.py --split test trước.")
    if a.limit:
        recs = recs[:a.limit]

    print(f"Nạp {a.base}" + (f" + LoRA {a.adapter}" if a.adapter else " (mô hình gốc)"))
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        a.base, torch_dtype=torch.bfloat16, device_map="auto")
    if a.adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.adapter)
    model.eval()
    proc = AutoProcessor.from_pretrained(a.base)

    out = open(a.out, "w", encoding="utf-8")
    t0, done = time.time(), 0
    for i in range(0, len(recs), a.batch):
        chunk = recs[i:i + a.batch]
        msgs, imgs = [], []
        for r in chunk:
            # tập kiểm dùng khoá gold_instruction; dựng bản ghi giống tập dạy để
            # câu nhắc đi qua đúng một hàm duy nhất
            rr = {"goal": r["goal"], "history": r.get("history") or []}
            im = Image.open(os.path.join(TEST, r["image"])).convert("RGB")
            imgs.append(im)
            msgs.append([{"role": "system", "content": SYS},
                         {"role": "user", "content": prompt_of(rr, ocr.get(r["image"]))}])
        texts = [proc.apply_chat_template(m, tokenize=False, add_generation_prompt=True)
                 for m in msgs]
        inputs = proc(text=texts, images=imgs, return_tensors="pt",
                      padding=True).to(model.device)
        with torch.no_grad():
            gen = model.generate(**inputs, max_new_tokens=a.max_new,
                                 do_sample=False, temperature=None, top_p=None)
        for r, g, inp in zip(chunk, gen, inputs["input_ids"]):
            txt = proc.decode(g[len(inp):], skip_special_tokens=True)
            out.write(json.dumps({
                "episode_id": r["episode_id"], "step_id": r["step_id"],
                "image": r["image"], "app": r.get("app", ""),
                "gold_instruction": r["gold_instruction"], "action": r["action"],
                "raw": txt.strip(),            # nguyên văn, giữ để soi lỗi
                "pred": strip_desc(txt),       # câu đem chấm
            }, ensure_ascii=False) + "\n")
        done += len(chunk)
        if done % 80 < a.batch:
            sp = done / max(time.time() - t0, 1)
            print(f"  {done}/{len(recs)}  ({sp:.1f} bước/giây, còn ~{(len(recs)-done)/max(sp,.01)/60:.0f} phút)")
    out.close()
    print(f"Xong {done} bước → {a.out}")


if __name__ == "__main__":
    main()
