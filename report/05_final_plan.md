# BÁO CÁO 5 — KẾ HOẠCH CHỐT CUỐI (DESIGN E) — nguồn-sự-thật để thực hiện

> ⚠️ **THẨM QUYỀN:** đây là **nguồn-sự-thật**. Khi mâu thuẫn với report 01–04 (mang khung cũ), **file 05 thắng**. Bản dễ hiểu toàn cảnh: `00_DOC_TU_DAU`; thiết kế chi tiết: `14`; metric rõ ràng: `18`; kết quả đã chạy: `15`.
> **Phiên bản:** viết lại 2026-06-25 theo **design E** (thay khung cũ "ReOrder-Tutor / SoM đặt-trước / DG1-DG2 / hệ tham chiếu").

## TÓM TẮT 30 GIÂY (đã khoá)
1. **HAI đóng góp NGANG NHAU:** (A) **hệ sinh hướng dẫn TỐT** = "lớp trung-thực-hoá độc-lập-model"; (B) **phương pháp ĐÁNH GIÁ** đáng tin khi không có bài mẫu của người. Đóng khung để **kết quả null vẫn ĐẬU** (nếu pre-register) ở cả hai.
2. **Pipeline lõi = design E:** bộ sinh VLM **thay được** (Qwen mở lõi; GPT-5/Gemini-3 đối chứng) → sinh **gọi nút theo TÊN** → **oracle kiểm BÊN CẠNH** (không chặn) → **fallback/sửa** khi không khớp. OmniParser+Set-of-Mark+constrained-ID = **một nhánh ABLATION**, không phải đường chính. **Không fine-tune lõi.**
3. **TRỌNG TÂM = AndroidControl** (goal thật + gold + a11y mỗi màn) chở phần lớn metric; **MobileViews** = kiểm 1-màn; **ScreenSpot** = đối chứng tìm-nút.
4. **Metric:** *(DG1 mỗi màn)* tách **Bịa** (ALOHa, đồng-nghĩa-OK) vs **Đúng-nhãn/Clarity** (đúng tên) + **Coverage** (trên gold) + **Grounding** (point-in-bbox) + **Format**; *(DG2 nhiều màn)* **Kendall τ-b** (xếp thứ tự, không cần judge) + **Step-SR** (làm-theo-tới-đích) + Tier A.
5. **6 pha có cổng; 4 cổng cứng = K1 (recall) · KN (histogram độ dài episode) · KZ′ (prior-art) · KB (chống leak).** Pre-registration cho cả hai đóng góp.
6. **Ngân sách:** 1 GPU 24GB (thuê/Colab) + ~$100–300 API. Phần lõi-logic đã chạy thử **miễn phí trên CPU** (xem §6).

---

## 1. HAI ĐÓNG GÓP (đóng khung để null vẫn đậu)

### (A) HỆ — "lớp trung-thực-hoá độc-lập-model"
Một hệ gắn lên **bất kỳ VLM mạnh nào** để hướng dẫn **ít bịa hơn, đúng-nút hơn, dễ làm-theo hơn** so với để chính model đó viết tự do.
- **Claim mức-CHẮC-THẮNG (an toàn):** giảm bịa + tăng đúng-nhãn so **baseline model viết-tự-do**. *Đã ĐO trên Qwen (CPU free): faithfulness 66.7%→100%, đúng-nhãn 59.3%→92.6% — `report/15`.*
- **Mức-THƯỞNG (GIẢ THUYẾT, CHƯA ĐO):** so **frontier (GPT-5/Gemini-3)** trên trục trung-thực/đúng-chỗ/làm-theo (KHÔNG so fluency). **KHÔNG claim SOTA leaderboard** (setup khác — sinh hướng dẫn cho người).
- **Không lỗi thời:** đóng góp = cái lớp + cách đánh giá (model thay được) → GPT-6 ra chỉ làm số đẹp hơn. Tiền lệ: SeeAct (ICML 2024), VDGD (ICLR 2025).

### (B) PHƯƠNG PHÁP ĐÁNH GIÁ (khi không có bài mẫu của người)
Neo bằng **cây phần tử thật (View Hierarchy / accessibility tree) = "đáp án bạc"**, chỉ dùng **lúc CHẤM**, không cho model xem lúc sinh.
- **Độ mới** ở phương pháp: (a) **chống-vòng-lập-luận** (nhãn cặp-bắt-buộc suy từ GOLD, không tự-chấm), (b) **truy-nguồn-tín-hiệu một-cue** (stratification), (c) **chấm thứ-tự-bộ-phận** (partial-order, Fagin), (d) **audit người**. **THỪA NHẬN prior-art** sắp-ảnh: Sort-Story (EMNLP 2016, Spearman) · Wu et al. (ACL 2022) · RankGPT (EMNLP 2023) · GUI Knowledge Bench (2510.26098) · TempVS (2506.10415).

### Nguyên tắc "NULL VẪN ĐẬU" (pre-registration, cả hai đóng góp)
- Phải nêu **giả thuyết bác-được + ngưỡng effect-size + quy tắc quyết định TRƯỚC khi chạy**.
- **(A):** kết quả null = "lớp trung-thực-hoá *không* cải thiện faithfulness sau khi kiểm soát recall — và đây là cơ chế" (kèm đường cong recall). Một null **được giải thích cơ chế** là đóng góp; một "không thắng" không-giải-thích thì không.
- **(B/DG2) KHÔNG được tautology:** pre-register "**τ-b(SELF-ORDER) > RANDOM-ORDER** quá effect-size + CI" (ngưỡng = null empirical theo từng N); nếu không vượt, hoặc GOAL-ONLY/VISUAL-ONLY cao bằng → **FAIL CÓ Ý NGHĨA** (model không suy được trật tự ở quy mô này). **Sàn định lượng bất biến:** dù hạ cấp gì, DG2 luôn còn **τ-b-thô trên ≥3 mốc N × ≥30 episode** + signal-attribution.

---

## 2. PHẠM VI ĐÃ KHOÁ

| | Trong luận văn | Future-work |
|---|---|---|
| Dataset | **AndroidControl (TRỌNG TÂM)** + MobileViews (kiểm 1-màn) + ScreenSpot (đối chứng) | Mind2Web (web) |
| Bộ sinh | **off-the-shelf, KHÔNG fine-tune lõi**; Qwen mở (lõi) + GPT-5/Gemini-3 (đối chứng) | LoRA-grounding; world-model tự-train (AGENT-NSI) |
| Ngôn ngữ | **EN định lượng**; ZH sanity | tiếng Việt (demo định tính; quant cần embedder đa-ngữ bge-m3 + dataset VN) |
| Nền tảng | mobile | web |

- **Sản phẩm:** `ảnh (1 hoặc N) + câu hỏi → hướng dẫn`. **N=1** → 1 màn; **N≥2 (xáo trộn)** → tự xếp rồi sinh (= DG2). Chế độ N-ảnh là **bài toán đặt ra ĐỂ ĐO** năng lực suy luận trật tự, **KHÔNG** khẳng định là nhu cầu deploy phổ biến (probing task).

---

## 3. PIPELINE ĐÃ KHOÁ (design E)

### 3.1. Luồng lõi
```
ẢNH + CÂU HỎI
   │  (N≥2 → Bước 0: xếp thứ tự màn — §3.6)
   ▼
BỘ SINH (VLM thay được: Qwen mở lõi / GPT-5 / Gemini-3) → tutorial GỌI NÚT THEO TÊN
   ▼
ORACLE (cây nút thật) đặt BÊN CẠNH: "nút TÊN này có thật? ở đâu?"  ← không chặn khâu sinh
   ▼
LỚP TRUNG-THỰC:  V1 kiểm tồn-tại (ALOHa) → (nếu lệch) SỬA bằng MODEL KHÁC chọn lại nút thật
                 → nếu vẫn không có: FALLBACK mô tả bằng lời (không bỏ bước, không bịa)
   ▼
TUTORIAL cuối  ……(chấm OFFLINE bằng oracle; oracle KHÔNG vào lúc sinh)……
```
- **Lý do design E (thay bản cũ "detector đặt-TRƯỚC + ép cite ID"):** detector đặt-trước **chặn trần** tutorial (sót nút → thiếu bước); oracle đặt **bên-cạnh** → recall thấp chỉ hạ **độ tin phép đo**, không cắt tutorial.
- **Với người đọc: TÊN nút + THỨ TỰ mới quan trọng, không phải pixel** (AskEase CHI 2026, GUI-Actor NeurIPS 2025) → sinh-theo-tên là đúng nhu cầu; point-in-bbox chỉ là neo-bạc để chấm.

### 3.2. Ablation (đo "cơ chế nào trả công") — thang bậc design E
| ĐK | Cấu hình | Cô lập |
|---|---|---|
| **L0 (baseline)** | model viết TỰ DO | sàn |
| **L1** | + oracle kiểm tồn-tại + **fallback** | giá trị "không-bịa / trung-thực" |
| **L2 (design E đầy đủ)** | + **SỬA** bằng model khác (chọn lại nút thật) | giá trị "recover lỗi" |
| **Arm-SoM** *(đối chứng)* | OmniParser + Set-of-Mark + constrained-ID (thiết kế CŨ) | SoM có đáng công không |
| **Arm-NG** *(đối chứng)* | Qwen2.5-VL **tự xuất toạ độ** (không detector/SoM) | native-grounding so detector+SoM |
→ Báo **delta L0→L1→L2** + so Arm-SoM/Arm-NG. *(Đã chạy A/B L0 vs L2 trên Qwen: bịa 33.3%→0% (recover 9/9), faithfulness 66.7%→100%, đúng-nhãn 59.3%→92.6% — `report/15`. Lưu ý: "recover về nút THẬT" chưa chắc ĐÚNG-việc; đúng-việc đo bằng Step-SR/Colab.)*
- **Điều kiện công bằng (khoá):** cùng base VLM, cùng K≤2/stop-on-no-change/JSON-schema/resolver-đối-xứng cho mọi ĐK; bước SỬA dùng **model KHÁC họ** (= phản hồi-từ-ngoài, thoát phê phán self-refine Huang ICLR 2024 / Kamoi TACL 2024).

### 3.3. Verifier — nói chính xác (chống overclaim)
- **V1 (code, không LLM):** kiểm nút-được-cite **có khớp** cây nút thật (ALOHa). Đảm bảo **TỒN TẠI**, KHÔNG đảm bảo **ĐÚNG-việc**.
- **Bước SỬA / V2 (model KHÁC):** khi V1 lệch → cho model khác **chọn lại nút thật** từ danh sách (hoặc `none`). **Bắt buộc có lựa chọn `none/abstain`** để khỏi ép-chọn nút-thật-nhưng-sai khi không có nút hợp (pre-register cách xử + audit xem có ép-sai không).
- **Fallback:** `none` → mô tả bằng lời (trung thực), KHÔNG tính bịa.

### 3.4. Ma trận model (chống shared-error)
`generator ≠ model-sửa(V2) ≠ judge-clarity ≠ judge-hallucination(text-only nuốt cây-nút, KHÔNG ảnh)` — **khác họ**; CI assert id khác nhau. *(4 họ chỉ GIẢM, không TRIỆT shared-error — phải ĐO tương quan lỗi judge trên subset audit.)*

### 3.5. Pin phiên bản
Pin **một build** mỗi thành phần (Qwen, OmniParser nếu dùng arm-SoM, matcher ALOHa). Recall của arm-SoM dùng **cùng build** với K1 — khác build thì "recall-conditioned" vô hiệu.

### 3.6. Bước 0 — xếp thứ tự màn (DG2, N≥2)
- **Nhánh chính = đọc ẢNH THÔ** (pixel trực tiếp cho VLM, không qua detector). *(Nhánh parser = ablation, đóng khung "conditioned on recall".)*
- **Cách xếp = pairwise-then-aggregate** (mỗi cặp hỏi "màn nào trước?" + bắt trích ≥1 ordering cue → **Copeland**). **= PRP-Allpair (Qin et al. NAACL 2024) + Copeland (1951)**; chọn pairwise vì **BẤT-BIẾN-thứ-tự-đầu-vào** (listwise/RankGPT tụt >50% khi đảo đầu vào) **và** vì nó **sản sinh nhãn-cặp + cue/cặp** cho signal-attribution. **Listwise = đối chứng fair-compute** (cùng tổng LLM-call). Phá-tie Copeland **tất định** (theo chỉ số ảnh tăng dần). Chu trình mâu thuẫn → min-feedback-arc-set.
- **5 ORDERING CUES** (trả lời "model dựa vào đâu biết thứ tự"): **gating · nav-affordance · state-delta · title-progression · drill-down**. **Signal-attribution = stratification một-cue** (giữ cặp phân biệt bởi ĐÚNG MỘT cue, đo acc theo nhóm — KHÔNG che pixel) + phân tích lỗi mở. *Caveat: cue model tự-trích chỉ là giải thích YẾU; kết luận dựa stratification, KHÔNG dựa lời model tự khai.*

---

## 4. METRIC ĐÃ KHOÁ
> Quy ước: **cao = tốt.** Định nghĩa + ví dụ chi tiết: `18_metric_ro_rang.md`.

### 4.1. DG1 — mỗi màn
- **Bịa / Faithfulness (⭐):** nút được nhắc có TỒN TẠI không? Matcher **ALOHa (embedding + Hungarian, đồng-nghĩa-OK)** — KHÔNG vu oan synonym. `Faithfulness = 1 − HER`. *(HER/CHAIR vocab-đóng = baseline; KHÔNG xếp chồng POPE/SummaC/QAGS/SelfCheckGPT/HaluEval; FActScore/SAFE CẤM cho trật-tự-màn.)*
- **Đúng-nhãn / Clarity:** gọi **ĐÚNG TÊN hiển thị** không? So **chính xác** (synonym → trừ clarity, KHÔNG tính bịa). *(Nút icon không chữ → loại khỏi mẫu này.)*
- **Coverage (đủ ý):** bỏ sót nút CẦN không? **Đo trên AndroidControl** (có gold → biết nút nào cần), **có trọng số bước quan trọng**. Trên MobileViews (không gold) = proxy, báo riêng, KHÔNG headline. **Luôn báo cặp [Faithfulness, Coverage]** (chống mẹo "viết ít cho khỏi sai").
- **Grounding (point-in-bbox):** điểm click rơi trong bbox nút thật? *(AndroidControl-native = point-in-bbox nhị phân; ngưỡng 14% = của AITW.)*
- **Format:** đánh số · động từ mệnh lệnh · 1 việc/bước (IFEval-style, strict+loose); **Clarity sâu** = rubric phân-rã + judge.
- **Matcher khoá & validate TRƯỚC:** ALOHa-style; **validate trên subset gán tay (báo false-pos/neg) rồi FREEZE** trước khi chấm bất kỳ ĐK nào. **Resolver/matcher ĐỐI XỨNG** cho mọi nhánh (ID-lookup của arm-SoM chỉ là dòng "oracle upper-bound" riêng).
- **Hai trần recall (khai báo cả hai):** (1) **detector sót** (K1) → mọi số "conditioned on recall=X%"; (2) **nhãn cây-nút thiếu** → element model nhắc mà cây-nút thiếu nhãn thì **đừng auto-tính bịa**, đưa vào **subset đã làm sạch**.

### 4.2. DG2 — nhiều màn (trên AndroidControl)
- **Headline = Kendall τ-b (KHÔNG cần judge → miễn nhiễm thiên lệch judge):** chấm **thứ-tự-bộ-phận** — chỉ phạt **cặp BẮT BUỘC** (gating/drill-down), cặp **TỰ-DO** đảo vẫn đúng. **τ-b partial-order = Kendall trên bucket-order của Fagin–Kumar–Sivakumar (SIAM JDM 2003 optimistic p=0; Fagin et al. 2006)** — trích nguồn, KHÔNG claim "tự-định-nghĩa". Báo **τ-b-thô** (toàn cặp) làm điểm-sàn. Phụ: pairwise-order-acc + position-acc@correct-place; **bỏ Exact-Order-Match** khỏi headline.
- ⚠️ **CHỐNG VÒNG-LẶP-LUẬN (D1, bất biến):** nhãn "cặp BẮT BUỘC" **suy TỪ GOLD trajectory bằng quy tắc nhân-quả tất định** (màn B chỉ xuất hiện SAU gold action ở A ⇒ (A,B) bắt buộc), **KHÔNG** lấy từ bộ-phát-hiện-cue mà model dùng. Pre-register: (i) tỷ lệ bắt-buộc/tự-do; (ii) **audit người 50–80 cặp** (% khớp); (iii) độ nhạy headline khi nhãn sai 10%. **Decision-rule:** % khớp <~90% → hạ headline xuống τ-b-thô.
- 🔴 **LỌC EPISODE trước khi đo τ-b (bắt buộc):** (1) loại bước `status`/`wait`; (2) loại episode **màn gần-trùng** (bộ lọc độ-phân-biệt-thị-giác, pre-register ngưỡng — đã thấy ep có 3 màn MAE 0.5–0.8/255 = suy biến); (3) **KN đếm theo "N màn PHÂN BIỆT ĐƯỢC"**, không theo num_steps thô. **KHÔNG đo τ-b trước khi lọc.**
- **Baseline (đối xứng):** **GOAL-ONLY** (che ảnh) + **VISUAL-ONLY** (che mục tiêu) + **RANDOM-ORDER**. **Ngưỡng "vượt RANDOM" = null EMPIRICAL theo từng N** (không giả định kỳ vọng=0). ⚠️ **GOAL-ONLY = cổng cứng:** nếu τ-b(GOAL-ONLY) ≥ τ-b(SELF-ORDER)−ε trên ≥X% episode → goal tự tiết lộ thứ tự → **lọc subset goal-không-tiết-lộ rồi mới báo headline**.
- **Step-SR (làm-theo-tới-đích) — bằng chứng "hiệu quả thật":** chuyển bước sinh ra thành thao tác, so **gold action** (đúng loại + đúng chỗ trong 14%). Cần gold → **AndroidControl/Colab**. *(Bản đầy đủ live-exec AndroidWorld = future-work.)*
- **Tier A teacher-forced (tham chiếu chuẩn ngành):** mỗi bước đưa MÀN THẬT của gold, model đoán bước kế → **Action-Type / Grounding@14% / Step-SR**. Là dụng-cụ-đo cận-trên, KHÔNG claim ngang leaderboard.
- **ordering gap = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER):** sanity **ORACLE ≥ SELF − ε mọi episode**. ⚠️ **Test nhạy-thứ-tự (D2):** đảo 1 cặp bắt-buộc, đo Δ metric tutorial; nếu Δ < ngưỡng → metric không nhạy thứ tự → **bỏ ordering gap, chỉ giữ τ-b**.
- **RAW vs ORACLE (báo cả hai):** RAW = thực; ORACLE = giả định resolver hoàn hảo (tách lỗi resolver khỏi lỗi suy luận).

### 4.3. Validate metric với người (Track B)
BWS (so-đôi) ~60–80 item từ các ĐK ablation → **Krippendorff α** (headline) + tương quan **Kendall τ-b** + **bootstrap CI-width** (trung thực về độ thiếu chính xác) + **pairwise-accuracy có tie-calibration** + **manipulation-robust** (rephrase/độ-dài). Phát biểu DIRECTIONAL, KHÔNG ra 1 con ρ điểm.

---

## 5. DATASET ĐÃ KHOÁ
- **AndroidControl (NeurIPS 2024, peer-reviewed) — TRỌNG TÂM:** 15,283 episode / 833 app / mean ~5.5 step (train 13,604 ep / 74,722 step = 5.49; Table 1 ghi 4.8; p5=1, p95=13). Có `goal` thật + gold action mỗi bước + **cây accessibility mỗi màn** (proto `AndroidAccessibilityForest` — cài `android_env`, parse ~30–50 dòng → text + bbox pixel + cờ; *có trong FULL dataset, KHÔNG trong sample đã trích*). Gold action click = **(x,y) pixel** trong **1080×2400**. **Tự đếm histogram theo N (cổng KN).** ⚠️ **ĐỌC AndroidControl-Curated (arXiv:2510.18488)** trước khi khoá cách chấm (phản biện nhãn — mà cặp-bắt-buộc suy từ nhãn đó).
- **MobileViews (preprint, ghi v1/v3) — kiểm 1-màn:** ảnh + cây-nút JSON. ⚠️ **bounds = `[[l,t],[r,b]]` lồng** (+`bound_box`); **field width/height là RÁC** → dùng kích thước ẢNH (PIL).
- **ScreenSpot/-v2 (SeeClick ACL 2024 / OS-Atlas ICLR 2025) — đối chứng tìm-nút:** có sẵn instruction + bbox (0–1 và pixel; ⚠️ khác theo mirror HF → pin 1 mirror + assert).
- **AITW (NeurIPS 2023):** **nguồn ngưỡng 14%** (trích bắt buộc).
- ⚠️ **BA HỆ TOẠ ĐỘ KHÁC NHAU** (MobileViews pixel lồng / ScreenSpot 0–1 / AndroidControl điểm pixel + `!FUNCTIONCALL`) → **convert về 1 hệ + assert range** trước khi point-in-bbox (chi tiết + unit-test: `12` §1.4).
- ⚠️ **CÂU HỎI USE-CASE:** **CHỈ MobileViews** phải **tự soạn** (theo protocol: mỗi màn 1–2 câu "làm sao để X", X làm-được-trên-màn, có người duyệt). **AndroidControl/ScreenSpot có sẵn goal/instruction → KHÔNG tự soạn.** "Tự soạn câu hỏi (INPUT) ≠ bịa đáp án (đáp án vẫn là dữ liệu THẬT)". *(Bài học từ chạy thử: câu hỏi mơ hồ → bịa nhiều; câu hỏi tốt là điều kiện then chốt.)*

---

## 6. ĐÃ CHỨNG MINH (miễn phí, CPU) — vs CÒN CHỜ (Colab)
**ĐÃ chạy thật (Ollama/Qwen/CPU, `report/15`, code `harness/`):**
- ✅ Pipeline design E chạy end-to-end; bộ chấm bắt lỗi đúng.
- ✅ Metric **nhạy** (3B bịa 40.7% vs 7B 25% — matcher chuỗi; tín hiệu sơ bộ).
- ✅ Matcher **ALOHa** đáng-tin-hơn (bịa 40.7%→33.3%); tách **Bịa vs Đúng-nhãn**.
- ✅ Hệ **hiệu quả về độ-trung-thực** (A/B L0 vs L2): faithfulness 66.7%→100%, đúng-nhãn 59.3%→92.6%, recover 9/9.
- ✅ AndroidControl a11y **verify chở được** metric.

**CÒN chờ Colab (một lần, sau pre-register):** coverage (gold) · **τ-b xếp thứ tự** · **Step-SR tới-đích** · chạy quy mô (vài trăm màn + ≥30 episode/N → ý nghĩa thống kê) · **audit người + Track B** · so frontier (GPT-5/Gemini-3).
> ⚠️ **Trung thực:** kết quả đã có là **tín hiệu sơ bộ MẠNH** (10 màn / 1 app / model nhỏ / matcher chưa-audit) — **chưa** kết luận thống kê. Xác nhận đầy đủ cần quy mô + gold.

---

## 7. THỨ TỰ THỰC HIỆN — 6 PHA CÓ CỔNG
> Pha k+1 không bắt đầu trước khi Pha k đạt DoD. **4 cổng CỨNG: K1 · KN · KZ′ · KB** (bộ 10 kill-test: + K3–K8, chi tiết `04`).

| Pha | Việc | DoD / Cổng |
|---|---|---|
| **P0 — Env** | dựng env (Qwen mở; nếu chạy arm-SoM thì pin OmniParser); ma trận model; *(đã làm phần CPU)* | model load; matcher ALOHa chạy; enum có `none` |
| **P1 — K1 + KZ′ + KN (cứng)** | **K1:** đo recall (nếu chạy arm-SoM); **KZ′:** rà prior-art (Sort-Story/Wu/RankGPT + **GUI Knowledge Bench + TempVS**) → đóng khung độ-mới; **KN:** tự đếm histogram **N-màn-phân-biệt** | K1: có X%, caption ghi "recall=X%"; KZ′: thừa nhận lineage, độ-mới = (a)–(d); KN: đủ episode N≥3 |
| **P2 — Harness DG1 + freeze matcher** | point-in-bbox + Bịa(ALOHa) + Đúng-nhãn + Coverage + Format; **validate matcher tay rồi FREEZE**; resolver đối xứng; câu hỏi MobileViews soạn xong; assert convert 3-format *(phần lớn ĐÃ làm trên CPU — `harness/`)* | metric phân biệt tutorial tốt vs hỏng-cố-ý; matcher đông cứng |
| **P2b — Harness DG2** | bộ xáo trộn **có cổng KB** (strip metadata + tái mã hoá + UUID + che status-bar/đồng-hồ/pin/badge + loại 2-ảnh-trùng); **lọc episode**; **τ-b partial-order** + nhãn cặp-bắt-buộc **suy từ GOLD (D1)** + audit người 50–80 cặp; stratification một-cue; GOAL-ONLY/VISUAL-ONLY/RANDOM (null empirical); Tier A; parse a11y proto | KB qua CI; audit % khớp; **test nhạy-thứ-tự (D2)**; sanity ORACLE≥SELF−ε; loại N≤2 |
| **P3 — Ablation trên DEV** | L0→L1→L2 + Arm-SoM + Arm-NG; chung base/resolver; chiếu chi phí ≤ ngân sách | các ĐK chạy thông; dự phóng ≤ ~$300 |
| **P4 — Full sweep + pilot + bảng DG2** | DG1 vài trăm màn (caption "recall=X%") + DG2 (τ-b SELF vs ORACLE + Step-SR + signal-attribution + Tier A); **≥30 episode/N**, **Holm–Bonferroni**; pilot BWS | bảng DG1 + bảng DG2 + pilot đạt; đã hiệu chỉnh đa-kiểm-định |

---

## 8. THỐNG KÊ + PRE-REGISTRATION
- **Pre-register TRƯỚC khi chạy quy mô:** giả thuyết bác-được + ngưỡng effect-size + quy tắc quyết định + ngưỡng matcher τ + ngưỡng lọc-episode + ngưỡng GOAL-ONLY. → **không chạy-lại-tới-khi-đẹp** (vừa tốn tiền vừa là p-hacking).
- **Kiểm định:** ghép-cặp **bootstrap BCa + permutation** (chỉ "significant" khi cận-dưới CI>0 **và** p<0.05); **effect size**; **Holm–Bonferroni** đa-mốc-N; **≥30 episode/N**; **kiểm định dấu per-model** cho "delta dương mọi model".
- **DG2 discrete-N:** τ-b nhận ít giá-trị-rời-rạc ở N nhỏ (N=3 chỉ 4 giá trị) → CI-width tính trên phân phối rời rạc theo từng N, không gộp.

---

## 9. NGÂN SÁCH
- **Phần cứng:** 1 GPU 24GB (thuê/Colab ~$0.3–0.5/h); Qwen2.5-VL-7B FP16 ~17GB. *(Lõi-logic đã chạy CPU miễn phí.)*
- **API:** judge đẩy sang model rẻ (gpt-4o-mini-class) + Batch; dev set 50–100, full chỉ cho bảng cuối. **Sàn ~$100–300.**
- **Chi phí Stage-0 (DG2):** pairwise = C(N,2) call/episode (N=6 → 15). Trần N≤6 cho đường-cong headline. Tách dòng chi phí theo từng baseline (SELF/ORACLE/GOAL-ONLY/VISUAL-ONLY/RANDOM) + 3 dòng judge.

---

## 10. RỦI RO & cách chặn (gọn)
| Rủi ro | Đã chặn |
|---|---|
| Recall detector chưa rõ | K1 (tự đo) + "recall-conditioned"; **design E giảm phụ thuộc** (oracle bên-cạnh, không chặn sinh) |
| Gaming: thắng bịa nhờ viết ít | Báo cặp **Faithfulness × Coverage** + **Step-SR** (làm-theo-tới-đích) |
| Vu oan synonym là "bịa" | **ALOHa** (đã chứng minh 40.7%→33.3%) + tách Bịa vs Đúng-nhãn |
| Recover thành nút-thật-nhưng-sai-việc | enum có `none` + audit + **Step-SR/gold** mới xác nhận đúng-việc |
| Vòng-lập-luận (tự chấm) | **D1:** nhãn cặp-bắt-buộc suy từ GOLD + audit người |
| Sàn random sai (giả định 0) | **null empirical theo từng N** |
| Goal tiết lộ thứ tự | **GOAL-ONLY = cổng cứng** + VISUAL-ONLY đối xứng |
| Episode suy biến (màn gần-trùng) | **lọc episode bắt buộc** + KN đếm N-màn-phân-biệt |
| Judge thiên lệch | **τ-b không-cần-judge** làm headline; phần judge: khác-họ + đo tương quan lỗi + Track B |
| Đa-kiểm-định nhiều N | Holm–Bonferroni + ≥30/N |
| Kết quả null = "hỏng" | Pre-register → null = pass (cho B + đo-cơ-chế của A) |
| Overclaim "thắng frontier" / Step-SR | Tách **ĐÃ-ĐO (vs baseline)** vs **CHƯA-ĐO (vs frontier + Step-SR)**; KHÔNG claim SOTA leaderboard |
| Overclaim "xếp ảnh xáo là mới" | Thừa nhận lineage + trích **Fagin / PRP / GUI Knowledge Bench / TempVS** |

---

## 11. QUYẾT ĐỊNH ĐÃ CHỐT (2026-06-25)
1. Pipeline = **design E** (lớp trung-thực-hoá). ✅
2. **Không fine-tune** lõi (LoRA = tùy chọn tương lai). ✅
3. Bộ sinh = **Qwen mở (lõi)** + GPT-5/Gemini-3 (đối chứng). ✅
4. **Trọng tâm AndroidControl**; MobileViews/ScreenSpot kiểm nhẹ. ✅
5. Tách **Bịa (ALOHa) vs Đúng-nhãn (Clarity)**. ✅
6. **EN định lượng; VN demo** (embedder VN yếu → bge-m3 future-work). ✅

---

## 12. NÓI GÌ VỚI THẦY (chốt)
> Em chốt **hai đóng góp ngang nhau**. **(A) Hệ:** một "lớp trung-thực-hoá" gắn lên bất kỳ VLM mạnh nào — model sinh hướng dẫn **gọi nút theo TÊN**, một bộ tra-cứu (cây nút thật) kiểm bên cạnh, sai thì **một model khác chọn lại nút thật** hoặc mô tả bằng lời. Em **đã chạy thật miễn phí trên CPU** và đo được: lớp này làm hướng dẫn **trung thực hơn (66.7%→100%) và đúng-nhãn hơn (59.3%→92.6%)** so với để model viết tự do — đây là claim **chắc-thắng**; còn "thắng cả GPT-5/Gemini-3" hay "tới-đích tốt hơn (Step-SR)" em đóng khung là **giả thuyết CHƯA đo**, sẽ đo trên AndroidControl/Colab. Em **KHÔNG claim SOTA leaderboard**. **(B) Cách đánh giá:** neo bằng cây-nút-thật (đáp án bạc), chống-vòng-lập-luận (nhãn cặp-bắt-buộc suy từ đáp án vàng), truy-nguồn-tín-hiệu theo 5 ordering cue, chấm thứ-tự-bộ-phận (Fagin), audit người. Em **đăng ký trước** giả thuyết + ngưỡng nên **kết quả null vẫn là đóng góp**. Toàn bộ off-the-shelf, 1 GPU 24GB + ~$100–300; phần lõi-logic đã chứng minh **miễn phí**. Future-work: tiếng Việt định lượng + world-model tự-train.

---

## 13. TÓM TẮT MỘT DÒNG
**Hệ = "lớp trung-thực-hoá độc-lập-model" (sinh-theo-tên + oracle-bên-cạnh + sửa/fallback) — đã chạy thật miễn phí và đo được hiệu quả về độ-trung-thực (faithfulness 66.7%→100%, đúng-nhãn 59.3%→92.6%); CỘNG một cách đánh giá đáng tin (Bịa-ALOHa/Đúng-nhãn + Coverage-gold + τ-b xếp-thứ-tự + Step-SR tới-đích + Track B), chống-vòng-lập-luận, pre-register "null vẫn đậu"; trọng tâm AndroidControl; còn lại = chạy quy mô + đo tới-đích trên Colab.**
