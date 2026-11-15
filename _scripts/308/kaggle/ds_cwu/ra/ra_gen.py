# -*- coding: utf-8 -*-
"""304 — sinh greedy cho bước click, cùng đường đã sinh ck500 (gen_test_grpo.py): `s1_merged` fp16 + adapter,
greedy, 96 token, câu nhắc SYS + [ảnh, "\\n" + prompt_body]. Thêm một tùy chọn: --ra chèn khối ví dụ truy hồi.

# test, khối k=4:      --recs T/test.jsonl --ocr T/ocr.jsonl --images T/images --expect 4463 --ra ex_test_k4.jsonl
# test, kho rỗng:      bỏ --ra (câu nhắc y hệt câu nhắc của ck500)
# val lớn:             --recs B/p1_val_rows.jsonl --ocr B/ocr.jsonl --images B/images --expect 1002 [--ra ex_val_k4.jsonl]
# chạy khô (CPU):      thêm --dry
Nối tiếp được: chạy lại đúng lệnh, bước đã có trong --out được bỏ qua.
"""
import os, sys, json, time, argparse

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_branch_data import prompt_body, SYS

TAPT = ("click", "long_press")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged", required=True)
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--recs", required=True)
    ap.add_argument("--ocr", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ra", default=None)
    ap.add_argument("--expect", type=int, default=0)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--shard", default="0/1", help="i/n: chỉ sinh các bước thứ i, i+n, … (chia đôi cho hai GPU)")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.q4 = False

    rows = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    rows = [r for r in rows if (r.get("action") or {}).get("action_type") in TAPT and "x" in r["action"]]
    if a.expect:
        assert len(rows) == a.expect, f"⛔ {len(rows)} bước click, cần {a.expect}"
    if a.n:
        rows = rows[:a.n]
    si, sn = map(int, a.shard.split("/"))
    rows = rows[si::sn]
    ocr = {o["image"]: o for o in map(json.loads, open(a.ocr, encoding="utf-8"))}
    thieu = [r["image"] for r in rows if not os.path.exists(os.path.join(a.images, os.path.basename(r["image"])))]
    print(f"[dữ liệu] {a.recs} · {len(rows)} bước click · thiếu OCR {sum(r['image'] not in ocr for r in rows)}"
          f" · thiếu ảnh {len(thieu)}", flush=True)
    assert a.dry or not thieu, f"⛔ thiếu ảnh, ví dụ {thieu[:3]}"

    EXM = None
    if a.ra:
        import ra_exemplars as RA
        EXM = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
        miss = sum((r["episode_id"], r["step_id"]) not in EXM for r in rows)
        print(f"[ví dụ] {a.ra} · {len(EXM)} bước · thiếu {miss}", flush=True)
        assert not miss, "⛔ tệp ví dụ không phủ đủ bước"
    else:
        print("[ví dụ] KHÔNG có khối — câu nhắc y hệt câu nhắc của ck500", flush=True)

    def body_of(r):
        b = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        if EXM is not None:
            b = RA.chen(b, EXM[(r["episode_id"], r["step_id"])])
        return b

    def msg_of(r):
        return [{"role": "system", "content": SYS},
                {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body_of(r)}]}]

    print("[câu nhắc bước đầu]\n" + body_of(rows[0]), flush=True)
    if a.dry:
        return

    import torch
    from PIL import Image
    from peft import PeftModel
    import grpo_spice as GS
    proc, model, _ = GS.nap(a)
    model = PeftModel.from_pretrained(model, a.ckpt)
    model.eval()
    print("[điểm lưu]", a.ckpt, flush=True)

    done = set()
    if os.path.exists(a.out):
        done = {(d["episode_id"], d["step_id"]) for d in map(json.loads, open(a.out, encoding="utf-8"))}
    print(f"[nối tiếp] đã có {len(done)}/{len(rows)}", flush=True)

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


if __name__ == "__main__":
    main()
