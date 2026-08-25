# 121 — ĐỀ XUẤT GIAI ĐOẠN THÁNG 9, BẢN ĐẦY ĐỦ ĐỂ PHẢN BIỆN

> Viết 25/8/2026. **Mục đích: đưa cho một người/một hệ thống KHÁC đọc và đánh giá.**
> Tự chứa — không cần mở file nào khác cũng hiểu được. Mọi con số trong đây đều đã đo,
> nguồn ghi ngay cạnh. Chỗ nào là **ước lượng** hoặc **dự báo** đều nói rõ.
>
> ⚠️ **Người phản biện hãy tấn công thẳng vào Mục 9** — đó là danh sách những chỗ tôi
> tự thấy yếu nhất. Nếu bạn lật được một trong số đó, chúng tôi tiết kiệm hàng chục giờ GPU.

---

## 0. TÓM TẮT MỘT TRANG

**Bài toán.** Cho ảnh chụp màn hình Android + mục tiêu của người dùng, sinh **một câu tiếng Anh**
bảo người ta chạm vào đâu ở bước này. Không phải sinh toạ độ — sinh **câu cho người đọc**.

**Cách chấm (`executability`).** Câu sinh ra được đưa cho một **mô hình định vị GUI độc lập**
(UGround-V1-2B), mô hình đó trả về một toạ độ; bước tính là đạt khi **loại thao tác khớp** câu
chuẩn của người **và** toạ độ rơi vào ô Voronoi của phần tử người dùng đã chạm. Mẫu số cố định
**4.463 bước chạm**.

**Trạng thái.** Trần (câu người) **75,73%**. Mô hình gốc **47,59%**. Nhánh tốt nhất đã train
**MIN-DESC 60,05%**.

**Cái vừa đo được và nó đổi mọi thứ.** Phân rã 4.463 bước theo việc khai báo của mô hình đúng
tên / đúng toạ độ: **63% dư địa còn lại nằm gọn trong 745 bước (16,7%)** nơi mô hình **nhắm sai
hẳn phần tử**. Ở đó mô hình được **3,6%** trong khi nhánh đối chứng đơn giản hơn (S1) được
**25,8%** và câu người được 64,4%. Ô lớn nhất (46,7% số bước) thì mô hình **đã vượt trần câu
người**. ⇒ **Không còn chỗ nào khác để lấy điểm.**

**Hệ quả.** Mọi thủ thuật ở khâu suy luận đều chạm trần rất sớm — bộ định tuyến **hoàn hảo**
(oracle) cũng chỉ cho **63,46%**. Muốn hơn thì phải **thật sự sửa việc nhắm sai phần tử**.

**Đề xuất.** Ba nhánh, đăng ký trước ở `report/106` mục (x14):
① **NHÁNH-ỨNG-VIÊN** — đưa danh sách phần tử trên màn **kèm toạ độ** vào **đầu vào**;
② **NHÁNH-LÙI** — dạy mô hình **nói "không chắc"** ở đúng những bước nó từng sai;
③ **MIX** — vá một điều kiện claim đang trượt, không nhắm điểm.

**Mục tiêu số.** Ngưỡng **DƯƠNG** của luật niêm phong 5/8 là Δ ≥ +2,8 pp so S1 ⇒ mức tuyệt đối
**≥ 62,16%**. Hiện 60,05% (Δ +0,69). Ước xác suất đạt: **~60%**. Chạm 65% thì khoảng **~30%**.

**Giá.** ~140 giờ A100 + ~43 giờ chấm Kaggle cho kịch bản đầy đủ, trong 9 tuần.

---

## 1. NỀN — đủ để người ngoài đọc hiểu

### 1.1 Dữ liệu
Nguồn **AndroidControl** (Li et al., Google DeepMind, **NeurIPS 2024 Datasets & Benchmarks**,
arXiv 2406.03679, CC0). Ghép hai kho HuggingFace theo `(episode_id, step_id)`:
`HarrytheOrange/parsed_AndroidControl` (câu người viết cho từng bước + cây trợ năng 99.131 màn)
với `ckg/AndroidControlParsedWithImages-20k` (ảnh).

· **Dạy:** 64.567 bước / 41.191 chạm / 12.895 tác vụ. Rò rỉ dạy-kiểm = **0**.
· **Kiểm:** 6.958 bước / **4.463 bước chạm** / 1.432 tác vụ.
· ⚠️ `history` trong câu nhắc là **câu chuẩn do người viết** ở các bước trước ⇒ khâu chấm là
  **teacher-forced trên ngữ cảnh**; mọi số tuyệt đối phải đọc kèm điều kiện đó.

### 1.2 Mô hình và huấn luyện
Qwen2.5-VL-3B-Instruct, **QLoRA 4-bit**, A100 40 GB, `cutoff_len` 2560, gradient checkpointing.
Một lượt SFT đầy đủ = **8.072 bước ≈ 23 giờ**. Stage-2 = 800 update ≈ **4,7 giờ**.

### 1.3 Các nhánh đã có
| tên | là gì |
|---|---|
| **Base** | mô hình gốc, không huấn luyện |
| **S1** | SFT trơn: đích sinh là **câu**, hết |
| **S2** | SFT "mô tả trước, phát ngôn sau": đích là `<desc>vai trò \| tên \| <point>x,y</point> \| dấu hiệu phân biệt</desc>` **rồi mới tới câu**. Chấm **chỉ lấy câu** |
| **CE2-S2** | từ checkpoint S2, **800 update SFT thuần** — đây là **đối chứng quy công** |
| **MIN-DESC** | từ checkpoint S2, **800 update ORPO** trên cặp quy chiếu tối thiểu ở tầng khai báo |

**Cặp của MIN-DESC:** `chosen = <desc>đúng</desc> + "\n" + câu`, `rejected = <desc>sai</desc> +
"\n" + **CÂU Y HỆT**. Chỉ ô khai báo đổi ⇒ gradient rơi đúng vào việc **chọn phần tử**.
(ORPO: Hong et al., **EMNLP 2024**.)

### 1.4 Kỷ luật đăng ký trước
`report/106_DANG_KY_TRUOC.md` niêm phong 5/8/2026 (commit `b93e85c`), khoá: 6 nhánh · thước đo ·
**luật đọc kết quả cho cả bốn kết cục** · 3 lát cắt · hạt giống. Mọi thay đổi về sau ghi vào
**mục sửa đổi đánh chữ**, không sửa đè. Hiện có **28 mục**, **21 mục trước điểm số đầu tiên**.
Kiểm được bằng `git log`.
⚠️ Dự án **tự khai đã hai lần nới ngưỡng sau khi thấy điểm** (ghi trong bài). Đó là lý do mọi
ngưỡng ở đây được khoá kèm ngày và commit.

---

## 2. SỐ HIỆN CÓ

### 2.1 Sáu nhánh, ghép cặp trên đúng 4.463 bước
| nhánh | executability | KTC95 | action_ok | hit_voronoi thuần |
|---|---|---|---|---|
| trần (câu người) | **75,73%** | [74,1 · 77,3] | 100 | 75,8 |
| **MIN-DESC/101** | **60,05%** | [58,33 · 61,77] | 98,9 | 60,4 |
| **CE2-S2/101** | **59,42%** | [57,69 · 61,14] | 98,9 | 59,8 |
| S1/101 | 59,11% | [57,3 · 60,8] | 94,4 | 60,2 |
| S2/101 | 57,18% | — | 94,9 | 58,1 |
| Base | 47,59% | — | 96,5 | 48,9 |

### 2.2 McNemar ghép cặp
| phép so | Δ pp | KTC95 | b | c | χ² | p |
|---|---|---|---|---|---|---|
| **MIN − CE2** (đại lượng chính) | **+0,63** | [+0,16 · +1,10] | 70 | 42 | 6,5 | **0,011** |
| CE2 − S2 | +2,24 | [+1,41 · +3,11] | 227 | 127 | 27,7 | 1,4e-07 |
| MIN − S2 | +2,87 | [+2,03 · +3,76] | 258 | 130 | 41,6 | 1,1e-10 |
| MIN − S1 | +0,94 | [−0,09 · +2,05] | 342 | 300 | 2,6 | 0,11 |
| CE2 − S1 | +0,31 | [−0,76 · +1,45] | 326 | 312 | 0,3 | 0,61 |

### 2.3 ⭐ Quy công — phần trung thực nhất
**S2 → CE2 = +2,24 pp** (SFT thuần) · **CE2 → MIN = +0,63 pp** (riêng mục tiêu ưu tiên)
⇒ **78% mức tăng của cả chặng thuộc về nhánh đối chứng.** Trình +2,87 như công của ORPO là
thổi phồng **gấp bốn lần**.

Và MIN-DESC **không vượt SFT trơn**: MIN − S1 = +0,94, p = 0,11. Cái nó làm được là **sửa thiệt
hại của chính S2** rồi nhô lên chút.

### 2.4 Nhiễu và ngưỡng
| nguồn | giá trị |
|---|---|
| nhiễu **thước** trên một cặp nhánh (bootstrap cụm) | SE **0,38 pp** |
| nhiễu **giữa hạt giống** (đo trên cặp S1/101 vs S1/202) | σ ≈ **0,46 pp**, ⚠️ **1 bậc tự do** |
| MDE 1 hạt giống | **2,11 pp** |
| MDE 2 hạt giống | 1,67 pp |
| **ngưỡng chốt, dòng thận trọng (σ×2)** | **2,8 pp** |

⇒ `Δ_component = +0,63` **có ý nghĩa trên nhiễu thước** (p=0,011) nhưng **dưới MDE**, và chỉ bằng
**1,4× σ giữa hạt giống** ⇒ **ô TRẮNG / inconclusive**.

### 2.5 ⚠️ SỬA MỘT CÁCH ĐỌC SAI — đọc kỹ chỗ này
Bảng dải khoá 5/8 định trên **Δ so S1 tính bằng pp**, cho **trung bình HAI hạt giống mỗi nhánh**:

| dải | Δ so S1 | mức tuyệt đối (S1 hai hạt = 59,36%) |
|---|---|---|
| TRẮNG | −2,8 … +1,7 | 56,56 – **61,06** |
| **DƯƠNG YẾU** | +1,7 … +2,8 | **61,06 – 62,16** |
| **DƯƠNG** | ≥ +2,8 | **≥ 62,16** |

· Trợ lý đã có lúc quy nhầm sang mức tuyệt đối và báo *"65% là ngưỡng dương yếu"* — **SAI**.
· Con số **65,0%** trong bài FAIR **đúng** nhưng trả lời câu khác: đó là điểm mà lượt **S2/202 đã
  huỷ** phải đạt để trung bình hai hạt của S2 chạm mép dương yếu (`2 × 61,06 − 57,18 = 64,95`).
· ⛔ **Ngưỡng không đổi một chữ** — vẫn +1,7 / +2,8 pp. Chỉ sửa phép quy đổi.
· ⛔ **Một hạt giống thì KHÔNG ĐƯỢC áp bảng** — bảng phát biểu cho trung bình hai hạt. Đó là lý
  do hai hạt giống là **điều kiện cần để có tuyên bố**, không phải thứ làm cho đẹp.

---

## 3. ⭐ PHÂN RÃ Ô — nền của mọi quyết định

Cắt 4.463 bước theo khai báo của MIN-DESC đúng tên / đúng toạ độ (so với nhãn vàng):

| ô | n | % | MIN | S1 | người | dư địa tới người |
|---|---|---|---|---|---|---|
| **A** tên✓ point✓ | 2.082 | 46,7% | **87,1** | 78,2 | 86,3 | **−0,36** |
| B tên✓ point✗ | 220 | 4,9% | 26,4 | 27,7 | 32,3 | +0,29 |
| C tên✗ point✓ | 411 | 9,2% | 57,2 | 53,0 | 73,0 | +1,46 |
| D không sinh desc | 15 | 0,3% | 0,0 | 0,0 | 60,0 | +0,20 |
| **D** tên✗ point✗ | **745** | **16,7%** | **3,6** | **25,8** | 64,4 | **+10,15** |
| ngoài lát (không có tên vàng) | 990 | 22,2% | 55,3 | 54,4 | 73,0 | +3,94 |
| **TỔNG** | 4.463 | | **60,05** | 59,11 | 75,73 | **+16,04** |

**Ba điều đọc ra:**
1. ⭐ **Ô A hết sạch chỗ** — MIN **vượt trần câu người** (87,1 vs 86,3) trên 46,7% số bước. Đây là
   kết quả mức-từng-mẫu, chưa thấy tiền lệ trình được.
2. ⭐ **63% dư địa nằm gọn ở ô D**, nơi **MIN 3,6% mà S1 25,8%** ⇒ khai báo sai **phá câu nặng hơn
   là không khai báo gì**. Đây là bản sắc nét của chẩn đoán "cơ chế bị chặn bởi độ chính xác khai
   báo".
3. **Trần của mọi can thiệp lúc suy luận rất thấp:**
   · định tuyến **hoàn hảo** (oracle: biết trước khai báo đúng/sai, sai thì lùi về S1) → **63,46%**
   · oracle chỉ ở ô D → **63,75%**
   · oracle **kép** (chọn nhánh tốt nhất từng bước ở ô D) → 66,23% — không dùng được, chỉ để tham chiếu
   ⇒ **Muốn 65% thì ô D phải đi từ 3,6% lên 33,3%.** Phải SỬA việc nhắm, không né được.

Tái lập: `python3 /home/uyenle/.claude/jobs/*/tmp/cells.py` (script phân tích, không gọi GPU).

---

## 4. ĐỀ XUẤT — ba nhánh

### ① NHÁNH-ỨNG-VIÊN — đường duy nhất nhắm vào ô D

**Ý.** Ô `<desc>` hiện là **sinh tự do**. Đổi thành **chọn trong danh sách ứng viên của chính màn
đó**: thêm vào **đầu vào** một khối `tên <point>x,y</point>` dựng từ **OCR (phủ 100% tập dạy) ∪
cây trợ năng offline**.

**Bốn số làm trụ (đo 25/8, 0 giờ GPU):**
| số | giá trị | nghĩa |
|---|---|---|
| **G1** tên vàng có trong khối ứng viên | **96,7%** | trần của cơ chế "chọn 1 ứng viên" |
| **G2** có ứng viên vừa khớp tên vừa trong ±140 lưới (C3) | **91,2%** | so với khai báo hiện tại **59,9%** ⇒ dư địa **+31,3 pp** ở tầng khai báo |
| câu nhắc hiện nhét | **24 dòng OCR, KHÔNG kèm toạ độ** | `build_branch_data.py:31` |
| trong số bước MIN gọi SAI tên, tên vàng đã nằm sẵn trong 24 dòng đó | **67,7%** | ⭐ **thông tin có sẵn mà mô hình không dùng được vì không có gì neo tên vào vị trí** |

✅ **G1 và G2 đo trên ĐỦ tập kiểm 4.463 màn** (3.505 bước có tên vàng), không phải mẫu — chạy
25/8 bằng `harness/build_candidates.py --split test --max 40`. Mẫu 1.074 màn tập dạy cho
96,0% / 91,1%, khớp. Vẫn phải đo lại ở quy mô đủ 41.099 màn **dạy** trước khi train, vì OCR đầy
đủ của tập dạy chỉ có trên Drive.

**✅ Cổng G3 — rò rỉ vị trí, đo trên 3.198 bước có ứng viên đúng:** vị trí tương đối của ứng viên
đúng trong danh sách có trung bình **0,474**, trung vị 0,43, và nằm ở vị trí **đầu tiên chỉ 4,8%**
(ngẫu nhiên đều ≈ 4,3%). Phân bố trải đều qua mười thập phân vị (17/12/11/8/6/8/7/7/6/4 %).
⇒ **Thứ tự đọc không tố cáo đáp án.** (13,8% nằm cuối là do danh sách ngắn, không phải tín hiệu.)

**Luật thiết kế, khoá trước:**
· Tên ứng viên đúc bằng **ĐÚNG** chuỗi hàm đã dựng nhãn vàng (`nodes_of` → `name_of`), không
  dùng OCR thô — nếu không sẽ đẻ ra chuỗi không tồn tại trong nhãn vàng, làm phủ tụt oan.
· Gộp cha-con bằng `overlapped` (cây trợ năng lồng nhiều tầng, ViewGroup bọc TextView cùng chữ).
· Sắp theo **thứ tự đọc** và cắt theo thứ tự đó. **Mọi cách sắp/cắt phụ thuộc phần tử đích đều là
  rò rỉ** — nó nói cho mô hình biết đáp án nằm đâu trong danh sách.
· Toạ độ dùng lưới [0,1000] **y hệt** ô `<point>` của khai báo ⇒ mô hình chép thẳng được.

**⚠️ VẤN ĐỀ KỸ THUẬT LỚN NHẤT — và cách xử lý.** Khối ứng viên tốn token:
| trần ứng viên | phủ tên vàng | token khối (max) | vừa ngân sách 543? |
|---|---|---|---|
| 16 | 76,2% | 492 | ✅ nhưng **trượt cổng 95%** |
| 32 | 93,2% | 656 (đã nén) | ✗ |
| **40** | **96,0%** | 1.012 | ✗ |

(Cột phủ đo trên mẫu tập dạy; trên đủ tập kiểm trần 40 cho **96,7%**.)

Ngân sách 543 token = chỗ trống dưới `cutoff_len` 2560, tính từ số đã ghi trong cấu hình: **ảnh
chiếm 1.272 token**, mẫu dài nhất của s2 là **2.017**. Vượt trần thì LLaMA-Factory **cắt từ đuôi**
— mà đuôi là **đích sinh**. Loss vẫn tính, log không báo gì.

⇒ **Đề xuất nâng `cutoff_len` 2560 → 3072**, ghi mục sửa đổi (x15) **trước khi train**.
Đã thử nén cách viết khối (bốn dạng) — dạng gọn nhất ở trần 32 vẫn tràn. Đã cân nhắc hạ độ phân
giải ảnh (`image_max_pixels` 1003520 → 602112, giải phóng ~509 token) và **loại**, vì tác vụ cần
đọc chữ nhỏ trên giao diện.

**Ba điều kiện bắt buộc kèm theo việc nâng** (nếu thiếu thì thành vi phạm thật):
1. ghi vào hồ sơ đăng ký trước **trước khi train**, không phải sau khi có điểm;
2. **cặp mới chỉ đọc nội bộ với nhau** — cấm đặt 62% của nhánh này cạnh 59,11% của S1 rồi bảo
   "hơn 3 pp"; hai bên khác điều kiện;
3. **nói thẳng trong bài** rằng nhánh này được chuỗi vào dài hơn và vì sao, cùng việc đối chứng
   cũng được y như vậy.

**⚠️ Đây là kết quả MỨC HỆ THỐNG** (thêm đầu vào). Bắt buộc: (a) train **đối chứng cùng đầu vào**
— câu-thẳng, không khai báo — và luôn trình theo cặp; (b) giữ nguyên bảng cũ không đầu vào phụ;
(c) ⛔ **CẤM chữ "đầu tiên"** — bài gốc AndroidControl (**NeurIPS 2024 D&B**) đã fine-tune với
danh sách trợ năng làm INPUT; Mind2Web (**NeurIPS 2023 D&B**) và Zheng et al. (**ICML 2024**) đã
lọc ứng viên ở tầng hành động.

**Tiền lệ hậu thuẫn:** Geng, Josifoski, Peyrard, West, **EMNLP 2023, tr. 10932–10952** — ràng buộc
vào **tập ứng viên riêng của từng đầu vào** cho AIDA **62,6 → 81,0** (so với 69,8 khi ràng buộc
vào toàn kho). Anderson, Fernando, Johnson, Gould, **EMNLP 2017, tr. 936–945** — ép lúc **giải mã**
thắng cách nhét cùng bộ nhãn vào lúc **huấn luyện**.
**Tiền lệ chống:** Schall & de Melo, **RANLP 2025, tr. 1074–1084** — ràng buộc giúp base model
nhưng **làm sụt model đã instruction-tune** ở tác vụ sinh; Qwen2.5-VL-3B thuộc vế **bị hại**.
Park et al., **NeurIPS 2024** — ràng buộc làm lệch phân bố.

**Dự báo viết trước:** nâng khai báo **+6…+12 pp** ⇒ nhân hệ số chuyển đổi **0,43** ⇒
**62,5 – 65,5% executability**.
**Giá:** ~54 h A100 (hai nhánh × 23 h + dựng + probe) + 10,8 h Kaggle, một hạt giống.

---

### ② NHÁNH-LÙI — dạy mô hình nói "không chắc"

**Ý.** Định tuyến **lúc suy luận** chết vì không có tín hiệu (Mục 5). Nhưng ở **tầng huấn luyện**
tín hiệu đã có sẵn và **đã trả tiền**: **14.000 khai báo mà chính S2 tự sinh** trên màn tập dạy
(sinh 25/8, 4,5 giờ A100), biết đúng/sai vì có nhãn vàng — **68,5% đúng tên**.

Dựng đích SFT: bước mô hình **từng sai** → `<desc>không chắc</desc>` + **câu chung chung kiểu S1**;
bước **từng đúng** → giữ khai báo vàng + câu đặc tả. Một mô hình duy nhất, **không thêm đầu vào**
⇒ **so với S1 vẫn công bằng**, không chạm oracle leak.

**Lát nhạy cảm** (lợi +22,2 pp mỗi bước bắt đúng ô D · hại −8,9 pp mỗi bước bắt nhầm ô A):

| recall ô D | FP 0% | FP 5% | FP 10% | FP 20% |
|---|---|---|---|---|
| 50% | 61,90 | 61,70 | 61,49 | 61,07 |
| **70%** | **62,64** | **62,44** | **62,23** | 61,81 |
| 90% | 63,39 | 63,18 | 62,97 | 62,55 |
| 100% | 63,76 | 63,55 | 63,34 | 62,93 |

⇒ **recall 70% với FP ≤10% đã vượt ngưỡng DƯƠNG 62,16%.**

**Rủi ro chính:** mô hình hedge tràn lan, mất +8,83 pp của ô A. Bắt bằng cổng G7 (tỉ lệ lùi trên
tập kiểm phải ∈ [15%, 45%]).
⚠️ **Thiên lệch biết trước, phải vào Limitations:** nhãn "từng sai" là hành vi của S2 trên **tập
dạy** (68,5% đúng) trong khi tập kiểm chỉ **60,6%** ⇒ mô hình sẽ **lùi ít hơn mức cần**.
**Tiền lệ:** ASPIRE, Chen J. et al., **Findings of EMNLP 2023, tr. 5190–5213** (huấn luyện mô hình
tự đánh giá để từ chối) ⇒ ⛔ **cấm chữ "đầu tiên"** cho ý *học cách từ chối*.
**Giá:** 4,7 h A100 + 5,4 h Kaggle.

---

### ③ MIX — không nhắm điểm

Trộn bước **không-chạm** dạng CE thuần vào stage-2. Lý do duy nhất: điều kiện claim (x5) mục 4
đang **TRƯỢT**. Đo trên 400 bước không-chạm: S2 **83,5%** → CE2 **63,0%** → MIN **63,8%** action_ok,
tức **−19,75 pp**, mà ngưỡng đòi cận dưới **> −3 pp** ⇒ trượt gần bảy lần. Nguyên nhân là **thiết
kế dữ liệu stage-2 chỉ có bước chạm**, không phải ORPO (CE2 và MIN trùng nhau gần tuyệt đối).
⛔ **Cấm trình MIX như một cải tiến điểm số.** Giá: 4,7 h + 5,4 h.

---

## 5. TÁM HƯỚNG ĐÃ LOẠI — kèm lý do ĐO ĐƯỢC

Người phản biện: nếu muốn lật một hướng, phải lật **con số**, không phải lật lập luận.

| # | hướng | lý do loại (số đo) |
|---|---|---|
| 1 | **định tuyến / abstention lúc suy luận** | trần **oracle 63,46%**; bảy bộ định tuyến thật cho **60,0–60,34%** — nhiễu. Độ chính xác tín hiệu 65–72% so tỉ lệ nền 60,6% ⇒ gần như không mang tin |
| 2 | **ràng buộc giải mã ô TÊN** theo chuỗi trên màn | dư địa vật lý **chỉ +1,46 pp** (ô C). Nặng hơn: ở ô D, **68,6% tên mô hình sinh ra ĐÃ là chuỗi có thật trên màn** ⇒ ràng buộc **không kích hoạt** ở phần lớn khối lỗi. **Mô hình không bịa tên — nó chọn đúng chuỗi của SAI phần tử** |
| 3 | **sửa tên có chọn lọc** rồi sinh lại câu | tầng khai báo rất đẹp (**+3,85 pp**, b=133, c=0, χ²=131) nhưng trần exec **60,01%**, vì **107/133** bước sửa được **đã trúng sẵn**. ⭐ Đây là ca hệ số chuyển đổi **dự báo sai** — nó ước trên can thiệp đổi **cả tên lẫn điểm** |
| 4 | **self-consistency k=5** trên ô `<desc>` | số duy nhất trên đầu ra **có cấu trúc** là **+0,4%** (PET-SQL, ⚠️preprint). Con số +17,9% của Wang et al. **ICLR 2023** là **k=40 trên mô hình 137B–540B**; ta là **3B**, không có trọng tài thực thi |
| 5 | **RFT / STaR** trên 14.000 rollout | RFT (⚠️preprint) đo mức tăng **teo theo độ mạnh của nền: +4,8…+6,1 pp ở nền 35,9–50,0%, −0,1 pp ở nền 54,6%**; nền của ta **68,5%** — ngoài dải nó còn tác dụng. Thêm: cơ chế RFT quy công cho *số đường suy luận phân biệt*, mà ô tên gần như chỉ có MỘT đáp án đúng; và lọc-giữ-cái-đúng đặt gradient lên đúng 68,5% mô hình **vốn đã làm đúng** |
| 6 | **copy/pointer từ OCR** | lấy mục OCR gần **điểm vàng** nhất cho tên đúng **64,9%** — **THẤP HƠN** 66,3% mô hình đang tự đạt. Copy điểm từ mục OCR khớp tên: 58,9% vs 71,8% hiện có |
| 7 | **`--ceiling gold`** làm cổng dư địa | **oracle leak đã đo**: câu chuẩn của người **chứa nguyên văn tên phần tử 53,9%** số bước ⇒ nạp khai báo vàng là mớm sẵn hơn nửa chữ khoá của câu đích |
| 8 | **`s2_nopoint` / `s2r`** | bảng bắt chéo: **toạ độ đúng một mình +1,12 pp** vs **tên đúng một mình +0,54 pp** ⇒ ô toạ độ là ô **gánh**, không phải ô gây hại. Tái lập ở ô C (411 bước đang được toạ độ cứu). `s2r` được thiết kế để chắc chắn thua |
| 9 | **rerank bằng bộ trỏ** | trọng tài trùng thước ⇒ **vòng tròn**. Dùng UI-Venus làm trọng tài thì hợp lệ nhưng tốn k × 5,4 h Kaggle |

**Và một hướng đã CHẠY rồi CHẾT (25/8):** biến thể **on-policy negative** — lấy khai báo mà chính
S2 đoán sai làm vế âm. Sinh khai báo trên 14.000 màn (4,5 h A100), dựng được **459 cặp** =
**3,3%** eligibility, ngưỡng khoá trước là **25%** ⇒ dừng.
⭐ **Lý do, và nó có giá trị khoa học riêng:** khoảng cách giữa phần tử mô hình gọi nhầm và phần tử
đích có **p25 = 70 px · trung vị = 351 · p75 = 748**; cổng 80–350 px loại **76,5%**. ⇒ **Lỗi khai
báo LƯỠNG CỰC** — hoặc cùng phần tử gọi khác tên, hoặc nhìn sang vùng khác hẳn màn — **không phải
lẫn giữa hai nút cạnh nhau**. Tiền đề của on-policy giả định một dạng lẫn **cục bộ** mà mô hình này
không mắc. Điều này cũng giải thích ngược vì sao nguồn heuristic là cách duy nhất dựng được tương
phản: nó **tạo ra** vùng nhầm-hàng-xóm mà dữ liệu thật gần như không có.

---

## 6. CỔNG CHẶN VÀ ĐIỂM QUYẾT ĐỊNH — số khoá trước khi thấy dữ liệu

| cổng | khi nào | ĐẠT | TRƯỢT ⇒ |
|---|---|---|---|
| G1 phủ | dựng xong khối ứng viên, 0 GPU | tên vàng trong khối ≥ **95%** | bỏ nhánh ① |
| G2 C3 | như trên | ứng viên khớp tên ∧ trong ±140 ≥ **75%** | bỏ nhánh ① |
| G3 rò rỉ | kiểm mù **300 mẫu** | khối **không** chứa dấu hiệu nào chỉ ra phần tử đích | bỏ nhánh ① |
| G4 độ dài | **200 mẫu dài nhất** | token ≤ `cutoff_len` | sửa cách cắt, **không** sửa cutoff sau khi đã khoá |
| G5 smoke | 20 bước, ~40 phút | `train_runtime` ~200–500 s (không ~15 s) · loss đúng dải stage | dừng |
| G6 sớm | nhánh ① ở **600 bước**, ~2 h | `gate_desc_acc` ≥ **+3,0 pp** so mốc 60,6% | **dừng, cứu ~40 h** |
| G7 dải lùi | nhánh ② trên tập kiểm | tỉ lệ lùi ∈ **[15%, 45%]** | dừng |

**Điểm quyết định:** **D1** sau ②: exec ≥ **61,5%** thì giữ · **D2** sau ①: exec ≥ **62,0%** **và**
(① − đối chứng cùng đầu vào) ≥ **+2,0 pp** — thiếu một vế là bỏ · **D3**: chọn **ĐÚNG MỘT** nhánh
để nhân hạt giống, chọn theo D1/D2 chứ không chọn sau khi ngó số.

**Cam kết trước khi thấy số:** nhánh nào chạy hạt giống thứ hai thì **báo trung bình hai hạt bất
kể ra sao** · khi báo Δ phải kèm bốn số riêng lẻ, tỉ lệ bước bất đồng (mốc null 6,4% · can thiệp
thật 24%), phân tầng độ dài câu, và **hai hạt lệch > 1,5 pp thì dừng truy nguyên nhân trước khi
đọc Δ** · **báo cả ba nhánh kể cả nhánh trượt cổng**.

---

## 7. LỊCH TRÌNH 9 TUẦN VÀ NGÂN SÁCH

| tuần | việc | A100 | Kaggle |
|---|---|---|---|
| 1 | dựng dữ liệu ba nhánh + cổng G1–G4 (0 GPU) | 0 | 0 |
| 2 | train ② + ③, một hạt giống · **D1** | 8,7 h | 5,4 h |
| 3–4 | train ① + đối chứng cùng đầu vào · cổng G6 ở 600 bước · **D2** | 54 h | 10,8 h |
| 5 | gộp ①+② nếu cả hai qua · **D3** | 23 h | 5,4 h |
| 6–8 | ⭐ **HAI HẠT GIỐNG** cho nhánh thắng **và** đối chứng của nó | 46 h | 21,6 h |
| 9 | đọc soát, viết, đệm mất máy | 0 | 0 |

| kịch bản | A100 | đơn vị Colab | Kaggle | P(≥62,16%) | P(≥65%) |
|---|---|---|---|---|---|
| ① trượt G6, ② thắng | ~50 h | ~270 | 27 h | ~50% | <10% |
| cả hai qua, gộp, nhân hạt giống | ~140 h | ~750 | 43 h | **~60%** | **~30%** |

Kaggle 30 h/tuần × 9 tuần ≈ **270 h khả dụng**, dùng tối đa 43 h ⇒ **không phải nút thắt**.
Nút thắt là **đơn vị Colab**. ⚠️ Giá đơn vị **phải tra tại thời điểm quyết, cấm nhớ**.

---

## 8. RÀNG BUỘC VẬN HÀNH (để người phản biện biết vì sao lịch trình trông chậm)

· **Colab dùng đơn vị trả trước, KHÔNG có background execution** ⇒ mất máy ảo là chuyện thường:
  **tám lần trong hai lượt S1, ~18 giờ, ~85 đơn vị**. Đồng bộ Drive mỗi 5 phút.
· ⛔ Tệp mở chế độ `"a"` ghi thẳng vào Drive **KHÔNG sống sót qua mất máy** — FUSE chưa đẩy lên
  cloud mà `ls` vẫn hiện tệp như thường. Đo thật 24/8: mất trắng 2 giờ suy luận.
· ⛔ Cắt cụt ở `cutoff_len` là **loại hỏng không có tiếng động**: cắt từ đuôi = cắt mất đích sinh,
  loss vẫn tính, log không báo gì.
· ⛔ Ô thăm dò phải xoá thư mục trước, không thì LLaMA-Factory **chạy tiếp từ checkpoint cũ**,
  nhảy qua hết rồi in `Training completed`.
· ⛔ Kaggle từng **treo 7 giờ vì log ngập** (`tqdm` in mỗi cập nhật thành một dòng).
· ⭐ **Kết quả trùng nhau tới nhiều chữ số giữa các cấu hình KHÁC nhau là dấu hiệu HỎNG**, không
  phải dấu hiệu bền vững — đã suýt đọc thành "cỡ ảnh không ảnh hưởng".
· ⭐ **Tệp thô là tài sản:** giữ `*_raw.jsonl` thì đổi luật chấm vẫn tính lại được **không gọi lại
  bộ trỏ** — đã tiết kiệm trọn một lượt 5,6 giờ.

---

## 9. ⚠️ CHỖ TÔI TỰ THẤY YẾU NHẤT — MỜI TẤN CÔNG THẲNG VÀO ĐÂY

1. **σ giữa hạt giống chỉ có 1 bậc tự do.** Toàn bộ ngưỡng 2,8 pp dựng trên **một** cặp quan sát
   (S1/101 vs S1/202). σ thật có thể gấp đôi hoặc bằng nửa. Nếu gấp đôi thì ngay cả nhánh đạt
   62,16% cũng chưa chắc đứng được.
2. **Nhánh ① đổi đầu vào ⇒ không so được với S1/Base.** Nếu người phản biện cho rằng cặp
   "xử lý vs đối chứng cùng đầu vào" **không** trả lời được câu hỏi gốc của luận văn
   (*mô-tả-trước có giúp không*), thì cả nhánh ① mất ý nghĩa dù điểm có cao.
   **Đây là đòn nguy hiểm nhất. Xin ý kiến thẳng.**
3. **Nâng `cutoff_len` sau khi đã khoá.** Tôi lập luận là hợp lệ (chưa có điểm nào, đổi cho cả hai
   nhánh, có tiền lệ 11/8). Nhưng đây vẫn là **sửa một thứ đã khoá**, và dự án đã có tiền án hai
   lần nới ngưỡng. Người phản biện có quyền cho rằng nên **để nhánh ① chết ở cổng** cho sạch.
4. **Phủ đã đo trên ĐỦ tập kiểm (96,7% / 91,2%, n=3.505)**, nhưng phía **tập dạy** mới chỉ có
   mẫu 1.074 màn (96,0% / 91,1%). Phải đo lại ở 41.099 màn dạy trước khi train — OCR đầy đủ của
   tập dạy chỉ có trên Drive. Rủi ro còn lại: phân bố app của tập dạy khác tập kiểm.
5. **Nhãn "từng sai" của nhánh ② lấy từ hành vi của S2 trên tập DẠY.** Mô hình mới xuất phát từ
   chính S2 ⇒ có thể **học thuộc** danh sách bước-nào-thì-lùi thay vì học **khi nào** nên lùi.
   Tôi chưa có phép kiểm tách bạch hai khả năng này. **Đây là lỗ hổng thật.**
6. **Lát nhạy cảm của nhánh ② giả định lợi/hại là hằng số** (+22,2 / −8,9 pp mỗi bước). Thực tế
   phụ thuộc bước nào bị bắt. Bảng đó là **ước lượng thô**, không phải phép đo.
7. **Hệ số chuyển đổi 0,43 đã có một ca dự báo SAI** (hướng #3 ở Mục 5: nó ước +3,85 pp khai báo
   thành ~+1,7 pp exec, thực tế trần là **+0,00**). Vậy dự báo 62,5–65,5% của nhánh ① đáng tin
   tới đâu?
8. **990 bước (22,2%) không có tên vàng** giữ **+3,94 pp** mà **chưa hướng nào chạm tới** — nhãn
   không đặt tên nổi phần tử. Có ai nghĩ ra cách không?
9. **Toàn bộ khâu chấm là teacher-forced trên ngữ cảnh** (history là câu người). Con số tuyệt đối
   sẽ khác trong triển khai thật. Chúng tôi khai điều này nhưng chưa đo được độ lệch.
10. **Bộ trỏ cùng họ mô hình.** UGround-V1-2B dựng trên Qwen2-VL, mô hình bị chấm là Qwen2.5-VL-3B.
    Đã đóng đòn *"bộ trỏ quen văn phong AndroidControl"* bằng cách chấm lại bằng UI-Venus-Ground-7B
    (chứng nhân S1−Base giữ 94%: +10,35 → +9,68 pp), nhưng **đòn cùng họ chưa đóng** — UI-Venus
    cũng là Qwen. Không có neo người.

---

## 10. CÂU HỎI CỤ THỂ CHO NGƯỜI PHẢN BIỆN

1. Mục 9 điểm 2 — nhánh ① đổi đầu vào có làm hỏng câu hỏi nghiên cứu gốc không?
2. Mục 9 điểm 3 — nâng `cutoff_len` là hợp lệ hay nên để nhánh chết ở cổng?
3. Mục 9 điểm 5 — có phép kiểm nào tách được "học thuộc bước" khỏi "học khi nào nên lùi"?
4. Mục 5 — có hướng nào trong tám hướng bị loại mà bạn cho là loại oan? Lật bằng số nào?
5. Mục 3 — nhìn bảng phân rã ô, bạn thấy hướng nào chúng tôi **chưa** nghĩ tới?
6. Mục 9 điểm 8 — 990 bước không có tên vàng, +3,94 pp bỏ ngỏ. Ý tưởng?
7. Ước xác suất ~60% đạt 62,16% có lạc quan quá không?

---

## 11. CITATION ĐÃ VERIFY (⚠️ = preprint, cấm trình như đã bình duyệt)

**Nền:** Li et al., *AndroidControl*, **NeurIPS 2024 D&B** · Hong et al., *ORPO*, **EMNLP 2024**.
**Ràng buộc giải mã:** Geng, Josifoski, Peyrard, West, **EMNLP 2023, tr. 10932–10952** · De Cao
et al., *GENRE*, **ICLR 2021 spotlight** · Scholak et al., *PICARD*, **EMNLP 2021, tr. 9895–9901**
· Anderson, Fernando, Johnson, Gould, **EMNLP 2017, tr. 936–945** · Hokamp & Liu, **ACL 2017,
tr. 1535–1546** · Post & Vilar, **NAACL 2018, tr. 1314–1324** · Koo, Liu, He, **COLM 2024**.
**Tác hại của ràng buộc:** Park et al., *Grammar-Aligned Decoding*, **NeurIPS 2024** · Banerjee
et al., *CRANE*, **ICML 2025, PMLR 267:2836–2857** · Schall & de Melo, **RANLP 2025, tr.
1074–1084** · Beurer-Kellner et al., *DOMINO*, **ICML 2024** · Tam et al., **EMNLP 2024 Industry,
tr. 1218–1236**.
**Self-consistency / abstention:** Wang et al., **ICLR 2023** (⚠️ +17,9% là **k=40, 137B–540B**) ·
Shi et al., *MBR-EXEC*, **EMNLP 2022, tr. 3533–3546** · Chen B. et al., *CodeT*, **ICLR 2023** ·
Kuhn, Gal, Farquhar, **ICLR 2023 Oral** · Cole et al., **EMNLP 2023, tr. 530–543** · Chen J. et
al., *ASPIRE*, **Findings EMNLP 2023, tr. 5190–5213** · Gupta et al., **ICLR 2024** · Chen L. et
al., *FrugalGPT*, **TMLR 2024** · Aggarwal et al., *AutoMix*, **NeurIPS 2024** · Lightman et al.,
**ICLR 2024**.
**Self-training:** Zelikman et al., *STaR*, **NeurIPS 2022** · Dong et al., *RAFT*, **TMLR 2023** ·
Singh et al., *ReST^EM*, **TMLR 2024** · Huang et al., **EMNLP 2023, tr. 1051–1068** · Shumailov
et al., **Nature 631:755–759** · Alemohammad et al., **ICLR 2024** · Bai et al., *DigiRL*,
**NeurIPS 2024** · Sun et al., *OS-Genesis*, **ACL 2025, tr. 5555–5579**.
**GUI / REG:** Deng et al., *Mind2Web*, **NeurIPS 2023 D&B** · Zheng, Gou, Kil, Sun, Su, **ICML
2024** · Bai et al., *UIBert*, **IJCAI 2021, tr. 1705–1712** · Wang et al., *Screen2Words*,
**UIST 2021, tr. 498–510** · Cheng et al., *SeeClick*, **ACL 2024, tr. 9313–9332** · Wu et al.,
*OS-ATLAS*, **ICLR 2025** · Xu et al., *Aguvis*, **ICML 2025** · Hu et al., *M4C*, **CVPR 2020** ·
Luo & Shakhnarovich, **CVPR 2017, tr. 7102–7111** · Yu et al., **CVPR 2017, tr. 7282–7290** ·
Andreas & Klein, **EMNLP 2016, tr. 1173–1182**.
⚠️ **Preprint:** RFT (arXiv 2308.01825) · PET-SQL (arXiv 2403.09732) · Universal Self-Consistency
(arXiv 2311.17311) · SafeGround (arXiv 2602.02419) · UI-TARS (arXiv 2501.12326) · HyperClick
(arXiv 2510.27266) · ReST (arXiv 2308.08998) · Cobbe et al. (arXiv 2110.14168).

**Ba lỗi ghi chú cũ của kho đã sửa:** Mao et al. **CVPR 2016** *không* phải bài rerank (chuỗi
"rerank" xuất hiện 0 lần trong PDF) · Screen2Words **không có Bengio** · trích Wang **ICLR 2023**
"+17,9%" mà không kèm điều kiện k=40/540B sẽ dẫn tới dự báo sai một bậc.

---

## 12. TRẢ LỜI VỀ CHO CHÚNG TÔI THẾ NÀO

Ưu tiên theo thứ tự: ① lật được một con số nào ở Mục 5 (loại oan) · ② trả lời câu 1–3 ở Mục 10
(ba đòn nguy hiểm nhất) · ③ hướng mới nhìn từ bảng phân rã ô ở Mục 3 · ④ đánh giá xác suất ~60%.
**Xin nêu rõ khi nào bạn đang suy đoán và khi nào bạn có nguồn.**
