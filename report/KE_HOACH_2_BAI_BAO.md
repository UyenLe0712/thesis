# KẾ HOẠCH CHIA ĐỀ TÀI THÀNH 2 BÀI BÁO — VCL & FAIR (trình thầy)

> **Mục đích:** từ một luận văn, tách thành **2 bài báo KHÔNG TRÙNG NHAU**, mỗi bài đúng tầm hội nghị, dễ được nhận. Luận văn thạc sĩ là “cái ô” gộp cả hai.
> **Cách tách:** dựa đúng **2 đóng góp song song đã có sẵn** trong đề tài — **DG1** (đánh giá hướng dẫn từ 1 ảnh) và **DG2** (suy luận trật tự màn từ nhiều ảnh). Hai nhánh này vốn **khác câu hỏi, khác dữ liệu, khác thước đo** → tách ra gần như không đụng nhau.

---

## 0. Sơ đồ chia (1 hình nắm ngay)

```
                 LUẬN VĂN THẠC SĨ  (cái ô — gộp cả hai)
                 Khung đánh giá hướng dẫn-từ-ảnh khi KHÔNG có đáp án mẫu
                          │
        ┌─────────────────┴──────────────────┐
   BÀI 1 — VCL (nộp trước)            BÀI 2 — FAIR (nộp sau)
   Tiếng VIỆT · dễ hơn                Tiếng ANH · khó/cạnh tranh hơn
   = DG1: chấm hướng dẫn 1 ẢNH        = DG2: SUY LUẬN TRẬT TỰ MÀN
   Dataset: MobileViews + ScreenSpot  Dataset: AndroidControl
   Metric: grounding/bịa/rõ           Metric: Kendall τ-b (partial-order)
   + demo tiếng Việt                  + signal-attribution + ordering-gap
```

---

## 1. Nguyên tắc chống “trùng” (để cả hai cùng được nhận)

1. **Hai câu hỏi nghiên cứu KHÁC NHAU** — không phải một kết quả gói lại hai lần.
2. **Không nộp cùng kết quả/thí nghiệm** cho cả hai. Mỗi bài có *headline* riêng.
3. **VCL ra trước ⇒ FAIR phải TRÍCH DẪN VCL** (như công trình trước của chính tác giả) và nêu rõ **phần MỚI** (delta). *(Bắt buộc theo chuẩn học thuật.)*
4. **Phần dùng chung** (pipeline sinh hướng dẫn, động cơ) → mỗi bài viết **1 đoạn ngắn + dẫn bài kia**, **viết lại câu chữ** (FAIR tiếng Anh dễ bị quét trùng).
5. Mỗi bài **tự đứng được**: đặt vấn đề → phương pháp → thí nghiệm → kết luận riêng.

---

## 2. BÀI 1 — Hội nghị VCL (nộp trước · tiếng Việt · DG1)

### 2.1. Tựa đề (dự kiến)
**“Khung đánh giá KHÔNG-THAM-CHIẾU cho hướng dẫn sử dụng phần mềm sinh tự động từ một ảnh giao diện.”**
*(Phụ đề gợi ý: “Chấm bám-đúng-màn, chống-bịa và rõ-ràng khi không có bản hướng dẫn mẫu của người.”)*

### 2.2. Tóm tắt (abstract nháp — tiếng Việt)
> Sinh tự động hướng dẫn sử dụng phần mềm từ ảnh giao diện đang khả thi nhờ mô hình thị giác–ngôn ngữ (VLM), nhưng **việc ĐÁNH GIÁ** gặp trở ngại lớn: **không có bộ hướng dẫn-chuẩn do người soạn** để so sánh. Bài báo đề xuất một **khung đánh giá không-tham-chiếu** cho hướng dẫn sinh từ **một ảnh**, neo bằng *view-hierarchy* (nhãn-bạc), gồm ba tiêu chí có nguồn đã bình duyệt: **(1) bám-đúng-màn** (point-in-bbox grounding), **(2) chống-bịa** (hallucination), **(3) rõ-ràng/đúng-định-dạng**. Khung kế thừa và điều chỉnh phương pháp Intrinsic/Extrinsic của Chim, Ive, Liakata (Computational Linguistics 2025) sang miền *ảnh→chữ*. Chúng tôi đánh giá trên **MobileViews** (kèm **ScreenSpot** làm đối chứng độ chính xác vị trí), dùng **thang bậc bật-dần cơ chế** để tách “cơ chế nào thực sự giúp”, và **đối chứng với người chấm**; đồng thời trình bày **demo định tính trên ứng dụng tiếng Việt thực tế**. Toàn bộ giả thuyết được **đăng-ký-trước** nên kết quả null vẫn có giá trị.

### 2.3. Câu hỏi nghiên cứu
**“Làm sao đánh giá ĐÁNG TIN chất lượng một bản hướng dẫn (sinh từ 1 ảnh) khi KHÔNG có đáp án mẫu của người?”**

### 2.4. Đóng góp (claim chính)
- **C1.** Một **khung đánh giá không-tham-chiếu** cho hướng dẫn-từ-ảnh, neo VH-bạc, gồm 3 tiêu chí có citation.
- **C2.** Quy trình **chống rò-rỉ** (view-hierarchy chỉ dùng lúc CHẤM, không đưa vào lúc sinh) + **thang bậc** tách đóng góp từng cơ chế.
- **C3.** **Đối chứng người chấm** (độ khớp máy↔người) + **demo tiếng Việt** cho thấy khung độc-lập-ngôn-ngữ.

### 2.5. Dữ liệu · Phương pháp · Thí nghiệm
- **Dữ liệu:** MobileViews (ảnh + view-hierarchy có toạ độ) · ScreenSpot (đối chứng point-in-bbox).
- **Phương pháp:** pipeline sinh (off-the-shelf) → chấm 3 tiêu chí; *chỉ cite ID nút đã dò* để chống bịa.
- **Thí nghiệm dự kiến:** thang bậc {C1 baseline → C3 ràng buộc → C4 kiểm-ý} trên tập dev rồi mở rộng; báo điểm grounding/hallucination/clarity kèm **“độ phủ bộ dò = X%”**; pilot người ≥60–80 mẫu. *(Số liệu cụ thể báo sau khi chạy — không nêu trước.)*

### 2.6. Vì sao hợp VCL & dễ được nhận
- **Tự-chứa, gọn, dễ minh hoạ** (1 ảnh → 3 điểm số rõ ràng).
- **Có demo tiếng Việt** → rất hợp hội nghị trong nước.
- Đóng góp là **phương pháp đánh giá có nền lý thuyết** (kế thừa CL 2025) → chắc chắn, ít rủi ro bị chê “mỏng”.

---

## 3. BÀI 2 — Hội nghị FAIR (nộp sau · tiếng Anh · DG2)

### 3.1. Title (draft — English)
**“Screen-Order Inference: Evaluating Vision-Language Models’ Ability to Reconstruct Multi-Step UI Workflows from Shuffled Screenshots.”**

### 3.2. Abstract (draft — English)
> Turning UI screenshots into step-by-step software tutorials with vision-language models (VLMs) requires understanding the **order** of screens in a multi-step workflow. We introduce **Screen-Order Inference**: given **N shuffled screenshots** of one workflow plus a goal, the model must **recover the correct order** before generating instructions. We propose a rigorous, **reference-based** evaluation built on **AndroidControl** (NeurIPS 2024 Datasets & Benchmarks), whose **gold action trajectories** provide ground-truth order. Our headline metric is a **partial-order-aware Kendall τ-b** that penalises **only mandatory pairs** — derived *deterministically from the gold trajectory* rather than from the cue detector the model itself uses, thereby **avoiding circular evaluation**. We further report an **ordering gap** (oracle-order vs self-order) and perform **single-cue signal attribution** to identify which on-screen cues drive correct ordering, using symmetric **GOAL-ONLY / VISUAL-ONLY** baselines and an **empirical per-N null** distribution. All hypotheses are **pre-registered** so null results remain informative. *(Results will characterise how VLM ordering accuracy changes with N and which visual cues are decisive.)*

### 3.3. Research questions
- **RQ1.** Suy luận trật tự màn của VLM **giảm thế nào khi N tăng**?
- **RQ2.** VLM **dựa vào tín hiệu nào trên màn** để biết thứ tự (signal attribution)?
- **RQ3.** “Giá của việc không biết trật tự” (**ordering gap**) lớn cỡ nào?

### 3.4. Contributions
- **C1.** Đặt bài toán **Screen-Order Inference** + giao thức xáo-trộn chống rò-rỉ thứ-tự (cổng KB).
- **C2.** **Thước đo τ-b chấm thứ-tự-bộ-phận** với nhãn cặp-bắt-buộc **suy từ gold (tất định)** → **chống vòng-lập-luận** (đóng góp phương pháp cốt lõi, neo Kendall 1938 + Lapata CL 2006).
- **C3.** **Signal attribution một-cue** + baseline đối xứng + null-theo-N → trả lời “AI dựa vào đâu”.

### 3.5. Dữ liệu · Phương pháp · Thí nghiệm
- **Dữ liệu:** AndroidControl (episode đa bước + gold trajectory). *(Có thể bổ sung GUI-Odyssey làm robustness — future/optional.)*
- **Phương pháp:** Stage-0 sắp-thứ-tự (hỏi-từng-cặp → tổng hợp) → so với gold; signal-attribution theo từng cue.
- **Thí nghiệm dự kiến:** đường cong τ-b theo N (≥30 episode/mốc, N∈[3,~6], báo thêm tới ~8–10) · ordering-gap · phân tầng một-cue · GOAL-ONLY/VISUAL-ONLY/RANDOM. Pre-register + hiệu chỉnh đa-kiểm-định.

### 3.6. Vì sao hợp FAIR (venue khó/cạnh tranh hơn)
- **Mới về bài toán + phương pháp đánh giá** (chống-vòng-lập-luận, signal-attribution) → đủ “độ mới” cho venue khó.
- **Reference-based, định lượng, tiếng Anh, dataset đã bình duyệt** (AndroidControl) → đúng khẩu vị hội nghị nghiên cứu.
- **Thừa nhận prior-art** (Sort-Story 2016, Wu 2022, RankGPT 2023) ở trục sắp-ảnh; claim độ mới ở **miền GUI + cách đánh giá** → an toàn, chuyên nghiệp.

---

## 4. Bảng RANH GIỚI — bằng chứng KHÔNG trùng

| Trục | BÀI 1 (VCL/DG1) | BÀI 2 (FAIR/DG2) |
|---|---|---|
| Câu hỏi | Chấm hướng dẫn **1 ảnh** không-tham-chiếu | **Suy luận trật tự** nhiều ảnh |
| Đầu vào | 1 ảnh + câu hỏi | N ảnh **xáo trộn** + mục tiêu |
| Dataset | MobileViews (+ ScreenSpot) | AndroidControl |
| Metric headline | grounding · hallucination · clarity | **Kendall τ-b partial-order** |
| Phân tích đặc trưng | thang bậc cơ chế C1/C3/C4 | signal-attribution + ordering-gap |
| Ngôn ngữ | Tiếng Việt (+ demo VN) | Tiếng Anh |
| Kết quả chính | bộ điểm chất-lượng-tutorial | đường cong τ-b theo N + cue nào trả công |

→ **Khác cả 7 trục.** Phần duy nhất dùng chung là **pipeline + động cơ** → xử lý theo §1 (viết ngắn, dẫn nhau).

---

## 5. Cách FAIR “thoát trùng” với VCL (viết cụ thể)
- Mở đầu FAIR: *“Building on a reference-free evaluation for single-screen tutorials [cite VCL paper], this work addresses a different problem: inferring screen ORDER in multi-step workflows.”*
- FAIR **không lặp** bảng số DG1; chỉ 1 câu nhắc + trích.
- Pipeline: FAIR mô tả **Stage-0 sắp-thứ-tự** (phần mới của FAIR) là chính; phần sinh per-màn chỉ tóm tắt + dẫn VCL.

---

## 6. Lịch trình & quan hệ với luận văn
1. **VCL trước** (dễ, gọn, tiếng Việt) — lấy “điểm tựa” + được xuất bản sớm.
2. **FAIR sau** — trích VCL, tập trung 100% vào DG2 (mới hơn).
3. **Luận văn** = gộp cả hai + chương framework chung + chương kết-luận. (2 bài báo = 2 chương đóng-góp; hoàn toàn chuẩn.)

---

## 7. Rủi ro & cách phòng
| Rủi ro | Phòng |
|---|---|
| Reviewer thấy 2 bài “na ná” | Bảng §4 + FAIR trích VCL + headline khác hẳn (1-ảnh-chấm vs nhiều-ảnh-sắp-xếp) |
| Mỗi bài bị chê thiếu nội dung | VCL: thêm pilot người + demo VN; FAIR: thêm signal-attribution + ordering-gap + null-theo-N |
| Lệch chủ đề với CFP | **Đọc Call-for-Papers** từng hội nghị trước, chỉnh tựa/khung cho khớp |
| Tự-đạo-văn (text) | Viết lại phần chung bằng câu chữ khác; FAIR là tiếng Anh nên không copy VCL tiếng Việt |

---

## 8. Đoạn NÓI VỚI THẦY (thuyết phục)

> “Thưa thầy, đề tài của em vốn có **hai đóng góp tách bạch**: (1) **đánh giá hướng dẫn sinh từ một ảnh** khi không có đáp án mẫu, và (2) **suy luận trật tự màn** từ nhiều ảnh. Hai phần này **khác câu hỏi, khác dữ liệu, khác thước đo**, nên em đề xuất tách thành **2 bài báo không trùng nhau**:
> – **VCL (nộp trước, tiếng Việt)** trình phần (1) — gọn, tự-chứa, kèm **demo tiếng Việt**, dễ được nhận, giúp em có công bố đầu tiên sớm.
> – **FAIR (nộp sau, tiếng Anh)** trình phần (2) — mới hơn về *bài toán + cách đánh giá chống-vòng-lập-luận*, hợp một venue cạnh tranh hơn. Bài FAIR sẽ **trích dẫn bài VCL** và chỉ tập trung vào phần mới, nên **không vi phạm trùng lặp**.
> Cả hai gộp lại đúng bằng **luận văn** của em, mỗi bài là một chương đóng góp. Em xin thầy duyệt hướng tách này để bắt đầu viết VCL trước ạ.”

---

*Lưu ý kiểm chứng: nên đọc Call-for-Papers (chủ đề, độ dài, ngôn ngữ, chính sách trùng-lặp) của **VCL** và **FAIR** trước khi chốt tựa/khung. Mọi citation trong bài lấy từ nguồn đã xác minh (AndroidControl–NeurIPS 2024; ScreenSpot–ACL 2024/ICLR 2025; Chim et al.–CL 2025; Kendall 1938; Lapata CL 2006). MobileViews là preprint → chỉ dùng làm nguồn ảnh/nhãn.*
