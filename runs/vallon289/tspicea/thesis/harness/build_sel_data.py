# -*- coding: utf-8 -*-
"""
FREE · offline — dựng dữ liệu hai nhánh của pipeline SEL (`report/123` §3.1–3.3).

    gui_sel         đích = <sel>tên <point>x,y</point></sel>\\n + câu vàng
                           hoặc <sel>none</sel>\\n + câu vàng
    gui_sft_match   đích =                                        câu vàng

⭐ Chỉ MỘT thứ khác nhau giữa hai nhánh: có đầu chọn tường minh hay không.
Cùng ảnh, cùng khối ứng viên trong câu nhắc (**từng byte**), cùng câu đích, cùng số dòng.
Đó là điều kiện để `Δ_component = exec(gui_sel) − exec(gui_sft_match)` chỉ mang một biến.
Nếu hai nhánh hoà nhau thì "khối ứng viên trong đầu vào" đã làm hết việc ⇒ **không được
viết là đóng góp mô hình**. Đừng bỏ nhánh đối chứng để tiết kiệm GPU (`123` §3.3).

⛔ Luật khoá, đừng đổi khi thấy số:
  · Nội dung `<sel>` là bản **CHÉP NGUYÊN** một dòng trong khối — không viết lại tên,
    không bịa `point`. Bất biến ⑤ canh điều này.
  · Câu là **câu vàng nguyên bản**: không bồi mệnh đề vị trí (`123` §2.1–2.2 — đã chết),
    không ép tên nguyên văn (`123` §2.3 — đã chết). Bồi vào là tự chế ra Δ giả qua kênh
    "chép từ giấy nháp" mà không có cải thiện cơ chế chọn nào.
  · Luật khớp tên là **khớp chuỗi chính xác sau `strip().lower()`**. Đổi luật (ví dụ
    chuẩn hoá khoảng trắng) là đổi cả tỉ lệ `none` lẫn `sel_acc` ⇒ phải quyết TRƯỚC khi
    dựng dữ liệu và ghi vào mục sửa đổi (x16) của `report/106`.
  · **Không xoá mẫu nào** khỏi tập dạy. Hai tệp cùng số dòng với `train.jsonl`.

Chạy:
  ~/.venvs/thesis/bin/python harness/build_sel_data.py --split train
  ~/.venvs/thesis/bin/python harness/build_sel_data.py --split train --img-prefix /content/ws/thesis/harness/dg1_cache/train_ac/
"""
import os, sys, json, random, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import descriptor_label_build as D
import build_candidates as BC
import build_branch_data as BB

TOL = 140          # ô dung sai trên lưới [0,1000] — cùng con số cổng G2 của build_candidates
SEED = 20260805    # hạt giống khoá ở report/106 mục 10
CUTOFF = 3072      # cutoff_len dự kiến của lượt train SEL (123 §3.3)


def gold_candidate(cands, gold_name, gold_nx, gold_ny):
    """Trả về ứng viên vàng, hoặc None nếu không có (→ nhãn <sel>none</sel>).

    Khoá nguyên văn ở `report/123` §3.2. `build_candidates.py:141–148` **không có** hàm
    này — nó chỉ đo phủ bằng `any(...)`, không trả về ứng viên nào là vàng và không có
    luật phá hoà. Viết mới ở đây, và `sel_acc` lúc chấm phải dùng ĐÚNG hàm này.
    """
    gn = (gold_name or "").strip().lower()
    if not gn:
        return None
    hits = [c for c in cands
            if c["name"].strip().lower() == gn
            and abs(c["x"] - gold_nx) <= TOL
            and abs(c["y"] - gold_ny) <= TOL]
    if not hits:
        return None
    # phá hoà: gần vàng nhất theo L2 (KHÔNG phải theo thứ tự đọc — thứ tự đọc là thông
    # tin của khối, lấy nó làm luật phá hoà là để thứ tự khối rò ra đáp án)
    return min(hits, key=lambda c: (c["x"] - gold_nx) ** 2 + (c["y"] - gold_ny) ** 2)


def sel_str(c):
    """Chuỗi trong thẻ <sel>. Đúc bằng CHÍNH `block_str` để không thể lệch với khối."""
    return BC.block_str([(c["name"], c["x"], c["y"])])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["train", "test"], default="train")
    ap.add_argument("--out", default="")
    ap.add_argument("--img-prefix", default="")
    ap.add_argument("--max", type=int, default=BC.MAX_CAND)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--cutoff", type=int, default=CUTOFF)
    ap.add_argument("--tokenizer", default=BB.BASE_MODEL,
                    help="chỉ dùng cho cổng G4; đổi backbone thì đổi cờ này")
    ap.add_argument("--no-g4", action="store_true", help="bỏ cổng G4 (khỏi nạp bộ tách token)")
    args = ap.parse_args()
    D.set_split(args.split)
    ROOT = D.ROOT
    # ⛔ --limit là chế độ THỬ: ghi ra thư mục riêng, không đè nhánh thật.
    # (2/9: một lượt thử --limit 30 của build_candidates.py đã đè mất bản 4.463 màn.)
    out_dir = args.out or os.path.join(
        ROOT, f"branches_thu_{args.limit}" if args.limit else "branches")
    rnd = random.Random(SEED)

    fn = "test.jsonl" if args.split == "test" else "train.jsonl"
    recs = [json.loads(l) for l in open(os.path.join(ROOT, fn), encoding="utf-8")]
    if args.limit:
        recs = recs[:args.limit]
    ocr = {}
    with open(os.path.join(ROOT, "ocr.jsonl"), encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            ocr[o["image"]] = o
    desc = {}
    with open(os.path.join(ROOT, "descriptors.jsonl"), encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            desc[(d["episode_id"], d["step_id"])] = d
    # khối ứng viên: dùng lại candidates.jsonl nếu có (bước chạm), tự tính cho phần còn
    # lại (bước cuộn/gõ/mở app — build_candidates.py chỉ chạy trên bước chạm)
    cache = {}
    cp = os.path.join(ROOT, "candidates.jsonl")
    if os.path.exists(cp):
        with open(cp, encoding="utf-8") as f:
            for line in f:
                c = json.loads(line)
                cache[(c["episode_id"], c["step_id"])] = c["cands"]
    print(f"nạp: {len(recs)} bước · {len(desc)} khai báo vàng · {len(cache)} khối có sẵn")

    sel_rows, ctl_rows, s1m_rows = [], [], []
    st = collections.Counter()
    tinh_moi = 0
    for i, r in enumerate(recs):
        key = (r["episode_id"], r["step_id"])
        cands = cache.get(key)
        if cands is None:
            rel = f"episode_{r['episode_id']}_screenshot_{r['step_id']}.png"
            w, h = r.get("w") or 1080, r.get("h") or 2400
            cands = [{"name": a, "x": b, "y": c}
                     for a, b, c in BC.candidates_of(rel, ocr.get(r["image"]), w, h, args.max)]
            cache[key] = cands
            tinh_moi += 1

        body = BB.prompt_body(r, ocr.get(r["image"]), cands=cands)
        p = "<image>\n" + body
        cau = r["target_instruction"].strip()

        la_cham = r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]
        g = desc.get(key)
        gc = None
        if la_cham and g and g.get("name"):
            gx, gy = g["point_norm"]
            gc = gold_candidate(cands, g["name"], gx, gy)

        if gc is not None:
            the = f"<sel>{sel_str(gc)}</sel>"
            st["sel_that"] += 1
        else:
            the = "<sel>none</sel>"
            if not la_cham:
                st["none_khong_cham"] += 1
            elif not (g and g.get("name")):
                st["none_khong_ten_vang"] += 1
            elif not cands:
                st["none_khoi_rong"] += 1
            else:
                st["none_khong_khop"] += 1
        if la_cham:
            st["cham"] += 1
        st["tong"] += 1

        goc = {"messages": [{"role": "system", "content": BB.SYS},
                            {"role": "user", "content": p}],
               "images": [args.img_prefix + r["image"]]}
        sel_rows.append({"messages": goc["messages"] + [{"role": "assistant",
                                                         "content": the + "\n" + cau}],
                         "images": goc["images"]})
        ctl_rows.append({"messages": goc["messages"] + [{"role": "assistant",
                                                         "content": cau}],
                         "images": goc["images"]})

        # S1-match (report/132 §3): mốc dưới của bảng phân rã ba tầng.
        # Giống `gui_sft_match` ở MỌI thứ trừ đúng một biến — không có khối ứng viên.
        # ⛔ Phải gọi `cands=None`, KHÔNG phải `cands=[]`: None giữ nguyên 24 dòng OCR
        # (đúng đường của S1 cũ), còn [] sẽ bỏ luôn cả OCR, tức lệch HAI biến và làm
        # Δ_menu hết nghĩa. Dựng trong cùng lượt này để loại nốt rủi ro lệch lượt OCR.
        p_nomenu = "<image>\n" + BB.prompt_body(r, ocr.get(r["image"]), cands=None)
        s1m_rows.append({"messages": [{"role": "system", "content": BB.SYS},
                                      {"role": "user", "content": p_nomenu},
                                      {"role": "assistant", "content": cau}],
                         "images": goc["images"]})
        if (i + 1) % 5000 == 0:
            print(f"  {i+1}/{len(recs)}", flush=True)

    # ── BẤT BIẾN — trượt một cái là dừng, không ghi tệp ────────────────────────
    print("\nBẤT BIẾN")
    kt = []
    kt.append(("① hai nhánh cùng số dòng, bằng số bản ghi nguồn",
               len(sel_rows) == len(ctl_rows) == len(recs)))
    kt.append(("② câu nhắc + ảnh trùng nhau từng byte ở mọi mẫu",
               all(a["messages"][:2] == b["messages"][:2] and a["images"] == b["images"]
                   for a, b in zip(sel_rows, ctl_rows))))
    kt.append(("③ đối chứng KHÔNG chứa thẻ <sel> nào",
               all("<sel>" not in b["messages"][2]["content"] for b in ctl_rows)))
    kt.append(("④ đích nhánh SEL = thẻ + '\\n' + ĐÚNG câu của đối chứng",
               all(a["messages"][2]["content"].split("\n", 1)[1] == b["messages"][2]["content"]
                   and a["messages"][2]["content"].startswith("<sel>")
                   for a, b in zip(sel_rows, ctl_rows))))
    def _noi_dung_sel(s):
        return s[len("<sel>"):s.index("</sel>")]
    xau = [a for a in sel_rows
           if _noi_dung_sel(a["messages"][2]["content"]) != "none"
           and _noi_dung_sel(a["messages"][2]["content"]) not in a["messages"][1]["content"]]
    kt.append((f"⑤ nội dung <sel> có NGUYÊN VĂN trong khối ứng viên của chính mẫu đó "
               f"({len(xau)} mẫu sai)", not xau))
    kt.append(("⑥ mọi bước KHÔNG-CHẠM đều mang <sel>none</sel>",
               all("<sel>none</sel>" in a["messages"][2]["content"]
                   for a, r in zip(sel_rows, recs)
                   if not (r["action"].get("action_type") in ("click", "long_press")
                           and "x" in r["action"]))))
    # ⑦ KHÔNG kiểm "câu không rỗng" — nguồn có sẵn một ít bước câu vàng rỗng và luật
    # `123` §3.2 cấm xoá mẫu. Cái phải canh là ta không TẠO THÊM mẫu rỗng nào: số mẫu
    # rỗng ở hai nhánh phải đúng bằng số câu vàng rỗng đọc từ train.jsonl.
    # (Lát 1.697 bước có 1 ca; cả tập s1.json đã train có 122 ca = 0,19%.)
    n_rong_nguon = sum(1 for r in recs if not r["target_instruction"].strip())
    kt.append((f"⑦ không tạo thêm mẫu rỗng (nguồn có {n_rong_nguon})",
               sum(1 for a in sel_rows if not a["messages"][2]["content"].split("\n", 1)[1].strip())
               == n_rong_nguon
               and sum(1 for b in ctl_rows if not b["messages"][2]["content"].strip())
               == n_rong_nguon))
    # ── bất biến riêng của S1-match (mốc dưới, report/132 §3) ─────────────────
    LB_MENU, LB_OCR = "Ứng viên trên màn:", "Chữ đọc được trên màn:"
    kt.append(("⑧ S1-match cùng số dòng với hai nhánh kia",
               len(s1m_rows) == len(sel_rows)))
    kt.append(("⑨ S1-match và đối chứng có CÙNG đích và CÙNG ảnh (chỉ khác câu nhắc)",
               all(m["messages"][2] == b["messages"][2] and m["images"] == b["images"]
                   for m, b in zip(s1m_rows, ctl_rows))))
    kt.append(("⑩ S1-match KHÔNG chứa khối ứng viên ở bất kỳ mẫu nào",
               all(LB_MENU not in m["messages"][1]["content"] for m in s1m_rows)))
    kt.append(("⑪ S1-match KHÔNG chứa thẻ <sel>",
               all("<sel>" not in m["messages"][2]["content"] for m in s1m_rows)))
    # ⑫ Đúng một biến: ở mẫu nào đối chứng CÓ khối ứng viên thì câu nhắc phải khác
    # S1-match, và khác đó phải nằm trọn ở khối chữ — S1-match dùng OCR, đối chứng
    # dùng menu. Mẫu nào khối rỗng thì hai câu nhắc trùng nhau, đó là hợp lệ.
    co_menu = [(m, b) for m, b in zip(s1m_rows, ctl_rows)
               if LB_MENU in b["messages"][1]["content"]]
    khac = sum(1 for m, b in co_menu
               if m["messages"][1]["content"] != b["messages"][1]["content"])
    kt.append((f"⑫ mọi mẫu có khối ứng viên đều đổi câu nhắc so với S1-match "
               f"({khac}/{len(co_menu)})", khac == len(co_menu)))
    n_ocr = sum(1 for m in s1m_rows if LB_OCR in m["messages"][1]["content"])
    print(f"  ⓘ S1-match: {n_ocr}/{len(s1m_rows)} mẫu có khối OCR · "
          f"{len(co_menu)}/{len(ctl_rows)} mẫu đối chứng có khối ứng viên")

    for nhan, ok in kt:
        print(f"  {'✅' if ok else '⛔'} {nhan}")
    if not all(ok for _, ok in kt):
        sys.exit("⛔ DỪNG — có bất biến trượt, không ghi tệp.")

    os.makedirs(out_dir, exist_ok=True)
    info_path = os.path.join(out_dir, "dataset_info.json")
    info = json.load(open(info_path, encoding="utf-8")) if os.path.exists(info_path) else {}
    for name, rows in (("gui_sel", sel_rows), ("gui_sft_match", ctl_rows),
                       ("gui_s1_match", s1m_rows)):
        f = f"{name}.json"
        json.dump(rows, open(os.path.join(out_dir, f), "w", encoding="utf-8"),
                  ensure_ascii=False)
        info[name] = {"file_name": f, "formatting": "sharegpt",
                      "columns": {"messages": "messages", "images": "images"},
                      "tags": {"role_tag": "role", "content_tag": "content",
                               "user_tag": "user", "assistant_tag": "assistant",
                               "system_tag": "system"}}
    json.dump(info, open(info_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    n, ncham = st["tong"], st["cham"]
    print("=" * 78)
    print(f"DỰNG DỮ LIỆU HAI NHÁNH SEL — {n} bước ({ncham} chạm) · tự tính thêm {tinh_moi} khối")
    print("=" * 78)
    print(f"  <sel> thật               : {st['sel_that']:6} = {st['sel_that']/n:5.1%} toàn tập"
          f" · {st['sel_that']/max(1,ncham):5.1%} trên bước chạm")
    for k, nhan in (("none_khong_cham", "none · bước không chạm"),
                    ("none_khong_ten_vang", "none · vàng không có tên"),
                    ("none_khong_khop", "none · vàng không khớp ứng viên nào"),
                    ("none_khoi_rong", "none · khối ứng viên rỗng")):
        if st[k]:
            print(f"  {nhan:25}: {st[k]:6} = {st[k]/n:5.1%}")

    # ── G3 · rò rỉ: khối có nói cho mô hình biết đáp án nằm đâu không ─────────
    print("=" * 78)
    print("G3 — RÒ RỈ (thứ tự và phép cắt phải độc lập với phần tử đích)")
    thu_hang, bi_cat = [], 0
    for a, r in zip(sel_rows, recs):
        key = (r["episode_id"], r["step_id"])
        cands = cache.get(key) or []
        g = desc.get(key)
        if not (g and g.get("name")):
            continue
        gx, gy = g["point_norm"]
        gc = gold_candidate(cands, g["name"], gx, gy)
        if gc is None:
            bi_cat += 1
        else:
            thu_hang.append(cands.index(gc) / max(1, len(cands) - 1) if len(cands) > 1 else 0.0)
    if thu_hang:
        thu_hang.sort()
        dau = sum(1 for t in thu_hang if t <= 0.10)
        print(f"  vị trí TƯƠNG ĐỐI của ứng viên vàng trong khối (0 = đầu, 1 = cuối):")
        print(f"    p25 {thu_hang[len(thu_hang)//4]:.2f} · trung vị {thu_hang[len(thu_hang)//2]:.2f}"
              f" · p75 {thu_hang[3*len(thu_hang)//4]:.2f}")
        print(f"    nằm trong 10% ĐẦU khối: {dau/len(thu_hang):5.1%}"
              f"   {'✅ ~đều, không dồn đầu' if dau/len(thu_hang) < 0.25 else '⛔ DỒN ĐẦU — nghi rò rỉ'}")
    # thứ tự khối phải đúng bằng thứ tự đọc, dựng lại từ đầu rồi so
    lech = 0
    for key, cands in list(cache.items())[:2000]:
        lai = sorted(cands, key=lambda c: (c["y"], c["x"]))
        if [c["name"] for c in lai] != [c["name"] for c in cands]:
            lech += 1
    print(f"  khối sắp đúng thứ tự đọc (y rồi x), kiểm 2.000 màn: "
          f"{'✅ 0 lệch' if lech == 0 else f'⛔ {lech} màn lệch'}")
    print(f"  bước có tên vàng mà KHÔNG có ứng viên khớp: {bi_cat}"
          f"  ← phải > 0; bằng 0 nghĩa là khối đang được dựng theo đáp án")
    g3p = os.path.join(out_dir, "g3_mau300_doc_mu.txt")
    mau = rnd.sample(range(len(sel_rows)), min(300, len(sel_rows)))
    with open(g3p, "w", encoding="utf-8") as f:
        f.write("300 câu nhắc ngẫu nhiên (hạt giống 20260805) — ĐỌC MÙ.\n"
                "Câu hỏi khi đọc: có dấu hiệu nào chỉ ra phần tử đích không (thứ tự lạ,\n"
                "nhãn thừa, một ứng viên được viết khác kiểu)? KHÔNG có đáp án trong tệp này.\n"
                + "=" * 78 + "\n")
        for j in mau:
            f.write(f"\n--- mẫu #{j} ---\n{sel_rows[j]['messages'][1]['content']}\n")
    print(f"  đã ghi {g3p} — 300 mẫu để đọc mù (cổng G3 của report/121 §6)")

    # ── G4 · độ dài token trên 200 mẫu DÀI NHẤT ──────────────────────────────
    if not args.no_g4:
        print("=" * 78)
        print(f"G4 — ĐỘ DÀI TOKEN, 200 mẫu dài nhất (cutoff {args.cutoff})")
        try:
            from transformers import AutoTokenizer
            tk = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
            nang = sorted(range(len(sel_rows)),
                          key=lambda j: -(len(sel_rows[j]["messages"][1]["content"])
                                          + len(sel_rows[j]["messages"][2]["content"])))[:200]
            dai = []
            for j in nang:
                m = sel_rows[j]["messages"]
                dai.append(len(tk(BB.SYS + m[1]["content"] + m[2]["content"]).input_ids))
            dai.sort()
            vuot = sum(1 for x in dai if x > args.cutoff)
            print(f"  token (chưa kể token ẢNH): trung vị {dai[len(dai)//2]} · max {dai[-1]}")
            print(f"  vượt cutoff {args.cutoff}: {vuot}/200   "
                  f"{'✅ ĐẠT' if vuot == 0 else '⛔ TRƯỢT — sửa cách cắt khối, KHÔNG nới cutoff'}")
            print("  ⚠️ CHƯA kể token ẢNH. Số token ảnh phụ thuộc cỡ ảnh của bộ xử lý và"
                  "\n     PHẢI đo bằng chính processor sẽ train, không suy từ lượt khác"
                  "\n     (lượt S1/S2 chạy cutoff_len 2560 — con số đó không tự chuyển sang đây).")
        except Exception as e:
            print(f"  ⚠️ không nạp được bộ tách token ({e}) — chạy lại cổng G4 khi có mạng")

    print("=" * 78)
    print("MỘT MẪU, xem thử (nhánh gui_sel):")
    vd = next(a for a in sel_rows if "<sel>none</sel>" not in a["messages"][2]["content"])
    print("--- đầu vào ---"); print(vd["messages"][1]["content"][:700])
    print("--- đích sinh ---"); print(vd["messages"][2]["content"])
    print(f"\nĐã lưu {out_dir}/gui_sel.json · gui_sft_match.json · gui_s1_match.json"
          f" · dataset_info.json")


if __name__ == "__main__":
    main()
