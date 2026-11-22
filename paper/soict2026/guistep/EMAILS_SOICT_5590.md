# SOICT 2026 — Paper 5590: mọi mail nhận được (chép nguyên văn từ tin user dán)

Đợt A: năm mail nhận 22/10/2026 (chấp nhận, phản biện, camera-ready). Đợt B: năm mail nhận sau camera-ready (user dán 21/11/2026). Mail SOICT mới thì chép nối vào cuối file này.

Việc cần làm rút ra từ các mail này: `CAMERA_READY_ACTION_22_10.md` (cùng thư mục).
Mail A4 có đính kèm file Word form License to Publish (nay là `thesis/SNCS_ProceedingsPaper_LTP_ST_SN_Singapore.docx`).

---

# ĐỢT A — năm mail nhận 22/10/2026

## Mail A1 — Chấp nhận + nhận xét phản biện

Dear Uyen Le Doan Phuong,

We are pleased to inform you that your submission has been accepted for an ORAL presentation and publication in the SOICT 2026 proceedings.
Paper ID: 5590
Paper Title: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation
Author(s): Uyen Le Doan Phuong


Please carefully review the information below, as it outlines the necessary steps to finalize your paper submission and prepare for the conference:

1. Paper Revision
You will find the evaluation of your paper below. We kindly ask you to thoroughly address the reviewers’ comments and revise your paper accordingly. The final submission should be between 12 and 15 pages.

2. Camera-ready Submission
All accepted papers will be published in the Springer CCIS series. The proceedings of SOICT 2026 will be indexed in DBLP, Google Scholar, EI-Compendex, Mathematical Reviews, SCImago, and Scopus.
To complete your camera-ready submission, you will need to grant publication rights to Springer and include the permission statement in your final paper. Detailed instructions for preparing the camera-ready version will be available on the conference website:
https://soict.org/submission/camera-ready-submission/
The camera-ready version of your paper is due by 30 October 2026.

3. Registration
At least one author is expected to register with a full registration and present the paper at the symposium. The registration instructions will be available on the symposium website: https://soict.org/registration/

4. Presentation Guidelines
Each paper will have a 15-minute oral presentation, including Q&A. Please adhere to this time limit to ensure smooth transitions between sessions. A projector and screen will be available in the session rooms.
Presenters should arrive 5-10 minutes before their session begins to inform the session chair and check that their slides work properly with the room’s audio-visual system. If any issues arise, notify the session chair or technical staff immediately.
We also invite you to participate in poster sessions. We aim to organize the sessions to encourage meaningful interaction and discussion among researchers, professors, scientists, and students attending the conference.
Poster sessions will run separately from oral sessions. We will provide adhesive tape for holding the posters. Please send us the file, and we will print it for you. Printing is free.

5. Visa Invitation Letter
If you require an invitation letter for your visa application, please register on the conference website and send a request to contact@soict.hust.edu.vn.
For more information, visit the conference website: http://soict.org/.

We look forward to welcoming you to Ho Chi Minh City, Vietnam.

Sincerely,
SOICT 2026 Program Chairs
Wray Buntine, Morten Fjeld, Klaus Schöffmann, Tran The Truyen, Tran Minh Triet, Huynh Thi Thanh Binh

SUBMISSION: 5590
TITLE: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation

----------------------- REVIEW 1 ---------------------

SUBMISSION: 5590
TITLE: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation

----------- Overall evaluation -----------
Summary:
The paper tackles the problem of generating GUI step instructions using a vision language model (VLM). Basically, the paper aims to generate a sentence that tells a person which element to touch next. The paper proposes to adapt a VLM in two ways, one is on the sentence and another is on the declaration followed by the sentence. The paper then proposes to refine the declaration model using preference pairs that differ in the declared element. The proposed approach is applied using the human step instructions in AndroidControl and automatically derived structured target declarations. The experimental evaluation is based on execution, assessing whether the generated step instructions are executable on the evaluated dataset.

Strengths:
+ The paper aims to solve a practical and challenging problem, which is to generate GUI step instructions.
+ The paper has some reasonable technical contributions, including the proposal of using two VLM modules, one for the step instruction sentences, and one for the declarations.
+ The experimental evaluation shows that the proposed framework achieves better performance than the base VLM.

Weaknesses:
+ The paper’s writing is very hard to follow. It mixes the actual implementation on the AndroidControl dataset with some specific configurations (that should be described in the experimental evaluation) and doesn’t describe a general framework (that could be applied to any dataset). It took me a lot of effort to understand the paper but I’m not sure if I can fully understand the technical details because of the unclear writing.
+ The proposed framework is only evaluated on one dataset and with one type of VLM, so I’m not sure if the proposed framework can generalize and still perform well.


----------------------- REVIEW 2 ---------------------

SUBMISSION: 5590
TITLE: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation

----------- Overall evaluation -----------
The paper presents GUIStep, a compact vision-language model for generating human-readable instructions describing the next action in a mobile GUI. It reuses AndroidControl instructions and automatically constructs target declarations and preference pairs. Three configurations are evaluated: sentence-only fine-tuning, declaration-assisted fine-tuning, and preference refinement. The paper also proposes an executability metric that uses a frozen grounding model to recover the target element from the generated instruction. On 4,463 touch steps, the best configuration achieves an executability score of 66.5, compared with 53.6 for the untuned backbone.

The application is useful, and the paper provides a clear account of its methods and limitations. However, the validity of the primary evaluation metric remains insufficiently established, and the experiments provide limited evidence of an advantage beyond standard supervised fine-tuning. These concerns lead me to recommend weak reject.

Strong points:
- Generating instructions for a person is a meaningful application of GUI understanding. The paper clearly explains why coordinate prediction and reference-overlap metrics do not fully address this task.

- Reusing existing human instructions and deriving auxiliary supervision from accessibility trees avoids additional training annotation. The paper describes the model adaptation, declaration construction, preference-pair filtering, and output extraction in reasonable detail.

- The authors explicitly acknowledge that declaration training reduces performance and that preference refinement does not significantly outperform sentence-only training. The matched cross-entropy control is valuable for separating the preference objective’s contribution from additional training. The metric validation also reports failed checks instead of presenting only favorable results.

Weak points:

- The framework combines an existing backbone, QLoRA fine-tuning, automatically constructed declarations, and an established preference objective. The task adaptation is useful, but the proposed additional components do not establish a clear benefit over sentence-only training. GUIStep-D reduces executability from 65.5 to 63.6, while GUIStep-P reaches 66.5 and is not significantly better than GUIStep-S. Its improvement over the matched cross-entropy control is only 0.52 points.

- Section 7 states that the injection suite uses Voronoi localization, whereas the reported executability scores use the D.3 bounding-box rule. Consequently, Table 2 does not directly validate the metric used in Table 3. The assertion that the reported detection rates are upper bounds also requires justification: bounding-box and Voronoi acceptance regions are not necessarily nested merely because one rule produces a higher aggregate acceptance rate. The full validation suite should be rerun using the exact primary scoring procedure.

- The injection suite detects only 33.1% of neighboring-element errors and 20.0% of negations outside the polarity table. Confusion between neighboring controls is directly relevant to the intended task, so this weakness affects confidence in the central evaluation. A manually assessed sample of generated instructions, or a small human target-selection study, would help establish how closely executability reflects instructions that people can actually follow.

- The experiments compare the adapted configurations with their own untuned backbone and an internal training control. This demonstrates the benefit of fine-tuning that backbone, but does not establish how GUIStep compares with other reasonable approaches. Useful baselines would include another instruction-capable vision-language model and a pipeline that selects a GUI target and then verbalizes it. Comparisons should use equivalent screenshots, goals, histories, and OCR information.

- Training and test tasks are disjoint, but applications can overlap, and 17.3% of test reference sentences occur verbatim in training. Repeated wording is common in GUI instructions and does not itself demonstrate leakage, but separate results for repeated and unseen sentences would clarify the source of the gains. An application-disjoint evaluation would provide stronger evidence of transfer.

- Section 5.3 reports a GUIStep-S improvement of 11.14 points under UGround, whereas Table 3 implies approximately 11.9 points from 65.5 minus 53.6. Please reconcile these values or identify any different evaluation subset.

- Section 6.4 labels all 1,443 non-action failures as descriptions of the wrong element. A failed grounding check can also arise from listener error or reconstructed-box error. Unless these cases were manually inspected, they should be described as localization failures.

- The paper recognizes within-application dependence when constructing confidence intervals, but uses McNemar’s test for paired comparisons. Please explain whether the significance tests account for this dependence. Repeated training runs would also help assess the stability of the small differences between adapted configurations.

- Reporting inference latency, peak memory usage, exact prompts, scoring rules, and availability of code or checkpoints would strengthen the compact-model motivation and reproducibility.


----------------------- REVIEW 3 ---------------------

SUBMISSION: 5590
TITLE: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation

----------- Overall evaluation -----------
The papers presents GUIStep, an automatically constructed training pipeline for GUI step instruction generation. GUIStep reuses AndroidControl’s instructions, derive target declarations from the accessibility tree and construct preference pairs from competing elements. It fine-tunes Qwen2.5-VL-3B using the AndroidControl data and introduces an executability based evaluation metric that assesses whether generated instructions identify the intended GUI element.

The best model achieves 66.5% executability, compared with 53.6% for the untuned backbone.

Strong points are meaningful task formulation, interesting evaluation approach and quite a comprehensive experimental analysis.

Weak points are as follow.
-A limited model-level novelty as the proposed training techniques rely on existing QloRA and preference optimization methods and most performance improvement comes from straightfoward supervised fine-tuning.
-Executability is measured by another learned model rather than actual human interactions.
-The effectiveness of preferenced refined GUIStep-P over GUIStep-S (66.5% vs. 65.5%, p=0.078) is not significantly observed. Therefore the benefit of the more complex training procedure is not clear.
-The writing is  hard to follow.


----------------------- REVIEW 4 ---------------------

SUBMISSION: 5590
TITLE: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation

----------- Overall evaluation -----------
The paper proposes GUIStep, a compact vision-language model for generating human-readable next-step GUI instructions, together with an execution-based evaluation metric using a frozen grounding model. However, the reviewer has some concerns as follows:
The primary executability metric depends on a learned grounding model and fails on neighboring-element and unseen-negation cases.
Evaluation is restricted to touch actions, excluding non-touch GUI interactions.
The study uses only one English dataset and one backbone, limiting generalization.
No external state-of-the-art GUI instruction-generation system is directly compared.
Test-time history uses ground-truth previous instructions rather than model-generated history, avoiding realistic error accumulation.

---

## Mail A2 — Nhắc camera-ready (bản có dấu `*******`, ban tổ chức chưa điền hạn)

- Paper: 5590
  - Authors: Uyen Le Doan Phuong
  - Title: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation

-------------------------------------------------------

Dear Uyen,

You have already received the comments by the reviewers in a previous email. Please take them carefully into account when preparing your camera-ready paper for the proceedings. The final paper and the signed copyright form are due on *******.

This is a firm deadline for the production of the proceedings. You should submit your paper using your EasyChair proceedings author role for SOICT 2026.

1. FINAL PAPER: Please submit the files belonging to your camera-ready paper using your EasyChair author account. Follow the instructions after the login for uploading two files:

  1. either a zipped file containing all your LaTeX sources or a Word file in the RTF format, and
  2. the PDF version of your camera-ready paper

The page limit is ******** and is strict. Please follow strictly the author instructions of Springer-Verlag (https://www.springer.com/gp/computer-science/lncs/conference-proceedings-guidelines) when preparing the final version.

Our publisher has recently introduced an extra control loop: once data processing is finished, they will contact all corresponding authors and ask them to check their papers. We expect this to happen shortly before the printing of the proceedings. At that time your quick interaction with Springer-Verlag will be greatly appreciated.

2. COPYRIGHT: Please upload a signed and completed copyright form to us as soon as possible. The Springer copyright forms can be found at https://resource-cms.springernature.com/springer-cms/rest/v1/content/19790018/data/SNCS_ProceedingsPaper_LTP_ST_SN_Switzerland

It is sufficient for one of the authors to sign the copyright form. You can scan the form into PDF or any other standard image format.

We greatly appreciate your cooperation in these matters. Thank you again for your contribution to SOICT 2026.

All questions about papers should be sent to the volume editors editors Huynh Thi Thanh Binh <binh.huynhthithanh@hust.edu.vn>, Wray Buntine <wray.buntine@gmail.com>, Tuan Dam <tuanquangdam@gmail.com>, Tuan Linh Dang <linhdt@soict.hust.edu.vn>, Ichiro Ide <ide@i.nagoya-u.ac.jp>, Minh-Triet Tran <tmtriet@hcmus.edu.vn>, Truyen Tran <truyen.tran@deakin.edu.au>.
__________________________________________________
Please be aware that this is an unmonitored email alias,
so please do not reply to this email.
To contact EasyChair use the EasyChair contact Web page
https://easychair.org/contact

---

## Mail A3 — Nhắc camera-ready (bản đã điền hạn và số trang)

- Paper: 5590
  - Authors: Uyen Le Doan Phuong
  - Title: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation

-------------------------------------------------------

Dear authors,

You have already received the comments by the reviewers in a previous email. Please take them carefully into account when preparing your camera-ready paper for the proceedings. The final paper and the signed copyright form are due on 30-October-2026.

This is a firm deadline for the production of the proceedings. You should submit your paper using your EasyChair proceedings author role for SOICT 2026.

1. FINAL PAPER: Please submit the files belonging to your camera-ready paper using your EasyChair author account. Follow the instructions after the login for uploading two files:

  1. either a zipped file containing all your LaTeX sources or a Word file in the RTF format, and
  2. the PDF version of your camera-ready paper

Regarding the pages limit, full papers must be from 12 to 15 pages (including figures and tables and references) while short papers must be from 8 to 11 pages (including figures and tables and references) in CCIS/Springer format. You must prepare your paper strictly following the Springer CCIS author guidelines. Please follow strictly the author instructions of Springer-Verlag (https://www.springer.com/gp/computer-science/lncs/conference-proceedings-guidelines) when preparing the final version.

Our publisher has recently introduced an extra control loop: once data processing is finished, they will contact all corresponding authors and ask them to check their papers. We expect this to happen shortly before the printing of the proceedings. At that time your quick interaction with Springer-Verlag will be greatly appreciated.

2. COPYRIGHT: Please upload a signed and completed copyright form to us as soon as possible. The Springer copyright forms can be found at https://resource-cms.springernature.com/springer-cms/rest/v1/content/19790018/data/SNCS_ProceedingsPaper_LTP_ST_SN_Switzerland

It is sufficient for one of the authors to sign the copyright form. You can scan the form into PDF or any other standard image format.

We greatly appreciate your cooperation in these matters. Thank you again for your contribution to SOICT 2026.

All questions about papers should be sent to the volume editors editors Huynh Thi Thanh Binh <binh.huynhthithanh@hust.edu.vn>, Wray Buntine <wray.buntine@gmail.com>, Tuan Dam <tuanquangdam@gmail.com>, Tuan Linh Dang <linhdt@soict.hust.edu.vn>, Ichiro Ide <ide@i.nagoya-u.ac.jp>, Minh-Triet Tran <tmtriet@hcmus.edu.vn>, Truyen Tran <truyen.tran@deakin.edu.au>.

---

## Mail A4 — Form License to Publish mới (đính kèm file Word)

Dear Authors,

Please use the updated Springer Nature License to Publish form attached to this email when preparing your camera-ready submission for SOICT 2026. The copyright consent template currently linked on the conference website is outdated and should be replaced by this attached version.

Please complete the following steps:

Complete the updated form with your paper title, the full names of all authors, the corresponding author’s name, and the required signatory details. Ensure that this information matches your final manuscript and the records in EasyChair. The conference name and volume editors’ names have already been filled in.

Print and sign the form in ink, then scan the completed, signed form as a PDF. The corresponding author may sign on behalf of all co-authors, provided they are authorized to do so. Digital signatures are not accepted.

Include the signed and scanned form in your camera-ready ZIP file, together with:

A folder named “Source” containing all files needed to reproduce the final manuscript.

A text file containing the name and email address of the paper’s single corresponding author.

Upload the ZIP file and the final manuscript PDF to EasyChair by October 30, 2026.

If you have already uploaded a signed copy of the old form, please complete and sign the updated form and replace the old copy in your camera-ready ZIP file, then upload the revised ZIP file to EasyChair by the same deadline.

The remaining camera-ready instructions are available at:
https://soict.org/submission/camera-ready-submission/

We apologize for any inconvenience and thank you for your cooperation.

Best regards,

SOICT 2026 Organizing Committee

---

## Mail A5 — Hướng dẫn nộp chi tiết

Dear Authors,

Following our previous email about the updated Licence to Publish form, please follow the instructions below to complete your SOICT 2026 camera-ready submission by October 30, 2026.

Please pay particular attention to the signature and contact details: the designated corresponding author must personally sign the form and clearly provide their full name and email address.

1. Complete and sign the updated Licence to Publish form

Use the updated form provided in our previous email, replacing the outdated template linked on the conference website.

Each paper must have one corresponding author.

The corresponding author must personally sign the form in ink.

Enter the corresponding author’s full name in the “Corresponding Author Name” field. The “Print Name” and “Email” fields in the signature section must identify that same person. Complete the date, address, and all other required fields.

Provide an active email address that the corresponding author checks regularly. This address will be used for publication queries, proofreading, and other follow-up communication.

Scan the complete signed form into a clear, readable PDF. Digital signatures are not accepted.

2. Prepare the two files to upload

File A — Final manuscript PDF

Prepare your final paper in Springer CCIS format, incorporating the reviewers’ comments. Clearly identify the corresponding author and their email address in the manuscript.

File B — One ZIP archive containing all three items below

A folder named “Source”, containing all files needed to reproduce the final PDF: the Word document, or the LaTeX source and all supporting bibliography, figure, and other required files.

A text file, for example “Corresponding_Author.txt”, clearly stating the paper title, corresponding author’s full name, and corresponding author’s email address.

The complete, signed and scanned updated Licence to Publish form in PDF format.

The corresponding author’s identity and email address must be consistent across the manuscript, licence form, contact-information text file, and EasyChair record.

3. Access your paper in EasyChair

Open the SOICT 2026 EasyChair page.

Log in using the EasyChair account associated with your accepted paper.

Select the “proceedings author” role for SOICT 2026 Proceedings.

Open the entry for your accepted paper and select the option to upload or update its proceedings files.

Please upload to the existing proceedings entry for your accepted paper. Do not create a new submission.

4. Upload and verify your files

Upload the final manuscript PDF and the ZIP archive in their respective fields, then complete the upload using the submission/save button shown on the page.

After submission, reopen your paper’s file list and verify that both files have been uploaded successfully and contain the correct final versions.

If you previously submitted the old form, a form signed by someone other than the corresponding author, or a form with missing contact details, please replace it with a correctly completed form signed by the corresponding author and upload the revised ZIP archive by October 30, 2026.

If you cannot find the proceedings-author role, access your paper, or upload your files, please contact the Organizing Committee promptly. Include your paper ID, paper title, EasyChair account email address, and a screenshot of the issue.

Thank you for your cooperation.

Best regards,
SOICT 2026 Organizing Committee

---

# ĐỢT B — năm mail nhận sau camera-ready (user dán 21/11/2026, theo thứ tự nhận, không rõ ngày)

## Việc rút ra từ các mail này

| việc | hạn | trạng thái 21/11 |
|---|---|---|
| Phí đăng ký | — | **đã nhận** (mail 1), Registration ID **SOICT2026-00067**, có biên lai đính kèm |
| Poster A0 dọc (841 × 1189 mm), gửi cả PPTX lẫn PDF qua https://forms.gle/HTPSK3scJ1b9zVq1A | **23/11/2026** | không bắt buộc (mail gọi là *invite*); ban tổ chức in miễn phí và tự dán |
| Xem lịch trình bày, thứ tự tác giả trong tài khoản EasyChair | — | xem tại https://easychair.org/smart-program/SOICT2026/ |
| Đăng ký làm chủ toạ phiên (session chair) qua https://forms.gle/fvsnq3p3FmK9BFXd9 | **23/11/2026** | tuỳ chọn |
| Trình bày oral 15 phút **gồm cả hỏi đáp**, tới phòng sớm 5–10 phút để báo chủ toạ và thử slide | hội nghị tháng 12/2026, TP.HCM | slide ở `slides/` (deck SOICT) |

### Lịch trình bày (tra chương trình EasyChair 21/11/2026)

- **Thứ Bảy 5/12/2026, 10:00**, **Session 6B: Applied AI, Big Data Analytics, and Data-Driven Applications** (SOICT Technical Session 17), phòng **Salon B**. Phiên 08:30–11:00, 10 bài cách nhau đúng 15 phút, GUIStep là bài thứ 7 (sau bài fake news 09:45, trước bài dự báo giá ngô 10:15). Chương trình chưa ghi chủ toạ phiên.
- GUIStep **không** có trong phiên poster 6F cùng giờ (14 poster, toàn bài khác) ⇒ bài chỉ trình bày oral; poster là việc thêm nếu muốn.
- Hội nghị 4–5/12/2026; chương trình chỉ ghi tên phòng (Salon A/B, Windsor, Buckingham, Balmoral), không ghi tên khách sạn; soict.org không truy cập được lúc tra.
- Thứ Bảy sau phiên: tea break 11:00–11:30 · Keynote III (Brigitte Jaumard) 11:30–12:10 · ăn trưa 12:10–13:30.
- Tiền lệ SOICT 2025 (Nha Trang, Sheraton, 12–13/12/2025): cũng chạy oral và "Poster Exhibition" song song, bài poster khác bài oral; mỗi phiên sáng mở bằng keynote.

Liên hệ: Hoa Binh Group `event31@hoabinh-group.com` (đăng ký) · `contact@soict.hust.edu.vn`.

---

## Mail B1 — Xác nhận đã nhận phí đăng ký (Hoa Binh Group)

Dear Ms. Lê Đoàn Phương Uyên,

Greetings from Hoa Binh Group, the registration services agency for The 15th International Symposium on Information and Communication Technology (SOICT 2026).

We are pleased to inform you that your registration fee has been successfully received. Please find the receipt attached for your reference.

Your Registration ID is SOICT2026-00067. Please keep this ID for reference in all future communications regarding SOICT 2026.

If you have any questions or need further assistance, please do not hesitate to contact us at event31@hoabinh-group.com or contact@soict.hust.edu.vn.

We look forward to welcoming you to SOICT 2026 and hope you enjoy a rewarding and enriching experience at the conference.

Warm regards,

SOICT 2026 Secretariat

---

## Mail B2 — Chấp nhận oral (bản gửi lại, kèm hướng dẫn poster, hạn 23/11)

Dear Uyen Le Doan Phuong,

We are pleased to inform you that your submission has been accepted for an ORAL presentation and publication in the SOICT 2026 proceedings.
Paper ID: 5590
Paper Title: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation
Author(s): Uyen Le Doan Phuong

Presentation Guidelines
Each paper will have a 15-minute oral presentation, including Q&A. Please adhere to this time limit to ensure smooth transitions between sessions. A projector and screen will be available in the session rooms.
Presenters should arrive 5-10 minutes before their session begins to inform the session chair and check that their slides work properly with the room's audio-visual system. If any issues arise, notify the session chair or technical staff immediately.

We also invite you to participate in poster sessions. We aim to organize the sessions to encourage meaningful interaction and discussion among researchers, professors, scientists, and students attending the conference.
Poster sessions will run separately from oral sessions. We will provide adhesive tape for holding the posters. Please send us the file, and we will print it for you. Printing is free.

Poster Presentation Preparation:
• Posters will be A0 size, 841 x 1189mm (portrait format). Feel free to use your own artwork and design.
• Please send the presentation files (in both PPTX and PDF formats) to the SOICT organizers no later than November 23, 2026: https://forms.gle/HTPSK3scJ1b9zVq1A
• To better assist authors, the organizers will handle the printing (for free) and setup of your poster, ensuring a hassle-free experience. This means you do not have to worry about printing the poster or setting it up for the conference. Therefore, please send us your presentation files following the due date.
Poster Exhibition:
Your poster will be on display in the exhibition rooms throughout the entire day of your presentation in SOICT, allowing all participants to engage with your research, not just during your designated presentation session.

We believe the poster presentation format will foster a rich, collaborative environment for sharing knowledge, networking, and building lasting connections with fellow researchers. Your paper's selection for poster presentation reflects its significance and contribution to the conference.

We eagerly anticipate your participation in SOICT 2026, which will be held in Ho Chi Minh City in December 2026. Your presence will undoubtedly enhance the quality of our conference, and we look forward to welcoming you to Ho Chi Minh City, Vietnam.

If you have any questions or require further assistance, please do not hesitate to contact us. Thank you once again for your valuable contribution to SOICT 2026.

Sincerely,
SOICT 2026 Program Chairs
Wray Buntine, Morten Fjeld, Klaus Schöffmann, Tran The Truyen, Tran Minh Triet, Huynh Thi Thanh Binh

---

## Mail B3 — Chương trình hội nghị đã đăng

Dear Uyen Le Doan Phuong,

Thank you for your contributions to SOICT 2026.

We are pleased to inform you that the conference program is now available at the following link: https://easychair.org/smart-program/SOICT2026/

We kindly ask you to review the schedule and make arrangements to attend your presentation session. Should you have any questions, please do not hesitate to contact us.

We look forward to seeing you at SOICT 2026.

SOICT 2026 Program Chairs
Wray Buntine, Morten Fjeld, Klaus Schöffmann, Tran The Truyen, Tran Minh Triet, Huynh Thi Thanh Binh

---

## Mail B4 — Chương trình cập nhật, kiểm thứ tự tác giả trên EasyChair

Dear Uyen Le Doan Phuong,

Paper ID: 5590
Paper Title: GUIStep: A Compact Vision-Language Model for GUI Step Instruction Generation
Author(s): Uyen Le Doan Phuong

Thank you for your contributions to SOICT 2026.

We have updated the program at the following link: https://easychair.org/smart-program/SOICT2026/

We kindly ask you to review information in your easychair account, the order of authors (it will be appeared in the program automatically as your input), the schedule and make arrangements to attend your presentation session. Should you have any questions, please do not hesitate to contact us.

We look forward to seeing you at SOICT 2026.

SOICT 2026 Program Chairs
Wray Buntine, Morten Fjeld, Klaus Schöffmann, Tran The Truyen, Tran Minh Triet, Huynh Thi Thanh Binh

---

## Mail B5 — Mời đăng ký làm chủ toạ phiên (hạn 23/11)

Dear Uyen Le Doan Phuong,

Thank you for contributing to SOICT 2026.

We have shared the available session time slots with you: https://easychair.org/smart-program/SOICT2026/

If you are interested in serving as Session(s) chair, please select the slot that best fits your availability and register by 23 Nov 2026 at: https://forms.gle/fvsnq3p3FmK9BFXd9

As Session chair, you will opening the session, introduce each speaker, keep the presentations on schedule, and moderate the Q&A. We will send you further details closer to the conference.

We greatly appreciate your support and look forward to welcoming you to SOICT 2026. Please do not hesitate to contact us if you have any questions.

SOICT 2026 Program Chairs
Wray Buntine, Morten Fjeld, Klaus Schöffmann, Tran The Truyen, Tran Minh Triet, Huynh Thi Thanh Binh
