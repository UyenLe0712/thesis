# -*- coding: utf-8 -*-
"""Lưới RL đợt 4 (report/329 §4, `report/reports/Baseline RL so với GRPO.md` E7–E11) + thưởng BCMR (report/330 §7).

Không sửa grpo_luoi.py / grpo_codien.py: tệp này thêm thuật toán, thêm phần thưởng rồi gọi main() của grpo_codien,
nên S1, 1.000 câu nhắc (cùng thứ tự với ck500), G = 8, lr, β = 0,04 (KL về S1), μ = 1, 500 bước giữ nguyên như ck500.

Thuật toán mới (--algo):
  rlce    Trộn RL + CE (Paulus 2018; SCST): mất mát GRPO + λ·CE(câu chuẩn | câu nhắc), thêm một lượt forward câu chuẩn
          mỗi lô nhỏ. λ = --ce-lam (mặc định 0,1 [suy]: CE/token của S1 trên câu chuẩn nhỏ hơn |A| của GRPO).
  mixer   MIXER bản rút gọn (Ranzato 2016), khai rõ: k = ⌊ρ_t · số token câu chuẩn⌋ token đầu của câu chuẩn được ép làm
          phần đầu của câu, mô hình sinh tiếp phần còn lại. Token ép học bằng CE (lợi thế = 1 trên từng token), phần sinh
          học bằng lợi thế GRPO của cả câu. ρ_t giảm tuyến tính từ --mixer-rho0 (0,5) về 0 ở --mixer-frac (0,5) số bước,
          sau đó là GRPO thuần. Khác bài gốc: bài gốc dùng ranh giới token cố định Δ tăng theo epoch và mốc hồi quy;
          ở đây ρ tính theo tỉ lệ câu, mốc là trung bình nhóm. Cùng nhóm G câu dùng cùng k nên so sánh trong nhóm công bằng.
  seqgan  SeqGAN bản rút gọn (Yu 2017), khai là ĐỔI CẢ PHẦN THƯỞNG: thưởng = D(câu | màn hình), D là MLP hai tầng trên
          trạng thái ẩn đã tách gradient của chính policy (vị trí cuối câu nhắc ‖ trung bình các vị trí của câu). Dương =
          câu chuẩn, âm = câu mẫu; D cập nhật một bước AdamW mỗi lô sinh, SAU khi đã chấm thưởng cho lô đó. Không có
          rollout Monte Carlo từng token (thưởng mức câu, lợi thế GRPO trong nhóm). --gan-warm bước đầu chỉ học D (A = 0).
          --gan-mix α: thưởng = α·SPICE + (1−α)·D, mặc định 0 (SeqGAN thuần). SPICE vẫn được tính để theo dõi.
  quark   Quark bản rút gọn (Lu 2022): chia thưởng thành K = --quark-k mức theo phân vị trên kho trượt --quark-pool câu
          gần nhất; câu mức k < K−1 được học lại với câu nhắc có thêm thẻ chữ " [quality k+1/K]" ở cuối lời người dùng,
          câu mức cao nhất học với câu nhắc gốc. Mất mát = CE (lợi thế = 1) + β·KL về S1 trên đúng câu nhắc có thẻ.
          Khác bài gốc: mức cao nhất là câu nhắc gốc (không thêm token mới vào từ vựng), nên sinh test KHÔNG cần đổi gì;
          không có kho phát lại (chỉ học lô vừa sinh), không có thưởng entropy.
  es      Evolution strategies trên trọng số LoRA (Salimans 2017; công thức cập nhật của Qiu 2025), không lan truyền
          ngược: mỗi bước --es-pop thành viên đối xứng θ ± σε, mỗi thành viên sinh greedy cho --es-m câu nhắc, độ thích
          nghi = thưởng TB, chuẩn hoá z-score trong quần thể, θ ← θ + lr·(1/n)·Σ z_i ε_i (KHÔNG chia σ, như Qiu; chia σ
          kiểu Salimans với lr 5e-4 làm mỗi bước dịch L2 ~170 trên 15 triệu tham số LoRA). Mặc định pop 16, m 2,
          σ 1e-3, lr 5e-4 (theo Qiu, chưa probe trên LoRA). 500 bước × m 2 = đúng 1.000 câu nhắc của ck500. Không có KL.
Phần thưởng mới (--reward, chỉ đi với --algo grpo):
  bcmr    (0,5·B1 + 0,5·B2 + B3 + B4 + CIDEr-D + 5·METEOR + 2·ROUGE-L) / 20 (Liu 2017, ICCV). BLEU-n mức câu của
          sacrebleu (effective order), CIDEr-D và METEOR, ROUGE-L như grpo_luoi. Chia 20 = tổng trọng số với CIDEr-D ≤ 10,
          đưa về cùng thang [0, 1] với SPICE để phạt độ dài 0,02/từ giữ trọng số như ck500.

  python grpo_moi_b2.py --selftest-algo
  python grpo_moi_b2.py --selftest-thuong --bundle B --rewards bcmr
  python grpo_moi_b2.py --train --algo seqgan --reward spice --bundle B --merged M --out O --resume auto [--gan-mix 0]
  python grpo_moi_b2.py --train --algo es --reward spice --bundle B --merged M --out O --resume auto [--es-pop 16]
Cờ chung giữ như grpo_luoi/grpo_codien (--no-q4, --bs, --accum, --gen-chunk, --G, --beta, --lr, --max-steps, --keys-ck500, ...);
ES bỏ qua --bs/--accum/--gen-chunk/--beta.
"""
import os, sys, json, time, glob, math, bisect, argparse, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_codien as CD                                  # noqa: E402
GL = CD.GL
GS = GL.GS

MOI = ("rlce", "mixer", "seqgan", "quark", "es")
RC = {"lam": 0.1}
MX = {"rho0": 0.5, "frac": 0.5}
GAN = {"mix": 0.0, "warm": 20, "lr": 1e-4, "hid": 256}
QK = {"k": 5, "pool": 2048}
ES = {"pop": 16, "m": 2, "sigma": 1e-3, "lr": 5e-4, "save": 25}

_loi_the = GL.loi_the
_lop = GL.lop_trainer
_train = GL.train
_bo_cham = GL.dung_bo_cham
_diem = GL.diem


# ============================ thưởng BCMR ============================
_BLEU = {}


def bleu_n(s, g, n):
    if n not in _BLEU:
        from sacrebleu.metrics import BLEU
        _BLEU[n] = BLEU(max_ngram_order=n, effective_order=True, lowercase=True)
    return _BLEU[n].sentence_score(s, [g]).score / 100.0


def dung_bo_cham(name, bundle):
    if name == "bcmr":
        for x in ("cider", "meteor", "rougel"):
            _bo_cham(x, bundle)
        print("[bcmr] (0,5·B1 + 0,5·B2 + B3 + B4 + CIDEr-D + 5·METEOR + 2·ROUGE-L) / 20", flush=True)
        return
    return _bo_cham(name, bundle)


def diem(name, sents, golds):
    if name != "bcmr":
        return _diem(name, sents, golds)
    me = _diem("meteor", sents, golds)
    ro = _diem("rougel", sents, golds)
    out = []
    for s, g, m, r in zip(sents, golds, me, ro):
        b = [bleu_n(s, g, n) for n in (1, 2, 3, 4)]
        c = GL.M["cider"].score(s, g)                        # CIDEr-D thô, 0..10
        out.append((0.5 * b[0] + 0.5 * b[1] + b[2] + b[3] + c + 5 * m + 2 * r) / 20.0)
    return out


# ============================ hàm thuần (tự kiểm được trên CPU) ============================
def loi_the(algo, r, G, b=None, r_greedy=None):
    import torch
    if algo == "quark":
        return torch.ones(len(r)), b
    if algo in ("rlce", "mixer", "seqgan", "es"):        # lợi thế GRPO; mixer/seqgan thay ở lớp con
        return _loi_the("grpo", r, G)
    return _loi_the(algo, r, G, b=b, r_greedy=r_greedy)


def rho_mixer(step, max_steps, rho0=None, frac=None):
    rho0 = MX["rho0"] if rho0 is None else rho0
    frac = MX["frac"] if frac is None else frac
    W = max(1, int(frac * max_steps))
    return rho0 * max(0.0, 1.0 - step / W)


def muc_quark(r, pool, K):
    """Mức phân vị (0..K−1) của từng thưởng trong kho đã sắp; hoà lấy hạng giữa."""
    n = len(pool)
    out = []
    for x in r:
        lo, hi = bisect.bisect_left(pool, x), bisect.bisect_right(pool, x)
        f = (lo + hi) / 2.0 / max(1, n)
        out.append(min(K - 1, int(f * K)))
    return out


def hang_tam(vals):
    """Fitness shaping (Salimans 2017): hạng → [−0,5; 0,5], hoà chia đều hạng."""
    n = len(vals)
    if n < 2:
        return [0.0] * n
    o = sorted(range(n), key=lambda i: vals[i])
    rk = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[o[j + 1]] == vals[o[i]]:
            j += 1
        for t in range(i, j + 1):
            rk[o[t]] = (i + j) / 2.0
        i = j + 1
    return [x / (n - 1) - 0.5 for x in rk]


def chuan_z(vals):
    """z-score trong quần thể (Qiu 2025); toàn hoà thì 0."""
    n = len(vals)
    m = sum(vals) / max(1, n)
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / max(1, n))
    return [0.0] * n if sd < 1e-12 else [(v - m) / sd for v in vals]


def chen_the(ids, the, duoi):
    """Chèn danh sách token `the` ngay trước lần xuất hiện CUỐI của `duoi` trong `ids`."""
    L = len(duoi)
    for i in range(len(ids) - L, -1, -1):
        if ids[i:i + L] == duoi:
            return ids[:i] + the + ids[i:]
    raise ValueError("không thấy đuôi câu nhắc <|im_end|>\\n<|im_start|>assistant\\n")


def selftest_moi(_):
    import torch
    CD.selftest_codien(_)
    r = [0.2, 0.4, 0.6, 0.8, 0.5, 0.5, 0.5, 0.5]
    A, _b = loi_the("quark", r, 4)
    assert A.tolist() == [1.0] * 8, A
    for al in ("rlce", "mixer", "seqgan", "es"):
        A, _b = loi_the(al, r, 4)
        assert torch.allclose(A, _loi_the("grpo", r, 4)[0]), (al, A)
    assert rho_mixer(0, 500, 0.5, 0.5) == 0.5 and abs(rho_mixer(125, 500, 0.5, 0.5) - 0.25) < 1e-9
    assert rho_mixer(250, 500, 0.5, 0.5) == 0.0 and rho_mixer(400, 500, 0.5, 0.5) == 0.0
    pool = sorted([0.1 * i for i in range(10)])
    assert muc_quark([0.0, 0.45, 0.9], pool, 5) == [0, 2, 4], muc_quark([0.0, 0.45, 0.9], pool, 5)
    assert muc_quark([1.0, 1.0], sorted([1.0] * 10), 5) == [2, 2]      # toàn hoà: mức giữa, không dồn về đáy
    u = hang_tam([3.0, 1.0, 2.0, 2.0])
    assert u == [0.5, -0.5, 0.0, 0.0], u
    assert hang_tam([1.0] * 4) == [0.0] * 4
    z = chuan_z([1.0, 3.0])
    assert z == [-1.0, 1.0] and chuan_z([2.0] * 3) == [0.0] * 3, z
    ids = [1, 2, 9, 3, 4, 5, 6, 9, 3, 4, 7, 8]
    assert chen_the(ids, [55, 56], [9, 3, 4]) == [1, 2, 9, 3, 4, 5, 6, 55, 56, 9, 3, 4, 7, 8]
    print("✅ selftest đợt 4 ĐẠT: quark · rlce · mixer · seqgan · es (hàm thuần)")


# ============================ lớp trainer ============================
def _tok(tr):
    return getattr(tr.processing_class, "tokenizer", tr.processing_class)


def _kw(inputs, P, T, img_id):
    """kwargs đa phương thức cho chuỗi (câu nhắc dài P) + (phần đuôi dài T) mới."""
    import torch
    kw = {k: inputs[k] for k in ("pixel_values", "image_grid_thw", "num_images", "pixel_attention_mask", "image_sizes")
          if k in inputs and inputs[k] is not None}
    for k in ("mm_token_type_ids", "token_type_ids"):
        if k in inputs and inputs[k] is not None:
            x = inputs[k][:, :P]
            kw[k] = torch.cat([x, x.new_zeros((x.size(0), T))], 1)
    return kw


def lop_trainer():
    import torch
    B = _lop()

    class MoiTrainer(B):
        _golds = None
        _mixer_k = None
        _resume = None
        _D = None
        _opt_D = None
        _pool = None
        _kiem_mm = False

        def train(self, resume_from_checkpoint=None, **kw):
            self._resume = resume_from_checkpoint
            return super().train(resume_from_checkpoint=resume_from_checkpoint, **kw)

        def _img_id(self):
            return _tok(self).convert_tokens_to_ids("<|image_pad|>")

        # ---------- MIXER: ép tiền tố câu chuẩn vào đầu phần sinh ----------
        def _generate_single_turn(self, prompt_ids, images, multimodal_fields):
            if self.algo != "mixer" or not self.model.training or self._golds is None:
                return super()._generate_single_turn(prompt_ids, images, multimodal_fields)
            assert len(self._golds) == len(prompt_ids), (len(self._golds), len(prompt_ids))
            tk, img = _tok(self), self._img_id()
            rho = rho_mixer(self.state.global_step, self.args.max_steps)
            pre = []
            for g in self._golds:
                t = tk(g, add_special_tokens=False)["input_ids"]
                pre.append(t[:int(math.floor(rho * len(t)))])
            mf = dict(multimodal_fields)
            assert "token_type_ids" not in mf, "⛔ mixer chưa hỗ trợ token_type_ids"
            if "mm_token_type_ids" in mf:
                if not self._kiem_mm:   # phép kiểm một lần: dựng lại mm_token_type_ids từ id phải trùng processor
                    v = mf["mm_token_type_ids"]
                    v = v.tolist() if hasattr(v, "tolist") else v
                    for p, row in zip(prompt_ids, v):
                        row = list(row)[-len(p):]
                        assert row == [1 if t == img else 0 for t in p], "⛔ mm_token_type_ids dựng lại lệch processor"
                    print("[mixer] kiểm mm_token_type_ids dựng lại trùng processor ✓", flush=True)
                    self._kiem_mm = True
                mf["mm_token_type_ids"] = [[1 if t == img else 0 for t in list(p) + q] for p, q in zip(prompt_ids, pre)]
            comp, lp, ex = super()._generate_single_turn([list(p) + q for p, q in zip(prompt_ids, pre)], images, mf)
            self._mixer_k = [len(q) for q in pre]
            self._mixer_rho = rho
            return [q + list(c) for q, c in zip(pre, comp)], lp, ex

        def _generate_and_score_completions(self, inputs):
            if not self.model.training or self.algo not in MOI:
                return super()._generate_and_score_completions(inputs)
            self._golds = [x["gold"] for x in inputs]
            self._mixer_k = None
            out = super()._generate_and_score_completions(inputs)
            self._golds = None
            G = self.num_generations
            mt = self._metrics["train"]
            dev = out["completion_ids"].device
            P, C = out["prompt_ids"].size(1), out["completion_ids"].size(1)
            img = self._img_id()
            golds = [x["gold"] for x in inputs]

            if self.algo == "rlce":
                L = [_tok(self)(g, add_special_tokens=False)["input_ids"] + [self.eos_token_id] for g in golds]
                T = max(map(len, L))
                gi = torch.full((len(L), T), self.pad_token_id, dtype=torch.long, device=dev)
                gm = torch.zeros_like(gi)
                for i, x in enumerate(L):
                    gi[i, :len(x)] = torch.tensor(x, device=dev)
                    gm[i, :len(x)] = 1
                out["gold_ids"], out["gold_mask"] = gi, gm

            elif self.algo == "mixer":
                ks = self._mixer_k
                assert ks is not None and len(ks) == out["completion_ids"].size(0)
                A = out["advantages"].view(-1, 1).expand(-1, C).clone()
                for i, k in enumerate(ks):
                    assert torch.equal(out["completion_ids"][i, :k].cpu(), torch.tensor(
                        _tok(self)(golds[i], add_special_tokens=False)["input_ids"][:k], dtype=torch.long)), "⛔ tiền tố ép lệch"
                    A[i, :k] = 1.0
                out["advantages"] = A
                mt["mixer/rho"].append(float(self._mixer_rho))
                mt["mixer/k_tb"].append(sum(ks) / len(ks))

            elif self.algo == "seqgan":
                kw = _kw(out, P, C, img)
                ids = torch.cat([out["prompt_ids"], out["completion_ids"]], 1)
                am = torch.cat([out["prompt_mask"], out["completion_mask"]], 1)
                f_gen = self._dac_trung(ids, am, C, kw)
                L = [_tok(self)(g, add_special_tokens=False)["input_ids"] + [self.eos_token_id] for g in golds]
                T = max(map(len, L))
                gi = torch.full((len(L), T), self.pad_token_id, dtype=torch.long, device=dev)
                gm = torch.zeros_like(gi)
                for i, x in enumerate(L):
                    gi[i, :len(x)] = torch.tensor(x, device=dev)
                    gm[i, :len(x)] = 1
                f_gold = self._dac_trung(torch.cat([out["prompt_ids"], gi], 1), torch.cat([out["prompt_mask"], gm], 1),
                                         T, _kw(out, P, T, img))[::G]
                D = self._mang_D(f_gen.size(-1), f_gen.device)
                with torch.no_grad():
                    rd = torch.sigmoid(D(f_gen).squeeze(-1))
                bce = torch.nn.functional.binary_cross_entropy_with_logits
                lg, lf = D(f_gold).squeeze(-1), D(f_gen).squeeze(-1)
                ld = bce(lg, torch.ones_like(lg)) + bce(lf, torch.zeros_like(lf))
                self._opt_D.zero_grad(set_to_none=True)
                ld.backward()
                self._opt_D.step()
                rs = torch.tensor(GL.LAST["r"], dtype=torch.float32, device=rd.device)
                txt = _tok(self).batch_decode(out["completion_ids"], skip_special_tokens=True)
                rong = torch.tensor([not t.strip() for t in txt], device=rd.device)
                r = GAN["mix"] * rs + (1 - GAN["mix"]) * rd
                r = torch.where(rong, torch.zeros_like(r), r)
                g = r.view(-1, G)
                A = ((g - g.mean(1, keepdim=True)) / (g.std(1, keepdim=True) + 1e-4)).flatten()
                if self.state.global_step < GAN["warm"]:
                    A = torch.zeros_like(A)
                out["advantages"] = A.to(out["advantages"].device, dtype=out["advantages"].dtype)
                mt["luoi/adv_abs_mean"][-1] = float(A.abs().mean())
                mt["luoi/frac_adv_zero"][-1] = float((A.abs() < 1e-6).float().mean())
                mt["seqgan/d_loss"].append(float(ld))
                mt["seqgan/d_real"].append(float(torch.sigmoid(lg).mean()))
                mt["seqgan/d_fake"].append(float(rd.mean()))
                mt["seqgan/r"].append(float(r.mean()))

            elif self.algo == "quark":
                K = QK["k"]
                if self._pool is None:
                    self._pool = collections.deque(maxlen=QK["pool"])
                    if self._resume and os.path.exists(os.path.join(self._resume, "quark_pool.json")):
                        self._pool.extend(json.load(open(os.path.join(self._resume, "quark_pool.json"))))
                        print(f"[quark] nạp kho {len(self._pool)} thưởng từ {self._resume}", flush=True)
                r = list(GL.LAST["r"])
                self._pool.extend(r)
                q = muc_quark(r, sorted(self._pool), K)
                tk = _tok(self)
                duoi = tk("<|im_end|>\n<|im_start|>assistant\n", add_special_tokens=False)["input_ids"]
                the = {k: tk(f" [quality {k + 1}/{K}]", add_special_tokens=False)["input_ids"] for k in range(K - 1)}
                rows = []
                for i in range(len(r)):
                    x = out["prompt_ids"][i][out["prompt_mask"][i].bool()].tolist()
                    rows.append(x if q[i] == K - 1 else chen_the(x, the[q[i]], duoi))
                P2 = max(map(len, rows))
                pid = torch.full((len(rows), P2), self.pad_token_id, dtype=torch.long, device=dev)
                pm = torch.zeros_like(pid)
                for i, x in enumerate(rows):
                    pid[i, P2 - len(x):] = torch.tensor(x, device=dev)
                    pm[i, P2 - len(x):] = 1
                if "mm_token_type_ids" in out:
                    mm0 = (out["prompt_ids"] == img).to(out["mm_token_type_ids"].dtype) * out["prompt_mask"].to(out["mm_token_type_ids"].dtype)
                    assert torch.equal(mm0, out["mm_token_type_ids"][:, :P]), "⛔ mm_token_type_ids dựng lại lệch processor"
                    mm = (pid == img).to(out["mm_token_type_ids"].dtype) * pm.to(out["mm_token_type_ids"].dtype)
                    out["mm_token_type_ids"] = torch.cat([mm, mm.new_zeros((mm.size(0), C))], 1)
                assert "token_type_ids" not in out and "old_per_token_logps" not in out, "⛔ quark cần μ = 1"
                out["prompt_ids"], out["prompt_mask"] = pid, pm
                if self.beta != 0.0:
                    kw = {k: out[k] for k in ("pixel_values", "image_grid_thw", "num_images", "mm_token_type_ids") if k in out}
                    with torch.no_grad(), self.accelerator.unwrap_model(self.model).disable_adapter():
                        ref, _ = self._get_per_token_logps_and_entropies(
                            self.model, torch.cat([pid, out["completion_ids"]], 1), torch.cat([pm, out["completion_mask"]], 1),
                            C, self.args.per_device_train_batch_size, **kw)
                    out["ref_per_token_logps"] = ref
                dem = collections.Counter(q)
                for k in range(K):
                    mt[f"quark/muc{k + 1}"].append(dem.get(k, 0) / len(q))
                mt["quark/kho"].append(len(self._pool))
            return out

        # ---------- RL + CE ----------
        def _compute_loss(self, model, inputs):
            loss = super()._compute_loss(model, inputs)
            if self.algo != "rlce" or not self.model.training:
                return loss
            P = inputs["prompt_ids"].size(1)
            gi, gm = inputs["gold_ids"], inputs["gold_mask"]
            kw = _kw(inputs, P, gi.size(1), self._img_id())
            lp, _ = self._get_per_token_logps_and_entropies(
                model, torch.cat([inputs["prompt_ids"], gi], 1), torch.cat([inputs["prompt_mask"], gm], 1), gi.size(1), **kw)
            ce = -(lp * gm).sum() / gm.sum().clamp(min=1)
            self._metrics["train"]["rlce/ce"].append(float(ce.detach()))
            return loss + RC["lam"] * ce / self.current_gradient_accumulation_steps

        # ---------- SeqGAN ----------
        def _dac_trung(self, ids, am, keep, kw):
            lm = self.accelerator.unwrap_model(self.model).get_output_embeddings()
            buf = []
            h = lm.register_forward_pre_hook(lambda _m, a: buf.append(a[0][:, :-1][:, -keep:].detach().float()))
            try:
                with torch.no_grad():
                    self._get_per_token_logps_and_entropies(self.model, ids, am, keep,
                                                            self.args.per_device_train_batch_size, **kw)
            finally:
                h.remove()
            H = torch.cat(buf, 0)
            m = am[:, -keep:].unsqueeze(-1).float().to(H.device)
            tb = (H * m).sum(1) / m.sum(1).clamp(min=1.0)
            return torch.cat([H[:, 0], tb], -1)

        def _mang_D(self, F, dev):
            if self._D is None:
                with torch.random.fork_rng(devices=[]):      # không làm lệch dãy lấy mẫu so với các nhánh khác
                    self._D = torch.nn.Sequential(torch.nn.Linear(F, GAN["hid"]), torch.nn.ReLU(),
                                                  torch.nn.Linear(GAN["hid"], 1)).to(dev)
                torch.nn.init.zeros_(self._D[-1].weight)
                torch.nn.init.zeros_(self._D[-1].bias)
                self._opt_D = torch.optim.AdamW(self._D.parameters(), lr=GAN["lr"], weight_decay=0.0)
                if self._resume:
                    p = os.path.join(self._resume, "discriminator.pt")
                    assert os.path.exists(p), f"DỪNG: điểm lưu thiếu bộ phân biệt {p}"
                    S = torch.load(p, map_location=dev, weights_only=True)
                    self._D.load_state_dict(S["D"])
                    self._opt_D.load_state_dict(S["opt"])
                    print(f"[seqgan] nạp bộ phân biệt từ {p}", flush=True)
            return self._D

        def _save_checkpoint(self, model, trial):
            super()._save_checkpoint(model, trial)
            d = os.path.join(self.args.output_dir, f"checkpoint-{self.state.global_step}")
            if self._D is not None:
                torch.save(dict(D=self._D.state_dict(), opt=self._opt_D.state_dict()), os.path.join(d, "discriminator.pt"))
            if self._pool is not None:
                json.dump(list(self._pool), open(os.path.join(d, "quark_pool.json"), "w"))

    return MoiTrainer


# ============================ ES (vòng lặp riêng, không dùng Trainer) ============================
def es_train(a):
    import torch, transformers, peft
    from peft import LoraConfig, get_peft_model, set_peft_model_state_dict
    from safetensors.torch import load_file
    from PIL import Image

    pop, m, sig, lr = ES["pop"], ES["m"], ES["sigma"], ES["lr"]
    assert pop % 2 == 0, "--es-pop phải chẵn (cặp đối xứng)"
    print(f"[cấu hình] seed {a.seed} · thuật toán es · thưởng {a.reward} · pop {pop} · m {m} · σ {sig} · lr {lr}", flush=True)
    print(f"transformers {transformers.__version__} · peft {peft.__version__} · torch {torch.__version__}", flush=True)
    GL.dung_bo_cham(a.reward, a.bundle)
    thuong = GL.lam_thuong(a.reward)
    proc, model, dt = GS.nap(a)
    proc.tokenizer.padding_side = "left"
    s1 = json.load(open(os.path.join(a.adapter, "adapter_config.json"), encoding="utf-8"))
    lc = LoraConfig(r=s1["r"], lora_alpha=s1["lora_alpha"], lora_dropout=0.0, bias="none",
                    target_modules=s1["target_modules"], task_type="CAUSAL_LM")
    model = get_peft_model(model, lc)
    model.eval()
    PR = []
    for n, p_ in model.named_parameters():
        if p_.requires_grad:
            assert "visual" not in n, f"⛔ tháp thị giác: {n}"
            if p_.dtype != torch.float32:
                p_.data = p_.data.float()
            p_.requires_grad_(False)
            PR.append(p_)
    ntr = sum(p_.numel() for p_ in PR)
    ns1 = GS._n_s1(a.adapter)
    print(f"[LoRA mới] tham số dò {ntr:,} · S1 có {ns1:,}", flush=True)
    assert ntr == ns1, "⛔ LoRA mới không cùng cỡ S1"

    rows, bo = GS.dung_hang(a.bundle, n=a.n_prompt, dai_nhat=(50 if a.probe else 0), seed=a.seed)
    print(f"[câu nhắc] {len(rows)} · bỏ {bo}", flush=True)
    os.makedirs(a.out, exist_ok=True)
    keys = [r["key"] for r in rows]
    json.dump(keys, open(os.path.join(a.out, "prompt_keys.json"), "w"))
    if a.keys_ck500:
        assert keys == json.load(open(a.keys_ck500)), "⛔ tập câu nhắc khác ck500"
        print("[câu nhắc] trùng thứ tự với ck500 ✓", flush=True)
    tong = 20 if a.probe else a.max_steps

    dev = PR[0].device
    log, buoc0 = [], 0
    resume = a.resume
    if resume == "auto":
        ck = sorted((p for p in glob.glob(os.path.join(a.out, "checkpoint-*"))
                     if all(os.path.exists(os.path.join(p, f)) for f in
                            ("trainer_state.json", "adapter_model.safetensors", "es_state.json"))),
                    key=lambda p: int(p.rsplit("-", 1)[1]))
        co = glob.glob(os.path.join(a.out, "checkpoint-*"))
        assert ck or not co, f"DỪNG: có {len(co)} điểm lưu mà không cái nào đủ tệp"
        resume = ck[-1] if ck else None
    print("[tiếp từ]", resume, flush=True)
    if resume:
        nB = lambda: sum(p.float().norm().item() for n, p in model.named_parameters() if "lora_B" in n and ".default." in n)
        truoc = nB()
        sd = load_file(os.path.join(resume, "adapter_model.safetensors"))
        kq = set_peft_model_state_dict(model, sd, adapter_name="default")
        la = [k for k in getattr(kq, "unexpected_keys", []) if "lora" in k]
        sau = nB()
        print(f"[nạp default] {len(sd)} tensor · |lora_B| {truoc:.4f} → {sau:.4f} · khoá lạ {len(la)}", flush=True)
        assert sau > 0 and not la, "DỪNG: không nạp được adapter default từ điểm lưu"
        st = json.load(open(os.path.join(resume, "trainer_state.json")))
        log, buoc0 = st["log_history"], st["global_step"]

    def sinh(rs):
        texts, imgs = [], []
        for r in rs:
            msg = [dict(r["prompt"][0]), {"role": "user", "content": [{"type": "image"},
                                                                     {"type": "text", "text": r["prompt"][1]["content"]}]}]
            texts.append(proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True))
            imgs.append(Image.open(r["image"]).convert("RGB"))
        inp = proc(text=texts, images=imgs, padding=True, return_tensors="pt").to(dev)
        L = inp["input_ids"].shape[1]
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=96, do_sample=False, use_cache=True,
                               temperature=None, top_p=None, top_k=None)
        return [s.strip() for s in proc.batch_decode(g[:, L:], skip_special_tokens=True)]

    def thich_nghi(rs):
        s = sinh(rs)
        return sum(thuong(s, [r["gold"] for r in rs])) / len(rs), s

    def nhieu(seed):
        g = torch.Generator(device=dev).manual_seed(seed)
        return [torch.randn(p_.shape, generator=g, device=dev, dtype=p_.dtype) for p_ in PR]

    def luu(step):
        d = os.path.join(a.out, f"checkpoint-{step}")
        model.save_pretrained(d)
        json.dump(dict(global_step=step, log_history=log), open(os.path.join(d, "trainer_state.json"), "w"), indent=1)
        json.dump(dict(pop=pop, m=m, sigma=sig, lr=lr, seed=a.seed), open(os.path.join(d, "es_state.json"), "w"))

    t_all = time.time()
    for step in range(buoc0, tong):
        t0 = time.time()
        rs = [rows[(step * m + i) % len(rows)] for i in range(m)]
        goc = [p_.detach().clone() for p_ in PR]
        vals, seeds, cau = [], [], set()
        for j in range(pop // 2):
            sd = a.seed * 1_000_003 + step * 1_009 + j
            seeds.append(sd)
            E = nhieu(sd)
            for dau in (1.0, -1.0):
                with torch.no_grad():
                    for p_, g0, e in zip(PR, goc, E):
                        p_.copy_(g0 + dau * sig * e)
                f, s = thich_nghi(rs)
                vals.append(f)
                cau.add(tuple(s))
            del E
        u = chuan_z(vals)
        with torch.no_grad():
            for p_, g0 in zip(PR, goc):
                p_.copy_(g0)
            buoc_tb = 0.0
            for j, sd in enumerate(seeds):
                w = lr * (u[2 * j] - u[2 * j + 1]) / pop
                if w == 0.0:
                    continue
                for p_, e in zip(PR, nhieu(sd)):
                    p_.add_(e, alpha=w)
            buoc_tb = math.sqrt(sum(float(((p_ - g0) ** 2).sum()) for p_, g0 in zip(PR, goc)))
            chuan = math.sqrt(sum(float((g0 ** 2).sum()) for g0 in goc))
        del goc
        dtb = time.time() - t0
        rec = {"loss": 0.0, "reward": sum(vals) / len(vals), "es/f_max": max(vals), "es/f_min": min(vals),
               "es/so_cau_khac": len(cau), "es/buoc_l2": buoc_tb, "es/buoc_tuong_doi": buoc_tb / max(chuan, 1e-12),
               "luoi/adv_abs_mean": sum(map(abs, u)) / len(u),
               "kl": 0.0, "step_time": dtb, "step": step + 1}
        log.append(rec)
        print(str({k: (round(v, 6) if isinstance(v, float) else v) for k, v in rec.items()}), flush=True)
        if not all(math.isfinite(x) for x in vals + [buoc_tb]):
            raise SystemExit("⛔ ES ra số không hữu hạn")
        if (step + 1) % ES["save"] == 0 and not a.probe:
            luu(step + 1)
    el = time.time() - t_all
    n = max(tong - buoc0, 1)
    print(f"[xong] {n} bước · {el/60:.1f} phút · {el/n:.1f} s/bước · "
          f"đỉnh VRAM {(torch.cuda.max_memory_allocated()/2**30 if torch.cuda.is_available() else 0):.2f} GiB · "
          f"thưởng {GL.STAT['t']/max(GL.STAT['n'], 1):.1f} s/lần", flush=True)
    if tong > buoc0 and not os.path.exists(os.path.join(a.out, f"checkpoint-{tong}")) and not a.probe:
        luu(tong)
    model.save_pretrained(os.path.join(a.out, "final"))
    json.dump(log, open(os.path.join(a.out, "log_history.json"), "w"), indent=1)


def train(a):
    if a.algo == "es":
        return es_train(a)
    return _train(a)


GL.ALGOS = GL.ALGOS + MOI
GL.REWARDS = GL.REWARDS + ("bcmr",)
GL.loi_the = loi_the
GL.lop_trainer = lop_trainer
GL.train = train
GL.dung_bo_cham = dung_bo_cham
GL.diem = diem
GL.selftest_algo = selftest_moi


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--ce-lam", type=float, default=RC["lam"])
    ap.add_argument("--mixer-rho0", type=float, default=MX["rho0"])
    ap.add_argument("--mixer-frac", type=float, default=MX["frac"])
    ap.add_argument("--gan-mix", type=float, default=GAN["mix"])
    ap.add_argument("--gan-warm", type=int, default=GAN["warm"])
    ap.add_argument("--gan-lr", type=float, default=GAN["lr"])
    ap.add_argument("--quark-k", type=int, default=QK["k"])
    ap.add_argument("--quark-pool", type=int, default=QK["pool"])
    ap.add_argument("--es-pop", type=int, default=ES["pop"])
    ap.add_argument("--es-m", type=int, default=ES["m"])
    ap.add_argument("--es-sigma", type=float, default=ES["sigma"])
    ap.add_argument("--es-lr", type=float, default=ES["lr"])
    ap.add_argument("--es-save", type=int, default=ES["save"])
    x, rest = ap.parse_known_args(argv)
    RC["lam"] = x.ce_lam
    MX.update(rho0=x.mixer_rho0, frac=x.mixer_frac)
    GAN.update(mix=x.gan_mix, warm=x.gan_warm, lr=x.gan_lr)
    QK.update(k=x.quark_k, pool=x.quark_pool)
    ES.update(pop=x.es_pop, m=x.es_m, sigma=x.es_sigma, lr=x.es_lr, save=x.es_save)
    print(f"[đợt 4] rlce {RC} · mixer {MX} · seqgan {GAN} · quark {QK} · es {ES}", flush=True)
    if "--reward" in rest and rest[rest.index("--reward") + 1] == "bcmr":
        al = rest[rest.index("--algo") + 1] if "--algo" in rest else "grpo"
        assert al == "grpo", "⛔ thưởng bcmr chỉ đi với --algo grpo (lưới đổi một yếu tố)"
    CD.main(rest)


if __name__ == "__main__":
    main()
