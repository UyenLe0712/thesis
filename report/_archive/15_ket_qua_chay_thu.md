# BÁO CÁO 15 — KẾT QUẢ CHẠY THỬ ĐẦU TIÊN (ghi nhận cột mốc)

> **Ngày:** 2026-06-25. **Mục đích:** ghi nhận lần chạy thử THẬT đầu tiên của pipeline design E + bộ chấm DG1, và **phân tích thẳng "kết quả tốt chưa"**.
> **Tính chất:** smoke-test tập NHỎ — chứng minh *cả vòng chạy được*, **chưa phải** đánh giá chính thức. Số liệu là **tín hiệu sơ bộ**, không phải kết luận chất lượng.

---

## 1. Cấu hình đã chạy (tái lập được)
- **Máy:** không GPU NVIDIA (chỉ Intel iGPU) → chạy **CPU**, miễn phí.
- **Bộ sinh:** **Ollama + `qwen2.5vl:3b`** (model mở, ~3.2GB), endpoint OpenAI-compat `localhost:11434/v1`.
- **Dữ liệu:** 3 màn MobileViews thật trong `dataset_samples/mobileviews/`.
- **Câu hỏi use-case:** tự soạn (MobileViews không kèm câu hỏi).
- **Harness:** `harness/run_dg1_trial.py` (sinh) + `harness/dg1_scorer.py` (chấm). Chạy lại: đặt 3 biến `VLM_*` rồi `python harness/run_dg1_trial.py`.

## 2. Tutorial model sinh ra (nguyên văn) + chấm

**Màn item1_state39** — hỏi *"đặt giờ rồi xác nhận thì làm thế nào?"*
- `1. Bấm OK` → khớp nút thật "OK".
- → faithfulness 100% · coverage 20% (1/5) · grounded 100%. *(Model viết quá ngắn — chỉ 1 bước.)*

**Màn item2_state203** — hỏi *"điền thông tin rồi gửi biểu mẫu thì bấm vào đâu?"*
- `1. Bấm vào ô Find or create a contact (required)` → **BỊA** (màn này không có ô đó).
- `2. Chọn Email address` → khớp.
- `3. Nhập First name` → khớp.
- `4. Nhập Last name` → khớp.
- → faithfulness 75% · coverage 50% (3/6) · grounded 75%. *(1 bước bịa thật.)*

**Màn item3_state129** — hỏi *"tạo công việc mới và nhập thông tin thì làm sao?"*
- `1. Bấm Find or create a task` · `2. Nhập thông tin (Find or create a task)` · `3. Bấm Estimated hours` · `4. Chọn Hourly rate` · `5. Nhập Estimated Amount` → tất cả khớp nút thật.
- → faithfulness 100% · coverage 57% (4/7) · grounded 100%.

**Trung bình 3 màn:** faithfulness **91.7%** · coverage **42.4%** · grounded **91.7%**.

---

## 3. PHÂN TÍCH — "kết quả tốt chưa?"

### ✅ Cái ĐÃ tốt (cột mốc thật)
1. **Toàn bộ pipeline design E chạy thật, end-to-end, miễn phí, không GPU.** Đây là điều quan trọng nhất — từ "không có GPU, tưởng bế tắc" → một vòng chạy thật trong vài phút.
2. **Bộ chấm BẮT ĐÚNG lỗi thật:** phát hiện bịa ở item2 (*"Find or create a contact"* không có trên màn) và lộ việc viết-quá-ngắn ở item1. Metric **phân biệt được** chỗ làm tốt/dở.
3. **Bẫy dữ liệu đã xử đúng** (kích thước ảnh thật, bounds lồng) — số toạ độ/khớp không sai âm thầm.

### ⚠️ Vì sao CHƯA thể kết luận "tốt" (phải nói thẳng)
1. **Mẫu quá nhỏ:** 3 màn / 10 bước. Một lỗi bịa = tụt 25% một màn. **Không có ý nghĩa thống kê** — cần ≥ vài chục đến vài trăm màn.
2. **Matcher còn LỎNG (chuỗi/token):** dễ **bỏ sót bịa** (báo "khớp" nhầm) hoặc phạt oan đồng nghĩa → **faithfulness 91.7% chưa đáng tin**, phải nâng lên **ALOHa (embedding) + audit người** mới chốt được con số.
3. **Coverage 42% đang dùng MẪU SỐ SAI:** hiện chia cho *mọi nút actionable trên màn*. Nhưng một tutorial cho **một câu hỏi cụ thể** KHÔNG cần nhắc mọi nút (vd hỏi "đặt giờ" thì không cần nhắc "Cancel"). → 42% **gây hiểu nhầm là kém**. Coverage đúng phải đo theo **nút LIÊN QUAN tới tác vụ** — mà MobileViews **không có gold** để biết "nút nào cần". → **coverage + Step-SR chỉ thật sự đo được trên AndroidControl** (có gold action mỗi bước). Đây là phát hiện phương-pháp quan trọng từ lần chạy này.
4. **faithfulness ≈ grounded** trong thiết kế sinh-theo-tên (cả hai = "bước có khớp nút thật") → **đang đo trùng**; cần tách: grounded = đúng vị trí hình học (cần toạ độ), faithfulness = tồn-tại.
5. **Chưa có BASELINE để so:** "tốt" chỉ có nghĩa khi so với *model viết tự do (không oracle)* và *model khác*. Chưa có baseline thì 91.7% là số treo lơ lửng.

### 📌 Kết luận phân tích
> **PIPELINE: tốt — đã được kiểm chứng chạy được + metric bắt lỗi đúng.**
> **SỐ LIỆU: mới là tín hiệu sơ bộ, CHƯA đủ để nói "model tốt/chưa tốt".** Quan sát thật rút ra: model 3B **có bịa** (item2) và **hay viết quá ngắn** (item1) — đúng kiểu model nhỏ. Muốn biết "tốt chưa" theo nghĩa luận văn, cần đủ 5 thứ ở mục dưới.

---

## 4. Cần gì để biến tín hiệu này thành KẾT LUẬN "tốt"
1. **Nhiều màn hơn** (≥ vài chục–trăm; tải thêm shard MobileViews) → có ý nghĩa thống kê + CI.
2. **Nâng matcher → ALOHa** (embedding + Hungarian) + **audit người** một subset để biết faithfulness thật.
3. **Sửa coverage:** đo trên **AndroidControl** (có gold) theo **nút liên quan, có trọng số** + thêm **Followability/Step-SR**.
4. **Thêm baseline:** model **viết tự do (không oracle/fallback)** + **model thứ hai** (vd model lớn hơn / frontier API) → bảng so sánh "lớp trung-thực-hoá có cải thiện không".
5. **Tách faithfulness vs grounding hình học** (yêu cầu model xuất toạ độ, hoặc dùng grounder).

→ Khi đủ 5 thứ trên + pre-register, kết quả (kể cả null) mới "đậu" theo khung đã chốt.

---

## 6. CHẠY THỬ #2 — 10 màn + matcher strict/loose + baseline vs design-E

**Cấu hình:** 10 màn trích từ `mv.zip` (cùng 1 app), **câu hỏi CHUNG** (không tự soạn riêng từng màn), matcher tách **strict/loose**, so **baseline (raw) vs design-E (fallback)**. Harness: `harness/run_dg1_trial2.py`.

**Kết quả (27 bước / 10 màn):**
- faithfulness **STRICT = 59.3%** (loose cũng 59.3% — matcher loose không bắt thêm cái nào).
- BASELINE (raw): **confident-wrong = 40.7%** (11/27 bước gọi nút KHÔNG có trên màn).
- DESIGN-E (fallback): **confident-wrong = 0%** (đổi 11 bước đó thành mô tả bằng lời).
- Cá biệt: s27 và s213 model bịa 100% số bước.

**Phân tích (quan trọng):**
1. **Tương phản với chạy thử #1 (91.7%) → bài học lớn:** #1 dùng câu hỏi tôi **tự soạn KHỚP màn** (vô tình "dẫn dắt" model tới nút đúng); #2 dùng câu hỏi **CHUNG mơ hồ** → model bịa nhiều hơn hẳn (**40.7%**). → **Chất lượng câu hỏi CHI PHỐI MẠNH kết quả.** Điều này *validate* quyết định "tự soạn câu hỏi phải là một PROTOCOL cẩn thận" — và cảnh báo: số liệu vô nghĩa nếu câu hỏi tuỳ tiện.
2. **Giá trị DESIGN E hiện rõ hơn:** chính vì model bịa nhiều, **fallback càng có giá trị** — biến **40.7% "lệnh bấm nút sai mà tự tin"** (tệ nhất cho người dùng) thành **mô tả trung thực**. Đây là minh chứng cụ thể, đo được, cho cơ chế cốt lõi của hệ.
3. **Matcher còn yếu:** loose bắt 0 → hoặc các bước unmatched là bịa thật, hoặc matcher chuỗi chưa bắt được đồng nghĩa. → "bịa thật" có thể THẤP hơn 40.7%; phải nâng **ALOHa + audit người** mới chốt.
4. **Generator 3B + câu hỏi mơ hồ = yếu:** với vai "viết tutorial tốt", model nhỏ này chưa đạt.

**Kết luận cập nhật:** **HỆ (design E + bộ đánh giá) hoạt động và chứng minh được giá trị fallback (40.7%→0%).** Nhưng **GENERATOR (3B, câu hỏi chung) còn yếu** — và kết quả cực nhạy với **chất lượng câu hỏi**. Để tiến tới "tốt": (a) **đầu tư câu hỏi use-case tốt**, (b) model mạnh hơn, (c) ALOHa + audit, (d) nhiều app/màn, (e) báo cáo strict/loose band.

## 7. SO SÁNH 3B vs 7B (CÙNG 10 màn, CÙNG câu hỏi chung)

| Chỉ số | Qwen2.5-VL **3B** | Qwen2.5-VL **7B** |
|---|---|---|
| Tổng bước | 27 | 24 |
| **faithfulness (strict)** | 59.3% | **75.0%** ↑ |
| **confident-wrong (baseline raw)** | 40.7% | **25.0%** ↓ |
| design-E (fallback) confident-wrong | 0% | 0% |
| fallback "cứu" được | 40.7% | 25.0% |
| s27 (ca tệ nhất của 3B) | 5/5 bịa (100%) | 1/2 bịa (50%) |

**Phân tích (3 điều quan trọng, đều có ích cho luận văn):**
1. **Metric NHẠY — phân biệt được 2 model:** bịa 40.7% (3B) → 25.0% (7B). Một thước đo phân biệt được model tốt/dở là dấu hiệu **thước đo đáng tin** (về mặt phân biệt). Đây là bằng chứng metric "có răng".
2. **Design E là model-agnostic:** fallback xoá sạch confident-wrong (→0%) cho **cả hai** model. Đúng tinh thần "model thay được": cắm model mạnh hơn vào → tutorial trung thực hơn, hệ vẫn chạy nguyên.
3. **Giá trị "cứu" của fallback GIẢM khi model mạnh lên (40.7%→25.0%) nhưng vẫn DƯƠNG** — khớp đúng dự đoán literature (lớp bọc giúp ít dần khi model mạnh, nhưng không về 0 vì *frontier vẫn bịa* — EACL 2026). Suy ra: với GPT-5/Gemini-3, fallback sẽ cứu ít hơn nhưng **vẫn > 0** → hệ vẫn có giá trị, chỉ cần đóng khung trung thực.

**Còn lại:** kể cả 7B vẫn **bịa 25%** (với câu hỏi chung + matcher chuỗi) → faithfulness/grounding **vẫn là vấn đề thật** → đề tài có đất. Cần câu-hỏi-tốt + ALOHa + audit để biết con số "bịa thật".

## 8. NÂNG MATCHER (ALOHa) + TÁCH 2 SỐ (Bịa vs Đúng-nhãn) — chạy thật, miễn phí

**Làm gì:** thay matcher chuỗi-thô bằng **ALOHa (embedding `nomic-embed-text` qua Ollama, CPU)** cho cột **Bịa**, và thêm cột **Clarity/đúng-nhãn** (so chính xác tên hiển thị). Harness: `harness/aloha_match.py` + `score_v2.py` (chấm lại trên tutorial đã lưu ở `gen_cache/`, miễn phí, tức thì).

**Tự kiểm matcher:** tiếng **Anh OK** (synonym "Configure"→"Settings" 0.61, "email field"→"Email address" 0.69; khác-nghĩa "Log out"→"Settings" 0.39 → ngưỡng ~0.55 tách được). Tiếng **Việt YẾU** với embedder này ("Đăng xuất"≈"Cài đặt" 0.82 sai) → **VN định lượng cần embedder đa ngữ (bge-m3)** → đúng kế hoạch để VN là demo/future-work.

**Kết quả (cùng 10 màn, 27 bước):**
| Cột | Số |
|---|---|
| Bịa — matcher **chuỗi** | 40.7% (thổi phồng) |
| Bịa — matcher **ALOHa** | **33.3%** (đáng tin hơn) |
| synonym **bị chuỗi vu oan** (ALOHa cứu) | 2 bước (7.4%) |
| **Đúng-nhãn (clarity)** | 59.3% |
| nút **có thật nhưng gọi sai nhãn** → trừ CLARITY, không tính bịa | 2 bước (7.4%) |

**Ý nghĩa (3 điều):**
1. **Matcher chuỗi THỔI PHỒNG bịa** (40.7% → 33.3%): 2 bước là synonym của nút thật bị vu oan là "bịa". → **ALOHa cho con số bịa đáng tin hơn** — đúng mối lo "số chưa đáng tin".
2. **Tách 2 số chạy được đúng ý user (câu hỏi #3):** "gọi sai nhãn" (nút có thật, gọi tên khác) → **trừ CLARITY 7.4%**, KHÔNG tính BỊA. Bịa (33.3%) và Đúng-nhãn (59.3%) là hai số riêng.
3. **De-risk harness trước Colab:** toàn bộ logic chấm DG1 (ALOHa + 2 số) đã chạy thật trên dữ liệu thật, miễn phí → khi lên Colab chỉ việc scale, không phải dò lại logic.

**Caveat:** ngưỡng τ=0.55 là lựa chọn → **pre-register + audit người** mới chốt; vẫn 3B + câu-hỏi-chung + 10 màn 1 app (sơ bộ). Model 3B vẫn bịa 33% (s27 bịa 5/5) → cần model mạnh + câu hỏi tốt.

## 9. THÍ NGHIỆM A/B — CHỨNG MINH "PIPELINE HIỆU QUẢ" (free, CPU)

**So:** BASE (model viết tự do) vs SYS (design E: bước nào bịa → bắt **model KHÁC (llama3.2)** sửa từ danh sách nút thật → không được thì fallback). Harness: `harness/effectiveness_ab.py`.

**Kết quả (10 màn, 27 bước):**
| | BASE (viết tự do) | SYS (design E) |
|---|---|---|
| **Bịa** (lệnh bấm nút không tồn tại) | 33.3% | **0%** |
| **Faithfulness** | 66.7% | **100%** |
| **Đúng-nhãn (Clarity)** | 59.3% | **92.6%** |
| 9 bước bịa của BASE → SYS xử lý | — | **9/9 SỬA thành nút THẬT** *(chưa chắc ĐÚNG-việc)*, 0 fallback |

*(9 = số bịa đếm theo **ALOHa**; matcher chuỗi đếm 11, ALOHa đã loại 2 synonym oan → khớp mục 8.)*

**Ý nghĩa:**
- **Đây là bằng chứng "pipeline hiệu quả" cụ thể nhất:** SYS **không chỉ giấu lỗi** (fallback) mà **SỬA** bịa thành nút thật → faithfulness **66.7%→100%**, clarity **59.3%→92.6%**, trên dữ liệu thật, **miễn phí**.
- Bước "sửa" dùng **model KHÁC** (llama3.2) → đúng tinh thần "verifier model khác = phản hồi từ ngoài" (thoát phê phán self-refine).

**⚠️ CAVEAT TRUNG THỰC (quan trọng — phải nói khi trình):**
- "**Recover về NÚT THẬT**" chứng minh **trung thực + đúng-nhãn**, **NHƯNG chưa chứng minh nút đó ĐÚNG cho MỤC TIÊU** (MobileViews không có đáp án vàng để biết "nút nào đúng"). Có rủi ro sửa thành **nút-thật-nhưng-sai-việc**.
- → "Đúng-mục-tiêu" phải đo bằng **Step-SR trên AndroidControl (có gold)** = phần **Colab**.
- Ở đây llama3.2 chọn nút thật cho **cả 9** bước (không dùng fallback lần nào) → cần **canh ngưỡng fallback + audit người** để chắc nó không **ép-chọn** khi thực ra không có nút hợp.

**Tóm:** ✅ chứng minh được **hiệu quả về độ trung thực/rõ ràng** (faithfulness 100%, clarity 92.6%) — free; ⏳ **hiệu quả về tới-đích** (Step-SR) chờ Colab.

## 10. MỘT DÒNG TÓM TẮT
**Pipeline design E CHẠY THẬT miễn phí trên CPU qua nhiều thí nghiệm: cách chấm NHẠY (3B bịa 40.7% vs 7B 25% — matcher chuỗi), matcher ALOHa đáng-tin-hơn (40.7%→33.3%), và A/B chứng minh hệ HIỆU QUẢ về độ-trung-thực (faithfulness 66.7%→100%, đúng-nhãn 59.3%→92.6%). Là TÍN HIỆU SƠ BỘ MẠNH (10 màn / 1 app / model nhỏ; matcher + mẫu cần audit) — xác nhận ĐẦY ĐỦ (ý nghĩa thống kê + "tới-đích"/Step-SR) cần AndroidControl/Colab.**

*(Lưu ý đọc số: 40.7%/59.3% là matcher CHUỖI; 33.3%/66.7% là ALOHa — khác matcher, không mâu thuẫn. §3 nói "91.7% chưa đáng tin" là caveat của chạy thử #1, đã được thay bằng headline 10-màn/ALOHa.)*
