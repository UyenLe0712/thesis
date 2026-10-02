# -*- coding: utf-8 -*-
"""
Sinh greedy trên TẬP KIỂM cho GRPO SPICE (action 258, 1/10/2026). Cùng đường với `grpo_spice.py --gen`
đã dùng chấm val: hoà S1 → `s1_merged`, gắn điểm lưu GRPO lên bản hoà, fp16, greedy, 96 token,
câu nhắc `prompt_body + SYS` của `build_branch_data.py`, ảnh đứng trước chữ.
⛔ Không gắn LoRA lên Qwen gốc (đường `infer_branch.py`) — ra một mô hình khác mô hình đã chấm val.

Chép từ ô 3 của 258, sửa hai chỗ: `grpo_spice.map` (lỗi chép ảnh) → `grpo_spice.nap`; kiểm hoà so
trên bước CLICK (là bước sẽ chấm) thay vì 20 bản ghi đầu bất kỳ.

  # kiểm hoà, không gắn điểm lưu: 20 bước click đầu, so preds_s1_seed101
  python gen_test_grpo.py --bundle B --merged M --recs test.jsonl --ocr ocr.jsonl --images IMG \
         --tap-only --s1 preds_s1_seed101.jsonl --n 20 --out kiem_hoa_test.jsonl --no-q4
  # lượt thật: 4.463 bước click, nối tiếp được
  python gen_test_grpo.py --bundle B --merged M --ckpt CK --recs test.jsonl --ocr ocr.jsonl \
         --images IMG --tap-only --out pred_ck500_test.jsonl --no-q4
  # chạy khô trên CPU (máy nhà): chỉ dựng câu nhắc, không nạp mô hình
  python gen_test_grpo.py --bundle x --merged x --recs ... --ocr ... --images ... --tap-only --dry --out /dev/null
"""
import os, sys, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_branch_data import prompt_body, SYS

TAPT = ("click", "long_press")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--merged", required=True)
    ap.add_argument("--ckpt", default=None)
    ap.add_argument("--recs", required=True)
    ap.add_argument("--ocr", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--s1", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--tap-only", action="store_true")
    ap.add_argument("--no-q4", dest="q4", action="store_false")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.adapter = os.path.join(a.bundle, "adapter_s1_seed101")

    rows = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    assert len(rows) == 6958, f"⛔ test.jsonl có {len(rows)} dòng, cần 6958"
    if a.tap_only:
        rows = [r for r in rows if r["action"].get("action_type") in TAPT and "x" in r["action"]]
        assert len(rows) == 4463, len(rows)
    if a.n:
        rows = rows[:a.n]
    ocr = {o["image"]: o for o in map(json.loads, open(a.ocr, encoding="utf-8"))}
    thieu = [r["image"] for r in rows if not os.path.exists(os.path.join(a.images, os.path.basename(r["image"])))]
    print(f"[dữ liệu] {a.recs} · {len(rows)} bước · thiếu OCR {sum(r['image'] not in ocr for r in rows)}"
          f" · thiếu ảnh {len(thieu)}", flush=True)
    assert not thieu, f"⛔ thiếu ảnh, ví dụ {thieu[:3]}"

    def msg_of(r):
        body = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        return [{"role": "system", "content": SYS},
                {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]

    if a.dry:
        m = msg_of(rows[0])
        print("[khô] câu nhắc bước đầu:", json.dumps(m, ensure_ascii=False)[:700], flush=True)
        return

    import grpo_spice
    proc, model, _ = grpo_spice.nap(a)
    if a.ckpt:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.ckpt)
        print("[điểm lưu]", a.ckpt, flush=True)
    else:
        print("[điểm lưu] KHÔNG gắn — đây là S1 hoà", flush=True)
    model.eval()

    done = set()
    if os.path.exists(a.out):
        done = {(d["episode_id"], d["step_id"]) for d in map(json.loads, open(a.out, encoding="utf-8"))}
    print(f"[nối tiếp] đã có {len(done)}/{len(rows)}", flush=True)

    import torch
    from PIL import Image
    fo = open(a.out, "a", encoding="utf-8")
    t0, moi = time.time(), 0
    for i, r in enumerate(rows):
        k = (r["episode_id"], r["step_id"])
        if k in done:
            continue
        text = proc.apply_chat_template(msg_of(r), tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.images, os.path.basename(r["image"]))).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                               temperature=None, top_p=None, top_k=None)
        s = proc.decode(g[0][L:], skip_special_tokens=True).strip()
        fo.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": s}, ensure_ascii=False) + "\n")
        fo.flush()
        moi += 1
        if (i + 1) % 50 == 0:
            dt = time.time() - t0
            print(f"  {i+1}/{len(rows)} · {dt/60:.1f} phút · {dt/moi:.2f} s/bước · {s[:60]!r}", flush=True)
    fo.close()

    P = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(a.out, encoding="utf-8"))}
    print(f"[xong] {len(P)} câu · rỗng {sum(not v for v in P.values())}", flush=True)
    if a.s1:
        S = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(a.s1, encoding="utf-8"))}
        same = sum(P[k] == S.get(k) for k in P)
        print(f"[kiểm hoà] {same}/{len(P)} trùng preds_s1_seed101", flush=True)


if __name__ == "__main__":
    main()
