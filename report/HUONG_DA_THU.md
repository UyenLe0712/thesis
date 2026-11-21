# CÁC HƯỚNG ĐÃ THỬ — đọc trước khi đề xuất, viết runbook/mã, hay đẩy GPU (cập nhật 21/11/2026)

File này được `CLAUDE.md` nạp tự động (`@report/HUONG_DA_THU.md`) nên mọi phiên đều thấy.

## Luật bắt buộc cho trợ lý

1. **Trước khi đề xuất một hướng mới**, hoặc trước khi viết mã/runbook/notebook cho một hướng, **tra file này**.
   Trùng, kể cả đổi tên hay đổi chút cấu hình (đổi lr, đổi số mẫu, đổi checkpoint xuất phát), thì phải nói với user:
   *"Hướng này đã thử ngày …, kết quả …, dừng vì …"*. Chỉ đề xuất lại khi nêu được **một điểm khác cụ thể** đánh
   vào đúng lý do đã dừng (cột "muốn thử lại phải"). Không có điểm khác thì **không đề xuất**.
2. Mục 0 là các câu hỏi đã có đáp án bằng số. Đừng đề xuất lại các "ý tưởng hiển nhiên" ở đó.
3. Số ở đây chép từ report gốc. Trích vào bài thì mở report gốc kiểm lại. Số **[val]** là số trên tập kiểm định, cấm trích.
4. Có kết quả mới (một hướng xong hoặc dừng) thì **thêm vào đây** cùng lúc với `report/320` và `report/334`.
5. Dọn 15/11 theo luật user: **chỉ xoá đồ của hướng KHÔNG ra số test / chỉ ở mức phụ lục**, gồm 288 người nghe [val],
   C1 gate, FGRB, TFVF, TRIAD, RA-GRPO G0, VIS-SFT loss val, RA-SFT cont và `_scripts/{288,289,312}`. Mọi thứ có số
   trong luận văn, trong `report/334`, hoặc hay dùng thì **giữ**. Lấy lại đồ đã xoá:
   - phần trong git: `git checkout 24959e6^ -- <đường dẫn>`;
   - phần ngoài git: Release `stopped-fgrb-tage-v1`, `stopped-misc-v1` (`gh release download <tag>`).

**Mốc số test** (4.463 bước chạm, exec chấm bằng UGround):
- câu chuẩn 75,73 · S1/101 59,11 · S1/202 59,6 · Base 47,59;
- sàn câu rỗng nghĩa 12,0 [lát 800];
- MDE ghép cặp ~2,1;
- hai lượt GRPO cùng công thức lệch 0,72–0,92 ⇒ **chênh dưới 1 điểm ở một hạt là không phân biệt được**.

Mọi số test chỉ một hạt, trừ S1 và ck500 (hai hạt).

---

## 0. Câu hỏi hay bị hỏi lại — đã có đáp án

| câu hỏi / đề xuất | đáp án đã đo | nguồn |
|---|---|---|
| Đổi sang prompting, không train? | Thầy bác 19/7, bắt buộc train mô hình. Khung DG1/DG2 (ReOrder-Tutor, ScreenSpot, GPT-4o E2E) đã chết. | memory advisor-pivot, CLAUDE.md |
| Đổi backbone lớn hơn (Qwen3-VL-4B, Qwen2.5-VL-7B train)? | Không (user 30/8). Trần bị chặn bởi độ phủ khối ứng viên, đổi backbone mua tối đa ~2 điểm, 4B chưa từng chạy, kịch bản xấu 112–148 h. Qwen2.5-VL-7B **prompting** làm mốc ngoài: exec 51,5. | CLAUDE.md 30/8, report/320 G12 |
| Đổi bộ trỏ mạnh hơn để điểm cao hơn? | UI-Venus-7B (ScreenSpot cao hơn) cho điểm **thấp hơn** ở cả ba nhánh. 72% ca thước mù là bộ trỏ lệch quá 14%. Hợp nhất hai bộ trỏ nâng đều mọi nhánh, tỉ lệ không đổi. | CLAUDE.md 30/8, report/138 |
| Đổi luật chấm cho số cao (±14%, AitW mọi khung)? | Tiêu đề vẫn exec. D.3 và AitW đầy đủ (77,3) báo kèm, AitW mọi khung (85,0) chỉ là cận trên. d14: 86% mức tăng là thứ câu rỗng nghĩa cũng lấy được. AitW mọi khung có sàn câu rỗng 41,6. | report/140, 151 §6, CLAUDE.md 14/9 |
| Dùng người nghe khác (Pixtral, Phi-4) làm thước chính? | Phi-4: trần chỉ 54,9 nên không làm tiêu đề, chỉ để đóng đòn "cùng họ Qwen". Pixtral: 8,0 do lỗi định dạng. | report/155 |
| Đưa OCR / cây trợ năng vào đầu vào? Vá tên bằng OCR? | Bác. 68,6% tên mô hình sinh **đã là chuỗi thật** trên màn, chỉ là chuỗi của **sai** phần tử. | report/151 §2.2 |
| Chấm tay 100 câu? | User quyết không làm (6/9). | CLAUDE.md |
| Train SFT thêm epoch / SFT tiếp là đủ? | SFT tiếp cùng câu nhắc: 60,16, − S1 +1,05. ck500 − SFT tiếp chỉ +0,49 p=0,11. Nhánh so sánh này đã có, không cần chạy lại. | report/320 §18 |
| Thưởng GRPO bằng bộ trỏ (UGround) hay người nghe? | Người nghe Phi-4 (288) không qua sàng +0,5 [val]. Thưởng bằng bộ trỏ dùng để chấm là Goodhart; dự án cố ý **không** có bộ trỏ trong thưởng. | report/289 |
| Gộp nhiều mô hình ở đầu ra / chọn câu tốt nhất lúc suy luận (MBR, reranker, τ)? | Oracle 8 nhánh 72,8 nhưng mọi bộ chọn không-oracle ≤ 60,45. MBR thua S1. τ: null thắng. Selector màn sau thua greedy. | report/151, 208, 142, 233 |
| Chạy hạt giống 202 cho hướng X? | Chỉ khi hạt 101 vượt mốc so có ý nghĩa. S2/202 không chạy (user 23/8, vĩnh viễn). | report/106 x1, x20c |
| L4 hay A100? | So theo đơn vị mỗi lượt. Giờ L4 ≤ 1,5× giờ A100 thì chọn L4/T4. Pha CPU/IO không chạy trên A100. | CLAUDE.md thủ tục chọn máy |

---

## 1. Đang dùng / phương pháp hiện hành (KHÔNG phải hướng đã bỏ)

| hướng | trạng thái | số chính (test) | nguồn |
|---|---|---|---|
| **S1** (SFT trơn Qwen2.5-VL-3B QLoRA, hai hạt) | nền của mọi nhánh | 59,11 / 59,6; − Base +11,5 | report/119 |
| **GRPO + SPICE từ S1 (ck500)**: G=8, KL 0,04, lr 1e-5, 500 update, thưởng SPICE − 0,02·phạt dài, 1.000 câu nhắc | phương pháp đề xuất trong luận văn | exec 60,65; − S1/101 +1,55 [+0,80; +2,33]; hạt 202 +0,83; trung bình hai hạt +1,19. Bước không chạm: scroll 83,97 → 77,75 (phải khai). Lượt A/A train lại 59,74, **không tái lập** (khác bước 1: thưởng 0,473 vs 0,223; khác phiên bản thư viện). Phần tái lập được là sửa loại thao tác (+20…+32 bước); "đổi đúng phần tử +41" chỉ có ở một lượt. | report/259, 261, 320 §14 §21, 328 |
| **ACE / R3** (ck500 + luật ghép câu `ra_k4` khi trùng ví dụ ∧ cùng loại thao tác) | mở rộng trong luận văn | 7/7 độ đo văn bản hơn ck500; exec 60,68 ≈ ck500 | report/304 §4–5 |
| **SFT-cont** (S1 + SFT tiếp trên TRAIN-v3) | điểm xuất phát nhánh SA | DEV-v3 62,93 [val] | report/333 |
| **GRPO + SA-SPICE-v3 từ SFT-cont, ck400**. Thưởng clip(0,8·[α·SPICE+(1−α)·chrF/100] + 0,2·A − d) | kết quả mới nhất, một hạt | exec **61,21**; − SFT tiếp +1,05 p=7e−4; − ck500 +0,56 p=0,069 (không ý nghĩa); − S1 +2,11. **Back không chạm 71,1 → 58,5** (phải khai). Văn bản: cao nhất METEOR 38,90 / ROUGE-L 69,31 / chrF 64,40; SPICE không tăng. Debate sau test: **không đổi reward**, chữa back ngoài reward. | report/320 §29, 333, `research_notes/Debate SA SPICE v3 sau test/03_phan_quyet.md` |
| **SPICE-MATCH** (SPICE thuần từ SFT-cont, ablation của SA) | train 16/11 (Colab L4 fp16), DEV trượt khả thi (không chạm −3,75), test ck400 vẫn chấm (user) | test exec **60,88**; − SA ck400 −0,34 ns; − SFT tiếp +0,72*. Văn bản: hơn SA ở BLEU-4/CIDEr-D/SPICE/BERTScore (*), SA chỉ hơn chrF. Không chạm 83,57 (SA 84,05), back −14,8 vs −12,6 ⇒ **composite không mua được gì rõ ràng so SPICE thuần** | report/333 §15–16 |
| Thước: exec (tiêu đề) · D.3 67,0 · AitW đầy đủ 77,3 (cận trên 85,0) · độ đo văn bản COCO + chrF + BERTScore · Phi-4 SoM · UI-Venus | chốt, đừng mở lại | | CLAUDE.md 13/9, 14/9 |

**Đang chạy (đợt B5, 20–21/11, `report/337`)** — xem §2e; đừng đề xuất lại như ý mới, đợi số test:
Dr.GRPO đầy đủ · DAPO · GSPO · GRPO μ=2 · REINFORCE++ lô 64 · DPO trực tuyến · GRPO + chrF / BLEU-4 / SPIDEr /
BERTScore từ S1.

Việc **chưa thử, đang chờ user** ở `report/336`:
- SA hạt 401/503;
- SA + câu nhắc phân tầng cho back;
- Sparse-SPICE;
- A2C (mới probe, chưa có số) / DQN / TRPO / MIXER / MRT;
- các họ RL mới chỉ qua selftest CPU, chưa train: Quark, ES trên LoRA, MIXER, BCMR, MRT, SPG, RLCE, SeqGAN,
  RAML, CEM (`_bundles/moi_b1`, `moi_b2`; `runs/luoi/smoke_6_11`);
- thưởng đã viết nhưng chưa train (xem §2d): `spice_cong`, `ten_loai`, `loai`, T6 `spice_kp`.

Những việc này **không** nằm trong danh sách đã thử.

---

## 2. Đã thử và DỪNG

Cách đọc: *ý tưởng → cách làm → số → vì sao dừng → muốn thử lại phải…*

### 2a. Giai đoạn đầu (tháng 7–8): khung đề tài, đích sinh

| hướng | đã làm và kết quả | vì sao dừng | muốn thử lại phải |
|---|---|---|---|
| Prompting zero/few-shot (DG1/DG2: ReOrder-Tutor, Copeland, MobileViews, ScreenSpot, GPT-4o E2E) | khung luận văn tới 19/7 | thầy bác: phải train mô hình | — (không thử lại) |
| Faithfulness trên MobileViews (đóng góp phụ, report/103) | chỉ là kế hoạch, chưa từng có số | 106+ thay thế | — |
| Giám sát chú ý (attention supervision) | tra tài liệu 1/8 | KLAL đã lên WACV 2026 ⇒ mất tính mới | — |
| DPO cặp hàng xóm + người nghe trong vòng (29/7) | bị loại khi chốt trụ | không giữ được đóng góp mô hình | — |
| RFT tự lọc | hạ xuống tuỳ chọn 29/7, không chạy | | |
| Đảo nguồn tên sang OCR-trước | bác 5/8 | ưu thế của OCR là **lọc rác** (11/12 ca), không phải thứ tự ⇒ áp cổng `clean_a11y` | — |
| TD-ROI | chết trong debate 23/8 | gold action không vào prompt | — |

### 2b. Descriptor, ORPO, khối ứng viên (tháng 8–9)

| hướng | đã làm và kết quả (test) | vì sao dừng | muốn thử lại phải |
|---|---|---|---|
| **S2**: đích `<desc>[vai trò \| tên \| <point> \| dấu hiệu]</desc>` rồi mới tới câu | exec 57,2; − S1 −1,93 [−3,08; −0,78], âm dưới cả UGround lẫn UI-Venus | gây hại một hạt; nhóm 325 bước đoán sai loại thao tác chiếm 34% chênh lệch; Base đúng loại nhiều hơn mọi bản SFT | đổi cách gắn khai báo cho bước không chạm; nhưng S2/202 cấm chạy |
| S2r (tiền tố sai cùng độ dài), S2-nopoint | không train | ô toạ độ là ô gánh (+1,12), ô tên chỉ +0,54; s2r thiết kế để thua; S2-nopoint đắt gấp đôi MIN | — |
| **MIN-DESC** (ORPO tầng khai báo từ S2, câu y hệt chỉ đổi `<desc>`) | 60,05; − CE2-S2 +0,63 p=0,011; − S1 +0,94 p=0,11 | dưới MDE; 78–88% mức tăng thuộc nhánh so sánh SFT thuần (CE2) | — |
| MIN-ONPOLICY (cặp âm từ khai báo sai của chính S2) | eligibility 3,3% < 25% ⇒ không train | lỗi khai báo **lưỡng cực** (trung vị lệch 351 px, 76,5% ngoài dải 80–350), không phải lẫn hai nút cạnh nhau | không có đường cứu: cổng là tỉ lệ, không phải số lượng |
| `gui_orpo_hard`, ORPO tầng câu, `gui_sft_match` | không chạy | ORPO đã đo được +0,63; trần ORPO câu 4,80 là hiệu ứng chọn mẫu (đổi lát còn −0,65); phản thực `gui_sft_match` 59,44 < 60,07 | — |
| **`gui_sel`** (khối ≤40 ứng viên + đầu chọn `<sel>`) | exec 56,13; cổng G6 57,5 < 63,6 | bỏ cuộc quá mức 27% (khi chọn thì 71,4); khối càng đông càng bỏ cuộc | — |
| Ngưỡng τ cho `gui_sel` (sequence score) | null thắng (tốt nhất +8/1.400) | bước bỏ cuộc mù với likelihood (AUC 0,69–0,72) | — |
| **GRPO `<point>`** (thưởng toạ độ tự khai ±14% từ MIN) | khai báo +2,56 p=1e−8 nhưng exec **+0,02** (60,07) | 66,7% thay đổi khai báo không tới được câu; hệ số truyền 0,028 | — |
| Nội suy trọng số MIN↔GRPO (V2), soup ba adapter (V3) | V2 đơn điệu, argmax = GRPO ⇒ không chấm test; V3 bỏ | hai adapter gần nhau (lora_B lệch 6,87%) | — |
| **VIS-SFT** (mở tháp thị giác, một biến so S1) | K1: step3200 −7,50 so MIN [val] ⇒ chạm ngưỡng dừng, không chạy tới cuối | không có số test | mốc K1 thiên vị chống VIS-SFT; thử lại cần lý do mới + ngân sách A100 |
| Chưng cất qua bộ trỏ thứ hai, đa nhiệm hộp/toạ độ, Spatial CoT, RL trực tuyến cho `<point>` | bác bằng số / tiền lệ | | report/151 §2.2 |
| DCRP (cặp target-vs-distractor chấm bằng a11y+OCR) | G0 FAIL: trần +0,97 (ngưỡng 3,0) | quét ngưỡng không chạm 3,0 | — |

### 2c. Kênh vị trí, bộ chọn, sửa câu (cuối 9 – 10)

| hướng | đã làm và kết quả | vì sao dừng | nguồn |
|---|---|---|---|
| PATA-C1 (TARGET token + localizer KL + bridge block 17) | localizer học được (hit 52% vs 5%), bật/tắt bridge chỉ +0,17 exec [val] | bridge không đưa vị trí vào câu; không chạy C0-Loc | report/194 |
| PATA-C2 (dual-view) | P1: speaker không phân biệt G với phần tử lân cận (ΔGD 0,004 ≪ 0,02) | dừng ở P1 | report/205 |
| ECGR (hai lượt + Element-Consistency Gate) | G0 147/958 < 250 | dừng ở G0 | report/206 |
| FGRB (tiêm role/zone vào S1) | P1 đạt (zone 3/5 hạt), P2 BLEU-4 −0,03, cổng tự đóng về 0 | kênh gắn thêm bị decoder bỏ qua | report/207 |
| TFVF (làm nét vùng đích) | G0: G>F chỉ 1/3 thước, G không hơn ảnh gốc | S1 phản ứng với biến đổi ảnh, không với vị trí | report/238 |
| Selector màn sau (distill) | thua greedy cả ba thước [val] | câu âm lúc dạy không giống lỗi mẫu S1 | report/233 |
| C1 8 mẫu (cổng cho RL) | **đạt**: oracle SPICE +5,22 [val] ⇒ mở đường GRPO | không phải hướng dừng; là căn cứ RL | report/252 |
| TRIAD-T / POB | C2 net 0; 16/21 bước cứu được bị bộ định vị chỉ-ảnh chặn | đóng (user) | report/274–275 |
| **TAGE** (ck500 nháp → vùng cắt 40% quanh điểm bộ định vị → bộ biên tập LoRA → cổng log-prob τ) | val +4,02 nhưng **test 60,23, − ck500 −0,43** (D.3 −0,58 có ý nghĩa) | τ chọn từ 11 câu val không chuyển sang test; 139/219 câu cổng nhận có vùng cắt sai | report/267, 269 |
| **CTG-GRPO** (thưởng phạt dịch loại thao tác) | test A3 − S1 −1,72; back A3 − A2 −2,96; A3 − ck500 −0,04 | không gỡ được tác hại không chạm của ck500 | report/279 |
| 288: train tiếp ck500 với thưởng người nghe Phi-4 (SPICE-cont, +LR, +GLR) | tspicea −0,20 · tnghev −0,50 · tnghe +0,30 [val], không nhánh nào qua sàng +0,5; tnghe SPICE −1,53 | λ=2 chưa chạy | report/289 |
| RA-SFT (khối 4 ví dụ truy hồi) train tiếp ck500 | val 1/5 thước hơn ck500 ở cả lr 2e-5 và 1e-5; `ra_k4` một mình exec −1,25 | chỉ giữ luật ghép R3 (ACE) | report/304 |
| CW-RA (thẻ COPY/WRITE) | test exec −2,13 [−2,94; −1,31], thua 7/7 thước | nhánh viết đổi 43% câu; đầu chép chỉ ~3% bước | report/310 |
| RA-GRPO | G0: S1 nhìn khối ví dụ thì kém hẳn (SPICE 47,3 → 32,6 [val]) | RL không có mẫu tốt để thưởng | report/312 |
| RAFT từ ck500 (best-of-8, SFT tiếp) | test exec −0,43 p=0,046, 0/7 thước hơn | | report/314 |
| GA-DPO (ngoại tuyến, cùng action) | lr 5e-6 margin ≈0; lr 5e-5 acc 0,544 < 0,6 ⇒ không có số test | mẫu "trội greedy" không có tín hiệu chung (cặp cải thiện acc 0,46) | report/314 GADPO |
| **xao101** (SPICE ghép ngẫu nhiên giữa các mẫu, kiểm soát) | = S1 (59,11); ck500 − xao101 +1,55 | là nhánh kiểm soát, giữ | report/320 |

### 2d. Lưới RL và trục thưởng (tháng 11; từ S1, hạt 101, 500 bước, cùng câu nhắc ck500)

| lượt | exec test | so ck500 | ghi chú |
|---|---|---|---|
| SFT tiếp (cùng câu nhắc) | 60,16 | −0,49 p=0,11 | − S1 +1,05 |
| REINFORCE + SPICE | 60,00 | −0,65 p=0,009 | |
| RLOO + SPICE | 59,44 | −1,21 p=4e−6 | |
| SCST + SPICE | 60,54 | ngang | |
| PPO, GAE λ=1 / 0,95 (1000 bước, value head trên LoRA) | 60,07 / 59,98 | ngang; thấp hơn ở BLEU-4 và CIDEr-D | §26–28; từng hết đĩa, phải `save_total_limit` |
| Dr.GRPO (lượt cũ) | treo ở bước 475, chưa chấm | | đã chạy lại đầy đủ ở đợt B5 (§2e) |
| GRPO + ROUGE-L | 60,63 | ngang | đứng đầu CIDEr-D |
| GRPO + METEOR | 60,27 | ngang | |
| GRPO + CIDEr-D | 60,27 | ngang; CIDEr-D thấp hơn ck500 −5,53 | §22: **không** do df hay tách từ (đã kiểm 5 biến thể), tối ưu kém ngay trên mục tiêu của chính nó |
| GRPO + SPICE A/A (`grpo_luoi.py`) | 59,74 | −0,91 | không tái lập ck500, xem mục 1 |
| RGTC-SPICE (thưởng có Gate B trên cây trợ năng) | Gate B phủ 10,3% (bỏ danh sách 34,8%); điểm T trên 8 mẫu: FULL < chrF [val] ⇒ dừng | | §24–25 |
| Biến thể thưởng SPICE R0–R4 (sàng tĩnh, độ đồng thuận với exec) | R0 0,753 … R4 0,818 < chrF 0,836 [val] | chưa train | §23, report/332 |
| Sàng SA-SPICE-v3 mức 1 (9 câu/bước, 622 bước) | SA 0,771 hơn mọi bản SPICE con nhưng **thua chrF** 0,794 (−0,023, KTC loại 0) | user vẫn chọn chạy SA mức 2 | report/333 §10 |
| GRPO + chrF từ SFT-cont, ck400 | trượt tiêu chí không chạm trên DEV-v3 ⇒ không chấm test | KL > 0,10 ở ck500 | report/333 |
| **A2: GRPO thưởng CIDEr-D từ S1** (đợt đầu, 1.000 câu nhắc, T4 fp16; khác lượt lưới) | A2_500 59,96 · A2_1000 59,98 | A2_500 − ck500 **−0,69 [−1,34; −0,02] p=0,04** (cứu 91 / phá 122) | đúng loại thao tác hơn (+10 bước) nhưng đổi phần tử kém (−41); report/299 |
| ck500 hạt 202 (GRPO + SPICE, hạt thứ hai) | 59,94 [58,13; 61,71] | − ck500/101 −0,72 [−1,27; −0,16] p=0,011; − S1/202 +0,31 p=0,50 | hai hạt cùng dương so S1; report/320 §2 |
| Thưởng `spice_cong` (SPICE × 0,1 khi sai loại) · `ten_loai` · `loai` | chưa train | H2 trên 8 mẫu C1 [val]: conc 0,704 · 0,736 · 0,620 (METEOR 0,871, CIDEr-D 0,868) | `spice_cong` nghĩ ra **sau khi** thấy số test ck500 (phải khai); câu chuẩn F1 tên chỉ 0,57 ⇒ `ten_loai` nhiễu; report/320 §16, `harness/thuong_moi.py` |
| T6 `spice_kp` (tách SPICE khỏi phạt độ dài) | chưa chạy | — | mã sẵn `harness/thuong_t6.py`; report/328 §T6 |
| **SPICE-chrF-A** (α=0,5 cố định, giữ A) + sàng trọng số w | không train | concordance giảm đơn điệu theo w: 0,794 (w=0) · 0,776 · 0,749 · 0,676 (w=1) [sàng] | phán quyết debate sau test: **không đổi reward**; `research_notes/Debate SA SPICE v3 sau test/03_phan_quyet.md` |

**Kết luận đã chốt của trục này:**
- Không lượt nào hơn ck500 có ý nghĩa. Cả nhóm hơn S1 +1,2…+1,5 ⇒ chỉ viết "nhóm dẫn đầu", **cấm "SPICE tốt nhất"**.
- SPICE dự báo exec **kém hơn** CIDEr-D, METEOR, chrF trên mẫu tĩnh (AUC 0,671; xếp đúng cặp 72,2% so với 85,2%).
- SPICE gần như mù loại thao tác ("Click"→"Swipe up" vẫn 0,919).
- Tiền lệ SPICE làm thưởng nghiêng bất lợi (Liu 2017, Pasunuru 2017, RL4LMs).

Giải thích H1–H5 đã đo (report/320 §15–17):
- H1: câu AC theo khuôn ("click on" 56%). AitZ còn theo khuôn hơn AC.
- H2: độ khớp exec trên mẫu tĩnh **không** dự đoán được thứ hạng sau train.
- H5: SPICE vẫn tách rõ đúng/sai loại ở bước không chạm ⇒ "ít tín hiệu ở bước cuộn" **không đứng**.

### 2e. Lưới RL đợt B5 (20–21/11; từ S1, hạt 101, cùng 1.000 câu nhắc ck500) — ĐANG CHẠY, chưa có số test

Nguồn: `report/337` (tình trạng kernel), `slides/ACTION_4_THUAT_TOAN_RL_2025_SO_VOI_GRPO_20_11_2026.md`.
Số dưới đây là **log train**, không phải số test. Có số test thì chép vào đây và vào `report/320`, `report/334`.

| lượt | tới đâu (21/11) | thưởng train · KL | ghi chú |
|---|---|---|---|
| Dr.GRPO đầy đủ | **xong ck500/500** | 0,467 → 0,520 · KL TB/max 0,014/0,095 | chờ chấm test |
| DAPO (lấy mẫu động, eps 0,28) | ck400/500 | 0,465 → 0,486 · KL max 0,211 | nhóm hoà bị loại 20,8% |
| GRPO μ=2 (2 lượt tối ưu mỗi lô sinh) | ck625/1.000 | phẳng 0,500 → 0,500 · **KL max 0,592** | |
| GSPO (tỉ số mức chuỗi) | ck600/1.000 | **giảm** 0,496 → 0,455 · clip_ratio 0,19 → 0,36 | dấu hiệu xấu |
| REINFORCE++ lô 64 | ck70/125 | 0,470 → 0,472 | OOM GPU lần đầu, sửa `--gen-chunk 4` |
| DPO trực tuyến (best-vs-worst trong nhóm 8, β 0,1) | ck450/500 | 0,486 → 0,511 · margin 0,006 → 0,116 | thiết kế ở report/336 §3 |
| GRPO + chrF / BLEU-4 / SPIDEr / BERTScore từ S1 | ck450 / 475 / 350 / 375 | chrF 0,591 → 0,656 (**KL max 0,923**) · BLEU-4 0,474 → 0,618 (KL max 0,311) · SPIDEr 0,464 → 0,500 · BERTScore 0,646 → 0,685 | |
| GRPO / REINFORCE++ lô 128 (`grpo_lon`, `rpp`) | **chết RAM** (-9) ở cả 5 kernel sau 6–8 phút | — | TRL tiền xử lý 128 ảnh = 9,83 GB; đừng chạy lại nguyên trạng |

### 2f. Câu ghép / chọn câu lúc suy luận và phép đo phụ (có số test, không thay phương pháp chính)

| hướng | cách làm | kết quả (test) | trạng thái · nguồn |
|---|---|---|---|
| **RAF** (6–7/10) | chọn giữa câu S1 và ck500 bằng đồng thuận CIDEr-D với 4 câu truy hồi kiểu Mao; chỉ mở khi hai câu khác nhau mà cùng loại thao tác (724/4.463 bước lùi về S1) | − ck500: BLEU-4 +0,72 · ROUGE-L +0,68 · CIDEr-D +5,61 [+1,46; +9,61] · SPICE +0,53 · BERTScore +0,55 · METEOR +0,17 (phủ 0) ⇒ 7/13 cột; 5 cột hành vi −0,13…−0,38 (phủ 0). Xếp hạng n-best kiểu Mao **hỏng**: −25…−84 CIDEr-D [val] | ACE (R3) thay thế; report/298, report/327 |
| AitZ zero-shot (26/10) | chấm 2.736 bước chạm AitZ, không train lại | câu chuẩn 66,26 · S1 37,79 · ck500 37,28 · ACE 37,28 · Base 34,50; ck500 − S1 −0,51 (phủ 0); ACE gần như không kích hoạt | SPICE học văn phong AC, không mang sang AitZ; report/320 §6, 334 §9 |
| ACU: AndroidControl phần S1 chưa thấy (27/10) | 1.484 bước chạm dựng từ TFRecord gốc | câu chuẩn 71,70 · S1 52,16 · **ck500 56,74** · ACE 57,01 · Base 49,80; ck500 − S1 **+4,58 [+3,17; +6,05]** p=2e−10 (vượt MDE) | xong; report/320 §8, 334 §10 |
| Lịch sử tự sinh (26/10) | câu bước trước do mô hình viết thay câu chuẩn | S1 59,11 → 54,96 (−4,15) · ck500 60,65 → 56,44 (−4,21); ck500 − S1 vẫn **+1,48 [+0,54; +2,43]** | xong; report/320 §7, 334 §8 |
| Qwen2.5-VL-7B prompting (26/10) | câu nhắc như Base | 51,51 [49,82; 53,15]; ck500 − 7B +9,14; 7B − Base +3,92 | mốc ngoài; report/320 |

### 2g. Thước đo / dụng cụ đã thử rồi bỏ

| hướng | kết quả | nguồn |
|---|---|---|
| UI-Venus-7B làm thước chính | thấp hơn UGround cả ba nhánh; giữ làm kiểm độ bền | CLAUDE.md 30/8 |
| Luật ±14% (d14) làm tiêu đề | 86% mức tăng là thứ câu rỗng nghĩa cũng lấy được | report/151 §6 |
| AitW với mọi khung bấm được | sàn câu rỗng 41,6 ⇒ chỉ là cận trên | CLAUDE.md 14/9 |
| `sel_acc` làm thước | bỏ abstain kéo 57,5 → 69,5 mà độ đúng thật giảm 63,3 → 50,0 | CLAUDE.md 3/9 |
| "79,3% năng lực của người" | sai công thức, đã gỡ; in hai số cạnh nhau | report/140 |
| CLIPScore làm thưởng / thước | P(đổi động từ > sai tên) 0,690, quá yếu | report/330 |
| Pixtral-12B người nghe | 8,0 do lỗi định dạng | report/155 |
| Phi-Ground-4B | đã chạy ở dụng cụ khác (`runs/phiground`) | report/320 §4 |
