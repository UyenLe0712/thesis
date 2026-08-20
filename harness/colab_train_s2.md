# Train S2 trên Colab — từng bước

**S2 là trụ đóng góp của luận văn.** Đích huấn luyện = khai báo phần tử **rồi mới tới câu**;
lúc chấm cắt bỏ phần khai báo, chỉ lấy câu. Nếu điểm tăng thì không phải vì nó được cho thêm
thông tin lúc chấm, mà vì **hành vi lúc suy luận đã đổi** — đó là điều kiện để gọi đây là đóng
góp *mô hình*, không phải đóng góp *dữ liệu*.

> ✅ **Điều kiện tiên quyết đã đủ.** Trình tự cứng (`report/106` mục 5): S1 ×2 hạt giống → chấm
> → MDE thật → **khoá ngưỡng** → mới train S2. Ngưỡng khoá ở **2,8 pp**, mục sửa đổi (w) ghi
> 17/8 **trước** khi chấm nhánh xử lý nào. Không còn gì chặn.

| | |
|---|---|
| máy | **A100** (L4 chậm 2,9× — xem mốc dừng 4) |
| một lượt | ~**26 giờ** tường · ~126 đơn vị |
| **hai hạt giống** | ~52 giờ · ~**252 đơn vị ≈ $25** |
| lịch | khởi động 18/8 ⇒ xong **~21-22/8** nếu suôn; lịch sử 8 lần mất máy nên tính **3 ngày** |

⚠️ **Kiểm số dư đơn vị Colab TRƯỚC khi bấm chạy.** Hết đơn vị giữa lượt train 26 giờ là mất
phần chưa lưu, và phải chờ mua rồi dựng lại từ điểm lưu.

---

## Toàn bộ khác biệt so với lượt S1: HAI giá trị

Trong ô **A.2** của `harness/run_on_colab.md`:

```python
BRANCH, SEED = "s2", 101        # lượt S1 là ("s1", 101)
```

**Không đụng gì khác.** Cấu hình còn lại phải giống hệt, và ô A.2b sẽ kiểm điều đó.

---

## Trình tự ô, chạy đúng thứ tự này

Tất cả đã chạy thật trong chiến dịch S1, qua 8 lần mất máy. Mở
`harness/run_on_colab.md` và chạy:

| # | ô | làm gì | mốc phải thấy |
|---|---|---|---|
| 1 | `0.3` | cài gói **+ liger-kernel** | rồi **Restart runtime** |
| 2 | `A.1` | bung dữ liệu từ Drive | đủ ảnh dạy |
| 3 | `A.1b` | **kiểm gói mã** | `infer 27.443` ✔ · `score` xem ghi chú dưới |
| 4 | — | đặt `HF_TOKEN` | |
| 5 | `A.2` | sinh cấu hình — **đổi `BRANCH="s2"`** | cỡ lô **16** · `BÊN TRONG output_dir: []` |
| 6 | — | vá `preprocessing_num_workers: 8` vào `/content/cfg.yaml` | mã hoá token 42 phút thay vì 2,5 giờ |
| 7 | 🛑 `A.2b` | **KIỂM VÀNG** so cfg với lượt S1 | **chỉ được khác `seed`, `output_dir`, `dataset`** |
| 8 | `A.4` | train, chạy **nền** | |
| 9 | `A.4b` | **đồng bộ log lên Drive mỗi 5 phút** | |
| 10 | `A.5` | theo dõi | chạy lại nhiều lần |

**Bỏ `A.3b`, `A.3d`, `A.3i`** — đo tốc độ và thử nối tiếp đã xong ở chiến dịch S1.

### ⛔ NHƯNG KHÔNG ĐƯỢC BỎ THĂM DÒ BỘ NHỚ — S2 là nhánh NẶNG NHẤT

Bản đầu của runbook này ghi *"bỏ A.3"*. **Sai, và đây là chỗ nguy hiểm nhất.**

Chính `run_on_colab.md` đặt luật: *"Mọi cấu hình đụng tới bộ nhớ đều phải thử lại trên **nhánh
nặng nhất (s2)** với các mẫu dài nhất."* Lý do có luật đó: cấu hình **P10** chạy ngọt trên mẫu
thường rồi **tràn bộ nhớ trên 200 mẫu dài nhất của s2**, và loại hỏng ấy là loại tệ nhất —
chạy trơn vài giờ rồi chết lúc vô tình gặp một lô mẫu dài, giữa đêm.

Cấu hình đang chọn là **P9**, và nó **được chọn dựa trên các lượt đo chạy trên `gui_s1`**.
P9 = P0 + liger, mà P0 giữ gradient checkpointing nên **về lý là tiết kiệm hơn P10** — nhưng
"về lý" không phải "đã đo", và giá của việc sai là **tràn bộ nhớ sau 42 phút mã hoá token**,
mất chỗ trong hàng đợi A100 rồi phải làm lại.

**Chạy thăm dò 12 phút trước khi cam kết 26 giờ.** Dữ liệu đã có sẵn: ô A.3g của chiến dịch
S1 đã dựng `s2_long.json` (200 mẫu dài nhất) + khoá `gui_s2_long`, và cả hai được sao lưu ở
`{D}/branches_backup/`. Nếu `branches/` trên máy ảo mới thiếu chúng thì chép lại từ đó.

```python
# sau ô A.2 (đã đặt BRANCH="s2"), TRƯỚC ô A.4
import yaml, subprocess, os
c = yaml.safe_load(open("/content/cfg.yaml", encoding="utf-8"))
c.update({"dataset": "gui_s2_long", "max_steps": 20,
          "output_dir": "/content/probe_s2long", "preprocessing_num_workers": 8})
yaml.safe_dump(c, open("/content/cfg_probe.yaml","w",encoding="utf-8"),
               allow_unicode=True, sort_keys=False)
print(subprocess.run(["llamafactory-cli","train","/content/cfg_probe.yaml"],
                     capture_output=True, text=True).stdout[-2500:])
```

| thấy gì | làm gì |
|---|---|
| chạy đủ 20 bước, in `total_flos` | ✅ P9 vừa bộ nhớ trên nhánh nặng nhất — sang A.4 |
| `CUDA out of memory` | ⛔ **DỪNG.** Hạ `per_device_train_batch_size` 4→2 **và** nâng `gradient_accumulation_steps` 4→8 để giữ cỡ lô hiệu dụng **16**, rồi thăm dò lại. Đổi cỡ lô hiệu dụng là đổi thí nghiệm, phải ghi mục sửa đổi `report/106` |

⚠️ Nhớ **xoá `max_steps` và `dataset: gui_s2_long`** khỏi `cfg.yaml` thật trước khi chạy A.4 —
ô A.2 có sẵn dòng quét khoá thăm dò, chạy lại A.2 là sạch.

### ⚠️ Ô A.1b sẽ báo lệch ở `score_run.py` — và đó là bình thường

A.1b chờ `score 34.610`. Số hiện tại ở máy nhà là **39.763 B** (`score_run.py` được vá 16/8:
thêm lớp UI-Venus, sửa docstring sai về bộ trỏ, thêm cờ `strict_back`). Gói
`thesis_rented.zip` trên Drive là bản **14/8** nên còn bản cũ.

**Không chặn lượt train này**, vì khâu train dùng LLaMA-Factory và khâu sinh câu dùng
`infer_branch.py` — tệp này **không đổi**, vẫn đúng **27.443 B**. `score_run.py` chỉ dùng lúc
chấm, mà chấm chạy trên Kaggle bằng gói `thesis_score.zip` mới.

⇒ Thấy `score` khác 34.610 thì **đọc kỹ xem `infer` có đúng 27.443 không**. Đúng thì đi tiếp.

### Ô A.2b là ô đáng giá nhất

`A.2b` so từng khoá cfg lượt này với cfg lượt S1 đã lưu trên Drive. **Chỉ ba khoá được phép
khác** — `seed` · `output_dir` · `dataset`. Khoá thứ tư khác là **dừng hẳn**, vì lúc đó S2 và
S1 không còn so được với nhau và cả phép ablation mất nghĩa.

Lượt S1/202 chạy ô này ba lần trong ngày, lần nào cũng **38/38 khoá**.

⚠️ Lần này sẽ khác **ba** khoá thay vì hai (thêm `dataset`: `gui_s1` → `gui_s2`). Đó là khác
biệt **cố ý và duy nhất** của thí nghiệm.

---

## Chống mất máy — ba lớp, đều đã chạy thật

**Điểm lưu ghi thẳng Drive.** Ô A.2 đặt `output_dir = {D}/ckpt/s2_seed101`, tức **trên Drive**
chứ không phải `/content`. Mất máy ảo thì điểm lưu còn nguyên.

**Log đồng bộ mỗi 5 phút** (ô A.4b), có `sync.err` giữ lỗi — bản phiên 0 từng nuốt lỗi bằng
`2>/dev/null`.

**Nối tiếp tự động.** LLaMA-Factory tự dò điểm lưu gần nhất **khi `resume_from_checkpoint` để
trống**. ⛔ **Đừng điền gì vào khoá đó**, kể cả `"auto"` — điền là tắt đúng cái nó định bật.

**Phiên đứt thì chạy lại:** `0.3 → Restart → A.1 → A.1b → A.1c → A.2 → A.4 → A.4b → A.5`.
Ô A.2 phải in `BÊN TRONG output_dir` **CÓ `checkpoint-*`**. Phần train đã làm **không mất**;
giá một lần đứt là ~42 phút mã hoá token, không phải cả lượt.

---

## Theo dõi: bốn dấu hiệu, đều đã học bằng cách mắc lỗi

**Đọc DÒNG CUỐI của `trainer_log.jsonl`, đừng lọc theo ngưỡng bước.** Tệp ghi nối thêm, nên sau
khi chạy tiếp, dòng mới đầu tiên có số bước **thấp hơn** dòng cuối cũ. Đặt `MOC` sai thì ô theo
dõi câm 35 phút hoặc in lại dòng cũ trông y như đang chạy.
💡 **Số bước TỤT XUỐNG là dấu hiệu tốt** — nó nghĩa là phiên mới đã ghi thật.

**`MOC` lấy theo dòng log cuối, KHÔNG theo số điểm lưu.** `logging_steps: 20` mà
`save_steps: 200` ⇒ log luôn chạy trước điểm lưu tới 180 bước. Ô A.1c tự chốt vào
`/content/MOC.txt`.

**Chữ `disconnect` trên trình duyệt KHÔNG phải bằng chứng máy chết.** Bằng chứng thật:
`st_mtime` của `/content/train_s2_seed101.log` cách hiện tại dưới ~120 giây.

**`grep "Resuming training from"` trống ngay sau A.4 là BÁO ĐỘNG GIẢ** — dòng đó in sau ~40
giây nạp thư viện. Hỏi ba thứ trước khi giết tiến trình: `getsize(log)` · `ps -p <PID>` ·
`tail -30`.

---

## Mốc thời gian dự kiến

| | |
|---|---|
| mã hoá token | ~42 phút (có `preprocessing_num_workers: 8`) |
| train | 8.072 bước × ~10,4 s = **23,3 giờ** |
| ghi điểm lưu cuối | ~25 phút |
| **một lượt** | **~26 giờ** |

Mốc ngó giữa chừng: **bước 4.036** = ranh giới lượt duyệt 2. Loss tụt một nấc ở đó là **bình
thường** (gặp lại dữ liệu lần hai). ⚠️ Đừng đọc nhịp tụt đó thành "khái quát tốt hơn", và
**đừng ngoại suy loss** — dự báo sàn 0,548 hôm 12/8 đã bị rút vì mới bước 5.100 đã xuống 0,465.

---

## Xong lượt 101 thì làm gì

1. `A.6` **bỏ qua** — tự kiểm lô chỉ chạy một lần cho cả chiến dịch, đã xong ở S1.
2. `A.7` xem 20 câu sinh thử. **Đây là chỗ nhìn `<desc>` có ra đúng khuôn không** — nếu khai
   báo lệch định dạng thì khâu cắt bỏ nó lúc chấm sẽ hỏng.
3. `A.8` sinh đủ 6.958 câu (~1,5 giờ).
4. `A.9` kiểm tệp dự đoán. Rồi ở máy nhà: `python3 harness/kiem_preds.py runs/preds_s2_seed101.jsonl`
   — phải **8/8 ĐẠT**, và bước bỏ phải **trùng khít** `[(18710, 1)]` như S1.
5. `A.10` lưu vết lên Drive **trước khi tắt máy**.
6. Đổi `SEED = 202`, chạy lại từ ô A.2.

**Chấm để cuối cùng**, sau khi có cả hai hạt giống — Kaggle 30 giờ/tuần, mỗi lượt 5,6 giờ.

---

## Luật đọc kết quả — đã khoá, đừng sửa sau

`report/106` mục sửa đổi (w). Δ = S2 − S1, trung bình hai hạt giống, ghép cặp:

| Δ | kết luận |
|---|---|
| **≥ +2,8 pp** và KTC95 loại trừ 0 | **DƯƠNG** — thành phần có tác dụng |
| +1,7 … +2,8 pp, KTC loại trừ 0 | **DƯƠNG YẾU** — không đưa vào abstract |
| −2,8 … +1,7 pp | **TRẮNG** — kết quả âm có kiểm soát |
| ≤ −2,8 pp | **ÂM** — báo thẳng |

Bắt buộc báo kèm: **bốn con số riêng lẻ** (không chỉ trung bình) · **tỉ lệ bước bất đồng**
(mốc: null 6,4% · can thiệp thật 24%) · **phân tầng theo độ dài câu**. Và nếu hai hạt giống S2
lệch nhau **> 1,5 pp** thì **dừng lại truy nguyên nhân** trước khi đọc Δ.
