# 119 — TRẠNG THÁI HIỆN TẠI (từ 23/8/2026 trở đi)

> **File này để làm gì:** đọc một mình file này là nắm đủ trạng thái luận văn từ phiên chốt
> 23/8 tới nay, không cần mở file nào khác. Mọi số trong đây đã đối chiếu tệp kết quả thật.
> Cần lịch sử trước 23/8 thì mở `report/109` (bản đồ) và `report/108` (sổ kê khai).
>
> **Cập nhật lần cuối: 25/8/2026.** Ngày viết ghi ở từng mục để biết cái nào mới.

---

## 0. Ba đoạn cho người mới vào

**Luận văn làm gì.** Cho một ảnh màn hình Android + mục tiêu người dùng, sinh ra **một câu
hướng dẫn tiếng Anh** cho đúng bước đó. Chấm bằng **executability**: đưa câu sinh ra cho một mô
hình định vị GUI độc lập (UGround-V1-2B), nó trỏ vào một toạ độ trên ảnh; câu được tính là chạy
được nếu loại thao tác khớp câu chuẩn **và** toạ độ rơi đúng ô Voronoi của phần tử đích. Chỉ
**câu** được chấm; mọi thứ mô hình sinh trước câu đều bị cắt bỏ. Mẫu số cố định **4.463 bước
chạm** của tập kiểm.

**Đóng góp mô hình đang theo đuổi.** Dạy mô hình **mô tả phần tử trước, phát ngôn sau**: sinh ô
khai báo `<desc>vai trò | tên | <point>x,y</point> | dấu hiệu phân biệt</desc>` rồi mới tới câu.
Nhánh S2 (SFT có khai báo) **thua** S1 (SFT trơn) −1,93 pp và đã bị dừng. Thay thế là
**MIN-DESC**: một chặng ORPO thứ hai nối tiếp từ checkpoint S2, huấn luyện trên cặp chỉ khác
nhau ở ô khai báo, để gradient rơi đúng vào việc **chọn đúng phần tử**.

**Đang ở đâu (25/8).** MIN-DESC/101 đã có điểm: **60,05%** — cao nhất trong mọi nhánh đã train,
nhưng so với SFT trơn chỉ **+0,94 pp, p=0,11**, không có ý nghĩa. Chẩn đoán đã chỉ ra chỗ nghẽn
nằm ở **độ chính xác ô khai báo**, không phải ở cơ chế. Nhánh đối chứng CE2-S2 đang được chấm.

---

## 1. Dòng thời gian 23 → 25/8

| ngày | việc | kết quả |
|---|---|---|
| 23/8 | Chủ luận văn dừng nhánh **S2/202** vì ngân sách | S2 vĩnh viễn là *thăm dò, một hạt giống* |
| 23/8 | Chốt đóng góp mô hình = **MIN-DESC** (`report/117`) | loại `s2_nopoint`, loại `s2r` |
| 23/8 | **Smoke ORPO ĐẠT** trên Colab | ~21 s/bước · LLaMA-Factory pin `c4e09c7cbe18…` |
| 23/8 | Viết lại hai bài: **FAIR = bài mô hình** (8 trang), **VCL = nhãn mô tả phần tử** (9 trang, tiếng Việt) | phản biện bốn giám khảo ở `report/118` |
| 24/8 | Train **MIN-DESC/101** rồi **CE2-S2/101** trên Colab A100 | mỗi lượt 800 update |
| 24/8 | Chẩn đoán trôi chạm/không-chạm **(x3d)** và mất no-harm **(x3e)** | điều kiện (x5) mục 4 **TRƯỢT** |
| 24/8 | Dựng biến thể **MIX** (trộn bước không-chạm) — chưa train | `build_min_desc_mix.py` |
| 24/8 | Mất máy ảo giữa lượt sinh câu CE2 (3.616/6.958) | nối tiếp thành công, xem Mục 6 |
| 25/8 | **Cổng cơ học ĐẠT** (`gate_desc_acc.py`) | S2 53,9 → CE2 59,8 → MIN 60,6 |
| 25/8 | Chấm 4.463 trên Kaggle, hai commit **song song** | một commit **chấm nhầm nhánh**, mất 5,3 h quota |
| 25/8 | **MIN-DESC/101 = 60,05%** | chẩn đoán chỗ nghẽn, xem Mục 4 |
| 25/8 | Chấm lại **CE2-S2/101** | ⏳ **đang chạy** |

---

## 2. Số hiện hành — bảng đầy đủ

Tất cả chấm bằng UGround-V1-2B trên **cùng 4.463 bước chạm**, cùng bản `metric_exec.py`
(md5 `9bf0b84145458fd55919a5e161b9766f`).

| nhánh | exec | KTC95 | action_ok | hit_disk | voronoi thuần |
|---|---|---|---|---|---|
| Câu chuẩn của người (**trần**) | **75,73%** | [74,1 · 77,3] | 100,0 | 84,3 | 75,8 |
| **MIN-DESC/101** | **60,05%** | **[58,33 · 61,77]** | **98,9** | 69,2 | **60,4** |
| S1/202 (SFT trơn) | 59,62% | — | — | — | — |
| S1/101 (SFT trơn) | 59,11% | [57,3 · 60,8] | 94,4 | 69,2 | 60,2 |
| S2/101 (SFT có khai báo) | 57,18% | [55,4 · 58,9] | 94,9 | 67,5 | 58,1 |
| Base (Qwen2.5-VL-3B gốc) | 47,59% | — | 96,5 | 57,6 | 48,9 |
| **CE2-S2/101** (đối chứng) | ⏳ đang chấm | | | | |
| sàn thước (`f1_trong`) | 12,0% | [9,7 · 14,4] | — | — | — |

### Phép so ghép cặp trên đúng 4.463 bước

| phép so | Δ pp | KTC95 (bootstrap cụm) | b | c | χ² | p |
|---|---|---|---|---|---|---|
| MIN − S2/101 | **+2,87** | [+2,03 · +3,76] | 258 | 130 | 41,6 | 1,1e-10 |
| **MIN − S1/101** | **+0,94** | **[−0,09 · +2,05]** | 342 | 300 | 2,6 | **0,11** |
| MIN − Base | +12,46 | [+11,03 · +14,00] | 827 | 271 | 280,5 | 5,7e-63 |
| S1 − S2 *(tự kiểm)* | +1,93 | [+0,82 · +3,00] | 340 | 254 | 12,2 | 0,00049 |

Hàng cuối tái lập **đúng** con số −1,93 pp của S2−S1 đã công bố, b/c trùng 340/254 ⇒ đường phân
tích không trôi giữa hai lần chạy.

### Cổng cơ học ở tầng khai báo — không gọi bộ trỏ (3.473 bước có tên vàng)

| nhánh | sinh `<desc>` | tên đúng | point đúng | **cả hai đúng** |
|---|---|---|---|---|
| S2/101 | 93,4% | 59,2% | 66,9% | **53,9%** |
| CE2-S2/101 | 99,6% | 66,2% | 71,2% | **59,8%** |
| MIN-DESC/101 | 99,6% | 67,0% | 71,8% | **60,6%** |

⇒ CE2 − S2 = **+5,90** (công của *train thêm trên bước chạm*, SFT thuần) · MIN − CE2 = **+0,80**
(phần riêng của mục tiêu ưu tiên). **87% mức tăng thuộc nhánh đối chứng.**

---

## 3. MIN-DESC là gì, tự chứa

Chặng ORPO thứ hai, nối tiếp adapter **S2** (không tạo adapter mới), 800 update, trên
**22.854 cặp** dựng bởi `harness/build_min_desc.py`:

```
chosen   = <desc>khai báo ĐÚNG</desc>  + "\n" + câu
rejected = <desc>desc_neg (SAI)</desc> + "\n" + CÂU Y HỆT
```

Hai vế **chỉ khác nhau ở ô khai báo**, câu giống hệt nhau ⇒ số hạng ưu tiên của ORPO chỉ có thể
giảm bằng cách chọn đúng phần tử, không thể giảm bằng cách đổi văn phong hay độ dài câu.

**Đối chứng quy công là CE2-S2:** SFT thuần trên đúng vế `chosen` của đúng những bước ấy, cùng
số update, cùng learning rate. Đại lượng chính đăng ký trước là
`Δ_component = mean_2seed(MIN − CE2)`.

· cấu hình: `train_config_orpo.yaml` (stage `dpo`, `pref_loss: orpo`) và `train_config_ce2.yaml`
  (stage `sft`) · runbook `harness/colab_train_min_desc.md`
· ⚠️ stage `dpo` **không** ghi `loss`/`lr` vào `trainer_log.jsonl`, stage `sft` thì có — ô theo
  dõi lọc theo `loss` sẽ vứt sạch mọi dòng ở nhánh `dpo`
· ⚠️ liger **không** kích hoạt ở stage `dpo` — cấm viết "dùng liger" cho MIN-DESC

---

## 4. ⭐ Chẩn đoán quan trọng nhất: chỗ nghẽn nằm ở đâu (25/8)

Chia 3.473 bước có tên vàng theo việc ô khai báo của **chính MIN-DESC** có đúng không
(đúng = tên khớp **và** point trong ±14% cạnh):

| nhóm | n | MIN exec | S1 exec | Δ ghép cặp | trần nhóm |
|---|---|---|---|---|---|
| MIN tả **ĐÚNG** phần tử | 2.106 (60,6%) | **87,1%** | 78,3% | **+8,83** | 86,3% |
| MIN tả **SAI** phần tử | 1.367 (39,4%) | **21,8%** | 32,9% | **−11,12** | 61,4% |

**Cơ chế KHÔNG hỏng — nó bị chặn bởi độ chính xác khai báo.** Tả đúng thì MIN-DESC hơn SFT trơn
8,83 pp và **vượt cả trần câu người của nhóm đó** (87,1 vs 86,3). Tả sai thì thua 11,12 pp: mô
hình chốt vào phần tử sai rồi viết câu tự tin về phần tử đó, còn S1 viết chung chung nên còn cơ
may. Hai chiều triệt tiêu nhau ⇒ tổng +0,94 pp không ý nghĩa.

**Trần lý thuyết của việc chặn vế âm:** nếu mỗi lần tả sai mà lùi về đúng hành vi S1 thì trên lát
3.473 được **65,79%** (thật: MIN 61,42 · S1 60,44) ⇒ **+5,36 pp so S1**, gấp 2,4 lần MDE 2,2.

**Một hướng đã loại miễn phí:** ép mô hình nhắc lại tên trong câu **không** phải đòn bẩy. Trong
nhóm tả đúng, câu có nhắc tên hơn câu không nhắc +9,12 vs +8,31 — chênh 0,8 pp và bám sát trần
từng nhóm (89,3 vs 80,9), tức khác biệt **độ khó**, không phải do nhắc tên.

⚠️ **Giới hạn phải khai:** biến chia nhóm là **hành vi của chính MIN-DESC**, hai nhóm khác hẳn
nhau về độ khó. Phép so MIN-vs-S1 **bên trong** mỗi nhóm hợp lệ vì ghép cặp trên cùng bước;
**cấm** so nhóm trên với nhóm dưới. Đây là chẩn đoán **hậu kiểm, không đăng ký trước**.

---

## 5. Cái gì được nói, cái gì cấm

**Được viết:**
· *"Ở hạt giống duy nhất, MIN-DESC/101 đạt 60,05% executability trên 4.463 bước, so với S1
  59,11/59,62% và S2/101 57,18%. Kết quả thăm dò, một hạt giống."*
· *"Trên quần thể đã đăng ký (bước chạm), …; đồng thời chúng tôi đo được mức tụt ~20 pp ở lớp
  thao tác trên bước không-chạm, do thiết kế dữ liệu stage-2, và báo cáo như một giới hạn."*

**⛔ Cấm:**
· *"MIN-DESC làm model tốt hơn"* · *"mục tiêu ưu tiên có tác dụng"* · mọi câu khẳng định về
  **phương pháp** — một hạt giống không tách được tác dụng khỏi biến thiên huấn luyện (sàn nhiễu
  đo trên S1 là ±0,52 pp).
· Nêu `action_ok` 98,9% mà **không** kèm mục (x3e): trên bước **không-chạm** `action_ok` tụt
  −19,75 pp. Hai con số là **một hiện tượng** — mô hình co về *"mọi thứ đều là chạm"*. Quần thể
  đăng ký trước chỉ có bước chạm nên thước không nhìn thấy phần thiệt.
· Trình +2,87 pp (so S2) như công của ORPO — cổng cơ học cho thấy 87% mức tăng ở tầng khai báo
  thuộc nhánh đối chứng CE2.
· `Δ_component` **chưa tính được** cho tới khi CE2 có điểm.

**Nguồn luật:** `report/106` mục (x8b) luật câu chữ · (x8c) cam kết nếu chạy hạt giống thứ hai ·
(x9) cổng cơ học · (x10) điểm và chẩn đoán.

---

## 6. Bẫy vận hành mới học 24–25/8 — mỗi cái là một lần trả giá

**① `--out` trỏ thẳng vào Google Drive KHÔNG sống sót qua mất máy.** Lượt sinh câu CE2 ghi thẳng
vào `MyDrive/thesis/preds_ce2_s2_seed101.jsonl` suốt 2 giờ; mất máy xong tệp **biến mất hoàn
toàn**. Tệp mở chế độ `"a"` chưa đóng lần nào thì FUSE chưa đẩy lên cloud, mà `ls` vẫn hiện tệp
như thường ⇒ **không có dấu hiệu nào báo trước**. Chỉ bản chụp định kỳ bằng `cp` sang **tên
khác** còn sống (3.616 dòng, cứu ~67 phút GPU).

**② mtime trên `/content/drive` không cập nhật khi ghi thêm** — tệp đang được ghi có thể hiện mốc
giờ cũ cả tiếng. Kiểm bằng `wc -l` hai lần cách nhau 60 giây, đừng đọc `ls -la`.

**③ Nhân Python bận chạy ô dài thì mọi ô khác xếp hàng** ⇒ lúc cần cứu tệp phải dùng **Terminal
Colab**. Hỏi tiến trình đang dùng đường dẫn nào bằng
`tr '\0' ' ' < /proc/$(pgrep -f infer_branch|head -1)/cmdline`, đừng đọc lại lệnh đã gõ.

**④ `peft` bản mới `raise ImportError` khi thấy `torchao` < 0.16** — chết ở đúng dòng
`PeftModel.from_pretrained`, tức **sau khi** đã tải 7,5 GB trọng số. Gỡ `torchao` là xong. Lượt
trước không dính vì LLaMA-Factory ghim `peft` bản cũ.

**⑤ Khai biến ở hai chỗ = chấm nhầm nhánh, mất 5,3 giờ quota.** Notebook Kaggle dành cho CE2 còn
dòng `TEN_COMMIT = ["min_desc_seed101"]` **bên trong ô 2**, gán đè giá trị mà ô 1 đặt. Ô tiền bay
chạy trước nên in ra `ce2` — **đúng** — rồi bị đè. Không lỗi, không cảnh báo. Phát hiện lúc giải
nén: hai tệp thô **trùng nhau từng byte**. Đã vá bằng ô tiền bay niêm phong `NHANH_CHOT` + ô 2
`assert` so với nó.

**⑥ Hai commit GPU Kaggle chạy song song ĐƯỢC** — đo thật 25/8, hai notebook riêng tách bằng
*Copy & Edit*, cả hai cùng chạy, đều nhận T4×2. Nhưng quota 30 h/tuần là quota chung nên song
song chỉ đổi **thời gian chờ**, không đổi số giờ; và lỗi cấu hình thì mất gấp đôi giờ để phát
hiện. ⚠️ Bản sao **thừa kế** biến của bản gốc ⇒ phải so dòng in nhánh của hai bên cạnh nhau.

**⑦ `assert` ở ô CUỐI notebook có thể giết cả commit.** Ô đọc kết quả chạy sau 5,4 giờ chấm; một
exception làm notebook kết thúc lỗi ⇒ Kaggle **không lưu** `/kaggle/working` ⇒ mất cả tệp thô.
Luật: **mọi ô đứng sau ô chấm phải không-thể-ném-lỗi**.

⭐ **Lợi ngoài ý muốn từ sự cố ⑤:** hai lượt chấm độc lập, hai phiên Kaggle, khác giờ, cho tệp thô
**trùng từng byte** (`md5 7ab8197edebb…`) trên **toàn bộ 4.463 bước**. Bằng chứng *thước tất định*
mạnh hơn hẳn bản cũ (0 bất đồng trên 1.625 phép so qua bốn lượt). Dùng được cho chương đo lường.

---

## 7. Hai bài báo (trạng thái 23/8, chưa đổi)

| | **FAIR'2026** | **VCL2026** |
|---|---|---|
| vai trò | **bài mô hình** | nhãn mô tả phần tử (REG trong miền GUI) |
| ngôn ngữ · hạn | tiếng Anh · **31/8**, EDAS | tiếng Việt · **30/8** |
| tệp | `paper/fair2026/main.tex` — 8 trang, 0 overfull | `paper/vcl2026/main.tex` — 9 trang, 0 overfull |
| bản dự phòng | `main_v1_metric_backup.tex` = **bản thước-đo cũ**, vẫn dùng được | — |

· Lệnh dựng: **`tectonic -X compile main.tex --outdir .`** — máy không có `xelatex`. Cấm
  `>/dev/null 2>&1` trên lệnh dựng; kiểm `ls -la main.pdf` mốc giờ trước khi tin số trang.
· Phản biện bốn giám khảo: `report/118`.
· ⚠️ CFP của VCL còn **ba thứ chưa xác minh**: giới hạn trang · mẫu định dạng · **chính sách nộp
  đồng thời** (quan trọng nhất, vì hai bài dùng chung dữ liệu và mô hình).
· ⚠️ **Quyết định đang mở:** FAIR được chuyển thành bài mô hình hôm 23/8, lúc MIN-DESC còn là ẩn
  số. Nay biết Δ so SFT trơn là +0,94 pp không ý nghĩa. Có nên quay lại bản thước-đo hay không là
  câu hỏi **chưa quyết** — đợi điểm CE2.

---

## 8. Việc đang chờ và việc kế

| | việc | trạng thái |
|---|---|---|
| 1 | Chấm **CE2-S2/101** trên 4.463 (Kaggle, 5,4 h) | ⏳ đang chạy |
| 2 | Tính `Δ_component = MIN − CE2` | chờ (1) |
| 3 | Chọn hướng cải tiến tiếp, train trên **một hạt giống** | xem Mục 9 |
| 4 | Nếu một hướng ra số tốt → mới nhân lên **hai hạt giống** | cam kết (x8c) áp dụng |
| 5 | Đọc soát + nộp hai bài | 30–31/8 |

**Chiến lược đã chốt với chủ luận văn:** dò nhiều biến thể trên **một hạt giống** trước, chọn
biến thể tốt nhất, rồi mới chi GPU cho hạt giống thứ hai. Mọi con số trong pha dò là **thăm dò**.

**Ràng buộc tài nguyên:** Kaggle **30 giờ GPU/tuần**, mỗi lượt chấm 5,4 h. Tuần này đã tiêu
~10,9 h (gồm 5,3 h chấm nhầm) + lượt CE2 đang chạy. Colab dùng **đơn vị trả trước, không có
background execution** ⇒ phải sống chung với mất máy; đồng bộ Drive mỗi 5 phút.

---

## 9. Hướng đi tiếp — ĐÃ TRANH LUẬN VÀ CHỐT 25/8

> Toàn văn lý lẽ, tiền lệ và số: **`report/120_TRANH_LUAN_HUONG_TIEP.md`**.

| hướng | phán quyết | lý do một dòng |
|---|---|---|
| Ⓐ đổi câu ở vế bị loại | ⛔ **BÁC** | thiết kế hiện tại có tiền lệ trực tiếp hơn (FRODO, Findings EMNLP 2024); ba nhóm độc lập đo được rằng cặp khác nhau **tối thiểu** học tốt hơn; Ⓐ mở cửa cho thiên vị độ dài |
| Ⓑ siết hard negative | ⛔ **BÁC** | `nearest_other()` **đã** là hard negative (100% cùng vai trò); chỉ 7–10% lỗi tên rơi vào hàng xóm gần nhất; hard quá còn phản tác dụng (FaceNet CVPR 2015 · Robinson ICLR 2021) |
| **Ⓑ′ vệ sinh cặp** | ✅ **CHỌN** | ba khuyết tật đo được, sửa bằng **0 giờ GPU** |
| Ⓒ MIX | giữ nguyên | làm để đạt điều kiện no-harm, không để tăng điểm |
| **Ⓓ negative on-policy** | ✅ **ĐÃ ĐĂNG KÝ 25/8** — `report/106` mục **(x11)** | nhắm đúng 90% khối lỗi heuristic bỏ sót. Bản ngây thơ **bị cấm** (CLAIR/TACL 2025 đo được −5,00 pp); phải **đúc lại** khai báo âm bằng chính hàm đã dựng nhãn vàng. Đại lượng chính đặt ở **tầng khai báo**, 0 quota Kaggle |

**Ⓑ′ — sau khi rút số, chỉ còn MỘT khuyết tật thật:**

| # | khuyết tật | tỉ lệ | trạng thái |
|---|---|---|---|
| ① | tách được **chỉ bằng chuỗi `(no name)`**, không cần nhìn màn hình | **17,4%** | ✅ đứng |
| ② | ~~vế âm nằm trong ô dung sai ±140~~ | ~~77,1%~~ | ⛔ **RÚT 25/8** — ±140 là luật **đĩa**, thước chính là **Voronoi**; dưới Voronoi mọi cặp đều phân biệt được. `report/120` Mục 3b |
| ③ | ~~ô dấu hiệu trùng hệt hai vế~~ | ~~13,1%~~ | ⛔ bỏ — không phải khuyết tật, tên và toạ độ vẫn khác |

⇒ **Ⓑ′ teo lại thành một thay đổi nhỏ:** bỏ 17,4% cặp có lối tắt `(no name)`, còn **18.872 cặp**.
Đáng làm (miễn phí, và là **lần thứ hai** dự án mắc mẫu hình lối-tắt-ở-ô-phụ, xem `report/106` mục
sửa đổi (l) ngày 9/8), nhưng **không đủ lớn để một mình biện minh cho một lượt train**.

⚠️ **SỐ HỌC PHẢI BIẾT TRƯỚC KHI CHI GPU:** hệ số chuyển đổi *khai báo → executability* đo được
trên chính dữ liệu này là **0,43** (MIN−S2: +6,70 pp khai báo → +2,87 pp exec), rơi đúng dải văn
liệu 0,3–0,6. Phần quy cho ORPO đối cực là **+0,80 pp** ở ô khai báo ⇒ dự báo **≈ +0,35 pp**
executability, **kém MDE 2,2 pp sáu lần**. Kể cả Ⓑ′ làm tốt, hiệu ứng thành phần nhiều khả năng
vẫn dưới ngưỡng phát hiện.

⛔ **ĐỪNG chạy `--ceiling gold` làm cổng dư địa.** Câu chuẩn của người **chứa nguyên văn tên phần
tử 53,9%** số bước ⇒ nạp `<desc>` vàng là mớm sẵn hơn nửa chữ khoá của câu đích, trần đo được sẽ
là số ảo. Đúng cái bẫy làm ba bài oracle trong image captioning bị vô nghĩa.

**Thứ tự việc — QUYẾT ĐỊNH LỚN ĐANG CHỜ SỐ CE2:**
1. chờ điểm **CE2-S2/101** (đang chạy) → biến dự báo +0,35 pp thành **phép đo** `Δ_component`
2. **rồi mới chọn giữa hai đường**, vì sau khi rút ② thì không còn cần gạt nào hứa hẹn vượt MDE
   2,2 pp bằng cách vá dữ liệu:
   · **đường mô hình** — negative **on-policy** (Ⓓ): dùng khai báo mà chính S2 đoán SAI trên màn
     tập dạy làm `desc_neg`. Đây là cần gạt duy nhất nhắm vào **90% khối lỗi** mà heuristic hàng
     xóm bỏ sót. Giá: ~5 h suy luận dựng dữ liệu + ~8 h train + 10,8 h chấm.
   · **đường đo lường** — dừng tối ưu mô hình, lấy **chẩn đoán** làm đóng góp: bảng 2×2 mức-từng-mẫu
     (không tiền lệ nào có), hệ số chuyển đổi 0,43 đo được, kết quả âm đăng ký trước của S2, và
     giới hạn listener-metric có tiền lệ CVPR 2017. Giá: **0 GPU**.
3. dù chọn đường nào, gộp sẵn bản vá `(no name)` vào lượt train kế — nó miễn phí.

⭐ **Thứ ta đang có mà tiền lệ KHÔNG có:** không bài nào trong cả ba lượt tra đo tương quan
bước-trung-gian ↔ đầu-ra ở **mức từng mẫu**; tất cả đều ở mức hệ thống. Bảng 2×2 của Mục 4 mạnh
hơn phần lớn tiền lệ ⇒ đó là chỗ có thể thành đóng góp thật, kể cả khi `Δ_component` không vượt
ngưỡng.

⚠️ **Thước của ta là listener metric, và có tiền lệ bình duyệt cho việc nó KHÔNG đơn điệu với chất
lượng thật:** Luo & Shakhnarovich, **CVPR 2017** — listener nhảy +17,2 pp chỉ mua được +4 pp ở
người, và trên RefCOCO+ quan hệ **đảo chiều**. Đưa vào Limitations của FAIR.

## 10. Tra file nào

| cần biết | mở |
|---|---|
| **trạng thái hiện tại** | **file này** |
| estimand, ngưỡng, mọi mục sửa đổi có đánh dấu | `report/106_DANG_KY_TRUOC.md` — mục (x1)…(x10) |
| vì sao chốt MIN-DESC, vì sao loại `s2_nopoint`/`s2r` | `report/117_QUYET_DINH_MIN_DESC.md` |
| phản biện bốn giám khảo cho hai bài | `report/118_PHAN_BIEN_HAI_BAI_23_8.md` |
| bản chép phiên debate 23/8 (nền tự chứa, 27 ảnh) | `report/116_DEBATE_23_8_FINAL_SOLUTION.md` |
| cơ chế kỹ thuật toàn dự án | `report/112_HIEU_TOAN_BO_KY_THUAT.md` |
| số đã đo trước 23/8, số đã rút | `report/108_DA_LAM_DUOC_GI.md` |
| runbook train MIN-DESC/CE2 (ô T1…T14) | `harness/colab_train_min_desc.md` |
| runbook chấm Kaggle (ô 0, 1, 1b, 2, 3, 4) | `harness/kaggle_cham_min_desc.md` |
| luật vận hành, bẫy đã trả giá | `CLAUDE.md` |

**Mâu thuẫn thì:** mã thắng về *hệ thống đang làm gì* · `106` thắng về *estimand và ngưỡng* ·
**file này thắng về *trạng thái hiện tại*** · `117` về *vì sao chọn MIN-DESC*.
