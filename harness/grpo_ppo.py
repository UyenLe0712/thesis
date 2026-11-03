"""PPO và A2C trên cùng vòng lặp với ck500 (report/329 đợt 1): đầu giá trị nhỏ, lợi thế theo từng token.

Giữ nguyên S1, 1.000 câu nhắc, G = 8, lr, β, phần thưởng SPICE. Đổi so với ck500:
  mốc trừ   V(s_t) học được thay vì TB nhóm; lợi thế GAE(λ), γ = 1, thưởng chỉ có ở cuối câu; chuẩn hoá trên mỗi lô sinh
  μ         a2c: 1 (clip không hoạt động); ppo: --mu, mặc định 2. Muốn cùng 1.000 câu nhắc thì --max-steps = 500·μ
Đầu giá trị: MLP hai tầng trên trạng thái ẩn cuối đã tách gradient, không chung gradient với LoRA, tối ưu riêng bằng AdamW,
không huấn luyện trước. Đây là "đầu giá trị nhỏ", KHÔNG phải critic đủ cỡ (report/329 §5). β = 0,04 giữ như ck500, không có hệ số entropy.

  python grpo_ppo.py --selftest-algo
  python grpo_ppo.py --train --algo ppo --lam 1.0 --mu 2 --max-steps 1000 --bundle B --merged M --out O --resume auto
"""
import os, sys, argparse, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_codien as CD                                  # noqa: E402
GL = CD.GL

LAM = 1.0
CHUAN_HOA = True
LR_V = 3e-4
_loi_the = GL.loi_the
_lop = GL.lop_trainer


def gae(V, r, mask, lam):
    """V, mask: (B, T); r: (B,). Thưởng chỉ ở token cuối của câu, γ = 1. Trả (A, đích V) cùng cỡ (B, T)."""
    import torch
    A = torch.zeros_like(V)
    tiep, a = r.clone(), torch.zeros_like(r)
    for t in reversed(range(V.size(1))):
        m = mask[:, t].to(V.dtype)
        # token ngoài câu: giữ nguyên giá trị đang mang để token trước nó nhận đúng thưởng cuối
        d = tiep - V[:, t]
        a = m * (d + lam * a) + (1 - m) * a
        tiep = m * V[:, t] + (1 - m) * tiep
        A[:, t] = a * m
    return A, (A + V) * mask.to(V.dtype)


def loi_the(algo, r, G, b=None, r_greedy=None):
    if algo in ("ppo", "a2c"):                            # chỉ để vòng lặp cha chạy; lợi thế thật tính ở lớp con
        return _loi_the("drgrpo", r, G)
    return _loi_the(algo, r, G, b=b, r_greedy=r_greedy)


def lop_trainer():
    import torch
    B = _lop()

    class PPOTrainer(B):
        _hid = None
        _keep = None
        _hook = None
        head = None
        opt_v = None
        _resume = None
        _ev = None

        def train(self, resume_from_checkpoint=None, **kw):
            self._resume = resume_from_checkpoint
            return super().train(resume_from_checkpoint=resume_from_checkpoint, **kw)

        def _bat(self):
            if self._hook is None:
                def moc(_m, args):
                    self._hid.append(args[0][:, :-1][:, -self._keep:].detach().float())
                lm = self.accelerator.unwrap_model(self.model).get_output_embeddings()
                self._hook = lm.register_forward_pre_hook(moc)

        def _get_per_token_logps_and_entropies(self, model, input_ids, attention_mask, logits_to_keep, *a, **k):
            self._bat()
            self._keep, self._hid = logits_to_keep, []
            return super()._get_per_token_logps_and_entropies(model, input_ids, attention_mask, logits_to_keep, *a, **k)

        def _dau_gia_tri(self, H, dev):
            if self.head is None:
                with torch.random.fork_rng(devices=[]):   # không làm lệch dãy lấy mẫu so với các nhánh khác
                    self.head = torch.nn.Sequential(torch.nn.Linear(H, 512), torch.nn.ReLU(), torch.nn.Linear(512, 1)).to(dev)
                torch.nn.init.zeros_(self.head[-1].weight)
                torch.nn.init.zeros_(self.head[-1].bias)
                self.opt_v = torch.optim.AdamW(self.head.parameters(), lr=LR_V, weight_decay=0.0)
                if self._resume:
                    p = os.path.join(self._resume, "value_head.pt")
                    assert os.path.exists(p), f"DỪNG: điểm lưu thiếu đầu giá trị {p}"
                    S = torch.load(p, map_location=dev, weights_only=True)
                    self.head.load_state_dict(S["head"])
                    self.opt_v.load_state_dict(S["opt"])
                    print(f"[đầu giá trị] nạp từ {p}", flush=True)
            return self.head

        def _gia_tri(self):
            h = torch.cat(self._hid, 0)
            self._hid = []
            return h

        def _generate_and_score_completions(self, inputs):
            out = super()._generate_and_score_completions(inputs)
            if not self.model.training:
                return out
            r = torch.tensor(GL.LAST["r"], dtype=torch.float32)
            ids = torch.cat([out["prompt_ids"], out["completion_ids"]], 1)
            am = torch.cat([out["prompt_mask"], out["completion_mask"]], 1)
            kw = {k: out[k] for k in ("pixel_values", "image_grid_thw", "num_images", "pixel_attention_mask",
                                      "image_sizes", "token_type_ids", "mm_token_type_ids") if k in out}
            with torch.no_grad(), self.compute_loss_context_manager():
                self._get_per_token_logps_and_entropies(self.model, ids, am, out["completion_ids"].size(1),
                                                        self.args.per_device_train_batch_size, **kw)
            h = self._gia_tri()
            with torch.no_grad(), torch.autocast(h.device.type, enabled=False):
                V = self._dau_gia_tri(h.size(-1), h.device)(h).squeeze(-1)
            mask = out["completion_mask"]
            assert V.shape == mask.shape, (V.shape, mask.shape)
            A, dich = gae(V, r.to(V.device), mask, LAM)
            mt = self._metrics["train"]
            m = mask.bool()
            # lớp cha đã ghi hai trường này từ lợi thế tạm drgrpo: thay bằng lợi thế thật, không ghi thêm dòng thứ hai
            mt["luoi/adv_abs_mean"][-1] = float(A[m].abs().mean()) if m.any() else 0.0
            mt["luoi/frac_adv_zero"][-1] = float((A[m].abs() < 1e-6).float().mean()) if m.any() else 0.0
            if CHUAN_HOA and m.any():
                A = (A - A[m].mean()) / (A[m].std() + 1e-4) * mask.to(A.dtype)
            out["advantages"] = A.to(dtype=out["advantages"].dtype)
            out["value_targets"] = dich
            return out

        def _compute_loss(self, model, inputs):
            loss = super()._compute_loss(model, inputs)
            h, dich = self._gia_tri(), inputs["value_targets"]
            m = inputs["completion_mask"].float()
            with torch.autocast(h.device.type, enabled=False):
                v = self._dau_gia_tri(h.size(-1), h.device)(h).squeeze(-1)
                n = m.sum().clamp(min=1.0)
                l = (((v - dich) ** 2) * m).sum() / n
                self.opt_v.zero_grad(set_to_none=True)
                l.backward()
                self.opt_v.step()
            mt = self._metrics["train"]
            mt["luoi/v_loss"].append(l.item())
            bd = m.bool()
            if bd.any():
                # đo trên 64 lô gần nhất: một lô 4 mẫu có thể cùng đích, phương sai ≈ 0 làm EV ra −1e6
                if self._ev is None:
                    self._ev = collections.deque(maxlen=64)
                self._ev.append(((dich - v.detach())[bd].cpu(), dich[bd].cpu()))
                sai, d = torch.cat([x[0] for x in self._ev]), torch.cat([x[1] for x in self._ev])
                if d.numel() > 1 and d.var() > 1e-6:
                    mt["luoi/v_ev"].append(float(1 - sai.var() / d.var()))
            return loss

        def _save_checkpoint(self, model, trial):
            super()._save_checkpoint(model, trial)
            if self.head is not None:
                d = os.path.join(self.args.output_dir, f"checkpoint-{self.state.global_step}")
                torch.save(dict(head=self.head.state_dict(), opt=self.opt_v.state_dict()), os.path.join(d, "value_head.pt"))

    return PPOTrainer


def selftest_ppo(_):
    import torch
    V = torch.tensor([[0.1, 0.2, 0.3, 9.0], [0.5, 9.0, 9.0, 9.0]])
    mask = torch.tensor([[1, 1, 1, 0], [1, 0, 0, 0]])
    r = torch.tensor([1.0, 0.0])
    A, d = gae(V, r, mask, 1.0)                           # λ = 1: A_t = r - V_t
    assert torch.allclose(A[0, :3], torch.tensor([0.9, 0.8, 0.7]), atol=1e-6) and A[0, 3] == 0, A
    assert abs(A[1, 0] + 0.5) < 1e-6 and A[1, 1:].abs().max() == 0, A
    assert torch.allclose(d[0, :3], torch.ones(3), atol=1e-6) and d[0, 3] == 0, d
    A, _ = gae(V, r, mask, 0.0)                           # λ = 0: A_t = V_{t+1} - V_t, token cuối: r - V
    assert torch.allclose(A[0, :3], torch.tensor([0.1, 0.1, 0.7]), atol=1e-6), A
    A, _ = gae(V, r, mask, 0.5)
    assert abs(A[0, 2] - 0.7) < 1e-6 and abs(A[0, 1] - (0.1 + 0.5 * 0.7)) < 1e-6, A
    print("✅ selftest GAE ĐẠT")


GL.ALGOS = GL.ALGOS + ("ppo", "a2c")
GL.loi_the = loi_the
GL.lop_trainer = lop_trainer
GL.selftest_algo = selftest_ppo

if __name__ == "__main__":
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--lam", type=float, default=1.0)
    ap.add_argument("--khong-chuan-hoa", action="store_true")
    a, rest = ap.parse_known_args()
    LAM, CHUAN_HOA = a.lam, not a.khong_chuan_hoa
    print(f"[PPO] λ {LAM} · chuẩn hoá lợi thế {CHUAN_HOA} · lr V {LR_V}", flush=True)
    CD.main(rest)
