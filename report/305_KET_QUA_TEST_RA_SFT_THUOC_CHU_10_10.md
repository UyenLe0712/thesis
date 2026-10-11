# 305 — Kết quả test RA-SFT (304): bảy thước chữ, chờ exec (10/10/2026)

Nối tiếp `report/304` (val + luật ghép chọn-khi-chép). File này ghi phần **đã có số trên test**: sinh câu
`ra_k4` (notebook G) và chấm bảy thước chữ. Phần exec / D.3 / AitW **đang chờ** Kaggle `ra-exec-test-304`,
đọc bằng `_scripts/304/kiem/doc_exec_304.py` khi tải về (mục 5).

## 1. Đã chạy gì

| bước | nơi | thời gian | tệp |
|---|---|---|---|
| sinh `ra_k4` trên 4.463 bước click test, chia 2 GPU (2.232 + 2.231) | Kaggle T4×2 (notebook G) | 2,16 h · 3,33 và 2,98 s/bước | `runs/ra304_G/pred_ra_k4_test.jsonl` (rỗng 0) |
| ghép chọn-khi-chép (luật khoá ở `report/304` §3.3, **trước** khi có số test) | WSL, 0 GPU | vài giây | `runs/ra304_G/pred_ghep_test.jsonl` |
| chấm 7 thước chữ (ck500 · `ra_k4` · `ghep`) | Kaggle CPU, hai lượt độc lập | 10 phút / 18 phút | `runs/ra304_G/cham_test/` · `runs/ra304_G/cham_cpu/` |

- Hai lượt chấm (`cham_test`, `cham_cpu`) cho **cùng số đến hai chữ số** ở cả ba nhánh.
- Tự kiểm: điểm ck500 tái lập số đã công bố (`report/261`, `report/299`), lệch ≤ 0,02 ở mọi thước.
- Chạy lại `ghep_test_304.py` trên WSL ra tệp **trùng từng byte** với `pred_ghep_test.jsonl`.
- `cham_cpu_v1/` là lượt hỏng (lỗi cú pháp ký tự `·` trong lệnh `python -c`), không có số; bỏ qua.

## 2. Bảy thước chữ trên 4.463 bước click test [đo]

| thước | ck500 | `ra_k4` | `ghep` |
|---|---:|---:|---:|
| BLEU-4 | 52,36 | 53,47 (+1,11) | 53,47 (+1,11) |
| METEOR | 37,91 | 37,79 (−0,12) | 38,33 (+0,42) |
| ROUGE-L | 68,34 | 68,67 (+0,33) | 68,97 (+0,63) |
| CIDEr-D | 430,04 | 437,54 (+7,50) | 441,53 (+11,49) |
| SPICE | 45,79 | 46,79 (+1,00) | 47,12 (+1,33) |
| chrF | 62,86 | 62,65 (−0,21) | 63,39 (+0,53) |
| BERTScore (rescaled) | 67,07 | 67,52 (+0,45) | 67,66 (+0,59) |
| số thước cao hơn ck500 | — | **5/7** | **7/7** |
| câu trùng nguyên văn câu chuẩn | 22,8% | 24,9% | 24,7% |
| câu rỗng | 1 | 0 | 1 |

Đếm câu đổi so với ck500 (hai cách đếm, đều đúng theo định nghĩa của chúng):

| | so từng byte (WSL) | sau tách từ (`ra_score.py`) |
|---|---:|---:|
| `ra_k4` khác ck500 | 2.229 bước (49,9%) | 43,3% |
| `ghep` khác ck500 | 453 bước (10,2%) | 8,8% |

- Luật ghép lấy câu `ra_k4` ở 846 bước (19,0%, câu trùng một trong 4 ví dụ của khối); 393 trong số đó câu
  `ra_k4` vốn đã trùng ck500, nên `ghep` chỉ thật sự đổi 453 câu.
- Chẩn đoán chép của `ra_k4`: chép nguyên văn một ví dụ ở 19,1% bước, **43,5%** số câu chép đúng câu chuẩn
  (val: 21,0% và 41,0%) ⇒ không phải chép mù.
- BLEU-4 của `ra_k4` và `ghep` trùng nhau ở 53,47 là trùng khi làm tròn, không phải cùng tệp (hai tệp khác
  nhau ở ~1.800 câu; các thước khác lệch nhau).

## 3. Đọc

- **Theo luật action 304 (≥ 4/7 thước chữ cao hơn ck500): cả hai nhánh ĐẠT.** `ra_k4` 5/7, `ghep` 7/7.
- **Test khác val ở `ra_k4`.** Trên val `ra_k4` chỉ hơn ck500 ở 1/5 thước (CIDEr-D); trên test hơn ở BLEU-4,
  ROUGE-L, CIDEr-D (và thêm SPICE, BERTScore vốn không chấm ở val). METEOR và chrF vẫn thua như ở val.
  Val lớn có tác vụ S1 đã thấy và chỉ 1.002 bước, nên lệch chiều giữa val và test ở mức ±1 điểm là
  trong tầm nhiễu đã biết của val (`CLAUDE.md`, khối 9/9 V2: val phóng đại khoảng cách giữa nhánh).
- **Luật ghép đứng được trên test.** Luật được khoá sau val nhưng **trước** test, một biến thể duy nhất, và
  trên test lặp lại đúng kết quả val (5/5 → 7/7, CIDEr-D +13,95 val → +11,49 test). Đây là phép xác nhận
  hợp lệ, không phải chọn trên test.
- Mức tăng lớn nhất nằm ở CIDEr-D và SPICE, nhỏ ở các thước còn lại; nhất quán với cơ chế "chép đúng lúc":
  câu chép đúng là câu trùng nguyên văn câu chuẩn (22,8% → 24,7%), thứ CIDEr-D thưởng mạnh nhất.
- So các lượt train thêm sau ck500 trên test: A2_500 (`runs/a2_test299/doc_299_bert.log`) chỉ hơn ck500
  ở 3/7 thước, chênh ≤ +0,23, và thua CIDEr-D −1,78 · chrF −1,10; đây là lượt đầu tiên tăng rõ thước chữ
  trên test so với ck500.

⚠️ Chưa có:
- **KTC cho thước chữ.** Mọi Δ ở mục 2 là điểm cấp kho, chưa bootstrap; Δ cỡ +0,3…+0,6 (ROUGE-L, chrF,
  METEOR, BERTScore) chưa nói được là hơn thật. Chỉ "đạt luật đếm thước", chưa phải "hơn có ý nghĩa".
- **exec / D.3 / AitW** — thước tiêu đề. Thước chữ tăng không bảo đảm exec tăng (tiền lệ: GRPO-point khai
  báo +2,56 mà exec +0,02; CTG/A2 thước chữ và exec đi lệch nhau).
- Một hạt giống, một lượt train.

## 4. Kỳ vọng exec [suy]

- `ghep` chỉ đổi 453 câu so với ck500 ⇒ trần dịch chuyển exec tối đa ~±10 điểm, thực tế nhỏ hơn nhiều; câu
  đổi lại phần lớn là câu chép đúng câu chuẩn (exec câu chuẩn 75,7 vs ck500 60,65) nên chiều kỳ vọng là
  dương nhẹ.
- `ra_k4` đổi ~2.229 câu, gồm cả phần câu mới mà trên val đã làm thước chữ giảm ⇒ khó đoán chiều.
- Không đặt ngưỡng trước cho exec; đọc bằng KTC ghép cặp + McNemar như `report/299`.

## 5. Khi exec về

```
python3 _scripts/304/kiem/doc_exec_304.py runs/ra304_G/exec_out
```

Script tự kiểm: 40 câu ck500 chấm lại phải trùng toạ độ tệp thô cũ, ck500 exec phải ra 60,65, tập bước được
chấm mới phải đúng bằng tập câu khác ck500 (so từng byte: 453 với `ghep`, 2.229 với `ra_k4`). In exec · D.3 ·
AitW kèm KTC cho ck500 / `ra_k4` / `ghep` / S1/101 và bốn phép so ghép cặp; ghi `doc_exec_304.json`.
Điền kết quả vào mục 6 file này.

## 6. Kết quả exec

(chờ)
