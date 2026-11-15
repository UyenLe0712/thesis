# Bằng chứng nội bộ: phần thưởng nào đã thử với RL và số đo nói gì (để chọn phần thưởng thay SA-SPICE-v3)

Phạm vi: chỉ đọc tệp trong kho `/mnt/d/Master/Thesis` (không web), ghi 15/11/2026. Mọi đường dẫn tính từ gốc kho.
Quy ước nhãn: **[test]** = tập kiểm 4.463 bước chạm + 2.495 bước không chạm, trích được. **[dev]/[val]** = DEV-v3, val C1, val lớn 289, val400: chỉ để chọn, **cấm trích ra bài**. **[train-screen]** = sàng offline trên 8 mẫu SFT-cont của TRAIN-v3. **[tự tính]** = số tôi tính hôm nay từ tệp sẵn có, 0 GPU. Mọi lượt một hạt giống (101) trừ chỗ ghi khác.
Lưu ý phiên bản: `report/334_BANG_KET_QUA_TONG_HOP.md` trong cây làm việc đang ở trạng thái *modified* (dòng 11 ghi "Bootstrap B = 1000"), còn commit HEAD `3069e74` ghi đã sinh lại với B = 10.000; số điểm giống nhau, KTC có thể lệch ở chữ số thứ hai. Tôi trích bản trong cây làm việc.

---

## 1. Bảng mọi phần thưởng đã dùng trong RL (công thức, điểm xuất phát, câu nhắc, bước, kết quả)

### Takeaway
Không phần thưởng nào vượt ck500 (GRPO + SPICE, exec 60,65) trên test với KTC loại 0; nhóm dẫn đầu gồm SPICE (ck500), ROUGE-L (60,63) và SCST + SPICE (60,54). Nhưng chính ck500 không tái lập: train lại cùng cấu hình (A/A) chỉ được 59,74, và so cùng mã (A/A) thì ROUGE-L (+0,90) và SCST + SPICE (+0,81) hơn GRPO + SPICE có ý nghĩa sau Holm. Số test của SA-SPICE-v3 ck400 **chưa có** (kernel `sa3-test-ck400` đang chạy).

### Cited Findings

**A. Lưới phần thưởng cùng GRPO, cùng điểm xuất phát S1/101, 1.000 câu nhắc của ck500, G = 8, KL β 0,04 về S1, lr 1e-5, 500 update** — [report/334 §1, §2](../../report/334_BANG_KET_QUA_TONG_HOP.md). Mọi phần thưởng lưới đều có dạng `clip?(metric − 0,02·max(0, n_w(y) − n_w(g) − 3))`, câu rỗng = 0 — [harness/grpo_luoi.py `lam_thuong`, dòng ~148–165](../../harness/grpo_luoi.py); ck500 dùng `SPICE − MU·max(0, n_w(y)−n_w(g)−3)`, MU = 0,02 — [harness/grpo_spice.py dòng 24, 58–62](../../harness/grpo_spice.py). ck500 dùng `loss_type="dapo"`, `num_iterations=1` nên clip không hoạt động — [report/326 §7](../../report/326_BAN_GIAO_LUOI_RL_1_11.md).

| phần thưởng (mã) | exec [test] | D.3 | AitW đầy đủ | đúng loại (chạm) | Δexec − A/A | Δexec − ck500 | Δexec − SFT tiếp | Δexec − S1/101 |
|---|---|---|---|---|---|---|---|---|
| SPICE, lượt gốc ck500 (`grpo_spice.py`) | **60,65** | 67,02 | 76,25 | 95,85 | +0,92 [+0,49; +1,40]† | – | +0,49 [−0,07; +1,08] p=0,109 | +1,55 [+0,83; +2,36] p=1,5e−5 |
| ROUGE-L | 60,63 | 67,04 | 76,79 | 96,75 | +0,90 [+0,40; +1,41]† | −0,02 [−0,53; +0,52] p=1,0 | +0,47 [−0,14; +1,05] | +1,52 [+0,78; +2,28] |
| METEOR | 60,27 | 66,75 | 76,27 | 96,17 | +0,54 [−0,04; +1,11] | −0,38 [−0,95; +0,18] | +0,11 | +1,17 [+0,40; +1,94] |
| CIDEr-D | 60,27 | 66,44 | 76,00 | 95,99 | +0,54 [+0,04; +1,07] | −0,38 [−0,87; +0,13] | +0,11 | +1,17 [+0,37; +1,99] |
| CIDEr-D (mã CTG A2, 500 update) | 59,96 | 66,44 | 76,52 | 96,10 | +0,22 | −0,69 [−1,37; −0,07] p=0,040 | −0,20 | +0,85 |
| CIDEr-D (mã CTG A2, 1000 update) | 59,98 | 66,35 | 76,07 | 96,15 | +0,25 | −0,67 [−1,32; +0,04] | −0,18 | +0,87 |
| SPICE, train lại (A/A, `grpo_luoi.py`) | 59,74 | 66,41 | 75,71 | 95,56 | 0 | −0,92 [−1,35; −0,46] p=5,5e−5 | −0,43 | +0,63 [−0,09; +1,36] p=0,085 |
| SPICE ghép ngẫu nhiên trong nhóm (xao101, kiểm soát) | 59,11 | 65,58 | 74,59 | 94,06 | −0,63 | −1,55 [−2,34; −0,81] | −1,05 [−1,63; −0,50] | 0,00 [−0,42; +0,44] |
| *không thưởng: SFT tiếp (125 update, cùng câu nhắc)* | *60,16* | *66,64* | *75,71* | *96,06* | +0,43 | −0,49 [−1,07; +0,09] p=0,109 | – | +1,05 [+0,46; +1,61] p=0,0004 |

Nguồn: [report/334 Bảng 2.1, 2.3, 3b](../../report/334_BANG_KET_QUA_TONG_HOP.md). † = còn ý nghĩa sau Holm (họ 9 phép so với A/A). Chạy chưa có số test: chrF, BLEU-4, SPIDEr, BERTScore trong lưới S1 — [report/334 chú thích b](../../report/334_BANG_KET_QUA_TONG_HOP.md).

**B. Cùng thưởng SPICE, đổi thuật toán** [test] — [report/334 Bảng 1.1, 1.3](../../report/334_BANG_KET_QUA_TONG_HOP.md): SCST (mốc greedy) 60,54 (− ck500 −0,11 [−0,56; +0,35]); PPO λ=1, 1.000 update 60,07 (−0,58 [−1,20; −0,02]); REINFORCE EMA 60,00 (−0,65*); PPO λ=0,95 59,98 (−0,67*); RLOO 59,44 (−1,21*). Dr.GRPO treo ở checkpoint-475, chưa chấm — [report/320 §20](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).

**C. Độ đo văn bản [test, mức kho]** — [report/334 Bảng 2.2](../../report/334_BANG_KET_QUA_TONG_HOP.md):
- SPICE ck500 45,79 · A/A 46,00 · ROUGE-L 45,57 · METEOR 45,13 · CIDEr-D 44,43 · SFT tiếp 45,33 · S1 44,37.
- ROUGE-L thắng ck500 ở 6/7 độ đo (trừ SPICE), KTC loại 0 ở ROUGE-L +0,91, chrF +0,55, BERTScore +0,51 — [report/320 §14.4](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- Ba điểm lưu GRPO + SPICE (ck500/101, ck500/202, A/A) gần trùng trên mọi độ đo văn bản (SPICE 45,7–46,0) trong khi exec 59,74–60,65 ⇒ "đích thưởng tái lập được, exec thì không" — [report/320 §21](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- So A/A, mỗi lượt tăng đúng độ đo nó được thưởng: METEOR chrF +1,80* nhưng BLEU-4 −2,21*, SPICE −0,87*; CIDEr-D: CIDEr-D −6,40*, SPICE −1,57* — [report/320 §21 bảng "X − A/A"](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).

**D. Các phần thưởng ngoài lưới đã train**
- **GRPO-point** (từ MIN-DESC, 500 update, 2.000 câu nhắc): `r_point` 1,0 nếu `<point>` trong ±140 quanh điểm vàng + `r_format` 0,2 + `r_name` 0,1, không bộ trỏ trong thưởng. [test] exec 60,07 (= MIN 60,05, Δ +0,02 [−0,59; +0,64]) dù khai báo tăng +2,56 pp — [CLAUDE.md khối "6/9 — LƯỢT GRPO `<point>`"](../../CLAUDE.md); [report/334 §3](../../report/334_BANG_KET_QUA_TONG_HOP.md).
- **CTG-GRPO** (A3 = CIDEr-D + cộng `λ_k·z(đúng loại)` vào advantage cho lớp scroll/type/back; A2 = CIDEr-D không cộng; 1.000 update) — [report/279 §1](../../report/279_TONG_HOP_CTG_GRPO_4_10.md). [test không chạm] A3 − A2 scroll +1,06 [−0,27; +2,48], back **−2,96 [−5,32; −0,76]**; A3 − S1 scroll −5,30 [−7,19; −3,53] ⇒ R-CTG không đạt, CTG không gỡ tác hại ở scroll — [report/279 §4g](../../report/279_TONG_HOP_CTG_GRPO_4_10.md). A4 (lấy mẫu lại theo lớp) và A7 (CIDEr-D + thưởng đúng loại +1) **không chạy** — [report/279 §1, §4g "Hệ quả"](../../report/279_TONG_HOP_CTG_GRPO_4_10.md).
- **288 người nghe Phi-4** (train tiếp ck500 thêm 250 bước): SPICE-cont, SPICE + LR (Phi-4 không cổng), SPICE + GLR (có cổng). [val lớn 1.002 bước] Δexec − ck500: −0,20 · **+0,30 [−0,79; +1,41]** · −0,50; SPICE + LR làm SPICE −1,53 [−2,83; −0,22]; không nhánh nào qua sàng +0,5 ⇒ giữ ck500 — [report/289 §1](../../report/289_KET_QUA_VAL_LON_288_BAN_4_7_10.md). λ = 2 chưa chạy — [CLAUDE.md bảng "Đọc file nào", hàng 288](../../CLAUDE.md).
- **RAFT** (chọn mẫu trội greedy của ck500, SFT 125 bước) [test] 60,23, − ck500 −0,43 [−0,82; −0,04]; **GA-DPO** không học (acc ≤ 0,544), không có số test — [CLAUDE.md hàng 314](../../CLAUDE.md); [report/334 §3b](../../report/334_BANG_KET_QUA_TONG_HOP.md).
- **RGTC-SPICE** (SPICE + action + target contrast T trên màn): dừng trước GPU vì FULL − A2 = 0,000 [−0,012; +0,010] [val C1, 8 mẫu S1] — [report/320 §25](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).

**E. SA-SPICE-v3** — công thức `R = clip(0,8·[α_g·s + (1−α_g)·c] + 0,2·A − d)`, α_g = 0,8·min(1, K_g/3), c = chrF/100, A ∈ {0; 0,5; 1}, d = min(0,05; 0,02·max(0, n_w(y)−n_w(g)−3)) — [report/SA_SPICE_v3_extracted_verified.md §2](../../report/SA_SPICE_v3_extracted_verified.md); verifier v3 làm A thực tế ∈ {0,5; 1} (toggle 0 trên 7.558 cặp RAFT) nên phần action thành "thưởng khớp thao tác" — [report/333 §9](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md). Train từ **SFT-cont** (không phải S1), KL về sft_cont_merged, 1.000 câu nhắc **TRAIN-v3**, 500 update, seed 101 (lệch memo 401/503/907, user quyết) — [report/333 §11](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md). Từ ck400 tới ck500 lấy mẫu có bản vá `remove_invalid_values` sau lỗi NaN fp16 — [report/333 §11 phiên 2–3](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md).
- [dev, 1.338 bước chạm] exec: SFT-cont 62,93 · SA ck500 64,35 · SA ck400 64,28 · chrF ck400 63,98. SA ck400 − SFT-cont **+1,35 [+0,32; +2,38] p=0,013**; chrF ck400 − SFT-cont +1,05 [−0,23; +2,24] p=0,114; **SA ck400 − chrF ck400 +0,30 [−0,60; +1,24] p=0,61** — [report/334 §6a–6b](../../report/334_BANG_KET_QUA_TONG_HOP.md); [report/333 §12](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md).
- [dev, không chạm, 667 bước gold tin được] SA ck500 − SFT-cont −5,55 [−8,17; −3,12]; SA ck400 −2,40 [−4,67; −0,29]; chrF ck400 −6,90 [−9,29; −4,71]; tụt gần hết ở back (84/104 → 56–60) — [report/333 §12](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md).
- [dev, văn bản, 2.223 bước] SA ck400 − SFT-cont: BLEU-4 −3,15*, ROUGE-L −0,87*, CIDEr-D −13,82*, SPICE −1,01*, chrF −0,04, BERTScore −1,08*; trên bước chạm chỉ BLEU-4 −1,94* và chrF +1,00*. SA ck400 − chrF ck400: BLEU-4 +2,57*, CIDEr-D +18,37*, SPICE +1,63* — [report/334 §6d](../../report/334_BANG_KET_QUA_TONG_HOP.md).
- Train: thưởng phẳng trong nhiễu (SA 0,608 → 0,609 ck100 → ck500); KL SA 0,004 → 0,043, chrF 0,009 → **0,114 ở ck500 (vượt ngưỡng 0,10)** — [report/333 §11 bảng "Số train"](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md).
- Chọn ck400 lên test theo tiêu chí khả thi (không chạm tụt ≤ 3, scroll+back gộp tụt ≤ 5, KL ≤ 0,10); chrF ck400 không chấm test vì trượt tiêu chí khả thi — [report/333 §13](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md). [test] **chưa có** — [report/334 §12](../../report/334_BANG_KET_QUA_TONG_HOP.md).

**F. Câu đã chốt cấm viết**
- "Cấm viết 'tốt nhất' từ lưới một hạt giống" — [report/320 §13](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md); "Chưa có căn cứ viết ck500 hay SPICE tốt nhất" — [report/320 §14.2](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- "Không còn viết được 'GRPO + SPICE tốt nhất trong lưới' hay 'ck500 hơn REINFORCE/RLOO' như kết luận về phương pháp" — [report/320 §21](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- "Cấm viết 'GRPO + SPICE hơn SFT tiếp'" — [report/320 §18](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- "Chưa được viết 'SPICE giúp định vị tốt hơn'" — [report/320 §14.5](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- Memo SA-SPICE-v3 cấm viết "SA-SPICE tốt nhất/SOTA", "no-harm nếu NI chưa pass" — [report/SA_SPICE_v3_extracted_verified.md §14](../../report/SA_SPICE_v3_extracted_verified.md).

### Inferences
- Trong lưới cùng mã, khoảng cách giữa các phần thưởng (≤ 0,9 exec) cỡ biến thiên giữa hai lượt train cùng phương pháp (ck500 − A/A 0,92; ck500 − ck500/202 0,72) ⇒ một hạt giống không đủ để xếp hạng phần thưởng; mọi thay thế SA-SPICE-v3 cũng sẽ chịu đúng giới hạn này.
- Không phần thưởng nào hơn SFT tiếp có ý nghĩa trên test (mọi Δ − SFT tiếp có KTC phủ 0) ⇒ đòn "RL không hơn train thêm" còn mở với mọi phần thưởng, kể cả phần thưởng thay thế.
- SA-SPICE-v3 trên dev mới hơn SFT-cont (cùng cỡ ck500 − S1 trên test) nhưng không hơn chrF; nếu test lặp lại hình này thì phần thưởng thay thế cần ít nhất phải vượt chrF và SFT-cont, không chỉ vượt SFT-cont.

### Gaps
- Chưa có exec test của SA-SPICE-v3 ck400 và của SFT-cont trên bước không chạm (kernel đang chạy, [report/334 §5, §12](../../report/334_BANG_KET_QUA_TONG_HOP.md)).
- Không có hạt giống thứ hai cho bất kỳ lượt lưới nào ngoài ck500/202; không có SA-SPICE-v3 với seed 401/503/907.
- GRPO + chrF/BLEU-4/SPIDEr/BERTScore từ S1 có mã nhưng chưa có số test; SPICE-MATCH, Sparse-SPICE, Action-SPICE, FIXED, FIXED+A, SPIDEr-like, ROUGE-L trên TRAIN-v3 chưa train.

---

## 2. Bằng chứng sàng offline (concordance, nhóm hoà, oracle) cho mọi phần thưởng ứng viên

### Takeaway
Ở cả ba bộ sàng (val C1 8 mẫu S1; TRAIN-v3 8 mẫu SFT-cont), SPICE thuần là phần thưởng xếp câu exec kém nhất, nhiều hoà nhất; mọi thành phần của SA-SPICE-v3 cộng thêm concordance có ý nghĩa so các bản SPICE con, nhưng **chrF đứng một mình luôn cao hơn SA-SPICE-v3** (có ý nghĩa trên TRAIN-v3). Và sàng offline **không dự đoán được** thứ hạng sau train (H2 bị bác, CIDEr-D oracle mạnh nhất nhưng GRPO + CIDEr-D không hơn; chrF sàng hơn SA nhưng sau train ngang SA).

### Cited Findings

**Sàng mức 1 TRAIN-v3** [train-screen; 622 bước chạm, 263 package, 8 mẫu SFT-cont T=1,0; greedy exec 61,41, TB mẫu 55,55; A=1 ở 6.025/8.000 câu] — [report/333 §10](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md); [runs/sa_spice_v3/screen/out/sa3_screen.json](../../runs/sa_spice_v3/screen/out/sa3_screen.json):

| reward | công thức (protocol, [report/SA_SPICE_v3_extracted_verified.md §6.1, §2bis](../../report/SA_SPICE_v3_extracted_verified.md)) | concordance | zero-std | oracle (pp) | SA − reward: concordance [KTC95 cụm package] |
|---|---|---|---|---|---|
| SPICE-MATCH | clip(0,8s + 0,1 − d) | 0,6766 | 5,79% | +7,22 | +0,094 [+0,069; +0,119] |
| Action-SPICE | clip(0,8s + 0,2A − d) | 0,7162 | 4,18% | +8,18 | +0,055 [+0,035; +0,074] |
| FIXED | clip(0,8(0,8s+0,2c) + 0,1 − d) | 0,7470 | 0,96% | +8,60 | +0,024 [+0,012; +0,037] |
| FIXED+A | clip(0,8(0,8s+0,2c) + 0,2A − d) | 0,7567 | 0,96% | +8,92 | +0,014 [+0,005; +0,025] |
| Sparse-SPICE | clip(0,8S + 0,1 − d) | 0,7634 | 0,96% | +8,76 | +0,007 [+0,003; +0,012] |
| **SA-SPICE-v3** | clip(0,8S + 0,2A − d) | 0,7708 | 0,96% | +9,08 | – |
| chrF | clip(c − d) | **0,7941** | 1,13% | **+10,85** | **−0,023 [−0,046; −0,002]** (oracle −1,77 [−3,09; −0,58]) |
| SPIDEr-like | clip(0,5s + 0,5·CIDEr-D/10 − d) | 0,7788 | 1,93% | +9,73 | −0,008 [−0,030; +0,012] |
| ROUGE-L | clip(ROUGE-L − d) | 0,7802 | 2,25% | +9,93 | −0,009 [−0,035; +0,016] |

Đọc của report: "mỗi thành phần của SA-SPICE-v3 … đều cộng thêm concordance có ý nghĩa so với các bản SPICE con, nhưng chrF đứng một mình xếp câu exec tốt hơn SA-SPICE-v3, có ý nghĩa ở cả hai đại lượng" — [report/333 §10](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md). Phân bố K_g trên 1.000 bước TRAIN-v3: K=0 31 · 1: 72 · 2: 345 · 3: 147 · 4: 97 · 5: 109 · ≥6: 198 — [sa3_screen.json `K_g_phan_bo`](../../runs/sa_spice_v3/screen/out/sa3_screen.json).

**Sàng val C1 R0–R4** [val, 249 bước chạm, 8 mẫu S1/101, 1.528 cặp khác exec] — [report/332 mục "Kết quả Kaggle CPU"](../../report/332_KAGGLE_CPU_REWARD_SCREEN_8_11.md): bỏ cặp hoà: R0 (SPICE − phạt) 0,753 (hoà 27,0%) · R0_capped 0,772 · R_fixed 0,8s+0,2c 0,793 · R2_sparse 0,793 · R3_action 0,816 · R4_sparse_action 0,818 · chrF một mình 0,836. R4 − chrF −0,018 [−0,053; +0,018]. "Phần lớn mức tăng của đồng thuận là do hết hoà". Stress test: R4 không phân biệt sai phần tử (`wrong_target`: câu đúng 0,254 < câu sai 0,912), sai vị trí, đảo bật/tắt.

**H2 (đặc tính tín hiệu) trên val C1** [val] — [report/320 §16](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md); [report/323 §9.1](../../report/323_DEBATE_VA_ACTION_KHAO_SAT_GRPO_SPICE_ACE_1_11.md): conc (hoà 0,5) METEOR 0,871 · CIDEr-D 0,868 · chrF 0,843 · BERTScore 0,843 · ROUGE-L 0,835 · SPIDEr 0,824 · BLEU-4 0,806 · tên+loại 0,736 · SPICE có cổng 0,704 · **SPICE 0,685** (nhóm hoà 7,2%, cặp hoà 38,2%) · chỉ loại 0,620. "Phép kiểm chéo quan trọng nhất … KHÔNG đạt": H2 xếp METEOR > CIDEr-D > ROUGE-L > SPICE gần như ngược thứ tự exec test ⇒ "độ khớp exec của thưởng trên mẫu tĩnh không dự đoán được thứ hạng sau train".

**Oracle best-of-9** [val C1] — [report/252 §4](../../report/252_KET_QUA_EXEC_8_MAU_C1_28_9.md): greedy 63,45; oracle SPICE 68,67 (+5,22 [+1,22; +9,36]) · BLEU-4 +7,63 · ROUGE-L +8,84 · CIDEr-D **+9,64 [+5,00; +14,29]**; SPICE hoà ở 33,8% cặp cần phân biệt. Ghi chú của report/332: "oracle CIDEr-D mạnh hơn SPICE ở report/252 nhưng GRPO + CIDEr-D không hơn".

**RGTC target T** [val C1, 79 bước active] — [report/320 §25](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md): SPICE 0,676 · chrF **0,866** · T 0,686 · A2 (0,70S+0,15A+0,075−d) 0,850 · FULL 0,850; FULL − chrF −0,016 [−0,063; +0,032]. "chrF một mình không thua công thức nào có SPICE."

**Log train (H3)**: tỉ lệ nhóm thưởng bằng nhau GRPO + SPICE 22,7% vs CIDEr-D/METEOR/ROUGE-L 16,2–16,7%; KL TB SPICE ~0,011 vs n-gram 0,026–0,033 — [report/320 §17 H3](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md); entropy và nhóm hoà theo lượt ở [report/320 §14.6](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).

**Ứng viên đã sàng nhưng chưa từng train**: SPICE-MATCH, Action-SPICE, FIXED, FIXED+A, Sparse-SPICE, SPIDEr-like, ROUGE-L trên TRAIN-v3 (đều là arm bắt buộc của memo §6, 27 lượt; chỉ SA và chrF đã train) — [report/SA_SPICE_v3_extracted_verified.md §6](../../report/SA_SPICE_v3_extracted_verified.md), [report/333 §11](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md); R0_capped/R2/R3/R4 trên val C1 — [report/332](../../report/332_KAGGLE_CPU_REWARD_SCREEN_8_11.md); `spice_cong`, `ten_loai`, `loai` — [report/320 §16](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md); R5 (SPICE-U rarity), R6/R7 (target contrast), R8, R9 (GDPO) — [report/331 §5.1](../../report/331_DEEP_RESEARCH_GRPO_SPICE_REWARD_2026_11_08.md).

### Inferences
- Thứ hạng sàng offline nhất quán qua ba bộ dữ liệu (SPICE cuối, chrF/n-gram đầu), nhưng ba lần đối chiếu với kết quả sau train đều cho thấy sàng không dự báo thứ hạng (H2 vs test; CIDEr-D oracle vs GRPO + CIDEr-D; chrF > SA trên sàng nhưng SA ≈ chrF trên dev exec, SA > chrF trên văn bản dev). Vì vậy concordance cao không phải điều kiện đủ để chọn phần thưởng thay thế; nó chỉ loại được các phần thưởng có nhiều nhóm hoà.
- Phần lớn lợi ích của SA so SPICE con đến từ việc phá hoà (zero-std 5,79% → 0,96%) chứ không từ thứ tự mới — cùng kết luận với report/332 trên val C1.

### Gaps
- Sàng TRAIN-v3 chỉ đo bước chạm; bước không chạm không có exec, proxy loại thao tác là vòng tròn với verifier A — [report/332](../../report/332_KAGGLE_CPU_REWARD_SCREEN_8_11.md), [report/SA_SPICE_v3_extracted_verified.md §0](../../report/SA_SPICE_v3_extracted_verified.md).
- Chưa có sàng nào đo khả năng phân biệt **phần tử đúng/sai** (stress `wrong_target` thất bại với R4) ngoài RGTC T (không có đóng góp biên).

---

## 3. Phân rã mức tăng exec (sửa loại thao tác vs đổi phần tử) và tác hại ở bước không chạm

### Takeaway
Từ S1, mọi phần thưởng thật đều sửa loại thao tác (phần này SFT tiếp cũng mua được); phần đổi phần tử +41 của ck500 không tái lập qua A/A và hạt 202. Từ SFT-cont (SA-SPICE-v3), mức tăng dev gần như **toàn là đổi phần tử** (sửa loại ròng ≈ 0) — nên thành phần A của SA có rất ít chỗ tác động ở bước chạm. Tác hại ở scroll/back xuất hiện với mọi phần thưởng đã đo (SPICE, CIDEr-D, CIDEr-D + CTG, SA, chrF) và tăng theo mức trôi khỏi điểm xuất phát.

### Cited Findings
- ck500 − S1/101 [test]: ròng +69 bước = **+28 sửa loại thao tác + 41 đổi phần tử** — [report/320 §5](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md) (khớp report/259).
- So S1 theo phần thưởng [test]: ROUGE-L loại +48 / phần tử +20 (p=0,19) · SCST + SPICE +33 / +31 (p=0,017) · CIDEr-D +34 / +18 · METEOR +31 / +21 · xao101 −3 / +3 — [report/320 §14.5](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md). So trực tiếp: ck500 − TB ba độ đo khác: phần tử +0,48 [+0,05; +0,91] p=0,035 (chọn sau khi thấy số); ck500 − ROUGE-L loại thao tác −0,45 [−0,68; −0,23] giữ sau Holm — cùng mục.
- Tái lập: ck500/202 +32 / +5; A/A +20 / +8 ⇒ "phần đổi phần tử +41 chỉ có ở ck500/101" và "câu 'thưởng SPICE giúp đổi đúng phần tử' KHÔNG tái lập" — [report/320 §21 "Phân rã + SPICE theo tuple"](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- ck500 − SFT tiếp [test]: exec +0,49 [−0,09; +1,07] = loại −0,09 + phần tử **+0,58 [+0,04; +1,14]**; SFT tiếp − S1: loại +0,74 [+0,46; +1,05] ⇒ "train thêm … đã mua phần sửa loại thao tác" — [report/320 §19](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **[tự tính, dev]** Phân rã trên DEV-v3 (1.338 bước chạm) so SFT-cont, dùng `executable`/`action_ok` trong `runs/sa_spice_v3/dev/{a,b}/score/score_dev_*_raw.jsonl` (cứu/phá tổng khớp `doc_dev.json`): SA ck500 cứu 40 (loại 4, phần tử 36) / phá 21 (loại 2, phần tử 19) ⇒ ròng loại +2, phần tử +17; SA ck400 cứu 33 (2/31) / phá 15 (2/13) ⇒ loại 0, phần tử +18; chrF ck400 cứu 41 (5/36) / phá 27 (2/25) ⇒ loại +3, phần tử +11. Nguồn số tổng: [runs/sa_spice_v3/dev/doc_dev.json](../../runs/sa_spice_v3/dev/doc_dev.json). SFT-cont trên dev đã đúng loại thao tác ở 97,09% bước chạm — [report/334 §6a](../../report/334_BANG_KET_QUA_TONG_HOP.md).
- Tác hại không chạm ck500 [test]: toàn bộ −1,68 [−2,76; −0,62], scroll **−6,23 [−8,30; −4,31]** (51 phá / 4 cứu; 47 thành câu chạm), back −5,93 [−9,42; −2,58], input_text −2,02; wait +4,55, open_app +1,71 — [report/261 §6](../../report/261_MUOI_BA_COT_CK500_2_10.md). "Một nửa mức tăng action_ok ở bước click được trả lại ở bước không chạm" — cùng mục.
- Cơ chế đã loại / còn đứng: SPICE vẫn thưởng câu scroll cao hơn câu chạm ở bước scroll (66,3 vs 14,0) nên thưởng tại chỗ không đẩy về chạm — [report/261 §6](../../report/261_MUOI_BA_COT_CK500_2_10.md); 37% câu nhắc ck500 là không chạm ⇒ loại giả thuyết "không train trên scroll" — [report/320 §16](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md); **29,4% câu scroll đúng loại và 37,0% câu back đúng loại có SPICE = 0** ("Swipe up" vs "Swipe up"), khi cả câu đúng lẫn câu chạm đều 0 thì "nhóm GRPO không có lợi thế nào để giữ câu cuộn"; [suy] 63% câu nhắc là chạm kéo văn phong về "Click on/Open the" — [report/320 §17 "Bước cuộn và quay lại"](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md). GRPO "lật câu ở các bước sát biên", tương quan mức ban đầu với mức đổi 0,71 — [report/279 §3](../../report/279_TONG_HOP_CTG_GRPO_4_10.md).
- CIDEr-D (A2) và CIDEr-D + CTG (A3) [test không chạm]: scroll 77,62 / 78,68 (S1 83,97, ck500 77,75), back 65,56 / 62,59 ⇒ đổi phần thưởng sang CIDEr-D "không đổi gì trên test" ở scroll (−0,13 [−1,77; +1,51] so ck500) — [report/279 §4g](../../report/279_TONG_HOP_CTG_GRPO_4_10.md); [report/334 §5](../../report/334_BANG_KET_QUA_TONG_HOP.md).
- SA-SPICE-v3/chrF [dev]: tụt ở back (84 → 56–60/104), ở ck500 "28 câu back của SFT-cont thành câu chạm, chỉ 6/28 còn nói back/arrow"; input_text giảm ở SA ck500 (88 → 78) và chrF (→ 75); scroll giữ hoặc tăng nhẹ (227 → 235/237/226 trên 283) — [report/333 §12](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md); [report/334 §6c](../../report/334_BANG_KET_QUA_TONG_HOP.md). Thành phần A (thưởng khớp thao tác) có mặt mà back vẫn tụt.
- Thứ tự tác hại dev theo KL: SA ck400 (KL 0,042) −2,40 < SA ck500 (0,043) −5,55 < chrF ck400 (0,045) −6,90 — [report/333 §11–12](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md) (KL gần như bằng nhau nên đây không phải quan hệ đơn điệu rõ).
- Lịch sử tự sinh làm tác hại không chạm của ck500 lớn thêm: đúng loại không chạm 84,29 → 76,83 — [report/334 §8](../../report/334_BANG_KET_QUA_TONG_HOP.md).

### Inferences
- Vì SFT-cont đã sửa gần hết lỗi loại thao tác ở bước chạm, phần thưởng thay SA (nếu vẫn xuất phát từ SFT-cont) chỉ còn đường đổi phần tử để tăng exec — đúng chỗ mà mọi phần thưởng so câu (SPICE, chrF, R4) đều yếu nhất theo stress test `wrong_target`.
- Tác hại ở back/scroll không do một độ đo cụ thể: nó xuất hiện với SPICE, CIDEr-D, CIDEr-D + CTG, SA (có A) và chrF. Ứng viên giải thích chung còn đứng là dịch chuyển văn phong về câu chạm do đa số câu nhắc là chạm, cộng với việc câu không chạm ngắn có SPICE = 0. Thưởng khớp thao tác với biên độ 0,2·(1 − 0,5) = 0,1 đã không đủ chặn trên dev.

### Gaps
- Chưa có phân rã theo câu nhắc không chạm trong log train (log không lưu câu lấy mẫu) — [report/320 §17](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- Chưa có số test không chạm của SA ck400 và SFT-cont; chưa biết tỉ lệ nhóm "mọi mẫu cùng loại thao tác" ở bước back trong lúc train SA (đại lượng report/331 §6.1 yêu cầu).

---

## 4. Dạng lỗi đã ghi cho từng phần thưởng

### Takeaway
SPICE: hoà nhiều, mù với câu không có tuple, tăng tuple "khuôn" trên AitZ, không tái lập phần đổi phần tử. chrF: trôi KL nhanh, hạ BLEU-4/CIDEr-D/SPICE, hại không chạm nặng nhất. CIDEr-D: tối ưu kém ngay trên chính nó (chưa giải thích). Thành phần action/target: không phân biệt phần tử.

### Cited Findings
- **SPICE hoà / tuple thưa:** SPICE("Scroll down","Scroll down") = 0 và SPICE("Go back","Go back") = 0 — [report/320 §16](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md); tuple câu chuẩn: chạm 3,73 · cuộn 2,50 · quay lại 2,41 · mở app 2,40; 0 tuple đối tượng ở 13,6% câu cuộn, 11,1% câu quay lại, 1,4% câu chạm — [report/320 §15 H5](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md); K_g trung vị 3, 99/249 bước C1 có K_g < 3 — [report/320 §25](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md). Nhóm hoà 22,7% trong log train ck500 — [report/320 §17 H3](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **SPICE vẫn tách loại thao tác ở bước không chạm**: SPICE TB câu đúng loại − sai loại 0,57 (không chạm) vs 0,33 (chạm) ⇒ giả thuyết "thưởng SPICE ít tín hiệu loại thao tác ở bước không chạm" không đứng — [report/320 §15 H5](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **SPICE tuple khuôn (AitZ):** 193/204 tuple khớp thêm của ck500 là tuple phổ biến; ΔF +1,0 có ý nghĩa nhưng exec 37,79 → 37,28 — [report/320 §17 AitZ](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **SPICE ít trôi:** KL TB SPICE ~0,011–0,013 vs GRPO + n-gram 0,026–0,033; "thưởng nhiều hoà làm cập nhật bảo thủ hơn" mới là [suy] — [report/320 §16, §17 H3](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **Không thấy lặp cụm/câu cụt kiểu Liu với ck500** (lặp 2 từ −0,25 [−0,61; +0,10]) — [report/320 §14.7](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **chrF:** KL 0,114 ở ck500 (vượt 0,10) — [report/333 §11](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md); [dev] chrF ck400 − SFT-cont BLEU-4 −5,71*, CIDEr-D −32,19*, SPICE −2,64* (toàn bộ), chrF −0,37 phủ 0; không chạm −6,90 — [report/334 §6c–6d](../../report/334_BANG_KET_QUA_TONG_HOP.md). Câu trùng nguyên văn gold giảm nhiều nhất (706 → 612) — [report/333 §12](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md). Memo đã lường "chrF có thể thưởng trùng chữ sai nghĩa" — [report/331 §5.1 R2](../../report/331_DEEP_RESEARCH_GRPO_SPICE_REWARD_2026_11_08.md).
- **METEOR:** câu dài nhất (+0,59 từ), BLEU-4 −1,60* so ck500 — [report/320 §14.4, §14.7](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **CIDEr-D:** GRPO + CIDEr-D thấp hơn ck500 ngay trên CIDEr-D (−5,53 [−10,21; −1,20]); giả thuyết df/tách từ bị bác (khoảng cách giữ nguyên dưới đúng hàm thưởng, −6,22); không do độ dài/chép câu; còn mở: nhiễu thưởng trong nhóm hoặc nhiễu một hạt — [report/320 §22](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md). CIDEr-D thuộc tính SPICE gần như không đổi (+0,1) — [report/320 §17 H4](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **Thành phần action (hard gate):** R4 gán 0 cho cả câu sai thao tác lẫn `zero_tuple`/`paraphrase`; không tách được `wrong_target` (0,254 < 0,912), bật/tắt (0,943 vs 0,765) — [report/332](../../report/332_KAGGLE_CPU_REWARD_SCREEN_8_11.md). Nhóm mọi mẫu cùng sai thao tác làm gate vô dụng; cộng hằng số không đổi advantage — [report/331 §6.1, §6.3](../../report/331_DEEP_RESEARCH_GRPO_SPICE_REWARD_2026_11_08.md).
- **Verifier action:** câu chuẩn ở bước `wait` khớp action log chỉ 0,4% ⇒ mọi bước wait thành A = 0,5; type 25,9% không suy được — [report/333 §3](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md). Người chấm 40 dòng: 7 dòng lệch Claude/verifier đều là "đường đi khác hợp lý" ⇒ chuyển sang v3 (khác loại → 0,5) — [report/333 §9](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md).
- **Tên phần tử (ten_loai):** câu chuẩn chỉ đạt F1 tên 0,57, 29% câu chuẩn F1 = 0 ⇒ thưởng nhiễu ngay với câu đúng — [report/320 §16](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md); tỉ lệ từ câu chuẩn trùng tên phần tử vàng chỉ 11,5% — [report/320 §15 H1](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **Target contrast (RGTC):** T hoà ở 201/441 cặp, không đổi thứ tự cặp nào khi ghép vào — [report/320 §25](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md); độ phủ Gate B chỉ 10,3% ở bản gốc, 34,8% khi bỏ danh sách role (quyết sau khi thấy số) — [report/320 §24](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- **Người nghe Phi-4 trong thưởng:** [val] SPICE −1,53 [−2,83; −0,22] với SPICE + LR — [report/289 §1](../../report/289_KET_QUA_VAL_LON_288_BAN_4_7_10.md).
- **r_point (GRPO-point):** cổng khai báo tăng +2,56 pp nhưng exec +0,02; 66,7% thay đổi khai báo không tới được câu — [CLAUDE.md khối 6/9](../../CLAUDE.md).

### Inferences
- Phần thưởng nào thêm tín hiệu "mặt chữ" (chrF, METEOR) thì trôi nhanh hơn và làm hỏng độ đo văn bản khác; phần thưởng nhiều hoà (SPICE) thì ít trôi. Đây có thể là lý do SA (80% SPICE trong S khi K_g ≥ 3) sau train ngang chrF về exec nhưng giữ văn bản tốt hơn — một đánh đổi giữa tín hiệu và độ ổn định chưa được đo trực tiếp.
- Mọi thành phần nhắm vào "đúng phần tử" đã thử (tên, target T, `<point>`, người nghe) đều không đổi được exec hoặc không vượt sàng; chưa có phần thưởng nào trong kho cho tín hiệu phần tử mà không dùng bộ trỏ.

### Gaps
- Nguyên nhân CIDEr-D tự tối ưu kém vẫn mở (chưa đo phương sai thưởng trong nhóm theo bước).
- Chưa có phép đo tác hại không chạm cho ROUGE-L, METEOR, SCST, PPO, RLOO trong lưới.

---

## 5. Ý tưởng "phần thưởng kế tiếp" đã viết nhưng chưa thi hành, và các ràng buộc user đặt ra

### Takeaway
Danh sách chờ có: SPICE-MATCH/Action-SPICE/FIXED/FIXED+A/Sparse-SPICE (factorial của memo), SPIDEr-like, ROUGE-L trên TRAIN-v3; BLEU-4, SPIDEr, BERTScore, BCMR, SPICE có cổng loại, tên + loại, CIDEr-R; R5 rarity, R6/R7 target, R8 thay chrF bằng CIDEr-D/METEOR, R9 GDPO; R4-Soft/CE/Balanced; người nghe Phi-4 từ S1; thưởng UI-Venus. Ràng buộc: giữ hướng GRPO + SPICE, không bộ trỏ chấm trong thưởng, không chỉnh hệ số sau khi thấy C1/test, khai mọi lệch protocol; ngân sách không còn là ràng buộc (user 11/11).

### Cited Findings
- Factorial 3×2 + baseline bắt buộc (chrF, SPIDEr-like, ROUGE-L), 27 lượt × 3 seed — [report/SA_SPICE_v3_extracted_verified.md §6](../../report/SA_SPICE_v3_extracted_verified.md). CONFIRM-v3 chỉ mở khi "SA > SPICE-MATCH, SA > Sparse-SPICE", hai arm chưa train — [report/333 §13](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md).
- Memo đã cân nhắc và **không chọn**: Action-SPIDEr (giữ làm baseline), SPICE + ROUGE-L + action ("dễ … bị gọi metric shopping", "không có prior trực tiếp mạnh như SPIDEr"), RGTC — [report/SA_SPICE_v3_extracted_verified.md §0, §15](../../report/SA_SPICE_v3_extracted_verified.md).
- Hệ số 0,8/0,2 là fallback ghi trước; "không thêm hệ số mới sau C1; không sweep weight trên test" — [report/SA_SPICE_v3_extracted_verified.md §3](../../report/SA_SPICE_v3_extracted_verified.md). User phải chấp nhận "kết quả âm, không đổi 0,8/0,2" — [report/333 §7 câu 4](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md).
- Danh sách lượt nên thêm ở trục phần thưởng: BLEU-4, SPIDEr, BERTScore, **BCMR**, **SPICE có cổng loại** (r = SPICE·a, "nghĩ ra sau khi đã thấy số test ck500, phải khai"), **tên phần tử + loại**, người nghe Phi-4 từ S1, chrF, CIDEr-R (chỉ khi CIDEr-D ≥ SPICE) — [report/330 §7](../../report/330_KHAO_SAT_DO_DO_THAY_SPICE_1_11.md); cần Colab: thưởng bằng UI-Venus-7B, LLM giám khảo (user quyết) — [report/330 §8](../../report/330_KHAO_SAT_DO_DO_THAY_SPICE_1_11.md).
- R0–R9 và các ablation phạt độ dài; R4-Hard/Soft/CE/Balanced để xử lý nhóm all-wrong action — [report/331 §5.1, §6.3](../../report/331_DEEP_RESEARCH_GRPO_SPICE_REWARD_2026_11_08.md). Chỉ số phải log: `frac_reward_zero_std`, % nhóm all-wrong/all-correct action, % cặp hoà, `E[A_i·(exec_i − mean)]` — [report/331 §6.2](../../report/331_DEEP_RESEARCH_GRPO_SPICE_REWARD_2026_11_08.md).
- CTG A4 (lấy mẫu lại câu nhắc theo lớp) và A7 (CIDEr-D + thưởng đúng loại +1) chưa chạy — [report/279 §1, §4g](../../report/279_TONG_HOP_CTG_GRPO_4_10.md). T5 (thưởng chỉ đúng loại, để giải thích), T6 (SPICE không phạt) — [report/326 §4](../../report/326_BAN_GIAO_LUOI_RL_1_11.md). λ = 2 cho người nghe chưa chạy — [CLAUDE.md hàng 288](../../CLAUDE.md).
- Checklist rút từ 6 bài reward 2025–2026: so SPICE-only/chrF-only/fixed/adaptive, phân tầng K_g = 0,1,2,≥3, train policy thật, DEV + CONFIRM + nhiều seed, "báo chrF dù bất lợi"; "SASI … vẫn là candidate … chrF-only vẫn cao hơn và chưa có kết quả policy sau training" — [report/335 §8, §10](../../report/335_TONG_HOP_6_PAPER_REWARD_2025_2026.md). Bài gần nhất GUI-G² (AAAI 2026): "adaptive phải thắng fixed" — [report/335 §7, §9](../../report/335_TONG_HOP_6_PAPER_REWARD_2025_2026.md) (venue chép từ ảnh, chưa kiểm lại ở nguồn trong phạm vi tác vụ này).
- **Ràng buộc user:**
  - Không bộ trỏ chấm trong thưởng (Goodhart): "Dùng UGround = tối ưu đúng dụng cụ chấm" — [report/330 §5](../../report/330_KHAO_SAT_DO_DO_THAY_SPICE_1_11.md); "Em chủ động giữ reward reference/rule-based trong training" — [report/331 dòng 521](../../report/331_DEEP_RESEARCH_GRPO_SPICE_REWARD_2026_11_08.md); GRPO-point "không bộ trỏ nào trong phần thưởng ⇒ không Goodhart lên UGround" — [CLAUDE.md khối 6/9](../../CLAUDE.md).
  - Hướng phương pháp: user chốt "PHƯƠNG PHÁP ĐÓNG GÓP = GRPO THƯỞNG SPICE (ck500)" 4/10 — [CLAUDE.md](../../CLAUDE.md); memo chọn SA vì "vẫn đúng hướng GRPO+SPICE" — [report/SA_SPICE_v3_extracted_verified.md §15](../../report/SA_SPICE_v3_extracted_verified.md).
  - "Ngân sách thì ko cần lo" (11/11) — [report/333 §8](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md); 1/11: "đừng sợ tốn tính toán. Tạm bỏ chạy nhiều hạt giống" — [report/326 §1](../../report/326_BAN_GIAO_LUOI_RL_1_11.md).
  - Seed 101 "cho dễ báo cáo", lệch memo (401/503/907) — [report/333 §11](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md).
  - Thầy đòi so họ RL + độ đo thưởng + giải thích vì sao, bảo vệ dời 3/2027; "không được hứa trước GRPO + SPICE đứng đầu" — [report/326 §1, §7](../../report/326_BAN_GIAO_LUOI_RL_1_11.md). Nếu GRPO + SPICE không đứng đầu ở cả hai hạt thì "đưa user quyết có đổi phương pháp chính hay không" — [report/323 §8.7](../../report/323_DEBATE_VA_ACTION_KHAO_SAT_GRPO_SPICE_ACE_1_11.md).
  - Non-inferiority không chạm của memo: toàn bộ −1, scroll −2, back −2 (cận dưới một phía) — [report/SA_SPICE_v3_extracted_verified.md §10](../../report/SA_SPICE_v3_extracted_verified.md).

### Inferences
- Bất kỳ phần thưởng thay thế nào được chọn *sau khi* thấy dev/test của SA sẽ phải khai là hậu nghiệm; memo đã định danh trước một tập ứng viên (factorial + 3 baseline) nên chọn trong tập đó ít rủi ro "metric shopping" hơn tạo công thức mới.
- Ràng buộc Goodhart loại mọi phần thưởng dùng UGround; UI-Venus/Phi-4 được phép nhưng cùng họ Qwen (UI-Venus) hoặc đã thấy kết quả âm trên văn bản (Phi-4, val).

### Gaps
- Không thấy trong kho quyết định của user cho memo §16 câu 5 (người gán nhãn audit / human eval 300 prompt) ngoài việc giao Claude chấm thay — [report/333 §8](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md).
- Không tìm thấy kết quả sàng cho BCMR, CIDEr-R, R5 rarity.

---

## 6. Chẩn đoán offline bổ sung trên dữ liệu sàng TRAIN-v3 (tự tính hôm nay)

### Takeaway
Trên 622 nhóm bước chạm của sàng TRAIN-v3, **tăng trọng số SPICE so với chrF làm concordance giảm đơn điệu** (0,794 ở trọng số 0 → 0,676 ở trọng số 1); không ứng viên nào có SPICE vượt chrF; thêm A cho chrF gần như không đổi gì (+0,002, phủ 0). Ứng viên có SPICE tốt nhất là 0,8·(0,5s + 0,5c) + 0,2A (0,7838, hơn SA +0,013 có ý nghĩa, kém chrF −0,010 phủ 0). Phân tầng K_g: chrF ≥ SA ở mọi tầng có đủ cỡ mẫu. Đây là **chẩn đoán offline**, đã có tiền lệ không dự báo được kết quả sau train.

### Cited Findings
**Phương pháp [tự tính].** Script `/tmp/claude-1000/-mnt-d-Master-Thesis/a826d459-2edf-44cb-b931-82b4bcbff84c/scratchpad/screen_extra.py` (scratchpad, có thể bị xoá; kết quả `screen_extra.json` cùng thư mục), `python3 -I`, ~6 phút CPU. Đầu vào: [runs/sa_spice_v3/screen/out/sa3_screen_buoc.jsonl](../../runs/sa_spice_v3/screen/out/sa3_screen_buoc.jsonl) (9 arm reward + A cho greedy và 8 mẫu mỗi bước), câu mẫu [runs/sa_spice_v3/mau_k1/mau_{0,1}.jsonl](../../runs/sa_spice_v3/mau_k1/), exec [runs/sa_spice_v3/cham_k2/*/score/score_k{1..8}_raw.jsonl](../../runs/sa_spice_v3/cham_k2/), gold/package [runs/sa_spice_v3/split/train_v3.jsonl](../../runs/sa_spice_v3/split/train_v3.jsonl). Tệp bước không lưu s, c riêng nên tôi giải ngược: d = phạt độ dài tính từ câu (đúng hàm `penalty` của [harness/sa3_reward_screen.py](../../harness/sa3_reward_screen.py)), s = (SPICE-MATCH − 0,1 + d)/0,8, c = (FIXED − 0,1 + d − 0,64s)/0,16 (không arm nào bị clip ở hai công thức này); kiểm tái dựng chrF và Action-SPICE lệch tối đa 1,3e−15. ROUGE-L thô chỉ khôi phục được khi arm ROUGE-L > 0 (159 mẫu bị clip về 0 được đặt rl = 0). α (⇒ K_g) suy từ arm Sparse-SPICE theo median trong bước. Concordance/zero-std/oracle đúng định nghĩa `group_stats` (hoà = 0,5, sai số hoà 1e−12); KTC95 bootstrap cụm package, 263 cụm, **B = 1.000**, seed 20261115. Tái lập: 9 arm gốc khớp report/333 §10 (SA 0,7708, chrF 0,7941; SPICE-MATCH 0,6768 so 0,6766 do khác dung sai hoà).

| ứng viên [train-screen, tự tính] | concordance | cặp hoà | zero-std | oracle pp | − chrF [KTC95] | − SA-SPICE-v3 [KTC95] |
|---|---|---|---|---|---|---|
| chrF (đối chứng) | 0,7941 | 0,2% | 1,13% | +10,85 | – | +0,023 [+0,003; +0,045] |
| N3: clip(0,8c + 0,2A − d) (chrF + thưởng khớp thao tác) | **0,7961** | 0,2% | 1,13% | **+11,01** | +0,002 [−0,005; +0,008] | +0,025 [+0,006; +0,047] |
| N10: clip(0,5c + 0,5·ROUGE-L − d) | **0,7967** | 0,2% | 1,29% | +10,37 | +0,003 [−0,010; +0,016] | +0,026 [+0,005; +0,049] |
| N6: clip(c·A − d) | 0,7937 | 0,2% | 1,13% | +10,85 | −0,000 [−0,010; +0,007] | +0,023 [+0,004; +0,044] |
| N2: clip(0,8(0,5s + 0,5c) + 0,2A − d) | 0,7838 | 0,2% | 0,96% | +10,05 | −0,010 [−0,026; +0,006] | **+0,013 [+0,002; +0,028]** |
| ROUGE-L (arm gốc) | 0,7802 | 4,3% | 2,25% | +9,93 | −0,014 [−0,037; +0,007] | +0,009 [−0,016; +0,034] |
| SPIDEr-like (arm gốc) | 0,7788 | 1,3% | 1,93% | +9,73 | −0,015 [−0,043; +0,011] | +0,008 [−0,012; +0,029] |
| N11: clip((s + c + rl)/3 − d) | 0,7771 | 0,2% | 1,13% | +9,89 | −0,017 [−0,035; −0,000] | +0,006 [−0,007; +0,021] |
| SA-SPICE-v3 | 0,7708 | 0,2% | 0,96% | +9,08 | −0,023 [−0,045; −0,003] | – |
| N1: clip(0,5s + 0,5c − d) (không A) | 0,7701 | 0,2% | 1,13% | +9,73 | −0,024 [−0,044; −0,005] | −0,001 [−0,010; +0,009] |
| N12: trung bình hạng (SPICE, chrF) trong nhóm | 0,7659 | 2,3% | 1,13% | +9,41 | −0,028 [−0,044; −0,012] | −0,005 [−0,018; +0,008] |
| N8: clip(0,5s + 0,5·ROUGE-L − d) | 0,7589 | 3,1% | 2,09% | +9,08 | −0,035 [−0,062; −0,011] | −0,012 [−0,030; +0,005] |
| N9: chrF nếu K_g = 0, ngược lại 0,8s + 0,2c | 0,7502 | 0,2% | 1,29% | +8,60 | −0,044 [−0,068; −0,020] | −0,021 [−0,032; −0,010] |
| N4: SPICE, phá hoà theo thứ tự từ điển bằng chrF | 0,7319 | 0,2% | 0,96% | +8,28 | −0,062 [−0,090; −0,035] | −0,039 [−0,054; −0,022] |
| N7: clip(√(s·c) − d) | 0,6902 | 29,9% | 11,90% | +8,52 | −0,104 [−0,132; −0,076] | −0,081 [−0,104; −0,058] |
| N5: clip(s·A − d) (SPICE có cổng thao tác) | 0,6795 | 31,7% | 12,70% | +7,65 | −0,115 [−0,146; −0,085] | −0,091 [−0,115; −0,069] |

Quét trọng số SPICE w trong clip(w·s + (1−w)·c − d) [tự tính; **chẩn đoán, memo §3 cấm dùng để chỉnh hệ số**]: w = 0 → 0,7941 · 0,2 → 0,7889 · 0,4 → 0,7765 · 0,6 → 0,7647 · 0,8 → 0,7488 · 1,0 → 0,6761. Cùng quét với + 0,2A: 0,7961 · 0,7905 · 0,7865 · 0,7731 · 0,7567 · 0,7163. Mọi w ≥ 0,4 thấp hơn chrF với KTC loại 0 (không A) và mọi w ≥ 0,6 (có A).

Phân tầng K_g (622 nhóm chạm; K suy được ở 616) [tự tính] — concordance:

| K_g | n nhóm | SPICE-MATCH (cặp hoà) | chrF | FIXED | Sparse-SPICE | SA-SPICE-v3 | N3 chrF + A | ROUGE-L |
|---|---|---|---|---|---|---|---|---|
| 0 | 3 | 0,125 | 1,000 | 0,438 | 1,000 | 1,000 | 1,000 | 0,750 |
| 1 | 28 | 0,628 (33,8%) | 0,662 | 0,617 | 0,692 | 0,699 | 0,699 | 0,662 |
| 2 | 192 | 0,597 (31,6%) | **0,771** | 0,698 | 0,728 | 0,732 | 0,772 | 0,745 |
| ≥3 | 393 | 0,731 (20,2%) | **0,815** | 0,787 | 0,787 | 0,796 | 0,815 | 0,809 |

### Inferences
- Trên bước chạm, K_g = 0 gần như không xuất hiện (3/622 nhóm) nên cơ chế "sparse-aware" của SA chỉ thực sự đổi được gì ở K_g = 1–2 (α 0,27–0,53); ở K_g ≥ 3 (63% nhóm) SA = FIXED + A với 80% SPICE, đúng vùng mà SPICE thua chrF rõ nhất.
- Thưởng khớp thao tác A thêm concordance khi SPICE chiếm tỉ trọng lớn (Action-SPICE − SPICE-MATCH ≈ +0,04) nhưng gần như 0 khi nền là chrF (N3 − chrF +0,002), vì từ SFT-cont 75% mẫu đã A = 1 và chrF đã phạt sai loại thao tác qua mặt chữ.
- Cổng nhân (s·A) và trung bình nhân (√(s·c)) giữ nguyên hoà của SPICE (zero-std ~12–13%) ⇒ loại; phá hoà theo từ điển cũng không cứu (0,732).
- Nếu phải giữ SPICE trong thưởng (ràng buộc "GRPO + SPICE"), bằng chứng offline nghiêng về trọng số SPICE ≤ 0,5 so với chrF, kèm A; nhưng đây là suy luận sau khi thấy số trên chính dữ liệu sàng, và chính report/333 nói sàng "chỉ chẩn đoán", memo cấm chỉnh hệ số theo sàng.

### Gaps
- Không có exec cho bước không chạm trong dữ liệu sàng nên mọi ứng viên trên chỉ đánh giá ở bước chạm — đúng chỗ ít liên quan nhất tới tác hại back/scroll.
- Bootstrap B = 1.000 (không phải 2.000 như sàng gốc); ROUGE-L thô bị clip ở 159 mẫu nên N8/N10/N11 hơi lệch; N12 tính hạng trên arm đã trừ d.
- Concordance trên mẫu tĩnh của SFT-cont không phản ánh phân bố mẫu sau khi policy đã trôi.

---

## 7. Hàm ý cho việc chọn phần thưởng thay SA-SPICE-v3

### Takeaway
Bằng chứng nội bộ **không ủng hộ** việc thay SA bằng một biến thể SPICE nặng hơn (SPICE-MATCH, Action-SPICE, SPICE·A, √(s·c), phá hoà từ điển): tất cả thua SA và chrF trên sàng, và SPICE thuần sau train không tái lập exec. Bằng chứng **ủng hộ có điều kiện**: (a) ROUGE-L — phần thưởng duy nhất có exec test ngang ck500 và hơn A/A sau Holm; (b) chrF hoặc chrF + A — đứng đầu mọi sàng, nhưng trôi KL và hại không chạm nặng nhất trên dev; (c) nếu buộc giữ SPICE, trộn SPICE với chrF ở tỉ trọng thấp hơn (≤ 0,5) kèm A. Rủi ro lớn nhất không nằm ở công thức mà ở biến thiên giữa lượt train (~0,7–0,9 exec), tác hại back/scroll chung cho mọi phần thưởng, và việc sàng offline không dự báo thứ hạng sau train.

### Cited Findings
- Thứ hạng exec test trong lưới cùng mã: ROUGE-L +0,90† và SCST + SPICE +0,81† hơn A/A; ck500 − A/A +0,92† — [report/334 Bảng 2.3, 1.3](../../report/334_BANG_KET_QUA_TONG_HOP.md). ROUGE-L tăng chủ yếu nhờ sửa loại thao tác (+48) — [report/320 §14.5](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md).
- Sàng TRAIN-v3: chrF > SA (−0,023 [−0,046; −0,002]) — [report/333 §10](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md); sau train dev SA ck400 − chrF ck400 exec +0,30 [−0,57; +1,20] và văn bản nghiêng về SA — [report/334 §6b, §6d](../../report/334_BANG_KET_QUA_TONG_HOP.md).
- Sàng offline không dự báo sau train: [report/320 §16](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md), [report/332 gạch cuối](../../report/332_KAGGLE_CPU_REWARD_SCREEN_8_11.md).
- Biến thiên giữa lượt: A/A − ck500 −0,92*; ck500 − ck500/202 +0,72* — [report/320 §21](../../report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md). Val/dev phóng đại khoảng cách (val − test +2,8 đến +8,3 exec; ck500 − S1 +2,81 val vs +1,55 test) — [report/334 §11](../../report/334_BANG_KET_QUA_TONG_HOP.md).
- Tác hại không chạm với mọi phần thưởng đã đo — [report/261 §6](../../report/261_MUOI_BA_COT_CK500_2_10.md), [report/279 §4g](../../report/279_TONG_HOP_CTG_GRPO_4_10.md), [report/333 §12](../../report/333_SA_SPICE_V3_PREFLIGHT_11_11.md). CTG (thưởng/advantage theo loại thao tác) không gỡ được scroll và làm back tệ hơn — [report/279 §4g](../../report/279_TONG_HOP_CTG_GRPO_4_10.md).
- Không phần thưởng nào hơn SFT tiếp có ý nghĩa trên test — [report/334 Bảng 2.3 cột "− SFT tiếp"](../../report/334_BANG_KET_QUA_TONG_HOP.md).
- Từ SFT-cont, dev gain gần như toàn phần tử (SA ck400 loại 0 / phần tử +18) [tự tính, dev, mục 3].

### Inferences
- **Được ủng hộ:**
  1. *GRPO + ROUGE-L (arm baseline đã đăng ký trong memo §6.2)*: có exec test tốt nhất trong lưới cùng mã, văn bản thắng ck500 6/7, ít hoà (4,3% cặp) và nằm trong tập ứng viên khai trước nên không phải metric shopping. Nhưng: cơ chế tăng là sửa loại thao tác, mà từ SFT-cont phần này đã bão hoà; chưa có số không chạm.
  2. *chrF + A (N3)* hoặc *0,5c + 0,5·ROUGE-L*: đứng đầu sàng; nhưng chrF đơn thuần đã train và trôi KL quá 0,10 ở ck500, hại back −6,90 trên dev ⇒ nếu dùng phải kèm cơ chế giữ không chạm và chọn điểm lưu sớm.
  3. *Giữ SPICE nhưng giảm tỉ trọng*: N2 = 0,8(0,5s + 0,5c) + 0,2A là biến thể có SPICE tốt nhất trên sàng (hơn SA có ý nghĩa, ngang chrF); phải khai là hệ số chọn sau khi thấy sàng (memo §3).
- **Bị bác hoặc yếu:** SPICE thuần / SPICE-MATCH / Action-SPICE / SPICE·A (cổng) / √(s·c) / phá hoà từ điển (thua sàng, nhiều hoà); target contrast RGTC (đóng góp biên 0); tên phần tử (nhiễu cả với câu chuẩn); CIDEr-D (không tối ưu được chính nó, thua ck500 ở exec); người nghe Phi-4 (hại SPICE trên val); r_point (không truyền tới câu). Sparse routing theo K_g có tác dụng nhỏ ở bước chạm vì K_g = 0 hiếm (3/622 nhóm).
- **Rủi ro chính còn mở:**
  1. Một hạt giống: mọi chênh giữa phần thưởng ≤ ~1 exec nằm trong biến thiên giữa lượt train; muốn khẳng định phần thưởng thay thế cần ≥ 2–3 seed (memo đòi 3).
  2. Tác hại back/scroll không do độ đo cụ thể; không phần thưởng nào trong kho đã chứng minh chặn được (CTG thất bại, A 0,2 không đủ). Phần thưởng thay thế cần một can thiệp riêng cho bước không chạm (A7, lấy mẫu cân bằng A4, R4-Balanced, hoặc chọn điểm lưu theo tiêu chí khả thi) — đều chưa chạy.
  3. Không có tín hiệu "đúng phần tử" không dùng bộ trỏ: mọi phần thưởng so câu không tách `wrong_target`; ràng buộc Goodhart cấm UGround trong thưởng.
  4. Sàng offline sai thứ hạng ít nhất ba lần; dev phóng đại khoảng cách so test (+1,26 ở ck500 − S1). Chọn phần thưởng thay thế bằng sàng hoặc dev đều phải khai và xác nhận trên test/CONFIRM-v3.
  5. Điểm xuất phát SFT-cont/TRAIN-v3 khác lưới S1 ⇒ không ghép cặp được với ck500 (report/333 §11); SA test (ck400) còn chờ, nên mọi quyết định "SA kém" hiện chưa có căn cứ test.

### Gaps
- Chưa có số test SA ck400 (exec, không chạm) — quyết định "SA underperforms" chưa đo được.
- Chưa có GRPO + ROUGE-L hay chrF + A xuất phát từ SFT-cont trên TRAIN-v3 với số dev/test, nên chưa biết lợi thế ROUGE-L từ S1 (chủ yếu sửa loại thao tác) có chuyển sang điểm xuất phát đã sửa loại hay không.
- Không có hạt giống thứ hai của ROUGE-L, SCST + SPICE.
