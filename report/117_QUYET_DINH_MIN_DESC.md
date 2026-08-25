# 117 — QUYẾT ĐỊNH 23/8/2026: đóng góp mô hình là **MIN-DESC**

> **Đọc file này trước khi đụng vào bất cứ việc train nào.** Nó thay phần *"sẽ train gì"* của
> `report/116` (bản chép lại phiên debate 23/8). Hồ sơ đăng ký trước của MIN-DESC nằm ở
> `report/106` **mục sửa đổi (x)**, khoá trước khi có bất kỳ điểm số nào.
>
> Thứ tự thắng khi mâu thuẫn: **mã** > `report/106` > file này > `report/116` > mọi ghi chú cũ hơn.

---

## 0. Ba câu

1. **Nhánh S2 dừng ở một hạt giống.** Chủ luận văn quyết 23/8, lý do ngân sách. Estimand (w)
   vĩnh viễn không hoàn tất; S2 chỉ được nói bằng đúng một câu, kèm nhãn *thăm dò*.
2. **Đóng góp mô hình mới = MIN-DESC**: ORPO stage-2 từ checkpoint **S2**, trên cặp quy chiếu tối
   thiểu ở **tầng khai báo** (`desc` vs `desc_neg`), câu giữ y nguyên. Đối chứng quy công là
   **CE2-S2**. Bốn lượt stage-2, ~20 h A100, ~110 đơn vị.
3. **Không train `s2_nopoint`, không train `s2r`, không train S2/202.** Lý do ở Mục 3.

---

## 1. Vì sao S2 thua — bảng quyết định mọi thứ

Bắt chéo **tên** × **toạ độ** mà chính S2/101 tự sinh, đối chiếu nhãn vàng của tập kiểm,
3.240 bước có tên vàng (`runs/preds_s2_seed101.jsonl` × `runs/score_*_raw.jsonl`):

| tên | point | n | S1 | S2 | Δ |
|---|---|---|---|---|---|
| **đúng** | **trúng** | 1.871 | 81,4% | **87,1%** | **+5,72** |
| đúng | trượt | 184 | 25,5% | 26,1% | +0,54 |
| sai | trúng | 448 | 56,2% | 57,4% | +1,12 |
| **sai** | **trượt** | 731 | 30,6% | **5,6%** | **−25,03** |

**S2 thắng hoặc hoà ở 3/4 ô.** Toàn bộ thiệt hại đến từ đúng một ô — cả tên lẫn toạ độ đều sai
(16,4% quần thể) thì S2 sụp xuống 5,6%.

Thêm ba số cùng nguồn:
- ô `<point>` S2 tự sinh **trúng cửa sổ 14% tới 71,0%**, sai số trung vị **0,81% ngang · 0,18% dọc**;
- nhóm S2 **không sinh** `<desc>` (324 bước): S2 10,8% vs S1 19,4%, `action_ok` 38,9% vs base 83,3%;
- phân rã tổng: **−1,28 pp** đến từ 92,7% bước *có* khai báo, **−0,63 pp** từ 7,3% bước sụp.

⚠️ **Đây là phân tầng hậu kiểm, bị nhiễu bởi độ khó** — đúng như `report/116` Mục 5 cảnh báo.
Nó là căn cứ để **đặt cược**, không phải bằng chứng nhân quả. Phải khai đúng vậy nếu đưa vào bài.

**Đọc ra:** cơ chế khai báo-trước-phát-ngôn-sau **hoạt động**; nó chỉ tự sát khi model nhận nhầm
phần tử rồi cam kết cứng vào cái nhầm đó. Đòn bẩy nằm ở **độ chính xác nhận diện phần tử**, không
nằm ở việc bỏ bớt ô nào của khai báo.

---

## 2. MIN-DESC là gì

```
chosen   = <desc>đúng</desc>       + "\n" + câu người
rejected = <desc>desc_neg</desc>   + "\n" + câu người      ← câu Y HỆT, chỉ ô khai báo đổi
```

Vì câu giống hệt nhau, toàn bộ gradient của vế ưu tiên rơi đúng vào **ô khai báo**: dạy model chọn
đúng phần tử trước khi nói, không đụng gì tới cách diễn đạt.

`desc_neg` = khai báo của phần tử-gần-nhất-khác, do `descriptor_label_build.nearest_other()` dựng
**từ tháng 8** — không dựng mới cho mục đích này.

| | |
|---|---|
| tập cặp | `harness/dg1_cache/train_ac/branches/min_desc.json` — **22.854 cặp** |
| đối chứng | `.../ce2_s2.json` — SFT thuần trên đúng vế chosen của đúng những bước ấy |
| dựng bằng | `harness/build_min_desc.py` (biến đổi thẳng từ `s2.json` ⇒ prompt trùng byte) |
| đo cổng bằng | `harness/do_eligibility.py` (in **cả hai** thiết kế, không có cờ tắt bớt) |
| cổng cơ học | `harness/gate_desc_acc.py` — độ chính xác khai báo, **không gọi bộ trỏ**. Mốc S2/101 = **53,9% cả hai đúng** |
| ⚠️ không dùng làm cổng | `rewards/accuracies` — đo được **0,94–0,97 ngay từ bước đầu** vì `chosen` là thứ S2 đã được dạy. Tín hiệu tiến bộ là `rewards/margins` |
| runbook train | `harness/colab_train_min_desc.md` |
| LR stage-2 | **2,0e-5** (1/5 LR gốc) — phán đoán thiết kế, khai ở (x3b) |
| bốn lượt | MIN-DESC/101 · MIN-DESC/202 · CE2-S2/101 · CE2-S2/202 |
| mỗi lượt | stage-2, **800 update**, `pref_loss: orpo`, β=0,1, final checkpoint |

**Primary `Δ_component = mean_2seed(MIN-DESC − CE2-S2)`.** Secondary `Δ_system = MIN-DESC − S1`.
Ngưỡng, cổng STOP và bốn điều kiện claim: `report/106` mục (x5)–(x6). Dải đọc **dùng lại** dải đã
khoá ở (w), không phát minh dải mới.

### Số đã đo TRƯỚC khi train

| | |
|---|---|
| eligibility tầng khai báo (lọc 80–350 px) | **22.854 / 41.099 = 55,61%** |
| eligibility tầng CÂU (thiết kế `report/116` Mục 12.2) | **26,40%** — sát cổng 25%, và là cận trên |
| bảy bất biến tập cặp | **7/7 ĐẠT** · 0 mẫu `s2.json` lệch khai báo |
| shortcut độ dài: "chọn vế dài hơn" đoán đúng | **43,2%** (ngưỡng 55%) ⇒ chết theo cấu tạo |

---

## 3. Vì sao không chọn ba phương án kia

**`s2_nopoint` (bỏ ô toạ độ, giữ role|name|hint).** Bảng Mục 1 đo đúng giá trị **đứng một mình**
của từng kênh: toạ độ đúng một mình **+1,12 pp**, tên đúng một mình **+0,54 pp**. Toạ độ là ô
*gánh*, không phải ô gây hại — nó trúng 71% với sai số trung vị 0,81%, còn `name` là chuỗi OCR
nhiễu. 448 bước "tên sai nhưng toạ độ trúng" hiện đang được toạ độ cứu; bỏ toạ độ thì nhóm đó rơi
về phía ô sụp. Lại còn đắt gấp đôi: SFT đầy đủ **46 h** cho hai hạt giống, vs 20 h của MIN-DESC.

**`s2r` (khai báo giả từ màn khác, toạ độ ngẫu nhiên).** Được thiết kế để *chắc chắn* thua — nó
tách phần đóng góp của độ dài chuỗi. Không bao giờ ra số đẹp. Chỉ chạy nếu MIN-DESC thắng và cần
quy công sâu hơn.

**MIN-ORPO tầng câu từ S1 (thiết kế gốc trong `report/116`).** Eligibility **26,40%** vs 55,61%;
cặp phải dựng mới và audit luật khớp tên; và quan trọng nhất — **không có thước dev nào không cần
listener**, trong khi Mục 13.3 cấm dùng bộ trỏ để chọn bất cứ thứ gì, nên cổng sau seed 101 gần
như rỗng. Bản tầng khai báo thì đo được thẳng độ chính xác `name`/`point` so với nhãn vàng.

**Vì sao đi từ S2 chứ không phải S1.** S2 khởi đầu thấp hơn 1,9 pp, đúng. Nhưng nó là nhánh duy
nhất có **đòn bẩy đã đo**: khi nhận diện đúng, khai báo cho +5,72 pp; S1 không có cơ chế nào như
vậy nên cải thiện chỉ cộng tuyến tính. Và lỗ trống đã lượng hoá: kéo ô "cả hai sai" (731 bước,
5,6%) lên **ngang mức S1** (30,6%) là đã **+4,1 pp → 61,3%**, tức **+2,2 so với S1**. Ngưỡng thắng
là 60,8% cho cả hai lựa chọn; chỉ có S2 là chỉ được ra chỗ lấy 4 điểm đó ở đâu.

Thêm: cách này **cứu đóng góp đã đăng ký** thay vì vứt. Câu chuyện thành một mạch — *khai
báo-trước-phát-ngôn-sau hoạt động, nhưng chỉ khi model nhận đúng phần tử; chúng tôi thêm một mục
tiêu huấn luyện làm việc nhận diện đáng tin*. Đi từ S1 thì luận văn có một nhánh chết cộng một
nhánh mới không liên quan.

---

## 4. Rủi ro — nói trước, không nói sau

1. **Phân tầng Mục 1 là hậu kiểm, nhiễu bởi độ khó.** Một phần của +5,72/−25 có thể chỉ là "bước
   dễ thì cái gì cũng đúng". Đây là rủi ro lớn nhất của cả phương án.
2. **ORPO pairwise đa phương thức trên LLaMA-Factory chưa từng chạy ở dự án này.** Smoke 20 rồi
   200 cặp dài nhất trước — đúng bài học P10 (12 phút thăm dò cứu một lượt train 20 giờ).
3. **Headline là lựa chọn hậu kiểm.** Mục (x2) của `report/106` khai thẳng điều đó. Cái được khoá
   trước là thiết kế/thước/ngưỡng của MIN-DESC, **không phải** việc chọn nó.
4. **Không trộn bước không-chạm vào stage-2** (lệch Mục 12.5 của `report/116`). Giảm nhẹ: hai nhánh
   bỏ y hệt nhau, và phép no-harm trên bước không-chạm là điều kiện claim bắt buộc.

---

## 5. Lịch

| | việc | GPU |
|---|---|---|
| ✅ 23/8 | Bung `derived_train_en.tar.gz` · đo eligibility đủ tập · dựng 22.854 cặp · 7 bất biến · đăng ký trước (x) | 0 |
| 24–25/8 | Audit mù 300 cặp · probe text-only/shuffled · wrong-referent counterfactual (validity gate) | 0 |
| **26/8** | **Smoke ORPO 20 rồi 200 cặp dài nhất** — `harness/colab_smoke_orpo.md` | ~1 h |
| 27–30/8 | MIN-DESC/101 + CE2-S2/101 → cổng cơ học **không gọi listener** → đạt thì chạy 202 | ~20 h |
| đầu 9/2026 | Chấm UGround **một lần** trên 4.463 cho 4 checkpoint | 0 đồng |

⚠️ **Câu cũ ở đây — "FAIR headline là thước đo" — đã bị quyết định 23/8 thay.** FAIR nay là **bài
mô hình** (headline: ablation khai báo-trước + chẩn đoán cơ chế); thước đo tụt xuống vai dụng cụ.
VCL vẫn là nhãn mô tả phần tử từ `ch3`. Trạng thái hai bản thảo và phản biện bốn giám khảo:
`report/118`. MIN-DESC **không** xuất hiện trong bài nào như một kết quả — chỉ được nhắc một câu
ở FAIR như hướng tiếp theo đã đăng ký trước, **không kèm bất kỳ con số nào**. Máy chạy nền trong
lúc viết bài.

Bảng 2×2 ở Mục 1 nay có **thêm cột Base và cột TRẦN**, dựng bằng `harness/phan_tich_o_khai_bao.py`
(dùng nguyên luật khớp tên của `gate_desc_acc.py`). Số hơi khác Mục 1 vì lọc thêm điều kiện *bước
phải có điểm ở cả S1 lẫn S2*: **1.871 / 184 / 452 / 738** thay cho 1.871 / 184 / 448 / 731.
⭐ Cột trần là thứ chặn biên được đòn *"phân tầng hậu kiểm chỉ đang đo độ khó"*: ô cả-hai-sai có
trần **66,3%** (toàn tập 75,7) trong khi S2 rơi xuống **5,6%** ⇒ độ khó không giải thích hết cú
sụp. Ô *"tên đúng, point trượt"* có trần chỉ **31,0%** ⇒ vùng thước gần như mù, Δ≈0 ở đó phải đọc
là *không có tín hiệu*.

---

## 6. Việc kế tiếp, đúng một dòng

**Chạy `harness/colab_smoke_orpo.md`.** Đó là cổng có thể giết cả phương án, và nó rẻ nhất trong
mọi thứ còn lại. Chưa qua smoke thì không train gì. Qua rồi thì sang
`harness/colab_train_min_desc.md`.

---

# 7. TRẠNG THÁI THỰC THI — chốt cuối phiên 23/8/2026

> Mục này để chat sau không phải dựng lại bối cảnh. Đọc mục này + `report/106` mục (x) là đủ chạy.

## 7.1 Đã xong

| | bằng chứng |
|---|---|
| Bung `derived_train_en.tar.gz` → **41.099 khai báo** bản tiếng Anh | `harness/dg1_cache/train_ac/` · bản pilot cũ sao lưu ở `_bak_pilot_0908/` |
| Đo eligibility đủ tập: **tầng khai báo 55,61%** vs **tầng câu 26,40%** | `harness/do_eligibility.py` |
| Dựng **22.854 cặp** MIN-DESC + **22.854** mẫu CE2-S2 + 200 cặp nặng nhất | `harness/build_min_desc.py` · 7/7 bất biến · 0 mẫu lệch |
| Đăng ký trước MIN-DESC | `report/106` mục **(x)**, **(x3b)** LR, **(x3c)** kết quả smoke |
| **Smoke ORPO QUA CỔNG** | `report/106` (x3c) |
| Vá `mde_that.py` | `report/106` mục **(y)** — ngưỡng đổi 0,01 pp, không kết luận nào đổi |
| Runbook train + cổng cơ học | `harness/colab_train_min_desc.md` · `harness/gate_desc_acc.py` |

## 7.2 Cấu hình đã khoá — không đổi giữa bốn lượt

```
LLaMA-Factory  c4e09c7cbe18844816af9e18a97fe465515edbcd   ← PIN, (x6) đòi cả 4 lượt cùng bản
transformers 5.8.0 · Python 3.13 · TRL DPOTrainer · A100
stage dpo · pref_loss orpo · β 0,1 · max_steps 800 (= 0,56 epoch, KHÔNG phải 1)
learning_rate 2.0e-5 (1/5 LR gốc, xem x3b) · cosine · warmup 0,05
per_device 1 × grad_accum 16 = 16 hiệu dụng   ← đã thử cỡ lô 2, chỉ nhanh 2% ⇒ giữ 1
adapter_name_or_path .../ckpt/s2_seed101 · create_new_adapter false
output_dir TRÊN DRIVE · save_steps 100 (~35 phút/điểm lưu)
```

## 7.3 Sáu cái bẫy đã trả giá trong phiên này — đừng mắc lại

1. ⛔ **`trainer_log.jsonl` ở stack này CHỈ có sáu trường**: `current_steps` · `total_steps` ·
   `epoch` · `percentage` · `elapsed_time` · `remaining_time`. **KHÔNG có `loss`, `lr`,
   `rewards/*`.** Ô theo dõi nào lọc dòng theo `loss` sẽ vứt sạch mọi dòng rồi in *"chưa có bước
   nào"* suốt cả lượt train. `loss`/`learning_rate`/`rewards/*` **chỉ có ở stdout** (`.log`).
2. ⛔ **`enable_liger_kernel` KHÔNG kích hoạt ở stage `dpo`** — log không in dòng nào về liger.
   Chạy tốt không cần nó, nhưng **cấm viết "chúng tôi dùng liger"** cho MIN-DESC.
3. ⛔ **`rewards/accuracies` KHÔNG phải tín hiệu tiến bộ** — nó ~0,85–0,96 ngay từ đầu vì
   `chosen` chính là thứ S2 đã được dạy. Tín hiệu thật là **`rewards/margins`** (mốc đầu ~0,019).
4. ⛔ **Sau ô T2 phải chạy lại ô T3.** `derived.tar.gz` ghi đè `dataset_info.json` bằng bản chỉ có
   4 nhánh cũ, làm mất `gui_min_desc` / `gui_ce2_s2`. Không có lỗi nào báo.
5. ⛔ **`train_runtime` không phải khoá cấp cao nhất** của `trainer_state.json` — nó nằm trong
   mục tóm tắt cuối của `log_history`.
6. ⛔ **`git clone --depth 1` không pin được phiên bản.** Phải clone đầy đủ rồi `git checkout` SHA,
   và kiểm `git rev-parse HEAD` in ra đúng SHA.

## 7.4 Việc kế, đúng thứ tự

1. **Upload `_bundles/thesis_rented.zip` lên Drive** (bản trên đó còn LR 1e-4 và thiếu 3 tệp mới).
2. `harness/colab_train_min_desc.md`: T1 → Restart → T2 → **T3** → T4 → T5 → T6 → T7.
   Ở T4 đổi đúng một dòng: `NHANH, SEED = "min_desc", 101`.
3. Xong MIN-DESC/101 → đổi sang `("ce2_s2", 101)` → chạy lại T4–T7.
4. **Cổng cơ học** `gate_desc_acc.py`, phải vượt mốc S2 **53,9%**. Δ âm ⇒ dừng, không chạy 202.
5. Đạt cổng → hai lượt seed 202.
6. Chấm UGround **một lần** trên 4.463 cho bốn checkpoint → `Δ_component`, `Δ_system` theo (x5).

**Ngân sách còn lại:** ~14–16 h A100 (~80–90 đơn vị) + 22,4 h Kaggle (0 đồng, vừa quota một tuần).
