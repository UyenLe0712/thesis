# Comparing Partial Rankings (Fagin et al. 2006) + Kendall's τ cho Information Ordering (Lapata 2006)

- **Link:** Fagin et al., *SIAM J. Discrete Math* 20(3):628–648 (2006) · Lapata, *Computational Linguistics* 32(4):471–484 (2006) · ⚠ *xác nhận link trước khi in*
- **Venue/năm:** SIAM J. Discrete Math 2006 · Computational Linguistics 2006.
- **Vai trong luận văn:** **tên đúng** cho thước **τ thứ-tự-bộ-phận** ở §5.2 (KHÔNG phải "Kendall τ-b").

## Paper này nói gì (cho người mới)
Khi hai thứ tự **không xếp hết mọi phần tử** (chỉ ràng buộc một số cặp — *partial ranking*), so chúng thế nào? **Fagin et al.** đưa cách đo khoảng cách giữa các **hạng bộ phận**. **Lapata** áp Kendall's τ để **đánh giá thứ tự thông tin** trong sinh văn bản (cặp nào đúng chiều, cặp nào ngược).

## Điểm cần biết
- Cho phép **chỉ phạt những cặp bắt buộc**, bỏ qua cặp tự do → đúng cái ta cần cho quy trình GUI có bước hoán đổi được.
- Là **tên gọi chuẩn** cho công thức τ = (C − D)/|M| của ta.
- Tránh lỗi trích dẫn: **không** gọi nhầm là "Kendall τ-b".

## Dùng refer gì cho bài của tôi
- **Trụ** cho Định nghĩa 5.4 (τ thứ-tự-bộ-phận, chỉ phạt cặp bắt buộc).
- Biện minh: nhãn cặp-bắt-buộc suy từ **gold** (nhân quả), cặp tự do đảo vẫn đúng.
- ⚠ Ghi đúng venue/tác giả — giám khảo dễ bắt lỗi chỗ này.

## Ghi chú attribution (R-08 — để chặt hơn)
- Ca **"cặp tự do / không-so-được" (incomparable pairs)** khớp chính xác hơn với **Brandenburg, Gleißner & Hofmeier (2012/13)** — còn Fagin gốc bàn về *ties / bucket-order*. Nên trích thêm Brandenburg cho phần cặp-tự-do.
- Khai đây là một **near-metric dùng để CHẤM ĐIỂM**: khi $p=0$ nó **không** thoả bất-đẳng-thức tam-giác (theo chính Fagin) → **tránh** gọi "the correct measure"; gọi là *"thước thứ-tự-bộ-phận ta dùng"*.
