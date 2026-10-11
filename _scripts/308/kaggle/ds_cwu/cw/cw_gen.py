# -*- coding: utf-8 -*-
"""308 - sinh cho CW-RA, cùng đường sinh ck500 (`s1_merged` fp16 + adapter, greedy, 96 token, SYS + [ảnh, "\\n" + body]).

Hai chế độ:
  --mode tu : câu greedy KHÔNG khối, mọi loại thao tác (mặc định) - đích [WRITE] cho cw_build.py. Gắn --ckpt ck500.
  --mode cw : khối k = 4 (--ra ex_*.jsonl). Mỗi bước ghi:
      lp       log-xác suất của từng thẻ "[WRITE]", "[COPY 1]"..."[COPY k]" (ép từng thẻ, cộng log-prob token)
      p_copy   Σ exp(lp COPY) / Σ exp(lp mọi thẻ)
      copy_idx i của thẻ COPY có lp cao nhất
      write    câu sinh tiếp sau khi ép tiền tố "[WRITE]"
    Ghép theo ngưỡng τ làm ở cw_ghep.py (CPU), không sinh lại.

python cw_gen.py --mode tu --merged M --ckpt CK500 --recs B/p1_train_rows.jsonl --ocr B/ocr.jsonl --images B/images --out pred_ck500_train.jsonl --shard 0/2
python cw_gen.py --mode cw --merged M --ckpt CW/final --recs T/test.jsonl --ocr T/ocr.jsonl --images T/images --ra ex_test_k4.jsonl --chi-cham --expect 4463 --out cw_test.jsonl --shard 0/2
thêm --dry: chỉ in câu nhắc + thẻ, không nạp mô hình.
Nối tiếp được: chạy lại đúng lệnh, bước đã có trong --out được bỏ qua.
"""
import os, sys, json, math, time, argparse

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)
from build_branch_data import prompt_body, SYS
import ra_exemplars as RA

TAPT = ("click", "long_press")
TAG_W = "[WRITE]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("tu", "cw"), required=True)
    ap.add_argument("--merged", default="")
    ap.add_argument("--ckpt", default="")
    ap.add_argument("--recs", required=True)
    ap.add_argument("--ocr", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ra", default=None)
    ap.add_argument("--chi-cham", action="store_true", help="chỉ bước click/long_press (val, test)")
    ap.add_argument("--expect", type=int, default=0)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.q4 = False
    assert a.mode == "tu" or a.ra, "⛔ --mode cw cần --ra"
    assert not (a.mode == "tu" and a.ra), "⛔ --mode tu là câu nhắc KHÔNG khối"

    rows = [json.loads(l) for l in open(a.recs, encoding="utf-8")]
    if a.chi_cham:
        rows = [r for r in rows if (r.get("action") or {}).get("action_type") in TAPT and "x" in r["action"]]
    rows = [r for r in rows if (r.get("target_instruction") or r.get("gold_instruction") or "").strip() or a.chi_cham]
    if a.expect:
        assert len(rows) == a.expect, f"⛔ {len(rows)} bước, cần {a.expect}"
    if a.n:
        rows = rows[:a.n]
    si, sn = map(int, a.shard.split("/"))
    rows = rows[si::sn]
    ocr = {o["image"]: o for o in map(json.loads, open(a.ocr, encoding="utf-8"))}
    thieu = [r["image"] for r in rows if not os.path.exists(os.path.join(a.images, os.path.basename(r["image"])))]
    print(f"[dữ liệu] {a.recs} · {len(rows)} bước · thiếu OCR {sum(r['image'] not in ocr for r in rows)} · thiếu ảnh {len(thieu)}",
          flush=True)
    assert a.dry or not thieu, f"⛔ thiếu ảnh, ví dụ {thieu[:3]}"

    EXM = None
    if a.ra:
        EXM = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
        miss = sum((r["episode_id"], r["step_id"]) not in EXM for r in rows)
        assert not miss, f"⛔ tệp ví dụ thiếu {miss} bước"

    def exs_of(r):
        return EXM[(r["episode_id"], r["step_id"])] if EXM is not None else []

    def body_of(r):
        b = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        e = exs_of(r)
        return RA.chen(b, e) if e else b

    def tags_of(r):
        return [TAG_W] + [f"[COPY {i}]" for i in range(1, len(exs_of(r)) + 1)]

    def msg_of(r):
        return [{"role": "system", "content": SYS},
                {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body_of(r)}]}]

    print(f"[chế độ] {a.mode} · [câu nhắc bước đầu]\n{body_of(rows[0])}\n[thẻ] {tags_of(rows[0]) if a.mode == 'cw' else '-'}",
          flush=True)
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

    def enc(text, img):
        return proc(text=[text], images=[img], return_tensors="pt").to(model.device)

    def gen(text, img):
        inp = enc(text, img)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                               temperature=None, top_p=None, top_k=None)
        return proc.decode(g[0][L:], skip_special_tokens=True).strip()

    def lp_tag(base, img, L0, ids0, tag):
        inp = enc(base + tag, img)
        ids = inp["input_ids"][0]
        assert ids[:L0].tolist() == ids0, "⛔ token câu nhắc đổi khi nối thẻ"
        with torch.no_grad():
            lg = model(**inp).logits[0].float().log_softmax(-1)
        return float(sum(lg[j - 1, ids[j]] for j in range(L0, ids.shape[0])))

    fo = open(a.out, "a", encoding="utf-8")
    t0, moi = time.time(), 0
    for i, r in enumerate(rows):
        k = (r["episode_id"], r["step_id"])
        if k in done:
            continue
        base = proc.apply_chat_template(msg_of(r), tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.images, os.path.basename(r["image"]))).convert("RGB")
        if a.mode == "tu":
            rec = {"episode_id": k[0], "step_id": k[1], "pred": gen(base, img)}
        else:
            inp0 = enc(base, img)
            L0, ids0 = inp0["input_ids"].shape[1], inp0["input_ids"][0].tolist()
            T = tags_of(r)
            lp = [lp_tag(base, img, L0, ids0, t) for t in T]
            m = max(lp)
            z = sum(math.exp(x - m) for x in lp)
            p_copy = sum(math.exp(x - m) for x in lp[1:]) / z
            ci = (max(range(1, len(T)), key=lambda j: lp[j]) if len(T) > 1 else 0)
            w = gen(base + TAG_W, img)
            rec = {"episode_id": k[0], "step_id": k[1], "lp": [round(x, 4) for x in lp], "p_copy": round(p_copy, 5),
                   "copy_idx": ci, "write": w}
            if moi < 3:
                print(f"  [mẫu] thẻ {T} · lp {rec['lp']} · p_copy {p_copy:.3f} · write {w[:60]!r}", flush=True)
        fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fo.flush()
        moi += 1
        if (i + 1) % 50 == 0:
            dt = time.time() - t0
            print(f"  {i+1}/{len(rows)} · {dt/60:.1f} phút · {dt/moi:.2f} s/bước", flush=True)
    fo.close()
    n = sum(1 for _ in open(a.out, encoding="utf-8"))
    print(f"[xong] {n} dòng trong {a.out}", flush=True)


if __name__ == "__main__":
    main()
