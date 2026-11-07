# Colab: train một lượt lưới RL (6/11/2026)

Tệp:
- `colab_luoi_train.ipynb`: notebook, mở bằng Colab (File → Upload notebook).
- `make_colab_nb.py`: dựng lại notebook: `python3 make_colab_nb.py [uyenle0712|trangphngngc|trangphuongngoc]`. Phải dựng lại mỗi khi kit `luoi-kit` hoặc dataset `grpo-luoi-script` đổi, vì md5 nhúng sẵn.
- `colab_logic.py`: phần logic, được nhúng nguyên văn vào ô 2.
- `kiem/`: script train giả và phép kiểm logic. Đã chạy trên Kaggle CPU, xem mục cuối.

## Nên chạy lượt nào trên Colab

Chỉ chạy những lượt mà Kaggle phải nối nhiều commit 11 h. Lượt khoảng 22 h vẫn để Kaggle chạy hai commit, vì Kaggle không tính phí.

| Lượt (`LUOT`) | T4 Kaggle [suy] | Ghi chú |
|---|---|---|
| `ppo:spice:101:mu=2,lam=1.0,steps=1000,tag=l1` | khoảng 41 h (299 s/lô, probe 3/11) | 4 commit Kaggle, qua hai tuần hạn mức |
| `ppo:spice:101:mu=2,lam=0.95,steps=1000,tag=l95` | khoảng 41 h | như trên |
| `gspo:spice:101:steps=1000,tag=s1000` | 25–30 h (`_bundles/moi_b1/GHI_CHU.md`) | bí danh ép μ=2 nên cần 1.000 bước |
| `dpo_on:spice:101`, `dpo_off:spice:101` | khoảng 26 h | lr 1e-5 như ck500; phân kỳ thì hạ lr và khai |
| `seqgan:spice:101`, `rlce:spice:101`, `quark:spice:101`, `mixer:spice:101`, `es:spice:101`, `grpo:bcmr:101` | 22–27 h (`_bundles/moi_b2/GHI_CHU.md`, chưa probe) | `grpo_moi_b2.py` (md5 `821411b8…`). Thường để Kaggle; dùng Colab khi rlce tràn VRAM T4 hoặc cần nhanh. ES phải thăm dò σ trước |

Tên thư mục ra trùng `make_nb.py` (`ppo_spice_101_l1`…), nên điểm lưu từ Kaggle chép được sang Drive để chạy tiếp, và ngược lại.
Chạy tiếp từ điểm lưu Kaggle: tải output kernel, đặt các `checkpoint-*` vào `MyDrive/thesis/luoi_colab/<thư mục>/`, rồi Run all.
Một số thuật toán cần thêm tệp trong điểm lưu, và notebook chỉ coi điểm lưu là đủ khi có các tệp đó (`colab_logic.tep_them`):
PPO/A2C cần `value_head.pt`, SeqGAN cần `discriminator.pt`, Quark cần `quark_pool.json`. ES thì cần `es_state.json` và không có `optimizer.pt`.
Cờ riêng của B2 đặt qua `LUOT`, ví dụ `es:spice:101:es_sigma=0.002,tag=s2` hoặc `rlce:spice:101:ce_lam=0.2,tag=c2`. Cờ không thuộc thuật toán đó sẽ bị chặn. `bcmr` chỉ đi với `grpo`.

## Chọn máy (luật CLAUDE.md)

1. `CHE_DO = "tham_do"` trên **L4**: 20 bước trên 50 câu nhắc dài nhất, khoảng 30–60 phút [suy]. Ô 5 in s/bước, đỉnh VRAM, số giờ cho cả lượt và khuyến nghị.
2. Đỉnh VRAM > 17 GiB thì chọn A100. Nếu đủ VRAM thì giữ L4, trừ khi đã đo cả A100 (thăm dò lại trên A100, kết quả cộng vào `tham_do_<lượt>.json` trên Drive) và tỉ số giờ L4/A100 > 1,5.
3. Đơn vị Colab = số giờ × đơn vị/giờ đang hiện trên Colab lúc chạy. Giá phải đọc tại chỗ, đừng nhớ.
4. L4/A100 chạy bf16, còn Kaggle T4 chạy fp16. Lượt Colab không trùng từng bit với lượt Kaggle cùng tên, nên khi báo số phải khai máy. Đừng đổi máy giữa một lượt.

## Khi chạy

- Ô 6 chạy foreground suốt lượt, in mỗi 2 phút (giờ VN, bước, s/bước, còn bao lâu, thưởng, KL, điểm lưu mới nhất trên Drive). Giữ tab mở.
- Bấm Stop không giết lượt train (`start_new_session=True`, phép kiểm T7). Nhưng khi mất ô theo dõi, Colab ngắt máy sau khoảng 90 phút không tương tác.
- Mất máy: bật lại đúng máy cũ, Run all. Ô 4 tải lại dữ liệu và hoà S1 (khoảng 15 phút [suy]). Ô 6 chép điểm lưu mới nhất từ Drive về, chạy tiếp và kiểm `[nạp default] … → x>0`. Nếu x = 0 thì ô 6 tự dừng (lỗi 30/9).
- Nhân Python restart mà máy còn: ô 6 thấy tiến trình cũ (pgrep) thì chỉ theo dõi tiếp, không chạy bản thứ hai.
- Mỗi lần mất máy, phần mất tối đa là 25 bước (khoảng điểm lưu) cộng tối đa 5 phút đồng bộ.
- Đồng bộ chỉ chép điểm lưu đã yên 60 giây, sang `.tam_checkpoint-N` rồi đổi tên. Drive giữ 3 điểm lưu cuối, không chép lại điểm lưu cũ đã tỉa.
- Xong: `final/` lên Drive, ô 7 zip `<thư mục>_ket_qua.zip` (giữ optimizer của điểm lưu cuối). Tải về và đặt vào `runs/luoi/<đợt>/`.

## Dữ liệu (tải bằng khoá Kaggle của `TK`)

| dataset | dùng cho |
|---|---|
| `<TK>/fgrb-p1-bundle` (2,7 GB) | adapter S1/101 (md5 `0c60a441…`), ảnh, OCR, `p1_val_rows.jsonl` |
| `<TK>/grpo-luoi-script` | `grpo_luoi.py`, `grpo_spice.py`, `build_branch_data.py`, `prompt_keys_ck500.json`, hai jar CoreNLP |
| `<TK>/luoi-kit` | `grpo_codien.py`, `grpo_ppo.py`, `sft_tiep.py`, `grpo_moi_b1.py`, `grpo_moi_b2.py`, `thuong_moi.py`, `metric_exec.py`, `descriptors_ten.jsonl` |

Mô hình gốc Qwen2.5-VL-3B tải từ HuggingFace lúc hoà S1. Khoá Kaggle lấy từ Colab Secrets `KAGGLE_TOKEN` hoặc gõ vào ô ẩn, chỉ ghi vào `/root/.kaggle`.

## Kiểm (không có Colab nên chỉ kiểm phần logic)

Kernel `trangphuongngoc/colab-luoi-kiem-k`, Kaggle CPU, chạy `kiem/kiem_logic.py` với tiến trình train giả `kiem/fake_train.py`. Kết quả ở mục dưới.
Phần chưa kiểm được: mount Drive, apt/pip trên Colab, tải dataset bằng khoá, hoà S1 và train thật trên L4/A100. Lần chạy đầu nên là `tham_do`.

### Kết quả kiểm (6/11/2026 tối, bản 3 của kernel, ĐẠT 11/11; log ở `runs/luoi/smoke_6_11/colab_kiem_v3/`)
- T1 dựng lệnh: 11 lượt (grpo/scst/bleu4/rft/dapo/ppo/a2c/gspo/dpo_on/spice_cong/sft) ra đúng script, cờ và tên thư mục; 6 lượt sai bị chặn.
- T3 lượt đầu: tiến trình ở nhóm riêng; đồng bộ Drive trong lúc chạy; dừng nhẹ ở trần giờ; Drive giữ 3 điểm lưu, không còn thư mục tạm.
- T4 mất máy: xoá /content, khôi phục checkpoint-15 từ Drive, chạy tiếp 15 → 40, `[nạp default]` đạt; không chép lại điểm lưu cũ đã tỉa (bản 1 có lỗi này, đã sửa).
- T5 `[nạp default]` ra 0 thì ô theo dõi dừng lượt trong 2 s.
- T6 điểm lưu thiếu tệp, hoặc chưa yên 60 s, không được chép và không được dùng để chạy tiếp.
- T7 gửi SIGINT vào nhóm tiến trình của notebook (như bấm Stop): lượt `start_new_session` còn sống, còn tiến trình đối chứng cùng nhóm thì chết.
- T8 đọc s/bước và đỉnh VRAM từ dòng `[xong]` của `--probe`; luật chọn máy đúng ở 6 trường hợp.
- T9 zip giữ optimizer của điểm lưu cuối. T10 notebook: 7 ô mã đúng cú pháp, có đủ các phần bắt buộc, không gọi `clear_output(`.
- T11 phát hiện tiến trình train cũ còn sống. T12 PPO: đối chứng bắt được 36 lần điểm lưu đủ ba tệp mà chưa có `value_head.pt`; bản đồng bộ chỉ đưa lên Drive điểm lưu có đủ `value_head.pt`, và chạy tiếp được.

### Bản 4 (6/11 tối, thêm B2): ĐẠT 12/12, log ở `runs/luoi/smoke_6_11/colab_kiem_v4/`
- T1 nay có 17 lượt: thêm seqgan, bcmr, es (σ), rlce (λ), mixer, quark, đều ra `grpo_moi_b2.py`. 9 lượt sai bị chặn, gồm `rloo:bcmr`, cờ ES đặt cho seqgan, cờ rlce đặt cho es.
- T13: với es, seqgan và quark, điểm lưu thiếu tệp riêng thì không được chép lên Drive; điểm lưu đủ thì khôi phục được đúng bộ tệp. ES không có optimizer vẫn chạy tiếp được.
- T3–T12 vẫn đạt như bản 3.
