# HỒ SƠ CONTEXT LUẬN VĂN THẠC SĨ
## "Sinh tự động hướng dẫn sử dụng phần mềm bằng LLM từ ảnh giao diện + câu hỏi use-case"

> **Đọc file này là hiểu đủ toàn bộ luận văn.** Tài liệu tự-chứa, viết cho người đọc lần đầu (kể cả AI như Gemini). Mọi thuật ngữ viết tắt đều được giải thích ngay tại chỗ. Cập nhật: 2026-07-05.

---

## 0. TÓM TẮT TRONG 1 PHÚT

Luận văn xây một **hệ thống dùng mô hình ngôn ngữ-thị giác (VLM) để tự động viết hướng dẫn sử dụng phần mềm từng bước**, đầu vào là **ảnh chụp màn hình giao diện (UI screenshot)** cộng **một câu hỏi bằng ngôn ngữ tự nhiên** (ví dụ: *"Làm sao để bật thông báo?"*), đầu ra là **hướng dẫn từng bước** cho con người đọc và làm theo.

Vấn đề cốt lõi: **không tồn tại bộ dữ liệu "hướng dẫn chuẩn do người soạn" để làm đáp án đối chiếu (ground truth).** Vì vậy luận văn có **hai đóng góp ngang nhau về trọng lượng**:

- **(A) Một HỆ THỐNG sinh hướng dẫn "bám sát màn hình"** — có cơ chế chống việc mô hình "bịa" ra nút/thao tác không có trên màn hình.
- **(B) Một PHƯƠNG PHÁP ĐÁNH GIÁ không cần đáp án chuẩn, không để mô hình tự chấm điểm chính nó** — áp dụng được cho cả trường hợp một màn hình lẫn nhiều màn hình.

Khung đánh giá được **kế thừa ý tưởng** từ một bài báo tạp chí (Chim, Ive, Liakata 2025 — xem mục 9), nhưng luận văn **không** kế thừa bài toán sinh của họ; chỉ mượn triết lý "đánh giá dữ liệu tổng hợp khi không có đáp án chuẩn".

---

## 1. BÀI TOÁN & HỢP ĐỒNG ĐẦU VÀO/ĐẦU RA

**Tên đề tài (đã chốt):** Sinh tự động hướng dẫn sử dụng phần mềm bằng LLM, từ ảnh giao diện (UI screenshot) + câu hỏi use-case.

**Đầu vào → Đầu ra:**
- **Đầu vào:** *(1)* **một ảnh** giao diện (trường hợp "một màn hình") **HOẶC** *(N ảnh đã bị xáo trộn thứ tự)* (trường hợp "nhiều màn hình") **+** *(2)* một câu hỏi ngôn ngữ tự nhiên.
- **Đầu ra:** hướng dẫn **từng bước** cho người dùng cuối đọc, bám sát ngữ cảnh trong ảnh.

**Tính chất bài toán:** đa phương thức (multimodal): ảnh + văn bản → văn bản.

**Cái khó trung tâm:** không có "hướng dẫn vàng" (gold instruction) do con người viết sẵn để so sánh. Đây chính là lý do phải phát minh ra phương pháp đánh giá riêng (đóng góp B).

**Hai thuật ngữ nội bộ (chỉ dùng khi trao đổi, TRÁNH trong slide/bảo vệ):**
- **"Một màn hình"** (nội bộ gọi tắt là DG1): đầu vào chỉ 1 ảnh.
- **"Nhiều màn hình"** (nội bộ gọi tắt là DG2): đầu vào N ảnh, hệ phải tự sắp lại đúng thứ tự trước khi sinh hướng dẫn.
- Trong tài liệu này tôi sẽ dùng cả hai cách gọi; khi trình bày chính thức thì luôn nói **"một màn / nhiều màn"**.

---

## 2. HAI ĐÓNG GÓP NGANG NHAU (đây là điều BẤT BIẾN của luận văn)

Người hướng dẫn/tác giả rất kiên quyết giữ **hai đóng góp có trọng lượng ngang nhau**. Không được hạ đóng góp (A) xuống mức "chỉ là kỹ thuật lập trình".

### (A) HỆ THỐNG sinh hướng dẫn bám-sát-màn
Gồm hai khối:
1. **Lớp "trung-thực-hoá" (faithfulness layer):** đối chiếu từng nút/thao tác mà mô hình đề xuất với **cây phần tử giao diện thật** (View Hierarchy / accessibility tree — danh sách các thành phần UI kèm tên và toạ độ). Nếu một bước **không khớp** với phần tử thật (tức mô hình đang bịa), thì **viết lại bước đó thành mô tả bằng lời chung chung, KHÔNG đoán sang một nút khác**. Cơ chế này *model-agnostic* (thay mô hình nào cũng chạy) và **triển khai được thực tế**.
2. **Khối sắp thứ tự màn hình** (chỉ dùng cho trường hợp nhiều màn): hỏi mô hình từng cặp ảnh "màn nào trước, màn nào sau?", tổng hợp bằng thuật toán **Copeland** (đếm số cặp thắng), rồi **phá vòng mâu thuẫn** bằng thuật toán *minimum feedback arc set*, dựa trên 5 tín hiệu thứ tự (xem mục 3).

### (B) PHƯƠNG PHÁP ĐÁNH GIÁ không-gold, không-tự-chấm
Áp dụng cho cả một màn và nhiều màn. Chi tiết ở mục 4.

### Trục phân định hai nhánh đánh giá
Ranh giới giữa nhánh "một màn" và "nhiều màn" là: **CÓ hay KHÔNG có "chuỗi thao tác đúng có sẵn trong dataset" (gold trajectory)** để đối chiếu.
- **Một màn (DG1):** dataset KHÔNG có gold trajectory → phải đánh giá gián tiếp qua đối chiếu cây phần tử.
- **Nhiều màn (DG2):** dataset CÓ gold trajectory → chấm được thứ tự và độ chính xác từng bước.

### Cách "thủ" khi giám khảo tấn công đóng góp A
Đòn tấn công dễ đoán nhất: *"Faithfulness tăng là do thiết kế ép buộc, đâu phải phát hiện khoa học?"* (gọi là đòn "faithfulness by-construction"). Cách phản biện (4 chân):
1. Faithfulness tăng **vì hệ đạt đúng mục tiêu thiết kế** — đó là bằng chứng thiết kế đúng, không phải gian lận.
2. Báo cáo **trung thực tỉ lệ mô hình bịa ở bản gốc + tỉ lệ phải dùng phương án dự phòng (fallback)** — KHÔNG khoe con số "100% trung thực sau khi sửa".
3. (A) là nghiên cứu nhờ có **đối-chứng-thất-bại đo được**: phương án ngây thơ "đoán nút gần nhất" tạo ra **lỗi ngầm** (silent error — sửa sai mà không ai biết), từ đó luận văn chốt "chỉ mô tả bằng lời, không đoán".
4. Phần "nhiều màn" và chỉ số "độ chính xác từng bước" cho ra **con số năng lực thật**, chứng minh giá trị nghiên cứu.

**Điều kiện để giữ "ngang nhau":** phần nhiều màn / chỉ số bước phải **ra được số dương thật** (chứng minh hệ có năng lực thực). Nếu số đó dương, trọng lượng của (A) đến từ **phát hiện thực nghiệm** (đo mức bịa trên nhiều mô hình + đối-chứng-thất-bại + sắp thứ tự màn + phân tích tín hiệu), KHÔNG phải từ độ phức tạp của code.

**Không claim "vượt SOTA leaderboard".** Setup của luận văn khác hẳn các bảng xếp hạng agent-bấm-máy: ta sinh hướng dẫn cho **con người đọc**, không phải cho agent tự động thao tác. Nhánh (B) và phần đo cơ chế theo nguyên tắc "kết quả null vẫn có giá trị khoa học"; riêng claim của (A) thì kỳ vọng dương.

**Tách thành 2 bài báo:**
- **Bài VCL** = phần một màn (DG1), viết tiếng Việt, nộp trước.
- **Bài FAIR** = phần nhiều màn (DG2), viết tiếng Anh, nộp sau.

---

## 3. PIPELINE (một hệ thống duy nhất, có bộ định tuyến đầu vào)

### Trường hợp MỘT MÀN (DG1) = 3 hộp xử lý
1. **VLM sinh "mù":** mô hình ngôn ngữ-thị giác chỉ được thấy **ẢNH + CÂU HỎI**, **KHÔNG** được đưa danh sách nút. Nó sinh ra bản hướng dẫn gốc (BASE). *Quan trọng:* câu hỏi cũng **không chứa tên nút** → mô hình buộc phải tự đọc ảnh, và đó chính là chỗ nó dễ bịa.
2. **Thuật toán so khớp embedding:** đối chiếu từng tên nút mà mô hình nhắc tới với cây phần tử giao diện (View Hierarchy). Nếu độ tương đồng ≥ ngưỡng τ → **khớp** (nút có thật); nếu < τ → **bịa**. Đây là **thuật toán**, KHÔNG phải một LLM khác.
3. **Với bước bị coi là bịa → viết lại thành MÔ TẢ bằng lời**, tuyệt đối KHÔNG đoán sang nút khác, KHÔNG tra cây phần tử để gán tên mới. Cách xử lý này được gọi là **"PA2"** (phương án 2). Luận văn đã **bỏ hẳn** phương án "correction/sửa lỗi" cũ, vì việc sửa dễ sửa-bậy → tạo lỗi ngầm.

### Trường hợp NHIỀU MÀN (DG2) = kế thừa nguyên pipeline một màn + thêm "Stage-0" ở đầu
Khi đầu vào là N ảnh bị xáo trộn:
- Hỏi VLM từng **cặp** ảnh: "màn nào đứng trước?"
- Tổng hợp bằng **Copeland** (mỗi ảnh được điểm = số ảnh khác mà nó "thắng" trong so cặp; phá hoà bằng quy tắc tất định).
- **Phá vòng mâu thuẫn** (khi A>B, B>C, C>A): dùng thuật toán *minimum feedback arc set*. **Trọng số cạnh** lấy từ **biên độ thắng của Copeland / độ nhất quán khi hỏi lại nhiều lần / số cạnh tối thiểu phải cắt** — **KHÔNG** dùng "độ tự tin do VLM tự khai báo" vì mô hình hiệu chỉnh (calibration) kém.
- Ra được chuỗi màn đã sắp đúng thứ tự → chạy pipeline một màn cho từng màn.
- **Nếu N=1** thì Stage-0 rỗng, quay về đúng trường hợp một màn.

*(Nền tảng học thuật của từng thành phần đều có bài peer-reviewed: so cặp bằng LLM — Qin et al. NAACL 2024; Copeland — Dwork et al. WWW 2001; minimum feedback arc set — Ailon et al. JACM 2008; tác vụ sắp lại chuỗi ảnh — Sort-Story EMNLP 2016; ngưỡng τ — Fagin et al. SIAM 2006 & Lapata CL 2006.)*

### LUẬT VÀNG chống rò rỉ đáp án (data leakage)
**Cây phần tử giao diện và đáp án vàng CHỈ được dùng vào lúc CHẤM ĐIỂM, KHÔNG được dùng vào lúc sinh hoặc sắp thứ tự.** Câu hỏi không chứa tên nút. Lưu ý: "chấm baseline" là một bước **đánh giá**, không phải một bước trong hệ thống khi triển khai thực tế (khi deploy chỉ có: sinh → tự kiểm → né bịa).

### 5 tín hiệu thứ tự (ordering cues)
Trả lời câu hỏi "mô hình dựa vào đâu để biết màn nào trước màn nào?":
1. **Gating** — màn này chặn, phải làm xong mới sang màn kia.
2. **Nav-affordance** — có nút Next/Back gợi ý hướng đi.
3. **State-delta** — thay đổi trạng thái (toggle bật/tắt, ô trống → đã điền, badge xuất hiện).
4. **Title-progression** — tiêu đề màn thể hiện tiến trình (Bước 1/3...).
5. **Drill-down** — đi sâu vào menu con.

Phân tích "mô hình dùng tín hiệu nào" được làm bằng **phân tầng một-cue** (chỉ giữ những cặp ảnh mà đúng **một** tín hiệu phân biệt chúng), **KHÔNG** che pixel, **KHÔNG** tin lời mô hình tự khai.

---

## 4. CHỈ SỐ ĐÁNH GIÁ & TÍNH HỢP LỆ

### Chỉ số cho MỘT MÀN (so với cây phần tử View Hierarchy)
- **Độ trung thực (faithfulness)** = 1 − (số bước bịa) / (số bước có nhắc tới nút). Dựa trên phương pháp ALOHa (NAACL 2024). **Con số headline = TỈ LỆ BỊA Ở BẢN GỐC** (quan sát sơ bộ ~¼ số bước), **KHÔNG** phải con số ~100% sau khi đã sửa (con số sau sửa bị trần do thiết kế, khoe nó là gian lận). Báo cáo ở dạng **"có điều kiện recall-VH"**: loại các nút chỉ có icon / nhãn chung chung khỏi mẫu số; và nói rõ ~¼ chỉ là quan sát sơ bộ trên 1 mô hình, chưa phải phát hiện tổng quát.
- **Độ đúng nhãn (label fidelity)** = có gọi đúng tên hiển thị của nút không. **Đây là chỉ số tự định nghĩa** (khai thẳng như vậy) — khớp chuỗi ký tự ≠ độ rõ ràng cho người đọc.
- **Độ đúng chỗ (grounding, point-in-bbox)** = toạ độ (x,y) mô hình chỉ có nằm trong khung nút không. Dựa trên SeeClick (ACL 2024); ngưỡng dung sai 14% lấy từ AITW (NeurIPS 2023). **CẢNH BÁO quan trọng:** (x,y) phải đến từ **một bộ định vị độc lập** (kiểu ScreenSpot, dự đoán toạ độ từ tên nút + ảnh), **KHÔNG** được lấy tâm của bbox đã khớp — nếu lấy tâm thì thành đúng 100% một cách vô nghĩa (tautology). Vì rủi ro này, chỉ số grounding đã được **đưa RA KHỎI headline của phần một màn** — chỉ dùng ở phần nhiều màn (nơi có toạ độ vàng) hoặc để đối chứng với ScreenSpot.

### Chỉ số cho NHIỀU MÀN (so với đáp án vàng)
- **τ (tau) — độ đúng thứ tự bộ phận** = (số cặp đúng thứ tự − số cặp sai) / (tổng số cặp bắt buộc). **Chỉ phạt các cặp BẮT BUỘC** (cặp mà thứ tự là ép buộc về mặt nhân quả). Đây là công thức của **Fagin 2006 "Comparing partial rankings" + Lapata CL 2006**, KHÔNG phải "Kendall τ-b". Nhãn "cặp bắt buộc" được **suy ra TỪ ĐÁP ÁN VÀNG** bằng quy tắc nhân quả (màn B chỉ hiện ra sau khi làm đúng thao tác vàng ở màn A), KHÔNG suy từ mô hình hay bộ dò tín hiệu (để chống tự-chấm). Các cặp tự do (ví dụ điền email trước hay số điện thoại trước đều được) thì đảo thứ tự vẫn tính đúng.
- **Step-SR (Step Success Rate, teacher-forced)** = số bước đúng / số bước vàng. Một bước tính đúng khi **đúng loại thao tác VÀ sai lệch toạ độ ≤ 14%**. Dựa trên AndroidControl (NeurIPS 2024). Đây là trục tham chiếu chuẩn của ngành, KHÔNG claim ngang leaderboard.

### Chống vòng lặp tự-chấm (anti-circularity)
- **Bên QUYẾT ĐỊNH** khớp/fallback dùng embedding **nomic** (đo theo ngưỡng τA).
- **Bên CHẤM ĐIỂM** dùng **3 cơ chế độc lập, khác họ mô hình**: embedding **bge-m3** (họ khác nomic) + một LLM-judge nhị phân khác họ + độ trùng token.
- Vì mô hình sinh là **gpt-4o-mini** (họ GPT), nên **LLM-judge tuyệt đối KHÔNG dùng mô hình họ GPT**.

### Cách validate (kiểm định) chính bộ chỉ số
Dùng **perturbation test tự động** = bơm các lỗi đã biết trước vào hướng dẫn (một cách độc lập với bộ khớp), rồi đo xem bộ chỉ số có phát hiện ra không, tỉ lệ báo động giả bao nhiêu, có đơn điệu không. Dựa trên Sai et al. (EMNLP 2021). **Người hướng dẫn KHÔNG thích chấm bằng người** → tương quan-với-người là *future-work*, KHÔNG nằm trong tiêu chí đậu/rớt. Đóng khung rõ: "perturbation = đo độ nhạy = điều kiện cần, CHƯA phải bằng chứng convergent validity đầy đủ".

### 6 nguyên tắc validate bộ khớp/bộ chấm (mỗi nguyên tắc có 1 trụ peer-reviewed)
1. Bộ khớp đo theo **ngữ nghĩa** + validate với người trên 80–120 cặp → báo Precision/Recall + hệ số đồng thuận Cohen's κ, rồi **cố định (freeze) ngưỡng τ**. (Trụ: ALOHa NAACL 2024.)
2. Gán tay tối thiểu (kiểu human-in-the-loop) → giảm ~**80%** công gán nhãn. (Trụ: Active Evaluation, ACL 2022 Outstanding Paper — con số peer-reviewed là 80%, KHÔNG phải 89%.)
3. LLM-judge phải **khác họ** với mô hình sinh + neo vào người; KHÔNG validate judge bằng chính nhãn do LLM tạo. (Trụ: Panickssery NeurIPS 2024 + Zheng NeurIPS 2023.)
4. Cây phần tử/accessibility tree **KHÔNG phải ground truth** (>77% ứng dụng thiếu nhãn) → phải biện minh bằng cơ chế hậu-kiểm + fallback. (Trụ: Chen et al. ICSE 2020 Distinguished Paper.)
5. Validate chỉ số CHÍNH bằng perturbation. (Trụ: Sai EMNLP 2021 + Ribeiro ACL 2020.)
6. Bỏ tương quan-với-người khỏi cổng đậu/rớt. (Trụ: Clark et al. ACL-IJCNLP 2021.)

### Thống kê
Cluster bootstrap **theo ứng dụng** (các màn cùng một app không độc lập với nhau) + khoảng tin cậy 95% + hiệu chỉnh Holm (khi so nhiều chỉ số) + cố định seed + 10.000 lần resample + **đăng ký trước (pre-register) ngưỡng TRƯỚC khi nhìn kết quả** + tối thiểu 30 episode cho mỗi mốc N. Vì số cụm nhỏ (khoảng 17 app), dùng **wild-cluster bootstrap-t** (Cameron-Gelbach-Miller 2008) và khai báo caveat under-coverage.

---

## 5. DATASET (3 bộ, mỗi bộ một vai cố định — đã verify tận file nguồn)

| Bộ dữ liệu | Nội dung | Có gold trajectory? | Vai trò |
|---|---|---|---|
| **MobileViews** | ảnh + cây phần tử (VH) + bbox | KHÔNG | **một màn / DG1** |
| **AndroidControl** | episode nhiều màn + accessibility tree + thao tác vàng mỗi bước | CÓ | **nhiều màn / DG2 + Step-SR** |
| **ScreenSpot-v2** | ảnh + bbox chuẩn | — | **đối chứng grounding** + bù độ tin cậy cho MobileViews |

**Chi tiết đã verify sâu (2026-07-03):**
- **MobileViews** = preprint arXiv 2409.14337 (bản v3 đổi tên thành "Million-scale"). Giấy phép **MIT**. Của BUPT + Tsinghua. Thu thập **tự động** bằng bot VLM-DroidBot. Paper nói 1,2 triệu màn nhưng **bản công khai chỉ 600K**; luận văn dùng **81 màn / 17 app**. Cấu trúc VH: trường `class` + `bounds` dạng `[[x1,y1],[x2,y2]]`.
- **AndroidControl** = "On the Effects of Data Scale on UI Control Agents", Li et al., Google DeepMind, **NeurIPS 2024 Datasets & Benchmarks** (arXiv 2406.03679). Giấy phép **CC0**. Dữ liệu người thật thao tác trên Pixel trong ~1 năm. 8 loại thao tác. **Tập test = 1.542 episode (KHÔNG phải 2.855 như một số nguồn ghi nhầm).** Tổng 15.283 episode / 833 app; trung bình ~5,5 bước; phân vị 95 = 13 bước.
- **ScreenSpot-v2** = đi kèm **OS-Atlas (ICLR 2025)**; gốc là SeeClick (ACL 2024). Giấy phép **apache-2.0**. 1.272 chỉ dẫn (502 mobile / 334 desktop / 436 web); đã sửa 11,32% lỗi nhãn của bản gốc; bbox dạng `[x1,y1,x2,y2]`.

**Ghi chú vai trò:**
- Cả MobileViews lẫn AndroidControl đều **có nguồn phần tử** (VH / a11y tree). Bộ chỉ-có-ảnh-trần thì cần một bộ dò riêng (và phải đo recall của bộ dò đó — đây là cổng kiểm định K1). Thực tiễn: trên thiết bị thật, accessibility tree có sẵn **live** qua AccessibilityService (dịch vụ trợ năng).
- **AITW (NeurIPS 2023):** là nguồn của ngưỡng dung sai 14% → trích dẫn bắt buộc; dùng làm dataset đối chứng thì tuỳ chọn.
- **Mind2Web (nhánh web) = future-work.**
- Để đo nhiều màn: episode của AndroidControl **bị xáo trộn**, hệ xếp lại, đối chiếu với gold. Chưa có sẵn thống kê số episode theo từng độ dài N → phải tự đếm histogram (cổng kiểm định KN).

---

## 6. TRẠNG THÁI HIỆN TẠI (2026-07-05)

**Giai đoạn:** đề cương/thiết kế đã hoàn chỉnh, có **kết quả sơ bộ**. Đã qua nhiều vòng review sâu bằng multi-agent + debate giám khảo mô phỏng.

**Phát hiện & sửa quan trọng nhất (circularity):** phiên bản cũ để bộ khớp **vừa sửa vừa chấm** → faithfulness ~100% là con số vô nghĩa (tautology). Đã vá bằng: **PA2** (chỉ khớp/fallback, không sửa) + chấm bằng **bge-m3 độc lập**. Claim của phần một màn được thu hẹp lại còn **DUY NHẤT một điều: "giảm việc tham chiếu tới nút không tồn tại, cái giá phải trả là tỉ lệ fallback"** (đã bỏ claim "đúng nhãn"; phần "sửa đúng" để dành cho nhiều màn / Step-SR).

**Kết quả sơ bộ (mô hình gpt-4o-mini, mẫu nhỏ):**
- Tỉ lệ mô hình bịa ở bản gốc ~¼ số bước.
- Lớp trung-thực-hoá nâng faithfulness ở mọi ngưỡng τ, **nhưng** khoảng tin cậy còn chạm 0 (do n nhỏ, mới 1 app cũ).
- Tỉ lệ fallback ~19%.
- Độ đúng nhãn và format đứng yên (chứng minh "không gây hại" — no-harm).
- **Bản chạy chính thức (81 màn / 17 app) CHƯA chạy** (cần API).

**5 điều chỉnh lớn đã áp dụng sau debate giám khảo (gọi là M1–M5):**
- **M1:** đưa chỉ số điểm-trong-khung (point-in-bbox) RA KHỎI phần một màn, dời sang phần nhiều màn (tránh tautology tâm-bbox).
- **M2:** thêm cổng kiểm định **K-pair** = đo độ chính xác so-cặp THÔ của VLM so với gold (sàn phải > 0.5) TRƯỚC khi tổng hợp Copeland — nếu ~0.5 thì Stage-0 vô hiệu, phải khai thẳng. Đồng thời BỎ cách "cắt cạnh ít chắc nhất" (vì VLM hiệu chỉnh kém).
- **M3:** thống kê dùng wild-cluster bootstrap-t + khai báo caveat số cụm nhỏ (~17); timestamp pre-register = `git init` + commit trước khi chạy; số hiện tại đánh dấu "exploratory".
- **M4:** tính độ-phủ-nhãn của cây phần tử → báo tỉ lệ bịa ở dạng khoảng "có điều kiện recall-VH", loại nút icon-only/nhãn-chung khỏi mẫu số.
- **M5:** đổi cách nói "hai đóng góp ngang nhau" thành **"ngang nhau CÓ ĐIỀU KIỆN (chờ kết quả nhiều màn dương)"**.

**Kết quả các vòng kiểm tra sức khoẻ đề tài (2026):**
- **Freshness scan 2025-2026:** đề tài KHÔNG lỗi thời, KHÔNG bị "scoop" (không ai đã ghép "sinh hướng dẫn cho người + đánh giá không-gold trên GUI"). Chỉ cần thêm ~8 trích dẫn định vị vào related-work, và **nên thêm ≥1 mô hình sinh đời mới** (GPT-4.1 / Gemini-2.5-Flash / Qwen3-VL) bên cạnh gpt-4o-mini để bảng số không kẹt ở mô hình cũ.
- **Debate giám khảo với pipeline:** kết luận **PASS có điều kiện** — KHÔNG có lỗi thiết kế; rủi ro chỉ nằm ở tài liệu hoá + chưa có số chính thức.
- **3 điều PHẢI NÂNG để đạt chuẩn 2026:** (1) đo tỉ lệ bịa trên ≥1 mô hình frontier 2025-26 giá rẻ (Gemini-2.5-Flash / GPT-4.1-mini) bên cạnh gpt-4o-mini, báo dạng đường-cong-theo-model chứ không phải headline "¼" tĩnh; (2) thêm baseline listwise một-shot (kiểu RankGPT) chấm cùng τ + Step-SR + cột chi phí, đóng khung so-cặp như một "audit chất nền"; (3) đóng khung lại (A) là "model-agnostic BY CONSTRUCTION, kiểm trên 3 đời mô hình" + đẩy mạnh **ứng dụng ngách on-device** (thiết bị có a11y-tree live + mô hình nhỏ không gọi được frontier).

---

## 7. MÔI TRƯỜNG & CODE (harness)

- **Máy KHÔNG có GPU** → VLM nhìn ảnh **phải dùng API cloud** (`gpt-4o-mini`; API key nằm ở `harness/.openai_key`, không được in ra). Chạy local qua Ollama: `nomic-embed-text`, `bge-m3` (chấm độc lập), `llama3.2`, `qwen2.5vl:3b/7b`.
- Windows: chạy Python phải đặt `$env:PYTHONIOENCODING="utf-8"`.
- **Dữ liệu:** `dataset_samples/mv_multiapp/` = 90 màn / 18 app thô → lọc rác còn **81 màn / 17 app**. App được suy từ tên màn (`screen.split("_")[0]`) → cho phép cluster theo app.
- **Các script chính trong `harness/`:** `dg1_data.py` (lọc rác), `dg1_run.py` (sinh bản gốc + PA2, có retry khi lỗi 429, resume theo tag), `dg1_pa2_score.py` (chấm PA2 + cluster bootstrap + Holm + seed), `dg1_independent_score.py` (chấm bằng bge-m3 độc lập + đo lỗi ngầm), `dg1_scorer.py` (nạp VH, tính point-in-bbox), `aloha_match.py`, `dg1_questions.py`, `dg1_vh_coverage.py` (đo độ phủ nhãn — đã viết, CHƯA chạy).

**Nguyên tắc chi tiền (người dùng nhấn mạnh):** chạy MỘT lần cho đúng; mọi bước tốn API phải HỎI trước; ưu tiên local/free + cache.

---

## 8. VIỆC TIẾP THEO & CÁC CỔNG KIỂM ĐỊNH

**Việc free (chưa làm):** cố định τA + báo precision/recall của bộ khớp (tập gán tay 80–120 cặp, precision ≥ 0.95); dựng harness perturbation; module LLM-judge khác họ; tính con số độ phủ nhãn VH.

**Việc tốn API (~$0.05, phải hỏi trước):** sinh câu hỏi gieo-từ-affordance + cổng answerability; sinh bản gốc cho 81 màn.

**5 cổng kiểm định cứng (kill-test) phải qua:**
- **K1:** đo recall của bộ dò phần tử.
- **KN:** đếm histogram độ dài episode.
- **KZ':** kiểm prior-art về sắp ảnh — ĐÃ GO.
- **KB:** chống rò rỉ chỉ số bước (strip metadata + tái mã hoá ảnh + che status bar/đồng hồ/pin/badge + loại episode 2-ảnh trùng pixel).
- **K-pair:** đo độ chính xác so-cặp thô của VLM so với gold TRƯỚC khi tổng hợp Copeland — nếu ~0.5 thì Stage-0 vô hiệu.

(KN và KZ' đã qua.)

**Kill-test tuần 1:** K1 + KN + KB → chốt khung với người hướng dẫn → xây harness → chạy ablation.

---

## 9. NEO HỌC THUẬT & CÁC TRÍCH DẪN ĐÃ VERIFY

**Bài báo neo khung đánh giá:** Chim, Ive, Liakata — *Evaluating Synthetic Data Generation from User Generated Text*, **Computational Linguistics 51(1):191–233, 2025** (tạp chí, KHÔNG phải "ACL 2025"). Luận văn **chỉ kế thừa khung ĐÁNH GIÁ** (Intrinsic + Extrinsic) cho "văn bản tổng hợp không có đáp án chuẩn", KHÔNG kế thừa bài toán sinh của họ (họ làm text→text).

**Prior-art phải thừa nhận (về sắp thứ tự ảnh):** Sort-Story (EMNLP 2016, dùng Spearman), Wu et al. (ACL 2022), RankGPT (EMNLP 2023, listwise). **Độ mới của luận văn** = miền GUI + điều-kiện-hoá theo mục tiêu + gắn việc sắp thứ tự vào việc sinh hướng dẫn + suy partial-order từ gold + phân tích tín hiệu.

**Các trích dẫn cốt lõi khác đã verify:** oracle = Barr et al. TSE 2015; ALOHa = NAACL 2024; SeeClick = ACL 2024; AITW = NeurIPS 2023; AndroidControl = NeurIPS 2024; OS-Atlas = ICLR 2025.

**Must-cite 2025-2026 (đã verify, để định vị related-work):** FaithScore (Findings EMNLP 2024, faithfulness reference-free cho LVLM — luận văn khác ở chỗ verify với VH có cấu trúc); VECTOR/What-Happens-When (2512.08979, "VLM mù thời gian" → luận cứ ủng hộ phần nhiều màn + chống leak); LLM-as-Meta-Judge (2603.09403, gần ý tưởng nhánh B → phải phân định rõ là ta ở miền GUI + bơm-lỗi-độc-lập-matcher); UI-TARS (2501.12326); GUI-Odyssey (ICCV 2025) / AMEX / ScreenSpot-Pro (acknowledge landscape).

**Tiền lệ "pipeline đơn giản mà vẫn đậu":** G-Eval, SelfCheckGPT, FActScore, RAGAS, ALOHa, BERTScore.

**Nguyên tắc trích dẫn:** xương sống phương pháp CHỈ trích bài peer-reviewed; preprint (OmniParser, Qwen, MobileViews...) chỉ dùng như hiện vật kỹ thuật, không làm trụ phương pháp. Luôn verify venue + năm trước khi trích.

---

## 10. CÁC ĐIỂM CHƯA CHỐT

- **Mô hình open/closed:** khuyến nghị bắt đầu bằng VLM API (gpt-4o-mini) làm lõi; thêm Qwen2.5-VL để so "đóng vs mở" nếu còn ngân sách. Fine-tune off-the-shelf ở lõi; LoRA-grounding là tuỳ chọn.
- **Tiếng Việt:** người hướng dẫn ưu tiên tiếng Việt, nhưng dataset chuẩn là tiếng Anh/Trung → phần định lượng chạy EN/ZH; tiếng Việt = demo định tính + ~120 mẫu app Việt cho chuyên gia đánh giá (nói rõ với thầy: KHÔNG có bảng số định lượng tiếng Việt).
- **Nhánh web (Mind2Web):** future-work.

---

## 11. NHỮNG ĐIỀU TUYỆT ĐỐI GIỮ (checklist bất biến)

1. **Hai đóng góp ngang nhau** (có điều kiện: chờ số nhiều màn dương). Không hạ (A) xuống "chỉ engineering".
2. Trong slide/bảo vệ: nói **"một màn / nhiều màn"**, KHÔNG dùng "DG1/DG2".
3. **Không claim vượt SOTA leaderboard.**
4. **Luật vàng chống leak:** VH + đáp án vàng chỉ vào lúc chấm.
5. **Headline một màn = tỉ lệ bịa bản gốc (~¼, có điều kiện)**, KHÔNG khoe 100% sau sửa.
6. Bên quyết định (nomic) ≠ bên chấm (bge-m3 + judge khác họ + token-overlap).
7. LLM-judge KHÔNG dùng họ GPT (vì generator là gpt-4o-mini).
8. Validate metric chính = perturbation; tương quan-với-người = future-work, KHÔNG phải cổng đậu/rớt.
9. Chỉ trích peer-reviewed cho phương pháp; verify venue/năm trước khi dùng.
10. Grounding point-in-bbox phải từ bộ định vị độc lập, KHÔNG lấy tâm bbox.

---

*Hết hồ sơ context. Nếu cần chi tiết hơn về bất kỳ mục nào (công thức đầy đủ, mã giả, ví dụ chạy đầu-cuối, danh sách Q&A giám khảo), đó nằm trong các file report nội bộ của luận văn.*
