# report/63 — Nếu không áp lực thời gian: giữ gì, đổi gì + plan deep-research chia nhỏ

> Trả lời câu hỏi của user (2026-07-16): *"Nếu không bị áp lực thời gian, bạn có còn xây pipeline và metric hiện tại không?"* + plan deep-research chi tiết, chia thành các vòng nhỏ độc lập. **Đây là PLAN, chưa chạy vòng nào** — mỗi vòng chỉ chạy khi user gật.
>
> Căn cứ: kết quả deep-research đã verify ở `report/61` (bản dễ hiểu: `report/62`), thiết kế hiện tại ở `report/54` + pre-registration `report/56`.

---

## PHẦN 1 — Trả lời thẳng: giữ gì, đổi gì

### Giữ nguyên (xương sống — kể cả có vô hạn thời gian cũng làm vậy)

| Thành phần | Vì sao giữ |
|---|---|
| **Filter-then-train với VH làm trọng tài ngoài** (teacher sinh mù → matcher đối chiếu VH → lọc → SFT) | report/61 xác nhận chưa ai làm đúng công thức này trong miền GUI — khoảng trống thật, không bị scoop. Đây là phần đáng giá nhất của thiết kế. |
| **Held-out theo app + Tier 1/Tier 2 hai tầng** | Tách "lưới an toàn gần chắc dương" khỏi "trụ chính có thể null" là thiết kế phòng thủ đúng, không phụ thuộc deadline. |
| **Anti-circularity** (nomic lọc ≠ bge-m3 chấm, judge khác họ) | Không có lý do nào để bỏ, thời gian nhiều hay ít. |
| **Pre-registration ngưỡng trước khi chạy** | Càng nhiều thời gian càng nên giữ — đây là chuẩn mực, không phải giải pháp tình thế. |

### Đổi nếu không áp lực thời gian (3 chỗ, xếp theo mức đáng đổi)

**1. Thước đo headline: cặp số rời → một đường risk-coverage.**
Hiện tại báo 2 số tách rời: tỉ-lệ-bịa và %fallback. Điểm yếu: hai số này đánh đổi lẫn nhau — một hệ có thể "ăn gian" giảm bịa bằng cách fallback thật nhiều, và ngược lại. Pre-reg hiện chặn bằng ngưỡng đôi (cả hai phải đạt), nhưng cách sạch hơn là vẽ **một đường cong duy nhất** (trục X = tỉ lệ dám trả lời cụ thể, trục Y = tỉ lệ bịa trong số đó) rồi so diện tích dưới đường (AURC). Hai model so nhau trên cả đường thay vì tại một điểm vận hành tuỳ ý. report/61 xác nhận khung này có trụ bình duyệt (CAP, ACML 2025) và **chưa ai áp vào miền sinh-hướng-dẫn-GUI** → vừa chặt chẽ hơn vừa là điểm mới. Đây là chỗ đáng đổi nhất.

**2. Fallback template cố định → tập câu đa dạng (hoặc abstention token).**
Nguy cơ model học vẹt một câu mẫu lặp lại là có cơ sở (GEM, ICLR 2025) nhưng chưa ai đo đúng kịch bản này (report/61 Q2). Không áp lực thời gian thì tôi né trước cho rẻ: thay 1 câu template bằng một tập ~5-10 câu cùng nghĩa khác chữ (bốc ngẫu nhiên khi viết lại), và đo đa dạng đầu ra trước/sau train làm bằng chứng. Chi phí thấp, chặn được một đòn phản biện đã thấy trước.

**3. Trọng tài: VH đơn lẻ → VH + OCR (± icon detector).**
VH thiếu nhãn nhiều (55.6% phần tử dạng ảnh — Fok CHI 2022) → matcher sẽ đánh nhầm một số bước ĐÚNG thành "bịa" (false positive), đẩy %fallback lên oan. Fusion VH+OCR để bù chỗ VH mù chữ-trên-ảnh **chưa ai làm** cho mục đích này (report/61 Q5) — vừa giảm oan sai vừa là điểm mới thứ hai. Tốn công vừa phải (OCR local, free).

**Thêm nếu thật sự dư dả:** (4) nhánh DPO trên cặp (bịa, đã-lọc) miễn phí — tính mới cao nhất tuyệt đối nhưng không có tiền lệ để dựa, rủi ro cao; (5) thí nghiệm so trực tiếp filter-then-train vs constrained-decoding — lấp khoảng trống Q4, rủi ro thấp nhưng ít "wow".

### Vì sao MÙA NÀY vẫn theo thiết kế cũ

Deadline FAIR 15/8 + pre-reg `report/56` đã commit. Đổi thước đo bây giờ = viết lại pre-reg + tính lại MDE + lùi lịch ~1 tuần. Cách dung hoà rẻ nhất (nếu muốn): **giữ cặp số rời làm headline đúng pre-reg, báo THÊM đường risk-coverage như phân tích phụ** — không phá cam kết, vẫn nhặt được điểm mới. Nhưng đó là quyết định của user + nên hỏi thầy, không tự quyết ở đây.

---

## PHẦN 2 — Plan deep-research chia nhỏ (5 vòng, mỗi vòng độc lập, có cổng dừng)

Nguyên tắc (theo yêu cầu user): **mỗi vòng chỉ 2-3 câu hỏi hẹp**, chạy xong đọc kết quả → quyết định rồi mới mở vòng sau. Không vòng nào tốn API OpenAI/GPU — chỉ tốn agent tokens. Vòng A/B/C phục vụ mùa này; D/E để dành sau 15/8.

### Vòng A — Thước đo risk-coverage (ưu tiên 1 — phải xong TRƯỚC pilot MDE nếu có ý định đổi)

*Bối cảnh: nếu quyết đổi/bổ sung thước đo thì phải sửa pre-reg TRƯỚC khi gọi API/GPU (luật đã khoá ở report/54). Nếu quyết không đổi, kết quả vòng này vẫn dùng được cho phần thảo luận/future work.*

- **A1.** Định nghĩa chuẩn AURC/coverage@risk và cách ước lượng khi "risk" không có gold mà đo bằng matcher tự động — có tiền lệ nào dùng proxy-risk (metric tự động thay người chấm) khi vẽ risk-coverage không? Nếu không có, mình phải tự biện minh chỗ nào?
- **A2.** Đường risk-coverage cần bao nhiêu điểm/mẫu để ổn định với 12 app test? Có cần calibration set tách riêng theo app không, hay dùng luôn train-apps?
- **A3.** Có bài nào báo CẢ đường cong LẪN cặp số rời song song không — để bắt chước cách trình bày "giữ pre-reg + thêm phân tích phụ"?

*Bước 0 free trước khi search:* đọc kỹ toàn văn CAP (PMLR v304) + SafeGround (2602.02419) đã có URL — nhiều phần A1/A2 có thể trả lời luôn từ 2 bài này, chỉ search phần còn thiếu. **Cỡ vòng:** 3 góc tìm, ~30-40 agent. **Cổng dừng:** nếu A1 ra "không ai từng dùng proxy-risk" → phương án đường cong yếu đi đáng kể, cân nhắc bỏ, không cần chạy A2/A3 sâu.

### Vòng B — Chống học vẹt template (ưu tiên 2 — quyết cách viết fallback trước khi build data)

- **B1.** Metric đo đa dạng đầu ra chuẩn ngành là gì (distinct-n, self-BLEU, entropy…) và ngưỡng nào bị coi là "collapse"? Có bài nào đo đa dạng TRƯỚC/SAU SFT trên data có target lặp cao?
- **B2.** Tiền lệ "paraphrase set" cho câu từ chối/hedge: bao nhiêu biến thể là đủ để tránh học vẹt (5? 10? 50?)? Có ablation nào về số biến thể không?
- **B3.** Abstention/refusal token cho VLM nhỏ (≤7B): đã ai gắn token từ-chối riêng khi fine-tune Qwen-VL/LLaVA cỡ nhỏ chưa, có công thức không?

**Cỡ vòng:** 3 góc, ~30 agent. **Cổng dừng:** nếu B2 tìm được con-số-biến-thể có trụ → áp thẳng vào script build data, không cần B3 (token là phương án phức tạp hơn, chỉ mở khi paraphrase-set không có tiền lệ).

### Vòng C — Fusion VH+OCR giảm oan sai (ưu tiên 3 — nâng chất matcher, có thể làm song song mùa này)

- **C1.** OCR nào tốt nhất cho screenshot Android chạy local free (PaddleOCR / EasyOCR / Tesseract) — có benchmark trên text UI (không phải scan giấy) không?
- **C2.** Quy tắc hợp nhất: khi OCR đọc được chữ mà VH không có nhãn, đưa vào nguồn đối chiếu thế nào để KHÔNG phá anti-circularity (OCR tham gia lúc LỌC, lúc CHẤM, hay cả hai — và phải khai báo sao trong pre-reg)?
- **C3.** Có số recall công bố của VH-only vs VH+OCR trên dataset công khai (Rico/MobileViews) để trích không, hay mình phải tự đo trên 127 màn?

**Cỡ vòng:** 3 góc, ~30 agent. **Cổng dừng:** nếu C3 xác nhận phải tự đo → việc tự đo là free (VH + OCR local trên 127 màn có sẵn), chuyển thành task code chứ không research thêm.

### Vòng D — Nhánh DPO (để dành — chỉ mở nếu quyết làm cho bài mở rộng / sau 15/8)

- **D1.** DPO + LoRA trên VLM 3B, 1 GPU: config thực chiến (beta, learning rate, số cặp tối thiểu để ổn định) từ các repo/paper đã làm gần nhất?
- **D2.** Cách né bẫy "DPO học văn phong thay vì nội dung" (HA-DPO đã cảnh báo) khi positive luôn là câu template viết lại — có kỹ thuật cân bằng style giữa 2 vế chưa?
- **D3.** OViP báo cặp offline kém ~nửa hiệu quả so với online — với budget luận văn (không đủ online), offline có còn đáng làm không, hay đợi?

### Vòng E — So sánh filter vs constrained-decoding (để dành — thí nghiệm phụ / bài mở rộng)

- **E1.** Công cụ constrained-decoding nào chạy được với Qwen2.5-VL sinh tự do (outlines / guidance / logit-processor tự viết)? Chi phí suy luận tăng bao nhiêu?
- **E2.** Checklist so sánh công bằng 2 paradigm (cùng data, cùng compute) — có template thiết kế từ literature không, để phản biện không bẻ được "so lệch"?

---

## Thứ tự đề xuất + điểm quyết định

```
[User + thầy quyết: có đổi/bổ sung thước đo không?]
        │
        ├─ CÓ ý định  → chạy Vòng A trước (bắt buộc trước pilot MDE, vì phải sửa pre-reg trước khi gọi API)
        └─ KHÔNG      → bỏ A (hoặc để sau 15/8), đi thẳng pilot MDE theo kế hoạch cũ
        
Vòng B: nên chạy TRƯỚC khi build data train (quyết cách viết fallback) — không phụ thuộc A
Vòng C: chạy lúc nào cũng được trước khi freeze matcher — không phụ thuộc A/B
Vòng D/E: sau 15/8, hoặc khi bàn bài mở rộng
```

Mỗi vòng ~30-40 agent (so với 108 của vòng gộp vừa rồi) — đúng tinh thần "mỗi lần một ít, dễ soát chất lượng". Kết quả mỗi vòng ghi thành một report riêng (64, 65, …) kèm bảng claim sống/bị bác như report/61.
