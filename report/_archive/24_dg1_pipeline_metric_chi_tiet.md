# 📘 DG1 — PIPELINE & METRIC GIẢI THÍCH CHI TIẾT (bản dành cho người mới **và** giám khảo khó tính)

> **File này tự chứa — đọc một mạch từ trên xuống là hiểu trọn vẹn.** Không cần mở file nào khác trước.
> Mục tiêu kép: (1) một **người chưa biết gì** đọc vẫn theo được từng bước; (2) một **giám khảo khó tính** đọc tới đâu cũng thấy chỗ nghi ngờ của mình đã được trả lời tới đó.
>
> Cách đọc nhanh theo vai:
> - **Người mới:** đọc §0 → §1 → §2 → §3 → §6 (ví dụ xuyên suốt) → §7.
> - **Giám khảo:** đọc §0 → §8 (HỘI ĐỒNG SẼ HỎI GÌ) → §9 (giới hạn) → §7 (kết quả) → §5 (thống kê).
>
> *Viết 2026-06-28, cập nhật 2026-06-29 sau khi chạy thật 80 màn.*

---

## MỤC LỤC
- §0. Hình dung trong 30 giây
- §1. Bối cảnh & **hai đóng góp** của luận văn (vì sao bài toán này khó)
- §2. Thuật ngữ (đọc 1 lần, theo được cả file)
- §3. PIPELINE — hệ thống chạy thế nào (từng chặng, có lý do thiết kế)
- §4. METRIC — 5 thước đo (định nghĩa + công thức + ví dụ số + nguồn)
- §5. THỐNG KÊ — vì sao con số đáng tin (bootstrap, pre-registration)
- §6. **VÍ DỤ CHẠY XUYÊN SUỐT 1 MÀN** (xem số ra ở đâu)
- §7. KẾT QUẢ THẬT 80 màn + đọc cho đúng
- §8. **HỘI ĐỒNG KHÓ TÍNH SẼ HỎI GÌ — trả lời sẵn** ⭐
- §9. GIỚI HẠN & mối đe doạ tính hợp lệ (khai trước, không giấu)
- §10. Chi phí & môi trường
- §11. Đã xong / còn lại
- §12. Bản đồ file code
- §13. Một dòng tóm

---

## §0. Hình dung trong 30 giây

Người dùng đưa **1 ảnh màn hình app + 1 câu hỏi** (ví dụ: *"Làm sao để thêm một khoản chi tiêu?"*). Máy phải trả về **hướng dẫn từng bước**:

```
1. Bấm nút "Add expense" ở góc dưới bên phải.
2. Nhập số tiền vào ô "Amount".
3. Bấm "Save".
```

**Vấn đề cốt lõi:** model AI (kể cả model mạnh) thường **bịa ra nút không có trên màn** — gọi là *hallucination* (ví dụ bảo "Bấm *Thanh toán*" trong khi màn không hề có nút đó). Người dùng làm theo sẽ bí ngay. Và **không có sẵn "đáp án mẫu" do người soạn** để so sánh → nên **không dễ biết hướng dẫn nào tốt, hướng dẫn nào tệ**.

Luận văn giải quyết bằng **hai thứ song song**:
1. Một **lớp kiểm-tra-trung-thực** (đặt tên **design-E**) gắn thêm vào model, để hướng dẫn **không bịa** và **gọi đúng tên nút thật**.
2. Một **cách đánh giá** đáng tin **khi không có đáp án vàng**, gồm 5 thước đo neo vào "sự thật trên màn".

**DG1** = phần thí nghiệm đo cả hai thứ trên, **trên hướng dẫn 1-màn** (trường hợp đơn giản nhất, không cần sắp xếp nhiều màn).
> *(Nhánh khó hơn — nhiều màn bị xáo trộn, máy phải tự suy ra thứ tự đúng rồi mới viết hướng dẫn — gọi là **DG2**, làm ở giai đoạn sau / bài báo sau. File này KHÔNG bàn DG2.)*

---

## §1. Bối cảnh & HAI đóng góp (vì sao bài toán khó, đóng góp nằm ở đâu)

### 1.1. Vì sao "không có đáp án vàng" là cái khó trung tâm
Với hầu hết bài toán AI, người ta có **bộ đáp án chuẩn do người soạn** (gold) để chấm: dịch máy có bản dịch mẫu, tóm tắt có bản tóm tắt mẫu. Ở đây **không có** một kho "hướng dẫn sử dụng chuẩn" cho mọi màn của mọi app — soạn tay thì vừa tốn kém vừa không tổng quát. Vậy làm sao **chấm** được hướng dẫn máy viết?

Luận văn trả lời: **đừng đi tìm đáp-án-vàng-toàn-văn; hãy neo vào một sự thật rẻ và sẵn có** — đó là **danh sách các nút/ô thật trên màn** (cây giao diện của hệ điều hành cung cấp). Từ sự thật đó suy ra được 3 điều kiểm chứng được: *nút có thật không* (không-bịa), *gọi có đúng tên không* (đúng-nhãn), *có đúng khuôn hướng dẫn không* (format). Đó là tinh thần "neo bằng **silver** (nhãn tự động đủ tin) thay cho **gold** (nhãn người soạn)".

### 1.2. Hai đóng góp NGANG NHAU (chốt của luận văn)
- **(A) HỆ THỐNG sinh hướng dẫn tốt — design-E.** Phải **ra kết quả dương thật sự**: hướng dẫn của hệ **giảm bịa** và **tăng gọi-đúng-tên** so với chính model đó viết tự do. Đây là claim **"mức-chắc-thắng"** (an toàn, kỳ vọng kết quả dương).
- **(B) PHƯƠNG PHÁP ĐÁNH GIÁ — 5 thước đo + quy trình.** Đánh giá đáng tin **khi không có gold tutorial**. Phần này theo nguyên tắc **"null vẫn đậu"**: kể cả kết quả ra trung tính, miễn đã **đăng ký trước (pre-register)**, vẫn là đóng góp khoa học.

> **Ranh giới phải nói thẳng với hội đồng:** luận văn **KHÔNG** claim "SOTA leaderboard". Lý do: ta sinh **hướng dẫn cho người đọc**, không phải agent bấm máy tự động — **setup khác** các bảng xếp hạng GUI-agent, nên so trực tiếp là khập khiễng. Ta chỉ claim "tốt hơn baseline cùng điều kiện".

---

## §2. Thuật ngữ (đọc 1 lần là theo được cả file)

| Từ | Nghĩa dễ hiểu | Vì sao cần biết |
|---|---|---|
| **Tutorial / hướng dẫn** | Danh sách bước "1. Bấm X, 2. Nhập Y…" máy sinh ra. | Đây là **đầu ra** ta đi chấm. |
| **Bước (step)** | Một dòng hướng dẫn, gồm 3 phần: **động từ** (Bấm/Nhập…), **element** (tên nút/ô), **note** (ghi chú ngắn). | Mọi thước đo đều tính trên từng bước. |
| **Element** | Tên của một nút / ô / mục mà bước trỏ tới (ví dụ "Add expense"). | Cái dễ bị bịa nhất. |
| **View Hierarchy (VH) / Oracle** | "Bản kê khai" hệ điều hành Android cung cấp cho mỗi màn: liệt kê **mọi nút/ô thật** + **tên** + **toạ độ khung (bbox)**. | Đây là **sự thật** để đối chiếu. Gọi là **oracle** = "lời sấm" biết đâu là nút thật. |
| **bbox** | Khung chữ nhật của 1 nút: `(trái, trên, phải, dưới)` tính bằng pixel. | Dùng cho grounding "điểm-nằm-trong-khung". |
| **Bịa (hallucination)** | Hướng dẫn nhắc một nút **không tồn tại** trên màn. | Lỗi nguy hiểm nhất với người dùng. |
| **Grounding ("neo")** | Tên/toạ độ trong hướng dẫn có khớp nút thật không. | Trục đo độ-bám-thực-tế. |
| **BASE** | Hướng dẫn model viết **tự do**, **chưa** qua lớp kiểm tra. | Đây là **nhóm đối chứng** (so sánh để thấy lớp design-E có tác dụng). |
| **design-E (sysE)** | Hướng dẫn **sau khi** đi qua lớp kiểm-tra-trung-thực. | Đây là **hệ của ta**. |
| **MobileViews** | Bộ dữ liệu nhiều nghìn ảnh màn app Android **kèm VH thật**. Ta lấy 80 màn. | Nguồn dữ liệu DG1 (vì có sẵn bbox để chấm grounding). |
| **Embedding** | Biến một chuỗi chữ thành một **vector số** sao cho chữ cùng nghĩa cho vector gần nhau. | Lõi của matcher (so theo nghĩa, không so chữ cứng). |
| **Pre-register** | Chốt giả thuyết + ngưỡng + cách tính **TRƯỚC** khi chạy/nhìn kết quả. | Chống vặn "chỉnh số cho đẹp". |

> ### 🔒 LUẬT VÀNG (bất biến — giám khảo sẽ kiểm cái này đầu tiên)
> Oracle/VH **CHỈ dùng ở khâu CHẤM và khâu SỬA**, **TUYỆT ĐỐI KHÔNG** đưa cho model lúc nó **đang sinh** hướng dẫn.
> - **Lý do:** nếu lúc sinh đã đưa danh sách nút thật cho model, model chỉ việc chép → "không-bịa" trở thành hiển nhiên và **kết quả tốt là giả** (data leakage).
> - **Lúc sinh, model chỉ thấy: ẢNH + CÂU HỎI.** Hết. Danh sách nút thật xuất hiện **sau đó**, ở khâu kiểm và khâu sửa.
> Đây là điều phân biệt một thí nghiệm trung thực với một thí nghiệm "mớm bài".

---

## §3. PIPELINE — hệ thống chạy thế nào (từng chặng, kèm lý do thiết kế)

Toàn bộ code nằm trong thư mục `harness/`. Có **4 chặng** B1→B4. Sơ đồ tổng:

```
                 ┌──────────────────────────────────────────────────────────┐
   [Ảnh màn] ───►│ B1  Sinh CÂU HỎI use-case  →  questions.json  (người duyệt)│
                 └──────────────────────────────────────────────────────────┘
                 ┌──────────────────────────────────────────────────────────┐
[Ảnh + Câu hỏi]─►│ B2  Sinh tutorial BASE (model viết TỰ DO)  →  base steps  │
                 └──────────────────────────────────────────────────────────┘
                 ┌──────────────────────────────────────────────────────────┐
     base steps─►│ B3  Lớp design-E: oracle KIỂM → SỬA / FALLBACK → sysE steps│
                 └──────────────────────────────────────────────────────────┘
                 ┌──────────────────────────────────────────────────────────┐
 base + sysE  ──►│ B4  CHẤM 5 thước đo trên CÙNG oracle → bảng + CI bootstrap │
                 └──────────────────────────────────────────────────────────┘
```

### B1 — Sinh câu hỏi use-case  (`dg1_questions.py`)
- **Làm gì:** đưa **ảnh màn** cho một VLM (model nhìn-ảnh-hiểu-chữ) kèm lệnh: *"Nhìn màn này, viết MỘT câu hỏi thực tế người dùng có thể hỏi, về việc LÀM ĐƯỢC NGAY trên màn này."*
- **Ra:** 1 câu hỏi/màn → lưu `harness/dg1_cache/questions.json`. Sau đó **người duyệt** loại câu vô lý.
- **Protocol chống thiên vị (giám khảo sẽ hỏi):** mỗi màn đúng 1 câu; nội dung câu phải **giải-quyết-được-ngay-trên-màn-đó** (không hỏi việc thuộc màn khác); sinh **tự động hàng loạt** rồi người duyệt — **không** tự tay viết từng câu để "né" lỗi của model. Số lượng công bố: **80**.
- **Vì sao máy tự soạn (không lấy có sẵn)?** Vì không tồn tại bộ câu-hỏi-chuẩn cho từng màn của mọi app. Ta **công khai** đây là một **giới hạn** (§9), không giấu.

### B2 — Sinh tutorial BASE  (`dg1_run.py` → `gen_tutorial`)
- **Làm gì:** đưa **ảnh + câu hỏi** cho model, ép trả về **JSON thuần** đúng khuôn:
  ```json
  {"steps":[{"verb":"Tap","element":"Add expense","note":"góc dưới phải"}]}
  ```
- **Lệnh ép (prompt):** *"Mỗi bước phải gọi nút/ô bằng ĐÚNG chữ hiển thị trên màn. KHÔNG bịa nút không thấy."*
  > Lưu ý công bằng: ngay cả BASE cũng đã **được nhắc đừng bịa**. Tức là design-E **không thắng nhờ baseline bị làm yếu đi** — baseline đã được prompt tử tế. design-E thắng nhờ **cơ chế kiểm-tra**, không nhờ "dìm" đối chứng.
- **Ra:** danh sách bước **chưa kiểm tra** = **BASE**.

### B3 — Lớp design-E  (`dg1_run.py` → `apply_designE`)  ⭐ **PHẦN LÕI**
Duyệt **từng bước** của BASE. Với mỗi bước, hỏi oracle: *"nút `element` này có THẬT trên màn không?"* — đối chiếu danh sách nhãn trong VH **bằng matcher ALOHa** (so theo nghĩa, xem §4.1). Ba khả năng:

1. **Khớp** (`matched`) → nút có thật → **giữ nguyên** bước.
2. **Không khớp** (bước đang trỏ "nút-ma") → gọi **một model KHÁC** (ở đây `llama3.2` chạy local) và đưa cho nó: **danh sách nút thật** + **ý định của bước** → yêu cầu **chọn 1 nút thật đúng nhất**:
   - Chọn được nút thật hợp lý → **SỬA** (`corrected`): thay tên-ma bằng **tên thật**.
   - Không nút nào hợp → **FALLBACK** (`fallback`): đổi bước thành **mô tả bằng lời** (ví dụ *"(mô tả) mở phần cài đặt"*) — **không** còn khẳng định một nút cụ thể nào, nên **không** bị tính là bịa.

> **Trực giác cốt lõi để giải thích cho hội đồng:** design-E **không làm model thông minh hơn**. Nó **đứng chặn ở đầu ra**: thấy bước nào trỏ nút không có thật thì **vá lại bằng thông tin thật** (sửa) hoặc **hạ cấp về mô tả an toàn** (fallback). Vì cơ chế này **không phụ thuộc model sinh là ai**, ta gọi nó là **"lớp trung-thực-hoá độc-lập-model"** — về lý thuyết gắn được vào GPT, Qwen, Gemini… như nhau.

> **Vì sao dùng MODEL KHÁC để sửa (không để chính model sinh tự sửa)?** Để **tránh model tự bao che lỗi của mình** và để cho thấy bước sửa là một **module độc lập**, thay được. Đây cũng là điểm thiết kế chống "vòng lập-luận tự-chấm".

### B4 — Chấm điểm  (`dg1_score_all.py`)
- Chấm **CẢ BASE LẪN sysE** trên **CÙNG một** oracle, ra **5 thước đo** (§4).
- Tính **khoảng tin cậy 95%** bằng **bootstrap ghép-cặp theo từng màn** (§5).
- **Điểm trung thực:** matcher dùng để **chấm** (§4.1) và bước **sửa** trong B3 là **hai khâu riêng**; ta không "chấm bằng chính công cụ đã dùng để sửa một cách lén lút" — bước sửa chọn nút thật, còn bước chấm độc lập đối chiếu lại với VH.

---

## §4. METRIC — 5 thước đo (định nghĩa + công thức + ví dụ số + nguồn)

Ký hiệu: một tutorial có `n` bước. **"button-step"** = bước trỏ tới một nút/ô cụ thể (KHÔNG tính bước `fallback` mô-tả-bằng-lời, vì nó không khẳng định nút nào).

### 4.1. Lõi dùng chung — **Matcher ALOHa**  (`aloha_match.py`)
**Bài toán con:** làm sao biết *"tên model viết"* và *"tên nút thật"* có **cùng nghĩa** không? So chữ cứng thì hỏng: *"Configure"* và *"Settings"* khác chữ nhưng cùng nghĩa — nếu so cứng sẽ **oan** cho model là "bịa".

**Cách làm (3 bước):**
1. Biến mỗi chuỗi thành **vector ý nghĩa (embedding)** qua model `nomic-embed-text` (chạy local, miễn phí).
2. Tính **cosine similarity** (độ gần hướng của 2 vector, từ −1 đến 1) giữa *tên-model-viết* và **từng** nhãn thật trên màn; lấy nhãn **gần nhất**.
3. **Coi là khớp** nếu độ gần ≥ **ngưỡng τ = 0.55**.

**Vì sao τ = 0.55, và vì sao con số này "sạch"?**
- τ được **chốt TRƯỚC khi chạy** (pre-registered) → không phải dò tới khi ra kết quả đẹp.
- Kiểm chứng bằng **self-test** (in ra khi chạy `aloha_match.py`):
  - `Configure → Settings` sim = **0.605** → ≥0.55 → **khớp** ✓ (đúng: cùng nghĩa)
  - `Log out → Settings` sim = **0.391** → <0.55 → **không khớp** ✓ (đúng: khác nghĩa)
  - → ngưỡng tách đúng cặp-đồng-nghĩa khỏi cặp-khác-nghĩa.
- *Nguồn:* **ALOHa** (Petryk et al., NAACL 2024) — đề xuất đo hallucination **theo nghĩa** bằng so khớp ngữ-nghĩa, tốt hơn đếm-trùng-chữ kiểu CHAIR. *(Khi trích trong bài, kiểm lại chính xác venue/năm trước khi nộp.)*
- *Tối ưu kỹ thuật (KHÔNG đổi thuật toán/ngưỡng):* gọi embed **theo lô** + **cache ra đĩa** → nhanh ~9× (78 phút → ~8 phút lần đầu, tức thì lần sau). Giá trị số y hệt nên τ giữ nguyên — tối ưu này **không** ảnh hưởng kết quả khoa học.

---

### 4.2. Faithfulness — "không bịa"  *(thước đo chính #1)*
- **Đo gì:** tỉ lệ bước **KHÔNG** khẳng định-tự-tin một nút-ma.
- **Công thức:**
  ```
  faithfulness = 1 − (số button-step trỏ nút mà nút KHÔNG tồn tại) / n
  ```
- **Ví dụ số:** tutorial 4 bước; 1 bước nhắc nút "Cài đặt" không có trên màn → `faith = 1 − 1/4 = 0.75 = 75%`.
- **Quan hệ với design-E:** ở sysE, các bước nút-ma đã bị **sửa/fallback** nên gần như không còn → faith ~**100% là DO THIẾT KẾ** (đọc cảnh báo ở §7, đừng đọc là "phép màu").
- *Nguồn ý tưởng:* tỉ lệ hallucination (CHAIR/HER) + matcher ALOHa (§4.1).

### 4.3. Đúng-nhãn / Clarity — "gọi đúng tên hiển thị"  *(thước đo chính #2)*
- **Đo gì:** trong các button-step, % bước gọi nút bằng **đúng CHÍNH XÁC chữ hiển thị** (so chuỗi đã chuẩn-hoá, **không** chấp nhận đồng-nghĩa).
- **Công thức:**
  ```
  label_fidelity = (số button-step có tên TRÙNG-HỆT nhãn thật) / (số button-step)
  ```
- **Khác Faithfulness chỗ nào?** (câu hội đồng hay hỏi)
  - **Faithfulness** rộng lượng: *Configure* ≈ *Settings* vẫn tính **không-bịa** (đúng nghĩa là đủ an toàn).
  - **Đúng-nhãn** khắt khe: phải gọi **đúng chữ trên nút** thì người dùng mới bấm trúng → đo **độ-rõ-ràng-thực-dụng**.
  - → Vì khắt khe hơn, **mức tăng của Đúng-nhãn là cải thiện THẬT** của design-E (sửa về đúng tên), **không** phải hiệu ứng "có oracle thì dễ".
- **Ví dụ số:** model viết "nút **Lưu lại**" nhưng nút thật ghi "**Save**" → **không** tính đúng-nhãn (dù không bị tính bịa, vì 2 từ gần nghĩa).
- *Nguồn:* ánh xạ từ tiêu chí **Style/Clarity** trong khung đánh giá Chim/Ive/Liakata (Computational Linguistics 51(1), 2025).

### 4.4. Grounded-existence — "neo tồn tại"
- **Đo gì:** tỉ lệ bước trỏ tới nút **có thật** (theo matcher ALOHa), tính trên **toàn bộ** bước.
- **Công thức:** `grounded = (số button-step khớp nút thật) / n`.
- **Ghi chú trung thực:** ở BASE, số này **gần trùng** Faithfulness (cùng cơ sở "tồn tại"). Vì vậy luận văn **bổ sung ScreenSpot** làm đối chứng **point-in-bbox độc lập** (model xuất toạ độ, kiểm điểm có nằm trong khung nút thật) — việc còn lại trong §11.
- *Nguồn:* point-in-bbox grounding (SeeClick, ACL 2024).

### 4.5. Format — "đúng khuôn hướng dẫn"
- **Đo gì:** % bước **bắt đầu bằng động từ mệnh lệnh** (Bấm/Tap/Select/Enter/Nhập…).
- **Công thức:** `format = (số bước mở đầu bằng động từ hành động) / n`.
- **Kỳ vọng:** design-E **chỉ sửa tên nút**, **không đụng** cấu trúc câu → BASE và sysE **bằng nhau** (74.4% = 74.4%) là **đúng dự đoán**, không phải lỗi. Đây là một **kiểm-tra-độ-lành (sanity check)**: nếu format tự nhiên chênh nhau thì mới đáng nghi có bug.
- *Nguồn:* tinh thần **IFEval** (kiểm tuân-thủ-định-dạng bằng luật).

### 4.6. Coverage (proxy) — "có bỏ sót nút quan trọng không"
- **Đo gì:** số **nút thật khác nhau** được nhắc / số **nút bấm-được (actionable)** trên màn.
- **Công thức:** `coverage = |tập nút-thật-được-nhắc| / |nút actionable|`.
- **Vì sao gọi thẳng là "proxy" (tạm/đại diện)?** — và vì sao trị số **thấp** không phải là điểm yếu của hệ:
  - DG1 chỉ **1 màn** và **không có "đáp án vàng" liệt kê đúng những nút CẦN cho câu hỏi**. Nên ta lấy **"mọi nút actionable trên màn"** làm mẫu số.
  - Một câu hỏi thường chỉ cần **1–2 nút**, trong khi màn có thể có **chục nút** → coverage tự nhiên **thấp & nhiễu**, kể cả khi hướng dẫn **hoàn toàn đúng**.
  - → Vì vậy ta **công bố rõ là proxy**, **KHÔNG** đưa làm headline. Coverage "vàng" thật chỉ có ở **DG2/AndroidControl** (nơi có chuỗi thao tác chuẩn để biết đúng các nút cần).

---

## §5. THỐNG KÊ — vì sao con số đáng tin

### 5.1. Vì sao so theo CẶP (paired)
Mỗi màn được chấm **cả hai cách** (BASE và sysE) → tạo ra một **hiệu số** `(điểm sysE − điểm BASE)` cho **chính màn đó**. So theo cặp loại bỏ yếu-tố-màn-dễ-hay-khó (màn nào khó thì khó cho cả hai), nên **công bằng và nhạy hơn** so trung-bình-rời.

### 5.2. Bootstrap ghép-cặp (từng bước, có số)
1. Có **80 hiệu số** (mỗi màn 1 hiệu).
2. **Rút lại có hoàn lại** 80 hiệu → được một "thế giới song song" → tính trung bình của nó.
3. Lặp **2000 lần** → có 2000 trung bình.
4. Sắp xếp 2000 số đó, lấy **phân vị 2.5%** và **97.5%** → đó là **khoảng tin cậy 95% (CI)**.

### 5.3. Quy tắc đọc (đơn giản, dứt khoát)
- **CI không chứa 0** ⇒ cải thiện **có ý nghĩa thống kê** (rất khó do may rủi).
- **CI chứa 0** ⇒ chưa kết luận được — và theo nguyên tắc **"null vẫn đậu"**, vẫn báo cáo trung thực.
- Ví dụ kết quả thật: Faithfulness `+24.6pp [+16.2, +33.3]` — **cả khoảng nằm bên phải 0** ⇒ thắng chắc.

### 5.4. Pre-registration (chốt trước — lá chắn chống "chỉnh số")
Trước khi chạy, đã **chốt sẵn**: (i) giả thuyết ("design-E giảm bịa & tăng đúng-nhãn so BASE, có ý nghĩa"); (ii) ngưỡng matcher **τ = 0.55**; (iii) cách tính CI (bootstrap 2000, ghép-cặp); (iv) quy tắc quyết định (CI loại 0). → Giám khảo không thể vặn "anh dò tham số tới khi đẹp" vì mọi lựa chọn đã khoá **trước** khi thấy số.

---

## §6. VÍ DỤ CHẠY XUYÊN SUỐT 1 MÀN (để thấy số ra ở đâu)

> *Ví dụ minh hoạ theo đúng cơ chế hệ thống (số làm tròn cho dễ theo).*

**Màn:** app quản lý chi tiêu. **VH (oracle) liệt kê các nút thật:** `Add expense`, `Amount`, `Category`, `Save`, `Settings`, `Back`.

**Câu hỏi (B1):** *"Làm sao để thêm một khoản chi tiêu mới?"*

**BASE (B2) — model viết tự do, 4 bước:**
| # | verb | element model viết | Nút có thật? |
|---|---|---|---|
| 1 | Tap | **Add new** | ❌ không có (thật ra là "Add expense") |
| 2 | Enter | **Amount** | ✅ có |
| 3 | Select | **Category** | ✅ có |
| 4 | Tap | **Confirm** | ❌ không có (thật ra là "Save") |

→ **Chấm BASE:**
- Faithfulness = 1 − 2/4 = **50%** (2 bước trỏ nút-ma: "Add new", "Confirm").
- Đúng-nhãn: bước 1 ("Add new"≠"Add expense") sai, bước 4 ("Confirm"≠"Save") sai, bước 2,3 đúng → 2/4 = **50%**.

**design-E (B3) — lớp trung-thực-hoá soi từng bước:**
- Bước 1 "Add new" không khớp → model-sửa chọn nút thật gần nhất → **SỬA** thành **"Add expense"**.
- Bước 2 "Amount" khớp → giữ.
- Bước 3 "Category" khớp → giữ.
- Bước 4 "Confirm" không khớp → model-sửa chọn → **SỬA** thành **"Save"**.

→ **Chấm sysE:**
- Faithfulness = 1 − 0/4 = **100%** (không còn nút-ma).
- Đúng-nhãn = 4/4 = **100%** (cả 4 bước gọi đúng tên thật).

**Đọc ví dụ:**
- Faithfulness nhảy 50% → 100% phần lớn **do thiết kế** (hệ chặn nút-ma). Cái **giá-trị-đo-được** là: BASE đã bịa **2/4 bước** — đó là rủi ro thật mà design-E loại bỏ.
- Đúng-nhãn nhảy 50% → 100% là **cải thiện thật**: hệ **sửa "Add new"→"Add expense"**, **"Confirm"→"Save"** đúng tên trên màn, giúp người dùng bấm trúng. Đây mới là phần "công" thật của hệ.

> Nhân ví dụ này lên **80 màn** + bootstrap → ra bảng §7.

---

## §7. KẾT QUẢ THẬT (80 màn, model sinh = gpt-4o-mini, chạy 2026-06-27)

| Thước đo | BASE (tự do) | design-E | Chênh [95% CI bootstrap] |
|---|---|---|---|
| **Faithfulness (không bịa)** | 75.4% | **100.0%** | **+24.6pp [+16.2, +33.3]** |
| **Đúng-nhãn / Clarity** | 67.9% | **89.8%** | **+21.9pp [+14.8, +30.0]** |
| Grounded-existence | 75.4% | 97.3% | — |
| Format | 74.4% | 74.4% | (design-E không đụng format) |
| Coverage (proxy) | 28.8% | 34.6% | (proxy yếu — khai báo limitation) |

**Hoạt động của design-E:** đã **SỬA 24 bước** lệch-tên về nút THẬT + **FALLBACK 4 bước** sang mô-tả-bằng-lời. (n=80 màn, paired bootstrap 2000.)

### Đọc kết quả cho ĐÚNG (đoạn quan trọng nhất khi bảo vệ)
1. **Hai thước đo chính có CI loại 0** ⇒ cải thiện **có ý nghĩa thống kê**, không phải may rủi.
2. **Faithfulness ~100% là DO THIẾT KẾ** — đừng đọc là "phép màu". Hệ đã *chặn* mọi bước trỏ nút-ma. Nên **giá trị thật đo được** gồm 2 phần:
   - **(a)** BASE tự do **bịa ~24.6%** số bước → đây chính là **rủi ro mà design-E loại bỏ** (đo được, đáng kể);
   - **(b)** **Đúng-nhãn +21.9pp là cải thiện THẬT** (sửa về đúng tên nút hiển thị) — phần này **không** phải hiệu ứng "có oracle".
3. → Khớp đúng claim **"mức-chắc-thắng"**: hệ **giảm bịa & tăng đúng-chỗ** so với chính model viết tự do. **KHÔNG** claim SOTA.
4. **Coverage thấp** (§4.6): proxy, để làm limitation — **không** phải hệ kém.
5. **Grounded ≈ Faithfulness ở BASE**: trùng cơ sở "tồn tại" → cần ScreenSpot độc lập (§11).
6. **Format đứng yên**: đúng kỳ vọng (design-E không sửa câu) → là sanity-check, không phải bug.

---

## §8. HỘI ĐỒNG KHÓ TÍNH SẼ HỎI GÌ — trả lời sẵn ⭐

> Đây là phần để **mở ra đọc khi bảo vệ**. Mỗi câu = một nghi ngờ điển hình + câu trả lời đã chuẩn bị + bằng chứng trỏ tới mục nào trong file.

**H1. "Có oracle rồi thì 'không bịa' là hiển nhiên — đóng góp tầm thường?"**
→ **Thừa nhận một nửa, và đã chủ động khai (§7):** con số ~100% là **do thiết kế**. Nhưng đóng góp **không** nằm ở con số 100%, mà ở: (a) **đo được BASE bịa 24.6%** = rủi ro thật được loại; (b) **Đúng-nhãn +21.9pp là cải thiện thật**; (c) **bản thân CÁCH ĐÁNH GIÁ** (5 thước đo neo-silver khi không có gold) **là đóng góp (B)**, độc lập với việc oracle dễ hay khó. Ta **không** claim "né nút-ma là phát minh".

**H2. "Metric tự động có khớp với người chấm không?" (câu nặng ký nhất cho một bài về ĐÁNH GIÁ)**
→ Cần **Track B**: người chấm tay ~**40 cặp A/B ẩn-danh** rồi đo tương quan auto-vs-người (+ độ rộng CI). **Đã dựng sẵn `harness/trackB.html`, CHƯA chấm** → đây là việc **bắt buộc còn lại** (§11). Tôi **không** tuyên bố DG1 đã xong khi chưa có phần này.

**H3. "Câu hỏi do máy tự soạn — có thiên vị để hệ dễ thắng không?"**
→ Có **protocol công khai (§B1):** 1 câu/màn, nội dung phải làm-được-ngay-trên-màn, sinh tự động hàng loạt rồi người duyệt loại câu vô lý, công bố số lượng (80). Quan trọng: **BASE và design-E nhận CÙNG câu hỏi** → câu hỏi không thể thiên vị riêng cho design-E.

**H4. "design-E thắng vì baseline bị làm yếu phải không?"**
→ **Không.** Baseline BASE **đã được prompt tử tế** ("gọi đúng chữ trên màn, đừng bịa" — §B2). design-E thắng nhờ **cơ chế kiểm-tra-và-sửa**, không nhờ dìm đối chứng. Đây là so sánh **cùng model, cùng câu hỏi, cùng oracle chấm** — chỉ khác có/không lớp trung-thực-hoá.

**H5. "Hệ chỉ chạy với 1 model thì sao gọi là 'phương pháp độc-lập-model'?"**
→ Đúng, claim model-agnostic cần **model thứ 2**. Hiện vướng **hạ tầng**: máy **không có GPU** → VLM local (Qwen-VL) **>5 phút/ảnh, không chạy nổi** ở quy mô 80 màn (§10). Nên model thứ 2 **bắt buộc dùng API cloud** (gpt-4o ~$0.20/40 màn) **hoặc** hạ H2 xuống future-work. ← Đây là **quyết định đang chờ**, đã nêu thẳng, không lấp liếm.

**H6. "Grounded-existence gần trùng Faithfulness — đo 2 lần 1 thứ?"**
→ Đã khai là **limitation #4 (§4.4):** ở BASE chúng trùng cơ sở "tồn tại". Hướng vá: **ScreenSpot point-in-bbox độc lập** (kiểm toạ độ nằm trong khung nút), tách bạch "tồn-tại-theo-tên" với "trúng-vị-trí-pixel".

**H7. "Vì sao dùng llama3.2 để SỬA mà không để chính gpt-4o-mini tự sửa?"**
→ Cố ý: (a) **chống tự-bao-che** (model tự sửa lỗi của mình dễ thiên vị); (b) cho thấy bước-sửa là **module độc lập, thay được** — đúng tinh thần "lớp độc-lập-model". Bước **chấm** lại độc lập với bước **sửa**, nên không có vòng tự-chấm.

**H8. "Coverage thấp (28–34%) — hướng dẫn bỏ sót nhiều?"**
→ **Không.** Đã giải thích (§4.6): đây là **proxy**, mẫu số là "mọi nút trên màn" trong khi 1 câu hỏi chỉ cần 1–2 nút → thấp là **đương nhiên kể cả khi đúng hoàn toàn**. Coverage thật cần gold-steps, chỉ có ở DG2. Vì vậy nó **không phải headline**.

**H9. "n=80 có đủ không?"**
→ Với **hiệu ứng lớn** (24.6pp, 21.9pp) và **bootstrap ghép-cặp**, **CI loại 0 rõ ràng** (không sát mép 0). 80 màn đủ cho **kết luận có-ý-nghĩa** ở mức hiệu ứng này; Track B + ScreenSpot sẽ củng cố thêm độ tin.

**H10. "Sao không so với GPT-4o end-to-end (model mạnh viết thẳng)?"**
→ Có trong kế hoạch như **baseline mạnh**; claim "mức-thưởng" (bonus) là thắng cả GPT-4o E2E về độ-bám-ảnh. Hiện đã chứng minh "mức-chắc-thắng" (vs chính model viết tự do); so GPT-4o E2E là bước mở rộng tốn thêm chi phí API.

---

## §9. GIỚI HẠN & mối đe doạ tính hợp lệ (khai trước, không giấu)

| # | Giới hạn | Đã/đang xử lý thế nào |
|---|---|---|
| L1 | **Faithfulness ~100% do thiết kế**, không phản ánh "độ thông minh". | Báo cáo tách bạch: phần do-thiết-kế vs phần cải-thiện-thật (Đúng-nhãn). |
| L2 | **Chưa có Track B** (đối chiếu người) — yếu chí mạng cho bài về đánh giá. | Đã dựng công cụ; chấm là việc còn lại bắt buộc. |
| L3 | **Mới 1 model sinh** (gpt-4o-mini). | Thêm model thứ 2 qua API hoặc hạ thành future-work (do không-GPU). |
| L4 | **Grounded ≈ Faithfulness** (đo gần trùng). | Bổ sung ScreenSpot point-in-bbox độc lập. |
| L5 | **Coverage là proxy** (không gold-steps ở 1-màn). | Công bố rõ là proxy; coverage thật để ở DG2. |
| L6 | **Câu hỏi do máy soạn** (có người duyệt). | Protocol công khai + người duyệt; cùng câu hỏi cho cả 2 nhánh. |
| L7 | **Dữ liệu nhãn tiếng Anh** (MobileViews), tiếng Việt chưa định lượng. | Demo định tính tiếng Việt (`questions_vi.json`); pipeline vốn ngôn-ngữ-độc-lập (chấm bằng tên/toạ độ). |
| L8 | **Oracle/VH cũng có thể thiếu element** (a11y tree không hoàn hảo). | Khung kết quả "có điều kiện theo độ-phủ-oracle"; sẽ đo recall như một caveat. |

---

## §10. Chi phí & môi trường (vì sao chọn cách chạy này)

- **Model sinh = gpt-4o-mini** (cloud OpenAI): rẻ ~**$0.0005/ảnh** → cả 80 màn ≈ **$0.05**. Nhanh vì chạy trên cloud.
- **Bước SỬA = llama3.2** + **matcher = nomic-embed-text** → chạy **local, miễn phí**.
- **🔴 Bài học hạ tầng (quan trọng cho mọi quyết định tiếp theo):** máy **không có GPU NVIDIA** ⇒ model **nhìn-ảnh** chạy local (Qwen-VL) **cực chậm**: 1 ảnh **>5 phút vẫn chưa xong** (một lần thử timeout ở 300 giây) ⇒ **không dùng được** ở quy mô 80 màn. Vì vậy **phần sinh-từ-ảnh BẮT BUỘC dùng API cloud**; chỉ phần **text + embedding** mới chạy local được. → Đây là lý do model thứ 2 (H5) cũng phải là API cloud.
- **Chống rate-limit (429):** đã thêm `_http.py` retry + backoff + nghỉ 0.6s/lần gọi → chạy 80 màn ổn định.

---

## §11. Đã làm xong / Còn lại

**✅ Đã xong:**
- 80 câu hỏi use-case (sinh + lưu `dg1_cache/questions.json`, chờ duyệt tay cuối).
- 80 màn chạy đủ **BASE + design-E**.
- Chấm **5 thước đo + CI bootstrap** → bảng §7.
- Hạ tầng kỹ thuật: chống rate-limit (retry/backoff), tăng tốc matcher (batch + cache đĩa ~9×).
- **Track B dựng sẵn** (`harness/trackB.html`, 40 màn A/B ẩn-danh chờ người chấm).

**⏳ Còn lại để khép DG1 (theo thứ tự ưu tiên thuyết phục):**
1. **Track B** — mở `trackB.html`, chấm so-đôi 40 cặp → đo "metric tự động khớp người tới đâu". *(Quan trọng nhất — H2.)*
2. **Model thứ 2** cho claim độc-lập-model — API cloud (gpt-4o ~$0.20/40 màn) hoặc hạ future-work. *(H5 — đang chờ quyết.)*
3. **ScreenSpot** — đối chứng grounding point-in-bbox độc lập. *(H6.)*
4. **Demo định tính tiếng Việt** (`questions_vi.json`).

---

## §12. Bản đồ file code (ai muốn xem sâu)

| File | Vai trò |
|---|---|
| `harness/dg1_questions.py` | **B1** — sinh câu hỏi use-case từ ảnh (qua VLM cloud) |
| `harness/dg1_run.py` | **B2 + B3** — sinh BASE rồi áp lớp design-E (oracle → sửa → fallback) |
| `harness/aloha_match.py` | **Matcher ALOHa** (embedding `nomic-embed-text` + cosine, τ=0.55) + cache đĩa |
| `harness/dg1_score_all.py` | **B4** — chấm 5 thước đo + bootstrap CI, gộp bảng |
| `harness/dg1_scorer.py` | bản chấm có thêm grounding point-in-bbox (đọc VH; xử lý "bẫy dữ liệu" MobileViews: kích thước ảnh thật, bbox lồng `[[l,t],[r,b]]`) |
| `harness/trackB_html.py` | dựng trang Track B cho người chấm so-đôi A/B ẩn-danh |
| `harness/_http.py` | gọi API có retry/backoff (chống 429 rate-limit) |
| `harness/_apikey.py` | đọc khoá API từ `harness/.openai_key` (KHÔNG in ra) |
| `harness/dg1_cache/` | câu hỏi + các run + cache embedding (`emb_cache.json`) |

---

## §13. MỘT DÒNG TÓM

**DG1 = đo lớp "kiểm-trung-thực" design-E trên hướng dẫn 1-màn:** model sinh hướng dẫn gọi-nút-theo-tên (chỉ thấy ảnh+câu hỏi, KHÔNG thấy oracle) → oracle (VH) kiểm nút có thật → **sửa bằng model khác** / **mô tả-bằng-lời** nếu không có → chấm **5 thước đo** (không-bịa, đúng-nhãn, grounded, format, coverage) bằng matcher ALOHa (τ=0.55, chốt-trước). Chạy thật **80 màn (gpt-4o-mini, ~$0.05): GIẢM BỊA +24.6pp & TĂNG ĐÚNG-NHÃN +21.9pp, CI bootstrap loại 0** — đúng claim "mức-chắc-thắng". **Faithfulness ~100% là do-thiết-kế** (đọc trung thực §7); **coverage là proxy** (limitation §4.6). **Hai đóng góp ngang nhau:** (A) hệ tốt + (B) cách đánh giá khi không có gold. **Còn lại:** Track B người-chấm + model thứ 2 + ScreenSpot độc lập.
