# 266 — Kết quả TAGE V1–V3 trên val C1, 3/10/2026 (nhật ký số theo cổng; bản trình bày khách quan, so S1: `report/267`)

> ⛔ **Số val — cấm trích vào luận văn.** Chỉ dùng để quyết có đi tiếp TAGE không (action 265).
> Nguồn: `runs/tage_val/that/` (Colab L4, lượt 2–3/10) · đọc bằng `python3 harness/tage_doc.py`.
> Action gốc: `harness/tai_lieu_2026-10-02/265_ACTION_KIEM_THU_TAGE_VAL_2_10_checked.md` · runbook
> `harness/colab_tage_val_l4.md`.

## 1. Phán quyết

**[V1] ĐI TIẾP.** Trên 249 bước click val C1, bộ biên tập đọc vùng cắt quanh phần tử vàng đưa exec
từ **165 (ck500) lên 184**, tức +19 bước ròng (ngưỡng ≥ 10). Cùng bộ biên tập đọc vùng cắt quanh phần
tử lân cận chỉ còn **60** ⇒ gold − neg = **+124 bước** (ngưỡng ≥ 10). Bộ biên tập thật sự đọc vùng cắt
chứ không chỉ viết lại câu cho hay hơn.

| nhánh | exec | Δ so ck500 | KTC95 (bootstrap theo episode) | cứu / phá | đổi câu |
|---|---|---|---|---|---|
| ck500 (mốc) | 165/249 · 66,27 | — | — | — | — |
| gold | **184/249 · 73,90** | **+7,63** | [+2,41; +12,85] | 29 / 10 | 175 (70,3%) |
| gold+cổng | 184/249 · 73,90 | +7,63 | [+2,81; +12,45] | 26 / 7 | 134 |
| neg | 60/249 · 24,10 | −42,17 | [−50,20; −34,14] | 12 / 117 | 217 (87,1%) |
| neg+cổng | 165/249 | 0,00 | — | 0 / 0 | 0 (τ = ∞) |
| k0_lai (kiểm dụng cụ) | 157/249 | — | — | — | — |

· Trong 29 bước cứu: **27/80** bước ck500 trỏ sai phần tử, 2/4 bước sai loại thao tác. `action_ok` của
  gold 249/249 (ck500 245).
· Cổng giữ/sửa **không thêm gì**: τ chọn chéo ≈ 0 (−0,003 · −0,203), gold+cổng = gold. Cổng chỉ giảm
  phá 10 → 7 nhưng mất 3 bước cứu. Ở nhánh neg, cổng tự đóng hẳn (τ = ∞) ⇒ log-prob sửa/nháp phân biệt
  được vùng cắt sai nhưng không cộng được điểm cho vùng cắt đúng.
· Cảnh báo đọc: vùng cắt **vàng** là oracle — đây là trần của TAGE, chưa phải hệ thật. Câu hỏi thật
  là V2 (bộ định vị có trỏ được vùng cắt đúng không).

## 2. Dụng cụ chấm lệch một bước (157 thay vì 158)

k0_lai (câu S1 greedy cũ, chấm lại) ra **157**, lượt 251 ra 158. Đã so từng bước với
`runs/grpo_spice/score_k0_lai_raw.jsonl`: **câu trùng 249/249**, toạ độ UGround lệch ở 53 bước (đa
số vài px, 6 bước > 50 px), **lật exec đúng 1 bước** (`(1161, 0)`). Nguyên nhân: lượt cũ chấm trên
Kaggle **T4 fp16**, lượt này chấm trên Colab **L4 bf16** (log `merge.log`, `cham_*.log`).
⇒ Nhiễu dụng cụ cỡ ±1 bước, nhỏ hơn rất nhiều so với +19 (gold − ck500) và +124 (gold − neg); phán
quyết không đổi. Nhưng ck500 (165) vẫn là số chấm trên T4 ⇒ **C6 đã thêm `cham("ck500_l4", …)`**
để có mốc cùng môi trường. Hai chỗ kiểm (`tage_doc.py`, ô C5b) nới thành 158 ± 2.

## 3. Train bộ biên tập (ed_gold, 1 epoch = 320 bước, 2.554 mẫu)

· Mẫu đầu nll vàng 1,873 (adapter mới) · cuối epoch nll vàng ~0,50 · nll nhiễu ~0,76 · biên hoạt
  0,5–0,65 ⇒ chưa bão hoà, epoch 2 còn chỗ học.
· Đỉnh VRAM 13,78 GiB trên L4.
· Câu nháp: greedy ck500 trùng câu người 686/2.554 (26,9%).
· Crash một lần ở bước 263 (mẫu 2.099 = `ep14503_s1`, nhãn x = 2163 > bề ngang 1080). Vá bằng kẹp
  điểm vào ảnh trong `cat_vung` (md5 `e15f9d52…`), thứ tự mẫu không đổi; mất máy một lần ở bước 270,
  chạy tiếp từ điểm lưu 260.

## 4. V2 + V3 (C6, Colab L4 3/10)

Train ba thứ, mỗi thứ 1 epoch (2.554 mẫu): `ed_none` 121,8 phút · `loc_g` · `loc_d` ~123 phút mỗi bộ,
2,8–2,9 s/mẫu, đỉnh VRAM 11,3 GiB.

**V2 đạt:** `loc_g` (ảnh + nhiệm vụ) trúng ±14% **193/249**, trên 80 bước ck500 trỏ sai trúng **38**
(ngưỡng ≥ 20); không đọc được toạ độ 0. `loc_d` (thêm câu nháp ck500) kém hơn: 190/249 và **28/80** ⇒
câu nháp kéo bộ định vị về đúng chỗ ck500 trỏ sai.

**V3 không đạt:**

| nhánh | exec / 249 | Δ so ck500 (T4) | KTC95 | cứu / phá |
|---|---|---|---|---|
| ck500 chấm lại L4 | 166 | (+1, nhiễu dụng cụ: lật 1 bước, câu trùng 249/249) | — | — |
| none | 164 | −0,40 | [−4,82; +3,61] | 11 / 12 |
| none+cổng | **169** | +1,61 | [−1,61; +4,82] | 9 / 5 |
| pred | 158 | −2,81 | [−8,03; +2,41] | 14 / 21 |
| pred+cổng | 168 | +1,20 | [−0,40; +3,61] | 4 / 1 · chỉ sửa 8 câu |

Cả hai điều kiện đều trượt: pred+cổng chỉ +3 bước (cần ≥ +3,7) **và** không hơn none+cổng (168 < 169).

### Vì sao vùng cắt vàng +19 mà vùng cắt đoán thì không

Chia 249 bước theo việc phần tử vàng có nằm trong vùng cắt quanh điểm `loc_g` đoán hay không (vùng
vuông cạnh 0,4·W, tính theo pixel; 196 bước trong · 53 ngoài; 193 bước "trúng ±14%" thì chỉ 2 bước
vàng nằm ngoài vùng ⇒ thước trúng không thổi phồng):

| tập | n | ck500 | gold | pred | none |
|---|---|---|---|---|---|
| vàng **trong** vùng đoán | 196 | 153 | 159 (+6) | 156 (+3) | 151 |
| vàng **ngoài** vùng đoán | 53 | 12 | **25 (+13)** | **2 (−10)** | 13 |

· **Hai phần ba mức tăng của gold (+13/+19) nằm ở 53 bước mà bộ định vị KHÔNG tìm ra phần tử.** Ở đó
  vùng cắt vàng mang thông tin vị trí mà cả ck500 lẫn bộ định vị đều không có; còn vùng cắt đoán sai thì
  bộ biên tập tin theo và phá 10 bước.
· Trên 196 bước bộ định vị tìm ra phần tử, chính vùng cắt vàng cũng chỉ +6 (cứu 16 phá 10) — câu pred
  trùng câu gold 158/196. Phần lớn các bước này ck500 vốn đã đúng (153/196).
· **Trần với cổng hoàn hảo** (chỉ sửa khi biết chắc vàng trong vùng): **168/249**, tức +3 so ck500 —
  vẫn dưới ngưỡng V3 dù cổng không sai lần nào.
⇒ Giá trị của TAGE nằm trọn ở việc **tìm vị trí trên những bước khó**, và đúng những bước đó bộ định vị
1 epoch không tìm ra. Bộ biên tập học được việc đọc vùng cắt (V1 rõ ràng), nhưng không bù được bộ định vị.

## 5. Kết luận và việc kế

Theo tiêu chí V3 đặt ở 265 thì chưa đạt; người dùng 3/10 bỏ khung ngưỡng, trình bày theo số đo ở `report/267`. Hướng cải thiện là một bộ định vị tìm được phần tử ở các bước
khó (53 bước ngoài vùng): train trên ~41 nghìn bước click thay vì 2.554, hoặc thay bằng bộ trỏ mạnh có sẵn.
Đó là một dự án định vị riêng, chi phí nhiều giờ GPU. Trần với bộ định vị hiện tại là 168 (cổng hoàn hảo);
trần với bộ định vị hoàn hảo là 184 (gold), và khoảng cách đó nằm trọn ở 53 bước khó — chưa có số đo nào
cho thấy bộ định vị lớn hơn tìm được các bước này. Chờ người dùng quyết.

**Phần cũ (trước C6), giữ để tra:** C6 = train `ed_none` + hai bộ định vị + sửa val `pred`/`none` + chấm 3
tệp (kể cả `ck500_l4`); phiên mới C1 → C4 → C5 → C6.
