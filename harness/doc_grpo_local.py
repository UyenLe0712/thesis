#!/usr/bin/env python3
"""Đọc kết quả lượt GRPO <point> mà KHÔNG cần GPU và không cần Colab.

Gộp ba ô G7a · G7b · G7d của harness/colab_grpo_point.md. Chạy trên máy nhà sau khi
tải ba thứ từ Drive về:
    ckpt/grpo_point_seed101/log_history.json
    ckpt/grpo_point_seed101/final/{adapter_model.safetensors,adapter_config.json}
    ckpt/min_desc_seed101/adapter_model.safetensors

    ~/.venvs/thesis/bin/python harness/doc_grpo_local.py --grpo <thư mục final> \
        --min <thư mục adapter MIN> --log <log_history.json>
"""
import argparse, json, os


def doc_log(p):
    h = json.load(open(p))
    ks = sorted({k for x in h for k in x})
    print(f"[G7a] bản ghi: {len(h)} · khoá bản ghi cuối: {sorted(h[-1])}")
    print(f"[G7a] mọi khoá: {ks}")
    quan_tam = [k for k in ks if "point" in k.lower() or "reward" in k.lower()]
    quan_tam += [k for k in ks if k in ("kl", "entropy", "completions/mean_length",
                                        "completions/clipped_ratio", "grad_norm", "loss")
                 and k not in quan_tam]
    for k in quan_tam:
        v = [x[k] for x in h if k in x]
        if not v:
            continue
        n = len(v) // 5 or 1
        chang = [round(sum(v[i * n:(i + 1) * n]) / len(v[i * n:(i + 1) * n]), 4) for i in range(5)]
        print(f"[G7a] {k:34s} n={len(v):4d} · 5 chặng: {chang}")


def _tep(p):
    """Nhận thư mục hoặc thẳng tệp .safetensors."""
    return p if p.endswith(".safetensors") else os.path.join(p, "adapter_model.safetensors")


def doc_adapter(grpo, mn):
    import collections
    from safetensors.torch import load_file
    A = load_file(_tep(grpo))
    B = load_file(_tep(mn))
    dA = collections.Counter(str(v.dtype) for v in A.values())
    dB = collections.Counter(str(v.dtype) for v in B.values())
    print(f"[G7b] dtype GRPO: {dict(dA)} · dtype đối chiếu: {dict(dB)}")
    if set(dA) != set(dB):
        print("[G7b] ⚠️ HAI BÊN KHÁC DTYPE — ‖Δ‖ dưới đây bị sàn bởi sai số cast (cỡ 1e-3),")
        print("[G7b]    không phân biệt được dịch chuyển thật với nhiễu định dạng số.")
        print("[G7b]    Dòng 'dịch chuyển THẬT' bên dưới đã tách sàn đó ra — đọc dòng đó.")
    norm = lambda d: sum(float(v.float().pow(2).sum()) for v in d.values()) ** 0.5
    print(f"[G7b] số tensor: {len(A)} vs MIN {len(B)}")
    print(f"[G7b] ‖GRPO‖ = {norm(A):.6f} · ‖MIN‖ = {norm(B):.6f}")

    chung = sorted(set(A) & set(B))
    print(f"[G7d] khoá chỉ có ở GRPO: {len(set(A) - set(B))} · chỉ có ở MIN: {len(set(B) - set(A))}")
    if not chung:
        print("[G7d] ⛔ không ghép được tensor nào theo tên — hai adapter khác cấu trúc")
        return
    import torch
    fl = lambda k, d: d[k].float()
    chuan = lambda f: sum(float(f(k).pow(2).sum()) for k in chung) ** 0.5
    den = chuan(lambda k: fl(k, B))
    tho = chuan(lambda k: fl(k, A) - fl(k, B)) / den
    # Sàn nhiễu: nếu hai bên khác dtype thì một phần ‖Δ‖ chỉ là sai số làm tròn của phép cast,
    # không phải trọng số dịch chuyển. Ép B qua đúng dtype của A rồi đo lại mới tách được.
    dt = next(iter(A.values())).dtype
    san = chuan(lambda k: fl(k, B).to(dt).float() - fl(k, B)) / den
    that = chuan(lambda k: fl(k, A) - fl(k, B).to(dt).float()) / den
    mx = max((float((fl(k, A) - fl(k, B).to(dt).float()).abs().max()), k) for k in chung)
    print(f"[G7d] tensor ghép được: {len(chung)}/{len(B)}")
    print(f"[G7d] ‖A-B‖/‖B‖ thô             = {tho:.6e}  (lẫn nhiễu cast nếu khác dtype)")
    print(f"[G7d] sàn nhiễu cast sang {str(dt).split('.')[-1]:9s} = {san:.6e}  (dịch chuyển 0 vẫn ra chừng này)")
    print(f"[G7d] ⭐ dịch chuyển THẬT       = {that:.6e}  ← so trên cùng lưới số")
    print(f"[G7d] lệch lớn nhất: {mx[0]:.6f} tại {mx[1]}")
    ti = that
    muc = ("dịch chuyển thật, chạy suy luận" if ti >= 1e-2 else
           "gần như không đổi — đọc r_point và kl trước khi tiêu tiền suy luận" if ti <= 1e-4 else
           "khoảng giữa, không đoán được — chạy suy luận và ghi lại độ dịch chuyển này")
    if ti < 3 * san:
        muc += " ⚠️ chưa gấp 3 lần sàn nhiễu cast, đọc dè dặt"
    print(f"[G7d] đọc theo (x19e)/runbook: {muc}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--grpo", required=True, help="thư mục final của lượt GRPO")
    ap.add_argument("--min", dest="mn", required=True,
                    help="adapter đối chiếu — thư mục hoặc thẳng tệp .safetensors. "
                         "Ưu tiên final/ref/ (cùng bf16) hơn MIN gốc (có thể fp32)")
    ap.add_argument("--log", help="log_history.json (mặc định: cạnh --grpo)")
    a = ap.parse_args()
    goc = a.grpo.rstrip("/")
    goc = os.path.dirname(goc) if goc.endswith(".safetensors") else goc
    log = a.log or os.path.join(os.path.dirname(goc), "log_history.json")
    if os.path.exists(log):
        doc_log(log)
    else:
        print(f"⚠️ không thấy {log} — bỏ qua G7a")
    print()
    doc_adapter(a.grpo, a.mn)
