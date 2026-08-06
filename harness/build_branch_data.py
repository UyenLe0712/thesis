# -*- coding: utf-8 -*-
"""
FREE · offline — Ghép nhãn khai báo vào dữ liệu dạy, xuất ra từng nhánh thí nghiệm.

Bốn nhánh có huấn luyện (report/106 mục 2). Mọi nhánh dùng CÙNG một đầu vào,
chỉ khác phần đích sinh — đó là lý do chênh lệch điểm quy được về can thiệp:

  s1           đích =                                câu
  s2           đích = <desc>khai báo thật</desc>  +  câu
  s2r          đích = <desc>khai báo GIẢ</desc>   +  câu      (giả = lấy từ màn KHÁC,
                      toạ độ ngẫu nhiên, độ dài ghép sát bản thật theo từng mẫu)
  s2_nopoint   đích = <desc>thật, bỏ ô toạ độ</desc> + câu

Nhánh s3 (mức 2) không xuất ở đây: nó dùng chính dữ liệu s2 cộng thêm trường
`desc_neg` sẵn có trong descriptors.jsonl để tính khoản phạt lề lúc huấn luyện.

Bước KHÔNG phải bước chạm (cuộn, gõ, mở ứng dụng...) không có khai báo — mọi nhánh
giữ nguyên đích là câu. Nhờ vậy phép kiểm không-gây-hại mới đọc được: phần dữ liệu
đó y hệt nhau ở mọi nhánh.

Xuất theo định dạng sharegpt của LLaMA-Factory, kèm dataset_info.json.

Chạy:  ~/.venvs/thesis/bin/python harness/build_branch_data.py
"""
import os, sys, json, random, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
OUT = os.path.join(ROOT, "branches")

SEED = 20260805                      # khoá trong report/106 mục 10
MAX_OCR = 24                         # số dòng chữ tối đa nhét vào đầu vào
BASE_MODEL = "Qwen/Qwen2.5-VL-3B-Instruct"   # chỉ dùng bộ tách token, không nạp trọng số

SYS = ("Bạn nhìn ảnh màn hình điện thoại và viết MỘT câu hướng dẫn ngắn bằng tiếng Anh "
       "cho người dùng, chỉ rõ cần chạm vào đâu để đi tiếp.")


def prompt_body(r, ocr_rec):
    """Phần CHỮ của đầu vào, KHÔNG kèm chỗ dành cho ảnh.

    Tách ra vì hai nơi cần chỗ-dành-cho-ảnh ở hai dạng khác nhau:
      · lúc DẠY, LLaMA-Factory nhận chuỗi "<image>" rồi tự thay bằng token ảnh thật
      · lúc CHẤM, phải đưa content dạng danh sách [{'type':'image'}, {'type':'text'}]
        cho chat template của Qwen, vì template in nguyên văn chuỗi "<image>" chứ
        KHÔNG thay — đưa chuỗi vào là mô hình chạy mù, không có token ảnh nào.
    Tách hàm để hai đường dùng chung đúng một nguồn chữ, kiểm được bằng cách render
    cả hai rồi so chuỗi (xem infer_branch.py --selftest).
    """
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


def prompt_of(r, ocr_rec):
    """Đầu vào lúc DẠY — giống hệt nhau ở mọi nhánh."""
    return "<image>\n" + prompt_body(r, ocr_rec)


def strip_point(desc):
    """Bỏ ô toạ độ khỏi chuỗi khai báo, giữ nguyên ba ô còn lại."""
    import re
    d = re.sub(r"\s*\|\s*<point>[^<]*</point>", "", desc)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--img-prefix", default="",
                    help="tiền tố đường dẫn ảnh trên máy sẽ huấn luyện, "
                         "vd /workspace/data/ — để trống thì ghi đường dẫn tương đối")
    args = ap.parse_args()
    rnd = random.Random(SEED)

    ocr = {}
    with open(os.path.join(ROOT, "ocr.jsonl"), encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            ocr[o["image"]] = o
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8")]
    desc = {}
    dpath = os.path.join(ROOT, "descriptors.jsonl")
    with open(dpath, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            desc[(d["episode_id"], d["step_id"])] = d

    # ── kho khai báo để bốc bản GIẢ cho nhánh s2r ──────────────────────────────
    # Luật: bốc từ tác vụ KHÁC (khác episode), chọn bản có độ dài sát nhất để
    # chênh lệch độ dài chuỗi đích không thành lời giải thích thay thế.
    #
    # Đo theo TOKEN chứ không theo ký tự. Mất mát tính trên token, nên "độ dài" mà
    # nhánh đối chứng cần ghép là độ dài token. Bản trước ghép theo ký tự: trung vị
    # lệch 0 ký tự nghe rất khít, nhưng đo lại theo token thì chỉ 54% số cặp nằm
    # trong 2 token, biên độ tới ±17. Trung bình vẫn ~0 nên đối chứng không lệch hệ
    # thống, song ghép theo token thì chặt hơn mà không mất gì.
    def _tok_len_factory():
        try:
            from transformers import AutoTokenizer
            tk = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
            return lambda s: len(tk(s).input_ids), "token"
        except Exception as e:
            print(f"  (không nạp được bộ tách token: {e} — ghép độ dài theo KÝ TỰ)")
            return len, "ký tự"

    tok_len, len_unit = _tok_len_factory()
    pool = [(d["episode_id"], tok_len(d["desc"]), d["desc"]) for d in desc.values()]
    pool.sort(key=lambda t: t[1])
    print(f"  ghép độ dài khai báo giả theo: {len_unit}")

    def fake_for(d):
        L = tok_len(d["desc"])
        cand = [p for p in pool if p[0] != d["episode_id"]]
        if not cand:
            return None
        # 12 bản gần nhất về độ dài, bốc ngẫu nhiên một trong số đó (có hạt giống)
        cand.sort(key=lambda t: abs(t[1] - L))
        near = cand[:12]
        _, _, s = near[rnd.randrange(len(near))]
        # toạ độ ngẫu nhiên: thay số trong <point> để nội dung vô nghĩa hoàn toàn
        import re
        return re.sub(r"<point>\d+,\d+</point>",
                      lambda _: f"<point>{rnd.randrange(1000)},{rnd.randrange(1000)}</point>", s)

    branches = {"s1": [], "s2": [], "s2r": [], "s2_nopoint": []}
    st = collections.Counter()
    for r in recs:
        o = ocr.get(r["image"])
        p = prompt_of(r, o)
        cau = r["target_instruction"].strip()
        d = desc.get((r["episode_id"], r["step_id"]))
        st["tong"] += 1

        tgt = {"s1": cau}
        if d:
            st["co_khai_bao"] += 1
            tgt["s2"] = d["desc"] + "\n" + cau
            tgt["s2_nopoint"] = strip_point(d["desc"]) + "\n" + cau
            fk = fake_for(d)
            tgt["s2r"] = (fk + "\n" + cau) if fk else (d["desc"] + "\n" + cau)
            if fk:
                st["co_khai_bao_gia"] += 1
                st["lech_do_dai"] += abs(len(fk) - len(d["desc"]))
        else:
            st["khong_khai_bao"] += 1
            for k in ("s2", "s2r", "s2_nopoint"):
                tgt[k] = cau                       # bước không chạm: mọi nhánh y hệt

        for name, out in branches.items():
            out.append({
                "messages": [
                    {"role": "system", "content": SYS},
                    {"role": "user", "content": p},
                    {"role": "assistant", "content": tgt[name]},
                ],
                "images": [args.img_prefix + r["image"]],
            })

    os.makedirs(args.out, exist_ok=True)
    info = {}
    for name, rows in branches.items():
        fn = f"{name}.json"
        json.dump(rows, open(os.path.join(args.out, fn), "w", encoding="utf-8"),
                  ensure_ascii=False)
        info[f"gui_{name}"] = {
            "file_name": fn,
            "formatting": "sharegpt",
            "columns": {"messages": "messages", "images": "images"},
            "tags": {"role_tag": "role", "content_tag": "content",
                     "user_tag": "user", "assistant_tag": "assistant",
                     "system_tag": "system"},
        }
    json.dump(info, open(os.path.join(args.out, "dataset_info.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    with open(os.path.join(args.out, "README.txt"), "w", encoding="utf-8") as f:
        f.write("Đường dẫn ảnh trong bốn tệp nhánh: "
                + (f"có tiền tố '{args.img_prefix}'" if args.img_prefix else "TƯƠNG ĐỐI")
                + "\nTrên máy huấn luyện, thư mục images/ phải nằm sao cho đường dẫn này đúng,\n"
                  "hoặc dựng lại bằng: build_branch_data.py --img-prefix /duong/dan/cua/may/\n")

    n = st["tong"]
    print("=" * 78)
    print(f"DỰNG DỮ LIỆU BỐN NHÁNH — {n} bước")
    print("=" * 78)
    print(f"  bước chạm, có khai báo   : {st['co_khai_bao']:5} = {st['co_khai_bao']/n:5.1%}")
    print(f"  bước khác, không khai báo: {st['khong_khai_bao']:5} = {st['khong_khai_bao']/n:5.1%}"
          f"   (mọi nhánh y hệt nhau → đọc được phép kiểm không-gây-hại)")
    if st["co_khai_bao_gia"]:
        print(f"  dựng được khai báo giả   : {st['co_khai_bao_gia']:5}"
              f"   lệch độ dài trung bình {st['lech_do_dai']/st['co_khai_bao_gia']:.1f} ký tự")
    print("-" * 78)
    for name, rows in branches.items():
        avg = sum(len(x["messages"][2]["content"]) for x in rows) / len(rows)
        print(f"  {name:11} {len(rows):5} mẫu · đích trung bình {avg:6.1f} ký tự")
    print("=" * 78)
    print("MỘT MẪU, xem thử (nhánh s2):")
    ex = next(x for x, r in zip(branches["s2"], recs) if desc.get((r["episode_id"], r["step_id"])))
    print("--- đầu vào ---"); print(ex["messages"][1]["content"][:520])
    print("--- đích sinh ---"); print(ex["messages"][2]["content"])
    print(f"\nĐã lưu {args.out}/  (4 tệp nhánh + dataset_info.json)")


if __name__ == "__main__":
    main()
