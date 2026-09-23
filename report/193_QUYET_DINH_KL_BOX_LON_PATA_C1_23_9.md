# 193 — Quyết định KL cho box lớn trong PATA-C1 (23/9/2026)

> Chép từ 5 ảnh chụp máy Mac, nhận 23/9 tối; ảnh gốc `report/anh_193_kl_box_lon_23_9/01…05_*.jpg`.
> Số hiệu 193 giữ theo kho Mac (các file 187–192 của kho đó chưa có trên WSL).
> **Thắng `186` §4b** về ngưỡng và về cách đọc số audit. Phần *Thi hành trên WSL* ở cuối là của
> phiên chép.

## Kết luận ngắn

Có thể và nên tắt KL theo từng mẫu, nhưng nên đặt ngưỡng `area_share >= 0.50`, không phải `>= 0.25`.

Luật đề xuất:

```
kl_ok = có box
        ∧ điểm chạm hợp lệ trong ảnh
        ∧ area_share < 0.50
```

- Không tắt KL toàn bộ.
- Không bỏ mẫu khỏi học câu.
- Stage H bỏ các mẫu không `kl_ok` vì chặng này chỉ học định vị.
- Stage J vẫn giữ CE cho mọi touch step; chỉ mask KL trên box quá lớn.
- Áp cùng eligibility rule cho train, val400 và val600.
- Khoá luật này trước train dài và trước xem `exec`.

## Vì sao ngưỡng 0.50 hợp lý hơn 0.25

### 1. Với box ≥ 0.50, KL gần như không còn là supervision định vị

Số đã đo:
- 657/40.089 mẫu train có box ≥ 0.50: **1,64%**.
- Box nhóm này phủ trung bình **1.096,3/1.272 patch = 86% màn hình**.
- Center prior không nhìn ảnh đã đặt **0,936 mass** vào box.
- Train-location prior không nhìn ảnh đã đặt **0,870 mass** vào box.

Đích KL là phân bố đều trên mọi patch giao box. Với box phủ 86% màn hình, tối ưu `KL(p || alpha)` buộc
attention trải gần khắp ảnh. Khi bridge tính `z = Σ alpha_i v_i`, kết quả gần với trung bình toàn màn
hình, không còn đại diện rõ cho phần tử đích. Đây không chỉ là tín hiệu yếu; nó còn đi ngược 98,36% mẫu
còn lại vốn dạy attention tập trung.

### 2. Audit ủng hộ loại nhóm ≥ 0.50, dù không cho phép ước lượng tỷ lệ lỗi quần thể

Trong mẫu chẩn đoán lấy dư:
- `area_share >= 0.25`: 10/18 lỗi nặng;
- `area_share >= 0.40`: 10/17 lỗi nặng;
- `area_share >= 0.50`: 10/17 lỗi nặng;
- mọi lỗi stale quan sát được đều nằm ở nhóm ≥ 0.50.

Không được dùng 10/17 hay 10/18 làm tỷ lệ lỗi quần thể vì mẫu cố ý oversample container lớn. Tuy nhiên,
dùng chúng để xác định dạng lỗi tập trung ở đâu là hợp lệ.

Quan trọng hơn: hạ ngưỡng từ 0.50 xuống 0.25 không loại thêm lỗi nặng nào trong mẫu audit, nhưng lại bỏ
KL của thêm 226 mẫu. Theo dữ liệu hiện có, 0.50 chi phối 0.25: loại cùng số lỗi đã quan sát nhưng giữ
nhiều supervision hơn.

### 3. Ngưỡng 0.25 vẫn loại các box còn mang thông tin

Nhóm 0.25–0.50 có 226 mẫu, được báo cáo khoảng:
- trung bình 465/1.272 patch dương, khoảng 36,6% màn hình;
- center-prior mass khoảng 0,454;
- train-location-prior mass khoảng 0,351.

Đây là target rộng nhưng chưa vô nghĩa: nó vẫn loại được hơn nửa tới gần hai phần ba màn hình. Không đủ
bằng chứng để mask cả nhóm này trước khi có người gán thứ hai hoặc đánh giá riêng tốt hơn.

## Đính chính kết luận trước

Các file 186 và 187 khuyến nghị tắt KL ở `area_share >= 0.25`. Khuyến nghị đó quá mạnh.

Sai ở hai điểm:
1. `10/18` đến từ mẫu pooled/oversampled, không phải ước lượng tỷ lệ lỗi quần thể. Không được nhân nó
   với 883 mẫu để suy ra 300–650 nhãn sai.
2. Chính bảng độ nhạy cho thấy các ngưỡng 0.25, 0.40 và 0.50 bắt được cùng 10 lỗi quan sát, trong khi
   0.25 bỏ thêm 226 mẫu. Vì vậy câu "ba ngưỡng gần như cùng kết quả nên chọn 0.25" không theo sau từ dữ
   liệu; nếu kết quả audit bằng nhau thì phải ưu tiên ngưỡng bảo thủ hơn là 0.50.

Phần đúng của 186/187 vẫn giữ:
- box rất lớn có target KL ít thông tin;
- lỗi chẩn đoán tập trung ở box lớn;
- CE phải giữ;
- luật phải áp đồng nhất train/validation;
- quyết định phải được khai là post-audit data-quality rule.

## Vì sao không giữ toàn bộ box

Giữ toàn bộ vẫn không vi phạm cổng audit 5%, vì tầng U đo được 4/148 = 2,7% và ngưỡng khoá trước chỉ
yêu cầu sửa labeler nếu điểm ước lượng vượt 5%.

Tuy nhiên cổng này trả lời "proxy box có dùng được nói chung không", chứ không trả lời "mỗi proxy box có
tạo ra target KL hữu ích không". Box phủ 86% màn hình có thể đúng về mặt phần tử nhưng vẫn là target
định vị kém. Vì vậy mask nhóm ≥ 0.50 là data-quality rule hợp lý ngay cả khi không dựa vào tỷ lệ lỗi
audit.

## Vì sao không dùng weighting liên tục lúc này

Có thể thay mask cứng bằng trọng số theo entropy/diện tích, nhưng đó là một thay đổi phương pháp mới,
cần chọn hàm trọng số và tuning. Trước một lượt train dài, hard mask 1,64% mẫu là phương án đơn giản, dễ
audit và ít bậc tự do hơn.

## Cách khai trong báo cáo sau này

Đoạn tiếng Anh có thể dùng:

> We retained every touch step for sentence supervision. We disabled the patch-level KL term when the
> proxy box covered at least half of the screen (1.64% of boxed training steps), because such targets
> covered 86% of visual patches on average and were also the region in which the diagnostic audit
> concentrated stale or wrong-container boxes. This eligibility rule was fixed after the label audit and
> before model training or inspection of execution scores, and was applied unchanged to training and
> development diagnostics.

Không được viết:
- "55,6% box lớn trong quần thể bị sai";
- "ước tính 300–650 nhãn sai";
- "ngưỡng 0.50 được paper chứng minh";
- "audit độc lập hai người" khi hiện mới có một người gán.

## Người dùng đã chấp thuận (23/9, chat này)

Ngưỡng **0.50 đã chốt**. Chat nhận file này phải sửa mã và dựng lại dữ liệu, không hỏi lại 0.25 vs 0.50
vs giữ toàn bộ. Không chạy `git`/`gh` (trừ `git clone` nếu người dùng yêu cầu). Không ghi vào
`thesis-master/` trừ khi người dùng nói rõ; mặc định sửa `harness/pata_data.py` trong clone đang dùng,
rồi báo đường dẫn.

## Việc chat kia phải làm

1. **Sửa `harness/pata_data.py`** — thêm `AREA_KL_MAX = 0.50` dưới `N_PROBE = 40`; trong `build()`
   tính `area`, `kl_ok = box is not None and not (area is not None and area >= AREA_KL_MAX)`, đếm
   `st["box_ge_050"]`; `box` giữ trong record kể cả khi KL tắt; `co_box` vẫn đếm mọi box hợp lệ. Dòng in
   ở `main()` thêm cột mask. Cập nhật docstring.
2. **Probe 40 — không được bốc lại.** Giữ nguyên `pata/probe40.jsonl`; khi tệp khoá đã tồn tại thì bỏ
   sample, giữ tệp, tiếp tục ghi hash ba split. Không sửa nội dung 40 dòng probe.
3. **Dựng lại dữ liệu** — `python harness/pata_data.py`. Số phải in ra:

   | tập | chạm | có box | box ≥ 0.50 (tắt KL) | kl_ok sau sửa |
   |---|---|---|---|---|
   | train_proper | 40.189 | 40.089 | 657 (1,64%) | 39.432 |
   | val400 | 400 | 400 | 4 (1,0%) nếu 186 đúng | 396 |
   | val600 | 602 | 601 | 19 (3,2%) nếu 186 đúng | ~582 |

   Cột val là số 186 đo cho ≥ 0.25. Chat kia đo lại với ≥ 0.50 và ghi số thật vào log; không bịa 4 và
   19 cho ngưỡng 0.50.
4. **Không cần sửa `pata_eval.py` / `pata_train.py`** nếu chúng đã lọc `kl_ok`.
5. **Bundle và train** — dựng lại `thesis_pata_kaggle.zip` và `thesis_pata_colab.zip` sau jsonl mới.
   Không train dài bằng bundle cũ. 13/13 test 3B và smoke vẫn bắt buộc trước A100.
6. **Manifest** (khi seal, chưa bịa checkpoint) — ghi `kl_ok = có box ∧ điểm trong ảnh ∧ area_share <
   0.50`; quyết định 23/9 sau audit, trước train/`exec`; áp train + val400 + val600; số `box_ge_050` từng
   split lấy từ lệnh mục 3.

## Cấm

- Tắt KL toàn bộ, hoặc mask CE.
- Ngưỡng 0.25.
- Nhân `10/18 × 883` thành "300–650 nhãn sai".
- Đổi probe 40.
- `git commit` / `git push` trừ khi người dùng yêu cầu.

## Việc chat kia không làm hộ

- Người gán thứ hai (60 mẫu overlap): không chặn sửa `kl_ok`; vẫn là hạn chế khi viết luận văn.
- Train Stage S/H/J trả phí.

---

## Thi hành trên WSL (23/9 tối) — [đo]

`python harness/pata_data.py` sau khi sửa:

| tập | chạm | có box | box ≥ 0.50 (tắt KL) | kl_ok | SHA-256 (16 đầu) |
|---|---|---|---|---|---|
| train_proper | 40.189 | 40.089 | **657** | **39.432** | `05d69b55c30ef4a6` |
| val400 | 400 | 400 | **2** | **398** | `1ea4c587ebb12663` |
| val600 | 602 | 601 | **14** | **587** | `2d7dfba02909ce83` |
| probe40 | — | — | 0 | 40 | `6c23c1898d85a0fd` (**không đổi**, in "đã khoá — giữ nguyên tệp") |

- Nhóm 0,25–0,50 (226 bước) vẫn `kl_ok = True` [đo].
- **Chỗ `193` chưa nêu nhưng bắt buộc:** `pata_model.make_item` trước đây dựng đích KL theo trường
  `box` chứ không theo `kl_ok` ⇒ chỉ đổi `kl_ok` thì box lớn **vẫn bị học KL**. Đã sửa: đích KL chỉ dựng
  khi `box` có **và** `kl_ok`; kiểm trên một bước box ≥ 0,50 ⇒ `ptarget = None` [đo].
- `pata_audit.py` chuyển sang chọn mẫu theo `box` (không theo `kl_ok`) để mẫu audit cũ tái lập đúng:
  150 mẫu tầng U dựng lại trùng tuyệt đối manifest cũ [đo].
- 13/13 unit test (tí hon, CPU) vẫn đạt. Hai gói zip đã dựng lại.
- Việc commit/push trên WSL do user yêu cầu trong chat WSL (khác với chat Mac).
