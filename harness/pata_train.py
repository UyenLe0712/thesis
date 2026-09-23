# -*- coding: utf-8 -*-
"""
PATA · trainer chung cho ba chặng S → H → J (report/185 §6). Vòng lặp PyTorch tự viết,
KHÔNG qua LLaMA-Factory: Stage H/J cần loss KL và hook trong decoder mà LLaMA-Factory không có;
Stage S cũng đi qua đây để cả ba chặng dùng CÙNG một hàm dựng mẫu (không lệch template).

    --stage S   speaker CE-only. Base + LoRA mới (r8 α16 dropout .05, 7 khối ngôn ngữ),
                mọi bước chạm Train-proper, LR 1e-4, warmup .05.       (user chốt 23/9: 1 epoch)
    --stage H   localizer KL-only. Nạp adapter S (ĐÓNG BĂNG), thêm TARGET + Pq/Pv, chỉ mẫu có box,
                forward CẮT sau block 17, LR 1e-4, warmup .03, 1 epoch.
    --stage J   C1 (bridge bật) hoặc C0-Loc (--no-bridge). Nạp adapter S (MỞ) + đầu H,
                CE + 1·KL, LR 2e-5 cho LoRA+localizer, 1e-4 cho Wo+gate, warmup .03, 1 epoch.

Chung: cỡ lô hiệu dụng 16 (per-device × accum), cosine, weight decay 0, clip 1.0, QLoRA NF4,
tháp thị giác đóng băng, gradient checkpointing KHÔNG reentrant.

Chuẩn hoá loss trên CẢ lô hiệu dụng (nạp trước đủ `accum` lô con):
    CE = Σ CE token / Σ token có nhãn          (khớp cách LLaMA-Factory tính cho S1)
    KL = Σ KL mẫu  / số mẫu có box trong lô    (§2; lô không có mẫu nào có box ⇒ L_KL = 0)

Nối tiếp sau mất máy: lưu `ckpt-XXXXX/` mỗi `--save-steps` update (adapter + đầu PATA +
optimizer + scheduler + RNG). Một điểm lưu chỉ được coi là trọn khi có tệp `DONE`. Chạy lại
đúng lệnh cũ là tự chạy tiếp; thứ tự mẫu là hoán vị cố định theo `--seed` nên bỏ qua được
chính xác các lô đã học.

Ví dụ (Colab):
  python harness/pata_train.py --stage S --out /content/ckpt/pata_S --data-root <train_ac>
  python harness/pata_train.py --stage H --init-adapter <S>/final --out .../pata_H ...
  python harness/pata_train.py --stage J --init-adapter <S>/final --init-heads <H>/final --out .../pata_C1 ...
Thử vòng lặp trên CPU (mô hình tí hon, 3 update):
  ~/.venvs/thesis/bin/python harness/pata_train.py --stage S --tiny --max-updates 3 --out /tmp/x
"""
import os, sys, json, math, time, glob, random, shutil, argparse, hashlib
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pata_model as PM

BASE = "Qwen/Qwen2.5-VL-3B-Instruct"

RECIPE = {   # §6 — khoá; đổi ở đây là đổi recipe, phải ghi vào manifest
    "S": dict(lr=1e-4, lr_bridge=None, warmup=0.05, split="train_proper", with_target=False,
              need_ce=True, need_kl=False, only_box=False),
    "H": dict(lr=1e-4, lr_bridge=None, warmup=0.03, split="train_proper", with_target=True,
              need_ce=False, need_kl=True, only_box=True),
    "J": dict(lr=2e-5, lr_bridge=1e-4, warmup=0.03, split="train_proper", with_target=True,
              need_ce=True, need_kl=True, only_box=False),
}


def sha256_dir(d):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, "*"))):
        if os.path.isfile(p):
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            out[os.path.basename(p)] = h
    return out


# ─────────────────────────────────────────────────────────────── dữ liệu
class DS(torch.utils.data.Dataset):
    def __init__(self, root, split, proc, tid, with_target, only_box, only_local=False):
        self.root, self.proc, self.tid, self.wt = root, proc, tid, with_target
        p = os.path.join(root, "pata", f"{split}.jsonl")
        recs = [json.loads(l) for l in open(p, encoding="utf-8")]
        if only_box:
            recs = [r for r in recs if r["kl_ok"]]
        if only_local:          # --tiny trên WSL: chỉ một phần ảnh tập dạy có trên đĩa
            recs = [r for r in recs if os.path.exists(os.path.join(root, r["image"]))]
        self.recs = recs
        self.ocr = {}
        for l in open(os.path.join(root, "ocr.jsonl"), encoding="utf-8"):
            o = json.loads(l); self.ocr[o["image"]] = o
        print(f"[dữ liệu] {p} — {len(recs)} mẫu" + (" (chỉ mẫu có box)" if only_box else ""), flush=True)

    def __len__(self):
        return len(self.recs)

    def __getitem__(self, i):
        r = dict(self.recs[i]); r["_ocr"] = self.ocr.get(r["image"])
        return PM.make_item(self.proc, r, self.root, self.wt, self.tid)


# ─────────────────────────────────────────────────────────────── mô hình
def load_model(a, stage):
    proc, model, inject, d_k, cdt = PM.load_base(a.tiny, a.revision, a.attn)
    for p in model.parameters():
        p.requires_grad_(False)

    if stage == "S":
        torch.manual_seed(a.init_seed)
        model = PM.add_lora(model)
    else:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.init_adapter, is_trainable=(stage == "J"))
    torch.manual_seed(a.init_seed)
    pata = None
    if stage in ("H", "J"):
        pata = PM.Pata(model, proc.tokenizer, inject=inject, d_k=d_k)
        if stage == "J":
            pata.load_state_dict(torch.load(os.path.join(a.init_heads, "pata_heads.pt"), map_location="cpu"))
        pata.bridge_enabled = (stage == "J" and not a.no_bridge)
    PM.enable_gc(model)
    model.train()
    return proc, model, pata, cdt


def param_groups(model, pata, stage, rec, a):
    lora = [p for n, p in model.named_parameters() if "lora_" in n]
    if stage == "S":
        for p in lora: p.requires_grad_(True)
        return [{"params": lora, "lr": rec["lr"], "name": "lora"}]
    H = pata.heads
    # TARGET (`tvec`) là NHÓM RIÊNG: gradient của nó lớn gấp hàng trăm lần phần còn lại (đo trên
    # Kaggle 23/9: 300–2.200 so với Pq/Pv ~3) vì khởi tạo mean-vocabulary có chuẩn rất nhỏ và
    # RMSNorm đầu vào khuếch đại gradient. Cắt gradient theo TỔNG chuẩn chung thì tvec kéo mọi nhóm
    # khác về gần 0 — xem clip theo nhóm trong vòng lặp.
    tv = [H.tvec]
    loc = list(H.ln_q.parameters()) + list(H.ln_v.parameters()) + \
        list(H.pq.parameters()) + list(H.pv.parameters())
    bridge = list(H.wo.parameters()) + [H.gate]
    for p in H.parameters(): p.requires_grad_(False)
    if stage == "H":
        for p in lora: p.requires_grad_(False)
        for p in loc + tv: p.requires_grad_(True)
        return [{"params": loc, "lr": rec["lr"], "name": "localizer"},
                {"params": tv, "lr": rec["lr"], "name": "target"}]
    for p in lora + loc + tv: p.requires_grad_(True)
    g = [{"params": lora, "lr": rec["lr"], "name": "lora"},
         {"params": loc, "lr": rec["lr"], "name": "localizer"},
         {"params": tv, "lr": rec["lr"], "name": "target"}]
    if pata.bridge_enabled:
        for p in bridge: p.requires_grad_(True)
        g.append({"params": bridge, "lr": rec["lr_bridge"], "name": "bridge"})
    return g


def gnorm(ps):
    s = sum(float(p.grad.float().norm()) ** 2 for p in ps if p.grad is not None)
    return math.sqrt(s)


# ─────────────────────────────────────────────────────────────── lưu / nạp
def save_ckpt(d, model, pata, opt, sch, step, meta):
    tmp = d + ".tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    model.save_pretrained(tmp)
    if pata is not None:
        torch.save(pata.state_dict(), os.path.join(tmp, "pata_heads.pt"))
    if opt is not None:
        torch.save({"opt": opt.state_dict(), "sch": sch.state_dict(), "step": step,
                    "rng": torch.get_rng_state(),
                    "cuda_rng": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
                    "py_rng": random.getstate()}, os.path.join(tmp, "trainer_state.pt"))
    json.dump(meta, open(os.path.join(tmp, "meta.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(tmp, "DONE"), "w").write(str(step))
    shutil.rmtree(d, ignore_errors=True)
    os.replace(tmp, d)


def latest_ckpt(out):
    c = [d for d in glob.glob(os.path.join(out, "ckpt-*")) if os.path.exists(os.path.join(d, "DONE"))]
    return max(c, key=lambda d: int(d.rsplit("-", 1)[1])) if c else None


def load_trainable(model, pata, d):
    """Nạp lại trọng số ĐANG HỌC từ điểm lưu (adapter + đầu), giữ nguyên đồ thị đã dựng."""
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file
    sd = load_file(os.path.join(d, "adapter_model.safetensors"))
    set_peft_model_state_dict(model, sd)
    if pata is not None:
        pata.load_state_dict(torch.load(os.path.join(d, "pata_heads.pt"), map_location="cpu"))


# ─────────────────────────────────────────────────────────────── vòng lặp
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["S", "H", "J"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--data-root", default=os.path.join(HERE, "dg1_cache", "train_ac"))
    ap.add_argument("--init-adapter", help="thư mục adapter Stage S (H, J)")
    ap.add_argument("--init-heads", help="thư mục chứa pata_heads.pt của Stage H (J)")
    ap.add_argument("--no-bridge", action="store_true", help="C0-Loc: J với bridge tắt")
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--bs", type=int, default=4, help="cỡ lô mỗi GPU")
    ap.add_argument("--accum", type=int, default=4, help="bs × accum phải = 16")
    ap.add_argument("--lam", type=float, default=1.0, help="λpatch (§5)")
    ap.add_argument("--seed", type=int, default=101, help="thứ tự dữ liệu + dropout")
    ap.add_argument("--init-seed", type=int, default=20260923, help="khởi tạo LoRA/đầu mới")
    ap.add_argument("--save-steps", type=int, default=100)
    ap.add_argument("--keep", type=int, default=2)
    ap.add_argument("--milestones", default="800", help="điểm lưu giữ vĩnh viễn, vd 800")
    ap.add_argument("--log-steps", type=int, default=20)
    ap.add_argument("--max-updates", type=int, default=0, help=">0: dừng sớm (smoke / thử)")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--revision", default="main")
    ap.add_argument("--attn", default="sdpa")
    ap.add_argument("--tiny", action="store_true", help="mô hình tí hon, CPU — chỉ thử vòng lặp")
    ap.add_argument("--only-local", action="store_true",
                    help="chỉ dùng mẫu có ảnh trên đĩa (smoke trên Kaggle với gói ảnh nhỏ)")
    a = ap.parse_args()
    assert a.bs * a.accum == 16 or a.tiny, "cỡ lô hiệu dụng phải là 16 (§6)"
    if a.stage in ("H", "J"):
        assert a.init_adapter, "--init-adapter là bắt buộc cho H/J"
    if a.stage == "J":
        assert a.init_heads, "--init-heads là bắt buộc cho J"
    rec = RECIPE[a.stage]
    os.makedirs(a.out, exist_ok=True)
    random.seed(a.seed); torch.manual_seed(a.seed)

    proc, model, pata, cdt = load_model(a, a.stage)
    tid = pata.tid if pata else None
    ds = DS(a.data_root, rec["split"], proc, tid, rec["with_target"], rec["only_box"],
            only_local=(a.tiny or a.only_local))
    groups = param_groups(model, pata, a.stage, rec, a)
    params = [p for g in groups for p in g["params"]]
    n_tr = sum(p.numel() for p in params)
    vis_tr = [n for n, p in model.named_parameters() if p.requires_grad and "visual" in n]
    assert not vis_tr, f"tháp thị giác đang mở: {vis_tr[:3]}"
    print(f"[tham số học] {n_tr:,} · nhóm: " +
          ", ".join(f"{g['name']} lr={g['lr']:g} ({sum(p.numel() for p in g['params']):,})" for g in groups),
          flush=True)
    opt = torch.optim.AdamW([{k: v for k, v in g.items() if k != "name"} for g in groups],
                            weight_decay=0.0)
    n = len(ds)
    per_epoch = math.ceil(n / (a.bs * a.accum))
    total = math.ceil(per_epoch * a.epochs)
    if a.max_updates:
        total_run = min(total, a.max_updates)
    else:
        total_run = total
    from transformers import get_cosine_schedule_with_warmup
    sch = get_cosine_schedule_with_warmup(opt, math.ceil(rec["warmup"] * total), total)

    # hoán vị cố định theo seed, nối các epoch
    order = []
    ep = 0
    while len(order) < total * a.bs * a.accum:
        g = torch.Generator().manual_seed(a.seed * 1000 + ep)
        order += torch.randperm(n, generator=g).tolist()
        ep += 1
    step = 0
    ck = latest_ckpt(a.out)
    if ck:
        st = torch.load(os.path.join(ck, "trainer_state.pt"), map_location="cpu", weights_only=False)
        load_trainable(model, pata, ck)
        opt.load_state_dict(st["opt"]); sch.load_state_dict(st["sch"]); step = st["step"]
        torch.set_rng_state(st["rng"]); random.setstate(st["py_rng"])
        if st["cuda_rng"] is not None and torch.cuda.is_available():
            torch.cuda.set_rng_state_all(st["cuda_rng"])
        print(f"[nối tiếp] từ {ck} — update {step}/{total}", flush=True)

    meta = {"stage": a.stage, "args": vars(a), "recipe": rec, "n_samples": n, "updates_total": total,
            "per_epoch": per_epoch, "inject": pata.inject if pata else None,
            "d_k": pata.heads.d_k if pata else None, "bridge_enabled": pata.bridge_enabled if pata else None,
            "lora": {"r": 8, "alpha": 16, "dropout": 0.05, "target": PM.LORA_REGEX},
            "quant": "nf4 double-quant" if not a.tiny else "none (tiny)", "compute_dtype": str(cdt),
            "clip": "1.0 theo từng nhóm (lora · localizer · target · bridge)", "weight_decay": 0.0, "grad_ckpt": "non-reentrant",
            "transformers": __import__("transformers").__version__, "torch": torch.__version__}
    print(f"[kế hoạch] {n} mẫu · {per_epoch} update/epoch · tổng {total} · chạy tới {total_run} · "
          f"warmup {math.ceil(rec['warmup'] * total)} · λ={a.lam}", flush=True)

    from torch.utils.data import DataLoader
    start = step * a.bs * a.accum
    idx = order[start: total_run * a.bs * a.accum]
    dl = DataLoader(torch.utils.data.Subset(ds, idx), batch_size=a.bs, shuffle=False,
                    num_workers=(0 if a.tiny else a.workers),
                    collate_fn=lambda b: PM.collate(b, proc.tokenizer.pad_token_id),
                    persistent_workers=False, prefetch_factor=(None if a.tiny else 4))
    it = iter(dl)
    logf = open(os.path.join(a.out, "train_log.jsonl"), "a", encoding="utf-8")
    milestones = {int(x) for x in a.milestones.split(",") if x}
    dev = next(p for p in params).device
    use_ac = dev.type == "cuda"
    t0 = time.time(); step0 = step
    acc = {"ce": 0.0, "tok": 0, "kl": 0.0, "nkl": 0, "mass": [], "hit": [], "resid": [], "n": 0}
    lora_ps = [p for n_, p in model.named_parameters() if "lora_" in n_]
    while step < total_run:
        micro = []
        for _ in range(a.accum):
            try:
                micro.append(next(it))
            except StopIteration:
                break
        if not micro:
            break
        tot_tok = sum(int((b["labels"][:, 1:] != -100).sum()) for b in micro)
        tot_kl = sum(sum(1 for p in b["ptarget"] if p is not None) for b in micro)
        for b in micro:
            with torch.autocast("cuda", dtype=cdt, enabled=use_ac):
                ce, nt, kl, nk, ex = PM.forward_losses(
                    model, pata, b, need_ce=rec["need_ce"],
                    need_kl=rec["need_kl"], truncate=(a.stage == "H"))
            loss = 0.0
            if rec["need_ce"]:
                loss = loss + ce / max(tot_tok, 1)
            if rec["need_kl"] and tot_kl > 0:
                loss = loss + a.lam * kl / tot_kl
            loss.backward()
            acc["ce"] += float(ce.detach()); acc["tok"] += nt; acc["kl"] += float(kl.detach()); acc["nkl"] += nk
            acc["mass"] += ex["mass"]; acc["hit"] += ex["hit"]; acc["resid"] += ex["resid"]
        step += 1
        do_log = step in (1, 2, 11, 101) or step % a.log_steps == 0 or step == total_run
        gn = {}
        if do_log:
            gn["lora"] = gnorm(lora_ps)
            if pata:
                H = pata.heads
                gn.update({"wo": gnorm([H.wo.weight]), "gate": gnorm([H.gate]), "pq": gnorm([H.pq.weight]),
                           "pv": gnorm([H.pv.weight]), "tvec": gnorm([H.tvec])})
        # clip 1,0 THEO TỪNG NHÓM (lora · localizer · target · bridge), không theo tổng chung — xem
        # param_groups. LR mỗi nhóm giữ nguyên recipe §6; chỉ cách cắt gradient đổi (spec không nói).
        for g_ in groups:
            torch.nn.utils.clip_grad_norm_(g_["params"], 1.0)
        opt.step(); sch.step(); opt.zero_grad(set_to_none=True)
        if do_log:
            el = time.time() - t0
            spu = el / max(step - step0, 1)
            r = {"update": step, "total": total, "lr": [g["lr"] for g in opt.param_groups],
                 "ce": acc["ce"] / max(acc["tok"], 1) if rec["need_ce"] else None,
                 "kl": acc["kl"] / max(acc["nkl"], 1) if acc["nkl"] else None,
                 "mass_in_box": sum(acc["mass"]) / len(acc["mass"]) if acc["mass"] else None,
                 "hit_in_box": sum(acc["hit"]) / len(acc["hit"]) if acc["hit"] else None,
                 "gate_sigmoid": float(torch.sigmoid(pata.heads.gate)) if pata else None,
                 "tvec_norm": float(pata.heads.tvec.norm()) if pata else None,
                 "resid_ratio": sum(acc["resid"]) / len(acc["resid"]) if acc["resid"] else None,
                 "grad_norm": gn, "s_per_update": round(spu, 2),
                 "eta_h": round(spu * (total_run - step) / 3600, 2),
                 "vram_gb": round(torch.cuda.max_memory_allocated() / 2 ** 30, 2) if use_ac else None,
                 "time": time.strftime("%H:%M:%S")}
            logf.write(json.dumps(r) + "\n"); logf.flush()
            print(f"[{r['time']}] u{step}/{total} ce={r['ce']} kl={r['kl']} mass={r['mass_in_box']} "
                  f"gate={r['gate_sigmoid']} resid={r['resid_ratio']} {spu:.1f}s/u còn {r['eta_h']}h "
                  f"vram={r['vram_gb']} gn={ {k: round(v, 4) for k, v in gn.items()} }", flush=True)
            acc = {"ce": 0.0, "tok": 0, "kl": 0.0, "nkl": 0, "mass": [], "hit": [], "resid": [], "n": 0}
        if step % a.save_steps == 0 or step in milestones or step == total_run:
            d = os.path.join(a.out, f"ckpt-{step:05d}")
            save_ckpt(d, model, pata, opt, sch, step, meta)
            keep = sorted((c for c in glob.glob(os.path.join(a.out, "ckpt-*"))
                           if int(c.rsplit("-", 1)[1]) not in milestones and not c.endswith(".tmp")),
                          key=lambda c: int(c.rsplit("-", 1)[1]))
            for c in keep[:-a.keep]:
                shutil.rmtree(c, ignore_errors=True)
            print(f"  [lưu] {d}", flush=True)

    if step >= total:
        fin = os.path.join(a.out, "final")
        save_ckpt(fin, model, pata, None, None, step, meta)
        os.remove(os.path.join(fin, "DONE"))          # final không phải điểm nối tiếp
        h = sha256_dir(fin)
        json.dump(h, open(os.path.join(a.out, "final_sha256.json"), "w"), indent=1)
        print(f"XONG chặng {a.stage}: {step}/{total} update → {fin}", flush=True)
        for k, v in h.items():
            print(f"  {k:30} {v[:16]}…")
    else:
        print(f"Dừng ở {step}/{total} (--max-updates). Chưa có final/.", flush=True)


if __name__ == "__main__":
    main()
