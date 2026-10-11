# -*- coding: utf-8 -*-
"""308 - ghép câu CW-RA theo ngưỡng τ (CPU, vài giây). Không sinh lại, không nhìn câu chuẩn.

Bước có p_copy >= τ → câu mẫu thứ copy_idx (nguyên văn trong khối); còn lại → câu `write`.
τ = 1.01 nghĩa là không bao giờ chép (đo độ trôi của nhánh viết so ck500).

python cw_ghep.py --cw cw_val.jsonl --ra ex_val_k4.jsonl --out-dir O --ten val
# O/pred_cw_t{τ}_val.jsonl cho mọi τ trong lưới; rồi chấm bằng ra_score.py (--pred cw_t0.5=...).
python cw_ghep.py --tu-kiem
"""
import os, json, argparse

LUOI = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.01)


def ghep(C, E, tau):
    out, chep = {}, 0
    for k, c in C.items():
        if c["copy_idx"] and c["p_copy"] >= tau:
            out[k] = E[k][c["copy_idx"] - 1]["sent"]
            chep += 1
        else:
            out[k] = c["write"]
    return out, chep


def tu_kiem():
    E = {(1, 0): [{"sent": "A"}, {"sent": "B"}], (1, 1): [{"sent": "C"}]}
    C = {(1, 0): dict(p_copy=0.7, copy_idx=2, write="w0"), (1, 1): dict(p_copy=0.2, copy_idx=1, write="w1")}
    assert ghep(C, E, 0.5) == ({(1, 0): "B", (1, 1): "w1"}, 1)
    assert ghep(C, E, 1.01) == ({(1, 0): "w0", (1, 1): "w1"}, 0)
    print("[tự kiểm] ĐẠT")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cw")
    ap.add_argument("--ra")
    ap.add_argument("--out-dir")
    ap.add_argument("--ten", default="val")
    ap.add_argument("--tau", type=float, default=None, help="chỉ ghép một τ (dùng cho test sau khi đã chốt τ trên val)")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        return tu_kiem()
    C = {(d["episode_id"], d["step_id"]): d for d in map(json.loads, open(a.cw, encoding="utf-8"))}
    E = {(d["episode_id"], d["step_id"]): d["exemplars"] for d in map(json.loads, open(a.ra, encoding="utf-8"))}
    assert set(C) == set(E), "⛔ thiếu khối ví dụ"
    os.makedirs(a.out_dir, exist_ok=True)
    for tau in ([a.tau] if a.tau is not None else LUOI):
        P, chep = ghep(C, E, tau)
        p = os.path.join(a.out_dir, f"pred_cw_t{tau}_{a.ten}.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            for k, s in P.items():
                f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "pred": s}, ensure_ascii=False) + "\n")
        print(f"τ={tau}: chép {chep}/{len(P)} ({100 * chep / len(P):.1f}%) → {p}")


if __name__ == "__main__":
    main()
