# -*- coding: utf-8 -*-
"""Sinh ô KHAI BÁO bằng chính checkpoint S2, trên màn TẬP DẠY.

Vì sao có file này: `desc_neg` hiện tại do `nearest_other()` ĐOÁN — phần tử cùng vai trò
gần nhất. Đo 25/8 (`report/120` Mục 4.2): chỉ **7–10%** lỗi tên của mô hình rơi đúng vào
hàng xóm đó, tức heuristic bỏ sót ~90% khối lỗi thật. Script này thay việc ĐOÁN bằng việc
HỎI: cho S2 tự sinh khai báo trên đúng những màn nó được dạy, rồi lấy chính chỗ nó đoán
sai làm vế âm.

⚠️ ĐIỂM QUAN TRỌNG NHẤT VỀ TÍNH ĐÚNG ĐẮN: câu nhắc **không được dựng lại**. Script lấy
nguyên `messages[0]` (system) và `messages[1]` (user) từ `branches/s2.json` — tức đúng
chuỗi mà mô hình đã thấy lúc train. Dựng lại câu nhắc bằng tay là mở đường cho một khác
biệt vô hình giữa lúc dạy và lúc hỏi, rồi ta đổ oan cho mô hình.

Chỉ sinh tới hết `</desc>`, KHÔNG sinh câu hướng dẫn — rẻ hơn nhiều và ta không cần câu.

    python3 harness/sinh_desc_train.py --adapter /content/drive/.../ckpt/s2_seed101 \
        --out /content/desc_train_s2.jsonl --limit 14000

Ghi dần + xả đệm mỗi lô + nối tiếp được, cùng cơ chế `infer_branch.py` (bài học 11/8:
mất máy ở 90% công việc, hai lần trong hai ngày).
"""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
BR   = os.path.join(ROOT, "branches")
BASE = "Qwen/Qwen2.5-VL-3B-Instruct"


def pick_dtype():
    """Bản sao có chủ đích của `infer_branch.pick_dtype` — bf16 chỉ chạy thật từ Ampere.
    ĐỪNG hỏi torch.cuda.is_bf16_supported(): T4 trả True qua đường giả lập (đo 9/8)."""
    import torch
    if not torch.cuda.is_available():
        return torch.float32
    return torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16


def dtype_kw():
    import transformers
    major = int(transformers.__version__.split(".")[0])
    return {("dtype" if major >= 5 else "torch_dtype"): pick_dtype()}


def khoa_anh(p):
    """ep7057_s1.png -> (7057, 1). Khoá duy nhất nối s2.json với descriptors.jsonl."""
    t = os.path.basename(p)
    if not t.startswith("ep") or "_s" not in t:
        return None
    a, b = t[2:].split("_s", 1)
    try:
        return int(a), int(b.split(".")[0])
    except ValueError:
        return None


def dung_text(msgs, proc):
    """Dựng chuỗi cho processor của Qwen từ messages kiểu LLaMA-Factory.

    ⛔ ĐÃ NỔ 25/8: đưa thẳng `messages` của s2.json vào `apply_chat_template` cho
    `ValueError: Image features and image tokens do not match, tokens: 0`. Lý do: lúc DẠY,
    LLaMA-Factory nhận chuỗi "<image>" rồi tự thay bằng token ảnh; còn chat template của Qwen
    **in nguyên văn** chuỗi đó. Phải tách làm hai phần đúng như `infer_branch.py:481-484`.

    Phần chữ lấy NGUYÊN VĂN từ s2.json (bỏ đúng sáu ký tự "<image>", giữ cả "\n" đứng đầu),
    nên chuỗi render ra trùng đúng bản lúc dạy — đó là lý do script này đọc s2.json thay vì
    dựng lại câu nhắc.
    """
    sysm = msgs[0]["content"]
    user = msgs[1]["content"]
    if not user.startswith("<image>"):
        raise ValueError(f"câu nhắc không mở đầu bằng <image>: {user[:60]!r}")
    body = user[len("<image>"):]
    return proc.apply_chat_template(
        [{"role": "system", "content": sysm},
         {"role": "user", "content": [{"type": "image"},
                                      {"type": "text", "text": body}]}],
        tokenize=False, add_generation_prompt=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", required=True, help="thư mục LoRA của S2")
    ap.add_argument("--out", required=True)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--limit", type=int, default=0, help="0 = tất cả bước có khai báo vàng")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--max-new", type=int, default=64,
                    help="chỉ cần hết </desc>; 64 token đủ cho ô khai báo dài nhất")
    ap.add_argument("--img-root", default="", help="thay tiền tố đường dẫn ảnh nếu khác máy")
    a = ap.parse_args()

    import torch
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from PIL import Image

    # ── chỉ lấy bước CÓ khai báo vàng: đó là quần thể duy nhất chấm đúng/sai được ──
    gold = {}
    with open(os.path.join(ROOT, "descriptors.jsonl"), encoding="utf-8") as f:
        for l in f:
            d = json.loads(l)
            gold[(d["episode_id"], d["step_id"])] = d
    s2 = json.load(open(os.path.join(BR, "s2.json"), encoding="utf-8"))

    recs = []
    for m in s2:
        k = khoa_anh(m["images"][0])
        if k is None or k not in gold:
            continue
        if "<desc>" not in m["messages"][2]["content"]:
            continue                      # bước không-chạm, không có ô khai báo
        recs.append({"ep": k[0], "step": k[1], "img": m["images"][0],
                     "msgs": m["messages"][:2]})
    print(f"bước có khai báo vàng trong s2.json: {len(recs)}", flush=True)
    if a.limit:
        recs = recs[:a.limit]

    # ── NỐI TIẾP: đọc tệp cũ, loại dòng ghi dở, bỏ qua bước đã xong ──
    xong = set()
    if os.path.exists(a.out):
        sach = []
        for line in open(a.out, encoding="utf-8"):
            try:
                o = json.loads(line)
            except Exception:
                continue                  # dòng đứt lúc mất máy
            xong.add((o["ep"], o["step"])); sach.append(line)
        open(a.out, "w", encoding="utf-8").writelines(sach)
        recs = [r for r in recs if (r["ep"], r["step"]) not in xong]
        print(f"Nối tiếp: đã có {len(xong)} bước, còn {len(recs)}", flush=True)
        if not recs:
            print(f"Xong sẵn {len(xong)} bước → {a.out}", flush=True); return

    print(f"Nạp {a.base} + LoRA {a.adapter}", flush=True)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        a.base, device_map="auto", **dtype_kw())
    from peft import PeftModel
    model = PeftModel.from_pretrained(model, a.adapter).eval()
    # Ba chỗ PHẢI khớp lúc dạy, sai một chỗ là kết quả lệch mà không rõ vì sao
    proc = AutoProcessor.from_pretrained(a.base, min_pixels=200704, max_pixels=1003520)
    proc.tokenizer.padding_side = "left"

    # ⚡ TIỀN BAY 5 giây: dựng thử một chuỗi và ĐẾM token ảnh. Sai thì chết ở đây,
    #    không phải sau khi đã nạp 7,5 GB trọng số và mã hoá cả lô.
    thu = dung_text(recs[0]["msgs"], proc)
    n_vis = thu.count("<|image_pad|>") + thu.count("<|vision_start|>")
    print(f"tiền bay · token ảnh trong chuỗi: {n_vis} (phải > 0)", flush=True)
    print(f"          80 ký tự đầu: {thu[:80]!r}", flush=True)
    assert n_vis > 0, ("⛔ chuỗi KHÔNG có token ảnh — processor sẽ báo "
                       "'tokens: 0, features: N'. Kiểm lại dung_text().")

    out = open(a.out, "a", encoding="utf-8")
    t0, done = time.time(), 0
    for i in range(0, len(recs), a.batch):
        chunk = recs[i:i + a.batch]
        texts, imgs = [], []
        for r in chunk:
            p = r["img"]
            if a.img_root:
                p = os.path.join(a.img_root, os.path.basename(p))
            imgs.append(Image.open(p).convert("RGB"))
            texts.append(dung_text(r["msgs"], proc))
        enc = proc(text=texts, images=imgs, return_tensors="pt",
                   padding=True).to(model.device)
        with torch.no_grad():
            # cùng cờ với infer_branch.py — use_cache đã kiểm 50/50 trùng tuyệt đối
            gen = model.generate(**enc, max_new_tokens=a.max_new, use_cache=True,
                                 do_sample=False, temperature=None, top_p=None)
        for r, g, n in zip(chunk, gen, enc["input_ids"]):
            s = proc.tokenizer.decode(g[len(n):], skip_special_tokens=True)
            d = ""
            if "<desc>" in s:
                d = "<desc>" + s.split("<desc>", 1)[1].split("</desc>", 1)[0] + "</desc>"
            out.write(json.dumps({"ep": r["ep"], "step": r["step"],
                                  "desc_pred": d, "raw": s[:300]},
                                 ensure_ascii=False) + "\n")
        out.flush()                       # mỗi lô một lần: mất máy thì mất nhiều nhất một lô
        done += len(chunk)
        if done % 80 == 0 or done == len(recs):
            sp = done / max(time.time() - t0, 1)
            print(f"  [{time.strftime('%H:%M:%S')}] {done}/{len(recs)} · {sp:.2f} bước/giây"
                  f" · còn ~{(len(recs)-done)/max(sp,1e-6)/60:.0f} phút", flush=True)
    out.close()
    print(f"Đã ghi {a.out}", flush=True)


if __name__ == "__main__":
    main()
