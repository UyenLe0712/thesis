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
