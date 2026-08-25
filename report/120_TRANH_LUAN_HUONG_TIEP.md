# 120 — TRANH LUẬN: đi hướng nào sau MIN-DESC/101 (25/8/2026)

> **Câu hỏi:** MIN-DESC/101 đạt 60,05%, hơn SFT trơn chỉ +0,94 pp (p=0,11, không ý nghĩa).
> Chẩn đoán cho thấy cơ chế **đúng nhưng bị chặn**. Sửa chỗ nào trước?
>
> Chiến lược đã chốt với chủ luận văn: **dò nhiều biến thể trên MỘT hạt giống**, chọn biến thể
> tốt nhất, rồi mới chi GPU cho hạt giống thứ hai. Mọi số trong pha dò là *thăm dò*.

---

## 0. Phán quyết trong bốn dòng

1. ⛔ **Hướng Ⓐ (đổi câu ở vế bị loại) — BÁC.** Văn liệu bình duyệt nghiêng hẳn về phía chống, và
   thiết kế hiện tại hoá ra có tiền lệ trực tiếp hơn Ⓐ.
2. ⛔ **Hướng Ⓑ như đã phát biểu lượt trước — VÔ NGHĨA.** `desc_neg` **đã** là hard negative cùng
   vai trò, gần nhất. 100,0% cặp âm cùng vai trò.
3. ✅ **Ⓑ′ — LỌC cặp âm cho phân biệt được thật.** Đây là hướng duy nhất được **cả** phép đo nội
   bộ **lẫn** văn liệu hậu thuẫn, và là hướng rẻ nhất: chỉ đổi bộ lọc dữ liệu, không đổi loss,
   không đổi cấu hình.
4. Ⓒ (MIX) giữ nguyên vị trí cũ: làm để **đạt điều kiện no-harm**, không phải để tăng điểm.

---

## 1. Phát hiện nội bộ làm đổi cả cuộc tranh luận

### 1.1 `desc_neg` đã là hard negative — Ⓑ cũ là không-làm-gì

`descriptor_label_build.nearest_other()` chọn *"phần tử **cùng vai trò** gần nhất, không chồng
lấn"*. Đo trên `descriptors.jsonl` tập dạy (37.663 bước có cả hai vế):

| | |
|---|---|
| `desc_neg` **cùng vai trò** với `desc` | **37.663/37.663 = 100,0%** |
| `desc_neg` **trùng tên** với `desc` | 6.259/37.663 = 16,6% *(đã bị `hop_le()` lọc bỏ)* |

### 1.2 ⭐ Vế âm QUÁ GẦN — 77,1% cặp không mang tín hiệu toạ độ

Đo trên đúng **22.854 cặp MIN-DESC đã dựng** (`branches/min_desc.json`):

| | |
|---|---|
| vế âm có toạ độ **nằm TRONG** ô dung sai ±140 | **17.624/22.854 = 77,1%** |
| \|dx\| trung vị · p75 | 42 · 126 |
| \|dy\| trung vị · p75 | 53 · 71 |

±140 trên thang norm-1000 là **đúng ngưỡng** mà `metric_exec.hit_disk` và `gate_desc_acc.py`
dùng để phán "point đúng". ⇒ **Ở 77% số cặp huấn luyện, vế bị-loại có toạ độ mà chính cây thước
của dự án cũng chấm là TRÚNG.** Số hạng ưu tiên ở những cặp đó gần như không mang tín hiệu về
toạ độ; chỉ còn phân biệt được qua ô tên.

Nguyên nhân cơ học: `hop_le()` lọc `neighbor_dist_px` trong khoảng **80–350 px**. Trên màn
1080×2400, 350 px theo chiều **dọc** chỉ bằng **146** đơn vị norm-1000 — sát ngay ngưỡng 140.
Bộ lọc khoảng cách được đặt bằng **pixel**, còn thước phán bằng **norm-1000 hai trục riêng**.
Hai hệ quy chiếu khác nhau, và không ai đối chiếu chúng cho tới hôm nay.

### 1.3 Toạ độ là biến MẠNH HƠN tên — nên chỗ mất tín hiệu là chỗ đắt nhất

Phân rã ô khai báo của MIN-DESC trên 3.473 bước kiểm có tên vàng:

| ô khai báo | n | % | exec nhóm |
|---|---|---|---|
| tên ✓ point ✓ | 2.106 | 60,6% | **87,1%** |
| tên ✓ point ✗ | 220 | 6,3% | 26,4% |
| tên ✗ point ✓ | 387 | 11,1% | 55,0% |
| tên ✗ point ✗ | 745 | 21,5% | 3,6% |
| không sinh `<desc>` | 15 | 0,4% | 0,0% |

Sai tên mà đúng chỗ còn gỡ được **55,0%**; đúng tên mà sai chỗ rơi xuống **26,4%**. Hai phép đo
độc lập (1.2 và 1.3) chỉ cùng một chỗ: **tín hiệu toạ độ trong cặp huấn luyện gần bằng không,
trong khi toạ độ là biến quyết định mạnh hơn.**

### 1.4 Chất lượng cặp quan trọng hơn số lượng cặp

`gradient_accumulation_steps: 16 × max_steps: 800` = **12.800 mẫu** trên 22.854 cặp ⇒ mô hình chỉ
đi qua **56% một epoch**. Lọc còn ~5.200 cặp thì 800 bước thành ~2,4 epoch — vẫn đủ, mà mỗi cặp
mang tín hiệu thật. ⇒ Lọc **không** phải đánh đổi dữ liệu lấy chất lượng; ở chế độ này nó gần như
thuần lợi.

---

## 2. Hướng Ⓐ — BÁC, có lý do đo được và lý do tiền lệ

**Ⓐ là gì:** đổi `rejected` từ *"khai báo sai + câu y hệt"* sang *"khai báo sai + câu mô tả chính
phần tử sai đó"*.

### 2.1 Thiết kế HIỆN TẠI có tiền lệ trực tiếp hơn Ⓐ

**FRODO** — Paul, West, Bosselut, Faltings, *Making Reasoning Matter: Measuring and Improving
Faithfulness of Chain-of-Thought Reasoning*, **Findings of EMNLP 2024**, tr. 15012–15032
(`aclanthology.org/2024.findings-emnlp.882/`) — dựng cặp `(x, r_w, y_w)` vs `(x, r_l, y_w)`:
lý luận phản-thực, **giữ nguyên đáp án đúng ở cả hai vế**. Đúng logic `chosen/rejected` của
MIN-DESC, và họ gọi nó là một mục tiêu **faithfulness** — ép đáp án phụ thuộc nhân quả vào lý
luận. ⇒ Cặp hiện tại của ta **không phải cặp lười**; nó là một mục tiêu đã có tên và đã bình duyệt.

Cùng hướng minimal-pair: **mDPO** (Wang et al., **EMNLP 2024 main**, tr. 8078–8088) đổi **ảnh**
chứ không đổi văn bản để tạo vế âm · **RLHF-V** (Yu et al., **CVPR 2024**) lấy phản hồi ở **mức
đoạn**, vế âm chỉ khác đúng đoạn bị ảo giác.

### 2.2 Văn liệu ĐO ĐƯỢC rằng cặp khác nhau tối thiểu học tốt hơn

· **CLAIR/APO** — D'Oosterlinck et al., **TACL Vol. 13 (2025)**, tr. 442–460: *"preference data
  gives a better learning signal when the underlying responses are contrastive"*; cặp chỉnh sửa
  tối thiểu cho tín hiệu mạnh nhất (+7,65% trên Llama-3-8B-Instruct, 32K cặp).
· **DCRM** — Huang & Goyal, **Findings of EMNLP 2025**: cặp tốt phải **tối thiểu hoá khác biệt
  nhiễu** và tối đa hoá khác biệt mong muốn. Ⓐ tăng cả hai — đúng con dao cắt vào Ⓐ.
· Nhóm **step-level DPO** (Step-level Value PO, Findings EMNLP 2024 · Full-Step-DPO, Findings ACL
  2025 · CPO, NeurIPS 2024) chọn **cắt loss về đúng chỗ khác nhau** thay vì loại cả câu trả lời,
  với lý do nêu thẳng: *"Rejecting an entire undesirable answer … may also discard preceding
  correct reasoning steps, introducing significant noise."*

### 2.3 Thiên vị độ dài là rủi ro thuật toán, không phải rủi ro nhãn

Hai vế của MIN-DESC hiện tại **gần bằng nhau về độ dài**; hai vế của Ⓐ thì không.
· Park, Rafailov, Ermon, Finn — **Findings of ACL 2024**, tr. 4998–5017: DPO khai thác độ dài rất
  mạnh · **SamPO** — Lu et al., **EMNLP 2024 main**: verbosity **sinh ra từ chính thuật toán**,
  do chênh KL cấp chuỗi giữa hai vế · Singhal et al., **COLM 2024**: phần lớn mức tăng reward của
  RLHF tái lập được bằng một reward **chỉ đếm độ dài**.

### 2.4 Tiền lệ của Ⓐ tồn tại, nhưng không đủ để bù

**Yu, Tan, Bansal, Berg**, *A Joint Speaker-Listener-Reinforcer Model for Referring Expressions*,
**CVPR 2017** — speaker có hinge loss với negative là **biểu thức của đối tượng gây nhiễu**, đúng
ý Ⓐ. ⚠️ Hai điểm phân định: câu negative của họ là **biểu thức thật do người viết**, không phải
câu mô hình tự sinh; và loss của họ là **hinge/ranking trên điểm ghép cặp**, không phải likelihood
kiểu DPO/ORPO — chuyển hệ chính là chỗ mọi bẫy ở 2.3 mới xuất hiện.
⛔ **Câu chữ:** Yu et al. đã chiếm ý này từ 2017 ⇒ nếu chạy Ⓐ thì **cấm viết "đầu tiên"/"mới"**.

### 2.5 Phép kiểm rẻ để bác Ⓐ bằng số, không bằng lời

Chuyển vị phép chẩn đoán của **mDPO** (họ gỡ ảnh khỏi dữ liệu preference rồi train lại; điểm
gần như không đổi ⇒ chứng minh mục tiêu giải được mà không cần nhìn ảnh):

> Một mô hình **chỉ-văn-bản, không thấy ảnh**, có phân biệt được `chosen` và `rejected` không?

· Cặp MIN-DESC hiện tại: **tự động qua** — hai vế chỉ khác ô `<desc>`, mà ô đó phải suy từ ảnh.
· Cặp Ⓐ: hai câu tiếng Anh khác nhau ⇒ gần như chắc chắn phân biệt được **mà không cần ảnh** ⇒
  gradient có thể đi vào văn phong/độ dài thay vì vào việc chọn phần tử.

⇒ Chạy phép này trước là cách **bác Ⓐ bằng đo đạc**, đúng luật "cổng rẻ chạy trước".

---

## 3. ⚠️ Đòn ngược chiều — và nó chính là chỗ mở ra Ⓑ′

**Razin, Malladi, Bhaskar, Chen, Arora, Hanin**, *Unintentional Unalignment: Likelihood
Displacement in Direct Preference Optimization*, **ICLR 2025** (arXiv 2410.08847).

Nguyên văn abstract: *"likelihood displacement is driven by preferences that induce similar
embeddings, as measured by a centered hidden embedding similarity (CHES) score"* và *"our results
highlight the importance of curating data with **sufficiently distinct** preferences"*.

Cơ chế: khi hai vế quá giống nhau, xác suất của **chính vế chosen** có thể **tụt xuống**, và khối
xác suất trôi sang một chuỗi thứ ba không ai muốn. Ví dụ của họ: dạy chuộng `No` hơn `Never` làm
xác suất `Yes` tăng vọt.

⭐ **Đây là bài phản biện nghiêm túc nhất một giám khảo có thể ném vào MIN-DESC — và phép đo nội
bộ ở Mục 1.2 nói rằng ta ĐANG ở đúng vùng nguy hiểm đó:** 77,1% cặp có vế âm nằm trong dung sai
của chính thước, tức khác biệt ngữ nghĩa thật gần bằng không.

**Hai nguồn độc lập, một kết luận:** văn liệu bảo *"cặp phải khác nhau ĐỦ"*, phép đo bảo
*"77% cặp của ta khác nhau KHÔNG ĐỦ"*. Đó là Ⓑ′.

⚠️ Giảm nhẹ có sẵn nhưng chưa ai đo: ORPO **có** số hạng NLL trên vế chosen (khác DPO thuần),
về lý thuyết chống được likelihood displacement. **Chưa ai đo hiện tượng này dưới ORPO** ⇒ nếu
viết vào bài thì phải khai là suy luận từ dạng loss, không phải kết quả đo.

---

## 4. Hướng Ⓑ (siết hard negative) — BÁC, ba lý do đo được

### 4.1 Đã làm rồi (Mục 1.1)

`nearest_other()` + dải `neighbor_dist_px` 80–350 px + lọc trùng tên **chính là** hard negative có
kiểm soát độ khó. Trùng khớp với hai tiền lệ trong miền GUI:
· **UIBert** — Bai et al., **IJCAI 2021**, tr. 1705–1712, Task 3: *"we use the k closest IMGs to
  the masked component i in the image as the negative components"*. ⚠️ Bài **không có ablation**
  k-closest so với random ⇒ đây là *tiền lệ thiết kế*, không phải *bằng chứng hiệu quả*.
· **Lexi** — Banerjee et al., **Findings of EMNLP 2022**, tr. 6992–7007: negative lấy ở **dải**
  cosine `[0,5 – 0,9]`, loại mọi thứ trên 0,9, lý do nêu thẳng: *"functional captions tend to be
  semantically very similar"*. Dải 80–350 px của ta là cùng ý tưởng, khác trục đo.

### 4.2 Sai trục — chỉ chạm dưới 10% khối lỗi

Đo trên chính preds: trong số bước **sai tên**, phần rơi đúng vào hàng xóm cùng vai trò gần nhất
là **7,4% (S2) · 10,4% (CE2-S2) · 9,8% (MIN-DESC)**. Hơn 80% lỗi tên rơi vào phần tử **khác hẳn**.
Siết cần gạt này không chạm được 90% khối lỗi.

### 4.3 Hard negative "quá khó" có phản tác dụng — bằng chứng chắc nhất trong cả cuộc tra

· **FaceNet** — Schroff et al., **CVPR 2015**, nguyên văn: *"Selecting the hardest negatives can
  in practice lead to bad local minima early on in training, specifically it can result in a
  collapsed model"* ⇒ cách vá là **semi-hard**.
· **Robinson et al.**, **ICLR 2021**, §6.1 *"Are harder samples necessarily better?"*: tăng độ khó
  **không** đơn điệu tốt lên; *"the hardest points are those closest to the anchor, and are
  expected to have a high propensity to have the same label"* — càng khó, tỉ lệ **false negative**
  càng cao. Nền tảng: **Debiased Contrastive Learning**, Chuang et al., **NeurIPS 2020**.
· **β-DPO** — Wu et al., **NeurIPS 2024**, Hình 1b: với **low-gap pairs** (chosen/rejected rất
  giống nhau — đúng định nghĩa cặp của ta), **tăng β làm win rate GIẢM**. ⭐ `pref_beta: 0.1` đang
  ở phía thấp ⇒ **đây là điểm cộng của cấu hình hiện tại, không phải chỗ cần sửa.**
· Mức tăng hard-so-với-easy ở tiền lệ gần nhất khiêm tốn: **Mao et al., CVPR 2016**, Bảng 1,
  UNC-Ref val, chỉ đổi tập negative: easy GT 0,677 → **hard GT 0,699** = **+2,2 pp**. Và họ chốt
  rằng negative tốt nhất là cái **rút từ đúng phân bố ứng viên lúc kiểm**, không phải cái khó nhất.

---

## 5. ✅ Ⓑ′ — VỆ SINH CẶP. Hướng được chọn.

Không đổi loss, không đổi cấu hình, không đổi cách chọn negative. **Chỉ đổi bộ lọc dữ liệu.**
Ba khuyết tật đã đo được trên đúng 22.854 cặp đang dùng, cả ba đều sửa bằng 0 giờ GPU.

| # | khuyết tật | tỉ lệ | hại gì |
|---|---|---|---|
| **①** | tách được **chỉ bằng chuỗi `(no name)`** — một vế `(no name)`, vế kia có tên | **17,4%** (9,6 + 7,8) | **LỐI TẮT**: phân biệt được mà **không cần nhìn màn hình** |
| **②** | vế âm có toạ độ **nằm trong** ô dung sai ±140 của chính thước | **77,1%** | không mang tín hiệu toạ độ — mà toạ độ là biến mạnh hơn (Mục 1.3) |
| **③** | ô **dấu hiệu phân biệt trùng hệt** hai vế | **13,1%** | ô thứ tư không đóng góp gì vào việc phân biệt |

**① là nghiêm trọng nhất** vì nó đúng chế độ hỏng mà **mDPO** (Wang et al., **EMNLP 2024 main**,
tr. 8078–8088) chứng minh được: họ **gỡ toàn bộ ảnh** khỏi dữ liệu preference rồi train lại, điểm
benchmark gần như không đổi ⇒ mục tiêu giải được mà không cần nhìn ảnh. Và đây là **lần thứ hai**
dự án mắc đúng mẫu hình này — `report/106` mục sửa đổi (l) ngày 9/8 đã bắt một hằng số ở ô thứ tư
làm lề đẹp mà không dạy được gì.

**② có chống lưng học thuật hai chiều:**
· **Razin et al., ICLR 2025** (Mục 3): cặp quá giống nhau gây **likelihood displacement**, khuyên
  *"curating data with sufficiently distinct preferences"*.
· ⚠️ Nhưng **CLAIR/APO (TACL 2025)** và **DCRM (Findings EMNLP 2025)** lại bảo cặp **càng tối
  thiểu càng tốt**. Hai bên **không mâu thuẫn**: CLAIR nói về khác biệt **bề mặt** (chỉnh sửa ít
  chữ), Razin nói về khác biệt **ngữ nghĩa/embedding** (phải đủ tách). Ⓑ′ giữ khác biệt bề mặt tối
  thiểu (vẫn chỉ đổi ô `<desc>`, câu y hệt) **và** ép khác biệt ngữ nghĩa đủ lớn (toạ độ ra ngoài
  dung sai, tên khác, dấu hiệu khác). ⇒ **Ⓑ′ thoả cả hai trường phái cùng lúc.**

**Cơ chế sinh ra khuyết tật ②, đáng ghi vào chương phương pháp:** `hop_le()` lọc khoảng cách bằng
**pixel** (80–350 px), còn thước phán bằng **norm-1000, hai trục riêng**. Trên màn 1080×2400, 350
px theo chiều **dọc** chỉ bằng **146** đơn vị norm — sát ngay ngưỡng 140. Hai hệ quy chiếu khác
nhau, không ai đối chiếu cho tới hôm nay.

**Cách làm:** thêm điều kiện vào `hop_le()` của `build_min_desc.py` → `build_min_desc_v2.py`:
`|dx| > 140 hoặc |dy| > 140` (norm-1000) · không được một vế `(no name)` còn vế kia có tên · ô
dấu hiệu phải khác nhau. Rồi chạy lại `do_eligibility.py` và phép chẩn đoán lối tắt.
⚠️ Số cặp sẽ tụt mạnh (ước còn ~5.000–7.000). **Không phải vấn đề**: `16 × 800 = 12.800 mẫu` nghĩa
là ở cấu hình hiện tại mô hình chỉ đi qua 56% một epoch, nên **chất lượng cặp quan trọng hơn số
lượng cặp** (Mục 1.4).

---

## 6. ⚠️ SỐ HỌC LẠNH LÙNG — đọc trước khi chi bất cứ giờ GPU nào

### 6.1 Hệ số chuyển đổi đo được trên chính dữ liệu này là **0,43**

| | ô khai báo "cả hai đúng" | exec_voronoi |
|---|---|---|
| S2/101 | 53,9% | 57,18% |
| MIN-DESC/101 | 60,6% | 60,05% |
| **Δ** | **+6,70 pp** | **+2,87 pp** |

⇒ **6,70 → 2,87 = hệ số 0,43**, rơi đúng giữa dải văn liệu **0,3–0,6** (Dong & Lapata, **ACL
2018**, tr. 731–742: 27–62% trên bốn tập; SeeAct **ICML 2024**: 0,58; UGround **ICLR 2025**:
0,23–0,33).

⇒ **Phần quy được cho ORPO đối cực là MIN − CE2 = +0,80 pp ở ô khai báo. Nhân 0,43 ⇒ dự báo
≈ +0,35 pp executability — kém MDE 2,2 pp của dự án SÁU LẦN.**

Đây là dự báo, không phải kết quả; điểm CE2 sẽ biến nó thành phép đo. Nhưng nó nói thẳng: **kể cả
Ⓑ′ làm tốt, hiệu ứng thành phần nhiều khả năng vẫn nằm dưới ngưỡng phát hiện của thiết kế đo hiện
tại.** Phải biết điều đó trước khi chi, không phải sau.

### 6.2 ⛔ ĐỪNG chạy phép thử "nạp `<desc>` vàng" để đo dư địa — trần sẽ ẢO

Ba bài oracle mạnh nhất trong image captioning đều lấy bước trung gian vàng **từ chính câu tham
chiếu** ⇒ trần bị thổi phồng (Wu et al., **CVPR 2016**: *"associate each image with a set of
attributes **according to its captions**"* · Yao et al., **BMVC 2016** · Yao et al., **ICCV 2017**:
LSTM-A\* B-4 **55,9** so với 32,4).

**Đo trên dữ liệu của ta, miễn phí:** trên 3.473 bước có tên vàng, câu chuẩn của người **chứa
nguyên văn tên phần tử 53,9%**, chứa ít nhất một từ đặc trưng của tên **60,5%**.
⇒ Nạp `<desc>` vàng vào câu nhắc là **mớm sẵn hơn một nửa chữ khoá của câu đích**. Trần đo được
sẽ là số ảo, và ta sẽ kết luận nhầm rằng ô khai báo còn nhiều dư địa.
⇒ **Nhánh `--ceiling gold` ở `infer_branch.py:480` KHÔNG dùng được làm cổng dư địa cho MIN-DESC.**
(Nó vẫn dùng được cho mục đích ban đầu — đo trần của **thước**, nơi rò rỉ này là *mong muốn*.)

### 6.3 Thước của ta là listener metric — có tiền lệ bình duyệt cho việc nó KHÔNG đơn điệu

**Luo & Shakhnarovich**, *Comprehension-Guided Referring Expressions*, **CVPR 2017**, tr. 3125–3134
— bài duy nhất đo **cùng lúc** độ chính xác listener máy và độ hiểu của người trên chính câu quy
chiếu sinh ra:

| RefCOCO TestA | listener acc | người hiểu đúng |
|---|---|---|
| MMI | 78,78% | 53% |
| SMIXEC | 79,99% | 62% |
| Rerank | **97,23%** | **66%** |

Listener nhảy **+17,2 pp** mua được **+4 pp** ở người. Trên RefCOCO+ TestA quan hệ **đảo chiều**:
Rerank listener 77,32 > SMIXEC 69,05, nhưng người 43% < 46%.
⇒ **Executability là listener metric.** Đây là tiền lệ đã bình duyệt cho giới hạn phải khai trong
bài, và nó mạnh hơn cách khai hiện tại. ⭐ Đưa vào Limitations của FAIR.

### 6.4 Một điểm sáng về mặt tiền lệ

**Wang et al.**, *Towards Understanding Chain-of-Thought Prompting*, **ACL 2023**, tr. 2717–2739,
Bảng 2: độ đúng của bước trung gian **mà mô hình TỰ SINH** tương quan gần **1:1** với độ đúng đầu
cuối (r=0,976, hệ số góc 0,97 — *phép tính của ta từ bảng của họ, bài không in*). Nhưng độ đúng
của cái **ta DẠY** ở bước trung gian thì gần như **không** chuyển đổi (làm hỏng lý luận trong ví
dụ mẫu vẫn giữ *"over 90% of the performance"*).
⇒ **MIN-DESC nằm ở vế thứ nhất** — nó cải thiện cái mô hình tự sinh. Đó là lý do tiền lệ để tin
cơ chế, dù độ lớn hiện đo được còn nhỏ.
⚠️ Tương quan của họ đo trên cùng một chuỗi sinh ra nên có phần **cơ học**, không phải nhân quả.

### 6.5 ⭐ Thứ ta đang có mà tiền lệ KHÔNG có

Không bài nào trong danh sách tra được đo tương quan bước-trung-gian ↔ đầu-ra ở **MỨC TỪNG MẪU**.
Tất cả đều ở mức hệ thống (so hai cấu hình). **Bảng 2×2 mức-mẫu của ta** (Mục 1.3 và `report/106`
mục x10b) mạnh hơn phần lớn tiền lệ tìm được — đó là chỗ có thể thành đóng góp thật, kể cả khi
Δ_component không vượt ngưỡng.
⚠️ Vẫn là **tương quan quan sát**, không phải hiệu ứng can thiệp — nhóm "desc sai" là nhóm bước
khó hơn sẵn. Cùng dạng giới hạn đã tự khai với nhóm 325 bước ở chẩn đoán 4j-18.

---

## 7. Quyết định — thứ tự việc, không có việc nào tiêu GPU trước việc 3

| # | việc | giá | quyết được gì |
|---|---|---|---|
| **1** | Chờ **CE2-S2/101** chấm xong (đang chạy) | 0 (đã chi) | biến dự báo +0,35 pp thành **phép đo** `Δ_component` |
| **2** | Dựng **`build_min_desc_v2.py`** theo Ⓑ′ + chạy lại `do_eligibility.py` + phép chẩn đoán lối tắt kiểu mDPO | **0 giờ GPU** | biết còn bao nhiêu cặp, lề đổi thế nào, có còn tách được không cần ảnh không |
| **3** | Chỉ khi (2) cho tập cặp lành mạnh → train MIN-DESC-v2/101 + CE2-v2/101 | ~8 h Colab + 10,8 h Kaggle | một điểm thăm dò nữa |
| 4 | (tuỳ chọn, đắt hơn) **negative on-policy** — dùng khai báo mà chính S2 đoán SAI trên màn tập dạy làm `desc_neg` | + ~5 h suy luận | nhắm đúng 90% khối lỗi mà heuristic hàng xóm bỏ sót; tiền lệ: UI-TARS *(preprint)*, nguyên lý FaceNet CVPR 2015 + Robinson ICLR 2021 |

⛔ **KHÔNG làm:** Ⓐ (đổi câu vế bị loại) · siết hard negative khó hơn · `--ceiling gold` làm cổng
dư địa · ghép hai thay đổi trong một biến thể.

⚠️ **Chữ cấm dùng** nếu về sau chạy Ⓐ hoặc viết về negative: **Yu et al., CVPR 2017** đã chiếm ý
*"negative là biểu thức của phần tử gây nhiễu"* từ 2017; **UIBert, IJCAI 2021** đã chiếm ý
*"k phần tử gần nhất làm negative"* trong miền GUI. Cấm *"đầu tiên"/"mới"* cho cả hai ý.

⚠️ **Preprint, chưa có venue — không được trình như đã bình duyệt:** Step-DPO (2406.18629) ·
DPO-Positive/Smaug (2402.13228) · UI-TARS (2501.12326) · LPO (2506.09373, tác giả khai Findings
ACL 2026 nhưng chưa xác minh độc lập được) · ROSCOE (2212.07919) · Lanham et al. (2307.13702).
