# report/73 — K1: kết quả kill-test bộ đối chiếu (hai chiều)

> VIỆC 0 trong report/72. Kiểm bộ đối chiếu lọc-bịa (embedding nomic-embed, τ=0.55) có đáng tin làm "trọng tài" không, theo hai chiều: bỏ-lọt bịa gần-nghĩa và kết-oan nút thật. Chạy trên **30 màn / 7 app** MobileViews (con số "127 màn" chỉ là mẫu số tính độ-phủ-VH, KHÔNG phải cỡ tập thử — vá 19/7), 130 cặp thử có nhãn-vàng gán theo chức năng. Code: `harness/k1_matcher_killtest.py`, số chi tiết: `harness/k1_results.json`. Ngày: 2026-07-18.

## Phán quyết 1 dòng

**KHÔNG ĐẠT.** Ở đúng ngưỡng pipeline (nomic τ=0.55), bộ đối chiếu **yếu cả hai chiều**: bỏ lọt **47,5%** bịa gần-nghĩa VÀ kết oan **47,5%** paraphrase thật (κ=0,38 — mức "vừa phải yếu"). Nặng hơn: đây **không phải lỗi chỉnh ngưỡng** — phân bố điểm của "paraphrase muốn nhận" và "bịa-gần-nghĩa muốn từ chối" **chồng lấn hoàn toàn** (40/40), nên **không τ nào tách được hai loại**. → phải **sửa trọng tài (pipeline)**, không phải chỉnh metric.

## Ba con số cốt lõi (tại τ=0.55, nomic — cổng thật)

| Chiều | Loại | Tỉ lệ sai | Ý nghĩa |
|---|---|---|---|
| **BỎ LỌT** (nguy hiểm) | bịa gần-nghĩa (nói "Send" khi chỉ có "Save") | **47,5%** (19/40) | ~nửa số bịa gần-nghĩa lọt vào data train |
| BỎ LỌT | bịa vô-quan ("Bluetooth" ở màn nghe nhạc) | 10% (2/20) | loại dễ thì bắt tốt |
| **KẾT OAN** (mất data) | paraphrase/dịch ("Tìm kiếm" cho "Search") | **47,5%** (19/40) | ~nửa bước đúng bị đánh oan là bịa |
| KẾT OAN | nhãn y hệt VH | 0% (0/30) | verbatim luôn nhận đúng (sanity OK) |

Tổng: precision bắt-bịa 67%, recall 65%, **κ=0,38**.

## Vì sao không chỉnh ngưỡng cứu được — bằng chứng cấu trúc

Điểm tương đồng (cosine) của hai nhóm gần như trùng nhau:
- **paraphrase thật** (nên ≥τ): median 0,562
- **bịa gần-nghĩa** (nên <τ): median 0,546
- **40/40** ca bịa gần-nghĩa có điểm ≥ điểm thấp nhất của paraphrase thật → **không có khe để đặt ngưỡng**.

Quét τ khẳng định đây là bập bênh: kéo τ lên 0,65 để bắt thêm bịa (bỏ lọt còn 10%) thì kết-oan paraphrase vọt lên 70%. Không τ nào cho cả hai chiều tốt; κ cao nhất chỉ 0,52.

## Đổi embedding có cứu được không? (trả lời câu hỏi "dùng OpenAI thì sao")

Chạy thêm **bge-m3** (embedding mạnh hơn nomic, có sẵn local): tách tốt hơn *một chút* (chồng lấn 30/40 thay vì 40/40; κ tốt nhất 0,59 thay vì 0,52) nhưng **vẫn không giải quyết** — bịa gần-nghĩa vẫn lọt nhiều. → **embedding mạnh hơn (kể cả OpenAI) chỉ đỡ chút, không phải lời giải.** Đúng như dự đoán: vấn đề thuộc bản chất (đo độ-gần-nghĩa không phân biệt "cùng nút khác chữ" với "khác nút gần nghĩa"), không phải chất lượng embedding.

## Hai chiều lỗi do hai cơ chế NGƯỢC nhau — đây là chìa khoá cách sửa

Chạy thêm **so-chuỗi thuần** (token-Jaccard, không embedding) trên cùng tập:

| Bộ đối chiếu | Bỏ lọt bịa gần-nghĩa | Kết oan paraphrase |
|---|---|---|
| **Embedding (nomic)** | 47,5% ✗ | 47,5% ✗ |
| **So-chuỗi thuần** | **5%** ✓ | **97,5%** ✗✗ |

So-chuỗi **bắt được bịa gần-nghĩa** (vì "Send" khác chữ "Save") nhưng **giết sạch paraphrase khác ngôn ngữ** ("Tìm kiếm" khác chữ "Search"). Tức hai cơ chế **hỏng ở hai trục ngược nhau** — không cái nào một mình thắng cả hai, và gộp AND/OR đơn giản cũng không (đã suy ra). Đây là lý do sâu nhất khiến trọng tài phải **đa-tín-hiệu + có cấu trúc**, không thể một-thước.

## Bối cảnh thêm: 37,6% nút không có chữ trong VH

Độ phủ nhãn VH = **62,4%** phần tử actionable có chữ. Nghĩa là **37,6% nút actionable không có chữ trong VH** (icon-only) — đây là nguồn **kết-oan thứ hai** mà không embedding nào cứu được (nút thật nhưng VH không có gì để khớp). Đây đúng chỗ **OCR (Vòng C / VIỆC OCR)** vào cuộc.

## Giới hạn của chính K1 (khai thẳng, đừng overclaim)

- **Tập thử là adversarial**: tôi cố ý chọn các ca bịa-gần-nghĩa KHÓ nhất và paraphrase KHÁC NGÔN NGỮ (Việt/Tây Ban Nha) — worst case. Phân bố bịa THẬT của gpt-4o-mini chưa biết → **K2 mới trả lời** "bao nhiêu % bịa thật là gần-nghĩa vs vô-quan".
- **Mẫu nhỏ** (40 cặp/loại khó) → các % có sai số rộng (~±15 điểm). Nhưng **phát hiện cấu trúc** (chồng lấn hoàn toàn; embedding vs chuỗi hỏng ngược trục) **vững** bất kể % chính xác.
- **Kết-oan bị thổi bởi cross-language**: với bài **FAIR (Anh–Anh)**, so-chuỗi kết-oan sẽ thấp hơn nhiều (paraphrase cùng ngôn ngữ vẫn trùng chữ phần lớn). Cross-language kết-oan là vấn đề riêng của **VCL**.

## Hệ quả cho luận văn

1. **Bắt buộc sửa trọng tài (đây là sửa PIPELINE, đúng như report/72 dự phòng).** Hướng: **so-chuỗi trước** (bắt bịa gần-nghĩa, nhận nhãn cùng-ngôn-ngữ) + **embedding phụ** + **OCR mở rộng nhãn** (cứu icon-only + tăng nhãn để khớp). Không chỉ đơn thuần bơm τ.
2. **Với FAIR (Anh):** so-chuỗi có vẻ là trọng tài tốt/bổ trợ — bỏ lọt bịa gần-nghĩa tụt 47,5%→5%. Cần K2 xác nhận trên bịa thật cùng-ngôn-ngữ.
3. **Với VCL (Việt):** có một quyết định thiết kế thật — hướng dẫn tiếng Việt nên **giữ nguyên tên nút hiển thị** (trích "Search") thay vì dịch ("Tìm kiếm"), vì (a) né được bẫy matcher, (b) hữu ích hơn cho người dùng (họ thấy chữ "Search" trên màn). Ghi cho bài VCL.
4. **Phải khai giới hạn của thước trung thực:** bộ chấm (bge-m3) cùng họ embedding → **cùng điểm mù** với bịa gần-nghĩa. Nên thước faithfulness phải khai "bắt tốt bịa-vô-quan, yếu với bịa thay-thế-gần-nghĩa" — và đây chính là chỗ **TN5 (hiệu chuẩn bge-m3 vs người)** và **TN6 (bơm lỗi)** sẽ lộ trần.
5. **Củng cố lý do thêm trục "ĐÚNG" (gold):** vì thước không-gold có điểm mù này, một trục đúng-sai bằng gold là tam-giác-hoá đáng giá hơn.
6. **KHÔNG freeze τ=0.55 vội.** Chỉ freeze τ SAU khi đã chốt trọng tài đa-tín-hiệu.

## Việc kế tiếp (đề xuất)

- **K2 (đếm phân loại bịa)** giờ là mắt xích quyết định: sinh/lấy output teacher thật, đếm bịa thật rơi vào loại nào (y-chữ / gần-nghĩa / vô-quan / ngoài-tên-nút). Nếu phần lớn là vô-quan → cổng embedding hiện tại "tạm dùng được"; nếu nhiều gần-nghĩa → phải sửa trọng tài trước khi build data.
- Mang **3 con số K1** (47,5% / 47,5% / κ=0,38 + chồng lấn 40/40) vào buổi gặp thầy như bằng chứng "vì sao cần nâng trọng tài".
- Cân nhắc đưa **so-chuỗi + OCR** vào bước lọc ngay từ đầu (thay vì nomic đơn).

> Tóm: bộ đối chiếu embedding-đơn **rớt K1** — không phải vì chỉnh sai, mà vì một-thước-độ-gần-nghĩa về bản chất không tách được hai loại. Đây là "hỏng có ích": nó chỉ thẳng cách sửa (trọng tài đa-tín-hiệu: so-chuỗi + embedding + OCR) và làm K2 thành việc bắt buộc tiếp theo.
