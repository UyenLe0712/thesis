"""Lưới RL, đợt b4: thêm ORPO (trực tuyến / từ S1), DPO bán trực tuyến và GPG trên cùng vòng lặp ck500.

Không sửa tệp nào có sẵn. Chuỗi vá nối tiếp: grpo_luoi (GL) ← grpo_codien (CD) ← grpo_moi_b1 (B1) ← tệp này. Tệp này
import B1 (B1 đã vá GL.loi_the / GL.lop_trainer / GL.ALGOS), vá thêm một lớp, rồi gọi B1.main() → CD.main() → GL.train().
Vì vậy điểm xuất phát (S1 hoà + LoRA mới), 1.000 câu nhắc, G = 8, lr 1e-5, 500 bước, μ = 1, thưởng SPICE, điểm lưu
mỗi 25 bước và dòng log `[nạp default]` giữ nguyên như ck500.

Cách cài giống B1: với μ = 1, gradient mất mát TRL (loss_type "dapo") là ∇L = −(1/N_tok)·Σ_i A_i·∇s_i, s_i = log π(y_i)
(tổng log-prob token), N_tok = tổng token câu sinh của lô sinh. Mỗi thuật toán chỉ cần đặt A_i = −N_tok·∂L_gốc/∂s_i,
khi đó gradient TRL trùng ĐÚNG gradient mục tiêu gốc (kiểm bằng autograd ở --selftest-algo). P = số câu nhắc trong lô sinh.

Thuật toán mới (--algo):
  orpo_on   ORPO (Hong, Lee & Thorne, EMNLP 2024) trực tuyến. Mỗi nhóm G câu: chosen = câu thưởng cao nhất, rejected =
            thấp nhất (bỏ câu bị cắt ở 96 token; nhóm hoà thì không có cặp, A = 0), như a_dpo của B1.
            ℓ = s/|y| (TB log-prob theo token), mất mát mỗi cặp
                L = −ℓ_c + λ·(−log σ(z)),  z = [ℓ_c − log(1−e^{ℓ_c})] − [ℓ_r − log(1−e^{ℓ_r})],  λ = 0,1 (--orpo-lam)
            TB theo P câu nhắc. 1−e^ℓ tính bằng −expm1(ℓ) và kẹp ≥ 1e−6 (chỉ đụng khi ℓ > −1e−6).
            Không cần mô hình tham chiếu ⇒ β KL mặc định 0.
            Khác bài gốc phải khai: (1) bài gốc dùng tập cặp cố định (UltraFeedback…), ở đây cặp dựng trực tuyến từ mẫu
            của chính sách và thưởng SPICE; (2) vế SFT ở đây là −ℓ_c TB theo câu (theo đặc tả lưới), còn ORPOTrainer
            của TRL lấy NLL TB theo token gộp cả lô; (3) mỗi câu nhắc chỉ một cặp (cao nhất/thấp nhất).
  orpo_off  Như orpo_on nhưng câu SINH TỪ S1 ĐÓNG BĂNG (tắt LoRA lúc sinh, giống dpo_off của B1) ⇒ tương đương ORPO một
            lượt trên tập cặp dựng sẵn từ mẫu của S1 trên 1.000 câu nhắc. Đây là dạng gần bài gốc nhất (ngoại tuyến).
  dpo_semi  DPO bán trực tuyến (Lanchantin và cộng sự 2025, "Bridging Offline and Online Reinforcement Learning for
            LLMs", arXiv 2506.21495, preprint [cần kiểm venue]). Câu sinh từ một BẢN CHỤP chính sách (adapter PEFT thứ
            hai tên "gen", không học, không vào optimizer), bản chụp đồng bộ với chính sách mỗi K lần sinh
            (--dpo-sync, mặc định 10 [suy]: bài gốc báo s = 5 hoặc 10 cho tác vụ không kiểm chứng được, s = 100 cho
            toán, theo bản tóm tắt chưa đối chiếu bảng gốc). Mất mát DPO y như dpo_on của B1 (tham chiếu S1, β_d 0,1
            qua --dpo-beta). dpo_off = K vô hạn, dpo_on = K = 1. Ở đây mỗi lần sinh = một bước cập nhật (steps_per_
            generation = gradient_accumulation_steps), nên K lần sinh = K bước optimizer.
            Adapter "gen" tạo lười ở lần sinh đầu tiên (sau assert ntr == ns1 của GL.train và sau khi optimizer đã dựng).
            Nối tiếp (resume): lần sinh đầu tiên của tiến trình luôn đồng bộ, rồi theo nhịp (k − 1) mod K = 0 với k là số
            thứ tự lần sinh toàn cục (tính lại từ global_step). Mỗi lần đồng bộ in `[dpo_semi] đồng bộ lần n ở lần sinh k`.
            Điểm lưu có thêm thư mục con gen/; transformers khi resume chỉ nạp thư mục con (gen/) chứ không nạp default ở
            gốc, nhưng GL.train đã nạp tay default trước đó ([nạp default]) và gen bị đè ngay ở lần sinh đầu.
  gpg       GPG (Chu và cộng sự, "GPG: A Simple and Strong Reinforcement Learning Baseline for Model Reasoning",
            arXiv 2504.02546; trường comments ghi "Accepted to ICLR2026" [chưa kiểm trên OpenReview]).
                A = α·(r − mean_nhóm)/F_norm,  α = B/(B − M)
            B = số câu trong lô sinh, M = số câu thuộc nhóm có thưởng bằng nhau hết (A = 0). β KL = 0, không clip (μ = 1).
            F_norm (--gpg-std): mặc định 0 tức F_norm = 1, theo bài gốc (Table 1: α = B/(B−M) với F_norm = 1 được 47,8,
            chia std 44,1; Table 14/15 hàng chính của GPG không chia std; đã đọc bản HTML v4 ngày 7/11/2026).
            Lô sinh ở đây chỉ 2 câu nhắc × 8 câu ⇒ α ∈ {1; 2}; lô toàn hoà thì A = 0. Gộp mất mát theo token như bài gốc
            (Eq. 5 chia cho Σ|o_i|), trùng loss_type dapo đang dùng.

Cờ MỚI: --orpo-lam (0,1) · --dpo-sync (10) · --gpg-std {0,1} (0). --dpo-beta của B1 dùng chung cho dpo_semi.
β mặc định 0 cho orpo_on · orpo_off · dpo_semi · gpg nếu không truyền --beta. Mọi cờ khác như grpo_moi_b1 / grpo_codien.

  python -I grpo_moi_b4.py --selftest-algo                          # CPU, không mạng: lợi thế ORPO/GPG vs autograd + selftest B1
  python -I grpo_moi_b4.py --selftest-cpu [--algos orpo_on,gpg]     # CPU, cần mạng tải trl-internal-testing/tiny-Qwen2...
  python grpo_moi_b4.py --train --algo dpo_semi --reward spice --bundle B --merged M --out O --resume auto
"""
import os, sys, math, copy, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_moi_b1 as B1                                  # noqa: E402  (import này vá GL qua codien rồi b1)
CD = B1.CD
GL = B1.GL

MOI4 = ("orpo_on", "orpo_off", "dpo_semi", "gpg")
OFF4 = ("orpo_off",)                                      # sinh từ S1 đóng băng
HS4 = dict(orpo_lam=0.1, dpo_sync=10, gpg_std=0)
EPS_ODDS = 1e-6
_cu = GL.loi_the                                          # = B1.loi_the
_lop = GL.lop_trainer                                     # = B1.lop_trainer


# ============================ công thức (tensor thuần, kiểm bằng autograd) ============================
def _cap(r, G, ok):
    """Chỉ số (chosen, rejected) mỗi nhóm như a_dpo của B1; None khi nhóm hoà hoặc rơi vào câu bị cắt."""
    import torch
    r = r.view(-1, G).float()
    okv = torch.ones_like(r, dtype=torch.bool) if ok is None else ok.view(-1, G)
    hi = r.masked_fill(~okv, -math.inf).argmax(1)
    lo = r.masked_fill(~okv, math.inf).argmin(1)
    out = []
    for p in range(r.shape[0]):
        c, j = int(hi[p]), int(lo[p])
        if not (okv[p, c] and okv[p, j]) or r[p, c] - r[p, j] < 1e-9:
            out.append(None)
        else:
            out.append((c, j))
    return out


def a_orpo(r, s, ny, G, ntok, lam, ok=None):
    """r, s, ny: (N,) theo nhóm liền nhau; s = tổng log-prob câu, ny = số token câu. Trả (A, số cặp, thống kê)."""
    import torch
    P = r.numel() // G
    sv = s.view(-1, G).double()
    nv = ny.view(-1, G).double().clamp(min=1.0)
    A = torch.zeros(P, G, dtype=torch.float64)
    n, zs, lcs, lrs = 0, [], [], []
    for p, cj in enumerate(_cap(r, G, ok)):
        if cj is None:
            continue
        c, j = cj
        lc, lr_ = sv[p, c] / nv[p, c], sv[p, j] / nv[p, j]
        dc, dr = (-torch.expm1(lc)).clamp(min=EPS_ODDS), (-torch.expm1(lr_)).clamp(min=EPS_ODDS)
        z = (lc - torch.log(dc)) - (lr_ - torch.log(dr))
        w = lam * torch.sigmoid(-z)
        A[p, c] += (1.0 + w / dc) / nv[p, c]              # −∂L/∂s_c = (1 + λσ(−z)/(1−e^{ℓ_c}))/|y_c|
        A[p, j] += (-w / dr) / nv[p, j]                    # −∂L/∂s_r = −λσ(−z)/(1−e^{ℓ_r})/|y_r|
        n += 1
        zs.append(float(z)); lcs.append(float(lc)); lrs.append(float(lr_))
    A = (A * (ntok / P)).float()
    tb = lambda x: sum(x) / len(x) if x else 0.0
    return A.flatten(), n, dict(z=tb(zs), lc=tb(lcs), lr=tb(lrs))


def a_gpg(r, G, chia_std):
    """Trả (A, α). r: (N,) theo nhóm liền nhau = toàn bộ lô sinh (B = N)."""
    import torch
    r = r.view(-1, G).float()
    B = r.numel()
    hoa = (r.max(1).values - r.min(1).values) < 1e-9
    M = int(hoa.sum()) * G
    if M == B:
        return torch.zeros(B), 1.0
    A = r - r.mean(1, keepdim=True)
    if chia_std:
        A = A / (r.std(1, keepdim=True) + 1e-4)
    A[hoa] = 0.0
    al = B / (B - M)
    return (al * A).flatten(), al


def loi_the(algo, r, G, b=None, r_greedy=None):
    """gpg cho lợi thế thật ngay ở đây; orpo_*/dpo_semi nhận lợi thế tạm drgrpo, lợi thế thật đặt ở lớp con."""
    import torch
    if algo == "gpg":
        return a_gpg(torch.tensor(r, dtype=torch.float32), G, HS4["gpg_std"])[0], b
    if algo in MOI4:
        return _cu("drgrpo", r, G)
    return _cu(algo, r, G, b=b, r_greedy=r_greedy)


# ============================ lớp trainer ============================
def lop_trainer():
    import torch
    from trl.trainer.utils import use_adapter
    Bc = _lop()

    class B4Trainer(Bc):
        n_sinh_s1 = 0
        hook_gen = None                                   # chỉ selftest dùng: gọi với mô hình PEFT khi gen sẵn sàng
        _gen_cap = None
        _n_sinh = 0
        _k0 = None
        _n_dongbo = 0

        def __init__(self, *args, **kw):
            super().__init__(*args, **kw)
            self.semi_log = []

        # ---------- dpo_semi: bản chụp "gen" ----------
        def _chuan_bi_gen(self):
            m = self.accelerator.unwrap_model(self.model)
            if "gen" not in m.peft_config:
                nhoc = sum(p.numel() for p in m.parameters() if p.requires_grad)
                cfg = copy.deepcopy(m.peft_config["default"])
                m.add_adapter("gen", cfg)
                m.set_adapter("default")
                for n_, p in m.named_parameters():
                    if ".gen." in n_:
                        p.requires_grad_(False)
                nsau = sum(p.numel() for p in m.parameters() if p.requires_grad)
                assert nsau == nhoc, f"⛔ tạo gen làm đổi số tham số học {nhoc} → {nsau}"
                print(f"[dpo_semi] tạo adapter gen · tham số học giữ {nhoc:,}", flush=True)
            else:
                print("[dpo_semi] adapter gen đã có (nạp từ điểm lưu), sẽ đè ngay", flush=True)
                for n_, p in m.named_parameters():
                    if ".gen." in n_:
                        p.requires_grad_(False)
            assert m.active_adapter == "default", m.active_adapter
            cap = []
            for n_, p in m.named_parameters():
                if "lora_" in n_ and ".default." in n_:
                    cap.append((p, m.get_parameter(n_.replace(".default.", ".gen."))))
            assert cap, "⛔ không thấy tham số LoRA default"
            self._gen_cap = cap
            if self.hook_gen is not None:
                self.hook_gen(m)

        @torch.no_grad()
        def _lech_gen(self):
            return math.sqrt(sum(float((pg.float() - pd.float()).pow(2).sum()) for pd, pg in self._gen_cap))

        @torch.no_grad()
        def _dong_bo(self):
            for pd, pg in self._gen_cap:
                pg.data = pd.data.detach().clone()            # cùng dtype/thiết bị với default
                pg.requires_grad_(False)

        def _generate(self, prompts):
            if not self.model.training or self.algo not in ("orpo_off", "dpo_semi"):
                return super()._generate(prompts)
            if self.algo == "orpo_off":
                self.n_sinh_s1 += 1
                with self._ref_ctx():
                    return super()._generate(prompts)
            # dpo_semi
            if self._gen_cap is None:
                self._chuan_bi_gen()
                self._k0 = (self.state.global_step * self.args.gradient_accumulation_steps
                            // self.args.steps_per_generation)
            self._n_sinh += 1
            k = self._k0 + self._n_sinh                       # số thứ tự lần sinh toàn cục, từ 1
            K = HS4["dpo_sync"]
            lech = self._lech_gen()
            sync = self._n_sinh == 1 or (k - 1) % K == 0
            if sync:
                self._dong_bo()
                self._n_dongbo += 1
                print(f"[dpo_semi] đồng bộ lần {self._n_dongbo} ở lần sinh {k} · lệch trước {lech:.3e}", flush=True)
            self.semi_log.append(dict(k=k, dong_bo=sync, lech_truoc=lech, lech_sau=self._lech_gen()))
            self._metrics["train"]["luoi/gen_lech_default"].append(lech)
            m = self.accelerator.unwrap_model(self.model)
            with use_adapter(m, adapter_name="gen"):
                out = super()._generate(prompts)
            assert m.active_adapter == "default", m.active_adapter
            return out

        def _generate_and_score_completions(self, inputs):
            out = super()._generate_and_score_completions(inputs)
            if self.algo not in MOI4 or not self.model.training:
                return out
            G = self.num_generations
            r = torch.tensor(GL.LAST["r"], dtype=torch.float32)
            mt = self._metrics["train"]
            if self.algo == "gpg":
                _, al = a_gpg(r, G, HS4["gpg_std"])
                mt["luoi/gpg_alpha"].append(float(al))
                return out
            ntok = float(out["num_items_in_batch"])
            ny = out["completion_mask"].sum(1).float().cpu()
            ok = (ny > 0)
            if self.algo in ("orpo_on", "orpo_off"):
                s = self._logp_cau(out)
                A, n, tk = a_orpo(r, s, ny, G, ntok, HS4["orpo_lam"], ok)
                mt["luoi/n_cap"].append(float(n))
                mt["luoi/orpo_z"].append(tk["z"])
                mt["luoi/orpo_lc"].append(tk["lc"])
                mt["luoi/orpo_lr"].append(tk["lr"])
            else:                                          # dpo_semi: mất mát DPO của B1
                s, s_ref = self._logp_cau(out), self._logp_cau(out, ref=True)
                A, n, mg = B1.a_dpo(r, s, s_ref, G, ntok, B1.HS["dpo_beta"], ok)
                mt["luoi/n_cap"].append(float(n))
                mt["luoi/dpo_margin"].append(mg)
                mt["luoi/logp_tru_ref"].append(float((s - s_ref).mean()))
                mt["luoi/n_dong_bo"].append(float(self._n_dongbo))
            assert torch.isfinite(A).all(), "⛔ lợi thế không hữu hạn"
            mt["luoi/adv_abs_mean"][-1] = float(A.abs().mean())
            mt["luoi/frac_adv_zero"][-1] = float((A.abs() < 1e-9).float().mean())
            if self.algo in OFF4:
                mt["luoi/sinh_tu_s1"].append(float(self.n_sinh_s1))
            out["advantages"] = A.to(out["advantages"].device, dtype=out["advantages"].dtype)
            return out

    return B4Trainer


# ============================ tự kiểm ============================
def selftest_b4(a):
    """Gradient của −Σ A_i s_i / N_tok phải trùng gradient mục tiêu gốc theo s (autograd). Rồi chạy selftest của B1."""
    import torch
    torch.manual_seed(0)
    G, P, ntok = 4, 3, 37.0
    r = torch.tensor([0.2, 0.9, 0.5, 0.1, 0.5, 0.5, 0.5, 0.5, 0.3, 0.8, 0.8, 0.0])
    ny = torch.tensor([5., 9., 7., 3., 6., 6., 6., 6., 4., 11., 8., 2.])
    s0 = -(torch.rand(G * P) * 8 + 0.5) * ny / 4          # ℓ = s/|y| ∈ khoảng (−2,1; −0,1), xa chỗ kẹp

    def kiem(ten, A, muc_tieu, s_goc=s0):
        s = s_goc.clone().double().requires_grad_(True)
        muc_tieu(s).backward()
        g_goc, g_thay = s.grad.float(), -A / ntok
        assert torch.allclose(g_goc, g_thay, atol=1e-6, rtol=1e-5), f"⛔ {ten}\n{g_goc}\n{g_thay}"
        print(f"  {ten:10s} ∇ trùng autograd ✓  |A| TB {float(A.abs().mean()):.4f}")

    def orpo_goc(cap, lam):
        def f(s):
            L = 0.0
            for c, j in cap:
                lc, lr_ = s[c] / ny[c], s[j] / ny[j]
                z = (lc - torch.log(-torch.expm1(lc))) - (lr_ - torch.log(-torch.expm1(lr_)))
                L = L - lc - lam * torch.nn.functional.logsigmoid(z)
            return L / P
        return f

    for lam in (0.1, 1.0):
        A, n, tk = a_orpo(r, s0, ny, G, ntok, lam)
        assert n == 2, n                                  # nhóm 1 hoà: không cặp
        assert (A.view(-1, G)[1] == 0).all()
        kiem(f"orpo λ={lam}", A, orpo_goc([(1, 3), (9, 11)], lam))
    ok = torch.ones(G * P, dtype=torch.bool)
    ok[9] = False                                         # câu bị cắt: nhóm 2 chọn chosen là chỉ số 10
    A, n, _ = a_orpo(r, s0, ny, G, ntok, 0.1, ok)
    assert n == 2 and A[9] == 0 and A[10] > 0
    kiem("orpo cắt", A, orpo_goc([(1, 3), (10, 11)], 0.1))
    # ℓ sát 0: kẹp giữ hữu hạn
    s_sat = s0.clone()
    s_sat[1] = -1e-9
    A, _, _ = a_orpo(r, s_sat, ny, G, ntok, 0.1)
    assert torch.isfinite(A).all(), A
    print("  orpo ℓ≈0   hữu hạn nhờ kẹp ✓")

    for std in (0, 1):
        A, al = a_gpg(r, G, std)
        assert abs(al - 12 / 8) < 1e-9, al                # B = 12, M = 4 (nhóm 1 hoà)
        rv = r.view(-1, G)
        Fn = (rv.std(1, keepdim=True) + 1e-4) if std else torch.ones(P, 1)
        Ah = ((rv - rv.mean(1, keepdim=True)) / Fn)
        Ah[1] = 0.0

        def gpg(s, Ah=Ah, al=al):                         # mất mát GPG Eq. 5 + α: −α/N_tok · Σ_i Â_i s_i
            return -(al * Ah.flatten().double() * s).sum() / ntok
        kiem(f"gpg std={std}", A, gpg)
        assert abs(float(A.view(-1, G)[0, 1]) - al * float(Ah[0, 1])) < 1e-6
    A, al = a_gpg(torch.tensor([0.5] * 8), G, 0)
    assert A.abs().max() == 0 and al == 1.0
    A, al = a_gpg(torch.tensor([0.1, 0.3, 0.5, 0.7, 0.4, 0.4, 0.4, 0.4]), G, 0)
    assert al == 2.0 and torch.allclose(A[:4], torch.tensor([-0.6, -0.2, 0.2, 0.6]), atol=1e-6), A
    HS4["gpg_std"] = 0
    assert torch.allclose(loi_the("gpg", r.tolist(), G)[0], a_gpg(r, G, 0)[0])
    assert torch.allclose(loi_the("orpo_on", r.tolist(), G)[0], GL.loi_the("drgrpo", r.tolist(), G)[0])
    assert torch.allclose(loi_the("grpo", r.tolist(), G)[0], _cu("grpo", r.tolist(), G)[0])
    assert all(x in GL.ALGOS for x in MOI4 + B1.MOI + CD.MOI)
    print("✅ selftest công thức b4 ĐẠT:", " · ".join(MOI4))
    print("— selftest của B1 —")
    B1.selftest_moi(a)
    print("— selftest của grpo_codien —")
    CD.selftest_codien(a)


def selftest_cpu(a):
    """3 bước mỗi thuật toán trên mô hình tí hon (CPU fp32); dpo_semi thêm một pha nối tiếp từ điểm lưu."""
    import re, json, time, shutil, torch, transformers, trl, peft
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model, set_peft_model_state_dict, get_peft_model_state_dict
    from safetensors.torch import load_file
    from trl import GRPOConfig
    from datasets import Dataset
    print(f"trl {trl.__version__} · transformers {transformers.__version__} · peft {peft.__version__} · torch {torch.__version__}",
          flush=True)
    Mten = "trl-internal-testing/tiny-Qwen2ForCausalLM-2.5"
    golds = ["Click on the search bar", "Open the Clock app", "Swipe up to see more", "Type hello in the box"]
    rows = [dict(key=f"k{i}", prompt=[{"role": "user", "content": f"Describe step {i}"}], gold=golds[i % 4],
                 action_type="") for i in range(16)]
    W = re.compile(r"[a-z0-9]+")

    def r_gia(completions, gold, **kw):
        out = []
        for c, g in zip(completions, gold):
            a_, b_ = set(W.findall(GL.GS._text(c).lower())), set(W.findall(g.lower()))
            k = len(a_ & b_)
            out.append(0.0 if not k else 2 * k / (len(a_) + len(b_)))
        out = [x + 0.01 * (len(GL.GS._text(c)) % 5) for x, c in zip(out, completions)]
        GL.LAST["r"] = list(out)
        return out

    K_TEST = 2
    goc_sync = HS4["dpo_sync"]
    HS4["dpo_sync"] = K_TEST
    algos = a.algos.split(",") if a.algos else list(MOI4)
    goc = a.out or "/tmp/b4_cpu"
    kq = {}

    def dung(ten, out, max_steps, save_steps):
        transformers.set_seed(101)
        tk = AutoTokenizer.from_pretrained(Mten)
        tk.padding_side = "left"
        m = AutoModelForCausalLM.from_pretrained(Mten, dtype=torch.float32)
        m = get_peft_model(m, LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0, target_modules=["q_proj", "v_proj"],
                                         task_type="CAUSAL_LM"))
        args = GRPOConfig(output_dir=out, seed=101, num_generations=4, per_device_train_batch_size=4,
                          gradient_accumulation_steps=2, max_completion_length=12, temperature=1.0, top_p=1.0, top_k=0,
                          beta=0.0, learning_rate=1e-2, max_steps=max_steps, logging_steps=1, save_steps=save_steps,
                          report_to="none", remove_unused_columns=False, use_cpu=True, bf16=False, fp16=False,
                          lr_scheduler_type="constant", disable_tqdm=True, mask_truncated_completions=False,
                          scale_rewards="group", loss_type="dapo", num_iterations=1)
        tr = lop_trainer()(model=m, reward_funcs=[r_gia], args=args, train_dataset=Dataset.from_list(rows),
                           processing_class=tk)
        tr.algo, tr.thuong = ten, r_gia
        dem = {"sinh": False, "default": 0, "gen_sinh": 0, "gen_ngoai": 0}
        for n_, mod in tr.model.named_modules():
            if n_.endswith("lora_B.default"):
                mod.register_forward_hook(lambda *_: dem.__setitem__("default", dem["default"] + dem["sinh"]))

        def hook_gen(pm):
            for n_, mod in pm.named_modules():
                if n_.endswith("lora_B.gen"):
                    mod.register_forward_hook(lambda *_: dem.__setitem__(
                        "gen_sinh" if dem["sinh"] else "gen_ngoai", dem["gen_sinh" if dem["sinh"] else "gen_ngoai"] + 1))
        tr.hook_gen = hook_gen
        goc_gen = tr._generate

        def gen_dem(p, _g=goc_gen):
            dem["sinh"] = True
            try:
                return _g(p)
            finally:
                dem["sinh"] = False
        tr._generate = gen_dem
        return tr, dem

    try:
        for ten in algos:
            t0 = time.time()
            out = os.path.join(goc, ten)
            shutil.rmtree(out, ignore_errors=True)
            tr, dem = dung(ten, out, 3, 2 if ten == "dpo_semi" else 10 ** 6)
            nB = lambda t: sum(p.norm().item() for n_, p in t.model.named_parameters()
                               if "lora_B" in n_ and ".default." in n_)
            nhoc0 = sum(p.numel() for p in tr.model.parameters() if p.requires_grad)
            truoc = nB(tr)
            tr.train()
            sau = nB(tr)
            nhoc1 = sum(p.numel() for p in tr.model.parameters() if p.requires_grad)
            H = tr.state.log_history
            loss = [h["loss"] for h in H if "loss" in h]
            adv = [h.get("luoi/adv_abs_mean") for h in H if "luoi/adv_abs_mean" in h]
            ly = []
            ok = (len(loss) >= 3 and all(math.isfinite(x) for x in loss) and sau > truoc and adv
                  and all(math.isfinite(x) for x in adv) and nhoc1 == nhoc0)
            if not ok:
                ly.append("loss/adv/LoRA/số tham số học")
            if ten in OFF4:
                if not (dem["default"] == 0 and tr.n_sinh_s1 >= 3):
                    ly.append("OFF: LoRA chạy lúc sinh")
            elif ten == "dpo_semi":
                if dem["default"] != 0:
                    ly.append("semi: default chạy lúc sinh")
            elif dem["default"] == 0:
                ly.append("ON: LoRA không chạy lúc sinh")
            if ten in ("orpo_on", "orpo_off", "dpo_semi") and not any(h.get("luoi/n_cap", 0) > 0 for h in H):
                ly.append("không có cặp")
            if ten == "gpg" and not any("luoi/gpg_alpha" in h for h in H):
                ly.append("thiếu gpg_alpha")
            them = {}
            if ten == "dpo_semi":
                L = tr.semi_log
                them["semi_log"] = [dict(k=x["k"], dong_bo=x["dong_bo"], lech_truoc=round(x["lech_truoc"], 6),
                                         lech_sau=round(x["lech_sau"], 6)) for x in L]
                them["dem"] = dict(dem)
                pm = tr.accelerator.unwrap_model(tr.model)
                gen_hoc = sum(p.numel() for n_, p in pm.named_parameters() if ".gen." in n_ and p.requires_grad)
                nhip = [x["k"] for x in L if x["dong_bo"]] == [1, 3] and len(L) == 3
                lech = L[1]["lech_truoc"] > 0 and L[2]["lech_truoc"] > 0 and all(x["lech_sau"] == 0 for x in L if x["dong_bo"])
                if not (nhip and lech and dem["gen_sinh"] > 0 and dem["gen_ngoai"] == 0 and gen_hoc == 0
                        and pm.active_adapter == "default"):
                    ly.append(f"semi: nhịp {nhip} · lệch {lech} · gen lúc sinh {dem['gen_sinh']} · gen ngoài sinh "
                              f"{dem['gen_ngoai']} · gen học {gen_hoc}")
                ck = os.path.join(out, "checkpoint-2")
                if not os.path.isdir(os.path.join(ck, "gen")):
                    ly.append("điểm lưu thiếu gen/")
                # ---- pha nối tiếp: nạp tay default như GL.train rồi resume từ checkpoint-2 ----
                tr2, dem2 = dung(ten, out, 3, 10 ** 6)
                sd = load_file(os.path.join(ck, "adapter_model.safetensors"))
                kqn = set_peft_model_state_dict(tr2.model, sd, adapter_name="default")
                la = [k for k in getattr(kqn, "unexpected_keys", []) if "lora" in k]
                kiem = {}
                g2 = tr2._generate

                def gen_kiem(p, _g=g2):
                    if not kiem:
                        pm2 = tr2.accelerator.unwrap_model(tr2.model)
                        cur = get_peft_model_state_dict(pm2, adapter_name="default")
                        kiem["lech_default"] = max(float((cur[k].float() - v.float()).abs().max()) for k, v in sd.items())
                        kiem["gen_co_san"] = "gen" in pm2.peft_config
                        kiem["active"] = pm2.active_adapter
                    return _g(p)
                tr2._generate = gen_kiem
                tr2.train(resume_from_checkpoint=ck)
                L2 = tr2.semi_log
                them["resume"] = dict(kiem, khoa_la=len(la), semi_log=[dict(k=x["k"], dong_bo=x["dong_bo"]) for x in L2],
                                      buoc=tr2.state.global_step)
                if not (not la and kiem.get("lech_default", 1) == 0 and kiem.get("active") == "default"
                        and L2 and L2[0]["k"] == 3 and L2[0]["dong_bo"] and tr2.state.global_step == 3):
                    ly.append(f"resume: {them['resume']}")
            kq[ten] = dict(dat=not ly, loi=ly, loss=[round(x, 5) for x in loss], adv=[round(x, 4) for x in adv or []],
                           lora_B=[round(truoc, 4), round(sau, 4)], lora_default_luc_sinh=dem["default"],
                           giay=round(time.time() - t0, 1),
                           log={k: [round(h[k], 4) for h in H if k in h] for k in
                                ("luoi/n_cap", "luoi/orpo_z", "luoi/orpo_lc", "luoi/dpo_margin", "luoi/gpg_alpha",
                                 "luoi/sinh_tu_s1", "luoi/gen_lech_default", "luoi/n_dong_bo") if any(k in h for h in H)},
                           **them)
            print(f"[{ten}] {'ĐẠT' if not ly else '⛔ KHÔNG ĐẠT'} · {json.dumps(kq[ten], ensure_ascii=False)}", flush=True)
    finally:
        HS4["dpo_sync"] = goc_sync
    os.makedirs(goc, exist_ok=True)
    json.dump(kq, open(os.path.join(goc, "selftest_cpu_b4.json"), "w"), ensure_ascii=False, indent=1)
    hong = [k for k, v in kq.items() if not v["dat"]]
    assert not hong, f"⛔ không đạt: {hong}"
    print(f"✅ selftest CPU b4 ĐẠT {len(kq)} thuật toán:", " · ".join(kq), flush=True)


# ============================ chạy ============================
GL.ALGOS = GL.ALGOS + MOI4
GL.loi_the = loi_the
GL.lop_trainer = lop_trainer


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--algo", default="grpo")
    ap.add_argument("--orpo-lam", type=float, default=HS4["orpo_lam"])
    ap.add_argument("--dpo-sync", type=int, default=HS4["dpo_sync"])
    ap.add_argument("--gpg-std", type=int, choices=(0, 1), default=HS4["gpg_std"])
    ap.add_argument("--dpo-beta", type=float, default=B1.HS["dpo_beta"])
    ap.add_argument("--selftest-cpu", action="store_true")
    ap.add_argument("--algos", default="")
    a, rest = ap.parse_known_args()
    assert a.dpo_sync >= 1, "--dpo-sync phải ≥ 1"
    HS4.update(orpo_lam=a.orpo_lam, dpo_sync=a.dpo_sync, gpg_std=a.gpg_std)
    B1.HS["dpo_beta"] = a.dpo_beta
    if "--selftest-algo" in rest:
        return selftest_b4(a)
    if a.selftest_cpu:
        a.out = rest[rest.index("--out") + 1] if "--out" in rest else ""
        return selftest_cpu(a)
    if a.algo in MOI4:
        if "--beta" not in rest:
            rest += ["--beta", "0"]
        beta = rest[len(rest) - 1 - rest[::-1].index("--beta") + 1]
        hs = {"orpo_on": dict(orpo_lam=a.orpo_lam), "orpo_off": dict(orpo_lam=a.orpo_lam),
              "dpo_semi": dict(dpo_sync=a.dpo_sync, dpo_beta=a.dpo_beta), "gpg": dict(gpg_std=a.gpg_std)}[a.algo]
        print(f"[moi_b4] --algo {a.algo} → {a.algo} · siêu tham số {hs} · β KL {beta}", flush=True)
    sys.argv = [sys.argv[0]] + rest + ["--dpo-beta", str(a.dpo_beta), "--algo", a.algo]
    B1.main()


if __name__ == "__main__":
    main()
