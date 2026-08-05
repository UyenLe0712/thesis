# report/89 — Review deck v5 trình thầy

> Ngày 2026-07-19. Tổng hợp 3 góc: (1) mạch chuyện & thuyết phục, (2) thầy phản biện khó tính, (3) trình bày & giọng.

## Phán quyết 1 dòng

**Cần sửa vài chỗ — KHÔNG phải làm lại.** Xương sống câu chuyện ("có kế hoạch → tự bỏ tiền túi kiểm rẻ → phát hiện kế hoạch sai → xoay hướng có căn cứ → kiểm setup bằng số → xin ý kiến") là tài sản lớn nhất, giữ nguyên. Rủi ro nằm ở **3 lỗ dễ bị vặn** + **slide 4 (cao trào) đang bị số đè nên chưa nổ**. Vá xong là dùng được.

## Giữ nguyên (điểm mạnh — cả 3 góc đồng thuận)

- **Arc "tự giết ý tưởng của mình trước khi tiêu tiền" (slide 3→4)** — mạch của người làm khoa học trưởng thành, thầy tin hơn sau slide 4. Đây là vũ khí mạnh nhất, đẩy lên chứ đừng xin lỗi vì nó.
- **Ba điểm trung thực chủ động:** khai in-distribution (s6), khai "cái mới ở tác vụ không ở 3B on-device" (s9), khai teacher 30% không sàn-0 (s8). Phơi điểm yếu trước khi bị vặn = ghi điểm.
- **Slide 8 có cột MDE + "không scoop"** — cho thấy biết lo power & novelty trước khi chạy; ít thạc sĩ nghĩ tới MDE.
- **Slide 11 kết bằng 3 câu hỏi cụ thể** — đúng thể loại "báo tiến độ", không lan man. Giữ.
- **Ẩn dụ thầy-trò nhất quán** (s3/6/8) + không dính cụm sáo AI — chất giọng người, khai thác tiếp.

## PHẢI SỬA (ưu tiên cao trước)

| Slide | Vấn đề | Sửa cụ thể |
|---|---|---|
| **6-9 (xuyên deck)** | **LỖ TO NHẤT — mâu thuẫn human-instruction vs machine-gold.** S9 claim "sinh hướng dẫn cho NGƯỜI"; s6-8 lại đo bằng gold AndroidControl = chuỗi thao-tác cho MÁY. Thầy đập: "thước đo con agent, không đo bài hướng dẫn cho người → hoặc claim 'cho người' giả, hoặc thí nghiệm không kiểm được đóng góp". | Tách bạch 2 trục trên slide: gold-action = **proxy tính-ĐÚNG của bước**; tính-hữu-ích-cho-NGƯỜI đo riêng (định tính/người). Nói thẳng: dùng action-correctness làm proxy vì hướng-dẫn-chữ vẫn KHÔNG có gold. |
| **2 ↔ 5** | Mâu thuẫn lý-do-tồn-tại: s2 dựng đề tài trên "không có đáp án mẫu", s5 xoay sang AndroidControl (CÓ gold) → s5 tự đấm s2. | Thêm 1 câu bắc cầu ở s5 nối về s2: *"AndroidControl cho ĐÁP ÁN mà khó (a) còn thiếu; và vì bịa hoá ra hiếm (khó b), ta dời trọng tâm sang ĐO ĐỘ ĐÚNG."* Vá luôn mâu thuẫn + biến pivot thành đỉnh câu chuyện. |
| **4** | **Cao trào bị quá tải + tự tố:** nhồi 4 số nặng (47,5/47,5/0-2%/35-40) cho 2 kill-test; title "4 phép thử" nhưng chỉ tả K1,K2; hai số 47,5% trùng khít trông như bịa. | (a) Đổi title → **"2 phép thử quyết định"** (hoặc để K3,K4 là dòng mờ nhỏ). (b) Chuyển chữ thành HÌNH: K1 = hai phân phối điểm chồng lấn (không ngưỡng nào tách); K2 = 1 con số lớn "~0-2%, không phải ¼". (c) Đưa số THÔ + cỡ mẫu (vd 19/40) thay % tròn đối xứng; thêm chú thích nguồn 2 số 47,5%. |
| **8** | **AUC 1.00 là cờ ĐỎ, không phải cờ xanh.** Tự dựng cặp lỗi-vs-paraphrase rồi tự đo tách sạch → đương nhiên tách. Title "ĐÃ KIỂM BẰNG SỐ" khiến tưởng đã có kết quả MODEL (thực ra chưa train). | Đổi title → **"SETUP đã sẵn sàng — kiểm bằng số"** (rõ: số HẠ TẦNG, chưa phải hiệu-năng model). Cạnh AUC ghi ngay: n=?, ai gán nhãn, cặp khó lấy từ dữ liệu THẬT hay tự bịa, có held-out không. Không có mấy dòng đó thì 1.00 là gánh nặng. |
| **9** | **"Đầu tiên sinh hướng dẫn cho người" = claim tuyệt đối nguy hiểm.** Có dòng tutorial-generation/how-to; thầy nêu 1 phản ví dụ là "first" sụp. "Không scoop" (s8) ≠ chứng minh first. | Hạ tông: *"khác hướng chủ đạo (sinh thao-tác cho MÁY) ở chỗ sinh hướng-dẫn-chữ cho NGƯỜI + ràng buộc trung thực"*. Bắt buộc thêm bảng related-work 3-5 bài gần nhất, cột "họ làm / em khác ở đâu". Cược novelty vào phát-hiện-thực-nghiệm + cặp-thước, KHÔNG vào chữ "đầu tiên". |
| **6** | **Học-trò vs Thầy-gốc là bar THẤP:** trò train trên gold thắng gpt-4o-mini zero-shot 30% là hiển nhiên. Và faithful-distillation tụt xuống toggle bật/tắt → "model còn gì mới ngoài QLoRA-fine-tune-trên-gold?" | Thêm baseline mạnh hơn (Qwen fine-tune KHÔNG distill, hoặc few-shot teacher). Cho nhánh MobileViews-phụ một lý-do MỚI (đa dạng ngôn ngữ/độ phủ, KHÔNG còn là lọc-bịa). Nói rõ đóng-góp-model còn lại là gì. |
| **6** | "app CHƯA THẤY" + "in-distribution" nghe mâu thuẫn; held-out-by-app = generalization YẾU. | Thêm 3-4 chữ phân biệt: "app mới nhưng cùng phân phối dataset, chưa phải cross-dataset". Thêm 1 câu biện minh (chuẩn ngành held-out-by-app + phạm vi mùa này; OOD/cross-dataset để bài mở rộng). |
| **7** | "Thước MỚI" = over-claim: tách (thao-tác, đích) + khớp từ-lõi ≈ chính step-accuracy của AndroidControl. Bị bóc là đồ có sẵn thì mất uy. | Đóng khung thật: **"mượn step-accuracy kiểu AndroidControl + thêm luật khớp-đích để né đúng bẫy K1"** — đừng gọi "thước mới". |
| **8** | MDE 8-9pp lập luận hở: "dưới ngưỡng 15-20 → đủ lực" nhưng 15-20 ở đâu ra? Nếu hiệu ứng thật 5pp thì nằm DƯỚI MDE → null lẫn với "không tác dụng". | Nói rõ 15-20pp dựa tiền lệ nào; thú nhận rủi ro nếu hiệu ứng thật nhỏ hơn. Thêm nửa câu định nghĩa MDE cho người ngoài thống kê: "cỡ khác biệt nhỏ nhất mình đủ sức phát hiện". |
| **9 (nâng)** | Đóng góp 2 ("cặp thước + phát hiện") nghe như kết quả phụ. | Nâng bằng cách gọi tên finding tái-dùng-được: **"VH không đủ tin cậy làm chuẩn-vàng cho faithfulness (35/40 ca 'bịa' thực ra là VH thiếu nhãn)"** — đây mới là thứ người khác trích lại. |
| **10** | Thiếu dòng thời gian/khả thi — báo tiến độ mà không có mốc, thầy hướng dẫn luôn lo "có xong không". | Thêm 1 dòng mốc train/chấm (mấy tuần, có kịp mùa này không). Đổi 2 cột chữ → thanh tiến độ/checklist trực quan (5 xong ✓ / 5 chờ). |
| **3** | VH xuất hiện lần đầu không giải nghĩa → s4 (K1/K2) mất lực vì khán giả chưa neo VH là gì. | Thêm cụm 4-5 chữ tại chỗ: "danh sách nút thật của màn hình do hệ điều hành cung cấp". |

## Câu thủ cho chỗ thầy dễ vặn

- **"Metric đo agent chứ đâu đo hướng dẫn cho người?"** → gold-action = proxy tính-ĐÚNG của bước; tính-hữu-ích-cho-người đo riêng bằng đánh giá định tính/người. Hai trục tách bạch, không lẫn.
- **"Sao không kiểm giả thuyết ¼ trước khi xây cả hướng?"** → *"¼ là số PILOT sơ bộ (1 model, n nhỏ), bọn em đã gắn cờ 'chưa chắc' và đăng-ký-trước 4 cổng kiểm MIỄN PHÍ. Kiểm nó tốn 0đ, nó rớt, nên đổi. Cái đắt là train model dựa trên giả thuyết chưa kiểm — bọn em tránh đúng cái đó."* Đóng khung: kỷ luật, không phải vá víu.
- **"AUC 1.00 sao đẹp thế?"** → đo trên tập chẩn (probe) có nhãn, n=__, gồm cả ca khó paraphrase; KHÔNG phải số kết quả train. (Phải có sẵn cỡ mẫu + nguồn cặp khó.)
- **"App chưa thấy mà in-distribution?"** → app mới nhưng cùng phân phối dataset (held-out-by-app, chuẩn ngành); cross-dataset/OOD để bài mở rộng, ngoài phạm vi mùa này.
- **"Thắng teacher 30% zero-shot chứng minh được gì?"** → đó là lưới an toàn (Tier 1); trụ chính là Tier 2 tắt-VH + thêm baseline Qwen-fine-tune-không-distill để so công bằng.
- **"Thước này khác gì step-accuracy AndroidControl?"** → không claim thước mới; mượn step-accuracy + thêm luật khớp-đích để né bẫy K1 (bịa nghe-giống / nút gọi-đúng-bằng-từ-khác).
- **"3B thì có gì mới?"** → cái mới ở TÁC VỤ (đặt đúng khung đo + phát hiện thực nghiệm), không ở kiến trúc 3B on-device. (giữ nguyên, đây là phòng thủ tốt.)

## Thiếu hình ở đâu

- **Slide 2:** ảnh 1 màn app + bong bóng câu hỏi → mũi tên → 3 bước output (I/O trong 1 hình). Cái khó (b) "bịa tên nút" xứng 1 hình minh hoạ.
- **Slide 3:** sơ đồ 3 hộp thầy→lọc(VH)→trò (bắt buộc nếu đang là danh sách chữ).
- **Slide 4 (QUAN TRỌNG NHẤT):** hai phân phối điểm khớp (bịa vs thật) chồng lên nhau, tô vùng chồng lấn = "không ngưỡng nào tách". Một hình thay cả đoạn 47,5%+47,5%.
- **Slide 6:** sơ đồ luồng 2 nguồn dữ liệu → 1 model → đo trên app-mới → so teacher ("kiến trúc cuối").
- **Slide 7:** tách câu "Chạm tab Gmail" → [thao-tác: chạm | đích: Gmail], đặt cạnh "tab Calendar" để lộ chỗ khác từ-lõi. Giữ ví dụ này làm trung tâm, để to.
- **Slide 10:** thanh tiến độ/checklist trực quan thay 2 cột chữ.

## Ghi chú giọng (góc 3)

- Giảm bệnh gạch-ngang-ghép-từ ("nghe-giống", "gọi-đúng-bằng-từ-khác", "chồng điểm") — nhất là slide 4, mật độ hiện tại đọc giật cục. Giữ gạch nối cho thuật ngữ thật, bỏ ở cụm mô tả thường.
- Nguyên tắc: **SLIDE in cụm danh từ ngắn + con số; NGƯỜI nói câu đầy đủ.** Nhãn slide 8 rút xuống 3-5 chữ, phần giải thích để nói. Hai câu (a)(b) slide 2 và câu K1 slide 4 đang nhét cả lời nói vào slide.
- "teacher 30%" đọc thẳng "ông thầy cũng chỉ đúng 30%" — tự nhiên hơn.
