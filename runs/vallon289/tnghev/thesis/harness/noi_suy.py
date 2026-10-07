# -*- coding: utf-8 -*-
"""Nội suy hai adapter LoRA trong KHÔNG GIAN TRỌNG SỐ — chính xác tới sai số máy ở mọi alpha.

    ~/.venvs/thesis/bin/python harness/noi_suy.py        # ra runs/noisuy/a0.00 … a1.00

Thi hành V2 của `report/151` §5.3bis.

⛔⛔ Vì sao KHÔNG bình quân riêng lora_A rồi riêng lora_B: LoRA có ΔW = scaling·B·A, là TÍCH chứ
   không phải tổng, nên [(1−α)B₁+αB₂][(1−α)A₁+αA₂] ≠ (1−α)B₁A₁ + αB₂A₂ — vế trái sinh hai số
   hạng chéo vô nghĩa, và hai đầu mút α=0 với α=1 vẫn đúng tuyệt đối nên phép kiểm đầu mút
   KHÔNG bắt được sai số ở giữa.
   ⚠️ Số đo thật trên CẶP NÀY: sai số của cách trộn thẳng chỉ 0,0163% tại α=0,5, không phải 65%
   như `151` §5.3bis ghi. Lý do: GRPO học tiếp từ MIN nên chỉ dịch chuyển A 1,39% và B 6,87%,
   mà số hạng chéo tỉ lệ với tích hai độ lệch ấy. Con số 65% chỉ đúng cho hai adapter huấn luyện
   độc lập. Vẫn dùng ghép nối vì nó đúng tới sai số máy ở mọi α và không tốn thêm gì.

⭐ Cách đúng — GHÉP NỐI theo hạng:
       B' = [(1−α)·B_MIN | α·B_GRPO]      (out, 2r)
       A' = [A_MIN ; A_GRPO]              (2r, in)
   ⇒ B'A' = (1−α)·B_MIN·A_MIN + α·B_GRPO·A_GRPO, đúng bằng tổ hợp cần dựng.
   Phải nhân đôi CẢ r LẪN lora_alpha để giữ nguyên scaling = lora_alpha / r.

⚠️ r đọc từ adapter_config.json chứ không viết số cứng: bộ adapter của dự án này có r = 8,
   trong khi `151` §5.3bis ghi 16. Số cứng sẽ làm sai scaling gấp đôi mà không có gì báo.
"""
import json, os, torch
from safetensors.torch import load_file, save_file

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DIR_MIN = os.path.join(ROOT, "runs", "grpo_point", "adapter_ref_min")
DIR_GRPO = os.path.join(ROOT, "runs", "grpo_point", "adapter_grpo_point_seed101")
MUC = (0.0, 0.25, 0.5, 0.75, 1.0)


def noi_suy(dir_min, dir_grpo, alpha, dir_ra):
    M = load_file(os.path.join(dir_min, "adapter_model.safetensors"))
    G = load_file(os.path.join(dir_grpo, "adapter_model.safetensors"))
    assert set(M) == set(G), f"hai adapter khác tập module: {set(M) ^ set(G)}"

    ra = {}
    for k in M:
        a, b = M[k].float(), G[k].float()     # ⛔ ép fp32: MIN là float32, GRPO là bfloat16
        assert a.shape == b.shape, f"lệch shape ở {k}"
        if ".lora_A." in k:
            ra[k] = torch.cat([a, b], dim=0)                     # (2r, in)
        elif ".lora_B." in k:
            ra[k] = torch.cat([(1 - alpha) * a, alpha * b], dim=1)   # (out, 2r)
        else:
            raise KeyError(f"khoá lạ, không phải lora_A/lora_B: {k}")

    os.makedirs(dir_ra, exist_ok=True)
    save_file(ra, os.path.join(dir_ra, "adapter_model.safetensors"))

    cfg = json.load(open(os.path.join(dir_min, "adapter_config.json")))
    r0, al0 = cfg["r"], cfg["lora_alpha"]
    cfg["r"] = r0 * 2
    cfg["lora_alpha"] = al0 * 2               # ⛔ PHẢI đổi cả hai, giữ scaling
    for ten in ("rank_pattern", "alpha_pattern"):
        if cfg.get(ten):                      # khác rỗng thì phải nhân đôi từng giá trị
            cfg[ten] = {k: v * 2 for k, v in cfg[ten].items()}
    json.dump(cfg, open(os.path.join(dir_ra, "adapter_config.json"), "w"), indent=2)
    return r0, al0, len(ra)


if __name__ == "__main__":
    for al in MUC:
        d = os.path.join(ROOT, "runs", "noisuy", f"a{al:.2f}")
        r0, al0, n = noi_suy(DIR_MIN, DIR_GRPO, al, d)
        print(f"  a{al:.2f}: {n} tensor · r {r0}->{r0*2} · lora_alpha {al0}->{al0*2}"
              f" · scaling giữ nguyên {al0/r0:g}", flush=True)
    print("\n⭐ Phép kiểm bắt buộc làm TRÊN CÂU, không trên điểm (MIN và GRPO chênh 0,02 pp):")
    print("   α=1 phải trùng từng ký tự runs/grpo_point/preds_grpo_point_seed101.jsonl")
    print("   α=0 phải trùng từng ký tự runs/preds_min_desc_seed101.jsonl")
