# Ô thăm dò chọn máy — chạy TRƯỚC mọi lượt GPU (viết 5/9/2026)

> Luật: `CLAUDE.md` §Nguyên tắc chi tiền. **Probe trên card RẺ trước.** A100 chỉ được dùng khi
> có số đo biện minh, và số đó phải ghi lại vào runbook của lượt.
> Giá mỗi giờ **tra tại thời điểm quyết**, cấm nhớ (Colab → Runtime → Change runtime type hiển
> thị đơn vị/giờ của từng card).

## Bước 0 — khâu này có thật sự dùng GPU không

Chạy khâu đó vài phút trên runtime **CPU** (hoặc runtime GPU rồi xem `nvidia-smi`). GPU đứng
0% / 0 GB suốt thì đây là khâu bám CPU–IO ⇒ **dùng CPU, 0 đơn vị**. Tiền lệ: phiên 0 dựng dữ
liệu + OCR chạy trọn trên CPU, GPU 0,0/40 GB, tiết kiệm 43 đơn vị.

⭐ **Phân loại chỗ nghẽn — quyết định trước cả việc đo:**
· nghẽn **CPU/IO** (dựng dữ liệu, OCR, mã hoá token, ghép ảnh): L4 **ngang** A100, vì card nằm
  không. Đo 11/8: cùng 12 lõi, L4 rẻ hơn 3,6 lần cho **cùng** thời gian ⇒ chọn L4 hoặc CPU.
· nghẽn **GPU compute** (train, sinh mẫu): phải đo, không suy. Đo 11/8 cho train SFT: L4
  31,26 s/bước vs A100 10,70.

## Ô M1 — đo trên card RẺ trước (L4), 10–15 phút

Chạy đúng cấu hình thật, chỉ hạ số bước, **trên mẫu nặng nhất của nhánh nặng nhất** (không
phải mẫu đầu tập — luật P10: L4 chạy ngọt mẫu thường rồi tràn ở 200 mẫu dài nhất).

```python
import torch, time, json
torch.cuda.reset_peak_memory_stats()
t0 = time.time()
# ... chạy 20 bước thật ở đây (cùng cfg, cùng cỡ lô, cùng cutoff, dữ liệu SẮP GIẢM theo độ dài) ...
dt = (time.time() - t0) / 20
print(f"s/bước       {dt:.2f}")
print(f"đỉnh cấp phát {torch.cuda.max_memory_allocated()/2**30:.2f} GB   ← số quyết định")
print(f"đỉnh dành sẵn {torch.cuda.max_memory_reserved()/2**30:.2f} GB")
print(torch.cuda.get_device_name(0), torch.cuda.get_device_properties(0).total_memory/2**30)
```

⚠️ Đọc `max_memory_allocated`, **không** đọc `nvidia-smi` — `nvidia-smi` tính cả bộ đệm của
allocator nên cao hơn mức cấp phát thật, dễ loại oan card rẻ.

**Luật đọc:**
· đỉnh cấp phát **≤ 17 GB** ⇒ L4 (22 GB dùng được) còn biên ≥ 25% ⇒ đi tiếp ô M2.
· tràn bộ nhớ ⇒ thử hạ `per_device` và bù bằng accum **một lần** trước khi bỏ card rẻ; vẫn tràn
  thì lên A100, ghi lại con số đã tràn.

## Ô M2 — quy ra ĐƠN VỊ MỖI LƯỢT rồi mới chọn

```python
GIA = {"L4": ..., "A100": ...}      # đơn vị/giờ, TRA tại thời điểm quyết
SB  = {"L4": ..., "A100": ...}      # s/bước đo được ở ô M1
BUOC = ...                          # số bước của lượt thật
for k in SB:
    gio = SB[k] * BUOC / 3600
    print(f"{k:5s} {gio:6.1f} giờ · {gio*GIA[k]:6.1f} đơn vị · {gio/12:.1f} phiên Colab 12 h")
```

**Luật chọn (user chốt 5/9/2026), đọc theo TỈ SỐ THỜI GIAN `giờ_L4 / giờ_A100`:**

| tỉ số | chọn | ghi chú |
|---|---|---|
| **≤ ~1,4×** (A100 5 h thì L4 6–7 h) | **L4** | user nói thẳng mức này *"okay"*. Ở đây L4 rẻ hơn khoảng **2,5 lần tổng tiền**, chậm thêm 1–2 giờ. |
| **> ~1,4×** | **A100** | *"lâu hơn thì dùng A100 được rồi"*. Train SFT rơi vào ô này (2,92×) nên quyết định A100 của 11/8 vẫn đúng luật mới. |

Tỉ số 1,4× là mốc mềm, đọc kèm hai điều: lượt vượt **12 giờ** phải cắt thành nhiều phiên Colab
(mỗi mối nối là một lần rủi ro mất bước), và tiền vẫn phải in ra bảng để user thấy.

Ví dụ đã đo (train SFT, 11/8): 8 lượt = **856 đơn vị trên L4** vs **858 trên A100** ⇒ ngang tiền,
A100 nhanh 3,4× thời gian tường ⇒ chọn A100 **có biện minh bằng số**. Nếu chênh lệch đơn vị lớn
hơn thì kết luận đảo chiều.

## Sau khi chọn

Ghi vào runbook của lượt: tên card · s/bước · đỉnh cấp phát · đơn vị ước tính. ⛔ **Không đổi
card giữa lượt đang chạy** — mất tiến độ về điểm lưu gần nhất cộng thời gian bung lại dữ liệu.

## Mốc đã đo: sinh câu test trên Colab T4 vs L4 (22/11/2026, lượt DPO trực tuyến ck500)

Việc: sinh 4.463 câu test + chấm exec, Qwen2.5-VL-3B (S1 hoà + adapter), một luồng, notebook
`_bundles/luoi/k_luoi-test-c-dpo/` (dựng bằng `make_test_nb2.py` + `colab_tu_kaggle.py`).

**Giá** [đo, đọc khi tạo máy bằng Colab CLI 22/11; giá đổi theo thời điểm, quyết lần sau phải tra lại]:

| card | VRAM | unit/giờ | ghi chú |
|---|---|---|---|
| T4 | 15 GB | **1,15** | lên máy ngay |
| L4 | 22,5 GB | **1,94** (gấp 1,69× T4) | tạo phiên timeout 3 lần liền (POST /tun/m/assign treo, không phải lỗi đăng nhập) |

**Tốc độ sinh câu** (s/bước, cùng mã sinh):

| máy | s/bước | nguồn |
|---|---|---|
| Kaggle T4 | 2,78 | các lượt test Kaggle (`luoi-test-u-*`) [đo] |
| Colab T4 | 2,31 lúc đầu → ~2,6 sau 250 bước | log `gen_dpo_on_spice_101.log` [đo] |
| Colab L4 | **chưa đo** | |

⇒ Một lượt test trên Colab T4 ≈ 3,2 h sinh + 20–30 phút chấm ≈ **4–4,5 unit** [ước từ số đo].

**Vì sao chọn T4 cho sinh câu** [suy, chưa đo L4]:
- L4 chỉ rẻ hơn mỗi lượt nếu nhanh hơn T4 ≥ 1,69× (xong dưới ~2,1–2,3 h).
- Sinh từng token ở lô nhỏ bị giới hạn bởi băng thông bộ nhớ: L4 ~300 GB/s, T4 ~320 GB/s ⇒ phần giải mã
  gần như không nhanh hơn; L4 chỉ nhanh hơn rõ ở phần xử lý ảnh đầu vào (tính toán). Ước cả lượt 1,2–1,5×.
- VRAM 22,5 GB của L4 không đủ để notebook chạy hai luồng song song (cần > 30 GB, tức A100).
- L4 đáng dùng khi: train cần > 15 GB VRAM, hoặc cần số gấp và chấp nhận trả thêm.
- Muốn chắc: chạy 10 phút trên L4 (~0,3 unit), đọc s/bước trong `gen_*.log`, điền vào bảng trên.

**Khác biệt Colab vs Kaggle cần khai:** kiểm bộ chấm trên Colab T4 ra 9/10 bước trùng toạ độ (Kaggle thường
10/10); vẫn qua ngưỡng ≥ 9. Kiểm hoà 16/20 như Kaggle.
