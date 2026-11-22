# SOICT 2026 talk script (cập nhật 21/11: gọn hơn, nhấn đóng góp) and expected questions

**Paper:** *GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation*
Uyen Le Doan Phuong · Paper ID 5590 · Oral, SOICT 2026 · Springer CCIS.

**When and where:** **Saturday 5/12/2026, 10:00, room Salon B**, Session 6B *Applied AI, Big Data
Analytics, and Data-Driven Applications* (08:30–11:00, 10 talks, ours is the 7th). Be in the room by
08:20–08:25, tell the session chair you are there, copy the slides and test them.

**Slot:** 15 minutes **including Q&A**, talks back to back. The talk below runs about **9 minutes**,
leaving 5 to 6 minutes for questions. If you run late, skip slide 10 (one sentence is enough).

**Source of numbers:** `paper/soict2026/guistep/camera_ready_5590/Source/main.tex` (camera-ready).

## Flow of the talk

```
 1  Title
 2  Task: write the next step for a person          (one example)
 3  Three contributions                            (what the audience should remember)
 4  Method: training signal from existing records, S / D / P
 5  Word overlap cannot judge these sentences      (why a new score)
 6  Executability: a listener follows the sentence
 7  The score is validated                         (ceiling, floor, other listeners, stricter rule)
 8  Main results: +13.0, above a prompted 7B
 9  Most of the gain comes from learning the sentence
10  The gain holds on sentences never seen in training
11  Conclusion + next steps
12  Thank you
```

**Tone:** speak about what the work achieves. Do not list weaknesses in the talk; the paper states them,
and the answers below (Group A, B) handle them if asked. Never contradict the paper: P is *not* claimed
to be significantly better than S.

**Why the talk looks like this (rà soát 21/11, nhìn từ phía người nghe hội nghị):**
- *Một ý cho mỗi slide, một câu kết cho cả bài:* "the human instruction already in the data is the strongest
  training signal, and a listener can check it". Mọi slide phục vụ ba đóng góp ở slide 3.
- *Mở đầu bằng nhu cầu thật* (trang trợ giúp, hướng dẫn sử dụng) chứ không bằng thuật ngữ.
- *Slide 8 có cột D thấp hơn S, người nghe sẽ thấy.* Nói ngay một câu ("declaring first does not help on its
  own; preference brings it to the best score") rồi đi tiếp. Không né, không sa đà.
- *Slide 9 không nói "P không hơn S"* (đúng nhưng tự hạ), cũng không nói "P hơn S" (sai với bài). Nói điều
  bài chứng minh được: hơn 90% mức tăng đến từ học câu, nhánh kiểm soát tách được đúng phần của preference.
- *Slide 7 có số*: khoảng cách S − backbone giữ 99% khi đổi người nghe (+11.14 → +11.02). Số thuyết phục hơn
  chữ "holds".
- *Điểm yếu không nằm trong bài nói* nhưng có sẵn slide dự phòng (B1, B4) và câu trả lời A3, B2, B5. Bị hỏi
  thì trả lời thẳng câu đầu, mở slide dự phòng.

**Góp ý phản biện → đã xử lý trong camera-ready → nói ở đâu khi trình bày.** Không nhắc chữ "reviewer"
trên sân khấu (người nghe không đọc phản biện); cứ trình bày phần đã bổ sung như một phần của bài.

| góp ý (reviewer) | đã làm trong bài | khi trình bày |
|---|---|---|
| Viết khó theo dõi, trộn khung chung với cài đặt AndroidControl (R1, R3) | Tách §3 *Framework* khỏi §5.1 *Setup*, thêm Hình 2 tổng quan, Bảng 1 định nghĩa S/D/P/control | Slide 4: dòng "none of it specific to AndroidControl"; cả bài một ý mỗi slide |
| Thước dựa vào mô hình học, cùng họ Qwen, đã thấy AndroidControl (R2, R3, R4) | Người nghe UI-Venus (giữ 99% khoảng cách) + Phi-4 khác họ; tiêu chí chặt Voronoi giữ thứ hạng | Slide 7 · câu A2 |
| Bộ bơm lỗi chấm bằng Voronoi, không phải D.3; "upper bound" thiếu căn cứ (R2) | Chạy lại dưới D.3 (đạt 6/10, Voronoi 8/10), bỏ chữ "upper bound" | Không nói; bị hỏi: câu A3 + slide B1 |
| Thiếu mốc ngoài: VLM khác, pipeline chọn đích rồi diễn đạt (R2, R4) | Thêm Qwen2.5-VL-7B prompting (57,7) và select-then-verbalise (62,4) | **Slide 8** (cả hai cột) · câu B4 |
| 17,3% câu trùng tập dạy, có học thuộc không (R2) | Tách câu lặp / chưa thấy: S − backbone +15,0 / **+8,4** | **Slide 10** · câu B6 |
| 11,14 vs 11,9 không khớp (R2) | Ghi rõ 11,14 là lát 2.532 bước, 11,9 là toàn 4.463 bước | Không nói; bị hỏi: hai tập chấm khác nhau |
| "1.443 mô tả sai phần tử" chưa kiểm tay (R2) | Đổi thành "không đạt kiểm tra định vị", nêu ba nguyên nhân | Câu B12 · slide B7 |
| McNemar không tính phụ thuộc trong app; cần lặp hạt giống (R2) | Bootstrap cụm theo app; S có hai hạt lệch 0,6 | **Slide 8** chú thích + lời nói · câu B5 |
| Độ trễ, prompt, luật chấm, mã (R2) | Phụ lục A (prompt, luật chấm); độ trễ khai chưa đo | Slide B9 · câu B11 |
| Tính mới hẹp, P không hơn S rõ (R2, R3) | Đóng góp thứ ba viết thành ablation có nhánh kiểm soát | **Slide 9** · câu B1 |
| Một dữ liệu, một backbone, chỉ bước chạm, lịch sử là câu chuẩn (R1, R4) | Limitations viết lại đủ bốn ý | Slide 11 dòng "Next" · câu A6, B9 |

**Speaking convention:** the first sentence of each slide links back, the last sentence leads to the next
(in italics). Keep these two even if you shorten the middle.

---

## Slide 1 · Title (~15 s)

**Say:**
Good morning. My name is Uyen, from the University of Science, VNU Ho Chi Minh City. I will present
GUIStep, a small vision-language model that writes step-by-step instructions for phone apps.
*Let me start with the task.*

*(ý chính: chào, giới thiệu tên bài.)*

---

## Slide 2 · Task: write the next step for a person (~50 s)

**On the slide:** GUI agents: instruction → action. GUIStep: screen + goal → instruction for a person.
Screenshot with "Sort by" circled; Goal / Generated / Reference.

**Say:**
*A user stuck in the middle of a phone task needs one sentence: what to touch next.* Sentences like this
make up help pages and step-by-step user guides, and today people write them by hand.

Most GUI research goes the other way: agents such as SeeClick or OS-Atlas read an instruction and act for
the machine. We do the reverse. From the screenshot, the user's goal and the previous steps, GUIStep writes
**one instruction for a person**.

Here the goal is to sort Aer Lingus flights by the cheapest direct one. Our model writes "Click on the sort
by option", the same element as the human reference, among five filter chips on this screen.

*Our work makes three contributions.*

*(ý chính: bài toán ngược với agent; một ví dụ.)*

---

## Slide 3 · Three contributions (~35 s)

**On the slide:** 1 Method: a compact 3B model trained only from existing GUI records, no new labels ·
2 Evaluation: executability, a validated listener-based score · 3 Results: +13.0 over the backbone, above a
prompted 7B model.

**Say:**
*First, a method:* a compact 3B model trained only from what GUI datasets already record, with no new
annotation. *Second, an evaluation:* executability, a score that checks whether the sentence can actually be
followed, and we validate it. *Third, the results:* 13 points over the untuned model, and above a prompted
model more than twice its size.

*First, the method.*

*(ý chính: ba đóng góp, nói chắc.)*

---

## Slide 4 · GUIStep: training signal from existing records (~60 s)

**On the slide:** flow recorded step → training targets → Qwen2.5-VL-3B + QLoRA; table S / D / P;
declaration example with labels role · name · position · nearby text; control line.

**Say:**
*Every training signal comes from what a recorded demonstration already contains:* the human
instruction, the touched point, and the accessibility tree that lists the elements on screen. No new labels,
and none of these inputs is specific to AndroidControl, so the framework carries over to other recorded
GUI datasets.

We fine-tune Qwen2.5-VL **3B** with QLoRA in three versions. **S** writes the sentence directly. **D** first
declares the target element, its role, name, position and a nearby text, then writes the sentence. **P**
refines D with preference pairs built automatically: the correct element against a nearby competitor.

To measure what each stage adds, we also train a **control** with the same extra training as P,
using only the correct examples.

*Now, how do we judge a generated sentence?*

*(ý chính: không cần nhãn mới; S, D, P và nhánh kiểm soát.)*

---

## Slide 5 · Word overlap cannot judge these sentences (~40 s)

**Say:**
*The same button can be described in many correct ways.* "Click on the search bar" and "Tap the magnifying
glass at the top" name the same element but share almost no words.

In a pilot, word overlap rejected **97.5%** of valid rewordings, and sentence embeddings were worse than
chance at telling the same element from a different one.

*So we score a sentence the way a person uses it: by trying to follow it.*

*(ý chính: BLEU/embedding không chấm được.)*

---

## Slide 6 · Executability: a listener follows the sentence (~50 s)

**Say:**
*The idea comes from referring expression generation: a description is good if a listener can find the
object.* Our listener is a frozen grounding model, UGround. It sees only the screenshot and our sentence,
never the answer, and points to the screen.

A step counts as correct if the sentence names the right action, keeps the right meaning, and the point
lands inside the element that was actually touched, which is the original matching rule of AndroidControl.
Executability is the share of steps that pass all three.

*Because the listener is a learned model, we validated it first.*

*(ý chính: người nghe đóng băng đọc câu rồi trỏ.)*

---

## Slide 7 · The score is validated (~50 s)

**Say:**
*First, the score separates good sentences from bad ones.* Human references score **83.8**. A sentence
that names nothing, "Tap the button", scores 14, and a real sentence from another screen only 9. So the
listener reads the content, not the style.

Second, the conclusions do not depend on this one listener. UI-Venus was never trained on AndroidControl,
and with it the gain of fine-tuning keeps 99% of its size. Phi-4, from a different model family, also
confirms the gain. Under a stricter localisation rule, the ranking of all systems stays the same.

*With a validated score, here are the results.*

*(ý chính: trần 83,8 vs sàn 14; đổi người nghe và đổi tiêu chí chặt vẫn giữ.)*

---

## Slide 8 · Main results (~45 s)

**Say:**
*On 4,463 test steps,* the untuned 3B model scores 53.6. A 7B model of the same family, prompted with the
same input, reaches 57.7, and a pipeline that first selects the target and then verbalises it reaches 62.4.
Every fine-tuned GUIStep model is above all three. Declaring the target first does
not help on its own, but preference refinement brings it to the best score: GUIStep-P reaches **66.5,
thirteen points above the starting model**, with a confidence interval from 11.5 to 14.4. The intervals
account for steps from the same app, and a second training run of S lands within 0.6 points, so this gain
is far above the noise.

*Where does this gain come from?*

*(ý chính: +13 điểm, 3B tinh chỉnh vượt 7B prompting.)*

---

## Slide 9 · Most of the gain comes from learning the sentence (~55 s)

**On the slide:** step chart backbone 53.6 → GUIStep-S 65.5 (+11.9) → GUIStep-P 66.5;
two lines: sentence supervision brings most of the gain · preference adds +0.52 over a matched control
(p = 0.043).

**Say:**
*The ablation shows where the gain comes from.* Training on the sentence alone, GUIStep-S, already brings **almost
twelve of the thirteen points**, more than ninety percent. And because we trained a matched control, we can
say exactly what the preference objective itself adds on top: half a point, and it is significant.

So **the human instruction already in the dataset is the strongest training signal**, and future rewards
should act on that sentence.

*A natural question is whether the model just copies sentences it has seen.*

*(ý chính: phần lớn mức tăng đến từ học câu; nhánh kiểm soát cho biết đúng phần đóng góp của preference.
Nếu bị hỏi D: khai báo đứng một mình làm giảm 1,9, P bù lại — câu B1/B2.)*

---

## Slide 10 · The gain holds on sentences never seen in training (~35 s) — *optional*

**Say:**
*App instructions repeat a lot, so about half of the test sentences also appear in training.* There, the
gain over the untuned model is 15 points. On sentences **never seen in training** the gain is still
**8.4 points**, which copying cannot explain.

*To conclude.*

*(ý chính: câu chưa thấy vẫn +8,4 ⇒ không phải học thuộc.)*

---

## Slide 11 · Conclusion (~40 s)

**Say:**
To sum up. First, the records already in GUI datasets are enough to train a compact 3B model that writes
next-step instructions for people. Second, executability scores these sentences by whether they can be
followed, and it holds up under other listeners and a stricter rule. Third, GUIStep gains 13 points over its
backbone and beats a prompted 7B model, and most of the gain comes from learning the sentence itself.

Next, we will extend it to a second dataset, add a human study, and put rewards directly on the sentence.

Thank you. I'm happy to take questions.

---

## Slide 12 · Thank you

**On the slide:** "Thank you · Questions?" · 24C15039@student.hcmus.edu.vn

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

**B1 ⭐. The declaration and preference stages don't help much. So what is the contribution?**
Three things: a new task direction (instructions for people, not actions for agents), a training pipeline
that needs no new labels, and a validated execution-based score. The ablation is a result in itself: with a
matched control we can attribute the gain precisely. Most of it comes from learning the sentence, and the
preference objective adds a small but significant half point. Without the control, one would wrongly credit
the preference stage with all 2.9 points it gains over D. The novelty is not a new learning algorithm, and we
say so in the paper.
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
