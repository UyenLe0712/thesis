# report/64 — Thiết kế lại từ trang giấy trắng: chỉ nhìn đề tài + 3 dataset

> Bài tập user giao (2026-07-16): *"Đừng bị bias. Chỉ nhìn nội dung đề tài và 3 bộ dataset, thử nghĩ xem pipeline + metric nên như thế nào, và bộ thí nghiệm để chứng minh pipeline đúng."*
>
> Cách làm: tôi cố tình KHÔNG xuất phát từ thiết kế hiện tại (report/54), mà đi lại từ đầu theo trình tự: (1) bài toán có thể hỏng ở đâu → (2) mỗi dataset cho phép kiểm cái gì → (3) từ đó suy ra pipeline, thước đo, thí nghiệm. Cuối bài mới đối chiếu với thiết kế hiện tại — chỗ nào trùng thì nói rõ VÌ SAO trùng (bị dữ liệu ép, không phải bias), chỗ nào khác thì nói thẳng.

---

## 1. Xuất phát điểm: bài toán và chỗ nó có thể hỏng

**Đề tài:** vào = ảnh màn hình + câu hỏi ("làm sao để X?") → ra = hướng dẫn từng bước cho NGƯỜI đọc. Không có bộ hướng dẫn chuẩn do người soạn để chấm.

Một bản hướng dẫn có thể hỏng theo 5 kiểu, độc lập nhau:

| # | Kiểu hỏng | Ví dụ |
|---|---|---|
| H1 | **Nhắc tới nút không tồn tại** trên màn | "Bấm Preferences" khi màn không có nút đó |
| H2 | Nút có thật nhưng **sai nút** cho việc cần làm | Bảo bấm "Share" khi cần "Settings" |
| H3 | Đúng các nút, **sai thứ tự** | Bảo toggle trước khi mở menu chứa nó |
| H4 | Không sai gì nhưng **vô dụng** | "Hãy tìm mục cài đặt phù hợp" |
| H5 | **Trả lời lạc đề** so với câu hỏi | Hỏi tắt thông báo, hướng dẫn đổi theme |

Điểm mấu chốt của cả thiết kế nằm ở đây: **không có gold thì không kiểm được H2/H3/H5 một cách trực tiếp trên dữ liệu không gold** — nhưng H1 thì kiểm được, vì "nút này có tồn tại không" là câu hỏi có đáp án khách quan nếu ta có danh sách phần tử thật của màn. Vậy câu hỏi đầu tiên khi nhìn 3 dataset là: **bộ nào cho đáp án khách quan cho kiểu hỏng nào?**

## 2. Ba dataset cho phép kiểm cái gì (đây là phần "ép" thiết kế)

| Dataset | Có gì | Kiểm được kiểu hỏng nào |
|---|---|---|
| **MobileViews** (ảnh + VH, KHÔNG gold task) | Danh sách phần tử thật của từng màn (tên, loại, bbox) — dù nhãn thiếu một phần | **H1** (tồn tại/bịa) — và CHỈ H1. Không có task nên H2/H3/H5 không có đáp án |
| **AndroidControl** (episode + gold action từng bước + a11y tree) | Chuỗi thao tác ĐÚNG do người thật làm, cho một goal cụ thể | **H2 + H3** (đúng nút? đúng thứ tự?) — bộ DUY NHẤT có sự thật về quy trình |
| **ScreenSpot-v2** (chỉ dẫn → bbox chuẩn) | Đáp án "phần tử này nằm đâu" | Năng lực **chỉ-đúng-chỗ** (grounding) — không phải kiểu hỏng của bản hướng dẫn, mà là phép thử năng lực nền của model |
| (không bộ nào) | — | **H4/H5** (hữu ích, đúng ý) — bắt buộc phải chấm bằng người hoặc judge, không dataset nào thay được |

Rút ra 3 hệ quả, và đây là các hệ quả **bị dữ liệu ép**, ai thiết kế từ đầu cũng phải đi tới:

1. **VH là nguồn sự-thật-khách-quan DUY NHẤT trên dataset không-gold** → mọi cơ chế chống bịa (H1) phải xoay quanh nó. Nhưng VH thiếu nhãn (nhìn ngay trong data thấy: nhiều phần tử icon không có text) → dùng VH làm trọng tài thì phải (a) khai điều kiện recall, và (b) nên bù bằng OCR đọc chữ trên ảnh — chữ hiển thị trên màn là thứ VH hay thiếu nhất.
2. **AndroidControl là bộ DUY NHẤT chấm được "hướng dẫn có ĐÚNG không"** (chứ không chỉ "có bịa không") → không dùng nó thì cả luận văn chỉ chứng minh được "không bịa", không chứng minh được "đúng". Một bản hướng dẫn toàn câu an toàn chung chung cũng "không bịa" — nên **thiếu trục H2/H3 là lỗ hổng logic**.
3. **H4 (hữu ích) không có nguồn khách quan** → phải có ít nhất một phép chấm chủ quan (judge khác họ + mẫu người nhỏ), và phép chấm đó phải được VALIDATE bằng cách bơm lỗi đã biết (nếu metric không bắt được lỗi cố tình bơm vào thì metric vô dụng).

## 3. Pipeline tôi sẽ vẽ (từ trang trắng)

### 3.1. Vì sao phải train model, và train cái gì

Không có gold → nguồn supervision duy nhất cho một model sinh hướng dẫn là: (a) model lớn hơn sinh dữ liệu mẫu (distill), hoặc (b) tự sinh rồi tự lọc (self-training). Cả hai đều cần một **bộ lọc chất lượng** đứng giữa, vì dữ liệu máy-sinh chắc chắn có bịa (H1). Và bộ lọc duy nhất khách quan là VH (hệ quả 1). Nên dù đi đường nào, kiến trúc cũng quy về:

```
[sinh nháp] → [đối chiếu VH: bước nào nhắc nút không tồn tại?] → [xử lý bước bịa] → [train model nhỏ]
```

Chỗ "xử lý bước bịa" có 3 lựa chọn: xoá bước (gãy mạch quy trình) · đoán nút thật gần nhất (tạo lỗi ngầm — sửa sai thành sai kiểu khác mà không ai biết) · **viết lại thành mô tả bằng lời, không nêu tên nút** (an toàn, mất chút cụ thể). Tôi chọn cách 3 — hai cách kia có chế độ hỏng tệ hơn cái chúng sửa.

Model nhỏ (cỡ 3B, LoRA) thay vì to: vì use-case thật của "hướng dẫn dùng app" là chạy trên máy người dùng, và vì ràng buộc compute. Đây không phải nhượng bộ — model to gọi API thì quay lại đúng cái "ghép công cụ" không có đóng góp.

### 3.2. Một lựa chọn KHÔNG hiển nhiên: teacher sinh mù hay sinh có VH?

Đây là ngã rẽ thật sự mà thiết kế từ trang trắng phải đối mặt (và đáng làm rõ hơn hiện tại):

- **Đường A — teacher sinh MÙ (chỉ ảnh) rồi lọc:** dữ liệu có bịa thật → lọc → tập train chứa cả ví dụ "khi không chắc thì viết mô tả". Student học được **hành vi né đúng chỗ**. Phụ phẩm: cặp (bản bịa, bản đã lọc) miễn phí.
- **Đường B — teacher sinh CÓ VH trong prompt:** dữ liệu sạch hơn ngay từ đầu, ít phải lọc. Nhưng student (lúc inference chỉ có ảnh) học từ dữ liệu viết bởi "người nhìn thấy đáp án" — không có ví dụ né nào, gặp màn lạ sẽ không biết lùi, cứ bịa tới.

Từ trang trắng, tôi nghiêng đường A vì hành vi né là thứ bảo vệ người dùng lúc triển khai — nhưng tôi sẽ **chạy cả hai như một thí nghiệm so sánh** (X6 dưới), vì (a) chưa chắc trực giác đúng, (b) đây chính là phép so "lọc-sau vs bám-ngay-từ-đầu" mà chưa ai công bố. Một mũi tên trúng hai đích: vừa là ablation nội bộ, vừa là đóng góp so-sánh.

### 3.3. Sơ đồ pipeline đầy đủ

```
MobileViews (ảnh + VH)
  │
  ├─ [P0] Sinh câu hỏi từ affordance của màn + CỔNG answerability
  │        (câu hỏi phải trả lời được từ màn — không thì "bịa" là do đề, không phải do model)
  │
  ├─ [P1] Teacher sinh nháp (chỉ ảnh + câu hỏi — KHÔNG VH)
  │
  ├─ [P2] Trọng tài: VH ∪ OCR-text  ← bù chỗ VH thiếu nhãn, giảm kết oan
  │        matcher embedding so từng tên nút được nhắc ↔ danh sách phần tử
  │        (ngưỡng τ freeze trước; validate matcher vs tay người ~100 cặp, báo P/R + κ)
  │
  ├─ [P3] Bước bịa → viết lại thành mô tả bằng lời
  │        (TẬP nhiều câu cùng nghĩa, bốc ngẫu nhiên — không 1 câu cố định, tránh học vẹt)
  │
  └─ [P4] SFT-LoRA model nhỏ 3B trên tập đã lọc
           inference cuối: CHỈ ảnh + câu hỏi (không VH, không internet)

Chấm (3 dataset, 3 vai):
  MobileViews held-out theo app → H1 (bịa/né) — thước chính
  AndroidControl (lấy TỪNG BƯỚC làm màn đơn: màn + gold action) → H2/H3 (đúng nút, đúng hành động) — thước "đúng"
  ScreenSpot-v2 → grounding control (model có chỉ đúng chỗ không) — thước năng lực nền
  Judge khác họ + mẫu người nhỏ → H4 (hữu ích) — validate bằng bơm-lỗi
```

Ghi chú quan trọng về AndroidControl: không cần đụng tới nhánh nhiều-màn. Mỗi episode chặt ra thành từng bước rời — mỗi bước là một cặp (màn hình, hành động đúng). Cho model sinh hướng dẫn cho đúng câu hỏi của bước đó rồi so: hành động đầu tiên bản hướng dẫn bảo làm có khớp gold action không (đúng loại thao tác + đúng vị trí trong dung sai). Đây là cách duy nhất có được con số "hướng dẫn ĐÚNG" mà không cần người chấm.

## 4. Bộ thước đo (từ trang trắng)

Nguyên tắc: mỗi kiểu hỏng một thước, cộng một thước cho cái giá phải trả (né nhiều quá thì vô dụng).

| Thước | Đo gì | Trên dataset | Định nghĩa |
|---|---|---|---|
| **M1. Tỉ lệ bịa** | H1 | MobileViews held-out | bước nhắc-nút không khớp (VH ∪ OCR) / tổng bước nhắc-nút; báo kèm điều kiện recall trọng tài |
| **M2. Tỉ lệ né (%fallback/hedge)** | giá của M1 | MobileViews held-out | bước mô-tả-chung / tổng bước |
| **M3. Đường đánh đổi né–bịa** | M1+M2 gộp | MobileViews held-out | quét ngưỡng quyết định → đường cong (trục X: tỉ lệ dám nói cụ thể; trục Y: tỉ lệ bịa trong số đó); so 2 model bằng diện tích dưới đường. **M1+M2 là 2 điểm cắt của M3 — báo cả hai dạng: cặp số cho dễ hiểu, đường cong cho chặt** |
| **M4. Đúng-hành-động (Step-match)** | H2+H3 | AndroidControl từng-bước | hành động đầu tiên hướng dẫn bảo làm khớp gold: đúng loại + đúng đích trong dung sai chuẩn ngành |
| **M5. Grounding control** | năng lực nền | ScreenSpot-v2 | point-in-bbox từ (tên phần tử + ảnh), bộ trỏ độc lập — không lấy tâm bbox đã khớp (tautology) |
| **M6. Hữu ích** | H4 | mẫu MobileViews | judge nhị phân KHÁC HỌ teacher + mẫu người nhỏ; chỉ được diễn giải sau khi qua X5 (validate bơm-lỗi) |
| **M7. Đa dạng đầu ra** | tác dụng phụ của train | output model | distinct-n / self-BLEU trước-sau SFT — bằng chứng model không thành máy lặp một câu |

Chống tự-chấm (bắt buộc, vì matcher vừa lọc data vừa dễ bị lấy đi chấm luôn): **embedding LỌC ≠ embedding CHẤM** (hai họ khác nhau), judge khác họ teacher, và mọi thước tự động phải qua bơm-lỗi (X5) trước khi được tin.

Thống kê: đơn vị cụm = **app** (màn cùng app không độc lập) → held-out theo app, bootstrap theo cụm, ngưỡng đậu/rớt khoá TRƯỚC khi chạy. (Đây là phần không có phương án thay thế nghiêm túc — làm khác đi là sai.)

## 5. Bộ thí nghiệm chứng minh pipeline đúng

Logic: pipeline đưa ra một CHUỖI khẳng định — mỗi thí nghiệm bẻ gãy được một khẳng định. Nếu tất cả sống → pipeline đứng.

| TN | Khẳng định bị thử | Cách thử | Dataset | Thước | Đậu khi |
|---|---|---|---|---|---|
| **X0** | "Vấn đề có thật": VLM bịa nút ở mức đáng kể | Đo tỉ lệ bịa của ≥2 VLM sinh mù (teacher + 1 model đời mới) | MobileViews | M1 | tỉ lệ bịa > 0 rõ rệt, báo per-model |
| **X1** | "Trọng tài đáng tin": matcher bắt đúng bịa | (a) validate vs nhãn tay ~100 cặp; (b) BƠM nút giả vào hướng dẫn sạch → matcher phải bắt được; bơm nút thật → không được kết oan | MobileViews | P/R, κ | precision ≥ ngưỡng khoá trước; oan sai thấp |
| **X2** | "OCR-fusion đáng công": VH∪OCR kết oan ít hơn VH-only | Cùng bộ hướng dẫn, chấm bằng 2 trọng tài, đếm ca "matcher nói bịa nhưng người nói nút có thật" | MobileViews | Δ oan sai | fusion giảm oan sai có ý nghĩa |
| **X3** | "Lọc có tác dụng": student-LỌC tốt hơn student-RAW | Train 2 model cùng config, khác duy nhất bước lọc | MobileViews held-out | M1/M2/M3 + M7 | LỌC thắng trên M3, không sập M7 |
| **X4** | "Học được bám-màn, không học vẹt": student giữ trung thực trên app CHƯA THẤY, không cần VH lúc chạy | So student vs teacher-BASE, cả hai chỉ có ảnh, app held-out | MobileViews held-out | M3 | student không thua teacher (kỳ vọng thắng; null vẫn báo trung thực) |
| **X5** | "Thước đo tự động đáng tin" | Bơm 4 loại lỗi đã biết (nút giả · sai thứ tự · xoá bước · câu vô dụng) độc lập với matcher → từng thước phải phát hiện đúng loại lỗi của nó, đơn điệu theo liều | mọi bộ | detection/FP | thước nào rớt X5 thì bị loại khỏi kết luận |
| **X6** | "Lọc-sau thắng bám-từ-đầu" (ngã rẽ 3.2) | Train thêm student-B từ data teacher-có-VH; so 3 nhánh: LỌC vs RAW vs CÓ-VH | MobileViews held-out + AndroidControl | M1–M4 | mô tả trung thực, bên nào thắng cũng là kết quả |
| **X7** | "Không bịa NHƯNG vẫn đúng": lọc không phá độ đúng của quy trình | Chấm M4 cho student-LỌC vs student-RAW vs teacher | AndroidControl từng-bước | M4 | LỌC không giảm M4 đáng kể so RAW (no-harm) |
| **X8** | "Cụ thể ở mức người dùng chấp nhận" | M6 trên mẫu ngẫu nhiên held-out, sau khi M6 đậu X5 | MobileViews | M6 | mô tả, có khoảng tin cậy |

Ba thí nghiệm **không được bỏ** dù thiếu thời gian: **X1** (trọng tài sai thì mọi số sau vô nghĩa), **X3** (không có nó thì "lọc" chỉ là niềm tin), **X5** (không có nó thì mọi thước tự động là tự khen). X0 rẻ và nên chạy đầu tiên vì nó là lý-do-tồn-tại của cả đề tài. X7 là thí nghiệm tôi coi trọng hơn thiết kế hiện tại đang coi (xem mục 6). X6 đắt nhất (thêm một lần teacher + một lần train) — cắt đầu tiên nếu kẹt.

## 6. Đối chiếu trung thực với thiết kế hiện tại (report/54)

### Trùng — và vì sao trùng không phải là bias

Phần lớn khung trùng: filter-then-train quanh VH, viết-lại-thay-vì-đoán, held-out theo app, X3≈Tier 1, X4≈Tier 2, X5≈validate-bơm-lỗi, X0≈đo-bịa-nhiều-model, chống tự-chấm 2 embedding. Lý do trùng nằm ở mục 2: **cấu trúc của 3 dataset ép thiết kế** — VH là sự-thật duy nhất trên bộ không-gold nên nó phải làm trọng tài; không có gold nên phải distill+lọc; màn cùng app tương quan nên phải chặn theo app. Đi lại từ đầu vẫn về đây, và đó là tin tốt: thiết kế hiện tại không phải sản phẩm của quán tính.

### Khác — 5 điểm, xếp theo mức tôi tin là đáng sửa

1. **[Lỗ thật] Thiết kế hiện tại không có trục "ĐÚNG" (H2/H3) cho mùa này.** AndroidControl bị xếp vào nhánh nhiều-màn rồi hoãn → mọi thước còn lại chỉ chứng minh "không bịa + có ích theo judge". Phản biện mạnh nhất tôi thấy: *"model của bạn né bịa, nhưng hướng dẫn có ĐÚNG không thì chưa có số nào."* Cách vá rẻ: **AndroidControl từng-bước như màn đơn** (M4/X7) — không đụng nhánh nhiều-màn, không cần sắp thứ tự, tái dùng 286 episode đã chọn. Đây là điểm khác lớn nhất và tôi cho là đáng đưa vào mùa này nhất.
2. **[Đáng thêm, rẻ] OCR bù VH (M... X2).** Thiết kế hiện tại xử lý VH-thiếu-nhãn bằng cách LOẠI phần tử icon-only khỏi mẫu số — tức là thu hẹp phạm vi đo. Từ trang trắng tôi muốn MỞ RỘNG trọng tài (VH∪OCR) hơn là thu hẹp thước — ít oan sai hơn và phạm vi claim rộng hơn. OCR local, free.
3. **[Đáng thêm, gần như free] Tập câu né đa dạng + thước M7.** Hiện tại: 1 template cố định, không đo đa dạng. Rủi ro học vẹt chưa ai đo được hộ mình (report/61 Q2) → tự phòng + tự đo, chi phí vài giờ.
4. **[Nâng cấp trình bày, không phá cam kết] M3 — đường đánh đổi.** Hiện tại báo cặp (bịa, fallback) với ngưỡng đôi. Từ trang trắng tôi coi cặp số là 2 điểm cắt của MỘT đường — báo cả hai: cặp số giữ đúng pre-registration, đường cong là phân tích thêm.
5. **[Để sau] X6 — so lọc-sau vs bám-từ-đầu.** Từ trang trắng đây là ngã rẽ đáng thử nhất về mặt khoa học (và là khoảng trống chưa ai lấp — report/61 Q4), nhưng đắt (thêm 1 lần teacher + 1 lần train) → đúng chỗ của nó là bài mở rộng, không phải trước 15/8.

### Kết luận một đoạn

Nếu chỉ nhìn đề tài + 3 dataset, tôi vẽ lại gần như cùng bộ xương với thiết kế hiện tại — vì dữ liệu không cho nhiều lựa chọn khác. Ba chỗ tôi làm khác thật sự: **dùng AndroidControl ngay mùa này ở dạng từng-bước để có số "hướng dẫn đúng" (không chỉ "không bịa")**, **mở rộng trọng tài bằng OCR thay vì thu hẹp mẫu số**, và **phòng học-vẹt bằng tập câu né + đo đa dạng**. Điểm 4 (đường đánh đổi) là nâng cấp cách trình bày. Cả 4 đều lắp thêm được vào thiết kế hiện tại mà không phá pre-registration — riêng điểm 1 cần bàn với thầy vì nó thêm một thí nghiệm vào bộ đã đăng ký.
