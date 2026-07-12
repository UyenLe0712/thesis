# SLIDE TRÌNH THẦY — CHỐT SCOPE (có speaker notes)

> Mỗi `---` là một slide. **Bullet** = chữ trên slide (ngắn gọn). **🎤 Nói** = lời thuyết trình. **🖼️** = hình gợi ý.
> Trọng tâm thuyết phục: **đa bước ĐƯỢC GIỮ và ĐO ĐƯỢC** (không phải bỏ). Mọi citation đã kiểm chứng web.
>
> 💡 **Đột phá so với bản nháp:** đa bước được đặt lại thành bài toán **SUY LUẬN TRẬT TỰ MÀN** — đưa N ảnh đã **xáo trộn** của một luồng đa bước, bắt model **tự xếp đúng thứ tự** rồi mới sinh hướng dẫn. Đây là kết quả của vòng debate (proponent ↔ skeptic) + verify, và trả lời thẳng câu hỏi của thầy *"làm sao model biết trật tự?"*.

---

## Slide 1 — Tiêu đề
**Sinh tự động hướng dẫn sử dụng phần mềm từ ảnh màn hình + câu hỏi, và đánh giá khi không có đáp án mẫu**
- Học viên: … · GVHD: … · 2026
- *Multimodal (ảnh + chữ → chữ) · có đánh giá đa bước đo được*

🎤 **Nói:** "Em xin trình bày đề tài và **phạm vi đề nghị chốt**. Điểm em muốn nhấn ngay từ đầu: **đề tài CÓ làm đa bước, và làm theo cách đo lường được bằng số** — em sẽ chứng minh ở slide 4."

---

## Slide 2 — Bài toán + ví dụ
**Vào:** 1 ảnh màn hình + 1 câu hỏi → **Ra:** hướng dẫn bấm từng bước
- VD: ảnh app eTax + *"Kiểm tra đã nộp thuế chưa thì vào đâu?"*
- → *"1. Bấm 'Tra cứu nghĩa vụ thuế'. 2. Chọn kỳ. 3. Xem trạng thái."*

🎤 **Nói:** "Người dùng chỉ đưa *một ảnh + một câu hỏi*; mọi xử lý bên dưới là việc của hệ thống. Đầu ra là hướng dẫn cho **người đọc**. Phần lõi dùng **VLM** = model AI vừa 'nhìn' ảnh vừa viết chữ (GPT-4o, Qwen2.5-VL). *Ví dụ kể được (EX-A — là ví dụ minh hoạ tự soạn để kể chuyện; record thật của dataset trong báo cáo):* em đưa **ảnh chụp app eTax** kèm câu hỏi *'Kiểm tra đã nộp thuế chưa thì vào đâu?'* — hệ trả về *'1. Bấm Tra cứu nghĩa vụ thuế. 2. Chọn kỳ. 3. Xem trạng thái.'* Đây là **đơn bước trên màn-0** vì nút cần bấm đã nằm ngay trong ảnh; ở slide 4 em sẽ kể ca **đa bước** khó hơn."

🖼️ Ảnh eTax với mũi tên sang khung hướng dẫn 3 bước.

---

## Slide 3 — Vì sao khó & đáng làm
- ❌ **Không có "đáp án mẫu"** (tutorial chuẩn do người viết) để học/chấm
- ⚠️ VLM **hay bịa nút không tồn tại** → hướng dẫn sai
- 🌐 Phải chạy được trên **app bất kỳ**

🎤 **Nói:** "Cái khó cốt lõi *không phải sinh cho hay*, mà là **đánh giá được chất lượng khi không có đáp án mẫu**. Đây chính là chỗ luận văn đóng góp về phương pháp."

---

## Slide 4 — ⭐ ĐA BƯỚC = SẮP THỨ TỰ MÀN (slide quan trọng nhất)
**Bài toán — trên AndroidControl (NeurIPS 2024 D&B):**
- Đưa **N ảnh ĐÃ XÁO TRỘN** của 1 luồng đa bước + **mục tiêu** → model phải (1) **suy ra THỨ TỰ đúng**, (2) **sinh hướng dẫn** theo thứ tự đó *(N thực tế 3→~6, có thể tới ~8–10 nếu ngân sách cho; p95 độ dài episode = 13)*
- Model dựa vào **ordering cues**: Next/Back · toggle off→on · đăng-nhập-trước · danh-sách→chi-tiết
- **Hai loại cặp:** **BẮT BUỘC** (vd *đăng nhập → xem kết quả*: đảo là sai thật) vs **TỰ-DO** (vd *điền email / điền sđt*: trước-sau đều được, đảo vẫn đúng)
- **Metric:** **Kendall τ-b** (chấm *partial-order-aware* — chỉ phạt cặp **BẮT BUỘC**) + **ordering gap** = ORACLE-ORDER − SELF-ORDER

🎤 **Nói (3 nhịp):**
- **[Nhịp 1 — ví dụ xáo trộn]** "Một luồng *'đặt báo thức 7:00'* trên app **Đồng hồ** có 3 màn: vào tab Báo thức → bấm '+' → nhập 07:00 rồi OK. Em **xáo trộn** 3 ảnh này đưa cho máy *không theo thứ tự* kèm mục tiêu." *(ví dụ minh hoạ tự soạn; record thật của AndroidControl là episode 'cruisedeals')*
- **[Nhịp 2 — máy tự xếp lại]** "Máy phải nhìn các tín hiệu giao diện — ví dụ màn nhập giờ có nút OK (drill-down), màn danh sách báo thức có nút '+' — để **suy ra trật tự đúng** rồi mới sinh hướng dẫn từng bước. Em đo **Kendall τ-b**: máy xếp giống thứ tự đúng đến đâu. Em chỉ phạt khi đảo **cặp BẮT BUỘC**; cặp **tự-do** (vd điền email/sđt độc lập) đảo vẫn tính đúng. **Quan trọng — chống vòng lặp-luận:** nhãn 'cặp bắt buộc' em **KHÔNG** lấy từ bộ phát-hiện-cue mà chính model dùng (lấy thế là **tự chấm**); em **suy từ gold trajectory của AndroidControl bằng quy tắc tất định: màn B chỉ xuất hiện SAU khi thực thi gold action ở màn A ⇒ cặp (A,B) là bắt buộc (phụ thuộc nhân-quả trong chuỗi vàng)**; cặp không có quan hệ đó = tự-do. Gold/VH **chỉ dùng khâu chấm offline**, không phải input lúc model xếp."
- **[Nhịp 3 — ý nghĩa ordering gap]** "Em so 2 chế độ: **ORACLE-ORDER** = đưa ảnh *đã sắp đúng* (chỉ sinh) vs **SELF-ORDER** = ảnh *xáo trộn* (tự xếp rồi sinh). Hiệu hai bên = **ordering gap** = **cái giá của việc không biết trật tự**. Sanity cứng: ORACLE luôn ≥ SELF mỗi episode."

🖼️ Trái: mockup N ảnh xáo trộn → mũi tên → chuỗi đã sắp lại. Phải: sơ đồ ordering gap (ORACLE-ORDER vs SELF-ORDER) trên trục τ-b.

---

## Slide 5 — Hai đóng góp
- **Đóng góp 1 (MỚI — không cần tutorial mẫu của người, neo bằng VH-silver):** đánh giá *không cần đáp án mẫu* cho **grounding + hallucination** trên **màn-0**, neo vào **View Hierarchy**
- **Đóng góp 2 (đa bước — có đáp án đúng để so):** **suy luận trật tự màn** (slide 4) — trả lời thẳng câu hỏi của thầy *"làm sao model biết trật tự?"*; headline **Kendall τ-b** (nhãn cặp bắt buộc **suy từ gold trajectory** bằng quy tắc tất định, không từ bộ phát-hiện-cue) + **ordering gap**, **mọi số dùng metric đã bình duyệt**

🎤 **Nói:** "View Hierarchy = cây cấu trúc UI có toạ độ chuẩn; 'reference-free' ở đây nghĩa hẹp là **vẫn neo bằng VH-silver**, chỉ thiếu *tutorial gold do người viết*. Hai đóng góp **độc lập về phương pháp** (một cái không-cần-đáp-án, một cái có-đáp-án) nhưng **bổ trợ nhau**: sau khi máy xếp đúng trật tự ở Đóng góp 2, mỗi màn được sinh hướng dẫn và **chấm grounding đầy đủ** bằng chính metric của Đóng góp 1 — hai nửa kiểm chứng lẫn nhau. Đặc biệt Đóng góp 2 chỉ ra **model dựa vào tín hiệu giao diện nào** (ordering cues) để biết trật tự — đó là câu trả lời trực tiếp cho thầy."

---

## Slide 6 — Hệ thống (pipeline: ReOrder-Tutor) — ý tưởng cốt lõi
**Biến bài "tự luận" (máy tự viết → hay bịa) thành "trắc nghiệm" (đánh số nút → ép máy chỉ vào số)**
- **Stage 0 — Screen-Ordering** (chỉ bật khi N≥2): xếp các màn xáo trộn theo thứ tự đúng → rồi mới chạy 5 bước dưới trên từng màn. *(N=1 → Stage-0 rỗng → về pipeline cũ. Một hệ duy nhất, có input router.)*
1. **Dò & đánh số** mọi nút trên ảnh (OmniParser + OCR) → ①②③…
2. **Vẽ số** lên ảnh (Set-of-Mark)
3. **Sinh có ràng buộc**: model chỉ được **chỉ vào số** (Qwen2.5-VL/GPT-4o)
4. **Kiểm 3 tầng**: có số? đúng-ý? sai thì tự sửa
5. **Đổi số → toạ độ** (để hiện cho người + để chấm)

🎤 **Nói:** "Mẹo chống bịa: model **không thể** nhắc nút ngoài danh sách đã dò, vì nó chỉ được chọn số. *Ví dụ (EX-A — ví dụ minh hoạ):* ở ảnh eTax, bước dò gán ③ *(ví dụ minh hoạ)* = nút 'Tra cứu nghĩa vụ thuế'; câu trả lời chỉ được nói 'bấm ③' — nếu model định bịa một nút 'Lịch sử nộp thuế' *không có trên ảnh*, tầng kiểm-tồn-tại loại ngay vì không có số tương ứng. Cuối cùng ③ được đổi ra toạ độ **(405,915)** *(ví dụ minh hoạ)* để hiện mũi tên cho người dùng. View Hierarchy **chỉ dùng lúc chấm**, không đưa cho máy lúc sinh — để hệ chạy được trên app thật. *(Làm rõ trọng tâm: cơ chế chống bịa nằm ở bước **SINH** — ép model chỉ được chọn số đã có trong danh sách E — chứ KHÔNG phải ở bước kiểm. Trong 3 tầng kiểm: **V1 = so khớp thuần bằng code** kiểm số có tồn tại trong E hay không (không phải LLM; vẫn cần làm như chốt an toàn), chỉ **V2** mới là **một LLM khác** kiểm đúng-ý/intent, V3 = tự sửa ≤2 lần.)*"

🖼️ Sơ đồ 5 hộp với ví dụ eTax (③ = 'Tra cứu nghĩa vụ thuế'); thêm hộp Stage 0 đứng trước (sơ đồ router N=1 / N≥2).

---

## Slide 6b — Ordering cues + signal-attribution (model dựa vào đâu để biết trật tự?)
**5 tín hiệu (ordering cues) — đặt tên để trả lời thẳng câu hỏi thầy:**
- **gating** — đăng nhập / cấp quyền phải đứng trước
- **nav-affordance** — nút Next/Back/breadcrumb
- **state-delta** — toggle off→on, ô trống→đã điền, badge 0→1
- **title-progression** — tiêu đề tiến theo phiếu (bước 1/3 → 2/3)
- **drill-down** — màn sau = chi tiết của item màn trước

**Cách xếp thứ tự:** hỏi VLM từng **cặp** "màn nào trước?" (bắt trích ≥1 cue) → tổng hợp bằng **Copeland score** → verifier code thuần dọn mâu thuẫn. **Chi phí:** pairwise = C(N,2) call (mốc chốt N=6 → 15; minh hoạ N=8 → 28, N=10 → 45, p95 N=13 → 78 call/episode) → **chốt trần N≤6** cho đường cong headline (báo thêm tới ~8–10 nếu ngân sách cho), tính chi phí Stage-0 vào ngân sách. *(Listwise 1-call làm đối chứng **fair-compute = CÙNG tổng số LLM-call**: listwise self-consistency số mẫu = số call pairwise.)* Phá tie Copeland **tất định** (vd theo chỉ số ảnh tăng dần), tách khỏi tie cặp-tự-do.

**Signal-attribution = stratification một-cue:** chỉ giữ cặp phân biệt bởi **đúng một cue**, đo accuracy theo từng nhóm cue → biết cue nào *thực sự* giúp xếp đúng. **Không che pixel** (che pixel tạo artifact). **Caveat:** cue do model **tự trích** chỉ là tín hiệu **giải thích YẾU**; kết luận "cue nào trả công" dựa trên **stratification một-cue**, KHÔNG dựa lời model tự khai. Baseline đối chứng: **GOAL-ONLY** (che ảnh, chỉ mục tiêu) + **VISUAL-ONLY** (che mục tiêu, chỉ ảnh — đối xứng GOAL-ONLY, tách đóng góp ảnh vs goal) + **RANDOM-ORDER**.

🎤 **Nói:** "Đây là câu trả lời trực tiếp cho thầy: **model không đoán bừa**, nó bám vào những tín hiệu cụ thể trên giao diện. Em đặt tên 5 loại tín hiệu, rồi **lọc ra các cặp màn chỉ khác nhau ở đúng một loại tín hiệu** để đo riêng từng loại — biết được cue nào trả công. Lưu ý: cue model tự khai chỉ là giải thích yếu, em kết luận bằng *stratification* chứ không tin lời tự khai. Hai baseline đối xứng: **GOAL-ONLY** (che ảnh) và **VISUAL-ONLY** (che mục tiêu) — nếu GOAL-ONLY mà đã xếp đúng cao thì chứng tỏ tín hiệu giao diện *không* phải nguồn; đây là chốt an toàn chống ngộ nhận."

🖼️ Bảng 5 cue + bar per-cue accuracy.

---

## Slide 7 — Metric: dựa trên bài bình duyệt
| Tiêu chí | Metric | Nguồn (venue) |
|---|---|---|
| Khung gốc | Intrinsic/Extrinsic | **Computational Linguistics 2025** (journal) |
| Grounding | Point-in-BBox | **ACL 2024** (SeeClick) |
| Hallucination | HER (CHAIR) | **EMNLP 2018** |
| — khớp tên | ALOHa | **NAACL 2024** |
| Format | IFEval | arXiv *(preprint nhưng là chuẩn instruction-following dùng rộng)* |
| Clarity | G-Eval | **EMNLP 2023** |
| Validate người | BWS + Spearman | **ACL 2017** + kinh điển |

> **Hướng tốt của metric:** HER càng **THẤP** càng tốt — báo cáo dạng **1−HER** (cao = tốt) để cùng chiều; **Point-in-BBox / G-Eval / Kendall τ-b** đều **cao = tốt**.

🎤 **Nói:** "**Không có metric nào em tự nghĩ ra.** Khung kế thừa từ một **journal bình duyệt**; mỗi metric từ **ACL/EMNLP/NAACL**. *Cách chấm bằng ví dụ EX-A:*
- **Point-in-BBox (grounding):** toạ độ máy chỉ — (405,915) *(ví dụ minh hoạ)* — có rơi trong bounding-box của nút 'Tra cứu nghĩa vụ thuế' theo View Hierarchy không; rơi trong = trúng, lệch ra ngoài = trượt.
- **HER (CHAIR-style):** đếm tỉ lệ nút máy nhắc mà cây UI **không hề có** — ví dụ bịa thêm nút 'Lịch sử nộp thuế' thì đó là 1 hallucination tính vào HER.
- **ALOHa:** lo phần khớp tên (máy gọi 'Tra cứu thuế' so với tên thật 'Tra cứu nghĩa vụ thuế')."

---

## Slide 8 — Dataset: dùng 2+ bộ, và xử lý credibility
- **Đóng góp 1:** **MobileViews** (mobile, có VH + bbox pixel) ⚠️ *là preprint*
- **Đóng góp 2:** **AndroidControl (NeurIPS 2024 D&B)** — đa bước có mục tiêu + metric chuẩn
- **Mỏ neo bù credibility:** **ScreenSpot** (gốc = SeeClick, **ACL 2024**) — hoặc **ScreenSpot-v2** (**OS-Atlas, ICLR 2025**) — đối chứng grounding
- *Thông lệ: ≥2 bộ để chứng minh tổng quát*

🎤 **Nói:** "Em nói thẳng một điểm yếu: **MobileViews chỉ là preprint, chưa bình duyệt**. Vì vậy em ghép thêm **các bộ đã bình duyệt** (ScreenSpot ACL 2024, AndroidControl NeurIPS 2024 D&B) làm mỏ neo — vừa theo thông lệ ≥2 bộ, vừa vá đúng lỗ hổng đó. Ngưỡng **Grounding@14%** lấy từ **AITW (NeurIPS 2023)**; AITW cũng có thể dùng đối chứng tuỳ chọn. *Bản ghi minh hoạ (cấu trúc thật, nội dung tự soạn):* node `{text:'Tra cứu', bounds:[270,820,540,1010], clickable:true}`; schema thật: root `bounds=[0,0,1080,1920]`."

---

## Slide 9 — Thiết kế thí nghiệm
- **Đóng góp 1 — ablation "thang bậc"** (thêm từng món, biết **cơ chế nào trả công**):

| Bậc | Thêm gì |
|---|---|
| **C0** | trần (chỉ VLM) |
| **C1** | + tự-sửa (self-refine) = **BASELINE CHÍNH** |
| **C2** | + đánh số (Set-of-Mark) |
| **C3** | + ràng-buộc + kiểm tồn-tại (V1) |
| **C4** | + kiểm-ý (V2) = đầy đủ |

> **LÕI/Gọn CHỈ chạy 3 bậc {C1, C3, C4};** C0 (sàn thô) và C2 (Set-of-Mark một mình) = MỞ RỘNG/ĐỐI CHỨNG, chạy thêm nếu ngân sách cho phép.

- **Đóng góp 2 — ORACLE-ORDER vs SELF-ORDER**: đường cong **τ-b theo N**, **ordering gap**, bar **per-cue accuracy**; baseline đối xứng **GOAL-ONLY / VISUAL-ONLY / RANDOM-ORDER** (ngưỡng vượt = phân phối NULL thực nghiệm theo từng N)
- *(Giữ Tier A teacher-forced làm trục tham chiếu chuẩn ngành — Action-Type/Grounding@14%/Step-SR — KHÔNG còn là "đa bước chính"; ORACLE-ORDER là skyline của trục ordering.)*
- **Tách lỗi:** báo **RAW vs ORACLE** (giả định nút đã được dò) → tách *lỗi nhìn* (dò sót) khỏi *lỗi nghĩ* (suy luận)

🎤 **Nói:** "Em không so kiểu A/B một phát, mà **thêm từng món đo từng nấc** — để kết luận được *cơ chế nào* thực sự có ích, chứ không chỉ 'hệ tôi thắng'. Mỗi nấc trả lời một câu hỏi: **C0** = mức nền? **C1** = tự sửa có đủ không? **C2** = gắn ①②③ có giúp grounding? **C3** = ép cite số có chống bịa? **C4** = có đúng ý người dùng? Còn Đóng góp 2 em đo **τ-b theo từng độ dài N** (N từ 3 đến ~6, báo thêm tới ~8–10 nếu ngân sách), so **ORACLE-ORDER** và **SELF-ORDER** để rút **ordering gap**, và vẽ **bar accuracy theo từng cue**."

🖼️ Bảng C0–C4 + đồ thị 2 đường (RAW, ORACLE) cho Đóng góp 1; đường cong τ-b theo N (ORACLE-ORDER vs SELF-ORDER) + bar per-cue accuracy cho Đóng góp 2.

---

## Slide 10 — Rủi ro lớn nhất (nói thẳng)
- Hệ chỉ giỏi bằng **bước dò nút**; tỷ lệ dò trúng (recall) cho UI mobile **chưa công bố rõ** — *ước lượng, tự đo tuần-1* (giả thuyết ~một nửa)
- → **Việc đầu tiên (tuần 1):** tự **đo tỷ lệ dò trúng** (K1, cổng cứng); mọi số grounding ghi kèm *"điều kiện recall = X%"*
- → Báo **RAW vs ORACLE** để lỗi-nhìn không bị nhầm thành lỗi-nghĩ
- → **BỐN cổng cứng** (tổng 10 kill-test): **K1** (recall dò nút) · **KN** (tự đếm histogram độ dài episode — sơ bộ mean ~5.5, p95=13) · **KZ'** (rà prior-art sắp-ảnh — đã khảo, GO) · **KB** (chống leak step-index: xáo trộn phải strip metadata + tái mã hoá ảnh + đặt tên UUID; **còn che status bar/đồng hồ/pin/badge** + loại episode 2-ảnh trùng-pixel)

🎤 **Nói:** "Em chủ động phơi bày rủi ro này thay vì giấu. Nếu recall thấp, em **đổi cách phát biểu** thành 'grounding trong giới hạn khả năng dò' — vẫn là đóng góp, không bỏ đề tài."

---

## Slide 11 — Kết quả âm vẫn ĐẬU
- Đóng góp = **quy trình đánh giá + câu hỏi khoa học có pre-register**, không phải "hệ phải thắng"
- Nếu "ràng buộc cấu trúc *không* giúp một khi kiểm soát recall" → đó là **phát hiện có giải thích cơ chế** = đóng góp hợp lệ

🎤 **Nói:** "Em **đăng ký giả thuyết trước khi chạy**. Một kết quả null *được giải thích cơ chế* là khoa học hợp lệ — đây là tấm bảo hiểm để luận văn không phụ thuộc vào việc hệ phải thắng baseline."

---

## Slide 12 — Tính khả thi
- Linh kiện **có sẵn**, **không cần fine-tune**
- **1 GPU 24GB** (thuê ~**$0.3–0.5/h**, *ước tính, tùy nhà cung cấp/bảng giá hiện hành*) + **~$100–300** API (*ước tính*)
- Bộ kill-test (**BỐN cổng cứng K1/KN/KZ'/KB** + tổng 10 kill-test) ≤1 ngày/cái để loại rủi ro trước khi cam kết

🎤 **Nói:** "Toàn bộ chạy bằng công cụ có sẵn, không huấn luyện model, trong tầm một học viên và ngân sách nhỏ. Chấm điểm là *offline* trên dữ liệu công khai nên không tốn thiết bị đặc biệt."

---

## Slide 13 — Phạm vi đề nghị CHỐT
| ✅ Trong luận văn | 🔭 Future-work |
|---|---|
| Grounding/hallucination màn-0 (reference-free — vẫn neo bằng VH-silver) | World-model tự huấn luyện (đoán màn kế bằng AI) |
| **Đa bước = suy luận trật tự màn (τ-b + ordering gap)** | **Chấm định lượng tiếng Việt** (không có dữ liệu) |
| Ablation thang bậc + pilot chuyên gia | Mở rộng web (Mind2Web) |

- **Tiếng Việt:** động cơ (eTax) + kiểm OCR đọc dấu + **demo định tính** — *không* có bảng số VN (vì khách quan không có dữ liệu chuẩn)

🎤 **Nói:** "Em để future-work *chỉ những gì không có dữ liệu để chấm* — đó là quyết định có cơ sở, không phải né. Về tiếng Việt: hệ **vẫn sinh hướng dẫn tiếng Việt được**; chỉ là *chấm điểm tự động* phải neo trên dữ liệu Anh/Trung vì không tồn tại dữ liệu chuẩn tiếng Việt."

---

## Slide 14 — Đề nghị duyệt + tuần 1
- Xin **chốt phạm vi** ở cột ✅ (gồm **đa bước = suy luận trật tự màn**)
- **Tuần 1:** chạy kill-test, quan trọng nhất là **đo recall dò nút** → báo lại thầy chốt cách phát biểu
- Lộ trình 6 pha có cổng kiểm tra

🎤 **Nói:** "Em xin thầy duyệt phạm vi này. Tuần này em chạy nhanh các kiểm tra rủi ro rồi báo lại để thầy chốt. Em cảm ơn thầy."

---

## PHỤ LỤC — Đối đáp (chuẩn bị sẵn)
| Thầy hỏi | Trả lời |
|---|---|
| **Làm sao model biết trật tự các màn?** | Model bám vào **5 loại tín hiệu giao diện (ordering cues)**: **gating** (đăng nhập/cấp quyền trước), **nav-affordance** (Next/Back/breadcrumb), **state-delta** (toggle off→on, ô trống→đã điền, badge 0→1), **title-progression** (tiêu đề tiến theo phiếu), **drill-down** (màn sau = chi tiết item màn trước). Em **đo riêng từng cue** bằng signal-attribution (chỉ giữ cặp khác đúng-một-cue) để biết cue nào *thực sự* giúp xếp đúng, không che pixel. |
| **Có thực sự làm đa bước không?** | Có — đa bước được đặt thành bài **suy luận trật tự màn**: đưa **N ảnh xáo trộn** của một luồng + mục tiêu, model phải **sắp đúng thứ tự các màn ĐƯỢC CUNG CẤP** (mọi ảnh đều do người dùng đưa và model đều thấy) rồi sinh hướng dẫn từng màn, **chấm grounding đầy đủ mọi màn**. Headline = **Kendall τ-b** chấm *partial-order-aware*. |
| **Đo trật tự bằng gì? Tại sao không dùng exact-match?** | Headline = **Kendall τ-b** (Kendall 1938 + tiền lệ "dùng τ chấm ordering" = **Lapata 2006**, *Computational Linguistics* 32(4):471–484; Gao et al. NAACL 2025 ở vai meta-eval). Em **không** dùng Exact-Order-Match làm headline vì N=3 thì trúng ngẫu nhiên đã ~17%, N≥6 còn ~0% → vô nghĩa. τ-b chấm **theo thứ-tự-bộ-phận**: chỉ phạt khi đảo **cặp BẮT BUỘC**; cặp tự-do (điền email/sđt trước-sau đều được) đảo vẫn tính đúng. **Nhãn cặp bắt buộc suy từ GOLD trajectory bằng quy tắc tất định** (màn B sinh ra sau gold action ở màn A ⇒ (A,B) bắt buộc) — **KHÔNG** lấy từ bộ phát-hiện-cue (tránh tự chấm vòng-lập-luận). **Pre-register:** (i) tỉ lệ cặp bắt-buộc/tự-do, (ii) **audit người 50–80 cặp** kiểm quy tắc tất định khớp đánh giá người (báo % khớp), (iii) đo **độ nhạy headline khi nhãn sai 10%**. Báo thêm **τ-b-thô** trên toàn tập làm điểm sàn robustness. |
| **"vượt RANDOM" nghĩa là gì — random τ-b bằng 0?** | Không giả định kỳ vọng τ-b random = 0. Ngưỡng "vượt RANDOM" = **phân phối NULL thực nghiệm theo TỪNG N** (sinh hoán vị ngẫu nhiên, đo τ-b → lấy phân vị). Discrete-N: pre-register **≥30 episode mỗi mốc N** + hiệu chỉnh đa-kiểm-định **Holm–Bonferroni** (hoặc hạ H2 xuống exploratory). *(Chỉ nói khi thầy hỏi.)* |
| **N-ảnh — ai dùng kiểu nhập nhiều ảnh trong thực tế?** | Em nói thẳng: chế độ N-ảnh là **bài toán em ĐẶT RA để ĐO** năng lực suy luận trật tự (trả lời đúng câu hỏi của thầy), **KHÔNG khẳng định** đây là nhu cầu deploy phổ biến. Sản phẩm có **input router**: người dùng thường nhập **1 ảnh** → đơn bước (DG1 nguyên vẹn); chỉ khi có N≥2 ảnh mới bật chế độ sắp-thứ-tự. Một hệ duy nhất. |
| **Sắp 3 màn thì có gì khó (chẳng phải dễ sao)?** | Em đã khảo độ dài episode AndroidControl: mean ~5.5 bước, **percentile-95 = 13 bước** → có nhiều luồng dài chứ không chỉ 3 màn. Em loại N≤2 (1 cặp thì τ-b vô nghĩa), trục N thực tế **3 đến ~6** (báo thêm tới ~8–10 nếu ngân sách). Việc tuần-1 (cổng **KN**) là **tự đếm histogram chính xác** để báo số episode còn lại ở mỗi mốc N. |
| **Đã có ai sắp ảnh GUI theo thứ tự chưa (prior-art)?** | Em đã rà (cổng **KZ'**): **không** có công trình trùng khít. Gần nhất là Sort-Story (EMNLP 2016, xếp ảnh+caption — **dùng Spearman, KHÔNG phải τ**), "Sequencing Multimodal Instructional Manuals" (Wu et al. ACL 2022), RankGPT (EMNLP 2023 — là **phương pháp listwise** sinh permutation theo query, không phải metric). Tiền lệ τ-cho-ordering = **Lapata 2006** + Wu 2022. Em **thừa nhận lineage** này, **không claim "xếp ảnh xáo là mới"**. Độ mới = (a) domain **GUI màn hình**, (b) **điều kiện hoá theo mục tiêu/use-case**, (c) gắn ordering → **sinh tutorial**, (d) **signal-attribution** theo ordering cue. |
| **ordering gap là gì, gap nhỏ có phải luôn tốt?** | gap = chất-lượng(**ORACLE-ORDER**, ảnh đã sắp đúng) − chất-lượng(**SELF-ORDER**, ảnh xáo trộn tự xếp) = "cái giá của việc không biết trật tự". Sanity: **ORACLE ≥ SELF − ε mỗi episode** (không phải ≥ tuyệt đối, cho phép biên ε). Cảnh báo floor-effect: gap chỉ có nghĩa nếu metric tutorial **nhạy với thứ tự**. Em **pre-register TEST NHẠY-THỨ-TỰ**: lấy input đã sắp đúng, **đảo 1 cặp bắt buộc**, đo delta metric tutorial; nếu delta < ngưỡng tối thiểu (pre-register) ⇒ metric không nhạy thứ tự ⇒ **bỏ ordering gap, chỉ giữ τ-b làm headline** (DG2 không sụp). *(Chỉ nói khi thầy hỏi.)* |
| **OmniParser sót ~50%?** | recall UI mobile **chưa công bố rõ** → K1 tự đo (giả thuyết ~một nửa). Báo **RAW vs ORACLE** (giả định nút đã dò) để tách *lỗi nhìn* khỏi *lỗi nghĩ*; mọi số kèm điều kiện recall. |
| **MobileViews chưa bình duyệt?** | Đúng, em thừa nhận; nên em ghép **ScreenSpot (ACL 2024)** + **AndroidControl (NeurIPS 2024 D&B)** đã bình duyệt làm mỏ neo. |
| **Đủ tầm thạc sĩ chưa?** | Có: (1) phương pháp đánh giá reference-free (vẫn neo bằng VH-silver) mới; (2) bài toán **suy luận trật tự màn** với τ-b + ordering gap + signal-attribution theo cue; (3) pilot người. Hai đóng góp + thí nghiệm có kiểm soát. |
| **Metric có phải tự chế?** | Không — toàn bộ từ ACL/EMNLP/NAACL/CL journal. Đóng góp của em là **thiết kế đánh giá**, không phải metric. |
| **Tiếng Việt sao không có số?** | Vì **không tồn tại** dữ liệu View Hierarchy tiếng Việt ở bất kỳ đâu → không tính được metric. Em giữ tiếng Việt ở dạng demo + kiểm OCR. |
| **Ví dụ eTax có thật trong dataset không?** | Không — ví dụ eTax (app eTax, bbox `[270,820,540,1010]`, điểm `(405,915)`) là **ví dụ minh hoạ tự soạn** để kể chuyện cho dễ hiểu. Dataset chấm điểm thật là **app tiếng Anh/Trung**. Record thật ví dụ: **AndroidControl** có bước `{action_type: click, x:313, y:742}`; **ScreenSpot** có mẫu instruction `'close'`, bbox `[0.948,0.144,0.994,0.207]` (chuẩn hoá 0–1). Khi vào báo cáo, mọi con số grounding đều lấy từ record thật của dataset. |
| **Tự soạn câu hỏi có phải bịa dữ liệu?** | Không — chỉ **MobileViews (màn-0, Đóng góp 1)** cần tự soạn câu hỏi vì bộ này **không kèm sẵn câu hỏi use-case**; AndroidControl/ScreenSpot đã có sẵn goal/instruction nên không phải soạn. "Tự soạn câu hỏi" = chỉ viết phần **INPUT (câu hỏi)** cho ảnh có sẵn; còn **đáp án chấm** (VH bbox / gold action) **vẫn là dữ liệu thật từ dataset**. Khác hẳn "sinh dữ liệu tổng hợp" (bịa ra cả đáp án/ground-truth) — việc luận văn **tránh**. |
| **Record thật AndroidControl trông thế nào?** | Một episode thật (KHÔNG phải ví dụ 'đặt báo thức' tự soạn): goal `"On cruisedeals, view cruise schedules for a four-night trip from New York to Canada"` → **B1** `open_app` **CruiseDeals** → **B2** `click` (x:313, y:742) → **B3** `swipe up`. Đây là chuỗi hành động gold thật dùng làm thứ-tự-đúng cho bài sắp-trật-tự (và làm gold action cho Tier A tham chiếu); ví dụ 'đặt báo thức 7:00 / app Đồng hồ' ở Slide 4 chỉ là minh hoạ tự soạn cho dễ kể. |

---

### ❖ Ghi chú dựng slide
- Slide **4** và **8** là 2 slide thuyết phục nhất → dành nhiều thời gian.
- Mỗi slide ≤6 dòng chữ; đẩy chi tiết vào lời nói.
- **Hình cần dựng (đinh):** (1) **sơ đồ input router** N=1 → đơn bước / N≥2 → sắp-thứ-tự; (2) **mockup N ảnh xáo trộn → mũi tên → chuỗi đã sắp lại**; (3) **đường cong τ-b theo N** (ORACLE-ORDER vs SELF-ORDER); (4) **bar per-cue accuracy** (5 ordering cues); (5) **ảnh thật AndroidControl** episode 'cruisedeals'; (6) **sơ đồ ordering gap** (ORACLE-ORDER − SELF-ORDER).
- **Hình CÒN THIẾU trong deck — đăng ký bổ sung:**
  - **(7) [Slide 12]** vẽ **đường ORACLE-ORDER chung trục với SELF-ORDER** để THẤY rõ **ordering gap** (hiệu hai đường = cái giá của việc không biết trật tự).
  - **(8) [Slide 5]** **mockup ngang 3 màn cruisedeals** (open app → click (313,742) → swipe up), ghi chú "**sơ đồ mô phỏng chuỗi gold THẬT** của AndroidControl" — minh hoạ nhãn cặp bắt buộc suy từ gold.
  - **(9) [Slide 6b]** **walkthrough Copeland 3 màn**: 3 câu hỏi cặp → cue trích được → đếm thắng A=2, B=1, C=0 → ra thứ tự A→B→C (kèm bước phá tie tất định).
