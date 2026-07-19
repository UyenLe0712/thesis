# Tóm tắt các quyết định đã chốt gần đây (đọc để nắm context)

> Gộp gọn chuỗi kiểm chứng + debate gần đây (report/73→82) và thiết kế cuối + plan hiện tại. Đọc file này là nắm được "mình đã chốt gì và vì sao". Chi tiết từng phần ở file gốc ghi trong ngoặc. Ngày: 2026-07-19.
>
> ⚠️ File này **mới hơn report/80** ở phần thiết kế: report/80 tả trạng thái cũ (train MobileViews, chấm AndroidControl kiểu cross-dataset); bản chốt cuối đã ĐỔI — xem mục 3 dưới.

---

## 1. Đề tài (không đổi)

Cho **một ảnh màn app + một câu hỏi** ("làm sao bật thông báo?"), model trả lời bằng **các bước hướng dẫn cho người đọc**. Yêu cầu cứng của thầy: **phải có model do học viên tự train** (đã xác nhận lại 19/7 — ràng buộc này vẫn cứng, model phải là một đóng góp thật).

## 2. Chuyện gì đã xảy ra gần đây (chuỗi kiểm chứng)

Mình chạy một loạt **phép thử miễn phí trên máy** để kiểm thiết kế TRƯỚC khi tiêu tiền. Kết quả lật vài giả định quan trọng:

| Việc | Phát hiện | File |
|---|---|---|
| **K1** — kiểm "bộ đối chiếu" (thuật toán so tên nút với danh sách nút thật) | Nó yếu cả hai chiều: vừa bỏ lọt bịa-nghe-giống, vừa đánh oan nút-gọi-đúng-bằng-từ-khác; hai loại trùng điểm nhau nên **không ngưỡng nào tách được** | 73 |
| **K2** — đếm bịa thật của thầy giáo (gpt-4o-mini) | **Thầy giáo gần như KHÔNG bịa (~0-2%)**, không phải "¼" như tưởng. Những chỗ bị đánh "bịa" thật ra là **nút thật mà VH bỏ sót nhãn** (nhất là nút hình +, ✓) | 74 |
| **OCR** — thử đọc chữ trên ảnh bù chỗ VH thiếu | Giúp với nút có chữ, **thua nút hình thuần**; còn ~20% nút không cách nào lấy nhãn | 75 |
| **VIỆC1** — đọc tay câu "chung chung" | An toàn nhưng **lặp lại mục tiêu**, không chỉ chỗ bấm → giá trị thấp | 76 |

**Hệ quả lớn:** tiền đề cũ *"thầy giáo bịa nhiều, ta lọc bỏ → dạy học trò trung thực hơn"* **lung lay** — vì thầy giáo gần như không bịa, nên chẳng có gì để lọc.

## 3. Quyết định lớn (qua debate đối kháng)

Vì tiền đề lung lay, mình chạy **hai vòng debate** để chốt hướng cuối:

**Vòng 1 — chọn hướng (report/78 → phương án LAI):** thay vì lấy "lọc bịa" làm đóng góp chính (đã yếu), lấy **"độ ĐÚNG"** làm trục chính — đo bằng bộ **AndroidControl** vì nó **có đáp án mẫu do người thật làm** (chấm được chính xác, khác MobileViews không có đáp án).

**Pilot AndroidControl (report/79):** thử xem trục ĐÚNG có khả thi không. Kết quả **đèn xanh** + tìm được cách hay hơn: AndroidControl có sẵn **hướng-dẫn-người viết từng bước** → so thẳng *hướng-dẫn-của-model* với *hướng-dẫn-người* (so hai đoạn văn), thay vì mò tên nút theo toạ độ.

**Vòng 2 — chốt thiết kế cuối (report/81):** đây là bản chốt hiện tại, **khác report/80**:

- **Train trên gì:** một model, tín hiệu **chính = hướng-dẫn-người của AndroidControl**; MobileViews-chưng-cất làm **data phụ** (có bật/tắt để so).
- **Đo ở đâu:** trục ĐÚNG (chính) đo **ngay trên app chưa-thấy của chính AndroidControl** (học và chấm cùng bộ, phần app khác nhau) → **bỏ được lỗ hổng "học một nơi chấm một nơi"** của bản trước.
- **MobileViews:** KHÔNG bỏ — giữ để đo trung thực (không cần đáp án, dùng VH) + giữ sợi "chưng cất" + là nhà của chương đo-lường. Nhưng hạ vai.
- **Metric:** tách mỗi bước thành **(thao-tác, đích)** — đây là chỗ vá đúng bẫy K1 (ví dụ "tab Gmail" vs "tab Calendar" là sai ĐÍCH cứng, dù nghe gần); validate bằng **bơm-lỗi làm CỔNG** (phải chứng minh thước bắt được lỗi + tách được lỗi khỏi paraphrase, TRƯỚC khi train).
- **Không cần dataset mới.**

**Verify chống scoop (report/82):** kiểm văn liệu + fetch thẳng đối thủ gần nhất (GUITrans2Act) → **không bị scoop**, chỗ trống còn thật. Đã fetch xác nhận GUITrans2Act khác hẳn (video→agent, không phải ảnh→người).

## 4. Hai đóng góp (chốt 19/7)

Luận văn có **HAI đóng góp ngang nhau**:

1. **MODEL** — model **đầu tiên sinh hướng dẫn nhiều-bước CHO NGƯỜI ĐỌC** từ một ảnh + câu hỏi (mọi model GUI khác sinh thao-tác cho MÁY tự bấm). Tính mới nằm ở **tác vụ mới**, KHÔNG ở "3B on-device" (chỗ đó đông rồi). ← thoả yêu cầu train-model của thầy.
2. **ĐÁNH GIÁ** — cặp thước **trung thực (đối chiếu VH, không cần đáp án) + đúng (so gold)**, cộng **phát hiện thực nghiệm** (4 kill-test) về vì sao cách đo ngây thơ hỏng.

**Câu định vị nên nói với hội đồng:** *"Lần đầu lấy hướng-dẫn-người của AndroidControl làm mục tiêu SINH cho hướng dẫn nhiều-bước phục vụ NGƯỜI ĐỌC, đo bằng cặp thước chưa ai ghép trên GUI: trung thực đối chiếu View Hierarchy song song với đúng-đắn so gold."*

**Đừng claim (sẽ bị đập):** "đánh giá kép là phát kiến" (đã có hybrid-metric); "model 3B on-device" là điểm mới (đông); "sinh hướng dẫn GUI cho người là mới hoàn toàn" (phải phân định CHI 2023 + GUITrans2Act).

## 5. Sơ đồ thiết kế cuối (gọn)

```
TRAIN (một model):
  AndroidControl: ảnh + gold-hướng-dẫn-người  ── tín hiệu CHÍNH ──┐
  MobileViews: ảnh + câu hỏi → thầy giáo sinh → lọc (vai phụ) ── data phụ ──┤
                                                                            ▼
                              Qwen2.5-VL-3B (QLoRA, freeze phần nhìn, Colab)

ĐO:
  TRỤ CHÍNH (độ ĐÚNG)        │  TRỤ PHỤ (trung thực)
  AndroidControl app-chưa-thấy│  MobileViews (tắt VH lúc sinh)
  so (thao-tác, đích) với gold│  học trò có bịa nút không
  Student vs Thầy-giáo-gốc     │  (báo dù kết quả nhạt)
  (thước đã qua cổng bơm-lỗi)  │
        + ScreenSpot (đối chứng) + Chương đo-lường (4 kill-test)
```

## 6. Cần research/debate gì nữa không?

**KHÔNG.** Thiết kế + tính-mới đã chốt và tự-đối-kháng đủ (7 vòng debate + 4 kill-test + pilot + verify-scoop). Việc còn lại là **THỰC THI** — và bản thân bước build-metric là phép kiểm chứng quan trọng nhất (cổng bơm-lỗi sẽ đo bằng số xem thước có tránh được bẫy K1 không).

## 7. Plan hiện tại — 4 việc FREE làm ngay (đang thực thi)

| # | Việc | Là gì |
|---|---|---|
| 1 | **Viết bản đăng-ký-trước mới** (thay report/56) | Khoá quy tắc thắng-thua theo trục chính mới (độ ĐÚNG) TRƯỚC khi train |
| 2 | **Tải AndroidControl-test về máy** | Lấy gold-hướng-dẫn-người + ảnh để dựng/kiểm thước |
| 3 | **Build + bơm-lỗi-validate thước (thao-tác, đích)** ⟵ **CỔNG** | Chứng minh thước bắt được lỗi + tách lỗi khỏi paraphrase (chỗ K1 chết). Rớt cổng → dừng, sửa thước, KHÔNG train |
| 4 | **Nghiên cứu nhỏ kiểm thước có đo đúng thứ cần** | So điểm-thước với người-chấm ~30-50 mẫu |

Sau khi 4 việc free này xong (nhất là qua CỔNG ở bước 3) → mới tới bước tốn tiền: dựng data → train → đo.

## 8. Rủi ro còn lại (khai thẳng)

1. **Thước có thể không qua cổng bơm-lỗi** — nếu tách (thao-tác, đích) vẫn dính bẫy K1 thì phải sửa thước. Đây là lý do bước 3 làm TRƯỚC khi train.
2. **Trích (thao-tác, đích) từ văn tự do có thể hỏng** — cần validate bộ trích riêng.
3. **~48% click trong AndroidControl là icon/ảnh** → đích khó đặt tên; phải báo tách nhóm chữ vs icon.
4. **Chưa chạy model sinh thật** → chưa có con số điểm-đúng; mới xác nhận khả-thi-dữ-liệu.
5. **Tính mới mỏng ở phần model-kiến-trúc** → phải bán bằng tác-vụ-mới + đánh-giá, không bằng size.

## Bản đồ file (recent)
- Kill-test: `73` K1 · `74` K2 · `75` OCR · `76` VIỆC1 · `77` hồ sơ gặp thầy.
- Debate/quyết định: `78` chọn LAI · `79` pilot · **`81` thiết kế cuối** · **`82` verify chống scoop**.
- Tổng hợp: `80` (đầy đủ nhưng phần thiết kế cũ hơn `81`) · **`83` file này** (chốt gần đây).
- Nhật ký quyết định: `CLAUDE.md` §0 (dòng đầu = mới nhất).
