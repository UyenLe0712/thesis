# -*- coding: utf-8 -*-
"""Dựng nhánh `gui_sel_cham` / `gui_sft_match_cham` — bỏ bước KHÔNG-CHẠM khỏi tập dạy.

VÌ SAO
------
Đo 5/9/2026 (`report/136` mục 11): nhãn `<sel>none</sel>` chiếm **54,78%** tập dạy, nhưng
trên riêng bước CHẠM — loại bước duy nhất được chấm — nó chỉ là **29,1%**, khớp tập kiểm
(28,34%) tới 0,8 pp. Mà mô hình phát ra **41,97%**, nằm giữa hai con số và nghiêng về
prior của toàn tập.

Nguyên do: `build_sel_data` gắn `<sel>none</sel>` cho MỌI bước không-chạm (vuốt, quay
lại, gõ chữ, mở ứng dụng), và nhóm đó chiếm 36,2% tập dạy. Bỏ nhóm đó ra thì prior của
nhãn chọn về đúng 29,1%.

CÁCH LÀM — lọc theo CHỈ SỐ, không dựng lại từ đầu
-------------------------------------------------
`build_sel_data.py` duyệt `train.jsonl` tuần tự và `append` từng dòng, không lọc bản ghi
nào (kiểm ở bất biến ① của chính nó: `len(sel_rows) == len(recs)`). Nên dòng thứ i của
`gui_sel.json` ứng đúng bản ghi thứ i của `train.jsonl`. Lọc bằng chỉ số vừa rẻ vừa
không có cơ hội lệch lượt OCR hay lệch lượt dựng khối ứng viên — thứ đã đắt một lần rồi.

    python harness/make_sel_cham.py

⛔ KHÔNG đổi câu nhắc, không đổi khối ứng viên, không đổi cách viết thẻ. Đúng một biến
đổi: tập mẫu.
"""
import os, sys, json, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
BR = os.path.join(ROOT, "branches")


def la_cham(r):
    a = r["action"]
    return a.get("action_type") in ("click", "long_press") and "x" in a


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8")]
    sel = json.load(open(os.path.join(BR, "gui_sel.json"), encoding="utf-8"))
    ctl = json.load(open(os.path.join(BR, "gui_sft_match.json"), encoding="utf-8"))
    print(f"nguồn: {len(recs)} bản ghi · {len(sel)} dòng gui_sel · {len(ctl)} dòng đối chứng")
    assert len(recs) == len(sel) == len(ctl), (
        "DỪNG: ba tệp không cùng số dòng — giả định 'khớp theo chỉ số' không còn đúng, "
        "phải dựng lại bằng build_sel_data.py thay vì lọc.")

    giu = [i for i, r in enumerate(recs) if la_cham(r)]
    sel_c = [sel[i] for i in giu]
    ctl_c = [ctl[i] for i in giu]

    def tgt(x):
        return [m["content"] for m in x["messages"] if m["role"] == "assistant"][0]

    def prompt(x):
        return (json.dumps([m for m in x["messages"] if m["role"] != "assistant"],
                           ensure_ascii=False) + "|" + json.dumps(x["images"]))

    st = collections.Counter()
    st["none_truoc"] = sum(1 for x in sel if tgt(x).startswith("<sel>none</sel>"))
    st["none_sau"] = sum(1 for x in sel_c if tgt(x).startswith("<sel>none</sel>"))

    # ── BẤT BIẾN — trượt một cái là dừng, không ghi tệp ──────────────────────────
    kt = []
    kt.append(("① số dòng giữ lại = số bước chạm trong train.jsonl",
               len(sel_c) == len(ctl_c) == sum(1 for r in recs if la_cham(r))))
    kt.append(("② ảnh của dòng giữ lại khớp bản ghi nguồn",
               all(sel_c[j]["images"] == [x for x in [sel[i]["images"][0]]]
                   for j, i in enumerate(giu))))
    kt.append(("③ prompt hai nhánh vẫn TRÙNG BYTE trên toàn tập mới",
               all(prompt(a) == prompt(b) for a, b in zip(sel_c, ctl_c))))
    kt.append(("④ target hai nhánh KHÁC nhau ở mọi dòng",
               all(tgt(a) != tgt(b) for a, b in zip(sel_c, ctl_c))))
    kt.append(("⑤ nhánh đối chứng không còn thẻ <sel> nào",
               all("<sel>" not in tgt(b) for b in ctl_c)))
    kt.append(("⑥ mọi dòng nhánh chọn đều mở đầu bằng thẻ <sel>",
               all(tgt(a).startswith("<sel>") for a in sel_c)))
    kt.append(("⑦ tỉ lệ none về đúng dải bước chạm (28-31%)",
               0.28 <= st["none_sau"] / len(sel_c) <= 0.31))
    for ten, ok in kt:
        print(("  ✅ " if ok else "  ⛔ ") + ten)
    assert all(ok for _, ok in kt), "DỪNG: có bất biến trượt, không ghi tệp"

    for ten, rows in (("gui_sel_cham", sel_c), ("gui_sft_match_cham", ctl_c)):
        p = os.path.join(BR, ten + ".json")
        json.dump(rows, open(p, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"  ghi {p}  {os.path.getsize(p):,} byte  sha256 {sha(p)[:32]}…")

    info_p = os.path.join(BR, "dataset_info.json")
    info = json.load(open(info_p, encoding="utf-8"))
    for ten in ("gui_sel_cham", "gui_sft_match_cham"):
        info[ten] = {"file_name": ten + ".json", "formatting": "sharegpt",
                     "columns": {"messages": "messages", "images": "images"},
                     "tags": {"role_tag": "role", "content_tag": "content",
                              "user_tag": "user", "assistant_tag": "assistant",
                              "system_tag": "system"}}
    json.dump(info, open(info_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    n = len(sel_c)
    print(f"\nTẬP MỚI: {n:,} mẫu (bỏ {len(sel) - n:,} bước không-chạm = "
          f"{(len(sel) - n) / len(sel) * 100:.1f}%)")
    print(f"  nhãn none : {st['none_truoc']:,}/{len(sel):,} = {st['none_truoc']/len(sel)*100:.2f}%"
          f"  ->  {st['none_sau']:,}/{n:,} = {st['none_sau']/n*100:.2f}%")
    import math
    print(f"  số bước train 1 epoch, lô hiệu dụng 16: {math.ceil(n/16)} "
          f"(bản cũ {math.ceil(len(sel)/16)})")


if __name__ == "__main__":
    main()
