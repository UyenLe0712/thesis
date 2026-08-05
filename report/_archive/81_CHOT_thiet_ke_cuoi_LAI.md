# report/81 — CHỐT thiết kế cuối (phương án LAI): dữ liệu, train, metric

> Bối cảnh: luận văn train Qwen2.5-VL-3B (SFT-LoRA, on-device) sinh **hướng dẫn sử dụng app cho người đọc** từ ảnh màn + câu hỏi. report/78 đã chốt đi phương án **LAI**; 4 kill-test free (report/73-76) đã rút nền dưới trụ "lọc-bịa" cũ; pilot AndroidControl (report/79) phát hiện bộ này có sẵn **gold hướng-dẫn-người từng bước**. File này chốt ba thứ còn treo: **train trên bộ nào, đo cái gì ở đâu, và thước "so hai đoạn hướng dẫn" định nghĩa chính xác ra sao.** Ngày: 2026-07-19.

---

## Phán quyết 1 dòng

**Train một model duy nhất, tín hiệu CHÍNH = gold `step_instructions` của AndroidControl, phụ trợ = data MobileViews-chưng-cất (ablation bật/tắt); đo TRỤ CHÍNH "độ ĐÚNG" ngay trên app-unseen split của chính AndroidControl (in-distribution held-out, KHÔNG cross-dataset) bằng thước phủ-bước action∧target đã-validate-bơm-lỗi; đo TRỤ PHỤ "độ trung thực" no-gold trên MobileViews (tắt VH lúc sinh); ScreenSpot-v2 giữ vai đối chứng grounding; K1/K2/OCR/VIỆC1 gói thành một chương đóng-góp đo-lường.**

Một xương sống dữ liệu (AndroidControl), một trụ chính rõ (ĐÚNG), một trụ phụ gần-miễn-phí (TRUNG THỰC). Đây là bản kết tinh của 4 mũi phân tích, nghiêng theo phán quyết trọng-tài (Mũi 4): **cắt khung cross-dataset của report/78, chuyển sang in-distribution held-out để phép đo đọc-được.**

---

## Vai từng dataset

| Bộ | Peer-reviewed? | Dùng làm gì (thiết kế cuối) | Quyết định |
|---|---|---|---|
| **AndroidControl** (Li et al., NeurIPS 2024 D&B, arXiv 2406.03679, CC0) | ✅ có | (1) **Tín hiệu train CHÍNH** = gold `step_instructions` do người viết. (2) **Bộ đo trục ĐÚNG** trên app-unseen split có sẵn. So hướng-dẫn-model ↔ gold-instruction (văn bản người↔người). | **ĐỔI VAI — LÊN xương sống chính** (trước chỉ là "bộ chấm phụ") |
| **MobileViews** (preprint arXiv 2409.14337, MIT) | ❌ preprint | (1) **Nền chưng cất** (teacher sinh trên màn không-gold → data aux, giữ sợi "distillation"). (2) **Bộ đo trục TRUNG THỰC no-gold** (VH sẵn, tắt VH lúc sinh, đối chiếu bịa-tên-nút). (3) Nhà của chương đo-lường + câu chuyện bề-rộng-app on-device. | **GIỮ — nhưng HẠ vai**: từ "trục chính" xuống "aux train + trục phụ đo" |
| **ScreenSpot-v2** (OS-Atlas ICLR 2025¹; gốc SeeClick ACL 2024 ✅; apache-2.0) | gốc ✅ | Đối chứng grounding point-in-bbox. **KHÔNG train, KHÔNG headline.** | **GIỮ NGUYÊN vai** |

¹ OS-Atlas/UGround ghi ICLR 2025 nhưng **chưa tự mở OpenReview xác nhận phiên này** — verify trước khi in "peer-reviewed". SeeClick (ACL 2024) đã chắc.

---

## Có bỏ MobileViews không (trả lời thẳng câu user)

**KHÔNG bỏ.** Nhưng cũng đừng ảo tưởng nó còn là trụ chính. Ba vai còn lại của MobileViews, không bộ nào khác gánh thay được:

1. **Nền chưng cất — chỗ DUY NHẤT giữ chữ "distillation" sống.** Nếu train thẳng trên gold của AndroidControl và bỏ hẳn MobileViews, luận văn rơi về **fine-tune-có-giám-sát-trên-gold** — gần SeeClick/UI-R1, mất đúng chỗ mới. MobileViews là bộ duy nhất trong ba bộ **vừa có VH sẵn (nhẹ) vừa KHÔNG có gold** → teacher sinh trên đó mà không lộ đáp án, đúng nghĩa "chưng cất tự-sinh rồi lọc". Đây là seam phòng-thủ-được (report/78 Mũi 3).
2. **Trục TRUNG THỰC no-gold — AndroidControl mirror nhẹ KHÔNG có a11y-tree.** Muốn đo "model có bịa tên nút không" cần một nguồn cấu-trúc (VH). Mirror HF của AndroidControl đã lược mất a11y-tree (report/79). MobileViews có VH sẵn, nhẹ, đã split 18/12, chi phí biên đo ≈ 0. Đây là chỗ DUY NHẤT demo được "đo-khi-không-có-gold" — nửa no-gold của đóng góp phương-pháp.
3. **Bề rộng ~220 app một-màn + nhà của chương đo-lường** (K1/K2/OCR/VIỆC1 đều chạy trên nền MobileViews+teacher).

**Bỏ được về mặt kỹ thuật không?** Được — "AndroidControl-only" vẫn là một luận văn hợp lệ, và là **sàn lui** nếu hết giờ. Nhưng bỏ MobileViews = mất cả ba vai trên = co về gần một bản tái hiện supervised-grounding, khó trả lời "khác gì SeeClick". Chỉ bỏ khi cạn thời gian.

**Lưu ý trung thực về giá trị thực-nghiệm của trục no-gold:** K2 (teacher bịa ~0) đã giết trục **Tier 1** (LỌC-vs-THÔ) ở tầng thực nghiệm — data-lọc ≈ data-thô nên ablation này nhiều khả năng **null tầm thường**. Trục no-gold còn sống là **Tier 2** = đo bịa của chính **student 3B** (không phải teacher) khi tắt VH lúc suy luận; K2 KHÔNG chạm construct này. Nhưng nếu student 3B cũng bịa ~0 thì Tier 2 cũng null → lúc đó nửa no-gold còn giá trị "phương pháp đo", không còn "phát hiện". Chưa có số student nên chưa biết — **phải khai thẳng khả năng này**.

---

## Metric "so hai đoạn hướng dẫn" — định nghĩa cụ thể + luật gióng + validate

Bài học xương máu từ K1: **so độ-gần-nghĩa bằng embedding, một mình, KHÔNG tách được "bịa nghe-giống" khỏi "gọi-đúng-bằng-từ-khác"** (hai phân bố chồng lấn hoàn toàn, không ngưỡng nào cắt được). Thước mới phải né đúng cái bẫy đó bằng cách **không dựa vào một con số tương đồng bề mặt**. Kiến trúc ba lớp:

### Lớp A — Tách mỗi bước thành cặp `(action, target)`

Cả bước-của-model lẫn gold `step_instruction` đều được phân tích thành:
- **action** = loại thao tác, khớp trên **từ vựng đóng** (tap/click, type, scroll, swipe, long-press, open, navigate…). Parser bằng luật, KHÔNG dùng LLM. Ví dụ: "Click on the Gmail tab" → action = `tap`.
- **target** = tên đích UI được gọi ("Gmail tab", "search bar", "settings icon"). Chuẩn hoá chuỗi + backstop bằng embedding **từ họ KHÁC** (bge-m3 — không phải nomic đã dùng lúc lọc, không phải GPT-family của teacher → chống vòng).

> **Đây chính là chỗ vá K1.** "Gmail tab" vs "Calendar tab" là **lệch target cứng** dù embedding rất gần. Tách action∧target biến "bịa nghe-giống" (near-miss) thành một mismatch phát hiện được — điều cosine-sim một mình không làm nổi. Tinh thần này khớp đúng cách chính AndroidControl chấm step-accuracy: đúng ⇔ đúng **loại action** VÀ đúng **đích** (họ dùng toạ độ lệch ≤14%, ta thay bằng target-trong-văn-bản vì mirror nhẹ không có a11y-tree).

**Một bước khớp ⇔ action khớp VÀ target khớp.**

### Lớp B — Gióng model ↔ gold: dùng PHỦ-TẬP (set-coverage), không ép gióng 1-1

Guide của model là văn nhiều bước cho người (có dẫn nhập, gộp/tách bước tầm thường); gold là chuỗi lệnh nguyên-tử cho agent. Ép gióng 1-1 kéo theo cả mớ siêu-tham-số segmentation (τ_align, phạt gap, luật gộp/tách) — mỗi cái lại phải validate riêng, dễ "tuning cho đẹp số".

**Chốt: gióng bằng phủ-tập.** Mỗi gold-step được coi là "được phủ" nếu **tồn tại** một model-step khớp cả action lẫn target (không bắt đúng vị trí). Đây là bậc lỏng nhất (kiểu mIoU trong dòng procedure-planning) và đúng câu hỏi thực chất: *"guide có bỏ sót thao tác nào không?"*

*Tuỳ chọn nâng cấp nếu pilot cho thấy model hay gộp/tách bước:* bật gióng đơn-điệu-giữ-thứ-tự (quy hoạch động kiểu Needleman-Wunsch / LCS-có-trọng-số, cho phép nhiều-model↔một-gold). Kỹ thuật chuẩn, không tự chế — nhưng **chỉ bật khi cần**, mặc định giữ set-coverage cho gọn.

### Lớp C — Ba số đọc ra (bậc chặt tăng dần)

- **Coverage / Recall-bước** (headline): % gold-action được guide phủ. Đúng câu hỏi "có bỏ sót không".
- **Precision-bước** (chống nhồi bước thừa/bịa) → **F1**.
- **Order-τ partial** (Fagin "Comparing partial rankings", SIAM 2006 + Lapata CL 2006 — **KHÔNG phải Kendall τ-b**): trên các cặp bước đã khớp, đếm vi phạm đơn-điệu. Chỉ phạt **cặp bắt-buộc** (suy từ gold theo nhân quả); cặp tự-do (điền email/sđt đảo được) không phạt oan.
- *Tuỳ chọn* **Success** (phủ đủ + đúng thứ tự + không sai action/target): chặt, dễ null, báo phụ.

**Headline chốt = target-khớp CÓ ĐIỀU KIỆN action-đã-đúng.** Báo action và target **RIÊNG**, không gộp. Lý do: action-type (tap/scroll) dễ hơn target-name nhiều; một student thoái-hoá "luôn đoán tap" sẽ ăn điểm action rẻ mà guide không tốt hơn. Điều-kiện-hoá chặn degeneracy đó.

**Điểm so:** Student vs **Teacher-BASE** (gpt-4o-mini zero-shot) trên cùng split, cùng thước. Đây là mốc tham chiếu bắt buộc để chứng minh điểm cao đến từ "đúng hơn" chứ không chỉ nhờ "khớp giọng gold" (rủi ro circular ngược — xem dưới).

### Lớp D — LLM-judge KHÁC HỌ = cross-check hội tụ, KHÔNG vào công thức

Một judge nhị phân "bước model có đạt cùng sub-goal với gold không", chạy bằng model **họ thứ ba** (không GPT vì teacher là GPT; không Qwen vì student là Qwen → Llama-3.x hoặc Gemini). Chỉ báo mức đồng thuận với thước action∧target + κ judge-vs-người. **KHÔNG được đưa vào headline** (tái nhập circularity + self-preference; Panickssery et al., NeurIPS 2024 cảnh báo judge tự-thiên-vị chính văn phong của nó).

### Validate thước = BƠM-LỖI (cổng, làm được KHÔNG cần model)

Trước khi tin thước, bơm lỗi đã-biết vào output rồi kiểm thước có bắt được không (Sai et al., "Perturbation CheckLists for Evaluating NLG Evaluation Metrics", **EMNLP 2021** — peer-reviewed). Pre-register ngưỡng TRƯỚC khi nhìn kết quả:

| Loại bơm lỗi | Kỳ vọng | Ngưỡng pre-register |
|---|---|---|
| Sai target ("Gmail tab"→"Calendar tab") | detection cao | ≥ 0.90 |
| Sai action (tap→type) | detection cao | ≥ 0.90 |
| Thiếu bước (xoá 1 gold-action khỏi guide) | recall tụt tương ứng | ≥ 0.90 |
| Thừa/bịa bước (chèn bước không có gold) | precision tụt | — |
| Đảo thứ tự | order-τ tụt, coverage GIỮ NGUYÊN | (chứng minh 2 trục tách nhau) |
| **Paraphrase giữ-nghĩa (control)** | điểm KHÔNG tụt | **false-positive ≤ 0.10** |
| Đơn-điệu: k lỗi | điểm giảm đều theo k | — |
| **Tách phân phối (bài kiểm mấu chốt — nơi K1 chết)** | phân phối "một-lỗi-target" TÁCH khỏi "paraphrase" | **AUC/separation ≥ 0.80** |

Dòng cuối là cổng sinh-tử: nếu thước mới cũng chồng lấn như K1, nó hỏng — phải biết TRƯỚC khi công bố, không phải sau. Nếu cổng này rớt → dừng, sửa thước, không train.

Cộng một **mini-study construct-validity ~30-50 mẫu**: chấm-người "guide này dùng được cho người không" rồi đối chiếu với điểm-thước (báo Cohen's κ, một lần, KHÔNG làm cổng đậu/rớt — khớp protocol report/27 §7). Giờ so người↔người nên nhẹ hơn nhiều so với khung cũ.

---

## Bộ thước đo cuối

| Trục | Đo cái gì | Bộ nào | Có gold? | Thước | Vai |
|---|---|---|---|---|---|
| **ĐÚNG** (trụ chính) | Guide có khớp thao-tác-đúng của người thật không | AndroidControl app-unseen split | ✅ gold `step_instructions` | Coverage-recall action∧target (headline) + F1 + order-τ partial; Student vs Teacher-BASE | **HEADLINE** |
| **TRUNG THỰC** (trụ phụ) | Student 3B có bịa tên nút không tồn tại không (tắt VH lúc sinh) | MobileViews held-out | ❌ no-gold (đối chiếu VH nhiều-tầng) | Tier 2 kiểu report/56, matcher nâng nhiều-tầng (chuỗi→VH→OCR) | phụ, gần-miễn-phí |
| *Tier 1* (readout phụ) | Student-LỌC vs Student-THÔ | MobileViews | ❌ | faithfulness | báo dù null (chi phí biên ~0) |
| **Grounding** (đối chứng) | point-in-bbox | ScreenSpot-v2 | ✅ bbox | tinh thần SeeClick; dung sai 14% AITW | tuỳ chọn, không headline |
| **Chương đo-lường** (đóng góp mới) | Vì sao đo faithfulness-VH kiểu naïve không đáng tin | MobileViews+teacher | — | K1/K2/OCR/VIỆC1 | chương độc lập |

---

## Có cần thêm dataset không (trả lời thẳng)

**KHÔNG cần bộ MỚI.** Ba bộ hiện tại đủ vai. Thêm bộ thứ tư = phình phạm vi, ngược ràng buộc <3 tháng, làm một mình.

**Nhưng có MỘT nâng cấp dữ-liệu đáng cân nhắc (không phải dependency mới):** cái "dataset có CẢ gold-instruction-người LẪN VH đầy đủ trên cùng màn" mà user mong ước **chính là AndroidControl bản GỐC nặng (GCS/tensorflow, ~vài GB)** — bản này có a11y-tree (→ đo trung thực kiểu VH) VÀ gold step_instruction (→ đo độ đúng) trên CÙNG màn. Mirror HF nhẹ chỉ lược mất a11y-tree. Nếu tải được bản nặng thì đo được **cả hai trục trên cùng màn** → có điểm-trong-miền để kiểm parallel-trends → co confound thêm.

Đây là **nâng cấp cao-giá-trị-nhất**, không phải bắt buộc. Rào chắn trước khi cam kết:
- **Chưa kiểm label-coverage của a11y-tree AndroidControl.** Pilot report/79 thấy ~48% gold-click nhắm icon/ảnh không chữ → a11y-tree có thể đụng ĐÚNG trần ~20-48% vô-nhãn như K2/OCR đã phơi. Nếu vậy lợi thế "richer labels" biến mất, tải GB không đáng. **Phải đếm trước.**
- **Chưa kiểm chi phí tải/parse** trên máy không-GPU. Nếu quá tốn → bỏ, dùng mirror nhẹ + khai giới hạn.

Trục ĐÚNG **không** phụ thuộc bản nặng (nó dùng gold `step_instructions` văn bản, mirror nhẹ đã đủ). Bản nặng chỉ giúp gom trục TRUNG THỰC về cùng bộ.

---

## Pipeline cuối (sơ đồ ASCII gọn)

```
 ┌─ NGUỒN TRAIN (một model, hai nguồn, vai rạch ròi) ─────────────────┐
 │                                                                    │
 │  AndroidControl (app train-split)          MobileViews (không-gold)│
 │   ảnh + gold step_instruction               ảnh + câu hỏi          │
 │        │ (tín hiệu CHÍNH)                         │                 │
 │        │                            teacher gpt-4o-mini sinh nháp   │
 │        │                                          │                 │
 │        │                            lọc-bịa vs VH (vai HẠ:          │
 │        │                            thành phần, KHÔNG phải trụ)     │
 │        │                                          │ (data AUX)      │
 │        └──────────────┬───────────────────────────┘                │
 │                       ▼                                             │
 │          Qwen2.5-VL-3B · QLoRA r=8/α=16 · freeze-vision             │
 │          LLaMA-Factory · 1 GPU Colab                                │
 │          [+ ablation: aux MV bật/tắt — nếu không lợi thì bỏ]        │
 └───────────────────────────┬────────────────────────────────────────┘
                             ▼
     ┌──────────────── ĐO (dual eval) ─────────────────┐
     │                                                 │
     │  TRỤ CHÍNH: độ ĐÚNG          TRỤ PHỤ: trung thực │
     │  AndroidControl              MobileViews         │
     │  app-UNSEEN split            (tắt VH lúc sinh)   │
     │  coverage action∧target      Tier2: student bịa? │
     │  Student vs Teacher-BASE     matcher nhiều-tầng  │
     │  (đã validate bơm-lỗi)       (báo dù null)        │
     └──────────────────────┬──────────────────────────┘
                            ▼
        ScreenSpot-v2 (đối chứng grounding, không headline)
        + Chương đo-lường K1/K2/OCR/VIỆC1 (đóng góp mới)
```

Luật vàng chống leak GIỮ NGUYÊN: **app ở test-split KHÔNG xuất hiện lúc train** (held-out chuẩn của AndroidControl); VH/gold chỉ vào lúc CHẤM.

---

## Vì sao chốt vậy (neo 4 mũi, phân biệt peer-reviewed/preprint)

**Trục ĐÚNG lên chính, in-distribution held-out (không cross-dataset) — đồng thuận cả 4 mũi, mạnh nhất ở Mũi 4.** K2 (report/74) đã giết trục lọc-bịa ở tầng thực nghiệm: teacher bịa ~0, 35/40 ca "bịa" là nút thật bị VH bỏ nhãn → data-LỌC ≈ data-THÔ → Tier 1 null tầm-thường (kiểu null tệ nhất: không đọc được). Trục ĐÚNG miễn nhiễm K2 vì "guide có đúng không" đo được bất kể teacher bịa hay không. **Điểm khác report/78:** report/78 còn dùng khung cross-dataset (train MV → chấm AC) với giả định "lệch-miền tác động ĐỒNG NHẤT mọi nhánh" — **không kiểm định được** (MV không gold nên không test parallel-trends), là "đòn giám khảo khó bác sạch". Chuyển sang train + eval **in-distribution trên app-unseen split của chính AndroidControl** xoá luôn confound đó: test-app không thấy lúc train là held-out chuẩn, không circular.

**So gold `step_instructions` (không map coord→a11y→tên) — phát hiện report/79.** Pilot: map `gold(x,y)→a11y→tên` chỉ ~40% (48% click là icon/ảnh không chữ; a11y-tree không có ở mirror nhẹ). Nhưng AndroidControl có sẵn gold `step_instructions` do người viết, phủ ~100% bước, chất lượng tốt ("Click on the Gmail tab at the bottom left corner"). Đây là gold ĐÚNG loại output của luận văn (hướng dẫn cho người ĐỌC) → **gỡ khe construct-validity** agent-action-vs-người mà report/78 tự nhận chưa dập được.

**Train đa-bộ GUI là chuẩn ngành, không thể bị đánh "ghép data tùy tiện" (Mũi 1).** Tiền lệ peer-reviewed: SeeClick (**ACL 2024**), OS-Atlas (**ICLR 2025**¹), UGround (**ICLR 2025**¹), Aguvis (**ICML 2025**). Đóng góp KHÔNG ở việc trộn mà ở: (i) output-type = hướng-dẫn-ngôn-ngữ-cho-người (không phải toạ độ/action-token như cả dòng grounding), (ii) đánh-giá-kép gold+no-gold, (iii) on-device 3B.

**Tính mới còn phòng-thủ-được — nhưng phải khai thẳng nó MỎNG (Mũi 3+4).** "Model 3B distilled on-device cho GUI" đã bị ba bài peer-reviewed chiếm: ZonUI-3B (**WACV 2026**), UI-R1 (**AAAI 2026**), LLaVA-KD (**ICCV 2025**) — tất cả output action-cho-máy hoặc miền-tổng-quát. Chỗ trống chưa scoop = **sinh hướng-dẫn nhiều-bước cho NGƯỜI ĐỌC + đánh-giá-kép**; nửa no-gold phân định với FaithScore (**Findings EMNLP 2024**): họ self-probe bằng VQA, ta verify bằng nguồn cấu-trúc-ngoài (VH). **Trung thực:** train trên gold đẩy đề tài từ "chưng cất + lọc" về gần "supervised-trên-gold" — ĐỪNG giả vờ bộ lọc còn là đóng góp sống (K2 đã giết nó ở tầng thực nghiệm). Tính mới dời hẳn sang output-type + dual-eval + chương đo-lường. Nếu hội đồng không mua framing này thì đây là rủi ro số 1, **không dập bằng số được** → nên hỏi thầy trước khi cam kết.

**Thước phải nhiều-lớp, validate bơm-lỗi là CỔNG (Mũi 2).** Trụ peer-reviewed chắc cho phần method: Sai (**EMNLP 2021**, validate bơm-lỗi), BERTScore (**ICLR 2020**, lý do không dùng sim thuần), AndroidControl (**NeurIPS 2024**, decomposition action∧target), Panickssery (**NeurIPS 2024**, judge tự-thiên-vị), Procedure-Planning ECCV 2020 (bậc mIoU/mAcc/SR), ALOHa (**NAACL 2024**), Fagin (SIAM 2006) + Lapata (CL 2006) cho order-τ partial, AITW (**NeurIPS 2023**) cho dung sai 14%.

**Preprint — chỉ acknowledge, ĐỪNG xếp ngang trụ:** MobileViews (2409.14337), LiteGUI (2605.07505), AutoDroid-V2 (2412.18116), ScreenSpot-Pro, AndroidControl-Curated (2510.18488), RAP (2403.18600), executable-plan (2210.04964), DeltaScore (Findings EMNLP 2023 — verify). **Verify phiên trước khi in:** STaR (NeurIPS 2022), CapFilt/BLIP (ICML 2022), VGA (EMNLP 2024), OS-Atlas/UGround OpenReview.

---

## Việc kế theo thứ tự (FREE trước, TỐN TIỀN sau)

**A. FREE — làm trước, không cần GPU/API:**
1. **Đối chiếu report/56 (pre-register đã commit).** Đổi trục chính = phải cập nhật estimand/ngưỡng ở report/56 + **commit lại TRƯỚC khi train**. (Chưa đọc trực tiếp report/56 phiên này — bắt buộc mở.)
2. **Tải AndroidControl-test về local một lần** (step_instructions + ảnh; đừng stream, mirror chập chờn). Pre-register: app-unseen split + lát gần-miền (AndroidControl-Low + app-category trùng) + phân biệt gold-step **bắt-buộc vs tự-do** (suy từ gold theo nhân quả).
3. **Đếm rộng chất lượng gold `step_instructions`** (report/79 mới verify 30 ep/159 step — đếm thêm để chắc không nhiều bước mơ hồ "tap the item").
4. **Build + bơm-lỗi-validate thước so-instruction** (không cần model). ← **CỔNG:** rớt bảng bơm-lỗi (nhất là tách-phân-phối AUC≥0.80) thì dừng, sửa thước.
5. **Mini-study construct-validity ~30-50 mẫu** (chấm-người, free).
6. *(Nâng cấp tuỳ chọn)* **Đếm label-coverage a11y-tree AndroidControl-full** trước khi quyết có tải bản nặng.

**B. TỐN TIỀN — chỉ sau khi A qua cổng (HỎI USER trước mỗi bước ✱):**
7. ✱ Build trainset: AC-gold (chính) [+ MV-distilled aux đã vá matcher/cân nhắc bỏ fallback-rewrite vì VIỆC1 cho thấy nó hại].
8. ✱ Pilot train nhỏ kiểm xung-đột-phong-cách (văn-tự-do MV vs step-instruction ngắn AC) — gắn tag-nguồn trong prompt nếu cần.
9. ✱ Train Student QLoRA r=8/α=16 freeze-vision, LLaMA-Factory, 1 GPU Colab (+ ablation MV on/off nếu ngân sách cho).
10. Eval: Student vs Teacher-BASE trên AC held-out (chính) + MV faithfulness Tier 2 (phụ).
11. Viết chương đo-lường K1/K2/OCR/VIỆC1.
12. Gặp thầy với khung này.

---

## Rủi ro + cắt gì nếu quá tải

**Rủi ro:**
- **Tính-mới mỏng** (rủi ro số 1, không dập bằng số): "SFT 3B trên AndroidControl gold" nhìn giống việc đã có. Phòng thủ duy nhất = framing (output-type cho-người + dual-eval + chương đo-lường) + giữ sợi distillation ở MV-aux. Nếu thầy không mua → cần MV-aux tạo khác biệt, nhưng MV-aux có thể ablation ra 0. **Hỏi thầy trước khi cam kết.**
- **Circular ngược chiều:** train trên gold rồi chấm bằng cách so với gold (held-out) → điểm cao một phần vì học đúng *phân bố câu chữ* metric thưởng. Chống bằng: mốc Teacher-BASE + thước ưu tiên khớp action∧target (bớt nhạy phong cách) + báo hiệu Student−Teacher có ý nghĩa chứ không chỉ khớp-giọng.
- **Xung đột phong-cách-output khi trộn** (văn-tự-do MV vs step ngắn AC): model 3B có thể "trung bình hoá" thành giọng nhạt. Pilot nhỏ + tag-nguồn trước.
- **Trích entity từ văn tự do dễ hỏng** — có thể chỉ dời chỗ fragile của K1. Phải validate riêng bộ tách action/entity (P/R trên tập gán-tay) trước khi tin Lớp A.
- **~48% click AndroidControl là icon/ảnh** → entity "settings icon" khớp lỏng hơn "Gmail tab". **Báo tách nhóm text-target vs icon-target**, đừng gộp một số.
- **In-distribution vẫn có thể ra số nhạt** nếu 3B sinh guide quá kém — nhưng vẫn đọc-được (có Teacher-BASE làm mốc), ít khả năng null-không-đọc-được. Chưa chạy model sinh trên AC → cổng "không suy biến sàn-0" chưa qua.

**Cắt gì nếu quá tải (thứ tự cắt):**
1. Ablation MV on/off (tốn một lượt train) → chỉ train "both".
2. AndroidControl-full bản nặng (nâng cấp tuỳ chọn) → dùng mirror nhẹ + khai giới hạn cross-dataset cho trục no-gold.
3. Trục TRUNG THỰC / Tier 2 (gần-miễn-phí nên cắt cuối) → về AC-only làm **sàn lui hợp lệ**.
4. LLM-judge khác-họ (chỉ cross-check, không headline) → bỏ, giữ thước action∧target + κ-người.
5. ScreenSpot-v2 đối chứng (đã tuỳ chọn) → bỏ.

**KHÔNG cắt (xương sống):** trục ĐÚNG in-distribution trên AC + validate-bơm-lỗi (cổng) + chương đo-lường + artifact model 3B (yêu-cầu-cứng của thầy).

---

*Ghi chú trung thực về chính file này:* tổng hợp từ 4 mũi + report/74/76/78/79/80. **Chưa tự mở lại phiên này:** report/56 (pre-register — BẮT BUỘC đối chiếu trước khi train), report/73/75 đầy đủ. Con số dataset (833 app/15.283 ep AC; 498/220 MV) lấy từ ghi-chú-đã-verify của dự án (CLAUDE.md), verify trước khi in. Venue OS-Atlas/UGround (ICLR 2025) + phiên STaR/CapFilt/VGA — verify OpenReview/proceedings trước khi ghi "peer-reviewed". Chấm bán-định-lượng A≪B≲LAI (report/78) kế thừa hướng, không kiểm lại độc lập.
