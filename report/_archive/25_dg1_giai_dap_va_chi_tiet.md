# 📗 DG1 — GIẢI ĐÁP THẮC MẮC + TRÌNH BÀY LẠI CHI TIẾT (bản 25, kế thừa & mở rộng bản 24)

> **File này thay cho 24 khi cần đọc kỹ.** Gồm 2 phần:
> - **PHẦN A — TRẢ LỜI 4 CÂU HỎI** của anh sau khi đọc 24 (giải đáp thẳng, dễ hiểu).
> - **PHẦN B — TRÌNH BÀY LẠI TOÀN BỘ NỘI DUNG 24**, nhưng lồng thêm cách diễn giải cho từng chỗ anh thắc mắc.
>
> Mục tiêu: người mới đọc hiểu, giám khảo khó tính đọc cũng gật. *Viết 2026-06-30.*

---
---

# PHẦN A — TRẢ LỜI 4 CÂU HỎI

## ❓A1. "Oracle (lời sấm)" — từ này ở đâu ra? Có bằng chứng khoa học hay mình tự đặt?

**Trả lời ngắn:** "Oracle" là **thuật ngữ chuẩn trong khoa học máy tính**, KHÔNG phải mình tự bịa. Chỉ có cụm tiếng Việt *"lời sấm"* là tôi thêm vào cho dễ hình dung — phần đó là cách diễn đạt, không phải thuật ngữ kỹ thuật.

**Giải thích đầy đủ:**
- Trong **kiểm thử phần mềm (software testing)** có khái niệm **"test oracle"**: một **nguồn cho biết kết quả ĐÚNG phải là gì**, để máy tự phán "test này đậu hay rớt". Khái niệm này có từ **Howden (1978)** và được hệ thống hoá trong khảo sát kinh điển **Barr, Harman, McMinn, Shahbaz, Yoo — "The Oracle Problem in Software Testing: A Survey", IEEE TSE 2015**. → Đây là **bằng chứng khoa học**, thuật ngữ có gốc rõ ràng.
- Trong **học máy / đánh giá**, "oracle" cũng dùng theo nghĩa **"nguồn chân-lý-tham-chiếu"** (oracle labels, oracle answer) — cái mình so kết quả model vào.
- **Trong luận văn, "oracle" = View Hierarchy (VH)** của màn hình: bản kê khai do hệ điều hành Android cung cấp, liệt kê **mọi nút/ô thật + tên + toạ độ**. Ta dùng nó làm **nguồn sự thật để CHẤM** xem hướng dẫn có bịa/đúng-tên không.

> **Ghi cho hội đồng:** dùng từ "oracle" là **đúng thông lệ ngành**; ta chỉ cần trích Barr et al. 2015 khi định nghĩa. Cụm "lời sấm" sẽ **bỏ khỏi văn bản học thuật**, chỉ giữ ở bản giải-thích-dễ-hiểu này. → Đây là một **đính chính phong cách**, không phải lỗi khái niệm.

> ⚠️ **Một caveat trung thực phải kèm:** VH **không hoàn hảo** — đôi khi thiếu element (nút vẽ bằng ảnh, custom view không khai báo accessibility). Nên đúng ra phải gọi nó là **"silver oracle"** (nguồn tự-động đủ-tin, không phải "vàng" tuyệt đối). Mọi con số grounding vì vậy đóng khung **"có điều kiện theo độ-phủ của VH"**. (Xem §9-L8 ở Phần B.)

---

## ❓A2. Bộ câu hỏi do mình TỰ SINH — vậy metric chấm nó làm sao chính xác/khoa học được?

Đây là câu **rất sắc**. Mấu chốt nằm ở một hiểu lầm cần gỡ:

> **Metric KHÔNG chấm "câu hỏi". Metric chấm "hướng dẫn" bằng cách đối chiếu với ORACLE (nút thật trên màn) — một nguồn ĐỘC LẬP với câu hỏi.**

Tức là dù câu hỏi từ đâu ra, thước đo "không-bịa / đúng-nhãn / grounded" vẫn so **tên nút model viết** với **tên nút thật trong VH**, **không** so với câu hỏi. Câu hỏi chỉ đóng vai **"đề bài"** (ép model phải viết một hướng dẫn nào đó), còn **thước đo neo vào màn hình**, không neo vào câu hỏi. → Việc câu hỏi tự sinh **không làm hỏng** tính khách quan của thước đo grounding.

**Bốn lớp bảo vệ khiến điều này khoa học (xếp theo độ mạnh):**

1. **Thước đo neo vào nguồn độc lập (VH), không neo vào câu hỏi.** Đây là lớp mạnh nhất: oracle có sẵn từ dataset, mình không tạo ra nó.
2. **So sánh GHÉP-CẶP triệt tiêu thiên vị câu hỏi.** BASE và design-E nhận **CÙNG một câu hỏi**. Nếu câu hỏi có "dễ" hay "thiên vị" thì **dễ/thiên vị NHƯ NHAU cho cả hai** → khi lấy hiệu `(sysE − BASE)`, phần thiên vị **tự khử**. Cái còn lại đúng là **tác dụng của lớp design-E**.
3. **Validate metric bằng PERTURBATION (TỰ ĐỘNG — thay cho chấm-người).** Bơm lỗi đã-biết vào hướng dẫn đúng (đổi 1 nút thật → nút-ma; đổi → đồng-nghĩa; phá format) rồi kiểm metric có "bắt" đúng không. Khách quan, tái lập, **không cần người chấm**. (Chi tiết §C3 — đây là lớp thay vị trí Track B vì thầy không ưa chấm-người.)
4. **Protocol + pre-register (+ tùy chọn người duyệt nhẹ).** Câu hỏi sinh theo luật ("1 câu/màn, phải làm-được-ngay-trên-màn") + **cổng answerability TỰ ĐỘNG** (§C2), công bố số lượng. Ngưỡng/giả thuyết chốt trước.

**Nhưng phải khai một rủi ro thật (không giấu):** nếu câu hỏi sinh ra **quá tầm thường** (kiểu "làm sao bấm nút Settings" khi nút Settings to đùng giữa màn) thì điểm sẽ **bị thổi cao một cách rẻ tiền**. Cách chặn:
- Người duyệt loại câu trivial / câu lộ sẵn đáp án.
- (Đề xuất tăng độ tin) **đo độ khó câu hỏi**: ví dụ thống kê số bước trung bình, hoặc đánh dấu câu cần ≥2 thao tác → báo cáo phân bố để chứng minh không toàn câu dễ.
- Track B cũng gián tiếp bắt lỗi này: nếu câu quá dễ, người chấm sẽ thấy BASE và sysE **đều tốt** → khoảng cách thu hẹp → mình không "ăn gian" được.

> **Một dòng chốt A2:** câu hỏi tự sinh **không** phá tính khoa học, vì (i) thước đo neo vào VH độc lập, (ii) thiết kế ghép-cặp khử thiên vị, (iii) metric được validate **tự động bằng perturbation** (§C3, không cần chấm-người), (iv) có protocol + cổng answerability tự động. Rủi ro duy nhất là câu *quá dễ / không-trả-lời-được* → chặn bằng **gieo câu hỏi từ nút-thật + cổng answerability tự động** (§C2).
>
> 👉 **Xem PHẦN C** (cuối file) để hiểu sâu cả hai điểm anh hỏi: *"câu hỏi dở thì sao"* và *"làm sao bỏ chấm-người mà vẫn validate được"*.

---

## ❓A3. Bước 2 (sinh tutorial BASE) — đây là baseline, tức CHƯA áp dụng cái của mình, để có cái so sánh, đúng không?

**Đúng chính xác.** BASE = **nhóm đối chứng (control)**:
- Là hướng dẫn model viết **tự do**, **CHƯA** đi qua lớp design-E.
- Tồn tại **chỉ để so sánh**: ta cần một mốc "nếu không có hệ của mình thì model viết tệ tới đâu".
- Cặp **BASE vs design-E trên cùng màn, cùng câu hỏi** chính là **thí nghiệm A/B** → chênh lệch giữa hai cái = **đóng góp đo-được của lớp design-E**.

Một điểm tinh tế đáng khen (và cũng để chống vặn): **BASE đã được nhắc "đừng bịa, gọi đúng tên trên màn" ngay trong prompt** (xem prompt thật ở Phần B, §3-B2). Nghĩa là mình **không** cố tình làm baseline ngu đi để dễ thắng — baseline đã được đối xử tử tế. design-E thắng nhờ **cơ chế kiểm-tra-và-sửa**, không nhờ "dìm" đối thủ.

---

## ❓A4. Matcher dùng model LOCAL có chính xác không? Người ta thường dùng gì? Đây là lõi — trình bày kỹ + đề xuất cách làm tốt nhất.

Đây là câu **quan trọng nhất**, vì:

> **Matcher là MÓNG của toàn bộ đánh giá.** Nó quyết định "nút này có thật không" → quyết định cả điểm *không-bịa*, *grounded*, *đúng-nhãn*, **và** cả hành vi *sửa/fallback* trong design-E. **Matcher sai ⇒ MỌI con số sai.** Vì vậy matcher không được "tin là đúng", mà phải **ĐO độ đúng**.

### A4.1. Hiện mình đang dùng gì (mô tả đúng code thật)
- Embedding model **`nomic-embed-text`** chạy **local qua Ollama** (miễn phí, không GPU vẫn chạy được vì là model text nhẹ).
- So bằng **cosine similarity**; **khớp nếu ≥ τ = 0.55** (chốt trước).
- Cột **đúng-nhãn** thì so **chuỗi chính xác** (chuẩn-hoá hoa/thường/khoảng trắng + kiểm trùng/substring), tách khỏi cột ngữ-nghĩa.

### A4.2. Có chính xác không? — Câu trả lời TRUNG THỰC
- `nomic-embed-text` là model embedding mở **khá tốt** cho tiếng Anh, **đủ cho bản chạy-thử miễn phí**. Self-test cho thấy nó **tách đúng** cặp đồng-nghĩa (Configure↔Settings 0.605) với cặp khác-nghĩa (Log out↔Settings 0.391).
- **NHƯNG** "thấy vài ví dụ đúng" ≠ "chính xác đã được chứng minh". Để nói với hội đồng "matcher của tôi chính xác", **bắt buộc phải ĐO** nó trên một tập có nhãn người → ra **precision/recall**. **Hiện mình CHƯA làm bước đo này** → đây là lỗ hổng phải vá (đề xuất A4.4).
- Một điểm yếu cụ thể của embedding ngắn: với **tên nút rất ngắn / mơ hồ** ("OK", "Done", icon-only), embedding dễ nhầm. Đây là chỗ cần matcher lai (hybrid).

### A4.3. Bình thường người ta dùng gì? (để biết mình đang ở đâu)
| Nhóm | Model tiêu biểu | Ghi chú |
|---|---|---|
| **Local / mở** | `nomic-embed-text` (đang dùng), **BGE-M3 (BAAI)**, **multilingual-e5-large**, `all-mpnet-base-v2`, `gte-large` | Miễn phí; BGE-M3 & e5 **đa ngôn ngữ** (tốt cho cả tiếng Việt). |
| **Cloud API** | **OpenAI `text-embedding-3-small/large`**, Cohere `embed-v3`, Voyage `voyage-3`, Google Gemini embedding | Mạnh hơn, rẻ bất ngờ (tên nút rất ngắn → vài cent cho cả bộ). |
| **Bảng so sánh chuẩn** | **MTEB leaderboard** | Nơi cộng đồng xếp hạng embedding; `text-embedding-3-large`, BGE-M3, e5-mistral thuộc nhóm đầu. |
| **Cách ALOHa gốc làm** | LLM trích thực thể + so khớp ngữ-nghĩa (embedding) + ghép Hungarian | "Chuẩn ngành" cho đo hallucination = **LLM + embedding**, không chỉ so chuỗi. |

→ Mình đang ở nhóm "local đủ-dùng". Để **ra kết quả tốt nhất + thuyết phục**, nên nâng theo A4.4.

### A4.4. ĐỀ XUẤT — làm matcher tốt nhất có thể (xếp theo *đáng làm nhất*)

> Anh bảo "cứ đề xuất, tôi xem xét" — nên tôi liệt kê đủ, kèm **chi phí / lợi ích** để anh chọn. Tôi **chưa chạy gì** (tốn tiền/thời gian) cho tới khi anh duyệt.

**① ĐO ĐỘ ĐÚNG CỦA MATCHER (validate against human) — BẮT BUỘC, rẻ, mạnh nhất.**
- Cách: lấy ~**80–120 cặp** *(tên-model-viết, nhãn-thật-gần-nhất)* trải đều quanh ngưỡng → **anh gán nhãn tay** "cùng-element hay không" → tính **precision/recall/F1** của matcher.
- Lợi ích: biến câu "có chính xác không?" thành **một con số trong bài** ("matcher đạt P=.., R=.. so với người"). Đây là thứ reviewer của một bài-về-đánh-giá **đòi đầu tiên**.
- Chi phí: **$0**, ~1–2 giờ công anh.

**② HIỆU CHỈNH τ TRÊN TẬP CÓ NHÃN (đừng để 0.55 "bằng mắt").**
- Sau khi có tập nhãn ở ①, vẽ **đường precision–recall theo τ**, chọn τ theo **F1 cao nhất** hoặc theo **cố định precision ≥ 95%** (ưu tiên không-oan "bịa").
- Lợi ích: ngưỡng có **căn cứ định lượng**, không bị vặn "anh chọn 0.55 cho đẹp".
- Chi phí: $0, vài phút sau khi có ①. (Vẫn pre-register: chốt *quy tắc chọn τ* trước, rồi mới đọc số.)

**③ MATCHER LAI 3 TẦNG (hybrid) — tăng độ chính xác, kiểm soát chi phí.**
```
Tầng 1  So chuỗi chính xác/fuzzy (chuẩn-hoá + Levenshtein)  → khớp chắc, MIỄN PHÍ, precision cao
Tầng 2  Embedding cosine (cho cặp tầng-1 không quyết được)   → bắt đồng-nghĩa
Tầng 3  LLM-judge CHỈ cho vùng "lưỡng lự" (vd sim∈[0.45,0.65]) → hỏi "2 tên này cùng 1 nút trên màn?"
```
- Lợi ích: chính xác hơn hẳn embedding đơn; **LLM-judge chỉ chạy trên số ít cặp biên** → chi phí nhỏ.
- Chi phí: ~vài cent LLM cho vùng biên.

**④ NÂNG EMBEDDING + KIỂM ĐỘ BỀN (robustness) QUA 2 MODEL.**
- Chạy lại matcher với **`text-embedding-3-small`** (cloud, ~vài cent cho toàn bộ tên-nút) **hoặc** **BGE-M3** (local, đa ngôn ngữ) song song nomic.
- Báo "kết luận giữ nguyên dưới CẢ HAI embedding" → **robustness** mạnh, chống vặn "phụ thuộc 1 model".
- Tiện thể: BGE-M3/e5 **đa ngôn ngữ** → dùng được cho **demo tiếng Việt**.

**⑤ ĐỐI CHIẾU KHÔNG-GIAN (name + bbox) — grounding đa phương thức.**
- Hiện chỉ khớp **tên**. Có thể buộc model xuất thêm **toạ độ/điểm** rồi kiểm **point-in-bbox** (ScreenSpot). Cặp "tên + vị trí" giảm match-nhầm (2 nút trùng tên khác chỗ).
- Lợi ích: vá luôn lỗ hổng "Grounded ≈ Faithfulness" (H6). Chi phí: vừa (đổi prompt + chấm toạ độ).

**⑥ TIỀN-XỬ-LÝ TÊN (rẻ, nên làm kèm).**
- Chuẩn-hoá: hạ thường, bỏ dấu câu, gộp khoảng trắng, mở viết-tắt thông dụng, xử lý nút icon-only (lấy `content-desc` trong VH).
- Lợi ích: giảm nhiễu đầu vào cho cả 3 tầng. Chi phí: $0.

### A4.5. Khuyến nghị gọn (nếu anh muốn "tốt nhất mà vẫn gọn")
Làm **① + ② + ⑥** trước (đều **$0**, biến matcher từ "tin là đúng" thành "đo được là đúng" + ngưỡng có căn cứ). Nếu còn ngân sách/thời gian thì thêm **③** (LLM-judge vùng biên) và **④** (robustness 2 embedding). **⑤** để chung với việc ScreenSpot. → Đây là đường ngắn nhất để matcher **vừa chính xác hơn, vừa chống vặn được trước hội đồng**.

> **Tôi đề xuất bắt đầu bằng ① (đo precision/recall của matcher) — vì nó miễn phí, do anh chấm, và là thứ khiến phần lõi này "khoa học hoá" mạnh nhất.** Anh duyệt cái nào tôi dựng cái đó.

---
---

# PHẦN B — TRÌNH BÀY LẠI TOÀN BỘ NỘI DUNG (kế thừa 24, lồng giải thích)

## §0. Hình dung trong 30 giây
Người dùng đưa **1 ảnh màn app + 1 câu hỏi** ("Làm sao thêm chi phí?"). Máy trả **hướng dẫn từng bước** ("1. Bấm *Add expense*…"). Khó: model hay **bịa nút** + **không có đáp án vàng** để so. Luận văn làm 2 việc: (A) **lớp design-E** chống bịa + gọi đúng tên; (B) **cách đánh giá** đáng tin khi không có gold. **DG1** = đo cả hai trên hướng dẫn **1-màn**. (Nhiều màn xáo trộn → DG2, làm sau.)

## §1. Bối cảnh & hai đóng góp
- **Cái khó trung tâm:** không có kho "hướng dẫn chuẩn do người soạn" cho mọi app. Giải: **đừng tìm đáp-án-vàng-toàn-văn; neo vào sự thật rẻ-mà-có-sẵn = danh sách nút thật trên màn (oracle/VH).** Từ đó suy ra 3 thứ kiểm-được: *nút có thật* (không-bịa), *gọi đúng tên* (đúng-nhãn), *đúng khuôn* (format). → tinh thần neo bằng **silver** thay **gold**.
- **Hai đóng góp NGANG NHAU:** (A) **hệ design-E ra kết quả dương thật** (claim "mức-chắc-thắng": giảm bịa + tăng đúng-tên so model viết tự do); (B) **phương pháp đánh giá** khi không có gold ("null vẫn đậu" — pre-register).
- **Ranh giới:** **KHÔNG** claim SOTA leaderboard (ta sinh hướng dẫn *cho người*, không phải agent bấm máy → setup khác).

## §2. Thuật ngữ + LUẬT VÀNG

| Từ | Nghĩa | (Liên hệ câu hỏi của anh) |
|---|---|---|
| Tutorial / bước / element | hướng dẫn / một dòng / tên nút bước trỏ tới | — |
| **View Hierarchy (VH) / Oracle** | bản kê khai nút thật + tên + bbox của màn | **(A1)** "oracle" = thuật ngữ chuẩn (Barr et al. 2015), không phải tự bịa; thực chất là **silver oracle** vì VH có thể thiếu element |
| bbox | khung `(trái,trên,phải,dưới)` px | dùng cho point-in-bbox |
| Bịa / Grounding | nhắc nút không có / neo xuống nút thật | — |
| **BASE** | model viết **tự do**, chưa qua design-E | **(A3)** đây là **đối chứng**, để có cái so |
| **design-E (sysE)** | sau khi qua lớp kiểm-trung-thực | hệ của ta |
| Embedding / cosine | biến chữ thành vector / đo độ gần | **(A4)** lõi matcher |
| Pre-register | chốt giả thuyết+ngưỡng TRƯỚC khi chạy | chống "chỉnh số" |

> ### 🔒 LUẬT VÀNG (giám khảo kiểm đầu tiên)
> Oracle/VH **CHỈ dùng lúc CHẤM và SỬA**, **KHÔNG** đưa cho model lúc đang **sinh**. Lúc sinh model **chỉ thấy ẢNH + CÂU HỎI**. Nếu mớm danh sách nút thật cho model thì "không-bịa" thành hiển nhiên → kết quả giả (data leakage).

## §3. PIPELINE — 4 chặng

```
[Ảnh] ─► B1 Sinh CÂU HỎI use-case ─► questions.json (người duyệt)
[Ảnh+Hỏi] ─► B2 Sinh tutorial BASE (TỰ DO) ─► base steps
   BASE ─► B3 design-E: oracle KIỂM → SỬA(model khác)/FALLBACK ─► sysE steps
base+sysE ─► B4 CHẤM 5 thước đo trên CÙNG oracle + bootstrap CI ─► bảng
```

### B1 — Sinh câu hỏi (`dg1_questions.py`)
Đưa ảnh cho VLM, lệnh "viết 1 câu hỏi thực tế làm-được-ngay-trên-màn" → lưu `questions.json` → **người duyệt**.
> **(Diễn giải cho A2):** câu hỏi tự sinh **không** phá tính khoa học vì thước đo **không chấm câu hỏi** — nó chấm **hướng dẫn đối chiếu VH** (nguồn độc lập). Thêm nữa, BASE và sysE **dùng chung câu hỏi** nên thiên vị (nếu có) **tự khử** khi lấy hiệu. Rủi ro còn lại = câu *quá dễ* → chặn bằng duyệt + đo độ-khó + Track B.

### B2 — Sinh tutorial BASE (`dg1_run.py → gen_tutorial`)
Đưa **ảnh + câu hỏi**, ép JSON `{"steps":[{"verb","element","note"}]}`. **Prompt thật** (trích code):
> *"Each step must name the button/field by its EXACT on-screen text. Do NOT invent buttons that are not visible."*
> **(Diễn giải cho A3):** đây **là baseline = chưa có design-E**, chỉ để so. Và baseline **đã được nhắc đừng bịa** ngay trong prompt → ta **không dìm** đối chứng; design-E thắng nhờ cơ chế, không nhờ baseline yếu.

### B3 — Lớp design-E (`dg1_run.py → apply_designE`) ⭐ LÕI
Duyệt **từng bước**: hỏi oracle "nút này có thật?" bằng **matcher ALOHa** (§4.1 / A4). 3 nhánh (đúng code):
1. **matched** (sim ≥ 0.55) → giữ nguyên.
2. **không khớp** → gọi **model KHÁC** (`llama3.2`) đưa *danh sách nút thật + ý định bước* → chọn 1 nút thật:
   - chọn được → **corrected** (thay tên-ma bằng tên thật).
   - "NONE"/vẫn không khớp → **fallback**: `element = "(describe) ..."` (mô tả-lời, **không** tính bịa).
> **(Diễn giải cho A4 — vì sao đây là LÕI):** chính ở bước này matcher quyết định **sửa hay không, fallback hay không**. Matcher sai → sửa nhầm/bỏ sót → hỏng cả pipeline lẫn điểm. Đó là lý do A4.4 đề xuất **đo + nâng matcher**.
> **Vì sao dùng model KHÁC để sửa?** chống model tự-bao-che + cho thấy bước-sửa là module độc lập, thay được.

### B4 — Chấm (`dg1_score_all.py`)
Chấm **cả BASE lẫn sysE** trên **cùng oracle** → 5 thước đo + **bootstrap CI ghép-cặp**. Matcher dùng để **chấm** và bước **sửa** là 2 khâu tách biệt (không tự-chấm vòng tròn).

## §4. METRIC — 5 thước đo

### 4.1. Matcher ALOHa (lõi dùng chung) — xem chi tiết & đề xuất ở **PHẦN A4**
Tóm: embedding `nomic-embed-text` (local) → cosine → khớp nếu ≥ **τ=0.55** (pre-register). Cột *đúng-nhãn* so **chuỗi chính xác**, tách khỏi cột *ngữ-nghĩa*. *Nguồn:* **ALOHa, Petryk et al., NAACL 2024** (kiểm lại venue trước khi nộp). **Khuyến nghị nâng cấp ở A4.4** (đo P/R, hiệu chỉnh τ, hybrid 3 tầng, robustness 2 embedding…).

### 4.2. Faithfulness — "không bịa" *(chính #1)*
`faith = 1 − (số button-step trỏ nút KHÔNG tồn tại)/n`. VD 4 bước, 1 nút-ma → 75%. **sysE ~100% là DO THIẾT KẾ** (đọc §7).

### 4.3. Đúng-nhãn/Clarity — "gọi đúng tên hiển thị" *(chính #2)*
`label_fid = (button-step trùng-hệt nhãn thật)/(button-step)`. Khắt khe hơn Faithfulness (không nhận đồng-nghĩa) → **mức tăng là cải thiện THẬT** (VD "Lưu lại"≠"Save" → trượt). *Nguồn:* Style/Clarity (Chim/Ive/Liakata, CL 2025).

### 4.4. Grounded-existence
`grounded = (button-step khớp nút thật)/n`. Ở BASE gần trùng Faithfulness → cần **ScreenSpot point-in-bbox độc lập**. *Nguồn:* SeeClick, ACL 2024.

### 4.5. Format
`format = (bước mở đầu bằng động từ)/n`. design-E không đụng → BASE=sysE là **sanity-check đúng kỳ vọng**. *Nguồn:* IFEval.

### 4.6. Coverage (proxy)
`coverage = |nút-thật-được-nhắc|/|nút actionable|`. **Là proxy** (DG1 không có gold-steps; 1 câu chỉ cần 1–2 nút trên màn chục nút) → **thấp là đương nhiên kể cả khi đúng**; **không** làm headline. Coverage thật ở DG2.

## §5. THỐNG KÊ
- **Ghép-cặp:** mỗi màn 1 hiệu `(sysE−BASE)` → khử yếu-tố-màn-khó.
- **Bootstrap:** rút lại 80 hiệu (có hoàn lại) **2000 lần** → lấy phân vị 2.5%/97.5% = **CI 95%**.
- **Đọc:** CI **không chứa 0** ⇒ có ý nghĩa thống kê.
- **Pre-register:** chốt trước giả thuyết + τ=0.55 + cách tính CI + quy tắc quyết định ⇒ chống "chỉnh số".

## §6. VÍ DỤ CHẠY XUYÊN SUỐT 1 MÀN
**VH (oracle):** `Add expense, Amount, Category, Save, Settings, Back`. **Câu hỏi:** "thêm khoản chi mới?".

**BASE (model tự do):** 1.Tap **Add new** ❌ · 2.Enter **Amount** ✅ · 3.Select **Category** ✅ · 4.Tap **Confirm** ❌
→ Faithfulness = 1−2/4 = **50%**; Đúng-nhãn = 2/4 = **50%**.

**design-E:** "Add new"→**SỬA**→"Add expense"; "Amount" giữ; "Category" giữ; "Confirm"→**SỬA**→"Save".
→ Faithfulness = **100%**; Đúng-nhãn = **100%**.

**Đọc:** Faithfulness 50→100 phần lớn **do thiết kế** (chặn nút-ma); *giá-trị-đo-được* = BASE bịa 2/4 bước (rủi ro được loại). Đúng-nhãn 50→100 là **cải thiện thật** (sửa đúng tên trên màn). Nhân lên 80 màn + bootstrap → §7.

## §7. KẾT QUẢ THẬT (80 màn, sinh = gpt-4o-mini)

| Thước đo | BASE | design-E | Chênh [95% CI] |
|---|---|---|---|
| **Faithfulness** | 75.4% | **100.0%** | **+24.6pp [+16.2, +33.3]** |
| **Đúng-nhãn** | 67.9% | **89.8%** | **+21.9pp [+14.8, +30.0]** |
| Grounded | 75.4% | 97.3% | — |
| Format | 74.4% | 74.4% | (không đụng) |
| Coverage(proxy) | 28.8% | 34.6% | (limitation) |

design-E: **SỬA 24 bước** + **FALLBACK 4 bước**. **Đọc đúng:** (1) 2 metric chính CI loại 0 ⇒ có ý nghĩa; (2) Faithfulness ~100% **do thiết kế** → giá-trị thật = *BASE bịa 24.6%* + *Đúng-nhãn +21.9pp là thật*; (3) khớp claim "mức-chắc-thắng", **không** SOTA; (4) Coverage proxy; (5) Grounded≈Faithfulness → cần ScreenSpot; (6) Format đứng yên = sanity đúng.

## §8. HỘI ĐỒNG SẼ HỎI GÌ (trả lời sẵn)
- **H1 "Có oracle thì không-bịa hiển nhiên?"** → con số 100% do thiết kế (đã khai); đóng góp = *đo được BASE bịa 24.6%* + *đúng-nhãn +21.9pp thật* + *cách-đánh-giá (B)*.
- **H2 "Metric có đáng tin / đo đúng thứ nó nói không?"** → validate **TỰ ĐỘNG bằng perturbation test** (bơm lỗi đã-biết, kiểm metric bắt được — §C3). **Không** dựa chấm-người (thầy không ưa). Track B chỉ còn là sanity nhỏ tùy chọn / future-work.
- **H3 "Câu hỏi tự sinh thiên vị / dở?"** → **(xem A2 + §C)** thước đo neo VH độc lập + ghép-cặp khử thiên vị + **gieo câu hỏi từ nút-thật** + **cổng answerability tự động**.
- **H4 "Baseline bị dìm?"** → không, BASE đã được prompt "đừng bịa".
- **H5 "Chỉ 1 model?"** → cần model #2; local bất khả (không GPU) → API cloud hoặc future-work.
- **H6 "Grounded≈Faithfulness?"** → bổ sung ScreenSpot point-in-bbox.
- **H7 "Sao dùng llama3.2 để sửa?"** → chống tự-bao-che + module độc lập.
- **H8 "Coverage thấp?"** → proxy, không headline.
- **H9 "n=80 đủ?"** → hiệu ứng lớn + CI loại 0 rõ.
- **H10 "Sao chưa so GPT-4o E2E?"** → kế hoạch bonus, tốn API.
- **H11 (MỚI) "Matcher local có đáng tin?"** → **(xem A4)** sẽ **đo precision/recall của matcher với người**, hiệu chỉnh τ trên tập nhãn, và (tùy ngân sách) hybrid 3 tầng + robustness 2 embedding.
- **H12 (MỚI) "Oracle tự đặt tên?"** → **(xem A1)** "oracle" = thuật ngữ chuẩn (Barr et al. 2015); ta dùng **silver oracle** (VH có thể thiếu element → đóng khung "có điều kiện độ-phủ VH").

## §9. GIỚI HẠN (khai trước)
L1 Faithfulness do-thiết-kế → tách bạch khi báo. · L2 Chưa Track B → việc bắt buộc. · L3 Mới 1 model sinh. · L4 Grounded≈Faithfulness → ScreenSpot. · L5 Coverage proxy. · L6 Câu hỏi máy soạn (có duyệt). · L7 Nhãn tiếng Anh; VN demo định tính. · **L8 Oracle/VH có thể thiếu element (silver, không gold)** → khung "có điều kiện độ-phủ". · **L9 (MỚI) Matcher chưa được đo P/R** → A4.4-① bắt buộc.

## §10. Chi phí & môi trường
Sinh = gpt-4o-mini cloud (~$0.05/80 màn). Sửa = llama3.2 local; matcher = nomic-embed local (free). **🔴 Không GPU ⇒ VLM nhìn-ảnh local >5ph/ảnh, không dùng được** ⇒ sinh-từ-ảnh phải API cloud (kéo theo H5/model #2 cũng phải cloud). Đã chống 429 (retry/backoff).

## §11. Đã xong / Còn lại
**✅** 80 câu hỏi · 80 màn BASE+design-E · 5 thước đo + CI · hạ tầng (retry, matcher batch+cache) · Track B dựng sẵn.
**⏳** (1) **Validate metric TỰ ĐỘNG bằng perturbation** [§C3 — thay Track B, hợp ý thầy]; (2) **Đo P/R + nâng matcher** [A4.4 — lõi]; (3) **Gieo câu hỏi từ nút-thật + cổng answerability tự động** [§C2]; (4) **Model #2** [H5]; (5) **ScreenSpot** [H6]; (6) demo tiếng Việt. *(Track B chấm-người: hạ xuống tùy-chọn/future-work.)*

## §12. Bản đồ file code
`dg1_questions.py` (B1) · `dg1_run.py` (B2+B3, đã đọc: prompt + apply_designE 3 nhánh) · `aloha_match.py` (matcher τ=0.55 + cache) · `dg1_score_all.py` (B4 + bootstrap) · `dg1_scorer.py` (point-in-bbox, bẫy dữ liệu MV) · `trackB_html.py` (Track B) · `_http.py` (retry 429) · `_apikey.py` (đọc khoá, KHÔNG in) · `dg1_cache/` (câu hỏi, runs, emb_cache).

## §13. MỘT DÒNG
**DG1 đo lớp design-E trên hướng dẫn 1-màn: model sinh (chỉ thấy ảnh+câu hỏi) → oracle/VH kiểm bằng matcher ALOHa → sửa(model khác)/mô-tả-lời → chấm 5 thước đo, bootstrap CI ghép-cặp. 80 màn (gpt-4o-mini): giảm bịa +24.6pp & tăng đúng-nhãn +21.9pp (CI loại 0). 4 thắc mắc đã gỡ: (A1) "oracle" là thuật ngữ chuẩn (silver, không gold); (A2) câu-hỏi-tự-sinh không phá khoa học vì thước đo neo VH độc lập + ghép-cặp khử thiên vị + validate-tự-động; (A3) BASE = đối chứng; (A4) matcher là LÕI — phải ĐO precision/recall + hiệu chỉnh τ + (tùy ngân sách) hybrid 3 tầng & robustness 2 embedding. Còn lại: validate-tự-động (perturbation) + nâng matcher + gieo-câu-hỏi-từ-nút-thật + model #2 + ScreenSpot.**

---
---

# PHẦN C — "CÂU HỎI DỞ THÌ SAO?" & VALIDATE KHÔNG CẦN CHẤM-NGƯỜI

> Phần này trả lời sâu **hai** điều anh nêu: (1) *nếu câu hỏi không tốt thì làm sao có câu trả lời tốt / đánh giá có còn nghĩa?* và (2) *thầy không thích chấm-người (Track B) — thay bằng gì cho khách quan?*
> **Kết luận trước:** kết quả CHÍNH của DG1 **không** phụ thuộc "câu hỏi tốt hay dở", và việc validate metric **chuyển hẳn sang TỰ ĐỘNG** (perturbation/sensitivity test), không cần chấm-người.

## §C1. Vì sao "câu hỏi dở → trả lời dở" KHÔNG phá kết quả chính (3 lý do)

**Lý do 1 — Headline là so-cặp CÙNG-CÂU-HỎI → chất lượng câu hỏi tự triệt tiêu.**
Claim chính của luận văn là **tương đối**: "design-E **tốt hơn BASE**", chứ không phải "hướng dẫn tốt tuyệt đối". Mà BASE và design-E **trả lời CÙNG MỘT câu hỏi**. Nên dù câu hỏi dở cỡ nào, nó **dở y hệt cho cả hai nhánh** → khi lấy hiệu `(design-E − BASE)`, phần "dở do câu hỏi" **bị khử sạch**. Cái còn lại đúng bằng **tác dụng của lớp trung-thực-hoá** (sửa nút-ma, gọi đúng tên). → Câu hỏi dở chỉ đe doạ một claim **tuyệt đối** mà **ta không hề tuyên bố**.

**Lý do 2 — Thước đo là tính-chất NỘI-TẠI của (hướng dẫn ↔ màn), không phải của câu hỏi.**
"Không-bịa / đúng-nhãn / grounded / format" đo *"các bước có trỏ đúng nút THẬT trên MÀN, đúng tên, đúng khuôn không"*. Đây là quan hệ giữa **hướng dẫn và màn hình**, **không** cần câu hỏi phải "chuẩn". Một câu hỏi mơ hồ, nếu model viết ra các bước trỏ nút thật, vẫn **grounded**. → Biến-phụ-thuộc xác định rõ kể cả khi câu hỏi không hoàn hảo.

**Lý do 3 — Ta KHÔNG xây hệ hỏi-đáp (QA).** Đối tượng đo là **"lớp sinh có bịa không"**, không phải "trả lời câu hỏi có đúng không". Câu hỏi chỉ là **cái cớ để ép model viết một hướng dẫn** đặng đem đi soi tính trung-thực.

> **Rủi ro còn sót (phải khai):** nếu câu hỏi **không-trả-lời-được trên màn** (hỏi việc thuộc màn khác) thì model **buộc phải bịa** → cảnh thoái hoá. Cái này **không** được Lý-do-1/2 che. ⇒ **bắt buộc có cổng answerability** (§C2). Còn câu *quá dễ* thì chỉ làm điểm tuyệt đối cao, **không** làm sai claim tương đối (Lý do 1).

## §C2. Làm câu hỏi TỐT mà KHÔNG cần người duyệt (đề xuất, anh chọn)

**Đề xuất ① — GIEO CÂU HỎI TỪ NÚT-THẬT (affordance-seeded). ⭐ khuyến nghị.**
Thay vì để model "tự nghĩ ra câu hỏi" (dễ tào lao / tự-phục-vụ), ta **lấy một nút actionable THẬT từ VH** (gọi là target X) rồi yêu cầu model: *"viết một câu hỏi tự nhiên mà người dùng sẽ hỏi, có lời giải là DÙNG tính năng '{X}' trên màn này."*
- **Đảm bảo trả-lời-được** (X tồn tại) → diệt rủi ro câu-không-trả-lời-được tận gốc.
- **Có target X đã-biết** → cho phép một **tín hiệu task-success YẾU, TỰ ĐỘNG**: hướng dẫn có dẫn tới X không? (không cần người chấm).
- **Phá vòng tự-phục-vụ:** seed X đến từ **oracle/VH**, không phải tưởng tượng của model; và model viết hướng dẫn **KHÔNG thấy X** (chỉ thấy câu hỏi + ảnh) → việc chấm "có tới X không" là **reference-based hợp lệ**.
- Vẫn giữ được "câu hỏi NGÔN NGỮ TỰ NHIÊN" (đúng hợp-đồng sản phẩm) vì model chỉ diễn đạt, còn target do oracle gieo.

**Đề xuất ② — CỔNG ANSWERABILITY TỰ ĐỘNG (bắt buộc, rẻ).**
Mỗi câu hỏi chỉ được giữ nếu **mục-tiêu của nó ánh xạ được tới ≥1 nút thật trong VH** (kiểm bằng matcher). Câu rớt cổng → loại tự động. **Báo cáo tỉ lệ loại** (drop rate). → Bỏ được khâu "người duyệt".

**Đề xuất ③ — TÁCH MODEL hỏi ≠ model trả lời.** Model M1 sinh câu hỏi, model M2 (khác) viết hướng dẫn → M2 không "trả lời câu hỏi do chính nó bịa ra cho hợp gu mình" → giảm thiên vị tự-phục-vụ.

**Đề xuất ④ (tùy chọn) — MƯỢN MỤC TIÊU NGƯỜI-THẬT từ AndroidControl.** Lấy từng màn lẻ + goal có sẵn (người soạn) làm "câu hỏi" → khỏi sinh, dùng goal thật. Mạnh nhưng trộn dataset; để dự phòng.

> **Khuyến nghị §C2:** ① + ② + ③ (đều tự động) → câu hỏi **đảm bảo trả-lời-được, có target để chấm, không tự-phục-vụ, không cần người duyệt**.

## §C3. VALIDATE METRIC KHÔNG CẦN CHẤM-NGƯỜI — Perturbation / Sensitivity test ⭐ (thay Track B)

**Vấn đề:** làm sao chứng minh "metric đo ĐÚNG thứ nó nói" mà **không** đi nhờ người chấm (thầy không ưa)?

**Ý tưởng (chuẩn ngành — *construct validity by controlled perturbation*):** tự tay **bơm lỗi ĐÃ-BIẾT** vào một hướng dẫn đúng, rồi kiểm metric **có phản ứng đúng kỳ vọng không**. Vì lỗi do mình tạo nên **đáp án đúng đã biết trước** → đo được **độ nhạy + độ chính xác của metric** hoàn toàn tự động, tái lập 100%.

**Bộ test bơm-lỗi (pre-register ngưỡng trước):**
| Phép bơm lỗi | Kỳ vọng metric phản ứng | Kiểm điều gì |
|---|---|---|
| Đổi 1 nút THẬT → **nút-ma** (tên không có trên màn) | **Faithfulness GIẢM** đúng ~1/n | bắt được bịa |
| Đổi 1 nút → **đồng-nghĩa** ("Save"→"Store") | **Đúng-nhãn giảm**, **Faithfulness GIỮ** | tách đúng 2 trục (không lẫn) |
| Xáo/bỏ động từ đầu bước | **Format giảm** | bắt lỗi khuôn |
| Đổi nút thật → **nút thật KHÁC nhưng đúng tên** | **KHÔNG metric nào báo lỗi** | **false-positive** (không "vu oan") |
| Bỏ bớt 1 bước cần thiết | Coverage giảm | độ nhạy coverage |

**Báo cáo:** *detection rate* (bắt đúng lỗi đã bơm), *false-positive rate* (không vu oan khi không có lỗi), *tính đơn-điệu* (bơm càng nhiều lỗi điểm càng xuống). → Đây là **bằng chứng metric đáng tin, KHÁCH QUAN, không người chấm.**

**Vì sao thầy sẽ thích hơn Track B:** (a) **không chủ quan** (không phụ thuộc gu người chấm); (b) **tái lập** (ai chạy lại cũng ra y hệt); (c) **đo trực tiếp** thứ ta quan tâm (metric có phân biệt đúng/sai không), thay vì đo gián tiếp qua "người có đồng ý không". Đây cũng đồng điệu với tinh thần **test nhạy-thứ-tự** đã pre-register cho DG2.

> **Track B (chấm-người) → HẠ XUỐNG tùy-chọn/future-work:** nếu sau này có hội đồng đòi "đối chiếu người", có thể chạy một **sanity nhỏ do CHUYÊN GIA** (gold-curated, không phải crowd), đóng khung là phụ. **Không** còn là trụ validate chính.

## §C4. Điều chỉnh PRE-REGISTRATION (đã cập nhật ở file `22`)
- **H3 cũ** (metric tương quan với người — Track B) → **ĐỔI thành H3 mới:** *metric vượt bộ perturbation/sensitivity test với ngưỡng pre-register* (detection ≥ ngưỡng, false-positive ≤ ngưỡng, đơn-điệu).
- Câu hỏi: bổ sung **gieo-từ-nút-thật + cổng answerability tự động** vào mục "cấu hình cố định".
- Track B: ghi rõ **tùy chọn, 1-người, future-work** — không nằm trong tiêu chí đậu/rớt.

> **MỘT DÒNG PHẦN C:** câu hỏi dở **không** phá kết quả vì headline là so-cặp cùng-câu-hỏi (tự khử) + metric nội-tại theo màn; để chắc, **gieo câu hỏi từ nút-thật + cổng answerability tự động**; và việc **chứng minh metric đáng tin chuyển sang PERTURBATION TEST tự động** (bơm lỗi đã-biết, đo detection/false-positive) — **bỏ phụ thuộc chấm-người** đúng ý thầy.
