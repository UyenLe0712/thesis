# -*- coding: utf-8 -*-
"""SA-SPICE-v3 mức 2 (memo §6–7): GRPO từ sft_cont_merged trên 1.000 câu nhắc TRAIN-v3, một arm × một seed mỗi lần gọi.

Dùng lại vòng train của grpo_luoi.py (GRPO thuần, LoRA mới cùng cỡ S1, KL β về chính sft_cont_merged, DAPO,
group std, G 8, 2 câu nhắc/update = bs 4 × accum 4, lr 1e-5, nhiệt độ 1, max 96 token, 500 update, nạp default khi chạy tiếp),
chỉ thay hai thứ: tập câu nhắc (TRAIN-v3 theo thứ tự tệp) và hàm thưởng (9 arm, đúng công thức sa3_reward_screen.rewards).

  python sa3_grpo.py --hoa --data D --merged-s1 W/s1_merged --merged W/sft_cont_merged     # dựng sft_cont_merged (fp16)
  python sa3_grpo.py --train --arm SA-SPICE-v3 --seed 101 --data D --merged W/sft_cont_merged --out W/sa3_SA_401 [--resume auto]
  python sa3_grpo.py --selftest                                                             # CPU, không cần mô hình
D chứa train_v3.jsonl · ocr.jsonl · images/ · adapter_s1_seed101/ · sft_final/ (dataset sa3-mau-train-v3).
Câu rỗng ⇒ 0; SPICE/chrF NaN/None ⇒ STOP (memo §2bis).
"""
import os, sys, json, time, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_spice as GS          # noqa: E402
import grpo_luoi as GL           # noqa: E402
from sa3_reward_screen import rewards, k_gold, ARMS  # noqa: E402

CAN_SPICE = {"SPICE-MATCH", "Action-SPICE", "FIXED", "FIXED+A", "Sparse-SPICE", "SA-SPICE-v3", "SPIDEr-like"}
MD5_SFT = "113e2a3e6a0781fd5121acda99962d1b"
STAT = {"n": 0, "t": 0.0}
BO = {}


def dung_hang_v3(data):
    rows = [json.loads(l) for l in open(os.path.join(data, "train_v3.jsonl"), encoding="utf-8")]
    assert len(rows) == 1000, len(rows)
    ocr = GS.nap_ocr(data)
    out = []
    for r in rows:
        p = os.path.join(data, r["image"])
        assert os.path.exists(p) and r["image"] in ocr, f"⛔ thiếu ảnh/OCR {r['image']}"
        g = (r.get("target_instruction") or "").strip()
        assert g, f"⛔ câu chuẩn trống {r['episode_id']}_{r['step_id']}"
        body = GS.body_of(r, ocr)
        out.append(dict(key=f"{r['episode_id']}_{r['step_id']}", image=p,
                        prompt=[{"role": "system", "content": GS.SYS}, {"role": "user", "content": "\n" + body}],
                        gold=g, action_type=r["action"]["action_type"], n_char=len(body)))
    return out


def dung_bo(arm, data):
    golds = [(json.loads(l).get("target_instruction") or "").strip() for l in open(os.path.join(data, "train_v3.jsonl"), encoding="utf-8")]
    if arm == "SPIDEr-like":
        BO["cider"] = GL.CiderD(golds)          # df chỉ từ câu chuẩn TRAIN-v3 (memo §2bis)
    if arm == "ROUGE-L":
        from pycocoevalcap.rouge.rouge import Rouge
        BO["rouge"] = Rouge()


def lam_thuong(arm, spice_fn=None):
    import sacrebleu
    import sa3_action_verify as V
    if spice_fn is None and arm in CAN_SPICE:
        from h4_spice_tuple_7_11 import spice_chi_tiet as spice_fn

    def thuong(completions, gold, action_type, **kw):
        t0 = time.time()
        ys = [GS._text(c).strip() for c in completions]
        idx = [i for i, y in enumerate(ys) if y]
        SP = {}
        if idx and arm in CAN_SPICE:
            res = spice_fn([ys[i] for i in idx], [gold[i] for i in idx], nhan=f"spice {STAT['n'] + 1}")
            for i, o in zip(idx, res):
                f = o["scores"]["All"]["f"]
                if f is None or f != f:
                    raise SystemExit(f"⛔ STOP: SPICE NaN ở câu {ys[i]!r}")
                SP[i] = (float(f), k_gold(o["ref"]))
        out, nA = [], {0.0: 0, 0.5: 0, 1.0: 0}
        for i, (y, g, at) in enumerate(zip(ys, gold, action_type)):
            if not y:
                out.append(0.0); continue
            A, _ = V.score_action(y, g, at); nA[A] += 1
            s, K = SP.get(i, (0.0, 0))
            c = sacrebleu.sentence_chrf(y, [g]).score / 100
            ci = BO["cider"].score(y, g) / 10 if arm == "SPIDEr-like" else 0.0
            rl = BO["rouge"].calc_score([" ".join(GL.tok(y))], [" ".join(GL.tok(g))]) if arm == "ROUGE-L" else 0.0
            out.append(rewards(y, g, s, c, ci, rl, A, K)[arm])
        GL.LAST["r"] = list(out)
        dt = time.time() - t0; STAT["n"] += 1; STAT["t"] += dt
        print(f"[{arm}] lần {STAT['n']} · {len(ys)} câu · {dt:.1f}s · thưởng TB {sum(out) / len(out):.3f}"
              f" · A=1/0,5/0 {nA[1.0]}/{nA[0.5]}/{nA[0.0]} · số từ TB {sum(map(GS.nwords, ys)) / len(ys):.1f}"
              f" · rỗng {len(ys) - len(idx)}", flush=True)
        return out
    thuong.__name__ = "r_" + arm.replace("-", "_").replace("+", "p")
    return thuong


def hoa(a):
    """s1_merged (grpo_spice --merge) + sft_final → merge_and_unload → sft_cont_merged, fp16 trên T4 (= đường sa3_mau đã probe)."""
    import torch, transformers
    from transformers import Qwen2_5_VLForConditionalGeneration
    from peft import PeftModel
    if os.path.exists(os.path.join(a.merged, "config.json")):
        print("[hoà sft-cont] đã có", a.merged, flush=True); return
    sft = os.path.join(a.data, "sft_final")
    import hashlib
    assert hashlib.md5(open(os.path.join(sft, "adapter_model.safetensors"), "rb").read()).hexdigest() == MD5_SFT, "⛔ sft_final sai md5"
    assert json.load(open(os.path.join(sft, "adapter_config.json")))["base_model_name_or_path"].endswith("s1_merged")
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): torch.float16}
    m = Qwen2_5_VLForConditionalGeneration.from_pretrained(a.merged_s1, device_map={"": 0}, **kw)
    m = PeftModel.from_pretrained(m, sft).merge_and_unload()
    m.save_pretrained(a.merged, safe_serialization=True)
    print(f"[hoà sft-cont] xong → {a.merged} · sft_final md5 {MD5_SFT}", flush=True)


def kiem_hoa(a, n=3):
    """Greedy của sft_cont_merged vừa hoà phải trùng từng ký tự greedy kernel 1 (mau_0.jsonl) trên n câu nhắc đầu shard 0."""
    import torch
    from PIL import Image
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
    import transformers
    M = [json.loads(l) for l in open(os.path.join(a.data, "mau_0.jsonl"), encoding="utf-8")][:n]
    rows = {(r["episode_id"], r["step_id"]): r for r in map(json.loads, open(os.path.join(a.data, "train_v3.jsonl"), encoding="utf-8"))}
    ocr = GS.nap_ocr(a.data)
    kw = {("dtype" if int(transformers.__version__.split(".")[0]) >= 5 else "torch_dtype"): torch.float16}
    proc = AutoProcessor.from_pretrained(GS.BASE, min_pixels=200704, max_pixels=1003520)
    m = Qwen2_5_VLForConditionalGeneration.from_pretrained(a.merged, device_map={"": 0}, **kw).eval()
    same = 0
    for d in M:
        r = rows[(d["episode_id"], d["step_id"])]
        msg = [{"role": "system", "content": GS.SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + GS.body_of(r, ocr)}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        inp = proc(text=[text], images=[Image.open(os.path.join(a.data, r["image"])).convert("RGB")], return_tensors="pt").to("cuda:0")
        with torch.no_grad():
            g = m.generate(**inp, max_new_tokens=96, do_sample=False, temperature=None, top_p=None, top_k=None, use_cache=True)
        y = proc.decode(g[0][inp["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        same += y == d["greedy"]
        print(f"  [kiểm hoà] {y!r} | kernel 1: {d['greedy']!r}", flush=True)
    print(f"[kiểm hoà] greedy trùng kernel 1: {same}/{len(M)}", flush=True)
    assert same == len(M), "⛔ STOP: sft_cont_merged không trùng mô hình đã sinh mẫu cho sàng"


def train(a):
    print(f"[SA-SPICE-v3 mức 2] arm {a.arm} · seed {a.seed} · xuất phát {a.merged}", flush=True)
    dung_bo(a.arm, a.data)
    th = lam_thuong(a.arm)
    rows = dung_hang_v3(a.data)
    GS.dung_hang = lambda *x, **k: (rows, {"nguon": "train_v3.jsonl"})
    GL.dung_bo_cham = lambda *x, **k: None
    GL.lam_thuong = lambda name: th
    GL.STAT = STAT
    a.bundle, a.algo, a.reward, a.probe, a.keys_ck500, a.n_prompt = a.data, "grpo", "spice", False, "", 1000
    a.adapter = os.path.join(a.data, "adapter_s1_seed101")      # chỉ lấy cấu hình LoRA (r, alpha, target) cùng cỡ S1
    GS.MODE.update(reward="spice", G=a.G, seed=a.seed)
    GL.train(a)


def selftest():
    fake = lambda hyp, ref, nhan="": [{"scores": {"All": {"f": 0.5}}, "ref": ["button", "button | ok"]} for _ in hyp]
    BO["cider"] = GL.CiderD(["Click OK", "Open the app"])
    from pycocoevalcap.rouge.rouge import Rouge
    BO["rouge"] = Rouge()
    ys = ["Click the OK button", "", "Scroll down"]
    gs = ["Click OK"] * 3
    at = ["click"] * 3
    import sacrebleu
    import sa3_action_verify as V
    for arm in ARMS:
        r = lam_thuong(arm, spice_fn=fake)(ys, gs, at)
        assert r[1] == 0.0 and all(0 <= x <= 1 for x in r), (arm, r)
        c = sacrebleu.sentence_chrf(ys[0], [gs[0]]).score / 100
        ci = BO["cider"].score(ys[0], gs[0]) / 10
        rl = BO["rouge"].calc_score([" ".join(GL.tok(ys[0]))], [" ".join(GL.tok(gs[0]))])
        A, _ = V.score_action(ys[0], gs[0], "click")
        want = rewards(ys[0], gs[0], 0.5 if arm in CAN_SPICE else 0.0, c, ci, rl, A, 2)[arm]
        assert abs(r[0] - want) < 1e-12, (arm, r[0], want)
    r = lam_thuong("SA-SPICE-v3", spice_fn=fake)(ys, gs, at)
    assert r[0] > r[2], r          # tap đúng loại > cuộn sai loại
    print("✅ selftest sa3_grpo ĐẠT (9 arm, câu rỗng 0, khớp công thức sàng)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    for f in ("--selftest", "--hoa", "--kiem-hoa", "--train"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--data"); ap.add_argument("--merged"); ap.add_argument("--merged-s1"); ap.add_argument("--out")
    ap.add_argument("--arm", choices=ARMS, default="SA-SPICE-v3")
    ap.add_argument("--seed", type=int, default=101)
    ap.add_argument("--G", type=int, default=8); ap.add_argument("--bs", type=int, default=4); ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--beta", type=float, default=0.04); ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--max-steps", type=int, default=500); ap.add_argument("--resume", default=None)
    ap.add_argument("--no-q4", dest="q4", action="store_false"); ap.add_argument("--gen-chunk", type=int, default=0)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.hoa:
        return hoa(a)
    if a.kiem_hoa:
        return kiem_hoa(a)
    assert a.train and a.data and a.merged and a.out
    assert a.seed in (101, 401, 503, 907), "seed: 101 (user 11/11, lệch memo §6) hoặc 401 · 503 · 907"
    train(a)


if __name__ == "__main__":
    main()
