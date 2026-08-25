# -*- coding: utf-8 -*-
"""PHƯƠNG ÁN ② — MIN-DESC có TRỘN bước không-chạm (chưa đăng ký, chưa train).

Vì sao có file này: đo 24/8 (`report/106` mục **x3e**) cho thấy stage-2 chỉ-có-bước-chạm làm
`action_ok` trên bước KHÔNG-chạm tụt **−20 pp** (83,5% → 63,8%), và CE2 tụt y hệt ⇒ nguyên nhân
là **thiếu dữ liệu không-chạm**, không phải ORPO. `report/116` Mục 12.5 đã đòi trộn ngay từ đầu;
mục **(x7) điểm 2** khai là đã cố ý bỏ. File này dựng bản CÓ trộn.

CÁCH TRỘN — mấu chốt nằm ở đây:

    bước CHẠM      : chosen = <desc>đúng</desc>\\n câu   ·  rejected = <desc>desc_neg</desc>\\n câu
    bước KHÔNG-chạm: chosen = câu trần               ·  rejected = **Y HỆT chosen**

Đặt `rejected == chosen` cho bước không-chạm là có chủ đích, không phải cẩu thả:

  · Số hạng ưu tiên của ORPO là `-log σ(log_odds(chosen) - log_odds(rejected))`. Hai vế giống hệt
    nhau thì hiệu bằng 0 **với mọi tham số**, nên đạo hàm của nó bằng 0. Dòng đó chỉ còn đóng góp
    số hạng SFT trên `chosen` — tức **đúng bằng CE thuần**, đúng thứ Mục 12.5 yêu cầu.
  · Vì sao KHÔNG đặt `rejected = <desc>…</desc> + câu` (tức "hành vi sai" mà model đang mắc):
    làm vậy thì mọi cặp không-chạm đều có vế bị loại **dài hơn**, và luật "chọn vế ngắn hơn" sẽ
    đoán đúng ~68% toàn tập — **vượt ngưỡng shortcut 55%** ở (x6), tức tự trượt cổng của chính
    mình. Với `chosen == rejected` thì hai vế hoà, probe không đọc được gì.

⚠️ **PHẢI SMOKE TRƯỚC.** Chưa biết LLaMA-Factory/TRL có chấp nhận dòng `chosen == rejected` không;
có thể nó `assert` hoặc chia cho 0 ở đâu đó. Chạy 20 bước trên tập này trước khi train thật.

Sinh ra: `min_desc_mix.json` (ranking) · `ce2_s2_mix.json` (SFT, cùng bước, học vế chosen).
"""
import json, os, re, sys, random, unicodedata, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
BR   = os.path.join(ROOT, "branches")
LO, HI = 80.0, 350.0
SEED = 20260805                      # hạt giống chung của mọi phép lấy mẫu, report/106 mục 10
PT = re.compile(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>")


def chuan(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def o_ten(d):
    o = (d or "").split("|")
    return o[1].strip() if len(o) >= 2 else ""


def hop_le(r):
    """Đúng sáu điều kiện đã khoá ở (x3) — giữ nguyên, không nới."""
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

    cap, kho_khong_cham = [], []
    for m in s2:
        r = desc.get(os.path.basename(m["images"][0]))
        goc = {"messages": m["messages"][:2], "images": m["images"]}
        noi = m["messages"][2]["content"]
        if r is None:                                   # bước KHÔNG-chạm
            kho_khong_cham.append({**goc,
                "chosen":   {"role": "assistant", "content": noi},
                "rejected": {"role": "assistant", "content": noi}})
            continue
        if not hop_le(r) or not noi.startswith(r["desc"] + "\n"):
            continue
        cau = noi[len(r["desc"]) + 1:]
        cap.append({**goc,
                    "chosen":   {"role": "assistant", "content": noi},
                    "rejected": {"role": "assistant", "content": r["desc_neg"] + "\n" + cau}})

    # ── tỉ lệ tự nhiên của tập dạy, Mục 12.5 ─────────────────────────────────
    n_cham_goc = sum(1 for m in s2 if desc.get(os.path.basename(m["images"][0])))
    n_khac_goc = len(s2) - n_cham_goc
    ti = n_khac_goc / n_cham_goc
    n_lay = min(round(len(cap) * ti), len(kho_khong_cham))
    random.Random(SEED).shuffle(kho_khong_cham)
    khong_cham = kho_khong_cham[:n_lay]

    print(f"\ntỉ lệ tự nhiên tập dạy : {n_cham_goc} chạm / {n_khac_goc} khác = 1 : {ti:.3f}")
    print(f"cặp tầng khai báo      : {len(cap)}")
    print(f"bước không-chạm lấy vào: {n_lay}  (kho có {len(kho_khong_cham)})")
    tron = cap + khong_cham
    random.Random(SEED).shuffle(tron)
    ce2 = [{"messages": x["messages"] + [x["chosen"]], "images": x["images"]} for x in tron]
    print(f"tổng dòng              : {len(tron)}"
          f"  ({100*len(cap)/len(tron):.1f}% chạm · {100*n_lay/len(tron):.1f}% không-chạm)")

    # ── bất biến ─────────────────────────────────────────────────────────────
    print("\nBẤT BIẾN")
    co_desc = lambda x: x["chosen"]["content"].startswith("<desc>")
    kt = [
        ("① dòng CHẠM: chosen ≠ rejected, cả hai có <desc>",
         all(x["chosen"]["content"] != x["rejected"]["content"]
             and x["rejected"]["content"].startswith("<desc>") for x in tron if co_desc(x))),
        ("② dòng KHÔNG-chạm: chosen == rejected, KHÔNG có <desc>",
         all(x["chosen"]["content"] == x["rejected"]["content"]
             and "<desc>" not in x["rejected"]["content"] for x in tron if not co_desc(x))),
        ("③ dòng CHẠM: CÂU sau \\n trùng nhau tuyệt đối",
         all(x["chosen"]["content"].split("\n", 1)[1] == x["rejected"]["content"].split("\n", 1)[1]
             for x in tron if co_desc(x))),
        ("④ dòng CHẠM: ô TÊN hai vế khác nhau",
         all(chuan(o_ten(x["chosen"]["content"])) != chuan(o_ten(x["rejected"]["content"]))
             for x in tron if co_desc(x))),
        ("⑤ CE2 học đúng vế chosen, cùng prompt + ảnh",
         all(a["messages"][:2] == b["messages"][:2] and a["images"] == b["images"]
             and b["messages"][2]["content"] == a["chosen"]["content"]
             for a, b in zip(tron, ce2))),
        ("⑥ số dòng chạm khớp số cặp dựng được",
         sum(1 for x in tron if co_desc(x)) == len(cap)),
    ]
    for nhan, ok in kt:
        print(f"  {'✅' if ok else '⛔'} {nhan}")
    if not all(o for _, o in kt):
        sys.exit("⛔ DỪNG — có bất biến trượt, không ghi tệp.")

    # ── probe shortcut độ dài, tính ngay tại chỗ ─────────────────────────────
    dai = ngan = hoa = 0
    for x in tron:
        d = len(x["chosen"]["content"]) - len(x["rejected"]["content"])
        dai += d > 0; ngan += d < 0; hoa += d == 0
    n = len(tron)
    print(f"\nprobe độ dài: chosen dài hơn {100*dai/n:.1f}% · ngắn hơn {100*ngan/n:.1f}%"
          f" · hoà {100*hoa/n:.1f}%")
    tot = max(dai, ngan) + hoa * 0.5
    print(f"  luật 'chọn vế dài hơn' đoán đúng {100*tot/n:.1f}%"
          f"  {'✅ dưới' if tot/n < .55 else '⛔ VƯỢT'} ngưỡng shortcut 55% ở (x6)")

    for ten, dat in (("min_desc_mix.json", tron), ("ce2_s2_mix.json", ce2)):
        p = os.path.join(BR, ten)
        json.dump(dat, open(p, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"\nghi {p}  ({os.path.getsize(p)/2**20:.1f} MB)")

    info = json.load(open(os.path.join(BR, "dataset_info.json"), encoding="utf-8"))
    tags = {"role_tag": "role", "content_tag": "content", "user_tag": "user",
            "assistant_tag": "assistant", "system_tag": "system"}
    info["gui_min_desc_mix"] = {
        "file_name": "min_desc_mix.json", "formatting": "sharegpt", "ranking": True,
        "columns": {"messages": "messages", "chosen": "chosen",
                    "rejected": "rejected", "images": "images"}, "tags": tags}
    info["gui_min_desc_mix_long"] = {
        "file_name": "min_desc_mix_long.json", "formatting": "sharegpt", "ranking": True,
        "columns": {"messages": "messages", "chosen": "chosen",
                    "rejected": "rejected", "images": "images"}, "tags": tags}
    info["gui_ce2_s2_mix"] = {
        "file_name": "ce2_s2_mix.json", "formatting": "sharegpt",
        "columns": {"messages": "messages", "images": "images"}, "tags": tags}
    json.dump(info, open(os.path.join(BR, "dataset_info.json"), "w",
                         encoding="utf-8"), ensure_ascii=False, indent=1)

    # 200 dòng nặng nhất + BẮT BUỘC có cả hai loại, để smoke bắt được lỗi chosen==rejected
    nang = sorted(tron, key=lambda x: -(len(x["chosen"]["content"])
                                        + len(x["rejected"]["content"])))
    lay = [x for x in nang if co_desc(x)][:150] + [x for x in nang if not co_desc(x)][:50]
    json.dump(lay, open(os.path.join(BR, "min_desc_mix_long.json"), "w",
                        encoding="utf-8"), ensure_ascii=False)
    print(f"ghi min_desc_mix_long.json — {len(lay)} dòng "
          f"({sum(1 for x in lay if co_desc(x))} chạm · {sum(1 for x in lay if not co_desc(x))} "
          f"không-chạm, để smoke chạm được nhánh chosen==rejected)")
    print("cập nhật dataset_info.json → gui_min_desc_mix · gui_min_desc_mix_long · gui_ce2_s2_mix")


if __name__ == "__main__":
    main()
