# -*- coding: utf-8 -*-
"""295 - GA-DPO: tối ưu ưu tiên (DPO + NLL) neo vào câu greedy của ck500, cặp chọn theo nhiều metric.

Đặt file này vào thư mục harness/ của repo (cạnh grpo_spice.py) rồi chạy:
  (1) lấy mẫu, GPU: python ga_dpo.py --mau --bundle B --merged M --ck500 CK --out mau.jsonl [--n 300] [--tu 1000]
  (2) dựng cặp, CPU+Java: python ga_dpo.py --cap --mau-file mau.jsonl --out cap.jsonl
  (3) train, A100:    python ga_dpo.py --train --bundle B --merged M --ck500 CK --cap-file cap.jsonl --out O [--kieu dpo|raft|gold]
  (4) gộp adapter để chấm bằng harness cũ (--ckpt):
      python tron_adapter.py --vao CK:1 --vao O/final:1 --ra O/ck500_cong_dpo
M = S1 đã hoà (như mọi lượt GRPO). CK = thư mục adapter ck500.
"""
import os, re, sys, json, time, math, random, argparse, collections, statistics as st

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SEED = 101
PIX = dict[str, int](min_pixels=200704, max_pixels=1003520)
BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
WORD = re.compile(r"[A-Za-z0-9'-]+")


def nwords(s):
    return len(WORD.findall(s or ""))


def msg_of(SYS, body):
    return [{"role": "system", "content": SYS},
            {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + body}]}]


# ---------- (1) lấy mẫu: greedy + k mẫu T=0,7 từ ck500 trên câu nhắc train KHÔNG thuộc 1.000 câu của ck500 ----------
def mau(a):
    import torch
    from PIL import Image
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
    from peft import PeftModel
    from grpo_spice import dung_hang, SYS, _dtype, _kw

    rows, bo = dung_hang(a.bundle, n=10 ** 9)
    print(f"[câu nhắc] tổng {len(rows)} · bỏ {bo} · dùng từ vị trí {a.tu} (0..{a.tu-1} là câu nhắc của ck500)", flush=True)
    rows = rows[a.tu:]
    if a.n:
        rows = rows[:a.n]
    dt = _dtype()
    proc = AutoProcessor.from_pretrained(BASE, **PIX)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(a.merged, device_map={"": 0}, **_kw(dt))
    model = PeftModel.from_pretrained(model, a.ck500).eval()
    done = set()
    if os.path.exists(a.out):
        done = {json.loads(l)["key"] for l in open(a.out, encoding="utf-8")}
    fo = open(a.out, "a", encoding="utf-8")
    t0, n = time.time(), 0
    for r in rows:
        if r["key"] in done:
            continue
        body = r["prompt"][1]["content"].lstrip("\n")
        text = proc.apply_chat_template(msg_of(SYS, body), tokenize=False, add_generation_prompt=True)
        img = Image.open(r["image"]).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                               temperature=None, top_p=None, top_k=None)
            torch.manual_seed(SEED + n)
            s = model.generate(**inp, max_new_tokens=96, do_sample=True, temperature=a.temp, top_p=1.0, top_k=0,
                               num_return_sequences=a.k, use_cache=True)
        fo.write(json.dumps(dict(key=r["key"], image=r["image"], body=body, gold=r["gold"],
                                 action_type=r["action_type"],
                                 greedy=proc.decode(g[0][L:], skip_special_tokens=True).strip(),
                                 mau=[proc.decode(x[L:], skip_special_tokens=True).strip() for x in s]),
                            ensure_ascii=False) + "\n")
        fo.flush()
        n += 1
        if n % 25 == 0:
            print(f"  {n} câu nhắc · {(time.time()-t0)/n:.1f} s/câu nhắc", flush=True)
    print(f"[mẫu] xong {n} câu nhắc mới · {(time.time()-t0)/60:.1f} phút", flush=True)


# ---------- (2) dựng cặp (CPU + Java cho SPICE) ----------
PUNCT = {"'", '"', "``", "''", "-lrb-", "-rrb-", "-lcb-", "-rcb-", ".", "?", "!", ",", ":", "-", "--", "...", ";"}
TOK = re.compile(r"n't|'s|'re|'ve|'ll|'d|'m|[a-z0-9]+(?:[-_/][a-z0-9]+)*|[^\sa-z0-9]")


def tok(s):
    s = (s or "").lower().replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")
    s = re.sub(r"(\w)n't\b", r"\1 n't", s)
    return [t for t in TOK.findall(s) if t not in PUNCT and t != ""]


def ngrams(ws, n=4):
    c = collections.defaultdict(int)
    for k in range(1, n + 1):
        for i in range(len(ws) - k + 1):
            c[tuple(ws[i:i + k])] += 1
    return c


class CiderD:
    def __init__(self, refs, n=4, sigma=6.0):
        self.n, self.sigma, self.df = n, sigma, collections.defaultdict(float)
        for r in refs:
            for ng in set(ngrams(tok(r), n)):
                self.df[ng] += 1
        self.log_n = math.log(float(len(refs)))

    def _vec(self, cnts):
        vec, norm, length = [dict() for _ in range(self.n)], [0.0] * self.n, 0
        for ng, tf in cnts.items():
            k = len(ng) - 1
            w = float(tf) * (self.log_n - math.log(max(1.0, self.df.get(ng, 0.0))))
            vec[k][ng] = w
            norm[k] += w * w
            if k == 1:
                length += tf
        return vec, [math.sqrt(x) for x in norm], length

    def score(self, cand, ref):
        vh, nh, lh = self._vec(ngrams(tok(cand), self.n))
        vr, nr, lr = self._vec(ngrams(tok(ref), self.n))
        pen = math.exp(-((lh - lr) ** 2) / (2 * self.sigma ** 2))
        tot = 0.0
        for k in range(self.n):
            v = sum(min(w, vr[k].get(ng, 0.0)) * vr[k].get(ng, 0.0) for ng, w in vh[k].items())
            if nh[k] and nr[k]:
                v /= nh[k] * nr[k]
            tot += v * pen
        return 10.0 * tot / self.n


def chrf(h, r, n=6, beta=2.0):
    h, r = (h or "").replace(" ", ""), (r or "").replace(" ", "")
    ps, rs = [], []
    for k in range(1, n + 1):
        hc = collections.Counter(h[i:i + k] for i in range(len(h) - k + 1))
        rc = collections.Counter(r[i:i + k] for i in range(len(r) - k + 1))
        m = sum(min(v, rc[x]) for x, v in hc.items())
        if hc:
            ps.append(m / sum(hc.values()))
        if rc:
            rs.append(m / sum(rc.values()))
    p, q = (st.mean(ps) if ps else 0.0), (st.mean(rs) if rs else 0.0)
    return 0.0 if p + q == 0 else (1 + beta ** 2) * p * q / (beta ** 2 * p + q)


def spice_many(cands, refs, chunk=2000):
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.spice.spice import Spice
    out = []
    for i in range(0, len(cands), chunk):
        c, r = cands[i:i + chunk], refs[i:i + chunk]
        tk = PTBTokenizer()
        g = tk.tokenize({j: [{"caption": x}] for j, x in enumerate(r)})
        h = tk.tokenize({j: [{"caption": x if x.strip() else "none"}] for j, x in enumerate(c)})
        _, sc = Spice().compute_score(g, h)
        for x, s in zip(sc, c):
            f = x["All"]["f"]
            out.append(0.0 if (not s.strip()) or f is None or f != f else float(f))
        print(f"  [spice] {min(i+chunk, len(cands))}/{len(cands)}", flush=True)
    return out


def cap(a):
    R = [json.loads(l) for l in open(a.mau_file, encoding="utf-8")]
    cid = CiderD([r["gold"] for r in R])
    flat = [(i, j, s) for i, r in enumerate(R) for j, s in enumerate([r["greedy"]] + r["mau"])]
    sp = spice_many([s for _, _, s in flat], [R[i]["gold"] for i, _, _ in flat])
    S = collections.defaultdict(dict)
    for (i, j, s), x in zip(flat, sp):
        S[i][j] = (x, cid.score(s, R[i]["gold"]), chrf(s, R[i]["gold"]))
    imp, keep = [], []
    for i, r in enumerate(R):
        cands = [r["greedy"]] + r["mau"]
        g = S[i][0]
        lg = nwords(r["gold"])
        best = None
        for j in range(1, len(cands)):
            y = S[i][j]
            ok = (y[0] >= g[0] + 0.05 and y[1] >= g[1] and y[2] >= g[2] and abs(nwords(cands[j]) - lg) <= 3
                  and cands[j].strip() and cands[j].strip() != r["greedy"].strip())
            if ok and (best is None or y[0] + y[1] / 10 > S[i][best][0] + S[i][best][1] / 10):
                best = j
        base = dict(key=r["key"], image=r["image"], body=r["body"], gold=r["gold"], greedy=r["greedy"])
        if best is not None:
            imp.append(dict(base, loai="cai_thien", chosen=cands[best], rejected=r["greedy"],
                            diem_chosen=S[i][best], diem_rejected=g))
        else:
            thua = [j for j in range(1, len(cands)) if all(S[i][j][m] < g[m] for m in range(3))
                    and cands[j].strip() != r["greedy"].strip()]
            if thua:
                w = min(thua, key=lambda j: sum(S[i][j]))
                keep.append(dict(base, loai="giu", chosen=r["greedy"], rejected=cands[w],
                                 diem_chosen=g, diem_rejected=S[i][w]))
    random.Random(SEED).shuffle(keep)
    keep = keep[:len(imp)]
    pairs = imp + keep
    random.Random(SEED).shuffle(pairs)
    with open(a.out, "w", encoding="utf-8") as fo:
        for p in pairs:
            fo.write(json.dumps(p, ensure_ascii=False) + "\n")
    ti = len(imp) / max(1, len(R))
    print(f"[cặp] {len(R)} câu nhắc · cặp cải thiện {len(imp)} ({100*ti:.1f}%) · cặp giữ {len(keep)} · tổng {len(pairs)}")
    print(f"[cặp] SPICE greedy TB {100*st.mean(S[i][0][0] for i in range(len(R))):.2f} · "
          f"greedy trùng hẳn câu chuẩn {sum(tok(r['greedy']) == tok(r['gold']) for r in R)}/{len(R)}")
    if imp:
        print(f"[cặp] ở cặp cải thiện: ΔSPICE TB {100*st.mean(p['diem_chosen'][0]-p['diem_rejected'][0] for p in imp):+.2f} · "
              f"ΔCIDER-D TB {100*st.mean(p['diem_chosen'][1]-p['diem_rejected'][1] for p in imp):+.1f}")
    print("CỔNG G1: tỉ lệ câu nhắc có cặp cải thiện ≥ 15% →", "ĐẠT" if ti >= 0.15 else "TRƯỢT (S1/ck500 đã thuộc câu chuẩn train)")


# ---------- (3) train: DPO + NLL viết tay (không phụ thuộc DPOTrainer cho VLM) ----------
def train(a):
    import torch
    import torch.nn.functional as F
    from PIL import Image
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration, get_cosine_schedule_with_warmup
    from peft import PeftModel, LoraConfig, get_peft_model
    from grpo_spice import SYS, _kw

    assert torch.cuda.get_device_capability()[0] >= 8, "DỪNG: train GA-DPO cần A100/L4 (giữ nền fp32 + autocast bf16)"
    torch.manual_seed(SEED)
    random.seed(SEED)
    proc = AutoProcessor.from_pretrained(BASE, **PIX)
    proc.tokenizer.padding_side = "right"
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(a.merged, device_map={"": 0}, **_kw(torch.float32))
    model = PeftModel.from_pretrained(model, a.ck500).merge_and_unload()  # nền = S1 + ck500, fp32, không làm tròn Δ
    cfg = json.load(open(os.path.join(a.ck500, "adapter_config.json")))
    model = get_peft_model(model, LoraConfig(r=cfg["r"], lora_alpha=cfg["lora_alpha"], lora_dropout=0.0, bias="none",
                                             target_modules=cfg["target_modules"], task_type="CAUSAL_LM"))
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    for n_, p_ in model.named_parameters():
        if p_.requires_grad and "visual" in n_:
            raise SystemExit(f"DỪNG: tháp thị giác đang học: {n_}")
    P = [json.loads(l) for l in open(a.cap_file, encoding="utf-8")]
    if a.kieu == "gold":
        P = [dict(p, chosen=p["gold"]) for p in P]
    print(f"[train] kiểu {a.kieu} · {len(P)} cặp · β {a.beta} · λ_nll {a.lam} · lr {a.lr}", flush=True)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr, weight_decay=0.0)
    steps = math.ceil(len(P) / a.accum)
    sch = get_cosine_schedule_with_warmup(opt, max(1, int(0.05 * steps)), steps)
    end = "<|im_end|>"

    def logps(texts, img, prompt_len):
        inp = proc(text=texts, images=[img] * len(texts), return_tensors="pt", padding=True).to(model.device)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            out = model(**inp)
        lg = out.logits[:, prompt_len - 1:-1].float()  # chỉ vị trí dự đoán token câu trả lời
        tgt = inp["input_ids"][:, prompt_len:]
        lp = torch.gather(F.log_softmax(lg, -1), 2, tgt.unsqueeze(-1)).squeeze(-1)
        mask = inp["attention_mask"][:, prompt_len:].float()
        return (lp * mask).sum(-1), mask.sum(-1)

    model.train()
    t0, log = time.time(), collections.defaultdict(list)
    for i, p in enumerate(P):
        prompt = proc.apply_chat_template(msg_of(SYS, p["body"]), tokenize=False, add_generation_prompt=True)
        img = Image.open(p["image"]).convert("RGB")
        L = proc(text=[prompt], images=[img], return_tensors="pt")["input_ids"].shape[1]
        txt = [prompt + p["chosen"] + end, prompt + p["rejected"] + end]
        if i == 0:
            ids = proc(text=txt[:1], images=[img], return_tensors="pt")["input_ids"][0]
            print(f"[kiểm] token trả lời: {proc.tokenizer.decode(ids[L:])!r} (phải là câu chosen + {end})", flush=True)
        if a.kieu == "dpo":
            with torch.no_grad(), model.disable_adapter():
                ref, _ = logps(txt, img, L)
            pol, ntok = logps(txt, img, L)
            marg = (pol[0] - ref[0]) - (pol[1] - ref[1])
            l_dpo = -F.logsigmoid(a.beta * marg)
            l_nll = -pol[0] / ntok[0]
            loss = l_dpo + a.lam * l_nll
            log["marg"].append(marg.item())
            log["acc"].append(float(marg.item() > 0))
            log["lp_c"].append((pol[0] / ntok[0]).item())
        else:                         # raft: NLL trên câu được chọn · gold: NLL trên câu chuẩn
            pol, ntok = logps(txt[:1], img, L)
            loss = -pol[0] / ntok[0]
            log["lp_c"].append(-loss.item())
        (loss / a.accum).backward()
        log["loss"].append(loss.item())
        if (i + 1) % a.accum == 0 or i + 1 == len(P):
            torch.nn.utils.clip_grad_norm_([q for q in model.parameters() if q.requires_grad], 1.0)
            opt.step(); sch.step(); opt.zero_grad(set_to_none=True)
            k = (i + 1) // a.accum
            if k % 10 == 0 or i + 1 == len(P):
                m = {x: st.mean(v[-a.accum * 10:]) for x, v in log.items()}
                print(f"  bước {k}/{steps} · " + " · ".join(f"{x} {y:.3f}" for x, y in m.items()) +
                      f" · {(time.time()-t0)/60:.1f} phút", flush=True)
    os.makedirs(os.path.join(a.out, "final"), exist_ok=True)
    model.save_pretrained(os.path.join(a.out, "final"))
    lp0, lp1 = st.mean(log["lp_c"][:100]), st.mean(log["lp_c"][-100:])
    print(f"[xong] {a.out}/final · log-p/token câu chosen: đầu {lp0:.3f} → cuối {lp1:.3f}", flush=True)
    if lp1 < lp0 - 0.10 * abs(lp0):
        print("⚠ log-p câu chosen giảm > 10% (dịch chuyển likelihood) — tăng --lam hoặc giảm --lr rồi chạy lại", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for f in ("--mau", "--cap", "--train"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--bundle"); ap.add_argument("--merged"); ap.add_argument("--ck500")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=0); ap.add_argument("--tu", type=int, default=1000)
    ap.add_argument("--k", type=int, default=8); ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--mau-file"); ap.add_argument("--cap-file")
    ap.add_argument("--kieu", choices=["dpo", "raft", "gold"], default="dpo")
    ap.add_argument("--beta", type=float, default=0.1); ap.add_argument("--lam", type=float, default=1.0)
    ap.add_argument("--lr", type=float, default=5e-6); ap.add_argument("--accum", type=int, default=16)
    a = ap.parse_args()
    if a.mau:
        mau(a)
    elif a.cap:
        cap(a)
    elif a.train:
        train(a)
    else:
        ap.error("chọn --mau / --cap / --train")
