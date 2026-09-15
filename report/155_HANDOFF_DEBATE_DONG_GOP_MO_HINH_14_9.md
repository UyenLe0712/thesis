# 155 — BÀN GIAO CHO PHIÊN DEBATE: chốt phương pháp cuối (đóng góp MÔ HÌNH) để nâng số

*Viết 14/9/2026 tối. **Tự chứa** — đọc một mình file này là đủ để tranh luận. **Thắng `146`** (bàn giao 7/9)
ở hai điểm: ranh giới về thước đã đổi (mục 0) và có thêm các thước mới (mục 2). Mọi con số dưới đây lấy
từ tệp kết quả trong kho (`runs/*.json`), đường dẫn ghi cạnh từng bảng.*

---

## 0. Câu hỏi và luật chơi hiện hành

**Câu hỏi:** chọn **một phương pháp mô hình cuối cùng** (train/suy luận trên phía mô hình sinh câu) để
nâng số chính của luận văn, chạy được trong thời gian và ngân sách còn lại (mục 5). Hoặc chứng minh bằng
số rằng không còn hướng nào đáng chạy.

**Chỉ đạo của chủ luận văn (14/9, thắng mọi luật cũ):** *"Quan trọng là metric nào đó vừa hợp lý (ưu tiên
metric đã có sẵn cho thuyết phục hội đồng) vừa cho số cao, còn mấy cái mà ngưỡng đăng ký trước hay gì đó
bạn cứ bỏ đi"* · *"Tôi chỉ cần tốt nghiệp"*.
⇒ **Bỏ** các ràng buộc "khoá trước / không đổi thước headline / không nới sau khi thấy điểm".
⇒ **Vẫn giữ** (vì hội đồng bắt được): số thật từ tệp thô · khai đúng tên và nguồn thước · in mốc câu chuẩn
cạnh số mô hình · không tuyên bố "hơn có ý nghĩa" khi bảng trong bài tự mâu thuẫn · **không tối ưu thẳng
vào bộ trỏ chấm (UGround-V1-2B)** — dùng nó để thưởng/lọc/chọn câu thì thước thành hàm mục tiêu, hội đồng bác.

---

## 1. Bài toán, dữ liệu, mô hình

- **Đầu vào:** ảnh màn hình Android + mục tiêu tác vụ + lịch sử các bước trước (câu chuẩn, teacher-forced)
  + 24 dòng OCR của màn. **Đầu ra:** một câu tiếng Anh cho người đọc, ví dụ *"Tap the share icon at the top right"*.
- **Dữ liệu:** AndroidControl (Li et al., NeurIPS 2024 D&B). Dạy 64.567 bước (41.191 bước chạm). Kiểm
  **4.463 bước chạm** = quần thể chấm. Rò rỉ dạy–kiểm = 0 ở mức tác vụ.
- **Mô hình:** Qwen2.5-VL-3B-Instruct, QLoRA 4-bit, phần thị giác đóng băng, cutoff 2560, 2 epoch (8.072 bước).
- **Chấm:** đưa câu cho **UGround-V1-2B** (bộ định vị độc lập, không thấy đáp án) → một toạ độ → so với
  điểm chạm vàng theo các luật ở mục 2. Tất định (0 bất đồng trên 1.625 lần chấm lại).

### Các nhánh đã train (một hạt giống trừ S1)

| nhánh | là gì |
|---|---|
| Base | Qwen2.5-VL-3B chưa tinh chỉnh |
| S1 (hạt 101, 202) | SFT trơn: sinh thẳng câu |
| **S2** | SFT **"mô tả phân biệt trước, phát ngôn sau"**: sinh `<desc>vai trò | tên | <point>x,y</point> | dấu hiệu phân biệt</desc>` rồi mới tới câu; `<desc>` bị cắt trước khi chấm. **Đóng góp đề xuất gốc.** |
| CE2-S2 | nhánh so sánh: SFT tiếp 800 bước từ S2 (cùng bước với MIN) |
| **MIN-DESC** (chặng hai) | ORPO tiếp từ S2 trên cặp chỉ khác ô khai báo (khai báo đúng vs khai báo phần tử khác), câu giữ nguyên |
| **Chặng ba (GRPO-point)** | GRPO 500 bước tiếp từ MIN, thưởng khi `<point>` trong ±140/1000 quanh điểm vàng; không có bộ trỏ trong phần thưởng |
| Nhánh ứng viên (`gui_sel`) | chọn tên trong khối ≤40 ứng viên dựng sẵn; lệch 3 biến so với các nhánh khác, chỉ so được với Base |

---

## 2. SỐ HIỆN CÓ — bộ ba số chính của luận văn (đã vào bài 14/9)

Nguồn: `runs/luat_d3.json` · `runs/luat_aitw_day_du.json` · `runs/luat_aitw_moi_hop.json` · `runs/d3_ktc.json`
(mã: `harness/luat_d3.py`, `luat_aitw_day_du.py`, `luat_aitw_moi_hop.py`, `d3_ktc.py`). KTC95 = bootstrap
gom cụm theo app, G = 1.091. Mọi nhánh cùng 4.463 bước.

### 2.1 Ba luật chính + cận trên

| nhánh | **AitW** (số chính) | AitW cận trên | D.3 | exec (chặt) |
|---|---|---|---|---|
| **Câu chuẩn (trần dụng cụ)** | **92,14** | 96,17 | 83,82 | 75,73 |
| **Chặng ba** | **77,30** [75,8; 78,8] | **85,01** | 67,04 [65,3; 68,7] | 60,07 [58,3; 61,8] |
| MIN-DESC | 76,41 | 84,36 | 66,55 | 60,05 |
| CE2-S2 | 76,09 | 83,93 | 66,03 | 59,42 |
| S1/202 | 75,31 | 81,92 | 66,10 | 59,62 |
| S1/101 | 74,37 | 81,04 | 65,49 | 59,11 |
| S2 | 73,40 | 80,78 | 63,63 | 57,18 |
| Nhánh ứng viên | 71,16 | 77,91 | 62,38 | 56,13 |
| Base | 63,39 | 73,36 | 53,60 | 47,59 |
| *sàn: "Tap the button." (lát 800)* | *25,88* | *41,62* | *14,12* | *12,00* |
| *sàn: câu của màn khác (lát 800)* | *17,38* | *35,88* | *8,62* | *6,12* |

**Định nghĩa (đọc từ mã):**
- **exec** = đúng loại thao tác ∧ |dx| ≤ 0,14W ∧ |dy| ≤ 0,14H ∧ điểm trỏ nằm trong ô Voronoi của điểm vàng
  (không phần tử nào gần hơn). Luật chặt: đòi tách khỏi phần tử sát bên.
- **D.3** = đúng loại thao tác ∧ điểm trỏ nằm trong khung phần tử vàng (luật gốc AndroidControl, Phụ lục D.3).
- **AitW** = đúng loại thao tác ∧ (‖Δ‖ chuẩn hoá ≤ 0,14 ∨ cả hai điểm trong khung phần tử vàng nới 1,4×).
  Chép từ `google-research/android_in_the_wild/action_matching.py`. Chỉ có khung vàng ⇒ **cận dưới** luật gốc.
- **AitW cận trên** = như trên nhưng vế khung xét **mọi** phần tử bấm được (≤50% màn). Sàn nhảy lên 41,6 ⇒ chỉ báo kèm.

### 2.2 Phép so ghép cặp (McNemar, KTC bootstrap cụm)

| phép so | AitW | D.3 | exec |
|---|---|---|---|
| S1/101 − Base | +10,98 *** | +11,90 *** | +11,52 *** |
| **S2 − S1/101** | **−0,96** [−2,18; +0,29] p=0,100 | −1,86 *** | −1,93 *** |
| CE2-S2 − S2 | +2,69 *** | +2,40 *** | +2,24 *** |
| MIN − S2 | +3,00 *** | +2,91 *** | +2,87 *** |
| **MIN − CE2** (riêng ORPO) | **+0,31** p=0,215 | +0,52 p=0,042 | +0,63 p=0,011 |
| **Chặng ba − S2** | **+3,90** [+2,90; +4,90] *** | +3,41 *** | +2,89 *** |
| **Chặng ba − S1/101** | **+2,94** [+1,77; +4,08] *** | +1,55 p=0,008 | +0,96 p=0,090 |
| Chặng ba − S1/202 | +1,99 [+0,84; +3,13] *** | +0,94 p=0,109 | +0,45 p=0,450 |
| MIN − S1/101 | +2,04 *** | +1,05 p=0,078 | +0,94 p=0,106 |
| Chặng ba − MIN (riêng GRPO) | +0,90 p=0,007 | +0,49 p=0,149 | +0,02 p=1 |

\*** = p < 0,001. **MDE** (mức chênh nhỏ nhất phát hiện được, đo trên exec) = **2,11**. Nhiễu giữa hai hạt giống S1:
0,52 (exec) · 0,94 (AitW).

**Đọc nhanh:**
- Hướng S2 → chặng hai → chặng ba là mô hình tốt nhất, và dưới AitW **vượt S1 có ý nghĩa** (+2,94 / +1,99).
- Nhưng **phần lớn công thuộc SFT tiếp** (CE2 − S2 = +2,69), riêng ORPO +0,31 (không ý nghĩa), riêng GRPO +0,90.
- Luật càng lỏng (exec → D.3 → AitW) thì các can thiệp càng lộ tác dụng ⇒ các cải thiện hiện có chủ yếu là
  **đưa lần chạm tới gần đúng phần tử**, chưa phải tách phần tử khỏi phần tử sát bên.

### 2.3 Thước khác đã đo (đã vào ch6)

- **Loại thao tác đúng** (bước chạm): chặng ba / MIN / CE2 **98,9** · S1 94,4 · Base 96,5.
- **Bộ chấm COCO** (`runs/text_metrics_coco.json`): BLEU-4 chặng ba 49,9 · S1 51,6/51,7 · Base 15,3 · METEOR 37,3 ·
  ROUGE-L 68,5 · SPICE 42,5 (S1 44,4) · CIDEr-D ~400. **BERTScore** rescaled 66,8 · **chrF** 61,9 (`runs/text_metrics_them.json`).
  ⚠️ Nhóm văn bản xếp **S1 trên** MIN/chặng ba.
- **Toạ độ mô hình tự khai trong `<desc>`**: chặng ba trong khung vàng 65,5 · AitW khung vàng 78,5 (MIN 65,2 / 77,3).
- **Người nghe trắc nghiệm**: kết quả đủ ở **§2.4** ngay dưới.

### 2.4 Người nghe trắc nghiệm Phi-4 (commit Kaggle đêm 14/9, về máy 15/9)

**Giao thức.** `microsoft/Phi-4-multimodal-instruct` (MIT, nền Phi-4-mini, ngoài họ Qwen; commit HF `93f923e1…`,
ghi ở `runs/som/huggingface_repos_commit_14_9.json`) nhận ảnh màn hình có vẽ khung + số lên mọi phần tử bấm được
(trung vị 15 ô/màn), cộng **một câu**, không mục tiêu, không lịch sử, rồi trả lời số ô. Đúng khi ô chọn chứa điểm chạm
vàng. Tiền lệ: *comprehension accuracy* của REG (Mao CVPR 2016 · Luo CVPR 2017) và định dạng trắc nghiệm của Mind2Web
(NeurIPS 2023). Giải mã tham lam, 16 mảnh ảnh, `sdpa`, fp16, T4×2, **3,4 s/bước**, **0 bước tràn bộ nhớ**.
Mã `harness/som_build.py · som_cau.py · som_listener.py (14/9-b)` · đọc `som_doc.py` + **`som_phan_tich.py`** (mới) →
`runs/som/som_ket_qua.json`, `runs/som/som_phan_tich.json`.

**Chọn người nghe (luật khoá trước, lát 200 bước cố định seed 20260914, theo câu chuẩn):** Phi-4 **50,5** · Pixtral-12B
**8,0** ⇒ Phi-4. ⚠️ Pixtral **không thua vì kém hiểu**: 164/200 câu trả lời mở đầu bằng *"The instruction …"* rồi bị cắt ở
8 token nên không ra số; trên 36 bước có ra số thì đúng 16 (44%). Đây là lỗi định dạng của giao thức (tối đa 8 token),
không phải phép so năng lực — nếu phải báo thì khai đúng vậy.
**Kiểm tất định:** 200 bước lát thử chạy lại trong lượt đủ cho kết quả **trùng tuyệt đối** (b = c = 0).

**Kết quả (4.463 bước chạm, KTC95 bootstrap cụm app G = 1.091):**

| câu đưa vào người nghe | chọn đúng | KTC95 | ∧ đúng thao tác |
|---|---|---|---|
| câu chuẩn | **54,94** | [53,05; 56,82] | 54,90 |
| chặng ba (GRPO) | **45,78** | [44,07; 47,49] | 45,57 |
| S1/101 | **44,63** | [42,88; 46,37] | 43,51 |
| Base *(3.566/4.463 bước — bị cắt ở trần giờ 11,3 h)* | 38,56 | [36,71; 40,44] | 37,55 |
| câu rỗng nghĩa `"Tap the button."` | 15,86 | [14,69; 17,04] | 15,86 |
| *mốc: đoán ngẫu nhiên (kỳ vọng) · trần phủ đáp án* | *10,06 · 95,72* | | |

**Phép so ghép cặp (4.463 bước):** chặng ba − S1/101 **+1,14 [+0,23; +2,10]**, McNemar b = 205 c = 256 **p = 0,020** ·
câu chuẩn − chặng ba +9,16 [+7,84; +10,48] · S1 − câu rỗng +28,77.

**Trên đúng 3.566 bước Base đã chấm — bốn thước cạnh nhau:**

| nhánh | người nghe Phi-4 | exec | D.3 | AitW |
|---|---|---|---|---|
| câu chuẩn | 55,22 | 75,32 | 83,51 | 92,12 |
| chặng ba | 46,27 | 60,24 | 67,19 | 77,31 |
| S1/101 | 44,70 | 58,92 | 65,40 | 74,06 |
| Base | 38,56 | 47,73 | 53,81 | 63,43 |
| **chặng ba − S1/101** | **+1,57 [+0,55; +2,58]** | +1,32 [+0,08; +2,53] | +1,79 [+0,52; +3,05] | +3,25 [+1,96; +4,57] |
| S1/101 − Base | +6,14 [+4,68; +7,62] | +11,19 | +11,58 | +10,63 |
| **vị trí chặng ba trong dải Base → câu chuẩn** | **46,3%** | 45,3% | 45,1% | 48,4% |

**Đọc:**
1. ⭐ **Thứ tự Base < S1 < chặng ba < câu chuẩn giữ nguyên dưới một người đọc ngoài họ Qwen**, và chặng ba nằm ở
   **cùng một vị trí tương đối (45–48%) trong dải Base → câu chuẩn dưới cả bốn thước**. Đây là bằng chứng độc lập mạnh
   nhất hiện có rằng mức tăng của mô hình không phải do UGround (dựng trên Qwen2-VL) ưu ái câu của mô hình họ Qwen ⇒
   **đóng phần lớn đòn "cùng họ Qwen"** còn mở ở mục GIỚI HẠN của `CLAUDE.md`.
2. ⭐ **Chặng ba hơn S1/101 có ý nghĩa dưới người nghe độc lập** (+1,14, p = 0,020, KTC loại 0), trong khi dưới exec
   trên 4.463 bước chỉ +0,96 p = 0,090. Cỡ hiệu ứng vẫn dưới MDE 2,11 và **chưa có S1/202, MIN dưới người nghe**.
3. **Thang nén:** trần câu chuẩn chỉ 54,9 và S1 − Base co từ ~+11 xuống +6,14 ⇒ người nghe này **không nâng số tiêu đề**;
   vai trò đúng là **kiểm chéo độc lập**, không phải số chính.
4. **Người nghe khó dần theo cỡ khối ứng viên** (câu chuẩn 79,6 ở ≤5 ô → 30,4 ở >40 ô; câu rỗng 41,4 → 6,4): phần lớn
   khoảng cách với trần là giới hạn của người nghe khi màn đông phần tử, không phải của câu.
5. **Đồng thuận từng bước với UGround thấp–vừa:** κ = 0,25 (câu chuẩn) · 0,44 (chặng ba) · 0,43 (S1) ⇒ hai người đọc
   sai ở **những bước khác nhau**, nên sự trùng thứ tự nhánh ở (1) không phải do hai dụng cụ cùng lỗi.
   ⛔ Không dùng "một trong hai người đọc trúng" (chặng ba 67,3%) làm số: không có tiền lệ cho luật "bất kỳ bộ nào
   trúng" (chỉ trung bình nhiều người nghe có tiền lệ, Zhao EACL 2021).

**Còn thiếu (cần một commit Kaggle nữa, ~5 h T4 miễn phí):** 897 bước còn lại của Base (~0,5 h, nối tiếp từ
`chon_phi4_base_s0/s1.jsonl`) · **MIN** (~2,3 h) · **S1/202** (~2,3 h). Có S1/202 thì mới in được phép so chặng ba − S1
dưới người nghe cho **cả hai hạt**, đúng luật "so với S1 phải báo cả hai hạt" ở §5.

**Hệ quả cho phiên debate đóng góp mô hình:** mọi phương pháp mới nên được chấm thêm bằng người nghe này (≈2,3 h T4/nhánh,
0 đồng) — nếu mức tăng giữ dưới cả UGround lẫn Phi-4 thì phản biện "tối ưu cho bộ chấm" khó đứng. Không dùng người nghe
này làm hàm thưởng (sẽ mất vai trò kiểm độc lập).

---

## 3. ĐIỂM NGHẼN ĐÃ ĐỊNH VỊ (nền cho mọi đề xuất)

1. **Nghẽn ở TRI GIÁC (chọn đúng phần tử), không ở diễn đạt.** Kênh A = toạ độ mô hình tự khai đúng (±14%): 70,10% ·
   kênh B = UGround đọc câu trỏ đúng: 69,36% (n=4.442). Khoảng cách câu chuẩn − MIN (exec) +15,53, **91% dồn vào 29,9%
   số bước mô hình tự khai sai phần tử**; trên lát đó câu chuẩn giảm 28,64 điểm, mô hình giảm 73,94.
2. **Khi khai báo đúng thì câu tốt:** MIN hơn S1 +8,83 exec và vượt cả câu chuẩn trên nhóm đó; khi khai báo sai thì −11,12.
3. **Lỗi khai báo lưỡng cực:** phần tử nhầm cách vàng trung vị 351 px (p25 70 · p75 748); 76,5% nằm ngoài dải 80–350 px
   ⇒ mô hình nhìn sang vùng khác hẳn, **không** lẫn hai nút cạnh nhau.
4. **Hệ số truyền nhỏ:** GRPO nâng tỉ lệ khai báo đúng cả tên lẫn toạ độ +2,56 (p=1,3e−08), kênh A +1,60, nhưng exec chỉ
   +0,045 trên cùng quần thể ⇒ d(exec)/d(A) ≈ 0,028 (dưới AitW mức tăng tổng là +0,90).
   **66,7%** số bước khai báo đổi mà câu không đổi một ký tự ⇒ học ưu tiên ở tầng khai báo khó chạm tới câu.
5. **Trần câu chuẩn dưới exec 75,73 là giới hạn dụng cụ:** 72% ca mù do bộ trỏ lệch >14%; dưới AitW trần là 92,1.
6. **Nhánh ứng viên:** khi có đáp án trong khối và mô hình dám chọn thì đạt 71,4 exec; hỏng vì **bỏ cuộc quá mức**
   (27,3% số bước có đáp án), khâu bỏ cuộc mù với log-likelihood của chính mô hình (AUC 0,69–0,72).

---

## 4. ĐÃ THỬ — kết quả và lý do dừng (đừng đề xuất lại mà không có lý do mới)

| hướng | kết quả | tệp |
|---|---|---|
| S2 khai báo trước (SFT) | −1,93 exec so S1; hạt 202 không chạy (ngân sách) | `report/117` |
| S2r, S2-nopoint | không train (lý do đo được) | `report/117` |
| MIN-DESC (ORPO tầng khai báo) | +0,63 exec so CE2 (78% mức tăng thuộc SFT tiếp) | `report/106` (x12) |
| MIN-ONPOLICY (cặp âm từ lỗi của chính S2) | dừng ở tiêu chí: chỉ 3,3% bước dựng được cặp | `report/106` (x13) |
| Nhánh ứng viên `gui_sel` | 56,13 exec; bỏ cuộc quá mức; quét ngưỡng τ không cứu được | `report/136`, `142` |
| Chặng ba GRPO thưởng `<point>` | +0,02 exec / +0,90 AitW so MIN; dự báo +1,10 bị bác | `report/144` |
| Nội suy trọng số MIN↔GRPO (5 mức α) | đường cong đơn điệu, không điểm giữa nào hơn đầu mút | `report/153` |
| **VIS-SFT** (mở băng thị giác, SFT từ Base trên dữ liệu S1) | điểm kiểm giữa lượt (bước 3.200/7.876) thấp hơn MIN **−7,50** trên val ⇒ dừng; lượt không chạy hết, **không có điểm test** | `harness/colab_vissft_9_9.md` mục KẾT QUẢ K1 |
| Bị bác bằng số, chưa chạy | ORPO tầng câu (trần thật −0,65…+2,88) · `gui_sft_match` (59,44) · OCR/cây trợ năng vào đầu vào · vá tên bằng OCR · chưng cất qua bộ trỏ thứ hai · đa nhiệm đích hộp · RL trực tuyến · Spatial CoT · gộp nhánh ở đầu ra (bộ chọn không-oracle ≤ 60,72) · Qwen3-VL-4B / Qwen2.5-VL-7B (ngân sách) | `report/151` §2.2, `143` |

⚠️ Với luật AitW (lỏng với lỗi gần), một số hướng bị bác **dưới exec** có thể đáng xét lại — nhưng phải có số, không suy.

---

## 5. RÀNG BUỘC

- **Thời gian:** mốc bảo vệ "trên 6 tuần" tính từ 9/9/2026 ⇒ còn khoảng **5 tuần** (tới cuối tháng 10). Luận văn cần
  thêm vài ngày viết + cập nhật slide sau khi có số.
- **Máy:** WSL không GPU. Kaggle T4×2 **miễn phí 30 h/tuần** (suy luận + chấm một nhánh 4.463 bước ≈ 5,6 h UGround;
  suy luận Qwen2.5-VL-3B ~2–3 h). Colab A100 **trả tiền**, ngân sách ban đầu 50 h A100, **đã tiêu một phần cho VIS-SFT**
  (đếm lại đơn vị trong phiên). Luật chọn máy: CPU → T4 → L4 → A100, chỉ lên A100 khi L4 chậm hơn 1,5×.
- **Chi phí đã đo:** SFT đủ 8.072 bước ≈ 23 h A100 (10,3 s/bước) · ORPO 800 bước ≈ 4,7 h · GRPO 500 bước ≈ 5,6 h A100.
  Khâu mã hoá token chạy CPU, **không** chạy trên A100.
- **Hạt giống:** nhánh mới chỉ có một hạt ⇒ so với S1 phải báo cả S1/101 và S1/202.
- **Backbone:** giữ Qwen2.5-VL-3B (bảng 8 nhánh cùng backbone; 7B ≥ 46 h A100).

---

## 6. BẢN ĐỒ TỆP để kiểm lại số

| cần | tệp |
|---|---|
| tệp thô từng bước (toạ độ trỏ, câu, cờ đúng) của mọi nhánh | `runs/score_*_raw.jsonl`, `runs/grpo_point/score_grpo_point_seed101_raw.jsonl`, `runs/sel/score_gui_sel_seed101_raw.jsonl` |
| câu sinh + `<desc>` | `runs/preds_*.jsonl`, `runs/grpo_point/preds_grpo_point_seed101.jsonl` |
| khung phần tử vàng | `harness/dg1_cache/test_ac/descriptors.jsonl` (không track; dựng bằng `descriptor_label_build.py`) |
| tính lại ba luật + KTC | `harness/luat_d3.py` · `luat_aitw_day_du.py` · `luat_aitw_moi_hop.py` · `d3_ktc.py` |
| người nghe trắc nghiệm Phi-4 | tệp từng bước `runs/som/chon_phi4_{chuan,grpo,s1_101,base,san}.jsonl` (tệp `_s0/_s1` là hai nửa GPU, tệp gộp đã đủ) · khối ứng viên `harness/dg1_cache/som/som.jsonl` · đọc `harness/som_doc.py`, `harness/som_phan_tich.py` · runbook `harness/kaggle_som_listener.md` |
| bảng trong luận văn | `harness/sinh_bang_nhieu_thuoc.py` → `thesis/chapters/bang_nhieu_thuoc.tex` (sinh tự động) |
| cấu hình train | `harness/train_config*.yaml`, `harness/grpo_point.py` |
| trạng thái + luật dự án | `CLAUDE.md` (khối 14/9 đứng đầu phần trạng thái) |

---

## 7. Gợi ý khung cho phiên debate (không phải kết luận)

1. Mục tiêu đo: nâng **AitW** (số chính) cho nhánh tốt nhất vượt 77,30, và giữ/vượt S1 ở cả hai hạt.
2. Mỗi đề xuất phải trả lời: tác động vào điểm nghẽn nào ở mục 3 · vì sao khác các hướng ở mục 4 · kỳ vọng bằng số có
   căn cứ · chi phí theo mục 5 · rủi ro hội đồng bắt (đặc biệt: công thuộc "train thêm" chứ không thuộc phương pháp —
   CE2 − S2 = +2,69 là tiền lệ).
3. Ưu tiên phương pháp có tiền lệ ở hội nghị lớn và chạy được trong ≤ 2 tuần máy.
