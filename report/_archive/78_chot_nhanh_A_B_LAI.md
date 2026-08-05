# report/78 — CHỐT nhánh: A (lọc-bịa) vs B (giữ-độ-đúng on-device) vs LAI

> Bối cảnh: luận văn train Qwen2.5-VL-3B (SFT-LoRA) sinh hướng dẫn sử dụng app cho người đọc, chưng cất từ gpt-4o-mini. Thiết kế pre-register (report/56) chỉ có MỘT trục = độ trung thực (không bịa tên nút, no-gold). 4 kill-test free (report/73-76) vừa lung lay chính trụ đó → report này chốt lại: giữ khung A, đổi sang B, hay LAI. Ngày: 2026-07-18.

## Phán quyết 1 dòng

**Chọn LAI, nhưng cấu trúc lại theo kỷ luật một-trụ-chính:** trục **ĐÚNG** (Step-SR-theo-tên trên AndroidControl, đóng khung **SO SÁNH CẶP tương đối** Student vs Teacher-BASE / vs Student-THÔ) lên làm **trụ chính**; **Tier 1 (LỌC vs THÔ) tụt xuống readout PHỤ gần-miễn-phí** (báo dù null); và bốn phát hiện K1/K2/OCR/VIỆC1 gói thành **một chương đóng-góp đo-lường** ("vì sao đo faithfulness-VH kiểu naïve không đáng tin"). Điều kiện bắt buộc TRƯỚC khi cam kết: một **pilot AndroidControl ~10-20 bước** phải qua hai kill-test — Step-SR không suy biến về sàn-0, và tỉ lệ map được `gold(x,y)→a11y-tree→tên-nút` đủ cao. Hỏng một trong hai → rơi về khung "nghiên cứu đo-lường + A-mô-tả", vẫn là luận văn hợp lệ nhưng yếu hơn.

Đây là **nâng cấp** so với report/71: ở 71, trục ĐÚNG còn là "phụ, hậu-đăng-ký, làm SAU". Bằng chứng K1/K2 (report/73-74) rút nền dưới trụ chính cũ (Tier 1) đủ mạnh để **đảo vai**: trục ĐÚNG lên chính, Tier 1 xuống phụ.

---

## Bảng chấm 5 tiêu chí (A · B · LAI)

Thang 1-5. Với hai dòng "Rủi ro null" và "Khả thi 3 tháng", **cao = tốt** (an toàn / dễ làm). Đây là chấm **bán-định-lượng** (kế thừa từ Mũi 4), không phải đo khách quan — dùng để so tương đối, đừng đọc như số tuyệt đối.

| Tiêu chí | A (giữ khung cũ) | B (đổi khung) | LAI |
|---|---:|---:|---:|
| Bền với K2 (teacher bịa ~0) | 1 | 4 | 4 |
| Đóng góp / tính mới | 2 | 4 | 4.5 |
| Rủi ro null (cao = an toàn) | 1 | 3 | 4 |
| Khớp yêu-cầu-train-model của thầy | 3 | 5 | 5 |
| Khả thi 3 tháng, làm một mình | 5 | 3 | 3 |
| **Tổng** | **12** | **19** | **20.5** |

**Đọc bảng:** A thua nặng ở đúng ba chỗ sợ nhất (bền-K2, rủi-ro-null, tính-mới). B và LAI ngang nhau ở hầu hết cột; LAI hơn B đúng nửa điểm nhờ **giữ được Tier 1 làm lưới phụ gần-miễn-phí** (hai student vẫn phải train dù chọn nhánh nào → readout Tier 1 tốn chi phí biên ~0). Khoảng cách B↔LAI (19 vs 20.5) **hẹp**: nếu coi rủi-ro-phình-phạm-vi nặng hơn, B thuần có thể ngang LAI. Khác biệt thực chất chỉ là "có dám tiêu gần-0 chi phí giữ Tier 1 làm lưới phụ không" — nghiêng CÓ.

---

## Vì sao chốt vậy (neo bằng chứng 4 mũi + K1-K2)

**1. A đặt toàn bộ trọng lượng lên một trụ mà bằng chứng free vừa rút nền.** Trụ chính của A là Tier 1 (LỌC vs THÔ). Chuỗi K1→K2 đánh thẳng:
- **K1 (report/73):** matcher embedding (nomic τ=0.55) yếu **cả hai chiều** — bỏ lọt 47,5% bịa gần-nghĩa + kết oan 47,5% paraphrase; phân bố điểm tương đồng của "khớp" và "bịa" **chồng lấn hoàn toàn**, không ngưỡng nào tách được. bge-m3/OpenAI chỉ đỡ chút.
- **K2 (report/74):** trên 80 màn output teacher THẬT — **0 ca bịa gần-nghĩa thật**; 35/40 ca bị matcher gắn "bịa" thực ra là **nút thật bị VH bỏ nhãn** (icon +/✓, nút mô tả). Teacher gpt-4o-mini bịa ~0-2%, **KHÔNG phải "¼"** như con số cũ; "¼" nhiều khả năng là kết-oan do matcher đọc nhầm.

Hệ quả: nếu gần như không có gì để lọc → data-LỌC ≈ data-THÔ → **Tier 1 null TẦM THƯỜNG** (null vì thiết kế bị vô hiệu, không phải null có ý nghĩa). Đây là kiểu null tệ nhất: không đọc được, không phản bác được. Hội đồng sẽ hỏi "bộ lọc của em chữa bệnh gì có thật?" và A không có câu trả lời số-dương-chắc-chắn nào ngoài Tier 2 — vốn report/53 đã tự nhận "có thể null thật".

**2. Mũi 1 (bênh-A) thừa nhận A chỉ cứu được TRỤ ĐO, không cứu TRỤ CAN-THIỆP.** Đòn cứu-A mạnh nhất là "đo bịa của chính STUDENT 3B thay vì teacher" — có văn liệu hậu thuẫn rằng model nhỏ kém trung thực hơn (scaling của hallucination). Nhưng Mũi 1 tự vạch lỗ: kể cả Student-THÔ bịa nhiều, nếu teacher bịa ~0 thì data-LỌC ≈ data-THÔ → hai student train trên gần cùng data → **Tier 1 vẫn null bất kể student bịa nhiều hay ít**. "Student bịa nhiều" chỉ giúp nếu việc-lọc thực-sự làm data khác đi — mà khác biệt chính của lọc lại là **fallback thay nút-thật bằng câu mơ hồ** (VIỆC1/report/76: 80% câu fallback chỉ lặp lại mục tiêu, circular), thứ có thể làm student **TỆ đi**. Vậy A không chết vì sai, nó chết vì **có thể null**, và cách duy nhất biết trước là chạy pilot đo-student.

**3. Trục ĐÚNG (B/LAI) MIỄN NHIỄM với phát hiện K2.** "Hướng dẫn có đúng không" đo được **bất kể teacher bịa hay không**. Neo dữ liệu: AndroidControl (Li et al., Google DeepMind, **NeurIPS 2024 Datasets & Benchmarks — peer-reviewed**, arXiv 2406.03679, CC0) có gold-action từng bước do người thật thao tác trên Pixel; ngưỡng dung sai point-in-bbox 14% từ AITW (**NeurIPS 2023 — peer-reviewed**); khớp-tên theo tinh thần SeeClick (**ACL 2024 — peer-reviewed**). Cách map (Mũi 2 đã chứng minh khả thi về kỹ thuật): lấy `gold(x,y)` → tra node clickable chứa điểm đó trong accessibility tree → đọc `text`/`content_description` = **TÊN nút thật** thao-tác-đúng đã chạm → so với tên model nói. Né hoàn toàn bộ grounder (tránh tautology tâm-bbox). Vì trục này không phụ thuộc "teacher bịa bao nhiêu", K2 không chạm được nó.

**4. B/LAI có ≥3 vật-chịu-lực độc lập; A chỉ có 1.**
- A: một trụ (bộ lọc tạo khác biệt LỌC-vs-THÔ). K2 đe doạ đúng trụ đó → cả bài lung lay.
- B/LAI: (i) **artifact model 3B on-device** sinh hướng dẫn — thoả yêu-cầu-cứng-của-thầy, tồn tại bất kể null/dương; (ii) **trục ĐÚNG** — miễn nhiễm K2; (iii) **trục TRUNG THỰC no-gold** (Tier 1 phụ + Tier 2). Một trục null, hai trục kia vẫn đứng. Cộng thêm (iv) trong LAI: **chương đo-lường K1/K2/OCR/VIỆC1** thành đóng góp có trọng lượng. Bốn nguồn nội-dung-đậu độc lập → xác suất "không có gì để viết" gần bằng 0.

**5. Tier 1 gần-miễn-phí là lý do LAI ≳ B.** Trong mọi phương án, học viên vẫn train CẢ HAI student (LỌC, THÔ) và vẫn tính faithfulness — dữ liệu đã có sẵn trên bàn. Báo Tier 1 như readout PHỤ tốn chi phí biên ~0. LAI ≈ B + một readout dự phòng gần-miễn-phí. Nguyên tắc "báo Tier 1 và Tier 2 ĐỘC LẬP để null bên này không kéo sập bên kia" đã pre-register ở report/53 — LAI là hiện thân của chính nguyên tắc đó, **không phải scope mới**.

---

## Điểm yếu lệch-miền của B — kiểm soát được không (kết luận Mũi 2)

Đây là rủi ro số 1 và là chỗ quyết định B/LAI có sống không. Kết luận Mũi 2: **kiểm soát được MỘT PHẦN, không sạch — và chỉ sống ở dạng SO SÁNH tương đối, KHÔNG phải con số Step-SR tuyệt đối.**

**Lệch miền là THẬT và LỚN, có số hậu thuẫn.** Chính bài AndroidControl (NeurIPS 2024 D&B) thiết kế 3 lát OOD: model LoRA-tuned rớt **13,3pp high-level / 5,1pp low-level** từ in-domain (71,5%/86,6%) xuống app-unseen (58,5%/78,5%); zero-shot tốt nhất (GPT-4 Turbo M3A) chỉ **42,1% HL / 55,0% LL**. *(Các con số này lấy qua fetch bản HTML arXiv một lần — PHẢI mở PDF proceedings đối chiếu từng ô trước khi trích vào luận văn.)* MobileViews→AndroidControl là cross-dataset **+** cross-task nên lệch **nghiêm ngặt lớn hơn** các số trên. Nghĩa là Step-SR tuyệt đối của student gần như chắc chắn thấp, và **thấp không quy được** về "hướng dẫn kém".

**Ba lá chắn (xếp theo độ sạch):**
1. **Đóng khung SO SÁNH CẶP (difference-in-differences).** Chấm Student-LỌC, Student-THÔ **và** Teacher-BASE trên **cùng** lát AndroidControl, **cùng** adapter output→tên. Lệch-miền + hao-adapter thành một offset chung → hiệu Student−Teacher (và LỌC−THÔ) triệt tiêu phần lớn. Estimand = **hiệu-số-cặp**, không phải mức tuyệt đối. Claim hợp lệ: "dưới cùng lệch-miền, student chưng-cất đạt/vượt teacher về ĐÚNG trong khi trung thực hơn". **Giả định load-bearing (không kiểm định được ở đây):** lệch tác động ĐỒNG NHẤT lên mọi nhánh. Sai được — gpt-4o-mini có thể bền với distribution-shift hơn model 3B, làm khoảng cách giãn ra vì lý do chẳng liên quan chưng cất. Vì MobileViews không có gold nên **không có** điểm-trong-miền để test "parallel trends". Đây là đòn giám khảo khó bác sạch → phải khai thẳng là giới hạn.
2. **Lát gần-miền, pre-register TRƯỚC khi nhìn số:** giới hạn vào **AndroidControl-Low** (chỉ dẫn từng-bước tường minh) + app-category trùng nhau. Có căn cứ số: low-level chuyển miền tốt hơn hẳn (rớt 5,1pp vs 13,3pp) vì "low-level tasks share more similarity across tasks and apps". Không pre-register định nghĩa lát = thành cherry-pick.
3. **Metric phải là khớp-tên CÓ ĐIỀU KIỆN đã-đúng-loại-thao-tác.** Action-type (tap/scroll) dễ hơn target-NAME nhiều; một student thoái-hoá "luôn đoán tap" ăn điểm action-type mà không guide tốt hơn. Không có lá chắn này thì nhánh THÔ có thể "thắng" bằng degeneracy.

**Tiền lệ phương-pháp ủng hộ đóng-khung-tương-đối:** cả dòng grounding GUI cross-domain (OS-Atlas, ScreenSpot-Pro, UGround) **không ai đọc con-số-tuyệt-đối-chéo-bộ như năng lực** — họ báo cải-thiện-tương-đối / held-out-split-trong-bộ. *(OS-Atlas & UGround ghi ICLR 2025 nhưng CHƯA tự mở OpenReview xác nhận phiên này — verify venue trước khi in "peer-reviewed"; ScreenSpot-Pro và AndroidControl-Curated là **preprint**.)*

**Khe hở còn to hơn lệch-miền — construct validity (Mũi 2 tự nhận, và tôi đồng ý đây là rủi ro chưa dập được):** kể cả TRIỆT sạch domain-shift, "step success rate" đo **thao-tác-agent-kế-tiếp của người-vận-hành**, còn đề tài là **hướng dẫn cho người ĐỌC**. Hai construct **liên quan chứ không đồng nhất**: một guide có thể đúng-sư-phạm (gọi đúng nút + giải thích luồng) mà **không khớp** thao-tác-gold nguyên-tử tại đúng step. Chưa tìm được tiền lệ trực tiếp đo "guide-cho-người" bằng gold-action-của-agent — có thể vì **chưa ai làm** (điểm mới) hoặc vì **cộng đồng coi là mismatch** (rủi ro). Chưa phân định được. → cần một **nghiên-cứu-nhỏ đối chiếu** "khớp-gold-step" vs "đúng theo người-chấm" trên vài chục mẫu TRƯỚC khi tin trục này làm trụ chính. Đây là lý do trục ĐÚNG vào ở dạng **so-sánh-tương-đối + validate-bằng-người-mẫu-nhỏ**, không phải "một cột số bơm vào bảng".

**Cách sạch nhất (tuỳ chọn nâng cấp, có giá):** nhét AndroidControl một-bước (mỗi step = một màn) **vào tập TRAIN**, chấm trên **app-unseen split có sẵn của chính AndroidControl** → held-out-in-distribution, confound tác-vụ/miền tan. Giá: đổi câu chuyện data (giờ có train trên gold-action) + vẫn còn hao-adapter format. **Chưa chốt** — chỉ ghi để cân nhắc nếu pilot cho thấy đóng-khung-tương-đối không đủ.

---

## Tính mới / đóng góp — nhánh chốt đứng ở đâu (Mũi 3)

**Xếp hạng:** tính-mới **B > A**; độ-đủ-ngưỡng-thạc-sĩ **B đủ thoải mái, A đủ-nhưng-mong-manh** (cược vào một kết quả có thể null).

**"Model 3B distilled on-device" KHÔNG còn là tính mới bán được** — cả A lẫn B đều KHÔNG được tựa vào chữ này. Ba tiền lệ peer-reviewed đã chiếm ô đó:
- **ZonUI-3B** — *A Lightweight VLM for Cross-Resolution GUI Grounding*, **WACV 2026** (đã nhận), arXiv 2506.23491. 3B, 24K mẫu, 1× RTX 4090. Nhưng output = **grounding (điểm-trong-bbox)**, không sinh hướng dẫn.
- **UI-R1** — *Enhancing Efficient Action Prediction of GUI Agents by RL*, **AAAI 2026** (ojs.aaai.org/index.php/AAAI/article/view/38816, arXiv 2503.21620). Nền Qwen2.5-VL-3B, nhưng output = **thao tác cho agent**, có gold, RL không SFT.
- **LLaVA-KD** — *A Framework of Distilling Multimodal LLMs*, **ICCV 2025**, arXiv 2410.16236. Chưng cất MLLM lớn→nhỏ nhưng **miền tổng quát**, không GUI, không đo trung thực.

→ Nếu nhánh chốt tự mô tả "chúng tôi chưng cất VLM 3B on-device cho GUI", hội đồng chỉ thẳng vào ba bài trên.

**Chỗ trống THẬT (tính mới phòng-thủ-được của B/LAI):** toàn bộ tiền lệ small-VLM-GUI (ZonUI, UI-R1, SeeClick [**ACL 2024**], LiteGUI) sinh **hành động cho MÁY thực thi**, chấm bằng gold trajectory / grounding accuracy. **Không bài nào sinh HƯỚNG DẪN nhiều-bước cho NGƯỜI ĐỌC** rồi hỏi kép: (a) có bịa nút không tồn tại không (no-gold, đối chiếu VH), (b) có khớp thao-tác-đúng của người thật không (có-gold, Step-SR-theo-tên). Cặp đánh-giá-kép đặt trên **output hiếm (hướng dẫn cho người)** là seam chưa bị scoop.
- Nửa no-gold phân định được với **FaithScore** (*Fine-grained Evaluations of Hallucinations*, **Findings of EMNLP 2024**, arXiv 2311.01477): họ verify atomic-facts bằng VQA trên chính ảnh (self-probe); ta verify bằng **nguồn có cấu trúc ngoài ảnh (View Hierarchy)** cho hành vi rủi-ro-cao (tên nút). Phân định hợp lệ.
- Landscape phải acknowledge (KHÔNG phải scoop): **LiteGUI** (arXiv 2605.07505 — **PREPRINT**) và **AutoDroid-V2** (arXiv 2412.18116 — **preprint**) là SLM-on-device-GUI gần nhất, nhưng cả hai là **agent thực thi**, không sinh hướng-dẫn-cho-người, không đo trung thực.

**A hẹp — và K2 làm hẹp thêm tới mức nguy hiểm.** Dòng "sinh-rồi-lọc-tạo-data-sạch" đã đông: **STaR** (Zelikman et al., NeurIPS 2022), **BLIP/CapFilt** (Li et al., **ICML 2022**), **KnowAda** (*Bridging the Visual Gap*, **NAACL 2025 Oral**, arXiv 2411.09018), VGA (EMNLP 2024). report/52 đã co tính-mới A về đúng 2 điểm: (a) lọc bằng nguồn NGOÀI có cấu trúc (VH) thay vì self-probe; (b) trụ thực nghiệm = trung thực khi TẮT VH lúc suy luận. K2 tấn công điểm (a) ở **tầng thực nghiệm**: teacher bịa ~0 → "phần cần lọc" gần rỗng → không có bệnh để chữa.

**Phân biệt độ-tin-cậy-citation (trung thực):**
- **Đã verify peer-reviewed phiên các mũi này:** ZonUI-3B (WACV 2026), UI-R1 (AAAI 2026), KnowAda (NAACL 2025 Oral), LLaVA-KD (ICCV 2025), FaithScore (Findings EMNLP 2024), AndroidControl (NeurIPS 2024 D&B), AITW (NeurIPS 2023), SeeClick (ACL 2024).
- **Dựa ghi-chú-đã-verify của dự án, CHƯA verify lại phiên này:** STaR (NeurIPS 2022), CapFilt/BLIP (ICML 2022), VGA (EMNLP 2024). Verify trước khi in.
- **Preprint — chỉ acknowledge landscape, ĐỪNG xếp ngang trụ:** LiteGUI (2605.07505), AutoDroid-V2 (2412.18116), ScreenSpot-Pro, AndroidControl-Curated (2510.18488). OS-Atlas / UGround (ICLR 2025) — verify OpenReview trước khi ghi peer-reviewed.

---

## Pipeline cuối theo nhánh chốt (sơ đồ + GIỮ/ĐỔI/THÊM so với report/71)

```
        ┌──────────────────────────────────────────────────────────┐
        │  XÂY DATA (chưng cất có lọc bịa) — GIỮ NGUYÊN (report/56) │
        └──────────────────────────────────────────────────────────┘
  ảnh màn MobileViews ─┐
  + câu hỏi (khử tên nút) ├─► teacher gpt-4o-mini sinh hướng dẫn thô
                        ┘             │
                                      ▼
                     ┌────────────────────────────────┐
                     │ LỚP LỌC BỊA (so tên nút vs VH) │  GIỮ — nhưng
                     │ nomic-embed, ngưỡng τ           │  vai HẠ: giờ là
                     └────────────────────────────────┘  "thành phần +
                        │ khớp (≥τ)     │ bịa (<τ)        điều-kiện-cần",
                        ▼               ▼                 KHÔNG còn là trụ
                   giữ nguyên      viết lại thành MÔ TẢ
                                   chung chung (fallback)
                                      │
                                      ▼
                     DATA-LỌC  ⇄  (đối chứng) DATA-THÔ
                                      │
                                      ▼
                     ┌────────────────────────────────┐
                     │ TRAIN — GIỮ NGUYÊN             │
                     │ Qwen2.5-VL-3B, QLoRA r=8/α=16, │
                     │ freeze-vision, LLaMA-Factory   │
                     └────────────────────────────────┘
                        │                        │
                 Student-LỌC              Student-THÔ
                        │                        │
   ┌────────────────────┼────────────────────────┼─────────────────────┐
   ▼                    ▼                         ▼                     ▼
┌──────────────┐  ┌──────────────────┐  ┌────────────────────┐  ┌──────────────┐
│ TRỤC ĐÚNG =  │  │ Tier 1: LỌC vs   │  │ Tier 2: Student vs │  │ CHƯƠNG ĐO-   │
│ TRỤ CHÍNH ★  │  │ THÔ (VH bật)     │  │ Teacher-BASE       │  │ LƯỜNG (mới)  │
│ ─────────────│  │ = readout PHỤ    │  │ TẮT VH lúc suy luận│  │ ─────────────│
│ Step-SR-theo-│  │ gần-MIỄN-PHÍ     │  │ = trung thực no-   │  │ K1: matcher  │
│ tên trên     │  │ (báo dù NULL)    │  │ gold, sign-flip    │  │  embedding   │
│ AndroidCtrl: │  │                  │  │ G=12               │  │  không tách  │
│ gold(x,y)→   │  │ ĐỔI: từ "trụ     │  │                    │  │ K2: teacher  │
│ a11y-tree→   │  │ chính" (report/56)│  │ GIỮ (report/56)    │  │  bịa ~0      │
│ TÊN thật →   │  │ xuống "lưới phụ" │  │ nhưng KHÔNG còn là │  │ OCR: ~20%    │
│ so tên model │  │                  │  │ headline duy nhất  │  │  nút vô nhãn │
│              │  │                  │  │                    │  │ VIỆC1: fall- │
│ SO SÁNH CẶP  │  │                  │  │                    │  │  back circular│
│ tương đối:   │  │                  │  │                    │  │              │
│ Student vs   │  │                  │  │                    │  │ = "vì sao đo │
│ Teacher-BASE │  │                  │  │                    │  │  faithfulness│
│ vs Student-  │  │                  │  │                    │  │  VH naïve    │
│ THÔ, cùng lát│  │                  │  │                    │  │  khó" + biện │
│ AndroidCtrl- │  │                  │  │                    │  │  minh PIVOT  │
│ Low pre-reg  │  │                  │  │                    │  │              │
│ ĐO = CÓ GOLD │  │                  │  │                    │  │  THÊM MỚI    │
└──────────────┘  └──────────────────┘  └────────────────────┘  └──────────────┘

LUẬT VÀNG (chống leak) — GIỮ, mở sang trục ĐÚNG:
  lúc SINH chỉ nạp (ảnh + goal đã khử tên nút). KHÔNG nạp VH,
  KHÔNG nạp low-level step_instruction, KHÔNG nạp action gold,
  KHÔNG nạp a11y-tree. Tất cả CHỈ vào lúc CHẤM.
```

**GIỮ nguyên (không đụng code, đã pre-register report/56):** toàn bộ khối xây-data + lọc-bịa + train hai student + Tier 2 (trung thực no-gold, sign-flip G=12). Xương sống, không thay một chữ.

**ĐỔI vai (không đổi code, chỉ đổi framing + bảng thí nghiệm):**
- Trục ĐÚNG: report/71 để "phụ, hậu-đăng-ký, làm SAU" → report/78 nâng lên **trụ chính**, đóng-khung-cặp-tương-đối, có pre-register lát AndroidControl-Low.
- Tier 1 (LỌC vs THÔ): report/56 coi là trụ / lưới-an-toàn-gần-chắc-dương → report/78 hạ xuống **readout phụ gần-miễn-phí**, báo trung thực dù null (vì K2 báo trước khả năng null-tầm-thường).
- Bộ lọc-VH: từ "đóng góp chính" → **"thành phần + điều-kiện-cần"** (đúng như report/52 đã khuyến nghị từ sớm).

**THÊM MỚI:**
- Pipeline **Step-SR-theo-tên**: parser trích (loại-thao-tác + tên-đích) từ văn xuôi guide + hàm lookup `point-in-bbox` trên a11y-tree AndroidControl. **Bộ đo này phải qua bơm-lỗi của chính nó** (Sai et al., **EMNLP 2021 — peer-reviewed**), không thì Step-SR là tự-khen.
- **Chương đo-lường** K1/K2/OCR/VIỆC1: biến bằng-chứng-âm thành đóng góp có trọng lượng khoa học + giải thích thẳng vì sao PIVOT khỏi trụ-lọc.
- **Nghiên-cứu-nhỏ construct-validity**: vài chục mẫu đối chiếu "khớp-gold-step" vs "người-chấm-đúng-guide" — điều kiện tin trục ĐÚNG.

---

## Điều kiện lật ngược (khi nào phải đổi sang nhánh kia)

**Rơi khỏi LAI → về "nghiên cứu đo-lường + A-mô-tả" (yếu hơn nhưng hợp lệ) NẾU pilot AndroidControl hỏng bất kỳ điều nào:**
- **K-domain:** Step-SR của CẢ Student lẫn Teacher-BASE suy biến về **sàn ~0** → không có tín hiệu để lấy hiệu-số → paired-design vô nghĩa, trục ĐÚNG mất lực.
- **K-map:** tỉ lệ map được `gold(x,y)→tên-nút` quá thấp — nếu gold-action thường rơi vào nút icon-only không nhãn (đúng bệnh OCR/K2 phơi ra: ~20% nút vô nhãn), mẫu số trục ĐÚNG teo lại hoặc sập. *(Giảm nhẹ: giới hạn Step-SR vào bước mà gold rơi trúng phần-tử-CÓ-tên = recall-conditioned; a11y-tree AndroidControl [người thật, Pixel] có thể giàu nhãn hơn VH-bot MobileViews — PHẢI đếm trong pilot.)*
- **K-construct:** nghiên-cứu-nhỏ cho thấy "khớp-gold-step" gần như không tương quan với "người-chấm-guide-đúng" → trục đo sai construct, không dùng làm trụ.

**Hồi sinh A một phần NẾU:** đo student (không chỉ teacher) cho **Student-THÔ bịa ≥ ~10-15%** VÀ lọc kéo xuống có ý nghĩa VÀ fallback KHÔNG làm hỏng độ-hữu-ích (kiểm bằng VIỆC1). Khi đó Tier 1 lên lại làm lưới-đồng-hạng. Nhưng **kể cả thế, tính-mới-văn-liệu của A vẫn hẹp** (Mũi 3) — điều này lay được *độ-đủ-ngưỡng* của A, không lay xếp-hạng tính-mới B>A.

**Chú ý:** K2 chỉ trên **1 miền app** (quản-lý-dự-án/chi-phí), 80 màn, **không xem được ảnh**. "Teacher bịa ~0" có thể không tổng quát sang app game / thiết-lập-hệ-thống / app nhiều icon-thuần. Nếu miền khác teacher bịa nhiều thật, điều-kiện-hồi-sinh-A dễ đạt hơn. Đừng đặt cược trụ chính vào khả năng này khi bằng-chứng hiện có nói ngược.

---

## Việc kế + cái phải hỏi thầy

**Việc kế (thứ tự thực thi, khoá TRƯỚC khi tiêu API/GPU):**
1. **PILOT AndroidControl ~10-20 bước** (✱ tốn API nhỏ — HỎI USER trước). Kill-test K-domain + K-map cùng lúc: chấm Student(giả lập/teacher) trên vài chục step, đo (a) Step-SR có > sàn-0 không, (b) tỉ lệ map được gold→tên. **Đây là cổng sống-chết của cả nhánh chốt** — làm TRƯỚC mọi thứ khác.
2. **Đếm phân bố action per-step thật** trên AndroidControl (`dg2_*.py`): tỉ lệ click/long_press/input_text (có tên để kiểm) vs scroll/wait/home/back (không tên); tỉ lệ gold-element CÓ text label. Ước cũ "30-50% bước dùng được" là ước lượng, phải đếm lại — mẫu số trục ĐÚNG có thể co đáng kể.
3. **VIỆC1 mở rộng** (report/76, free): đọc tay 30-50 câu fallback — "mô tả chung chung" có dùng được cho người không? Kill giả định load-bearing của cả lớp lọc.
4. **Nghiên-cứu-nhỏ construct-validity** (vài chục mẫu): "khớp-gold-step" vs "người-chấm-đúng-guide".
5. Chỉ khi 1-4 xanh → **cập nhật pre-register (report/56)**: khai trục ĐÚNG lên trụ chính, Tier 1 xuống phụ, định nghĩa lát AndroidControl-Low, metric khớp-tên-có-điều-kiện-đúng-loại. Commit TRƯỚC khi train thật.

**Phải hỏi thầy (không tự quyết):**
- Thầy có chấp nhận **đổi trục xác-nhận chính** từ "trung thực no-gold" (đã trình trước) sang "ĐÚNG có-gold trên dataset KHÁC (AndroidControl), đóng-khung-so-sánh-tương-đối"? Đây là thay đổi câu chuyện, không phải thay code.
- Thầy có chấp nhận **hạ bộ lọc-VH** (từng là đóng góp chính) xuống "thành phần + điều-kiện-cần", và coi **chương đo-lường K1/K2/OCR** (bằng chứng âm → vì sao naïve-VH-faithfulness khó đo) là một đóng góp?
- Thầy đánh giá thế nào về rủi ro construct-validity "đo guide-cho-người bằng gold-action-của-agent" — chấp nhận như điểm-mới hay coi là mismatch không nên làm?

---

## Rủi ro của chính bản chốt này

- **Trục ĐÚNG THỪA KẾ đúng bệnh VH-thiếu-nhãn mà OCR/K2 vừa phơi.** Bước map `gold(x,y)→a11y→tên` thất bại đúng với nút icon-only. Nếu gold-action thường rơi vào nút không tên, trục sập. Đây là **rủi ro kỹ thuật lớn nhất**, và pilot (việc 1) phải dập trước khi cam kết. Chưa chạy → chưa được coi trục ĐÚNG là chắc.
- **Giả định homogeneous-shift của mỏ-neo-teacher KHÔNG kiểm định được** (MobileViews không gold → không test parallel-trends). Giám khảo khó có thể bác: "hiệu Student−Teacher dưới lệch phản ánh độ-bền-phân-bố khác nhau theo cỡ model, không phản ánh chưng cất". Phản-bác sạch duy nhất = đưa AndroidControl vào train (đổi câu chuyện data). Chưa chốt làm.
- **Ranh giới "trụ comparative trung thực" vs "null lịch sự" MỎNG** (Mũi 2 tự nhận). "Student lọc đúng-ngang-teacher trên tác-vụ lệch-miền mà cả hai đều làm kém" có thể là phát-hiện **nhạt** chứ không phải trụ. Quyết định cuối chờ pilot: hiệu-số có **tách khỏi 0 VÀ đọc thành câu chuyện** không.
- **Nguy cơ phình phạm vi / "hai trụ loãng".** LAI có tới 3-4 nguồn nội dung → dễ thành hai-nửa-kết-quả đọc như luận văn yếu. Đây là **rủi ro TRÌNH BÀY, không phải khoa học** — quản bằng kỷ luật: MỘT trụ chính rõ (trục ĐÚNG) + MỘT phụ rõ (Tier 1) + chương đo-lường tách bạch. Người làm một mình 3 tháng phải giữ kỷ luật này, nếu không LAI mất lợi thế so với B thuần.
- **Khả thi build harness Step-SR** (parse a11y-tree, map toạ-độ→tên, so khớp, tự-validate bằng bơm-lỗi) là code **trung bình chưa từng chạy**. Nếu pilot cho thấy tốn hơn dự kiến, tiêu-chí khả-thi của B/LAI phải hạ, kéo cán cân về A-mô-tả.
- **Chấm điểm 5 tiêu chí là bán-định-lượng, tự gán thang.** Thứ tự A≪B≲LAI vững; khoảng cách B↔LAI (19 vs 20.5) đủ hẹp để nếu bạn coi rủi-ro-phình nặng hơn thì B thuần ngang LAI. Khác biệt thực chất chỉ là "có giữ Tier 1 làm lưới phụ gần-miễn-phí không".
- **Bằng chứng mỏng đã khai:** (1) tôi không đọc trực tiếp report/73-76, chỉ dựa tóm tắt đề bài — nếu K2 thực ra đã đo cả student thì một phần lập luận đổi; (2) các con số IDD/OOD AndroidControl lấy qua fetch HTML một lần, chưa đối chiếu PDF proceedings; (3) K2 giới hạn 1 miền + không xem ảnh nên "teacher bịa ~0" chưa phải kết luận toàn cục.
