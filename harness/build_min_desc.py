# -*- coding: utf-8 -*-
"""Dựng tập cặp quy chiếu tối thiểu ở TẦNG KHAI BÁO (MIN-DESC) + tập đối chứng CE2-S2.

Nguyên tắc dựng: KHÔNG dựng lại câu nhắc. Lấy thẳng từ `branches/s2.json` rồi chỉ
thay ô <desc> ở vế bị loại. Như vậy prompt, đường dẫn ảnh và câu đích trùng
byte-với-byte nhánh S2 đã huấn luyện — hợp đồng đầu vào không thể lệch.

    chosen   = <desc>đúng</desc>    + "\\n" + câu người      (= đúng mẫu s2.json)
    rejected = <desc>desc_neg</desc> + "\\n" + câu người      (câu Y HỆT)

`desc_neg` do `descriptor_label_build.nearest_other()` dựng sẵn từ tháng 8.

Sinh ra hai tệp:
  · min_desc.json  — ranking, cho ORPO stage-2
  · ce2_s2.json    — SFT thuần trên đúng vế chosen của đúng những bước ấy.
                     Đây là đối chứng quy công: cùng bước, cùng số update, chỉ khác
                     mục tiêu. Cả hai đều KHÔNG trộn bước không-chạm (xem ghi chú
                     lệch chuẩn ở report/106) nên chênh lệch giữa chúng không thể
                     do khác dữ liệu.
"""
import json, os, re, sys, unicodedata, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
BR   = os.path.join(ROOT, "branches")
LO, HI = 80.0, 350.0
PT = re.compile(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>")
IMG = re.compile(r"ep(\d+)_s(\d+)\.png$")


def chuan(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def o_ten(d):
    o = (d or "").split("|")
    return o[1].strip() if len(o) >= 2 else ""


def hop_le(r):
    """Đúng sáu điều kiện đã khoá trước ở report/106 mục sửa đổi (x)."""
    d0, dn = r.get("desc"), r.get("desc_neg")
    if not d0 or not dn or d0.strip() == dn.strip():
        return False
    if chuan(o_ten(d0)) == chuan(o_ten(dn)):
        return False
    m0, mn = PT.search(d0), PT.search(dn)
    if not m0 or not mn or m0.group(0) == mn.group(0):
        return False
    kc = r.get("neighbor_dist_px")
    return kc is not None and LO <= float(kc) <= HI


def main():
    desc = {}
    with open(os.path.join(ROOT, "descriptors.jsonl"), encoding="utf-8") as f:
        for l in f:
            d = json.loads(l)
            desc[os.path.basename(d["image"])] = d

    s2 = json.load(open(os.path.join(BR, "s2.json"), encoding="utf-8"))
    print(f"nạp: {len(desc)} khai báo · {len(s2)} mẫu s2")

    cap, ce2 = [], []
    bo = collections.Counter()
    for m in s2:
        ten_anh = os.path.basename(m["images"][0])
        r = desc.get(ten_anh)
        if r is None:
            bo["khong_co_khai_bao"] += 1
            continue
        if not hop_le(r):
            bo["truot_dieu_kien"] += 1
            continue
        chosen = m["messages"][2]["content"]
        # bất biến ①: mẫu s2 phải đúng dạng <desc>…</desc>\ncâu, và khai báo phải
        # trùng đúng bản trong descriptors.jsonl. Lệch một ký tự là dừng — nghĩa là
        # hai tệp đến từ hai lần dựng khác nhau.
        if not chosen.startswith(r["desc"] + "\n"):
            bo["s2_khong_khop_khai_bao"] += 1
            continue
        cau = chosen[len(r["desc"]) + 1:]
        rejected = r["desc_neg"] + "\n" + cau
        goc = {"messages": m["messages"][:2], "images": m["images"]}
        cap.append({**goc,
                    "chosen":   {"role": "assistant", "content": chosen},
                    "rejected": {"role": "assistant", "content": rejected}})
        ce2.append({"messages": m["messages"][:2] +
                                [{"role": "assistant", "content": chosen}],
                    "images": m["images"]})

    print(f"\ncặp dựng được: {len(cap)}")
    for k, v in bo.most_common():
        print(f"  bỏ · {k:<26}{v}")

    # ── bảy bất biến, dừng hẳn nếu trượt ─────────────────────────────────────
    print("\nBẤT BIẾN")
    kt = []
    kt.append(("① chosen ≠ rejected ở mọi cặp",
               all(c["chosen"]["content"] != c["rejected"]["content"] for c in cap)))
    kt.append(("② hai vế cùng bắt đầu bằng <desc>",
               all(c["chosen"]["content"].startswith("<desc>")
                   and c["rejected"]["content"].startswith("<desc>") for c in cap)))
    kt.append(("③ CÂU sau \\n trùng nhau tuyệt đối",
               all(c["chosen"]["content"].split("\n", 1)[1]
                   == c["rejected"]["content"].split("\n", 1)[1] for c in cap)))
    kt.append(("④ ô TÊN hai vế khác nhau",
               all(chuan(o_ten(c["chosen"]["content"])) !=
                   chuan(o_ten(c["rejected"]["content"])) for c in cap)))
    kt.append(("⑤ ô POINT hai vế khác nhau",
               all(PT.search(c["chosen"]["content"]).group(0) !=
                   PT.search(c["rejected"]["content"]).group(0) for c in cap)))
    kt.append(("⑥ prompt + ảnh trùng CE2 từng dòng",
               all(a["messages"][:2] == b["messages"][:2] and a["images"] == b["images"]
                   for a, b in zip(cap, ce2))))
    kt.append(("⑦ CE2 học đúng vế chosen",
               all(b["messages"][2]["content"] == a["chosen"]["content"]
                   for a, b in zip(cap, ce2))))
    for nhan, ok in kt:
        print(f"  {'✅' if ok else '⛔'} {nhan}")
    if not all(ok for _, ok in kt):
        sys.exit("⛔ DỪNG — có bất biến trượt, không ghi tệp.")

    # ── phân bố lệch độ dài (chống shortcut độ dài) ──────────────────────────
    dl = [len(c["chosen"]["content"]) - len(c["rejected"]["content"]) for c in cap]
    dl.sort()
    trong2 = sum(1 for x in dl if abs(x) <= 8)   # ~2 token ≈ 8 ký tự
    print(f"\nlệch độ dài chosen−rejected (ký tự): trung vị {dl[len(dl)//2]:+d} · "
          f"p05 {dl[len(dl)//20]:+d} · p95 {dl[19*len(dl)//20]:+d}")
    print(f"  trong ±8 ký tự: {100*trong2/len(dl):.1f}%  "
          f"→ đây KHÔNG phải cặp ghép độ dài; phải chạy probe độ dài ở Mục 12.3")

    # 200 cặp NẶNG NHẤT cho ô thăm dò bộ nhớ. Nặng = tổng token của cả hai vế, vì ORPO
    # forward cả chosen lẫn rejected trong một bước. Bài học P10: cấu hình chạy ngọt trên
    # mẫu thường vẫn chết trên mẫu dài nhất, và probe trên mẫu ĐẦU TẬP không kết luận được.
    nang = sorted(cap, key=lambda c: -(len(c["chosen"]["content"])
                                       + len(c["rejected"]["content"])))[:200]
    print(f"\n200 cặp nặng nhất: tổng ký tự hai vế "
          f"{len(nang[0]['chosen']['content'])+len(nang[0]['rejected']['content'])} "
          f"… {len(nang[-1]['chosen']['content'])+len(nang[-1]['rejected']['content'])}")

    for ten, dat in (("min_desc.json", cap), ("ce2_s2.json", ce2),
                     ("min_desc_long.json", nang)):
        p = os.path.join(BR, ten)
        json.dump(dat, open(p, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"\nghi {p}  ({os.path.getsize(p)/2**20:.1f} MB)")

    info = json.load(open(os.path.join(BR, "dataset_info.json"), encoding="utf-8"))
    tags = {"role_tag": "role", "content_tag": "content", "user_tag": "user",
            "assistant_tag": "assistant", "system_tag": "system"}
    info["gui_min_desc"] = {
        "file_name": "min_desc.json", "formatting": "sharegpt", "ranking": True,
        "columns": {"messages": "messages", "chosen": "chosen",
                    "rejected": "rejected", "images": "images"}, "tags": tags}
    info["gui_min_desc_long"] = {
        "file_name": "min_desc_long.json", "formatting": "sharegpt", "ranking": True,
        "columns": {"messages": "messages", "chosen": "chosen",
                    "rejected": "rejected", "images": "images"}, "tags": tags}
    info["gui_ce2_s2"] = {
        "file_name": "ce2_s2.json", "formatting": "sharegpt",
        "columns": {"messages": "messages", "images": "images"}, "tags": tags}
    json.dump(info, open(os.path.join(BR, "dataset_info.json"), "w",
                         encoding="utf-8"), ensure_ascii=False, indent=1)
    print("cập nhật dataset_info.json → gui_min_desc · gui_min_desc_long · gui_ce2_s2")


if __name__ == "__main__":
    main()
