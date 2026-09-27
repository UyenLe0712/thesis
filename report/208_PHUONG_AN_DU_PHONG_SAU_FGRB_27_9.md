# 208 — Phương án đóng góp mô hình dự phòng nếu FGRB không ra số (27/9/2026)

Mục tiêu do user đặt 27/9: (1) một đóng góp **mô hình** đủ bảo vệ luận văn; (2) vượt S1/101 trên các
thước câu phổ biến (BLEU-4 · CIDEr-D · SPICE · BERTScore…), không bắt buộc xuất phát từ S1;
(3) tra khoảng 50 bài gần nhất xem có hướng nào dùng được.

Cách làm: bốn nhánh tra cứu song song (tối ưu thẳng thước câu · sinh văn bản cho GUI · người nghe
trong vòng lặp · backbone/chưng cất/dữ liệu), khoảng 50 mục tài liệu, rồi một phép đo 0-GPU trên tệp thô.
Nhãn: [đo] = đo trong kho · [trích] = từ bài · [suy] = suy luận chưa kiểm.

## 1. Mốc phải vượt (bộ chấm COCO chính thức, n = 4.463) [đo]

| nhánh | BLEU-4 | CIDEr-D | SPICE | exec |
|---|---|---|---|---|
| **S1/101** | **51,56** | **416,1** | **44,37** | **59,11** |
| S1/202 | 51,66 | 419,2 | 44,23 | 59,62 |
| MIN-DESC | 49,92 | 401,0 | 42,24 | 60,05 |
| GRPO-point | 49,86 | 402,9 | 42,50 | 60,07 |

Mọi nhánh sau S1 đều **thua S1 trên thước câu** ⇒ muốn vượt S1 ở nhóm này thì mục tiêu huấn luyện
phải nhắm thẳng vào câu, không nhắm vào ô khai báo hay toạ độ.

## 2. Phép đo 0-GPU 27/9 — dư địa ở tầng câu [đo]

Script: `harness/cong_metric_cau.py` (tái lập đúng số từng nhánh của `runs/text_metrics_coco.json`
và `exec` gốc trước khi tính phần mới).

| cách chọn câu | BLEU-4 | CIDEr-D | exec |
|---|---|---|---|
| S1/101 greedy | 51,56 | 416,1 | 59,11 |
| oracle 2 hạt S1 (chọn theo CIDEr so câu chuẩn) | **55,25** | **457,9** | 61,75 |
| oracle 7 nhánh đã tinh chỉnh | 61,49 | 533,9 | 67,49 |
| MBR chéo 7 nhánh (không nhìn câu chuẩn) | 50,94 | 413,0 | 60,48 |

- Hai hạt S1 viết khác nhau ở **37%** số bước; cả 7 nhánh trùng nguyên văn chỉ 21,5%.
- MBR lúc suy luận **thua S1** trên thước câu, và exec 60,48 trùng trần ≤60,45 của hướng "gộp đầu ra"
  đã bác ⇒ **bỏ MBR lúc suy luận**. Dư địa chỉ lấy được bằng cách **học**.
- CIDEr câu và exec cùng chiều: exec của S1 theo tứ phân vị CIDEr câu 19,8 · 62,1 · 77,9 · 76,6
  (nhánh tra cứu GUI đo, tách từ đơn giản). ⚠️ Tương quan mặt cắt ngang, hệ số truyền thật có thể nhỏ
  như 0,028 (`151`).
- Tín hiệu người nghe không dùng nhãn vàng (UGround trỏ rơi vào ô Phi-4 chọn): S1 đạt exec 70,77 khi
  hai người nghe đồng ý và 46,17 khi bất đồng; kiểm bằng **UI-Venus độc lập**: 58,32 so với 37,65
  (lát 2.010 bước) ⇒ tín hiệu là chất lượng thật, không phải đặc thù UGround.

## 3. Ba phương án, xếp theo thứ tự nên thử

### PA-1 ⭐ — GRPO thưởng câu: CIDEr-D + người nghe khác thước (từ S1/101)

- Xuất phát: adapter S1/101 (nay có ở `runs/s1_seed101/adapter_s1_seed101/`).
- Thưởng, tính ngoài GPU chính:
  `r = CIDEr-D(câu, câu chuẩn)` (df trên câu chuẩn tập dạy)
  `+ λ₁·r_action` (động từ khớp `action_type` vàng — nhắm nguồn +3,11 dưới AitW đã đo 21/9)
  `+ λ₂·r_listener` (người nghe **không phải UGround** chọn đúng phần tử vàng: LLM chỉ đọc chữ trên
  khối ≤40 tên từ `train_ac/candidates.jsonl`, hoặc Phi-4 SoM)
  `+ mặt nạ độ dài` (BalCapRL).
- Hạ tầng dùng lại `harness/grpo_point.py` (TRL 0.29.1, β=0,04, tham chiếu = bản sao S1). G=8,
  nhiệt độ 1,0, ~2.000 câu nhắc.
- Chi phí [suy]: 6–8 h A100 (GRPO cũ 500 bước G=4 = 5,63 h [đo]); probe L4 trước theo luật 1,5×.
  Chấm test ~3 h T4, thước câu chạy CPU.
- Kỳ vọng [suy]: BLEU/CIDEr tăng vì mục tiêu trùng thước; exec không chắc.
- Tiền lệ [trích]: SCST (CVPR 2017) · BLEUBERI (NeurIPS 2025, BLEU làm thưởng GRPO) · CapRL
  (ICLR 2026, người nghe làm verifier) · BalCapRL (arXiv 2026, chạy trên Qwen2.5-VL-3B) ·
  Wright & Suhr (COLM 2026, thưởng bằng listener khác thước).
- Khác hướng đã chết: GRPO `<point>` thưởng toạ độ, ở đây thưởng **câu**; ORPO tầng câu chết vì
  66,67% cặp câu giống hệt, ở đây gradient vào thẳng câu; "RL trực tuyến" trong `151` bị bác vì bộ trỏ
  Venus trong vòng lặp và thưởng nhị phân, ở đây thưởng liên tục và không có bộ trỏ ảnh.
- Rủi ro chính: S1 sinh G mẫu giống nhau ⇒ advantage bằng 0 (GRPO cũ: `frac_reward_zero_std`
  0,515). Chặn bằng cổng C1 bên dưới.

### PA-2 — LV-RFT: lấy mẫu, lọc bằng người nghe + CIDEr, SFT lại (offline, gần như toàn T4)

- S1 sinh N=8 câu (nhiệt độ 0,7) trên ~5–10k bước chạm tập dạy; giữ câu được **UI-Venus ∧ Phi-4**
  xác minh trỏ trúng phần tử vàng, ưu tiên câu CIDEr cao; SFT adapter **mới** trên câu chuẩn + câu lọc.
- Nhánh so sánh bắt buộc: cùng số mẫu, lọc **ngẫu nhiên** (tránh bẫy 78% công thuộc nhánh so sánh).
- Tiền lệ: ReST/STaR, MBR/QE finetuning (ICLR 2024), CoGen (EMNLP 2024), Speaker-Follower (NeurIPS 2018).
- Chi phí [suy]: sinh 15–30 h T4 (0 đồng, 1–2 tuần hạn mức), chấm lọc UI-Venus là phần đắt; SFT vài giờ L4.
- Dùng khi PA-1 trượt cổng tài nguyên hoặc cần tránh A100.

### PA-3 — HPSD: tự chưng cất có màn kế làm thông tin đặc quyền

- Teacher = chính mô hình khi được xem thêm **màn sau thao tác** (chỉ lúc train); student giữ đầu vào
  y như S1. Loss = CE + 0,1·JSD, chỉ bật khi câu student kém câu teacher (khuôn GHD, arXiv 8/2026).
- Tín hiệu [đo, nhánh GUI]: 28,9% ca S1 đúng thao tác mà trượt có từ nội dung của câu chuẩn nằm ở màn
  kế mà S1 chưa nói ra; nhưng tên vàng chỉ nằm riêng ở màn kế 2,9%.
- Chi phí 8–10 h A100 [suy]; mới hơn nhưng rủi ro cao hơn ⇒ để sau.

### Không khuyến nghị lúc này

- **Đổi backbone sang Qwen3-VL-4B**: đi ngược quyết định 30/8 của user. Lý do ① (trần khối ứng viên)
  không còn áp cho SFT trơn, nhưng ③④ (ngân sách, chưa từng chạy, phải nâng LLaMA-Factory) vẫn đứng,
  và đổi backbone một mình là đóng góp yếu. Chỉ xét nếu user mở lại quyết định.
- **MBR / rerank lúc suy luận**: đo ở mục 2, thua S1 trên thước câu.

## 4. Cổng chung trước khi tiêu tiền

**C1 (Kaggle T4, ~1,5 h, 0 đồng):** S1/101 sinh 8 câu (nhiệt độ 1,0) + 1 câu greedy cho 400 bước val.
Đo: CIDEr best-of-8 so với greedy · tỉ lệ nhóm có độ lệch chuẩn thưởng bằng 0 · số câu khác nhau
trung bình mỗi nhóm.
- Dừng PA-1 và PA-2 nếu best-of-8 không hơn greedy ≥ +5% CIDEr, **hoặc** > 50% nhóm có std = 0.
- Có thể dùng lại dataset Kaggle `fgrb-p1-bundle` (đã có adapter S1/101 + ảnh + OCR của 1.567 bước val).
- ⚠️ Val là dữ liệu S1 đã thấy ⇒ greedy bị ghi nhớ làm đẹp ⇒ cổng này **thận trọng** (thiên vị chống
  lại việc đạt). Không trích số val ra báo.

**C2 (0-GPU, cho PA-1):** dựng người nghe chỉ đọc chữ trên khối ứng viên, chạy trên **câu chuẩn** và
câu S1 của vài trăm bước dạy; người nghe phải phân biệt được câu chuẩn với câu rỗng (dải ≥ 20 điểm)
thì mới đưa vào thưởng.

## 5. Trả lời câu (3) của user

Có. Khoảng 50 mục đã tra hội tụ về một điểm: **học từ phần thưởng đặt trên chính câu** (thước tham
chiếu + người nghe khác thước). Khe còn trống [đã tra, không khẳng định tuyệt đối]: chưa thấy bài nào
sinh step instruction trên AndroidControl rồi chấm bằng BLEU/CIDEr hoặc bằng bộ trỏ. Neo peer-reviewed
dùng được: SCST (CVPR 2017) · Speaker-Follower (NeurIPS 2018) · MBR finetuning (ICLR 2024) · CoGen
(EMNLP 2024) · OS-Genesis (ACL 2025) · SC-Captioner (ICCV 2025) · BLEUBERI (NeurIPS 2025) ·
CapRL (ICLR 2026) · Wright & Suhr (COLM 2026) · Jandial (Findings EACL 2026). Phần còn lại phần lớn
là arXiv, phải ghi đúng là preprint.

⛔ Chữ cấm: không viết "đầu tiên"/"novel" cho thưởng CIDEr, cho người nghe làm thưởng, hay cho màn kế
làm thông tin đặc quyền — đều đã có chủ (SCST · Mao/Luo · CapRL · GHD).

---

## 6. KIỂM TÍNH MỚI 27/9 (tối) — user: "phải có đóng góp mô hình, đừng chỉ áp dụng"

⛔ **PA-1 như viết ở mục 3 là ÁP DỤNG** (SCST 2017 + CapRL 2026 + đa thưởng kiểu BalCapRL). Bốn thành
phần mới được đề xuất để bù, mỗi cái kiểm tiền lệ đối kháng riêng (≥10 truy vấn/nhánh):

| ứng viên | ý | tiền lệ chiếm cơ chế | phán quyết | động cơ đo |
|---|---|---|---|---|
| C-A | advantage theo thứ tự từ điển: trúng đích trước, CIDEr sau | ReCode (ACL 2026 Main) · PROGRS (arXiv) · GDPO (ICML 2026) | trùng một phần, nặng | oracle lex exec **70,71** vs CIDEr-only 67,49, BLEU-4 −0,6; CIDEr xếp ngược exec 11,5% cặp [đo] |
| C-A′ | cổng mềm = P(đích đúng) từ hai người nghe khác họ, hiệu chỉnh trên nhãn vàng | Weaver (ICML 2025 workshop) · Cai et al. (arXiv, rút khỏi ICLR 2026) · Coste (ICLR 2024) | trùng một phần, nặng | hai người nghe đồng ý → UI-Venus 58,32 vs 37,65 [đo, nhánh tra cứu] |
| C-B | dồn advantage của người nghe vào span tên phần tử | Khandoga 2026 · CoRT · Wright & Suhr (COLM 2026) · VPPO (ICLR 2026) | trùng một phần | ⛔ **yếu**: chỉ 12,2% cặp hai hạt S1 khác exec là khác THUẦN ở chữ trên màn [đo] ⇒ **loại** |
| C-C | rollout phản thực đổi đích làm mẫu âm | NoisyRollout (NeurIPS 2025) · Mao MMI (CVPR 2016) · LUFFY (NeurIPS 2025) | trùng một phần, nặng | rủi ro rò đích qua 24 dòng OCR ⇒ **xếp cuối** |

Số C-B khác [đo]: token tên phần tử chiếm ~16% câu chuẩn; S1 đúng thao tác mà câu có từ của tên vàng
exec 80,9% (n=1.883) vs 38,8% (n=1.220). Script: `harness/cong_thuong_sai.py` (C-A) + lệnh trong phiên.

**Kết luận trung thực:** ở tầng học tăng cường trên câu, tới 2026 **không còn cơ chế nào còn trống**
trong bốn ứng viên. Cái còn bảo vệ được là **một phương pháp cho đúng bài toán này**: các mảnh thích
nghi từ tiền lệ, ghép theo lỗi đo được của chính bài toán, và **phải thắng các mốc "chỉ áp dụng" trong
ablation cùng ngân sách**. Nếu không thắng thì đó là áp dụng, phải báo đúng như vậy.

### Phương pháp đề xuất sau kiểm (thay PA-1)

GRPO từ S1/101, thưởng = g·𝟙[lớp đúng] trước, CIDEr-D trong lớp sau (C-A + C-A′), người nghe
huấn luyện (UI-Venus-7B + Phi-4 SoM) tách khỏi bộ trỏ chấm (UGround).
- Phần thích nghi (phải trích): GRPO · SCST · cổng theo kết quả (ReCode/PROGRS) · verifier yếu có
  hiệu chỉnh (Weaver) · hiệu chỉnh thưởng nhiễu (Cai).
- Phần riêng của bài toán: verifier là người nghe định vị GUI, hiệu chỉnh bằng **hộp vàng** của
  AndroidControl (không phải nhãn yếu); thước chấm là bộ trỏ thứ ba không vào vòng train.
- **Ablation quyết định có phải đóng góp không** (cùng số bước, cùng G):
  B0 GRPO CIDEr-only (= áp dụng SCST/BLEUBERI) · B1 cổng cứng một người nghe (= ReCode) ·
  B2 hiệu chỉnh Cai một người nghe · B3 g xáo trộn · **ours**.
  Ours phải hơn B0 ở exec mà không mất thước câu, và hơn B1/B2 ở exec. Không đạt ⇒ báo là áp dụng.
- Cổng trước GPU: C1 (độ đa dạng mẫu, mục 4) + **C3**: tỉ lệ FN/FP của từng người nghe trên câu chuẩn
  và **tương quan lỗi** giữa hai người nghe. Nhiễu ≤15% thì lợi ích dự báo gần 0 (2604.07666); tương
  quan lỗi cao thì hai người nghe không hơn một.
- ⚠️ 5 lượt × 6–8 h A100 ≈ 30–40 h ⇒ vượt xa mọi lượt trước; lịch sử dự án 0/5 can thiệp vượt MDE trên
  exec. Kỳ vọng thước câu tăng là có cơ sở (oracle), exec thì **không hứa**.

### Kiểm venue 27/9: 14/14 trích dẫn của report này ĐÚNG
(chi tiết "BalCapRL chạy Qwen2.5-VL-3B" chưa xác minh). Số SCST gốc (CVPR 2017, Bảng 4, Karpathy
test): Att2in XE greedy 99,0 → SCST 111,3. ⛔ "104,9 → 114,7" là bảng xếp hạng COCO, không phải XE→SCST.

## 7. Hai cổng rẻ — trạng thái 27/9

**C3 ĐẠT (0-GPU, `harness/c3_nhieu_nguoi_nghe.py` → `runs/c3_nhieu_nguoi_nghe.json`).** Luật ghi trong
đầu script trước khi chạy. Trên câu S1/101, giao ba bộ trỏ n=2.531 (đại diện trên tập kiểm, UGround
đóng vai "sự thật" nhiễu — hiệu chỉnh thật sẽ làm trên tập dạy bằng hộp vàng):
- (i) trượt trên câu chuẩn: Phi-4 45,06% (n=4.463) · UI-Venus 26,0% (n=300, sai số ≤14%) · UGround
  24,22% ⇒ nhiễu > 15%, cổng mềm có chỗ làm việc.
- (ii) κ(UI-Venus, Phi-4) = 0,426 ≤ 0,60 (κ Venus–UGround 0,747 · Phi-4–UGround 0,441).
- (iii) UGround trúng theo ô: V1P1 **95,05** (n=768) · V1P0 86,71 (489) · V0P1 41,53 (236) · V0P0
  **11,46** (1.038); lift gộp so với người nghe tốt nhất **+3,24 pp** (ngưỡng 3) — **vừa qua**.
- Phi-4 trúng câu rỗng 15,86% (đoán ngẫu nhiên 10,06%).

**C1 CHUẨN BỊ XONG, chưa chạy.** `harness/c1_mau_s1.py` (Kaggle T4) + `harness/c1_doc.py` (CPU) +
runbook `harness/kaggle_c1_da_dang_s1.md` + gói `_bundles/c1_script.zip`. Dùng lại dataset
`fgrb-p1-bundle`. 400 bước val chọn bằng seed 20260927 (249 click · 39 open_app · 33 input_text ·
32 scroll · 32 wait · 15 navigate_back). Đường đọc đã kiểm trên dữ liệu giả (8 nhánh làm 8 mẫu):
21,8% nhóm giống hệt, khớp 21,5% đo độc lập ở §2.
