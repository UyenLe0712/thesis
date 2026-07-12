# 58 — REVIEW ĐỘC LẬP (Fable 5) + PLAN HOÀN THÀNH LUẬN VĂN (2026-07-12)

> Giám khảo phản biện độc lập (model Fable 5) review toàn bộ project + lập plan thực thi 12/7→30/8.
> Verdict tổng: **ĐẠT-CÓ-ĐIỀU-KIỆN** — thiết kế khoa học vững, KHÔNG lỗ chí mạng, khả thi ở biên với fallback hợp lệ.
> **Đã verify lại các claim then chốt bằng git + đếm file thật (xem §Đính chính).**

---

## ⚠️ ĐÍNH CHÍNH SAU VERIFY (Claude kiểm tra lại git/đĩa — đọc TRƯỚC)

1. **Split 18/12 ĐÃ git commit** (commit `3776212`, 12/7) — chứa `dg3_freeze_split.py` + `train_eval_app_split.json`. → **`report/00 §6` và `CLAUDE.md §0` đang ghi SAI "split CHƯA commit — chờ review"; cần vá.** Bước pre-reg "commit split" coi như XONG.
2. **`report/56_PREREG_MODEL.md` TỒN TẠI** (tạo 12/7 15:03) — là pre-registration THẬT đầy đủ (Tier1/Tier2, ngưỡng PASS/NULL, công thức MDE, Holm, 4 điểm vá thống kê) — **nhưng CHƯA git commit**. → Đây MỚI là bước pre-reg còn treo (không phải split). Ô `[MDE]` §6 để trống đúng thiết kế (điền sau pilot).
3. `mv_train_pool/` thực có **1192 file (~596 màn)**, không phải "130 file/~65 màn" như Fable ước — pool train mở rộng đã fetch NHIỀU hơn Fable tưởng (tốt hơn, không đổi kết luận).
4. Xác nhận đúng: 127 màn/30 app · 286 episode DG2 · `dg1_cache/runs` toàn app1 (1 app, KHÔNG đủ Var liên-app cho MDE → cần pilot mới) · script `dg1_*.py`/`aloha_match.py` khớp tài liệu · công thức thống kê (3.077, 4096, p_min=0.00049) đúng toán.

**Hệ quả cho plan:** T0.2 = "commit split" đổi thành **"vá 4 lỗ + commit `report/56` (prereg ngưỡng)"**; split đã xong.

---

# PHẦN A — XÁC THỰC (verdict)

## A1. Hợp lý khoa học — ĐẠT-CÓ-ĐIỀU-KIỆN
Điểm mạnh: câu hỏi trung tâm (né-bịa có nội-tại-hoá khi tắt-VH?) falsifiable, có thể null; tính-mới thu hẹp trung thực (bảng so 7 công trình); chống-vòng-lặp đúng (lọc nomic ≠ chấm bge-m3+judge+token-overlap).
Lỗ phải vá TRƯỚC khi commit prereg:
- **A1-1** Metric Tier 1 mơ hồ: chưa nói rõ f đo trên output THÔ từng student hay SAU lớp viết-lại PA2. Nếu đo SAU viết-lại → Δ≈0 null giả tạo (tái phạm tautology-trần). Phải ghi: *"f Tier 1 đo trên output THÔ; %fallback báo song song."*
- **A1-2** Màn 0-mention chưa định nghĩa: f = 1−bịa/số-lần-nhắc-nút; student né bằng cách không nhắc nút nào → mẫu số 0. Ghi quy tắc: loại màn 0-mention khỏi f, báo riêng tỉ lệ như chỉ báo né-trả-lời.

## A2. Phương pháp / thống kê — ĐẠT-CÓ-ĐIỀU-KIỆN
Exact sign-flip G=12 đúng công cụ few-clusters; Δ_train mẫu số điều kiện (B) bảo thủ; không lỗ leakage lớn (luật VH-chỉ-lúc-chấm giữ xuyên suốt; K-leak 2 lớp; split commit trước mọi bước tốn tiền).
Lỗ:
- **A2-1** Prereg 56 CHƯA commit — mọi giá trị đăng-ký-trước đang treo. Ưu tiên số 1.
- **A2-2** Prompt teacher lúc eval Tier 2 chưa pre-register: teacher BASE sinh bằng GEN_PROMPT (CÓ "Do NOT invent buttons"), student eval prompt KHÔNG có. Nếu f_teacher lấy từ BASE-có-dặn → student thắng "chấp một câu dặn" (bảo thủ, TỐT — nhưng phải khai tường minh).
- **A2-3** Perturbation-validate được hứa trong abstract FAIR (C2) nhưng KHÔNG trong prereg 56 + chưa có harness. Hoặc đưa vào plan (~1–1.5 ngày) hoặc rút claim khỏi FAIR.

## A3. Khả thi thời gian + compute — RỦI RO (có kiểm soát)
Track model khả thi (QLoRA r=8 3B, tiền lệ ZonUI-3B, $70–100). Nhưng lịch rất sát: 12/7→2/8 = 21 ngày phải rơi cận-trên "thực tế" 0 buffer; FAIR (2/8→15/8 viết tiếng Anh) là điểm nghẽn. Cứu cánh: fallback cứng "bỏ FAIR giữ VCL" đã thành luật + VCL không phụ thuộc Tier 2.
- **A3-1 (rủi ro MỚI, 7 vòng debate bỏ sót vì chỉ soi FAIR):** SFT 100% target tiếng Anh có thể làm student MẤT khả năng xuất tiếng Việt (language drift). Smoke-test tuần 1 chạy trên BASE model → không bắt được (thứ sinh Việt cho VCL là STUDENT sau SFT). Né: re-test tiếng Việt NGAY trên checkpoint SFT đầu (tuần 2, +30'); drift → trộn 5–10% mẫu target Việt (ghi prereg TRƯỚC train chính) hoặc kích hoạt fallback bài-phương-pháp sớm.

## A4. Chuẩn thạc sĩ trường top — ĐẠT
Có model tự train + câu hỏi pre-registered + giao thức đánh giá tự xây + kiểm định exact mẫu nhỏ → vượt sàn constructive/technological. 3 đòn giám khảo mạnh nhất: (1) "LoRA recipe có sẵn + sinh-lọc-train đã có tên 2022 — đóng góp ở đâu?" → khiên SẴN; (2) "student thắng teacher có khập khiễng (3B vs 4o-mini, prompt khác)?" → khiên CHƯA đủ, cần vá A2-2; (3) "12 app đại diện?" → khiên sẵn (56 §8). 2/3 có khiên, 1 cần vá.

## A5. Chiến lược 2 bài — ĐẠT-CÓ-ĐIỀU-KIỆN
Trục tách (câu hỏi + output khác ngôn ngữ + trích chéo) hợp lý, khai trung thực overlap. Điều kiện: 3 sự kiện chưa verify — (1) deadline VCL 30/8 chỉ là trí nhớ; (2) dual-submission policy 2 venue chưa đọc; (3) FAIR gia hạn? → tra ~1h trong 48h tới, không để "trước khi nộp".

## VERDICT TỔNG
**ĐẠT-CÓ-ĐIỀU-KIỆN. Không lỗ chí mạng buộc làm lại.** 5 rủi ro còn lại (2 cái đầu phải xong TRƯỚC khi tiêu tiền):

| # | Rủi ro | Mức | Né |
|---|---|---|---|
| 1 | Prereg 56 chưa commit + 4 lỗ (A1-1, A1-2, A2-2, A2-3) | CAO | Vá 4 đoạn (~2h) + git commit HÔM NAY, trước pilot MDE |
| 2 | Language drift SFT-English làm hỏng VCL | CAO (cho VCL) | Re-test Việt trên checkpoint SFT đầu (tuần 2); drift → trộn target Việt hoặc fallback sớm |
| 3 | Đường-găng FAIR 0 buffer (GGUF bug, hiệu chuẩn tay ngốn ngày) | TRUNG-CAO | Gate cứng 28/7: chưa xong train → bỏ FAIR; train qua đêm; test GGUF ngay checkpoint đầu |
| 4 | 3 sự kiện venue chưa verify | TRUNG | User tra 48h |
| 5 | Tier 2 null/bất định | THẤP-TRUNG (phòng thủ tốt nhất) | 2 tầng độc lập + Tier 1 sớm + nói trước thầy + dose-response nếu dư giờ |

---

# PHẦN B — PLAN HOÀN THÀNH (12/7 → 30/8)

Ký hiệu: ✱ = tốn tiền, HỎI USER trước · [GATE] = điểm quyết định · DoD = tiêu chí xong.

## TUẦN 0 (12–13/7): khoá pre-registration
| Task | Việc | DoD | Công |
|---|---|---|---|
| T0.1 | Vá 4 lỗ vào `report/56`: (a) f Tier-1 đo output THÔ + %fallback song song; (b) quy tắc màn 0-mention; (c) khai f_teacher = GEN_PROMPT-có-dặn (cố ý bất lợi student); (d) thêm mục perturbation-validate HOẶC rút claim khỏi FAIR | 4 mục có câu chữ định lượng | 2–3h |
| T0.2 | `git commit report/56` (+ dọn working tree) — khoá dấu thời gian | `git ls-files` thấy 56 | 15' |
| T0.3 | Vá mâu thuẫn "split chưa commit" trong `report/00 §6` + `CLAUDE.md` (đã commit rồi) | 2 file khớp git thật | 10' |
| T0.4 | Smoke-test tiếng Việt BASE (Ollama, free, 5 màn) | quyết hướng VCL tạm | 1–2h |
| T0.5 | USER tra venue: CFP VCL2026, dual-submission 2 venue, FAIR gia hạn | 3 câu có nguồn | 1h (user) |

**[GATE-0]** Không chạy API nào (kể cả pilot MDE) khi T0.2 chưa xong.

## TUẦN 1 (13–19/7): data + MDE + smoke train
- **T1.1** Fetch full pool train (đã có ~596 màn `mv_train_pool/`; bổ sung nếu cần) + dedup perceptual-hash + assert K-leak ∅ có log. *(free)*
- **T1.2** ✱(~$0.1) Pilot MDE: teacher BASE ~4–5 TRAIN-app (KHÔNG đụng 12 test; cache app1 cũ không đủ) → Var(f_teacher) → điền [MDE] §6 → commit lần 2. **[GATE-1]** MDE ≤15–20pp → giữ 18/12; ngược lại re-split 15/15.
- **T1.3** Sinh câu hỏi train (Ollama local, 3 câu/màn) + duyệt lướt (không câu nào chứa tên nút). *(free)*
- **T1.4** ✱(~$1–2, đo `DG1_LIMIT=30` trước) Teacher BASE full ~3.000 lệnh (resume-able).
- **T1.5** Matcher τA=0.55 + rewrite fallback + render → `sft_train.json` (lọc) + `sft_raw.json` (thô); chạy lại K-leak + spot-check 20 mẫu.
- **T1.6** Hiệu chuẩn matcher bằng AndroidControl (~100–120 step ngoài eval) → P/R + κ, precision ≥0.95.
- **T1.7** ✱(Colab Pro $10) Smoke train 20 mẫu: dựng LLaMA-Factory, YAML Phụ lục C, checkpoint→Drive, resume. **[GATE-1b]** OK → GO train full.

## TUẦN 2 (20–26/7): train 2 bản ✱(Colab Pro+ $50)
- **T2.1** Train Student (data lọc) full qua đêm — best checkpoint theo dev-loss held-out-by-app.
- **T2.2** Train Student-RAW (data thô, cùng hyperparam/apps).
- **T2.3** Test GGUF export NGAY checkpoint đầu; fail → dự phòng safetensors+infer Colab.
- **T2.4 [GATE-2]** Re-test tiếng Việt trên Student checkpoint (rủi ro #2). Drift → trộn 5–10% target Việt + retrain (ghi prereg TRƯỚC) HOẶC chốt VCL = bài phương-pháp.
- **T2.5** Gặp thầy: sơ đồ "có sẵn vs tự-train" + bảng 7 bài + nói thẳng khả năng Tier 2 null + kế hoạch 2 bài.

## TUẦN 3 (27/7–2/8): eval + thống kê — deadline nội bộ model
- **T3.1** Hiệu chuẩn τB bge-m3: 80–120 cặp gán tay, P/R + κ, freeze.
- **T3.2** Inference Student + Student-RAW trên 12 test-app VÀ 18 train-app (cần cho Δ_train); f_teacher tái dùng BASE.
- **T3.3** Chấm 3 cơ chế + %fallback + silent-error + tỉ lệ màn-0-mention.
- **T3.4** Perturbation harness (bơm lỗi độc lập matcher — trả nợ C2 FAIR).
- **T3.5** Sign-flip exact Tier 1 + Tier 2 + Holm + đối chiếu 3-kết-cục prereg + phép-đo hữu-ích phụ.

**[GATE-3, ngày 28/7 — QUAN TRỌNG NHẤT]:** 2 bản chưa hội tụ / eval chưa bắt đầu → **BỎ FAIR ngay**, dồn VCL + luận văn. Không thương lượng.

## TUẦN 4–5 (3–15/8): viết FAIR (tiếng Anh)
Outline+bảng/hình (số từ T3.5) → full draft (Intro/Related theo Phụ lục B; Method theo 54; Results Tier1/2+perturbation) → polish+rà tiếng Anh. **Nộp 13–14/8.** **[GATE-4, 8/8]:** chưa có full draft → nộp "đủ-chuẩn-không-đẹp" hay bỏ. KHÔNG lập kế hoạch dựa trên gia hạn.

## TUẦN 6–7 (16–30/8): bài VCL (tiếng Việt)
- **T6.1** Student sinh hướng dẫn tiếng Việt trên 12 test-app (local, free).
- **T6.2** Chấm no-gold (tên nút English trong câu Việt vẫn so VH) + so arm English (lượng hoá suy giảm) + taxonomy lỗi (bịa/lẫn Anh/dịch sai tên nút).
- **T6.3** Viết VCL (nếu GATE-2 rẽ fallback → headline perturbation, tách mạnh khỏi FAIR).
- **T6.4** Nộp **~27–28/8** (buffer vì deadline 30/8 chưa verify).

## Bảng mốc + đường-găng
| Mốc | Ngày | Điều kiện |
|---|---|---|
| M0: Prereg 56 vá + commit | 12–13/7 | trước mọi API |
| M1: MDE điền, ngưỡng khoá (commit 2) | ~15/7 | GATE-1 |
| M2: Data SFT ×2 + smoke train | 19/7 | GATE-1b |
| M3: 2 checkpoint + gate tiếng Việt | 26/7 | GATE-2 |
| M4: Go/No-Go FAIR | 28/7 | GATE-3 |
| M5: Kết quả Tier1/2 + perturbation | 2/8 | — |
| M6: Nộp FAIR | 13–14/8 | GATE-4 (8/8) |
| M7: Nộp VCL | 27–28/8 | — |

**Đường-găng:** T0.1→T0.2→T1.2(MDE)→T1.4(teacher)→T1.5(SFT)→T1.7(smoke)→T2.1/2.2(train)→T3.2–3.5(eval)→FAIR. VCL nằm NGOÀI đường-găng (chỉ cần 1 checkpoint + eval local) — đúng vai "sàn chắc".

**Tốn tiền cần duyệt (~$62–72):** ① pilot MDE ~$0.1 · ② teacher full ~$1–2 · ③ Colab Pro $10 (tuần 1) · ④ Colab Pro+ $50 (tuần 2–3) · ⑤ dự phòng inference ~$0–5.

## VIỆC LÀM NGAY HÔM NAY (12/7)
1. Vá 4 lỗ vào `report/56` (A1-1, A1-2, A2-2, A2-3) — ~2h.
2. `git commit report/56` — khoá dấu thời gian pre-registration.
3. Vá mâu thuẫn "split chưa commit" trong `report/00` + `CLAUDE.md`.
4. Smoke-test tiếng Việt base (5 màn, free).
5. Giao user tra CFP VCL2026 + dual-submission 2 venue.
6. Xin duyệt chi ①+② (pilot MDE + teacher full).

*Kết luận: KHÔNG lỗ chí mạng thiết kế. Hai chỗ thật sự lo: (1) prereg `report/56` chưa commit trong khi cả giá trị phương pháp đứng trên nó; (2) language-drift cho VCL mà 7 vòng debate bỏ sót (vì soi FAIR). Xử lý 2 điểm này trong 48h thì phần còn lại là kỷ luật thực thi, không phải research thêm.*
