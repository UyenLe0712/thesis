# -*- coding: utf-8 -*-
"""314 - RAFT bước 1: ck500 sinh greedy + G mẫu (T = 0,7) trên câu nhắc train ck500 CHƯA thấy trong GRPO (Kaggle T4).

Viết lại theo mô tả file 314 (bản Mac không có trên máy WSL). Câu nhắc lấy bằng đúng `grpo_spice.dung_hang`
(cùng thứ tự xáo hạt 101 như lúc train ck500): ck500 đã dùng hàng [0, 1000), lượt này lấy [--tu, --den).
Đường sinh giống ck500 lúc chấm (`s1_merged` fp16 + adapter, SYS + [ảnh, "\\n" + body]).

    python raft_mau.py --bundle B --merged M --ckpt CK500 --out raft_mau_0.jsonl --shard 0/2
    python raft_mau.py --bundle B --dry          # in số hàng + câu nhắc đầu, không nạp mô hình
Mỗi dòng ra: {key, image, body, gold, action_type, greedy, samples[G]}. Nối tiếp được.
"""
import os, sys, json, time, argparse

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HAT = 20261012


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--merged", default="")
    ap.add_argument("--ckpt", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--tu", type=int, default=1000)
    ap.add_argument("--den", type=int, default=3000)
    ap.add_argument("--g", type=int, default=8)
    ap.add_argument("--t", type=float, default=0.7)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.q4 = False

    import grpo_spice as GS
    from build_branch_data import SYS
    tat, bo = GS.dung_hang(a.bundle, n=10 ** 9)
    ck = {r["key"] for r in tat[:1000]}
    rows = tat[a.tu:a.den]
    assert not ({r["key"] for r in rows} & ck), "⛔ lẫn câu nhắc ck500 đã thấy"
    si, sn = map(int, a.shard.split("/"))
    rows = rows[si::sn]
    for r in rows:
        r["body"] = GS._text(r["prompt"][1]["content"])[1:]
    print(f"[câu nhắc] hàng [{a.tu}, {a.den}) trên {len(tat)} · shard {a.shard}: {len(rows)} · bỏ {bo}", flush=True)
    print("[câu nhắc đầu]\n" + rows[0]["body"][:1500], flush=True)
    if a.dry:
        return

    import torch
    from PIL import Image
    from peft import PeftModel
    proc, model, _ = GS.nap(a)
    model = PeftModel.from_pretrained(model, a.ckpt)
    model.eval()
    print("[điểm lưu]", a.ckpt, flush=True)

    done = set()
    if os.path.exists(a.out):
        done = {json.loads(l)["key"] for l in open(a.out, encoding="utf-8")}
    print(f"[nối tiếp] đã có {len(done)}/{len(rows)}", flush=True)
    fo = open(a.out, "a", encoding="utf-8")
    t0, moi = time.time(), 0
    for i, r in enumerate(rows):
        if r["key"] in done:
            continue
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + r["body"]}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(r["image"]).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                               temperature=None, top_p=None, top_k=None)
            gr = proc.decode(g[0][L:], skip_special_tokens=True).strip()
            ep, st = r["key"].split("_")
            torch.manual_seed(HAT + 1000 * int(ep) + int(st))
            s = model.generate(**inp, max_new_tokens=96, do_sample=True, temperature=a.t, top_p=1.0, top_k=0,
                               num_return_sequences=a.g, use_cache=True)
            sm = [proc.decode(x[L:], skip_special_tokens=True).strip() for x in s]
        fo.write(json.dumps(dict(key=r["key"], image=r["image"], body=r["body"], gold=r["gold"],
                                 action_type=r["action_type"], greedy=gr, samples=sm), ensure_ascii=False) + "\n")
        fo.flush()
        moi += 1
        if (i + 1) % 25 == 0:
            dt = time.time() - t0
            print(f"  {i+1}/{len(rows)} · {dt/60:.1f} phút · {dt/moi:.2f} s/bước · {gr[:50]!r}", flush=True)
    fo.close()
    print(f"[xong] {sum(1 for _ in open(a.out, encoding='utf-8'))} dòng → {a.out}", flush=True)


if __name__ == "__main__":
    main()
