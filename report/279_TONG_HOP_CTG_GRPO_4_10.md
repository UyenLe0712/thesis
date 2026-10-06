# 279 — Tổng hợp CTG-GRPO tới 4/10/2026: đã làm gì, ra số gì, làm gì tiếp

File một chỗ cho toàn bộ nhánh CTG-GRPO. Chi tiết số đo ở `report/278`, đặc tả gốc ở
`harness/tai_lieu_2026-10-04/276_ACTION_CTG_GRPO_4_10.md`. **Mọi số dưới đây là số val hoặc số thăm dò,
cấm trích vào luận văn.** Chưa có điểm test nào của CTG.

---

## 1. CTG-GRPO là gì (một đoạn)

GRPO trên S1/101 (Qwen2.5-VL-3B + LoRA mới), thưởng **CIDEr-D** thay cho SPICE của ck500, cộng bộ giữ
loại thao tác **CTG**: với nhóm 8 câu sinh của một câu nhắc có lớp vàng scroll/type/back, cộng thêm
`λ_k · z(đúng loại)` vào advantage; `λ_k` tự tăng khi tỉ lệ đúng loại `ĉ_k` tụt dưới đích `p_k`, tự giảm
về 0 khi mô hình giữ được đích. Mục tiêu: giữ điểm click của GRPO mà không làm rớt bước không-chạm
(ck500 rớt scroll −6,23 trên test, `report/261`).

| nhánh | thưởng | CTG | bước |
|---|---|---|---:|
| **A3** (đề xuất) | CIDEr-D | bật | 1000 |
| **A2** (ablation) | CIDEr-D | tính, không cộng | 1000 |
| A4 | CIDEr-D + lấy mẫu lại câu nhắc theo lớp | tắt | 500 |
| A7 | CIDEr-D + thưởng đúng loại (+1) | tắt | 500 |

---

## 2. Đã làm (4/10)

| việc | kết quả |
|---|---|
| Viết mã `harness/ctg_grpo.py` | r_cider, CTGTrainer, lưu/nạp `ctg_state.json`, `ctg_log.jsonl`, A4, A7, P0(b), đo đích, đo máy |
| Tự kiểm CIDEr-D (0 GPU) | **3.484/3.600 · 399/400**, khớp 276, sau khi thêm `'"'` vào PUNCT (Phụ lục A chép rơi ký tự) |
| P0(a) Kaggle T4 | **ĐẠT**: 20 bước, chạy tiếp từ checkpoint-10 nạp đúng adapter và λ; T4 136–137 s/bước, đỉnh 11,9 GiB |
| P0(b) luật cũ | **trượt** (trung bình log P(câu chạm) giảm S1 → ck500) — nhưng là **đo sai đại lượng** |
| P0(b) đọc lại theo xác suất | scroll P(câu chạm) **0,140 → 0,161 → 0,212**, ck500 − S1 +0,072 [+0,025; +0,126] ⇒ giả thuyết đúng |
| Đổi luật P0(b) (user quyết, phải khai) | đếm lật greedy trên val: **4 lật sang chạm vs 1 lật ngược**; test: 47/51 bước scroll bị phá thành câu chạm ⇒ ĐẠT |
| Đo đích `p_k` trên 440 câu nhắc train (Kaggle T4) | scroll **0,856** · type **0,814** · back **0,707** — gần trùng đích cũ (0,837 · 0,813 · 0,733) ⇒ không có rủi ro λ tự tắt |
| Kiểm tương đương cấu hình máy (CPU) | micro-batch 8×2 / 16×1 lệch 6e-9 · tắt gradient checkpointing lệch 0 · tắt CTG lệch 4,5e-3 ⇒ tăng tốc không làm sai phép train |

---

## 3. Bốn phát hiện đáng giữ

1. **GRPO phân cực, không kéo đều** (`report/278` §2). Bước S1 đang phân vân (P(câu chạm) TB 0,36) bị
   đẩy lên 0,57, 10/11 bước tăng, cả 4 bước bị lật nằm ở đây; bước S1 đã chắc thì chắc thêm. Tương quan
   mức ban đầu với mức đổi **0,71**. Bài phải viết "GRPO lật câu ở các bước sát biên", **không** viết
   "GRPO kéo cả lớp về câu chạm".
2. **Trung bình log là sai đại lượng** cho câu hỏi này: nó bị kéo bởi các bước P ≈ 0 (trung vị 0,026).
   Luật P0(b) cũ và đích `p_k` đều được sửa **sau khi thấy số** ⇒ khai trong bài.
3. **CTG có việc để làm:** câu sai loại của scroll 84% là câu chạm; 33% câu nhắc scroll, 48% type, 71%
   back có cả câu đúng lẫn câu sai trong 8 mẫu (chỗ CTG tác động được).
4. **Lớp `type` chỉ phủ ~70% bước nhập chữ** (102/146 câu chuẩn input_text quy về `type`, phần còn lại
   về `tap`), và GRPO tự làm lớp type tốt lên ⇒ phần lợi của CTG nằm chủ yếu ở scroll và back.

---

## 4. Tối ưu GPU đã thuê (hướng dẫn: `harness/runbook/colab_ctg_toi_uu.md`)

| núm | đúng? | lợi |
|---|---|---|
| micro-batch lớn hơn (bs × accum = 16 giữ nguyên) | ✅ đã kiểm | +5–20% [suy] |
| tắt gradient checkpointing | ✅ đã kiểm | +20–30% nếu đủ VRAM [suy] |
| 2 nhánh chung một GPU (A3 + A2) | ✅ hai tiến trình độc lập | trả 1 máy thay vì 2; mức lợi phải đo (Ô T2) |
| lưu mỗi 50 bước | ✅ không đụng phép tính | mất máy chỉ mất ≤ ~40 phút |
| tự trả máy khi xong | ✅ | không đốt tiền sau khi xong |
| **không làm:** dùng chung phần ảnh/câu nhắc cho 8 câu, vLLM, flash-attention 2 | | rủi ro sai im lặng hoặc cài khó |

Thời gian một bước nằm ở forward/backward trên 16 chuỗi ~1.000–2.000 token; khâu sinh rẻ (câu 5–10 token).

---

## 4b. Kết quả dò máy (5/10) và cấu hình CHỐT

Đo trên 12 câu nhắc dài nhất, 10 bước, đọc bước 6–10 (số thật của lượt train sẽ nhanh hơn một chút):

| máy · cấu hình | s/bước | đỉnh VRAM | GPU % |
|---|---:|---:|---|
| L4 · bs4×4 gc | **86,3** | 13,5 GiB | 90–100 (bão hoà) |
| L4 · bs8×2 gc | 89,8 | 16,4 GiB | |
| L4 · tắt gc | tràn bộ nhớ | | |
| A100 · bs4×4 gc | **36,4** | 13,5 GiB | 30–100 (còn rỗi) |
| A100 · bs8×2 / bs16×1 gc | 36,2 / 35,7 | 16,4 / 25,0 GiB | |
| A100 · tắt gc (bs4, bs8) | tràn bộ nhớ | | |
| **A100 · 2 nhánh chung, bs4×4 gc** | **49,3 / 49,4 mỗi nhánh** | 28,9 GiB cả máy | |

Giá Colab đọc lúc đo: L4 1,54 · A100 5,3 đơn vị/giờ. Cho A3 + A2 (2 × 1.000 bước):

| phương án | giờ máy | đơn vị | xong sau |
|---|---:|---:|---:|
| L4, hai phiên | 48,0 | ~74 | ~24 h |
| A100, hai phiên | 20,2 | ~107 | ~10 h |
| **A100, một phiên chạy chung** | **13,7** | **~73** | **~14 h** |

⇒ **Chốt: A100, một phiên, `ARMS = {"A3": 1000, "A2": 1000}`, `BS, ACC, NO_GC = 4, 4, False`, `SAVE = 50`,
`TAT_MAY = True`.** Cùng tiền với L4, xong sớm hơn ~10 h, chỉ phải trông một phiên. Lô to hơn chỉ nhanh ~2%
(dưới ngưỡng 5%) nên giữ bs4 (đúng cấu hình P0, ít VRAM để chạy chung).

## 4c. Train 5/10 + val bước 250 (Kaggle T4) — số val, cấm trích

Tệp: `runs/ctg/val/` (zip gốc `ctg_val_out.zip`) · log train tới bước ~360 `runs/ctg/train/A{2,3}/`.
Đọc bằng `harness/ctg_doc.py`. Kiểm đường: S1 chấm lại 158/249, trùng từng bước tệp cũ (lệch 0).

| nhánh | đúng loại 75 | scroll /32 | type /28 | back /15 | exec 249 | số từ |
|---|---|---|---|---|---|---|
| S1 | 66 | 29 | 25 | 12 | 158 | 7,28 |
| ck250 (SPICE) | 66 | 28 | 26 | 12 | 161 | 7,19 |
| A2_250 | 64 | 26 | 27 | 11 | 161 | 7,25 |
| A3_250 | 66 | 28 | 27 | 11 | 161 | 7,29 |

- exec: A3 = A2 = 161 (cứu/phá lẫn nhau 3/3; K2: +0,00 [−1,98; +1,99] ⇒ qua). So S1 cả hai +1,20, KTC phủ 0.
  A3 cứu 9 phá 6, A2 cứu 10 phá 7 so S1. Hai nhánh trùng 334/400 câu.
- Đúng loại: A3 − A2 = +2 (scroll +2: hai bước A2 lật swipe → back/click, A3 giữ swipe). Chiều đúng như
  CTG nhắm nhưng n=75, 2 bước ⇒ chưa đọc được. A2 scroll 26/32 đã gần ck500 (25/32).
- K3: rỗng 0 %, số từ lệch +0,1 % ⇒ qua. KL của A2 (cờ K3 từ bước ~236): trung vị theo khối 25 bước chỉ cao
  hơn A3 10–20 %; cờ đến từ 3 bước gai (251: 0,90 · 313: 0,44 · 348: 2,03) kéo trung bình trượt 20 bước.
  A2_250 không thấp hơn S1 ⇒ **cho A2 chạy tiếp; quyết định bỏ qua cờ KL phải khai khi báo.**
- Bước 250 chưa tách được hai nhánh là đúng dự kiến: ck250 cũng chỉ +3 so S1; trôi về câu chạm theo 278 §1
  rõ ở khoảng bước 500. Phép quyết là K1/K2 ở bước 500.

## 4d. Val bước 500 (Kaggle T4, 5/10) — số val, cấm trích

Tệp: `runs/ctg/val/` (zip gốc `ctg_val_out_500.zip`; zip lượt 250 đổi tên `ctg_val_out_250.zip`).
Kiểm đường: S1 chấm lại 249 bước, exec 158 (đạt).

| nhánh | đúng loại 75 | scroll /32 | type /28 | back /15 | exec 249 | số từ |
|---|---|---|---|---|---|---|
| S1 | 66 | 29 | 25 | 12 | 158 | 7,28 |
| ck500 (SPICE) | 63 | 25 | 26 | 12 | 165 | 7,37 |
| A2_500 | 63 | 26 | 25 | 12 | 163 | 7,12 |
| A3_500 | 66 | 27 | 27 | 12 | 163 | 7,03 |

- K1: đúng loại không-tap A3 − A2 = +3 (scroll +1, type +2) ⇒ qua theo luật (> 0), nhưng chỉ 3/75 bước.
  A3 giữ ngang S1 (66), còn A2 tụt về đúng mức ck500 (63). Scroll của A3 vẫn thấp hơn S1 2 bước.
- K2: exec A3 = A2 = 163 (cứu 2, phá 2), +0,00 [−1,62; +1,60] ⇒ qua. So S1 cả hai +2,01, KTC phủ 0
  (A3 cứu 12 phá 7, A2 cứu 13 phá 8).
- K3: rỗng 0 %, số từ A3 7,03 (−3,5 % so S1) ⇒ qua.
- Hai nhánh trùng 325/400 câu; từ 250 → 500 A3 đổi 114 câu, A2 đổi 102.
- Hình ảnh đúng như CTG nhắm (giữ loại thao tác mà không mất exec), nhưng cỡ hiệu ứng quá nhỏ để đọc trên val.
  Theo luật 276: A3 qua K1/K2 ⇒ được mở đợt 2 A4 + A7 (A7 còn chờ chốt dấu).

## 4e. Val bước 1000 (Kaggle T4, 5/10) — số val, cấm trích

Tệp: `runs/ctg/val/*_1000*` (zip gốc `ctg_val_out_1000.zip`). Kiểm đường: S1 chấm lại md5 trùng tệp cũ
(`1c8dbcd5…`), exec 158. Đọc bằng `harness/ctg_doc.py`.

| nhánh | đúng loại 75 | scroll /32 | type /28 | back /15 | exec 249 | trùng S1 /400 | số từ |
|---|---|---|---|---|---|---|---|
| S1 | 66 | 29 | 25 | 12 | 158 | 400 | 7,28 |
| ck500 (SPICE) | 63 | 25 | 26 | 12 | **165** | 328 | 7,37 |
| A2_500 → A2_1000 | 63 → **60** | 26 → 27 | 25 → **23** | 12 → 10 | 163 → 164 | 203 | 7,10 |
| A3_500 → A3_1000 | 66 → 63 | 27 → 27 | 27 → 26 | 12 → 10 | 163 → **160** | 229 | 7,22 |

- **A3 − A2 ở 1000:** đúng loại không-tap +3, nằm trọn ở type (26 vs 23); scroll 27 = 27, back 10 = 10.
  exec −4 bước (cứu 2, phá 6) = −1,61 [−3,91; +0,42]. K3 qua (rỗng 0, số từ −0,7 %).
- **Chọn điểm lưu theo luật:** A3 exec@1000 − @500 = −1,20, A2 +0,40, đều trong ngưỡng 2,6 ⇒ cả hai giữ
  `checkpoint-1000`. ⚠️ A3_500 tốt hơn A3_1000 trên mọi cột val; đổi sang 500 lúc này là chọn sau khi thấy
  số, nếu làm phải khai.
- **So ck500:** không nhánh CTG nào hơn ck500 về exec val (A3 −2,01 [−4,47; +0,37], A2 −0,40). Đúng loại
  A3_1000 = ck500 = 63. Scroll của cả A2 lẫn A3 (27) cao hơn ck500 (25) ⇒ phần giữ scroll trên val đến từ
  việc đổi thưởng SPICE → CIDEr-D, không phải từ CTG.
- **Cơ chế CTG thật sự làm được (đo):** A2 trôi dần về câu "Search for X" (3 → 5 → 8 câu ở 250/500/1000;
  S1 5, ck500 5), mà `canon_action` quy câu này về `tap` ⇒ đó là 2/3 bước type A2 mất. A3 giữ ở 2 câu ở cả
  ba điểm lưu. λ_type của A3 cao nhất đầu lượt (1,17 → 1,58 tới bước 150) rồi về 0 ở bước 350 — khớp với
  việc lực giữ type tác động sớm.
- **Back rớt 12 → 10 ở cả hai nhánh, đúng cùng hai bước** ("Go back" → "Click on the Holi event" /
  "Open the MaxMilhas app", A3_500 còn đúng). Không phải lỗi riêng của CTG: λ_back của A3 về **0 từ bước
  150** (A2 tính cũng 0 từ bước 200) vì tỉ lệ đúng loại khi lấy mẫu trên train đã vượt đích 0,707 ⇒ bộ giữ
  tự tắt ở lớp back, rồi drift của GRPO lấy đi hai bước. Đích back đo bằng lấy mẫu T=1 (0,707) thấp hơn
  độ đúng greedy của S1 trên val (12/15 = 0,80), nên bộ giữ coi back là ổn trong khi greedy vẫn trôi.
- **Đọc chung:** CTG có tác dụng đo được nhưng hẹp (chặn một lối diễn đạt sai loại ở lớp type), đổi lại exec
  click thấp hơn A2 1,6 điểm (KTC phủ 0). n = 75 bước không-tap và 249 click quá nhỏ để kết luận; đây là
  thông tin để quyết có chấm test hay không, không phải kết quả.

## 4f. Việc kế (5/10): test KHÔNG chạm cho A3_1000, A2_1000

Runbook `harness/runbook/kaggle_ctg_test_nontap.md` (Kaggle T4 ×2, A3 và A2 song song, ~2,2–2,5 h, 0 đồng,
không upload mới). Đọc bằng `harness/ctg_nontap_doc.py` → `runs/ctg/test_nontap/`. Chạy khô `--kho` tái lập đúng
bảng ck500. Ghi nhận từ chạy khô: trên 494 bước input_text của test, câu "Search for" có S1 77 · ck500 121 ⇒ lối
trôi đã thấy ở A2 trên val có chỗ để hiện ra trên test. A4/A7 hoãn tới khi có số này.

## 4g. ✅ TEST KHÔNG CHẠM 6/10 — R-CTG KHÔNG ĐẠT, scroll vẫn rớt (số test, trích được)

Kaggle T4×2, A3 2,73 s/bước và A2 2,50 s/bước chạy song song (~1,9 h). Kiểm hoà 20/20, cả hai log có
`[điểm lưu] …/A3_1000` và `…/A2_1000`, mỗi nhánh 2.495 câu (A3 có 1 câu rỗng). Tệp nằm ở `runs/ctg/test_nontap/`,
số máy đọc ở `ctg_nontap_doc.json`. Thước noharm, KTC cụm app, B = 10.000.

| nhóm | n | S1 | ck500 | A2 | A3 | A3 − A2 [KTC] | A3 − S1 [KTC] |
|---|---|---|---|---|---|---|---|
| toàn bộ | 2.495 | 85,97 | 84,29 | 84,45 | 84,25 | −0,20 [−0,87; +0,47] | −1,72 [−2,82; −0,63] |
| scroll | 755 | 83,97 | 77,75 | 77,62 | 78,68 | +1,06 [−0,27; +2,48] (cứu 17 phá 9) | **−5,30** [−7,19; −3,53] |
| wait | 505 | 90,69 | 95,25 | 94,46 | 94,46 | 0,00 | +3,76 [+1,79; +5,90] |
| input_text | 494 | 81,58 | 79,55 | 81,38 | 80,36 | −1,01 [−3,09; +1,03] | −1,21 [−4,16; +1,80] |
| open_app | 469 | 96,16 | 97,87 | 98,72 | 98,72 | 0,00 | +2,56 [+1,14; +4,20] |
| navigate_back | 270 | 72,96 | 67,04 | 65,56 | 62,59 | **−2,96 [−5,32; −0,76]** (cứu 1 phá 9) | −10,37 [−14,62; −6,23] |

Luật §6: **R-CTG KHÔNG ĐẠT** (cận dưới scroll −0,27) · **R-noharm scroll KHÔNG ĐẠT** (−5,30 < −3) · R-noharm toàn
bộ đạt sát (cận dưới −2,82 ≥ −3). A3 − ck500: toàn bộ −0,04 [−0,89; +0,83], scroll +0,93 [−0,28; +2,22], back −4,44
[−7,58; −1,50] ⇒ CTG **không gỡ được** tác hại không chạm của ck500 (scroll −6,23 → −5,30, chênh trong nhiễu).

**Đọc cơ chế:**
1. **Scroll:** lỗi chính vẫn là scroll→tap: S1 114 · ck500 161 · A2 157 · A3 151. CTG chỉ bớt được 6 câu so với A2.
   Thưởng CIDEr-D thay SPICE (A2 so với ck500) không đổi gì trên test: −0,13 [−1,77; +1,51]. Trên val, scroll giữ
   được là nhờ CIDEr-D; ở đây kết quả đó không chuyển sang test.
2. **Back là phép so có ý nghĩa duy nhất của A3 − A2, và theo chiều gây hại.** A3 viết sang câu "Open … app" hoặc
   "Click on the screen" ở bước quay lại. Trên 270 bước back, số câu "Open … app" là S1 11 · ck500 27 · A2 28 ·
   A3 33; số câu "go back" là S1 189 · A2 169 · A3 158. λ_back của A3 về 0 từ bước 150, nên phần này không đến
   từ một lực đẩy CTG nhắm vào back. [suy] Lực đẩy lên scroll/type dồn xác suất khỏi lớp back. Phép so này là
   một trong sáu nhóm chưa hiệu chỉnh bội, cần khai như vậy.
3. **"Search for" không phải lỗi theo thước.** Trên input_text, `canon_action` quy 121/494 câu chuẩn về tap, vì
   người chú thích cũng viết "search for X". Lớp vàng của CTG lấy từ chính `canon_action(câu chuẩn)` nên nhất quán
   với thước. A3 bớt "Search for" (A2 100 → A3 85, khớp hướng đã thấy trên val), nhưng ở bước vàng là type thì
   chỉ đúng 312 so với 311, còn ở bước vàng là tap thì mất 85 so với 91 (ví dụ vàng "search for udon noodles",
   A3 viết "enter the udon noodles"). Mức +3 ở lớp type trên val **không tái lập** trên test.
4. **wait / open_app tăng là của GRPO, không phải của CTG:** ck500, A2, A3 đều tăng ngang nhau so với S1, và
   A3 − A2 = 0 ở cả hai nhóm.
5. Val không dự báo test lần thứ ba (sau V2 và TAGE): val cho A3 − A2 ở scroll = 0, type +3, back 0; test cho
   +1,06, −1,01 và −2,96.

⚠️ Các cặp so với S1 có lẫn biến đường sinh (S1 dùng `infer_branch`). Kiểm hoà 20/20 trên chính 20 bước không
chạm làm biến này nhỏ, nhưng không loại hẳn. Cặp A3 − A2 và A3 − ck500 thì sạch.

**Hệ quả (đề xuất, chờ user quyết):** đóng CTG-GRPO như một kết quả âm có khai báo. Không train A4/A7 (~73 đơn
vị A100), không chấm bước chạm của A3/A2 trên test (val exec của cả hai thấp hơn ck500, và R-CTG đã không đạt).
Mô hình chính giữ ck500, khai tác hại ở scroll/back. CTG vào luận văn ở mục "các hướng đã thử".

## 5. Làm gì tiếp — từng bước

| # | việc | máy · giờ | xong khi |
|---|---|---|---|
| 1 | Kéo `_bundles/ctg-grpo-script/` (6 tệp) và `_bundles/fgrb_p1_bundle.zip` lên `MyDrive/thesis/ctg/` | máy nhà | Drive có đủ |
| 2 | Phiên **A100** dò: `colab_ctg_train.md` Ô C1–C3, rồi `colab_ctg_toi_uu.md` Ô T0 → T1 → T2 → T3 | A100 ~1,5 h | có bảng T1, T2, T3 |
| 3 | Phiên **L4** dò: mục 4 của `colab_ctg_toi_uu.md` | L4 ~0,5 h | có s/bước L4 |
| 4 | Gửi Claude bảng T1/T2/T3 + số L4 ⇒ chốt máy, `BS/ACC/NO_GC`, chạy chung hay tách | — | cấu hình chốt |
| 5 | Train **A3 + A2** theo `colab_ctg_train.md` (Ô C1: `ARMS`, `BS/ACC/NO_GC`, `SAVE = 50`, `TAT_MAY = True`) | A100 hoặc L4, ~11–17 h mỗi nhánh [suy] | `final/` trên Drive |
| 6 | Khi có `checkpoint-250` và `-500`: tải adapter → dataset Kaggle `ctg-ckpts` → chấm `kaggle_ctg_val.md` → `ctg_doc.py` (K1, K2, K3) | Kaggle T4 ~1–1,5 h/lần | qua hoặc dừng |
| 7 | Nếu A3 qua K1/K2 ở 500: đợt 2 **A4 + A7** (`ARMS = {"A4": 500, "A7": 500}`) | ~11–17 h | |
| 8 | Chọn điểm lưu (mặc định 1000) trên val → chấm **test** A3, A2 (click + không chạm) → UI-Venus | Kaggle ~15–18 h | bảng số theo 276 §9 |

Ước tổng: ~35–50 h GPU thuê (ít hơn nếu chạy chung hai nhánh hoặc dùng L4), ~20–25 h Kaggle; tín hiệu
đầu tiên (K1/K2 ở bước 500) sau ~1,5–2 ngày.

---

## 6. Luật dừng và đọc (276 §8, giữ nguyên)

- **K1** (bước 500): đúng loại không-tap trên val của A3 không cao hơn A2 ⇒ dừng A3.
- **K2** (bước 250, 500): exec click val của A3 thấp hơn A2 quá 2,6 ⇒ dừng.
- **K3** (bất kỳ lúc nào): câu rỗng > 1% · số từ lệch > 30% so S1 · λ ở trần 3 liền > 100 nhóm · KL gấp 3 ck500.
- **Test:** R-click (A3 so S1, ck500, 60,07; chỉ nói "cao nhất có ý nghĩa" khi cận dưới KTC > 0) · R-CTG (A3 − A2
  scroll cận dưới > 0) · R-noharm (scroll A3 − S1 ≥ −3) · R-giữ ngoài (UI-Venus cùng dấu).

---

## 7. Còn treo

1. **Dấu của A7:** 276 ghi `R − 1[đúng loại]`, mã cài **cộng** (tên nhánh là "cộng loại"). Chốt trước bước 7.
2. File `277_HO_SO_NEN_…` (hồ sơ nền của 276) không có trong kho.
3. Mã chưa commit: `harness/ctg_grpo.py` (md5 `332765b7…`), `harness/kiem_tuong_duong_ctg.py`,
   `harness/runbook/colab_ctg_toi_uu.md`, `colab_ctg_train.md` (bản 2), `report/278`, `report/279`.
4. Phần đo `[máy]` và chạy nhiều nhánh một GPU **chưa chạy trên GPU**; phiên dò ở bước 2 là lần kiểm đầu.

---

## 8. Tệp liên quan

| loại | tệp |
|---|---|
| đặc tả | `harness/tai_lieu_2026-10-04/276_ACTION_CTG_GRPO_4_10.md` |
| mã | `harness/ctg_grpo.py` · `harness/ctg_doc.py` · `harness/kiem_tuong_duong_ctg.py` |
| runbook | `harness/runbook/kaggle_ctg_p0.md` · `kaggle_ctg_dich.md` · `colab_ctg_toi_uu.md` · `colab_ctg_train.md` · `kaggle_ctg_val.md` |
| phân tích | `report/278_PHAN_TICH_P0_CTG_4_10.md` |
| kết quả thô | `runs/ctg/p0/` (P0a log, `p0b.json`) · `runs/ctg/dich/` (đích, 3.520 câu mẫu S1) |
| gói upload | `_bundles/ctg-grpo-script/` (6 tệp) |
