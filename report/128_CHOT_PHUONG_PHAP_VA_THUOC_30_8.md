# 128 — CHỐT PHƯƠNG PHÁP SPRINT THÁNG 9 VÀ CHỐT KHÔNG ĐỔI THƯỚC (30/8/2026)

> Phiên này trả lời hai câu của chủ luận văn: **(1)** cuối cùng chốt phương pháp nào để ra điểm
> cao hơn, **(2)** có nên đổi thước hoặc đổi bộ trỏ vì trần chỉ 75,7% và điểm hiện tại 60% khó
> mang đi bảo vệ.
>
> ⭐ **Hai câu trả lời một dòng:** train `gui_sel` vs `gui_sft_match` **trên Qwen2.5-VL-3B**, thêm
> mốc `S1-match`, tổng **6 lượt ~69 h A100**. **Không đổi thước, không đổi bộ trỏ** — cả hai
> hướng đều đã có số bác từ chính dự án.
>
> File này **thắng `report/126` ở đúng hai điểm**: backbone (3B thay vì Qwen3-VL-4B) và phạm vi
> lượt chạy (thêm `S1-match`). Mọi thứ còn lại của `126` giữ nguyên: thiết kế hai nhánh, 1 epoch,
> hai hạt vô điều kiện, bộ cổng G1–G11, và các lệnh cấm.

---

## 1. Tách hai đại lượng bị trộn

Gốc của mọi tranh cãi trong `126` là trộn hai thứ không cùng chiều:

| | cái gì quyết định nó |
|---|---|
| **Điểm tuyệt đối** (thứ mang đi bảo vệ) | **khối ứng viên trong câu nhắc** — menu ≤40 dòng có tên + toạ độ |
| **Δ** (thứ đi vào bài) | **đầu chọn `<sel>`** — menu có ở cả hai vế nên triệt tiêu trong hiệu số |

---

## 2. Bốn phương án, phán quyết

| phương án | điểm tuyệt đối | Δ | phán quyết |
|---|---|---|---|
| **`gui_sel` vs `gui_sft_match`** | **63,7–65,1%** kỳ vọng | nhiều khả năng trắng | ✅ **CHỌN** — phương án duy nhất còn nâng được điểm |
| `gui_orpo_hard` | 60,1% (không menu) | ⛔ cần gấp 4,4× mức đã đo | ⛔ chết bằng số của chính dự án |
| chỉ chạy nốt MIN/202 + CE2/202 | 60,1% | gần chắc trắng (+0,63 vs ngưỡng +1,7) | ⏸ tuỳ chọn cuối, không chặn gì |
| không train | 60,1%, một hạt | ô trắng vĩnh viễn | ⛔ kịch bản xấu nhất khi bảo vệ |

`gui_orpo_hard` chết vì: toàn bộ công của ORPO-khó chồng SFT **đã đo = +0,63 pp exec**
(CE2/101 59,42 → MIN/101 60,05), mà estimand của nó còn là **tập con** của +0,63 (khó − ngẫu
nhiên ⊂ khó − không có gì); cộng (x13c) lỗi khai báo lệch trung vị **351 px**, **76,5%** nằm
ngoài dải vế âm khó 80–350 ⇒ tiền đề "vế âm khó" sai, đúng lý do MIN-ONPOLICY đã chết.

---

## 3. ⭐ ĐẢO QUYẾT ĐỊNH CỦA `126`: giữ **Qwen2.5-VL-3B**, không đổi Qwen3-VL-4B

`126` mục 12.2 đã nêu vấn đề và đề nghị phương án (a) là thêm mốc `Base@4B`. Sau khi đọc `123`
§7.2 thì (a) **không đủ**. Chủ luận văn quyết **(b) giữ 3B** ngày 30/8. Bốn lý do đo được:

**① Đổi backbone mua tối đa ~2 pp.** Trần của cả cơ chế là **67,2%**, bị chặn bởi **độ phủ khối
ứng viên** (22% số bước không có tên vàng trong khối) — con số này **không phụ thuộc backbone**.
Lát chọn đúng đã bão hoà: MIN **85,2%** so với người **85,7%**. Dư địa giữa kỳ vọng 65,1 và trần
67,2 chỉ còn **2,1 pp**.

**② Căn cứ đổi backbone yếu về bản chất.** ScreenSpot-v2 93,08 vs 80,9 là benchmark **định vị**.
Mô hình ở đây **không định vị** — nó viết câu và chọn một dòng trong danh sách chữ đã có sẵn tên
và toạ độ; việc định vị do UGround làm. `123` cũng tự khai số đó *"phải xác minh model card,
hiện dùng làm quyết định vận hành tạm"*.

**③ Giữ 3B mua được bảng phân rã ba tầng, mỗi tầng đúng một biến** — thứ đắt hơn hẳn 2 pp:

```
S1-match  --[thêm menu]-->  gui_sft_match  --[thêm đầu chọn]-->  gui_sel
```

Tầng một đo **công của khối ứng viên**, tầng hai đo **công của đầu chọn** (chính là Δ đã đăng ký).
Kể cả tầng hai ra trắng, vẫn có bảng đọc được. Với 4B thì không có ngân sách cho mốc nào ⇒ Δ
trắng là **không còn gì để trình**.

**④ Rủi ro vận hành.** Qwen3-VL chưa từng chạy trong dự án; giờ/epoch chưa đo (kịch bản xấu
112–148 h là vỡ ngân sách); phải ghim `torch==2.8.0` vì regression 3DConv (LLaMA-Factory #9380);
G4 phải đo lại bằng tokenizer mới kể cả token ảnh.

⚠️ **Chọn 3B không phá quyết định nào của bản Mac.** `123` §8.1 đã ghi 3B là nhánh cứu chính thức
(~46 h) và thứ tự hy sinh là **epoch → backbone → nhánh phụ**. Đây là thi hành nhánh đó ngay thay
vì chờ G5b. **Cổng G5b vẫn chạy** để có số giờ/epoch thật, chỉ không còn dùng để quyết 4B/3B.

---

## 4. Phạm vi chốt: **6 lượt**

| gói | lượt | A100 | Kaggle | trạng thái |
|---|---|---|---|---|
| bắt buộc — `gui_sel` / `gui_sft_match` × hạt 101, 202 | 4 | ~46 h | ~22 h | ✅ chạy |
| + `S1-match` × hạt 101, 202 (1 epoch, cutoff 3072, **câu nhắc không menu**) | 2 | ~23 h¹ | ~11 h | ✅ chạy |
| + MIN/202 + CE2/202 | 2 | ~13,5 h¹ | ~11 h | ⏸ **tuỳ chọn cuối** |
| **tổng đang chốt** | **6** | **~69 h** | **~33 h** | trong ngân sách 72–88 h, **còn nguyên 15 h đệm** |

¹ ước lượng suy ra (46 h / 4 lượt cho `S1-match`; 800 bước × ~21 s/bước × 2 + suy luận cho
MIN/CE2), **chưa phải số đo** — G5b sẽ cho số thật.

**Vì sao không lấy cả ba gói.** MIN/202 + CE2/202 tốn 13,5 h A100 + 11 h Kaggle để xác nhận một
con số đã biết (+0,63 pp), gần chắc vẫn rơi ô trắng; nó không nâng điểm, không đổi bảng bảo vệ.
Đổi 15 h đệm mất máy lấy một ô trắng là đổi sai chiều — Colab đã ăn của dự án **18 giờ trong hai
lượt S1**. Giữ ở dạng tuỳ chọn: chạy nếu xong 6 lượt mà còn đệm và còn tuần Kaggle.

**Vì sao không rút xuống 4 lượt.** Không có `S1-match` thì tầng dưới phải so với S1 cũ, vốn lệch
**ba biến cùng lúc** (2 epoch vs 1 · cutoff 2560 vs 3072 · câu nhắc không menu) — đúng loại so
bắc cầu mà `123` §9.1 cấm.

⚠️ Kaggle 33 h phải **chia hai tuần** (trần 30 h/tuần).

---

## 5. ⛔ THƯỚC VÀ BỘ TRỎ: KHÔNG ĐỔI. Ba câu hỏi, ba số bác.

### 5.1 Đổi luật chấm cho điểm cao hơn — không mua được gì

Năm luật, lát 698 bước (`report/112` §5.7):

| luật | trần |
|---|---|
| **Voronoi (đang dùng)** | **82,2%** |
| chỉ cần đúng hộp chứa (lỏng nhất) | 82,2% |
| chữ nhật 14% kiểu AITW | 80,2% |
| chữ nhật 7% | 74,2% |
| chữ nhật 3% | 56,6% |

Voronoi **đã là luật cho trần cao nhất**; luật lỏng nhất chỉ bằng. Nới luật còn **nâng cả sàn** ⇒
dải phân biệt hẹp lại. Và dưới `hit_disk` thì **MIN ngang S1 (69,2 vs 69,2)** ⇒ đổi sang disk
**xoá luôn Δ**. Con số *"~77–78%"* mà một agent từng nêu là **bịa**, không có trong kho.

### 5.2 Đổi bộ trỏ mạnh hơn — dự án đã thử một lần, kết quả NGƯỢC

Phép B (20/8), `UI-Venus-Ground-7B` mạnh hơn UGround trên ScreenSpot-v2 (99,0/90,0 vs 95,0/83,3):

| | UGround-2B | UI-Venus-7B |
|---|---|---|
| trần (lát 2.532) | 70,0% | **69,3%** |
| Base | 42,50 | **39,06** |
| S1 | 52,84 | **48,74** |
| S2 | 49,45 | **46,60** |

⭐ **Bộ trỏ điểm benchmark cao hơn cho điểm THẤP hơn ở cả ba nhánh.** Cơ chế: thước phán bằng
ngưỡng 14% trước rồi mới Voronoi, nên sai số khoảng cách không dự đoán được trần; và **72% ca
thước mù là bộ trỏ lệch >14% bề ngang**, tức nó **bỏ cuộc**, không phải trỏ nhầm nút bên cạnh —
loại lỗi mà độ chính xác pixel cao hơn không cứu được.

Giá: bộ trỏ 7B chấm ~**14,4 h** một lượt đủ 4.463 bước ⇒ sáu bảy lượt là **ba tuần quota Kaggle**,
và mọi con số trong hai bài báo lẫn luận văn phải đo lại từ đầu.

Đòn nặng nhất: **đổi thước sau khi đã thấy điểm** là đúng thứ dự án tự khai cấm, và dự án đã tự
khai **hai lần nới ngưỡng sau khi thấy điểm**. Trước hội đồng, câu hỏi *"vì sao đổi thước ở giai
đoạn này"* không có câu trả lời nào ngoài *"để số đẹp hơn"*.

### 5.3 ⭐ Cách đúng để 60% hết khó bảo vệ: đổi CÁCH TRÌNH, không đổi thước

Vấn đề không nằm ở con số, mà ở chỗ **60% đang bị đọc trên nền 100**. Thước này chạy từ **12,0**
(câu vô nội dung) tới **75,7** (câu do chính người viết).

| nhánh | exec | so với trần người | vị trí trong dải dùng được |
|---|---|---|---|
| Base | 47,59 | 62,8% | 55,9% |
| S1/101 | 59,11 | 78,0% | 74,0% |
| MIN-DESC | 60,05 | **79,3%** | 75,4% |
| `gui_sel` kỳ vọng | 63,7–65,1 | **84,1–86,0%** | 81,2–83,2% |

⇒ Câu đi bảo vệ **không phải** *"mô hình đạt 60%"*, mà là **"câu do mô hình sinh ra đạt 84–86%
năng lực của câu do người viết, trên cùng một phép đo"**.

Ba thứ chống lưng, đều đã đo:
- **Trần 75,7% là giới hạn dụng cụ, không phải giới hạn ngôn ngữ:** 1.083 bước câu người cũng
  trượt, **72%** do bộ trỏ lệch >14%; lọc riêng câu chuẩn ≤3 từ trần chỉ lên **77,0%**.
- **Thước này chặt hơn quy ước của lĩnh vực:** bài gốc AndroidControl chấm bằng khớp thao tác và
  toạ độ trực tiếp; ta thêm một tầng suy giảm — câu sinh ra phải đủ để **một mô hình độc lập,
  không thấy nhãn**, trỏ trúng. So 60% của ta với 70–80% của họ là so hai đại lượng khác nhau,
  và điều này phải nói rõ ngay trong chương thước đo.
- **Thứ tự các nhánh không đổi dưới cả năm luật chấm lẫn hai bộ trỏ** ⇒ kết luận so sánh bền,
  chỉ con số tuyệt đối phụ thuộc luật.

### 5.4 ✅ Một việc nên làm, tốn 0 giờ GPU

Báo thêm `exec` dưới **luật chữ nhật 14% kiểu AITW** như **thước đồng-báo** (không phải headline).
Tính lại được từ **tệp thô**, không gọi lại bộ trỏ. Nó cho số cao hơn và so được với quy ước của
lĩnh vực. `123` §5 vốn đã dự tính *"1 thước chính + 4 đồng-báo"* nên đây **không phải nới luật**.

⚠️ **Điều kiện bắt buộc phải khai kèm:** dưới luật lỏng đó Δ giữa các nhánh **co lại gần 0**
(dưới `hit_disk`, MIN ≈ S1). Nó chỉ để định vị so với literature, **không** để đọc đóng góp.

---

## 6. Những gì KHÔNG đổi so với `126`

Thiết kế hai nhánh (`<sel>` + câu vs chỉ câu, câu nhắc byte-identical) · 1 epoch · **hai hạt
101/202 vô điều kiện** · QLoRA 4-bit, freeze vision, cutoff 3072, lr 1e-4, lô hiệu dụng 16 ·
`Δ = mean_2hạt[exec(gui_sel)] − mean_2hạt[exec(gui_sft_match)]` · dải đọc (w) · bộ cổng
G1/G2/G3/G4/G5/G5b/G6/G9/G10/G11 · **headline `exec`/`hit_voronoi` không đổi** · `sel_acc` là
**thước phụ, không phải headline** · bốn cách kéo Δ cho đẹp vẫn **cấm**.

⚠️ **Cổng G6 giữ ngưỡng ≥63,6% trên dev.** Trượt G6 = STOP.

---

## 7. Việc phải làm, thứ tự

| # | việc | chặn cái gì |
|---|---|---|
| 1 | Kéo `train_ac/train.jsonl` + `train_ac/ocr.jsonl` bản đầy đủ từ Drive (~80 MB) | **mọi thứ ở dưới** |
| 2 | `build_candidates.py --split train --all-steps` → G1/G2 TRAIN + tỉ lệ khối rỗng | (x16), dựng data |
| 3 | Đọc mù 300 mẫu G3 (`branches/g3_mau300_doc_mu.txt`) | dựng data |
| 4 | Dán **(x16)** vào `report/106` — **sau** khi có số ở #2, **ghi rõ backbone 2.5-VL-3B và ba nhánh** | train |
| 5 | `build_sel_data.py --split train` từ **đúng** `ocr.jsonl` đã dựng S1/S2 | train |
| 6 | Dựng thêm nhánh **`S1-match`** (cùng config, câu nhắc **không** khối ứng viên) | tầng menu |
| 7 | G4 đo lại — **tokenizer Qwen2.5-VL, cutoff 3072** (không còn là Qwen3-VL) | train |
| 8 | G5 smoke 20 bước → **G5b pilot 200 bước** (lấy số giờ/epoch thật, không còn để quyết backbone) | lịch |
| 9 | Train `gui_sel` ≥2.000 update → **G6 trên dev ≥63,6%**. Trượt = STOP | năm lượt còn lại |
| 10 | Sáu lượt → suy luận greedy → chấm (chia hai tuần Kaggle) → Δ = trung bình 2 hạt → G8/G10/G11 | — |

**Làm song song, 0 GPU:** thêm thước đồng-báo AITW-14% từ tệp thô · đưa cảnh báo lát nội sinh
**11,50 pp** [9,40 · 13,37] vào Limitations · viết lại cách trình điểm theo **tỉ lệ trên trần
người** trong luận văn (mục 5.3 file này) · verify nguồn còn treo ở `126` mục 11.3.

---

## 8. Một câu để nhớ

Thước không phải chỗ để kiếm điểm. **Đổi luật không nâng trần** (Voronoi đã là luật trần cao
nhất) và **đổi bộ trỏ mạnh hơn còn hạ điểm** (đo rồi, cả ba nhánh). Chỗ duy nhất còn kiếm được
điểm là **khối ứng viên**, và chỗ duy nhất còn kiếm được sức thuyết phục là **trình 60% đúng nền
của nó**: 79,3% năng lực của câu do người viết, trên một phép đo chặt hơn quy ước của lĩnh vực.
