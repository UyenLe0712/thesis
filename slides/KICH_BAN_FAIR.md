# Kịch bản trình bày hội nghị FAIR'2026 (bài nói tiếng Anh)

Sinh tự động từ `slides/build/build_fair.js`. Sửa lời dẫn trong script rồi chạy lại
`node build_fair.js && python3 make_kichban_fair.py`, đừng sửa tay file này.

---

## Slide 1 · FAIR'2026  ·  Fundamental and Applied IT Research  ·  Natural Language Processing  —  ~25s  (cộng dồn 0:25)

Good morning. I am Le Doan Phuong Uyen, from the University of Science, VNU-HCM. This is joint work with Dr. Nguyen Hong Buu Long. The paper asks what descriptor-first supervision is worth for GUI instruction generation, and it reports a pre-registered ablation that we could not complete, together with the condition that governs when the component pays.

## Slide 2 · A different consumer of the same input  —  ~45s  (cộng dồn 1:10)

Start from the input a GUI agent takes: a screenshot and a user goal. An agent turns that into a coordinate, so that a machine can click. We keep the input and change the consumer. The output is one sentence, addressed to a person who has to be told which element to touch. That is the setting of accessibility and user-support tools. The change of consumer is not cosmetic. A coordinate can be compared to a recorded coordinate. A sentence cannot be compared to a single reference, because many wordings identify the same button and no dataset enumerates them.

## Slide 3 · A model paper needs an instrument first  —  ~40s  (cộng dồn 1:50)

So this is a model paper that needs an instrument first. We use executability. The generated sentence, with any descriptor removed, goes to a separate grounding model that never sees the gold coordinate. The step counts as correct when that model lands in the cell of the element the user actually touched and the action class agrees. The rubric is a recorded human touch, not a model's opinion, so this is not LLM-as-judge. The grounder only contributes a localisation; geometry against the gold point decides, and the same grounder scores every branch.

## Slide 4 · Four contributions, and the honest status of each  —  ~40s  (cộng dồn 2:30)

Four contributions. An instrument calibrated at both ends, with a measured ceiling and, less usually, a measured floor. A supervision pipeline that adds no annotation of its own, whose gain is measured at two seeds and replicated under a second grounder. A pre-registered ablation reported against its own reading rules, including the case where those rules refuse a conclusion. And a diagnosis of the condition under which the component pays. I will be explicit about the status of each: two are complete, one is permanently incomplete, and the last is exploratory.

## Slide 5 · Executability: three conditions, read from the implementation  —  ~55s  (cộng dồn 3:25)

The metric in one slide. Three conditions must hold together. The canonicalised action types agree. Polarity: the two sentences must not name opposite states of the same control. And localisation: the returned point is inside the conventional fourteen per cent tolerance, and no competing element centre is closer to it than the gold point itself. Two details are easy to get wrong, so I read them from the implementation. The tolerance region is a per-axis rectangle, not a disc: a hundred fifty-one pixels horizontally against three hundred thirty-six vertically. And the seed that generates the cell is the recorded touch point, not the centre of the element box. The figure is a real step where the two rules disagree.

## Slide 6 · Calibrated at both ends before any model claim  —  ~65s  (cộng dồn 4:30)

The instrument is calibrated at both ends before any model claim. Human references reach seventy-five point seven, so every score in the paper is read against that and not against a hundred. A contentless sentence, tap the button everywhere, scores twelve. A genuine reference written for a different screen, right register, matched length, wrong content, scores six point one, below the contentless floor on disjoint intervals. That control matters most: a wrong sentence actively misleads the instrument where an empty one leaves it to a weak prior, and it disposes of the objection that the metric rewards annotator style, because style is exactly what it preserves. The cell condition was chosen from what it refuses: displace the answer to the nearest competing element and the tolerance rule still awards credit in eighty-four per cent of cases, the cell rule in under three.

## Slide 7 · What the instrument weighs, and what it ignores  —  ~50s  (cộng dồn 5:20)

What does the metric weigh? Keep the locative clause and replace the element name with the generic the item: minus twenty-eight point five points. Delete the locative clause and keep the name, on a near-identical population: minus three point five. Naming the element is worth roughly eight times saying where it is, which is what the title of this line of work should be about. In the other direction, meaning-preserving rewrites, verb substitution and fronting the locative clause, move the score by a third of a point with an interval containing zero. So the instrument is insensitive to phrasing and sensitive to content.

## Slide 8 · Supervision assembled without new annotation  —  ~60s  (cộng dồn 6:20)

Supervision. We collect no new annotation and we do not label with another language model. The scored target is the per-step instruction the dataset already records, and the descriptor slots are derived by rule. Two public mirrors are joined on episode and step; because an off-by-one join would corrupt every label while leaving the pipeline functional, we test it: OCR text at the gold point appears in the reference on forty-eight per cent of sampled steps against twenty per cent under a deliberately shifted control. Four branches differ only in the generation target. The one invariant that matters here is that the scored sentence is byte-identical across branches on all sixty-four thousand examples, so a difference between branches is a difference in what precedes the sentence and nothing else.

## Slide 9 · The design was sealed before the first training run  —  ~60s  (cộng dồn 7:20)

The design was committed to version control before the first training run, and it fixes the reading of all four outcomes in advance, including the inconclusive one. The registered quantity averages two seeds per branch. The minimum detectable paired effect from instrument noise alone is two point two points, and a contrast across two training runs also carries the seed term. Twenty-seven amendments are recorded with dates, twenty-one of them before any executability score existed. And the sentence I would rather not have to say: the second seed of the treatment branch was never run, a budget decision, and it will not be. The registered estimand is permanently incomplete, and nothing later in the talk upgrades a single-seed comparison into the conclusion the two-seed rule would have licensed.

## Slide 10 · Executability on the 4,463-step touch population  —  ~35s  (cộng dồn 7:55)

Here is the full table. Read the column against seventy-five point seven at the top and twelve at the bottom. The untuned model is at forty-seven point six. Plain sentence supervision is at fifty-nine point four over two seeds. The descriptor branch is at fifty-seven point two at its single seed. The two stage-two branches, at one seed each, are at fifty-nine point four and sixty. Everything below the line has one seed and is labelled exploratory throughout the paper.

## Slide 11 · Q1  Automatic supervision works, and it replicates  —  ~65s  (cộng dồn 9:00)

The first question is whether supervision assembled this way works at all. It does. Forty-seven point six to fifty-nine point four, closing forty-two per cent of the distance to the human level, McNemar p below a thousandth at both seeds. The size to compare it against is retraining noise: rebuilding the same branch under a second seed moves the score by half a point, so the effect is about twenty-two times the noise. Three further readings. On the steps where the model does not reproduce the reference's content words, the gap is still eight point four points. There is no home advantage across seen, unseen and unattributable applications. And under a second grounder not trained on AndroidControl, the positive control retains ninety-four per cent of its size, so the explanation that fine-tuning merely teaches the annotator's register does not survive.

## Slide 12 · Q2  The descriptor branch: our own rules refuse a conclusion  —  ~65s  (cộng dồn 10:05)

The second question is whether naming the element before writing helps. Here the study cannot say. At the single seed available the treatment sits one point nine three points below its control, and against the two-seed control mean, minus two point one nine, inside the band declared inconclusive in advance. What the missing run could have changed is fixed by the same thresholds, and I would rather state it than let anyone infer a suppressed positive. To reach the weakly-positive edge it would have had to score sixty-five per cent, five points above the best checkpoint we ever measured. The remaining outcome space was inconclusive or negative. Two things do not depend on that seed: the branch is well above the untuned model, and it emits its coordinate slot accurately. Whatever the prefix costs, it does not cost the ability to point.

## Slide 13 · Where the prefix pays, and where it costs  —  ~70s  (cộng dồn 11:15)

This is the slide I would keep if I could keep only one. The branch emits its own descriptor, so its identification is scored against gold labels independently of the sentence. Cross name against coordinate. Where the model gets both right, the prefix is worth plus five point seven points and the branch exceeds the human level on those steps. Where it gets both wrong, on seven hundred thirty-eight steps, executability collapses to five point six. The cost of the design is commitment: having named the wrong element, the branch writes a sentence faithful to it, while the control, committed to nothing, still retrieves the right element on thirty per cent of them. The objection is that this conditions on a variable the treatment produces, so the failing row may just be the hard steps. The rightmost column is not conditioned on the treatment and answers it: the human references still reach sixty-six per cent there.

## Slide 14 · A third of the difference sits in 7.3% of the steps  —  ~55s  (cộng dồn 12:10)

A third of the total difference sits in the seven point three per cent of steps where the branch emits no descriptor at all, a slice registered on nineteen August, before any treatment score existed. There the model misjudges the action class: the reference says click the close icon and the branch writes swipe up. The references score sixty-eight per cent there, so the steps are solvable and the instrument is not blind. And the failure is not created by the descriptor: the untuned model names the correct action class on eighty-three per cent of them, against fifty-five for the control and thirty-nine for the treatment. Fine-tuning damages the action prior and the descriptor target amplifies it.

## Slide 15 · The objective this diagnosis specifies, and what it returned  —  ~65s  (cộng dồn 13:15)

The diagnosis points at identification accuracy rather than at the prefix, so we ran the objective registered for exactly that. Minimal pairs: accepted and rejected sides carry the same sentence verbatim and differ only in the descriptor, so the preference term can be reduced only by choosing the right element. It adds plus zero point six three points over a matched control, inside the inconclusive band again. The number I want on the slide is the attribution. The stage gains two point eight seven points in total, but seventy-eight per cent belongs to the control, which is eight hundred further supervised updates with no preference term anywhere. Reporting the whole stage as the effect of the objective would overstate it fourfold. One registered variant never trained at all, stopped by a feasibility check at three point three per cent usable pairs against a threshold of twenty-five.

## Slide 16 · Conclusion  —  ~50s  (cộng dồn 14:05)

To close. On a scale calibrated at both ends, automatic supervision works and replicates. Whether the descriptor prefix adds anything is a question our own reading rules refuse to answer, and the run that would have answered it was never executed. But the mechanism is legible: the prefix is worth plus five point seven where identification succeeds and minus twenty-five where it fails, and the largest single locus of damage is an action-prior failure that fine-tuning introduces before any descriptor exists. So what descriptor-first supervision is worth is conditional on identification accuracy, and that is where the next experiment has to act. Thank you.

## Slide 17 · Thank you  —  ~0s  (cộng dồn 14:05)

[Q&A] Backup slides follow: alternative metrics, the second grounder, hit-rule robustness, the paraphrase checklist, the floor design, training cost, the status of all registered branches, the on-policy variant, the blind region, and three verbatim examples.

## Dự phòng 1 · Why not BLEU, ROUGE, or an embedding score

Open if asked: why not BLEU/ROUGE/BERTScore. Key point: a reference-based score charges the branches unequally for register, and it scores the references 100 by construction, so it cannot locate the headroom. We follow Zhao et al. and make every claim at system level.

## Dự phòng 2 · Re-scored with a second, independently trained grounder

Open if asked: is the result an artefact of the grounder. The positive control keeps 94% of its size under a grounder not trained on AndroidControl. Not closed: both grounders are Qwen-family, and there is no human anchor.

## Dự phòng 3 · Hit-rule sensitivity and determinism

Open if asked: did you pick the hit rule that flatters you. Five rules, the level moves 26 points, the ordering never does. Also the determinism check and the conditional kappa.

## Dự phòng 4 · Is the instrument brittle to phrasing?

Open if asked: is the metric brittle to phrasing. Meaning-preserving rewrites move it by a third of a point; deleting the locative clause does cost, so it is not inert. Declared scope: we probed phrasing, not the referring expression itself.

## Dự phòng 5 · How the floor was built, and what it rules out

Open if asked: how do you know the floor is real, or does the metric reward annotator style. The wrong-screen control preserves style exactly and scores below the contentless floor on disjoint intervals.

## Dự phòng 6 · Training configuration and cost

Open if asked: training details, compute, reproducibility. One config serves every branch with four keys changing; L4 and A100 agree to three digits.

## Dự phòng 7 · Status of every registered branch

Open if asked: what happened to the branches you registered. Say plainly which ones were cancelled and why, and that they are marked registered-but-not-run rather than dropped.

## Dự phòng 8 · The registered variant stopped by its feasibility check

Open if asked: why did you use heuristic negatives instead of the model's own errors. The on-policy source was stopped by a feasibility check fixed in advance, and the error-distance distribution explains why.

## Dự phòng 9 · Limitations, with the numbers attached

Open if asked: limitations, split composition, or gaming the metric. The 89.5 against 3.3 pair bounds the write-for-the-grounder objection rather than excluding it.

## Dự phòng 10 · One held-out step from each regime, verbatim

Open if asked: show me an actual failure. Read (b) aloud: the sentence is fluent, faithful to its own descriptor, and unusable.

---

**Tổng phần trình bày: 14 phút 05 giây** ở tốc độ 135 từ mỗi phút, chưa tính thời gian chuyển slide và dừng lại chỉ bảng. Trần của phiên là 15 phút.

Tám slide dự phòng nằm sau slide 17, không thuộc mạch chính. Lúc trình chiếu, gõ số slide rồi Enter để mở.
