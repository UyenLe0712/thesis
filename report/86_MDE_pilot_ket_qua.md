# report/86 — Pilot đo-nền + MDE trục ĐÚNG

> Việc cuối khâu free-cốt-lõi (report/85 §6). Đo độ-dao-động điểm-đúng của teacher gpt-4o-mini trên ảnh thật AndroidControl → SD → MDE, để biết trục ĐÚNG có đủ lực thống kê không. ✱ Đã tốn API (~50-80 lượt gpt-4o-mini vision, ~$0.3-0.6). Code: `harness/mde_pilot.py`. Ngày: 2026-07-19.

## Phán quyết 1 dòng

**Trục ĐÚNG ĐỦ LỰC.** MDE ≈ **9 pp** (G=150) / **8 pp** (G=200) — dưới ngưỡng nguy hiểm 15-20 pp. Teacher gpt-4o-mini điểm-đúng = **30%** (per-bước) → **KHÔNG suy biến về sàn-0** (qua đúng cổng report/79 lo). → không cần đổi split; trục ĐÚNG chạy được.

## Số liệu (26 app app-unseen, ~85 bước)

- **Teacher điểm-đúng trung bình = 0.301** (per-bước: khớp loại-thao-tác VÀ khớp đích).
- SD per-app (một arm) = 0.256; SD-hiệu bảo thủ = √2 × 0.256 = **0.362**.
- MDE = 3.077 × SD-hiệu / √G:

| G (số app test) | MDE |
|---|---|
| 26 (pilot) | 21.9 pp |
| 100 | 11.1 pp |
| **150** (ước thực) | **9.1 pp** |
| 200 | 7.9 pp |

Vì split app_unseen thật có **G ~150-250 app** (report/85 §1) → **MDE thực ≈ 8-9 pp**.

## Đọc kỹ — mấy điểm phải hiểu đúng

1. **Teacher chỉ 30% không phải lỗi — là tác vụ khó + thước NGHIÊM.** Đoán đúng-y bước-kế-tiếp từ 1 ảnh + goal, khớp ĐÚNG bước gold người viết, là khó. Thêm nữa **thước per-bước phạt cả "bước hợp lệ khác gold"** (có nhiều bước-kế-tiếp hợp lệ, gold chỉ ghi một). → 30% là **cận dưới**; headline thật (coverage cả episode) sẽ cao hơn. **Giới hạn "nhiều-bước-hợp-lệ" phải khai trong luận văn.**
2. **MDE này BẢO THỦ (overestimate):** pilot chỉ 2-4 bước/app → điểm per-app nhiễu → SD phồng. Thực nghiệm thật nhiều bước/app hơn → SD nhỏ hơn → MDE nhỏ hơn. Nên 8-9 pp là cận-trên an toàn.
3. **Hướng hiệu ứng plausible DƯƠNG:** teacher = zero-shot; student sẽ **train TRÊN AndroidControl gold** → chấm in-distribution (app-unseen) → student có lợi-thế-sân-nhà so teacher zero-shot. **Student > Teacher-BASE trên độ đúng in-domain là kết cục kỳ vọng hợp lý** (không phải "học trò 3B nhỏ thua thầy lớn" như lo ở khung cross-dataset cũ).
4. **Không lộ hướng hiệu ứng student** (chỉ đo teacher + phương sai nền) → **không phá pre-registration**.

## Điền vào bản đăng-ký-trước

- **[MDE trục ĐÚNG = ~9 pp @ G=150 (bảo thủ; 8 pp @ G=200)]** — dưới 15-20 pp → giữ nguyên thiết kế, không đổi split.
- SD-hiệu nền = 0.362 (dùng lại nếu tính lại MDE khi biết G chính xác).

## Việc kế
- Điền số này vào report/85 §6 (đã làm) → **report/85 giờ đủ để commit** (chỉ còn chốt số-app-chính-xác lúc build).
- Bước tốn tiền tiếp theo (build data → train) — hỏi user trước.

> Tóm: pilot cho hai tin tốt đo-được — trục ĐÚNG **đủ lực** (MDE 8-9 pp) và **không sàn-0** (teacher 30%); cộng một giới-hạn phải khai (thước per-bước nghiêm vì nhiều-bước-hợp-lệ). Bản đăng-ký-trước đủ điều kiện commit.
