# -*- coding: utf-8 -*-
"""CTG-GRPO (action 276): GRPO trên S1/101, thưởng CIDEr-D + bộ giữ loại thao tác CTG.

Bốn nhánh, cùng một tệp:
  A3  r_cider + CTG bật                 (mô hình đề xuất, 1.000 bước)
  A2  r_cider, CTG tính và ghi log nhưng không cộng vào advantage (ablation, 1.000 bước)
  A4  r_cider + lấy mẫu lại câu nhắc theo lớp kiểu DISCO (500 bước)
  A7  r_cider + thưởng đúng loại toàn cục kiểu Co-EPG (500 bước)

Máy nhà (CPU, 0 GPU):
  python ctg_grpo.py --selftest-cider --c1-recs runs/c1/exec8/c1data/c1_recs.jsonl \
         --c1-mau runs/c1/c1_mau.jsonl --metric runs/c1/exec8/metric_tung_cau.json
  python ctg_grpo.py --selftest --bundle B
GPU (dùng chung --merge của grpo_spice.py):
  python ctg_grpo.py --train --arm A3 --bundle B --merged M --out O --resume auto
  python ctg_grpo.py --logp-probe --bundle B --merged M --c1 c1_mau.jsonl --ckpts ck250=P,ck500=Q --out p0b.json
Sinh greedy trên val C1 cho điểm lưu: `grpo_spice.py --gen --ckpt O/checkpoint-N` (không đổi).
"""

import os, re, sys, json, time, glob, math, random, argparse, dataclasses, collections
from collections import defaultdict

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from metric_exec import canon_action  # noqa: E402

SEED = 101
MU = 0.02
N_PROMPT = 2000
WORD = re.compile(r"[A-Za-z0-9'-]+")

# ---- tham số CTG, khoá trước (276 §6) ----
CTG_LOP = ("scroll", "type", "navigate_back")
P_DICH = {"scroll": 0.837, "type": 0.813, "navigate_back": 0.733}
LAM0, ETA, LAM_MAX, DELTA, EMA = 1.0, 0.5, 3.0, 0.01, 0.8


def nwords(s):
    return len(WORD.findall(s or ""))


def _text(c):
    if isinstance(c, list):
        return (c[0].get("content") if c else "") or ""
    return c or ""


def lop(s):
    return canon_action(s, strict_back=True)


# ============================ CIDEr-D (276 Phụ lục A, nguyên văn) ============================
# '"' không có trong Phụ lục A của 276 (rơi lúc chép): thiếu nó chỉ tái lập 3.407/3.600, có nó ra
# đúng 3.484/3.600 · 399/400 như 276 ghi. PTBTokenizer đổi " thành `` / '' rồi bỏ.
PUNCT = {"''", "'", "``", "`", "-lrb-", "-rrb-", "-lcb-", "-rcb-", ".", "?", "!", ",", ":", "-", "--",
         "...", ";", '"'}
TOK = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-./][a-z0-9]+)*|[^\sa-z0-9]")


def tok(s):
    """Xấp xỉ PTBTokenizer của pycocoevalcap: chữ thường, tách n't / 's, bỏ dấu câu."""
    s = (s or "").lower().replace("“", '"').replace("”", '"').replace("’", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    return [t for t in TOK.findall(s) if t not in PUNCT and t != ""]


def ngrams(ws, n=4):
    c = defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(ws) - k + 1):
            c[tuple(ws[i:i + k])] += 1
    return c


class CiderD:
    """CIDEr-D đúng công thức pycocoevalcap (sigma 6, clip, x10) nhưng df và số tài liệu CỐ ĐỊNH."""

    def __init__(self, ref_corpus, n=4, sigma=6.0):
        self.n, self.sigma = n, sigma
        self.df = defaultdict(float)
        for r in ref_corpus:
            for ng in set(ngrams(tok(r), n)):
                self.df[ng] += 1
        self.log_n = math.log(float(len(ref_corpus)))

    def _vec(self, cnts):
        vec = [dict() for _ in range(self.n)]
        norm = [0.0] * self.n
        length = 0
        for ng, tf in cnts.items():
            k = len(ng) - 1
            w = float(tf) * (self.log_n - math.log(max(1.0, self.df.get(ng, 0.0))))
            vec[k][ng] = w
            norm[k] += w * w
            if k == 1:
                length += tf
        return vec, [math.sqrt(x) for x in norm], length

    def score(self, cand, refs):
        vh, nh, lh = self._vec(ngrams(tok(cand), self.n))
        tot = [0.0] * self.n
        for r in refs:
            vr, nr, lr = self._vec(ngrams(tok(r), self.n))
            pen = math.exp(-((lh - lr) ** 2) / (2 * self.sigma ** 2))
            for k in range(self.n):
                v = sum(min(w, vr[k].get(ng, 0.0)) * vr[k].get(ng, 0.0) for ng, w in vh[k].items())
                if nh[k] != 0 and nr[k] != 0:
                    v /= nh[k] * nr[k]
                tot[k] += v * pen
        return 10.0 * (sum(tot) / self.n) / len(refs)


# ============================ thưởng ============================
CID = {"m": None}
STAT = {"n": 0, "t": 0.0}


def dung_cider(bundle):
    tr = [json.loads(l) for l in open(os.path.join(bundle, "p1_train_rows.jsonl"), encoding="utf-8")]
    refs = [(r.get("target_instruction") or "").strip() for r in tr]
    refs = [r for r in refs if r]
    CID["m"] = CiderD(refs)
    print(f"[cider] df dựng từ {len(refs)} câu chuẩn của p1_train_rows.jsonl", flush=True)


def r_cider(completions, gold, **kw):
    t0 = time.time()
    sents = [_text(c).strip() for c in completions]
    out = [0.0 if not s else CID["m"].score(s, [g]) / 10.0 - MU * max(0, nwords(s) - nwords(g) - 3)
           for s, g in zip(sents, gold)]
    STAT["n"] += 1
    STAT["t"] += time.time() - t0
    print(f"[cider] lần {STAT['n']} · {len(sents)} câu · thưởng TB {sum(out)/len(out):.3f}"
          f" · số từ TB {sum(map(nwords, sents))/len(sents):.1f} · rỗng {sum(not s for s in sents)}",
          flush=True)
    return out


def r_loai(completions, gold, **kw):
    """A7: +1 khi loại thao tác của câu sinh trùng loại của câu chuẩn, mọi câu nhắc."""
    return [float(bool(_text(c).strip()) and lop(_text(c).strip()) == lop(g))
            for c, g in zip(completions, gold)]


def kiem_thuong():
    gold = ["Click on the search bar", "Click on the search bar", "Click on the search bar"]
    cand = ["Click on the search bar", "", "Swipe up"]
    r = r_cider(cand, gold)
    print("thưởng:", [round(x, 4) for x in r], "← kỳ vọng [> 0, 0, < 0,05]", flush=True)
    assert r[0] > 0 and r[1] == 0.0 and r[2] < 0.05, r


# ============================ CTG ============================
class CTG:
    """Trạng thái dual {λ, ĉ} và phép cộng advantage cho một nhóm G câu."""

    def __init__(self):
        self.lam = {k: LAM0 for k in CTG_LOP}
        self.chat = dict(P_DICH)

    def to_dict(self):
        return {"lam": self.lam, "chat": self.chat}

    def nap(self, d):
        self.lam = {k: float(d["lam"][k]) for k in CTG_LOP}
        self.chat = {k: float(d["chat"][k]) for k in CTG_LOP}

    def nhom(self, k, c, adv, tap, apply):
        """k: lớp vàng · c: list 0/1 đúng loại · adv: tensor (G,) advantage của nhóm (sửa tại chỗ khi apply).
        tap: list bool câu sinh là tap. Trả về dòng log."""
        import torch
        cbar = sum(c) / len(c)
        self.chat[k] = EMA * self.chat[k] + (1 - EMA) * cbar
        self.lam[k] = min(max(self.lam[k] + ETA * (P_DICH[k] - DELTA - self.chat[k]), 0.0), LAM_MAX)
        ct = torch.tensor(c, dtype=torch.float32)
        sd = ct.std(unbiased=True).item()
        day_truoc = float(sum(adv[i].item() for i in range(len(c)) if tap[i]))
        if sd > 0 and apply:
            z = (ct - ct.mean()) / (sd + 1e-4)
            adv += self.lam[k] * z.to(adv.device, adv.dtype)
        day_sau = float(sum(adv[i].item() for i in range(len(c)) if tap[i]))
        return dict(lop=k, lam=round(self.lam[k], 5), chat=round(self.chat[k], 5), cbar=cbar,
                    std_pos=sd > 0, n_tap=sum(tap), day_truoc=round(day_truoc, 5), day_sau=round(day_sau, 5))


def lam_ctg_trainer(arm, out_dir):
    from trl import GRPOTrainer

    class CTGTrainer(GRPOTrainer):
        ctg = CTG()
        apply = arm == "A3"
        log_path = os.path.join(out_dir, "ctg_log.jsonl")

        def _generate_and_score_completions(self, inputs):
            out = super()._generate_and_score_completions(inputs)
            if not self.model.training:
                return out
            G = self.num_generations
            assert len(inputs) % G == 0, (len(inputs), G)
            assert out["advantages"].dim() == 1 and len(out["advantages"]) == len(inputs), \
                "⛔ advantage không phải (B,) hoặc không khớp số câu (nhiều tiến trình?)"
            tk = getattr(self.processing_class, "tokenizer", self.processing_class)
            txt = [s.strip() for s in tk.batch_decode(out["completion_ids"], skip_special_tokens=True)]
            dong = []
            for j in range(0, len(inputs), G):
                assert len({x["key"] for x in inputs[j:j + G]}) == 1, "⛔ nhóm G không liền khối"
                k = lop(inputs[j]["gold"])
                cls = [lop(s) for s in txt[j:j + G]]
                tap = [x == "tap" for x in cls]
                rec = dict(buoc=self.state.global_step, arm=arm, key=inputs[j]["key"], lop=k,
                           day_truoc=round(float(sum(out["advantages"][j + i].item()
                                                     for i in range(G) if tap[i])), 5),
                           n_tap=sum(tap), rong=sum(not s for s in txt[j:j + G]))
                if k in CTG_LOP:
                    c = [int(x == k) for x in cls]
                    rec.update(self.ctg.nhom(k, c, out["advantages"][j:j + G], tap, self.apply))
                dong.append(rec)
            with open(self.log_path, "a", encoding="utf-8") as f:
                for r in dong:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            return out

    return CTGTrainer


def lam_callback(trainer):
    from transformers import TrainerCallback

    class LuuCTG(TrainerCallback):
        def on_save(self, args, state, control, **kw):
            p = os.path.join(args.output_dir, f"checkpoint-{state.global_step}", "ctg_state.json")
            json.dump({"buoc": state.global_step, **trainer.ctg.to_dict()}, open(p, "w"), indent=1)
            print(f"[ctg_state] lưu {p} · λ {trainer.ctg.lam}", flush=True)

    return LuuCTG()


# ============================ câu nhắc ============================
def hang(bundle, arm, n):
    from grpo_spice import dung_hang
    rows, bo = dung_hang(bundle, n=n)
    for r in rows:
        r["lop"] = lop(r["gold"])
    if arm == "A4":
        cnt = collections.Counter(r["lop"] for r in rows)
        w = {k: (math.log(1 + len(rows) / cnt[k]) if k in CTG_LOP else 1.0) for k in cnt}
        rng = random.Random(SEED)
        rows = rng.choices(rows, weights=[w[r["lop"]] for r in rows], k=len(rows))
        print(f"[A4] trọng số lớp {({k: round(v, 3) for k, v in w.items()})}", flush=True)
    return rows, bo


def in_phan_bo(rows):
    cnt = collections.Counter(r["lop"] for r in rows)
    print("[lớp vàng theo câu chuẩn]", dict(cnt.most_common()), flush=True)
    MAP = {"click": "tap", "long_press": "long_press", "scroll": "scroll", "input_text": "type",
           "navigate_back": "navigate_back"}
    co = [r for r in rows if r["action_type"] in MAP]
    khop = sum(MAP[r["action_type"]] == r["lop"] for r in co)
    print(f"[khớp lớp vàng với action_type] {khop}/{len(co)} = {100*khop/max(1,len(co)):.1f}% "
          f"(bước có action_type ánh xạ được; open_app/wait/navigate_home không tính)", flush=True)
    for at in ("scroll", "input_text", "navigate_back"):
        x = [r for r in co if r["action_type"] == at]
        if x:
            print(f"    {at}: {sum(MAP[at] == r['lop'] for r in x)}/{len(x)} câu chuẩn quy đúng lớp", flush=True)
    return cnt


# ============================ tự kiểm 0 GPU ============================
def selftest_cider(a):
    C1 = [json.loads(l) for l in open(a.c1_mau, encoding="utf-8")]
    recs = [json.loads(l) for l in open(a.c1_recs, encoding="utf-8")]
    M = json.load(open(a.metric))
    assert [(r["episode_id"], r["step_id"]) for r in recs] == [(d["episode_id"], d["step_id"]) for d in C1]
    gold = [r["gold_instruction"] for r in recs]
    cd = CiderD(gold)
    trung, best = 0, 0
    lech = []
    for i, d in enumerate(C1):
        cau = [d["greedy"]] + d["mau"]
        s = [cd.score(c, [gold[i]]) for c in cau]
        ref = [M["ciderD"][k][i] for k in range(9)]
        for k in range(9):
            if abs(s[k] - ref[k]) < 1e-6:
                trung += 1
            else:
                lech.append((round(s[k] - ref[k], 3), cau[k][:60]))
        best += max(range(9), key=lambda k: (s[k], -k)) == max(range(9), key=lambda k: (ref[k], -k))
    print(f"[tái lập CIDEr-D] trùng tuyệt đối {trung}/3600 (cần ≥ 3480) · chọn cùng câu tốt nhất {best}/400 (cần ≥ 399)")
    for x in lech[:8]:
        print("   lệch", x)
    assert trung >= 3480 and best >= 399, "⛔ r_cider không tái lập pycocoevalcap"
    print("✅ tái lập CIDEr-D ĐẠT")


def selftest(a):
    dung_cider(a.bundle)
    kiem_thuong()
    rows, bo = hang(a.bundle, "A3", a.n_prompt)
    print(f"[câu nhắc] {len(rows)} · bỏ {bo}")
    assert len(rows) == a.n_prompt, len(rows)
    in_phan_bo(rows)
    r4, _ = hang(a.bundle, "A4", a.n_prompt)
    print("[A4 sau lấy mẫu lại]", dict(collections.Counter(r["lop"] for r in r4).most_common()))
    assert len(r4) == a.n_prompt

    import torch
    ctg = CTG()
    adv = torch.tensor([1.0, -1.0, 0.5, -0.5, 0.2, -0.2, 0.0, 0.0])
    goc = adv.clone()
    rec = ctg.nhom("scroll", [1, 0, 0, 0, 0, 0, 0, 0], adv, [False] + [True] * 7, apply=True)
    print("[CTG một nhóm]", rec)
    assert adv[0] > goc[0] and all(adv[i] < goc[i] for i in range(1, 8)), "⛔ CTG không đẩy câu đúng loại lên"
    assert ctg.lam["scroll"] > LAM0, "⛔ λ không tăng khi ĉ dưới đích"
    adv2 = goc.clone()
    CTG().nhom("scroll", [0] * 8, adv2, [True] * 8, apply=True)
    assert torch.equal(adv2, goc), "⛔ std(c)=0 mà vẫn cộng"
    adv3 = goc.clone()
    CTG().nhom("scroll", [1, 0, 0, 0, 0, 0, 0, 0], adv3, [False] + [True] * 7, apply=False)
    assert torch.equal(adv3, goc), "⛔ A2 mà vẫn cộng"
    c = CTG()
    for _ in range(200):
        c.nhom("type", [1] * 8, torch.zeros(8), [False] * 8, apply=False)
    assert c.lam["type"] == 0.0, c.lam
    print("[CTG] λ về 0 khi mô hình giữ đích ⇒ đúng")
    print("✅ selftest ĐẠT")


# ============================ train ============================
def train(a):
    import torch, trl, transformers, peft
    from peft import LoraConfig, get_peft_model
    from trl import GRPOConfig
    from datasets import Dataset, Image as HFImage
    from grpo_spice import nap, _n_s1, sinh_theo_khuc

    print(f"[nhánh] {a.arm} · trl {trl.__version__} · transformers {transformers.__version__} · "
          f"peft {peft.__version__} · torch {torch.__version__}", flush=True)
    assert trl.__version__ == "0.29.1", "⛔ CTG chỉ đối chiếu với mã TRL 0.29.1"

    dung_cider(a.bundle)
    kiem_thuong()

    proc, model, dt = nap(a)
    proc.tokenizer.padding_side = "left"

    s1 = json.load(open(os.path.join(a.adapter, "adapter_config.json"), encoding="utf-8"))
    lc = LoraConfig(r=s1["r"], lora_alpha=s1["lora_alpha"], lora_dropout=0.0, bias="none",
                    target_modules=s1["target_modules"], task_type="CAUSAL_LM")
    model = get_peft_model(model, lc)
    model.enable_input_require_grads()

    ntr = 0
    for n, p_ in model.named_parameters():
        if p_.requires_grad:
            if "visual" in n:
                raise SystemExit(f"⛔ tháp thị giác đang học: {n}")
            if p_.dtype != torch.float32:
                p_.data = p_.data.float()
            ntr += p_.numel()
    ns1 = _n_s1(a.adapter)
    print(f"[LoRA mới] tham số học {ntr:,} · S1 có {ns1:,}", flush=True)
    assert ntr == ns1, "⛔ LoRA mới không cùng cỡ S1"

    rows, bo = hang(a.bundle, a.arm, a.n_prompt)
    print(f"[câu nhắc] {len(rows)} · bỏ {bo} · n_char max {max(r['n_char'] for r in rows)}", flush=True)
    assert len(rows) == a.n_prompt
    in_phan_bo(rows)

    os.makedirs(a.out, exist_ok=True)
    json.dump([r["key"] for r in rows], open(os.path.join(a.out, "prompt_keys.json"), "w"))
    ds = Dataset.from_list(rows).cast_column("image", HFImage())

    bf = dt == torch.bfloat16
    want = dict(
        output_dir=a.out, seed=SEED, bf16=bf, fp16=not bf,
        gradient_checkpointing=True, gradient_checkpointing_kwargs={"use_reentrant": False},
        num_generations=a.G, per_device_train_batch_size=a.bs, gradient_accumulation_steps=a.accum,
        steps_per_generation=a.accum,
        max_completion_length=96, temperature=1.0, top_p=1.0, top_k=0, repetition_penalty=1.0,
        beta=0.04, learning_rate=1e-5, lr_scheduler_type="constant_with_warmup", warmup_steps=10,
        max_steps=a.max_steps, num_train_epochs=1,
        scale_rewards="group", loss_type="dapo", num_iterations=1,
        mask_truncated_completions=True, log_completions=False,
        logging_steps=1, save_steps=a.save_steps, save_total_limit=None,
        report_to="none", remove_unused_columns=False, dataloader_num_workers=2,
        disable_tqdm=True, max_grad_norm=1.0,
    )
    F = {f.name for f in dataclasses.fields(GRPOConfig)}
    thieu = sorted(set(want) - F)
    assert not thieu, f"⛔ GRPOConfig thiếu khoá {thieu}"
    args = GRPOConfig(**want)
    print("GRPOConfig:", {k: getattr(args, k, None) for k in (
        "num_generations", "per_device_train_batch_size", "gradient_accumulation_steps",
        "generation_batch_size", "steps_per_generation", "num_iterations", "beta", "learning_rate",
        "loss_type", "scale_rewards", "temperature", "max_steps", "save_steps", "bf16", "fp16")}, flush=True)
    gb = args.generation_batch_size
    print(f"[lô] mỗi lượt sinh {gb} câu = {gb // a.G} câu nhắc × {a.G}", flush=True)
    assert args.steps_per_generation <= args.gradient_accumulation_steps and args.num_iterations == 1, \
        "⛔ old_per_token_logps khác None ⇒ tỉ số PPO ≠ 1, khác thiết kế 276 §3"

    funcs = [r_cider] + ([r_loai] if a.arm == "A7" else [])
    Trainer = lam_ctg_trainer(a.arm, a.out)
    trainer = Trainer(model=model, reward_funcs=funcs, args=args, train_dataset=ds, processing_class=proc)
    trainer.add_callback(lam_callback(trainer))
    print(f"[thưởng] {[f.__name__ for f in funcs]} · CTG cộng vào advantage: {Trainer.apply} · "
          f"λ₀ {LAM0} · đích {P_DICH}", flush=True)

    if a.gen_chunk:
        sinh_theo_khuc(trainer.model, a.gen_chunk, proc.tokenizer.pad_token_id)
        print(f"[sinh theo khúc] bật, mỗi khúc ≤ {a.gen_chunk} chuỗi", flush=True)

    can = ("trainer_state.json", "optimizer.pt", "adapter_model.safetensors", "ctg_state.json")
    resume = a.resume
    if resume == "auto":
        ck = sorted((p for p in glob.glob(os.path.join(a.out, "checkpoint-*"))
                     if all(os.path.exists(os.path.join(p, f)) for f in can)),
                    key=lambda p: int(p.rsplit("-", 1)[1]))
        co = glob.glob(os.path.join(a.out, "checkpoint-*"))
        assert ck or not co, f"DỪNG: có {len(co)} điểm lưu mà không cái nào đủ tệp {can}"
        resume = ck[-1] if ck else None
    print("[tiếp từ]", resume, flush=True)

    if resume:
        # như grpo_spice.py: transformers chỉ nạp thư mục con ref/, phải nạp tay adapter default
        from safetensors.torch import load_file
        from peft import set_peft_model_state_dict
        nB = lambda: sum(p.float().norm().item() for n, p in trainer.model.named_parameters()
                         if "lora_B" in n and ".default." in n)
        truoc = nB()
        sd = load_file(os.path.join(resume, "adapter_model.safetensors"))
        kq = set_peft_model_state_dict(trainer.model, sd, adapter_name="default")
        la = [k for k in getattr(kq, "unexpected_keys", []) if "lora" in k]
        sau = nB()
        print(f"[nạp default] {len(sd)} tensor · |lora_B| {truoc:.4f} → {sau:.4f} · khoá lạ {len(la)}", flush=True)
        assert sau > 0 and not la, "DỪNG: không nạp được adapter default từ điểm lưu"
        st = json.load(open(os.path.join(resume, "ctg_state.json")))
        trainer.ctg.nap(st)
        print(f"[nạp ctg_state] bước {st['buoc']} · λ {trainer.ctg.lam} · ĉ {trainer.ctg.chat}", flush=True)

    torch.cuda.reset_peak_memory_stats()
    t0 = time.time()
    trainer.train(resume_from_checkpoint=resume)
    el = time.time() - t0
    buoc = max(trainer.state.global_step - (int(resume.rsplit("-", 1)[1]) if resume else 0), 1)
    print(f"[xong] {buoc} bước · {el/60:.1f} phút · {el/buoc:.1f} s/bước · "
          f"đỉnh VRAM {torch.cuda.max_memory_allocated()/2**30:.2f} GiB · λ cuối {trainer.ctg.lam}", flush=True)
    trainer.save_model(os.path.join(a.out, "final"))
    json.dump(trainer.state.log_history, open(os.path.join(a.out, "log_history.json"), "w"), indent=1)


# ============================ P0(b): log-prob động từ chạm ============================
TAP_VERB = ["Click", "click", "Tap", "tap", "Select", "select", "Open", "open", "Press", "press", "Choose"]


def logp_probe(a):
    import torch
    from PIL import Image
    from peft import PeftModel
    from grpo_spice import nap, nap_ocr, body_of, SEED_C1
    from build_branch_data import SYS

    proc, model, _ = nap(a)
    tk = proc.tokenizer
    ids_tap = sorted({tk.encode(w, add_special_tokens=False)[0] for w in TAP_VERB})
    print("[token động từ chạm]", [tk.decode([i]) for i in ids_tap], flush=True)

    va = [json.loads(l) for l in open(os.path.join(a.bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    rows = random.Random(SEED_C1).sample(va, 400)
    C1 = [json.loads(l) for l in open(a.c1, encoding="utf-8")]
    assert [(r["episode_id"], r["step_id"]) for r in rows] == [(d["episode_id"], d["step_id"]) for d in C1]
    chon = [(r, d) for r, d in zip(rows, C1) if lop(d["gold"]) in CTG_LOP]
    print(f"[câu nhắc] {len(chon)} bước C1 có lớp vàng scroll/type/navigate_back", flush=True)
    ocr = nap_ocr(a.bundle)

    cks = dict(x.split("=", 1) for x in a.ckpts.split(",")) if a.ckpts else {}
    ten0 = None
    for ten, p in cks.items():
        if ten0 is None:
            model = PeftModel.from_pretrained(model, p, adapter_name=ten)
            ten0 = ten
        else:
            model.load_adapter(p, adapter_name=ten)
        print(f"[adapter] {ten} ← {p}", flush=True)
    model.eval()

    def mot_buoc(r, d):
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body_of(r, ocr)}]}]
        txt = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(a.bundle, r["image"])).convert("RGB")
        P = proc(text=[txt], images=[img], return_tensors="pt").to(model.device)
        L = P["input_ids"].shape[1]
        g = tk(d["gold"], add_special_tokens=False, return_tensors="pt")["input_ids"].to(model.device)
        full = torch.cat([P["input_ids"], g], 1)
        kw = {k: v for k, v in P.items() if k not in ("input_ids", "attention_mask")}
        with torch.no_grad():
            lg = model(input_ids=full, attention_mask=torch.ones_like(full), **kw).logits.float()
        lp = torch.log_softmax(lg[0], -1)
        p_tap = torch.logsumexp(lp[L - 1, ids_tap], 0).item()
        tgt = full[0, L:]
        lp_gold = lp[L - 1:full.shape[1] - 1].gather(1, tgt[:, None]).mean().item()
        return p_tap, lp_gold

    KQ = {}
    for ten in ["S1"] + list(cks):
        t0 = time.time()
        res = []
        for r, d in chon:
            if ten == "S1":
                with model.disable_adapter() if cks else _null():
                    res.append(mot_buoc(r, d))
            else:
                model.set_adapter(ten)
                res.append(mot_buoc(r, d))
        KQ[ten] = res
        theo = collections.defaultdict(list)
        for (pt, lg), (_, d) in zip(res, chon):
            theo[lop(d["gold"])].append((pt, lg))
        print(f"[{ten}] {(time.time()-t0)/60:.1f} phút · " + " · ".join(
            f"{k} n={len(v)}: log P(động từ chạm ở token đầu) TB {sum(x[0] for x in v)/len(v):.3f}"
            f", logp/token câu chuẩn TB {sum(x[1] for x in v)/len(v):.3f}" for k, v in sorted(theo.items())),
            flush=True)

    keys = [f"{r['episode_id']}_{r['step_id']}" for r, _ in chon]
    json.dump({"keys": keys, "lop": [lop(d["gold"]) for _, d in chon], "kq": KQ},
              open(a.out, "w"), indent=0)
    sc = [i for i, (_, d) in enumerate(chon) if lop(d["gold"]) == "scroll"]
    tb = {t: sum(KQ[t][i][0] for i in sc) / len(sc) for t in KQ}
    print("[P0(b) scroll] log P(động từ chạm) TB:", {t: round(v, 3) for t, v in tb.items()}, flush=True)
    if "ck250" in tb and "ck500" in tb:
        dat = tb["ck500"] > tb["S1"] and tb["ck250"] >= tb["S1"] - 0.05
        print("✅ P0(b) ĐẠT: lực kéo về câu chạm tăng theo điểm lưu" if dat else
              "⛔ P0(b) KHÔNG ĐẠT: không tăng theo điểm lưu ⇒ DỪNG, báo user trước khi thuê A100", flush=True)


class _null:
    def __enter__(self):
        return self

    def __exit__(self, *x):
        return False


def main():
    ap = argparse.ArgumentParser()
    for f in ("--selftest-cider", "--selftest", "--train", "--logp-probe"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--arm", choices=("A3", "A2", "A4", "A7"), default="A3")
    ap.add_argument("--bundle")
    ap.add_argument("--merged", default="/kaggle/working/s1_merged")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--out")
    ap.add_argument("--c1")
    ap.add_argument("--ckpts", default="")
    ap.add_argument("--c1-recs")
    ap.add_argument("--c1-mau")
    ap.add_argument("--metric")
    ap.add_argument("--n-prompt", type=int, default=N_PROMPT)
    ap.add_argument("--G", type=int, default=8)
    ap.add_argument("--bs", type=int, default=4)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--max-steps", type=int, default=1000)
    ap.add_argument("--save-steps", type=int, default=250)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--no-q4", dest="q4", action="store_false")
    ap.add_argument("--gen-chunk", type=int, default=0)
    a = ap.parse_args()
    if a.bundle:
        a.adapter = a.adapter or os.path.join(a.bundle, "adapter_s1_seed101")

    if a.selftest_cider:
        selftest_cider(a)
    elif a.selftest:
        selftest(a)
    elif a.train:
        assert a.out, "cần --out"
        train(a)
    elif a.logp_probe:
        assert a.c1 and a.out, "cần --c1 và --out"
        logp_probe(a)
    else:
        ap.error("chọn một chế độ")


if __name__ == "__main__":
    main()
