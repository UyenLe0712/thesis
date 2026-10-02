# 261 — Mười ba cột của bảng nhiều thước: GRPO SPICE ck500 so với S1/101 (2/10/2026)

Nguồn: 7 ảnh do chat Mac gửi 2/10 (zip `My Documents [02-10-2026 08_24]`, đã xoá sau khi chép), bản
chép OCR thô từng nằm ở `harness/extracted_text.md`. File này **sắp lại** bản chép đó, **sửa các chỗ
OCR đọc sai** (§0), và ghi **kết quả action §5 đã chạy trên WSL** (§4).

Quần thể: 4.463 bước click của tập kiểm, ghép cặp theo `(episode_id, step_id)`, cùng luật với
`thesis/chapters/bang_nhieu_thuoc.tex`. Số test, chấm một lần (action 258, `report/259`).

## 0. Chỗ bản chép OCR sai — đã sửa trong file này

| chỗ | OCR ghi | đúng | căn cứ |
|---|---|---|---|
| exec S1 / ck500 / Δ | 69,11 / 69,65 / +0,55 | **59,11 / 60,65 / +1,55** | `score_s1_seed101.json` · `score_ck500_test.json` · `report/259` |
| exec chặng ba | 69,07 | **60,07** | `report/144` |
| bước rỗng chung | (18716, 1) | **(18710, 1)** | tệp thô cả hai nhánh; mã BERTScore của Mac `assert` số sai này nên chạy nguyên văn sẽ dừng |
| action_ok chặng ba | 98,68 | **98,86** | tính lại từ tệp thô |
| ROUGE-L chặng ba | 68,64 | **68,54** | `runs/text_metrics_coco.json` |
| SPICE chặng ba | 42,60 | **42,50** | như trên |

Các sửa này không đổi kết luận so sánh nào của bản Mac (ck500 vẫn thấp hơn chặng ba ở ROUGE-L,
vẫn cao hơn ở SPICE).

## 1. Sáu cột vị trí (tính lại trên WSL, khớp bản Mac)

Bootstrap 10.000 lần, cụm = ứng dụng (1.091 cụm), đúng `score_run.cluster_bootstrap` qua `d3_ktc.ktc`.
KTC của Mac tự viết bootstrap nên lệch ở chữ số thứ hai (vd. ±14% trục [+0,89; +2,44] vs [+0,90; +2,46]);
dùng bản dưới đây vì cùng hàm với mọi KTC trong luận văn.

| cột | S1/101 | ck500 | Δ | KTC95 | phá / cứu | p McNemar |
|---|---:|---:|---:|---|---|---|
| AitW đầy đủ | 74,37 | 76,25 | +1,88 | [+1,17; +2,63] | 88 / 172 | 2,6e−7 |
| Hộp D.3 | 65,49 | 67,02 | +1,52 | [+0,77; +2,29] | 97 / 165 | 3,5e−5 |
| **exec** | 59,11 | **60,65** | **+1,55** | [+0,80; +2,33] | 90 / 159 | 1,6e−5 |
| ±14% theo trục | 67,24 | 68,90 | +1,66 | [+0,90; +2,46] | 98 / 172 | 8,9e−6 |
| AitW cận trên | 81,04 | 82,90 | +1,86 | [+1,17; +2,60] | 80 / 163 | 1,4e−7 |
| Đúng loại thao tác | 94,35 | 95,97 | +1,61 | [+1,17; +2,08] | 11 / 83 | 2,4e−13 |

## 2. Bảy cột chữ

| cột | S1/101 (kho) | ck500 | Δ | bản Mac ck500 |
|---|---:|---:|---:|---:|
| BLEU-4 | 51,56 | 52,36 | +0,80 | 52,36 |
| METEOR 1.5 | 36,79 | 37,92 | +1,13 | 37,91 |
| ROUGE-L | 67,35 | 68,36 | +1,01 | 68,34 |
| CIDEr-D | 416,12 | 430,05 | +13,93 | 430,04 |
| SPICE | 44,37 | 45,79 | +1,42 (KTC [+0,69; +2,16], `report/259`) | 45,79 |
| chrF | 61,26 | 62,87 | +1,61 | 62,86 |
| **BERTScore** (rescaled) | **66,33** | **67,07** | **+0,74** | chưa tính được |

⇒ Cả **13 cột** ck500 đều cao hơn S1/101. S1 tính lại trên WSL trùng **tuyệt đối** cả bảy số đã lưu
(kể cả 67,35 · 416,12 · 61,26 mà bản Mac lệch 0,01–0,02 vì khác công cụ chrF/Java); ck500 khớp bản
Mac trong 0,02. BERTScore thô 94,30 → 94,42 (+0,12), không tách được nhánh như mọi bản thô khác.
Hash `roberta-large_L17_no-idf_version=0.3.12(hug_trans=5.14.1)-rescaled`, trùng hash của 66,33;
4.463 câu, một câu rỗng chung (18710, 1) tính 0.

Năm cột COCO (BLEU-4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE) tính mức kho bằng `pycocoevalcap`
sau `PTBTokenizer`, đúng đường `text_metrics_coco.py`. chrF và BERTScore đúng hàm `tinh()` của
`text_metrics_them.py` (sacreBLEU chrF2; BERTScore `roberta-large` L17, idf=False, rescale, câu rỗng = 0).
Mã: `harness/ck500_text_metrics.py` → `runs/grpo_spice/text_metrics_ck500.json`. S1 tái lập số đã
lưu trước khi ghi ck500 (lệch > 0,025 là dừng).

## 3. Đặt cạnh dòng cao nhất đang in trong luận văn (chặng ba = GRPO `<point>`)

| cột | chặng ba | ck500 | ck500 hơn? |
|---|---:|---:|---|
| exec | 60,07 | **60,65** | có |
| D.3 | **67,04** | 67,02 | ngang |
| AitW đầy đủ | **77,30** | 76,25 | không |
| ±14% theo trục | **69,37** | 68,90 | không |
| AitW cận trên | **85,01** | 82,90 | không |
| Đúng loại thao tác | **98,86** | 95,97 | không |
| BLEU-4 | 49,86 | **52,36** | có |
| METEOR 1.5 | 37,31 | **37,92** | có |
| ROUGE-L | **68,54** | 68,36 | không |
| CIDEr-D | 402,91 | **430,05** | có |
| SPICE | 42,50 | **45,79** | có |
| chrF | 61,88 | **62,87** | có |
| BERTScore | 66,85 | **67,07** | có |

Số chặng ba lấy từ tệp đã lưu (`luat_d3.json` · `luat_aitw_*.json` · `text_metrics_*.json`). ck500 hơn
ở exec và sáu cột chữ; thua ở bốn cột vị trí lỏng + ROUGE-L; D.3 ngang. exec ck500 − chặng ba
= +0,58 [−0,50; +1,69], p = 0,31 (`report/259`) ⇒ **không** hơn có ý nghĩa.

## 4. Action §5 của bản Mac (BERTScore) — ĐÃ CHẠY trên WSL 2/10

Bản Mac không cài được `torch` nên để trống BERTScore và đề nghị chat khác chạy. Máy WSL có sẵn
môi trường đã sinh số 66,33 của luận văn (`bert_score` 0.3.12 · transformers 5.14.1 · torch 2.8 CPU)
⇒ chạy ngay, không cần Kaggle.

- Lệnh: `~/.venvs/thesis/bin/python harness/ck500_text_metrics.py` (~13 phút CPU, hai nhánh).
- Điều kiện của bản Mac, đối chiếu:
  1. 4.463 khoá, hai tập bằng nhau — đạt (`load()` assert 4.463, cùng quần thể `report/259`).
  2. `roberta-large` L17, idf=False, lang en, rescale — đạt (hash ở §2).
  3. Câu rỗng giữ, F1 rescale ép 0 — đạt; bước rỗng là **(18710, 1)**, không phải (18716, 1).
  4. S1 tái lập 66,33 ±0,02 — **đạt, ra đúng 66,33**.
  5. Trả về: S1 **66,33** · ck500 **67,07** · Δ **+0,74** · n 4.463.
- Dòng điền vào bảng: `| BERTScore | 66,33 | 67,07 | +0,74 | |`

## 5. Thứ tự việc sau file này (theo bản Mac, kèm tình trạng)

1. ~~Đóng cột BERTScore~~ — **xong** (§4).
2. **Chấm 2.495 bước không chạm** (nhất là scroll) — phép kiểm cuối cho tác dụng phụ. Cần sinh câu
   ck500 cho 2.495 bước trên Kaggle T4 (~2 h), chấm `score_run.py --mode noharm` 0 GPU ở máy nhà.
   Gói ảnh `test_images_nontap.tar` (2.495 ảnh, 1,65 GB) **đã chép từ `/tmp` cũ ra
   `_bundles/test_images_nontap.tar`** (gitignore), chưa lên dataset Kaggle. **Runbook: `harness/kaggle_grpo_spice_nontap_ck500.md`** (luật đọc khoá trong đó) · đọc bằng `harness/grpo_spice_nontap_doc.py`. Mốc S1: 85,97 toàn bộ · scroll 83,97.
3. Khi scroll không giảm quá 3 điểm so với S1 ⇒ chốt ck500 là mô hình cuối.
4. Sửa luận văn: thêm hàng ck500 vào hai bảng 13 thước; bỏ sàn MDE 2,2 khỏi luật quyết định; báo KTC
   ghép cặp; ghi rõ một hạt giống và **không chạy S1-hoà theo quyết định ngày 2/10** (bản Mac ghi;
   tức đề xuất §5.1 của `report/259` đã bị bác).
5. Dừng train. Không chạy lại test, không đổi checkpoint.

## 6. KẾT QUẢ bước KHÔNG chạm (2/10, Kaggle T4 2,0 h + đọc WSL) — ⛔ SCROLL RỚT

Tệp: `runs/grpo_spice/pred_ck500_test_nontap.jsonl` (2.495 câu, 0 rỗng, `[điểm lưu] …grpo-spice-ck500`,
2,94 s/bước) · `nontap_ck500_doc.json`. Kiểm hoà 20 bước không chạm: **20/20** S1-hoà trùng S1 công bố
(ở bước click là 16/20) ⇒ lẫn biến đường sinh ở đây gần như không có, Δ dưới đây là của GRPO.

Thước: `canon_action(câu) == canon_action(câu chuẩn)`, `strict_back`, cụm app, ghép cặp.

| nhóm | n | S1/101 | ck500 | Δ | KTC95 | phá / cứu |
|---|---:|---:|---:|---:|---|---|
| **toàn bộ** | 2.495 | 85,97 | 84,29 | **−1,68** | [−2,76; −0,62] | 108 / 66 |
| **scroll** | 755 | 83,97 | 77,75 | **−6,23** | [−8,30; −4,31] | 51 / 4 |
| navigate_back | 270 | 72,96 | 67,04 | −5,93 | [−9,42; −2,58] | 19 / 3 |
| input_text | 494 | 81,58 | 79,55 | −2,02 | [−5,59; +1,42] | 36 / 26 |
| wait | 505 | 90,69 | 95,25 | +4,55 | [+2,56; +6,73] | 2 / 25 |
| open_app | 469 | 96,16 | 97,87 | +1,71 | [+0,65; +2,94] | 0 / 8 |

**Luật khoá trước:** toàn bộ cận dưới −2,76 ≥ −3 ⇒ ĐẠT (sát ngưỡng) · scroll Δ −6,23 < −3 ⇒ **RỚT**
⇒ **không chốt ck500 là mô hình cuối theo §5.3; phải khai là tác hại ở bước không chạm.**

**Cơ chế (đo):** ck500 dịch thiên hướng về câu *chạm*.
- 51 bước scroll bị phá: 47 thành câu chạm (*"Swipe up"* → *"Click on technology"*), 4 thành quay lại.
  Câu ck500 quy về chạm trên 755 bước scroll: S1 117 → ck500 167.
- 19/19 bước quay lại bị phá thành câu chạm, phần lớn *"Open the X app"* / *"Go to … tab"*.
- input_text: *"Type X in the search bar"* → *"Search for X"* (quy về chạm) ở 32/36 bước phá.
- Hai nhóm "được" cũng là cùng một dịch chuyển: wait có câu chuẩn phần lớn là câu chạm, ck500 cứu
  25 bước mà S1 viết *swipe*; ở bước click (`report/259`) chính dịch chuyển này là +28 bước action_ok.
- Theo toàn tập kiểm 6.958 bước, ròng đúng loại thao tác: bước click +72 (83/11), bước không chạm
  −42 (66/108) ⇒ +30 bước. **Một nửa mức tăng action_ok ở bước click được trả lại ở bước không chạm.**

**Đã loại:** "thưởng SPICE mù ở câu ngắn kiểu *Swipe up*" — SPICE câu chuẩn tự so ở 101 bước scroll
có câu chuẩn ≤ 3 từ chỉ 6,9 (đúng là mù), nhưng mức giảm không dồn vào nhóm đó (−7,9 vs −6,0 ở câu
dài). Trên bước scroll SPICE còn **thưởng câu scroll cao hơn** câu chạm (ck500 66,3 vs 14,0) ⇒ thưởng
tại bước scroll không đẩy về chạm. Tập câu nhắc GRPO có đủ loại thao tác (4.000 dòng: click 2.549 ·
scroll 445 · wait 292 · input_text 286 · open_app 276 · navigate_back 144). [suy] Dịch chuyển học từ
64% câu nhắc click, nơi sửa *swipe → click* được thưởng, rồi lan sang thiên hướng chung.

**Hệ quả cho luận văn (chờ chat lập kế hoạch quyết):** ck500 vẫn hơn S1 ở 13 cột bước click, nhưng
không đạt điều kiện chốt mô hình cuối. Cách trình hợp lệ: báo ck500 như một nhánh RL thưởng metric
câu, in **kèm** hàng bước không chạm (scroll −6,23) cạnh mọi số bước click — đúng cam kết noharm
của `report/106` mục 3. Tiêu đề 60,07 (GRPO-point) chưa có số bước không chạm để so ((x20b) vẫn nợ).

## Phụ lục — bản Mac

Script `_so_metric_ck500.py` và `_exports/so_metric_ck500.json` nằm ngoài clone trên máy Mac
(Java Corretto 11, venv `~venv_go`); chrF ở đó tính bằng công thức tự viết vì không cài được
sacreBLEU, nên S1 ra ROUGE-L 67,33 · CIDEr-D 416,11 · chrF 61,25 (kho lưu 67,35 · 416,12 · 61,26).
Mã Python trong ảnh (sáu cột vị trí, bootstrap tự viết seed 101, McNemar nhị thức chính xác) dùng
cùng `luat_d3.luat` · `luat_aitw_day_du.aitw_full` · `luat_aitw_moi_hop.aitw_moi_hop` như §1, nên
không chép lại; đoạn BERTScore của Mac được thay bằng `harness/ck500_text_metrics.py`.
