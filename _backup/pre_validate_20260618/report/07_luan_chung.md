# LUẬN CHỨNG: METRIC · DATASET · PIPELINE (để bảo vệ scope với thầy)

> Tài liệu này trả lời 3 câu hỏi của thầy: *dựa vào đâu, vì sao hợp lý, áp dụng thế nào*.
> Mọi citation đã được kiểm chứng chéo (đối chiếu ACL Anthology / arXiv / NeurIPS / MIT Press).
> **Ký hiệu độ tin cậy:** ✅ = hội nghị/journal bình duyệt (peer-reviewed); ⚠️ = preprint arXiv (chưa bình duyệt).

---

## TÓM TẮT 30 GIÂY

- **Căn cứ metric:** kế thừa khung đánh giá của một journal bình duyệt (**Computational Linguistics 2025**) cho bài toán "đánh giá văn bản nhân tạo khi không có đáp án mẫu", rồi hiện thực hoá bằng các metric **từ ACL/EMNLP/NAACL**. Không có metric nào tự nghĩ ra.
- **Hai đóng góp, chia theo "có sẵn đáp án đúng để chấm hay không":** **DG1** (màn-0, chấm bằng mỏ neo cấu trúc VH) và **DG2** (**suy luận trật tự màn** — Screen-Order Inference: cho N ảnh **xáo trộn** của 1 luồng đa bước + mục tiêu, model phải tự xếp đúng thứ tự rồi sinh hướng dẫn; chấm có-đối-chiếu trên AndroidControl, headline = **Kendall τ-b**; giữ Tier A teacher-forced làm trục tham chiếu chuẩn ngành).
- **Dataset:** 3 bộ, mỗi bộ một vai — **MobileViews** (màn-0, DG1) + **AndroidControl** (đa bước, DG2) + **ScreenSpot** (đối chứng grounding). ScreenSpot/AndroidControl đã bình duyệt → bù việc MobileViews là preprint.
- **Pipeline** được suy ra trực tiếp từ 3 ràng buộc bài toán (không có VH lúc chạy → tự dò nút từ ảnh; máy hay bịa → ép chỉ chọn nút đã dò; phải chấm được → gắn nút↔toạ độ), và mỗi bước có kỹ thuật nguồn.
- **Điều kiện duy nhất gắn mọi con số:** tỷ lệ máy dò trúng nút (recall) — con số này **chưa được công bố rõ** cho detector UI mobile (tài liệu mới chỉ có *grounding accuracy* ~57% trên ScreenSpot, KHÁC với recall phát hiện nút) → **K1 tự đo** ở tuần 1 (cổng cứng go/no-go); giả thuyết làm việc: có thể **~một nửa**. Mọi số grounding báo kèm "recall = X%".

---

## ❖ TRƯỚC TIÊN: "Bài trên arXiv có đáng tin không?" (thầy chắc chắn hỏi)

**arXiv là kho *preprint* — bài đăng lên CHƯA qua bình duyệt (peer review).** Ai cũng đăng được. Vì vậy:
- Một bài *"chỉ có trên arXiv"* = **chưa được cộng đồng thẩm định** → **không** được coi ngang một bài ở ACL/EMNLP/NeurIPS/journal.
- **Nhưng** rất nhiều công trình ML uy tín *cũng* nằm trên arXiv (đó chỉ là bản mở; bản chính ở hội nghị). Và nhiều công cụ tốt (model, thư viện) công bố dạng *technical report* trên arXiv là chuyện bình thường.

**Nguyên tắc dùng cho luận văn (để thầy yên tâm):**
1. **Xương sống phương pháp** (khung đánh giá, các metric khoa học) → **chỉ trích peer-reviewed.** May mắn: **gần như TẤT CẢ metric của ta đều từ hội nghị/journal đỉnh** (xem bảng cuối Phần A).
2. **Công cụ/model** (OmniParser, Qwen2.5-VL, Set-of-Mark) là **hiện vật kỹ thuật ta *dùng*, không phải tuyên bố khoa học ta *dựa vào*** → preprint chấp nhận được, nhưng **ghi rõ trạng thái** và ưu tiên cái có code + được dùng rộng.
3. **Không bao giờ trình một preprint như thể đã peer-reviewed** (bài học từ lỗi citation Chim et al. lúc đầu).

---

# PHẦN A — METRIC: dựa vào đâu, vì sao, áp dụng thế nào

> **❖ KHAI BÁO 1 LẦN (áp cho toàn Phần A):** mọi mục "**Ví dụ áp dụng (EX-A — eTax)**" và "**Ví dụ áp dụng (EX-B — Đồng hồ)**" trong tài liệu này là **ví dụ MINH HOẠ tự soạn** để giải thích *cách chấm* — **KHÔNG phải bản ghi (record) có thật** trong dataset. Cụ thể cụm "Tra cứu nghĩa vụ thuế / app eTax / bbox `[270,820,540,1010]` / điểm `(405,915)`" là **số liệu tự nghĩ cho dễ hiểu**, không phải node thật của MobileViews. **Record THẬT** (vd episode `cruisedeals`, mẫu ScreenSpot `'close'`, root VH `[0,0,1080,1920]`) xem `02_datasets.md` / mục **HỘP-THẬT**. Dưới mỗi mục dễ trích lẻ vẫn lặp lại hậu tố "(minh hoạ)" để khỏi nhầm khi đọc rời từng đoạn.

## A0. Hai đóng góp (DG1 / DG2) — chia theo "có sẵn đáp án đúng hay không"

Luận văn có **hai đóng góp**, chấm theo **hai chế độ dữ liệu khác nhau**, phân biệt bằng câu hỏi: *bộ dữ liệu có sẵn chuỗi thao tác đúng (gold trajectory) để so hay không?*

- **DG1 — MÀN-0, KHÔNG có tutorial mẫu của người.** VH là **đáp án bạc (silver):** cấu trúc nút do máy dò tự động, không phải tutorial vàng do người viết. **Vẫn chấm được** nhờ neo VH (grounding + hallucination + clarity), chỉ **thiếu bản mẫu của người để so câu chữ**. Dataset: **MobileViews** (+ **ScreenSpot** đối chứng). **Input router:** đây chính là chế độ **N=1** (một ảnh → đơn bước) — Stage-0 (xếp thứ tự) rỗng → chạy thẳng pipeline cũ.
- **DG2 — SUY LUẬN TRẬT TỰ MÀN (Screen-Order Inference), CÓ sẵn đáp án đúng** (AndroidControl, NeurIPS 2024). **Đổi trục:** input = **N ảnh ĐÃ XÁO TRỘN** của 1 luồng đa bước + mục tiêu → model phải (1) suy ra **THỨ TỰ đúng** của các màn, (2) sinh hướng dẫn từng bước theo thứ tự đó. Đây là **chế độ N≥2** của cùng một hệ (router N≥2 → bật chế độ sắp-thứ-tự). Headline = **Kendall τ-b** chấm partial-order-aware. Vẫn **giữ Tier A teacher-forced** làm *trục tham chiếu chuẩn ngành* (mốc trần). Chi tiết ở **A4**.

> **Trung thực với thầy:** chế độ N-ảnh là **bài toán ĐẶT RA ĐỂ ĐO** năng lực suy luận trật tự (trả lời đúng câu hỏi của thầy *"làm sao model biết trật tự các màn?"*), **KHÔNG khẳng định** N-ảnh là nhu cầu deploy phổ biến. Hợp đồng sản phẩm với người dùng vẫn là `1 ảnh + 1 câu hỏi → hướng dẫn`.

→ **Đa bước KHÔNG còn là future-work.** Future-work chỉ còn đúng 3 mục: (1) chấm định lượng tiếng Việt, (2) world-model tự huấn luyện (AGENT-NSI), (3) nhánh web Mind2Web.

## A0b. Vì sao ta có *đúng* bộ metric này (không phải bịa ra ngẫu nhiên)

Ta **không tự chế** tiêu chí. Ta **kế thừa khung đánh giá** của một bài **bình duyệt ở journal hàng đầu ngành**:

> ✅ **Chim, Ive, Liakata. "Evaluating Synthetic Data Generation from User Generated Text." *Computational Linguistics* 51(1):191–233, MIT Press, 2025.**
> (*Computational Linguistics* là journal Q1 lâu đời của ngành NLP — độ tin cậy rất cao.)

Bài đó giải đúng bài toán của ta: **đánh giá văn bản nhân tạo khi KHÔNG có đáp án mẫu.** Khung của họ gồm:
- **Intrinsic (nội tại):** *Meaning preservation* (giữ đúng nghĩa), *Style preservation* (giữ văn phong), *Divergence* (khác biệt với nguồn).
- **Extrinsic (ngoại tại):** hiệu quả khi đem đi làm tác vụ.

**Văn bản hướng dẫn máy sinh ra chính là "synthetic text".** Ta **ánh xạ** khung đó sang bài toán ảnh→tutorial:

| Trục gốc (Chim et al., ✅ CL 2025) | → Tiêu chí của ta | Diễn giải |
|---|---|---|
| Meaning preservation | **Grounding + Hallucination** | hướng dẫn "đúng nghĩa" = thao tác đúng nút *có thật* |
| Style preservation | **Clarity / Format** | đánh số, có động từ hành động, dễ đọc |
| Divergence | **(diversity, tuỳ chọn)** | tránh lặp khuôn — *tái diễn giải* vì ta không có corpus tham chiếu |
| Extrinsic | **Task Success → Tier A (AndroidControl)** | tới đúng màn hình đích — chấm **reference-based** (có gold trajectory) trên AndroidControl, thuộc nhánh **DG2** |

→ **Đây là cái "căn cứ" thầy hỏi:** bộ metric của ta **bắt nguồn từ một khung bình duyệt**, rồi mỗi tiêu chí được hiện thực hoá bằng **một metric cụ thể cũng từ bài bình duyệt**. Không có chỗ nào "tự nghĩ ra".

---

## A1. GROUNDING — "chỉ có đúng chỗ không?"

**Metric: Point-in-BBox Accuracy** (độ chính xác điểm-trong-ô).
- **Dùng để:** kiểm toạ độ máy định bấm có rơi đúng ô của nút thật không.
- **Nguồn:** ✅ Cheng et al., *SeeClick*, **ACL 2024** (giới thiệu benchmark ScreenSpot gốc). *(ACL = một trong những hội nghị hàng đầu ngành NLP.)*
- **Nói nôm na:** "bbox" = cái ô chữ nhật bao quanh một nút (toạ độ 4 góc, tính bằng pixel). "Point-in-bbox" = kiểm xem **dấu chấm** (chỗ máy định bấm) có nằm **lọt trong ô** đó không — như chơi ném phi tiêu trúng đích.
- **Vì sao chọn:** đây là **chuẩn de-facto** để đo grounding GUI; và nó **chỉ cần toạ độ ô (bbox)** — đúng thứ MobileViews cho sẵn, **không cần đáp án mẫu**.
- **Áp dụng (ví dụ eTax):** máy bảo "bấm *Tra cứu nghĩa vụ thuế*" tại điểm (x,y). Mở VH thật → nút đó có ô bao `[x1,y1,x2,y2]`. **Đúng** nếu `x1≤x≤x2 và y1≤y≤y2`. → `Accuracy = số bước đúng / tổng số bước`.
- **Ví dụ áp dụng (EX-A, màn-0 eTax) *(minh hoạ — không phải record thật)*:** máy định bấm tại **(405, 915)**; nút "Tra cứu" trong VH có ô bao **[270, 820, 540, 1010]**. Vì `270≤405≤540` và `820≤915≤1010` → **điểm rơi trúng ô → tính ĐÚNG**.

---

## A2. HALLUCINATION — "có bịa nút không?"

**Metric chính: Hallucinated-Element-Rate (HER)**, phái sinh từ **CHAIR**.
- **Dùng để:** đo tỷ lệ máy nhắc tới nút không có thật.
- **Nguồn:** ✅ Rohrbach et al., *Object Hallucination in Image Captioning*, **EMNLP 2018**. *(CHAIR là metric kinh điển đo "bịa vật thể" trong mô tả ảnh.)*
- **Nói nôm na:** "hallucination" (ảo giác) = máy **bịa** ra một nút không hề có trên màn hình rồi bảo người dùng bấm. HER = tỷ lệ nút bịa trên tổng số nút máy nhắc tới — càng thấp càng tốt.
- **Ý tưởng gốc:** CHAIR = (số vật thể nhắc tới mà ảnh không có) / (số vật thể nhắc tới). Ta thay "vật thể" bằng "nút UI", "ảnh" bằng "cây VH".
- **Áp dụng:** trích các nút máy nhắc → đối chiếu danh sách nút thật trong VH. `HER = số nút bịa / số nút nhắc`. Báo dạng **faithfulness = 1 − HER** (cao = tốt).
- **Ví dụ áp dụng (EX-A, màn-0 eTax) *(minh hoạ — không phải record thật)*:** tutorial nhắc **3 nút** — "Tra cứu", "Đăng nhập", "Cài đặt". Đối chiếu VH: "Tra cứu" và "Đăng nhập" có thật, nhưng **"Cài đặt" không có trong VH** (máy bịa) → `HER = 1/3 ≈ 0.33`, tức faithfulness = 2/3.

**Metric kèm bắt buộc: Coverage/Recall** (chống "không bịa nhưng bỏ sót hết").
- **Nói nôm na:** Coverage = "độ phủ" — tutorial có nhắc **đủ** các nút quan trọng cần dùng không, hay bỏ sót. HER chống *bịa thừa*; Coverage chống *thiếu sót*. Hai cái bù nhau.
- **Dùng để:** phạt tutorial nói "1. mở app" rồi dừng — *không bịa gì* nhưng *vô dụng* (HER một mình sẽ chấm cao oan).
- **Nguồn:** ✅ *VALOR-EVAL* (Qiu et al., **Findings of ACL 2024** — đã xác nhận) — mở rộng CHAIR thêm chiều "độ phủ". (Coverage là khái niệm mượn, không phụ thuộc venue cụ thể.)
- **Ví dụ áp dụng (EX-A, màn-0 eTax):** giả sử để hoàn thành việc cần dùng 2 nút thật ("Tra cứu", "Đăng nhập"). Nếu tutorial chỉ nói "bấm Đăng nhập" rồi dừng → HER = 0 (không bịa) nhưng **Coverage = 1/2** (bỏ sót "Tra cứu") → bị phạt đúng chỗ.

**Metric khớp tên tốt hơn: ALOHa** (dùng cho khâu so khớp tên nút).
- **Nói nôm na:** vấn đề là máy hay gọi nút bằng tên khác chữ trong VH (VH ghi "Cài đặt" nhưng máy nói "icon bánh răng"). So chuỗi thô sẽ chấm SAI dù ý đúng. ALOHa dùng **nghĩa của từ** (embedding) để khớp thông minh, rồi ghép cặp tối ưu (Hungarian — thuật toán ghép 1-1 sao cho tổng độ giống cao nhất).
- **Dùng để:** khớp tên nút thông minh — "bấm icon bánh răng" vẫn khớp được nút nhãn "Cài đặt".
- **Nguồn:** ✅ Petryk et al., *ALOHa*, **NAACL 2024**. Dùng embedding + ghép Hungarian thay vì so chuỗi thô.
- **Ví dụ áp dụng (EX-A, màn-0 eTax):** máy viết "bấm vào *mục tra cứu thuế*"; VH có nút nhãn "Tra cứu nghĩa vụ thuế". So chuỗi thô → khác nhau → trượt; ALOHa thấy nghĩa gần (similarity cao) → **khớp đúng**, không bị tính oan là bịa.

**Metric cho quan hệ/chuỗi (tutorial dài): FActScore.**
- **Nói nôm na:** với tutorial dài, máy không chỉ nêu nút mà còn nói quan hệ ("bấm X **thì mở ra** Y"). FActScore xé câu dài thành các **mệnh đề nguyên tử** (atomic claim — câu khẳng định nhỏ nhất, kiểm đúng/sai độc lập) rồi chấm từng mệnh đề → điểm = tỷ lệ mệnh đề đúng.
- **Dùng để:** kiểm từng mệnh đề kiểu "bấm X mở ra menu Y" với VH (thuộc **nhánh đa bước DG2**, nối với Tier A/B ở A4).
- **Nguồn:** ✅ Min et al., *FActScore*, **EMNLP 2023**. Tách hướng dẫn thành các "atomic claim" rồi kiểm từng cái với VH.
- **Ví dụ áp dụng (EX-B, đa bước Đồng hồ):** câu "bấm *Đồng hồ* sẽ mở tab *Báo thức*, rồi bấm *+* để thêm" tách thành 3 claim: (1) có nút "Đồng hồ", (2) nó mở "Báo thức", (3) có nút "+". Kiểm từng claim với VH các màn → FActScore = số claim đúng / 3.

*(Triangulate thêm: ✅ POPE — Li et al. EMNLP 2023; ✅ SummaC — Laban et al. TACL 2022; ✅ SelfCheckGPT — Manakul et al. EMNLP 2023. Đều peer-reviewed, dùng làm kiểm chứng phụ.)*

---

## A3. CLARITY / FORMAT — "có rõ ràng, đúng định dạng không?"

**Metric cứng: IFEval** (kiểm định dạng bằng luật).
- **Nói nôm na:** IFEval chấm bằng **luật cứng** (lập trình if-else), không dùng AI nên chạy lại bao nhiêu lần cũng ra y hệt. Nó chỉ kiểm *hình thức* (có đánh số chưa, có động từ chưa), KHÔNG kiểm nội dung đúng/sai.
- **Dùng để:** kiểm tự động định dạng — có đánh số 1,2,3? mỗi bước bắt đầu bằng động từ ("Bấm", "Chọn")? mỗi bước 1 hành động? → báo % đạt. **Không cần AI, tái lập 100%.**
- **Nguồn:** ⚠️ Zhou et al., *IFEval*, arXiv:2311.07911 (Google) — *preprint nhưng được dùng cực rộng làm chuẩn instruction-following*.
- **Ví dụ áp dụng (EX-A, màn-0 eTax) *(minh hoạ — không phải record thật)*:** tutorial "1. Mở app eTax 2. Bấm Tra cứu 3. Đăng nhập" → đạt 3/3 luật (có đánh số, mỗi dòng mở đầu bằng động từ, mỗi dòng 1 hành động) = 100%. Nếu viết "Vào phần thuế rồi đăng nhập và kiểm tra" (không đánh số, gộp 3 hành động) → trượt luật đánh số → % giảm.

**Metric mềm: G-Eval** (AI chấm độ rõ).
- **Nói nôm na:** G-Eval = nhờ chính một LLM đóng vai "giám khảo" chấm điểm độ dễ hiểu theo một bảng tiêu chí (rubric). Bù cho IFEval (chỉ chấm hình thức) — nhưng vì là AI chấm AI nên phải kiểm lại bằng người.
- **Dùng để:** một LLM chấm độ rõ (clarity) 1–5 theo rubric.
- **Nguồn:** ✅ Liu et al., *G-Eval*, **EMNLP 2023**.
- **Cảnh báo:** tương quan với người chỉ ~0.514 (trên bộ SummEval) → phải **tự kiểm bằng track chuyên gia** (A5) trước khi tin.
- **Ví dụ áp dụng (EX-A, màn-0 eTax):** đưa tutorial 3 bước cho LLM-giám-khảo kèm rubric "1=rối, 5=rõ ràng mạch lạc". Bản đánh số rõ, mỗi bước 1 hành động → chấm 5/5; bản viết gộp một đoạn dài → chấm 2/5.

**(Thống kê mô tả: Flesch/FKGL — ✅ Kincaid 1975 / Flesch 1948 — chỉ để mô tả, KHÔNG dùng cho tiếng Việt.)**

---

## A4. DG2 — SUY LUẬN TRẬT TỰ MÀN (reference-based) + Tier A tham chiếu

Đo năng lực đa bước **cần một chuỗi thao tác vàng** (gold trajectory — chuỗi thao tác mẫu do dataset cung cấp). Tình huống chia làm hai:
- **DG1 (MobileViews, màn-0): KHÔNG có gold tutorial.** MobileViews không có chuỗi vàng theo từng câu hỏi → ở nhánh này ta chấm bằng VH-silver như A1–A3.
- **DG2 (AndroidControl, NeurIPS 2024): CÓ gold mỗi bước.** AndroidControl cung cấp **episode đa bước + gold action mỗi bước** → vừa cho **thứ tự màn vàng có sẵn** (để chấm suy luận trật tự một cách reference-based), vừa cho **Step-SR** (Step Success Rate). → **Đa bước đã vào scope chính**, KHÔNG còn là future-work.

DG2 gồm **trục chính (suy luận trật tự)** + **trục tham chiếu (Tier A)**:

### A4.1 — Trục CHÍNH: suy luận trật tự màn (Screen-Order Inference)

**Bài toán:** cho **N ảnh ĐÃ XÁO TRỘN** của 1 luồng đa bước + mục tiêu → model phải (1) suy ra **thứ tự đúng** của các màn, (2) sinh hướng dẫn từng bước theo thứ tự đó. Vì AndroidControl đã có **thứ tự màn vàng**, ta chỉ việc **xáo trộn rồi đo model có xếp lại đúng không** — chấm reference-based hợp lệ.

**Hai chế độ để đo "cái giá của việc không biết trật tự":**
- **ORACLE-ORDER (mốc trần / skyline):** đưa N ảnh **ĐÃ SẮP ĐÚNG** + mục tiêu → model chỉ việc sinh hướng dẫn (không phải tự xếp).
- **SELF-ORDER (thật):** đưa N ảnh **xáo trộn** → model tự xếp rồi mới sinh.
- **ordering gap** = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = **"cái giá của việc không biết trật tự"**. *Sanity cứng:* ORACLE-ORDER ≥ SELF-ORDER ở **mọi episode** (vi phạm = bug). *Cảnh báo floor-effect:* gap chỉ có nghĩa nếu metric tutorial **nhạy** với thứ tự; nếu không, **τ-b là trục chính, gap chỉ phụ**.

**HEADLINE = Kendall τ-b** (đo độ tương quan thứ hạng giữa thứ tự model xếp và thứ tự vàng).
- **Nguồn:** ✅ Kendall (1938) — hệ số kinh điển; + ✅ Gao et al., **NAACL 2025** (đã có trong `01_metrics` Track B) dùng τ cho bài sắp thứ tự. *(Kendall τ-b xử lý đúng trường hợp có "hoà" — nhiều màn cùng hạng.)*
- **Vì sao KHÔNG dùng pairwise-accuracy thô làm headline:** nó **tautology** (nếu xếp đúng phần lớn cặp thì hiển nhiên cao) và không phạt đủ mạnh các đảo cặp quan trọng. τ-b là chuẩn được công nhận cho tương quan thứ hạng.
- **Vì sao BỎ Exact-Order-Match (EM) khỏi headline:** EM quá khắc nghiệt và nhiễu — N=3 thì EM ngẫu nhiên đã ~17% (1/6 hoán vị), N≥6 thì EM gần như ~0 dù model xếp gần đúng → không phân biệt được "sai 1 cặp" với "sai hết". τ-b biến thiên mượt, đọc được.
- **Metric PHỤ:** **pairwise-order-accuracy** (tỷ lệ cặp xếp đúng) + **position-accuracy@correct-place** (tỷ lệ màn nằm đúng vị trí). Báo kèm để bổ trợ, không làm headline.

**CHẤM THEO THỨ-TỰ-BỘ-PHẬN (partial-order-aware) — bắt buộc:** không phải cặp màn nào đảo cũng là sai.
- Chỉ **PHẠT khi sai cặp BẮT BUỘC** (gating / drill-down: đảo là sai thật). Cặp **TỰ-DO** (làm trước-sau đều được) thì **đảo vẫn tính ĐÚNG**.
- Để biết cặp nào bắt buộc → phát hiện quan hệ **gating** (phải qua màn A mới tới B) và **drill-down** (B là chi tiết của item ở A) — trùng với hệ **ordering-cues** ở Phần C.
- **HEADLINE τ-b chỉ tính trên CẶP BẮT BUỘC**; báo **THÊM τ-b-thô** (so với thứ tự gốc trên toàn tập) làm **"điểm sàn"** robustness.
- **Ví dụ minh hoạ:** điền **Email** và **SĐT** là hai ô độc lập → model xếp Email-trước-SĐT hay ngược lại đều **ĐÚNG** (cặp tự-do). Ngược lại, **đăng-nhập-TRƯỚC** rồi mới **xem-kết-quả** → nếu model đảo (xem trước, đăng nhập sau) là **SAI thật** (cặp bắt buộc — gating).

**Trục N (số ảnh):** **loại N≤2** (N=2 chỉ có đúng 1 cặp → τ-b chỉ nhận {−1,+1}, vô nghĩa). Trục N thực tế **N ∈ [3, ~10]**. Vì AndroidControl không công bố số đếm theo từng N, phải **tự đếm histogram độ dài episode** (việc tuần-1, cổng **KN**) và báo số episode còn lại ở mỗi mốc N.

**Chất lượng tutorial từng màn** (sau khi đã xếp) vẫn chấm đầy đủ: grounding (point-in-bbox, A1), hallucination (HER+coverage, A2), format (IFEval, A3). Vì grounding chấm **đầy đủ mọi màn**, đây là điểm **mạnh hơn** cách đoán-mù cũ (không còn màn nào không quan sát được). Mỗi số kèm **"recall detector = X% (K1)"** + báo RAW vs ORACLE.

  - **Ví dụ áp dụng (EX-B, đa bước Đồng hồ — luồng 3 màn):** lấy episode "đặt báo thức" gồm 3 màn, **xáo trộn** rồi đưa cho model + mục tiêu. SELF-ORDER: model xếp lại được 2/3 cặp đúng thứ tự, đảo cặp "mở Đồng hồ ↔ vào tab Báo thức" (cặp gating, là sai) → τ-b (trên cặp bắt buộc) phản ánh đúng. ORACLE-ORDER: đưa 3 màn đã sắp đúng → model chỉ sinh hướng dẫn → chất lượng cao hơn. **ordering gap** = chênh lệch hai chế độ = giá của việc tự xếp.

### A4.2 — Trục THAM CHIẾU: Tier A teacher-forced (giữ làm chuẩn ngành)

- **Tier A — mốc trần, *teacher-forced*:** ở mỗi bước, bộ chấm **đưa cho model đúng màn thật của đáp án vàng** rồi yêu cầu đoán thao tác kế, so với gold. *("teacher-forced" = mỗi bước model luôn được đặt lại đúng trạng thái thật, không bị lệ thuộc lỗi bước trước — như học sinh làm bài mà mỗi câu đều được nhắc đáp án câu trước.)* Đây là cách đo step-wise theo **chuẩn ngành** (thầy expect). Metric: **Action-Type accuracy**, **Grounding@14%**, **Step-SR**.
  - **Ví dụ áp dụng (EX-B, đa bước Đồng hồ — chuỗi 3 bước):** mỗi bước bộ chấm cho model thấy đúng màn thật rồi hỏi thao tác kế. Model đoán đúng cả 3 → **Step-SR = 3/3**. Đây là *trần lý tưởng* vì model luôn được "đặt lại" đúng màn.
- Tier A **KHÔNG còn là "đa bước chính"** (trục chính giờ là suy luận trật tự); nó là **trục tham chiếu chuẩn ngành**. ORACLE-ORDER chính là skyline của trục ordering.

**Hai nguyên tắc khai báo trung thực:**
1. **Tier A là mốc trần (skyline) có chủ đích, KHÔNG phải năng lực sản phẩm.** Ta cố tình cho model xem màn thật mỗi bước. Nguyên tắc "VH/màn thật không vào lúc sinh" chỉ áp cho claim về **sản phẩm** (DG1 + SELF-ORDER).
2. **Không so ngang leaderboard (bảng xếp hạng công khai).** Pipeline của ta dò nút từ ảnh bằng OmniParser (recall **chưa công bố rõ, K1 tự đo — giả thuyết ~một nửa**), khác setup bảng xếp hạng → Tier A chỉ "đặt trong cùng giao thức để tham chiếu **định tính**".

*(Định nghĩa Step-SR / Action-Type / Grounding@14% mượn từ ✅ AndroidControl, NeurIPS 2024 và ✅ Mind2Web, NeurIPS 2023; ngưỡng 14% trích từ ✅ AITW, NeurIPS 2023. τ-b cho sắp thứ tự: ✅ Kendall 1938 + ✅ Gao et al. NAACL 2025.)*

---

## A5. KIỂM METRIC TỰ ĐỘNG CÓ ĐÁNG TIN KHÔNG — track chuyên gia

Để chứng minh "metric máy chấm bám sát cảm nhận người" (chính là Phụ lục A.2 của Chim et al.):
- **Best-Worst Scaling (BWS):** ✅ Kiritchenko & Mohammad, **ACL 2017** — chuyên gia chọn *tốt nhất/tệ nhất* trong nhóm 4 (tin cậy hơn thang 1–5). *Nói nôm na:* người ta khó cho điểm tuyệt đối "tutorial này 3.5 hay 4 điểm?", nhưng dễ chỉ ra "trong 4 cái này, cái nào hay nhất, cái nào tệ nhất" → ổn định hơn nhiều.
  - **Ví dụ áp dụng (EX-A, màn-0 eTax) *(minh hoạ — không phải record thật)*:** đưa chuyên gia 4 tutorial cùng câu hỏi eTax (sinh từ các nấc C1–C4). Họ chỉ chọn best/worst; từ nhiều bộ-4 suy ra thứ hạng → đối chiếu xem điểm máy (HER, G-Eval...) có xếp hạng giống người không.
- **Độ đồng thuận (IAA):** ✅ Krippendorff's α (sách kinh điển) / Fleiss κ (1971) — chứng minh các chuyên gia nhất quán.
- **Tương quan:** ✅ Spearman (1904) + Kendall τ-b — đo metric máy vs điểm người. Báo **độ rộng khoảng tin cậy (CI)** vì N nhỏ.

---

## ❖ BẢNG TỔNG: metric nào, từ đâu, độ tin cậy

| Tiêu chí | Metric | Nguồn | Venue | Tin cậy |
|---|---|---|---|---|
| Grounding | Point-in-BBox | SeeClick/ScreenSpot | **ACL 2024** | ✅ |
| Hallucination | HER (CHAIR) | Rohrbach et al. | **EMNLP 2018** | ✅ |
| Hallucination | Coverage | VALOR-EVAL | **Findings of ACL 2024** (xác nhận) | ✅ |
| Hallucination | matcher ALOHa | Petryk et al. | **NAACL 2024** | ✅ |
| Hallucination | FActScore | Min et al. | **EMNLP 2023** | ✅ |
| Format | IFEval | Zhou et al. | arXiv (Google) | ⚠️ (chuẩn rộng) |
| Clarity | G-Eval | Liu et al. | **EMNLP 2023** | ✅ |
| Validate | BWS | Kiritchenko & Mohammad | **ACL 2017** | ✅ |
| Validate | Krippendorff α / Fleiss κ | kinh điển | journal | ✅ |
| Validate | Spearman/Kendall | kinh điển | journal | ✅ |
| **DG2 trật tự (HEADLINE)** | Kendall τ-b (partial-order-aware) | Kendall; Gao et al. | **Kendall 1938** + **NAACL 2025** | ✅ |
| **DG2 trật tự (phụ)** | pairwise-order-acc + position-acc@correct-place | kinh điển | — | metric phụ |
| **DG2 Tier A** | Action-Type acc / Grounding@14% / Step-SR | AndroidControl; OS-Atlas (protocol) | **NeurIPS 2024**; **OS-Atlas ICLR 2025** | ✅ / ✅ |
| **DG2 Tier A** | ngưỡng 14% (Grounding@14%) | AITW | **NeurIPS 2023** | ✅ |

> **Ghi chú metric DG2:**
> - **Trục chính (suy luận trật tự):** **HEADLINE = Kendall τ-b** chấm **partial-order-aware** (chỉ phạt cặp BẮT BUỘC: gating/drill-down; cặp tự-do đảo vẫn đúng) — nguồn ✅ Kendall 1938 + ✅ Gao et al. NAACL 2025. Báo thêm **τ-b-thô** (toàn tập) làm điểm sàn. **BỎ Exact-Order-Match** khỏi headline (N=3 EM~17% ngẫu nhiên, N≥6 ~0). Phụ: pairwise-order-accuracy + position-accuracy@correct-place. Loại N≤2; trục N ∈ [3, ~10] (tự đếm histogram, cổng KN). **ordering gap** = ORACLE-ORDER − SELF-ORDER (sanity cứng: ORACLE ≥ SELF mọi episode).
> - **Tier A (tham chiếu):** **Action-Type accuracy** (đúng loại thao tác: bấm/nhập/vuốt…), **Grounding@14%** (điểm click trong vùng đúng với dung sai 14% — **ngưỡng 14% trích BẮT BUỘC từ ✅ AITW, NeurIPS 2023**), **Step-SR** (tỷ lệ bước đúng). *(Protocol tách Type/Grounding/SR mượn từ ✅ OS-Atlas — ICLR 2025, peer-reviewed.)* Tier A là **trục tham chiếu chuẩn ngành** (skyline = ORACLE-ORDER), KHÔNG phải đa-bước-chính.

### ❖ CAVEAT gom chung (đọc 1 lần, áp cho cả Phần A)
- **VALOR-EVAL (Coverage):** venue đã chốt = **Findings of ACL 2024** (peer-reviewed). Coverage là khái niệm mượn, không phụ thuộc venue cụ thể.
- **IFEval / OmniParser / Qwen2.5-VL / Set-of-Mark:** đều là ⚠️ preprint → trích như **hiện vật kỹ thuật ta dùng**, KHÔNG trình như đã bình duyệt. *(OS-Atlas đã bình duyệt — ICLR 2025.)*
- **G-Eval:** tương quan với người chỉ ~0.514 → phải tự kiểm bằng track chuyên gia (A5) trước khi tin.
- **Mọi số grounding** (DG1, ScreenSpot, AndroidControl/DG2) báo kèm **"recall = X%"** — recall detector UI mobile **chưa công bố rõ** (chỉ có grounding accuracy ~57% trên ScreenSpot, là chỉ số khác), nên **K1 tự đo** ở tuần 1 (cổng cứng); giả thuyết ~một nửa.
- **3 bộ → 3 hệ toạ độ (harness PHẢI quy đổi):** **MobileViews** = bbox **pixel** `[left,top,right,bottom]` (root `[0,0,1080,1920]`); **ScreenSpot** = bbox **chuẩn hoá 0–1** `[x_min,y_min,x_max,y_max]`; **AndroidControl** = **toạ độ điểm click `(x,y)`** trong gold action. Vì format khác nhau, code chấm phải **convert về cùng hệ** trước khi so point-in-bbox — và phải **ghi rõ trong phần phương pháp** để không nhầm lẫn khi đọc số grounding giữa 3 bộ.

→ **Thông điệp với thầy:** *"Toàn bộ xương sống đánh giá của em đứng trên các bài bình duyệt ở những hội nghị/journal hàng đầu (ACL, EMNLP, NAACL, CL journal). Không có metric nào em tự nghĩ ra."*

---

# PHẦN B — DATASET: 3 bộ vai cố định (DG1 + DG2)

> **❖ KHAI BÁO 1 LẦN (áp cho toàn Phần B):** mọi mục "**Ví dụ áp dụng (EX-A — eTax)**" / "**Ví dụ áp dụng (EX-B — Đồng hồ)**" là **ví dụ MINH HOẠ tự soạn** minh hoạ *cách chấm*, **KHÔNG phải record có thật**. Các con số có thật của dataset (root VH `[0,0,1080,1920]`, episode `cruisedeals`, mẫu ScreenSpot `'close'` bbox `[0.948,0.144,0.994,0.207]`) được ghi rõ nhãn "**record thật**" ngay tại mục tương ứng bên dưới và trong `02_datasets.md` / **HỘP-THẬT**. Dưới mỗi mục dễ trích lẻ vẫn lặp hậu tố "(minh hoạ)" để khỏi nhầm khi đọc rời.

## B0. Thông lệ + bố cục: 3 bộ, mỗi bộ một vai

- Trong ML/NLP/CV, paper thực nghiệm thường **đánh giá trên ≥2 benchmark** để chứng minh *tính tổng quát* (không ăn may trên 1 bộ). Dùng **1 bộ** chỉ ổn khi đó là *chuẩn mặc định* của bài toán.
- **Chốt cho luận văn này: dùng 3 bộ, mỗi bộ một VAI cố định** — phục vụ hai đóng góp DG1/DG2 (xem A0):

| Bộ | Vai trò | Phục vụ |
|---|---|---|
| **MobileViews** ⚠️ (preprint, ghi rõ v1/v3 khi trích) | ảnh + VH + bbox pixel → **màn-0** | **DG1** |
| **AndroidControl** ✅ (NeurIPS 2024) | episode đa bước + **thứ tự màn vàng** + gold action mỗi bước | **DG2** (suy luận trật tự + Tier A tham chiếu) |
| **ScreenSpot** ✅ (SeeClick, ACL 2024) · **ScreenSpot-v2** ✅ (OS-Atlas, ICLR 2025) | đối chứng grounding (point-in-bbox) + bù credibility | đối chứng DG1 |

- Lý do **kép** vẫn giữ: (1) theo thông lệ ≥2 bộ; (2) **vá đúng điểm yếu credibility** của MobileViews (xem B1).
- *(AITW NeurIPS 2023 **phân vai đôi**: (a) **NGUỒN NGƯỠNG 14%** = citation BẮT BUỘC cho Grounding@14%; (b) dataset đối chứng = TÙY CHỌN. Mind2Web = future-work nhánh web.)*

## B1. Bộ chính — MobileViews ⚠️ (mạnh về dữ liệu, YẾU về credibility)

- **Là gì:** bộ GUI mobile (Android) **quy mô lớn** (1.2M màn / 30K app), mỗi màn có **ảnh + cây VH + toạ độ pixel + cờ tương tác** — *đúng thứ làm thước đo grounding*.
- **Venue:** ⚠️ **chỉ là preprint arXiv:2409.14337 — CHƯA bình duyệt.** **Đây là điểm yếu thầy có thể bắt.**
- **Schema THẬT (record thật):** mỗi màn = ảnh + `state_*.json` (View Hierarchy). Mỗi node có `viewClass` / `text` / `bounds` **pixel** dạng `[left,top,right,bottom]` / `clickable`; **root bounds thật = `[0,0,1080,1920]`** (khung màn chuẩn 1080×1920). Giá trị `text` của node con KHÔNG in trong tài liệu MobileViews → muốn lấy ví dụ node thật phải tải 1 shard mới có (việc trong checklist).
- **Ví dụ một bản ghi *(minh hoạ — số tự soạn, không phải record thật)*:** `0.jpg` + `0.json` chứa `viewHierarchy` → node `{viewClass:"Button", text:"Tra cứu nghĩa vụ thuế", bounds:[270,820,540,1010], clickable:true}`.
- **Mạnh:** quy mô + app hiện đại (2024) + bbox pixel + license MIT, tải dễ. **Yếu:** preprint; nhãn do dò tự động nên có thể nhiễu; không có câu hỏi use-case (phải tự soạn).
- **Ví dụ áp dụng (EX-A, màn-0 eTax) *(minh hoạ — không phải record thật)*:** lấy 1 màn eTax + tự soạn câu hỏi "Kiểm tra đã nộp thuế chưa thì vào đâu?". VH cho ô bao nút "Tra cứu" = **[270,820,540,1010]** → dùng làm "đáp án bạc" để chấm point-in-bbox (405,915) và HER (phát hiện nút "Cài đặt" bịa) như A1/A2.

## B2. Bộ thứ hai — chọn 1 bộ PEER-REVIEWED để vá credibility + tăng tổng quát

Hai ứng viên, đều ✅ bình duyệt và đều có toạ độ:

| Bộ | Venue | Nói về gì | Vai trò bổ trợ |
|---|---|---|---|
| **ScreenSpot** (trong SeeClick) | ✅ **ACL 2024** | benchmark *grounding GUI* (mobile/web/desktop): câu lệnh → ô đúng | **chuẩn hoá & kiểm metric grounding** trên một bộ đã bình duyệt |
| **Rico** | ✅ **UIST 2017** (kinh điển) | 66K màn Android **có VH + bbox** | **mỏ neo VH mobile đã bình duyệt** — đối chứng cho MobileViews |

- **Khuyến nghị: MobileViews (chính) + ScreenSpot (đối chứng grounding).** Vì ScreenSpot **đúng việc** ta cần (đo điểm-trong-ô) và là **ACL 2024** → câu chuyện thành: *"số liệu grounding của em được hiệu chỉnh/đối chứng trên một benchmark đã bình duyệt; MobileViews cung cấp quy mô + VH đầy đủ."*
- **Mẫu THẬT (record thật):** một mẫu ScreenSpot có `instruction:"close"`, `bbox:[0.948,0.144,0.994,0.207]` (**chuẩn hoá 0–1**, dạng `x_min,y_min,x_max,y_max`), `data_type:"icon"`, `source:"Windows"` (nguồn: bộ `rootsautomation/ScreenSpot` trên HuggingFace). **Lưu ý format:** bbox ScreenSpot là **toạ độ chuẩn hoá 0–1** — **KHÁC** format **pixel** `[l,t,r,b]` của MobileViews → harness phải quy đổi trước khi so.
- **Ví dụ áp dụng (ScreenSpot) *(minh hoạ — không phải record thật)*:** chạy đúng phép đo point-in-bbox của EX-A (điểm (405,915) ∈ ô [270,820,540,1010]) trên ScreenSpot để báo một con số grounding **trên benchmark đã bình duyệt** — đối chứng cho con số đo trên MobileViews, chứng minh không phải "ăn may trên 1 bộ".
- *(Nếu thầy muốn mỏ neo VH mobile bình duyệt thay vì benchmark grounding → thay ScreenSpot bằng Rico.)*

## B2b. Bộ cho nhánh suy luận trật tự — AndroidControl ✅ (NeurIPS 2024, mạnh credibility)

- **Là gì:** bộ **episode đa bước** GUI mobile, mỗi **bước có gold action** (thao tác vàng) và **thứ tự màn vàng** — đúng thứ cần để chấm **reference-based** cho DG2.
- **Venue:** ✅ **NeurIPS 2024 — đã bình duyệt** → là **trụ credibility** cho phần đa bước (bù việc MobileViews là preprint).
- **Episode THẬT (record thật — gold, DÙNG LÚC CHẤM):** goal `"On cruisedeals, view cruise schedules for a four-night trip from New York to Canada"` → **B1** `{action_type: open_app, app_name: CruiseDeals}` → **B2** `{action_type: click, x:313, y:742}` → **B3** `{action_type: swipe, direction: up}` (nguồn: README `android_control` của Google Research). **Lưu ý format:** gold action AndroidControl ghi **toạ độ điểm click `(x,y)`** trong action — **KHÁC** bbox pixel (MobileViews) và bbox 0–1 (ScreenSpot). Đây là chuỗi vàng dùng làm "thước" reference-based khi chấm DG2.

**Vì sao đúng bộ này cho suy luận trật tự:** episode đã có **thứ tự màn vàng** sẵn → ta chỉ việc **xáo trộn N ảnh của episode** rồi đo model xếp lại có khớp thứ tự gold không (chấm bằng τ-b). Đây là lý do AndroidControl khả thi cho trục chính, không phải bịa thêm nhãn.

**Số liệu quy mô (đã verify, có nguồn):** ✅ Li et al., *"On the Effects of Data Scale on UI Control Agents"*, **NeurIPS 2024 D&B** (arXiv 2406.03679) — **15,283 episode / 833 app**; train **13,604 episode / 74,722 step**; **mean ~5.5 step/episode** (Table 1 ghi 4.8; tính lại từ train = 5.49); **percentile-5 = 1 step**, **percentile-95 = 13 step**. So sánh độ dài: AndroidControl ~5.5 < AITW ~6.5 < Mind2Web ~7.3 action/task. *(Lưu ý: paper KHÔNG công bố số đếm theo từng N → phải **tự đếm histogram** ở tuần-1, cổng **KN**.)*

  - **Ví dụ áp dụng (EX-B, đa bước Đồng hồ) *(minh hoạ — không phải record thật)*:** lấy 1 episode "đặt báo thức" gồm 3 màn có thứ tự gold. **Xáo trộn** 3 ảnh + mục tiêu → SELF-ORDER: model tự xếp, đảo cặp gating "mở Đồng hồ ↔ tab Báo thức" (sai) → τ-b phản ánh; ORACLE-ORDER: đưa 3 màn đã sắp đúng → chỉ sinh hướng dẫn. **ordering gap** = chênh hai chế độ. Chính thứ tự màn vàng của AndroidControl làm "thước".

**Ba cảnh báo phương pháp (phải xử lý, gắn với kill-test):**
1. **Partial-order (cặp tự-do vs bắt buộc):** không phải đảo màn nào cũng là sai. τ-b headline **chỉ chấm cặp bắt buộc** (gating/drill-down); cặp tự-do (vd điền 2 ô độc lập) đảo vẫn đúng — nếu không phân biệt sẽ phạt oan model. Báo thêm τ-b-thô làm điểm sàn.
2. **Episode quá ngắn (cổng KN):** rất nhiều episode chỉ 1–2 bước (percentile-5 = 1) → **loại N≤2** (N=2 chỉ 1 cặp, τ-b vô nghĩa). Phải **tự đếm histogram** để biết còn bao nhiêu episode ở mỗi mốc N ∈ [3, ~10]; nếu quá ít thì trục chính hụt power → KN là cổng.
3. **Chống leak step-index (cổng KB):** ảnh AndroidControl có thể mang metadata/thứ tự file tiết lộ thứ tự gốc. Khi xáo trộn **PHẢI strip metadata + tái mã hoá ảnh + đặt tên UUID** để model không "đọc lén" thứ tự. CI test: một detector **mù** (chỉ nhìn pixel) **không** được suy ra thứ tự tốt hơn ngẫu nhiên — nếu nó làm được thì có leak.

- **Vai tham chiếu (Tier A, xem A4.2):** chạy từng bước trên màn thật → đo **Action-Type acc / Grounding@14% / Step-SR**. *(Đây là **tham chiếu giao thức ĐỊNH TÍNH**, KHÔNG đặt ngang leaderboard — vì pipeline ta dò nút từ ảnh, recall **chưa công bố rõ, K1 tự đo, giả thuyết ~một nửa**.)* ORACLE-ORDER là skyline của trục ordering.
- **Khung điều kiện recall** (mỗi số grounding kèm "recall=X%", cổng kill-test K1) áp cho **CẢ** MobileViews, ScreenSpot **VÀ** AndroidControl.

## B2c. PRIOR-ART cho suy luận trật tự (cổng KZ') — đóng góp mới nằm ở đâu?

Trước khi tuyên bố "suy luận trật tự màn" là mới, ta đã **rà prior-art** (cổng kill-test **KZ'**). Kết luận: **KHÔNG có công trình nào trùng khít**, nhưng có một dòng lineage phải thừa nhận trung thực.

**Các công trình gần nhất (citation đã verify):**
- ✅ **Sort-Story** — Agrawal et al., **EMNLP 2016**: xếp lại một tập ảnh + caption bị **xáo trộn** về đúng thứ tự câu chuyện. *(Đây là tiền thân trực tiếp của ý tưởng "xếp ảnh xáo".)*
- ✅ **"Sequencing Multimodal Instructional Manuals"** — Wu et al., **ACL 2022**: xếp lại các **bước hướng dẫn đa phương thức** bị xáo về đúng trình tự.
- ✅ **RankGPT** — Sun et al., **EMNLP 2023**: dùng LLM **sinh permutation** (sắp xếp lại) theo một query.
- ✅ **Sentence-ordering** (Gong et al., **AAAI 2018**) + **Screen2Vec** (Li et al., **CHI 2021**) — nền lý thuyết phụ.

**Đóng khung độ MỚI (trung thực, KHÔNG over-claim):** ta **KHÔNG** claim "xếp ảnh xáo là mới" (Sort-Story đã làm). Độ mới của luận văn = **kết hợp 4 yếu tố chưa từng đặt chung**:
- (a) **domain GUI màn-hình** (không phải ảnh story/manual chung);
- (b) **điều kiện hoá theo mục tiêu/use-case** (xếp thứ tự *phục vụ một câu hỏi cụ thể*, không xếp thuần cảm quan);
- (c) gắn ordering → **SINH tutorial** từng bước (không dừng ở việc trả về permutation);
- (d) **signal-attribution** — phân tích *ordering-cue nào* giúp model xếp đúng (gating/nav/state-delta/title/drill-down).

→ Phải **thừa nhận lineage** Sort-Story / ACL 2022 / RankGPT trong phần related-work; KZ' đã **GO** với khung claim này.

## B3. "Có chắc dataset này ứng dụng hiệu quả vào bài không?" — trả lời thẳng

**Có — với điều kiện đã biết:**
- ✅ **Tính được mọi metric của Phần A** từ field thật của MobileViews (đã xác minh: bbox, label, cờ tương tác đều có).
- ✅ Mobile hợp ngữ cảnh thực tế (eTax) và là nơi VH dồi dào nhất.
- ⚠️ **Hai điều kiện phải nói rõ:** (1) **câu hỏi use-case phải tự soạn** *(chỉ MobileViews — AndroidControl/ScreenSpot đã có sẵn goal/instruction nên không cần soạn; và **tự soạn câu hỏi ≠ bịa đáp án**: ta chỉ viết phần INPUT (câu hỏi) cho ảnh có sẵn, còn **đáp án chấm vẫn là VH thật** của dataset — khác hẳn "sinh dữ liệu tổng hợp" là bịa ra ground-truth, điều luận văn TRÁNH)*; (2) mọi số grounding kèm **"có điều kiện tỷ lệ dò nút = X%"** (rủi ro số 1). → Cả hai đều có cách xử (soạn câu hỏi theo protocol; đo recall ở tuần 1).

→ **Thông điệp với thầy:** *"Em dùng 3 bộ, mỗi bộ một vai: **MobileViews** cho màn-0 (DG1, quy mô + VH + bbox), **AndroidControl** (NeurIPS 2024) cho nhánh **suy luận trật tự màn** có gold (DG2 — headline Kendall τ-b, kèm Tier A teacher-forced làm trục tham chiếu chuẩn ngành), và **ScreenSpot** (ACL 2024) để đối chứng metric grounding trên benchmark đã bình duyệt — vừa theo thông lệ ≥2 bộ, vừa bù điểm yếu MobileViews là preprint."*

---

# PHẦN C — PIPELINE: căn cứ đề xuất, có hợp metric+dataset không, các bước

## C0. Pipeline **được suy ra** từ 3 ràng buộc (không phải vẽ tuỳ hứng)

Mỗi quyết định thiết kế đến từ một ràng buộc cụ thể:

| Ràng buộc | → Hệ quả thiết kế |
|---|---|
| Lúc chạy thật **không có VH** | phải **tự dò nút từ ẢNH** (bước ①) — không được lấy nút từ VH |
| VLM **hay bịa nút** | phải **ép chỉ chọn nút đã dò** (Set-of-Mark + ràng buộc, bước ②③) |
| Phải **chấm được** bằng metric Phần A | output phải gắn **(nút → toạ độ)** để so point-in-bbox/HER với VH (bước ⑤) |

→ **Đây là "căn cứ" thầy hỏi:** pipeline là *lời giải tối thiểu* cho 3 ràng buộc trên, không phải lắp ghép ngẫu nhiên.

## C0b. Hệ chính = **ReOrder-Tutor** — thêm **Stage 0 "Screen-Ordering"** trước pipeline 5 bước

Hệ là **một đường ống duy nhất** có **input router**: **N=1** → Stage-0 rỗng → chạy thẳng pipeline 5 bước cũ (DG1 màn-0); **N≥2** → bật **Stage 0 (sắp thứ tự)** rồi mới chạy 5 bước trên từng màn (DG2).

| Khâu Stage-0 | Cơ chế | Ghi chú |
|---|---|---|
| **S0a — per-screen feature** | **TÁI DÙNG parser Stage-1/M1** | không thêm module mới |
| **S0b — ordering reasoner (CHÍNH)** | **pairwise-then-aggregate**: hỏi VLM từng cặp "màn nào trước?" + bắt **trích ≥1 ordering-cue** → tổng hợp bằng **Copeland score** | **listwise** (1 call ép permutation) làm **ĐỐI CHỨNG** chạy fair-compute |
| **S0c — order verifier** | **code thuần, KHÔNG LLM**; chu trình mâu thuẫn → **min-feedback-arc-set** xấp xỉ | đảm bảo output là thứ tự hợp lệ |

- **5 ORDERING CUES** (trả lời câu hỏi thầy *"model dựa vào đâu để biết trật tự?"*): **gating** (đăng nhập/cấp quyền trước) · **nav-affordance** (Next/Back/breadcrumb) · **state-delta** (toggle off→on, ô trống→đã điền, badge 0→1) · **title-progression** (tiêu đề theo phiếu) · **drill-down** (màn sau = chi tiết item màn trước).
- **Signal-attribution = stratification cấp một-cue:** chỉ giữ cặp phân biệt bởi **đúng MỘT cue**, đo accuracy theo nhóm cue — **KHÔNG che pixel** (che pixel tạo artifact) + phân tích lỗi mở (đọc cặp xếp sai).
- **Baseline bắt buộc:** **GOAL-ONLY** (che hết ảnh, chỉ goal+nhãn trong — nếu goal-only đã cao thì cue giao diện không phải nguồn tín hiệu) + **RANDOM-ORDER** + E2E-VLM/Self-Refine.
- Sau khi sắp xong → chạy **pipeline 5 bước cũ trên từng màn** → grounding chấm **đầy đủ mọi bước**. VH chỉ vào lúc chấm.

## C1. Mỗi bước dựa trên một kỹ thuật đã công bố

| Bước | Kỹ thuật/Tool | Nguồn | Tin cậy | Vì sao bước này tồn tại |
|---|---|---|---|---|
| ① Dò & đánh số nút | **OmniParser** | ⚠️ Lu et al. arXiv:2408.00203 (Microsoft) | preprint, code+dùng rộng | thay VH bằng "danh sách nút từ ảnh" |
| ② Vẽ số lên ảnh | **Set-of-Mark** | ⚠️ Yang et al. arXiv:2310.11441 (Microsoft) | preprint, dùng rộng | cho model "chỉ vào số" thay vì tự tả |
| ③ Sinh có ràng buộc | **Qwen2.5-VL** + constrained decoding | ⚠️ tech report 2502.13923 | preprint/model | ép không bịa được nút |
| ④ Tự sửa | **Self-Refine** | ✅ Madaan et al. **NeurIPS 2023** | peer-reviewed | sửa lỗi lặp |
| ④ Critic ngoài | **CRITIC / Woodpecker** | ✅ Gou et al. **ICLR 2024** | peer-reviewed | kiểm bằng *tín hiệu ngoài* (pixel), không tự huyễn |
| ⑤ Đổi số→toạ độ | tra bảng | — | tất định | tạo dữ liệu để chấm |

→ Các bước **lõi khoa học** (tự sửa, critic) là **peer-reviewed**; các **công cụ** (dò nút, đánh số, model) là preprint nhưng *chỉ là hiện vật kỹ thuật ta dùng* (đúng nguyên tắc ở đầu bài).

> **❖ Đâu mới là cơ chế chống-bịa CHÍNH (tránh hiểu nhầm):** cốt lõi chống bịa nằm ở **dòng ③ — SINH CÓ RÀNG BUỘC** (ép model chỉ được trỏ vào **ID nút đã dò từ ảnh** trong tập E; nút không có trong E thì model **không cách nào** sinh ra) — chứ KHÔNG phải ở khâu verify. Dòng ④ (**tự sửa + critic**) chỉ là **lưới an toàn phía sau** để bắt lỗi sót. Và phải tách rõ 3 tầng verify: **V1 = code thuần** (so khớp membership ID↔E, **KHÔNG phải LLM**) → **V2 = một LLM KHÁC** (chỉ tầng này mới là LLM, kiểm đúng-ý/intent) → **V3 = tự sửa** (≤2 vòng). Nói cách khác, **chỉ V2 dùng LLM**; đừng để người đọc hiểu nhầm "chống bịa = nhờ một LLM khác kiểm". V1 (membership tất định) vẫn là chốt an toàn bắt buộc làm.

## C2. Pipeline **khớp** metric & dataset (chứng minh không lệch)

| Metric (Phần A) | Pipeline sinh ra tín hiệu gì để chấm? |
|---|---|
| Point-in-bbox | bước ⑤ cho (nút → toạ độ) → so với bbox MobileViews ✓ |
| HER / Coverage | tập nút máy nhắc (③) so với lá VH MobileViews ✓ |
| IFEval / G-Eval | văn bản tutorial (③) ✓ |
| Kendall τ-b (DG2 trật tự) | thứ tự Stage-0 (S0b/S0c) sinh ra → so với thứ tự màn vàng AndroidControl ✓ |
| BWS (người) | các tutorial từ các nấc C1–C4 để chuyên gia rank ✓ |

→ **Mọi metric đều có "nhà sản xuất" trong pipeline, và dữ liệu chấm đều có trong MobileViews.** Không có metric nào "treo" không chấm được.

## C3. Cách kiểm pipeline có ích — thí nghiệm thang bậc (đã giải thích ở `03b` §4)
Thêm từng cơ chế (C0→C4), đo từng nấc, để biết *cơ chế nào* trả công — và **pre-register** để kết quả âm vẫn là phát hiện hợp lệ.

---

## ❖ MỘT CÂU CHỐT VỚI THẦY
> *"Bộ đánh giá của em **kế thừa khung từ một journal bình duyệt (Computational Linguistics 2025)** và hiện thực hoá bằng **các metric từ ACL/EMNLP/NAACL**; em dùng **3 dataset** (MobileViews cho màn-0/DG1, AndroidControl NeurIPS 2024 cho nhánh **suy luận trật tự màn**/DG2 — headline **Kendall τ-b** chấm partial-order-aware, kèm Tier A teacher-forced làm trục tham chiếu chuẩn ngành, và ScreenSpot ACL 2024 để đối chứng grounding — bù việc MobileViews là preprint); và **pipeline ReOrder-Tutor được suy ra trực tiếp từ ràng buộc bài toán** (thêm Stage-0 sắp thứ tự khi N≥2, một hệ duy nhất), mỗi bước có kỹ thuật nguồn, **khớp 1-1 với các metric**. **DG2 trả lời đúng câu hỏi của thầy "làm sao model biết trật tự các màn?"** bằng 5 ordering-cue + signal-attribution. Future-work em để một cách trung thực chỉ còn: **đánh giá định lượng tiếng Việt**, **world-model tự huấn luyện (AGENT-NSI)**, và **nhánh web Mind2Web**."*
