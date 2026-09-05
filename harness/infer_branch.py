# -*- coding: utf-8 -*-
"""
Chạy một nhánh đã huấn luyện trên TẬP KIỂM, sinh câu hướng dẫn để đem chấm.

Mắt xích giữa huấn luyện và chấm điểm: nạp mô hình gốc + bộ trọng số LoRA của một
nhánh, chạy qua toàn bộ tập kiểm, cắt bỏ phần khai báo, lưu câu ra tệp cho
`metric_exec.py` chấm.

BA ĐIỀU KIỆN PHẢI GIỮ, nếu phá là hỏng cả phép so:

  1. Đầu vào lúc chấm phải GIỐNG HỆT lúc dạy. Mã dựng câu nhắc ở đây import thẳng
     từ `build_branch_data.py` chứ không chép lại, để không có đường nào lệch nhau.
  2. Cắt bỏ phần `<desc>…</desc>` trước khi chấm — người dùng không bao giờ thấy nó,
     và bộ trỏ cũng không được thấy, kẻo thành đưa đáp án cho giám khảo.
  3. Mọi nhánh sinh với cùng tham số sinh (greedy, cùng độ dài tối đa). Sinh ngẫu
     nhiên sẽ thêm một nguồn nhiễu nữa vào giữa hai nhánh.

Chạy trên máy có GPU:
  python harness/infer_branch.py --adapter /workspace/ckpt/s1_seed101 --out preds_s1_seed101.jsonl
  python harness/infer_branch.py --adapter ... --limit 50        # thử nhanh trước
  python harness/infer_branch.py --no-adapter --out preds_base.jsonl   # mô hình gốc, chưa huấn luyện
"""
import os, sys, json, re, argparse, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_branch_data import prompt_body, prompt_of, SYS   # dùng chung mã dựng câu nhắc

TEST = os.path.join(HERE, "dg1_cache", "test_ac")
BASE = "Qwen/Qwen2.5-VL-3B-Instruct"


def strip_desc(s):
    """Bỏ phần khai báo, chỉ giữ câu hướng dẫn.

    Ba dạng phải xử: khai báo đóng thẻ đủ; khai báo bị cắt cụt do chạm trần độ dài
    (thẻ mở mà không có thẻ đóng — khi đó coi như mô hình chưa kịp viết câu);
    và mô hình không sinh khai báo nào.

    Xử CẢ HAI loại thẻ tiền tố của dự án:
      · `<desc>…</desc>` — nhánh S2 / MIN-DESC / CE2 (khai báo bốn ô)
      · `<sel>…</sel>`   — nhánh gui_sel (đầu chọn, thêm 2/9/2026)
    ⛔ Thiếu nhánh `<sel>` thì `pred` của gui_sel sẽ là chính cái thẻ, còn câu thật bị
    vứt — bộ trỏ đọc toạ độ trong thẻ và chấm ra điểm vô nghĩa, log không báo gì.
    """
    for mo, dong in (("<desc>", "</desc>"), ("<sel>", "</sel>")):
        if dong in s:
            s = s.split(dong, 1)[1]
        elif mo in s:
            s = re.sub(re.escape(mo) + r".*", "", s, flags=re.S)
    return s.strip().split("\n")[0].strip()


VISION = "<|vision_start|><|image_pad|><|vision_end|>"

def pick_dtype():
    """Chọn kiểu số theo card ĐANG CÓ, đừng ép bf16.

    A100 có bf16; T4 (Turing) và P100 (Pascal) — hai card của Colab/Kaggle bản miễn phí —
    thì KHÔNG. Ép bf16 ở đó sẽ lỗi hoặc rơi vào đường giả lập chậm khủng khiếp, rồi ta
    ngồi đổ oan cho bộ trỏ hay cho mô hình. Với suy luận, fp16 không đổi kết luận.

    ⚠ ĐỪNG hỏi `torch.cuda.is_bf16_supported()`. PyTorch đời mới trả True cho cả T4 vì
    mặc định nó tính luôn đường GIẢ LẬP — đo được trên Kaggle ngày 9/8: Tesla T4 báo
    True. Hỏi thẳng đời kiến trúc: bf16 chạy thật từ Ampere (sm_80) trở lên.
    """
    import torch
    if not torch.cuda.is_available():
        return torch.float32
    return torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16


def dtype_kw():
    """transformers 5 đổi tên tham số `torch_dtype` thành `dtype`; bản 4.x chỉ hiểu tên
    cũ. Kaggle ngày 9/8 cài sẵn 5.0.0, máy nhà thì 4.x — cùng một dòng mã phải chạy
    được ở cả hai chỗ, không thì lại sinh ra một khác biệt môi trường vô hình."""
    import transformers
    major = int(transformers.__version__.split(".")[0])
    return {("dtype" if major >= 5 else "torch_dtype"): pick_dtype()}


MAX_ELEMS = 40          # cắt danh sách; màn có trung vị 89 phần tử, nhét hết là phình câu nhắc
W_SCREEN, H_SCREEN = 1080, 2400


def screen_elements(rec):
    """Danh sách phần tử hiển thị của màn — đầu vào của nhánh B-infer.

    B-infer là đối thủ RẺ NHẤT: không huấn luyện gì thêm, chỉ lấy trọng số S1 rồi nhét
    thông tin phần tử vào đầu vào lúc chạy. Nếu nó bằng được S2 thì việc huấn luyện mất
    lý do tồn tại, nên phải đo.

    ⚠ KHÔNG đánh dấu phần tử nào là đích, và KHÔNG dùng toạ độ chuẩn ở bất kỳ đâu. Nhét
    khai báo của đúng nút đích là một thí nghiệm KHÁC — `report/106` mục 5 bước 6 đã đăng
    ký riêng và gọi đúng tên là phép thử TRẦN. Trộn hai thứ vào nhau sẽ bắt ta kết luận
    "huấn luyện mất lý do tồn tại" từ chỗ một điều kiện có-lời-giải-sẵn thắng một điều
    kiện không có (`report/106` sửa đổi 7/8 mục c).

    Giới hạn phải khai kèm: cây trợ năng cho trung vị 89 phần tử mỗi màn nhưng chỉ 14,1%
    có tên, nên danh sách này phần lớn là vai trò kèm toạ độ, ít chữ.
    """
    import a11y_inventory as A11Y
    rel = f"episode_{rec['episode_id']}_screenshot_{rec['step_id']}.png"
    o = A11Y._load(A11Y.key_for(rel) or "")
    if not o:
        return []
    out = []
    for w in o:
        if w.get("window_type") == 3:
            continue
        for n in w.get("tree", []):
            if not n.get("is_visible_to_user"):
                continue
            b = n.get("bounds_in_screen") or {}
            x1, y1 = b.get("left", 0), b.get("top", 0)
            x2, y2 = b.get("right", 0), b.get("bottom", 0)
            if x2 - x1 < 8 or y2 - y1 < 8:
                continue
            # Bỏ KHUNG CHỨA. Không có luật này thì danh sách toàn "(không tên)
            # <point>500,500</point>" lặp đi lặp lại — tâm của các khung phủ gần hết
            # màn đều rơi vào giữa. Đây đúng lỗi hộp lồng nhau đã bắt ở khâu dựng nhãn
            # (report/108 mục 8, dòng đầu), chỉ khác chỗ xuất hiện.
            if (x2 - x1) * (y2 - y1) > 0.25 * W_SCREEN * H_SCREEN:
                continue
            nm = (n.get("content_description") or "").strip()
            out.append((y1, x1, nm, (x1 + x2) // 2, (y1 + y2) // 2))
    out.sort()                                   # thứ tự đọc: trên xuống, trái sang phải

    # Gộp phần tử trùng tâm: cây trợ năng lồng nhiều lớp nên một nút hay xuất hiện 2-3
    # lần với cùng một tâm, chỉ khác lớp bọc.
    seen, uniq = set(), []
    for y1, x1, nm, cx, cy in out:
        k = (cx // 8, cy // 8, nm)
        if k in seen:
            continue
        seen.add(k); uniq.append((nm, cx, cy))

    # Cắt còn MAX_ELEMS: ưu tiên phần tử CÓ TÊN, vì chỉ 14,1% có tên mà danh sách theo
    # thứ tự đọc thuần sẽ để phần không tên ăn hết chỗ. Giữ nguyên thứ tự đọc trong mỗi
    # nhóm để tín hiệu vị trí không bị xáo.
    named = [e for e in uniq if e[0]]
    anon = [e for e in uniq if not e[0]]
    keep = named[:MAX_ELEMS] + anon[:max(0, MAX_ELEMS - len(named))]
    order = {id(e): i for i, e in enumerate(uniq)}
    keep.sort(key=lambda e: order[id(e)])

    lines = []
    for nm, cx, cy in keep:
        px, py = round(cx / W_SCREEN * 1000), round(cy / H_SCREEN * 1000)
        lines.append(f"{nm or '(không tên)'} <point>{px},{py}</point>")
    return lines


def with_elements(body, rec):
    """Nối danh sách phần tử vào câu nhắc, đặt TRƯỚC dòng lệnh cuối để không phá cấu trúc."""
    els = screen_elements(rec)
    if not els:
        return body
    block = "Phần tử trên màn: " + " · ".join(els)
    tail = "Viết câu hướng dẫn cho bước tiếp theo."
    return body.replace(tail, block + "\n" + tail) if tail in body else body + "\n" + block


def load_test_descriptors():
    """Nhãn khai báo CHUẨN của tập kiểm — dựng bằng
    `descriptor_label_build.py --split test`. Chỉ dùng cho phép thử TRẦN."""
    p = os.path.join(TEST, "descriptors.jsonl")
    if not os.path.exists(p):
        sys.exit("Thiếu " + p + " — chạy: python harness/descriptor_label_build.py --split test")
    d = {}
    for line in open(p, encoding="utf-8"):
        r = json.loads(line)
        d[(r["episode_id"], r["step_id"])] = r["desc"]
    return d


def filler_like(desc, tok):
    """Đoạn đệm vô nghĩa dài BẰNG khai báo chuẩn, tính theo TOKEN.

    Nhánh đối chứng của phép thử trần tồn tại để loại một khả năng duy nhất: điểm tăng
    chỉ vì đầu vào dài thêm. Ghép theo ký tự là ghép nhầm đại lượng — mất mát và ngân
    sách ngữ cảnh đều tính theo token. Đây đúng lỗi đã bắt ở S2r ngày 7/8 (ghép ký tự
    trong khi bản đăng ký ghi token: chỉ 54,0% cặp lệch ≤2 token).
    """
    n = len(tok.encode(desc))
    unit = " nihil"
    k = max(1, len(tok.encode(unit)))
    out = (unit * max(1, round(n / k))).strip()
    # tỉa cho khít: bớt/thêm từng đơn vị cho tới khi lệch ≤1 token
    while len(tok.encode(out)) > n + 1 and " " in out:
        out = out.rsplit(" ", 1)[0]
    while len(tok.encode(out)) < n - 1:
        out += unit
    return out


def with_ceiling(body, rec, mode, descs, tok):
    """Phép thử TRẦN — report/106 mục 5 bước 6.

    Nối khai báo CHUẨN của đúng phần tử đích vào đầu vào lúc suy luận. Nó cho biết
    **trần trên của thiết kế**: nếu mô hình được phát không công đúng thứ mà tầng khai
    báo cố sinh ra, điểm lên tới đâu. Nhánh `filler` là đối chứng độ dài.

    ⚠️ KHÔNG phải B-infer. B-infer nhét DANH SÁCH phần tử của màn, không đánh dấu cái
    nào là đích — một phép so công bằng. Phép trần nhét thẳng lời giải. Hai thứ này
    từng bị đọc lẫn vào nhau; đã tách bạch ở report/106 sửa đổi 7/8 mục c.
    """
    d = descs.get((rec["episode_id"], rec["step_id"]))
    if not d:
        return body
    block = "Khai báo phần tử đích: " + (d if mode == "gold" else filler_like(d, tok))
    tail = "Viết câu hướng dẫn cho bước tiếp theo."
    return body.replace(tail, block + "\n" + tail) if tail in body else body + "\n" + block


def selftest(base=None, n_batch=5):
    """Chứng minh đường chấm khớp đường dạy — chạy được trên CPU, không tốn gì.

    Ba phép, phép nào rớt là CẤM chạy tiếp (lỗi loại này không báo lỗi, chỉ làm
    điểm tụt mà không ai biết vì sao):

      1. Chuỗi render lúc chấm phải TRÙNG TỪNG KÝ TỰ với chuỗi lúc dạy. Lúc dạy
         LLaMA-Factory thay "<image>" bằng ba token ảnh; ở đây mô phỏng đúng phép
         thay đó rồi so với chuỗi mà chat template sinh từ content dạng danh sách.
      2. Đầu vào đã tách token phải CÓ token ảnh. Bản cũ đưa chuỗi "<image>" nên
         template in nguyên văn, số token ảnh bằng 0 — mô hình chạy mù.
      3. (cần GPU) sinh ở lô 1 và lô n phải ra câu TRÙNG NGUYÊN VĂN. Lệch tức là
         đệm sai bên, và mọi con số theo lô đều không tin được.
    """
    from transformers import AutoProcessor
    from PIL import Image
    base = base or BASE
    proc = AutoProcessor.from_pretrained(base, min_pixels=200704, max_pixels=1003520)
    proc.tokenizer.padding_side = "left"

    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")][:n_batch]
    ocr = {}
    op = os.path.join(TEST, "ocr.jsonl")
    if os.path.exists(op):
        for line in open(op, encoding="utf-8"):
            o = json.loads(line); ocr[o["image"]] = o

    ok = True
    r = recs[0]
    rr = {"goal": r["goal"], "history": r.get("history") or []}
    body = prompt_body(rr, ocr.get(r["image"]))

    # (1) so chuỗi render hai đường
    m_chua = [{"role": "system", "content": SYS},
              {"role": "user", "content": [{"type": "image"},
                                           {"type": "text", "text": "\n" + body}]}]
    t_cham = proc.apply_chat_template(m_chua, tokenize=False, add_generation_prompt=True)
    m_day = [{"role": "system", "content": SYS},
             {"role": "user", "content": prompt_of(rr, ocr.get(r["image"]))}]
    t_day = proc.apply_chat_template(m_day, tokenize=False, add_generation_prompt=True)
    t_day = t_day.replace("<image>", VISION)          # đúng phép LLaMA-Factory làm
    print(f"  [1] chuỗi lúc chấm trùng lúc dạy : {'ĐẠT' if t_cham == t_day else 'RỚT'}")
    if t_cham != t_day:
        ok = False
        for i, (x, y) in enumerate(zip(t_cham, t_day)):
            if x != y:
                print(f"      lệch từ vị trí {i}:")
                print(f"        chấm: {t_cham[max(0,i-40):i+40]!r}")
                print(f"        dạy : {t_day[max(0,i-40):i+40]!r}")
                break

    # (2) đếm token ảnh trong đầu vào thật
    img = Image.open(os.path.join(TEST, r["image"])).convert("RGB")
    inp = proc(text=[t_cham], images=[img], return_tensors="pt", padding=True)
    pad_id = proc.tokenizer.convert_tokens_to_ids("<|image_pad|>")
    n_img = int((inp["input_ids"] == pad_id).sum())
    print(f"  [2] số token ảnh trong đầu vào   : {n_img}  {'ĐẠT' if n_img > 0 else 'RỚT — chạy mù'}")
    if n_img == 0:
        ok = False
    print(f"      (đệm bên: {proc.tokenizer.padding_side} · ngân sách điểm ảnh khớp train_config)")

    print(f"  [3] lô 1 vs lô {n_batch} ra cùng câu  : cần GPU, chạy trên máy thuê bằng"
          f" --selftest-batch trước lượt chấm đầu tiên")
    print("\n" + ("TỰ KIỂM ĐẠT — được phép chạy tiếp." if ok else
                  "TỰ KIỂM RỚT — KHÔNG chạy tiếp, sửa xong hãy chạy lại."))
    return ok


def selftest_batch(a, n_batch=8):
    """Phép thứ ba của tự kiểm — CẦN GPU, nên tách riêng.

    Sinh cùng một bước ở lô kích thước 1 và ở lô kích thước n, rồi so câu ra. Lệch nhau
    tức đệm sai bên: với mô hình sinh, đệm bên PHẢI đẩy token đệm vào giữa câu nhắc và
    chỗ bắt đầu sinh, làm câu ở lô lớn khác câu ở lô một. Lỗi này không báo gì cả — chỉ
    làm điểm tụt ở mọi nhánh, và tụt không đều theo thứ tự bản ghi.

    Cho tới 7/8 phép này KHÔNG CÓ CỜ ĐỂ CHẠY: dòng in ở phép [3] bảo chạy
    `--selftest-batch`, mà `argparse` không có cờ đó. Nghĩa là ai làm theo hướng dẫn
    cũng sẽ nhận lỗi "unrecognized arguments" rồi bỏ qua, và tưởng đã kiểm.
    """
    import torch
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from PIL import Image

    proc = AutoProcessor.from_pretrained(a.base, min_pixels=200704, max_pixels=1003520)
    proc.tokenizer.padding_side = "left"
    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")][:n_batch]
    ocr = {}
    op = os.path.join(TEST, "ocr.jsonl")
    if os.path.exists(op):
        for line in open(op, encoding="utf-8"):
            o = json.loads(line); ocr[o["image"]] = o

    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        a.base, device_map="auto", **dtype_kw())
    if a.adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.adapter)
    model.eval()

    def gen(batch):
        texts, imgs = [], []
        for r in batch:
            rr = {"goal": r["goal"], "history": r.get("history") or []}
            msg = [{"role": "system", "content": SYS},
                   {"role": "user", "content": [
                       {"type": "image"},
                       {"type": "text", "text": "\n" + prompt_body(rr, ocr.get(r["image"]))}]}]
            texts.append(proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True))
            imgs.append(Image.open(os.path.join(TEST, r["image"])).convert("RGB"))
        inp = proc(text=texts, images=imgs, return_tensors="pt", padding=True).to(model.device)
        with torch.no_grad():
            g = model.generate(**inp, max_new_tokens=a.max_new, do_sample=False,
                               use_cache=True)
        return [proc.decode(g[i][len(inp["input_ids"][i]):], skip_special_tokens=True).strip()
                for i in range(len(batch))]

    print(f"Sinh lô 1 cho {len(recs)} bước...")
    one = [gen([r])[0] for r in recs]
    print(f"Sinh lô {len(recs)} một lượt...")
    many = gen(recs)

    bad = [i for i in range(len(recs)) if one[i] != many[i]]
    print("=" * 70)
    print(f"  [3] lô 1 vs lô {len(recs)} : {len(recs)-len(bad)}/{len(recs)} trùng nguyên văn"
          f"   {'ĐẠT' if not bad else 'RỚT'}")
    for i in bad[:3]:
        print(f"      bước {recs[i]['episode_id']}/{recs[i]['step_id']}")
        print(f"        lô 1  : {one[i][:110]!r}")
        print(f"        lô lớn: {many[i][:110]!r}")
    if bad:
        print("\n  RỚT — gần như chắc chắn là đệm sai bên. Kiểm padding_side='left'.\n"
              "  KHÔNG chấm khi chưa sửa: mọi con số theo lô đều không tin được.")
    else:
        print(f"\n  ĐẠT — đệm bên {proc.tokenizer.padding_side}, chấm theo lô an toàn.")
    return not bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", default=None, help="thư mục LoRA của nhánh")
    ap.add_argument("--no-adapter", action="store_true", help="chạy mô hình gốc, chưa huấn luyện")
    ap.add_argument("--out", help="bắt buộc trừ khi chạy --selftest / --selftest-batch")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--max-new", type=int, default=96)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--cands", default="",
                    help="đường dẫn candidates.jsonl. BẮT BUỘC cho nhánh gui_sel và "
                         "gui_sft_match — hai nhánh đó được DẠY với khối ứng viên trong câu "
                         "nhắc, chấm mà thiếu là lệch dạy-chấm và không có gì báo lỗi. "
                         "BỎ TRỐNG cho S1/S2/MIN-DESC/CE2/gui_s1_match (giữ 24 dòng OCR).")
    ap.add_argument("--save-conf", action="store_true",
                    help="lưu xác suất tại BƯỚC QUYẾT ĐỊNH (token đầu ngay sau thẻ <sel>): "
                         "p_none · p_top · token top. Không có nó thì mô hình chỉ cho ra một "
                         "quyết định cứng, không dựng được đường risk-coverage và không hiệu "
                         "chỉnh được ngưỡng abstain. Tốn thêm ~0,5 GB VRAM cho bảng logits.")
    ap.add_argument("--force-sel", action="store_true",
                    help="CẤM mô hình trả <sel>none</sel> — phép thử chẩn đoán 3/9: khi bị ép "
                         "chọn thì nó chọn đúng bao nhiêu? Phân biệt 'dè dặt quá mức' với "
                         "'thật sự không biết'. ⛔ Không dùng cho lượt chấm chính.")
    ap.add_argument("--only", default="",
                    help="tệp jsonl chỉ chứa các bước cần sinh (đọc episode_id/step_id). "
                         "Dùng để sinh lại đúng một lát thay vì cả tập.")
    ap.add_argument("--selftest", action="store_true",
                    help="kiểm câu nhắc khớp lúc dạy (CPU, không cần mô hình)")
    ap.add_argument("--b-infer", action="store_true",
                    help="nhánh B-infer: nối DANH SÁCH phần tử của màn vào đầu vào lúc chạy "
                         "(không đánh dấu đích, không dùng toạ độ chuẩn). Dùng với trọng số S1.")
    ap.add_argument("--ceiling", choices=["gold", "filler"],
                    help="phép thử TRẦN (report/106 mục 5 bước 6): nối khai báo CHUẨN của "
                         "phần tử đích vào đầu vào (gold), hoặc đoạn đệm vô nghĩa cùng số "
                         "token (filler, đối chứng độ dài). KHÔNG phải --b-infer.")
    ap.add_argument("--selftest-batch", action="store_true",
                    help="phép [3]: lô 1 và lô n có ra cùng câu không (CẦN GPU). "
                         "Chạy trước lượt chấm đầu tiên trên máy thuê.")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest(a.base) else 1)
    if a.selftest_batch:
        sys.exit(0 if selftest_batch(a, a.batch) else 1)
    if not a.out:
        sys.exit("Thiếu --out.")
    if a.b_infer and a.ceiling:
        sys.exit("--b-infer và --ceiling là HAI thí nghiệm khác nhau, không chạy chung.")
    if not a.adapter and not a.no_adapter:
        sys.exit("Phải cho --adapter, hoặc --no-adapter nếu cố ý chạy mô hình gốc.")

    import torch
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    from PIL import Image

    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")]
    ocr = {}
    op = os.path.join(TEST, "ocr.jsonl")
    if os.path.exists(op):
        with open(op, encoding="utf-8") as f:
            for line in f:
                o = json.loads(line)
                ocr[o["image"]] = o
    else:
        print("CẢNH BÁO: chưa có ocr.jsonl của tập kiểm — đầu vào sẽ THIẾU phần chữ đọc "
              "được, khác lúc dạy. Chạy prep_ocr_train.py --split test trước.")

    # ── KHỐI ỨNG VIÊN (thêm 2/9/2026, nhánh gui_sel · gui_sft_match) ──────────────
    # Hai nhánh đó được DẠY với khối ứng viên thay cho 24 dòng OCR. Chấm mà không
    # truyền `cands` là dựng câu nhắc KHÁC lúc dạy, và không có gì báo lỗi: mô hình
    # vẫn sinh ra chữ, thước vẫn chấm, chỉ là chấm một hệ thống chưa từng tồn tại.
    cands = {}
    if a.cands:
        with open(a.cands, encoding="utf-8") as f:
            for line in f:
                c = json.loads(line)
                cands[c["image"]] = c["cands"]
        print(f"khối ứng viên: {len(cands)} màn ← nhánh CÓ menu (gui_sel / gui_sft_match)")
    else:
        print("khối ứng viên: KHÔNG dùng ← nhánh giữ 24 dòng OCR "
              "(S1 · S2 · MIN-DESC · CE2 · gui_s1_match)")

    if a.only:
        gi = set()
        for line in open(a.only, encoding="utf-8"):
            o = json.loads(line)
            gi.add((str(o["episode_id"]), str(o["step_id"])))
        truoc = len(recs)
        recs = [r for r in recs
                if (str(r["episode_id"]), str(r["step_id"])) in gi]
        print(f"--only: {truoc} -> {len(recs)} bước (danh sách có {len(gi)} khoá)")
        assert recs, "DỪNG: --only lọc sạch mọi bước — nghi lệch kiểu khoá int/str"

    if a.limit:
        recs = recs[:a.limit]

    # ── FAIL-CLOSED KHỐI ỨNG VIÊN (vá 4/9/2026, report/134 §11) ───────────────────
    # Trước bản vá: `cands.get(image)` trả None im lặng khi thiếu khoá, câu nhắc tụt
    # về bản 24 dòng OCR và KHÔNG có gì báo lỗi — chấm một hệ thống chưa từng tồn tại.
    # Đúng dạng "lỗi câm" đã trả giá ngày 20/8. Kiểm ở đây, TRƯỚC khi nạp mô hình, để
    # hỏng thì hỏng trong 2 giây chứ không phải sau 5,6 giờ Kaggle.
    if a.cands:
        thieu = [r["image"] for r in recs if r["image"] not in cands]
        if thieu:
            sys.exit(f"DỪNG: {len(thieu)}/{len(recs)} bước không có khoá trong {a.cands} "
                     f"(ví dụ: {thieu[:3]}). Nhánh gui_sel/gui_sft_match được DẠY với khối "
                     f"ứng viên; thiếu khoá là dựng câu nhắc khác lúc dạy. Dựng lại "
                     f"candidates.jsonl bằng build_candidates.py --all-steps --max 40, "
                     f"hoặc bỏ --cands nếu cố ý chấm nhánh 24 dòng OCR.")
        print(f"khối ứng viên: phủ {len(recs)}/{len(recs)} bước — fail-closed ĐẠT")

    # ── NỐI TIẾP + XẢ ĐỆM (thêm 11/8/2026) ────────────────────────────────────────
    # Bản trước mở tệp ở chế độ "w" và không gọi flush. Máy ảo Colab bị thu hồi giữa
    # chừng — đã xảy ra HAI lần trong hai ngày, 10 và 11/8, cả hai lần đều ở khoảng 90%
    # công việc — là mất trắng cả lượt sinh câu 1,5 giờ. Chiến dịch có cả chục lượt
    # (4 nhánh × 2 hạt giống + trần gold/filler + B-infer + mô hình gốc), nên đây là
    # chỗ phơi nhiễm lớn nhất còn lại sau khi khâu OCR đã được vá.
    # Dòng ghi dở lúc mất điện bị loại hẳn khỏi tệp, không để lại giữa chừng — score_run
    # đọc bằng json.loads nên một dòng hỏng là hỏng cả lượt chấm.
    # Chữ ký của lượt chạy, đóng vào TỪNG bản ghi. Nối tiếp mà tệp cũ là của thí nghiệm
    # khác thì mọi bước đều "đã có", nó in "Xong sẵn" rồi thoát trong hai giây — trông y
    # như vừa chạy xong, mà thật ra chưa sinh câu nào cho thí nghiệm này. Chiến dịch có
    # cả chục lượt chỉ khác nhau vài cờ (2 hạt giống × 4 nhánh, trần gold/filler,
    # B-infer, mô hình gốc), toàn dùng chung một dòng lệnh chép qua chép lại.
    sig = ("base" if a.no_adapter else f"lora:{os.path.basename(str(a.adapter).rstrip('/'))}")
    if a.b_infer:
        sig += "+binfer"
    if a.ceiling:
        sig += f"+ceiling_{a.ceiling}"
    if a.force_sel:
        sig += "+forcesel"
    if a.save_conf:
        sig += "+conf"        # tệp ép chọn KHÔNG được nối tiếp vào tệp thường

    xong, sach = set(), []
    if os.path.exists(a.out):
        cu = []
        for line in open(a.out, encoding="utf-8"):
            try:
                o = json.loads(line)
            except Exception:
                continue
            xong.add((o["episode_id"], o["step_id"]))
            sach.append(line)
            cu.append(o)
        open(a.out, "w", encoding="utf-8").writelines(sach)
        khac = {o.get("run") for o in cu if o.get("run") and o["run"] != sig}
        if khac:
            sys.exit(f"⛔ {a.out} là của lượt chạy KHÁC: {sorted(khac)} ≠ {sig!r}.\n"
                     f"   Đổi --out, hoặc xoá tệp cũ nếu cố ý sinh lại.")
        if cu and not any("run" in o for o in cu):
            print(f"⚠️  {a.out} không có chữ ký lượt chạy (tệp sinh trước 12/8) — "
                  f"tự kiểm tra nó đúng là của {sig!r}.")
        recs = [r for r in recs if (r["episode_id"], r["step_id"]) not in xong]
        print(f"Nối tiếp: đã có {len(xong)} bước, còn {len(recs)}")
        if not recs:
            print(f"Xong sẵn {len(xong)} bước → {a.out}")
            return
    print(f"Nạp {a.base}" + (f" + LoRA {a.adapter}" if a.adapter else " (mô hình gốc)"))
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        a.base, device_map="auto", **dtype_kw())
    if a.adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.adapter)
    model.eval()
    # Ba chỗ phải khớp lúc dạy, sai một chỗ là điểm tụt mà không rõ vì sao:
    #  · ngân sách điểm ảnh: train_config.yaml đặt 200704/1003520; mặc định của
    #    processor là 12.845.056, lệch ~2,6 lần trên ảnh 1080x2400
    #  · đệm bên TRÁI: sinh theo lô mà đệm bên phải thì phần đệm nằm giữa câu nhắc
    #    và chỗ mô hình bắt đầu viết → lô 8 ra khác lô 1
    proc = AutoProcessor.from_pretrained(a.base, min_pixels=200704, max_pixels=1003520)
    proc.tokenizer.padding_side = "left"

    CEIL_DESCS = load_test_descriptors() if a.ceiling else {}
    if a.ceiling:
        thieu = sum(1 for r in recs if (r["episode_id"], r["step_id"]) not in CEIL_DESCS)
        print(f"Phép thử TRẦN ({a.ceiling}): có khai báo chuẩn cho "
              f"{len(recs)-thieu}/{len(recs)} bước; {thieu} bước giữ nguyên đầu vào.")

    # ── ÉP CHỌN (phép thử chẩn đoán) ─────────────────────────────────────────────
    # Cấm mọi cách viết "none" ⇒ mô hình buộc phải nêu tên một ứng viên. Câu hướng dẫn
    # có chứa chữ "none" sẽ bị chặn theo, nhưng đó là ca hiếm và phép thử này chỉ để
    # chẩn đoán, không phải để báo cáo điểm chính.
    NONE_IDS = []
    for w in ("none", " none", "None", " None", "NONE", " NONE"):
        ids = proc.tokenizer(w, add_special_tokens=False).input_ids
        if ids and ids not in NONE_IDS:
            NONE_IDS.append(ids)

    bad = None
    if a.force_sel:
        bad = []
        bad = list(NONE_IDS)
        print(f"ÉP CHỌN: cấm {len(bad)} chuỗi token của 'none'")

    out = open(a.out, "a", encoding="utf-8")
    t0, done = time.time(), 0
    for i in range(0, len(recs), a.batch):
        chunk = recs[i:i + a.batch]
        msgs, imgs = [], []
        for r in chunk:
            # tập kiểm dùng khoá gold_instruction; dựng bản ghi giống tập dạy để
            # câu nhắc đi qua đúng một hàm duy nhất
            rr = {"goal": r["goal"], "history": r.get("history") or []}
            im = Image.open(os.path.join(TEST, r["image"])).convert("RGB")
            imgs.append(im)
            # content dạng DANH SÁCH, không phải chuỗi: chat template của Qwen in
            # nguyên văn chuỗi "<image>" chứ không thay bằng token ảnh. "\n" đứng đầu
            # phần chữ để chuỗi render ra trùng đúng bản LLaMA-Factory dựng lúc dạy.
            # lưới an toàn thứ hai: phép kiểm phủ ở trên đã chặn, nhưng chỗ này là
            # chỗ lỗi câm sinh ra nên giữ luôn `assert`, đừng rút gọn về `.get()`.
            if a.cands:
                assert r["image"] in cands, f"thiếu khoá ứng viên: {r['image']}"
                cd = cands[r["image"]]
            else:
                cd = None
            body = prompt_body(rr, ocr.get(r["image"]), cands=cd)
            if a.b_infer:
                body = with_elements(body, r)
            if a.ceiling:
                body = with_ceiling(body, r, a.ceiling, CEIL_DESCS, proc.tokenizer)
            msgs.append([{"role": "system", "content": SYS},
                         {"role": "user", "content": [
                             {"type": "image"},
                             {"type": "text", "text": "\n" + body}]}])
        texts = [proc.apply_chat_template(m, tokenize=False, add_generation_prompt=True)
                 for m in msgs]
        inputs = proc(text=texts, images=imgs, return_tensors="pt",
                      padding=True).to(model.device)
        with torch.no_grad():
            # xem chú thích use_cache ở score_run.py — kiểm bằng 50/50 trùng tuyệt đối
            g_out = model.generate(**inputs, max_new_tokens=a.max_new, use_cache=True,
                                   do_sample=False, temperature=None, top_p=None,
                                   bad_words_ids=bad,
                                   output_scores=a.save_conf,
                                   return_dict_in_generate=a.save_conf)
            gen = g_out.sequences if a.save_conf else g_out

        # ── ĐIỂM TIN CẬY TẠI BƯỚC QUYẾT ĐỊNH ─────────────────────────────────
        # Bước quyết định = token đầu tiên sinh ra NGAY SAU khi chuỗi đã có "<sel>".
        # Đó là chỗ mô hình chọn giữa "none" và tên một ứng viên, nên p(none) ở đúng
        # bước ấy là điểm tin cậy cần cho đường risk-coverage.
        conf = [None] * len(chunk)
        if a.save_conf:
            for bi in range(len(chunk)):
                sinh = gen[bi][len(inputs["input_ids"][bi]):]
                buoc = None
                for t in range(min(len(sinh), len(g_out.scores))):
                    if "<sel>" in proc.decode(sinh[:t + 1], skip_special_tokens=True):
                        buoc = t + 1
                        break
                if buoc is None or buoc >= len(g_out.scores):
                    continue
                pr = torch.softmax(g_out.scores[buoc][bi].float(), dim=-1)
                # ⛔ KHỬ TRÙNG token đầu: "none" và "None" có thể cùng một token id, cộng
                #    thẳng theo danh sách chuỗi sẽ đếm hai lần và p_none vọt quá 1.
                #    Chỉ lấy token ĐẦU của mỗi cách viết vì bước quyết định chỉ có một token.
                pn = float(sum(pr[i] for i in {q[0] for q in NONE_IDS} if i < len(pr)))
                top = int(torch.argmax(pr))
                conf[bi] = {"p_none": round(pn, 5),
                            "p_top": round(float(pr[top]), 5),
                            "tok_top": proc.tokenizer.decode([top]),
                            "buoc_qd": buoc}
        for bi, (r, g, inp) in enumerate(zip(chunk, gen, inputs["input_ids"])):
            txt = proc.decode(g[len(inp):], skip_special_tokens=True)
            out.write(json.dumps({
                "episode_id": r["episode_id"], "step_id": r["step_id"],
                "image": r["image"], "app": r.get("app", ""),
                "gold_instruction": r["gold_instruction"], "action": r["action"],
                "raw": txt.strip(),            # nguyên văn, giữ để soi lỗi
                "pred": strip_desc(txt),       # câu đem chấm
                "conf": conf[bi],              # None nếu không bật --save-conf
                "run": sig,                    # chữ ký lượt chạy — xem khối nối tiếp
            }, ensure_ascii=False) + "\n")
        out.flush()          # mỗi lô một lần: mất máy thì mất nhiều nhất một lô
        done += len(chunk)
        if done % 80 < a.batch:
            sp = done / max(time.time() - t0, 1)
            print(f"  {done}/{len(recs)}  ({sp:.1f} bước/giây, còn ~{(len(recs)-done)/max(sp,.01)/60:.0f} phút)")
    out.close()
    print(f"Xong {done} bước → {a.out}")


if __name__ == "__main__":
    main()
