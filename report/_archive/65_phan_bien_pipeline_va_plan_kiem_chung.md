# report/65 — Tự phản biện pipeline: chắc chỗ nào, nghi chỗ nào + plan kiểm chứng chia nhỏ

> Trả lời câu user (2026-07-17): *"Nghiên cứu kỹ, phản biện thử — chắc chắn vẫn đi với pipeline này phải không? Nếu không chắc thì lên plan chia nhỏ deep-research/debate, tôi sẽ thực thi sau."*
>
> **Trả lời thẳng: KHÔNG chắc 100%.** Xương sống (distill + trọng tài ngoài + held-out theo app + báo cáo hai tầng) tôi tin vững — vì cấu trúc dữ liệu ép, đã kiểm ở report/64. Nhưng khi tự phản biện đến cùng, tôi tìm thấy **6 nghi ngờ chưa có bằng chứng**, trong đó **1 cái nếu hỏng thì phải sửa pipeline thật** (không phải chỉ thêm thí nghiệm). Phần 1 liệt kê nghi ngờ + mức sát thương. Phần 2 là plan kiểm chứng chia nhỏ — mỗi vòng độc lập, có câu hỏi viết sẵn để dán, có cổng quyết định.
>
> Quan hệ với 2 file plan trước: `report/63` = các phương án NÂNG CẤP (risk-coverage, template, OCR, DPO); file này = kiểm PIPELINE CÓ ĐỨNG KHÔNG. Chỗ trùng được ánh xạ rõ ở Phần 2, không lặp nội dung.

---

## PHẦN 1 — Sáu nghi ngờ, xếp theo mức sát thương

### NGHI 1 — Matcher (trọng tài) có thể hỏng CẢ HAI CHIỀU ⚠️ nặng nhất — hỏng là phải sửa pipeline

Toàn bộ pipeline đứng trên một giả định: matcher embedding phân biệt được "tên nút có thật" và "tên nút bịa". Nhưng:

- **Chiều bỏ lọt (false negative):** embedding đo độ GẦN NGHĨA. Mà VLM bịa kiểu gì? Nó bịa tên **hợp lý và gần nghĩa** với nút thật — màn có "Settings" thì nó bịa "Preferences", có "Save" thì bịa "Confirm". Cosine của các cặp này CAO → matcher có nguy cơ cho qua đúng những ca bịa **điển hình nhất**. Nếu bỏ lọt nhiều: tập "đã lọc" vẫn bẩn → Tier 1 (lọc vs raw) nhỏ hoặc null vì lý do tầm thường.
- **Chiều kết oan (false positive):** VH thiếu nhãn (55.6% phần tử dạng ảnh — Fok CHI22) → bước ĐÚNG bị đánh là bịa → fallback oan, data mất chi tiết tốt.

Bằng chứng hiện có: chỉ số sơ bộ trên mẫu nhỏ, chưa có phép đo hai chiều có chủ đích. **Đây là mắt xích duy nhất mà nếu đứt, "lọc" — đóng góp trung tâm — mất nghĩa.** Tin tốt: kiểm được **free, local, ngay bây giờ** (vòng K1).

### NGHI 2 — Phạm vi lọc: chỉ bắt bịa TÊN PHẦN TỬ, lọt bịa HÀNH ĐỘNG/LUỒNG

Matcher chỉ soi những bước có nhắc tên nút. Nhưng model còn bịa kiểu khác: *"vuốt sang trái để mở menu"* (không có gesture đó), *"vào tab Lịch sử"* (không có tab đó — nếu diễn đạt không khớp mẫu trích tên thì lọt), bịa cả một màn trung gian không tồn tại. Nếu loại bịa-ngoài-tên-nút chiếm phần lớn tác hại thực tế → claim "giảm bịa" phải thu hẹp thành "giảm bịa-tên-phần-tử" — vẫn sống nhưng yếu đi rõ. **Chưa từng đếm** tỉ trọng loại này trên chính data của mình, dù đếm được free trên kết quả BASE sơ bộ cũ (vòng K2).

### NGHI 3 — Ngã rẽ chưa có bằng chứng: teacher sinh MÙ rồi lọc, hay teacher NHÌN VH từ đầu?

Đã nêu ở report/64 §3.2, nhắc lại vì đây là nghi ngờ thiết kế thật sự chứ không phải tuỳ chọn nâng cấp. Lý lẽ "sinh mù rồi lọc thì data có ví dụ né → student học được hành vi né" nghe xuôi nhưng là **trực giác chưa kiểm**. Phản biện hoàn toàn có thể đòi arm "teacher nhìn VH" làm baseline — và nếu arm đó cho student tốt hơn thì đóng góp "lọc" lung lay. report/61 Q4 xác nhận literature chưa so trực tiếp → không trích được ai, phải tự xử bằng debate + (nếu cần) thí nghiệm.

### NGHI 4 — Student có học "né ĐÚNG CHỖ" không, hay chỉ học "né đúng TẦN SUẤT"?

SFT dạy bắt chước phân bố. Kịch bản xấu: student học được "khoảng 1/5 số bước thì viết câu mô tả chung chung" và rắc fallback **ngẫu nhiên** — tỉ lệ bịa vẫn giảm (vì nói cụ thể ít đi), %fallback giống hệt thiết kế mong muốn, nhưng model không hề biết bám màn. **Cặp thước hiện tại không tách được hai trường hợp này.** Cần một phép đo "né có đúng chỗ không" (đây là lý do sâu nhất khiến khung selective-prediction ở report/61/63 đáng quan tâm — không phải để trình bày đẹp, mà để bịt đúng lỗ này).

### NGHI 5 — "Còn gì để lọc": chọn teacher gpt-4o-mini là con dao hai lưỡi

Tier 1 so student-lọc vs student-raw — delta đến từ những chỗ teacher bịa. Teacher càng ít bịa → hai tập train càng giống nhau → Tier 1 null vì chẳng có gì khác nhau. gpt-4o-mini (đời 2024, bịa ~¼ theo sơ bộ) vô tình là lợi thế cho thí nghiệm — nhưng mở ra đòn phản biện đối xứng: *"dùng teacher 2026 xịn thì đâu cần lọc?"*. Câu thủ phải chuẩn bị trước bằng số liệu (đo bịa của ≥1 teacher đời mới trên chính task này — nếu >0 rõ rệt thì lớp lọc vẫn có việc) + lý lẽ on-device (model nhỏ tự sinh vẫn bịa, và student 3B là thứ chạy thật trên máy). Một phần đã nêu ở report/42 M1 nhưng chưa gắn vào khung model hiện tại.

### NGHI 6 — Câu fallback có HỮU ÍCH thật với người đọc không?

Toàn bộ lý lẽ "viết lại thành mô tả an toàn" giả định câu mô tả đó dùng được. Chưa ai xác nhận. Nếu người dùng đọc *"hãy tìm nút phù hợp trong khu vực cài đặt"* và bó tay → ta chỉ đổi "sai nguy hiểm" lấy "vô dụng lịch sự". Kiểm nhanh được bằng một vòng đọc tay ~30 câu fallback thật (free) + là đúng chỗ cho mẫu người nhỏ nếu thầy cho phép.

### Tóm bảng

| Nghi | Nếu đúng là hỏng thì… | Kiểm bằng | Chi phí |
|---|---|---|---|
| 1. Matcher hai chiều | **sửa pipeline** (nâng trọng tài: OCR/luật/ngưỡng kép) | kill-test local | free |
| 2. Lọt bịa ngoài-tên-nút | thu hẹp claim + cân nhắc thêm luật bắt hành-động | đếm tay trên data cũ | free |
| 3. Mù-rồi-lọc vs nhìn-VH | thêm arm thí nghiệm, có thể đổi cách kể đóng góp | debate → (nếu cần) 1 lần train thêm | debate free; arm ~$ |
| 4. Né đúng chỗ vs đúng tần suất | thêm thước đo (selective) | debate + research nhỏ | free |
| 5. Teacher ít bịa → không còn gì lọc | chuẩn bị câu thủ + số frontier | pilot API nhỏ | ~$1-2, hỏi trước |
| 6. Fallback vô dụng | sửa template + cần mẫu người | đọc tay 30 câu | free |

**Kết luận Phần 1:** đi tiếp với pipeline này — CÓ, nhưng chỉ sau khi K1/K2 (free, vài giờ) cho số đẹp. Nếu K1 xấu, chỗ sửa là NÂNG TRỌNG TÀI (fusion, luật, ngưỡng kép), không phải đập khung — khung thay thế nào cũng vẫn cần một trọng tài, và trọng tài nào cũng phải qua đúng phép thử này.

---

## PHẦN 2 — Plan kiểm chứng chia nhỏ (bạn thực thi sau, mỗi vòng độc lập)

Ba track: **K = kill-test local free** (chạy trước, cho số thật) · **D = debate đa-agent** · **R = deep-research nhỏ**. Mỗi vòng có câu hỏi viết sẵn. Thứ tự khuyến nghị: K1 → K2 → (D1, D2 song song) → R1/R2 chen khi cần → K3 cuối (tốn tiền, hỏi trước).

### K1 — Kill-test matcher hai chiều (NGHI 1) — LÀM ĐẦU TIÊN
- **Loại:** thực nghiệm local, không cần API (nomic-embed qua Ollama + 127 màn/VH có sẵn).
- **Cách chạy:** (a) chiều bỏ lọt: lấy ~50 màn, với mỗi màn tạo tập tên-nút-bịa-gần-nghĩa (đổi "Settings"→"Preferences", "Save"→"Confirm"… tự sinh bằng từ điển đồng nghĩa + vài ca bịa THẬT từ kết quả BASE sơ bộ cũ) → đo bao nhiêu % bịa-gần-nghĩa được matcher cho qua ở ngưỡng τ hiện tại; (b) chiều kết oan: lấy ~50 bước ĐÚNG đã xác nhận tay → đo bao nhiêu % bị đánh bịa. Vẽ hai đường theo τ.
- **Cổng quyết định:** bỏ-lọt ≤ ~20% và kết-oan ≤ ~10% ở một τ nào đó → matcher đạt, freeze τ, đi tiếp. Vượt → mở vòng C của report/63 (OCR fusion) + cân nhắc ngưỡng kép (nghi-ngờ-thì-hỏi-lại) TRƯỚC khi build data. Số cụ thể của cổng nên chốt trước khi nhìn kết quả.

### K2 — Đếm phân loại bịa trên data cũ (NGHI 2)
- **Loại:** đọc tay, free, ~2 giờ. Lấy 40-60 bước bịa/lỗi từ kết quả BASE sơ bộ (đã có sẵn) → phân loại: bịa tên-phần-tử / bịa hành-động-cử-chỉ / bịa màn-luồng / khác.
- **Cổng:** bịa-tên-phần-tử chiếm ≥ ~70% → claim hiện tại đứng, chỉ cần một câu giới hạn phạm vi. Dưới → phải thêm luật bắt động-từ-hành-động vào matcher (bàn ở D1) và viết lại claim.

### K3 — Đo "còn gì để lọc" với teacher đời mới (NGHI 5) — ✱ tốn API ~$1-2, HỎI TRƯỚC
- **Loại:** pilot API nhỏ, 15-20 màn × (gpt-4o-mini + 1 model 2025-26 rẻ). Ghép chung với pilot MDE đã có kế hoạch để không tốn hai lần.
- **Cổng:** teacher mới vẫn bịa >0 rõ rệt → có câu thủ bằng số. Gần 0 → chuyển trọng tâm lý lẽ sang "student 3B on-device tự nó bịa" và đo bịa của Qwen2.5-VL-3B base (local, free) làm bằng chứng chính.

### D1 — Debate: sinh MÙ rồi lọc vs teacher NHÌN VH (NGHI 3)
- **Loại:** debate đa-agent (2 phe + verify + chủ toạ), free.
- **Câu hỏi dán sẵn:** *"Cho pipeline distill dạy VLM 3B sinh hướng dẫn GUI (inference chỉ có ảnh): Phương án A = teacher sinh mù rồi lọc bằng VH, giữ ví-dụ-né trong data. Phương án B = teacher nhìn VH khi sinh, data sạch từ đầu nhưng không có ví dụ né. Phe A và phe B tranh luận: (1) student nào trung thực hơn trên app lạ không có VH lúc chạy? (2) phản biện hội đồng có quyền đòi arm B làm baseline không, và nếu thiếu nó bài có bị bác không? (3) nếu chỉ đủ tiền train 2 arm (không phải 3), chọn cặp nào?"*
- **Cổng:** debate ra "arm B bắt buộc" → thêm 1 lần gọi teacher + 1 lần train vào budget, cập nhật report/56. Ra "không bắt buộc, chỉ cần thủ miệng" → viết sẵn đoạn thủ vào report/54.

### D2 — Debate: trục "ĐÚNG" bằng AndroidControl từng-bước (điểm 1 của report/64)
- **Loại:** debate, free.
- **Câu hỏi dán sẵn:** *"Đề xuất: chặt episode AndroidControl thành từng bước rời (màn + gold action), cho model sinh hướng dẫn rồi trích hành-động-đầu-tiên để so gold (đúng loại + đúng đích trong dung sai) — làm trục đo 'hướng dẫn ĐÚNG' bổ sung cho trục 'không bịa'. Phản biện 3 hướng: (1) bước trích-hành-động-từ-text tự nó sai bao nhiêu và có làm thước đo vô nghĩa không? (2) câu hỏi đưa model là goal của episode — model không biết tiến độ đã làm tới đâu, so với gold next-action có công bằng không, xử lý sao? (3) thêm thí nghiệm này SAU khi đã commit report/56 có phá pre-registration không, trình thầy thế nào cho sạch?"*
- **Cổng:** sống cả 3 → thêm vào bộ TN như thí-nghiệm-bổ-sung khai báo rõ là hậu-đăng-ký. Chết ở (1) hoặc (2) → bỏ, chấp nhận giới hạn "mùa này chỉ đo trung thực".

### D3 — Debate: "né đúng chỗ" đo thế nào (NGHI 4) — gộp với vòng A của report/63
- **Loại:** debate + đọc kỹ 2 bài đã có URL (CAP PMLR v304, SafeGround) trước, chỉ search bổ sung nếu thiếu.
- **Câu hỏi dán sẵn:** *"Thiết kế đo 'model né đúng chỗ' cho sinh hướng dẫn GUI khi không có gold: (1) đo mức-bước (bước né ↔ phần tử liên quan có thật thiếu/mơ hồ trên màn?) khả thi không khi không biết model ĐỊNH nói nút nào; (2) đo mức-quần-thể bằng đường risk-coverage có đủ trả lời không; (3) với 12 app test, đường cong có ổn định không, cần calibration set riêng không; (4) nếu chỉ thêm MỘT phân tích phụ không phá pre-reg, chọn dạng nào?"*
- **Cổng:** ra được một phép đo khả thi → thêm làm phân tích phụ (không thay headline đã đăng ký). Không ra → khai giới hạn này thẳng trong luận văn (một đoạn "threats to validity").

### R1 — Deep-research nhỏ: taxonomy bịa GUI (NGHI 2, phần văn liệu)
- **Câu hỏi (3 góc):** đã ai phân loại hallucination của VLM trong miền GUI thành element/action/flow chưa · benchmark nào đo bịa-hành-động (không phải bịa-vật-thể) · các hệ lọc element-level có khai giới hạn này không, khai thế nào.
- **Cổng:** có taxonomy trích được → dùng để đóng khung claim + đối chiếu số K2. Không có → K2 tự thành đóng góp quan sát nhỏ, ghi vào bài.

### R2 — Deep-research nhỏ: chọn teacher yếu có tiền lệ không (NGHI 5, phần văn liệu)
- **Câu hỏi (2-3 góc):** có công trình nào bàn việc distill từ teacher CÓ NHIỄU + lọc, so với teacher sạch hơn không lọc · "noisy teacher + verifier" có tên gọi/dòng nghiên cứu riêng chưa · có ai lập luận "chọn teacher rẻ + lọc rẻ hơn chọn teacher xịn" bằng số chi phí chưa.
- **Cổng:** có tiền lệ → thêm 1-2 citation thủ cho đòn "sao không dùng teacher xịn". Không có → câu thủ dựa hoàn toàn vào số K3, phải chắc K3 chạy.

### Bản đồ phụ thuộc

```
K1 (matcher) ─┬─ ĐẠT → freeze τ → K2 → D1, D2 (song song) → D3/R1/R2 theo nhu cầu → K3 (ghép pilot MDE)
              └─ RỚT → mở vòng C report/63 (OCR fusion) + ngưỡng kép → chạy lại K1 → mới đi tiếp
```

Mọi vòng đều nhỏ (debate ~20-30 agent; research 2-3 góc ~25-35 agent; kill-test local vài giờ máy). Kết quả mỗi vòng ghi report riêng kèm bảng claim sống/chết như report/61. **Không vòng nào được phép sửa report/56 trực tiếp** — mọi thay đổi bộ TN đi qua bàn với thầy + commit có ghi chú hậu-đăng-ký.
