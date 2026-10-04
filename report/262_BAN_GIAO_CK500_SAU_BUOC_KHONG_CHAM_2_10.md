# 262 — Bàn giao: GRPO SPICE ck500 sau phép kiểm bước không chạm (2/10/2026)

Cho chat lập kế hoạch. Tự chứa. Gom ba lượt trong ngày 2/10: chấm test bước click (`report/259`),
đủ 13 cột (`report/261` §1–4), bước không chạm (`report/261` §6). **Mọi số là số test, chấm một lần.**

## 1. Kết luận một đoạn

ck500 (GRPO thưởng SPICE trên S1/101) **hơn S1/101 ở cả 13 cột** trên 4.463 bước click (exec +1,55
[+0,80; +2,33]), nhưng **rớt phép kiểm bước không chạm ở scroll** (Δ −6,23 [−8,30; −4,31], ngưỡng −3
khoá trước). Theo luật `report/261` §5.3 ⇒ **không chốt ck500 là mô hình cuối**; nếu đưa vào luận văn
thì phải in kèm tác hại ở bước không chạm. Cơ chế của cả mức tăng lẫn tác hại là **một**: ck500 nghiêng
về câu "chạm vào X".

## 2. Bước click (4.463 bước, so S1/101, ghép cặp, KTC cụm app)

| cột | S1/101 | ck500 | Δ | KTC95 |
|---|---:|---:|---:|---|
| **exec** | 59,11 | **60,65** | **+1,55** | [+0,80; +2,33] p = 1,6e−5 |
| D.3 | 65,49 | 67,02 | +1,52 | [+0,77; +2,29] |
| AitW đầy đủ | 74,37 | 76,25 | +1,88 | [+1,17; +2,63] |
| ±14% theo trục | 67,24 | 68,90 | +1,66 | [+0,90; +2,46] |
| AitW cận trên | 81,04 | 82,90 | +1,86 | [+1,17; +2,60] |
| đúng loại thao tác | 94,35 | 95,97 | +1,61 | [+1,17; +2,08] |
| BLEU-4 | 51,56 | 52,36 | +0,80 | |
| METEOR 1.5 | 36,79 | 37,92 | +1,13 | |
| ROUGE-L | 67,35 | 68,36 | +1,01 | |
| CIDEr-D | 416,12 | 430,05 | +13,93 | |
| **SPICE** | 44,37 | **45,79** | **+1,42** | [+0,69; +2,16] |
| chrF | 61,26 | 62,87 | +1,61 | |
| BERTScore | 66,33 | 67,07 | +0,74 | |

- So các nhánh khác (exec): − GRPO-point 60,07 **+0,58 p = 0,31** · − MIN 60,05 +0,60 p = 0,30 ·
  − S1/202 59,62 +1,03 p = 0,014. So chặng ba (GRPO-point) trên 13 cột: ck500 hơn ở exec + 6 cột chữ,
  thua 4 cột vị trí lỏng + ROUGE-L, D.3 ngang.
- Phân rã Δexec: sửa loại thao tác +28 bước · đổi phần tử (cả hai đúng loại) +41 bước.
- S1 tính lại trên WSL trùng tuyệt đối mọi số đã lưu (exec, KTC, 7 cột chữ kể cả BERTScore 66,33).

## 3. Bước KHÔNG chạm (2.495 bước, đúng loại thao tác, `canon_action` strict_back)

| nhóm | n | S1/101 | ck500 | Δ | KTC95 | phá / cứu |
|---|---:|---:|---:|---:|---|---|
| toàn bộ | 2.495 | 85,97 | 84,29 | −1,68 | [−2,76; −0,62] | 108 / 66 |
| **scroll** | 755 | 83,97 | 77,75 | **−6,23** | [−8,30; −4,31] | 51 / 4 |
| navigate_back | 270 | 72,96 | 67,04 | −5,93 | [−9,42; −2,58] | 19 / 3 |
| input_text | 494 | 81,58 | 79,55 | −2,02 | [−5,59; +1,42] | 36 / 26 |
| wait | 505 | 90,69 | 95,25 | +4,55 | [+2,56; +6,73] | 2 / 25 |
| open_app | 469 | 96,16 | 97,87 | +1,71 | [+0,65; +2,94] | 0 / 8 |

Luật khoá trước (runbook `harness/runbook/kaggle_grpo_spice_nontap_ck500.md`): toàn bộ cận dưới ≥ −3 ⇒
**ĐẠT sát** (−2,76) · scroll Δ ≥ −3 ⇒ **RỚT** (−6,23).

## 4. Cơ chế (đo)

- Scroll: 47/51 bước phá thành câu chạm (*"Swipe up"* → *"Click on technology"*); câu quy về chạm
  trên 755 bước scroll 117 → 167. Back: 19/19 bước phá thành câu chạm (*"Open the X app"*).
  input_text: *"Type X in the search bar"* → *"Search for X"* (quy về chạm).
- Wait **tăng** vì cùng lý do: câu chuẩn ở bước wait phần lớn là câu chạm.
- Toàn tập 6.958 bước, ròng đúng loại thao tác: click +72 · không chạm −42 ⇒ **gần một nửa mức tăng
  action_ok ở bước click bị trả lại ở bước không chạm.**
- Đã loại "SPICE mù với câu ngắn": SPICE câu chuẩn tự so ở câu scroll ≤ 3 từ chỉ 6,9 (đúng là mù),
  nhưng mức giảm không dồn vào đó (−7,9 vs −6,0); trên bước scroll SPICE thưởng câu scroll **cao hơn**
  câu chạm (66,3 vs 14,0). Tập câu nhắc GRPO có đủ loại thao tác (click 2.549/4.000, scroll 445…).
  [suy] Thiên hướng học từ 64% câu nhắc click, nơi sửa *swipe → click* được thưởng, rồi lan chung.

## 5. Độ tin của đường đo

- Sinh: S1 hoà fp16 + ck500 (md5 `491fa667…`), greedy 96 token. Kiểm hoà: click **16/20**, không chạm
  **20/20** ⇒ ở bước không chạm lẫn biến đường sinh gần như không có; ở bước click còn (quyết 2/10:
  không chạy S1-hoà đủ tập).
- Một hạt giống; Δexec +1,55 trong dải "trắng" −2,8…+1,7 của ch4 và dưới MDE 2,11.
- Chưa có nhánh "train thêm cùng số bước không GRPO".

## 6. Cần quyết

1. **Vai của ck500 trong luận văn.** Khuyến nghị: báo như một nhánh RL thưởng metric câu cạnh GRPO-point,
   in hàng bước không chạm (scroll −6,23) cạnh mọi số bước click; **giữ tiêu đề 60,07**, vì ck500 không
   hơn có ý nghĩa (+0,58, p = 0,31) và rớt noharm.
2. **GRPO-point chưa có số bước không chạm** ((x20b) vẫn nợ) ⇒ không biết tiêu đề hiện hành có cùng tác
   hại không. Chạy được bằng đúng runbook này (đổi đường sinh sang `infer_branch` + adapter GRPO-point,
   ~2 h T4, chấm 0 GPU). Khuyến nghị: chạy, để hai nhánh RL so được trên cùng hàng.
3. Có muốn thử sửa (vd. thưởng thêm đúng loại thao tác, hoặc lọc câu nhắc theo tỉ lệ loại thao tác)
   không — mỗi lượt là train mới ~25 h T4 + chấm test lại; lý do sửa đến **sau** khi thấy số test.

## Tệp

`report/259` · `report/261` · `runs/grpo_spice/` (`*_test*`, `*_nontap*`, `text_metrics_ck500.json`,
`test_ck500_doc.json`, `nontap_ck500_doc.json`) · mã `harness/gen_test_grpo.py` ·
`grpo_spice_test_doc.py` · `ck500_text_metrics.py` · `grpo_spice_nontap_doc.py` · runbook
`kaggle_grpo_spice_test_ck500.md` · `kaggle_grpo_spice_nontap_ck500.md`.
