# BÁO CÁO 14 — THIẾT KẾ CUỐI (2026): PIPELINE · METRIC · CÁCH "THẮNG" FRONTIER

> **Trạng thái:** ✅ **ĐÃ CHỐT (2026-06-25).** Người dùng duyệt **design E**; **KHÔNG fine-tune** ở lõi (LoRA = tùy chọn tương lai); **bộ sinh lõi = Qwen mở** (GPT-5/Gemini-3 chạy ít làm đối chứng cross-model). Bước tiếp: **chạy thử trên tập dataset NHỎ**. Thiết kế này đã đồng bộ xuống các file lõi.
> **Mục đích:** sau khi rà sâu literature **2026** (5 agent đối kháng, web-search, kiểm chéo bình duyệt), chốt **pipeline + metric cuối cùng** sao cho (a) ra **kết quả tốt thật**, (b) **ổn định / không lỗi thời** khi GPT-6/Gemini-4 ra, (c) trung thực.
> **Khi duyệt xong:** §9 liệt kê chính xác tôi sẽ sửa gì ở file nào.
> ⚠️ **Liêm chính dữ liệu:** mọi bảng "GPT-5.x / Gemini-3.x ground 86–88%" trôi nổi trên web 2026 là **spam/bịa** (không truy được nguồn OpenAI/Google) — **KHÔNG dùng**. Mọi kết luận dưới đây tựa nguồn **bình duyệt**.

---

> 🔧 **TINH CHỈNH 2026-06-25 (đã duyệt — quan trọng):**
> 1. **TRỌNG TÂM = AndroidControl** (có `goal` THẬT + gold action + ảnh + cây accessibility mỗi màn) → **chở phần lớn metric**: grounding/bịa/đủ-ý TỪNG MÀN + τ-b xếp thứ tự + Step-SR. **MobileViews** = kiểm 1-màn (vai nhẹ, câu hỏi tự soạn). **ScreenSpot** = đối chứng tìm-nút. → claim nặng dựa dataset bình duyệt + goal thật ⇒ khó bị vặn "câu hỏi tự bịa".
> 2. **TÁCH 2 SỐ ở phần "đúng nút"** (do câu hỏi sắc của user): **(a) Bịa (hallucination)** = nút có TỒN TẠI không → matcher **ALOHa (đồng-nghĩa-OK)** để KHÔNG vu oan synonym là bịa; **(b) Đúng-nhãn (clarity/label-fidelity)** = có gọi ĐÚNG tên hiển thị không → so **chính xác** (gọi synonym bị trừ CLARITY, KHÔNG trừ BỊA). *Lý do:* nói "Thiết lập" cho nút "Cài đặt" = người dùng khó tìm (lỗi clarity) NHƯNG nút có thật (không phải bịa) — hai lỗi khác nhau, đo riêng. *(Caveat: nút icon không chữ → không đòi đúng-nhãn được → thêm lý do tách 2 số.)*
> 3. **Cây accessibility AndroidControl ĐÃ VERIFY chở được** grounding/bịa/đủ-ý: serialized proto `AndroidAccessibilityForest` (cài `android_env` để có proto, ~30–50 dòng walk) → mỗi node có `bounds_in_screen` (bbox pixel) + `text`/`content_description` + đủ cờ (`is_clickable`/`is_editable`…). Gold action có **(x,y) pixel = tâm element** → **Step-SR + grounding chạy được KHÔNG cần parse tree**. **AndroidControl-native grounding = point-in-bbox (nhị phân); ngưỡng 14% là của AITW** (giữ trích dẫn đúng). **Pre-register: quy tắc lọc element** (visible + bbox không rỗng) vì nó định mẫu-số bịa/coverage.

## 0. TL;DR (đọc 30 giây)
- **Không thắng GPT-5/Gemini-3 về độ trôi chảy** — và không cần. **Thắng được** trên trục **trung thực/grounding/làm-theo-được**, **trên MỌI model**, ở **chi phí thấp** — đây là câu chuyện *mạnh hơn* và *không lỗi thời*.
- **Pipeline cuối = "lớp trung-thực-hoá độc-lập-model" (design E):** model mạnh nhất (thay được) **SINH theo TÊN nút** → một **oracle grounding đặt BÊN CẠNH** (không chặn khâu sinh) để **chấm + kích fallback**. Detector+SoM+ràng-buộc cũ → **hạ xuống 1 bậc ablation + công cụ đo recall**.
- **Metric cuối:** **cặp faithfulness×coverage** (chống gaming) + point-in-bbox + **τ-b không-cần-judge** + Tier A + **THÊM Followability/Step-SR** (ít gaming nhất) + meta-eval chance-corrected.
- **Đóng góp bền = phương pháp đánh giá + cái lớp** (thay model nào cũng chạy) → GPT-6 ra chỉ làm số đẹp hơn.

---

## 1. CÂU HỎI & TRẢ LỜI THẲNG
**Hỏi:** 2026 có GPT-5/Gemini-3 rồi, hệ của mình làm sao ra kết quả tốt / thắng được, mà ổn định không lỗi thời?
**Đáp:**
- ❌ **Thắng về fluency:** không. Frontier viết hay hơn; cược vào đây là thua.
- ✅ **Thắng về trục yếu đo được** (bịa nút / sai-chỗ / làm-theo-được): có, **honest & lớn**, vì frontier **vẫn yếu đúng chỗ này**.
- ✅ **Bền không lỗi thời:** đặt đóng góp ở **phương pháp + cái lớp độc-lập-model**, báo kết quả thành **đường cong qua nhiều model** → model mới = data point mới, khung vẫn đứng.

---

## 2. BẰNG CHỨNG 2026 — vì sao CÒN CỬA THẮNG (bình duyệt)
- **Frontier vẫn bịa nút UI & sai toạ độ & tự tin thái quá:**
  - *"Do GUI Grounders Truly Understand UI Elements?"* — **Findings of EACL 2026**: 12 model, benchmark "không phản ánh năng lực thật", dò gây lỗi tới **84%**, và **"frontier model bịa cả khi chỉ sinh một câu lệnh".** ⭐ câu trích load-bearing.
  - **HyperClick** (arXiv 2510.27266, preprint): model GUI **miscalibrated** nặng trên UI dày (ECE 0.48–0.63); thêm lớp calibrate cắt ECE ~50–60%.
  - **ScreenSpot-Pro** (**ACM MM 2025**): generalist GPT-4o ~**0.8%** grounding thô; mảng UI khó còn rất xa bão hoà.
- **Với người đọc tutorial: TÊN nút + THỨ TỰ mới quan trọng, KHÔNG phải pixel** — AskEase (**CHI 2026**) sinh hướng dẫn bằng *tên/loại nút*, tránh mô tả pixel; GUI-Actor (**NeurIPS 2025**) "con người không tính toạ độ màn hình". → hợp lý hoá việc **sinh-theo-tên + point-in-bbox chỉ là neo bạc để chấm**.
- **"Frontier + lớp neo > frontier trần" là tiền lệ vững:** SeeAct (**ICML 2024**) planner-frontier + grounding ngoài thắng model gốc, *cái lớp* là đóng góp; VDGD (**ICLR 2025**) lớp grounding-lúc-decode độc-lập-model tăng faithfulness 2–33%.
- **Cảnh báo cân bằng (phải thừa nhận):** model native chuyên-dụng (UI-TARS) có thể **vượt** frontier+wrapper ở *thực thi agent* — nhưng đó là **bấm máy**, không phải **tutorial cho người**; càng củng cố "KHÔNG claim SOTA hệ thống, claim phương pháp".

---

## 3. PIPELINE CUỐI — Design E: "Lớp trung-thực-hoá độc-lập-model"

```
                 ẢNH (1 hoặc N) + CÂU HỎI
                          │
        (N≥2)  Stage-0: xếp thứ tự màn (pairwise+Copeland, ảnh thô, verifier tất định)
                          │  chuỗi đã sắp
                          ▼
   ┌─────────────────────────────────────────────────────────┐
   │  BỘ SINH = VLM mạnh nhất, CÓ THỂ THAY                    │
   │  (GPT-5 / Gemini-3 qua API  HOẶC  Qwen open)            │
   │  → sinh tutorial GỌI NÚT THEO TÊN/loại (không pixel)    │
   └─────────────────────────────────────────────────────────┘
                          │  tutorial [tên nút + hành động]
                          ▼
   ┌─────────────────────────────────────────────────────────┐
   │  ORACLE GROUNDING (đặt BÊN CẠNH — KHÔNG chặn khâu sinh) │
   │  open grounder (Qwen2.5-VL/OS-Atlas) / OmniParser:      │
   │  "nút TÊN này có thật? ở đâu?" → tồn-tại + toạ độ        │
   └─────────────────────────────────────────────────────────┘
                          │
                          ▼
   ┌─────────────────────────────────────────────────────────┐
   │  LỚP TRUNG-THỰC:                                         │
   │  V1 kiểm tồn-tại/khớp-tên (code, tất định)              │
   │  V2 (tùy chọn) critic KHÁC HỌ, hỏi nhị phân "đúng nút?" │
   │  FALLBACK: grounding fail → mô tả bằng lời              │
   │            (KHÔNG bỏ bước, KHÔNG sinh nút-sai-tự-tin)   │
   └─────────────────────────────────────────────────────────┘
                          ▼
        TUTORIAL cuối + (mỗi bước: tên nút, toạ độ nếu có, cờ fallback)
        ……… CHẤM OFFLINE bằng chính oracle (VH-silver) …………
```

**Khác bản cũ ở 4 điểm cốt lõi:**
| | Bản cũ (file 13/03 hiện tại) | Bản cuối (design E) |
|---|---|---|
| Vị trí detector | OmniParser+SoM **đặt TRƯỚC**, ràng-buộc model chỉ cite ID detector thấy | **Oracle đặt BÊN CẠNH** — chỉ chấm + kích fallback |
| Trần recall | Recall detector **cắt cụt cả tutorial** (bịa-an-toàn-nhưng-thiếu) | Recall chỉ ảnh hưởng **độ tin phép đo**, KHÔNG cắt tutorial |
| Cách sinh | Cite **ID số** | Gọi **TÊN nút** (đúng nhu cầu người đọc) |
| Khi grounding fail | abstain/bỏ bước | **fallback mô tả bằng lời** (giữ hữu dụng) |
| SoM/constrained-ID | Đường chính | **1 bậc ablation + công cụ đo K1** |

**Vì sao ổn định/không lỗi thời:** đóng góp = **cái lớp + phương pháp đánh giá**, model sinh là **mảnh thay được**. GPT-6 ra → cắm vào khe "bộ sinh", **số đẹp hơn, khung không đổi**. (Tiền lệ: SeeAct ICML2024, VDGD ICLR2025.)

---

## 4. METRIC CUỐI (sound cho 2026 — chỉ tinh chỉnh)

### DG1 (một màn)
1. **⭐ Headline = CẶP faithfulness × coverage (BẮT BUỘC báo cùng nhau — lá chắn chống gaming):**
   - *faithfulness/precision:* matcher open-vocab **ALOHa** (NAACL2024) → tỉ lệ bịa.
   - *coverage/recall:* % nút thật (VH-silver) được nhắc, **có trọng số bước quan trọng** (một tutorial bỏ bước bắt buộc bị phạt nặng).
   - **Lý do bắt buộc:** hệ ràng buộc/cautious thắng điểm-bịa **bằng cách nói ít** → coverage lộ ngay. (Nền VALOR-EVAL ACL2024; củng cố mới **PROVE ICCV2025**, **OVFact EMNLP2025**.)
2. **Grounding = point-in-bbox** (SeeClick/ScreenSpot **ACL2024**), kèm "recall=X% (K1)". (Thừa nhận phê bình nhị phân → trích **GUI-Actor NeurIPS2025**; phụ: dung sai khoảng cách 14%.)
3. **Format = IFEval-style** (đánh số/động từ) + **Clarity = rubric PHÂN-RÃ + judge** (bỏ G-Eval chấm-1-điểm-tổng). Neo bình duyệt cho dòng IFEval = **IFBench NeurIPS2025**.

### DG2 (xếp thứ tự màn)
4. **⭐ Headline = Kendall τ-b partial-order** — **chấm KHÔNG cần LLM-judge** → *miễn nhiễm mọi thiên lệch judge* = headline an-toàn-nhất. (Lapata CL2006; partial-order/ties = **Fagin et al. PODS2004 / SIAM JDM2006** — *verify đúng bài*.)
5. **Tier A teacher-forced** (Action-Type/Grounding@14%/Step-SR) = trục tham chiếu **tĩnh** chuẩn ngành. + **ordering gap**.

### ➕ MỚI — Followability / Step-SR (ít gaming nhất, là điểm mới)
6. **Đưa các bước tutorial SINH RA chạy lại trên gold trajectory AndroidControl** → resolve mỗi bước thành thao tác, so với gold action (action-type + grounding@14%) → **bao nhiêu bước khớp / có tới đích không**. Trả lời thẳng "tutorial có DÙNG ĐƯỢC không" — phản biện khó bác nhất.
   - **Khả thi NGAY (offline):** AndroidControl có sẵn gold action mỗi bước → so được, không cần emulator.
   - **Bản đầy đủ (live execution trên AndroidWorld ICLR2025) = future-work** (nặng env). Làm **bản nhỏ pre-register** trước.

### Meta-eval
7. **Krippendorff α (headline, chance-corrected)** + tương quan người (Kendall) + **bền với rephrase/độ-dài** (GEM **ICLR2025**). Judge: khác-họ-với-generator, swap-and-average, rubric phân-rã, **đo tương quan lỗi judge** (panel nhiều ≠ nhiều phiếu độc lập).

### 🔧 Đính chính venue (committee dễ bắt)
**ScreenSpot-Pro = ACM MM 2025** (không phải ICLR workshop) · **UI-Vision = ICML2025** · **OS-Atlas = ICLR2025 Spotlight** · **GUI-Actor = NeurIPS2025** · **IFBench = NeurIPS2025** · ALOHa = NAACL2024 short · POPE = EMNLP2023 main.

---

## 5. CLAIM "THẮNG FRONTIER" — gộp 3 tầng, spine = eval
Phát biểu cuối (winnable + honest):
> *"Trên cùng ngân sách tính, **lớp trung-thực-hoá** của chúng tôi **giảm bịa nút + tăng đúng-nhãn** so với **chính model đó viết tự do**, và (mục tiêu) **làm tutorial DỄ LÀM THEO hơn — Step-SR** — đúng trên **cả GPT-5, Gemini-3 LẪN model mở** (delta dương mọi model); đạt được trên **model mở ở chi phí bằng một phần nhỏ frontier**. Tất cả chấm bằng phương pháp đã **tương quan với người** và **bền với thao túng**."*
> ⚠️ **TRẠNG THÁI CHỨNG MINH (trung thực):** "giảm bịa/đúng-nhãn so **baseline viết-tự-do**" = **ĐÃ ĐO** (Qwen, `report/15`: 66.7%→100%, 59.3%→92.6%). "So **frontier GPT-5/Gemini-3**" + "**Step-SR (tới-đích)**" = **GIẢ THUYẾT, CHƯA ĐO** → phần AndroidControl/Colab.

Bốn tầng (xếp theo độ vững): **(1) phương pháp đánh giá** (spine, không lỗi thời) → **(2) thắng trục-yếu** grounding/coverage/followability → **(3) bền qua nhiều model** (model-agnostic) → **(4) Pareto chi phí** (open+scaffold ≈ frontier, rẻ hơn nhiều; tiền lệ GTA1 **ICLR2026**, MoA **ICLR2025**, HAL **ICLR2026**). *"frontier + lớp" trong-một-model* chỉ là **1 ô** của ma trận, không phải headline (vì self-refine không-có-tín-hiệu-ngoài dễ thua — Huang ICLR2024/Kamoi TACL2024; lớp của ta CÓ tín hiệu ngoài = oracle nên thoát).

---

## 6. THÍ NGHIỆM + THỐNG KÊ (để claim không "bay màu")
- **Ma trận:** {GPT-5 / Gemini-3 / Qwen open / grounder mở} × {free-form → +oracle-verify → +fallback → +reorder}. Baseline bắt buộc: **self-consistency CÙNG ngân sách tính** (chặn "thắng nhờ gọi nhiều hơn"); GOAL-ONLY/VISUAL-ONLY/RANDOM (null empirical theo N).
- **Thống kê 2026:** paired **bootstrap BCa + permutation** (chỉ "significant" khi cận-dưới CI>0 **và** p<0.05); **effect size**; **Holm/FDR** đa-N; **kiểm định dấu per-model** cho "delta dương mọi model"; ≥30 episode/N; human N≥60–80 + **báo Krippendorff α**.
- **Chống gaming (quan trọng nhất):** coverage báo kèm + **sàn coverage pre-register** (precision dưới sàn không được tính "thắng") + **Step-SR** (tutorial thiếu bước thì rớt). Cost-Pareto: chốt mốc ngày + nhiều baseline.

---

## 7. GIỮ / ĐỔI / BỎ so với bản hiện tại
| Hạng mục | Quyết định |
|---|---|
| Khung 2 đóng góp (hệ tốt + eval) | **GIỮ** (đã chốt) |
| DG1 grounding + hallucination + clarity | **GIỮ**, thêm **coverage bắt buộc** + rubric phân-rã |
| DG2 τ-b partial-order (Fagin) | **GIỮ** (headline an toàn) |
| Tier A teacher-forced | **GIỮ** (tham chiếu tĩnh) |
| 3 dataset (MobileViews/AndroidControl/ScreenSpot) | **GIỮ NGUYÊN** |
| OmniParser + SoM + constrained-ID **đặt trước** | **ĐỔI** → oracle bên cạnh + 1 bậc ablation |
| Sinh cite ID số | **ĐỔI** → sinh theo **tên nút** |
| abstain im lặng | **ĐỔI** → **fallback mô tả bằng lời** |
| Bộ sinh cố định | **ĐỔI** → **model thay được** (GPT-5/Gemini-3/open), báo đường cong qua model |
| Followability/Step-SR | **THÊM** (mới) |
| Claim "thắng GPT-4o" chung chung | **ĐỔI** → claim 3-tầng có điều kiện + spine eval |
| Venue vài citation | **SỬA** (ScreenSpot-Pro=MM2025…) |

---

## 8. RỦI RO CÒN LẠI & cách chặn
| Rủi ro | Chặn |
|---|---|
| Gaming: thắng grounding nhờ bỏ bước | Cặp faithfulness×coverage + sàn coverage + **Step-SR** |
| Claim bay màu khi model mới ra | Đóng góp ở phương pháp/lớp + đường cong qua nhiều model + kiểm định dấu |
| Frontier API đắt/đổi/khai tử | Pin phiên bản + ghi ngày; lõi tái lập trên model mở; Pareto chi phí |
| Self-refine vô dụng | Lớp dùng **tín hiệu ngoài** (oracle), không phải tự-soi; compute-match |
| Judge thiên lệch | τ-b không-cần-judge làm headline; phần judge: khác-họ + swap + α |
| Step-SR đổ lỗi nhầm (agent dở ≠ tutorial dở) | Có **skyline ORACLE** + bản nhỏ pre-register; live-exec = future-work |
| Recall detector thấp | Nay chỉ hạ **độ tin đo**, không cắt tutorial; vẫn đo K1 |

---

## 9. QUYẾT ĐỊNH CẦN BẠN DUYỆT + tôi sẽ sửa gì
**Bạn duyệt §3 (pipeline) + §4 (metric) + §5 (claim).** Khi OK, tôi sẽ:
1. **`report/00_DOC_TU_DAU`** (đã thay file 13, nay ở `_archive/`) — bản dễ hiểu pipeline design E (oracle + sinh-theo-tên + fallback) + Followability. *(ĐÃ ĐỒNG BỘ.)*
2. **`report/03_pipeline.md`** — đổi sơ đồ/đường chính sang oracle; SoM→ablation; thêm coverage + Step-SR.
3. **`report/05_final_plan.md`** — cập nhật pipeline khoá + metric khoá (coverage bắt buộc, Step-SR, venue fixes) + ma trận thí nghiệm + thống kê.
4. **`report/01_metrics.md`** — thêm coverage-có-trọng-số + Followability/Step-SR + rubric phân-rã + venue fixes.
5. **`CLAUDE.md`** + **skill `vcl-fair-paper`** + **memory** — đồng bộ khung design E.
*(Nếu bạn muốn đổi điểm nào trong §3–§5, sửa ở file 14 này trước rồi tôi mới áp xuống.)*

---

## 10. NGUỒN (peer-reviewed anchors — đã verify 2026)
EACL 2026 *Do GUI Grounders Truly Understand UI Elements?* · ScreenSpot/SeeClick **ACL2024** · ScreenSpot-Pro **ACM MM2025** · OS-Atlas/UGround **ICLR2025** · GUI-Actor **NeurIPS2025** · AskEase **CHI2026** · SeeAct **ICML2024** · VDGD **ICLR2025** · ALOHa **NAACL2024** · VALOR-EVAL **ACL2024 Findings** · PROVE **ICCV2025** · OVFact **EMNLP2025** · IFBench **NeurIPS2025** · Lapata **CL2006** · Fagin et al. **PODS2004/SIAM JDM2006** (verify) · AndroidControl **NeurIPS2024** · AndroidWorld **ICLR2025** · GEM **ICLR2025** · Snell test-time **ICLR2025** · Huang **ICLR2024** / Kamoi **TACL2024** · MoA **ICLR2025** · GTA1/HAL **ICLR2026** · paired-permutation **ACL2022**. *(Preprint flag: HyperClick 2510.27266, UI-TARS 2501.12326 — dùng làm hiện vật, không trình như bình duyệt. Mọi bảng leaderboard GPT-5/Gemini-3 trên web 2026 = KHÔNG dùng.)*
