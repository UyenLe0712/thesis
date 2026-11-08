# Notebook lưới RL dựng thêm 6/11/2026 (agent A)

Bổ sung cho `CHAY_7_11.md` (5 kernel ưu tiên sáng 7/11; không lặp lại ở đây). Chạy từ `_bundles/luoi`.
Thứ tự theo `report/329` §4 (đợt 1 → 4) và `report/326` dòng 104–107 ("ưu tiên một"). Mỗi kernel 2 lượt, mỗi lượt một T4, trần 11 h.

- md5 của mọi script trên `grpo-luoi-script` và `luoi-kit` (cả ba tài khoản) đã kiểm 6/11 tối, khớp `ds/` và `kit_<user>/`.
  Kit đã có B1 (`grpo_moi_b1.py`), B2 (`grpo_moi_b2.py` md5 821411b8…), B3 (`thuong_moi.py`, `metric_exec.py`, `descriptors_ten.jsonl`).
- Nếu ai sửa script trong `ds/` hoặc kit thì notebook sẽ dừng ở phép kiểm md5 (đúng ý). Lúc đó dựng lại kit, rồi chạy lại đúng lệnh `make_nb.py` của dòng đó.
- Lượt B1/B2/B3 phải có **probe 20 bước trên T4 đạt** (dòng `pb-*`) trước khi đẩy train. GPU tối 6/11 chỉ còn 0,05–0,11 h mỗi tài khoản, nên **các probe này chạy thử sáng 7/11**.

## Thứ tự đẩy

| # | Đợt | Kernel (thư mục `k_<tên>`) | Lượt GPU0 · GPU1 | Điều kiện / ghi chú |
|---|---|---|---|---|
| 1 | 1 | `uyenle0712/luoi-u-4` | SCST + CIDEr-D `scst:cider:101` · REINFORCE không mốc `vanilla:spice:101` | sau khi `luoi-probe-u-2` (CHAY_7_11 #5) đạt |
| 2 | 1+2 | `trangphngngc/luoi-t-4` | A2C `a2c:spice:101` · Dr. GRPO đủ `grpo:spice:101:loss=dr_grpo,scale=none,tag=drg` | A2C đã probe T4 3/11 |
| 3 | T2 | `trangphngngc/venus-ck202` (thư mục `../venus_kernel4`) | UI-Venus chấm 838 câu ck500/202 chưa có kết quả | ~1,5 h; dataset `venus-ck-script4` |
| 4 | T2 | `uyenle0712/som-ck202` (thư mục `../som_kernel3`) | Phi-4 người nghe, 838 câu ck500/202 | ~1 h; dataset `thesis-som-ck202` |
| 5 | probe | `uyenle0712/luoi-pb-1` | `dpo_on:spice:101` · `dpo_off:spice:101` | ưu tiên một (DPO) |
| 6 | probe | `trangphngngc/luoi-pb-2` | `rft_off:spice:101` · GRPO gộp theo câu `grpo_seq:spice:101` | ưu tiên một |
| 7 | probe | `trangphuongngoc/luoi-pb-3` | `grpo:bcmr:101` · RL + CE `rlce:spice:101` | **đọc đỉnh VRAM của rlce** (nvidia-smi trong dòng theo dõi) |
| 8 | probe | `uyenle0712/luoi-pb-4` | `grpo:spice_cong:101` · `grpo:ten_loai:101` | |
| 9 | 1/3 | `trangphuongngoc/luoi-t2-8` | `dpo_on:spice:101` · `dpo_off:spice:101` | sau pb-1 |
| 10 | 3 | `uyenle0712/luoi-u-8` | `rft_off:spice:101` · `grpo_seq:spice:101` | sau pb-2 |
| 11 | 2 | `trangphuongngoc/luoi-t2-5` | DAPO lõi `grpo:spice:101:beta=0,tag=dapo0` · `grpo:bleu4:101` | |
| 12 | 2 | `uyenle0712/luoi-u-5` | `grpo:chrf:101` · `grpo:spider:101` | |
| 13 | 2 | `trangphngngc/luoi-t-8` | `grpo:bcmr:101` · `grpo:spice_cong:101` | sau pb-3, pb-4; `spice_cong` nghĩ ra sau khi thấy số test ck500, phải khai |
| 14 | 2+3 | `trangphngngc/luoi-t-5` | `grpo:bertscore:101` · RFT online `rft:spice:101` | BERTScore đã smoke GPU 6/11 (3 bước, không tràn) |
| 15 | 2+4 | `trangphuongngoc/luoi-t2-9` | `grpo:ten_loai:101` · GSPO `gspo:spice:101:steps=1000,tag=s1000` | sau pb-4, pb-7 |
| 16 | 3+4 | `trangphuongngoc/luoi-t2-6` | `cem:spice:101` · chuẩn hoá theo lô `grpo:spice:101:scale=batch,tag=sb` | |
| 17 | probe | `trangphngngc/luoi-pb-5` | `es:spice:101` · SeqGAN `seqgan:spice:101` | **đọc σ của ES**: `es/so_cau_khac` > 1, `es/buoc_l2` > 0 |
| 18 | probe | `trangphuongngoc/luoi-pb-6` | MIXER `mixer:spice:101` · `quark:spice:101` | |
| 19 | probe | `uyenle0712/luoi-pb-7` | `gspo:spice:101:steps=1000,tag=s1000` · MRT `mrt:spice:101` | MRT: xem `luoi/mrt_q_max`; ≈ 1/G thì α quá nhỏ (B1 gợi ý 0,1–1) |
| 20 | probe | `trangphngngc/luoi-pb-8` | softmax PG `spg:spice:101` · `grpo:loai:101` | |
| 21 | 4 | `uyenle0712/luoi-u-6` | kiểu AWR `awr:spice:101` · kiểu RAML `raml:spice:101` | |
| 22 | 4 | `trangphngngc/luoi-t-6` | `rank:spice:101` · `mad:spice:101` | |
| 23 | 4 | `trangphuongngoc/luoi-t2-7` | μ=2 `grpo:spice:101:mu=2,steps=1000,tag=mu2` · Clip-Higher `…:mu=2,eps=0.28,steps=1000,tag=ch` | |
| 24 | 4 | `uyenle0712/luoi-u-9` | `rlce:spice:101` · `mixer:spice:101` | sau pb-3, pb-6 |
| 25 | 4 | `trangphngngc/luoi-t-9` | `seqgan:spice:101` · `quark:spice:101` | sau pb-5, pb-6 |
| 26 | 4 | `trangphuongngoc/luoi-t2-10` | `es:spice:101` · `mrt:spice:101` | sau pb-5, pb-7 (có thể phải đổi σ / α, dựng lại với `essig=`/`mrta=`) |
| 27 | 4 | `uyenle0712/luoi-u-7` | độ nhạy `grpo:spice:101:G=4,tag=g4` · `grpo:spice:101:G=16,tag=g16` | |
| 28 | 4 | `uyenle0712/luoi-u-10` | `spg:spice:101` · `grpo:loai:101` | `loai` chỉ để giải thích (T5) |

```
kg <tk> kernels push -p k_<tên kernel> --accelerator NvidiaTeslaT4
kg trang  kernels push -p ../venus_kernel4 --accelerator NvidiaTeslaT4
kg uyenle kernels push -p ../som_kernel3   --accelerator NvidiaTeslaT4
```
Kaggle chỉ cho mỗi tài khoản chạy một phiên GPU một lúc [suy, chưa thấy hai phiên song song], nên mỗi tài khoản đẩy theo thứ tự trong bảng.
Đọc T2: tải output về `runs/venus/ck202_7_11/` (giải nén để có `out/score_m1_raw.jsonl`), chép `som/chon_phi4_ck202_diff.jsonl`
vào `runs/som/`, rồi chạy `python3 -I harness/t2_ck202_doc.py` (tra theo (bước, câu); bước có câu trùng nhánh đã chấm thì dùng lại kết quả).
Dựng lại notebook: `python3 make_nb.py <user> <kernel> <train|probe> <lượt0> <lượt1 | -> [kernel trước]`.
Nối tiếp khi chạm trần: `MOI= python3 make_nb.py <user> <kernel mới> train <lượt0> <lượt1> <kernel trước>`. Log của lượt nối tiếp phải có `[nạp default] … → x>0`.
Probe dài 20 bước, trần 2 h (`PROBE_H=2.0`). Đọc trong log: s/bước, dòng nvidia-smi, không Traceback/OOM, và dòng `[moi_b1]` / `[đè cấu hình]`.

## Lượt nên chạy Colab (theo `_bundles/colab_luoi/HUONG_DAN.md`)

Nguyên tắc: Kaggle không tính phí, nên chỉ đưa lên Colab những lượt mà Kaggle phải nối từ 3 commit 11 h trở lên (> ~30 h), hoặc tràn VRAM T4. Lần đầu chạy `CHE_DO = "tham_do"` trên L4. Đỉnh VRAM ≤ 17 GiB thì giữ L4, chỉ lên A100 khi tỉ số giờ L4/A100 > 1,5.

| Ưu tiên | Lượt (`LUOT`) | Vì sao Colab | Bỏ khỏi Kaggle |
|---|---|---|---|
| C1 | `ppo:spice:101:mu=2,lam=1.0,steps=1000,tag=l1` | khoảng 41 h trên T4, tức 4 commit qua hai tuần | nếu chạy Colab thì `luoi-t-3` (CHAY_7_11 #3) chỉ giữ lượt l95, hoặc dừng sau commit đầu và chép điểm lưu sang Drive (tên thư mục trùng) |
| C2 | `ppo:spice:101:mu=2,lam=0.95,steps=1000,tag=l95` | như trên | như trên |
| C3 | `gspo:spice:101:steps=1000,tag=s1000` | 25–30 h [suy], μ=2 | thay vế phải của `luoi-t2-9` bằng `-` nếu chạy Colab |
| C4 | `dpo_on:spice:101` · `dpo_off:spice:101` | khoảng 26 h mỗi lượt [suy] | `luoi-t2-8` |
| C5 | `rlce:spice:101` | chỉ khi `pb-3` báo đỉnh VRAM > ~14 GiB hoặc OOM trên T4 | vế trái `luoi-u-9` |
| C6 | `es:spice:101` | chỉ khi `pb-5` cho s/bước quá cao (CPU 6/11: 2 bước mất 927 s, chậm gấp 6 lần các lượt khác) | vế trái `luoi-t2-10` |

Đổi lượt nào sang Colab thì dựng lại kernel Kaggle tương ứng với lượt còn lại (`-` cho GPU trống), đừng chạy trùng hai nơi.

## Hạn mức

Mỗi lượt 500 bước ở khoảng 150–190 s/bước tốn 21–26 h một GPU, tức 2–3 commit 11 h. Riêng gspo, μ=2, ES chưa đo.
Tuần 7/11 có 90 h. `CHAY_7_11.md` dùng khoảng 37 h, T2 khoảng 2,5 h, tám probe khoảng 9 h. Phần còn lại đủ cho chừng bốn commit train đầu (#1, #2, #9, #10). Các dòng sau sang tuần kế.

## Cách đặt cấu hình (phải khai khi viết)

- Mặc định của `grpo_luoi.py` đã là `loss_type="dapo"`. Vì vậy "DAPO lõi" = mặc định + β=0. Không có dynamic sampling (TRL 0.29.1 không có), và Clip-Higher không tác dụng khi μ=1.
- "Dr. GRPO đủ" (`drg`) = `loss_type="dr_grpo"` + bỏ chia std, giữ β=0,04. Cấu hình này trùng bí danh `drgrpo_full` của B1, nên không chạy hai lần.
- GSPO dùng bí danh `gspo` của B1 (tỉ số theo câu, clip [1−3e−4; 1+4e−4], μ=2, 1.000 bước). Smoke 6/11 dùng `is=sequence` với ngưỡng clip mặc định của TRL; đó **không** phải GSPO đúng nghĩa, nên đã bỏ khỏi lượt train.
- μ=2 (mu2, Clip-Higher, GSPO) đặt `steps=1000` để vẫn đi qua đủ 1.000 câu nhắc, như PPO.
- G=4 và G=16 giữ 500 bước và lô sinh 16 chuỗi, tức cùng ngân sách tính toán. G=4 đi 2.000 lượt câu nhắc, G=16 chỉ 500.
- `make_nb.py` thêm 6/11 (bản cũ ở scratchpad `make_nb_truoc_A.py`):
  - `PROBE_H`.
  - Lượt thứ hai `-`.
  - B1/B2/B3 trong `tep_cua()` và FILES, kèm selftest B1, B2, bcmr, B3.
  - Cờ k mới `dpob mrta spgt epsl celam rho0 mfrac ganmix ganwarm ganlr qk qpool espop esm essig eslr`.
  - md5 của tệp chỉ có ở kit lấy từ `kit_<user>/`. Khi tệp trùng tên ở nhiều dataset thì chọn theo md5.
  - Dựng lại `luoi-probe-u-2` thì phần chạy không đổi, chỉ thêm các nhánh `if` cho B1/B2/B3.
- `make_cpu_nb.py` (mới) dựng kernel CPU chạy đúng script và cờ của notebook train trên Qwen2.5-VL tí hon, 2 bước. Nó bắt được cờ sai, khoá cấu hình TRL sai và thưởng ném lỗi. Nó không bắt được VRAM hay tốc độ.

## Kernel đã chạy 6/11 tối (agent A) và kết quả — KHÔNG chạy lại

| Kernel | Máy | Kiểm gì | Kết quả | Tệp |
|---|---|---|---|---|
| `uyenle0712/luoi-smoke-a-u` | T4×2, probe, trần 0,25 h | `grpo:bertscore:101` (roberta-large thêm trên GPU) · `grpo:spice:101:mu=2,is=sequence` | **ĐẠT**: tới bước 3 và bước 2, không Traceback/OOM. BERTScore 158–160 s/bước, thưởng 0,46–0,69 (số train), mỗi lần chấm 16 câu ≤0,3 s; μ=2 130 s/bước, `[đè cấu hình]` đúng. Dừng ở trần như dự kiến (mã −15). Dòng nvidia-smi không in số GPU nên **chưa có đỉnh VRAM**. Lượt `is=sequence` chỉ là phép kiểm đường chạy, đã thay bằng GSPO của B1 | `runs/luoi/smoke_6_11/smoke_a_u/` |
| `trangphngngc/luoi-cpu-cau-hinh` | CPU, Qwen2.5-VL tí hon, 2 bước/lượt | 21 cấu hình của notebook #1–#2, #11–#12, #14, #16, #21–#23, #27 (đúng script + cờ của notebook train) | **21/21 ĐẠT**: mã 0, đủ 2 bước, 0 Traceback; selftest lợi thế, cổ điển, GAE đạt. `[đè cấu hình]` in đúng cho drg (`dr_grpo` + `none`), sb (`batch`), mu2 (μ=2), ch (μ=2, ε_high 0,28). Thưởng bleu4, chrf, spider, bertscore chạy thật. 70–156 s/lượt | `runs/luoi/smoke_6_11/cpu_cau_hinh/` |
| `trangphuongngoc/luoi-cpu-moi` | CPU, cùng cách | 16 cấu hình B1/B2/B3 chạy đúng `tep_cua()` + cờ như notebook train | **16/16 ĐẠT**: mã 0, đủ 2 bước, không Traceback. Selftest B1 (∇ trùng autograd), B2 (đợt 4, hàm thuần), cổ điển, GAE đều đạt. `[moi_b1]` in đúng: gspo → `sequence`, ε 3e−4/4e−4, μ=2; grpo_seq → `loss_type=grpo`. bcmr, ten_loai, loai chạy thật trên CPU. ES chậm nhất: 927 s cho 2 bước (16 lần sinh mỗi bước), các lượt khác 71–162 s | `runs/luoi/smoke_6_11/cpu_moi/out/` |
| `trangphngngc/venus-ck202`, `uyenle0712/som-ck202` | — | — | chưa đẩy (GPU hết); dataset đã tạo | — |

Chưa kiểm được trên T4 (để probe sáng 7/11): đỉnh VRAM (nhất là rlce, BERTScore), s/bước, σ của ES, `mask_truncated_completions`, fp16.
Đỉnh VRAM đọc ở dòng `[xong] … đỉnh VRAM x GiB` mà `--probe` in khi chạy đủ 20 bước, nên probe B1/B2/B3 dựng với `PROBE_H=2.0` (trần 2 h). Dòng nvidia-smi trong ô theo dõi in rỗng ở smoke 6/11, đừng dựa vào nó.
Lưu ý lần sau: `kernels output` luôn kèm `--file-pattern '\.(log|json|txt|md)$'`. Kernel CPU bản đầu để ảnh xám trong `/kaggle/working`, nên output có 4.000 ảnh; `make_cpu_nb.py` nay đặt chúng ở `/tmp`.

## Bổ sung 7/11/2026: mã còn thiếu so với `report/326` B-list, `report/328` T6, `report/330` §7 hàng 7

| Tệp mới | Nội dung | Tự kiểm |
|---|---|---|
| `harness/grpo_moi_b4.py` (md5 e5d2443a…) | `orpo_on`, `orpo_off` (ORPO, λ 0,1, cặp best/worst trong nhóm), `dpo_semi` (DPO bán trực tuyến, adapter `gen` đồng bộ mỗi K = 10 lần sinh [suy]), `gpg` (α = B/(B−M), mặc định không chia std theo Table 1 của bài gốc). β KL mặc định 0 cho cả bốn. Cờ k: `orpol` `dsync` `gstd` | công thức ∇ trùng autograd; CPU mô hình tí hon (transformers 5.14.1, không phải 5.20.2) ĐẠT 4/4, kể cả nối tiếp của `dpo_semi` |
| `harness/thuong_t6.py` (64d0caf4…) | thưởng `spice_kp` (SPICE không phạt độ dài) và `phat_dai` (chỉ phạt độ dài) | SPICE thật (Java) ĐẠT, bốn thứ tự nạp cùng `thuong_moi.py` ĐẠT |
| `harness/grpo_tu_base.py` (71a0bbb0…) | xuất phát từ Qwen gốc: ép `--merged Qwen/Qwen2.5-VL-3B-Instruct`, in `[xuất phát] Base …`; lượt viết `grpo:spice:101:tu=base,tag=base` | nạp giả ĐẠT, chưa nạp mô hình thật |
| `_bundles/nghe_s1/` | probe người nghe Phi-4 từ S1 (T4×2, Phi-4 venv transformers 4.48.2 ở GPU1, train `--train --max-steps 20` ở GPU0), xem `HUONG_DAN.md` | `grpo_nghe --selftest` 13/13 CPU; chưa chạy Kaggle |

`make_nb.py`, `make_kit.py`, `make_cpu_nb.py` đã nhận B4 / T6 / `tu=base` (bản cũ ở scratchpad phiên 7/11). Dựng lại các notebook cũ cho ra ô 1–2 giống hệt, ô 3–4 chỉ thêm nhánh `if` không tác dụng. Kit ba tài khoản đã dựng lại ở máy nhà; **chỉ `trangphngngc/luoi-kit` đã đẩy phiên bản mới** (7/11), hai tài khoản kia phải `kg <tk> datasets version -p kit_<tk>` trước khi chạy probe mới.

Probe GPU đã dựng, CHƯA đẩy (chờ user):
- `uyenle0712/luoi-pb-9`: `orpo_on:spice:101` · `orpo_off:spice:101`
- `trangphngngc/luoi-pb-10`: `dpo_semi:spice:101` · `gpg:spice:101`
- `trangphuongngoc/luoi-pb-11`: `grpo:spice:101:tu=base,tag=base` · `grpo:phat_dai:101` (`spice_kp` không cần probe riêng)
- `trangphuongngoc/nghe-s1-probe` (`_bundles/nghe_s1/`, cần tạo dataset `nghe-s1-kit` trước)
Kiểm CPU: `trangphngngc/luoi-cpu-b4` (8 cấu hình B4 + T6) đẩy 7/11, **8/8 ĐẠT** (mã 0, đủ 2 bước, 0 Traceback, 71–244 s/lượt; log `runs/luoi/7_11/cpu_b4/`). tu=base kiểm riêng bằng mô hình thật: `trangphngngc/kiem-tu-base-cpu` (`harness/kiem_tu_base_cpu.py`).

Không viết (chờ user): DAPO đủ (dynamic sampling, TRL 0.29.1 không có), DQN / soft Q, TRPO, SAC, ILQL, PPO critic đủ cỡ. CIDEr-R bỏ vì điều kiện "CIDEr-D ≥ SPICE" không đạt (60,27 < 60,65).
