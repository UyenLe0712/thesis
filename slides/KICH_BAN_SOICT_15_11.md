# SOICT 2026 talk script (15/11) and expected questions

**Paper:** *GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation*
Uyen Le Doan Phuong · Paper ID 5590 · Oral, SOICT 2026 (4–5/12/2026, HCMC) · Springer CCIS.

**Slot:** 15 minutes **including Q&A**. The script below runs about **10.5–11 minutes** at a calm pace,
which leaves 4 minutes for questions. If the chair says the slot is tight, skip slide 9
(repeated sentences) and say one line about it instead.

**Source of numbers:** `paper/soict2026/guistep/camera_ready_5590/Source/main.tex` (camera-ready).
The talk uses no number that is not in the paper. Two answers in the Q&A use thesis numbers that
are not published; they are marked.

**How to use this file:**
- *On the slide* is what goes on the slide (the slide agent follows it). Keep text short.
- *Say* is what you say. Do not memorise word for word. Know the idea and the bold numbers.
- Under each slide there is a short Vietnamese line *(ý chính)* to help you remember the point.

---

## Slide 1 · Title (~15 s)

**On the slide:** title · Uyen Le Doan Phuong · Faculty of Information Technology, University of
Science, VNU-HCM · SOICT 2026.

**Say:**
Good morning. My name is Uyen. I'm from the University of Science, VNU Ho Chi Minh City. My talk is about
GUIStep, a small vision-language model that writes step-by-step instructions for phone apps.

---

## Slide 2 · The task (~55 s)

**On the slide:** Figure 1 of the paper (`fig1_screen.png` with goal, previous steps, GUIStep box,
generated vs reference sentence). Top line: *Agents: sentence → action. GUIStep: screen + goal → sentence for a person.*

**Say:**
Imagine a user who gets stuck in the middle of a task on their phone. What they need is one sentence
that tells them what to touch next.

Most GUI research goes the other way. Agents like SeeClick or OS-Atlas read an instruction and output
a machine action, like click at 872, 141. Grounding models like UGround read a description and return
a point. We study the reverse direction: the input is the screenshot, the user's goal and the previous
steps, and the output is **one sentence written for a person**.

Here is an example. The goal is to find cheap direct flights on Aer Lingus. The model writes "Click on
the sort by option". The human reference says "Click on sort by option at the top left of the screen".
Notice there are five filter chips on this screen, so the sentence has to name the right one.

*(ý chính: bài toán ngược với agent; đầu ra là câu cho người đọc.)*

---

## Slide 3 · Why it is hard to evaluate (~50 s)

**On the slide:** two example sentences pointing to the same button:
"Click on the search bar" / "Tap the magnifying glass at the top"
Three small facts:
- word overlap rejects **97.5%** of valid rewordings (small pilot)
- embedding similarity: AUC **0.336**, below chance 0.5
- cosine: inbox / outbox **0.76** > search / magnifying glass **0.55**

**Say:**
The hard part is not only generation, it's evaluation. One button can be described in many correct
ways. "Click on the search bar" and "Tap the magnifying glass at the top" mean the same element, but they
share almost no words.

In a small pilot with rewordings we wrote ourselves, matching content words against the reference
rejected **97.5%** of them. Sentence embeddings were not better. They separate "same element, different
words" from "different element" with an AUC of **0.34**, which is worse than flipping a coin. The reason
is that embeddings reward a shared topic. "Inbox" and "outbox" look very similar to them, while "search"
and "magnifying glass", two names for one button, look less similar.

*(ý chính: BLEU/embedding không chấm được câu chỉ phần tử.)*

---

## Slide 4 · Our score: executability (~60 s)

**On the slide:** a simple flow: generated sentence + screenshot → **frozen listener** (UGround-V1-2B) → point.
Three checks in boxes: (i) action class matches · (ii) no polarity inversion (enable vs disable) · (iii) point inside the target box (AndroidControl App. D.3).
Bottom: *Executability = share of steps passing all three.*

**Say:**
So we borrow the criterion from referring expression generation: a description is good if a listener
can find the object. On phone screens, our listener is a frozen grounding model, UGround. It sees only
the screenshot and our sentence, never the answer, and it returns a point.

A step counts as correct when three things hold. First, the sentence names the right kind of action,
for example touch versus scroll. Second, it doesn't flip the meaning, like "enable" when the reference
says "disable". Third, the point lands inside the box of the element that was actually touched. This
third rule comes from Appendix D.3 of the AndroidControl paper.

**Executability** is the share of steps that pass all three. Because the listener is itself a learned
model, we don't trust it blindly. The next slide shows how we checked it.

*(ý chính: người nghe đóng băng đọc câu rồi trỏ; trúng hộp + đúng loại thao tác = đạt.)*

---

## Slide 5 · Checking the score (~65 s)

**On the slide:** small table (from Table 2 of the paper):
| sentence given to listener | D.3 |
|---|---|
| human reference (ceiling) | **83.0** |
| "Tap the button." | 14.1 |
| reference from a different screen | 8.6 |
| usable range | **68.9** |
Side box: *delete element name: −34.2 pts · delete position: −4.1 pts · 1,139 verb/word-order rewrites: −0.09*
Small line: *Injection suite: passes 6/10 under D.3 (8/10 under stricter Voronoi). Weak on neighbouring elements.*

**Say:**
We checked the score in several ways.

First, ceiling and floor. Human reference sentences score **83**. A sentence that names nothing, "Tap the
button", scores 14. A real sentence taken from a different screen scores only 9. So the listener really
reads the sentence, not just the style.

Second, what drives the score. If we delete the element name from reference sentences, we lose **34
points**. If we delete the position phrase, we lose 4. Rewriting the verb or the word order changes almost
nothing.

Third, an injection suite: we corrupt references on purpose, like a wrong action, a negation, or a
different element, and check if the score catches it. Under our main rule it passes six of ten criteria.
It is good at catching wrong actions and wrong content, but **weak at neighbouring elements** that are very
close to the target. I want to say this clearly: absolute numbers can be optimistic, so we rely mostly on
comparisons between systems.

*(ý chính: trần 83, sàn 14; bỏ tên mất 34 điểm; khai thẳng điểm yếu với phần tử sát bên.)*

---

## Slide 6 · The ranking holds with other listeners (~40 s)

**On the slide:** three rows:
- Stricter Voronoi rule: same ranking of all 5 systems
- UI-Venus-Ground-7B (not trained on AndroidControl): S − backbone **+11.14 → +11.02**
- Phi-4-multimodal (other model family, multiple choice): S − backbone **+6.4** [+5.1, +7.7]

**Say:**
A fair question is: what if the listener just likes our model? UGround has seen AndroidControl data, and
it's from the same Qwen family as our backbone.

So we changed the listener. With UI-Venus, which was not trained on AndroidControl, the gap between our
fine-tuned model and the backbone stays almost the same, 11.1 versus 11.0. With Phi-4, which is from a
different model family, we ask a multiple-choice question over numbered boxes, and the gain is still
**6.4 points**, clearly above zero. With the stricter Voronoi rule, the ranking of all five systems stays
the same.

*(ý chính: đổi người nghe, đổi tiêu chí, thứ hạng vẫn giữ.)*

---

## Slide 7 · GUIStep: supervision without new labels (~60 s)

**On the slide:** Figure 2 of the paper (pipeline). Table of 3 configurations:
| | training target | objective |
|---|---|---|
| GUIStep-S | sentence | cross-entropy |
| GUIStep-D | declaration, then sentence | cross-entropy |
| GUIStep-P | preferred vs rejected declaration, same sentence | ORPO |
| control | same as P, no rejected | cross-entropy |
Example declaration in mono: `<desc>item | Close | <point>274,285</point> | just below "3:09"</desc>`

**Say:**
Now the model. GUIStep builds all its training signal from what a recorded demonstration already has: the
human instruction, the touched point, and the accessibility tree. We collect no new labels.

We train Qwen2.5-VL **3B** with QLoRA, in three versions. **S** learns to write the sentence directly.
**D** first writes a short declaration of the target: its role, its name, its position and a relation to
nearby text, and then writes the sentence. The idea is to make the model commit to one element before
describing it. **P** refines D with preference pairs: the preferred side declares the right element, the
rejected side declares a nearby competitor, and both end with exactly the same sentence. So the only
difference is which element is declared.

We also train a **control**: same data and same number of extra updates as P, but without the rejected
side. This tells us whether P's gain comes from the preference objective or simply from training longer.

*(ý chính: S chỉ học câu; D khai báo phần tử trước; P thêm cặp ưu tiên; nhánh kiểm soát cùng số bước.)*

---

## Slide 8 · Main results (~60 s)

**On the slide:** horizontal bar chart, executability (D.3), 4,463 touch steps:
- untuned 3B backbone 53.6
- Qwen2.5-VL-7B, prompted 57.7
- select-then-verbalise variant 62.4
- GUIStep-D 63.6
- GUIStep-S 65.5
- control 66.0
- **GUIStep-P 66.5**
- human reference 83.8 (different colour)
Callout: *P − backbone: +13.0 [+11.5, +14.4], p < 0.001*

**Say:**
Here are the main numbers on **4,463** held-out touch steps.

The untuned 3B model scores 53.6. A larger 7B model of the same family, just prompted, gets 57.7. All our
fine-tuned 3B models are well above both. The best, GUIStep-P, reaches **66.5**, which is **13 points**
over the backbone, and the confidence interval is far from zero.

We also compare with an older variant of ours that first picks the target from a list of candidates and
then describes it. It scores 62.4. Its main problem is that it says "none" too often, on more than a quarter
of the steps where the right candidate was in the list.

And there is still a gap of 17 points to human sentences, so the task is far from solved.

*(ý chính: 3B tinh chỉnh vượt 7B prompting; P hơn backbone 13 điểm; còn cách người 17 điểm.)*

---

## Slide 9 · Ablation: where the gain comes from (~65 s)

**On the slide:** three paired differences with CI bars:
- D − S: **−1.9** [−3.0, −0.7], p = 0.003
- P − S: +1.05 [−0.11, +2.20], p = 0.073 (not significant)
- P − control: +0.52 [+0.02, +1.00], p = 0.043
Bottom line: *Control recovers 2.4 of the 2.9 points P gains over D. Second seed of S: 66.1 (+0.6).*

**Say:**
This is the slide I think matters most, because it is not the result we hoped for.

Adding the declaration, D, actually **lowers** executability by 1.9 points compared with writing the
sentence alone. Preference refinement, P, recovers that loss, but P is **not significantly** better than S.

Against the control, the preference objective adds half a point, which is just significant. But the control
alone already recovers 2.4 of the 2.9 points. So most of the recovery comes from extra training steps, not
from the preference pairs.

Also, D, P and the control were each trained once. A second seed of S differs from the first by 0.6 points,
which is the same size as these differences. So our honest conclusion is: **most of the gain comes from
training on the sentence itself.** The declaration and preference stages add little on top.

*(ý chính: khai báo làm giảm 1,9; P không hơn S có ý nghĩa; phần lớn nhờ học thêm bước. Nói thẳng.)*

---

## Slide 10 · Repeated vs unseen sentences (~45 s) — *skip if short of time*

**On the slide:**
| | repeated (2,347) | unseen (2,116) |
|---|---|---|
| S − backbone | +15.0 | **+8.4** |
| P − S | +0.3 (p = 0.75) | +1.9 (p = 0.031) |
Note: *52.6% of test references equal a training sentence (after lower-casing).*

**Say:**
Training and test tasks are disjoint, but app instructions repeat a lot. **52.6%** of test references are
exactly a training sentence after lower-casing. So we split the test set.

Fine-tuning helps in both groups. The gain is bigger on repeated sentences, so part of it is learning the
dataset's usual wording. But on unseen sentences the gain is still **8.4 points**, and that cannot come from
copying. On unseen sentences P is ahead of S by 1.9 points. This split was done after seeing the results, so
we treat it as a hint, not a claim.

*(ý chính: một nửa câu lặp; câu chưa thấy vẫn +8,4; P hơn S chỉ ở câu chưa thấy, phân tích hậu kiểm.)*

---

## Slide 11 · Text metrics and errors (~40 s)

**On the slide:** short table (BLEU-4 / SPICE / ROUGE-L / BERTScore) for backbone, S, D, P, best per column bold.
Right side: *P fails on 1,493 steps: 96.3% fail localisation, 50 wrong action, 5 polarity.*
Two example errors in mono: "select minutes 00" vs ref "click on the OK option".

**Say:**
For completeness we also report the usual text metrics. All of them improve a lot over the backbone. But
they disagree with each other: S leads on BLEU-4, CIDEr and SPICE, P leads on METEOR, ROUGE-L, chrF and
BERTScore. None of them checks whether the sentence picks the right element, which is why we use them only as
a complement.

On errors: when P fails, 96% of the time it is the localisation check. Only 50 cases are the wrong action.
We did not label these failures by hand, so a failure can come from the sentence, the listener, or the box.

*(ý chính: độ đo văn bản đều tăng nhưng mâu thuẫn thứ hạng; 96% lỗi là ở định vị.)*

---

## Slide 12 · Limitations (~40 s)

**On the slide:** four short bullets:
- Score not validated against human judgement; fails 4/10 injection criteria (neighbouring elements)
- One dataset (AndroidControl, English), one backbone, touch steps only
- D, P, control: one seed each
- 90% of test tasks are in AndroidControl's official training split; history = reference instructions

**Say:**
Let me be clear about the limits.

The score uses a model as a stand-in for a person, and we have not compared it with human judgement. It's
weak on neighbouring elements. We used one dataset, one backbone, and only touch steps. Three of our models
were trained with one seed. Our test split is not the official one, and 90% of its tasks belong to the
official training split. And the model always sees the human's previous instructions, not its own, so errors
cannot pile up across a task.

*(ý chính: khai đủ bốn giới hạn, nói nhanh, không xin lỗi.)*

---

## Slide 13 · Conclusion (~35 s)

**On the slide:** three lines:
- Records already in a GUI dataset are enough to train a compact instruction writer: **+13.0** points over the backbone
- A frozen listener can score such sentences without listing valid wordings (with known gaps)
- Most of the gain comes from learning the sentence; declaration + preference add little
Small: *Next: a second dataset, human evaluation, rewards that act on the sentence itself.*

**Say:**
To conclude. The records already inside a GUI dataset are enough to train a small 3B model that writes
next-step instructions for people, with a gain of 13 points over the untuned model and better than a
prompted 7B. A frozen listener can score these sentences without a list of valid wordings, although it still
has gaps on neighbouring elements. And most of the gain comes from learning the sentence; the extra
declaration and preference stages add little. One reason may be that our preference signal acts on the
declaration, not on the sentence. That is where we are going next.

Thank you. I'm happy to take questions.

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
3. Listener checks in detail: UI-Venus 2,532 steps, Phi-4 SoM (median 15 boxes, 95.7% coverage, ceiling 54.9, S 44.6, backbone 38.2). For A2.
4. Full text-metric table (Table 5: 7 metrics). For A1.
5. Training details: rank 8, scale 16, 4-bit NF4, 2 epochs = 8,072 updates, lr 1e-4; ORPO β = 0.1, 800 updates, lr 2e-5. For B3.
6. Prompt (Appendix A, English translation). If asked about the input.
7. Repeated / unseen table in full (Table 4). For B6.
