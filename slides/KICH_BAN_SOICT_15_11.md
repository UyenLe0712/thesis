# SOICT 2026 talk script (15/11, reordered for a clear flow) and expected questions

**Paper:** *GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation*
Uyen Le Doan Phuong · Paper ID 5590 · Oral, SOICT 2026 (4–5/12/2026, HCMC) · Springer CCIS.

**Slot:** 15 minutes **including Q&A**. The talk below runs about **10 minutes**, leaving ~5 minutes for
questions. If time is short, skip slide 10 and say one sentence about it.

**Source of numbers:** `paper/soict2026/guistep/camera_ready_5590/Source/main.tex` (camera-ready).

## Flow of the talk (read before rehearsing)

Each slide answers the question left by the previous one:

```
1. TASK
  2  Write the next-step instruction for a person            (task, one example)
  3  Outline
2. METHOD
  4  GUIStep: training signal from existing records, 3 variants S / D / P
3. EVALUATION
  5  Word overlap cannot judge these sentences               (why a new score)
  6  Executability: a frozen listener tries to follow the sentence
  7  The score is checked: ceiling, floor, other listeners, known weakness
4. RESULTS
  8  Main results: +13.0 over the backbone, above a prompted 7B
  9  Ablation: most of the gain comes from learning the sentence
 10  Repeated vs unseen sentences  (optional)
5. CONCLUSION
 11  Limitations
 12  Conclusion (one line per part)
```

**On-slide conventions:** every content slide has a small progress bar at the top right:
*Task · Method · Evaluation · Results · Conclusion*, current part in bold. Slide text is short phrases,
3–5 lines plus a figure, table or chart, so the audience understands the slide on its own. Each big
number has a one-line caption saying what it measures, in plain words.

**Speaking convention:** the first sentence of each slide links back, the last sentence leads to the next
(in italics). Keep these two even if you shorten the middle.

---

## Slide 1 · Title (~15 s)

**On the slide:** GUIStep · A Compact Vision-Language Model for GUI Step Instruction Generation · Uyen Le
Doan Phuong · Faculty of Information Technology, University of Science, VNU-HCM · SOICT 2026.

**Say:**
Good morning. My name is Uyen, from the University of Science, VNU Ho Chi Minh City. My talk is about
GUIStep, a small vision-language model that writes step-by-step instructions for phone apps.
*Let me start with the task.*

*(ý chính: chào, giới thiệu tên bài.)*

---

## Slide 2 · Task: write the next step for a person (~55 s)

**Part:** Task
**On the slide:** one line at top: *GUI agents: instruction → action. GUIStep: screen + goal → instruction for a person.*
Left: the screenshot (`fig1_screen.png`), **large enough to read**, with the red circle on "Sort by".
Right, three short boxes stacked:
- **Goal:** find Aer Lingus flights, sort by cheapest direct flight
- **Generated:** "Click on the sort by option"
- **Reference:** "Click on sort by option at the top left of the screen"
Small caption: *5 filter chips on screen: the sentence must name the right one.*

**Say:**
*A user stuck in the middle of a phone task needs one sentence: what to touch next.*

Most GUI research goes the other way. Agents such as SeeClick or OS-Atlas read an instruction and output an
action for the machine. We do the reverse: the input is the screenshot, the user's goal and the previous
steps, and the output is **one sentence for a person**.

Here, the goal is to find Aer Lingus flights sorted by the cheapest direct one. Our model writes "Click on
the sort by option". The human reference says "Click on sort by option at the top left of the screen". There
are five filter chips here, so the sentence has to pick the right one.

*The talk has four parts.*

*(ý chính: bài toán ngược với agent; một ví dụ cụ thể.)*

---

## Slide 3 · Outline (~15 s)

**Part:** Task
**On the slide:** four numbered lines:
1. **Method:** GUIStep, training without new labels
2. **Evaluation:** scoring a sentence by whether it can be followed
3. **Results:** main comparison and ablation
4. **Conclusion:** limitations and next steps

**Say:**
First, how we train the model. Second, how we score the sentences, because standard metrics don't work
here. Third, the results. And finally the limitations. *Let me start with the method.*

*(ý chính: dàn ý bốn phần.)*

---

## Slide 4 · GUIStep: training signal from existing records (~65 s)

**Part:** Method
**On the slide:** top: one simple flow, large boxes:
`recorded step (screenshot · human instruction · touch point · UI tree)` → `training targets` → `Qwen2.5-VL-3B + QLoRA`
Below, a table of three variants with one-phrase descriptions:
| | learns to write | training |
|---|---|---|
| **S** | the sentence | cross-entropy |
| **D** | a declaration of the target, then the sentence | cross-entropy |
| **P** | D + preference: right vs wrong element declared | ORPO |
Example declaration, one line in mono: `<desc>item | Close | <point>274,285</point> | just below "3:09"</desc>`
Small: *+ a control with the same extra updates as P, without the wrong side.*

**Say:**
*GUIStep builds all its training signal from what a recorded demonstration already contains:* the human
instruction, the touched point, and the accessibility tree, which lists the elements on screen. No new labels.

We fine-tune Qwen2.5-VL **3B** with QLoRA, in three versions. **S** learns to write the sentence directly.
**D** first writes a short declaration of the target element, its role, name, position and a nearby text,
and then the sentence. The idea is to make the model commit to one element before describing it. **P**
refines D with preference pairs: the preferred side declares the right element, the rejected side a nearby
competitor, and both end with the same sentence.

We also train a **control** with the same extra updates as P but no rejected side, so we can tell whether a
gain comes from the preference objective or just from training longer.

*Now, how do we know if a generated sentence is good?*

*(ý chính: không cần nhãn mới; S, D, P và nhánh kiểm soát.)*

---

## Slide 5 · Word overlap cannot judge these sentences (~45 s)

**Part:** Evaluation
**On the slide:** two sentences pointing to one magnifying-glass button:
"Click on the search bar" · "Tap the magnifying glass at the top"
Two numbers with captions:
- **97.5%** · valid rewordings rejected by word overlap (small pilot)
- **0.34 AUC** · embedding similarity, below chance (0.5)

**Say:**
*The same button can be described in many correct ways.* "Click on the search bar" and "Tap the magnifying
glass at the top" mean the same element but share almost no words.

In a small pilot, word overlap rejected **97.5%** of valid rewordings. Sentence embeddings did no better: an
AUC of 0.34, worse than chance, because they reward a shared topic rather than the same element.

*So we score a sentence the way a person would use it: by trying to follow it.*

*(ý chính: BLEU/embedding không chấm được.)*

---

## Slide 6 · Executability: can a listener follow the sentence? (~55 s)

*(Title on slide without the question mark: "Executability: a listener follows the sentence")*

**Part:** Evaluation
**On the slide:** flow: `generated sentence + screenshot` → **frozen listener (UGround)** → `point on screen`
Three checks below, short:
(i) right action type · (ii) no opposite meaning (enable vs disable) · (iii) point inside the target element
Bottom bar: **Executability = % of steps passing all three**

**Say:**
*We borrow the idea from referring expression generation: a description is good if a listener can find the
object.* Our listener is a frozen grounding model, UGround. It sees only the screenshot and our sentence,
never the answer, and returns a point.

A step is correct if the sentence names the right type of action, does not flip the meaning, and the point
lands inside the element that was actually touched. This last rule comes from the AndroidControl paper itself.
Executability is the share of steps that pass all three.

*Since the listener is a learned model, we checked it before trusting it.*

*(ý chính: người nghe đóng băng đọc câu rồi trỏ.)*

---

## Slide 7 · The score is checked before use (~65 s)

**Part:** Evaluation
**On the slide:** left: a small bar chart, listener score for:
- human reference **83.8** (ceiling) · "Tap the button." **14.1** · reference from another screen **8.6**
Right: two short lines:
- Other listeners (UI-Venus, Phi-4): fine-tuning gain still holds
- Stricter localisation rule: same ranking
Bottom, orange box: **Known weakness: confuses neighbouring elements (30 to 80 px)**

**Say:**
*First, the ceiling and the floor.* Human sentences score **83.8**. A sentence that names nothing, "Tap the
button", scores 14. A real sentence from a different screen scores only 9. So the listener actually reads
the content.

Second, the listener might simply favour our model, since UGround saw AndroidControl and is from the same
Qwen family. So we repeated the main comparison with UI-Venus, not trained on AndroidControl, and Phi-4, from
another family. The gain from fine-tuning holds with both. A stricter localisation rule gives the same ranking.

And one weakness I want to state clearly: it often cannot tell apart two elements right next to each other.
So we rely mainly on comparisons between systems, not on absolute numbers.

*With that score, here are the results.*

*(ý chính: trần 83,8, sàn 14; đổi người nghe vẫn giữ; khai điểm yếu.)*

---

## Slide 8 · Main results (~55 s)

**Part:** Results
**On the slide:** horizontal bar chart, executability on 4,463 test steps:
untuned 3B 53.6 · prompted 7B 57.7 · GUIStep-D 63.6 · GUIStep-S 65.5 · control 66.0 · **GUIStep-P 66.5** · human 83.8 (different colour)
Callout: **+13.0** · GUIStep-P over the untuned 3B model

**Say:**
*On 4,463 test steps:* the untuned 3B model scores 53.6. A larger 7B model of the same family, just prompted,
gets 57.7. All our fine-tuned 3B models are well above both. The best, GUIStep-P, reaches **66.5**, which is
**13 points** above the starting model.

There is still a 17-point gap to human sentences, so the task is far from solved.

*But which part of GUIStep brings this gain?*

*(ý chính: 3B tinh chỉnh vượt 7B prompting; +13 điểm; còn cách người 17 điểm.)*

---

## Slide 9 · Most of the gain comes from learning the sentence (~65 s)

**Part:** Results
**On the slide:** three rows with a CI bar each:
- D vs S: **−1.9** (significant)
- P vs S: +1.05 (not significant)
- P vs control: +0.52 (small)
One line below: *Control already recovers 2.4 of P's 2.9 points over D.*

**Say:**
*This is the result we did not expect.* Adding the declaration, D, actually **lowers** the score by 1.9 points
compared with writing the sentence alone. Preference refinement, P, recovers that loss, but P is **not
significantly** better than S.

Against the control, the preference objective adds only half a point. The control alone recovers 2.4 of the
2.9 points, so most of the recovery comes from extra training, not from the preference pairs. And D, P and the
control were trained with one seed each.

So our honest conclusion: **most of the gain comes from training on the sentence itself.**

*One more question: is the model just copying sentences it has seen?*

*(ý chính: khai báo làm giảm; P không hơn S rõ; phần lớn nhờ học câu. Nói thẳng.)*

---

## Slide 10 · Gain holds on unseen sentences (~40 s) — *optional*

**Part:** Results
**On the slide:** two big numbers:
- **+15.0** · gain over the untuned model, sentences seen in training (52.6% of test)
- **+8.4** · gain on sentences never seen in training

**Say:**
*About half of the test sentences, 52.6%, also appear in the training data*, because app instructions repeat a
lot. The gain there is 15 points. On sentences never seen in training it is smaller, **8.4 points**, but still
clear, and it cannot come from copying.

*Let me finish with the limitations.*

*(ý chính: một nửa câu lặp; câu chưa thấy vẫn +8,4.)*

---

## Slide 11 · Limitations (~35 s)

**Part:** Conclusion
**On the slide:** three short lines:
- No human evaluation; weak on neighbouring elements
- One dataset, one backbone, touch steps only
- One seed for D, P and the control

**Say:**
*Three limitations.* We have not compared the score with human judgement, and it is weak on neighbouring
elements. We used one dataset, one backbone and touch steps only. And D, P and the control were trained once,
so their small differences may not hold with another seed.

*To conclude.*

*(ý chính: ba giới hạn, nói nhanh.)*

---

## Slide 12 · Conclusion (~35 s)

**Part:** Conclusion
**On the slide:** three labelled lines:
- **Method:** a 3B model trained only from existing records
- **Evaluation:** a checked, listener-based score
- **Results:** **+13.0** over the untuned model; most of it from learning the sentence
Small: *Next: a second dataset, human evaluation, rewards on the sentence itself.*

**Say:**
To sum up. The records already in a GUI dataset are enough to train a small 3B model that writes next-step
instructions for people. A frozen listener can score these sentences without a list of correct wordings,
with known gaps. The model gains 13 points over the untuned one, and most of it comes from learning the
sentence, not from the declaration or preference stages. That is why our next step is to put the reward on
the sentence itself.

Thank you. I'm happy to take questions.

---

## Slide 13 · Thank you

**On the slide:** "Thank you" · 24C15039@student.hcmus.edu.vn

---
---

# EXPECTED QUESTIONS AND HOW TO ANSWER

General tips:
- Answer in the **first sentence** (yes / no / the number). Explain after.
- If you don't know: "We haven't measured that." Don't guess.
- Speak slowly. Short sentences are fine. You can say "Good question, let me check the slide" and go to a backup slide.
- ⭐ = most likely to be asked.
- Each answer has a Vietnamese line *(VN)* so you remember the idea even if you forget the English.

## Group A. Evaluation metric

**A1 ⭐. Why not use BLEU, CIDEr or a VLM judge like GPT-4o?**
BLEU and similar metrics compare words with a single reference, and one button has many correct names. In
our pilot, word overlap rejected 97.5% of valid rewordings, and embeddings were below chance. Zhao et al.
(EACL 2021) found the same for navigation instructions. We still report seven text metrics in Table 5, as a
complement. A VLM judge is possible, but it is also a learned model that needs validation, and it would
judge the sentence by reading, not by acting. Our listener actually tries to use the sentence.
*(VN: BLEU so chữ với một câu chuẩn, sai bản chất; có báo kèm; VLM giám khảo cũng cần kiểm định.)*

**A2 ⭐. Your listener, UGround, was trained on AndroidControl, and it's Qwen-based like your model. Isn't the score biased?**
That's why we ran two more listeners. UI-Venus-Ground-7B was not trained on AndroidControl: the gap between
S and the backbone was 11.14 under UGround and 11.02 under UI-Venus on the same 2,532 steps. Phi-4-multimodal
is from a different family: S is still 6.4 points above the backbone, interval from 5.1 to 7.7. The
limitation is that we only ran these listeners on S and the backbone, not on P and the control.
*(VN: đã đổi sang UI-Venus (sạch AC) và Phi-4 (khác họ), chênh lệch vẫn giữ; nhưng chưa chạy cho P.)*

**A3 ⭐. Your score fails 4 of 10 validation criteria. Why should we trust it?**
We report it openly. It fails mainly on neighbouring elements, 30 to 80 pixels away, and on large boxes. It
passes the criteria about wrong action, wrong content, scroll direction and paraphrase. So it is reliable for
"did the sentence name the right kind of element in the right area", and weaker for "did it pick the exact
button next to it". That's why we rely on comparisons between systems, which hold under the stricter Voronoi
rule too, rather than on absolute levels.
*(VN: khai thẳng; yếu ở phần tử sát bên; đọc so sánh giữa hệ, thứ hạng giữ dưới tiêu chí chặt hơn.)*

**A4. Why D.3 as the main rule and not Voronoi, which is stricter?**
We chose by usable range: the ceiling minus the score of a generic sentence. D.3 has the widest range, 68.9,
versus 62.9 for Voronoi and 62.5 for the tolerance window. D.3 is also the original rule of the AndroidControl
paper. Voronoi is better at rejecting nearby elements, so we report every system under Voronoi too, and the
ranking does not change.
*(VN: chọn theo dải dùng được rộng nhất; D.3 là tiêu chí gốc của AndroidControl; Voronoi báo kèm.)*

**A5. Why does the human reference only reach 83.8, not 100?**
Two reasons: the listener makes mistakes, and some human sentences are ambiguous on their own. So we read
every result against 83.8 as the measured ceiling, not against 100. The gap between our best model and the
humans is 17.3 points.
*(VN: trần 83,8 là giới hạn dụng cụ + câu người đôi khi mơ hồ.)*

**A6. Is executability only for touch actions? What about scroll or typing?**
Yes, the scored population is the 4,463 touch steps, because the score needs a touch point. Scroll and other
steps are in training but not in this score. The action-class check does exist, so a sentence that says
"scroll" on a touch step fails.
*(VN: chỉ chấm bước chạm vì cần điểm chạm; bước khác có trong huấn luyện.)*

**A7. Did you do any human evaluation?**
No, and it's our first limitation. We validated the listener with ceiling and floor, ablations of the
sentence, an injection suite and two other listeners, but not against people.
*(VN: chưa; đây là giới hạn số một.)*

## Group B. Method and results

**B1 ⭐. The declaration and preference stages don't help. So what is the contribution?**
The contribution is the task setup, the supervision built from existing records without new labels, and a
validated score. The ablation is part of the contribution: with a matched control we show that most of the
gain comes from learning the sentence, and that the preference objective adds only about half a point.
Reporting this is useful, because without the control one would credit the preference stage with all 2.9
points. We say in the paper that the novelty is not a new learning algorithm.
*(VN: đóng góp là bài toán + giám sát không cần nhãn mới + thước đã kiểm định; ablation trung thực cũng là đóng góp.)*

**B2 ⭐. Why does adding the declaration hurt?**
We have a likely reason but haven't proven it. The model must write a structured line before the sentence,
and if the declaration names the wrong element, the sentence follows it. Also, if the declaration is not
closed, the sentence is empty and the step fails. In the thesis we saw that changing the declaration often
does not change the sentence at all, so the declaration and the sentence are only loosely connected. That is
why I said future work should put the reward on the sentence.
*(VN: khai báo sai thì câu sai theo; khai báo và câu gắn lỏng; hướng tiếp là thưởng trực tiếp trên câu.)*

**B3. Why only 3B? Why not 7B or larger?**
Two reasons: cost and use case. One training run of 8,072 updates already takes about a day on one A100 with
4-bit QLoRA. And a small model is more realistic for on-device help. The prompted 7B result shows that size
alone doesn't solve it: our fine-tuned 3B is 7.8 points above the prompted 7B. We did not fine-tune a 7B.
*(VN: chi phí + chạy trên thiết bị; 3B tinh chỉnh hơn 7B prompting 7,8 điểm; chưa tinh chỉnh 7B.)*

**B4. The 7B baseline is only prompted, with no prompt tuning. Is that fair?**
It's a weak baseline and we say so. We gave it exactly the same input as our backbone and did not tune the
prompt. There is no public system trained for this task, so we had no stronger external baseline. The main
comparison in the paper is the controlled ablation inside GUIStep.
*(VN: thừa nhận mốc yếu; chưa có hệ công khai nào cho đúng bài toán.)*

**B5 ⭐. Single seed. How do you know the differences are real?**
For S we ran two seeds: they differ by 0.6 points, interval from −0.2 to +1.4. S over the backbone, about 12
points, is far above that noise. But the differences between S, D, P and the control are around one to two
points, the same order as seed noise, and D, P and control were trained once. So we don't claim those small
differences are stable. That is exactly why our conclusion is "most of the gain comes from the sentence".
*(VN: S có 2 hạt lệch 0,6; chênh lệch lớn với backbone chắc; chênh lệch nhỏ giữa cấu hình chưa chắc.)*

**B6. Isn't the model just memorising sentences, since half the references repeat?**
Partly, yes, and we measured it. On repeated sentences the gain over the backbone is 15 points; on unseen
ones it's 8.4. The 8.4 points cannot come from copying a training sentence verbatim.
*(VN: có một phần học thuộc; câu chưa thấy vẫn +8,4.)*

**B7. What about unseen apps?**
Only 78 test steps come from 20 apps not in training. P scores 68.0 and the backbone 56.4 there, but the
interval is too wide to conclude anything.
*(VN: chỉ 78 bước, KTC quá rộng, không kết luận.)*

**B8. Your test split is not the official AndroidControl test split. Why?**
We used the partition of the image release we joined with. We found later that 90% of our test tasks are in
the official training split. Our training and test tasks are still disjoint, so it doesn't leak into our
model. The risk is for the listener, which saw AndroidControl training data. That's one more reason for the
UI-Venus and Phi-4 checks.
*(VN: dùng cách chia của bản có ảnh; mô hình mình không rò rỉ; rủi ro ở người nghe nên đã đổi người nghe.)*

**B9. Why use the human previous instructions as history and not the model's own?**
To isolate one step. It makes evaluation step-by-step, like teacher forcing. The cost is that errors cannot
accumulate, so real multi-step use may be harder. We list this as a limitation.
*(VN: để đánh giá từng bước độc lập; giá là lỗi không tích luỹ.)*

**B10. How are the preference pairs built? Are they checked?**
The competitor is the nearest visible element with the same role, 80 to 350 pixels away, with a different name
and point. That gives 22,854 pairs. They are built automatically from the accessibility tree and were not
checked by hand.
*(VN: phần tử cùng vai trò gần nhất, cách 80–350 px; 22.854 cặp; không kiểm tay.)*

**B11. Inference latency? Can it run on a phone?**
We didn't measure latency; it's in the limitations. The model is 3B and trained with 4-bit quantisation, so
on-device use is plausible, but we have no measurement to show.
*(VN: chưa đo độ trễ.)*

**B12. Most errors are localisation. Is it the model or the listener?**
We can't say for sure, because we didn't label the 1,438 failures by hand. It could be a sentence naming the
wrong element, a listener error, or an error in the box we rebuilt from the tree. Our guess is element naming,
which Widget Captioning also reports as the hardest case, but we haven't tested it.
*(VN: chưa gán nhãn tay nên không tách được; đoán là gọi tên phần tử.)*

## Group C. What's next (if asked about future work)

**C1. What have you done since the paper?**
*(Unpublished thesis work. Say it only if asked, and say it is ongoing.)*
In my thesis I tried putting a reward directly on the sentence, with reinforcement learning (GRPO) and SPICE
as the reward, starting from GUIStep-S. On the same test set it improves over S by about 1.5 points under
the D.3 rule (67.0 vs 65.5) and stays significant under the stricter rule. With a second seed the gain is
smaller, so it is still work in progress.
*(VN: luận văn thử GRPO thưởng SPICE từ S, D.3 67,0 vs 65,5; hạt 202 tăng ít hơn; chưa công bố, nói là đang làm.)*

**C2. Would this work in other languages, like Vietnamese?**
The pipeline only needs a screenshot, a touch point, a UI tree and a human instruction, so it is not tied to
English. The bottleneck is data: there is no Vietnamese dataset of recorded app use at this scale yet.
*(VN: quy trình không gắn tiếng Anh; thiếu dữ liệu tiếng Việt.)*

## If you don't understand the question

Say: *"Sorry, could you repeat the question?"* or *"Do you mean … ?"* and rephrase what you understood.
It's completely fine to do this once or twice.

---

## Backup slides to prepare (after the Thank-you slide)

1. Full validation table (Table 3 of the paper, 11 rows, D.3 and Voronoi). For A3.
2. Full rule-choice table (Table 2: D.3 / Voronoi / ±14% window). For A4.
3. Listener checks in detail: UI-Venus 2,532 steps (+11.14 → +11.02), Phi-4 SoM (median 15 boxes, 95.7% coverage, S 44.6, backbone 38.2, +6.4 [+5.1, +7.7]); Voronoi scores of the 5 systems. For A2.
4. Ablation with full CIs: D − S −1.9 [−3.0, −0.7] p = 0.003 · P − S +1.05 [−0.11, +2.20] p = 0.073 · P − control +0.52 [+0.02, +1.00] p = 0.043 · second seed of S 66.1 (+0.6 [−0.2, +1.4]). For B5.
5. Other baselines: select-then-verbalise variant 62.4 (abstains on 27.3%; differs in 3 settings) · prompted 7B 57.7 (+4.1 over 3B backbone, −7.8 vs S). For B4.
6. Full text-metric table (Table 5: 7 metrics). For A1.
7. Error analysis: P fails on 1,493 steps, 96.3% localisation, 50 wrong action, 5 polarity; two example errors. For B12.
8. Training details. For B3.
9. Prompt (Appendix A). If asked about the input.
10. Repeated / unseen table in full (Table 4). For B6.
