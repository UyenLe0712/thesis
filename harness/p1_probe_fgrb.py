# -*- coding: utf-8 -*-
"""P1 — probe phân loại action/role/zone từ hidden state đóng băng của S1.

Theo đúng khoá của harness/tai_lieu_2026-09-27/230_ACTION_PROBE_FGRB_CHO_CHAT_LAM_27_9.md.
Chạy trên Kaggle T4 (không cần internet ngoài việc nạp Qwen2.5-VL-3B-Instruct từ HuggingFace,
nếu dataset không kèm sẵn cache model).

    python harness/p1_probe_fgrb.py --bundle /kaggle/input/fgrb-p1-bundle

Không mở test.jsonl, score_s1_seed101_raw.jsonl, hay bất kỳ file điểm test nào — script này
không import hay đọc các file đó ở bất kỳ đâu.
"""
import os, sys, json, re, argparse, time, collections

# Chặn thanh tiến trình tqdm TRƯỚC khi import transformers/huggingface_hub — nếu không,
# lượt tải Qwen2.5-VL-3B (~7 GB) in mỗi lần cập nhật thành MỘT DÒNG log trên Kaggle
# (tqdm ngoài terminal tương tác không ghi đè được dòng cũ), đã từng treo một lượt commit
# 7 giờ vì log ngập (xem harness/kaggle_pheA_CHAY_LAI.md). Đặt ở đây, KHÔNG đặt trong main().
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

MAX_OCR = 24
IMAGE_TOKEN_ID = 151655              # khớp harness/pata_model.py — hằng số của Qwen2.5-VL,
                                      # không suy từ model.config (thuộc tính có thể không tồn tại)
SYS = ("Bạn nhìn ảnh màn hình điện thoại và viết MỘT câu hướng dẫn ngắn bằng tiếng Anh "
       "cho người dùng, chỉ rõ cần chạm vào đâu để đi tiếp.")
BASE = "Qwen/Qwen2.5-VL-3B-Instruct"

ROLES = ["button", "option", "icon", "tab", "section", "bar", "list", "item", "view",
         "field", "box", "menu", "link", "card", "tile", "row", "toggle", "switch",
         "checkbox", "image", "text"]
ROLE_RE = re.compile(r"\b(" + "|".join(ROLES) + r")\b", re.I)
ZONE_RE = re.compile(
    r"\b(?:at|on|in) the ((?:top|bottom|middle|center|upper|lower)"
    r"(?: left| right)?(?: corner)?(?: of the (?:screen|page))?)\b", re.I)
ACTIONS = ["click", "scroll", "wait", "input_text", "open_app", "navigate_back",
           "long_press", "navigate_home"]


def label_role_zone(text):
    found = ROLE_RE.findall(text or "")
    zone = ZONE_RE.search(text or "")
    role = found[0].lower() if found else "NONE"
    return role, (zone.group(1).lower() if zone else "NONE")


def zone_coarse(z):
    """CHẨN ĐOÁN (không phải nhãn đã khoá của 230): gộp 31 cách viết zone về lưới 3×3.
    'bottom of the screen' / 'bottom' / 'lower' → 'bottom'; 'top right corner of the page' → 'top-right'."""
    if z == "NONE":
        return z
    w = z.split()
    v = next((x for x in w if x in ("top", "upper", "bottom", "lower", "middle", "center")), "")
    v = {"upper": "top", "lower": "bottom", "center": "middle"}.get(v, v)
    h = next((x for x in w if x in ("left", "right")), "")
    return f"{v}-{h}" if h else v


def prompt_body(r, ocr_rec):
    parts = [f"Mục tiêu: {r['goal'].strip()}"]
    hist = r.get("history") or []
    if hist:
        parts.append("Đã làm: " + " → ".join(h.strip() for h in hist[-3:]))
    if ocr_rec:
        items = ocr_rec["items"][:MAX_OCR]
        txt = " · ".join(f"{it['text']}" for it in items if it.get("text", "").strip())
        if txt:
            parts.append(f"Chữ đọc được trên màn: {txt}")
    parts.append("Viết câu hướng dẫn cho bước tiếp theo.")
    return "\n".join(parts)


def pick_dtype():
    import torch
    if not torch.cuda.is_available():
        return torch.float32
    return torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16


def dtype_kw():
    import transformers
    major = int(transformers.__version__.split(".")[0])
    return {("dtype" if major >= 5 else "torch_dtype"): pick_dtype()}


def load_rows(path):
    return [json.loads(x) for x in open(path, encoding="utf-8")]


def load_ocr(path):
    ocr = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            o = json.loads(line)
            ocr[o["image"]] = o
    return ocr


def extract_hidden(model, proc, image_dir, rows, ocr, log_every=200):
    """Trả về tensor [n, 2*hidden] và danh sách nhãn action/role/zone song song."""
    import torch
    from PIL import Image

    feats = []
    t0 = time.time()
    for i, r in enumerate(rows):
        rr = {"goal": r["goal"], "history": r.get("history") or []}
        msg = [{"role": "system", "content": SYS},
               {"role": "user", "content": [
                   {"type": "image"},
                   {"type": "text", "text": "\n" + prompt_body(rr, ocr.get(r["image"]))}]}]
        text = proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        img = Image.open(os.path.join(image_dir, r["image"])).convert("RGB")
        inp = proc(text=[text], images=[img], return_tensors="pt").to(model.device)

        with torch.no_grad():
            out = model(**inp, use_cache=False, output_hidden_states=True)
        h = out.hidden_states[-1][0]                      # [seq, hidden]
        ids = inp["input_ids"][0]
        img_mask = ids == IMAGE_TOKEN_ID
        if img_mask.sum() == 0:
            raise RuntimeError(f"Khong tim thay token anh o buoc {r['episode_id']}/{r['step_id']} "
                                f"(image_token_id={IMAGE_TOKEN_ID}). Dung lai, dung doan.")
        img_vec = h[img_mask].mean(dim=0)
        txt_vec = h[-1]
        vec = torch.cat([img_vec, txt_vec], dim=0).float().cpu()
        feats.append(vec)
        if (i + 1) % log_every == 0 or i == len(rows) - 1:
            el = time.time() - t0
            print(f"  hidden {i+1}/{len(rows)}  {el/60:.1f} phut, con lai ~"
                  f"{el/(i+1)*(len(rows)-i-1)/60:.1f} phut", flush=True)
    import torch
    return torch.stack(feats)


def load_model(bundle):
    import torch
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from peft import PeftModel

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("device", device, flush=True)

    proc = AutoProcessor.from_pretrained(BASE, min_pixels=200704, max_pixels=1003520)
    # device_map="auto" (như infer_branch.py) để accelerate tự cân bằng qua nhiều GPU nếu có —
    # nhưng "auto" có thể quyết định OFFLOAD ra CPU/đĩa tuỳ cách nó ước lượng bộ nhớ, và bản peft
    # đang cài lỗi khi nạp adapter LoRA vào một model có offload_index (KeyError trong
    # _update_offload — bắt được khi thử --limit trên CPU, xem harness/kaggle_p1_probe_fgrb.md
    # mục Ô 2.5). Model 3B thừa chỗ trong MỘT GPU T4 (16 GB) nên không cần "auto" cân bằng gì cả —
    # chỉ định thẳng một thiết bị, khớp cách harness/pata_model.py:load_base() đã làm
    # (device_map={"": 0}), loại hẳn nhánh mã có thể kích hoạt offload.
    dev_map = {"": 0} if torch.cuda.is_available() else {"": "cpu"}
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(BASE, device_map=dev_map, **dtype_kw())
    model = PeftModel.from_pretrained(model, os.path.join(bundle, "adapter_s1_seed101"))
    model.eval()
    for p in model.parameters():
        p.requires_grad = False
    return model, proc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True, help="thư mục bundle (images/, ocr.jsonl, "
                     "p1_train_rows.jsonl, p1_val_rows.jsonl, adapter_s1_seed101/)")
    ap.add_argument("--cache-out", default="/kaggle/working/_fgrb_probe",
                     help="nơi cache vector hidden state, ngoài clone")
    ap.add_argument("--cache-in", default="",
                     help="thư mục CHỈ ĐỌC chứa sẵn hiddens_*_seed101.pt (vd. output của một lượt "
                          "Kaggle trước, gắn vào /kaggle/input). Rỗng = chỉ tìm trong --cache-out")
    ap.add_argument("--max-epoch", type=int, default=30)
    # Sửa 28/9: lượt đầu train head FULL-BATCH, đặc trưng thô, Adam lr 1e-3 ⇒ 30 epoch = 30 bước
    # cập nhật, epoch chọn là epoch cuối, loss đầu 14 (logit quá lớn) và tăng ở epoch 1→3 ⇒ head
    # chưa hội tụ (report/207 §8.2). Mặc định mới: chuẩn hoá z-score theo train + minibatch 64 +
    # AdamW. Tái lập đúng lượt cũ: --batch-size 0 --no-standardize --lr 1e-3 --weight-decay 0.
    ap.add_argument("--batch-size", type=int, default=64, help="0 = full-batch (cách của lượt 27/9)")
    ap.add_argument("--no-standardize", action="store_true")
    ap.add_argument("--zone-coarse", action="store_true",
                     help="CHẨN ĐOÁN: gộp zone về lưới 3×3 trước khi train/chấm. Cổng P1 của 230 chấm "
                          "trên nhãn gốc 31 lớp — kết quả với cờ này KHÔNG dùng để phán P1")
    ap.add_argument("--save-heads", default="",
                     help="ghi ba head ở epoch được chọn + mu/sd chuẩn hoá + danh sách lớp ra tệp .pt "
                          "(P2 khởi tạo head từ tệp này)")
    ap.add_argument("--head-seed", type=int, default=101,
                     help="seed khởi tạo head + thứ tự minibatch (KHÔNG đổi mẫu 4.000, mẫu cố định ở bundle)")
    ap.add_argument("--shuffle-labels", action="store_true",
                     help="ĐỐI CHỨNG: hoán vị nhãn train (cùng hoán vị cho cả ba đầu) — head không thể học "
                          "tín hiệu thật; recall đạt được ở chế độ này là mức do đoán tràn")
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--weight-decay", type=float, default=1e-2)
    ap.add_argument("--limit", type=int, default=0,
                     help="CHỈ để thử nhanh trước khi commit: cắt train và val còn n dòng đầu. "
                          "0 = chạy đủ 4.000/1.567 (bắt buộc cho kết quả P1 thật). Có --limit thì "
                          "TUYỆT ĐỐI không dùng số ra để tính phán quyết P1.")
    args = ap.parse_args()

    os.makedirs(args.cache_out, exist_ok=True)

    tr_rows = load_rows(os.path.join(args.bundle, "p1_train_rows.jsonl"))
    va_rows = load_rows(os.path.join(args.bundle, "p1_val_rows.jsonl"))
    ocr = load_ocr(os.path.join(args.bundle, "ocr.jsonl"))
    print(f"train={len(tr_rows)} val={len(va_rows)} ocr_keys={len(ocr)}", flush=True)
    if args.limit:
        print(f"⚠️  --limit {args.limit} ĐANG BẬT — đây là lượt THỬ, không phải P1 thật. "
              f"Số ra sau đây KHÔNG được dùng để tính phán quyết P1.", flush=True)
        tr_rows = tr_rows[: args.limit]
        va_rows = va_rows[: args.limit]
    else:
        assert len(tr_rows) == 4000, "n_train_probe phai dung 4000, dung ngay neu khac"
        assert len(va_rows) == 1567, "val phai dung 1567, dung ngay neu khac"

    import torch

    tag = f"_limit{args.limit}" if args.limit else ""   # tách cache lượt thử khỏi lượt thật,
                                                          # kẻo lượt thật đọc nhầm cache 20 dòng
    cache_tr = os.path.join(args.cache_out, f"hiddens_train_seed101{tag}.pt")
    cache_va = os.path.join(args.cache_out, f"hiddens_val_seed101{tag}.pt")

    for d in [args.cache_in, args.cache_out]:
        if d and os.path.exists(os.path.join(d, os.path.basename(cache_tr))) \
                and os.path.exists(os.path.join(d, os.path.basename(cache_va))):
            cache_tr = os.path.join(d, os.path.basename(cache_tr))
            cache_va = os.path.join(d, os.path.basename(cache_va))
            break

    if os.path.exists(cache_tr) and os.path.exists(cache_va):
        print(f"Dung cache co san, khoi nap model va forward lai: {cache_tr} · {cache_va}", flush=True)
        Xtr = torch.load(cache_tr)
        Xva = torch.load(cache_va)
    else:
        model, proc = load_model(args.bundle)
        print("Trich hidden state — train...", flush=True)
        Xtr = extract_hidden(model, proc, args.bundle, tr_rows, ocr)
        torch.save(Xtr, cache_tr)
        print("Trich hidden state — val...", flush=True)
        Xva = extract_hidden(model, proc, args.bundle, va_rows, ocr)
        torch.save(Xva, cache_va)
        print(f"Da cache vector ra {args.cache_out} (khong thay file ket qua 231)", flush=True)

    # nhãn
    def labels_of(rows):
        act, role, zone = [], [], []
        for r in rows:
            a = (r.get("action") or {}).get("action_type", "?")
            r_, z_ = label_role_zone(r["target_instruction"])
            if args.zone_coarse:
                z_ = zone_coarse(z_)
            act.append(a)
            role.append(r_)
            zone.append(z_)
        return act, role, zone

    act_tr, role_tr, zone_tr = labels_of(tr_rows)
    act_va, role_va, zone_va = labels_of(va_rows)

    act_classes = sorted(set(act_tr) | set(act_va))
    role_classes = sorted(set(role_tr) | set(role_va))
    zone_classes = sorted(set(zone_tr) | set(zone_va))

    def to_idx(vals, classes):
        m = {c: i for i, c in enumerate(classes)}
        return torch.tensor([m[v] for v in vals], dtype=torch.long)

    y_act_tr, y_role_tr, y_zone_tr = (to_idx(act_tr, act_classes), to_idx(role_tr, role_classes),
                                       to_idx(zone_tr, zone_classes))
    y_act_va, y_role_va, y_zone_va = (to_idx(act_va, act_classes), to_idx(role_va, role_classes),
                                       to_idx(zone_va, zone_classes))

    assert Xtr.shape[0] == len(tr_rows) and Xva.shape[0] == len(va_rows), \
        f"cache lech so dong: {tuple(Xtr.shape)} / {tuple(Xva.shape)} vs {len(tr_rows)} / {len(va_rows)}"
    Xtr = Xtr.float()
    Xva = Xva.float()
    mu = torch.zeros(1, Xtr.shape[1])
    sd = torch.ones(1, Xtr.shape[1])
    if not args.no_standardize:
        mu = Xtr.mean(dim=0, keepdim=True)
        sd = Xtr.std(dim=0, keepdim=True).clamp(min=1e-6)
        Xtr = (Xtr - mu) / sd          # thống kê CHỈ lấy từ train, áp nguyên cho val
        Xva = (Xva - mu) / sd
    torch.manual_seed(args.head_seed)
    bs = args.batch_size if args.batch_size > 0 else len(tr_rows)
    print(f"head: standardize={not args.no_standardize} batch={bs} lr={args.lr} "
          f"weight_decay={args.weight_decay} max_epoch={args.max_epoch} "
          f"=> {args.max_epoch * ((len(tr_rows) + bs - 1) // bs)} buoc cap nhat", flush=True)
    dim = Xtr.shape[1]
    if args.zone_coarse:
        print(f"⚠️  --zone-coarse: CHAN DOAN, zone gop ve {len(zone_classes)} lop — khong phai cong P1",
              flush=True)
    if args.shuffle_labels:
        print("⚠️  --shuffle-labels: DOI CHUNG, nhan train bi hoan vi — khong phai P1 that", flush=True)

    def class_weight(y, n_classes):
        cnt = torch.bincount(y, minlength=n_classes).float()
        w = 1.0 / cnt.clamp(min=1)
        return w / w.sum() * n_classes

    head_act = torch.nn.Linear(dim, len(act_classes))
    head_role = torch.nn.Linear(dim, len(role_classes))
    head_zone = torch.nn.Linear(dim, len(zone_classes))
    params = list(head_act.parameters()) + list(head_role.parameters()) + list(head_zone.parameters())
    if args.weight_decay > 0:
        opt = torch.optim.AdamW(params, lr=args.lr, weight_decay=args.weight_decay)
    else:
        opt = torch.optim.Adam(params, lr=args.lr)

    if args.shuffle_labels:
        pi = torch.randperm(len(tr_rows), generator=torch.Generator().manual_seed(args.head_seed + 7))
        y_act_tr, y_role_tr, y_zone_tr = y_act_tr[pi], y_role_tr[pi], y_zone_tr[pi]
    w_act = class_weight(y_act_tr, len(act_classes))
    w_role = class_weight(y_role_tr, len(role_classes))
    w_zone = class_weight(y_zone_tr, len(zone_classes))

    def macro_f1(pred, gold, n_classes):
        f1s = []
        for c in range(n_classes):
            tp = ((pred == c) & (gold == c)).sum().item()
            fp = ((pred == c) & (gold != c)).sum().item()
            fn = ((pred != c) & (gold == c)).sum().item()
            if tp + fp + fn == 0:
                continue
            p = tp / (tp + fp) if tp + fp else 0.0
            r = tp / (tp + fn) if tp + fn else 0.0
            f1 = 2 * p * r / (p + r) if (p + r) else 0.0
            f1s.append(f1)
        return sum(f1s) / len(f1s) if f1s else 0.0

    def recall_non_none(pred, gold, none_idx):
        mask = gold != none_idx
        if mask.sum() == 0:
            return float("nan")
        return (pred[mask] == gold[mask]).float().mean().item()

    role_none_idx = role_classes.index("NONE")
    zone_none_idx = zone_classes.index("NONE")

    best = {"epoch": -1, "score": -1.0}
    gen = torch.Generator().manual_seed(args.head_seed)
    for epoch in range(args.max_epoch):
        head_act.train(); head_role.train(); head_zone.train()
        perm = torch.randperm(len(tr_rows), generator=gen)
        tot, nb = 0.0, 0
        for k in range(0, len(tr_rows), bs):
            idx = perm[k:k + bs]
            opt.zero_grad()
            la = torch.nn.functional.cross_entropy(head_act(Xtr[idx]), y_act_tr[idx], weight=w_act)
            lr_ = torch.nn.functional.cross_entropy(head_role(Xtr[idx]), y_role_tr[idx], weight=w_role)
            lz = torch.nn.functional.cross_entropy(head_zone(Xtr[idx]), y_zone_tr[idx], weight=w_zone)
            loss = la + lr_ + lz
            loss.backward()
            opt.step()
            tot += loss.item()
            nb += 1
        loss = torch.tensor(tot / nb)

        head_act.eval(); head_role.eval(); head_zone.eval()
        with torch.no_grad():
            pa = head_act(Xva).argmax(dim=1)
            pr = head_role(Xva).argmax(dim=1)
            pz = head_zone(Xva).argmax(dim=1)
        f1_a = macro_f1(pa, y_act_va, len(act_classes))
        f1_r = macro_f1(pr, y_role_va, len(role_classes))
        f1_z = macro_f1(pz, y_zone_va, len(zone_classes))
        mean_f1 = (f1_a + f1_r + f1_z) / 3
        print(f"epoch {epoch:02d} loss {loss.item():.4f} macroF1 act/role/zone "
              f"{f1_a:.4f}/{f1_r:.4f}/{f1_z:.4f} mean {mean_f1:.4f}", flush=True)
        if mean_f1 > best["score"]:
            best = {"epoch": epoch, "score": mean_f1,
                    "sd_a": {k: v.clone() for k, v in head_act.state_dict().items()},
                    "sd_r": {k: v.clone() for k, v in head_role.state_dict().items()},
                    "sd_z": {k: v.clone() for k, v in head_zone.state_dict().items()},
                    "pa": pa.clone(), "pr": pr.clone(), "pz": pz.clone()}

    print("\n=== KHOA EPOCH THEO macro-F1 TRUNG BINH TREN VAL ===", flush=True)
    print(f"epoch chon: {best['epoch']}  macro-F1 trung binh: {best['score']:.4f}", flush=True)
    if best["epoch"] == args.max_epoch - 1:
        print("⚠️  epoch chon la epoch CUOI — head co the chua hoi tu, doc ket qua than trong.",
              flush=True)

    pa, pr, pz = best["pa"], best["pr"], best["pz"]
    if args.save_heads:
        torch.save({"act_classes": act_classes, "role_classes": role_classes,
                    "zone_classes": zone_classes, "zone_coarse": args.zone_coarse,
                    "mu": mu[0], "sd": sd[0], "head_act": best["sd_a"], "head_role": best["sd_r"],
                    "head_zone": best["sd_z"], "epoch": best["epoch"], "head_seed": args.head_seed},
                   args.save_heads)
        print(f"Da ghi head (epoch {best['epoch']}) ra {args.save_heads}", flush=True)

    acc_act = (pa == y_act_va).float().mean().item()
    acc_role = (pr == y_role_va).float().mean().item()
    acc_zone = (pz == y_zone_va).float().mean().item()
    recall_role = recall_non_none(pr, y_role_va, role_none_idx)
    recall_zone = recall_non_none(pz, y_zone_va, zone_none_idx)
    f1_a = macro_f1(pa, y_act_va, len(act_classes))
    f1_r = macro_f1(pr, y_role_va, len(role_classes))
    f1_z = macro_f1(pz, y_zone_va, len(zone_classes))

    majority_act = collections.Counter(act_va).most_common(1)[0]
    n_gold_none_role = int((y_role_va == role_none_idx).sum())
    n_pred_none_role = int((pr == role_none_idx).sum())
    n_gold_none_zone = int((y_zone_va == zone_none_idx).sum())
    n_pred_none_zone = int((pz == zone_none_idx).sum())

    print("\n=== P1 — KET QUA TREN VAL (1.567 buoc), BAT BUOC IN THEO MUC 6 CUA 230 ===")
    print("n_train_probe = 4000, seed = 101")
    print(f"role: accuracy={acc_role*100:.2f}% recall_khac_NONE={recall_role*100:.2f}% "
          f"macroF1={f1_r*100:.2f}% gold_NONE={n_gold_none_role} pred_NONE={n_pred_none_role}")
    print(f"zone: accuracy={acc_zone*100:.2f}% recall_khac_NONE={recall_zone*100:.2f}% "
          f"macroF1={f1_z*100:.2f}% gold_NONE={n_gold_none_zone} pred_NONE={n_pred_none_zone}")
    print(f"action: accuracy={acc_act*100:.2f}% majority=({majority_act[0]}, "
          f"{100*majority_act[1]/len(va_rows):.2f}%)")
    print(f"epoch_chon={best['epoch']} macroF1_trungbinh_luc_chon={best['score']*100:.2f}%")

    print("\n=== 8 VI DU VAL DU DOAN ROLE SAI + 8 DUNG (episode_id, step_id, gold, pred) ===")
    wrong, right = [], []
    for i, r in enumerate(va_rows):
        g = role_classes[y_role_va[i]]
        p = role_classes[pr[i]]
        item = (r["episode_id"], r["step_id"], g, p)
        (wrong if g != p else right).append(item)
    for kind, lst in [("SAI", wrong[:8]), ("DUNG", right[:8])]:
        print(f"-- {kind} --")
        for ep, st, g, p in lst:
            print(f"  ep={ep} step={st} gold={g} pred={p}")

    print("\n=== P1 GATE ===")
    gate_role = recall_role >= 0.50
    gate_zone = recall_zone >= 0.30
    gate_act = acc_act >= 0.739
    print(f"recall_role>=50%: {'DAT' if gate_role else 'TRUOT'} ({recall_role*100:.2f}%)")
    print(f"recall_zone>=30%: {'DAT' if gate_zone else 'TRUOT'} ({recall_zone*100:.2f}%)")
    print(f"accuracy_action>=73.9%: {'DAT' if gate_act else 'TRUOT'} ({acc_act*100:.2f}%)")
    p1_pass = gate_role and gate_zone and gate_act
    print(f"\nP1 = {'DAT' if p1_pass else 'TRUOT'}")


if __name__ == "__main__":
    main()
