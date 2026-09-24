# -*- coding: utf-8 -*-
"""
PATA · đo thời gian mỗi update dồn vào đâu (Kaggle T4, 0 đồng). Không train, không lưu gì.

Bối cảnh (đo 23/9 trên A100): Stage S chạy 22,8–23,9 s/update, S1 cũ (LLaMA-Factory) 10,3; chờ dữ liệu
0%, GPU bận 30–50%, và lô 16 × 1 KHÔNG nhanh hơn lô 4 × 4.
Nghi phạm: với attn "sdpa", tháp thị giác Qwen2.5-VL chạy attention TỪNG CỬA SỔ bằng vòng lặp Python
(`modeling_qwen2_5_vl.py`, nhánh "Process each chunk separately") ⇒ hàng chục nghìn lời gọi nhỏ mỗi
update, số lời gọi tăng theo số ảnh — khớp cả ba số đo.

Đo, với cùng một lô thật:
  1. thời gian tháp thị giác (no_grad)  · 2. forward toàn bộ + CE  · 3. backward
  cho hai cách tính attention thị giác:
     loop   = mặc định transformers (từng cửa sổ một lời gọi)
     block  = gom các cửa sổ liên tiếp vào MỘT lời gọi sdpa với mặt nạ khối-chéo (cửa sổ không nhìn
              sang nhau) — cùng phép toán, khác kernel
  và độ lệch số học giữa hai cách (đầu ra tháp thị giác, CE).
  4. top 15 phép CUDA tốn thời gian nhất (torch.profiler) cho cách loop.

Chạy (Kaggle, sau ô K2 của kaggle_pata_test.md):
    python harness/pata_profile.py --data-root <DR> --bs 2 --steps 3
"""
import os, sys, time, json, argparse
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pata_model as PM


def dong_bo():
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def do(fn, n):
    dong_bo(); t = time.time()
    for _ in range(n):
        out = fn()
    dong_bo()
    return (time.time() - t) / n, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=os.path.join(HERE, "dg1_cache", "train_ac"))
    ap.add_argument("--bs", type=int, default=2)
    ap.add_argument("--steps", type=int, default=3)
    ap.add_argument("--block-max", type=int, default=6144)
    a = ap.parse_args()

    proc, model, inject, d_k, cdt = PM.load_base()
    model = PM.add_lora(model)
    PM.enable_gc(model)
    model.train()
    base, vl, text = PM.parts(model)
    for n, p in model.named_parameters():
        p.requires_grad_("lora_" in n)

    recs = [json.loads(l) for l in open(os.path.join(a.data_root, "pata", "train_proper.jsonl"))]
    recs = [r for r in recs if os.path.exists(os.path.join(a.data_root, r["image"]))][: a.bs]
    ocr = {}
    for l in open(os.path.join(a.data_root, "ocr.jsonl"), encoding="utf-8"):
        o = json.loads(l); ocr[o["image"]] = o
    its = []
    for r in recs:
        r = dict(r); r["_ocr"] = ocr.get(r["image"])
        its.append(PM.make_item(proc, r, a.data_root, False, None))
    b = PM.collate(its, proc.tokenizer.pad_token_id)
    dev = text.embed_tokens.weight.device
    pv, thw = b["pixel_values"].to(dev), b["image_grid_thw"].to(dev)
    print(f"[lô] {a.bs} mẫu · chuỗi dài {b['input_ids'].shape[1]} · patch thị giác {pv.shape[0]} · "
          f"GPU {torch.cuda.get_device_name(0)}", flush=True)

    def vis():
        with torch.no_grad(), torch.autocast("cuda", dtype=cdt):
            o = vl.visual(pv, grid_thw=thw)
        return o.pooler_output if hasattr(o, "pooler_output") and o.pooler_output is not None else \
            (o[0] if isinstance(o, (tuple, list)) else getattr(o, "last_hidden_state", o))

    def fwd():
        with torch.autocast("cuda", dtype=cdt):
            ce, nt, _, _, _ = PM.forward_losses(model, None, b, need_ce=True, need_kl=False)
        return ce / nt

    def step():
        loss = fwd(); loss.backward()
        model.zero_grad(set_to_none=True)
        return float(loss.detach())

    # ⭐ 24/9: lượt K9 đầu cho thấy `block` CHẬM hơn (0,60×) và tháp thị giác chỉ 14% forward, nhưng
    # backward gấp đôi forward với 4.748 lời gọi backward attention ⇒ tháp thị giác bị kéo vào đồ thị
    # gradient bởi enable_input_require_grads. So thêm: gỡ hook đó (mặc định mới) vs giữ (hành vi cũ).
    kq = {}
    for mode in ("khong_vis_grad", "co_vis_grad"):
        PM.enable_gc(model, vision_grad=(mode == "co_vis_grad"))
        vis(); step()
        t_vis, o_vis = do(vis, a.steps)
        t_fwd, ce = do(lambda: float(fwd().detach()), a.steps)
        t_step, _ = do(step, a.steps)
        kq[mode] = {"fwd_bwd_s": t_step, "ce": ce}
        print(f"[{mode:14}] forward+CE {t_fwd:6.2f} s · backward {t_step - t_fwd:6.2f} s · cả bước "
              f"{t_step:6.2f} s · CE {ce:.6f}", flush=True)
    print(f"tăng tốc cả bước khi gỡ gradient tháp thị giác: "
          f"{kq['co_vis_grad']['fwd_bwd_s'] / kq['khong_vis_grad']['fwd_bwd_s']:.2f}×")
    # So GRADIENT LoRA trên mô hình thật, cùng lô, dropout tắt: hai chế độ phải cho cùng gradient
    for m_ in model.modules():
        if hasattr(m_, "lora_dropout"):
            for d_ in m_.lora_dropout.values():
                d_.p = 0.0
    gs = {}
    for mode in ("co_vis_grad", "khong_vis_grad"):
        PM.enable_gc(model, vision_grad=(mode == "co_vis_grad"))
        model.zero_grad(set_to_none=True)
        loss = fwd(); loss.backward()
        gs[mode] = torch.cat([p.grad.float().flatten() for n, p in model.named_parameters()
                              if "lora_" in n and p.grad is not None]).cpu()
        model.zero_grad(set_to_none=True)
    dg = (gs["co_vis_grad"] - gs["khong_vis_grad"]).abs()
    print(f"GRADIENT LoRA hai chế độ (mô hình thật, cùng lô, dropout tắt): số phần tử "
          f"{gs['co_vis_grad'].numel()} / {gs['khong_vis_grad'].numel()} · max|Δ| {float(dg.max()):.3e} · "
          f"chuẩn {float(gs['co_vis_grad'].norm()):.4f} vs {float(gs['khong_vis_grad'].norm()):.4f} · "
          f"cosine {float(torch.nn.functional.cosine_similarity(gs['co_vis_grad'], gs['khong_vis_grad'], dim=0)):.6f}")
    PM.enable_gc(model)
    PM.enable_gc(model)                          # về mặc định mới
    for mode in ("loop", "block"):
        PM.set_vision_attn(mode, a.block_max)
        vis(); step()                               # khởi động
        t_vis, o_vis = do(vis, a.steps)
        t_fwd, ce = do(lambda: float(fwd().detach()), a.steps)
        t_step, _ = do(step, a.steps)
        kq[mode] = {"vision_s": t_vis, "forward_s": t_fwd, "fwd_bwd_s": t_step,
                    "backward_s": t_step - t_fwd, "ce": ce, "vis_out": o_vis.float().cpu()}
        print(f"[{mode:5}] tháp thị giác {t_vis:6.2f} s · forward+CE {t_fwd:6.2f} s · "
              f"backward {t_step - t_fwd:6.2f} s · cả bước {t_step:6.2f} s · CE {ce:.6f}", flush=True)
    d = float((kq["loop"]["vis_out"] - kq["block"]["vis_out"]).abs().max())
    rel = d / float(kq["loop"]["vis_out"].abs().max())
    print("=" * 78)
    print(f"lệch đầu ra tháp thị giác loop↔block: max|Δ| {d:.3e} (tương đối {rel:.2e}) · "
          f"lệch CE {abs(kq['loop']['ce'] - kq['block']['ce']):.2e}")
    print(f"tỉ trọng tháp thị giác trong cả bước (loop): {kq['loop']['vision_s'] / kq['loop']['fwd_bwd_s']:.0%}")
    print(f"tăng tốc cả bước block/loop: {kq['loop']['fwd_bwd_s'] / kq['block']['fwd_bwd_s']:.2f}×")

    PM.set_vision_attn("loop")
    try:                                    # phần phụ — lỗi ở đây không làm mất các số đo phía trên
        from torch.profiler import profile, ProfilerActivity
        with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
            step(); dong_bo()
        ks = prof.key_averages()
        for key in ("device_time_total", "cuda_time_total", "cpu_time_total"):
            try:
                print(ks.table(sort_by=key, row_limit=15)); break
            except Exception:
                continue
        n_sdpa = sum(e.count for e in ks if "scaled_dot_product" in e.key or "efficient_attention" in e.key)
        print(f"số lời gọi attention trong MỘT bước (loop): {n_sdpa}")
    except Exception as e:
        print("(bỏ qua profiler:", repr(e)[:200], ")")


if __name__ == "__main__":
    main()
