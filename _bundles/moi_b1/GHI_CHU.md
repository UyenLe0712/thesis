# Agent B1 — mã RL mới, nhóm câu/ưu tiên (6/11/2026)

Mã: `harness/grpo_moi_b1.py` (bản chép ở `_bundles/moi_b1/ds/`, dataset `trangphngngc/moi-b1-code`).
Không sửa `grpo_luoi.py` · `grpo_codien.py` · `grpo_ppo.py` · `make_nb.py`. Tệp import `grpo_codien` rồi gọi `CD.main`,
nên điểm xuất phát, 1.000 câu nhắc, G, lr, lô, số bước, phần thưởng, điểm lưu 25 bước, dòng `[nạp default]` giữ như ck500.

## Thuật toán

Với μ = 1 tỉ số quan trọng bằng 1, nên gradient của mất mát DAPO của TRL là −(1/N_tok)·Σ A_i ∇log π(y_i). Mỗi thuật toán
chỉ đặt A_i sao cho gradient trùng ĐÚNG gradient mục tiêu gốc. `--selftest-algo` kiểm điều này bằng autograd.

| `--algo` | phương pháp | mới hay cờ | β KL mặc định | tốn thêm mỗi bước |
|---|---|---|---|---|
| `dpo_on` | DPO trực tuyến từ S1 (cặp = thưởng cao nhất / thấp nhất của G câu, tham chiếu S1) | mã mới | 0 | 2 lượt forward (chính sách + S1) |
| `dpo_off` | DPO ngoại tuyến từ S1 (câu sinh từ S1 đóng băng; tương đương tập cặp dựng sẵn, một lượt) | mã mới | 0 | 2 lượt forward |
| `rft_off` | RFT một vòng (sinh từ S1 đóng băng, SFT câu tốt nhất nhóm) | mã mới | 0,04 | không |
| `rft` | Online RFT | đã có ở grpo_codien | 0,04 | — |
| `mrt` | Minimum Risk Training, α = 0,005 | mã mới | 0,04 | 1 lượt forward |
| `spg` | Softmax policy gradient, τ = 0,2, mốc 1/G | mã mới | 0,04 | không |
| `drgrpo_full` | Dr. GRPO đủ: bỏ chia std + `loss_type=dr_grpo` | bí danh cờ TRL | 0,04 | không |
| `grpo_seq` | GRPO gộp theo câu (`loss_type=grpo`) | bí danh cờ TRL | 0,04 | không |
| `gspo` | GSPO: tỉ số theo câu, clip [1−3e−4; 1+4e−4], μ = 2 | bí danh cờ TRL | 0,04 | — (cần `--max-steps 1000`) |

Cờ mới: `--dpo-beta` (0,1) · `--mrt-alpha` (0,005) · `--spg-tau` (0,2) · `--eps-low` · `--selftest-cpu [--algos a,b]`.
Mọi cờ khác như `grpo_codien.py` (`--reward`, `--max-steps`, `--resume auto`, `--loss-type`, `--mu`, `--is-level`, `--eps-high`…).

Ghi chú phải khai khi viết:
- `spg` và `raml` (grpo_codien) có cùng kỳ vọng gradient, chỉ khác mốc trừ 1/G và thang. RAML đúng nghĩa (mẫu từ q* quanh câu chuẩn) chưa viết.
- `mrt` không khử mẫu trùng trong G câu như bài gốc. Thang của A nhỏ (α·Q), mà Adam chuẩn hoá thang nên ảnh hưởng chủ yếu qua tỉ lệ với số hạng KL β = 0,04. [suy] Có thể phải thử α lớn hơn.
- DPO: lr mặc định vẫn 1e-5 như ck500 (đổi một yếu tố); các bài DPO thường dùng 5e-7 đến 5e-6. GA-DPO cũ (314) không học ở 5e-6 vì thiếu bước. Nếu dpo_* phân kỳ thì hạ lr, phải khai.
- `gspo` với μ = 1 trùng hệt ck500, nên bí danh ép μ = 2. Với μ = 2 phép clip mới hoạt động, khác ck500 ở hai yếu tố (μ và mức tỉ số), giống PPO.
- Câu bị cắt ở 96 token (mask 0 khi chạy GPU) không được chọn làm chosen/rejected.

## Lệnh mẫu (Kaggle, cùng bộ khung như make_nb)

```
python grpo_moi_b1.py --train --algo dpo_on  --reward spice --bundle B --merged M --out O --resume auto
python grpo_moi_b1.py --train --algo dpo_off --reward spice --bundle B --merged M --out O --resume auto
python grpo_moi_b1.py --train --algo rft_off --reward spice --bundle B --merged M --out O --resume auto
python grpo_moi_b1.py --train --algo gspo --max-steps 1000 --reward spice --bundle B --merged M --out O --resume auto
```
make_nb hiện gọi `grpo_luoi.py`/`grpo_codien.py`: để dùng tệp này cần thêm `grpo_moi_b1.py` vào kit và đổi tên script theo
thuật toán (agent chính gộp). Dòng log đầu là `[moi_b1] --algo … → … · đè TRL … · siêu tham số …`, kiểm dòng này trước khi đọc.

## Ước lượng GPU (T4, một lượt 500 bước) [suy]

ck500 ~160 s/bước ⇒ ~22 h. `rft_off` · `spg` · `drgrpo_full` · `grpo_seq` ≈ ck500. `mrt` thêm một lượt forward
không gradient trên 16 chuỗi, khoảng +10%. `dpo_*` thêm hai lượt, khoảng +20% (~26 h). `gspo` 1.000 bước, nửa số bước
không sinh câu, khoảng 25–30 h. Mỗi lượt cần 2–3 commit 11 h. Chưa đo; phải probe 20 bước (`--probe`) trước.

## Kết quả kiểm

- `py_compile` ở máy nhà: đạt.
- Kaggle CPU `trangphngngc/moi-b1-cpu`: xem mục dưới.
- Kaggle CPU `trangphngngc/moi-b1-cpu` bản 2 (6/11 tối, ~3 phút): **đạt cả hai phép kiểm**. Tệp ở `runs/luoi/smoke_6_11/moi_b1_cpu/`.
  - `--selftest-algo`: gradient của dpo, mrt, spg trùng autograd (atol 1e−6). Nhóm thưởng hoà thì không có cặp; câu bị cắt không được chọn.
  - `--selftest-cpu`: 11 thuật toán, mỗi cái 3 bước (gspo 6 bước vì μ = 2) trên `tiny-Qwen2ForCausalLM-2.5`. Loss và lợi thế hữu hạn, LoRA B đổi từ 0.
    Gồm dpo_on · dpo_off · rft_off · mrt · spg · drgrpo_full · grpo_seq · gspo, cùng grpo · drgrpo · rft làm đối chiếu.
  - Sinh từ S1 thật sự tắt LoRA: số lần nhánh lora_B chạy trong lúc sinh là **0** ở dpo_off và rft_off, **144** ở mọi thuật toán khác.
  - Cấu hình TRL của bí danh được áp, đọc lại từ `trainer.args`: drgrpo_full `dr_grpo` + `none`; grpo_seq `grpo`; gspo `sequence`, ε 3e−4/4e−4, μ = 2.
  - Số trùng nhau giữa dpo_on và dpo_off, rft_off và rft, grpo_seq và grpo, drgrpo_full và drgrpo là do mô hình tí hon, không phải lỗi.
    Cùng hạt giống thì LoRA nhỏ không đổi token lấy mẫu, nên hai nguồn sinh ra câu giống nhau. Mô hình tí hon cũng không sinh EOS,
    nên mọi câu dài đúng 12 token, và khi đó các cách chuẩn hoá theo độ dài cho cùng một giá trị. Phép đếm lora_B và phép đọc lại cấu hình mới là bằng chứng.
  - mrt: `luoi/mrt_q_max` = 0,25 = 1/G, tức Q gần đều khi α = 0,005. Khi đó MRT gần với drgrpo nhân một thang nhỏ. [suy] Trên Qwen 3B tổng log-prob câu chỉ khoảng −5 đến −20, nên Q vẫn gần đều; nên cân nhắc α ≈ 0,1–1.
- **Chưa kiểm:** đường dòng lệnh đầy đủ `main → grpo_codien.main → grpo_luoi.train` với Qwen2.5-VL (cần GPU). Phải chạy `--probe` 20 bước trên T4 trước lượt thật.
