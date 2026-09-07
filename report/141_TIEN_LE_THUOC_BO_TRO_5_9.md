# 141 — Tra cứu 5/9/2026: trên thế giới có ai chấm câu hướng dẫn bằng một "bộ trỏ" như mình không, và ngoài cách đó còn thước nào

> Câu hỏi của chủ luận văn (5/9): *"tất cả các bài báo bây giờ, không có phần nào là làm như bài
> của tôi hay sao? Không có metric nào khác ngoài việc dùng một bộ trỏ bằng mô hình khác rồi
> dùng câu hướng dẫn của mình để trỏ lên hình ảnh?"*
>
> Tra bằng WebSearch/WebFetch, 20 lượt tìm + 20 lượt mở nguồn. Mức xác minh ghi ở cột cuối mỗi
> bảng: **[N]** đã mở đúng trang nguồn và đọc câu nguyên văn · **[A]** chỉ đọc abstract ·
> **[T]** chỉ có tóm tắt của máy tìm, chưa mở nguồn. ⛔ Mục **[T]** không được trích vào bài.

---

## 0. Trả lời ngắn

1. **Cách đo "đưa câu cho một mô hình khác, xem nó có trỏ đúng không" KHÔNG phải của riêng
   mình.** Đó là một họ thước có tên hẳn hoi trong văn liệu: *listener-based / comprehension-based
   evaluation* (dòng REG từ Mao 2016), *follower-based / task-based evaluation* (dòng VLN từ
   Fried 2018, Zhao 2021), và xa hơn là *extrinsic evaluation* (GREC 2009 dùng công cụ giải đồng
   tham chiếu chấm văn sinh). Luận văn đã trích đúng dòng này (ch5, FAIR §V), nên chỗ này không
   có rủi ro bị nói là "tự bịa thước".

2. **Trong miền GUI di động, sau hai vòng tra (17/8 và 5/9), vẫn chưa thấy bài nào chấm câu
   hướng dẫn *viết cho người* bằng cách cho bộ trỏ GUI đọc câu rồi trỏ lên ảnh.** Cái gần nhất
   là ba thứ dùng **cùng cơ chế nhưng khác mục đích**:
   · Jedi (2505.13227) dùng bộ trỏ UI-TARS-72B **lọc dữ liệu** huấn luyện: giữ mẫu mà toạ độ dự
     đoán khớp nhãn. Cùng phép "trỏ lại", nhưng để làm sạch dữ liệu, không để chấm hệ sinh câu.
   · Instruction Agent (2509.07098) cho **agent thực thi** hướng dẫn sinh ra rồi đo tỉ lệ hoàn
     thành tác vụ trên OSWorld. Cùng tinh thần "câu có dùng được không", nhưng đơn vị là cả tác vụ
     nhiều bước, và người đọc câu là agent chứ không phải người.
   · Jandial et al. (Findings EACL 2026) dùng bộ trỏ làm **mục tiêu tấn công**: sinh câu để bộ
     trỏ trượt. Ngược chiều với mình.
   ⇒ Câu được phép viết: *"trong phạm vi tra cứu của chúng tôi, chưa thấy công trình nào trong
   miền GUI dùng bộ trỏ độc lập làm thước cho câu hướng dẫn sinh ra"*. ⛔ **Không** viết "đầu
   tiên" hay "chưa ai làm" (luật đã có ở `CLAUDE.md`, mục Tiền lệ ⑥).

3. **Có nhiều thước khác**, và mỗi thước trả lời một câu hỏi khác. Bảng ở mục 2. Cái luận văn
   thiếu so với hai bài mạnh nhất cùng họ (Marky CVPR 2022, Zhao EACL 2021) là **neo người
   thật**: họ có người đi theo hướng dẫn, mình không. Đây là hạn chế đã khai, không lấp được bằng
   lập luận.

---

## 1. Họ thước "mô hình thứ hai đọc câu rồi hành động" — tiền lệ theo miền

### 1a. Referring expression generation (REG), ảnh tự nhiên

| bài | venue | cách chấm | liên hệ với mình | xác minh |
|---|---|---|---|---|
| Mao et al., *Generation and Comprehension of Unambiguous Object Descriptions* | CVPR 2016 | mô hình comprehension (và người) định vị vật thể từ câu sinh ra | gốc của họ thước; đã trích | [N] (tra 18/8) |
| Yu et al., *Joint Speaker-Listener-Reinforcer* | CVPR 2017 | listener chấm speaker; IoU>0,5 là đúng | cùng khuôn; đã trích | [T] |
| Luo & Shakhnarovich, *Comprehension-guided referring expressions* | CVPR 2017 | comprehension model là *"differentiable proxy of human evaluation"*; có cả người chấm | ⚠️ họ tự cảnh báo máy chấm có thể bị lợi dụng; con số 97,23 vs 66 mà `report/114` ghi **chưa mở được PDF** (403) | [A] |
| Cohn-Gordon, Goodman, Potts | NAACL 2018 short | *"an automatic method for testing the performance of pragmatic speaker models"* (listener trên dữ liệu tách riêng) | ý *"listener lúc chấm ≠ listener lúc sinh"* mà `114` ghi: **chưa xác minh chi tiết** | [A] |
| Dessì et al., *Communication breakdown* | EMNLP 2022 | neural retriever nhận caption người / caption máy rồi truy hồi ảnh | ⭐ máy chấm caption máy **cao hơn** caption người, còn người đọc caption máy gần ngẫu nhiên ⇒ đúng bẫy mà thước của mình **không** mắc (trần người 75,7 > mọi nhánh) | [A] |
| Multi-perspective referential communication (Tang et al.) | EMNLP 2024 | *communicative success*: listener chọn đúng vật; có cặp người–người làm mốc (87,6%) | cùng khuôn, có neo người | [A] |
| IREG, *Whether you can locate or not?* | preprint 2308.09977 | REG tương tác với một REC model thật, dùng tín hiệu "định vị được không" để sửa câu | cùng cơ chế, nhưng dùng làm **vòng lặp sinh**, không phải thước | [A] |
| Discourse-aware comprehension guiding | INLG 2024 | *text-image retrieval accuracy* + người | cùng khuôn | [A] |
| VIE-DM, *Generation and Comprehension Hand-in-Hand* | ICLR 2025 | sinh câu đa dạng để tăng cường dữ liệu REC | chỉ xác nhận có bài; **cách chấm chưa đọc được** (OpenReview chặn) | [T] |

### 1b. Vision-and-language navigation (VLN) — họ gần mình nhất về *mục đích* (câu viết cho người đi theo)

| bài | venue | cách chấm | liên hệ | xác minh |
|---|---|---|---|---|
| Zhao et al., *On the Evaluation of VLN Instructions* | EACL 2021 | người đi theo (wayfinding) làm chuẩn; BLEU/ROUGE/METEOR/CIDEr **không hiệu quả**; đề xuất mô hình tương thích học được; xếp hạng hệ thống thì khuyên SPICE | đã trích; là đòn nặng nhất cho khẳng định mức hệ thống | [N] (18/8) |
| Wang et al., *Less is More* (Marky) | CVPR 2022 | **người thật** đi theo: 71% thành công với câu máy so với 75% với câu người | ⭐ khuôn "hai số tuyệt đối cạnh nhau" mà ch5 đã áp; họ có neo người | [T] (abstract qua máy tìm) |
| Kamath et al., *A New Path* | CVPR 2023 | dùng Marky sinh 4,2M câu; abstract không nói chấm câu | chỉ là ứng dụng | [A] |
| InstruGen | preprint 2411.11394 | **không** BLEU/CIDEr; chấm gián tiếp bằng SR/SPL của agent huấn luyện trên câu sinh ra | "câu tốt = agent học từ nó tốt", khác "câu tốt = bộ đọc trỏ đúng" | [N] |
| FCA-R2R | preprint 2506.08566 | tương tự: lợi ích huấn luyện của SF/EnvDrop/RecBERT/HAMT | như trên | [A] |
| LaF-GRPO (Zhao, Wang, Li) | **AAAI 2026** | BLEU/ROUGE/METEOR/SPICE + **LLM giả lập người khiếm thị** diễn giải câu thành (hướng, khoảng cách, cảnh báo) rồi so với tham chiếu; người chấm 100 cặp | ⭐ gần nhất về triết lý: "câu đúng khi người đọc **hành động** đúng"; nhưng bộ đọc là LLM văn bản, không nhìn ảnh | [N] |
| GoViG | preprint 2508.09547 | chỉ BLEU-4/CIDEr/METEOR/ROUGE-L | đối chứng: bài 2025 vẫn dùng thước tham chiếu | [N] |

### 1c. Tiền lệ xa hơn, ngoài thị giác

| bài | venue | cách chấm | xác minh |
|---|---|---|---|
| GREC-MSR (Belz, Kow, Viethen, Gatt) | Generation Challenges 2009 | *extrinsic*: chạy các công cụ giải đồng tham chiếu lên văn bản sinh ra, đo MUC-6/CEAF/B³ của công cụ | [T] |
| Open Grounded Planning (Guo et al.) | ACL 2024 | "executability" = tra bảng ký hiệu, không mô hình | [N] (18/8) |

⇒ **Kết luận mục 1:** thước của mình là một thành viên của họ *listener/follower-based
evaluation*, với hai đặc điểm riêng: (i) bộ đọc là **mô hình định vị GUI có sẵn, không huấn
luyện lại** (họ REG thường tự train listener; Cohn-Gordon phải tách dữ liệu vì thế), và (ii)
**không có neo người**. Đặc điểm (i) là ưu thế (bộ đọc không nhìn thấy bộ sinh), đặc điểm (ii)
là hạn chế đã khai.

---

## 2. Các thước KHÁC đang được dùng, và mỗi thước trả lời câu gì

| họ thước | ví dụ (venue) | trả lời câu hỏi | có ở luận văn? |
|---|---|---|---|
| **A. Tham chiếu n-gram** (BLEU/CIDEr/METEOR/SPICE) | Widget Captioning EMNLP 2020 · GoViG 2025 · LaF-GRPO AAAI 2026 | câu có *giống* câu người không | có, ở vai phụ; Zhao 2021 đã cho thấy nó không đo được tính hướng dẫn |
| **B. Người thật làm theo** | Marky CVPR 2022 (71/75) · Zhao EACL 2021 (wayfinding) · AskEase CHI 2026 (user study 12 người) | câu có *dùng được* với người không | **không** (đã quyết không chấm người) |
| **C. Mô hình đọc rồi hành động** (listener / follower / bộ trỏ) | Mao 2016 · Yu 2017 · Dessì 2022 · Tang EMNLP 2024 · **luận văn** | câu có đủ thông tin để một bộ đọc độc lập *tìm ra* đích không | **thước chính** |
| **D. Agent thực thi cả tác vụ** | Instruction Agent 2025 (60% trên 20 tác vụ OSWorld) · AgentTrek ICLR 2025 (VLM replay + VLM evaluator) | chuỗi hướng dẫn có *hoàn thành* tác vụ không | không; đơn vị của mình là một bước |
| **E. LLM/VLM làm giám khảo** | OS-Genesis ACL 2025 (TRM GPT-4o chấm 1–5) · AutoGUI ACL 2025 (hai LLM verifier, nhất quán 94,5%) · UI-Ins 2025 (GPT-4.1 xác nhận câu chỉ trỏ tới đúng một phần tử) · FLEUR | câu có *hợp lý* theo một mô hình ngôn ngữ không | không; và là thứ Jandial 2026 cảnh báo (mô hình tự khai không đáng tin) |
| **F. LLM giả lập người dùng** | LaF-GRPO AAAI 2026 | người đọc sẽ *hành động* thế nào | không; gần C nhưng bộ đọc không nhìn ảnh |
| **G. Mô hình tương thích học được** | Zhao EACL 2021 (instruction–trajectory compatibility) | câu có *khớp* đường đi không | không |
| **H. Lợi ích huấn luyện hạ nguồn** | InstruGen · FCA-R2R · UI-E2I-Synth Findings ACL 2025 · UI-Ins | dữ liệu sinh ra có *dạy* được mô hình khác không | không; đo dữ liệu, không đo câu |
| **I. Lọc bằng bộ trỏ (round-trip)** | Jedi 2505.13227 §2.2.5: *"we use UI-TARS-72B to filter them and keep the labeled and predicted matching part"* | mẫu này có *sạch* không | cùng cơ chế với C nhưng dùng làm bộ lọc dữ liệu |
| **J. Kiểm tay** | UI-Ins (1.909 mẫu, 23,3% lỗi) · UI-E2I-Synth (bench 1.477 mẫu) | tỉ lệ lỗi của dữ liệu | có lát 1.074 nhãn ở VCL |

**Điều đáng ghi cho phần liên quan của luận văn:** hai bài GUI mới nhất về sinh câu chỉ dẫn cho
grounding (UI-Ins 10/2025, UI-E2I-Synth ACL Findings 2025) đều **không** chấm câu sinh ra bằng
bộ trỏ; họ dùng GPT + kiểm tay (E, J) rồi đo lợi ích huấn luyện (H). Tức là trong miền GUI, thước
kiểu C của mình vẫn là chỗ trống, dù cơ chế đã có ở REG/VLN.

---

## 3. Điểm phân định nên viết (một đoạn, không quá ba câu mỗi ý)

1. **Với dòng REG (Mao/Yu/Luo):** họ tự huấn luyện listener trên cùng dữ liệu với speaker nên
   phải lo "speaker nhìn thấy giám khảo" (Cohn-Gordon tách đôi dữ liệu; Luo 2018 có cột `Acc-new`
   bằng mô hình thứ hai). Mình dùng bộ trỏ **có sẵn, không đụng vào**, và đã đổi sang bộ trỏ thứ
   hai (UI-Venus) để kiểm. ⚠️ Nhưng cả hai cùng họ Qwen, và UGround có AndroidControl trong
   recipe. Đã khai.
2. **Với dòng VLN (Zhao/Marky):** họ có người thật đi theo; mình không. Zhao khuyên thước không
   tham chiếu chỉ tin ở mức câu, xếp hạng hệ thống thì cần tham chiếu. Mình trả lời bằng năm luật
   chấm không đổi thứ tự và bơm lỗi, nhưng đó là phép kiểm nội bộ, không thay được neo người.
3. **Với Dessì 2022 (bẫy máy chấm thích văn máy):** thước của mình xếp câu người trên mọi nhánh
   máy, khoảng cách 15,7 pp, đúng chiều kỳ vọng trước khi chấm. Đây là lá chắn tốt nhất và đã
   nằm trong FAIR §V.
4. **Với Jedi / Instruction Agent / Jandial (GUI):** cùng cơ chế "bộ trỏ đọc câu", khác mục đích
   (lọc dữ liệu / hoàn thành tác vụ / tấn công). Nêu cả ba để hội đồng thấy đã tra, rồi nói rõ
   khác biệt: mình dùng nó làm **thước cho câu viết cho người, ở mức từng bước, có trần và sàn đo
   được**.

---

## 4. Việc còn nợ từ lượt này

- Mở PDF Luo & Shakhnarovich CVPR 2017 (openaccess trả 403 từ WSL) để xác minh cặp số 97,23/66
  trước khi trích. Cho tới lúc đó chỉ được trích ý *"comprehension model as differentiable proxy
  of human evaluation"* (abstract).
- Cohn-Gordon 2018: mở PDF để xác minh câu *"otherwise this S1 production model effectively has
  access to the system evaluating it"*.
- Marky CVPR 2022: mở PDF xác nhận 71% / 75% rồi mới đưa vào ch5 làm tiền lệ cho khuôn "hai số
  cạnh nhau" (hiện ch5 đang dựa Zhao 2021 và Nangia & Bowman 2019, đủ dùng).
- VIE-DM ICLR 2025: đọc mục thực nghiệm để biết có chấm câu sinh ra bằng REC model không.

---

## 5. Nguồn đã mở

- Mao et al. CVPR 2016: https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Mao_Generation_and_Comprehension_CVPR_2016_paper.pdf
- Luo & Shakhnarovich CVPR 2017 (abstract): https://arxiv.org/abs/1701.03439
- Cohn-Gordon et al. NAACL 2018: https://aclanthology.org/N18-2070/
- Dessì et al. EMNLP 2022: https://aclanthology.org/2022.emnlp-main.546/
- Tang et al. EMNLP 2024: https://arxiv.org/abs/2410.03959
- IREG: https://arxiv.org/abs/2308.09977
- INLG 2024 discourse-aware: https://arxiv.org/abs/2409.05721
- VIE-DM ICLR 2025: https://openreview.net/forum?id=1qbZekXGrp
- Zhao et al. EACL 2021: https://aclanthology.org/2021.eacl-main.111/
- Marky CVPR 2022: https://arxiv.org/abs/2111.12872
- Kamath et al. CVPR 2023: https://arxiv.org/abs/2210.03112
- InstruGen: https://arxiv.org/html/2411.11394
- FCA-R2R: https://arxiv.org/abs/2506.08566
- LaF-GRPO AAAI 2026: https://arxiv.org/html/2506.04070 · https://ojs.aaai.org/index.php/AAAI/article/view/40804
- GoViG: https://arxiv.org/html/2508.09547v1
- GREC 2009: https://www.researchgate.net/publication/268238662_The_GREC_main_subject_reference_generation_challenge_2009
- UI-Ins: https://arxiv.org/html/2510.20286
- UI-E2I-Synth Findings ACL 2025: https://aclanthology.org/2025.findings-acl.809/ · https://arxiv.org/html/2504.11257
- AutoGUI ACL 2025: https://aclanthology.org/2025.acl-long.510/
- OS-Genesis ACL 2025: https://aclanthology.org/2025.acl-long.277/
- AgentTrek ICLR 2025: https://iclr.cc/virtual/2025/poster/30416
- Jedi (UI decomposition & synthesis): https://arxiv.org/html/2505.13227
- Instruction Agent: https://arxiv.org/html/2509.07098
- AskEase CHI 2026: https://arxiv.org/abs/2601.18092
- Jandial et al. Findings EACL 2026: https://aclanthology.org/2026.findings-eacl.144/

---

## 6. Bổ sung 5/9 tối — thước tham chiếu và tỉ lệ đúng loại thao tác cho đủ tám nhánh (0 giây GPU)

Bảng 6.1 luận văn chỉ có BLEU-4 / ROUGE-L cho Base, S1/101 và câu chuẩn. Script gốc không còn
trong kho, nên `harness/text_metrics.py` tái lập cách tính trước rồi mới điền phần thiếu.
Cách tính duy nhất tái lập đúng **38,7 / 67,3** (S1/101), **96,1 / 100,0** (câu chuẩn) và đúng
**176** câu chuẩn ngắn hơn bốn token: BLEU-4 mức câu của nltk, không làm mượt, token là chuỗi
`\w+` thường hoá; ROUGE-L là F1 của `rouge_score`, không stem. Kết quả ở `runs/text_metrics.json`.

| nhánh | Exec. | BLEU-4 | ROUGE-L | đúng loại thao tác |
|---|---|---|---|---|
| Base | 47,59 | **9,9** | **40,4** | 96,46 |
| S1/101 | 59,11 | 38,7 | 67,3 | 94,35 |
| S1/202 | 59,62 | 39,0 | 67,6 | 94,58 |
| S2/101 | 57,18 | 36,4 | 65,9 | 94,85 |
| CE2-S2/101 | 59,42 | 38,1 | 68,6 | 98,86 |
| MIN-DESC/101 | 60,05 | 37,9 | 68,4 | 98,88 |
| gui_sel/101 | 56,13 | 34,5 | 63,0 | 90,90 |
| Câu chuẩn | 75,73 | 96,1 | 100,0 | 100,00 |

⚠️ **Base tái lập ra 9,9 / 40,4, bảng đang in 9,7 / 40,3.** Câu của Base trong
`paper/fair2026/preds_base.jsonl` trùng 4.463/4.463 với tệp thô, tính trên 6.958 bước cho
8,8 / 36,2 nên cũng không phải nhầm quần thể. Lệch 0,2 và 0,1 điểm chưa truy được nguồn; khi
điền bảng nên dùng bộ số tính lại bằng một script cho cả tám hàng và ghi rõ như vậy.

⭐ **Điều bảng mới cho thấy:** trên thước tham chiếu, MIN-DESC (37,9 / 68,4) **thấp hơn** S1/101
về BLEU và chỉ nhỉnh hơn về ROUGE-L, còn CE2-S2 lại cao nhất ROUGE-L; trong khi trên thước
chính MIN-DESC đứng đầu. Thước tham chiếu và thước bộ trỏ **đồng thuận ở ba nhánh xa nhau**
(Base < S1 < câu chuẩn) nhưng **không đồng thuận ở cụm 57–60** — đúng luận điểm của ch5 §5.10 và
Zhao et al. EACL 2021: thước tham chiếu xếp hạng được các hệ khác xa nhau, không đọc được khác
biệt nhỏ. Đây là lý do có số liệu để giữ thước chính, không phải chỉ lập luận.

Cột *đúng loại thao tác* là thước phụ có sẵn trong tệp thô (`action_ok`), đo một cấu trúc khác
hẳn: câu có gọi đúng động từ thao tác không. Hai nhánh chặng hai (CE2, MIN) cao nhất, gần 99;
nhánh ứng viên thấp nhất, 90,9, khớp chẩn đoán bỏ cuộc ở `report/136`.

✅ **Đã đưa vào luận văn và slide (5/9 tối):** Bảng 6.1 điền đủ tám hàng (Base đổi sang 9,9 /
40,4), Bảng 6.2 thêm hàng nhánh ứng viên, Mục 5.10 thêm đoạn về chỗ ba thước bất đồng; slide dự
phòng B1 (`build_baove.js`) cùng bộ số. Dựng lại: 112 trang, 0 overfull, 0 tham chiếu hỏng.
