# TỔNG HỢP 6 PAPER REWARD 2025–2026 — BẢN MARKDOWN HAI CỘT

> Chép từ 12 ảnh chụp màn hình (tệp gốc trên máy Mac: `TONG_HOP_06_PAPER_REWARD_2025_2026_2_COT.md`,
> chụp 15/11/2026, 9:59–10:02). Ảnh đã xoá sau khi đối chiếu. Bảng hai cột của bản gốc được chép
> thành hai khối liên tiếp: **Vấn đề và phương pháp** rồi **Thực nghiệm và kết quả**.
> Chỗ ảnh bị cắt hoặc bản gốc hiển thị lỗi được ghi `[…]`.

**Mục tiêu:** nắm nhanh vấn đề, phương pháp, công thức, thực nghiệm, giới hạn và liên hệ với SASI/SA-SPICE-v3.
**Định dạng:** Markdown hai cột bằng bảng; không cần Canvas hoặc file phụ.
**Ngày tổng hợp:** 15/11/2026.

> Cách đọc mỗi paper: đọc dòng **"Nói nôm na"** trước, sau đó đọc cột trái để hiểu ý tưởng, rồi mới sang cột phải xem con số. Không cần học thuộc công thức ở lần đọc đầu.

## Từ chuyên môn cần biết trước

- **Reward:** điểm dùng để hướng dẫn model học.
- **Reward function:** công thức tính reward.
- **Reward model:** một model riêng được huấn luyện để chấm reward.
- **Outcome reward:** chấm toàn bộ câu/kết quả cuối.
- **Process reward:** chấm từng bước suy luận trung gian.
- **Token-level reward:** chấm từng token.
- **Adaptive:** tự thay đổi theo từng trường hợp, thay vì dùng một cấu hình cố định.
- **Ablation:** bỏ hoặc thay một thành phần để đo đóng góp của nó.
- **Best-of-N (BON):** sinh N lời giải rồi dùng reward chọn lời giải tốt nhất.
- **Baseline:** phương pháp đối chứng.
- **Downstream policy:** model cuối cùng được huấn luyện hoặc được reward hướng dẫn.

## Hiểu reward bằng một ví dụ đời thường

Hãy tưởng tượng model là một học sinh đang tập viết hướng dẫn sử dụng điện thoại. Reward là điểm mà giáo viên chấm cho mỗi câu. Nếu cách chấm điểm quá thô, học sinh không biết mình sai ở đâu.

Ví dụ giáo viên chỉ cho:

- đúng hoàn toàn: 1 điểm;
- còn lại: 0 điểm.

Một câu gần đúng và một câu hoàn toàn vô nghĩa đều nhận 0. Học sinh không biết câu nào gần đáp án hơn. Thiết kế reward là thiết kế cách giáo viên phản hồi: chấm nội dung, hành động, mục tiêu hay từng bước; chấm cố định hay thay đổi theo độ khó của bài.

Sáu paper dưới đây đều nghiên cứu "người giáo viên chấm điểm", nhưng mỗi bài sửa một vấn đề khác:

- GUI-G² sửa cách chấm vị trí trên màn hình;
- Reward Features sửa việc mỗi người có sở thích khác nhau;
- PQM sửa cách chấm các bước suy luận;
- Free Process Rewards tìm cách có điểm từng bước mà không cần người gán từng bước;
- Q-RM tách người viết và người chấm ở mức token;
- POLAR dạy bộ chấm bằng lượng dữ liệu cực lớn trước khi dùng thật.

Nếu không chuyên kỹ thuật, chỉ cần đọc các đoạn văn "Paper này kể câu chuyện gì?" và "Liên hệ với luận văn". Các bảng và công thức phía sau dùng để tra cứu khi chuẩn bị bảo vệ.

## 0. Nên đọc bài nào trước?

| Đọc kỹ | Đọc chọn lọc / làm nền |
|---|---|
| **1. GUI-G² — AAAI 2026**<br>Gần nhất: GUI + GRPO + adaptive reward. | **PQM — ICLR 2025**<br>Reward ranking ở mức reasoning step. |
| **2. Reward Features — NeurIPS 2025**<br>Gần SASI về feature combination và adaptive weighting. | **Free Process Rewards — ICML 2025**<br>Process reward không cần step labels. |
| **3. SPIDEr — ICCV 2017** *(ngoài bộ sáu bài mới)*<br>Trực tiếp dùng SPICE làm reward. | **Q-RM — ICML 2025**<br>Token-level reward; extension tương lai. |
| **4. SCST — CVPR 2017** *(ngoài bộ sáu bài mới)*<br>Nền sequence RL và reward comparison. | **POLAR — NeurIPS 2025**<br>Pretrain reward model quy mô lớn. |

---

## 1. GUI-G² — Gaussian Reward Modeling for GUI Grounding

**Venue:** AAAI 2026
**Paper:** https://arxiv.org/abs/2507.15846
**Code:** https://github.com/ZJU-REAL/GUI-G2

> **Nói nôm na:** reward cũ chỉ nói "trúng" hoặc "trượt". GUI-G² cho điểm giảm dần theo khoảng cách và tự điều chỉnh độ rộng vùng thưởng theo kích thước button/icon.

### Paper này kể câu chuyện gì?

Hãy tưởng tượng target là một nút lớn trên màn hình. Cách chấm cũ vẽ một đường biên quanh nút: model dự đoán vào trong đường biên thì được 1 điểm, ra ngoài dù chỉ một pixel cũng nhận 0. Một dự đoán sát mép nút và một dự đoán ở góc đối diện màn hình bị xem như nhau. Đây là tín hiệu học rất nghèo.

GUI-G² thay mặt phẳng điểm số bằng một "ngọn đồi" Gaussian. Đỉnh đồi nằm ở tâm nút. Càng dự đoán gần tâm, model càng được nhiều điểm; càng đi xa, điểm càng giảm dần. Nhờ đó model biết một dự đoán gần target tốt hơn một dự đoán rất xa, kể cả khi cả hai chưa trúng hoàn toàn.

Paper còn nhận ra icon nhỏ và button lớn không nên dùng cùng độ rộng ngọn đồi. Icon nhỏ đòi hỏi tọa độ chính xác, nên vùng điểm cao phải hẹp. Button lớn có nhiều vị trí bấm hợp lệ, nên vùng điểm cao rộng hơn. Đây là phần "adaptive": reward tự điều chỉnh theo kích thước của từng element.

Điểm quan trọng với luận văn không phải hàm Gaussian. Điều cần học là cấu trúc lập luận: tác giả tìm ra một thuộc tính của từng mẫu làm reward cũ mất thông tin, rồi dùng chính thuộc tính đó để điều chỉnh reward. SASI cũng muốn làm điều tương tự: câu chuẩn càng ít tuple, SPICE càng ít thông tin, nên reward phải dựa nhiều hơn vào chrF.

### Ví dụ tính tay trước khi đọc công thức

Giả sử button thật có tọa độ:

```
góc trái trên:  (x₁=100, y₁=200)
góc phải dưới: (x₂=300, y₂=280)
```

Button rộng 200 pixel và cao 80 pixel. Tâm của button là:

```
μ = ((100+300)/2, (200+280)/2) = (200, 240)
```

Với `α=0,5`, độ rộng Gaussian là:

```
σx = 0,5 × 200 = 100
σy = 0,5 × 80  = 40
```

Nếu model dự đoán tâm `(210,250)`, nó chỉ lệch:

```
Δx = 210 − 200 = 10 pixel
Δy = 250 − 240 = 10 pixel
```

So với button này, sai số 10 pixel là nhỏ, nên point reward xấp xỉ:

```
R_point ≈ exp{−0,5 × [(10/100)² + (10/40)²]}
        ≈ 0,964
```

Model vẫn nhận điểm rất cao vì prediction nằm gần tâm.

Nếu target là icon chỉ rộng 20 và cao 20 pixel, cùng `α=0,5` sẽ cho `σx=σy=10`. Vẫn lệch 10 pixel theo cả hai chiều thì:

```
R_point ≈ exp{−0,5 × [(10/10)² + (10/10)²]}
        ≈ 0,368
```

Cùng một sai số 10 pixel:

- đối với button lớn: còn tốt;
- đối với icon nhỏ: sai đáng kể.

Đó chính là ý nghĩa của adaptive variance. Reward không dùng cùng một mức tolerance cho mọi element.

### Vấn đề và phương pháp

**Vấn đề**
Reward GUI grounding thường là nhị phân: prediction nằm trong target box → 1, ngoài box → 0. Near-miss một pixel và lệch rất xa cùng nhận 0. Element là vùng hai chiều nhưng reward coi như một điểm.

**Ý tưởng**
Biến mỗi GUI element thành Gaussian 2D.
- Point reward chấm độ gần tâm.
- Coverage reward chấm mức khớp vùng.
- Adaptive variance thay đổi theo kích thước element.
- Giữ GRPO; reward framework là đóng góp chính.

**Giải thích công thức từng dòng**

1. **Tìm tâm target** — `μ=((x₁+x₂)/2,(y₁+y₂)/2)`
   `x₁,y₁` là góc trái trên; `x₂,y₂` là góc phải dưới. `μ` là tâm bounding box thật.
2. **Đo sai số** — `Δx` và `Δy` là khoảng lệch giữa tâm dự đoán với tâm thật theo hai chiều.
3. **Đổi sai số thành điểm** — `R_point = exp{−½[(Δx/σx)²+(Δy/σy)²]}`
   Nếu sai số bằng 0 thì reward bằng 1. Sai số tăng thì reward giảm mượt. `exp` là hàm mũ giúp điểm giảm nhanh nhưng không rơi đột ngột về 0.
4. **Tạo tolerance thích nghi** — `σx=α·width; σy=α·height`
   `σ` càng lớn thì reward "dễ tính" hơn với sai số. Paper dùng `α=0,5`, nên độ lệch chuẩn bằng nửa kích thước element.
5. **Ghép hai loại reward** — `R_total=νR_point+γR_coverage`
   `R_point` chấm tâm; `R_coverage` chấm cả vùng. `ν` và `γ` là trọng số. Paper đặt cả hai bằng 1, tức xem hai phần quan trọng ngang nhau.
6. **GRPO đọc reward thế nào?** — `Aᵢ=(Rᵢ−mean(R))/std(R)`
   Model sinh 8 prediction cho cùng instruction. Một prediction cao hơn trung bình nhóm có advantage dương và được tăng xác suất; thấp hơn trung bình có advantage âm. Chia cho `std` đưa nhóm điểm phân tán rộng/hẹp về thang tương đối gần nhau.

**Liên hệ SASI**
GUI-G²: `element size → adaptive variance`.
SASI: `tuple sparsity K_g → adaptive SPICE–chrF weight`.

Cả hai dùng thuộc tính từng sample để điều chỉnh reward. SASI phải học cách họ so adaptive với fixed và ablate từng component.

Không được copy Gaussian formula sang text reward vì output luận văn là câu, không phải tọa độ.

### Thực nghiệm và kết quả

**Cấu hình**
Qwen2.5-VL-7B; GRPO; 8 response/instruction; khoảng 100K instances; 8×A100-80GB; KL β=0,04; một epoch.

**Benchmark**
ScreenSpot 92,0%; ScreenSpot-v2 93,3%; ScreenSpot-Pro 47,5%.

**So UI-TARS-72B**
47,5% vs 38,1%: +9,4 điểm phần trăm; +24,7% tương đối.

**Ablation nghĩa là gì và chứng minh gì?**
Ablation là giữ model, dữ liệu và cách train gần như giống nhau, chỉ bỏ hoặc thay một thành phần. Nhờ vậy ta biết thành phần nào tạo cải thiện.

1. **Sparse point 87,4% → GUI-G² 93,3%**
   Sparse point chỉ cho tín hiệu khi prediction đạt điều kiện rời rạc. Gaussian dense reward cho điểm cả khi prediction chưa trúng. Gain +5,9 điểm cho thấy tín hiệu liên tục hữu ích hơn tín hiệu thưa trong setup này.
2. **Fixed variance 87,8% → adaptive 93,3%**
   Fixed dùng cùng tolerance cho mọi element. Adaptive thay tolerance theo kích thước. Gain +5,5 điểm là bằng chứng trực tiếp cho component adaptive, không chỉ cho Gaussian nói chung.
3. **Inside-only 88,4% → reward mọi nơi 93,3%**
   Inside-only vẫn cho 0 nếu prediction nằm ngoài box. Reward mọi nơi cho near-miss một mức điểm, giúp model biết hướng tiến gần target.
4. **Bỏ coverage còn 92,1%**
   Chỉ biết tâm chưa đủ; thông tin vùng đóng góp thêm khoảng 1,2 điểm.
5. **Bỏ point còn 90,2%**
   Chỉ biết vùng mà không nhấn mạnh tâm làm giảm khoảng 3,1 điểm. Point component có đóng góp lớn hơn coverage trong ablation này.
6. **Dùng cả hai đạt 93,3%**
   Hai component bổ sung nhau: một phần giữ độ chính xác tâm, phần kia giữ kích thước và độ chồng lấp vùng.
7. **So nhiều sigma**
   1σ quá hẹp; 3σ quá rộng; 2σ gần tốt nhất. Adaptive 93,3% vẫn nhỉnh hơn 2σ 92,92%, cho thấy điều chỉnh theo từng element tốt hơn một tolerance cố định dùng toàn bộ dữ liệu.

**Giới hạn**
- Không thấy nhiều independent seed/KTC.
- Reward geometry gần metric center-in-box.
- Leaderboard khác model/data; causal evidence nằm ở ablation.
- Không có human evaluation trực tiếp.
- Quy mô compute/dữ liệu lớn hơn luận văn nhiều.

**Phán quyết**
Paper gần luận văn nhất và bắt buộc đọc kỹ.

---

## 2. Capturing Individual Human Preferences with Reward Features

**Venue:** NeurIPS 2025
**Proceedings:** https://proceedings.neurips.cc/paper_files/paper/2025/hash/761bc7f095f927e5a5de31ed4154bb45-Abstract-Conference.html

> **Nói nôm na:** thay vì một bộ chấm chung cho tất cả mọi người, paper học các tiêu chí chung rồi thay trọng số của từng tiêu chí cho mỗi người.

### Paper này kể câu chuyện gì?

Giả sử ba người chấm một câu trả lời. Người thứ nhất coi độ chính xác là quan trọng nhất. Người thứ hai thích câu ngắn gọn. Người thứ ba quan tâm văn phong lịch sự. Nếu lấy trung bình tất cả thành một reward duy nhất, bộ chấm có thể không thật sự giống sở thích của bất kỳ người nào.

Paper đề xuất tách reward thành nhiều "tiêu chí con", gọi là reward features. Có thể hình dung mỗi câu trả lời có một bảng điểm gồm độ chính xác, độ ngắn gọn, văn phong và các đặc tính khác. Mỗi người có một bộ trọng số riêng: người này đặt trọng số cao cho độ chính xác, người kia đặt trọng số cao cho văn phong.

Model lớn chỉ cần học các tiêu chí chung một lần. Khi gặp người mới, hệ thống không huấn luyện lại toàn bộ model mà chỉ học một vector trọng số nhỏ từ vài lựa chọn của người đó. Đây là lý do paper gọi reward là adaptive theo user.

SASI có nét giống về hình thức: SPICE và chrF có thể xem như hai tiêu chí, còn số tuple quyết định trọng số giữa chúng. Nhưng sự giống nhau chỉ dừng ở cấu trúc. Paper này học tiêu chí và trọng số từ preference data; SASI dùng hai metric có sẵn và một công thức viết tay. Vì vậy không được gọi SASI là personalized reward model.

### Vấn đề và phương pháp

**Vấn đề**
Reward model trung bình hóa preference của mọi người. Khi rater bất đồng, một reward chung có thể không đại diện cho từng cá nhân.

**Ý tưởng**
Reward của user là tổ hợp tuyến tính các reward features chung. Học features trên nhiều người; với user mới chỉ fit vector trọng số nhỏ bằng logistic regression.

**Giải thích công thức**

```
r_h(x,y)=⟨φ_θ(x,y),w_h⟩
```

- `x` là prompt.
- `y` là câu trả lời.
- `h` là một người dùng cụ thể.
- `φ_θ(x,y)` là danh sách điểm theo các tiêu chí chung mà model tự học, ví dụ một chiều có thể phản ánh độ dài, chiều khác phản ánh văn phong.
- `w_h` là trọng số riêng của người `h`.
- Ký hiệu `⟨·,·⟩` nghĩa là nhân từng điểm tiêu chí với trọng số tương ứng rồi cộng lại.

```
P(y≻y′|x,h)=σ(⟨φ(x,y)−φ(x,y′),w_h⟩)
```

Model lấy chênh lệch feature giữa hai câu, nhân với sở thích của user rồi dùng hàm σ biến thành xác suất từ 0 đến 1 rằng user thích `y` hơn `y′`.
*(Bản gốc hiển thị lỗi công thức này, bị tách thành hai mảnh ở hai cột; đã ghép lại theo hai mảnh nhìn thấy.)*

**Liên hệ SASI**
Có thể viết analogy:

```
φ=(SPICE,chrF)
w(K_g)=(α_g,1−α_g)
```

Nhưng SASI **không phải RFM** vì features/weights không học từ preference và điều kiện là tuple sparsity, không phải user.

Bài học: adaptive phải so non-adaptive và báo uncertainty.

### Thực nghiệm và kết quả

**Cấu hình**
UltraFeedback: 60.829 train, 985 test.
Gemma 1.1 2B.
Feature dimension 8/32/128.
20–100 training raters; 500 held-out synthetic users.
Năm runs, 99% KTC.

**Lưu ý**
Controlled study chủ yếu dùng synthetic users; chưa có personalized RL end-to-end.

**PAC intuition**
Nếu chỉ hỏi một người rất nhiều lần, ta hiểu người đó tốt hơn nhưng vẫn không hiểu sự khác nhau giữa cộng đồng. Hỏi nhiều người độc lập giúp model học được variation giữa users.

**Ablation và giới hạn**
- Dimension 32/128 ổn hơn 8 khi users dị biệt.
- Lợi ích adaptive tăng khi disagreement cao.
- Distribution shift theo raters làm baseline giảm mạnh.
- Không có individual-human study.
- Synthetic criteria hẹp, deterministic, không preference noise/drift.
- Feature identifiability chưa chứng minh.
- Equation (6) published có dấu hiệu thiếu sigmoid.

**Phán quyết:** gần SASI thứ hai về cấu trúc adaptive weighting.

---

## 3. Process Reward Model with Q-value Rankings — PQM

**Venue:** ICLR 2025
**OpenReview:** https://openreview.net/forum?id=wQEdh2cgEk

> **Nói nôm na:** thay vì chỉ nói mỗi bước suy luận "đúng/sai", PQM cố học bước nào đưa lời giải đến gần đáp án đúng hơn và xếp hạng các bước đó.

### Paper này kể câu chuyện gì?

Hãy tưởng tượng giáo viên chấm một bài toán nhiều bước. Cách chấm đơn giản đánh dấu từng dòng là đúng hoặc sai. Nhưng hai dòng cùng được đánh dấu "đúng" chưa chắc có giá trị như nhau: một dòng có thể mới bắt đầu, dòng khác đã đưa lời giải rất gần đáp án cuối.

PQM muốn điểm số thể hiện mức tiến bộ. Khi chuỗi suy luận đúng tiếp tục, điểm nên tăng dần vì xác suất giải đúng cuối cùng tăng lên. Khi xuất hiện lỗi và chuỗi tiếp tục đi sai, điểm nên giảm. Thay vì chỉ học hai nhãn 0/1, model học thứ tự giữa các trạng thái suy luận.

Đây là lý do paper dùng từ Q-value ranking. "Q-value" ở đây được diễn giải như mức triển vọng hoàn thành đúng từ prefix hiện tại. Paper xây một loss buộc các bước tốt được xếp cao hơn các bước xấu và có khoảng cách giữa hai nhóm.

Liên hệ với luận văn chỉ ở ý tưởng xếp hạng: reward tốt phải xếp câu thực thi được cao hơn câu sai. PQM không dùng SPICE, không làm GUI và không chứng minh việc trộn SPICE–chrF là đúng. Nó chỉ giúp giải thích tại sao concordance/ranking là một diagnostic có ý […]

### Vấn đề và phương pháp

**Vấn đề**
PRM truyền thống dùng BCE phân loại từng step đúng/sai. Nó không ép ordering: bước đúng tiến dần lên và chuỗi sai giảm dần.

**Ý tưởng**
Học thứ hạng Q-value giữa reasoning states thay vì chỉ classification. Score biểu diễn logit xác suất hoàn thành đúng từ prefix hiện tại.

**Giải thích công thức và ordering**

```
Q^π(prefix,step)=logit(E[1(final correct)])
```

- `prefix` là toàn bộ phần lời giải trước bước hiện tại.
- `step` là bước mới vừa thêm.
- `1(final correct)` bằng 1 nếu cuối cùng giải đúng, bằng 0 nếu sai.
- `E[...]` là xác suất trung bình lời giải sẽ kết thúc đúng khi tiếp tục từ prefix đó.
- `logit` đổi xác suất 0–1 sang một thang số không bị chặn.

Với chuỗi đúng, paper muốn `Q₀ < Q_c1 < Q_c2 < …`: mỗi bước đúng đưa ta gần đáp án hơn.

Với chuỗi sai, paper muốn `… < Q_w2 < Q_w1 < Q₀`: càng tiếp tục sau lỗi, triển vọng càng thấp.

Margin `ζ` là khoảng cách tối thiểu mà loss cố tạo giữa vùng đúng và sai.

**Liên hệ SASI**
Hữu ích để lập luận reward phải giữ thông tin thứ hạng, không chỉ đúng/sai.

Không biện minh trực tiếp cho SASI: PQM học process verifier từ math labels; SASI là outcome reward thủ công mức câu.

### Thực nghiệm và kết quả

**Cấu hình**
Khoảng 440K Math-Shepherd trajectories.
DeepSeek-Math-7B-Base + scalar head; kiểm thêm nhiều backbones.
MATH500, GSM-Plus.
128 candidates/question; BON@8→128; beam search.
Response score = minimum step score.

**Kết quả có ý nghĩa gì?**
Ở MATH500, model sinh 128 lời giải rồi reward model chọn một lời giải tốt nhất — đây là BON@128.
- BCE PRM chọn đúng 39,8%.
- PQM chọn đúng 51,4%.
- Gain +11,6 điểm cho thấy học thứ hạng tiến bộ hữu ích hơn chỉ phân loại từng bước đúng/sai trong setup này.

Trên GSM-Plus, 61,72% tăng lên 66,00%. Khi dùng reward để hướng dẫn beam search cho Llama-3.1-8B, accuracy tăng từ BCE 26,4% lên PQM 31,6%.
Đây là kết quả reranking/search, chưa phải online RL training.

**Ablation và giới hạn**
- `ζ` khoảng 2–8 thường tốt; 0 quá yếu, 16 có thể quá mạnh.
- Loss lý thuyết kém implementation do noisy negative labels.
- Q là logit success probability, không hẳn standard expected-return Q.
- Minimum-step aggregation là heuristic.
- Chưa kiểm online RL; thiếu multi-seed/KTC rõ.

**Phán quyết:** đọc chọn lọc để xây nền reward ranking.

---

## 4. Free Process Rewards without Process Labels

**Venue:** ICML 2025
**PMLR:** https://proceedings.mlr.press/v267/yuan25c.html

> **Nói nôm na:** chỉ có nhãn đáp án cuối đúng/sai, paper vẫn cố suy ra điểm cho từng bước bằng cách xem policy đã học tăng xác suất token đó bao nhiêu so với model tham chiếu.

### Paper này kể câu chuyện gì?

Giả sử ta chỉ biết học sinh giải đúng hay sai ở cuối bài, nhưng không có người chấm từng dòng. Bình thường muốn tạo process reward, ta phải thuê người hoặc dùng một hệ thống đắt tiền để gán nhãn từng bước.

Paper nhận ra model sau khi học outcome đúng/sai sẽ thay đổi xác suất của các token. Nếu một token hoặc bước được model đã học ưu tiên nhiều hơn model tham chiếu, thay đổi đó có thể dùng như một tín hiệu process reward. Vì thế paper lấy log-ratio giữa policy đã học và reference policy ở từng prefix.

Tên "Free Process Rewards" không có nghĩa hoàn toàn miễn phí. Hệ thống vẫn cần nhãn đúng/sai cuối và vẫn phải train một model. Phần "free" chỉ nói rằng không phải thu thập thêm nhãn cho từng bước.

Đối với luận văn, đây là hướng tương lai nếu muốn chấm từng token trong câu hướng dẫn. Hiện tại không nên áp dụng ngay vì SPICE và chrF được thiết kế cho câu hoàn chỉnh. Chấm prefix như "Tap the..." có thể không mang ý nghĩa ổn định và còn làm phức tạp phương pháp chính.

### Vấn đề và phương pháp

**Vấn đề**
Nhãn từng reasoning step đắt; MCTS phải rollout nhiều continuation.

**Ý tưởng**
Huấn luyện outcome reward dưới dạng log-ratio policy/reference. Prefix log-ratio tạo implicit soft value; hiệu hai prefix tạo process reward. Không cần step labels.

**Giải thích công thức**

```
r_φ(y)=β log[π_φ(y)/π_ref(y)]
```

- `y` là toàn bộ lời giải.
- `π_φ(y)` là xác suất model đã học gán cho lời giải đó.
- `π_ref(y)` là xác suất model tham chiếu ban đầu.
- Tỷ số lớn hơn 1 nghĩa là sau training, model ưu tiên lời giải này hơn trước.
- `log` biến phép nhân xác suất của nhiều token thành phép cộng.
- `β` điều chỉnh thang điểm.

`q_φᵗ` cộng log-ratio từ token đầu đến token thứ `t`, tạo điểm cho prefix hiện tại.

`r_φᵗ=q_φᵗ−q_φᵗ⁻¹` lấy phần thay đổi khi thêm token/bước mới, xem đó là process reward của bước vừa thêm.

Đây là soft value có regularization, không phải kỳ vọng reward thông thường.

**Liên hệ SASI**
Hữu ích cho khái niệm densification không cần step labels.

Không đưa thẳng vào method: SPICE trên prefix không ổn định, chrF prefix lệch theo độ dài và log-ratio có thể double-count KL/reference trong GRPO.

### Thực nghiệm và kết quả

**Cấu hình**
Khoảng 33K UltraInteract instructions; 8 rollout/instruction; tối đa 264K responses.
Llama-3.1-8B reward/reference.
MATH500; BON@4/16/64.
Mistral-7B, Llama-8B/70B generators.
`β=0,05`.

**Kết quả có ý nghĩa gì?**
Trung bình qua 9 tổ hợp generator và số candidate:
- DPO implicit PRM đạt 50,4.
- Math-Shepherd matched reimplementation đạt 47,8.

Với Llama-8B sinh 64 lời giải, Math-Shepherd chọn đúng 52,8%, implicit PRM đạt 57,0%. Với Llama-70B: 68,8% → 72,2%.

Paper báo development FLOPs thấp hơn khoảng 38,7 lần vì không cần MCTS để gán nhãn từng step. Đây là tiết kiệm compute của pipeline tạo/huấn luyện reward, không có nghĩa inference miễn phí hoặc dữ liệu ít hơn đúng 38,7 lần theo mọi cách đếm.

**Ablation và giới hạn**
- Weighted majority voting giúp.
- Thêm responses thường giúp hơn thêm instructions.
- Khả năng làm reward model tốt không đồng nghĩa policy tốt.
- "Free" vẫn cần outcome labels và training.
- Minimum-step là heuristic.
- Chỉ reranking MATH500; chưa online RL; thiếu multi-seed rõ.

**Phán quyết:** nền process reward, không phải component nên thêm ngay.

---

## 5. Q-RM — Token-Level Q-function Reward Model

**Venue:** ICML 2025
**PMLR:** https://proceedings.mlr.press/v267/chen25ca.html

> **Nói nôm na:** paper huấn luyện một "giám khảo token" riêng, thay vì dùng chính xác suất sinh token của model để giả làm reward.

### Paper này kể câu chuyện gì?

Trong một số phương pháp, chính model viết câu cũng được dùng để suy ra token nào tốt qua xác suất sinh. Điều này giống như bắt thí sinh vừa làm bài vừa tự chấm bài: token quen thuộc có xác suất cao, nhưng quen thuộc không đồng nghĩa đúng hoặc hữu ích.

Q-RM tách hai vai trò. Policy chịu trách nhiệm sinh câu; một discriminative reward model riêng chấm từng token dựa trên prefix và token đó. Reward model được học từ các cặp câu được ưu tiên và bị từ chối, nhưng cố phân bổ tín hiệu xuống từng token.

Kết quả đáng chú ý là Q-RM có accuracy phân loại cặp thấp hơn một outcome reward model, nhưng khi dùng để huấn luyện policy thì policy lại tốt hơn. Điều này cho thấy một bộ chấm không nên chỉ được đánh giá bằng khả năng phân loại trên tập reward; cần xem nó tạo ra model downstream tốt đến đâu.

Đây là bài học quan trọng cho SASI: offline concordance là hữu ích nhưng chưa đủ. Reward phải được đưa vào training rồi kiểm `exec`/human/holdout. Tuy nhiên model reward 70B của Q-RM quá lớn so với phạm vi luận văn, nên chỉ đọc để hiểu tư tưởng, không nên thêm vào implementation hiện tại.

### Vấn đề và phương pháp

**Vấn đề**
DPO-derived token reward trộn generation probability và reward quality. Token xác suất cao chưa chắc tốt; reference policy tăng chi phí.

**Ý tưởng**
Học discriminative policy `φ(s,a)` riêng. Logit `Z(s,a)` làm token reward/advantage proxy. Train từ preference pairs, không cần process labels.

**Giải thích công thức**

```
φ(s,a)=exp Z(s,a)/Σa′ exp Z(s,a′)
```

- `s` là prefix đã có.
- `a` là token đang được xem xét.
- `Z(s,a)` là điểm thô mà reward model gán cho token `a` trong context `s`.
- Mẫu số cộng điểm mũ của mọi token có thể chọn, biến logits thành phân phối xác suất `φ`.

Paper lập luận `β log φ*(s,a)` gần với `Q*(s,a)−V*(s)`, tức mức token này tốt hơn mức kỳ vọng của state bao nhiêu. Audit cho rằng nên gọi đây là advantage proxy, không phải true Q đã được chứng minh chắc.

Để train từ một cặp câu thắng/thua, paper so trung bình logit của các token trong câu thắng với câu thua rồi trừ offset `γ`. Paper dùng `β=0,2`, `γ=2`.

**Liên hệ SASI**
Chỉ là extension tương lai nếu cần token credit/hard negatives action-target.

Không nên làm ngay: RM 70B quá lớn; token RM có thể chỉ distill bias SPICE/chrF; không gọi logit là true Q nếu chưa chứng minh.

### Thực nghiệm và kết quả

**Cấu hình**
Reward model Llama-3-70B, LoRA rank 128.
Policy Llama-3.2-3B.
GSM8K 45.364 pairs; MATH 94.941; QA 17.835; UltraFeedback 52.712.
Reward training 8×A100-80GB; RL 8×A100-40GB.

**Kết quả có ý nghĩa gì?**
`Pass@1` là tỷ lệ câu trả lời đầu tiên đúng. Trung bình GSM8K và MATH:
- SFT 45,33.
- PPO dùng outcome reward 46,74.
- GRPO 49,32.
- RLOO 50,25.
- PPO+Q-RM 52,59.
- REINFORCE+Q-RM 53,28.

Q-RM giúp PPO tăng 5,85 điểm và REINFORCE tăng 4,70 điểm so outcome reward. Ý nghĩa quan trọng: thay reward signal có thể tạo gain lớn hơn đổi optimizer. Nhưng reward model chính là Llama-70B, vượt xa tài nguyên luận văn.

**Ablation và giới hạn**
- Q-RM pairwise accuracy thấp hơn ORM nhưng downstream RL tốt hơn.
- RewardBench lại kém ORM ở nhiều category.
- Theory Q-function có bước suy luận/entropy assumption yếu.
- Global γ không có bias bound.
- Không rõ multi-seed main math table.

**Phán quyết:** đọc lướt để biết hướng token reward.

---

## 6. POLAR — Pre-Trained Policy Discriminators are General Reward Models

**Venue:** NeurIPS 2025
**Proceedings:** https://proceedings.neurips.cc/paper_files/paper/2025/hash/f888b1a383cc85410e0ba9819e7ac36e-Abstract-Conference.html

> **Nói nôm na:** trước khi học sở thích con người, POLAR cho reward model quan sát output của rất nhiều policy khác nhau để học phân biệt chúng; sau đó mới fine-tune thành bộ chấm chất lượng.

### Paper này kể câu chuyện gì?

Reward model thường được huấn luyện trực tiếp từ dữ liệu con người chọn câu A hay B. POLAR cho rằng trước bước đó, bộ chấm nên được "học nền" từ lượng output cực lớn của nhiều model khác nhau.

Trong pretraining, POLAR chưa biết câu nào tốt hơn theo con người. Nó chỉ học nhận ra hai output có đến từ cùng một policy hay không. Tác giả kỳ vọng quá trình này giúp model học các đặc trưng tổng quát về khác biệt giữa các policy. Sau đó reward model mới được fine-tune bằng human ranking để biến khả năng phân biệt thành khả năng chấm chất lượng.

Khi sử dụng, POLAR còn nhận một câu reference chất lượng cao để so với candidate. Cách này có thể giúp model biết mục tiêu mong muốn, nhưng cũng tạo nguy cơ ưu tiên câu giống reference. Một câu đúng nhưng diễn đạt khác có thể bị điểm thấp.

Paper này cho thấy reward model có thể là một chương trình nghiên cứu lớn, nhưng không phải mô hình để luận văn bắt chước. POLAR dùng hàng nghìn tỷ token và hàng trăm nghìn giờ GPU. Bài học phù hợp chỉ là: phải kiểm reward bằng chất lượng policy sau training và phải kiểm reference anchoring/paraphrase.

### Vấn đề và phương pháp

**Vấn đề**
Reward model cần nhiều human preference labels và thường generalize yếu.

**Ý tưởng**
Pretrain RM như policy discriminator: outputs cùng policy là positive, khác policy là negative. Fine-tune sau bằng human ranking. Runtime scorer nhận prompt + high-quality reference + candidate.

**Giải thích công thức động lực**

```
π*(τ|x) = π_init(τ|x) […]
```

*(Bản gốc hiển thị lỗi công thức này: chỉ thấy mảnh `π*(τ` ở cột trái và `x) = π_init(τ` ở cột phải, phần giải thích không hiện.)*

**Liên hệ SASI**
Bài học: downstream policy quan trọng hơn reward accuracy; phải kiểm reference anchoring và paraphrase.

Không sao chép: pretraining khổng lồ, single-reference tuyệt đối hoặc average benchmark không uncertainty.

### Thực nghiệm và kết quả

**Quy mô**
InternLM2.5 1.8B/7B.
Tổng 3,60T generated tokens.
POLAR-7B: khoảng 159.600 H800-GPU-hours.
150K human-ranked examples.
PPO/RFT trên 1,25M prompts, mỗi prompt có reference từ model mạnh.

**Ablation và giới hạn**
- 7B preference average: full 76,3; no-pretrain 76,5.
- Nhưng downstream full tốt hơn no-pretrain.
- Có thể học generator fingerprint/style.
- Reference là confound mạnh và phạt paraphrase.
- Không rõ seed/std/KTC.
- Compute không khả thi cho luận văn.

**Phán quyết:** chỉ đọc concept và reference ablation.

---

## 7. So sánh chéo

### Mỗi paper trong một câu

- **GUI-G²:** reward thích nghi theo geometry của từng GUI element.
- **Reward Features:** reward thích nghi theo preference của từng user.
- **PQM:** process reward học thứ hạng tiến bộ của reasoning steps.
- **Free Process Rewards:** lấy process reward từ outcome labels mà không cần nhãn từng bước.
- **Q-RM:** học token reward bằng một discriminative scorer riêng.
- **POLAR:** pretrain reward model trên output của nhiều policy trước khi học human preference.

| Paper | Reward source | Mức reward | Cách dùng | Bài học gần nhất cho SASI |
|---|---|---|---|---|
| GUI-G² | Công thức geometry | Output box | GRPO training | Adaptive phải thắng fixed |
| Reward Features | Learned features + adaptive weights | Response | Preference/reranking | Feature+weight structure |
| PQM | Learned Q-ranking | Reasoning step | BON/beam | Giữ ordering |
| Free PRM | Policy/reference log-ratio | Token/step | BON | Densify không step labels |
| Q-RM | Discriminative logits | Token | PPO/REINFORCE | Reward accuracy ≠ RL quality |
| POLAR | Policy-discriminator pretraining | Sequence | PPO/RFT | Reference anchoring |

## 8. Checklist SASI rút ra từ sáu bài

| Phải làm | Lý do |
|---|---|
| SPICE-only vs chrF-only vs fixed vs adaptive | Chứng minh component thật |
| Phân tầng `K_g=0,1,2,≥3` | Xác nhận đúng cơ chế sparse-aware |
| Ablate action và length penalty | Tách đóng góp |
| Train policy thật | Offline concordance chưa đủ |
| DEV + CONFIRM + nhiều seed | Giảm selection/training randomness |
| `exec`, action, target, non-tap, repetition | Đánh giá độc lập reward |
| Paraphrase/human check | Chống reference anchoring |
| Báo chrF dù bất lợi | Baseline đang mạnh hơn SA-SPICE screen |

## 9. Câu trình bày với thầy

> Dạ em đã đọc sáu hướng reward gần đây. Paper gần nhất là GUI-G² tại AAAI 2026: họ giữ GRPO và đóng góp adaptive Gaussian reward cho GUI, sau đó chứng minh adaptive hơn fixed bằng ablation và downstream policy. Reward Features tại NeurIPS 2025 cho thấy reward có thể phân rã thành feature chung và trọng số thích nghi. PQM, Free Process Rewards và Q-RM tập trung vào process/token reward; POLAR pretrain general reward model ở quy mô rất lớn. Bài học cho SASI là component reward có thể là đóng góp chính, nhưng phải chứng minh adaptive routing hơn fixed/chrF sau training, trên holdout và bằng evaluator độc lập.

## 10. Kết luận

- **Gần nhất:** GUI-G².
- **Gần thứ hai về adaptive weighting:** Reward Features.
- **Nền ranking:** PQM.
- **Nền process reward không step labels:** Free Process Rewards.
- **Extension token-level:** Q-RM.
- **Tiền lệ reward-model quy mô lớn:** POLAR.

> SASI có vị trí hợp lý trong reward-centric research, nhưng hiện vẫn là candidate. Offline screen mới cho thấy adaptive tốt hơn các SPICE sub-arm; chrF-only vẫn cao hơn và chưa có kết quả policy sau training.

### Nếu chỉ nhớ ba điều

[…] *(ảnh cuối cắt ở tiêu đề này, nội dung phía dưới không có trong ảnh chụp)*
