# Luận văn — tất cả trong một file để đọc

> Tài liệu này gộp mọi thứ cần đọc để hiểu trọn luận văn, đặt trong giả định **không bị áp lực thời gian**: thiết kế đang chốt, trạng thái hiện tại, những chỗ nếu rảnh thì nên đổi, các nghi ngờ chưa có bằng chứng, và kết quả ba vòng nghiên cứu nâng cấp vừa chạy (18/7/2026). Viết để đọc một mạch trên điện thoại; phần kỹ thuật sâu để trong "hộp" — bỏ qua vẫn hiểu mạch chính.
>
> Nguồn gốc: gộp từ report/54 (thiết kế), report/56 (ngưỡng đã khoá), report/63 (giữ gì/đổi gì), report/65 (tự phản biện), report/66–68 (ba vòng nghiên cứu nâng cấp). Khi cần đào sâu con số nào, mở đúng file gốc — bản đồ ở cuối.

---

## Mấy chữ hay gặp (đọc một lần cho khỏi rối)

Tài liệu có vài thuật ngữ lặp lại nhiều lần. Hiểu bảng này thì phần sau đọc trôi:

| Chữ | Nghĩa dễ hiểu |
|---|---|
| **View Hierarchy (VH)** | File do điện thoại Android xuất ra kèm mỗi ảnh, liệt kê các nút **thật** đang có trên màn (tên, loại, vị trí). Dùng làm "trọng tài" để biết mô hình có bịa nút không |
| **Độ trung thực** | Thước đo chính: tỉ lệ bước **không** bịa nút. Càng cao càng tốt |
| **Câu mô tả chung chung** (fallback) | Câu an toàn viết thay vào chỗ mô hình bịa (kiểu "tìm nút phù hợp với việc cần làm"), thay vì đoán bừa một tên nút |
| **Bộ đối chiếu** (matcher) | Thuật toán so tên nút mô hình nhắc với danh sách nút thật trong VH — khớp thì giữ, không khớp thì coi là bịa |
| **Thầy giáo / Học trò** | Thầy giáo = mô hình lớn có sẵn (gpt-4o-mini) viết bản nháp; Học trò = mô hình nhỏ (Qwen2.5-VL-3B) học viên tự huấn luyện — sản phẩm chính |
| **Tier 1 / Tier 2** | Hai tầng thí nghiệm. Tier 1 = lưới an toàn (gần chắc có kết quả tốt); Tier 2 = phép thử chính (có thể ra "không khác biệt") |
| **Đăng-ký-trước** (pre-register) | Khoá sẵn quy tắc thắng-thua vào sổ trước khi chạy, để không "nhìn số rồi mới đặt tiêu chuẩn cho vừa" |
| **Kết quả rỗng** (null) | Thí nghiệm không tìm thấy khác biệt đủ tin cậy — vẫn là một phát hiện, không phải thất bại |
| **Vòng A/B/C · K1–K3 · D1–D3** | Mã các vòng nghiên cứu và kiểm chứng — mỗi cái được giải thích tại chỗ khi gặp |

---

# PHẦN I — HIỂU LUẬN VĂN LÀM GÌ

## 1. Đề tài và vì sao đổi hướng

**Đề tài:** cho một tấm ảnh chụp màn hình ứng dụng cộng một câu hỏi kiểu *"làm sao để bật thông báo cho tập mới?"*, hệ thống trả lời bằng các bước cụ thể bám đúng màn hình đó — *"1. Chạm Settings — 2. Chạm Notifications — 3. Bật New episode alerts"*.

**Vì sao đổi hướng.** Bản đầu của luận văn = gọi API gpt-4o-mini đọc ảnh viết hướng dẫn, rồi dùng thuật toán so chuỗi kiểm bịa. Thầy nhận xét thẳng: đây chủ yếu là *gọi API + so chuỗi*, chưa thấy **mô hình do học viên tự huấn luyện** — mà quy định thạc sĩ của trường bắt buộc phải có. Nên toàn bộ phần lõi (bài toán, ba bộ dữ liệu, cách đo không cần đáp án mẫu) giữ nguyên, chỉ thêm một khối trung tâm mới: **một mô hình thật được huấn luyện.**

Hướng này đã qua **bảy vòng "vặn"** (dựng lên rồi cố tình tìm cách bẻ gãy bằng cách tra cứu các nghiên cứu đã có + cho nhiều góc nhìn công kích) + một vòng rà soát tổng thể. Không vòng nào tìm ra lỗi buộc phải đập đi làm lại — chỉ có chỗ phải nói khiêm tốn hơn, đo thêm cho chắc, hoặc thống nhất lại định nghĩa.

## 2. Bài toán khó ở đâu

**Khó thứ nhất — không có đáp án mẫu.** Không tồn tại bộ hướng dẫn "chuẩn" do người soạn cho từng màn hình; tự soạn thì tốn hàng nghìn giờ, ngoài tầm luận văn. Phải nghĩ cách đo không cần đáp án mẫu.

**Khó thứ hai — một kiểu lỗi đặc biệt nguy hiểm.** Mô hình có thể **bịa tên một nút không tồn tại** trên màn (ví dụ nói "Chạm Preferences" trong khi màn không có nút đó). Người dùng dò không thấy, hoặc bấm nhầm nút khác nghe na ná. Lỗi này *khó phát hiện bằng mắt* vì câu văn đọc lên trơn tru — chỉ khi đối chiếu đúng màn mới lòi ra nút ấy không có thật.

## 3. Ý tưởng cốt lõi: dạy một mô hình nhỏ thói quen "thành thật"

Hình dung có **thầy giáo** và **học trò**:

- **Thầy giáo** = gpt-4o-mini (mô hình lớn, gọi qua mạng). Chỉ được nhìn ảnh + câu hỏi, **không** thấy trước danh sách nút thật → đôi khi đoán bừa, bịa tên nút.
- **Đối chiếu** từng tên nút thầy giáo nhắc với **View Hierarchy (VH)** — file do hệ điều hành Android xuất kèm mỗi ảnh, liệt kê mọi phần tử đang hiển thị (loại gì, tên hiển thị, toạ độ). Đây là **thuật toán so khớp theo nghĩa**, không phải một AI khác. Không khớp = biết chắc là bịa.
- Chỗ bịa → **viết lại thành câu mô tả chung chung nhưng trung thực** (kiểu "Tìm và chạm vào tuỳ chọn phù hợp với việc bạn cần làm ở bước này"), tất định, không đoán nút khác, không gọi LLM viết lại.
- Bộ dữ liệu đã lọc sạch → dùng để **huấn luyện học trò** = **Qwen2.5-VL-3B** (mô hình mở, nhỏ, chạy ngay trên laptop/điện thoại, không cần internet).
- **Lúc dùng thật:** học trò chỉ nhận ảnh + câu hỏi, không cần VH, không cần thầy giáo.

> **Vì sao không "đoán nút thay".** Có một phương án khác: tra VH rồi thay tên nút bịa bằng một nút có thật nghe gần giống. Đã **loại**, vì rất dễ thay bằng nút có thật nhưng **sai chức năng** → hướng dẫn vẫn sai, mà lần này sai kín đáo không ai thấy (luận văn đo thẳng chuyện này bằng *tỉ lệ lỗi-ngầm*).

### Bốn "nhân vật" cần nhớ

| Gọi trong tài liệu | Thực chất | Vai |
|---|---|---|
| **Thầy giáo** | gpt-4o-mini | Viết bản nháp để tạo data. Chỉ có mặt lúc chuẩn bị dữ liệu |
| **Thầy giáo trần** (Teacher-BASE) | gpt-4o-mini, lấy nguyên nháp **chưa lọc** | Mốc so ở Tier 2 = "nếu cứ gọi API như bản cũ thì được bao nhiêu" |
| **Học trò** (Student) | Qwen2.5-VL-3B, học từ data **đã lọc** | **Sản phẩm chính** |
| **Học trò đối chứng** (Student-RAW) | Qwen2.5-VL-3B, học từ data **thô** | Đối chứng ở Tier 1 |

Học trò và học trò đối chứng **giống nhau tuyệt đối** — cùng mô hình gốc, cấu hình, số mẫu, số vòng. Khác duy nhất: data học có qua bước lọc bịa hay không. Nhờ vậy mọi chênh lệch đo được chỉ có thể đến từ đúng bước lọc.

### Sơ đồ luồng

```
LÚC HUẤN LUYỆN (một lần, offline)
  Ảnh + câu hỏi → Thầy giáo (không thấy VH) → nháp (~1/4 bước có bịa)
       → Đối chiếu VH (thuật toán) → đúng: giữ · bịa: viết lại chung chung
       → Data đã lọc → huấn luyện Học trò (Qwen2.5-VL-3B) → MÔ HÌNH HỌC TRÒ

LÚC DÙNG THẬT (trên máy người dùng)
  Ảnh + câu hỏi → Học trò tự viết hướng dẫn → người dùng
  (không cần thầy giáo, internet, hay VH)
```

*(Con số "~1/4" là quan sát sơ bộ từ một lần thử nhỏ trên một mô hình — dùng để hình dung quy mô, chưa phải tỉ lệ đo chính thức.)*

## 4. Cái mới ở đây là gì — nói thật, không phóng đại

Công thức "sinh → lọc → huấn luyện lại" **không mới**: đã có STaR (2022), KnowAda (2025, viết lại phần không chắc thành mô tả chung chung cho caption ảnh), VGA (2024, dùng VH giảm bịa cho GUI). Tính mới thu về **đúng hai điểm**, sau khi một vòng tranh luận riêng cố bẻ gãy mà nó vẫn đứng:

1. **Nguồn kiểm tra độc lập với chính AI đang bị kiểm.** KnowAda để mô hình tự hỏi-tự-trả-lời đoán xem nó có "biết" chi tiết vừa viết không — tự chấm mình. Ở đây dùng nguồn hoàn toàn bên ngoài (VH) để đối chiếu, cho hành vi **rủi ro cao** (bịa tên nút khiến thao tác sai trên hệ thống thật).
2. **Câu hỏi trung tâm chưa ai đặt:** khi học trò — mô hình nhỏ, chạy trên máy, **không có nguồn kiểm tra bên ngoài lúc dùng thật** — liệu thói quen thành thật có còn giữ được không? Đây là câu hỏi **có thể trả lời "không"** (kết quả rỗng, model chỉ học vẹt bề mặt). Chính vì có khả năng trả lời "không" một cách trung thực, nó mới là câu hỏi nghiên cứu thật.

## 5. Có đủ ngưỡng luận văn thạc sĩ không

**Đủ, với một điều kiện.** Thạc sĩ không đòi đánh bại kỷ lục thế giới — được phép có đúng một thí nghiệm trọng tâm có thể ra "không khác biệt", miễn thiết kế nghiêm túc + có quy tắc thắng-thua định trước. (Tiền lệ: workshop Pre-registration gắn với NeurIPS 2021 chuyên nhận nghiên cứu kiểu này; Thông tư 23/2021 của Bộ GD.)

Về **khối lượng**, đề tài thiên về *hơi rộng*, không mỏng — bốn khối việc thực chất: (1) quy trình tổng hợp data chống-bịa; (2) huấn luyện thật hai bản mô hình độc lập (lọc + thô); (3) phương pháp đo không đáp án mẫu (bơm lỗi + chấm độc lập khác họ + chống tự-chấm); (4) thiết kế thí nghiệm hai tầng có đăng-ký-trước. Có **xây** + có **đo** + có **phát hiện**.

**Điều kiện bắt buộc về thiết kế: tách rõ hai tầng thí nghiệm** (mục 8 dưới) — để một kết quả rỗng ở tầng rủi ro không kéo sập cả luận văn.

## 6. Mô hình xây thế nào (không cần biết máy học)

Huấn luyện lại toàn bộ mô hình từ đầu quá tốn kém. Kỹ thuật dùng ở đây là **LoRA**: chỉ gắn thêm ít "miếng dán" học được vào một phần mô hình và chỉ huấn luyện những miếng đó, phần còn lại đóng băng — rẻ hơn hàng trăm lần.

Mô hình có phần "nhìn" (hiểu ảnh) và phần "nói" (viết câu). Vì việc cần dạy là thói quen *nói gì khi không chắc*, không phải *nhìn thấy gì*, nên **đóng băng phần nhìn**, chỉ huấn luyện phần nói. Vừa tiết kiệm, vừa tránh nhiễu kết quả bởi thay đổi không liên quan.

> **Hộp kỹ thuật.** LLaMA-Factory; QLoRA 4-bit (chạy được T4 16GB); LoRA r=8, alpha=16, chỉ vào decoder, freeze ViT; ~1.500–3.000 mẫu; lr 1e-4, 3 epoch (ước tính, cần smoke-test). Cấu hình neo theo ZonUI-3B (WACV 2026) — từng train thật loại mô hình này trên một card đồ hoạ phổ thông.

## 7. Dữ liệu

- **MobileViews** (preprint arXiv, giấy phép MIT) — ảnh + VH, dùng train + chấm một-màn. Bản công khai tải được ~231K dòng (không phải 600K — phần còn lại ở định dạng chưa tương thích). Thừa xa nhu cầu.
- **AndroidControl** (NeurIPS 2024 D&B, CC0) — có gold trajectory, để dành nhánh nhiều-màn (làm sau). Test = 1.542 (không in "2.855").
- **ScreenSpot-v2** (OS-Atlas, ICLR 2025) — 501 mobile, đối chứng grounding.

**Không có bộ dữ liệu giao diện tiếng Việt** (đã quét MobileViews trên máy 231 file → chỉ 2 màn có chữ Việt lẻ). Ảnh hưởng bài VCL (xử bằng hướng "sinh tiếng Việt trên màn hình tiếng Anh").

**Chia 18 ứng dụng để dạy / 12 ứng dụng để chấm, khoá cố định và ghi vào sổ TRƯỚC khi chạy** (giống ra đề thi khác hẳn bài ôn — chống mô hình "học thuộc" ứng dụng từng thấy). Kho dữ liệu dạy mở rộng (đã tải 12/7): **498 màn / 220 ứng dụng**, đã lọc trùng theo tên và theo ảnh, **không màn nào rò rỉ sang** 12 ứng dụng để chấm.

> **Các con số màn dễ lẫn:** 127 màn/30 app = toàn bộ pilot đã lọc chất lượng; 76 màn/18 app = phần train của pilot; 51 màn/12 app = phần test; 498 màn/220 app = mở rộng (chỉ vào train); **≈574 màn = 76 + 498 = tổng train thật** → ~1.700–2.870 mẫu.

## 8. Đo lường và quy tắc thắng-thua (khoá trước khi nhìn số)

### Thước chính — độ trung thực

**`f = 1 − tỉ lệ bịa`.** Tỉ lệ bịa = (số bước nhắc đích danh một nút **không** có trong VH) / (số bước có nhắc tên nút). Bước nói chung chung không tính vào mẫu số. Ví dụ: 4 bước, 3 bước nhắc tên nút, 1 bước nhắc "Preferences" (không có) → tỉ lệ bịa = 1/3. Càng thấp càng tốt.

> **Hộp kỹ thuật.** Trụ = ALOHa (Petryk et al., NAACL 2024): trích thực thể bằng LLM → so embedding → ghép Hungarian → không cặp nào đủ giống thì tính bịa. Gộp trung bình theo app trước → đơn vị thống kê = **12 con số per-app** (macro-per-app). Estimand = trung bình đều trên app, **cấm viết "đại diện cho ứng dụng nói chung"**.

### Ba thước kèm bắt buộc (chống ăn gian thước chính)

Thước chính ăn gian rất dễ: cứ nói chung chung mọi bước là bịa = 0. Nên luôn báo kèm:

| Thước | Đo gì | Vì sao bắt buộc |
|---|---|---|
| **%fallback** | Tỉ lệ bước rơi vào câu mô tả chung chung | Trung thực cao + fallback cao ngất = né trả lời. Đây là **cái giá** báo song song với **cái lợi** |
| **Tỉ lệ lỗi-ngầm** | Trong "phương án đoán thay" đã loại: bao nhiêu bước bị thay bằng nút có thật nhưng **sai chức năng** | Bằng chứng cho quyết định "chỉ mô tả, không đoán" |
| **Tỉ lệ màn 0-nhắc-nút** | Bao nhiêu màn model không nêu tên nút nào | Chỉ báo né-trả-lời. >50% màn 0-nhắc-nút/app → gắn cờ |

### Chống "vừa đá bóng vừa thổi còi"

**Bản luận văn cũ đã chết một lần đúng ở đây:** bộ lọc vừa sửa lỗi vừa chấm chính mình → trung thực vọt gần 100%, một con số đẹp và vô nghĩa (chỉ nói bộ lọc đồng ý với chính nó). Nguyên tắc rút ra: **thứ dùng để lọc lúc train tuyệt đối không dùng lại để chấm.**

> **Hộp kỹ thuật.** Lọc: embedding `nomic-embed-text`, ngưỡng τA=0.55 (freeze). Chấm: **ba cơ chế khác họ**, kết luận bịa khi ≥2/3 đồng ý — (1) `bge-m3` với τB **hiệu chuẩn riêng** (80–120 cặp gán tay, P/R + Cohen's κ, precision ≥0.95, **không tái dùng τA**); (2) LLM-judge `llama3.2` local, khác họ generator GPT (trụ Panickssery NeurIPS 2024 về self-preference bias); (3) token-overlap phi-neural. **Khai thẳng:** ba cơ chế *giảm* chứ không *loại* tương quan sai số → báo hệ số tương quan giữa các bộ chấm, không tuyên bố "độc lập".

### Thống kê — phép đổi-dấu chính xác cho mẫu nhỏ

Chỉ có 12 app test → thống kê giả định mẫu lớn không đáng tin. Dùng **exact sign-flip test**: có 12 con số chênh lệch, liệt kê hết 2¹²=4.096 tổ hợp đảo/giữ dấu, tính trung bình từng tổ hợp, xem kết quả thật xếp thứ mấy. Nằm trong nhóm 5% cao nhất → khác biệt thật, không do may. **Liệt kê hết mọi khả năng, không cần giả định phân bố** — đáng tin hơn hẳn thống kê thường với mẫu nhỏ.

### MDE — con số quyết định thí nghiệm có đáng chạy không

MDE = mức chênh lệch nhỏ nhất mà thí nghiệm đủ sức nhìn thấy với 12 app. Ví như độ phân giải của kính: MDE=25 điểm mà khác biệt thật chỉ 10 điểm → ra "không thấy gì" **vì kính mờ, không phải vì học trò kém**. Phải đo MDE bằng số liệu pilot thật **trước** khi khoá mọi thứ. Nếu MDE > 15–20 điểm → **đổi chia 18/12 thành 15/15** (hy sinh data dạy lấy thêm app chấm) — nhưng chỉ được đổi *trước* khi khoá ngưỡng.

> **Ô `[MDE = ___ pp]` trong bản đăng-ký-trước hiện CÒN TRỐNG — đây là việc kế tiếp.**

### "Đủ lớn về mặt thực tế" — điều kiện (B)

Thống kê chỉ trả lời "có thật không", không trả lời "có đáng kể không". Nên thêm mức sàn: lấy mức cải thiện trên **18 app train** làm mốc (`Δ_train` — điều kiện thuận lợi nhất), rồi đòi mức trên **12 app test** (`Δ_test`) đạt ít nhất **một nửa** mốc đó: **`Δ_test ≥ 0.5 × Δ_train`**.

> Hệ số 0.5 = **tự đề xuất, không lấy từ literature** — thầy hỏi thì nói đúng vậy, đừng bịa nguồn. Điều kiện bắt buộc: cả `Δ_train` và `Δ_test` đo **cùng công thức, cùng điều kiện tắt-VH**, chỉ khác nhóm app.

### Ba kết cục, viết sẵn diễn giải trước khi chạy

| Kết cục | Điều kiện | Ý nghĩa |
|---|---|---|
| **Thắng đầy đủ** | (A) có ý nghĩa thống kê + (B) đủ lớn | Thói quen thành thật đã ngấm thật, tổng quát sang app lạ (trong loại màn giống MobileViews đã QC) |
| **Thắng một phần** | (A) đúng, (B) sai | Có ngấm nhưng yếu — vẫn là phát hiện có giá trị |
| **Không thấy khác biệt** | CI chứa 0 | Báo trung thực + MDE, đây là giới hạn thật. Không có nghĩa cả luận văn thất bại vì Tier 1 đứng độc lập |

## 9. Bộ thí nghiệm — một cổng + bảy thí nghiệm

Chỉ **hai** cái mang kết luận luận văn (một gần chắc thắng, một có thể thua thật); năm cái còn lại để thủ trước các câu vặn.

| # | Thí nghiệm | So gì | VH lúc suy luận | Ngưỡng (đã khoá) | Vai |
|---|---|---|---|---|---|
| **TN0** | Cổng MDE + khoá split | — | — | MDE > 15–20 pp → đổi 18/12 thành 15/15 trước khi khoá | **Cổng — chạy trước hết** |
| **TN1** | **Tier 1 — lưới an toàn** | Student vs Student-RAW | Tắt (chấm output thô) | CI 95% của Δ hoàn toàn trên 0. Nếu null → dừng, rà lại pipeline lọc | **Bắt buộc — gần chắc dương** |
| **TN2** | **Tier 2 — trụ chính** | Student vs Teacher-BASE | **Tắt hẳn**, held-out theo app | (A) CI trên 0 **VÀ** (B) Δ_test ≥ 0.5·Δ_train | **Bắt buộc — có thể null** |
| **TN3** | Thước đi kèm | mọi arm | — | Không ngưỡng, báo cáo bắt buộc | Bắt buộc |
| **TN4** | Đo hữu-ích/mạch-lạc | Student vs Student-RAW | — | Trong family Holm | Bắt buộc |
| **TN5** | Hiệu chuẩn bộ chấm | bge-m3 vs người, 80–120 cặp | — | Precision ≥0.95, báo κ | Bắt buộc — không có nó thì TN1/TN2 vô nghĩa |
| **TN6** | Validate thước đo bằng bơm lỗi | metric vs lỗi đã biết | — | detection ≥0.80, false-pos ≤0.10, đơn-điệu | **Bỏ được** — không kịp thì rút claim tương ứng |
| **TN7** | Dose-response (trộn 25/50/75% data lọc) | — | Tắt | Chưa pre-register → chỉ báo thăm dò | Tuỳ chọn / Plan B |

> **Một chỗ dễ đọc nhầm:** cụm "Tier 1 VH vẫn có" mô tả **bối cảnh triển khai** (hệ deploy đầy đủ vẫn còn lớp viết-lại phía sau). Còn **phép đo `f` ở cả hai tầng đều trên output THÔ, giống hệt nhau** — chỉ khác cặp đem so. Nếu chấm `f` *sau* lớp viết-lại thì mọi bản đều sạch, Δ≈0 → null giả tạo. Lợi ích của lớp viết-lại báo riêng qua %fallback + lỗi-ngầm.

---

# PHẦN II — TRẠNG THÁI VÀ ĐƯỜNG ĐI

## 10. Đang ở đâu (18/7/2026)

**Đã xong:** 7 vòng tranh luận + rà soát; nghiên cứu chọn hướng; danh sách chia 18/12 đã ghi vào sổ (`3776212`); bản đăng-ký-trước report/56 đã vá 4 lỗ + ghi sổ (`2c84ce8`); kho dữ liệu dạy mở rộng 498 màn/220 ứng dụng, đã kiểm không rò rỉ.

**Thứ tự cứng — không đảo:**
1. Khoá danh sách chia ứng dụng (✅ xong).
2. Chạy **thử nghiệm nhỏ đo độ dao động nền** → **tính MDE thật** (mức chênh lệch nhỏ nhất nhìn thấy được) → điền ô `[MDE=___pp]` ở report/56 → nếu cần đổi cách chia 15/15 thì đổi → **ghi sổ lần 2**.
3. **Chỉ sau đó** mới chạy bước tốn tiền đầu tiên: gọi thầy giáo gpt-4o-mini viết bản nháp (~$1–2, hỏi trước).
4. Đối chiếu + viết lại → dựng dữ liệu huấn luyện → chạy thử 20 mẫu → huấn luyện Học trò + Học trò đối chứng → chấm hai tầng.

> **⚠️ Đường đi đã ĐỔI (16–17/7):** vòng tự-phản-biện (mục 12) chỉ ra bộ đối chiếu là mắt xích chưa kiểm. Nên **trước khi tính MDE** giờ chèn hai phép thử nhanh *miễn phí, chạy trên máy*: **K1** (kiểm bộ đối chiếu có sai không) → **K2** (đếm phân loại kiểu bịa). Xong K1/K2 mới tới bước tính MDE.

## 11. Nếu KHÔNG áp lực thời gian — giữ gì, đổi gì

Đây là câu hỏi trọng tâm của bản này. Ngay cả khi có vô hạn thời gian:

**Giữ nguyên (xương sống):**

| Thành phần | Vì sao giữ |
|---|---|
| Sinh nháp → lọc bằng VH → huấn luyện lại | Chưa ai làm đúng công thức này cho giao diện điện thoại — khoảng trống thật, chưa bị người khác làm mất |
| Chấm trên ứng dụng chưa từng thấy + hai tầng Tier 1/Tier 2 | Tách "lưới an toàn" khỏi "phép thử chính có thể ra rỗng" là thiết kế phòng thủ đúng, không phụ thuộc thời gian |
| Không tự đá bóng tự thổi còi (thuật toán lọc khác hẳn bộ chấm) | Không có lý do bỏ, rảnh hay gấp |
| Khoá ngưỡng thắng-thua trước khi chạy | Càng rảnh càng nên giữ — đây là chuẩn mực khoa học |

**Ba chỗ đáng đổi nếu rảnh** (xếp theo mức đáng đổi) — và ba vòng research ở mục 13 đã đi kiểm đúng ba chỗ này:

1. **Thước đo headline:** cặp số rời (tỉ-lệ-bịa + %fallback) → một **đường risk-coverage** duy nhất (AURC). Hai số rời đánh đổi nhau (ăn gian bằng fallback nhiều); một đường cong so trên cả dải thay vì tại một điểm tuỳ ý. → **Vòng A.**
2. **Fallback template cố định → tập câu đa dạng.** Nguy cơ model học vẹt một câu mẫu lặp lại. → **Vòng B.**
3. **Trọng tài VH đơn lẻ → VH + OCR.** VH thiếu nhãn nhiều → matcher đánh oan bước đúng thành "bịa". → **Vòng C.**

**Vì sao mùa này vẫn theo thiết kế cũ:** deadline FAIR 15/8 + pre-reg đã commit. Đổi thước đo bây giờ = viết lại pre-reg + tính lại MDE + lùi lịch. Cách dung hoà rẻ nhất: **giữ cam kết cũ làm headline, báo THÊM cái mới như phân tích phụ** — nhưng đó là quyết định của user + nên hỏi thầy.

## 12. Tự phản biện — sáu nghi ngờ chưa có bằng chứng

Xương sống tin vững (cấu trúc dữ liệu ép). Nhưng khi phản biện đến cùng, còn **sáu nghi ngờ**, trong đó **một cái nếu hỏng thì phải sửa pipeline thật**:

| # | Nghi ngờ | Nếu đúng là hỏng thì… | Kiểm bằng | Chi phí |
|---|---|---|---|---|
| **1** ⚠️ | **Bộ đối chiếu sai CẢ HAI CHIỀU:** bỏ lọt bịa gần-nghĩa (bịa "Preferences" khi màn có "Settings" — hai chữ gần nghĩa nên máy tưởng khớp, cho qua) · kết oan bước đúng vì VH thiếu nhãn | **phải sửa pipeline** (nâng bộ đối chiếu) | phép thử **K1** | miễn phí |
| **2** | Chỉ bắt bịa **tên nút**, lọt bịa **hành động/luồng** ("vuốt sang trái mở menu" — không có thao tác đó) | thu hẹp phạm vi khẳng định | đếm tay dữ liệu cũ **K2** | miễn phí |
| **3** | Thầy giáo viết MÙ rồi lọc, hay cho NHÌN VH từ đầu? Lý lẽ "viết mù rồi lọc" chưa kiểm | thêm một bản để so, đổi cách kể đóng góp | tranh luận **D1** | miễn phí |
| **4** | Học trò học "né ĐÚNG CHỖ" hay chỉ "né đúng TẦN SUẤT" (rắc câu chung chung ngẫu nhiên)? Bộ thước hiện tại chưa tách được | thêm một thước đo mới | tranh luận + tra cứu **D2** | miễn phí |
| **5** | Thầy giáo ít bịa → không còn gì để lọc → Tier 1 rỗng. Đòn "dùng mô hình 2026 xịn thì đâu cần lọc?" | chuẩn bị câu thủ + số liệu | thử nhỏ trên mô hình mới | ~$1–2 |
| **6** | Câu mô tả chung chung có HỮU ÍCH thật với người đọc không, hay chỉ đổi "sai nguy hiểm" lấy "vô dụng lịch sự"? | sửa lại mẫu câu | đọc tay 30 câu | miễn phí |

**Kết luận:** đi tiếp với thiết kế này — CÓ, nhưng chỉ sau khi **K1/K2** (miễn phí, vài giờ) cho số đẹp. Nếu K1 xấu, chỗ sửa là **nâng cấp bộ đối chiếu** (thêm OCR / thêm luật / ngưỡng chặt hơn), không phải đập cả khung — thiết kế thay thế nào cũng cần một trọng tài, và trọng tài nào cũng phải qua đúng phép thử này.

## 13. Kết quả ba vòng research nâng cấp (chạy 18/7/2026)

Ba vòng đi kiểm đúng ba chỗ "đáng đổi" ở mục 11. **Không vòng nào đòi đập thiết kế** — đều là thêm/tinh chỉnh.

### Vòng A — Thước đo risk-coverage (report/66)

*Bối cảnh: ý tưởng là gộp hai con số hiện tại (tỉ-lệ-bịa và tỉ-lệ-nói-chung-chung) thành một đường cong duy nhất để so công bằng hơn. Vòng A đi tìm xem có tiền lệ khoa học để dựa không.*

**Cổng A1 = KHÔNG ĐẠT.** Đọc toàn văn hai bài trụ (CAP — ACML 2025, đã bình duyệt; SafeGround — bản tiền ấn phẩm 2602.02419) thấy **cả hai đều đo mức "rủi ro" bằng đáp án chuẩn có sẵn** (CAP: đáp án trắc nghiệm; SafeGround: vùng đúng do người khoanh tay). **Không có bài bình duyệt nào** đo rủi ro bằng thuật toán tự động (không đáp án mẫu) như luận văn → đây là chỗ trống phải **tự biện minh**, không mượn được ai.

- Vẫn dùng được: CAP báo song song cả đường cong lẫn con số → tiền lệ về *cách trình bày*. Nhưng đường của CAP vẽ ngược chiều và không cho công thức rõ ràng.
- **Khuyến nghị:** **giữ hai con số rời đúng như đã đăng-ký-trước + thêm đường cong làm biểu đồ PHỤ.** Rẻ nhất, không phải sửa cam kết/tính lại MDE/lùi lịch, vẫn chặn được đòn "ăn gian bằng cách nói chung chung nhiều". **Không đổi hẳn con số chủ đạo trước 15/8.**

### Vòng B — Chống học vẹt template fallback (report/68)

*Bối cảnh: nếu câu mô tả chung chung chỉ là MỘT câu mẫu lặp đi lặp lại trong dữ liệu dạy, mô hình có thể học vẹt đúng câu đó. Vòng B tìm cách đo và phòng.*

- **Cách đo độ đa dạng câu chữ:** dùng ba thước quen thuộc trong ngành (đếm cụm từ khác nhau, độ trùng lặp giữa các câu, độ "tản" của phân bố — trụ Liu ACL 2022, Zhu SIGIR 2018, GEM ICLR 2025). Không có ngưỡng tuyệt đối → **so tương đối: trước khi huấn luyện vs sau khi huấn luyện**; báo động khi độ đa dạng của phần câu chung chung tụt gần về 0. Tiền lệ: bài GEM đo được độ "tản" tăng 0.42→0.76 sau khi vá.
- **Số câu diễn đạt khác nhau cho câu mô tả = 10** (dựa theo bài FLAN ICLR 2022). Không có con số vàng riêng cho trường hợp này.
- **Có nên gắn một "ký hiệu từ chối" riêng không? Không.** Chưa ai làm việc này cho mô hình thị giác nhỏ, lại dễ khiến mô hình từ chối quá đà, và không có đáp án mẫu để chứng minh nó hoạt động đúng → **chọn cách 10 câu diễn đạt khác nhau**. Tuỳ chọn nhẹ: gắn dấu `[MÔ TẢ]` ở đầu câu.
- **Cổng B2 = ĐẠT-có-điều-kiện:** có một con số dùng được (10) để đưa thẳng vào lúc dựng dữ liệu.

### Vòng C — Fusion VH+OCR giảm oan sai matcher (report/67)

*Bối cảnh: VH hay thiếu nhãn với chữ nằm trên ảnh → bộ đối chiếu dễ đánh oan một bước ĐÚNG thành "bịa". Ý tưởng: dùng thêm OCR (đọc chữ trong ảnh) bù chỗ VH mù. Vòng C hỏi: dùng thế nào cho đúng.*

- **Cổng C3 = đóng (theo nghĩa tốt):** không ai công bố sẵn con số so "chỉ dùng VH" với "VH + OCR" để trích thẳng → **phải tự đo** trên 127 màn (miễn phí, chạy trên máy). Ba nguồn đã kiểm chống lưng: Fok CHI 2022 (55,6% phần tử dạng ảnh thiếu nhãn), Screen Recognition của Apple CHI 2021 (59% màn / 94% ứng dụng có phần tử VH không liệt kê được — mã bài đúng là **2101.04893**), PW2SS Neurocomputing 2024 (OCR + bộ dò đọc được nhiều hơn hẳn chỉ đọc VH, hơn 17%).
- **Đặt OCR ở đâu:** **chỉ ở khâu LỌC dữ liệu** (cấp thêm tên nút cho bộ đối chiếu), **tuyệt đối không đưa vào khâu chấm điểm** → giữ nguyên tắc "không tự đá bóng tự thổi còi". Tiền lệ: chính nhóm làm MobileViews cũng dùng OCR trong bước lọc.
- **Chọn phần mềm OCR nào:** phần tìm kiếm không cho ra xếp hạng kiểm chứng được → **chọn bằng cách chạy thử** (PaddleOCR làm mặc định, EasyOCR làm đối chứng trên ~20 màn), vì dù sao cũng phải tự đo.
- **Bước tiếp:** mở rộng đoạn mã đo độ phủ nhãn sẵn có thêm nhánh OCR; **khoá ngưỡng "chữ nằm trong khung nút" trước khi chạy**; khai rõ giới hạn "chỉ đo được trên phần tử VH có liệt kê".

### Tổng ba vòng

| Vòng | Kết quả cổng | Áp vào luận văn |
|---|---|---|
| **A** — đường cong đánh đổi | **KHÔNG ĐẠT** | Giữ hai con số rời + thêm đường cong làm biểu đồ phụ. Không đổi con số chủ đạo trước 15/8 |
| **B** — chống học vẹt câu mẫu | **ĐẠT có điều kiện** | Câu mô tả = 10 cách diễn đạt khác nhau; đo độ đa dạng trước/sau huấn luyện; không gắn ký hiệu từ chối |
| **C** — dùng thêm OCR | **đóng** (phải tự đo) | OCR chỉ ở khâu lọc; viết mã đo mức bù độ phủ nhãn; khoá ngưỡng trước khi chạy |

### Còn một điểm report/64 nêu mà ba vòng chưa chạm: trục "ĐÚNG"

report/64 (thử thiết kế lại từ trang trắng, chỉ nhìn đề tài + ba bộ dữ liệu) vẽ lại **gần như cùng bộ khung** — vì cấu trúc dữ liệu ép phải vậy: VH là nguồn đúng-sai duy nhất khi không có đáp án mẫu nên phải làm trọng tài; không có đáp án mẫu nên phải chưng cất rồi lọc; các màn trong cùng ứng dụng giống nhau nên phải chia tách theo ứng dụng. Đây là tin tốt: thiết kế hiện tại không phải sản phẩm của quán tính. Bản đó nêu **5 điểm khác**, và ba trong số đó đúng là ba vòng vừa chạy:

| Điểm report/64 | Trạng thái |
|---|---|
| **1. [Lỗ thật] Thiếu trục "ĐÚNG"** | **CHƯA chạy — chỗ đáng bàn nhất** (xem dưới) |
| 2. OCR bù VH | = **Vòng C** (đã chạy) |
| 3. Tập câu né đa dạng + đo | = **Vòng B** (đã chạy) |
| 4. Đường đánh đổi (risk-coverage) | = **Vòng A** (đã chạy) |
| 5. So lọc-sau vs bám-từ-đầu | = **Vòng E** (để sau 15/8) |

**Điểm 1 — trục "ĐÚNG" — là lỗ thật, đáng cân nhắc cho việc chốt.** Toàn bộ thước đo hiện tại chỉ chứng minh *"không bịa + có ích theo judge"*. Phản biện mạnh nhất thầy có thể tung: *"model né bịa được, nhưng hướng dẫn có ĐÚNG — có dẫn tới đích — không thì chưa có con số nào."* Độ trung thực (không bịa) và độ đúng (dẫn đúng việc) là hai chuyện khác nhau: một hướng dẫn toàn nút có thật vẫn có thể sai thứ tự hoặc trỏ nhầm việc.

- **Cách vá rẻ report/64 đề xuất:** dùng bộ **AndroidControl** ở dạng từng-bước-như-một-màn — bộ này CÓ sẵn chuỗi thao tác đúng do người thật làm, nên đo được "bước mô hình sinh ra có khớp thao tác đúng không". Không đụng nhánh nhiều-màn, không cần sắp thứ tự, dùng lại 286 tình huống đã chọn.
- **Cái giá:** thêm một thí nghiệm vào bộ đã đăng-ký-trước → **phải bàn với thầy** (khác với điểm 2/3/4 lắp thêm được mà không phá cam kết).
- Trong danh sách việc kiểm chứng (mục 14), đây chính là **D2** — chưa chạy.

Nói thẳng: đây là điểm **có thể đổi phạm vi luận văn** (thêm một trục đo mới). Nếu bạn muốn chốt "có đưa trục ĐÚNG vào mùa này không", nên chạy **D2** hoặc hỏi thầy trước — ba vòng A/B/C đã chạy KHÔNG trả lời câu này.

## 14. Plan nghiên cứu/kiểm chứng tiếp theo

**Nhóm phép thử nhanh trên máy (miễn phí — chạy trước, cho số thật):**
- **K1** — kiểm bộ đối chiếu có sai hai chiều không (nghi ngờ 1). **Việc đầu tiên.**
- **K2** — đếm phân loại kiểu bịa (bịa tên nút vs bịa hành động/luồng, nghi ngờ 2).
- **K3** — thử nhỏ trên mô hình mới xem nó còn bịa nhiều không (nghi ngờ 5, ~$1–2, hỏi trước).

**Nhóm tranh luận / tra cứu nhỏ (miễn phí):**
- **D1** — thầy giáo viết mù rồi lọc, hay cho nhìn VH ngay từ đầu (nghi ngờ 3).
- **D2** — thêm trục đo "ĐÚNG" bằng AndroidControl từng-bước (điểm 1 của report/64, mục 13) — **chỗ có thể đổi phạm vi, đáng chạy / hỏi thầy nhất**.
- **D3** — mô hình né đúng chỗ hay né đúng tần suất (nghi ngờ 4, gộp với hướng đường-cong của Vòng A).
- **R1** — phân loại các kiểu bịa trên giao diện (nghi ngờ 2, phần tra cứu). **R2** — chọn thầy giáo hay-bịa có tiền lệ khoa học không (nghi ngờ 5, phần tra cứu).

**Hai vòng nâng cấp còn lại (để sau 15/8, cho bài mở rộng):**
- **Vòng D** — thử một cách huấn luyện khác (học từ cặp câu bịa vs câu đã sửa): tính mới cao nhất nhưng khó thực thi nhất.
- **Vòng E** — so trực tiếp cách "sinh rồi lọc" với cách "chặn ngay lúc sinh": lấp khoảng trống, ít rủi ro.

Thứ tự khuyến nghị: **K1 → K2 → (D1, D2) → K3 (khi cần) → tính MDE → bắt tay huấn luyện**.

## 15. Nhánh nhiều-màn — ngoài phạm vi mùa này

Đã thiết kế xong + có nền khoa học đầy đủ (sắp thứ tự các màn: hỏi từng cặp "màn nào trước" → tổng hợp phiếu → phá vòng mâu thuẫn), nhưng **cố ý không làm mùa này** — nó treo trên một phép thử chưa chạy, mà ba tháng không đủ để cược vào chỗ chưa biết kết quả. Phần này có mặt để **thủ khi thầy hỏi "còn nhiều màn thì sao?"**, không phải xin duyệt chạy. Để dành bài tiếng Anh mở rộng.

## 16. Lịch, công sức, chi phí

- **Model một-màn:** ~10–15 ngày lý tưởng / ~14–21 ngày thực tế (10h/ngày). + viết bài ~10–15 ngày.
- **Lịch mùa này (~10 tuần):** tuần 1 = cổng TN0 (khoá split → pilot MDE → khoá ngưỡng) rồi mới sinh data; tuần 2–3 train hai bản + thử xuất GGUF sớm; tuần 4 đệm; tuần 5–7 eval + thống kê; tuần 8–10 viết.
- **Chi phí:** ~$70–100 (teacher API ~$1–2 · Colab ~$60–70 · local free).
- **Mẹo:** xếp train chạy **qua đêm** → giờ GPU thành thời gian rảnh miễn phí.

## 17. Hai bài báo mùa này

- **FAIR** (hạn 15/8, tiếng Anh, danh giá hơn) = **bài về MÔ HÌNH, bài chủ lực** (mô hình thành thật, Tier 1/Tier 2 trên MobileViews tiếng Anh). Khó + gấp — đây là **bài liều, cố gắng đạt**.
- **VCL** (hạn ~30/8, tiếng Việt, dễ hơn) = **bài SINH TIẾNG VIỆT** (mô hình huấn luyện bằng tiếng Anh nhưng viết hướng dẫn bằng tiếng Việt + đánh giá không cần đáp án mẫu). Đây là **bài sàn chắc ăn**.
- **Phương án lùi cứng:** nếu FAIR không kịp 15/8 → bỏ FAIR giữ VCL, mô hình gửi hội nghị khác sau. Không để canh bạc FAIR làm hỏng VCL.
- **Chưa kiểm chứng (đừng bịa):** hạn nộp VCL thật, và quy định về việc gửi hai bài dùng chung dữ liệu nguồn cho hai hội nghị — phải đọc kỹ trước khi nộp.

## 18. Rủi ro lớn nhất

Không nằm ở kỹ thuật mà ở chỗ **tính mới đặt cược vào đúng một câu hỏi (Tier 2) có thể ra rỗng.** Phòng ngừa: (1) chạy Tier 1 sớm (bảo hiểm, gần luôn có số đẹp); (2) nói thẳng với thầy khả năng Tier 2 null ngay từ đề cương; (3) mốc kiểm tra ở 2/3 thời gian — nếu Tier 1 chưa ổn thì hạ Tier 2 xuống mục phụ; (4) chạy TN7 dose-response làm bằng chứng bổ sung.

---

# BẢN ĐỒ FILE (khi cần đào sâu con số cụ thể)

- **Thiết kế tự-đủ:** `report/54` (pipeline + thước đo + thí nghiệm + phụ lục kỹ thuật).
- **Ngưỡng đã khoá:** `report/56` (pre-registration).
- **Giữ gì/đổi gì nếu rảnh:** `report/63`. **Thiết kế lại từ trang trắng:** `report/64`. **Tự phản biện 6 nghi ngờ + plan K/D/R:** `report/65`.
- **Ba vòng research:** `report/66` (A risk-coverage) · `report/67` (C VH+OCR) · `report/68` (B template). Nền đã verify: `report/61` (+ bản dễ hiểu `report/62`).
- **Trạng thái tổng:** `report/00`. **Kế hoạch 2 bài:** `report/KE_HOACH_2_BAI_BAO`. **Config khi code:** `report/53`.

> Bản này là ảnh chụp tại 18/7/2026. Khi mâu thuẫn: report/54 (thiết kế) + report/56 (ngưỡng) + report/65 (đường-găng hiện tại) là nguồn-sự-thật.
