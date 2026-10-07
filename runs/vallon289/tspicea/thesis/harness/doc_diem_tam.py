# -*- coding: utf-8 -*-
"""FREE · offline — đọc điểm TẠM từ tệp thô đang chấm dở.

Vì sao cần: nhân Python của notebook chỉ chạy **một ô một lúc**, nên trong lúc ô chấm đang
chạy thì KHÔNG chạy được ô kiểm nào — bấm ô thứ hai chỉ xếp hàng đợi. Nhưng Kaggle cho **tải
tệp trong `/kaggle/working` ngay khi phiên còn chạy** (panel Output → làm mới → tải). Nên cách
xem tiến độ không đụng gì tới lượt chạy là: tải tệp thô về rồi đọc ở đây.

Tệp thô cũng chính là bản bảo hiểm: `score_run.py` ghi dần và nối tiếp được, nên phiên chết thì
đưa tệp này lên dataset rồi chấm tiếp từ đúng chỗ.

Chạy: python3 harness/doc_diem_tam.py runs/score_s1_seed202_raw.jsonl
"""
import sys, json, os

MOC = {"s1_seed101": 59.1, "base": 47.6, "ceiling_human": 75.7}


def main():
    p = sys.argv[1]
    n = ok = bq = 0
    for l in open(p, encoding="utf-8"):
        o = json.loads(l)
        n += 1
        if "bo_qua" in o:
            bq += 1
        else:
            ok += o.get("executable", 0)
    cham = n - bq
    if not cham:
        print("chưa có bước nào chấm được")
        return
    e = ok / cham * 100
    # sai số chuẩn nhị thức, CHƯA hiệu chỉnh cụm ⇒ hẹp hơn thực tế, chỉ dùng để canh dải
    se = (e * (100 - e) / cham) ** 0.5
    print(f"{os.path.basename(p)}")
    print(f"  đã chấm {n}/4463 = {n/4463:5.1%}  (bỏ {bq})")
    print(f"  điểm tạm {e:.1f}%  ±{1.96*se:.1f} (nhị thức, chưa cụm)")
    print(f"  mốc: s1/101 {MOC['s1_seed101']}  ·  Base {MOC['base']}  ·  trần {MOC['ceiling_human']}")
    if n < 500:
        print("  ⏳ dưới 500 bước thì còn nhiễu, chưa đọc được gì")
    elif 55 <= e <= 63:
        print("  ✔ trong dải mong đợi — cứ để chạy")
    else:
        print("  ⚠ NGOÀI dải 55–63%: xem lại trước khi đốt thêm giờ."
              " 63% câu của nó trùng nguyên văn seed101 nên điểm không thể lệch xa;"
              " lệch xa ⇒ nghi nối sai dữ liệu chứ không phải tính chất mô hình")


if __name__ == "__main__":
    main()
