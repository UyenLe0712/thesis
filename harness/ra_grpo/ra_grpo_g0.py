# -*- coding: utf-8 -*-
"""311 — cổng G0 trước RA-GRPO: S1 (hoà, KHÔNG adapter) nhìn khối 4 câu mẫu thì sinh ra sao (Kaggle T4).

Hai chế độ, cùng đường sinh S1 của lượt 289 (`s1_merged` fp16, SYS + [ảnh, "\n" + body]):
--mode greedy  : greedy 96 token cho mọi bước click của --recs, có khối (--ra) -> so với pred_S1_vallon (không khối)
--mode mau     : 8 mẫu T = 1,0 cho --n-mau bước click rút cố định (hạt 20261012), có khối (--ra) hoặc không
                 -> đo trần best-of-8 có khối so với không khối; RL chỉ học được tới chỗ mẫu đã chạm

python ra_grpo_g0.py --mode greedy --merged M --recs B/p1_val_rows.jsonl --ocr B/ocr.jsonl --images B/images --ra ex_val_k4.jsonl --out g0_greedy_ra_0.jsonl --shard 0/2
python ra_grpo_g0.py --mode mau --merged M ... --ra ex_val_k4.jsonl --out g0_mau_ra.jsonl
python ra_grpo_g0.py --mode mau --merged M ... --out g0_mau_khong.jsonl        # không khối
thêm --dry: in câu nhắc, không nạp mô hình. Nối tiếp được.
"""
import os, sys, json, time, random, argparse
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script"),
          os.path.join(HERE, "..", "..", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)
from build_branch_data import prompt_body, SYS
import ra_exemplars as RA

TAPT = ("click", "long_press")
HAT_MAU = 20261012


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("greedy", "mau"), required=True)
    ap.add_argument("--merged", default="")
    ap.add_argument("--recs", required=True)
    ap.add_argument("--ocr", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--ra", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-mau", type=int, default=300)
    ap.add_argument("--g", type=int, default=8)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.q4 = False

    rows = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    rows = [r for r in rows if (r.get("action") or {}).get("action_type") in TAPT and "x" in r["action"]]
    if a.mode == "mau":
        keys = sorted((r["episode_id"], r["step_id"]) for r in rows)
        chon = set(random.Random(HAT_MAU).sample(keys, min(a.n_mau, len(keys))))
        rows = [r for r in rows if (r["episode_id"], r["step_id"]) in chon]
    si, sn = map(int, a.shard.split("/"))
    rows = rows[si::sn]
    ocr = {o["image"]: o for o in map(json.loads, open(a.ocr, encoding="utf-8"))}
    EXM = None
    if a.ra:
        EXM = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
        assert all((r["episode_id"], r["step_id"]) in EXM for r in rows), "⛔ tệp ví dụ thiếu bước"

    def body_of(r):
        b = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        e = EXM[(r["episode_id"], r["step_id"])] if EXM is not None else None
        return RA.chen(b, e) if e else b

    print(f"[G0] {a.mode} - khối {'CÓ' if a.ra else 'KHÔNG'} - {len(rows)} bước - [câu nhắc đầu]\n{body_of(rows[0])}", flush=True)
    if a.dry:
        return

    import torch
    from PIL import Image
    import grpo_spice as GS
    proc, model, _ = GS.nap(a)
    model.eval()
    print("[kiểm lưu] KHÔNG gắn - S1 hoà", flush=True)
    done = set()
    if os.path.exists(a.out):
        done = {(d["episode_id"], d["step_id"]) for d in map(json.loads, open(a.out, encoding="utf-8"))}
    fo = open(a.out, "a", encoding="utf-8")
    t0, moi = time.time(), 0
    for i, r in enumerate(rows):
        k = (r["episode_id"], r["step_id"])
        if k in done:
            continue
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body_of(r)}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.images, os.path.basename(r["image"]))).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            if a.mode == "greedy":
                g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                                   temperature=None, top_p=None, top_k=None)
                rec = {"episode_id": k[0], "step_id": k[1], "pred": proc.decode(g[0][L:], skip_special_tokens=True).strip()}
            else:
                torch.manual_seed(HAT_MAU + 1000 * int(k[0]) + int(k[1]))
                g = model.generate(**inp, max_new_tokens=96, do_sample=True, temperature=1.0, top_p=1.0, top_k=0,
                                   num_return_sequences=a.g, use_cache=True)
                rec = {"episode_id": k[0], "step_id": k[1],
                       "samples": [proc.decode(x[L:], skip_special_tokens=True).strip() for x in g]}
        fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fo.flush()
        moi += 1
        if (i + 1) % 25 == 0:
            dt = time.time() - t0
            print(f"  {i+1}/{len(rows)} - {dt/60:.1f} phút - {dt/moi:.2f} s/bước", flush=True)
    fo.close()
    print(f"[xong] {sum(1 for _ in open(a.out, encoding='utf-8'))} dòng -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
