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

# PHẦN B — PLAN HOÀN THÀNH (12/7 → 30/8) — **BẢN 2 (đã áp 12 sửa từ Fable stress-test plan)**

> Bản 1 do lượt review đầu viết. **Bản 2 (2026-07-12)** vá 11 lỗi thực thi (L1–L11): tuần-2-trống↔tuần-3-quá-tải, GATE-3 tự-mâu-thuẫn, thiếu task viết luận-văn-chính, 2 lỗi thứ-tự-hiệu-chuẩn, nghẽn CPU local, plan-stale. **Nguyên tắc tái cấu trúc: mọi việc KHÔNG cần checkpoint phải xong TRƯỚC khi có checkpoint.** Khung mốc/gate/fallback bản 1 giữ nguyên.

Ký hiệu: ✱ = tốn tiền, HỎI USER trước · [GATE] = điểm quyết định · DoD = tiêu chí xong.

## Bảng mốc — TICK KHI QUA GATE (chống plan hoá văn-bia)
| Mốc | Ngày | Điều kiện qua | ✔ |
|---|---|---|---|
| **M0** Prereg 56 vá 4 lỗ + commit | 12/7 | commit `2c84ce8` | ✅ **XONG** |
| **M0b** Doc-sync (00/CLAUDE split-đã-commit) | 12/7 | khớp git | ✅ **XONG** |
| **M1** MDE điền + ngưỡng khoá (commit 2) | ~16/7 | GATE-1 | ☐ |
| **M2** Data SFT ×2 sạch + smoke-train OK | 19/7 | GATE-1b | ☐ |
| **M3** 2 checkpoint hội tụ + gate tiếng Việt | 26/7 | GATE-2 + GATE-3 | ☐ |
| **M4** Bảng số Tier1/2 + perturbation | 5/8 | **GATE-3b** | ☐ |
| **M5** Draft FAIR đầy đủ → gửi thầy | 10/8 | — | ☐ |
| **M6** Nộp FAIR | 13–14/8 | GATE-4 (8/8) | ☐ |
| **M7** Nộp VCL | 27–28/8 | — | ☐ |
| **M8** Luận văn chính (quyển) | sau 30/8 | deadline trường | ☐ |

*Quy tắc: mỗi lần qua gate → tick + 1 dòng ghi chú ngày thực tế. Mỗi tuần chừa ~1 ngày KHÔNG gán task; việc tràn ăn vào ngày đó TRƯỚC khi ăn vào gate.*

## TUẦN 0 (12–13/7): khoá pre-registration + de-risk hạ tầng
| Task | Việc | DoD | Công |
|---|---|---|---|
| ~~T0.1~~ | ~~Vá 4 lỗ report/56~~ | ✅ commit `2c84ce8` | — |
| ~~T0.2~~ | ~~commit report/56~~ | ✅ | — |
| ~~T0.3~~ | ~~vá "split chưa commit" report/00~~ | ✅ (00 đã đúng; CLAUDE 1-dòng đã sửa) | — |
| **T0.4** | Smoke-test tiếng Việt **BASE** (Ollama, free, 5 màn) — quyết hướng VCL tạm | 5 output đọc được/không | 1–2h |
| **T0.5** | USER tra: CFP VCL2026 · dual-submission 2 venue · FAIR gia hạn · **+ tải template/CFP FAIR (giới hạn trang/format)** | 4 câu có nguồn | 1h (user) |
| **T0.6** ★mới | **Email thầy HÔM NAY**: hẹn lịch gặp tuần 20–26/7 + gửi trước 1 trang tóm tắt (sơ đồ có-sẵn-vs-tự-train + kế hoạch 2 bài + khả năng Tier-2 null) | email đã gửi | 30' |
| **T0.7** ★mới | **Sanity hạ tầng local**: `ollama serve` + đủ 4 model + **đo throughput qwen2.5vl:3b/CPU trên 3 màn** (verify: server đang TẮT). Chậm >~3'/lệnh → ghi 2 nhánh: (i) ✱sinh câu hỏi bằng API gpt-4o-mini ~$0.5–1, (ii) dồn lên Colab | có số phút/lệnh + nhánh chọn | 30' |
| **T0.8** ★mới | USER hỏi trường: **deadline nộp quyển luận văn + lịch bảo vệ** (deadline duy nhất KHÔNG có trong mọi tài liệu) | có ngày | (user) |

**[GATE-0]** ✅ đã tuân thủ — không API nào chạy trước commit `2c84ce8`.

## TUẦN 1 (13–19/7): data + MDE + smoke-train SỚM
- **T1.1** Fetch/hoàn tất pool train (đã có **498 màn/220 app sau dedup** `mv_train_pool/`) + assert K-leak pool∩12test = ∅ có log. *(free)*
- **T1.6→ĐẢO LÊN TRƯỚC** Hiệu chuẩn matcher **τA** bằng AndroidControl (~100–120 step ngoài eval) → P/R + κ, **precision ≥0.95**. Rớt → chỉnh τA/rebuild TRƯỚC khi build data (rẻ). *(free/local)*
- **T1.2** ✱(~$0.1) **Pilot MDE**: teacher BASE ~4–5 **TRAIN-app** (KHÔNG đụng 12 test) → Var(f_teacher) → điền `[MDE]` §6 → **commit lần 2**. **Chấm-cho-MDE (vá L4):** hiệu chuẩn **τB sơ bộ ngay từ output pilot** (gán tay nhanh) HOẶC khai 1 câu trong commit-2: *"SD ước lượng bằng bộ chấm tạm; τB chính thức freeze trước eval — phương sai nền không lộ hướng hiệu ứng nên không phá pre-reg"*. **[GATE-1]** MDE ≤15–20pp → giữ 18/12; ngược lại **re-split 15/15 → chạy LẠI K-leak + commit lại prereg**.
- **T1.3** Sinh câu hỏi train (theo nhánh T0.7: local nếu đủ nhanh, else API/Colab) + duyệt lướt (không câu chứa tên nút).
- **T1.4** ✱(~$1–2, đo `DG1_LIMIT=30` trước) **Teacher BASE full** ~3.000 lệnh. **Tách (vá L5):** phần **pool-220 chạy song song ngay** (bất biến với re-split, pool disjoint 30 app); phần **18-app-clean + eval-questions CHỜ GATE-1**. Quota ~3.000 đã gồm ~1.720 train + ~380 eval (12 test + 18 train-app cho Δ_train) → KHÔNG xin duyệt API lần 2.
- **T1.5** (sau T1.6✔ + GATE-1✔) Matcher τA + rewrite fallback + render → `sft_train.json` (lọc) + `sft_raw.json` (thô); chạy lại K-leak + spot-check 20 mẫu.
- **T1.7** ✱(Colab Pro $10) **Smoke-train SỚM 14–16/7** bằng **20 mẫu từ cache app1 cũ** (KHÔNG chờ data mới — de-risk LLaMA-Factory, phần "lần đầu hay vướng 3–5 ngày"): dựng LLaMA-Factory, YAML Phụ lục C, checkpoint→Drive, resume. **[GATE-1b]** dựng OK → GO train full khi data sẵn.
- **T1.8** ★mới Chuẩn bị sẵn **gói contingency GATE-2**: script sinh target tiếng Việt (chưa chạy) + đoạn prereg-amendment viết sẵn (+$0.2–0.5 dự phòng).

## TUẦN 2 (20–26/7): train chạy nền + DỒN việc-không-cần-checkpoint (vá L1)
- **T2.1/T2.2** Train **Student** (data lọc) + **Student-RAW** (data thô, cùng hyperparam/apps) full, qua đêm — best checkpoint theo dev-loss held-out-by-app. *(chạy nền, không ngồi canh)*
- **T2.3** Test **GGUF export NGAY checkpoint đầu**; fail → dự phòng safetensors + infer Colab (quyết đường inference bằng phép đo, không bằng hy vọng).
- **T3.1→KÉO LÊN** Hiệu chuẩn **τB** bge-m3: 80–120 cặp gán tay, P/R + κ, **freeze** (chỉ cần output teacher — đã có từ T1.4).
- **T3.4→KÉO LÊN** Dựng **perturbation harness** (bơm lỗi độc lập matcher — chỉ cần metric + output teacher). Trả nợ claim C2 FAIR.
- **T2.6** ★mới **Viết trước FAIR** phần Intro/Related/Method (nguyên liệu: report/57 related-work + report/54) + **dàn khung chương luận văn**.
- **T2.5 [GATE-2]** Re-test tiếng Việt trên **Student checkpoint** (rủi ro #2 language-drift). Drift → trộn 5–10% target Việt + retrain (dùng gói T1.8, ghi amendment TRƯỚC) HOẶC chốt VCL = bài phương-pháp. ⚠ Nếu rẽ retrain → **VCL tạm phụ thuộc checkpoint**, không còn hoàn toàn ngoài đường-găng.
- **T2.7** Gặp thầy (đã hẹn từ T0.6): sơ đồ có-sẵn-vs-tự-train + bảng 7 bài + **nói thẳng khả năng Tier-2 null** + trình kế hoạch 2 bài (nếu thầy bác trục 2-bài, biết SỚM để đổi đuôi plan).

## TUẦN 3 (27/7–2/8): CHỈ inference + chấm + thống kê (đã nhẹ nhờ tuần 2)
- **T3.2** Inference Student + Student-RAW trên **12 test-app VÀ 18 train-app** (cho Δ_train); f_teacher tái dùng BASE. *(đường inference đã chốt ở T2.3)*
- **T3.3** Chấm 3 cơ chế (τB đã freeze ở tuần 2) + %fallback + silent-error + **tỉ-lệ-màn-0-nhắc-nút**.
- **T3.5** Sign-flip exact Tier 1 + Tier 2 + Holm + đối chiếu 3-kết-cục prereg + phép-đo hữu-ích phụ.

**[GATE-3, 28/7 — đo TRAIN]:** 2 checkpoint hội tụ (dev-loss ổn) + **đường inference đã thông** (GGUF OK hoặc Colab đã test) → tiếp. Chưa → cảnh báo đỏ. *(khớp M3=26/7, KHÔNG còn tự-mâu-thuẫn như bản 1.)*

## TUẦN 4–5 (3–15/8): điền Results + polish FAIR (Intro/Related/Method đã viết tuần 2)
Điền Results/Discussion (số từ T3.5) → polish + rà tiếng Anh. **10/8 gửi thầy duyệt draft** (nếu thầy đồng tác giả). **Nộp 13–14/8.**
- **[GATE-3b, 5/8 — đo EVAL, MỚI]:** bảng số chính (Tier1+Tier2+MDE) **đã đủ trong draft** → đi tiếp; **CHƯA đủ số → BỎ FAIR** (dồn VCL + luận văn). *(Đây mới là gate thật quyết sống-chết FAIR, thay vai "GATE-3 28/7" mơ hồ của bản 1.)*
- **[GATE-4, 8/8 — quy tắc nhị phân]:** bảng kết quả chính đã đầy đủ trong draft → tiếp tục nộp bản đạt-chuẩn dù văn chưa đẹp (văn xấu sửa được 5 ngày); bảng chính CÒN THIẾU số → bỏ FAIR. **KHÔNG lập kế hoạch dựa trên gia hạn.**

## TUẦN 6–7 (16–30/8): bài VCL (tiếng Việt)
- **T6.1** Student sinh hướng dẫn tiếng Việt trên 12 test-app (local nếu T0.7 xác nhận đủ nhanh).
- **T6.2** Chấm no-gold (tên nút English trong câu Việt vẫn so VH) + so arm English (lượng hoá suy giảm chuyển-giao) + taxonomy lỗi (bịa/lẫn Anh/dịch sai tên nút).
- **T6.3** Viết VCL (nếu GATE-2 rẽ fallback → headline perturbation, tách mạnh khỏi FAIR).
- **T6.4** Nộp **~27–28/8** (buffer vì deadline 30/8 chưa verify).
- *Nếu FAIR bị bỏ ở bất kỳ gate nào → thời gian dôi chuyển thẳng sang **viết chương luận văn**, KHÔNG "nghỉ".*

## TUẦN 8+ (sau 30/8): LUẬN VĂN CHÍNH ★mới (vá L3)
Quyển luận văn ~**8–15 ngày** bằng **tái chế**: bài FAIR = lõi chương Mô hình + Thực nghiệm · VCL = chương ứng dụng tiếng Việt · report/54 = chương phương pháp → viết quyển chủ yếu là dịch/ghép/mở rộng. **Ràng buộc: xác nhận deadline nộp quyển + lịch bảo vệ (T0.8) NGAY tuần 0** — nếu bảo vệ rơi tháng 9–10 thì chuỗi FAIR→VCL→quyển phải nén.

## Đường-găng + chi phí
**Đường-găng (rút gọn nhờ tái phân bổ):** M0✅→T1.6(τA)→T1.2(MDE/GATE-1)→T1.4(teacher)→T1.5(SFT)→T1.7(smoke)→T2.1/2.2(train)→T3.2/3.3/3.5(eval)→GATE-3b(5/8)→điền Results→FAIR. Tuần 3 từ ~7–9 ngày-người xuống ~4–5; "viết FAIR 13 ngày 0-buffer" thành "điền số 10 ngày có draft sẵn". **VCL ngoài đường-găng** (trừ khi GATE-2 rẽ retrain).

**Tốn tiền cần duyệt (~$65–80, vẫn <$100):** ① pilot MDE ~$0.1 · ② teacher full ~$1–2 · ③ Colab Pro $10 (tuần 1) · ④ Colab Pro+ $50 (tuần 2–3) · ⑤ dự phòng inference ~$0–5 · ⑥ ★câu-hỏi-qua-API nếu CPU chậm ~$1 (L6) · ⑦ ★target Việt nếu GATE-2 rẽ ~$0.5 (L10).

## VIỆC LÀM NGAY HÔM NAY (12/7) — cập nhật
1. ~~Vá + commit report/56~~ ✅ · ~~doc-sync~~ ✅
2. **T0.4** Smoke-test tiếng Việt base (5 màn, free) — nhưng làm SAU T0.7 (cần Ollama chạy).
3. **T0.7** Sanity Ollama (`ollama serve` + đo throughput CPU) — **chặn nhiều bước "free local"**.
4. **T0.6** Email thầy hẹn lịch + gửi tóm tắt 1 trang.
5. **T0.5 + T0.8** Bạn tra: CFP VCL2026 + dual-submission + template FAIR + **deadline quyển/lịch bảo vệ trường**.
6. Xin duyệt chi ①+② (pilot MDE + teacher full).

*Kết luận (bản 2): thiết kế khoa học KHÔNG lỗ chí mạng; **plan bản 1 có 11 lỗi thực thi đã vá** — quan trọng nhất là dồn việc-không-cần-checkpoint sang tuần 2 để tuần 3 không tự bóp chết FAIR, tách GATE-3(train)/GATE-3b(eval, 5/8), và thêm task viết-luận-văn-chính + de-risk hạ-tầng-CPU + quan-hệ-thầy. Kịch bản trượt FAIR dễ xảy ra nhất KHÔNG phải "null khoa học" mà là "lịch tự bóp" — bản 2 xử đúng chỗ đó.*
