"""Lưới RL, nhóm câu/ưu tiên (report/326 ưu tiên một, report/329 hàng 2–4): thêm thuật toán MỚI trên cùng vòng lặp ck500.

Không sửa grpo_luoi.py · grpo_codien.py · grpo_ppo.py: tệp này import grpo_codien rồi gọi main() của nó, nên điểm xuất phát
(S1 hoà + LoRA mới), 1.000 câu nhắc, G = 8, lr, số bước, phần thưởng, điểm lưu và dòng log `[nạp default]` giữ nguyên.

Ý chính: với num_iterations = 1 tỉ số quan trọng luôn bằng 1, nên gradient của hàm mất mát TRL (loss_type "dapo") là
    ∇L = −(1/N_tok) · Σ_i A_i · ∇ log π(y_i)        (N_tok = tổng token câu sinh trong lô sinh, log π(y) = tổng log-prob token)
Mọi thuật toán dưới đây chỉ cần tính A_i sao cho ∇L trùng ĐÚNG gradient của mục tiêu gốc (đã kiểm bằng autograd ở
--selftest-algo). Lợi thế tính một lần lúc sinh, với chính sách lúc sinh = chính sách lúc cập nhật (μ = 1) nên là chính xác.

Thuật toán mới (--algo):
  dpo_on   DPO trực tuyến (Guo và cộng sự 2024, OAIF): mỗi nhóm G câu lấy câu thưởng cao nhất làm chosen, thấp nhất làm
           rejected, mất mát DPO −log σ(β_d·[(log π_c − log π_ref,c) − (log π_r − log π_ref,r)]), tham chiếu = S1
           (tắt LoRA). β KL của GRPO mặc định 0 (KL đã nằm trong DPO). Nhóm thưởng bằng nhau: không có cặp, A = 0.
  dpo_off  DPO ngoại tuyến từ S1: như dpo_on nhưng câu được SINH TỪ S1 ĐÓNG BĂNG (tắt LoRA lúc sinh), không từ chính sách
           đang học. Tương đương dựng sẵn tập cặp từ mẫu của S1 trên 1.000 câu nhắc rồi DPO một lượt (mỗi câu nhắc một lần).
  rft_off  RFT một vòng (DeepSeekMath §5.2.1): sinh từ S1 đóng băng, SFT câu thưởng cao nhất nhóm (A = 1, còn lại 0).
           Online RFT là `rft` của grpo_codien (sinh từ chính sách). β = 0,04 giữ như ck500 để rft_off − rft chỉ khác nguồn mẫu.
  mrt      Minimum Risk Training (Shen và cộng sự, ACL 2016): rủi ro Σ_y Q(y)·(−r(y)), Q = softmax(α·log π(y)) trên G mẫu
           của nhóm, α = 0,005 như bài gốc. A_y = α·Q_y·(r_y − E_Q r)·N_tok/P. Không khử mẫu trùng (bài gốc có khử).
  spg      Softmax policy gradient (Ding & Soricut, NeurIPS 2017): gradient Σ_y q(y)∇log π(y), q ∝ π·exp(r/τ); mẫu từ π nên
           trọng số tự chuẩn hoá w = softmax(r/τ) trong nhóm, trừ mốc 1/G. A_y = (w_y − 1/G)·N_tok/P, τ = 0,2.
           Khác `raml` của grpo_codien (A = G·softmax(r/τ)) đúng ở mốc trừ và thang; kỳ vọng gradient như nhau.
Bí danh chỉ đổi cấu hình TRL (không mã mới, viết sẵn để make_nb gọi bằng một --algo):
  drgrpo_full  Dr. GRPO đủ (Liu và cộng sự 2025): bỏ chia std (drgrpo) VÀ bỏ chuẩn hoá theo độ dài (loss_type dr_grpo)
  grpo_seq     GRPO gộp theo câu như bài gốc DeepSeekMath: loss_type "grpo" (TB theo token trong câu rồi TB theo câu)
  gspo         GSPO (Zheng và cộng sự 2025): tỉ số theo câu, clip [1−3e−4; 1+4e−4], μ = 2 (μ = 1 thì GSPO trùng hệt ck500).
               Muốn cùng 1.000 câu nhắc thì --max-steps 1000.
P = số nhóm (câu nhắc) trong lô sinh. Câu bị cắt ở 96 token (mask = 0) không được chọn làm chosen/rejected.

Cờ MỚI so với grpo_luoi/grpo_codien: --dpo-beta (0,1) · --mrt-alpha (0,005) · --spg-tau (0,2) · --eps-low ·
--selftest-cpu (chạy 3 bước mỗi thuật toán trên mô hình tí hon, CPU). Mọi cờ khác giống grpo_codien.main.

  python grpo_moi_b1.py --selftest-algo                       # CPU, không mạng: công thức lợi thế so với autograd
  python grpo_moi_b1.py --selftest-cpu [--algos dpo_on,mrt]   # CPU, cần mạng tải trl-internal-testing/tiny-Qwen2...
  python grpo_moi_b1.py --train --algo dpo_on --reward spice --bundle B --merged M --out O --resume auto
"""
import os, sys, math, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_codien as CD                                  # noqa: E402
GL = CD.GL

MOI = ("dpo_on", "dpo_off", "rft_off", "mrt", "spg")
ALIAS = {
    "drgrpo_full": ("drgrpo", dict(loss_type="dr_grpo")),
    "grpo_seq": ("grpo", dict(loss_type="grpo")),
    "gspo": ("grpo", dict(importance_sampling_level="sequence", epsilon=3e-4, epsilon_high=4e-4, num_iterations=2)),
}
OFF = ("dpo_off", "rft_off")                              # sinh từ S1 đóng băng
CAN_LOGP = ("dpo_on", "dpo_off", "mrt")                   # cần log π(y) của chính sách lúc sinh
CAN_REF = ("dpo_on", "dpo_off")                           # cần log π_ref(y)
HS = dict(dpo_beta=0.1, mrt_alpha=0.005, spg_tau=0.2)
_cu = GL.loi_the
_lop = GL.lop_trainer


# ============================ công thức (tensor thuần, kiểm bằng autograd) ============================
def a_dpo(r, s, s_ref, G, ntok, beta, ok=None):
    """r, s, s_ref: (N,) theo nhóm liền nhau. ok: (N,) bool, False = câu bị cắt, không chọn. Trả (A, số cặp, margin TB)."""
    import torch
    r = r.view(-1, G).float()
    P = r.shape[0]
    rr = r.clone()
    okv = torch.ones_like(rr, dtype=torch.bool) if ok is None else ok.view(-1, G)
    hi = rr.masked_fill(~okv, -math.inf).argmax(1)
    lo = rr.masked_fill(~okv, math.inf).argmin(1)
    A = torch.zeros_like(rr)
    lr_ = (s - s_ref).view(-1, G).float()
    n, mg = 0, []
    for p in range(P):
        c, j = int(hi[p]), int(lo[p])
        if not (okv[p, c] and okv[p, j]) or rr[p, c] - rr[p, j] < 1e-9:
            continue
        h = lr_[p, c] - lr_[p, j]
        w = beta * torch.sigmoid(-beta * h)
        A[p, c] += w
        A[p, j] -= w
        n += 1
        mg.append(float(h))
    A = A * (ntok / P)                                    # mất mát = TB theo câu nhắc (nhóm không cặp góp 0)
    return A.flatten(), n, (sum(mg) / len(mg) if mg else 0.0)


def a_mrt(r, s, G, ntok, alpha):
    import torch
    r = r.view(-1, G).float()
    Q = torch.softmax(alpha * s.view(-1, G).float(), dim=1)
    A = alpha * Q * (r - (Q * r).sum(1, keepdim=True))
    return (A * (ntok / r.shape[0])).flatten()


def a_spg(r, G, ntok, tau):
    import torch
    r = r.view(-1, G).float()
    A = torch.softmax(r / tau, dim=1) - 1.0 / G
    return (A * (ntok / r.shape[0])).flatten()


def loi_the(algo, r, G, b=None, r_greedy=None):
    """Vòng lặp cha gọi hàm này trước; thuật toán mới nhận lợi thế tạm drgrpo, lợi thế thật đặt ở lớp con."""
    if algo in MOI:
        return _cu("drgrpo", r, G)
    return _cu(algo, r, G, b=b, r_greedy=r_greedy)


# ============================ lớp trainer ============================
def lop_trainer():
    import torch
    from trl.trainer.utils import use_adapter
    B = _lop()

    class MoiTrainer(B):
        n_sinh_s1 = 0

        def _ref_ctx(self):
            m = self.accelerator.unwrap_model(self.model)
            return use_adapter(m, adapter_name="ref" if "ref" in m.peft_config else None)

        def _generate(self, prompts):
            if self.algo in OFF and self.model.training:
                self.n_sinh_s1 += 1
                with self._ref_ctx():
                    return super()._generate(prompts)
            return super()._generate(prompts)

        def _logp_cau(self, out, ref=False):
            ids = torch.cat([out["prompt_ids"], out["completion_ids"]], 1)
            am = torch.cat([out["prompt_mask"], out["completion_mask"]], 1)
            kw = {k: out[k] for k in ("pixel_values", "image_grid_thw", "num_images", "pixel_attention_mask",
                                      "image_sizes", "token_type_ids", "mm_token_type_ids") if k in out}
            with torch.no_grad(), self.compute_loss_context_manager():
                if ref:
                    with self._ref_ctx():
                        lp, _ = self._get_per_token_logps_and_entropies(
                            self.model, ids, am, out["completion_ids"].size(1), self.args.per_device_train_batch_size, **kw)
                else:
                    lp, _ = self._get_per_token_logps_and_entropies(
                        self.model, ids, am, out["completion_ids"].size(1), self.args.per_device_train_batch_size, **kw)
            m = out["completion_mask"].to(lp.dtype)
            return (lp * m).sum(1).float().cpu()

        def _generate_and_score_completions(self, inputs):
            out = super()._generate_and_score_completions(inputs)
            if self.algo not in MOI or not self.model.training:
                return out
            G = self.num_generations
            r = torch.tensor(GL.LAST["r"], dtype=torch.float32)
            ntok = float(out["num_items_in_batch"])
            ok = (out["completion_mask"].sum(1) > 0).cpu()
            mt = self._metrics["train"]
            if self.algo in ("dpo_on", "dpo_off"):
                s, s_ref = self._logp_cau(out), self._logp_cau(out, ref=True)
                A, n, mg = a_dpo(r, s, s_ref, G, ntok, HS["dpo_beta"], ok)
                mt["luoi/n_cap"].append(float(n))
                mt["luoi/dpo_margin"].append(mg)
                mt["luoi/logp_tru_ref"].append(float((s - s_ref).mean()))
            elif self.algo == "rft_off":
                A = CD._top(r.view(-1, G), 1).flatten()
            elif self.algo == "mrt":
                s = self._logp_cau(out)
                A = a_mrt(r, s, G, ntok, HS["mrt_alpha"])
                Q = torch.softmax(HS["mrt_alpha"] * s.view(-1, G), 1)
                mt["luoi/mrt_q_max"].append(float(Q.max(1).values.mean()))
            elif self.algo == "spg":
                A = a_spg(r, G, ntok, HS["spg_tau"])
            assert torch.isfinite(A).all(), "⛔ lợi thế không hữu hạn"
            # lớp cha đã ghi hai trường từ lợi thế tạm: thay bằng lợi thế thật, không ghi dòng thứ hai
            mt["luoi/adv_abs_mean"][-1] = float(A.abs().mean())
            mt["luoi/frac_adv_zero"][-1] = float((A.abs() < 1e-9).float().mean())
            if self.algo in OFF:
                mt["luoi/sinh_tu_s1"].append(float(self.n_sinh_s1))
            out["advantages"] = A.to(out["advantages"].device, dtype=out["advantages"].dtype)
            return out

    return MoiTrainer


# ============================ tự kiểm ============================
def selftest_moi(_):
    """Gradient của mất mát thay thế −Σ A_i s_i / N_tok phải trùng gradient của mục tiêu gốc theo s (autograd)."""
    import torch
    torch.manual_seed(0)
    G, P, ntok = 4, 3, 37.0
    r = torch.tensor([0.2, 0.9, 0.5, 0.1, 0.5, 0.5, 0.5, 0.5, 0.3, 0.8, 0.8, 0.0])
    s0 = -torch.rand(G * P) * 10
    sref = s0 - torch.randn(G * P) * 0.3

    def kiem(ten, A, muc_tieu):
        s = s0.clone().requires_grad_(True)
        muc_tieu(s).backward()
        g_goc = s.grad.clone()
        g_thay = -A / ntok
        assert torch.allclose(g_goc, g_thay, atol=1e-6), f"⛔ {ten}\n{g_goc}\n{g_thay}"
        print(f"  {ten:8s} ∇ trùng autograd ✓  |A| TB {float(A.abs().mean()):.4f}")

    beta = 0.1
    A, n, _ = a_dpo(r, s0, sref, G, ntok, beta)
    assert n == 2, n                                      # nhóm 2 thưởng bằng nhau: không có cặp

    def dpo(s):
        L = 0.0
        pairs = [(1, 3), (9, 11)]                         # nhóm 0: chosen 0,9 (chỉ số 1), rejected 0,1 (3); nhóm 2: 9 / 11
        for c, j in pairs:
            h = (s[c] - sref[c]) - (s[j] - sref[j])
            L = L - torch.nn.functional.logsigmoid(beta * h)
        return L / P
    kiem("dpo", A, dpo)
    ok = torch.ones(G * P, dtype=torch.bool)
    ok[9] = False                                         # câu bị cắt: nhóm 2 phải chọn chosen là chỉ số 10
    A2, n2, _ = a_dpo(r, s0, sref, G, ntok, beta, ok)
    assert n2 == 2 and A2[9] == 0 and A2[10] > 0, A2

    alpha = 0.005
    A = a_mrt(r, s0, G, ntok, alpha)

    def mrt(s):
        Q = torch.softmax(alpha * s.view(-1, G), 1)
        return (Q * (-r.view(-1, G))).sum(1).mean()
    kiem("mrt", A, mrt)

    tau = 0.2
    A = a_spg(r, G, ntok, tau)
    w = torch.softmax(r.view(-1, G) / tau, 1)
    # ước lượng SPG: tối đa hoá Σ_p [Σ_y w_y s_y − TB_y s_y] / P (w không phụ thuộc s vì mẫu lấy từ π)

    def spg(s):
        sv = s.view(-1, G)
        return -((w * sv).sum(1) - sv.mean(1)).mean()
    kiem("spg", A, spg)
    assert torch.allclose(A.view(-1, G).sum(1), torch.zeros(P), atol=1e-5)

    A = CD._top(r.view(-1, G), 1).flatten()
    assert A.tolist() == [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], A   # nhóm 2 hoà 0,8/0,8: stable chọn chỉ số đầu
    assert torch.allclose(loi_the("grpo", r.tolist(), G)[0], _cu("grpo", r.tolist(), G)[0])
    print("✅ selftest công thức MỚI ĐẠT:", " · ".join(MOI))


def selftest_cpu(a):
    """3 bước mỗi thuật toán trên mô hình tí hon (CPU fp32): chạy hết vòng TRL, loss và lợi thế hữu hạn, LoRA có đổi."""
    import re, json, time, shutil, torch, transformers, trl, peft
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    from trl import GRPOConfig
    from datasets import Dataset
    print(f"trl {trl.__version__} · transformers {transformers.__version__} · peft {peft.__version__} · torch {torch.__version__}",
          flush=True)
    Mten = "trl-internal-testing/tiny-Qwen2ForCausalLM-2.5"
    golds = ["Click on the search bar", "Open the Clock app", "Swipe up to see more", "Type hello in the box"]
    rows = [dict(key=f"k{i}", prompt=[{"role": "user", "content": f"Describe step {i}"}], gold=golds[i % 4],
                 action_type="") for i in range(16)]
    W = re.compile(r"[a-z0-9]+")

    def r_gia(completions, gold, **kw):                   # F1 từ đơn, tất định, khác nhau giữa các câu
        out = []
        for c, g in zip(completions, gold):
            a_, b_ = set(W.findall(GL.GS._text(c).lower())), set(W.findall(g.lower()))
            k = len(a_ & b_)
            out.append(0.0 if not k else 2 * k / (len(a_) + len(b_)))
        out = [x + 0.01 * (len(GL.GS._text(c)) % 5) for x, c in zip(out, completions)]   # phá hoà khi F1 = 0
        GL.LAST["r"] = list(out)
        return out

    algos = a.algos.split(",") if a.algos else list(MOI) + list(ALIAS) + ["grpo", "drgrpo", "rft"]
    kq = {}
    for ten in algos:
        base, ov = ALIAS.get(ten, (ten, {}))
        t0 = time.time()
        out = os.path.join(a.out or "/tmp/b1_cpu", ten)
        shutil.rmtree(out, ignore_errors=True)
        transformers.set_seed(101)
        tk = AutoTokenizer.from_pretrained(Mten)
        tk.padding_side = "left"
        m = AutoModelForCausalLM.from_pretrained(Mten, dtype=torch.float32)
        m = get_peft_model(m, LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0, target_modules=["q_proj", "v_proj"],
                                         task_type="CAUSAL_LM"))
        beta = 0.0 if base in ("dpo_on", "dpo_off") else 0.04
        want = dict(output_dir=out, seed=101, num_generations=4, per_device_train_batch_size=4,
                    gradient_accumulation_steps=2, max_completion_length=12, temperature=1.0, top_p=1.0, top_k=0,
                    beta=beta, learning_rate=1e-2, max_steps=3 * ov.get("num_iterations", 1), logging_steps=1,
                    save_steps=10 ** 6, report_to="none", remove_unused_columns=False, use_cpu=True, bf16=False,
                    fp16=False, lr_scheduler_type="constant", disable_tqdm=True, mask_truncated_completions=False,
                    scale_rewards=("none" if base == "drgrpo" else "group"), loss_type="dapo", num_iterations=1)
        want.update(ov)
        args = GRPOConfig(**want)
        T = lop_trainer()
        tr = T(model=m, reward_funcs=[r_gia], args=args, train_dataset=Dataset.from_list(rows), processing_class=tk)
        tr.algo, tr.thuong = base, r_gia
        nB = lambda: sum(p.norm().item() for n_, p in tr.model.named_parameters() if "lora_B" in n_)
        # đếm số lần nhánh LoRA chạy TRONG LÚC SINH: tắt adapter thì PEFT bỏ qua lora_B, nên OFF phải ra 0
        dem = {"sinh": False, "lora": 0}
        for n_, mod in tr.model.named_modules():
            if n_.endswith("lora_B.default"):
                mod.register_forward_hook(lambda *_: dem.__setitem__("lora", dem["lora"] + dem["sinh"]))
        goc_gen = tr._generate

        def gen_dem(p, _g=goc_gen):
            dem["sinh"] = True
            try:
                return _g(p)
            finally:
                dem["sinh"] = False
        tr._generate = gen_dem
        truoc = nB()
        tr.train()
        sau = nB()
        lech = {k: (getattr(tr.args, k), v) for k, v in ov.items() if getattr(tr.args, k) != v}
        assert not lech, f"⛔ {ten}: cấu hình TRL không áp {lech}"
        H = tr.state.log_history
        loss = [h["loss"] for h in H if "loss" in h]
        adv = [h.get("luoi/adv_abs_mean") for h in H if "luoi/adv_abs_mean" in h]
        ok = (len(loss) >= 3 and all(math.isfinite(x) for x in loss) and sau > truoc
              and (base == "grpo" or (adv and all(math.isfinite(x) for x in adv))))
        ok = ok and ((dem["lora"] == 0) if base in OFF else (dem["lora"] > 0))
        if base in OFF:
            ok = ok and tr.n_sinh_s1 >= 3
        if base in ("dpo_on", "dpo_off"):
            ok = ok and any(h.get("luoi/n_cap", 0) > 0 for h in H)
        if ten == "gspo":
            ok = ok and abs(tr.args.epsilon - 3e-4) < 1e-12 and tr.args.importance_sampling_level == "sequence"
        kq[ten] = dict(dat=bool(ok), loss=[round(x, 5) for x in loss], adv=[round(x, 4) for x in adv or []],
                       lora_B=[round(truoc, 4), round(sau, 4)], lora_luc_sinh=dem["lora"],
                       cau_hinh={k: getattr(tr.args, k) for k in ("loss_type", "scale_rewards", "num_iterations",
                                                                   "importance_sampling_level", "epsilon", "epsilon_high", "beta")},
                       giay=round(time.time() - t0, 1),
                       them={k: [round(h[k], 4) for h in H if k in h] for k in
                             ("luoi/n_cap", "luoi/dpo_margin", "luoi/mrt_q_max", "luoi/sinh_tu_s1", "kl") if any(k in h for h in H)})
        print(f"[{ten}] {'ĐẠT' if ok else '⛔ KHÔNG ĐẠT'} · {json.dumps(kq[ten], ensure_ascii=False)}", flush=True)
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        json.dump(kq, open(os.path.join(a.out, "selftest_cpu.json"), "w"), ensure_ascii=False, indent=1)
    hong = [k for k, v in kq.items() if not v["dat"]]
    assert not hong, f"⛔ không đạt: {hong}"
    print(f"✅ selftest CPU ĐẠT {len(kq)} thuật toán:", " · ".join(kq), flush=True)


# ============================ chạy ============================
GL.ALGOS = GL.ALGOS + MOI
GL.loi_the = loi_the
GL.lop_trainer = lop_trainer


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--algo", default="grpo")
    ap.add_argument("--dpo-beta", type=float, default=HS["dpo_beta"])
    ap.add_argument("--mrt-alpha", type=float, default=HS["mrt_alpha"])
    ap.add_argument("--spg-tau", type=float, default=HS["spg_tau"])
    ap.add_argument("--eps-low", type=float, default=None)
    ap.add_argument("--selftest-cpu", action="store_true")
    ap.add_argument("--algos", default="")
    a, rest = ap.parse_known_args()
    HS.update(dpo_beta=a.dpo_beta, mrt_alpha=a.mrt_alpha, spg_tau=a.spg_tau)
    if "--selftest-algo" in rest:
        return selftest_moi(a)
    if a.selftest_cpu:
        o = rest[rest.index("--out") + 1] if "--out" in rest else ""
        a.out = o
        return selftest_cpu(a)
    base, ov = ALIAS.get(a.algo, (a.algo, {}))
    CD.OVERRIDE.update(ov)
    if a.eps_low is not None:
        CD.OVERRIDE["epsilon"] = a.eps_low
    if base in ("dpo_on", "dpo_off") and "--beta" not in rest:
        rest += ["--beta", "0"]
    print(f"[moi_b1] --algo {a.algo} → {base} · đè TRL {ov or '-'} · siêu tham số {HS}", flush=True)
    if CD.OVERRIDE.get("num_iterations", 1) > 1 and "--max-steps" not in rest:
        print("⚠️ μ > 1 mà để --max-steps 500: chỉ đi qua 500 câu nhắc; cùng 1.000 câu nhắc như ck500 thì --max-steps 1000",
              flush=True)
    # grpo_codien.main dựng OVERRIDE từ cờ của nó rồi vá GRPOConfig; khoá của bí danh đã nằm sẵn trong OVERRIDE
    CD.main(rest + ["--algo", base])


if __name__ == "__main__":
    main()
