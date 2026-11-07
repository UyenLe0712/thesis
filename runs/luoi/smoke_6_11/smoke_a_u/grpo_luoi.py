"""Lưới GRPO (report/323 §8): đổi đúng MỘT yếu tố so với ck500, giữ nguyên mọi thứ khác.

Trục 1 — thuật toán (--algo), phần thưởng giữ SPICE. Với num_iterations = 1 (như ck500) tỉ số
PPO luôn bằng 1, nên các thuật toán dưới đây chỉ khác nhau ở MỐC TRỪ và CHUẨN HOÁ lợi thế:
  grpo       A = (r - mean_nhóm) / std_nhóm                     (ck500, TRL mặc định)
  drgrpo     A =  r - mean_nhóm                                  (scale_rewards="none", như Dr. GRPO)
  rloo       A = (r - mean của G-1 câu còn lại) = G/(G-1)·(r - mean_nhóm)
  reinforce  A =  r - b,  b = trung bình trượt (0,9) của thưởng TB mỗi lô, không phụ thuộc câu nhắc
  scst       A =  r - r(câu greedy của chính câu nhắc đó)

Trục 2 — phần thưởng (--reward), thuật toán giữ grpo. Mọi phần thưởng cùng dạng
  r = điểm(câu, câu chuẩn) - 0,02·max(0, số từ câu - số từ câu chuẩn - 3),  câu rỗng = 0,
với điểm đưa về khoảng [0, 1] để phần phạt độ dài có cùng trọng số như ở ck500.

Không sửa grpo_spice.py: ck500/xao101 vẫn tái lập đúng bằng tệp cũ. Tệp này nạp lại các hàm của nó.

  python grpo_luoi.py --selftest-thuong --bundle B          # CPU: kiểm mọi phần thưởng
  python grpo_luoi.py --selftest-algo                        # CPU: kiểm công thức lợi thế
  python grpo_luoi.py --train --algo rloo --reward spice --bundle B --merged M --out O --resume auto
"""
import os, sys, json, time, glob, math, copy, random, argparse, dataclasses
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_spice as GS                                   # noqa: E402

ALGOS = ("grpo", "drgrpo", "rloo", "reinforce", "scst")
REWARDS = ("spice", "cider", "bleu4", "rougel", "chrf", "meteor", "bertscore", "spider")
EMA = 0.9
LAST = {}                                                 # thưởng của lần gọi gần nhất (để tính lại lợi thế)


# ============================ phần thưởng ============================
PUNCT = {"''", "'", "``", "`", "-LRB-", "-RRB-", "-LCB-", "-RCB-", ".", "?", "!", ",", ":", "-", "--",
         "...", ";", '"', "(", ")", "[", "]", "{", "}"}


def tok(s):
    """Xấp xỉ PTBTokenizer của pycocoevalcap (cùng hàm ctg_grpo.py đã kiểm tái lập CIDEr-D)."""
    import re
    s = (s or "").lower().replace("“", '"').replace("”", '"').replace("’", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    T = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-./][a-z0-9]+)*|[^\sa-z0-9]")
    return [t for t in T.findall(s) if t not in PUNCT and t != ""]


def _ngrams(ws, n=4):
    c = defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(ws) - k + 1):
            c[tuple(ws[i:i + k])] += 1
    return c


class CiderD:
    """CIDEr-D theo công thức pycocoevalcap (sigma 6, clip, x10), df CỐ ĐỊNH từ câu chuẩn tập dạy."""

    def __init__(self, ref_corpus, n=4, sigma=6.0):
        self.n, self.sigma = n, sigma
        self.df = defaultdict(float)
        for r in ref_corpus:
            for ng in set(_ngrams(tok(r), n)):
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

    def score(self, cand, ref):
        vh, nh, lh = self._vec(_ngrams(tok(cand), self.n))
        vr, nr, lr = self._vec(_ngrams(tok(ref), self.n))
        pen = math.exp(-((lh - lr) ** 2) / (2 * self.sigma ** 2))
        tot = 0.0
        for k in range(self.n):
            v = sum(min(w, vr[k].get(ng, 0.0)) * vr[k].get(ng, 0.0) for ng, w in vh[k].items())
            if nh[k] != 0 and nr[k] != 0:
                v /= nh[k] * nr[k]
            tot += v * pen
        return 10.0 * tot / self.n


M = {}   # bộ chấm dựng một lần


def dung_bo_cham(name, bundle):
    if name in ("cider", "spider"):
        tr = [json.loads(l) for l in open(os.path.join(bundle, "p1_train_rows.jsonl"), encoding="utf-8")]
        refs = [(r.get("target_instruction") or "").strip() for r in tr]
        refs = [r for r in refs if r]
        M["cider"] = CiderD(refs)
        print(f"[cider] df dựng từ {len(refs)} câu chuẩn của p1_train_rows.jsonl", flush=True)
    if name == "rougel":
        from pycocoevalcap.rouge.rouge import Rouge
        M["rouge"] = Rouge()
    if name == "meteor":
        from pycocoevalcap.meteor.meteor import Meteor
        M["meteor"] = Meteor()
    if name == "bertscore":
        import torch
        from bert_score import BERTScorer
        M["bert"] = BERTScorer(model_type="roberta-large", num_layers=17, lang="en",
                               rescale_with_baseline=True,
                               device=("cuda" if torch.cuda.is_available() else "cpu"))
        print("[bertscore] roberta-large tầng 17, đã hiệu chỉnh theo đường cơ sở", flush=True)


def diem(name, sents, golds):
    """Điểm thô trong [0, 1] (BERTScore đã hiệu chỉnh có thể < 0), cho câu KHÔNG rỗng."""
    if name == "spice":
        return GS.spice_batch(sents, golds)
    if name == "cider":
        return [M["cider"].score(s, g) / 10.0 for s, g in zip(sents, golds)]
    if name == "spider":
        sp = GS.spice_batch(sents, golds)
        return [0.5 * a + 0.5 * M["cider"].score(s, g) / 10.0 for a, s, g in zip(sp, sents, golds)]
    if name == "bleu4":
        import sacrebleu
        return [sacrebleu.sentence_bleu(s, [g], lowercase=True).score / 100.0 for s, g in zip(sents, golds)]
    if name == "chrf":
        import sacrebleu
        return [sacrebleu.sentence_chrf(s, [g]).score / 100.0 for s, g in zip(sents, golds)]
    if name == "rougel":
        return [M["rouge"].calc_score([" ".join(tok(s))], [" ".join(tok(g))]) for s, g in zip(sents, golds)]
    if name == "meteor":
        gts = {i: [" ".join(tok(g))] for i, g in enumerate(golds)}
        res = {i: [" ".join(tok(s))] for i, s in enumerate(sents)}
        _, sc = M["meteor"].compute_score(gts, res)
        return [float(x) for x in sc]
    if name == "bertscore":
        _, _, f = M["bert"].score(list(sents), list(golds))
        return [float(x) for x in f.tolist()]
    raise ValueError(name)


STAT = {"n": 0, "t": 0.0}


def lam_thuong(name):
    def thuong(completions, gold, **kw):
        t0 = time.time()
        sents = [GS._text(c).strip() for c in completions]
        idx = [i for i, s in enumerate(sents) if s]
        sc = diem(name, [sents[i] for i in idx], [gold[i] for i in idx]) if idx else []
        f = dict(zip(idx, sc))
        out = [0.0 if not s else f[i] - GS.MU * max(0, GS.nwords(s) - GS.nwords(g) - 3)
               for i, (s, g) in enumerate(zip(sents, gold))]
        LAST["r"] = list(out)
        dt = time.time() - t0
        STAT["n"] += 1
        STAT["t"] += dt
        print(f"[{name}] lần {STAT['n']} · {len(sents)} câu · {dt:.1f}s · thưởng TB {sum(out)/len(out):.3f}"
              f" · số từ TB {sum(map(GS.nwords, sents))/len(sents):.1f} · rỗng {len(sents) - len(idx)}",
              flush=True)
        return out
    thuong.__name__ = f"r_{name}"
    return thuong


# ============================ lợi thế ============================
def loi_the(algo, r, G, b=None, r_greedy=None):
    """r: danh sách thưởng theo thứ tự nhóm liền nhau (G câu/nhóm). Trả (A, b_mới)."""
    import torch
    r = torch.tensor(r, dtype=torch.float32).view(-1, G)
    m = r.mean(1, keepdim=True)
    if algo == "grpo":
        A = (r - m) / (r.std(1, keepdim=True) + 1e-4)
    elif algo == "drgrpo":
        A = r - m
    elif algo == "rloo":
        A = (r - m) * G / (G - 1)
    elif algo == "reinforce":
        b0 = float(r.mean()) if b is None else b
        A = r - b0
        b = EMA * b0 + (1 - EMA) * float(r.mean())
    elif algo == "scst":
        rb = torch.tensor(r_greedy, dtype=torch.float32).view(-1, 1)
        assert rb.shape[0] == r.shape[0], (rb.shape, r.shape)
        A = r - rb
    else:
        raise ValueError(algo)
    return A.flatten(), b


def lop_trainer():
    from trl import GRPOTrainer

    class LuoiTrainer(GRPOTrainer):
        algo = "grpo"
        thuong = None
        b = None
        _greedy = None
        _dang_greedy = False

        def _generate(self, prompts):
            out = super()._generate(prompts)
            if self.algo == "scst" and self.model.training and not self._dang_greedy:
                G = self.num_generations
                uniq = prompts[::G]
                mt = self._metrics["train"]
                snap = {k: len(v) for k, v in mt.items()}
                seen = self.state.num_input_tokens_seen
                gc, gk = self.generation_config, self.generation_kwargs
                gk2 = dict(gk, do_sample=False, temperature=None, top_p=None, top_k=None, min_p=None)
                from transformers import GenerationConfig
                self.generation_config, self.generation_kwargs = GenerationConfig(**gk2), gk2
                self._dang_greedy = True
                try:
                    g = super()._generate(uniq)
                finally:
                    self.generation_config, self.generation_kwargs = gc, gk
                    self._dang_greedy = False
                    for k in list(mt.keys()):            # bỏ số log của lượt greedy, giữ log của lượt lấy mẫu
                        if k in snap:
                            del mt[k][snap[k]:]
                        else:
                            del mt[k]
                    self.state.num_input_tokens_seen = seen
                    mt["num_tokens"] = [seen]
                self._greedy = [GS._text(c) for c in g[3]]
                assert len(self._greedy) == len(uniq)
            return out

        def _generate_and_score_completions(self, inputs):
            LAST.clear()
            self._greedy = None
            out = super()._generate_and_score_completions(inputs)
            if self.algo == "grpo" or not self.model.training:
                return out
            G = self.num_generations
            keys = [x["key"] for x in inputs]
            assert len(keys) % G == 0 and all(len(set(keys[i:i + G])) == 1 for i in range(0, len(keys), G)), \
                "⛔ các câu cùng nhóm không cùng câu nhắc"
            r = LAST["r"]
            assert len(r) == len(inputs) == out["advantages"].numel(), (len(r), len(inputs), out["advantages"].shape)
            rg = None
            if self.algo == "scst":
                assert self._greedy is not None, "⛔ SCST chưa sinh câu greedy"
                golds = [x["gold"] for x in inputs[::G]]
                rg = self.thuong(self._greedy, golds)
            A, self.b = loi_the(self.algo, r, G, b=self.b, r_greedy=rg)
            out["advantages"] = A.to(out["advantages"].device, dtype=out["advantages"].dtype)
            mt = self._metrics["train"]
            mt["luoi/adv_abs_mean"].append(float(A.abs().mean()))
            mt["luoi/frac_adv_zero"].append(float((A.abs() < 1e-6).float().mean()))
            if self.algo == "reinforce":
                mt["luoi/baseline"].append(float(self.b))
            if rg is not None:
                mt["luoi/r_greedy"].append(float(sum(rg) / len(rg)))
            return out

    return LuoiTrainer


def b_tu_log(resume):
    """Dựng lại mốc trượt REINFORCE từ log của điểm lưu (TRL ghi `reward` = thưởng TB mỗi bước)."""
    st = json.load(open(os.path.join(resume, "trainer_state.json")))
    rs = [h["reward"] for h in st["log_history"] if "reward" in h]
    b = None
    for x in rs:
        b0 = x if b is None else b
        b = EMA * b0 + (1 - EMA) * x
    return b, len(rs)


# ============================ train ============================
def train(a):
    import torch, trl, transformers, peft
    from peft import LoraConfig, get_peft_model
    from trl import GRPOConfig
    from datasets import Dataset, Image as HFImage

    print(f"[cấu hình] seed {a.seed} · thuật toán {a.algo} · thưởng {a.reward}", flush=True)
    print(f"trl {trl.__version__} · transformers {transformers.__version__} · "
          f"peft {peft.__version__} · torch {torch.__version__}", flush=True)
    dung_bo_cham(a.reward, a.bundle)
    thuong = lam_thuong(a.reward)

    proc, model, dt = GS.nap(a)
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
    ns1 = GS._n_s1(a.adapter)
    print(f"[LoRA mới] tham số học {ntr:,} · S1 có {ns1:,}", flush=True)
    assert ntr == ns1, "⛔ LoRA mới không cùng cỡ S1"

    rows, bo = GS.dung_hang(a.bundle, n=a.n_prompt, dai_nhat=(50 if a.probe else 0), seed=a.seed)
    print(f"[câu nhắc] {len(rows)} · bỏ {bo} · n_char max {max(r['n_char'] for r in rows)}", flush=True)
    os.makedirs(a.out, exist_ok=True)
    keys = [r["key"] for r in rows]
    json.dump(keys, open(os.path.join(a.out, "prompt_keys.json"), "w"))
    if a.keys_ck500:   # phải trùng đúng tập câu nhắc của ck500
        k0 = json.load(open(a.keys_ck500))
        assert keys == k0, "⛔ tập câu nhắc khác ck500"
        print("[câu nhắc] trùng thứ tự với ck500 ✓", flush=True)
    ds = Dataset.from_list(rows).cast_column("image", HFImage())

    bf = dt == torch.bfloat16
    gpu = torch.cuda.is_available()          # False chỉ ở phép thử CPU với mô hình tí hon
    want = dict(
        output_dir=a.out, seed=a.seed, bf16=bf and gpu, fp16=(not bf) and gpu,
        gradient_checkpointing=True, gradient_checkpointing_kwargs={"use_reentrant": False},
        num_generations=a.G, per_device_train_batch_size=a.bs, gradient_accumulation_steps=a.accum,
        max_completion_length=96, temperature=1.0, top_p=1.0, top_k=0, repetition_penalty=1.0,
        beta=a.beta, learning_rate=a.lr, lr_scheduler_type="constant_with_warmup", warmup_steps=10,
        max_steps=(20 if a.probe else a.max_steps), num_train_epochs=1,
        mask_truncated_completions=gpu,           # CPU tí hon không sinh EOS: tắt để phép thử đi qua gradient log_completions=a.probe, num_completions_to_print=2,
        logging_steps=1, save_steps=(10 ** 9 if a.probe else 25), save_total_limit=None,
        report_to="none", remove_unused_columns=False, dataloader_num_workers=2,
        disable_tqdm=True, max_grad_norm=1.0,
        scale_rewards=("none" if a.algo == "drgrpo" else "group"),
        loss_type="dapo", num_iterations=1,
    )
    F = {f.name for f in dataclasses.fields(GRPOConfig)}
    thieu = sorted(set(want) - F)
    assert not thieu, f"⛔ GRPOConfig thiếu khoá {thieu}"
    args = GRPOConfig(**want)
    print("GRPOConfig:", {k: getattr(args, k, None) for k in (
        "num_generations", "per_device_train_batch_size", "gradient_accumulation_steps",
        "generation_batch_size", "steps_per_generation", "num_iterations", "max_completion_length",
        "temperature", "top_p", "top_k", "beta", "learning_rate", "loss_type", "scale_rewards",
        "max_steps", "bf16", "fp16")}, flush=True)
    assert args.steps_per_generation * args.per_device_train_batch_size == args.generation_batch_size

    T = lop_trainer()
    trainer = T(model=model, reward_funcs=[thuong], args=args, train_dataset=ds, processing_class=proc)
    trainer.algo, trainer.thuong = a.algo, thuong
    if a.gen_chunk:
        GS.sinh_theo_khuc(trainer.model, a.gen_chunk, proc.tokenizer.pad_token_id)
        print(f"[sinh theo khúc] bật, mỗi khúc ≤ {a.gen_chunk} chuỗi", flush=True)

    resume = a.resume
    if resume == "auto":
        ck = sorted((p for p in glob.glob(os.path.join(a.out, "checkpoint-*"))
                     if all(os.path.exists(os.path.join(p, f)) for f in
                            ("trainer_state.json", "optimizer.pt", "adapter_model.safetensors"))),
                    key=lambda p: int(p.rsplit("-", 1)[1]))
        co = glob.glob(os.path.join(a.out, "checkpoint-*"))
        assert ck or not co, f"DỪNG: có {len(co)} điểm lưu mà không cái nào đủ tệp"
        resume = ck[-1] if ck else None
    print("[tiếp từ]", resume, flush=True)
    if resume:
        # lỗi 30/9: transformers chỉ nạp thư mục con ref/ của điểm lưu ⇒ nạp tay adapter default
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
        if a.algo == "reinforce":
            trainer.b, nb = b_tu_log(resume)
            print(f"[reinforce] mốc trượt dựng lại từ {nb} bước log: b = {trainer.b:.4f}", flush=True)

    if gpu:
        torch.cuda.reset_peak_memory_stats()
    t0 = time.time()
    trainer.train(resume_from_checkpoint=resume)
    el = time.time() - t0
    buoc = max(trainer.state.global_step - (int(resume.rsplit("-", 1)[1]) if resume else 0), 1)
    print(f"[xong] {buoc} bước · {el/60:.1f} phút · {el/buoc:.1f} s/bước · "
          f"đỉnh VRAM {(torch.cuda.max_memory_allocated()/2**30 if gpu else 0):.2f} GiB · "
          f"thưởng {STAT['t']/max(STAT['n'], 1):.1f} s/lần", flush=True)
    trainer.save_model(os.path.join(a.out, "final"))
    json.dump(trainer.state.log_history, open(os.path.join(a.out, "log_history.json"), "w"), indent=1)


# ============================ tự kiểm (CPU) ============================
def selftest_algo(_):
    import torch
    G = 4
    r = [0.2, 0.4, 0.6, 0.8, 0.5, 0.5, 0.5, 0.5]
    A, _ = loi_the("grpo", r, G)
    assert torch.allclose(A[:4], torch.tensor([-1.1619, -0.3873, 0.3873, 1.1619]), atol=1e-3), A
    assert torch.allclose(A[4:], torch.zeros(4)), A
    A, _ = loi_the("drgrpo", r, G)
    assert torch.allclose(A[:4], torch.tensor([-0.3, -0.1, 0.1, 0.3]), atol=1e-6), A
    A, _ = loi_the("rloo", r, G)        # 0,2 - TB(0,4; 0,6; 0,8) = -0,4
    assert abs(A[0] - (0.2 - (0.4 + 0.6 + 0.8) / 3)) < 1e-6, A
    A, b = loi_the("reinforce", r, G, b=None)
    assert abs(b - 0.5) < 1e-6 and abs(A[0] - (0.2 - 0.5)) < 1e-6, (A, b)
    A, b = loi_the("reinforce", [1.0] * 8, G, b=0.5)
    assert abs(A[0] - 0.5) < 1e-6 and abs(b - (0.9 * 0.5 + 0.1 * 1.0)) < 1e-6, (A, b)
    A, _ = loi_the("scst", r, G, r_greedy=[0.6, 0.5])
    assert torch.allclose(A, torch.tensor(r) - torch.tensor([0.6] * 4 + [0.5] * 4)), A
    print("✅ selftest công thức lợi thế ĐẠT (grpo · drgrpo · rloo · reinforce · scst)")


def selftest_thuong(a):
    gold = ["Click on the search bar", "Open the Clock app",
            "Click on the Settings icon at the top right corner"]
    cand = ["Click on the search bar", "",
            "Click on the Settings icon at the top right corner of the screen and then wait for it to open fully"]
    ten = a.rewards.split(",") if a.rewards else list(REWARDS)
    for name in ten:
        dung_bo_cham(name, a.bundle)
        r = lam_thuong(name)(cand, gold)
        print(f"  {name:10s} thưởng: {[round(x, 3) for x in r]}")
        assert r[0] > 0.9 and r[1] == 0.0 and r[2] < r[0], f"⛔ {name}: {r}"
        # câu sai phần tử phải thấp hơn câu đúng
        r2 = lam_thuong(name)(["Click on the search bar", "Click on the play button"],
                              ["Click on the search bar", "Click on the search bar"])
        assert r2[0] > r2[1], f"⛔ {name} không phân biệt phần tử: {r2}"
    print("✅ selftest phần thưởng ĐẠT:", ten)


def main():
    ap = argparse.ArgumentParser()
    for f in ("--selftest-thuong", "--selftest-algo", "--probe", "--train"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--bundle")
    ap.add_argument("--merged", default="/kaggle/working/s1_merged")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--out")
    ap.add_argument("--algo", choices=ALGOS, default="grpo")
    ap.add_argument("--reward", choices=REWARDS, default="spice")
    ap.add_argument("--rewards", default="")               # cho --selftest-thuong
    ap.add_argument("--keys-ck500", default="")            # prompt_keys.json của ck500 để đối chiếu
    ap.add_argument("--n-prompt", type=int, default=GS.N_PROMPT)
    ap.add_argument("--G", type=int, default=8)
    ap.add_argument("--bs", type=int, default=4)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--beta", type=float, default=0.04)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--max-steps", type=int, default=500)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--no-q4", dest="q4", action="store_false")
    ap.add_argument("--seed", type=int, default=GS.SEED)
    ap.add_argument("--gen-chunk", type=int, default=0)
    a = ap.parse_args()
    if a.selftest_algo:
        return selftest_algo(a)
    if a.selftest_thuong:
        return selftest_thuong(a)
    assert a.bundle and a.out and (a.train or a.probe), "cần --bundle, --out và --train/--probe"
    if a.algo != "grpo" and a.reward != "spice":
        raise SystemExit("⛔ lưới chỉ đổi MỘT yếu tố: đổi thuật toán thì giữ thưởng spice")
    a.adapter = a.adapter or os.path.join(a.bundle, "adapter_s1_seed101")
    GS.MODE.update(reward="spice", G=a.G, seed=a.seed)
    train(a)


if __name__ == "__main__":
    main()
