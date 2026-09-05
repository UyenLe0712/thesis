# 135 — Tiền lệ cho trục đóng góp mới của SOICT (bỏ cuộc / selective prediction)

> Tra ngày **4/9/2026**, mở tận nguồn từng bài (ACL Anthology / CVF / JMLR / trang arXiv để đọc
> trường `journal-ref`), không trích theo trí nhớ. Đây là phần chống lưng câu chữ cho readout mới
> ở `report/134` mục 9. File `134` thắng về thi hành; file này chỉ lo **trích dẫn và phân định**.

## 1. Bảng tiền lệ đã xác minh

| ý cần chống lưng | bài | venue chính xác | trang | trích nguyên văn (rút gọn) |
|---|---|---|---|---|
| Ngưỡng trên hiệu điểm số so với `null`, chỉnh trên dev | Devlin, Chang, Lee, Toutanova (2019), *BERT* | **NAACL-HLT 2019**, Vol. 1 | 4171–4186 | "We predict a non-null answer when ŝ_{i,j} > s_null + τ, where the threshold τ is selected on the dev set to maximize F1." |
| Bỏ cuộc theo ngưỡng, chỉnh riêng cho từng mô hình trên dev | Rajpurkar, Jia, Liang (2018), *Know What You Don't Know* | **ACL 2018**, Vol. 2 (Short) | 784–789 | "At test time, models abstain whenever their predicted probability that a question is unanswerable exceeds some threshold. We tune this threshold separately for each model on the development set." |
| Gốc của selective classification và đánh đổi risk–coverage | El-Yaniv & Wiener (2010) | **JMLR** vol. 11 | 1605–1641 | "selective classification… trading classifier coverage for improved accuracy"; đưa ra "risk-coverage (RC) trade-off" |
| Selective classification cho mạng sâu | Geifman & El-Yaniv (2017) | **NIPS 2017** (⚠️ **không phải NeurIPS** — hội nghị đổi tên năm 2018) | 4878–4887 | "guaranteed 2% top-5 error on ImageNet with 99.9% confidence while maintaining ~60% test coverage" |
| **Risk tại coverage cố định**, AUC của đường cong | Kamath, Jia, Liang (2020) | **ACL 2020** | 5684–5696 | "any choice of γ has an associated coverage—the fraction of D_test the model makes a prediction on—and risk—the error on that fraction… We plot risk versus coverage and evaluate on the area under this curve (AUC), as well as the maximum possible coverage for a desired risk level." |
| Selective risk tại coverage cho trước, trong NLP | Xin, Tang, Yu, Lin (2021), *The Art of **Abstention*** | **ACL-IJCNLP 2021**, Vol. 1 (Long) | 1040–1051 | "The selective classifier aims to minimize the selective risk at a given coverage." (công thức γ(h), r(h), eq. 3–4) |
| **Bỏ cuộc quá mức là một dạng hỏng**, không phải an toàn | Srinivasan et al. (2024), *Selective "Selective Prediction"* | **Findings of ACL 2024** | 12935–12948 | "selective prediction may be over-cautious and abstain too frequently, even on many correct predictions" |
| Khảo sát abstention, gồm cả thước và benchmark | Wen, Yao, Feng, Xu, Tsvetkov, Howe, Wang (2025) | **TACL** vol. 13 | 529–556 | mục riêng về "benchmarks, and evaluation metrics" |
| ⚠️ **Thước phải phủ cả nhóm không có đích**, trong quy chiếu thị giác | Liu, Ding, Jiang (2023), *GRES* | **CVPR 2023** (Highlight) | 23592–23601 | "we further propose a new metric called generalized IoU (gIoU), which extends the mean IoU to all samples including no-target ones. Moreover, No-target performance is also separately evaluated by computing No-target-accuracy (N-acc.) and Target-accuracy (T-acc.)" |
| Điểm chuỗi chuẩn hoá theo độ dài để xếp hạng | Yang, Huang, Ma (2018), *Breaking the Beam Search Curse* | **EMNLP 2018** | 3054–3059 | "RNNSearch… first introduces the length normalization method, whose score is simply the average model score: Ŝ_{length norm}(x,y) = S(x,y)/\|y\|. This is the most widely used rescoring method since it is hyperparameter-free." |
| Bản so sánh các cách chuẩn hoá độ dài | Murray & Chiang (2018) | **WMT 2018** (Proc. Third Conf. on MT: Research Papers) | 212–223 | "we compare some commonly-used methods for doing this, finding that a simple per-word reward works well" |

## 2. Ba chỗ phải sửa so với cách nhớ thông thường

1. **Tên bài của Xin et al. là *"The Art of Abstention"***, không phải *"The Art of Abstaining"*.
2. **Geifman & El-Yaniv 2017 ở NIPS**, không phải NeurIPS. Trích đúng: *Advances in Neural
   Information Processing Systems 30 (NIPS 2017)*.
3. ⛔ **GNMT (Wu et al. 2016, arXiv 1609.08144) CHƯA từng qua bình duyệt** — báo cáo kỹ thuật,
   không `journal-ref`. Luật dự án chỉ trình peer-reviewed ⇒ **không dùng GNMT làm trụ trích dẫn
   cho length normalization**. Trụ đúng là **Yang et al. EMNLP 2018** (nêu thẳng công thức
   `S(x,y)/|y|` và gọi nó là cách rescoring dùng rộng nhất), truy tiếp về Bahdanau 2014. Muốn
   nhắc GNMT thì chỉ nhắc như nguồn của biến thể `length^α`, **kèm nhãn preprint**.

## 3. Abstention trong miền GUI — KHÔNG tìm thấy bài đã bình duyệt

Tám bài gần nhất đều là **preprint arXiv không venue**, tính tới 4/9/2026:

| bài | arXiv | ngày | venue |
|---|---|---|---|
| SafeGround: Know When to Trust GUI Grounding Models via Uncertainty Calibration | 2602.02419 | 2/2026 | không có |
| HyperClick: Enhancing Trustworthy GUI Grounding via Self-Critiqued RL | 2510.27266 | 10/2025, v2 5/2026 | không có |
| Uncertainty Quantification for Computer-Use Agents | 2606.25760 | 6/2026 | không có |
| Uncertainty-Aware GUI Agent | 2508.04025 | 8/2025 | không có |
| UI-Zoomer: Uncertainty-Driven Adaptive Zoom-In for GUI Grounding | 2604.14113 | 4/2026 | không có |
| AgentAbstain: Do LLM Agents Know When Not to Act? | 2607.10059 | 7/2026 | không có; **sandbox tool-use, không phải GUI** |
| ReDAct: Uncertainty-Aware Deferral for LLM Agents | 2604.07036 | 4/2026 | không có; **ALFWorld/MiniGrid, không phải GUI** |
| AbstentionBench | 2506.09038 | 6/2025 | không có |

⚠️ **Câu chữ an toàn: *"chúng tôi không tìm thấy"*, KHÔNG viết *"chưa có"***. Phép tra dùng công
cụ tìm kiếm, không phải quét vét cạn ACL Anthology + CVF. Và bốn bài xuất hiện chỉ trong nửa năm
gần đây ⇒ **đây là chỗ đang đông người**, khả năng có bài mới trước 16/9 là thật.

## 4. ⛔ Cái bẫy lớn nhất: GRES/GREC đã chiếm ý "no-target" từ CVPR 2023

Nếu bài đóng khung theo hướng **biểu thức quy chiếu** (đúng khung VCL đang dùng) thì **GRES**
đã có sẵn đúng cấu trúc thước ba mảnh mà dự án định dựng: gIoU tính trên **toàn bộ** mẫu kể cả
no-target, cộng **N-acc.** và **T-acc.** báo riêng. Gần như trùng bộ ba HasAns / NoAns / overall,
chỉ khác miền (vùng ảnh vs phần tử rời rạc) và khác dạng đầu ra.

⇒ **Bắt buộc nêu điểm khác ngay chỗ trình bộ ba:** GRES chọn **vùng ảnh**; bài này chọn **một
phần tử trong khối ứng viên rời rạc** rồi mới **sinh câu**. Không nêu thì phản biện quy về
*"áp lại GREC"*.

## 5. Phân định — được nói gì, cấm nói gì

**Đã có chủ, cấm nhận là mới:** ngưỡng trên hiệu điểm số so với null (BERT · SQuAD 2.0) ·
risk-coverage và risk tại coverage cố định (El-Yaniv & Wiener · Kamath · Xin) · hiện tượng bỏ
cuộc quá mức (Srinivasan) · tách nhóm có/không có đáp án kèm mốc "luôn bỏ cuộc" (Rajpurkar, mốc
48,9 F1) · thước phủ cả nhóm no-target trong quy chiếu thị giác (GRES) · điểm chuỗi chuẩn hoá độ
dài (Yang et al.).

**Ba lớp chưa tìm thấy tiền lệ, hẹp dần:**
1. Bỏ cuộc đặt **bên trong đầu chọn phần tử tường minh của mô hình SINH câu hướng dẫn GUI** —
   bảy preprint ở §3 đều làm ở tầng **định vị** hoặc tầng **agent thi hành**, không tầng sinh ngôn ngữ.
2. **Định lượng cái bẫy của thước** trong miền GUI: bỏ abstain kéo thước-nhóm-có-đích
   **57,54 → 69,05** trong khi độ đúng toàn tập **tụt 63,43 → 49,71**. Rajpurkar có mốc "luôn bỏ
   cuộc", nhưng đó là mốc suy biến ở **đầu kia**; phép so **ép-phải-chọn trên cùng một mô hình đã
   train**, trong miền GUI, thì không thấy ai làm.
3. Nối bỏ cuộc với **dạng lỗi đã đo được**: điểm-đúng-tên-sai **34:1**, và lẫn loại thao tác gấp
   **20 lần** ở ca bỏ cuộc (39,6% vs 2,0%). Các bài GUI kia dừng ở hiệu chuẩn độ tin cậy, không
   truy về cơ chế sai.

**Câu chữ đề nghị cho bài:** *"Chúng tôi áp bộ đọc kết quả kiểu SQuAD 2.0 và đường cong
risk-coverage, vốn đã chuẩn hoá trong hỏi đáp và phân loại chọn lọc, vào miền sinh hướng dẫn GUI,
nơi chúng tôi không tìm thấy công trình đã bình duyệt nào áp dụng."*
⛔ **Cấm chữ "đầu tiên" / "mới"** cho bản thân cơ chế bỏ cuộc.
