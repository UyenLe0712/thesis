# Deep Research & Debate — Vì sao GRPO, vì sao SPICE, và hướng cải tiến reward cho GUI Instruction Generation

**Ngày chốt tài liệu:** 08/11/2026  
**Trạng thái:** Tài liệu nghiên cứu / đề cương thí nghiệm; **chưa phải kết quả của reward mới**.  
**Ngữ cảnh code:** Windows `D:\Master\Thesis` (CodeLocal), nhánh S1/101 → GRPO-SPICE → ACE.  
**Phạm vi:** hướng dẫn thao tác GUI bằng câu tiếng Anh từ ảnh màn hình, goal, history và OCR; **không phải** mô hình xuất tọa độ hoặc agent thực thi trực tiếp.  
**Mục tiêu:** đưa ra lập luận có thể phản biện trước hội đồng, các công thức reward được ưu tiên, và thiết kế bằng chứng để chọn cấu hình tốt nhất mà không chọn trên test.

> **Nguyên tắc đọc.** `[REPO/ĐO]`: kết quả có trong source/report ngày 08/11; `[PAPER]`: công trình đã kiểm tra trên nguồn xuất bản gốc; `[GIẢ THUYẾT]`: phương pháp đề xuất, **chưa được kiểm nghiệm**; `[KHÔNG ĐƯỢC KHẲNG ĐỊNH]`: một suy diễn mà số liệu hiện tại không hỗ trợ. Kết quả trong các báo cáo nội bộ không tự động trở thành kết quả xác nhận độc lập khi đã dùng test để thăm dò nhiều lần.

---

## 0. Kết luận điều hành — có thể dùng khi báo cáo với thầy

**Không nên cố chứng minh “GRPO là thuật toán tốt nhất” hay “SPICE là metric tốt nhất”.** Đây là hai khẳng định mạnh hơn dữ liệu đang có. Lập luận chặt hơn là:

1. **GRPO là lựa chọn thuật toán xuất phát có lý do rõ ràng:** tối ưu sequence-level, non-differentiable reward từ nhiều candidate cho cùng screenshot, không cần value model riêng, phù hợp tài nguyên 3B VLM. **Nhưng** SCST/RLOO/PPO/SFT tiếp là đối chứng bắt buộc; kết quả hiện tại chưa cho phép kết luận GRPO vượt SCST.
2. **SPICE là nền tảng semantic có ý nghĩa**, đã có tiền lệ khi đánh giá instruction và caption, không phụ thuộc n-gram thuần túy. **Nhưng** trên GUI câu ngắn, SPICE bỏ sót action verb, bị zero tuple và dễ thưởng “đúng khuôn” hơn đúng target. Vì vậy **cần sửa SPICE cho GUI**, chứ không nói SPICE đã là reward tối ưu.
3. **Đóng góp nghiên cứu khả dĩ**: một cơ chế *reliability-conditioned*, *sparse-aware*, *action-aware* semantic reward cho **natural-language GUI instructions**; giữ SPICE, thay đổi cách đo khi parser thiếu tín hiệu và chỉ bật verifier khi nhãn đáng tin. Đây là **đề xuất thích nghi phương pháp**, không phải tuyên bố phát minh action reward hay weighted SPICE.
4. **Ứng viên chính**: `R4 — Action-Conditioned Sparse-SPICE (ACSS)`; mở rộng `R6/R7` với target contrast và reliability mask **chỉ khi** giải quyết được nhiễu descriptor. Đối chứng quan trọng nhất: SPICE, SPIDEr, SPICE+gate, SPICE+fallback, SFT continuation, SCST+SPICE.
5. **Lựa chọn “reward tốt nhất”** phải dùng validation/holdout chưa xem, nhiều seed, kiểm soát đầy đủ pipeline, báo riêng tap / non-tap / target correctness, và hiệu chỉnh khi có nhiều phép so. Không lấy cực đại trên test đã được quan sát như bằng chứng xác nhận.
6. **Đóng góp chỉ được kết luận sau ablation.** Nếu không cải thiện hoặc SCST/SPIDEr thắng, nên báo cáo trung thực kết quả âm và giới hạn, không giữ tên “ours” bằng mọi giá.

### Những câu tuyệt đối không nên nói ở buổi bảo vệ lúc này

- “GRPO tốt nhất vì phổ biến hơn PPO/ORPO”.
- “SPICE có tương quan với executability cao hơn CIDEr-D/METEOR”. Thực nghiệm của chính Thesis **ngược lại**.
- “GRPO-SPICE cải thiện chọn đúng phần tử ổn định qua các seed”. Phần target gain chưa tái lập.
- “+1,55 pp chứng minh RL tốt hơn SFT tiếp”. Chênh `ck500 − SFT tiếp` chỉ +0,49 pp, CI bao gồm 0.
- “Tự nhiên một reward có nhiều thành phần hơn là đóng góp mới”. FoCUS, UI-R1, iSPICE, SC-Captioner, SPIDEr, GDPO đã có các cơ chế liên quan.

---

## 1. Định nghĩa bài toán và đường dữ liệu hiện tại

Đầu vào mỗi bước là `x = (I, goal, history, OCR)`, đích là câu hướng dẫn tự nhiên `g` của người. Mô hình `πθ(y|x)` sinh một câu `y` để người dùng/grounder hiểu **động tác và phần tử cần tương tác**. Về mặt đánh giá, một grounder đọc `I+y` để suy ra vị trí; evaluator chấm loại action, vị trí/phần tử, mâu thuẫn toggle. **Đây là executability surrogate dựa trên mô hình định vị**, không phải tỷ lệ người dùng thực hiện thành công trên thiết bị.

### 1.1 Các file then chốt đã đối chiếu

| Nguồn trong repo | Vai trò |
|---|---|
| `harness/grpo_spice.py` | Cấu hình ck500 gốc, reward SPICE + length penalty, LoRA merge, resume |
| `harness/grpo_luoi.py` | Các thuật toán `grpo/drgrpo/rloo/reinforce/scst`; các reward `spice/cider/rougel/meteor/chrf/bertscore/spider` |
| `harness/thuong_moi.py` | `spice_cong`, `ten_loai`, `loai`; các selftest hiện có |
| `harness/thuong_t6.py` | `spice_kp` (SPICE thuần), `phat_dai` (chỉ length penalty) |
| `harness/h2_thuong.py`, `harness/thuong_dac_tinh.py` | Kiểm reward offline trên 8 mẫu C1, concordance, reward tie, zero-gradient |
| `harness/grpo_ppo.py` | PPO/A2C variant với đầu giá trị MLP nhỏ, **không phải full critic** |
| `harness/grpo_moi_b4.py` | ORPO online/offline, DPO semi-online, GPG, xây trên pipeline lưới |
| `harness/metric_exec.py` | Action canonicalization + Voronoi/box-based executability; bug `go back` mặc định |
| `harness/build_branch_data.py` | Prompt dùng chung; system instruction hiện thiên về “chạm” |
| `report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md` | Kết quả mới nhất đến 08/11, đặc biệt §16–21 |
| `report/328_DANH_GIA_GRPO_SPICE_VA_THUYET_PHUC_1_11.md` | Phản biện khả năng khẳng định GRPO-SPICE tốt nhất |
| `report/330_KHAO_SAT_DO_DO_THAY_SPICE_1_11.md` | Stress test các metric/reward và khảo sát tài liệu |
| `report/323_DEBATE_VA_ACTION_KHAO_SAT_GRPO_SPICE_ACE_1_11.md` | Câu hỏi của thầy và đề cương lưới so sánh |
| `thesis/chapters/ch4_phuongphap.tex`, `ch6_thucnghiem.tex` | Cách luận văn đang kể câu chuyện; chưa đồng bộ toàn bộ phát hiện ngày 08/11 |

### 1.2 Cấu hình baseline phải giữ đúng

- Base policy: **S1/101** từ Qwen2.5-VL-3B-Instruct, SFT với LoRA. Merge adapter S1 vào backbone; gắn **LoRA mới** có LoRA-B khởi tạo 0. Bởi vậy policy ban đầu và KL reference trở về **S1**, không phải Qwen gốc.
- 1.000 prompt train từ 4.000 prompt P1 hợp lệ; chia theo episode để không trùng tập val. Trong 1.000 prompt ck500: **630 tap, 120 scroll, 81 input, 69 wait, 65 open app, 35 back** (`report/320` §16). Không được nói mô hình chưa được train trên scroll.
- `G=8`, 2 prompt × 8 completion cho một bước cập nhật, 500 optimizer steps, temperature 1.0, max 96 completion tokens, LR `1e-5`, KL `β=0.04`, length penalty `0.02`, gradient norm 1.0; pipeline TRL dùng loss kiểu **DAPO** (token aggregation), `num_iterations=1` theo log/khảo sát repo.
- Reward gốc (câu rỗng = 0):

  \[
  r_0(y,g)=\operatorname{SPICE}(y,g)-0.02\max(0,L(y)-L(g)-3).
  \]

- Action cùng nghĩa trong văn bản (`click`/`tap`/`open` ở nhiều ngữ cảnh) cần xử lý nhất quán; `metric_exec.canon_action` default có lỗi biết trước với `go back`, còn `strict_back=True` sửa một phần trong no-harm test. **Không dùng trực tiếp classifier này làm reward verifier trước khi audit độc lập.**
- System prompt hiện có câu “chỉ rõ cần chạm vào đâu”; với non-tap đây là confound khả dĩ. **Giữ prompt cố định** trong so reward; làm ablation prompt trung lập sau, tách biến.

### 1.3 Số kết quả phải thuộc lòng

Đơn vị `%` là tỉ lệ trên **4.463 bước tap**, `Δ` là *điểm phần trăm* (pp):

| Model / thuật toán | Tap executability | Ghi chú |
|---|---:|---|
| Base | 47,59 | Không SFT |
| S1/101 | **59,11** | Mốc chung |
| S1/202 | 59,62 | Seed SFT khác |
| `ck500` gốc GRPO+SPICE | **60,65** | +1,55 pp so S1/101; test paired CI [+0,80;+2,33] |
| `ck500/202` | 59,94 | Cùng phương pháp lịch sử, seed GRPO khác |
| A/A GRPO+SPICE (`grpo_luoi.py`) | **59,74** | +0,63 pp [−0,12;+1,37] so S1/101; không tái lập ck500 60,65 |
| SFT tiếp | **60,16** | Không RL; ck500 − SFT chỉ +0,49 [−0,09;+1,07] |
| SCST+SPICE | **60,54** | Trong cùng lưới, hơn A/A +0,81 pp, p Holm 0,009 |
| GRPO+ROUGE-L | **60,63** | Trong cùng lưới, hơn A/A +0,90 pp, p Holm 0,009 |
| GRPO+METEOR | 60,27 | +0,54 so A/A, chưa rõ vượt sau hiệu chỉnh |
| GRPO+CIDEr-D | 60,27 | +0,54 so A/A, chưa rõ vượt sau hiệu chỉnh |
| REINFORCE+SPICE | 60,00 | +0,27 so A/A, chưa rõ |
| RLOO+SPICE | 59,44 | −0,29 so A/A, chưa rõ |

**Cực kỳ quan trọng:** cùng reward SPICE, ba GRPO checkpoint có SPICE text **45,69–46,00**, nhưng tap exec **59,74–60,65**. Có thể tối ưu tốt metric mà không đạt tương đương ở task metric; khác biệt từ seed/môi trường và xử lý target là đáng kể. `ck500` gốc và A/A khác pipeline/phiên bản GPU; mọi so thuật toán trong lưới nên dùng A/A cùng pipeline làm đối chứng.

**Tác dụng phụ:** Trên 2.495 bước non-tap, `ck500` giảm action accuracy toàn bộ **85,97 → 84,29** (−1,68 pp); **scroll 83,97 → 77,75** (−6,23 pp); `navigate_back` 72,96 → 67,04 (−5,93 pp). Mốc kiểm scroll −3 pp đã bị vi phạm (`report/262`, `report/320`). Ở toàn bộ 6.958 bước, số tổng hợp *tap exec + non-tap action accuracy* của ck500 so S1 khoảng **+0,39 pp, CI [−0,21;+0,99]**. Đây là hai định nghĩa thành công khác nhau; nếu cộng, **bắt buộc giải thích cách tính và báo hai cấu phần riêng**.

**Phân rã target/action:** ck500/101 ròng +28 bước sửa action và +41 bước sửa target; seed 202 +32/+5, A/A +20/+8. **Lợi ích về target không tái lập**, tác dụng sửa action lặp lại hơn. Đo thị giác qua UGround có giới hạn; không gọi là tỷ lệ tác vụ thực hoàn thành.

---

## 2. Paper map — kiểm chứng nguồn xuất bản, không đồng nhất bài toán

### 2.1 Tối ưu chính sách / sequence-level metric

| Paper [PAPER] | Đóng góp đã công bố | Hệ quả cho Thesis / giới hạn so sánh |
|---|---|---|
| DeepSeekMath (Shao et al., 2024, [arXiv 2402.03300](https://arxiv.org/abs/2402.03300)) | Giới thiệu GRPO thay value model riêng bằng reward-relative trong nhóm; bối cảnh toán | Cơ chế GRPO có nguồn gốc rõ, **không phải thuật toán mới của Thesis** |
| PPO (Schulman et al., 2017, [arXiv 1707.06347](https://arxiv.org/abs/1707.06347)) | Policy surrogate, clipping, nhiều vòng cập nhật trên batch | PPO là baseline thuật toán; không mặc định một PPO critic nhỏ đại diện mọi cấu hình PPO |
| SCST (Rennie et al., CVPR 2017, [CVF](https://openaccess.thecvf.com/content_cvpr_2017/html/Rennie_Self-Critical_Sequence_Training_CVPR_2017_paper.html)) | Policy gradient cho caption, reward greedy làm baseline | **Baseline quan trọng nhất** vì cũng sinh text và inference greedy |
| RLOO / REINFORCE revisit (Ahmadian et al., ACL 2024, [ACL](https://aclanthology.org/2024.acl-long.662/)) | Các thuật toán policy gradient đơn giản cạnh tranh PPO/DPO/RAFT trong RLHF | Không nói GRPO vượt RLOO về bản chất; phải so cùng reward |
| ORPO (Hong et al., EMNLP 2024, [ACL](https://aclanthology.org/2024.emnlp-main.626/)) | Preference optimization bằng odds-ratio kết hợp SFT, không cần reference model | Khác bài toán scalar online reward; có thể tạo ranked pairs nhưng mất thông tin độ lớn và phát sinh lựa chọn cặp |
| DPO (Rafailov et al., NeurIPS 2023, [NeurIPS](https://papers.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html)) | Tối ưu từ preference pair | Không được tuyên bố “DPO không thể dùng”; chỉ nói phải chuyển reward thành nhãn cặp |
| Dr. GRPO (Liu et al., COLM 2025, [COLM](https://proceedings.colm.cc/paper_files/paper/2025/hash/ecd8143eeaf83e6dc87ffcb683b0f81b-Abstract-Conference.html)) | Phân tích length bias và difficulty bias trong GRPO | Cần kiểm `scale_rewards`, normalization; “Dr. GRPO” trong script là **không chia std reward**, không nên đánh đồng với mọi thay đổi của paper |
| GDPO (Liu et al., ICML 2026, [PMLR](https://proceedings.mlr.press/v306/liu26aa.html)) | Chuẩn hóa riêng từng reward channel khi multi-reward GRPO | Nếu scalar combine thất bại, thử GDPO **như đổi thuật toán**, không gọi nó là reward mới |

### 2.2 Semantic metrics / caption reward

| Paper [PAPER] | Đã có điều gì | Ranh giới cần giữ |
|---|---|---|
| CIDEr (Vedantam et al., CVPR 2015, [CVF](https://openaccess.thecvf.com/content_cvpr_2015/html/Vedantam_CIDEr_Consensus-Based_Image_2015_CVPR_paper.html)) | TF-IDF n-gram consensus; CIDEr-D | Mạnh về phân biệt tên/đoạn câu nhưng phụ thuộc corpus DF và câu tham chiếu |
| SPICE (Anderson et al., ECCV 2016, [paper](https://mlanthology.org/eccv/2016/anderson2016eccv-spice/)) | So F1 semantic propositions/object/attribute/relation | Gốc là caption evaluation, **không mô hình hóa đúng thao tác GUI** |
| SPIDEr (Liu et al., ICCV 2017, [CVF PDF](https://openaccess.thecvf.com/content_ICCV_2017/papers/Liu_Improved_Image_Captioning_ICCV_2017_paper.pdf)) | Tối ưu combination SPICE + CIDEr bằng policy gradient | Baseline reward lai **bắt buộc**; cộng SPICE với một metric không mới |
| SPICE-U (Wang et al., ECCV 2020, [ECVA PDF](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123520613.pdf)) | Uniqueness-weighted semantic concepts | Cẩn thận: hiếm không đồng nghĩa đúng/quan trọng đối với GUI |
| iSPICE (Raajesh et al., CVPR 2024, [CVF](https://openaccess.thecvf.com/content/CVPR2024/html/Raajesh_MICap_A_Unified_Model_for_Identity-Aware_Movie_Descriptions_CVPR_2024_paper.html)) | Nhấn mạnh identity tuples trong movie description | Chứng minh identity-sensitive metric đã có; GUI target contrast phải khác rõ |
| SC-Captioner (Zhang et al., ICCV 2025, [CVF](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_SC-Captioner_Improving_Image_Captioning_with_Self-Correction_by_Reinforcement_Learning_ICCV_2025_paper.html)) | Thưởng sửa thêm/bớt semantic facts qua scene graph set difference | Phạt thêm/bớt tuple không phải mới; đề tài cần nêu phiên bản GUI/nhãn tin cậy |
| CCCaption (Tang et al., CVPR 2026, [CVF](https://openaccess.thecvf.com/content/CVPR2026/html/Tang_CCCaption_Dual-Reward_Reinforcement_Learning_for_Complete_and_Correct_Image_Captioning_CVPR_2026_paper.html)) | Dual reward completeness & correctness, tránh hallucination | Multi-reward image captioning đã có; không claim novelty cho “hai reward” |
| FoCUS (Hyun et al., EMNLP 2026, [ACL](https://aclanthology.org/2026.emnlp-main.2622/)) | Prompt-conditioned object/attribute/relation score, cả negative weight, tối ưu GRPO | **Closest methodological prior** với graph-component reward; phải đối chiếu novelty cực nghiêm |

### 2.3 GUI / instruction-grounded evaluation

| Paper [PAPER] | Ý nghĩa và phạm vi |
|---|---|
| AndroidControl (Li et al., NeurIPS 2024, [NeurIPS](https://papers.nips.cc/paper_files/paper/2024/hash/a79f3ef3b445fd4659f44648f7ea8ffd-Abstract-Datasets_and_Benchmarks_Track.html)) | Nguồn dữ liệu UI control; có low-/high-level instructions; cho phép nêu rõ miền nhiệm vụ |
| On the Evaluation of Vision-and-Language Navigation Instructions (Zhao et al., EACL 2021, [ACL](https://aclanthology.org/2021.eacl-main.111/)) | SPICE có thể phù hợp **xếp hạng hệ thống** có reference, nhưng compatibility với quỹ đạo tốt hơn cho **đánh giá từng instruction**; là neo quan trọng cho “semantic ≠ executability” |
| UI-R1 (Lu et al., AAAI 2026, [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/38816)) | Rule-based action reward và GRPO cho GUI action prediction. **Action reward không mới**, nhưng output khác với hướng dẫn ngôn ngữ tự nhiên của Thesis |
| GUI-G1 (Zhou et al., NeurIPS 2025, [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2025/hash/89dcbea9f19960edd7765068adb13b1d-Abstract-Conference.html)) | Cảnh báo reward hacking theo kích thước box, độ khó sample và length; không dùng grounder một cách ngây thơ |
| CapRL (Xing et al., ICLR 2026, [ICLR](https://proceedings.iclr.cc/paper_files/paper/2026/hash/15f1dbc086bfd94d8c32557b573cbe18-Abstract-Conference.html)) | Caption được chấm bằng khả năng hỗ trợ mô hình không nhìn ảnh trả lời câu hỏi; ý tưởng listener utility có tiền lệ |

**Mức độ nguồn:** các URL trên dẫn tới paper chính thức / bản tác giả tại nguồn hội nghị hoặc arXiv được chỉ rõ. Chúng cho **động cơ và cơ chế**, không phải bằng chứng một thuật toán vượt trên AndroidControl của Thesis. Không chuyển phần trăm từ COCO/ScreenSpot sang phát biểu về GUI instructions.

---
## 3. Debate A — Tại sao RL? Tại sao GRPO, không phải các lựa chọn khác?

### 3.1 SFT so với reward optimization: luận điểm đúng và sai

SFT tối ưu token likelihood của câu gold: `L_SFT = −log πθ(g|x)`. Một screenshot/goal có thể có nhiều câu đều hướng đến cùng hành động (chẳng hạn “Tap Settings” / “Open Settings”). SFT tối ưu một văn bản tham chiếu duy nhất, không tối ưu trực tiếp thước đo không khả vi của các câu tự sinh. Policy gradient tối ưu kỳ vọng reward theo **cả câu**: `J(θ)=E_{x,y~πθ}[r(x,y)]`; đạo hàm score-function đưa tín hiệu sequence-level xuống token. Đó là **lý do nghiên cứu RL**, không phải chứng minh RL luôn hơn CE.

**Phản biện của thầy:** “Nếu chỉ train thêm 500 bước SFT cũng được 60,16 mà ck500 được 60,65, vậy RL đóng góp gì?”  
**Trả lời hợp lệ:** “Hiện chưa đủ chứng cứ RL hơn SFT tiếp. Chênh +0,49 pp có CI chứa 0. Em dùng continuation SFT cùng prompt, optimizer/update budget làm baseline mạnh; nếu reward mới không vượt bằng phép thử xác nhận thì không quy kết lợi ích cho RL.”

### 3.2 Vì sao GRPO được chọn làm algorithmic substrate?

Với nhóm `G=8` câu cho cùng `x`, trong cấu hình hiện tại:

\[
 r_i=r(x,y_i),\quad
 \widehat A_i=\frac{r_i-\bar r_x}{s_x+\epsilon},\quad
 \bar r_x=\frac1G\sum_{i=1}^{G}r_i.
\]

Các lợi thế thực dụng:

1. **Không phải học critic/value model** như PPO truyền thống; phù hợp VLM 3B với tài nguyên T4/L4.
2. **So cùng trạng thái GUI**: baseline theo prompt có thể loại phần sai khác độ khó giữa các màn hình; nếu chỉ dùng global mean, câu của màn dễ/dễ được thưởng cao hơn câu màn khó.
3. **Dùng reward nondifferentiable** như Java SPICE, CIDEr-D, `canon_action` mà không phải backprop qua scorer.
4. **Có code và thiết bị chấm đáng tin hiện hữu**, cho phép giải thích gradient và reward logs trên đúng dữ liệu.

Những điểm này **không đủ** để nói GRPO hơn SCST/RLOO/PPO về kết quả. Hơn nữa bản đang chạy `loss_type=dapo`, `num_iterations=1`; nếu số vòng cập nhật một minibatch chỉ là một thì clipping không phải động cơ khác biệt như nhiều-epoch PPO. Chỉ nên mô tả **group-normalized policy gradient + KL-to-S1** là hiệu ứng chủ đạo, kèm đúng tên cấu hình TRL. Độ dài completion, clipping/truncation, reward variance và KL phải có bảng log.

### 3.3 Ma trận đối chất thuật toán (tất cả giữ reward SPICE gốc)

| Thuật toán | Advantage / training signal | Điểm mạnh chính | Đòn phản biện | Phép kiểm cần làm |
|---|---|---|---|---|
| SFT tiếp | Cross-entropy trên câu người | Baseline chi phí thấp, mạnh về học khuôn/cách diễn đạt | Không trực tiếp tối ưu reward câu sinh | Same exposure + same model/LoRA |
| REINFORCE | `A=r−b_global` hoặc EMA | Đơn giản, ít machinery | Mốc không theo độ khó prompt, variance | Log std/grad norm/kl |
| RLOO | `A_i=r_i−mean(r_{−i}) = G/(G−1)(r_i−mean_group)` | Không critic, gần GRPO | Không chia std → khác scale reward/clip grad, không phải “chỉ đổi baseline” | Có `K1 = group mean không chia std` để nối so công bằng |
| **GRPO** | `(r_i−mean_group)/(std_group+ε)` | Prompt-relative, dễ dùng scalar reward | Zero-gradient nhóm hòa; khó khi std quá nhỏ; difficulty bias | `frac_zero_std`, ranking, gradient clipping, β, all-tap/all-scroll |
| Dr. GRPO variant | `r_i−mean_group` (theo script) | Không chia std, ít nhạy difficulty bias | Còn khác loss normalization của paper gốc | Ghi tên chính xác và bản loss được dùng |
| SCST | `r(sample)−r(greedy)` | Baseline gắn với greedy inference; tiền lệ captioning | Cần thêm một greedy generation mỗi prompt; nhiều sample A=0 | So same prompts + thực tế rollout/reward-call/time |
| PPO variant | Learned value/GAE; multiple iterations có thể dùng clip thật | Có baseline value và cập nhật nhiều lần | Chi phí và lỗi critic, repo chỉ có MLP nhỏ | Kiểm value loss, VRAM, μ, sample exposure |
| ORPO/DPO | Trích preferred/rejected từ reward; odds/DPO loss | Không cần online critic; phù hợp preference data | Biến reward liên tục thành cặp; nếu 8 câu giống nhau, ít cặp hữu ích; ORPO code là biến thể online/offline | Pair coverage; chosen/rejected reward gap; số prompt có cặp |

**Debate chốt:** “Vì sao GRPO?” → *Vì phù hợp bài toán, dữ liệu và tài nguyên để làm thuật toán chính; phép so thực nghiệm xác định nó cạnh tranh đến đâu.* Không thể dựa vào độ phổ biến, thứ tự năm xuất bản hay một lượt ck500 cao để loại SCST. Nếu SCST thắng sau nhiều seed, **nên báo SCST thắng**; đóng góp reward vẫn có thể đứng riêng nếu được đánh giá tiếp trên cả GRPO và SCST.

### 3.4 Quan điểm phản biện về “sự phổ biến”

Cách nói “GRPO phổ biến bởi DeepSeek-R1” chỉ là **bối cảnh ngành**, không phải bằng chứng khoa học trong task này. Thầy có thể hỏi: “Nếu có RLOO tương đương mà rẻ hơn, em chọn GRPO làm gì?” — câu trả lời đúng phải dùng **trade-off đo được**: cùng data/budget, exec, action/target error, runtime, peak VRAM, tỉ lệ nhóm không có advantage, seed variability. Tên thuật toán không đủ để thay số liệu.

---

## 4. Debate B — Vì sao SPICE? Thước câu khác có thể tốt hơn ở chỗ nào?

### 4.1 Chỗ SPICE có lý do khoa học

SPICE trích tuple semantic của `y` và `g`: object, attribute, relation; tính F1 trên tập các proposition khớp. Thay `Click on the Settings icon` bằng `Tap Settings` vẫn có thể giữ những thành phần ngữ nghĩa quan trọng dù n-gram thay đổi. SPICE là một chỉ báo **semantic content** đáng cân nhắc cho instruction, đặc biệt khi tham chiếu chỉ có một câu.

**Nguồn độc lập quan trọng nhất ngoài captioning:** Zhao et al. (EACL 2021) gợi ý SPICE để xếp hạng **hệ thống sinh navigation instructions** nếu có references, trong khi mô hình compatibility instruction–trajectory dự đoán **mức instruction** tốt hơn. Điều này ủng hộ **chọn SPICE làm điểm xuất phát**, đồng thời trực tiếp dự báo giới hạn của SPICE nếu mục tiêu của Thesis là executability từng bước.

### 4.2 Phản biện nặng nhất đến từ chính dataset, không phải paper

`report/330` stress test 400 câu đã làm phép đổi action mà giữ từ vựng/đối tượng: SPICE còn khoảng **0,919** với biến thể `Swipe up on ...` sai action và **0,945** với `Go back from ...` sai action. Điều đó cho thấy **động từ action gần như không nằm trong proposition của SPICE**. Câu chuẩn `Scroll down` và `Go back` tự so có thể được 0 vì không có tuple. `report/320` §17: 29,4% câu scroll đúng loại và 37,0% câu back đúng loại của những lát đo có SPICE = 0. Đây là bằng chứng cơ chế, không phải giả thuyết thuần túy.

Trên dữ liệu C1 có 8 candidate S1 cùng một prompt (`report/320` §16, **chỉ validation**):

| Reward | Nhóm reward bằng nhau | Cặp câu hòa | Concordance với exec trên cặp khác exec |
|---|---:|---:|---:|
| METEOR | 1,6% | 17,7% | **0,871** |
| CIDEr-D | 1,6% | 15,4% | **0,868** |
| SPIDEr | 1,6% | 15,4% | 0,824 |
| SPICE + action gate | 7,2% | 38,0% | 0,704 |
| **SPICE** | **7,2%** | **38,2%** | **0,685** |
| Chỉ action type | 45,8% | 76,3% | 0,620 |

**Điểm mấu chốt:** Điểm ranking trên câu tĩnh **không dự đoán được thứ tự checkpoint sau RL**. Các lưới thực nghiệm mới cho GRPO+SPICE ngang/nhỉnh vài cấu hình theo một số metric, nhưng có biến thiên seed lớn; không nên tự biện luận “reward concordance cao tất thắng”. H2 chỉ là phép lọc và giải thích, không thay việc train.

### 4.3 So sánh đúng các họ metric

| Metric | Đo tốt điều gì | Yếu gì cho GUI | Vai trong luận văn |
|---|---|---|---|
| **SPICE** | Semantic object/attribute/relation ít nhạy đổi khuôn | Zero tuple, động từ action, tên riêng không ổn định, quan hệ parser thiếu | **Semantic anchor** cho nghiên cứu reward |
| **CIDEr-D** | TF-IDF n-gram, phạt lặp; nhạy khác biệt tên phần tử | IDF cần kho train; một reference hạn chế tính consensus; dễ khớp khuôn | Baseline mạnh bắt buộc |
| **METEOR** | Unigram alignment, stem/synonym | Action paraphrase GUI có thể không được xem là đồng nghĩa; chấm Java tốn chi phí | Baseline mạnh với H2 cao nhất |
| **ROUGE-L** | LCS, ổn định cho câu ngắn | Câu theo khuôn có thể được điểm cao dù target sai | Baseline thực nghiệm đang cạnh tranh mạnh |
| **BLEU-4** | Chính xác n-gram 1–4 | Câu 4–7 từ dễ thiếu 4-gram, cần smoothing | Kiểm hệ n-gram, không ưu tiên final |
| **chrF** | N-gram ký tự, có tín hiệu ngay với câu ngắn | Không đảm bảo tương đương nghĩa của paraphrase; dễ bị sai tên gần giống | **Fallback** hợp lý nhưng phải stress-test |
| **BERTScore** | Similarity embedding/contextual | Dễ cho điểm cao câu sai target/vị trí vì gần ngữ nghĩa | Đối chứng embedding, đắt hơn |
| **SPIDEr** | SPICE + CIDEr-D | Vẫn phụ thuộc reference; không có hard semantic action | **Closest classical hybrid baseline** |

### 4.4 Khi thầy hỏi “Vì sao không chọn CIDEr hoặc METEOR luôn?”

**Đừng trả lời:** “SPICE tốt hơn vì chú trọng ngữ nghĩa” — rất dễ bị H2 phản bác.  
**Nên trả lời:** “Công trình của em đặt câu hỏi về khả năng *thích nghi một semantic reward dựa trên SPICE cho GUI*; vì vậy SPICE là lựa chọn nghiên cứu có lý do. CIDEr/METEOR/ROUGE-L được giữ làm đối chứng mạnh để biết cải tiến có thật sự đáng dùng không. Nếu reward khác thắng, em không tiếp tục khẳng định SPICE đứng đầu. Cần phân biệt lý do chọn *đối tượng nghiên cứu* với kết luận *hiệu quả thực nghiệm*.”

Điều này giữ tính trung thực, đồng thời vẫn có một thesis research question có hướng thay vì “thử tất cả rồi kể câu chuyện cho winner”.

---

## 5. Đề xuất **một họ reward SPICE có ablation**, thay vì chốt sớm một công thức

**Ký hiệu:** `x` là ảnh/goal/history/OCR/training annotation của một bước; `g` là một reference instruction; `y` là câu được sinh; `s(y,g)=SPICE_F(y,g) ∈ [0,1]`; `c(y,g)=chrF(y,g)/100 ∈ [0,1]`; `d(y,g)=min(0.05, 0.02·max(0,words(y)−words(g)−3))`; `T(g)` là tuple được SPICE parser tạo từ `g`. Câu rỗng luôn reward = 0. Không đưa gold/test annotation vào inference; reference/ground truth chỉ tham gia **training reward**.

### 5.1 Danh mục reward tối thiểu phải so

| ID | Công thức / mô tả | Tín hiệu mới so R0 | Mục đích, giả thuyết | Rủi ro |
|---|---|---|---|---|
| **R0** | `s − length_penalty_gốc` | Không | Baseline ck500 / A/A | Sparse/action blind |
| **R1** | `0.5·s + 0.5·CIDEr-D/10 − d` (SPIDEr theo scale lưới) | N-gram TF-IDF | Reward lai cổ điển đủ hay chưa? | Không trực tiếp xác minh action |
| **R2** | `q_sparse − d` với `q_sparse` tại §5.2 | Sparse fallback, chưa gate | Cứu câu không có tuple có ích độc lập không? | chrF có thể thưởng trùng chữ sai nghĩa |
| **R3** | **R3-Hard:** cùng `c_a`, bonus `0.2`, hard gate và penalty của R4 nhưng thay `q_sparse` bằng `s`. **R3-Soft:** `spice_cong` sẵn có, giữ làm baseline lịch sử riêng | Action-only trong so sánh nhân quả | Sửa action một mình đủ không? | `s=0` vẫn không có tín hiệu |
| **R4** | **Action-Conditioned Sparse-SPICE (ACSS)** dưới đây | Sparse fallback + action gate | Ứng viên **ưu tiên đầu tiên** | Cần action verifier và lượng gradient đủ |
| **R5** | R4 + rarity-weighted tuple score (SPICE-U inspired) | Giảm thưởng khuôn phổ biến | Hữu ích cho AitZ có nhiều tuple phổ biến? | Rarity ≠ relevance; parser nặng |
| **R6** | R4 + target contrast trên screenshot | Đúng phần tử trong các câu cùng action | Cứu target gain qua seed? | Descriptor/target label nhiễu |
| **R7** | R6 + **reliability mask** để bỏ contrast khi dữ liệu yếu | Chỉ tin target có đủ bằng chứng | Reliability conditioning > fixed sum? | Ít mẫu bật contrast; power thấp |
| **R8** | R4 thay `chrF` bằng `CIDEr-D/10` hoặc METEOR | Tách tác dụng của fallback choice | Tránh kết luận chọn chrF theo trực giác | Chạy thêm nhiều cấu hình |
| **R9 (extension)** | R4 các channel tách riêng theo GDPO | Thay advantage normalization | Nếu scalar reward collapse | **Đây là đổi thuật toán**, không phải so reward đơn thuần |

**Phép kiểm riêng về phạt độ dài:** thêm `R0-no-length` (chỉ SPICE, câu rỗng = 0), và `R0-capped-length`. Đây là ablation phụ, không dùng lại ID R2 vì R2 đã dành cho sparse fallback.

Không nên đưa toàn bộ 10 ô vào một lưới GPU ngay. Ưu tiên đo offline R0/R1/R3/R4/R5/R6/R7, chọn tối đa 3–4 finalist rồi mới train full. R8 và R9 chỉ mở khi H2/stress test chỉ rõ lí do.

### 5.2 R4 — Công thức lõi **Action-Conditioned Sparse-SPICE (ACSS)**

**Bước 1: cứu sự thiếu semantic tuple:**

\[
 w(g)=0.8\min(1, |T(g)|/3),\qquad
 q_{\mathrm{sparse}}(y,g)=w(g)\,s(y,g)+[1-w(g)]\,c(y,g).
\]

- `|T(g)|=0` → trọng số SPICE = 0, dùng chrF. Vì thế `Scroll down` khớp chính nó **được thưởng**, thay vì `SPICE=0`.
- 1–2 tuple → sử dụng cả hai tín hiệu; ≥3 tuple → SPICE tối đa 80%, chrF 20%.
- Các hệ số `0.8`, `3` là **giả thuyết**, không được phát biểu như giá trị học được từ dữ liệu. Nên thử grid rất nhỏ trên *validation* (`0.6/0.8` và ngưỡng `2/3`) **sau khi định sẵn**, không dò theo test.
- Tính `T(g)` từ **câu chuẩn của train** trước buổi training; cache theo key, tránh gọi parser nhiều lần. Bảo đảm `spice_batch` không bị thay/loại trong path production.

**Bước 2: action reliability:**

- `a*(x)` là action label đáng tin của bước train, **không mặc định** bằng `canon_action(g)` nếu dữ liệu log và câu người bất đồng.
- `â(y)` là action suy ra từ câu sinh bằng bộ xác minh có nhãn `unknown` và rule priority riêng. `go back`, `press back`, `navigate back` phải tách khỏi `open X`; `swipe up` và `scroll down` có thể đồng nghĩa về hiệu ứng nội dung màn hình tùy khung mô tả; `wait`, `open_app`, `input_text` phải xử lý rõ.
- `c_a(x)∈{0,1}` là **độ tin cậy của nhãn vàng** (gold action và gold instruction thống nhất / xác minh thủ công hoặc bằng quy tắc được kiểm trên holdout). Rule về `c_a` được định trước, phụ thuộc **chỉ vào x/g/annotation của train**, không phụ thuộc output test hay evaluator UGround.

**Bước 3: reward scalar:**

\[
 R_{\mathrm{ACSS}}(y,x)=
 \begin{cases}
 0, & y=\varnothing,\\
 \max(0,\;0.2+0.8q_{\mathrm{sparse}}-d), & c_a=1,\;\hat a(y)=a^*,\\
 0, & c_a=1,\;\hat a(y)\ne a^*,\\
 \max(0,\;q_{\mathrm{sparse}}-d), & c_a=0.
 \end{cases}
\]

**Lý do thiết kế từng thành phần:**

1. `q_sparse` giữ semantic F1 của SPICE nhưng tránh **parser-caused zero reward**.
2. `action gate` không cho câu sai action nhận điểm cao vì trùng object. Trong nhóm có cả câu đúng và sai action, nó tạo khoảng cách rõ ràng mà chỉ nhân `SPICE × 0.1` không làm được khi SPICE=0.
3. `c_a` tránh phạt oan khi nhãn loại thao tác của log và câu tham chiếu bất đồng (đã có dấu hiệu ở wait/open_app trong repo).
4. `d` chặn reward hacking bằng kéo dài câu. **Đây là length penalty có trần**, khác bản gốc; phải tách nó trong ablation, không lén thay nhiều biến.

**Lỗ hổng phải trình trước khi bị hỏi:** Nếu **cả 8 câu đều sai action**, reward đều 0 → không có advantage giúp policy phục hồi. Không sửa bằng cách nhân mọi reward sai action 0,01 vì **group normalization triệt tiêu hệ số chung**; phải kiểm tỷ lệ nhóm all-wrong và nếu lớn thì nghiên cứu `soft gate` có chấm mức lỗi hành động hoặc hỗn hợp CE có kiểm soát. Cả hai là **nhánh nghiên cứu riêng**, phải giải thích khác R4. Khi classifier dự đoán `unknown`, cần quy tắc bảo thủ (bỏ gate hoặc đánh giá confidence) được khóa trước để không phạt sai một cách âm thầm.

### 5.3 R6/R7 — Verified target contrast (*chưa phải công thức lõi*)

Nhãn phần tử lấy từ train annotation/OCR/accessibility/candidate inventory, **không** từ UGround ở tập test. Đặt `t+` = phần tử đích có chứng cứ, `N(x)` = tên/mô tả các phần tử cạnh tranh khác hiện trên ảnh, `M(y,t)∈[0,1]` = điểm tên/định danh có kiểm chứng từ câu `y` tới `t`:

\[
 D(y,x)=\max\bigl(0,\;M(y,t^+)-\max_{t^-\in N(x)}M(y,t^-)\bigr),
 \quad
 q_{\rm target}=(1-\eta m(x))q_{\rm sparse}+\eta m(x)D(y,x)
\]

với `η=0.25` là **giả thuyết**, `m(x)∈{0,1}` là reliability mask **được dựng không dùng output y**. Thay `q_sparse` trong R4 bằng `q_target`. Bản R6 cố định `m=1` ở tất cả bước có descriptor; R7 mask theo độ tin cậy. So R6−R7 kiểm **giá trị của reliability**, không chỉ giá trị của tên.

**Những điều kiện bật mask đề xuất** (tất cả kiểm bằng train-only/validation và cần chốt rule cụ thể): gold target có tọa độ/box nhất quán với candidate; tên descriptor không mơ hồ, đủ ngữ nghĩa; tên/alias của nó xuất hiện hoặc tương đương với câu chuẩn; có ít nhất một phần tử đối thủ hợp lệ để kiểm contrast; không phải dạng icon vô danh. Nếu nhiều điều kiện quá chặt khiến m bật ở rất ít bước, phải báo **coverage** và lợi ích theo coverage, không thổi phồng kết quả toàn tập.

**Cảnh báo từ repo:** ở 181/249 bước tap C1 có tên vàng, 29% câu chuẩn đã có `F1_tên=0` (`report/320` §16). Reward target-only sẽ phạt oan câu gold, một sai lầm nghiêm trọng. Trước khi dùng R6/R7 cần công bố **false-rejection rate trên chính câu gold** và random negative, không chỉ `target F1`.

**Cảnh báo novelty:** iSPICE đã có identity tuples; FoCUS đã có component-weighted scene graph và negative weights; SC-Captioner đã có semantic correction penalty. Vì thế novelty nếu có chỉ là **định nghĩa reliability/contrast chuyên cho GUI instruction với nhãn thiếu chắc chắn**, và phải được chứng minh bằng đối chứng **fixed-weight**/always-on/never-on, không phải “người đầu tiên đưa identity vào reward”.

### 5.4 R5 — SPICE-U inspired rarity để xử lý “tuple khuôn”

Tính `df(t)` trong **training gold corpus**; `u(t)=log[(N+1)/(df(t)+1)]` rồi clip/normalize. Thay semantic F1 bằng `weighted F1(T(y),T(g);u)`, hoặc giữ SPICE F và thêm bonus nhỏ cho khớp tuple hiếm. So tuple hiếm/phổ biến trên AitZ **chỉ là động cơ**: không bảo đảm tuple hiếm chỉ phần tử đúng; hiếm cũng có thể là lỗi parser/hallucination. Phải so `R5` với `R4` và đo cụ thể target discrimination; nếu không thêm ích lợi, loại R5.

### 5.5 Một ví dụ minh họa, không phải điểm reward thật

Gold: `Scroll down`. Ứng viên: A=`Scroll down`, B=`Swipe up`, C=`Click on the down arrow`. SPICE có thể 0 cho A/B; với C nếu parser tạo tuple, SPICE có thể cho điểm dương dù sai action. R0 thiếu tín hiệu; R3 chỉ nhân/gate vẫn không cứu A/B nếu SPICE=0; **R4 tạo reward cho A và một phần cho B qua chrF, đồng thời loại C khi action verifier đáng tin**. Tuy nhiên chrF có thể phạt oan B (paraphrase khác mặt chữ); stress test phải so riêng các cặp synonym/contrary: `swipe up` vs `scroll down` tùy ngữ cảnh, `go back` vs `return to previous screen`, `tap` vs `click`.

Gold: `Click on Cancel`, trên màn có `Cancel` và `Delete`. R4 có thể vẫn nhầm nếu parser/chrF không tách rõ; R6/R7 thêm target contrast để phạt `Click on Delete`, **nhưng chỉ ở bước có target label đủ tin**. Tính chất **có điều kiện** này cần là đóng góp đo được, không chỉ sơ đồ hợp lý.

---
## 6. Phản biện toán học: một reward nhìn “hay” vẫn có thể vô dụng với GRPO

### 6.1 Group normalization triệt tiêu affine scaling

Với một nhóm phần thưởng `r_i`, nếu áp dụng `r_i' = a·r_i+b` với cùng `a>0,b` cho tất cả i, thì `(r_i'−mean(r'))/std(r') = (r_i−mean(r))/std(r)` khi bỏ qua `epsilon`. Vì vậy:

- **Cộng cùng một bonus cho mọi câu** trong nhóm không giúp GRPO phân biệt câu tốt.
- **Nhân cả nhóm bằng 0,1** cũng không có tác dụng làm gradient “nhỏ 10 lần” theo trực giác, trừ ảnh hưởng epsilon, clipping, loss khác.
- **Chỉ thay score tuyệt đối** không đủ; phải thay **thứ tự/độ phân biệt giữa câu tốt và sai** trong cùng nhóm hoặc thay cách chuẩn hóa/việc xuất hiện của nhóm có reward hữu ích.

`r=SPICE×action_gate` có thể thất bại nếu trong nhóm tất cả câu cùng loại thao tác; `r=SPICE+constant_bonus_for_correct_action` cũng chỉ khác biệt khi nhóm có cả đúng và sai action. Cần báo tỷ lệ nhóm mixed-action, all-correct, all-wrong theo từng action type.

### 6.2 Reward tie và zero-gradient

`report/320` §17: trong log train, **22,7% nhóm** của GRPO+SPICE `ck500` có mọi phần thưởng bằng nhau; với GRPO+CIDEr-D/METEOR/ROUGE-L là khoảng **16,2–16,7%**. Các con số này là **train log**, khác thống kê H2 trên val (7,2%). Không gộp hai bộ số.

Tác dụng của reward mới phải đo bằng:

- `frac_reward_zero_std`, `% all-wrong action groups`, `% all-correct action groups`.
- `% pairs tied`, `% wrong-action sample outranks correct-action sample`.
- `E[A_i·(exec_i−mean_exec_group)]` chỉ trên validation có exec label, và cho từng action.
- `grad_norm`, `% grad clipped`, KL-to-S1, length, output emptiness, hallucination, action distribution.
- Tách **chất lượng reward khi cho 8 mẫu S1 cố định** và **hiệu quả sau RL**. H2 từng không dự báo được thứ hạng checkpoint; cần kiểm chéo trước khi kết luận cơ chế.

### 6.3 Mối nguy “hard action gate”

Giả sử `x` là scroll và 8 câu lấy mẫu đều mở đầu bằng `Click`. Nếu gate gán 0 cho cả 8, GRPO không biết mẫu nào ít sai hơn. Lựa chọn khoa học không phải che lỗi bằng cách cộng một hằng số, mà là **pre-register một ablation**:

1. R4-Hard: action sai = 0 như công thức hiện tại.
2. R4-Soft: action sai nhận một tín hiệu *graded*, ví dụ độ tin cậy action classifier hoặc penalty theo nhầm loại hành động **đã định nghĩa trước**. Có rủi ro vẫn thưởng sai action.
3. R4-CE: hard gate + hệ số nhỏ SFT loss trên gold (đây là đổi **training objective**, không phải chỉ reward).
4. R4-Balanced: giữ reward nhưng lấy mẫu prompt theo type cân bằng hơn (đây là đổi **data distribution**).

Không so phiên bản vừa thay action verifier, vừa thay sampling, vừa thêm CE rồi nói hiệu quả đến từ SPICE. Nếu training recipe thay đổi, phải tách biến.

### 6.4 Reward hacking và annotation noise

- **Tối ưu vào scorer**: SPICE parser có thể bị khai thác bằng câu dài/khung lặp; chrF có thể bị khai thác bằng copy chuỗi trên màn mà sai hành động; `M` target có thể thưởng tên hiếm nhưng không đủ mô tả để định vị.
- **Annotation noise**: `wait` với gold phrase dạng tap, `open_app` có thể được verbalize như tap; nếu ép action log bất chấp reference sẽ phạt câu người. Bắt buộc có `unknown`/mask và manual audit.
- **Grounder conflict**: không dùng UGround (metric đánh giá) làm reward chính. Nếu sau này dùng listener độc lập, báo chi phí và đánh giá qua nhiều grounder; tránh training trực tiếp theo lỗi của một evaluator.
- **OOD**: AitZ có nhiều tuple khuôn phổ biến, SPICE tăng không đồng nghĩa exec tăng; đừng chọn winner trên AndroidControl rồi tuyên bố generalizes tới mọi GUI.
- **Token length**: length penalty có trần là đề xuất mới so với ck500; nếu cải thiện, phải biết bao nhiêu thuộc về thay penalty.

### 6.5 Trạng thái “cùng code cùng seed” chưa đồng nghĩa reproducible

`report/320` §21: train lại SPICE qua `grpo_luoi.py` cùng 500 step và prompt/seed ra 59,74 thay vì 60,65; code và version khác, CUDA kernel khác, và GPU sampling có thể nondeterministic. Trên CPU tiny model 8/8 đầu vào/RNG trùng, **không** chứng minh GPU 3B giống. Cần:

- `pip freeze` / version `torch`, `transformers`, `trl`, `peft`, `bitsandbytes`, CUDA, GPU type.
- Hash base+SFT merged weights, adapter, train prompt keys, tokenizer processor, prompt template, `SPICE.jar`, `PTBTokenizer`, CoreNLP/Java version.
- Seed cho **dataset permutation**, **generation**, **training initialization** ghi riêng; giữ *train prompt identity* cố định nếu muốn đo chỉ seed của RL.
- Log tập sample/reward đầu tiên nếu bộ nhớ cho phép, có `episode_id/step_id`, action type, 8 câu, 8 score, std/advantage; không upload dữ liệu bản quyền/PII ngoài môi trường được phép.
- Run A/A giữa các công thức trong **cùng môi trường và cùng checkpoint source**, không lấy một ck500 lịch sử làm group control chuẩn.

---

## 7. Protocol thí nghiệm đủ chặt để hội đồng tin

### 7.1 Các giả thuyết cần có khả năng bị bác bỏ

**H0 — Baseline:** `R0` là một reward có ích cho học metric SPICE nhưng không bảo đảm nâng executability một cách ổn định.  
**H1 — Sparse repair:** `R2` so `R0` giảm reward tie/zero-advantage ở bước zero-tuple, tăng hoặc giữ action accuracy scroll/back, không làm tap target giảm quá ngưỡng đã chốt.  
**H2 — Action conditioning:** `R4` so `R2` giảm false positive cho câu sai action và giảm non-tap regression; đồng thời **không làm tăng all-zero groups quá mức**.  
**H3 — Target contrast:** `R6/R7` so `R4` tăng đúng phần tử *khi cùng đúng action* và cải thiện có cùng chiều qua seed.  
**H4 — Reliability:** `R7` so `R6` giảm false rejection trên gold instruction và tăng/giữ target success; lợi ích phải rõ hơn fixed-weight/always-on contrast.  
**H5 — Thuật toán:** GRPO có trade-off chấp nhận được về chất lượng, cost, stability so với SCST/RLOO/PPO/SFT tiếp khi reward cố định. Không yêu cầu nó thắng tất cả.  
**H6 — SPICE làm nền:** SPICE-based winner có khả năng cân bằng semantic quality và hành vi task tốt hơn các baseline thay metric; nếu không thì ghi trung thực.

Không đặt giả thuyết “R7 chắc chắn tốt nhất”; giả thuyết này **không thể bị kiểm định một cách công bằng** nếu bắt đầu bằng việc chọn winner trên test.

### 7.2 Pha 0 — audit trước khi thay reward

- Dựng unit test độc lập cho action extraction: tap/click/press/select/open X, `go back`, `press back`, `navigate back`, `swipe up/down`, `scroll down/up`, `wait`, `type`, `open app`, câu không có động từ, câu chứa hai động từ; báo confusion matrix và tỷ lệ unknown.
- Kiểm nhãn vàng của train: log action, câu người, box/element. Báo `c_a=1` coverage theo action. Dùng mẫu thủ công đủ rộng theo từng loại (đặt trước mẫu và số lượng; không lấy chỉ các case reward thích).
- Kiểm `SPICE(g,g)` và `chrF(g,g)` theo action, tỉ lệ 0 tuple; manual check parser failures.
- Xác minh `spice_batch` đúng Java/cache/scale, `CIDEr-D` DF **chỉ từ train**, chrF là sentence-level đúng version.
- Kiểm target-label confidence, nhất là **gold false-rejection** của target-name F1; chưa đạt thì **loại R6/R7 khỏi shortlist**, không buộc train.

### 7.3 Pha 1 — offline reward diagnostics (0 GPU hoặc CPU/Java)

Tái sử dụng **C1 8 samples** (`harness/h2_thuong.py`) và xây một **counterfactual stress test** có kiểm soát trên train/val:

| Case | Gold | Câu biến đổi | Thứ tự reward mong muốn |
|---|---|---|---|
| Synonym | `Click Settings` | `Tap Settings` | Gần gold, không phạt sai action |
| Wrong action | `Click Settings` | `Swipe on Settings` | Phạt rõ |
| Zero tuple | `Scroll down` | `Scroll down` | Reward đúng > 0 và > câu sai |
| Navigation paraphrase | `Go back` | `Return to previous screen` | Không phạt nếu cùng nghĩa |
| Wrong target | `Click Cancel` | `Click Delete` | Câu đúng > câu sai |
| Target omission | `Click Cancel` | `Click the button` | Câu cụ thể > câu chung |
| Position swap | `Click top-right icon` | `Click bottom-left icon` | Câu đúng > câu sai khi có target evidence |
| Contradictory toggle | `Enable notifications` | `Disable notifications` | Phạt sai dù cùng nút |
| Noisy gold | Log `wait`, gold `Click Next` | `Click Next` | Không được “phạt chắc” khi nhãn mâu thuẫn |
| Excess length | `Tap X` | `Tap X, ...` thêm chi tiết không kiểm chứng | Không dễ tăng điểm bằng kéo dài |

Metrics ở Pha 1:

1. `Exact-match reference reward` theo action: câu tự so không nên bằng 0 vì lỗi parser.
2. Fraction `gold < wrong action` trên stress set; action false reject rate theo sample audit.
3. Pairwise concordance, reward ties, zero-std group, oracle selection trên **cùng nhóm 8**; bootstrap theo episode, không dùng các số này làm kết luận test.
4. Reward ranking với paraphrase đúng, wrong target, wrong action, spurious location; số case bị đảo thứ tự.
5. Runtime reward/scorer, tần suất crash Java/timeout, memory; cache tuple references.

**Cổng đề xuất để ưu tiên train (không phải chuẩn khoa học bắt buộc):** reject reward nào làm câu gold bị phạt oan nghiêm trọng, không phân biệt đúng/sai action ở nhóm zero tuple, làm zero-std groups vượt R0 rõ ràng, hoặc cần target labels chưa đủ tin cậy. Chốt tiêu chí định lượng của cổng trên validation trước khi chạy reward full; không hậu nghiệm đặt ngưỡng để giữ phương án ưa thích.

### 7.4 Pha 2 — algorithm comparison: giữ reward R0

`A0` SFT continuation, `A1` GRPO gốc, `A2` SCST, `A3` RLOO, `A4` REINFORCE, `A5` Dr.GRPO, `A6` PPO variant, `A7` ORPO online/offline nếu vẫn còn ngân sách. **Không nhất thiết chạy lại** các kết quả đã có từ **cùng một môi trường khớp**, nhưng phải đánh dấu rõ các nhánh còn thiếu/khác model/khác budget.

- `max_steps` **không** là cách duy nhất chuẩn hóa chi phí: SCST sinh thêm greedy, PPO `μ=2` tính hai optimizer step trên cùng rollout, RLOO có sample cost khác. Báo cả `unique prompts`, `sampled completions`, `reward calls`, `optimizer updates`, `tokens trained`, wall time, peak VRAM.
- Đối chứng một chiều: fixed reward+data+prompt+pipeline. Nếu đổi advantage normalization, báo rõ learning-rate/gradient-scale confound; dùng GRPO-no-std (K1) làm cầu nối.
- Kết luận thuật toán dựa trên **hành vi thực thi và tài nguyên**, không dựa vào điểm SPICE training.

### 7.5 Pha 3 — reward comparison: giữ GRPO

**Factorial nhỏ để tách tác dụng:**

| | Action gate OFF | Action gate ON |
|---|---|---|
| SPICE thuần (penalty match) | R0-capped-length | **R3-Hard** |
| Sparse-aware SPICE | R2 | **R4** |

Nếu `R4 > R3-Hard` và `R2 > R0-capped-length` theo cùng hướng, có bằng chứng fallback ích lợi. Nếu `R4 − R3-Hard` tốt nhưng `R2 − R0-capped-length` không, cần kiểm tương tác; đừng gọi fallback có tác dụng độc lập. `R1 SPIDEr` luôn có trong shortlist; dùng `R5` và `R6/R7` làm incremental ablations **sau khi** kiểm nhãn target.

**Quan trọng về penalty:** `R0` trong factorial được ký hiệu `R0-capped-length`: phải có version length penalty giống R2/R3-Hard/R4. R3-Hard phải dùng CHÍNH XÁC action verifier/c_a, bonus, hard gate và penalty của R4, chỉ đổi `q_sparse` → SPICE; `spice_cong` 0.1×SPICE hiện có là baseline **R3-Soft**, không đặt vào factorial thay R3-Hard nếu muốn tách **chỉ tác dụng fallback/gate**. Giữ `R0-historical` với penalty không capped để đối chiếu ck500, nhưng báo là baseline phụ. Không quy chênh penalty cho SPICE.

**Siêu tham số:** trên validation grid nhỏ, định trước (ví dụ max `w∈{0.6,0.8}`, threshold tuple `k∈{2,3}`, action bonus `b∈{0.1,0.2}`), hoặc chọn một cấu hình trước rồi ablate từng giá trị. Có nhiều khả năng thử thì phải ghi số thử và chi phí; winner được đánh giá lại trên confirm holdout. Không chạy 30 tổ hợp xong chọn điểm test cao nhất.

### 7.6 Pha 4 — confirmatory evaluation và chọn winner

**Đơn vị split:** episode-disjoint là tối thiểu, tốt hơn có thêm **app-disjoint** cho claim khái quát ứng dụng mới; phải kiểm tên app/screenshot leaks. Tập C1 và test AndroidControl chính đã được thăm dò nhiều lần trong dự án; nếu dùng lại phải gọi là **exploratory**. Xây thêm holdout từ nguồn phù hợp/training-untouched trước khi chọn cấu hình và không chạm tới cho đến khi khóa model.

**Endpoint chính nên quyết trước khi có số:**

- `E_tap`: UGround/Voronoi-based executability trên các bước tap; kèm cột action đúng riêng và target correct trong nhóm action đúng.
- `E_nontap`: action-type accuracy `strict_back` trên các bước non-tap, báo scroll/back/input/wait/open_app riêng; không gọi đây là “executability” ngang với tap.
- Có thể dùng một **weighted composite pre-registered**: `E_all = (n_tap·E_tap + n_nontap·E_nontap)/(n_tap+n_nontap)`, nhưng luôn ghi rõ đây là **mixed surrogate**, không phải completion rate. Thêm **macro average theo 5/6 action type** để không để tap áp đảo.
- `Text`: BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE, chrF, BERTScore; đánh giá chất lượng ngôn ngữ **phụ**, không dùng chọn winner khi primary task metric giảm.
- `Safety/robustness`: false action, toggle contradiction, empty, malformed, reward hacking, non-tap no-harm, OOD AitZ/ACU; thêm ít nhất một independent grounder nếu đủ tài nguyên.

**Quy tắc lựa chọn được đề nghị:** trên validation, chọn các cấu hình không thua nghiêm trọng ở scroll/back (ngưỡng absolute pp phải **khóa trước**), sau đó tối đa hóa primary mixed surrogate (hoặc Pareto `tap exec` và `non-tap action`) và ưu tiên cấu hình đơn giản hơn nếu CI của chênh nằm trong vùng không phân biệt. Chọn checkpoint trên val, chốt trước test. Đừng lấy *SPICE* làm primary khi bài toán cuối cùng là GUI executability.

**Thống kê:** 10.000 bootstrap **theo ứng dụng** và/hoặc **episode** cho Δ ghép cặp, McNemar exact cho nhãn paired binary. Với nhiều reward/algorithm comparisons, pre-register *họ chính* 4–6 phép và chỉnh Holm; những so hậu kiểm chỉ mô tả. Seed variability được ước lượng qua các lần train; CI theo test cluster **không** bao phủ training-seed randomness. Với 2 seed chỉ được nói “kết quả trên hai seed”, không gọi là ổn định. Nếu có điều kiện chạy **≥3 seed** cho finalists, báo mean ± SD *giữa seed* và direction từng seed.

**MDE:** thiết kế cũ có MDE khoảng **2,11 pp**; lợi ích ck500 +1,55 pp trên tap nằm dưới. Không dùng p-value nhỏ để tuyên bố hiệu ứng thực tế lớn; báo effect size, CI, MDE/power và khả năng còn kết quả không phân biệt được.

### 7.7 Quy tắc dừng và diễn giải kết quả âm

| Kết quả quan sát được | Phán quyết được phép viết |
|---|---|
| R4 tăng zero-tuple reward nhưng tap exec giảm và scroll không cứu | Fallback cải thiện metric *diagnostic*, **không** cải thiện ứng dụng |
| R4 tăng scroll nhưng target tap giảm | Có trade-off; không được nói “toàn diện tốt hơn”; xem Pareto hoặc reject theo safety gate |
| R6 tăng target trên subset có mask nhưng không tăng toàn test | Chỉ công bố subgroup effect + coverage, không khẳng định general |
| R7 tốt hơn always-on trên nhiều seed và false reject giảm | Bằng chứng cho **reliability conditioning** (đóng góp mạnh hơn cộng trọng số) |
| SPIDEr hoặc ROUGE-L vượt tất cả reward SPICE cải tiến | Bỏ claim “SPICE-based tốt nhất”; vẫn có thể nêu bài học về reward mismatch và đóng góp âm |
| SCST vượt GRPO với cùng reward | Nêu rõ SCST tốt hơn; chọn GRPO theo constraints/cost nếu có số hỗ trợ, không ép thành winner |
| SFT tiếp ngang RL trên confirm holdout | Không được quy lợi ích cho RL; đóng góp có thể chuyển thành phân tích reward và giới hạn phương pháp |

---

## 8. Kịch bản đối chất với hội đồng (15 câu khó, câu trả lời ngắn có thể tập nói)

**Q1. Vì sao em phải dùng RL sau SFT?**  
A: SFT tối ưu likelihood của một reference, trong khi reward mức câu cho phép so chất lượng các câu mô hình thực sự sinh; đây là giả thuyết cần kiểm. Em so với SFT continuation để tách tác dụng của RL.

**Q2. Vì sao GRPO mà không PPO?**  
A: GRPO không cần critic riêng, so nhóm câu cùng GUI và phù hợp tài nguyên VLM 3B. Nhưng PPO vẫn có thể mạnh hơn; em đã định nghĩa PPO variant và so thực nghiệm cùng reward; không khẳng định GRPO tốt nhất chỉ vì rẻ.

**Q3. Vì sao không SCST?**  
A: SCST là đối chứng gần nhất từ captioning, dùng greedy baseline. Lưới hiện tại cho SCST+SPICE cạnh tranh với GRPO+SPICE. Em báo đầy đủ số và chạy nhiều seed; nếu SCST hơn thì không ép GRPO thắng.

**Q4. ORPO/DPO rẻ hơn sao không dùng?**  
A: ORPO/DPO cần preference pairs. Bài này có scalar metric cho từng sampled sentence; chuyển sang cặp cần quyết tie/chosen/rejected và có thể mất thông tin. Đây là khác biệt về nguồn học, **không** phải bất khả thi; có nhánh ORPO online/offline trong repo để kiểm.

**Q5. Em nói GRPO có PPO clip, liệu clipping thực sự hoạt động?**  
A: Trong ck500 `num_iterations=1` và `loss_type=dapo`, hiệu ứng chính tương tự policy gradient chuẩn hóa theo nhóm + KL; không được gán gain cho “trust-region clipping” nếu không có log ratio/clip hoặc ablation.

**Q6. Vì sao dùng SPICE nếu METEOR/CIDEr dự báo exec tốt hơn?**  
A: SPICE là **semantic anchor** có cấu trúc và tiền lệ trong grounded instruction evaluation, không phải metric xếp hạng từng câu tốt nhất. Đề tài nghiên cứu sửa đúng giới hạn SPICE khi chuyển sang GUI. Các metric kia là đối chứng mạnh, không bị loại trước.

**Q7. SPICE có thể cho `Scroll down` đúng bằng 0. Em vẫn dùng làm gì?**  
A: Chính đây là điểm yếu được đo, là động cơ thiết kế fallback theo tuple sparsity, phải chứng minh giảm zero-gradient và giảm tác hại scroll/back.

**Q8. Sao không chỉ dùng SPIDEr?**  
A: SPIDEr là baseline reward lai rất mạnh. Nó cung cấp metric bổ sung nhưng chưa xác minh đúng action. Em so R4 với SPIDEr để biết action-aware mechanism có lợi ngoài việc cộng thêm n-gram hay không.

**Q9. Có gì mới khi UI-R1 đã dùng action reward và FoCUS đã dùng scene graph reward?**  
A: Em không tuyên bố mới ở từng thành phần. Giả thuyết đóng góp là cơ chế **kích hoạt theo độ tin cậy và semantic sparsity** cho câu hướng dẫn GUI, kèm kiểm định *đúng action → đúng phần tử* dưới nhãn thiếu chắc chắn. Nếu ablation không tách được với fixed sum hoặc SPIDEr, em không gọi là methodological novelty mạnh.

**Q10. Em lấy target name từ đâu? Có nhiễu không?**  
A: Training-only annotation/OCR/candidate inventory. Repo đo thấy 29% câu chuẩn có `F1_tên=0` ở các bước có descriptor. Vì vậy R6 chỉ là extension; R7 có reliability mask và phải báo false-rejection của gold, coverage và target contrast quality.

**Q11. Tại sao không reward bằng UGround để trúng executability luôn?**  
A: UGround đang tham gia evaluation; reward từ đúng evaluator dễ Goodhart/model-specific gaming và rất tốn inference. Em chủ động giữ reward reference/rule-based trong training; kiểm kết quả qua UGround và thêm listener độc lập nếu đủ ngân sách.

**Q12. Nếu SPICE tăng mà exec không tăng thì luận văn thất bại?**  
A: Không thất bại về quan sát khoa học nếu nêu đúng hạn chế, nhưng **không thể** ghi “improves executability”. Cần thí nghiệm reward-alignment và báo điều kiện nào chuyển metric gain thành task gain, hoặc kết luận phương pháp chưa đủ.

**Q13. Reward nào điểm test cao nhất thì lấy, có vấn đề gì?**  
A: Có selection bias từ nhiều phép thử; điểm cực đại trên test bị optimistic. Em chọn trên val, khóa công thức/checkpoint, test holdout một lần; báo rõ multiple comparisons và seed variation. Tập test cũ đã nhìn nên là exploratory.

**Q14. Vì sao ck500 60,65 nhưng train lại cùng phương pháp 59,74?**  
A: Đây là reproducibility caveat thật. Các run khác version/library/GPU, sampling dynamics có thể đổi; seed 202 cũng cho khoảng 59,94. Không được dùng ck500 là bằng chứng phương pháp ổn định, cần matched-pipeline A/A và nhiều seed.

**Q15. Điểm đóng góp nào đứng vững ngay cả nếu R4 không vượt SPIDEr?**  
A: Bộ phân tích có kiểm chứng về zero semantic tuple, action mismatch, target-label noise và evaluator sensitivity trên AndroidControl; nếu có protocol/negative controls/ablation đủ chặt đó là đóng góp thực nghiệm. Nhưng không được nói đã có đóng góp phương pháp vượt trội nếu kết quả âm.

---

## 9. Đề nghị cấu trúc chương 2, 4, 6 và mục “Đóng góp”

### Chương 2 — Tổng quan và liên hệ nghiên cứu

- 2.1 Natural-language GUI instruction generation và AndroidControl; khác biệt với GUI agent xuất action/coordinates.
- 2.2 SFT vs sequence-level RL (SCST, PPO, GRPO, RLOO, ORPO/DPO); matrix ưu điểm và giới hạn.
- 2.3 Metric reward BLEU/CIDEr/METEOR/ROUGE/SPICE/SPIDEr/BERTScore; SPICE cho grounded instruction.
- 2.4 Related methods đặc biệt gần: SPICE-U, iSPICE, UI-R1, SC-Captioner, FoCUS, CCCaption, GDPO; bảng novelty boundary.

### Chương 4 — Phương pháp

- 4.1 Input và output (ảnh+goal+history+OCR → 1 câu), phân biệt train reward với inference và external grounder.
- 4.2 S1 pretraining/SFT, LoRA merge, KL reference là S1.
- 4.3 GRPO optimizer **đúng bản TRL/dapo** và group advantage, không lạm dụng “PPO clipping”.
- 4.4 SPICE baseline và các lỗi có phép đo: zero tuple, action blindness, target ambiguity, prompt bias.
- 4.5 ACSS formula, c_a, parser-fallback, zero handling, length penalty, reliability constraints; chỉ công bố công thức **đã khóa**.
- 4.6 Extension target contrast nếu đủ nhãn; ACE hậu xử lý báo riêng, không lẫn vào đóng góp RL.

### Chương 6 — Kết quả, không che kết quả xấu

- 6.1 Sanity/baseline A/A, kiểm nguồn và môi trường.
- 6.2 RQ-algorithm: SFT vs GRPO vs SCST/RLOO/... (same SPICE).
- 6.3 RQ-reward: SPICE vs CIDEr/ROUGE/METEOR/SPIDEr và ACSS family (same GRPO).
- 6.4 Ablation: 2×2 sparse×action và `target_mask` vs always-on; stress tests; gradient signal.
- 6.5 Primary tap exec và non-tap accuracy, action/target decomposition, multi-grounder/OOD.
- 6.6 Multiple-seed, paired uncertainty, negative controls (shuffled reward, length-only), compute costs.
- 6.7 Giới hạn: semantic metric ≠ behavior, class imbalance, noise, replay/test selection, prompt bias, model-only executability.

### Mục “Đóng góp” — chỉ dùng sau khi có chứng cứ

**C1 — Thiết kế (nếu được xác nhận):** Một cách dựng reward *Action-Conditioned Sparse-SPICE* có reliability handling cho sinh hướng dẫn GUI.  
**C2 — Kiểm chứng cơ chế (nếu được xác nhận):** Ablation cho thấy khi nào sparse fallback và action gate làm tăng gradient hữu ích, giảm sai action mà giữ đúng target.  
**C3 — Đánh giá hệ thống (được phép nếu làm đúng):** Protocol so có kiểm soát giữa SFT/GRPO/SCST/... và giữa các reward, chỉ ra tác động lên tap/non-tap và giới hạn đo lường.  
**Không khẳng định:** “phát minh GRPO”, “phát minh scene graph reward”, “đầu tiên dùng SPICE làm RL reward”, “đầu tiên dùng action-aware reward cho GUI”, “giải quyết triệt để executability”.

---

## 10. Kế hoạch thực hiện theo code hiện có (chưa sửa source)

1. **Đóng băng môi trường thí nghiệm:** tạo `experiment_manifest.json` (version, code hash, S1 weights, prompt keys, data split, reward ID, seed, GPU, reference); log 16 sample/reward đầu. Giữ các file uncommitted hiện có, không reset.
2. **Thêm reward như module mới** (ví dụ `harness/reward_acss.py`) để `grpo_luoi.py` không bị đổi baseline lịch sử; kiểm signatures `completions`, `gold`, `key`, `action_type` xem TRL chuyển field nào. Bổ sung `--selftest` mock SPICE, không gọi Java cho pure unit tests, sau đó chạy Java thật.
3. **Viết action verifier versioned** (ví dụ `harness/action_reward_verify.py`) độc lập `metric_exec`, có `unknown` và explicit conflict checks. Audit với gold, synonyms và negative controls trước khi train.
4. **Cache `T(g)`** và precompute train-only reliability action/target; không dùng test metadata; kiểm checksum để data không lệch.
5. **Nâng H2 reward diagnostics**: R0, R1, R2, R3, R4 và R6/R7 chỉ nếu đủ nhãn; phân nhóm theo action; log false rejection, all-wrong, oracle; lưu các stress case do người kiểm (không phán kết quả bằng một metric duy nhất).
6. **Chạy lưới có thứ tự:** thí nghiệm baseline A/A đầu tiên, sau đó factorial 2×2 reward, SPIDEr; R6/R7 nếu R4 đáng giữ; tách seed prompt khỏi seed optimizer. Không train reward “thích mắt” qua nhiều test.
7. **Thiết lập evaluation xác nhận:** holdout khóa, app/episode grouping, mixed surrogate giải thích rõ, targeted error analysis, Holm cho primary comparisons, báo compute và CI qua seed.
8. **Chỉ sau khi đã có số mới sửa `thesis/`**: thay lời văn hiện hành chưa đồng bộ 08/11, xác minh lại bảng và references, không làm sạch/overwrite dữ liệu lịch sử để tạo câu chuyện đẹp.

### Exit criteria trước buổi gặp thầy

- [ ] Có bảng đầy đủ **tại sao GRPO** gồm SCST/RLOO/SFT/PPO và thừa nhận nhánh không thắng.
- [ ] Có bảng **tại sao nghiên cứu SPICE** gồm H2 bất lợi, 0-tuple, `scroll/back`, SPIDEr/CD/ROUGE/METEOR.
- [ ] Có **một reward đã khóa**; pseudo/code và selftest cho từng thành phần; không dùng evaluator test trong reward.
- [ ] Có **2×2 ablation**, cùng pipeline và penalty, cùng prompt/seed/budget.
- [ ] Có **multiple seed**, thống kê đúng mức; không chọn winner bằng nhìn test nhiều lần.
- [ ] Có **novelty comparison** với FoCUS/UI-R1/iSPICE/SC-Captioner, chỉ claim phần khác biệt đã kiểm.
- [ ] Có số **tap và non-tap riêng**, target decomposition, action false rejects.
- [ ] Chương 4/6 không khẳng định GRPO/SPICE là tốt nhất nếu số không hỗ trợ.

---

## 11. Kết luận cuối và quyết định khuyến nghị

**Đề nghị khoa học hiện thời:** Không giữ câu chuyện “GRPO+SPICE đã tốt nhất”. Giữ GRPO làm **algorithmic baseline có cơ sở tài nguyên và thiết kế**, SPICE làm **semantic anchor có tiền lệ**, dùng **SPIDEr, SCST, RLOO, SFT continuation** để chủ động thử bác bỏ hai lựa chọn đó. Thử trước **R4/ACSS** vì giải quyết hai lỗi được đo nhiều nhất và không cần target descriptors; chỉ sau khi có bằng chứng về chất lượng nhãn mới mở **R6/R7** để nhắm vào phần target gain không tái lập.

Nếu R4 vượt baseline nhưng không vượt SPIDEr: chỉ claim là một biến thể có kết quả cạnh tranh, không claim vượt mọi reward. Nếu R7 thắng rõ ràng, lặp lại nhiều seed và tốt hơn cả **fixed-weight/always-on** nhờ reliability mask, đó mới là hướng có câu chuyện phương pháp mạnh nhất. Nếu tất cả reward mới đều không vượt, kết luận khoa học đúng là **SPICE-based reward shaping chưa khắc phục gap giữa text similarity và GUI executability trong điều kiện này**; một kết quả âm được kiểm soát vẫn có giá trị hơn một lời khẳng định không tái lập.

**Trạng thái thực thi của tài liệu:** Đây là deep research + thiết kế/phản biện, **chưa triển khai các reward mới, chưa chạy training, chưa chấm confirm holdout**, và không sửa bất kỳ dữ liệu hay code đã có nào.

---

## Phụ lục A — Bản đồ tra cứu nhanh (link paper + nguồn code)

**Nguồn chính về GRPO và thuật toán:**

- Shao et al. 2024, *DeepSeekMath* — https://arxiv.org/abs/2402.03300
- Schulman et al. 2017, *Proximal Policy Optimization Algorithms* — https://arxiv.org/abs/1707.06347
- Rennie et al. 2017, *Self-Critical Sequence Training for Image Captioning* — https://openaccess.thecvf.com/content_cvpr_2017/html/Rennie_Self-Critical_Sequence_Training_CVPR_2017_paper.html
- Ahmadian et al. 2024, *Back to Basics: Revisiting REINFORCE-Style Optimization...* — https://aclanthology.org/2024.acl-long.662/
- Hong et al. 2024, *ORPO* — https://aclanthology.org/2024.emnlp-main.626/
- Rafailov et al. 2023, *DPO* — https://papers.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html
- Liu et al. 2025, *Understanding R1-Zero-Like Training: A Critical Perspective (Dr. GRPO)* — https://proceedings.colm.cc/paper_files/paper/2025/hash/ecd8143eeaf83e6dc87ffcb683b0f81b-Abstract-Conference.html
- Liu et al. 2026, *GDPO* — https://proceedings.mlr.press/v306/liu26aa.html
- TRL GRPO Trainer reference (phải ghim theo **version thực chạy**, không đọc docs latest để suy ra ck500) — https://huggingface.co/docs/trl/v0.24.0/grpo_trainer

**Nguồn chính về SPICE, caption và semantic reward:**

- Anderson et al. 2016, *SPICE* — https://mlanthology.org/eccv/2016/anderson2016eccv-spice/
- Liu et al. 2017, *SPIDEr* — https://research.google/pubs/improved-image-captioning-via-policy-gradient-optimization-of-spider/
- Vedantam et al. 2015, *CIDEr* — https://openaccess.thecvf.com/content_cvpr_2015/html/Vedantam_CIDEr_Consensus-Based_Image_2015_CVPR_paper.html
- Wang et al. 2020, *Towards Unique and Informative Captioning of Images (SPICE-U)* — https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123520613.pdf
- Raajesh et al. 2024, *MICap / iSPICE* — https://openaccess.thecvf.com/content/CVPR2024/html/Raajesh_MICap_A_Unified_Model_for_Identity-Aware_Movie_Descriptions_CVPR_2024_paper.html
- Zhang et al. 2025, *SC-Captioner* — https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_SC-Captioner_Improving_Image_Captioning_with_Self-Correction_by_Reinforcement_Learning_ICCV_2025_paper.html
- Tang et al. 2026, *CCCaption* — https://openaccess.thecvf.com/content/CVPR2026/html/Tang_CCCaption_Dual-Reward_Reinforcement_Learning_for_Complete_and_Correct_Image_Captioning_CVPR_2026_paper.html
- Hyun et al. 2026, *FoCUS* — https://aclanthology.org/2026.emnlp-main.2622/

**Nguồn chính về GUI/instruction evaluation:**

- Li et al. 2024, *AndroidControl* — https://papers.nips.cc/paper_files/paper/2024/hash/a79f3ef3b445fd4659f44648f7ea8ffd-Abstract-Datasets_and_Benchmarks_Track.html
- Zhao et al. 2021, *On the Evaluation of Vision-and-Language Navigation Instructions* — https://aclanthology.org/2021.eacl-main.111/
- Lu et al. 2026, *UI-R1* — https://ojs.aaai.org/index.php/AAAI/article/view/38816
- Zhou et al. 2025, *GUI-G1* — https://proceedings.neurips.cc/paper_files/paper/2025/hash/89dcbea9f19960edd7765068adb13b1d-Abstract-Conference.html
- Xing et al. 2026, *CapRL* — https://proceedings.iclr.cc/paper_files/paper/2026/hash/15f1dbc086bfd94d8c32557b573cbe18-Abstract-Conference.html

**Nguồn nội bộ đặc biệt cần mở khi triển khai:** `report/320` §16–21, `report/323` §8, `report/328`, `report/330`; mã `harness/grpo_luoi.py`, `harness/grpo_spice.py`, `harness/thuong_moi.py`, `harness/h2_thuong.py`, `harness/metric_exec.py`, `harness/grpo_ppo.py`, `harness/grpo_moi_b4.py`.

## Phụ lục B — Mẫu bảng kết quả để điền sau thí nghiệm

| Run ID | Reward | Algo | Seed | S1 source hash | Tap exec | Non-tap action | Scroll | Back | Target-conditional | SPICE | CI vs matched A/A | GPU-h | Chú thích |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| EXP-BASE | R0 | GRPO | 101 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Repro A/A |
| EXP-SPIDER | R1 | GRPO | 101 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Baseline hybrid |
| EXP-SPARSE | R2 | GRPO | 101 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Fallback only |
| EXP-GATE | R3 | GRPO | 101 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Action only |
| EXP-ACSS | **R4** | GRPO | 101 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Candidate primary |
| EXP-TARGET | R7 | GRPO | 101 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Chỉ nếu nhãn đủ tốt |
| EXP-SCST | R0 | SCST | 101 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Algo baseline |
| EXP-SFT | — | SFT tiếp | 101 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Non-RL control |

*Không điền các ô TBD bằng suy đoán; số test lịch sử không thay thế confirm run. File này là research brief, không phải kết quả nghiệm thu.*