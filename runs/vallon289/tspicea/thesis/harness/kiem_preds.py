# -*- coding: utf-8 -*-
"""FREE · offline — KIỂM TỆP PREDS TRƯỚC KHI TRẢ TIỀN/QUOTA CHO MỘT LƯỢT CHẤM.

Một lượt chấm là **5,6 giờ** GPU (và Kaggle chỉ cho 30 giờ/tuần). Mọi lỗi bên dưới đều thuộc
loại **chạy trơn mà kết quả sai hoặc không so được**, tức không có tiếng động nào:

  · thiếu/thừa bước        → chấm trên quần thể khác, số không so được với nhánh đã chấm
  · sai khoá `pred`        → `score_run.load_preds` trả chuỗi rỗng ⇒ chấm 4.463 câu RỖNG
  · câu rỗng ở bước chạm   → bị `bo_qua`, làm lệch quần thể so với nhánh đối chiếu
  · trộn hai lượt chạy     → tệp nối tiếp còn dòng của lượt trước, điểm là số của mô hình khác
  · nhánh chấm lệch nhau   → McNemar ghép cặp không còn ghép được

Phép kiểm quan trọng nhất là **số 5**: bước bị bỏ phải TRÙNG KHÍT nhánh đối chiếu, không thì
hai nhánh chấm trên hai quần thể và mọi phép ghép cặp phải trừ bù.

Chạy:
    python3 harness/kiem_preds.py runs/preds_s1_seed202.jsonl
    python3 harness/kiem_preds.py <tệp> --doi-chieu runs/preds_s1_seed101.jsonl
"""
import os, sys, json, argparse, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
TEST = os.path.join(HERE, "dg1_cache", "test_ac", "test.jsonl")
TAP_VERB = ("click", "tap", "press", "select", "choose", "touch")


def nap_preds(p):
    rows, dup = {}, []
    for i, l in enumerate(open(p, encoding="utf-8"), 1):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        k = (o["episode_id"], o["step_id"])
        if k in rows:
            dup.append((i, k))
        rows[k] = o
    return rows, dup


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("preds")
    ap.add_argument("--doi-chieu", default=os.path.join(HERE, "..", "runs",
                                                       "preds_s1_seed101.jsonl"),
                    help="nhánh đã chấm để đối chiếu quần thể (mặc định s1/seed101)")
    a = ap.parse_args()
    dat = 0
    tong = 8

    print(f"KIỂM {a.preds}\n" + "─" * 72)

    # ── 0. đọc tập kiểm làm nguồn sự thật ───────────────────────────────────────────
    T, TAP = {}, set()
    for l in open(TEST, encoding="utf-8"):
        o = json.loads(l)
        k = (o["episode_id"], o["step_id"])
        T[k] = o
        if o["action"].get("action_type") in ("click", "long_press") and "x" in o["action"]:
            TAP.add(k)
    print(f"tập kiểm: {len(T)} bước · {len(TAP)} bước chạm")

    rows, dup = nap_preds(a.preds)

    # ── 1. số dòng ──────────────────────────────────────────────────────────────────
    ok = len(rows) == len(T)
    dat += ok
    print(f"{'✔' if ok else '✘'} 1. số bản ghi: {len(rows)} (cần {len(T)})")

    # ── 2. trùng khoá ───────────────────────────────────────────────────────────────
    ok = not dup
    dat += ok
    print(f"{'✔' if ok else '✘'} 2. khoá trùng lặp: {len(dup)}"
          + (f"  ví dụ dòng {dup[0][0]} {dup[0][1]}" if dup else ""))

    # ── 3. khớp khoá với tập kiểm ───────────────────────────────────────────────────
    thieu, thua = set(T) - set(rows), set(rows) - set(T)
    ok = not thieu and not thua
    dat += ok
    print(f"{'✔' if ok else '✘'} 3. khớp khoá tập kiểm: thiếu {len(thieu)} · thừa {len(thua)}")

    # ── 4. khoá `pred` và câu rỗng ───────────────────────────────────────────────────
    thieu_pred = [k for k, o in rows.items() if "pred" not in o]
    rong = [k for k, o in rows.items() if not str(o.get("pred", "")).strip()]
    rong_tap = [k for k in rong if k in TAP]
    ok = not thieu_pred and len(rong_tap) <= 5
    dat += ok
    print(f"{'✔' if ok else '✘'} 4. khoá `pred`: thiếu {len(thieu_pred)} · câu rỗng "
          f"{len(rong)} (trong đó {len(rong_tap)} ở bước CHẠM ⇒ sẽ bị bỏ khi chấm)")
    if thieu_pred:
        print("     ⛔ thiếu khoá `pred` ⇒ `load_preds` trả chuỗi rỗng, chấm sẽ ra số rác")

    # ── 5. quần thể chấm có TRÙNG KHÍT nhánh đối chiếu? (phép kiểm quan trọng nhất) ──
    dc = os.path.abspath(a.doi_chieu)
    if os.path.exists(dc):
        rows2, _ = nap_preds(dc)
        rong2 = {k for k in TAP if not str(rows2.get(k, {}).get("pred", "")).strip()}
        r1 = set(rong_tap)
        ok = r1 == rong2
        dat += ok
        print(f"{'✔' if ok else '✘'} 5. bước bị bỏ trùng khít nhánh đối chiếu "
              f"({os.path.basename(dc)}): tệp này {sorted(r1)} · đối chiếu {sorted(rong2)}")
        if not ok:
            print(f"     ⚠ hai nhánh sẽ chấm trên {len(TAP)-len(r1)} vs {len(TAP)-len(rong2)} "
                  f"bước ⇒ McNemar ghép cặp phải trừ bù, và mọi bảng phải khai con số riêng")
        # ── 8. câu có thật sự khác nhánh đối chiếu không ─────────────────────────────
        chung = [k for k in TAP if k in rows and k in rows2]
        giong = sum(1 for k in chung
                    if str(rows[k].get("pred", "")).strip() == str(rows2[k].get("pred", "")).strip())
        ok8 = 0.05 < giong / len(chung) < 0.95
        print(f"{'✔' if ok8 else '⚠'} 8. câu giống nhánh đối chiếu: {giong}/{len(chung)} = "
              f"{giong/len(chung):.1%}  (100% ⇒ cùng một mô hình; ~0% ⇒ nghi sai tệp)")
        dat += ok8
    else:
        print(f"⚠ 5+8. không thấy nhánh đối chiếu {dc}, bỏ qua hai phép")
        tong -= 2

    # ── 6. chữ ký lượt chạy: chỉ được có MỘT ────────────────────────────────────────
    sigs = {o.get("run") for o in rows.values() if o.get("run")}
    ok = len(sigs) <= 1
    dat += ok
    print(f"{'✔' if ok else '✘'} 6. chữ ký lượt chạy: {sigs or '(tệp không có trường `run`)'}")
    if len(sigs) > 1:
        print("     ⛔ trộn nhiều lượt ⇒ điểm là số của mấy mô hình cộng lại")

    # ── 7. thống kê câu, so với nhánh đối chiếu ──────────────────────────────────────
    sents = [str(rows[k].get("pred", "")).strip() for k in TAP if k in rows]
    sents = [s for s in sents if s]
    dai = st.median(len(s) for s in sents)
    dong_tu = sum(1 for s in sents if s.lower().split()[:1] and s.lower().split()[0] in TAP_VERB)
    ok = 15 <= dai <= 120
    dat += ok
    print(f"{'✔' if ok else '✘'} 7. câu ở bước chạm: {len(sents)} câu · độ dài trung vị "
          f"{dai:.0f} ký tự · mở đầu bằng động từ chạm {dong_tu/len(sents):.1%}")
    print(f"     mốc s1/101: trung vị 33 ký tự · Base 70 · người 34")

    print("─" * 72)
    print(f"{dat}/{tong} phép ĐẠT — " + ("✅ CHẤM ĐƯỢC" if dat == tong else
          "⛔ DỪNG, sửa trước khi tiêu quota"))
    print("\n3 câu đầu để mắt người xem:")
    for k in list(TAP)[:3]:
        if k in rows:
            print(f"  gold: {T[k]['gold_instruction'].strip()}")
            print(f"  pred: {rows[k].get('pred','')}\n")
    return 0 if dat == tong else 1


if __name__ == "__main__":
    sys.exit(main())
