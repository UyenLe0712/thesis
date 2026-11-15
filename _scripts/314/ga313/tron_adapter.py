# 295: dùng adapter LoRA mới = tổ hợp tuyến tính CHÍNH XÁC của các adapter cùng nền (S1 đã hoà).
#   ΔW_mới = Σ w_i B_i A_i * s   (s = lora_alpha / r, như nhau ở mọi adapter vào)
# Ngoại suy Exp0:   --vao ck500:1.5                         → ΔW = 1,5 * Δ_ck500
# Trung bình:       --vao ck250:0.5 --vao ck500:0.5         → ΔW = (Δ_ck250 + Δ_ck500)/2
# Trung bình + ngoại suy: --vao ck250:0.75 --vao ck500:0.75
# Ghép hạng: A_mới = [A_1; ...; A_k] (k*r x vào), B_mới = [w_1 B_1, ..., w_k B_k] (ra x k*r),
# r_mới = k*r, lora_alpha_mới = k*lora_alpha → s giữ nguyên → không xấp xỉ (khác trung bình riêng A và B).
# Chạy (Kaggle, có torch + safetensors):
#   python tron_adapter.py --vao /kaggle/input/grpo-spice-ck500/ck500:1.5 --ra /kaggle/working/expo15
import argparse, json, os, shutil

import torch
from safetensors.torch import load_file, save_file

ap = argparse.ArgumentParser()
ap.add_argument("--vao", action="append", required=True, help="thư_mục_adapter:trọng_số")
ap.add_argument("--ra", required=True)
ap.add_argument("--chuan-norm", action="store_true",
                help="soup chuẩn hoá norm: mỗi module nhân thêm β_l = TB_i||ΔW_il||_F / ||Σ w_i ΔW_il||_F (cần Σ w_i = 1)")
a = ap.parse_args()

dirs, ws = [], []
for s in a.vao:
    d, w = s.rsplit(":", 1)
    dirs.append(d)
    ws.append(float(w))
cfgs = [json.load(open(os.path.join(d, "adapter_config.json"))) for d in dirs]
c0 = cfgs[0]
for c in cfgs:
    for k in ("r", "lora_alpha", "base_model_name_or_path"):
        assert c.get(k) == c0.get(k), f"DỪNG: khác {k}: {c.get(k)} vs {c0.get(k)}"
    # 314: PEFT lưu target_modules từ một set ⇒ thứ tự đổi theo tiến trình; so theo tập hợp
    assert set(c.get("target_modules") or []) == set(c0.get("target_modules") or []), "DỪNG: khác target_modules"
    assert not c.get("use_rslora") and not c.get("use_dora"), "DỪNG: rslora/dora chưa hỗ trợ"
    assert not c.get("rank_pattern") and not c.get("alpha_pattern"), "DỪNG: rank/alpha_pattern chưa hỗ trợ"
    assert not c.get("modules_to_save"), "DỪNG: modules_to_save chưa hỗ trợ"
sds = [load_file(os.path.join(d, "adapter_model.safetensors")) for d in dirs]
keys = sorted(sds[0])
for sd in sds:
    assert sorted(sd) == keys, "DỪNG: tập khoá khác nhau"
k, r = len(dirs), c0["r"]
s = c0["lora_alpha"] / r
if a.chuan_norm:
    assert abs(sum(ws) - 1) < 1e-6, "DỪNG: --chuan-norm cần tổng trọng số = 1"
ALPHA, out = {}, {}
for key in keys:
    if "lora_A" in key:
        out[key] = torch.cat([sd[key].float() for sd in sds], 0).contiguous()
    elif "lora_B" in key:
        al = 1.0
        if a.chuan_norm:
            xa = key.replace("lora_B", "lora_A")
            dws = [sd[key].float() @ sd[xa].float() for sd in sds]
            al = (sum(d.norm() for d in dws) / k / sum(w * d for d, w in zip(dws, ws)).norm().clamp_min(1e-12)).item()
            ALPHA[key] = al
        out[key] = torch.cat([al * w * sd[key].float() for sd, w in zip(sds, ws)], 1).contiguous()
    else:
        raise SystemExit(f"DỪNG: khoá lạ {key}")
if ALPHA:
    v = sorted(ALPHA.values())
    print(f"[chuẩn norm] β_l: min {v[0]:.3f} · trung vị {v[len(v)//2]:.3f} · max {v[-1]:.3f} · {len(v)} module")

# kiểm chính xác trên mọi module: ΔW ghép == Σ α_l w_i ΔW_i (lưu fp32 → chỉ lệch làm tròn fp32)
emax = 0.0
for x in [x for x in keys if "lora_A" in x]:
    xb = x.replace("lora_A", "lora_B")
    ref = ALPHA.get(xb, 1.0) * sum(w * (sd[xb].float() @ sd[x].float()) * s for sd, w in zip(sds, ws))
    new = (out[xb] @ out[x]) * ((k * c0["lora_alpha"]) / (k * r))
    emax = max(emax, (ref - new).abs().max().item() / max(ref.abs().max().item(), 1e-12))
assert emax < 1e-5, f"DỪNG: lệch tương đối {emax}"
print(f"[kiểm] mọi module: lệch tương đối lớn nhất {emax:.2e}")

os.makedirs(a.ra, exist_ok=True)
cfg = dict(c0)
cfg["r"] = k * r
cfg["lora_alpha"] = k * c0["lora_alpha"]
json.dump(cfg, open(os.path.join(a.ra, "adapter_config.json"), "w"), indent=2)
save_file(out, os.path.join(a.ra, "adapter_model.safetensors"))
json.dump({"vao": a.vao, "r_moi": k * r, "lora_alpha_moi": k * c0["lora_alpha"], "chuan_norm": a.chuan_norm,
           "alpha_l": ALPHA},
          open(os.path.join(a.ra, "tron_meta.json"), "w"), indent=2)
print(f"[xong] {a.ra}: {k} adapter, trọng số {ws}, r {r}->{k*r}, alpha {c0['lora_alpha']}->{k*c0['lora_alpha']}")
