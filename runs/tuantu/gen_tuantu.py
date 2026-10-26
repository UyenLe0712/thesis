# -*- coding: utf-8 -*-
"""
Sinh câu hướng dẫn TUẦN TỰ theo từng tác vụ, lịch sử là câu do chính mô hình sinh ở các bước trước
(việc #5 của report/322, 26/10/2026). Chép từ `gen_aitz.py` (cùng đường hoà S1 → gắn điểm lưu, fp16,
greedy, 96 token, câu nhắc `prompt_body + SYS`), chỉ đổi MỘT thứ: trường `history` của câu nhắc.

  --history self   lịch sử = câu mô hình đã sinh cho các bước trước của cùng tác vụ (mặc định)
  --history gold   lịch sử = câu chuẩn trong test.jsonl, tức đúng đường của lượt test cũ; dùng để kiểm
                   rằng đường sinh này tái lập pred_ck500_test (chỉ khác lịch sử thì mới so được)

Sinh đủ 6.958 bước (cả bước không chạm), vì câu của bước không chạm cũng đi vào lịch sử của bước sau.
Thứ tự: theo (episode_id, step_id). Nối tiếp được: đọc lại tệp ra, dựng lại lịch sử từ đó.

  python gen_tuantu.py --bundle AD --merged M [--ckpt CK] --recs test.jsonl --ocr ocr.jsonl \
         --images IMG --out pred_self.jsonl
  python gen_tuantu.py ... --dry --out /dev/null        # máy nhà, không nạp mô hình: in câu nhắc mẫu
"""
import os, sys, json, time, argparse, collections
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
    ap.add_argument("--out", required=True)
    ap.add_argument("--history", choices=["self", "gold"], default="self")
    ap.add_argument("--n-tap", type=int, default=0, help="--history gold: chỉ sinh N bước chạm đầu (kiểm tái lập)")
    ap.add_argument("--no-q4", dest="q4", action="store_false")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.adapter = os.path.join(a.bundle, "adapter_s1_seed101")

    rows = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    assert len(rows) == 6958, f"⛔ {a.recs} có {len(rows)} dòng, cần 6958"
    rows.sort(key=lambda r: (r["episode_id"], r["step_id"]))
    # lịch sử chuẩn ở bước k luôn dài đúng k (gồm cả bước không có ảnh). 327 tác vụ thiếu 625 bước vì
    # không có ảnh: ở những bước đó mô hình không sinh được câu, nên lịch sử lấy câu chuẩn thay vào và
    # mỗi dòng ra ghi `n_chuan` = số câu chuẩn phải thay. Phân tích chính dùng 1.105 tác vụ đủ ảnh.
    for r in rows:
        assert len(r.get("history") or []) == r["step_id"], f"⛔ lịch sử chuẩn ở {r['episode_id']}/{r['step_id']}"
    if a.history == "gold" and a.n_tap:
        rows = [r for r in rows if r["action"].get("action_type") in TAPT and "x" in r["action"]][:a.n_tap]
    ocr = {o["image"]: o for o in map(json.loads, open(a.ocr, encoding="utf-8"))}
    thieu = [r["image"] for r in rows if not os.path.exists(os.path.join(a.images, os.path.basename(r["image"])))]
    print(f"[dữ liệu] {a.recs} · {len(rows)} bước · lịch sử {a.history} · thiếu OCR "
          f"{sum(r['image'] not in ocr for r in rows)} · thiếu ảnh {len(thieu)}", flush=True)
    assert not thieu, f"⛔ thiếu ảnh, ví dụ {thieu[:3]}"

    P = {}
    if os.path.exists(a.out) and not a.dry:
        P = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(a.out, encoding="utf-8"))}
    print(f"[nối tiếp] đã có {len(P)}/{len(rows)}", flush=True)

    def lich_su(r):
        if a.history == "gold":
            return r.get("history") or []
        ep, k, g = r["episode_id"], r["step_id"], r.get("history") or []
        return [P.get((ep, j), g[j]) for j in range(k)]

    def n_chuan(r):
        return 0 if a.history == "gold" else sum((r["episode_id"], j) not in P for j in range(r["step_id"]))

    def msg_of(r):
        body = prompt_body({"goal": r["goal"], "history": lich_su(r)}, ocr.get(r["image"]))
        return [{"role": "system", "content": SYS},
                {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]

    if a.dry:   # giả lập: lịch sử tự sinh lấy tạm câu chuẩn có gắn nhãn, chỉ để xem câu nhắc dựng đúng
        for r in rows[:4]:
            for j in range(r["step_id"]):
                P[(r["episode_id"], j)] = f"<câu tự sinh bước {j}>"
            print(f"[khô] {r['episode_id']}/{r['step_id']}:", json.dumps(msg_of(r)[1]["content"][1]["text"],
                  ensure_ascii=False)[:600], flush=True)
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

    import torch
    from PIL import Image
    fo = open(a.out, "a", encoding="utf-8")
    t0, moi = time.time(), 0
    for i, r in enumerate(rows):
        k = (r["episode_id"], r["step_id"])
        if k in P:
            continue
        text = proc.apply_chat_template(msg_of(r), tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.images, os.path.basename(r["image"]))).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                               temperature=None, top_p=None, top_k=None)
        s = proc.decode(g[0][L:], skip_special_tokens=True).strip()
        P[k] = s
        fo.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": s, "history": lich_su(r),
                             "n_chuan": n_chuan(r)}, ensure_ascii=False) + "\n")
        fo.flush()
        moi += 1
        if (i + 1) % 50 == 0:
            dt = time.time() - t0
            print(f"  {i+1}/{len(rows)} · {dt/60:.1f} phút · {dt/moi:.2f} s/bước · {s[:60]!r}", flush=True)
    fo.close()
    print(f"[xong] {len(P)} câu · rỗng {sum(not v for v in P.values())}", flush=True)


if __name__ == "__main__":
    main()
