# -*- coding: utf-8 -*-
"""SA-SPICE-v3 — kernel 1 (Kaggle T4): dựng sft_cont_merged, probe ghép, sinh greedy + 8 mẫu trên TRAIN-v3.

Mô hình đúng như lượt SFT-cont đã chấm test (kernel luoi-test-u-3): s1_merged (grpo_spice.py --merge, fp16 trên T4) → gắn sft_final. Hai đường phải trùng:
  A = s1_merged + adapter sft_final bật (PeftModel)        B = A.merge_and_unload() (= sft_cont_merged)
Probe trên --probe-n câu nhắc đầu: max |logit_A − logit_B| ở token cuối ≤ --atol và greedy trùng từng ký tự; lệch ⇒ STOP.

Lấy mẫu: nhiệt độ 1,0 · top_p 1,0 · top_k 0 · max_new 96 (= recipe GRPO §7 của memo). Câu nhắc = build_branch_data.prompt_body
+ SYS, ảnh trước chữ (cùng đường c1_mau_s1.py / gen_test_grpo.py). In cấu hình thật sự dùng. Ghi dần, nối tiếp được.
Chia hai GPU: --shard i --nshard 2.

  python sa3_mau.py --data D --merged S1_MERGED --sft ADAPTER_SFT --out mau_0.jsonl --shard 0 --nshard 2
  python sa3_mau.py ... --n 3 --out thu.jsonl          # thử nhanh
"""
import os, sys, json, time, hashlib, argparse

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_branch_data import prompt_body, SYS  # noqa: E402

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
MD5_SFT = "113e2a3e6a0781fd5121acda99962d1b"


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="thư mục có train_v3.jsonl, ocr.jsonl, images/")
    ap.add_argument("--merged", required=True, help="s1_merged do grpo_spice.py --merge dựng"); ap.add_argument("--sft", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshard", type=int, default=1)
    ap.add_argument("--n", type=int, default=0); ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--probe-n", type=int, default=8); ap.add_argument("--atol", type=float, default=0.15)
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(os.path.join(a.data, "train_v3.jsonl"), encoding="utf-8")]
    assert len(rows) == 1000, len(rows)
    rows = rows[a.shard::a.nshard]
    if a.n:
        rows = rows[: a.n]
    ocr = {}
    for l in open(os.path.join(a.data, "ocr.jsonl"), encoding="utf-8"):
        o = json.loads(l); ocr[o["image"]] = o
    miss = [r["image"] for r in rows if r["image"] not in ocr or not os.path.exists(os.path.join(a.data, r["image"]))]
    assert not miss, f"⛔ thiếu ảnh/OCR: {miss[:3]} ({len(miss)})"
    assert md5(os.path.join(a.sft, "adapter_model.safetensors")) == MD5_SFT, "⛔ adapter SFT-cont không đúng md5 đã chấm test"
    done = set()
    if os.path.exists(a.out):
        done = {(d["episode_id"], d["step_id"]) for d in map(json.loads, open(a.out, encoding="utf-8"))}
    todo = [r for r in rows if (r["episode_id"], r["step_id"]) not in done]
    print(f"[dữ liệu] shard {a.shard}/{a.nshard} · {len(rows)} câu nhắc · đã có {len(done)} · còn {len(todo)}", flush=True)
    if not todo:
        print("Xong sẵn.", flush=True); return

    import torch, transformers
    from PIL import Image
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from peft import PeftModel

    dt = torch.float16
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): dt}
    proc = AutoProcessor.from_pretrained(BASE, min_pixels=200704, max_pixels=1003520)
    m = Qwen2_5_VLForConditionalGeneration.from_pretrained(a.merged, device_map={"": 0}, **kw)   # s1_merged
    assert json.load(open(os.path.join(a.sft, "adapter_config.json")))["base_model_name_or_path"].endswith("s1_merged")
    A = PeftModel.from_pretrained(m, a.sft); A.eval()

    def inputs(r):
        body = prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.data, r["image"])).convert("RGB")
        return proc(text=[text], images=[img], return_tensors="pt").to("cuda:0")

    def greedy(model, inp):
        L = inp["input_ids"].shape[1]
        g = model.generate(**inp, max_new_tokens=96, do_sample=False, temperature=None, top_p=None, top_k=None, use_cache=True)
        return proc.decode(g[0][L:], skip_special_tokens=True).strip()

    # ---- probe A (adapter bật) vs B (đã hoà) ----
    pr = rows[: a.probe_n]
    la, ga = [], []
    with torch.no_grad():
        for r in pr:
            inp = inputs(r)
            la.append(A(**inp).logits[0, -1].float().cpu()); ga.append(greedy(A, inp))
    B = A.merge_and_unload(); B.eval()                                              # sft_cont_merged
    with torch.no_grad():
        dmax, same = 0.0, 0
        for r, l0, g0 in zip(pr, la, ga):
            inp = inputs(r)
            dmax = max(dmax, (B(**inp).logits[0, -1].float().cpu() - l0).abs().max().item())
            same += greedy(B, inp) == g0
    print(f"[probe ghép] {len(pr)} câu nhắc · max|Δlogit| {dmax:.4f} (atol {a.atol}) · greedy trùng {same}/{len(pr)}", flush=True)
    assert dmax <= a.atol and same == len(pr), "⛔ STOP: sft_cont_merged lệch đường adapter bật"
    json.dump({"probe_n": len(pr), "max_abs_dlogit": dmax, "greedy_same": same, "atol": a.atol, "dtype": "float16",
               "probe_keys": [f"{r['episode_id']}_{r['step_id']}" for r in pr],
               "greedy_sha256": hashlib.sha256("\n".join(ga).encode()).hexdigest()},
              open(a.out + ".probe.json", "w"), ensure_ascii=False, indent=1)
    del A

    samp = dict(do_sample=True, temperature=1.0, top_p=1.0, top_k=0, repetition_penalty=1.0,
                num_return_sequences=a.k, max_new_tokens=96, use_cache=True)
    print(f"[cấu hình] dtype {dt} · torch {torch.__version__} · transformers {transformers.__version__} · lấy mẫu {samp}", flush=True)
    torch.manual_seed(20261111 + a.shard)
    out = open(a.out, "a", encoding="utf-8"); t0 = time.time()
    for i, r in enumerate(todo):
        inp = inputs(r); L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = greedy(B, inp)
            s = B.generate(**inp, **samp)
        mau = [proc.decode(x[L:], skip_special_tokens=True).strip() for x in s]
        trunc = [int((x[L:] != proc.tokenizer.eos_token_id).all().item() and len(x) - L >= 96) for x in s]
        out.write(json.dumps({"episode_id": r["episode_id"], "step_id": r["step_id"], "action_type": r["action"]["action_type"],
                              "package": r.get("package", ""), "gold": r["target_instruction"], "greedy": g, "mau": mau,
                              "mau_cut96": trunc}, ensure_ascii=False) + "\n")
        out.flush()
        if (i + 1) % 10 == 0 or i == len(todo) - 1:
            el = time.time() - t0
            print(f"  {i + 1}/{len(todo)} · {el / 60:.1f} phút · còn ~{el / (i + 1) * (len(todo) - i - 1) / 60:.1f} phút · greedy: {g[:50]!r}", flush=True)
    out.close(); print("XONG", flush=True)


if __name__ == "__main__":
    main()
