# B2: mã RL đợt 4 + thưởng BCMR (6/11/2026)

Tệp: `harness/grpo_moi_b2.py`. Mã này không sửa `grpo_luoi.py`, `grpo_codien.py`, `grpo_ppo.py` hay `make_nb.py`.
Tệp mới chỉ thêm thuật toán và thưởng rồi gọi `grpo_codien.main()`, nên S1, 1.000 câu nhắc (cùng thứ tự ck500), G = 8, lr,
β = 0,04 và 500 bước giữ như ck500. Kiểm CPU: kernel `trangphuongngoc/moi-b2-cpu`, dataset `trangphuongngoc/moi-b2-code`.

## Đã viết (theo thứ tự ưu tiên report/329 §4)

| `--algo` / `--reward` | Phương pháp | Bản rút gọn, phải khai |
|---|---|---|
| `--reward bcmr` (với `--algo grpo`) | BCMR của Liu 2017 (đợt 2, trục thưởng) | (0,5·B1 + 0,5·B2 + B3 + B4 + CIDEr-D + 5·METEOR + 2·ROUGE-L)/20. BLEU-n mức câu của sacrebleu; chia 20 để về thang [0, 1] như SPICE |
| `seqgan` | SeqGAN (E9) | Thưởng mức câu D(câu ∣ màn hình), không rollout Monte Carlo; D là MLP trên trạng thái ẩn tách gradient của policy; **đổi cả phần thưởng** |
| `mixer` | MIXER (E7) | Ép k = ⌊ρ·số token⌋ token đầu câu chuẩn rồi sinh tiếp; token ép học CE, phần sinh học lợi thế GRPO; ρ giảm tuyến tính 0,5 → 0 trong nửa đầu lượt |
| `rlce` | Trộn RL + CE (E8) | GRPO + λ·CE câu chuẩn, λ = 0,1 [suy] |
| `quark` | Quark (E10) | K = 5 mức phân vị trên kho 2.048 thưởng gần nhất; mức cao nhất = câu nhắc gốc (không token mới, test không đổi); không kho phát lại |
| `es` | ES trên trọng số LoRA (E11) | pop 16 đối xứng, m = 2 câu nhắc/bước, greedy, z-score trong quần thể, θ += lr·(1/n)·Σ zε (công thức Qiu, không chia σ), σ 1e-3, lr 5e-4 (chưa probe) |

MRT và softmax PG không thuộc phần việc B2.

## Cờ mới

`--ce-lam` (rlce) · `--mixer-rho0`, `--mixer-frac` · `--gan-mix` (0 = SeqGAN thuần; α>0 trộn SPICE), `--gan-warm` (20 bước đầu chỉ học D), `--gan-lr` ·
`--quark-k`, `--quark-pool` · `--es-pop`, `--es-m`, `--es-sigma`, `--es-lr`, `--es-save`. Mọi cờ khác giống `grpo_codien.py`.

Mẫu lệnh, khớp đúng cách `make_nb.py` gọi:
```
python grpo_moi_b2.py --train --no-q4 --bs 4 --accum 4 --gen-chunk 8 --algo seqgan --reward spice --seed 101 \
  --bundle B --merged M --out O --resume auto --keys-ck500 K
python grpo_moi_b2.py --train --no-q4 --algo grpo --reward bcmr --seed 101 --bundle B --merged M --out O --resume auto
python grpo_moi_b2.py --train --no-q4 --algo es --reward spice --seed 101 --bundle B --merged M --out O --resume auto
```
Điểm lưu: TRL lưu mỗi 25 bước như cũ. SeqGAN lưu thêm `discriminator.pt`, Quark lưu `quark_pool.json`, ES lưu `checkpoint-N/`
(gồm `adapter_model.safetensors`, `trainer_state.json` có `global_step`, `es_state.json`). Khi chạy tiếp, lượt nào cũng in dòng
`[nạp default] … → x>0`. Adapter ra cùng dạng LoRA mới trên `s1_merged`, nên `gen_test_grpo.py` dùng được ngay. Quark cũng không cần thêm thẻ lúc sinh test.

## Muốn `make_nb.py` gọi được (B2 KHÔNG sửa `make_nb.py`, chủ của tệp đó làm)

1. Thêm `"rlce", "mixer", "seqgan", "quark", "es"` vào danh sách algo hợp lệ, và `"bcmr"` vào danh sách thưởng.
2. `tep_cua(r)` trả `grpo_moi_b2.py` cho năm algo trên và cho `rw == "bcmr"`. `FILES` thêm `grpo_codien.py` + `grpo_moi_b2.py`.
3. Selftest: `python grpo_moi_b2.py --selftest-algo`. Với bcmr: `--selftest-thuong --rewards bcmr`, cần Java như METEOR.
4. Thêm cờ mới vào bảng `CO` nếu muốn đặt qua `tag=`.
5. Ô theo dõi đọc dòng `{'loss'…}`. ES cũng in dòng dạng đó (`reward`, `step_time`, `luoi/adv_abs_mean` = |u| TB), nên ô theo dõi dùng chung được.

## Kết quả kiểm CPU

Kernel `trangphuongngoc/moi-b2-cpu`, chạy 6/11/2026, hai lần, CPU, mô hình Qwen2.5-VL tí hon khởi tạo ngẫu nhiên (2 tầng, processor thật).
SPICE thay bằng thưởng giả băm câu, nên không cần Java. Các thưởng bcmr, cider, rougel, meteor chạy thật. Tệp: `runs/luoi/moi_b2_cpu/` (lần 1), `runs/luoi/moi_b2_cpu_v2/` (lần 2, bản cuối).

- **Lần 1: 11/11 phép kiểm đạt, nhưng bắt được một lỗi thiết kế ở ES.** Cập nhật kiểu Salimans chia σ, với lr 5e-4 và σ 1e-3, làm mỗi bước dịch L2 khoảng 6
  ngay trên mô hình tí hon. Ngoại suy lên 15 triệu tham số LoRA thì khoảng 170 mỗi bước, đủ phá adapter. Đã sửa theo đúng công thức của Qiu 2025 (nguồn của lr):
  z-score, không chia σ. Thêm log `es/buoc_tuong_doi` = ‖Δθ‖/‖θ‖.
- **Lần 2 (md5 `grpo_moi_b2.py` 821411b8…): 11/11 đạt.**
  - selftest hàm thuần (lợi thế, ρ của MIXER, mức Quark có hoà, z-score, chèn thẻ) đạt. selftest thưởng bcmr, cider, rougel, meteor đạt: bcmr cho câu trùng = 1,0, câu rỗng = 0, câu dài = 0,156.
  - grpo (đối chứng), bcmr, rlce, mixer, seqgan, quark: mỗi lượt 3 bước, mã thoát 0, có `[xong]`, mọi số trong log hữu hạn, grad_norm > 0.
  - rlce: có `rlce/ce`. CE khoảng 11,9 vì mô hình ngẫu nhiên, đúng cỡ ln(151.936).
  - mixer: k TB 1,5 token khi ρ 0,5; về 0 khi ρ nhỏ. Dựng lại mm_token_type_ids trùng processor ✓, tiền tố ép trùng câu chuẩn ✓.
  - seqgan: bước khởi động có A = 0 và grad 0; các bước sau D học (d_loss 1,386 → 1,3856) và |A| > 0.
  - quark: các mức đều có mặt; KL tính trên câu nhắc đã chèn thẻ.
  - seqgan và quark chạy 25 bước, lưu điểm lưu, rồi chạy tiếp tới 27 bước: in `[nạp default] … → x>0`, nạp lại `discriminator.pt` và `quark_pool.json` (200 thưởng).
  - es: chạy 3 bước, lưu, rồi chạy tiếp tới bước 4 (`[nạp default]`, global_step 4). `es/buoc_tuong_doi` 0,005–0,007 mỗi bước, 4 câu khác nhau giữa các thành viên, nên bước khác 0.
- **Chưa kiểm** (vì CPU tí hon không kiểm được): VRAM và s/bước trên T4, `mask_truncated_completions` (tắt trên CPU), fp16, SPICE thật.
  Trước khi chạy lượt thật, phải probe 20 bước trên T4 cho từng thuật toán.

## Ước lượng GPU T4 [suy, chưa probe]

Mốc: ck500/GRPO khoảng 160 s/bước trên T4 (29/9), 500 bước khoảng 22 h.
- bcmr: như GRPO + METEOR (Java), khoảng 22–24 h.
- rlce: thêm một forward + backward câu chuẩn mỗi lô nhỏ (câu nhắc dài khoảng 1.000 token ảnh). Khoảng +15–25% thời gian và đỉnh VRAM tăng,
  **phải probe VRAM** (ck500 đã 13,2/15 GiB).
- mixer: như GRPO (phần sinh còn ngắn hơn vì có tiền tố).
- seqgan: thêm hai forward không gradient mỗi lô sinh (câu mẫu và câu chuẩn), khoảng +20%.
- quark: thêm một forward ref mỗi lô sinh (thay cho forward ref của TRL), khoảng +5–10%.
- es: không backward. Mỗi bước gồm 16 lần sinh greedy, mỗi lần 2 câu. Chưa đo, có thể nhanh hơn GRPO. **Phải probe σ**: σ nhỏ quá thì
  mọi thành viên sinh cùng câu và bước bằng 0 (theo dõi `es/so_cau_khac` và `es/buoc_l2`).
