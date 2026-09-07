# Bản đồ kho — luận văn "Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM từ các trường hợp sử dụng và giao diện người dùng"

Học viên: Lê Đoàn Phương Uyên · GVHD: TS. Nguyễn Hồng Bửu Long · Khoa CNTT, ĐH KHTN – ĐHQG-HCM

> 👉 **Được mời đọc để phản biện? Mở `AGENT_BRIEF.md` trước** — nó nói rõ đọc gì theo thứ tự nào,
> cách tự tính lại số từ tệp thô, những đòn đã bị bác bằng số đo, và chỗ nào còn thật sự hở.

**Cần hiểu dự án thì đọc theo thứ tự:** `report/112_HIEU_TOAN_BO_KY_THUAT.md` (cơ chế) →
`report/109_BAN_DO_HIEN_TAI.md` (đang ở đâu) → `CLAUDE.md` (nhật ký quyết định).

---

## Thư mục

| Thư mục | Chứa gì | Ghi chú |
|---|---|---|
| `harness/` | **Toàn bộ mã**: dựng dữ liệu, huấn luyện, sinh câu, chấm điểm, runbook Colab/Kaggle | Script giải đường dẫn theo `__file__` nên di chuyển cả thư mục thì an toàn; **đừng đổi cấu trúc bên trong** |
| `report/` | Báo cáo tiến độ, bản đăng ký trước, sổ kê khai, ghi chú tài liệu | Đánh số tăng dần; số lớn hơn = mới hơn |
| `runs/` | Kết quả chấm điểm (`preds_*.jsonl`, `score_*.json`, `score_*_raw.jsonl`) | `runs/gate_a/` = kết quả cổng chặn bộ định vị |
| `thesis/` | **Luận văn LaTeX** → `thesis/main.pdf` | `./build.sh` để biên dịch; xem `thesis/README.md` |
| `paper/fair2026/` | Bài báo tiếng Anh (IEEEtran) | Đang **10 trang**, giới hạn hội nghị là 8 ⇒ còn phải cắt |
| `slides/` | Slide bảo vệ | Xem bảng dưới |
| `dataset_samples/` | Mẫu dữ liệu nhỏ để chạy thử tại máy | |
| `_bundles/` | Gói zip chuyển sang Colab/Kaggle | **Tái tạo được** bằng `harness/make_bundle.py`; không commit |

## Bên trong `slides/`

| Đường dẫn | Là gì |
|---|---|
| `slides/LUAN_VAN_SLIDE.pptx` | **Deck đang dùng** — chỉ một file, sửa tại chỗ rồi build đè, đừng đẻ bản v11/v12 |
| `slides/build/build_slide.js` | Script dựng deck (`cd slides/build && node build_slide.js`) |
| `slides/build/_preview/preview.html` | Xem nhanh deck trên trình duyệt |
| `slides/latex/` | Bản LaTeX/Beamer cùng nội dung |
| `slides/_reference/` | Mẫu style tham khảo |

## Bên trong `report/`

| Đường dẫn | Là gì |
|---|---|
| `report/1xx_*.md` | Báo cáo hiện hành |
| `report/papers/` | Ghi chú đọc tài liệu (một file một bài) |
| `report/paper_figures/` | Ảnh bảng cắt từ PDF gốc, dùng cho slide dự phòng |
| `report/_archive/` | Báo cáo của khung thiết kế cũ — **không có trong bản GitHub**, xem `AGENT_BRIEF.md` §7 |

**Khi hai file mâu thuẫn:** `report/106` thắng về *phải làm gì* · `report/108` thắng về
*đã đo được gì* · `report/109` thắng về *đang ở đâu* · `report/112` thắng về *cơ chế hoạt động*.

---

## Biên dịch / chạy

```bash
# Luận văn
cd thesis && ./build.sh                    # -> thesis/main.pdf

# Bài báo
cd paper/fair2026 && tectonic -X compile main.tex --outdir .   # -> main.pdf
#   ⚠️ đúng lệnh này, và kiểm `ls -la main.pdf` xem mốc giờ trước khi tin số trang

# Slide
cd slides/build && node build_slide.js     # -> slides/LUAN_VAN_SLIDE.pptx

# Chấm lại một nhánh (không gọi lại bộ định vị nếu đã có tệp thô)
python harness/score_run.py --mode score --grounder uground \
    --preds runs/preds_s1_seed101.jsonl --out runs/score_s1_seed101.json
```

---

## Ghi chú tái cấu trúc (16/8/2026)

Đã gom: `ppt_build/` → `slides/build/` · `ckpt/` → `runs/gate_a/` · `report/_papers/` →
`report/paper_figures/` · pptx và PDF mẫu về đúng thư mục của chúng. Đã xoá hai thứ rác:
một `_preview/` ở gốc trùng md5 với bản trong `slides/build/`, và một file `datasets` rỗng
0 byte.

**Cố ý KHÔNG đổi tên `harness/` và `report/`.** Hai tên này có 597 và 1991 tham chiếu trong
CLAUDE.md, các report, runbook Colab và trong layout gói zip mà lượt chấm đang chạy phụ thuộc
vào (`make_bundle.py` ghi đường dẫn `thesis/harness/...` vào trong zip, và runbook trên Colab
`cd` vào đúng đường dẫn đó). Đổi tên lúc chiến dịch huấn luyện đang chạy là rủi ro thật mà
lợi ích chỉ là thẩm mỹ.

⚠️ Chữ `thesis` xuất hiện ở hai nghĩa khác nhau, đừng nhầm: `thesis/` tại máy là **luận văn
LaTeX**, còn `thesis/` bên trong gói zip là **thư mục làm việc trên Colab** (tương ứng
`harness/` tại máy).
