#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Điểm chuỗi chuẩn hoá độ dài cho từng ứng viên + `none` — thi hành hợp đồng
`report/134` §6.1, đã đăng ký trước ở `report/106` mục (x16d).

VÌ SAO CÓ TỆP NÀY
-----------------
Lượt suy luận thường chỉ cho ra MỘT quyết định cứng: mô hình phát `<sel>none</sel>`
hoặc phát tên một ứng viên. Từ một quyết định cứng thì không dựng được đường
risk-coverage và không chỉnh được ngưỡng bỏ cuộc. Tệp pred của cổng G6 cũng không có
trường `conf` nào dùng được cho việc này.

Ở đây mỗi phương án được TÍNH ĐIỂM riêng bằng teacher-forcing, nên có một điểm số so
sánh được giữa mọi ứng viên và `none`:

    s(c|x) = ( Σ_t log p(token_t | x, token_<t) ) / số_token(span_c)

`c* = argmax s` trên các ứng viên THẬT; `m = s(c*) − s(none)`; phát `c*` khi `m > τ`.

⛔ BA CHỖ DỄ SAI, ĐÃ CHẶN TRONG MÃ
  ① Span phải là bản CHÉP NGUYÊN từ artifact, render bằng chính `build_sel_data.sel_str`
     (vốn gọi lại `build_candidates.block_str`). Tự format lại tên hay toạ độ là dựng
     một chuỗi chưa từng có lúc dạy, và không có gì báo lỗi.
  ② Chỉ cộng log-prob của token THUỘC SPAN. Cộng cả câu nhắc thì điểm bị chi phối bởi
     phần giống hệt nhau ở mọi phương án; cộng cả câu hướng dẫn thì đang đo một đại
     lượng khác.
  ③ Điểm quyết định là điểm CHUỖI ĐẦY ĐỦ. Xác suất token đầu không đủ để gọi tên thủ
     tục của Devlin et al. — xem (x16d).

⛔ Tệp này KHÔNG quét τ và KHÔNG đọc kết quả. Nó chỉ sinh điểm. Quét τ là bước riêng,
   chỉ chạy trên lát dev, và phải chạy TRƯỚC khi nhìn exec đối chứng hoặc phần 3.062.
"""

import os, sys, json, time, argparse, hashlib, ast

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build_branch_data import prompt_body, SYS          # cùng một nguồn chữ với lúc dạy
from build_sel_data import gold_candidate, sel_str      # bản DUY NHẤT, không viết lại
from infer_branch import TEST, BASE, dtype_kw           # cùng cách nạp mô hình


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def span_of(c):
    """Chuỗi span của một ứng viên, và của `none`."""
    return f"<sel>{sel_str(c)}</sel>" if c is not None else "<sel>none</sel>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--cands", required=True,
                    help="candidates.jsonl ĐÃ PIN của tập kiểm. Bắt buộc: mọi phương án "
                         "phải chép nguyên từ đúng tệp mà lượt train và lượt G6 đã dùng.")
    ap.add_argument("--only", default="",
                    help="jsonl liệt kê bước cần chấm (đọc episode_id/step_id). Lát dev "
                         "1.400 thì trỏ vào chính tệp pred của G6.")
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--probe", type=int, default=0,
                    help="chạy N bước rồi dừng và in thống kê — dùng 50 trước lượt dài.")
    ap.add_argument("--span-batch", type=int, default=8,
                    help="số span tính cùng một lượt truyền ở ĐƯỜNG CHẬM. Giảm nếu hết bộ nhớ.")
    ap.add_argument("--dtype", default="", choices=["", "float32", "bfloat16", "float16"],
                    help="ĐỂ TRỐNG cho mọi lượt chấm thật — khi đó dùng đúng pick_dtype() "
                         "của infer_branch, tức cùng kiểu số với các lượt đã chấm. Chỉ đặt "
                         "tay khi chạy PROBE trên máy không GPU: pick_dtype() thấy không có "
                         "CUDA thì trả float32, mà 3B ở float32 là ~12,4 GB trọng số, tràn "
                         "RAM máy 12 GB. Đặt bfloat16 thì vừa, nhưng CHẬM và ⛔ điểm số "
                         "KHÔNG so được với lượt chạy trên GPU — chỉ dùng để kiểm mã.")
    ap.add_argument("--cache-prompt", action="store_true",
                    help="ĐƯỜNG NHANH: mã hoá câu nhắc (gồm ảnh ~1.272 token) đúng MỘT lần "
                         "cho mỗi bước rồi chạy từng span trên bộ nhớ đệm đó. Rẻ hơn khoảng "
                         "5-7 lần vì đường chậm mã hoá lại cả ảnh cho từng lô span. "
                         "Bật cờ này thì 3 bước đầu BẮT BUỘC tính bằng CẢ HAI đường và so; "
                         "lệch quá 1e-3 là dừng hẳn, không tự ý chạy tiếp.")
    args = ap.parse_args()

    import torch
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from PIL import Image

    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")]
    ocr = {}
    with open(os.path.join(TEST, "ocr.jsonl"), encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            ocr[o["image"]] = o
    cands = {}
    with open(args.cands, encoding="utf-8") as f:
        for line in f:
            c = json.loads(line)
            cands[c["image"]] = c["cands"]
    # nhãn vàng chỉ dùng để GHI KÈM (`gold_in_menu`), không tham gia tính điểm. Đọc theo
    # đúng luật của build_sel_data.py: descriptors.jsonl khoá (episode_id, step_id).
    desc = {}
    dp = os.path.join(TEST, "descriptors.jsonl")
    if os.path.exists(dp):
        with open(dp, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                desc[(str(d["episode_id"]), str(d["step_id"]))] = d
    print(f"nhãn vàng: {len(desc)} khai báo")

    if args.only:
        gi = []
        for line in open(args.only, encoding="utf-8"):
            o = json.loads(line)
            gi.append((str(o["episode_id"]), str(o["step_id"])))
        gs = set(gi)
        truoc = len(recs)
        recs = [r for r in recs if (str(r["episode_id"]), str(r["step_id"])) in gs]
        print(f"--only: {truoc} -> {len(recs)} bước (danh sách có {len(gs)} khoá)")
        assert len(recs) == len(gs), (
            f"DỪNG: danh sách có {len(gs)} khoá nhưng chỉ khớp {len(recs)} bản ghi — "
            f"nghi lệch kiểu khoá int/str hoặc lệch tệp test.")
    if args.limit:
        recs = recs[:args.limit]

    # ── FAIL-CLOSED, cùng luật với infer_branch.py (report/134 §11) ────────────────
    thieu = [r["image"] for r in recs if r["image"] not in cands]
    if thieu:
        sys.exit(f"DỪNG: {len(thieu)}/{len(recs)} bước không có khoá trong {args.cands} "
                 f"(ví dụ {thieu[:3]}).")
    print(f"khối ứng viên: phủ {len(recs)}/{len(recs)} bước — fail-closed ĐẠT")

    sig = f"seqscore:{os.path.basename(str(args.adapter).rstrip('/'))}"
    xong = set()
    if os.path.exists(args.out):
        sach, khac = [], set()
        for line in open(args.out, encoding="utf-8"):
            try:
                o = json.loads(line)
            except Exception:
                continue          # dòng ghi dở lúc mất máy — bỏ hẳn, đừng để giữa chừng
            xong.add((str(o["episode_id"]), str(o["step_id"])))
            sach.append(line)
            if o.get("run") and o["run"] != sig:
                khac.add(o["run"])
        open(args.out, "w", encoding="utf-8").writelines(sach)
        if khac:
            sys.exit(f"⛔ {args.out} là của lượt chạy KHÁC: {sorted(khac)} ≠ {sig!r}.")
        recs = [r for r in recs if (str(r["episode_id"]), str(r["step_id"])) not in xong]
        print(f"Nối tiếp: đã có {len(xong)} bước, còn {len(recs)}")
        if not recs:
            print(f"Xong sẵn {len(xong)} bước → {args.out}")
            return
    if args.probe:
        recs = recs[:args.probe]
        print(f"PROBE: chỉ chạy {len(recs)} bước rồi dừng.")

    if args.dtype:
        import transformers as _tf
        kw = {("dtype" if int(_tf.__version__.split(".")[0]) >= 5 else "torch_dtype"):
              getattr(torch, args.dtype)}
        print(f"⚠️  KIỂU SỐ ĐẶT TAY: {args.dtype}. Điểm của lượt này KHÔNG so được với "
              f"lượt chạy trên GPU. Chỉ dùng để kiểm mã, đừng đưa vào bài.")
    else:
        kw = dtype_kw()
    print(f"Nạp {args.base} + LoRA {args.adapter} · kiểu số {list(kw.values())[0]}")
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        args.base, device_map="auto", **kw)
    from peft import PeftModel
    model = PeftModel.from_pretrained(model, args.adapter)
    model.eval()
    proc = AutoProcessor.from_pretrained(args.base, min_pixels=200704, max_pixels=1003520)
    if proc.tokenizer.pad_token_id is None:
        proc.tokenizer.pad_token = proc.tokenizer.eos_token

    manifest = {
        "run": sig, "base": args.base, "adapter": args.adapter,
        "cands": args.cands, "sha256_cands": sha256(args.cands),
        "sha256_test": sha256(os.path.join(TEST, "test.jsonl")),
        "sha256_ocr": sha256(os.path.join(TEST, "ocr.jsonl")),
        "only": args.only, "luc": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    print("manifest:", json.dumps(manifest, ensure_ascii=False))

    fo = open(args.out, "a", encoding="utf-8")
    t0, done, kiem_cheo = time.time(), 0, []
    for r in recs:
        img = Image.open(os.path.join(TEST, r["image"])).convert("RGB")
        rr = {"goal": r["goal"], "history": r.get("history") or []}
        cd = cands[r["image"]]
        body = prompt_body(rr, ocr.get(r["image"]), cands=cd)
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [{"type": "image"},
                                            {"type": "text", "text": "\n" + body}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)

        phuong_an = [None] + list(cd)              # `none` đứng đầu, rồi ứng viên thật
        spans = [span_of(c) for c in phuong_an]

        def duong_nhanh():
            """Mã hoá câu nhắc một lần, chạy từng span trên bộ nhớ đệm của nó.

            Sau mỗi span phải CẮT bộ nhớ đệm về đúng độ dài câu nhắc. Quên bước cắt thì
            span thứ hai đọc thấy span thứ nhất trong ngữ cảnh, điểm sai mà không có gì
            báo — nên chỗ này có `assert` độ dài, đừng gỡ."""
            enc = proc(text=[text], images=[img], return_tensors="pt").to(model.device)
            with torch.no_grad():
                o = model(**enc, use_cache=True)
            past, n_prompt = o.past_key_values, enc["input_ids"].shape[1]
            lg_cuoi = o.logits[:, -1].float()      # dự đoán token ĐẦU của span
            ds, ts = [], []
            for sp in spans:
                sid = proc.tokenizer(sp, add_special_tokens=False)["input_ids"]
                lp = float(torch.log_softmax(lg_cuoi[0], dim=-1)[sid[0]])
                if len(sid) > 1:
                    inp = torch.tensor([sid[:-1]], device=model.device)
                    with torch.no_grad():
                        o2 = model(input_ids=inp, past_key_values=past, use_cache=True)
                    lo = torch.log_softmax(o2.logits[0].float(), dim=-1)
                    for k in range(len(sid) - 1):
                        lp += float(lo[k, sid[k + 1]])
                    past = o2.past_key_values
                if not hasattr(past, "crop"):
                    sys.exit("⛔ DỪNG: lớp bộ nhớ đệm của transformers bản này không có "
                             "`crop`, không cắt về độ dài câu nhắc được. Chạy lại KHÔNG "
                             "có --cache-prompt (chậm hơn ~5-7 lần nhưng đúng).")
                past.crop(n_prompt)
                assert past.get_seq_length() == n_prompt, "cắt bộ nhớ đệm hỏng"
                ds.append(lp / len(sid))
                ts.append(len(sid))
            return ds, ts

        def duong_cham():
            """Mã hoá lại cả câu nhắc (gồm ảnh) cho từng lô span. Chậm, nhưng không phải
            tự tay quản bộ nhớ đệm — đây là đường CHUẨN, đường nhanh phải khớp với nó."""
            ds, ts = [], []
            for i in range(0, len(spans), args.span_batch):
                lo = spans[i:i + args.span_batch]
                full = [text + sp for sp in lo]
                enc_full = proc(text=full, images=[img] * len(lo),
                                return_tensors="pt", padding=True).to(model.device)
                with torch.no_grad():
                    out = model(**enc_full)
                logits = out.logits.float()
                ids = enc_full["input_ids"]
                attn = enc_full["attention_mask"]
                for b, sp in enumerate(lo):
                    n_span = len(proc.tokenizer(sp, add_special_tokens=False)["input_ids"])
                    assert int(attn[b].sum().item()) >= n_span, \
                        "span dài hơn cả chuỗi — nghi lệch bộ tách token"
                    # token cuối của chuỗi luôn là token cuối của span, nên đếm NGƯỢC từ
                    # cuối; cách này đúng với cả padding trái lẫn phải.
                    lp = 0.0
                    for k in range(n_span):
                        pos = ids.shape[1] - 1 - k
                        lp += float(torch.log_softmax(logits[b, pos - 1], dim=-1)[ids[b, pos]])
                    ds.append(lp / n_span)
                    ts.append(n_span)
            return ds, ts

        def _tinh():
            """Bộ chọn đường, kèm phép kiểm chéo bắt buộc ở ba bước đầu."""
            if not args.cache_prompt:
                return duong_cham()
            if len(kiem_cheo) < 3:
                dn, tn = duong_nhanh()
                dc, tc = duong_cham()
                lech = max(abs(a - b) for a, b in zip(dn, dc))
                kiem_cheo.append(lech)
                print(f"  kiểm chéo nhanh↔chậm: lệch tối đa {lech:.2e} "
                      f"trên {len(dn)} span", flush=True)
                if lech > 1e-3 or tn != tc:
                    sys.exit(f"⛔ DỪNG: hai đường tính ra khác nhau (lệch {lech:.2e}). "
                             f"Chạy lại KHÔNG có --cache-prompt. Đừng sửa ngưỡng kiểm.")
                return dc, tc
            return duong_nhanh()

        diem, sotoken = _tinh()
        s_none = diem[0]
        that = list(zip(phuong_an[1:], diem[1:], sotoken[1:]))
        if that:
            c_star, s_star, tok_star = max(that, key=lambda z: z[1])
        else:
            c_star, s_star, tok_star = None, float("-inf"), 0
        # cùng luật với build_sel_data.py: chỉ bước CHẠM và có tên vàng mới xét
        act = r["action"] if isinstance(r["action"], dict) else ast.literal_eval(
            str(r["action"]))
        la_cham = act.get("action_type") in ("click", "long_press") and "x" in act
        g = desc.get((str(r["episode_id"]), str(r["step_id"])))
        gc = None
        if la_cham and g and g.get("name"):
            gx, gy = g["point_norm"]
            gc = gold_candidate(cd, g["name"], gx, gy)

        rec = {
            "episode_id": str(r["episode_id"]), "step_id": str(r["step_id"]),
            "image": r["image"], "n_cand": len(cd),
            "s_none": s_none, "tok_none": sotoken[0],
            "s_star": s_star, "tok_star": tok_star,
            "cand_star": ({"name": c_star["name"], "x": c_star["x"], "y": c_star["y"]}
                          if c_star else None),
            "margin": (s_star - s_none) if that else None,
            # điểm của MỌI ứng viên, để quét lại τ mà không phải gọi GPU lần nữa
            "scores": [{"name": c["name"], "x": c["x"], "y": c["y"], "s": d, "tok": t}
                       for c, d, t in that],
            "la_cham": la_cham,
            "gold_in_menu": bool(gc),
            "gold_cand": ({"name": gc["name"], "x": gc["x"], "y": gc["y"]} if gc else None),
            "run": sig,
        }
        fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fo.flush()
        os.fsync(fo.fileno())      # mất máy Colab/Kaggle là chuyện thường, đừng để đệm
        done += 1
        if done % 20 == 0 or done == len(recs):
            t = time.time() - t0
            print(f"[{done}/{len(recs)}] {t/done:.2f} s/bước · "
                  f"còn ~{(len(recs)-done)*t/done/60:.0f} phút", flush=True)
    fo.close()
    print(f"Xong {done} bước → {args.out}")
    if args.probe:
        print("⚠️ Đây là lượt PROBE. Kiểm ba dòng trước khi chạy lượt dài: "
              "s_none và s_star phải âm và cùng cỡ; tok_none phải bằng nhau ở mọi bước; "
              "n_cand phải khớp khối ứng viên của bước đó.")


if __name__ == "__main__":
    main()
