# -*- coding: utf-8 -*-
"""314 — Phép kiểm "GA-DPO không học là do cách train hay do cặp dữ liệu" (13/10).

Ý tưởng: lấy 200 cặp train + 200 cặp giữ riêng (tách theo câu nhắc, cân hai loại cai_thien/giu),
train nhiều epoch trên 200 cặp, đo acc/margin ở chế độ eval trên CẢ HAI tập sau mỗi mốc epoch.
  - acc trên cặp ĐÃ THẤY lên cao  ⇒ optimizer học được ⇒ lượt cũ thiếu bước.
  - acc trên cặp GIỮ RIÊNG lên theo ⇒ cặp có quy luật chung ⇒ đáng chạy lượt đủ.
  - đã-thấy cao mà giữ-riêng ~0,5 ⇒ học thuộc được nhưng cặp không có tín hiệu chung (khớp kết quả RAFT).
  - đã-thấy cũng không lên ⇒ lỗi ở khâu train (chạy lại với --lam 0 để tách phần NLL).

Khác ga_dpo.py --train ở 4 chỗ (cố ý, để đo được, không phải để ra mô hình):
  nhiều epoch · tập con 200 cặp · log-p của ref tính MỘT lần rồi dùng lại · đo eval trên hai tập.
Mọi thứ khác giữ như ga_dpo.py: nền S1 hoà + ck500 hoà fp32, LoRA mới cùng r/α/target của ck500,
autocast bf16, loss = −logσ(β·marg) + λ·NLL câu chosen, AdamW, clip 1,0, cosine có warmup 5%.

Chạy (Colab L4, trong thư mục có ga_dpo.py + grpo_spice.py):
  python kiem_hoc_dpo.py --merged M --ck500 CK --cap-file cap_colab.jsonl --out /content/kiem_dpo
Tự kiểm phần chia tập + luật đọc (CPU, không cần mô hình):
  python kiem_hoc_dpo.py --tu-kiem --out /tmp/x
"""
import os, sys, json, time, math, random, argparse, collections, statistics as st

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SEED = 101


def chia(P, n_train, n_giu, seed=SEED):
    """Tách theo câu nhắc (key), cân hai loại. Trả (train, giu)."""
    theo_loai = collections.defaultdict(list)
    for p in P:
        theo_loai[p["loai"]].append(p)
    assert set(theo_loai) == {"cai_thien", "giu"}, f"DỪNG: loại cặp lạ {sorted(theo_loai)}"
    tr, gi = [], []
    for loai in sorted(theo_loai):
        ds = sorted(theo_loai[loai], key=lambda p: p["key"])
        random.Random(seed).shuffle(ds)
        a, b = n_train // 2, n_giu // 2
        assert len(ds) >= a + b, f"DỪNG: loại {loai} chỉ có {len(ds)} cặp, cần {a + b}"
        tr += ds[:a]
        gi += ds[a:a + b]
    k_tr, k_gi = {p["key"] for p in tr}, {p["key"] for p in gi}
    assert not (k_tr & k_gi), "DỪNG: một câu nhắc nằm ở cả hai tập"
    random.Random(seed).shuffle(tr)
    return tr, gi


def tom_tat(margs, loais, lp_c, lp_r):
    """margs: log-ratio chosen − rejected (chưa nhân β), theo từng cặp."""
    out = dict(n=len(margs), acc=st.mean(m > 0 for m in margs), marg=st.mean(margs),
               lp_c=st.mean(lp_c), lp_r=st.mean(lp_r))
    for loai in ("cai_thien", "giu"):
        mm = [m for m, l in zip(margs, loais) if l == loai]
        if mm:
            out[f"acc_{loai}"] = st.mean(m > 0 for m in mm)
    return out


def doc(cuoi_train, cuoi_giu):
    """Luật đọc viết trước khi chạy. Trả một dòng kết luận."""
    if cuoi_train["acc"] < 0.65:
        return ("KHÂU TRAIN: không học thuộc được cả cặp đã thấy (acc đã-thấy < 0,65) ⇒ chạy lại với --lam 0; "
                "nếu --lam 0 cũng không lên thì có lỗi trong vòng train")
    if cuoi_train["acc"] < 0.80:
        return "CHƯA RÕ: acc đã-thấy 0,65–0,80 ⇒ gửi log, chưa kết luận"
    if cuoi_giu["acc"] >= 0.60:
        return ("CẶP CÓ TÍN HIỆU: học thuộc được và tổng quát hoá (acc giữ-riêng ≥ 0,60) ⇒ lượt 52 bước cũ thiếu bước; "
                "đáng chạy GA-DPO đủ 830 cặp nhiều epoch rồi mới chấm")
    return ("CẶP KHÔNG CÓ TÍN HIỆU CHUNG: học thuộc được (acc đã-thấy ≥ 0,80) nhưng giữ-riêng < 0,60 ⇒ vấn đề ở cách dựng cặp, "
            "không ở cách train; khớp kết quả RAFT ⇒ đóng hướng")


def chay(a):
    import torch
    import torch.nn.functional as F
    from PIL import Image
    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration, get_cosine_schedule_with_warmup
    from peft import PeftModel, LoraConfig, get_peft_model
    from ga_dpo import BASE, PIX, msg_of
    from grpo_spice import SYS, _kw

    assert torch.cuda.get_device_capability()[0] >= 8, "DỪNG: cần L4/A100 (bf16)"
    torch.manual_seed(SEED)
    random.seed(SEED)
    os.makedirs(a.out, exist_ok=True)
    P = [json.loads(l) for l in open(a.cap_file, encoding="utf-8")]
    TR, GI = chia(P, a.n_train, a.n_giu)
    print(f"[chia] {len(P)} cặp → đã-thấy {len(TR)} · giữ-riêng {len(GI)} · "
          f"cải thiện {sum(p['loai'] == 'cai_thien' for p in TR)}/{sum(p['loai'] == 'cai_thien' for p in GI)}", flush=True)
    print(f"[cấu hình] epoch {a.epoch} · lr {a.lr} · β {a.beta} · λ_nll {a.lam} · accum {a.accum} · "
          f"đo ở epoch {a.do_o}", flush=True)

    proc = AutoProcessor.from_pretrained(BASE, **PIX)
    proc.tokenizer.padding_side = "right"
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(a.merged, device_map={"": 0}, **_kw(torch.float32))
    model = PeftModel.from_pretrained(model, a.ck500).merge_and_unload()
    cfg = json.load(open(os.path.join(a.ck500, "adapter_config.json")))
    model = get_peft_model(model, LoraConfig(r=cfg["r"], lora_alpha=cfg["lora_alpha"], lora_dropout=0.0, bias="none",
                                             target_modules=cfg["target_modules"], task_type="CAUSAL_LM"))
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    for n_, p_ in model.named_parameters():
        if p_.requires_grad and "visual" in n_:
            raise SystemExit(f"DỪNG: tháp thị giác đang học: {n_}")
    end = "<|im_end|>"

    def vao(p):
        prompt = proc.apply_chat_template(msg_of(SYS, p["body"]), tokenize=False, add_generation_prompt=True)
        img = Image.open(p["image"]).convert("RGB")
        L = proc(text=[prompt], images=[img], return_tensors="pt")["input_ids"].shape[1]
        return [prompt + p["chosen"] + end, prompt + p["rejected"] + end], img, L

    def logps(texts, img, L):
        inp = proc(text=texts, images=[img] * len(texts), return_tensors="pt", padding=True).to(model.device)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            out = model(**inp)
        lg = out.logits[:, L - 1:-1].float()
        tgt = inp["input_ids"][:, L:]
        lp = torch.gather(F.log_softmax(lg, -1), 2, tgt.unsqueeze(-1)).squeeze(-1)
        mask = inp["attention_mask"][:, L:].float()
        return (lp * mask).sum(-1), mask.sum(-1)

    def b_norm():
        return math.sqrt(sum(float(q.detach().float().pow(2).sum()) for n_, q in model.named_parameters()
                             if q.requires_grad and "lora_B" in n_))

    # log-p của ref (adapter tắt) tính một lần cho cả 400 cặp; ref không đổi suốt lượt
    t0 = time.time()
    REF = {}
    model.eval()
    with torch.no_grad(), model.disable_adapter():
        for i, p in enumerate(TR + GI):
            txt, img, L = vao(p)
            r, _ = logps(txt, img, L)
            REF[p["key"]] = (r[0].item(), r[1].item())
            if (i + 1) % 100 == 0:
                print(f"  [ref] {i + 1}/{len(TR) + len(GI)} · {(time.time() - t0) / 60:.1f} phút", flush=True)

    fo = open(os.path.join(a.out, "kiem_hoc_dpo.jsonl"), "w", encoding="utf-8")

    def do(ep):
        model.eval()
        kq = {}
        with torch.no_grad():
            for ten, ds in (("da_thay", TR), ("giu_rieng", GI)):
                margs, lc, lr_ = [], [], []
                for p in ds:
                    txt, img, L = vao(p)
                    pol, nt = logps(txt, img, L)
                    rc, rr = REF[p["key"]]
                    margs.append((pol[0].item() - rc) - (pol[1].item() - rr))
                    lc.append((pol[0] / nt[0]).item())
                    lr_.append((pol[1] / nt[1]).item())
                kq[ten] = tom_tat(margs, [p["loai"] for p in ds], lc, lr_)
        kq.update(epoch=ep, b_norm=b_norm(), phut=round((time.time() - t0) / 60, 1))
        fo.write(json.dumps(kq, ensure_ascii=False) + "\n")
        fo.flush()
        d, g = kq["da_thay"], kq["giu_rieng"]
        print(f"[đo] epoch {ep} · ĐÃ-THẤY acc {d['acc']:.3f} marg {d['marg']:+.3f} lp_c {d['lp_c']:.3f} lp_r {d['lp_r']:.3f}"
              f" · GIỮ-RIÊNG acc {g['acc']:.3f} marg {g['marg']:+.3f} lp_c {g['lp_c']:.3f}"
              f" · ‖B‖ {kq['b_norm']:.4f} · {kq['phut']} phút", flush=True)
        model.train()
        return kq

    k0 = do(0)
    assert abs(k0["da_thay"]["marg"]) < 1e-2 and k0["b_norm"] == 0.0, \
        "DỪNG: ở epoch 0 policy phải trùng ref (B = 0, margin 0) — nạp sai nền hoặc adapter"

    opt = torch.optim.AdamW([q for q in model.parameters() if q.requires_grad], lr=a.lr, weight_decay=0.0)
    steps = a.epoch * math.ceil(len(TR) / a.accum)
    sch = get_cosine_schedule_with_warmup(opt, max(1, int(0.05 * steps)), steps)
    print(f"[train] {steps} bước optimizer", flush=True)
    model.train()
    k, kq = 0, k0
    for ep in range(1, a.epoch + 1):
        ds = TR[:]
        random.Random(SEED + ep).shuffle(ds)
        for i, p in enumerate(ds):
            txt, img, L = vao(p)
            pol, nt = logps(txt, img, L)
            rc, rr = REF[p["key"]]
            marg = (pol[0] - rc) - (pol[1] - rr)
            loss = -F.logsigmoid(a.beta * marg) + a.lam * (-pol[0] / nt[0])
            (loss / a.accum).backward()
            if (i + 1) % a.accum == 0 or i + 1 == len(ds):
                torch.nn.utils.clip_grad_norm_([q for q in model.parameters() if q.requires_grad], 1.0)
                opt.step(); sch.step(); opt.zero_grad(set_to_none=True)
                k += 1
                if k % 5 == 0:
                    print(f"  bước {k}/{steps} · epoch {ep} · loss {loss.item():.3f} · marg cặp cuối {marg.item():+.3f}"
                          f" · {(time.time() - t0) / 60:.1f} phút", flush=True)
        if ep in a.do_o:
            kq = do(ep)
    fo.close()
    ket = doc(kq["da_thay"], kq["giu_rieng"])
    json.dump(dict(cau_hinh=vars(a), ket_luan=ket, cuoi=kq), open(os.path.join(a.out, "ket_luan.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"[kết luận] {ket}", flush=True)


def tu_kiem(a):
    P = []
    for i in range(830):
        P.append(dict(key=f"{i}_0", loai="cai_thien" if i < 415 else "giu"))
    tr, gi = chia(P, 200, 200)
    assert len(tr) == 200 and len(gi) == 200
    assert sum(p["loai"] == "cai_thien" for p in tr) == 100 and sum(p["loai"] == "cai_thien" for p in gi) == 100
    assert chia(P, 200, 200)[0] == tr, "chia không tất định"
    s = tom_tat([0.5, -0.1, 0.2, 0.0], ["cai_thien", "cai_thien", "giu", "giu"], [-0.2] * 4, [-0.3] * 4)
    assert s["acc"] == 0.5 and s["acc_cai_thien"] == 0.5 and s["acc_giu"] == 0.5
    assert doc(dict(acc=0.5), dict(acc=0.5)).startswith("KHÂU TRAIN")
    assert doc(dict(acc=0.7), dict(acc=0.5)).startswith("CHƯA RÕ")
    assert doc(dict(acc=0.9), dict(acc=0.65)).startswith("CẶP CÓ TÍN HIỆU")
    assert doc(dict(acc=0.9), dict(acc=0.52)).startswith("CẶP KHÔNG CÓ")
    print("[tự kiểm] ĐẠT")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged"); ap.add_argument("--ck500"); ap.add_argument("--cap-file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-train", type=int, default=200); ap.add_argument("--n-giu", type=int, default=200)
    ap.add_argument("--epoch", type=int, default=5)
    ap.add_argument("--do-o", type=lambda s: [int(x) for x in s.split(",")], default=[1, 3, 5])
    ap.add_argument("--lr", type=float, default=5e-5); ap.add_argument("--accum", type=int, default=8)
    ap.add_argument("--beta", type=float, default=0.1); ap.add_argument("--lam", type=float, default=1.0)
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        tu_kiem(a)
    else:
        assert a.epoch in a.do_o, "DỪNG: phải đo ở epoch cuối"
        chay(a)
