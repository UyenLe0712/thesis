# Rà từng khẳng định trong bài ngược lại mã và dữ liệu thật (13/8/2026)

> Không đọc report rồi tin. Mở thẳng `.jsonl` và `.py` rồi tính lại.
> Ba lỗi bắt được ghi ở mục 3 — đều là loại "bài đọc trơn tru nhưng mô tả sai hệ thống".

## 1. Tái lập chính xác — khớp tới chữ số cuối

| Khẳng định trong bài | Nguồn kiểm | Kết quả |
|---|---|---|
| Tập kiểm 6.958 bước / 4.463 bước chạm / 1.432 tác vụ | `test_ac/test.jsonl` | **6.958 / 4.463 / 1.432** ✅ (chạm = click 4.446 + long\_press 17) |
| Bước không-chạm 35,9% | như trên | **2.495 = 35,9%** ✅ |
| G = 1.091 · G hiệu dụng 454,3 · 259 app · cụm lớn nhất 58 | tính lại theo luật cụm-đơn | **1.091 · 454,3 · 259 · 58** ✅ |
| 45,0% bước gán được app, 269 app | như trên | **45,0% (3.130) · 269** ✅ |
| 40,7% bước chạm gán được app | như trên | **40,7% (1.815/4.463)** ✅ |
| Cổng A: trung vị 0,7% · p75 8,8% · ĐẠT | `runs/gate_a/gate_A.json` | `median_err` **0,00729** · `p75` **0,0876** · `pass: true` ✅ |
| Dấu hiệu "x giữa màn" 30,7% | như trên | `mid_x_share` **0,30667** ✅ |
| Phân vị p10 0,1 · p25 0,2 · p50 0,7 · p75 9,1 · p90 36,3 | tính lại từ `gate_A_raw.jsonl` | **khớp cả năm** ✅ |
| Các dải sai số n = 188/21/16/12/63 | như trên | **188/21/16/12/63** (tổng 300) ✅ |
| 62,7% số bước ≤3% | như trên | **62,7%** ✅ |
| Trần Voronoi 70,0% KTC [64,5; 75,3] · đĩa 81,3% [76,6; 86,0] | `runs/gate_a/gate_A_ceiling.json` | **0,70 [0,6452; 0,7525]** · **0,8133 [0,7659; 0,8601]** ✅ |
| 239 cụm (hiệu dụng 191,5) · trung vị 72 phần tử · 0 màn thiếu cây | như trên | **239 · 191,49 · 72 · 0** ✅ |
| Mười ngưỡng bơm lỗi | `exec_injection_v3.py:32` | **khớp cả 10** ✅ |
| Tham số huấn luyện 14.966.784 | tính tay | **14.966.784** ✅ |
| Toạ độ trên lưới [0,1000] | `descriptors.jsonl` | **1.074/1.074** trong khoảng ✅ |
| Cổng hình học 25 ca hộp >25% màn | như trên | **25** ✅ |
| Nguồn tên: trợ năng 224 / OCR 599 | như trên | **224 / 599** ✅ |
| Nhãn lát thử: tên rõ 73,8% · không tên 23,4% · trùng tên 7,0% | như trên | **793/1.074 = 73,8%** · **251 = 23,4%** · **7,0%** ✅ |
| Mỏ neo chữ 737 ca | như trên | **737** (738 chuỗi chứa chữ "chữ", chênh 1 do một luật khác) ✅ |
| Bán kính gộp 24dp ≈ 63 px | `metric_exec.min_sep_px` | 24 × 1080/411 = **63,07 px** ✅ |
| Siêu tham số QLoRA | `train_config.yaml` | khớp từng khoá ✅ |

## 2. Không kiểm được tại máy này — số của Colab, giữ nguyên nguồn report

Tập dạy đủ (64.567 / 41.191 / 12.895), phủ OCR 100%, phân bố nhãn ở quy mô đủ,
9 bất biến, rò rỉ = 0, phép ghép n=400, độ dài chuỗi, ghép token của S2r, số đo tốc
độ card. Máy này chỉ có **lát 1.697 bước**; các số trên đo ở phiên Colab
(`report/110`). Không dựng lại được ở đây thì không tự nhận là đã kiểm.

## 3. BA LỖI BẮT ĐƯỢC — đã sửa vào bài

### 3.1. Bảng ví dụ là do tôi bịa, và bịa sai ngôn ngữ *(nặng)*

Bản đầu tôi tự viết một ví dụ toàn tiếng Anh. Mở `descriptors.jsonl` mới thấy nhãn
thật viết **tiếng Việt**, câu đem chấm **tiếng Anh**:

```
desc: <desc>mục | CATEGORIES | <point>127,238</point> | bên trái chữ "MEN"</desc>
target_instruction: click on Categories at the top left corner of the screen
```

`build_branch_data.py:146` ghép `desc + "\n" + câu`. Bài đã mô tả sai thứ đang huấn
luyện. **Đã thay bằng bản ghi thật** (episode 13765) + thêm khai báo scaffold song
ngữ ở mục III-D và mục Giới hạn.

### 3.2. Định nghĩa hình thức của thước KHÔNG khớp mã chấm *(nặng nhất)*

Bài viết thước có **hai** điều kiện, và trình bày đĩa dung sai với Voronoi như hai
lựa chọn đối lập. `metric_exec.score_step:197` thực tế là **hội của ba**:

```python
executable = bool(action_ok and toggle_ok and hv)
def hit_voronoi(...):
    if not hit_disk(pred, gold, wh, tau): return False   # ← vẫn đòi đĩa 14%
```

Ba sai lệch: (a) thiếu hẳn điều kiện **chống đảo nghĩa** — mà mục IV-D lại có nhắc
tới "toggle condition", tức bài viện dẫn một điều kiện chưa bao giờ định nghĩa;
(b) Voronoi **vẫn đòi nằm trong đĩa 14%**, nên nó là **bản siết chặt** của luật quy
ước chứ không phải phương án thay thế; (c) lớp gộp thao tác có **12 động từ** chứ
không phải 4. Đã viết lại mục IV-A đủ ba điều kiện và nói rõ quan hệ bao hàm — chỗ
này còn làm bài **mạnh hơn**: thước không vứt bỏ quy ước của ngành, nó siết quy ước
đó lại.

### 3.3. Lập luận đặt ngưỡng cổng A dùng số của mẫu n=76 *(vừa)*

Bài viết "nút đích 189×126 px, nút khác gần nhất cách 69 px". Đo trên 1.074 bản ghi
thật: hộp trung vị **266×126 px**, khoảng cách hàng xóm trung vị **179 px**. Con số
189×126/69 có thật nhưng đo trên **lát 76 bước** (`report/108` mục 7), không đại
diện. Đã thay bằng phép đo đúng cỡ có sẵn trong bản đăng ký (`report/106` sửa đổi
6/8 (i), **1.496 bước chạm**): biên dung sai trung vị **67 px = 6,2%**, phân vị 10 là
**39 px = 3,6%** ⇒ ngưỡng 3% nằm **dưới phân vị 10**. Kèm lợi ích ngoài dự tính: bán
kính mù 63 px giờ giải thích được bằng chính con số đó (63 px chỉ vừa dưới biên
trung vị 67 px), thay vì bằng một cỡ hộp lấy từ mẫu khác.

## 4. Hai chỗ vặt cũng đã sửa

- Liệt kê bước không-chạm trong bài cộng lại ra 2.493 nhưng tổng ghi 2.495 — **thiếu
  `navigate_home` 2**. Đã thêm.
- Bảng nhánh bỏ sót **S3-pilot** trong khi `report/106` có đăng ký ⇒ thành báo cáo
  chọn lọc. Đã thêm một câu khai là *registered and not run*.


---

## 5. Rà lượt 4 (15/8) — có ĐIỂM SỐ THẬT, tính lại từ tệp thô

Nguồn: `runs/score_s1_seed101.json` + `runs/score_s1_seed101_raw.jsonl` (4.463 dòng).
Không đọc `report/110` rồi chép — mở tệp thô tính lại.

| Khẳng định | Tính lại từ `_raw.jsonl` | |
|---|---|---|
| n chấm được 4.462 (1 bỏ vì câu rỗng) | 4.463 dòng · 1 mang khoá `bo_qua` · **4.462** | ✅ |
| Executability 59,1% | **0,5912** | ✅ |
| KTC95 [57,3 – 60,8] · đĩa 69,2% | json: `[0,5733; 0,6083]` · `exec_disk 0,6917` | ✅ |
| Cụm 1.091 · hiệu dụng 454,3 | json: `1091` · `454,33` — **khớp con số tính ngày 9/8, trước khi có mô hình** | ✅ |
| Đúng loại thao tác 94,4% | **94,37%** | ✅ |
| Lát app: 59,1 / 59,0 / 59,2 | **59,1%** (n=1.737) · **59,0%** (n=78) · **59,2%** (n=2.647) | ✅ |
| Trượt 1.824 · sai thao tác 251 · còn lại 1.573 = 86% | **1.824 · 251 · 1.573 (86%)** | ✅ |
| Thiên vị câu dài 5,4 pp tại trung vị 33 ký tự | trung vị **33** · ≤33: **56,5%** (n=2.293) · >33: **61,9%** (n=2.169) · chênh **5,4** | ✅ |
| App đã thấy 95,6% phần gán được | `test.jsonl`: True 2.991 · False 139 → **95,6%** | ✅ |

Thêm hai số tự đo, không có trong report: `toggle_ok` **99,91%** (luật chống đảo nghĩa
gần như không bao giờ kích hoạt trên đầu ra thật) và `hit_disk` **69,2%** khớp json.

**Đã đưa vào bài:** mục VII đổi từ *"Status of the Ablation Study"* (bảng rỗng) thành
**"First Measurement"** với Bảng VI (S1 = 59,1%, các nhánh còn lại `—`) và Bảng VII
(lát cắt chẩn đoán). Ba phát hiện vào thân bài; phần room 485 bước vào cùng mục.
Tóm tắt và Kết luận cập nhật theo. Mục III-B đổi từ *"lợi thế sân nhà là giới hạn"*
sang *"giới hạn kèm số bác bỏ 0,1–0,2 pp"*. Mục IV-F thêm phép ghép cặp McNemar.

**Vẫn CHƯA có trong bài, đúng theo luật đã đăng ký:** so sánh S1-vs-S2 · MDE thật ·
mốc Base (đang chấm) · cỡ nhiễu hạt giống.
