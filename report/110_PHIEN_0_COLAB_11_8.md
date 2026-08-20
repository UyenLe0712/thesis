# 110 — PHIÊN 0 TRÊN COLAB (10-11/8/2026): SỐ ĐO, LỖI BẮT ĐƯỢC, TRẠNG THÁI

> Ghi lại kết quả chạy `harness/run_on_colab.md` phiên 0 (dựng dữ liệu dạy + OCR + nhãn
> khai báo + bốn nhánh + tập kiểm). Mọi con số dưới đây **đo trên máy thật**, không phải
> ước. Khi mâu thuẫn với `report/108`: file này thắng về *phiên 0 đo được gì*.

## 1. Máy và tiền — bảng đo thật, thay mọi con số nhớ

| runtime Colab | lõi | đơn vị/giờ | OCR 64.567 ảnh | tiền |
|---|---|---|---|---|
| CPU | 2 | **0** | 45,3 giờ *(đo: 0,39 ảnh/giây)* | $0 |
| **L4** | 12 | **1,54** | **7,7 giờ** *(2,13-2,22 ảnh/giây)* | **~$1,2** |
| A100-SXM4-**40GB** | 12 | **5,3** | 8,1 giờ | ~$4,3 |

**L4 rẻ hơn A100 3,6 lần với cùng 12 lõi** — vì khâu này bám CPU, card nằm không. Phát hiện
này chưa áp cho khâu train: train dùng card thật, phải đo lại bằng **ô A.3** (thử 20 bước)
trên cả L4 lẫn A100 rồi mới chọn. Chênh ở đó tính bằng vài chục đô vì có 12 lượt train.

**Quy luật rút ra:** tốc độ OCR ≈ **0,37-0,39 ảnh/giây mỗi lõi VẬT LÝ**. `os.cpu_count()`
đếm luồng, chia đôi mới ra lõi vật lý. Suy từ tốc độ một luồng nhân số luồng thì hụt 2 lần.

⛔ Số cũ đã rút: "A100 80 GB", "6,77 đơn vị/giờ", "67 GB ảnh dạy", "OCR 2,8 giờ".
Thật: **A100 40 GB · 5,3 đơn vị/giờ · ảnh dạy ~31 GB (493 KB/ảnh) · OCR 7,7-8,1 giờ**.

## 2. Dữ liệu đã dựng (dựng lại 3 lần trên 3 máy, ra y hệt)

| | số | ghi chú |
|---|---|---|
| bước tập dạy | **64.567** | từ 76 shard |
| bước chạm | **41.191 = 63,8%** | lát 2 shard cho 63,3% |
| tác vụ | **12.895** | |
| ảnh thiếu | **0** | |
| bước tập kiểm | **6.958** | khớp bản đã khoá |
| gán được app (tập kiểm) | **3.130 = 45,0% · 269 app** | khớp 44,9% ghi trong hồ sơ |
| không gán được → cụm riêng | 3.828 | nhóm cụm-đơn chi phối G hiệu dụng |

Tải 31 GB ảnh mất **32 phút** khi có `HF_TOKEN`; không token thì chậm hơn và **treo cứng
giữa chừng** (đứng 409/800 MB, không báo lỗi).

## 3. OCR — ba tầng kiểm, và tầng nào KHÔNG có

**Tầng 1, độ phủ:** gộp 12 mảnh → **64.567 bản ghi · phủ 100,00% · thiếu 0**.
Bỏ đúng 957 dòng trùng (sinh ra do đổi từ 2 tiến trình sang 12 giữa chừng).

**Tầng 2, kiểm chéo máy** (ô 0.9b, thêm 11/8):

| | ảnh | chữ/màn | trung vị | màn rỗng |
|---|---|---|---|---|
| tập KIỂM (máy khác, 6/8) | 6.969 | 24,2 | 22 | 0,1% |
| tập DẠY (Colab L4, 11/8) | 64.567 | **23,6** | **22** | **0,1%** |

Lệch 2,5%, trung vị và tỉ lệ màn rỗng trùng khít. ⇒ **bộ đọc chữ hành xử như nhau trên hai
máy cách nhau 5 ngày** — đây là căn cứ cho câu "đổi máy không đổi độ chính xác", trước đó
chỉ là suy luận.

**Tầng KHÔNG có, cấm nói là có:** chưa bao giờ đo bộ đọc chữ đúng/sai so với chữ thật trên
màn (AndroidControl không có nhãn chữ chuẩn). Giới hạn đã biết và phải khai: **đọc nhầm
biểu tượng thành ký tự** (`build_train_data.py:152`), và **nuốt dấu cách** ở một số nhãn
nút (quan sát 11/8: `Turnon`, `ONLYATADIDAS`, `NEW&TRENDING`). Nuốt dấu cách đẩy phần tử
xuống nhóm "không tên" chứ không gán bậy — kiểu hỏng *bỏ sót*, nhẹ hơn *gán sai*, và **đo
được là không gây hại**: "không tên" ra 22,0%, còn thấp hơn mốc tham chiếu 23%.

## 4. Nhãn khai báo ở quy mô đủ — năm số tham chiếu đều khớp

| | tham chiếu (1.697 bước + tập kiểm 4.448) | **đo 11/8 (41.191 bước)** |
|---|---|---|
| tên rõ | ~74% | **73,6%** (cây trợ năng 8.581 · OCR 23.480) |
| chỉ ký hiệu lẻ | — | 4,4% |
| không tên | ~23% | **22,0%** |
| vai trò rõ | ~76% | **75,8%** |
| có phần tử trùng tên | ~7% | **7,6%** |
| có hàng xóm cùng vai trò | ~92% | **91,6%** |
| hộp to hơn 1/4 màn | — | 2,2% (912) |

Phủ nhãn: 41.099/41.191 = **99,8%** (92 bước rơi vì màn không có cây trợ năng hoặc điểm
chạm nằm ngoài mọi hộp). ⇒ **khâu dựng nhãn không hỏng khi lên quy mô gấp 24 lần.**

## 4b. Nhãn `app_seen_in_train` — CHÊNH VỚI HỒ SƠ CŨ, phải đối chiếu

Đo 11/8 (`tag_app_seen.py`, tập dạy đủ 12.895 tác vụ):

| | bước |
|---|---|
| ĐÃ thấy lúc dạy | 2.526 = **80,7%** của phần gán được |
| CHƯA thấy lúc dạy | **604** |
| không gán được app | 3.828 |

⚠️ **Chênh với con số ghi trong `CLAUDE.md`**: hồ sơ 6/8 ghi *"chỉ 21 app unseen = 67 bước
chạm"*, nay ra **604 bước** ⛔ *(số này ĐÃ RÚT — tính bằng bản mã có lỗi; số đúng sau khi vá:
**139 bước / 22 app**, xem mục 4j-11)* (ước ~385 bước chạm theo tỉ lệ 63,8%). Lệch gần 6 lần. Chưa
truy ra nguyên nhân — nghi do lần trước đối chiếu với lát 2 shard chứ không phải tập dạy
đủ, nhưng lát nhỏ hơn thì lẽ ra phải cho NHIỀU app unseen hơn, tức chiều lệch ngược với
suy đoán đó. **Phải truy ra trước khi báo lát cắt phụ.** Chiều lệch có lợi (lát app-unseen
được cấp nhiều mẫu hơn), nhưng "có lợi" không phải lý do bỏ qua.

Cảnh báo do chính script in ra, giữ nguyên khi viết luận văn: **nhóm 3.828 "không gán được
app" là KHÔNG BIẾT, không được đọc thành "chưa thấy"**.

## 4c. MỐC DỪNG 3 — bảng đối chiếu đầy đủ (11/8/2026)

| ô | kiểm gì | ngưỡng | đo được | |
|---|---|---|---|---|
| 0.9 | phủ OCR | 100% | **100,00%** · thiếu 0 | ✅ |
| 0.9b | OCR có giống máy khác không | lệch <15% | **2,5%** (23,6 vs 24,2 chữ/màn) | ✅ |
| 0.10 | nhãn khai báo | 5 số tham chiếu | lệch <1 điểm ở cả 5 | ✅ |
| 0.11 | 9 bất biến bốn nhánh | đạt 9/9 | **9/9** · 64.567 mẫu/nhánh · 41.099 khai báo | ✅ |
| 0.11b | **rò rỉ dạy ↔ kiểm** | **= 0** | **0** (12.895 vs 1.432 tác vụ) | ✅ |
| 0.11c | phép ghép ảnh ↔ câu chuẩn | chênh >1,4× | **2,4×** (48% vs 20%, n=400) | ✅ |
| 0.11d | tập kiểm dựng lại | 6.958 / 4.463 / ~99,7% | **6.958 / 4.463 / 99,7%** | ✅ |
| 0.11e | phân bố app | — | 55,0% không biết · 36,3% đã thấy · 8,7% chưa thấy | — |

**0.11b lần đầu chạy ở quy mô đủ.** Trước nay "0 tác vụ trùng" mới chỉ kiểm trên lát 2
shard. Rò rỉ là loại sai không chữa được sau khi train, nên đây là chốt chặn thật.

**9 bất biến đạt hết nghĩa là bốn nhánh so được với nhau:** câu đích của s2/s2r/s2_nopoint
trùng khít s1 ở cả 64.567 mẫu ⇒ chênh lệch điểm về sau chỉ có thể đến từ phần khai báo,
không thể đến từ câu.

**0.11c đã được siết, và siết ra kết quả TỐT HƠN.** `--check` vốn gọi cứng
`check(n_shards=1)` và bỏ qua `--shards`, nên mặc định chỉ 60 mẫu của một shard (±12,6
điểm) — mỏng hơn hẳn mọi phép kiểm khác của phiên 0. Đã mở `--shards` và `--n-check`
(sửa 11/8). Chạy lại với 400 mẫu / 3 shard, tốn 0,2 đơn vị:

| n | ghép ĐÚNG | ghép LỆCH (đối chứng) | chênh |
|---|---|---|---|
| 60 | 47% (28/60) | 27% (12/44) | 1,74× |
| **400** | **48% (193/400)** | **20% (61/311)** | **2,4×** |

Mẫu nhỏ đang *làm nhẹ* khoảng cách chứ không thổi phồng. Ở n=400 hai khoảng tin cậy
(48±4,9 và 20±4,4) tách bạch, không chạm nhau.

## 4d. ĐỘ DÀI CHUỖI — đo trước khi train, và đã phải nâng trần

Đo trên đủ 64.567 mẫu, **không cần ảnh**: lấy kích thước từ `train.jsonl`, tính token thị
giác bằng `smart_resize` của Qwen2.5-VL, cộng token văn bản của cả ba lượt (system + user +
assistant). Chạy trên runtime CPU miễn phí.

| nhánh | trung vị | p90 | p99 | tối đa | đích sinh (trung vị / tối đa) |
|---|---|---|---|---|---|
| s1 | 1.498 | 1.564 | 1.651 | **1.984** | 7 / 86 |
| s2 | 1.524 | 1.593 | 1.675 | **2.017** | 41 / 101 |

Token ảnh: **1.272** (ảnh 1080×2400 co theo `image_max_pixels 1003520`).

**0% mẫu vượt 2048 — nhưng dư đúng 31 token**, mỏng hơn cả sai số của phép đếm (phần khung
hội thoại là số ước, không đo). ⇒ **nâng `cutoff_len` 2048 → 2560 ngày 11/8, trước lượt
train đầu tiên** (thời điểm duy nhất được phép đổi).

Nâng trần **không tốn thêm gì**: LLaMA-Factory đệm theo mẫu dài nhất trong từng lô, không
đệm tới `cutoff_len`. Dữ liệu không dài ra thì bộ nhớ và thời gian không đổi.

⚠️ Vì sao đáng bỏ công đo: cắt cụt ở đây **không có tiếng động**. LLaMA-Factory cắt từ ĐUÔI,
mà đuôi là đích sinh — mất `<desc>` hoặc mất luôn câu, trong khi mẫu vẫn vào huấn luyện và
loss vẫn tính. Tệ hơn nữa, đích của s2 dài hơn s1 nên **s2 bị cắt nhiều hơn**, tức phép so
S2−S1 thiên vị đúng chiều làm s2 trông kém đi — hỏng đúng con số headline.

**Lỗi trong chính phép đo này (ghi lại vì suýt đọc nhầm):** ô đếm bản đầu lấy `messages[0]`
làm lượt user, trong khi `messages[0]` là **system** — bỏ sót trọn câu nhắc. Nó cho trung vị
1.337 thay vì 1.498. Lộ ra vì trừ đi token ảnh chỉ còn ~40 token cho cả câu nhắc lẫn đích,
trong khi riêng dòng OCR đã 25 cụm chữ. Bản sửa in ra `['system','user','assistant']` để
không lấy nhầm lượt lần nữa.

## 4e. KIỂM SẴN SÀNG TRƯỚC KHI TRAIN (11/8, chạy trên runtime CPU miễn phí)

| kiểm gì | cách | kết quả |
|---|---|---|
| độ dài chuỗi | đếm token đủ 64.567 mẫu | 0% vượt; nhưng dư chỉ 31 token ⇒ nâng `cutoff_len` 2048→2560 |
| đường dẫn ảnh nướng cứng | so tên ảnh trong 4 tệp nhánh với `train.jsonl` | 4/4 nhánh: tiền tố đúng **một** giá trị, **0** tên ảnh lạ |
| cấu hình có được LLaMA-Factory nhận | chạy thật `llamafactory-cli train` trên CPU | **không khoá nào bị từ chối**; nạp đúng `gui_s1` 64.567 mẫu; qua được khâu mã hoá token |
| cờ dòng lệnh khớp runbook | so `add_argument` với chỗ runbook gọi | khớp hết (`--selftest-batch`, `--ceiling`, `--b-infer`, `--no-adapter`, `--mode`) |

⚠️ **Đường dẫn ảnh bị nướng cứng** `/content/ws/thesis/harness/dg1_cache/train_ac/` vào bốn
tệp nhánh. Phiên sau đặt `WS` khác là mọi ảnh trỏ trượt. Giữ nguyên `WS`, hoặc dựng lại bốn
nhánh với `--img-prefix` mới.

⏳ **Mỗi lượt train mất 20-30 phút TRƯỚC bước 1** để chuyển định dạng và mã hoá token
(đo: 7,3 mẫu/giây trên 2 lõi ⇒ ~25 phút trên 12 lõi). Không phải treo. Không dùng
`tokenized_path` để né — bộ đệm cũ lệch cấu hình sẽ chạy trơn và ra số của cấu hình cũ.

**Bốn lỗi runbook sửa cùng ngày, đều sẽ nổ ở đầu phiên train:** ô A.1 thiếu `makedirs` cho
thư mục `images` (4 gói đóng bằng tên tệp trần ⇒ `tar -C` chết "Cannot chdir") · A.1 vẫn tìm
`train_images.tar` một tệp thay vì 4 gói · câu "card không phải A100 thì DỪNG PHIÊN" mâu
thuẫn với phát hiện L4 · mốc dừng 4 vẫn nhân 6,77 đơn vị/giờ.

## 4f. HAI KHÂU SAU TRAIN CŨNG MẤT TRẮNG KHI ĐỨT MÁY — đã vá 11/8

Soi lại trước khi train, thấy đúng lỗi đã làm mất 42 đơn vị hôm 10/8, lặp ở hai chỗ nữa:

| tệp | hỏng thế nào | vá |
|---|---|---|
| `infer_branch.py` | mở tệp dự đoán ở chế độ `"w"`, **không `flush`**, không nối tiếp. Đứt máy giữa lượt sinh câu 1,5 giờ là mất trắng. Chiến dịch có **cả chục lượt** (4 nhánh × 2 hạt giống + trần gold/filler + B-infer + mô hình gốc) | đọc tệp cũ → bỏ dòng ghi dở → mở `"a"` → chỉ sinh phần thiếu → `flush()` mỗi lô |
| `score_run.py` | gom `raw` trong bộ nhớ, chỉ ghi khi xong. Bộ trỏ chạy **~5 giờ mỗi nhánh** trên 4.463 ảnh | ghi từng bước + `flush` → nối tiếp bằng tệp thô → **gộp số cuối từ TỆP, không từ bộ nhớ**, nên lượt chạy bị cắt mấy khúc vẫn ra đúng con số toàn tập |

Vá cho `score_run.py` có một chi tiết dễ bỏ sót: các bản ghi "bỏ qua" (câu rỗng, bộ trỏ
không trả toạ độ) trước đây **không lưu trường `app`** — gộp lại từ tệp thô thì mấy bước đó
sẽ rơi sang cụm `ep<id>` thay vì cụm ứng dụng, làm lệch khoảng tin cậy. Đã thêm `app` và
`app_seen_in_train` vào cả hai nhánh bỏ qua.

## 4g. Ô theo dõi: nhật ký cuộn, KHÔNG xoá màn hình

Toàn bộ ô theo dõi (C.3b · C.6 · 0.12b · A.5) đã bỏ `clear_output`, đổi sang in thêm một
dòng mỗi lần, có **mốc giờ · phần trăm · tốc độ · còn bao lâu**. Lý do: `clear_output` chỉ
chừa lại dòng hiện tại nên mất sạch lịch sử — không biết tốc độ đang tụt hay đứng yên từ
lúc nào, và khi máy bị thu hồi thì không còn gì để dựng lại mốc thời gian. Trong script
Python phải thêm `flush=True`, không thì nhật ký kẹt trong bộ đệm khi chạy nền bằng `nohup`.

## 4h. MỐC DỪNG 4 — thăm dò train 20 bước trên L4 (11/8 chiều)

Ô A.3, nhánh `s1` hạt giống 101, `max_samples 2000`, 20 bước. Ba phép kiểm cơ học **đạt hết**:

| kiểm | ngưỡng | đo được |
|---|---|---|
| tham số huấn luyện | 14.966.784 | **14.966.784** ✅ |
| cỡ lô hiệu dụng | 16 | **16** ✅ |
| tràn bộ nhớ | không | **không** (L4 **24 GB**, `per_device 4`, `image_max_pixels 1003520`) ✅ |
| loss có tụt không | — | 2,036 → 0,969 → 0,864 → 0,955 (20 bước) |

**Tốc độ: 31,26 s/bước** (ba giá trị cuối 30,89 · 30,89 · 31,26 ⇒ đã vào trạng thái đều,
không còn là bước khởi động). `train_samples_per_second 0,512`.

| | L4, cấu hình gốc |
|---|---|
| 1 lượt = 8.071 bước | **69,5 giờ** |
| đơn vị 1 lượt | 107 ≈ $10,7 |
| **8 lượt** (4 nhánh × 2 hạt giống) | **556 giờ · 856 đơn vị · ~$86** |

⚠️ **Nút thắt KHÔNG phải tiền mà là thời gian tường.** 556 giờ = 23 ngày máy chạy liên tục,
trong khi hạn nộp còn ~7 tuần và còn phải chấm điểm, tính MDE, viết luận văn. Bốn lượt cốt
lõi (s1 + s2 × 2 hạt giống) vẫn là 278 giờ ≈ 11,6 ngày. Một lượt 69,5 giờ = **6-7 phiên
Colab nối tiếp**, mỗi mối nối một lần rủi ro.

**Vì sao chậm — bóc từ chính log:** `total_flos 9.527.912 GF` cho 20 bước ⇒ 4,76·10¹⁴ FLOP
mỗi bước ⇒ **15,2 TFLOPS hiệu dụng**, khoảng **12,6%** công suất bf16 của L4. Cấu hình đang
đánh đổi tốc độ ở hai chỗ mà chưa cần đánh đổi: `gradient_checkpointing: true` (tính lại
activation để tiết kiệm VRAM — trong khi VRAM còn dư, không OOM) và `quantization_bit: 4`
(bnb NF4 phải giải nén trọng số mỗi phép nhân, rất tốn trên card băng thông thấp). Chưa bật
`enable_liger_kernel`.

### 4h-2. Đã đo 5 biến thể tăng tốc trên L4 — KHÔNG cái nào dùng được (ô A.3b + A.3d)

| biến thể | s/bước | kết quả |
|---|---|---|
| P0 4-bit + gradient checkpointing (gốc) | **31,26** | đường cơ sở |
| P1 4-bit, **tắt** checkpointing | 31,37 | **không mua được gì** — card nghẽn ở chỗ khác |
| P4 **bf16** (bỏ 4-bit), giữ checkpointing, 4×4 | — | **TRÀN BỘ NHỚ** |
| P5 = P4 + liger | — | **TRÀN BỘ NHỚ** |
| P6 bf16, tắt checkpointing, `per_device 2 × accum 8` | — | **TRÀN BỘ NHỚ** |

**Chẩn đoán:** OOM ở forward đầu tiên, `down_proj` của MLP, **21,54 GB đã cấp trên card
22,03 GB**. dtype đúng `bfloat16` (không phải fp32 như nghi ban đầu), liger nạp thành công
⇒ tên khoá đúng, không phải lỗi cấu hình. Nghĩa là **P0 vốn đã chạy sát trần VRAM**: 4-bit
ép mô hình xuống ~1,9 GB, đổi sang bf16 thêm ~4,3 GB là đủ đẩy qua mép.

⇒ **L4 kịch trần ở ~31 s/bước, không có đường tăng tốc nào trong 22 GB.** Giá phải trả để
biết: ~1,2 đơn vị.

**Bài học về cách đo:** biến thể P2 ban đầu ghép *hai* thay đổi (bỏ 4-bit **và** tắt
checkpointing) nên chết trước khi kịp trả lời câu nào — phải tách biến mới đọc được. Và
tắt checkpointing hoá ra **có** tác dụng (activations phình lên 21,5 GB chứng minh điều
đó), chỉ là không đổi tốc độ — khác hẳn suy đoán "khoá bị ghi đè".

⇒ **Đổi A100 40 GB**: 6,2 GB mô hình + activations nằm gọn, mở được đúng cấu hình mà L4
vừa từ chối. Chênh lệch thực tế giữa hai card do đó **lớn hơn** tỉ lệ giá 3,44×.

### 4h-3. A100-SXM4-40GB — đo được 10,70 s/bước, ĐÃ CHỐT DÙNG A100

Đổi runtime, bung lại 33 GB (~35 phút), chạy đúng ô A.3 với cùng `cfg.yaml`:

| | L4 (22 GB) | **A100-SXM4-40GB** |
|---|---|---|
| P0 gốc (4-bit + ckpt, 4×4) | 31,26 s/bước | **10,70 s/bước** (ổn định 10,49) |
| hiệu suất | 15,2 TFLOPS = 12,6% đỉnh | 44,5 TFLOPS = **14,3%** đỉnh |
| 1 lượt = 8.071 bước | 69,5 giờ · 107 đv | **24,0 giờ · 127 đv** |
| **2 lượt S1** (×2 hạt giống) | 139 giờ = 5,8 ngày · 214 đv ≈ $21 | **48 giờ = 2 ngày · 254 đv ≈ $25** |
| 8 lượt | 556 giờ = 23 ngày · 856 đv ≈ $86 | 192 giờ = 8 ngày · 1.017 đv ≈ $102 |

**A100 nhanh hơn 2,92× trong khi giá gấp 3,44× ⇒ đắt hơn 19% tiền, rẻ hơn 3 lần thời gian.**
Hạn nộp còn ~7 tuần nên ràng buộc thật là thời gian tường, không phải tiền ⇒ **chốt A100**.
Chênh $4 ở hai lượt đầu đổi lấy 4 ngày, và số phiên nối tiếp tụt từ ~12 xuống ~4.

✅ **Bằng chứng đổi card không đổi kết quả** (dùng được trong luận văn): cùng `seed 101`,
loss 20 bước trùng tới ba chữ số — L4 `2,036 / 0,9686 / 0,8635 / 0,9553` · A100 `2,040 /
0,9679 / 0,8635 / 0,9547`; `total_flos` y hệt **9.527.912 GF** ở cả hai máy; tham số huấn
luyện **14.966.784** và cỡ lô **16** khớp. Cùng loại lập luận với phép kiểm chéo máy của bộ
đọc chữ ở ô 0.9b, nhưng lần này cho khâu train.

### 4h-4. Bốn biến thể trên A100 — cấu hình GỐC vẫn thắng (ô A.3d, 11/8 15:47)

| biến thể trên A100-40GB | s/bước | |
|---|---|---|
| **P0 gốc: 4-bit + gradient checkpointing, 4×4** | **10,70** | ⬅ **nhanh nhất** |
| P4 bf16, giữ checkpointing, 4×4 | — | TRÀN BỘ NHỚ |
| P5 = P4 + liger | 14,76 | chạy được nhưng **chậm hơn P0 38%** (33,1 giờ/lượt · 175 đv) |
| P7 bf16, tắt checkpointing, 4×4 | — | TRÀN BỘ NHỚ |
| P8 bf16, tắt checkpointing, `8×2` | — | TRÀN BỘ NHỚ |

⛔ **HAI KẾT LUẬN NGƯỢC TRỰC GIÁC — đã đo trên máy thật, đừng thử lại:**

**1. QLoRA 4-bit NHANH HƠN bf16 ở bài này** (10,70 vs 14,76 s/bước). Dự đoán "bnb NF4 phải
giải nén mỗi phép nhân nên chậm" **sai ở cả hai card**. Mô hình 3B đủ nhỏ để khâu giải nén
không thành nút thắt; đổi lại 4-bit trả về ~4,3 GB cho activations, mà chỗ nghẽn thật nằm
đúng ở activations. ⇒ ✅ **Cấu hình đăng ký trước giữ nguyên, KHÔNG phải ghi mục sửa đổi
`report/106`** — đỡ một chỗ phải giải trình với hội đồng.

**2. Chỗ ngốn bộ nhớ là BẢNG LOGITS, không phải trọng số.** Bằng chứng sạch: P4 tràn, mà
P5 = *chính P4 cộng liger* thì chạy được. Liger gộp bước cross-entropy nên khỏi dựng bảng
`151.936 từ vựng × ~1.500 token × 4 mẫu` nâng lên fp32 (~3,6 GB, cộng bản sao lúc tính đạo
hàm). Đây cũng là lời giải cho việc **L4 chết ở mọi biến thể bf16** — không phải vì 6,2 GB
trọng số như suy đoán ban đầu.

### 4h-6. ⭐ CHỐT CUỐI: P9 (4-bit + checkpointing + liger) — P10 BỊ LOẠI VÌ TRÀN Ở CHUỖI DÀI

Ô A.3g chạy bốn cấu hình trên **200 mẫu dài nhất của s2** (nhánh nặng nhất), cùng `seed 101`,
cùng thứ tự ⇒ loss so được trực tiếp:

| biến thể | s/bước (mẫu dài) | loss 4 mốc |
|---|---|---|
| P0 gốc | 11,66 | 3.189 · 3.014 · 2.597 · 2.545 |
| **P9 = P0 + liger** | **11,33** | 3.188 · 3.015 · 2.595 · 2.545 |
| P10 = P9, tắt ckpt | — | **TRÀN BỘ NHỚ** |
| P11 = tắt ckpt, không liger | — | **TRÀN BỘ NHỚ** |

⛔ **P10 bị loại — và đây là chỗ 12 phút thăm dò cứu một lượt train 20 giờ.** P10 chạy
9,03 s/bước rất ngọt trên mẫu thường, nhưng **tràn bộ nhớ ở chuỗi dài**. Nếu đã bấm A.4 với
nó thì lượt train sẽ chạy trơn vài giờ rồi chết lúc vô tình gặp một lô mẫu dài — giữa đêm,
không ai ngồi trước máy. Bỏ liger cũng không cứu (P11 cũng tràn).

✅ **Liger KHÔNG đổi phép tính — chứng minh bằng số:** loss P0 và P9 trùng tới **chữ số thứ
tư** trên cùng dữ liệu, cùng hạt giống. Lệch cỡ nhiễu dấu phẩy động. ⇒ dùng được mà không
phải sửa hồ sơ đăng ký trước; `quantization_bit: 4` và mọi siêu tham số giữ nguyên.

**⭐ CẤU HÌNH CHẠY CHÍNH THỨC = P9**: `train_config.yaml` giữ nguyên, **thêm đúng một khoá**
`enable_liger_kernel: true`.

| | s/bước | 1 lượt | 2 lượt S1 | 8 lượt |
|---|---|---|---|---|
| P0 gốc | 10,70 | 24,0 giờ · 127 đv | 48 giờ · 254 đv | 192 giờ · 1.017 đv |
| **P9** | **10,38** | **23,3 giờ · 123 đv** | **46,6 giờ · 246 đv ≈ $25** | 186 giờ · 987 đv ≈ $99 |

⚠️ **Bài học phương pháp, quan trọng hơn 3% tốc độ:** thăm dò trên **mẫu đầu tập** không đủ
để kết luận về bộ nhớ. Chuỗi dài nhất 2.017 token so với trung vị 1.524 — mẫu thường không
chạm đỉnh. Mọi cấu hình đụng tới bộ nhớ phải thử lại trên **nhánh nặng nhất với mẫu dài
nhất**. Ô A.3g để lại `s2_long.json` + khoá `gui_s2_long` trong `branches/` (nên thư mục đó
giờ có **7 tệp thay vì 6** — vô hại, `cfg.yaml` trỏ `gui_s1`).

**Tổng thăm dò cả chiến dịch: ~5 đơn vị (~$0,50) cho 16 phép đo trên 2 card.**

### 4h-7. ✅ CƠ CHẾ NỐI TIẾP ĐÃ CHẠY THẬT (ô A.3i, 11/8 16:21)

Thay vì đợi `checkpoint-200` (1 tiếng) mới thử được như kế hoạch cũ, dựng một lượt 10 bước
ghi thẳng lên Drive rồi chạy tiếp lên 20 bước — **8 phút**, và thử được thêm thứ A.5b không
đụng tới: **ghi điểm lưu qua Drive fuse**. Trước ô này mọi lượt thăm dò đều ghi vào
`/content/probe`, mà Drive fuse chính là thứ đã làm chết một lệnh `tar` sáng cùng ngày.

| kiểm | kết quả |
|---|---|
| ghi điểm lưu lên Drive | ✅ **182,7 MB**/bản |
| có `optimizer.pt` | ✅ — nối tiếp khôi phục đúng trạng thái tối ưu hoá, **không** khởi động lại |
| tự dò điểm lưu | ✅ `Resuming training from /content/drive/MyDrive/...` |
| chạy tiếp đúng chỗ | ✅ `global_step = 20`, không quay về 10 |
| `trainer_state.json` giữ lịch sử loss | ✅ 4 mốc — bảo hiểm nếu mất `train.log` |

⇒ Cơ chế cố ý dựng bằng cách **bỏ trống** `resume_from_checkpoint` (lỗi bắt 7/8: điền vào là
tắt đúng cái định bật) và **chưa từng chạy lần nào** — nay đã xác nhận. Một trong ba việc
treo đã xoá.

**Dung lượng điểm lưu:** 182,7 MB × 2 (`save_total_limit`) + bản `_ep1` + bản cuối ở
`output_dir` ≈ **0,73 GB mỗi lượt** ⇒ ~5,8 GB cho tám lượt. Drive 5 TB, không phải lo.

### 4i. Thời gian và cái gì được cứu khi mất máy

| | |
|---|---|
| mã hoá token 64.567 mẫu | ~25 phút (chưa có bước train nào — **không phải treo**) |
| 8.071 bước × 10,38 s | **23,3 giờ** |
| ghi 40 điểm lưu lên Drive | ~25 phút cộng dồn |
| **một lượt** | **~24 giờ · ~126 đơn vị** |
| **hai lượt S1** | **~48 giờ ≈ 2 ngày · ~252 đơn vị ≈ $25** |

⚠️ **24 giờ dài hơn tuổi thọ một phiên Colab** ⇒ gần như chắc chắn phải nối tiếp ít nhất một
lần. Mỗi lần đứt tốn thêm **~1 giờ**: bung lại 33 GB ảnh (35 phút) + mã hoá token lại (25
phút). **Phần train đã làm thì không mất.**

| thứ | ở đâu | mất máy thì |
|---|---|---|
| điểm lưu | `MyDrive/thesis/ckpt/s1_seed101` | còn; mất tối đa **35 phút** train (`save_steps 200`) |
| bản cuối lượt duyệt 1 | `..._ep1`, ô A.5 tự sao trước khi `save_total_limit` xoá | còn |
| `train.log`, `cfg.yaml` | đồng bộ mỗi 5 phút (ô A.4b) | mất ≤5 phút |
| log 16 phép đo thăm dò | `logs/probe_11_8/` (cất 11/8) | còn |
| câu mô hình sinh | ghi thẳng Drive, có nối tiếp | còn |

**Không dùng `tokenized_path`** để né 25 phút mã hoá: bộ đệm cũ lệch cấu hình vẫn chạy trơn
và cho ra số của cấu hình cũ — sai âm thầm, loại hỏng tệ nhất.

### 4h-5. [đã bị 4h-6 thay] Vòng A.3f: P10 từng thắng trên mẫu thường

Tách biến lần cuối (ô A.3f), mỗi biến thể chỉ đổi một thứ so với cái trước:

| | s/bước | 1 lượt | 8 lượt |
|---|---|---|---|
| P0 gốc (4-bit + ckpt, 4×4) | 10,70 | 24,0 giờ · 127 đv | 192 giờ · 1.017 đv |
| P9 = P0 + liger | 10,38 | 23,3 giờ · 123 đv | 186 giờ · 987 đv |
| **P10 = P9, tắt checkpointing** | **9,03** | **20,2 giờ · 107 đv** | **162 giờ · 858 đv** |

**Cấu hình chạy chính thức = P10**: giữ nguyên `quantization_bit: 4` và cỡ lô `4×4`, thêm
`enable_liger_kernel: true` · `disable_gradient_checkpointing: true` ·
`gradient_checkpointing: false`, cộng `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.

Tiết kiệm **30 giờ và ~159 đơn vị (~$16)** so với P0. Ở P10, A100 tốn **bằng** L4 về đơn vị
(858 vs 856) mà nhanh hơn 3,4 lần ⇒ chuyện chọn card đóng lại hoàn toàn.

✅ **Không đổi thiết kế đăng ký trước:** liger là kernel hợp nhất *cùng công thức*; tắt
tính-lại-activation là thuần đổi bộ nhớ lấy tốc độ; `quantization_bit: 4` giữ nguyên. Nếu
giữa lượt bị tràn bộ nhớ thì **bật lại checkpointing rồi chạy tiếp vẫn hợp lệ** — không đổi
phép tính, mất tối đa ~200 bước tới điểm lưu gần nhất.

⚠️ **Rủi ro của việc tắt checkpointing, và cách chặn (ô A.3g):** probe chạy trên 1.000 mẫu
đầu, không bảo đảm gặp mẫu dài nhất (chuỗi dài nhất là **2.017 token của s2**, trung vị chỉ
1.524). Nên trước khi bấm A.4 phải ép P10 nuốt **200 mẫu dài nhất của s2** — nhánh nặng
nhất trong bốn nhánh. Qua được thì cả tám lượt an toàn.

**Tổng chi phí thăm dò: ~4 đơn vị (~$0,40)** cho 12 phép đo trên 2 card. Đổi lại: cấu hình
nhanh hơn 15,6% (đáng ~$16 và 30 giờ), biết L4 kịch trần, và **không phải sửa hồ sơ đăng ký
trước** — kịch bản "buộc phải bỏ 4-bit" đã tự loại bằng số đo.

**Không phải cam kết 8 lượt ngay:** trình tự đã khoá là S1 × 2 hạt giống → chấm → MDE thật
→ khoá ngưỡng → mới train S2.

## 4j. LƯỢT TRAIN ĐẦU TIÊN ĐÃ CHẠY — s1 hạt giống 101 (12/8/2026)

Khởi động 12/8 lúc ~03:14 (giờ máy ảo). Số đo thật ở bước 20:

| | |
|---|---|
| tốc độ | **10,5 s/bước** (thăm dò A.3f cho 10,38 — lệch 1,2%) |
| `total_steps` | 8.072 (làm tròn lên từ 8.071, không phải sai) |
| `remaining_time` LLaMA-Factory tự tính | **23 giờ 34 phút** |
| loss ở bước 20 | 2,13 (probe cho 2,04 ở bước 5) |

**Hai lỗi vấp lúc khởi động, cả hai đã vá vào runbook:**

1. **`liger-kernel` chưa cài trên máy ảo mới** — ô 0.3 chưa có gói, mà `cfg.yaml` đã bật
   `enable_liger_kernel`. `llamafactory-cli` **chết ngay lúc kiểm phụ thuộc**
   (`PackageNotFoundError`), trước cả khi nạp dữ liệu. Cài rời rồi chạy lại A.4, không cần
   restart. ⇒ đã thêm `liger-kernel` vào ô 0.3 kèm dòng in phiên bản.
   **Ô kiểm 90 giây bắt được lỗi này ngay lần đầu dùng** — không có nó thì phải đợi dòng đầu
   của A.5, muộn hơn 4 phút và dễ đọc nhầm thành "đang mã hoá token".
2. **Lượt chạy thành công lại chạy TIỀN CẢNH** (phần `>> LOG 2>&1 &` không có tác dụng), nên
   nhân Python bận và mọi ô khác xếp hàng. **Không ngắt** — hai thứ quan trọng nhất là điểm
   lưu và `trainer_log.jsonl` đều ghi thẳng Drive, không phụ thuộc nền hay tiền cảnh. Theo
   dõi bằng **Terminal Colab** (`watch` trên `trainer_log.jsonl`), không bị nhân Python chặn.

**Bỏ ô A.5b ở lượt này.** Muốn thử nối tiếp phải giết tiến trình, mà khởi động lại tốn **25
phút mã hoá token**. Giá trị đó đã lấy được ở ô A.3i hôm trước (có `optimizer.pt`, log in
`Resuming training from…`, `global_step` đi tiếp). Trả 25 phút để xác nhận lại chuyện đã
biết là không đáng.

### 4j-2. MẤT MÁY ẢO LẦN THỨ BA (12/8, ~bước 1.780) — và lần này giá chỉ bằng 30 phút

| | 10/8 (chưa có gì trên Drive) | 11/8 (OCR có đồng bộ) | **12/8 (train, điểm lưu trên Drive)** |
|---|---|---|---|
| mất | 42 đơn vị + 8 giờ | 372 ảnh ≈ 3 phút | **180 bước ≈ 30 phút train** |
| khôi phục | làm lại từ đầu | 35 phút tải + 51 phút OCR | ~1 giờ dựng lại môi trường |

Trạng thái lúc mất: `current_steps 1780 / 8072` (22,05%), loss 0,578, `checkpoint-1600` an
toàn trên Drive. ⚠️ **Màn hình cuối người dùng nhìn thấy là bước 1.080** — train vẫn chạy
tiếp gần 12 phút sau khi trình duyệt mất kết nối. Đừng suy trạng thái từ dòng cuối nhìn
thấy; phải đọc `trainer_log.jsonl` trên Drive.

**Lỗi cách chạy đã sửa:** ô A.4 dùng `!cd … && nohup … &` **chạy tiền cảnh** — tiến độ mã
hoá token đổ ra ô, nhân Python bị chiếm suốt nên **không chạy được ô A.5 lẫn ô canh gác
`_ep1`**, phải theo dõi bằng Terminal. Nay đổi sang `subprocess.Popen(...,
start_new_session=True)`: ô trả về ngay và tiến trình sống sót cả khi nhân bị khởi động lại.

### 4j-3. CHẠY TIẾP SAU KHI MẤT MÁY — cơ chế nối tiếp đã chạy ở QUY MÔ THẬT (12/8 08:51)

Ô A.3i hôm 11/8 mới xác nhận nối tiếp trên một lượt 10 bước dựng riêng. Lần này là lượt
thật, 8.072 bước, sau khi mất máy ảo ở bước 1.780:

```
[INFO|2026-08-12 08:51:15] llamafactory.hparams.parser:144 >> Resuming training
from /content/drive/MyDrive/thesis/ckpt/s1_seed101/checkpoint-1600.
```

Cơ chế **bỏ trống `resume_from_checkpoint`** hoạt động đúng như thiết kế. Kiểm bằng một lệnh
`grep` trên log, mất 2 giây — và phải kiểm **ngay lúc khởi động**, vì nếu nó không nhận ra
điểm lưu thì cái giá là 2,5 giờ mã hoá token rồi train lại từ bước 0.

### 4j-4. MÃ HOÁ TOKEN TỐN 2,5 GIỜ, KHÔNG PHẢI 25 PHÚT — và số cũ sai ở chỗ SUY RA

Đo thật trên A100 ngày 12/8: `24000/64567 [56:38<1:34:25, 7.11 examples/s]` ⇒ **2 giờ 31
phút** cho đủ 64.567 mẫu.

Con số "~25 phút" của runbook là **suy** từ 7,3 mẫu/giây đo trên runtime CPU 2 lõi rồi nhân
12 lõi. Giả định "chia được cho số lõi" sai: `ps` cho thấy `llamafactory-cli` chỉ ăn **165%
CPU trên 12 lõi**, vì `datasets.map` chạy một tiến trình — `train_config.yaml` không khai
`preprocessing_num_workers`.

Ba nghi ngờ khác đã loại bằng số đo cùng lúc, đáng ghi lại vì đều là thủ phạm hợp lý:

| nghi | đo | kết luận |
|---|---|---|
| máy ảo ít lõi hơn | `nproc` = **12** | bằng lượt trước |
| có tiến trình tranh CPU | `loadavg` **1,93** | không |
| ảnh đọc qua Drive fuse | 64.567 ảnh ở đúng `/content/ws/...` | không |

⇒ **Mỗi lần đứt phiên tốn ~3 giờ dựng lại** (bung 33 GB 35 phút + mã hoá 2,5 giờ), không
phải ~1 giờ như đã ghi ở mục 4i. Phần train đã làm vẫn không mất.
🔬 Việc nên thử trước lượt hạt giống 202: `preprocessing_num_workers: 8`, đo bằng lượt thăm
dò `max_samples`. Ăn thì bớt ~2 giờ mỗi lượt và mỗi lần đứt — cỡ 14 giờ tường cho 7 lượt còn
lại. Khoá này không đổi dữ liệu ra nên không phải ghi mục sửa đổi `report/106`.

⚠️ **Hai mốc giờ ở mục 4j-2 phải sửa lại.** Neo cứng là `elapsed_time 5:00:06` tại bước
1.780 — đây là thời gian train thuần (1.780 × 10,11 s = 5,0 giờ, khớp; nếu nó tính cả khâu
mã hoá token thì s/bước phải ra 5,06, mâu thuẫn với mọi lượt thăm dò). Kéo lùi lại:

| | bản cũ ghi | tính lại từ `elapsed_time` |
|---|---|---|
| train bắt đầu | — | ~03:40 (03:14 + ~25 phút mã hoá) |
| chạm bước 1.780 | "mất máy ~07h" | **~08:39** — khớp với việc khởi động lại lúc 08:51 |
| chạy tiếp sau khi trình duyệt mất kết nối | "gần 12 phút" | **~2 giờ** (1.780 − 1.080 = 700 bước × 10,11 s) |

"~07h" nhiều khả năng là **lúc người dùng nhìn thấy**, không phải lúc máy ảo bị thu hồi. Còn
con số "12 phút" thì sai hẳn, và **sửa lại làm bài học mạnh hơn chứ không yếu đi**: máy ảo
vẫn train tiếp **khoảng hai giờ** sau khi trình duyệt rớt. Nghĩa là mất kết nối trình duyệt
không giết máy ảo ngay — càng đáng đọc `trainer_log.jsonl` trên Drive thay vì suy từ màn hình
cuối nhìn thấy.

Hệ quả thứ hai: nếu mốc 03:40 đúng thì **lượt đầu mã hoá token chỉ mất ~25 phút thật**, chênh
6 lần với lượt này trên cùng cấu hình. **Chưa giải thích được.** Suy đoán (ghi rõ là suy
đoán): bộ đệm `datasets` còn ấm từ 16 lượt thăm dò ngày 11/8 trên máy ảo cũ. Nếu đúng vậy thì
**2,5 giờ mới là con số của một máy ảo mới** — và đó là con số phải dùng khi lập kế hoạch,
vì mọi phiên nối tiếp đều bắt đầu trên máy ảo mới.

### 4j-5. VIỆC TREO `app_seen_in_train` — ĐÃ TRUY RA VÀ VÁ (12/8, miễn phí)

Chênh lệch 604-vs-67 ở mục 4b nằm trong `harness/tag_app_seen.py`. Nó suy tên ứng dụng của
tập dạy bằng **regex trên câu chữ**, trong khi tập kiểm đọc thẳng trường `app_name`
(`build_test_data.py:84`) — hai nguồn khác nhau thì lệch hình thức bị đọc thành lệch nội
dung. Hai lỗi cụ thể: quét `goal` trước lịch sử rồi `break`, nên câu mục tiêu dài lọt vào
thành tên app (`"adidas app and find local outlet stores…"`) và tên sạch trong lịch sử không
bao giờ được đọc tới; và không cắt dấu chấm cuối nên `"amazon app."` không khớp `amazon`.

Hoá ra `train.jsonl` **có sẵn** `action.open_app.app_name` — đúng trường tập kiểm dùng. Đo
trên lát 1.697 bước có ở máy để bàn:

| nguồn tên ứng dụng của tập dạy | app suy ra | rác | khớp được với 269 app tập kiểm |
|---|---|---|---|
| regex trên câu chữ (bản cũ) | 129 | **42** | 35 |
| **trường `app_name`** | 90 | 0 | **60** |

27 ứng dụng có thật trong tập dạy bị đếm nhầm thành chưa-thấy, gồm `maps`, `youtube music`,
`nike`, `citymapper`, `skyscanner`, `tripadvisor`, `google play books`. Trên lát này, số bước
bị gọi "chưa thấy" giảm **2.262 → 1.756**. Số thật phải chạy lại trên Colab với `train.jsonl`
đủ 64.567 bước (ô **A.1d** mới thêm vào runbook).

Phần còn lại của khoảng cách là do **nguồn khác**: con số 67 hôm 6/8 là một lượt vá tay không
có mã sinh ra (`report/108` mục lỗi đã bắt), đối chiếu với split train đầy đủ của
AndroidControl chứ không phải 12.895 tác vụ thật sự dựng — nhiều ứng dụng hơn nên ít
chưa-thấy hơn. Cả hai cơ chế đều đẩy cùng một chiều, khớp với dấu của chênh lệch.

Bản vá còn chốt hai thứ nhỏ mà im lặng: chuẩn hoá **ký tự vô hình** (`audio­mack` có gạch nối
mềm, `yandex maps` có khoảng trắng cứng, `contacts﻿+` có BOM — so chuỗi thì trượt, mắt thường
không thấy), và **chọn chiều lỗi có chủ ý** — giữ phần suy từ câu chữ làm nguồn phụ, vì gán
nhầm thành "đã thấy" chỉ pha loãng nhóm lớn 2.526 bước, còn gán nhầm thành "chưa thấy" thì
bóp méo đúng nhóm nhỏ đang xét.

⚠️ Chỉ đụng **lát cắt phụ**, không đụng phép so chính S1-vs-S2. Nhưng khâu chấm chạy trên
Kaggle và đọc nhãn thẳng từ `test.jsonl`, nên bản đã gắn nhãn phải theo sang — nếu không thì
lát cắt đọc theo nhãn cũ mà không có gì báo.

### 4j-6. Lượt chạy tiếp — bốn số đo mới (12/8, 11:26 → 12:45)

**Khâu nhảy qua 1.600 bước dữ liệu RẺ, không phải chỗ đáng lo.** Sau khi mã hoá token xong
lúc ~11:26, tiến trình phải bỏ qua 1.600 lô đầu để về đúng chỗ đứt. Đo được: bước 1.601 ở
mốc 17 giây (~94 lô/giây), rồi tốc độ rơi ngay về nhịp train thật (1.604 ở mốc 48 giây).
⇒ **Toàn bộ chi phí của một lần đứt phiên nằm ở mã hoá token (2,5 giờ), không ở khâu nhảy.**
Đây là câu trả lời cho nỗi lo "chạy tiếp ở bước 6.000 thì phải nạp lại 6.000 lô ảnh".

**Tốc độ ở quy mô thật: 10,29 giây/bước.** Đo từ hai đầu một quãng dài — bước 1.640 lúc
11:33:15, bước 2.060 lúc 12:45:15 = 4.320 giây cho 420 bước. Khớp thăm dò 11/8 (10,38) trong
0,9% và khớp số đo bước 20 sáng nay (10,5) trong 2%. ⇒ **Ba phép đo độc lập hội tụ; con số
10,3–10,5 s/bước dùng được để lập kế hoạch cho bảy lượt còn lại.**
Suy ra: một lượt trọn 8.072 bước = **23,1 giờ train** + ~25 phút ghi điểm lưu + 2,5 giờ mã
hoá token nếu máy ảo mới ⇒ **~26 giờ tường mỗi lượt trên máy mới**, ~123 đơn vị tiền card.

**Lượt s1 hạt giống 101 dự kiến xong ~05:55 sáng 13/8** (ghi điểm lưu cuối xong ~06:20).

**Đường cong loss tới bước 2.080** (gộp mỗi 200 bước, đã khử trùng lặp do chạy lại):

| bước | 20–200 | 220–400 | 420–600 | 620–800 | 820–1000 | 1020–1200 | 1220–1400 | 1420–1600 | 1620–1800 | 1820–2000 |
|---|---|---|---|---|---|---|---|---|---|---|
| loss | 1,1030 | 0,6895 | 0,7011 | 0,6497 | 0,6656 | 0,6408 | 0,6251 | 0,6320 | 0,6328 | 0,6114 |

Hình dạng đúng kỳ vọng: rơi mạnh trong 200 bước đầu (học định dạng đầu ra), rồi giảm chậm
và đều. **Chưa chững** — nhật ký ghi `lr 9,227e-5` ở bước 1.780, tức tốc độ học mới đi được
8% quãng đường của lịch `cosine` (đỉnh 1e-4, hâm nóng 404 bước); nó sẽ về ~5,4e-5 ở bước
4.036 và gần 0 ở cuối. Ranh giới sang lượt duyệt thứ hai ở **bước 4.036, khoảng 18:20 ngày
12/8** — chỗ đó thường tụt một nấc; **tăng dần đều sau mốc đó** mới là dấu hiệu học vẹt.

### 4j-6b. "Loss cứ vòng vòng 0,6" — đo bằng hồi quy, KHÔNG bằng mắt (12/8, tới bước 2.620)

Câu hỏi đặt đúng — nhìn nhật ký 20 bước thì loss nhảy 0,53–0,66 không ra quy luật. Hồi quy
trên chính dữ liệu đó cho câu trả lời rõ:

| quãng đo | số điểm | độ dốc /1000 bước | t | sd nhiễu |
|---|---|---|---|---|
| 220 → 2.620 (khối 200 bước) | 12 | **−0,0441** | **−8,9** | 0,0122 |
| 1.020 → 2.620 (nửa sau) | 8 | **−0,0330** | **−6,8** | 0,0067 |
| 2.100 → 2.620 (cửa sổ nhật ký thô) | 27 | −0,0215 | −0,50 | 0,0348 |

⇒ **Chưa hội tụ** — xu hướng giảm chắc chắn trên nền đủ dài, và vẫn còn khi bỏ hết phần dễ.
⇒ **Cửa sổ ngắn mù về mặt vật lý:** trong 520 bước, mức giảm thật ~0,011 còn nhiễu mỗi điểm
0,035 — gấp ba lần tín hiệu. **Cần ít nhất ~1.000 bước liên tục thì xu hướng mới vượt nhiễu**
(t≈2), ~1.350 bước cho t≈3. Đây là con số dùng chung cho mọi lần đọc loss về sau.
⇒ **Dao động là nhiễu thành phần lô, không có cấu trúc lạ:** sd khối gộp 10 điểm là 0,0122,
đúng bằng 0,0348/√10 = 0,011.
⇒ **Không có dấu hiệu tăng:** chia cửa sổ 2.100–2.620 làm đôi được 0,5991 vs 0,5992
(t = +0,01).

Khớp hàm mũ có sàn trên 12 điểm khối: sàn **c ≈ 0,545**, hệ số tắt 0,497/1000 bước (nửa đời
~1.400 bước) → dự báo 0,569 ở bước 4.036 · 0,554 ở 6.000 · **0,548 ở 8.072**.
⚠️ Đây là **cận trên** và ngoại suy vốn yếu (12 điểm, sàn gần như không định danh được). Hai
thứ nó không mô hình hoá — nhịp tụt ở ranh giới lượt duyệt 2 và tốc độ học về 0 ở đoạn cuối
— đều đẩy xuống thấp hơn. Ngoại suy tuyến tính cùng dữ liệu cho 0,344, chắc chắn sai; hai
cách vênh nhau xa cỡ đó là bằng chứng rằng **đừng quyết định gì dựa trên ngoại suy loss**.

**Câu hỏi "0,6 rồi thì dừng được chưa" — không.** Ba lý do độc lập: (a) loss không có ngưỡng
diễn giải được ở bài này, vì đích sinh là câu **do người viết** nên có phần ngẫu nhiên thuần
không học được, sàn không bằng 0; (b) cấu hình **không có tập kiểm định trong lúc train**
(`val_size` đã bỏ) ⇒ không tồn tại tiêu chí dừng sớm hợp lệ, dừng ở đây là nhìn bằng mắt vào
loss huấn luyện; (c) `report/106` khoá **2 lượt duyệt cho MỌI nhánh** — dừng S1 sớm rồi train
S2 đủ thì hiệu số S2−S1 lẫn cả phần "được train lâu hơn", hỏng phép so chính.
**Điều kiện dừng thật:** loss tăng đều qua 500+ bước · `nan` · nhảy vọt >1,5. Nằm ngang không
phải một trong ba.

### 4j-6c. MẤT MÁY LẦN 4 (12/8 ~16:30) — và hai thứ đo được nhờ nó

Mất máy ảo lúc bước ~3.360. Điểm lưu `checkpoint-3000` và `checkpoint-3200` đều nguyên
(182,7 MB, có `optimizer.pt`), máy mới cấp lại đúng **A100-SXM4-40GB**, chạy tiếp từ 3.200
lúc 17:06 ⇒ **mất 160 bước ≈ 27 phút train**, đúng như thiết kế `save_steps: 200`.
Bốn lần mất máy tới nay: 10/8 (42 đơn vị + 8 giờ) · 11/8 (3 phút) · 12/8 sáng (30 phút) ·
12/8 chiều (27 phút + dựng lại).

**⭐ `preprocessing_num_workers: 8` ĂN ĐẬM — 42 phút thay vì 2,5 giờ.** Thử ngay ở lần dựng
lại này (thêm một khoá vào `/content/cfg.yaml` sau ô A.2, trước ô A.4). Log in
`num_proc=8`; khâu `Converting format` xong trong 1 giây ở **48.419 mẫu/giây**; từ dòng
`Resuming` 17:06 tới bước train đầu tiên ~17:48 = **~42 phút**, so với **150 phút** sáng
cùng ngày. **Nhanh 3,6 lần** (không phải 8 lần — có phần chi phí gộp lại).
⇒ Áp cho **bảy lượt còn lại và mọi lần đứt phiên**: tiết kiệm ~1,8 giờ mỗi lần dựng máy mới.
⇒ **Không đổi dữ liệu ra** (`datasets.map` giữ nguyên thứ tự, xáo trộn nằm ở bộ lấy mẫu lúc
train) nên **không phải ghi mục sửa đổi `report/106`**.

**Nhịp tụt ở ranh giới lượt duyệt 2 ĐÃ XẢY RA, đúng bước dự đoán.** `tb10` (trung bình 10 mốc
gần nhất) quanh **0,54–0,575** ở quãng 3.260–4.060, rồi tụt xuống **0,495** ở 4.220 và
**0,465** ở 5.100 — nấc ~0,08 rơi đúng khoảng bước **4.036**.
⚠️ **Đây KHÔNG phải bằng chứng mô hình khái quát tốt hơn** — nó gặp lại đúng dữ liệu lần hai,
loss huấn luyện giảm ở đó là đương nhiên. Chỉ đọc được thành "lượt train khoẻ, đúng kỳ vọng".
⛔ **Rút dự báo sàn 0,548 ở mục 4j-6b:** mới tới bước 5.100 đã xuống 0,465. Đúng như đã khai
lúc đó — khớp hàm mũ là **cận trên** vì không mô hình hoá được nhịp epoch 2. Bài học giữ lại:
**đừng quyết định gì dựa trên ngoại suy loss.**

Tốc độ giữ nguyên **10,2 s/bước** sau khi đổi máy (10,29 đo sáng cùng ngày trên máy trước)
⇒ đổi máy ảo cùng loại card không đổi tốc độ.

### 4j-7. Hai bẫy khi ĐỌC tiến độ — đều là lỗi của ô theo dõi, không phải của máy

**(a) Lấy mẫu 60 giây trên cửa sổ 20 bước cho ra số răng cưa.** 20 bước mất ~206 giây, mà ô
hỏi 60 giây một lần, nên nó bắt được lúc 180 giây (ra 9,0 s/bước) lúc 240 giây (ra 12,0) —
xen kẽ suốt một tiếng rưỡi, **không giá trị nào đúng**, và giờ xong nhảy giữa 03:40 và 08:55.
⇒ **Đo tốc độ phải neo vào MỘT mốc cố định rồi chia cả quãng, đừng chia cửa sổ liền trước.**
Cùng dữ liệu, cách neo cho 10,29 s/bước — sai 0,2% thay vì 17%.

**(b) `trainer_log.jsonl` ghi nối thêm nên KHÔNG lọc được bằng ngưỡng bước.** Sau khi chạy
tiếp từ `checkpoint-1600`, dòng mới đầu tiên là bước **1.620** — *thấp hơn* dòng cuối cũ
(1.780). Nên đặt `MOC = 1780` thì ô theo dõi câm suốt ~35 phút trong khi máy chạy ngon; đặt
`MOC = 1600` thì nó in lại các dòng 1.620–1.780 **của lượt trước** đang nằm sẵn trong tệp,
trông y hệt đang chạy. **Cách đúng: đọc DÒNG CUỐI** (dòng cuối luôn là của lượt hiện tại), và
khi dựng đường cong thì **khử trùng lặp theo số bước, giữ lần xuất hiện sau cùng**.
Dấu hiệu lượt mới đã bắt đầu ghi nhật ký = dòng cuối **tụt xuống** dưới mốc cũ.

**(b2) ⛔ `remaining_time` của LLaMA-Factory SAI SAU KHI CHẠY TIẾP — lạc quan 2,5 lần.** Đo
12/8 23:55: ở bước 5.340/8.072 nó in `còn 3:07:25`, trong khi số thật là **7,7 giờ**. Lý do:
nó tính `elapsed / current_steps`, mà sau khi chạy tiếp `elapsed` chỉ đếm từ lúc khởi động
lại (bước 3.200) còn `current_steps` gồm cả 2.140 bước của lượt trước ⇒ ra 4,12 s/bước thay
vì 10,2. Kiểm lại đúng số: `2.732 × (22.000/5.340) = 11.254 giây = 3:07:34`.
⇒ **Dùng `xong ~` của ô theo dõi tự viết** (nó neo mốc riêng nên không dính), **bỏ
`remaining_time`**. Sai số này đủ lớn để dẫn tới quyết định sai — suýt dùng nó làm căn cứ
"nán lại chờ chạy xong" trong khi thực tế còn gần 8 giờ.

**(c) Chữ `disconnect` trên trình duyệt KHÔNG phải bằng chứng máy ảo chết.** 12/8 trưa hiện
chữ đó trong khi logo Colab vẫn xám và train vẫn chạy. Bằng chứng thật là tệp: `os.stat` trên
log train, xem `st_mtime` cách hiện tại bao nhiêu giây (dưới ~120 giây là sống), kèm
`ps -eo etime,pid,cmd | grep [l]lamafactory`. ⚠️ Log **không** tên `train.log` — ô A.2 sinh
`LOG = /content/train_{BRANCH}_seed{SEED}.log`, phải dò bằng `glob("/content/train_*.log")`.

### 4j-8. MẤT MÁY LẦN 5 (12/8 tối, ~bước 5.540) — phép thử "gập nắp mang đi" THẤT BẠI

Tối 12/8 phải mang máy đi làm. Ba đường đã cân: (1) để máy chạy tại nhà · (2) gập nắp mang
theo, chặn ngủ bằng `powercfg /change standby-timeout-dc 0` + `monitor-timeout-dc` +
`hibernate-timeout-dc`, lid = *Do nothing*, **không đóng tab, không shut down** · (3) tắt hẳn,
tối về dựng lại. Chọn (2) vì hỏng thì tự rơi về (3), không mất thêm gì.

**Kết quả: hỏng.** Sáng 13/8 máy ảo đổi tên (`65d1097af2af` → `ea8ca03ec1c9`), `/content/ws`
mất, không còn tiến trình train. Đọc mốc giờ mới thấy đau: `trainer_log.jsonl` **ngừng ghi
12,0 giờ trước**, tức máy chết gần như ngay sau khi gập nắp — không phải chạy được vài giờ
rồi mới đứt. ⇒ **ba lệnh `powercfg … -dc 0` KHÔNG đủ**; nghi mất mạng lúc chuyển vùng hoặc
Modern Standby vẫn cắt mạng dù CPU còn thức. **Đừng thử lại cách này**: hoặc để máy chạy tại
chỗ có sạc, hoặc chấp nhận đứt và tính luôn 1,4 giờ dựng lại vào kế hoạch.

**Cái giá:** bước cuối ghi được 5.540, điểm lưu cuối `checkpoint-5400` ⇒ mất **140 bước ≈ 24
phút train**, cộng dựng lại (bung ảnh ~40 phút + mã hoá token ~42 phút) ≈ **1,8 giờ ≈ $0,9**.
Cộng dồn năm lần đứt: ~12 giờ và ~60 đơn vị. Còn **bảy lượt ~24 giờ** phía trước ⇒ phải tra
xem gói Colab đang dùng có **background execution** không (Pro+ có) — có thì đóng trình duyệt
vẫn chạy và **xoá hẳn lớp lỗi này**, đáng giá hơn mọi tối ưu tốc độ đã làm.

**Hai chi tiết kiểm được việc gì:**
- **Cỡ điểm lưu đổi 182,7 → 191,6 MB** nhưng *cả hai* bản 5200 và 5400 đều 191,6 ⇒ không phải
  ghi dở. Phép kiểm rẻ cho câu "điểm lưu có trọn không": **ghi dở thì bản CUỐI phải NHỎ HƠN
  bản trước nó**; hai bản bằng nhau chính xác là bằng chứng cả hai đều trọn.
- **`grep "Resuming training from"` chạy ngay sau A.4 trả về TRỐNG — và đó là báo động giả.**
  Log lúc đó mới 0 byte. Dòng `Resuming` in ở `hparams.parser:144`, sớm thật, nhưng vẫn sau
  khâu nạp thư viện (~40 giây). ⇒ **thấy trống thì đừng giết tiến trình ngay**, hỏi ba thứ
  trước: `os.path.getsize(log)` · `ps -p <PID>` · `tail -30`. Chỉ khi log đã qua khâu phân
  tích tham số mà vẫn không có dòng đó mới là hỏng thật. Suýt `pkill` một lượt chạy lành.

**Số đo lặp lại được:** `preprocessing_num_workers: 8` cho `Converting format` **33.177
mẫu/giây** (lần trước 48.419) — cùng bậc, xác nhận khoá này ăn thật chứ không phải may một
lần. `yaml.safe_dump` ghi đè `cfg.yaml` **không làm mất khoá nào** (đối chiếu đủ 34 khoá),
chỉ mất chú thích — an toàn để vá cấu hình bằng script.

### 4j-9. MẤT MÁY LẦN 6 (13/8 ~20:30, bước 7.880) — và đuôi lịch cosine đọc được gì

**Chết cách đích 192 bước.** Điểm lưu cuối `checkpoint-7800`, mất 80 bước train. Dựng lại
mất ~1,4 giờ (bung ảnh + mã hoá token) rồi chạy nốt 272 bước ≈ 46 phút, tổng ≈ **$1,1**.

**Quyết định: chạy nốt, KHÔNG lấy `checkpoint-7800` làm bản cuối.** Về số thì hai bản gần
như trùng — `lr` ở đoạn đó đã xuống ~1e-8 nên trọng số gần như đứng yên. Nhưng `report/106`
đăng ký trước luật chọn điểm lưu là *dùng bản cuối 2 lượt duyệt*; lấy bản 7.800 là lệch khỏi
hồ sơ và phải viết một mục khai giới hạn. **$1,1 mua một dòng không phải giải trình** — đúng
thứ tự ưu tiên đã chốt (độ chính xác trước, tiền sau).

**Dấu hiệu nhận biết mới: nhân Python restart thì Drive rớt gắn.** Ô theo dõi văng
`FileNotFoundError` trên `trainer_log.jsonl` trong khi tệp vẫn nằm nguyên trên Drive web
(PID nhân đổi từ … sang `ipykernel_7177` là manh mối). ⇒ Gặp lỗi này **đừng chạy lại A.4**;
chạy ô chẩn đoán ba câu — tên máy · `ps -eo pid,etime,cmd | grep '[l]lamafactory-cli'` ·
`st_mtime` của `/content/train_*.log` — rồi mới quyết. Lần này ba câu đó cho ra máy ảo đã
đổi tên (`ea8ca03ec1c9` → `47040838ba9e`), tức mất máy thật, chứ không phải chỉ rớt nhân.

**Đuôi lịch `cosine` — đọc từ 21 dòng nhật ký, bước 6.060 → 7.840 (5 giờ):**

| | dải giá trị | biên độ |
|---|---|---|
| `loss` (một lô 16 mẫu) | 0,415 – 0,518 | **0,103** |
| `tb10` (trung bình 10 lô) | 0,4511 – 0,4726 | **0,0215** |

Trung bình 10 lô làm biên độ hẹp đi ~5 lần, đúng quy luật √10 ≈ 3,2 (các cửa sổ gối nhau nên
không khớp chính xác). ⇒ **cái "nhảy qua nhảy lại" là nhiễu độ khó giữa các lô, không phải mô
hình học rồi quên.** Đường thật gần như phẳng: `tb10` đi 0,4712 → 0,4554 trong 1.780 bước,
trong khi `lr` tụt **1,61e-05 → 2,28e-07** (gần bằng 0 theo thiết kế của lịch cosine).
**Phẳng ở đây là kết thúc sạch, không phải chững vì hỏng** — và nhắc lại: loss huấn luyện
không phải thước quyết định, thước quyết định là executability trên tập kiểm, nền 70,0%.

**Đã tra xong câu hỏi treo về `background execution`:** bảng Resources in
`You are not subscribed · Available: 391.3 compute units · 5.3 per hour`. Tài khoản đang dùng
**đơn vị trả trước, không đăng ký Pro/Pro+ ⇒ KHÔNG có background execution.** Không có cách
nào đóng trình duyệt mà máy vẫn chạy. Cộng dồn 6 lần mất máy: **~14 giờ, ~70 đơn vị**.

### 4j-10. LƯỢT TRAIN ĐẦU TIÊN XONG (13/8 22:43) — và ba số của HF phải vứt

`s1` hạt giống 101 chạy hết **8.072 bước / 2 lượt duyệt**, qua sáu lần mất máy ảo.
`adapter_model.safetensors` **59,9 MB** (đúng cỡ 14.966.784 tham số ở fp32).

⛔ **Ba số trong `all_results.json` SAI sau khi chạy tiếp — cấm trích vào luận văn:**
`train_loss = 0,0151` không phải loss cuối; HF cộng dồn loss **chỉ từ lúc khởi động lại**
(272 bước) rồi chia cho cả 8.072. Kiểm: 0,01505 × 8.072 ÷ 272 = **0,447**, khớp đúng vùng
loss thật những bước cuối. Kéo theo `train_runtime = 45:55` (chỉ lượt cuối) và
`train_samples_per_second 46,87` / `steps_per_second 2,93` cũng hỏng — tốc độ thật **10,2
s/bước**. Cùng lớp lỗi với `remaining_time` ở mục 4j-7 (b2): **mọi số HF chia cho `elapsed`
đều hỏng sau resume.** Số dùng được nằm ở `trainer_state.json`, ô A.10 đã bóc sẵn.

⛔ **BẢN NÀY ĐÃ SAI, ĐÃ SỬA 17/8 — xem mục 4j-15.** ~~`total_flos` thì đúng và làm được bằng
chứng: **3.857.778.344 GF**. Ngoại suy từ thăm dò 11/8 (9.527.912 GF cho 20 bước) ra
3.845.466.483 GF — **lệch 0,32%**.~~ Con số 3.857.778.344 là **ghi sai**: đọc lại
`trainer_state.json` và `all_results.json` của chính lượt 101 ngày 17/8, cả hai cho
**4.142.257.957 GF**. Kết luận "không mất cũng không lặp bước nào" **vẫn đứng**, nhưng bằng
chứng cứ khác — xem 4j-15.

**Mốc dừng 5 — A.6 ĐẠT, A.7 sạch, A.7b LỘ MỘT LỖ:**
- **A.6: 8/8 trùng nguyên văn** ⇒ chấm theo lô an toàn, đệm bên trái không làm lệch kết quả.
- **A.7:** câu tiếng Anh mạch lạc, đúng khuôn một câu, không lặp vô hạn, `pred` trùng `raw`
  (đúng với s1 vì không có `<desc>` để cắt). Trong 8 câu xem tay: 2 trùng gần nguyên văn câu
  chuẩn · 1 sai app thật (Tripadvisor thay vì Foursquare) · 1 ca tả **vị trí** thay vì gọi
  **tên** phần tử (*"Open the second video from the list"* vs chuẩn *"click on the Dimitri
  vegas song"*) — đúng kiểu hỏng mà S2 nhắm vào. ⚠️ n=8, **chỉ để biết đường ống chạy đúng,
  tuyệt đối chưa phải kết quả.**
- ⛔ **A.7b: chữ ký lượt chạy KHÔNG hoạt động.** Chạy `--ceiling gold` ghi vào tệp của lượt
  `lora:s1_seed101` thì nó in `Xong sẵn 20 bước` và thoát, thay vì `⛔ … là của lượt chạy
  KHÁC`. Cơ chế **nối tiếp** thì chạy đúng (`đã có 20 bước, còn 0`, không sinh lại câu nào),
  nhưng nó in `Nạp …` trước — mà bản vá 12/8 đã dời khối nối tiếp lên trước lúc nạp mô hình.
  ⇒ **gói `thesis_rented.zip` trên Drive là bản trước các vá sáng 12/8**, đúng cùng nguyên
  nhân làm ô A.1d ra con số 604 của bản có lỗi.
  **Không chặn lượt này** (một nhánh, một tệp đích, không có gì để lẫn), nhưng **phải đóng
  gói lại zip trước chiến dịch nhiều nhánh** — chỗ đó mới là nơi lỗi câm cắn: hơn chục lượt
  chỉ khác vài cờ, quên đổi `--out` là thoát sau hai giây trông y như đã chạy xong.

### 4j-11. `app_seen_in_train` — SỐ THẬT Ở QUY MÔ ĐỦ (14/8, runtime CPU miễn phí)

Đóng gói lại `thesis_rented.zip` với bản vá 12/8 (`infer_branch.py` 26.062 → **27.443 B**,
có chữ ký lượt chạy; `tag_app_seen.py` đọc `action.open_app.app_name`) rồi chạy lại ô A.1d
trên `train.jsonl` đủ 64.567 bước. **Không cần card, không cần ảnh, 0 đơn vị.**

| | trước (mã lỗi) | **sau (mã đã vá)** |
|---|---|---|
| app nhận ra ở tập dạy | 2.766 | **1.717** (673 từ trường `app_name` + 1.044 suy từ câu chữ) |
| đã thấy lúc dạy | 2.526 | **2.991** |
| CHƯA thấy lúc dạy | 604 | **139** (22 app) |
| không gán được app | 3.828 | 3.828 (không đổi) |
| tỉ lệ trong phần gán được app | 80,7% | **95,6%** |

Số app tụt 2.766 → 1.717 chính là **phần rác regex bị loại**: bản cũ quét `goal` trước rồi
`break` nên câu mục tiêu dài lọt vào thành tên app. 465 bản ghi đổi nhãn.

**Hội tụ về phía hồ sơ 6/8** (21 app / 67 bước) thay vì 604: nay 22 app / 139 bước. Khoảng
cách còn lại đã biết nguyên nhân và **không phải lỗi** — hồ sơ 6/8 đối chiếu với split train
**đầy đủ** của AndroidControl, còn đây là 12.895 tác vụ thật sự dựng được. Danh sách 22 app
đọc hợp lý (`altfit` 18 · `orbitz` 13 · `immoscout24` 13 · `sneaker thief` 10 …), không còn
tên bị đếm nhầm kiểu `maps` / `nike` / `citymapper`.

⚠️ **PHẢI SỬA TRONG LUẬN VĂN:** hồ sơ cũ ghi *"92% app trong tập kiểm cũng có ở tập dạy"*.
Số đúng ở quy mô đủ là **95,6%** — **lợi thế sân nhà RÕ HƠN chứ không nhẹ đi**. Vẫn kèm cảnh
báo: **3.828/6.958 bước (55%) không gán được app** ⇒ nhóm đó là *không biết*, cấm đọc thành
*chưa thấy*. Bản đã gắn nhãn nằm ở `MyDrive/thesis/test_jsonl_tagged.jsonl` — **phải mang
đúng tệp này sang Kaggle**, vì `score_run.py:405` đọc nhãn thẳng từ đó.
⇒ **Việc treo cuối cùng của phiên train đã xoá.**

### 4j-12. ⭐ ĐIỂM SỐ THẬT ĐẦU TIÊN — s1 hạt giống 101 (14/8, Kaggle T4, miễn phí)

> ⚠️ **MỤC NÀY VIẾT KHI TRẦN CÒN LÀ 70,0%.** Điểm 59,1% [57,3–60,8] vẫn đúng, nhưng mọi con số
> **dẫn xuất từ trần** trong mục này đã bị thay ở **mục 4j-13**: room *485 bước / 10,9 pp* →
> **741 bước / 16,6 pp** · *S1 đạt 84,4% của trần* → **78,1%** · *S2 phải sửa 40–60% room* →
> **16–27%** (nhờ MDE ghép cặp). **Đọc 4j-13 trước.**

Chấm đủ **4.462 bước chạm** (tệp có 4.463, **1 bị bỏ vì câu rỗng** — ep 18710/step 1).
5,6 giờ trên Kaggle, 0 đồng. Kết quả ở `runs/score_s1_seed101.json` + tệp thô
`runs/score_s1_seed101_raw.jsonl`.

| | giá trị |
|---|---|
| **Executability (ô Voronoi, headline)** | **59,1%** KTC95 **[57,3 – 60,8]** |
| đĩa dung sai (báo kèm) | 69,2% [67,6 – 70,7] |
| cụm | 1.091 · **hiệu dụng 454,3** |
| n | 4.462 |

`g_eff` **454,3** khớp đúng con số tính trước ngày 9/8 — xác nhận quy tắc cụm-đơn hoạt động
như thiết kế.

#### (a) Điều kiện sống còn của thiết kế: ĐẠT

Kịch bản giết luận văn là **S1 chạm trần** — khi đó không còn chỗ cho S2 và mọi so sánh vô
nghĩa. Nó vừa bị loại bằng số: trần thước **70,0% [64,5–75,3]** so với S1 **59,1%
[57,3–60,8]**, **hai khoảng tin cậy KHÔNG chồng lấn**. Thước cũng không suy biến về sàn.
Room 10,9 pp > MDE chiếu 3,9–6,6 pp ⇒ **cuộc thí nghiệm còn đáng chạy** — điều mà trước
ngày 14/8 chưa ai biết chắc.

#### (b) ⭐ LỢI THẾ SÂN NHÀ KHÔNG XUẤT HIỆN — đòn phản biện nặng nhất bị vô hiệu

| lát cắt | n | exec |
|---|---|---|
| app **đã thấy** lúc dạy | 1.737 | **59,1%** |
| app **CHƯA thấy** | 78 | **59,0%** |
| không gán được app | 2.647 | **59,2%** |

Chênh 0,1–0,2 điểm. Hồ sơ tự khai từ 6/8 rằng *"92% (nay 95,6%) app tập kiểm cũng có ở tập
dạy nên điểm bị thổi"* — **không có cơ sở thực nghiệm**. Nhóm chưa-thấy chỉ n=78 nên KTC
rộng, nhưng chênh 0,1 pp không thể là hiệu ứng lớn. Vẫn khai giới hạn, nhưng nay khai kèm
số bác bỏ chứ không phải khai suông.

#### (c) Chỗ hỏng đúng là chỗ S2 nhắm vào

Mô hình gọi **đúng loại thao tác 94,4%** số bước. Trong **1.824 bước trượt**: chỉ **251 do
sai thao tác**, còn **1.573 (86%) là thao tác đúng nhưng bộ trỏ không tìm ra nút**. ⇒ lỗi
nằm ở **cách gọi tên / tả phần tử**, không ở việc hiểu phải làm gì. Bằng chứng trực tiếp
cho động cơ của nhánh "mô tả trước, phát ngôn sau", đo trên chính mô hình đã huấn luyện
chứ không phải suy từ pilot 76 câu gold.

#### (d) ⚠️ ROOM THẬT CHỈ ~485 BƯỚC, KHÔNG PHẢI 1.573 — con số đáng lo nhất

Nhìn thoáng thì 1.573 ca trỏ trượt nghe như rất nhiều chỗ để cải thiện. **Sai.** Trần 70%
nghĩa là **ngay cả câu người viết cũng trượt 30%** — đó là giới hạn của dụng cụ.

| | bước |
|---|---|
| Tổng bước chạm | 4.462 |
| Trượt kể cả nếu câu hoàn hảo (30% × 4.462) | ~1.339 |
| S1 trượt thật | 1.824 |
| **Room thật do câu chưa đủ tốt** | **~485 = 10,9 pp** |

⇒ **S2 phải sửa được 40–60% của 485 bước đó** mới vượt MDE 3,9–6,6 pp. Đối chiếu hiệu ứng
kỳ vọng từ văn liệu (+3…+11 pp, trung vị ~+5): **trung vị kỳ vọng nằm ngay trong dải MDE**.
Xác suất ra kết quả đọc được ≈ **50%** — đúng như ước từ đầu (P ≈ 0,50–0,60), nay có số đo
xác nhận thay vì phỏng đoán. **Rủi ro cụ thể nhất: S2 − S1 rơi vào 0–4 pp ⇒ kết cục "trắng"**
theo luật đã đăng ký trước.

#### (e) ⚠️ Thiên vị câu dài đã đo được: 5,4 pp

Cắt tại trung vị 33 ký tự: câu **ngắn 56,5%** (n=2.293) · câu **dài 61,9%** (n=2.169).
Nếu S2 sinh câu dài hơn thì một phần chênh lệch có thể chỉ là độ dài. ⚠️ Nhánh **S2r kiểm
soát độ dài của TIỀN TỐ, không kiểm soát độ dài CÂU ĐẦU RA** ⇒ **bắt buộc phân tầng theo độ
dài khi đọc S2**, nay đã có số nền để làm.

#### (f) 🔬 Việc miễn phí có thể đổi cục diện: MDE phải tính GHÉP CẶP

S1 và S2 chấm trên **cùng 4.462 bước** ⇒ đừng tính MDE như hai mẫu độc lập. Chỉ đếm số bước
**bất đồng** (S1 đúng/S2 sai và ngược lại) — kiểm định **McNemar**. Phương sai của hiệu số
ghép cặp nhỏ hơn nhiều so với hiệu hai tỉ lệ độc lập ⇒ **MDE thật có thể xuống dưới 3 pp**,
mở rộng hẳn vùng phát hiện được. Đây là thay đổi ở **cách đọc**, không ở dữ liệu — miễn phí.
**Khi có s1/202 phải tính CẢ HAI cách** rồi mới khoá ngưỡng.

### 4j-13. ⭐⭐ TRẦN THẬT LÀ 75,7% — KHÔNG PHẢI 70,0% (15/8, Kaggle, 0 đồng)

Chấm **câu chuẩn của người viết** trên **đủ 4.462 bước** thay vì suy từ 300 điểm của cổng A.
Cách làm rẻ hơn tưởng: **không cần sinh câu, không cần GPU Colab** — dựng tệp `preds` trong đó
`pred` = `gold_instruction` (`runs/preds_ceiling_human.jsonl`) rồi chấm như mọi nhánh.

| | cỡ mẫu | trần Voronoi | đĩa |
|---|---|---|---|
| cũ (`gate_a_ceiling.py`, suy từ vết cổng A) | 300 | 70,0% [64,5–75,3] | 81,3% |
| **mới (chấm đủ)** | **4.462** | **75,7% [74,1–77,3]** | **84,3%** |

Chênh **+5,7 điểm**, nằm ngay ngoài mép trên KTC cũ; KTC hẹp từ ±5,4 xuống **±1,6**.
⇒ **Mẫu 300 lệch thấp.** Bài học: đại lượng mà mọi số khác đọc dựa vào thì đừng đo trên mẫu con.

#### Bảng ba nhánh, cùng 4.462 bước

| | executable | hit_voronoi | action_ok |
|---|---|---|---|
| **Human (trần)** | **75,7%** | 75,8% | 100% (theo định nghĩa) |
| **S1 (SFT)** | **59,1%** | 60,2% | 94,4% |
| **Base (chưa train)** | **47,6%** | 48,9% | 96,5% |

Ghép cặp (McNemar, đều p<0,001): S1−Base **+11,5 pp** (χ²=243,2 · b=284, c=798) ·
Human−S1 **+16,6 pp** (χ²=579,5 · b=102, **c=843**) · Human−Base **+28,1 pp** (χ²=1.077,8).
**SE của hiệu ghép cặp 0,64–0,75 pp ⇒ MDE ghép cặp 1,8–2,1 pp** (chưa hiệu chỉnh cụm; áp tỉ lệ
0,68 lên MDE chiếu cũ ⇒ **ước 2,7–4,5 pp có cụm**).

#### Room tính lại — rộng hơn 50%

| | với trần 70,0 | **với trần 75,7** |
|---|---|---|
| room cho can thiệp | 485 bước · 10,9 pp | **741 bước · 16,6 pp** |
| S1 đạt % của trần | 84,4% | **78,1%** |
| SFT lấy được % khoảng Base→trần | 51% | **41%** |

Con số cụ thể nhất: **843 bước câu người định vị được mà câu S1 thì không** (chiều ngược lại chỉ
102). Đó là vùng S2 có thể ăn. Với MDE ~2,7–4,5 pp, **S2 chỉ cần lấy 16–27% room** — trước đó
tính là 40–60%.

#### ⭐ NĂM ĐÒN PHẢN BIỆN "S1 hơn Base": SỐNG SÓT CẢ NĂM

1. **"Thắng vì bắt chước phong cách câu chuẩn"** — bác. Base cũng mở đầu bằng `click` 84%;
   tỉ lệ dùng động từ chạm: Human 91,2% · S1 87,5% · **Base 86,0%**. Gần như nhau.
2. **"Chênh do `action_ok`"** — bác. Bỏ hẳn `action_ok`, chỉ định vị thuần: **+11,3 pp**
   (b=272, c=777).
3. **"Chỉ thắng ở một loại bước"** — bác. Bước đầu tác vụ **+15,0** · bước sau **+11,0**.
4. **"Chỉ thắng ở màn dễ"** — bác. Ít phần tử +12,7 · vừa +9,4 · nhiều +12,3.
5. **"Vài app kéo cả bảng"** — bác. Trên 1.091 cụm: thắng **395** · hoà 565 · thua **131**.

#### ⚠️ Thước mù ở đâu — đo được rồi

**1.083 bước (24,3%) mà chính câu người cũng trượt.** Trong đó **72% là do bộ trỏ sai >14% bề
ngang** — nó **bỏ cuộc**, không phải câu mơ hồ. Sai số lưỡng cực rõ: ca trúng trung vị **0,4%**,
ca trượt **26,2%**, không có vùng giữa. **935 bước (21% toàn tập) cả ba nhánh cùng trượt** —
vùng thước không phân giải được gì. ⇒ **trần 75,7% là giới hạn của DỤNG CỤ, không phải của
ngôn ngữ.**

✅ **Nghi ngờ "câu chuẩn hỏng làm hạ trần" BỊ BÁC:** câu chuẩn ≤3 từ cho trần **77,0%**, dài
hơn 3 từ cho 75,7% — câu ngắn không tệ hơn.
✅ **102 ca người trượt mà S1 trúng là THẬT, không phải may** — xem tay thấy đó là chỗ câu chuẩn
mơ hồ còn S1 cụ thể hơn (`Select the tab shown on the screen` vs `Click on the tab Toronto
Pearson International`).
⚠️ **Giới hạn còn lại chưa kiểm: chỉ một bộ trỏ (UGround).** Phép so **giữa các nhánh** hợp lệ
vì cùng dụng cụ, nhưng **con số tuyệt đối gắn với UGround**. `score_run.py --grounder openai`
kiểm chéo được, tốn tiền API, không bắt buộc.
⚠️ Hai bước có `toggle_conflict` với **chính câu chuẩn của nó** (75,77% hv vs 75,73% exec) —
lỗi nhỏ trong hàm đó, ảnh hưởng 0,04%.

### 4j-14. VIỆC ĐÃ TRA XONG, CHƯA CHẠY — kiểm chéo bộ trỏ thứ hai (tra 15/8)

**Đã tra kỹ và verify tận nguồn, ĐỪNG TRA LẠI.** Câu hỏi: kết luận "nhánh A hơn nhánh B" có
đổi khi đổi dụng cụ đo không? Toàn bộ số hiện tại gắn với **một** bộ trỏ (UGround).

#### ⭐ Chọn: `inclusionAI/UI-Venus-Ground-7B` (Apache-2.0, không gated)

| | UGround (đang dùng) | **UI-Venus-Ground-7B** | Phi-Ground-4B | ShowUI-2B |
|---|---|---|---|---|
| ScreenSpot-v2 mobile | 95,0 / 83,3 | **99,0 / 90,0** | 78,1 (gộp) | — |
| nền | Qwen2-VL | Qwen2.5-VL-7B | **Phi-3.5-Vision** | Qwen2-VL |
| sạch AndroidControl | ✅ | ✅ | ✅ | ✅ |
| chạy T4 16GB | ✅ | chỉ khi NF4 | ✅ 8,5 GB | ✅ |

Lý do chọn UI-Venus: **mạnh hơn UGround ở mobile**, mà điều kiện then chốt là bộ trỏ thứ hai
phải **qua được cổng A** (sai số trung vị ≤3% bề ngang) — không qua thì phép kiểm chéo chỉ đo
nhiễu của dụng cụ. Lấy điểm = tâm bbox chuẩn hoá 0–1 (có sẵn công thức ở model card).
⚠️ Lượng tử hoá NF4 ăn vào đúng thứ cổng A đo ⇒ **ưu tiên chạy A100 hơn T4**.

**Phi-Ground-4B** = lựa chọn duy nhất **ngoài họ Qwen**, khai thẳng *"We did not include any
mobile data in the training set"* và chỉ lấy lát sạch của OS-Atlas. Đổi lại nó **yếu nhất đúng
ở mobile**. Dùng nếu ưu tiên độc lập-họ-mô-hình hơn chất lượng.
**ShowUI-2B** = phương án T4 thuần, trả điểm chuẩn hoá 0–1 sẵn. ⚠️ Rủi ro: Qwen2-VL có lỗi
**tràn số fp16 → NaN/rác** (transformers #33294, #35151 vá đúng nhánh eager-attention mà T4
buộc dùng) ⇒ phải thử vài mẫu trước; đường lui là fp32 (2B ≈ 8,8 GB, vẫn vừa).

#### ⛔ Đã loại, có lý do — đừng cân nhắc lại

| | vì sao |
|---|---|
| **GUI-G2-3B** | nền **Qwen2.5-VL-3B — trùng đúng mô hình sinh của luận văn**, tệ nhất về tính độc lập. Con số 98,3/91,9 trên model card là của bản **7B chép nhầm** |
| **Jedi** | bảng dữ liệu ghi `AndroidControl · 54.678 images · Sampling: All` — dù bài tự quảng bá "chỉ dữ liệu tổng hợp" |
| **CogAgent-9B-20241220** | không có paper arXiv, báo cáo kỹ thuật link chết ⇒ **vĩnh viễn không kiểm được** dữ liệu train; lại cần ≥29 GB |
| **Aria-UI** | 3,9B *activated* nhưng **25,3B tổng** (MoE phải nạp hết) ≈ 50 GB |
| **OS-Atlas** | đã loại từ trước, nhiễm AC |
| **SE-GUI · GUI-G1 · GUI-R1 · Holo1/1.5 · GUI-Cursor · POINTS-GUI-G** | nhiễm **gián tiếp** qua OS-Atlas hoặc qua pool trộn |

#### ⚠️ CÂU CHỮ TRONG LUẬN VĂN — chỗ dễ bị vặn nhất

UI-Venus, ShowUI, GUI-G2 **không có AndroidControl** nhưng **KHÔNG phải chưa từng thấy
Android** — chúng dùng Widget Captioning, UI RefExp, RICO, đều là kho Android.
✅ Viết: *"bộ trỏ không được huấn luyện trên AndroidControl"*.
⛔ Cấm viết: *"chưa từng thấy màn hình di động"*.
Lập luận phụ trợ dùng được: Widget Captioning (EMNLP 2020), UI RefExp (2021), RICO (2017) đều
**ra đời trước AndroidControl (6/2024)** ⇒ về mặt thời gian không thể chứa nó.

#### Cách chạy khi tới lúc — RẺ, đừng chạy toàn tập

**Lát 500 bước, hai nhánh S1 và Base, ~1,2 giờ tổng.** Đủ trả lời đúng câu phản biện:
*thứ tự các nhánh có đổi khi đổi dụng cụ không?* Con số tuyệt đối sẽ khác — điều đó bình
thường và không phải vấn đề, vì phép so nội bộ dùng cùng dụng cụ.
Chạy toàn tập 3 nhánh = 17 giờ quota Kaggle, **không đáng**.

#### Hai chỗ CHƯA giải quyết được

- **UI-R1** và **InfiGUI-R1** dùng **split nào** của AndroidControl — cả hai paper đều không nói.
- **SE-GUI**: 3.018 mẫu còn lại có sót mẫu gốc AndroidControl không. **Tự kiểm được**, tập công
  khai ở `XinBB/SE-GUI-3k`.

### 4j-15. LƯỢT s1 HẠT GIỐNG 202 XONG (17/8 00:40) — và `total_flos` phải sửa

Lượt thứ hai của cặp hạt giống chạy xong đủ **8.072 bước**, `adapter_model.safetensors`
**59,9 MB**. Ba lần mất máy (bước 2.480 · 4.880 · 7.280), mỗi lần mất đúng phần từ điểm lưu
gần nhất tới lúc chết = **80 bước**, vì `save_steps: 200` mà log ghi mỗi 20.

**Cặp hạt giống khớp rất chặt** — đây là thứ cần cho MDE:

| | seed 101 | seed 202 | lệch |
|---|---|---|---|
| `global_step` | 8.072 | 8.072 | — |
| `total_flos` | 4.142.257.957 GF | 4.142.783.361 GF | **0,013%** |
| GF mỗi bước | 513.164 | 513.229 | 0,013% |
| loss đuôi-20 | 0,4486 | 0,4467 | 0,0019 |
| số lần mất máy | **6** | **3** | — |

Và xem tay 8 câu sinh: lượt 202 mắc **đúng lỗi** của lượt 101 ở cùng bước 18175/0
(*"Open Tripadvisor app"* thay vì Foursquare). n=8 nên chỉ đọc là "đường ống chạy đúng".

#### ⛔ Số đã bị rút: `total_flos = 3.857.778.344 GF`

Mục 4j-10 ghi con số đó cho lượt 101 và kết luận *"khớp ngoại suy từ thăm dò trong 0,32%
⇒ cả 8.072 bước chạy thật"*. Đọc lại ngày 17/8 thì **cả `trainer_state.json` lẫn
`all_results.json` của chính lượt 101 đều cho 4.142.257.957 GF** — hai tệp khớp nhau 0,00%.
Con số cũ cao hơn ngoại suy đúng 0,32% và thấp hơn số thật 7,4%; nó là **số ghi sai**, không
phải số đo.

**Ba hệ quả:**

1. **`all_results.json` KHÔNG hỏng ở trường `total_flos`.** Mục 4j-10 chia đôi tệp đó —
   bác `train_loss`/`train_runtime`/`*_per_second` nhưng tin `total_flos` — mà không có căn cứ
   nào cho việc chia đôi. Hoá ra trường này vốn vẫn đúng; chỉ mấy trường **chia cho `elapsed`**
   mới hỏng sau resume.
2. **Lập luận cũ vòng tròn.** "Số đo khớp ngoại suy" mất giá trị nếu số đem so lại chính là
   kết quả ngoại suy. Phải bỏ.
3. **Ngoại suy từ thăm dò lệch 7,7% — và có lý do.** Lượt thăm dò chạy `max_samples`, tức lấy
   **phần đầu tập dữ liệu chưa trộn**, nên độ dài chuỗi trung bình không đại diện cho toàn tập.
   ⇒ **Bài học: số suy từ lượt thăm dò `max_samples` không ngoại suy được sang toàn tập** nếu
   đại lượng đó phụ thuộc độ dài chuỗi.

#### ✅ Bằng chứng thay thế, chặt hơn và không vòng tròn

Kết luận *"không mất cũng không lặp bước nào"* **vẫn đứng**, bằng lập luận khác:

> Hai lượt train độc lập, số lần đứt phiên khác hẳn nhau (**6** vs **3**), cho `total_flos`
> mỗi bước khớp **0,013%**; và trong lượt 202, nhịp giữa hai điểm lưu cuối phẳng
> (513.256 ở bước 8.000 → 513.229 ở 8.072). Nếu việc nối tiếp làm sai kế toán thì hai lượt
> phải lệch **theo số lần đứt**. Chúng không lệch.

Lập luận này không mượn con số nào từ thăm dò, nên dùng được cho phần tái lập của bài.

#### ✅ A.7b — việc treo từ 13/8 đã đóng

Mốc dừng 5 của lượt 101 để lại một lỗ: chữ ký lượt chạy không hoạt động. Sau khi đóng gói lại
`thesis_rented.zip` với bản vá (`infer_branch.py` 27.443 B), thử lại ngày 17/8 bằng **hai** ca
thay vì một:

- **Nối tiếp có ghi thêm thật:** tệp đã có 20 bước, xin 30 → in `còn 10` → `Nạp Qwen…` →
  sinh xong, tệp thành **30 dòng**. ✅
- **Chữ ký có chặn:** chạy `--no-adapter` lên đúng tệp đó → thoát ngay
  `⛔ … là của lượt chạy KHÁC: ['lora:s1_seed202'] ≠ 'base'`. ✅

⚠️ **Lần thử đầu không phải phép thử.** Xin đúng 20 bước trong khi tệp đã có 20 → `còn 0` →
in `Xong sẵn` rồi thoát. Không có gì để nối tiếp thì không chứng minh được nối tiếp chạy.
**Phép thử nối tiếp phải xin NHIỀU HƠN số đã có.**

### 4j-16. LƯỢT S2 HẠT GIỐNG 101 XONG (19/8) — và một chẩn đoán ĐĂNG KÝ TRƯỚC khi có điểm

**Số của lượt:** đủ **8.072 bước** / 2 lượt duyệt · `adapter_model.safetensors` **59,9 MB**
(bằng S1) · **403 điểm log** = 8.072 ÷ 20, không thiếu đoạn nào · loss 20 điểm cuối **0,2915**.

⚠️ **`total_flos`/bước = 522.198 GF, cao hơn S1 (513.164) đúng 1,76%.** Đúng chiều dự đoán:
đích của S2 có thêm dòng `<desc>` nên chuỗi dài hơn. **Đây là mốc để đối chiếu hạt giống 202** —
hai lượt S1 khớp nhau 0,013%, nếu 202 lệch nhiều hơn thế thì có gì đó khác giữa hai lượt.
⛔ Cấm so `total_flos`/bước của S2 với S1 để kết luận gì về "mất bước" — hai nhánh khác độ dài.

**Lượt này đứt máy 4 lần** (cộng dồn cả dự án ~10 lần, ~13 giờ tường chỉ để dựng lại). Mỗi lần
tốn ~42 phút mã hoá token + ≤200 bước ≈ 34 phút. Ba lỗi **của khâu dựng lại**, không lỗi nào ở
khâu train:

· ⛔ **Ô 2 bung `derived.tar.gz` = bản khai báo TIẾNG VIỆT, đè lên bản tiếng Anh.** Bắt được
nhờ phép ④ của ô 7b: **41.099** khai báo còn tiếng Việt. Nếu bấm train luôn thì bước 4.600 trở
đi học trên dữ liệu khác 4.600 bước đầu — lượt train lai, không dùng được, **log không báo gì**.
Đã vá: ô 2 tự bung đè `derived_train_en.tar.gz` và in xác nhận; trình tự chạy lại thêm ô 7b.
· ⛔ **Ảnh tập kiểm 3,2 GB không có trên máy ảo mới** (ô 2 chỉ bung ảnh dạy) ⇒ khâu sinh câu
chết ngay dòng đầu. Đã thêm ô 11b.
· ⛔ **Trình tự chạy lại sót ô 4 (`HF_TOKEN`)** — máy ảo mới có bộ đệm HF rỗng.

**Ba lỗi của Ô THEO DÕI, tìm được bằng cách dựng log giả cho ba kịch bản** (chạy thường · vừa
chạy tiếp · đang mã hoá token). Đáng ghi vì cả ba đều **không nhìn ra được bằng cách đọc mã**:

| lỗi | hậu quả |
|---|---|
| đọc dòng cuối bằng `max`/`sort` theo bước | điểm lưu đi sau log 180 bước ⇒ sau khi chạy tiếp, tệp còn dòng của phiên cũ **số bước CAO HƠN** chỗ đang chạy. Ô in **4.740 đứng yên ~24 phút**, tốc độ **401,98 s/bước**, giờ xong **04/09** |
| không phân biệt *mã hoá token* với *treo* | suốt 42 phút sau mỗi lần chạy tiếp, ô in số bước của **phiên trước** kèm giờ xong rất hợp lý. Vá bằng mtime của `trainer_log.jsonl`: cũ hơn 5 phút ⇒ không có bước nào chạy |
| lịch `lr` lệch **0,10%** có hệ thống | HF dùng **`ceil`** cho warmup (**404** bước, không phải 403) và ghi `lr` của bước **b−1**. Khớp đúng hai điều đó thì lệch còn **0,013%** ⇒ siết ngưỡng cảnh báo xuống **0,2%** |

Cộng hai chỗ **phân giải quá mịn** làm người đọc tưởng lượt train trồi sụt: `loss` một lô có
biên **0,045** trong 300 bước còn `tb10` chỉ **0,0049** (hẹp hơn 9 lần) ⇒ nhìn `loss` mà kết
luận là đọc nhiễu; và so `tb10` với **200 bước trước** ở đuôi lịch là vô nghĩa vì mức trôi thật
(~0,004) nhỏ ngang nhiễu của chính `tb10` — phải so **1.000 bước**.
⇒ **Mẫu hình cũ lặp lại lần nữa: mọi lỗi nằm ở khâu MÔ TẢ/ĐO, không ở khâu train.**

⭐ **Bước 18175/0 sinh *"Open Tripadvisor app"* thay vì Foursquare — S1 hạt giống 101, S1 hạt
giống 202 và nay S2 hạt giống 101 đều mắc đúng lỗi đó ở đúng bước đó.** Ba lượt train độc lập,
hai nhánh khác nhau ⇒ đây là đặc tính của **màn hình/dữ liệu**, không phải của nhánh. Đọc được
đúng một điều: đường ống chạy đúng và tất định. n=8, **cấm** suy ra gì về chất lượng.

**Khuôn `<desc>` ĐẠT** (mốc dừng quan trọng nhất của lượt này): 20 bước thử → **11 bước có
`<desc>`, 11/11 đúng khuôn bốn phần**, **0** bước còn sót `<desc>` trong câu đem chấm.
⚠️ Tỉ lệ 11/20 **không phải** dấu hiệu hỏng — chỉ bước **chạm** mới có khai báo (4.463/6.958 =
64%). Phép kiểm bản đầu chia cho toàn bộ 20 nên in `11/20 ← cần gần hết`, trông như rớt; đã sửa
mẫu số.

#### Vì sao KHÔNG early stopping — câu hỏi nảy ra lúc theo dõi 19/8, và là câu giám khảo dễ hỏi

Ở đuôi lịch, `tb10` gần như phẳng (5.400 → 6.180 chỉ đi 0,3053 → 0,2988) nên câu hỏi tự nhiên
là *"sao không dừng sớm cho đỡ 5 giờ"*. Bốn lý do, lý do đầu là cứng nhất:

1. **`report/106` đã đăng ký trước và khoá luật chọn điểm lưu**: *dùng bản cuối 2 lượt duyệt
   cho mọi nhánh*, kèm chữ **CẤM chọn theo điểm trên tập kiểm**. Early stopping chính là chọn
   mô hình theo một thước — làm thế là phá niêm phong thiết kế, mà niêm phong đó đang gánh vai
   "không có thầy chốt miệng".
2. **Không có tập validation để dừng theo.** Hai lựa chọn thay thế đều hỏng: dừng theo **loss
   huấn luyện** thì vô nghĩa (nó gần như luôn giảm, kể cả khi đang học vẹt); dừng theo **tập
   kiểm** thì đó là rò rỉ, vì chính tập kiểm dùng để báo executability.
3. **S1 và S2 phải cùng ngân sách huấn luyện thì hiệu `S2 − S1` mới đọc được.** S1 chạy đủ
   8.072 bước; S2 dừng ở 6.200 thì hiệu lẫn cả phần "ít bước hơn" và ablation mất nghĩa.
4. **Loss không phải thước.** Loss của S2 tính trên cả `<desc>` lẫn câu, trong khi chấm chỉ lấy
   **câu sau khi cắt bỏ `<desc>`**. Loss phẳng không kết luận được gì về chất lượng câu.

Và về mặt tiền: muốn biết bản 6.200 có gần bằng bản 8.072 không thì **phải chấm cả hai**, mỗi
lượt 5,6 giờ quota Kaggle (trần 30 giờ/tuần) — đắt hơn 5 giờ Colab định tiết kiệm.

#### ⭐ BƯỚC BỎ CỦA S2 KHÁC S1 — và nó cho thấy một CƠ CHẾ, không phải một ca lẻ

`preds_s2_seed101.jsonl`: 6.958 bản ghi · 4.463 bước chạm · **0** sót `<desc>` trong câu · độ
dài câu trung vị **31** ký tự (S1: 33) · đúng **một** câu rỗng — nhưng ở bước **`(20011, 2)`**,
trong khi **cả hai** hạt giống S1 bỏ `(18710, 1)`.

Ô 14 chỉ **đếm** số câu rỗng nên không lộ ra điều đó; phải hỏi *bước nào* (ô 14b mới thêm).

**`raw` của bước ấy:** `<desc>tappable text | 7 徇␣␣␣␣…` — **U+200A (hair space) lặp tới hết
ngân sách sinh**, kèm một chữ Hán và một ký tự hỏng. Mô hình rơi vào **vòng lặp lặp ký tự ngay
trong phần khai báo**, tiêu sạch token, **không còn chỗ để sinh câu**. Câu chuẩn là
`"Set time 7' o clock in the clock"` — màn đồng hồ, chỗ OCR đọc rác nhất.

⇒ **Chẩn đoán đăng ký trước hôm qua (rác OCR trong khai báo) nay có cơ chế cụ thể**, không còn
là phỏng đoán: rác không chỉ làm khai báo xấu, nó **kích hoạt vòng lặp nuốt ngân sách sinh**.

**Ba hệ quả:**
1. ⚠️ **Kiểu hỏng này S1 về cấu trúc KHÔNG THỂ có** — không có khai báo thì không có chỗ cho
   vòng lặp xảy ra *trước khi* tới câu. Thành phần đóng góp của S2 mang rủi ro riêng ⇒ **phải
   khai như giới hạn của nhánh**, không lấp liếm.
2. ⚠️ **Quần thể ghép cặp S2-vs-S1 = 4.461 bước**, không phải 4.462. Chênh ~0,02 pp nên **không
   đổi kết luận**, nhưng câu *"chấm trên cùng 4.462 bước"* trong `report/112` và bản thảo bài
   báo **phải sửa** khi S2 vào bảng.
3. ⭐ **Mất hẳn câu chỉ là ĐUÔI NẶNG NHẤT.** Cùng cơ chế ở mức nhẹ hơn sẽ **cắt ngắn** câu chứ
   không giết hẳn — và phép đếm câu rỗng **không thấy được**. Đây mới là chỗ có thể ăn mòn điểm
   S2 một cách âm thầm.

⇒ Đã thêm **ô 14c**: khoá định nghĩa *"khai báo có rác"* (dấu cách lạ · CJK · ký tự hỏng · một
ký tự lặp ≥10 lần · khai báo dài >200), đếm tỉ lệ, **so độ dài câu hai nhóm**, rồi ghi danh
sách bước lên Drive kèm md5. **Chạy trước khi chấm** ⇒ phép phân tầng sau này là **đăng ký
trước**, không phải bới số sau khi thấy điểm.

#### 🔒 CHẨN ĐOÁN ĐĂNG KÝ TRƯỚC — ghi 19/8, **trước khi có bất kỳ điểm S2 nào**

Trong 3 khai báo đầu tiên xem tay đã thấy **một ca rác**:
`just below the text “① 舜”` — OCR đọc nhầm biểu tượng thành chữ Hán. Nhiễu này có sẵn trong
nhãn khai báo dựng tự động; mô hình chỉ học lại.

**Nếu S2 − S1 rơi vào vùng TRẮNG**, đây là giả thuyết đầu tiên phải kiểm, và phải kiểm **bằng
số chứ không bằng lời**:
1. Đếm tỉ lệ khai báo sinh ra có **ký tự ngoài ASCII/dấu câu thường** (CJK, ký hiệu lạ) trong
   `preds_s2_*.jsonl` — và cùng phép đếm đó trên **nhãn dạy** `descriptors.jsonl`.
2. Phân tầng executability theo hai nhóm *khai báo sạch* / *khai báo có rác*, ghép cặp với S1
   trên cùng bước.
3. Chỉ khi hai nhóm chênh nhau rõ mới được nói nhiễu nhãn là nguyên nhân.

⚠️ Ghi mục này **trước khi chấm** chính là để nó không trở thành lời bào chữa nghĩ ra sau khi
thấy điểm xấu. Nếu S2 thắng, **cấm** dùng mục này để giải thích hậu kỳ theo chiều ngược lại.

## 5. Bốn lỗi bắt được trong phiên này

1. **Ô theo dõi OCR đếm DÒNG thay vì ẢNH KHÁC NHAU.** 957 dòng trùng làm nó báo 100,5% và
   tự dừng khi còn **thiếu 559 ảnh thật**. `--merge` vẫn chạy trơn, phủ ra 99,1%, và 559
   bước đó sẽ vào huấn luyện với đầu vào thiếu chữ. Chỉ ô 0.9a (thêm 11/8) mới lộ ra.
   → đã sửa điều kiện dừng của ô C.6 sang đếm ảnh khác nhau.
2. **Nhãn in `hộp to hơn nửa màn` trong khi biến đếm là `area_share > 0.25`** (1/4 màn).
   Con số 2,2% đúng, tên gọi sai — loại số dễ bị chép thẳng vào luận văn rồi bị vặn.
   → đã sửa `descriptor_label_build.py:413`.
3. **Tải HuggingFace ẩn danh treo cứng không báo lỗi** (409/800 MB, đứng >5 phút).
   → `C.1` nạp `HF_TOKEN` từ Colab Secrets, `C.3` có `assert` chặn trước khi chạy.
4. **Máy ảo Colab bị thu hồi hai lần**, cả hai đều ở ~90% khâu OCR, ~7-8 giờ sau khi chạy,
   và đều vào lúc không ai ngồi trước máy. Xem mục 6.

## 6. Mất máy ảo — nguyên nhân và cái giá

| | 10/8 (A100, chưa có đồng bộ) | 11/8 (L4, có đồng bộ Drive) |
|---|---|---|
| mất | 31 GB ảnh + **58.000 ảnh đã OCR** + 8 giờ + **42 đơn vị** | **372 ảnh ≈ 3 phút công** |
| khôi phục | làm lại từ đầu | 35 phút tải ảnh + 51 phút OCR nốt |

Khác biệt duy nhất: `ocr.part*.jsonl` được chép lên Drive **mỗi 5 phút** (ô C.4), có nhật
ký để kiểm (ô C.5). Bản đồng bộ đầu tiên nuốt lỗi bằng `2>/dev/null` — đã bỏ, vì Drive
trục trặc thì nó im lặng không chép gì và chỉ lộ ra lúc mất máy.

**Nguyên nhân nghi cao nhất: trình duyệt mất kết nối** (tab ngủ / máy tính ngủ) → Colab thu
hồi máy ảo. Cách chặn: Chrome `Cài đặt → Hiệu năng → Trình tiết kiệm bộ nhớ` cho phép
`colab.research.google.com` luôn hoạt động; Windows `Nguồn & pin` đặt không bao giờ ngủ khi
cắm điện. **Việc này quan trọng gấp bội ở phiên train (11-18 giờ).**

## 7. Đã cất gì lên Drive (phiên 0 KẾT THÚC 11/8)

| tệp trên `MyDrive/thesis/` | cỡ | kiểm bằng `tar tf` |
|---|---|---|
| `derived.tar.gz` | 0,08 GB | 13 mục, đủ 7 đường dẫn (train + test) |
| `derived_train.tar.gz` | 0,08 GB | 11 mục (bản dự phòng, chỉ phần tập dạy) |
| `test_images.tar` | 3,19 GB | **6.959 mục** = 6.958 ảnh + thư mục |
| `train_images_p0..p3.tar` | 29,6 GB | 16.142+16.142+16.142+16.141 = **64.567** |
| `train.jsonl`, `ocr_parts/` | | bản rời, dự phòng |

⚠️ **Không tar 30 GB thành MỘT tệp.** Drive fuse ghi vào đệm cục bộ trước rồi mới đẩy lên,
nên một tệp 30 GB đòi thêm ~30 GB đĩa máy ảo. Thử một lần ngày 11/8 và chết với
`tar: Cannot write: No space left on device` — trong khi Drive còn 5 TB, tức thông báo lỗi
trỏ sai chỗ hoàn toàn. Cắt 4 gói thì đỉnh đệm chỉ ~8 GB, chạy 12 phút là xong.

⚠️ Bốn gói đóng bằng `tar -C images -T danh_sách` nên bên trong là **tên tệp trần**, phải
bung vào thẳng `train_ac/images` — khác `test_images.tar` (bung vào `test_ac`). Ô A.1 đã sửa.

**Vì sao cất ảnh, dù nó không tiết kiệm thời gian:** đọc 30 GB từ Drive chưa chắc nhanh hơn
tải 32 phút từ HuggingFace. Lý do thật là (1) **bỏ điểm chết đơn lẻ** — không cất thì 12 lượt
train đều phụ thuộc kho HF còn sống; (2) **tránh lệch nguồn âm thầm** — ô A.1 lấy bản kê từ
Drive nhưng ảnh từ HF, bên kia sửa dữ liệu thì hai bên lệch nhau mà `thiếu ảnh 0` vẫn đúng.

Sau đó: nạp thêm ~400-600 đơn vị (~$40-60) → đo L4-vs-A100 cho train bằng ô A.3 → train S1
×2 hạt giống → chấm (Kaggle, miễn phí) → **MDE thật** → khoá ngưỡng → mới train S2.
