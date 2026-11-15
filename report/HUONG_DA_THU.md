# CÁC HƯỚNG ĐÃ THỬ — đọc trước khi đề xuất, viết runbook/mã, hay đẩy GPU (cập nhật 15/11/2026)

File này được `CLAUDE.md` nạp tự động (`@report/HUONG_DA_THU.md`) nên mọi phiên đều thấy.

**Luật bắt buộc cho trợ lý:**
1. Trước khi đề xuất một hướng mới, hoặc trước khi viết mã/runbook/notebook cho một hướng, tra bảng dưới. Trùng (kể cả đổi tên, đổi chút cấu hình) thì **phải nói rõ "đã thử ngày …, kết quả …, lý do dừng …"** và chỉ đề xuất lại khi nêu được **điểm khác cụ thể** làm kết quả có thể đổi.
2. Số ghi ở đây là số đã báo trong report gốc; trích vào bài thì mở report gốc kiểm lại. Số **[val]** cấm trích.
3. Có kết quả mới (một hướng xong hoặc dừng) thì **thêm một dòng vào đây** cùng lúc với report/320 và report/334.
4. Thư mục `_bundles/`, `_scripts/`, adapter của hướng đã dừng đã xoá khỏi máy nhà 15/11; lấy lại phần trong git bằng `git log --all -- <đường dẫn>` rồi `git checkout <commit>^ -- <đường dẫn>`; phần ngoài git ở GitHub Release `stopped-fgrb-tage-v1` và `stopped-misc-v1` (`gh release download <tag>`).

Mốc số test (4.463 bước chạm, exec UGround): câu chuẩn 75,73 · S1/101 59,11 · S1/202 59,6 · Base 47,59. MDE ghép cặp ~2,1. Hai hạt GRPO cùng công thức lệch 0,72–0,92 ⇒ chênh < 1 điểm ở một hạt là không phân biệt được.

## 1. Đang dùng / phương pháp hiện hành (KHÔNG phải hướng đã bỏ)

| hướng | trạng thái | số chính | nguồn |
|---|---|---|---|
| GRPO + SPICE từ S1 (ck500) | phương pháp đề xuất trong luận văn | exec 60,65; − S1/101 +1,55 [+0,80; +2,33]; hạt 202 +0,83; A/A train lại 59,74 (không tái lập) | report/259, 320 §14 §21 |
| ACE / R3 (ck500 + luật ghép câu `ra_k4`) | mở rộng trong luận văn | 7/7 độ đo văn bản hơn ck500, exec 60,68 ≈ ck500 | report/304 §4–5 |
| GRPO + SA-SPICE-v3 từ SFT-cont, ck400 | kết quả mới nhất, một hạt | exec 61,21; − SFT tiếp +1,05 p=7e−4; − ck500 +0,56 p=0,069; **back không chạm 71,1 → 58,5** | report/320 §29, 333 |
| SPICE-MATCH (SPICE thuần từ SFT-cont) | đang chạy Colab L4 15/11 | — | memory colab-chay-15-11 |
| Thước: exec (tiêu đề) · D.3 · AitW đầy đủ 77,3 → cận trên 85,0 · Phi-4 SoM · UI-Venus | chốt, đừng mở lại | | CLAUDE.md khối 13/9, 14/9 |

Việc còn chờ (chưa thử): `report/336` (DPO trực tuyến, SA hạt 401/503, SPIDEr/chrF/BLEU/BERTScore từ S1, SA + câu nhắc phân tầng, Dr.GRPO chạy nốt, A2C/DQN/TRPO/MIXER/MRT).

## 2. Đã thử và DỪNG — đừng đề xuất lại nếu không có điểm khác cụ thể

### 2a. Đích sinh, SFT, học ưu tiên (tháng 8–9)
| hướng | kết quả | lý do dừng | nguồn |
|---|---|---|---|
| S2 (descriptor `<desc>` trước câu) | exec 57,2, − S1 −1,93 (thua dưới cả UGround lẫn UI-Venus) | âm, một hạt; S2/202 không chạy (user 23/8) | report/106 x12, 119 |
| S2r, S2-nopoint | không train | đo được ô toạ độ là ô gánh; s2r thiết kế để thua; đắt gấp đôi | report/117 |
| MIN-DESC (ORPO tầng khai báo từ S2) | 60,05; − CE2 +0,63; − S1 +0,94 p=0,11 | trắng, 78–88% mức tăng thuộc nhánh so sánh | report/106 x12 |
| MIN-ONPOLICY | eligibility 3,3% < 25% | lỗi khai báo lưỡng cực (trung vị lệch 351 px), không phải lẫn nút cạnh | report/106 x13 |
| `gui_orpo_hard`, ORPO tầng câu, `gui_sft_match` | không chạy | công ORPO đã đo = +0,63; trần ORPO câu là hiệu ứng chọn mẫu; phản thực 59,44 | report/151 §2.2 |
| `gui_sel` (khối ≤40 ứng viên + đầu chọn) | exec 56,13; cổng G6 trượt (57,5 < 63,6) | bỏ cuộc quá mức 27%; τ: null thắng | report/136, 142 |
| GRPO `<point>` (thưởng toạ độ tự khai) | khai báo +2,56 nhưng exec +0,02 (60,07) | đổi khai báo không tới câu (66,7%) | report/144 |
| Nội suy MIN↔GRPO (V2), soup ba adapter (V3) | V2 đơn điệu, argmax = GRPO; V3 bỏ | không cho gì | report/153 |
| VIS-SFT (mở tháp thị giác) | K1 step3200 −7,50 so MIN [val] | chạm ngưỡng dừng, không có số test | runbook colab_vissft_9_9 |
| Đổi backbone Qwen3-VL-4B / Qwen2.5-VL-7B train | không chạy | trần chặn bởi độ phủ ứng viên; vỡ ngân sách | CLAUDE.md 30/8 |
| Qwen2.5-VL-7B prompting (mốc ngoài) | exec 51,5 | chỉ làm mốc | report/320 G12 |
| OCR / cây trợ năng vào đầu vào, vá tên bằng OCR, chưng cất bộ trỏ thứ hai, đa nhiệm hộp/toạ độ, Spatial CoT, gộp nhánh ở đầu ra (oracle 72,8, bộ chọn ≤60,45), MBR lúc suy luận | bác bằng số | | report/151 §2.2, 208 |

### 2b. Kênh vị trí, bộ chọn, sửa câu (tháng 9–10)
| hướng | kết quả | nguồn |
|---|---|---|
| DCRP (cặp target-vs-distractor) | G0 FAIL, trần +0,97 < 3,0 | report/183 |
| PATA-C1 (TARGET token + localizer + bridge) | localizer học (hit 52%) nhưng bridge không đổi câu, cổng cuối trượt | report/194 |
| PATA-C2 | S không phân biệt G với phần tử lân cận (ΔGD 0,004) | report/205 |
| ECGR | G0 147/958 < 250 | report/206 |
| FGRB (tiêm role/zone vào S1) | P2: BLEU-4 −0,03, cổng tự đóng | report/207 §8–11 |
| TFVF (làm nét vùng đích) | G>F chỉ 1/3 thước, S1 phản ứng biến đổi ảnh không theo vị trí | report/238 |
| Selector màn sau (distill) | thua greedy cả ba thước [val] | report/233 |
| TRIAD-T / POB | C2 net 0; nghẽn ở bộ định vị chỉ-ảnh | report/274–275 |
| TAGE (biên tập theo vùng cắt + cổng τ) | test 60,23 vs ck500 −0,43; τ không chuyển val → test | report/267, 269 |
| CTG-GRPO (A3/A2) | test A3 − S1 −1,72, back −2,96 vs A2; không gỡ tác hại ck500 | report/279 |
| 288 người nghe Phi-4 làm thưởng (SPICE-cont, +LR, +GLR) | không nhánh nào qua sàng +0,5 [val] | report/289 |
| RA-SFT (khối 4 ví dụ) train tiếp ck500 | 1/5 thước hơn ck500 ở cả hai LR; `ra_k4` đứng một mình exec −1,25 | report/304 |
| CW-RA (thẻ COPY/WRITE) | test exec −2,13 vs ck500, thua 7/7 thước | report/310 |
| RA-GRPO | G0: S1 nhìn khối ví dụ thì kém hẳn | report/312 |
| RAFT từ ck500 | exec −0,43 p=0,046 | report/314 |
| GA-DPO (ngoại tuyến) | không học (acc 0,544); mẫu "trội greedy" không có tín hiệu chung | report/314 GADPO |
| xao101 (SPICE ghép ngẫu nhiên, kiểm soát) | = S1 (59,11); ck500 − xao101 +1,55 | report/320 |

### 2c. Lưới RL và trục thưởng (tháng 11, từ S1, một hạt 101, 500 bước)
| lượt | exec test | so ck500 | nguồn |
|---|---|---|---|
| SFT tiếp (cùng câu nhắc) | 60,16 | −0,49 p=0,11 | report/320 §18 |
| REINFORCE + SPICE | 60,00 | −0,65 p=0,009 | §18 |
| RLOO + SPICE | 59,44 | −1,21 p=4e−6 | §18 |
| SCST + SPICE | 60,54 | ngang | §14 |
| PPO (GAE λ=1 / 0,95, 1000 bước) | 60,07 / 59,98 | ngang, thấp hơn ở BLEU-4/CIDEr-D | §28, report/334 |
| Dr.GRPO | treo ở 475, chưa chấm | user để sau | §20 |
| GRPO + ROUGE-L / METEOR / CIDEr-D | 60,63 / 60,27 / 60,27 | ngang; CIDEr-D thấp CIDEr-D −5,53 (không do df/tách từ) | §14, §22 |
| RGTC-SPICE | Gate B phủ 10,3% (bỏ danh sách 34,8%); T trượt, FULL < chrF | dừng | §24–25 |
| Biến thể thưởng SPICE R2–R4 (sàng tĩnh) | không hơn chrF một mình [val] | chỉ sàng, chưa train | §23, report/332 |
| GRPO + chrF từ SFT-cont, ck400 | trượt ở bước không chạm trên DEV-v3, không chấm test | | report/333 |

Kết luận đã chốt của trục này: không lượt nào hơn ck500 có ý nghĩa; cả nhóm hơn S1 +1,2…+1,5 ⇒ chỉ viết "nhóm dẫn đầu", cấm "SPICE tốt nhất". SPICE dự báo exec kém hơn CIDEr-D/METEOR/chrF trên mẫu tĩnh (report/328, 330).

### 2d. Thước đo / dụng cụ đã đổi thử
| hướng | kết quả | nguồn |
|---|---|---|
| Bộ trỏ mạnh hơn (UI-Venus-7B) làm thước chính | điểm thấp hơn cả ba nhánh; giữ làm kiểm độ bền | CLAUDE.md 30/8 |
| Luật dung sai ±14% (d14) làm tiêu đề | 86% mức tăng là thứ câu rỗng nghĩa cũng lấy được | report/151 §6 |
| AitW với mọi khung bấm được | sàn câu rỗng 41,6 ⇒ chỉ cận trên | CLAUDE.md 14/9 |
| Pixtral-12B người nghe | 8,0 do lỗi định dạng | report/155 |
| CLIPScore làm thưởng | P(đổi động từ > sai tên) 0,690, quá yếu | report/330 |
| Hợp nhất hai bộ trỏ | nâng đều mọi nhánh, tỉ lệ không đổi | report/138 |
| Chấm tay 100 câu | user quyết không làm | CLAUDE.md |
