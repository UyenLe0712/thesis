# 🎤 BẢN TRÌNH BÀY: PIPELINE & METRIC (DG1) — trình thầy

> **Dùng thế nào:** đọc theo từng "SLIDE". Mỗi slide có **(a) nói gì** + **(b) giải thích cho người chưa biết**. Cuối có **PHẦN THỦ — câu hỏi khó + câu trả lời chắc**. Nguyên tắc xuyên suốt: **nói THẲNG cái mình KHÔNG claim** — đó là cách mạnh nhất để thầy khó tính không bắt bẻ được.
> **Phạm vi:** đây là **DG1** (hướng dẫn trên MỘT màn) = bài VCL. (Phần đa-màn/thứ-tự là DG2, làm sau — không nói hôm nay để khỏi loãng.)

---

## 🎯 PITCH MỞ ĐẦU (30 giây — học thuộc)

> *"Em làm hệ sinh **hướng dẫn sử dụng phần mềm** từ một ảnh chụp màn hình và câu hỏi của người dùng. Vấn đề: các mô hình đa phương thức hay **bịa ra nút không có thật**, mà lại **không có hướng dẫn mẫu chuẩn** để chấm. Em đóng góp **hai thứ NGANG NHAU**: (1) một **phương pháp tạo sinh hướng dẫn bám-sát-màn** — gắn 'lớp làm-cho-trung-thực' lên model mạnh để **giảm bịa nút**; (2) một **phương pháp đánh giá độ trung thực không cần đáp án mẫu**, neo vào danh sách nút thật của màn. Em **không** tuyên bố hệ mạnh nhất — em chứng minh bằng số rằng lớp sinh của em **giảm bịa** (kèm cái giá minh bạch) và cách đo của em **đáng tin**."*

---

## SLIDE 1 — VẤN ĐỀ (cho người chưa biết gì)

**(a) Nói:**
- Người dùng gặp app lạ thường hỏi: *"muốn làm việc này thì bấm vào đâu?"*.
- Mô hình **đa phương thức (VLM)** — loại AI **vừa nhìn ảnh vừa đọc chữ** — có thể nhìn ảnh màn hình + câu hỏi rồi viết **hướng dẫn từng bước**.
- **Hai cái khó:**
  1. VLM hay **"ảo giác" (hallucination)** — nhắc tới nút/menu **không có trên màn** → người làm theo bị lạc.
  2. **Không có "đáp án mẫu"** (hướng dẫn chuẩn do người soạn) cho mọi app → **không biết lấy gì để chấm**.

**(b) Giải thích:** "Ảo giác" = AI tự tin nói ra thứ không tồn tại (giống ChatGPT bịa trích dẫn). Ở đây là bịa **tên nút**. Còn "không có đáp án mẫu" nghĩa là: với bài dịch máy ta có bản dịch chuẩn để so, nhưng với "hướng dẫn dùng app X" thì **chẳng ai soạn sẵn** → đây là cái khó trung tâm.

---

## SLIDE 2 — MỤC TIÊU & HAI ĐÓNG GÓP

**(a) Nói — HAI đóng góp NGANG NHAU:**
- **Đóng góp ① — Phương pháp TẠO SINH hướng dẫn bám-sát-màn** (lớp "làm-cho-trung-thực", *cắm model nào cũng chạy*): giảm bịa nút so với để model viết tự do.
- **Đóng góp ② — Phương pháp ĐÁNH GIÁ** độ trung thực khi **không có đáp án mẫu**.
- **Phạm vi:** một màn hình (DG1). **Không** claim "hệ mạnh nhất thế giới".

**(b) Giải thích + RANH GIỚI claim (quan trọng):** Em **cố ý** không thi đua "viết hay" với GPT-5 — frontier viết văn hay hơn là đương nhiên. Đóng góp ① thi đua ở trục **"có bịa nút không"**, và claim **HẸP đúng mức:** *"giảm tham chiếu đến nút không tồn tại, giá = % bước phải mô tả khái quát"*. Em **KHÔNG** claim "sinh ra hướng dẫn đúng-ý/hữu-ích" — cái đó cần đáp án vàng, để dành DG2. Giữ hẹp = đóng góp **vững, không bắt bẻ được**.

---

## SLIDE 3 — ⭐ Ý TƯỞNG THEN CHỐT (cái làm bài này khả thi)

**(a) Nói:**
- Mỗi màn Android có sẵn **cây phân cấp giao diện (View Hierarchy)** — bản kê khai **mọi nút thật + tên + toạ độ**, do hệ điều hành cung cấp tự động.
- Em dùng nó làm **"đáp án bạc" (silver)** để chấm: *"nút mà hướng dẫn nhắc tới có nằm trong danh sách nút thật không?"*.
- **LUẬT VÀNG:** View Hierarchy **chỉ dùng LÚC CHẤM**, **tuyệt đối không đưa cho model lúc SINH**.

**(b) Giải thích:** "Bạc" (không phải "vàng") vì nó là nhãn **tự động, đủ tin nhưng không hoàn hảo** (đôi khi thiếu nút vẽ bằng ảnh) — em khai thẳng cái này. **Luật vàng** quan trọng: nếu mớm danh sách nút cho model lúc viết thì "không bịa" thành hiển nhiên → kết quả giả. Nên ta giấu nó đi lúc sinh, chỉ lấy ra lúc chấm.

---

## SLIDE 4 — PIPELINE (4 bước)

```
[Ảnh màn hình + Câu hỏi]
        │
   ┌────▼─────────────────────────────────────────┐
   │ B1. VLM sinh hướng dẫn BASE (gọi nút theo TÊN)│   ← model chỉ thấy ảnh + câu hỏi
   └────┬─────────────────────────────────────────┘
        │ "1. Bấm Add expense  2. Nhập Amount  3. Bấm Confirm"
   ┌────▼──────────────────────────────────────────────┐
   │ B2. Đối chiếu từng bước với View Hierarchy (chấm)  │   ← oracle "bên cạnh"
   └────┬──────────────────────────────────────────────┘
        │ "Add expense"✓  "Amount"✓  "Confirm"✗(không có trên màn)
   ┌────▼──────────────────────────────────────────────┐
   │ B3. Lớp hậu kiểm: bước trỏ nút KHÔNG tồn tại       │
   │     → viết lại thành MÔ TẢ BẰNG LỜI (bỏ tên bịa)   │
   └────┬──────────────────────────────────────────────┘
   ┌────▼──────────────────────────────────────────────┐
   │ B4. Chấm 4 thước đo + thống kê                     │
   └───────────────────────────────────────────────────┘
```

**(b) Giải thích:** "BASE" = bản model viết **tự do** (chưa qua lớp của em) — để làm mốc so sánh. "Lớp hậu kiểm" **không sửa** bước đúng; nó chỉ **cách-ly** bước bịa: thay vì bắt người dùng tìm một nút không có thật, nó nói **mô tả việc cần làm bằng lời**.

---

## SLIDE 5 — CÁC THƯỚC ĐO (metric — rõ ràng)

| Thước đo | Đo gì | Công thức (đơn giản) | Cao = tốt? |
|---|---|---|---|
| **Trung thực (Faithfulness)** | Bước có trỏ nút **không tồn tại** không? | 1 − (số bước bịa)/(tổng bước) | ✓ |
| **Đúng-nhãn (Label-fidelity)** | Có gọi **đúng tên hiển thị** của nút? | (số bước đúng tên)/(tổng bước) | ✓ |
| **Đúng-chỗ (Grounding)** | Toạ độ bấm có **rơi trúng khung nút**? | (số bước trúng)/(số bước có toạ độ) | ✓ |
| **Định dạng (Format)** | Có đánh số, động từ mệnh lệnh? | (điều kiện đạt)/(tổng điều kiện) | ✓ |

**Ví dụ 1 màn** (màn có: *Add expense, Amount, Save, Settings*):
- BASE viết: 1.Bấm **Add new** ❌ · 2.Nhập **Amount** ✅ · 3.Bấm **Confirm** ❌ → Trung thực = 1 − 2/3 = **33%**.
- Sau lớp hậu kiểm: "Add new"→mô-tả-bằng-lời, "Confirm"→mô-tả-bằng-lời → không còn nút bịa.

**(b) Giải thích:** Tách **"Bịa"** (nút có tồn tại không — *đồng nghĩa OK*) khỏi **"Đúng-nhãn"** (gọi đúng tên hiển thị — gọi "Thiết lập" cho nút "Cài đặt" thì trừ Đúng-nhãn, **không** tính bịa). Hai lỗi khác nhau, đo riêng.

---

## SLIDE 6 — ⭐⭐ CHỐNG VÒNG-LẬP-LUẬN (điểm khiến KHÔNG bắt bẻ được)

**(a) Nói:**
- **Bẫy:** nếu dùng **cùng một công cụ** để vừa **quyết** "bịa hay không" (chọn cách-ly) vừa **chấm điểm** → điểm trung thực **đương nhiên = 100%**. Đó là **đẳng thức**, không phải kết quả.
- **Em tách đôi:**
  - **QUYẾT** cách-ly: dùng matcher A (`nomic` embedding).
  - **CHẤM** điểm: dùng matcher B (`bge-m3`) **ĐỘC LẬP** + thêm một **LLM-judge KHÁC HỌ** với model sinh.
- **Số thật để báo** = **tỉ lệ bịa của BASE** (đo *độ lớn vấn đề*), **không phải** con số 100% sau lớp hậu kiểm.

**(b) Giải thích:** Đây là chỗ thầy khó tính hay đánh nhất ("có oracle thì không-bịa là hiển nhiên!"). Câu trả lời: **đúng, 100% sau-lớp là TRẦN do thiết kế — em KHAI thẳng và KHÔNG khoe nó là 'thắng'**. Cái em báo là (1) BASE bịa bao nhiêu, (2) lớp cách-ly được bao nhiêu, **chấm bằng công cụ khác** với công cụ đã quyết → hết đẳng thức.

---

## SLIDE 7 — VALIDATE CHÍNH THƯỚC ĐO (không cần chấm người)

**(a) Nói:**
- Làm sao biết **thước đo đáng tin**? → **Perturbation test**: tự **bơm lỗi đã biết** vào một hướng dẫn đúng (đổi 1 nút thật → nút-ma; đổi → đồng nghĩa; phá format) rồi xem **thước đo có bắt đúng không**.
- Báo: **tỉ lệ phát hiện** (bắt đúng lỗi) + **tỉ lệ báo nhầm** (vu oan khi không lỗi).
- **Khách quan, tái lập, không phụ thuộc người chấm.**

**(b) Giải thích:** Vì lỗi do **mình tạo** nên **đáp án đúng đã biết trước** → đo được độ nhạy của thước đo hoàn toàn tự động. Có tiền lệ bình duyệt: **Sai et al., EMNLP 2021** ("Perturbation CheckLists for Evaluating NLG Evaluation Metrics").

---

## SLIDE 8 — THỐNG KÊ CHẶT (chống "may rủi")

**(a) Nói:**
- **Cluster bootstrap theo APP** (17 app): các màn cùng app **không độc lập** → phải gộp theo app, nếu không **CI giả-chặt**.
- **Holm-Bonferroni** khi báo nhiều thước đo.
- **Pre-registration** (đăng ký trước giả thuyết + ngưỡng + cách quyết định) → chống "chạy tới khi đẹp".

**(b) Giải thích:** "Cluster theo app" = nếu em lấy 8 màn từ cùng 1 app, chúng giống nhau, không tính là 8 mẫu độc lập. Gộp theo app cho con số **khiêm tốn nhưng thật**. "Pre-register" = chốt luật chơi **trước** khi nhìn kết quả → không ai cãi được là em "chỉnh số".

---

## SLIDE 9 — PHẠM VI & TRUNG THỰC (đây là lá chắn mạnh nhất)

**(a) Nói — em CHỦ ĐỘNG nêu giới hạn:**
- **Claim DUY NHẤT của DG1:** lớp hậu kiểm **giảm tham chiếu đến nút không tồn tại**, **cái giá = % bước phải mô tả khái quát hơn** (fallback).
- **Em KHÔNG claim** hướng dẫn "đúng ý / hữu ích" — vì điều đó cần **đáp án vàng từng bước** → để dành phần sau (DG2, dùng AndroidControl có gold).
- **Matcher** sẽ được **đo precision/recall + Cohen's kappa với nhãn người** (một tập nhỏ, ~20–30 phút, theo kỹ thuật HITLC) trước khi chốt ngưỡng.

**(b) Giải thích:** Tự nêu giới hạn **trước** khi thầy bắt = tước vũ khí của người phản biện. Và việc **thu hẹp claim** (chỉ "giảm bịa", không "đúng ý") làm mọi câu em nói đều **đứng vững**.

---

## SLIDE 10 — ĐÓNG GÓP & ĐỘ MỚI (chốt)

**HAI đóng góp NGANG NHAU:**
- **① Phương pháp tạo sinh hướng dẫn bám-sát-màn** (lớp "làm-cho-trung-thực", *model-agnostic*): giảm tham chiếu đến nút không tồn tại so với model viết tự do, **kèm báo cái giá (% fallback) minh bạch**. (Claim hẹp: giảm bịa, *không* claim đúng-ý.)
- **② Phương pháp đánh giá không cần đáp án mẫu:** neo View Hierarchy + matcher **độc lập** + **validate thước đo bằng perturbation** + thống kê **cluster theo app**.

**Kèm theo (giá trị cộng thêm):**
- **Lượng hóa được vấn đề:** đo tỉ lệ VLM bịa nút trong hướng dẫn (một con số có giá trị).
- **Quy trình nghiêm:** pre-register + cluster bootstrap + matcher validate với người (Cohen's kappa).

---

# 🛡️ PHẦN THỦ — CÂU HỎI KHÓ & TRẢ LỜI (thầy khó tính)

**❓ "Có sẵn danh sách nút (oracle) thì không-bịa là hiển nhiên, hay ho gì?"**
✅ Đúng một nửa. Con số trung thực ~100% **sau** lớp hậu kiểm là **TRẦN do thiết kế — em KHAI thẳng, không coi là kết quả**. Giá trị thật là: (1) **đo được BASE bịa bao nhiêu** (độ lớn vấn đề), (2) lớp cách-ly được bao nhiêu, **chấm bằng matcher ĐỘC LẬP họ khác** matcher đã quyết → không phải đẳng thức. (3) Và **phương pháp đánh giá** mới là đóng góp.

**❓ "Sao tin được matcher tự động? Lỡ nó sai thì mọi số sai?"**
✅ Em **không tin mặc định — em ĐO**: lấy ~80–120 cặp gán nhãn người → tính **precision/recall + Cohen's kappa** của matcher. Ngưỡng τ được **hiệu chỉnh trên tập có nhãn rồi FREEZE trước khi chạy chính**. Em còn báo **độ nhạy của kết luận theo nhiều ngưỡng**. (Để đỡ tốn công người: model mạnh pre-label, người chỉ duyệt ~20–30 cặp vùng-bất-đồng — kỹ thuật HITLC.)

**❓ "Đây chỉ đo TỰ-NHẤT-QUÁN (nút có thật không), đâu đo ĐÚNG-Ý?"**
✅ **Chính xác, và em thừa nhận thẳng.** Matcher chỉ bảo "nút có thật", không bảo "đúng nút theo ý". Nên **claim của DG1 thu hẹp đúng vào 'giảm bịa'**, **không** đụng tới 'đúng ý'. Phần 'đúng ý' cần đáp án vàng → **để dành DG2 trên AndroidControl** (có gold + Step-SR).

**❓ "Câu hỏi do AI tự sinh — có làm hỏng tính khách quan?"**
✅ Không, vì: (1) thước đo **neo vào View Hierarchy** (nguồn độc lập với câu hỏi), không neo vào câu hỏi; (2) BASE và bản-có-lớp **dùng CHUNG câu hỏi** → thiên vị (nếu có) **tự khử** khi lấy hiệu; (3) câu hỏi **gieo từ nút thật** (affordance-seeded) + có **cổng answerability tự động** (chỉ giữ câu trả-lời-được trên màn); (4) **model sinh câu hỏi ≠ model viết hướng dẫn**.

**❓ "Dùng thêm một AI (LLM-judge) để chấm — AI chấm AI có đáng tin?"**
✅ Em **không** để AI chấm "hay/dở" (vùng đó AI lệch). Em dùng nó cho một **phán đoán HẸP, NHỊ PHÂN, NEO-THAM-CHIẾU**: *"tên nút này có khớp đúng một nút trong danh sách thật không?"*. Đây là **vùng dễ nhất** của LLM-judge — bài bình duyệt **Zheng et al., NeurIPS 2023** cho thấy đưa sẵn tham chiếu vào giúp judge **giảm sai từ 70% xuống 15%**. Judge dùng **model khác họ** với model sinh (tránh tự thiên vị), và **được đo precision/recall + kappa với nhãn người** y như matcher.

**❓ "Lớp hậu kiểm chỉ là 'né' (không chắc thì mô tả chung chung) — gọi là cải thiện?"**
✅ Em báo **cả cái giá**, không giấu: trung thực **tăng** nhưng "đúng-chỗ cụ thể" **giảm** + có **% fallback**. Đây là một **đánh đổi minh bạch**, và bản thân việc **đo được đánh đổi đó** + lượng hóa tỉ lệ bịa của model là đóng góp. Em **không** thổi nó thành "hệ hoàn hảo".

**❓ "Mẫu bao nhiêu, có ý nghĩa thống kê không?"**
✅ 81 màn / **17 app**, dùng **cluster bootstrap theo app** (khiêm tốn nhưng thật) + **Holm** + **pre-register**. Và theo nguyên tắc **"null vẫn đậu"** (đăng ký trước): nếu lớp không cải thiện, em vẫn báo trung thực kèm lý do — luận văn **không lệ thuộc "phải thắng"**.

**❓ "Con số 100% trung thực nghe quá đẹp, có đáng ngờ?"**
✅ Đáng ngờ nếu coi là "kết quả" — nên em **KHÔNG** trình nó như kết quả. Em trình **tỉ lệ bịa của BASE** (số thật, có CI) + **% fallback** (cái giá). 100% chỉ là hệ quả tất yếu của "loại bỏ tham chiếu không tồn tại" → em nói rõ đó là **trần do thiết kế**.

**❓ "Tiếng Việt đâu? Đề tài hướng tiếng Việt mà dữ liệu tiếng Anh?"**
✅ Pipeline/metric **vốn ngôn-ngữ-độc-lập** (chấm bằng khớp tên/toạ độ). Em **chứng minh định lượng trên dữ liệu Anh** (có sẵn nhãn chuẩn), **tiếng Việt làm demo định tính** trên app VN thật. Em **trung thực**: chưa có bảng số VN vì **thiếu dataset VN có nhãn+toạ độ** — đây là giới hạn **dữ liệu**, không phải pipeline.

---

# 📌 MỘT DÒNG ĐỂ KẾT

> *"DG1 có **hai đóng góp ngang nhau**: (1) một **phương pháp tạo sinh hướng dẫn bám-sát-màn** (lớp làm-cho-trung-thực, model-agnostic) **giảm bịa nút** kèm báo cái giá minh bạch; (2) một **phương pháp đánh giá độ trung thực khi không có đáp án mẫu** (neo View Hierarchy, chấm bằng matcher độc lập + validate bằng perturbation, cluster theo app). Em **thu hẹp claim đúng vào điều chứng minh được** và **tự nêu mọi giới hạn** — nên mỗi câu đều đứng vững."*

---

## GHI CHÚ CHO NGƯỜI TRÌNH BÀY
- **Số liệu cuối đang chạy** (81 màn/17 app) → khi thầy hỏi số, nói: *"thử nghiệm sơ bộ cho thấy đúng hướng (BASE bịa ~1/4 số bước trên tập thử nhỏ); em đang chạy chính trên 17 app để có bảng số + CI cuối"*. **Đừng đọc số cuối chưa có.**
- Nếu thầy đào sâu DG2 (đa màn/thứ tự): nói *"đó là nhánh sau (bài FAIR), hôm nay em xin tập trung DG1 cho gọn"*.
- Vũ khí mạnh nhất: **chủ động nói cái mình KHÔNG claim** (Slide 9) trước khi bị hỏi.
