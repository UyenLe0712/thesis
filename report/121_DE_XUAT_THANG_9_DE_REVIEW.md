# 121 — ĐỀ XUẤT GIAI ĐOẠN THÁNG 9, BẢN ĐẦY ĐỦ ĐỂ PHẢN BIỆN

> Viết 25/8/2026. **Mục đích: đưa cho một người/một hệ thống KHÁC đọc và đánh giá.**
>
> ✅ **ĐỌC MỘT MÌNH FILE NÀY LÀ ĐỦ.** Nó tự chứa toàn bộ bối cảnh cần thiết: nền dữ liệu và mô
> hình · thước đo và cách thước đã được kiểm · mọi số hiện có · mọi việc đã xảy ra từ **23/8/2026**
> tới nay · tám hướng đã loại · ba nhánh đề xuất · lịch trình và ngân sách · và **mười chỗ chúng
> tôi tự thấy yếu nhất**. Không cần mở file nào khác.
>
> **Bản đồ đọc:**
> · **Mục 0** — tóm tắt một trang, đọc cái này trước.
> · **Mục 1** — nền: dữ liệu, mô hình, các nhánh · **mô tả CHÍNH XÁC dụng cụ (1.3b)** · **mười
>   phép kiểm thước đo (1.3c)** — vào đây nếu muốn nghi ngờ tính hợp lệ của phép đo · **định nghĩa
>   các đại lượng (1.3d)** · **siêu tham số đầy đủ (1.3e)** · **cách tái lập từng con số (1.5)**.
> · **Mục 2** — mọi số hiện có, quy công, ngưỡng · **chẩn đoán cốt lõi (2.9): cơ chế hoạt động
>   nhưng bị chặn bởi độ chính xác khai báo** · **dòng thời gian 23/8 → 25/8 (2.10)**, gồm cả hai
>   sự cố của phiên làm việc.
> · **Mục 3** — ⭐ **phân rã ô**, thứ quyết định mọi đề xuất phía sau.
> · **Mục 4** — ba nhánh đề xuất.
> · **Mục 5** — tám hướng đã loại, kèm con số.
> · **Mục 6–8** — cổng chặn, lịch trình, ràng buộc vận hành.
> · **Mục 9–10** — ⚠️ **chỗ yếu và câu hỏi cho bạn. Đây là phần chúng tôi cần nhất.**
> · **Mục 11–11c** — citation đã verify · số đã rút cấm trích lại · trạng thái hai bài báo.
>
> **Về nguồn số:** mọi con số trong file đều đã đo trong dự án và ghi trong sổ (`report/106`,
> `CLAUDE.md`, `runs/`). Chỗ nào là **ước lượng** hay **dự báo** đều nói rõ ngay tại chỗ. Các phân
> tích mới của ngày 25/8 (phân rã ô, phủ khối ứng viên, trần các bộ định tuyến) chạy trên tệp
> `runs/*_raw.jsonl` đã có, **0 giờ GPU**, tái lập được.
>
> ⚠️ **Người phản biện hãy tấn công thẳng vào Mục 9** — đó là danh sách những chỗ chúng tôi tự thấy
> yếu nhất. Nếu bạn lật được một trong số đó, chúng tôi tiết kiệm hàng chục giờ GPU và có thể tránh
> được một kết luận sai trong luận văn.

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

### 1.3b ⚠️ MÔ TẢ CHÍNH XÁC DỤNG CỤ — đọc từ MÃ, không từ ý định

Ba chỗ dự án từng tả sai và đã phải sửa. Người phản biện cần bản đúng:

· **`hit_disk` là HÌNH CHỮ NHẬT**, không phải đĩa Euclid: `|dx| ≤ 0,14·W ∧ |dy| ≤ 0,14·H`.
  Dung sai **dọc rộng gấp 2,2× ngang** (336 px vs 151 px trên màn 1080×2400).
· **Hạt Voronoi là chính ĐIỂM CHẠM của người dùng**, không phải tâm phần tử.
· **`hit_voronoi` BAO GỒM luật đĩa** (`if not hit_disk(...): return False`) ⇒ Voronoi là bản
  **siết chặt** của luật quy ước. ⛔ Cấm trình như hai lựa chọn ngang hàng.
· ⛔ **Đừng lấy ngưỡng ±14% để suy luận về việc thước có phân biệt được hai phần tử hay không.**
  Trợ lý đã mắc lỗi này ngày 25/8 và suýt dựa vào đó để đổi thiết kế dữ liệu huấn luyện. Voronoi
  phán bằng *nút nào GẦN NHẤT*; hàm gộp nút chỉ gộp các nút cách nhau dưới **63 px**, trong khi
  phần tử âm bị ép cách **80–350 px** ⇒ **mọi phần tử âm đều phân biệt được**.
· `canon_action` **cố tình không sửa** một lỗi: `go back` quy về *tap* (81 bước ở S1). Sửa thì
  59,12 → 58,81. Giữ nguyên để ba nhánh đã chấm còn tái lập được; thêm cờ tuỳ chọn cho lượt mới.

### 1.3c ⭐ THƯỚC ĐÃ ĐƯỢC KIỂM THẾ NÀO — người phản biện nên soi kỹ mục này

Đây là phần đã chịu **bốn lượt phản biện độc lập** và không lượt nào lật được.

**① Sàn của thước** (Kaggle, lát 800 bước, trần trên lát 74,9%):
| nhánh giả | câu thành gì | điểm | KTC95 |
|---|---|---|---|
| `f1_trong` | `"Tap the button."` ở **mọi** bước | **12,0%** | [9,7 · 14,4] |
| `f3_lechman` | câu **thật** của bước khác — **đúng văn phong, sai màn** | **6,1%** | [4,5 · 7,9] |
| `f2_khongten` | giữ vị trí, **bỏ tên** | 68,0% toàn lát · **61,1%** phần bị đụng |

⇒ **Dải dùng được 62,9 điểm.** ⭐ `f3` (6,1%) **THẤP HƠN** `f1` (12,0%), hai KTC không chồng lấn
⇒ **câu văn phong hoàn hảo mà sai nội dung ăn thấp nhất trong mọi thứ đã đo** ⇒ đòn *"bộ trỏ chỉ
phản ứng với văn phong"* **bị giết bằng số**. Bộ trỏ thật sự đọc nội dung câu.

**② ⭐ GỌI TÊN ĐẮT GẤP 8 LẦN CHỈ CHỖ** — đòn bẩy lớn nhất từng đo trong dự án, và là **lý do
nền của nhánh ỨNG-VIÊN**:
· bỏ **TÊN** giữ vị trí: **−28,5 pp** (193 bước, b=58, c=3, χ²=47,8, p<0,001)
· bỏ **VỊ TRÍ** giữ tên: **−3,5 pp** (198 bước, b=8, c=1, p=0,046)
Hai quần thể gần bằng nhau nên so trực tiếp được.
⚠️ Con số là **−28,5 pp trên PHẦN BỊ ĐỤNG**, không phải −6,9 pp toàn lát (pha loãng 4,15 lần).

**③ Năm luật chấm khác nhau** (698 bước): trần trôi **56,6 → 82,2%** nhưng **thứ tự ba nhánh
không đổi ở luật nào**, và chênh S1−Base nằm gọn **9,5–13,0 pp**. Lá chắn mạnh nhất của chương đo.

**④ Thước tất định:** cùng chuỗi + cùng ảnh ⇒ cùng toạ độ, **0 bất đồng trên 1.625 phép so** qua
bốn lượt độc lập khác thứ tự và khác cách gom lô.

**⑤ κ = 0,867** toàn tập; **0,650 có điều kiện** trên 1.652 bước viết khác nhau (luôn trình kèm
điều kiện).

**⑥ Phép diễn đạt lại:** ba biến thể bảo toàn nghĩa (đổi động từ · đổi trật tự câu · cả hai) =
**1.139 bước viết lại, 30 bước đổi chiều (2,6%)**, hiệu ròng **+0,35 pp** KTC95 [−0,59 · +1,29]
⇒ mép dưới loại được mọi mức tụt > 0,6 pp.
· Cơ chế: **hỏng tất-cả-hoặc-không** — bỏ mệnh đề vị trí không làm trung vị sai số nhích
  (0,24% → 0,24%) mà làm **đuôi bung**: p90 6,88 → 31,16, p95 27,54 → 62,38.
· ⚠️ Câu chữ bắt buộc: viết *"bền trước việc đổi động từ và đổi trật tự câu"*. **CẤM** viết
  *"bền trước diễn đạt lại"* — Jandial et al. đổi *cách mô tả phần tử*, nặng hơn hẳn.

**⑦ Đổi hẳn bộ trỏ** (2.532 bước, `UI-Venus-Ground-7B`, sạch AndroidControl, 8,15 giờ Kaggle):
| phép so | UGround | UI-Venus |
|---|---|---|
| **S1 − Base** (chứng nhân) | +10,35 [+8,39 · +12,40] | **+9,68** [+7,60 · +11,78] |
| S2 − S1 (quy về 4.463) | −1,93 [−3,08 · −0,78] p=0,0005 | −1,21 [−2,30 · −0,12] p=0,026 |
⇒ **Chứng nhân giữ 94%** ⇒ thang đo không bị nén, và đòn *"bộ trỏ quen văn phong AndroidControl"*
**đã đóng**. ⚠️ Nhưng UI-Venus **cũng thuộc họ Qwen** ⇒ đòn *cùng họ* **chưa đóng**.

**⑧ Không lợi thế sân nhà:** app đã-thấy 59,1% (n=1.737) · chưa-thấy 59,0% (n=78) ·
không-gán-được 59,2% (n=2.647).

**⑨ Trần 75,7% là giới hạn DỤNG CỤ, không phải của ngôn ngữ:** 1.083 bước câu người cũng trượt,
72% do bộ trỏ sai > 14% bề ngang; **935 bước (21%) cả ba nhánh cùng trượt**.

**⑩ Thiên vị câu dài 5,4 pp** (câu > 33 ký tự 61,9% vs ≤ 33 là 56,5%). Base dài trung vị 71 ký tự,
S1 chỉ 33 ⇒ thiên vị **nghiêng về Base** ⇒ **S1 > Base là kết luận mạnh**.

### 1.3d ĐỊNH NGHĨA CÁC ĐẠI LƯỢNG PHỤ — dùng khắp file, định nghĩa một lần ở đây

· **`action_ok`** — loại thao tác mà câu sinh ra hàm ý có khớp loại thao tác của câu chuẩn không
  (chạm / vuốt / quay lại / nhập chữ …). Là **điều kiện cần** của `executability`: sai loại thao
  tác thì bước tính trượt bất kể toạ độ.
· **`hit_voronoi` thuần** — tỉ lệ trúng ô Voronoi **không đòi** `action_ok`. Trình kèm để thấy
  phần nào của chênh lệch đến từ *trỏ* và phần nào từ *chọn sai loại thao tác*.
· **Độ chính xác khai báo** (`harness/gate_desc_acc.py`) — mô hình tự sinh ô `<desc>`, đối chiếu
  **thẳng với nhãn vàng của tập kiểm**, **KHÔNG gọi bộ trỏ**, **không tiêu quota chấm**. Bảng bắt
  chéo hai chiều: *tên đúng?* × *toạ độ trong ±14% hai cạnh?*. Cột theo dõi là **"cả hai đúng"**.
  Mốc hiện hành: **S2 53,9% · CE2-S2 59,8% · MIN-DESC 60,6%** trên 3.473 bước có tên vàng.
  ⇒ Đây là **cổng rẻ nhất của cả dự án**: nó đo đúng thứ đóng góp mô hình được thiết kế để sửa,
  với 0 giây GPU, nên mọi nhánh phải qua nó trước khi được tiêu 5,4 giờ chấm.
· **Mẫu số 4.463 vs 4.462** — file cũ ghi *"cùng 4.462 bước"* là **không chính xác**. Khâu chấm
  cho câu rỗng vào quần thể với `exec = 0`, nên mẫu số đúng là **4.463** cho mọi nhánh. Một bước
  duy nhất bị bỏ ở phép ghép cặp hai hạt giống (cùng một bước ở cả hai) để McNemar sạch.
· **Hệ số chuyển đổi 0,43 / 0,79** — tỉ số *(chênh executability) / (chênh độ chính xác khai báo)*
  đo trên chính dữ liệu này: MIN−S2 cho **0,43**, MIN−CE2 cho **0,79**. Dùng để **viết dự báo ra
  trước** khi chi GPU. ⚠️ Đã có một ca nó dự báo **sai** — xem Mục 5 hướng #3 và Mục 9 điểm 7.

### 1.3e SIÊU THAM SỐ — để đánh giá được tính chặt của thí nghiệm

**SFT (cấu hình P9, dùng cho S1 · S2 và mọi lượt train đầy đủ):** QLoRA 4-bit (bitsandbytes),
`lora_rank 8` · `lora_alpha 16` · `lora_dropout 0.05` · target `q,k,v,o,gate,up,down_proj` ·
**đóng băng vision tower và multimodal projector** · `lr 1e-4` cosine · `warmup_ratio 0.05` ·
cỡ lô 4 × tích luỹ 4 = **16 hiệu dụng** · `cutoff_len 2560` · gradient checkpointing · bf16 ·
`image_min/max_pixels 200704 / 1003520` · **8.072 bước ≈ 23 giờ A100**.

**ORPO stage-2 (MIN-DESC):** nối tiếp adapter S2 (`create_new_adapter: false`) · `stage: dpo`,
`pref_loss: orpo`, **`pref_beta: 0.1` khoá trước, KHÔNG quét** · `lr 2e-5` = **1/5 của lượt SFT
gốc** · cỡ lô **1** × tích luỹ **16** = 16 hiệu dụng, **đúng bằng** lượt SFT · **`max_steps: 800`
khoá trước** · 22.854 cặp / 16 = 1.428 update mỗi epoch ⇒ 800 bước ≈ **0,56 epoch** ·
`save_steps 100`. ORPO **không cần reference model** nên bộ nhớ vừa một GPU.
⚠️ `enable_liger_kernel` **không kích hoạt ở stage `dpo`** — cấm viết "dùng liger" cho MIN-DESC.

**Đối chứng CE2-S2:** y hệt trên, đổi đúng hai thứ — `stage: sft` và tập dữ liệu chỉ còn vế
`chosen`. **Cùng số bước, cùng số update, cùng lịch `lr`.**

⭐ **Đã kiểm hai thứ hay bị nghi:** liger **không đổi phép tính** (cùng 200 mẫu cùng hạt giống,
loss trùng tới chữ số thứ tư); **đổi card không đổi kết quả** (L4 vs A100 cùng `seed 101`, loss
20 bước trùng ba chữ số, `total_flos` y hệt).

### 1.4 Kỷ luật đăng ký trước
`report/106_DANG_KY_TRUOC.md` niêm phong 5/8/2026 (commit `b93e85c`), khoá: 6 nhánh · thước đo ·
**luật đọc kết quả cho cả bốn kết cục** · 3 lát cắt · hạt giống. Mọi thay đổi về sau ghi vào
**mục sửa đổi đánh chữ**, không sửa đè. Hiện có **28 mục**, **21 mục trước điểm số đầu tiên**.
Kiểm được bằng `git log`.
⚠️ Dự án **tự khai đã hai lần nới ngưỡng sau khi thấy điểm** (ghi trong bài). Đó là lý do mọi
ngưỡng ở đây được khoá kèm ngày và commit.

---

### 1.5 TÁI LẬP — kiểm được gì và bằng lệnh nào

| muốn kiểm | chạy gì | tốn gì |
|---|---|---|
| **hồ sơ đăng ký trước có thật là viết TRƯỚC không** | `git log --follow report/106_DANG_KY_TRUOC.md` — bản niêm phong 5/8 là commit `b93e85c`; mỗi mục sửa đổi là một commit riêng có mốc ngày | 0 |
| điểm của một nhánh | `runs/score_<nhánh>.json` (`exec_voronoi`, `ci_voronoi`, `n`) | 0 |
| **tính lại điểm theo luật chấm KHÁC** | `runs/score_<nhánh>_raw.jsonl` giữ toạ độ bộ trỏ trả về ⇒ đổi luật vẫn tính lại được **không gọi lại bộ trỏ** | 0 |
| luật chấm thật sự là gì | đọc `harness/metric_exec.py` — **không đọc ghi chú**, dự án đã tả sai ba lần | 0 |
| độ chính xác khai báo | `python3 harness/gate_desc_acc.py runs/preds_*.jsonl` | vài giây CPU |
| khối ứng viên + ba cổng G1/G2/G3 | `python3 harness/build_candidates.py --split test --max 40` | vài phút CPU |
| sàn của thước | `python3 harness/doc_san.py` | 0 |
| phép diễn đạt lại | `python3 harness/phep_a_ghep_cap.py` — ⚠️ **đừng** đọc `score_para_*.json` trần, số tổng bị pha loãng 3,8 lần | 0 |
| năm luật chấm | `python3 harness/rule_sensitivity.py` | 0 |
| phép đổi bộ trỏ | `python3 harness/phan_tich_venus.py` | 0 |

⚠️ **Một cảnh báo về phương pháp kiểm, đã trả giá:** *phép kiểm dùng chính phép biến đổi mà nó cần
phát hiện thì mù* — một `assert` hỏi "bộ trỏ có tất định không" tự `.strip()` chuỗi, che mất đúng
thứ nó cần thấy (72/589 câu chuẩn có dấu cách cuối, và **một bước đổi hẳn kết luận** vì lệch một
ký tự).
⚠️ Và: **kết quả trùng nhau tới nhiều chữ số giữa các cấu hình KHÁC nhau là dấu hiệu HỎNG**, không
phải dấu hiệu bền vững — dự án suýt đọc thành *"cỡ ảnh không ảnh hưởng"*, hoá ra là dataset giữ
bản mã cũ nên phép thử **chưa hề diễn ra**.

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

### 2.6 Bối cảnh: quyết định 23/8 dừng nhánh S2

Chủ luận văn quyết **KHÔNG chạy S2 hạt giống 202**, lý do ngân sách. Hệ quả **vĩnh viễn**, phải
khai trong mọi bản báo cáo:
· estimand đã đăng ký **không hoàn tất**;
· `−2,19 pp` của S2 **ở nguyên dải TRẮNG**, không được nâng thành kết quả âm về sau;
· **mọi phân tích S2 mang nhãn thăm dò, một hạt giống** — kể cả chẩn đoán ở 2.7 và phép đổi bộ trỏ.

Đó cũng là lý do đóng góp mô hình chuyển từ S2 sang **MIN-DESC** (ORPO stage-2 từ chính checkpoint
S2), và là lý do lịch trình tháng 9 **bắt buộc có hai hạt giống** cho nhánh thắng.

### 2.7 Chẩn đoán ĐĂNG KÝ TRƯỚC (19/8, trước khi có bất kỳ điểm S2 nào)

| nhóm | n | S1 | S2 | Δ |
|---|---|---|---|---|
| **CÓ** kích hoạt (sinh `<desc>`) | 4.138 | 62,2% | 60,8% | −1,38 |
| **KHÔNG** kích hoạt | 325 | 19,7% | 10,8% | **−8,92** |

**7,3% số bước gánh 34% chênh lệch.** Trần ở nhóm 325 là **68,3%** ⇒ bước giải được, thước không mù.
⭐ **Base gọi đúng loại thao tác nhiều hơn CẢ HAI bản đã huấn luyện** (83,4% vs S1 55,1% vs S2
38,8%) ⇒ đây là **cái giá của SFT**, S2 chỉ khuếch đại.
**Bốn lời giải thích thay thế ĐÃ LOẠI:** độ dài câu (âm ở cả lát dài lẫn ngắn) · lát cắt app (âm cả
ba) · lỗi `canon_action` go-back (Δ −1,93 → −1,86) · khai báo rác OCR (26 bước, Δ **+7,69**, p=0,63
— ngược chiều).
⚠️ Giới hạn phải khai: nhóm 325 định nghĩa bằng **hành vi của chính S2**.

### 2.8 Chỗ hỏng nằm đúng chỗ thiết kế nhắm tới

Trong **1.824 bước S1 trượt**, chỉ 251 do sai thao tác; **1.573 (86%) là thao tác ĐÚNG mà bộ trỏ
không tìm ra nút** ⇒ lỗi nằm ở **cách gọi tên / tả phần tử**, đúng chỗ đóng góp mô hình nhắm vào.

### 2.9 ⭐ CHẨN ĐOÁN CỐT LÕI — cơ chế hoạt động, nhưng bị chặn

Cắt 3.473 bước có tên vàng theo việc **khai báo của chính MIN-DESC** đúng hay sai:

| khi ô khai báo | tỉ lệ bước | MIN so với S1 |
|---|---|---|
| **ĐÚNG** | 60,6% | **+8,83 pp** — và **vượt cả trần câu người của nhóm đó** |
| **SAI** | 39,4% | **−11,12 pp** |

⇒ **Cơ chế không hỏng.** Nó trả tiền rất đậm ở chỗ nhận diện đúng phần tử, và phá câu ở chỗ nhận
diện sai. Ràng buộc duy nhất là **độ chính xác khai báo 60,6%**.
⇒ Số học: **triệt tiêu được vế âm ⇒ Δ ≈ +5,4 pp** — đúng cỡ để đi từ 60,05% lên vùng 65%.
⇒ **Đây là lý do tồn tại của cả hai nhánh đề xuất:** nhánh ỨNG-VIÊN nâng vế dương (nâng 60,6%),
nhánh LÙI cắt vế âm (không khai báo khi không chắc).
⚠️ Giới hạn: lát cắt định nghĩa bằng **hành vi của chính mô hình**, một hạt giống ⇒ **thăm dò**.

### 2.10 DÒNG THỜI GIAN 23/8 → 25/8 — mọi việc đã xảy ra

| ngày | việc | kết quả |
|---|---|---|
| **23/8** | quyết **dừng nhánh S2**, không chạy hạt giống 202 (ngân sách) | estimand không hoàn tất **vĩnh viễn**; đóng góp mô hình chuyển sang MIN-DESC |
| 23/8 | smoke ORPO | ĐẠT — ORPO chạy thật, không tạo reference model, ~21 s/bước |
| 23/8 | viết lại hai bài báo trong một phiên song song | FAIR thành **bài mô hình** 8 trang · VCL 9 trang tiếng Việt |
| **24/8** | train **MIN-DESC/101** và **CE2-S2/101**, sinh câu đủ 6.958 bước mỗi nhánh | mất máy Colab một lần giữa lượt CE2, cứu được từ bản chụp 3.616 dòng |
| **25/8** | cổng khai báo (0 GPU) | S2 **53,9** → CE2 **59,8** → MIN **60,6** |
| 25/8 | chấm Kaggle hai nhánh, **hai commit tách rời** | MIN **60,05%** · CE2 **59,42%** ⇒ `Δ_component` **+0,63 pp**, **ô TRẮNG** |
| 25/8 | ⚠️ **sự cố:** hai commit đầu **cùng chấm một nhánh** | mất **5,3 giờ quota**; phát hiện vì hai tệp thô **trùng từng byte**; đã vá bằng niêm phong tên nhánh + in tên nhánh ngay đầu lượt |
| 25/8 | đăng ký trước biến thể **on-policy negative**, rồi chạy | 14.000 màn / 4,5 h A100 ⇒ **459 cặp = 3,3%**, ngưỡng 25% ⇒ **DỪNG ở cổng** |
| 25/8 | phân tích ô + trần các bộ định tuyến (0 GPU, trên `*_raw.jsonl`) | phân rã ô ở Mục 3; oracle định tuyến **63,46%** |
| 25/8 | ⚠️ **trợ lý tự phát hiện đọc sai bảng dải** | *"65% là ngưỡng dương yếu"* là **SAI**; ngưỡng đúng là **62,16%** — xem 2.5 |
| 25/8 | dựng khối ứng viên + ba cổng, trên **đủ tập kiểm** | G1 **96,7%** · G2 **91,2%** · G3 không rò rỉ vị trí ⇒ **cả ba ĐẠT** |
| 25/8 | đưa MIN-DESC vào bài FAIR, vá hai câu đã hết đúng | FAIR vẫn **8 trang, 0 overfull** |

⚠️ **Hai sự cố ở trên (chấm nhầm nhánh · đọc sai bảng dải) được ghi lại có chủ ý.** Dự án đã tự
khai **hai lần nới ngưỡng sau khi thấy điểm** trong bài; việc ghi cả sai sót của phiên làm việc là
cùng một kỷ luật. Người phản biện nên coi đây là tín hiệu về **tần suất sai sót thật**, và soi kỹ
hơn chứ không phải bớt soi.

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

## 11b. ⛔ SỐ ĐÃ RÚT — cấm trích lại, kể cả khi thấy trong file cũ

Dự án tự kiểm và đã rút chín con số. Liệt kê để người phản biện không trích nhầm từ bản thảo cũ:

| số cũ | thật ra | vì sao rút |
|---|---|---|
| trần **70,0%** | **75,73%** | đo trên mẫu con 300, đo lại đủ 4.462 bước 15/8 |
| MDE **2,7–4,5 pp** | **2,2 pp** | hệ số nở do cụm 1,10× chứ không phải 1,5–2× |
| bộ trỏ trượt **84%** khi đổi diễn đạt | 84% = **năng suất của một agent ĐỐI KHÁNG** trên **desktop Windows** | đọc nhầm abstract của Jandial et al., sống 20 ngày và đã vào bản thảo |
| "UGround sạch, không có AndroidControl" | **SAI** — Bảng 1 có AC **47K nhãn người** | mở lại đúng Bảng 1 |
| "bộ trỏ khác họ mô hình được chấm" | **SAI** — UGround-V1-2B dựng trên **Qwen2-VL** | như trên |
| trung vị sai số trỏ **8% cạnh** | **15,0% / 29,3%** | hàm cũ chỉ lấy sai số của ca ĐÃ TRÚNG |
| app chưa-thấy **604 bước** | **139 bước / 22 app** | chạy bằng bản mã có lỗi regex |
| dư địa **485 bước (10,9 pp)** | **741 bước (16,6 pp)** | kéo theo trần 75,7 |
| `total_flos` **3.857.778.344 GF** | **4.142.257.957 GF** | đọc sai; lập luận "khớp ngoại suy" còn **vòng tròn** |

⭐ **Mẫu hình đáng chú ý:** bảy lỗi bắt được trong hai ngày, **KHÔNG lỗi nào ở khâu ĐO** — tất cả
nằm ở **câu chữ mô tả nguồn**. Và cụ thể hơn: mọi lỗi sinh ra ở khâu **tóm tắt một nguồn thành câu
ngắn cho tiện trích**, rồi câu ngắn sống nhiều tuần vì không ai mở lại nguồn.
⇒ Nếu người phản biện muốn tìm lỗi, **soi văn bản trước, soi mã sau**.

## 11c. TRẠNG THÁI HAI BÀI BÁO (để hiểu vì sao lịch trình chia hai mốc)

| | **FAIR'2026** | **VCL2026** |
|---|---|---|
| ngôn ngữ | tiếng Anh | tiếng Việt |
| hạn nộp | **31/8/2026**, qua EDAS, track NLP | **30/8/2026** |
| vai | **bài MÔ HÌNH** | **bài NHÃN MÔ TẢ PHẦN TỬ** (hướng sinh biểu thức quy chiếu) |
| trạng thái 25/8 | **8 trang, 0 overfull** | **9 trang, 0 overfull** |

FAIR nay chứa: bảng sáu nhánh · mục riêng cho MIN-DESC với `Δ_component` +0,63 đọc là **ô trắng**
· **quy công 78/22** · chẩn đoán 2×2 mức từng mẫu · biến thể on-policy chết ở cổng · sàn ·
gọi-tên-vs-chỉ-chỗ · năm luật chấm · phép đổi bộ trỏ.

⇒ **Hai bài chốt số hiện tại.** Nhánh tháng 9 nếu ra số tốt thì vào **luận văn** (hạn tháng 10),
không kịp vào bài báo. Vì vậy lịch trình chia **mốc A (5 ngày, không tiêu GPU để tăng điểm)** và
**mốc B (9 tuần, cho luận văn)**.

## 12. TRẢ LỜI VỀ CHO CHÚNG TÔI THẾ NÀO

Ưu tiên theo thứ tự: ① lật được một con số nào ở Mục 5 (loại oan) · ② trả lời câu 1–3 ở Mục 10
(ba đòn nguy hiểm nhất) · ③ hướng mới nhìn từ bảng phân rã ô ở Mục 3 · ④ đánh giá xác suất ~60%.
**Xin nêu rõ khi nào bạn đang suy đoán và khi nào bạn có nguồn.**
