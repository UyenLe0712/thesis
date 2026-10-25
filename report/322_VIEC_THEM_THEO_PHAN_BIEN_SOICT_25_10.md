# 322 — Việc làm thêm cho phương pháp đóng góp chính, rút từ phản biện SOICT (ghi 25/10/2026)

Nguồn: bốn phản biện bài GUIStep (#5590), chép nguyên văn ở `paper/soict2026/guistep/EMAILS_SOICT_5590_22_10.md`.
Phạm vi: chỉ những gì làm mạnh **phương pháp đóng góp của luận văn** (GRPO thưởng SPICE = ck500, và luật ghép ACE/R3).
Góp ý về thước đo đã trả lời phần lớn (UI-Venus, Phi-4, Phi-Ground, bộ bơm lỗi dưới D.3, hạt giống 202 của ck500), xem `report/320` mục A, B, G.
Kết quả có số thì ghi vào `report/320` (theo luật làm việc), file này chỉ giữ danh sách việc và trạng thái.

## 1. Ba đòn còn lại nhắm vào phương pháp

| đòn | reviewer | tình trạng số hiện có |
|---|---|---|
| Mức tăng chủ yếu đến từ SFT, phần GRPO nhỏ và chưa tách khỏi "học thêm" | R2, R3 | ck500 − S1/101 +1,55, ck500/202 − S1/101 +0,83, đều dưới MDE 2,11 (`report/320` G4) |
| Một bộ dữ liệu, một backbone | R1, R3, R4 | chỉ AndroidControl, chỉ Qwen2.5-VL-3B |
| Không so với hệ nào bên ngoài | R2, R4 | chỉ so Base (cùng backbone) và `gui_sel` (biến thể nội bộ) |

## 2. Danh sách việc, xếp theo giá trị trên chi phí

| # | việc | trả lời | chi phí | trạng thái |
|---|---|---|---|---|
| 1 | Chấm test **xao101** (GRPO thưởng xáo trộn, cùng số bước, chỉ khác thưởng) | đòn 1 | ~5–8 h Kaggle T4 | ✅ XONG 26/10: xao101 59,11 = S1/101 (+0,00); ck500 − xao101 +1,55 [+0,81; +2,30] ⇒ report/320 G12 |
| 2 | Chấm zero-shot trên **AitZ** (2.736 bước chạm): Base, S1, ck500, ACE; không train lại | đòn 2 | ~4 × 2–3 h T4 | ✅ **XONG 26/10 (report/320 G12): S1 37,79 · ck500 37,28 (−0,51, KTC phủ 0) · ck500/202 36,62 · Base 34,50.** ▶️ **26/10 05:25 đẩy `trangphuongngoc/aitz-ace-tran`** (gói `_bundles/aitz_ace/`, dataset `trangphuongngoc/aitz-ace-kit`): trần câu chuẩn AitZ qua UGround + ACE/R3 (ra_k4 = `runs/ra304_T/ra_sft/final`, md5 f3c543b0, trùng adapter của lượt test 304; luật R3 tái lập pred_R3_test 4.463/4.463) + ra_k4 đứng một mình. Khối ví dụ dựng trên CPU (`xuat_ex_aitz.py`, tự kiểm 30/30 trùng ex_test_k4); khối chứa đúng câu chuẩn AitZ 0,0% (AndroidControl ~13%). Dự kiến ~4 h. Ghi chú cũ: nhận việc 25/10 tối (phiên khác): chạy trên tài khoản thứ ba `trang2` (`trangphuongngoc`)**, kernel `trangphuongngoc/aitz-gen-s1-ck500`: Base, S1 (hoà), ck500, ck500/202 sinh câu + chấm UGround trên 2.736 bước. ACE chưa (cần truy hồi câu ví dụ + mô hình RA), làm sau. Đừng đẩy trùng trên uyenle/trang. |
| 3 | Mốc so bên ngoài: **Qwen2.5-VL-7B-Instruct** prompting, cùng ảnh, mục tiêu, lịch sử, 24 dòng OCR, cùng câu nhắc với Base | đòn 3 | ~1 commit T4×2 (đo tốc độ ở ô thử) + chấm UGround | ✅ XONG 26/10: 7B 51,51; ck500 − 7B +9,14 [+7,55; +10,75] ⇒ report/320 G12 |
| 4 | Bảng bước không chạm cho ACE (ck500 đã có: scroll −6,23, `report/261`) | phạm vi (R4) | ~0 GPU nếu ACE chỉ đổi câu ở bước chạm, cần kiểm | ⬜ |
| 5 | Lịch sử do mô hình sinh thay cho câu chuẩn (S1, ck500), đo lỗi cộng dồn | R4 | ~2 × 5,6 h T4 | ⬜ xếp sau |
| 6 | Chấm tay 60–100 câu (dùng lại B7a của SOICT nếu làm) | thước (R2, R3, R4) | thời gian của user | ⬜ user quyết |
| 7 | Đo độ trễ và VRAM đỉnh lúc suy luận (3B vs 7B) | R2 | 0, lấy từ log của việc #3 | ⬜ đọc khi #3 xong |

Không làm: **backbone thứ hai** (SFT lại ~23 h A100 rồi GRPO, đắt nhất mà chỉ trả lời một đòn). Ghi thành giới hạn, kèm các phép kiểm qua ba bộ trỏ và (nếu xong #2) hai bộ dữ liệu.

## 3. Việc #3 — Qwen2.5-VL-7B-Instruct (chi tiết để chạy lại)

- Gói mã: `_bundles/qwen7b_script/` → dataset `trangphngngc/qwen7b-infer-script`: `infer_branch.py` (md5 `0eef768c…`), `build_branch_data.py` (md5 `619e63e1…`), `only_tap.jsonl` (4.463 bước click + long_press, md5 `7480ae6d…`).
- Kernel: `_bundles/qwen7b_kernel/qwen7b-test.ipynb`, dataset `thesis-score` (tập kiểm 6.958 dòng, 4.463 ảnh) + gói trên, T4×2, `device_map="auto"`, fp16, lô 4, `--no-adapter --base Qwen/Qwen2.5-VL-7B-Instruct`.
- Đã kiểm trên máy nhà 25/10: câu nhắc bản mã hiện tại **trùng 6.958/6.958** với bản 12/8 đã dùng chấm Base (cùng `SYS`, cùng `prompt_body`, OCR nạp theo khoá `image`). Vậy 7B và Base 3B nhận đúng một đầu vào; khác nhau chỉ ở cỡ mô hình.
- Ô 3 thử 8 bước, dừng nếu dưới 7/8 câu có chữ (phòng tràn số fp16 trên T4). Ô 4 chạy đủ, nối tiếp được, cắt ở 11,0 h. Ô 5 chấm UGround chỉ khi còn ≥ 3,2 h; không thì commit 2 gắn output commit 1 vào `kernel_sources` (ô 1 tự chép tệp dở sang).
- Phải khai khi báo: Qwen2.5-VL-7B cùng họ với mô hình của luận văn và cùng họ với UGround (Qwen2-VL); chưa kiểm 7B có thấy AndroidControl lúc huấn luyện hay không; prompting zero-shot, không tinh chỉnh câu nhắc riêng cho 7B (dùng nguyên câu nhắc của Base để so công bằng).
- Đọc kết quả: so 7B với Base 3B (47,59) và S1/ck500 bằng `score_run.cluster_bootstrap`, ghép cặp trên 4.463 bước. Thước chữ chạy thêm trên kernel CPU nếu cần.
