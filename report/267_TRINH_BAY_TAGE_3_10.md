# 267 — Trình bày kỹ thuật: GRPO-SPICE (ck500) và TAGE so với S1/101 (2–3/10/2026)

Tổng hợp những gì đã làm và đo được trong đợt này, theo thứ tự: mốc S1 → GRPO-SPICE ck500 → TAGE xây
trên ck500. Số chi tiết, nhật ký sự cố và bảng phân rã đầy đủ ở `report/259` · `261` · `262` (GRPO) và
`report/266` (TAGE).

**Hai loại số, đọc khác nhau:**
- **Số test** (4.463 bước click của tập kiểm, chấm một lần): chỉ có cho ck500.
- **Số val** (249 bước click của val C1, tách từ tập dạy, theo episode): có cho mọi nhánh TAGE. Val dùng để
  so các nhánh với nhau; ⛔ không trích vào luận văn. TAGE chưa có số test.

Mọi phép so đều **ghép cặp theo bước** `(episode_id, step_id)`. KTC95 bootstrap 10.000 lần, cụm = ứng dụng
(test, đúng `score_run.cluster_bootstrap`) hoặc cụm = episode (val, `tage_doc.ktc`).

---

## 1. Mốc S1/101

S1/101 là SFT trơn trên Qwen2.5-VL-3B (QLoRA, 2 epoch, 64.567 bước dạy, hạt giống 101). Trên test: exec
**59,11** [57,33; 60,83] (`score_s1_seed101.json`). Trên val C1: câu greedy (tệp `k0`, lượt 251) exec
**158/249 = 63,45**.

**exec** = câu sinh ra được UGround-V1-2B đọc và trỏ trúng: đúng loại thao tác ∧ điểm trỏ trong ±14% bề
ngang/bề cao quanh điểm vàng ∧ phần tử gần điểm trỏ nhất (Voronoi) là phần tử vàng (`metric_exec.py`).

## 2. GRPO thưởng SPICE — checkpoint 500 (ck500)

### 2.1 Phương pháp

- Hoà adapter S1/101 vào mô hình gốc (fp16) rồi gắn một LoRA **mới**; tham chiếu KL là đúng S1.
- GRPO (TRL), G = 8 câu mỗi câu nhắc, 500 bước cập nhật, thưởng = **SPICE(câu sinh, câu chuẩn) − 0,02 ×
  phạt độ dài**. Không bộ trỏ nào nằm trong phần thưởng.
- Train trên Kaggle T4 (~160 s/bước, VRAM 13,2 GiB), nối 3 commit; điểm lưu mỗi 25 bước. Lượt chạy tiếp
  ở commit 2 từng nạp sai adapter (transformers chỉ nạp thư mục `ref/`), đã sửa bằng nạp tay và chạy lại
  250 → 500 (`report/254`).
- Mã: `harness/grpo_spice.py` · runbook `harness/kaggle_grpo_spice_commit.md`.

### 2.2 ck500 so với S1/101 trên test — 13 cột (`report/259`, `261`)

| cột | S1/101 | ck500 | Δ | KTC95 | phá / cứu |
|---|---:|---:|---:|---|---|
| **exec** | 59,11 | **60,65** | **+1,55** | [+0,80; +2,33] (p McNemar 1,6e−5) | 90 / 159 |
| D.3 (hộp phần tử, luật AndroidControl) | 65,49 | 67,02 | +1,52 | [+0,77; +2,29] | 97 / 165 |
| AitW đầy đủ | 74,37 | 76,25 | +1,88 | [+1,17; +2,63] | 88 / 172 |
| ±14% theo trục | 67,24 | 68,90 | +1,66 | [+0,90; +2,46] | 98 / 172 |
| AitW cận trên | 81,04 | 82,90 | +1,86 | [+1,17; +2,60] | 80 / 163 |
| đúng loại thao tác | 94,35 | 95,97 | +1,61 | [+1,17; +2,08] | 11 / 83 |
| BLEU-4 | 51,56 | 52,36 | +0,80 | | |
| METEOR 1.5 | 36,79 | 37,92 | +1,13 | | |
| ROUGE-L | 67,35 | 68,36 | +1,01 | | |
| CIDEr-D | 416,12 | 430,05 | +13,93 | | |
| **SPICE** | 44,37 | **45,79** | **+1,42** | [+0,69; +2,16] | |
| chrF | 61,26 | 62,87 | +1,61 | | |
| BERTScore (rescaled) | 66,33 | 67,07 | +0,74 | | |

- ck500 cao hơn S1/101 ở cả 13 cột.
- Phân rã Δexec: +28 bước từ sửa loại thao tác, +41 bước từ đổi sang đúng phần tử (trên các bước cả hai
  đúng loại thao tác).
- So các nhánh khác (exec, test): − S1/202 (59,62) **+1,03** [+0,25; +1,83] · − GRPO-point (60,07)
  +0,58 [−0,50; +1,69] · − MIN-DESC (60,05) +0,60 [−0,52; +1,73].
- **Bước không chạm** (2.495 bước, `report/262`): toàn bộ 85,97 → 84,29 (−1,68 [−2,76; −0,62]); scroll
  83,97 → 77,75 (**−6,23** [−8,30; −4,31]); navigate_back −5,93; wait **+4,55**; open_app +1,71. Cơ chế
  đo được: ck500 viết câu chạm nhiều hơn (47/51 bước scroll bị phá chuyển thành câu "Click …").
- Kiểm đường sinh: ck500 sinh trên S1 đã hoà (fp16, từng câu), S1/101 công bố sinh qua LoRA chưa hoà theo
  lô; trên 20 câu kiểm, 16/20 trùng.

### 2.3 ck500 so với S1/101 trên val C1 (249 bước)

| | S1/101 | ck500 | Δ |
|---|---:|---:|---:|
| exec | 63,45 | 66,27 | +2,81 [−0,40; +6,02] · cứu 12 phá 5 |

(Bảng đủ thước chữ ở §3.4.) Trong 84 bước ck500 sai: **80 bước trỏ sai phần tử**, 4 bước sai loại thao
tác; 52/84 bước không câu nào trong 9 câu S1 (1 greedy + 8 mẫu) làm đúng.

## 3. TAGE — Type-Aware Grounded Editor (xây trên ck500)

### 3.1 Phương pháp

```
ảnh + nhiệm vụ ─► ck500 viết câu nháp
bộ định vị ─► điểm (x, y) ─► cắt vùng vuông cạnh 40% bề ngang, tâm (x, y), phóng 448×448
ảnh gốc + vùng cắt + câu nháp ─► bộ biên tập viết lại câu
cổng: nhận câu sửa khi lp(câu sửa) − lp(câu nháp) > τ, ngược lại giữ câu nháp
```

**Bộ biên tập.** LoRA r16 / α32 / dropout 0,05 trên S1 đã hoà, chỉ tầng ngôn ngữ (q, k, v, o, gate, up,
down của LLM; không đụng phần thị giác), 29,9 triệu tham số học.
- Mất mát = CE(câu chuẩn | ảnh, vùng cắt đúng) + 0,5 · relu(0,2 − (nll_nhiễu − nll_vàng)); nll_nhiễu là
  nll của cùng câu chuẩn khi vùng cắt đặt quanh **phần tử lân cận cùng vai trò** (từ `descriptors_trueD`,
  41.099 dòng; thiếu lân cận thì lấy một ô OCR khác trên màn, không có nữa thì lấy điểm đối xứng qua tâm màn).
- Câu nháp lúc train: chọn ngẫu nhiên giữa câu greedy và các câu mẫu của ck500 cho bước đó; 30% câu nháp
  bị làm hỏng có chủ ý (thay tên phần tử bằng tên phần tử lân cận).
- Che nhãn: chỉ tính mất mát trên câu trả lời; mã kiểm câu nhắc là tiền tố của chuỗi đầy đủ trước khi che.
- AdamW lr 1e-4, warmup 30 bước rồi giảm tuyến tính về 0, accum 8, clip 1,0, bf16.

**Bộ định vị.** Cùng cấu hình LoRA, đích là chuỗi `(x, y)` thang 0–1000. Hai biến thể: `loc_g` (ảnh +
nhiệm vụ), `loc_d` (thêm câu nháp ck500).

**Cổng.** τ chọn chéo theo episode: chia episode làm hai nửa, τ tối ưu exec trên nửa này được áp lên nửa
kia (hoà thì lấy τ lớn hơn).

**Dữ liệu dạy.** 2.554 bước click của `fgrb_p1_bundle` (đã bỏ mọi episode có mặt trong val). Câu nháp
ck500 cho 2.554 bước: greedy trùng câu chuẩn 26,9%.

**Các nhánh đã chạy:**

| nhánh | bộ biên tập | vùng cắt lúc sửa val |
|---|---|---|
| gold | `ed_gold` | quanh điểm vàng |
| neg | `ed_gold` | quanh phần tử lân cận (đối chứng: vùng cắt sai chỗ) |
| none | `ed_none` (train không vùng cắt) | không có (đối chứng: chỉ viết lại) |
| pred | `ed_gold` | quanh điểm `loc_g` đoán (hệ chạy thật) |
| +cổng | | cổng giữ/sửa áp lên nhánh tương ứng |

### 3.2 Hiện thực và chạy máy

- Mã viết trên WSL: `harness/tage_val.py` (hoà, selftest, câu nháp, train, sửa val, định vị) ·
  `harness/tage_doc.py` (đọc kết quả, 0 GPU) · `harness/tage_neg_build.py` · `harness/tage_text_metrics.py`
  (§3.4) · runbook `harness/colab_tage_val_l4.md`.
- Máy: Colab L4, mỗi thành phần train **1 epoch** (320 bước tối ưu, 2.554 mẫu).

| pha | thời gian | tốc độ / VRAM |
|---|---|---|
| câu nháp 2.554 bước | ~2,5 h | 3,5 s/bước |
| `ed_gold` | ~4,8 h | 6,7 s/mẫu · 13,8 GiB |
| `ed_none` | 121,8 phút | 2,9 s/mẫu · 11,3 GiB |
| `loc_g` · `loc_d` | 122,7 · 123,3 phút | 2,8 s/mẫu · 11,3 GiB |
| định vị val (mỗi bộ) | ~8 phút | 1,8 s/bước |
| sửa val (mỗi nhánh) | ~15 phút | 3,6 s/bước |
| chấm UGround (mỗi tệp) | 6–8 phút | 0,71 bước/s |

Tổng ~15–16 h L4. Lượt chạy chịu được mất máy: train lưu `ckpt_last/` (adapter + optimizer + lịch lr) mỗi
20 bước với thứ tự mẫu tất định; sửa val, định vị, chấm ghi từng dòng; đồng bộ Drive 5 phút; ô cuối tự ngắt
runtime khi xong/lỗi.

**Sự cố đã xử:** (1) nhãn hỏng `ep14503_s1` (x = 2.163 > bề ngang 1.080) làm crash ở bước 263 → kẹp điểm vào
ảnh trong `cat_vung`, thứ tự mẫu giữ nguyên, quét toàn tập chỉ một bước hỏng; (2) mất máy ở bước 270 → chạy
tiếp từ điểm lưu 260; (3) chấm trên L4 bf16 lệch Kaggle T4 fp16: k0 chấm lại 157 (lượt cũ 158), ck500 chấm
lại 166 (lượt cũ 165); câu trùng 249/249, mỗi tệp lật đúng 1 bước.

### 3.3 Kết quả thành phần

**Train.**
- `ed_gold`: nll vàng 1,873 (mẫu đầu) → ~0,50 cuối epoch; nll nhiễu ~0,76; luôn nll vàng < nll nhiễu.
- `ed_none`: nll vàng 1,851 → 0,46–0,64.
- `loc_g`: nll 2,834 → 2,38 (bước 10) → 1,40 (bước 20).

**Bộ định vị trên val** (trúng = trong ±14% quanh điểm vàng):

| bộ định vị | trúng / 249 | trên 84 bước ck500 sai | trên 80 bước ck500 trỏ sai | không đọc được toạ độ |
|---|---:|---:|---:|---:|
| `loc_g` | 193 (77,5%) | 40 | 38 | 0 |
| `loc_d` | 190 (76,3%) | 30 | 28 | 0 |

Trong 193 bước `loc_g` trúng, 191 bước có phần tử vàng nằm trong vùng cắt; tổng cộng 196/249 bước phần tử
vàng nằm trong vùng cắt đoán.

**Sửa val:** gold đổi 175/249 câu (70,3%) · neg 217 (87,1%) · pred 174 (69,9%) · none 162 (65,1%); câu
trung vị 5–6 từ; 0 câu tiếng Việt.

### 3.4 Mọi nhánh so với S1/101 trên val C1 (249 bước) — bảng đủ thước

Nguồn: `runs/tage_val/that/so_s1.json` (`harness/tage_text_metrics.py`). Thước vị trí dùng đúng hàm của
`luat_d3.py` / `luat_aitw_day_du.py` (kiểm: tái lập tuyệt đối S1 trên test 65,49 · 74,37 · 67,24); hộp vàng
từ `train_ac/descriptors.jsonl`, phủ 248/249 bước (bước thiếu hộp tính trượt). Thước chữ tính mức kho,
một câu chuẩn mỗi bước (CIDEr-D vì vậy > 100). Chưa có cột *AitW cận trên* (cần mọi hộp bấm được của màn val).

**Thước vị trí**

| nhánh | exec | Δexec vs S1 [KTC95] | cứu / phá | D.3 | AitW đầy đủ | ±14% theo trục | AitW khoảng cách | action_ok |
|---|---:|---|---|---:|---:|---:|---:|---:|
| S1/101 | 63,45 | — | — | 69,88 | 78,31 | 70,68 | 70,68 | 95,98 |
| ck500 | 66,27 | +2,81 [-0,40; +6,02] | 12 / 5 | 71,08 | 79,92 | 73,09 | 73,09 | 98,39 |
| TAGE gold | 73,90 | +10,44 [+5,62; +15,66] | 33 / 7 | 80,72 | 89,96 | 82,73 | 82,33 | 100,00 |
| TAGE neg | 24,10 | -39,36 [-47,79; -30,92] | 14 / 112 | 28,11 | 51,41 | 45,38 | 42,57 | 100,00 |
| TAGE none | 65,86 | +2,41 [-1,20; +6,02] | 13 / 7 | 73,09 | 81,53 | 73,90 | 73,90 | 100,00 |
| TAGE pred | 63,45 | +0,00 [-5,62; +6,02] | 21 / 21 | 68,27 | 79,52 | 72,29 | 71,89 | 100,00 |
| TAGE none+cổng | 67,87 | +4,42 [+1,61; +7,63] | 13 / 2 | 74,30 | 81,93 | 75,10 | 75,10 | 100,00 |
| **TAGE pred+cổng** | 67,47 | +4,02 [+0,40; +7,63] | 16 / 6 | 71,89 | 81,93 | 74,70 | 74,30 | 98,39 |

**Thước chữ**

| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---:|---:|---:|---:|---:|---:|---:|
| S1/101 | 53,32 | 38,95 | 70,85 | 454,38 | 48,62 | 63,13 | 69,80 |
| ck500 | 54,64 | 39,56 | 70,91 | 445,16 | 49,05 | 64,13 | 69,28 |
| TAGE gold | 52,10 | 38,26 | 70,41 | 433,68 | 47,57 | 62,35 | 69,36 |
| TAGE neg | 30,33 | 25,56 | 56,03 | 199,33 | 28,23 | 45,57 | 54,42 |
| TAGE none | 51,59 | 37,70 | 70,24 | 438,04 | 47,55 | 61,68 | 69,12 |
| TAGE pred | 47,20 | 35,41 | 67,01 | 383,67 | 43,75 | 58,97 | 66,64 |
| TAGE none+cổng | 55,07 | 39,63 | 72,59 | 470,69 | 49,52 | 64,28 | 70,75 |
| **TAGE pred+cổng** | 54,88 | 39,83 | 71,64 | 446,53 | 49,50 | 64,40 | 69,95 |

Ghi chú bảng:
- Số exec: S1/101 và ck500 chấm trên T4 (lượt 251/254); các nhánh TAGE chấm trên L4. Câu giữ nguyên câu
  nháp trong nhánh +cổng dùng kết quả chấm T4 của ck500. Chấm lại cùng môi trường L4: S1 157, ck500 166.
- τ chọn chéo: pred+cổng 0,738 · 0,961 (nhận 8 câu sửa); none+cổng −0,007 · −0,071 (nhận 102 câu sửa).

**So với ck500** (mốc mà TAGE sửa từ đó, `tage_doc.py`):

| nhánh | exec / 249 | Δ vs ck500 | KTC95 | cứu / phá |
|---|---:|---:|---|---|
| gold | 184 | +7,63 | [+2,41; +12,85] | 29 / 10 |
| gold+cổng | 184 | +7,63 | [+2,81; +12,45] | 26 / 7 |
| neg | 60 | −42,17 | [−50,20; −34,14] | 12 / 117 |
| none | 164 | −0,40 | [−4,82; +3,61] | 11 / 12 |
| none+cổng | 169 | +1,61 | [−1,61; +4,82] | 9 / 5 |
| pred | 158 | −2,81 | [−8,03; +2,41] | 14 / 21 |
| pred+cổng | 168 | +1,20 | [−0,40; +3,61] | 4 / 1 |

### 3.5 Phân rã theo việc vùng cắt đoán có chứa phần tử vàng

| tập | n | S1/101 | ck500 | gold | pred | none |
|---|---:|---:|---:|---:|---:|---:|
| vàng trong vùng cắt `loc_g` | 196 | — | 153 | 159 | 156 | 151 |
| vàng ngoài vùng cắt `loc_g` | 53 | — | 12 | 25 | 2 | 13 |

- 53 bước ngoài vùng chứa 41 bước ck500 sai, trong đó 29 bước thuộc nhóm 52 bước không câu S1 nào đúng.
- 29 bước gold cứu (so ck500): 27 thuộc nhóm trỏ sai phần tử, 2 thuộc nhóm sai loại thao tác; 10 bước thuộc
  nhóm 52 bước không câu S1 nào đúng.
- Nếu chỉ nhận câu pred ở đúng các bước vàng nằm trong vùng cắt (cổng biết trước): 168/249.

## 4. Tóm tắt số

**Test (4.463 bước click):** ck500 − S1/101: exec **+1,55** [+0,80; +2,33], SPICE **+1,42** [+0,69; +2,16],
cao hơn ở 13/13 cột; bước không chạm −1,68 (scroll −6,23).

**Val C1 (249 bước click), so S1/101 (63,45):**

| hệ | exec | Δ | KTC95 |
|---|---:|---:|---|
| ck500 | 66,27 | +2,81 | [−0,40; +6,02] |
| TAGE pred+cổng (hệ chạy thật) | 67,47 | +4,02 | [+0,40; +7,63] |
| TAGE none+cổng (viết lại, không vùng cắt) | 67,87 | +4,42 | [+1,61; +7,63] |
| TAGE gold (vùng cắt từ điểm vàng) | 73,90 | +10,44 | [+5,62; +15,66] |

## 5. Giới hạn của các phép đo

- Mọi số TAGE là số val, 249 bước, một hạt giống, mỗi thành phần 1 epoch; chưa chấm test.
- Val C1 tách từ tập dạy của S1/ck500 (theo episode, đã loại khỏi tập dạy của TAGE nhưng S1/ck500 đã
  thấy) ⇒ số tuyệt đối trên val cao hơn test; dùng để so các nhánh với nhau.
- Hai môi trường chấm (T4 fp16 / L4 bf16) lệch ±1 bước trên 249.
- Nhánh gold dùng điểm vàng lúc suy luận; không phải hệ triển khai được.
- ck500 trên test: một hạt giống; chưa có nhánh "train thêm cùng số bước không GRPO"; đường sinh khác S1
  công bố (16/20 câu trùng khi kiểm).

## 6. Trạng thái và các hướng cải thiện đã đề xuất

**TAGE chưa chạy trên tập test** (3/10). Runbook Kaggle dạng commit đã sẵn: `harness/kaggle_tage_test.md`,
gói `_bundles/tage-test-script/` (thêm chế độ `--rows/--shard` cho `tage_val.py`, tệp `test_rows.jsonl`
4.463 hàng click). Thiết kế: τ chọn trên toàn bộ 249 bước val (`τ_pred = 0,73767`, `τ_none = −0,04327`) rồi áp
nguyên lên test; chỉ chấm UGround những câu cổng nhận sửa, phần còn lại gộp từ chấm ck500 test đã có (cùng
`score_run.py`, cùng T4). Commit 1 = nhánh pred; commit 2 (tuỳ chọn) = nhánh none.

**Đã thử, không tốn GPU, không giúp:** cổng theo đồng thuận hai bộ định vị (nhận câu pred khi `loc_g` và
`loc_d` chỉ cùng chỗ, ngưỡng 0,02/0,05/0,1 thang chuẩn hoá) ⇒ exec 161–162/249, thấp hơn ck500 165. Kể cả trên
196 bước vùng cắt chứa phần tử vàng, câu pred cứu 14 phá 11 so ck500.

**Các hướng đề xuất, xếp theo chi phí** (thời gian là ước lượng, chưa đo):

| # | việc | nhắm vào (số đo trên val) | chi phí |
|---|---|---|---|
| 1 | Dạy bộ biên tập **giữ câu nháp khi câu nháp đã đúng**: chấm 2.554 câu nháp train bằng UGround; câu đã đúng thì đích = chính câu nháp | 11 bước bị phá dù vùng cắt chứa phần tử vàng | ~1 h chấm + ~4,8 h train L4 |
| 2 | Dạy bộ biên tập **chịu được vùng cắt sai**: thêm mẫu vùng cắt lệch (kiểu lỗi của bộ định vị), đích vẫn là câu chuẩn | 10 bước bị phá ở 53 bước vùng cắt sai | ~4,8 h train |
| 3 | Train `ed_gold` thêm epoch 2 (nll vàng ~0,50, biên hoạt 0,5–0,65, chưa bão hoà) | chất lượng sửa câu nói chung | ~4,8 h |
| 4 | Bộ định vị train trên ~41 nghìn bước click của tập dạy thay vì 2.554 | 53 bước bộ định vị không tìm ra phần tử (gold +13 ở đó) | nhiều giờ, chưa ước |
| 5 | **Chạy TAGE trên tập test** (runbook trên) | có số test, so S1/ck500 trên 4.463 bước | ~6–9 h Kaggle T4 ×2 (commit 1) |
| 6 | Cột *AitW cận trên* cho bảng val (cần mọi hộp bấm được của màn val) | đủ 13 cột như bảng test | 0 GPU |

## 7. Tệp

- GRPO: `runs/grpo_spice/` · `report/254`, `259`, `261`, `262`.
- TAGE: `runs/tage_val/that/` (score `*_raw.jsonl`, `pred_*_meta.jsonl`, `loc_val_*.jsonl`, log, `so_s1.json`)
  · `report/266` · action `harness/tai_lieu_2026-10-02/`.
- Adapter TAGE (`ed_gold`, `ed_none`, `loc_g`, `loc_d`) chỉ có trên Drive `MyDrive/thesis/tage/out/that/`.
- Gói Colab: `_bundles/tage-val-script/` (zip `_bundles/tage_colab.zip` bị gitignore, md5 `36919554…`).
