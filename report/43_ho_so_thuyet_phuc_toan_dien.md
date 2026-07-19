# SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM TỪ ẢNH GIAO DIỆN VÀ ĐÁNH GIÁ KHÔNG CẦN ĐÁP ÁN MẪU
## Bản thuyết minh toàn diện — trình bày theo lối luận văn bảo vệ

> 🔴 **CẬP NHẬT 2026-07-08 — ĐỌC [CHƯƠNG 0](#chương-0--kiến-trúc-mới-mô-hình-làm-trung-tâm-2026-07-08) TRƯỚC.** Thầy yêu cầu luận văn phải **huấn luyện một MÔ HÌNH thật** (khung "prompting + đánh giá" cũ bị bác). **Chương 0** (ngay dưới, trước Chương 1) trình bày **kiến trúc MỚI đầy đủ — đọc một lần hiểu hết**: mô hình grounding huấn luyện bằng RLVR, lấy chính thước đo no-gold làm hàm reward. Các chương 1–13 bên dưới là **khung CŨ** — giữ lại vì phần *dữ liệu / thước đo / literature vẫn tái dùng nguyên*, nhưng "đóng góp = hệ prompting" đã đổi thành "đóng góp = mô hình train được". Chi tiết chọn hướng: `report/50`; bối cảnh: `CLAUDE.md §0`.

> **Đối tượng đọc:** người chưa biết gì về AI **và** hội đồng phản biện. Văn bản này được viết theo lối một
> chương luận văn: mỗi phần mở đầu bằng dẫn nhập và trực giác, kế đó là định nghĩa hình thức với ký hiệu đầy
> đủ, rồi ví dụ số minh hoạ, và cuối cùng là ghi chú về hiệu lực/giới hạn. Mọi thuật ngữ đều được định nghĩa
> bằng lời thường ở lần xuất hiện đầu; mọi công thức đều kèm diễn giải. Dữ liệu minh hoạ trích trực tiếp từ
> `dataset_samples/`. Cập nhật 2026-07-05.
>
> *Quy ước nội bộ: trong tài liệu này (không phải trên slide) đôi khi gọi tắt "một màn" = **DG1**, "nhiều
> màn" = **DG2**. Khi trình bày trước hội đồng, chỉ dùng "một màn / nhiều màn".*
>
> Đây là **bản văn xuôi mở rộng** để đọc là hiểu và để bảo vệ. Các con số, công thức và trích dẫn trong
> đây đều đồng nhất với tài liệu gốc chuẩn: `report/05` (kế hoạch), `report/36` (thuyết minh một màn),
> `report/44` (chương dữ liệu đã verify tận file), `report/40` (phán quyết phản biện), `report/42` (độ mới
> 2026). Khi mâu thuẫn, các file đó thắng.
>
> **TÀI LIỆU TỰ ĐỦ — chỉ cần đọc đúng file này.** Đã gom mọi thứ cần biết: bài toán · dữ liệu (ảnh thật, Ch.3) ·
> pipeline (Ch.4) · metric (Ch.5) · tính hợp lệ (Ch.7) · kết quả sơ bộ (Ch.8) · định vị 2026 (Ch.9) ·
> lộ trình + môi trường + trạng thái (Ch.11) · tổng hợp phòng thủ (Ch.12) · thiết kế thí nghiệm (Ch.13).
> Pipeline (Ch.4) và metric (Ch.5) là **bản chốt cuối**, đã qua nhiều vòng kiểm định 2024–2026.
> *(Phán quyết & trạng thái mới nhất → xem hộp ngay bên dưới.)*

---

## TRẠNG THÁI MỚI NHẤT (2026-07-06) — ĐỌC CÁI NÀY LÀ NẮM TOÀN CẢNH

**Một câu:** *Thiết kế (pipeline + metric + bộ thí nghiệm + mẫu dữ liệu) đã đạt chuẩn thạc sĩ trường top và không còn lỗ hổng bất ngờ; việc DUY NHẤT còn lại để "bảo vệ được" là **CHẠY thí nghiệm ra ≥1 con số dương CI sạch** — hiện mới có kết quả sơ bộ.*

**① Đã CHỐT (đóng băng, không đổi nữa):**
- **Đề tài + 2 đóng góp** (A hệ sinh bám màn · B đánh giá no gold), đặt ngang vai **có điều kiện** (chờ số nhiều màn dương).
- **Pipeline** (Ch.4) và **metric** (Ch.5) — bản cuối, qua nhiều vòng phản biện.
- **Bộ thí nghiệm** (Ch.13) — tái khung còn **~7 thí nghiệm cốt lõi** (đừng đọc "15" là 15 việc) + E16 hữu ích + arm "nạp VH lúc sinh".
- **Mẫu dữ liệu 3 bộ ĐÃ CÓ TRONG TAY** (Ch.3 + `report/48_dataset_selection.md`):
  - MobileViews (một màn): **127 màn / 30 app** (`kept_screens_final.json`).
  - ScreenSpot (đối chứng grounding): **501 item** (290 text / 211 icon).
  - AndroidControl (nhiều màn): **286 ep N∈{4,5,6}** + **48 ep N∈{7–10}** (`dg2_episodes.json` + `_Nlong.json`), **237 app**, nguồn `smolagents/android-control`.

**② Đã KIỂM ĐỊNH (các vòng debate — chi tiết Ch.12):**
- Bộ thí nghiệm · pipeline · metric · **mẫu dữ liệu** đều qua debate đối kháng nhiều giám khảo → **HỢP LÝ CÓ ĐIỀU KIỆN**, KHÔNG lỗi thiết kế, KHÔNG phải chọn lại.
- **Estimand khai rõ:** con số là **trung bình đều trên app (macro)**, KHÔNG phải "đại diện app nói chung" → claim bảo thủ, khó bị bác "mẫu không đại diện".

**③ CÒN LẠI (việc thật, xếp ưu tiên):**
- **Free trước:** git-freeze 3 manifest làm pre-registration · MIN_ACT-sensitivity (chống thiên lệch màn dày nhãn) · độ phủ nhãn VH (M4) · perturbation harness · matcher κ.
- **Tốn API (hỏi trước):** sinh BASE 127 màn × ≥2 model → mục tiêu **faithfulness-gain CI không chạm 0** · cổng K-pair · Step-SR.
- **Mắt xích yếu nhất (đồng thuận mọi giám khảo):** cả hai đóng góp đang chờ **số chưa chạy** → ưu tiên chạy để có bằng chứng, đừng bảo vệ với "lời hứa".

**④ Điểm sáng (đủ để đậu khi có số):** chống tự chấm **vượt** G-Eval/FActScore/RAGAS · luật vàng chống leak · khai giới hạn trung thực · đối chứng thất bại đo được · citation verify tận venue.

---

## TÓM TẮT

Luận văn nghiên cứu bài toán **sinh hướng dẫn sử dụng phần mềm theo từng bước cho người đọc**, nhận đầu vào là một hoặc nhiều **ảnh chụp màn hình giao diện** kèm một **câu hỏi bằng ngôn ngữ tự nhiên**, và sinh ra một chuỗi bước thao tác bám sát ngữ cảnh ảnh. Công cụ nền là **mô hình ngôn ngữ thị giác (VLM)** — hệ thống AI nhận ảnh và văn bản, trả về văn bản.

Bài toán này vấp phải hai khó khăn không thể né. **Thứ nhất**, VLM có xu hướng **ảo giác**: nó viết ra những bước nghe rất hợp lý nhưng tham chiếu tới nút/thành phần **không hề tồn tại** trên màn hình đang xét — một dạng lỗi vừa phổ biến vừa nguy hiểm, vì người dùng làm theo sẽ bấm nhầm hoặc bối rối. **Thứ hai**, và sâu hơn về mặt khoa học, là **không tồn tại một tập hướng dẫn chuẩn do con người biên soạn** cho mọi ứng dụng để làm mốc so sánh (không có "đáp án mẫu", tiếng Anh là *no gold reference*). Thiếu đáp án mẫu thì cách đánh giá kinh điển — so đầu ra của máy với đáp án do người soạn viết — sụp đổ. Đó là nút thắt trung tâm mà luận văn phải gỡ.

Luận văn đề xuất **hai đóng góp đặt ngang vai (có điều kiện)**:

- **(A) Một hệ thống sinh hướng dẫn bám sát màn.** Cốt lõi là **bước đối chiếu với giao diện thật**: sau khi VLM sinh bản nháp một cách "mù" (chỉ nhìn ảnh, không được cho danh sách nút), một thuật toán đối chiếu từng tên nút mà máy nhắc tới với **cây phân cấp giao diện** thật của màn; bước nào tham chiếu nút không có thật thì **viết lại thành mô tả bằng lời**, tuyệt đối không đoán sang nút khác. Với nhiều ảnh, một **bước sắp lại thứ tự các màn** đứng trước sẽ khôi phục trình tự trước khi sinh.
- **(B) Một phương pháp đánh giá không cần đáp án mẫu và không tự chấm.** Thay vì so với đáp án do người soạn viết, ta neo vào **cây phân cấp giao diện** (cho nhánh một màn) và **quỹ đạo thao tác vàng** (cho nhánh nhiều màn), đồng thời dùng nhiều cơ chế chấm độc lập để tránh bẫy "vừa ra đề vừa chấm". Phương pháp được **kiểm định bằng nhiễu loạn có kiểm soát** (cố ý bơm lỗi đã biết để xem thước đo có phản ứng đúng không).

Toàn bộ xương sống phương pháp đều tựa trên nguồn **đã bình duyệt**. Đóng góp (A) không bị hạ xuống "chỉ kỹ thuật" vì nó dựa trên một **phát hiện thực nghiệm đo được** — phương án "đoán nút gần nhất" gây ra **lỗi âm thầm** — và vì nó báo cáo trung thực **tỉ lệ ảo giác của bản gốc** cùng **giá phải trả** (tỉ lệ bước bị hạ thành mô tả), chứ không khoe con số hoàn hảo hậu xử lý.

---

## MỤC LỤC
- **Chương 1** — Giới thiệu: bối cảnh, phát biểu bài toán hình thức, ba thách thức, đóng góp
- **Chương 2** — Kiến thức nền & thuật ngữ (giải thích tận gốc cho người mới)
- **Chương 3** — Dữ liệu: ba bộ, vai cố định, ví dụ thật + cấu trúc
- **Chương 4** — Phương pháp I: hệ thống sinh (pipeline một hệ, hai nhánh)
- **Chương 5** — Phương pháp II: đánh giá (thước đo hai nhánh)
- **Chương 6** — Ví dụ chạy đầu–cuối, có số
- **Chương 7** — Tính hợp lệ & thiết kế thực nghiệm
- **Chương 8** — Kết quả sơ bộ (trung thực)
- **Chương 9** — Định vị & công trình liên quan (rà soát 2025–2026)
- **Chương 10** — Đóng góp, giới hạn, hướng phát triển
- **Chương 11** — Bối cảnh thực hiện: lộ trình hai bài báo, môi trường, trạng thái & việc tiếp theo
- **Chương 12** — Tính đúng thời & tổng hợp phòng thủ (đã kiểm định gì, các vòng research 2026)
- **Chương 13** — Thiết kế thí nghiệm (7 RQ · **~7 thí nghiệm cốt lõi** [đánh số E1–E16] · cỡ mẫu · cổng · thứ tự chạy · bảng/hình)
- **Phụ lục A** — Bảng thuật ngữ đầy đủ · **B** — Hỏi–đáp giám khảo · **C** — Danh mục nguồn bình duyệt

---

# CHƯƠNG 0 — KIẾN TRÚC CHỐT: FAITHFUL DISTILLATION [2026-07-09, VÁ 2026-07-09 SAU DEBATE VÒNG 4]

> **Đọc hết chương này là nắm trọn hướng chốt.** Đây là kết quả sau **3 vòng debate giám khảo** (loại grounding-RLVR, generator-RLVR, classifier — `report/50` §7–§9) + **2 deep-research** (verify 39 claim bình-duyệt sống) + **1 vòng debate riêng kiểm tra tính-mới** (`report/52`, 2026-07-09). Ràng buộc đã chốt: **model tự train = đóng góp CHÍNH; đánh giá no-gold = chương PHỤ; <3 tháng; solo; Colab; đề tài cố định.** *(Phương án grounding cũ đã bị bác — dời xuống Phụ lục 0-CŨ cuối chương.)*
>
> **⚠️ VÁ SAU DEBATE TÍNH-MỚI (`report/52`): pipeline SỐNG nhưng tính mới hẹp hơn bản dưới đây mô tả.** KHÔNG được nói "quy trình lọc-faithfulness MỚI" — công thức generate→filter→retrain đã có ở STaR (Zelikman 2022), và cơ chế gần-song-ánh đã có ở KnowAda (NAACL25)/BLIP-CapFilt (ICML22)/VGA (Findings EMNLP24). Tính mới sống sót chỉ còn ở **2 điểm cụ thể**: (a) bộ lọc đối chiếu NGUỒN NGOÀI có cấu trúc (View Hierarchy, không tự-probe như KnowAda) cho một hành vi RỦI RO CAO (bịa tên nút → thao tác sai, không phải chi tiết caption vô hại); (b) đo **faithfulness khi TẮT hậu-kiểm/VH lúc suy luận** — đây phải là **TRỤ THỰC NGHIỆM SỐ MỘT** (không phải mục phụ), vì đây là câu hỏi có thể ra kết quả NULL thật. Ablation raw-vs-filtered vẫn làm nhưng chỉ là điều-kiện-cần/robustness-check, KHÔNG phải trụ đóng góp. Chi tiết đầy đủ (bảng precedent, câu tuyên bố tính-mới dùng khi trình thầy, citation bắt buộc bổ sung: STaR, FaithDial/BEGIN, WinDOM, Trust-the-Right-Teacher, LiteGUI, CORA): `report/52`.

## 0.1. Mục tiêu (một câu)

Xây dựng một **MÔ HÌNH SINH hướng dẫn GUI chạy on-device** — fine-tune (SFT-LoRA) một VLM nhỏ (**Qwen2.5-VL-3B**) bằng **chưng cất có LỌC TRUNG THỰC (faithful distillation)**: một mô hình lớn (teacher) sinh hướng dẫn, **lớp trung-thực-hoá LỌC bỏ/viết-lại bước bịa**, rồi **student học trên dữ liệu ĐÃ SẠCH** → student bám màn hơn, ít bịa hơn, chạy được trên máy không cần API. **Đóng góp chính = model, chứng minh bằng việc hành-vi-né-bịa sống sót khi KHÔNG còn View Hierarchy lúc suy luận; quy trình lọc là phương-tiện THÍCH-NGHI từ recipe đã biết (STaR/KnowAda/CapFilt), không phải phát minh; đánh giá no-gold = phụ.**

## 0.2. Sơ đồ tổng thể (một hình)

```
── PHA HUẤN LUYỆN (offline, một lần) ─────────────────────────────
 Ảnh + câu hỏi ─▶ TEACHER (gpt-4o-mini) ─▶ hướng dẫn nháp (bịa ~¼)
                                              │
                                              ▼
                    ★ LỚP LỌC FAITHFULNESS (đối chiếu View Hierarchy)
                      bước matched → giữ · bước bịa → viết lại/loại
                                              │
                                              ▼
                         TẬP SFT SẠCH  ─▶  SFT-LoRA Qwen2.5-VL-3B
                                              │
                                              ▼
                                   ★★ MODEL STUDENT (đóng góp)

── PHA SUY LUẬN (deploy, on-device) ──────────────────────────────
 Ảnh + câu hỏi ─▶ ★★ STUDENT sinh ─▶ (tuỳ chọn) hậu-kiểm ─▶ hướng dẫn
                  (chạy trên máy, KHÔNG cần teacher/API)
```

**Hai thứ ★ là đóng góp:** (★) quy trình LỌC tạo data sạch, (★★) MODEL student on-device. Teacher chỉ là công cụ sinh data (bỏ đi lúc deploy).

## 0.3. "Faithful distillation" là gì — và vì sao KHÔNG phải "distill trần"

- **Distillation thường:** student học *nguyên* output teacher → thừa kế luôn ~¼ bước bịa của teacher. Đây là recipe đã biết (Alpaca/Orca) → **novelty 0**.
- **FAITHFUL distillation (của ta):** student CHỈ học output teacher **đã qua lớp lọc** (bỏ/viết-lại bước bịa). → student học "**thói quen trung thực**" của pipeline, không kế thừa cái bịa. **Đóng góp = chính quy trình lọc-tạo-data này** (data-centric), không phải bản thân distillation.
- **Trụ bình duyệt (verify):** **BLIP CapFilt (ICML 2022)** = "captioner sinh + filter loại nhiễu"; **KnowAda (NAACL 2025)** = fine-tune VLM trên caption đã-điều-chỉnh → **giảm ảo giác mà GIỮ độ chi tiết**; **VGA (Findings EMNLP 2024)** = fine-tune VLM cho **GUI** để **giảm ảo giác**.

## 0.4. Model + cách huấn luyện (cụ thể)

- **Base:** `Qwen2.5-VL-3B-Instruct` (VLM mở, nhỏ, chạy on-device). **QLoRA 4-bit**, rank 8–16, gradient-checkpointing, checkpoint ra Drive (chống ngắt Colab).
- **Chỉ SFT — KHÔNG RL** (RL/GRPO đã bị 2 debate bác: nặng + reward-hack). SFT ổn định, vừa Colab.
- **Input train:** ảnh + câu hỏi (**KHÔNG đưa View Hierarchy vào lúc train** — giữ luật vàng chống rò rỉ). **Target:** hướng dẫn đã-lọc.
- **Quy mô:** ~1,5–3k mẫu (mở rộng pool màn MobileViews public; teacher API ~$5–20).
- **Trụ distill teacher→VLM nhỏ (verify):** **ALLaVA** (GPT-4V→lite VLM 3B/4B ngang 7–13B), **LLaVA-KD (ICCV 2025)**, GenRecal.

## 0.5. Quy trình LỌC — thích-nghi có chủ đích (KHÔNG phải phát minh mới), điều-kiện-cần cho đóng góp

1. Teacher sinh hướng dẫn nháp.
2. Matcher (`nomic`) đối chiếu từng tên nút với View Hierarchy → bước **matched** (giữ) / **bịa** (viết lại thành mô tả bằng lời — PA2, hoặc loại).
3. **Đo silent-error của bộ lọc TRƯỚC** (cổng K1, recall-conditioned) — biết bộ lọc sạch đến đâu trước khi dùng làm target.
4. **Seed câu-đúng-THẬT từ AndroidControl gold-action** khi có (dựng target đúng thật, không tự-chấm) — bù chỗ VH mù.
> ⚠️ **Sau debate tính-mới (`report/52`): đây KHÔNG phải "quy trình lọc MỚI".** Công thức generate→filter→retrain đã có tên (STaR, Zelikman 2022) và cơ chế cụ thể "viết-lại-phần-không-kiểm-chứng-được thành mô tả chung chung" gần-song-ánh với KnowAda (NAACL25). Vai trò đúng của bước này = **điều-kiện-cần** để trụ đóng góp thật (§0.6, robust-khi-không-VH) có ý nghĩa — KHÔNG tự nó là novelty. Khác biệt thật duy nhất so với KnowAda: nguồn xác nhận là VIEW HIERARCHY bên ngoài (external, có cấu trúc), không phải model tự-probe chính nó (self-referential/circular).

## 0.6. Đo cái gì (estimand — điểm dễ sai nhất)

- ❌ **KHÔNG đo faithfulness-SAU-hậu-kiểm** — vì hậu-kiểm đã đưa nó về ~100% (bão hoà) → train vô ích, đo ra 0 chênh lệch.
- ✅ **TRỤ THỰC NGHIỆM SỐ MỘT (sau debate `report/52` — đây là nơi tính-mới thật sự sống hay chết, phải pre-register cỡ mẫu + ngưỡng đậu/rớt TRƯỚC pilot):**
  - **(c) robust khi KHÔNG có VH** (tắt hậu-kiểm hoàn toàn lúc suy luận, held-out theo APP) — nơi student là phòng thủ DUY NHẤT, không có accessibility tree nào để dựa vào = **niche on-device**. Câu hỏi: hành-vi né-bịa có được NỘI TẠI HOÁ vào trọng số 3B, hay chỉ là pattern bề mặt phụ thuộc bộ lọc bên ngoài? Có thể ra NULL thật — nếu null, báo trung thực ("chưa nội-tại-hoá được ở scale 3B"), KHÔNG giấu.
- **Đo bổ trợ (điều-kiện-cần, KHÔNG phải trụ chính):**
  - (a) **tỉ-lệ-bịa của STUDENT lúc sinh** vs base/teacher (student ≤ teacher-raw?);
  - (b) **%fallback ↓** — student ít bịa → ít phải viết-lại-thành-mô-tả → hướng dẫn **cụ thể/hữu-ích hơn ở cùng mức trung thực**;
  - (d) **chi phí / độ trễ / VRAM**.
- **Bảng số chính:** base / teacher-raw / teacher-lọc / student; **ablation train-trên-LỌC vs train-trên-RAW** (cô lập giá trị lớp lọc — vai trò: robustness-check hỗ trợ, KHÔNG phải bằng chứng novelty tự thân, vì 2/7 precedent gần nhất — KnowAda, BLIP-CapFilt — đã làm đúng dạng ablation này).
- **Trụ đo-không-gold (verify):** **FEWL** (đo & giảm ảo giác không cần gold), **Mind-the-Gap (ICLR 2025)** (generation-verification gap chi phối cải thiện từ dữ liệu tự-sinh-đã-lọc).

## 0.7. Chống vòng lặp + thống kê (giữ nghiêm dù eval là phụ)

- **Lọc bằng `nomic`; CHẤM bằng họ KHÁC:** `bge-m3` + LLM-judge non-GPT + **neo người ~80–120 mẫu (báo κ)**. **Held-out theo APP** (không chỉ theo màn).
- **Paired design** (student vs base trên CÙNG màn → paired bootstrap, triệt phương sai giữa-app) + **pre-register MDE** + wild-cluster bootstrap-t. Mẫu nhỏ (~24 app hiệu dụng) → nếu thiếu power: khai "exploratory / đường-cong", **null vẫn đậu**.

## 0.8. Đóng góp + độ mới (wedge) — bản đã vá sau debate tính-mới (`report/52`)

- **(A) MODEL sinh hướng dẫn GUI on-device**, train bằng faithful distillation (đóng góp CHÍNH) — chứng minh bằng thực nghiệm **robust-khi-không-VH** (§0.6), KHÔNG bằng "có model" hay "có ablation" đơn thuần.
- **(B) Quy trình LỌC-faithfulness tạo data** = thích-nghi có chủ đích từ STaR/KnowAda/CapFilt, KHÔNG phải phát minh — vai trò điều-kiện-cần.
- *(phụ) Phương pháp đánh giá no-gold — tái dùng có chủ đích, pre-register TRƯỚC ý tưởng train model (chống p-hacking, một rủi ro mà KnowAda/CapFilt không cần né).*
- **Wedge thật sự (sau khi loại bỏ 4/5 đòn tấn công đã xác nhận hợp lệ):** KHÔNG phải "chưa ai ghép recipe lọc+distill vào GUI" (đã gần — VGA/KnowAda/CapFilt) mà là — khi bộ lọc dùng **nguồn xác nhận bên ngoài có cấu trúc** (VH, không self-probe) cho một hành vi **rủi ro cao** (bịa tên nút → thao tác sai, khác caption vô hại), tín hiệu né-bịa đó có **sống sót khi nén xuống 3B on-device VÀ không còn accessibility-tree lúc suy luận** hay không — câu hỏi này chưa precedent nào (VGA/KnowAda/CapFilt/STaR/dòng GUI-agent 2026 WinDOM/Trust-the-Right-Teacher/LiteGUI) đặt ra, và có thể ra kết quả null.

## 0.9. Khả thi <3 tháng (lịch)

| Tuần | Việc |
|---|---|
| 1 | Mở rộng pool màn · teacher sinh · **lọc** → tập SFT · đo silent-error bộ lọc · **smoke-test 20 mẫu chạy trọn vòng** |
| 2–4 | SFT-QLoRA Qwen2.5-VL-3B + tinh chỉnh (**deadline cứng 3 tuần**) |
| 5–7 | Đánh giá: bảng số + ablation lọc-vs-raw + neo người nhỏ (E16) + thống kê paired |
| 8–10 | Viết. **CẮT nhiều-màn** (để bài FAIR/future) |

Chi phí: teacher ~$5–20 + Colab Pro+ ~$100–150.

## 0.10. Rủi ro + thủ sẵn

| Rủi ro | Thủ |
|---|---|
| "student ≈ teacher, không mới" | ablation lọc-vs-raw + niche on-device + claim "**ngang teacher, rẻ 1/50, chạy trên máy**" (KHÔNG "vượt teacher") |
| delta nhỏ / thiếu power (mẫu ~24 app) | paired design + pre-register MDE + null-vẫn-đậu |
| data nhiễu (teacher bịa × VH mù >77%) | đo silent-error bộ lọc trước + seed AndroidControl gold + loại target %fallback cao |
| lọc gây hướng dẫn cụt | **KnowAda** cho thấy giữ được độ chi tiết; kiểm hữu-ích định tính (E16) |
| rò rỉ (leakage) | input train chỉ ảnh+câu hỏi; distill hành-vi "mô-tả-khi-không-chắc", KHÔNG tra tên nút từ VH |

## 0.11. Neo citation (trụ bình duyệt — đã verify ở deep-research + debate tính-mới `report/52`)

- **Meta-pattern generate→filter→retrain (PHẢI thừa nhận là khung sườn đã có, không phải của ta):** STaR/RFT/ReST — Zelikman et al. 2022 (arXiv 2203.14465).
- **Fine-tune VLM giảm ảo giác cho GUI:** VGA — Findings EMNLP 2024 (arXiv 2406.14056). *Câu phân định: VGA ràng buộc LÚC SINH (Referent Method), ta lọc HẬU-KIỂM sau khi sinh mù.*
- **Fine-tune trên data đã-lọc/điều-chỉnh → giảm ảo giác GIỮ chi tiết:** KnowAda "Bridging the Visual Gap" — NAACL 2025 (arXiv 2411.09018). *Câu phân định: KnowAda lọc bằng self-probe VQA (circular), ta lọc bằng đối chiếu VH bên ngoài (external, có cấu trúc); rủi ro bịa của ta là actionable (bấm sai nút), không phải chi tiết caption vô hại.*
- **Sinh + LỌC (bootstrapping data):** BLIP CapFilt — ICML 2022 (arXiv 2201.12086). *Câu phân định: CapFilt không đo robust-khi-thiếu-nguồn-lọc-lúc-suy-luận; ta thêm đúng phép đo này.*
- **Viết lại phát ngôn bịa dựa trên tri thức nền có cấu trúc:** FaithDial/BEGIN — Dziri et al., TACL 2022 (arXiv 2204.10757). *Câu phân định: FaithDial coi "generic/mơ hồ" là LỖI cần sửa; ta coi mô tả chung chung là CHIẾN LƯỢC né-bịa có chủ đích, giữ hữu ích mà không đoán bừa.*
- **Distill teacher → VLM nhỏ:** ALLaVA (arXiv 2402.11684) · LLaVA-KD — ICCV 2025 (arXiv 2410.16236) · GenRecal (arXiv 2506.15681).
- **VLM nhỏ on-device / thiết bị hạn chế:** VLsI — CVPR 2025 (arXiv 2412.01822).
- **Giảm ảo giác KHÔNG gold + lý thuyết lọc-rồi-train:** FEWL (arXiv 2402.10412) · Mind-the-Gap — ICLR 2025 (arXiv 2412.02674).
- **Dòng GUI-agent 2026 gần nhất (PHẢI trích để chủ động phân định trước khi bị hỏi):** WinDOM (arXiv 2606.25964) · Trust-the-Right-Teacher (arXiv 2606.18101) · LiteGUI (arXiv 2605.07505) · CORA (arXiv 2604.09155). *Câu phân định chung: các paper này verify bằng HÌNH HỌC liên tục (click-in-bbox) cho agent bấm-máy, recovery chỉ nhị phân execute/abstain; ta verify bằng đối chiếu NGỮ-NGHĨA-CẤU-TRÚC (tên nút so với VH) cho văn bản tự do người-đọc, recovery liên tục (mô tả mơ hồ vẫn hữu ích).*
- **Giữ nguyên trụ đánh giá cũ** (ALOHa NAACL24 · FaithScore EMNLP24 · Sai EMNLP21 · Fagin SIAM06 · Panickssery NeurIPS24…). *(⚠ verify lại arXiv ID + venue trước khi in.)*
- **⚠ KHÔNG dùng:** bất kỳ khung "Application-vs-Modeling theo arXiv 2508.10795" — đã verify đây là trích dẫn bịa/gán sai claim cho một paper có thật (paper đó không định nghĩa tiêu chí này).

---

# PHỤ LỤC 0-CŨ — (LỖI THỜI) phương án grounding + RLVR đã bị 3 debate bác

> ⚠️ Toàn bộ các mục **## 0.1–## 0.12 DƯỚI ĐÂY** là phương án CŨ (grounding, point-in-bbox làm reward). **ĐÃ BỊ BÁC** (vòng-lặp/lệch-trục/trùng-lặp — `report/50` §7). Giữ lại chỉ để tham chiếu lịch sử cân nhắc. **KHÔNG làm theo** — hướng chốt là Faithful Distillation ở trên.

## 0.1. Vì sao đổi + mục tiêu mới

**Vì sao:** thầy chê khung cũ *"chủ yếu prompting (gọi API gpt-4o-mini + so embedding), chưa thấy MODEL đâu"*; quy định thạc sĩ trường bắt **sản phẩm phải là một MÔ HÌNH do học viên HUẤN LUYỆN**.

**Mục tiêu mới (một câu):** *Xây dựng một **mô hình bám-màn (GUI grounding)** — fine-tune từ VLM nhỏ bằng LoRA rồi hậu-huấn-luyện bằng học tăng cường với **thưởng tự động** — trong đó **chính thước đo không-đáp-án-mẫu (point-in-bbox / độ trung thực) là HÀM THƯỞNG**; đặt mô hình này làm lõi của hệ sinh hướng dẫn sử dụng phần mềm, và đánh giá hệ bằng phương pháp không-đáp-án-mẫu.*

Cụm khoá chống lời chê "chỉ prompting": **có trọng số được huấn luyện, có đường cong học, có ablation SFT-vs-RL, có bảng số trước/sau train.**

## 0.2. Nhìn tổng thể một hình (toàn kiến trúc)

```
                         ┌─────────────────────────────────────────────┐
 VÀO: 1 ảnh (hoặc N ảnh  │                                             │
 xáo trộn) + câu hỏi ───▶│  (nhiều màn) STAGE-0 sắp thứ tự màn         │  ← thuật toán
                         │   so cặp → đếm phiếu (Copeland) → gỡ vòng    │
                         └───────────────────┬─────────────────────────┘
                                             ▼
                         ┌─────────────────────────────────────────────┐
                         │  Bộ SINH hướng dẫn (VLM) → các bước ngôn ngữ │  ← có sẵn / hoặc distill
                         └───────────────────┬─────────────────────────┘
                                             ▼
                ┌────────────────────────────────────────────────────────┐
                │  ★ MÔ HÌNH BÁM-MÀN (GROUNDING) — ĐÓNG GÓP CHÍNH ★        │  ← MÔ HÌNH TỰ TRAIN
                │  Qwen2.5-VL-3B + LoRA, huấn luyện SFT → RLVR             │     (LoRA + RLVR)
                │  vào: (ảnh + tên/ý-định phần tử) → ra: toạ độ (x,y)/vùng │
                └───────────────────┬────────────────────────────────────┘
                                     ▼
                ┌────────────────────────────────────────────────────────┐
                │  Lớp KIỂM point-in-bbox / faithfulness                   │  ← 2 VAI:
                │  (x,y) ∈ khung nút thật? bước nhắc nút không có → mô tả  │     reward khi TRAIN
                └───────────────────┬────────────────────────────────────┘     thước khi ĐO
                                     ▼
                         RA: hướng dẫn từng bước, có kiểm chứng bám màn
```

**Đọc hình:** phần **★** (mô hình bám-màn) là **thứ được huấn luyện** — đóng góp "model" của luận văn. Các khối còn lại: Stage-0 = thuật toán; bộ sinh = VLM có sẵn (hoặc distill sau); lớp kiểm = thuật toán, **nhưng tín hiệu của nó chính là hàm thưởng để train mô hình ★**.

## 0.3. MÔ HÌNH ĐÓNG GÓP — chi tiết huấn luyện

- **Nền (base):** `Qwen2.5-VL-3B-Instruct` (VLM mở, nhỏ, chạy được on-device).
- **Cách chỉnh:** **LoRA** (rank 8, alpha 16) — chỉ train một ít ma trận thấp-hạng, đóng băng phần lớn trọng số → vừa 1 GPU 24GB (Colab). *(Trụ: ZonUI/Qwen-GUI-3B, WACV 2026.)*
- **Nhiệm vụ mô hình:** *grounding* — cho **ảnh màn + tên/ý-định một phần tử** → trả **toạ độ (x,y) hoặc vùng nút** cần bấm.
- **Hai giai đoạn huấn luyện:**
  1. **Giai đoạn 1 — SFT (học có giám sát):** học bám-màn từ **ScreenSpot-v2 (bbox chuẩn) + AndroidControl (toạ độ/thao-tác vàng)**. Ra một mô hình grounding cơ bản.
  2. **Giai đoạn 2 — RLVR / GRPO (học tăng cường, thưởng kiểm-chứng-được):** tối ưu bằng **hàm thưởng TỰ ĐỘNG**
     $$R = R_{\text{coord}} + R_{\text{type}} + R_{\text{format}},\qquad R_{\text{coord}} = \mathbb{1}[(x,y)\in \text{bbox vàng}]$$
     — tức **điểm point-in-bbox của phương pháp no-gold CHÍNH LÀ phần thưởng**. Không cần người gán nhãn. *(Trụ: UI-R1, AAAI 2025 — 136 mẫu đã +22% ScreenSpot; SE-GUI, NeurIPS 2025 — ~3k mẫu.)*
- **Vì sao đây là "model thật" (không phải prompting):** có tập tham số LoRA được cập nhật bằng gradient, có đường cong reward/accuracy theo bước train, có **ablation "SFT" vs "SFT+RLVR"** và **bảng số trước/sau** trên ScreenSpot-v2/AndroidControl.

## 0.4. Phương pháp đánh giá no-gold — GIỜ LÀM HAI VAI

Đây là chỗ đẹp nhất của hướng mới: thước đo cũ **không bị vứt đi**, mà **kiêm thêm vai huấn luyện**.

| Vai | Dùng khi | Cụ thể |
|---|---|---|
| **Hàm THƯỞNG (mới)** | lúc TRAIN (RLVR) | point-in-bbox = reward để mô hình học bám đúng nút |
| **Thước ĐO (cũ)** | lúc ĐÁNH GIÁ | độ trung thực · τ thứ-tự-bộ-phận · Step-SR · point-in-bbox trên tập no-gold |

→ Câu chốt trước thầy: *"Phương pháp đánh giá không-đáp-án-mẫu của em vừa là thước đo, vừa là **tín hiệu huấn luyện** cho mô hình — đó là điểm mới, và là lý do mô hình không cần bộ hướng-dẫn-mẫu do người soạn."*

## 0.5. Dòng dữ liệu: TRAIN vs ĐO (tách bạch, chống rò rỉ)

- **TRAIN (có gold để làm reward):** ScreenSpot-v2 (bbox), AndroidControl (thao-tác/toạ-độ vàng từng bước).
- **ĐO không-gold (không có hướng dẫn mẫu):** MobileViews (ảnh + View Hierarchy) — đo *độ trung thực* của hệ sinh (dùng mô hình đã train để bám nút), theo đúng bộ thước cũ.
- **Ranh giới quan trọng (cảnh báo trung tâm từ research):** đóng góp *mô hình* đặt ở **grounding** (nơi CÓ gold để train + reward tự động); phần **sinh hướng-dẫn-cho-người** giữ vai **ứng dụng + đánh giá no-gold** — đây là wedge khác biệt, tránh trùng các bài GUI-agent.

## 0.6. Pipeline từng-bước-nhỏ + model mỗi bước (đúng thứ thầy yêu cầu)

| Bước | Việc | Model / công cụ | Huấn luyện? |
|---|---|---|---|
| 1 | Định tuyến (đếm ảnh) | luật | — |
| 2 | (nhiều màn) sắp thứ tự màn | so cặp + Copeland + gỡ vòng (thuật toán) | — |
| 3 | Sinh hướng dẫn ngôn ngữ | VLM có sẵn (hoặc distill sau) | tuỳ chọn |
| **4** | **Bám-màn: bước ↔ toạ độ nút** | **Qwen2.5-VL-3B + LoRA + RLVR** | ✅ **MÔ HÌNH CHÍNH** |
| 5 | Kiểm point-in-bbox / né bịa | thuật toán (đồng thời là reward) | — |
| 6 | (tuỳ chọn) verifier phát-hiện-ảo-giác | action-head/verifier nhẹ | ✅ tuỳ chọn (Phase 2) |

## 0.7. Cái gì ĐỔI so với khung cũ (bản đồ chuyển)

| Khung CŨ (prompting) | Khung MỚI (model-centric) |
|---|---|
| gpt-4o-mini gọi API làm lõi | **Qwen2.5-VL-3B tự train (LoRA+RLVR)** làm lõi; gpt-4o-mini hạ vai teacher |
| point-in-bbox = chỉ để chấm | point-in-bbox = **hàm thưởng train** + thước chấm |
| Đóng góp A = "hệ thống prompting" | Đóng góp A = **mô hình grounding huấn luyện được** |
| Đóng góp B = phương pháp đánh giá | Giữ B, **kiêm vai tín hiệu train** |
| Chạy API, không GPU | **Colab Pro/Pro+ (LoRA 3B 24GB)** |

## 0.8. Đóng góp + độ mới (wedge)

- **(A) Mô hình bám-màn huấn luyện bằng RLVR với thước-đo-no-gold làm reward** — sản phẩm "model" của luận văn.
- **(B) Phương pháp đánh giá không-đáp-án-mẫu** — vừa đo vừa làm reward.
- **Độ mới (khác InfiGUI-R1 / SE-GUI / UI-R1):** các bài đó train **agent bấm máy** (task-success, có gold). Ta train grounding **đặt trong bộ sinh hướng-dẫn-CHO-NGƯỜI**, cho tác vụ **không có đáp án mẫu**, và dùng **độ-trung-thực làm reward** — tổ hợp chưa ai làm (đã có nền `report/42`).

## 0.9. Compute + chi phí (Colab)

- LoRA 3B vừa **24GB** (Colab L4/A100). RLVR cần **ít mẫu** (136–3k). Ước cả luận văn (gồm chạy lỗi/lặp) ~**40–80 GPU-giờ**.
- Chi phí ~**$100–150** (Colab **Pro+ $50/th × 2–3 th**, có background execution để train không đứt) — hoặc **< $50** nếu thuê GPU ngoài (RunPod/Vast ~$0,4/h). Giá đổi theo thời điểm, kiểm lại khi mua.

## 0.10. Kế hoạch thí nghiệm (điều chỉnh cho model)

| TN | Câu hỏi | Đo trên | Kỳ vọng |
|---|---|---|---|
| M1 | SFT grounding có học được không? | ScreenSpot-v2 | acc tăng rõ so với base |
| M2 | RLVR có nâng thêm không? | ScreenSpot-v2 / AndroidControl | acc ↑ (đường cong reward), ablation SFT vs SFT+RLVR |
| M3 | Reward nào tốt? | biến thể R_coord/R_type | biện minh thiết kế reward |
| M4 | Hệ sinh dùng model có bám màn hơn? | MobileViews (no-gold) | độ trung thực ↑ so với baseline (giữ bộ thước cũ) |
| M5 (tuỳ) | Verifier nhẹ có ích? | tập perturbation | phát hiện lỗi, κ với người |

→ **Pre-register ngưỡng trước khi nhìn kết quả** (giữ kỷ luật cũ).

## 0.11. Rủi ro + câu hỏi mở (phải thủ)

1. **Lệch tác vụ:** precedent là agent-có-gold, không phải sinh no-gold → **đóng góp model ở grounding**, phần sinh giữ no-gold (đã xử ở §0.5).
2. **Reward cho phần sinh no-gold:** độ trung thực có đủ *dày & ít nhiễu* để làm reward RL không, hay **chỉ nên dùng làm bộ lọc distillation**? → cần thử; mặc định dùng point-in-bbox (dày) cho grounding.
3. **Thời gian/VRAM Colab L4 thực tế** cho LoRA-distill + light-RL 3B → chạy thử mẩu nhỏ trước.
4. **Nhãn cho verifier** khi không gold → sinh cặp *perturbation* (bơm lỗi đã-biết); kiểm κ với người.

## 0.12. Neo citation (theo luật: xương-sống chỉ trích bình duyệt)

- **Bình duyệt (trụ):** UI-R1 (AAAI 2025) · SE-GUI (NeurIPS 2025) · GUI-Actor (NeurIPS 2025) · ZonUI/Qwen-GUI-3B (WACV 2026).
- **Preprint (chỉ hiện-vật kỹ thuật, verify ID trước khi trích):** LiteGUI, GUI-AIMA, ReGUIDE, InfiGUI-R1, self-distillation.
- **Giữ nguyên trụ cũ cho đánh giá:** ALOHa (NAACL24), FaithScore (EMNLP24), Fagin (SIAM06), AITW/AndroidControl/SeeClick, Sai (EMNLP21), Panickssery (NeurIPS24)…

---

# CHƯƠNG 1 — GIỚI THIỆU

## 1.1. Bối cảnh và động lực

Hằng ngày, hàng triệu người mở một phần mềm lạ và mắc kẹt ở một câu hỏi rất đời thường: *"giờ tôi phải bấm vào đâu?"*. Tài liệu hướng dẫn viết tay thì đắt, lỗi thời nhanh, và không thể phủ hết mọi ứng dụng, mọi phiên bản, mọi màn hình. Nếu có một trợ lý **nhìn được ảnh màn hình đang hiển thị** và **viết ra hướng dẫn từng bước** cho đúng ngữ cảnh đó, thì lợi ích trải rộng: tự động hoá tài liệu trợ giúp; dẫn dắt người mới làm quen phần mềm (onboarding); và đặc biệt là **trợ năng cho người khiếm thị** — nhóm phụ thuộc nặng vào việc phần mềm mô tả đúng thứ đang có trên màn.

> **Bốn chỗ dùng thật (để trả lời "không leo leaderboard agent thì ứng dụng là gì?"):**
> 1. **Trợ giúp ngay trong ứng dụng (in-app help).** Người dùng đang đứng ở một màn, hỏi "làm sao đổi mật khẩu?" → hệ đọc ảnh màn hiện tại, trả lời bằng các bước bám đúng nút *đang có* trên màn đó.
> 2. **Tự sinh tài liệu how-to.** Thay vì đội kỹ thuật viết tay từng bài và cập nhật mỗi lần app đổi giao diện, hệ sinh nháp trực tiếp từ ảnh màn.
> 3. **Hỗ trợ khách hàng.** Khách gửi ảnh chụp màn kèm câu hỏi → hệ sinh hướng dẫn bám đúng ảnh đó, thay vì trả lời chung chung.
> 4. **Trợ năng & onboarding — và niche *on-device*.** Trên Android, **AccessibilityService cấp cây trợ năng (a11y tree) sống** cho màn đang hiển thị → hệ có ngay danh sách nút thật để đối chiếu, chạy được **trên máy với model nhỏ** — đúng chỗ bước đối chiếu với giao diện thật có giá trị nhất.
>
> **Vì sao setup này KHÁC "AI tự bấm máy" (leaderboard agent) — và khác biệt đó là ĐIỂM MẠNH, không phải điểm yếu:** đầu ra của ta là hướng dẫn cho **con người** làm theo (người còn trong vòng lặp, tự dừng khi thấy vô lý), không phải lệnh cho máy tự thực thi (sai là bấm bậy, khó thu hồi). Vì thế ta chấm bằng **chất lượng hướng dẫn cho người** (không có đáp án chuẩn), *không* so điểm task-success với leaderboard agent — không phải vì yếu hơn, mà vì **đo thứ khác**. Chính chỗ "đo thứ khác, không có đáp án chuẩn" này là lý do đóng góp (B) tồn tại.

Công nghệ khiến việc này khả thi là **mô hình ngôn ngữ thị giác (VLM)**. Đây là lớp mô hình AI thế hệ mới, có khả năng đồng thời "nhìn" ảnh và "đọc–viết" văn bản. Ta đưa cho nó một ảnh chụp màn hình cùng một câu hỏi, nó trả về một đoạn hướng dẫn. Nghe thì lý tưởng, nhưng chính cách VLM hoạt động lại gieo mầm cho khó khăn trung tâm của luận văn.

> **Định nghĩa 1.1 (VLM — Vision-Language Model).** Mô hình ngôn ngữ thị giác là một mô hình học máy ánh xạ cặp *(ảnh, văn bản)* thành *văn bản*. Về bản chất, nó **dự đoán chuỗi chữ có xác suất cao nhất** dựa trên các quy luật thống kê học được từ khối dữ liệu huấn luyện khổng lồ, chứ **không "hiểu" giao diện theo nghĩa con người**. Nó không thật sự "biết" nút nào đang có trên màn; nó chỉ đang ước lượng "câu trả lời trông giống một hướng dẫn hợp lý sẽ như thế nào". Chính cơ chế dự đoán theo xác suất này khiến nó đôi lúc sinh ra nội dung nghe rất trôi chảy, rất tự tin, nhưng **không có thật** — hiện tượng gọi là *ảo giác* (hallucination).

Nói cách khác: điểm mạnh (sinh văn bản trôi chảy từ ảnh) và điểm yếu (bịa ra thứ không tồn tại) của VLM đến từ cùng một cơ chế. Luận văn không cố "chữa" VLM ở tầng mô hình; thay vào đó, ta bọc quanh VLM một **lớp kiểm soát** buộc đầu ra phải chịu trách nhiệm trước những gì thật sự có trên màn.

## 1.2. Phát biểu bài toán (hình thức hoá)

Để tránh mơ hồ, ta phát biểu bài toán như một *hợp đồng vào–ra* rõ ràng. Đây cũng là ranh giới phân định luận văn với các hướng lân cận (chẳng hạn "AI tự bấm máy" — sẽ phân biệt ở §1.3 và Chương 9).

> **Định nghĩa 1.2 (Hợp đồng vào–ra).**
> **Đầu vào:** một tập ảnh màn hình $S = \{s_1, s_2, \dots, s_N\}$ với $N \ge 1$. Khi $N \ge 2$, thứ tự các ảnh trong tập **đã bị xáo trộn** — hệ không được biết trước màn nào đến trước. Kèm theo là một câu hỏi $q$ bằng ngôn ngữ tự nhiên.
> **Đầu ra:** một bản hướng dẫn $T = (t_1, t_2, \dots, t_k)$ gồm $k$ bước **có thứ tự**; mỗi bước $t_i$ là một câu thao tác cho người đọc làm theo (ví dụ *"Chọn nút OK"*, *"Cuộn xuống rồi bấm Thêm vào màn hình chính"*).
> **Ràng buộc bắt buộc:**
> 1. Câu hỏi $q$ **không được chứa tên nút** — nếu câu hỏi đã nói sẵn "bấm nút Settings" thì ta chẳng đo được gì, vì máy chỉ việc chép lại. Câu hỏi phải buộc máy tự đọc ảnh.
> 2. Tài nguyên chấm điểm (cây phân cấp giao diện, quỹ đạo vàng) **không được cấp cho mô hình ở thì sinh** — chỉ được dùng lúc chấm (xem Nguyên tắc 3.1, "luật vàng chống rò rỉ").
>
> Trường hợp $N=1$ gọi là **một màn**; trường hợp $N \ge 2$ gọi là **nhiều màn** và đòi hỏi thêm bước **suy luận thứ tự**.

Hai ràng buộc trên không phải chi tiết kỹ thuật vụn vặt — chúng là *điều kiện để phép đo có ý nghĩa*. Nếu vi phạm, mọi con số đẹp thu được đều là ảo (Chương 7 sẽ phân tích kỹ dưới tên "circularity" và "data leakage").

## 1.3. Ba thách thức trung tâm

Bài toán trên gói ba khó khăn riêng biệt, và luận văn phải trả lời cả ba.

**1. Ảo giác giao diện.** VLM tham chiếu tới phần tử không tồn tại trên màn đang xét: nhắc "bấm nút Menu" khi màn không có nút nào tên Menu, hoặc "mở Cài đặt" khi không có lối vào Cài đặt. Đây là dạng lỗi *đặc thù* của bài toán (khác với ảo giác trong sinh văn bản thuần), có tần suất cao, và nguy hiểm vì nó dẫn người dùng đi sai. Đóng góp (A) sinh ra chủ yếu để đối phó với thách thức này.

**2. Thiếu đáp án mẫu.** *Đây là khó khăn khoa học trung tâm.* Không tồn tại một kho hướng dẫn chuẩn, do con người soạn tỉ mỉ, phủ đủ mọi ứng dụng và mọi câu hỏi, để ta lấy làm mốc "đúng". Không có mốc thì không so được theo lối kinh điển. Cả một mảng nghiên cứu đánh giá — BLEU, ROUGE, so khớp với tham chiếu người — đều giả định có đáp án mẫu; ở đây giả định đó biến mất. Luận văn kế thừa **khung đánh giá cho văn bản tổng hợp không có đáp án chuẩn** từ Chim, Ive & Liakata (*Computational Linguistics* 51(1):191–233, 2025) — lưu ý đây là **tạp chí**, không phải "ACL 2025" — nhưng chỉ kế thừa *khung đánh giá* (Nội tại + Ngoại lai), **không** kế thừa bài toán sinh của họ (họ làm text→text). Đóng góp (B) là câu trả lời cho thách thức này.

**3. Suy luận thứ tự.** Khi đầu vào là nhiều ảnh bị xáo trộn, hệ phải **tự khôi phục trình tự đúng** trước khi viết hướng dẫn (không thể bảo "chụp ảnh 3 trước ảnh 1"), và ta phải **đo được** năng lực khôi phục đó một cách khách quan. Đây là nơi nhánh nhiều màn và thước $\tau$ (Chương 5) vào cuộc.

> **Ranh giới cần nhấn mạnh ngay:** luận văn sinh **hướng dẫn cho *người* đọc**, không phải điều khiển một *agent* tự bấm máy. Vì vậy ta **không** đặt mục tiêu leo bảng xếp hạng (leaderboard) của các benchmark điều khiển agent — setup khác nhau về bản chất. Điều này sẽ được viện dẫn nhiều lần khi phân biệt với công trình liên quan (Chương 9) và khi khiêm tốn hoá các claim (Chương 10).

## 1.4. Đóng góp

> ⚠️ **[LỖI THỜI — khung cũ]** Khung "hai đóng góp = (A) hệ prompting + (B) đánh giá" đã đổi. Đóng góp MỚI: **(A) MÔ HÌNH grounding tự huấn luyện (LoRA + RLVR), (B) phương pháp đánh giá no-gold kiêm HÀM THƯỞNG.** → đọc **Chương 0 §0.8**.

- **(A) Hệ thống sinh** làm giảm ảo giác bằng bước đối chiếu với giao diện thật và bước sắp lại thứ tự các màn — trình bày ở **Chương 4**.
- **(B) Phương pháp đánh giá** không cần đáp án mẫu, không tự chấm — trình bày ở **Chương 5**, kiểm định bằng nhiễu loạn ở **Chương 7**.

Hai đóng góp được đặt **ngang vai *có điều kiện*** (chi tiết §10.1): điều kiện là nhánh nhiều màn phải cho ra con số dương thật. Ngay cả khi điều kiện đó chưa được thoả, (A) vẫn đứng vững nhờ ba chân độc lập — đạt mục tiêu thiết kế, đo được tỉ lệ ảo giác gốc và giá phải trả, và có đối chứng thất bại đo được — chứ không dựa vào độ phức tạp mã nguồn.

---

# CHƯƠNG 2 — KIẾN THỨC NỀN & THUẬT NGỮ

Chương này giải thích tận gốc các khái niệm sẽ dùng xuyên suốt, ở mức người chưa từng học AI cũng theo được. Ai đã quen có thể lướt sang Chương 3.

## 2.1. Ảo giác (hallucination)

*Ảo giác* là hiện tượng mô hình sinh ra một phần tử hoặc một khẳng định **không có thật**, và trình bày nó một cách trôi chảy, tự tin đến mức người đọc khó nghi ngờ. Trong bài toán của ta, biểu hiện cụ thể là một bước hướng dẫn nhắc tới **một nút không tồn tại trên màn đang xét**. Cần phân biệt với "sai chính tả tên nút" (nút có thật nhưng gọi lệch tên — đó là vấn đề *đúng nhãn*, §5.1): ảo giác là *nút hoàn toàn không có*.

Vì sao ta không chỉ "bảo VLM đừng ảo giác"? Vì như Định nghĩa 1.1 đã nêu, ảo giác không phải một lỗi có công tắc tắt/bật — nó là hệ quả của cơ chế dự đoán theo xác suất. Cách hành động khả thi là **kiểm chứng đầu ra sau khi sinh**, dựa vào một nguồn sự thật về "màn này thật sự có gì". Nguồn đó chính là cây phân cấp giao diện.

## 2.2. Cây phân cấp giao diện (View Hierarchy — VH)

Hệ điều hành Android, ở mọi thời điểm, duy trì sẵn một cấu trúc dữ liệu mô tả **mọi phần tử đang hiển thị** trên màn: mỗi phần tử có tên (trường `text` hoặc `content-description`), toạ độ khung bao (bounding box), loại (nút bấm / ô nhập chữ / ảnh / nhãn), và các thuộc tính (bấm được không, nhập được không). Cấu trúc này vốn dĩ **sinh ra để phục vụ công nghệ trợ năng** — để trình đọc màn hình đọc được giao diện cho người khiếm thị — nên nó tồn tại sẵn, miễn phí, không cần ta tự dựng.

> **Định nghĩa 2.1 (View Hierarchy).** Với một màn $s$, ký hiệu $\text{VH}(s) = \{e_1, e_2, \dots, e_m\}$ là tập các phần tử của màn. Mỗi phần tử $e_j$ mang một nhãn $\ell_j$ (chuỗi văn bản mô tả) và một khung bao $\text{box}_j = (l_j, t_j, r_j, b_j)$ — bốn số là toạ độ trái/trên/phải/dưới tính bằng pixel.
>
> **VH đóng vai "nhãn bạc" (silver label):** nó không phải đáp án vàng do người soạn cho *bài toán hướng dẫn*, nhưng là một **mốc tự động đủ tin cậy** về "màn này có những nút gì". Ta dùng nó làm **proxy no-gold để đánh giá** mà không cần người soạn hướng dẫn mẫu.
> **Không "thay 1:1" đáp án do người soạn viết** (khai thẳng để không overclaim): VH là proxy **có điều kiện, recall-conditioned** — nó phủ được *"nút gì có trên màn"* và *thứ tự*, nhưng **không** phủ *"diễn đạt rõ / đúng ý cho người đọc"* (thứ mà đáp án do người soạn vốn bắt); và VH tự thiếu nhãn (>77% app — Chen, ICSE 2020) → ta báo mọi số **"có điều kiện độ phủ nhãn"** (§7.3), không coi VH thay hoàn toàn cho đáp án do người soạn.

Một điều tối quan trọng, sẽ nhắc lại nhiều lần: **VH chỉ được dùng ở thì *chấm điểm*, tuyệt đối không đưa cho VLM ở thì *sinh*.** Nếu đưa, VLM chỉ việc chép danh sách nút và ta mất khả năng đo *mức nó tự ảo giác* — vốn là thứ ta muốn đo. Ranh giới này (Nguyên tắc 3.1) là cột sống chống rò rỉ của toàn bộ thiết kế.

Cũng cần thành thật ngay: **VH không hoàn hảo.** Nhiều nút chỉ có biểu tượng, không có nhãn chữ, nên VH đành ghi một nhãn chung chung ("Image", "Button") hoặc bỏ trống. Nghiên cứu của Chen và cộng sự (ICSE 2020, Distinguished Paper) đo được **hơn 77% ứng dụng có nút thiếu nhãn dùng được**. Vì thế ta không đối xử VH như chân lý tuyệt đối; ta đo *độ phủ nhãn* của VH và loại các nút nhãn chung ra khỏi mẫu số khi tính toán (§5.1, §7.3). Cách xử lý trung thực này là một phần của tính hợp lệ, không phải điểm yếu bị che giấu.

## 2.3. Bảng thuật ngữ rút gọn (đầy đủ ở Phụ lục A)

Bảng dưới là *bản đồ nhanh* để đọc tiếp không vấp; mỗi mục sẽ được định nghĩa kỹ đúng chỗ nó xuất hiện.

| Thuật ngữ | Nghĩa một dòng |
|---|---|
| Embedding / vector nghĩa | biến một chữ thành dãy số để so được *nghĩa* thay vì so mặt chữ |
| Độ tương đồng (similarity) | một số trong khoảng 0→1 đo hai chữ gần nghĩa cỡ nào |
| Ngưỡng τ | lằn ranh quyết "cùng nút" hay "ảo giác" |
| Fallback | thay bước ảo giác bằng mô tả khái quát, không đoán nút khác |
| Copeland | cách xếp hạng bằng cách đếm số "trận thắng" từng đối tượng |
| τ thứ tự bộ phận | điểm đo sắp đúng thứ tự, chỉ phạt những cặp *bắt buộc* phải đúng |
| Step-SR | tỉ lệ bước hệ làm đúng so với quỹ đạo vàng |
| Perturbation | cố ý bơm lỗi đã biết vào để kiểm tra thước đo có nhạy không |
| Circularity | bẫy logic "vừa ra đề vừa chấm" khiến điểm số vô nghĩa |
| Data leakage (rò rỉ) | để lộ đáp án cho mô hình ở thì sinh, làm hỏng phép đo |

---

# CHƯƠNG 3 — DỮ LIỆU

> **Bản CHI TIẾT CHUẨN LUẬN VĂN của chương này nằm ở `report/44`** (nguồn gốc, tên venue, quy mô, giấy phép, cấu trúc trường dữ liệu, ví dụ thật, hạn chế — mọi số liệu đã được kiểm tra tận file *và* đối chiếu qua web). Dưới đây là bản trình bày mạch lạc đủ để hiểu và bảo vệ.

**Hình dung nhanh — ba bộ, ba vai (đọc cái này trước là nắm cả chương).** Luận văn cần trả lời ba câu hỏi khác nhau, nên cần ba bộ dữ liệu khác nhau, mỗi bộ như một "phòng thí nghiệm" riêng:
- **MobileViews** = *"AI có bịa nút không?"* — mỗi mẫu là **một ảnh màn + danh sách nút thật** của màn đó. Có danh sách nút thật để đối chiếu → đo được bịa. (Nhánh MỘT màn.)
- **AndroidControl** = *"AI có sắp đúng thứ tự + làm đúng thao tác không?"* — mỗi mẫu là **một quy trình nhiều bước do người thật làm**, kèm *chuỗi thao tác đúng* (quỹ đạo vàng). Có chuỗi đúng → đo được thứ tự & từng bước. (Nhánh NHIỀU màn.)
- **ScreenSpot-v2** = *"AI có chỉ đúng chỗ bấm không?"* — mỗi mẫu là **một mô tả nút + khung pixel chuẩn**. Dùng làm **đối chứng** cho thước "bấm đúng chỗ", và bù uy tín cho MobileViews (vì MobileViews là bản thảo chưa bình duyệt).

Việc chọn dữ liệu ở đây không tuỳ tiện: mỗi bộ được chọn để **lấp đúng một lỗ hổng** của thiết kế đánh giá không gold. Ta dùng **ba bộ dữ liệu công khai**, mỗi bộ giữ **một vai cố định**. Trước hết cần hai khái niệm nền mà cả ba bộ xoay quanh:

- **Bảng kê nút (chính là VH, Định nghĩa 2.1):** danh sách nút *thật* của một màn — đây là mỏ neo thay cho đáp án ở nhánh một màn.
- **Quỹ đạo vàng (gold trajectory):** với một tác vụ nhiều bước, đây là chuỗi thao tác *đúng chuẩn* đã có sẵn trong dataset — mỏ neo cho nhánh nhiều màn.

> **Định nghĩa 3.1 (Quỹ đạo vàng).** $G = (a_1, a_2, \dots, a_n)$, trong đó mỗi $a_i$ là một thao tác chuẩn gồm *loại* thao tác và *tham số*. Ví dụ $a_i = \text{click}(x, y)$ (chạm vào toạ độ $(x,y)$) hoặc $a_i = \text{scroll}(\text{down})$ (cuộn xuống). Quỹ đạo vàng do *người thật thực hiện tác vụ* và được ghi lại, nên nó đáng tin làm mốc.

> **Trục phân định hai nhánh** chính là câu hỏi: *"có quỹ đạo vàng để chấm hay không?"*. Nhánh một màn — **không** có quỹ đạo vàng, chỉ có bảng kê nút — nên chỉ đo được *mức không ảo giác*. Nhánh nhiều màn — **có** quỹ đạo vàng — nên đo được cả *đúng thứ tự* lẫn *làm tới đích*. Hiểu trục này là hiểu vì sao đóng góp (A) cần nhánh nhiều màn để chứng minh "năng lực thật", chứ không chỉ "không bịa".

> **CHỐT MẪU 3 BỘ (2026-07-06 — item cụ thể sẽ chạy; chi tiết + debate: `report/48_dataset_selection.md`).**
>
> | Bộ | Vai | Mẫu đã chốt (trong tay) | Artifact |
> |---|---|---|---|
> | **MobileViews** | một màn / faithfulness | **127 màn / 30 app** (mean 4,2 màn/app) | `kept_screens_final.json` |
> | **ScreenSpot-v2** | đối chứng grounding | **501 mobile** (290 text / 211 icon; iOS 238/Android 211/shop 52) | `screenspot_mobile_v2.json` |
> | **AndroidControl** | nhiều màn / τ + Step-SR | **286 ep** N∈{4,5,6} + **48 ep** N∈{7–10}; **237 app** | `dg2_episodes.json` (+`_Nlong`) |
>
> Nguồn AndroidControl = `smolagents/android-control` split test (community re-split; **zero-shot nên vô hại leakage**). Chọn mẫu **tối đa hoá đa dạng app** → estimand = **macro-average mỗi app một phiếu** (KHÔNG "đại diện app nói chung"). Tổng ~$2 API cho toàn bộ định lượng.

## 3.1. MobileViews — bộ cho phần MỘT MÀN

**Mô tả.** MobileViews là một kho lớn gồm các cặp *(ảnh một màn Android; VH của chính màn đó)*. Bản công bố nêu quy mô cỡ **1,2 triệu** cặp (bản công khai thực tế cỡ **600 nghìn**). Bộ này **không** có quỹ đạo vàng — mỗi mẫu chỉ là một màn tĩnh — nên nó hợp cho nhánh một màn. **Trạng thái xuất bản:** tiền ấn phẩm (preprint arXiv 2409.14337; bản v3 đổi tên thành "Million-scale"), do BUPT + Tsinghua thực hiện, **giấy phép MIT**, thu thập **tự động bằng bot** (VLM điều khiển DroidBot dò ứng dụng). Việc nó là preprint và thu thập tự động là lý do ta dùng thêm ScreenSpot-v2 (đã bình duyệt) để bù độ tin cậy (§3.3).

**Cấu trúc một mẫu thật.** Mỗi màn gồm một ảnh `.jpg` và một file `.viewhierarchy.json`. File JSON chứa: `width`, `height` (kích thước ảnh), `foreground_activity` (app/màn đang mở), và một danh sách `views`; mỗi phần tử có trường `class` (loại) và `bounds` lồng dạng `[[x1,y1],[x2,y2]]`. Để bạn đọc hình dung cụ thể, dưới đây là trích *thật* từ màn `ccpacerandroidapp_s1` (một app mạng xã hội cho người chạy bộ) — màn này có **127 phần tử**, ta lấy vài nút bấm được:

<p align="center">
  <img src="../dataset_samples/mv_multiapp/ccpacerandroidapp_s1.jpg" width="250" alt="Màn ccpacerandroidapp_s1 — app Pacer, tab Following/Popular/Groups">
</p>

> **Hình 3.1 — Ảnh thật `ccpacerandroidapp_s1` (MobileViews).** Thấy rõ thanh tab **Following / Popular / Groups** ở đầu màn — chính là ba dòng đầu của bảng VH bên dưới. Đồng hồ **5:33** và biểu tượng pin/khoá ở status bar là ví dụ điển hình của **tín hiệu rò rỉ** mà cổng KB phải che khi xáo trộn nhiều màn (§3.2, §7.5).

| Nhãn $\ell$ | Loại | Bấm được | Khung $(l,t,r,b)$ |
|---|---|---|---|
| Following | TextView | ✓ | (113, 216, 310, 336) |
| Popular | TextView | ✓ | (432, 216, 647, 336) |
| Groups | TextView | ✓ | (794, 216, 942, 336) |
| Find My Friends | Button | ✓ | (0, 1420, −120, 1516) |
| **Image** | ImageView | ✓ | (30, 102, 114, 186) |

> **Quan sát then chốt (dòng cuối bảng).** Nút "Image" là một **nút chỉ có biểu tượng, không có nhãn chữ**; VH đành gán cho nó nhãn chung "Image". Đây chính là hiện thân sống động của con số *hơn 77% ứng dụng có nút thiếu nhãn* (Chen, ICSE 2020). Hệ quả trực tiếp lên phép đo: giả sử AI mô tả **đúng chức năng** nút này, bộ khớp của ta vẫn sẽ coi là *ảo giác oan* — vì không có nhãn chữ nào để đối chiếu. Để không bị con số này bóp méo, luận văn **loại các nút nhãn chung ra khỏi mẫu số** khi tính độ trung thực, và luôn báo cáo kết quả kèm điều kiện *độ phủ nhãn của VH* (§5.1, §7.3). Nói cách khác: ta thừa nhận thẳng giới hạn của mốc, thay vì giả vờ mốc là hoàn hảo.

**Quy mô sử dụng trong luận văn.** Bộ đã curated (lọc màn hỏng/trùng) hiện là **127 màn / 30 app** (`harness/kept_screens_final.json`, chốt 2026-07-06) — phân bố **mean 4,2 màn/app** (range 1–8). *(Mốc pilot 2026-07-01 trước đây là 81 màn/17 app — nay đã mở rộng thêm 13 app.)* Việc có **30 app** là điều kiện để ước lượng sai số theo **cụm app** với G=30 — các màn cùng một app không độc lập thống kê với nhau (§7.4).

> **Điều kiện chốt trước khi in (từ `report/44` §8):** MobileViews có **lệch khung toạ độ** giữa ảnh và VH (width/height không khớp trực tiếp) — phải **hiệu chỉnh khung toạ độ trước khi tính bất kỳ thước grounding nào**, nếu không mọi phép "điểm bấm có trong khung không" đều sai lệch hệ thống.

## 3.2. AndroidControl — bộ cho phần NHIỀU MÀN

**Mô tả.** AndroidControl là bộ dữ liệu *đã bình duyệt* — công bố tại **NeurIPS 2024 Datasets & Benchmarks** (Li et al., Google DeepMind; bài "On the Effects of Data Scale on UI Control Agents", arXiv 2406.03679; **giấy phép CC0**). Điểm quý của nó là dữ liệu **người thật**: người dùng thao tác trên điện thoại Pixel suốt khoảng một năm, mọi bước được ghi lại. Bộ gồm **15.283** quy trình nhiều bước, trải **833** app, trung bình **~5,5** bước mỗi quy trình (percentile-95 = 13 bước). Mỗi quy trình có một **mục tiêu** (câu mô tả tác vụ) và một **quỹ đạo vàng** (chuỗi thao tác đúng), với 8 loại thao tác. Nhờ có quỹ đạo vàng, đây là bộ để đo nhánh nhiều màn: đo *sắp đúng thứ tự* ($\tau$) và *làm tới đích* (Step-SR).

**Một quy trình thật (`ep2_14851`).** Để không nói suông, đây là một quy trình lấy nguyên từ dataset:

> **Mục tiêu:** *"Create a shortcut for me of The Queen's Gambit pdf file to the home screen on the Drive app."* (Tạo lối tắt cho file PDF "The Queen's Gambit" ra màn hình chính, trong app Drive.)

Quỹ đạo vàng $G$ của quy trình này gồm 5 thao tác:

| $i$ | $a_i$ (thao tác vàng) | Diễn giải bằng lời |
|---|---|---|
| 1 | `click(1016, 866)` | chạm nút "⋮" (thêm tuỳ chọn) cạnh file |
| 2 | `scroll(down)` | cuộn danh sách tuỳ chọn xuống |
| 3 | `click(602, 2105)` | chọn "Add to Home screen" |
| 4 | `click(821, 2252)` | xác nhận "Add automatically" |
| 5 | `status(successful)` | báo tác vụ hoàn tất |

<p align="center">
  <img src="../dataset_samples/androidcontrol/ep2_14851_step1.png" width="150" alt="Drive - danh sách file">
  <img src="../dataset_samples/androidcontrol/ep2_14851_step2.png" width="150" alt="menu tuỳ chọn">
  <img src="../dataset_samples/androidcontrol/ep2_14851_step3.png" width="150" alt="Add to Home screen">
  <img src="../dataset_samples/androidcontrol/ep2_14851_step4.png" width="150" alt="Add automatically">
  <img src="../dataset_samples/androidcontrol/ep2_14851_step5.png" width="150" alt="hoàn tất">
</p>

> **Hình 3.2 — Năm màn thật của quy trình `ep2_14851`** (Google Drive, tạo lối tắt PDF "The Queen's Gambit"), theo đúng thứ tự quỹ đạo vàng ở bảng trên. Ở **màn 1**, nút "⋮" cạnh file nằm đúng toạ độ gold `click(1016, 866)` (đã đối chiếu ảnh). Status bar hiện đồng hồ **11:47** và huy hiệu thông báo Snapchat — lại là **tín hiệu rò rỉ thứ tự** phải che (cổng KB, §7.5). Trong thực nghiệm nhiều màn, năm ảnh này được **xáo trộn** rồi buộc hệ tự khôi phục trình tự.

**Cách sử dụng (thiết kế thực nghiệm).** Ta lấy các màn của một quy trình, **xáo trộn thứ tự**, rồi buộc hệ tự khôi phục (chấm bằng $\tau$, §5.2). Sau đó ta so từng thao tác hệ đề xuất với quỹ đạo vàng (chấm bằng Step-SR). Điều tinh tế: khi xáo trộn màn, ta phải **che mọi tín hiệu rò rỉ thứ tự** — đồng hồ, mức pin, chỉ số bước, huy hiệu thông báo — nếu không, hệ có thể "đoán" thứ tự nhờ đồng hồ nhảy số chứ không phải nhờ hiểu quy trình. Đây là cổng chống rò rỉ **KB** (§7).

> **Đính chính số liệu bắt buộc (cập nhật từ `report/48` §7):** **không** in "2.855" như kích thước tập test. Tập test chính thức gồm **4 sub-split chồng nhau** (IDD + app-unseen + task-unseen + category-unseen; paper ghi rõ "may overlap"), **tổng 2.855**; số quy trình **duy nhất sau khử trùng ≈ 1.540** (Li et al., NeurIPS 2024 D&B). Cách khai an toàn: *"tập test gồm 4 sub-split chồng nhau tổng 2.855, số duy nhất sau khử trùng ≈1.540; 286 = mẫu phân tầng con."* — **không** in "1.542" như trích nguyên văn (chênh 2 quy trình so với ≈1.540, cần đếm tay `episode_id` duy nhất trước khi in). Nguồn ta dùng là bản chia lại `smolagents/android-control` (test=3.051), khai rõ provenance; vô hại leakage vì luận văn zero-shot.

> **Cổng cứng KN:** dataset chỉ công bố thống kê tổng (mean, p95), **chưa** có phân bố số quy trình theo từng độ dài $N$. Ta **phải tự đếm histogram độ dài quy trình** trước khi chốt thiết kế nhiều màn — nếu quá ít quy trình dài, các claim về "nhiều màn" phải thu hẹp tương ứng.

## 3.3. ScreenSpot-v2 — bộ ĐỐI CHỨNG

**Mô tả.** ScreenSpot-v2 là chuẩn cho tác vụ *"định vị nút từ mô tả"* (grounding): cho một câu mô tả, hãy chỉ ra khung pixel của nút tương ứng trên ảnh. Bộ này **đã bình duyệt** — đi kèm OS-Atlas tại **ICLR 2025** (gốc từ SeeClick, ACL 2024; **giấy phép apache-2.0**), gồm **1.272** chỉ dẫn (502 mobile / 334 desktop / 436 web), đã sửa 11,32% lỗi nhãn của bản gốc. Bbox dạng `[x1,y1,x2,y2]`.

**Một item thật (`item1`):**

> **Câu lệnh:** *"invert the lens"* · **Loại phần tử:** icon · **Kích thước ảnh:** 1170×2532 · **Đáp án (khung pixel):** **(965, 2105, 1110, 2258)**.

<p align="center">
  <img src="../dataset_samples/screenspot/item1.png" width="250" alt="ScreenSpot item1 — app Camera, nút lật ống kính">
</p>

> **Hình 3.3 — Ảnh thật ScreenSpot `item1`** (app Camera iPhone, 1170×2532). Câu lệnh *"invert the lens"* trỏ tới **nút lật camera trước/sau** ở góc **dưới phải** — đúng khung chuẩn (965, 2105, 1110, 2258). Đây là dạng "định vị nút từ mô tả": ta dùng nó để **đối chứng bộ trỏ độc lập** (§5.3), thay vì lấy tâm khung nút đã khớp (sẽ thành tautology).

**Vai của nó.** ScreenSpot-v2 là **đối chứng độc lập cho thước "bấm đúng chỗ"** (grounding). Vì nó có *đáp án toạ độ chuẩn* và *đã bình duyệt*, ta dùng nó để kiểm tra **bộ trỏ toạ độ** một cách công bằng — thay vì lấy tâm khung nút đã khớp làm điểm bấm (điều đó sẽ tạo tautology, luôn đúng 100%; xem §5.1). Nó cũng bù đắp độ tin cậy cho MobileViews (vốn là preprint thu thập tự động).

## 3.4. Luật vàng chống rò rỉ (nhắc lại, vì nó là cột sống)

> **Nguyên tắc 3.1 (Luật vàng chống rò rỉ).** VH và quỹ đạo vàng **chỉ tham gia ở thì CHẤM**, tuyệt đối **không** được cung cấp cho mô hình ở thì sinh hoặc thì sắp thứ tự. Câu hỏi $q$ không chứa tên nút.
>
> **Diễn giải bằng ẩn dụ.** Việc này giống như *không cho thí sinh xem đáp án trong lúc làm bài*. Nếu lộ đáp án, thí sinh (mô hình) chỉ việc chép, và ta hoàn toàn mất khả năng đo **mức độ nó tự ảo giác** — mà đó chính là đại lượng ta cần đo. Việc để lộ đáp án cho mô hình ở thì sinh gọi là **rò rỉ dữ liệu (data leakage)**, và nó là nguyên nhân số một khiến các con số đánh giá trông đẹp mà vô nghĩa.
>
> **Một hệ quả thường bị hiểu nhầm:** "chấm baseline bằng VH" **là một bước đánh giá**, không phải một bước trong hệ khi triển khai thật. Khi *deploy*, hệ chỉ làm ba việc: sinh → kiểm → né ảo giác; nó **không** cần VH lúc sinh. VH chỉ xuất hiện trong phòng thí nghiệm khi ta *đo* chất lượng.

---

# CHƯƠNG 4 — PHƯƠNG PHÁP I: HỆ THỐNG SINH

> ⚠️ **[MỘT PHẦN LỖI THỜI — khung cũ prompting]** Các cơ chế trong chương (sắp thứ tự Stage-0 · đối chiếu–né bịa) **VẪN là THÀNH PHẦN** của hệ mới. NHƯNG cách đóng khung "hệ prompting = đóng góp, không train model" đã bị thay: đóng góp giờ là **mô hình grounding tự train** (**Chương 0**). → Đọc chương này để hiểu *cơ chế từng bước*, KHÔNG phải để hiểu *đâu là đóng góp*.

> **PIPELINE CHỐT — nhìn một trang là nắm.**
> Một hệ duy nhất, một **bộ định tuyến theo số ảnh**. Với **một màn** ($N = 1$), chạy ba bước nối tiếp:
>
> 1. **VLM sinh mù** — chỉ thấy ảnh + câu hỏi, *không* thấy danh sách nút.
> 2. **Thuật toán so embedding** — đối chiếu từng tên nút với cây phân cấp giao diện (khớp nếu tương đồng $\ge \tau$; ngược lại là *ảo giác*).
> 3. **Fallback** — bước ảo giác được viết lại thành mô tả bằng lời, *không đoán nút khác*.
>
> Với **nhiều màn** ($N \ge 2$, ảnh đã xáo trộn), thêm **Stage-0** ở đầu:
>
> > **so cặp → tổng hợp Copeland → phá vòng bằng min-feedback-arc-set** → chuỗi đã sắp rồi cho từng màn chạy tiếp qua ba bước trên.
>
> Toàn bộ **không** dùng cây giao diện / quỹ đạo vàng ở thì sinh (luật vàng chống rò rỉ, §3.4). Đây là bản đã chốt sau deep-research 2026; các mục §4.2–§4.4 giải thích tận gốc từng khối.

## 4.1. Tổng quan: một hệ duy nhất, bộ định tuyến theo số ảnh

Điểm thiết kế cần nhấn: **không có hai hệ thống rời rạc.** Chỉ có *một* hệ, với một **bộ định tuyến theo số ảnh** ở đầu vào. Nếu $N=1$, đầu vào đi thẳng vào **nhánh một màn**. Nếu $N \ge 2$, đầu vào đi qua thêm một **Stage-0** (bước sắp lại thứ tự các màn) để khôi phục trình tự, rồi *từng màn đã sắp* lại chạy qua đúng nhánh một màn ấy. Trường hợp $N=1$ chỉ là trường hợp riêng khi Stage-0 rỗng. Nhờ vậy nhánh nhiều màn **kế thừa nguyên vẹn** nhánh một màn — không phải viết lại logic sinh.

```
Đầu vào (S, q)
   │
   ├─ N = 1 ─────────────────────────────► [Nhánh một màn]
   │
   └─ N ≥ 2 ► [Stage-0: sắp thứ tự màn] ► chuỗi đã sắp ► [Nhánh một màn] lặp cho từng màn
```

Cách tổ chức này cũng làm rõ điều gì là *mới*: nhánh một màn đóng góp **bước đối chiếu với giao diện thật**; Stage-0 đóng góp **bước sắp lại thứ tự các màn** với năm tín hiệu và cơ chế phá vòng. Cả hai hợp lại thành hệ thống (A).

## 4.2. Nhánh một màn (ba bước)

Nhánh này là trái tim của đóng góp (A). Nó gồm ba bước nối tiếp: **sinh mù → đối chiếu ngữ nghĩa → né ảo giác**.

### Bước 1 — Sinh mù (blind generation)

VLM nhận đầu vào là *(ảnh, câu hỏi)* và **không** nhận VH. Nó sinh ra một bản nháp $T^{(0)}$ — ta gọi là *baseline*. Chữ "mù" ở đây có nghĩa **mù danh sách nút**: mô hình phải tự đọc ảnh để đoán màn có gì, thay vì được đưa sẵn. Chính vì mù mà nó *có cơ hội ảo giác* — và đó là điều ta muốn đo, không phải muốn tránh né ở bước này. (Câu hỏi cũng không chứa tên nút, đúng theo Định nghĩa 1.2 và Nguyên tắc 3.1.)

### Bước 2 — Đối chiếu ngữ nghĩa (semantic matching)

Với mỗi bước $t_i$ trong bản nháp có nhắc tới một nút tên $b_i$, ta kiểm tra: *nút này có thật trên màn không?* Câu trả lời không thể dựa vào so khớp mặt chữ (vì "Lưu" và "Save" khác mặt chữ nhưng cùng nghĩa), nên ta so *nghĩa* bằng embedding.

> **Định nghĩa 4.1 (khớp / ảo giác).** Cho một hàm embedding $\phi(\cdot)$ và độ tương đồng cosine $\text{sim}(u, v)$. Bước $t_i$ được coi là **khớp** (nút có thật) nếu
> $$\max_{e \in \text{VH}(s)} \text{sim}\big(\phi(b_i),\, \phi(\ell_e)\big) \ge \tau,$$
> tức tồn tại ít nhất một nút thật $e$ trên màn mà tên của nó $\ell_e$ gần nghĩa với $b_i$ ở mức vượt ngưỡng $\tau$. Ngược lại, nếu nút gần nhất vẫn dưới ngưỡng, $t_i$ bị coi là **ảo giác**.

**Giải thích embedding cho người mới.** Hàm $\phi$ biến một chữ thành một **dãy số** (vài trăm chiều), được huấn luyện sao cho các chữ *cùng nghĩa* cho ra dãy số *gần nhau* trong không gian đó. Hàm $\text{sim}$ đo độ gần ấy và trả về một số trong khoảng **0→1**. Vài ví dụ trực giác:

- $\text{sim}\big(\phi(\text{"Save"}),\, \phi(\text{"Lưu"})\big) \approx 0{,}7$ — cùng nghĩa, điểm cao.
- $\text{sim}\big(\phi(\text{"Menu"}),\, \phi(\text{"Save"})\big) \le 0{,}3$ — khác nghĩa, điểm thấp.

Ngưỡng $\tau = 0{,}55$ đóng vai "lằn ranh": từ $\tau$ trở lên coi là *cùng nút*, dưới $\tau$ coi là *ảo giác*. **Lưu ý về tính độc lập:** embedding dùng để *quyết* khớp/ảo giác là `nomic-embed-text`; còn embedding dùng để *chấm điểm* (Chương 5, 7) là `bge-m3` — **họ khác nhau** — để không rơi vào bẫy "dùng chính công cụ ra quyết định để tự chấm mình" (Chương 7).

> Nhấn mạnh: bước 2 là **thuật toán so embedding**, *không phải* một lời gọi LLM khác. Đây là một phép tính xác định, kiểm chứng được, không thêm một tầng "AI đoán AI".

### Bước 3 — Né ảo giác bằng fallback (không đoán nút khác)

Với mỗi bước bị bước 2 gắn cờ *ảo giác*, ta **không** cố sửa nó thành một nút cụ thể. Ta thay bằng một **mô tả khái quát**:

> `Bấm "Menu"` (ảo giác) → `Tìm và bấm nút phù hợp để mở thêm tuỳ chọn` (fallback)

**Vì sao không đoán nút gần nhất?** Đây là quyết định thiết kế cốt lõi, và nó có *cơ sở thực nghiệm* (xem "Định lý thiết kế" bên dưới). Phương án hấp dẫn là: nếu "Menu" không có, hãy tra VH tìm nút gần nghĩa nhất rồi thay vào. Nhưng phương án đó tạo ra **lỗi âm thầm** — nó thay bằng một nút *có thật nhưng sai chức năng*, khiến hướng dẫn trông đúng mà dẫn người dùng bấm nhầm, và cái sai bị *che giấu* thay vì lộ ra. Đây gọi là phương án PA2 (chỉ *matched / fallback*), thay hẳn cho phương án "correction" cũ đã bị loại bỏ.

**Ví dụ chạy trọn ba bước (nối lý thuyết lại một mạch).** Đầu vào: ảnh một màn đặt giờ + câu hỏi *"Cần làm gì để đặt 20:35 rồi xác nhận?"*. Danh sách nút thật của màn (VH): {hour, minute, AM, PM, OK, Cancel}.

| | Nội dung | Diễn ra gì |
|---|---|---|
| **Bước 1 (sinh mù)** | VLM trả về bản nháp: ① "Chọn giờ và phút" ② "Chọn **PM**" ③ "Bấm **Menu**" | VLM tự đọc ảnh, tự viết — *không thấy VH* |
| **Bước 2 (đối chiếu)** | ①→ khớp *hour/minute* (sim 0,85 ≥ 0,55) ✓ · ②→ khớp *PM* (sim 1,0) ✓ · ③"Menu"→ nút gần nhất *OK* chỉ sim 0,30 < 0,55 → **ảo giác** | so nghĩa từng tên nút với VH |
| **Bước 3 (fallback)** | Bước ③ viết lại: "Bấm **Menu**" → *"Tìm và bấm nút phù hợp để mở thêm tuỳ chọn"* | *không* đoán "OK"; chỉ mô tả |

Kết quả: bản cuối gồm ①②③', trong đó ③' là mô tả chung thay vì tham chiếu bịa. *Chấm:* độ trung thực bản gốc $= 1 - \tfrac13 \approx 67\%$ (§5.1); tỉ lệ fallback $= 1/3$. **Đây là toàn bộ nhánh một màn chạy end-to-end.**

**Mã giả (nhánh một màn đầy đủ):**
```
HÀM SinhMotMan(ảnh s, câu hỏi q):
    T ← VLM_sinh_mù(s, q) # bước 1: baseline, KHÔNG đưa VH
    cho mỗi bước t trong T:
        nếu t nhắc tới nút tên b:
            sim ← max{ cosine(φ(b), φ(ℓ_e)) : e ∈ VH(s) } # bước 2: so nghĩa
            nếu sim < τ: # phát hiện ảo giác
                t ← "Tìm và bấm nút phù hợp để …" # bước 3: fallback (KHÔNG đoán nút khác)
    trả về T
```

> **Định lý thiết kế (đối chứng thất bại đo được).** Phương án thay bước ảo giác bằng **nút thật gần nhất** tạo ra **lỗi âm thầm (silent error)** — đo được trực tiếp trên 10 màn thử nghiệm. Ví dụ cụ thể quan sát được: `✓ → Navigate up`, `+ → More options`, `ADD LOCATION → Copy project`. Trong mỗi trường hợp, hệ thay một tham chiếu bịa bằng một nút *có tồn tại nhưng sai chức năng*; người dùng làm theo sẽ bấm nhầm mà không hề hay biết. Chính phát hiện này buộc ta chốt "chỉ mô tả, không đoán". **Đây là một phát hiện thực nghiệm, và nó là cơ sở khoa học nâng đóng góp (A) từ 'kỹ thuật' lên 'nghiên cứu':** ta thử một phương án hợp lý, đo được nó thất bại theo một cách cụ thể (silent error), và rút ra một nguyên tắc thiết kế có bằng chứng.

## 4.3. Nhánh nhiều màn (Stage-0: sắp thứ tự màn)

Khi có $N \ge 2$ ảnh xáo trộn, Stage-0 khôi phục thứ tự qua ba bước con: **so cặp → tổng hợp Copeland → phá vòng mâu thuẫn**. Sau khi có chuỗi đã sắp, từng màn chạy qua nhánh một màn ở §4.2.

### (a) So cặp (pairwise comparison)

Với $\binom{N}{2}$ cặp màn, ta hỏi VLM từng cặp một: *"trong hai màn này, màn nào đến trước?"* (ví dụ $N=4$ → $\binom{4}{2}=6$ câu hỏi; $N=5$ → 10 câu hỏi). Ta cố ý **KHÔNG** đưa cả $N$ màn vào một lần rồi bảo VLM "sắp hết đi" (cách đó gọi là *listwise*). Nền peer-reviewed: pairwise ranking — Qin, Findings NAACL 2024.

> **Vì sao hỏi từng CẶP thay vì bảo model sắp cả dãy một lần? — ba lý do, đều có neo khoa học:**
> 1. **Hợp "chế độ" của ta (luận điểm mạnh nhất).** Qin et al. (Findings NAACL 2024) chứng minh: *với model tầm trung*, hỏi so cặp cho xếp hạng tốt hơn hẳn bảo model sắp cả dãy. Trực giác: phán "A hay B trước" là bài toán *nhỏ, tập trung*; sắp 5 màn cùng lúc là bài toán *nặng*, dễ loạn. VLM của ta đúng là tầm trung (`gpt-4o-mini`) và số màn ít (trung bình ~5,5) → rơi đúng vùng so cặp thắng.
> 2. **Để lại "dấu vết kiểm tra được".** Mỗi phán đoán cặp là một mẩu rời, soi được từng cái đúng/sai so với gold. Bảo model xuất thẳng một dãy thì nó là *hộp đen* — sai chỗ nào cũng không biết. Dấu vết này chính là thứ cho phép **bắt mâu thuẫn nội tại** (bước c) và **phân tích tín hiệu** ("Năm tín hiệu thứ tự" bên dưới).
> 3. **Cho phép phát hiện *mâu thuẫn nội tại*** (kiểu "A trước B, B trước C, nhưng C lại trước A") — điều mà một dãy xuất thẳng che mất hoàn toàn (xem bước c).

> **Khai thẳng (không overclaim):** so cặp chính xác hơn listwise *ở model tầm trung* (Qin) — đúng chế độ của ta (VLM tầm trung, ít màn: mean ~5,5; p95 = 13). Trên model rất mạnh thì listwise một shot (RankGPT) có thể ngang hoặc hơn. Vì vậy ta **không** claim so cặp *luôn* tốt hơn; ta chọn nó vì hợp chế độ + cho dấu vết kiểm, và **thêm baseline listwise một shot** (RankGPT-style) chấm cùng $\tau$/Step-SR/chi phí để so thẳng (§4.4).

### (b) Tổng hợp Copeland — biến "một đống phán đoán cặp" thành MỘT hàng thứ tự

Sau bước (a) ta có một **đống phán đoán rời rạc**: "màn này trước màn kia", "màn kia trước màn nọ"… nhưng chúng **chưa thành một hàng**. Việc của bước (b) là gộp tất cả lại thành **một thứ tự duy nhất từ đầu đến cuối**. Ta dùng **phương pháp Copeland**.

**Ẩn dụ dễ hình dung — giải đấu vòng tròn (round-robin).** Hãy tưởng tượng mỗi màn hình là một *đội bóng*, và mỗi câu hỏi so cặp ở bước (a) là một *trận đấu* giữa hai đội. "Đội thắng" = màn được VLM cho là **đứng trước**. Cuối giải, ta **đếm số trận mỗi đội thắng**: đội thắng nhiều nhất xếp đầu bảng, ít nhất xếp cuối. Đó chính xác là Copeland — không có gì bí ẩn, chỉ là **đếm số lần "đứng trước"**.

> **Định nghĩa 4.2 (điểm Copeland).** Với mỗi màn $s$, **điểm Copeland** của nó là *số màn khác mà $s$ được đánh giá là đứng trước*:
> $$\text{cop}(s) = \text{số màn } s' \text{ sao cho VLM phán "} s \text{ đứng trước } s'\text{"}.$$
> Sau đó **sắp các màn theo điểm Copeland từ cao xuống thấp** → đó là thứ tự khôi phục. Nếu hai màn *bằng điểm* (hoà), ta phá hoà bằng một quy tắc **cố định, tái lập được** (ví dụ: xét trực tiếp trận giữa hai màn đó).

**Ví dụ chạy đầy đủ — 4 màn "bật thông báo".** Giả sử một quy trình có 4 màn, thứ tự đúng (gold) là:
> **A** (màn Cài đặt chính) → **B** (màn Thông báo) → **C** (bật công tắc thông báo của app) → **D** (màn xác nhận đã bật).

Ta đưa 4 màn này vào **đã xáo trộn**, và hỏi VLM cả $\binom{4}{2} = 6$ cặp. Giả sử VLM trả lời (ở đây trả lời đúng hết):

| Cặp hỏi | VLM phán "đứng trước" |
|---|---|
| A vs B | **A** |
| A vs C | **A** |
| A vs D | **A** |
| B vs C | **B** |
| B vs D | **B** |
| C vs D | **C** |

Giờ **đếm số trận thắng** cho từng màn:
- **A** đứng trước B, C, D → **cop(A) = 3**
- **B** đứng trước C, D → **cop(B) = 2**
- **C** đứng trước D → **cop(C) = 1**
- **D** không đứng trước ai → **cop(D) = 0**

Sắp theo điểm giảm dần: **A (3) → B (2) → C (1) → D (0)** → **đúng bằng thứ tự gold**. Đó là cách Stage-0 "sắp lại" các màn.

> **Nếu hai (hay nhiều) màn BẰNG ĐIỂM Copeland thì sao? — có HAI tình huống, đừng lẫn:**
>
> **Tình huống 1 — hoà "lành" (các phán đoán vẫn nhất quán, không có vòng).** Ví dụ hai màn bằng điểm nhưng giữa chúng có một trận trực tiếp rõ ràng. → **Phá hoà bằng trận đối đầu trực tiếp (head-to-head):** xét đúng cái cặp giữa hai màn đó, ai được phán "đứng trước" trong trận trực tiếp thì xếp trên. Quy tắc này **cố định, tái lập được** (chạy lại ra y hệt), nên không tuỳ tiện.
>
> **Tình huống 2 — hoà "do vòng cắn đuôi".** Ví dụ 3 màn: A trước B, B trước C, **nhưng C lại trước A** → đếm điểm thì **cả ba đều = 1** (hoà cả ba), và head-to-head cũng **vô dụng** (A thắng B, B thắng C, C thắng A — xét trận trực tiếp vẫn quay vòng). Lúc này Copeland **bó tay** → phải chuyển sang **bước (c) phá vòng**.
>
> Chính vì Copeland *để lộ ra* tình huống 2 (hoà mà head-to-head không gỡ được) mà ta **phát hiện được mâu thuẫn nội tại** — đó là "dấu vết" mà bước (a) nhắc tới. Một dãy xuất thẳng thì không bao giờ lộ ra điều này.

Nền peer-reviewed: Copeland — Dwork et al., WWW 2001. *Copeland là **một trong nhiều** cách tổng hợp hạng (một chuẩn phổ biến khác là **Bradley-Terry / Elo**, kiểu bảng xếp hạng cờ vua, dùng ở Chatbot Arena). Ta chọn Copeland + phá vòng vì nó **đơn giản, cho kết quả tái lập được, và để lại "dấu vết" giúp bắt mâu thuẫn** (xem bước c) — ta **không** tuyên bố nó là "chuẩn duy nhất", và có so với baseline khác ở §4.4.*

### (c) Phá vòng mâu thuẫn — khi các phán đoán "cắn đuôi nhau"

VLM không phải lúc nào cũng nhất quán. Đôi khi các phán đoán cặp tạo thành một **vòng luẩn quẩn** vô lý, kiểu: *A đứng trước B, B đứng trước C, nhưng C lại đứng trước A*. Vẽ ra thì nó thành một **vòng tròn khép kín** (A → B → C → A) — **không thể xếp thành một hàng thẳng** được, vì cứ đi mãi không có điểm đầu điểm cuối.

**Cách gỡ — cắt ít dây nhất để hết vòng.** Hãy hình dung mỗi phán đoán "X trước Y" là một **sợi dây** nối X đến Y. Khi có vòng luẩn quẩn, ta **cắt bỏ một số sợi dây ít nhất có thể** để phá vòng, sao cho phần còn lại xếp được thành hàng. Bài toán "cắt ít dây nhất để hết vòng" này có tên chính thức trong toán học là **minimum feedback arc set** (tập cạnh phản hồi nhỏ nhất) — Ailon et al., JACM 2008.

> **Ví dụ chạy — một vòng luẩn quẩn 3 màn.** Giả sử VLM phán:
> - A vs B → **A** trước (dây A → B)
> - B vs C → **B** trước (dây B → C)
> - A vs C → **C** trước (dây C → A) ← *đây là phán đoán gây mâu thuẫn*
>
> Ba dây này tạo thành vòng **A → B → C → A**. Nếu tính điểm Copeland thì cả ba đều thắng đúng 1 trận (cop = 1 cho cả A, B, C) → **hoà cả ba, không sắp được**.
> **Cách phá:** ta cắt **đúng một** dây — dây nào *ít đáng tin nhất*. Giả sử khi hỏi lại cặp (A, C) vài lần, VLM **lúc nói C trước, lúc nói A trước** (không ổn định) → dây "C → A" là **yếu nhất** → cắt nó. Còn lại A → B → C (không còn vòng) → thứ tự khôi phục là **A → B → C**.

**Chọn dây nào để cắt bằng cách nào? (điểm M2, quan trọng)** Câu hỏi mấu chốt là "dây nào ít đáng tin nhất để cắt". Ta **KHÔNG** hỏi VLM "mày chắc bao nhiêu %" rồi cắt dây nó tự nhận là yếu — vì VLM **hiệu chỉnh độ tự tin rất kém** (nó hay tự tin ngay cả khi sai). Thay vào đó, "độ yếu" của một dây được đo bằng ba tín hiệu **khách quan hơn**:
1. **Khoảng cách thắng (margin-Copeland):** trận thắng sát nút thì dây yếu hơn trận thắng áp đảo.
2. **Tính ổn định (self-consistency):** hỏi lại cặp đó nhiều lần — nếu câu trả lời *lật qua lật lại* thì dây yếu.
3. **Cắt ít nhất (min-cardinality):** trong các cách phá vòng, ưu tiên cách cắt **ít dây nhất**.

> *Lựa chọn "đo độ yếu bằng tín hiệu khách quan thay vì hỏi VLM tự khai" này có tiền lệ bình duyệt:* Dodgersort (PAKDD 2026) dùng đúng nguyên lý "trọng số theo độ bất định" cho xếp hạng cặp bằng mô hình thị giác. Ta viện dẫn để biện minh, đồng thời phân định: miền của ta là GUI **tự động hoàn toàn** (Dodgersort có người tham gia lúc sắp). Ta cũng chạy một *ablation* (§4.4, thí nghiệm E11) so cách phá vòng này với cách ngây thơ, để **chứng minh bằng số** rằng nó tốt hơn.

> **Tóm tắt bước (c) trong ba nhịp — đọc dòng này là đủ nắm ý:**
> 1. **Phát hiện vòng.** Các phán đoán cặp cắn đuôi nhau (A→B→C→A) → không duỗi thành hàng thẳng được → phải gỡ.
> 2. **Cắt ít "dây" nhất.** Coi mỗi phán đoán là một sợi dây; cắt *số dây ít nhất có thể* để hết mọi vòng (bài toán *minimum feedback arc set*, Ailon JACM 2008).
> 3. **Cắt dây YẾU nhất — đo bằng tín hiệu khách quan, KHÔNG hỏi model tự khai** (vì VLM tự tin cả khi sai): (i) *khoảng cách thắng* sát nút → dây yếu; (ii) *hỏi lại nhiều lần* mà đảo qua đảo lại → dây yếu; (iii) giữa các cách gỡ, ưu tiên *cắt ít dây nhất*.
>
> **Vì sao không đơn giản là "hỏi VLM chắc mấy % rồi cắt dây nó tự nhận yếu"?** Vì VLM **hiệu chỉnh độ tự tin rất kém** — nó hay tự tin ngay cả khi sai. Tin lời tự khai của model = rơi lại vào bẫy "để hệ tự chấm mình". Nên ta chỉ dùng ba tín hiệu *quan sát được từ ngoài* ở trên.

### Năm tín hiệu thứ tự (5 ordering cues)

Câu hỏi giám khảo tự nhiên là: *"dựa vào đâu mà biết màn nào trước?"*. Ta trả lời bằng cách nêu rõ **năm loại tín hiệu** mà một quy trình GUI thường để lại:

1. **Gating** — màn sau chỉ mở được sau khi hoàn tất một hành động ở màn trước (điều kiện tiên quyết).
2. **Nút điều hướng (nav-affordance)** — sự có mặt của "Next / Back / Tiếp / Quay lại".
3. **Biến thiên trạng thái (state-delta)** — một toggle chuyển bật/tắt, một ô từ trống thành đã điền, một huy hiệu số thay đổi.
4. **Tiêu đề tiến trình (title-progression)** — "Bước 1/3", "Bước 2/3"…
5. **Drill-down** — đi từ màn tổng quan vào màn chi tiết.

> **Năm tín hiệu này lấy ở đâu? Có luận điểm khoa học không? — trả lời trung thực (quan trọng, giám khảo hay hỏi):**
> - Năm tín hiệu **KHÔNG bê nguyên từ một bài báo duy nhất** — chúng là **quan sát/đóng góp của chính luận văn** về "một quy trình GUI thường để lại dấu vết thứ tự ở đâu". Đây là *chỗ mới*, không phải chỗ đi mượn — và đó là điểm mạnh nếu trình bày đúng.
> - **Từng tín hiệu riêng lẻ đều là cơ chế điều hướng chuẩn trong HCI/GUI:** gating (điều kiện tiên quyết), nút Next/Back, drill-down (tổng quan→chi tiết), tiêu đề "Bước 1/3"… — không phải ta bịa, mà mô tả lại thứ ai làm giao diện cũng biết.
> - **Cái mới nằm ở *cách dùng* chúng để phân tích, và chỗ này CÓ trụ khái niệm bình duyệt:** Gardner et al. (Findings EMNLP 2020, *contrast sets*) đặt nguyên lý — muốn biết mô hình *dựa vào tín hiệu nào* thì **cô lập từng tín hiệu** rồi đo. Ta áp đúng: giữ những cặp màn chỉ khác nhau *đúng một* tín hiệu (phân tầng một cue) để đo riêng ảnh hưởng từng loại.
> - Ta **khai thẳng** đây là trụ *khái niệm* chứ không phải tiền lệ trùng khít — vì nếu có bài y hệt thì đây đâu còn là đóng góp mới. Chính chỗ "chưa ai làm khít" này chứng minh phần sắp thứ tự là *nghiên cứu*, không chỉ ghép thư viện.

Khi *phân tích quy kết* (signal-attribution — trả lời "hệ dựa vào tín hiệu nào"), ta dùng **phân tầng một cue (single-cue stratification):** chỉ giữ lại những cặp màn được phân biệt bởi *đúng một* tín hiệu, để cô lập ảnh hưởng của từng loại. Ta **không** che pixel và **không** tin lời mô hình tự khai nó "đã dùng tín hiệu nào" — vì cả hai cách đó đều thiếu tin cậy. Trụ khái niệm cho lối phân tích này: Gardner et al., Findings of EMNLP 2020 (đây là *chỗ đóng góp mới*, nên chỉ có trụ khái niệm chứ chưa có tiền lệ trùng khít — điều này được khai thẳng, không giấu).

> **Cổng cứng K-pair (M2):** trước khi tin vào bất cứ kết quả Copeland nào, ta phải đo **độ chính xác so cặp THÔ của VLM so với gold** — tức tỉ lệ VLM phán đúng "màn nào trước" trên từng cặp riêng lẻ. Nếu con số này chỉ quanh **0,5** (bằng đoán mò), thì toàn bộ Stage-0 vô hiệu về nguyên tắc, và ta phải khai thẳng điều đó thay vì tô vẽ kết quả tổng hợp.

## 4.4. Thừa nhận prior-art & phát biểu độ mới của bước sắp lại thứ tự các màn (chống câu phản biện "chỉ ghép đồ có sẵn")

Deep-research 2026 xác nhận: **từng viên gạch thuật toán của Stage-0 đều đã có sẵn** — pairwise ranking (Qin, Findings NAACL 2024), Copeland (Dwork, WWW 2001), minimum feedback arc set (Ailon, JACM 2008), và gần đây được hình thức hoá lại đúng quy trình "so cặp → min-weighted-FAS" (arXiv 2412.16181, 2025, *preprint*). Cũng đã có tiền lệ **bình duyệt** về "dùng VLM/CLIP so cặp để sắp ảnh": EZ-Sort (CIKM 2025) và Dodgersort (PAKDD 2026). Ta **trích đầy đủ và không giấu** điều này — vì lờ đi mới là chỗ giám khảo bắt "chỉ áp method có sẵn".

> **Độ mới của bước sắp lại thứ tự các màn KHÔNG nằm ở thuật toán lõi**, mà ở **năm điểm ghép lại chưa ai làm cùng lúc**: (1) *miền GUI* thay vì ảnh tổng quát; (2) *điều kiện hoá theo mục tiêu tác vụ* (sắp để phục vụ một câu hỏi, không phải sắp chung chung); (3) *gắn ordering vào sinh hướng dẫn* (đầu ra là chuỗi bước cho người, không phải một bảng xếp hạng); (4) *partial-order suy từ gold* (chỉ phạt cặp bắt buộc, §5.2) — khác các bài sắp ảnh dùng Spearman/Kendall toàn phần; (5) *signal-attribution một cue* (§4.3). Ta neo Stage-0 như một **"substrate-audit" cho miền GUI** (*substrate-audit = dùng so cặp làm **nền để phân tích** — phân tích cue, kiểm tính bắc cầu, partial-order — chứ KHÔNG nhằm thắng bảng xếp hạng*) — không tuyên bố chất lượng xếp hạng tổng quát vượt các bài trên. EZ-Sort/Dodgersort còn *có human-in-the-loop* lúc sắp; ta thì *tự động hoàn toàn* ở thì suy luận.

> **"Nhiều tài liệu trích từ năm 2000–2008, có cũ quá không, còn giá trị khoa học không?" — trả lời: còn nguyên giá trị, vì có HAI loại trích dẫn khác nhau.**
> - **Loại 1 — nền toán học / thuật toán → *nên* trích bài kinh điển gốc.** Copeland (Dwork, WWW 2001), minimum feedback arc set (Ailon, JACM 2008), $\tau$ so-hạng-bộ-phận (Fagin, SIAM 2006 / Lapata, CL 2006) là **định lý và định nghĩa toán học** — chúng **không hết hạn**: đúng năm 2001 thì 2026 vẫn đúng. Trích bài *đặt nền* là chuẩn mực học thuật (chứng tỏ biết nguồn cội, không "phát hiện lại bánh xe"); trích một preprint 2025 cho khái niệm Copeland mới là *lỗi trích dẫn*. Ví như dùng quy nạp toán học không ai chê "cũ vì có từ thời Euclid".
> - **Loại 2 — bằng chứng thực nghiệm / năng lực model / xu hướng đánh giá → phải MỚI**, và luận văn đã phủ bằng bài 2024–2026: pairwise (Qin, NAACL 2024), faithfulness không-tham-chiếu (FaithScore, EMNLP 2024), validate bằng nhiễu loạn (Sai, EMNLP 2021), so cặp bằng model thị giác (EZ-Sort CIKM 2025, Dodgersort PAKDD 2026), cùng một *freshness scan 2025–2026* (`report/42`) để chắc thiết kế không lỗi thời/bị scoop.
> - **Nguyên tắc gọn:** *nền toán → bài kinh điển; bằng chứng thực nghiệm → bài mới*. Trộn đúng chỗ là dấu hiệu khảo sát tài liệu **chín**, không phải cũ.

## 4.5. Chế độ ĐO vs Chế độ TRIỂN KHAI (điểm phòng thủ pipeline quan trọng nhất)

> ⚠️ **[LỖI THỜI phần lớn]** Lập luận "sinh mù để ĐO ảo giác của model *được prompt*" thay đổi khi ta **tự HUẤN LUYỆN model có mục tiêu**. Phần này cần viết lại theo Chương 0. Ranh giới train-vs-đo mới: **Chương 0 §0.5**.

Đây là mục **quan trọng nhất để bảo vệ pipeline** trước hội đồng 2026, và cũng là chỗ dễ bị hiểu nhầm nhất. Một giám khảo sắc sảo sẽ hỏi ngay:

> *"Xu hướng 2026 cho sinh hướng dẫn cho người là **grounded generation** — nạp thẳng cây giao diện / tài liệu vào mô hình **ngay lúc sinh** (ví dụ AskEase, CHI 2026). Vậy tại sao luận văn lại 'sinh mù'? Đưa danh sách nút vào lúc sinh thì vừa chính xác hơn vừa đúng triển khai thật chứ?"*

Đây là **câu hỏi hóc búa nhất về kiến trúc**. Câu trả lời gọn: **"sinh mù" không phải kiến trúc triển khai đề xuất — nó là *thiết bị đo*.**

> **Ẩn dụ dễ nhớ nhất — tháo kính để đo thị lực.** Muốn đo **thị lực thật** của một người, bác sĩ **bắt bỏ kính ra** rồi đọc bảng chữ. Không phải vì bác sĩ khuyên "sống đừng đeo kính" — mà vì **đeo kính vào thì đo ra thị lực của cái kính, không phải của mắt.** Sống thì cứ đeo kính (= triển khai *grounded*, cho model xem cây giao diện). Nhưng **lúc ĐO** thì phải tháo kính (= *sinh mù*, không cho model xem danh sách nút).
> Ánh xạ vào luận văn: nếu lúc ĐO mà vẫn "đeo kính" (nạp cây giao diện vào lúc sinh), model **chép lại** danh sách nút → phần nó *tự bịa* bị **che mất** → ta **không còn đo được đại lượng cần đo** (mức ảo giác tự thân của model). Grounding chỉ *giảm* ảo giác chứ không triệt tiêu, nên đưa nó vào lúc sinh **làm hỏng phép đo**, chứ không phải "cải tiến" nó.

Phải phân biệt rạch ròi hai chế độ:

| | **Chế độ ĐO** (trong luận văn, để đánh giá) | **Chế độ TRIỂN KHAI** (khi dùng thật) |
|---|---|---|
| Mục tiêu | *đo* mức mô hình tự ảo giác | *phục vụ* người dùng tốt nhất |
| Có đưa cây giao diện lúc sinh? | **KHÔNG** (sinh mù) | **CÓ THỂ CÓ** (grounded, như AskEase) |
| Vai của cây giao diện | chỉ ở thì **hậu kiểm / chấm** | có thể ở thì sinh |
| Vì sao chọn vậy | để phép đo không bị "chép đáp án" | để chính xác tối đa |

**Cách hoá giải bốn lớp (thứ tự đọc):**

1. **Phân định đo vs triển khai.** Luận văn **không** phản đối grounded-generation. Nó cần một *phép đo năng lực thật* của mô hình, và phép đo đó **buộc phải tháo bỏ ngữ cảnh** — nếu không thì không đo được gì. Chế độ triển khai hoàn toàn có thể grounded.
2. **Grounded-gen làm *hỏng phép đo*, không phải cải tiến nó.** Thêm ngữ cảnh vào lời nhắc làm tỉ lệ ảo giác **sụt mạnh** — ví dụ prompting phù hợp (chain-of-thought) hạ ảo giác từ **~38% xuống ~18%** (*Survey on hallucinations & prompting*, Frontiers in Artificial Intelligence 2025). Hệ quả logic: nếu nạp cây giao diện lúc sinh, mô hình **chép lại** → phần ảo giác *do model tự sinh* bị **che / làm nhiễu** trong phép đo (grounding chỉ *giảm*, không triệt tiêu ảo giác) → ta mất khả năng đo đại lượng cần đo. Đây là lý do **phương pháp luận**, không phải sở thích kỹ thuật.
3. **Grounded-gen cũng không "sạch".** Đưa nguyên cây giao diện dài vào lời nhắc gây kém hiệu quả và *vẫn sinh ảo giác* do thông tin thiếu trong cây — khớp con số >77% ứng dụng thiếu nhãn (Chen, ICSE 2020). Cây khuyết → grounded-gen vẫn bịa, lại còn mất khả năng đo. Vậy nó **không** phải "giải pháp hiển nhiên tốt hơn".
4. **Hậu kiểm đối chiếu nguồn ngoài là *paradigm chính danh* 2024–2026**, không phải chắp vá: FaithScore (Findings EMNLP 2024), Chain-of-Verification (Findings ACL 2024), RARR (ACL 2023), CaLM (ACL 2024), CRITIC (ICLR 2024) đều theo mẫu "sinh trước → đối chiếu / sửa theo nguồn độc lập". Và vì ta dùng tín hiệu **NGOÀI, phi-LLM, tất định** (so embedding với cây giao diện), ta thuộc đúng nhánh *được chứng minh hợp lệ* — **khác** "tự sửa nội tại" đã bị Huang et al. (ICLR 2024) chứng minh làm giảm chất lượng, và được củng cố bởi Tyen et al. (Findings ACL 2024): mô hình sửa lỗi *tốt* khi được **cấp vị trí lỗi từ một tín hiệu ngoài**, chứ tự dò thì kém.

> **"Nhưng thực tế nhiều app KHÔNG có sẵn cây giao diện — hệ có sập không?" (câu hỏi hay, trả lời 3 tầng):**
> 1. **Cây giao diện chỉ cần lúc CHẤM, không phải điều kiện để hệ CHẠY.** Nó là *kính hiển vi để nghiên cứu ĐO* (đo hệ bịa bao nhiêu), không phải *bánh xe để hệ chạy*. Triển khai thật: *sinh → kiểm → né bịa*, phần "kiểm" dùng bất kỳ nguồn nút nào **có sẵn tại thời điểm đó** (a11y tree live nếu có).
> 2. **Khi KHÔNG có nguồn nút nào → hệ xuống cấp AN TOÀN, không sập.** Đây đúng chỗ thiết kế "chỉ mô tả, không đoán" phát huy: không đối chiếu được thì **mô tả việc cần làm bằng lời** thay vì bịa tên nút. Người đọc vẫn dùng được, chỉ kém cụ thể hơn — và ta **báo minh bạch** %bước phải hạ xuống mô tả (fallback).
> 3. **Đảm bảo cốt lõi giữ ở mọi mức nguồn:** *không bao giờ trỏ tới một nút không tồn tại một cách tự tin*. Ta khai thẳng: chất lượng phần "kiểm" chỉ tốt bằng nguồn nút có được (>77% app thiếu nhãn — Chen ICSE 2020), nên dùng cây giao diện ở mức *hậu kiểm + fallback*, KHÔNG coi là chân lý tuyệt đối.

> **Sắc thái quan trọng (khớp thực tiễn 2026 — đọc kèm để không phòng thủ sai hướng):** khuyến nghị chủ đạo 2026 là **xếp lớp** (prompt + grounding/retrieval + hậu kiểm *cùng lúc*), **không** phải "post-hoc thay grounded". Vì vậy luận văn **không đối đầu** grounded-generation: chế độ triển khai hoàn toàn có thể grounded, và lớp hậu kiểm của ta là **một tầng kiểm tra độc lập xếp thêm lên trên** — đúng dòng "hybrid" mà ngành khuyến nghị. Ta chỉ tháo ngữ cảnh ở **chế độ ĐO** để đo được năng lực thật của mô hình.

> **Câu để tự trấn an (và để trả lời hội đồng):** câu hỏi này *không đâm vào kiến trúc*, nó đâm vào *cách trình bày kiến trúc*. Chỉ cần in rõ mục 4.5 này là vô hiệu hoá. (Xem thêm tổng hợp phòng thủ pipeline ở Chương 12.)

---

# CHƯƠNG 5 — PHƯƠNG PHÁP II: ĐÁNH GIÁ

Đây là đóng góp (B). Nguyên tắc bao trùm: **đo được mà không cần đáp án mẫu người viết, và không để hệ tự chấm chính mình.** Ta chia thước đo theo hai nhánh, đúng theo trục "có quỹ đạo vàng hay không" (§3).

> **BỘ THƯỚC CHỐT — nhìn một trang.**
>
> - **Nhánh một màn** (không có quỹ đạo vàng): *Độ trung thực* — headline = **tỉ lệ ảo giác bản gốc**, *không* phải trị số sau fallback — cộng *Độ đúng nhãn*.
> - **Nhánh nhiều màn** (có quỹ đạo vàng): *$\tau$ thứ tự bộ phận* (chỉ phạt cặp bắt buộc) + *Step-SR* (năng lực từng bước, teacher-forced) + *bấm đúng chỗ* (chỉ ở nhánh này, với bộ trỏ độc lập).
>
> Mọi điểm số được **chấm bằng 3 cơ chế độc lập** với công cụ ra quyết định (§5.4), và toàn bộ bộ thước được **kiểm định bằng nhiễu loạn** dưới khung *lý thuyết đo lường* (§7.2). Đây là bộ thước đã chốt sau deep-research 2026.

## 5.1. Nhóm thước đo một màn (không có quỹ đạo vàng)

> ⚠️ **[CẬP NHẬT — ĐẢO CHIỀU]** Trước đây point-in-bbox bị RÚT khỏi headline một-màn (M1 cũ). Hướng mới **đảo lại: point-in-bbox thành LÕI** — chính là **hàm thưởng** để train mô hình grounding (**Chương 0 §0.3–0.4**). Các thước còn lại (độ trung thực, đúng-nhãn) vẫn dùng để ĐO.

Vì nhánh một màn không có quỹ đạo vàng, nó chỉ đo được *mức không ảo giác* và *chất lượng gọi tên*, **chưa** đo được *đúng ý*. Ta khai thẳng giới hạn này (Chương 10) và để dành phần "đúng ý" cho nhánh nhiều màn.

**Giải thích bằng lời thường — chấm bài khi KHÔNG có "bài mẫu".** Bình thường muốn chấm một bài, ta so nó với *đáp án mẫu*. Ở đây không có đáp án mẫu — không ai soạn sẵn "hướng dẫn chuẩn" cho mọi màn hình của mọi app. Vậy chấm kiểu gì? *Mẹo của luận văn:* đừng cố chấm **"hay hay dở"** (chủ quan, cần đáp án mẫu), mà chấm **"có thật hay bịa"** (khách quan, chỉ cần đối chiếu danh sách nút thật). Cụ thể, thay vì hỏi *"hướng dẫn này có hay không?"*, ta hỏi *"mỗi nút mà hướng dẫn nhắc tới có THẬT SỰ tồn tại trên màn không?"*. Câu hỏi thứ hai trả lời được **mà không cần bài mẫu** — chỉ cần so với cây phân cấp giao diện (danh sách nút thật). **Hai thước một-màn** dưới đây (Def 5.1 *Độ trung thực* + Def 5.2 *Độ đúng nhãn*) đều xoay quanh ý này. *(Def 5.3 "bấm đúng chỗ" nêu ngay dưới CHỈ để tham chiếu định nghĩa — theo quyết định M1 nó KHÔNG tính vào headline một màn, mà là đối chứng ở nhánh nhiều màn / ScreenSpot.)*

> **Định nghĩa 5.1 (Độ trung thực — Faithfulness).**
> $$\text{Faith} = 1 - \frac{\big|\{\text{bước ảo giác}\}\big|}{\big|\{\text{bước có nhắc tới nút}\}\big|}.$$
> **Ví dụ.** Nếu trong 3 bước có nhắc nút mà 1 bước là ảo giác, thì $\text{Faith} = 1 - \tfrac{1}{3} \approx 67\%$.
>
> **Con số headline báo cáo là *tỉ lệ ảo giác của bản gốc* $\approx \tfrac{1}{4}$**, chứ **không** phải con số ~100% sau khi đã fallback. Lý do: sau fallback, mọi tham chiếu bịa đều đã bị thay bằng mô tả, nên độ trung thực gần như luôn ~100% *do thiết kế* — đó là một *trần trời*, khoe nó là tự lừa. Cái ta thật sự phát hiện là *bản gốc bịa bao nhiêu*, và cái ta trả giá là *bao nhiêu bước phải hạ thành mô tả* (%fallback). Con số $\tfrac{1}{4}$ luôn đi kèm **ba điều kiện**: (a) *độ phủ nhãn VH* (do vấn đề nút icon-only ở §3.1); (b) *màn-dày-nhãn* — mẫu một-màn lọc theo tiêu chí `MIN_ACT≥6` (ưu tiên màn nhiều nút có nhãn actionable), nên tỉ-lệ-bịa quan sát được là **hạ thấp có hệ thống** so với màn thưa nhãn; (c) ở giai đoạn này là *quan sát sơ bộ trên một mô hình*. Vì vậy tỉ-lệ-bịa được báo **phân tầng theo độ-phủ-nhãn** (55/38/45 màn thấp/trung/cao) như một *kiểm-tra-cơ-chế* (phủ↓ ⇒ bịa↑), **không** nâng $\tfrac{1}{4}$ thành "phát hiện tổng quát".
> Trụ nguồn: ALOHa, NAACL 2024.

**Cách đọc công thức bằng lời.** Mẫu số = *số bước có nhắc tới một nút* (chỉ đếm các bước dạng "bấm nút X", bỏ qua bước dạng "chờ 3 giây"). Tử số = *trong các bước đó, bao nhiêu bước nhắc tới nút KHÔNG có thật*. Lấy 1 trừ đi tỉ lệ bịa → ra "độ trung thực": 100% = mọi nút được nhắc đều có thật; 0% = bịa hết.

**Ví dụ chạy đầy đủ.** Hướng dẫn cho một màn gồm 4 bước: *(1) "Bấm **Following**" · (2) "Bấm **Popular**" · (3) "Chờ trang tải" · (4) "Bấm **Cài đặt**"*. Đối chiếu với danh sách nút thật {Following, Popular, Groups, …} (màn KHÔNG có nút "Cài đặt"):
- Bước 3 *không nhắc nút* → **không tính vào mẫu số**.
- Còn 3 bước nhắc nút (1, 2, 4); trong đó **bước 4 ("Cài đặt") là bịa**.
- ⇒ Độ trung thực $= 1 - \tfrac{1}{3} \approx 67\%$ → ta báo *tỉ lệ ảo giác gốc = 33%* cho màn này.

Đây đúng là bước mà bước đối chiếu với giao diện thật (§4.2) sẽ bắt: phát hiện bước 4 bịa và viết lại thành *"Tìm và bấm nút phù hợp để mở thêm tuỳ chọn"*.

> **Định nghĩa 5.2 (Độ đúng nhãn — Label fidelity).** Tỉ lệ bước gọi **đúng tên hiển thị** của nút, trên tổng số bước có trỏ tới nút thật. Ví dụ nếu màn có nút hiển thị "OK" mà hướng dẫn viết "Đồng ý", thì bước đó *đúng chỗ nhưng sai tên*. **Đây là thước tự định nghĩa — ta khai thẳng điều này**: khớp chuỗi tên không đồng nghĩa với *độ rõ ràng cho người đọc*, nên đây là một chỉ báo bổ trợ, không phải chân lý.

> **Định nghĩa 5.3 (Bấm đúng chỗ — grounding).** Một điểm bấm dự đoán $(x, y)$ được coi là **trúng** nếu nó nằm **trong khung nút chuẩn** (point-in-GT-bbox): $l \le x \le r$ và $t \le y \le b$.
> **Ví dụ thật:** item ScreenSpot "invert the lens" có khung $(965, 2105, 1110, 2258)$; nếu bộ trỏ dự đoán $(1030, 2180)$ thì điểm nằm trong khung → *trúng*.
>
> **Chuẩn chấm — cập nhật 2026.** Deep-research xác nhận: chuẩn grounding hiện hành (ScreenSpot-Pro, UI-TARS — 2025) là **point-in-GT-bbox nguyên bản** (điểm có nằm trong khung đúng hay không), *cố ý bỏ* IoU và bán kính dung sai-%. Vì vậy ta lấy **point-in-GT-bbox làm định nghĩa chính**, và chỉ giữ *dung sai 14% đường chéo* (AITW, NeurIPS 2023) như một **biến thể đối chứng** khi so trên bộ có toạ độ vàng (AITW / AndroidControl) — **không** làm định nghĩa chuẩn. Nguồn thước gốc: SeeClick, ACL 2024; neo bình duyệt cho chuẩn point-in-bbox: ScreenSpot-v2 / OS-Atlas, ICLR 2025.
>
> **Đã chuyển thước này RA KHỎI headline một màn (quyết định M1).** Lý do: nếu ta lấy *tâm của khung nút đã khớp* làm $(x,y)$ thì nó luôn nằm trong khung → luôn trúng → **tautology 100%**, một con số vô nghĩa. Thước này chỉ được dùng ở (i) nhánh nhiều màn — nơi có *toạ độ vàng* thật để so — hoặc (ii) đối chứng ScreenSpot-v2, và trong cả hai trường hợp, $(x,y)$ **phải đến từ một bộ trỏ độc lập** (dự đoán từ tên + ảnh, kiểu ScreenSpot), **không** được lấy tâm bbox đã khớp.
>
> *Ghi chú tách trục (quan trọng khi bảo vệ):* năng lực **grounding toạ độ** của VLM đang cải thiện nhanh theo đời model, nhưng đó là *trục khác* với **độ trung thực của văn bản sinh cho người** (§5.1) — cái sau mới là vấn đề trung tâm của luận văn. Bảng số phải trình bày hai trục tách biệt để không bị so lệch.

> **Giải thích thêm bằng lời thường — bộ trỏ đứng ở đâu, và ScreenSpot chứng minh gì (bốn câu hay bị hỏi).**
> - **Bộ trỏ không nằm trong hệ sinh.** Hệ sinh chỉ đẻ ra *văn bản* ("Bấm nút OK"), không hề tính toạ độ. Bộ trỏ là một *dụng cụ đo* riêng — một mô hình grounding có sẵn — chỉ chạy *lúc chấm điểm*, đứng ngoài và sau hệ sinh. Cách phân định gọn: hệ sinh làm việc với *chữ*, bộ trỏ làm việc với *toạ độ*; mà toạ độ thì hệ sinh không sinh ra cũng không dùng tới.
> - **ScreenSpot không chứng minh hệ sinh hiệu quả.** Trên ScreenSpot, bộ trỏ chạy trên chỉ dẫn của *chính ScreenSpot*, nên con số đó dùng để *kiểm chất lượng dụng cụ đo* (bộ trỏ giỏi cỡ nào) trên một bộ chuẩn đã bình duyệt, đồng thời *bù độ tin cậy* cho MobileViews (vốn là preprint). Hiệu quả của hệ sinh nằm ở chỗ khác: **độ trung thực trước/sau + %fallback + đối chứng silent-error** (một màn) và **τ + Step-SR** (nhiều màn) — những thước này chấm bằng *văn bản*, không đụng bộ trỏ.
> - **Bộ trỏ đo dở có làm hệ tụt điểm oan không?** Có — *nếu* dùng grounding để chấm hệ, nên ta không làm vậy. Grounding chỉ là trục phụ; bảng điểm chính không dùng bộ trỏ; và ta hiệu chỉnh bộ trỏ trên ScreenSpot rồi báo kèm độ chính xác của nó, để quy được một cú "trượt" là do nút khó hay do dụng cụ. Thay bộ trỏ tốt/dở chỉ đổi *con số grounding*, không đổi một chữ nào trong hướng dẫn hệ sinh ra.
> - **Nút chỉ có biểu tượng (icon), không có nhãn chữ thì sao?** Với *người đọc*, mô tả theo chức năng ("nút lật ống kính") vẫn dùng được — người nhìn icon là nhận ra, không cần toạ độ. Lúc chấm độ trung thực, nút không có nhãn dùng được bị *loại khỏi mẫu số* (không tính đúng cũng không tính sai) và ta *báo độ phủ nhãn* kèm theo (>77% app thiếu nhãn — Chen, ICSE 2020). Lúc chấm grounding, ta *báo riêng nút chữ và nút biểu tượng* vì icon khó trỏ hơn — khai thẳng, không giấu.

## 5.2. Nhóm thước đo nhiều màn (có quỹ đạo vàng)

Nhờ có quỹ đạo vàng, nhánh này đo được hai thứ mà nhánh một màn không đo được: *sắp đúng thứ tự* ($\tau$) và *năng lực từng bước* (Step-SR, teacher-forced — xem lưu ý quan trọng ở Định nghĩa 5.5). Đây là nơi cung cấp "con số năng lực thật" cho đóng góp (A).

**Giải thích bằng lời thường — vì sao KHÔNG chấm "sắp đúng y hệt".** Khi hệ sắp lại N màn, cách chấm ngây thơ là "so với thứ tự vàng, đúng y hệt thì 10 điểm, sai một chỗ trừ điểm". Nhưng cách đó **phạt oan**: nhiều quy trình có những bước **đổi thứ tự vẫn đúng** (ví dụ *điền email* rồi *điền số điện thoại* — làm cái nào trước cũng được). Nếu bắt hệ phải khớp đúng thứ tự vàng từng li thì ta phạt nó ở chỗ *vốn dĩ tự do*. Vì vậy ta dùng **thứ tự bộ phận (partial order)**: chỉ chấm những cặp màn mà thứ tự **buộc phải đúng** (gọi là *cặp bắt buộc*), bỏ qua các cặp tự do. Thước $\tau$ dưới đây hiện thực hoá ý này.

> **Định nghĩa 5.4 ($\tau$ thứ tự bộ phận — partial-order correlation).** Gọi $M$ là tập **cặp bắt buộc** — những cặp màn mà thứ tự giữa chúng *buộc phải đúng*. Tập $M$ được suy ra **từ quỹ đạo vàng** bằng quy tắc *nhân quả*: nếu màn $B$ chỉ xuất hiện *sau* khi thực hiện một gold-action ở màn $A$, thì $(A, B) \in M$. Gọi $C$ là số cặp trong $M$ mà hệ xếp *thuận chiều* gold, $D$ là số cặp hệ xếp *nghịch chiều*. Khi đó:
> $$\tau = \frac{C - D}{|M|} \in [-1, +1].$$
> **Ví dụ.** Gold có thứ tự $A < B < C$ và cả ba cặp đều bắt buộc. Hệ xếp thành $A, C, B$: cặp $(A,B)$ thuận, $(A,C)$ thuận, $(B,C)$ nghịch → $\tau = \tfrac{2 - 1}{3} = +0{,}33$.
>
> **Điểm tinh tế — cặp tự do không bị phạt.** Nếu quy trình cho phép làm hai việc theo thứ tự bất kỳ (ví dụ điền email rồi số điện thoại, hay ngược lại — đều đúng), thì cặp đó **không** thuộc $M$, nên hệ đảo thứ tự vẫn được tính đúng. Nhãn của $M$ được suy **từ gold**, **không** hỏi mô hình hay bộ dò cue (để chống tự chấm).
>
> **Tên đúng của thước:** đây là *tương quan thứ tự bộ phận* theo **Fagin et al. 2006** ("Comparing partial rankings", SIAM J. Discrete Math) và **Lapata, Computational Linguistics 2006** — **KHÔNG** phải "Kendall τ b". Việc gọi đúng tên tránh một lỗi trích dẫn mà giám khảo có thể bắt.
> *Ghi chú attribution (để chặt hơn):* ca "cặp *tự do* / không so được" (incomparable pairs) khớp chính xác hơn với **Brandenburg, Gleißner & Hofmeier (2012/13)** — Fagin gốc bàn về *ties/bucket-order*. Ta khai đây là một **near-metric dùng để chấm điểm** (khi $p=0$, độ đo không thoả bất đẳng thức tam giác — theo chính Fagin), nên tránh chữ "the correct measure"; gọi là *"thước thứ tự bộ phận ta dùng"*.

**Ví dụ chạy đầy đủ — có cả cặp bắt buộc lẫn cặp tự do.** Một quy trình 4 màn, thứ tự vàng: **A** (mở form) → **B** (điền email) → **C** (điền số điện thoại) → **D** (bấm Gửi). Quy tắc nhân quả từ gold cho biết:
- $(A,B)$, $(A,C)$, $(A,D)$: **bắt buộc** (phải mở form trước mới điền/gửi được).
- $(B,D)$, $(C,D)$: **bắt buộc** (phải điền xong mới gửi).
- $(B,C)$: **TỰ DO** — điền email hay số điện thoại trước đều được → *không* đưa vào tập $M$.

Vậy tập cặp bắt buộc $M = \{(A,B),(A,C),(A,D),(B,D),(C,D)\}$, tức $|M| = 5$.
Giả sử hệ sắp ra: **A → C → B → D** (nó đảo B và C). Kiểm từng cặp trong $M$:
- $(A,B)$ thuận ✓ · $(A,C)$ thuận ✓ · $(A,D)$ thuận ✓ · $(B,D)$ thuận ✓ · $(C,D)$ thuận ✓ → **cả 5 đều thuận!**
- Cặp $(B,C)$ bị đảo? *Không sao* — nó là cặp tự do, không nằm trong $M$.
- ⇒ $C = 5$, $D = 0$, $\tau = \tfrac{5-0}{5} = +1{,}0$ (điểm tuyệt đối).

**Ý nghĩa:** hệ đảo B↔C nhưng vẫn được **10 điểm**, vì đó là chỗ *đổi thứ tự vẫn đúng*. Nếu dùng thước ngây thơ (Kendall toàn phần) thì hệ bị trừ oan ở cặp $(B,C)$. Đây chính là cái hay của "thứ tự bộ phận".

> **Định nghĩa 5.5 (Step-SR — Step Success Rate, teacher-forced).**
> $$\text{Step-SR} = \frac{\big|\{\text{bước hệ làm đúng}\}\big|}{\big|\{\text{bước trong quỹ đạo vàng}\}\big|}.$$
> Một bước được coi là "đúng" khi *đúng loại thao tác* **và** *lệch toạ độ $\le 14\%$* (14% là **ngưỡng mượn từ AITW**, không phải chuẩn ngành thống nhất). "Teacher-forced" nghĩa là ở mỗi bước ta đặt hệ vào đúng trạng thái của gold rồi mới hỏi bước kế.
> **Step-SR là *proxy chẩn đoán NĂNG LỰC TỪNG BƯỚC*, KHÔNG phải thước "làm tới đích".** Chính bài AndroidControl (Li et al., NeurIPS 2024) cảnh báo: step-accuracy *không* dự báo tốt xếp hạng theo người, và teacher-forcing (bơm lại trạng thái vàng mỗi bước) **cố ý che lỗi tích luỹ** → **không** đo được năng lực end-to-end "tới đích". Muốn đo "tới đích" phải dùng *task-success-rate* riêng (ngoài phạm vi hiện tại → future-work).
> **Ví dụ thật (quy trình Drive 5 bước ở §3.2):** nếu hệ khớp đúng 4/5 thao tác vàng thì $\text{Step-SR} = 80\%$ — đọc là *"làm đúng 4/5 bước KHI được đặt đúng trạng thái"*, **không** phải "hoàn thành 80% tác vụ".
> Nguồn: AndroidControl, NeurIPS 2024. Trục tham chiếu chuẩn ngành cho *step-accuracy*, ta **không** claim ngang leaderboard.

> **Định nghĩa 5.6 (PMR — Perfect Match Rate).** Trên một tập $E$ episode nhiều màn, PMR là **tỉ lệ episode được sắp ĐÚNG TRỌN thứ tự bắt buộc** — tức mọi cặp trong $M$ (Def. 5.4) đều thuận chiều gold ($\tau = +1$ cho episode đó):
> $$\text{PMR} = \frac{\big|\{\,e \in E : \tau(e) = +1\,\}\big|}{|E|} \in [0, 1].$$
> **Quan hệ với $\tau$:** $\tau$ đo *mức* đúng trung bình trên từng cặp (mềm, từng phần); PMR đo *tỉ lệ episode hoàn hảo* (cứng, tất cả hoặc không). Hai thước bổ nhau — một hệ có thể $\tau$ cao mà PMR thấp (gần đúng ở nhiều episode nhưng hiếm khi trọn vẹn). **Ví dụ:** 100 episode, 42 episode đạt $\tau=+1$ → PMR = 42%. PMR là thước phụ ở E8/T8 cạnh $\tau$ và pairwise-acc.

## 5.3. Bảng định vị các thước đo

| Thước | Nhánh | Đo điều gì | Nguồn |
|---|---|---|---|
| Độ trung thực (Faith) | một màn | không tham chiếu nút không tồn tại | ALOHa, NAACL 2024 |
| Độ đúng nhãn | một màn | gọi đúng tên hiển thị | tự định nghĩa (khai thẳng) |
| Bấm đúng chỗ (grounding) | nhiều màn / ScreenSpot | điểm trỏ trúng khung nút (point-in-GT-bbox) | SeeClick ACL 2024 · OS-Atlas ICLR 2025 |
| $\tau$ thứ tự bộ phận | nhiều màn | sắp đúng thứ tự (chỉ cặp bắt buộc) | Fagin 2006 · Lapata CL 2006 |
| Step-SR | nhiều màn | năng lực từng bước (teacher-forced; **không** phải "tới đích") | AndroidControl, NeurIPS 2024 |
| PMR (Perfect Match Rate) | nhiều màn | tỉ lệ episode sắp ĐÚNG TRỌN thứ tự (phụ, cạnh τ) | Def. 5.6 (dựng trên Fagin 2006) |

## 5.4. Ba cơ chế chấm khác cơ chế (chống tự chấm) — giảm, KHÔNG loại, tương quan

Một thước đo tốt vẫn có thể vô nghĩa nếu *công cụ ra quyết định cũng là công cụ chấm điểm*. Ta phòng bẫy này bằng cách tách rõ:

- **Quyết định** khớp/fallback dùng embedding `nomic` (đặt tên $\tau_A$).
- **Chấm** dùng **ba cơ chế khác cơ chế / khác họ:** (1) embedding `bge-m3` (họ khác `nomic`); (2) một LLM-judge nhị phân *khác họ với generator*; (3) token-overlap (chồng lấp từ) — một phép đếm **phi-neural**, thực sự khác cơ chế.

> **Khai thẳng (không overclaim "độc lập tuyệt đối"):** ba cơ chế **giảm** chứ **không loại** tương quan sai số — hai bộ neural (bge-m3, LLM-judge) vẫn có thể mắc lỗi tương quan; chỉ token-overlap là trục *thực sự khác cơ chế*. Vì vậy ta **báo hệ số tương quan / số cơ chế hiệu dụng (neff) giữa các bộ chấm** thay vì tuyên bố chúng "độc lập". Điểm mạnh cốt lõi vẫn giữ: bước **QUYẾT** dùng embedding (`nomic`), *không phải generator*, nên bẫy "generator tự chấm mình" vốn đã không tồn tại ở bước quyết. Trụ self-preference: Panickssery, NeurIPS 2024.

> **Vì sao LLM-judge phải khác họ generator?** Vì generator ở lõi là `gpt-4o-mini` (họ GPT), nên LLM-judge **không được** dùng mô hình họ GPT — do một mô hình có xu hướng *thiên vị đầu ra của chính họ nó* (Panickssery et al., NeurIPS 2024). Đây không phải cẩn thận thừa mà là một nguồn thiên lệch đã được đo trong tài liệu.

---

# CHƯƠNG 6 — VÍ DỤ CHẠY ĐẦU–CUỐI

Để gắn kết mọi định nghĩa lại, chương này chạy trọn vẹn hai ví dụ có số.

## 6.1. Một màn (đầy đủ, có số)

**Đầu vào.** Ảnh một màn đặt giờ; VH của màn $= \{\text{hour}, \text{minute}, \text{PM}, \text{OK}, \text{Cancel}\}$; câu hỏi *"Cần thao tác gì để đặt giờ 20:35 và xác nhận?"* (câu hỏi không chứa tên nút, đúng ràng buộc).

**Bước 1 — sinh mù.** VLM (không thấy VH) trả về bản nháp $T^{(0)}$:
1. `Chọn giờ và phút`
2. `Chọn "PM"`
3. `Bấm "Menu"`

**Bước 2 — đối chiếu ngữ nghĩa** (ngưỡng $\tau = 0{,}55$):

| Bước | Nút thật gần nhất | sim | Kết luận |
|---|---|---|---|
| 1 | hour / minute | 0,85 | khớp |
| 2 | PM | 1,00 | khớp |
| 3 "Menu" | (không nút nào gần) | 0,30 | **ảo giác** |

**Bước 3 — fallback.** Bước 3 được viết lại: `Bấm "Menu"` → `Tìm và bấm nút phù hợp để mở thêm tuỳ chọn`.

**Chấm.**
- Độ trung thực của *bản gốc*: $\text{Faith} = 1 - \tfrac{1}{3} \approx 67\%$ → **báo cáo tỉ lệ ảo giác gốc $= 33\%$** cho màn này.
- Độ đúng nhãn: 2/2 nút thật được gọi đúng tên → $100\%$.
- Tỉ lệ fallback: $1/3$ số bước.

Ví dụ này cho thấy trọn vẹn *cái ta báo cáo* (33% ảo giác gốc) và *cái ta trả giá* (một bước thành mô tả) — không tô vẽ con số 100% hậu fallback.

## 6.2. Nhiều màn (dùng quy trình Drive thật ở §3.2)

**Đầu vào.** 5 màn của quy trình "tạo lối tắt PDF" bị **xáo trộn**, kèm mục tiêu đã cho.

**Stage-0 — sắp thứ tự.** So $\binom{5}{2} = 10$ cặp → tổng hợp Copeland → giả sử ra một thứ tự $\hat\pi$. Giả sử $\hat\pi$ đảo *một cặp bắt buộc* so với gold; khi đó $\tau < 1$ — ví dụ $\tau = +0{,}8$.

**Sinh + chấm.** Đưa chuỗi đã sắp qua nhánh một màn; so từng thao tác hệ đề xuất với quỹ đạo vàng $G = (\text{click}(1016,866),\, \text{scroll}(\text{down}),\, \dots)$ → Step-SR, ví dụ khớp 4/5 = $80\%$.

**Kết quả một quy trình:** cặp số $(\tau = +0{,}8,\ \text{Step-SR} = 80\%)$ — nói lên hệ *vừa sắp gần đúng thứ tự, vừa làm đúng phần lớn thao tác từng bước (khi được đặt đúng trạng thái)*. Đây chính là loại con số nâng đóng góp (A) từ "không bịa" lên "làm đúng thao tác" — *lưu ý: đây là năng lực từng bước, không phải "hoàn thành tác vụ" (§5.5)*.

---

# CHƯƠNG 7 — TÍNH HỢP LỆ & THIẾT KẾ THỰC NGHIỆM

Chương này trả lời câu hỏi mà một hội đồng nghiêm khắc sẽ hỏi trước tiên: *"làm sao biết các con số này không phải tự huyễn hoặc?"*.

## 7.1. Chống vòng lặp luận lý (circularity)

> **Nguyên tắc 7.1.** Công cụ **QUYẾT** ảo giác (embedding $A$ = `nomic`) phải **khác** công cụ **CHẤM** (embedding $B$ = `bge-m3`, khác họ) + LLM-judge *khác họ generator* + token-overlap = **ba cơ chế khác cơ chế** (giảm — không loại — tương quan sai số; báo neff, §5.4). Con số headline là *tỉ lệ ảo giác gốc*, **không** phải trị số sau fallback.
>
> **Cơ sở.** Nếu dùng chính công cụ ra quyết định để chấm, ta rơi vào *circularity* — "vừa ra đề vừa chấm", điểm số cao là hiển nhiên chứ không phản ánh chất lượng. Và LLM có xu hướng thiên vị đầu ra cùng họ (Panickssery, NeurIPS 2024), nên judge bắt buộc khác họ.

Đây là bài học lớn nhất rút ra từ một vòng review sâu (3 agent) hồi thiết kế: bản đầu có bộ khớp *vừa sửa vừa chấm*, khiến độ trung thực ~100% chỉ là *tautology*. Bản hiện tại vá lỗi này bằng PA2 (chỉ *matched / fallback*, không sửa) và chấm bằng `bge-m3` độc lập.

## 7.2. Kiểm định thước đo bằng nhiễu loạn có kiểm soát (perturbation)

Thay vì nhờ người chấm (thầy hướng dẫn không ưa chấm người, và bản thân human-eval cũng thiếu tin cậy — xem cuối mục), ta kiểm tra *chính thước đo* bằng cách **cố ý bơm lỗi đã biết** vào những hướng dẫn đúng, rồi xem thước đo có phản ứng đúng hướng không. Đây là một **paradigm meta đánh giá có tiền lệ bình duyệt**: kiểm thử hành vi bằng cặp tối thiểu/nhiễu loạn (CheckList → Ribeiro ACL 2020; Sai et al., EMNLP 2021; **BUMP — "Benchmark of Unfaithful Minimal Pairs", ACL 2023**, đúng cơ chế bơm một lỗi tối thiểu vào bản trung thực rồi đo thước có phân biệt được không).

> **Bốn tiêu chí một thước đo tốt phải qua (chuẩn meta-eval 2025).** Deep-research cho thấy bar 2025 không chỉ đòi "độ nhạy" mà cả bốn:
> 1. **Độ nhạy (sensitivity)** — bơm lỗi thật thì điểm phải đổi đúng hướng.
> 2. **Đơn điệu theo mức nghiêm trọng (monotonicity)** — lỗi nặng hơn thì điểm phải tệ hơn.
> 3. **Bền với biến đổi lành tính (benign robustness)** — đổi cách viết mà **không** đổi nghĩa thì điểm **không được** đổi.
> 4. **Phân biệt loại lỗi (error-type discrimination)** — phải tách được bịa nút vs sai thứ tự vs sai nhãn.

Cụ thể, harness bơm các loại lỗi (mỗi loại kiểm một tiêu chí):
- **Chèn một nút ma** vào hướng dẫn đúng → độ trung thực **phải giảm** *(sensitivity)*; chèn nhiều nút ma hơn → giảm sâu hơn *(monotonicity)*.
- **Thay tên bằng đồng nghĩa** ("Save" → "Lưu") → độ trung thực **phải giữ nguyên** (vẫn đúng nút), nhưng độ đúng nhãn **giảm** *(một dạng error-type discrimination)*.
- **(bổ sung 2026 — bắt buộc để đủ 4/4) Diễn đạt lại lành tính (benign paraphrase):** viết khác đi mà giữ đúng nút/thứ tự → **mọi điểm số phải bất biến**. Nếu điểm đổi, thước đang bắt nhầm *văn phong* thay vì *nội dung*.
- **(bổ sung 2026 — bắt buộc) Phân biệt loại lỗi:** bơm riêng từng loại (bịa nút / sai thứ tự / sai nhãn) và kiểm mỗi loại rơi đúng vào thước tương ứng (bịa nút → Faith; sai thứ tự → $\tau$; sai nhãn → đúng nhãn), không lẫn.

Quan trọng: *lỗi được bơm độc lập với bộ khớp* — nếu dùng chính bộ khớp để tạo lỗi thì lại circular.

> **Đóng khung theo lý thuyết đo lường (measurement theory) — vá câu phản biện "thiếu validation".** Ta khai rõ: perturbation chứng minh **độ nhạy + độ tin cậy hành vi** của thước — đây là *một mặt* (facet) của tính hợp lệ, **chưa** phải *convergent validity* (đối sánh với chuẩn vàng độc lập). Construct "trung thực hoá" được đo bằng **tam giác bằng chứng**: perturbation (độ nhạy) + đối chứng thất bại silent-error (§4.2) + %fallback. **Human-correlation KHÔNG làm cổng đậu/rớt** — vì (i) đây đúng khung *measurement-theory* mà reviewer 2026 dùng để đọc metric (định vị bằng position/D&B track NeurIPS 2025 về *construct validity* của benchmark LLM), và (ii) bản thân human-eval cũng thiếu tin cậy: chỉ ~18–30% bài báo NLG báo độ đồng thuận giữa người chấm, và người chưa huấn luyện phân biệt văn người/máy chỉ ~49,9% (≈ ngẫu nhiên) — ép nó làm gold-gate là *nguỵ hợp lệ* (Clark et al., ACL-IJCNLP 2021).
> **Điều chỉnh (R-08, quan trọng): KHÔNG đẩy human-correlation *hẳn* về 0-annotate.** Ta vẫn **chấm người một MẪU NHỎ per-criterion NGAY** (để chứng minh *content validity* + *độ nhạy*, ở mức **partial**), chỉ là **không** làm cổng cứng. Lý do: measurement-theory dùng để biện minh *lại đòi* convergent/criterion validity = tương quan người; nếu 0 annotate thì để hở "validation gap". Vì vậy đóng khung là **"content + sensitivity validity (partial)"**, KHÔNG claim đạt *construct validity đầy đủ*. Trụ nguồn bình duyệt: Sai et al. (EMNLP 2021) · BUMP (ACL 2023) · Ribeiro et al. (ACL 2020) · Clark et al. (ACL-IJCNLP 2021).
>
> **Phân định chủ động với FaithScore (bắt buộc — câu hỏi hóc búa nhất).** FaithScore (Findings EMNLP 2024) cũng đo faithfulness *reference-free* cho mô hình thị giác nhưng **vẫn** validate bằng human-correlation — reviewer có thể chỉ vào đó nói ta "thiếu". Ba điểm phân định: (1) FaithScore *tự soi lại bằng chính VLM* (self-check, dễ kế thừa lỗi thị giác → chính nó cũng cần validate), còn ta đối chiếu với **cây phân cấp giao diện CÓ CẤU TRÚC** bằng matcher embedding *tất định* (không LLM ở bước quyết matched/fallback); (2) ta **không bỏ** human-correlation — vẫn chấm người một **mẫu nhỏ per-criterion** (content + sensitivity validity, *partial*) — chỉ đặt perturbation làm *trục chính* và **không** biến human-correlation thành cổng đậu/rớt; (3) miền của ta là GUI no-gold với nguồn neo cấu trúc, không phải mô tả ảnh tự do. Viết đoạn này **trước khi** giám khảo nêu.

## 7.3. Xử lý VH không hoàn hảo

Như §2.2 và §3.1 đã nêu, VH thiếu/nhiễu nhãn (>77% app thiếu nhãn — Chen, ICSE 2020). Cách xử lý: đo **độ phủ nhãn** (tỉ lệ nút *bấm được* mà có nhãn dùng được), **loại các nút nhãn chung khỏi mẫu số**, và luôn báo tỉ lệ ảo giác dưới dạng "**có điều kiện độ phủ (recall-VH)**". Ta **không** khẳng định "vì có sẵn khung nút nên rủi ro bị chặn" — khẳng định đó mâu thuẫn với chính Chen ICSE 2020 và đã bị gỡ khỏi tài liệu.

> **Cổng cứng K1:** phải *đo được recall của bộ dò/VH* trước khi tin vào mẫu số. Một bộ chỉ có ảnh trần không đủ; ta cần nguồn phần tử (VH / a11y tree) với recall đo được.

## 7.4. Thiết kế thống kê

Con số đẹp mà không có khoảng tin cậy đúng thì vô giá trị. Thiết kế thống kê:

- **Cluster bootstrap theo APP.** Các màn cùng một app *không độc lập* với nhau (chung phong cách thiết kế, chung tên nút). Nếu bootstrap theo từng màn, ta sẽ có khoảng tin cậy *hẹp giả tạo*. Do đó ta tái chọn mẫu **theo cụm app** (10.000 lần resample). Số cụm: **một màn G=30 app** (127 màn/30 app) — nhưng do lệch cỡ (top-4 app = 25% mẫu, 4 app singleton), **số cụm hiệu dụng Kish $G_{\text{eff}} \approx 24$**, KHÔNG phải 30; **nhiều màn 237 app** trên 286 ep (nhưng **194 app singleton 1-ep** → G danh nghĩa cao mà nhiều cụm cỡ 1, báo N_eff thật). Vì một màn $G_{\text{eff}}\approx24 < 42$, ta dùng **wild-cluster bootstrap-t** làm phương pháp chính, **kiểm chéo jackknife CV3/CV3J**, **khai thẳng caveat under-coverage**.
  > **Estimand (khai rõ để không overclaim):** mẫu chọn theo hướng **tối đa hoá đa dạng app** (có chủ đích), nên đại lượng ước lượng là **trung bình đều trên app (macro-average, mỗi app một phiếu)**, KHÔNG phải "tần suất app điển hình người dùng gặp". **CẤM chữ "đại diện cho ứng dụng nói chung"** ở mọi chỗ. Lợi thế: macro-average làm claim **bảo thủ HƠN** (nhiều app hiếm/khó) → hiệu ứng dương sống trên mẫu macro thì **mạnh hơn** mẫu prevalence lệch về vài app phổ biến.
  > *Cập nhật trụ nguồn 2026 (R7):* không có phương án "sạch" cho ít cụm — wild-cluster bootstrap-t (Cameron–Gelbach–Miller 2008) under-coverage khi $G$ nhỏ + cụm lệch cỡ; subcluster-bootstrap và randomization-inference cũng có điểm gãy riêng. Ta nâng trích dẫn lên **MacKinnon–Nielsen–Webb (Journal of Econometrics 2023)** làm hướng dẫn đương đại + **jackknife CV3 (JAE 2023)** kiểm chéo. Nhánh một màn $G_{\text{eff}}\approx24$ vẫn dưới 42 nên vẫn là *điều kiện bất lợi đã biết* (nhẹ hơn mốc pilot 17 cũ); nhánh nhiều màn **237 app** thoát vùng nguy hiểm về số cụm (dù 194 singleton → báo N_eff thật). Số hiện tại là **exploratory** cho tới khi chạy chính thức.
  > *Ước lượng power/MDE (thô, chốt lại sau pilot):* với m̄≈4,2 và ICC giả định ~0,2 (**ICC = tương quan nội cụm**: màn cùng app giống nhau cỡ nào), cỡ mẫu hiệu dụng một màn $N_{\text{eff}} \approx 127/(1+3{,}2\cdot0{,}2) \approx 77$ (ICC thực sẽ **đo từ pilot** rồi tính MDE chính thức — không chốt số MDE trước khi có phương sai quan sát).
  > *(Các thuật ngữ thống kê — wild-cluster bootstrap-t, N_eff, MDE, approximate-randomization — đều có định nghĩa một dòng ở **chú giải bảng §13.2**.)*
- **Hiệu chỉnh đa kiểm định Holm** (vì báo cáo nhiều thước cùng lúc).
- **Cố định hạt giống** (seed) để tái lập; **≥ 30 episode mỗi mốc $N$**.
- **Đăng ký trước (pre-registration).** Ghi ngưỡng và giả thuyết **TRƯỚC** khi nhìn kết quả. Timestamp của pre-registration = `git init` + commit `report/22` *trước khi chạy* (repo phải ở trạng thái git để dấu thời gian đáng tin). Kết quả "**không khác biệt**" vẫn được báo cáo — đó là đóng góp hợp lệ, không phải thất bại (chủ trương "null vẫn đậu" cho nhánh B). Ở giai đoạn hiện tại, mọi số là *exploratory* cho đến khi hoàn tất pre-registration + chạy chính thức.

## 7.5. Bản đồ các cổng cứng (kill-test)

Toàn bộ tính hợp lệ được bảo vệ bởi **năm cổng cứng** — mỗi cổng là một phép kiểm phải qua, nếu trượt thì phải thu hẹp claim tương ứng:

| Cổng | Kiểm điều gì | Trạng thái |
|---|---|---|
| **K1** | đo recall của bộ dò/VH (mẫu số có đáng tin không) | cần chạy |
| **KN** | histogram độ dài quy trình (đủ quy trình dài không) | GO |
| **KZ'** | prior-art sắp ảnh (có bị scoop không) | GO |
| **KB** | chống rò rỉ chỉ số bước (strip metadata + tái mã hoá ảnh + che status bar/đồng hồ/pin/badge + loại quy trình 2 ảnh trùng pixel) | cần chạy |
| **K-pair** | đo acc-pairwise thô của VLM vs gold *trước* khi tổng hợp Copeland (sàn > 0,5) | cần chạy khi prototype nhiều màn |

---

# CHƯƠNG 8 — KẾT QUẢ SƠ BỘ (trung thực)

> ⚠️ **[LỖI THỜI — số của khung cũ]** Kết quả ở đây là của **hệ prompting gpt-4o-mini** (~25% bịa, ~19% fallback…). Hướng mới sẽ báo **số của MÔ HÌNH tự train** (kế hoạch M1–M5, **Chương 0 §0.10**). Giữ để tham chiếu *hiện tượng*, KHÔNG phải kết quả cuối.

Luận văn đang ở giai đoạn *đề cương/thiết kế, có kết quả sơ bộ*. Ta báo cáo trung thực, kèm mọi giới hạn — vì báo cáo thổi phồng sẽ vỡ ngay trước một hội đồng đọc kỹ.

**Trên `gpt-4o-mini`, mẫu nhỏ (1 app cũ):**
- **Tỉ lệ ảo giác của bản gốc $\approx \tfrac{1}{4}$ số bước** — con số headline (không phải trị số sau fallback).
- **Bước đối chiếu với giao diện thật nâng độ trung thực ở mọi ngưỡng** $\tau$ — nghĩa là fallback thật sự cắt được tham chiếu bịa.
- **Giá phải trả $\approx 19\%$ số bước** bị hạ thành mô tả khái quát (%fallback).
- **Bộ chấm độc lập cho ~95\%** (không phải 100%) → xác nhận *không tautology*: nếu chấm bằng chính bộ khớp thì đã ra 100%.
- Độ đúng nhãn và định dạng **đứng yên** (no-harm) — bước đối chiếu với giao diện thật không làm hỏng các mặt khác.

> **Khai giới hạn (bắt buộc, không né):** mẫu **nhỏ**, chỉ **một mô hình**, **một app cũ**, và **khoảng tin cậy còn chạm 0** (chưa đủ mạnh để tuyên bố chắc). Bản chính (127 màn / 30 app) **chưa chạy** — cần API. Kế hoạch: **thêm ≥ 1 mô hình frontier 2025–2026 rẻ** (Gemini-2.5-Flash / GPT-4.1-mini) cạnh `gpt-4o-mini`, để báo tỉ lệ ảo giác dưới dạng **đường cong theo đời mô hình**, chứ không cố định một con số "¼" tĩnh. Đây cũng là luận cứ bảo vệ cho câu hỏi "AI 2026 hết bịa" (Chương 9, Phụ lục B): đường cong dự kiến vẫn > 0 ngay cả ở mô hình frontier, và niche *on-device* (chỉ chạy được mô hình nhỏ) luôn cần bước đối chiếu với giao diện thật.

---

# CHƯƠNG 9 — ĐỊNH VỊ & CÔNG TRÌNH LIÊN QUAN (rà soát 2025–2026)

> ⚠️ **[CẦN BỔ SUNG]** Thiếu nhánh liên-quan về **huấn luyện model GUI grounding**: UI-R1 (AAAI 2025), SE-GUI (NeurIPS 2025), GUI-Actor (NeurIPS 2025), ZonUI (WACV 2026) — xem **Chương 0 §0.12** + `report/50`. Phần định vị "sinh hướng dẫn cho người + đánh giá no-gold" vẫn đúng (đó là wedge khác các bài agent).

Một rà soát độ mới trên tài liệu 2025–2026 (đã verify) cho kết luận: đề tài **không lỗi thời và không bị scoop**. Không công trình nào ghép đúng bộ ba *sinh hướng dẫn cho người + neo bằng VH có cấu trúc + đánh giá không gold*. Cần phân định rõ với các công trình gần nhất:

| Công trình | Họ làm gì | Khác biệt của luận văn |
|---|---|---|
| **AskEase** (CHI 2026) — *bài gần nhất, rủi ro novelty CAO nhất* | trợ lý sinh hướng dẫn từng bước cho người dùng trình đọc màn hình; đánh giá bằng user-study 12 người + 45 tác vụ | **ba điểm phân định** (xem dưới) |
| **FaithScore** (Findings EMNLP 2024) — *câu phản biện "thiếu validation" nguy hiểm nhất* | đo faithfulness *reference-free* cho mô hình thị giác, **vẫn** báo human-correlation | **ba điểm phân định** (xem §7.2 + dưới) |
| **LLM-as-Meta-Judge** (preprint 2025) | validate thước đo không cần nhãn người | họ ở miền text; ta ở miền GUI + *bơm lỗi độc lập với matcher* + trụ Sai EMNLP 2021 / BUMP ACL 2023 |

**Phân định AskEase (bắt buộc — giám khảo sẽ hỏi "khác AskEase chỗ nào").** AskEase trùng *trục sinh hướng dẫn cho người*, nhưng khác ba điểm không thể lẫn: (1) **đầu vào** — AskEase là trợ lý *live*, có ngữ cảnh runtime + ý định người dùng đang thao tác; ta sinh từ **ảnh tĩnh + câu hỏi**, không có state runtime; (2) **cách đánh giá** — AskEase dùng *user-study HCI* đo task-success/workload (người hoàn thành được coi như *gold ngầm*); ta dùng **phương pháp no-gold neo bằng cây phân cấp giao diện có cấu trúc**, đo tỉ lệ ảo giác/faithfulness — không có người hoàn thành làm chuẩn; (3) **thành phần** — AskEase **không có** bước đối chiếu với giao diện thật đối chiếu cây giao diện, cũng **không có** nhánh sắp thứ tự màn. ⇒ novelty của cả (A) *bước đối chiếu với giao diện thật* lẫn (B) *phương pháp đánh giá* vẫn còn trống. Ta còn **dùng AskEase để hậu thuẫn niche on-device / trợ năng**, nơi bước đối chiếu với giao diện thật đúng chỗ có giá trị nhất.

**Phân định FaithScore** — xem §7.2 (đã viết đoạn thủ chủ động): ta verify với **cây giao diện cấu trúc + matcher tất định** (≠ FaithScore tự soi lại bằng VLM), và *hạ có chủ đích* human-correlation xuống future-work dưới khung measurement-theory, thay vì bỏ sót.

Các bộ dữ liệu GUI mới (GUI-Odyssey ICCV 2025, AMEX, ScreenSpot-Pro) đều thuộc dòng *agent-control / element-detection* — vai khác hẳn với "sinh hướng dẫn cho người đọc".

> **Hai "hàng xóm gần nhất" phải thừa nhận (R-07, chống nguy cơ trùng lặp):** (1) *"From Task to Tutorial"* (FSE'26, preprint 2509.21816) — sinh tutorial nhưng khác trục đánh giá/đầu vào; (2) một công trình *accessibility bug-report* dùng cơ chế **verify-vs-a11y-tree** (preprint 2603.23828) — cơ chế đối chiếu VH đã xuất hiện ở miền bug-report. ⇒ **Bài học:** ta **neo tính mới vào COMBO đầy đủ** (sinh hướng dẫn cho người + hậu kiểm neo VH + đánh giá no gold), **KHÔNG** neo vào riêng "lớp VH-check" — vì cơ chế verify-vs-VH bản thân đã có tiền lệ. Hai bài này là *preprint* → chỉ *acknowledge*, không ảnh hưởng đậu/rớt.

> **Bằng chứng "ảo giác chưa tự khỏi ở model 2025-26"** (để thủ câu phản biện *"frontier mới hết bịa → bước đối chiếu với giao diện thật thừa"*): trên benchmark grounding khó, mọi thế hệ vẫn xa hoàn hảo (điểm còn dưới 90%); model on-device 3B (Ferret-UI Lite) chỉ ~53% trên ScreenSpot-Pro; và ảo giác phần tử còn *truyền chéo* giữa các họ model. Các nguồn này đều **preprint** → chỉ dùng *định vị landscape / động cơ*, **không** làm trụ đậu/rớt; trụ vẫn là ALOHa (NAACL 2024) + FaithScore (Findings EMNLP 2024). **Hệ quả bắt buộc:** ta phải **tự đo đường cong tỉ lệ ảo giác per-model** trên chính setup (≥1 frontier rẻ 2025-26 cạnh gpt-4o-mini), vì reviewer sẽ phản "số mượn là tác vụ khác".

**Prior-art phải thừa nhận (về sắp ảnh):** Sort-Story (EMNLP 2016, dùng Spearman), Wu et al. (ACL 2022), RankGPT (EMNLP 2023, listwise), và hai bài **bình duyệt mới** về VLM/CLIP so cặp để sắp ảnh: **EZ-Sort (CIKM 2025)** và **Dodgersort (PAKDD 2026)** (cả hai *có human-in-the-loop*, khác ta ở chỗ tự động hoàn toàn lúc suy luận). Độ mới của ta nằm ở: *miền GUI + điều kiện hoá theo mục tiêu + gắn ordering vào sinh hướng dẫn + partial-order suy từ gold + signal-attribution một cue* (đã phát biểu đầy đủ ở §4.4). Ta cũng sẽ **thêm một baseline listwise một shot** (kiểu RankGPT) chấm cùng $\tau$ + Step-SR + cột chi phí, và reframe so cặp như một *substrate-audit* (nền cho stratification một cue + kiểm tính bắc cầu + partial-order-from-gold), viện dẫn VECTOR ("VLM mù thời gian") làm luận cứ cho nhánh nhiều màn + chống rò rỉ.

**Khung neo đánh giá.** Bài neo là Chim, Ive & Liakata (*Computational Linguistics* 51(1):191–233, 2025) — ta kế thừa *khung đánh giá* (Nội tại + Ngoại lai) cho văn bản tổng hợp không đáp án chuẩn, **không** kế thừa bài toán sinh của họ.

---

# CHƯƠNG 10 — ĐÓNG GÓP, GIỚI HẠN, HƯỚNG PHÁT TRIỂN

## 10.1. Hai đóng góp — ngang vai CÓ ĐIỀU KIỆN

> ⚠️ **[LỖI THỜI]** Khung "hai đóng góp ngang vai (A = hệ prompting)" đã đổi → **(A) mô hình grounding tự train, (B) đánh giá no-gold kiêm hàm thưởng**. Xem **Chương 0 §0.8**.

Luận văn có **hai đóng góp đặt ngang vai *có điều kiện***: (A) hệ thống sinh bám sát màn; (B) phương pháp đánh giá không gold. Điều kiện để giữ "ngang vai" là **nhánh nhiều màn (Step-SR) phải cho ra số dương thật** — vì trọng lượng của (A) đến từ *phát hiện thực nghiệm* (đo ảo giác trên nhiều mô hình + đối chứng thất bại + sắp thứ tự nhiều màn + phân tích cue), **không** từ độ phức tạp mã nguồn.

Nếu điều kiện đó chưa được thoả, (A) **vẫn đứng vững** nhờ **ba chân độc lập**:
1. **Đạt mục tiêu thiết kế** — hệ thật sự cắt được tham chiếu bịa.
2. **Đo được tỉ lệ ảo giác gốc + %fallback** — báo cáo trung thực cả cái được lẫn cái giá.
3. **Đối chứng thất bại đo được** — phương án "đoán nút gần nhất" gây silent error, đo trên 10 màn.

Ta **không** tuyên bố ngang vai *vô điều kiện* khi chưa có số, và **không** claim SOTA leaderboard (setup khác về bản chất). Chủ trương "null vẫn đậu" áp cho nhánh (B) và phần đo cơ chế; riêng claim của (A) thì *kỳ vọng dương*.

## 10.2. Giới hạn (khai chủ động)

Khai thẳng giới hạn là một phần của tính khoa học, không phải điểm yếu:
- Nhánh một màn chỉ đo *không ảo giác*, **chưa** đo *đúng ý* → phần *năng lực thao tác từng bước* dồn sang Step-SR ở nhiều màn; còn *"hoàn thành tác vụ tới đích"* cần **task-success-rate riêng** (future-work, §5.5).
- Độ trung thực ~100% sau fallback là **trần thiết kế** → báo cáo tỉ lệ ảo giác gốc thay vì con số đó.
- VH thiếu nhãn → mọi số về ảo giác đều **có điều kiện độ phủ**.
- **Thiên lệch chọn mẫu (`MIN_ACT≥6`):** mẫu một-màn ưu tiên màn nhiều nút có nhãn → tỉ-lệ-bịa quan sát **hạ thấp có hệ thống**; vá bằng báo tỉ-lệ-bịa **phân tầng theo độ-phủ-nhãn** + tầng màn thưa (sensitivity) + khai selection-rate (§5.1, `report/48`).
- **MobileViews thu thập tự động bằng bot** (VLM điều khiển DroidBot) → bot khó vào màn **sau đăng nhập / thanh toán / post-auth**, nên mẫu **thiên lệch phủ** (thiếu các loại màn quan trọng đó) → ta thu hẹp phạm vi claim tương ứng (nối Chen ICSE 2020).
- Máy **không GPU** → giai đoạn đầu chỉ một mô hình, mẫu nhỏ → kế hoạch mở rộng + thêm mô hình frontier.
- **Chưa có bảng số định lượng tiếng Việt** → định lượng chạy trên EN/ZH (dataset chuẩn); tiếng Việt là *demo định tính* + ~120 mẫu app Việt cho chuyên gia. Ta nói rõ điều này với hội đồng.

## 10.3. Hướng phát triển

- Bộ trỏ grounding *độc lập* (GUI-Actor / UI-TARS) thay vì tâm bbox.
- Củng cố cổng đo sàn so cặp (K-pair) và ablation phá vòng.
- Bổ sung 2 test perturbation còn thiếu để đủ 4/4 tiêu chí meta-eval 2025: *bền với diễn đạt lại* và *phân biệt loại lỗi* (§7.2).
- Tự đo **đường cong tỉ lệ ảo giác per-model** trên chính setup (≥1 frontier rẻ 2025-26) — điều kiện chốt để thủ câu phản biện "frontier hết bịa".
- Đường cong ảo giác *đa mô hình* (nhiều đời VLM) làm bằng chứng "niche còn sống ở frontier".
- Nhánh web (Mind2Web) — hiện là future-work vì chỉ có DOM, không bbox.
- Convergent validity với chuẩn độc lập (nâng cấp từ perturbation) — về lâu dài.

---

# CHƯƠNG 11 — BỐI CẢNH THỰC HIỆN: LỘ TRÌNH, MÔI TRƯỜNG, TRẠNG THÁI & VIỆC TIẾP THEO

> ⚠️ **[LỖI THỜI]** Môi trường (máy không-GPU / chỉ-API), trạng thái, và việc-tiếp-theo ở đây thuộc khung cũ. Mới: **huấn luyện trên Colab Pro+ (LoRA 3B, ~$100–150)**; việc tiếp = **Pha 1 dựng code train** (**Chương 0 §0.9–0.10**).

Chương này cho bạn bức tranh *thực tế của dự án* — không phải lý thuyết mà là "đang ở đâu, dựng bằng gì, làm tiếp gì". Đọc xong chương này là biết trọn tình hình.

## 11.1. Lộ trình hai bài báo (một màn trước, nhiều màn sau)

Luận văn được tách thành **hai bài báo** để giảm rủi ro và nộp được sớm:

| Bài | Phạm vi | Ngôn ngữ | Thứ tự | Nội dung |
|---|---|---|---|---|
| **VCL** | **một màn** (nội bộ gọi DG1) | tiếng Việt | **nộp trước** | bước đối chiếu với giao diện thật + đánh giá faithfulness không gold một màn |
| **FAIR** | **nhiều màn** (nội bộ gọi DG2) | tiếng Anh | nộp sau | bước sắp lại thứ tự các màn (Stage-0) + $\tau$ + Step-SR |

> **Quy ước trình bày:** trong slide và khi nói trước hội đồng, **luôn dùng "một màn / nhiều màn"**, *không* dùng "DG1/DG2" (đó chỉ là tên gọi tắt nội bộ). Chi tiết kế hoạch tách bài ở tài liệu kế hoạch riêng; nguyên tắc là **không để hai bài trùng nội dung** và **attribution đúng**.

Vì sao tách? Nhánh một màn đã có kết quả sơ bộ và đủ khép kín để thành một bài hoàn chỉnh; nhánh nhiều màn cần thêm thực nghiệm (cổng K-pair, histogram độ dài quy trình) nên để sau. Cách này cũng khớp trục phân định "có quỹ đạo vàng hay không" (§3).

## 11.2. Môi trường & công cụ hiện thực

- **Máy không có GPU** → mọi VLM *nhìn ảnh* phải gọi **API đám mây**. Mô hình lõi hiện tại: `gpt-4o-mini` (khoá API để ở tệp riêng, không in ra). Kế hoạch thêm ≥1 mô hình frontier rẻ 2025–26 (Gemini-2.5-Flash / GPT-4.1-mini) để có đường cong theo đời mô hình.
- **Chạy cục bộ (miễn phí) qua Ollama:** `nomic-embed-text` (bộ *quyết* khớp/fallback), `bge-m3` (bộ *chấm* độc lập, khác họ), `llama3.2`, `qwen2.5vl:3b/7b`. Việc tách "quyết" và "chấm" sang hai họ embedding là luận cứ bảo vệ chống circularity (§7.1).
- **Nền tảng:** Windows (chạy Python cần đặt mã hoá UTF-8). Bộ mã (*harness*) viết bằng Python, chia module: lọc dữ liệu, sinh baseline + PA2, chấm PA2 (cluster bootstrap + Holm), chấm độc lập bge-m3 + đo silent-error, tải View Hierarchy + point-in-bbox, so khớp ALOHa, sinh câu hỏi.
- **Dữ liệu:** tập `mv_multiapp` lọc rác → bộ chốt **127 màn / 30 app** (`kept_screens_final.json`, 2026-07-06; pilot cũ 81/17 nay đã mở rộng); app suy từ tiền tố tên màn nên *gom cụm theo app* được (G=30 cho cluster bootstrap, §7.4).

## 11.3. Trạng thái hiện tại (2026-07-06)

> *(Tóm tắt nhanh ở hộp "TRẠNG THÁI MỚI NHẤT" đầu tài liệu. Mục này ghi chi tiết.)*

- **Giai đoạn:** đề cương / thiết kế **đã đóng băng**, **đã có kết quả sơ bộ** (Chương 8) + **mẫu dữ liệu 3 bộ đã chốt trong tay** (Ch.3, `report/48_dataset_selection.md`). Thiết kế qua nhiều vòng review → đã **vá circularity** (PA2 + chấm bge-m3 độc lập).
- **Đã qua nhiều vòng research + debate 2026** (chi tiết Chương 12): không lỗi thời, không bị scoop, **không lỗi thiết kế, không cần đổi kiến trúc**; **mẫu dữ liệu cũng qua debate → hợp lý có điều kiện**.
- **Mẫu đã chốt:** MobileViews **127 màn/30 app**; ScreenSpot **501**; AndroidControl **286 ep + 48 ep N dài, 237 app** (`dg2_sample.py`). **Bản chính CHƯA chạy** — cần API.
- **Năm cổng cứng (kill-test):**

| Cổng | Kiểm | Trạng thái |
|---|---|---|
| K1 | recall của bộ dò / VH | cần chạy |
| KN | histogram độ dài quy trình | GO |
| KZ' | prior-art sắp ảnh (scoop?) | GO |
| KB | chống rò rỉ chỉ số bước | cần chạy |
| K-pair | acc so cặp thô > 0,5 | cần chạy khi prototype nhiều màn |

## 11.4. Việc tiếp theo + nguyên tắc chi tiền

**Miễn phí (làm được ngay, không tốn API):**
- Freeze ngưỡng $\tau$ + báo precision/recall của matcher trên tập gán tay 80–120 cặp (precision ≥ 0,95) + Cohen's κ.
- Dựng harness nhiễu loạn (bơm lỗi độc lập matcher) — gồm cả 2 test mới (§7.2).
- Module LLM-judge khác họ generator.
- Tính con số **độ phủ nhãn VH** thật.

**Tốn API (ước tính nhỏ — HỎI Ý BẠN TRƯỚC):**
- Sinh câu hỏi affordance-seeded + cổng answerability; sinh baseline cho 127 màn.
- Thêm ≥1 mô hình frontier để có đường cong ảo giác.

**Kill-test tuần đầu:** K1 (recall) + KN (histogram) + KB (chống rò rỉ) → chốt khung với thầy → hoàn thiện harness → ablation.

> **Nguyên tắc chi tiền (bất biến):** chạy **một lần cho đúng**; **mọi bước tốn tiền phải hỏi trước**; ưu tiên **cục bộ / miễn phí + cache**. Con số hiện tại là *exploratory* cho tới khi hoàn tất pre-registration + chạy chính thức.

---

# CHƯƠNG 12 — TÍNH ĐÚNG THỜI & TỔNG HỢP PHÒNG THỦ (đã kiểm định những gì)

> ⚠️ **[MỘT PHẦN LỖI THỜI]** Các vòng debate ở đây kiểm khung CŨ (prompting). Còn dùng được: luận cứ chống rò rỉ, đánh giá no-gold, độ mới miền GUI. Đã bị thay: mọi phán quyết về "đóng góp A = prompting / không train model" → xem Chương 0.

Chương này trả lời một câu hỏi sống còn cho luận văn 2026: *"đề tài này có lỗi thời, có bị người khác làm mất rồi, có bị hội đồng bác vì sai hướng không?"*. Câu trả lời — sau **tám vòng research độc lập** — là **không**. Dưới đây tổng hợp cả tám để bạn nắm trọn "đã kiểm định gì và kết luận ra sao".

## 12.1. Các vòng research đã chạy

| Vòng | Câu hỏi | Kết luận |
|---|---|---|
| **1. Rà độ mới 2025–2026** | đề tài có lỗi thời / bị scoop không? | **Không.** Không ai ghép đúng combo *sinh hướng dẫn cho người + neo VH cấu trúc + đánh giá no gold*. |
| **2. Deep-research đối kháng** | có lý do gì để reject không? | **Đủ vững nộp 2026, không lỗi thiết kế.** 7 rủi ro R1–R7, đều thủ được — đã vá vào tài liệu. |
| **3. Research riêng kiến trúc pipeline** | pipeline có đúng nhu cầu 2026 không? | **Đúng hướng, KHÔNG cần đổi kiến trúc.** Rủi ro chỉ ở *cách trình bày*, không phải sai paradigm. |
| **4. Verify PIPELINE (đóng góp A) + citation** — đối kháng 3 phiếu | pipeline đủ làm ĐÓNG GÓP thạc sĩ không? | **ĐỦ — có điều kiện.** 7/8 khẳng định vững; A5 (pairwise "tốt hơn/chuẩn") bị bác về *tính tuyệt đối* → đã hạ giọng. 6/6 citation ĐÚNG venue (TOMATO = ICLR 2025 Poster). `report/45` §C. |
| **5. Verify METRIC (đóng góp B)** — đối kháng 3 phiếu | phương pháp đánh giá đủ làm ĐÓNG GÓP thạc sĩ không? | **ĐỦ — có điều kiện (đối xứng A).** 7/8 vững (M5/M7/M8 sống sạch); M6 (Step-SR = "tới đích") bị bác → **reframe = năng lực từng bước**; M3 → thêm **mẫu nhỏ human-validation**. `report/27` §8. |
| **6. Debate BỘ THÍ NGHIỆM (2026-07-06)** — 3 phản biện (thừa/trùng · clarity · thiếu) | bộ thí nghiệm có nhiều/trùng không, trình bày rõ chưa? | **KHÔNG trùng khoa học, KHÔNG lỗi thiết kế** — nhưng phình đếm số → **tái khung ~7 cốt lõi** + E16 + arm VH; vá clarity (PMR Def 5.6, bảng mẫu, ngưỡng số). Ch.13. |
| **7. Debate TOP-TIER (2026-07-06)** — 4 giám khảo (pipeline · metric · thí nghiệm · tổng thể) | có phù hợp chuẩn thạc sĩ trường top? | **ĐẬU CÓ ĐIỀU KIỆN.** Thiết kế đạt chuẩn top, KHÔNG lỗi kiến trúc; **mắt xích yếu nhất = chưa có số** (phải chạy ra ≥1 kết quả dương CI sạch). |
| **8. Debate MẪU DỮ LIỆU (2026-07-06)** — 4 giám khảo (MobileViews · AndroidControl · ScreenSpot+coherence · phương pháp chọn mẫu) | item 3 bộ chọn đã hợp lý chưa? | **HỢP LÝ CÓ ĐIỀU KIỆN.** 3 lỗ CAO = MIN_ACT bias · cắt N≥7 (đã bổ tầng N dài) · ScreenSpot iOS/demote; app-diversity đã vá (96→**237 app**); estimand = **macro-per-app**. `report/48`. |

> **Ghi chú vòng 4+5:** cả hai đóng góp A và B đã qua **cùng một "lò" phản biện 3 phiếu** → "hai đóng góp ngang nhau" **GIỮ ĐƯỢC** (đều "đủ có điều kiện, chờ số DG2 dương"). Mọi điểm bị bác đều là *câu chữ tuyệt đối*, không phải lỗi thiết kế — đã áp vá vào tài liệu này (R-07: A5/A2/A4/A7; R-08: M6/M1/M3/M4/M5). Điều kiện cứng cuối cùng cho cả hai: **ra số thực nghiệm**.

## 12.2. Tổng hợp câu hỏi khó và cách trả lời

| Câu hỏi của hội đồng | Trả lời gọn | Chi tiết |
|---|---|---|
| "Sao không grounded-gen (đưa cây giao diện vào lúc sinh) như AskEase?" | Sinh mù = **thiết bị ĐO**, không phải kiến trúc triển khai; grounded-gen làm *hỏng phép đo* (model chép → ảo giác bị *che/nhiễu* trong phép đo) | §4.5 |
| "AI 2026 hết bịa → bước đối chiếu với giao diện thật thừa?" | Báo **đường cong per-model** vẫn > 0 ở frontier; niche on-device (model nhỏ) luôn cần | §8, §9 |
| "Metric reference-free vẫn phải có human-correlation (FaithScore)?" | Ta neo **VH cấu trúc + matcher tất định** (≠ self-check VLM); hạ human xuống future-work dưới khung *measurement-theory* | §7.2 |
| "Khối sắp màn chỉ ghép đồ có sẵn?" | Độ mới ở **tổ hợp 5 điểm**, không ở thuật toán lõi; trích đủ prior-art | §4.4 |
| "Grounding tautology? / tolerance 14% lỗi thời?" | Đã bỏ khỏi headline một màn; chuẩn 2026 = **point-in-GT-bbox**, 14% chỉ là biến thể | §5.3 |
| "Perturbation đủ chưa?" | Paradigm meta-eval bình duyệt (BUMP ACL23 + Sai); đủ **4 tiêu chí**; human-eval bản thân agreement thấp | §7.2 |
| "Long-context nuốt module sắp cặp?" | VLM xử lý ảnh kiểu "bag-of-frames" (TOMATO ICLR25 Poster; GPT-4o ~24% vs người ~80% khi sắp ảnh) → Stage-0 là *scaffold có cấu trúc*, không phải long-context "bất lực tuyệt đối". Pairwise hơn listwise *ở model tầm trung* (Qin, Findings NAACL 2024) | §4.3, §4.4 |
| "Gộp vào 'tự sửa đã bị bác' (Huang ICLR24)?" | Ta dùng tín hiệu **NGOÀI, phi-LLM, tất định** → đúng nhánh *được* chứng minh hợp lệ | §4.5 |
| "Chỉ ghép đồ có sẵn (cả pipeline)?" | Đóng góp ở **phát hiện thực nghiệm + phương pháp đánh giá** — cùng loại G-Eval/FActScore/RAGAS | §10.1 |

## 12.3. Phán quyết tổng & điều kiện đậu

> **PHÁN QUYẾT (tổng tám vòng):** thiết kế **đủ vững để nộp 2026, không có lỗi thiết kế, không cần đổi pipeline hay metric**. Rủi ro còn lại đều là *cách trình bày* — đã vá ngay trong tài liệu này.

**Ba việc "phải làm" để hiện thực hoá (không đụng kiến trúc):**
1. **Đóng khung** — in rõ mục 4.5 (Đo vs Triển khai) + các đoạn phân định (đã có trong tài liệu).
2. **Cổng K-pair** — đo acc so cặp thô > 0,5 *trước* khi tổng hợp Copeland (điều kiện sống còn của nhánh nhiều màn).
3. **Baseline listwise** một shot + cột chi phí (đã có trong kế hoạch).

**Lưới an toàn (vì sao không sợ số xấu):** nhánh đánh giá theo chủ trương **"null vẫn đậu"** (kết quả không khác biệt vẫn là đóng góp hợp lệ, đã pre-register); đóng góp hệ thống đứng trên **ba chân** (đạt mục tiêu + đo được tỉ lệ bịa/%fallback + đối chứng thất bại) không phụ thuộc con số phải dương. Rủi ro thực nghiệm thật duy nhất là cổng K-pair — nếu VLM so cặp ~0,5 thì khai thẳng "Stage-0 không kết luận cho model đó", nhánh một màn + đánh giá vẫn đứng.

> **Kỷ luật nguồn:** các bằng chứng *preprint* (HalluClear, Ferret-UI Lite, ScreenSpot-Pro, UI-TARS, GUI-Actor, A11y-Compressor…) chỉ dùng **định vị landscape / minh hoạ trend**, **không** làm trụ đậu/rớt. Trụ đậu/rớt chỉ xây trên nguồn *đã bình duyệt* (Phụ lục C).

---

# CHƯƠNG 13 — THIẾT KẾ THÍ NGHIỆM (chứng minh hai đóng góp)

> ⚠️ **[LỖI THỜI phần lớn — thay bằng M1–M5]** Bộ E1–E16 thiết kế cho hệ prompting. Kế hoạch TN MỚI cho MÔ HÌNH = **Chương 0 §0.10 (M1–M5)**. VẪN tái dùng: **E4–E7** (validate thước đo bằng perturbation + so matcher với người) — vì thước đo giờ kiêm hàm thưởng, càng cần validate.

> Chương này là **kế hoạch chứng minh**: mỗi đóng góp gắn với các câu hỏi nghiên cứu (RQ), mỗi RQ gắn với thí nghiệm cụ thể (dataset + cỡ mẫu + thước đo + baseline/ablation + cổng). Cỡ mẫu neo vào chuẩn ngành (Chương 11 §11.4 + research cỡ mẫu). **Bản đầy đủ** (bảng neo nguồn 30+ paper, ghi chú thống kê chi tiết) ở `report/47`.
> Nguyên tắc xuyên suốt: mọi số kèm **CI bootstrap 95% cluster theo app**; so 2 hệ dùng **paired test**; **pre-register ngưỡng trước khi nhìn kết quả**; **không** claim SOTA; human-correlation = future-work.

> **ĐỌC TRƯỚC — "15 thí nghiệm" nghe nhiều, nhưng đếm trung thực chỉ **~7 thí nghiệm THẬT**.** Danh sách E1–E16 là *cách đánh số để trích chéo*, KHÔNG phải 15–16 việc ngang nhau.
> - **~7 THÍ NGHIỆM CỐT LÕI (bắt buộc):**
> 1. **E1+E2 = MỘT lần chạy, hai readout** — chung bản sinh BASE trên MobileViews. **E1** = readout *lớp kiểm TẮT, đa model* (đường cong bịa per-model); **E2** = readout *bật/tắt lớp kiểm* (Δfaithfulness + %fallback + no-harm). Không phải hai thí nghiệm rời — một run, hai lát cắt. *(Lõi A.)*
> 2. **E3** — đối chứng silent-error ("chỉ mô tả" vs "đoán nút"): *biến A thành research*.
> 3. **E4** — validate metric bằng perturbation: *trục chính B*.
> 4. **E5** — validate matcher vs người (P/R + κ).
> 5. **E8 (+cổng E9)** — sắp thứ tự màn (sàn / pairwise / listwise).
> 6. **E14** — Step-SR (nhiều màn).
> 7. **E6** — anti-circularity: chấm bằng **3 cơ chế khác họ** generator (điều kiện để số faithfulness hợp lệ). *(Lõi B — thuộc giao thức chấm §5.4 nhưng là một chân bắt buộc, xem §13.5.)*
> - **KHÔNG phải thí nghiệm riêng (mục con / cổng / nên-có):**
> - **E16** *(nên có, KHÔNG bắt buộc)* = kiểm hữu ích định tính với người đọc (lấp trục "faithfulness ≠ usefulness") — rẻ và thủ được câu hỏi giám khảo, nhưng không phải chân đóng góp bắt buộc (§13.5).
> - **E9** = *cổng K-pair* — if-check điều kiện tiên quyết của E8 (nếu so cặp ≈0,5 thì dừng Stage-0).
> - **CONTINGENT (chỉ chạy khi cần, KHÔNG upfront):**
> - **E10–E13** = *một gói* ablation mổ xẻ Stage-0 (Copeland / min-FAS / position-bias / cue). Chạy **nếu** nhánh nhiều màn cho số dương (để quy công từng khối) **hoặc nếu** ra số âm (để biến "số xấu" thành *phát hiện có cấu trúc* về giới hạn VLM sắp thời gian). Ưu tiên cue-analysis + intransitivity-audit.
> - **TUỲ CHỌN / bù độ tin cậy:** E7 (neo người judge, KHÔNG cổng) · E15 (đối chứng grounding — cần bộ trỏ độc lập, máy không GPU khó chạy → dễ hoãn nhất).
>
> → Khối lượng thật = **~7 việc chính + 1 gói contingent + vài tuỳ chọn**, KHÔNG phải "15 việc". Mỗi E vẫn đo một trục riêng (không trùng khoa học — ma trận claim↔E ở `report/47`); cách đánh số gộp lại để hội đồng không đọc nhầm thành "16 việc ngang nhau".

## 13.1. Khung câu hỏi nghiên cứu (RQ)

- **RQ1 — Đo hiện tượng (đóng góp A):** VLM sinh mù bịa nút không tồn tại với tần suất bao nhiêu, và biến thiên thế nào **giữa các đời model**? → báo *đường cong per-model*, không headline "¼" tĩnh.
- **RQ2 — Bước đối chiếu với giao diện thật có giúp ích không & giá bao nhiêu? (A, lõi):** BASE vs BASE+kiểm trên **cùng generator** → faithfulness ↑? %fallback? có hại chỉ số phụ không? *(RQ2b: đối chứng "chỉ mô tả" vs "đoán nút gần nhất" → đo silent-error.)*
- **RQ3 — Phương pháp đánh giá no-gold có HỢP LỆ không? (đóng góp B, lõi):** metric có nhạy với lỗi (perturbation), tách bản lỗi/bản đúng, không tự chấm vòng tròn, khớp người ở mức tối thiểu?
- **RQ4 — Hệ sắp thứ tự màn có đúng không? (A, nhiều màn):** Stage-0 > sàn ngẫu nhiên? ≈/> baseline listwise? từng khối (Copeland/min-FAS/chống position-bias) đóng góp bao nhiêu?
- **RQ5 — Năng lực từng bước thật? (điều kiện giữ "A ngang B"):** Step-SR teacher-forced ra số dương thật không?
- **RQ6 — Grounding đối chứng:** bộ trỏ *độc lập* trúng khung nút ở tỉ lệ nào (tách text/icon)?
- **RQ7 — Hữu ích thực với người đọc? (MỚI, định tính):** bản có bước đối chiếu với giao diện thật (kèm mô tả fallback) có *làm theo được* không kém bản gốc? → kiểm định tính nhỏ, **KHÔNG** làm cổng đậu/rớt (human-agreement vốn thấp).

## 13.2. Bảng thí nghiệm tổng (E1–E16)

| # | RQ | Thí nghiệm | Dataset + cỡ mẫu | Thước đo | Baseline / Ablation | Cổng | Kỳ vọng |
|---|---|---|---|---|---|---|---|
| **E1** | RQ1 | Đo tỉ lệ bịa thô, **đường cong per-model** *(readout lớp kiểm TẮT của run E2)* | MobileViews **127 màn/30 app** *(ĐÃ CÓ — `kept_screens_final.json`)*; **≥2 model** (gpt-4o-mini + ≥1 frontier rẻ) | faithfulness (per-step) | so giữa model | K1, M4 | frontier vẫn bịa **≥5%** (cận dưới CI >0) |
| **E2** | RQ2 | Toggle lớp kiểm BASE vs BASE+kiểm, **cùng generator**, quét τ; **+ arm "nạp VH lúc sinh"** (đo leakage nội bộ) | MobileViews **127 màn/30 app** *(đã có)* | faithfulness before/after + **%fallback** + no-harm; **Δbịa khi nạp VH** | ablation on/off; quét τ; **arm grounded-gen** | M4, pre-reg τ | faith ↑ mọi τ; %fallback ~19%; phụ đứng yên; **nạp VH làm bịa tụt mạnh → chứng minh vì sao phải sinh mù** |
| **E3** | RQ2b | **Đối chứng thất bại:** "chỉ mô tả" vs "đoán nút gần nhất" | **toàn mẫu E2** (KHÔNG chỉ 10 màn) + báo CI | **silent-error-rate** (định nghĩa ở chú giải dưới bảng) | ablation 2 nhánh | — | nhánh đoán tạo silent-error **>0, CI dưới >0** |
| **E4** | RQ3a | **Perturbation harness:** bơm 10–15 loại lỗi × ≥30 mẫu | MobileViews subset + bản sinh | detection + false-positive + đơn điệu | breakdown per loại lỗi | — | metric tụt đúng hướng; **FP <5%; đơn điệu Spearman ρ>0,8** |
| **E5** | RQ3b | **Validate matcher** vs người | 80–120 cặp gán tay | Precision/Recall + Cohen κ | so matcher nomic τA | — | P≥0.95; freeze τ trước khi chạy |
| **E6** | RQ3c | **Anti-circularity:** 3 cơ chế chấm | bản sinh E2 | đồng thuận bge-m3 + judge khác họ + token-overlap | quyết(nomic) tách chấm | — | 3 cơ chế đồng thuận |
| **E7** | RQ3d | Neo người cho LLM-judge | 100–200 cặp | κ judge vs người | — | — | κ đủ "điều kiện cần" (không cổng) |
| **E8** | RQ4a | **Sàn + đối kiến:** random vs Pairwise+Copeland vs Listwise-1-shot | AndroidControl **286 ep** (`dg2_episodes.json`, nguồn smolagents test=3.051; N∈{4,5,6} KN PASS; **237 app/1 unknown** re-scan goal+open_app, 194 singleton; cắt N≥7 → bổ 1 tầng N dài báo đường cong τ/N) | τ(partial) + pairwise-acc + PMR + **cột chi phí** | 3 hệ cùng thước | KN, KB, K-pair | ta > random (CI tách); **≈ listwise = |Δτ|≤0,05**; hoặc > |
| **E9** *(cổng, không phải TN riêng)* | RQ4b | **Cổng K-pair:** acc-pairwise thô vs gold — *if-check của E8* | cùng E8 | accuracy-pairwise | sàn 0,5 | **K-pair** | >0,5 (nếu ~0,5 → khai Stage-0 vô hiệu) |
| **E10–E13** *(1 GÓI ablation, nếu còn thời gian)* | RQ4c-f | Mổ xẻ Stage-0: tổng hợp (Copeland/Borda) · phá vòng (min-FAS/ngây thơ) · position-bias · cue-analysis 1-cue | cùng E8, phân tầng | τ/PMR + intransitivity + pairwise-acc per-cue | ablation từng khối | — | mỗi khối/cue biện minh được |
| **E14** | RQ5 | **Step-SR** teacher-forced | AndroidControl — lớp-chuẩn Step-SR **giữ N=1** (random-500, protocol Li 2024), tách khỏi 286 ep core N∈{4,5,6} | Step-SR (đúng loại ∧ ≤14%) | phân tầng theo N | KB | số **dương** thật |
| **E15** | RQ6 | **Grounding đối chứng**, (x,y) từ bộ trỏ **độc lập** | ScreenSpot-v2 **501 mobile** | **point-in-GT-bbox nguyên bản** (native), tách text/icon; @14% chỉ là biến-thể đối-chứng phụ | so ScreenSpot | — | trong khung (không lấy tâm bbox) |
| **E16** *(MỚI — nên có)* | RQ7 | **Kiểm hữu ích định tính:** ~3–5 người đọc thử ~10 hướng dẫn | bản sinh E2 (một màn) | *làm theo được?* (Likert 1–5) + ghi chú định tính | so BASE vs BASE+kiểm | — | mô tả fallback **không** giảm khả năng làm theo |

*Thống kê chung: paired **approximate-randomization** (chính) + paired-bootstrap 10k (phụ); **wild-cluster bootstrap-t** — cụm theo app **G=30 danh nghĩa nhưng G_eff-Kish≈24 (một màn) / G=237 app (nhiều màn, 194 app singleton → báo N_eff thật)**; caveat G<42 **chỉ áp cho nhánh một-màn** (G_eff≈24<42) — nhánh nhiều-màn 237 app đã vượt 42; **Holm** đa metric; khai **power/MDE** + **N_eff** (một màn m̄≈4,2), kết quả không ý nghĩa trình bày như **null hợp lệ** (không kết luận "bằng nhau").*

> **Chú giải thước đo & thuật ngữ thống kê trong bảng (định nghĩa tại chỗ — vì đây là chương thiết kế phải tự đủ).**
> - **PMR (Perfect Match Rate)** — tỉ lệ *episode được sắp ĐÚNG TRỌN thứ tự bắt buộc* (mọi cặp bắt buộc đều đúng). Bù cho τ: τ đo *mức* đúng trên từng cặp, PMR đo *tỉ lệ episode hoàn hảo*. VD 100 episode, 42 đúng trọn → PMR = 42%. *(Định nghĩa hình thức: xem Def. 5.6 — thêm cạnh τ ở Chương 5.)*
> - **silent-error-rate** — trong nhánh "đoán nút gần nhất": (số bước bịa bị thay bằng *nút có thật nhưng sai chức năng*) / (số bước bịa được xử lý). Đây là lỗi *bị che*, khác fallback (lộ ra là mô tả). VD 30 bước bịa, nhánh đoán tạo 6 nút sai âm thầm → 20%.
> - **N_eff (cỡ mẫu hiệu dụng)** — cỡ mẫu sau khi trừ tương quan trong cụm app: $N_{\text{eff}} \approx N/(1+(\bar m-1)\cdot \text{ICC})$, $\bar m$ = số màn trung bình mỗi app. Một màn $\bar m\approx4,2$ nên $N_{\text{eff}}$ < số màn thô.
> - **wild-cluster bootstrap-t** — cách tính CI/kiểm định khi **ít cụm** (G nhỏ): tái chọn mẫu ở cấp *cụm app* + lật dấu phần dư (Cameron-Gelbach-Miller 2008), tránh CI hẹp giả tạo khi G<42.
> - **approximate-randomization (paired)** — kiểm định hoán vị: xáo nhãn hệ A/hệ B trên từng cặp nhiều lần, đếm tần suất chênh lệch ≥ quan sát → p-value, **không** giả định phân phối.
> - **MDE (Minimum Detectable Effect)** — hiệu ứng nhỏ nhất mà cỡ mẫu hiện tại đủ sức phát hiện ở power cho trước; báo MDE để đọc "null" cho đúng (không kết luận "bằng nhau" khi chỉ là thiếu power).
>
> **Ngưỡng đậu/rớt (pre-register TRƯỚC khi nhìn kết quả — số dự kiến, chốt ở `report/22`):** E1 bịa ≥5% & CI dưới>0 · E4 FP<5% + đơn điệu ρ>0,8 · E5 P≥0,95 & κ≥0,6 · E8 ta>random (CI tách) và ≈listwise nghĩa |Δτ|≤0,05 · E9 acc-pairwise>0,5 (CI dưới) · E14 Step-SR CI dưới>0.
>
> **Chú thích cỡ mẫu (cập nhật 2026-07-06):** bộ MobileViews đã curated hiện là **127 màn/30 app** (`kept_screens_final.json`) — **đã có trong tay**, khớp đúng cỡ mục tiêu pre-register (research cỡ mẫu §11.4) và m̄≈4,2. Con số **81 màn/17 app** là *mốc pilot 2026-07-01* (đã lỗi thời, nay mở rộng thêm 13 app). Mọi bảng kết quả ghi rõ **cỡ thực tế đã chạy**.

### 13.2b. Giải thích từng thí nghiệm bằng lời thường (mỗi cái CHỨNG MINH điều gì)

Bảng trên viết cô đọng; dưới đây nói rõ **mỗi thí nghiệm trả lời câu hỏi gì bằng ngôn ngữ đời thường**:

- **E1 — "AI bịa nhiều hay ít, và AI mới có bớt bịa không?"** Cho ≥2 model (một cũ, một frontier mới) sinh hướng dẫn mù, đo tỉ lệ bịa mỗi model → vẽ *đường cong*. Chứng minh: vấn đề có thật, và **chưa tự khỏi** ở model mới.
- **E2 — "Lớp kiểm của mình có giúp ích không, giá bao nhiêu?"** Cùng một AI, so *trước* và *sau* khi bật bước đối chiếu với giao diện thật: bịa có giảm không, và bao nhiêu bước bị hạ thành mô tả (%fallback). Đây là **lõi đóng góp A**. *(Thêm **arm "nạp VH lúc sinh"**: cho AI nhìn luôn danh sách nút rồi đo bịa tụt bao nhiêu — chứng minh **trên chính data của ta** rằng nạp VH lúc sinh làm ảo giác bị che, nên phải sinh mù mới đo được; biến lập luận §4.5 từ số mượn ngoài thành bằng chứng nội bộ.)*
- **E3 — "Vì sao chọn 'chỉ mô tả' thay vì 'đoán nút gần nhất'?"** Chạy song song hai cách xử lý bước bịa; đếm số *lỗi âm thầm* mà cách "đoán nút" gây ra. Chứng minh: cách đoán nguy hiểm → cách của mình đúng. Đây là **phát hiện biến A thành nghiên cứu**.
- **E4 — "Làm sao tin thước đo của mình?"** Cố ý bơm lỗi đã biết (thêm nút ma, đổi tên, xáo thứ tự…) rồi xem thước có phản ứng đúng không. Giống *thử máy báo khói bằng cách tạo khói*. Đây là **cách chính** để chứng minh metric đáng tin (thay chấm người).
- **E5 — "Bộ khớp tên nút có chính xác không?"** Gán tay 80–120 cặp rồi so với máy → báo precision/recall + độ đồng thuận. Đây là điều kiện để **mọi con số bịa** có nghĩa.
- **E6 — "Có tự chấm mình không?"** Chấm bằng 3 công cụ khác nhau (khác họ với AI sinh) rồi xem chúng có đồng thuận không. Chống bẫy "vừa đá bóng vừa thổi còi".
- **E7 — "Bộ chấm AI có giống người không?"** (nice-to-have) So AI-judge với người trên ~100 cặp — chỉ để tham khảo, **không** làm cổng đậu/rớt.
- **E8–E9 — "Hệ sắp thứ tự màn có đúng không?"** Xáo N màn của một quy trình, cho hệ sắp lại, so với thứ tự đúng (τ). So 3 cách: đoán mò (sàn) / cách của mình (so cặp + Copeland) / cách "sắp một lần" (listwise). **E9 (cổng K-pair)** kiểm điều kiện tiên quyết: nếu AI so cặp chỉ đúng ~50% (bằng đoán mò) thì cả nhánh này vô hiệu → khai thẳng.
- **E10–E13 — "Từng bộ phận của bước sắp lại thứ tự các màn đóng góp bao nhiêu?"** Tắt/bật từng khối (Copeland, phá vòng, chống thiên lệch vị trí, phân tích tín hiệu) để biết cái nào thực sự giúp.
- **E14 — "Hệ làm đúng thao tác từng bước ở mức nào?"** Đặt hệ vào đúng trạng thái mỗi bước rồi hỏi bước kế → Step-SR. *(Nhớ: đây là năng lực từng bước, không phải "hoàn thành tác vụ" — §5.5.)*
- **E15 — "Chỉ đúng chỗ bấm không?"** (đối chứng) Dùng ScreenSpot-v2 có toạ độ chuẩn để kiểm bộ trỏ, tránh tự lừa bằng cách lấy tâm khung nút.
- **E16 — "Hướng dẫn có thực sự DÙNG ĐƯỢC không?"** *(MỚI, định tính)* Đưa ~10 hướng dẫn (bản gốc vs bản có bước đối chiếu với giao diện thật) cho ~3–5 người đọc thử làm theo, chấm *làm theo được* (Likert) + ghi chú. Trả lời câu hỏi giám khảo "faithfulness cao chưa chắc hữu ích" mà đối thủ AskEase (CHI 2026) đang chiếm. **KHÔNG** làm cổng đậu/rớt (mẫu nhỏ, chỉ để không trống trục "giá trị thực").

## 13.3. Thứ tự chạy (free trước → API sau; cổng chặn gì)

- **GĐ0 — Pre-register (free):** commit `report/22` (ngưỡng, seed, τ dự kiến) **trước** khi nhìn kết quả.
- **GĐ1 — Cổng cứng free (Ollama local, không API):** K1 (recall detector) · M4 (`dg1_vh_coverage.py`) · KN (histogram N, GO) · KZ' (GO) · KB (chống leak) · dựng perturbation harness (E4) + gán tay 80–120 cặp (E5) + judge khác họ (E6/E7).
- **GĐ2 — API tối thiểu (mỗi bước HỎI USER):** sinh câu hỏi → BASE 127 màn (E1/E2) → nhánh PA2 + đối chứng "đoán nút" (E3) → **K-pair (E9)** → *nếu GO*: E8/E10–E13 → E14 Step-SR → E15 grounding.
- **Cổng chặn:** K1→E1/E2 · M4→*cách báo* E1/E2 · KN→phân tầng E8/E14 · KB→E8/E14 · **K-pair→toàn bộ Stage-0 (E8–E13)**. K-pair fail ⇒ nhánh nhiều màn thành *phát hiện âm tính hợp lệ*, vẫn nộp.

## 13.4. Bảng & hình trong luận văn
**Bảng:** T1 đặc tả 3 dataset · T2 bịa per-model · T3 hiệu quả lớp kiểm (before/after×τ+%fallback+no-harm) · T4 silent-error · T5 perturbation · T6 matcher P/R+κ · T7 anti-circularity · T8 sắp thứ tự×N (3 hệ+chi phí) · T9 ablation Stage-0 · T10 cue · T11 Step SR×N · T12 grounding.
**Hình:** F1 sơ đồ pipeline · F2 đường cong bịa per model · F3 trade-off faith↑/%fallback · F4 perturbation đơn điệu · F5 τ theo N · F6 intransitivity+min-FAS · F7 bar-per-cue · F8 ví dụ định tính đầu cuối.

**Ánh xạ RQ → E → Bảng/Hình (nối trọn mạch):** RQ1→E1→T2/F2 · RQ2→E2→T3/F3 · RQ2b→E3→T4 · RQ3a→E4→T5/F4 · RQ3b→E5→T6 · RQ3c→E6→T7 · RQ3d→E7→(gộp T7) · RQ4→E8+E9→T8/F5, E10–E13→T9/T10/F6/F7 · RQ5→E14→T11 · RQ6→E15→T12 · RQ7→E16→(bảng Likert nhỏ).

**Bảng mẫu (shell — dòng số là *giả* để hình dung đầu ra, ô `[—]` = điền sau khi chạy):**

*T3 — Hiệu quả lớp kiểm (một màn):*

| Model | τ | Faith trước | Faith sau | %fallback | Label-fid Δ | No-harm? |
|---|---|---|---|---|---|---|
| gpt-4o-mini | 0,55 | 0,74 | *[—]* | 19% | ≈0 | ✓ |
| *frontier rẻ* | 0,55 | *[—]* | *[—]* | *[—]* | ≈0 | ✓ |

*T8 — Sắp thứ tự màn theo N (nhiều màn), 3 hệ + cột chi phí:*

| N | Hệ | τ(partial) | pairwise-acc | PMR | Chi phí (lượt gọi/ep) |
|---|---|---|---|---|---|
| 5 | random (sàn) | 0,00 | 0,50 | *[—]* | 0 |
| 5 | Pairwise+Copeland (ta) | *[—]* | *[—]* | *[—]* | ~10 |
| 5 | Listwise-1-shot | *[—]* | *[—]* | *[—]* | 1 |

## 13.5. Phân định THẠC SĨ vs PAPER (cái gì bắt buộc)

**BẮT BUỘC cho thạc sĩ** (mỗi cái = một chân đóng góp): **E2** (lõi A) · **E3** (silent-error → biến A thành research) · **E1 với ≥2 model** (vá câu phản biện "neo 1 model cũ") · **E4** (trục validate B) · **E5** (điều kiện để số faithfulness hợp lệ) · **E6** (anti-circularity) · **E8+E9** (sắp thứ tự + K-pair) · **E14** (Step-SR) · toàn bộ khung thống kê.

**NÊN CÓ (rẻ, thủ câu hỏi giám khảo mạnh):** **E16** (kiểm hữu ích định tính — lấp trục usefulness) · **arm "nạp VH lúc sinh"** trong E2 (đo leakage nội bộ, thuần code) · **inter-annotator κ người người** cho E5 (≥2 người trên subset, để nhãn vàng có độ tin cậy trước khi làm chuẩn cho matcher — CLAUDE.md: κ TỰ ĐO, không mượn 0.801).

**CONTINGENT (chạy khi nhánh nhiều màn CÓ kết quả):** **E10–E13** — chạy để *quy công từng khối* (nếu dương) hoặc *biến số âm thành phát hiện có cấu trúc* về giới hạn VLM sắp thời gian (nếu âm); ưu tiên cue-analysis + intransitivity-audit. **Đây là đường lui khoa học khi số âm**, nên KHÔNG để hẳn ở "tuỳ chọn".

**Nếu còn thời gian/ngân sách:** E7 (neo người) · mở rộng 127→150+ màn · E15 grounding (cần bộ trỏ độc lập, máy không GPU khó chạy) · model thứ 3 (Qwen mở) · demo tiếng Việt định tính (~120 mẫu app VN — **không** có bảng số VN định lượng, nói rõ với thầy).

> **Điều kiện then chốt giữ "hai đóng góp ngang nhau":** **K-pair GO + Step-SR/τ dương thật (E9/E14)**. Nếu âm → khai thẳng như *phát hiện hợp lệ*, không che. Đây là rủi ro thực nghiệm thật duy nhất còn lại của toàn luận văn.

---

# PHỤ LỤC A — BẢNG THUẬT NGỮ ĐẦY ĐỦ

| Thuật ngữ | Nói nôm na | Ví dụ |
|---|---|---|
| VLM | AI vừa nhìn ảnh vừa viết chữ | ChatGPT xem được ảnh |
| Ảo giác (hallucination) | AI nói ra thứ không có thật | "bấm Cài đặt" khi màn không có |
| VH / bảng kê nút | danh sách nút thật của một màn | {hour, minute, PM, OK, Cancel} |
| Quỹ đạo vàng | chuỗi thao tác đúng chuẩn có sẵn | click(1016,866)→scroll(down)→… |
| Embedding | biến chữ thành dãy số để so nghĩa | "Lưu" ≈ "Save" |
| Độ tương đồng (similarity) | số 0→1 đo mức gần nghĩa | 0,7 = gần |
| Ngưỡng τ | lằn ranh cùng nút / ảo giác | 0,55 |
| Matcher | bộ khớp tên nút bằng embedding | `nomic` (quyết), `bge-m3` (chấm) |
| Fallback | thay bịa bằng mô tả chung, không đoán nút | — |
| Silent error | sửa thành nút thật nhưng sai chức năng | Submit → Save |
| Copeland | xếp hạng bằng đếm số trận thắng | — |
| Feedback arc set | phá vòng mâu thuẫn bằng loại ít cạnh nhất | — |
| Bounding box | khung chữ nhật của nút (l,t,r,b) | (100, 850, 200, 900) |
| point-in-bbox | điểm bấm có nằm trong khung chuẩn không | point-in-GT-bbox (14% = biến thể đối chứng) |
| τ thứ tự bộ phận | điểm sắp đúng thứ tự, chỉ phạt cặp bắt buộc | +0,33 |
| Step-SR | tỉ lệ bước làm đúng so gold | 4/5 = 80% |
| Perturbation | bơm lỗi đã biết để thử thước đo | chèn nút ma |
| Circularity | bẫy "vừa ra đề vừa chấm" | matcher tự chấm mình |
| Data leakage | lộ đáp án cho mô hình ở thì sinh | đưa VH lúc sinh |
| Cluster bootstrap | tính sai số theo cụm app | G=30 app (một màn) |
| Pre-registration | ghi ngưỡng trước khi xem kết quả | commit report/22 |
| Peer-reviewed | bài đã được chuyên gia bình duyệt | ACL, NeurIPS, ICLR |
| PMR (Perfect Match Rate) | tỉ lệ episode sắp ĐÚNG TRỌN thứ tự | 42/100 = 42% |
| silent-error-rate | tỉ lệ bước bịa bị thay bằng nút thật sai chức năng | 6/30 = 20% |
| N_eff | cỡ mẫu hiệu dụng sau khi trừ tương quan cụm app | 127 màn → N_eff < 127 |
| wild-cluster bootstrap-t | CI/kiểm định khi ít cụm app (G nhỏ) | G=30<42 (một màn) → dùng cái này |
| approximate-randomization | kiểm định hoán vị theo cặp, không giả định phân phối | p từ xáo nhãn A/B |
| MDE | hiệu ứng nhỏ nhất cỡ mẫu đủ sức phát hiện | để đọc "null" cho đúng |

# PHỤ LỤC B — HỎI–ĐÁP GIÁM KHẢO (21 câu, chuẩn bị sẵn)

| Câu hỏi giám khảo | Gợi ý trả lời |
|---|---|
| "Kết quả đâu? hai đóng góp ngang nhau thật à?" | Ngang vai **có điều kiện**; nhánh một màn đã có số sơ bộ, nhánh nhiều màn đang chạy. Nếu chưa có số nhiều màn, (A) vẫn đứng bằng ba chân: đạt mục tiêu + đo được ảo giác/fallback + đối chứng thất bại silent-error. |
| "Sao không đưa luôn VH cho AI cho đỡ bịa?" | Vì cần *đo* mức AI tự bịa; đưa VH thì nó chép, ta hết đo được. VH chỉ vào lúc chấm (luật vàng). |
| "VH thiếu nút thì AI bị oan?" | Có, nên ta đo *độ phủ nhãn*, loại nút không tên (như "Image"), và báo mọi số "có điều kiện độ phủ". |
| "Matcher chính xác cỡ nào?" | Gán tay 80–120 cặp → báo precision + Cohen's κ, freeze ngưỡng; headline được thiết kế *độc lập với ngưỡng cụ thể*. |
| "Grounding là tautology?" | Đúng nếu lấy tâm bbox — nên đã **bỏ khỏi một màn**; chỉ dùng ở nhiều màn / ScreenSpot với bộ trỏ *độc lập*. |
| "AI này đời cũ; AI 2026 hết bịa thì hệ thừa?" | Ta báo ảo giác trên **nhiều đời AI kể cả mới nhất** — đường cong vẫn > 0; và *on-device* chỉ chạy được AI nhỏ nên luôn cần bước đối chiếu với giao diện thật. |
| "Chỉ ghép đồ có sẵn chứ gì?" | Đóng góp nằm ở **phát hiện thực nghiệm + phương pháp đánh giá** — cùng loại đóng góp như G-Eval / FActScore / RAGAS. |
| "Long-context làm sắp cặp thành thừa?" | So cặp cho *dấu vết kiểm tra* + bắt mâu thuẫn nội tại; và VLM long-context "mù thời gian" (VECTOR 2025) nên không tự sắp đúng. |
| "Bị FaithScore / AskEase / Meta-Judge bao trùm?" | Không cái nào đối chiếu **VH có cấu trúc bằng matcher tất định** ở miền GUI no-gold. AskEase (gần nhất) khác 3 điểm: ảnh tĩnh vs live · no-gold vs user-study · có bước đối chiếu với giao diện thật + sắp màn. FaithScore tự soi bằng VLM (chính nó cần validate). Niche còn trống. |
| "Perturbation đã đủ để tin thước đo chưa?" | Là paradigm meta-eval bình duyệt (Sai EMNLP21 + **BUMP ACL23**). Đủ **4 tiêu chí**: nhạy · đơn điệu · bền với diễn đạt lại · phân biệt loại lỗi. Đóng khung *measurement-theory*: đây là 1 mặt hợp lệ; human-correlation = future-work (bản thân human-eval agreement thấp). **Không** lấy AI tự chấm làm cổng. |
| "Không có số tiếng Việt?" | Dataset chuẩn là EN/ZH nên định lượng chạy EN/ZH; tiếng Việt là minh hoạ định tính + ~120 mẫu app Việt — ta nói rõ điều này. |
| "Sao không đưa cây giao diện vào lúc sinh (grounded-gen) như AskEase?" | Sinh mù là **thiết bị ĐO ảo giác**, không phải kiến trúc triển khai. Nạp cây vào lúc sinh → model chép → ảo giác bị *che/nhiễu* trong phép đo (grounding chỉ giảm, không triệt tiêu). Triển khai thật vẫn có thể grounded (xếp lớp). (§4.5) |
| "Đây là 'tự sửa' mà tự sửa đã bị chứng minh vô dụng (Huang ICLR24)?" | Không — ta dùng tín hiệu **NGOÀI, phi-LLM, tất định** (so embedding vs cây giao diện), đúng nhánh *được* chứng minh hợp lệ. Cái bị bác là *tự soi nội tại*. |
| "a11y-tree lỗi thời, field chuyển sang visual-grounding rồi?" | Trend đó là **agent bấm toạ độ** — trục khác. Ta sinh cho **người đọc** và chỉ dùng cây giao diện lúc **chấm/hậu kiểm**, kèm khai độ phủ nhãn + fallback. |
| "Fallback 'mô tả chung' là câu giờ vô dụng?" | Với **người đọc**, mô tả định hướng vẫn hữu dụng (khác agent bấm máy cần toạ độ). %fallback = *abstention hợp lý*, và ta đo chất lượng mô tả để không rỗng nghĩa. |
| "Pairwise O(N²) sao không listwise một shot?" | N nhỏ (mean ~5,5; p95 = 13) → vài chục cặp, rẻ; pairwise hơn listwise *ở model tầm trung* (Qin, Findings NAACL 2024) — **không** claim tốt hơn phổ quát; ta thêm baseline listwise + cột chi phí để so thẳng; Bradley-Terry/Elo là chuẩn thay thế. |
| "Bộ trỏ toạ độ có phải một phần hệ thống của em không?" | **Không.** Hệ sinh chỉ đẻ *chữ*; bộ trỏ là *dụng cụ đo* (mô hình grounding có sẵn), chạy lúc chấm, đứng ngoài và sau hệ. Phải để độc lập mới tránh được tautology (lấy tâm nút đã khớp thì luôn trúng 100%). (§5.1) |
| "Vậy ScreenSpot chứng minh hệ sinh hiệu quả à?" | **Không.** Nó kiểm *chính dụng cụ đo* (bộ trỏ) trên bộ chuẩn đã bình duyệt + bù độ tin cho MobileViews (preprint). Hiệu quả hệ sinh nằm ở trung thực/%fallback (một màn) + τ/Step-SR (nhiều màn), chấm bằng *chữ*, không đụng bộ trỏ. (§5.1) |
| "Bộ trỏ đo dở thì hệ tụt điểm oan?" | Có *nếu* dùng grounding để chấm hệ — nên ta không làm vậy. Grounding là trục phụ; bảng điểm chính không dùng bộ trỏ; và ta hiệu chỉnh bộ trỏ trên ScreenSpot + báo độ chính xác của nó. Thay bộ trỏ chỉ đổi *con số*, không đổi *hướng dẫn*. |
| "Nút chỉ có icon (không nhãn chữ) thì sao?" | Với người đọc, mô tả theo chức năng vẫn dùng được. Lúc chấm trung thực: loại nút không nhãn khỏi mẫu số + báo độ phủ nhãn. Lúc chấm grounding: báo riêng nút chữ / nút biểu tượng (icon khó hơn, khai thẳng). |

# PHỤ LỤC C — DANH MỤC NGUỒN BÌNH DUYỆT

**Thước đo & faithfulness:** ALOHa (NAACL 2024) · SeeClick (ACL 2024) · AITW (NeurIPS 2023) · Sai et al. (EMNLP 2021) · **BUMP (ACL 2023)** · Ribeiro et al. — CheckList (ACL 2020) · Panickssery et al. (NeurIPS 2024) · Chen et al. (ICSE 2020, Distinguished Paper) · Clark et al. (ACL-IJCNLP 2021) · FaithScore (Findings EMNLP 2024).

**Hậu kiểm / verify đối chiếu nguồn (nền cho pipeline "sinh mù → hậu kiểm"):** FaithScore (Findings EMNLP 2024) · **Chain-of-Verification — CoVe (Findings ACL 2024)** · **RARR (ACL 2023)** · **CaLM (ACL 2024, verify grounded generation bằng nguồn ngoài)** · **CRITIC (ICLR 2024, sửa bằng công cụ/tín hiệu ngoài)** · **Huang et al. — "LLMs Cannot Self-Correct Reasoning Yet" (ICLR 2024)** · **Tyen et al. (Findings ACL 2024, sửa tốt khi được cấp vị trí lỗi ngoài)** · **TACL survey on self-correction (2024)** · **Survey on hallucinations & prompting (Frontiers in AI 2025)** · "Do GUI Grounders Truly Understand UI Elements?" (Findings EACL 2026).

**Sắp thứ tự & xếp hạng:** Qin et al. (Findings NAACL 2024, pairwise) · RankGPT (EMNLP 2023, listwise) · Bradley-Terry/Elo (chuẩn de-facto rank-aggregation, đối chứng) · Dwork et al. (WWW 2001, Copeland) · Ailon et al. (JACM 2008, min-FAS) · Fagin et al. (SIAM J. Discrete Math 2006, partial ranking) · **Brandenburg, Gleißner & Hofmeier (2012/13, partial-order với cặp không so được)** · Lapata (Computational Linguistics 2006) · Gardner et al. (Findings of EMNLP 2020, cue/attribution) · Sort-Story (EMNLP 2016) · Wu et al. (ACL 2022) · **EZ-Sort (CIKM 2025)** · **Dodgersort (PAKDD 2026, Springer LNCS)** · **GVL — Generative Value Learning (ICLR 2025, Google DeepMind; xáo frame→suy thứ tự)** · **TOMATO (ICLR 2025 Poster; "bag-of-frames" — VLM yếu suy luận thứ tự)**.

**Bối cảnh GUI / định vị setup:** ShowUI (CVPR 2025) · GUI-Odyssey (ICCV 2025) · AMEX · ScreenSpot-Pro · UI-TARS · GUI-Actor (đều dòng agent điều khiển, phân biệt setup) · AskEase — "From Struggle to Success" (CHI 2026, sinh hướng dẫn cho người, phân định novelty).

**Dữ liệu:** AndroidControl (NeurIPS 2024 D&B) · ScreenSpot-v2 / OS-Atlas (ICLR 2025) · MobileViews (preprint arXiv 2409.14337) · AITW (NeurIPS 2023).

**Khung đánh giá neo & tính hợp lệ:** Chim, Ive & Liakata (*Computational Linguistics* 51(1):191–233, 2025) · **"Measuring what Matters: Construct Validity in LLM Benchmarks" (NeurIPS 2025 D&B)** · **"Neither Valid nor Reliable?" (NeurIPS 2025, Position track)**.

**Thống kê:** Cameron, Gelbach & Miller (2008, wild-cluster bootstrap-t) · **MacKinnon, Nielsen & Webb (Journal of Econometrics 2023, hướng dẫn ít cụm)** · **jackknife CV3/CV3J (JAE 2023)**.

**Định vị bối cảnh (accessibility / generation):** **AskEase — "From Struggle to Success" (CHI 2026)**.

**Tiền lệ pipeline gọn mà đậu:** G-Eval · FActScore · SelfCheckGPT (EMNLP 2023) · RAGAS (EACL 2024) · BERTScore (ICLR 2020).

*Nguyên tắc trích dẫn: xương sống phương pháp chỉ trích nguồn đã bình duyệt; preprint (MobileViews, OmniParser, Qwen, VECTOR, HalluClear, Ferret-UI Lite, ScreenSpot-Pro, UI-TARS, min-weighted-FAS 2412.16181, LLM-as-Meta-Judge…) chỉ đóng vai hiện vật kỹ thuật / định vị landscape, không làm trụ chính.*
> **Đã xác minh venue/năm (deep-research R-07+R-08, nguồn sơ cấp ACL Anthology/ACM/OpenReview/DBLP/SIAM):** FaithScore (Findings EMNLP 2024) · CoVe (Findings ACL 2024) · RARR (ACL 2023) · Huang (ICLR 2024) · ALOHa (NAACL 2024 Short) · Qin (Findings NAACL 2024) · "Do GUI Grounders…" (Findings EACL 2026) · AskEase (CHI 2026, DOI 10.1145/3772318.3790661) · CaLM (ACL 2024) · CRITIC (ICLR 2024) · GVL (ICLR 2025) · **TOMATO (ICLR 2025 — Poster)** · **EZ-Sort (CIKM 2025, DOI 10.1145/3746252.3760848)** · **Dodgersort (PAKDD 2026, DOI 10.1007/978-981-92-1468-6_32)** · **"Measuring what Matters…in Large Language Model Benchmarks" (NeurIPS 2025 D&B Track)** · **"Neither Valid nor Reliable?" (NeurIPS 2025 Poster)** · **MacKinnon-Nielsen-Webb (J. Econometrics 232(2):272–299, 2023)** · BUMP (ACL 2023) · Ribeiro CheckList (ACL 2020) · Fagin (SIAM J. Discrete Math 2006) · Lapata (CL 2006) · Chim-Ive-Liakata (CL 51(1) 2025).
> **Sửa NHÃN khi in (venue đúng, chỉ chỉnh nhãn):** ghi **"Poster"** cho TOMATO; ghi **tên đầy đủ + "Datasets & Benchmarks Track"** cho "Measuring what Matters"; **Active Evaluation (Mohankumar & Khapra, ACL 2022) = OUTSTANDING Paper, KHÔNG phải "Best Paper"**. Còn *chỉ* ở vài link cổ điển (Copeland/Dwork, min-FAS/Ailon) — đối chiếu PDF trước khi trích. Chi tiết: `report/45` §C + `report/27` §8.

---

*Nguồn đào sâu: `report/05` (kế hoạch — thắng khi mâu thuẫn) · `report/36` (thuyết minh một màn) · `report/40` (phán quyết phản biện + 5 fix M1–M5) · `report/42` (độ mới 2026) · `report/44` (chương dữ liệu verify tận file). Dữ liệu thật minh hoạ: `dataset_samples/`.*
