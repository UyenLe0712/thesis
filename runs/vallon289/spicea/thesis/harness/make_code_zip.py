# -*- coding: utf-8 -*-
"""
FREE · offline — dựng gói MÃ + PREDS để đưa lên Google Drive cho Kaggle tải về.

Vì sao có tệp này: ảnh tập kiểm nặng 4,1 GB nên dataset Kaggle chứa ảnh gần như không
ai muốn upload lại; hệ quả là MÃ trên Kaggle cứ là bản cũ, phải vá trong notebook, và
ngày 20/8/2026 đã hai lần vá nhầm lớp — im lặng, không một dòng lỗi. Mã chỉ 456 KB.
Tách ra khỏi ảnh thì cập nhật mất vài giây, và ảnh nối bằng symlink chứ không copy.

Gói gồm hai thư mục:
    py/     mã harness (*.py + train_config.yaml)
    preds/  tệp dự đoán của phép B (runs/venus/*.jsonl) — để khỏi phải New Version
            dataset thesis-preds mỗi lần dựng lại lát

Chạy:  python3 harness/make_code_zip.py
Rồi:   upload _bundles/harness_code.zip lên Drive, share "anyone with the link".
⭐ Lần cập nhật sau: dùng "Quản lý phiên bản / Manage versions" trên Drive để THAY tệp,
   ID và link giữ nguyên ⇒ không phải sửa DRIVE_URL trong notebook. Xoá rồi upload mới
   là ID đổi, link cũ chết.
"""
import os, sys, glob, zipfile, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(HERE)
OUT = os.path.join(GOC, "_bundles", "harness_code.zip")

def main():
    py = sorted(glob.glob(os.path.join(HERE, "*.py")) +
                glob.glob(os.path.join(HERE, "*.yaml")))
    preds = sorted(glob.glob(os.path.join(GOC, "runs", "venus", "preds_venus_*.jsonl")))
    if not py:
        sys.exit("DỪNG: không thấy tệp .py nào trong harness/")
    if not preds:
        print("⚠️  không thấy runs/venus/preds_venus_*.jsonl — gói sẽ CHỈ có mã")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in py:
            z.write(f, "py/" + os.path.basename(f))
        for f in preds:
            z.write(f, "preds/" + os.path.basename(f))

    # Phép kiểm rẻ nhất chống "gói cũ mà tưởng mới": in dấu vân tay để đối chiếu với
    # dòng notebook in ra sau khi tải. Đọc mã trên máy này KHÔNG chứng minh được máy kia
    # đang chạy mã gì — chỉ dấu vân tay khớp mới chứng minh.
    h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:12]
    kb = os.path.getsize(OUT) / 1024
    print(f"✅ {OUT}")
    print(f"   {len(py)} tệp mã · {len(preds)} tệp preds · {kb:.0f} KB")
    print(f"   sha256[:12] = {h}    ← đối chiếu với dòng notebook in sau khi tải")
    thieu = [n for n in ("base", "s1", "s2")
             if not any(f"preds_venus_{n}_" in p for p in preds)]
    if thieu:
        print(f"   ⛔ THIẾU nhánh {thieu} — nhánh base là chứng nhân chống bẫy pha loãng")
    else:
        for lat in (2532, 1266, 633):
            co = [n for n in ("base", "s1", "s2")
                  if any(p.endswith(f"venus_{n}_{lat}.jsonl") for p in preds)]
            print(f"   lát {lat}: {co}" + ("" if len(co) == 3 else "   ⚠️ thiếu"))

if __name__ == "__main__":
    main()
