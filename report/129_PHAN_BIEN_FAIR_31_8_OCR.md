# Phản biện FAIR 31/8 — bản chép từ 18 ảnh

> Nguồn: `paper/fair2026/My Documents [31-08-2026 11_30].zip`, 18 ảnh chụp màn hình file
> `PHAN_BIEN_FAIR_31_8.md` trên máy Mac. Ảnh đã bung ở scratchpad phiên 31/8.
> Bản chấm: `paper/fair2026/main.tex` **clone `598e4ff`** (8 trang) — **không phải** bản
> working tree hiện tại, vốn đã đi trước một lượt vá (xem mục cuối file này).
> Thang chấm: soundness / excitement 1–5, chuẩn ACL Rolling Review.

Ba đợt. Đợt C = chạy Task thật, 7 agent độc lập đọc `main.tex`, không đọc file phản biện trước.

| đợt | vai | họ |
|---|---|---|
| A · B | tóm tắt hội đồng trước khi spawn | — |
| C | AC nội dung | GPT |
| C | Văn phong IEEE | Gemini |
| C | Thống kê / RR | Claude |
| C | Hình thức GUI | Grok |
| C | Cáo giọng AI | Gemini |
| C | Biện hộ văn | GPT |
| C | Copy-editor | Claude |

Bản 16/8 (`PHAN_BIEN_5_GIAM_KHAO.md`) chấm **bài khác** — không trộn.

---

## PHẦN I — CHỐT HỘI ĐỒNG

**Weak reject / reject-as-Registered-Report.**
FAIR vẫn có cửa nếu **hạ pretension**: headline = thước executability + S1 (47,6 → 59,4).
Bỏ *"pre-registered"* và *"condition under which it pays"* khỏi title. Giữ title hiện tại thì không.

| vai | điểm | phán |
|---|---|---|
| Nội dung (GPT) | S 2 / E 2 | weak reject |
| Văn phong IEEE (Gemini) | writing 2 | — |
| Thống kê (Claude) | protocol hỏng | reject as RR |
| Hình thức (Grok) | 2 | — |
| Cáo / biện / copy-editor | hybrid xương người + da LLM | PC viết *overwritten*, ít khi viết chữ "AI" |

**Đồng thuận bắt buộc sửa:** title overclaim · abstract nhồi số, 3 vs 4 đóng góp ·
*"loses 25.2 where it does not"* sai phần bù (−13,1) · giọng theater · không screenshot GUI ·
MIN +0,63 không phải xác nhận cơ chế · *"independently trained"* ≠ khác họ · `rather than` ×22 ·
**không gắn nhãn inconclusive cho S2** (đợt C: luật cần 2 seed; CI không chứa 0).

**Giữ:** trần/sàn/wrong-screen · byte-identical sentence · McNemar S1−Base · Venus giữ dấu
S1−Base · khai missing seed (1 câu, bỏ kịch) · fig Voronoi (không làm Hình 1 duy nhất) ·
mạng số xấu khớp nhau (không bịa) — thống kê C xác nhận LoRA 14 966 784, χ², 8 072 bước.

---

## PHẦN II — PHÁT HIỆN CHỦ TỊCH ĐÃ KIỂM TỪ FILE

- **L1 — Hình.** `fig_voronoi.png` **có** (44 KB). Lỗi = *loại* hình: sơ đồ luật chấm, không phải
  screenshot GUI / 3 mô hình. (Lúc đầu glob nhầm "thiếu" vì trước reclone.)
- **L2 — Overclaim grounder.** Abstract: *independently trained grounder*. Limitations: cùng họ
  Qwen. *"Independently"* = không train AndroidControl, **không** = khác họ.
- **L3 — Title vs estimand.** Δ đăng ký 2 hạt **không tồn tại**. +5,7 / −25,2 = lát nội sinh,
  1 hạt, exploratory.
- **L4 — 3 vs 4 đóng góp.** Abstract *"three things"*; Intro (i)–(iv).
- **L5 — 22×.** 11,8 / 0,52 ≈ 22,7. Tỉ số với nhiễu hạt **cùng nhánh**, không phải replication S2.

---

## PHẦN III — ĐỢT A: BỐN GIÁM KHẢO NỘI DUNG

### A1. Hình thức (Grok) — 2/5

PC 2 phút: title 3 dòng, abstract 272 từ, bảng chính trang 5/8, S2 đứng trên S1 (dễ đọc nhầm
nhánh thẳng). `\sbar` human = 100% khi exec 75,7; sàn 12% vẽ 16% (chia trần lát 74,9).
Kết luận ≈ abstract. Ba bài nhồi một skeleton (thước / SFT / registered report).

**Sửa gấp:** bỏ `\sbar` · sắp Base → S1 → S2 · một số đậm 59,4 · screenshot 3 cột thay
`tab:qual` · bar chart · cắt Venus/activation/27 amendments khỏi visual hierarchy.

**Rủi ro IEEE:** XeTeX/fontspec, PDF/A OFF, `main.xdv` chưa camera-ready, hyperref bookmark
`7.3\%`, TikZ trong bảng.

### A2. Nội dung (GPT) — weak reject, S 2 / E 2

1. Estimand 2 hạt **thiếu by design**, không phải *"inconclusive trung thực"*. Dừng sau khi đã
   thấy 1 run treatment.
2. Title claim = **collider**: strata name×point do output S2. Human Ceil không xoá bias.
   Sửa: oracle/corrupt descriptor cùng example, hoặc stratify bằng model đóng băng **trước** treatment.
3. Không human eval dù consumer là người. Executability ≠ người hiểu.
4. *"Floor 12%"* vs wrong-screen 6,1%; S2 87,1 > Ceil 86,6. 78,4% of human bỏ sàn →
   floor-adjusted ≈ **74,4%** = (59,4−12)/(75,7−12).
5. Ba contribution = metric + SFT thường + ablation thiếu. Widget Captioning / GCoT / Aguvis /
   a11y-list không có so thực nghiệm.
6. 22× không có ý nghĩa thống kê (mẫu số 1 hiệu 2 hạt).
7. MIN +0,63 dưới MDE; 78% gain = CE2 (thêm SFT). Không xác nhận cơ chế.
8. Cùng họ Qwen; lát 325 no-descriptor là treatment-defined.

**Số:** 42% đúng (11,8/28,1). 1,93 / 2,19 / 2,44 cộng được nhưng abstract chọn 2,19, intro chọn
1,93. *"Outcome space chỉ trắng/âm"* **sai**: chính bài tính S2/202 = 65% thì tới cạnh +1,7.
Table Venus trộn raw n=2532 và rescale 4463. 228 vs 325 no-descriptor (97 không tên vàng, không in).

### A3. Văn phong IEEE (Gemini) — writing 2/5

Tựa overpromise. Abstract tường chữ, quá nhiều số. Fragment *"First, an instrument…"*.
*will never exist* = melodrama. *before speaking* nhân hoá. Calibration + Pre-registration =
tường chữ (pre-reg → appendix). Theater không phải thận trọng.

### A4. Thống kê / pre-reg (Claude) — protocol = LIABILITY

Số học nội bộ **reconcile tốt** (4138+325=4463; phân rã −1,93 khớp; χ² continuity correction;
4,2 pp = 25,2×738/4463; 78% = 2,24/2,87). **Không bịa. Protocol hỏng.**

- **L1 chí tử.** 3/7 nhánh huỷ **23/8 sau khi đã có điểm S2** (S2/202, S2r, S2-nopoint).
  S2r = đối chứng duy nhất tách *"descriptor sai"* vs *"mọi prefix / độ dài token"*.
  S2-nopoint = slot toạ độ. Mất chúng → attribution *"commitment"* sụp.
- **L2.** Band −2,8 … +1,7 **bất đối xứng** (dễ dương, khó hại). |−2,19| > 1,67 và > 2,11;
  khoảng một-hạt loại 0 → theo rule hẹp = **harm**. Bài chỉ dùng ngưỡng rộng nhất.
- **L3.** σ = 0,46 từ **1 df**. *"16,9 SD"* spurious. Nhiễu seed báo 0,38 / 0,46 / ±1,3 tuỳ câu.
- **L4.** CI một-hạt cạnh band hai-hạt. Table 1 S1 mean **không có CI**. Venus: 3 mẫu số.
- **L5.** 5 hit rule chỉ báo cho S1−Base, không báo S2−S1 (số gần như đã tính trên 698 bước, không in).
- **L6.** Lát *"registered"* thì nội sinh; lát exogenous thì không đăng ký.
- **L7.** G=1091 vs 259 app; G_eff=454 trang trí (DE thật ~1,10). MIN−CE2 SE=0,24 = naive McNemar.
- **L8.** *"Scale not compressed"* (94%) rồi *"shrinkage mechanical"* (Venus thấp đều 2,8–4,1) —
  không cùng đúng. DiD +1,26 loại 0, ngược lợi bài, bị gạt *"exploratory"*.
- **L9.** +0,63 p=0,011 không khớp ô rule nào (loại 0 nhưng dưới MDE). Nhánh bảo đảm inconclusive
  trước khi chạy.
- **L10.** *"Paired against S1 seed 101"* không mua variance reduction. CE2/MIN thừa hưởng draw S2/101.

**Lỗi số phải sửa:**
1. Abstract *"loses 25.2 where it does not"* — phần bù ô đúng tên/điểm ≈ **−13,1 pp**, không −25,2.
2. Conclusion *"most of that cost"* / *"largest locus"* gán cho no-descriptor (34%) trong khi ô
   nhận dạng sai = **−4,17 pp toàn cục**.
3. Ngưỡng 2,8 không ghép từ 0,38+0,46 doubled (~1,0) trừ khi nhân hệ số power 2,8 **chưa in**;
   0,38 và 0,46 cùng từ hiệu 0,52 → double-count.
4. Ô n=893 không tên vàng, Δ ≈ **+1,8**, **không in**, ngược story.
5. Δ trên bảng chéo 3245 bước = **−2,26**, tệ hơn headline −1,93.

**Khác (nhỏ, cùng chiều hoặc gây nhầm):** 78,4 vs 78,5 · làm tròn 62,8/75,5 · Δ in +0,5 vs 0,6 ·
94% vs 93,5% · usable range 62,9 vs 63,7 · 70,0 withdrawn rồi Table 2 · 228 vs 325 ·
*"six"* vs *"four"* alternative explanations · 73,6+22,0=95,6 thiếu 4,4% ·
Tol. human 84,3 trùng injection 84,3 — xác nhận không copy-paste.

**8 câu Results sạch (ý Claude):** không gán nhãn đăng ký cho S2 · báo 28% cạnh 42% ·
Δ 2 hạt không tính được · phân rã số học + exploratory · MIN−CE2 chỉ nhiễu dụng cụ, không nhãn.

---

## PHẦN IV — VĂN PHONG (ĐÀO SÂU, 31/8)

Đếm trên `main.tex` dòng 72–664 (thân bài, không bibliography).
Giám khảo: cáo / biện / copy-editor / chủ tịch nhà.

### IV.0 Chẩn đoán một câu

Bài **không** giống ChatGPT mặc định (Furthermore, SOTA, em-dash, "delve", "tapestry",
"robust framework").
Bài **giống** lớp 2024–2026: *Claude-careful + ACL Findings registered-report + non-native
over-edit*. PC FAIR ít khi viết chữ "AI"; họ viết **overwritten / defensive / exhausting**.

| lớp | nguồn | ví dụ | giữ? |
|---|---|---|---|
| **A — xương người** | nhật ký lab, số xấu, sẹo pipeline | off-by-one join; ±151 vs ±336 px; 459/14 000 = 3,3%; leak 12 verb; L4/A100 `total_flos`; "broken installation fired"; 30,7% tâm màn | **Giữ nguyên** |
| **B — da LLM** | prompt *"make it rigorous / honest / pre-registered"* | `rather than` ×22; `where` = whereas; thề; chiasmus; First/Second/Third; nhân hoá rules; abstract = conclusion | **Cạo** |

Sửa văn = cạo B, không làm hỏng A. **Không** thêm lỗi tiếng Anh để "giống người".

### IV.1 Inventory — `rather than` = 22 (đúng 22, không ước)

Mỗi lần = khuôn *X, not Y disguised as scholarship*. IEEE conference English dùng được
**3–4 lần/bài** khi đối lập thật (trained vs prompted; emitted vs consumed). **22 lần = tic.**

| # | dòng | cụm | loại |
|---|---|---|---|
| 1 | 80 | 75.7 rather than 100 | số + slogan (lặp caption bảng) |
| 2 | 90 | identification rather than on the prefix | slogan title (lặp intro + §8 + conclusion) |
| 3 | 160 | trained rather than prompted | **hợp lệ** (GCoT) |
| 4 | 165 | source rather than beliefs | triết ALOHa, có thể `instead of` |
| 5 | 212 | emitted rather than consumed | **hợp lệ** (một lần) |
| 6 | 214 | commitment rather than extra input | gần #5, dư |
| 7 | 267 | depress rather than inflate | phòng thủ metric |
| 8 | 323 | sentences rather than action log | **hợp lệ** (teacher-forced) |
| 9 | 336 | flag rather than hide | thề — xoá |
| 10 | 348 | 75.7 rather than 100 | lặp #1 (caption) |
| 11 | 427 | own denominator rather than rescaled | kỹ thuật, giữ hoặc `not the` |
| 12 | 438 | inconclusive rather than a negative | thề nhãn |
| 13 | 446 | report this rather than let a reader infer | thề |
| 14 | 452 | identification rather than prefix | lặp slogan |
| 15 | 486 | rarely contains rather than sampling | dài, cắt |
| 16 | 503 | Ceil. rather than a causal claim | phòng thủ bảng |
| 17 | 529 | bounded rather than removed | phòng thủ collider |
| 18 | 532 | absence of signal rather than of effect | chiasmus |
| 19 | 617 | boundary rather than contradiction | slogan Related |
| 20 | 622 | identification rather than prefix | slogan lần 4 |
| 21 | 643 | adversarial rather than paraphrase | Related, giữ được |
| 22 | 656 | bound rather than exclude | thề Limitations |

**Giữ tối đa #3, #5, #8, #21.** Xoá hết thề (#9, #12, #13, #22) và slogan lặp (#2, #14, #20).

### IV.2 Năm máy văn (cùng một bài, lặp)

**Máy 1 — Antithesis / chiasmus.** Cấu trúc *A where B, B where A* hoặc *not X rather than Y*:
abstract *gains 5.7 where … loses 25.2 where it does not* · intro *works where … costs heavily
where it does not* · §8 *adds 5.7 … subtracts 25* · Conclusion *pays where identification
succeeds* · Qual *Neither failure is a failure of fluency*.
Đó không phải thận trọng, đó là **đối xứng tu từ**. Một lần trong Results là đủ; bốn lần = PC nhớ
slogan, quên số.
Sửa: một câu số học, không vế đối — *On 1,871 steps with a correct name and in-tolerance point,
S2 is +5.7 over S1. On 738 steps with both wrong, S2 is −25.2 (n=738). The split uses S2's own
labels; it is exploratory.*

**Máy 2 — `where` = `whereas` / `while`.** IEEE dùng `where` cho *place* hoặc *in the case that*.
Bài dùng như liên từ đối lập (dòng 278, 297, 253, 558). Đếm cảm giác ~15 chỗ. Đổi thành
`while` / `but` / hai câu.

**Máy 3 — Thể liêm chính (moral theater).** Cùng một ý *"chúng tôi không giấu"* viết ba lần gần
nhau: *We flag rather than hide…* (336) · *We report this rather than let a reader infer a
suppressed positive* (446) · *We do not say what the pre-registration forbids* (629–632).
Cộng: *rules refuse a conclusion* (86, 139); *will never exist* (88); *permanently incomplete*
(127, 340, 629); *and it will not be* (127, 340).
Độc giả tin **hành vi** (một câu: second S2 seed not run, 23 Aug, budget). Họ không tin vì được
thề. Thề nhiều khi protocol yếu (huỷ run sau khi đã có điểm) → **phản tác dụng**: PC đọc
*protest too much*.
Sửa một lần, xong: *The second S2 seed was not run (budget, 23 August). We do not treat the
one-seed Δ as the registered two-seed estimand.* **Không:** never / permanently / refuse / flag /
infer suppressed.

**Máy 4 — Number-as-armor.** Abstract 1 câu = 8 số. Câu Second (80–84) nhồi 47.6, 59.4, 42%,
78.4%, two seeds, 22×, second grounder. Câu Third (84–91): 57.2, 2.19, band, 5.7, 25.2.
IEEE abstract: **một kết quả chính + một điều kiện**. Không phải appendix trong 272 từ.
42% và 78,4% cùng một phép (khoảng 47.6→75.7). 22× = 11,8/0,52, mẫu số 1 hiệu hạt — không được
vào abstract.

**Máy 5 — Refrain.** Abstract ≈ Intro (i)–(iv) ≈ Conclusion, cùng 4 nhịp: thước hai đầu 75.7/12 ·
SFT 47.6→59.4 · S2 incomplete/inconclusive · +5.7/−25 identification.
IEEE: abstract = phát hiện; intro = lỗ hổng + câu hỏi; conclusion = 4–6 câu, **không** nhai lại
5.7/25. Kết luận hiện tại ~160 từ ≈ 60% abstract.

### IV.3 Dấu "Claude careful 2025" (không phải ChatGPT)

| tic | chỗ | ghi chú |
|---|---|---|
| *both* nhấn | abstract *calibrated at both ends* | LLM thích both/all/every |
| *unusually* | intro (i) measured floor | tự khen thước |
| *nonetheless* | intro *mechanism is nonetheless legible* | chuyển cảnh kịch |
| *deliberately conservative* | §5 band 2.8 | tự gắn nhãn phương pháp |
| *Our claim is narrow* | Related 158 | ACL meta |
| *Two cautions apply* | Related 165 | mở đoạn textbook |
| *Two design choices are not free* | §4 209 | mở đoạn LLM |
| *This is a model study* | intro 109 | tuyên ngôn thể loại |
| *a different consumer* | abs + intro ×3 | nhân hoá độc giả |
| *before speaking* | heading câu hỏi 2 | ẩn dụ miệng |
| *outcome space* | contrib + results + concl | jargon pre-reg, 1 lần đủ |
| *the actionable variable* | §8 623 | consultant-speak |
| *license no verdict* | §8 | luật sư |
| *What the missing run could have changed is fixed by* | 441 | kịch bản phản thực |
| *16.9 seed-to-seed SD* | 444 | theater số (1 df) |
| *First / Second / Third* | abstract | **cấm** IEEE trừ enumerate phương trình |
| *we contribute three things* vs (i)–(iv) | abs vs intro | copy-paste sót |

**Không có:** Furthermore, Moreover, Importantly, Notably, It is worth noting, SOTA, novel
framework, play a crucial role. → Detector *"ChatGPT vocab"* **âm tính**. Detector *"LLM edit
pass"* **dương tính**.

### IV.4 Câu quá dài / clause-stack (mổ)

- **Abstract câu 1–2 (73–76):** *A GUI agent outputs… We train… a different consumer… and we
  contribute three things.* Ba việc một hơi: (agent vs người) + (train) + (đếm đóng góp).
  Sửa: ba câu. Bỏ *consumer*. Bỏ *three things*.
- **Abstract First (75–80):** fragment *First, an instrument…* — không có động từ chính cho
  "instrument". IEEE không thích telegraphic list trong abstract.
- **Intro 125–133 (một khối):** tradition citing → 1,825 failures → registered branch → byte for
  byte → four runs → permanently incomplete → 1.93 → nonetheless legible → works where / costs
  where → largest locus → stage-2 MIN +0.63 → 78%. Đó là **toàn bộ paper** nhét vào 8 dòng.
  Tách: 1 đoạn S1, 1 đoạn S2 chỉ *"not run"*, **không** +5.7/−25 ở intro (để §8).
- **§5 325–337:** một đoạn = 4 nhãn pre-reg + công thức 0.38+0.46 doubled + band lệch + MIN 2.11
  + √2 σ + 27 amendments + thề six later. Sửa: bảng 2×2 nhãn; 2.8 vào footnote hoặc `106`;
  một câu amendments.
- **Conclusion 660–664:** bốn câu, câu cuối ~55 từ, lại pays/worth/must act.
  Sửa: bốn câu ngắn; câu 4 không lặp 5.7/25.

### IV.5 Đoạn **đừng** sửa (giọng người, PC tin)

Giữ nguyên nhịp, chỉ sửa typo nếu có:

1. Join test: OCR 48% vs 20% shifted (177–178).
2. Hình Voronoi caption: Gender vs Birthday, 128 px, ±336 (242–247) — **đây là hình hay nhất**,
   văn khớp hình.
3. 30.7% horizontal = screen centre (266–267) — cắt *rather than inflate* phía sau.
4. On-policy 459/14 000, quartiles 70 / 351 / 748 px (479–486) — cắt *rather than sampling* cuối.
5. Qual table verbatim (586–605) — caption (a)(b) bỏ *pays* / *binds*; để *succeeds* / *fails*.
6. Teacher-forced: history = human sentences not action log (323) — giữ `rather than` lần này.
7. Byte-identical 2,811 (306).

Những đoạn này **chứng minh** người viết đã đụng data. Lớp B đang **che** chúng.

### IV.6 Cáo / biện / copy-editor (đợt B, giữ nguyên án)

**Cáo.** Over-compressed human draft → Claude/ChatGPT *"more careful, more like a registered
report"*. 12 dấu: stack mệnh đề; A/B/C/D; rather than; theater; number-as-armor;
abstract≈conclusion; 3 vs 4; meta study; consumer/speaking; both/unusually/nonetheless;
nhiệt độ đều (mọi đoạn cùng mật độ phòng thủ).

**Biện.** Không phải LLM hallucinate số — số khớp file (đợt A). Bề mặt = non-native
**over-edit**, không phải native *casual*. FAIR maybe *"sounds AI"*; nhãn đúng hơn:
**overwritten**. Viết vụng cố ý = tự hại.

**Copy-editor.** Rule 0: câu thêm **dữ kiện** hay **tư thế**? Tư thế → xoá.
Ba lời thề một section = smoking gun của pass *"make it honest"*.

### IV.7 House style — 15 cấm (giữ) + 8 cấm thêm

Cấm cũ 1–15 như trước (`rather than` max 4; không First/Second/Third; không thề; không nhân hoá
rules; không `where`=whereas; không chiasmus; không unusually/nonetheless/deliberately
conservative; không câu 35–45 từ; không refrain).

Thêm:

16. `consumer` / `before speaking` / `name the element before writing` → *human reader* /
    *before the scored sentence*
17. `outcome space` quá 1 lần
18. `actionable variable` / `license no verdict`
19. `16.9 SD` / kịch bản 65.0% missing seed (để appendix nếu cần)
20. `This is a model study`
21. `Our claim is narrow` / `Two cautions apply` / `Two design choices are not free`
22. In đậm *both*, *unusually*, *measured floor* như hàng hiệu
23. Lặp slogan identification vs prefix ngoài **một** câu Results

### IV.8 Bản sửa câu — dán được vào tex

**Abstract (thay toàn bộ; ~170 từ; số đã gạn đợt A):**

> GUI agents emit click coordinates. We generate one English instruction for a human reader,
> fine-tuning Qwen2.5-VL-3B on AndroidControl with no new labels. A separate grounding model
> scores a sentence as executable if the action class matches and the predicted point lies in
> the cell of the touched element. Human-written instructions score 75.7% on 4,463 touch steps.
> The dummy "tap the button" scores 12.0% (n=800). Fine-tuning raises the base model from 47.6%
> to 59.4% (two seeds). A second grounder, not trained on AndroidControl, keeps the same sign on
> the fine-tuning gain. A descriptor prefix before the same sentence scores 57.2% at one seed,
> 2.2 points below the two-seed sentence-only mean. The second treatment seed was not run.
> A post-hoc split by the prefix's own name and point is exploratory: +5.7 when both are right
> (n=1,871) and −25.2 when both are wrong (n=738).

Bỏ: First/Second/Third; 42%; 78,4%; 22×; *independently trained* (đổi wording); *refuse a
conclusion*; *will never exist*; *worth* / *rather than*.

**Intro — hai câu hỏi (thay 114–133):**

> We ask whether this supervision works. Fine-tuning moves executability from 47.6 to 59.4 at
> two seeds. The gap remains after dropping sentences that copy the reference's content words.

> We also ask whether naming the element in a prefix, then writing the same sentence, helps.
> That comparison was specified over two seeds per branch. The second treatment seed was not
> run. At the available seed the prefix sits 1.93 points below its matched control. A later
> preference stage, still one seed, adds 0.63 points over a matched supervised control.

Bỏ: *before speaking*; *permanently*; *nonetheless*; *works where / costs where*;
*largest locus*; 78% ở intro.

**Contributions (135–142) — ba mục, khớp abstract:**

> (i) an executability score with a measured human-reference level of 75.7% and a
> contentless-sentence floor of 12.0%; (ii) a no-new-labels fine-tune, 47.6 → 59.4 at two seeds,
> same sign under a second grounder not trained on this corpus; (iii) a one-seed
> descriptor-prefix comparison, reported as incomplete relative to the two-seed plan, plus an
> exploratory name×point split.

Bỏ (iv) hoặc gộp 3 chữ vào (iii). Bỏ *unusually*, *refuse a conclusion*, *what the prefix is worth*.

**Amendments (336–337):**

> Twenty-seven amendments are dated and appended. Twenty-one predate any executability score.
> Six later ones moved the headroom up and the threshold down; the first of those also cut the
> control's share of the ceiling from 84.4% to 78.0%.

Xoá *We flag rather than hide.*

**Missing seed (339–341 + 441–446):** giữ đoạn in đậm 339. Xoá *permanently* / *will not be*
lần 2. Xoá nguyên đoạn 441–446 (65.0%, 16.9 SD, remaining outcome space, report rather than
infer). Một câu: *A two-seed mean is not reported.*

**Qual closer (610):** xoá *Neither failure is a failure of fluency.* →
*In (b) the sentence follows a nameless descriptor. In (c) the action class is wrong.*

**Implications (621–624) + Conclusion:** một câu — *The name×point table is not a registered
effect of the prefix; identification accuracy did not move enough under MIN.*
Conclusion không lặp +5.7/−25. Câu chốt: *Whether the prefix helps is unset. Identification
accuracy is the quantity that has to move.*

### IV.9 Nhịp sau khi cạo (checklist biên tập)

- Mỗi 3–4 câu: một câu 8–12 từ.
- Một ý / một câu. Số vào câu riêng.
- `rather than` còn ≤ 4, không ở abstract.
- Abstract ≠ conclusion (conclusion không có 5.7, 25, 2.19, 0.63 trừ khi 1 câu "see §").
- Title không *Pays* / *Pre-Registered*.
- Đọc thành tiếng 2 phút: nếu nghe như **thề** thì cắt.

### IV.10 Án văn phong (cập nhật)

Writing **2/5** đúng. Cạo lớp B có thể lên **3+** mà không thêm thí nghiệm — đó là việc 48 giờ rẻ
nhất. Không cạo thì PC nhớ giọng hơn số; số xấu (đợt A) + giọng thề = *weak reject* chắc hơn
*borderline*.

---

## PHẦN V — VIỆC SỬA (GỘP HAI ĐỢT)

### 48 giờ, không GPU

1. Title 1–2 dòng, bỏ pre-registered / condition. Ví dụ: *An Executability Metric and
   Automatically Supervised Fine-Tuning for GUI Instruction Generation.*
2. Abstract ~180 từ, một số 47.6 → 59.4 vs 75.7; S2 một câu single-seed, **không** nhãn
   inconclusive đăng ký; bỏ 22× và 78,4%; 42% nếu giữ thì kèm 28% bước không copy reference.
3. Sửa *"loses 25.2 where it does not"* và *"largest locus"* / *"most of that cost"*.
4. `tab:main`: Base → S1 → S2; một số đậm; bỏ `\sbar`.
5. Hình 1 = screenshot 3 cột (`tab:qual`); Voronoi thu nhỏ.
6. Pre-reg: 1 câu + trỏ `106`; xoá ba lời thề; `rather than` ≤ 4.
7. Không gán positive/inconclusive/harm cho S2. In ô n=893 nếu giữ bảng chéo.
8. *"Independently trained"* → *"not trained on AndroidControl"* + limitations cùng họ.
9. Compile PDF thật; font embedding / PDF/A.
10. Bẻ nhịp: mỗi 3–4 câu một câu 8–12 từ.

### Không làm trước deadline FAIR

S2/202 + S2r + S2-nopoint + chấm người + grounder khác họ = **bài khác**.

---

## PHẦN VI — BẤT ĐỒNG ĐÃ XỬ

| bất đồng | xử |
|---|---|
| Hình thiếu vs có | Có. Lỗi = **loại** hình. |
| Inconclusive trung thực vs theater | Minh bạch hơn giấu; **không** đủ làm verdict đăng ký. Band bất đối xứng + missing by design. |
| Bài thước vs mô hình | Headline = instrument + S1. S2/MIN = exploratory, không (iii)(iv). |
| Copy-editor giữ 22× | Không. Nhịp lấy copy-editor, số lấy đợt A / C thống kê. |
| IEEE chair rewrite còn First/Second + 42% | **Không dán.** Chair đếm đúng tic, bản abstract của chính chair tái phạm. |
| Copy-editor C vẫn *"inside inconclusive band"* | **Không.** Thống kê C: luật không áp khi thiếu 2 seed; interval S2 không chứa 0. |
| *"Inconclusive"* thiện chí vs chọn ngưỡng | Thiện chí (MIN dương cũng bỏ) **và** chọn nhân đôi σ chỗ âm. Câu sạch: *registered two-seed test was never performed.* |

---

## PHẦN VII — ĐỢT C: BẢY AGENT CHẠY THẬT

Độc lập. Trùng đợt A/B thì ghi *khớp*. Dưới đây chỉ **lời mới** hoặc **số mới**.

### C1. Nội dung — S 2 / E 2, ACL reject; FAIR borderline nếu hạ pretension

Khớp A2. Thêm:

- **75,7 không là *"human level"***: là human *reference qua grounder*.
  Floor-share (59,4−12)/(75,7−12) = **74,4%**, không 78,4%. Floor đo trên slice 800 / trần 74,9
  — phép này cũng không sạch.
- 27 amendments, sáu cái hậu điểm *moved headroom up, threshold down* — pre-reg **không audit
  được** (không hash).
- S1 = QLoRA trên instruction **đã có**; 95,6% app overlap, 17,3% test reference verbatim trong train.
- S2 87,1 > Ceil. 86,6 ở hàng 1 = tín hiệu *write for the grounder* (Limitations có, không nối
  với bảng).
- 48h không GPU: đổi title, bỏ *"human level"*, hash registration. **Human eval subset nâng
  soundness rõ nhất** trong các việc không train.

### C2. Văn phong — writing 2/5

Khớp inventory 22× `rather than`; 6 `where`=whereas. 12 câu mổ + rewrite ngắn.
**Chủ tịch gạt abstract/conclusion của Gemini:** vẫn First/Second/Finally, vẫn *closing 42% of
the gap*, vẫn *"stark conditional effect"* không gắn collider. Dùng nhịp câu 8–17 từ; **không**
dán nguyên abstract đó.
Giọng: *human-lab-notes + diễn kịch Claude*. IEEE muốn technical report, không hồi ký liêm chính.

### C3. Thống kê — protocol = liability; lỗi số học **đúng bất thường**

Khớp A4 (F1 −13,1; n=893 Δ≈+1,8; 16,9 SD 1 df). **Mới, fatal:**

| | |
|---|---|
| **F2** | Thiết kế thật = **1 seed vs 2 seed** → ngưỡng khớp = **1,90 pp**. \|−2,19\| > 1,90. *"Verdict same under all three"* **sai** với 2/3 ngưỡng nếu áp S2. Nhân đôi σ chỗ S2 âm; **không** nhân đôi chỗ MIN dương (cùng cặp seed S1). |
| **F3** | Luật: *interval covering zero + \|Δ\| < MDE = inconclusive*. S2 **[−3,06, −0,75] không chứa 0** → chữ nghĩa = **harm**. MIN **[+0,16, +1,10] không chứa 0** → chữ nghĩa = **positive**. Cả hai bị nhét *"inconclusive"*. |
| **F5** | Injection n=250: 84,3% ×250 = **210,75 không nguyên**; 99,7% ×250 = **249,25 không nguyên**. 84,3 trùng Tol. human Table 1. |
| **F6** | Mẫu n=300 trần 70,0 CI tới 75,3; full-scale **75,7 ngoài CI đó**. Vẫn dùng 300 cho adequacy + Venus hàng 3. |
| **F7** | Cùng section: band *"fixed before any score"* và six later *"moved the threshold downward"*. RR chỉ từ chối nếu không in bảng 27 amendment. |
| **F8** | 0,38 = SE cặp seed **cùng nhánh**; SE S2−S1 từ CI bài ≈ 0,589. Không được vừa nói contrast-specific vừa dùng 0,38 cho mọi contrast. |

Sáu cách dựng ngưỡng: 3 inconclusive / 3 ngoài band. **Câu được phép:** *the registered two-seed
test was never performed; single-seed Δ = −2.19, inside −2.8…+1.7 but outside design-matched 1.90.*

**Đúng, đừng sửa:** 14 966 784 LoRA; χ² 243,2; 8 072 bước; 0,38=√286/4463; phân rã −1,93.

**Tám câu Results sạch:** xem transcript agent (câu 2 vẫn có 22× — **chủ tịch bỏ câu 2**, giữ 1,
4–8; câu 3 Venus đổi *"94%"* → *"+10.35 → +9.68"*).

### C4. Hình thức — 2/5

Khớp A1. Thêm: chỉ có `main.xdv`, **không** `main.pdf` trên đĩa; bookmark `7.3\%` hỏng; Venus
không đáng một bảng; MIN **đậm** cướp 59,4; `\IEEEtriggeratref` trang 8.

### C5. Cáo — epistemic theater, không ChatGPT vocab

**12 smoking gun mới** (không chỉ `rather than`):

1. *second run will never exist* — fatalism
2. *sets an expectation without settling it* — aphorism
3. *G only localises, geometry against g decides* — 3-beat defense
4. *actively misleads / disposes of the reading* — tranh tụng
5. *researcher degree of freedom* — over-formal
6. *flag rather than hide*
7. *closed it at inconclusive / suppressed positive*
8. *Measurement noise is separable here and training noise is not*
9. *repairs the damage the descriptor target did to itself*
10. *What the design costs here is commitment / committed to nothing*
11. *boundary condition on that prior rather than a contradiction*
12. *We do not say what the pre-registration forbids* — luật sư

**Người:** off-by-one join; 30,7% tâm màn; L4/A100 `total_flos` + 14 966 784.
**PC:** *overwritten*, không viết "AI".

### C6. Biện — cáo một phần; không thêm lỗi ngữ pháp

Khớp B2. Tám nhát cắt (quote+thay). Câu 1 biện vẫn còn `rather than` — khi dán, đổi:
*one-sentence instructions for a human reader, not click coordinates.*

### C7. Copy-editor — 20 cấm + 4 đoạn English

Ban-list thêm: hệ số nhân không neo (22×, eight times, fourfold, 16.9 SD); % của % không n;
nghiêng tranh luận; *byte for byte* 4 lần; hedge xếp tầng.

**Chủ tịch sửa bản copy-editor trước khi dán:**

- Abstract C7 còn *rather than to an action head*, còn *inside the inconclusive band*, còn
  *All scores are read against 75.7*. **Cắt ba cái.**
- Contributions (iii) còn *remaining outcome space* — cắt. Dùng **325 không 228**: đúng (F4).
- Conclusion còn *condition for the descriptor to pay* — cắt slogan.

---

## PHẦN VIII — VIỆC SỬA CẬP NHẬT SAU ĐỢT C

Thêm vào list 48h:

11. Đổi *"human level"* → **human-reference pipeline score**.
12. In ô n=893, Δ≈+1,8 hoặc bỏ story *"chỉ trả khi nhận diện đúng"*.
13. *"Loses 25.2"* chỉ với **both name and point wrong, n=738**; phần bù *"does not identify"* = **−13,1**.
14. Không viết inconclusive/harm/positive cho S2. Một câu: *two-seed estimand not computed.*
15. Injection 84,3% / 99,7% trên n=250: **sửa mẫu số** hoặc làm tròn nguyên.
16. Một `\textbf` duy nhất: **59,4**. MIN không đậm.
17. Cạo 12 smoking gun cáo C5 (kể cả *expectation without settling it*, *committed to nothing*).
18. PDF thật, không nộp `.xdv`.

*Hết. Đợt C là debate chạy agent; Phần I–VI là lần gom trước.*

---

## Đối chiếu với bản WSL hiện tại (31/8, chưa commit)

⚠️ Hội đồng chấm clone `598e4ff`. Working tree WSL **đã đi trước một lượt vá**
(`main_TRUOC_PHANBIEN_31_8.tex.bak` = đúng bản `598e4ff`). Những mục sau **đã làm rồi**,
đừng làm lại:

| mục | trạng thái |
|---|---|
| Abstract viết lại theo IV.8 | ✅ đã thay, 246 → 205 từ |
| Intro hai câu hỏi (IV.8) | ✅ đã thay |
| Contributions còn **ba** mục, khớp abstract (L4) | ✅ đã sửa |
| *"independently trained"* → *"not trained on this corpus"* (L2, mục 8) | ✅ 0 lần còn lại |
| *"loses 25.2 where it does not"* → *both wrong (n=738)* (mục 13) | ✅ đã sửa trong abstract |
| *"three things"*, *"a different consumer"*, *"before speaking"*, *"This is a model study"*, *"Our claim is narrow"*, *"Two cautions apply"*, *"Two design choices are not free"* | ✅ đã cạo |
| *"We flag rather than hide"*, *"will never exist"*, *"permanently incomplete"* | ✅ đã cạo |
| `rather than` 22 → **17** | ⚠️ giảm chưa đủ (đích ≤ 4) |

Còn nguyên: title · `\sbar` (15 chỗ) · cột *"vs. human level"* · 78,4% · thứ tự bảng · hình
screenshot GUI · nhãn inconclusive cho S2 · ô n=893 · injection 250 · six-vs-four · 73,6+22,0.

---

## ĐÃ VÁ 31/8 (lượt trợ lý, sau khi đọc phản biện)

Bản trước lượt này: `paper/fair2026/main_TRUOC_VA_PHANBIEN_31_8.tex.bak`.
Sau mỗi bước đều dựng lại; kết thúc **8 trang · 0 overfull · 0 tham chiếu hỏng · 0 cảnh báo
bookmark**. Đối chiếu toàn bộ chữ số trước/sau: chỉ mất tham số hình của `\sbar` đã gỡ, thêm
đúng tám số cố ý (`4.4` · `17` · `881` · `1.48` · `1.16` · `4.10` · `13.1` · `1.374`).

### ⭐ Đòn CHẶN — F3, đã xử bằng cách khai cả hai cách đọc

`report/106` có **hai bản luật đọc**, và bài in bản này rồi áp bản kia:

| bản | điều kiện Trắng | S2 rơi vào |
|---|---|---|
| gốc 5/8, dòng 85 | KTC phủ 0 **VÀ** \|Δ\| < MDE | **Âm** (cận trên −0,75 < 0) |
| sửa đổi (w) 17/8, dòng 1268 | dải −2,8 … +1,7 (chỉ hàng Dương/Âm mới đòi KTC loại 0) | **Trắng** |

⭐ **(w) ngày 17/8 khoá TRƯỚC khi train S2** (nguyên văn mục (w): *"trình tự cứng ở mục 5 đòi
phải hoàn tất trước khi train S2"*), nên dải là hợp lệ — **không** phải ngưỡng dời sau khi thấy
điểm. Nhưng nó khoá **sau** khi S1/Base/trần đã có điểm, nên câu cũ *"both edges fixed before
any score existed"* là **sai** và đã sửa thành *"filed after the control branch was scored and
before the treatment branch was trained"*.

Bài nay in dải (bản đang hiệu lực) làm luật chính, khai rõ mệnh đề khoảng của cùng hồ sơ cho ra
nhãn **harm**, và nói thẳng người đọc theo mệnh đề khoảng sẽ tới nhãn kia. Áp **đối xứng** cho
MIN: khoảng `[+0,16 · +1,10]` loại 0 nên mệnh đề khoảng cho phép gọi **positive**, bài ghi rõ
**không** nhận. Câu *"The verdict is the same under all three"* đã gỡ (sai với S2: 2,19 < 2,8
nhưng > 2,11 và > 1,67).

### Lỗi số — ba cái, đều kiểm được

| chỗ | cũ | mới | căn cứ |
|---|---|---|---|
| dụng cụ | *"84,3% … (injection study, 250 steps)"* | thêm *"with four injected angles each, so 1.000 draws"* | `report/106` dòng 270: **4 lần mỗi bước** ⇒ 843/1000 và 997/1000, đều nguyên. Trên 250 thì 84,3 và 99,7 **bất khả thi** |
| §dữ liệu | 73,6% có tên · 22,0% không | thêm **4,4% chỉ có ký hiệu** | 30.252 / 1.809 / 9.038 = 41.099, cộng đúng (VCL Bảng 3) |
| intro | *"survives six alternative explanations"* | phát biểu thẳng: bỏ bước chép lại câu chuẩn vẫn còn **+8,4 pp** | mục §alt chỉ có **bốn** mục, lại là bốn mục cho hiệu S2−S1 chứ không phải S1−Base |

### Ô bị giấu — đã tính thật, không lấy số của hội đồng

Hội đồng ước *"n=893, Δ≈+1,8"*. **Số thật đo từ tệp thô: n=881, Δ=+1,48 pp, KTC95
[−1,16 · +4,10]** (phủ 0). Script: `harness/o_bi_loai_khoi_bang_cheo.py`, tái lập trùng khít
bốn ô của bảng chéo (+5,72 / +0,54 / +1,11 / −25,20). Đã thêm một câu vào §bảng chéo.

⭐ **Lỗi số #1 của hội đồng đúng, đã xác minh độc lập:** phần bù của ô *"cả hai đúng"* là
**n=1.374, Δ = −13,10 pp** [−15,39 · −10,77], **không phải −25,2** (−25,2 là của riêng ô
*"cả hai sai"*, n=738). Kết luận cũ viết *"loses 25 where it does not [identify correctly]"* —
gán phần bù sai, nay đã sửa.

### Hình thức + văn phong

· **Title** bỏ *"A Pre-Registered Ablation and the Condition Under Which It Pays"*, còn
  **Descriptor-First Supervision for GUI Instruction Generation**. Giữ nguyên phần đầu vì bài
  VCL **đã nộp 30/8** có mục tài liệu trích FAIR theo đúng cụm đó.
· **Bảng chính:** gỡ sạch `\sbar` (kéo theo gỡ luôn gói `tikz`, hết đòn *"TikZ trong bảng"*) ·
  nhan đề cột *"vs. human level"* → **`% of 75.7`**, caption nói rõ 75,7 là **điểm của đường ống
  chấm câu người, không phải trần của con người** · sắp lại **Base → S1 → S2** · chỉ còn **một**
  số đậm là 59,4.
· **`rather than` 22 → 4**, đúng bốn chỗ hội đồng cho giữ (#3 GCoT · #5 emitted/consumed ·
  #8 teacher-forced · #21 adversarial). Bốn cụm C5 còn sót đã cạo.
· **Bookmark PDF:** tiêu đề mục có `$7.3\%$` làm hyperref rơi *math shift* ⇒ bọc
  `\texorpdfstring`, nay **0 cảnh báo**.
· **Kết luận** tách ba đoạn, bỏ slogan đóng bài, sửa hai lỗi gán số nói trên.
· **PDF thật đã dựng** (`main.pdf`, 8 trang, 6 font đều nhúng dạng subset) — đòn 18 xong.

### ⛔ CHƯA làm, có lý do

· **Hình screenshot GUI làm Hình 1.** Đòn đúng về chất, nhưng bài kín đúng 8 trang cứng, thêm
  hình là phải cắt chữ đúng ngày nộp. Có sẵn `paper/vcl2026/hinh/fig_moneo.png` dùng lại được.
· **Human eval subset** (C1 bảo nâng soundness nhiều nhất) · **sửa collider bằng stratify với
  model đóng băng** · **S2r / S2-nopoint / S2/202 / bộ trỏ khác họ** — chính hội đồng xếp vào
  *"bài khác"*.
· **Dán abstract của Gemini hoặc của copy-editor** — chủ tịch hội đồng đã gạt cả hai (Phần VI,
  C7): bản Gemini còn First/Second/Finally và *closing 42% of the gap*, bản C7 còn *inside the
  inconclusive band*, tức dính lại đúng đòn F3.

### Lượt bổ sung (hai đòn còn treo, đã làm nốt)

· **F6 — Bảng 2.** Hàng `Adequacy ceiling (n=300)` đổi tên thành **`Adequacy sample`** (chữ
  *ceiling* chính là thứ đã bị rút), và caption nay nói thẳng: **75,7 nằm NGOÀI khoảng
  [64,5 · 75,3] của mẫu n=300** — 300 bước là quá ít để định vị mốc, và đó chính là lý do ước
  lượng ấy bị rút khỏi vai trò trần. Trước đây caption chỉ ghi *"full-scale reference ceiling
  is 75.7"*, để người phản biện tự phát hiện chỗ vênh.

· ⭐ **Bắt thêm một chỗ lặp lỗi số #1 mà hội đồng KHÔNG nêu.** Mục *Implications* còn câu
  *"adds 5.7 points where the model identifies the element correctly and subtracts 25 where
  identification has failed"* — đúng cái lỗi gán phần bù đã sửa ở kết luận, nằm ở chỗ khác.
  Nay: **+5,7 trên 1.871 bước · −13,1 trên 1.374 bước còn lại**. Sau lượt này `−25,2` chỉ còn
  **đúng hai chỗ**, cả hai đều gắn với ô *"cả hai sai"* (tóm tắt `n=738` và hàng bảng chéo).

· **`where` = whereas:** vá hai chỗ dùng sai (`$9$ points below their $75.7$, where…` →
  `while`; `passing the action check where only 21 are executable` → `while`). Giữ nguyên các
  chỉ chỗ/điều kiện hợp lệ và chỗ so hai câu ở Bảng chất lượng (hội đồng đã duyệt).
  Bỏ nốt chữ slogan *pays* ở Related Work (*"The prefix pays where…"* → *"helps when"*).

**Trạng thái xuất bản:** `main.pdf` dựng lúc 07:17 — **8 trang · 0 overfull · 0 tham chiếu hỏng
· 0 cảnh báo bookmark · 6 font nhúng subset**. Chữ số vào/ra so bản đầu phiên: chỉ mất tham số
hình của `\sbar` đã gỡ, thêm đúng tám số cố ý.

### Lượt rà văn phong cuối (user yêu cầu: soi câu tu từ)

Quét theo cả danh sách cấm của hội đồng lẫn các mẫu tu từ tiếng Anh. **Sạch: 0 câu hỏi tu từ ·
0 cụm thề (12 smoking gun C5) · 0 tic Claude-careful · 0 First/Second/Third · 0 từ vựng ChatGPT
(Furthermore/Moreover/Notably/SOTA…) · 0 em dash · 0 hedge chồng · 0 chiasmus.**

Bảy chỗ còn lại đã vá:

1. ⭐ **Tật MỚI do chính lượt vá trước đẻ ra.** Thay 11 chỗ `rather than` bằng `, not X` làm cụm
   phủ định-đối lập vọt lên **22** — đúng bằng con số `rather than` cũ, tức chỉ đổi tên cái tật.
   Đã gỡ ba cụm `and not …` cùng khuôn và hai chỗ `not against 100` lặp (thân bài + caption bảng).
   Nay **15 + 2**, phần lớn là định nghĩa bắt buộc (*per-axis rectangle, not a disc* · *touch
   coordinate, not the box centre* · *held out by task, not by application*).
   📌 **Bài học:** sau mỗi lượt cạo một khuôn câu, phải đếm lại **khuôn thay thế**.
2. ⭐ **Refrain.** Đoạn *Implications* nói cùng một ý **bốn lần** (*conditional on identification
   accuracy* · *What has to move is the reliability of identification* · *both the target … and
   the quantity that has not moved enough*) rồi kết luận lặp lần thứ tư. Nén còn **một** câu;
   `identification accuracy` toàn bài nay **3 lần**, `What has to move` **1 lần**.
3. **Đoạn phản thực dùng `16,9 seed-to-seed SD`** — σ ước từ **1 bậc tự do** nên đơn vị đó vô
   nghĩa (C3-L3). Gỡ cả `16,9` lẫn `2,7 such deviations`, giữ nguyên phần thông tin thật (cần
   đạt 65,0% để chạm mép dương, ≤56,0% cho dải âm). Bỏ luôn câu *"The remaining outcome space
   was inconclusive or negative"* mà A2 bác.
4. **`overstate it more than fourfold`** — hệ số nhân trên mẫu số đang tranh cãi (+0,63), lại
   chồng đúng câu `78%` ngay cạnh ⇒ cắt, còn *"so $+2.87$ is not the effect of the objective"*.
   ⚠️ **Giữ `eight times`** ở phép gọi-tên-vs-chỉ-chỗ: nó có neo ngay trước (28,5 vs 3,5 kèm
   McNemar cả hai), khác hẳn `22×` mà C7 cấm (mẫu số là một hiệu hai hạt giống).
5. **Nhãn (a)(b) bảng chất lượng** bỏ *pays* / *binds* đúng yêu cầu IV.5: nay tả thẳng hành vi
   (*"The descriptor names the right element, and the sentence succeeds"*). Chữ `pay` nay **0 lần**
   toàn bài, khớp với việc đã bỏ nó khỏi title.
6. **Giọng nói-với-người-đọc** ở §S2 (*"a reader who prefers the interval clause is reading the
   same numbers and should reach the other label"*) → phát biểu thẳng.
7. **Đồng bộ cách tả bộ trỏ thứ hai:** kết luận ghi *"trained on different data"* (mơ hồ, dễ đọc
   thành không chồng lấn gì) → **"not trained on AndroidControl"**, khớp tóm tắt và §Venus.

⛔ **F8 đã xem và KHÔNG sửa** — bài không hề dùng `0,38` cho mọi contrast: nó ghi rõ *"the
bootstrap standard error of the seed pair, $0.38$ pp"* và nêu riêng *"standard errors are
contrast-specific, $0.785$ pp for S1−Base"*. Đòn này đọc sót chữ.

**Xuất bản cuối:** `main.pdf` 11:04 — **8 trang · 0 overfull · 0 tham chiếu hỏng · 0 cảnh báo
bookmark · 6 font nhúng subset**. Không con số kết quả nào đổi trong lượt này (chỉ mất `16,9`
và `2,7` của mệnh đề đã gỡ).
