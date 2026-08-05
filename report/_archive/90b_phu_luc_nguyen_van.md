
## B. 27 đòn sống sót sau vòng bác bỏ (xếp theo mức nghiêm trọng SAU khi kiểm)

### B1. [CHÍ MẠNG] Cổng validate thước 'AUC=1.000' là tự-chứng; trên paraphrase thật thước RỚT (AUC=0.35, 10/10 kết oan) → headline Δ(Student−Teacher) có nguy cơ là artifact phong cách

- **Trục:** Đủ ngưỡng luận văn thạc sĩ? + logic đổi hướng + khả thi (giám khảo hoài nghi, tự kiểm số trước khi đọc report)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** CHÍ MẠNG → **sau kiểm chéo:** CHÍ MẠNG

**Vấn đề.** Perturbation 'paraphrase' trong metric_v1_validate.py chỉ xáo lại ĐÚNG token gốc của gold (dòng 115-119: '{Verb} on the {tgt}' với tgt = chính content-token của gold → Jaccard=1.0 tất yếu), còn 'target_error' chọn target KHÔNG chồng token nào (dòng 96-97) → hai phân phối được XÂY để tách rời, AUC=1.000 by construction. Tôi chạy probe với 10 cặp paraphrase-đồng-nghĩa THẬT (cùng nút, khác chữ: 'filter option'↔'funnel icon', 'settings icon'↔'gear icon', 'compose button'↔'pencil icon'...) vs 10 cặp bịa-gần-nghĩa: 10/10 paraphrase thật bị chấm 0 (kết oan 100%), AUC(para>near)=0.350 — TỆ HƠN TUNG XU. Backstop bge-m3 τ=0.85 không cứu được ca nào: sim paraphrase thật = 0.49-0.79 CHỒNG LẤN sim bịa 0.59-0.72 ('gmail tab'↔'calendar tab' [bịa] = 0.717 > 'search bar'↔'magnifying glass' [thật] = 0.490) → lời hứa 'chỉnh backstop khi có output model' (report/84:44, 85:84) đâm lại đúng bức tường K1 đã chết, không có τ nào tách được. HỆ QUẢ CHÍ MẠNG: Student train TRÊN gold AC học đúng phân bố từ vựng gold ('Click on X'), Teacher zero-shot diễn đạt khác ('Tap the funnel icon') bị kết oan hệ thống → hiệu-cặp Student−Teacher (headline trục ĐÚNG, kết cục PASS report/85 §7) bị thổi phồng một chiều bởi khớp-giọng chứ không phải đúng-hơn. Report/85 §8 rủi ro 4 khẳng định thước 'action∧target bớt nhạy phong cách' — đo được là SAI: token-overlap là thước nhạy phong cách NHẤT khi từ vựng khác nhau. Thêm nữa ~48% target AC là icon (report/79 tự đo) — chính vùng mà từ vựng gọi tên phân kỳ mạnh nhất ('+' bị regex content_tokens loại luôn). Teacher 30% trong MDE pilot cũng bị nén bởi chính lỗi kết oan này.

**Bằng chứng.** harness/metric_v1_validate.py:115-119 (paraphrase giữ nguyên token), :96-97 (target_error zero-overlap); chạy lại cổng ra đúng AUC=1.000; probe tự viết: AUC=0.350, para kết oan 10/10, near bỏ lọt 0/10; bge sims đo được: settings/gear=0.794, back-arrow/go-back=0.718 (thật) vs gmail/calendar-tab=0.717, save/send=0.695 (bịa); đối chiếu report/84:7 'QUA CỔNG... cả ca dễ LẪN ca khó', report/85 §4 'false-positive paraphrase 0.000 ✓' — đã commit b5a6b29 với chữ 'metric-gate PASSED'

**Đề xuất sửa.** TRƯỚC khi đốt tiền train: (1) chạy lại cổng với bộ paraphrase-đồng-nghĩa thật (icon↔tên chức năng, human-rewrite 50-100 cặp) và ghi nhận thước hiện tại rớt; (2) vá thước bằng từ-điển chuẩn-hoá nút/icon (đúng hướng report/75 đề xuất cho matcher nhưng chưa áp vào thước chấm) + đo lại; (3) bất kể vá kiểu gì, thêm bước chấm-tay mẫu con (~50 cặp step Student & Teacher) để ƯỚC LƯỢNG bias kết-oan theo arm và báo hiệu-cặp đã hiệu chỉnh; (4) sửa report/84/85: cổng mới qua trên perturbation-giữ-từ-vựng, KHÔNG được viết 'giải được chỗ K1 chết'

**Người phản-bác nói gì.** Tôi cố bác nhưng không bác được; ngược lại kiểm chứng độc lập trên dữ liệu THẬT còn nặng hơn probe của họ.

1) Phần "AUC=1.000 tự-chứng" ĐÚNG về mã. `/mnt/d/Master/Thesis/harness/metric_v1_validate.py` dòng 115-119: paraphrase = `f"{v} on the {tgt}"` với `tgt = target_of(g[i])` → giữ NGUYÊN content-token gold → Jaccard=1.0 tất yếu; dòng 96-97 target_error chọn alt sao cho `set(content_tokens(alt)) & cur` rỗng → Jaccard=0 tất yếu. Hai phân phối được dựng để tách rời. Điểm giảm nhẹ DUY NHẤT cho tác giả: report/84 mục "Hoài nghi còn lại" §1 và §3 đã TỰ KHAI đúng chỗ này ("tôi giữ nguyên từ-lõi → Jaccard=1 tất yếu", "perturbation do chính tôi dựng → có phần circular"). Nên đây là lỗ đã-biết, không phải che giấu. NHƯNG report/85 §4 vẫn ghi bảng cổng "false-positive paraphrase 0.000 ✓ / AUC 1.000 ✓" như một cổng ĐÃ QUA và đóng băng vào đăng-ký-trước, commit b5a6b29 "metric-gate PASSED" — tức là lời tự-khai KHÔNG chảy được vào chỗ nó phải chặn. Cổng vẫn vô hiệu.

2) Phần hệ quả (nguy hiểm hơn) tôi xác nhận bằng ĐO, không phải suy luận. Tôi ghép lại 91 cặp (teacher gpt-4o-mini output ↔ gold step_instruction) từ cache pilot có sẵn — tái tạo đúng điểm 0.286/0.30 của report/86 — rồi chỉ đổi các lựa chọn BỀ MẶT của thước, không đổi nội dung nào:
   - nguyên trạng (Jaccard + action chặt): 0.286
   - gộp tap/open/navigate thành một lớp chạm: 0.330
   - thay Jaccard bằng containment: 0.473
   - cả hai + bỏ từ chỉ vị trí: 0.604
   Điểm teacher NHẢY 0.286 → 0.604 chỉ do lựa chọn từ-vựng/chuẩn-hoá của thước. 33/65 ca "trượt" có containment target ≥0.5 (nhiều khả năng CÙNG nút).

3) Ví dụ kết oan là hệ thống chứ không lẻ tẻ: 'Tap the CNN app' vs 'Open CNN app' (ts=0.905 nhưng a_ok=False); 'Tap the "World" category' vs 'Go to the World category' (ts=0.905, rớt vì action); 'Tap the Search bar' vs 'Click on the search box' (ts=0.333); 'Type "Knoxville" in the search bar' vs 'Type Knoxville' (ts=0.333); 'Tap the Gmail icon' vs 'Select Gmail for sharing the Article' (ts=0.25 — rớt vì gold có thêm mệnh đề mục đích); 'Tap the Share icon' vs 'Click on the share icon on top right side of the screen' (ts=0.25 — rớt vì gold có cụm vị trí). Hai cơ chế kết oan: (a) ACTION_MAP coi "open"/"go" khác "tap" dù cùng một cú chạm; (b) Jaccard bị pha loãng bởi cụm vị-trí/mục-đích mà gold AC rất hay có.

4) Vì thế khẳng định report/85 §8 rủi ro 4 "thước ưu tiên action∧target (bớt nhạy phong cách)" là SAI theo số: chính lớp action là bẫy phong cách (+4.4 điểm chỉ do gộp lớp), và target-Jaccard nhạy phong cách nhất đúng lúc từ vựng lệch. Backstop bge-m3 τ=0.85 gần như không cứu ca nào (nó chỉ chạy khi j<0.5, và ngưỡng 0.85 hiếm khi chạm) → lời hứa "chỉnh backstop khi có output model" (report/84 §1, report/85 §8.2) đâm lại đúng bức tường K1.

5) Chuỗi nhân quả tới headline là thật: Student SFT trên gold AC sẽ sinh đúng giọng gold ("Click on the search icon at the bottom right corner"), Teacher zero-shot sinh giọng khác ("Tap the Search icon") → thắng ở đúng 33/65 ca kể trên mà không đúng-hơn một chút nào. Δ(Student − Teacher) — headline trục ĐÚNG, kết cục PASS report/85 §7 — do đó bị thổi phồng một chiều bởi khớp-giọng. Đồng thời điểm nền 0.30 và SD=0.362 trong report/86 (→ MDE) cũng tính bằng thước này nên nhiễm theo.

Chỗ DUY NHẤT tôi trừ điểm người ra đòn: bộ probe 10 cặp của họ ('search bar'↔'magnifying glass', 'compose button'↔'pencil icon') là chọn tay ở cực đại phân kỳ (đặt tên theo hình vs theo chức năng) nên AUC=0.350 là cận dưới bi quan, không phải phân bố thật. Nhưng điều đó không cứu được gì — dữ liệu thật với mức phân kỳ nhẹ hơn nhiều đã đủ tạo hố 32 điểm phần trăm.

Kết luận: không hạ mức. Đây là lỗi CHÍ MẠNG với hiện trạng (cổng validate không chứng minh được điều nó tuyên bố; estimand headline bị lẫn phong cách; pre-registration đã commit trên nền đó). Sửa được, không phải chết đề tài: bơm-lỗi paraphrase phải sinh ĐỘC LẬP với logic token của thước (đổi danh từ loại nút, bỏ/thêm cụm vị-trí, đổi động từ chạm) rồi chạy lại cổng; gộp lớp action tương đương; đổi Jaccard→containment + tước cụm vị-trí/mục-đích; và bắt buộc thêm arm đối chứng phong-cách (Teacher few-shot mồi bằng ví dụ gold-style) để tách "khớp giọng" khỏi "đúng hơn". Phải làm TRƯỚC khi train, và phải sửa lại report/85 + ghi rõ cổng cũ vô hiệu thay vì để commit b5a6b29 đứng như đã-qua.

**Bằng chứng của người kiểm.** Mã: /mnt/d/Master/Thesis/harness/metric_v1_validate.py:96-97 (target_error zero-overlap), :115-119 (paraphrase giữ nguyên content-token → Jaccard=1 by construction), :60-68 (target_score, backstop chỉ chạy khi j<0.5 với TAU_BGE=0.85), :20-31 (ACTION_MAP tách open/navigate khỏi tap).
Tài liệu: /mnt/d/Master/Thesis/report/84_*.md mục "Hoài nghi còn lại" §1+§3 (TỰ KHAI circularity) vs "Phán quyết 1 dòng" + /mnt/d/Master/Thesis/report/85_*.md §4 bảng cổng (FP paraphrase 0.000 ✓, AUC 1.000 ✓), §3 (headline), §8.2+§8.4 ("bớt nhạy phong cách"); commit b5a6b29 "metric-gate PASSED".
Đo lại (dữ liệu thật, free, không gọi API): ghép 91 cặp teacher↔gold từ /mnt/d/Master/Thesis/harness/dg1_cache/mde_pilot/gen.json + episode json trong ~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test → tái tạo điểm 0.286 (khớp mean 0.301 của /mnt/d/Master/Thesis/harness/mde_pilot_results.json). Biến thể thước: gộp tap/open/navigate → 0.330; containment thay Jaccard → 0.473; cả hai + bỏ từ vị-trí → 0.604. 33/65 ca trượt có containment target ≥0.5. Cặp kết oan điển hình: 'Tap the CNN app' vs 'Open CNN app' ts=0.905 a_ok=False; 'Tap the "World" category' vs 'Go to the World category' ts=0.905 a_ok=False; 'Tap the Search bar' vs 'Click on the search box' ts=0.333; 'Tap the Gmail icon' vs 'Select Gmail for sharing the Article' ts=0.25.
Bối cảnh khớp: /mnt/d/Master/Thesis/report/79_*.md dòng 15 (~48% gold-click là icon/ảnh) — đúng vùng từ vựng phân kỳ mạnh nhất, và regex content_tokens `[a-z0-9@._]+` loại luôn ký tự '+'.

---

### B2. [NẶNG] AUC=1.000 là một hằng đẳng thức số học, không phải phép đo — cổng không thể rớt

- **Trục:** THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, metric_v1_results.json, mde_pilot.py, report/84, report/85)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** CHÍ MẠNG → **sau kiểm chéo:** NẶNG

**Vấn đề.** Bộ bơm-lỗi dựng ca 'paraphrase' bằng cách LẮP LẠI câu từ chính target_of(gold) (dòng 117-118: g[i]=f"{v} on the {tgt}" với tgt=target_of(g[i])). Vì 'on/the' là stopword và v luôn nằm trong ACTION_MAP, tập content_tokens của 'paraphrase' TRÙNG KHỚP TUYỆT ĐỐI với gold → Jaccard = 1.0 theo định nghĩa. Đối xứng, ca 'target_error' (dòng 97) ÉP chọn target có tập từ-nội-dung GIAO RỖNG với gold → Jaccard = 0 theo định nghĩa. AUC = P(1.0 > 0) = 1.0 với phương sai BẰNG KHÔNG. Không tồn tại dữ liệu nào khiến AUC < 1. Cổng 'rớt AUC<0.80 → DỪNG, KHÔNG train' (report/85:53) do đó không bao giờ kích hoạt được — nó không phải cổng. Về khoảng tin cậy: cận dưới rule-of-three trên 185 ep là 0.984, nhưng con số đó vô nghĩa vì thống kê không có biến thiên. Vấn đề không phải cỡ mẫu nhỏ, mà là estimand được dựng sẵn.

**Bằng chứng.** harness/metric_v1_validate.py:97 (ép giao rỗng), :115-119 (paraphrase tái dựng từ target_of). Chạy lại (probe1): 994/1027 bước paraphrase có Jaccard = 1.0 CHÍNH XÁC (96.8%), 33 bước còn lại rỗng-cả-hai và được backstop cứu về 1.0; 168/185 bước target_error có Jaccard = 0 CHÍNH XÁC (90.8%), 17 ca còn lại max 0.20. metric_v1_results.json: paraphrase_mean=0.9999999998, target_error_mean=0.0118.

**Đề xuất sửa.** Ngừng trích AUC=1.000 như bằng chứng. Dựng lại tập validate từ nguồn ĐỘC LẬP với hàm chuẩn-hoá của matcher: (a) paraphrase do người/LLM khác-họ viết lại trên output THẬT, không tái dựng từ token của thước; (b) sai-target lấy từ các nút CÙNG MÀN trong VH/a11y (đối thủ thật), bỏ ràng buộc giao-rỗng. Báo AUC kèm CI bootstrap theo episode. Đây là việc phải làm TRƯỚC khi chi tiền train.

**Người phản-bác nói gì.** Tôi đã cố bác và không bác được phần cốt lõi: cơ chế đòn nêu là CÓ THẬT và tôi tái hiện được bằng số. Nhưng mức phải hạ từ chi_mang xuống nang, vì ba lý do dưới.

**Phần đòn ĐÚNG (không cãi được):**
1. `perturb(kind="paraphrase")` dựng lại bước bằng `f"{v} on the {tgt}"` với `tgt=target_of(g[i])`. Mọi `v` đều nằm trong ACTION_MAP, "on/the" đều trong STOP → `content_tokens` của bản paraphrase TRÙNG TUYỆT ĐỐI với gold. Probe của tôi: 170/177 bước bị sửa có Jaccard đúng 1.0; 7 ca còn lại rỗng-cả-hai → backstop bge cos(" "," ")=1.0 → cũng về 1.0. Tức paraphrase bị GHIM Ở TRẦN 1.0 trên 177/177 = 100% ca.
2. `target_error` (dòng 97) ép chọn alt có `content_tokens` GIAO RỖNG với gold → 178/185 Jaccard đúng 0, 7 ca còn lại max 0.25.
3. Vì pos ghim ở trần tuyệt đối 1.0, AUC=P(pos>neg) chỉ có thể <1 nếu neg cũng chạm đúng 1.0 — điều mà ràng buộc giao-rỗng loại trừ theo định nghĩa. Nên AUC=1.000, phương sai bằng 0. Cổng "AUC<0.80 → DỪNG" không có đường kích hoạt.
4. **Đòn còn NHẸ HƠN thực tế:** cùng cơ chế đó ghim luôn 2 dòng khác của bảng cổng report/85 — `detection_target=1.000` (vì neg luôn <0.5) và `fp_paraphrase=0.000` (vì pos luôn ≥0.5). Ba trong năm dòng cổng là hằng đẳng thức, không phải hai.

**Các đường bác tôi đã thử và THẤT BẠI:**
- "Vòng 2 ca khó cứu được" (report/84 nói target-score-khó=0.350, AUC vẫn 1.0): (a) **code vòng 2 KHÔNG có trong repo** — `metric_v1_validate.py` chỉ có vòng 1, không script nào sinh ra 0.350, con số này không tái hiện được; (b) kể cả tin nó, vòng 2 chỉ làm CỨNG phía âm, còn phía dương vẫn ghim 1.0 → AUC=1 vẫn bị dựng sẵn. Hedge "cả ca khó" ở report/85:50 và report/88:137 không cứu được.
- "Cỡ mẫu / CI": đúng như đòn nói, vấn đề không phải n mà là estimand suy biến. Rule-of-three vô nghĩa khi var=0.

**Vì sao hạ xuống `nang`:**
1. **Tác giả ĐÃ tự khai đúng cơ chế này**, không giấu. report/84 mục "Hoài nghi còn lại" §1 viết nguyên văn: *"tôi giữ nguyên từ-lõi (chỉ đảo trật tự + thêm article) → **Jaccard=1 tất yếu**"*, và §3: *"Perturbation do chính tôi dựng → có phần circular"*. Lỗi thật nằm ở khâu TRUYỀN XUỐNG: report/85 (bản đăng-ký-trước đã commit b5a6b29) và report/88 cắt mất caveat, in "AUC 1.000 ✓ QUA CỔNG". Đây là lỗi framing/pre-reg integrity, không phải nguỵ tạo bằng chứng.
2. **Nó vô hiệu một phép VALIDATE, không bác một KẾT QUẢ.** Không có gì chứng minh thước (action,target) sai — chỉ chứng minh nó CHƯA ĐƯỢC KIỂM. Chưa train, chưa có số headline nào dựa lên AUC này.
3. **Fix free, chạy trước mọi khoản chi:** cho paraphrase thay từ-đồng-nghĩa thật (tab→section, button→control) + lấy target_error từ pool CÓ GIAO từ-nội-dung (đúng ca "Gmail tab" vs "Calendar tab"). Lúc đó AUC mới là phép đo có phương sai. Vài giờ, không tốn API. Sửa pre-reg trước khi thu số là hợp lệ.

**Cái phải chết theo đòn:** câu "tách (action,target) GIẢI được đúng chỗ K1 chết, **đo bằng số không assume**" (CLAUDE.md) và headline report/84 "tin tốt cứng nhất... không phải suy luận mà là số đo" — hai câu này hiện KHÔNG có bằng chứng đỡ, phải rút cho tới khi chạy lại bộ bơm-lỗi không suy biến.

**Cái KHÔNG chết:** các dòng còn lại của bảng bơm-lỗi thật sự có thông tin và đã đổi thiết kế — extra=1.000 lộ ra coverage không phạt nhồi bước (→ thêm F1), reorder=1.000 lộ ra phải tách order-τ riêng, target/action/missing tụt ~0.15 đúng tỉ lệ 1/5 bước. Harness bơm-lỗi không phải sân khấu toàn phần, chỉ đúng dòng AUC + 2 dòng detection/FP là sân khấu.

**Bằng chứng của người kiểm.** TÁI HIỆN (probe riêng, ~/.venvs/thesis/bin/python, nạp trực tiếp harness/metric_v1_validate.py, SEED=20260719, 185 ep):
- paraphrase, chỉ đếm bước THỰC SỰ bị sửa: 177 bước → Jaccard đúng 1.0: 170; rỗng-cả-hai (backstop kéo về 1.0): 7; không có giá trị nào khác. => 177/177 ghim ở trần 1.0.
- target_error: 185 bước → Jaccard đúng 0.0: 178; còn lại [0.25, 0.25, 0.25, 0.20, 0.20, 0.091, 0.091]. Max 0.25.
=> AUC = P(1.0 > ≤0.25) = 1.0, var = 0. Khớp harness/metric_v1_results.json: separation_auc=1.0, paraphrase_mean=0.9999999998594595, target_error_mean=0.01177, detection_target=1.0, fp_paraphrase=0.0.

CODE (đọc harness/metric_v1_validate.py):
- :117-118 paraphrase = f"{v} on the {tgt}", tgt=target_of(g[i]); mọi v ∈ ACTION_MAP; "on","the" ∈ STOP (:28-29) → content_tokens trùng khít.
- :97 target_error yêu cầu `set(content_tokens(alt)) and not (set(content_tokens(alt)) & cur)` → ép giao rỗng.
- :62-68 target_score: j=Jaccard; :74 step_match ngưỡng J_MATCH=0.5 → :185-186 detection/FP cũng bị ghim theo.
- :128-136 auc() đếm cặp p>n. Không có nguồn biến thiên nào.
=> Hai dòng code đòn trích (:97, :115-119) TỒN TẠI và ĐÚNG nội dung như họ mô tả.

SAI SỐ NHỎ TRONG BẰNG CHỨNG CỦA HỌ (không đổi kết luận):
- Họ ghi "994/1027 bước paraphrase Jaccard=1.0" — 1027 là TỔNG mọi bước kể cả bước KHÔNG bị sửa (bước không sửa dĩ nhiên =1.0, vô nghĩa). Số đúng cần đếm là 177 bước bị sửa. Cách đếm của họ thổi phồng mẫu số ~6 lần.
- Họ ghi 33 ca rỗng-cả-hai; tôi đếm 7. Họ ghi 168/185 target_error Jaccard=0; tôi đếm 178/185. Lệch do trạng thái rng khác nhau khi gọi lại perturb. Hướng và độ lớn không đổi.

TÀI LIỆU:
- report/84 §"Hoài nghi còn lại" §1: "tôi giữ nguyên từ-lõi ... → Jaccard=1 tất yếu" và §3: "Perturbation do chính tôi dựng → có phần circular" — TÁC GIẢ ĐÃ TỰ KHAI CƠ CHẾ NÀY.
- report/85_PREREG_v2_LAI.md:47,50,53 — bảng cổng in "detection 1.000 ✓ / FP 0.000 ✓ / AUC 1.000 (cả ca khó) ✓" + "Cổng cứng: rớt AUC≥0.80 → DỪNG, KHÔNG train". Caveat của report/84 KHÔNG được truyền xuống. Đã commit b5a6b29.
- report/88:137-138, :199 — nhắc lại "AUC=1.000 cả ca dễ lẫn ca khó", "✅ QUA (AUC=1.0)".
- KHÔNG TỒN TẠI code vòng-2 "ca khó": ls harness/*.py + grep "artworks|hard" không ra script nào sinh target_error_mean=0.350. Số 0.350 trong report/84 không tái hiện được từ repo.

---

### B3. [NẶNG] Matcher sai 9/10 ca hiểm mà bộ bơm-lỗi không bao giờ sinh ra — sai CẢ HAI CHIỀU, đúng bệnh của K1

- **Trục:** THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, metric_v1_results.json, mde_pilot.py, report/84, report/85)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NẶNG

**Vấn đề.** Bộ bơm-lỗi chỉ sinh hai cực (token trùng hoàn toàn / giao rỗng). Vùng giữa — nơi thước thật sự phải phân xử — chưa từng được test. Tôi tự dựng 10 ca và chạy qua step_match của tác giả: KHỚP OAN (nhận là đúng trong khi sai): 'Turn off notifications' vs gold 'Turn on notifications' (score 0.667, MATCH — hướng dẫn NGƯỢC NGHĨA vẫn được tính đúng); 'Set the timer to 30 minutes' vs '10 minutes' (0.600, MATCH); 'Enter quantity 5' vs 'quantity 2' (1.000, MATCH — số bị stopword nuốt); 'Click on Tools & Hardware' vs 'Click on Tools' (0.500, MATCH — hai bước gold KHÁC NHAU trong cùng episode); 'Scroll up' vs 'Scroll down' (0.500, MATCH). KẾT OAN (bác bỏ trong khi đúng): 'Tap Log in' vs 'Tap the Sign in button' (0.000); 'Tap the More options icon' vs 'Click on the three-dot menu' (0.000); 'Tap the Trash icon' vs 'Click on Delete' (0.000). Cơ chế: với target dài, Jaccard≥0.5 dung thứ một token đảo nghĩa; với target ngắn, một từ đồng nghĩa là mismatch tuyệt đối. Đây đúng là hai chiều lỗi mà report/73 (K1) mô tả — khẳng định 'tách (action,target) GIẢI được đúng chỗ K1 chết' (CLAUDE.md, report/84:33-38) không được số liệu chống đỡ.

**Bằng chứng.** Chạy probe tự viết trên harness/metric_v1_validate.step_match, output đầy đủ 10 ca ở trên; script tại /tmp/claude-1000/-mnt-d-Master-Thesis/2577d164-1efa-40fc-8357-fedb08789c63/scratchpad/probe3.py. Nguồn logic: metric_v1_validate.py:60-74 (Jaccard J_MATCH=0.5), :28-29 (STOP nuốt 'on','next','item','option'...).

**Đề xuất sửa.** Thêm vào bộ bơm-lỗi ít nhất 4 họ ca hiểm: (1) đảo nghĩa/toggle on↔off; (2) đổi số lượng/số thứ tự; (3) đích cha↔con trong cùng cây UI; (4) từ-đồng-nghĩa nhãn nút (Log in/Sign in, Delete/Trash, three-dot/More). Bỏ 'on' và 'next' khỏi STOP, giữ số nguyên vẹn, và cân nhắc luật cứng: khác token phủ định/số lượng ⇒ mismatch bất kể Jaccard.

**Người phản-bác nói gì.** Tôi cố bác nhưng không bác nổi phần lõi. Ba hướng bác đều thất bại: (1) "ca bịa, không thực tế" — sai, ca #4 của họ ('Click on Tools' vs 'Click on Tools & Hardware') là văn bản CÓ THẬT trong ac_test_200ep.json, và tôi đo được 122/1027 = 11.9% bước gold bị phủ oan bởi một bước gold KHÁC cùng episode (chạy Jaccard-only, tắt bge → đây là CẬN DƯỚI). (2) "phụ thuộc probe của họ" — sai, tôi viết lại script độc lập bỏ bge và tái hiện 8/9 ca sai. (3) "tác giả đã xử lý rồi" — chỉ đúng MỘT NỬA: chiều KẾT OAN (3 ca đồng nghĩa) đã được khai thẳng ở report/84 "Hoài nghi còn lại" §1 kèm cách sửa và mốc thời gian, nên không được tính là phát hiện mới; nhưng chiều KHỚP OAN (nghịch nghĩa, sai số lượng, cha/con, sai hướng cuộn) KHÔNG có ở bất kỳ đâu trong report/84 hay 85 — đây mới là phần sống của đòn, và là chiều nguy hiểm hơn vì nó THỔI PHỒNG coverage. Khẳng định cấu trúc của họ được xác nhận tận code: perturb() ép target_error phải giao rỗng token (:95) và paraphrase dựng lại target NGUYÊN VĂN (:117) → bộ bơm-lỗi theo thiết kế chỉ sinh J=0 và J=1, không bao giờ chạm vùng giữa vốn chiếm 13.5% cặp bước thật. Vậy AUC=1.000 gần như tautology, và câu "tách (action,target) GIẢI được đúng chỗ K1 chết" (CLAUDE.md, report/84) là OVERCLAIM — nó chỉ chứng minh thước phân biệt được hai cực, đúng thứ mà cả K1 lẫn khớp-chuỗi thuần cũng làm được. Điểm tôi phải THÊM vào chứ không bác được: sai số này KHÔNG triệt tiêu trong hiệu-cặp Student-vs-Teacher. Student train trên chính gold AC → output gần gold về mặt từ vựng → hưởng lợi từ Jaccard dễ dãi; Teacher zero-shot diễn đạt lại → bị chiều kết-oan trừng phạt. Cả hai chiều lỗi đều đẩy Δ về phía giả thuyết. Đây là lý do tôi giữ mức "nang" thay vì hạ. Phần tôi CẮT BỚT của họ: ca 'quantity 5 vs 2' (score 1.000) dựa vào token 1-chữ-số bị filter len>1 nuốt, nhưng số 1-chữ-số chỉ xuất hiện ở 5/1027 = 0.5% bước gold thật → ca ồn ào nhất lại gần như vô hại thực tế; và "sai 9/10" hơi rộng tay (ca 'Tap Settings in Chrome' vs 'Gmail' thước BÁC ĐÚNG). Giảm nhẹ: chưa tốn tiền, chưa train, chưa công bố số nào dựa trên thước này; cách sửa rẻ và free tại chỗ (gỡ on/off/left/right/next khỏi STOP, bỏ filter len>1 cho chữ số, đòi khớp cứng với từ phân cực + số, dùng containment bất đối xứng cho cha/con, và THÊM một họ bơm-lỗi vùng-giữa vào bộ validate). Nhưng phải làm TRƯỚC khi commit report/85, vì ngưỡng bơm-lỗi đang được đóng băng vào bản đăng-ký-trước chính là ngưỡng của một cổng không test đúng vùng cần phân xử.

**Bằng chứng của người kiểm.** KIỂM CODE: /mnt/d/Master/Thesis/harness/metric_v1_validate.py — :28-29 STOP chứa 'on','left','right','next','item','option'; :35-37 content_tokens lọc len(t)>1 (nuốt chữ số đơn); :60-74 target_score/step_match chỉ cần action khớp AND Jaccard>=0.4995; :95 target_error BẮT BUỘC giao token rỗng ("not (set(content_tokens(alt)) & cur)"); :117 paraphrase dựng lại "f'{v} on the {tgt}'" giữ nguyên target → J=1 tất yếu. Đây là bằng chứng cứng cho "bộ bơm-lỗi chỉ sinh hai cực".

CHẠY LẠI ĐỘC LẬP (script riêng, TẮT bge, chỉ Jaccard — cận dưới số ca khớp): tái hiện 'Turn off' vs 'Turn on' J=0.667 MATCH; timer 30 vs 10 J=0.600 MATCH; quantity 5 vs 2 J=1.000 MATCH; Tools & Hardware vs Tools J=0.500 MATCH; Scroll up vs down J=0.500 MATCH; Log in vs Sign in J=0.000 KHÔNG khớp; More options vs three-dot J=0.000; Trash icon vs Delete J=0.000. → 8/9 sai, độc lập với probe của người ra đòn.

ĐO TRÊN DỮ LIỆU THẬT (dataset_samples/androidcontrol_test/ac_test_200ep.json, 185 ep / 1027 bước): cross-credit 122/1027 = 11.9% bước gold được phủ bởi bước gold KHÁC cùng episode, ví dụ thật trong data: "Click on Tools" ↔ "Click on Tools & Hardware", "Click on Tools" ↔ "Click on Hand Tools", "Tap on the cross icon to clear the search bar" ↔ "Tap on the search bar at the top of the screen", "Click on the search icon at the bottom right corner of the keyboard." ↔ "Click on the search icon.". Vùng giữa 0<J<1 = 391/2901 = 13.5% cặp bước thật → vùng bộ bơm-lỗi không bao giờ chạm.

ĐỐI CHIẾU REPORT: report/84 "Hoài nghi còn lại" §1 ĐÃ khai chiều kết-oan paraphrase-đồng-nghĩa + §3 đã khai perturbation tự dựng có phần circular → 3/9 ca của đòn là đã-biết-đã-khai, không phải phát hiện mới. Nhưng grep report/85 không có mục nào về khớp-oan/false-positive của matcher → chiều KHỚP OAN chưa từng được ghi nhận. harness/metric_v1_results.json xác nhận separation_auc=1.0, target_error_mean=0.0118, paraphrase_mean=1.0 — đúng dạng "hai cực" chứ không phải tách được vùng giữa.

BÁC ĐƯỢC MỘT PHẦN: chỉ 5/1027 = 0.5% bước gold thật chứa số 1-chữ-số → ca 'quantity 5 vs 2' là artifact ít giá trị thực tế. Tôi cũng tự loại hai chỉ số của chính mình vì thổi phồng: "61% bước có từ toggle/phủ-định" và "24% có từ hướng" đều bị 'Click on X' và 'top right corner' làm nhiễu, không dùng làm bằng chứng.

---

### B4. [NẶNG] Cross-credit: 12.4% bước gold được 'phủ' bởi một bước gold KHÁC, và ~32% bước bị xoá vẫn được tính là có

- **Trục:** THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, metric_v1_results.json, mde_pilot.py, report/84, report/85)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NẶNG

**Vấn đề.** coverage() (dòng 76-82) là bài toán phủ-tập không ràng buộc 1-1: một bước model có thể được ghi công cho nhiều bước gold. Trên dữ liệu THẬT, 127/1027 (12.4%) bước gold được phủ bởi một bước gold khác có VĂN BẢN KHÁC HẲN trong cùng episode; nếu tính cả các bước gold trùng lặp nguyên văn (AndroidControl có thật, vd 'Click on Hand Tools' lặp 2 lần liền nhau), tỉ lệ thu hồi lên ~32% — suy ra từ Δ(missing)=0.150 so với trần 0.221. Nghĩa là gần một phần ba số bước có thể bị model bỏ sót mà thước vẫn cho điểm. Đây là lý do thật sự khiến detection ở mức coverage chỉ đạt ~68%, và nó sẽ thổi phồng coverage của mọi arm trong so sánh Student vs Teacher.

**Bằng chứng.** probe3 trên ac_test_200ep.json: CROSS-CREDIT 127/1027 (12.4%), ví dụ 'Click on Tools' được tính là phủ 'Click on Hand Tools', 'Tap on the cross icon to clear the search bar' được tính là phủ 'Tap on the search bar at the top of the screen'. metric_v1_results.json missing=0.8503649 (Δ=0.150) so với E[1/L]=0.221.

**Đề xuất sửa.** Đổi phủ-tập thành gióng 1-1 tối ưu (Hungarian trên ma trận target_score, ràng buộc mỗi model-step dùng một lần). Khử trùng lặp gold trước khi chấm hoặc gộp bước gold trùng thành một. Báo lại toàn bộ bảng report/84 sau khi sửa.

**Người phản-bác nói gì.** **Đòn ĐỨNG. Tôi cố bác và thất bại — mọi con số họ nêu tôi tái lập được độc lập, một số còn nặng hơn họ mô tả.**

Ba hướng bác tôi đã thử và kết quả:

**(1) "Tác giả đã xử lý rồi"? — KHÔNG cứu được.** `report/85` dòng 34 có ghi rõ *"Gióng model↔gold bằng phủ-tập (tồn tại model-step khớp gold-step; không ép 1-1)"*. Nhưng đây là **khai báo lựa chọn thiết kế, không phải xử lý**: khai rằng ước lượng của mình có thiên lệch thì nó vẫn thiên lệch. Tệ hơn, không chỗ nào trong report/84 hay 85 định lượng hệ quả, còn report/84 dòng 16 thì diễn giải sai chính con số hụt đó thành dấu ✓.

**(2) "Bằng chứng của họ không tồn tại / nói sai file"? — KHÔNG.** Ví dụ trích đúng verbatim, `missing=0.8503649` đúng trong `metric_v1_results.json`, `E[1/L]=0.221` đúng khi tính lại. Không có chỗ nào họ bịa.

**(3) "Thiên lệch triệt tiêu trong hiệu-số cặp"? — Đây là chỗ DUY NHẤT họ nói quá, nhưng không đủ hạ đòn.** Estimand headline (report/85) là Δ(Student − Teacher) trên CÙNG lát AC. Một trần bị thổi chung sẽ **nén cả hai nhánh về phía trần → hiệu-số bị teo (attenuation), tức bảo thủ** cho tiêu chí PASS "CI hoàn toàn trên 0". Nên câu *"thổi phồng coverage của mọi arm trong so sánh"* là mô tả sai cơ chế hại. **Nhưng điều đó không cứu được thiết kế, vì hai lẽ:** (a) rò rỉ cross-credit **không phải hằng số** — nó tỉ lệ với độ chung-chung của văn bản model sinh, mà Teacher (gpt-4o-mini zero-shot, dài dòng) và Student (train trên gold AC, ngắn gọn) chắc chắn khác nhau ở đúng chiều đó → thiên lệch **vi sai, dấu chưa biết**, không phải nhiễu chung triệt tiêu; (b) `report/86` đã chốt MDE ≈ 8-9pp — teo hiệu-số ~1/3 recall hoàn toàn đủ đẩy một hiệu ứng thật xuống dưới MDE, tức làm hỏng cả kết cục PASS lẫn kết cục NULL.

**Vì sao vẫn là `nang` chứ không lên `chi_mang`:** đây là lỗi ước-lượng **sửa được rẻ và sửa TRƯỚC KHI train** — thay `coverage()` bằng cặp-ghép nhị phân cực đại rồi chạy lại bơm-lỗi (~10 dòng, free, không cần API). Xương sống thiết kế (tách action/target, đo trên AC app-unseen, hiệu-cặp) không sụp. Nhưng **các con số cổng trong report/84 và ngưỡng đã đóng băng trong report/85 phải coi là VÔ HIỆU cho tới khi chạy lại**, và phải sửa dòng 16 report/84 + đo lại detection ở đúng mức coverage. Riêng phần 29.6% trùng-nguyên-văn cần quyết định rõ ràng và đăng-ký-trước: với output là hướng-dẫn-cho-NGƯỜI, lặp y hệt một câu hai lần có tính là thiếu bước hay không — đó là câu hỏi construct, không phải câu hỏi code.

**Bằng chứng của người kiểm.** **Tôi tự chạy lại, KHÔNG dùng số của họ** (`scratchpad/probe_fast.py`, `probe_fix.py`, Jaccard-only nên là CẬN DƯỚI — bge-m3 backstop chỉ làm tăng thêm):

1. **Cross-credit có thật, còn CAO HƠN họ nói.** 392/1027 = **38.2%** bước gold được phủ bởi một bước gold KHÁC trong cùng episode. Tách ra: trùng nguyên văn 304 (29.6%), **khác văn bản 88 (8.6%)** (họ nói 12.4% — chênh vì họ tính cả bge backstop; cùng bậc, số của tôi là cận dưới).

2. **Ví dụ họ trích CÓ THẬT, verbatim trong dữ liệu**, và đúng là bệnh nặng chứ không phải nhiễu vô hại:
   - `'Tap on the search bar at the top of the screen'` ⟵ được phủ bởi `'Tap on the cross icon to clear the search bar'` (hai thao tác khác hẳn nhau)
   - `'Click on the search icon at the bottom.'` ⟵ `'Click on the search box at the top.'`
   - `'Click on the steps drop down box'` ⟵ `'Click on the heart points drop down box'` — **đây đúng là ca K1 chết mà report/84 tuyên bố đã giải được**

3. **E[1/L] = 0.2209** — khớp chính xác con số 0.221 của họ (185 ep, L̄=5.55).

4. **Suy luận ~32% của họ đúng.** `metric_v1_results.json` missing=0.85036 → Δ=0.1496; trần không-rò-rỉ = 0.2209 → rò rỉ = **32.3%**. Tôi kiểm lại bằng thực nghiệm độc lập (`probe_fix.py`): phủ-tập Δ=0.1728 vs ép-1-1 greedy Δ=0.2508 → **rò rỉ 35.3%**.

5. **Điểm làm đòn NẶNG THÊM (họ chưa nêu):** cổng "detection ≥0.90" trong `report/85` được báo là 1.000, nhưng code dòng `det_te = sum(1 for s in te_scores if s < J_MATCH)` đo trên **target-score từng bước**, KHÔNG đi qua `coverage()`. Tức cổng đăng-ký-trước **không hề kiểm hàm tổng-hợp mà headline dùng**. Ở mức coverage, detection thật ≈ 0.68.

6. **`report/84` dòng 16 đọc NHẦM chính con số này**: ghi `target_error 0.847 −0.153 ✓ (1 bước/~5 sai → tụt ~1/5)` — nhưng 1/5 = 0.20, thực đo 0.153. Tác giả coi khoảng hụt 32% là **bằng chứng xác nhận**. Cổng cho phép đi tới bước train đã qua một phần nhờ chỗ hụt này không ai để ý.

**Chỗ tôi bác được (duy nhất):** greedy 1-1 của tôi vọt quá trần (0.2508 > 0.2209) do first-fit gán sai khi có bước trùng — fix đúng phải là **cặp-ghép nhị phân cực đại (Hungarian)**, không phải greedy. Đây là ghi chú cách sửa, không cứu được đòn.

---

### B5. [NẶNG] CONSTRUCT VALIDITY: thước thưởng cho việc chép lại câu chú thích cộc lốc và PHẠT hướng dẫn hữu ích hơn cho người

- **Trục:** THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, metric_v1_results.json, mde_pilot.py, report/84, report/85)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NẶNG

**Vấn đề.** Đề tài tuyên bố sinh hướng dẫn CHO NGƯỜI ĐỌC, nhưng thước chấm là 'trùng token với câu chú thích của crowdworker AndroidControl'. Tôi đo trực tiếp trên gold 'Click on filter option': bản chép cộc lốc 'Tap the Filter button' → score 1.000, KHỚP; bản hữu ích hơn cho người 'Tap the funnel-shaped Filter icon at the top right of the screen' → 0.333, KHÔNG KHỚP; bản có ngữ cảnh 'Tap Filter to narrow the list, then choose a category' → 0.250, KHÔNG KHỚP. Thêm chi tiết chỉ chỗ và hình dạng làm MẪU SỐ Jaccard phình ra nên bị trừ điểm. Trớ trêu là report/76 (VIỆC 1) kết luận điểm yếu của model chính là KHÔNG chỉ vị trí/hình dạng — nghĩa là trục ĐÚNG đang đẩy model đi ngược hướng chất lượng mà luận văn muốn. Thước KHÔNG đo: rõ ràng, đủ ngữ cảnh, thứ tự (đo được là 0), không thừa (đo được là 0), cảnh báo. Chính gold cũng nhiễu: có bước trùng lặp nguyên văn, có câu vô nghĩa như 'Click on the top at the bottom right corner'. Việc HOÃN nghiên-cứu-nhỏ construct-validity với người nghĩa là hiện KHÔNG có một bằng chứng nào nối thước với phán xét của người — trong khi PASS/NULL của luận văn đã được đăng-ký-trước trên chính thước đó.

**Bằng chứng.** probe4 chạy trên step_match: 1.000 / 0.333 / 0.250 như trên. Gold nhiễu: ac_test_200ep.json episode đầu có 'Go back to the previous page ' và 'Click on Hand Tools' lặp, và 'Click on the top at the bottom right corner'. report/85:75-77 (PASS/NULL neo trên coverage-đúng). report/76 (fallback thiếu chỉ-chỗ).

**Đề xuất sửa.** Đảo thứ tự ưu tiên: làm nghiên-cứu-nhỏ construct-validity TRƯỚC khi train, không sau. Không cần model đã train — chấm 60-100 cặp (gold AC vs output teacher đã có sẵn trong harness/dg1_cache/mde_pilot/gen.json, 91 câu, MIỄN PHÍ) bằng 2 người chấm 'hướng dẫn này giúp bạn bấm đúng nút không', rồi báo tương quan với điểm (action,target) + κ người-người. Nếu tương quan thấp, phải sửa thước (vd chấm theo 'model có nêu đúng đích không', bỏ phạt phần mô tả thêm) trước khi tiêu tiền GPU.

**Người phản-bác nói gì.** Tôi vào với ý định bác, và bác được BA điểm phụ — nhưng lõi thì không những sống mà còn NẶNG HƠN họ tưởng.

BÁC ĐƯỢC:
(1) "Phạt chi tiết chỉ VỊ TRÍ" — SAI HẲN. `target_of()` có regex xoá cụm vị trí đuôi, cộng STOP list chứa top/bottom/left/right/corner/screen/button/icon/option. Tôi đo: "Tap the Filter button at the top right of the screen" = 1.000 KHỚP; "in the bottom left corner" = 1.000 KHỚP. Thước BẤT BIẾN với vị trí, và đó là thiết kế có chủ đích. Vì report/76 than model thiếu "chỉ vị trí/hình", nửa cái mỉa mai của họ sụp: vị trí được MIỄN PHÍ, chỉ hình dạng ("funnel-shaped") mới bị trừ.
(2) "Thước không đo thứ tự (đo được 0)" — đọc nhầm. reorder=1.000 là ĐÚNG THIẾT KẾ, ghi rõ report/84:20 và report/85:51; thứ tự đo bằng order-τ partial (Fagin) TÁCH RIÊNG, đã pre-register.
(3) "Không đo bước thừa (đo được 0)" — extra=1.000 vì coverage là RECALL. Headline pre-register (report/85:35) = coverage + **F1 (chống nhồi bước thừa)** + order-τ. Họ đo một trong ba thành phần rồi quy điểm mù của nó thành điểm mù của cả thước.

KHÔNG BÁC ĐƯỢC (và tôi tự đào ra thứ tệ hơn):
(a) Ba con số 1.000/0.333/0.250 tái lập CHÍNH XÁC, kể cả sau khi backstop bge-m3 đã có cơ hội chạy và không cứu nổi. Jaccard đối xứng ⇒ mẫu số phình ⇒ chi tiết hình dạng và diễn giải gộp-bước bị trừ thật.
(b) ĐÒN CHÍ TỬ mà chính họ bỏ lỡ: cổng validate ở report/84 dựng nhánh paraphrase bằng `f"{v} on the {tgt}"` với `tgt = target_of(g[i])` — tức paraphrase GIỮ NGUYÊN 100% token nội dung của gold. paraphrase_mean = 0.99999999986, AUC=1.000 là HỆ QUẢ TOÁN HỌC của cách dựng, không phải bằng chứng. Cổng chưa từng thử một biến-thể-từ-vựng nào. Nghĩa là cổng CẤU TRÚC KHÔNG THỂ bắt được đúng lỗi này — lập luận construct-validity của họ mạnh hơn họ trình bày.
(c) Gold nhiễu tái lập nguyên văn ở episode 0.
(d) report/85:97 tự thú construct-validity NGƯỜI còn treo, trong khi PASS/NULL (85:75) đã neo lên thước.

VÌ SAO GIỮ "NẶNG" chứ không hạ: confound này chạy CÙNG CHIỀU với giả thuyết. Student train trên gold cộc lốc sẽ học văn phong cộc lốc; Teacher-BASE zero-shot thì dài dòng. Thước có thể sinh ra Δ dương từ VĂN PHONG thuần tuý. report/86 đã gọi chiều dương kỳ vọng là "lợi-thế-sân-nhà" và coi đó là hiệu ứng, chứ không phải hiện vật đo lường. Rủi ro #4 ở report/85 có nêu circularity nhưng thuốc giải là "mốc Teacher-BASE" — chính cái bị confound làm bẩn. Nên đây không phải lỗ đã xử.

Đề nghị vá (rẻ, free): đổi target-score sang bao-hàm bất-đối-xứng |s_model ∩ s_gold| / |s_gold| cho trục recall (giữ Jaccard cho F1), và dựng lại nhánh paraphrase bằng biến-thể-từ-vựng THẬT trước khi coi cổng là đã qua.

**Bằng chứng của người kiểm.** Tái lập (~/.venvs/thesis/bin/python + ollama bge-m3, không gọi API):
- harness/metric_v1_validate.py:70-84 — target_score dùng Jaccard đối xứng trên token nội dung, backstop bge chỉ khi ≥0.85.
- Probe gold "Click on filter option" (target rút gọn = 'filter'): "Tap the Filter button" score=1.000 match=True; "Tap the funnel-shaped Filter icon at the top right of the screen" toks=[filter,funnel,shaped] score=0.333 match=False; "Tap Filter to narrow the list, then choose a category" score=0.250 match=False. ĐÚNG như họ khai.
- Probe bác vị trí: "…Filter button at the top right of the screen"=1.000 True; "…in the bottom left corner"=1.000 True; "…at the top of the page"=1.000 True. Do target_of() regex + STOP (harness/metric_v1_validate.py:39-47).
- harness/metric_v1_validate.py:124-128 — nhánh perturb "paraphrase" dựng từ chính target_of() ⇒ token nội dung trùng khít. harness/metric_v1_results.json: paraphrase_mean=0.9999999998594595, separation_auc=1.0, fp_paraphrase=0.0 → cổng vacuous.
- harness/metric_v1_results.json: reorder=1.0, extra=1.0 (coverage là recall) — nhưng report/85:35 pre-register headline gồm F1 + order-τ; report/84:20 ghi rõ reorder-không-đổi là chủ ý.
- dataset_samples/androidcontrol_test/ac_test_200ep.json ep[0]: "Click on Hand Tools" và "Click on Wrenches & Spanners " lặp 2 lần, có "Click on the top at the bottom right corner" — nhiễu gold ĐÚNG.
- report/85_PREREG_v2_LAI.md:97 tự khai construct-validity NGƯỜI còn chờ output model; report/84:46 tự khai perturbation "có phần circular".

---

### B6. [NẶNG] Cổng validate thước (report/84, AUC=1.000) là tautology theo cấu tạo, và 'vòng 2 ca khó' không tái lập được

- **Trục:** DỮ LIỆU, SPLIT, RÒ RỈ — và câu hỏi "vừa học vừa chấm cùng loại"
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** CHÍ MẠNG → **sau kiểm chéo:** NẶNG

**Vấn đề.** AUC=1.000 được dùng làm CỔNG cho phép đi train. Nhưng hai phân phối được đem so đều do chính thước tự sinh ra: 'paraphrase' được dựng bằng f"{v} on the {tgt}" với tgt = target_of(gold) → tập từ-nội-dung y hệt gold theo định nghĩa; 'target_error' được ép chọn target có GIAO RỖNG với gold. Nghĩa là pos≡1.0, neg≡0.0 trước khi thước chạy. Cổng không kiểm được điều nó tuyên bố kiểm (paraphrase-thật của model sẽ đổi từ, đúng chỗ K1 chết). Ngoài ra 'vòng 2 ca khó' (target-score 0.350, AUC 1.0, bge cứu nhầm 5%) không có trong code đã commit và không có trường nào trong file kết quả.

**Bằng chứng.** harness/metric_v1_validate.py:118-124 (paraphrase) và 100-110 (target_error, điều kiện `not (set(content_tokens(alt)) & cur)`). Tôi chạy lại đúng bộ perturbation, seed 20260719: paraphrase có Jaccard đúng bằng 1.0 ở 85,9% ca; target_error có Jaccard đúng bằng 0.0 ở 96,2% ca (max chỉ 0.250). harness/metric_v1_results.json: paraphrase_mean=0.9999999998594595, target_error_mean=0.0118. Không có mục nào cho vòng 2; grep trong metric_v1_validate.py không có nhánh 'ca khó'.

**Đề xuất sửa.** Hạ 'CỔNG QUA' xuống 'chưa kiểm'. Dựng paraphrase ĐỘC LẬP với thước: lấy 100-150 gold step, viết lại bằng người (hoặc bằng model KHÁC họ, không dùng target_of) sao cho đổi từ chỉ nút ('tab'→'section', 'three lines'→'menu icon'), rồi mới đo AUC. Commit code + file kết quả cho vòng 2 trước khi trích số 0.350.

**Người phản-bác nói gì.** Tôi cố bác nhưng không bác được — đòn đúng về cơ chế, và bằng chứng họ nêu là thật (nếu có sai thì sai theo hướng NHẸ ĐI so với thực tế).

(1) Tautology: xác nhận bằng chạy lại. `perturb(...,"paraphrase")` dựng `f"{v} on the {tgt}"` với `tgt = target_of(g[i])`; mọi verb trong map (Click/Enter/Swipe/Open/Go to/Long-press) tokenize ra toàn từ nằm trong ACTION_MAP hoặc STOP, và `target_of` idempotent → tập từ-nội-dung của paraphrase ĐỒNG NHẤT với gold theo định nghĩa. Đối xứng, sampler `target_error` ép `not (set(content_tokens(alt)) & cur)` → giao rỗng theo fiat. pos≡1.0, neg≡0.0 TRƯỚC khi thước chạy. AUC=1.000 là hệ quả của bộ sinh nhiễu, không phải của thước.

(2) Điểm nặng hơn đòn gốc nêu: "tab" KHÔNG nằm trong STOP → cặp kiểu "artworks tab" vs "energy tab" (đúng ca K1 chết mà report/84 tuyên bố đã phủ) có giao khác rỗng nên bị sampler LOẠI BỎ theo cấu tạo. Round 1 không chỉ thiếu ca khó — nó loại trừ ca khó. Draw thật: 'Click on the share icon' → 'Click we cant help everyone but everyone can help someone center'.

(3) "Vòng 2 ca khó" không tồn tại: không có nhánh hard/ca-khó trong metric_v1_validate.py (chỉ 1 commit b5a6b29), không có field nào trong metric_v1_results.json, không có file scratch. Con số 0.350 / AUC 1.0 / 3-of-60 (n=60) không tái lập được từ repo, NHƯNG đã lan vào report/85:50 ("1.000 (cả ca khó) ✓") và vào CLAUDE.md như dữ kiện.

(4) Hệ quả structural — chỗ này mới thực sự đau: report/85 đã COMMIT ngưỡng "AUC ≥ 0.80" làm cổng cứng và dặn chạy lại trên config cuối. Nếu bộ sinh nhiễu giữ nguyên, lần chạy lại sẽ lại ra 1.000. Một cổng không thể rớt thì không phải cổng. Câu trong CLAUDE.md "đo bằng số không assume" là sai đúng nghĩa đen: chính chỗ đó đang assume.

VÌ SAO HẠ TỪ chi_mang XUỐNG nang (3 lý do, không phải bao che):
- report/84 §"Hoài nghi còn lại" #1 nói thẳng "tôi giữ nguyên từ-lõi → Jaccard=1 tất yếu" và #3 nói "Perturbation do chính tôi dựng → có phần circular". Tautology được TỰ KHAI ở tài liệu nguồn, không giấu. Lỗi thật nằm ở dòng phán-quyết headline + việc lan xuống report/85/CLAUDE.md, tức lỗi TRÌNH BÀY/OVERCLAIM chồng lên lỗi thiết-kế-test, không phải bịa số có chủ ý.
- Chưa mất gì: chưa train, chưa tốn API, chưa in. Sửa rẻ (bộ sinh paraphrase dùng từ-điển đồng-nghĩa loại-nút tab→section/button→control + cho phép target_error CHIA SẺ từ-loại, chỉ khác entity). Cỡ 1 giờ, free.
- Thước (tách action,target) KHÔNG bị bác — nó chỉ CHƯA ĐƯỢC VALIDATE. Lý lẽ từ K1 rằng tách action/target giúp vẫn còn nguyên giá trị tiên nghiệm; đòn này giết bằng-chứng, không giết thiết kế.

Việc phải làm trước khi train: (a) viết lại perturb cho paraphrase đổi từ-nội-dung thật + target_error chung từ-loại khác entity, chạy lại, chấp nhận AUC có thể tụt dưới 0.80; (b) sửa report/85:50 và CLAUDE.md — gỡ cụm "cả ca khó" cho tới khi có code tái lập được; (c) nếu giữ số vòng 2 thì phải commit code sinh ra nó.

**Bằng chứng của người kiểm.** CHẠY LẠI (~/.venvs/thesis/bin/python, seed 20260719, 185 ep):
- paraphrase Jaccard == 1.0 ở 994/1027 bước = 96.8% (33 ca còn lại là target rỗng, sentinel -1, KHÔNG phải phản-ví-dụ). Đòn gốc ghi 85.9% → họ NÓI NHẸ hơn thực tế.
- target_error Jaccard == 0.0 ở 178/185 = 96.2% (khớp chính xác con số họ nêu), max = 0.25.
- 'tab' in STOP → False ⇒ cặp chung từ-loại ("... tab" vs "... tab") bị điều kiện `not (set(content_tokens(alt)) & cur)` LOẠI, tức ca K1-khó bị exclude by construction.
- Ví dụ target_error thật: 'Click on the share icon' → 'Click we cant help everyone but everyone can help someone center'; 'Click on Tools' → 'Click first aid techniques'.

CODE (harness/metric_v1_validate.py, đọc toàn file 9251 bytes):
- dòng ~118-124 paraphrase: g[i] = f"{v} on the {tgt}" với tgt = target_of(g[i]); verb map = Click/Enter/Swipe/Open/Go to/Long-press → tokenize ra long/press/go/to/on/the đều thuộc ACTION_MAP hoặc STOP.
- dòng ~100-110 target_error: điều kiện `if set(content_tokens(alt)) and not (set(content_tokens(alt)) & cur)`.
- target_of() idempotent (regex chỉ strip cụm vị trí đuôi; 'on'/'the' đằng nào cũng là STOP).
- grep 'khó|hard|round2|vòng 2|0.350' trong file → KHÔNG khớp dòng nào.

DỮ LIỆU: harness/metric_v1_results.json (untracked, 377 bytes) có đúng 12 khoá: n_ep=185, coverage_by_kind (7 loại), separation_auc=1.0, paraphrase_mean=0.9999999998594595, target_error_mean=0.01177, detection_target=1.0, fp_paraphrase=0.0. KHÔNG có bất kỳ khoá nào cho vòng 2.

GIT: `git log --all -- harness/metric_v1_validate.py` → duy nhất b5a6b29. Không có bản nào khác chứa nhánh ca-khó.

TÀI LIỆU:
- report/84 §"Hoài nghi còn lại" #1: "tôi giữ nguyên từ-lõi (chỉ đảo trật tự + thêm article) → Jaccard=1 tất yếu"; #3: "Perturbation do chính tôi dựng → có phần circular. Đã giảm bằng vòng-2 ca-khó" (← viện dẫn vòng 2 không tồn tại để tự trấn an chính điểm circular này).
- report/84 §Số liệu "Vòng 2": target-score TB 0.350, AUC 1.000, bge cứu-nhầm 3/60 = 5% → không tái lập được.
- report/85:47-53 đã COMMIT: "detection sai-target ≥0.90 | 1.000 ✓"; "tách-phân-phối ... AUC ≥ 0.80 | 1.000 (cả ca khó) ✓"; "Cổng cứng: rớt AUC≥0.80 trên config cuối → DỪNG, KHÔNG train".
- CLAUDE.md §0 mục (3): "AUC(paraphrase>sai-target)=1.000 cả ca DỄ lẫn ca KHÓ ... đo bằng số không assume".

---

### B7. [NẶNG] AUC=1.000 là hằng đẳng thức của thiết kế bơm-lỗi, không phải phép đo — và cổng "FP paraphrase = 0.000" đã được đăng-ký-trước như ĐẬU

- **Trục:** TRUNG THỰC BÁO CÁO — đối chiếu prose (report/73-86, 88, CLAUDE.md §0) với code + số thô trong harness/
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** CHÍ MẠNG → **sau kiểm chéo:** NẶNG

**Vấn đề.** Cổng validate thước (report/84, đưa vào pre-registration report/85) tuyên bố "tách sạch sai-đích khỏi paraphrase, AUC=1.000, false-positive paraphrase=0.000". Nhưng đọc code thì hai nhánh bơm-lỗi được dựng sao cho kết quả là tất yếu: nhánh `paraphrase` GỌI CHÍNH `target_of()` — thứ đang được kiểm — rồi dán lại nguyên văn output của nó, nên Jaccard=1.0 luôn; nhánh `target_error` lại BẮT BUỘC target thay thế phải có 0 token chung với gold, nên Jaccard=0.0 luôn. AUC=1.0 là hệ quả toán học của cách dựng, không phải bằng chứng thước tốt. Nguy hiểm hơn: con số FP=0.000 đó là con số duy nhất bảo chứng thước không kết-oan, và nó vô nghĩa. Tôi đo lại bằng paraphrase THẬT ở mức target (đúng thứ model sẽ sinh) thì tỉ lệ kết-oan là 5/8 = 62%. Backstop bge-m3 (TAU=0.85) không cứu ca nào. Hệ quả thực chất: headline coverage thưởng cho việc TRÙNG TỪ với gold. Student được train chính trên gold step_instructions nên sẽ bắt chước từ ngữ gold; Teacher-BASE zero-shot thì không. Vậy kết quả "Student > Teacher" mà report/86 gọi là "lợi-thế-sân-nhà hợp lý" có thể phần lớn là hiệu ứng bắt-chước-văn-phong, không phải năng lực. Đây là confound đánh thẳng vào trụ đóng góp MODEL.

**Bằng chứng.** harness/metric_v1_validate.py:115-119 (paraphrase: `tgt = target_of(g[i])`; `g[i] = f"{v} on the {tgt}"`) vs :92-101 (target_error: điều kiện `not (set(content_tokens(alt)) & cur)`). Tôi chạy lại: paraphrase giữ NGUYÊN target_of() 400/400 = 100.0% ca. metric_v1_results.json: "paraphrase_mean": 0.9999999998594595, "target_error_mean": 0.0118, "fp_paraphrase": 0.0. Probe của tôi trên paraphrase target thật: 'Tap the Home tab' vs 'Tap the main screen tab' score=0.333; 'Sign in button' vs 'Log in button' 0.000; 'hamburger menu' vs 'navigation drawer' 0.000; 'Tap Settings' vs 'Tap the gear icon' 0.000; 'profile picture' vs 'avatar' 0.000 → 5/8 = 62% kết oan. report/85_PREREG_v2_LAI.md:49 ghi "false-positive paraphrase | ≤0.10 | 0.000 ✓"; :53 "Synthetic đã qua".

**Đề xuất sửa.** Trước khi train: (1) viết lại nhánh paraphrase để nó KHÔNG gọi target_of() — dùng bộ paraphrase target gán tay (đổi từ đồng nghĩa danh từ đích, đổi loại-nút tab/section, bỏ/thêm bổ ngữ) rồi đo lại FP; (2) nới target_error để cho phép giao token (ca 'artworks tab' vs 'energy tab'), vì hiện tại nó bị luật :97 loại thẳng; (3) chạy lại cổng và ghi số THẬT vào report/85 — nếu FP thật >0.10 thì theo đúng cam kết của chính report/85 là DỪNG, sửa thước; (4) bắt buộc thêm một arm chống confound văn-phong: chấm Teacher-BASE có few-shot gold-style, hoặc báo thêm thước không nhạy từ vựng (LLM-judge khác họ) song song headline.

**Người phản-bác nói gì.** TÔI ĐÃ CỐ BÁC VÀ BÁC ĐƯỢC MỘT NỬA, NHƯNG PHẦN CÒN LẠI SỐNG.

**Phần đòn ĐÚNG (không bác được):** đọc code xác nhận đúng. Nhánh `paraphrase` (:115-119) lấy `tgt = target_of(g[i])` rồi ráp `f"{v} on the {tgt}"`; vì "on"/"the" nằm trong STOP và verb nằm trong ACTION_MAP, `target_of()` áp lần hai trả về đúng `tgt` → Jaccard = 1.0 theo định nghĩa. Nhánh `target_error` (:97) ép `not (set(content_tokens(alt)) & cur)` → giao rỗng → Jaccard = 0. AUC = 1.000 quả thật là hệ quả của cách dựng. Tôi chạy lại probe của họ và tái hiện được: 'Sign in'/'Log in' = 0.000, 'hamburger menu'/'navigation drawer' = 0.000, 'Tap Settings'/'gear icon' = 0.000, 'profile picture'/'avatar' = 0.000, 'Home tab'/'main screen tab' = 0.333 — bge-m3 @0.85 không nâng ca nào. Đúng như họ nói.

**Nhưng đây KHÔNG phải phát hiện bị giấu — tác giả đã tự khai NGUYÊN VĂN.** report/84 §"Hoài nghi còn lại" mục 1 viết đúng chữ: *"Paraphrase test còn dễ: tôi giữ nguyên từ-lõi (chỉ đảo trật tự + thêm article) → **Jaccard=1 tất yếu**. Nếu model THẬT dùng từ đồng nghĩa cho loại nút ('tab'→'section', 'button'→'control') thì Jaccard tụt → có thể **kết-oan** (false-positive)."* Mục 3 viết thêm: *"Perturbation do chính tôi dựng → có phần circular."* Toàn bộ luận điểm kỹ thuật của đòn — kể cả từ "tất yếu" và cả kịch bản kết-oan-synonym — đã nằm sẵn trong chính file mà giám khảo trích. Một khiếm khuyết được ghi rõ trong tài liệu nguồn không thể xếp `chi_mang` ("giấu lỗ hổng chí tử"); nó là **giới hạn đã khai, chưa được mang lên bảng tóm tắt**.

**Trích dẫn của họ có cắt xén.** Họ dẫn report/85:53 là "Synthetic đã qua" rồi dừng. Câu đầy đủ là: *"(Synthetic đã qua; **chạy lại trên parser cuối + validate bộ-trích P/R trên tập gán-tay khi có output model**.)"* — tức bản đăng-ký-trước KHÔNG chốt cổng là đã đậu vĩnh viễn, mà buộc chạy lại + validate bằng nhãn người trước khi dùng. Cắt vế sau làm sai lệch đáng kể sức nặng của đòn.

**Con số "62% kết-oan" là bịa cỡ hiệu ứng, không phải phép đo.** 8 cặp do chính giám khảo tự nghĩ ra, không lấy mẫu từ phân phối nào. Tệ hơn, ít nhất 3/5 ca "kết-oan" của họ (Settings↔gear icon, Add button↔+, profile picture↔avatar) không phải paraphrase cùng-đích mà là **gọi-tên-nhãn vs mô-tả-hình-icon** — đúng cái mà report/85 §3 đã pre-register là phải **báo tách nhóm target-CHỮ vs target-ICON** (vì report/79 đo ~48% click AC là icon). Nên "62%" không thể dùng làm ước lượng tỉ lệ FP thật.

**PHẦN SỐNG, và là phần đáng giá nhất của đòn (tác giả CHƯA nêu ở đâu):**
(a) **Lỗi tài liệu ở văn bản ràng buộc.** report/85 dòng 44-51 bê "FP paraphrase 0.000 ✓" và "AUC 1.000 (cả ca khó) ✓" vào bảng ngưỡng đóng băng mà **rụng mất caveat "Jaccard=1 tất yếu"**. Người đọc bản đăng-ký-trước — đúng thứ hội đồng sẽ đọc — nhận một bảo chứng mạnh hơn bằng chứng thực có. Chưa kể "cả ca khó" ở vòng 2 chỉ làm khó nhánh target_error, **nhánh paraphrase vẫn nguyên cơ chế tự-gọi-target_of()**, nên chữ "cả ca khó" không hề gia cố phía FP như bảng ngụ ý.
(b) **Confound trùng-từ-với-gold trên Δ(Student − Teacher-BASE).** Đây là đóng góp thật của đòn và tôi không bác được về nguyên tắc: theo report/81 tín hiệu train CHÍNH là gold `step_instructions` của AndroidControl, còn `harness/mde_pilot.py:15,99` chấm Teacher bằng chính `target_score` này. Một thước thưởng trùng-từ-nội-dung, đem so model fine-tune-trên-gold với model zero-shot, thì Δ dương có đường bị nhiễm bởi bắt-chước-từ-vựng. Đánh trúng trụ đóng góp MODEL.
   *Giảm nhẹ (có thật nhưng chưa đủ):* thứ được "bắt chước" phần lớn là **nhãn hiển thị trên màn**, không phải văn phong tuỳ ý — gọi đúng nhãn nút chính là nội dung tác vụ, nên không phải toàn bộ Δ là artifact. report/85 cũng đã pre-register 3 lá chắn liên quan: báo action/target RIÊNG, tách CHỮ vs ICON, và LLM-judge khác-họ cross-check. Nhưng judge được ghi rõ "KHÔNG vào headline" → headline vẫn phơi confound.

**Vì sao `nang` chứ không `chi_mang`:** không có lỗi thiết kế phải làm lại, không tốn tiền/GPU nào đã đổ theo con số hỏng, và cổng chưa bị dùng để mở khoá train (chưa train). Việc phải sửa là: (1) sửa 2 ô bảng report/85 thành "chưa kết luận — synthetic tautological", (2) dựng lại nhánh paraphrase KHÔNG gọi `target_of()` (dùng từ-điển đồng-nghĩa-loại-nút + paraphrase người viết) rồi chạy lại cổng FP/AUC, (3) thêm vào pre-reg một readout chống-confound (vd đo overlap-từ-vựng-với-gold như covariate, hoặc arm Teacher-few-shot-mồi-bằng-gold-style để tách phong-cách khỏi năng-lực). Đều là việc free/rẻ, làm trước khi train.

**Vì sao không `vua`:** vì (a) và (b) đều nằm trong văn bản đăng-ký-trước và đều đánh vào con số headline của trụ MODEL; nếu để nguyên mà đi tiếp thì Δ dương sẽ không phòng thủ được trước hội đồng.

**Bằng chứng của người kiểm.** ĐÃ ĐỌC/CHẠY:

1. /mnt/d/Master/Thesis/harness/metric_v1_validate.py — xác nhận :115-119 (paraphrase gọi `tgt = target_of(g[i])` rồi `g[i] = f"{v} on the {tgt}"`) và :92-101 (target_error ép `not (set(content_tokens(alt)) & cur)`). Cộng STOP (:28-29, chứa "on","the","in") + `content_tokens` lọc ACTION_MAP (:39) → `target_of` idempotent trên chuỗi vừa dựng ⇒ Jaccard=1.0 by construction. Đòn mô tả code CHÍNH XÁC.

2. Chạy lại probe bằng ~/.venvs/thesis/bin/python, import trực tiếp target_score/step_match — TÁI HIỆN ĐƯỢC:
   'Tap the Home tab' vs 'Tap the main screen tab' = 0.333 (match=False)
   'Sign in button' vs 'Log in button' = 0.000
   'hamburger menu' vs 'navigation drawer' = 0.000
   'Tap Settings' vs 'Tap the gear icon' = 0.000
   'profile picture' vs 'avatar' = 0.000
   'Tap the Add button' vs 'Tap +' = 0.000
   (bge-m3 @TAU=0.85 không nâng ca nào — đúng như họ nói)
   Ngược lại 'Click on the search bar' vs 'Tap the search field' = 0.500 match=True; 'Enter your email address' vs 'Type the email' = 0.500 match=True → thước KHÔNG hỏng đều, hỏng ở synonym-thay-hẳn-từ-lõi và ở nhãn-vs-icon.

3. harness/metric_v1_results.json — xác nhận nguyên văn "paraphrase_mean": 0.9999999998594595, "target_error_mean": 0.01177, "separation_auc": 1.0, "fp_paraphrase": 0.0, "detection_target": 1.0. Số họ trích đúng.

4. **report/84_metric_validate_ket_qua.md:44 (§"Hoài nghi còn lại" mục 1) — ĐÒN CHÍ MẠNG BỊ TỰ KHAI TRƯỚC:** "Paraphrase test còn dễ: tôi giữ *nguyên từ-lõi* (chỉ đảo trật tự + thêm article) → **Jaccard=1 tất yếu**. Nếu model THẬT dùng **từ đồng nghĩa cho loại nút** ("tab"→"section", "button"→"control") thì Jaccard tụt → có thể **kết-oan** (false-positive)."
   :46 mục 3: "**Perturbation do chính tôi dựng** → có phần circular (lỗi/paraphrase theo cùng logic token của thước)."
   :7 phán quyết cũng đã ghi: "Còn một điểm chỉnh sau (kết-oan với paraphrase đổi từ-đồng-nghĩa)".
   ⇒ Giám khảo trình bày như phát hiện mới bằng cách đọc code; thực tế nằm sẵn trong file, cùng ý, cùng từ "tất yếu".

5. report/85_PREREG_v2_LAI.md:44-51 — xác nhận bảng có "false-positive paraphrase | ≤0.10 | 0.000 ✓" và "AUC ≥0.80 | 1.000 (cả ca khó) ✓", KHÔNG kèm caveat. Đây là điểm đòn ghi bàn thật.
   NHƯNG :53 đầy đủ = "**Cổng cứng:** rớt AUC≥0.80 trên config cuối → DỪNG, sửa thước, KHÔNG train. (Synthetic đã qua; **chạy lại trên parser cuối + validate bộ-trích P/R trên tập gán-tay khi có output model**.)" — giám khảo chỉ trích 3 chữ "Synthetic đã qua", CẮT vế mitigation. Trích dẫn thiếu trung thực.

6. report/84:26-31 (vòng 2 "ca khó") — xác nhận vòng 2 chỉ siết nhánh đích-sai (TB 0.350), **nhánh paraphrase vẫn TB=1.000 bằng cơ chế cũ**. Nên chữ "cả ca khó" trong bảng report/85 không gia cố phía FP ⇒ nhãn ✓ đó overclaim.

7. harness/mde_pilot.py:15 `from metric_v1_validate import canon_action, target_of, target_score` và :99 `ts = target_score(target_of(out), target_of(gold))` — xác nhận con số Teacher 30% (report/86) chấm bằng CHÍNH thước này ⇒ confound trùng-từ áp được lên Δ Student−Teacher. Phần này của đòn đứng.

8. report/85:36-38 — có sẵn 3 mitigation liên quan đã pre-register: "Báo action và target RIÊNG", "Báo tách nhóm target-CHỮ vs target-ICON (~48% click AC là icon — report/79)", "LLM-judge khác-họ ... KHÔNG vào headline". ⇒ 3/5 ca "kết-oan" của giám khảo (Settings↔gear icon, Add↔+, profile picture↔avatar) rơi đúng nhóm ICON đã được pre-register tách riêng ⇒ "62%" không phải tỉ lệ FP của trục headline. Nhưng vì judge không vào headline nên confound (b) vẫn chưa bị dập.

9. Không tìm thấy chỗ nào trong report/84/85/86 nêu confound "Student bắt-chước từ-vựng gold vì train trên gold" ⇒ điểm (b) là đóng góp MỚI thật của đòn.

---

### B8. [NẶNG] Chuỗi caveat rụng dần 84 → 85 → 88: "perturbation của chính tôi, có phần circular" biến thành "✓ ĐẬU" rồi thành sự thật cứng

- **Trục:** TRUNG THỰC BÁO CÁO — đối chiếu prose (report/73-86, 88, CLAUDE.md §0) với code + số thô trong harness/
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NẶNG

**Vấn đề.** Đây là đúng kiểu lỗi cần soi. report/84 §"Hoài nghi còn lại" TỰ KHAI rất sòng phẳng hai điều: (1) "Paraphrase test còn dễ: tôi giữ nguyên từ-lõi ... Jaccard=1 tất yếu", (3) "Perturbation do chính tôi dựng → có phần circular". Nhưng ngay trong CÙNG file đó, phần Kết luận lại viết "giả định lớn nhất đã kiểm bằng số, KHÔNG assume" và "tin tốt cứng nhất từ trước tới nay" — mâu thuẫn nội bộ trong một file. Sang report/85 (bản pre-registration, thứ được commit làm dấu thời gian), caveat teo lại thành một dòng và bị QUY SAI NGUYÊN NHÂN: nó đổ cho "backstop bge-m3 có thể kết-oan", trong khi nguyên nhân thật là lõi Jaccard cộng với việc arm paraphrase tự sao chép target_of(); còn bảng cổng thì ghi thẳng "0.000 ✓" và "AUC 1.000 (cả ca khó) ✓". Đến report/88 (file tóm tắt đọc-đầu-tiên mỗi phiên) thì caveat BIẾN MẤT HOÀN TOÀN: chỉ còn "AUC = 1.000 ... cả ca dễ lẫn ca khó", "báo động giả trên paraphrase = 0.000", và bảng trạng thái "✅ QUA (AUC=1.0)". CLAUDE.md §0 cũng chốt "metric-gate PASSED" và commit message b5a6b29 ghi "metric-gate PASSED". Một điều được khai là circular ở tầng nguồn đã trở thành cổng đã-đậu ở tầng cam kết chính thức.

**Bằng chứng.** report/84_metric_validate_ket_qua.md:44 "Jaccard=1 tất yếu ... có thể kết-oan"; :46 "Perturbation do chính tôi dựng → có phần circular"; đối lại :50 "đã kiểm bằng số, không assume" và :54 "tin tốt cứng nhất từ trước tới nay". report/85:49-50 bảng cổng "0.000 ✓" / "1.000 (cả ca khó) ✓"; :84 caveat còn lại quy sai cho backstop. report/88:137-138 không còn caveat nào; :199 "✅ QUA (AUC=1.0)". git log b5a6b29 "...4 kill-test + pilot + metric-gate PASSED".

**Đề xuất sửa.** Nguyên tắc cứng: con số nào vào bảng cổng của pre-registration thì caveat của nó phải đi kèm TRONG Ô ĐÓ, không đẩy xuống mục hoài nghi ở cuối file. Sửa report/85 bảng §4: ghi "FP paraphrase = 0.000 (KHÔNG hợp lệ — arm paraphrase tái dùng target_of(), chưa đo)" và AUC "1.000 (tautological; ca khó chưa vào harness)". Sửa report/88:137-138 và CLAUDE.md §0 theo. Nếu report/85 đã commit thì ra bản vá có dấu thời gian mới, ghi rõ lý do — đừng sửa lặng.

**Người phản-bác nói gì.** ĐÒN ĐỨNG VỮNG VỀ THỰC CHẤT, dù hai chi tiết bằng chứng họ nêu là SAI. Tôi cố bác nhưng thất bại — và khi mở code thì lỗi còn nặng hơn họ mô tả.

**Chỗ họ nói SAI (phải đính chính):**
1. "report/88 caveat BIẾN MẤT HOÀN TOÀN, :137-138 không còn caveat nào" — SAI, họ cherry-pick đúng hai dòng ngay TRƯỚC caveat. report/88:140 ghi rõ: "*Hoài nghi còn giữ:* nếu mô hình thật dùng từ đồng nghĩa cho loại nút ("tab"→"section") có thể kết oan → chỉnh dự phòng bge-m3 khi có output mô hình." report/88:213 còn giữ việc #7 "Nghiên cứu nhỏ kiểm thước vs người chấm (construct-validity)".
2. "report/85 caveat teo lại một dòng" — SAI, 85 hedge MẠNH HƠN mô tả: cột bảng ghi "Kết quả **synthetic** (report/84)"; §4 tiêu đề "đã chạy synthetic report/84, **phải chạy lại trên config cuối**"; §4 có cổng cứng "rớt AUC≥0.80 trên config cuối → DỪNG, sửa thước, KHÔNG train"; §9 bước 1 buộc chạy lại trước khi commit.
3. "report/85 QUY SAI NGUYÊN NHÂN (đổ cho backstop)" — 85 chỉ chép lại đúng chẩn đoán của CHÍNH report/84 caveat #1 ("Đây là chỉnh backstop bge-m3"). Chẩn đoán đó có thể sai, nhưng đó là lỗi từ 84, không phải suy thoái 84→85.

**Chỗ họ ĐÚNG, và tôi xác nhận mạnh hơn bằng code:**
AUC=1.000 là TẤT YẾU SỐ HỌC do thiết kế bơm lỗi, không phải phát hiện về thước:
- Arm paraphrase (`metric_v1_validate.py:115-119`) dựng câu bằng `f"{v} on the {tgt}"` với `tgt = target_of(g[i])`. Thước chấm lại bằng `target_of()`, mà STOP (dòng 29) chứa "on"/"the" và `content_tokens` loại verb trong ACTION_MAP → **round-trip về đúng chính nó**. Tôi chạy thử: J=1.000 trên 8/8 mẫu đầu. Arm này không hề kiểm paraphrase — nó kiểm `target_of(x) == target_of(x)`.
- Arm target_error (dòng 96) ép chọn alt có **giao token RỖNG** (`not (set(content_tokens(alt)) & cur)`) → J=0 by construction.
- Hệ quả: paraphrase_mean=0.99999999986, target_error_mean=0.0118, fp=0.000, AUC=1.000 — đều bị ép, không đo được gì.
Đây đúng như 84 caveat #1 ("Jaccard=1 tất yếu") và #3 ("perturbation do chính tôi dựng → có phần circular") tự khai.

**Chỗ tôi tìm được NẶNG HƠN đòn gốc:** vòng-2 "ca khó" (artworks/energy tab) — arm DUY NHẤT có thể phá tautology, và là mệnh đề chịu lực trong cả 85 lẫn 88 ("cả ca khó") — **KHÔNG có code, KHÔNG có file kết quả**. `metric_v1_validate.py` chỉ có vòng 1; grep "ca khó/hard/artworks" trong harness/ ra RỖNG; `metric_v1_results.json` chỉ chứa 7 kind vòng 1. Không tái lập được.

**Sai lệch đúng nghĩa "rụng caveat":** 84 có 3 caveat; caveat #1 (synonym) sống tới 88; caveat #2 (parser) sống ở 85 §8.1; nhưng caveat #3 (**perturbation tự dựng → circular**) BIẾN MẤT từ 85 trở đi. Và cách 85 "vá" nó — "chạy lại trên config cuối" — KHÔNG chữa được circularity: chạy lại cùng bộ perturbation tự dựng trên parser khác vẫn ra AUC tautological. Thuốc không trị đúng bệnh.

**Vì sao "nặng" chứ không "chí mạng":** chưa train, chưa có kết quả nào phụ thuộc; 85 vẫn có cổng cứng chặn; tautology nghĩa là thước CHƯA ĐƯỢC KIỂM, không phải thước SAI — việc tách (action,target) vẫn khác cơ chế với cosine-cả-câu của K1. **Vì sao không nhẹ hơn:** report/88 là file đọc-đầu-tiên mỗi phiên và CLAUDE.md §0 + commit b5a6b29 đều chốt "metric-gate PASSED" — tức ở tầng ra quyết định chi tiền train, cái cổng đáng lẽ chặn lãng phí đang RỖNG mà được ghi là đã đậu.

**Việc phải làm:** sửa arm paraphrase để KHÔNG tái dùng `target_of()` (dùng từ đồng nghĩa loại nút thật: tab→section, button→control, và paraphrase do người/LLM khác-họ viết); phục hồi hoặc viết lại code vòng-2 ca-khó và lưu results; hạ "✅ QUA" ở 88/CLAUDE.md xuống "chưa kiểm được — perturbation tautological"; trả caveat #3 về đúng chỗ.

**Bằng chứng của người kiểm.** /mnt/d/Master/Thesis/harness/metric_v1_validate.py:29 (STOP chứa "on","the") · :36-44 (content_tokens/target_of loại verb+stopword) · :61-66 (target_score = max(Jaccard, bge≥0.85)) · :96-101 (target_error ép giao-token RỖNG → J=0) · :115-119 (paraphrase dựng từ target_of(g[i]) → round-trip J=1). Chạy kiểm: J=1.000 trên 8/8 mẫu đầu ac_test_200ep.json. /mnt/d/Master/Thesis/harness/metric_v1_results.json (paraphrase_mean=0.99999999986, target_error_mean=0.0118, separation_auc=1.0, fp_paraphrase=0.0; chỉ 7 kind vòng 1, KHÔNG có vòng-2 ca-khó). grep "artworks|ca khó|hard_case" trong harness/ = RỖNG → vòng-2 không tái lập được. /mnt/d/Master/Thesis/report/84_metric_validate_ket_qua.md (caveat #1/#2/#3 tồn tại đúng như trích; đối lại "đã kiểm bằng số, không assume" + "tin tốt cứng nhất" — mâu thuẫn nội bộ CÓ THẬT). /mnt/d/Master/Thesis/report/85_PREREG_v2_LAI.md:41 ("đã chạy synthetic, phải chạy lại trên config cuối"), :48-50 (bảng cổng, cột ghi rõ "Kết quả synthetic"), :53 (cổng cứng DỪNG-KHÔNG-train), :84 (caveat backstop = chép từ 84), :92 (buộc chạy lại trước commit) → hedge MẠNH HƠN đòn mô tả. /mnt/d/Master/Thesis/report/88_TOAN_CANH_CHI_TIET.md:140 (caveat synonym VẪN CÒN — đòn nói "biến mất hoàn toàn" là SAI, họ trích :137-138 và bỏ qua :140), :199 ("✅ QUA (AUC=1.0)" không kèm cờ synthetic — chỗ này đòn ĐÚNG), :213 (construct-validity vẫn nằm trong việc còn lại). git log b5a6b29 "metric-gate PASSED" — đúng như trích.

---

### B9. [VỪA] 'Vòng 2 — stress-test ca khó' không có code và không có kết quả lưu, nhưng được đóng băng vào pre-registration

- **Trục:** THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, metric_v1_results.json, mde_pilot.py, report/84, report/85)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** CHÍ MẠNG → **sau kiểm chéo:** VỪA

**Vấn đề.** report/84 §Vòng 2 báo ba con số (đích-sai-khó target-score TB = 0.350; AUC = 1.000 trên ca khó; bge cứu-nhầm 3/60 = 5%) và report/85:50 đóng băng '1.000 (cả ca khó)' làm kết quả cổng chính thức. Không có script nào trong repo sinh ra các con số này, và metric_v1_results.json chỉ chứa MỘT giá trị AUC (của vòng 1). Đây chính là phần được dùng để bác lại nghi ngờ 'vòng 1 quá dễ' — tức là mắt xích chịu lực nhất lại là mắt xích không tái lập được.

**Bằng chứng.** grep -rln 'artworks|0.350' --include=*.py . → không có file nào. harness/metric_v1_results.json chỉ có "separation_auc": 1.0 (một khoá duy nhất, 16 dòng). report/84:26-31 vs report/85:50.

**Đề xuất sửa.** Hoặc commit code + JSON của vòng 2, hoặc GỠ con số khỏi report/84 và report/85 và ghi rõ 'chưa chạy'. Một pre-registration trích số không có artifact thì mất hiệu lực làm dấu-thời-gian.

**Người phản-bác nói gì.** SỰ KIỆN họ nêu ĐÚNG HẾT, tôi không bác được phần dữ kiện: (1) không .py nào chứa "artworks"/"0.350"; (2) harness/metric_v1_results.json đúng 16 dòng, đúng MỘT khoá "separation_auc": 1.0; (3) harness/metric_v1_validate.py (196 dòng) KHÔNG có nhánh ca-khó nào — grep "hard|stress|round2" ra rỗng; (4) không có commit/stash/file kết quả nào khác. Thêm một điểm họ CHƯA nêu mà còn nặng hơn: vòng 1 dễ BY CONSTRUCTION — perturb(kind="target_error") ép `not (set(content_tokens(alt)) & cur)`, tức target sai bắt buộc RỜI HẲN token với gold ⇒ Jaccard=0, còn paraphrase giữ nguyên từ-lõi ⇒ Jaccard=1. AUC=1.000 của vòng 1 là hệ quả toán học của cách bơm lỗi, gần như không mang thông tin. Nên đúng như họ nói: sức nặng khoa học ("giải được chỗ K1 chết") dồn hết vào vòng 2 — phần không có code. Và report/84 ghi ở đầu file "Code: harness/metric_v1_validate.py" cho CẢ hai vòng là quy-nguồn SAI, vì script đó không thể sinh ra số vòng 2.

NHƯNG họ PHÓNG ĐẠI ở chữ "không tái lập được" và ở mức chí_mạng. Tôi đã tái lập vòng 2 trong ~10 phút, chỉ dùng data đã commit + đúng các hàm trong metric_v1_validate.py, dựng ca khó theo mô tả trong report (giữ từ-loại, đổi một từ-lõi, target đúng 2 token nội dung — chính hình dạng "artworks tab" vs "energy tab"): ra target-score TB = 0.351 (report: 0.350), AUC = 1.000 (report: 1.000), bge cứu-nhầm 2/60 ≈ 3% (report: 3/60 = 5%). Trùng tới 3 chữ số ở con số chính. Vậy đây KHÔNG phải số bịa, cũng không phải số chết-theo-người-chạy: là lỗi VỆ SINH TÁI LẬP (quên lưu script driver + json vòng 2), vá bằng ~40 dòng code, không đụng tới thiết kế hay kết luận.

Hạ xuống "vừa" chứ không phải "nhẹ", vì hai chỗ vẫn cắn thật: (a) một bản ĐĂNG-KÝ-TRƯỚC (report/85:50) đóng băng con số "1.000 (cả ca khó)" mà không có log sinh ra nó — pre-registration mất đúng thứ nó tồn tại để có, là dấu vết kiểm toán được; giám khảo bắt chỗ này là bắt trúng. (b) Kể cả khi tái lập, AUC=1.000 vòng 2 vẫn hơi rỗng vì nhánh paraphrase dựng ra có Jaccard=1 tất yếu — số thật sự có tin là "đích-sai-khó = 0.35 < ngưỡng J_MATCH 0.5 nên không khớp, và bge chỉ cứu nhầm ~3-5%", chứ không phải bản thân AUC. Điều an ủi: report/84 mục "Hoài nghi còn lại" đã tự khai đúng hai điểm này (paraphrase test còn dễ; perturbation do chính tác giả dựng nên có phần circular) — tác giả không giấu, nên đây không phải overclaim cố ý.

Việc phải làm: commit script vòng 2 + metric_v1_results_hard.json, sửa dòng "Code:" ở report/84 cho đúng, và ở report/85 ghi kèm nguồn file kết quả cho ô AUC. Không cần chạy lại thí nghiệm, không cần đổi ngưỡng.

**Bằng chứng của người kiểm.** Kiểm trên repo /mnt/d/Master/Thesis:
1. grep -rln "artworks|0\.350" --include=*.py . → (none). Xác nhận đòn.
2. wc -l harness/metric_v1_results.json → 16; chỉ một khoá "separation_auc": 1.0 (cùng n_ep=185, coverage_by_kind của vòng 1). Xác nhận đòn.
3. harness/metric_v1_validate.py:1-196 — không có nhánh ca-khó; grep "hard|stress|round2|vong2" → rỗng. git log --all cho file này chỉ 1 commit (b5a6b29); git stash list rỗng.
4. BẰNG CHỨNG TÔI TỰ TÌM THÊM (mạnh hơn đòn gốc): metric_v1_validate.py:93-100, nhánh kind=="target_error" có điều kiện `if set(content_tokens(alt)) and not (set(content_tokens(alt)) & cur)` ⇒ target sai luôn rời token hoàn toàn ⇒ Jaccard=0; nhánh kind=="paraphrase" (dòng ~113) giữ nguyên target_of(g[i]) ⇒ Jaccard=1. Nên AUC vòng 1 = 1.000 là tất yếu về mặt cấu tạo, không phải bằng chứng thước tốt. Khớp với số đã lưu: target_error_mean=0.0118, paraphrase_mean≈1.0.
5. TÁI LẬP VÒNG 2 (script: /tmp/claude-1000/-mnt-d-Master-Thesis/2577d164-1efa-40fc-8357-fedb08789c63/scratchpad/repro_r2b.py, import trực tiếp harness/metric_v1_validate.py, ollama bge-m3 local, data dataset_samples/androidcontrol_test/ac_test_200ep.json = 1039 step, 320 ứng viên target 2-token, n=60, seed 20260719):
   - đích-sai-KHÓ target-score TB = 0.351   [report/84: 0.350]
   - paraphrase TB = 1.000                  [report/84: 1.000]
   - AUC(paraphrase > đích-sai-khó) = 1.000 [report/84 + report/85:50: 1.000]
   - bge cứu-nhầm cos>=0.85: 2/60 = 3%      [report/84: 3/60 = 5%]
   (Biến thể nới lỏng, target >=2 token: 0.504 / AUC 1.000 / 25% — cho thấy con số 0.350 gắn chặt với hình dạng target đúng-2-token mà report mô tả, tức report tả đúng thí nghiệm đã chạy.)
6. report/84 dòng 3 ghi "Code: harness/metric_v1_validate.py" cho cả tài liệu, trong khi script đó không sinh được số vòng 2 → quy-nguồn sai, cần sửa.
7. report/84 mục "Hoài nghi còn lại" điểm 1 và 3 đã tự khai "paraphrase test còn dễ (Jaccard=1 tất yếu)" và "perturbation do chính tôi dựng → có phần circular".

---

### B10. [VỪA] Target rỗng khớp nhau hoàn hảo — đúng vào lớp nút icon-only mà K2/OCR đã chỉ là chỗ đau

- **Trục:** THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, metric_v1_results.json, mde_pilot.py, report/84, report/85)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** VỪA

**Vấn đề.** content_tokens() loại mọi từ trong STOP và ACTION_MAP. Nhưng nhiều NHÃN NÚT phổ biến nhất của GUI lại nằm trong hai tập đó: 'Next' (STOP), 'Back'/'Open'/'Enter'/'Go'/'Select'/'Return' (ACTION_MAP), cùng 'icon','button','arrow' bị STOP nuốt một phần. Hệ quả: 3.2% bước gold rút gọn về target RỖNG. Và target_score('','') = 1.0000 — vì khi Jaccard=0 code rơi xuống backstop, gọi emb([t1 or ' ', t2 or ' ']) trên hai chuỗi ' ' giống hệt nhau, cos=1.0 ≥ 0.85 → trả về 1.0. Kết quả kiểm chứng: step_match('Tap Next','Tap Back') = True, score 1.000; step_match('Click on the + icon','Click on the right arrow') = True, score 1.000. Đây chính xác là lớp nút icon-only mà report/74 (K2) đếm 20/40 ca và report/75 (OCR) nói không cứu được.

**Bằng chứng.** Chạy probe2 trên metric_v1_validate: target_score('','')=1.0000; step_match('Tap Next','Tap Back')→match=True score=1.000. Đếm trên dữ liệu thật: 33/1027 (3.2%) bước gold có target rỗng, ví dụ 'Go back'(x6), 'Click on L'(x2), 'Click on the + icon', 'Click on the right arrow'. Code: metric_v1_validate.py:37-39 (lọc), :63 (Jaccard=0 khi hợp rỗng), :66-68 (backstop trên ' ').

**Đề xuất sửa.** Chặn cứng: nếu một trong hai target rỗng sau chuẩn-hoá thì KHÔNG được match (trả 0), và đếm riêng nhóm này thành một hạng mục 'không phân xử được' báo minh bạch. Tách bảng từ-vựng-động-từ khỏi bảng-lọc-token: một từ chỉ bị loại khỏi target nếu nó nằm ở vị trí động từ, không loại ở mọi vị trí.

**Người phản-bác nói gì.** CƠ CHẾ ĐÚNG, TÔI KHÔNG BÁC ĐƯỢC. Tôi tự chạy lại và tái hiện y hệt: target_score('','') = 0.999999999 (≥ TAU_BGE 0.85 → trả 1.0), step_match('Tap Next','Tap Back') = True/1.000, step_match('Click on the + icon','Click on the right arrow') = True/1.000. Đây là lỗi thật trong harness/metric_v1_validate.py, chưa được nêu đích danh ở bất kỳ report nào — report/84 §"Hoài nghi" mục 2 chỉ nói chung chung "parser trích còn thô", không nói tới ca target rỗng tự-khớp. Phải vá trước khi đóng băng parser cuối.

NHƯNG BỐN ĐIỂM LÀM XẸP MỨC "NẶNG" XUỐNG "VỪA":

1. CỔNG report/84 KHÔNG BỊ NHIỄM — đây là phép kiểm quyết định. Tôi chạy lại toàn bộ cổng bơm-lỗi CHỈ trên 159/185 episode không có bước rỗng nào: AUC = 1.000, detection = 1.000, FP = 0.000 — trùng khít con số đã công bố (AUC 1.000 / 1.000 / 0.000). Nghĩa là kết luận "thước qua cổng, tách được chỗ K1 chết" KHÔNG do lỗi này tạo ra. Về mặt cơ chế cũng hợp lý: perturb target_error thay bằng alt KHÔNG rỗng, nên khi gold rỗng thì j=0 và backstop cos(' ', alt) vẫn thấp → vẫn bắt đúng. Lỗi này không thể bơm AUC lên.

2. PHÂN LOẠI 33 CA RỖNG CHO THẤY ĐÒN GỘP NHẦM. Đếm thật: 12 icon-like, 8 "go back"/nav, 6 gold rác (3 ca chuỗi RỖNG, 2 ca "click on the page", 1 ca "Click on the top at the bottom right corner"), 7 còn lại (nút Next/C/L). Với nhóm nav (8 ca), rỗng-khớp-rỗng là ĐÚNG chứ không sai: "Go back" ↔ "go back" phải khớp, thao-tác đã mang trọn nghĩa, không có đích. Với 6 ca gold rác thì lỗi nằm ở gold AndroidControl, không phải ở thước. Lớp thực sự hại = 12 icon + 7 misc = 19/1042 = 1,8% bước gold, không phải 3,2%.

3. CHỐT ACTION LÀ HÀNG RÀO CÓ THẬT, đòn bỏ qua. step_match('Go back','Tap Next') = False (navigate ≠ tap) dù score = 1.000. Nên bề mặt khớp-nhầm chỉ trong cùng một canon_action: 25 ca tap và 8 ca navigate tách rời nhau. Trên dữ liệu thật chỉ 5/185 episode có ≥2 bước rỗng CÙNG action — điều kiện để tự-khớp-nhầm nội bộ xảy ra.

4. HƯỚNG THIÊN LỆCH LÀ BẢO THỦ, KHÔNG PHẢI THỔI PHỒNG KẾT QUẢ. Estimand đã đăng-ký-trước (report/85 §3, §6) là HIỆU CẶP Student vs Teacher-BASE trên cùng split, cùng thước, wild-cluster bootstrap. Lỗi này cộng điểm cho CẢ HAI nhánh như nhau (nó phụ thuộc gold, không phụ thuộc model) → triệt tiêu bậc nhất trong hiệu-số, và phần dư đẩy cả hai lên trần → NÉN hiệu về null, tức làm luận văn KHÓ đạt kết quả dương hơn, chứ không tạo ra kết quả dương giả. Trần khai thác tối đa của một model suy biến kiểu "luôn xuất Tap Next" cũng chỉ ăn được 25/1042 = 2,4% coverage.

MÔ TẢ NHÂN QUẢ CỦA ĐÒN CÓ CHỖ SAI: 'arrow' KHÔNG nằm trong STOP (tôi kiểm: arrow → STOP=False, ACTION=False; content_tokens('Click on the right arrow') = ['arrow']). Nó bị nuốt bởi regex bỏ-cụm-vị-trí ở dòng 42 ("on the right ...[\w\s]*"), không phải bởi STOP. Câu "'icon','button','arrow' bị STOP nuốt" chỉ đúng 2/3. Và việc quy lớp này về "chính xác lớp icon-only K2 đếm 20/40" là gán ghép: chỉ 12/33 ca rỗng là icon.

KẾT: lỗi thật, phải sửa (chặn backstop khi một trong hai target rỗng; regex vị trí dòng 42 quá tham, đang nuốt cả danh từ đích sau chỉ-hướng; cân nhắc bỏ 'next'/'button'/'icon' khỏi STOP vì chúng là NHÃN nút). Nhưng nó là lỗi parser cục bộ ~2%, đối xứng giữa hai nhánh, thiên lệch bảo thủ, và KHÔNG làm hỏng cổng đã công bố — đúng mức "vừa", không tới "nặng". Cũng cần ghi nhận report/85 §4 đã đăng-ký-trước việc "chạy lại cổng trên parser cuối + validate bộ-trích P/R trên tập gán tay", tức có sẵn chốt kiểm sẽ bắt được lỗi này — dù lần này nó chưa bắt.

**Bằng chứng của người kiểm.** TÔI TỰ CHẠY (~/.venvs/thesis/bin/python, ollama bge-m3 local, không gọi API):

[1] Tái hiện lỗi — XÁC NHẬN:
  target_score('','') = 0.9999999990000009
  step_match('Tap Next','Tap Back')                    → match=True  score=1.0000
  step_match('Click on the + icon','Click on the right arrow') → match=True  score=1.0000
  step_match('Tap Next','Tap the Search button')       → match=False score=0.0000
  step_match('Go back','Tap Next')                     → match=False score=1.0000  ← chốt action chặn được

[2] Từ vựng (bác một phần mô tả của đòn):
  next  STOP=True  ACTION=False
  icon  STOP=True  ACTION=False
  button STOP=True ACTION=False
  arrow STOP=False ACTION=False  ← KHÔNG bị STOP nuốt
  back/open/enter/go/select/return: ACTION=True
  content_tokens('Click on the right arrow') = ['arrow'] → target_of = '' (do regex vị trí dòng 42, KHÔNG do STOP)

[3] Prevalence trên ac_test_200ep.json (1042 step):
  target rỗng = 33/1042 = 3,2% (khớp con số đòn nêu)
  phân loại: icon-like=12, nav/go-back=8, gold-rác=6, khác=7
  action của bước rỗng: {tap: 25, navigate: 8}
  episode chứa ≥1 bước rỗng: 26/185
  episode có ≥2 bước rỗng CÙNG action (điều kiện tự-khớp-nhầm): 5/185

[4] PHÉP KIỂM QUYẾT ĐỊNH — cổng chạy lại chỉ trên 159/185 episode SẠCH (không bước rỗng):
  AUC(paraphrase > target_error) = 1.000
  paraphrase TB = 1.000 | target_error TB = 0.008
  detection = 1.000 | FP = 0.000
  → trùng khít metric_v1_results.json đã công bố (AUC 1.0, det 1.0, FP 0.0, target_error_mean 0.0118)
  → kết luận "QUA CỔNG" của report/84 KHÔNG phụ thuộc lỗi này.

[5] Đọc code xác nhận vị trí lỗi: harness/metric_v1_validate.py:37-39 (content_tokens lọc STOP ∪ ACTION_MAP), :42 (regex bỏ cụm vị trí — thủ phạm thật của ca 'right arrow'), :63 (j=0 khi hợp rỗng), :66-68 (emb([t1 or ' ', t2 or ' ']) → cos(' ',' ')=1.0 ≥ 0.85).

[6] Đọc report/84_metric_validate_ket_qua.md §"Hoài nghi còn lại" mục 2 + report/85_PREREG_v2_LAI.md §4: có đăng-ký-trước "chạy lại cổng trên parser cuối + validate bộ-trích P/R trên tập gán-tay khi có output model" — nhưng KHÔNG nêu đích danh ca target rỗng, nên không tính là "đã xử lý".

---

### B11. [VỪA] Trục TRUNG THỰC G=12: lực thật rất yếu, và đúng ô MDE đó đang để TRỐNG

- **Trục:** THỐNG KÊ + LỰC MẪU (MDE trục ĐÚNG, wild-cluster bootstrap vs exact sign-flip, đa phép so sánh)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** VỪA

**Vấn đề.** Trục phụ dùng exact sign-flip với G=12. Ô MDE của trục này chưa điền. Với chính SD nền mà pilot đo được, lực để bắt một hiệu ứng cỡ vừa là rất thấp — nghĩa là một kết quả null ở trục trung thực sẽ không đọc được gì, không phân biệt được "không có hiệu ứng" với "có hiệu ứng 15 pp".

**Bằng chứng.** Tôi mô phỏng exact sign-flip đầy đủ (liệt kê cả 2^12=4096 tổ hợp dấu), α=0,05 hai phía, 400 lần lặp mỗi ô, d_j ~ N(eff, SD_d): với SD_d=0,362 → lực = 7% @5pp, 12% @10pp, 25% @15pp, 43% @20pp, 73% @30pp. Ngay cả với SD_d lạc quan 0,20 → 36% @10pp, 66% @15pp. report/85:67 để ngỏ "[MDE trục trung thực MobileViews = ___ pp]". Công thức của chính tác giả ở G=12: 3.077×0.362/√12 = 32,2 pp.

**Đề xuất sửa.** Điền ô MDE trục trung thực TRƯỚC khi commit report/85, không để trống. Nếu ra ~30 pp thì hoặc (a) tăng số app MV (kích hoạt đúng cơ chế 15/15 mà report/56:65 đã dự trù), hoặc (b) hạ trục trung thực xuống mức mô tả/định tính và khai thẳng là không đủ lực để kiểm định — chứ đừng chạy rồi báo "null".

**Người phản-bác nói gì.** Đòn SỐNG nhưng phải HẠ từ "nặng" xuống "vừa". Phần đúng: mô phỏng của họ chính xác (tôi lặp lại độc lập, khớp trong 1-3 pp), ô [MDE trục trung thực = ___] ở report/85:67 đúng là còn trống, và report/_archive/55:42(b) chính tác giả đã tự khai "chưa tự mô phỏng lại power của exact sign-flip rời rạc" — họ làm đúng việc tác giả còn nợ. Nhưng ba chỗ phóng đại: (1) SD_d=0.362 KHÔNG thuộc trục này — nó đo trên trục ĐÚNG (điểm-đúng gpt-4o-mini trên AndroidControl, 26 app, 2-4 bước/app, report/86), còn trục trung thực đo f=1−bịa/nhắc-nút trên MobileViews, chưa từng đo; con số headline 32,2 pp là mượn SD sai chỗ. (2) Bản thân 0.362 = √2×SD_arm, giả định TƯƠNG QUAN BẰNG 0 giữa hai arm trong khi Tier 2 là thiết kế GHÉP CẶP trên cùng app/màn/câu hỏi (report/54:541 đã ghi rõ đây là "cận trên thận trọng"); nặng hơn, K2 (report/74) đo teacher bịa ~0-2% → arm teacher gần như hằng số → Var(d)≈Var(student), không phải 2×Var. Dùng √2 ở đây là chồng hai lớp bi quan. (3) Ô trống không phải sơ suất mà là CỔNG TN0 đã đăng-ký-trước (report/56:58-66; report/54 dòng 446/568/607/1069/1120; report/85:93) và là ô DUY NHẤT được phép sửa sau commit. Thêm nữa trục này là PHỤ: report/85 §5-§7 đặt trục ĐÚNG (MDE 8-9 pp @ G≈150-250) làm trụ quyết định, Tier 1 ghi rõ "báo dù null" → null ở đây đã pre-register là chấp nhận được, không kéo sập kết luận. Phần CÒN SỐNG mà tôi không bác được: phương án dự phòng 15/15 gần như vô dụng (G 12→15 chỉ giảm MDE ~13%: 32,2→28,1 pp, hoặc 22,7→19,9 pp ở SD=0.256), và CV số-màn/app = 0.53 với một app chỉ 1 màn khiến xấp xỉ liên tục là "cận dưới lạc quan" (đúng cảnh báo report/_archive/55:21). Phát biểu đúng của đòn phải là "SD trục trung thực còn chưa đo + van 15/15 quá yếu nếu SD cao", KHÔNG phải "trục trung thực chết ở 32 pp".

**Bằng chứng của người kiểm.** (1) Mô phỏng độc lập exact sign-flip, liệt kê đủ 2^12=4096 tổ hợp dấu, α=0,05 hai phía, 4000 lặp/ô: SD_d=0.362 → 7% @5pp, 15% @10pp, 26% @15pp, 42% @20pp, 75% @30pp — khớp bảng của họ (7/12/25/43/73) trong sai số mô phỏng. SD=0.256 → 24% @10pp, 47% @15pp, 72% @20pp; SD=0.20 → 36%/66%/89%; SD=0.15 → 54%/88%/98%. (2) report/85:67 xác nhận có chuỗi "[MDE trục trung thực MobileViews = ___ pp] ← điền khi pilot trung thực (v1 để trống)" — bằng chứng họ nêu CÓ THẬT, không bịa. (3) report/86:12 "SD per-app (một arm) = 0.256; SD-hiệu bảo thủ = √2 × 0.256 = 0.362" — xác nhận đây là cận trên giả định độc lập, và report/86:27 tự khai "MDE này BẢO THỦ (overestimate): pilot chỉ 2-4 bước/app → SD phồng". (4) report/86 header: pilot chạy trên AndroidControl app-unseen, 26 app, ~85 bước, đo điểm-đúng — KHÁC construct/dataset với trục trung thực. (5) report/74 (K2): 127 bước teacher, 40 ca không-verbatim soi tay = 0 ca bịa-gần-nghĩa → teacher bịa ~0-2%, arm teacher gần trần. (6) report/56:58-66 cổng MDE + luật "MDE > 15-20 pp → tăng split 15/15 TRƯỚC khi khoá ngưỡng"; report/56:4 ô [MDE] là ngoại lệ duy nhất được sửa sau commit; report/85:93 "Pilot đo-nền → điền [MDE] → commit lần 2". (7) report/85 §5-§6: trục trung thực ghi rõ "TRỤC PHỤ", Tier 1 = "readout phụ gần-miễn-phí, báo dù null"; trục ĐÚNG dùng wild-cluster bootstrap G~150-250, MDE 8-9 pp. (8) Tính lại MDE: G=12/SD=0.362 → 32,2 pp; G=15 → 28,1 pp (chỉ giảm 13%); G=15/SD=0.256 → 19,9 pp. (9) harness/train_eval_app_split.json + kept_screens_final.json: 12 app test, số màn/app = [5,2,3,8,4,4,5,2,8,3,6,1], tổng 51 màn, mean 4,25, CV 0,53. (10) report/_archive/55:42 tự khai "(b) chưa tự mô phỏng lại power của chính exact sign-flip rời rạc để xác nhận MDE thật lệch bao nhiêu so với xấp xỉ Julious" + :21 cảnh báo CV lớn → MDE là "cận dưới lạc quan".

---

### B12. [VỪA] Thước đo thưởng cho việc bắt chước TỪ VỰNG annotator AC, không phải hướng dẫn tốt hơn

- **Trục:** DỮ LIỆU, SPLIT, RÒ RỈ — và câu hỏi "vừa học vừa chấm cùng loại"
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** CHÍ MẠNG → **sau kiểm chéo:** VỪA

**Vấn đề.** Headline của trục ĐÚNG là Student (train trên gold AC) > Teacher zero-shot, chấm bằng chồng-từ-nội-dung với chính gold AC. Tôi đọc thước và thấy cơ chế cho hiệu ứng dương KHÔNG cần model hướng dẫn tốt hơn: STOP-list ở metric_v1_validate.py cắt hết từ vị trí/loại-nút (bottom/top/corner/screen/button/icon), nên phần còn lại để so là ĐÚNG DANH TỪ mà annotator AC đã dùng. Model học văn phong AC sẽ trúng từ đó; teacher nói cách khác thì trượt dù đúng nghĩa. Thiết kế hiện tại KHÔNG có nhánh nào tách 'khớp văn phong' khỏi 'chọn đúng nút', nên con số headline không diễn giải được.

**Bằng chứng.** harness/metric_v1_validate.py:41-56 (STOP + content_tokens + target_of). Tôi chạy lại thước trên 4 cặp hướng dẫn ĐỀU ĐÚNG cho người: gold 'Click on the three lines at the bottom left corner' vs 'Tap the hamburger menu icon' → Jaccard=0.00; 'Click on the bell icon at the bottom' vs 'Tap the notifications tab' → 0.00; 'Click on the search icon at the top left corner' vs 'Tap the magnifying glass' → 0.00; 'Select the third artwork.' vs 'Tap the third image in the list' → 0.25 (dưới ngưỡng J_MATCH=0.5). Thêm: 243/1042 (23,3%) gold step kết thúc bằng dấu câu, mà content_tokens dùng regex [a-z0-9@._]+ nên giữ dấu chấm dính vào từ → 'artwork.' KHÔNG khớp 'artwork' (chạy lại: giao tập chỉ còn {'third'}). Tức là cả DẤU CÂU của annotator cũng được tính điểm.

**Đề xuất sửa.** Trước khi tiêu tiền train: (1) thêm nhánh Teacher-STYLE-MATCHED (few-shot nhét vài gold step AC vào prompt để teacher nói cùng phương ngữ) — rẻ, và hiệu-số Student − Teacher-STYLE mới là ước lượng của 'chọn đúng nút'; hiệu-số Teacher-STYLE − Teacher-BASE chính là lượng khớp-văn-phong thuần. (2) Chuẩn hoá bỏ dấu câu trong content_tokens. (3) Pre-register rằng nếu Student − Teacher-STYLE mà CI chứa 0 thì đóng góp model không được claim là 'hướng dẫn tốt hơn'.

**Người phản-bác nói gì.** Đòn SỐNG nhưng phải thu hẹp mạnh: hai trong ba chân của nó đổ khi kiểm bằng số.

CHÂN CÒN ĐỨNG (thật, không bác được): với đích KHÔNG có nhãn chữ trên màn (nút icon), STOP-list ở metric_v1_validate.py:28-29 cắt hết từ vị trí/loại-nút, phần còn lại đúng là TÊN TỰ ĐẶT của annotator ("three lines", "bell", "tick"). Model học văn phong AC trúng từ đó; teacher gọi cách khác ("hamburger menu", "notifications tab", "magnifying glass") trượt dù đúng nút. Tôi chạy lại 3 cặp icon của họ QUA CẢ backstop bge-m3 (không chỉ Jaccard như họ làm): target_score = 0.000/0.000/0.000, step_match = False cả ba. Backstop 0.85 không cứu. Và report/85 KHÔNG có nhánh nào đo riêng phần lợi do khớp văn phong — mitigation ghi ở §8 rủi ro 4 ("mốc Teacher-BASE + thước ưu tiên action∧target") không xử được đúng cơ chế này, vì Teacher-BASE chính là arm bị thiệt.

CHÂN ĐỔ 1 — "thước thưởng văn phong" là SAI với ~80-90% dữ liệu. Tôi test đảo hoàn toàn văn phong nhưng GIỮ nhãn trên màn (đổi động từ, bỏ cụm vị trí, thêm ngoặc kép, thêm mệnh đề: gold 'click on Add bookmark option' → 'Tap on "add bookmark" to continue'): khớp 73/73 = 100.0%. Đối chứng đổi sang nhãn khác: 0/68 = 0.0%. Tức thước KHÔNG nhạy văn phong; nó nhạy DANH TỪ NHÃN. Mà với đích là chữ hiển thị, cả annotator lẫn model đúng đều chép cùng chữ từ màn → trùng từ = grounding đúng, không phải bắt chước. Đếm trên 1042 gold step: chỉ 3.6% chứa cụm mô-tả-icon rõ (regex three dots/lines, tick, bell icon, magnifying, hamburger, cross/plus icon); nới rộng vocab tối đa (có nhiễu) mới lên ~18%; 78-92% giữ nhãn-chữ riêng của app. Vậy cơ chế họ nêu áp cho thiểu số stratum, không phải "con số headline không diễn giải được".

CHÂN ĐỔ 2 — chân dấu câu SAI VỀ VẬN HÀNH. Đúng là regex [a-z0-9@._] giữ dấu chấm dính từ (tôi xác nhận content_tokens('Select the third artwork.') = ['third','artwork.']) và 243/1042 = 23.3% gold kết thúc bằng dấu câu (số họ nêu đúng). NHƯNG họ dừng ở Jaccard, không chạy hàm thật: target_score('third artwork.','third artwork') = 0.943 ≥ TAU_BGE 0.85 → step_match = True. Backstop bge-m3 nuốt trọn lỗi dấu câu. Câu "cả DẤU CÂU của annotator cũng được tính điểm" là sai; đó là vết bẩn 1 dòng code, không phải nguồn hiệu ứng.

Tác giả cũng đã chạm tới vấn đề, dù chưa dập: report/85 §3 BẮT BUỘC "báo tách nhóm target-CHỮ vs target-ICON" (chính là stratification cô lập đúng chỗ đòn này bám) + báo action và target riêng + LLM-judge khác-họ cross-check; §8 rủi ro 4 gọi tên "circular ngược (train trên gold, chấm so gold)"; report/86 §3 viết thẳng rằng hiệu ứng dương kỳ vọng đến từ "lợi-thế-sân-nhà in-distribution". Ngoài ra mde_pilot.py đã neo văn phong cho teacher trong prompt ("in the style 'Tap the Search bar'") = một phần kiểm soát văn phong đã cài sẵn. Mini-study construct-validity người (report/78) thì đang HOÃN — đây là lỗ thật.

Kết luận: hạ chi_mang → vua. Không phải "headline không diễn giải được"; mà là "ở stratum target-ICON (~5-15% bước) hiệu số Student−Teacher lẫn lợi-do-khớp-quy-ước-đặt-tên, và chưa có arm nào tách ra". Vá rẻ, không phải thiết kế lại: (1) báo Δ riêng cho stratum CHỮ (headline) và ICON (phụ) — pre-reg đã yêu cầu, chỉ cần thi hành; (2) thêm arm Teacher-FEWSHOT-AC-style (vài ví dụ gold trong prompt) để hấp thụ quy ước đặt tên → phần Δ còn lại là năng lực thật; (3) sửa regex content_tokens bỏ dấu câu đuôi (1 dòng). Nếu bỏ cả ba thì đòn leo lại thành nặng.

**Bằng chứng của người kiểm.** Code đọc: /mnt/d/Master/Thesis/harness/metric_v1_validate.py:28-29 (STOP), :37-44 (content_tokens regex [a-z0-9@._]+, target_of), :60-74 (target_score max(Jaccard, bge≥0.85), step_match); /mnt/d/Master/Thesis/harness/mde_pilot.py:27-30 (PROMPT neo văn phong teacher).

Chạy lại 3 cặp icon của họ QUA hàm thật target_score/step_match (có bge-m3 ollama, không chỉ Jaccard): 'three lines at the bottom left corner' vs 'hamburger menu icon' = 0.000/False; 'bell icon at the bottom' vs 'notifications tab' = 0.000/False; 'search icon at the top left corner' vs 'magnifying glass' = 0.000/False → chân icon của họ ĐÚNG, backstop không cứu.

Bác chân dấu câu: target_score('Select the third artwork.','Select the third artwork') = 0.943, step_match = True (bge nuốt dấu chấm). Xác nhận 243/1042 = 23.3% gold có dấu câu cuối, và content_tokens giữ 'artwork.' — nhưng không gây trượt.

Bác chân "thưởng văn phong": test 120 gold mẫu (seed 3), giữ nhãn + đảo văn phong hoàn toàn → khớp 73/73 = 100.0%; đối chứng thay nhãn khác → 0/68 = 0.0%.

Đếm stratum trên dataset_samples/androidcontrol_test/ac_test_200ep.json (1042 step): cụm mô-tả-icon rõ 38/1042 = 3.6%; vocab icon nới rộng (có nhiễu 'up/down') 188/1042 = 18.0%; target rỗng sau STOP 33 (3.2%); còn nhãn-chữ riêng 819-958 (78.6-91.9%).

Đọc: report/85_PREREG_v2_LAI.md §3 (bắt buộc tách target-CHỮ vs target-ICON, báo action/target riêng, LLM-judge khác-họ), §8 rủi ro 2 & 4 (backstop kết-oan synonym; circular ngược); report/86_MDE_pilot_ket_qua.md §3 ("lợi-thế-sân-nhà" in-distribution); harness/metric_v1_results.json (AUC=1.000 nhưng bơm-lỗi sinh paraphrase từ chính target_of(gold) → cổng này KHÔNG hề test biến-thiên-từ-vựng giữa hai người viết khác nhau — đây là điểm đòn nói đúng mà report/84 chỉ ghi mơ hồ là "paraphrase-synonym có thể kết-oan").

---

### B13. [VỪA] Gold step_instructions của AndroidControl là nhãn thao tác ngắn, không phải 'hướng dẫn cho người'

- **Trục:** DỮ LIỆU, SPLIT, RÒ RỈ — và câu hỏi "vừa học vừa chấm cùng loại"
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** VỪA

**Vấn đề.** Tuyên bố tính mới là 'model đầu tiên sinh hướng dẫn nhiều bước CHO NGƯỜI ĐỌC'. Tôi đọc dữ liệu thật và thấy target train là nhãn action ngắn, nhiều nhiễu annotator. Train trên đây ra một bộ sinh nhãn-thao-tác-từng-bước bằng ngôn ngữ tự nhiên — khác các bài GUI-agent chủ yếu ở chỗ output là câu chữ thay vì function call, không phải ở chỗ 'viết cho người đọc'.

**Bằng chứng.** dataset_samples/androidcontrol_test/ac_test_200ep.json (200 ep, 1042 step). Tôi đo: trung vị 6 từ, 48,9% câu ≤5 từ, 10,3% ≤3 từ; 60,4% bắt đầu bằng click/tap/press/select; chỉ 749 câu distinct / 1042; 167/842 cặp bước LIỀN NHAU trùng y hệt (ep 'The Times Of India' có 'Click on the first result podcast' 2 lần liên tiếp, action thứ 2 là 'wait'); 3 step rỗng; câu hỏng kiểu 'Click on the top at the bottom right corner' (ep 10265, gõ nhầm 'cart').

**Đề xuất sửa.** Chọn một trong hai: (a) khai thẳng target là step-instruction của AC và hạ claim xuống 'sinh mô tả thao tác bằng ngôn ngữ tự nhiên', hoặc (b) giữ claim 'cho người' nhưng phải có tầng viết-lại + một eval NGƯỜI trên output thật (mini-study construct-validity hiện đang HOÃN chính là chỗ này). Đồng thời lọc dữ liệu train: bỏ step rỗng, gộp cặp trùng liên tiếp (~20%), nếu không model sẽ học cả tật lặp của annotator.

**Người phản-bác nói gì.** Đòn SỐNG nhưng phải hạ mức, và phải cắt bỏ phần kết luận.

PHẦN SỐNG (thật, tác giả phải sửa): cụm 'CHO NGƯỜI ĐỌC' ở report/85 dòng 11 — đóng góp số 1 — đang gánh sức nặng tu từ mà dữ liệu không đỡ nổi. Giám khảo mở AC thấy 'Click on Gmail' (6 từ, 60% mở đầu bằng click) rồi nghe 'hướng dẫn cho người đọc' sẽ thấy như dán nhãn lại. Thêm nữa họ tìm được lỗi MỚI mà bản tự-kiểm 30-ep của tác giả bỏ sót: 3 step rỗng, câu gõ nhầm ('the top' = 'the cart'), trùng liền nhau. Câu 'TB 7 từ, 0% ngắn-mơ-hồ' ở report/79 là kiểm mẫu quá nhỏ và hơi tự khen — phải đo lại trên toàn bộ và khai số nhiễu.

PHẦN BỊ BÁC (4 chỗ vượt quá bằng chứng):
1. 'Ngắn ⇒ không phải cho người' là bước nhảy logic. Sách hướng dẫn điện thoại, wikiHow đều viết mệnh lệnh ngắn. 22% câu chỉ vị trí trên màn, 6,9% nêu mục đích — đó chính xác là thứ chỉ có nghĩa với NGƯỜI đọc, function call không cần. Mỉa mai là report/76 (VIỆC1) phát hiện fallback tự sinh của tác giả THIẾU đúng phần chỉ-vị-trí này, còn gold AC thì CÓ.
2. 'Nhiều nhiễu annotator' phóng đại ~6x: 86/167 cặp trùng là nhãn đúng cho thao tác lặp thật, 58/81 còn lại là artifact 'wait' lọc được máy móc. Nhiễu thật ~2,7% + 0,3% rỗng.
3. Lập luận nhiễu tự đá chân mình: AC là tập ĐO của trục ĐÚNG, nhiễu ở đó kéo hiệu ứng về NULL — làm tác giả khó hơn, không giúp thổi phồng. report/86 đã đo teacher 30%, SD-hiệu 0,362, MDE 8-9pp — trục còn đủ lực DÙ có nhiễu.
4. Quy khác biệt về 'câu chữ thay vì function call' là đọc thiếu thiết kế: khác biệt cấu trúc là step_instruction chuyển từ INPUT sang TARGET, và model phải sinh trọn chuỗi từ MỘT ảnh. Bằng chứng độ-dài-câu không nói gì về điều đó.
5. 'Tác giả chưa nhận ra' là SAI hiển nhiên — report/81 gọi đích danh 'step-instruction NGẮN AC', và MV-aux ablation tồn tại đúng để cấp giọng văn dài.

HẠ nặng → vừa: đây là lỗi CÁCH KỂ ở một câu headline, sửa bằng viết lại (bỏ 'cho người đọc' trần trụi, chuyển sang trục report/82 'target sinh + sinh trọn chuỗi từ 1 ảnh', khai thống kê độ dài + tỉ lệ nhiễu, cộng thêm bước lọc step rỗng/trùng-wait trước khi train). Không đổi thí nghiệm, không đổi thước đo, không đổi dữ liệu, không sập trục nào. Không phải 'nặng' vì nặng phải là hỏng thiết kế hoặc phải chạy lại — cái này không.

**Bằng chứng của người kiểm.** ĐO LẠI ĐỘC LẬP (dataset_samples/androidcontrol_test/ac_test_200ep.json, 200 ep / 1042 step): TẤT CẢ số họ nêu đều TÁI LẬP CHÍNH XÁC — trung vị 6 từ (mean 7.0), 48,9% ≤5 từ, 10,3% ≤3 từ, 60,4% mở đầu click/tap/press/select, 749 distinct/1042, 167/842 cặp liền nhau trùng, 3 step rỗng; ep 10265 có thật câu 'Click on the top at the bottom right corner'. Không có bịa bằng chứng.

NHƯNG các phép đo BỔ SUNG tôi chạy làm yếu suy luận của họ:
(1) REGISTER người-đọc: 22,2% câu có chỉ-dẫn vị trí ('at the bottom right corner of the screen'), 44,3% gọi tên loại phần tử UI (icon/button/tab/field), 34,3% dùng động từ NGOÀI click (scroll/swipe/type/open/go back), 6,9% có mệnh đề mục đích ('to see category', 'to read the article'). Mẫu ngẫu nhiên: 'Tap on the search icon present at the bottom right corner of the screen.', 'Swipe up to read the article', 'Click on the Email section to add the email address to this contact.' Đây là văn phong sách hướng dẫn điện thoại, KHÔNG phải function call.
(2) 'Ngắn' ≠ 'mơ hồ': đọc 25 mẫu ≤3 từ — 'Select Madinah', 'Click on Gmail', 'Open Clock app', 'Choose Gigawatt unit' đều nêu đích danh mục tiêu. Chỉ 2/25 thật sự hỏng.
(3) NHIỄU BỊ THỔI PHỒNG: trong 167 cặp trùng liền nhau, 86 cặp có action + toạ độ Y HỆT (người thật sự bấm hai lần → nhãn ĐÚNG, không phải lỗi); trong 81 cặp khác-action thì 58 dính step 'wait' (annotator kéo nhãn sang bước chờ — artifact hệ thống, lọc bằng 1 dòng code). Còn lại ~23/842 = 2,7% đáng ngờ thật. 3 rỗng = 0,3%. Số '749 distinct' gây hiểu nhầm: 'Go back'/'Scroll down' lặp qua 200 ep KHÁC NHAU là dùng lại từ vựng, không phải trùng nội dung.
(4) TÁC GIẢ ĐÃ BIẾT: report/79 dòng 58-59 có mục 'đã kiểm chất lượng gold step_instructions' — đọc 30 ep/159 step, tự báo 'TB 7 từ' (KHỚP CHÍNH XÁC số tôi đo). report/81:191,204 gọi thẳng tên 'step-instruction NGẮN AC' làm rủi ro xung-đột-phong-cách với văn tự do MobileViews. report/85:27 giữ MV-chưng-cất làm data AUX + ablation bật/tắt — chính là arm cấp giọng văn dài cho người đọc.
(5) TRỤC TÍNH MỚI THẬT nằm chỗ khác: report/82 chốt seam = 'AC step_instruction làm TARGET SINH (không phải input)' — mọi bài GUI-agent đặt step_instruction ở ĐẦU VÀO rồi đoán MỘT action; ở đây model chỉ thấy 1 ảnh + câu hỏi và phải sinh TRỌN chuỗi nhiều bước, không nhìn màn kế tiếp. Bằng chứng của họ (độ dài câu) không chạm tới khác biệt cấu trúc này.

---

### B14. [VỪA] G (số app) trong tính MDE phồng 2-3 lần vì lấy nhầm file; hai con số của report/86 đều sai

- **Trục:** DỮ LIỆU, SPLIT, RÒ RỈ — và câu hỏi "vừa học vừa chấm cùng loại"
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** VỪA

**Vấn đề.** MDE 8-9 pp được suy từ 'G ~150-250 app'. Con số G đó lấy từ ac_test_200ep.json — là test set CHUNG, không phải quần thể đánh giá. Quần thể thật là app_unseen 631 ep, và file của chính dự án cho thấy app ở đó tập trung hơn nhiều (tin tức/nghệ thuật/moon-phase).

**Bằng chứng.** report/85_PREREG_v2_LAI.md:19 và :64 ('~114 app distinct chỉ trong 200 ep' → 'G ~150-250'). Đối chiếu harness/ac_app_unseen_count.json: sampled 250, with_app 102, distinct_apps 42. Tôi tính Chao1 từ chính bảng đó (f1=22 app xuất hiện 1 lần, f2=8 app 2 lần): 42 + 22²/(2·8) ≈ 72 app — trần độ giàu của cả split, không phải 150-250. MDE = 3.077×0.362/√72 = 13,1 pp (không phải 9,1), √42 → 17,2 pp. PHẢN BÁC công bằng: SD=0.362 bị phồng vì pilot chỉ ~3,5 bước/app (harness/mde_pilot_results.json: n_apps=26, n_steps=91) — thành phần nhị thức p(1−p)/n = 0,3·0,7/3,5 = 0,060 so với phương sai quan sát 0,0656 → phương sai GIỮA-app thật chỉ ≈0,006, SD_between ≈0,075, khi đó MDE @G=72 ≈ 2,7 pp. Tức kết luận 'đủ lực' nhiều khả năng vẫn sống, nhưng cả tử số lẫn mẫu số trong report/86 đều sai và bù trừ cho nhau.

**Đề xuất sửa.** Đếm lại G trên đúng 631 ep app_unseen sau khi chuẩn hoá tên app, và tính MDE bằng phân rã phương sai (between-app vs binomial-within) thay vì lấy SD thô của pilot. Sửa report/85 §1/§6 và report/86 trước khi commit bản đăng-ký-trước.

**Người phản-bác nói gì.** Lõi sự kiện của đòn ĐÚNG và tái lập được: G lấy nhầm quần thể (test CHUNG thay vì app_unseen) nên phồng ~2-3 lần, kéo theo MDE headline của report/86 dưới-ước ~45% (8-9 pp thay vì ~13 pp @ G=72). Phải sửa trước khi commit report/85. Nhưng mức "nặng" là quá tay vì bốn lẽ: (1) không quyết định đăng-ký-trước nào bị lật — cổng MDE<15-20 pp vẫn QUA ở chính G=72 của đòn (13,1 pp), và lựa chọn wild-cluster bootstrap vẫn đúng vì 2^42 vẫn bất khả thi; (2) nửa "tử số sai" không phải phát hiện — report/86 mục Đọc kỹ điểm 2 đã tự khai nguyên văn SD phồng do 2-4 bước/app và gọi 8-9 pp là cận-trên; một cận-trên khai báo có chủ ý không phải lỗi, lại còn chồng thêm lớp bảo thủ sd_diff=√2×sd (bỏ tương quan cặp cùng-app); (3) đòn sai chiều estimator — Chao1 là cận DƯỚI (Chao 1984), không phải "trần độ giàu", lại tính trên tập chỉ phủ 41% ep với 59% rớt lệch không-ngẫu-nhiên về phía app hiếm; con số thay thế sd_between=0.075 là hiệu của hai ước lượng nhiễu (0.0656−0.0600) trên 26 app nên cũng không đáng tin hơn; (4) con số bị đánh vốn đã có cờ tạm — report/85:19 đóng ngoặc vuông "[≈150-250 — chốt chính xác lúc build]" theo đúng quy ước ô-điền-sau của file, report/86 kèm công thức tính lại. Lỗi ghi-chép/nguồn-dữ-liệu phải vá, không phải lỗi thiết kế.

**Bằng chứng của người kiểm.** TÁI LẬP ĐỘC LẬP (chạy ~/.venvs/thesis/bin/python, không gọi API):
1) Nguồn gốc G — chạy chính hàm app_of() của /mnt/d/Master/Thesis/harness/mde_pilot.py trên /mnt/d/Master/Thesis/dataset_samples/androidcontrol_test/ac_test_200ep.json (test CHUNG): with_app=134/200 (67%), distinct=103, f1=81, f2=17. Khớp gần khít "phủ ~72% ep trên mẫu 200" + "~114 app distinct chỉ trong 200 ep" ở /mnt/d/Master/Thesis/report/85_PREREG_v2_LAI.md:19 => XÁC NHẬN số lấy từ test CHUNG. Đối chiếu /mnt/d/Master/Thesis/harness/ac_app_unseen_count.json (app_unseen thật): app_unseen_total=631, sampled=250, with_app=102, distinct_apps=42. Mật độ app/ep 0.77 (chung) vs 0.41 (app_unseen).
2) Chao1 — đếm lại từ bảng apps: f1=22, f2=8 => 42+484/16=72.2. Ngoại suy Colwell (f0=30.25, n=102) tới 257 ep gán-được: ~62; tới 631 ep: ~72. Không ra 150-250.
3) MDE = 3.077*0.362/sqrt(G): G=42 -> 17.2pp; G=72 -> 13.1pp; G=100 -> 11.1pp; G=150 -> 9.1pp; G=200 -> 7.9pp. Xác nhận report/86 dùng G=150 để ra 9.1pp.
4) Phân rã phương sai từ /mnt/d/Master/Thesis/harness/mde_pilot_results.json (n_apps=26, n_steps=91, sd_1arm=0.25612, sd_diff=0.36221): var=0.0656, binom 0.3*0.7/3.5=0.0600, giữa-app=0.0056, sd_between=0.075. Tái lập đúng phép của đòn — nhưng là hiệu hai ước lượng nhiễu.
5) Tự-khai sẵn có — /mnt/d/Master/Thesis/report/86_MDE_pilot_ket_qua.md, mục "Đọc kỹ" điểm 2: "MDE này BẢO THỦ (overestimate): pilot chỉ 2-4 bước/app → điểm per-app nhiễu → SD phồng ... 8-9 pp là cận-trên an toàn"; và "SD-hiệu nền = 0.362 (dùng lại nếu tính lại MDE khi biết G chính xác)".
6) Cờ tạm — report/85_PREREG_v2_LAI.md:19 "[số app test AC ≈ 150-250, phần lớn singleton — chốt chính xác lúc build]"; header file định nghĩa ô ngoặc vuông = điền sau bước đo-nền.
7) Pilot ĐÚNG quần thể — mde_pilot.py dòng ~46 lấy app_unseen từ reece124/android_control (không phải test chung), nên SD=0.362 không dính lỗi nhầm file; chỉ mẫu số G dính.
8) Timestamp: ac_app_unseen_count.json 01:54 < mde_pilot_results.json 02:22 < report/85 02:24 — tác giả ĐÃ có số app_unseen lúc viết, tức đây là sơ suất đối chiếu chứ không phải thiếu dữ liệu.
VIỆC PHẢI SỬA: report/85:19 + :64 thay "≈150-250" bằng "quan sát 42 trên mẫu 250 ep; ước ~62-80 sau gán tay"; report/86 sửa headline 8-9pp -> ~13pp @ G=72 (vẫn dưới cổng 15-20pp).

---

### B15. [VỪA] K2 — toàn bộ 80 màn đến từ MỘT app duy nhất; kết luận lật đổ luận văn dựa trên n_app = 1

- **Trục:** Bốn phép thử K1 / K2 / OCR / VIỆC1 — có bị khái quát quá không
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** CHÍ MẠNG → **sau kiểm chéo:** VỪA

**Vấn đề.** K2 là phép thử đắt giá nhất về mặt hệ quả: nó kết luận teacher gpt-4o-mini bịa ~0-2% (không phải ~¼), qua đó giết đóng góp "lọc bịa", hạ Tier 1 xuống readout phụ và đẩy cả thiết kế sang trục ĐÚNG. Nhưng toàn bộ 80 file cache là của một app (một phần mềm quản lý dự án/chi phí). Không có 30 app, không có 80 app — chỉ một. Thêm nữa, 40 ca "soi tay" quy về 18 chuỗi element khác nhau, trong đó riêng '+' chiếm 15 ca và 13/40 dòng là bản sao y hệt cặp (element, sim). Nghĩa là bằng chứng "20/40 ca kết-oan là icon" thực chất là 3-4 widget riêng biệt của cùng một app được đếm lặp. Cỡ mẫu hiệu dụng gần 1 app / vài widget, không phải 127 bước độc lập. report/74 §Giới hạn chỉ ghi "một-hai miền app" — nói nhẹ hơn sự thật, và tuyệt đối không nêu con số n_app=1.

**Bằng chứng.** `ls harness/dg1_cache/runs | wc -l` = 80; `sed 's/_s[0-9]*.*//' | sort | uniq -c` → "80 app1". k2_results.json: 40 dòng nonvb_detail, mọi trường "screen" đều là app1_sNNN; đếm lại: 18 chuỗi element distinct, Counter đứng đầu ('+',15), ('Project name',4), ('✓',3); 27 cặp (el,sim) distinct → 13 dòng trùng. report/74:50 "Mẫu hẹp: 80 màn, một teacher, một-hai miền app".

**Đề xuất sửa.** Trước khi để K2 gánh bất kỳ quyết định thiết kế nào: chạy lại trên ≥15 app khác nhau của MobileViews (cache cũ không dùng được vì lệch bộ), và báo cáo con số theo cụm-app (macro-per-app) chứ không phải theo bước. Trong mọi văn bản, đổi "80 màn" thành "80 màn của 1 app", và đổi "127 bước" thành "127 bước, 18 tham chiếu element distinct". Nếu không kịp chạy lại, phải hạ K2 từ "bằng chứng" xuống "quan sát thăm dò trên một app" và KHÔNG dùng nó để biện minh cho việc bỏ Tier 1.

**Người phản-bác nói gì.** Mọi quan sát THỰC TẾ của đòn đều đúng và tôi kiểm lại được từng cái: 80/80 file cache là app1 (n_app=1), 40 dòng nonvb chỉ có 18 chuỗi element distinct, '+' chiếm 15, 27 cặp (el,sim) distinct → 13 dòng trùng, và report/74:50 quả thật chỉ ghi "một-hai miền app" chứ không nêu n_app=1. Không có chỗ nào bịa bằng chứng.

NHƯNG luận điểm trung tâm — "kết luận lật đổ luận văn dựa trên n_app=1" — bị bác bởi một sự thật quyết định: con số "~¼ bịa" mà K2 lật ĐỔ CŨNG đến từ đúng bộ app1 đó. CLAUDE.md:157 ghi rõ "~¼ ... CI còn chạm 0 (n nhỏ, 1 app cũ); Bản chính (127 màn/30 app) CHƯA CHẠY (cần API)". Vậy K2 là phép kiểm-lại-trong-cùng-mẫu: nó soi lại đúng output teacher duy nhất tồn tại và thấy "¼" thực chất là kết-oan matcher trên nút icon không nhãn. Bác một claim bằng chính mẫu đã sinh ra claim đó KHÔNG cần tính đại diện ngoài mẫu. Cái K2 không thể làm ở n_app=1 là khẳng định phổ quát "teacher bịa ~0-2% ở mọi miền" — và các file thiết kế TỪ CHỐI khẳng định đó một cách minh thị (report/78:178 và 78:206).

Thêm ba điểm gỡ: (1) provenance app1 ĐÃ được khai ở report/75:68; (2) kết luận hành-động-được của K2 (VH bỏ nhãn icon → matcher kết oan nút thật) được xác nhận ĐỘC LẬP ở quy mô 30 app: k1_results.json n_screens=127, vh_label_coverage=0,624, và OCR chạy 127 màn/3964 nút actionable trên 30 app thật, cùng ra sàn ~20% icon vô nhãn — nên "OCR là fix số 1" đứng trên bằng chứng 30 app, không phải app1; (3) phản ứng với K2 là hạ-vai chứ không xoá: Tier 1 giữ làm readout phụ có đăng-ký-trước báo cả khi null (report/78:19,159), đúng cách xử lý bằng chứng chưa chắc tổng quát. Trục chính mới được biện minh DƯƠNG bởi report/79 (gold step_instructions) và report/86 (MDE 26 app), không phải bởi K2.

Phần còn sống của đòn (nên vá, mức vừa): report/74 nên ghi thẳng n_app=1 thay vì "một-hai miền app" (cụm này đọc ra là nhiều app trong 1-2 miền — nói nhẹ hơn sự thật), và nên báo 40 ca soi tay dưới dạng ~18 widget distinct thay vì 40 quan sát độc lập, vì tỉ lệ "20/40 là icon" đã lan vào CLAUDE.md như một trọng số. Đây là hai dòng sửa tài liệu, không phải lỗi thiết kế — nên hạ từ chi_mang xuống vua.

**Bằng chứng của người kiểm.** KIỂM ĐÚNG (đòn không bịa): `ls harness/dg1_cache/runs | wc -l`=80; `sed 's/_s[0-9]*.*//' | sort | uniq -c` → "80 app1"; questions.json = 80 key, Counter app = {'app1': 80}. k2_results.json: 40 dòng nonvb_detail, apps=Counter({'app1':40}), 35 screen distinct, 18 el distinct, top = ('+',15), ('Project name',4), ('✓',3), 27 cặp (el,sim) distinct → 13 dòng trùng. report/74:50 = "Mẫu hẹp: 80 màn, một teacher, một-hai miền app" (không nêu n_app=1).

BẰNG CHỨNG BÁC:
1. CLAUDE.md:157 — "tỉ lệ bịa bản gốc ~¼ số bước; ... CI còn chạm 0 (n nhỏ, 1 app cũ); Bản chính (127 màn/30 app, kept_screens_final.json) CHƯA CHẠY (cần API)" → claim bị lật cũng là n_app=1; không tồn tại số bịa teacher nào ở quy mô 30 app trong dự án. report/54:325 và 54:502 cũng đã gắn cờ "¼ = quan sát sơ bộ một model, tập ảnh giới hạn"; CLAUDE.md:113 (M4, 2026-07-02) đã ghi "¼ = quan sát sơ bộ 1 model, KHÔNG làm headline-phát-hiện tổng quát" — tức giới hạn này được khai TỪ TRƯỚC K2.
2. report/75:68 — "K2 dùng bộ 80 màn pilot cũ tên `app1_sN`; OCR chạy trên bộ 127 chuẩn" → provenance app1 đã khai.
3. report/78:178 — "K2 chỉ trên 1 miền app (quản-lý-dự-án/chi-phí), 80 màn, không xem được ảnh. 'Teacher bịa ~0' CÓ THỂ KHÔNG TỔNG QUÁT sang app game / thiết-lập-hệ-thống / app nhiều icon-thuần." Lặp ở 78:206 mục (3). Đây là file THIẾT KẾ đã hành động dựa trên K2 — nó tự khai đúng giới hạn mà đòn tố là bị giấu.
4. Cơ chế được xác nhận ở 30 app: harness/k1_results.json → n_screens=127, vh_label_coverage=0,6244, n_pairs=130. report/75 (ocr_coverage_results.json) chạy 127 màn/3964 nút actionable, VH 74%→80% nút cỡ-nút, sàn ~20% icon thuần. dataset_samples/mv_multiapp có 30 app package thật (comxeroprojects, sgbigolive, comabappscutekoalawa...); kept_screens_final.json = 127 màn/30 app.
5. report/78:19,159 — Tier 1 GIỮ làm "readout phụ gần-miễn-phí, báo dù null", không bị xoá. Trục chính mới neo vào report/79 (phát hiện gold step_instructions của AndroidControl) + report/86 (MDE trên 26 app AC), độc lập K2.

---

### B16. [VỪA] Cơ chế gán app vừa tách một app thành nhiều cụm vừa đẻ cụm rác — phá chính giả định độc lập mà thiết kế cluster-bootstrap dựa vào

- **Trục:** TRUNG THỰC BÁO CÁO — đối chiếu prose (report/73-86, 88, CLAUDE.md §0) với code + số thô trong harness/
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** VỪA

**Vấn đề.** Đơn vị thống kê của trục ĐÚNG là per-app, và cluster bootstrap chỉ hợp lệ nếu các cụm độc lập nhau. Nhưng hàm gán app dùng regex bắt "... app" trong goal, và output của nó trong chính kết quả pilot cho thấy: (a) MỘT app bị tách thành NHIỀU cụm — 'The Washington Post' và 'Washington post' là hai cụm riêng, 'Arts & Culture' và 'Art & Culture' riêng, 'NYTimes' và 'Newyork times' riêng; (b) cụm RÁC không phải tên app — 'Knoxville on the CNN', 'Inspire in this', 'On the Pinerest', 'Video Audio', và trong file đếm còn có 'Expert Paper art & Professional Origami Designing steps'. Hai hệ quả ngược chiều nhưng đều xấu: G bị THỔI PHỒNG (làm MDE trông tốt hơn thực — cộng dồn với phát hiện trên), và quan sát của cùng một app thật bị rải vào các cụm khác nhau nên bootstrap coi chúng độc lập → khoảng tin cậy HẸP GIẢ, p-value lạc quan giả. Đây đúng là lỗi mà lựa chọn "cluster theo app" được dựng ra để tránh.

**Bằng chứng.** harness/mde_pilot.py:36 regex `([A-Z][A-Za-z0-9&\.\- ]{1,20}?) app`. harness/mde_pilot_results.json app_scores chứa đồng thời: "The Washington Post":0.25 và "Washington post":0.333; "Arts & Culture":0.25 và "Art & Culture":0.0; "NYTimes":0.333 và "Newyork times":0.25; cùng các cụm rác "Knoxville on the CNN":0.0, "Inspire in this":0.5, "On the Pinerest":1.0. harness/ac_app_unseen_count.json chứa "Expert Paper art & Professional Origami Designing steps":1, "Video Audio":1. Tức trong 26 "app" của pilot có ít nhất 3 cặp trùng thực thể + 3 cụm rác ≈ 6/26 = 23% cụm sai.

**Đề xuất sửa.** Chuẩn hoá tên app (lowercase, bỏ 'the', bỏ dấu, fuzzy-merge) + danh sách trắng tên app hợp lệ; ưu tiên TUYỆT ĐỐI action open_app.app_name và chỉ dùng regex khi có xác nhận tay; loại các ep không gán được app khỏi phân tích cụm thay vì để regex đoán bừa. Báo lại G sau khi gộp — con số này phải là G dùng cho MDE và cho bootstrap.

**Người phản-bác nói gì.** Lỗi CÓ THẬT nhưng mức "nặng" là phóng đại — mọi hệ quả định lượng tôi đo được đều nhỏ, và một mảnh bằng chứng bị quy sai nguồn.

SỐNG: regex gán app đúng là vừa tách app vừa đẻ cụm rác, và tệ hơn họ nêu (thêm 'Utilize the Snapdeal', 'Fairey on the Artsy', 'Faye on the Pinterest', 'Google fit' vs 'Google Fit', 'On the Etsy'/'Artworks on the Etsy' vs 'Etsy'). report/85 §1 chỉ khai ĐỘ PHỦ (~72%, phần thiếu gán tay lúc build), KHÔNG khai CHẤT LƯỢNG của phần đã gán → đây là lỗ chưa được ghi nhận. Nếu để nguyên lúc build thì SE lệch xuống, G lệch lên, đúng chiều họ nói.

BỊ HẠ MỨC vì 4 điểm:
(1) Sai bằng chứng: 'Expert Paper art & Professional Origami Designing steps' dài 55 ký tự, regex chặn capture ở 21 ký tự → KHÔNG THỂ do regex sinh; nó đến từ open_app app_name, tức tên app thật AndroidControl ghi. Gọi nó là "cụm rác do regex" là sai. 'Video Audio' tương tự.
(2) Nhánh open_app (dataset-authoritative) KHÔNG hề tách; toàn bộ biến thể tách đều nằm ở nhánh regex fallback (62/200 ep). Fix = chuẩn hoá/gán tay đúng nhánh đó, không đụng thiết kế.
(3) Hệ quả MDE gần như bằng 0: gộp 4 cặp trùng → SD 0.256→0.267, MDE@G=150 9.1→9.5 pp, ngưỡng cổng là 15-20 pp. Bỏ cụm rác còn LÀM MDE TỐT LÊN (8.0 pp) → luận điểm "rác thổi phồng sức mạnh" ngược chiều trong mẫu này. G thổi phồng 10-18% ⇒ MDE bị hụt ~0.4-0.7 pp.
(4) Luận điểm "phá giả định độc lập" yếu nhất: AC app-unseen gần như toàn singleton (69/93 cụm n=1), Kish n̄=1.67 (thô) vs 2.49 (over-merge cố ý) → deff 1.134 vs 1.299 @ρ=0.2, tức SE hụt ~7% (14% @ρ=0.5). Không phải sai lệch bậc lớn; ρ gần như không có gì để cắn.

Kết: giữ lại như việc-phải-làm trước build (canonicalize tên app + gán tay nhánh regex, khai vào report/85), KHÔNG phải lỗi thiết kế đe doạ trục ĐÚNG.

**Bằng chứng của người kiểm.** KIỂM TRỰC TIẾP:
- harness/mde_pilot.py:36 regex đúng như trích; app_of ưu tiên open_app action rồi mới regex.
- harness/mde_pilot_results.json: xác nhận đủ 3 cặp trùng + 3 cụm rác họ nêu; phát hiện thêm 'Knoxville on the CNN' là cặp thứ 4 tách khỏi 'CNN'.
- Chạy lại app_of trên dataset_samples/androidcontrol_test/ac_test_200ep.json (200 ep): nguồn = open_app 72 / regex 62 / không gán 66. distinct thô 103; chuẩn-hoá bảo thủ 93; over-merge (containment) 84 → G thổi phồng 10-18%. Mọi biến thể tách đều thuộc nhánh regex.
- Ví dụ then chốt: ep goal "Open the Art & Culture app and find an artwork inspired by Emily Carr." có open_app=['Arts & Culture'] → ep này gán ĐÚNG canonical; cụm 'Art & Culture' rời đến từ ep khác không có open_app ⇒ tách chỉ do fallback.
- Đếm ký tự: 'Expert Paper art & Professional Origami Designing steps' = 55 ký tự > trần capture 21 của regex ([A-Z][...]{1,20}?) ⇒ đến từ open_app, là tên app thật, không phải rác regex.
- Tính lại MDE từ mde_pilot_results.json (công thức 3.077*sqrt(2)*SD/sqrt(G) như trong mde_pilot.py): nguyên trạng G=26 SD=0.256 → 9.1 pp @G=150 / 7.9 pp @G=200; sau gộp 4 cặp G=22 SD=0.267 → 9.5 / 8.2 pp; gộp + bỏ 2 cụm rác G=20 SD=0.226 → 8.0 / 6.9 pp. Ngưỡng pre-register (report/85 §6) = 15-20 pp.
- Design effect trên 200 ep: thô G=103 Kish n̄=1.67 deff(ρ=.2)=1.134; over-merge G=84 n̄=2.49 deff=1.299 → SE hụt tối đa ~7% (ρ=.2) / ~14% (ρ=.5). 69/93 cụm là singleton.
- report/85_PREREG_v2_LAI.md:19 đã ghi "phủ ~72% ... phần còn lại gán tay/GCS lúc build" + "[số app test AC ≈ 150-250 — chốt chính xác lúc build]" (placeholder ngoặc vuông) ⇒ G cuối và cách gán đã được hoãn có chủ đích sang lúc build; G=26 của pilot không đi vào phân tích.

---

### B17. [VỪA] GuideMe (CHI 2026) đã chiếm đúng tác vụ 'sinh hướng dẫn nhiều bước cho NGƯỜI từ screenshot + câu hỏi' — vòng scoop cũ bỏ sót

- **Trục:** TÍNH MỚI + CHỐNG SCOOP
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** VỪA

**Vấn đề.** CLAUDE.md chốt 19/7 đóng góp model = 'TÁC VỤ MỚI: model ĐẦU TIÊN sinh hướng dẫn nhiều bước cho người đọc từ 1 ảnh + câu hỏi'. Nhưng GuideMe (Fang, Zhang, Ni, Hui, Wang — Proceedings of CHI 2026, dl.acm.org/doi/10.1145/3772318.3791448) là hệ thống VLM: người dùng (người già) hỏi câu hỏi trong app, hệ thống chụp screenshot + lấy UI element info, VLM phân tích, sinh hướng dẫn từng bước kèm highlight in-situ để người làm theo. Tức là ở MỨC TÁC VỤ, 'sinh hướng dẫn nhiều bước cho người từ ảnh+câu hỏi+thông tin UI' đã được công bố tại venue HCI hàng đầu. Cái còn sống cho luận văn chỉ là: (a) TRAIN model nhỏ mở chuyên biệt (GuideMe prompt VLM lớn qua API), (b) đánh giá định lượng kép (GuideMe là system+user-study, không có metric gold/faithfulness). Nếu bài FAIR viết 'first model to generate multi-step instructions for humans' mà không trích GuideMe, reviewer HCI-aware sẽ đập ngay. report/82 và report/57 đều KHÔNG có GuideMe (grep 0 hit); report/82 mục 'Chỗ chưa tìm hết' tự khai 'chưa quét CHI/UIST' — lỗ tự khai đó hoá ra chứa đúng quả mìn.

**Bằng chứng.** Search 'GuideMe VLM smartphone learning older adults' → dl.acm.org/doi/10.1145/3772318.3791448 (Proceedings of the 2026 CHI Conference, Barcelona 4/2026): 'GuideMe can capture UI element information... analyze the screenshot... provide instructions via in-situ highlighting... follow step-by-step instructions'. Đối chiếu: grep -i guideme report/82_verify_tinh_moi_scoop.md report/57_related_work.md → 0 kết quả. Lưu ý: chưa xác nhận được full-paper hay LBW/EA (ACM 403, DOI prefix 3772318 chưa đối chiếu được).

**Đề xuất sửa.** TRƯỚC khi viết related work FAIR/gặp thầy: (1) lấy full-text GuideMe, xác định full-paper hay extended abstract; (2) hạ claim 'tác vụ mới/model đầu tiên' xuống 'model nhỏ mở ĐẦU TIÊN được TRAIN cho tác vụ này + khung đánh giá định lượng kép đầu tiên' — GuideMe trở thành trụ biện minh nhu-cầu (HCI đã cần tác vụ này) thay vì bị coi là scoop; (3) thêm GuideMe + Synapse (IMWUT 2022, dl.acm.org/doi/10.1145/3550321) + ExplorAR (2508.01282) + DigitalCoach (arXiv 2606.31980) vào theme T1b của report/57.

**Người phản-bác nói gì.** Paper CÓ THẬT (đã verify độc lập): GuideMe, Fang/Zhang/Ni/Hui/Wang, Proceedings of CHI '26, DOI 10.1145/3772318.3791448, trang publication Pan Hui liệt kê dạng full paper (giải quyết nghi ngờ LBW của chính người ra đòn theo hướng bất lợi cho repo). grep -ri guideme report/ = 0 hit, đúng. Nên đòn SỐNG ở tầng citation: bắt buộc phải trích GuideMe trong related-work FAIR, và dòng CLAUDE.md:27 'model đầu tiên sinh hướng dẫn nhiều bước cho người đọc từ 1 ảnh+câu hỏi (mọi model GUI khác sinh action-cho-máy)' giờ sai ở mức tác vụ, phải hạ về 'model được HUẤN LUYỆN chuyên biệt đầu tiên'.

NHƯNG mức 'nặng' phóng đại, hạ xuống 'vừa' vì 5 lý do kiểm được:
(1) Trục CHI KHÔNG phải điểm mù: report/papers/askease_chi2026.md đã có AskEase — CHI 2026, DOI 10.1145/3772318.3790661, CÙNG proceedings (prefix 3772318 giống hệt) — và tự dán nhãn 'bài gần nhất trên trục sinh hướng dẫn cho người → rủi ro novelty CAO NHẤT, phải phân định'. Lập luận phân định (LIVE runtime vs ảnh tĩnh; user-study vs no-gold VH metric) đã viết sẵn, áp nguyên xi cho GuideMe. Đây là thêm instance vào lớp đe doạ đã nhận diện, không phải mìn chưa biết.
(2) Đòn đánh vào claim repo ĐÃ TỰ CẤM: report/82 mục 'KHÔNG nên claim' ghi rõ ❌ 'Quy trình sinh hướng dẫn GUI cho người là mới hoàn toàn' (từ 19/7). Kịch bản 'nếu FAIR viết first model...' là điều pre-registration đã cấm.
(3) Bản thảo nộp KHÔNG chứa overclaim: grep -in 'first|đầu tiên' report/57_related_work.md = 0 hit. Câu định vị thật (57:151) neo vào 'no source document and no gold tutorial' — GuideMe không bác được vì nó CÓ nguồn ngữ cảnh ngoài (UI element info + clarifying dialogue) và KHÔNG có gold/faithfulness metric. Overclaim chỉ nằm ở dòng nhật ký nội bộ CLAUDE.md:27.
(4) Không chạm trục tính-mới phòng-thủ-được nào của report/82: (a) reference-free bằng VH, (b) AndroidControl step_instructions làm TARGET SINH, (c) tổ hợp. GuideMe không train model, không dataset, không metric, không đụng AndroidControl; đóng góp là tương tác (floating bubble, in-situ hollow highlight), đo bằng eye-tracking + số click sai. Hai trụ luận văn (model train được + cặp thước đánh giá + chương đo-lường K1/K2/OCR/VIỆC1) nguyên vẹn.
(5) Input contract khác thật: CLAUDE.md §1 = 1 ảnh TĨNH + 1 câu hỏi, không đối thoại; GuideMe bắt buộc vòng clarifying question + ngữ cảnh app đang chạy + overlay live.

Chi phí khắc phục = một đoạn phân định + sửa một câu nội bộ, chính là việc report/82 §'Chỗ chưa tìm hết' đã lên lịch. Không đổi thiết kế, không đổi pre-registration (report/85), không đổi thí nghiệm.

**Bằng chứng của người kiểm.** WebSearch + WebFetch panhui.people.ust.hk/publications.html → xác nhận GuideMe: A VLM-Based System Assisting Independent Smartphone Learning for Older Adults, CHI '26 Barcelona 4/2026, DOI 10.1145/3772318.3791448, dạng full paper; nội dung = floating bubble + clarifying question + in-situ hollowed highlight, đo bằng eye-tracking + số click sai (KHÔNG train model, KHÔNG metric faithfulness/gold). dl.acm.org trả 403 nên không đọc được full-text.
grep -ril 'guideme|3791448|3772318' report/ harness/ CLAUDE.md → GuideMe 0 hit; nhưng prefix 3772318 hit tại report/papers/askease_chi2026.md:3-4 (AskEase, CHI 2026, DOI 10.1145/3772318.3790661, cùng proceedings) + report/_archive/42:84 + report/_archive/45:51,116,272 (đã verify venue).
report/papers/askease_chi2026.md:5 — 'bài gần nhất trên trục sinh hướng dẫn cho người → rủi ro novelty cao nhất, phải phân định (§9, §12)'; §'Điểm cần biết' đã có sẵn 3 luận cứ phân định (input LIVE vs ảnh tĩnh; user-study vs no-gold VH; không hậu-kiểm VH).
report/82_verify_tinh_moi_scoop.md:33-36 — 'KHÔNG nên claim: ❌ Quy trình sinh hướng dẫn GUI cho người là mới hoàn toàn'; :28-31 — 3 trục phòng-thủ-được (VH reference-free / AndroidControl step_instruction làm target sinh / tổ hợp); :51 — TODO tự khai 'chưa quét CHI/UIST'.
grep -in 'first|đầu tiên' report/57_related_work.md → 0 hit; report/57:151 dùng 'differs in kind ... no source document and no gold tutorial'.
CLAUDE.md:27 — chỗ duy nhất chứa overclaim 'model đầu tiên SINH HƯỚNG DẪN NHIỀU BƯỚC CHO NGƯỜI ĐỌC từ 1 ảnh+câu hỏi'.

---

### B18. [VỪA] G≈150-250 và MDE 8-9pp lấy từ ĐẾM SAI SPLIT; trên đúng app_unseen split, độ đa dạng app thấp hơn hẳn và cluster pilot chứa rác trích xuất

- **Trục:** Đủ ngưỡng luận văn thạc sĩ? + logic đổi hướng + khả thi (giám khảo hoài nghi, tự kiểm số trước khi đọc report)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** VỪA

**Vấn đề.** Report/85 §1 ghi '~114 app distinct chỉ trong 200 ep, phần lớn singleton → G≈150-250' và report/86 kết luận 'MDE 8-9pp @ G=150-200 → đủ lực'. Tôi tái lập: con số ~114 (tôi đếm ra 103 distinct, 67% gán được) đến từ ac_test_200ep.json = mẫu test CHUNG, KHÔNG phải app_unseen split. File đếm trên ĐÚNG split trục ĐÚNG sẽ dùng (ac_app_unseen_count.json, 250/631 ep sampled) cho bức tranh khác hẳn: chỉ 41% gán được app (không phải '~72%' như 85 ghi), 42 distinct/102 ep gán được, và KHÔNG 'phần lớn singleton' mà tập trung mạnh (Pinterest 14, Arts&Culture 8, CNN 6, Guardian 6 — split app_unseen là cụm app nghệ thuật/tin tức hẹp). Ngoại suy 631 ep → G gán-được cỡ 60-90 → MDE = 3.077×0.362/√G ≈ 12.5-14.4pp, không phải 8-9pp (vẫn dưới ngưỡng 15-20 nhưng sát hơn nhiều); còn muốn giữ G lớn thì phải đếm 59% ep không-gán-được thành singleton — phá giả định độc lập cluster (2 ep cùng app không tên bị đếm là 2 cluster). Thêm: 26 'app' trong mde_pilot_results.json chứa rác regex — 'Knoxville on the CNN' vs 'CNN', 'On the Pinerest', 'Inspire in this', 'Washington post' vs 'The Washington Post', 'Art & Culture' vs 'Arts & Culture', 'NYTimes' vs 'Newyork times' — cùng app bị tách thành 2 cluster 'độc lập' → cả SD lẫn G của pilot đều nhiễu.

**Bằng chứng.** harness/ac_app_unseen_count.json: with_app=102/250 (41%), distinct=42, Pinterest=14; tôi chạy lại app_of() trên ac_test_200ep.json: 134/200 gán (67%), 103 distinct, G-nếu-singleton=169; mde_pilot_results.json app_scores chứa 'Knoxville on the CNN', 'On the Pinerest', 'Inspire in this'; mde_pilot.py:36 regex trích goal; report/85:19 vs report/86:22 đối chiếu

**Đề xuất sửa.** Gán app cho toàn bộ 631 ep app_unseen bằng tay (1-2 ngày, khả thi) hoặc từ metadata AC gốc TRƯỚC khi khoá thống kê; tính lại G thật và MDE với G đó; sửa report/85 §1 (72%→41% trên đúng split; bỏ 'phần lớn singleton'); nếu G thật <60 thì cân nhắc chuyển sang phân tích per-episode với wild-cluster theo app + khai under-coverage

**Người phản-bác nói gì.** Đòn ĐÚNG ở lỗi nguồn và lỗi rác regex, nhưng SAI ở toàn bộ phần định lượng thay thế, và kết luận thiết kế không lật.

ĐỨNG (phải sửa report):
1. ac_test_200ep.json KHÔNG phải app_unseen. Tôi đối chiếu với trường app_unseen của reece124/android_control test: chỉ 79/200 episode nằm trong app_unseen. Vậy con số "~114 distinct/200 ep" ở report/85 §1 quả thật lấy từ mẫu test CHUNG → suy ra G≈150-250 là ngoại suy sai pool. Đây là lỗi thật, phải sửa.
2. Rác trích xuất trong mde_pilot_results.json có thật, đúng nguyên văn: "Knoxville on the CNN" vs "CNN", "On the Pinerest", "Inspire in this", "Washington post" vs "The Washington Post", "Art & Culture" vs "Arts & Culture", "NYTimes" vs "Newyork times". Cùng app bị tách cụm → G phồng, SD nhiễu. Lỗi thật.
3. app_unseen đúng là cụm miền hẹp (nghệ thuật/tin tức/thiên văn) chứ không "CỰC đa dạng" như report/85 mô tả — mẫu test chung có Maps/Amazon/Etsy/Kitchen Stories, app_unseen thì không.

BỊ BÁC (phần định lượng của đòn sai, lệch theo hướng phóng đại):
4. "Chỉ 41% gán được, không phải 72%" — SAI. Tôi tải mới 260 episode ngẫu nhiên từ CHÍNH app_unseen (wangyuanlei/android_control_test) rồi chạy đúng app_of() của mde_pilot.py: 198/260 = 76.2% gán được, 88 distinct, 46 singleton. Con số 41% của họ đến từ harness/ac_app_unseen_count.json — file trung gian CŨ của chính tác giả (mtime 01:54, trước report/85 lúc 02:24), rõ ràng chỉ đếm nhánh open_app mà bỏ fallback regex-goal: mẫu của tôi có đúng 102/260 ep có action open_app, khớp gần như hệt "102/250" của họ. Họ lấy một artifact hỏng của tác giả làm chuẩn để đánh lại số hoàn chỉnh. "~72%" ở report/85 là ĐÚNG, thậm chí bảo thủ.
5. "42 distinct/102 gán được, không phần lớn singleton" — cùng một artifact hỏng. Số thật: 88 distinct/198, 46/88 = 52% là singleton. Tập trung có thật (Arts&Culture 12, DeviantArt 9, Pinterest 8) nhưng không tới mức họ vẽ.
6. "G ≈ 60-90 → MDE 12.5-14.4 pp" — SAI. Ngoại suy Chao lên 631 ep: G ≈ 125 (thô) / ≈ 94 (sau khi chuẩn hoá đúng phần rác tên mà họ nêu). MDE = 3.077×0.362/√G = 10.0-11.5 pp, không phải 12.5-14.4.
7. "Muốn giữ G lớn phải đếm 59% ep không-gán-được thành singleton → phá độc lập cụm" — tiền đề sập: chỉ 24% không gán được, và report/85 §1 đã ghi sẵn "phần còn lại gán tay/GCS lúc build", không hề giả định singleton.

HỆ QUẢ THẬT: report/85 §1 phải sửa G từ "150-250, phần lớn singleton" xuống ~95-130 và bỏ chữ "CỰC đa dạng"; report/86 phải sửa MDE 8-9 pp → 10-11.5 pp; mde_pilot cần chuẩn hoá tên app rồi tính lại SD. Nhưng ngưỡng nguy hiểm đã đăng-ký-trước là 15-20 pp, MDE mới vẫn dưới ngưỡng → cổng "trục ĐÚNG đủ lực" KHÔNG lật, không phải đổi split, không phải bỏ thiết kế. Thêm nữa report/86 §2 đã tự khai SD=0.362 là phồng do pilot chỉ 2-4 bước/app → còn đệm thật. Vì vậy: lỗi tài liệu/số liệu cần sửa, không phải lỗi thiết kế → hạ từ "nặng" xuống "vừa".

**Bằng chứng của người kiểm.** TỰ CHẠY LẠI (~/.venvs/thesis/bin/python, không gọi OpenAI):

[1] Đối chiếu split: load_dataset('reece124/android_control', split='test', streaming=True) → row['app_unseen'] = 631 id. Giao với episode_id trong dataset_samples/androidcontrol_test/ac_test_200ep.json → CHỈ 79/200 nằm trong app_unseen. ⇒ xác nhận lỗi nguồn của đòn.

[2] Tách 200 ep local theo split, chạy harness/mde_pilot.py:app_of():
  - 79 ep app_unseen: 57 gán (72%), 42 distinct, 30 singleton — top: Arts&Culture 4, CNN 3, DailyArt/SkyView/Sketchar/Flipsnack/Pinterest 2.
  - 121 ep còn lại (không app_unseen): 77 gán (64%), 62 distinct — top: Maps 5, Amazon 4, Kitchen Stories 3, Etsy 2.
  ⇒ hai miền khác hẳn (xác nhận ý "cụm hẹp"), nhưng tỉ lệ gán app_unseen = 72%, không phải 41%.

[3] Tải MỚI 260 episode json ngẫu nhiên (seed 123) từ wangyuanlei/android_control_test, chỉ lấy id thuộc app_unseen (631/631 có file json). Chạy app_of():
  - gán được 198/260 = 76.2%
  - distinct = 88, singleton = 46 (52%)
  - top: Arts & Culture 12, DeviantArt 9, Pinterest 8, Artier 8, CNN 8, Guardian 7, NYTimes 6, Art & Culture 5, Stellarium 4, Reuters 4, In the Pinterest 4, Flipboard 4
  - số ep CÓ action open_app = 102/260 ⇒ khớp gần hệt "with_app=102/250" trong ac_app_unseen_count.json ⇒ chứng minh file đó chỉ đếm nhánh open_app, bỏ fallback regex.

[4] Ngoại suy richness (Chao1 + Chao extrapolation tới 631 ep):
  - thô: f1=46, f2=21, Chao1=138.4, extrap@631ep = 124.6 → MDE = 100×3.077×0.362/√125 = 10.0 pp
  - sau chuẩn hoá tên (gộp "Art & Culture"→"Arts and Culture", "In the Pinterest"→"Pinterest", "Newyork times"→"NYTimes", "Washington post"→"The Washington Post"...): distinct 71, f1=33, f2=19, Chao1=99.7, extrap@631ep = 94.1 → MDE = 11.5 pp
  ⇒ khoảng thật 10.0-11.5 pp, không phải 12.5-14.4 pp của đòn, cũng không phải 8-9 pp của report/86.

[5] Đọc file gốc:
  - harness/ac_app_unseen_count.json: {app_unseen_total:631, sampled:250, with_app:102, distinct_apps:42, Pinterest:14, Arts & Culture:8, CNN:6, Guardian:6}; singleton = 22/42. mtime 2026-07-19 01:54 — TRƯỚC report/85 (02:24) ⇒ artifact trung gian của chính tác giả, không phải bằng chứng độc lập.
  - harness/mde_pilot_results.json: n_apps=26, mean=0.3013, sd_1arm=0.2561, sd_diff=0.3622, n_steps=91; app_scores chứa đúng các tên rác đòn nêu (kiểm verbatim: "Knoxville on the CNN" 0.0 vs "CNN" 0.25; "On the Pinerest" 1.0; "Inspire in this" 0.5; "Washington post" 0.333 vs "The Washington Post" 0.25; "Art & Culture" 0.0 vs "Arts & Culture" 0.25; "NYTimes" 0.333 vs "Newyork times" 0.25).
  - harness/mde_pilot.py:36 app_of() — regex r"\b(?:the |using |on |open )?([A-Z][A-Za-z0-9&\.\- ]{1,20}?) app\b", đúng là nguồn rác.
  - harness/mde_pilot.py:47 — pilot lấy id từ app_unseen split (đúng split), nên SD nền KHÔNG bị lỗi sai-split, chỉ bị lỗi rác tên.
  - report/85 §1: "~114 app distinct chỉ trong 200 ep, phần lớn app 1-2 ep → [số app test AC ≈ 150-250]"; "phủ ~72% ep trên mẫu 200; phần còn lại gán tay/GCS lúc build".
  - report/86: bảng MDE + dòng "split app_unseen thật có G ~150-250 app (report/85 §1) → MDE thực ≈ 8-9 pp"; §2 tự khai MDE bảo thủ vì pilot 2-4 bước/app.
  - report/85 §6/§4: ngưỡng nguy hiểm pre-register = 15-20 pp.
  - chạy lại app_of() trên toàn 200 ep: 134/200 gán (67%), 103 distinct, 81 singleton ⇒ con số "~114 / ~72%" trong report/85 cũng lệch nhẹ so với chính file 200ep (103 / 67%).

---

### B19. [NHẸ] Kế hoạch 'hiệu chỉnh backstop bge-m3 khi có output model thật' = chỉnh thước trên chính dữ liệu đánh giá, sau khi đã đăng-ký-trước

- **Trục:** THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, metric_v1_results.json, mde_pilot.py, report/84, report/85)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NHẸ

**Vấn đề.** Về nguồn gốc con số 0.85: nó được đặt tiên nghiệm với lý lẽ 'backstop cao, chỉ cứu synonym thật' (metric_v1_validate.py:15) và nhất quán với kết luận K1 rằng không ngưỡng đơn nào tách được — nên bản thân 0.85 KHÔNG có dấu hiệu bị dò theo kết quả. Vấn đề nằm ở kế hoạch: report/84:44 và report/85:84 đều ghi sẽ 'hiệu chỉnh backstop / hạ nhẹ ngưỡng / thêm từ-điển-loại-nút KHI CÓ OUTPUT MODEL THẬT'. Đó chính là tinh chỉnh tham số của thước sau khi nhìn dữ liệu đánh giá, trong một thiết kế đã đóng băng ngưỡng — đúng thứ mà pre-registration sinh ra để ngăn. Nếu làm vậy, mọi CI và mọi phán quyết PASS/NULL mất hiệu lực danh nghĩa.

**Bằng chứng.** harness/metric_v1_validate.py:15 (TAU_BGE=0.85, comment). report/84:44 ('CẦN output model thật để hiệu chỉnh'). report/85:84 ('hiệu chỉnh khi có output model'). report/85:2 ('KHÔNG sửa sau commit').

**Đề xuất sửa.** Nếu cần hiệu chỉnh backstop, hiệu chỉnh trên một tập DEV tách riêng (app không nằm trong test split, hoặc output của teacher trên train-split), khoá lại, rồi mới chạy test. Ghi rõ vào report/85 rằng backstop được hiệu chỉnh trên dev nào, ngày nào, commit nào.

**Người phản-bác nói gì.** Đòn còn một lõi thật rất nhỏ (câu văn ở report/85 §8 không nói rõ sẽ hiệu chỉnh trên dữ liệu NÀO), nhưng ba trụ chính của nó đều bị bác bằng file và bằng số.

(1) MÔ TẢ SAI BẰNG CHỨNG. Đòn gọi report/85:84 là "kế hoạch". Nó không nằm ở mục kế hoạch: nó là dòng số 2 của §8 "RỦI RO KHAI TRƯỚC (đưa vào luận văn)" — một hạn chế tự khai để in vào luận văn, nằm cạnh 5 rủi ro khác cùng loại. Tương tự report/84:44 nằm dưới đề mục "Hoài nghi còn lại (khai thẳng, để chỉnh sau)". Khai hạn chế của thước ≠ cam kết dò tham số trên tập đánh giá.

(2) TIỀN ĐỀ "NGƯỠNG ĐÃ ĐÓNG BĂNG" SAI Ở ĐÚNG THAM SỐ ĐANG BÀN. grep report/85 cho "0.85", "TAU", "J_MATCH", "0.5" → KHÔNG khớp dòng nào. TAU_BGE=0.85 chưa bao giờ được đăng-ký-trước. Cái được đóng băng ở §4 là NGƯỠNG HÀNH VI của thước (detection ≥0.90, FP ≤0.10, AUC ≥0.80) — và chính §4 viết rõ: "phải chạy lại trên config cuối… chạy lại trên parser cuối + validate bộ-trích P/R khi có output model", §9 xếp thứ tự "chạy lại bơm-lỗi trên config cuối → commit → SAU ĐÓ mới build/train/eval". Nghĩa là: chỉnh nội-tham-số rồi phải qua lại cổng đã đóng băng chính là QUY TRÌNH ĐƯỢC THIẾT KẾ, không phải vi phạm nó. Đòn nhầm "tham số nội bộ của thước" với "ngưỡng phán quyết".

(3) "MỌI CI VÀ PHÁN QUYẾT PASS/NULL MẤT HIỆU LỰC" — phóng đại, bác bằng số. Tôi quét TAU_BGE từ 0.50→0.95 (chạy lại metric_v1_validate trên 185 ep, bge-m3 local): AUC = 1.000 ở TẤT CẢ giá trị; FP-paraphrase = 0.000 ở tất cả; coverage clean và paraphrase phẳng tuyệt đối 1.000. Headline coverage trên ca target_error chỉ nhúc nhích 0.860→0.846 giữa 0.70 và 0.95. Trong đúng khoảng mà rủi ro tự khai nói tới ("hạ nhẹ ngưỡng", tức 0.85→0.80/0.75), thước gần như TRƠ. Một tham số không đổi được cổng nào và dịch headline ≤1.4pp không thể "làm mất hiệu lực mọi CI".

(4) LÝ LẼ THIẾT KẾ đòn bỏ qua: thước áp GIỐNG HỆT lên Student và Teacher-BASE trên CÙNG split, headline là HIỆU-SỐ (report/85 §3, §7). Backstop nghiêm quá thì bóp cả hai nhánh; nó không phải cần gạt sinh ra Δ dương. Kênh rò duy nhất là student paraphrase nhiều hơn teacher — đòn không nêu kênh này, và với AUC/FP trơ như trên thì độ lớn cũng không có.

(5) DỰ ÁN ĐÃ CÓ TIỀN LỆ TÁCH DỮ LIỆU HIỆU CHỈNH KHỎI DỮ LIỆU ĐÁNH GIÁ: report/56:49 định nghĩa Δ_train "đo trên 18 TRAIN-app thay vì 12 TEST-app", đúng cùng công thức cùng điều kiện. Thiết kế có train-split AC + 18 train-app MV để lấy output model mà không đụng 631-ep app-unseen. Đòn giả định phương án xấu nhất ("chỉnh trên chính dữ liệu đánh giá") mà không có dòng nào trong repo nói vậy.

CÒN LẠI GÌ THẬT: câu ở report/85 §8-2 không ghi rõ "hiệu chỉnh trên train-split, không đụng app-unseen", và không ghi rằng sau khi chỉnh phải chạy lại cổng §4 rồi commit lại. Đó là một lỗ TÀI LIỆU, sửa bằng một dòng — không phải lỗi thiết kế, không phải vi phạm đã xảy ra (chưa có output model nào tồn tại). Vì vậy hạ từ "nặng" xuống "nhẹ".

TỰ KIỂM (không bao che): quét TAU của tôi dùng perturbation tổng hợp giữ nguyên từ-lõi → Jaccard=1 nên bge hầu như không kích hoạt, đó chính là lý do TAU trơ. Trên output model thật có từ đồng nghĩa, tham số sẽ có sức nặng hơn con số của tôi. Nhưng điều đó cắt cả hai chiều: bên buộc tội cũng không chứng minh được độ lớn, mà họ mới là bên phải chứng minh "mọi CI mất hiệu lực".

**Bằng chứng của người kiểm.** - grep TAU/0.85/J_MATCH trên /mnt/d/Master/Thesis/report/85_PREREG_v2_LAI.md → KHÔNG có dòng nào. Tham số 0.85 chưa từng được pre-register; chỉ TAU_BGE=0.85 tồn tại ở harness/metric_v1_validate.py:15.
- report/85_PREREG_v2_LAI.md:84 nằm trong "## 8. RỦI RO KHAI TRƯỚC (đưa vào luận văn)" (mục bắt đầu dòng ~80), là 1 trong 6 rủi ro tự khai — KHÔNG phải mục kế hoạch. report/84 dòng tương ứng nằm dưới "## Hoài nghi còn lại (khai thẳng, để chỉnh sau)".
- report/85 §4: "Cổng cứng: rớt AUC≥0.80 trên config cuối → DỪNG, sửa thước, KHÔNG train. (Synthetic đã qua; chạy lại trên parser cuối + validate bộ-trích P/R trên tập gán-tay khi có output model.)" — chỉnh-rồi-chạy-lại-cổng là quy trình được viết sẵn.
- report/85 §9: "1. …chạy lại bơm-lỗi trên config cuối → commit file này. 2. Pilot đo-nền → điền [MDE] → commit lần 2. 3. SAU đó mới build data / train / eval."
- report/85:3 (điều khoản freeze) liệt kê ngoại lệ là các ô [___] "KHÔNG lộ hướng hiệu ứng" — nhất quán với việc ngưỡng phán quyết mới là thứ bị khoá.
- report/56_*.md:49 — Δ_train "đo bằng ĐÚNG cùng công thức + ĐÚNG cùng điều kiện tắt-VH như Δ_test, chỉ khác là tính trên 18 TRAIN-app thay vì 12 TEST-app" → tiền lệ tách dữ liệu hiệu chỉnh khỏi test.
- git: report/85_PREREG_v2_LAI.md đã tracked & clean, commit b5a6b29.
- CHẠY LẠI (local, bge-m3 ollama, 185 ep, seed 20260719) quét TAU_BGE — scratchpad/sweep.py:
  TAU   AUC   det_te  fp_pp  cov_clean cov_te  cov_pp
  0.50  1.000 0.611   0.000  1.000     0.950   1.000
  0.60  1.000 0.919   0.000  1.000     0.889   1.000
  0.70  1.000 0.995   0.000  1.000     0.860   1.000
  0.80  1.000 0.995   0.000  1.000     0.847   1.000
  0.85  1.000 1.000   0.000  1.000     0.846   1.000
  0.95  1.000 1.000   0.000  1.000     0.846   1.000
  → AUC và FP bất biến trên toàn dải; cổng §4 (AUC≥0.80, FP≤0.10) qua ở mọi giá trị; detection≥0.90 từ 0.60 trở lên. Headline dịch ≤1.4pp trong dải 0.70-0.95.
- harness/metric_v1_validate.py:71 step_match: điều kiện "ts >= J_MATCH*0.999" (0.5) đã bao trùm "ts >= TAU_BGE" (0.85) → clause TAU thứ hai dư; TAU chỉ gác việc bge có được thay Jaccard hay không, giải thích vì sao tham số trơ.

---

### B20. [NHẸ] Ngưỡng 15-20 pp là CƠ CHẾ CHỮA CHÁY của trục khác, bị bê sang làm cổng đậu/rớt cho trục ĐÚNG

- **Trục:** THỐNG KÊ + LỰC MẪU (MDE trục ĐÚNG, wild-cluster bootstrap vs exact sign-flip, đa phép so sánh)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NHẸ

**Vấn đề.** Truy được nguồn: đây là quy tắc "nếu MDE quá tệ thì đổi split 18/12 → 15/15" viết cho trục MobileViews G=12 cố định. Ở trục AndroidControl, biện pháp 15/15 vô nghĩa, nên ngưỡng mất hết ý nghĩa vận hành — nó bị dùng như thể là tiêu chí hợp lệ khoa học.

**Bằng chứng.** report/56_PREREG_MODEL.md:65 — "nếu MDE thật > 15–20 điểm phần trăm → tăng split lên 15/15 TRƯỚC khi khoá ngưỡng"; §6 dòng 60 định nghĩa MDE với df=11, √12 = đúng trục MobileViews. report/85:67 và report/86:7/33 tái dụng cùng con số làm cổng cho trục AC. NGOÀI RA: áp chính SD pilot (0.362) vào đúng trục mà ngưỡng được viết cho (G=12) → MDE = 32,2 pp, RỚT ngưỡng gấp đôi — không report nào nhắc.

**Đề xuất sửa.** Công bằng mà nói: ngưỡng KHÔNG chọn sau khi biết MDE — report/56 commit 2c84ce8 ngày 2026-07-12, pilot chạy 2026-07-19 (git log). Điểm này sạch, nên nói rõ để thủ. Nhưng phải (a) khai rằng ngưỡng vốn thuộc trục khác, (b) đặt một ngưỡng có căn cứ riêng cho trục ĐÚNG (hiệu bao nhiêu pp thì mới đáng gọi là đóng góp model?), (c) ghi nhận SD pilot làm trục TRUNG THỰC rớt ngưỡng.

**Người phản-bác nói gì.** Lõi sự thật đứng: 15-20pp thật sự ra đời ở report/53:356 + report/56:65 gắn với biện pháp 15/15 và công thức df=11/√12 của trục MobileViews, rồi được tái dụng ở report/85:67, report/86:7/33, report/88:146 cho trục AC. Nhưng ba lớp làm nhẹ đòn: (1) Đảo nhân quả — report/54:446 định nghĩa 15-20pp là ngưỡng "kính mờ tới mức chắc chắn ra null bất kể sự thật", tức phát biểu về độ phân giải cần có trên một thước tỉ-lệ 0-1, axis-agnostic; 15/15 chỉ là hệ quả. Ở AC mệnh đề SAI (MDE=9pp) nên biện pháp không kích hoạt — biện pháp không áp dụng được không làm tiền đề mất nghĩa. (2) Ngưỡng KHÔNG chịu lực: cổng go/no-go đăng-ký-trước cho trục ĐÚNG là report/79:51/64 ("không suy biến sàn-0 + phủ bước đủ cao"), pilot qua bằng teacher=30%, không bằng 15-20pp; report/86 báo MDE tuyệt đối kèm bảng G đầy đủ. Xoá câu "dưới 15-20" thì thiết kế không đổi, và 8-9pp cách ngưỡng đủ xa để kết luận bền với mọi ngưỡng hợp lý (10-12pp vẫn qua) — người ra đòn không lập luận ngưỡng đúng phải <9pp. (3) Đã tự phát hiện: report/89:29 ghi nguyên văn "15-20 ở đâu ra?" và PHAN_BIEN_PROMPT.md:26 chủ động mời đánh chỗ này. Phần "NGOÀI RA" (32,2pp) phải GẠCH vì sai phạm trù: SD=0.362 đo trên điểm-đúng teacher so gold step_instruction của AC (harness/mde_pilot.py:107-113), trong khi trục MV đo f=1−bịa/nhắc-nút so VH (report/85:57) — thước khác, phương sai khác; report/85:67 CỐ Ý để trống ô MDE MobileViews chờ pilot riêng nên cáo buộc "không report nào nhắc" là đọc chỗ-trống-có-chủ-ý thành chỗ-giấu; so sánh MV lại là cặp trong cùng app còn √2×SD giả định độc lập (report/56:60 khai rõ là cận trên thận trọng); và report/56 §8 điểm 2 đã khai công thức là xấp xỉ liên tục kiểu Julious, KHÔNG phải ngưỡng chính xác của exact sign-flip — đúng phép kiểm trục MV dùng (report/85:65). Dư lượng còn lại: một con số ad-hoc thiếu trụ trích dẫn dùng làm mốc tu từ trong văn bản đăng-ký-trước — lỗ biện minh/trình bày, không phải lỗi thiết kế, đã nằm trong danh sách phải vá. Hạ nang → nhe.

**Bằng chứng của người kiểm.** report/56_PREREG_MODEL.md:60-65 (công thức df=11/√12 + quy tắc 15/15; §8 điểm 2 khai "xấp xỉ liên tục kiểu Julious, KHÔNG phải ngưỡng chính xác của exact sign-flip"; §6 khai SD-hiệu là "cận trên thận trọng" giả định độc lập); report/53_ke_hoach_build_model.md:356 (nguồn gốc 15-20pp, nêu với SD giả định 0.15, dạng "cân nhắc"); report/54:446/570/607/998 (định nghĩa ngưỡng = "kính mờ tới mức chắc chắn null bất kể sự thật" — phát biểu về độ phân giải, không về MobileViews); report/85_PREREG_v2_LAI.md:67 (tái dụng ngưỡng; ĐỒNG THỜI để trống có chủ ý "[MDE trục trung thực MobileViews = ___ pp] ← điền khi pilot trung thực"), :57 (trục MV đo f=1−bịa/nhắc-nút — thước khác AC), :64-65 (AC dùng wild-cluster bootstrap G lớn, MV dùng exact sign-flip 2^12); report/86_MDE_pilot_ket_qua.md:7/13-25/33 (SD per-app 0.256 → SD-hiệu 0.362 đo trên điểm-đúng teacher AC; bảng MDE đầy đủ G=26/100/150/200 → kết luận tự đủ không cần ngưỡng); report/79_pilot_androidcontrol.md:51/64 (cổng go/no-go THỰC của trục ĐÚNG = "không suy biến sàn-0 + phủ bước đủ cao", không phải 15-20pp); harness/mde_pilot.py:107-117 (SD tính từ điểm-đúng per-app của teacher trên AC, sd_diff=√2×sd, MDE=3.077×sd_diff/√G — xác nhận 0.362 là đại lượng của trục AC); report/89_review_deck_v5.md:29 + report/PHAN_BIEN_PROMPT.md:26 (tác giả đã tự log đúng lỗ "15-20 ở đâu ra?"). Kiểm số học: 3.077×0.362/√12 = 0.3216 → 32,2pp đúng về phép tính nhưng sai đầu vào (SD của thước khác).

---

### B21. [NHẸ] Biến CỤM bị vỡ: một app thật bị tách thành nhiều "cụm", vài cụm không phải app

- **Trục:** THỐNG KÊ + LỰC MẪU (MDE trục ĐÚNG, wild-cluster bootstrap vs exact sign-flip, đa phép so sánh)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NHẸ

**Vấn đề.** Hàm gán app dùng regex bắt từ goal khi không có open_app. Nó đẻ ra tên trùng lặp và tên rác. Ở pilot thì chỉ làm G phồng; ở phân tích thật, app CHÍNH LÀ biến cụm của wild-cluster bootstrap — tách một app thành hai cụm là vi phạm thẳng giả định độc-lập-giữa-cụm và thổi G.

**Bằng chứng.** mde_pilot_results.json app_scores có đồng thời: "CNN" và "Knoxville on the CNN"; "NYTimes" và "Newyork times"; "Arts & Culture" và "Art & Culture"; "The Washington Post" và "Washington post". Thêm "On the Pinerest", "Inspire in this", "Artier" — sản phẩm của regex ở mde_pilot.py:36 `([A-Z][A-Za-z0-9&\.\- ]{1,20}?) app`. Tôi gộp bí danh và chạy lại: G 26→22, SD_1arm 0,2561→0,2632.

**Đề xuất sửa.** Chuẩn hoá tên app (lowercase + bỏ mạo từ + fuzzy-merge + duyệt tay danh sách ~70 tên, việc này rẻ) TRƯỚC khi khoá biến cụm trong report/85 §6. Bỏ hẳn nhánh regex hoặc bắt buộc duyệt tay đầu ra của nó — 59% ep không có open_app nên nhánh này gánh phần lớn nhãn.

**Người phản-bác nói gì.** Bằng chứng có thật nhưng hệ quả bị phóng đại ~2 bậc. (1) Regex mde_pilot.py:36 và các bí danh CNN/Knoxville, NYTimes/Newyork times, Arts & Culture/Art & Culture, Washington Post/Washington post đều đúng như họ nêu — không bác được phần dữ kiện. (2) NHƯNG hàm gán app đó chỉ là helper 3 dòng NỘI BỘ pilot, không nằm trên đường phân tích thật: repo đã có bộ gán chặt hơn ở scan_androidcontrol.py:18 (neo giới từ + strip 'the/my/your'), chính nó sinh ra ac_app_unseen_count.json — file cấp số app cho report/85. Chạy đối chiếu trên 200 ep: pilot cho 103 tên distinct/134 gán (đầy rác 'In the Pinterest', 'Go to the Zinio', 'On the Etsy'); scan cho 79 tên sạch (Pinterest, Zinio, Etsy). Đòn quy lỗi của một script pilot cho một script phân tích CHƯA VIẾT. (3) Tác động lên sản phẩm duy nhất của pilot (SD→MDE) là không đáng kể: tôi gộp 4 cặp bí danh, G 26→22, SD_1arm 0.2561→0.2674, MDE@G=150 9.10→9.50 pp, @G=200 7.88→8.23 pp — ngưỡng đăng-ký-trước là 15-20 pp, vẫn qua với biên ~2 lần. Mean 30.1%→31.8%, vẫn cách xa cổng sàn-0 của report/79. Kết luận report/86 KHÔNG đổi. (4) Một bằng chứng của họ SAI: họ xếp 'Artier' vào tên rác regex, nhưng goal thật là 'I want to learn about the Monalisa art and who made this in the Artier app' — Artier là app có thật, xuất hiện cả trong bộ scan sạch. (5) Tác giả đã ghi nhận lỗ này trước: report/85:19 khai gán app phủ ~72%, 'phần còn lại gán tay/GCS lúc build', số app để ngỏ '[≈150-250 — chốt chính xác lúc build]'; report/85:92 mục 1 bắt điền số app TRƯỚC khi commit. Phần còn sống: ngay bộ scan tốt vẫn còn bí danh sót (Art & Culture vs Arts & Culture, CNN vs CNN News, Voice Recorder vs Voice Recorder - URecorder ≈ 5% cụm so với 15% ở pilot) và pre-reg chưa viết thành thủ tục chuẩn-hoá tên app. Đó là một dòng bổ sung vào bản đăng-ký-trước cho một mục vốn đã để ngỏ, không phải lỗi thiết kế hay phân tích hỏng ⇒ hạ từ 'nặng' xuống 'nhẹ'.

**Bằng chứng của người kiểm.** /mnt/d/Master/Thesis/harness/mde_pilot.py:32-36 (hàm app_of + regex bị tố, xác nhận tồn tại) · /mnt/d/Master/Thesis/harness/mde_pilot_results.json (xác nhận đủ 4 cặp bí danh trong app_scores; n_apps=26, sd_1arm=0.2561216324293803, mean=0.30128) · /mnt/d/Master/Thesis/harness/scan_androidcontrol.py:18-30 (APP_IN_GOAL — bộ gán chặt hơn, neo giới từ, strip article) · /mnt/d/Master/Thesis/harness/ac_app_unseen_count.json (tên sạch: 'Pinterest':14, 'CNN':6 — không có 'On the Pinerest'/'Knoxville on the CNN' ⇒ đường phân tích dùng bộ khác) · /mnt/d/Master/Thesis/dataset_samples/androidcontrol_test/ac_test_200ep.json (đối chiếu 2 regex: pilot 134 gán/103 distinct vs scan 107 gán/79 distinct, 32 ep khác nhau; goal 'in the Artier app' chứng minh Artier là app thật) · /mnt/d/Master/Thesis/report/85_preregistration_v2_LAI.md dòng 19 (gán app ~72% + 'gán tay/GCS lúc build' + số app để ngỏ) và dòng 92 (điền số app trước khi commit) · Tính lại tại chỗ sau khi gộp bí danh: G=22, mean=0.3182, SD_1arm=0.2674, SD_diff=0.3782, MDE(3.077×SD_diff/√G) = 9.50pp@150, 8.23pp@200, 7.36pp@250 — đều dưới ngưỡng 15-20pp.

---

### B22. [NHẸ] Đơn vị cụm không phải 'app' mà là chuỗi trích từ goal — một app bị tách thành nhiều cụm

- **Trục:** DỮ LIỆU, SPLIT, RÒ RỈ — và câu hỏi "vừa học vừa chấm cùng loại"
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NHẸ

**Vấn đề.** Thống kê wild-cluster bootstrap giả định cụm độc lập = app. Bộ gán nhãn app là một regex trên câu goal, cho ra nhiều biến thể của CÙNG một app. Tách một app thành nhiều cụm vừa thổi phồng G vừa làm SE bị ước lượng THẤP (lệch về phía có lợi cho kết quả dương) — đúng hướng nguy hiểm.

**Bằng chứng.** harness/mde_pilot.py:44-49 (app_of). Tôi chạy lại app_of trên 200 ep local: 134/200 có nhãn, 103 nhãn distinct, trong đó 'Polaris Office' và 'In the Polaris Office'; 'Etsy' và 'On the Etsy'; 'Flipsnack' / 'Flipsnack magazine' / 'In Flipsnack'; 'CNN' và 'CNN News'; 'Google Fit' và 'Google fit'; rác kiểu 'Utilize the Snapdeal', 'Fairey on the Artsy'. Kết quả pilot đã dùng nhãn hỏng này: harness/mde_pilot_results.json chứa đồng thời 'Arts & Culture' và 'Art & Culture', 'NYTimes' và 'Newyork times', 'The Washington Post' và 'Washington post', cùng 'On the Pinerest', 'Knoxville on the CNN', 'Inspire in this'.

**Đề xuất sửa.** Gán app bằng open_app.app_name + tra bảng chuẩn hoá (lowercase, bỏ tiền tố 'in/on/the/using/go to', map bí danh TOI↔The Times of India, NYTimes↔Newyork times...), rà tay danh sách cuối. Đây là việc free và phải làm TRƯỚC khi khoá pre-registration, vì G và SE đều phụ thuộc nó.

**Người phản-bác nói gì.** Lõi quan sát ĐÚNG và tôi tái lập được: app_of (harness/mde_pilot.py:32-37) đúng là sinh nhiều biến thể cho cùng một app, và mde_pilot_results.json đúng là chứa 'Art & Culture'/'Arts & Culture', 'NYTimes'/'Newyork times', 'The Washington Post'/'Washington post'. Bằng chứng họ nêu KHÔNG bịa. Nhưng ba mắt xích suy luận phía sau đều hỏng, nên mức 'nang' là phóng đại:

(1) ĐỘ LỚN nhỏ hơn nhiều họ ngụ ý. Trên 200 ep local: 134 ep có nhãn, 103 nhãn distinct; chuẩn hoá (bỏ tiền tố 'in the/on the/open the/utilize the', casefold, bỏ dấu câu) chỉ gộp được 6 nhóm (googlefit, polarisoffice, etsy, artsculture, flipsnack, pinterest) → 103→~97, tức G phồng ~6%, SE ước thấp ~3%. Họ trộn lẫn 'nhãn xấu' với 'cụm bị tách': 'Utilize the Snapdeal', 'ZAR using the XE', 'Fairey on the Artsy' là nhãn xấu nhưng DUY NHẤT — một app một nhãn, không tách cụm nào. Chỉ loại thứ hai gây hại họ mô tả.

(2) HƯỚNG LỆCH bị nói sai ở chính file họ dẫn. mde_pilot.py KHÔNG chạy wild-cluster bootstrap — nó tính SD per-app thô rồi 3.077×√2×SD/√G. Trong vai trò ước lượng phương sai, tách app còn tự-hạn-chế: ít bước/cụm hơn → trung bình cụm nhiễu hơn → SD PHỒNG. Tôi gộp 4 cặp trùng trong pilot: SD 0.256→0.267, MDE@G=150 đi từ 9.1 lên 10.3 pp. Có tilt nhẹ có lợi (do phồng G), nhưng 1.2 pp so với ngưỡng đăng-ký-trước 15-20 pp → kết luận cổng report/86 'đủ lực' không suy chuyển.

(3) ĐÂY KHÔNG PHẢI LUẬT ĐÃ ĐÓNG BĂNG. report/85:19 đã tự dán cờ: 'phủ ~72% ep... phần còn lại gán tay/GCS lúc build' + '[số app test AC ≈ 150-250 — chốt chính xác lúc build]', report/86:37 nhắc lại 'chỉ còn chốt số-app-chính-xác lúc build'. Regex là bộ ƯỚC LƯỢNG G tạm cho pilot, không phải quy tắc gán cụm đã pre-register.

Phần SỐNG (nên thừa nhận thẳng): dấu ngoặc mở ở report/85 chỉ nói gán tay cho ~33% ep KHÔNG có nhãn, không nói gì về chuẩn-hoá/dedup các nhãn regex ĐÃ sinh ra. Không thêm bước canonicalize thì 6 nhóm tách sẽ chui vào lúc build. Đây là việc vá một dòng (strip tiền tố + casefold, hoặc dùng thẳng app_name của open_app / package name bản GCS), không phải lỗi thiết kế → mức 'nhe', hạng mục vệ-sinh-dữ-liệu + một câu bổ sung vào pre-registration.

**Bằng chứng của người kiểm.** ĐÃ ĐỌC: /mnt/d/Master/Thesis/harness/mde_pilot.py (app_of dòng 32-37; tính SD/MDE dòng 104-117 — KHÔNG có wild-cluster bootstrap), /mnt/d/Master/Thesis/harness/mde_pilot_results.json, /mnt/d/Master/Thesis/harness/ac_app_unseen_count.json, /mnt/d/Master/Thesis/report/85_PREREG_v2_LAI.md (§1 dòng 19, §6 dòng 64-67), /mnt/d/Master/Thesis/report/86_MDE_pilot_ket_qua.md.

ĐÃ CHẠY (~/.venvs/thesis/bin/python, local, free) trên /mnt/d/Master/Thesis/dataset_samples/androidcontrol_test/ac_test_200ep.json:
- Tái lập app_of: 134/200 ep có nhãn (67%, KHÔNG phải ~72% như report/85 khai), 103 nhãn distinct; nguồn nhãn = 72 ep từ open_app-action (52 nhãn distinct, sạch) + 62 ep từ regex-goal (57 nhãn distinct, chứa toàn bộ rác họ liệt kê).
- Chuẩn hoá core() = bỏ tiền tố (in the|on the|open the|go to the|utilize the|using the) + casefold + bỏ ký tự không alnum → chỉ 6 nhóm có >1 biến thể: {Google Fit, Google fit}, {In the Polaris Office, Polaris Office}, {On the Etsy, Etsy}, {In the Arts & Culture, Arts & Culture}, {In Flipsnack, Flipsnack}, {In the Pinterest, In the pinterest, Pinterest}. → G phồng ~6%.
- 18 nhãn regex chồng lấn với nhãn open_app đã có ⇒ fix tất định rẻ: ưu tiên open_app app_name làm khoá chuẩn.
- Sensitivity gộp 4 cặp trùng trong mde_pilot_results.json (Art&Culture, NYTimes, Washington Post, CNN): G 26→22, mean 0.301→0.318, SD 0.256→0.267; MDE@G=150 9.1→9.5 pp; gộp + co G tương ứng (150→127) → 10.3 pp. Vẫn dưới ngưỡng 15-20 pp.

PHÁT HIỆN PHỤ (không thuộc đòn này): con số '~72%' ở report/85 không khớp artifact nào — tôi đo 67% trên ac_test_200ep.json, còn ac_app_unseen_count.json ghi 102/250 = 41% với chỉ 42 app distinct.

---

### B23. [NHẸ] K1 — tập thử là 30 màn / 7 app chứ không phải "127 màn", và 27,5% mỗi lớp then chốt là một chuỗi duy nhất

- **Trục:** Bốn phép thử K1 / K2 / OCR / VIỆC1 — có bị khái quát quá không
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NHẸ

**Vấn đề.** report/73 mở đầu bằng "chạy trên 127 màn MobileViews thật, 130 cặp thử". Con số 127 chỉ là mẫu số để tính độ phủ VH; tập thử thật chỉ lấy từ 30 màn thuộc 7 app, và hai lớp quyết định (paraphrase, nearsyn) mỗi lớp chỉ đến từ 17 màn. Nặng hơn là thành phần: 'Everything' chiếm 11/40 paraphrase và 'None' chiếm 11/40 nearsyn. Riêng cặp anchor 'all' đóng góp hơn một phần tư của cả hai lớp. Và 'None' vs 'All' là quan hệ TRÁI NGHĨA — embedding vốn nổi tiếng đặt trái nghĩa rất gần nhau, nên chọn nó làm đại diện cho "bịa gần-nghĩa" là tự xếp bài để phép thử rớt. Ngoài ra κ=0,38 được tính trên tỉ lệ lớp do tác giả tự đặt bằng caps (70 REAL / 60 HALLUC); κ phụ thuộc mạnh vào prevalence, mà prevalence thật ngoài đời — theo chính K2 — là ~2%. Nên κ=0,38 không nói được gì về chất lượng matcher lúc triển khai.

**Bằng chứng.** k1_matcher_killtest.py:118 caps={exact:30, paraphrase:40, nearsyn:40, unrelated:20}; chạy lại build_pairs(): "DISTINCT SCREENS CONTRIBUTING PAIRS: 30", "DISTINCT APPS: 7", paraphrase 40 cặp từ 17 màn, nearsyn 40 cặp từ 17 màn; Counter paraphrase [('Everything',11), ...], Counter nearsyn [('None',11), ...]. LEX dòng 93: {"a":"all", "para":["Everything",...], "near":["None",...]}. Hàm kappa (dòng 155-165) tính trên toàn bộ 130 cặp với thành phần do caps quy định. report/73:3 "chạy trên 127 màn MobileViews thật".

**Đề xuất sửa.** Sửa mọi chỗ ghi "127 màn" thành "30 màn / 7 app". Cân bằng lại tập thử: giới hạn mỗi chuỗi ứng viên tối đa ~3 lần, bỏ hoặc tách riêng cặp trái-nghĩa 'All'/'None' (báo riêng vì nó là ca đặc biệt, không đại diện cho bịa gần-nghĩa). Bỏ κ khỏi headline hoặc báo kèm prevalence giả định; báo AUC (bất biến với prevalence) làm số chính.

**Người phản-bác nói gì.** Đòn sống ở phần MÔ TẢ nhưng chết ở phần LẬP LUẬN, và mức "nặng" là phóng đại.

SỐNG: (1) report/73:3 "chạy trên 127 màn" là nói quá thật — tập thử chỉ từ 30 màn, 127 chỉ là mẫu số vh_cov. Phải sửa. (2) Cô đặc thành phần có thật, và tôi còn tìm ra nặng hơn đòn nêu: hai lớp quyết định chỉ từ 4 app (không phải 7), 19/80 dòng trùng nguyên văn → chỉ 61 phép thử thật sự khác nhau. (3) κ phụ thuộc prevalence do caps là đúng về kỹ thuật.

CHẾT: cáo buộc trung tâm — "chọn trái nghĩa None/All là tự xếp bài để phép thử rớt" — SAI và NGƯỢC DẤU. Trong chính dữ liệu, 'None' được chấm THẤP hơn 'Everything' ở 9/11 ca; bỏ anchor 'all' khiến AUC tụt 0.525→0.366 và bỏ-lọt vọt 47,5%→62,1%. Cặp bị tố "xếp bài cho rớt" thực ra đang ĐỠ cho matcher. Leave-one-out cả 12 anchor: chồng lấn vẫn 100% ở mọi cấu hình, AUC không bao giờ quá 0.585 — kết luận cấu trúc BẤT BIẾN với việc xoá bất kỳ anchor nào. Cô đặc không tạo ra kết luận.

HẠ MỨC: K1 là kill-test, kết luận duy nhất nó chở là "đừng tin matcher embedding-đơn" — một khẳng-định-tồn-tại, chỉ cần phản ví dụ, không cần mẫu đại diện. Nó không ước lượng tỉ lệ dân số nào. Report đã tự khai adversarial + ±15 điểm + tự giới hạn claim vào "phát hiện cấu trúc" — và test leave-anchor-out của tôi xác nhận cách tự giới hạn đó ĐÚNG. Thêm nữa chiều bỏ-lọt đã bị chính tác giả rút ở K2, matcher đã bị thay, thước mới đã validate độc lập (report/84 AUC=1.0), và report/85 không treo ngưỡng nào lên 47,5% hay κ=0,38.

Còn lại đúng một việc: sửa câu "127 màn" thành "30 màn/7 app (hai lớp quyết định: 4 app, 61 phép thử khác nhau)" và bổ sung dòng cô-đặc/trùng-lặp vào mục Giới hạn. Đó là vệ sinh tài liệu trong một memo nội bộ, không phải lỗi thiết kế → "nhẹ", không phải "nặng".

**Bằng chứng của người kiểm.** **Tái tạo build_pairs() (~/.venvs/thesis/bin/python):** "DISTINCT SCREENS CONTRIBUTING PAIRS: 30", "DISTINCT APPS: 7"; paraphrase 40 cặp/17 màn, nearsyn 40 cặp/17 màn; Counter paraphrase [('Everything',11)], nearsyn [('None',11)]; anchor 'all' = 11/40 mỗi lớp. → mọi số mô tả của đòn ĐÚNG. report/73:3 "chạy trên 127 màn" trong khi 127 chỉ là mẫu số tính vh_cov=0.6244.

**Tính lại sims bằng nomic-embed local (130 cặp), test leave-one-anchor-out — BÁC mechanism:**
- FULL: overlap 40/40, AUC(para>near)=0.525, FP_para 47.5%, FN_near 47.5%
- DROP anchor='all': overlap 29/29, **AUC=0.366** (DƯỚI ngẫu nhiên), **FN_near 62.1%**, FP_para 58.6% → bỏ cặp bị tố "xếp bài" làm matcher TỆ ĐI, không tốt lên.
- Sims cặp 'all': 'None' THẤP hơn 'Everything' ở 9/11 ca (0.442 vs 0.674) → antonym là ca embedding tách TỐT nhất, ngược hẳn tiền đề "embedding đặt trái nghĩa rất gần".
- Leave-one-out cả 12 anchor: overlap = n/n (100%) ở MỌI ca; AUC max 0.585 (drop share). Per-app overlap: 9/9, 9/9, 9/9, 12/13.

**Điểm đòn BỎ SÓT (nặng hơn họ nêu):** hai lớp quyết định chỉ từ **4 app** (7 app là của lớp exact); 19/80 dòng key là TRÙNG LẶP nguyên văn (('Everything',0.674)×6, ('None',0.442)×6) → distinct (cand,sim) = 61/80. Cluster-bootstrap theo app (G=4, 5000 lần): FN_nearsyn CI95 [28%, 64%]; AUC CI95 [0.323, 0.715] (cắt 0.5).

**Tự khai sẵn trong report/73 mục "Giới hạn":** "Tập thử là adversarial: tôi cố ý chọn các ca bịa-gần-nghĩa KHÓ nhất... worst case"; "Mẫu nhỏ (40 cặp/loại khó) → các % có sai số rộng (~±15 điểm). Nhưng phát hiện cấu trúc... vững bất kể % chính xác."

**Không load-bearing:** report/74:7 tác giả tự rút chiều bỏ-lọt ("gần như KHÔNG xảy ra trong output thật"); report/85:57 chỉ dùng K1 làm lý do "matcher đa-tầng nâng cấp (không phải nomic-đơn đã chết ở K1)"; report/84 thay thước, AUC=1.000 độc lập. Không ngưỡng đăng-ký-trước nào tựa vào 47,5% hay κ=0,38.

---

### B24. [NHẸ] OCR — số đếm glyph icon bị thổi ~7 lần do đếm substring; arrow và checkmark thực tế là ZERO

- **Trục:** Bốn phép thử K1 / K2 / OCR / VIỆC1 — có bị khái quát quá không
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NHẸ

**Vấn đề.** report/75 §Cập nhật khẳng định "OCR ĐỌC ĐƯỢC nhiều icon glyph — '+' (23 lần), 'X/x/×' (97), '<'/'>' (46)" và dùng đúng đó để chốt hướng thiết kế: gắn từ-điển-ký-hiệu thẳng lên glyph OCR trả về, không cần model dò icon. Tôi đếm lại từ chính ocr_cache.json: glyph đứng riêng ở conf≥0,5 chỉ có '+' = 11, 'X' = 13, '<'/'>' = 0, '✓' = 0. Khi tôi đếm theo kiểu substring-anywhere thì ra đúng 23 và 97 → xác nhận lỗi đếm: mọi chuỗi chứa chữ x ('Expenses', 'Next', 'Box') đều bị tính là đọc được icon X. Hệ quả thiết kế nghiêm trọng: OCR trả về ZERO mũi tên đứng riêng và ZERO dấu tích — đúng hai loại icon mà K2 nói là nguồn kết-oan chính. Tầng 4 của trọng tài đa-tín-hiệu như mô tả sẽ không chạy được cho chính các ca nó sinh ra để cứu.

**Bằng chứng.** Đếm lại từ harness/dg1_cache/ocr_cache.json, conf≥0,5, tổng 2053 hộp: exact-standalone '+' = 11 / 'X','x','×' = 13 / '<','>' = 0 / '三' = 8 / '✓' = 0; substring-anywhere '+' = 23 / 'X','x','×' = 97 → khớp y hệt con số report/75:45.

**Đề xuất sửa.** Sửa lại bảng glyph trong report/75 bằng số đếm standalone. Bỏ mệnh đề "không cần model dò icon" — với ✓ và mũi tên thì OCR không cung cấp gì để gắn từ-điển vào. Ghi thẳng vào phần giới hạn: sàn kết-oan icon-hình-thuần không xoá được bằng OCR, và trước khi cam kết tầng 4, phải đo lại xem còn bao nhiêu ca thật sự cứu được.

**Người phản-bác nói gì.** LÕI SỰ KIỆN CỦA ĐÒN ĐÚNG — tôi tái lập được y hệt. report/75:45 đúng là đếm substring/occurrence: ở conf≥0,5 trên 2053 hộp, glyph ĐỨNG RIÊNG chỉ có '+' = 11, 'X/x/×' = 13, '<'/'>' = 0, '✓' = 0, '三' = 8; còn đếm-chứa-ký-tự ra đúng 23 / 97 / 47 / 8 = trùng khít bộ số report. Đọc text thô càng rõ: 47 lần '<>' KHÔNG phải mũi tên điều-hướng mà là rác OCR ('<>!' lặp lại, 'SD:>_', 'Let's chat>'). Câu "OCR ĐỌC ĐƯỢC nhiều icon glyph — '<'/'>' (46)" là SAI và phải xoá. Thêm một lỗi tài liệu người phản biện chưa nêu: bảng 3 tầng ở §Cập nhật (74,0/79,2/79,5) KHÔNG có code lẫn artifact nào lưu lại — ocr_coverage_results.json chỉ chứa bộ số §Số liệu, và harness/ocr_vh_coverage.py:106 lọc has_alnum() nên loại sạch glyph thuần, tức bảng đó do script ad-hoc không lưu sinh ra.

NHƯNG "MỨC NẶNG" VÀ "HỆ QUẢ THIẾT KẾ NGHIÊM TRỌNG" THÌ BỊ BÁC, vì bốn điểm:

(1) Con số thiết kế KHÔNG rút ra từ chỗ đếm sai. Tôi dựng lại tầng từ-điển bằng luật trung thực (chỉ glyph đứng riêng): nút cỡ-nút 74,0% → +OCR text 80,0% → +từ-điển 80,2%, tức +0,22 điểm riêng icon, cứu vỏn vẹn 8 nút. Report ghi 74,0/79,2/79,5, +0,3. Khớp trong sai số làm tròn ⇒ bảng đó vốn đã được tính bằng luật standalone, không phải bằng con số bị thổi. Kết luận định lượng không đổi một ly.

(2) Thân bài report ĐÃ nói đúng điều ngược lại. Dòng 7 (Phán quyết) và dòng 31 khẳng định OCR "hoàn toàn không cứu được icon thuần (+ / ✓ / mũi tên)". Câu ở dòng 45 tự mâu thuẫn với chính tài liệu của nó — là một câu lạc, không phải luận điểm chịu lực.

(3) Report đã tự khai đúng cái người phản biện trình bày như phát hiện mới. Dòng 54: "Sàn kết-oan còn lại ~20,5% ... icon hình thuần như '✓', avatar, logo → giới hạn không xoá hết bằng OCR; muốn hết phải phân-loại-icon bằng thị giác (ngoài phạm vi)". Dòng 53 tự hạ từ-điển-icon xuống "không phải đòn lớn như tưởng". Tác giả đã xử lý rồi.

(4) LUẬN CỨ TRUNG TÂM CỦA NGƯỜI PHẢN BIỆN SAI SỰ KIỆN. Họ viết arrow và checkmark là "đúng hai loại icon mà K2 nói là nguồn kết-oan chính". Đọc harness/k2_results.json thì phân bố ca kết-oan glyph ngắn là: '+' = 15, '✓' = 3, '<' = 1, '>' = 1, 'OK' = 1, '30' = 1. Loại áp đảo là '+' (15/22 = 68%), mà '+' chính là glyph OCR CÓ đọc đứng riêng (11 hộp; 7 hộp cứu được nút vốn không nhãn trong phép đo lại của tôi). Mũi tên + dấu tích chỉ 5/22 ≈ 23%. Nên khẳng định "tầng 4 sẽ không chạy được cho chính các ca nó sinh ra để cứu" là ngược với dữ liệu K2: nó chạy cho đa số ca.

TỒN ĐỌNG THẬT (nên sửa, mức biên tập 2 câu): xoá/sửa câu đếm glyph ở dòng 45, và hạ "cứu đúng 20/40 ca K2" (dòng 40, 70) xuống ~15/40 vì phần ✓ và mũi tên không có glyph OCR để gắn từ-điển. Không có số nào, quyết định thiết kế nào, hay hạng mục đăng-ký-trước nào (report/85 dùng matcher đa-tầng) phải đổi.

**Bằng chứng của người kiểm.** Đếm lại harness/dg1_cache/ocr_cache.json (127 màn, 2053 hộp, conf≥0,5): exact-standalone '+' = 11, 'X/x/×' = 13, '<'/'>' = 0, '✓' = 0, '三' = 8; substring/occurrence '+' = 23, 'X/x/×' = 97/100, '<>' = 47, khớp report/75:45 ⇒ xác nhận lỗi đếm. Dump text chứa '<>' cho thấy toàn rác OCR ('<>!', 'SD:>_', 'OPEN >'), không có mũi tên đứng riêng nào.

Dựng lại tầng từ-điển-ký-hiệu bằng luật standalone trên 3561 nút cỡ-nút (area<5% màn), script scratchpad/recheck.py dùng lại logic containment + conf≥0,5 của harness/ocr_vh_coverage.py: VH-only 74,0% → +OCR text 80,0% (+6,0) → +từ-điển 80,2% (+0,22 riêng icon), chỉ 8 nút được cứu, phân bố glyph = {'+': 7, '三': 1}. Đối chiếu report/75:47-51 (74,0/79,2/79,5, +0,3) ⇒ bảng report tái lập được, không dựa vào số bị thổi.

harness/ocr_coverage_results.json chỉ lưu recall_vh_micro=0.6978 / recall_vhocr_micro=0.8098 / recall_vh_macro=0.6451 / recall_vhocr_macro=0.8074 / ocr_added=444 — KHÔNG có bảng 3 tầng; harness/ocr_vh_coverage.py:106 có điều kiện has_alnum(bx["text"]) loại hết glyph thuần ⇒ §Cập nhật do script ad-hoc không lưu sinh ra (lỗ reproducibility, không nằm trong đòn gốc).

harness/k2_results.json, nonvb_detail, lọc phần tử ≤2 ký tự: '+' = 15, '✓' = 3, '<' = 1, '>' = 1, 'OK' = 1, '30' = 1 (tổng 22) ⇒ bác thẳng mệnh đề "arrow và checkmark là hai loại kết-oan chính của K2"; loại chính là '+' 68%, đúng glyph OCR đọc được.

report/75:7 và :31 (thân bài) đã nói OCR "hoàn toàn không cứu được icon thuần + / ✓ / mũi tên"; :54 đã khai sàn kết-oan ~20,5% icon hình thuần gồm '✓' là giới hạn ngoài phạm vi; :68 đã khai K2 chạy trên bộ 80 màn app1_s* khác bộ 127 màn OCR (tôi kiểm: ảnh app1_s* không còn trong dataset_samples/ nên không đo trực tiếp trên ca K2 được — đúng như report tự khai).

---

### B25. [NHẸ] Bảng report/84 ghi "✓ Đúng kỳ vọng" cho hai dòng mà chính script in ra cờ cảnh báo "⚠ KHÔNG tụt đủ"

- **Trục:** TRUNG THỰC BÁO CÁO — đối chiếu prose (report/73-86, 88, CLAUDE.md §0) với code + số thô trong harness/
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NHẸ

**Vấn đề.** Script tự cài ngưỡng độ nhạy: nếu coverage tụt <0.15 với target_error/action_error/missing thì in cờ "⚠ KHÔNG tụt đủ". Tôi chạy lại script và nó IN RA cờ đó cho action_error (Δ=0.149) và missing (Δ=0.150 nhưng thực là 0.14907). Vậy hai trong ba phép kiểm độ nhạy đã trượt ngưỡng do chính tác giả đặt. Nhưng bảng trong report/84 ghi cả hai dòng là "✓" và phán quyết chung là QUA CỔNG; report/88 và CLAUDE.md chỉ còn "✅ QUA". Về bản chất Δ≈0.15 là hợp lý (sửa 1 bước trên ~6-7 bước thì coverage tụt ~1/6), tức ngưỡng 0.15 mới là cái đặt sai chứ không phải thước hỏng — nhưng đúng quy trình đăng-ký-trước thì không được im lặng bỏ qua cờ đỏ của chính mình rồi ghi ✓; phải hoặc sửa ngưỡng và khai là đã sửa, hoặc báo là trượt.

**Bằng chứng.** harness/metric_v1_validate.py:174 `if k in ("target_error","action_error","missing") and drop < 0.15: flag = "  ⚠ KHÔNG tụt đủ"`. Output tôi chạy lại nguyên văn: "action_error coverage=0.851 Δ=+0.149 ⚠ KHÔNG tụt đủ" / "missing coverage=0.850 Δ=+0.150 ⚠ KHÔNG tụt đủ". Đối lại report/84:17-18 ghi cả hai là "✓".

**Đề xuất sửa.** Định nghĩa lại ngưỡng độ nhạy theo tỉ lệ chứ không theo hằng số tuyệt đối (kỳ vọng Δ ≈ 1/số-bước-trung-bình, ~0.15 ở đây), ghi rõ trong report/85 là đã hiệu chỉnh ngưỡng và VÌ SAO, kèm ngày. Hoặc giữ nguyên ngưỡng và ghi trung thực là 2/3 phép kiểm trượt.

**Người phản-bác nói gì.** Sự kiện nền là THẬT (cờ ⚠ có in ra cho action_error/missing, bảng report/84 ghi ✓, không khai) nên đòn không bị bác sạch — nhưng khung "trượt cổng / vi phạm đăng-ký-trước" thì SAI, và mức "nặng" là phóng đại.

(1) Ngưỡng 0.15 KHÔNG phải cổng. Phán quyết pass/fail duy nhất trong script là dòng 182, chỉ cho AUC ("✅ QUA CỔNG (≥0.80)"). Bộ tiêu chí đăng-ký-trước gồm đúng 3 mục: detection≥0.90, FP≤0.10, AUC≥0.80 (report/84:51 và report/85:47-53, kèm câu "rớt AUC≥0.80 → DỪNG, KHÔNG train"). Số 0.15 không xuất hiện ở bản đăng-ký-trước. Cả 3 tiêu chí thật đều đạt kịch trần (1.000 / 0.000 / 1.000). Cờ ⚠ là dòng in sanity lúc debug, không phải cổng bị bỏ qua.

(2) Hai dòng bị gắn cờ không phân biệt được với dòng mà chính người ra đòn coi là đạt: 0.15298 vs 0.14907, cách nhau 0.004 trên 185 ep. Luật nào cho một dòng qua và dòng kia rớt ở khoảng cách đó là fitting nhiễu.

(3) Chính người ra đòn thừa nhận phần nội dung: "Δ≈0.15 là hợp lý… ngưỡng 0.15 mới là cái đặt sai chứ không phải thước hỏng". Không con số nào sai, không kết luận nào đổi → còn lại là chú thích tài liệu, không phải lỗi nặng.

(4) Trích dẫn bằng chứng bị lệch: gán 0.14907 cho missing, nhưng 0.14907 là action_error (missing = 0.14964).

(5) Downstream không bị rửa số: report/88:199 ghi "✅ QUA (AUC=1.0)" — quy thẳng phán quyết về AUC, đúng cổng thật.

Điểm còn lại đáng sửa (rất nhẹ): report/84 nên có 1 dòng chú thích rằng script in cờ độ-nhạy nội bộ ở 2 dòng, và độ tụt kỳ vọng phụ thuộc độ dài episode (≈1/|gold|, bị suy giảm do bước trùng lặp) nên con số 0.15 là mô tả, không phải tiêu chí.

**Bằng chứng của người kiểm.** Đã đọc/chạy: harness/metric_v1_validate.py (dòng 174 đúng nguyên văn như trích; dòng 182 = verdict duy nhất, chỉ cho AUC). Tính lại từ harness/metric_v1_results.json (base clean=1.000): target_error Δ=0.15298, action_error Δ=0.14907, missing Δ=0.14964, extra/reorder/paraphrase Δ=0 — khớp output họ dán (làm tròn .3f → +0.149 / +0.150), nhưng họ gán nhầm 0.14907 cho missing.

report/84_metric_validate_ket_qua.md:16-18 (bảng ghi ✓ cho cả 3 dòng, cột tên là "Đúng kỳ vọng?" kèm giải thích cơ chế "1 bước/~5 sai → tụt ~1/5") và :51 (bộ ngưỡng đăng-ký = detection≥0.90 / FP≤0.10 / AUC≥0.80, KHÔNG có 0.15).

report/85_PREREG_v2_LAI.md:47-53 — bảng cổng chính thức chỉ 4 dòng (detection sai-target, detection sai-action, FP paraphrase, AUC), cổng cứng = AUC≥0.80. Không có ngưỡng 0.15.

report/88_TOAN_CANH_CHI_TIET.md:199 — "✅ QUA (AUC=1.0)", quy về AUC chứ không phải độ tụt.

Kiểm thêm (điểm họ bỏ sót): mean(1/len) trên 185 ep = 0.2209 trong khi cả BA dòng đều tụt ~0.15 → ~1/3 bước bị sửa vẫn được phủ bởi bước trùng lặp khác (đặc tính của coverage phủ-tập). Áp dụng đồng đều cả 3 dòng, càng cho thấy tách riêng 2 dòng là tuỳ tiện. Dữ liệu: dataset_samples/androidcontrol_test/ac_test_200ep.json (185 ep hợp lệ, mean 5.55 bước).

---

### B26. [NHẸ] Tính mới 'tác vụ mới: hướng dẫn cho NGƯỜI' — đứng được một nửa; gold thực tế là lệnh low-level cho agent-mode, và estimand 'nhiều bước từ 1 ảnh' chưa được chốt nhất quán

- **Trục:** Đủ ngưỡng luận văn thạc sĩ? + logic đổi hướng + khả thi (giám khảo hoài nghi, tự kiểm số trước khi đọc report)
- **Phân loại:** chưa đủ dữ kiện · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NHẸ

**Vấn đề.** Phản biện 2 chiều như đề bài yêu cầu. CHIỀU ĐẬP: (a) gold step_instructions của AC là câu lệnh thao tác do annotator viết cho chế độ agent low-level — dữ liệu thô tôi đọc: 'Click on filter option', 'Go back to the previous page', 'Click on the top at the bottom right corner' — KHÔNG phải văn hướng-dẫn-người-đọc; train model sinh ra chúng = mô tả hành-động-kế-tiếp bằng NL, khoảng cách với pitch 'hướng dẫn nhiều bước cho người' chủ yếu là ĐỔI NHÃN audience; (b) sinh instruction từ screen/trajectory đã là thành phần chuẩn trong pipeline data-synthesis của dòng agent (kiểu OS-Genesis/Aguvis reverse-synthesis) và dòng sinh-văn-cho-người trên GUI đã có Widget Captioning (EMNLP 2020), Screen2Words (UIST 2021) — claim 'mọi bài dùng AC đều để instruction ở INPUT, chưa ai làm target' dựa trên deep-research chưa đọc full-text (report/82 tự khai chưa quét CHI/UIST + chưa đọc GUITrans2Act); (c) mâu thuẫn estimand đo được: MDE pilot đo 1-ảnh→1-bước-kế-tiếp (mde_pilot.py PROMPT 'Write ONE short next-step instruction'), metric validate đo coverage ĐA-bước trên gold nguyên episode, còn gold đa-bước trải NHIỀU MÀN — model chỉ thấy ảnh 1 thì các bước sau về nguyên tắc không suy được từ ảnh → 'coverage-episode cao hơn 30%' (CLAUDE/86 hứa hẹn) sẽ đo trí nhớ app + đoán mò, không đo grounding; chưa file nào chốt input thật của trục ĐÚNG. CHIỀU ĐỠ: seam 'goal-conditioned instruction làm TARGET + dual-eval gold/no-gold + audience người' vẫn hẹp nhưng có thật; chuẩn thạc sĩ (constructive/technological, không đòi SOTA) không đòi tác vụ mới hoàn toàn — một artifact model + khung đánh giá + chương negative-results là đủ NẾU hạ tông claim từ 'model ĐẦU TIÊN' xuống 'tác vụ ít được khai thác, phân định rõ với X/Y/Z'.

**Bằng chứng.** ac_test_200ep.json ep đầu: steps trùng nguyên văn ×2 ('Click on Hand Tools', 'Click on Wrenches & Spanners'), 'Click on the top at the bottom right corner'; tôi đếm 1042 step: 17.7% trùng-trong-episode (184), 4.3% go-back, 10.3% ≤3 từ — đối lập report/81:167 'chất lượng tốt'; việc A.3 'đếm rộng chất lượng gold' (81:184) không có file kết quả; mde_pilot.py:27-30 vs metric_v1_validate.py coverage đa-bước; report/82 tự khai 'CHƯA đọc full-text'

**Đề xuất sửa.** (1) Chốt bằng văn bản estimand trục ĐÚNG: input là ảnh NÀO cho bước nào (per-step teacher-forced như MDE pilot là lựa chọn duy nhất khả thi về construct — nói thẳng và bỏ pitch 'nhiều bước từ 1 ảnh' trên AC, hoặc giữ multi-step nhưng khai nó đo app-prior); (2) hoàn tất related-work sweep (OS-Genesis, Aguvis data pipeline, Widget Captioning, Screen2Words, GUITrans2Act full-text) trước khi viết chữ 'first'; (3) làm A.3 thật: đếm + lọc bước gold trùng/mơ hồ, khai 17.7% dup vì nó làm coverage dễ hơn

**Người phản-bác nói gì.** Đòn có 3 mũi; tôi kiểm từng mũi trên file thật thì **2/3 mũi sai hoặc dựa trên đọc thiếu file**, chỉ còn phần "hạ tông chữ ĐẦU TIÊN" là sống — mà chính dự án đã tự đăng ký rủi ro đó. Mức "nang" là phóng đại.

**Mũi (b) — SAI SỰ THẬT, bác thẳng.** Giám khảo khẳng định claim dựa trên deep-research "chưa quét CHI/UIST" nên bỏ sót Widget Captioning (EMNLP 2020) và Screen2Words (UIST 2021). Nhưng cả hai bài **đã có trong hồ sơ, kèm câu phân định**: `report/82_verify_tinh_moi_scoop.md:19-20` có hẳn hai dòng bảng ("Screen2Words | UIST 2021 | ✅ | 1 câu tóm tắt, không nhiều bước, không theo câu hỏi; eval CHỈ reference-based" / "Widget Captioning | EMNLP 2020 | ✅ | đơn-phần-tử, không quy trình"), và `report/57_related_work.md:59-64,151` đã viết đoạn related-work tiếng Anh phân định đúng hai bài này + UGIF (Findings NAACL 2024) + ScreenAI (IJCAI 2024). Trích "report/82 tự khai chưa quét UIST" để suy ra "đã bỏ sót UIST" là đọc sai chính file mình trích. Phần còn sống của mũi này chỉ là **OS-Genesis chưa xuất hiện ở bất kỳ file nào** (`grep -rn "OS-Genesis" report/ harness/` → 0 hit) — một citation thiếu, sửa bằng 1 dòng related-work, không đụng thiết kế; và dòng reverse-synthesis đó sinh instruction làm INPUT huấn luyện agent, không phải deliverable cho người đọc, đúng như `report/82:24` đã định vị cả cụm.

**Mũi (c) — GẦN NHƯ BÁC SẠCH.** Giám khảo nói "chưa file nào chốt input thật của trục ĐÚNG" và suy ra model chỉ thấy ảnh-1 rồi đoán mò các bước sau. `report/88_TOAN_CANH_CHI_TIET.md:87-89` chốt rõ ràng, đóng khung riêng: "**Đưa vào:** ảnh màn hình tại một bước + mục tiêu tổng thể + các bước đã làm trước đó. **Dạy nó trả ra:** đúng câu hướng dẫn do người viết cho bước đó." Tức là teacher-forced từng màn — đúng chuẩn Step-SR của AndroidControl (CLAUDE.md §4 đã ghi "Step-SR (teacher-forced)"). Ảnh per-step có thật ở mirror (`harness/mde_pilot.py:72` khớp `episode_{eid}_screenshot_{si}.png`), nên prompt 1-ảnh→1-bước của `mde_pilot.py:27-30` **không mâu thuẫn** với coverage đa-bước: chạy model lần lượt trên từng màn của episode rồi gom N câu so phủ-tập với N gold (`report/85` §3 "gióng bằng phủ-tập, không ép 1-1"; order-τ chỉ có nghĩa khi có nhiều bước). Vậy "coverage-episode cao hơn 30%" không hề đo trí-nhớ-app hay đoán mò — mỗi câu vẫn neo vào chính màn của nó. Cái sống lại duy nhất ở mũi này là **câu chữ pitch**: `report/85:11` và `report/88:78` viết "sinh hướng dẫn nhiều-bước từ **1 ảnh** + câu hỏi", lệch với giao thức per-màn ở 88:87. Đó là lỗi diễn đạt phải sửa 1 câu, không phải "estimand chưa chốt".

**Mũi (a) — số ĐÚNG nhưng kết luận đã bị dự án xử trước.** Tôi đếm lại độc lập trên `dataset_samples/androidcontrol_test/ac_test_200ep.json`: 1042 step, trùng-trong-episode 184 (17,7%), go-back 42 (4,0%), ≤3 từ 107 (10,3%), dài trung bình 7,0 từ. Số khớp. Nhưng: (i) trùng-lặp là **artifact của thao tác lặp** (click cùng toạ độ 2 lần) và dưới phủ-tập nó **triệt tiêu trong hiệu-số Student−Teacher** — estimand là Δ, không phải mức tuyệt đối, nên không tạo thiên lệch; (ii) soi tay 107 câu ≤3 từ thì phần lớn vẫn **gọi đúng tên đích** ("Click on Tools", "Type Paramedic news", "Open Maps App", "Click on gmail"), không phải câu trơ kiểu "tap the item" (chỉ 18/1042 kết bằng "the item/it/this"); (iii) quan trọng nhất, `report/88:120` — file nguồn-sự-thật mới nhất, đè `report/81` — **đã tự khai chính đòn này**: "thước này so văn-bản với hướng-dẫn-người-viết... chỉ đo *bước có gọi đúng thao-tác + đúng đích không*, là **proxy cho tính-ĐÚNG**, KHÔNG đo *hướng dẫn có dễ đọc/đủ dùng cho người thường* — cái sau đo RIÊNG bằng nghiên cứu nhỏ chấm-người", và nói thẳng mục đích là chặn đòn "thước đo con máy chứ đâu đo hướng dẫn cho người". Câu "chất lượng tốt" ở `report/81:167` là bản 19/7 sáng đã bị 88 thay; và chính `report/81:184` liệt việc A.3 "đếm rộng chất lượng gold" như việc-phải-làm — dự án tự biết chưa đếm, không phải giấu.

**Chênh lệch còn lại giữa hai bên là 1 chữ, không phải 1 thiết kế.** Giám khảo đề nghị hạ "model ĐẦU TIÊN" → "tác vụ ít khai thác, phân định rõ với X/Y/Z". Đó **đúng bằng** những gì `report/85` §8.5 ("Tính-mới mỏng ở kiến-trúc → bán bằng tác-vụ-mới + đánh-giá") và `report/81:171` ("phải khai thẳng nó MỎNG... nếu hội đồng không mua framing này thì đây là rủi ro số 1, không dập bằng số được → hỏi thầy") đã đăng ký trước. Đòn không thêm thiệt hại mới; nó xác nhận một rủi ro đã khai.

Việc phải làm: (1) sửa "từ 1 ảnh" → "từng màn của quy trình (teacher-forced), gom theo episode" ở `report/85:11` + `report/88:78`; (2) thêm 1 câu ở `report/86` nói rõ coverage-episode = gom output per-màn; (3) thêm OS-Genesis + 1 dòng phân định vào `report/57`; (4) đổi "model đầu tiên" → "chưa thấy tiền lệ ở tổ hợp X/Y/Z"; (5) làm sớm mini-study construct-validity (đang hoãn) vì nó là câu trả lời thật cho "chỉ đổi nhãn audience". Không đụng pre-registration, không đụng thước, không đụng split.

**Bằng chứng của người kiểm.** Đếm lại độc lập ac_test_200ep.json (1042 step): trùng-trong-ep 184=17,7% · go-back 42=4,0% · ≤3 từ 107=10,3% · dài TB 7,0 từ / median 6 · chỉ 18 câu kết bằng "the item/it/this" → số của giám khảo ĐÚNG nhưng phần lớn câu ngắn vẫn nêu đích cụ thể ("Click on Tools", "Type Paramedic news").
/mnt/d/Master/Thesis/report/88_TOAN_CANH_CHI_TIET.md:87-89 — chốt input trục ĐÚNG: "ảnh màn hình tại MỘT BƯỚC + mục tiêu tổng thể + các bước đã làm trước đó → câu hướng dẫn người viết cho bước đó" ⇒ bác "chưa file nào chốt input" và bác "model chỉ thấy ảnh 1".
/mnt/d/Master/Thesis/report/88_TOAN_CANH_CHI_TIET.md:120 — đã tự khai giới hạn "proxy cho tính-ĐÚNG, KHÔNG đo hữu-ích-cho-người; đo riêng bằng mini-study chấm người".
/mnt/d/Master/Thesis/report/82_verify_tinh_moi_scoop.md:19-20 — CÓ Screen2Words (UIST 2021) + Widget Captioning (EMNLP 2020) kèm phân định ⇒ bác "chưa quét CHI/UIST nên bỏ sót".
/mnt/d/Master/Thesis/report/57_related_work.md:59-64,151 — đoạn related-work đã phân định Widget Captioning/Screen2Words/UGIF/ScreenAI vs tác vụ của luận văn.
grep -rn "OS-Genesis" report/ harness/ → 0 hit ⇒ phần duy nhất của mũi (b) còn sống: thiếu citation OS-Genesis.
/mnt/d/Master/Thesis/harness/mde_pilot.py:72 — tải ảnh per-step "episode_{id}_screenshot_{si}.png" ⇒ teacher-forced từng màn khả thi, coverage-episode không đòi suy màn tương lai.
/mnt/d/Master/Thesis/report/85_PREREG_v2_LAI.md:11 và :48 (§3 phủ-tập) + §8.5 — pitch "từ 1 ảnh" lệch chữ với giao thức per-màn (phải sửa), và rủi-ro "tính mới mỏng" đã được đăng-ký-trước.
/mnt/d/Master/Thesis/report/81_CHOT_thiet_ke_cuoi_LAI.md:167,171,184 — "chất lượng tốt" là bản cũ đã bị 88 đè; 81:171 đã tự khai tính-mới mỏng; 81:184 tự liệt việc đếm chất lượng gold là việc chưa làm.

---

### B27. [NHẸ] Khả thi 7 tuần: FAIR 15/8 gần chắc trượt — 27 ngày nhưng chưa có dòng code train nào, data train chưa tải, bài FAIR trong KE_HOACH vẫn bán đóng góp ĐÃ CHẾT; VCL là sàn nhưng thừa hưởng lỗi thước cross-lingual

- **Trục:** Đủ ngưỡng luận văn thạc sĩ? + logic đổi hướng + khả thi (giám khảo hoài nghi, tự kiểm số trước khi đọc report)
- **Phân loại:** lỗi thật phải sửa · **Mức ban đầu:** NẶNG → **sau kiểm chéo:** NHẸ

**Vấn đề.** Kiểm kê thực tế repo: (a) KHÔNG có script train / config LLaMA-Factory nào; (b) AC train-split (nguồn tín hiệu CHÍNH, ~13k episode + ảnh) chưa tải — local chỉ có 200 ep test + count file; (c) matcher đa-tầng cho trục TRUNG THỰC (chuỗi→VH→OCR→từ-điển-icon, prereg §2) chưa build — mới có script phân tích ocr_vh_coverage; (d) chưa gặp thầy sau 3 lần đổi khung (mọi mốc 'HỎI THẦY' còn treo); (e) KE_HOACH_2_BAI_BAO (bản 3, 12/7) — abstract FAIR vẫn nguyên văn 'training only on data whose fabricated button references have been filtered' + headline Tier1/Tier2 MobileViews — chính là khung đã bị K2 giết 18/7 → bài FAIR phải viết lại từ số 0 theo khung LAI; (f) chuỗi việc còn lại trước FAIR: vá thước (phát hiện #1) → build data 2 nguồn → pilot xung-đột-phong-cách → train + ablation → eval 2 trục + thống kê → viết bài tiếng Anh — trong 27 ngày, một người, phụ thuộc Colab Pro chưa mua. Cái trượt trước: FAIR. Đường lui CÓ và đã tự khai ('BỎ FAIR giữ VCL', KE_HOACH §0.4) — điểm cộng thật. Nhưng VCL cũng không an toàn như tưởng: chấm trung thực output tiếng Việt đối chiếu VH tiếng Anh = đúng ca cross-lingual mà K1 đo được so-chuỗi kết oan 97.5% và embedding không cứu; hack 'bảo model giữ tên nút tiếng Anh' chưa có số nào; thời gian thật cho luận văn (bảo vệ, không phải bài báo) thì đủ NẾU bỏ FAIR sớm và cắt theo đúng thứ tự report/81 §cắt.

**Bằng chứng.** ls harness/*.py: không có train script; dataset_samples/androidcontrol_test chỉ có ac_test_200ep.json; KE_HOACH_2_BAI_BAO.md §2.2 abstract FAIR nguyên khung lọc-bịa (bản 3, 12/7, chưa sửa sau K2 18/7); k1_results.json: fp_paraphrase so-chuỗi... K1 report ghi 97.5% kết oan khác-ngôn-ngữ, LEX trong k1_matcher_killtest.py:81-98 chứa cặp Việt/Tây Ban Nha đo trực tiếp; hôm nay 19/7 → 15/8 = 27 ngày

**Đề xuất sửa.** Quyết định bỏ/giữ FAIR NGAY TUẦN NÀY thay vì 1/8 (mỗi ngày giữ FAIR là một ngày mất của VCL + luận văn); nếu giữ: cắt ngay ablation MV-aux, Tier2, ScreenSpot theo thứ tự 81 §cắt và chấp nhận bài FAIR chỉ có trục ĐÚNG; viết lại KE_HOACH §2 theo khung LAI trước khi làm gì khác; smoke-test sinh-tiếng-Việt + chấm-giữ-tên-nút-Anh (free với Qwen local) trước khi tin VCL là sàn

**Người phản-bác nói gì.** Phần kiểm kê repo của đòn ĐÚNG SỰ THẬT nhưng KHÔNG PHẢI PHÁT HIỆN: mọi hạng mục (a)(b)(c)(f) đều đã được tác giả tự khai bằng văn bản TRƯỚC đòn này, kèm biện pháp — KE_HOACH §0.4/§134, report/88 §7.6, report/81:209-216 (thứ tự cắt, AC-only làm sàn lui). Cái "trượt" mà đòn chỉ ra (FAIR) là hạng mục tác giả đã dán nhãn stretch-tuỳ-chọn với đường lui viết sẵn; luận văn — thứ thật sự đem bảo vệ — không nằm trong đường đạn. Đòn tự thừa nhận điều này rồi tự hạ trọng lượng của chính nó.

Hai chỗ đòn PHÓNG ĐẠI: (1) "chưa có dòng code train nào" — sai; toàn bộ pipeline dựng dữ liệu (dg3_*) đã viết và YAML train đầy đủ nằm sẵn report/53:182, trainer là config đút vào LLaMA-Factory chứ không phải hạng mục nghiên cứu. (2) "bài FAIR phải viết lại từ số 0" — bài chưa viết dòng nào, nên abstract lỗi thời là việc sửa 20 phút, không phải công sức mất trắng.

Chỗ đòn SAI HẲN là chính đòn leo thang mà nó tự quảng cáo là mới ("VCL cũng không an toàn như tưởng"). Đo lại tại chỗ: bge-m3 xử lý paraphrase tiếng Việt TỐT HƠN tiếng Anh (med 0.789 vs 0.702; kết-oan @τ=0.55 là 5.0% vs 10.7%; @τ=0.50 cả hai 0%) — embedding chính là nhánh CỨU được cross-lingual, không phải "không cứu". Còn 97.5% là bệnh của so-chuỗi thuần trên paraphrase nói chung: kết-oan EN 96.4%, gần bằng VI 100% — không phải thuế cross-lingual, và FAIR (Anh-Anh) dính y hệt. Chiều lỗi K1 thật sự chết (bịa gần-nghĩa) là chiều KHÔNG phụ thuộc ngôn ngữ, và K2 đo được nó ≈0% trong output teacher thật. Thêm nữa report/73:52 đã ghi sẵn cross-lingual là vấn đề riêng của VCL — ngay cả cách đặt vấn đề cũng không mới.

Hạ từ "nặng" xuống "nhẹ": cái sống sót không phải rủi ro khả thi mà là NỢ TÀI LIỆU — KE_HOACH_2_BAI_BAO.md (12/7) vẫn rao khung lọc-bịa đã bị K2 giết trong khi report/88 (19/7) đã đè lên. Đáng sửa để tác giả không lỡ tay soạn bài từ bản chết, nhưng không đe doạ luận văn.

**Bằng chứng của người kiểm.** KIỂM (a)-(e): (a) ĐÚNG — `ls /mnt/d/Master/Thesis/harness/*.py` không có train script, không có train_config.yaml; report/53:394 tự liệt kê nó vào "cần viết mới". Nhưng KHÔNG phải "chưa có dòng code train nào": dg3_freeze_split / dg3_train_questions / dg3_rewrite_fallback / dg3_render (build ShareGPT cho LLaMA-Factory) / dg3_eval_no_vh / dg3_stats / dg3_dedup_pool đều đã viết, và YAML train đầy đủ nằm sẵn ở report/53:182-192 — trainer là ~30 dòng YAML đút vào framework có sẵn, không phải hạng mục nghiên cứu. (b) ĐÚNG — dataset_samples/androidcontrol_test/ chỉ có ac_test_200ep.json (report/88 khai 631 ep app-unseen, đĩa không thấy). Đây là việc TẢI, free, tính bằng giờ. (c) ĐÚNG — không có matcher đa-tầng. (d) ĐÚNG nhưng là lựa chọn có chủ đích: report/81 tiêu đề ghi "user TỰ CHỐT đi LAI, không đợi thầy", report/88 §6.3 khai thẳng. (e) ĐÚNG NGUYÊN VĂN — KE_HOACH_2_BAI_BAO.md:60 vẫn là "training only on data whose fabricated button references have been filtered".

KIỂM đường lui (đòn tự thừa nhận nhưng hạ thấp): KE_HOACH §0.4:37 "VCL = sàn CHẮC · FAIR = stretch… Tuyệt đối không để canh bạc FAIR làm hỏng VCL"; :134 "nếu trễ → bỏ FAIR giữ VCL"; report/88 §7.6 rủi ro y hệt + biện pháp y hệt; report/81:209-216 thứ tự cắt, trong đó trục TRUNG THỰC (= hạng mục (c)) là thứ CẮT ĐẦU, AC-only là sàn lui hợp lệ. Trục ĐÚNG (headline) đã build + qua cổng: harness/metric_v1_validate.py, AUC=1.0.

BÁC BỎ phần cross-lingual (chạy lại local, ollama bge-m3, trên chính bộ neo LEX của k1_matcher_killtest.py, tách theo ngôn ngữ — script: scratchpad/xl.py):
- VI-paraphrase (n=20): min 0.547 / med 0.789 / max 0.885
- EN-paraphrase (n=28): min 0.530 / med 0.702 / max 0.928
- near-syn/bịa (n=54): min 0.439 / med 0.589 / max 0.802
- kết-oan @τ=0.50: VI 0.0% · EN 0.0% | @τ=0.55: VI 5.0% · EN 10.7% | @τ=0.65: VI 10.0% · EN 25.0%
→ bge-m3 xử lý tiếng Việt TỐT HƠN tiếng Anh ở MỌI ngưỡng.
- Lexical (token-Jaccard <0.5) kết-oan: VI 100% · **EN 96.4%** → con số 97.5% KHÔNG phải hình phạt cross-lingual, so-chuỗi thuần chết trên paraphrase CÙNG ngôn ngữ gần y hệt.
- report/73:52 đã tự ghi "Cross-language kết-oan là vấn đề riêng của VCL" + :56-57 đã chốt hướng sửa (so-chuỗi + embedding + OCR) — không phải phát hiện mới.
- K2 (report/74): bịa gần-nghĩa thật ≈ 0/40 → đúng chiều lỗi mà embedding thua thì thực tế gần như không xảy ra.

---


## C. 12 đòn ĐÃ BỊ BÁC BỎ (ghi lại để khỏi lo oan, và để nếu ai hỏi thì có sẵn câu trả lời)

### C1. ~~Chính script tự in cảnh báo RỚT cho 2/3 loại lỗi, nhưng report/84 đánh dấu ✓ và kết luận QUA CỔNG~~

- **Đòn gốc (trục THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, m):** Tôi chạy lại nguyên văn script của tác giả. Output in ra '⚠ KHÔNG tụt đủ' cho action_error (Δ=0.149 < ngưỡng 0.15) và cho missing (Δ=0.150, sát mép, điều kiện drop<0.15 kích hoạt do sai số dấu phẩy động: 1.0−0.850933=0.1490670; missing 1.0−0.8503649=0.1496351). Bảng ở report/84:17-18 ghi cả hai là '✓'. Thêm nữa, trần lý thuyết cho một bộ đối chiếu HOÀN HẢO khi chỉ hỏng 1 bước là E[1/L]=0.221 (185 ep, độ dài TB 5.55) — nên tỉ lệ phát hiện THẬT ở mức coverage chỉ là 0.153/0.221=69% (target), 67% (action), 68% (missing), KHÔNG phải 'detection = 1.000' như báo cáo (con số 1.000 đo trên kênh khác — min target-score per-episode — chứ không đo trên thước headline là coverage). Và bản thân ngưỡng 0.

- **Vì sao bị bác:** Đòn đúng về mặt quan sát bề mặt (script thật sự in cảnh báo) nhưng lõi định lượng — "tỉ lệ phát hiện thật chỉ 67-69%, không phải 1.000" — bị bác bằng đo trực tiếp, nên không thể giữ mức chí mạng.

1) Sai mẫu số. Đối thủ lấy trần E[1/L]=0.221, ngầm giả định không gold step nào trùng trong cùng episode. Tôi đo được 392/1027 = 38,2% gold step bị một bước khác trong CÙNG episode phủ lại (lặp nguyên văn, hoặc lồng nhau như 'Click on Tools' vs 'Click on Tools & Hardware'). Trần thật cho một matcher HOÀN HẢO dưới đúng sơ đồ bơm-lỗi này = 0.1538. So lại: missing 0.1496 = 97,2% trần; action_error 0.1491 = 96,9%; target_error 0.1530 = 99,5%. Thước gần như chạm trần khả thi, không phải "hụt 31%".

2) 0.15 KHÔNG phải cổng. Grep report/84 và report/85: con số 0.15 không xuất hiện ở đâu như ngưỡng. Cổng đăng-ký-trước (report/85:47-53) = detection≥0.90, FP≤0.10, AUC≥0.80, cả ba đo riêng và đều qua. Cột "✓" ở report/84:17-18 có tiêu đề "Đúng kỳ vọng?", kỳ vọng ghi rõ "1 bước/~5 sai → tụt ~1/5", không phải "≥0.15". Đòn đánh đồng một dòng print chẩn-đoán trong script với cổng chính thức.

3) "detection=1.000 đo kênh khác" đúng về mô tả nhưng không phải lỗi: detection-rate trong perturbation-validate (Sai EMNLP 2021) VỐN định nghĩa per-injected-error, còn coverage là tổng hợp cấp-episode bị pha loãng 1/L theo thiết kế. Report không hề claim coverage-level detection = 1.000.

4) Ý (3) của đối thủ (0.15 là hàm độ dài episode) đúng, nhưng lật ngược kết luận của chính họ: hằng số 0.15 nằm ngay DƯỚI trần thật 0.1538, nên một matcher hoàn hảo cũng chỉ vượt với biên 0.0038. Cảnh báo in ra là tạo tác của hằng số đặt ẩu, không phải bằng chứng thước hỏng.

5) Đính chính: "kích hoạt do sai số dấu phẩy động" là sai — 0.149067 và 0.1496351 thật sự dưới 0.15, chỉ hiển thị làm tròn lên 0.150.

Cái còn s

---

### C2. ~~Thước headline mới xây được 1/3: F1 và order-τ chưa tồn tại trong code, nhưng đã được đóng băng và đánh ✓ trong pre-registration~~

- **Đòn gốc (trục THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, m):** report/85:35 định nghĩa headline = coverage-recall + F1 (chống nhồi bước thừa) + order-τ partial (Fagin). Trong toàn bộ harness/ không có hàm F1, không có precision, không có order-τ/Fagin nào. Chỉ coverage tồn tại. Hệ quả đo được ngay trong kết quả của chính tác giả: extra Δ=0.000 và reorder Δ=0.000 — thước đã-validate MÙ HOÀN TOÀN trước bước thừa bịa ra và trước thứ tự sai. Với một luận văn mà đóng góp là chống bịa và output là hướng dẫn tuần tự cho người, đó là hai lỗ đúng vào tim. Nghiêm trọng hơn: report/85:51 đánh dấu '✓' cho dòng 'đảo thứ tự → order-τ tụt, coverage GIỮ' — tức đóng dấu đạt cho một thành phần chưa được viết.

- **Vì sao bị bác:** Phần dữ kiện thô của đòn ĐÚNG (F1/precision/order-τ chưa có trong code), nhưng ba mệnh đề làm nên sức nặng của nó đều sai hoặc đã bị tác giả xử lý sẵn.

(1) "F1 đã được đóng băng và đánh ✓" — SAI. Bảng cổng validate ở report/85 dòng 45-51 có đúng 5 dòng: detection sai-target, detection sai-action, FP paraphrase, AUC tách-phân-phối, và dòng thứ tự. KHÔNG có dòng nào cho F1. F1 chỉ xuất hiện ở §3 (dòng 35) như định nghĩa headline, không hề được tick, không hề có ngưỡng. Đòn gộp F1 vào cáo buộc "đóng dấu đạt cho thành phần chưa viết" là dựng thêm.

(2) "Δ=0 ở extra/reorder = thước MÙ HOÀN TOÀN, hai lỗ vào tim" — đây là đọc ngược. Coverage-recall bất biến với chèn thêm và với hoán vị là TÍNH CHẤT TOÁN HỌC của nó, không phải khiếm khuyết phát hiện được. Tác giả không những biết mà đã ghi thẳng trong report/84 ngay tại hai dòng đó: extra → "✓ (không giảm coverage; bắt bằng precision)"; reorder → "✓ (đúng thiết kế: coverage không đổi, đảo thứ tự đo bằng order-τ RIÊNG)". Mạnh hơn nữa, code có cờ cảnh báo NGƯỢC chiều: metric_v1_validate.py:176 chỉ in cảnh báo khi reorder LÀM TỤT coverage >0.10. Tức Δ=0 là điều kiện ĐẬU đã đặt trước, không phải điểm mù bị bắt quả tang. Chính vì coverage bất biến như vậy mà prereg mới phải kê thêm F1 và order-τ — Δ=0 là luận cứ cho thiết kế ba thành phần, không phải bằng chứng chống lại nó.

(3) "chưa tồn tại mà đã đóng băng" — hiểu sai bản chất pre-registration. Prereg đóng băng ĐỊNH NGHĨA trước khi chạy; kê một thước chưa code xong là đúng thứ tự, không phải gian lận. §4 ghi rõ ngay ở tiêu đề "đã chạy synthetic report/84, phải chạy lại trên config cuối" và lặp lại ở cổng cứng dòng 53.

Không có kết quả nào bị nhiễm: chưa train, chưa có so Student vs Teacher-BASE nào chạy dưới headline. File duy nhất có số (mde_pilot_results.json) chỉ chứa mean/s

---

### C3. ~~Pilot MDE đo một tác vụ DỄ HƠN hẳn tác vụ sẽ eval — kết luận 'không suy biến sàn-0' không chuyển giao được~~

- **Đòn gốc (trục THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, m):** mde_pilot.py đưa cho teacher ĐÚNG ảnh của từng bước (episode_{eid}_screenshot_{si}.png, dòng 72) và yêu cầu sinh MỘT bước kế tiếp cho chính màn đó, rồi chấm với gold[si]. Nhưng hợp đồng I/O của luận văn (report/85 §0) là MỘT ảnh + câu hỏi → TOÀN BỘ chuỗi bước của episode, mà episode trải qua nhiều màn model chưa từng thấy. Điểm 30% vì thế thu được trong điều kiện quan sát đầy đủ từng màn — nó là CẬN TRÊN xa của điều kiện thật, và hoàn toàn có thể setting thật vẫn suy biến sàn-0. Cổng go/no-go của report/79 được tuyên bố là đã qua dựa trên con số này. Ngoài ra pilot còn lọc chỉ giữ bước có gold action ∈ {click, long_press, input_text} (dòng 69), loại scroll/navigate_back/open_app/wait — tức m

- **Vì sao bị bác:** Đòn sập ở CẢ BA chân, hai chân bị bác bằng số đo được, một chân bị bác bằng chính văn bản họ trích thiếu.

**Chân 1 — "pilot đo per-step, eval là 1-ảnh→cả-episode" → SAI PREMISE.** Người ra đòn suy điều kiện eval từ một dòng quảng cáo đóng góp (report/85:11 "từ 1 ảnh + câu hỏi") rồi coi đó là hợp đồng I/O của trục ĐÚNG. Nhưng thiết kế nói ngược, và nói rất rõ ở chỗ họ không mở:
- `report/88:166` (kế hoạch dựng data, mục 5.1): *"Mỗi mẫu huấn luyện = (ảnh màn hình tại một bước) + (mục tiêu tổng thể + các bước đã làm) → (hướng dẫn do người viết cho bước đó)"*; `:167` *"khi thấy một màn hình và biết mục tiêu, sinh ra đúng câu hướng dẫn cho bước kế tiếp"*.
- `report/81:130-131` sơ đồ pipeline tách rạch ròi HAI định dạng nguồn: **AndroidControl = "ảnh + gold step_instruction"** (per-step), **MobileViews = "ảnh + câu hỏi"** (một-màn). Cụm "1 ảnh + câu hỏi" là nhánh MobileViews/khung sản phẩm, KHÔNG phải điều kiện của trục ĐÚNG.
Tức pilot đo ĐÚNG đơn vị mà trục ĐÚNG đã đặc tả. Hơn nữa pilot còn KHẮC NGHIỆT HƠN thiết kế: prompt ở `mde_pilot.py:27-30` chỉ có goal + ảnh, KHÔNG có "các bước đã làm" mà `88:166` cho model dùng lúc train/eval. Pilot bỏ bớt context → là cận DƯỚI, không phải "cận trên xa".

**Chân 2 — "lọc action type → mẫu dễ hơn phân phối eval" → ĐO ĐƯỢC LÀ NGƯỢC LẠI.** Tôi chạy lại trên 1042 bước AC-test local, chấm bằng chính thước `metric_v1_validate`, với một "teacher mù" thuần luật (KHÔNG nhìn ảnh):
| loại bị loại | n (%) | điểm của đoán-công-thức MÙ |
|---|---|---|
| open_app | 72 (6,9%) | **97,2%** |
| navigate_back | 44 (4,2%) | **54,5%** |
| scroll | 118 (11,3%) | 18,6% (fixed "Swipe up", sàn mù) |
Gold của các loại này formulaic tới mức đoán mù đã gần trần ("Open the amazon app", "Go back to the previous page"). So với 30,1% teacher đạt trên nhóm ĐƯỢC GIỮ (c

---

### C4. ~~G=150-250 lấy từ SAI POPULATION — con số MDE 8-9 pp treo trên một G không tồn tại~~

- **Đòn gốc (trục THỐNG KÊ + LỰC MẪU (MDE trục ĐÚNG, wild-cluster bootstrap vs):** report/85:19 và report/86:22 chốt "G ~150-250 app" dựa trên "~114 app distinct trong 200 ep" và "phủ ~72% ep". Nhưng 200 ep đó là mẫu của TOÀN BỘ test set AC, KHÔNG phải app_unseen split — mà app_unseen theo định nghĩa là tập app bị giữ lại, nên đa dạng app thấp hơn hẳn. Chính repo có artifact đếm đúng population và nó mâu thuẫn thẳng.

- **Vì sao bị bác:** Đòn đúng một nửa về NGUỒN GỐC con số, nhưng SAI hẳn ở phần định lượng — và chính phần định lượng mới là chỗ họ xếp "chí mạng".

1) Phần đúng (nhỏ): tôi xác nhận mẫu 200 ep trong `dataset_samples/androidcontrol_test/ac_test_200ep.json` KHÔNG phải app_unseen — chỉ 79/200 ep nằm trong danh sách `app_unseen` (631 id, lấy từ reece124/android_control). Nên câu "~114 app distinct trong 200 ep / phủ ~72%" ở report/85:19 đúng là đếm trên full test set. Đây là lỗi trích nguồn, phải sửa.

2) Phần SAI (quyết định): kết luận "G thật ≈ 42, Chao1 ≈ 72" của họ không tái lập được. Tôi chạy CHÍNH `app_of()` (mde_pilot.py:32-37) trên 327 episode app_unseen có sẵn trong HF cache local (nhiều hơn mẫu 250 của họ, và là episode THẬT đã tải, không phải ước lượng): tỉ lệ gán được app = 257/327 = 78,6% (KHÔNG phải 40,8% như artifact của họ), distinct = 107, Chao1 = 220. Sau khi gộp biến thể do regex ("Arts & Culture" vs "Art & Culture", "In the Pinterest" vs "Pinterest", "Newyork times" vs "NYTimes"): distinct = 85 trên 327 ep, Chao1 = 137. Tức riêng HƠN MỘT NỬA split đã cho 85-107 app distinct — không có cách nào tổng 631 ep chỉ còn 42-72 app. Giả thuyết lý thuyết của họ ("app_unseen là tập app bị giữ lại nên đa dạng thấp hơn hẳn") bị chính số liệu bác: đuôi dài singleton ở app_unseen y hệt full test (f1=38, f2=14).

3) Artifact họ dựa vào (`harness/ac_app_unseen_count.json`, sampled=250, with_app=102) không có script sinh ra nó trong repo (grep toàn repo: 0 hit), và tỉ lệ gán-nhãn 40,8% của nó lệch gần 2 lần so với đo trực tiếp 78,6% trên episode thật → nhiều khả năng vòng lấy mẫu của họ đếm cả episode tải hỏng/thiếu trường `actions` vào mẫu số. Không tái lập được thì không đủ tư cách làm bằng chứng "chí mạng".

4) Ngay cả khi chấp kịch bản xấu của họ, kết luận của report/86 vẫn không đổ: G=42

---

### C5. ~~SD=0.256 KHÔNG phải độ dao động giữa app — nó gần như 100% là nhiễu nhị thức của việc chỉ chấm 3,5 bước/app~~

- **Đòn gốc (trục THỐNG KÊ + LỰC MẪU (MDE trục ĐÚNG, wild-cluster bootstrap vs):** Toàn bộ MDE dựng trên SD per-app đo từ điểm số mỗi app tính trên 2-4 bước nhị phân. Với n nhỏ như vậy, SD quan sát được là nhiễu lấy mẫu, không phải phương sai cụm. Hệ quả: SD này KHÔNG chuyển được sang thực nghiệm thật (mỗi app sẽ có nhiều bước hơn hẳn) — nó là hàm của tham số STEPS_PER_APP=4 trong script, không phải thuộc tính của tổng thể.

- **Vì sao bị bác:** Cơ chế họ nêu (nhiễu nhị thức chiếm gần hết SD) ĐÚNG và tôi tái lập được — nhưng HỆ QUẢ họ rút ra thì SAI, và tác giả đã khai chính cơ chế đó rồi. Ba lý do bác:

(1) TÁC GIẢ ĐÃ XỬ LÝ. report/86 mục "Đọc kỹ" §2 viết nguyên văn: "MDE này BẢO THỦ (overestimate): pilot chỉ 2-4 bước/app → điểm per-app nhiễu → SD phồng." Đòn trình bày cơ chế này như một phát hiện bị giấu, trong khi nó là một trong bốn caveat được in ra ngay dưới bảng MDE.

(2) TIỀN ĐỀ THỰC NGHIỆM CỦA ĐÒN SAI. Trụ của đòn là "SD KHÔNG chuyển được sang thực nghiệm thật (mỗi app sẽ có nhiều bước hơn hẳn)". Tôi kiểm split thật: harness/ac_app_unseen_count.json cho 42 app distinct / 102 ep có gán app, phân bố **52,4% app chỉ 1 episode, 71,4% ≤2 ep, median = 1,0 ep/app**. Đếm bước click/long_press/input_text trên 200 ep thật (dataset_samples/androidcontrol_test/ac_test_200ep.json): **mean 3,73 · median 3,0 bước dùng được mỗi episode**. → App TRUNG VỊ của thực nghiệm thật có ~3 bước, tức BẰNG HOẶC ÍT HƠN pilot (3,5). Nhiễu nhị thức per-app không phải tạo tác của STEPS_PER_APP=4; nó là thuộc tính nội tại của estimand macro-per-app trên một phân bố app đuôi-dài toàn singleton. SD chuyển được gần 1:1. Trớ trêu: câu này bác luôn cả lý do tác giả nêu ở (1) — SD sẽ không co lại như tác giả tưởng — nhưng đó là sai theo hướng AN TOÀN, MDE ≈ 9 pp vẫn đúng như đã báo.

(3) KẾT LUẬN SỐNG NGUYÊN DÙ CHẤP NHẬN TRỌN PHÂN RÃ CỦA HỌ. MDE là cổng GO/NO-GO lực thống kê: 9 pp < ngưỡng 15-20 pp. Nếu SD phồng vì nhiễu thì MDE thật NHỎ HƠN → cổng càng dễ qua. Tôi tính lại bằng chính Var-giữa-app của họ (0,0055): n̄=10 → MDE 5,8 pp; n̄=15 → 5,0 pp; n̄=20 → 4,5 pp. Mọi kịch bản đều dưới ngưỡng rất xa. Không có con số hay quyết định nào bị lật. Thêm nữa, ICC≈0 mà họ chứng minh lại là lý lẽ CHO thiết kế: wild-cluster bootstrap khi ICC≈0 là bả

---

### C6. ~~SD của HIỆU-SỐ chưa hề được đo — √2×SD_teacher là giả định, và nhãn "bảo thủ" chưa được chứng minh~~

- **Đòn gốc (trục THỐNG KÊ + LỰC MẪU (MDE trục ĐÚNG, wild-cluster bootstrap vs):** Pilot chỉ đo teacher zero-shot. SD dùng để lập kế hoạch cho hiệu Student−Teacher được suy ra bằng nhân √2. Việc này giả định đồng thời (a) hai arm ĐỘC LẬP — nhưng thiết kế là ghép cặp trên cùng app/cùng bước, và (b) Var(student)=Var(teacher) — chưa có một điểm dữ liệu student nào.

- **Vì sao bị bác:** Đòn tự đánh đổ mình ở ba điểm, đều kiểm được bằng số.

Thứ nhất, chiều tác động ngược. Đòn nêu thiết kế là GHÉP CẶP (cùng app, cùng bước) như một khiếm khuyết, rồi lại tính phản ví dụ ở ρ=0. Nhưng Var(d)=Var(s)+Var(t)−2ρ·SD_s·SD_t: chính việc ghép cặp làm √2 trở nên bảo thủ. Hai arm chấm trên CÙNG ảnh, CÙNG goal, CÙNG gold; report/86:26 còn nêu thước phạt cả "bước hợp lệ khác gold" — nhiễu cấp-item đánh đồng đều hai arm, ép ρ>0 về mặt cấu trúc. Đòn phải giả định triệt tiêu đúng đặc tính thiết kế mà nó viện dẫn.

Thứ hai, nhầm giữa phương sai và SD. MDE tỉ lệ với SD chứ không với Var. Con số 0.46 vs 0.42 của họ = +9.5% Var = +4.7% SD → MDE 9.1 → 9.5 pp, so với ngưỡng nguy hiểm đã đăng-ký-trước 15-20 pp. "Thiếu ~10%" là phóng đại hơn gấp đôi tác động thật.

Thứ ba, và quyết định nhất: tiền đề của họ (phương sai chủ yếu là nhị thức per-bước) tôi kiểm ra ĐÚNG — 92% Var per-app của pilot là nhiễu lấy mẫu từ chỉ 3.5 bước/app, Var giữa-app thật chỉ 0.0055. Mà n̄=3.5 là do trần cứng `STEPS_PER_APP = 4` trong mde_pilot.py:22, không phải giới hạn dữ liệu. Ở n≈8 bước/app thực tế (suy từ ac_app_unseen_count.json), chạy đúng kịch bản xấu nhất của họ vẫn cho SD_hiệu=0.262 so với 0.362 kế hoạch — kế hoạch dư 38%. Nhãn "bảo thủ" vì thế KHÔNG phải giả định chưa chứng minh: nó đúng, chỉ là đúng vì lý do khác với dòng comment trong code, và report/86:27 đã ghi rõ lý do đó ("pilot chỉ 2-4 bước/app → SD phồng") — dòng mà đòn bỏ qua khi liệt kê bằng chứng.

Còn sót một mẩu thật nhưng vô hại: chưa có điểm dữ liệu student nào, nên comment mde_pilot.py:108 biện minh √2 bằng chữ "bảo thủ" mà không nêu giả định là mỏng về tài liệu. Đáng thêm một dòng caveat vào report/85 rằng SD_hiệu sẽ được ước lượng lại từ dữ liệu ghép-cặp thật lúc phân tích. Đó là việc biên tập, không phải lỗi thiết kế: kết lu

---

### C7. ~~Độ phủ nhãn app trên split đánh giá là ~41%, không phải 72%; phần thiếu bị DROP âm thầm~~

- **Đòn gốc (trục DỮ LIỆU, SPLIT, RÒ RỈ — và câu hỏi "vừa học vừa chấm cùng lo):** report/85 ghi phủ ~72% và hẹn 'gán tay phần còn lại'. Trên đúng split app_unseen con số là 40,8%. Nghĩa là ~370 ep phải gán tay — chi phí chưa khai. Nghiêm trọng hơn: code pilot bỏ luôn ep không có nhãn, nên mẫu phân tích là tập con CHỌN LỌC (ep mà goal có nhắc tên app hoặc có open_app), estimand không còn là split app_unseen.

- **Vì sao bị bác:** Đòn dựa trên một phép đếm SAI LUẬT. Luật gán app đã đăng ký (report/85:19, hàm app_of tại harness/mde_pilot.py:31-36) là open_app-action CỘNG trích-từ-goal. File harness/ac_app_unseen_count.json mà người ra đòn viện dẫn chỉ đếm nhánh open_app, bỏ hẳn nhánh regex-goal — nên ra 40,8%. Đo lại bằng đúng luật đăng ký trên mẫu không thiên lệch 327 ep thuộc app_unseen: phủ 78,6%, tức CAO HƠN con số 72% mà report/85 khai, không phải thấp hơn một nửa. Hệ quả: (a) claim "41% không phải 72%" sai; (b) claim "hai file khác quần thể" sai nguyên nhân — khác LUẬT chứ không khác quần thể (kiểm chéo: cùng luật đầy đủ, ep ngoài app_unseen phủ 63,6% < app_unseen 78,6%); (c) "~370 ep phải gán tay" sai tỉ lệ, thực tế ~135 ep, và report/85 đã khai trước là "gán tay/GCS lúc build". Vế duy nhất đúng về mã là mde_pilot.py:60-62 có drop ep không nhãn, nhưng script đó chỉ ước SD per-app để tính MDE (report/86), không sinh estimand nào, nên không phá estimand của phân tích đã đăng ký; report/86 cũng đã tự khai MDE là cận-trên bảo thủ. Ghi nhận riêng (không thuộc đòn này): nhãn app từ regex-goal bẩn thật, mde_pilot_results.json có cụm rác và tách đôi cùng app — cần chuẩn-hoá tên app trước khi build, nhưng đó là vấn đề khác.

---

### C8. ~~K2 không có code phân loại — bảng 6 dòng quyết định số phận luận văn chỉ tồn tại trong văn xuôi~~

- **Đòn gốc (trục Bốn phép thử K1 / K2 / OCR / VIỆC1 — có bị khái quát quá khô):** `k2_hallucination_types.py` chỉ làm hai việc: đếm verbatim và in danh sách ca không-verbatim ra màn hình. Nó KHÔNG phân loại gì. Bảng trong report/74 (icon 20 / field 11 / chữ-hoa 4 / placeholder 3 / khác 2 / bịa-gần-nghĩa 0) không có trong code, không có trong k2_results.json, không có rubric viết trước, không có rater thứ hai, không có κ. Chính tài liệu tự khai là KHÔNG XEM ẢNH. Vậy căn cứ để nói "nút THẬT bị VH bỏ nhãn" là: một trợ lý AI nhìn chuỗi element + ghi chú của teacher rồi tự đoán, sau đó tự dùng kết luận của mình làm bằng chứng đảo ngược khung đóng góp. Đây là mắt xích suy luận yếu nhất trong toàn dự án và nó đang chịu tải nặng nhất. Cụ thể ca '+': không xem ảnh thì không thể ph

- **Vì sao bị bác:** Đòn mô tả ĐÚNG về mặt code (không có nhánh phân loại, JSON không có trường nhãn, không rubric/rater-2/κ, report/74:49 tự khai không xem ảnh) — nhưng KẾT LUẬN "không thể phân biệt thật/bịa" bị bác bằng chính dữ liệu có sẵn, và ví dụ chủ lực của đòn ('+') sai hẳn.

(1) BÁC ví dụ chủ lực: đòn nói không xem ảnh thì không phân biệt được "FAB thật VH thiếu nhãn" vs "teacher suy từ prior". Tôi kiểm: cả 15 màn có '+' đều chứa nhãn VH literal "Floating Action Button Menu". Tương tự '<'/'>' → màn có "Go to previous"/"Go to next"; '✓' → màn có "Submit". Toàn bộ nhóm icon 20 ca (dòng lớn nhất bảng) được chứng thực bằng kiểm tra tái lập được, KHÔNG cần ảnh. Giả thuyết thay thế của đòn bị loại bằng dữ liệu.

(2) Nửa còn lại cũng đứng, qua phép kiểm đòn không nghĩ tới: teacher sinh MÙ (không thấy VH). Đối chiếu chuỗi non-verbatim với nhãn VH ở màn KHÁC cùng app: Project name(4), Find or create a contact (required)(2), Add a description (optional)(2), ADD LOCATION, EXPENSES, OK, 30 = 12 ca nữa. Model mù tái tạo đúng từng ký tự chuỗi đặc thù như "Find or create a contact (required)" nghĩa là nó ĐỌC TỪ PIXEL → nút có thật, chứng minh không cần ảnh.

(3) Tổng: 32/40 ca có bằng chứng tái lập được. 8 ca còn lại gồm 3 artifact <...> (report/74 đã xếp là rác khuôn mẫu, không phải tên nút) + 2 từ chỉ loại control (slider/toggle) → chỉ 3 ca thực sự chưa ngã ngũ (ADD NEW x2, Refresh), và không ca nào thuộc loại near-synonym mà K1 lo (sim thấp, matcher vẫn bắt). Headline "bịa-gần-nghĩa = 0" SỐNG.

(4) "Chịu tải nặng nhất" phóng đại: tải chạy theo hướng THU HẸP (K2 làm BỎ một đóng góp, không phải khẳng định thêm). Kết luận vận hành của K2 có hậu thuẫn độc lập bằng code: ocr_coverage_results.json đo recall_vh_micro=0.698 → ~30% phần tử actionable không có nhãn VH, định lượng đúng cơ chế mà bảng văn

---

### C9. ~~"Không τ nào tách được" đúng với nomic nhưng SAI với bge-m3; suy rộng "⇒ OpenAI cũng vậy" không có dữ liệu~~

- **Đòn gốc (trục Bốn phép thử K1 / K2 / OCR / VIỆC1 — có bị khái quát quá khô):** Thống kê chồng-lấn mà K1 dùng là "số ca nearsyn có sim ≥ min(sim của paraphrase)" — tức so với giá trị THẤP NHẤT trong 40 mẫu, một thống kê thứ tự cực trị gần như chắc chắn ra 40/40 dù hai phân phối tách khá tốt. Tôi tính AUC (thước tách-phân-phối đúng): nomic 0,525 → kết luận "không tách được" ĐÚNG cho nomic, tôi xác nhận. Nhưng bge-m3 ra 0,677, và tại τ=0,55 bge-m3 cho precision 95,5% với kết-oan paraphrase chỉ 2,5% — đó là một điểm vận hành dùng được, không phải "rớt". Vậy câu "embedding mạnh hơn (kể cả OpenAI) chỉ đỡ chút, không phải lời giải" vừa nói quá về bge-m3, vừa suy diễn về một model chưa hề chạy. CLAUDE.md còn cứng hơn nữa: "bge-m3 đỡ chút, không giải quyết (⇒ OpenAI cũng vậy)" 

- **Vì sao bị bác:** Đòn sập ở cả hai chân chính. Chân "CLAUDE.md ghi sai 40/40": đọc nhầm chủ ngữ — 40/40 là số của nomic, báo cáo gốc ghi rõ bge-m3 = 30/40. Chân "bge-m3 thật ra tách được": chỉ đúng nếu che cột recall. Điểm τ=0,55 mà giám khảo gọi là "vận hành dùng được" bỏ lọt 75% bịa gần-nghĩa — tệ hơn hẳn nomic tại cùng τ; còn điểm κ tốt nhất của bge-m3 (τ=0,70) thì kết oan 55% paraphrase. Đúng nghĩa bập bênh, đúng kết luận "đỡ chút, không giải quyết". Mỉa mai nhất: thước AUC mà giám khảo mang vào để lật lại là thước luận văn đã đóng băng ngưỡng ≥0,80 (report/84/85) — bge-m3 0,677 rớt ngưỡng đó. Phê bình phương pháp (thống kê cực trị) hợp lý về nguyên tắc nhưng vô hại ở đây, vì kết luận không treo trên nó mà trên bảng quét τ hai chiều. Hạt nhân CÒN SỐNG duy nhất: cụm "(kể cả OpenAI)" ở report/73:31 và "⇒ OpenAI cũng vậy" ở CLAUDE.md là suy diễn từ 2 họ embedding, chưa chạy — nên viết là "dự đoán, chưa kiểm" thay vì khẳng định. Đây là sửa CÂU CHỮ, không đụng thiết kế: hướng xử lý đã chọn không phải "mua embedding xịn hơn" mà là đổi cấu trúc trọng tài (tách (action,target) → AUC 1,000 ở report/84, kể cả ca khó "artworks tab" vs "energy tab"), nên dù OpenAI có nhỉnh hơn cũng không lật quyết định nào. Thêm nữa K2 (report/74) cho thấy teacher bịa ~0-2%, làm nhánh này càng ít trọng lượng.

---

### C10. ~~Cả bốn phép thử chạy trên MobileViews (bot thu thập) nhưng được dùng để biện minh thiết kế trên AndroidControl (người thật) — và trục mới thậm chí không dùng nhãn VH~~

- **Đòn gốc (trục Bốn phép thử K1 / K2 / OCR / VIỆC1 — có bị khái quát quá khô):** Đây là vấn đề khái quát hoá lớn nhất, xét ở mức toàn trục. K1/K2/OCR/VIỆC1 đều đo một thứ: chất lượng nhãn View Hierarchy của MobileViews (độ phủ 62,4%), trên dữ liệu bot VLM-DroidBot sinh ra, với K2 thì trên đúng một app. Bốn kết luận đó đang được dùng để: bỏ Tier 1, thiết kế lại trọng tài, và đẩy trục ĐÚNG lên chính. Nhưng trục ĐÚNG mới so hướng-dẫn-model với gold step_instructions dạng VĂN BẢN của AndroidControl — không đụng tới nhãn VH chút nào. Nên phát hiện "VH thiếu nhãn gây kết-oan" gần như không chuyển giao sang trục nó đang được viện dẫn để biện minh. Ngược lại, thứ DUY NHẤT thật sự cần chuyển giao — teacher có bịa trên AndroidControl không, tức tiền đề của cả khung distillation — 

- **Vì sao bị bác:** Các dữ kiện họ nêu ĐÚNG (tôi xác minh từng cái), nhưng mệnh đề trung tâm — "bốn phép thử MobileViews được dùng để biện minh thiết kế trên AndroidControl" — sai, và sai theo cách kiểm được bằng file trong repo.

**1) Không có "chuyển giao" nào cả — miền khớp miền.** report/85 chia hai trục rạch ròi: trục TRUNG THỰC (§21, §57) chạy TRÊN MobileViews VH, split 18/12; data aux chưng-cất (§27) LÀ MobileViews; Tier 1 bị hạ (§58) là readout của chính cặp teacher-MobileViews. Cả ba quyết định mà đòn liệt kê ("bỏ Tier 1, thiết kế lại trọng tài, đẩy trục ĐÚNG lên chính") thì hai cái đầu nằm nguyên trong miền MobileViews — đo ở đâu kết luận ở đó, không ngoại suy.

**2) Trục ĐÚNG được biện minh bằng ba nghiên cứu AC-bản-địa, không phải bằng K1/K2.** report/81:165-167 ghi rõ lý do đẩy trục ĐÚNG lên chính là (a) report/79 — pilot chạy trên ảnh AC thật, phát hiện gold `step_instructions` phủ ~100% bước và khung toạ độ khớp; (b) xoá confound parallel-trends của khung cross-dataset report/78. Cộng thêm report/84 (cổng thước, `metric_v1_validate.py` DATA = `ac_test_200ep.json`, 185 episode AC) và report/86 (`mde_pilot.py`, 26 app AC app_unseen, ảnh thật). Đòn không nhắc tới ba cái này.

**3) Câu "phát hiện K1 gần như không chuyển giao" là đọc sai chính K1 — và đã bị bác bằng số TRÊN AndroidControl.** K1 không kết luận "VH MobileViews thiếu nhãn"; nó kết luận "cosine embedding một mình KHÔNG tách được bịa-gần-nghĩa khỏi paraphrase" — tính chất của BỘ ĐỐI CHIẾU, không phải của dataset. Bài học đó được cấy thẳng vào thước mới (tách action∧target) và **chạy lại đúng trên AC**: `harness/metric_v1_results.json` cho `separation_auc = 1.0`, `detection_target = 1.0`, `fp_paraphrase = 0.0`, kể cả ca khó cùng-từ-loại khác-entity. Nghĩa là thứ đòn bảo "không chuyển giao được" thì tác giả đã chuyển gi

---

### C11. ~~MÂU THUẪN cứng: G=150-250 app trong pre-registration bị chính file số của repo bác (42 app / 250 ep) — MDE thật ~13-17pp chứ không phải 8-9pp~~

- **Đòn gốc (trục TRUNG THỰC BÁO CÁO — đối chiếu prose (report/73-86, 88, CLAU):** Toàn bộ lập luận "trục ĐÚNG ĐỦ LỰC" đứng trên một con số duy nhất: số cụm (app) G ở split app_unseen. report/85 §1 và report/86 khẳng định G ≈ 150-250, suy ra MDE 8-9pp, dưới ngưỡng nguy hiểm 15-20pp. Nhưng con số 150-250 được suy từ "~114 app distinct trong 200 ep" — mà 200 ep đó là mẫu TEST CHUNG của AndroidControl, KHÔNG phải split app_unseen. Chính repo có một file đo TRỰC TIẾP split app_unseen: 250 ep → chỉ 42 app distinct, và chỉ 102/250 (40,8%) ep gán được app. Hai quần thể khác hẳn nhau: tôi tính lại trên mẫu test chung local được 67% gán được app / 103 distinct (khớp con số 72%/114 mà report dùng), còn app_unseen thì 41%/42 — vì app_unseen là một miền HẸP (nhìn danh sách app: gần nh

- **Vì sao bị bác:** Đòn này sụp ở đúng chỗ nó tự tin nhất: nó SO SÁNH HAI PHƯƠNG PHÁP GÁN APP KHÁC NHAU rồi quy toàn bộ chênh lệch cho "app_unseen là miền hẹp".

1) TÔI ĐÃ ĐO TRỰC TIẾP, KHÔNG NGOẠI SUY. Tải trọn 631/631 episode app_unseen (reece124 index → wangyuanlei/android_control_test) và chạy đúng hàm app_of() của mde_pilot.py — chính phương pháp report/85 đặc tả ("open_app-action + trích-từ-goal"). Kết quả CENSUS: with_app = 488/631 = 77,3%; DISTINCT APPS = 141. Không phải 42, không phải "tối đa ~106, thực tế 60-85". Ngoại suy tuyến tính mà đòn gọi là "đã là cận trên" thực ra là CẬN DƯỚI hụt 35%.

2) MDE THẬT KHỚP REPORT, KHÔNG PHẢI 13-17pp. Dùng đúng công thức mde_pilot.py:116 và SD-hiệu 0,362: G=141 → MDE = 9,4pp. Dùng hằng số t đúng cho G lớn (2,80 — chính đòn thừa nhận 3,077 là hằng số G=12 bảo thủ) → 8,5pp. Tức "8-9 pp" của report/86 là ĐÚNG theo nghĩa đen. Xa hẳn ngưỡng nguy hiểm 15-20pp.

3) TÔI TÌM RA NGUỒN GỐC CON SỐ 42 — LÀ ARTIFACT PHƯƠNG PHÁP, KHÔNG PHẢI ĐẶC TÍNH QUẦN THỂ. ac_app_unseen_count.json tái lập CHÍNH XÁC khi bỏ vế trích-từ-goal, chỉ dùng open_app: trên toàn 631 ep cho 38,5% / 53 app; lấy mẫu 250 ở 4 seed cho with_app 93/99/107/93 và distinct 38/37/43/38 — file repo ghi 102 và 42, nằm giữa dải. Thêm bằng chứng khoá chặt: TOÀN BỘ 42 tên app trong file đều nằm trong census open_app-only (hiệu tập rỗng). Vậy file đó đo bằng thước YẾU HƠN thước mà pre-registration đặc tả.

4) LỖI SO SÁNH CỦA CHÍNH ĐÒN. Nó áp app_of() ĐẦY ĐỦ lên test chung (ra 67%/103 — tôi tái lập đúng: 134/200, 103 distinct) nhưng lấy file open_app-only cho app_unseen (41%/42), rồi kết luận "hai quần thể khác hẳn". Cùng một thước thì app_unseen (77,3%/141) PHỦ TỐT HƠN test chung (67,0%/103). Luận cứ "miền hẹp toàn báo chí + nghệ thuật + pha trăng" chỉ là ảo ảnh do open_app-only bỏ sót phần lớn ep.


---

### C12. ~~Tiền đề sập đổ 'teacher bịa ~0-2%' (K2) — mắt xích làm cả luận văn đổi khung — chỉ dựa trên MỘT app duy nhất~~

- **Đòn gốc (trục Đủ ngưỡng luận văn thạc sĩ? + logic đổi hướng + khả thi (giá):** K2 là bằng chứng giết trục Faithful Distillation (Tier 1 null tầm thường → hạ lọc-bịa xuống phụ → đổi sang phương án LAI). Nhưng toàn bộ 80 file cache teacher mà k2_hallucination_types.py đọc đều là 'app1_s*' — một app time-tracking duy nhất, 1 model (gpt-4o-mini), 1 kiểu câu hỏi tự sinh. Kết luận 'gpt-4o-mini bịa RẤT ÍT ~0-2%' được nâng lên thành phát hiện tổng quát và làm trục quyết định trong report/78/81/85. Con số '~¼ bịa' cũ (cũng từ nền hẹp tương tự) và '~0 bịa' mới đều chưa đủ nền để in. VIỆC1 (127 câu fallback) cũng chạy trên cùng cache 1-app này. Lưu ý công bằng: CHIỀU điều chỉnh là thận trọng (demote đóng góp thay vì thổi phồng) nên không phá validity của thiết kế mới — nhưng nếu 

- **Vì sao bị bác:** Sự kiện nền (80/80 file cache đều là app1 = một app Xero Projects) ĐÚNG và tôi xác nhận độc lập. Nhưng ba mệnh đề chịu lực của đòn đều sai:

(1) "Không hề khai giới hạn" — sai tại nguồn. report/74 có hẳn mục "Giới hạn của K2 (khai thẳng)" nêu mẫu hẹp/một teacher/một-hai miền app + "miền khác có thể bịa nhiều hơn", và đặt việc-kế #3 = "đo lại bịa thật trên mẫu rộng hơn". Đòn chỉ đúng với dòng tóm tắt CLAUDE.md, không đúng với artifact khoa học.

(2) "Nâng thành phát hiện tổng quát, làm trục quyết định trong 78/81/85" — bị chính các file đó phản bác. report/78:178 ghi rõ "K2 chỉ trên 1 miền app... có thể không tổng quát sang app game/thiết-lập-hệ-thống"; 78:206 liệt kê nó vào "bằng chứng mỏng đã khai"; 81:165 khoanh "giết trục lọc-bịa Ở TẦNG THỰC NGHIỆM"; 85:58 hedge "nhiều khả năng null". Đây là ngôn ngữ có phạm vi, không phải claim tổng quát.

(3) "Mắt xích làm cả luận văn đổi khung" — sai nhân quả. report/52 (9/7, TRƯỚC K2 9 ngày) đã hạ ablation lọc xuống "điều-kiện-cần, không phải trụ"; report/82 giết tính-mới lọc bằng prior art (STaR/CapFilt/KnowAda/VGA) — lập luận độc lập hoàn toàn với n_app. K2 chỉ đẩy thêm một bậc thứ đã bị hạ.

Thêm: kết luận K2 thực sự chịu lực (matcher kết-oan nút thật → sửa trọng tài trước build) được chống lưng bởi K1 (stress-test cơ chế) và OCR/report/75 chạy trên ĐỦ 127 màn/30 app (VH phủ nhãn 62-74%) — không phải nền 1 app. Thiết kế còn tự sửa: Tier 1 vẫn chạy và báo dù null trên pool đầy đủ, nên kịch bản phản-thực của đòn (30 app ra 10-15%) chỉ làm Tier 1 dương, tức luận văn được thêm kết quả, không sập. Đòn đánh VIỆC1 hỏng hẳn: fallback là template tất định nên phát hiện "circular, không chỉ ở đâu" bất biến theo app.

Dư lượng hợp lệ: report/74 mô tả nền là "một-hai miền app" trong khi thực tế là 1 app, và tóm tắt CLAUDE.md in "~0-2%" kh

---


## D. Phán quyết từng trục (lời của chính giám khảo trục đó)

### THƯỚC ĐO + TÍNH HỢP LỆ CỦA PHÉP ĐO (metric_v1_validate.py, metric_v1_results.json, mde_pilot.py, report/84, report/85)

*Đã chạy lại code:* Chạy lại toàn bộ trên venv ~/.venvs/thesis + ollama bge-m3 local (không gọi API OpenAI). (1) Chạy lại nguyên văn harness/metric_v1_validate.py → tái lập đúng metric_v1_results.json, và thu được output console mà report/84 không phản ánh: "action_error Δ=+0.149 ⚠ KHÔNG tụt đủ", "missing Δ=+0.150 ⚠ KHÔNG tụt đủ". (2) probe1 — bóc tách bộ bơm-lỗi: paraphrase cho Jaccard = 1.0 CHÍNH XÁC ở 994/1027 bước (96.8%), 33 bước còn lại rỗng-cả-hai; target_error cho Jaccard = 0 CHÍNH XÁC ở 168/185 (90.8%), 17 ca còn lại ≤0.20; 33/1027 (3.2%) bước gold có target rỗng sau chuẩn-hoá. (3) probe2 — null-model: dùng hướng dẫn của episode KHÁC làm output cho coverage TB = 0.040 (27/185 ep >0); ba câu chung chung cho 0.052; target_score('','') = 1.0000; step_match('Tap Next','Tap Back') = True score 1.000; step_match('Click on the + icon','Click on the right arrow') = True score 1.000. (4) probe3 — 10 ca hiểm

Trục thước đo KHÔNG đứng vững ở dạng hiện tại, và điểm gãy nằm đúng ở chỗ tài liệu tự tin nhất. "AUC = 1.000" không phải kết quả đo mà là hằng đẳng thức: bộ bơm-lỗi dựng ca paraphrase bằng cách lắp lại chính token của thước (Jaccard = 1.0 chính xác ở 994/1027 bước) và ép ca sai-target giao rỗng (Jaccard = 0 chính xác ở 168/185), nên cổng "rớt AUC<0.80 thì dừng" về mặt toán học không thể kích hoạt. Đáng lo hơn là chuỗi lan truyền: report/84 §Hoài nghi CÓ tự khai "Jaccard=1 tất yếu" và "perturbation do chính tôi dựng nên có phần circular", nhưng phán quyết đầu file vẫn là "đã kiểm bằng số, không assume" và chính câu đó đi thẳng vào CLAUDE.md rồi vào pre-registration như cổng đã qua — lời tự khai bị chôn dưới tiêu đề khẳng định. Ngoài ra tôi chạy lại script và chính nó in "⚠ KHÔNG tụt đủ" cho action_error và missing, hai dòng mà report/84 đánh ✓; phần "stress-test ca khó" chống đỡ nghi ngờ "vòng 1 quá dễ" thì không có code lẫn kết quả lưu trong repo. Về bản thân bộ đối chiếu: nó sai 9/10 ca hiểm tôi tự dựng, sai cả hai chiều — nhận "Turn off" là khớp với "Turn on" (0.667), nhận "30 minutes" khớp "10 minutes", nhưng bác "Tap Log in" vs "Tap the Sign in button" (0.000) — tức vẫn đúng căn bệnh K1 chứ chưa chữa được. Công bằng mà nói, có hai điểm thật sự tốt và tôi đã kiểm: thước KHÔNG bị đánh lừa tầm thường (dùng hướng dẫn của episode khác làm output chỉ được coverage 0.040; ba câu chung chung được 0.052), và ngưỡng 0.85 được đặt tiên nghiệm chứ không dò theo kết quả. Nhưng đòn nặng nhất là construct validity: đo trực tiếp cho thấy bản chép cộc lốc được 1.000 còn bản chỉ rõ hình dạng và vị trí nút — đúng thứ report/76 nói model đang thiếu — chỉ được 0.333 và bị chấm SAI. Cộng với việc thước mù hoàn toàn trước bước thừa và trước thứ tự sai (đo được Δ=0.000 cả hai, mà F1 và order-τ dùng để vá thì chưa được viết dòng nào), và pilot MDE lại đo một tác vụ dễ hơn hẳn tác vụ sẽ eval, tôi cho rằng chưa đủ điều kiện bỏ tiền train. Việc phải làm trước, và làm được miễn phí: dựng lại tập validate từ nguồn độc lập với hàm chuẩn-hoá của thước, và kéo nghiên-cứu-nhỏ construct-validity lên TRƯỚC train bằng 91 output teacher đã cache sẵn.

*Các phát hiện mức vừa/nhẹ của trục này (không qua vòng bác bỏ):*

- **SD trong pilot MDE gần như toàn bộ là nhiễu lấy mẫu, không phải phương sai giữa app** — Pilot có 26 app, 91 bước → 3.5 bước/app, mỗi bước là 0/1. Trung bình 0.301, SD giữa các app 0.256. Nhưng SD nhị thức thuần tuý ở n=3.5, p=0.30 đã là 0.245. Suy ra SD giữa-app THẬT chỉ khoảng 0.074 — nghĩa là pilot chủ yếu đo sai số đo của chính nó. Phân bố điểm per-app (7 app đúng 0.0, 1 app đúng 1.0) là thứ nhiễu nhị thức ở n=3.5 dự đoán y hệt, không phải bằng chứng app khác nhau. Chiều sai ở đây `[lỗi thật phải sửa]`
- **Hằng số 3.077 trong công thức MDE là hằng số của G=12, bị dùng lại ở G=150-200, và không khớp với phương pháp suy luận đã đăng ký** — 3.077 = t_{0.025,df=11} + t_{0.20,df=11}, dẫn ra cho thiết kế MobileViews G=12 (report/56:60, report/53:351). Nó được bê nguyên sang trục ĐÚNG với G=150-200 (report/85:67, mde_pilot.py:116) trong khi giá trị đúng ở df≈150-200 là ≈2.80 — dùng 3.077 thổi MDE lên ~10%. Chiều sai an toàn nên không phải overclaim. Vấn đề còn lại: công thức lực thống kê này là công thức t-test tham số, trong khi phương  `[lỗi thật phải sửa]`

---

### THỐNG KÊ + LỰC MẪU (MDE trục ĐÚNG, wild-cluster bootstrap vs exact sign-flip, đa phép so sánh)

*Đã chạy lại code:* Chạy lại toàn bộ bằng ~/.venvs/thesis/bin/python (cài thêm scipy), KHÔNG gọi API. (1) Tái tính từ mde_pilot_results.json: G=26, mean=0.3013, sd=0.2561, sd_diff=0.3622 → khớp JSON. (2) Giải mã hằng 3.077 = t(.975,11)+t(.80,11)=3.0765 (df=11 ↔ G=12); đúng hằng cho G=150 là 2.836, G=200 là 2.828. (3) Bảng MDE tái tính: G=26→21.9pp, G=42→17.2, G=72→13.2, G=150→9.1, G=200→7.9 (hằng của họ). (4) Phân rã phương sai: Var(app means)=0.0656, thành phần nhị thức trong-app (n̄=3.5)=0.0601 → 92% là nhiễu; σ²_giữa≈0.0055, bootstrap 20k CI chạm 0. (5) Mô phỏng null 20k lần (không dị biệt app, p=0.301, n∈{2,3,4}): SD kỳ vọng 0.2729, khoảng 95% [0.2058,0.3425]; SD quan sát 0.2561 ở phân vị 32%. (6) CI 95% chi-square của SD_1arm = [0.2009, 0.3536]. (7) MDE 2 tầng với cấu trúc app_unseen chiếu lên 631 ep (G=42, 268 ep, ~1072 bước): 7.0pp (σ²_giữa=0) → 9.0pp (σ²_giữa cận trên CI). (8) ac_app_unseen_count.js

Trục thống kê KHÔNG bịa số — pilot có chạy thật, ngưỡng 15-20 pp có trước pilot (report/56 commit 2c84ce8 ngày 12/7, pilot 19/7), và thiết kế có định nghĩa trước kết cục null. Ba điểm đó thủ được. Nhưng gần như MỌI đầu vào của phép tính lực mẫu đều sai hoặc chưa đo: G=150-250 lấy nhầm từ full test set (đếm lại đúng app_unseen: 42 distinct/250 ep, Chao1 ≈ 72, và chỉ 40,8% ep gán được app — chính artifact ac_app_unseen_count.json trong repo mâu thuẫn với report/85:19); SD=0,256 không phải dao động giữa app mà là nhiễu nhị thức của việc chấm 3,5 bước/app (mô phỏng null không-dị-biệt cho SD kỳ vọng 0,273, quan sát 0,256 nằm ở phân vị 32%); hằng số 3.077 là t-sum của df=11 bị bê sang G=200, lách guard ở dg3_stats.py:89-93; SD-hiệu chỉ là √2×SD_teacher, chưa từng đo arm student, và nhãn "bảo thủ" chưa chứng minh được. Cái cứu luận văn là hai sai số lớn nhất đi ngược chiều và triệt tiêu nhau: tôi tính lại bằng công thức 2 tầng với cấu trúc app_unseen thật (G=42, ~1072 bước) ra MDE ≈ 7,0-9,0 pp, tức kết luận "đủ lực" sống — nhưng sống nhờ may, không nhờ lập luận. Nghiêm trọng nhất về mặt bảo vệ: theo ĐÚNG công thức và ĐÚNG ngưỡng mà tác giả tự đặt, ở G=42 thì MDE=17,2 pp và trục ĐÚNG RỚT cổng của chính nó; còn trục TRUNG THỰC G=12 có lực chỉ 25% ở hiệu ứng 15 pp mà ô MDE vẫn để trống. Phải đếm lại G, tính lại MDE bằng công thức 2 tầng, gộp bí danh app, điền ô MDE trục trung thực và liệt kê đích danh family Holm — tất cả đều free — TRƯỚC khi đổ tiền train.

*Các phát hiện mức vừa/nhẹ của trục này (không qua vòng bác bỏ):*

- **Hằng số 3.077 là t-sum của df=11 (G=12), bị dùng cho G=150-200; và nó lách chính cái guard trong thư viện** — Hằng số (t_{.975,df}+t_{.80,df}) phụ thuộc df=G−1, không phải hằng. Dùng hằng số của G=12 cho G=200 là sai kỹ thuật. Đáng nói hơn: thư viện thống kê của chính dự án CHẶN việc này, còn script pilot copy hằng số ra ngoài để chạy được. `[lỗi thật phải sửa]`
- **Wild-cluster bootstrap được biện minh bằng "G lớn" — mà G lớn là tiền đề sai; G hiệu dụng thực chỉ ~21** — report/85:64 chọn wild-cluster bootstrap-t Rademacher và loại exact sign-flip với lý do "G lớn ~150-250, 2^G quá lớn". Ở G thật (~42-72) và mất cân bằng cụm nặng, đây đúng là vùng mà Cameron-Gelbach-Miller cảnh báo under-coverage; Rademacher không được khuyến nghị khi số cụm hiệu dụng thấp (Webb weights). Thêm nữa với ICC≈0 và >50% cụm singleton, việc cluster theo app gần như không mua được gì mà  `[lỗi thật phải sửa]`
- **Family Holm khai 3 ô nhưng thiết kế cam kết ~8 phép kiểm; "phép-đo-phụ" là một cái túi không định nghĩa** — Đóng băng family đa-so-sánh là điều tốt, nhưng family được khai chỉ có 3 phần tử trong khi chính bản đăng-ký-trước cam kết công bố nhiều readout hơn hẳn, và một phần tử là bucket mở. Family mở = không phải family đóng băng. `[lỗi thật phải sửa]`
- **"3 kết cục" thực chất là 2, và NULL không được neo vào MDE nên sẽ không đọc được** — PASS và PASS-một-phần là cùng một biến cố thống kê (CI trên 0), khác nhau ở chữ "nhỏ" không định lượng → chừa đường diễn giải hậu-nghiệm. Còn NULL định nghĩa thuần bằng "CI chứa 0", không kèm biên tương đương, nên với MDE ~7-9 pp thì một NULL không phân biệt được "không có hiệu ứng" với "có hiệu ứng thật 6 pp". `[chưa đủ dữ kiện]`

---

### DỮ LIỆU, SPLIT, RÒ RỈ — và câu hỏi "vừa học vừa chấm cùng loại"

*Đã chạy lại code:* Chạy lại toàn bộ bằng ~/.venvs/thesis/bin/python, không gọi API. (1) Thống kê 1042 gold step trong dataset_samples/androidcontrol_test/ac_test_200ep.json: trung vị 6 từ, 48,9% ≤5 từ, 60,4% mở đầu click/tap/press/select, 749/1042 distinct, 167/842 cặp liền nhau trùng, 3 step rỗng, 243 step kết thúc bằng dấu câu, 41 step không có động từ nào trong ACTION_MAP (mặc định thành 'tap'). (2) Import harness/metric_v1_validate.py và chạy lại bộ bơm-lỗi với đúng seed 20260719: paraphrase Jaccard =1.0 ở 85,9% ca, target_error Jaccard =0.0 ở 96,2% ca (max 0.250) → AUC 1.000 là tautology. (3) Chạy target_of/content_tokens trên 4 cặp paraphrase-người-viết: J = 0.00/0.00/0.00/0.25; và trên toàn bộ gold: 33/1042 (3,2%) target rỗng, 29,7% target đúng 1 token. (4) Chạy lại app_of() của mde_pilot.py trên 200 ep: 134/200 (67%) có nhãn, 103 nhãn distinct, nhiều biến thể cùng app. (5) Tính Chao1 từ harness/ac_

Trục này đứng vững ở đúng một chỗ, và đó là chỗ tôi kỳ vọng sẽ đổ: KHÔNG có rò rỉ ở MobileViews. Tôi tự kiểm chứ không tin văn: 220 app pool train giao 30 app eval = rỗng, và chạy lại dHash chéo 498x138 ảnh cho 0 cặp gần-trùng ở ngưỡng Hamming ≤6 (khoảng cách nhỏ nhất thực tế là 13). Câu hỏi 4 của đề bài coi như đóng. Phần còn lại thì không đứng. Đòn nền tảng là thật và có bằng chứng cứng, không phải tu từ: thước chấm sau khi cắt hết từ vị trí và loại-nút chỉ còn so đúng danh từ mà annotator AC đã chọn, nên bốn hướng dẫn đều ĐÚNG cho người vẫn bị chấm 0.00; thậm chí dấu chấm cuối câu cũng được tính điểm (23,3% gold step dính dấu câu, tokenizer giữ nguyên). Student train trên gold AC sẽ ăn điểm ở đúng chỗ đó mà không cần hướng dẫn tốt hơn, và thiết kế hiện tại không có nhánh nào tách hai thứ ra — thiếu một arm teacher-nói-cùng-phương-ngữ thì con số headline vô nghĩa. Cổng cho phép tiêu tiền train cũng không phải cổng: paraphrase trong bộ bơm-lỗi được dựng từ chính hàm target_of của thước nên 85,9% ca có Jaccard đúng bằng 1.0, target_error bị ép giao rỗng nên 96,2% ca đúng bằng 0.0 — AUC=1.000 là hệ quả của cấu tạo, biết trước khi chạy; và 'vòng 2 ca khó' được trích trong report/84 không tồn tại trong code lẫn file kết quả đã commit. Về số liệu thống kê, G=150-250 lấy nhầm từ test set chung; file của chính dự án (42 app distinct/102 ep có nhãn) cho ước lượng Chao1 ≈72 app, và nhãn app lại là chuỗi regex tách một app thành nhiều cụm ('Etsy' và 'On the Etsy'), tức SE bị ước lượng thấp đúng hướng nguy hiểm — dù công bằng mà nói, phân rã phương sai cho thấy SD pilot phồng nặng nên kết luận 'đủ lực' có thể vẫn sống, chỉ là sống nhờ hai cái sai bù nhau. Cuối cùng, đọc 1042 gold step thật thì đây là nhãn thao tác ngắn (trung vị 6 từ, 60% mở đầu bằng click/tap, 20% cặp bước liền nhau trùng y hệt, có câu hỏng), không phải hướng dẫn cho người — claim tính mới phải sửa hoặc phải có eval người. Đề nghị: chưa train cho tới khi dựng lại cổng thước bằng paraphrase độc lập và thêm arm teacher khớp văn phong. Lưu ý về luật bịt mắt: CLAUDE.md được harness tự nạp vào context nên tôi không thể không thấy nó; tôi đã không mở report/88 và chỉ mở report/79/84/85/86 SAU khi đã kết luận từ code và dữ liệu thô.

*Các phát hiện mức vừa/nhẹ của trục này (không qua vòng bác bỏ):*

- **Bước icon-only tạo target RỖNG → thước không chấm được đúng nhóm mà K2/OCR đã chỉ là điểm yếu** — target_of trả chuỗi rỗng cho các bước chỉ tên nút bằng ký hiệu. Rỗng-vs-rỗng vô tình được bge cứu (nhúng ' ' vs ' ' cho cos≈1 → điểm 1.0, tức khớp 'đúng' mà không kiểm gì); rỗng-vs-có-chữ thì luôn trượt. Đây trùng đúng nhóm icon 20/40 ca mà K2 đã xác định là chỗ chết. `[lỗi thật phải sửa]`
- **Con số neo cho G không tái lập được (không có script sinh ra file)** — harness/ac_app_unseen_count.json là artifact quan trọng nhất cho G và cho tỉ lệ gán nhãn, nhưng không có code nào trong repo sinh ra nó, nên không kiểm được cách sample 250 ep, dùng regex nào, có lọc gì. `[lỗi thật phải sửa]`
- **Kết luận 'khung toạ độ KHỚP SẠCH' phần lớn được test ở tỉ lệ 1.0** — pilot mặc định screenshot_width/height = 1080/2400 khi thiếu trường, mà 91/100 ảnh đúng bằng 1080x2400 → hệ số scale = 1, tức phép kiểm gần như không kiểm gì cho ảnh khác kích thước. Đây là suy đoán, chưa đủ dữ kiện kết luận sai. `[chưa đủ dữ kiện]`

---

### Bốn phép thử K1 / K2 / OCR / VIỆC1 — có bị khái quát quá không

*Đã chạy lại code:* 1) `ls harness/dg1_cache/runs | sed 's/_s[0-9]*.*//' | sort | uniq -c` → **80/80 file đều tiền tố `app1`** (một app duy nhất). 2) Đếm lại k2_results.json: 40 dòng non-verbatim → **18 chuỗi element khác nhau**, `'+'`×15, `'Project name'`×4, `'✓'`×3; 13/40 dòng là trùng lặp y hệt cặp (element, sim). 3) Dựng lại `build_pairs()` của K1 (không cần ollama): 130 cặp đến từ **30 màn / 7 app**, không phải 127 màn; lớp paraphrase 40 cặp từ 17 màn với `'Everything'`×11 (27,5%), lớp nearsyn 40 cặp từ 17 màn với `'None'`×11 (27,5%). 4) Tính AUC thật (ollama, nomic + bge-m3): **nomic AUC(paraphrase>nearsyn)=0,525** (đúng như K1 kết luận), **bge-m3 AUC=0,677** (KHÔNG khớp kết luận "không tách được"); bỏ 2 chuỗi thống trị: nomic 0,366 / bge 0,611. 5) Dựng lại so-chuỗi token-Jaccard trên đúng tập K1: bỏ-lọt nearsyn 7,5% / kết-oan paraphrase 87,5% (report/73 ghi 5% / 97,5% — cùng chiều, lệch số, không có 

Trục này đứng ở mức yếu, và điểm yếu nằm đúng chỗ chịu tải nặng nhất. Bốn phép thử được viết như bốn kết quả đo, nhưng thực chất chỉ K1 có tập thử được dựng có hệ thống và có file số tái lập được — và tôi xác nhận kết luận cốt lõi của nó về nomic đứng vững (AUC 0,525, vẫn 0,366 sau khi bỏ hai chuỗi thống trị), dù phần suy rộng sang bge-m3 và OpenAI thì sai. K2 là chỗ sập: nó là phép thử duy nhất lật ngược tiền đề gốc của luận văn, nó không có code phân loại, không xem ảnh, một người AI tự chấm, và toàn bộ 80 màn đến từ MỘT app với 40 ca soi tay quy về 18 chuỗi element mà riêng dấu '+' chiếm 15. Một kết luận có sức công phá như "teacher bịa ~0-2%, không phải ¼" không thể đứng trên nền đó. OCR khá hơn về code nhưng con số được chính tài liệu chỉ định làm headline (+6 điểm) lại là con số duy nhất không có code, tỉ lệ rác bị khai thấp khoảng gấp đôi so với ước lượng độc lập của tôi (28% so với 63%), và bảng đếm glyph icon bị thổi ~7 lần do đếm substring — với hệ quả thiết kế thật là mũi tên và dấu tích thực tế OCR đọc được ZERO lần. VIỆC1 không có tạo tác nào cả. Về khái quát hoá: các report gốc khai giới hạn khá trung thực (report/73:50-52, report/74:49-51, report/76:39-40 đều tự nhận mẫu hẹp, một người chấm, không xem ảnh) — công bằng mà nói tác giả không giấu; vấn đề là lớp tóm tắt phía trên đã bóc sạch caveat và trình những thứ này như số đo đã kiểm, rồi dùng chúng để biện minh cho quyết định trên một miền dữ liệu khác (AndroidControl, người thật) mà trục mới thậm chí không dùng nhãn VH. Việc bắt buộc trước khi bỏ tiền train: chạy lại K2 trên ≥15 app với rubric viết trước và mở ảnh ra xem — đây là việc free, dữ liệu đã có sẵn trên đĩa, và nó quyết định khung đóng góp của cả luận văn.

*Các phát hiện mức vừa/nhẹ của trục này (không qua vòng bác bỏ):*

- **report/75 tự mâu thuẫn về icon trong cùng một file, và CLAUDE.md lan truyền nửa sai** — Dòng phán quyết của report/75 viết OCR "hoàn toàn không cứu được icon thuần ('+' '✓' mũi tên)". Bốn mươi dòng sau, §Cập nhật viết "OCR ĐỌC ĐƯỢC nhiều icon glyph — '+' (23 lần), 'X/x/×' (97), '<'/'>' (46)". Hai câu không thể cùng đúng. CLAUDE.md chỉ chép câu đầu. Theo số đếm lại của tôi thì câu đầu gần đúng hơn cho ✓ và mũi tên (đúng bằng 0), còn '+' thì OCR có đọc được 11 lần — nên cả hai câu đều  `[lỗi thật phải sửa]`
- **Con số OCR mà chính report gọi là "đáng tin nhất" (+6 điểm, 74→80%) không có code và không có trong file kết quả** — report/75 đưa ra ba mức: micro +11,2, macro +16,2, và "chỉ nút cỡ-nút (area < 5% màn) 74,0→80,0 = +6,0" rồi tuyên bố con số +6 là trung thực nhất; bảng 3-tầng tiếp theo (74,0 / 79,2 / 79,5) cũng vậy. Nhưng ocr_vh_coverage.py chỉ sinh ra micro và macro; không file .py nào trong harness có bộ lọc kích thước; ocr_coverage_results.json không có trường nào lọc theo diện tích. Nghĩa là con số được chỉ đ `[lỗi thật phải sửa]`
- **Bộ đếm sanity của OCR trộn đơn vị: đếm phần tử nhưng in ra là "hộp"** — Biến sane_ocr_in_any được tăng bên trong vòng lặp phần tử (mỗi phần tử actionable có hit thì +1), còn sane_ocr_total được tăng trong vòng lặp hộp OCR. Rồi câu print ghép hai cái thành một phân số và gán nhãn "%d/%d hộp OCR rơi TRONG một nút actionable". Tử số là phần tử, mẫu số là hộp — phân số 1085/2053 vô nghĩa. report/75 chép nguyên con số này làm bằng chứng khung toạ độ khớp. Bằng chứng khung  `[lỗi thật phải sửa]`
- **VIỆC1 hoàn toàn không có tạo tác — bảng số trong report/76 không có code, không có file kết quả, không có rubric viết trước** — report/76 đưa bảng bốn dòng (100% có ý-định, 20% lặp động từ, 60% bắt đầu bằng động-từ-hành-động, ~80% lặp lại mục tiêu) trên 127 câu fallback. Không có script chấm trong harness/, không có viec1_results.json, không có danh sách 127 câu được lưu lại, và không có tiêu chí viết trước cho "lặp lại mục tiêu". Hai con số 20% và 60% trông như đếm được bằng regex nhưng không có code; con số ~80% — cái đư `[điểm yếu đã tự khai]`
- **Hàm verbatim của K2 dùng Jaccard ≥ 0,7 nên "verbatim 68,5%" không phải verbatim** — Một bước được xếp là "khớp y-chữ nhãn VH" nếu chuỗi bằng nhau, HOẶC là substring của nhau (chỉ cần ≥3 ký tự), HOẶC trùng token Jaccard ≥ 0,7. Điều kiện substring rất lỏng: element 'Add' sẽ khớp verbatim với nhãn 'Add a new expense category'. Nên con số 68,5% verbatim là cận trên của "tham chiếu nút thật", và tương ứng 31,5% non-verbatim là cận dưới của tập ứng viên bịa. Ảnh hưởng vừa phải nhưng nó `[lỗi thật phải sửa]`

---

### TRUNG THỰC BÁO CÁO — đối chiếu prose (report/73-86, 88, CLAUDE.md §0) với code + số thô trong harness/

*Đã chạy lại code:* Đã chạy lại (đều local/free, KHÔNG gọi API OpenAI): (1) `~/.venvs/thesis/bin/python harness/metric_v1_validate.py` với ollama bge-m3 — tái hiện đúng AUC=1.000, fp_paraphrase=0.000, và thu được thêm output mà prose không nhắc: script tự in cờ "⚠ KHÔNG tụt đủ" cho action_error (Δ=0.149) và missing (Δ=0.150), tức 2/3 phép kiểm độ nhạy trượt ngưỡng do chính tác giả đặt ở dòng 174. (2) Probe tính tautology: dựng lại nhánh paraphrase của perturb() trên 400 gold step_instructions → target_of(paraphrase) trùng byte-for-byte target_of(gold) 400/400 = 100%, chứng minh Jaccard=1.0 là tất yếu chứ không phải kết quả đo. (3) Probe ca khó (thứ report/84 "vòng 2" tuyên bố nhưng không có code): 8 cặp gần-nghĩa khác-entity qua target_score → 0.000-0.333, tất cả đều bị bắt đúng, trung bình khớp con số 0.350 mà report nêu → phần THỰC CHẤT của vòng 2 được tôi xác nhận độc lập, chỉ thiếu tái lập. Đồng thời xá

Trục này đứng vững và cho kết quả thật: prose CÓ nói mạnh hơn số ở đúng hai chỗ gánh nhiều trọng lượng nhất, và cả hai đều nằm ngay trước cửa quyết định chi tiền train. Thứ nhất, cổng validate thước "AUC=1.000, false-positive paraphrase=0.000" là hằng đẳng thức của cách dựng bơm-lỗi chứ không phải phép đo — nhánh paraphrase gọi chính hàm đang được kiểm rồi dán lại nguyên văn output (tôi xác nhận 400/400 ca trùng khít), nhánh target_error thì bị ép 0 token chung; đo lại bằng paraphrase thật tôi thấy kết oan 5/8 = 62%, và vì Student train trên gold còn Teacher zero-shot thì không, thước này thưởng cho bắt-chước-văn-phong, tức confound thẳng vào trụ đóng góp MODEL. Thứ hai, lập luận "đủ lực thống kê, MDE 8-9pp" đứng trên G=150-250, con số suy từ tập test CHUNG, trong khi chính repo có phép đo trực tiếp split app_unseen cho 42 app/250 ep — MDE thật rơi vào 12-17pp, chạm hoặc vượt ngưỡng nguy hiểm 15-20pp mà chính pre-registration tự đặt; phép đo đó lại đã nằm trong repo 30 phút trước khi report/85 được chốt. Kiểu lỗi "caveat rụng dần" mà tôi được yêu cầu săn thì có thật và truy được từng nấc: report/84 tự khai "perturbation của chính tôi, có phần circular" → report/85 ghi "0.000 ✓ ĐẬU" và quy sai nguyên nhân sang backstop → report/88 và commit message chỉ còn "metric-gate PASSED". Cũng phải nói cho công bằng: tầng báo cáo NGUỒN nhìn chung trung thực đáng khen — report/74 tự khai người chấm không hề xem ảnh và mẫu hẹp, report/79 giữ nguyên caveat 48% đích là icon suốt tới report/88, report/86 chủ động nhận MDE là ước lượng bảo thủ. Sự tô hồng không nằm ở người làm thí nghiệm mà nằm ở tầng tóm tắt: mỗi lần nội dung được nén lại thì điều kiện rụng còn kết luận thì cứng lên. Khuyến nghị: chưa được commit report/85 như hiện trạng và chưa được tiêu tiền train cho tới khi chạy lại cổng thước với nhánh paraphrase không-tự-quy-chiếu và đếm lại G trên toàn bộ 631 ep — cả hai đều free và mất chưa tới một buổi.

*Các phát hiện mức vừa/nhẹ của trục này (không qua vòng bác bỏ):*

- **"Vòng 2 — ca khó" của report/84 không có code, không có số lưu — nhưng được viện dẫn trong pre-registration** — report/84 dựng cả một mục "Vòng 2 stress-test CA KHÓ" với ba con số cụ thể (đích-sai-khó target-score TB = 0.350; AUC = 1.000; bge cứu nhầm 3/60 = 5%), và chính ba con số này là thứ biến câu "AUC=1.0" thành "AUC=1.0 CẢ CA KHÓ" — mệnh đề được chép vào report/85:50, report/88:137 và CLAUDE.md. Nhưng trong repo không tồn tại code sinh ra vòng 2: metric_v1_validate.py chỉ có 7 loại bơm lỗi và không lo `[lỗi thật phải sửa]`
- **Kết luận đảo hướng cả luận văn (K2) dựa trên gán nhãn tay của một người chấm, không nhìn ảnh, không lưu nhãn, không κ** — K2 là phát hiện có sức nặng chiến lược lớn nhất trong cả chuỗi: nó kết luận teacher gần như không bịa (~0-2%), qua đó GIẾT đóng góp "lọc bịa" và đẩy toàn bộ thiết kế sang hướng LAI. Bằng chứng nền của nó là việc phân loại tay 40 ca không-verbatim thành "35/40 là nút THẬT bị VH bỏ nhãn, 0 ca bịa gần-nghĩa". Nhưng: code chỉ IN 40 ca ra để soi, không phân loại; k2_results.json chỉ lưu 5 con số đếm và `[lỗi thật phải sửa]`
- **ac_app_unseen_count.json là hiện vật mồ côi — không script nào trong repo sinh ra nó** — File này là phép đo TRỰC TIẾP duy nhất về split app_unseen (631 ep, 42 app distinct) — tức là dữ kiện quan trọng nhất cho lập luận đủ-lực-thống-kê. Nhưng tôi grep toàn repo không tìm thấy script nào ghi ra nó, cũng không .py nào nhắc chuỗi 'distinct_apps'. Không tái lập được nghĩa là không kiểm được nó đo trên gì (250 ep nào, seed nào, hàm gán app nào — nếu dùng cùng regex lỗi ở phát hiện trên thì `[lỗi thật phải sửa]`
- **Con số K1 "kết oan 47,5% paraphrase" phần lớn do bộ thử là dịch đa ngữ — không phải chế độ lỗi của pipeline tiếng Anh** — K1 kết luận bộ đối chiếu embedding "RỚT" với hai chiều lỗi đối xứng 47,5%/47,5%. Nhưng nhìn bộ neo LEX thì phần lớn item "paraphrase" (= cùng nút, gold REAL) là bản DỊCH sang tiếng Việt/Tây Ban Nha ('Tìm kiếm' cho 'Search', 'Guardar' cho 'Save'). Tôi đếm: 32/48 = 67% item paraphrase là phi-tiếng-Anh. Pipeline FAIR chạy hoàn toàn tiếng Anh (màn MobileViews English, teacher gpt-4o-mini xuất tiếng An `[chưa đủ dữ kiện]`
- **Vài chỗ code chết / rút thăm thừa trong script đang giữ vai trò cổng** — Script cổng nên sạch vì nó là hiện vật đăng-ký-trước. Hiện có: dòng 98 tính g[i] rồi bị dòng 99 ghi đè vô điều kiện (code chết); dòng 161 rút một số ngẫu nhiên `i = rng.randrange(len(gold))` rồi không dùng tới (chỉ tiêu tốn trạng thái RNG, làm việc tái lập theo seed khó lý giải hơn cần thiết). Không làm sai kết quả nhưng là dấu hiệu script chưa được rà trước khi lấy số làm cam kết. `[lỗi thật phải sửa]`

---

### TÍNH MỚI + CHỐNG SCOOP

*Đã chạy lại code:* Không chạy lại thí nghiệm số (trục này là scoop-check, không có số để tái lập). Đã tự kiểm dữ liệu nền: python inspect dataset_samples/androidcontrol_test/ac_test_200ep.json → 200 episode, mỗi episode có keys [episode_id, goal, step_instructions, actions], step_instructions đúng là câu người-viết từng bước ('Go back to the previous page to see category', 'Click on filter option'); grep xác nhận harness dùng nó làm gold so sánh (metric_v1_validate.py:141-156, mde_pilot.py:64) — tức mô tả 'step_instruction làm target sinh' khớp code thật. Grep report/82 + report/57 xác nhận 0 hit cho GuideMe/CoAT/GUI-Narrator/OS-Genesis/Synapse.

Trục tính-mới đứng được NHƯNG đúng như report/81 tự khai: MỎNG, và mỏng hơn hồ sơ đang nghĩ. Claim 2 (AC step_instruction làm target sinh) sống sót qua nhiều đợt search trực diện của tôi — chưa tìm được ai làm — nhưng chỉ đáng giá khi đi kèm phân định với dòng action-description generation (CoAT/GUI-Narrator/OS-Genesis) hiện đang vắng hoàn toàn trong related work. Claim 1 (VH-check vs self-probe) là phân định cơ chế hợp lệ nhưng cỡ 'ứng dụng chuẩn hoá', không phải phát kiến, và report/57 thực ra đã tự thu hẹp gần đúng. Đòn nặng nhất: GuideMe (CHI 2026) đã công bố đúng tác vụ 'screenshot + câu hỏi → hướng dẫn từng bước cho người' dưới dạng hệ thống prompt-VLM — câu 'model đầu tiên sinh hướng dẫn nhiều bước cho người' như đang chốt trong nhật ký quyết định 19/7 sẽ bị bác nếu giữ nguyên chữ; phải dịch thành 'model nhỏ mở đầu tiên được TRAIN cho tác vụ này + khung đánh giá kép định lượng đầu tiên'. Đây là lỗi framing sửa được bằng chữ và citation, không phải lỗi thiết kế thí nghiệm — nhưng phải sửa TRƯỚC khi viết bài và trước khi mang đi gặp thầy, vì nó nằm đúng ở câu bán hàng số một. Nguồn chính: dl.acm.org/doi/10.1145/3772318.3791448 (GuideMe), arxiv.org/abs/2403.02713 (CoAT), arxiv.org/abs/2406.13719 (GUI-Narrator), arxiv.org/abs/2412.19723 (OS-Genesis), arxiv.org/abs/2606.12817 (GUITrans2Act — đã verify độc lập, phân định của report/82 đúng), arxiv.org/pdf/2604.17284 (HalluClear).

*Các phát hiện mức vừa/nhẹ của trục này (không qua vòng bác bỏ):*

- **Dòng 'sinh mô tả bước thao tác GUI' đông hơn related work đang ghi: CoAT, GUI-Narrator, OS-Genesis, UItron đều vắng mặt trong report/57** — Claim (2) 'AndroidControl step_instruction làm target sinh — chưa ai làm' SỐNG ở nghĩa hẹp (tôi search nhiều cách diễn đạt, không tìm được bài nào train/eval sinh instruction trên AC step_instructions làm output), NHƯNG năng lực 'sinh câu mô tả bước thao tác GUI bằng ngôn ngữ tự nhiên' thì hoàn toàn KHÔNG mới: CoAT/Android-in-the-Zoo (Findings EMNLP 2024) có hẳn thành phần 'Next Action Description `[lỗi thật phải sửa]`
- **Claim (1) VH-check phân định được với FaithScore nhưng mức mới thấp — và phía agent đã dùng cùng cơ chế làm mitigation** — Phân định 'nguồn ngoài có cấu trúc vs self-probe' đứng được về cơ chế (FaithScore verify bằng VQA trên chính ảnh; ta đối chiếu VH metadata). Nhưng hai chỗ làm nó mỏng trong mắt reviewer khó tính: (a) CHAIR (EMNLP 2018) đã chấm hallucination bằng annotation đối tượng NGOÀI — 'external structured source' không phải phát kiến, chỉ khác là VH đi kèm miễn phí với màn hình; (b) dòng agent đã dùng đúng t `[điểm yếu đã tự khai]`
- **Ba lỗ report/82 tự khai vẫn chưa lấp: HalluClear + TIST 2022 chưa đọc full-text, vòng quét CHI/UIST chưa chạy — và lỗ CHI/UIST đã được chứng minh là có mìn thật** — report/82:50-53 tự khai chưa đọc HalluClear (2604.17284, taxonomy + 3-stage VLM-judge cho GUI hallucination — chạm thẳng 'chương đo-lường' của luận văn), chưa verify TIST 2022, chưa quét CHI/UIST/venue tiếng Trung. Một giờ search của tôi trong đúng lỗ CHI/UIST đã ra GuideMe (phát hiện 1). Suy ra xác suất còn sót ở hai lỗ chưa quét còn lại (venue tiếng Trung, workshop HCI) không nhỏ. Điểm cộng: khẳ `[điểm yếu đã tự khai]`
- **Chưa loại trừ được scoop ở venue tiếng Trung và preprint 2606-2607 mới nhất** — Mảng GUI-VLM Trung Quốc ra bài rất nhanh (GUITrans2Act, MobileVLM, UItron, KnowAct-GUIClaw đều TQ); search tiếng Anh của tôi không phủ được venue/paper tiếng Trung, và các preprint tháng 6-7/2026 chưa được index đầy đủ. Không tìm thấy scoop không có nghĩa là không có. `[chưa đủ dữ kiện]`

---

### Đủ ngưỡng luận văn thạc sĩ? + logic đổi hướng + khả thi (giám khảo hoài nghi, tự kiểm số trước khi đọc report)

*Đã chạy lại code:* (1) Chạy lại harness/metric_v1_validate.py (ollama bge-m3): tái lập đúng AUC=1.000, detection=1.0, FP=0.0 — kèm 2 cờ '⚠ KHÔNG tụt đủ' (action_error Δ=0.149, missing Δ=0.150) không được nhắc trong report/84. (2) Probe tự viết dùng chính step_match/target_score của họ trên 10 cặp paraphrase-thật vs 10 cặp bịa-gần-nghĩa: AUC=0.350, 10/10 paraphrase thật bị kết oan (ts=0.000), 0/10 bịa bỏ lọt; đo sim bge-m3: paraphrase thật 0.49-0.79 chồng lấn bịa 0.59-0.72 → backstop 0.85 không bao giờ kích hoạt. (3) Đếm cache K2: 80/80 file = app1 (một app duy nhất). (4) Chạy lại app_of() của mde_pilot.py trên ac_test_200ep.json: 134/200 gán (67%), 103 distinct — xác nhận '~114/200' của report/85 đến từ mẫu test CHUNG, trong khi ac_app_unseen_count.json trên ĐÚNG split chỉ 41% gán, 42 distinct/250, Pinterest 14 ep. (5) Đếm chất lượng gold trên 1042 step: 17.7% trùng-nguyên-văn trong episode, 4.3% go-back, 

Trục đứng MỘT PHẦN. Về logic đổi hướng: chuỗi quay xe có kill-test đi kèm và tài liệu tự khai khá thẳng — lành mạnh hơn biện minh suông — nhưng hai mắt xích mang tải sập khi tự kiểm: (1) tiền đề K2 'teacher không bịa' rút từ đúng MỘT app (80/80 file cache = app1); (2) cổng thước 'AUC=1.000, giải được chỗ K1 chết' là tự-chứng — tôi chạy probe paraphrase-đồng-nghĩa thật thì thước rớt hoàn toàn (AUC=0.35, kết oan 10/10, backstop bge vùng chết đo được), nghĩa là headline Δ(Student−Teacher) sắp tới có nguy cơ lớn là artifact khớp-giọng-gold chứ không phải đúng-hơn — PHẢI sửa trước khi bỏ tiền train. Lực thống kê 'MDE 8-9pp' dựa trên G đếm nhầm split (số thật trên app_unseen kém đa dạng hơn hẳn), thực tế cỡ 12-14pp — sống nhưng sát ngưỡng. Phần còn lại (artifact 3B + thước-sau-vá + prereg + chương negative-results) TẠM ĐỦ chuẩn thạc sĩ constructive nếu vá thước, hạ tông 'model đầu tiên', và thầy duyệt khung — điều kiện thứ ba chưa xảy ra sau 3 lần đổi hướng. Khả thi: FAIR 15/8 gần chắc trượt (27 ngày, 0 dòng code train, data train chưa tải, bài FAIR trong kế hoạch vẫn bán đóng góp đã chết); đường lui bỏ-FAIR-giữ-VCL có thật nhưng VCL thừa hưởng lỗi thước cross-lingual chưa test — nên quyết bỏ/giữ FAIR ngay tuần này.

*Các phát hiện mức vừa/nhẹ của trục này (không qua vòng bác bỏ):*

- **Logic đổi hướng: lành mạnh về HÌNH THỨC (có kill-test trước khi quay xe) nhưng hai lần quay xe gần nhất đứng trên bằng chứng mỏng, và khung 'hai trụ ngang nhau' được giữ bằng cách hạ chuẩn kết cục** — Chuỗi prompting→bác→distillation-lọc-bịa→K2 giết tiền đề→LAI train-trên-gold: mỗi lần quay đều có phép thử đi kèm (K1/K2/OCR/pilot AC) — hình thức là điều chỉnh khoa học thật, KHÔNG phải biện minh suông, và tài liệu tự khai khá thẳng (81: 'ĐỪNG giả vờ bộ lọc còn sống', 'tính mới MỎNG, không dập bằng số'). NHƯNG hai điểm gợn: (1) các phép thử quyết định (K2, VIỆC1) chạy trên 1 app; cổng thước chạy  `[điểm yếu đã tự khai]`
- **Sau khi trừ hết phần chết, phần CÒN chắc chắn làm được — và câu trả lời 'đủ thạc sĩ không'** — Liệt kê thẳng phần còn đứng: (1) một artifact model thật: Qwen2.5-VL-3B SFT-LoRA trên AC gold, khả thi với Colab Pro, thoả yêu-cầu-cứng của thầy; (2) thước (action,target) SAU KHI VÁ + quy trình perturbation-validate + pre-registration/freeze-split có commit — về phương pháp luận là trên mặt bằng thạc sĩ trong nước; (3) chương đo-lường 4 kill-test — các negative result (embedding-đơn không tách đư `[chưa đủ dữ kiện]`

---
