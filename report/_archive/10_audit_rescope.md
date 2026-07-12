# Audit + Debate rescope — Phán quyết & danh sách gap

> Kết quả workflow đa-agent (4 góc nhìn tranh luận đối kháng + audit 17 file). Đối chiếu với `09_rescope_research.md`.

## 1. Phán quyết debate: `appropriate-with-fixes`

4 góc nhìn ĐỒNG THUẬN: rescope **PHÙ HỢP về nền tảng** (không cần thay trụ cột metric/dataset/pipeline nào), **NHƯNG CHƯA sẵn sàng trình thầy** — còn lỗi citation chưa áp vào file thật + 3 lỗ hổng phương pháp/khoa học chưa đóng dứt điểm.

### Phản biện mạnh nhất (xếp theo nguy hiểm)

1. **[GÓC THẦY — nguy hiểm nhất, CÒN HỞ] "Tráo bài toán khó bằng bài toán dễ".** Câu hỏi gốc thầy = "làm sao model biết màn TIẾP THEO khi CHƯA THẤY" (predict unseen, open-world). Scope mới đưa SẴN N màn thật, model chỉ RE-SORT (closed-set, dễ hơn). File 05/06 claim "trả lời thẳng câu hỏi thầy" = **OVERCLAIM**. Phải tách bạch: DG2 trả lời "suy thứ tự GIỮA các màn ĐÃ quan sát"; phần predict-unseen đẩy future-work AGENT-NSI một cách CHỦ ĐỘNG.
2. **[PHƯƠNG PHÁP — CÒN HỞ] DG2 nguy cơ tầm thường hóa: GOAL-ONLY tự giải.** Goal AndroidControl mô tả thủ tục tuyến tính → LLM-text có thể suy thứ tự chỉ từ goal, không cần nhìn ảnh. Nếu GOAL-ONLY đạt τ-b cao ⇒ DG2 không đo "suy luận trật tự MÀN". Chưa nâng thành cổng cứng.
3. **[PHƯƠNG PHÁP — CÒN HỞ một phần] Vòng-lập-luận nhãn cặp-bắt-buộc chưa đóng hết.** Quy tắc tất định (B sau gold-action ở A) mã hóa y hệt cấu trúc nhân-quả mà 4/5 cue bắt → signal-attribution có thể thành tautology. D1 + audit người đã phòng một phần, nhưng cần TEST PHÂN-LY construct.
4. **[PHƯƠNG PHÁP — CÒN HỞ] "S0a tái dùng parser cho ordering" là KEEP SAI.** Ordering ăn feature đã-parse → recall OmniParser thành confound TRỰC TIẾP lên τ-b. Phải đổi: ordering reasoner đọc ẢNH THÔ là nhánh chính, parser chỉ ablation.
5. **[KHẢ THI — CÒN HỞ] Khối lượng vượt 1 luận văn thạc sĩ** (≈3-4 bài báo). File 09 nói "đã nhẹ hơn" nhưng chưa cắt gì cụ thể.
6. **[KHOA HỌC — CHƯA VÁ] Headline τ-b thiếu citation biện minh** "dùng τ chấm ordering" (đang chỉ neo Kendall 1938 + Gao). Phải áp Lapata 2006.

### Phản biện ĐÃ được trả lời (không phải must-fix)
- "Recall giết cả 2 nhánh" → delta C0-C4 triệt tiêu recall như hằng số (ĐK: gap #4 phải sửa).
- "N=3..8 không đủ episode" → 13,604 train ep, mean 5.5 → hàng nghìn ep/mốc, chỉ squeeze ở N≥9.
- "Ngân sách phi thực tế" → Qwen local gánh phần lớn (CẢNH BÁO: dòng chi phí thật ở ma trận 4-họ-judge §5.3 chưa tách).

## 2. Gap ưu tiên

### P0 — phải sửa TRƯỚC khi trình thầy
| # | File | Vấn đề | Cách sửa |
|---|---|---|---|
| P0-1 | 00_TONG_QUAN d.157 | Nhãn cặp-bắt-buộc suy từ "phát hiện cue" → SẬP chống-vòng-lập-luận D1 | Sửa: "suy từ GOLD bằng quy tắc tất định, KHÔNG từ bộ phát-hiện cue" |
| P0-2 | 05 d.139, 01 d.242/360, 03 d.340, 02 d.267 | OS-Atlas vẫn ghi "preprint" (sai: ICLR 2025) | "OS-Atlas (ICLR 2025, peer-reviewed)" |
| P0-3 | 05/06 + slide | OVERCLAIM "trả lời thẳng câu hỏi thầy" | Hạ giọng, tách 2 câu hỏi, predict-unseen → future-work |
| P0-4 | 05 (DG2 spec) | GOAL-ONLY chưa là cổng cứng | Pre-register: τ-b(GOAL-ONLY) ≥ τ-b(SELF) − ε trên ≥X% ep ⇒ lọc subset "goal-không-tiết-lộ-thứ-tự" |
| P0-5 | 01_metrics §4.4 | Headline τ-b thiếu Lapata 2006 | Áp Lapata 2006 (CL 32(4):471-484); giữ Gao ở vai meta-eval |

### P1 — nên sửa
P1-1 ordering đọc ảnh thô (sửa thiết kế, không "clarify"); P1-2 test phân-ly construct cho nhãn cặp; P1-3 đặt SÀN định lượng DG2; P1-4 đính chính lineage τ (Sort-Story=Spearman; RankGPT=phương pháp không phải metric); P1-5 gắn nhãn "adaptation" cho partial-order-τ; P1-6 KN đếm theo SỐ MÀN PHÂN BIỆT (không phải step); P1-7 làm rõ model judge §5.3 vs §8 + bảng chi phí tách theo baseline; P1-8 CẮT SCOPE (spine = chỉ Lapata + carry-over; hạ GUI-Odyssey/AMEX/Setwise/CLIPScore/VISUAL-ONLY xuống future/exploratory; ZH chỉ sanity; N headline ≤6); P1-9 tái-đóng-khung độ mới vào trục ĐÁNH GIÁ; P1-10 thêm mục "giá-của-rescope"; P1-11 trả lời tính thực-tế N-ảnh + bảng đối chiếu scope cũ/mới.

### P2 — nhỏ (biên tập)
−ε ở sanity (00/03b/07/08/build.js d.148); build.js d.252 "RANDOM≈0"→null empirical; build.js d.332 "reference-free" thêm "neo VH-silver"; bỏ cụm "đoán mù" câu phủ định; Mind2Web lý do +bbox-pixel-native; dòng tóm tắt đầu file "1 ảnh"→"1 hoặc N ảnh"; cite Chim CL 51(1):191-233 ở 06/00/BAI; CHANGELOG thêm disclaimer; 07 d.345 thêm VISUAL-ONLY.

## 3. Tuân thủ yêu cầu thầy
| Yêu cầu | Đạt? |
|---|---|
| Nhận 1 HOẶC N ảnh + câu hỏi use-case | ✅ (vài dòng tóm tắt đầu file còn ghi "1 ảnh" — P2) |
| Đơn ảnh DG1 bám màn → sinh hướng dẫn | ✅ |
| Đa ảnh N≥2 thật, đã xáo trộn | ✅ |
| Model tự sắp xếp rồi sinh | ✅ cơ chế (⚠️ yếu bởi GOAL-ONLY P0-4 + d.157 P0-1) |
| Cả 2 nhánh, trọng số gần ngang | ⚠️ DG2 chưa có SÀN cam kết (P1-3) |
| Đóng góp chính = phương pháp đánh giá | ✅ |
| Pipeline = hệ tham chiếu, không SOTA | ✅ |
| Trả lời câu hỏi gốc thầy | ⚠️ một phần (ordering-among-observed, không predict-unseen — P0-3) |

## 4. Kết luận
**CHƯA sẵn sàng trình thầy.** Nền tảng vững nhưng phải xử 5 gap P0 — đặc biệt: vá d.157 (vòng-lập-luận), bỏ "OS-Atlas preprint", hạ giọng "trả lời thẳng câu hỏi thầy" + tách predict-unseen sang future-work, nâng GOAL-ONLY thành cổng cứng, áp Lapata 2006. Rủi ro lớn nhất: thầy quy "tráo bài toán dễ" nếu không CHỦ ĐỘNG thừa nhận giá-của-rescope.
