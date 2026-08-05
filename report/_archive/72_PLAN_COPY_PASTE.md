# report/72 — PLAN cuối cùng, dạng dán-thẳng-vào-chat-mới

> Mỗi việc là một khối bấm copy dán vào **một đoạn chat MỚI** là chạy được. Khối đã ghi sẵn "đọc file nào trước" để chat mới bắt được ngữ cảnh (chat mới không nhớ hội thoại cũ, nhưng đọc report là hiểu). Mỗi khối nói rõ: **kill-test/code** (viết + chạy mã trên máy) hay **research/debate** (chạy vòng tra cứu/tranh luận) hay **hỏi thầy**.
>
> Pipeline đã chốt ở `report/71`. Thứ tự đúng: làm hết GIAI ĐOẠN 1 (free) → **hỏi thầy** → mới sang GIAI ĐOẠN 2. Ba việc phụ (song song, free) làm lúc nào cũng được.
>
> Ngày: 2026-07-18. Cập nhật: K1 đã chạy (report/73) → thêm VIỆC 0b (K2) cho rõ.

> **Ánh xạ tên (tránh lẫn K1/K2/K3 ↔ VIỆC):** K1 = VIỆC 0 (✅ xong, report/73) · K2 = VIỆC 0b (đếm phân loại bịa) · K3 = gộp trong VIỆC 2 (đo teacher mới). VIỆC 1 (đọc tay fallback) là test RIÊNG, KHÔNG phải K2.

---

## GIAI ĐOẠN 1 — làm trước, gần như miễn phí (để có số mang đi hỏi thầy)

### VIỆC 0 — K1: kiểm "bộ đối chiếu" có sai không  ·  *kill-test / code · LÀM ĐẦU TIÊN*

```
Đọc report/71 (pipeline đã chốt) + report/65 (mục K1) + report/56 (pre-reg) để nắm ngữ cảnh.

Làm K1 — kill-test bộ đối chiếu lọc-bịa, kiểm HAI CHIỀU. Đây là việc viết + chạy code
trên máy (local), KHÔNG phải web research.

Bộ đối chiếu = thuật toán so tên nút mô hình nói với danh sách nút thật trong View
Hierarchy (embedding nomic-embed; xem harness/aloha_match.py, harness/dg1_pa2_score.py,
ngưỡng τ hiện tại). Cần đo nó có đáng tin để làm "trọng tài" lọc dữ liệu không:

- Chiều BỎ LỌT (false negative): nó có cho qua các ca bịa gần-nghĩa không? (mô hình bịa
  "Preferences" khi màn chỉ có "Settings" — hai chữ gần nghĩa nên máy dễ tưởng là khớp)
- Chiều KẾT OAN (false positive): nó có đánh nhầm bước ĐÚNG thành "bịa" khi VH thiếu nhãn
  (chữ nằm trên ảnh, VH không liệt kê) không?

Cách làm: dựng tập 80–120 cặp (tên mô hình nói ↔ nhãn VH) gán tay, cố ý gồm cả ca
bịa-gần-nghĩa lẫn ca đúng-nhưng-VH-thiếu-nhãn. Đo precision/recall CẢ HAI CHIỀU, báo
Cohen's κ, rồi freeze ngưỡng τ.

Kết luận cần có: bộ đối chiếu có đủ tin không. Nếu precision/recall xấu → đề xuất cách
sửa (thêm OCR / thêm luật / ngưỡng chặt hơn) — lưu ý đây là sửa PIPELINE, không phải metric.
Xong báo số + kết luận rõ ràng.
```

### VIỆC 0b — K2: đếm phân loại kiểu bịa THẬT  ·  *kill-test / đếm tay · free (hoặc ✱ vài cent nếu phải sinh teacher)*

```
Đọc report/73 (kết quả K1) + report/71 để nắm ngữ cảnh. K1 đã cho thấy bộ đối chiếu MÙ với
bịa GẦN-NGHĨA (bỏ lọt 47,5%). K2 trả lời: bịa THẬT của teacher rơi vào loại nào — để biết
điểm mù đó có thật sự nghiêm trọng trong thực tế không. Đây là cổng QUYẾT ĐỊNH có phải nâng
trọng tài trước khi build data hay không.

Việc: lấy output teacher gpt-4o-mini THẬT (từ pilot cũ trong harness/ nếu còn; nếu không có
thì sinh ~30–50 màn — ✱ tốn vài cent, HỎI user duyệt trước). Với mỗi bước nhắc tên nút mà
bị coi là bịa (không khớp VH), phân loại tay vào 4 nhóm:
  - Y-CHỮ        : tên trùng chữ nhưng vẫn bị đánh bịa (lỗi khớp kỹ thuật)
  - GẦN-NGHĨA    : khác nút, gần nghĩa một nút thật ("Send" khi màn có "Save")
  - VÔ-QUAN      : tên không liên quan gì trên màn
  - NGOÀI-TÊN-NÚT: bịa hành động/luồng/tab, không phải tên nút (matcher không soi được)
Báo phân bố % 4 nhóm + vài ví dụ.

Ý nghĩa cổng:
  - Phần lớn là VÔ-QUAN → bộ đối chiếu embedding hiện tại TẠM DÙNG ĐƯỢC → đi tiếp.
  - Nhiều GẦN-NGHĨA hoặc NGOÀI-TÊN-NÚT → phải nâng trọng tài (so-chuỗi + OCR) hoặc thu hẹp
    claim TRƯỚC khi build data.
Đây là việc đếm tay/định-tính, KHÔNG phải web research.
```

### VIỆC 1 — Đọc tay câu fallback  ·  *kill-test / đọc tay · free*

```
Đọc report/71 (trục 2 "hữu-ích") + report/56 §9 để nắm ngữ cảnh.

Việc: lấy 30–50 câu "fallback" (câu mô tả chung chung mà pipeline viết vào chỗ mô hình
bịa — kiểu "tìm nút phù hợp với việc cần làm"). Nguồn: kết quả pilot cũ trong harness/
(các lần chạy dg1_run.py / dg1_pa2_score.py trước đây); nếu chưa có sẵn thì sinh nhanh
vài chục câu bằng đúng khuôn mẫu fallback hiện dùng.

Đọc tay từng câu và tự đánh giá: một người dùng thật đọc câu này có làm được việc không,
hay chỉ là "vô dụng lịch sự"? Đếm tỉ lệ câu thật sự dùng được.

Đây là kill-test cho giả định YẾU NHẤT của cả thiết kế: toàn bộ lý lẽ "viết lại bịa thành
mô tả an toàn" giả định câu đó dùng được — chưa ai kiểm. Báo tỉ lệ + vài ví dụ tốt/tệ +
kết luận: giả định này đứng hay đổ. Đây là việc đọc-tay/định-tính, không phải research.
```

### VIỆC 2 — Pilot MDE + đo bịa của teacher đời mới  ·  *tốn ~$1–2 API · phải hỏi trước khi gọi API*

```
Đọc report/71 (PLAN bước 2) + report/56 §6 (công thức MDE) để nắm ngữ cảnh.

Việc: chạy pilot nhỏ 5–10 app để tính MDE thật (mức chênh lệch nhỏ nhất mà thí nghiệm
12-app đủ sức nhìn thấy), rồi điền ô [MDE = ___ pp] ở report/56 §6 và commit pre-reg lần 2.
Ghép luôn: đo tỉ lệ bịa của ÍT NHẤT 1 teacher đời mới (vd gpt-4.1-mini / gemini-2.5-flash)
trên vài màn — để thủ đòn "sao không dùng teacher 2026 xịn thì đâu cần lọc".

⚠ Bước này GỌI API tốn ~$1–2 → HỎI TÔI (user) DUYỆT trước khi chạy phần tốn tiền.
⚠ Chỉ đo phương sai nền, KHÔNG được nhìn hướng/độ-lớn hiệu ứng (giữ tính pre-registration).

Xong: báo MDE, kết luận có cần đổi cách chia 18/12 → 15/15 không, và tỉ lệ bịa teacher mới.
```

---

## ⛳ CỔNG HỎI THẦY — sau VIỆC 2, TRƯỚC mọi bước mở rộng

```
Mang 3 con số đi gặp thầy: (a) bộ đối chiếu chính xác cỡ nào (VIỆC 0), (b) câu fallback có
dùng được không (VIỆC 1), (c) MDE — kính có đủ nét không (VIỆC 2). Hỏi thầy 4 câu (chi tiết
ở report/71 mục "Cái phải hỏi thầy"):
1. Có cho thêm trục "ĐÚNG" (dùng AndroidControl có đáp án mẫu) ở dạng phụ + khai exploratory không?
2. Trục hữu-ích dừng ở đọc-tay hay nâng thành mẫu-người-nhỏ có κ?
3. Có cho mở rộng app test không, rút từ pool nào?
4. Chấp nhận khả năng mô hình-lọc chấm điểm ĐÚNG thấp hơn mô hình-thô (càng trung thực càng
   làm-việc kém) → thống nhất trước cách trình bày.

KHÔNG chạy Giai đoạn 2 trước khi thầy duyệt — vì các bước đó đụng bộ thí nghiệm đã khoá.
```

---

## GIAI ĐOẠN 2 — sau khi thầy duyệt (mỗi việc một khối)

### VIỆC 3 — (nếu thầy OK) Thêm app test  ·  *tốn API*

```
Đọc report/71 (bước 3) + report/56 §1. Thầy đã duyệt mở rộng app test.
QC thêm app test tới CÙNG chuẩn lọc chất lượng như 30 app gốc, nới cách chia — làm TRƯỚC
khi nhìn bất kỳ kết quả test nào, khai rõ trong pre-reg. Báo split mới + số app test cuối.
```

### VIỆC 4 — Dựng data + train 2 bản mô hình  ·  *tốn Colab GPU + ~$1–2 API*

```
Đọc report/71 (bước 4) + report/53 (config train) + report/56 (pre-reg).
Gọi teacher gpt-4o-mini sinh nháp → chạy pipeline lọc bịa → dựng data-LỌC + data-THÔ.
GẮN LUÔN 2 vá pipeline đã chốt: (i) dùng thêm OCR ở bước lọc (xem VIỆC OCR đã đo trước đó);
(ii) câu fallback dùng 10 cách diễn đạt khác nhau thay vì 1 câu mẫu (report/68).
Rồi train Student-LỌC + Student-THÔ (Qwen2.5-VL-3B, QLoRA r=8/α=16, freeze-vision,
LLaMA-Factory). Smoke-test 20 mẫu trước. ⚠ Tốn GPU/API → báo trước khi chạy phần tốn tiền.
```

### VIỆC 5 — Chạy Trục 1 (trụ chính)  ·  *tốn GPU/API chấm*

```
Đọc report/71 (bước 5) + report/56 §3–§5.
Chạy Tier 1 (Student-LỌC vs Student-THÔ) + Tier 2 (Student vs Teacher-BASE, tắt VH),
chấm bằng 3 cơ chế khác họ, thống kê exact sign-flip G=12. Đây là trụ chính — chạy dù
các trục khác ra sao. Báo kết quả theo 3 kết cục đã viết sẵn ở report/56 §5.
```

### VIỆC 6 — (nếu thầy OK) Trục "ĐÚNG" + cổng kiểm khung toạ độ  ·  *free lúc chấm*

```
Đọc report/71 (bước 6 + Rủi ro #1, #2) để nắm cổng bắt buộc.
(i) Fetch bản GỐC AndroidControl (google-research/android_control — bản smolagents đang
dùng đã bị lược, KHÔNG có accessibility tree). (ii) Viết parser + hàm point-in-bbox tra
(x,y) đáp án → nhãn nút thật. (iii) CỔNG BẮT BUỘC: kiểm mắt 5–10 bước xác nhận toạ độ action
và bbox a11y CÙNG khung. (iv) Đo sai số của chính cầu-đo này — nếu tự sai >15–20% thì DỪNG
trục này. (v) Đếm mẫu số thật (chỉ click/long_press/input_text có tên để kiểm) — nếu quá
nhỏ thì khai giới hạn. (vi) Nếu qua hết: chạy Step-SR-theo-tên teacher-forced. Khai thẳng
đây là "biến thể Step-SR theo tên", KHÔNG claim ngang leaderboard toạ-độ.
```

---

## VIỆC PHỤ — song song, free, làm lúc nào cũng được

### VIỆC OCR — đo VH vs VH+OCR (quyết có gắn OCR vào bước lọc không)  ·  *code · free*

```
Đọc report/67 (Vòng C) để nắm ngữ cảnh.
Mở rộng harness/dg1_vh_coverage.py thêm nhánh OCR: đo độ phủ nhãn "chỉ VH" vs "VH + OCR"
trên 127 màn có sẵn (PaddleOCR mặc định, EasyOCR đối chứng). Khoá ngưỡng "chữ nằm trong
khung nút" TRƯỚC khi chạy. Kết luận: OCR bù được bao nhiêu, có đáng gắn vào bước lọc không.
Đây là code chạy local, không tốn tiền.
```

### VIỆC R — verify các citation còn lung lay  ·  *research nhỏ · free*

```
Đọc report/71 (mục "Chỗ bằng chứng YẾU"). Chạy một vòng deep-research/verify NHỎ, chia nhỏ,
để xác minh tận gốc mấy nguồn chưa chắc TRƯỚC khi đưa vào bài: CAP (ACML 2025 — venue thật
nhưng có đúng "risk = Step-SR" không?), bài AURC arXiv 2410.15361 (có phải chỉ là preprint?),
năm đúng của Geifman–El-Yaniv (2017 hay 2019?). Báo: giữ / sửa / bỏ từng cái.
```

### VIỆC D — debate phòng khi trục "ĐÚNG" tự bắn chân  ·  *debate · free*

```
Đọc report/71 (Rủi ro #3). Chạy một vòng debate đa-góc-nhìn: nếu mô hình-LỌC (học để trung
thực/né) lại chấm điểm ĐÚNG THẤP HƠN mô hình-THÔ → lộ "càng trung thực càng làm-việc kém".
Cần chuẩn bị trước cách trình bày (no-harm / đánh-đổi) và ranh giới nào thì đó là kết quả
âm thật. Báo: kịch bản + câu trả lời thủ sẵn cho thầy.
```

---

## Nhắc nhanh

- **Xương sống pipeline đã chốt** (report/71) — không đổi. Plan này chủ yếu để chốt **thước đo** + kiểm ruột pipeline (VIỆC 0) + 2 vá nhỏ (OCR, 10 câu fallback).
- **Thứ tự cứng:** VIỆC 0 → 1 → 2 → **HỎI THẦY** → 3/4/5/6. Ba việc phụ (OCR, R, D) chen vào lúc nào cũng được.
- **Mọi bước tốn tiền (✱ API/GPU): hỏi user duyệt trước.**
- Bắt đầu: **VIỆC 0 (K1)** — dán khối đầu tiên vào chat mới.
