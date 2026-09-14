# 138 — Tra cứu: nâng số `exec` và nâng trần phép đo (5/9/2026)

> Trả lời prompt `report/137`. Bối cảnh mới so với `137`: **chủ luận văn quyết 5/9 BỎ HẠN SOICT
> 16/9**, không chạy đối chứng `gui_sft_match`; mục tiêu duy nhất còn lại là **đóng góp mô hình cho
> luận văn với số dễ bảo vệ hơn**, thước là đóng góp phụ. Mọi ràng buộc ở `137` mục 7 vẫn giữ.
>
> Ba phép đo mới, làm hôm nay trên tệp thô, **0 giây GPU**, nằm ở mục 0. Chúng thay đổi thứ tự
> ưu tiên nên đặt trước phần tra cứu.

---

## 0. Ba số đo được hôm nay, trước khi tra tài liệu

### 0a. Trần của mọi thứ đã có trên đĩa: **60,72%**

Ghép `gui_sel` với MIN-DESC theo luật *"bước nào `gui_sel` phát `<sel>none</sel>` thì lấy câu của
MIN-DESC"* (tệp `runs/sel/score_gui_sel_seed101_raw.jsonl` + `runs/score_min_desc_seed101_raw.jsonl`,
n = 4.463):

| hệ thống | exec | so MIN |
|---|---|---|
| MIN-DESC | 60,05 | — |
| `gui_sel` | 56,13 | −3,92 |
| **ghép: `gui_sel`; `none` → MIN** | **60,72** | **+0,67** |
| ghép → S1 | 59,44 | −0,60 |
| ghép → CE2 | 60,54 | +0,49 |
| oracle `sel` ∪ `min` (biết trước ai đúng) | 66,10 | *không thi hành được* |
| oracle `sel` ∪ `min` ∪ `s1` | 68,65 | *không thi hành được* |

Quét thêm luật theo cỡ khối ứng viên (< 10 … < 120) và theo độ dài câu (< 20 … < 80 ký tự):
**mọi luật tinh vi hơn đều thấp hơn luật đơn giản** (60,12 … 60,65). ⇒ 60,72 là kịch trần
của đồ đã có; vẫn trong ô TRẮNG (dải 56,56–61,06 theo `106` (x14b)).

Trong nhóm 1.873 bước `gui_sel` bỏ cuộc (41,97%): `gui_sel` 39,78 · MIN 50,72 · S1 47,68 ·
người 71,92. Trong nhóm 2.590 bước dám chọn: `gui_sel` **67,95** · MIN 66,80 · S1 67,37 ·
người 78,49. Tức là **khi dám chọn, `gui_sel` là nhánh tốt nhất từng train**; toàn bộ thiệt
hại nằm ở việc bỏ cuộc.

### 0b. Hợp nhất hai bộ trỏ (câu B1): trần câu người **79,0 → 87,7**, S1 **52,84 → 56,71**

Tính từ tệp thô của phép B (UI-Venus, 20/8) và của UGround, cùng bước, cùng câu:

| | UGround | UI-Venus | **HỢP NHẤT** (một trong hai trúng) | cả hai trúng |
|---|---|---|---|---|
| **trần câu người**, 300 bước cổng A, luật `err ≤ 14%` (không Voronoi) | 79,0 | 74,0 | **87,7** | 65,3 |
| S1, 2.532 bước, luật đầy đủ Voronoi | 52,84 | 48,74 | **56,71** | 44,87 |
| S2 | 49,45 | 46,60 | 53,28 | 42,77 |
| Base | 42,50 | 39,06 | 46,21 | 35,35 |
| S1 − Base | 10,34 | 9,68 | **10,50** | 9,52 |

Hai bộ trỏ **bổ sung nhau thật**: chỉ 65,3% bước cả hai cùng trúng, nhưng 87,7% có ít nhất một
bên trúng. Hợp nhất nâng **mọi nhánh cùng +3,7…+3,9 pp** dưới luật đầy đủ và **giữ nguyên
khoảng cách S1−Base** (10,50 vs 10,34). ⚠️ Trần 87,7 đo dưới luật `err ≤ 14%` thuần trên 300
bước; dưới Voronoi đầy đủ và đủ 4.463 bước sẽ thấp hơn — chưa đo vì Venus chưa chấm câu người
trên đủ tập.

### 0c. Vị trí ứng viên vàng trong khối và tỉ lệ bỏ cuộc (câu A3): hình chữ U tái lập

3.198 bước có ứng viên vàng trong khối, `preds_gui_sel_seed101_touch4463.jsonl`:

| vị trí vàng trong khối | n | bỏ cuộc |
|---|---|---|
| tam phân ĐẦU | 1.315 | 27,2% |
| tam phân GIỮA | 786 | **31,4%** |
| tam phân CUỐI | 1.097 | 24,3% |
| *chỉ khối cỡ 30–40:* ĐẦU / GIỮA / CUỐI | 712 / 274 / 231 | 29,1 / **40,1** / 35,1 |

Đúng dạng "lost in the middle" của Liu và cs. (TACL 2024, mục 1). ⚠️ Hậu kiểm, chưa kiểm định,
và vị trí tương quan với cỡ khối; hàng dưới đã kiểm soát cỡ khối mà hình U vẫn còn.

---

## PHẦN 1 — Bảng tiền lệ

Quy ước cột *venue*: **đậm** = đã bình duyệt, xác minh trang/kỷ yếu; *nghiêng* = preprint arXiv,
chưa xác minh venue. Cột *chi phí* tính cho dự án này (A100 ≈ 21 s/bước lô 16; T4 chấm ≈ 5,6 h
một nhánh 4.463 bước bằng UGround-2B, ≈ 14,4 h bằng UI-Venus-7B).

### Câu A — đưa exec 56–60 lên 65–70

| # | hướng | tiền lệ | trích nguyên văn | mức tăng trong bài gốc | gần miền GUI? | chi phí ở đây | vi phạm mục 7? |
|---|---|---|---|---|---|---|---|
| A1-1 | **Ngưỡng bỏ cuộc τ chọn trên dev** (đúng thủ tục SQuAD 2.0) | Rajpurkar, Jia, Liang 2018, **ACL 2018 short, tr. 784–789** | *"At test time, models abstain whenever their predicted probability that a question is unanswerable exceeds some threshold. We tune this threshold separately for each model on the development set."* Và lý do: *"…does slightly better than simply taking the argmax prediction, possibly due to the different proportions of negative examples at training and test time."* | Không nêu số riêng; là chuẩn của mọi hệ SQuAD 2.0 | Không (QA văn bản), nhưng cấu trúc bài toán trùng khít: nhãn `none` 54,78% ở tập dạy vs 29,1% ở bước chạm | **< 1 h T4** (`kaggle_SEQSCORE_SAU_O.md`), 0 A100 | Không; đã đăng ký ở `106` (x16d) |
| A1-2 | Cùng ý, dạng điểm span vs null | Devlin và cs. 2019, **NAACL 2019** (BERT) | *"We predict a non-null answer when ŝᵢ,ⱼ > s_null + τ, where the threshold τ is selected on the dev set to maximize F1."* | SQuAD 2.0 F1 test 83,1 | Không | như trên | Không |
| A1-3 | **Hiệu chỉnh logit theo tiên nghiệm nhãn** (post-hoc, không train lại) | Menon và cs. 2021, **ICLR 2021** (spotlight) | *"…logit adjustment based on the label priors, either applied post-hoc to a trained model, or enforced in the loss during training."* Bản post-hoc là Bayes-tối ưu dưới label shift | Tăng trên long-tail CIFAR/ImageNet-LT; không có số cho QA | Không, nhưng đúng chẩn đoán: lệch tiên nghiệm dạy/kiểm | **0 GPU** sau khi có điểm τ: τ₀ = log(0,5478/0,291) ≈ **+0,63 nat** cộng vào vế ứng viên | Không |
| A1-4 | Bộ hiệu chuẩn học riêng để quyết bỏ cuộc (selective prediction) | Kamath, Jia, Liang 2020, **ACL 2020, tr. 5684–5696** | *"Our method answers 56% of questions while maintaining 80% accuracy; in contrast, directly using the model's probabilities only answers 48% at 80% accuracy."* | +8 điểm phủ ở cùng 80% chính xác | Không | ~1 h CPU trên 1.400 điểm τ (đặc trưng: margin, cỡ khối, vị trí vàng, động từ) | Không, nhưng thêm một mô hình phụ |
| A1-5 | Đọc rồi kiểm lại (verifier) | Hu và cs. 2019, **AAAI 2019** | Abstract: hệ *read-then-verify*, reader sinh xác suất no-answer + verifier kiểm câu trả lời có được đoạn văn hậu thuẫn không (trích ý, chưa lấy nguyên văn) | SQuAD 2.0 test F1 74,2, hơn mốc trước >7 điểm trên dev | Không | Cần mô hình verifier riêng: ~10–20 h A100 | Không |
| A1-6 | Tinh chỉnh có ý thức từ chối, chọn tập từ chối theo hiểu biết của chính mô hình | Zhang và cs. 2024, **NAACL 2024** (Outstanding Paper) — R-Tuning | Dựng dữ liệu từ chối ở *"knowledge intersection"* giữa tham số và dữ liệu tinh chỉnh (trích ý) | Tăng cả trả lời đúng lẫn từ chối đúng; từ chối là "meta-skill" sang miền khác | Không | Train lại ~23 h A100 | Không |
| A1-7 | **Chống từ chối quá mức** khi tinh chỉnh từ chối | Zhu và cs. 2025, **Findings of NAACL 2025, tr. 4006–4021** — GRAIT | *"avoid over-refusal to ensure questions that can be correctly answered are not rejected, thereby maintain the helpfulness of LLM outputs"* | "significantly outperforms existing RAIT methods" (không có số trong abstract) | Không | Train lại ~23 h A100 | Không |
| A1-8 | Tỉ lệ mẫu "không có đáp án" là siêu tham số phải cân | GRES, Liu, Ding, Jiang 2023, **CVPR 2023** (Highlight) | Đặt N-acc (no-target accuracy) làm thước riêng cho biểu thức không có đích | — | **Có** (referring expression, có lớp no-target) | 0 GPU: báo N-acc riêng như một cột | Không |
| A2-1 | **Hai tầng: lọc ứng viên bằng mô hình nhỏ, rồi chọn kiểu trắc nghiệm** | Deng và cs. 2023, **NeurIPS 2023 D&B** — Mind2Web / MindAct | *"a two-stage model that involves first using a fine-tuned small LM to filter the web elements and then using an LLM to select from the filtered elements in a multi-choice question answering fashion"* | Ele. Acc Cross-Task: Generation **20,2** · Classification 26,8 · MindAct Flan-T5-B **43,6** | **Có** (web GUI) | Dựng lại dữ liệu + train ~23 h A100 | Không |
| A2-2 | Cùng ý trên GPT-4V, ba cách ground | Zheng và cs. 2024, **ICML 2024** — SeeAct | Bảng 2 step-SR Cross-Task: textual choice **40,6** · image annotation 13,0 · element attributes 4,7 · oracle 65,7; ứng viên top-50 *"clustered into groups of 17 options"* | Textual choice gấp 3 image annotation | **Có** | 0 GPU (đối chiếu thiết kế) | Không |
| A2-3 | Tách grounding khỏi planning, và giá của việc bỏ inner monologue | Xu và cs. 2025, **ICML 2025** (PMLR v267) — Aguvis | AndroidControl-Low: **80,5 → 69,1** khi bỏ inner monologue; ScreenSpot 84,4 → 79,3 | −11,4 pp | **Có, chính AndroidControl** | Đã có (nhánh `<desc>`/`<sel>` là inner monologue) | Không |
| A3-1 | Thiên lệch chọn theo vị trí lựa chọn | Zheng và cs. 2024, **ICLR 2024** (spotlight) | LLM *"prefer to select specific option IDs"*; PriDe khử prior bằng hoán vị, không cần nhãn | — | Không (MCQ văn bản) | 0 GPU nếu quét τ có hoán vị | Không |
| A3-2 | **Mất giữa chừng**: ngữ cảnh dài, thông tin ở giữa bị bỏ | Liu và cs. 2024, **TACL 2024** | Hiệu năng cao nhất khi thông tin ở đầu/cuối, tụt hơn 30% khi ở giữa (multi-doc QA) | — | Không, nhưng **0c tái lập ở đây** | 0 GPU (đã đo) | Không |
| A3-3 | Đánh số/đánh dấu trực tiếp trên ảnh (Set-of-Mark) | Yang và cs. 2023, *arXiv 2310.11441* — **chưa xác minh venue** | GPT-4V + SoM zero-shot vượt mô hình RefCOCOg fine-tune | — | Có (grounding) | Dựng lại dữ liệu + train ~23 h; ⚠️ SeeAct đo image annotation **thua** textual choice 13,0 vs 40,6 | Không |
| A4-1 | Ghép mô hình có bỏ cuộc với mô hình không bỏ cuộc (cascade) | Không có tiền lệ riêng trong GUI; gần nhất là selective prediction A1-4 | — | — | — | **0 GPU, đã đo: 60,72** | Không, nhưng là hệ hai mô hình, phải khai |

### Câu B — nâng trần phép đo mà không nới tiêu chí

| # | hướng | tiền lệ | trích nguyên văn | số trong bài gốc | gần GUI? | chi phí | vi phạm? |
|---|---|---|---|---|---|---|---|
| B1-1 | **Hợp nhất nhiều lần trỏ** bằng bỏ phiếu vùng | GUI-RC, **AAAI 2026** (arXiv 2508.05615) | *"GUI-RC improves accuracy by 2-3% across various architectures on ScreenSpot benchmarks"*; Bảng 1: Qwen2.5-VL-3B **80,11 → 82,63** (⚠️ một tóm tắt thứ cấp ghi 83,57; lấy số trong bảng) | +2–3 pp, 64 mẫu, T = 0,5 | **Có** | Chấm lại 7 nhánh × 64 mẫu — không khả thi trên T4 | Không |
| B1-2 | Hợp nhất nhiều **góc nhìn** ảnh, gom cụm không gian | MVP, Zhang và cs. 2026, **CVPR 2026** | Tăng "consistently and significantly" trên ScreenSpot-Pro / UI-Vision / OSWorld-G (không có số trong abstract) | — | **Có** | như trên | Không |
| B1-3 | Hợp nhất **hai mô hình khác nhau** | Không tìm thấy tiền lệ GUI; **0b đo trực tiếp** | — | — | — | Trần đủ tập: chấm câu người bằng Venus 4.463 bước ≈ 14 h T4; mỗi nhánh thêm ≈ 14 h | Không nới hình học; nhưng trọng tài vẫn cùng họ Qwen |
| B2-1 | Bộ trỏ trả về **vùng** + verifier chọn vùng | GUI-Actor, Wu và cs. 2025, **NeurIPS 2025** | Đầu attention ghép token `<ACTOR>` với patch; *"grounding verifier to evaluate and select the most plausible action region"* | ScreenSpot-Pro 7B: 44,6 vs UI-TARS-72B 38,1 | **Có** | ⛔ Bảng 7 của bài: **có AndroidControl 47K** trong dữ liệu train | Không, nhưng bộ trỏ không sạch AC |
| B3-1 | **Trọng tài mức phần tử: điểm nằm trong hộp của phần tử vàng** | Li và cs. 2024, **NeurIPS 2024 D&B** — AndroidControl, Phụ lục D.3 | *"if the target element's coordinates are within the bounding box of the ground truth target element, it is considered as matching"* | Là thước gốc của chính bộ dữ liệu | **Chính bộ dữ liệu đang dùng** | **0 GPU** từ tệp thô + cây a11y | Không nới hình học; là luật của tác giả dữ liệu |
| B3-2 | Cùng ý, dạng "hoặc": 14% màn **hoặc** cùng hộp | Rawles và cs. 2023, **NeurIPS 2023 D&B** — AITW | Hai cú chạm bằng nhau nếu cách nhau < 14% màn **hoặc** rơi cùng hộp phần tử (hộp nở 240%) | — | **Có** | 0 GPU | Không |
| B3-3 | Làm sạch nhãn + đổi sang hộp, số nhảy ~15 pp | *arXiv 2510.18488* AndroidControl-Curated — **chưa xác minh venue** | Chuyển "Exact Point Matching" sang "Bounding-Box-based Intent Alignment"; SR ~75%, hơn bản gốc ~15% | +15 pp (theo họ) | **Chính AC** | Không dùng làm trích dẫn chính | — |
| B4-1 | LLM làm giám khảo quỹ đạo agent, hiệu chuẩn với người | Xue và cs. 2025, **COLM 2025** — Online-Mind2Web / WebJudge | Đồng thuận với người **85,7%** (o4-mini), chênh SR 3,8% | — | Có, nhưng chấm **quỹ đạo**, không chấm **câu chỉ dẫn** | Gọi API mỗi bước | ⚠️ vòng tròn nếu giám khảo cùng họ Qwen; và không có hiệu chuẩn người cho tác vụ này |
| B4-2 | Refusal grounding: bộ trỏ tự từ chối khi phần tử không có | Jedi/OSWorld-G, **NeurIPS 2025 D&B** (spotlight); VenusBench-GD *arXiv 2512.16501* | OSWorld-G có lớp *Refusal*, đầu ra `(-1,-1)`; VenusBench-GD có "refusal grounding" | — | Có | — | Jedi có AndroidControl (`CLAUDE.md`) |

### B5 — bộ trỏ mạnh tính tới 9/2026 (di động), giấy phép, có AndroidControl trong train không

| mô hình | venue | ScreenSpot-v2 (theo bài) | AndroidControl trong train? | ghi chú |
|---|---|---|---|---|
| UGround-V1-2B/7B | **ICLR 2025 oral** | 95,0/83,3 (mobile text/icon, 2B) | **CÓ, 47K** (Bảng 1) | đang dùng; nền Qwen2-VL |
| UI-Venus-Ground-7B | *arXiv 2508.10833* (tech report) | 94,1 (7B) | **KHÔNG** (đã tra 15/8) | đã dùng phép B; nền Qwen2.5-VL |
| GUI-Actor-7B | **NeurIPS 2025** | ScreenSpot-Pro 44,6 | **CÓ, 47K** (Bảng 7) | loại |
| GTA1-7B | **ICLR 2026** | 92,4 | Không thấy AC trong danh sách (Aria-UI-Web, OmniACT, UI Vision, Widget Caption, OS-Atlas-Desktop) — **chưa xác minh trọn bảng** | ứng viên bộ trỏ thứ ba; nền Qwen2.5-VL |
| Jedi | **NeurIPS 2025 D&B** | — | CÓ (`CLAUDE.md`) | loại |
| UI-TARS-1.5 | *arXiv 2501.12326* | 91,6 (7B) | **CÓ** (tích hợp AndroidControl) | loại |
| UI-Venus-1.5 / -2 | *arXiv 2602.09082 / 2609.00028* | SS-Pro 69,6 (1.5) | **chưa xác minh** | tra sau nếu cần |
| InfiGUI-R1-3B, Holo1.5 | *preprint* | 97,1/81,2 mobile (InfiGUI-R1) | **chưa xác minh** | — |

Chưa kiểm được giấy phép của GTA1, InfiGUI-R1, Holo1.5 trong lượt này.

---

## PHẦN 2 — Xếp hạng (thang 1–5, cao = tốt; cột rủi ro: 5 = ít bị phản biện nhất)

| hướng | nâng số thật | chi phí | rủi ro "chọn phương pháp cho hợp kết quả" | ghi chú |
|---|---|---|---|---|
| **A1-1/A1-2 τ trên dev** | 3 (0–3 pp thực tế, trần +9,31) | **5** (<1 h T4) | **5** — thủ tục đã đăng ký (x16d), dev ≠ one-look | chạy đầu tiên, không có gì cạnh tranh |
| **A1-3 τ₀ từ tiên nghiệm** | 2–3 | **5** (0 GPU) | **5** — giá trị suy từ lý thuyết, không nhìn điểm | báo cạnh τ chọn trên dev; nếu hai τ gần nhau là bằng chứng mạnh |
| **Train lại chỉ trên bước chạm** (hệ quả trực tiếp của Rajpurkar 2018 + Menon 2021) | **4** | 3 (41.191 mẫu ⇒ 2.575 bước ≈ **15 h A100**) | **4** — chẩn đoán đã có trước khi train, ghi ở `137` mục 4 | xem Phần 3 |
| A1-4 bộ hiệu chuẩn học riêng | 3 | 4 | 3 — thêm mô hình, nhiều đặc trưng | chỉ khi τ đơn không đủ |
| A4-1 cascade → MIN | 1 (+0,67, đã đo) | 5 | 2 — luật chọn sau khi thấy điểm | đã hết chỗ; chỉ đáng khi ghép với τ |
| A2-1 hai tầng kiểu MindAct | 3–4 | 2 (dựng lại + 23 h) | 3 | tiền lệ mạnh nhất, nhưng đổi kiến trúc |
| A3 đổi thứ tự/đánh số khối | 2 | 2 | 3 | 0c cho thấy có hiệu ứng vị trí, nhưng SeeAct cảnh báo image annotation kém xa textual |
| A1-6/A1-7 refusal-aware tuning | 3 | 2 | 3 | trùng ý với train-chỉ-bước-chạm nhưng đắt hơn |
| A1-5 verifier | 3 | 2 | 3 | — |
| **B3-1 luật hộp phần tử của chính AndroidControl** | trần → ~82–84 (đã đo: chữ nhật 14% gated **84,23**; hộp-gần-nhất 82,2 trên 698) | **5** (0 GPU) | **5** — là thước của tác giả dữ liệu, không phải luật tự đặt | thước đồng-báo; ⚠️ dưới luật lỏng Δ giữa các nhánh co lại |
| **B1-3 hợp nhất hai bộ trỏ** | trần → 87,7 (luật 14%, 300 bước) | 2 (~14 h T4 mỗi nhánh với Venus-7B) | 3 — "executable bởi ít nhất một trong K bộ trỏ độc lập" là định nghĩa phải khai từ đầu | nâng đều mọi nhánh +3,7–3,9, giữ Δ |
| B1-1/B1-2 bỏ phiếu trong một mô hình | trần +2–3 | 1 (×64 mẫu) | 4 | không đủ máy |
| B4-1 LLM giám khảo | — | 3 | 1 — vòng tròn + không có neo người | không khuyên |
| B2-1 GUI-Actor vùng | — | 2 | 2 — có AC trong train | loại |

---

## PHẦN 3 — Ba hướng làm trước

### ① τ trên dev 1.400, kèm τ₀ suy từ tiên nghiệm — hôm nay, < 1 h T4

**Thay đổi:** không đổi mô hình. Chạy `harness/kaggle_SEQSCORE_SAU_O.md` để có điểm chuẩn hoá
độ dài của mọi ứng viên và `none` trên 1.400 bước dev. Quét τ theo thủ tục (x16d): cực đại độ
đúng trên **toàn bộ** 1.400, luật null trong lưới, khoá trước khi nhìn 3.062.

**Thêm một giá trị τ₀ không cần dev**, theo Menon và cs. 2021 (post-hoc logit adjustment):
`τ₀ = log(π_train(none) / π_test(none)) = log(0,5478 / 0,291) ≈ 0,63 nat`. Cộng vào vế ứng
viên (hoặc trừ khỏi `none`). ⚠️ Điểm đang dùng là **trung bình theo token**, không phải log-xác
suất của một lớp; `none` có độ dài token cố định nên vế `none` là log-xác suất thật chia hằng,
còn vế ứng viên thì không. Vì thế τ₀ chỉ là **mốc tham chiếu**, không phải giá trị Bayes-tối ưu
đúng nghĩa; nếu τ chọn trên dev rơi gần τ₀ thì đó là bằng chứng cơ chế đúng như chẩn đoán.

**Phép đo rẻ nhất để biết sống/chết:** đường cong độ-đúng-1.400 theo τ. Nếu lift tốt nhất
< 18/1.400 (≈ 1 SE nhị thức) ⇒ luật null thắng, hướng ② mới là đường chính.

**Kỳ vọng:** exec 56,13 → **58–60** (khoảng bất định 56–63). Trần lý thuyết 65,44 không với
tới vì nhóm bỏ-cuộc-sai chỉ có `action_ok` 71,22% (câu sai động từ, ép chọn cũng không cứu).

**Sau đó, 0 GPU:** ghép `gui_sel`+τ với MIN theo luật 0a. Oracle cho phép tới 66,10, nên ghép
sau τ **có thể vượt 61,06** (mép dương yếu). Phải khoá luật ghép trên dev rồi báo trên 3.062.

### ② Train lại `gui_sel` chỉ trên 41.191 bước chạm — ~15 h A100, hạt 101

**Căn cứ đo được:** `137` mục 4 — `none` chiếm 54,78% tập dạy nhưng chỉ 29,1% trên bước chạm,
khớp tập kiểm 28,34%; mô hình phát 41,97%, nằm giữa. Đây **chính xác** là hiện tượng Rajpurkar
và cs. 2018 mô tả (*"different proportions of negative examples at training and test time"*),
và Menon và cs. 2021 chứng minh sửa tiên nghiệm lúc train tương đương sửa post-hoc dưới label
shift. 36,2% tập dạy là bước không-chạm gán `none` theo thiết kế — chúng dạy mô hình một lối
tắt "không chắc thì `none`" mà tập kiểm không thưởng.

**Thay đổi cụ thể:** lọc `gui_sel.json` giữ đúng 41.191 mẫu có `action_type ∈ {click,
long_press}` (cùng tiêu chí mẫu số 4.463 của thước). Cùng yaml, chỉ đổi `dataset`/`output_dir`.
Prompt, khối ứng viên, đầu `<sel>` giữ nguyên ⇒ **đúng một biến đổi: phân bố nhãn**. 2.575
bước × ~21 s ≈ 15 h.

⚠️ Hệ quả phải khai: mô hình không còn thấy bước không-chạm ⇒ trên 2.495 bước không-chạm của
tập kiểm (không được chấm) hành vi sẽ đổi; thước 4.463 không đụng tới, nhưng luận văn phải
nói rõ hệ thống chỉ được huấn luyện cho bước chạm.

**Phép đo rẻ trước khi tiêu 15 h:** kết quả ① là phép thử post-hoc của đúng cơ chế này. Nếu τ
(hoặc τ₀) nâng được exec ≥ 2 pp trên dev, hướng ② gần như chắc có tác dụng và có thể hơn (vì
sửa ở gradient chứ không chỉ ở ngưỡng). Nếu τ không nâng được gì, ② vẫn có thể có tác dụng
nhưng xác suất thấp hơn nhiều — khi đó cân nhắc trước khi chạy.

**Kỳ vọng:** exec **60–64** (bất định 57–66). Chạm mép DƯƠNG 62,16 là **có thể** nhưng không
chắc. Cộng ghép với MIN sau đó: thêm 0–2 pp.

⚠️ Nhãn: một hạt giống ⇒ TRẮNG theo định nghĩa (x14c). Muốn ra khỏi ô trắng phải chạy hạt 202
(thêm 15 h).

### ③ Thước đồng-báo mức phần tử theo Phụ lục D.3 của AndroidControl — 0 GPU

**Thay đổi:** thêm một cột `exec_bbox`: điểm trỏ nằm **trong hộp phần tử vàng** (cây a11y,
`all_forest_dict`), giữ nguyên `action_ok`/`toggle_ok`. Là luật của chính tác giả bộ dữ liệu
(NeurIPS 2024 D&B), nên **không phải luật tự đặt cho đẹp số**. Áp cho **tất cả** nhánh từ tệp
thô, không gọi lại bộ trỏ.

**Số đã có gần nhất:** chữ nhật 14% gated — người 84,23 · MIN 68,72 · S1 67,24 · `gui_sel`
63,86 · Base 55,86. Hộp phần tử thật sẽ chặt hơn ở phần tử nhỏ và lỏng hơn ở phần tử to;
trần ước **82–86**.

**Cách trình:** headline vẫn Voronoi; cột hộp phần tử để định vị với literature (AITW, AC đều
dùng hộp). Đọc tỉ lệ so trần: MIN 68,72/84,23 = **81,6% năng lực câu người**. ⚠️ Đã đo: dưới
luật lỏng, MIN và S1 sát nhau ⇒ cột này **không dùng để đọc đóng góp**, chỉ để định vị.

**Về mong muốn "trần 95 → mô hình 85":** không có thước hợp lệ nào cho trần 95 mà vẫn giữ tiêu
chí *câu phải đủ để một mô hình độc lập trỏ trúng*. Cách duy nhất đo được tới nay là **hợp nhất
hai bộ trỏ** (0b): trần 87,7 dưới luật 14%. Ghép thêm luật hộp phần tử có thể tới ~90; con số
95 là ngoài tầm với của mọi đường đã tra. Và hợp nhất nâng **đều** mọi nhánh, nên tỉ lệ
mô-hình/trần gần như không đổi: cái đẹp lên là số tuyệt đối, không phải khoảng cách tới người.

---

## PHẦN 4 — Không tìm thấy tiền lệ

- **Hợp nhất hai bộ trỏ GUI khác nhau làm trọng tài** (B1-3): không thấy bài nào; chỉ có bỏ
  phiếu trong một mô hình (GUI-RC, MVP). Nếu dùng, phải tự định nghĩa và tự đo sàn.
- **Cân bằng tỉ lệ nhãn `none` cho grounding có từ chối** với số đo cụ thể: VenusBench-GD và
  OSWorld-G có lớp refusal nhưng không có ablation tỉ lệ; số "22% tối ưu" tìm thấy chỉ nằm
  trong một preprint miền ngân hàng, không dùng được.
- **Hiệu ứng vị trí trong danh sách ứng viên dài với mô hình thị giác-ngôn ngữ**: có preprint
  về MCQA bias của LVLM (arXiv 2509.16805), chưa bình duyệt; không có bài nào đo trên danh sách
  phần tử GUI. Phép đo 0c là số tự đo.
- **LLM giám khảo cho câu chỉ dẫn GUI có hiệu chuẩn với người**: WebJudge chấm quỹ đạo, không
  chấm câu. Không tìm thấy.
- **Verifier riêng cho GUI instruction generation**: không tìm thấy; chỉ có verifier cho QA
  (Hu 2019) và cho grounding (GUI-Actor).

---

## Nguồn đã mở (không phải ghi chú của người khác)

ACL Anthology P18-2124 · 2020.acl-main.503 · 2024.naacl-long.394 · 2025.findings-naacl.223 ·
2024.tacl-1.9 · arXiv 1810.04805 (BERT §4.3) · 2306.06070 (Mind2Web) · 2401.01614 (SeeAct) ·
2412.04454 (Aguvis, PMLR v267) · 2309.03882 (ICLR 2024) · 2310.11441 (SoM) · 2406.03679 (AC,
Phụ lục D.3) · 2307.10088 (AITW) · 2508.05615 (AAAI 2026) · 2512.08529 (CVPR 2026) ·
2506.03143 (GUI-Actor, Bảng 7) · 2505.13227 (Jedi) · 2507.05791 (GTA1, ICLR 2026) ·
2504.01382 (COLM 2025) · 2410.05243 (UGround) · 2007.07314 (ICLR 2021) · 2602.02419 ·
2510.18488 · 2512.16501 · openaccess CVPR 2023 GRES · ojs.aaai.org 4619 (Read+Verify).

---

## Phụ lục 9/9 — ĐO XONG PHÉP HỢP NHẤT BỘ TRỎ: NÂNG TRẦN THÌ ĐƯỢC, NHƯNG NỚI RỘNG KHOẢNG CÁCH

Tính từ `runs/gate_a/gate_A_raw.jsonl`, `runs/venus/venus_gate_raw.jsonl` và ba tệp
`venus/score_venus_*_2532_raw.jsonl`. **0 giây GPU.**

### 1. Con số 79,0 → 87,7 của mục trên tái lập được, và nó thuộc luật nào

| luật trên lát trần 300 bước | UGround | UI-Venus | hợp nhất | lợi |
|---|---|---|---|---|
| `err_frac` = ‖p−g‖/W ≤ ,14 | **79,00** | 74,00 | **87,67** | +8,67 |
| chữ nhật ±14% từng trục | 81,33 | 75,00 | 89,33 | +8,00 |
| AitW hai trục | 81,00 | 75,00 | 89,33 | +8,33 |

⇒ Cặp **79,0 → 87,7** ghi ở mục trên là luật `err_frac`, tức `disk_l2` của
`rule_sensitivity.py`, **không phải** luật tiêu đề. Kết luận không đổi theo luật: hợp nhất mua
được **+8,0 đến +8,7 pp** cho trần.

### 2. ⛔ Nhưng mô hình chỉ được một nửa chỗ đó ⇒ khoảng cách RỘNG RA

Cùng luật chữ nhật ±14%, lát 2.532 bước:

| nhánh | UGround | UI-Venus | hợp nhất | lợi |
|---|---|---|---|---|
| Base | 50,67 | 45,22 | 54,27 | **+3,59** |
| S1/101 | 61,41 | 54,94 | 65,05 | **+3,63** |
| S2/101 | 58,73 | 52,73 | 61,81 | **+3,08** |

**Trần được +8,00 · mô hình được +3,63 ⇒ khoảng cách trần − S1 RỘNG RA 4,37 pp.**
⇒ ⛔ Hợp nhất bộ trỏ **không** phải đường nâng số. Nó làm mô hình trông **kém đi** so với trần,
đúng chiều ngược với mục đích. Câu ghi ở `CLAUDE.md` (*"nâng đều mọi nhánh nên tỉ lệ gần như
không đổi"*) nay phải sửa: **không nâng đều**, trần được gấp **2,2 lần** mô hình.

### 3. ⭐ Vì sao — và đây là con số đáng mang đi bảo vệ

Trên đúng **174 bước** giao nhau giữa hai lát, cùng luật, cùng bước:

| | UGround | UI-Venus | hợp nhất | **CẢ HAI cùng trượt** |
|---|---|---|---|---|
| câu chuẩn | 82,18 | 75,86 | 90,80 | **9,20%** |
| S1/101 | 66,67 | 55,17 | 71,26 | **28,74%** |

Phần mà **không bộ trỏ nào cứu được** ở mô hình gấp **3,1 lần** ở câu chuẩn. Thêm một bộ trỏ thứ
hai chỉ vớt được những bước mà câu vốn đã đủ tốt để trỏ trúng; nó không vớt được bước mà câu
**gọi tên sai phần tử**. Đó chính là dạng lỗi lưỡng cực đã tái lập bốn lần (`106` (x13c) ·
`report/136` · `report/144` · `report/153` §7.4).

⇒ **Trần 75,73 không phải thứ đang chặn.** Chặn là 28,74% số bước mà câu chỉ sang phần tử khác,
và không phép đổi dụng cụ nào chạm tới được. Đường duy nhất còn lại là **sửa mô hình**, tức đúng
chẩn đoán tri giác của `151` mục 2 và đúng lượt VIS-SFT.

### 4. Giá nếu vẫn muốn làm

UI-Venus-7B chấm ~14,4 h một lượt; muốn có hàng hợp nhất cho **GRPO** phải chạy thêm một lượt nữa,
rồi mọi số của hai bài báo và luận văn phải đo lại. Đổi lại là một trần cao hơn mà mô hình **không**
theo kịp. ⇒ Không đáng.

---

## Phụ lục 9/9 (b) — ghép với GRPO THẤP HƠN ghép với MIN, và một câu của `151` cần sửa

Tính lại mục 0a trên đủ 4.463 bước, thêm hàng cho nhánh tiêu đề hiện tại:

| hệ thống | exec | so nhánh nền | b/c | p |
|---|---|---|---|---|
| `gui_sel` một mình | 56,13 | — | — | — |
| **ghép: sel; `none` → MIN** | **60,72** | +0,67 | 127/157 | 0,085 |
| ghép: sel; `none` → CE2 | 60,54 | +1,12 | 115/165 | **0,003** |
| ghép: sel; `none` → GRPO | 60,52 | +0,45 | 112/132 | 0,224 |
| ghép: sel; `none` → S1 | 59,44 | +0,34 | 116/131 | 0,373 |

Tỉ lệ bỏ cuộc tái lập đúng **41,97%** (1.873/4.463).

⭐ **Số mới:** ghép với **GRPO** cho **60,52**, tức **thấp hơn** ghép với MIN dù GRPO là nhánh
tiêu đề và hơn MIN 0,02 pp khi đứng một mình. Nghĩa là trên đúng 1.873 bước mà `gui_sel` bỏ
cuộc, MIN là nhánh dự phòng **tốt hơn** GRPO. Phù hợp với chẩn đoán ở `report/153` §7.4: GRPO
đổi hẳn phần tử ở một số bước, và trong nhóm bước khó thì việc đổi ấy hại nhiều hơn lợi.

⛔⛔ **Một câu của `151` mục 2.2 sai:** *"mọi bộ chọn không-oracle ≤ 60,45"*. Bộ chọn
`none → MIN` cho **60,72**, và `none → CE2` cho **60,54** — cả hai đều thi hành được, không
oracle. Câu ấy có lẽ nói về một họ bộ chọn khác (bộ định tuyến học được trên 8 nhánh); phải
khai đúng phạm vi, đừng để nó phủ định một phép đo đã có.

⛔ **Nhưng 60,72 KHÔNG được lên tiêu đề**, ba lý do độc lập:
1. Nó là **argmax của một họ luật thử sau khi thấy điểm** — các luật khác trong cùng bó cho
   60,12 đến 60,65 (mục 0a). Đây đúng hiệu ứng chọn mẫu mà `151` §2.2 và `report/153` §7.4 nêu.
2. **p = 0,085**, và +0,67 pp nằm sâu dưới MDE 2,11 ⇒ ô **TRẮNG**.
3. Nó là **hai mô hình chạy lúc suy luận**, không phải một điểm lưu mới, nên là đóng góp hệ
   thống chứ không phải đóng góp mô hình.
⇒ Cách dùng đúng: một hàng bảng gắn nhãn **luật hậu kiểm**, kèm cả ba điều trên.
