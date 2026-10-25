# Colab: ck500 hạt giống 202 và nhánh kiểm "xáo thưởng" (viết 23/10/2026)

Hai lượt GRPO thưởng SPICE, cùng thiết kế với ck500 (`report/254`, `report/259`), chỉ đổi một biến mỗi lượt:

| lượt | tên | đổi gì so với ck500 | trả lời câu hỏi |
|---|---|---|---|
| A | `s202` | `--seed 202` (đổi tập 1.000 câu nhắc và hạt lấy mẫu) | mức tăng của ck500 có lặp lại ở hạt giống khác không |
| B | `xao101` | `--reward shuffle` (xáo thưởng trong từng nhóm 8 câu, giữ hạt 101 và đúng 1.000 câu nhắc của ck500) | mức tăng đến từ tín hiệu thưởng SPICE hay chỉ từ việc chạy thêm 500 bước GRPO có KL |

Cả hai khởi đầu từ S1/101 (adapter có sẵn trong gói), 500 bước, G=8, lr 1e-5, β=0,04, thưởng tính SPICE rồi trừ phạt độ dài như cũ.
Ở lượt B, thưởng vẫn được tính bằng SPICE nên phân phối thưởng y hệt, chỉ mất quan hệ giữa thưởng và câu sinh ra, nên lợi thế (advantage) trong nhóm là nhiễu.

**Phạm vi khai trung thực.** Lượt A chỉ đổi hạt GRPO, không đổi S1 (vẫn S1/101). Nó đo nhiễu của bước RL, chưa đo nhiễu của bước SFT. Lượt B là một hạt giống, chưa chạy lặp.
ck500 gốc từng bị sự cố nối lượt (OOM, nạp adapter sai ở commit 2) và chạy ở cỡ lô 4×4 rồi 2×8, còn hai lượt này chạy liền một mạch. Phải khai điều này khi báo.

## Mã, gói, md5

Gói `_bundles/colab-ck500-s202/` có hai tệp:
- `grpo_spice.py` md5 **`8489108147c8d1ed80c3dc67c8ad3d3f`** (bản cũ `07ea87b6…` cộng hai cờ `--seed` và `--reward`, mặc định giữ nguyên hành vi; đã chạy thử xáo thưởng trên máy nhà: cùng tập giá trị trong từng nhóm, khác thứ tự).
- `build_branch_data.py` md5 `619e63e123a6dbf60086e65ee94a3912` (không đổi).

⚠️ Chưa chạy `--train` với bản mã mới trên GPU. Ô 4 của notebook (thăm dò 20 bước) chính là phép kiểm đó. Dòng `[cấu hình] seed … · thưởng …` phải hiện đúng.

## Việc làm ở máy nhà trước khi mở Colab

1. Chép lên Google Drive, thư mục `MyDrive/thesis/ck500_s202/`:
   - `_bundles/fgrb_p1_bundle.zip` (2,7 GB, giữ nguyên tên tệp; chứa `adapter_s1_seed101`, ảnh, OCR, `p1_train_rows.jsonl`, `p1_val_rows.jsonl`);
   - hai tệp `grpo_spice.py`, `build_branch_data.py` trong `_bundles/colab-ck500-s202/`;
   - thư mục `_bundles/colab-ck500-s202/stanford_jars/` (2 jar, 385 MB). Colab không tải được jar Stanford của SPICE (No route to host, đo 23/10), nên ô 3 chép chúng từ Drive vào thư viện.
2. Kiểm hạn mức Colab trước khi bấm chạy. Số đơn vị và giá GPU phải tra tại phiên, đừng dùng số nhớ.

## Chọn máy (theo thủ tục chọn máy của CLAUDE.md)

Khâu nghẽn là sinh mẫu và SPICE (Java trên CPU), không chỉ GPU. Trên Kaggle T4 đo được 146 đến 160 s/bước, đỉnh VRAM 12,4 đến 13,2 GiB.
1. Mở runtime **L4** (hoặc T4 nếu đang có), chạy ô 0 đến 4, đọc `s/bước` và `đỉnh VRAM`.
2. Nếu có thể đo cả A100, đo thêm 20 bước ở đó. Chọn L4 nếu `giờ_L4 / giờ_A100 ≤ 1,5`, ngược lại A100. Đơn vị mỗi lượt = giá/giờ × giờ mỗi lượt.
3. Ghi lại quyết định vào `report/` sau khi có số.

Kỳ vọng thô [suy, chưa đo trên Colab]: 500 bước × 150 s ≈ 21 h trên T4. L4 và A100 chưa có số cho bài này.

## Bốn luật Colab áp nguyên

`start_new_session=True` ở mọi `Popen` · không bấm Stop khi train đang chạy · ô theo dõi đọc log LOCAL · ô theo dõi chạy foreground suốt lượt (không có thì Colab ngắt máy sau khoảng 90 phút không tương tác).
Đồng hồ máy WSL là UTC, mốc giờ đọc bằng `TZ='Asia/Ho_Chi_Minh' date`.

## Cách chạy: nhập notebook

Mã nằm trong **`harness/runbook/colab_ck500_s202_va_kiem_thuong.ipynb`** (bản chạy duy nhất, file này chỉ mô tả).
Colab → *File → Upload notebook* → chọn tệp. Chọn runtime GPU (L4, T4 hoặc A100) trước khi chạy.

| ô | việc | thời gian | kiểm (thiếu một là dừng) |
|---|---|---|---|
| 0 | đặt `RUN` (`"s202"` hoặc `"xao101"`) và đường dẫn Drive | tức thì | |
| 1 | kiểm GPU, cài gói, Java 8 | 5 phút | trl đúng `0.29.1`; torch có CUDA; in dtype sẽ dùng |
| 2 | gắn Drive, bung gói 2,7 GB, kiểm md5, kéo điểm lưu cũ nếu có | 10 đến 20 phút | md5 hai tệp mã khớp; gói đủ thư mục |
| 3 | chép 2 jar SPICE từ Drive, selftest (có SPICE, không GPU) và hoà S1 | 10 phút | `✅ selftest ĐẠT`; có bản hoà |
| 4 | thăm dò 20 bước, đo s/bước và VRAM | 10 đến 20 phút | có dòng `[cấu hình] …` đúng lượt; đủ 20 bước; không OOM |
| 5 | train nền và đồng bộ điểm lưu sang Drive | trả về ngay | in PID và lệnh |
| 6 | theo dõi foreground | suốt lượt | xem bên dưới |
| 7 | kiểm checkpoint-500 và đóng gói adapter ra Drive | 5 phút | adapter đủ, in md5 |

**Thứ tự:** 0, 1, 2, 3, 4, rồi 5 và 6 liền nhau. **Mất máy:** chạy lại 0, 1, 2, 3, rồi 5 và 6 (bỏ 4).
Mỗi lượt (`s202`, `xao101`) dùng một runtime mới.

### Ô 4: quyết máy ở đây
Ô in `~X s/bước ⇒ 500 bước ≈ Y h` và dòng `[xong]` có đỉnh VRAM. Với L4 chỉ chọn khi VRAM ≤ ~17 GiB. Nếu đo được cả A100, chọn L4 khi `giờ_L4 / giờ_A100 ≤ 1,5`. Không đổi card giữa chừng.

### Ô 6: đọc gì trong 15 phút đầu
- Dòng `[cấu hình]` đúng lượt.
- `s/bước` gần số ở ô 4; `kl` bắt đầu gần 0 rồi tăng (cỡ 0,01 sau vài chục bước).
- Lượt `xao101`: `thưởng TB` đứng phẳng quanh mức đầu (không tăng). Đó là dấu hiệu xáo thưởng chạy đúng. Lượt `s202`: thưởng tăng chậm như ck500 (0,44 lên 0,52).
- Không `nan`, không `Traceback`.

### Chạy tiếp sau mất máy
Sau dòng `[tiếp từ] …/checkpoint-N` bắt buộc có `[nạp default] … |lora_B| 0.0000 → x` với x > 0, và `kl` bước đầu xấp xỉ mức cuối lượt trước (không về ~0). Thiếu một trong hai thì dừng ngay (bài học 30/9). Điểm lưu trên Drive được giữ: chỉ hai điểm mới nhất (sửa 24/10, trước đó còn giữ thêm các bội số của 250).

### Nếu OOM
Đổi `--bs 4 --accum 4` thành `--bs 2 --accum 8` ở ô 4 và ô 5 (cùng một bước cập nhật về toán), và khai.

### Hai chỗ khác ck500 gốc, phải khai khi báo
1. **dtype:** ck500 gốc train ở float16 trên Kaggle T4. L4 và A100 tự chọn bfloat16 (mã chọn theo compute capability). Muốn y hệt thì chạy Colab T4 (chậm hơn). Ô 1 in dtype sẽ dùng.
2. **Cỡ lô:** ck500 gốc chạy 4×4 rồi 2×8 ở đoạn nối; hai lượt này 4×4 liền mạch, sinh theo khúc 8 chuỗi (đã kiểm trùng tuyệt đối với sinh một lần ở lượt 1/10).

## Sau Colab: chấm test trên Kaggle (0 đồng)

Dùng nguyên `harness/runbook/kaggle_grpo_spice_test_ck500.md` (sinh 4.463 bước rồi chấm UGround), chỉ đổi:
- dataset điểm lưu: tạo `grpo-spice-ck500-{RUN}` từ gói vừa tải (thay `grpo-spice-ck500`);
- tên tệp ra: `pred_ck500_{RUN}.jsonl`, `score_ck500_{RUN}_raw.jsonl` (đừng ghi đè tệp ck500 gốc);
- thư mục đích sau khi tải về: `runs/grpo_spice/` (đặt cùng chỗ với phép đo ck500).
Ước chừng 9,4 h T4 mỗi lượt (sinh ~3,7 h cộng chấm ~5,4 h). Hai lượt cần hai lần commit, hạn mức tuần 30 h.

Sau đó (0 GPU) đọc bằng `harness/grpo_spice_doc.py`, mở rộng thêm hai nhánh. Các phép so ghép cặp theo bootstrap cụm app như mọi chỗ khác:

| phép so | đọc để biết gì |
|---|---|
| ck500_s202 − S1/101 | mức tăng lặp lại ở hạt thứ hai không (ck500 gốc: +1,55 [+0,80; +2,33]) |
| ck500_s202 − ck500 | hai hạt GRPO khác nhau bao nhiêu |
| xao101 − S1/101 | việc chạy thêm 500 bước GRPO không tín hiệu tự nó cho bao nhiêu |
| ck500 − xao101 | phần thuộc tín hiệu SPICE |

## Cách đọc (viết trước khi có số, không nới sau)

- Lượt A: nếu ck500_s202 − S1/101 cùng dấu dương và KTC không chứa giá trị âm lớn, báo "mức tăng lặp lại ở hai hạt RL", kèm trung bình hai hạt và nhiễu giữa hai hạt. Nếu về gần 0, báo thẳng là ck500 một hạt có thể do may mắn, và hạ mọi câu về ck500 trong luận văn.
- Lượt B: nếu ck500 − xao101 dương và KTC loại 0, báo "tín hiệu SPICE đóng góp phần tăng". Nếu xao101 − S1 đã gần +1,5, báo "phần lớn mức tăng của ck500 đến từ việc chạy thêm bước GRPO có KL, không phải tín hiệu SPICE" và đổi cách viết đóng góp.
- Một hạt giống mỗi lượt, MDE 2,11. Chênh lệch dưới MDE vẫn là ô trắng. Không viết "kết luận chắc chắn".
- Thước chính vẫn là exec dưới UGround, báo kèm D.3 và thước chữ như ck500.
- Số val không trích.

## Nếu có trục trặc

| dấu hiệu | xử lý |
|---|---|
| ô 2 báo `grpo_spice.py là bản cũ` | chép lại tệp từ `_bundles/colab-ck500-s202/` lên Drive |
| ô 4 không có dòng `[cấu hình]` | mã là bản cũ, dừng |
| ô 4 OOM | `--bs 2 --accum 8` (giữ `--gen-chunk 8`) |
| `pip` làm torch thành bản CPU | cài lại torch bản CUDA, Restart, chạy lại ô 1 |
| `kl` về ~0 sau khi chạy tiếp | điểm lưu nạp sai; xem mục "Sự cố 30/9" trong `kaggle_grpo_spice_commit.md` |
| ô 6 văng `FileNotFoundError` trên Drive | Drive rớt gắn; chạy lại `drive.mount`, đừng chạy lại lệnh train |
