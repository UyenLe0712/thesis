# -*- coding: utf-8 -*-
"""MIN-ONPOLICY — dựng cặp ORPO với vế âm là lỗi CHÍNH S2 mắc, đã ĐÚC LẠI.

Đăng ký trước ở `report/106` mục (x11). Đổi đúng MỘT thứ so với `build_min_desc.py`:
nguồn của `desc_neg`.

    heuristic:  desc_neg = nearest_other()  — ta ĐOÁN mô hình nhầm sang phần tử nào
    on-policy:  desc_neg = phần tử mà S2 THẬT SỰ chọn nhầm, đúc lại bằng desc_str()

⛔ VÌ SAO PHẢI ĐÚC LẠI, KHÔNG LẤY CHUỖI THÔ — (x11b):
D'Oosterlinck et al., TACL 13 (2025), dựng tập `Stronger Preferred` đúng bằng cấu trúc ngây
thơ (rejected = mô hình đích tự sinh, chosen = nguồn khác). Đó là tập DUY NHẤT trong bốn tập
của họ cho số âm sâu: MaxΔ −5,00, MeanΔ −6,94. Mô hình học ĐẶC TRƯNG NGUỒN thay vì nội dung.
Đúc lại bằng `desc_str()` — chính hàm đã dựng nhãn vàng — làm hai vế cùng khuôn, chỉ khác
danh tính phần tử. On-policy về NỘI DUNG lỗi, off-policy về HÌNH THỨC.

Đầu vào:
  · `desc_train_s2.jsonl`  do `sinh_desc_train.py` sinh (S2 tự sinh khai báo trên màn tập dạy)
  · `descriptors.jsonl`    nhãn vàng tập dạy
  · `branches/s2.json`     để lấy đúng câu nhắc + câu đích
  · cây trợ năng qua `a11y_inventory` (tải từ HuggingFace lần đầu)

Sinh ra: `min_desc_onpolicy.json` (ranking) · `ce2_onpolicy.json` (SFT, CÙNG bước, học vế chosen).
Và in ba cổng của (x11c). Không có cờ nào tắt bớt cổng.

    python3 harness/build_min_desc_onpolicy.py desc_train_s2.jsonl
"""
import json, os, re, sys, math, collections, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
BR   = os.path.join(ROOT, "branches")
LO, HI = 80.0, 350.0          # cùng dải với hop_le() của build_min_desc.py — (x11c) cổng ②
W_SCREEN, H_SCREEN = 1080, 2400
PT = re.compile(r"<point>\s*(\d+)\s*,\s*(\d+)\s*</point>")


def chuan(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def o_ten(d):
    o = (d or "").split("|")
    return o[1].strip() if len(o) >= 2 else ""


def khoa_anh(p):
    t = os.path.basename(p)
    if not t.startswith("ep") or "_s" not in t:
        return None
    a, b = t[2:].split("_s", 1)
    try:
        return int(a), int(b.split(".")[0])
    except ValueError:
        return None


def diem_pixel(desc):
    """Ô <point> ở thang norm-1000 → pixel màn tham chiếu."""
    m = PT.search(desc or "")
    if not m:
        return None
    return (int(m.group(1)) / 1000.0 * W_SCREEN, int(m.group(2)) / 1000.0 * H_SCREEN)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "desc_train_s2.jsonl"
    if not os.path.exists(src):
        sys.exit(f"⛔ không thấy {src} — chạy sinh_desc_train.py trước")

    import a11y_inventory as A11Y
    from descriptor_label_build import (nodes_of, name_of, distinguish, desc_str,
                                        ROLE, GENERIC, overlapped)

    gold = {}
    with open(os.path.join(ROOT, "descriptors.jsonl"), encoding="utf-8") as f:
        for l in f:
            d = json.loads(l)
            gold[(d["episode_id"], d["step_id"])] = d

    ocr = {}
    with open(os.path.join(ROOT, "ocr.jsonl"), encoding="utf-8") as f:
        for l in f:
            o = json.loads(l)
            ocr[os.path.basename(o["image"])] = o

    pred = {}
    with open(src, encoding="utf-8") as f:
        for l in f:
            o = json.loads(l)
            pred[(o["ep"], o["step"])] = o

    s2 = json.load(open(os.path.join(BR, "s2.json"), encoding="utf-8"))
    print(f"nạp: {len(gold)} nhãn vàng · {len(pred)} khai báo S2 tự sinh · {len(s2)} mẫu s2")

    cap, ce2, bo = [], [], collections.Counter()
    kc_gold, tach_bang_chuoi = [], collections.Counter()

    for m in s2:
        k = khoa_anh(m["images"][0])
        g = gold.get(k) if k else None
        p = pred.get(k) if k else None
        if g is None or p is None:
            bo["thieu_du_lieu"] += 1; continue
        d0 = g.get("desc")
        if not d0 or not p.get("desc_pred"):
            bo["thieu_khai_bao"] += 1; continue

        # ① mô hình có SAI TÊN thật không (không lồng nhau)
        gt, mt = chuan(o_ten(d0)), chuan(o_ten(p["desc_pred"]))
        if not gt or gt == "no name":
            bo["gold_khong_ten"] += 1; continue
        if mt and (mt == gt or mt in gt or gt in mt):
            bo["s2_da_dung_ten"] += 1; continue

        # ② quy ô <point> của mô hình về pixel, dùng ĐÚNG cỡ màn của bước đó
        pa, pn = g.get("point_abs"), g.get("point_norm")
        if not pa or not pn or not pn[0] or not pn[1]:
            bo["thieu_moc_quy_doi"] += 1; continue
        w = pa[0] * 1000.0 / pn[0]
        h = pa[1] * 1000.0 / pn[1]
        mm = PT.search(p["desc_pred"])
        if not mm:
            bo["thieu_point"] += 1; continue
        pp = (int(mm.group(1)) / 1000.0 * w, int(mm.group(2)) / 1000.0 * h)
        kc = math.dist((float(pa[0]), float(pa[1])), pp)
        kc_gold.append(kc)
        if not (LO <= kc <= HI):
            bo["ngoai_dai_80_350"] += 1; continue   # cổng (x11c)② — chặn FALSE NEGATIVE

        # ③ ĐÚC LẠI bằng ĐÚNG chuỗi hàm đã dựng nhãn vàng (descriptor_label_build:362-381)
        rel = f"episode_{k[0]}_screenshot_{k[1]}.png"
        nds = nodes_of(rel)
        if not nds:
            bo["khong_co_cay_tro_nang"] += 1; continue
        gbox = g.get("box")
        cont = [t for t in nds if t[0][0] <= pp[0] <= t[0][2] and t[0][1] <= pp[1] <= t[0][3]]
        if cont:                       # hộp NHỎ NHẤT chứa điểm — cùng luật với nhãn vàng
            nb, ncls, nnm = min(cont, key=lambda t: (t[0][2]-t[0][0]) * (t[0][3]-t[0][1]))
        else:                          # không hộp nào chứa ⇒ lấy hộp gần nhất
            nb, ncls, nnm = min(nds, key=lambda t: math.dist(
                ((t[0][0]+t[0][2])/2, (t[0][1]+t[0][3])/2), pp))
        if gbox and overlapped(nb, tuple(gbox)):
            bo["node_chong_lan_gold"] += 1; continue   # cùng phần tử ⇒ false negative

        ocr_rec = ocr.get(os.path.basename(m["images"][0]))
        nshare = (nb[2]-nb[0]) * (nb[3]-nb[1]) / max(w*h, 1)
        nname, _ = name_of(nb, nnm, ocr_rec, nshare)
        if not nname:
            bo["node_khong_dat_ten_duoc"] += 1; continue
        ncx, ncy = int(round((nb[0]+nb[2])/2)), int(round((nb[1]+nb[3])/2))
        npt = (int(round(ncx/max(w,1)*1000)), int(round(ncy/max(h,1)*1000)))
        nrole = ROLE.get(ncls) or ("item" if ncls in GENERIC else "element")
        nhint, _, _ = distinguish(nb, ncls, nname, nds, ocr_rec)
        dn = desc_str(nrole, nname, npt, nhint)

        if chuan(o_ten(dn)) == gt or dn.strip() == d0.strip():
            bo["duc_lai_trung_gold"] += 1; continue

        chosen = m["messages"][2]["content"]
        if not chosen.startswith(d0 + "\n"):
            bo["s2_khong_khop_khai_bao"] += 1; continue
        cau = chosen[len(d0) + 1:]
        goc = {"messages": m["messages"][:2], "images": m["images"]}
        cap.append({**goc,
                    "chosen":   {"role": "assistant", "content": chosen},
                    "rejected": {"role": "assistant", "content": dn + "\n" + cau}})
        ce2.append({"messages": m["messages"][:2] +
                                [{"role": "assistant", "content": chosen}],
                    "images": m["images"]})
        for chuoi in ("(no name)",):
            if (chuoi in d0) != (chuoi in dn):
                tach_bang_chuoi[chuoi] += 1

    print(f"\ncặp dựng được: {len(cap)}")
    for kk, v in bo.most_common():
        print(f"  bỏ · {kk:<26} {v}")
    if kc_gold:
        kc_gold.sort()
        print(f"\nkhoảng cách phần tử-nhầm ↔ gold (px): trung vị {kc_gold[len(kc_gold)//2]:.0f}"
              f" · p25 {kc_gold[len(kc_gold)//4]:.0f} · p75 {kc_gold[3*len(kc_gold)//4]:.0f}")

    if not cap:
        sys.exit("⛔ 0 cặp — dừng, không ghi tệp.")

    # ══ BA CỔNG CỦA (x11c) — không có cờ tắt bớt ══
    print("\n" + "=" * 62)
    print("CỔNG (x11c) — trượt bất kỳ cổng nào thì DỪNG, không train")
    print("=" * 62)

    ngan = sum(1 for c in cap
               if len(c["chosen"]["content"]) < len(c["rejected"]["content"]))
    tl = ngan / len(cap)
    print(f"① lối tắt độ dài — luật 'vế NGẮN hơn là chosen' đoán đúng: {tl:6.1%}"
          f"   {'✅ ĐẠT (<55%)' if tl < 0.55 else '⛔ TRƯỢT'}")
    tach = sum(tach_bang_chuoi.values())
    print(f"① lối tắt chuỗi  — tách được bằng '(no name)':            {tach/len(cap):6.1%}"
          f"   {'✅ ĐẠT' if tach == 0 else '⛔ TRƯỢT — lọc thêm'}")
    dl = [abs(len(c["chosen"]["content"]) - len(c["rejected"]["content"])) for c in cap]
    dl.sort()
    print(f"① chênh độ dài ký tự hai vế: trung vị {dl[len(dl)//2]} · p90 {dl[int(.9*len(dl))]}")
    print(f"② false negative — mọi cặp đã ép khoảng cách ∈ [{LO:.0f}, {HI:.0f}] px  ✅ ĐẠT theo dựng")
    el = len(cap) / 41099
    print(f"③ eligibility: {len(cap)}/41.099 = {el:6.1%}"
          f"   {'✅ ĐẠT (≥25%)' if el >= 0.25 else '⛔ TRƯỢT'}")

    # ══ BẤT BIẾN — cùng tinh thần bảy phép của build_min_desc.py ══
    kt = []
    kt.append(("① hai vế KHÁC nhau",
               all(c["chosen"]["content"] != c["rejected"]["content"] for c in cap)))
    kt.append(("② câu sau </desc> TRÙNG KHỚP hai vế",
               all(c["chosen"]["content"].split("</desc>", 1)[1]
                   == c["rejected"]["content"].split("</desc>", 1)[1] for c in cap)))
    kt.append(("③ vế rejected đúng khuôn desc_str",
               all(c["rejected"]["content"].startswith("<desc>") for c in cap)))
    kt.append(("④ prompt + ảnh trùng CE2 từng dòng",
               all(a["messages"][:2] == b["messages"][:2] and a["images"] == b["images"]
                   for a, b in zip(cap, ce2))))
    kt.append(("⑤ CE2 học đúng vế chosen",
               all(b["messages"][2]["content"] == a["chosen"]["content"]
                   for a, b in zip(cap, ce2))))
    print("\nBẤT BIẾN")
    for ten, ok in kt:
        print(f"  {'✅' if ok else '⛔'} {ten}")
    if not all(o for _, o in kt):
        sys.exit("⛔ trượt bất biến — không ghi tệp.")

    for ten, dat in (("min_desc_onpolicy.json", cap), ("ce2_onpolicy.json", ce2)):
        with open(os.path.join(BR, ten), "w", encoding="utf-8") as f:
            json.dump(dat, f, ensure_ascii=False)
        print(f"ghi {ten}: {len(dat)} mẫu")

    ip = os.path.join(BR, "dataset_info.json")
    info = json.load(open(ip, encoding="utf-8")) if os.path.exists(ip) else {}
    info["gui_min_desc_onpolicy"] = {
        "file_name": "min_desc_onpolicy.json", "formatting": "sharegpt", "ranking": True,
        "columns": {"messages": "messages", "chosen": "chosen", "rejected": "rejected",
                    "images": "images"},
        "tags": {"role_tag": "role", "content_tag": "content",
                 "user_tag": "user", "assistant_tag": "assistant", "system_tag": "system"}}
    info["gui_ce2_onpolicy"] = {
        "file_name": "ce2_onpolicy.json", "formatting": "sharegpt",
        "columns": {"messages": "messages", "images": "images"},
        "tags": {"role_tag": "role", "content_tag": "content",
                 "user_tag": "user", "assistant_tag": "assistant", "system_tag": "system"}}
    json.dump(info, open(ip, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("cập nhật dataset_info.json → gui_min_desc_onpolicy · gui_ce2_onpolicy")


if __name__ == "__main__":
    main()
