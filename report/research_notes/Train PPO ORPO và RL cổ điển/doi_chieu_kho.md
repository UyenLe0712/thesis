# Đối chiếu kho: dự án đã làm gì với PPO, ORPO và RL cổ điển (tính đến 3/11/2026, 21:06 giờ VN)

Quy ước: mọi đường dẫn tính từ `/mnt/d/Master/Thesis/`. `[đo]` = có trong log hoặc tệp số, `[đọc mã]` = tôi đọc mã nguồn, `[suy]` = suy luận của tôi, chưa đo. Mã TRL đọc từ bản 0.29.1 đúng phiên bản notebook ghim (`_bundles/luoi/make_nb.py:50,53`), bản sao tạm ở `/tmp/claude-1000/-mnt-d-Master-Thesis/f8c22a00-f56d-41dc-bd70-6f4951a71b5e/scratchpad/venv_cpu/lib/python3.12/site-packages/trl/trainer/grpo_trainer.py` (dưới đây viết `TRL:dòng`). Số val không được trích ở đây; chỗ nào cơ chế dựa vào số val thì chỉ tả định tính và chỉ tệp.

## 1. ORPO: đã thử gì, chưa thử gì, câu "ORPO đã chết" còn đúng tới đâu

### Takeaway
Dự án có đúng **một lượt ORPO có điểm test**, ở **tầng khai báo, xuất phát từ S2, cặp dựng bằng heuristic, không có phần thưởng**: MIN-DESC/101 60,05, hơn nhánh so sánh +0,63 và không hơn S1 có ý nghĩa. **ORPO tầng câu từ S1 với mẫu chấm SPICE chưa từng chạy.** Câu "ORPO đã chết" chỉ đúng cho họ tương phản tầng khai báo; với cấu hình mới kia thì phải viết "chưa thử", kèm một số bằng chứng gián tiếp bất lợi.

### Cited Findings

**MIN-DESC, cấu hình**
- Stage-2 nối tiếp từ checkpoint S2 (`create_new_adapter: false`), `pref_loss: orpo`, `pref_beta: 0.1`, 800 update, lô 1 × tích luỹ 16, lr 2e-5 cosine, warmup 5%, QLoRA 4-bit, 22.854 cặp, tức khoảng 0,56 epoch — `harness/train_config_orpo.yaml:17,25-26,38-40,62-65,86,91-93`.
- Pin: LLaMA-Factory `c4e09c7cbe18844816af9e18a97fe465515edbcd`, transformers 5.8.0, A100; khoảng 21 s/bước trên 200 cặp nặng nhất nên 800 bước ≈ 4,7 h (cận trên); log có `sft_loss`, `odds_ratio_loss`, không có ref model — `report/106_DANG_KY_TRUOC.md:1479-1490`.
- Thiết kế cặp: `chosen` = `<desc>` đúng + câu, `rejected` = `<desc>` của phần tử gần nhất (`nearest_other()`) + **câu y hệt** — `report/106_DANG_KY_TRUOC.md:1811-1817`; `CLAUDE.md`, mục *MIN-DESC là gì*.
- Trainer ghép cặp tắt mọi dropout còn nhánh SFT giữ LoRA dropout 0,05, nên MIN và CE2 lệch một biến phải khai — `CLAUDE.md`, mục *MIN-DESC là gì*.

**MIN-DESC, kết quả test (UGround, 4.463 bước chạm, một hạt giống 101)**
- MIN-DESC 60,05 [58,33; 61,77] · CE2-S2 59,42 [57,69; 61,14] · S1/101 59,11 · S2/101 57,18 · Base 47,59 · câu chuẩn 75,73 — `report/106_DANG_KY_TRUOC.md:1734,1893-1904`.
- MIN − CE2 **+0,63 [+0,16; +1,10]**, b=70, c=42, p=0,011 · CE2 − S2 +2,24 p=1,4e−7 · MIN − S2 +2,87 · CE2 − S1 +0,31 p=0,61 · MIN − S1 **+0,94 [−0,09; +2,05]** p=0,11 — `report/106_DANG_KY_TRUOC.md:1907-1915`. Tính lại 25/10 cho KTC hơi khác do bootstrap: MIN − S1 [−0,16; +2,08], MIN − CE2 [+0,16; +1,09] — `runs/bang_ghep_cap_25_10.json`.
- Quy công: 78% mức tăng S2 → MIN thuộc nhánh SFT, 22% thuộc ORPO; ở tầng khai báo tỉ lệ đã sửa là 87,66% / 12,34% (+5,93 / +0,84) — `report/106_DANG_KY_TRUOC.md:1940-1950`; `CLAUDE.md`, mục *Cổng cơ học*.
- +0,63 dưới MDE 2,11 và chỉ gấp 1,4 lần σ giữa hạt giống 0,46; câu được phép viết là "đóng góp +0,63 so với đối chứng SFT cùng bước, dưới MDE, kết quả thăm dò"; cấm "ORPO cải thiện mô hình" — `report/106_DANG_KY_TRUOC.md:1917-1938`.
- Dưới AitW đầy đủ: MIN − S1/101 +2,04 p<0,001 nhưng MIN − CE2 chỉ +0,31 p=0,215 — `CLAUDE.md`, khối 14/9 (nguồn `runs/d3_ktc.json`).
- Trên bước không chạm, đúng loại thao tác của MIN giảm −19,75 và CE2 −20,50, do dữ liệu chỉ có bước chạm chứ không do ORPO — `report/106_DANG_KY_TRUOC.md:1559,1573-1601`.
- ck500 − MIN-DESC +0,60 [−0,52; +1,73] p=0,30, tức chưa phân biệt được — `runs/bang_ghep_cap_25_10.json`.
- MIN/202 và CE2/202 không chạy — `report/106_DANG_KY_TRUOC.md:1617-1643`; `report/128_CHOT_PHUONG_PHAP_VA_THUOC_30_8.md:34`.

**Biến thể cùng tầng khai báo**
- MIN-ONPOLICY dừng ở cổng, không train: 14.000 màn sinh khai báo, 459 cặp, eligibility 3,3% (1,1% in ra là lỗi mẫu số; 14,1% ở mẫu số rộng lượng nhất), ngưỡng 25%; tốn khoảng 4,5 h A100 — `report/106_DANG_KY_TRUOC.md:1975-2015`.
- Lý do đo được: khoảng cách phần tử nhầm và phần tử đúng p25 70 px, trung vị 351, p75 748; 76,5% nằm ngoài dải 80–350 px — `report/106_DANG_KY_TRUOC.md:2020-2041`.
- `gui_orpo_hard` không chạy, bác bằng số học: phần riêng của ORPO đã đo +0,63 và estimand của nó là tập con của mức đó — `report/128_CHOT_PHUONG_PHAP_VA_THUOC_30_8.md:33,37-39`.
- Ở thiết kế tầng câu cũ (câu chuẩn so với câu đổi phần tử), eligibility 26,40%, sát cổng 25% — `report/106_DANG_KY_TRUOC.md` mục (x4). Đây là lý do chọn tầng khai báo hồi 23/8, không phải kết quả huấn luyện.

**"ORPO tầng câu bị bác" thật ra là gì**
- Không có lượt train nào. Đó là một phép **thay thế phản thực trên tệp thô**: trên lát "kênh A của MIN sai", thay exec của MIN bằng exec của S1 — `harness/phu_luc_c.py:84,90`.
- Số: +4,80 theo lát A(MIN) sai · +2,88 theo A(GRPO) sai · −0,72 ở lát A(GRPO) sai ∧ A(MIN) đúng · −0,65 ở lát 30% màn đông nút — `report/151_BAN_CHOT_CUOI_PHUONG_PHAP_VA_THUOC_7_9.md:172,843-853`; tái lập khớp tuyệt đối theo `report/152_LO_TRINH_SAU_151_9_9.md:99`.
- Cùng script in thêm: thay bằng câu chuẩn trên lát đó thì +14,14 — `report/151_BAN_CHOT_CUOI_PHUONG_PHAP_VA_THUOC_7_9.md:786-790`.
- 66,67%: trong 1.950/4.463 bước MIN và GRPO khác `<desc>`, 1.300 bước câu giữ nguyên từng ký tự. Bản gốc tự khai "không quy nhân quả", và đọc đúng là "hàm mất mát chưa bao giờ so hai CÂU khác nhau" — `report/151_BAN_CHOT_CUOI_PHUONG_PHAP_VA_THUOC_7_9.md:868-873,889-906`.
- Cùng bảng §2.2 đó cũng ghi "⛔ RL trực tuyến" bị bác bằng số — `report/151_BAN_CHOT_CUOI_PHUONG_PHAP_VA_THUOC_7_9.md:178`. Sau đó GRPO + SPICE từ S1 lại cho ck500 60,65, ck500 − S1/101 +1,55 [+0,80; +2,33] — `report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md` §14.1; `CLAUDE.md`, mục GRPO thưởng SPICE.

**Tương phản tầng câu: có chạy, nhưng khác cấu hình cần hỏi**
- GA-DPO (tên nội bộ, không phải phương pháp công bố): DPO β=0,1 + NLL λ=1,0, có tham chiếu, LoRA mới trên **S1 + ck500** đã hoà, 830 cặp từ mẫu ck500 T=0,7 (415 cặp cải thiện và 415 cặp giữ, rejected hoặc chosen luôn là câu greedy), 52 bước, Colab L4 bf16, khoảng 107 phút/lượt — `report/314_KET_QUA_GADPO_13_10.md:13-17`.
- Log train: lr 5e-6 không dịch khỏi ref; lr 5e-5 acc cao nhất 0,544, dưới luật chấm 0,6. **Không có số test; cấm viết "GA-DPO thua ck500"** — `report/314_KET_QUA_GADPO_13_10.md:23-43`.
- Phép kiểm trên chính tập cặp train (đây là chẩn đoán học, không phải kết quả val của mô hình): 200 cặp, 5 epoch, 125 bước, acc đã thấy 1,00, giữ riêng 0,61; tách loại: cặp cải thiện 0,46, cặp giữ 0,76; log-p câu chosen trên câu nhắc giữ riêng giảm −0,261 → −0,457 — `report/314_KET_QUA_GADPO_13_10.md:68-97`. Không chạy lượt đủ — `report/314_KET_QUA_GADPO_13_10.md:105`.
- Kết luận của chính báo cáo: mẫu "trội greedy" do ck500 tự sinh không chứa quy luật chung; không nên mở lại nếu **không đổi cách lấy đích** — `report/314_KET_QUA_GADPO_13_10.md:99-107`.
- RAFT từ ck500 (lọc mẫu rồi SFT, không phải tương phản): 415/2.000 đích đổi, 125 bước, test exec 60,23 so ck500 60,65, −0,43 [−0,82; −0,04] p=0,046 — `report/314_KET_QUA_GADPO_13_10.md:52`; `report/314_KET_QUA_RAFT_12_10.md:10-13`.

**So cấu hình**

| lượt | tầng cặp | điểm đầu | nguồn cặp | có phần thưởng? | có điểm test? |
|---|---|---|---|---|---|
| MIN-DESC | khai báo, câu y hệt | S2 | câu chuẩn so phần tử gần nhất (heuristic) | không | có: 60,05 |
| MIN-ONPOLICY | khai báo | S2 | khai báo sai của S2 | không | không, dừng ở cổng |
| `gui_orpo_hard` | khai báo | S2 | vế âm khó | không | không chạy |
| "ORPO tầng câu" (151) | không train | không | thay exec S1 trên một lát | không | không, chỉ phản thực |
| GA-DPO | câu | S1 + ck500 | mẫu ck500 so greedy, trên nhiều độ đo | nhiều độ đo, lọc trội | không |
| **B6: ORPO từ S1, mức câu** | câu | **S1** | **8 mẫu S1, chấm SPICE** | **SPICE** | **chưa viết mã, chưa chạy** |

B6 đang là dòng ưu tiên hai, đợt 3 — `report/reports/Baseline RL so với GRPO.md:130`; `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md:74`. DPO trực tuyến A5, ngoại tuyến A6, RFT A7, online RFT A8 cũng chưa có kết quả — `report/reports/Baseline RL so với GRPO.md:112-115`; `report/326_BAN_GIAO_LUOI_RL_1_11.md:104`. Đoạn mã gần nhất phải sửa vì đang chốt máy: `assert ... "DỪNG: train GA-DPO cần A100/L4"` — `_scripts/314/ga313/ga_dpo.py:221`.

### Inferences
- [suy] Câu "ORPO đã chết" ở `CLAUDE.md` và `report/128` mở rộng quá tầm nếu áp cho B6. Điểm đầu khác (S1 chứ không S2), tầng khác (hai câu khác nhau), nguồn cặp khác (mẫu on-policy, không heuristic), và lần đầu có thưởng.
- [suy] Trần +4,80 không phải cận trên cho B6: nó giả định đích là "bằng S1" trong khi B6 bắt đầu từ S1. Nó cũng phụ thuộc kênh `<desc>` mà S1 không có. Phản bác trần đó làm yếu lập luận *ủng hộ* tầng câu thời đó, chứ không chứng minh tầng câu vô dụng.
- [suy] 66,67% thực ra ủng hộ việc **chưa có dữ liệu** về tầng câu: ORPO cũ không so hai câu. Dùng nó làm "bằng chứng cắt ORPO câu" như `report/151:872` là đọc quá chữ. Khi bị hỏi, nên nói số này giải thích vì sao tầng khai báo khó truyền xuống câu.
- [suy] Bằng chứng bất lợi còn lại là gián tiếp: GA-DPO cho thấy cặp mẫu so greedy của ck500 thiếu tín hiệu chung, và SPICE có nhiều hoà và tín hiệu đầu yếu hơn các độ đo khác (`report/323` §9, số val, không trích). Nếu nguồn cặp B6 cũng là "mẫu thắng nhờ dao động", kỳ vọng thấp. Nhưng GA-DPO đo trên ck500, không phải S1, và không có điểm test.
- [suy] Một điểm khác đáng nêu: `report/252` cho thấy cổng oracle trên mẫu S1 đạt trên val (không trích số), nên S1 có mẫu tốt hơn để chọn so với ck500; đây là lý do duy nhất để B6 chưa bị loại sẵn, nhưng oracle không phải chính sách học được.

### Gaps
- Không có số test nào cho ORPO hoặc DPO tầng câu. Không có đối chứng SFT tiếp cùng cặp vì SFT tiếp chưa chấm test.
- Chưa có mã B6; thời gian và VRAM trên T4 của ORPO chưa đo (ước lượng ở mục 5).
- Chưa mở bài ORPO gốc trong phiên này để kiểm cách đặt λ, phần đó thuộc nhóm tra tài liệu.

## 2. PPO: mã làm gì, đúng tới đâu, probe ra sao

### Takeaway
`harness/grpo_ppo.py` đúng về mặt công thức: tôi đọc kỹ và **không thấy lỗi làm sai gradient**. Nhưng đây là "PPO đầu giá trị nhỏ trong khung GRPO", đổi cùng lúc nhiều yếu tố. Rủi ro lớn nhất: **phép clip nhiều khả năng vẫn gần như không hoạt động ngay cả khi μ=2, vì lr 1e-5 làm tỉ số xác suất gần 1, và probe đang chạy không đủ để kiểm tra clip**. Chưa có số test nào cho PPO; kernel probe vẫn RUNNING lúc 21:06 giờ VN.

### Cited Findings

**Cơ chế [đọc mã]**
- Đầu giá trị: MLP `Linear(H,512) → ReLU → Linear(512,1)`, tầng cuối khởi tạo 0 nên ban đầu V = 0, AdamW riêng lr 3e-4, không weight decay, không huấn luyện trước, không clip gradient — `harness/grpo_ppo.py:19,76-79`.
- Đặc trưng: hook `forward_pre_hook` trên `lm_head`, lấy `args[0][:, :-1][:, -keep:]` rồi `.detach().float()` — `harness/grpo_ppo.py:63-66`. Vị trí đúng là trạng thái **trước** token t, tức V(s_t). Gradient của V không về LoRA, nên đặc trưng không được huấn luyện theo giá trị.
- Lợi thế: GAE γ=1, thưởng chỉ ở token cuối, mặc định λ=1 thì A_t = r − V(s_t) và đích V = r — `harness/grpo_ppo.py:24-36`; selftest kiểm λ=1, 0, 0,5 — `harness/grpo_ppo.py:148-161`. Đích V lấy trước khi chuẩn hoá nên không bị lệch thang — `harness/grpo_ppo.py:111-118`.
- Chuẩn hoá: trừ trung bình rồi chia std trên **mọi token của lô sinh** (16 câu của 2 câu nhắc), không theo nhóm — `harness/grpo_ppo.py:115-116`.
- μ: `num_iterations` đè bằng cờ `--mu`, mặc định ppo 2 theo docstring, a2c μ=1 — `harness/grpo_ppo.py:3-5`; `harness/grpo_codien.py:122,133-136`. Notebook dùng `ppo:spice:101:mu=2,lam=1.0,steps=1000,tag=l10` và `a2c:spice:101` — `_bundles/luoi/k_luoi-probe-ppo/luoi-probe-ppo.ipynb`.
- Bước: tham số `steps_per_generation = 4`, `generation_batch_size = 16`, tức 2 câu nhắc × G=8 — log `runs/luoi/lo1/*/*.train.log` dòng `GRPOConfig`. Với μ=2, 1.000 bước vẫn dùng 1.000 câu nhắc nhưng 1.000 lần cập nhật (ck500 500) — `harness/grpo_ppo.py:5`; `TRL:911,1111`.
- Tỉ số: μ=2 cho `gradient_accumulation_steps % generate_every = 4 % 8 ≠ 0` nên TRL tính `old_per_token_logps` — `TRL:1788-1790`. μ=1 thì không, tỉ số luôn bằng 1 — `TRL:2144-2148`. TRL nhận lợi thế dạng (B, T) — `TRL:2138-2143`.
- Clip: `-min(coef_1·A, coef_2·A)`, ε = 0,2 hai phía (mặc định, không phải 0,28 của DAPO) — `TRL:2196-2203`; `grpo_config.py:573-575`. Không có `delta`.
- Giữ nguyên của ck500: `loss_type="dapo"` (cũng là mặc định TRL, gộp theo số token của lô tích luỹ) — `harness/grpo_luoi.py:333`; `grpo_config.py:651-660`. `beta=0.04` phạt KL về **S1 cố định**, không về chính sách trước — `harness/grpo_luoi.py:326`; `TRL:2174-2181`. Không có hệ số entropy; `entropies` chỉ để log — `TRL:2118-2123,2256`; docstring `harness/grpo_ppo.py:7`. G=8, T=1, lr 1e-5, warmup 10 — `harness/grpo_luoi.py:324-327`.
- Lưu và nạp đầu giá trị khi nối tiếp có kiểm tồn tại tệp — `harness/grpo_ppo.py:80-86,139-143`.

**Đã kiểm, không phải lỗi [đọc mã]**
- GAE đúng: `gae()` xử lý token ngoài câu không làm mất thưởng cuối.
- Căn hàng đặc trưng và mặt nạ đúng; có `assert V.shape == mask.shape` — `harness/grpo_ppo.py:110`. Forward thêm chạy `no_grad`, `_hid` được xoá ở mỗi lượt gọi nên forward của tham chiếu và của `old_logps` không lẫn — `harness/grpo_ppo.py:70,103-106`.
- `LAST["r"]` đọc trước khi TRL xáo lô; `value_targets` và `advantages` xáo cùng hoán vị — `harness/grpo_ppo.py:98,118`; `TRL:1115-1118`.
- `l.backward()` của V tách đồ thị khỏi loss chính; đầu giá trị ở fp32 ngoài autocast — `harness/grpo_ppo.py:125-131`.
- Thứ tự vá module khớp nhau: `GL.lop_trainer`, `GL.loi_the`, `GL.ALGOS` — `harness/grpo_ppo.py:15,20-21,164-167`; `harness/grpo_codien.py:145-147`.
- Tệp trong gói trùng md5 máy nhà: `grpo_ppo.py` `c7dd1658…`, `grpo_codien.py` `5499d604…` [đo, md5sum].

**Điểm không chuẩn hoặc có rủi ro**
1. **Clip có lẽ không làm gì.** Với μ=2, bước lẻ tỉ số bằng 1 theo cấu tạo; bước chẵn tỉ số chỉ phản ánh **một** lần cập nhật. Muốn tính vào `clip_ratio` phải có `|log ratio|` vượt khoảng 0,18–0,22 đúng chiều lợi thế — `TRL:2266-2268`. Log các lượt cùng lr: KL trung bình mỗi token **so với S1** ở bước 10 là 3e-6 đến 9e-6, bước 20 là 2e-5 đến 3e-5, cuối commit đầu (khoảng bước 260) khoảng 0,007–0,035 [đo, log train, không phải kết quả] — `runs/luoi/lo1/luoi-*/*.train.log`; ck500 bước 20 là 1,7e-5, bước 262 là 0,005 — `runs/grpo_spice/train_c1.log`. KL ≈ Δ²/2 cho RMS log ratio khoảng 0,006 ở bước 20 và khoảng 0,12–0,26 sau khoảng 260 bước **cộng dồn** [suy].
2. **Probe không kiểm được clip.** `clip_ratio/region_mean = 0` ở probe không phân biệt được "clip lỗi" với "tỉ số chưa đủ lớn". `report/326:120` đặt yêu cầu xem chỉ số này > 0, nhưng [suy] yêu cầu đó khó đạt và số 0 không chứng minh được gì.
3. **Probe bị cắt sớm.** Notebook đặt `CAT = 3600 * 0.65` (39 phút, bản nguồn `make_nb.py:116` là 1,5 h) trong khi chỉ tính từ đầu notebook. Lượt cũ có bước 1 ở khoảng 0,14–0,17 h — `runs/luoi/lo1/luoi-u-1/luoi-u-1.log`. Với khoảng 150 s/bước, [suy] tới trần mới được khoảng 11–12 bước trên 20, gồm 5–6 lần tỉ số khác 1 và phần lớn ở vùng warmup. Khi `terminate`, dòng `[xong]` chứa đỉnh VRAM và s/bước sẽ **không in** — `harness/grpo_luoi.py:386`; VRAM chỉ còn `memory.used` mỗi 120 s — `_bundles/luoi/make_nb.py:169`. s/bước vẫn tính được từ `step_time`, và `luoi/v_loss`, `luoi/v_ev` vẫn ở log.
4. **Đổi nhiều yếu tố một lúc** so với ck500: mốc (V thay TB nhóm) · lợi thế theo token · chuẩn hoá theo lô thay theo nhóm · bỏ chia std nhóm · μ · gấp đôi số cập nhật. `report/reports/Baseline RL so với GRPO.md:110` đã yêu cầu khai, nhưng chỉ nêu mốc và μ. A2C loại được riêng μ, nhưng không loại ba yếu tố còn lại.
5. **V yếu nên có thể thua vì lý do cài đặt.** V bắt đầu từ 0, không pretrain, đặc trưng không học. [suy] Những bước đầu A gần như r trừ trung bình lô, nên phương sai giữa hai câu nhắc rơi vào lợi thế, còn GRPO đã trừ theo nhóm. G=8 vẫn được giữ để cùng ngân sách mẫu nhưng PPO không dùng cấu trúc nhóm. `luoi/v_ev` phải được đọc trước khi kết luận gì.
6. **Thiếu chẩn đoán chuẩn của PPO:** không log `approx_kl` hay phân vị `|log ratio|` — `harness/grpo_ppo.py:112-114,132-136`; chỉ có `clip_ratio`. Không có clip giá trị, không xáo lại minibatch giữa hai vòng (`_buffered_inputs` giữ nguyên thứ tự) — `TRL:1119`.
7. **Lẫn chỉ số:** lớp cha ghi `luoi/adv_abs_mean` theo công thức nhóm rồi lớp con ghi thêm theo PPO, hai giá trị trộn nhau; `luoi/frac_adv_zero` vẫn là của công thức nhóm — `harness/grpo_luoi.py:253-254`; `harness/grpo_ppo.py:114`; `harness/grpo_ppo.py:40-41`. Không ảnh hưởng train, cấm dùng làm số mô tả.
8. **Lỗi nhỏ về log:** chú thích nuốt mất `log_completions=a.probe, num_completions_to_print=2` — `harness/grpo_luoi.py:328`. Không đổi train nhưng probe không in câu mẫu.
9. **Cờ `eps` chỉ đặt `epsilon_high`** — `harness/grpo_codien.py:124,134`. Muốn kiểm clip cơ học thì đặt `eps` rất nhỏ để `clip_ratio/high_mean` > 0 ở bước chẵn, còn vế thấp chưa có cờ.
10. **Nối tiếp với μ=2:** `save_steps=25` rơi vào bước lẻ, khi nạp lại `_step`=0 và sinh lại thay vì chạy vòng hai — `harness/grpo_luoi.py:329`; `TRL:1112-1113`. [suy] ảnh hưởng nhỏ, phải khai.
11. **Forward thêm:** mỗi lô sinh có thêm một forward `no_grad` để lấy đặc trưng, ngoài forward tham chiếu và `old_logps` — `harness/grpo_ppo.py:103-105`. Đầu giá trị nhỏ nên [suy] VRAM gần 12,7 GiB của GRPO; phải đọc từ probe.

**Trạng thái probe**
- `kg trang kernels status trangphngngc/luoi-probe-ppo`: **RUNNING** lúc kiểm cuối (21:05–21:06 giờ VN). Không có output nên không tải. Thư mục notebook tạo lúc 20:51 giờ VN theo mtime; [suy] kernel chạm trần khoảng 21:30–21:40.
- Mục đích ghi trước: VRAM, s/bước, `clip_ratio/region_mean` — `report/326_BAN_GIAO_LUOI_RL_1_11.md:120`; tràn thì chuyển danh sách Colab — `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md:89`.
- Chưa có lượt train PPO, A2C nào; lượt `k_luoi-*` đã chạy thật không chứa `ppo`, `a2c` ngoài probe [đo, đọc `RUNS` của từng notebook].
- Bên cạnh: `uyenle0712/luoi-test-u-2` (chấm nốt GRPO + CIDEr-D) đang ở trạng thái **ERROR** lúc kiểm; chưa đọc log, cần xem, số CIDEr-D vẫn là số tạm.

### Inferences
- [suy] Vì tỉ số gần 1 và clip gần như không hoạt động, PPO μ=2 trên bài này có thể gần với "actor-critic cập nhật hai lần trên mỗi lô". Nếu vậy, phép so PPO với GRPO đo chủ yếu mốc học được và số cập nhật, không đo cơ chế clip. Câu trả lời cho thầy phải nói rõ điều này.
- [suy] Làm clip hoạt động thật cần lr lớn hơn hoặc μ lớn hơn, nhưng mỗi thay đổi đó cũng rời khỏi ngân sách của ck500, nên nên là lượt độ nhạy riêng, không thay lượt chính.
- [suy] Phép kiểm clip tốn ít: đo phân vị `|log ratio|` trên một lô ở bước cuối điểm lưu đã có, và probe nhỏ với `eps` rất nhỏ.

### Gaps
- Không có số thật nào về PPO (VRAM, s/bước, `v_ev`, `clip_ratio`) cho tới khi probe xong. Chưa kiểm được đuôi phân bố `|log ratio|`; KL trung bình không nói hết về đuôi.
- Chưa so với mã UI-TARS-2 về độ lớn lr, μ, critic; không có trong kho.

## 3. RL cổ điển: `harness/grpo_codien.py`

### Takeaway
Cả bảy nhánh `vanilla, mad, rft, cem, awr, raml, rank` đã có mã, **selftest và chạy CPU đạt, chưa probe T4, chưa train, chưa có số**. Tất cả chỉ đổi trọng số A của từng câu mẫu trong khung ck500, nên chỉ `vanilla` và `mad` sát tên gốc; còn lại phải gọi "kiểu …".

### Cited Findings
- Công thức và phạm vi: `harness/grpo_codien.py:5-12,21-23,34-55`; selftest `:58-79`. Cùng điểm đầu S1, 1.000 câu nhắc, G=8, lr, β=0,04, `loss_type="dapo"`, μ=1, 500 bước — `:3-4`; `harness/grpo_luoi.py:324-333`. Mọi nhánh giữ KL về S1 và không có entropy. Vì μ=1 nên clip không hoạt động — `report/326_BAN_GIAO_LUOI_RL_1_11.md:132`.
- Trạng thái: "chưa probe T4", cùng vòng lặp nên [suy] cùng VRAM — `report/326_BAN_GIAO_LUOI_RL_1_11.md:119`; `report/reports/Baseline RL so với GRPO.md:162`. `make_nb.py` đã nhận các nhánh này và cờ — `_bundles/luoi/make_nb.py:20-22`. Xếp sau đợt 1: `vanilla` thuộc đợt 1, `rft`/`cem` đợt 3, `awr`/`raml`/`rank`/`mad` đợt 4 — `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md:68,74,77`. `report/328:221` khuyên dừng thêm phương pháp cổ điển tới khi xong A1, K1, SCST + CIDEr-D, PPO.

| mã | công thức A | mức trung thành | phải khai |
|---|---|---|---|
| `vanilla` | r | Sát REINFORCE không mốc, nhưng theo batch nhóm 8 mẫu, thêm KL | Thưởng gần như luôn dương nên đẩy lên mọi câu; phạt độ dài có thể làm r âm |
| `mad` | (r − TB)/MAD | Công thức một dòng theo DGPO | `report/reports/…:141,172` ghi nguồn MathForge; phải kiểm công thức trong bài trước khi gọi DGPO |
| `rft` | 1 cho câu cao nhất nhóm | Online RFT, không có SFT rời như RFT một vòng | Hoà một phần thì chọn câu đứng đầu theo thứ tự (`stable`) — `:29`; mẫu số `dapo` vẫn tính token các câu A=0 nên cỡ bước nhỏ đi so với KL |
| `cem` | 1 cho 25% câu cao nhất (`round(8·0,25)=2`) | **Không phải CEM cổ điển** (dò trên tham số hoặc trình tự); đây là chọn elite trên đầu ra, gần `rft` | Như trên; elite theo từng nhóm, không có cập nhật phân phối kiểu MLE nhiều vòng |
| `awr` | exp((r − TB nhóm)/τ), chặn 20 | **Kiểu AWR**: không V, không replay, không off-policy | τ=0,2 do dự án chọn — `:22`; A luôn dương, không có vế đẩy xuống |
| `raml` | G·softmax(r/τ) | **Kiểu RAML**: mẫu từ chính sách, không từ q* | [suy] Khác `awr` chỉ ở hệ số chuẩn hoá theo nhóm, có thể đếm là một — `report/reports/…:170` |
| `rank` | hạng trong nhóm về [−0,5; 0,5] | Chỉ fitness shaping, không phải ES | Thưởng hoà một phần nhận hạng khác nhau theo thứ tự — `:53`; SPICE hoà nhiều, nên đây là nhiễu riêng [đọc mã] |

- Chưa có mã (Kaggle, viết sau): MRT · softmax PG · MIXER rút gọn · trộn RL + CE · SeqGAN · Quark · ES đủ — `report/326_BAN_GIAO_LUOI_RL_1_11.md:107`.
- Có mã nhưng không phải cổ điển: SCST + SPICE có số; phải viết là "mốc greedy kiểu SCST trong khung GRPO" — `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md:116-119`. RLOO, REINFORCE EMA đủ 500 bước, chưa chấm test — `report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md:684`; `harness/grpo_luoi.py:179-184`.
- SFT tiếp (Behavior Cloning): đủ 500 bước, chưa chấm — `report/326_BAN_GIAO_LUOI_RL_1_11.md:37`.
- Cần Colab hoặc chưa chắc vừa T4, chờ user: PPO critic đủ cỡ · TRPO · DQN/soft Q đủ cỡ · SAC rời rạc · ILQL — `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md:104-110`.
- Không chạy: DDPG, TD3, DPG (hành động liên tục); A3C (A2C đại diện); Double DQN, Rainbow; GAIL; Decision Transformer — `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md:112-114`.
- DQN vướng vì Q(s, a) cho 151.936 token, thưởng chỉ ở cuối câu, logits S1 không phải giá trị Q — `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md:50`.
- Mẫu đếm độ phổ biến là 99 bài chọn tay, số chỉ để sắp thứ tự, không đưa vào luận văn trừ khi kiểm lại — `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md:9,13`.

### Inferences
- [suy] Vì cùng G=8 nhóm, ngân sách và KL, các nhánh này trả lời "đổi trọng số mẫu có đáng không", chưa trả lời "thuật toán cổ điển X có tốt không". Khi trình phải dùng đúng chữ "kiểu".
- [suy] Với `rft`, `cem`, `awr`, `raml`, `vanilla`, thang của A khác GRPO nhiều nên tỉ trọng so với β·KL khác nhau; kết quả lẫn cả yếu tố cỡ bước và yếu tố giữ gần S1.
- [suy] Phép xử lý hoà của `rft`, `cem`, `rank` nên được sửa trước khi chạy (chia đều hạng hoặc chọn ngẫu nhiên có ghi hạt) vì SPICE hoà nhiều; thứ tự trong nhóm hiện theo sinh mẫu nên không thiên vị rõ, nhưng không có chủ đích.

### Gaps
- Không có số train hay test nào cho bảy nhánh. Chưa đối chiếu công thức DGPO với bài gốc trong phiên này.

## 4. Số đã đo: test, tốc độ, VRAM, hạn mức

### Takeaway
Trên test, bốn lượt lưới đã chấm cùng ck500 nằm trong dải 60,25–60,65 exec, không phép so exec nào với ck500 loại 0 và tất cả hơn S1 dưới MDE. Chưa có số PPO, ORPO, cổ điển, SFT tiếp.

### Cited Findings

**Test (một hạt giống 101, 500 bước, cùng câu nhắc ck500)** — `report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md` §14.1 (dòng 647 trở đi), §14.4

| nhánh | exec | D.3 | AitW đầy đủ | đúng loại thao tác | − ck500 exec | − S1 exec |
|---|---|---|---|---|---|---|
| S1/101 | 59,11 | 65,49 | 74,37 | 94,35 | | |
| ck500 | 60,65 | 67,02 | 76,25 | 95,97 | | +1,55 [+0,80; +2,33] |
| GRPO + ROUGE-L | 60,63 | 67,04 | 76,79 | 96,86 | −0,02 [−0,54; +0,49] | +1,52 [+0,78; +2,29] |
| SCST + SPICE | 60,54 | 66,88 | 76,14 | 96,08 | −0,11 [−0,56; +0,35] | +1,43 [+0,79; +2,11] |
| GRPO + METEOR | 60,27 | 66,75 | 76,27 | 96,28 | −0,38 [−0,95; +0,19] | +1,17 [+0,39; +1,97] |
| GRPO + CIDEr-D (tạm, 4.428 bước) | 60,25 | 66,44 | 75,97 | 96,05 | −0,36 [−0,87; +0,14] | +1,17 [+0,43; +1,96] |

- Holm tạm cho bốn phép so với ck500: 0,71 · 0,71 · 1,00 · 1,00. Toàn bộ lượt CIDEr-D nếu đủ bước nằm trong [59,78; 60,56].
- Độ đo văn bản: ck500 không dẫn đầu cột nào; GRPO + ROUGE-L hơn ck500 ở 6/7, SCST + SPICE hơn ở 6/7; GRPO + CIDEr-D thấp hơn ck500 ngay trên CIDEr-D −5,53 [−10,21; −1,20], chưa giải thích được — `report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md` §14.4.
- ck500 hai hạt chênh 0,72 exec; ngưỡng "hơn": KTC loại 0 và |Δ| ≥ 1, kèm nhãn một hạt; MDE 2,11 — `report/326_BAN_GIAO_LUOI_RL_1_11.md:135`. Tính cả bước không chạm, lợi ích ck500 còn +0,39 [−0,21; +0,99] — `report/328_DANH_GIA_GRPO_SPICE_VA_THUYET_PHUC_1_11.md:13`.
- Phần lặp lại được của mức tăng chủ yếu là sửa loại thao tác — `report/328_DANH_GIA_GRPO_SPICE_VA_THUYET_PHUC_1_11.md:11`.
- Dự kiến: lưới nằm trong dải khoảng 1 điểm exec [suy của báo cáo] — `report/328_DANH_GIA_GRPO_SPICE_VA_THUYET_PHUC_1_11.md:82`.

**Tốc độ và VRAM đã đo**

| việc | máy | s/bước | đỉnh VRAM | nguồn |
|---|---|---|---|---|
| Probe SCST + SPICE, 50 câu dài nhất | T4 | 158,1 | 12,71 GiB | `report/323…:469-474` |
| Probe GRPO + CIDEr-D | T4 | 149,1 | 12,71 GiB | như trên |
| Train thật: METEOR / ROUGE-L / RLOO / REINFORCE / CIDEr-D / SCST | T4 chung 2 lượt | 150 / 148 / 150 / 147 / 141 / 163 | | `step_time` TB, `runs/luoi/lo1/luoi-*/*.train.log` |
| ck500 (nối tiếp 75 bước) | T4 | 146–157 | 12,38 GiB | `report/254_TINH_TRANG_GRPO_SPICE_30_9.md:11,64,117` |
| SFT tiếp, 2 câu nhắc/bước | T4 | **13,4** | **10,94 GiB** | `runs/luoi/lo3/luoi-t2-3/luoi-t2-3.log`; `report/326:37` |
| SFT từ ck500, 16 câu/bước | T4 | 110,7 | 6,7 GiB | `report/314_KET_QUA_RAFT_12_10.md:12` |
| Thưởng SPICE | | 7–11 s/lần | | log `[spice] lần` |
| CTG (GRPO G=8, bs4×4, 12 câu dài nhất) | L4 | 86,3 | 13,5 GiB | `report/279_TONG_HOP_CTG_GRPO_4_10.md:75-83` |
| như trên | A100 | 36,4 | 13,5 GiB | như trên |
| như trên, 2 nhánh chung | A100 | 49,3/nhánh | 28,9 GiB cả máy | như trên |
| như trên | T4 | 136–137 | 11,9 GiB | `report/279:32` |
| MIN-DESC, 200 cặp nặng | A100 | ~21 | | `report/106:1487` |
| GA-DPO 52 bước | L4 bf16 | ~107 phút/lượt | | `report/314_KET_QUA_GADPO_13_10.md:17` |

- Hạn mức: 30 h GPU/tuần/tài khoản, ba tài khoản, làm mới 7/11; phiên T4×2 chạy hai lượt, trần commit 11 h; toàn lưới [suy] khoảng 50 lượt, 795 giờ, 9 tuần — `report/326_BAN_GIAO_LUOI_RL_1_11.md:68,111`. Lịch: sau 7/11 — `report/326:40`.
- Bậc thang và luật: CPU → T4 → L4 → A100, tỉ số thời gian L4/A100 ≤ 1,5 thì chọn L4; SFT đo được 2,92× — `CLAUDE.md`, *THỦ TỤC CHỌN MÁY*. Đo CTG cho 2,37× nên cũng ở ô A100. Giá đọc 5/10: L4 1,54, A100 5,3 đơn vị/giờ; phải đọc lại lúc quyết — `report/279:85`.
- `report/326:15` ghi Colab chỉ chạy khi user quyết.

## 5. Ước lượng chi phí nếu chạy [suy, chưa đo]

### Takeaway
Mọi con số dưới đây là ước lượng từ các số đo trên; probe sẽ thay. PPO μ=2 đủ 1.000 bước trên T4 khoảng gấp đôi một lượt GRPO, nên chạy được miễn phí nhưng cần nhiều commit. ORPO từ S1 kiểu ngoại tuyến rẻ hơn GRPO.

### Cited Findings
Cách tính: 16 chuỗi train ≈ 107–111 s (khớp 13,4 s/2 chuỗi và 110,7 s/16 chuỗi ở bảng trên), nên GRPO 148 s/bước ≈ 110 s cập nhật + 38 s sinh, chấm, tham chiếu; forward `no_grad` thêm giả định khoảng 20 s.

| lượt | T4 (phiên T4×2, 2 lượt) | Colab A100 (scale từ 36,4 s) | Colab L4 (scale từ 86,3 s) | VRAM |
|---|---|---|---|---|
| A2C, 500 bước | ~168 s/bước, ~23 h, 3 commit | ~6 h, ~31 đv | ~14 h, ~21 đv | gần 12,7 GiB |
| PPO μ=2, 1.000 bước | ~149 s/bước, ~41 h (khoảng 38–45), 4 commit | ~10 h, ~54 đv; 2 lượt chung máy ~14 h, ~73 đv | ~24 h, ~37 đv | gần 12,7 GiB |
| Cổ điển, 500 bước | như GRPO, ~21 h | như GRPO, ~5 h, ~27 đv | ~12 h, ~18 đv | 12,7 GiB |
| ORPO từ S1, ngoại tuyến, 1.000 cặp | sinh 8 mẫu 2,7–5,3 h + train 500 bước × 2 cặp ~27 s, ~3,7 h | không cần | không cần | [suy] 11–13 GiB |
| DPO/ORPO trực tuyến | ~65 s/bước, ~9 h | ~1,5 h nếu cần | | [suy] ≤ 13 GiB |
| PPO critic đủ cỡ | chưa rõ vừa T4 | chưa có số | | chưa có số |
| Sinh câu + chấm test | ~4–5 h/lượt | Kaggle | | |

Cả A2C và PPO vẫn cần sinh câu và chấm test sau khi train; mốc đã có là trần 8,7 h cho 2 lượt của `luoi-test-t-1` — `report/326:46`.

### Inferences
- PPO λ=1,0 + λ=0,95 cùng A2C: khoảng 65 h phiên T4 + chấm ~13 h, tức gần trọn một tuần hạn mức của cả ba tài khoản (90 h) nếu không làm gì khác.
- Theo luật chọn máy, các lượt này ở bậc T4 vì Kaggle chạy được, chỉ khác là chậm; không cần Colab trừ PPO critic đủ cỡ hoặc khi probe tràn.

### Gaps
- Chưa có giá Colab hiện tại, đơn vị nên đọc lại lúc quyết. Chưa đo ORPO trên T4, chưa có cấu hình fp16 (`ga_dpo.py:221` đang chặn).

## 6. Khảo sát cũ nói gì về PPO và ORPO (`report/reports/Baseline RL so với GRPO.md`)

### Takeaway
Khảo sát 153 bài không cho căn cứ nói GRPO hơn PPO: chênh nhỏ, đổi dấu theo bài. Đòn nguy hiểm là UI-TARS-2 chọn PPO trên GUI. ORPO chỉ xuất hiện trong kế hoạch như một lượt ưu tiên hai.

### Cited Findings
- Mẫu có chủ đích, không phải tổng quan hệ thống: GRPO 36/42 bài RLVR; PPO 16/30, SFT 20/30, DPO 15/30 ở RLHF; 23/32 bài GUI không so với thuật toán RL khác — `report/reports/Baseline RL so với GRPO.md:3,7,19-32`.
- UI-TARS-2 là bài GUI duy nhất chạy cả hai và chọn PPO; chỉ có đường cong train, đa lượt, có pretrain giá trị, preprint — `:34,58`.
- PPO so GRPO: Lian 2025 đổi vị trí theo bộ đo (preprint) · R1 ở λ=1,0 gần GRPO, λ=0,95 kém, lý do còn lại của GRPO là chi phí · Back to Basics PPO 67,6 so RLOO 77,9 nhưng REBEL chép PPO 77,6 — `:53,59-61`.
- ORPO và DPO: Bridging cho DPO trực tuyến hơn ngoại tuyến rõ, có bộ chấm đảo thứ tự; QRPO và Bridging là khuôn đưa DPO vào lưới với cùng một tín hiệu; không bài ngoại tuyến nào trong mẫu so bằng số với REINFORCE, RLOO, GRPO — `:34,40,63`.
- B6: "Khác MIN-DESC cũ (từ S2, mức khai báo)" — `:130`. Khảo sát cấm dùng MIN-DESC, GA-DPO như văn liệu về ORPO, DPO — `:216`. Ở DPO ngoại tuyến phải có tiêu chí "có học": không đạt thì báo "không học", không báo "thua" — `:113`.
- Cấm viết "bỏ critic làm kết quả tốt hơn" và không dùng "nhờ clip" — `:209`; `report/328:244`.
- Mọi số trích ở khảo sát chưa đối chiếu bản đăng — `:218`.

### Inferences
- [suy] Lý do trung thực để chưa chọn PPO hôm nay là chi phí, tiền lệ và thứ tự làm việc, không phải bằng chứng PPO kém.

## 7. Câu có thể nói với thầy hôm nay

### Takeaway
Có thể nói chắc rằng chưa có số PPO, ORPO tầng câu, cổ điển trên cùng điều kiện; đừng nói chúng kém.

### Cited Findings
Bản nói được, mỗi vế đã có số ở trên:

> "Về ORPO, chúng em đã chạy một lần ở tầng khai báo, xuất phát từ S2, cặp dựng bằng heuristic và không dùng thưởng. Một hạt giống: 60,05 so với 59,42 của nhánh SFT cùng số bước (+0,63, KTC [+0,16; +1,10], dưới MDE 2,11), so S1 +0,94 không có ý nghĩa. Biến thể lấy vế âm từ lỗi của mô hình dừng ở điều kiện dựng dữ liệu vì chỉ 3,3% bước đủ điều kiện. Còn ORPO tầng câu, từ S1, chấm SPICE thì **chưa chạy**; trước đây chỉ có một phép phản thực trên tệp thô và một lượt DPO từ ck500 không học được, không có điểm test. Nên không thể nói ORPO kém, chỉ nói chưa có số."

> "Về PPO, mã đã xong: đầu giá trị nhỏ tách gradient, GAE, μ=2, đang probe trên T4, **chưa có số**. Trong cấu hình GRPO đang dùng, μ=1 nên clip không hoạt động; thực chất là policy gradient với mốc trung bình nhóm. Chọn GRPO lúc đầu là vì không cần mô hình giá trị, tiền lệ và chi phí, không phải vì đã thắng PPO."

> "Về RL cổ điển, đã có mã bảy nhánh chỉ đổi trọng số mẫu trong cùng khung, chưa chạy, nên phần lớn phải gọi 'kiểu AWR', 'kiểu RAML'. Những thuật toán hành động liên tục như DDPG, TD3 không áp dụng được với token. DQN, TRPO, SAC chưa làm và có thể cần Colab."

> "Số test đã có: S1 59,11, ck500 60,65 (+1,55 [+0,80; +2,33]), SCST + SPICE 60,54, GRPO + ROUGE-L 60,63, GRPO + METEOR 60,27, GRPO + CIDEr-D số tạm 60,25. Không phép so nào với ck500 loại 0, một hạt giống. Vậy chưa thể nói GRPO + SPICE tốt nhất, chỉ nói thuộc nhóm dẫn đầu của những gì đã chấm."

Không nên nói: "ORPO đã chết" (không kèm tầng) · "GA-DPO thua ck500" (`report/314_KET_QUA_GADPO_13_10.md:42`) · "GRPO hơn PPO" · "PPO có clip nên…" trước khi có số clip · "tốt nhất" (`report/320` §13) · bất kỳ số val nào.

### Inferences
- [suy] Việc nâng sức thuyết phục nhanh nhất, theo thứ tự: chấm test SFT tiếp (đã train, rẻ) → đọc probe PPO và kiểm clip bằng `eps` nhỏ → đẩy PPO, A2C → viết B6 cùng A6 trên một nguồn cặp, có đặt trước tiêu chí "có học".

### Gaps
- Câu trả lời "vì sao" chưa có bằng số cho tới khi xong SFT tiếp, K1, A/A, PPO (`report/320` §13, `report/328` §6).
