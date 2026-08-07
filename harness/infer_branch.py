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
    """
    if "</desc>" in s:
        s = s.split("</desc>", 1)[1]
    elif "<desc>" in s:
        s = re.sub(r"<desc>.*", "", s, flags=re.S)
    return s.strip().split("\n")[0].strip()


VISION = "<|vision_start|><|image_pad|><|vision_end|>"

def pick_dtype():
    """Chọn kiểu số theo card ĐANG CÓ, đừng ép bf16.

    A100 có bf16; T4 (Turing) và P100 (Pascal) — hai card của Colab/Kaggle bản miễn phí —
    thì KHÔNG. Ép bf16 ở đó sẽ lỗi hoặc rơi vào đường giả lập chậm khủng khiếp, rồi ta
    ngồi đổ oan cho bộ trỏ hay cho mô hình. Với suy luận, fp16 không đổi kết luận.
    """
    import torch
    if not torch.cuda.is_available():
        return torch.float32
    return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16


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
        a.base, torch_dtype=pick_dtype(), device_map="auto")
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
            g = model.generate(**inp, max_new_tokens=a.max_new, do_sample=False)
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
    ap.add_argument("--selftest", action="store_true",
                    help="kiểm câu nhắc khớp lúc dạy (CPU, không cần mô hình)")
    ap.add_argument("--b-infer", action="store_true",
                    help="nhánh B-infer: nối DANH SÁCH phần tử của màn vào đầu vào lúc chạy "
                         "(không đánh dấu đích, không dùng toạ độ chuẩn). Dùng với trọng số S1.")
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
    if a.limit:
        recs = recs[:a.limit]

    print(f"Nạp {a.base}" + (f" + LoRA {a.adapter}" if a.adapter else " (mô hình gốc)"))
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        a.base, torch_dtype=pick_dtype(), device_map="auto")
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

    out = open(a.out, "w", encoding="utf-8")
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
            body = prompt_body(rr, ocr.get(r["image"]))
            if a.b_infer:
                body = with_elements(body, r)
            msgs.append([{"role": "system", "content": SYS},
                         {"role": "user", "content": [
                             {"type": "image"},
                             {"type": "text", "text": "\n" + body}]}])
        texts = [proc.apply_chat_template(m, tokenize=False, add_generation_prompt=True)
                 for m in msgs]
        inputs = proc(text=texts, images=imgs, return_tensors="pt",
                      padding=True).to(model.device)
        with torch.no_grad():
            gen = model.generate(**inputs, max_new_tokens=a.max_new,
                                 do_sample=False, temperature=None, top_p=None)
        for r, g, inp in zip(chunk, gen, inputs["input_ids"]):
            txt = proc.decode(g[len(inp):], skip_special_tokens=True)
            out.write(json.dumps({
                "episode_id": r["episode_id"], "step_id": r["step_id"],
                "image": r["image"], "app": r.get("app", ""),
                "gold_instruction": r["gold_instruction"], "action": r["action"],
                "raw": txt.strip(),            # nguyên văn, giữ để soi lỗi
                "pred": strip_desc(txt),       # câu đem chấm
            }, ensure_ascii=False) + "\n")
        done += len(chunk)
        if done % 80 < a.batch:
            sp = done / max(time.time() - t0, 1)
            print(f"  {done}/{len(recs)}  ({sp:.1f} bước/giây, còn ~{(len(recs)-done)/max(sp,.01)/60:.0f} phút)")
    out.close()
    print(f"Xong {done} bước → {a.out}")


if __name__ == "__main__":
    main()
