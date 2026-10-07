# -*- coding: utf-8 -*-
"""
PATA · 14 unit test bắt buộc trước train dài (report/185 §7).

Hai chế độ, cùng một bộ test:
  --tiny  (mặc định) Qwen2.5-VL TÍ HON dựng từ đúng config thật (cùng processor, cùng id
          token ảnh, cùng thứ tự raster), trọng số ngẫu nhiên, CPU FP32. Kiểm NỐI DÂY.
          Chạy trên WSL, 0 GPU, ~1–3 phút.
  --real  Qwen2.5-VL-3B thật trên GPU (Kaggle T4). Kiểm lại cùng 13 điều ở cỡ thật; test 4
          đo sai số BF16/FP16; test 12 overfit 8 mẫu thật.

⛔ Fail test 9 (KV-cache) hoặc 10 (save/reload) ⇒ CẤM train dài (§7).

Chạy:
    ~/.venvs/thesis/bin/python harness/pata_test.py                 # tí hon, CPU
    python harness/pata_test.py --real --data-root <train_ac>       # Kaggle
"""
import os, sys, json, math, time, argparse, tempfile, copy
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pata_model as PM

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"
RES = []


def check(name, cond, msg=""):
    RES.append((name, bool(cond), msg))
    print(f"  {'ĐẠT ' if cond else 'HỎNG'}  {name}  {msg}", flush=True)
    return cond


# ─────────────────────────────────────────────────────────────── dựng mô hình
def tiny_model(seed=0):
    from transformers import Qwen2_5_VLConfig, Qwen2_5_VLForConditionalGeneration
    c = Qwen2_5_VLConfig.from_pretrained(BASE)
    t = c.text_config
    t.hidden_size, t.intermediate_size = 64, 128
    t.num_hidden_layers, t.num_attention_heads, t.num_key_value_heads = 4, 4, 2
    t.layer_types = ["full_attention"] * 4
    t.max_window_layers = 4
    for k in ("rope_scaling", "rope_parameters"):
        rp = getattr(t, k, None)
        if isinstance(rp, dict) and "mrope_section" in rp:
            rp = dict(rp); rp["mrope_section"] = [2, 3, 3]; setattr(t, k, rp)
    v = c.vision_config
    v.depth, v.hidden_size, v.num_heads, v.intermediate_size = 2, 32, 2, 64
    v.out_hidden_size = 64
    v.fullatt_block_indexes = [1]
    c.hidden_size = 64
    c._attn_implementation = "eager"
    torch.manual_seed(seed)
    m = Qwen2_5_VLForConditionalGeneration(c).float()
    return m


def setup(a, seed=0, lora=False):
    proc, model, inject, d_k, cdt = PM.load_base(tiny=not a.real)
    if lora:
        torch.manual_seed(seed + 1)
        model = PM.add_lora(model)
    torch.manual_seed(seed + 2)
    pata = PM.Pata(model, proc.tokenizer, inject=inject, d_k=d_k)
    return proc, model, pata


def items(a, proc, pata, n, with_target=True, recs=None):
    root = a.data_root
    ocr = {}
    for l in open(os.path.join(root, "ocr.jsonl"), encoding="utf-8"):
        o = json.loads(l); ocr[o["image"]] = o
    if recs is None:
        recs = [json.loads(l) for l in open(os.path.join(root, "pata", "probe40.jsonl"))][:n]
    out = []
    for r in recs:
        r = dict(r); r["_ocr"] = ocr.get(r["image"])
        out.append(PM.make_item(proc, r, root, with_target, pata.tid))
    return out


def batch_of(its, proc):
    return PM.collate(its, proc.tokenizer.pad_token_id)


def logits_full(model, pata, b):
    dev = next(pata.heads.parameters()).device
    with torch.no_grad():
        o = model(input_ids=b["input_ids"].to(dev), attention_mask=b["attention_mask"].to(dev),
                  pixel_values=b["pixel_values"].to(dev), image_grid_thw=b["image_grid_thw"].to(dev),
                  use_cache=False)
    # ⛔ Chuyển ngay sang CPU: 3 mẫu × ~1.500 token × 151.936 từ vựng là ~1,4 GB FP16 mỗi bảng,
    # giữ vài bảng trên T4 16 GB là tràn (đo trên Kaggle 23/9: OOM ở test 10).
    L = o.logits.to("cpu", torch.float32)
    del o
    free()
    return L


def free():
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def tol(a):
    return 5e-2 if a.real else 1e-5


# ─────────────────────────────────────────────────────────────── 13 test
def run(a):
    dev = "cuda" if a.real else "cpu"
    print(f"== PATA unit test · {'THẬT (3B, GPU)' if a.real else 'TÍ HON (CPU)'} ==", flush=True)
    proc, model, pata = setup(a, lora=True)
    model.eval()
    its = items(a, proc, pata, 3)

    # 1 ─ số token thị giác khớp image_grid_thw sau merge
    ok = all(int((x["input_ids"] == PM.IMAGE_TOKEN_ID).sum()) == int(x["image_grid_thw"].prod()) // 4
             == x["ptarget"].numel() for x in its)
    check("1 token thị giác = t·h·w/4 = số ô đích", ok,
          f"{[int(x['image_grid_thw'].prod())//4 for x in its]}")

    # 2 ─ box ở bốn góc cho đúng ô dương
    g = (1, 20, 10)                   # ảnh resize 140×280 → lưới 5 cột × 10 hàng ô 28px
    W, H = 140, 280
    cases = {"trên-trái": ([0, 0, 5, 5], 0), "trên-phải": ([135, 0, 140, 5], 4),
             "dưới-trái": ([0, 275, 5, 280], 45), "dưới-phải": ([135, 275, 140, 280], 49)}
    ok = True
    for k, (bx, idx) in cases.items():
        p = PM.patch_target(bx, W, H, W, H, g)
        ok &= (p.numel() == 50 and int(p.argmax()) == idx and int((p > 0).sum()) == 1)
    p = PM.patch_target([20, 20, 40, 40], W, H, W, H, g)       # vắt qua 4 ô
    ok &= sorted((p > 0).nonzero().flatten().tolist()) == [0, 1, 5, 6]
    check("2 box bốn góc + box vắt ô → đúng ô dương, raster", ok)

    # 3 ─ đổi hậu tố vàng, giữ tiền tố ⇒ α của TARGET không đổi
    r0 = [json.loads(l) for l in open(os.path.join(a.data_root, "pata", "probe40.jsonl"))][0]
    r1 = dict(r0); r1["target_instruction"] = "Completely different words here please."
    i0, i1 = items(a, proc, pata, 0, recs=[r0])[0], items(a, proc, pata, 0, recs=[r1])[0]
    la = []
    for x in (i0, i1):
        logits_full(model, pata, batch_of([x], proc))
        la.append(pata.last[0]["logalpha"].detach().float().cpu())
    check("3 đổi hậu tố vàng không đổi α(TARGET)", torch.allclose(la[0], la[1], atol=tol(a)),
          f"max|Δ|={float((la[0]-la[1]).abs().max()):.2e}")

    # 4 ─ Wo=0 ⇒ logits bật bridge = tắt bridge
    b = batch_of(its, proc)
    pata.bridge_enabled = True
    L_on = logits_full(model, pata, b)
    pata.bridge_enabled = False
    L_off = logits_full(model, pata, b)
    pata.bridge_enabled = True
    d = float((L_on - L_off).abs().max())
    check("4 Wo=0: logits bridge bật = tắt", d <= (1e-2 if a.real else 1e-6), f"max|Δ|={d:.2e}")

    # 5 ─ bật residual chỉ đổi TARGET/hậu tố, không đổi tiền tố
    with torch.no_grad():
        pata.heads.wo.weight.normal_(0, 0.5 if not a.real else 0.02)
    L_on = logits_full(model, pata, b)
    tpos = [rec["tpos"] for rec in pata.last]
    pata.bridge_enabled = False
    L_off = logits_full(model, pata, b)
    pata.bridge_enabled = True
    pre = max(float((L_on[i, :t] - L_off[i, :t]).abs().max()) for i, t in enumerate(tpos))
    post = min(float((L_on[i, t:] - L_off[i, t:]).abs().max()) for i, t in enumerate(tpos))
    check("5 Wo≠0: tiền tố không đổi, TARGET/hậu tố đổi", pre <= tol(a) and post > 10 * max(pre, 1e-7),
          f"tiền tố {pre:.2e} · hậu tố {post:.2e}")

    # 14 ─ ép α (swap §8 điều 5): đổi logits sau TARGET, KHÔNG đổi tiền tố; ép đúng α của chính
    #      localizer thì phải trùng tuyệt đối với không ép (kiểm đường ép không lệch hàng/thứ tự ô)
    L_free = logits_full(model, pata, b)
    la_ = [rec["logalpha"].exp().detach() for rec in pata.last]
    pata.alpha_override = [PM.patch_target([0, 0, r0["w"] // 3, r0["h"] // 3], r0["w"], r0["h"],
                                           r0["w"], r0["h"], x["image_grid_thw"]) for x in its]
    L_sw = logits_full(model, pata, b)
    pata.alpha_override = la_
    L_same = logits_full(model, pata, b)
    pata.alpha_override = None
    pre = max(float((L_sw[i, :t] - L_free[i, :t]).abs().max()) for i, t in enumerate(tpos))
    post = min(float((L_sw[i, t:] - L_free[i, t:]).abs().max()) for i, t in enumerate(tpos))
    same = float((L_same - L_free).abs().max())
    check("14 ép α: tiền tố không đổi, hậu tố đổi; ép đúng α tự sinh = không ép",
          pre <= tol(a) and post > 10 * max(pre, 1e-7) and same <= tol(a),
          f"tiền tố {pre:.2e} · hậu tố {post:.2e} · ép α tự sinh {same:.2e}")

    # 9 ─ teacher-forced full pass = sinh tăng dần có KV-cache (dùng Wo≠0 hiện tại)
    x = its[0]
    ids = x["input_ids"]
    tp = int((ids == pata.tid).nonzero()[0])
    pre_ids = ids[: tp + 1].unsqueeze(0).to(dev)
    with torch.no_grad():
        g_out = model.generate(input_ids=pre_ids, attention_mask=torch.ones_like(pre_ids),
                               pixel_values=x["pixel_values"].to(dev),
                               image_grid_thw=x["image_grid_thw"].unsqueeze(0).to(dev),
                               max_new_tokens=6, min_new_tokens=6, do_sample=False, use_cache=True,
                               output_logits=True, return_dict_in_generate=True)
    seq = g_out.sequences
    gen_logits = torch.stack([l[0].float().cpu() for l in g_out.logits])     # (k, V), CPU
    with torch.no_grad():
        full = model(input_ids=seq, attention_mask=torch.ones_like(seq),
                     pixel_values=x["pixel_values"].to(dev),
                     image_grid_thw=x["image_grid_thw"].unsqueeze(0).to(dev), use_cache=False).logits
    ref = full[0, tp: tp + gen_logits.shape[0]].float().cpu()
    del full; free()
    d = float((ref - gen_logits).abs().max())
    check("9 teacher-forced = KV-cache tăng dần (bridge bật, Wo≠0)", d <= (0.1 if a.real else 1e-4),
          f"max|Δ|={d:.2e} trên {gen_logits.shape[0]} bước")

    # 10 ─ save → reload giữ logits, α và câu
    tmp = tempfile.mkdtemp()
    model.save_pretrained(tmp)
    torch.save(pata.state_dict(), os.path.join(tmp, "pata_heads.pt"))
    L_a = logits_full(model, pata, b); la_a = pata.last[0]["logalpha"].float().cpu()
    with torch.no_grad():
        s_a = model.generate(input_ids=pre_ids, attention_mask=torch.ones_like(pre_ids),
                             pixel_values=x["pixel_values"].to(dev),
                             image_grid_thw=x["image_grid_thw"].unsqueeze(0).to(dev),
                             max_new_tokens=8, do_sample=False).tolist()
    from peft import PeftModel
    free()
    proc2, base2, pata2 = setup(a, lora=False)
    pata2.remove()                              # gắn lại hook SAU khi bọc PEFT
    m2 = PeftModel.from_pretrained(base2, tmp)
    m2.eval()
    pata2 = PM.Pata(m2, proc2.tokenizer, inject=pata.inject, d_k=pata.heads.d_k)
    pata2.load_state_dict(torch.load(os.path.join(tmp, "pata_heads.pt")))
    L_b = logits_full(m2, pata2, b); la_b = pata2.last[0]["logalpha"].float().cpu()
    with torch.no_grad():
        s_b = m2.generate(input_ids=pre_ids, attention_mask=torch.ones_like(pre_ids),
                          pixel_values=x["pixel_values"].to(dev),
                          image_grid_thw=x["image_grid_thw"].unsqueeze(0).to(dev),
                          max_new_tokens=8, do_sample=False).tolist()
    d1 = float((L_a - L_b).abs().max()); d2 = float((la_a - la_b).abs().max())
    check("10 save→reload: logits, α, câu giữ nguyên", d1 <= tol(a) and d2 <= tol(a) and s_a == s_b,
          f"logits {d1:.2e} · α {d2:.2e} · câu {'trùng' if s_a == s_b else 'KHÁC'}")
    pata2.remove(); del m2, base2, L_a, L_b, L_on, L_off; free()

    # 11 ─ box nhỏ / sát biên không tạo NaN
    gthw = its[0]["image_grid_thw"]
    w, h = r0["w"], r0["h"]
    ok = True
    for bx in ([0, 0, 1, 1], [w - 1, h - 1, w, h], [0, h // 2, 2, h // 2 + 1], [w // 2, 0, w // 2 + 1, 3],
               [10, 10, 10, 10]):
        p = PM.patch_target(bx, w, h, w, h, gthw)
        ok &= bool(torch.isfinite(p).all()) and abs(float(p.sum()) - 1) < 1e-6
        kl = PM.kl_target_alpha(p, torch.log_softmax(torch.randn(p.numel()), -1))
        ok &= bool(torch.isfinite(kl))
    check("11 box nhỏ/sát biên/suy biến: đích hợp lệ, KL hữu hạn", ok)

    # 13 ─ strip TARGET đúng định dạng evaluator
    from infer_branch import strip_desc
    enc = proc.tokenizer(PM.TARGET + "Tap the share icon.", add_special_tokens=False).input_ids
    txt = proc.tokenizer.decode(enc, skip_special_tokens=True)
    ok = enc[0] == pata.tid and txt == "Tap the share icon." and strip_desc(txt) == txt
    check("13 <TARGET> là MỘT token, decode bỏ được, strip_desc giữ nguyên câu", ok, repr(txt))

    # 6, 7, 8 ─ gradient (bật gradient checkpointing KHÔNG reentrant như lúc train thật)
    with torch.no_grad():
        pata.heads.wo.weight.zero_()
    model.train()
    PM.enable_gc(model)
    vis_before = {n: p.detach().clone() for n, p in model.named_parameters() if "visual" in n}
    base_, _, _ = PM.parts(model)
    for n, p in model.named_parameters():
        p.requires_grad_("lora_" in n)
    params = [p for p in model.parameters() if p.requires_grad] + list(pata.heads.parameters())
    opt = torch.optim.AdamW(params, lr=1e-3, weight_decay=0.0)
    ce, nt, kl, nk, _ = PM.forward_losses(model, pata, b)
    loss = ce / max(nt, 1) + kl / max(nk, 1)
    loss.backward()
    gn = lambda p: 0.0 if p.grad is None else float(p.grad.norm())
    H = pata.heads
    lora_g = sum(gn(p) for n, p in model.named_parameters() if "lora_" in n)
    ok6 = gn(H.wo.weight) > 0 and gn(H.pq.weight) > 0 and gn(H.pv.weight) > 0 and gn(H.tvec) > 0 and lora_g > 0
    check("6 backward đầu: Wo, Pq, Pv, TARGET, LoRA có gradient; gate = 0 vì Wo=0",
          ok6 and gn(H.gate) == 0.0,
          f"Wo {gn(H.wo.weight):.1e} Pq {gn(H.pq.weight):.1e} T {gn(H.tvec):.1e} LoRA {lora_g:.1e} gate {gn(H.gate):.1e}")
    opt.step(); opt.zero_grad()
    ce, nt, kl, nk, _ = PM.forward_losses(model, pata, b)
    (ce / max(nt, 1) + kl / max(nk, 1)).backward()
    check("7 sau một optimizer step: gate có gradient", gn(H.gate) > 0, f"gate {gn(H.gate):.2e}")
    opt.step(); opt.zero_grad()
    vg = [p.grad for n, p in model.named_parameters() if "visual" in n and p.grad is not None]
    same = all(torch.equal(p, vis_before[n]) for n, p in model.named_parameters() if "visual" in n)
    check("8 tháp thị giác: không gradient, trọng số không đổi", not vg and same)

    # 12 ─ overfit 8 mẫu: CE/KL giảm, mass trong box tăng
    its8 = items(a, proc, pata, 8)
    b8 = batch_of(its8, proc) if not a.real else None
    hist = []
    steps = 40 if not a.real else 30
    opt = torch.optim.AdamW(params, lr=(3e-3 if not a.real else 2e-4), weight_decay=0.0)
    for s in range(steps):
        if a.real:
            tot = [0, 0, 0, 0, []]
            for j in range(0, 8, 2):
                bb = batch_of(its8[j:j + 2], proc)
                ce, nt, kl, nk, ex = PM.forward_losses(model, pata, bb)
                ((ce / 8 / 20) + kl / 8).backward()
                tot[0] += float(ce); tot[1] += nt; tot[2] += float(kl); tot[3] += nk; tot[4] += ex["mass"]
            hist.append((tot[0] / tot[1], tot[2] / tot[3], sum(tot[4]) / len(tot[4])))
        else:
            ce, nt, kl, nk, ex = PM.forward_losses(model, pata, b8)
            (ce / nt + kl / nk).backward()
            hist.append((float(ce) / nt, float(kl) / nk, sum(ex["mass"]) / len(ex["mass"])))
        opt.step(); opt.zero_grad()
    f5 = [sum(h[i] for h in hist[:5]) / 5 for i in range(3)]
    l5 = [sum(h[i] for h in hist[-5:]) / 5 for i in range(3)]
    check("12 overfit 8 mẫu: CE↓ KL↓ mass↑", l5[0] < f5[0] and l5[1] < f5[1] and l5[2] > f5[2],
          f"CE {f5[0]:.3f}→{l5[0]:.3f} · KL {f5[1]:.3f}→{l5[1]:.3f} · mass {f5[2]:.3f}→{l5[2]:.3f}")

    print("=" * 70)
    n_ok = sum(1 for _, ok, _ in RES if ok)
    print(f"{n_ok}/{len(RES)} ĐẠT")
    bad = [n for n, ok, _ in RES if not ok]
    if bad:
        print("HỎNG:", "; ".join(bad))
    if any(n.startswith(("9 ", "10 ")) for n in bad):
        print("⛔ Fail KV-cache hoặc save/reload ⇒ CẤM train dài (report/185 §7).")
    return 0 if not bad else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--real", action="store_true")
    ap.add_argument("--data-root", default=os.path.join(HERE, "dg1_cache", "train_ac"))
    a = ap.parse_args()
    t0 = time.time()
    rc = run(a)
    print(f"({time.time() - t0:.0f} s)")
    sys.exit(rc)
