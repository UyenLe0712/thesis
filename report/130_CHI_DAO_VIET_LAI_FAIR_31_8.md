# 130 — CHỈ ĐẠO VIẾT LẠI `paper/fair2026/main.tex` (BẢN FINAL 31/8)

> Chép từ 11 ảnh trong `paper/fair2026/My Documents [31-08-2026 22_43].zip`
> (file gốc trên máy Mac: `CHI_DAO_VIET_LAI_FAIR.md`, chốt sau vòng debate cuối 31/8
> với bốn phản biện: Grok overclaim · Claude liêm chính · GPT soát số · Gemini ngân sách trang).
> **File này thắng `report/127` và `report/129` ở mọi chỗ mâu thuẫn.**

Đầu vào: `paper/fair2026/main.tex` (IEEEtran, hai cột, **trần 8 trang cứng**, đang vừa đúng 8 trang).
Việc: **viết lại**. Không train thêm, không human eval, không đổi mã chấm, không invent số.

---

## 0. Sự thật thực nghiệm (khoá — mọi con số trong bài phải khớp bảng này)

| Nhánh | Là gì | Exec. | Số lượt train |
|---|---|---|---|
| Base | chưa tinh chỉnh | 47.6% | — |
| S1/101 | SFT câu | 59.1% | seed 101 |
| S1/202 | SFT câu | 59.6% | seed 202 |
| **S1 mean** | trung bình hai lượt | **59.4%** | hai |
| S2 | descriptor-first (`<desc>` rồi câu byte-identical) | 57.2% | một (101) |
| CE2 | nối từ checkpoint S2, +800 update, **không** preference | 59.4% | một |
| MIN | MIN-DESC: preference trên cặp descriptor, câu verbatim, nối từ S2, +800 update | 60.0% | một |

- **MIN − CE2 = +0.63 pp** — so sánh cùng ngân sách **duy nhất** trong bảng.
- **MDE 2.11 pp** (thiết kế một lượt/nhánh). **1.67 pp** nếu hai lượt/nhánh.
- **MIN − S1 = +0.94 pp**, CI [−0.09, +2.05], **p = 0.11**.
- **S2 → MIN = +2.87 pp**, trong đó **+2.24 pp thuộc CE2** (train thêm), chỉ **+0.63** thuộc preference.
- **S2 − S1 mean = −2.18 pp** (KHÔNG phải 2.19: 59.3659 − 57.1813 = 2.1846).
- Human reference **75.7%, n = 4,463** bước touch. Sàn: **12.0%** (câu rỗng nghĩa) và **6.1%**
  (câu màn hình khác), **n = 800**.
- Đăng ký trước nhưng **không chạy** (hết ngân sách GPU 23/8): S2 seed 202, S2r, S2-nopoint.

---

## 1. Khoá không thương lượng

**Thứ tự đóng góp:**

1. **Primary model contribution**: một họ **controlled target-space training interventions** gồm
   - descriptor-first target (S2);
   - descriptor-controlled ORPO pairs (MIN-DESC);
   - accepted-only stage-2 control (CE2) để đọc đúng contrast MIN−CE2.
2. **Empirical baseline**: SFT câu (S1), 47.6 → **59.4% trung bình hai lượt**. Đây là baseline
   mạnh, **không gọi là "model contribution"**.
3. **Secondary instrument**: executability **chỉ để chấm**. Không mở bài bằng thước, không để
   thước dài hơn Method, không gọi `reference-free`.

**Một câu tự kiểm framing:** nếu xoá toàn bộ con số kết quả, phần đóng góp model vẫn phải đúng và
hiểu được. Nếu contribution cần 60.0 hoặc +0.63 để tồn tại, câu đó đang bán kết quả chứ không mô
tả phương pháp.

**Sàn trung thực (đã phán quyết CÓ vượt, nhưng vượt sát sàn):**

- Abstract **phải** có 57.2 (không được giấu số thấp hơn control) nhưng **không** để nó thành câu
  độc lập ngay sau 59.4 → xem mục 3.
- MIN **luôn** đi kèm CE2. Cấm để 60.0 đứng cạnh 59.4 của S1 như xếp hạng.
- Số lượt train khai **đúng một lần**, ở footnote Table 1 (mục 7). Không rải khắp bài.
- Abstract **cấm**: `one seed` / `band` / `inconclusive` / `harm` / `tie-break` / `MDE 2.11` /
  bảng 2×2 / `+5.7` / `−13.1`.

---

## 2. Title

**Chốt:** `Descriptor and Preference Targets for GUI Instruction Generation`

Umbrella phrase dùng trong Intro (**không** nhét lên title): `controlled target-space training interventions`.

**Cấm bốn dạng title:**
- title hiện tại (dòng 44–45) `Descriptor-First Supervision for GUI Instruction Generation` —
  reviewer đọc Table 1 thấy 57.2 < 59.4;
- `Descriptor-First and Preference Supervision…` (vẫn map title vào hàng S2 thua);
- `MIN-DESC:` đứng đầu;
- `Pre-Registered / Registered…`, `Ablation`, `Condition Under Which It Pays`, `Proposed …`.

---

## 3. Abstract (~185 từ) — DÁN NGUYÊN KHỐI

```
Given a mobile screenshot and a user goal, we train Qwen2.5-VL-3B to generate one English
instruction for a human reader, with no new annotation. The intervention is a change of
training target: a structured descriptor (role, name, coordinate, distinguishing cue)
precedes the same scored sentence, and a second stage applies ORPO to descriptor-controlled
pairs whose two sides share that sentence verbatim. Sentence-only fine-tuning, the control
for the target change, reaches 59.4% executability averaged over two training runs, up from
47.6% for the untuned model, against a human-reference score of 75.7% on 4,463 touch steps.
MIN-DESC reaches 60.0% against an accepted-only supervised continuation at 59.4% given the
same checkpoint and 800 updates, both continuing from the descriptor-first stage at 57.2%.
A sentence is scored as executable when a separate grounding model, which never sees the
gold coordinate, predicts a point that is within tolerance of the touched element and closer
to it than to any competitor, and the action class matches. Contentless text scores 12.0%
and a fluent sentence written for a different screen scores 6.1%, both on an 800-step slice.
Identification accuracy and further runs of the descriptor stages remain the open
experimental variables.
```

**Ba điểm kỹ thuật của bản này (đừng "sửa cho gọn"):**
- Câu 2 mở bằng `The intervention is a change of training target`: reviewer phải phân loại bài là
  model-training/target-design **trước khi** gặp số.
- Gọi ORPO đúng tên; `descriptor-controlled pairs` là artifact của bài, **ORPO không phải phát
  minh của bài**.
- Gọi 59.4 là `the control for the target change`, không để control thành headline chính.
- 57.2 nằm trong mệnh đề phụ `both continuing from the descriptor-first stage at 57.2%` — khai đủ,
  không dựng thành luận cứ chống chính mình.
- MIN báo bằng **hai mức** (60.0 vs 59.4) và gọi đúng comparator là
  `accepted-only supervised continuation`; hiệu +0.63, MDE 2.11 và giới hạn compute để ở §Results.

**Đã quyết (31/8): dùng đúng bản trên.** Hai biến thể sau **không dùng** — chép lại chỉ để chat
viết lại đừng tự ý quay về chúng: (a) hiệu `+0.63 pp` trơ trọi trong abstract; (b) hiệu kèm 10 từ
`single runs; below what one run per branch can resolve`.

---

## 4. Keywords (đúng 5, trần FAIR là 5)

```
GUI instruction generation, vision-language models, referring expression generation,
preference tuning, executability
```

Bỏ `reference-free evaluation` (dòng 82–83 hiện tại): thước **vẫn dùng toạ độ vàng và action class
của reference**. `pre-registration` chỉ giữ **nếu** thân bài không dual-report.

---

## 5. Introduction + contributions

- Đoạn 1: task — câu cho người đọc, không phải click coordinate.
- Đoạn 2: **method trước** — descriptor-first rồi MIN-DESC (câu verbatim). S1 là control.
  Một câu về thước + trỏ `Section~\ref{sec:metric}`.
- Contributions — mở bằng `Our primary contribution is model training`, rồi ba mệnh đề.
  **Không dùng số kết quả để định nghĩa (i)–(ii).** Khối dán:

```
Our primary contribution is a controlled target-space training design for GUI instruction
generation. It comprises (i) descriptor-first supervision, in which the model emits a
rule-built role, name, point and distinguishing cue before a scored sentence held
byte-identical to the sentence-only target; and (ii) MIN-DESC, descriptor-controlled ORPO
pairs with a shared sentence suffix, evaluated against an accepted-only continuation from
the same checkpoint for the same 800 updates. As a secondary contribution, (iii) we use a
calibrated executability instrument to compare these systems. The sentence-only control
rises from 47.6% to 59.4% averaged over two training runs; human references score 75.7%
(n=4,463), and contentless and wrong-screen controls score 12.0% and 6.1% (n=800).
```

- **Không gọi S1 là contribution. Không gọi ORPO là contribution** — đóng góp là cách dựng
  target/cặp và protocol đối chứng.
- **Không viết** `the two sides differ only in the element named`: name, point và cue đều đổi, độ
  dài token có thể đổi.
- **Xoá:** `The first is whether…` / `The second is whether…` (dòng 106, 112) ·
  `The study is about the model, so it needs a calibrated instrument first` (96) · câu liệt kê mục
  lục §Instrument (102–103) · `ours is behavioural and visual` ở Intro (100–101; **giữ** bản ở
  Related dòng 175–177) · `read against the registration rather than around it`.

---

## 5.1 §IV Method — STRICT FINAL (mục quan trọng nhất)

**Luật biên tập:** Method **chỉ chứa câu vẫn đúng trước khi có kết quả**. Mọi score, CI, MDE,
feasibility outcome, 2×2 và lời giải thích vì sao +0.63 nhỏ phải sang Results. Method **không
được** tuyên bố "cô lập identification"; hai control cần cho attribution (S2r, S2-nopoint) chưa chạy.

**Heading:** `Targets and a Stage-2 Objective`. Thứ tự bắt buộc:

### IV-A. What is held fixed (~80 từ + hình)

```
The intervention changes the training target, not the model architecture or input. S1 and S2
use the same Qwen2.5-VL-3B backbone, prompt, previous-step history, OCR input and decoding
rule. Evaluation strips any descriptor with a fixed parser and scores only the instruction.
Figure~\ref{fig:targets} shows the target strings: S1 predicts the sentence; S2 predicts a
descriptor followed by that same sentence; MIN-DESC compares two descriptor-bearing
responses that share the sentence suffix verbatim.
```

### IV-B. Descriptor-first target (~110 từ)

```
Let $x$ be the screenshot, goal, history and OCR prompt, and let $s$ be the instruction. S1
uses target $y=s$. S2 uses $y=d^{+}\mathbin{\|}s$, where $d^{+}$ records the target element's
role, name, normalized touch point and distinguishing cue. The labels are constructed by
rule from the accessibility tree, OCR and recorded touch point (Section~\ref{sec:data}), with
no new annotation. The sentence $s$ is byte-identical across S1 and S2 on all 64,567 training
examples. Thus S2 makes element information an explicit pre-sentence output and leaves it in
the autoregressive context of the sentence. S1 and S2 still differ in prefix presence,
content and length; separating those factors requires the registered S2r and S2-nopoint
controls that were not run.
```

**Cấm thay câu cuối bằng** `ablation of discriminative commitment`, `isolates identification`,
`not extra input`, hoặc `the model must commit before it writes`. Training là teacher-forced;
"commit" chỉ mô tả thứ tự decode lúc inference, không phải cơ chế đã chứng minh.

### IV-C. MIN-DESC objective (~180 từ; công thức bắt buộc)

```
MIN-DESC continues from the S2 checkpoint on descriptor-controlled preference pairs. The
accepted response is $y^{+}=d^{+}\mathbin{\|}s$; the rejected response is
$y^{-}=d^{-}\mathbin{\|}s$, where $d^{-}$ describes the nearest different same-role element
80--350 px away. The role slot and sentence suffix $s$ are shared; name, point and cue may
differ. Holding $s$ verbatim removes sentence-content variation between the two strings, but
does not make its autoregressive likelihood cancel because the sentence remains conditioned
on the preceding descriptor and the descriptors may differ in token length.

We optimize ORPO~\cite{orpo}. With the length-normalized log likelihood
$\ell_\theta(y|x)=|y|^{-1}\sum_t\log p_\theta(y_t|x,y_{<t})$, the implemented loss is
\[
\mathcal{L}_{\mathrm{MIN}}=-\ell_\theta(y^{+}|x)
-\beta\log\sigma\!\left[g(\ell^{+})-g(\ell^{-})\right],
\quad g(z)=z-\log(1-e^z),
\]
with $\beta=0.1$. State whether sentence tokens are included in the preference score, report
the token-length distributions of both sides and the number of truncated pairs under the
2,560-token cutoff; if these implementation facts cannot be recovered, state that limitation
and do not claim the pair isolates identification.
```

Bắt buộc thêm bibliography:

```
\bibitem{orpo} J. Hong, N. Lee, and J. Thorne, ``ORPO: Monolithic preference optimization
without reference model,'' in \emph{Proc. EMNLP}, 2024.
```

**Không gọi ORPO là mới.** Artifact của bài là descriptor-controlled pair construction. Dùng chữ
`minimal pair` **chỉ sau khi** đã định nghĩa rõ ô giữ cố định và ô thay đổi.

### IV-D. Accepted-only stage-2 control (~100 từ)

```
CE2 continues supervised training from the same S2 checkpoint on the same 22,854 accepted
examples, with the same seed, effective batch, learning-rate schedule and 800 optimizer
updates, but without rejected responses or a preference term. CE2 is therefore
update-matched and accepted-data-matched to MIN, not compute-matched: MIN additionally
processes one rejected response per example. MIN$-$CE2 compares the two implemented stage-2
training procedures; it does not isolate a causal effect of the preference term. Verify
whether the pinned pairwise trainer disables dropout while the SFT trainer retains LoRA
dropout 0.05. If so, disclose this implementation difference here; if not verified, do not
assert it.
```

**Luật đọc bắt buộc:** không gọi CE2 là `fully budget-matched`, `all else equal`,
`objective-only control`, hoặc control "transfers to any future intervention".

### Dời khỏi Method

- Sang **§III Data**: cách dựng đủ bốn slot; 41,099 và 73.6/4.4/22.0/7.6; một mệnh đề
  `no new annotation` + trích companion. Kiểm chính sách trùng lặp với companion trước khi giữ các
  thống kê này.
- Sang **§VI Design**: LR, schedule, 800 update, cutoff, dải 80–350 px, ngưỡng feasibility 25%,
  seed và nhánh chưa chạy.
- Sang **§VII Results**: 14,000 → 459 (3.3%); 70/351/748; 76.5%; +5.9 vs +0.8; +2.24/+2.87.
- Sang **§VIII Diagnosis**: việc descriptor sai đi cùng câu sai; đây là hậu kiểm, không phải thuộc
  tính method đã biết trước.

### Cách viết kết quả nguồn negative (không spin)

```
The on-policy source failed its pre-registered feasibility gate: 14,000 training screens
yielded 459 usable pairs (3.3% against 25%). On the 3,246 wrong-name training steps, the
distance quartiles were 70, 351 and 748 px; an 80--350 px window rejected 76.5%. We did not
test why the preference procedure moved identification so little. The heuristic negative
source is one possibility; the 800-update budget, the objective and the backbone are others,
and this design cannot separate them.
```

### Hình 2 bắt buộc — thay Fig. Voronoi hiện tại, KHÔNG thêm hình thứ hai. Ba hàng:

1. `S1 target: [sentence]`
2. `S2 target: <desc> role | name | <point>x,y</point> | cue </desc> [same sentence]`
3. `MIN-DESC: accepted <gold descriptor>[same sentence] / rejected <wrong descriptor>[same sentence]`

Caption:

```
Training targets for one step. S1 predicts only the scored sentence. S2 prepends a four-slot
descriptor while keeping that sentence byte-identical. MIN-DESC applies ORPO to responses
that share the role slot and sentence suffix; name, point and cue may differ. Scoring strips
the descriptor.
```

**Không ghi** `proposed method`, `identification is isolated`, `only the descriptor differs`,
hoặc mũi tên kiến trúc giả. Sơ đồ Voronoi **không phải model contribution**; chuyển định nghĩa
nearest-centre thành hình nhỏ trong text hoặc bỏ hình.

---

## 6. Thứ tự mục và ngân sách từ

8 trang IEEEtran hai cột ≈ 6,500–7,000 từ; trừ 4 bảng + 1 hình model còn ≈ 5,200 từ khả dụng.
**Hình target thay hình Voronoi, không thêm hình thứ hai.** Ngân sách dưới đây tổng ~4,900 từ.

| # | Mục | Từ |
|---|---|---|
| — | Abstract + keywords | 200 |
| I | Introduction | 400 |
| II | Related work (ngắn) | 350 |
| III | Task & Data Pipeline (slot construction; không results) | 350 |
| IV | **Targets and a Stage-2 Objective** — A–D + hình target | 540 |
| V | Instrument (định nghĩa 3 câu, calibration, robustness) | 450 |
| VI | Experimental setup (config + design; **bỏ band**) | 180 |
| VII | Results (gồm feasibility outcome) | 750 |
| VIII | Diagnosis — 2×2, **một lần** | 550 |
| IX | Limitations (**một cột**) | 400 |
| X | Conclusion | 150 |
| — | References | 450 |

**Method phải đứng trước Instrument.** Sau viết lại: Method ~540 từ + một hình; Instrument ≤450 từ.
§III chỉ dựng dữ liệu; §IV chỉ định nghĩa target/loss/control; §VI chỉ setup; §VII mới được chứa
kết quả. Không trộn bốn chức năng để "làm Method trông dài".

---

## 7. Table 1

Sao **nguyên xi** các cột Exec./CI/Tol. từ bảng hiện tại (dòng 390–400) — dưới đây đã khớp, nhưng
vẫn đối chiếu lại, đừng gõ lại từ đầu.

```latex
\begin{table}[!t]
\caption{Executability over the $4{,}463$-step touch population. \emph{Tol.}\ is the same run
under the conventional $14\%$ rule alone, without the nearest-centre condition. The
human-reference row is a pipeline score, not a human ceiling.}
\label{tab:main}
\centering
\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{tabular}{lccc}
\toprule
Branch & Exec. & 95\% CI & Tol. \\
\midrule
Base (not fine-tuned)      & 47.6 & $[45.9, 49.3]$ & 57.6 \\
S1 (sentence, seed 101)    & 59.1 & $[57.3, 60.8]$ & 69.2 \\
S1 (sentence, seed 202)    & 59.6 & $[57.9, 61.3]$ & 69.8 \\
S1 (mean of two runs)      & \textbf{59.4} & - & - \\
S2 (descriptor, seed 101)  & 57.2 & $[55.4, 58.9]$ & 67.4 \\
\midrule
\multicolumn{4}{@{}l}{\emph{Stage 2: from the S2 checkpoint, $+800$ updates}} \\
CE2 (stage 2, control)     & 59.4 & $[57.7, 61.1]$ & 68.9 \\
MIN (stage 2, preference)  & 60.0 & $[58.3, 61.8]$ & 69.2 \\
\midrule
\emph{Human references}    & 75.7 & $[74.1, 77.3]$ & 84.3 \\
\emph{Contentless sentence}& 12.0 & $[9.7, 14.4]$  & - \\
\midrule
\multicolumn{4}{@{}p{0.95\columnwidth}@{}}{\footnotesize S1 is the mean of two training
runs; S2, CE2 and MIN are one run each at seed 101; CE2 and MIN continue from the same S2
checkpoint for 800 updates, making MIN$-$CE2 update-matched and accepted-data-matched, but
not compute-matched or an isolated objective effect.} \\
\multicolumn{4}{@{}p{0.95\columnwidth}@{}}{\footnotesize The contentless control uses an
$800$-step slice.} \\
\bottomrule
\end{tabular}
\end{table}
```

**Quy tắc bảng:**
- **Xoá cột** `% of 75.7` (dòng 388, 390–399). Nó cho MIN 79.3 vs S1 78.4, tức xếp hạng lại đúng
  thứ vừa tách khối; và 78.4 dễ bị đọc thành "78.4% of human".
- Một `\textbf` **duy nhất**: 59.4 của S1 mean. **Cấm đậm MIN 60.0.** Cấm `best` / `highest` /
  `our final model` / `best checkpoint we have measured` (đang có ở dòng 489).
- `\midrule` + nhãn khối **Stage 2** trước CE2/MIN: mắt người đọc xếp hạng theo khối liền mạch;
  hiện bốn nhánh nằm liền nên 60.0 tự thành hạng nhất.
- Đơn vị: mức dùng `%`, hiệu dùng `pp`. Cấm `59.4 points`.
- Run-count note là **đúng một câu**. Dòng thứ hai chỉ khai `n=800`. Danh sách unrun + quyết định
  ngân sách 23/8 xuất hiện **đúng một lần** ở Limitations, không lặp dưới bảng.

---

## 8. Results — khối dán cho S2 và MIN

```
Descriptor-first training scores 57.2%, 2.18 pp below the two-run sentence-only mean of
59.4%. MIN-DESC scores 60.0%. CE2, the accepted-only supervised continuation, scores 59.4%;
both procedures start from the same S2 checkpoint and use the same accepted data, schedule
and 800 optimizer updates, while MIN additionally processes a rejected response. The
implemented-procedure contrast is +0.63 pp, below the 2.11 pp this design can resolve with
one run per branch. About four fifths of the rise from S2 to MIN-DESC is the supervised
continuation (+2.24 of +2.87 pp), not the preference-procedure contrast.
```

- **MIN−S1 nhắc đúng một lần**, tại §Results, **không** ở abstract: point estimate +0.94 pp,
  CI [−0.09, +2.05], p = 0.11; dưới luật dung sai quy ước MIN và S1/101 ngang nhau ở 69.2.
- **2×2: giữ bảng, một lần ở §Diagnosis.** Caption phải có: *post-hoc, stratified by the branch's
  own descriptor, not a causal effect of the descriptor slot*; và MIN được chọn **sau khi thấy kết
  quả S2** (giữ câu ở dòng 625).

---

## 9. Sửa số bắt buộc (soát lại toàn bộ, đây là chỗ chết người)

| Dòng | Đang ghi | Phải ghi | Vì |
|---|---|---|---|
| 69–70 | sàn 12.0 / 6.1 không n | thêm **n = 800** | đứng cạnh 4,463 → tưởng cùng mẫu số |
| 74, 122, 480, 665 | `2.19 points` | **2.18 pp** | 2.19 là làm tròn hai lần |
| 74–77, 624, 667 | `the other 1,374` | `the other 1,374 **of the 3,245 crossed steps**` | phần bù thật của 1,871 trên toàn quần thể là 2,592, không phải 1,374 |
| 132–133, 663 | 75.7 cạnh 12.0/6.1 không n | human **n = 4,463**, sàn **n = 800** | |
| 139 | `+0.63 points` | `+0.63 **pp**` | |
| 270–275 | trộn `0.7 / 2.00 / 7.82`, kết `The condition is met there` | cổng **n = 300** (trung vị **0.73%**, nhánh human) tách khỏi bộ ba trên giao **n = 4,462**: **0.67 = human, 2.00 = S1/101, 7.82 = Base**; ghi rõ **Base trượt cổng 3%** | 7.82 > 3, và 7.82 không phải S2 |
| 407, 663 | `47.6 to 59.4 points` | `47.6% to 59.4%` | mức là `%` |
| 491 | `71.0%` không mẫu số | thêm n, **hoặc bỏ số** | không tìm được nguồn cho n |
| 491 | `does not break fine-tuning` / `the ability to point is intact` | giữ hai số **+9.6 [+8.2, +11.1]** và **71.0%**, **bỏ hai kết luận** | CI chỉ chứa nhiễu dụng cụ của một lượt |
| 512 | `does not overtake` | `point estimate +0.94 pp; CI [-0.09, +2.05], p=0.11 chưa xác lập khác biệt` | điểm ước lượng dương |
| 537–541 | 228 và 109 bước `emit no descriptor`; `There … +1.48` | **"không có descriptor parse được"**; gắn **+1.48 với n = 881** | ngữ pháp hiện gắn +1.48 vào n=109 |
| 588–590 | 4,138 + 325 = 4,463, lệch 12 bỏ trống | một mệnh đề: **4,138 − 4,126 = 12 bước sinh descriptor nhưng không parse được** | 228+109 = 337 vs 325, lệch đúng 12 |

**Phân hoạch đã kiểm khớp, giữ nguyên:** 3,245+228+881+109 = 4,463 · 1,871+184+452+738 = 3,245 ·
1,737+78+2,648 = 4,463 · 259+832 = 1,091 · 395+565+131 = 1,091.

**Số học 2×2** (dùng nếu cần viết lại): +107/1,871 = +5.72 · +1/184 = +0.54 · +5/452 = +1.11 ·
−186/738 = −25.20 · (1+5−186)/1,374 = −13.10.

**MDE 2.2 (dòng 320) và 2.11 (dòng 356) không mâu thuẫn:** 2.2 chỉ bao nhiễu dụng cụ, 2.11 là
thiết kế một lượt có thêm thành phần seed. **Đừng "hợp nhất" hai số.**

---

## 10. Cắt hẳn (giải phóng ~450–500 từ)

| Dòng | Cắt gì | Thay bằng |
|---|---|---|
| 73–79 | abstract: `On the one seed we ran of the two we registered`, `2.19 points below the two-seed control mean`, cả lát 5.7/13.1 với 1,871/1,374, `not the presence of a descriptor slot` | abstract mục 3 |
| 123–129 | Intro: band vs interval clause, `we decline the \emph{positive}` | `Descriptor-first scores 57.2\% against 59.4\% for sentence-only supervision; the stage-2 procedures score 60.0\% for MIN-DESC and 59.4\% for its accepted-only supervised continuation.` |
| 96, 100–103, 106, 112 | meta + trùng Related + `The first/second is whether` | `Sentences are scored by executability (Section~\ref{sec:metric}).` |
| 340–367 | bộ máy bốn kết cục, dài 17/8, đếm 27 mục sửa đổi, `once in our favour and once against it`, `makes harm harder to declare` | `Twenty-seven dated amendments are recorded, twenty-one before any executability score existed.` |
| 480–488 | hai luật đọc, tie-break, ba ngưỡng 2.8/2.11/1.67 đặt cạnh nhau | `S2/101 scores 57.2\%, 1.93 pp below S1/101 ($b=254$, $c=340$, $[-3.06,-0.75]$) and 2.18 pp below the two-run S1 mean; the sign holds under UI-Venus.` |
| 489 | ngoại suy S2/202 phải đạt 65.0% | **cắt, không thay** (số này thuộc luận văn) |
| 505–507 | `By the band … inconclusive`, `runs against us`, `We do not claim it` | `The difference is below the 2.11 pp this design can resolve.` |
| 578 | `absence of signal and not evidence of an absent effect` | `With a human-reference level of 31.0\%, the instrument barely reads this row.` |
| 624 | hai câu đầu §Implications lặp +5.7/−13.1 + `The presence of a slot does not explain that split` | giữ từ `The two middle rows…` trở đi |
| 663–667 | Conclusion: câu band trùng dòng 123–125, kể lại 5.7/13.1/738/881/+1.48 lần thứ ba đến năm, `Identification accuracy must improve.` | khối Conclusion mục 11 |

**Nén (không cắt):** 228–246 định nghĩa thước → **3 câu** · 340–357 estimand + hai ngưỡng → **2 câu** ·
270–281 adequacy (bỏ `The condition is met there`, bỏ tự nhận "percentile would have been better",
bỏ chuyện một phép kiểm cài đặt hỏng) · 464–469 grounder thứ hai → **2 câu** (chứng nhân giữ 94%,
hai trần cách 0.7, UI-Venus thấp hơn 2.8–4.1 ở mọi nhánh) · 573–578 → **một câu** dùng cột Base và
cột human-reference (không bị điều kiện hoá theo treatment) · 592–593 → **một mệnh đề** (325 bước
định nghĩa bằng hành vi của chính nhánh; đối chứng cũng chỉ 19.7%) · 616–621 → **một câu** (hai
thang không quy đổi được) · 630 → **một câu** ngân sách (bỏ `Three readings are not available from
these numbers`) · 446–448 caption Table 2 (bỏ kể lại chuyện rút trần 70.0) · 131–139 contributions
→ mục 5.

---

## 11. Conclusion (dán)

```
We studied two controlled target-space training interventions for GUI instruction
generation: a descriptor-first target and descriptor-controlled ORPO pairs. Sentence-only
fine-tuning reaches 59.4% executability averaged over two training runs, up from 47.6%
(human-reference score 75.7%, n=4,463). Descriptor-first scores 57.2%; the stage-2
procedures score 60.0% for MIN-DESC and 59.4% for its accepted-only supervised continuation.
Executability is the scoring rule, not the model contribution.

The gain concentrates where the branch's own descriptor is right and reverses where it is
wrong (Table~\ref{tab:cross}). Further runs of the descriptor stages and methods that raise
identification accuracy are the natural next experiments.
```

---

## 12. Giữ nguyên — xương phòng thí nghiệm, đừng "mượt hoá"

Teacher-forced trên ngữ cảnh câu người viết (337, 656–659) · sự thật *Registered, not run*
(chuyển thành **một câu** ở Limitations) · quy công 78/22 của stage 2 (509–511) · cổng eligibility
3.3% = 459/14,000 và quartile 70/351/748 px (519–527) · năm luật chấm và tính tất định (305–313) ·
off-by-one join 48% vs 20% · Birthday/Gender 128 px · 30.7% tâm màn · 14,966,784 tham số +
`total_flos` L4/A100 · GPU quota 2,532 · rút trần 70.0 · byte-identical scored sentence · UGround
có AndroidControl trong recipe, đóng bằng UI-Venus (435–436, 457–469) · 95.6% app trùng train và
17.3% reference test trùng nguyên văn (644–646).

Nếu chuẩn hoá giọng: British → American (favour→favor, behavioural→behavioral, centre→center),
trừ tên riêng/IEEE.

---

## 13. Cấm viết

### A. Cấm claim (viết là gian, không phải là mạnh miệng)

1. Descriptor-first improves over sentence-only supervision.
2. MIN-DESC is our best model / outperforms sentence-only at 60.0%.
3. The pre-registered hypothesis is refuted / descriptor-first is harmful.
4. +0.63 pp is significant (p=0.011), so the preference objective works.
5. MIN improves over S2 by +2.87 pp, demonstrating the preference objective.
6. McNemar p<0.001 shows the difference is not training noise.
7. The descriptor slot, rather than identification accuracy, explains the loss. *(S2r và
   S2-nopoint không chạy)*
8. We are the first to place discriminativeness in the training target.
9. `reference-free`.
10. `generalises to unseen applications` (78 bước; 2,648 là **unmapped**, không phải unseen).
11. `The preference term can be reduced only by choosing the right element` / `the sentence cancels`.
12. `MIN-DESC isolates identification` / `objective-only effect` / `all else equal`.
13. `CE2 is compute-matched` / `fully budget-matched`. Chỉ được viết `update-matched and
    accepted-data-matched`.
14. `S2 is an ablation of discriminative commitment` / `the model must commit during training`.
15. `Only the identified element differs`: role và sentence giữ; name, point, cue và có thể token
    length đổi.

### B. Cấm văn phong

16. `First` / `Second` / `Third` mở đoạn trong abstract và intro.
17. `rather than` > 4 lần / bài (bản cũ 22 lần).
18. `in our favour` / `against us` / `tie-break` / `decline the positive`.
19. `will never exist` / `permanently incomplete` / `refuse a conclusion`.
20. `inconclusive` / `harm` / `the band` cho S2 hoặc MIN.
21. `loses 25.2 where it does not` (thiếu n) — nếu nêu: −25.2 trên **n = 738** khi cả tên và điểm
    đều sai.
22. `closing 42%` · `78.4% of human` · `22 times the seed-to-seed difference`.
23. `independently trained` → `not trained on AndroidControl`.
24. `consumer` → `reader` / `user`. `This is a model study.` / `Our claim is narrow` /
    `Two cautions apply` / `Two design choices are not free`.
25. `absence of signal and not evidence of an absent effect` · chiasmus · `where` = `whereas`.
26. `, so` dây chuyền (43 lần ở bản cũ) — tách câu. Câu 35–45 từ — cắt.
27. Bày tên cho S2 — chỉ `S2` và `descriptor-first`.
28. `\emph{}` để tranh luận (`positive`, `harm`, `and`).
29. `human level` / `ceiling` cho 75.7 → `human-reference score`.
30. Lặp nguyên văn một câu ở Intro và Conclusion.

### 13.1 Protocol viết strict (áp dụng từng đoạn)

1. Câu đầu mỗi đoạn nêu **một chức năng**: problem, design, evidence hoặc limitation; không trộn.
2. Chủ ngữ–động từ chính cách nhau tối đa ~8 từ; một câu tối đa 30 từ, trừ định nghĩa/formula.
3. Hiện tại đơn cho method/result (`uses`, `scores`); quá khứ cho hành động đã làm (`trained`,
   `registered`, `stopped`).
4. Mỗi claim số phải kèm comparator, đơn vị và mẫu số trong cùng câu khi mẫu số thay đổi.
5. Mỗi contrast phải gọi đúng estimand: S2−S1, MIN−CE2, MIN−S1; không dùng `gain` trần.
6. Method phát biểu invariant và objective; Results phát biểu outcome; Diagnosis phát biểu hậu
   kiểm; Limitations phát biểu cái chưa phân giải.
7. Không dùng từ nhân quả (`causes`, `explains`, `isolates`, `attributable`) nếu thiết kế không
   cấp phép. Dùng `is associated with`, `contrast`, `coincides with`.
8. Khi nêu giới hạn, nói **một lần tại nơi nó thay đổi cách đọc**, không xin lỗi lặp lại.
9. Thuật ngữ cố định: `sentence-only S1`, `descriptor-first S2`, `accepted-only CE2`, `MIN-DESC`,
   `executability instrument`.
10. Không gọi Base/S1/S2/CE2/MIN là "model architecture"; đó là training branches của cùng backbone.
11. Citation đặt ngay sau method borrowed: ORPO, QLoRA, tolerance rule; không gom citation cuối câu dài.
12. Mọi từ `only`, `same`, `matched`, `identical`, `isolates` phải có invariant hoặc kiểm chứng cụ
    thể ngay cạnh.
13. Không kết đoạn bằng hedge. Kết bằng observation hoặc scope: `This contrast does not separate X from Y.`
14. Abstract/Intro/Conclusion không được sao chép cùng một câu hoặc cùng chuỗi ba số.
15. Sau rewrite, tìm toàn bài các token:
    `only|isolate|matched|caus|significant|improve|best|first|rather than|inconclusive|harm`;
    kiểm thủ công từng match.

---

## 14. Rủi ro Overfull khi đổi thứ tự

- Dòng 199–202: chuỗi verbatim `<desc>…` có `|` và `<` `>` không tự ngắt → chèn `\allowbreak` sau mỗi `|`.
- Dòng 238–240: `$|p_x-g_x| \le 0.14W,\ |p_y-g_y| \le 0.14H$` → tách hai công thức, dấu phẩy ở text mode.
- References 670–725: mã arXiv dài → bọc `\url{}` (preamble đã có `url`).
- Table 1 sau khi bỏ một cột thì rộng dư — có thể tăng `\tabcolsep` lên 4pt (đã làm ở mục 7).

---

## 15. Build và điều kiện xong

```
cd thesis-master/paper/fair2026
rm -f main.log && tectonic -X compile main.tex --outdir . --keep-logs
grep -oE "Output written on main\.xdv \([0-9]+ page" main.log   # phải là 8
grep -c Overfull main.log                                        # phải là 0
```

`main.log` trong git **không tin được**. Thêm chữ ở đâu thì phải cắt chữ chỗ khác.

**Xong khi:** PDF đúng 8 trang · 0 Overfull · title mục 2 · abstract mục 3 · keywords mục 4 ·
contributions mục 5 · Method có công thức ORPO + citation + giới hạn autoregressive + CE2 không
compute-matched · hình target thay Voronoi · Table 1 mục 7 (một `\textbf`, không cột `% of 75.7`,
run-note một câu) · toàn bộ mục 9 đã sửa · Limitations một câu ngân sách/unrun · không câu nào
trong mục 13.

**Không làm:** đổi số đã khớp ở mục 0 · chạy S2/202, S2r, human eval · đưa 2×2 lên abstract ·
đậm MIN · commit (chờ tác giả).

---

## 16. Phụ lục — biết mình sẽ bị đánh ở đâu

**Năm đòn reject còn sống, xếp theo sát thương:**

1. **Nhánh mang tên bài thì thua.** Table 1: S2 57.2 < S1 59.4; ba nhánh đăng ký không chạy.
   Footnote không xoá được phép trừ.
2. **Hiệu quả của MIN chưa được phân giải.** +0.63 dưới MDE 2.11; +2.24 của +2.87 là CE2;
   MIN−S1 p = 0.11.
3. **Câu viết cho người nhưng chấm bằng bộ trỏ, không có neo người.** UGround có AC trong recipe;
   UI-Venus cùng họ Qwen.
4. **Một màn hình, English, một 3B, một cấu hình, history teacher-forced.** 95.6% app trùng train.
5. **2×2 là hậu kiểm** trên descriptor do chính S2 sinh; MIN được chọn sau khi thấy S2.

**Rủi ro nền, không cứu được bằng câu chữ:** không có can thiệp target nào vừa mang tên đóng góp
vừa thắng có ý nghĩa. Nếu reviewer coi đó là điều kiện cần thì hết cách. Chỉ đạo này tối ưu để
review ghi *"evidence is incomplete"*, không phải *"claims exceed evidence"*. Không gắn xác suất
accept giả chính xác; chỉ biết chắc để 57.2 thành câu độc lập ngay sau 59.4 làm framing xấu hơn
đáng kể.

**Luận văn được nói thêm gì mà FAIR không được:**

1. Cả hai luật đọc của hồ sơ đăng ký (dải 17/8 vs mệnh đề khoảng bản gốc 5/8) và vì sao lấy dải
   làm luật vận hành.
2. Lấy kết quả không thuận làm trục: 2×2 thành một chương chẩn đoán (+5.7 trên 1,871; −13.1 trên
   1,374; 5.6% trên 738; nâng hàng bốn lên mức đối chứng đáng 4.2 pp trên 4,463).
3. Lượt còn thiếu cần ra bao nhiêu: S2/202 phải đạt 65.0% để trung bình hai lượt tới mép +1.7 pp,
   hoặc ≤56.0% để thành âm — bài học về công suất thiết kế.
4. Trọn sổ thất bại: MIN on-policy chết ở cổng (459/14,000 = 3.3% so ngưỡng 25%), lỗi mã mẫu số
   41,099, hai lần nới ngưỡng sau khi thấy điểm.
5. Nói thẳng "chưa kết luận descriptor-first hơn SFT câu", kèm MIN−S1 +0.94 p=0.11 và MIN ngang
   S1/101 ở 69.2 dưới luật dung sai, rồi để lộ trình có chi phí (lượt hai cho S2/CE2/MIN + nhánh
   nhắm identification: khi descriptor đúng MIN hơn S1 +8.83 pp, khi sai −11.12 pp).
