# SOICT 2026 talk script (cập nhật 21/11: gọn hơn, nhấn đóng góp) and expected questions

**Paper:** *GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation*
Uyen Le Doan Phuong · Paper ID 5590 · Oral, SOICT 2026 · Springer CCIS.

**When and where:** **Saturday 5/12/2026, 10:00, room Salon B**, Session 6B *Applied AI, Big Data
Analytics, and Data-Driven Applications* (08:30–11:00, 10 talks, ours is the 7th). Be in the room by
08:20–08:25, tell the session chair you are there, copy the slides and test them.

**Slot:** 15 minutes **including Q&A**, talks back to back. The talk below runs about **9 minutes**,
leaving 5 to 6 minutes for questions. If you run late, skip slide 11 (one sentence is enough).

**Source of numbers:** `paper/soict2026/guistep/camera_ready_5590/Source/main.tex` (camera-ready).

## Flow of the talk

```
 1  Title
 2  Task: write the next step for a person          (one example)
 3  Three contributions                            (what the audience should remember)
 4  Every training signal comes from existing records (flow + declaration)
 5  Three versions of GUIStep, plus a control      (S / D / P / control)
 6  Word overlap cannot judge these sentences      (why a new score)
 7  Executability: a model follows the sentence, we check where it taps
 8  The score tells good from bad, across listeners (ceiling, floor, other listeners, rewording)
 9  Main results: +13.0, above a prompted 7B
10  Most of the gain comes from learning the sentence
11  The gain holds on sentences never seen in training
12  Conclusion + next steps
13  Thank you
```

**Tone:** speak about what the work achieves. Do not list weaknesses in the talk; the paper states them,
and the answers below (Group A, B) handle them if asked. Never contradict the paper: P is *not* claimed
to be significantly better than S.

**Why the talk looks like this (rà soát 21/11, nhìn từ phía người nghe hội nghị):**
- *Một ý cho mỗi slide, một câu kết cho cả bài:* "the human instruction already in the data is the strongest
  training signal, and a listener can check it". Mọi slide phục vụ ba đóng góp ở slide 3.
- *Mở đầu bằng nhu cầu thật* (trang trợ giúp, hướng dẫn sử dụng) chứ không bằng thuật ngữ.
- *Slide 9 có cột D thấp hơn S.* Lời nói chỉ nêu điều tích cực: thêm preference lên khai báo thì P đạt điểm
  cao nhất. Không tự nói "D thấp hơn"; bị hỏi thì trả lời thẳng theo câu B1/B2 (khai báo một mình −1,9, P bù lại).
- *Slide 10 không nói "P không hơn S"* (đúng nhưng tự hạ), cũng không nói "P hơn S" (sai với bài). Nói điều
  bài chứng minh được: hơn 90% mức tăng đến từ học câu, nhánh kiểm soát tách được đúng phần của preference.
- *Slide 8 có số*: khoảng cách S − backbone giữ 99% khi đổi người nghe (+11.14 → +11.02). Số thuyết phục hơn
  chữ "holds".
- *Điểm yếu không nằm trong bài nói* nhưng có sẵn slide dự phòng (B1, B4) và câu trả lời A3, B2, B5. Bị hỏi
  thì trả lời thẳng câu đầu, mở slide dự phòng.

**Góp ý phản biện → đã xử lý trong camera-ready → nói ở đâu khi trình bày.** Không nhắc chữ "reviewer"
trên sân khấu (người nghe không đọc phản biện); cứ trình bày phần đã bổ sung như một phần của bài.

| góp ý (reviewer) | đã làm trong bài | khi trình bày |
|---|---|---|
| Viết khó theo dõi, trộn khung chung với cài đặt AndroidControl (R1, R3) | Tách §3 *Framework* khỏi §5.1 *Setup*, thêm Hình 2 tổng quan, Bảng 1 định nghĩa S/D/P/control | Slide 4: dòng "none of it specific to AndroidControl"; cả bài một ý mỗi slide |
| Thước dựa vào mô hình học, cùng họ Qwen, đã thấy AndroidControl (R2, R3, R4) | Người nghe UI-Venus (giữ 99% khoảng cách) + Phi-4 khác họ; tiêu chí chặt Voronoi giữ thứ hạng | Slide 8 · câu A2 |
| Bộ bơm lỗi chấm bằng Voronoi, không phải D.3; "upper bound" thiếu căn cứ (R2) | Chạy lại dưới D.3 (đạt 6/10, Voronoi 8/10), bỏ chữ "upper bound" | Không nói; bị hỏi: câu A3 + slide B1 |
| Thiếu mốc ngoài: VLM khác, pipeline chọn đích rồi diễn đạt (R2, R4) | Thêm Qwen2.5-VL-7B prompting (57,7) và select-then-verbalise (62,4) | **Slide 9** (cả hai cột) · câu B4 |
| 17,3% câu trùng tập dạy, có học thuộc không (R2) | Tách câu lặp / chưa thấy: S − backbone +15,0 / **+8,4** | **Slide 11** · câu B6 |
| 11,14 vs 11,9 không khớp (R2) | Ghi rõ 11,14 là lát 2.532 bước, 11,9 là toàn 4.463 bước | Không nói; bị hỏi: hai tập chấm khác nhau |
| "1.443 mô tả sai phần tử" chưa kiểm tay (R2) | Đổi thành "không đạt kiểm tra định vị", nêu ba nguyên nhân | Câu B12 · slide B7 |
| McNemar không tính phụ thuộc trong app; cần lặp hạt giống (R2) | Bootstrap cụm theo app; S có hai hạt lệch 0,6 | **Slide 9** chú thích + lời nói · câu B5 |
| Độ trễ, prompt, luật chấm, mã (R2) | Phụ lục A (prompt, luật chấm); độ trễ khai chưa đo | Slide B9 · câu B11 |
| Tính mới hẹp, P không hơn S rõ (R2, R3) | Đóng góp thứ ba viết thành ablation có nhánh kiểm soát | **Slide 10** · câu B1 |
| Một dữ liệu, một backbone, chỉ bước chạm, lịch sử là câu chuẩn (R1, R4) | Limitations viết lại đủ bốn ý | Slide 12 dòng "Next" · câu A6, B9 |

**Speaking convention:** the first sentence of each slide links back, the last sentence leads to the next
(in italics). Keep these two even if you shorten the middle.

---

## Slide 1 · Title (~15 s)

**Say:**
Good morning. I'm Uyen, from the University of Science, VNU Ho Chi Minh City. I'll present GUIStep, a
compact vision-language model that writes step-by-step instructions for phone apps.
*Let me start with the task.*

*(ý chính: chào, giới thiệu tên bài.)*

---

## Slide 2 · Task: write the next step for a person (~50 s)

**On the slide:** GUI agents: instruction → action. GUIStep: screen + goal → instruction for a person.
Screenshot with "Sort by" circled; Goal / Generated / Reference.

**Say:**
*When you get stuck in a phone app, you need one sentence: what to touch next.* Help pages and user
guides are made of sentences like this, and today people write them by hand.

Most GUI research goes the other way. Agents such as SeeClick or OS-Atlas read an instruction and carry it
out on the screen. We do the reverse: from the screenshot, the user's goal and the previous steps, GUIStep
writes one instruction for a person.

Here the goal is to sort Aer Lingus flights by the cheapest direct one. There are five filter chips on
this screen. Our model writes "Click on the sort by option", the same chip as the human reference.

*We make three contributions.*

*(ý chính: bài toán ngược với agent; một ví dụ.)*

---

## Slide 3 · Three contributions (~35 s)

**On the slide:** 1 Method: a compact 3B model trained only from existing GUI records, no new labels ·
2 Evaluation: executability, a validated listener-based score · 3 Results: +13.0 over the backbone, above a
prompted 7B model.

**Say:**
*First, a method:* a compact 3B model trained only on what GUI datasets already record. We add no new
labels. *Second, an evaluation:* executability, a score that checks whether someone can follow the
sentence, and we validate it before using it. *Third, the results:* 13 points over the untuned model, and
better than a prompted model more than twice its size.

*Let's start with the method.*

*(ý chính: ba đóng góp, nói chắc.)*

---

## Slide 4 · GUIStep: every training signal comes from existing records (~35 s)

**On the slide:** flow recorded step → training targets → Qwen2.5-VL-3B + QLoRA; "no new labels · none of it
specific to AndroidControl"; declaration example with labels role · name · position · nearby text.

**Say:**
*All our training data comes from recorded demonstrations.* Each recorded step stores the human
instruction, the point that was touched, and the accessibility tree, which lists the elements on the
screen. We add no labels, and other GUI datasets record the same three things.

From the tree we build a short declaration of the target element: its role, its name, its position, and
a text next to it.

*With these targets we train three versions.*

*(ý chính: không cần nhãn mới; khai báo phần tử lấy từ cây giao diện.)*

---

## Slide 5 · Three versions of GUIStep, plus a control (~30 s)

**On the slide:** table S / D / P (learns to write · training); control box.

**Say:**
We fine-tune Qwen2.5-VL 3B with QLoRA. S writes the sentence directly. D writes the declaration first,
then the sentence. P refines D with preference pairs that we build automatically: the correct element
against a nearby one.

P gets extra training, so we also train a control with the same extra updates on correct examples only.
The gap between P and this control is what the preference objective itself adds.

*Now, how do we judge a generated sentence?*

*(ý chính: S, D, P và nhánh kiểm soát.)*

---

## Slide 6 · Word overlap cannot judge these sentences (~40 s)

**Say:**
*One button can be described correctly in many ways.* "Click on the search bar" and "Tap the magnifying
glass at the top" point to the same button, yet they share almost no words.

In a pilot, word overlap rejected 97.5% of correct rewordings. Sentence embeddings did worse than
chance at telling the same element from a different one.

*So we score a sentence the way a person would use it: by trying to follow it.*

*(ý chính: BLEU/embedding không chấm được.)*

---

## Slide 7 · Executability: a model follows the sentence, we check where it taps (~55 s)

**On the slide:** the flight screen from slide 2 with the tapped element circled · 1 the listener reads
screenshot + sentence · 2 it taps one point, never sees the answer · 3 three checks (right action · same
meaning · point inside the element the user tapped) · Executability = % of test steps that pass all three.

**Say:**
*The idea comes from referring expression generation: a description is good if a listener can find
the object.* Our listener is UGround, a frozen grounding model that plays the user. It gets the screenshot
and our sentence, never the answer, and taps one point.

Take the flight example again. The listener reads "Click on the sort by option" and taps. The step counts
as correct if three checks pass. The action must be right, a click and not a scroll. The sentence must not
flip the meaning, for example enable instead of disable. And the point must land inside the element the
user actually tapped. Executability is the share of test steps that pass all three.

*The listener is a learned model, so we validated it first.*

*(ý chính: một mô hình đóng vai người dùng đọc câu rồi bấm; bấm trúng phần tử người dùng đã bấm thì tính đúng.)*

---

## Slide 8 · The score tells good sentences from bad ones, across listeners (~50 s)

**Say:**
*The score separates good sentences from bad ones.* Human references score 83.8. "Tap the button",
which names nothing, scores 14, and a real sentence taken from another screen scores 9. Style alone earns
almost nothing; the listener needs the right content.

Our conclusions also hold beyond this one listener. With UI-Venus, which was never trained on
AndroidControl, the gain from fine-tuning keeps 99% of its size. Phi-4, from another model family, shows
the gain as well. A stricter localisation rule gives the same ranking of all systems, and rewriting a
reference with another verb or word order leaves the score unchanged.

*Now the results.*

*(ý chính: trần 83,8 vs sàn 14; đổi người nghe và đổi tiêu chí chặt vẫn giữ.)*

---

## Slide 9 · Main results (~45 s)

**Say:**
*Our best model, GUIStep-P, gains thirteen points over its starting model.* On 4,463 test steps the
untuned 3B model scores 53.6. A 7B model from the same family, prompted with the same input, reaches 57.7,
and a pipeline that first selects the target and then describes it reaches 62.4. Every fine-tuned GUIStep
model beats all three.

With preference training on top of the declaration, GUIStep-P reaches the best score, 66.5. The
confidence interval for its gain runs from 11.5 to 14.4.
The intervals account for steps from the same app. A second training run of S lands within 0.6 points,
far less than thirteen.

*Where does this gain come from?*

*(ý chính: +13 điểm, 3B tinh chỉnh vượt 7B prompting.)*

---

## Slide 10 · Most of the gain comes from learning the sentence (~55 s)

**On the slide:** step chart backbone 53.6 → GUIStep-S 65.5 (+11.9) → GUIStep-P 66.5;
two lines: sentence supervision brings most of the gain · preference adds +0.52 over a matched control
(p = 0.043).

**Say:**
*Most of it comes from learning the sentence.* GUIStep-S, trained on the sentence alone, already gets
almost twelve of the thirteen points, more than ninety percent. Thanks to the matched control, we can also
isolate what the preference objective adds on top: a significant +0.52 points.

So the human instruction already in the dataset is the strongest training signal, and future rewards
should act on that sentence.

*A natural question: does the model just copy sentences it has seen?*

*(ý chính: phần lớn mức tăng đến từ học câu; nhánh kiểm soát cho biết đúng phần đóng góp của preference.
Nếu bị hỏi D: khai báo đứng một mình làm giảm 1,9, P bù lại — câu B1/B2.)*

---

## Slide 11 · The gain holds on sentences never seen in training (~35 s) — *optional*

**Say:**
*About half of the test sentences also appear in training, because app instructions repeat a lot.*
On those, the gain over the untuned model is 15 points. On sentences never seen in training, the gain is
still 8.4 points, and copying a training sentence word for word cannot explain that.

*To conclude.*

*(ý chính: câu chưa thấy vẫn +8,4 ⇒ không phải học thuộc.)*

---

## Slide 12 · Conclusion (~40 s)

**Say:**
To sum up. The records already in GUI datasets are enough to train a compact 3B model that writes
next-step instructions for people. Executability scores these sentences by whether they can be followed,
and it holds with other listeners and a stricter rule. GUIStep gains 13 points over its backbone and beats
a prompted 7B model, and most of the gain comes from learning the sentence itself.

Next, we plan to add a second dataset, a human study, and rewards that act directly on the sentence.

Thank you. I'm happy to take questions.

---

## Slide 13 · Thank you

**On the slide:** "Thank you · Questions?" · 24C15039@student.hcmus.edu.vn

---
---

# EXPECTED QUESTIONS AND HOW TO ANSWER

General tips:
- Answer in the **first sentence** (yes / no / the number). Explain after.
- Lead with what the work shows, then state any limit as a plain fact and say what we did about it. No
  apologies, no "it's a weak point".
- If you don't know: "We haven't measured that." Don't guess.
- Speak slowly. Short sentences are fine. You can say "Good question, let me show the slide" and go to a backup slide.
- ⭐ = most likely to be asked.
- Each answer has a Vietnamese line *(VN)* so you remember the idea even if you forget the English.

## Group A. Evaluation metric

**A1 ⭐. Why not use BLEU, CIDEr or a VLM judge like GPT-4o?**
Because one button has many correct names, and BLEU-style metrics compare words with a single reference. In
our pilot, word overlap rejected 97.5% of valid rewordings, and embeddings were below chance. Zhao et al.
(EACL 2021) found the same for navigation instructions. We still report seven text metrics in Table 5 as a
complement. A VLM judge reads the sentence; our listener tries to use it, which is what a real user does.
And a VLM judge is also a learned model that would need the same validation we did.
*(VN: BLEU so chữ với một câu chuẩn; có báo kèm 7 độ đo; người nghe thì thật sự làm theo câu.)*

**A2 ⭐. Your listener, UGround, was trained on AndroidControl, and it's Qwen-based like your model. Isn't the score biased?**
We tested exactly that with two more listeners. UI-Venus-Ground-7B was never trained on AndroidControl: the
gap between S and the backbone is 11.14 under UGround and 11.02 under UI-Venus, on the same 2,532 steps, so
99% of it remains. Phi-4-multimodal comes from a different model family, and S is still 6.4 points above the
backbone, interval 5.1 to 7.7. These two listeners were run on S and the backbone.
*(VN: đã thử đúng điều đó: UI-Venus (không học AC) giữ 99%, Phi-4 (khác họ) vẫn +6,4; chạy cho S và backbone.)*

**A3 ⭐. Your score fails 4 of 10 validation criteria. Why should we trust it?**
Because it passes every criterion on what matters most: wrong action, wrong content, scroll direction and
paraphrase. The four criteria it misses are about telling apart elements right next to each other, 30 to 80
pixels apart, or inside one large box. We published all ten so readers can judge. That is also why we read
the results as comparisons between systems, and those comparisons keep the same ranking under the stricter
Voronoi rule.
*(VN: đạt mọi tiêu chí chính; bốn tiêu chí còn lại là phần tử sát bên; công bố đủ 10; thứ hạng giữ dưới Voronoi.)*

**A4. Why D.3 as the main rule and not Voronoi, which is stricter?**
D.3 is the original rule of the AndroidControl paper, and it gives the widest usable range: ceiling minus
the score of a generic sentence. That range is 68.9 for D.3, against 62.9 for Voronoi and 62.5 for the
tolerance window. We also report every system under Voronoi, and the ranking does not change.
*(VN: D.3 là tiêu chí gốc của AndroidControl, dải dùng được rộng nhất; Voronoi báo kèm, thứ hạng giữ.)*

**A5. Why does the human reference only reach 83.8, not 100?**
The listener makes some mistakes, and some human sentences are ambiguous on their own. So 83.8 is the
measured ceiling, and we read every result against it. Our best model is 17.3 points below that ceiling.
*(VN: trần 83,8 là giới hạn dụng cụ + câu người đôi khi mơ hồ.)*

**A6. Is executability only for touch actions? What about scroll or typing?**
Executability is scored on the 4,463 touch steps, because it needs a touch point. Scroll and other steps are
in training. The action check still applies, so a sentence that says "scroll" on a touch step fails.
*(VN: chấm bước chạm vì cần điểm chạm; bước khác có trong huấn luyện.)*

**A7. Did you do any human evaluation?**
Not with people yet; that is our next step. We validated the listener in four ways: ceiling and floor,
removing parts of the sentence, an injection suite, and two other listeners.
*(VN: chưa chấm bằng người, là bước tiếp theo; đã kiểm người nghe bằng bốn cách.)*

## Group B. Method and results

**B1 ⭐. The declaration and preference stages add little. So what is the contribution?**
Three things. First, the task itself: instructions for people, where most GUI work produces actions for
agents. Second, a training pipeline that needs no new labels. Third, a validated score based on following
the sentence. The ablation is a finding of its own: with a matched control we can say where the gain comes
from. Most of it comes from learning the sentence, and the preference objective adds a significant +0.52.
Without the control, the preference stage would get credit for all 2.9 points it gains over D. We do not
claim a new learning algorithm.
*(VN: đóng góp là bài toán + quy trình không cần nhãn mới + thước đã kiểm định; ablation có nhánh kiểm soát cũng là kết quả.)*

**B2 ⭐. Why does adding the declaration hurt?**
Our explanation: the model writes a structured line before the sentence, and if that line names the wrong
element, the sentence follows it. If the line is not closed, the sentence is empty and the step fails. In the
thesis we also saw that the declaration and the sentence are only loosely connected. That points to the next
step: put the reward on the sentence itself, which is what our follow-up work does.
*(VN: khai báo sai thì câu sai theo; khai báo và câu gắn lỏng; hướng tiếp là thưởng trực tiếp trên câu.)*

**B3. Why only 3B? Why not 7B or larger?**
Cost and use case. One training run of 8,072 updates takes about a day on one A100 with 4-bit QLoRA, and a
compact model fits on-device help. Size alone does not solve the task: our fine-tuned 3B is 7.8 points above
the prompted 7B. Fine-tuning a 7B is a natural next experiment.
*(VN: chi phí + chạy trên thiết bị; 3B tinh chỉnh hơn 7B prompting 7,8 điểm; tinh chỉnh 7B là thí nghiệm tiếp.)*

**B4. The 7B baseline is only prompted, with no prompt tuning. Is that fair?**
It gets exactly the same input as our backbone, so the comparison is controlled. There is no public system
trained for this task yet, so we also built a select-then-verbalise pipeline, which reaches 62.4. GUIStep is
above both. The main evidence is the controlled ablation inside GUIStep.
*(VN: cùng đầu vào nên so có kiểm soát; chưa có hệ công khai cho bài toán này; có thêm pipeline 62,4; GUIStep hơn cả hai.)*

**B5 ⭐. Single seed. How do you know the differences are real?**
For S we ran two seeds: they differ by 0.6 points, interval −0.2 to +1.4. The main gain, about 12 points over
the backbone, is twenty times larger than that. The differences among S, D, P and the control are one to two
points, and D, P and the control were trained once, so our conclusion rests on the large gain: most of it
comes from the sentence.
*(VN: S có 2 hạt lệch 0,6; mức tăng chính ~12 điểm lớn gấp 20 lần; kết luận dựa trên mức tăng lớn.)*

**B6. Isn't the model just memorising sentences, since half the references repeat?**
We measured it. On unseen sentences the gain over the backbone is 8.4 points, and copying a training
sentence word for word cannot produce that. On repeated sentences the gain is 15 points, so learning the
dataset's usual wording also helps.
*(VN: câu chưa thấy vẫn +8,4, học thuộc không giải thích được; câu lặp +15.)*

**B7. What about unseen apps?**
There are 78 test steps from 20 apps not in training. P scores 68.0 there and the backbone 56.4. With so few
steps the interval is wide, so we report it without drawing a conclusion.
*(VN: 78 bước, P 68,0 vs backbone 56,4; ít bước nên không kết luận.)*

**B8. Your test split is not the official AndroidControl test split. Why?**
We used the partition of the image release we built on. Our training and test tasks are disjoint, so our
model sees no test task. 90% of our test tasks fall in the official training split, which matters for the
listener, since it saw AndroidControl data. That is why we added UI-Venus, which never saw AndroidControl, and
the gain holds.
*(VN: theo cách chia của bản có ảnh; mô hình không rò rỉ; người nghe thì đã kiểm bằng UI-Venus.)*

**B9. Why use the human previous instructions as history and not the model's own?**
To score each step on its own, like teacher forcing. In real multi-step use, errors could accumulate. In the
thesis we also fed the model its own previous sentences: both models drop by about 4 points, and the gap
between our RL follow-up and S stays the same, +1.5.
*(VN: để chấm từng bước; luận văn chạy lịch sử tự sinh: cả hai giảm ~4 điểm, khoảng cách vẫn +1,5.)*

**B10. How are the preference pairs built? Are they checked?**
Automatically from the accessibility tree: the competitor is the nearest visible element with the same role,
80 to 350 pixels away, with a different name and point. That gives 22,854 pairs with no manual labelling.
*(VN: phần tử cùng vai trò gần nhất, cách 80–350 px; 22.854 cặp, tự động, không cần gán tay.)*

**B11. Inference latency? Can it run on a phone?**
We haven't measured latency yet. The model has 3B parameters and is trained with 4-bit quantisation, which
makes on-device use realistic; measuring it is on our list.
*(VN: chưa đo độ trễ; 3B + 4-bit nên khả thi.)*

**B12. Most errors are localisation. Is it the model or the listener?**
We haven't labelled the 1,438 failures by hand, so we can't split them yet. The candidates are a sentence that
names the wrong element, a listener error, or the box rebuilt from the tree. Widget Captioning reports element
naming as the hardest case, which is where we would look first.
*(VN: chưa gán nhãn tay nên chưa tách được; Widget Captioning cho thấy gọi tên phần tử là khó nhất.)*

## Group C. What's next (if asked about future work)

**C1. What have you done since the paper?**
*(Unpublished thesis work. Say it only if asked, and say it is ongoing.)*
In my thesis I put a reward directly on the sentence, with reinforcement learning (GRPO) and SPICE as the
reward, starting from GUIStep-S. On the same test set it improves over S by about 1.5 points under the D.3
rule (67.0 vs 65.5), and the gain stays significant under the stricter rule. A second seed also improves over S, by less, so we
are running more seeds.
*(VN: luận văn thử GRPO thưởng SPICE từ S, D.3 67,0 vs 65,5; đang chạy thêm hạt; chưa công bố, nói là đang làm.)*

**C2. Would this work in other languages, like Vietnamese?**
Yes, the pipeline only needs a screenshot, a touch point, a UI tree and a human instruction, so it is not tied
to English. What is missing is data: there is no Vietnamese dataset of recorded app use at this scale yet.
*(VN: quy trình không gắn tiếng Anh; chỉ thiếu dữ liệu tiếng Việt.)*

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
