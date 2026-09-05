# -*- coding: utf-8 -*-
"""Sinh `kaggle_DEM_4_9_BAY_O.md` — bảy ô dán tuần tự — từ runbook gốc
`kaggle_commit_sel_4_9.md`.

Vì sao có tệp này: runbook gốc xếp theo CHỦ ĐỀ (ô chung, C1, C2, C3) nên lúc dán phải
nhảy giữa bốn mục, dễ sót hoặc sai thứ tự. Bản dán tuần tự thì chép tay là sinh ra bản
thứ hai, và hai bản sẽ lệch nhau sau vài lần sửa. Nên bản tuần tự được TRÍCH tự động.

    python harness/make_7o.py

Sửa nội dung ô thì sửa runbook gốc rồi chạy lại, đừng sửa tệp sinh ra.
"""
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.join(HERE, "kaggle_commit_sel_4_9.md")
RA = os.path.join(HERE, "kaggle_DEM_4_9_BAY_O.md")

# chỉ số khối mã trong runbook gốc, theo THỨ TỰ DÁN (khối 0 là ô cuối §0.1, nằm đầu tệp)
THU_TU = [(1, "Ô 1 — cài gói và GỠ torchao"),
          (2, "Ô 2 — dựng workspace, kiểm hai hash"),
          (3, "Ô 3 — hàm chạy-và-chờ"),
          (4, "Ô 4 — tiền bay + dựng danh sách 3.063 bước"),
          (7, "Ô 5 — suy luận 3.063 bước (~4 h)"),
          (8, "Ô 6 — soi tệp pred"),
          (0, "Ô 7 — gộp 4.463 + cổng giờ + chấm exec (~5,6 h)")]

DAU = """# Kaggle đêm 4/9 — BẢY Ô DÁN TUẦN TỰ

Sinh tự động từ `kaggle_commit_sel_4_9.md` bằng `harness/make_7o.py`. **Đừng sửa tay tệp này** —
sửa runbook gốc rồi chạy lại lệnh sinh, nếu không hai bản sẽ lệch nhau.

Dán đúng bảy ô dưới đây, theo đúng thứ tự, mỗi khối một ô notebook. Không thêm ô nào khác.
Ô probe 3 bước là ô chạy TAY một lần trước khi commit, **không** đưa vào notebook đem commit.

Trước khi bấm: Accelerator **GPU T4 x2** · Internet **On** · ba input đã gắn
(`thesis-sel-infer` bản mới nhất · `thesis-score` · `gui-sel-adapter`).

Bấm **Save Version → Save & Run All (Commit)**.

---
"""

CUOI = """---

## Sáng dậy — tab Output phải có bốn tệp

| tệp | nghĩa |
|---|---|
| `preds_gui_sel_seed101_rest3063.jsonl` | 3.063 câu sinh mới |
| `preds_gui_sel_seed101_touch4463.jsonl` | gộp với lát dev, đủ mẫu số |
| `score_gui_sel_seed101.json` | **số exec** |
| `score_gui_sel_seed101_raw.jsonl` | tệp thô, giữ bằng mọi giá |

Thiếu hai tệp cuối nghĩa là cổng giờ đã cắt phần chấm. Đọc dòng `⛔ BỎ phần chấm` trong đầu ra
của ô 7, rồi chấm `exec` bằng mục **C2** của runbook gốc thành một commit riêng — tệp gộp 4.463
đã có sẵn nên commit đó chỉ còn đúng một việc.

Tải về đặt thẳng vào `runs/sel/`, đừng để lạc sang thư mục khác.
"""


# ── Lượt thứ hai: sequence-score trên lát dev 1.400 (mục C3 của runbook gốc) ─────
RA_C3 = os.path.join(HERE, "kaggle_SEQSCORE_SAU_O.md")

THU_TU_C3 = [(1, "Ô 1 — cài gói và GỠ torchao"),
             (2, "Ô 2 — dựng workspace, kiểm hai hash"),
             (3, "Ô 3 — hàm chạy-và-chờ"),
             (11, "Ô 4 — kiểm API bộ nhớ đệm (quyết định dùng được --cache-prompt hay không)"),
             (12, "Ô 5 — PROBE 50 bước, đọc bốn dòng rồi mới phóng"),
             (6, "Ô 6 — dọn tệp probe"),
             (13, "Ô 7 — lượt dài: 1.400 bước")]

DAU_C3 = """# Kaggle — sequence-score lát dev 1.400 (bảy ô dán tuần tự)

Sinh tự động từ `kaggle_commit_sel_4_9.md` bằng `harness/make_7o.py`. **Đừng sửa tay tệp này.**

Lượt này sinh điểm chuẩn hoá độ dài cho từng ứng viên và cho `none`, theo hợp đồng
`report/134` §6.1, đã đăng ký trước ở `report/106` mục **(x16d)**.

⛔ Tệp này **chỉ sinh điểm**. Quét ngưỡng τ là việc riêng, chạy trên máy nhà, 0 GPU, và phải
theo đúng thủ tục đã đăng ký — cực đại **độ đúng trên toàn bộ 1.400 bước** chứ không phải trên
nhóm HasAns, luật null nằm trong lưới quét, và khoá τ **trước** khi nhìn `exec` đối chứng.

Ba input như đêm qua. Accelerator **GPU T4 x2**, Internet **On**.

## Cách chạy — hai giai đoạn

**Giai đoạn 1, chạy TAY:** dán đủ bảy ô, chạy ô 1 → ô 6. Ô 5 là probe 50 bước, mất khoảng 5–10
phút, và là chỗ duy nhất biết được `--cache-prompt` có dùng được không cùng giây-mỗi-bước thật.
Đọc bốn dòng kiểm ở cuối tệp này.

**Giai đoạn 2, đem commit:** ⛔ **xoá ô 5 và ô 6 khỏi notebook**, còn lại **năm ô** — 1 · 2 · 3
· 4 · 7. Rồi **Save Version → Save & Run All (Commit)**, gập máy.

Vì sao xoá: mỗi ô gọi một tiến trình riêng nên mô hình nền được nạp lại từ đầu ở từng ô; để ô
probe trong notebook commit là tốn thêm một lần nạp cộng 50 bước tính vô ích. Ô 4 thì giữ — nó
chỉ in một dòng và là thứ chặn lượt dài nếu bản `transformers` trên máy ảo không cắt được bộ
nhớ đệm.

⚠️ Nếu ô 4 báo `crop: False`, bỏ cờ `--cache-prompt` ở ô 7 trước khi commit; lượt dài khi đó
tốn khoảng 4,7 giờ thay vì dưới 1 giờ, vẫn nằm dưới trần 12 giờ.

---
"""

CUOI_C3 = """---

## Bốn dòng phải đúng ở ô 5 trước khi phóng lượt dài

1. Ba dòng `kiểm chéo nhanh↔chậm: lệch tối đa ...` đều **dưới 1e-3**. Đây là thứ quyết định lượt
   dài tốn dưới 1 giờ hay khoảng 4,7 giờ. Script tự dừng nếu vượt; **đừng nới ngưỡng**.
2. `tok_none` chỉ có **một** giá trị — span `<sel>none</sel>` cố định nên số token phải bằng nhau
   ở mọi bước. Nhiều hơn một giá trị nghĩa là bộ tách token đang làm gì đó khác.
3. `s_none` và `s_star` đều **âm và cùng cỡ**. Dương là sai dấu; lệch nhau vài bậc là sai chuẩn hoá.
4. Giây mỗi bước **nhân 1.400 phải dưới 12 giờ**, có đệm.

## Sau khi có tệp

Tải `seqscores_gui_sel_seed101_dev1400.jsonl` về `runs/sel/`. Mỗi dòng có điểm của **mọi** ứng
viên cùng `s_none`, `margin`, số token — nên quét lại τ về sau **không phải gọi GPU lần nữa**.
"""


def main():
    s = open(GOC, encoding="utf-8").read()
    B = re.findall(r"```python\n(.*?)```", s, re.S)
    for ra, dau, thu_tu, cuoi in ((RA, DAU, THU_TU, CUOI),
                                  (RA_C3, DAU_C3, THU_TU_C3, CUOI_C3)):
        phan = [dau]
        for idx, ten in thu_tu:
            phan.append(f"## {ten}\n\n```python\n{B[idx]}```\n")
        phan.append(cuoi)
        open(ra, "w", encoding="utf-8").write("\n".join(phan))
        print(f"{ra} — {len(thu_tu)} ô")


if __name__ == "__main__":
    main()
