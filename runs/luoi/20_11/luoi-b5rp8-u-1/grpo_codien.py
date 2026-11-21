"""Mở rộng lưới GRPO (report/323 §12): các phương pháp cổ điển chỉ đổi TRỌNG SỐ của từng câu mẫu.

Không sửa grpo_luoi.py: các lượt đã chạy vẫn tái lập đúng bằng tệp cũ. Tệp này thêm thuật toán rồi gọi main() của nó,
nên điểm xuất phát, 1.000 câu nhắc, G, lr, β, số bước và phần thưởng giữ nguyên như ck500.
  vanilla  A = r                                            (REINFORCE không mốc, Williams 1992)
  mad      A = (r - mean_nhóm) / độ lệch tuyệt đối TB        (DGPO, MathForge)
  rft      A = 1 cho câu thưởng cao nhất nhóm, còn lại 0     (online RFT, DeepSeekMath)
  cem      A = 1 cho 25% câu thưởng cao nhất nhóm, còn lại 0 (cross-entropy method)
  awr      A = exp((r - mean_nhóm) / τ), chặn ở 20           (AWR, mốc là TB nhóm thay cho mô hình giá trị)
  raml     A = G · softmax(r / τ) trong nhóm                 (kiểu RAML: mẫu lấy từ chính sách, không từ q*)
  rank     A = thứ hạng trong nhóm đưa về [-0,5; 0,5]        (fitness shaping của ES)
Nhóm có thưởng bằng nhau hết: rft · cem cho A = 0 (không có câu nào đáng học), awr · raml cho A = 1 đều, rank cho A = 0.

  python grpo_codien.py --selftest-algo
  python grpo_codien.py --train --algo awr --reward spice --bundle B --merged M --out O --resume auto
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_luoi as GL                                    # noqa: E402

MOI = ("vanilla", "mad", "rft", "cem", "awr", "raml", "rank")
TAU = 0.2                                                 # cùng cỡ độ lệch chuẩn thưởng trong nhóm ở log ck500 (~0,35)
_cu = GL.loi_the


def _top(r, k):
    import torch
    A = torch.zeros_like(r)
    A.scatter_(1, r.argsort(dim=1, descending=True, stable=True)[:, :k], 1.0)
    A[(r.max(1).values - r.min(1).values) < 1e-9] = 0.0
    return A


def loi_the(algo, r, G, b=None, r_greedy=None):
    import torch
    if algo not in MOI:
        return _cu(algo, r, G, b=b, r_greedy=r_greedy)
    r = torch.tensor(r, dtype=torch.float32).view(-1, G)
    m = r.mean(1, keepdim=True)
    if algo == "vanilla":
        A = r.clone()
    elif algo == "mad":
        A = (r - m) / ((r - m).abs().mean(1, keepdim=True) + 1e-4)
    elif algo == "rft":
        A = _top(r, 1)
    elif algo == "cem":
        A = _top(r, max(1, round(G * 0.25)))
    elif algo == "awr":
        A = torch.exp((r - m) / TAU).clamp(max=20.0)
    elif algo == "raml":
        A = G * torch.softmax(r / TAU, dim=1)
    elif algo == "rank":
        A = r.argsort(dim=1, stable=True).argsort(dim=1).float() / (G - 1) - 0.5
        A[(r.max(1).values - r.min(1).values) < 1e-9] = 0.0
    return A.flatten(), b


def selftest_codien(_):
    import torch
    G = 4
    r = [0.2, 0.4, 0.6, 0.8, 0.5, 0.5, 0.5, 0.5]
    A, _ = loi_the("vanilla", r, G)
    assert torch.allclose(A, torch.tensor(r)), A
    A, _ = loi_the("mad", r, G)
    assert torch.allclose(A[:4], torch.tensor([-1.5, -0.5, 0.5, 1.5]), atol=1e-2) and A[4:].abs().max() < 1e-6, A
    A, _ = loi_the("rft", r, G)
    assert A.tolist() == [0, 0, 0, 1, 0, 0, 0, 0], A
    A, _ = loi_the("cem", [0.2, 0.4, 0.6, 0.8, 0.1, 0.1, 0.1, 0.1], 8)
    assert A.tolist() == [0, 0, 1, 1, 0, 0, 0, 0], A
    A, _ = loi_the("awr", r, G)
    assert abs(A[3] - torch.exp(torch.tensor(0.3 / TAU))) < 1e-4 and A[4:].sub(1).abs().max() < 1e-6, A
    A, _ = loi_the("raml", r, G)
    assert abs(A[:4].sum() - G) < 1e-4 and A[3] > A[0] and A[4:].sub(1).abs().max() < 1e-5, A
    A, _ = loi_the("rank", r, G)
    assert torch.allclose(A[:4], torch.tensor([-0.5, -1 / 6, 1 / 6, 0.5]), atol=1e-5) and A[4:].abs().max() < 1e-6, A
    assert _cu is not loi_the
    A, _ = loi_the("grpo", r, G)
    assert torch.allclose(A, _cu("grpo", r, G)[0]), A
    print("✅ selftest cổ điển ĐẠT:", " · ".join(MOI))


OVERRIDE = {}                                             # khoá GRPOConfig đè lên cấu hình ck500, in ra ở dòng GRPOConfig


def _va_cau_hinh():
    """train() của grpo_luoi ghi cứng loss_type, num_iterations, scale_rewards: đè tại lúc dựng GRPOConfig."""
    import trl
    goc = trl.GRPOConfig.__init__

    def init(self, **kw):                                 # vá __init__, không tạo lớp con: Trainer phải pickle được cấu hình
        kw.update(OVERRIDE)
        goc(self, **kw)
    trl.GRPOConfig.__init__ = init


def main(argv=None):
    """Như main() của grpo_luoi, thêm cờ đổi cấu hình TRL và cho phép đúng một ô đổi hai yếu tố: SCST + CIDEr-D."""
    ap = argparse.ArgumentParser()
    for f in ("--selftest-thuong", "--selftest-algo", "--probe", "--train"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--bundle")
    ap.add_argument("--merged", default="/kaggle/working/s1_merged")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--out")
    ap.add_argument("--algo", choices=GL.ALGOS, default="grpo")
    ap.add_argument("--reward", choices=GL.REWARDS, default="spice")
    ap.add_argument("--rewards", default="")
    ap.add_argument("--keys-ck500", default="")
    ap.add_argument("--n-prompt", type=int, default=GL.GS.N_PROMPT)
    ap.add_argument("--G", type=int, default=8)
    ap.add_argument("--bs", type=int, default=4)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--beta", type=float, default=0.04)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--max-steps", type=int, default=500)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--no-q4", dest="q4", action="store_false")
    ap.add_argument("--seed", type=int, default=GL.GS.SEED)
    ap.add_argument("--gen-chunk", type=int, default=0)
    ap.add_argument("--loss-type", default=None, choices=("grpo", "dr_grpo", "dapo"))
    ap.add_argument("--scale-rewards", default=None, choices=("group", "batch", "none"))
    ap.add_argument("--mu", type=int, default=None, help="num_iterations; μ > 1 thì phép clip mới hoạt động")
    ap.add_argument("--is-level", default=None, choices=("token", "sequence"))
    ap.add_argument("--eps-high", type=float, default=None)
    a = ap.parse_args(argv)
    if a.selftest_algo:
        return GL.selftest_algo(a)
    if a.selftest_thuong:
        return GL.selftest_thuong(a)
    assert a.bundle and a.out and (a.train or a.probe), "cần --bundle, --out và --train/--probe"
    if a.algo != "grpo" and a.reward != "spice" and (a.algo, a.reward) != ("scst", "cider"):
        raise SystemExit("⛔ đổi thuật toán thì giữ thưởng spice (ngoại lệ có chủ ý: SCST + CIDEr-D)")
    for k, v in (("loss_type", a.loss_type), ("scale_rewards", a.scale_rewards), ("num_iterations", a.mu),
                 ("importance_sampling_level", a.is_level), ("epsilon_high", a.eps_high)):
        if v is not None:
            OVERRIDE[k] = v
    if OVERRIDE:
        print("[đè cấu hình]", OVERRIDE, flush=True)
    _va_cau_hinh()
    a.adapter = a.adapter or os.path.join(a.bundle, "adapter_s1_seed101")
    GL.GS.MODE.update(reward="spice", G=a.G, seed=a.seed)
    GL.train(a)


GL.ALGOS = GL.ALGOS + MOI
GL.loi_the = loi_the
GL.selftest_algo = selftest_codien

if __name__ == "__main__":
    main()
