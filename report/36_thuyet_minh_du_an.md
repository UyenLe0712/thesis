# THUYẾT MINH DỰ ÁN
## Sinh và đánh giá hướng dẫn sử dụng phần mềm từ ảnh giao diện, khi không có đáp án mẫu

> **Cấu trúc:** (1) tổng quan cho người mới; (2) pipeline một màn; (3) đánh giá một màn; (4) đánh giá đa màn; (5) nguồn các thước đo; (6) đóng góp; (7) giới hạn; (phụ lục) câu hỏi giám khảo hay hỏi. Hai ví dụ được dùng xuyên suốt.

> **Định vị đóng góp — HAI đóng góp NGANG NHAU.**
> - **(A) HỆ THỐNG sinh hướng dẫn bám sát màn:** một lớp hậu kiểm (đối chiếu danh sách nút thật, bước bịa thì viết lại thành mô tả bằng lời, không đoán nút khác) đảm bảo đầu ra không trỏ tới nút không tồn tại; cộng một khối sắp thứ tự màn cho đầu vào nhiều ảnh. Gắn được vào bất kỳ mô hình nào.
> - **(B) PHƯƠNG PHÁP ĐÁNH GIÁ khi không có đáp án mẫu:** đo độ trung thực không cần đáp án vàng mà không tự chấm (một màn), và đo năng lực suy luận thứ tự + mức làm tới đích trên dữ liệu có đáp án vàng (đa màn).

---

# PHẦN 1 — TỔNG QUAN CHO NGƯỜI MỚI BẮT ĐẦU

## 1.1. Bài toán bằng ngôn ngữ đời thường
Bạn mở một ứng dụng lạ và không biết bấm vào đâu. Bạn chụp màn hình, rồi hỏi *"làm sao thêm một khoản chi mới?"*. Chúng tôi muốn một trợ lý AI **nhìn ảnh màn hình cộng câu hỏi, rồi viết hướng dẫn bấm từng bước**. Loại AI làm được việc này gọi là **mô hình đa phương thức (VLM)** — vừa "nhìn" ảnh, vừa "đọc" chữ.

## 1.2. Vấn đề: hiện tượng "ảo giác"
VLM có một tật: đôi khi nó **tự tin nhắc đến một nút không có trên màn**. Giống một người bạn liếc qua điện thoại của bạn rồi bảo "bấm nút Gửi đi", trong khi chẳng có nút nào tên "Gửi". Bạn tìm mãi không thấy. Hiện tượng này gọi là **"ảo giác" (hallucination)**. Khó khăn thứ hai: **không ai soạn sẵn bản hướng dẫn chuẩn** cho mọi ứng dụng, nên không có gì để đối chiếu mà chấm điểm.

## 1.3. Ví dụ chạy xuyên suốt (một màn)
**Màn hình** một app ghi chi tiêu, có đúng 6 nút thật: `Add expense · Amount · Category · Save · Settings · Back`.
**Câu hỏi:** *"Làm sao thêm một khoản chi mới?"* (câu hỏi diễn đạt theo ý muốn, không chứa tên nút).

AI viết ra bản hướng dẫn gốc:

| Bước | AI viết | Có thật? |
|---|---|---|
| 1 | Bấm **Add expense** | Có |
| 2 | Nhập số tiền vào ô **Amount** | Có |
| 3 | Bấm **Submit** | **KHÔNG có** → nút bịa |
| 4 | Bấm **Save changes** | Nút thật tên "Save"; AI gọi lệch |

> **⚠️ Điểm dễ hiểu nhầm nhất — đọc kỹ:** AI viết 4 bước này khi **CHƯA hề thấy danh sách 6 nút thật**. Nó tự đọc ảnh mà đoán tên nút (nên mới bịa "Submit"). Danh sách nút chỉ được dùng ở **bước đối chiếu sau đó**, và cái đối chiếu là một **thuật toán**, không phải AI. (Vì sao phải làm vậy: mục 2.3.)

Hệ thống phát hiện bước 3 trỏ nút không tồn tại, rồi **viết lại** thành *"Tìm và bấm nút để lưu khoản chi vừa nhập"* (đổi lại bước đó kém cụ thể hơn — cái giá này được đo và báo, khoảng 1/4 số bước). Ba bước còn lại giữ nguyên.

---

# PHẦN 2 — PIPELINE MỘT MÀN (DG1)

## 2.1. "Danh sách nút thật"
Mỗi màn Android đi kèm một bản kê khai do hệ điều hành cấp, liệt kê mọi nút cùng tên và khung toạ độ. Thuật ngữ kỹ thuật là *View Hierarchy* (hay *accessibility tree*); trong tài liệu này gọi là **"danh sách nút thật"**.

## 2.2. Ba hộp — ai thấy gì, làm gì
Hình dung hệ thống là dây chuyền ba hộp nối tiếp. Cột quan trọng nhất là **"thấy danh sách nút thật?"**: chỉ một hộp được thấy, và hộp đó **không phải AI**.

| Hộp | Ai làm | Nhận gì | Thấy danh sách nút? | Làm gì |
|---|---|---|---|---|
| **1 — SINH** | VLM | ảnh + câu hỏi | **KHÔNG** | Viết hướng dẫn, gọi nút theo tên. Viết **một lần, mù**, rồi thôi. |
| **2 — ĐỐI CHIẾU** | **Thuật toán so-nghĩa** (không phải AI) | bản gốc + danh sách nút thật | **CÓ** (duy nhất) | Từng tên nút → dò có nút thật nào cùng nghĩa không. Khớp = hợp lệ; không khớp = bịa. |
| **3 — HẬU KIỂM** | Quy tắc viết lại | các bước bị gắn cờ "bịa" | Không cần | Xoá tên nút bịa, thay bằng **mô tả chức năng bằng lời**. Bước hợp lệ giữ nguyên. |

Hộp 2 là chỗ dễ nhầm: cái đối chiếu **không phải một AI khác đọc hiểu**, mà là phép so **bằng con số**. Mỗi tên nút được quy về một dãy số (*vector nghĩa* / embedding); hai tên gần nghĩa thì hai dãy gần nhau; vượt một ngưỡng cố định thì coi là "khớp". Nhờ so theo **nghĩa**, "Save changes" vẫn khớp nút thật "Save" (không tính oan là bịa); còn "Submit" không gần nghĩa nút nào → bị gắn cờ bịa.

## 2.3. Vì sao TUYỆT ĐỐI không cho AI thấy danh sách nút lúc sinh
Mục tiêu là **đo xem AI bịa nhiều hay ít**. Muốn đo, tình huống bịa phải có cơ hội xảy ra.
- Nếu đưa sẵn 6 nút cho AI ở Hộp 1, nó chỉ việc **chép lại** → không bao giờ bịa → con số "tỉ lệ bịa = 0%" là **giả**. Giống đo trí nhớ học sinh nhưng để mở tờ đáp án trên bàn.
- Câu hỏi đầu vào cũng giữ không chứa tên nút, để bịt đường rò rỉ gián tiếp.

**Giấu danh sách nút khỏi lúc sinh chính là điều kiện để phép đo có ý nghĩa.**

## 2.4. Vì sao Hộp 3 chỉ "mô tả bằng lời", không đoán một nút khác
Phản xạ tự nhiên: sao không sửa "Submit" thành nút gần nhất "Save"? Chúng tôi đã thử và **đo được** phương án này gây **lỗi ngầm**: hệ đổi "Submit" thành "Save" trong khi thao tác đúng là một nút khác → người dùng bấm nhầm mà không biết, còn nguy hơn để nguyên. Vì có bằng chứng thực nghiệm rằng "đoán nút khác" gây hại, ta chọn phương án an toàn: **chỉ mô tả việc cần làm**. Cái giá (bước kém cụ thể hơn) được đo và báo minh bạch.

---

# PHẦN 3 — ĐÁNH GIÁ MỘT MÀN (DG1)

## 3.1. Nền tảng: bộ khớp theo nghĩa và ngưỡng τ
Mỗi tên nút được quy về vector nghĩa; độ gần đo bằng cosine (`cos(u,v)` từ −1 đến 1); vượt ngưỡng τ thì coi là khớp. Ba điều để chống bắt bẻ:
- **Không so chữ cứng:** "Save changes" khác "Save" về ký tự nhưng cùng nghĩa; so chữ sẽ tính oan là bịa (theo ALOHa, NAACL 2024).
- **Ngưỡng τ không chọn bằng mắt:** hiệu chỉnh trên 80–120 cặp gán nhãn tay, chọn theo **precision ≥ 0.95** (thà bỏ sót còn hơn tính oan không-bịa), và **đóng băng trước khi chạy chính** — không tinh chỉnh sau khi thấy kết quả. Báo cả precision lẫn recall; mọi số đóng khung "có điều kiện recall đã đo".
- **Bộ chấm gồm ba cơ chế khác nhau** (mục 3.3), không chỉ một embedding.

## 3.2. Các thước đo — công thức, ví dụ 1 điểm / 0 điểm
Chấm ở cấp từng bước; "1 điểm" = bước đạt, "0 điểm" = không đạt.

**Thước đo 1 — Độ trung thực (không bịa).** `Trung thực = 1 − (bước nhắc nút không tồn tại)/(bước có nhắc tên nút)`.
- 1 điểm: "Bấm **Save**" — có nút Save. · 0 điểm: "Bấm **Submit**" — không có.
- *Ví dụ:* bản gốc 1 bịa/4 → `75%`. *(Nguồn cơ chế: ALOHa, NAACL 2024.)*

**Thước đo 2 — Độ đúng nhãn (gọi đúng tên).** `= (bước gọi đúng tên)/(bước trỏ nút có thật)`.
- 1 điểm: nút thật "Save", AI viết "Save". · 0 điểm: AI viết "Save changes" (nút có thật nên **không** tính bịa, nhưng sai tên).
- *Ví dụ:* 2/3 ≈ `67%`. *(Đây là thước đo **tự định nghĩa** — khớp chuỗi chính xác, không từ một bài báo cụ thể; dùng làm kiểm-tra-phụ "không làm hỏng", không overclaim.)*

**Thước đo 3 — Độ đúng chỗ (grounding).** Nếu có toạ độ bấm, kiểm điểm đó rơi trong khung nút. Trúng nếu `l≤x≤r` và `t≤y≤b`. *(Cập nhật 2026-07-02: thước đo này **để dành cho nhánh nhiều màn** — nơi có toạ độ vàng — hoặc đối chứng trên ScreenSpot-v2; **KHÔNG tính vào headline một-màn** vì nếu lấy tâm khung nút đã khớp làm điểm bấm thì luôn "trúng" = vô nghĩa. Muốn đo thật cần một bộ trỏ ĐỘC LẬP đoán toạ độ từ tên+ảnh.)*
- 1 điểm: khung Save `[100,850,200,900]`, bấm `(120,880)` → trong khung. · 0 điểm: bấm `(240,880)` → ngoài.
- *(Nguồn: SeeClick/ScreenSpot, ACL 2024.)* Báo kèm tỉ lệ bước có toạ độ; phần không có toạ độ ghi "không đo được".

Sau hậu kiểm: bước 3 thành mô tả → không còn nút bịa; **tỉ lệ bước phải mô tả khái quát = 25%** (cái giá).

## 3.3. Chống vòng lặp luận (điểm mấu chốt)
**Bẫy:** nếu cùng một công cụ vừa *quyết* "bước nào bịa để viết lại" vừa *chấm* "còn bịa không", thì điểm sau hậu kiểm là 100% — một đẳng thức, không phải kết quả.
**Xử lý ba lớp:**
1. **Tách công cụ quyết ≠ công cụ chấm, ba cơ chế khác nhau.** *Quyết* dùng embedding A (nomic-embed). *Chấm* dùng embedding B **họ khác** (BGE-M3) **+ một bộ chấm LLM nhị phân** (được nạp danh sách nút, phán "tên này có trong danh sách không") **+ so trùng từ**. Ba cơ chế lỗi khác nhau → sự đồng thuận không còn hiển nhiên (nếu chỉ hai embedding cùng họ, chúng sai giống nhau).
2. **Con số headline là tỉ lệ bịa của bản gốc, không phải 100%.** Vì bộ chấm độc lập với bộ quyết, độ trung thực sau hậu kiểm **không ghim 100%** — chạy thử cho khoảng **95%**; chính khe hở giữa hai bộ là bằng chứng không tautology. **Con số báo cáo chính = tỉ lệ bịa của bản gốc** (đo độ lớn vấn đề) + % fallback (cái giá).
3. **Giới hạn phạm vi claim.** Trên một màn chỉ khẳng định *giảm tham chiếu nút không tồn tại*, **không** khẳng định *đúng ý* hơn — việc đó cần đáp án vàng, thuộc nhánh đa màn.

Về rò rỉ dữ liệu: danh sách nút và câu hỏi đều không mang tên nút vào lúc sinh (mục 2.3). Nếu danh sách nút thiếu một nút mà AI gọi đúng, ta sẽ tính oan là bịa. Danh sách nút của MobileViews **cũng có thể thiếu nút** (nút chỉ có icon, không nhãn chữ — Chen et al., ICSE 2020 đo hơn 77% app có nút thiếu nhãn), nên ta **KHÔNG coi nó là chân lý hoàn hảo**: ta **đo tỉ lệ nút có nhãn dùng được (độ-phủ-nhãn)**, **loại các nút nhãn chung khỏi mẫu số**, và báo tỉ lệ bịa dưới dạng **"có điều kiện độ-phủ-nhãn VH"**. Khi triển khai từ một ảnh thật thì cần bộ dò và mọi số cũng đóng khung "có điều kiện recall".

## 3.4. Kiểm chính thước đo (perturbation test)
Ta kiểm *bản thân thước đo có đáng tin không* mà không cần chấm người: **cố ý bơm lỗi đã biết** vào một hướng dẫn đúng rồi xem thước đo phản ứng đúng không.

| Lỗi bơm vào | Kỳ vọng | Kiểm |
|---|---|---|
| Chèn nút rõ ràng không có ("Export to PDF") | Trung thực **giảm** | bắt được bịa |
| Đổi nút → đồng nghĩa ("Save"→"Lưu") | Trung thực **giữ**, Đúng nhãn **giảm** | tách đúng hai lỗi |
| Đổi nút thật → nút thật khác đúng tên | **Không** thước đo nào báo lỗi | không vu oan |

Đo được **tỉ lệ phát hiện** và **tỉ lệ báo nhầm** một cách khách quan. **Giới hạn nói thẳng:** phép này chứng minh thước đo *nhạy* với lỗi, **chưa** chứng minh bám phán đoán người; ta bổ sung một mẫu chuyên gia nhỏ đăng ký trước, đặc biệt báo đường cong ở vùng gần đồng nghĩa (Confirm/Save) — nơi bộ khớp dễ bắt hụt nhất. *(Cách kiểm metric bằng lỗi tiêm có tiền lệ: Sai et al., EMNLP 2021.)*

---

# PHẦN 4 — ĐÁNH GIÁ ĐA MÀN (DG2)

## 4.1. DG2 KHÔNG phải hệ thống thứ hai
Vẫn **một hệ duy nhất**. Khi chỉ có 1 ảnh, khối sắp thứ tự rỗng và ta về đúng Phần 2. Khi có N ảnh, khối này bật lên trước pha sinh. Một bộ định tuyến chọn chế độ theo số ảnh.

> **Cách nhớ: DG2 = STAGE-0 (sắp thứ tự) + DG1 (nguyên vẹn).**

## 4.2. Vì sao cần nhánh này
- **Về bài toán:** người dùng đôi khi đưa cả một xấp ảnh của quy trình nhiều màn, không đúng thứ tự; muốn hướng dẫn đúng, phải biết màn nào trước.
- **Về phép đo:** DG1 chỉ đo *không bịa*, chưa đo *đúng ý*. DG2 lấp chỗ đó bằng **AndroidControl** (bình duyệt tại NeurIPS 2024) — mỗi luồng có sẵn **thứ tự đúng** và **thao tác đúng từng bước**. Có đáp án vàng thì mới chấm được *có sắp đúng thứ tự* và *có làm tới đích* — hai thứ DG1 không với tới.

## 4.3. DG2 kế thừa gì, thêm gì

| | DG1 (một màn) | DG2 (nhiều màn) |
|---|---|---|
| AI sinh mù (không thấy danh sách nút) | Có | **Kế thừa nguyên** |
| Thuật toán đối chiếu danh sách nút | Có | **Kế thừa nguyên** |
| Viết lại bước bịa thành mô tả | Có | **Kế thừa nguyên** |
| Chấm trung thực / đúng nhãn / đúng chỗ | Có | **Kế thừa**, chấm cho **từng màn** |
| **Khối STAGE-0: sắp thứ tự N ảnh** | — | **THÊM MỚI** |
| **Thước đo τ (xếp đúng thứ tự)** | — | **THÊM MỚI** (nhờ có gold) |
| **Thước đo Step-SR (làm tới đích)** | — | **THÊM MỚI** (nhờ có gold) |

## 4.4. Sơ đồ luồng DG2
```
[ N ảnh ĐÃ XÁO + mục tiêu ]
        │
   STAGE-0 (THÊM MỚI)
     (a) hỏi AI từng CẶP: "màn nào đứng trước?"
     (b) Copeland: đếm 'trận thắng' → xếp từ nhiều đến ít
     (c) vòng mâu thuẫn → bỏ cặp AI ít chắc chắn nhất
     ▸ AI chỉ thấy ảnh (che đồng hồ/pin/badge) + mục tiêu; gold KHÔNG có ở đây
        │  → chuỗi màn ĐÃ SẮP
   PIPELINE DG1 (KẾ THỪA NGUYÊN, chạy trên TỪNG màn)
     sinh mù → đối chiếu nút → viết lại bước bịa
        │
   CHẤM: (DG1) trung thực/đúng nhãn/đúng chỗ  +  (mới) τ, Step-SR
```
Nhất quán với DG1: **gold và danh sách nút chỉ ở khâu chấm, không ở khâu sắp thứ tự hay sinh.** Che đồng hồ/pin/badge để AI không "đọc lén" dấu vết thời gian mà đoán thứ tự.

## 4.5. Ví dụ khối sắp thứ tự (Copeland)
Luồng 3 màn, đáp án vàng: **A = Đăng nhập → B = Trang chủ → C = Hồ sơ.** Đưa 3 ảnh **đã xáo** + mục tiêu.

Hỏi từng cặp: A trước B (đăng nhập rồi mới vào trang chủ) · A trước C · B trước C. Đếm trận thắng: A=2, B=1, C=0 → xếp **A → B → C**, trùng vàng.
Nếu AI lỡ trả lời tạo vòng (A→B, B→C, **C→A**): khối **bỏ cặp AI ít chắc chắn nhất** để cắt vòng. *(Vì sao hỏi từng cặp thay vì bắt AI phun cả dãy: pairwise ổn định hơn; chi phí C(N,2) call/luồng, N=6 → 15 call, nên chốt trần N≤6.)*
Chuỗi `A→B→C` đi thẳng vào pipeline DG1.

## 4.6. Hai thước đo THÊM MỚI (chỉ bật được vì có gold)

**Thước đo 4 — Xếp đúng thứ tự (τ thứ-tự-bộ-phận).**
- *τ (đọc là "tau") là hệ số tương quan thứ hạng Kendall — đo hai danh sách xếp giống nhau tới đâu, từ −1 (đảo ngược hoàn toàn) đến +1 (khớp hoàn toàn), 0 = như ngẫu nhiên.*
- `τ = (C − D) / |M|`, `M` = tập **cặp bắt buộc**, `C` cặp thuận, `D` cặp nghịch.
- 1 điểm: "Đăng nhập trước Hồ sơ", hệ xếp đúng chiều. · 0 điểm: hệ xếp "Hồ sơ trước Đăng nhập".
- *Ví dụ:* vàng A<B<C, hệ sắp A,C,B → (2−1)/3 = **+0.33**.
- **Chỉ phạt cặp bắt buộc:** cặp tự do (điền email/sđt trước-sau đều được) đảo vẫn đúng.
- *Vì sao dùng τ, không dùng khớp-thứ-tự-tuyệt-đối:* khớp tuyệt đối với N=3 đã ~17% đúng do ngẫu nhiên, vô nghĩa; τ đo mức-độ-giống nên có nội dung. *(Nguồn: Kendall 1938; tiền lệ NLP: Lapata, CL 2006; partial-order: Fagin et al. 2003/2006.)*

**Thước đo 5 — Làm-theo-tới-đích (Step-SR).**
- `Step-SR = (bước làm đúng)/(bước của đáp án vàng)`; đúng = đúng loại thao tác **và** bấm cách toạ độ vàng ≤ **14% kích thước màn** (hoặc cùng khung nút). *(Ngưỡng 14% lấy từ benchmark AITW, Rawles et al., NeurIPS 2023.)*
- 1 điểm: vàng "bấm Login tại (cx,cy)", hệ "bấm Login" → đúng loại + trong 14%. · 0 điểm: "bấm Settings" (sai đối tượng) hoặc lệch >14%.
- **Đây là thứ DG1 không đo được:** một hướng dẫn có thể **không bịa nút nào mà vẫn sai việc** (bấm nút có thật nhưng nhầm chức năng); chỉ khi có thao tác vàng mới bắt được. Đó là lý do DG2 mới chứng minh được *đúng ý*.
- **Step-SR là cận dưới (lower bound):** so với *một* quỹ đạo vàng, một hướng dẫn đúng đi đường khác vẫn bị tính sai. *(Nguồn bộ metric: AndroidControl, NeurIPS 2024.)*

## 4.7. Chống vòng lặp luận ở DG2
Nhãn "cặp bắt buộc" **suy từ đáp án vàng** bằng quy tắc nhân-quả (màn B chỉ hiện sau thao tác vàng ở A ⇒ (A trước B) bắt buộc), **không** lấy từ mô hình đang chấm, và **tuyệt đối không suy từ bộ phát-hiện-cue** (gating/drill-down) mà model dùng khi sắp — để tránh model vừa xếp vừa tự định nghĩa mình đúng. Quy tắc là *xấp xỉ* → kiểm bằng audit người 50–80 cặp + đo độ nhạy khi gán nhãn sai 10%.

---

# PHẦN 5 — NGUỒN CÁC THƯỚC ĐO (để trả lời khi thầy hỏi "metric ở đâu ra")

| Thước đo | Nguồn (đã kiểm) | Bình duyệt? |
|---|---|---|
| Trung thực / hallucination (khớp + Hungarian) | **ALOHa** — Petryk et al., **NAACL 2024** (short) | ✅ |
| Đúng chỗ (point-in-bbox) | **SeeClick / ScreenSpot** — Cheng et al., **ACL 2024** | ✅ |
| Ngưỡng dung sai 14% | **AITW** — Rawles et al., **NeurIPS 2023** | ✅ |
| τ cho ordering | Kendall 1938; tiền lệ NLP **Lapata, CL 2006** | ✅ |
| Partial-order (chỉ phạt cặp bắt buộc) | **Fagin et al., 2003 & 2006** (SIAM J. Discrete Math.) | ✅ |
| Step-SR / Action-Type | **AndroidControl** — Li et al., **NeurIPS 2024** | ✅ |
| Perturbation validate metric | **Sai et al., EMNLP 2021** | ✅ |
| Đúng nhãn (label-fidelity) | **Tự định nghĩa** (khớp chuỗi chính xác) — dùng làm kiểm-tra-phụ | ❌ |

**5/6 nhóm thước đo là peer-reviewed.** Chỉ "đúng nhãn" là tự định nghĩa, và ta khai thẳng điều đó, chỉ dùng nó làm kiểm-tra-phụ.

---

# PHẦN 6 — ĐÓNG GÓP (hai đóng góp — ngang nhau CÓ ĐIỀU KIỆN)

- **(A) Hệ thống:** sinh hướng dẫn **không bịa nút** (lớp hậu kiểm, cắm được vào VLM nào cũng chạy, quyết định thiết kế có đối-chứng-thất-bại) + **sắp thứ tự màn** (Stage-0). Là đóng góp hệ thống hợp lệ: xây được một hệ đảm bảo đầu ra không trỏ nút không tồn tại.
- **(B) Phương pháp đánh giá:** đo trung thực không cần đáp án mẫu mà không tự chấm (DG1) + đo thứ tự và làm-tới-đích trên dữ liệu có gold (DG2).

*Về "ngang nhau CÓ ĐIỀU KIỆN":* vị thế ngang nhau được giữ **với điều kiện nhánh nhiều màn (Step-SR) cho số dương thật**. Ở thời điểm này DG2 chưa prototype, nên trụ của A **KHÔNG** tựa vào con số DG2 (chưa có), mà tựa vào **3 chân ĐÃ CÓ**: (1) hệ **đạt đúng mục tiêu thiết kế** (đảm bảo không trỏ nút không tồn tại); (2) con số trung thực báo cáo = **tỉ lệ bịa của bản gốc** + cái giá %fallback; (3) **đối-chứng-thất-bại đo được** (phương án "đoán nút gần nhất" → lỗi ngầm trên 10 màn → chốt "chỉ mô tả") = phát hiện thực nghiệm, không phải độ-phức-tạp-code. DG2/Step-SR khi chạy xong sẽ **bổ sung** con số năng-lực-thật, chứ A không phụ thuộc vào nó để đứng vững.

---

# PHẦN 7 — GIỚI HẠN (nêu rõ)
- **DG2 chưa prototype** → phần "năng lực suy luận thứ tự" của A hiện là **kế hoạch**; nếu Step-SR ra null/âm, A vẫn đứng bằng lớp-trung-thực-hoá + đối-chứng-thất-bại đo được, **KHÔNG tuyên bố ngang B ở nửa đa-màn cho tới khi có số**.
- Nhánh một màn chỉ đo *không bịa*, chưa đo *đúng ý* → đúng ý đo ở nhánh đa màn (Step-SR).
- **Grounding (đúng-chỗ) đã RA khỏi headline một-màn** (chỉ dùng ở DG2/ScreenSpot-v2) để tránh tautology tâm-bbox.
- Trung thực sau hậu kiểm (~95%) một phần là tất yếu do thiết kế → báo tỉ lệ bịa của bản gốc, không trưng con số sau hậu kiểm như thành tựu.
- Lớp hậu kiểm đánh đổi độ cụ thể lấy độ an toàn (một phần bước thành mô tả khái quát).
- Danh sách nút là ảnh chụp một trạng thái → nút sau khi cuộn có thể bị nhầm "không có" → lọc/đánh dấu.
- Khi triển khai từ một ảnh cần bộ dò nút (có sai số) → tự đo độ phủ trước (cổng K1), đóng khung "số có điều kiện recall".
- Step-SR và nhãn cặp bắt buộc suy từ một quỹ đạo vàng → cận dưới và xấp xỉ → audit người.
- Chưa có bảng số tiếng Việt → định lượng làm trên dữ liệu tiếng Anh, tiếng Việt làm demo.

---

# PHỤ LỤC — CÂU HỎI GIÁM KHẢO HAY NGẮT (để thủ, không đọc)

1. **"Lúc sinh AI có thấy danh sách nút không?"** → Không. AI viết mù (ảnh + câu hỏi). Danh sách nút chỉ vào ở khâu đối chiếu, bằng thuật toán. Nếu cho thấy thì "không bịa" là hiển nhiên, đo vô nghĩa.
2. **"Faithfulness cứ bịa là viết lại thì đương nhiên 100%?"** → Đúng là tất yếu một phần, nên **em không lấy con số sau hậu kiểm làm headline**. Vì bộ chấm độc lập với bộ quyết nên nó ra ~95% chứ không ghim 100% — khe hở đó chứng minh không tautology. Headline của em = **tỉ lệ bịa bản gốc** + % fallback.
3. **"τ là gì, sao không dùng độ chính xác thường?"** → τ là tương quan thứ hạng Kendall (−1 đến +1). Khớp-thứ-tự-tuyệt-đối với N=3 đã ~17% đúng do ngẫu nhiên nên vô nghĩa; τ đo mức-độ-giống.
4. **"DG2 có phải hệ khác?"** → Không, một hệ duy nhất: N=1 thì khối sắp thứ tự rỗng, về đúng DG1; N≥2 thì bật khối đó lên. DG2 = DG1 + Stage-0.
5. **"Bộ khớp coi Confirm = Save thì bịa mà tính không bịa?"** → Đó là vùng khó nhất; em chọn ngưỡng theo precision ≥ 0.95, đóng băng trước khi chạy, báo precision/recall, và có bộ chấm LLM khác cơ chế làm backstop đúng vùng đó.
6. **"Ngưỡng 14% ở đâu ra?"** → Từ benchmark AITW (NeurIPS 2023), chuẩn dùng chung để một cú bấm "đủ gần tâm nút" được tính đúng.
7. **"Perturbation là tự bơm tự chấm?"** → Nó chứng minh thước đo *nhạy* với lỗi (có tiền lệ Sai et al., EMNLP 2021); em khai thẳng nó chưa thay được đối chiếu người, nên bổ sung mẫu chuyên gia nhỏ.
8. **"Đổi Submit thành mô tả là làm tệ đi?"** → Đúng, đổi độ-cụ-thể lấy độ-an-toàn; em đo và báo % bước bị khái quát hoá (~25%). Không giấu.
9. **"Cặp bắt buộc ai quyết?"** → Suy từ đáp án vàng bằng quy tắc nhân-quả, không từ model, không từ bộ-phát-hiện-cue → không tự chấm.
10. **"Step-SR so một quỹ đạo, đường khác thì sao?"** → Nên em gọi nó là **cận dưới**; báo cả bản teacher-forced để tách lỗi thứ tự khỏi lỗi thao tác.
