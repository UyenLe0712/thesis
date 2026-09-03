# 133 — Context đầy đủ cho phiên debate: đi đâu sau khi cổng G6 trượt

> Viết 3/9/2026, ngay sau khi có kết quả cổng G6 và phép thử ép chọn.
> **Mục đích của file:** đưa cho một phiên trò chuyện khác đọc một mình là đủ hiểu, rồi phản
> biện phán quyết ở Mục 8. Không cần mở file nào khác, trừ khi muốn tra nguồn gốc một con số.
> File này **không thay** `report/132` — 132 là kế hoạch và nhật ký thi hành, 133 là bản gói
> gọn để tranh luận.

---

## 1. Dự án đang làm gì

Luận văn thạc sĩ. Bài toán: cho **ảnh chụp màn hình Android** + **mục tiêu người dùng**, sinh
ra **câu hướng dẫn** cho bước thao tác kế tiếp.

Thước đo chính là **executability**: đưa câu sinh ra cho một mô hình định vị độc lập
(UGround-V1-2B) và xem nó có trỏ trúng phần tử đúng không. Câu do người viết đạt **75,7%** —
đó là trần của thước, và là giới hạn của dụng cụ chứ không phải của ngôn ngữ.

Các nhánh đã đo trước sprint này (cùng 4.463 bước chạm của tập kiểm):

| nhánh | executability |
|---|---|
| câu chuẩn của người (trần) | **75,7%** |
| MIN-DESC (ORPO tầng khai báo) | **60,0%** |
| S1 hạt 101 (SFT trơn) | **59,1%** |
| mô hình gốc chưa huấn luyện | **47,6%** |

Đóng góp mô hình hiện chốt ở MIN-DESC, ô **TRẮNG** (Δ = +0,63 pp, p=0,011, KTC
[+0,16 · +1,10], dưới MDE 2,11 của thiết kế một hạt giống).

---

## 2. Sprint `gui_sel` — thiết kế đã đăng ký trước

Ý tưởng: đưa vào câu nhắc một **khối ứng viên** (tối đa 40 dòng, mỗi dòng là tên phần tử +
toạ độ, trích từ OCR và cây trợ năng), và dạy mô hình **chọn tường minh** một dòng trước khi
viết câu.

Đích sinh là MỘT chuỗi liền:

```
<sel>TÊN PHẦN TỬ <point>x,y</point></sel>
câu hướng dẫn cho người dùng
```

hoặc `<sel>none</sel>` + câu, khi không ứng viên nào là phần tử đích.

**Thiết kế ba tầng, mỗi tầng đổi đúng một biến:**

| nhánh | câu nhắc | đích sinh |
|---|---|---|
| `gui_s1_match` | 24 dòng OCR, **không** menu | câu |
| `gui_sft_match` | **khối ứng viên** | câu |
| `gui_sel` | khối ứng viên | **`<sel>` + câu** |

`Δ_menu = sft_match − s1_match` · **`Δ_sel = sel − sft_match` là đại lượng CHÍNH**.

Kế hoạch: 6 lượt (3 nhánh × 2 hạt giống). **Mới chạy đúng 1 lượt** (`gui_sel`/101).

**Cấu hình:** Qwen2.5-VL-3B-Instruct, QLoRA 4-bit rank 8 alpha 16 dropout 0,05, freeze vision
tower, 1 epoch, lr 1e-4 cosine, warmup 5%, cỡ lô hiệu dụng 16, cutoff 3072, LLaMA-Factory pin
`c4e09c7cbe18`. 4.036 bước trên 64.567 mẫu, ~23 giờ A100.
⚠️ **`val_size: 0.0`, `do_eval: false`** — không chừa val. Đây là thiếu sót thiết kế đã nhận.

---

## 3. Cổng G6 và kết quả

**Cổng đăng ký trước** (`report/132` §5, khoá TRƯỚC khi train): `sel_acc` ≥ **63,6%** trên
bước có ứng viên vàng. Trượt ⇒ **dừng cả sprint**, bài đổi thành báo cáo âm.

**Kết quả: 57,5% (580/1008) — TRƯỢT, kém 6,1 điểm.**

Đã xác minh ba lượt trước khi tin con số:

| kiểm | kết quả |
|---|---|
| `raw` có thẻ `<sel>` | 1400/1400 = **100%** |
| tên chọn nằm trong khối ứng viên | 814/817 = **99,6%** ⇒ câu nhắc CÓ menu, mô hình thật sự đọc danh sách |
| cỡ mẫu trong phạm vi cổng | **1.008**, lớn hơn 600 mà §5 yêu cầu |

⚠️ Lỗi đã bắt và vá trong lượt chấm đầu: cổng đọc trường `pred`, mà `strip_desc()` đã bóc thẻ
`<sel>` khỏi `pred` (đúng thiết kế — câu đem chấm không được chứa đáp án). Kết quả in ra
**0,0% ở mọi cột**, trông y như mô hình không học được gì. Nguồn đúng là `raw`.

---

## 4. Mổ xẻ: điểm mất ở đâu

### 4.1 Phân rã hai vế

```
sel_acc 57,5%  =  72,9% (dám chọn)  ×  78,9% (chọn đúng khi đã dám)
```

Trong 735 lần dám chọn: **580 đúng cả tên lẫn điểm** · 46 điểm đúng tên sai · **4 tên đúng
điểm sai** · 103 sai cả hai.

Để chạm 63,6% cần **một trong hai**: giữ 78,9% đúng thì phải dám chọn ≥80,6%; hoặc giữ 72,9%
dám chọn thì phải đúng ≥87,2%. Cả hai cách hiện tại 8 điểm.

### 4.2 ⭐ Mô hình PHÂN BIỆT ĐƯỢC — không phải tái tạo prior

| nhóm | n | mô hình trả `none` | nhãn đúng |
|---|---|---|---|
| **A** — chạm, **có** ứng viên vàng | 1008 | **27,1%** | CHỌN |
| **B** — chạm, **không** có tên vàng | 288 | **80,2%** | `none` ✓ |
| **C** — chạm, có tên nhưng không khớp ứng viên | 104 | **74,0%** | `none` ✓ |

Khoảng cách 80,2% so với 27,1% loại bỏ giả thuyết *"mô hình bắt chước tỉ lệ nhãn"* — prior
`none` của bước chạm trong tập dạy là 29,1%, mà mô hình cho ra hai tỉ lệ khác hẳn nhau tuỳ
nhóm. Đọc như bộ phân loại nhị phân *"có nên chọn không"*: recall **72,9%**, specificity
**78,6%**, đúng **74,5%** trên 1.400 bước.

### 4.3 Phép thử ép chọn

Cấm mọi cách viết `none` lúc sinh (`--force-sel`), chạy lại đúng 273 ca đã bỏ cuộc.
**Kết quả: 42,5% (116/273).**

⇒ Bỏ cuộc là **tín hiệu thật** (42,5% thấp hơn hẳn 78,9%) nhưng **quá tay** (42,5% vẫn hơn
0% mà `none` mang lại).

### 4.4 ⛔ Ép chọn LỖ ở mọi ngưỡng

| chỉ ép khi khối ≥ | lãi nhóm A | lỗ nhóm B+C | so nền |
|---|---|---|---|
| 0 (ép tất) | +116,0 | −308 | **−13,7 pp** |
| 15 | +90,0 | −226 | −9,7 pp |
| 25 | +70,0 | −162 | −6,6 pp |
| 35 | +50,0 | −122 | −5,1 pp |
| **không ép** | 0 | 0 | **0,0 pp ← tốt nhất** |

Nền: **888/1400 = 63,4%** đúng trên bước chạm. Lý do lỗ: trong 581 ca abstain chỉ **47%**
thuộc nhóm A, mà **điều kiện hoà vốn đòi 69,4%** (mỗi ca chuyển được thêm 0,44 điểm kỳ vọng,
mỗi ca abstain đúng bị phá mất 1,00).

### 4.5 ⭐ CÁI BẪY CỦA THƯỚC

| | `sel_acc` (chỉ nhóm A) | đúng trên cả 1.400 bước |
|---|---|---|
| hiện nay | 57,5% | **63,3%** |
| bỏ abstain hoàn toàn | **69,5%** (+11,9) | 50,0% (**−13,3**) |

**Thước đang dùng thưởng cho hành vi làm hệ thống tệ đi.** `sel_acc` chính là cột *HasAns*
của SQuAD 2.0 báo một mình.

---

## 5. Hai phát hiện có giá trị khoa học độc lập

### 5.1 Điểm nghẽn là NHẬN DIỆN, không phải ĐỊNH VỊ — tỉ số 34:1

273 ca ép chọn: đúng cả hai **116** · **điểm đúng tên sai 34** · **tên đúng điểm sai 1** · sai
cả hai 122. Nhóm tự nguyện chọn cũng vậy: 580 · 46 · **4** · 103.

⇒ Khi mô hình nhận ra phần tử thì toạ độ **gần như luôn chuẩn** (toạ độ được chép nguyên dòng
từ khối ứng viên). Chỗ hỏng là **quyết định phần tử nào là đích**.

**122 ca sai cả hai**: khoảng cách tới ứng viên vàng **p25 268 · trung vị 398 · p75 570** trên
lưới 1000 (dung sai 140); chỉ **25,8%** nằm trong hai lần dung sai ⇒ khi sai, mô hình **không
lẫn sang nút bên cạnh mà nhìn sang vùng khác hẳn màn hình**.

⭐ **Tái lập độc lập** của `report/106` mục (x13c) đo trên nhánh MIN-DESC ngày 25/8: khoảng
cách phần-tử-nhầm ↔ gold có p25 70 px · trung vị 351 · p75 748, **76,5% nằm ngoài dải 80–350**.
Hai can thiệp khác nhau, hai cơ chế khác nhau, hai lượt train khác nhau, **cùng một dạng lỗi
lưỡng cực**. Đây cũng là lý do MIN-ONPOLICY chết ở cổng eligibility 3,3%.

### 5.2 Lẫn loại thao tác là dấu hiệu mạnh nhất của bỏ cuộc

Đọc chính câu hướng dẫn mô hình sinh kèm mỗi ca `none` sai:

| | 273 ca **bỏ cuộc** | 735 ca **dám chọn** |
|---|---|---|
| câu mang động từ **không chạm** (swipe · back · type · scroll) | **108 = 39,6%** | 15 = **2,0%** |

Chênh **+37,5 pp, gấp 20 lần**. Ví dụ thật: *"Swipe up to view more options."* ·
*"Type 9877655532 in the phone number section."* — trong khi thao tác vàng là một cú **chạm**.

⭐ **Tái lập chẩn đoán 4j-18** (`report/110`, tháng 8, nhánh S2): nhóm 325 bước không kích hoạt
khai báo cũng đúng kiểu này, và **Base đoán đúng loại thao tác nhiều hơn CẢ HAI bản đã huấn
luyện** (83,4% vs S1 55,1% vs S2 38,8%) ⇒ **cái giá của SFT**.

⚠️ **Nhưng không phải nguyên nhân duy nhất.** Ép chọn tách theo nhóm: ca lẫn loại thao tác
đúng **37,0%** (n=108), ca không lẫn **46,1%** (n=165) — chênh chỉ 9 pp, và nhóm không lẫn vẫn
xa 78,9%. Bỏ cuộc thừa có **ít nhất hai nguồn chồng lên nhau**.

### 5.3 Đặc trưng nào dự báo bỏ cuộc

| trục | phán |
|---|---|
| **cỡ khối** | **biến thật**: 18,8% → 25,0% → 32,9% → **34,9%** theo bốn tầng, đơn điệu, chênh 16 pp |
| vị trí tương đối trong danh sách | **vô can**: 0,478 vs 0,471, chênh 0,006 |
| tên có chữ số | tín hiệu yếu: 24,2% vs 13,6% |
| độ dài tên · trùng tên · cùng vai · nguồn tên (OCR/a11y) | không khác |

⚠️ Hiệu ứng vị trí thô (11,2 vs 8,5) **hoàn toàn do cỡ khối** — phải phân tầng trước khi đọc.
**Nghịch lý:** khối lớn khiến bỏ cuộc nhiều nhất (34,9%) nhưng ép chọn trên khối lớn lại đúng
nhiều nhất (**49,5%** vs 31,2% ở khối 15–24).

---

## 6. Dữ liệu

**Tập dạy:** 64.567 mẫu, **54,8% đích là `<sel>none</sel>`** = 36,2% bước không chạm + 14,1%
chạm không tên vàng + 4,4% chạm có tên không khớp.
Dữ liệu **không tự mâu thuẫn**: nhãn `none` chỉ khi `gold_candidate()` trả None.
Khối ứng viên: độ phủ tên vàng **96,7%**, khớp tên ∧ điểm ±14% là **91,2%** (cao hơn Recall@50
= 88,9% của Mind2Web).

**Tập kiểm:** 6.958 bước, 4.463 bước chạm.
· **1.400 bước chạm** đã suy luận = **DEV**, đã chạm hai lần (cổng G6 + ép chọn).
· **3.063 bước chạm còn lại** = **HOLD-OUT**, chưa chạm lần nào, chỉ được chạm MỘT lần.

---

## 7. Năm hướng research đã tra (3/9, năm agent song song)

### 7.1 Abstention và calibration
· **Chow (IEEE T-IT 1970)**: nếu abstain sai và trả lời sai cùng 0 điểm thì ngưỡng tối ưu = 0.
  NHƯNG ở đây `none` là **lớp có đáp án đúng** (nhóm B, C) nên Chow không áp thẳng.
· **Cole et al. (EMNLP 2023)**: thiết kế "trả lời hoặc nói Unknown" kém đều so với chấm ngưỡng
  trên điểm tin cậy.
· Kỹ thuật rẻ: Robinson & Wingate (ICLR 2023) · Guo et al. (ICML 2017, temperature scaling) ·
  self-consistency · Vishwakarma et al. (ICLR 2025, conformal).
· Cần train: Kamath et al. (ACL 2020) · ASPIRE (Findings EMNLP 2023) · R-Tuning (NAACL 2024).

### 7.2 Listwise selection trong GUI
· Thứ tự có ảnh hưởng lớn nhưng đo trên mô hình **prompting**: Liu et al. (TACL 2024) ·
  Chi et al. (**workshop** NeurIPS 2024) · Pezeshkpour & Hruschka (Findings NAACL 2024) ·
  Zheng et al. (ICLR 2024 Spotlight, thiên vị token nhãn).
· ⚠️ **Đối trọng:** Mind2Web (NeurIPS 2023 D&B) xáo phần tử **cả lúc train lẫn suy luận**, 5
  hạt giống cho độ lệch chuẩn <1 điểm. Mô hình đã fine-tune thì không suy thẳng sang được.
· **AndroidControl (NeurIPS 2024 D&B) Phụ lục C.2**: LLM làm tốt **như nhau** khi xuất tâm
  phần tử hay chỉ số phần tử.
· ⭐ Khối ứng viên là truyền thống **web agent** (Mind2Web, SeeAct), gần như **vắng mặt ở
  nhánh di động** (SeeClick, CogAgent, Ferret-UI, Aguvis, UI-Ins đều chỉ dùng ảnh) ⇒ điểm phân
  định dùng được, **miễn không viết "đầu tiên"**.

### 7.3 Thước đo
· **SQuAD 2.0 (Rajpurkar, Jia, Liang, ACL 2018)**: báo EM/F1 **toàn bộ** cộng hai cột
  **HasAns** và **NoAns**. `sel_acc` chính là cột HasAns báo một mình.
· Risk–coverage + AURC: El-Yaniv & Wiener (JMLR 2010) · Geifman & El-Yaniv (NeurIPS 2017) ·
  Geifman et al. (ICLR 2019). Dùng cho LLM: Kamath (ACL 2020) · Xin et al. (ACL 2021) ·
  Varshney et al. (Findings ACL 2022). Cảnh báo: Traub et al. (NeurIPS 2024) — AURC che mất
  hành vi ở vùng coverage thực dụng, báo kèm risk tại vài mức coverage cố định.
· Macro-F1 **ba lớp là sai khái niệm** (A/B/C là phân tầng dữ liệu, không phải lớp).
· Tiền lệ tổ chức bài kết quả âm: Kaushik & Lipton (EMNLP 2018) · Michel, Levy, Neubig
  (NeurIPS 2019). Track riêng: Insights from Negative Results in NLP (6 kỳ 2020–2025).
· Đăng ký trước: van Miltenburg et al. (NAACL 2021) · NeurIPS 2020 Pre-registration Workshop
  (PMLR vol. 148).

### 7.4 Mất cân bằng nhãn (agent này TỰ ĐÍNH CHÍNH một trích dẫn quá rộng)
· **Focal loss: loại hẳn.** Li et al. (ACL 2020, *Dice Loss for Data-imbalanced NLP Tasks*) đo
  trên SQuAD 2.0 tỉ lệ âm:dương **82:1** — nặng hơn 54,8% nhiều — chỉ được **+0,30 F1** (BERT),
  +0,53 (XLNet), +1,24 (QuoRef 169:1), **−0,05** (SQuAD 1.1 XLNet EM). Dưới cả σ hạt giống
  0,46 và MDE 2,11.
· ⛔ **Không có công trình bình duyệt nào nói focal loss gây hại cho language generation** —
  đừng viết câu đó.
· **Loại bớt mẫu lớp đa số: bằng chứng đi NGƯỢC.** Henning et al. (EACL 2023 survey): ROS
  thắng RUS. Tayyar Madabushi et al. (NLP4IF@EMNLP 2019): oversampling **−1,1 pp F1 khi
  train/test cùng phân bố**, +4,7 pp khi lệch; BERT tự xử lý được mất cân bằng.
· **Zhao et al. (ICML 2021, Calibrate Before Use)**: majority label bias tồn tại **ngay cả khi
  đầu ra là văn sinh**; contextual calibration = biến đổi affine trên xác suất, **không train
  lại**, tới **+30,0 điểm tuyệt đối**.
· ⭐ **Devlin et al. (NAACL 2019)**: SQuAD 2.0 dự đoán non-null khi `ŝ_ij > s_null + τ`, **τ
  chọn trên dev**. Tiền lệ chuẩn ngành, đúng y hệt việc đang định làm.
· Kamath et al. (ACL 2020): abstain có calibrator trả lời **56%** câu ở mức 80% accuracy so
  với **48%** nếu dùng softmax trần. Srinivasan et al. (Findings ACL 2024, VLM): +tới 20%
  coverage không giảm accuracy.

### 7.5 Structured decoding
· GENRE (De Cao et al., ICLR 2021): trie-constrained beam search cho tên thực thể.
· Geng et al. (EMNLP 2023): F1 17,5→36,0 (trích xuất thông tin), 54,1%→80,3% (NER) — ⚠️ mô
  hình **chưa fine-tune**, phần lớn mức tăng là sửa lỗi định dạng.
· ⛔ **Trie đã chết bằng số của chính dự án: 98,2% tên mô hình chọn ĐÃ nằm trong khối** (268/273)
  ⇒ không còn gì để cấm.
· Đánh số ứng viên rồi sinh số: Robinson & Wingate (ICLR 2023) cho MCP thắng cloze 16/20 tập,
  +9,7 pp — ⚠️ nhưng cùng bài đó thấy mô hình cỡ nhỏ **nằm sát mức đoán ngẫu nhiên** ở năng
  lực này, và 3B nằm đúng vùng rủi ro; cộng lệch train-test ⇒ phải train lại.
· Tách hai giai đoạn · pointer/copy: không có bằng chứng bình duyệt so trực tiếp, bỏ.

---

## 8. ⭐ PHÁN QUYẾT — phần cần debate

### 8.1 Việc phải làm

| # | việc | giờ GPU | cơ sở |
|---|---|---|---|
| 1 | **Ngưỡng τ kiểu Devlin** trên `log p(none) − log p(ứng viên tốt nhất)` tại bước quyết định. Quét τ trên lát 1.400 (dev), chọn theo **đúng toàn bộ** chứ không theo `sel_acc`, áp **một lần** lên 3.063 bước hold-out | 0 A100 · ~2 h T4 | Devlin (NAACL 2019) · Kamath (ACL 2020) |
| 2 | ✅ Đếm tên ngoài khối | 0 | xong: 98,2% trong khối ⇒ trie vô giá trị |
| 3 | **Chấm executability** cho `gui_sel`/101 trên 4.463 bước | 5,6 h Kaggle | G6 chỉ là cổng proxy, `exec` mới là estimand thật |
| 4 | ✅ Kiểm lẫn loại thao tác | 0 | xong, Mục 5.2 |

### 8.2 Không làm, mỗi thứ một lý do đo được
focal loss · loại bớt mẫu lớp đa số · đánh số ứng viên rồi sinh số · tách hai giai đoạn ·
trie · self-consistency · ép chọn (lỗ ở cả bốn ngưỡng).

### 8.3 Phân bổ hai lượt A100 còn lại

⚠️ Luật khoá nói trượt G6 thì **dừng sprint sáu lượt**, và điều đó giữ nguyên. Nhưng luật dừng
*sprint*, không cấm dùng ngân sách cho câu hỏi khác — với điều kiện **ghi thành mục sửa đổi và
commit TRƯỚC khi bấm train**.

| lượt | nhánh | vì sao |
|---|---|---|
| 1 | **`gui_sft_match`/101** (~23 h) | không có nó thì báo cáo âm chỉ nói được "trượt một ngưỡng", không nói được đầu chọn có làm `exec` tệ đi hay không |
| 2 | **`gui_sel`/202** (~23 h) | σ giữa hạt giống trên `sel_acc` **chưa ai đo** |
| 3 | **không chạy** | giữ làm đệm mất máy |

⛔ Bỏ `S1-match` và `gui_sft_match`/202. `Δ_sel` một hạt giống nằm dưới MDE 2,11 **theo thiết
kế** ⇒ phải khai là trắng ngay từ đầu.

### 8.4 Trục đóng góp SOICT — nộp bản SHORT 8–11 trang

*(i)* Kiểm định theo thiết kế đăng ký trước một đầu chọn tường minh trên khối ứng viên cho
Qwen2.5-VL-3B ở miền di động; nó **trượt cổng đã khoá** (57,5% so với 63,6%).
*(ii)* Dạng lỗi là **bỏ cuộc thừa**: 27,1% `none` trên bước có đáp án; và thước `sel_acc` chỉ
đếm cột HasAns nên **cộng 11,9 điểm cho việc bỏ hẳn abstain trong khi độ đúng toàn bộ tụt
13,3 điểm**.
*(iii)* Thay bằng bộ thước kiểu **SQuAD 2.0** cộng risk–coverage, và một ngưỡng τ chỉnh trên
dev, đo **một lần** trên hold-out.

**Đóng góp là (ii) và (iii).** (i), `Δ_sel`, `exec` và hạt 202 là **bằng chứng**.
⚠️ Câu (ii) phải viết là *thước do chính chúng tôi đăng ký đã dẫn chúng tôi sai*, **không**
viết như phát hiện về thước của người khác.

### 8.5 Ranh giới trung thực — phải khai trong bài

lát 1.400 đã chạm **hai lần** ⇒ mọi số trên đó là dev · G6 trượt và **giữ nguyên trượt**, τ là
luật đọc hậu kiểm chứ không thay cổng · τ chỉnh trên dev, hold-out chạm **một lần**, in kết
quả **kể cả khi τ = ∞** · train **không chừa val** · 42,5% ép chọn, cỡ khối, vị trí đều là
**hậu kiểm một hạt giống** · kế hoạch sáu lượt bị thay ở đâu, ngày nào, commit nào · `sel_acc`
là thước **do chính dự án đăng ký**.

### 8.6 ⛔ Câu không được viết
*"điểm nghẽn ở định vị thị giác"* (tỉ số 34:1 bác thẳng) · *"focal loss gây hại cho sinh văn
bản"* (không nguồn) · *"đầu tiên"* cho khối ứng viên ở di động · so số với Chi et al. hay
Pezeshkpour (họ đo trên mô hình prompting) · *"mô hình học prior 54,8%"* (bằng chứng ngược:
80,2% vs 27,1%) · *"τ cải thiện hệ thống"* trước khi có số hold-out · trong abstract 9/9
**không hứa số chưa đo**.

---

## 9. Ràng buộc

· **Ngân sách**: còn 2–3 lượt A100 (15–23 h/lượt). Kaggle T4 **miễn phí**, 30 h/tuần, dùng cho
  mọi khâu suy luận và chấm.
· **Deadline SOICT 2026**: abstract **9/9/2026**, full paper **16/9/2026**, kỷ yếu Springer
  CCIS, hội nghị 4–5/12 tại TP.HCM. Full 12–15 trang, short 8–11 trang. **Hôm nay 3/9/2026.**
· Hai bài khác đã nộp: **FAIR'2026** (đóng góp mô hình, chờ kết quả 15/9) và **VCL2026**
  (bộ ngữ liệu quy chiếu).
· Luận văn cần bảo vệ; chương chẩn đoán đang thiếu nội dung, và hai phát hiện ở Mục 5 lấp
  đúng chỗ đó.
· ⛔ Dự án đã **tự khai hai lần** nới ngưỡng sau khi thấy điểm. Lần thứ ba là mất hẳn lập luận
  đăng ký trước — lá chắn mạnh nhất của cả ba bài.

---

## 10. Câu hỏi cho phiên debate

1. Phán quyết ở **8.3** có đúng không: dùng hai lượt A100 cuối cho `gui_sft_match`/101 và
   `gui_sel`/202, thay vì thử một can thiệp mới? Lập luận phản đối mạnh nhất là gì?
2. Trục đóng góp ở **8.4** có đủ sức cho Springer CCIS không, hay nên bỏ SOICT và dồn vào
   luận văn? Nếu nộp thì short hay full?
3. Có hướng kỹ thuật nào **0 giờ A100** mà cả năm agent lẫn phán quyết đều bỏ sót?
4. Hai phát hiện ở **Mục 5** (tỉ số 34:1 và lẫn loại thao tác) có đủ mạnh để làm đóng góp
   chính thay cho (ii)+(iii) không?
5. Ngưỡng τ ở **8.1** có rủi ro gì chưa lường: nếu quét trên dev rồi áp hold-out mà kết quả
   xấu đi thì đọc thế nào?
6. Chỗ nào trong file này kết luận **vượt quá bằng chứng**?
