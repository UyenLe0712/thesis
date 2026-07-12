# 🔴 REVIEW SÂU DG1 TRƯỚC KHI CHẠY CHÍNH (2026-06-30)

> **Cách làm:** 3 agent độc lập review song song — (1) phản biện adversarial như hội đồng, (2) kiểm chứng citation + chuẩn-mực metric (WebSearch), (3) audit code harness tìm bug/tốn-tiền. Ba bên **hội tụ** vào cùng lỗi sống còn.
> **Phán quyết: KHÔNG chạy chính cho tới khi vá ① + ⑨ (bắt buộc). Nếu chạy ngay → kết quả TAUTOLOGY không đăng được + tốn tiền.**

---

## 0. KẾT LUẬN 1 DÒNG
Phương pháp **nền tốt nhưng có 1 lỗi sống còn (vòng lập-luận matcher)** khiến headline hiện tại (Faithfulness 100%) **vô nghĩa về mặt logic**; cộng 1 giới hạn bản chất (**DG1 không đo được đúng-ý, chỉ đo tự-nhất-quán**). Cả hai **vá được** trước khi chạy — và phải vá, nếu không tiền chạy ra số không dùng được.

---

## ① LỖI SỐNG CÒN — Vòng lập-luận matcher (CAO; cả agent phản-biện lẫn audit-code bắt độc lập)
**Sự việc (đẳng-thức, không phải thực nghiệm):** matcher ALOHa (`nomic-embed`, cosine ≥ **τ=0.55**) được dùng ở **hai chỗ cùng một lúc**:
- **SỬA** (`dg1_run.py:47-48`, `apply_designE`): bước nào matcher nói "không khớp" → sửa/fallback.
- **CHẤM** (`dg1_score_all.py`): `Faithfulness = 1 − (bước trỏ nút không tồn tại)/n` — *cũng* bằng matcher đó.

⇒ design-E chạy **cho tới khi matcher hài lòng**, rồi **chính matcher đó** chấm → **Faithfulness design-E không thể < 100%**. Đây là **100% do định nghĩa**, không phải "phần lớn do thiết kế". `+24.6pp` thực chất chỉ là `100 − tỉ-lệ-bịa-BASE`.

**Đúng-nhãn +21.9pp cũng nhiễm:** bước SỬA được đưa **danh-sách-nhãn-thật từ oracle** và bảo "chọn 1" → tên chọn ra **đương nhiên trùng khít** một nhãn thật → đúng-nhãn của bước-đã-sửa **được bảo đảm**. Nên +21.9pp **phần lớn là tạo-tác của vòng lặp**, không phải bằng chứng độc lập.

> Vi phạm đúng quy ước CLAUDE.md đã ghi: **"metric chấm ≠ verifier V1"**.

**VÁ (bắt buộc, trước khi chạy):**
- **Tách công cụ:** matcher SỬA (nomic) ≠ matcher CHẤM. Chấm Faithfulness/Grounded bằng **matcher ĐỘC LẬP họ khác** — `text-embedding-3` / `BGE-M3`, hoặc **LLM-judge khác họ** trên subset, hoặc token-overlap (`dg1_scorer.match`). Code: ở `dg1_score_all.py` đổi `from aloha_match import best_match` sang matcher khác.
- Khai thẳng: design-E Faithfulness = **trần do-thiết-kế (by-design ceiling)**, KHÔNG phải kết quả. Số thực-nghiệm hợp lệ duy nhất = **tỉ-lệ-bịa BASE** (đo độ-lớn vấn đề).

---

## ② GIỚI HẠN BẢN CHẤT — DG1 (MobileViews, no gold) đo TỰ-NHẤT-QUÁN, KHÔNG đo ĐÚNG-Ý (CAO)
Matcher chỉ bảo "khớp MỘT nút thật", **không** bảo "khớp ĐÚNG nút theo ý định". design-E có thể sửa nút-ma → **nút-thật-nhưng-SAI** (vd "Confirm" → "Save" trong khi đúng là "Submit") và vẫn ghi **100% faithfulness + 100% đúng-nhãn** — thậm chí **nguy hiểm hơn** BASE (lỗi im-lặng thay lỗi lộ-liễu).

⇒ **MobileViews/DG1 KHÔNG thể đứng làm kết quả "đúng/hữu ích" chính.** Claim đúng-việc cần **gold** ⇒ thuộc **AndroidControl (Step-SR)**.

**Claim DG1 HỢP LỆ (thu hẹp, trung thực):**
- (a) **Đo tỉ-lệ-bịa BASE** (~24.6%) = lượng-hoá vấn đề hallucination — đóng góp đo-lường thật.
- (b) **design-E giảm tham-chiếu nút-KHÔNG-tồn-tại** (chấm bằng matcher ĐỘC LẬP) + **audit % bước-sửa-đúng-ý** trên subset có gold/chuyên-gia (để bác lo "sửa thành nút-sai").
- (c) **Phương pháp đánh giá** khi không có gold (đóng góp B).

---

## ③ HEADLINE REFRAME (CAO — framing)
- Bỏ Faithfulness-100% khỏi bảng "thắng". Trình lại: **"đo được tỉ-lệ-bịa BASE = 24.6% [CI]"**; design-E Faithfulness ghi **by-design + caveat ②**.
- **Bỏ bootstrap-CI** trên đại-lượng tất-định (design-E≈100%) — CI trên hằng-số-do-thiết-kế là **gây hiểu lầm** (ngụ ý có bất định lấy mẫu không tồn tại).
- **THÊM cột "% bước fallback"**: fallback `(describe)` bị loại khỏi mẫu-số-bịa → chính là **đường gaming** faithfulness; phải cho hội đồng thấy cái giá.

---

## ④ VALIDATE METRIC — perturbation ĐÚNG nhưng KHÔNG ĐỦ (CAO; rủi ro không-đăng-được)
- **Perturbation chứng minh:** độ-nhạy/đặc-hiệu với lỗi **tự bơm** (sensitivity / known-groups validity). Có tiền lệ chính danh: **Sai et al., "Perturbation CheckLists for Evaluating NLG Evaluation Metrics", EMNLP 2021** (thêm cite này).
- **KHÔNG chứng minh:** convergent/criterion validity (tương quan phán-đoán-người / hữu-ích-thật); không lộ được unknown errors; và "nút-ma" trong test lại do **chính matcher** định nghĩa → vòng tròn lần nữa (lỗi bơm phải định-nghĩa ĐỘC LẬP matcher: người soạn, hoặc lấy tên từ app khác).
- **Chuẩn ngành:** ở venue về metric (BLEU/BERTScore/COMET…), **tương quan người là bằng chứng validity CHÍNH**; perturbation = cần-nhưng-không-đủ. Hội đồng NLP sẽ hỏi thẳng *"human correlation đâu?"*.

**VÁ:** giữ perturbation làm **một trụ**; **khôi phục tương quan CHUYÊN-GIA nhỏ, pre-register (N≥50, báo Krippendorff α + Kendall)** làm convergent validity — đóng khung **"expert-gold, KHÔNG phải crowd grading"** (dung hoà việc thầy không ưa chấm-người). ⚠️ **PHẢI BÀN VỚI THẦY.**
**Mâu thuẫn nội bộ phải gỡ:** `14`/`05` vẫn để Krippendorff α + Track B làm meta-eval headline, còn `22`/`25` hạ xuống tùy-chọn → hai chỗ đá nhau = điểm bị tấn công.

---

## ⑤ THỐNG KÊ (TRUNG → CAO)
- 🔴 **Clustering theo APP chưa xử lý:** thử-chạy trên **~1 app** → màn cùng app KHÔNG độc lập → phải **cluster bootstrap (resample APP → màn)**; nếu không CI **giả-chặt**, n-hiệu-lực ≪ 80. Báo **#app**; lấy màn **trải nhiều app**.
- **Đa-kiểm-định:** ≥2 metric headline → **Holm-Bonferroni** (hiện chỉ áp cho đa-N của DG2).
- **Resample 2000 → 10000** (rẻ, đuôi 95% ổn hơn) + **seed cố định** (T2).
- Đơn-vị resample = **màn** (đã gộp bước trong màn) — điểm này code làm đúng.

---

## ⑥ τ = 0.55 (CAO — rẻ mà nền-tảng)
Rủi ro: chọn "bằng mắt" → bị bác p-hack; một τ-sai lan khắp SỬA+CHẤM+cổng+perturbation (tự-nhất-quán, lỗi vô hình); phụ thuộc embedder; nhãn ngắn ("OK","Done", icon) cosine bất ổn.
**VÁ (gần như miễn phí):** gán tay **80–120 cặp** quanh ngưỡng (ĐỘC LẬP matcher) → vẽ P–R theo τ → chọn τ theo **quy tắc pre-register** (vd precision ≥ 0.95) → **FREEZE trước khi chạy chính**. Báo **precision/recall matcher** (vá L9). Bỏ bước này → reviewer bác τ → **chạy lại toàn bộ**.

---

## ⑦ CÂU HỎI affordance-seeded (TRUNG → CAO)
- "So-cặp cùng-câu-hỏi nên chất-lượng câu hỏi tự khử" — **đúng một nửa:** ghép-cặp khử **hiệu-ứng-chính cộng tính**, KHÔNG khử **tương tác câu × điều-trị** — mà chính tương tác đó lái effect size (design-E chỉ giúp khi BASE bịa). ⇒ +24.6pp là **hàm của phân bố độ-khó câu hỏi mà nhóm tự chọn** → reviewer: "tự điều chỉnh độ khó cho delta đẹp".
- **Rò rỉ:** gieo X rồi để câu hỏi lộ X ("Add expense" → "Làm sao thêm khoản chi?") → task-success bão-hoà, vô dụng. **Cổng answerability cũng dùng matcher** → giữ lại đúng tập matcher-thân-thiện.
**VÁ:** pre-register **phân bố độ-khó** (proxy: tỉ-lệ-bịa-BASE/câu, #bước, độ-nổi-bật target) + báo effect **theo tầng độ-khó**; đo **overlap lexical câu↔X** loại/tầng-hoá câu lộ X; M1≠M2 (đã có); "tới X" chấm bằng **gold/người**, không bằng matcher.

---

## ⑧ COVERAGE proxy (TRUNG)
Để "28.8→34.6% (limitation)" trong **bảng headline** có hại (hội đồng đọc "bỏ sót 65-70% nút"; design-E coverage cao hơn dễ bị đọc là "chỉ thêm bước cho nhiều"). **VÁ:** trên MobileViews **bỏ coverage khỏi bảng chính → phụ lục**; giữ cặp faithfulness×coverage **CHỈ trên AndroidControl** (có gold). Bắt buộc cột **% fallback**.

---

## ⑨ BUG CODE — vá TRƯỚC khi tốn tiền (audit harness)
| Mã | Nơi | Bug | Hậu quả | Fix |
|---|---|---|---|---|
| **N1** | `dg1_run.py:47` ↔ `dg1_score_all.py` | matcher sửa = matcher chấm | tautology (= điểm ①) | matcher chấm độc lập |
| **T1** | `dg1_run.py:29-41` | `gen_tutorial` import `chat` nhưng KHÔNG dùng → urlopen thô, **không retry** | 429/lỗi mạng → skip → **gọi lại API = mất tiền** | route qua `_http.chat` |
| **T2** | `dg1_score_all.py:50` | bootstrap không seed | CI không tái lập | `random.seed(...)` |
| **T3** | `dg1_score_all.py:41-45` | coverage match trên `labels` nhưng chia `len(actionable)` | coverage có thể >100% / sai tuyệt đối | match trên `actionable` hoặc chia `len(labels)` |
| **T4** | `aloha_match.py:79-82` | `exact_label("")` → `"" in l` luôn True | element rỗng bị tính đúng-nhãn → thổi BASE | guard `if not nn: return False` |
| **S1** | `aloha_match.py:14,37` | cache key chỉ là text, không kèm model | đổi embedder → vector cũ sai âm thầm | key `f"{EMB_MODEL}\t{text}"` |

**ĐÃ XÁC NHẬN ĐÚNG (yên tâm):** không rò oracle lúc sinh (GEN_PROMPT/QPROMPT chỉ ảnh+câu hỏi); `button_steps` loại fallback đúng chỗ + mẫu-số `n` vẫn gồm fallback (bảo thủ, không gaming bằng bỏ-khỏi-mẫu); paired bootstrap đúng phương pháp; bbox parse đúng `[[l,t],[r,b]]` + dùng `Image.size` (không field rác); temp=0; resume/cache không gọi lại màn đã xong; `_apikey`/`_http` không in key.

---

## ⑩ CITATION (8/8 ĐÚNG — chỉ cần chuẩn cách ghi)
| Mục | Phán quyết | Ghi đúng |
|---|---|---|
| ALOHa | ✅ | Petryk et al., **NAACL 2024 short** (2024.naacl-short.30); LLM extract + embedding + **Hungarian** |
| SeeClick | ✅ | Cheng et al., **ACL 2024 long**; **chính là nguồn ScreenSpot** |
| Chim/Ive/Liakata | ✅ | **CL journal 51(1):191-233, MIT Press 2025** (KHÔNG ghi "ACL 2025") |
| IFEval | ✅ (chuẩn ghi) | **Zhou et al., arXiv 2311.07911, 2023 (Google)** — đừng gán hội nghị/năm khác |
| test oracle | ✅ | **Barr et al., IEEE TSE 2015** + gốc **Howden 1978** |
| nomic-embed-text | ⚠️ một phần | MTEB **≈62** (< BGE-M3≈63, < text-embedding-3-large≈64.6, > 3-small≈58); MTEB đo task DÀI → **KHÔNG** bảo chứng tên-nút NGẮN → đóng khung "≈, đã tự-validate trên tên-nút", đừng trích làm bằng-chứng-đủ |
| paired bootstrap | ✅ | chuẩn (Efron-Tibshirani; Koehn EMNLP 2004) — nêu rõ đơn-vị resample |
| perturbation validate | ✅ có tiền lệ | **Sai et al., EMNLP 2021 "Perturbation CheckLists for Evaluating NLG Evaluation Metrics"** — THÊM cite |

---

## CHECKLIST VÁ TRƯỚC KHI TỐN TIỀN (ưu tiên)
1. **① + N1** tách matcher chấm ≠ matcher sửa  ·  **⑥** hiệu chỉnh + FREEZE τ trên tập gán-tay — *nền tảng, chặn re-run.*
2. **②+③** đổi headline: bỏ Faithfulness-100% khỏi "win"; số chính = tỉ-lệ-bịa BASE + metric chấm độc lập; thêm % fallback + audit sửa-đúng-ý.
3. **④** khôi phục tương quan chuyên-gia nhỏ pre-register (bàn với thầy) + gỡ mâu thuẫn 14/05 vs 22/25.
4. **⑤** cluster bootstrap theo app + #app + Holm + 10k + seed.
5. **⑦** pre-register độ-khó câu hỏi + đo rò-rỉ X↔câu hỏi.
6. **⑨ T1-T4, S1** vá code (đặc biệt T1 — tránh mất tiền chạy lại).
7. **⑩** đổi tên "Clarity"→"label fidelity"; thêm cite Sai et al.; đóng khung nomic.

> **Sau khi vá xong + thầy duyệt khung ④ → mới chạy chính (1 lần).**

---

## ✅ XỬ LÝ & KẾT QUẢ CHẠY THỬ (2026-06-30, free, 10 màn cache app1)

**Quyết định: CHỐT PA2** = design-E chỉ **matched/fallback**, **BỎ correction llama**. Lý do thực nghiệm: 10 màn cho thấy correction cũ ép nút-thật-nhưng-SAI (silent error):
- `app1_s1`: `✓` → `Navigate up` (đúng phải là "Submit")
- `app1_s103`: `ADD LOCATION` → `Copy project` (sim 0.49)
- `app1_s121`: `+` → `More options` (sim 0.65)

**Đã hiện thực chống-tautology:** hệ quyết matched/fallback bằng **nomic (τA=0.55)**; CHẤM faithfulness/grounded bằng **bge-m3 ĐỘC LẬP** (`dg1_independent_score.py`, `dg1_pa2_score.py`). Bằng chứng hết-ghim: ở τB=0.80, PA2 faithfulness = **95%** (không phải 100%) → matcher độc lập bắt được 1 bước nomic cho qua.

**Kết quả PA2 (bge-m3, 10 màn, app1):**
| Metric | BASE (τB 0.6→0.8) | PA2 | Đọc |
|---|---|---|---|
| Faithfulness | 90→65% | **100→95%** | chênh **+10..+30pp**, dương ở MỌI τB; **CI chạm 0 (n=10)** → hướng vững, chưa significant |
| Grounded-exist | 90→65% | 70→65% | **GIẢM = cái giá** (fallback không trỏ nút cụ thể; KHÔNG phải "kém grounding") |
| Label-fidelity | 70% | 70% | **no-harm** (PA2 giữ nguyên chữ) |
| Format | 80% | 80% | no-harm |
| fallback | — | **19%** | correction=0, **silent-error=0 (cấu trúc)** |

**CLAIM DG1 thu hẹp (chốt):** DUY NHẤT = *"design-E giảm tham-chiếu-nút-không-tồn-tại, giá = X% fallback"*. **Bỏ** claim "+21.9pp đúng-nhãn" cũ (đó là tạo-tác của correction). Trade-off chính = **faithfulness ↑ đổi bằng grounded-concrete ↓**.

**Còn lại trước khi chạy CHÍNH (API ~$0.05):** (a) màn **nhiều app** (cache 100% app1); (b) hiệu chỉnh + **FREEZE τA**; (c) đơn-giản-hoá `apply_designE`→PA2; (d) cluster bootstrap theo app + Holm; (e) bộ perturbation-test (lỗi bơm độc-lập-matcher).
