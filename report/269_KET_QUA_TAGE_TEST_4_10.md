# Kết quả TAGE pred+cổng trên tập test (4/10/2026)

Nguồn: Kaggle commit theo `harness/runbook/kaggle_tage_test.md`, tệp ở `runs/tage_test/`. Đọc bằng
`harness/tage_test_doc.py` (0 GPU, ~2 phút, tự kiểm đạt), số ghi ở `runs/tage_test/tage_test_doc.json`.
Thiết kế: câu nháp ck500 → bộ định vị `loc_g` → vùng cắt 40% → bộ biên tập `ed_gold` → cổng
lp_edit − lp_draft > τ = 0,73767 (**chọn trên val, không chỉnh trên test**). Bước cổng không nhận giữ kết
quả chấm ck500 test đã có; 219 bước cổng nhận được chấm mới (cùng `score_run.py`, cùng T4).

## 1. Kết luận

- **TAGE không hơn câu nháp của chính nó trên test.** exec 60,23 so với ck500 60,65: Δ **−0,43**
  [−0,87; +0,02], p=0,093 (cứu 48, phá 67). Dưới D.3 thua có ý nghĩa: −0,58 [−1,07; −0,09], p=0,027.
- So S1/101 thì TAGE hơn: +1,12 [+0,31; +1,94], p=0,007. Nhưng toàn bộ phần hơn đó đến từ ck500
  (+1,55 so S1, `report/259`); khâu sửa câu lấy bớt đi 0,43.
- Mức tăng trên val (+1,20 so ck500: 67,47 vs 66,27, `report/267`) **không lặp lại trên test**. Nguyên nhân đo
  được ở §3: τ chọn từ 11 câu trên val, và trên test tín hiệu cổng lại chọn đúng những bước bộ định vị trỏ sai.

## 2. Bảng 4.463 bước click (ghép cặp; KTC95 bootstrap cụm = app, như mọi KTC trong luận văn)

| thước | S1/101 | ck500 | **TAGE** | TAGE − S1 | p | TAGE − ck500 | cứu / phá | p |
|---|---|---|---|---|---|---|---|---|
| exec (tiêu đề) | 59,11 | 60,65 | **60,23** | +1,12 [+0,31; +1,94] | 0,007 | −0,43 [−0,87; +0,02] | 48 / 67 | 0,093 |
| D.3 | 65,49 | 67,02 | **66,44** | +0,94 [+0,11; +1,80] | 0,029 | −0,58 [−1,07; −0,09] | 51 / 77 | 0,027 |
| AitW đầy đủ | 74,37 | 76,25 | **76,07** | +1,70 [+0,88; +2,55] | 7e−5 | −0,18 [−0,66; +0,32] | 63 / 71 | 0,55 |
| ±14% theo trục | 67,24 | 68,90 | **68,74** | +1,50 [+0,66; +2,37] | 5e−4 | −0,16 [−0,65; +0,34] | 63 / 70 | 0,60 |
| action_ok | 94,35 | 95,97 | **96,64** | +2,29 | 3e−20 | +0,67 [+0,44; +0,92] | 30 / 0 | 1e−7 |
| SPICE | 44,37 | 45,79 | **45,74** | +1,37 [+0,61; +2,13] | – | −0,05 [−0,38; +0,27] | – | – |

Mọi số chung một quần thể 4.463 bước, một hạt giống. Cột action_ok tăng vì bộ biên tập luôn viết câu bấm:
30 câu nháp mở đầu bằng swipe/go back/scroll/type được đổi thành câu click.

## 3. Vì sao khâu sửa câu lấy bớt điểm

**Đường ống chạy đúng.** Bộ định vị trỏ trúng (±14%) 3.103/4.463 = 69,5% (val 77,5%), 0 bước không đọc được
toạ độ. Bộ biên tập đổi câu ở 70,8% số bước, 0 câu tiếng Việt. Cổng nhận 219/4.463 = 4,91% (val 4,4%). Tốc độ
T4: định vị 2,9–3,0 s/bước, sửa 7,4–7,8 s/bước, chấm 0,26 bước/s.

**Riêng 219 bước cổng nhận:** exec của ck500 ở đó chỉ 34,7% (76/219), tức cổng có chọn đúng những bước câu
nháp yếu. Nhưng câu sửa còn tệ hơn: 26,0% (57/219).

| 219 bước cổng nhận (tách theo điểm vàng, chỉ để chẩn đoán) | n | exec ck500 → TAGE | cứu | phá |
|---|---|---|---|---|
| bộ định vị trỏ trúng | 80 | 16 → 55 | 46 | 7 |
| bộ định vị trỏ sai | 139 | 60 → 2 | 2 | 60 |

Khi vùng cắt đúng, câu sửa thắng rõ (+39 bước). Khi vùng cắt sai, bộ biên tập tả phần tử nằm trong vùng cắt
sai, nên phá gần hết các câu nháp vốn đúng (−58 bước). Các ví dụ trong log khớp đúng kiểu này: câu nháp
"Click on the Richard contact." (trúng) bị thay bằng "Click on the + icon at the bottom right of the screen.".

**Tín hiệu cổng chọn ngược.** Tỉ lệ bộ định vị trỏ trúng giảm dần khi Δlp tăng:

| Δlp = lp_edit − lp_draft (câu bị đổi) | ≤ 0 | (0; 0,4] | (0,4; 0,74] | > 0,74 (cổng nhận) |
|---|---|---|---|---|
| test: bộ định vị trúng | 74,0% (n=1.214) | 67,7% (1.439) | 44,8% (290) | **36,9% (217)** |
| val: bộ định vị trúng | 86,2% (58) | 70,2% (94) | 54,5% (11) | 72,7% (11) |

Trên val, 11 câu cổng nhận tình cờ có 8 câu vùng cắt đúng (cứu 6, phá 0), nên τ trông tốt. Ba nhóm Δlp thấp
hơn của val đã cho cùng xu hướng giảm như test; nhóm trên cùng của val chỉ có 11 câu nên lệch khỏi xu hướng.
Diễn giải [suy]: khi vùng cắt rơi vào phần tử khác, bộ biên tập viết một câu rất chắc về phần tử *trong vùng cắt*,
nên lp_edit cao; lp_draft thì thấp vì câu nháp nói về phần tử nằm ngoài vùng cắt. Hiệu Δlp vì vậy đo mức
*lệch giữa câu nháp và vùng cắt*, không đo câu nào đúng hơn.

**Không dùng được bảng trên để chỉnh lại cổng.** Tách theo "bộ định vị trúng" cần điểm vàng; mọi cổng mới chọn
sau khi đã thấy test là chọn trên test. Con số "chỉ nhận khi vùng cắt đúng ⇒ +39 bước ≈ +0,87 pp" là **trần
chẩn đoán**, không phải kết quả.

## 4. Đặt cạnh các hệ khác (exec, test, 4.463 bước)

S1/101 59,11 · S1/202 59,62 · MIN-DESC 60,05 · GRPO-point 60,07 · **TAGE 60,23** · ck500 60,65 · câu chuẩn 75,73.
TAGE nằm trong dải các hệ một hạt giống, dưới MDE 2,11 so S1, và dưới chính ck500.

## 5. Hệ quả cho các hướng ở `report/267` §6

- Hướng 2 (dạy bộ biên tập chịu vùng cắt sai) nay có số đo trực tiếp: 139 bước vùng cắt sai trong nhóm cổng
  nhận gây −58 bước, đây là điểm nghẽn chính.
- Hướng 4 (bộ định vị tốt hơn) đánh vào cùng chỗ: test trúng 69,5%, thấp hơn val 77,5%.
- Cổng log-prob của chính bộ biên tập không đủ: cần một tín hiệu độc lập với vùng cắt. Ứng viên rẻ: so điểm
  UGround trỏ từ câu nháp (đã có trong `score_ck500_test_raw.jsonl`) với toạ độ của bộ định vị. Cổng này
  **phải chọn trên val** rồi mới áp lên test.
- Commit 2 (nhánh `none`, không vùng cắt) chưa chạy. Trên val nó hơn pred (67,87 vs 67,47) và không chịu lỗi
  vùng cắt sai, nhưng cổng `τ_none` cũng chọn trên val (108 câu) nên cùng rủi ro không chuyển sang test.
  Tốn ~3–4 h T4, hỏi user trước.

## 6. Giới hạn

Một hạt giống; cổng chọn trên 249 bước val (11 câu nhận); chẩn đoán §3 dùng điểm vàng nên chỉ để giải thích.
Chấm cùng T4 fp16 với ck500 nên phần gộp không lẫn dụng cụ.
