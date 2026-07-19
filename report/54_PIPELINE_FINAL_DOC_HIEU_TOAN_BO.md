# Luận văn: xây một mô hình nhỏ biết "thành thật" khi hướng dẫn sử dụng phần mềm

> File này viết để đọc một lần là hiểu trọn luận văn — không cần đọc thêm file nào khác. Các file report/50, 52, 53, 55, 43 là nhật ký chi tiết của từng vòng tranh luận/kiểm chứng phía sau — chỉ cần mở khi muốn tra lại vì sao một quyết định cụ thể được chốt như vậy.
>
> **Nếu mục tiêu là TRÌNH BÀY / THUYẾT PHỤC THẦY:** đọc và trình bày "🎓 TRANG DÀNH CHO BUỔI GẶP THẦY" ngay dưới đây trước tiên — nó trả lời thẳng câu thầy đã phê ("chưa thấy MODEL đâu"), dài ~2 trang. Các phần sau là chỗ để đào sâu khi thầy hỏi kỹ.
>
> **Nếu buổi gặp cần duyệt PIPELINE + THƯỚC ĐO + BỘ THÍ NGHIỆM để chạy ngay:** bốn mục xương sống, đọc theo thứ tự này —
> 1. **"Ý tưởng cốt lõi"** + **"Toàn bộ luồng, tóm trong một sơ đồ"** → pipeline.
> 2. **"Đo thành công thế nào"** + **"Bộ thước đo đầy đủ"** → thước đo (lời thường trước, hộp kỹ thuật kèm công thức/citation sau).
> 3. **"Bộ thí nghiệm đầy đủ — thứ sẽ chạy ngay tuần sau"** → 7 thí nghiệm + ngưỡng đậu/rớt. ⚠️ Đây là bộ **của khung mô hình hiện tại**; bộ **E1–E16** trong `report/43`/`report/47` là của **khung prompting CŨ đã bị thầy bác** — **đừng trình bộ đó**.
> 4. **"Nhánh nhiều màn hình"** → 🚩 **ngoài phạm vi mùa này**, chỉ để thủ khi thầy hỏi, **không xin duyệt chạy**.
>
> **Trước khi chạy bất kỳ dòng lệnh tốn tiền nào:** xem mục "Thứ tự bắt buộc…" — freeze split + khoá ngưỡng phải xong TRƯỚC, kể cả trước pilot. Ô **[MDE = ___ pp]** hiện còn trống, phải điền bằng số liệu pilot rồi commit lần hai.

---

## 🎓 TRANG DÀNH CHO BUỔI GẶP THẦY — trình bày phần này trước

> Mục tiêu của trang: trong ~10 phút đầu buổi gặp, tháo gỡ đúng mối lo của thầy ("chủ yếu là gọi API + so chuỗi, chưa có mô hình học viên tự train") và chỉ rõ **đâu là mô hình do học viên fine-tune**. Trình bày theo đúng thứ tự bảy mục đầu; mục 8 là bản tra nhanh để dùng khi thầy cắt ngang, không đọc tuần tự.

**Phê bình của thầy (bản cũ):** *"Luận văn chủ yếu là gọi API mô hình có sẵn (gpt-4o-mini) rồi so khớp embedding — chưa thấy mô hình nào do chính học viên huấn luyện."* Quy định đào tạo thạc sĩ của trường yêu cầu luận văn phải có một mô hình như vậy.

**Trả lời gọn:** Bản mới **fine-tune một mô hình thị giác–ngôn ngữ (VLM) Qwen2.5-VL-3B** làm bộ sinh hướng dẫn. Huấn luyện bằng **supervised fine-tuning với LoRA adapter** (đóng băng vision encoder, chỉ cập nhật adapter trên nhánh ngôn ngữ), nên có đầy đủ tạo tác của một quá trình train thật: trọng số adapter thay đổi, loss giảm theo epoch, hai checkpoint độc lập, và một bảng đo hành vi trước/sau. **Chính mô hình này là artefact trung tâm của luận văn**; gpt-4o-mini và các thuật toán còn lại chỉ là công cụ trong khâu **tổng hợp dữ liệu huấn luyện**, không có mặt trong inference cuối.

> **🔖 Chú giải nhanh thuật ngữ** (dành cho người đọc không chuyên — thầy có thể bỏ qua). Trang này dùng thuật ngữ chuẩn ngành để nói chuyện với hội đồng; bảng dưới dịch nhanh sang lời thường:
>
> | Thuật ngữ | Nói nôm na |
> |---|---|
> | VLM (mô hình thị giác–ngôn ngữ) | Mô hình AI vừa "nhìn" được ảnh vừa viết ra chữ |
> | Fine-tune / SFT (supervised fine-tuning) | Huấn luyện tiếp một mô hình có sẵn trên dữ liệu của mình để đổi hành vi nó |
> | LoRA adapter | Chỉ gắn thêm và dạy một phần nhỏ, đóng băng phần còn lại → rẻ, chạy được máy yếu |
> | Vision encoder | Phần "mắt" của mô hình (chuyên đọc ảnh) — ở đây giữ nguyên, không đụng tới |
> | Epoch | Một lượt mô hình học đi hết toàn bộ dữ liệu huấn luyện đúng một lần (ở đây chạy 3 epoch) |
> | Loss (điểm-sai) / loss curve | Con số đo mô hình đang sai bao nhiêu; đường loss đi xuống dần qua các epoch = bằng chứng mô hình thật sự đang học |
> | Checkpoint | Bản lưu lại của mô hình tại một thời điểm huấn luyện — tải lại được để chạy hoặc học tiếp; luận văn có hai checkpoint độc lập |
> | Inference (suy luận) | Lúc mô hình chạy thật để trả lời người dùng, SAU khi đã huấn luyện xong (khác với lúc học) |
> | Teacher / Student | Mô hình lớn (gpt-4o-mini) tạo dữ liệu mẫu / mô hình nhỏ được dạy lại từ dữ liệu đó |
> | Silver labels | Dữ liệu mẫu do máy tự sinh (đối lại "gold" = do người soạn) |
> | View Hierarchy (VH) | Bản mô tả máy-đọc-được liệt kê chính xác các nút/phần tử thật đang có trên màn hình |
> | Verifier | Bộ kiểm tra độc lập (ở đây là thuật toán đối chiếu với VH) |
> | Faithfulness / bịa | Độ trung thực — không nhắc tới nút không hề tồn tại trên màn hình |
> | %fallback | Tỉ lệ bước bị thay bằng câu mô tả chung chung (vì phát hiện bịa) |
> | Held-out theo app | Tách hẳn một số ứng dụng chỉ để chấm, mô hình không hề thấy lúc học |
> | On-device inference | Chạy thẳng trên máy người dùng, không cần internet/máy chủ |
> | Ablation | Bản đối chứng cố tình bỏ một yếu tố, để đo yếu tố đó đóng góp bao nhiêu |
> | Null (kết quả rỗng) | Không đủ bằng chứng thống kê để nói có khác biệt |
> | Pre-registration (đăng-ký-trước) | Khoá sẵn ngưỡng thắng/thua + cách diễn giải TRƯỚC khi nhìn số kết quả |
> | Exact sign-flip test | Cách kiểm định thống kê chính xác cho mẫu nhỏ (liệt kê đủ mọi khả năng thay vì ước lượng) |
> | MDE (mức phát hiện tối thiểu) | Với cỡ mẫu đang có, khác biệt phải lớn cỡ nào thì thí nghiệm mới đủ sức nhìn thấy. MDE càng lớn thì thí nghiệm càng "cận thị" |
> | QLoRA | LoRA + nén mô hình gốc xuống 4-bit cho nhẹ máy — cách chạy mặc định ở đây, để card yếu nhất cũng train được |
> | G | Số **cụm** trong thống kê. Ở đây một cụm = một ứng dụng, nên **G = 12** nghĩa là 12 ứng dụng test |
> | Arm (nhánh) | Một bản mô hình đem ra so trong thí nghiệm (Student · Student-RAW · Teacher-BASE) |
> | GGUF | Một định dạng file mô hình chạy được nhẹ trên máy không có GPU — cần nó để chấm điểm miễn phí trên laptop |
> | Holm | Cách siết ngưỡng khi kiểm nhiều giả thuyết cùng lúc (kiểm càng nhiều thì càng dễ ăn may, nên phải siết). "Family" = danh sách các phép kiểm bị siết chung |
> | Step-SR (Step Success Rate) | Tỉ lệ bước làm đúng so với quỹ đạo vàng — chỉ dùng ở nhánh nhiều màn |
> | PMR | Tỉ lệ quy trình được sắp đúng trọn vẹn — chỉ dùng ở nhánh nhiều màn |
> | Estimand | Đại lượng ta thật sự muốn ước lượng (khác với con số đo được) |
> | Cohen's κ (kappa) | Chỉ số chuẩn đo mức đồng thuận giữa hai người/hai bộ chấm, đã trừ phần đồng thuận do ăn may |

### 1. Phân định "công cụ có sẵn" và "mô hình học viên tự train" — để thầy khỏi phải truy

Lời phê của thầy quy về đúng một câu: *trong hệ này, cái gì là của em?* Bản cũ không trả lời được vì mọi thành phần đều là đồ có sẵn ghép lại. Mục này trả lời bằng cách chỉ thẳng vào một thành phần duy nhất, và đưa ra sẵn tiêu chí để thầy tự kiểm chứng thay vì phải tin lời.

**Nếu chỉ có 60 giây:** trình bảng phân định + ví dụ chạy một mẫu ngay dưới. Ba mục còn lại (đường ranh giới ngay trên, câu truy sâu và tạo tác ở dưới) chỉ mở khi thầy hỏi tới.

#### Đường ranh giới dùng để phân loại

Một thành phần chỉ được tính là **"mô hình do học viên huấn luyện"** khi trả lời được **có** cho cả ba câu:

1. **Nó có trọng số** (tham số học được) không?
2. Những trọng số đó **có thay đổi vì dữ liệu của luận văn này** không?
3. Cái thay đổi đó **có đo được** không — trước/sau khác nhau ở đâu, khác bao nhiêu?

Tiêu chí này cố ý đặt cao hơn mức cần thiết: nó loại luôn cả những thành phần *có* dùng mạng nơ-ron nhưng chỉ chạy ở dạng đóng băng (mục "câu thầy có thể truy tiếp" dưới đây nói rõ). Toàn hệ chỉ có **đúng một** thành phần qua được cả ba câu.

#### Bảng phân định

| Thành phần | Vai trò trong luận văn | Có trọng số? | Trọng số đổi vì luận văn? | Kết luận |
|---|---|---|---|---|
| gpt-4o-mini (teacher) | Sinh silver labels (hướng dẫn nháp) để tạo tập SFT — chỉ chạy ở khâu data, **không có trong inference cuối** | Có, nhưng nằm trên máy chủ OpenAI, không ai đụng được | **Không** — gọi qua API, luận văn không sửa được một tham số nào | Công cụ có sẵn |
| Matcher đối chiếu View Hierarchy | Dò bước bịa để lọc dữ liệu, bằng cách so nghĩa tên nút với VH | Có (mô hình nhúng `nomic-embed-text`), nhưng **đóng băng** | **Không** — chỉ dùng như một hàm đo khoảng cách, không huấn luyện gì | Công cụ có sẵn |
| Rewrite template | Thay đoạn bịa bằng mô tả chung chung | **Không** — khuôn mẫu chữ cố định, không gọi LLM | Không | Đoạn mã tất định |
| **Qwen2.5-VL-3B (student)** | **Bộ sinh hướng dẫn — mô hình đích, inference on-device** | **Có — LoRA adapter trên nhánh ngôn ngữ** | **Có — cập nhật bằng chính tập SFT do luận văn tạo ra** | **★ MÔ HÌNH HỌC VIÊN TỰ FINE-TUNE (SFT-LoRA)** |

Đọc bảng theo cột "Trọng số đổi vì luận văn?": chỉ có đúng một ô **Có**. Đó là câu trả lời cho "mô hình của em đâu".

#### Ví dụ: một mẫu dữ liệu đi qua cả bốn thành phần

Lấy một màn hình thật trong bộ dữ liệu — màn chính của một ứng dụng nghe podcast, câu hỏi *"How do I turn on notifications for new episodes?"*. Theo dõi xem từng thành phần làm gì với nó:

**① Thầy giáo (gpt-4o-mini) — công cụ có sẵn.** Nhận ảnh + câu hỏi, không được xem VH. Viết ra bản nháp:

```
1. Tap "Settings"
2. Tap "Preferences"          ← bịa: màn này không có nút nào tên vậy
3. Toggle "New episode alerts"
```

**② Matcher — công cụ có sẵn, đóng băng.** Đối chiếu từng tên nút với VH của màn đó. `"Settings"` khớp; `"New episode alerts"` khớp; `"Preferences"` không khớp với bất kỳ phần tử nào (khoảng cách vượt ngưỡng đã chốt) → **đánh dấu bước 2 là bịa**. Nó chỉ *chỉ ra chỗ sai*, không sửa, không học được gì từ việc này.

**③ Rewrite template — đoạn mã tất định.** Thay đúng bước bị đánh dấu bằng một câu chung chung nhưng không sai sự thật:

```
1. Tap "Settings"
2. Look for the option on this screen that matches what you need
   for this step, and tap it.          ← đã viết lại, không đoán nút khác
3. Toggle "New episode alerts"
```

Ba bước trên **kết thúc ở đây**. Sản phẩm của chúng không phải một mô hình, mà là **một dòng dữ liệu huấn luyện** — đúng dòng `mv__aucommixfm4sss_s1__q0` in trong Phụ lục D, Bước 6. Vài nghìn dòng như vậy hợp thành tập SFT.

**④ Học trò (Qwen2.5-VL-3B) — thành phần duy nhất được huấn luyện.** Nuốt vài nghìn dòng như trên, chạy 3 epoch, cập nhật LoRA adapter. Sau đó, khi gặp một màn hình của **ứng dụng nó chưa từng thấy bao giờ**, không có thầy giáo, không có matcher, không có VH, không có mạng, nó tự viết hướng dẫn và tự biết chuyển sang lối nói chung chung ở chỗ không chắc. Không ai bảo nó làm vậy tại thời điểm đó; thói quen ấy nằm trong trọng số.

**Phép thử để thấy rõ ranh giới:** xoá sạch ba thành phần ① ② ③ khỏi máy sau khi huấn luyện xong — hệ thống vẫn chạy y nguyên, vì sản phẩm giao đi chỉ gồm mô hình học trò. Xoá ④ thì không còn gì để giao nữa. Ba thành phần đầu là giàn giáo: dựng lên để xây, xây xong thì tháo.

#### Câu thầy có thể truy tiếp — trả lời sẵn

- **"So-embedding cũng là mạng nơ-ron mà, sao em bảo nó không phải mô hình?"**

  → **Đúng, `nomic-embed-text` là một mạng nơ-ron thật — không hề giấu điều này.** Nó nhận vào hai đoạn chữ (ví dụ tên nút `"Preferences"` và tên nút `"Settings"`), và trả ra đúng **một con số** đo hai chữ đó giống nghĩa nhau bao nhiêu (ví dụ 0.31 — thấp, coi như không khớp). Việc nó *là mạng nơ-ron* không phải điều gây tranh cãi.

  **Điều gây tranh cãi là: nó có được HUẤN LUYỆN trong luận văn này không?** Câu trả lời là không, và đây mới là chỗ khác biệt với Qwen. Hình dung thế này: `nomic-embed-text` được tải về từ kho có sẵn, dùng y nguyên suốt từ đầu tới cuối — **không hề có bước nào "dạy lại" nó bằng dữ liệu của luận văn.** Nó chỉ đứng đó làm một phép so sánh có sẵn, giống hệt việc bạn lấy một cái thước đã có vạch sẵn ra đo hai vật, chứ không phải tự tay khắc vạch lên thước.

  Ráp lại với **ba câu hỏi đã đặt ra ở đầu mục 1** ("có trọng số không / trọng số có đổi vì dữ liệu luận văn không / cái đổi đó có đo được không"): `nomic-embed-text` trả lời **có** cho câu 1 (nó có trọng số, đúng là mạng nơ-ron), nhưng trả lời **không** cho câu 2 (trọng số của nó không hề nhúc nhích, dù có huấn luyện Qwen bao nhiêu lần đi nữa). Trượt ở câu 2 là đủ để loại khỏi danh sách "mô hình do học viên tự train" — không cần đợi tới câu 3.

  **Vì sao phải kể chi tiết này ra, thay vì chỉ nói gọn "đây là thuật toán so khớp"?** Vì nói vậy không sai, nhưng thiếu — và một thầy hướng dẫn kỹ tính hoàn toàn có thể tự tra ra `nomic-embed-text` là một mạng nơ-ron thật. Nếu điều đó bị phát hiện *sau khi* bạn đã lỡ nói "không phải mô hình, chỉ là thuật toán", thầy sẽ nghi ngờ luôn cả những chỗ khác trong luận văn có bị nói giảm nói tránh tương tự không — dù chỗ đó bản chất không sai. Nói hết ra ngay từ đầu, kèm lý do vì sao nó vẫn không tính là "mô hình của học viên", thì vừa an toàn vừa cho thấy bạn hiểu rõ ranh giới mình đang vẽ, không phải né tránh.

- **"Vậy chẳng phải gpt-4o-mini viết hộ hết rồi sao?"**

  → **Không — và có một phép thử cụ thể để kiểm tra điều đó, không chỉ là lý lẽ suông.**

  Băn khoăn của câu hỏi này rất hợp lý: nếu Qwen chỉ học cách "bắt chước" gpt-4o-mini, thì công của luận văn chẳng qua là nén một AI có sẵn vào một AI nhỏ hơn — không có gì gọi là "học trò tự thành thật" cả. Đây đúng là điều Tier 2 (mục 4 ngay dưới) được dựng ra để kiểm tra thẳng.

  Cách kiểm: đặt **Qwen sau khi train** (học trò) đối đầu trực tiếp với **chính gpt-4o-mini chạy thô, không qua lọc** (gọi là "thầy giáo trần" — bảng "Bốn cái tên cần nhớ" ở mục "Ý tưởng cốt lõi" phía dưới phân biệt rõ bốn nhân vật này). Cả hai cùng bị bịt VH lúc trả lời, tức là cùng một đề thi, không ai được ưu ái.

  Bây giờ hình dung điều gì xảy ra nếu nghi ngờ "Qwen chỉ chép lại thầy giáo" là đúng: Qwen học từ dữ liệu do gpt-4o-mini viết ra, nên nếu nó chỉ đang bắt chước, khi gặp màn hình mới nó sẽ viết ra **những kiểu câu giống hệt gpt-4o-mini hay viết** — kể cả những chỗ gpt-4o-mini có xu hướng bịa. Hai bên sẽ **ra điểm gần như bằng nhau**, vì bản chất chỉ là một bản sao của bản gốc. Đó chính xác là kịch bản luận văn **thua** ở Tier 2 — và nó *có thể xảy ra thật*, không ai đảm bảo trước.

  Nhưng có một lý do kỹ thuật khiến Qwen **không thể** đơn thuần là bản sao: nó **chưa bao giờ được nhìn thấy bản nháp thô** của gpt-4o-mini. Thứ nó học chỉ là bản đã bị lọc — chỗ nào gpt-4o-mini bịa thì đã bị thay bằng câu mô tả chung chung trước khi đưa cho Qwen học (xem lại ví dụ "Preferences" ở phần ①②③ phía trên). Tức là **dữ liệu huấn luyện của Qwen là một thứ mà bản thân gpt-4o-mini, nếu chỉ gọi thẳng qua API, không bao giờ tự viết ra được** — vì gpt-4o-mini gọi API luôn kèm khả năng bịa, còn bản đã lọc thì không.

  Nên câu trả lời gọn: nếu Qwen thắng ở Tier 2, đó là bằng chứng nó học được *thói quen* né bịa từ tấm gương đã lọc, chứ không phải chỉ ghi nhớ lại giọng văn của thầy giáo. Còn nếu Qwen thua (ra điểm ngang gpt-4o-mini trần), đó là tín hiệu trung thực rằng việc "nội-tại-hoá" chưa xảy ra — và đây chính là lý do Tier 2 được thiết kế để **có thể null**, không phải một phép thử chắc thắng dựng lên cho có.
- **"Sao không huấn luyện luôn cái matcher cho nó cũng là mô hình của em?"** → Đã cân nhắc và loại có lý do (Phụ lục A, hướng 2): một mô hình học phát hiện bịa từ dữ liệu tự bơm lỗi sẽ chỉ học lại đúng cách bơm lỗi của chính mình, không chắc bắt được lỗi bịa thật. Giữ matcher ở dạng thuật toán đóng băng vừa tránh cái bẫy đó, vừa giữ cho ranh giới "đâu là mô hình của học viên" sạch sẽ — chỉ có đúng một thứ được huấn luyện, nên không có chỗ nào cho việc vừa đá bóng vừa thổi còi.
- **"Fine-tune bằng LoRA thì có tính là train không, hay chỉ là dùng lại model có sẵn?"** → Có tính. LoRA vẫn là huấn luyện có giám sát thật: có tập dữ liệu, có hàm mất mát, có lan truyền ngược, có gradient cập nhật tham số qua từng bước, có tập held-out để theo dõi. Điểm khác duy nhất so với huấn luyện toàn phần là **số tham số được cập nhật ít hơn** (chỉ adapter, phần gốc đóng băng) — một lựa chọn về chi phí, không phải một loại "train giả". Đây cũng là cách làm tiêu chuẩn của hầu hết công trình fine-tune VLM gần đây trong điều kiện một GPU (tiền lệ trực tiếp: ZonUI-3B).

#### Tạo tác chứng minh có train thật — đưa thầy xem trực tiếp

Bốn thứ dưới đây **không thể có** nếu chỉ gọi API. Chúng sẽ có sau khi chạy xong (hiện chưa chạy — không điền số trước):

| # | Tạo tác | Cụ thể là gì | Chứng minh điều gì |
|---|---|---|---|
| 1 | **Δ trọng số adapter** | File adapter trước/sau huấn luyện, so từng ma trận LoRA → khác 0 ở đúng các lớp đã chọn (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate/up/down_proj`), và **bằng 0 tuyệt đối ở nhánh thị giác** vì đã đóng băng | Có tham số thật sự bị sửa, và sửa đúng chỗ đã thiết kế |
| 2 | **Loss curve theo epoch** | Đồ thị điểm-sai giảm dần qua 3 epoch, đo trên tập held-out theo ứng dụng (không phải trên chính dữ liệu đã học) | Mô hình đang học ra quy luật dùng được cho ứng dụng lạ, không phải học thuộc |
| 3 | **Hai checkpoint độc lập** | Hai thư mục file trọng số: `Student` (học từ data đã lọc) và `Student-RAW` (học từ data thô) — cùng cấu hình, cùng số mẫu, cùng số epoch, khác đúng một biến là dữ liệu | Đây là một **thí nghiệm có đối chứng**, không phải một lần chạy lấy kết quả đẹp |
| 4 | **Bảng delta hành vi** | Tỉ lệ bịa và %fallback của: mô hình gốc chưa fine-tune → `Student-RAW` → `Student`, trên 12 ứng dụng test | Việc huấn luyện tạo ra **thay đổi hành vi đo được**, và tách được phần công của bước lọc |

Trong bốn thứ trên, nên nhấn vào tạo tác số 3 khi trình bày: **hai checkpoint chỉ khác nhau ở dữ liệu học** cho thấy đây là một thí nghiệm có đối chứng, chứ không phải một hệ thống ghép sao cho chạy được rồi thôi.

### 2. Đóng góp trí tuệ của học viên (không phải "lắp ráp công cụ")
1. **Quy trình tổng hợp dữ liệu chống-bịa** dùng một verifier ngoài, có cấu trúc (View Hierarchy) cho một hành vi rủi-ro-cao — bịa tên nút dẫn tới thao tác sai trên hệ thống thật, khác hẳn hallucination mô tả ảnh thông thường.
2. **Một mô hình on-device do học viên fine-tune,** giữ được hành vi né-bịa khi inference không có mạng và không có verifier.
3. **Một câu hỏi nghiên cứu chưa ai đặt** cùng thiết kế thí nghiệm hai tầng để trả lời (mục 4).

### 3. Tính mới — nói thật, không thổi phồng (thầy chắc chắn hỏi "khác gì mấy bài đã có")
Khung generate → filter → retrain **không mới** (STaR/RFT 2022, KnowAda NAACL 2025, BLIP CapFilt ICML 2022, VGA EMNLP-Findings 2024 — luận văn cite đầy đủ, không giấu điểm trùng). Delta thật sự còn lại đúng **hai điểm**:
- **(a)** verifier là **nguồn ngoài, có cấu trúc** (VH) thay vì self-probing như KnowAda (mô hình tự hỏi–tự chấm), và áp cho một hành vi high-stakes.
- **(b) câu hỏi trọng tâm chưa ai đặt:** hành vi faithfulness đó có **được nội-tại-hoá vào trọng số student** không, khi inference **tắt hẳn VH** (held-out theo app)? Đây là câu hỏi **có thể ra kết quả null** — chính vì vậy nó là câu hỏi nghiên cứu thật, không phải kết luận biết trước.

### 4. Thiết kế hai tầng trả lời câu hỏi trọng tâm (điểm thuyết phục nhất về phương pháp)

> **Quy ước tên gọi dùng thống nhất từ đây tới hết tài liệu:** hai tầng thí nghiệm gọi là **Tier 1** và **Tier 2**, không gọi kèm biến thể nào khác. Trong bảng thí nghiệm chúng mang mã **TN1** và **TN2**.
>
> **🔒 LUẬT VÀNG VỀ VH — phát biểu chuẩn, mọi chỗ khác trong tài liệu phải hiểu theo câu này:** View Hierarchy vào hệ ở **đúng ba chỗ**: (1) lọc dữ liệu huấn luyện, (2) lớp viết-lại của hệ deploy đầy đủ *khi máy người dùng có sẵn VH*, (3) khâu chấm điểm. **Student không bao giờ thấy VH ở đầu vào** — không lúc train, không lúc suy luận. Và **phép đo `f` luôn chấm trên output thô ở CẢ hai tier** (lý do: chỗ truy ① dưới bảng thí nghiệm).
>
> Khác biệt giữa hai tier **không nằm ở VH**, mà nằm ở **đem so với ai**: Tier 1 so hai bản student với nhau, Tier 2 so student với teacher trên app chưa từng thấy.

| Tầng | So sánh | Điều kiện lúc CHẤM `f` | Ý nghĩa |
|---|---|---|---|
| **Tier 1 — lưới an toàn** (gần chắc dương) | `Student` (data lọc) vs `Student-RAW` (data thô), cùng kiến trúc | Chấm trên output thô | Existence proof: **có mô hình học viên tự train + việc lọc data tạo hiệu ứng đo được** → đã thoả yêu cầu của thầy, độc lập với Tier 2 |
| **Tier 2 — trụ chính** (có thể null) | `Student` vs `Teacher-BASE` (gpt-4o-mini) | Chấm trên output thô, **held-out theo app** | Câu hỏi mới: faithfulness có nội-tại-hoá vào student không |

Hai tier **báo cáo độc lập** để một null ở Tier 2 không kéo sập Tier 1. Ngưỡng pass/fail và cách diễn giải cả ba kết cục (pass đầy đủ / pass một phần / null) đã **pre-register trước khi nhìn số** (`report/56`).

### 5. Đủ ngưỡng luận văn thạc sĩ → **Đủ**
Thông tư 23/2021/TT-BGDĐT không đòi hỏi SOTA; đóng góp dạng **constructive/technological** có thiết kế nghiêm túc là hợp lệ, và có tiền lệ chấp nhận nghiên cứu đăng-ký-trước có khả năng null (NeurIPS 2021 Pre-registration Workshop). Hai điểm mạnh phương pháp (chặt hơn phần lớn luận văn cùng cấp): **pre-registration** (freeze app split + ngưỡng + diễn giải trước khi nhìn kết quả) và **exact sign-flip test cho mẫu nhỏ** (G=12: liệt kê đủ 2¹²=4.096 tổ hợp dấu, không xấp xỉ tiệm cận).

### 6. Khả thi về thời gian & chi phí → **Có**
Trong **<3 tháng**, chi phí **~$70–100** (chủ yếu Colab Pro/Pro+; teacher API chỉ ~$1–2), một laptop + tài khoản Colab. QLoRA 4-bit chạy được cả trên T4 16GB, và có tiền lệ trực tiếp (ZonUI-3B, 2026) fine-tune đúng dòng Qwen2.5-VL-3B trên một GPU 24GB phổ thông.

### 7. Điều học viên chủ động khai trước (để không bị hiểu là bào chữa về sau)
Tier 2 (trụ chính) **có thể ra null**. Nếu vậy, đây là một phát hiện trung thực về **giới hạn generalization** của phương pháp, **không phải** luận văn thất bại — vì Tier 1 đứng độc lập và gần chắc dương, đủ chứng minh phần thầy yêu cầu. Học viên xin trình đề cương với khả năng null này được **khai trước ngay từ đầu**, thay vì đợi có số xấu mới giải thích.

### 8. Câu thầy hay hỏi — trả lời sẵn

> Bảy mục trên là kịch bản trình bày. Mục này là bản tra nhanh khi thầy cắt ngang giữa chừng. Tiêu chí xếp nhóm: câu nào **tài liệu đã trả lời ở chỗ khác** thì đây chỉ ghi một dòng chốt để nói ra miệng, cộng con trỏ; câu nào **chưa có ở đâu** thì viết đủ tại đây.

**Nhóm A — đã có chỗ trả lời, đây chỉ là câu chốt để nói ra miệng:**

- **"Nó khác gì mấy bài đã có?"** → "Công thức sinh-lọc-huấn-luyện-lại không phải em phát minh, em cite đủ. Delta của em đúng hai điểm: bộ lọc dùng nguồn ngoài có cấu trúc thay vì để mô hình tự chấm mình, và một câu hỏi chưa ai đặt về việc tắt hẳn bộ kiểm tra lúc dùng thật." → **mục 3** (đầy đủ: Phụ lục B).
- **"Nếu kết quả null thì sao?"** → "Tier 1 vẫn đứng độc lập và giữ giá trị luận văn; null ở Tier 2 đã được khai trước và pre-register nên vẫn công bố được." → **mục 7**.
- **"Mô hình của em đâu?"** → "Qwen2.5-VL-3B, em fine-tune bằng SFT-LoRA; deliverable là checkpoint chạy on-device. gpt-4o-mini chỉ là teacher ở khâu tạo data, không nằm trong inference cuối." → **mục 1**.
- **"Khác gì distillation thông thường?"** → "Em không copy trực tiếp output teacher. Student chỉ học từ phần đã lọc bịa bằng verifier ngoài, tức là học từ một thứ mà bản thân teacher gọi qua API không bao giờ tự viết ra được." → **mục 1** (câu hỏi "gpt-4o-mini viết hộ hết rồi sao?").
- **"Đề tài có đủ phạm vi cho thạc sĩ không?"** → "Đủ — rủi ro là hơi rộng chứ không hẹp: bốn khối việc, đủ ba trụ xây/đo/phát hiện. Em đã chủ động cắt nhiều-màn, học-tăng-cường và đua SOTA để vừa 3 tháng." → mục **"Vậy có đủ để bảo vệ một luận văn thạc sĩ không?"**. *(Lưu ý phân biệt: mục 5 ở trên trả lời về **chất lượng** đóng góp — có cần SOTA không; mục này trả lời về **khối lượng** — có đủ việc không. Thầy có thể hỏi một trong hai, hoặc cả hai.)*

**Nhóm B — chưa có ở đâu khác, chỉ nằm ở đây:**

- **"Tại sao em chọn đề tài này?"** → Ba lý do: (1) nhu cầu có thật — người dùng kẹt ở một màn hình, chụp ảnh rồi hỏi "làm sao?" là hành vi tự nhiên; (2) bài toán khó chưa ai giải đúng chỗ — không có đáp án chuẩn để chấm, lại phải chống đúng kiểu bịa tên nút khiến người dùng bấm nhầm, điểm giao ba yếu tố này còn trống; (3) đúng thời điểm và vừa sức — VLM nhỏ nay đủ khoẻ, LoRA cho phép tự train thật với ~$100, và mô hình on-device đáp đúng yêu cầu của thầy. *(Chi tiết: mục "Vì sao chọn đúng đề tài này".)*
- **"Sao không train from scratch hoặc dùng model lớn hơn?"** → Hai lý do. Ràng buộc compute (laptop + Colab) không cho phép pretrain from scratch — cái này mục 6 đã nói. Nhưng lý do thứ hai mới là chính: **mục tiêu vốn là mô hình chạy trên máy người dùng**, nên train ra một model to hơn là đi ngược đề tài, chứ không phải làm không nổi.
- **"Tiếng Việt thì sao?"** → Có một bài thứ hai cho student sinh hướng dẫn **bằng tiếng Việt** (cross-lingual transfer); smoke-test ngay tuần đầu để xác nhận khả thi.
- **"18 ứng dụng để dạy có ít quá không?"** → 18 chỉ là phần đã qua kiểm tra chất lượng từ bộ pilot ban đầu, không phải số cuối. Việc mở rộng **đã chạy xong 12/7**: thêm 220 ứng dụng / 498 màn hình mới, kiểm tra rò rỉ chéo với nhóm test cho **0 ca** (so cả theo tên lẫn theo ảnh) → tổng ~574 màn, đủ dựng ~1.700–2.870 mẫu. 12 ứng dụng test giữ nguyên, không mở rộng, vì cần là nguồn chấm điểm đáng tin nhất (12 nghe ít, nhưng đó là 40% của bộ đã qua kiểm tra chất lượng — xem mục "Vì sao chia 18/12"). Có van an toàn: tính MDE bằng số liệu pilot **trước** khi khoá; nếu MDE quá lớn thì đổi cách chia thành 15 app train / 15 app test — làm trước khi khoá, không sửa sau khi đã nhìn kết quả. *(MDE là gì: mục "Đo thành công thế nào".)*
- **"Sao không lấy nhiều dữ liệu hơn nữa — kho có tới 600 nghìn màn?"** → (Nói cho chính xác: bản công khai là 600 nghìn, nhưng phần lấy được ngay bằng code hiện có là ~231 nghìn — vẫn thừa sức so với nhu cầu.) Không phải vì hết dữ liệu. Lý do là thời gian (mỗi app thêm vào tốn công kiểm tra chất lượng), việc kiểm tra chất lượng không tự nhân rộng miễn phí, và câu hỏi nghiên cứu ở Tier 2 không cần quy mô khổng lồ để trả lời. Rủi ro thật của đề tài là quá tải tiến độ, không phải thiếu dữ liệu.

> Sau khi thầy đồng ý hướng, toàn bộ phần dưới (từ "Vì sao phải đổi hướng") là chi tiết triển khai + tài liệu trả lời khi thầy đào sâu.

---

## Vì sao phải đổi hướng

Bản đầu tiên của luận văn làm việc như sau: gọi một AI có sẵn (gpt-4o-mini của OpenAI) để đọc ảnh màn hình và viết hướng dẫn, rồi dùng một thuật toán so sánh văn bản để kiểm tra AI đó có bịa ra tên nút không tồn tại hay không. Cách làm này chạy tốt, nhưng khi trình bày, thầy hướng dẫn nhận xét thẳng: đây chủ yếu là *gọi API và so sánh chuỗi ký tự* — chưa thấy đâu là phần "mô hình do chính học viên huấn luyện", trong khi quy định của trường bắt buộc luận văn thạc sĩ phải có một mô hình như vậy.

Vì thế toàn bộ phần lõi (bài toán, ba bộ dữ liệu, cách đo lường không cần đáp án mẫu) được giữ nguyên, chỉ thêm một khối mới: một mô hình thật sự được huấn luyện, đóng vai trò trung tâm của luận văn thay vì chỉ gọi API có sẵn.

Trước khi chốt bản này, hướng đi đã bị mang ra "vặn" nhiều lần — dựng lên rồi cố tình tìm cách bẻ gãy nó bằng cách tra cứu các nghiên cứu liên quan và để nhiều góc nhìn khác nhau công kích từng điểm yếu. Bảy vòng như vậy đã chạy, và không vòng nào phát hiện lỗi buộc phải đập đi làm lại — chỉ có những chỗ phải nói khiêm tốn hơn, đo thêm cho chắc, hoặc thống nhất lại một định nghĩa cho khỏi mâu thuẫn giữa các file. Đây là lý do file này có thể tự tin gọi là bản chốt (vòng thứ bảy, 2026-07-12, đã soi lại đúng bản này và report/53 — mọi phát hiện của vòng đó đã được vá thẳng vào các mục dưới đây).

---

## Bài toán là gì, nói đơn giản

Người dùng đưa cho hệ thống một tấm ảnh chụp màn hình ứng dụng, cộng với một câu hỏi kiểu "làm sao để bật thông báo cho tập mới?". Hệ thống phải trả lời bằng các bước cụ thể, kiểu "1. Chạm vào Cài đặt — 2. Chạm vào Thông báo — 3. Bật công tắc...".

Cụ thể bằng một ví dụ thật, để hình dung đúng thứ đi vào và thứ đi ra:

> **Vào:** một tấm ảnh chụp màn hình chính của một ứng dụng nghe podcast + câu hỏi *"Làm sao để bật thông báo cho tập mới?"*
>
> **Ra:** `1. Chạm vào "Settings" — 2. Chạm vào "Notifications" — 3. Bật "New episode alerts"`
>
> **Một câu trả lời hỏng trông thế nào:** `... 2. Chạm vào "Preferences" ...` — trong khi trên màn hình đó không hề có nút nào tên "Preferences". Người dùng cầm điện thoại dò mãi không thấy, hoặc tệ hơn là bấm nhầm sang một nút khác nghe na ná.

Cái khó nằm ở hai chỗ.

**Khó thứ nhất: không có đáp án mẫu để chấm.** Với hầu hết bài toán AI, người ta có sẵn một bộ "đề + đáp án đúng" do con người soạn, chấm bằng cách so đáp án. Ở đây không hề có bộ hướng dẫn "chuẩn" nào do con người soạn sẵn cho từng màn hình — mà tự soạn thì tốn hàng nghìn giờ người, ngoài tầm một luận văn. Nên phải nghĩ ra cách đo khác, không cần đáp án mẫu.

**Khó thứ hai: có một kiểu lỗi đặc biệt nguy hiểm.** AI có thể bịa ra tên một nút bấm không hề tồn tại trên màn hình đó (như "Preferences" trong ví dụ trên). Người dùng làm theo sẽ chạm vào khoảng trống hoặc bấm nhầm — hướng dẫn sai không chỉ vô dụng mà còn gây hại. Chỗ nguy hiểm là kiểu lỗi này *khó phát hiện bằng mắt thường*, vì câu "Chạm vào Preferences" đọc lên nghe hoàn toàn trơn tru và hợp lý; chỉ khi đối chiếu với đúng màn hình đó mới lòi ra là nút ấy không tồn tại.

---

## Vì sao chọn đúng đề tài này — ba lý do (câu thầy gần như chắc chắn hỏi đầu tiên)

Thầy thường mở đầu bằng hai câu: *"Tại sao em chọn đề tài này?"* và *"Nó khác gì những cái đã có?"*. Phần này trả lời câu thứ nhất một cách gọn và thật; câu thứ hai (điểm khác biệt) được trả lời riêng ở mục "Cái mới ở đây là gì" phía dưới và ở bảng so sánh đầy đủ trong Phụ lục B. Có ba lý do, xếp theo thứ tự nên trình bày cho thầy.

**Lý do một — nhu cầu có thật, không phải bài toán tự nghĩ ra cho có.** Hầu như ai cũng từng bị "kẹt" ở một màn hình ứng dụng: nhìn thấy giao diện trước mắt nhưng không biết chạm vào đâu để làm được việc mình cần. Hành vi tự nhiên nhất trong tình huống đó là chụp lại màn hình rồi hỏi "giờ phải làm gì?". Một hệ thống nhận đúng tấm ảnh màn hình *đang mở* cộng câu hỏi, rồi trả lời bằng các bước bám sát đúng màn hình đó, là thứ có ích thật cho người dùng phổ thông, người lớn tuổi, hay người mới dùng một phần mềm lạ. Đây là bài toán xuất phát từ một nhu cầu đời thường, không phải một bài toán học thuật nghĩ ra để có cái mà làm.

**Lý do hai — đây là một bài toán khoa học khó và chưa được giải đúng chỗ.** Cái khó cốt lõi đã nói ở trên: không có đáp án mẫu do người soạn sẵn để chấm, nên không thể đo bằng cách thông thường (so với đáp án chuẩn). Khó hơn nữa, có một kiểu lỗi rất đặc thù mà ít ai nghiên cứu cho đúng tình huống "viết hướng dẫn cho người đọc": AI bịa ra tên nút không tồn tại. Kiểu lỗi này nguy hiểm hơn hẳn "tả sai một chi tiết trong ảnh" thông thường, vì hậu quả là người dùng thao tác nhầm trên một hệ thống thật. Điểm giao của ba yếu tố — *sinh hướng dẫn cho người đọc* (không phải cho robot tự bấm) × *không có đáp án chuẩn* × *chống đúng kiểu bịa tên nút này* — là một khoảng trống chưa ai lấp (đã tra cứu kỹ ở mục "Cái mới ở đây là gì" và Phụ lục B).

**Lý do ba — đúng thời điểm, vừa sức, và khớp đúng yêu cầu của thầy.** Ba điều kiện chín muồi cùng lúc: (1) các mô hình thị giác–ngôn ngữ *nhỏ* nay đã đủ khoẻ để đọc được ảnh màn hình và viết hướng dẫn, thứ vài năm trước chưa làm được; (2) kỹ thuật huấn luyện nhẹ (LoRA) cho phép một học viên với laptop cá nhân và tài khoản Colab huấn luyện *thật* một mô hình như vậy với chi phí chỉ khoảng một trăm đô-la, thay vì cần cả một trung tâm máy tính; (3) và quan trọng nhất với buổi bảo vệ này — hướng đi tạo ra một mô hình chạy được ngay trên máy người dùng *chính là* thứ đáp đúng yêu cầu của thầy: luận văn phải có một mô hình do học viên tự huấn luyện, chứ không chỉ gọi công cụ có sẵn. Đề tài này vừa tận dụng lại được toàn bộ ba bộ dữ liệu và khung đo lường đã chuẩn bị từ trước, vừa gắn được một mô hình thật vào trung tâm.

---

## Ý tưởng cốt lõi: dạy một mô hình nhỏ thói quen "thành thật"

Hãy hình dung có hai nhân vật: một "thầy giáo" và một "học trò".

**Thầy giáo** là gpt-4o-mini — một mô hình AI mạnh, có sẵn, chỉ cần gọi qua mạng. Thầy giáo chỉ được nhìn ảnh màn hình và đọc câu hỏi, **không** được xem trước danh sách các nút thật sự có trên màn hình đó. Vì vậy thầy giáo đôi khi đoán bừa và bịa ra tên nút.

Sau khi thầy giáo viết xong bản nháp, có một bước kiểm tra: đối chiếu từng tên nút mà thầy giáo nhắc tới với VH của màn đó.

**View Hierarchy (VH) là gì.** Mỗi ảnh chụp màn hình Android đều đi kèm một file do chính hệ điều hành xuất ra, liệt kê mọi thứ đang hiển thị: từng phần tử là loại gì (nút bấm, ô nhập, nhãn chữ), tên hiển thị ra sao, nằm ở toạ độ nào. Đại khái:

> `[nút] "Settings" — góc trên phải` · `[nút] "Library"` · `[nút] "Search"` · `[ô nhập] "Search podcasts"` · `[nút] "Play"` …

Nếu thầy giáo viết "Chạm vào Preferences" mà VH không có phần tử nào tên gần giống vậy, ta biết chắc đó là bịa — không phải đoán, không phải hỏi ý kiến một AI khác. Đây là thứ khiến việc dò bịa ở bài toán này làm được, trong khi ở phần lớn bài toán AI khác thì rất khó.

Hai lưu ý. **Một,** bước đối chiếu không phải một AI khác, chỉ là thuật toán so khớp văn bản theo nghĩa (để "Cài đặt" vẫn khớp với "Settings"), chạy miễn phí trên máy. **Hai,** VH chỉ có lúc *chuẩn bị dữ liệu* — vì bộ dữ liệu nghiên cứu có sẵn kèm nó. Trên điện thoại thật thì không phải lúc nào cũng có, và đó chính là lý do tồn tại câu hỏi trung tâm ở cuối mục này.

Chỗ nào thầy giáo bịa, có hai cách xử lý. Cách thứ nhất — **gọi là "phương án đoán thay"** — là tra VH rồi thay tên nút bịa bằng một nút có thật nghe gần giống nhất. Cách này **đã bị loại**, vì nó rất dễ thay bằng một nút có thật nhưng sai chức năng: hướng dẫn vẫn sai, mà lần này sai một cách kín đáo, không ai nhìn ra (luận văn đo thẳng chuyện này bằng *tỉ lệ lỗi-ngầm*, xem mục "Bộ thước đo đầy đủ"). Cách thứ hai — **cách đang dùng** — là viết lại thành một câu mô tả chung chung nhưng trung thực, kiểu "Tìm và chạm vào tuỳ chọn trên màn hình phù hợp với việc bạn cần làm ở bước này." — không đoán bừa, nhưng vẫn có ích.

Sau khi có một bộ dữ liệu "đã dọn sạch" như vậy, nó được dùng để dạy cho **học trò** — một mô hình nhỏ hơn nhiều, mở mã nguồn, tên là Qwen2.5-VL-3B, đủ nhỏ để chạy ngay trên một chiếc laptop hay điện thoại, không cần gọi internet, không cần trả tiền API. Học trò được huấn luyện lại (kỹ thuật gọi là fine-tuning) sao cho khi tự viết hướng dẫn, nó tự nhiên có xu hướng thành thật — kể cả khi lúc đó không còn VH nào để đối chiếu, vì trên điện thoại thật không phải lúc nào cũng có sẵn thông tin cấu trúc màn hình đầy đủ.

Tóm lại: **thầy giáo lớn, hay bịa. Ta không dùng nguyên lời thầy giáo để dạy học trò — ta chỉ dạy học trò từ phần lời thầy giáo đã được lọc sạch bịa. Câu hỏi trung tâm của cả luận văn là: liệu thói quen thành thật đó có thật sự "ngấm" vào học trò, hay chỉ là vẻ ngoài phụ thuộc vào việc có ai đó kiểm tra hộ hay không.**

### Bốn cái tên cần nhớ — đọc kỹ bảng này thì các phần sau không rối

Từ đây trở đi tài liệu nhắc tới bốn "nhân vật" mô hình. Chúng dễ bị lẫn vì hai cặp chỉ khác nhau đúng một chi tiết, mà chính chi tiết đó lại là toàn bộ nội dung thí nghiệm:

| Gọi trong tài liệu | Thực chất là gì | Vai |
|---|---|---|
| **Thầy giáo** | gpt-4o-mini, gọi qua mạng | Viết bản nháp hướng dẫn để tạo dữ liệu dạy học trò. Chỉ có mặt lúc chuẩn bị dữ liệu, không có trong sản phẩm cuối |
| **Thầy giáo trần** (Teacher-BASE) | Vẫn là gpt-4o-mini đó, nhưng lấy nguyên bản nháp **chưa qua lọc** | Là mốc để so ở Tier 2 — tức "nếu cứ gọi API mô hình lớn như bản luận văn cũ thì được bao nhiêu điểm" |
| **Học trò** (Student) | Qwen2.5-VL-3B, học viên tự fine-tune, học từ dữ liệu **đã lọc sạch bịa** | **Sản phẩm chính của luận văn** |
| **Học trò đối chứng** (Student-RAW) | Cũng Qwen2.5-VL-3B đó, fine-tune y hệt, chỉ khác: học từ dữ liệu **thô, chưa lọc** | Bản đối chứng ở Tier 1 — có nó mới tách được "giỏi lên là nhờ lọc dữ liệu" khỏi "giỏi lên là nhờ được huấn luyện thêm nói chung" |

**Học trò và học trò đối chứng giống nhau tuyệt đối** — cùng mô hình gốc, cùng cấu hình, cùng số mẫu, cùng số vòng huấn luyện. Khác biệt duy nhất giữa chúng là dữ liệu học có qua bước lọc bịa hay không. Nhờ vậy, mọi chênh lệch đo được giữa hai bản chỉ có thể đến từ đúng bước lọc đó, không thể đổ cho nguyên nhân nào khác.

---

## Toàn bộ luồng, tóm trong một sơ đồ

```
LÚC HUẤN LUYỆN (làm một lần, offline)

  Ảnh màn hình + câu hỏi
        │
        ▼
  Thầy giáo (gpt-4o-mini, không thấy VH)
        │  viết hướng dẫn nháp — khoảng 1/4 số bước có bịa
        ▼
  Đối chiếu với VH (thuật toán, không phải AI)
        │  đúng → giữ nguyên · bịa → viết lại thành câu mô tả chung chung
        ▼
  Bộ dữ liệu đã lọc sạch  →  huấn luyện học trò (Qwen2.5-VL-3B)
                                      │
                                      ▼
                              MÔ HÌNH HỌC TRÒ  ← đây là sản phẩm chính

LÚC SỬ DỤNG THẬT (trên máy người dùng)

  Ảnh màn hình + câu hỏi  →  Học trò tự viết hướng dẫn  →  đưa cho người dùng
  (không cần thầy giáo, không cần internet, không cần VH)
```

(Con số "khoảng 1/4" trong sơ đồ trên là quan sát sơ bộ từ một lần thử nhỏ trước đây — trên một mô hình và một tập ảnh giới hạn — dùng để hình dung quy mô vấn đề, không phải một tỉ lệ đã đo chính thức trên toàn bộ dữ liệu. Con số thật sẽ được đo lại khi chạy bản chính.)

---

## Cái mới ở đây là gì — nói thật, không phóng đại

Nếu chỉ tìm hiểu sơ, công thức "cho AI viết, kiểm tra, lọc bỏ chỗ sai, rồi lấy phần sạch dạy lại một AI nhỏ hơn" nghe rất giống nhiều việc đã có người làm — vì đúng là vậy. Ý tưởng "sinh rồi lọc rồi huấn luyện lại" đã có tên riêng trong giới nghiên cứu từ 2022 (gọi là STaR). Có một nghiên cứu năm 2025 (KnowAda) làm gần như y hệt bước "viết lại phần không chắc chắn thành mô tả chung chung" cho việc mô tả ảnh. Và cũng có một nghiên cứu năm 2024 (VGA) dùng đúng loại "VH" này để giảm bịa khi huấn luyện AI cho giao diện điện thoại.

Đây đúng là điều một vòng tranh luận riêng đã cố tình xoáy vào để tìm cách bẻ gãy — và nó đứng vững, không phải vì không ai tìm ra điểm giống, mà vì sau khi phân tích kỹ, điểm khác biệt thật sự vẫn còn:

**Một, nguồn kiểm tra độc lập với chính AI đang bị kiểm.** Ở KnowAda, chính mô hình AI đó tự hỏi-tự-trả-lời để đoán xem nó có "biết" chi tiết mình vừa viết ra hay không — tự mình chấm mình. Ở đây, ta dùng một nguồn hoàn toàn bên ngoài (VH) để đối chiếu, không phụ thuộc vào việc AI có "tự nhận thức" tốt hay không. Và cái giá của việc bịa ở đây cao hơn nhiều so với việc mô tả sai một chi tiết trong bức ảnh — bịa tên nút khiến người dùng thao tác sai trên một hệ thống thật.

**Hai, và đây là câu hỏi trung tâm, chưa ai từng đặt ra:** khi "học trò" — một mô hình nhỏ, chạy ngay trên máy, không có nguồn kiểm tra bên ngoài nào để dựa vào lúc dùng thật — liệu thói quen thành thật đó có còn giữ được hay không? Đây là câu hỏi có thể trả lời là "không" (kết quả rỗng, model chỉ học vẹt bề mặt chứ chưa thật sự thấm), và chính vì có khả năng trả lời "không" một cách trung thực, nó mới là một câu hỏi nghiên cứu thật, chứ không phải một việc chắc chắn thắng từ đầu.

---

## Vậy có đủ để bảo vệ một luận văn thạc sĩ không?

Câu trả lời sau khi tra cứu kỹ các quy định và thông lệ (bao gồm cả Thông tư 23/2021 của Bộ Giáo dục về đào tạo thạc sĩ): **đủ, với một điều kiện.** Luận văn thạc sĩ không bắt buộc phải đánh bại mọi kỷ lục thế giới — được phép có đúng một thí nghiệm trọng tâm có khả năng ra kết quả "không có gì khác biệt", miễn là thí nghiệm đó được thiết kế nghiêm túc, có quy tắc thắng-thua định sẵn trước khi nhìn số liệu. Đây không phải chuyện chúng tôi tự nghĩ ra để bào chữa — từng có một hội thảo khoa học chuyên đề gắn với hội nghị NeurIPS năm 2021 (không phải bản thân hội nghị chính NeurIPS, mà một workshop riêng về nghiên cứu đăng-ký-trước) chuyên nhận những nghiên cứu kiểu này, đánh giá dựa trên chất lượng của câu hỏi và cách thiết kế, không dựa trên việc kết quả có đẹp hay không.

Trên đây là trả lời cho lo ngại về *chất lượng đóng góp*. Còn nếu thầy lo về *khối lượng công việc* — liệu có đủ việc để thành một luận văn hay không — thì phạm vi ở đây thực ra thiên về **hơi rộng chứ không hẹp**. Có bốn khối việc thực chất, mỗi khối tự nó đã đáng kể:

1. **Xây một quy trình tổng hợp dữ liệu chống-bịa** — mô hình lớn sinh bản nháp, một thuật toán đối chiếu với VH để dò chỗ bịa, rồi viết lại chỗ bịa thành mô tả trung thực. Đây là kỹ thuật thật, không phải chỉ gọi API rồi dừng.
2. **Huấn luyện thật một mô hình thị giác–ngôn ngữ** (fine-tune LoRA), tạo ra *hai bản độc lập* — bản chính học từ dữ liệu đã lọc và bản đối chứng học từ dữ liệu thô — để tách bạch được đâu là công của việc lọc.
3. **Một phương pháp đo chất lượng khi không có đáp án mẫu** — kiểm chính bằng cách bơm lỗi đã biết, chấm bằng một mô hình độc lập khác họ, và thiết kế chống "vừa đá bóng vừa thổi còi". Bản thân phần này đã là một đóng góp về phương pháp, đứng riêng được.
4. **Một thiết kế thí nghiệm hai tầng** có đăng-ký-trước ngưỡng thắng-thua và một phép kiểm định thống kê chính xác cho mẫu nhỏ, để trả lời một câu hỏi nghiên cứu chưa ai đặt.

Gộp lại là đủ cả ba trụ của một luận văn nghiên cứu: có **xây** (mô hình + quy trình dữ liệu), có **đo** (khung đánh giá), có **phát hiện** (câu hỏi hai tầng). Ở chiều ngược lại, rủi ro thật sự của đề tài này là *quá tải* chứ không phải mỏng — nên đã **chủ động cắt bớt** cho vừa sức: bỏ phần nhiều-màn/sắp thứ tự ra khỏi phần huấn luyện, chỉ dùng học-có-giám-sát (không dùng học tăng cường), và không đua bảng xếp hạng.

Điều kiện duy nhất về *cách thiết kế* (khác với chuyện khối lượng ở trên): phải tách rõ thành **hai tầng thí nghiệm** thay vì gộp làm một. Bảng ở mục 4 của trang gặp thầy đã ghi rõ Tier 1 so gì với gì, Tier 2 so gì với gì, và ngưỡng đậu/rớt nằm ở bảng "Bộ thí nghiệm đầy đủ" — phần dưới đây chỉ nói thêm hai điều mà bảng đó không chứa: vì sao phép so ở Tier 2 đáng giá, và vì sao bắt buộc phải tách rời hai tầng.

Vì sao phép so ở Tier 2 mới là phép so đáng giá:

- **Nó là so công bằng, không phải so lệch sân.** Cả hai bên cùng bị bịt đúng một nguồn thông tin. Học trò không được ưu ái gì thêm — thậm chí lúc hỏi, học trò còn không được nhắc câu "đừng bịa nút không có thật", trong khi thầy giáo lúc sinh dữ liệu thì có được nhắc (chi tiết ở Phụ lục D, Bước 6). Nếu học trò vẫn thành thật hơn, cái đó chỉ có thể đến từ trọng số đã học, không đến từ lời nhắc.
- **Nó là phép so ngược đời — và chính vì thế mới đáng hỏi.** Thầy giáo là mô hình lớn chạy trên máy chủ của OpenAI; học trò chỉ là mô hình 3B chạy trên laptop. Bình thường không ai kỳ vọng học trò thắng thầy. Ở đây chỉ hỏi đúng một khía cạnh hẹp — độ thành thật — với giả thuyết: thói quen thành thật *học được* có thể bù lại chênh lệch về kích cỡ. Giả thuyết này hoàn toàn có thể sai.
- **Nó trả lời thẳng lời phê của thầy.** Thầy giáo trần chính là bản luận văn cũ ("chỉ gọi API"). Thắng được nó nghĩa là mô hình tự train ra được thứ mà gọi API không có; không thắng thì cũng biết rõ giới hạn thật nằm ở đâu.

Lý do phải tách bạch hai tầng nằm ở cỡ mẫu: chỉ có 12 ứng dụng dùng để kiểm tra. Nếu gộp cả hai phép so vào một con số duy nhất, thứ đáng lo không phải một kết quả rỗng — một kết quả rỗng được trình bày đúng cách vẫn cho biết giới hạn thật của phương pháp, và đó là một phát hiện khoa học. Thứ đáng lo là một **kết quả mơ hồ, không đủ tin cậy để nói lên điều gì**, vì với 12 ứng dụng thì khoảng tin cậy rất dễ trùm qua cả hai phía. Và đây mới là mắt xích chính: gộp chung thì cái gần-chắc-dương (Tier 1) bị cái có-thể-null (Tier 2) kéo tuột về vùng mơ hồ đó — mất luôn cả hai, trong khi tách ra thì chỉ mất một. Kết quả mơ hồ thì không kể được câu chuyện nào, và dễ khiến người nghe quay lại đúng nhận xét ban đầu của thầy. Tách rời ra thì Tier 1 luôn có một câu chuyện chắc chắn để kể, bất kể Tier 2 ra sao.

---

## Mô hình được xây dựng ra sao (giải thích không cần biết máy học)

Huấn luyện lại toàn bộ một mô hình AI từ đầu tốn rất nhiều tiền và máy tính mạnh — không khả thi với một laptop cá nhân hay tài khoản Google Colab thông thường. Kỹ thuật được dùng ở đây gọi là **LoRA**: thay vì "dạy lại" toàn bộ bộ não của mô hình, ta chỉ gắn thêm một số ít "miếng dán" nhỏ có thể học được vào một phần của mô hình, và chỉ huấn luyện đúng những miếng dán đó — phần còn lại giữ nguyên, đóng băng. Cách này rẻ hơn hàng trăm lần nhưng vẫn đủ để mô hình học được thói quen mới.

Cụ thể hơn: mô hình có hai phần chính — phần "nhìn" (hiểu ảnh) và phần "nói" (viết câu). Vì việc cần dạy ở đây là thói quen *nói gì* khi không chắc chắn, chứ không phải *nhìn thấy gì*, nên phần "nhìn" được giữ nguyên hoàn toàn (đóng băng), chỉ có phần "nói" được gắn miếng dán và huấn luyện. Việc này vừa tiết kiệm, vừa tránh việc kết quả thí nghiệm bị nhiễu bởi những thay đổi không liên quan đến câu hỏi đang muốn trả lời.

Toàn bộ cấu hình này (bao nhiêu miếng dán, tốc độ học, số lần lặp qua dữ liệu...) đã được chốt dựa trên một nghiên cứu công bố năm 2026 (ZonUI-3B) từng huấn luyện thành công đúng loại mô hình này trên một card đồ hoạ phổ thông — nên đây không phải con số đoán mò, mà có tiền lệ thật để dựa vào, dù vẫn cần chạy thử một lần nhỏ trước khi tin tưởng hoàn toàn.

---

## Dữ liệu lấy từ đâu, chuẩn bị thế nào

Nguồn ảnh màn hình chính là MobileViews — một bộ sưu tập công khai gồm ảnh chụp màn hình ứng dụng Android thật, kèm theo đúng loại "VH" cần để đối chiếu, được phép dùng cho nghiên cứu. Bản công khai tải được tên là **MobileViews-600K** (hơn 600.000 cặp ảnh–VH). ⚠️ **Nhưng đừng dùng thẳng con số 600.000 để nói "còn thừa dữ liệu":** phần thật sự lấy được bằng code hiện có chỉ khoảng **231.000 dòng** (phần còn lại nằm ở một định dạng khác, chưa tương thích — chi tiết ở Phụ lục D, Bước 1). Dù vậy 231.000 vẫn lớn hơn nhu cầu rất nhiều lần, nên kết luận không đổi: 30 ứng dụng pilot cộng pool mở rộng nói ngay dưới vẫn chỉ là một phần rất nhỏ, lấy thêm là hoàn toàn khả thi về mặt dữ liệu, chỉ là cần đánh đổi thêm thời gian/công sức kiểm tra (vì sao không lấy nhiều hơn ngay từ đầu: xem câu "Sao không lấy nhiều dữ liệu hơn nữa" ở mục 8 của trang gặp thầy).

**"Vòng kiểm tra chất lượng" nói ở nhiều chỗ trong tài liệu này nghĩa là gì, nói cụ thể:** đây KHÔNG phải việc có người ngồi xem từng ứng dụng. Đó là một bước lọc tự động hai lớp: (1) bỏ những nhãn nút bị coi là "rác" trong VH — nhãn rỗng, nhãn quá dài (nhiều khả năng là đoạn văn bản chứ không phải tên nút), hoặc nhãn chứa đường dẫn/tham số quảng cáo; (2) chỉ giữ lại màn hình nào còn đủ số nút bấm/gõ khác nhau sau khi đã lọc sạch — màn nào còn quá ít nút thật thì bị loại vì không đủ để làm một phép thử có ý nghĩa. **Ngưỡng "đủ" khác nhau tuỳ vòng lấy dữ liệu, và điều này là cố ý:** vòng lọc rác trên dữ liệu có sẵn dùng **≥ 5 nút**, còn các vòng đi lấy thêm dữ liệu mới dùng **≥ 6 nút** (siết hơn vì lúc đó có cả kho để chọn, không việc gì phải nhận màn nghèo nút). Con số chính xác của từng vòng ghi ở Phụ lục F. Ứng dụng nào còn ít nhất một màn sống sót qua bước lọc này thì được tính là "đã qua kiểm tra chất lượng". Nói cách khác, đây là một tiêu chí kỹ thuật hẹp ("đủ nút thật, sạch, để thử nghiệm"), không phải một cuộc kiểm định toàn diện về độ đa dạng hay độ tiêu biểu của ứng dụng.

Có một bước rất quan trọng làm ngay từ đầu, trước bất kỳ việc gì khác: chia sẵn danh sách ứng dụng thành hai nhóm không bao giờ trộn lẫn — một nhóm chỉ dùng để dạy mô hình, một nhóm chỉ dùng để kiểm tra sau này. Việc này giống như ra đề thi bằng những câu hoàn toàn khác với bài tập đã cho học sinh ôn — nếu để lẫn, mô hình có thể chỉ đang "học thuộc lòng" ứng dụng nó từng thấy, chứ không thật sự học được thói quen tổng quát. Danh sách chia này được khoá lại và ghi vào hệ thống quản lý phiên bản ngay khi tạo ra, không được sửa sau khi đã nhìn kết quả.

Con số "18 ứng dụng dùng để dạy" không phải là toàn bộ số ứng dụng học trò sẽ thấy lúc train — đó chỉ là phần đã qua kiểm tra chất lượng từ bộ 30 ứng dụng pilot ban đầu. Việc mở rộng thêm dữ liệu train **đã chạy thật rồi**, không còn là dự kiến:

> **✅ Kết quả mở rộng (đã chạy 12/7/2026 — mọi con số về dữ liệu train trong tài liệu này đều lấy từ đây).** ⚠️ *Đã chạy xong phần lấy dữ liệu, nhưng còn một việc chưa xong: danh sách 220 app này chưa được ghi vào file split đã commit — xem Phụ lục D, Bước 1.* Lấy thêm từ hai phần kho dữ liệu chưa dùng → lọc trùng theo tên và theo ảnh → thu được **498 màn hình mới, thuộc 220 ứng dụng mới** (trung bình ~2,3 màn mỗi ứng dụng; đã loại 98 màn trùng lặp trong nội bộ).
>
> **Và điều quan trọng nhất: 0 ca rò rỉ chéo** — không một màn nào trong 220 ứng dụng mới trùng với 12 ứng dụng dành để kiểm tra, kể cả khi so bằng ảnh chứ không chỉ so tên. Cổng chống rò rỉ **sạch**.
>
> Số này **ít hơn kỳ vọng ban đầu** (~1.000 màn): thực tế mỗi ứng dụng mỏng hơn dự tính (92 ứng dụng chỉ có đúng 1 màn). Nhưng **đủ dùng** cho quy mô LoRA nhỏ. Muốn dày hơn thì chạy tiếp phần fetch còn lại, bỏ qua ứng dụng đã có.

**Mấy con số màn hình hay bị lẫn với nhau — bảng này gỡ một lần cho rõ.** Tài liệu nhắc tới 127, 76, 51, 498 và 574 màn ở nhiều chỗ khác nhau; chúng không mâu thuẫn, chỉ là những lát cắt khác nhau của cùng một kho:

| Con số | Là gì | Dùng vào việc gì |
|---|---|---|
| **127 màn / 30 app** | Toàn bộ bộ pilot đã qua vòng lọc chất lượng, gồm cả app train lẫn app test | Nguồn để cắt ra hai nhóm dưới |
| **76 màn / 18 app** | Phần của bộ pilot rơi vào nhóm **train** | Dạy học trò |
| **51 màn / 12 app** | Phần còn lại của bộ pilot, rơi vào nhóm **test** | Chấm điểm — **không bao giờ đụng tới lúc train** |
| **498 màn / 220 app** | Phần mở rộng thêm ngày 12/7, chỉ đổ vào nhóm train | Dạy học trò |
| **≈574 màn** | 76 + 498 — **tổng dữ liệu train thật sự** | → dựng ~1.700–2.870 mẫu huấn luyện |

Quy trình đầy đủ chạy tuần tự: mở rộng ảnh màn hình (✅ xong) → tự động sinh vài câu hỏi tình huống cho mỗi màn → gọi thầy giáo viết hướng dẫn nháp → đối chiếu và lọc → đóng gói thành định dạng huấn luyện. Nhóm ứng dụng mở rộng này KHÔNG qua cùng vòng kiểm tra chất lượng kỹ như 30 ứng dụng gốc — rủi ro đã ghi ở Phụ lục E (#10). Riêng 12 ứng dụng dành để kiểm tra thì giữ cố định, không mở rộng, để giữ đây là nguồn chấm điểm đáng tin cậy nhất.

Toàn bộ các bước này đều rẻ hoặc miễn phí, trừ đúng một bước phải trả tiền cho việc gọi thầy giáo (gpt-4o-mini) — ước tính chỉ khoảng một, hai đô-la cho vài nghìn lượt gọi dựa trên một lần chạy thử nhỏ trước đó, nhưng sẽ đo lại chi phí thật trên một mẫu nhỏ trước khi quyết định chạy toàn bộ.

---

## Đo thành công thế nào, và quy tắc thắng-thua đã chốt trước khi biết kết quả

### Đo con số gì

Trước khi nói chuyện thắng-thua, phải nói rõ **thước đo chính là gì**: **độ trung thực `f`**, tính bằng `f = 1 − tỉ lệ bịa`. Hai cách nói cùng một thứ, cộng lại bằng 1; luận văn và bản đăng-ký-trước đều báo cáo ở dạng `f` (càng cao càng tốt), nhưng giải thích thì dễ hình dung hơn nếu đi từ tỉ lệ bịa. Cách tính tỉ lệ bịa, bằng lời:

> Cho mô hình viết hướng dẫn cho một màn hình. Đếm xem trong đó có bao nhiêu bước *có nhắc đích danh tên một nút* (những bước chỉ nói chung chung không tính vào mẫu số, vì chúng không hề khẳng định nút nào tồn tại cả). Trong số đó, đếm bao nhiêu bước nhắc tới một nút **không** có trong VH của màn đó. Chia hai số ấy cho nhau ra tỉ lệ bịa.
>
> Ví dụ: hướng dẫn có 4 bước, 3 bước nhắc tên nút, trong đó 1 bước nhắc "Preferences" (không tồn tại) → tỉ lệ bịa = 1/3 ≈ 33%. **Càng thấp càng tốt.**

**Ba điều phải nói kèm, nếu không sẽ bị vặn:**

1. **Ai chấm?** Không dùng lại đúng thuật toán đã dùng để lọc dữ liệu lúc huấn luyện — làm vậy là vừa đá bóng vừa thổi còi. Lúc chấm dùng ba cơ chế độc lập khác (một mô hình so-nghĩa khác họ, một AI đóng vai giám khảo khác dòng với thầy giáo, và một phép so từ ngữ thô), một bước chỉ bị kết luận là bịa khi đa số đồng ý. Cơ chế đầy đủ ở mục "Chống vừa đá bóng vừa thổi còi" ngay dưới.
2. **Có mẹo nào ăn gian được thước đo này không?** Có, và đã chặn: một mô hình có thể đạt tỉ lệ bịa bằng 0 rất dễ — cứ nói chung chung mọi bước, không bao giờ nêu tên nút nào. Vì vậy luôn báo kèm **%fallback** (tỉ lệ bước phải nói chung chung). Tỉ lệ bịa thấp đi kèm %fallback cao ngất chỉ có nghĩa là mô hình đang né trả lời.
3. **Gộp lại thành 12 con số.** Điểm được tính trung bình theo từng ứng dụng trước, rồi mỗi ứng dụng test cho ra đúng một con số chênh lệch (tỉ lệ bịa của học trò trừ đi của bên kia). 12 ứng dụng test → 12 con số. Gộp theo ứng dụng chứ không gộp theo màn hình, vì các màn trong cùng một ứng dụng giống nhau nhiều, đếm chúng như 12 bằng chứng độc lập sẽ thổi phồng độ chắc chắn của kết luận.

### Quy tắc thắng-thua, khoá trước khi nhìn số

Một nguyên tắc quan trọng trong khoa học thực nghiệm nghiêm túc: quyết định trước "thế nào là thắng, thế nào là thua" rồi mới chạy thí nghiệm, không phải nhìn số liệu xong mới bịa ra tiêu chuẩn cho vừa với kết quả đẹp. Nguyên tắc này được áp dụng chặt ở Tier 2 (tầng rủi ro thật).

Vì chỉ có 12 ứng dụng dùng để kiểm tra (một con số khá nhỏ), phương pháp thống kê thông thường (giả định mẫu lớn) không đáng tin. Thay vào đó dùng một cách tính chính xác tuyệt đối phù hợp cho mẫu nhỏ, gọi là **phép kiểm định đổi-dấu-chính-xác**. Ý tưởng của nó, nói không cần công thức:

> Ta có 12 con số chênh lệch, giả sử phần lớn đều dương (học trò tốt hơn). Câu hỏi cần trả lời: **liệu có phải chỉ do may mắn không?**
>
> Cách kiểm tra: nếu thật ra học trò chẳng hơn gì, thì việc mỗi ứng dụng ra dấu dương hay âm chẳng khác gì tung đồng xu. Vậy hãy thử **lật dấu 12 con số đó theo đủ mọi cách có thể** — mỗi con số có 2 khả năng (giữ nguyên hoặc đảo dấu), 12 con số nên có 2¹² = 4.096 tổ hợp. Máy tính liệt kê hết cả 4.096 tổ hợp đó và tính trung bình từng tổ hợp.
>
> Cuối cùng xem: kết quả thật của ta xếp thứ mấy trong 4.096 khả năng ấy? Nếu nó nằm trong nhóm 5% cao nhất, kết luận là khác biệt thật, không phải may. Nếu nó nằm lẫn giữa đám đông, không kết luận được gì.

Cách này **liệt kê hết mọi khả năng chứ không ước lượng**, nên không cần bất kỳ giả định nào về hình dạng phân bố dữ liệu. Với mẫu nhỏ, đây là thứ đáng tin hơn hẳn phương pháp thống kê thông thường — và cũng là một điểm mạnh về phương pháp để trình bày với thầy.

#### MDE — con số quyết định thí nghiệm có đáng chạy hay không

Phép kiểm định trên trả lời "khác biệt này có thật không". Nhưng còn một câu phải hỏi **trước khi chạy**: với vỏn vẹn 12 ứng dụng, thí nghiệm này đủ sức nhìn thấy khác biệt lớn cỡ nào? Đó là **MDE** (*minimum detectable effect* — mức phát hiện tối thiểu).

> Hình dung MDE như độ phân giải của một cái kính. Kính có MDE = 5 điểm phần trăm thì nhìn được mọi khác biệt từ 5 điểm trở lên. Nếu MDE = 25 điểm, mà khác biệt thật ngoài đời chỉ là 10 điểm, thì thí nghiệm sẽ ra "không thấy gì" — **không phải vì học trò kém, mà vì cái kính quá mờ**. Kết quả rỗng kiểu đó không nói lên điều gì về phương pháp cả, chỉ nói cỡ mẫu quá nhỏ.
>
> MDE phụ thuộc hai thứ: số ứng dụng test (càng nhiều càng nhìn rõ) và độ dao động của điểm giữa các ứng dụng (càng nhiễu càng nhìn mờ). Vì vậy phải đo nó bằng số liệu pilot thật, **trước** khi khoá mọi thứ.

Đây là lý do phải có một **thí nghiệm cổng** chạy trước cả đồng tiền đầu tiên (nó mang mã TN0 ở bảng thí nghiệm phía dưới): nếu MDE tính ra lớn hơn 15–20 điểm phần trăm, cái kính mờ tới mức Tier 2 gần như chắc chắn ra kết quả rỗng bất kể sự thật là gì. Khi đó phải **đổi cách chia 18 app train / 12 app test thành 15/15** — hy sinh bớt dữ liệu dạy để lấy thêm ứng dụng chấm, cho kính nét lên. Việc đổi này chỉ được làm **trước** khi khoá ngưỡng; đổi sau khi đã thấy kết quả thì thành ra chọn cỡ mẫu cho vừa với kết quả mong muốn.

Ô `[MDE = ___ pp]` trong bản đăng-ký-trước hiện **còn trống** — đây chính là việc kế tiếp phải làm.

Ba kết cục có thể xảy ra, và cả ba đều được viết sẵn cách diễn giải trước khi chạy:

| Kết quả | Điều kiện | Ý nghĩa |
|---|---|---|
| Thắng đầy đủ | Khác biệt rõ ràng về mặt thống kê, và đủ lớn về mặt thực tế (xem định nghĩa "đủ lớn" ngay dưới bảng) | Thói quen thành thật đã thật sự ngấm vào mô hình, áp dụng được cho ứng dụng chưa từng thấy — trong phạm vi loại ứng dụng giống với bộ dữ liệu đã dùng để kiểm tra, chưa phải "mọi ứng dụng GUI nói chung" |
| Thắng một phần | Khác biệt có ý nghĩa thống kê, nhưng nhỏ hơn "đủ lớn" | Có ngấm, nhưng còn yếu — vẫn là một phát hiện có giá trị |
| Không thấy khác biệt | Không đủ bằng chứng thống kê | Báo cáo trung thực, đây là giới hạn thật của phương pháp — không có nghĩa là toàn bộ luận văn thất bại, vì Tier 1 (lưới an toàn) đã đứng độc lập |

#### Định nghĩa "đủ lớn về mặt thực tế"

Vì sao cần thêm điều kiện này bên cạnh "có ý nghĩa thống kê"? Vì hai câu hỏi khác nhau. Thống kê chỉ trả lời *"khác biệt này có thật không, hay do may?"*. Nó không trả lời *"khác biệt này có đáng kể không?"* — một cải thiện 0,5 điểm phần trăm vẫn có thể "thật" về mặt thống kê mà chẳng có ý nghĩa gì với người dùng. Nên phải định trước một mức sàn.

Mức sàn đó lấy ở đâu ra? Ý tưởng: **lấy chính những ứng dụng mô hình ĐÃ được học làm mốc**. Trên nhóm ứng dụng đã học, mô hình ở điều kiện thuận lợi nhất, nên mức cải thiện đo được ở đó là mức *tốt nhất có thể trông đợi*. Câu hỏi Tier 2 thực chất là: sang ứng dụng lạ chưa từng thấy, giữ lại được bao nhiêu phần của mức đó?

Định nghĩa chính thức, gồm ba bước:

1. Đo mức cải thiện trên **18 ứng dụng dùng để huấn luyện** — gọi là **mốc tham chiếu**, ký hiệu **`Δ_train`**.
2. Đo mức cải thiện trên **12 ứng dụng test** (ứng dụng lạ) — đây là con số đang quan tâm, ký hiệu **`Δ_test`**.
3. **"Đủ lớn" = con số ở bước 2 đạt ít nhất MỘT NỬA mốc tham chiếu ở bước 1**, viết bằng ký hiệu là **`Δ_test ≥ 0.5 × Δ_train`** — đây chính là điều kiện (B) sẽ gặp lại ở bảng thí nghiệm và ở bản đăng-ký-trước.

> **Hệ số 0.5 ở đâu ra?** Đây là **con số tự đề xuất, không lấy từ literature** — nếu thầy hỏi thì trả lời đúng như vậy, đừng bịa nguồn.

> Ví dụ bằng số: nếu trên 18 ứng dụng train, học trò giảm được 20 điểm phần trăm tỉ lệ bịa, thì mốc tham chiếu = 20. Muốn gọi là "thắng đầy đủ", trên 12 ứng dụng test phải giảm được ít nhất 10 điểm. Giảm 6 điểm nhưng vẫn có ý nghĩa thống kê → xếp vào "thắng một phần".

**Điều kiện bắt buộc để hai con số này so được với nhau:** cả hai phải đo bằng CÙNG một công thức và ở CÙNG một điều kiện — cụ thể là **đều tắt VH lúc suy luận**, giống hệt Tier 2. Chỉ khác duy nhất ở chỗ đo trên nhóm ứng dụng nào.

> *(Ghi chú thống nhất tài liệu: một bản nháp trước đây từng lấy mốc tham chiếu là mức cải thiện đo lúc VẪN CÒN VH. Cách đó đã bị bỏ, vì khi ấy một mốc đo lúc còn "phao cứu sinh" còn mốc kia đo lúc đã "bỏ phao" — chia hai con số không cùng điều kiện cho nhau thì tỉ lệ ra được chẳng nói lên điều gì. Từ nay toàn bộ tài liệu chỉ dùng đúng một định nghĩa ba bước ở trên.)*

Một câu hỏi từng được đặt ra: liệu có rủi ro là mô hình được huấn luyện trên dữ liệu sạch lại viết ra câu trả lời mơ hồ nhàm chán, trong khi mô hình huấn luyện trên dữ liệu thô (dù có bịa) lại nghe cụ thể và có ích hơn, khiến người chấm bị đánh lừa? Câu hỏi này đã được tra cứu kỹ và không tìm thấy bằng chứng ủng hộ mối lo đó trong đúng tình huống của luận văn — nhưng để chắc chắn, một phép đo phụ, rẻ tiền được thêm vào để kiểm tra riêng độ hữu ích (tách biệt khỏi độ trung thực) của hai bản — đó chính là **TN4** ở bảng thí nghiệm, đặc biệt ở những chỗ từng bị viết lại thành mô tả chung chung.

---

## Bộ thước đo đầy đủ

Mục này quan trọng hơn vẻ ngoài của nó, vì một lý do rất cụ thể: **bản luận văn cũ đã chết một lần đúng ở chỗ này.** Hồi đó bộ lọc vừa sửa lỗi vừa chấm điểm chính mình, nên độ trung thực vọt lên gần 100% — một con số đẹp long lanh và hoàn toàn vô nghĩa, vì nó chỉ nói rằng bộ lọc đồng ý với chính bộ lọc. Lỗi đó được phát hiện trong một vòng rà soát nội bộ và đã vá.

Bài học rút ra từ lần đó định hình toàn bộ thiết kế đo lường hiện tại. Có ba nguyên tắc, và nên trình bày với thầy đúng ba câu này:

1. **Mọi thước đo đều có cách ăn gian.** Nên với mỗi cái lợi, luôn báo kèm cái giá của nó: một mô hình đạt điểm trung thực cao bằng cách nói chung chung mọi bước thì cái giá của nó nằm ở %fallback.
2. **Thứ dùng để lọc không bao giờ được dùng lại để chấm.** Đây là điều kiện sống-còn của tính hợp lệ, không phải chi tiết kỹ thuật.
3. **Con số nào cũng phải kèm điều kiện đọc nó.** Mẫu số gồm gì, giả định nào chưa kiểm chứng, phạm vi khái quát tới đâu.

Mỗi thước dưới đây viết hai tầng: một đoạn lời thường cho người không chuyên, rồi một **hộp kỹ thuật** kèm công thức và trụ trích dẫn cho người đọc muốn kiểm tận gốc. Ai không cần công thức thì bỏ qua các hộp, mạch đọc vẫn liền.

### Thước chính — độ trung thực (faithfulness)

Đã định nghĩa ở mục trước: đếm bao nhiêu lần mô hình nhắc tên nút, trong đó bao nhiêu lần nhắc nút không tồn tại.

> **Hộp kỹ thuật.** Độ trung thực mỗi màn: **f = 1 − (số lần nhắc nút BỊA / tổng số lần nhắc nút)**. Gộp mỗi ứng dụng: `f_app` = trung bình f của các màn trong ứng dụng đó. Đơn vị thống kê cuối cùng = **12 con số per-app** (macro-per-app, mỗi ứng dụng một phiếu). Trụ: **ALOHa (Petryk et al., NAACL 2024 Short)** — cơ chế gốc: trích thực thể bằng LLM → so embedding → ghép Hungarian → không cặp nào đủ giống thì tính là bịa.
>
> **Estimand — phải khai đúng:** ước lượng này là *trung bình đều trên ứng dụng*, **cấm viết "đại diện cho ứng dụng nói chung"** (không có mẫu ngẫu nhiên từ quần thể app).
>
> **Ba điều kiện phải khai kèm khi báo con số:** (a) độ phủ nhãn của VH (nút icon-only/nhãn chung bị loại khỏi mẫu số); (b) mẫu chỉ giữ màn dày nhãn, mà màn dày nhãn thì VH liệt kê đủ hơn → nhiều tên nút khớp được hơn → ít bước bị gắn cờ bịa hơn, nên tỉ lệ bịa quan sát được là **hạ thấp có hệ thống** so với thực tế; (c) con số ~¼ hiện có chỉ là quan sát sơ bộ trên một mô hình.

### Ba thước đi kèm bắt buộc — để không ai gaming được thước chính

Thước chính một mình thì ăn gian rất dễ (cứ nói chung chung là bịa bằng 0). Ba con số dưới đây bắt buộc báo kèm, luôn luôn:

| Thước | Đo gì | Vì sao bắt buộc |
|---|---|---|
| **%fallback** | Tỉ lệ bước phải rơi vào câu mô tả chung chung | Trung thực cao mà fallback cao ngất = né trả lời, không phải thành công. Đây là **cái giá** phải trả, báo song song với **cái lợi** |
| **Tỉ lệ lỗi-ngầm** (silent-error) | Trong "phương án đoán thay" đã bị loại (xem mục "Ý tưởng cốt lõi"): bao nhiêu bước bị thay bằng **một nút có thật nhưng sai chức năng** | Đây là bằng chứng cho quyết định thiết kế "chỉ mô tả, không đoán". Lỗi ngầm nguy hiểm hơn fallback vì nó **không lộ ra** |
| **Tỉ lệ màn 0-nhắc-nút** | Bao nhiêu màn mô hình không nêu tên nút nào cả | Chỉ báo né-trả-lời ở mức màn. Nếu một ứng dụng có **>50% màn 0-nhắc-nút** → gắn cờ cảnh báo |

> **Hộp kỹ thuật.** Lỗi-ngầm = (số bước bịa bị thay bằng nút có thật nhưng sai chức năng) / (số bước bịa được xử lý). Ví dụ: 30 bước bịa, nhánh đoán tạo 6 nút sai âm thầm → 20%. Đây là thước của **thí nghiệm đối-chứng-thất-bại**, báo cáo trong TN3 ở bảng thí nghiệm phía dưới, không phải thước của mô hình chính.

### Hai thước phụ, và một thước cố ý loại khỏi headline

- **Đúng-nhãn (label fidelity)** — gọi đúng tên hiển thị của nút. *Đây là thước tự định nghĩa, luận văn khai thẳng điều đó,* không mượn danh chuẩn ngành.
- **Đúng-chỗ (grounding)** — điểm bấm dự đoán có nằm trong khung nút không. **Cố ý ĐƯA RA KHỎI headline một màn**, chỉ giữ làm đối chứng trên ScreenSpot-v2.

> **Hộp kỹ thuật — vì sao loại grounding khỏi headline (câu hỏi hội đồng rất dễ hỏi).** Định nghĩa chính: point-in-GT-bbox, `l ≤ x ≤ r` và `t ≤ y ≤ b` (**SeeClick, ACL 2024**); dung sai 14% đường chéo (**AITW, Rawles et al., NeurIPS 2023**) chỉ là biến thể đối chứng. Lý do loại: nếu lấy **tâm của khung nút đã khớp** làm (x,y) thì điểm đó luôn nằm trong khung → **tautology 100%**, con số vô nghĩa. Muốn đo thật thì (x,y) phải đến từ một bộ trỏ độc lập dự đoán từ tên+ảnh — việc đó thuộc nhánh khác, không thuộc mùa này.

### Chống "vừa đá bóng vừa thổi còi" — điểm mạnh phương pháp nên nhấn với thầy

Nguyên tắc: **thứ dùng để lọc dữ liệu lúc train, tuyệt đối không được dùng lại để chấm điểm lúc đánh giá.** (Lý do lịch sử đã kể ở đầu mục.)

> **Hộp kỹ thuật.**
> - **Lọc (lúc chuẩn bị data):** embedding `nomic-embed-text`, ngưỡng **τA = 0.55** (đã freeze).
> - **Chấm (lúc đánh giá):** ba cơ chế **khác họ**, một bước bị kết luận là bịa khi **≥2/3 đồng ý không-khớp**:
>   1. embedding `bge-m3` (khác họ nomic), ngưỡng **τB hiệu chuẩn RIÊNG** — 80–120 cặp gán tay, báo P/R + Cohen's κ, **precision ≥ 0.95**, rồi freeze. **Không được tái dùng τA = 0.55** (hai mô hình nhúng khác nhau, không có lý do gì ngưỡng trùng nhau).
>   2. LLM-judge `llama3.2` chạy local, prompt nhị phân — **khác họ với generator** gpt-4o-mini (generator là GPT-family → judge không được dùng GPT-family; trụ: **Panickssery et al., NeurIPS 2024** về self-preference bias).
>   3. token-overlap (so từ ngữ thô) — phép đếm **phi-neural**.
> - **Khai thẳng giới hạn:** ba cơ chế **giảm** chứ **không loại** tương quan sai số — bge-m3 và LLM-judge đều là mạng nơ-ron, vẫn có thể sai giống nhau; chỉ token-overlap là trục thực sự khác cơ chế. Vì vậy luận văn **báo hệ số tương quan giữa các bộ chấm** thay vì tuyên bố chúng "độc lập".

### Thống kê

> **Hộp kỹ thuật — trọn bộ.**
> - **Kiểm định chính:** exact sign-flip trên 12 con số per-app. `t_obs = mean(d)/(std(d,ddof=1)/√12)`; liệt kê toàn bộ `2¹² = 4096` tổ hợp dấu (không Monte Carlo); `p = mean(|null_stats| ≥ |t_obs|)`; **CI 95% bằng test-inversion** (quét thử mọi giá trị giả định, giữ lại những giá trị mà phép kiểm không bác bỏ) **trên chính phân phối exact đó**. Trụ: **Canay, Santos & Shaikh, REStat 103(2):346–363, 2021**; gộp per-cluster theo **Cameron & Miller, JHR 50(2):317–372, 2015**.
> - **Vì sao G=12 chấp nhận được:** literature cluster-robust cổ điển cảnh báo G < ~40–50, nhưng đó là cho **không dùng bootstrap**; wild/sign-flip bootstrap khắc phục xuống G rất nhỏ (mô phỏng ổn tới G≈5–10). Nhiều tài liệu hay nhắc ngưỡng "phải có ít nhất G ≥ 30 cụm", nhưng **con số 30 đó không có nguồn trực tiếp** — đừng để bị vặn bằng nó. (Lưu ý đọc: 30 ở đây là số CỤM, không liên quan tới 30 ứng dụng pilot.)
> - **Nếu sau này đổi lên G lớn hơn** → chuyển sang wild-cluster bootstrap Rademacher B=9999 (**Cameron-Gelbach-Miller, REStat 2008**).
> - **MDE** = `(t_{0.025,df=11} + t_{0.20,df=11}) × SD(d_j)/√12 ≈ 3.077 × SD(d_j)/√12`. SD lấy từ **12 con số ĐÃ trung bình theo app** (không phải SD thô per-màn); ước lượng bằng **cận trên thận trọng** `SD(d) ≈ √(Var(f_teacher) + Var(f_student_proxy))` — trong đó `f_student_proxy` = độ trung thực của **Qwen2.5-VL-3B gốc CHƯA fine-tune**, dùng thay cho student thật vì lúc tính MDE thì student chưa tồn tại; lấy từ pilot baseline (chỉ đo phương sai nền, không lộ hướng hiệu ứng → không phá pre-registration). **Ô [MDE = ___ pp] hiện còn TRỐNG — điền sau pilot rồi commit lần 2.**
> - **Đa so sánh:** Holm step-down. **Family đã đóng băng:** { độ trung thực Tier 1, độ trung thực Tier 2, phép đo hữu-ích/mạch-lạc }. Thêm/bớt sau khi nhìn số = vi phạm pre-registration.
> - **Bốn điểm khai thẳng:** (1) SD là SD của con số đã gộp per-app; (2) công thức MDE là **xấp xỉ liên tục kiểu Julious**, không phải ngưỡng chính xác của exact sign-flip rời rạc; (3) giả định **12 app độc lập** (không cùng công ty / cùng UI-kit / không chấm cùng lô API) là **giả định chưa kiểm chứng**, nêu như giới hạn đã biết; (4) kết luận Tier 2 viết đúng phạm vi "khái quát trong loại màn giống MobileViews đã qua kiểm tra chất lượng", không viết "mọi ứng dụng GUI".
> - **Chi tiết nhỏ đáng biết:** 4096 × 0.025 = 102.4 không nguyên → mức ý nghĩa danh nghĩa 2.5% không đạt được chính xác tuyệt đối (bản chất rời rạc của kiểm định exact).

### Vì sao chia 18/12 chứ không phải 80/20 như thông lệ

Câu hỏi rất dễ bị hỏi. Lý do: 30 ứng dụng gốc là bộ **duy nhất** đã qua vòng lọc chất lượng, nên nhóm test phải đủ lớn để làm nguồn chấm đáng tin — 20% của 30 chỉ còn 6 ứng dụng, quá mỏng để kết luận bất cứ điều gì. Cách chia: chia đều theo số màn mỗi ứng dụng, khoá bằng seed cố định, commit trước khi chạy bất kỳ bước sinh dữ liệu hay huấn luyện nào.

### Một đòn tấn công vào Tier 1 đã tự sụp — đáng kể lại khi thầy hỏi

Một vòng rà soát độc lập từng thử bẻ giả định "Tier 1 gần chắc thắng", bằng cách viện dẫn các nghiên cứu nói rằng train trên dữ liệu đã lọc **đôi khi thua** train trên dữ liệu thô. Đòn này tự sụp khi kiểm lại nguồn: hai nghiên cứu nó viện dẫn không thuộc nhóm tiền lệ của luận văn, còn KnowAda — nghiên cứu luận văn thật sự trích — khi tra đúng thì lại **ủng hộ** cách làm hiện tại. Kết luận: giữ nguyên mức tự tin ở Tier 1.

Thứ nên kể với thầy ở đây là **quy trình kiểm chứng đã bắt được một trích dẫn sai** — đó là bằng chứng cho thấy các lập luận trong tài liệu này đều bị soi nguồn chứ không nhận bừa.

---

## Bộ thí nghiệm đầy đủ — thứ sẽ chạy ngay tuần sau

> **Mục này nói gì:** trong bảy thí nghiệm, chỉ hai cái mang kết luận của luận văn (một cái gần chắc thắng, một cái có thể thua thật). Năm cái còn lại là để trả lời trước các câu vặn nhắm vào hai cái đó.

> ⚠️ **Cảnh báo trước khi trình thầy.** Bộ thí nghiệm dưới đây là bộ của **khung mô hình hiện tại**. Trong các file cũ (`report/43` Chương 13, `report/47`) có một bộ khác đánh số **E1–E16** — đó là bộ của **khung prompting CŨ mà thầy đã bác**, phần lớn đã lỗi thời. Chỉ còn đúng nhóm validate-thước-đo (E4–E7 cũ) được tái dùng, và đã gộp vào bảng dưới. **Đừng trình E1–E16 cho thầy** — trình bộ này.

### Toàn bộ bộ thí nghiệm trong một sơ đồ

```
   TN0 · CỔNG — chạy TRƯỚC MỌI THỨ, trước cả đồng tiền đầu tiên
   khoá danh sách app  →  pilot đo phương sai nền  →  tính MDE  →  khoá ngưỡng
        │                                            │
        │                          MDE > 15-20 điểm? ─ có ──→ đổi 18/12 thành 15/15
        ▼                                                      (trước khi khoá!)
   ┌─────────────────────────────────────────────────────┐
   │  HUẤN LUYỆN — cùng cấu hình, khác đúng một biến      │
   │   data đã lọc ──→ Student        (bản chính)        │
   │   data thô     ──→ Student-RAW   (bản đối chứng)    │
   └─────────────────────────────────────────────────────┘
        │                          │
        ▼                          ▼
   TN1 · TIER 1                TN2 · TIER 2
   Student vs Student-RAW      Student vs Thầy-giáo-trần
   "lọc data có tác dụng       "thói quen thành thật có
    đo được không?"             NGẤM vào mô hình không?"
   → gần chắc DƯƠNG            → CÓ THỂ NULL
   → lưới an toàn              → trụ chính, câu hỏi mới
        │                          │
        └──────────┬───────────────┘
                   ▼
   TN3 %fallback · lỗi-ngầm · màn-0-nhắc-nút   ← cái GIÁ, báo kèm luôn
   TN4 đo hữu-ích/mạch-lạc                     ← chống "sạch nhưng vô dụng"
   TN5 hiệu chuẩn bộ chấm vs người             ← không có nó, TN1/TN2 vô nghĩa
   TN6 bơm lỗi để validate thước đo            ← bỏ được (thì rút claim)
   TN7 trộn tỉ lệ 25/50/75%                    ← thăm dò, chưa đăng ký trước
```

**Đọc sơ đồ theo ba nhóm** — và đây cũng là cách nên trình bày với thầy:

- **Một cổng chặn (TN0).** Không qua nó thì không được tiêu đồng nào. Nó tồn tại để bảo vệ giá trị của việc đăng-ký-trước.
- **Hai thí nghiệm mang kết luận (TN1, TN2).** Một cái là lưới an toàn gần chắc dương — nó đủ chứng minh phần thầy yêu cầu. Một cái là câu hỏi nghiên cứu thật, có thể thua. Chúng **báo cáo độc lập**, nên cái sau thua không kéo sập cái trước.
- **Năm cái còn lại là lá chắn (TN3–TN7).** Chúng không tạo ra kết luận mới; chúng tồn tại để mỗi lần ai đó định vặn "sao biết không phải do X?" thì đã có sẵn một con số trả lời. TN5 là cái không được phép bỏ trong nhóm này: bộ chấm chưa hiệu chuẩn thì mọi con số ở TN1/TN2 đều không diễn giải được.

### Bảng chi tiết

Tám dòng, xếp đúng thứ tự chạy: một cổng (TN0) cộng bảy thí nghiệm (TN1–TN7). Cột cuối là thứ quan trọng nhất khi trình bày: cái nào **bắt buộc**, cái nào **bỏ được nếu hết thời gian**.

| # | Thí nghiệm | So gì với gì | VH lúc suy luận | Ngưỡng đậu/rớt (đã khoá trước) | Vai trò |
|---|---|---|---|---|---|
| **TN0** | **Cổng MDE + khoá split** | — (không phải so sánh) | — | Tính MDE bằng số liệu pilot thật. **Nếu MDE > 15–20 điểm phần trăm → đổi chia 18/12 thành 15/15 TRƯỚC khi khoá** | **Cổng — chạy trước mọi thứ** |
| **TN1** | **Tier 1 — lưới an toàn** | `Student` vs `Student-RAW` | Tắt (chấm trên output thô) | CI 95% của Δ nằm **hoàn toàn trên 0**. Không cần điều kiện "đủ lớn". **Nếu Tier 1 cũng null → DỪNG, rà lại toàn bộ pipeline lọc trước khi diễn giải Tier 2** | **Bắt buộc — gần chắc dương** |
| **TN2** | **Tier 2 — trụ chính** | `Student` vs `Teacher-BASE` | **Tắt hẳn**, held-out theo app | **(A)** CI 95% của Δ hoàn toàn trên 0 **VÀ (B)** `Δ_test ≥ 0.5 × Δ_train` | **Bắt buộc — có thể null** |
| **TN3** | **Thước đi kèm** | mọi arm | — | Không ngưỡng — **báo cáo bắt buộc**, không được giấu | **Bắt buộc** |
| **TN4** | **Đo hữu-ích/mạch-lạc** | `Student` vs `Student-RAW`, tập trung vào các bước từng bị viết lại | — | Không ngưỡng; **nằm trong family Holm** | **Bắt buộc** (đã khoá trong family) |
| **TN5** | **Hiệu chuẩn bộ chấm** | `bge-m3` vs người, 80–120 cặp gán tay | — | **Precision ≥ 0.95**, báo Cohen's κ, rồi freeze τB | **Bắt buộc** — không có nó thì mọi con số ở TN1/TN2 vô nghĩa |
| **TN6** | **Validate thước đo bằng bơm lỗi** | metric vs lỗi đã biết | — | detection **≥ 0.80**; false-positive **≤ 0.10**; đơn-điệu (Spearman — đo xu hướng đồng biến — phải < 0, p < 0.05) | **Bỏ được** — nếu không kịp thì **RÚT claim tương ứng khỏi bài báo**, không hứa suông |
| **TN7** | **Dose-response** | trộn 25%/50%/75% data lọc | Tắt | **CHƯA pre-register → chỉ báo dạng thăm dò (exploratory)**, không dùng làm bằng chứng chính | **Tuỳ chọn / Plan B** |

**Ba chỗ thầy có thể truy:**

**① Vì sao Tier 1 lại chấm ở điều kiện tắt VH, trong khi mục trước nói Tier 1 "VH vẫn bật"?** Đây là chỗ dễ đọc nhầm nhất trong toàn bộ thiết kế, nên phải nói cho chuẩn: cụm "VH vẫn có ở Tier 1" mô tả **bối cảnh triển khai** (hệ deploy đầy đủ vẫn còn lớp viết-lại phía sau), còn **phép đo `f` ở cả Tier 1 lẫn Tier 2 đều thực hiện trên output THÔ, giống hệt nhau** — chỉ khác **cặp đem ra so**. Lý do bắt buộc phải vậy: nếu chấm `f` *sau* lớp viết-lại thì cả `Student` lẫn `Student-RAW` đều sạch bong, Δ ≈ 0 → **null giả tạo**, thí nghiệm tự huỷ. Lợi ích của lớp viết-lại được báo riêng qua %fallback và lỗi-ngầm, không trộn vào `f`.

**② Có bất đối xứng nào không?** Có một chỗ, và luận văn khai trước: `f_teacher` ở Tier 2 chấm trên output sinh bằng prompt gốc của teacher — prompt đó **có** câu dặn "đừng bịa nút không có thật"; còn student thì bị hỏi bằng prompt **không** có câu đó. Bất đối xứng này **thiên về phía bất lợi cho student**, tức là nó làm phép so **khó hơn** cho phía ta, không dễ hơn. Đây là hướng sai lệch an toàn, nên khai thẳng ra sẽ có lợi cho lập luận.

**③ Vì sao `Student-RAW` là bắt buộc chứ không phải "có thì tốt"?** Vì nó là nhánh **duy nhất** tách được "giỏi lên nhờ lọc dữ liệu" khỏi "giỏi lên nhờ được fine-tune nói chung". Không có nó, mọi cải thiện đều có thể bị quy cho việc mô hình đơn giản là quen miền dữ liệu hơn. Nếu vì lý do gì buộc phải bỏ, kết luận phải **hạ cấp** xuống "chưa tách bạch được lọc-VH khỏi SFT nói chung" — mất gần hết giá trị.

---

## Nhánh nhiều màn hình — ngoài phạm vi mùa này, nhưng phải trả lời được khi thầy hỏi

> 🚩 **Mục này nói gì:** nhánh nhiều màn đã thiết kế xong và có trụ khoa học đầy đủ cho cả sáu thành phần, nhưng **cố ý không làm mùa này** — nó treo trên một cổng chưa chạy (K-pair), mà ba tháng thì không đủ để đánh cược vào một cổng chưa biết kết quả.
>
> Vì vậy phần này có mặt để **thủ sẵn khi thầy hỏi "còn nhiều màn hình thì sao?"**, chứ **không phải để xin thầy duyệt chạy**. Nếu trình nó như việc sẽ làm, khối lượng sẽ vượt 3 tháng — và quá tải đúng là rủi ro lớn nhất của đề tài này.

### Bài toán nhiều màn là gì

Thay vì một tấm ảnh, người dùng đưa **N tấm ảnh đã bị xáo trộn thứ tự** (ví dụ chụp lại cả một quy trình đăng ký gồm 5 màn nhưng thứ tự lộn xộn) cộng một mục tiêu. Hệ phải **tự khôi phục đúng thứ tự trước**, rồi mới viết hướng dẫn.

**Đây không phải một hệ thứ hai.** Nó là **đúng hệ một màn, cộng thêm một khối sắp thứ tự cắm ở đầu** (gọi là Stage-0). Khi N=1, Stage-0 rỗng và mọi thứ trở về đúng hệ một màn. Nhánh này *kế thừa* chứ không *thay thế* — nên công sức đã bỏ vào nhánh một màn không mất đi khi mở rộng sau này.

```
   N ảnh ĐÃ XÁO TRỘN  +  mục tiêu
        │
        ▼
   ┌──────────── STAGE-0 — khối THÊM MỚI ────────────┐
   │  ① hỏi từng CẶP: "màn nào đến trước?"            │
   │        (N=4 → 6 câu · N=5 → 10 câu)              │
   │             ▼                                    │
   │  ② COPELAND: đếm 'trận thắng' → xếp hạng         │
   │             ▼                                    │
   │  ③ có vòng cắn đuôi? → cắt ít dây nhất, cắt      │
   │     dây YẾU nhất (đo khách quan, KHÔNG hỏi       │
   │     model "mày chắc mấy %")                      │
   └──────────────────┬───────────────────────────────┘
                      ▼
              chuỗi màn ĐÃ SẮP
                      │
                      ▼
   ┌──── PIPELINE MỘT MÀN — kế thừa NGUYÊN VẸN ───────┐
   │  sinh nháp → đối chiếu VH → viết lại bước bịa     │
   └──────────────────┬───────────────────────────────┘
                      ▼
   CHẤM:  τ (thứ tự)  +  Step-SR (từng bước)  + bộ thước một màn

   ⚠ Đáp án vàng và VH CHỈ có ở khâu CHẤM —
     không bao giờ vào khâu sắp thứ tự hay khâu sinh.
     Che đồng hồ / pin / huy hiệu để model không đọc lỏm thứ tự.
```

### Khối sắp thứ tự hoạt động thế nào — ba nhịp

**Nhịp 1 — hỏi từng cặp.** Với N ảnh, hỏi mô hình từng cặp một: *"trong hai màn này, màn nào đến trước?"*. N=4 → 6 câu hỏi; N=5 → 10 câu. Cố ý **không** hỏi kiểu "sắp xếp cả N màn giúp tôi" (listwise) vì ba lý do: hợp với cỡ mô hình tầm trung, để lại **dấu vết kiểm tra được** (listwise là hộp đen), và cho phép **phát hiện mâu thuẫn nội tại**.

**Nhịp 2 — tổng hợp bằng Copeland.** Coi như một giải đấu vòng tròn: mỗi màn là một đội, mỗi câu hỏi cặp là một trận, "thắng" nghĩa là được xếp trước. Điểm Copeland của một màn = số màn khác mà nó được xếp trước. Sắp theo điểm từ cao xuống thấp là ra thứ tự.

> Ví dụ 4 màn A→B→C→D, hỏi đủ 6 cặp, mô hình trả lời đúng hết → cop(A)=3, cop(B)=2, cop(C)=1, cop(D)=0 → xếp A→B→C→D, trùng đáp án vàng.

**Nhịp 3 — phá vòng mâu thuẫn.** Mô hình có thể trả lời tự mâu thuẫn: A trước B, B trước C, **nhưng C trước A** — một vòng cắn đuôi, cả ba cùng 1 điểm, Copeland bó tay. Phải cắt bỏ một "dây" để hết vòng. Và đây là chỗ có một quyết định đáng nói.

> **Quyết định đáng trình thầy (điểm M2):** cách hiển nhiên là hỏi mô hình "mày chắc bao nhiêu phần trăm?" rồi cắt dây nó tự nhận là yếu. **Cách đó đã bị loại**, vì mô hình ngôn ngữ **hiệu chỉnh độ tự tin rất kém** — nó tự tin ngay cả khi sai. Tin lời tự khai của mô hình là rơi lại đúng cái bẫy "để hệ tự chấm mình". Thay vào đó, độ yếu của một dây đo bằng ba tín hiệu khách quan: **khoảng cách thắng** (thắng sát nút = dây yếu), **tính ổn định** (hỏi lại nhiều lần, câu trả lời lật qua lật lại = dây yếu), và **cắt ít nhất** (ưu tiên phương án cắt ít dây nhất).

> **Hộp kỹ thuật — trụ bình duyệt cho từng nhịp** (cả 6 thành phần đều đã xác minh venue):
> | Thành phần | Trụ |
> |---|---|
> | Hỏi pairwise | Qin et al., *LLMs are Effective Text Rankers with Pairwise Ranking Prompting*, **Findings of NAACL 2024**, pp. 1504–1518 |
> | Tổng hợp Copeland | Dwork, Kumar, Naor & Sivakumar, *Rank Aggregation Methods for the Web*, **WWW 2001**, pp. 613–622 |
> | Phá vòng (min feedback arc set) | Ailon, Charikar & Newman, *Aggregating Inconsistent Information*, **J. ACM 55(5), 2008** |
> | Tiền lệ tác vụ (xáo ảnh → sắp lại) | Agrawal et al., *Sort Story*, **EMNLP 2016**, pp. 925–931 |
> | Thước τ thứ-tự-bộ-phận | Fagin, Kumar, Mahdian, Sivakumar & Vee, *Comparing Partial Rankings*, **SIAM J. Discrete Math. 20(3):628–648, 2006** |
> | Tiền lệ dùng τ làm headline | Lapata, *Automatic Evaluation of Information Ordering*, **Computational Linguistics 32(4):471–484, 2006** |
> | Phân tích cue (stratification) | Gardner et al., *Contrast Sets*, **Findings of EMNLP 2020** — ⚠️ **trụ KHÁI NIỆM**, không phải trụ chính danh |
>
> **Khai thẳng:** luận văn **không phát minh** pairwise/Copeland/min-FAS/τ. Đóng khung đúng là: *bài đầu tiên ráp chúng thành một hệ sắp-màn-theo-mục-tiêu phục vụ sinh hướng dẫn, với chấm partial-order suy từ gold + phân tích cue.* Thành phần cue chỉ có trụ khái niệm, và đó chính là chỗ luận văn đóng góp thêm.

### Mô hình dựa vào đâu để biết màn nào trước — năm tín hiệu

Đây là câu hỏi hay nhất mà một hội đồng có thể hỏi ở nhánh này, và luận văn có câu trả lời có cấu trúc. Năm tín hiệu thứ tự:

1. **Điều kiện tiên quyết (gating)** — màn sau chỉ mở được sau khi làm xong một việc ở màn trước.
2. **Nút điều hướng** — sự có mặt của "Next / Back / Tiếp / Quay lại".
3. **Biến thiên trạng thái** — một công tắc chuyển bật/tắt, một ô từ trống thành đã điền, một huy hiệu số đổi.
4. **Tiêu đề tiến trình** — "Bước 1/3", "Bước 2/3"…
5. **Đi từ tổng quan vào chi tiết (drill-down).**

> **Hộp kỹ thuật.** Năm tín hiệu này **không bê từ một bài báo nào** — chúng là quan sát của chính luận văn (từng tín hiệu riêng lẻ đều là cơ chế điều hướng chuẩn trong HCI/GUI, nên không phải bịa; cái mới nằm ở *cách dùng chúng để quy kết*). Cách quy kết: **phân tầng một-cue** — chỉ giữ những cặp màn được phân biệt bởi **đúng một** tín hiệu, để cô lập ảnh hưởng từng loại. **Không che pixel** (tạo artifact lệch phân phối) và **không tin lời mô hình tự khai** đã dùng tín hiệu nào (không đáng tin). Phân định với Gardner: họ *can thiệp* vào dữ liệu để đổi nhãn vàng; ta chỉ *phân tầng* tập cặp quan sát sẵn — nên trình là "so sánh có kiểm soát, lấy cảm hứng từ contrast sets", không áp y nguyên.

### Đo bằng gì

Nhánh này **có đáp án vàng** (khác hẳn nhánh một màn), nên đo được trực tiếp. Hai thước:

**Thước τ — thứ tự bộ phận.** Không đòi hệ xếp trùng khít đáp án vàng, vì **không phải cặp nào cũng bắt buộc có thứ tự**: điền email trước hay điền số điện thoại trước đều đúng. Chỉ phạt những cặp **buộc phải đúng thứ tự**.

> **Hộp kỹ thuật.** ⚠️ **Cảnh báo ký hiệu:** chữ **τ** ở mục này (thước thứ tự) **không liên quan gì** tới `τA`/`τB` ở mục thước đo một màn (ngưỡng khớp embedding) — trùng chữ Hy Lạp, hai nghĩa hoàn toàn khác. Cả hai tên đều theo đúng quy ước của tài liệu gốc nên giữ nguyên, nhưng khi viết luận văn phải chú rõ chỗ này.
>
> `τ = (C − D)/|M| ∈ [−1, +1]`, với **M** = tập cặp bắt buộc, **C** = số cặp hệ xếp thuận chiều gold, **D** = nghịch chiều.
>
> **M suy từ đâu — điểm chống vòng lặp luận quan trọng nhất của nhánh này:** M suy **từ quỹ đạo vàng** bằng quy tắc nhân quả (màn B chỉ xuất hiện *sau* khi thực hiện một gold-action ở màn A ⇒ (A,B) ∈ M). **Không** lấy từ mô hình đang chấm, và **tuyệt đối không** suy từ bộ phát-hiện-cue mà chính hệ dùng để sắp. Quy tắc này là *xấp xỉ* → phải kiểm bằng audit người 50–80 cặp + đo độ nhạy khi gán nhãn sai 10%.
>
> **Ví dụ:** 4 màn A(mở form)→B(điền email)→C(điền sđt)→D(Gửi). Cặp (B,C) **tự do**; M = {(A,B),(A,C),(A,D),(B,D),(C,D)}, |M|=5. Hệ sắp A→C→B→D → cả 5 cặp bắt buộc đều thuận → τ = +1.0, **đúng hoàn toàn** dù thứ tự không trùng khít gold.
>
> **Cảnh báo đặt tên (dễ bị vặn):** đây là *tương quan thứ tự bộ phận* theo **Fagin 2006** + tiền lệ **Lapata CL 2006** — **KHÔNG phải "Kendall τ-b"**, đừng gọi nhầm. Định nghĩa |M| = số cặp bắt buộc suy từ gold là **định nghĩa riêng của luận văn**, không phải công thức nguyên bản của Fagin. Thước phụ: **PMR** = tỉ lệ episode sắp đúng trọn (τ = +1), thang [0,1].

**Thước Step-SR.** Tỉ lệ bước hệ làm đúng so với quỹ đạo vàng.

> **Hộp kỹ thuật + một cái bẫy phải biết.** `Step-SR = |{bước làm đúng}| / |{bước trong quỹ đạo vàng}|`; "đúng" = đúng loại thao tác **và** lệch toạ độ ≤ 14% (ngưỡng **mượn từ AITW, NeurIPS 2023** — không phải chuẩn ngành thống nhất, khai thẳng). Teacher-forced = mỗi bước đặt hệ vào đúng trạng thái gold rồi mới hỏi bước kế.
>
> **Bẫy:** Step-SR là **proxy chẩn đoán năng lực từng bước**, KHÔNG phải thước "làm tới đích". Chính bài AndroidControl (Li et al., NeurIPS 2024) cảnh báo step-accuracy *không* dự báo tốt xếp hạng theo người, và teacher-forcing **cố ý che lỗi tích luỹ**. Ngoài ra Step-SR là **cận dưới**: so với *một* quỹ đạo vàng, một hướng dẫn đúng nhưng đi đường khác vẫn bị tính sai.

### Bốn cổng phải qua trước khi tin bất kỳ con số nào

| Cổng | Kiểm gì | Ngưỡng | Trạng thái |
|---|---|---|---|
| **K-pair** | Độ chính xác so cặp **thô** của mô hình vs gold, đo **trước** khi tổng hợp Copeland | **> 0.5** (cận dưới CI). Nếu ≈ 0.5 (bằng đoán mò) → **toàn bộ khối sắp thứ tự vô hiệu về nguyên tắc, phải khai thẳng** | Cần chạy |
| **KN** | Histogram độ dài quy trình (có đủ quy trình dài không) | Định tính | **✅ GO** |
| **KZ'** | Prior-art sắp ảnh (có bị người khác làm trước không) | Định tính | **✅ GO** |
| **KB** | Chống rò rỉ chỉ số bước | Strip metadata + tái mã hoá ảnh + che status bar/đồng hồ/pin/huy hiệu + loại quy trình 2 ảnh trùng pixel | Cần chạy |

K-pair là cổng quan trọng nhất: nó **chặn toàn bộ nhánh nhiều màn**. Nếu fail, nhánh này không "bỏ" mà chuyển thành **một phát hiện âm tính hợp lệ** ("mô hình so cặp không hơn đoán mò trên miền GUI" — bản thân nó là một kết quả). Rò rỉ ở KB là chuyện có thật chứ không lo hão: trong dữ liệu đã tìm thấy đồng hồ hiện 5:33, mức pin, và huy hiệu số trên icon — mô hình chỉ cần đọc đồng hồ là biết thứ tự mà không cần hiểu gì về giao diện.

### Dữ liệu

> **Hộp kỹ thuật.** **AndroidControl** (Li et al., Google DeepMind, *On the Effects of Data Scale on UI Control Agents*, **NeurIPS 2024 Datasets & Benchmarks**; arXiv 2406.03679; **CC0**): 15.283 quy trình / 833 app / trung bình ~5,5 bước / p95 = 13.
> - **Mẫu đã chọn:** **286 episode, N ∈ {4,5,6}** — phân bố N = {4:107, 5:103, 6:76}, trải **237 app**, chỉ 1 app unknown. Cộng tầng N-dài: **48 ep, N ∈ {7..10}, 48 app**.
> - ⚠️ **Cảnh báo phải khai:** **194/237 app là singleton (chỉ 1 episode)** → số cụm danh nghĩa cao nhưng nhiều cụm cỡ 1. **Báo G thật + N_eff** (cỡ mẫu hiệu dụng sau khi trừ tương quan trong cụm)**, KHÔNG khoe "G=237 rất mạnh".**
> - ⚠️ **Provenance:** nguồn dùng là bản cộng đồng re-split (`smolagents/android-control`, test = 3.051 ≠ held-out chính thức). Vô hại về leakage vì luận văn chạy zero-shot, nhưng **phải khai khi viết**. **Không in "2.855" làm cỡ test** (là tổng 4 sub-split chồng nhau); số duy nhất sau khử trùng ≈ 1.540 — **chưa tự đếm lại, đừng trích như số chắc**.
> - Step-SR giữ N=1 (theo protocol gốc), tách khỏi 286 ep core.

### Vì sao cắt, và cắt đi đâu

Ba lý do, xếp theo sức nặng: **(1)** nhánh này **cần thêm thực nghiệm mới đủ chín** — cổng K-pair chưa chạy, histogram độ dài quy trình mới xong; **(2)** lịch 3 tháng đã kín cho nhánh một màn (tuần 8–10 là viết luận văn); **(3)** nhánh một màn đã tự khép kín thành một câu chuyện hoàn chỉnh, không cần nhiều màn để đứng vững.

Cắt đi đâu: để dành cho **bài báo mở rộng tiếng Anh sau này**, đúng theo kế hoạch tách hai bài. Trục phân định giữa hai nhánh cũng sạch sẽ về mặt khoa học: **có quỹ đạo vàng để chấm hay không** — một màn thì không có (nên mới cần phương pháp đo không-đáp-án-mẫu), nhiều màn thì có.

**Câu trả lời gọn khi thầy hỏi "sao không làm luôn nhiều màn?":** *"Khối sắp thứ tự đã thiết kế xong, có trụ bình duyệt đầy đủ cho cả sáu thành phần, và dữ liệu đã chọn mẫu xong — nhưng nó còn một cổng chưa chạy (K-pair), mà nếu cổng đó rớt thì cả nhánh vô hiệu. Em không muốn đánh cược ba tháng vào một cổng chưa biết kết quả, trong khi nhánh một màn đã đủ khép kín để thành luận văn. Nhiều màn để dành cho bài mở rộng sau."*

---

## Thứ tự bắt buộc trước khi chạm vào code hoặc tốn tiền — không được đảo

Có đúng hai việc phải xong trước, theo đúng thứ tự này, trước khi gọi bất kỳ lệnh nào tốn tiền hoặc tốn thời gian đáng kể — kể cả bước chạy thử thầy giáo trên vài chục màn để đo chi phí:

1. **Sinh và khoá danh sách ứng dụng train/test** (file mô tả ở Bước 0, Phụ lục D) — lưu vào hệ quản lý phiên bản ngay lập tức, không sửa sau khi đã lưu.
2. **Tính "mức chênh lệch nhỏ nhất có thể phát hiện được" bằng số liệu thật** (không phải số đoán — công thức ở mục "Bộ thước đo đầy đủ"), rồi khoá toàn bộ quy tắc thắng-thua (định nghĩa "đủ lớn", ngưỡng, ba kết cục của cả hai tầng) vào một bản ghi không sửa được nữa, cũng lưu vào hệ quản lý phiên bản.

Chỉ sau khi cả hai việc này đã khoá xong mới được chạy bước tốn tiền đầu tiên. Đảo thứ tự (chạy thử trước, tính ngưỡng sau khi đã lỡ thấy vài con số) sẽ làm hỏng toàn bộ giá trị của quy tắc "đăng ký trước" — thấy số rồi mới đặt ngưỡng thì ngưỡng nào cũng "vừa khít" một cách giả tạo, không còn ý nghĩa kiểm chứng gì nữa.

---

## Lịch trình và chi phí

Toàn bộ công việc dự kiến gói trong khoảng mười tuần, dùng Google Colab (một dịch vụ cho thuê máy tính có card đồ hoạ theo tháng) làm nơi huấn luyện.

| Tuần | Việc chính |
|---|---|
| 1 | **Cổng TN0 trước đã:** khoá danh sách app → pilot đo phương sai nền → tính MDE → khoá ngưỡng. **Chỉ sau khi khoá xong** mới: sinh câu hỏi, gọi thầy giáo, lọc sạch, chạy thử 20 mẫu để chắc quy trình không lỗi |
| 2–3 | Huấn luyện đầy đủ cả hai bản mô hình (bản học từ dữ liệu sạch và bản đối chứng học từ dữ liệu thô). **Ngay khi có bản lưu tạm đầu tiên: thử xuất mô hình ra dạng chạy nhẹ (GGUF)** — bước này từng có lỗi thật với đúng dòng mô hình này, phải phát hiện sớm chứ không đợi train xong |
| 4 | Đệm: xử lý lỗi xuất mô hình nếu tuần 2–3 phát hiện, dựng script đánh giá |
| 5–7 | Chạy hai tầng đánh giá, tính toán thống kê |
| 8–10 | Viết luận văn |

Chi phí ước tính khoảng 70–100 đô-la, chủ yếu là tiền thuê máy tính có card đồ hoạ (phần gọi thầy giáo chỉ tốn 1–2 đô).

### Quy ra công sức thật — bao nhiêu ngày làm việc

Bảng tuần ở trên là lịch part-time có buffer. Nếu quy ra **ngày làm việc tập trung 10 tiếng**, con số thật như sau. Cách tính: lúc GPU đang huấn luyện (3–6 tiếng mỗi lần) **không phải ngồi canh máy** — thời gian đó chồng lấn với việc viết script cho bước sau, hoặc để chạy qua đêm. Nên tính theo ngày-làm-việc thực tế, **không cộng cứng "giờ người + giờ GPU"** (sẽ đếm trùng).

| Giai đoạn | Gồm những gì | Ngày (10h) |
|---|---|---|
| **Chuẩn bị dữ liệu** | khoá split · tải + lọc MobileViews · sinh câu hỏi · gọi thầy giáo · đối chiếu + viết lại · đóng gói · hiệu chuẩn bộ chấm | ~4–6 |
| **Huấn luyện** | dựng Colab/LLaMA-Factory (lần đầu hay vướng) · smoke-test 20 mẫu · train Student + Student-RAW · debug/train lại · test xuất GGUF | ~3–5 |
| **Đánh giá** | viết eval-tắt-VH · chạy Tier 1 + Tier 2 · chấm 3 cơ chế · thống kê (sign-flip/MDE) · đo hữu-ích | ~3–4 |
| **Cộng phần một màn** | | **~10–15 ngày** |

| Kịch bản | Ngày |
|---|---|
| Lý tưởng, chạy trơn | **~10–15 ngày** |
| Thực tế, +30–40% ma sát (cài môi trường, hết VRAM, Colab rớt phiên, lỗi xuất GGUF, train lại) | **~14–21 ngày** |

**Ba lưu ý về bảng này:**
- **Chưa gồm viết luận văn** — thêm khoảng **10–15 ngày** nữa.
- **Nhánh nhiều màn nếu làm** sẽ tốn thêm ~5–6 ngày và ~$10 — nhưng nó **nằm ngoài đường găng** của mốc 3 tháng, nên không tính vào đây.
- **Mẹo đáng giá:** xếp lệnh train chạy **qua đêm** → giờ GPU thành thời gian rảnh miễn phí, đây là cách rút ngắn lịch thật sự hiệu quả nhất khi làm một mình.

---

## Rủi ro lớn nhất, và phương án dự phòng

Rủi ro lớn nhất không nằm ở kỹ thuật, mà ở chỗ toàn bộ giá trị "tính mới" của luận văn đang đặt cược vào đúng một câu hỏi (Tier 2) có thể ra kết quả rỗng. Nếu không chuẩn bị trước, một kết quả rỗng dễ bị hiểu nhầm thành "luận văn thất bại" — đúng điều thầy từng phê bình.

Cách phòng ngừa, theo thứ tự ưu tiên:

Chạy và có kết quả của Tier 1 càng sớm càng tốt (trong khoảng một tháng đầu) — đây là "khoản bảo hiểm" chắc chắn nhất, gần như luôn có số đẹp để trình bày dù chuyện gì xảy ra ở Tier 2.

Nói thẳng với thầy về khả năng Tier 2 có thể ra kết quả rỗng ngay từ lúc trình bày đề cương, thay vì đợi có số liệu xấu mới giải thích — việc chủ động nói trước khiến một kết quả rỗng (nếu xảy ra) được hiểu là một phát hiện khoa học trung thực, chứ không phải một lời bào chữa muộn màng.

Đặt thêm một mốc kiểm tra nội bộ ở khoảng hai phần ba thời gian: nếu đến lúc đó Tier 1 còn chưa chạy ổn định, chủ động hạ Tier 2 xuống thành một mục thử nghiệm phụ trong luận văn, không đánh cược toàn bộ vào sát ngày nộp.

Chạy thêm phép đo trộn tỉ lệ (TN7 ở bảng thí nghiệm): nếu độ trung thực tăng dần đều theo tỉ lệ dữ liệu đã lọc, đó là bằng chứng bổ sung cho "thói quen thành thật đến từ bước lọc" — trình bày được ngay cả khi phép kiểm định nhị phân ở Tier 2 không đạt ngưỡng. Lưu ý: chưa đăng ký trước nên chỉ báo dạng thăm dò.

---

## Việc phải làm trước khi chốt với thầy

Chạy thử quy mô nhỏ (5–10 ứng dụng) để xác nhận toàn bộ quy trình chạy được thật, không chỉ đúng trên giấy — nhiều con số trong kế hoạch (thời gian train, VRAM cần) vẫn là ước tính nội suy từ nghiên cứu khác, chưa phải số đo của chính cấu hình này.

Và bảy vòng tranh luận đã chạy vẫn không thay được việc ngồi trao đổi trực tiếp với thầy.

---

Đến đây là hết phần cần đọc để hiểu luận văn. Phần dưới là phụ lục kỹ thuật — chỉ cần mở khi thật sự bắt tay code hoặc cần một con số/công thức cụ thể, không cần đọc để nắm bức tranh chung.

---
---

# PHẦN PHỤ LỤC — TOÀN BỘ CHI TIẾT KỸ THUẬT (gộp từ các vòng debate, không cần mở file nào khác)

> Phần này dài và kỹ thuật hơn hẳn phần trên, viết cho lúc thật sự ngồi vào code hoặc cần trích một con số cụ thể ra khỏi file. Không cần đọc tuần tự — dùng mục lục dưới để nhảy tới đúng chỗ cần.

**Mục lục phụ lục:**
- A. Lịch sử quyết định — vì sao các hướng khác bị loại
- B. So sánh đầy đủ với từng nghiên cứu liên quan (tính mới)
- C. Cấu hình mô hình + file YAML train thật
- D. Data pipeline — từng bước, schema JSON, script cần viết
- E. Rủi ro kỹ thuật + cách né
- F. Ba bộ dữ liệu — venue · giấy phép · quy mô · schema · bẫy toạ độ · điều kiện trước khi in
- G. Bản đăng-ký-trước — toàn văn ngưỡng đã khoá (Tier 1/Tier 2 · 3 kết cục · code kiểm định · 4 bản vá)
- H. Bản đồ các vòng debate đã chạy (chỉ để tra cứu)

---

## Phụ lục A — Lịch sử quyết định: vì sao các hướng khác bị loại

Trước khi chốt "Faithful Distillation", có ba hướng khác từng được cân nhắc nghiêm túc và bị loại sau khi bị mang ra tranh luận đối kháng:

**Hướng 1 — huấn luyện một mô hình "bấm đúng nút" (grounding), dùng chính thước đo không-cần-đáp-án-mẫu làm phần thưởng để huấn luyện bằng học tăng cường (RLVR).** Nghe hấp dẫn vì biến thẳng phương pháp đánh giá thành tín hiệu huấn luyện. Nhưng bị bác vì ba lý do: (1) một thứ vừa dùng để huấn luyện vừa dùng để chấm điểm chính nó dễ rơi vào vòng lặp tự-khen (giống lỗi từng gặp ở bản pipeline cũ, khi bộ lọc vừa sửa vừa chấm khiến điểm trung thực ảo lên gần 100%); (2) việc "bấm đúng nút" không phải bước mà thầy chê thiếu — bước thầy chê là bước *viết ra hướng dẫn*, nên dù có huấn luyện xong phần bấm nút, phần viết hướng dẫn vẫn chỉ là gọi API, không giải quyết đúng lời phê bình; (3) việc này trùng khá nhiều với các nghiên cứu GUI-agent-bấm-máy đã có (UI-R1, SE-GUI, GUI-Actor).

**Hướng 2 — một mô hình nhỏ chuyên "học phát hiện bịa" từ dữ liệu tự chế (bơm lỗi có chủ đích rồi để mô hình học nhận ra).** Có vẻ đúng trọng tâm hơn, nhưng lại rơi vào một vòng lặp tương tự: mô hình chỉ học lại đúng cách mà bộ bơm-lỗi tạo ra lỗi giả, không chắc bắt được lỗi bịa thật của một AI khác khi triển khai thật.

**Hướng 3 — dùng học tăng cường để huấn luyện thẳng phần viết-hướng-dẫn, lấy điểm-trung-thực làm phần thưởng.** Cũng bị cân nhắc và loại: mô hình có xu hướng "lách luật phần thưởng" — học cách không bao giờ nêu tên nút cụ thể nữa, chỉ mô tả chung chung mọi lúc, để tối đa điểm trung thực một cách giả tạo. Kết quả là điểm trung thực rất cao nhưng hướng dẫn vô dụng — không phải thói quen luận văn muốn dạy.

Sau khi cả ba hướng trên bị loại, hướng "Faithful Distillation" — dạy một mô hình nhỏ thói quen thành thật bằng cách chỉ cho nó học từ dữ liệu đã lọc sạch — được chọn vì giữ đúng trọng tâm mà thầy yêu cầu (bước sinh hướng dẫn có mô hình tự train), không rơi vào vòng lặp tự-chấm, và có một câu hỏi thực nghiệm thật (mô hình có nội tại hoá được thói quen đó hay không) thay vì một kết quả biết trước.

---

## Phụ lục B — So sánh đầy đủ với các nghiên cứu liên quan

Bảng dưới đây là kết quả sau khi để năm góc nhìn khác nhau cố tình tìm cách chứng minh "cái này không có gì mới", rồi kiểm chứng lại từng lý lẽ tấn công đó có đúng sự thật hay không (một trong năm lý lẽ tự sụp vì trích dẫn sai nguồn — quy trình kiểm chứng bắt được).

| Nghiên cứu | Năm / nơi công bố | Giống ở đâu | Khác ở đâu |
|---|---|---|---|
| STaR / RFT (Zelikman) | 2022 | Công thức tổng quát "sinh → lọc → huấn luyện lại" đã có tên từ đây, không phải phát minh của luận văn | Luận văn áp dụng công thức này cho đúng tình huống rủi ro cao (bịa nút bấm trên giao diện thật), với nguồn kiểm tra bên ngoài có cấu trúc |
| KnowAda (Yanuka và cộng sự) | NAACL 2025, hạng mục trình bày miệng | Cơ chế "viết lại phần không kiểm chứng được thành mô tả chung chung" gần như giống hệt bước viết-lại-bịa của luận văn | KnowAda để chính mô hình tự hỏi-tự-trả-lời để đoán nó có "biết" phần đó không (tự chấm mình); luận văn đối chiếu với VH, không phụ thuộc năng lực tự nhận thức của mô hình. Rủi ro khi sai cũng khác hẳn: KnowAda sai một chi tiết mô tả ảnh là vô hại, còn ở đây sai là người dùng bấm nhầm nút thật |
| BLIP — CapFilt | ICML 2022 | Có đúng kỹ thuật "sinh rồi lọc" và từng đo tách riêng giá trị của bước lọc (giống thí nghiệm Tier 1 của luận văn) | Không đo xem hành vi đã học có còn giữ được khi *không còn gì để lọc nữa lúc dùng thật* — đây là câu hỏi Tier 2, CapFilt chưa từng hỏi |
| VGA — Vision GUI Assistant | Hạng mục Findings, EMNLP 2024 | Cũng dùng đúng loại "VH" để giảm bịa khi huấn luyện một mô hình cho giao diện điện thoại, phục vụ người đọc chứ không phải agent bấm máy | VGA ép mô hình phải bám vào VH *ngay từ lúc sinh* (kiểu viết-có-ràng-buộc); luận văn để mô hình sinh tự do trước, rồi mới lọc sau — giữ được khả năng học từ đúng những chỗ mô hình lớn "tự nhiên" hay sai |
| FaithDial / BEGIN (Dziri và cộng sự) | Tạp chí TACL, 2022 | Cũng viết lại câu trả lời bịa dựa trên đối chiếu với một nguồn tri thức có cấu trúc | FaithDial coi câu trả lời mơ hồ/chung chung là một *lỗi cần sửa tiếp*; luận văn coi mô tả chung chung là một *chiến lược có chủ đích* để né bịa mà vẫn giữ được ích lợi |
| Nhóm nghiên cứu GUI-agent gần đây (WinDOM, Trust-the-Right-Teacher, LiteGUI, CORA) | Đều công bố năm 2026 | Cũng lọc dữ liệu rồi huấn luyện lại một mô hình nhỏ chạy trên máy cho giao diện điện thoại | Nhóm này kiểm tra đúng-sai bằng hình học (toạ độ chạm có nằm trong khung nút không) để phục vụ agent tự bấm máy; luận văn kiểm tra bằng đối chiếu ngôn ngữ (tên nút được nhắc có khớp với danh sách nút thật không) để phục vụ người đọc — khi bị bịa, agent chỉ có hai lựa chọn là bấm hoặc dừng lại, còn văn bản tự do có thể mô tả mơ hồ mà vẫn hữu ích, agent không có tương đương cho việc này |

Câu trả lời ngắn khi bị hỏi lại đã có ở phần chính của file này (mục "Cái mới ở đây là gì").

---

## Phụ lục C — Cấu hình mô hình và file huấn luyện

| Hạng mục | Lựa chọn đã chốt | Vì sao |
|---|---|---|
| Mô hình học trò | Qwen2.5-VL-3B-Instruct | Mô hình mở, đủ nhỏ để chạy trên máy cá nhân, có tiền lệ huấn luyện thành công (ZonUI-3B, công bố 2026) |
| Công cụ huấn luyện | LLaMA-Factory | Có sẵn ví dụ huấn luyện đúng dòng mô hình này, xử lý sẵn việc chỉ tính điểm-sai (loss) trên phần mô hình tự viết, không tính trên câu hỏi |
| Cách nén để vừa máy yếu | QLoRA 4-bit (lượng tử hoá) — dùng mặc định, không phải phương án dự phòng | Google Colab không đảm bảo luôn cấp đúng loại card đồ hoạ mạnh, nên chọn phương án chạy được cả trên card yếu nhất |
| "Miếng dán" LoRA | rank 8, hệ số 16, chỉ gắn vào phần "nói" của mô hình (không đụng phần "nhìn") | Có tiền lệ thật xác nhận đúng cấu hình này chạy được với đúng mô hình 3B này trên một card đồ hoạ phổ thông |
| Độ chính xác số học | fp16 trên card đời cũ (T4), bf16 trên card đời mới (L4/A100) — tự động chọn | Đặc điểm phần cứng đã công bố, không phải đoán |
| Đầu vào lúc huấn luyện/sử dụng | Chỉ ảnh và câu hỏi — không bao giờ đưa VH vào | Giữ đúng nguyên tắc "học trò phải tự lo được, không được học tủ" |
| Số lượng mẫu | Dải thiết kế 1.500–3.000 mẫu; ước tính thật từ ~574 màn = **1.700–2.870** (nằm gọn trong dải) | Đủ cho quy mô LoRA nhỏ, ước tính chi phí gọi thầy giáo chỉ vài đô-la |
| Số bản train | Hai bản — bản học từ dữ liệu đã lọc và bản đối chứng học từ dữ liệu thô | Bắt buộc, không phải tuỳ chọn — đây là cách duy nhất tách bạch "cải thiện vì lọc sạch" khỏi "cải thiện vì huấn luyện nói chung" |

File cấu hình thật (dùng trực tiếp với LLaMA-Factory):

```yaml
model_name_or_path: Qwen/Qwen2.5-VL-3B-Instruct
image_min_pixels: 200704
image_max_pixels: 1003520
trust_remote_code: true

stage: sft
do_train: true
finetuning_type: lora
lora_rank: 8
lora_alpha: 16
lora_dropout: 0.05
lora_target: q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj
freeze_vision_tower: true
freeze_multi_modal_projector: true
quantization_bit: 4
quantization_method: bnb

dataset: faithful_gui_train
template: qwen2_vl
cutoff_len: 2048
train_on_prompt: false

output_dir: /content/drive/MyDrive/thesis_ckpt/qwen25vl3b_faithful_lora
save_steps: 50
save_total_limit: 3
resume_from_checkpoint: auto

per_device_train_batch_size: 1
gradient_accumulation_steps: 16    # đổi thành 8 nếu chắc chắn có card L4/A100
learning_rate: 1.0e-4
num_train_epochs: 3.0
lr_scheduler_type: cosine
warmup_ratio: 0.05
bf16: false        # đổi true nếu card là L4/A100
fp16: true
gradient_checkpointing: true

val_size: held_out_by_app
eval_strategy: epoch
```

Ghi chú độ tin cậy: tốc độ học (1e-4), số vòng lặp (3 epoch), và cách chia batch trong bảng trên là **ước tính hợp lý nội suy từ các trường hợp tương tự, chưa phải số đo thật cho đúng quy mô dữ liệu này** — cần xác nhận lại bằng lần chạy thử nhỏ trước khi tin tưởng hoàn toàn. Riêng cấu hình LoRA (rank/hệ số/phần đóng băng) có tiền lệ xác nhận trực tiếp (ZonUI-3B), đáng tin hơn.

---

## Phụ lục D — Data pipeline: từng bước, schema, script cần viết

**Bước 0 — khoá danh sách ứng dụng train/test trước tiên, lưu vào hệ quản lý phiên bản ngay khi tạo:** file `harness/train_eval_app_split.json` ghi rõ 18 ứng dụng dùng để dạy và 12 ứng dụng chỉ dùng để kiểm tra (lấy từ 30 ứng dụng MobileViews đã qua vòng kiểm tra chất lượng trước đó), cộng thêm quy tắc: bất kỳ ứng dụng nào mở rộng thêm sau này để lấy thêm dữ liệu train cũng phải được đối chiếu, đảm bảo không trùng với 12 ứng dụng test dù chỉ một màn hình.

**Bước 1 — mở rộng thêm dữ liệu train (✅ ĐÃ CHẠY 12/7/2026):** kho MobileViews công khai trên HuggingFace thực tế chỉ có 4 file dữ liệu chia sẵn, hai file đầu đã dùng ở bản thử trước, còn hai file sau (`MobileViews_300000-400000.parquet` và `MobileViews_400000-522301.parquet`) chưa dùng — lấy thêm từ đây được khoảng 231.000 dòng dữ liệu mới (con số 600.000 hay thấy trong tài liệu quảng bá gồm cả một định dạng khác không tương thích trực tiếp với code hiện có, không dùng được ngay).

**Kết quả thật** (`fetch_mv_expand_train.py` + `dg3_dedup_pool.py`, dedup theo tên + perceptual hash (dHash)): **498 màn / 220 app** — con số và cách đọc nó xem mục "Dữ liệu lấy từ đâu" ở phần chính, không lặp lại ở đây.

**Hiện vật nằm ở đâu (đối chiếu được ngay):** ảnh + VH của pool nằm ở `dataset_samples/mv_train_pool/` (498 file `.jpg`, mỗi file kèm một `.viewhierarchy.json`; các màn bị loại vì trùng nằm trong `mv_train_pool/_dupes/`).

⚠️ **Một việc còn nợ, phải làm trước khi build data SFT:** trường `train_pool_expanded` trong `harness/train_eval_app_split.json` **hiện vẫn là mảng rỗng** — danh sách 220 app mở rộng mới chỉ tồn tại dưới dạng file ảnh trên đĩa, chưa được ghi vào file split đã commit. Cần đổ danh sách này vào đó rồi commit, để split-đã-khoá phản ánh đúng dữ liệu thật sự đem đi train (xem thêm ô tương ứng ở Phụ lục G).

Dedup dùng **hai lớp**: theo tên app, **cộng** theo ảnh-giống-nhau (perceptual hash) — hai app khác tên có thể dùng chung khuôn giao diện y hệt, so tên sẽ bỏ sót đúng ca đó. Chi tiết rủi ro: Phụ lục E (#7).

**Bước 2 — sinh câu hỏi tình huống:** dùng một mô hình nhỏ chạy miễn phí trên máy (không tốn API) để tạo vài câu hỏi hợp lý cho mỗi màn hình.

**Bước 3 — gọi thầy giáo (gpt-4o-mini) viết hướng dẫn nháp — bước duy nhất tốn tiền, cần hỏi ý kiến trước khi chạy thật.** Ước tính chi phí dựa trên lần chạy thử trước: khoảng 1–2 đô-la cho vài nghìn lượt gọi, nhưng nên đo lại chi phí thật trên một mẫu nhỏ trước khi chạy toàn bộ.

**Bước 4 — đối chiếu với VH:** dùng lại đúng thuật toán so khớp đã có sẵn (dựa trên một mô hình nhúng văn bản chạy miễn phí trên máy, ngưỡng khớp đã được chốt từ trước).

**Bước 5 — viết lại phần bịa thành mô tả chung chung, bằng khuôn mẫu cố định, KHÔNG dùng thêm AI để viết lại.** Đây là một quyết định thiết kế quan trọng: nếu dùng AI để "viết lại cho hay", chính bước lọc lại có thể mở ra một chỗ bịa mới. Khuôn mẫu ví dụ: "Tìm và chạm vào tuỳ chọn trên màn hình phù hợp để [ý định của bước này]." — nếu câu này vô tình lại trùng khớp với một tên nút thật nào đó, hệ thống tự động đổi sang một trong vài câu dự phòng trung tính đã chuẩn bị sẵn.

**Bước 6 — đóng gói thành định dạng huấn luyện.** Mỗi mẫu dữ liệu gồm: một ảnh, một câu hỏi, và một hướng dẫn (đã lọc sạch). Câu hỏi dùng để huấn luyện phải giống hệt câu hỏi dùng lúc đánh giá sau này ("Hãy viết hướng dẫn từng bước cho một người dùng thực hiện trên điện thoại để: ...") — giữ nguyên như vậy để không ai có thể nói kết quả khác nhau chỉ vì đổi cách hỏi.

Có một chỗ cố ý làm khác với thầy giáo, để bịt một lỗ hổng chắc chắn sẽ bị hỏi: câu hỏi cho học trò **KHÔNG** chứa dặn dò kiểu "đừng bịa ra nút không có thật" — trong khi câu nhắc cho thầy giáo (lúc sinh dữ liệu nháp) CÓ đúng câu này. Nếu học trò cũng được nhắc câu đó, sẽ không ai chứng minh được rằng thói quen thành thật của học trò đến từ việc huấn luyện trên dữ liệu đã lọc sạch, chứ không phải chỉ đơn giản đến từ một câu dặn dò thêm vào lúc hỏi.

Ví dụ một dòng dữ liệu thật (định dạng LLaMA-Factory):
```json
{
  "id": "mv__aucommixfm4sss_s1__q0",
  "conversations": [
    {"from": "human", "value": "<image>\nWrite step-by-step instructions for a person to follow on their phone, to: \"How do I turn on notifications for new episodes?\""},
    {"from": "gpt", "value": "1. Tap \"Settings\"\n2. Tap \"Notifications\"\n3. Look for the option on this screen that matches what you need for this step, and tap it.\n4. Toggle \"New episode alerts\""}
  ],
  "images": ["mv_train_pool/aucommixfm4sss_s1.jpg"]
}
```

**Bước 7 — hiệu chuẩn độ tin cậy của BỘ LỌC (bước 4, tức `nomic` + τA).** ⚠️ **Đừng lẫn với TN5**, vốn hiệu chuẩn **bộ CHẤM** (`bge-m3` + τB) — đây là hai bộ khác nhau, phải hiệu chuẩn riêng, đúng theo nguyên tắc "thứ dùng để lọc không được dùng lại để chấm". Cách làm: lấy khoảng 100–120 thao tác đã có đáp án đúng sẵn từ bộ dữ liệu AndroidControl (tránh 237 ứng dụng đã chọn mẫu cho nhánh nhiều màn — nhánh đó để dành bài mở rộng, xem mục "Nhánh nhiều màn hình") để đo xem thuật toán đối chiếu đúng bao nhiêu phần trăm — báo cáo độ chính xác/độ bao phủ và một chỉ số đồng thuận chuẩn (Cohen's kappa).

**Script cần viết mới:** `dg3_freeze_split.py` (khoá danh sách app), `fetch_mv_expand_train.py` (sửa từ `fetch_mv_expand.py` có sẵn — thêm phần tải 2 file dữ liệu chưa dùng + loại trừ theo danh sách đã khoá + đối chiếu ảnh-giống-nhau ở Bước 1), `dg3_train_questions.py` (sinh câu hỏi), `dg3_rewrite_fallback.py` (viết lại bằng khuôn mẫu), `dg3_render.py` (đóng gói dữ liệu), `dg3_eval_no_vh.py` (chạy đánh giá Tier 2), cộng với file cấu hình huấn luyện đã có ở Phụ lục C. Các phần còn lại (gọi thầy giáo, thuật toán đối chiếu) tái sử dụng nguyên script đã viết cho bản thử nghiệm trước đó.

---

## Phụ lục E — Toàn bộ rủi ro kỹ thuật đã rà soát + cách né

| # | Rủi ro | Cách né |
|---|---|---|
| 1 | Đoán sai tên file dữ liệu khi tải thêm từ kho MobileViews, dẫn đến lỗi không tải được | Dùng đúng tên file đã xác nhận: `MobileViews_300000-400000.parquet` và `MobileViews_400000-522301.parquet`; hạ kỳ vọng số lượng dữ liệu mới xuống khoảng 231.000 dòng, không phải 600.000 |
| 2 | Thiếu một khối cấu hình nhỏ trong file mô tả dữ liệu, khiến công cụ huấn luyện đọc sai vai trò câu hỏi/câu trả lời | Thêm tường minh khối `tags` mô tả rõ vai trò từng phần trong file cấu hình dữ liệu |
| 3 | Card đồ hoạ yếu (loại 16GB) có thể vẫn hết bộ nhớ nếu tăng độ phân giải ảnh hoặc kích thước lô dữ liệu | Giữ nguyên phương án nén 4-bit làm mặc định; nếu vẫn hết bộ nhớ, hạ thêm độ phân giải ảnh đầu vào |
| 4 | Bước xuất mô hình ra định dạng chạy nhẹ (để đánh giá miễn phí trên máy) từng có báo lỗi thật với đúng dòng mô hình này ở một công cụ phổ biến | Kiểm tra bước xuất này ngay từ sớm (đầu giai đoạn huấn luyện, ngay khi có bản lưu tạm đầu tiên), chuẩn bị sẵn hai phương án dự phòng nếu lỗi xảy ra |
| 5 | Google Colab không đảm bảo luôn cấp đúng loại card đồ hoạ đã đăng ký, kể cả bản trả phí | Luôn kiểm tra loại card ngay đầu mỗi phiên làm việc, tự động chọn cấu hình phù hợp thay vì giả định cố định |
| 6 | Việc lưu bản huấn luyện tạm ra bộ nhớ đám mây có thể thất bại giữa chừng nếu mất kết nối | Lưu tạm trên máy ảo trước, sau đó sao chép ra đám mây có thử lại nếu thất bại, kiểm tra file tồn tại sau khi sao chép xong |
| 7 | Phần dữ liệu mở rộng thêm để train có thể vô tình chứa lại đúng ứng dụng đã dành riêng để test, ở một màn hình khác — HOẶC hai ứng dụng khác tên nhưng dùng chung khuôn giao diện y hệt | Đối chiếu và loại bỏ tường minh mọi trùng lặp theo TÊN ứng dụng, **cộng thêm** đối chiếu ảnh-giống-nhau-về-thị-giác (perceptual hash) cả trong nội bộ dữ liệu train lẫn giữa train và 12 ứng dụng test — hai lớp phòng thủ này bổ sung cho nhau, không thay thế nhau. Ghi log xác nhận không còn trùng trước khi huấn luyện |
| 8 | Nếu bỏ qua bản đối chứng (học từ dữ liệu thô) vì lý do chi phí, sẽ không tách bạch được nguyên nhân thật của bất kỳ cải thiện nào | Bắt buộc phải huấn luyện cả hai bản; nếu buộc phải bỏ, phải hạ thấp mức độ chắc chắn của mọi kết luận rút ra và ghi rõ giới hạn này |
| 9 | Cấu hình "miếng dán" LoRA hiện chỉ có đúng một tiền lệ xác nhận trực tiếp, không phải nhiều nguồn hội tụ | Ghi rõ trong luận văn đây là điểm khởi đầu hợp lý cần tự xác nhận lại bằng theo dõi quá trình huấn luyện, không phải con số "đã chứng minh tối ưu" |
| 10 | Pool train mở rộng **không qua vòng lọc chất lượng kỹ** như 30 app gốc (quy mô của nó: xem mục "Dữ liệu lấy từ đâu") | Khai thẳng trong luận văn rằng pool mở rộng chỉ qua lọc tự động; nếu thiếu dữ liệu thì resume fetch, bỏ qua app đã có |
| 11 | MDE bị đánh giá thấp giả tạo nếu SD chỉ lấy từ một phía (thầy giáo) thay vì cả hai phía | Dùng cận trên thận trọng (cộng phương sai hai phía); MDE > 15-20 điểm phần trăm → tăng lên 15/15 TRƯỚC khi khoá pre-reg |

---

## Phụ lục F — Ba bộ dữ liệu: chi tiết đã xác minh tận file

> Phụ lục này gộp trọn chương dữ liệu (gộp từ `report/44` + `report/48`) để không phải mở file khác. Mọi con số dưới đây **đã verify tận file thật**, không lấy từ tài liệu quảng bá.

### Bảng so sánh nhanh ba bộ

| | **MobileViews** | **AndroidControl** | **ScreenSpot-v2** |
|---|---|---|---|
| **Nơi công bố** | ⚠️ **preprint arXiv 2409.14337, CHƯA bình duyệt** | ✅ **NeurIPS 2024 Datasets & Benchmarks** (đã bình duyệt) | ✅ phát hành kèm **OS-Atlas, ICLR 2025**; gốc ScreenSpot từ **SeeClick, ACL 2024** |
| **Giấy phép** | MIT | CC0 1.0 | apache-2.0 |
| **Thu thập** | **Bot tự động** (VLM + DroidBot, 200+ môi trường Android song song) | **Người thật**, ~20 annotator, điện thoại Pixel, kéo dài ~1 năm | Người gán thủ công, v2 hiệu đính tay |
| **Có đáp án vàng?** | ❌ Không | ✅ Có (gold action mỗi bước) | — (chỉ bbox) |
| **Vai trò** | **Một màn** — nguồn ảnh + VH để đối chiếu | **Nhiều màn** — ngoài phạm vi mùa này | Đối chứng grounding — **đã hạ vai** |
| **Luận văn dùng** | **127 màn / 30 app** (pilot) **+ 498 màn / 220 app** (mở rộng, đã chạy) | 286 episode / 237 app (không dùng mùa này) | 501 item mobile (không dùng mùa này) |

**Điểm cần chủ động khai với thầy:** bộ dữ liệu chính (MobileViews) là **preprint chưa bình duyệt**. Cách xử lý đúng: đóng khung nó là **hiện vật kỹ thuật** (một kho ảnh + VH), không phải một trụ khoa học; phần credibility bù bằng hai bộ đã bình duyệt (AndroidControl NeurIPS 2024, OS-Atlas ICLR 2025). **Không khoe "triệu-scale"**.

### MobileViews — bộ chính của mùa này

- **Tên/nơi:** Gao và cộng sự, `arXiv:2409.14337` (cs.HC), BUPT + AIR Tsinghua. **Chưa tìm thấy dấu hiệu công bố hội nghị/tạp chí.** v1–v2 (2024) tên "*A Large-Scale Mobile GUI Dataset*"; v3 (11/2025) đổi thành "*A Million-scale…*" → **ghi rõ phiên bản v3 + ngày tải khi trích**.
- ⚠️ **Không khẳng định** ba đồng tác giả thuộc Xiaomi — có tin nhưng không tự xác nhận được.
- **Quy mô:** paper v3 nói >1,2 triệu cặp ảnh–VH / >30.000 app; **bản công khai tải được chỉ là "MobileViews-600K"** (>600.000 cặp, >20.000 app). Đây là mâu thuẫn phải khai, không được im.
- **Schema:** mỗi màn = 1 ảnh `.jpg` + 1 `.viewhierarchy.json`. Node có `class` (⚠️ **tên trường là `class`, KHÔNG phải `viewClass`**), `text`, `content_description`, `resource_id`, `clickable`, `editable`, `bounds`, `children`…
- ⚠️ **Bẫy toạ độ — phải xử lý trước khi tính grounding:** trường cấp cao ghi `width=2340, height=1080` nhưng ảnh thật là **1080×2340 (dọc)** — hai trường **không khớp hướng ảnh**; `bounds` chạy tới `y≈1920` và có giá trị âm/tràn. **Khung toạ độ phải hiệu chỉnh theo từng file**, nếu không thước grounding vô hiệu.
- **Định dạng `bounds` LỒNG NHAU:** `[[x1,y1],[x2,y2]]` — **không** phải `[x1,y1,x2,y2]` phẳng.
- **Cách chọn mẫu pilot:** 90 màn/18 app (vòng đầu, `MIN_ACT ≥ 5` — `MIN_ACT` = số nút bấm/gõ tối thiểu mỗi màn phải còn lại) → mở rộng 138 màn/30 app (vòng hai siết hơn: `MIN_ACT ≥ 6`, `MAX_PER_APP = 5`) → dedup theo chữ-ký-cấu-trúc-VH, loại 8 nhóm gần trùng / 11 màn thừa → **127 màn / 30 app**, ghi ở `harness/kept_screens_final.json`. **Báo đúng n-hiệu-dụng là 127, không phải 138.**
- **Độ đa dạng đã đo** (⚠️ phân bố này đo trên **138 màn TRƯỚC bước dedup**, nên cộng lại ra 138 chứ không phải 127 — đừng in kèm nhau mà không chú): 55 màn phủ-nhãn thấp (<0.5) · 38 trung · 45 cao (>0.8); nút-có-nhãn mỗi màn: min 5 · median 10,5 · max 280; 30 miền app khác nhau. Có một app (`mxcomminisoapp`, phủ nhãn 0,11) gần như toàn icon — **ca quý để test xử lý nút icon-only**.
- **Hạn chế phải khai:** ① preprint; ② mâu thuẫn 1,2M vs 600K; ③ **VH sinh tự động → thiếu/nhiễu nhãn** (đối chiếu: **>77% app thiếu nhãn trợ năng, Chen et al., ICSE 2020**) → đây chính là lý do phải có hậu-kiểm + fallback; ④ không có đáp án vàng; ⑤ bot duyệt → vài trạng thái không phản ánh luồng người thật (thiếu màn sau đăng nhập/thanh toán); ⑥ **chỉ tiếng Anh, không có app Việt Nam**.
- ⚠️ **Còn nợ:** con số **độ phủ nhãn VH thật** chưa tính (`harness/dg1_vh_coverage.py` chưa chạy). Cần nó để báo tỉ lệ bịa dạng "có điều kiện recall-VH".

### AndroidControl — bộ nhiều màn (ngoài phạm vi mùa này)

- **Tên đầy đủ:** Li và cộng sự (**Google DeepMind**), *"On the Effects of Data Scale on UI Control Agents"*, `arXiv:2406.03679`, **NeurIPS 2024 Datasets & Benchmarks**. (Bản arXiv v1 tên "…Computer Control Agents", bản NeurIPS đổi "…UI Control Agents" — **cùng một bài**.)
- **Quy mô:** 15.283 episode · 14.548 task duy nhất · **833 app** · 40 category. Độ dài: trung bình **5,5** bước, p5–p95 = 1–13. Train 13.604 ep / val 137 ep ⚠️ (**val = 137 nghe bất thường — chỉ 0,9% của 15.283; tự đếm lại trước khi in, đừng trích như số chắc**).
- **Thu thập:** người thật thao tác trên **Google Pixel** qua WebUSB + ADB, ~20 annotator được đào tạo nhiều tuần, kéo dài ~1 năm. Vì là quỹ đạo người thật nên **"gold action" mỗi bước là thao tác đúng do người thực hiện** — đây là lý do nó đáng tin làm chuẩn chấm.
- **8 loại thao tác:** `click, long_press, input_text, scroll, navigate_home, navigate_back, open_app, wait` (+ `status`).
- ⚠️ **Cỡ test-split — chỗ dễ in sai nhất, đọc kỹ:** **KHÔNG in "2.855"** (đó là tổng 4 sub-split **chồng nhau**: in-domain 721 + app-unseen 631 + task-unseen 803 + category-unseen 700; chính paper ghi "may overlap"). Số duy nhất sau khử trùng ≈ **1.540**. Nhưng cũng **không trích "1.542" như số nguyên văn** — hai số lệch nhau 2 episode, **phải tự đếm `episode_id` duy nhất trước khi in**. Câu an toàn được phép viết: *"Test-split gồm 4 sub-split chồng nhau, tổng 2.855; số duy nhất sau khử trùng ≈1.540 (Li et al., NeurIPS 2024 D&B, Table 3)."*
- ⚠️ **Provenance:** nguồn thực dùng là bản cộng đồng re-split 80/20 (`smolagents/android-control`, test = 3.051 ≠ held-out chính thức). **Vô hại về rò rỉ** vì luận văn chạy zero-shot và không claim leaderboard — nhưng **phải khai khi viết**.

### ScreenSpot-v2 — đối chứng grounding (đã hạ vai)

- **Bản chất:** bản **hiệu đính thủ công** của ScreenSpot gốc, **phát hành kèm bài OS-Atlas** (`arXiv:2410.23218`, **ICLR 2025** poster). ScreenSpot gốc từ nhóm **SeeClick, ACL 2024**.
- ⚠️ **Diễn đạt bắt buộc chính xác:** *"ScreenSpot-v2 không có bài bình duyệt riêng; nó được mô tả và phát hành kèm OS-Atlas (đã bình duyệt ICLR 2025)."* Đừng viết tắt thành "ScreenSpot-v2 ICLR 2025".
- **Quy mô:** 1.272 chỉ dẫn một-bước — Mobile 502 · Desktop 334 · Web 436. OS-Atlas phát hiện **~11,32% lỗi chú thích** trong bản gốc và sửa 144 mục (Web 63 · Desktop 28 · Mobile 53).
- **Bản làm việc:** 501 item mobile (icon 211 / text 290; nguồn: iOS 238 / Android 211 / shop 52). *(⚠️ 502 theo paper vs 501 trong file làm việc — lệch 1, chưa đối chiếu.)*
- **`bbox` dạng `[x1,y1,x2,y2]`** ở bản làm việc (bản gốc HuggingFace có thể dùng `[x,y,w,h]` → nêu rõ đã chuẩn hoá để tái lập).
- **Vì sao hạ vai:** lệch nền tảng (238 iOS / chỉ 211 Android thật sự bảo chứng cho MobileViews) + chỉ dẫn của nó thường **chứa sẵn tên phần tử đích** → khác hợp đồng vào/ra của luận văn. Chốt: chỉ trích số OS-Atlas đã công bố, hoặc hạ khung xuống "**tham chiếu ngoài**". Bộ này cũng **đã bão hoà** với model đời mới.
- ⚠️ **Cần verify trước khi in:** đối chiếu danh sách tác giả OS-Atlas trên OpenReview. Giấy phép ScreenSpot **gốc** chưa xác minh riêng.

### Năm điều kiện chốt trước khi in bản cuối

1. **Không in số test "2.855"** cho AndroidControl (xem ở trên — và cũng đừng trích "1.542" nguyên văn; tự đếm trước).
2. **Tính con số độ phủ nhãn VH** thật (`harness/dg1_vh_coverage.py`, chưa chạy).
3. **Hiệu chỉnh khung toạ độ MobileViews** (lệch width/height, bounds lồng nhau) **TRƯỚC** khi tính bất kỳ số grounding nào.
4. **Đối chiếu danh sách tác giả OS-Atlas** trên OpenReview trước khi in trích dẫn.
5. **Không khẳng định** affiliation Xiaomi của 3 đồng tác giả MobileViews.

---

## Phụ lục G — Bản đăng-ký-trước: toàn văn ngưỡng đã khoá

> **Đây là bản gốc pháp lý của mọi ngưỡng trong tài liệu này** (file `report/56`, đã commit `2c84ce8` lúc **12/7/2026 15:35 UTC**). Split đã khoá ở commit `3776212` (12/7/2026 12:07 UTC), **seed = 20260710**. Chép vào đây để không phải mở file khác — nhưng **bản có hiệu lực là file 56 đã commit**, không phải bản chép này.

**Cam kết:** mọi định nghĩa + ngưỡng được ĐÓNG BĂNG **trước khi chạy thí nghiệm**. `git commit` = dấu thời gian. **Không sửa sau khi commit** — trừ đúng một ô `[MDE]`, điền sau pilot baseline (việc này không lộ hướng/độ lớn hiệu ứng nên không phá tính đăng-ký-trước).

**Quy trình ba bước, không được đảo:**
1. Commit bản đăng-ký-trước **TRƯỚC** pilot. ✅ *(xong — `2c84ce8`)*
2. Chạy pilot baseline → điền `[MDE]` → nếu cần đổi 15/15 thì đổi + **commit lần 2**. ⬅️ **việc kế tiếp**
3. **SAU ĐÓ** mới chạy full Tier 1 / Tier 2.

**Hai cam kết cứng về rò rỉ:**
- Cổng K-leak: `pool ∩ 12 test app = ∅` (dedup theo package-name **+** perceptual-hash), assert rỗng + ghi log **trước khi** build data SFT. ✅ *(đã chạy 12/7: 0 ca)*
- **Student KHÔNG bao giờ thấy View Hierarchy** — cả lúc train lẫn lúc suy luận. VH chỉ vào lúc **CHẤM**.

**Ngưỡng đã khoá:**

| | Tier 1 | Tier 2 |
|---|---|---|
| So sánh | `Student` vs `Student-RAW` | `Student` vs `Teacher-BASE` |
| Điều kiện | 12 test app, `f` đo trên **output THÔ** | 12 test app, **tắt hẳn VH**, `f` trên output thô |
| **(A) Thống kê** | CI 95% của `Δ = mean(f_student − f_studentRAW)` **hoàn toàn trên 0** | CI 95% của `Δ = mean(f_student − f_teacher)` **hoàn toàn trên 0** |
| **(B) Thực tế** | **Không cần** (gần chắc dương theo tiền lệ) | `Δ_test ≥ 0.5 × Δ_train` |
| Nếu null | **DỪNG** — rà lại toàn bộ pipeline lọc trước khi diễn giải Tier 2 | Báo trung thực kèm MDE |

- **Δ_train (định nghĩa DUY NHẤT):** đo bằng **đúng cùng công thức + đúng cùng điều kiện tắt-VH** như `Δ_test`, chỉ khác là tính trên **18 train-app** thay vì 12 test-app.
- **Hệ số 0.5 = tự đề xuất**, khai rõ trong luận văn, **không lấy từ literature**. (Thầy hỏi "sao lại 0.5?" → trả lời đúng như vậy, đừng bịa nguồn.)

**Ba kết cục — cách diễn giải viết sẵn trước khi nhìn số:**

| Kết cục | Điều kiện | Diễn giải đã khoá |
|---|---|---|
| **PASS đầy đủ** | (A) + (B) | Nội-tại-hoá thật, tổng quát hoá đáng kể sang app mới — *trong phạm vi màn giống MobileViews đã qua vòng kiểm tra chất lượng* |
| **PASS một phần** | (A) đúng, (B) sai | Nội-tại-hoá có ý nghĩa nhưng suy giảm mạnh — vẫn là existence-proof có giá trị |
| **NULL** | CI chứa 0, hoặc `Δ_test ≤ 0` | Báo trung thực kèm MDE — giới hạn tổng quát hoá đáng công bố (khung negative-results, NeurIPS 2021 Pre-reg Workshop). **KHÔNG tự động lùi về "chỉ lắp ráp công cụ"** vì Tier 1 vẫn đứng độc lập |

**Kiểm định — code nguyên văn:**
```python
d_j = mean_{i in app_j}(f_student_i − f_comparison_i)     # j = 1..12
t_obs = mean(d) / (std(d, ddof=1) / sqrt(12))
# EXACT: liệt kê toàn bộ 2^12 = 4096 tổ hợp dấu (không Monte Carlo)
null_stats = [ mean(s*d)/(std(s*d)/sqrt(12)) for s in product([+1,-1], repeat=12) ]
p_value = mean( abs(null_stats) >= abs(t_obs) )
# CI 95% bằng test-inversion trên chính phân phối exact đó
```

**Bốn bản vá đã áp (12/7, sau vòng rà soát độc lập):**

- **[A1-1] `f` đo trên output THÔ ở CẢ hai tầng.** Vì lớp viết-lại chữa bịa cho **mọi** bản → nếu chấm `f` *sau* viết-lại thì Student và Student-RAW đều sạch, `Δ_f ≈ 0` → **null giả tạo**, tái phạm đúng lỗi tautology đã vá một lần. Lợi ích của lớp viết-lại báo **riêng** qua %fallback + lỗi-ngầm, không trộn vào `f`.
- **[A1-2] Màn 0-nhắc-nút.** Mẫu số = 0 → `f` **không xác định** → **LOẠI màn đó** khỏi trung bình `f_app` (**không** mặc định `f = 1`). Báo riêng **tỉ lệ màn 0-nhắc-nút** từng arm làm chỉ báo né-trả-lời; app nào **>50%** màn như vậy → gắn cờ cảnh báo.
- **[A2-2] Bất đối xứng prompt là CỐ Ý.** `f_teacher` chấm trên output sinh bằng prompt gốc của teacher — **có** câu "don't invent buttons"; student eval bằng prompt **không** có câu đó. Student phải thắng teacher **dù teacher được nhắc né-bịa còn student thì không** → sai lệch **hướng an toàn**, student thắng thì kết luận càng mạnh.
- **[A2-3] Validate thước đo bằng bơm lỗi.** Gắn với claim C2 của bài FAIR. Bơm 4 loại lỗi độc-lập-matcher: (a) đổi tên nút thật → tên không có trên màn; (b) đổi sang nút có thật nhưng **sai màn**; (c) chèn bước nhắc nút bịa; (d) hoán tên nút giữa 2 màn. Ngưỡng: detection **≥0.80**, false-positive **≤0.10**, đơn-điệu (Spearman < 0, p<0.05). Trụ: **Sai et al., EMNLP 2021**. Phạm vi: **điều kiện CẦN** (độ nhạy), **không** claim convergent-validity với người (**Clark et al., ACL-IJCNLP 2021**). **Không kịp → RÚT claim C2, không hứa suông.**

**Family Holm đã đóng băng:** `{ faithfulness Tier 1, faithfulness Tier 2, phép-đo-phụ hữu-ích/mạch-lạc }`. Thêm/bớt sau khi nhìn số = **vi phạm**.

**Các ô còn trống:**

| Ô | Trạng thái |
|---|---|
| **`[MDE = ___ pp]`** | **TRỐNG** — ô **duy nhất** được phép sửa sau commit. Điền sau pilot baseline → commit lần 2 |
| **τB** (ngưỡng bge-m3) | Chưa có số — chờ hiệu chuẩn 80–120 cặp gán tay |
| Quyết định 15/15 | Treo, phụ thuộc `[MDE]` |
| Pool train mở rộng | Bản 56 ghi "điền sau khi fetch"; fetch **đã chạy 12/7** nhưng prereg chưa cập nhật con số, và trường `train_pool_expanded` trong file split vẫn rỗng (xem Phụ lục D, Bước 1) |

---

## Phụ lục H — Bản đồ các vòng debate đã chạy (chỉ để tra cứu)

Bảy vòng tranh luận/kiểm tra đối kháng đã chạy để đi đến bản chốt này, mỗi vòng đều có bước kiểm chứng độc lập (một bên đưa ra lập luận, một bên khác cố tình tìm cách bác bỏ bằng cách tra cứu lại nguồn gốc):

1. Chọn hướng đi (loại phương án "huấn luyện mô hình bấm nút", "mô hình học phát hiện bịa từ dữ liệu tự chế", và "học tăng cường lấy điểm-trung-thực làm phần thưởng") — xem Phụ lục A.
2. Kiểm tra tính mới so với các nghiên cứu đã có — xem Phụ lục B.
3. Kiểm tra có đủ ngưỡng để bảo vệ luận văn thạc sĩ không.
4. Lập kế hoạch kỹ thuật chi tiết (cấu hình, dữ liệu, hạ tầng) — xem Phụ lục C, D, E.
5. Kiểm tra riêng công thức thống kê của phần đánh giá — kết quả đã gộp vào mục "Bộ thước đo đầy đủ".
6. Kiểm tra riêng công thức thống kê một lần nữa bằng ba đòn tấn công độc lập (Tier 1 có thật sự an toàn, MDE có lỗ hổng, 12 app test có quá mỏng) — xem `report/55`; kết luận đứng vững ở cốt lõi, chỉ cần vá câu chữ định nghĩa.
7. **(2026-07-12) Kiểm tra độ vững toàn bộ 64 quyết định đã chốt** (dùng một mô hình ngôn ngữ độc lập khác, đối chiếu nội bộ report/50→54 + xác minh lại citation/thống kê qua web search): kết luận thiết kế đứng vững (60/64 quyết định khớp nhất quán, citation trụ chính đúng venue/năm, không bị nghiên cứu khác đi trước), phát hiện 6 lỗ tài liệu/pre-registration (định nghĩa "đủ lớn" ở Tier 2 bị mô tả mâu thuẫn giữa report/53 và bản này, Tier 1 thiếu ngưỡng thắng-thua bằng số, công thức MDE thiếu vế cận-trên, thiếu bước đối chiếu ảnh-giống-nhau, trích dẫn UI-R1 sai năm hội nghị, chưa khoá thứ tự thực thi) — toàn bộ đã vá thẳng vào các mục tương ứng ở trên trong lần sửa này.

Toàn bộ log gốc, chi tiết từng lượt tranh luận, và các con số/trích dẫn đã bị loại bỏ vì không xác thực được, vẫn được giữ lại trong các file `report/43`, `report/50`, `report/52`, `report/53`, `report/55` trong cùng thư mục — chỉ cần khi muốn tra lại nguyên văn một cuộc tranh luận cụ thể, không cần cho việc hiểu hay trình bày luận văn.
