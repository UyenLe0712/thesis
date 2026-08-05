# Chỉ mục archive — file nào bị thay bởi file nào

> Mọi file ở đây đều **đọc được, không xoá**. Chỉ chuyển ra khỏi `report/` để bớt cửa đọc nhầm.
> Nguyên tắc: nếu cần trích claim/số liệu → dùng file THAY THẾ ở cột phải, không trích từ đây.

## Đợt dọn 2026-07-18

| File archive | Bị thay bởi | Còn sót giá trị gì |
|---|---|---|
| `59_deepresearch_dang_do.md` (100K) | **`report/61`** — bản đã verify đối kháng (25 claim → 20 sống, 5 bác) | Chỉ mục **26 nguồn thô chưa verify**. Moi lại khi vòng research sau muốn xét nguồn không lọt vào bản chốt. ⛔ **ĐỪNG trích claim trực tiếp** — chưa qua verify. |
| `51_deepresearch_faithful_distillation_partial.md` (72K) | **`report/50`** (hướng đã chốt) + **`report/43` Ch.0** (đã gấp trụ citation: VGA EMNLP24, KnowAda NAACL25, BLIP-CapFilt ICML22, ALLaVA, LLaVA-KD ICCV25, VLsI CVPR25, Mind-the-Gap ICLR25) | Workflow `wf_45ce881b` treo ở synthesis cuối nhưng **verify đã xong: 39 claim sống / 18 bác** + 20 nguồn. Claim sống đã trích tay sang 43 → **không cần resume**. Giữ để tra nguồn gốc. |
| `58_review_fable_plan_hoan_thanh.md` (18K) | **`report/00 §5`** — lịch từng tuần + bảng mốc/gate đã rút sang đó, rebase 18/7, chèn thêm K1/K2 | Verdict review Fable 5 (Phần A: A1–A5 ĐẠT-CÓ-ĐIỀU-KIỆN) + lý lẽ 11 lỗi thực thi L1–L11 đã vá khi soạn plan bản 2. Mở khi cần biết *vì sao* lịch xếp như vậy. |
| `60_EXPORT_CONTEXT_2026-07-15.md` (40K) | **`report/00`** (mới hơn) | Định dạng "dán nguyên vào chat AI khác, không cần mở file nào". Nếu cần export lại thì **sinh bản mới từ `00` + `54`**, đừng dùng bản 15/7 (đã cũ). |

**Không archive dù cũng thuộc khung đã bị bác:** `report/43`, `47` — vẫn được `CLAUDE.md`/`54`/`38` trỏ tới làm log gốc. Muốn dọn thì phải sửa con trỏ ở 4–5 file trước. ⚠️ Bộ thí nghiệm **E1–E16** trong hai file đó là của khung prompting **đã bị thầy bác** — đừng trình nhầm; bộ thật là **TN0–TN7** ở `report/54`.

## Các đợt trước
37 file dọn trước 2026-07-18 (khung prompting cũ, bản nháp superseded). Xem `00_TONG_QUAN.md` / `00_DOC_TU_DAU.md` trong thư mục này.
