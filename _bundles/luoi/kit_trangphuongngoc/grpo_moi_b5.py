"""Lưới RL, lượt 1 và 2 của bảng 12.3 (slides/ACTION_4_THUAT_TOAN_RL_2025_SO_VOI_GRPO_20_11_2026.md, mục 12):
GRPO batch lớn và REINFORCE++-Baseline, cùng ĐÚNG một lô 128 câu sinh on-policy.

Không sửa grpo_luoi.py · grpo_codien.py · grpo_moi_b1/b2/b4.py · grpo_ppo.py · grpo_spice.py: tệp này import grpo_codien rồi
gọi main() của nó, nên điểm xuất phát (S1 hoà + LoRA mới), 1.000 câu nhắc của ck500, G = 8, lr 1e-5, β 0,04 (KL của TRL),
loss_type "dapo", phần thưởng SPICE và dòng log `[nạp default]` giữ nguyên. Không import grpo_moi_b1 (tránh vá chồng).

Thuật toán mới (--algo):
  grpo_lon  GRPO batch lớn: P = 16 câu nhắc × G = 8 = 128 câu sinh dưới cùng một chính sách đóng băng, MỘT bước tối ưu
            sau cả lô; A = (r − mean_nhóm) / (std_nhóm + 1e-4), y hệt `grpo` (đối chứng cho rpp).
  rpp       REINFORCE++-Baseline (Hu và cộng sự 2025, arXiv 2501.03262): cùng đúng 128 câu như grpo_lon;
            A' = r − mean_nhóm, rồi A = A' / (std(A' trên TOÀN BỘ 128 giá trị) + 1e-4). Sau bước trừ mốc trung bình
            cả lô bằng 0 nên không trừ thêm. KHÔNG cửa sổ trượt (mục 5.2 cũ đã bị bác ở 12.2, blocker 2).
            std là std CÓ hiệu chỉnh (chia n − 1, torch.std mặc định, cũng là `scale_rewards="batch"` của TRL):
            ví dụ mục 2.6 (nhóm 0·1·0·1 và 0,1·0,3·0,1·0,3) ra ±1,30 và ±0,26 chỉ với std chia n − 1
            (chia n thì ±1,39 và ±0,28). Ví dụ mục 5.2 (0,2·0,4·0,6·0,8 và 0,5×4) ra −1,77 · −0,59 · +0,59 · +1,77.
            Khai so với bài gốc: KL là ước lượng của TRL trên mất mát (β 0,04), không phải KL k2 cộng vào thưởng.

Cấu hình module TỰ ÉP cho cả hai (không phụ thuộc cờ notebook; in một dòng `[b5] …`):
  gradient_accumulation_steps = P·G / bs = 32 (bs 4)  ⇒ TRL tự đặt steps_per_generation = 32, generation_batch_size = 128
  num_iterations = 1, max_steps = ⌊n_prompt / P⌋ = 62, warmup_steps = 1 (thay 10 vì chỉ 62 bước), save_steps = 2
  (mỗi bước ~20 phút trên T4 [suy], trần phiên 11 h). Ghi đè bằng CD.OVERRIDE (vá GRPOConfig.__init__) VÀ thay cờ
  --accum / --max-steps trong argv trước khi gọi CD.main, nên hai đường cùng ra một số.

Đã kiểm trong mã TRL 0.29.1 (trl/trainer/…):
  · grpo_config.py:823–825 — chỉ đặt gradient_accumulation_steps thì steps_per_generation = accum,
    generation_batch_size = bs·num_processes·steps_per_generation = 4·1·32 = 128 (Kaggle chạy 1 tiến trình).
  · grpo_trainer.py:862 — DataLoader lấy lô = bs·steps_per_generation = 128 dòng; :1111–1119 _prepare_inputs gọi
    _generate_and_score_completions MỘT lần cho cả 128 dòng mỗi steps_per_generation·num_iterations = 32 micro-lô,
    rồi cắt thành 32 micro-lô 4 câu ⇒ đúng một bước tối ưu cho cả lô sinh.
  · grpo_trainer.py:1881 → :1127–1171 _calculate_rewards gọi mỗi hàm thưởng đồng bộ MỘT lần với cả 128 câu
    (`reward_func(prompts=…, completions=…)`) ⇒ GL.LAST["r"] có đủ 128 giá trị khi lớp LuoiTrainer tính lại lợi thế.
  · grpo_trainer.py:1788–1790 — accum % (steps_per_generation·num_iterations) = 0 ⇒ không tính old_per_token_logps,
    tỉ số quan trọng = 1 (đúng on-policy, cùng chế độ μ = 1 của lưới).
  · grpo_trainer.py:2237–2239 — loss_type "dapo": chia tổng mất mát cho num_items_in_batch = tổng token câu sinh của
    CẢ lô sinh 128 câu (:1616), cộng dồn qua 32 micro-lô ⇒ một trung bình theo token trên cả lô, như lưới cũ trên 16 câu.
  · utils.py:794–812 RepeatSampler (grpo_trainer.py:907–914, batch_size = generation_batch_size / G = 16 câu nhắc):
    xáo 1.000 chỉ số rồi cắt khúc 16, BỎ khúc lẻ cuối (1.000 = 62·16 + 8) ⇒ một epoch = 62 khúc = 62 bước tối ưu,
    992/1.000 câu nhắc, mỗi câu nhắc đúng một lần (8 câu nhắc bị bỏ do hoán vị theo seed, khác nhau giữa các seed).
    max_steps = 62 nên không bước vào epoch hai. Phương án lùi P = 8: 125 khúc · 125 bước · đủ 1.000 câu nhắc.

⚠️ BỘ NHỚ: lô sinh 128 câu giữ pixel_values của 128 ảnh, prompt đệm theo câu dài nhất của 128, cùng mọi tensor của lô
(completion_ids, ref_per_token_logps…) trên GPU suốt 32 micro-lô. Probe PHẢI đo đỉnh VRAM (dòng `[xong] … đỉnh VRAM`
của grpo_luoi.train) trên lô thật trước lượt train. Tràn thì lùi: --b5-prompts 8 ⇒ 8 × 8 = 64 câu, accum 16,
max_steps 125 (mọi số tự suy ra). Sinh vẫn theo khúc --gen-chunk 8 như lưới.

Log mỗi bước (trainer_state): luoi/rpp_std (std 128 giá trị đã trừ mốc; với rpp là std đã dùng để chia, với grpo_lon
chỉ để đối chiếu) · luoi/adv_abs_mean · luoi/frac_adv_zero · luoi/n_cau_lo (số câu trong lô sinh, phải = P·G).

  python grpo_moi_b5.py --selftest-algo                       # CPU, không mạng: công thức lợi thế
  python grpo_moi_b5.py --selftest-cpu [--out D]              # CPU, cần mạng tải trl-internal-testing/tiny-Qwen2...
  python grpo_moi_b5.py --train --no-q4 --bs 4 --accum 4 --gen-chunk 8 --algo rpp --reward spice --seed 101 \
      --bundle B --merged M --out O --resume auto --keys-ck500 K [--b5-prompts 16] [--b5-max-steps N]
"""
import os, sys, math, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_codien as CD                                  # noqa: E402
GL = CD.GL

MOI = ("grpo_lon", "rpp")
_cu = GL.loi_the
_lop = GL.lop_trainer


# ============================ công thức ============================
def tru_moc(r, G):
    """r: (N,) theo nhóm liền nhau. Trả r − mean_nhóm, dạng (N,)."""
    import torch
    r = torch.as_tensor(r, dtype=torch.float32).view(-1, G)
    return (r - r.mean(1, keepdim=True)).flatten()


def std_lo(r, G):
    """std CÓ hiệu chỉnh (n − 1) của toàn bộ giá trị đã trừ mốc nhóm trong lô."""
    return float(tru_moc(r, G).std())


def a_rpp(r, G):
    a = tru_moc(r, G)
    return a / (a.std() + 1e-4)


def loi_the(algo, r, G, b=None, r_greedy=None):
    if algo == "grpo_lon":
        return _cu("grpo", r, G)
    if algo == "rpp":
        return a_rpp(r, G), b
    return _cu(algo, r, G, b=b, r_greedy=r_greedy)


def so_buoc(n_prompt, P):
    """Số bước của một epoch theo RepeatSampler TRL 0.29.1: bỏ khúc lẻ cuối."""
    return n_prompt // P


# ============================ lớp trainer ============================
def lop_trainer():
    import torch
    B = _lop()

    class B5Trainer(B):
        def __init__(self, *args, **kw):
            super().__init__(*args, **kw)
            self._b5_goi = []                             # số câu mỗi lần gọi hàm thưởng trong một lô sinh
            for i, f in enumerate(self.reward_funcs):
                if isinstance(f, torch.nn.Module):
                    continue

                def boc(*aa, _f=f, **kk):
                    self._b5_goi.append(len(kk.get("completions", aa[1] if len(aa) > 1 else [])))
                    return _f(*aa, **kk)
                boc.__name__ = getattr(f, "__name__", "thuong")
                self.reward_funcs[i] = boc

        def _generate_and_score_completions(self, inputs):
            self._b5_goi = []
            out = super()._generate_and_score_completions(inputs)
            if self.algo not in MOI or not self.model.training:
                return out
            n = len(inputs)
            assert n == self.args.generation_batch_size, \
                f"⛔ lô sinh {n} câu ≠ generation_batch_size {self.args.generation_batch_size}"
            assert self._b5_goi and all(k == n for k in self._b5_goi), \
                f"⛔ hàm thưởng không nhận cả lô một lần: {self._b5_goi} (lô {n})"
            mt = self._metrics["train"]
            mt["luoi/rpp_std"].append(std_lo(GL.LAST["r"], self.num_generations))
            mt["luoi/n_cau_lo"].append(float(n))
            return out

    return B5Trainer


# ============================ tự kiểm ============================
def selftest_b5(_):
    import torch
    G = 4
    r = [0.2, 0.4, 0.6, 0.8, 0.5, 0.5, 0.5, 0.5]
    A, _ = loi_the("rpp", r, G)
    d = torch.tensor([-0.3, -0.1, 0.1, 0.3])
    s = math.sqrt((0.09 * 2 + 0.01 * 2) / 7)              # std có hiệu chỉnh trên 8 giá trị đã trừ mốc
    assert torch.allclose(A[:4], d / (s + 1e-4), atol=1e-5), A
    assert A[4:].abs().max() < 1e-7, A
    assert torch.allclose(A[:4], torch.tensor([-1.77, -0.59, 0.59, 1.77]), atol=6e-3), A   # mục 5.2
    print(f"  rpp mục 5.2: {[round(x, 3) for x in A.tolist()]} (std lô {s:.4f})")
    r26 = [0, 1, 0, 1, 0.1, 0.3, 0.1, 0.3]                 # mục 2.6
    A, _ = loi_the("rpp", r26, G)
    assert torch.allclose(A, torch.tensor([-1.30, 1.30, -1.30, 1.30, -0.26, 0.26, -0.26, 0.26]), atol=6e-3), A
    sn = math.sqrt((4 * 0.25 + 4 * 0.01) / 8)              # chia n: ±1,39 / ±0,28 — KHÔNG khớp tài liệu
    assert abs(0.5 / sn - 1.30) > 0.05
    assert abs(A[1] / A[5] - 5.0) < 1e-4                   # giữ tỉ lệ thật giữa hai nhóm (0,5 / 0,1)
    print(f"  rpp mục 2.6: {[round(x, 3) for x in A.tolist()]} (std chia n − 1; chia n sẽ ra ±{0.5/sn:.2f})")
    Ag, _ = loi_the("grpo", r26, G)
    assert torch.allclose(Ag, torch.tensor([-0.866, 0.866] * 2 + [-0.866, 0.866] * 2), atol=2e-3), Ag
    for rr in (r, r26):
        assert torch.allclose(loi_the("grpo_lon", rr, G)[0], _cu("grpo", rr, G)[0])
        assert torch.allclose(loi_the("grpo", rr, G)[0], _cu("grpo", rr, G)[0])
        assert torch.allclose(loi_the("drgrpo", rr, G)[0], _cu("drgrpo", rr, G)[0])
    rb = torch.rand(128).tolist()                          # lô thật: 16 nhóm × 8
    A = a_rpp(rb, 8)
    assert abs(float(A.mean())) < 1e-5 and abs(float(A.std()) - 1) < 1e-3, (A.mean(), A.std())
    assert so_buoc(1000, 16) == 62 and so_buoc(1000, 8) == 125
    print("✅ selftest công thức b5 ĐẠT: rpp (std lô, chia n − 1) · grpo_lon = grpo · grpo/drgrpo trùng hàm cũ")


def selftest_cpu(a):
    """Lô lớn thu nhỏ: 4 câu nhắc × G 4 = 16 câu, bs 4 ⇒ accum 4, một bước tối ưu mỗi lô sinh; cấu hình ép qua
    CD.OVERRIDE + vá GRPOConfig.__init__ như lúc train thật."""
    import re, json, time, shutil, torch, transformers, trl, peft
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    from trl import GRPOConfig
    from datasets import Dataset
    print(f"trl {trl.__version__} · transformers {transformers.__version__} · peft {peft.__version__} · torch {torch.__version__}",
          flush=True)
    Mten = "trl-internal-testing/tiny-Qwen2ForCausalLM-2.5"
    golds = ["Click on the search bar", "Open the Clock app", "Swipe up to see more", "Type hello in the box"]
    NP, P, G, bs = 14, 4, 4, 4                             # 14 câu nhắc: 3 khúc 4 + khúc lẻ 2 bị bỏ
    rows = [dict(key=f"k{i}", prompt=[{"role": "user", "content": f"Describe step {i}"}], gold=golds[i % 4],
                 action_type="") for i in range(NP)]
    W = re.compile(r"[a-z0-9]+")
    goi = []

    def r_gia(completions, gold, key, **kw):
        goi.append(list(key))
        out = []
        for c, g in zip(completions, gold):
            a_, b_ = set(W.findall(GL.GS._text(c).lower())), set(W.findall(g.lower()))
            k = len(a_ & b_)
            out.append(0.0 if not k else 2 * k / (len(a_) + len(b_)))
        out = [x + 0.01 * (len(GL.GS._text(c)) % 5) for x, c in zip(out, completions)]
        GL.LAST["r"] = list(out)
        return out

    CD._va_cau_hinh()
    kq = {}
    for algo in MOI:
        t0 = time.time()
        goi.clear()
        out = os.path.join(a.out or "/tmp/b5_cpu", algo)
        shutil.rmtree(out, ignore_errors=True)
        accum, steps = P * G // bs, so_buoc(NP, P)
        CD.OVERRIDE.clear()
        CD.OVERRIDE.update(gradient_accumulation_steps=accum, num_iterations=1, max_steps=steps, warmup_steps=1,
                           save_steps=2)
        transformers.set_seed(101)
        tk = AutoTokenizer.from_pretrained(Mten)
        tk.padding_side = "left"
        m = AutoModelForCausalLM.from_pretrained(Mten, dtype=torch.float32)
        m = get_peft_model(m, LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0, target_modules=["q_proj", "v_proj"],
                                         task_type="CAUSAL_LM"))
        # cấu hình "như notebook" (accum 4 lưới, 500 bước, warmup 10, save 25): OVERRIDE phải đè hết
        args = GRPOConfig(output_dir=out, seed=101, num_generations=G, per_device_train_batch_size=bs,
                          gradient_accumulation_steps=1, max_completion_length=12, temperature=1.0, top_p=1.0, top_k=0,
                          beta=0.04, learning_rate=1e-2, lr_scheduler_type="constant_with_warmup", warmup_steps=10,
                          max_steps=500, num_train_epochs=1, logging_steps=1, save_steps=25, report_to="none",
                          remove_unused_columns=False, use_cpu=True, bf16=False, fp16=False, disable_tqdm=True,
                          mask_truncated_completions=False, scale_rewards="group", loss_type="dapo", num_iterations=1)
        T = lop_trainer()
        tr = T(model=m, reward_funcs=[r_gia], args=args, train_dataset=Dataset.from_list(rows), processing_class=tk)
        tr.algo, tr.thuong = algo, r_gia
        nB = lambda: sum(p.norm().item() for n_, p in tr.model.named_parameters() if "lora_B" in n_)
        truoc = nB()
        tr.train()
        sau = nB()
        ca = {k: getattr(tr.args, k) for k in ("generation_batch_size", "steps_per_generation", "gradient_accumulation_steps",
                                                  "num_iterations", "max_steps", "warmup_steps", "save_steps", "beta",
                                                  "loss_type")}
        H = tr.state.log_history
        loss = [h["loss"] for h in H if "loss" in h]
        adv = [h["luoi/adv_abs_mean"] for h in H if "luoi/adv_abs_mean" in h]
        sd = [h["luoi/rpp_std"] for h in H if "luoi/rpp_std" in h]
        nl = [h["luoi/n_cau_lo"] for h in H if "luoi/n_cau_lo" in h]
        khoa = [k for g_ in goi for k in g_[::G]]
        kiem = {
            "cấu hình": ca["generation_batch_size"] == P * G and ca["steps_per_generation"] == accum
            and ca["gradient_accumulation_steps"] == accum and ca["max_steps"] == steps and ca["warmup_steps"] == 1
            and ca["save_steps"] == 2 and ca["num_iterations"] == 1,
            "số bước": tr.state.global_step == steps and len(loss) == steps,
            "thưởng nhận cả lô": len(goi) == steps and all(len(g_) == P * G for g_ in goi),
            "nhóm cùng câu nhắc": all(len(set(g_[i:i + G])) == 1 for g_ in goi for i in range(0, P * G, G)),
            "1 epoch không lặp": len(khoa) == len(set(khoa)) == steps * P,
            "hữu hạn": all(math.isfinite(x) for x in loss + adv + sd) and len(adv) == steps and len(sd) == steps,
            "n_cau_lo": nl == [float(P * G)] * steps,
            "lora_B đổi": sau > truoc,
            "điểm lưu": sorted(int(p.rsplit("-", 1)[1]) for p in os.listdir(out) if p.startswith("checkpoint-"))
            == sorted(set(range(2, steps + 1, 2)) | {steps}),      # transformers 5 lưu thêm bước cuối
        }
        ok = all(kiem.values())
        kq[algo] = dict(dat=ok, kiem=kiem, cau_hinh=ca, loss=[round(x, 5) for x in loss], adv=[round(x, 4) for x in adv],
                        rpp_std=[round(x, 4) for x in sd], lora_B=[round(truoc, 4), round(sau, 4)],
                        so_cau_nhac_dung=len(set(khoa)), giay=round(time.time() - t0, 1))
        print(f"[{algo}] {'ĐẠT' if ok else '⛔ KHÔNG ĐẠT'} · {json.dumps(kq[algo], ensure_ascii=False)}", flush=True)
    CD.OVERRIDE.clear()
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        json.dump(kq, open(os.path.join(a.out, "selftest_cpu_b5.json"), "w"), ensure_ascii=False, indent=1)
    hong = [k for k, v in kq.items() if not v["dat"]]
    assert not hong, f"⛔ không đạt: {hong}"
    print(f"✅ selftest CPU b5 ĐẠT: {' · '.join(kq)}", flush=True)


# ============================ chạy ============================
GL.ALGOS = GL.ALGOS + MOI
GL.loi_the = loi_the
GL.lop_trainer = lop_trainer


def _lay(rest, co, mac_dinh, kieu=int):
    return kieu(rest[rest.index(co) + 1]) if co in rest else mac_dinh


def _dat(rest, co, gia_tri):
    if co in rest:
        rest[rest.index(co) + 1] = str(gia_tri)
    else:
        rest += [co, str(gia_tri)]


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--algo", default="grpo")
    ap.add_argument("--b5-prompts", type=int, default=16, help="số câu nhắc mỗi lô sinh (lùi 8 nếu tràn VRAM)")
    ap.add_argument("--b5-max-steps", type=int, default=0, help="0 = trọn 1 epoch (⌊n_prompt/P⌋); >0 chỉ để probe")
    ap.add_argument("--selftest-cpu", action="store_true")
    a, rest = ap.parse_known_args()
    if "--selftest-algo" in rest:
        return selftest_b5(a)
    if a.selftest_cpu:
        a.out = _lay(rest, "--out", "", str)
        return selftest_cpu(a)
    if a.algo in MOI:
        P = a.b5_prompts
        G, bs = _lay(rest, "--G", 8), _lay(rest, "--bs", 4)
        n_prompt = _lay(rest, "--n-prompt", GL.GS.N_PROMPT)
        assert P >= 1 and (P * G) % bs == 0, f"⛔ P·G = {P * G} không chia hết bs {bs}"
        accum = P * G // bs
        probe = "--probe" in rest
        steps = a.b5_max_steps or (2 if probe else so_buoc(n_prompt, P))
        cu = (_lay(rest, "--accum", 4), _lay(rest, "--max-steps", 500))
        ov = dict(gradient_accumulation_steps=accum, num_iterations=1, max_steps=steps, warmup_steps=1,
                  save_steps=(10 ** 9 if probe else 2))
        CD.OVERRIDE.update(ov)
        _dat(rest, "--accum", accum)
        _dat(rest, "--max-steps", steps)
        for k in ("--mu", "--loss-type", "--scale-rewards", "--is-level", "--eps-high"):
            assert k not in rest, f"⛔ {a.algo} không nhận {k}: cấu hình phải trùng lượt đối chứng"
        print(f"[b5] --algo {a.algo} · P {P} câu nhắc × G {G} = {P * G} câu sinh/lô, bs {bs} ⇒ ép "
              f"gradient_accumulation_steps {accum} (cờ notebook {cu[0]}; ⇒ steps_per_generation {accum}, "
              f"generation_batch_size {P * G}: một bước tối ưu mỗi lô sinh) · num_iterations 1 (on-policy) · "
              f"max_steps {steps} (cờ notebook {cu[1]}; {'probe' if probe or a.b5_max_steps else f'⌊{n_prompt}/{P}⌋ = 1 epoch, {steps * P}/{n_prompt} câu nhắc vì RepeatSampler bỏ khúc lẻ'}) · "
              f"warmup_steps 1 (thay 10: chỉ {steps} bước) · save_steps {ov['save_steps']} (~20 phút/bước trên T4, trần 11 h) · "
              f"lợi thế {'(r − mean_nhóm)/std_nhóm như grpo' if a.algo == 'grpo_lon' else '(r − mean_nhóm)/std cả lô (n − 1)'} · "
              f"β, lr, thưởng giữ cờ notebook", flush=True)
    CD.main(rest + ["--algo", a.algo])


if __name__ == "__main__":
    main()
