# ORPO và cách so công bằng với GRPO dưới phần thưởng câu liên tục (tra 3/11/2026)

Quy ước nhãn: [S] đã thấy trên trang kỷ yếu hoặc nguồn xuất bản · [Pre] preprint hoặc chưa thấy venue · [suy] suy luận của tôi · [nội bộ] số của dự án, không phải văn liệu. Số [nội bộ] đo trên val thì cấm trích vào luận văn.

Phần kiểm MIN-DESC do người khác làm, ở đây chỉ nhắc khi cần phân biệt.

## 1. Bài ORPO quy định gì: hàm mất mát, λ, chosen/rejected, không mô hình tham chiếu, quan hệ với DPO

### Takeaway
ORPO (Hong, Lee, Thorne, EMNLP 2024 main) là NLL trên câu chosen cộng λ nhân log-sigmoid của log odds ratio, chạy một giai đoạn từ mô hình pretrained, không cần mô hình tham chiếu. Bài dùng λ từ 0,1 đến 0,25 cho kết quả chính, và rejected lấy sẵn từ tập ưu tiên ngoại tuyến. Bài không định nghĩa biến thể trực tuyến, cũng không nói cách đổi điểm liên tục thành cặp.

### Cited Findings
- Thư mục: *ORPO: Monolithic Preference Optimization without Reference Model*, Jiwoo Hong, Noah Lee, James Thorne, EMNLP 2024 (Miami), tr. 11170–11189, DOI 10.18653/v1/2024.emnlp-main.626 [S] — [ACL Anthology](https://aclanthology.org/2024.emnlp-main.626/).
- Hàm mất mát: L_ORPO = E[L_SFT + λ·L_OR], với L_OR = −log σ(log(odds(y_w|x)/odds(y_l|x))) và odds(y|x) = P(y|x)/(1−P(y|x)). P được tính từ **trung bình log-xác suất theo token**: log P(y|x) = (1/m)·Σ log P(y_t|x, y_<t) (Phương trình 3–7) — [ORPO, arXiv 2403.07691](https://arxiv.org/abs/2403.07691).
- Gradient: ∇L_OR = δ(d)·h(d), với δ = (1 + odds(y_w)/odds(y_l))⁻¹ và h = ∇log P(y_w)/(1−P(y_w)) − ∇log P(y_l)/(1−P(y_l)) (Phương trình 8–10) — [ORPO](https://arxiv.org/abs/2403.07691).
- λ trong các kết quả chính: Phi-2 λ=0,25 · Llama-2 7B λ=0,2 · Mistral λ=0,1 — [ORPO §6.1](https://arxiv.org/abs/2403.07691).
- Độ nhạy theo λ (Phụ lục E): λ=0,1 thì log-p chosen và rejected đi sát nhau, rejected không giảm mà chosen tăng. λ=1,0 thì cả hai cùng giảm trong khi biên rộng ra. Trên MT-Bench, λ=1,0 kém hơn λ=0,1 ở extraction, math, reasoning nhưng hơn ở STEM, humanities, roleplay. Bài suy ra rằng biên lớn hơn dẫn tới quá thích nghi với tập chosen, và viết "this does not mean smaller λ is always the better" — [ORPO Phụ lục E](https://arxiv.org/abs/2403.07691).
- Chosen/rejected: lấy từ HH-RLHF và UltraFeedback đã nhị phân, lọc bỏ trường hợp y_w = y_l hoặc một vế trống — [ORPO §5.1](https://arxiv.org/abs/2403.07691). Cách nhị phân UltraFeedback theo mô tả của Tülu 3: chosen là câu điểm cao nhất, rejected lấy ngẫu nhiên từ các câu điểm thấp hơn — [Tülu 3](https://arxiv.org/abs/2411.15124) [Pre, chưa kiểm venue].
- Không tham chiếu: bài lập luận ORPO cập nhật trực tiếp π_SFT nên số lượt forward giảm một nửa so với DPO và RLHF (4 xuống 2 mỗi lô) — [ORPO §7.3](https://arxiv.org/abs/2403.07691).
- Quan hệ với DPO: DPO dùng tỉ số xác suất so với mô hình tham chiếu sau một lượt SFT riêng; ORPO gộp SFT và tương phản thành một giai đoạn. Trong thí nghiệm, DPO và PPO chạy trên mô hình đã SFT một epoch, còn ORPO chạy thẳng. Bài lập luận dùng tỉ số xác suất khi gộp với SFT sẽ đè quá mạnh token của rejected nên chọn odds ratio — [ORPO §5.1, §7.1](https://arxiv.org/abs/2403.07691).
- Win rate của ORPO trên OPT-125M/350M/1.3B (bài đề xuất, chấm bằng GPT-4): HH-RLHF so SFT 84,0/82,7/78,0 · so DPO 41,7/49,4/70,9 · so PPO 66,1/79,4/65,9. UltraFeedback so SFT 73,2/80,5/69,4 · so DPO 48,8/50,5/57,8 · so PPO 71,4/85,8/65,7 (Bảng 2–3) — [ORPO](https://arxiv.org/abs/2403.07691).
- Bảng độc lập: trong KTO (ICML 2024 [S]), trên Zephyr-β-SFT, ở MMLU/GSM8k/HumanEval/BBH: SFT 57,2/39,0/30,1/46,3 · DPO 58,2/40,0/30,1/44,1 · ORPO (λ=0,1) 57,1/36,5/29,5/47,5 · KTO 58,6/53,5/30,9/52,6 — [KTO Bảng 2, arXiv](https://arxiv.org/abs/2402.01306); [PMLR](https://proceedings.mlr.press/v235/ethayarajh24a.html). KTO là bài đề xuất của phương pháp khác, nên đọc kèm thiên vị đó.

### Inferences
- [suy] Câu văn bản bài nói mẫu số 1−P "amplifies the gradients when ... P(y|x) is low" có vẻ ngược với chính công thức: 1/(1−P) lớn khi P **cao**. Đừng chép câu đó, chỉ chép công thức.
- [suy] Vì P là trung bình hình học theo token, câu ngắn của dự án có P cao, và λ không chuyển thẳng từ bài sang đây được. Số [nội bộ] ở `report/314_KET_QUA_GADPO_13_10.md` §5: log-p/token trước train −0,26 (chosen), −0,37 (rejected), tức P ≈ 0,77 và 0,69, δ ≈ 0,40, hệ số 1/(1−P) ≈ 4,4 và 3,3. Với λ=0,1 gradient cộng thêm cỡ +0,18·∇log P(chosen) và −0,13·∇log P(rejected) so với hệ số 1 của NLL. Hình 7 của bài có log-p khoảng −0,9 đến −1,8, tức hệ số 1/(1−P) chỉ khoảng 1,2–1,7. Vậy λ=0,1 ở đây có tác dụng lớn hơn khoảng 2–3 lần so với cùng λ trong bài. Đây là ước lượng tại điểm đầu, trên cặp của ck500, chỉ để hiểu cỡ.
- [suy] Dùng ORPO sau S1 là dùng khác với thiết kế gốc của bài (chạy thẳng từ pretrained) và phải khai như vậy. Bài chạy DPO/PPO từ SFT nhưng ORPO thì không.

### Gaps
- Bài không báo kết quả cho câu rất ngắn, phần thưởng dựa trên tham chiếu, hay mô hình đa phương thức. Không so với GRPO (bài ra trước khi GRPO phổ biến).

## 2. Đổi điểm liên tục thành cặp ưu tiên: các cách đã công bố, và số so DPO/ORPO với PPO/GRPO

### Takeaway
Cách có tiền lệ rõ nhất là lấy n mẫu từ chính sách, xếp theo điểm, dùng cặp tốt nhất và kém nhất, bỏ câu nhắc không tạo được cặp (Bridging). Các phép so có số thường dùng DPO, không phải ORPO. Tôi không tìm thấy phép so trực tiếp ORPO với GRPO nào. Kết quả chung là trực tuyến hoặc bán trực tuyến hơn hẳn ngoại tuyến cho cùng hàm mất mát, nhưng không phải ở mọi thí nghiệm.

### Cited Findings
**Cách dựng cặp**
- Bridging [Pre]: với thưởng vô hướng từ mô hình thưởng, xếp hạng câu rồi tạo cặp tốt nhất–kém nhất; chú thích ghi "we choose the best-vs-worst due to its simplicity and stability" và thừa nhận còn cách khác. Với thưởng nhị phân, chọn ngẫu nhiên một câu đúng và một câu sai; câu nhắc toàn đúng hoặc toàn sai thì **bỏ khỏi bước đó**, và bài chỉ ra điều này tương tự GRPO vì lợi thế đều bằng 0 — [Lanchantin et al.](https://arxiv.org/abs/2506.21495).
- OAIF [Pre]: mỗi vòng lấy 2 câu từ chính sách hiện tại, annotator LLM chọn câu hơn, cập nhật bằng DPO/IPO/SLiC — [Guo et al.](https://arxiv.org/abs/2402.04792). Đây chính là mẫu của `OnlineDPOTrainer` trong TRL (mục 4).
- OPTune [Pre, chưa kiểm venue]: lập luận cặp có chênh thưởng lớn hữu ích hơn nên đề xuất wDPO, gán trọng số theo chênh thưởng; chỉ sinh lại câu cho các câu nhắc thưởng thấp — [Chen et al.](https://arxiv.org/abs/2406.07657).
- RPO [Pre, chưa kiểm venue]: đưa thưởng vào hàm mất mát cặp, mô tả ba chế độ ngoại tuyến, ngoại tuyến lặp (ít hơn 10 vòng) và trực tuyến — [Sun et al.](https://arxiv.org/abs/2502.00203).
- Self-rewarding only-prompting [Pre]: kiểm soát khoảng cách giữa cặp bằng số học, thu hẹp dần để sinh nhiều mẫu âm khó ở cuối train — [Xu et al.](https://arxiv.org/abs/2409.17534).
- Rejection sampling theo mô tả của Tülu 3: sinh n câu, xếp hạng, giữ câu tốt nhất, các câu còn lại làm rejected; Tülu 3 thử và thấy mức tăng tối thiểu so với chi phí, và nhấn mạnh cần bộ chấm mạnh — [Tülu 3](https://arxiv.org/abs/2411.15124) [Pre].
- KTO: cần nhãn mong muốn/không mong muốn cho từng câu, không cần cặp — [KTO](https://proceedings.mlr.press/v235/ethayarajh24a.html) [S]. RAFT giữ mẫu tốt nhất để SFT, không dùng rejected — [RAFT](https://arxiv.org/abs/2304.06767) (venue chưa kiểm ở lượt này).

**Số so sánh**
- Bridging, Math500/NuminaMath/AMC23: seed 47,4/33,9/23,7 · DPO ngoại tuyến 53,7/36,4/28,8 · bán trực tuyến s=100 58,9/39,3/35,1 · s=10 57,2/39,4/31,4 · trực tuyến 58,7/39,6/32,9 · GRPO 58,1/38,8/33,6 — [Lanchantin et al., Bảng 1](https://arxiv.org/abs/2506.21495).
- Bridging, AlpacaEval LC với GPT-4-1106 / GPT-4o và ArenaHard với cùng hai bộ chấm: seed 27,3/21,3/32,0/27,8 · ngoại tuyến 53,2/38,3/39,4/38,2 · s=10 81,6/59,4/61,1/43,0 · s=5 78,7/60,7/58,5/49,8 · trực tuyến 83,1/60,1/62,8/50,4. GRPO ở AlpacaEval GPT-4-1106 là 75,2 và ArenaHard GPT-4o là 54,3 (hai số này lấy từ `report/reports/Baseline RL so với GRPO.md`, đã thấy hàng GRPO nhưng chưa chép đủ cột ở lượt này) — [Lanchantin et al., Bảng 2](https://arxiv.org/abs/2506.21495).
- Xu et al. (ICML 2024, theo [trang arXiv](https://arxiv.org/abs/2404.10719)), SafeRLHF, Llama 2 7B, Δhelpfulness/harmlessness/tỉ lệ an toàn: SFT −2,12/0,00/52,1 · DPO −2,86/−6,82/95,8 · DPO-Iter −2,96/−11,07/99,9 · PPO +1,69/−12,08/99,5 — [Xu et al., Bảng 6](https://arxiv.org/abs/2404.10719). Bài kết luận PPO hơn và DPO-Iter hơn DPO tĩnh.
- OAIF, TL;DR, người chấm, trực tuyến so ngoại tuyến cùng hàm mất mát (thắng/hoà/thua): DPO 63,74/28,57/7,69 · IPO 64,81/31,48/3,71 · SLiC 71,43/26,98/1,59. Số lấy từ [ghi chú cũ của dự án](../Baseline%20RL%20so%20v%E1%BB%9Bi%20GRPO/rlhf_preference.md), phải đối chiếu [bài gốc](https://arxiv.org/abs/2402.04792) trước khi trích.
- Back to Basics (ACL 2024 [S]), TL;DR: RLOO k=4 77,9 · RAFT k=4 73,2 · PPO 67,6 · DPO 66,6 — [ghi chú dự án](../../reports/Baseline%20RL%20so%20v%E1%BB%9Bi%20GRPO.md), [bài](https://aclanthology.org/2024.acl-long.662/). Ghi chú đó còn báo PPO 77,6 ở bài khác, nên biên PPO phụ thuộc cài đặt.
- Kết quả âm cho trực tuyến: Tülu 3 chạy online DPO 200K episode trên toán từ một điểm DPO, thấy gần như không tăng ở GSM8K và giảm ở MATH — [Tülu 3](https://arxiv.org/abs/2411.15124). RPO: phương pháp trực tuyến với mô hình thưởng học được "can barely improve over the SFT model", có reward hacking — [Sun et al.](https://arxiv.org/abs/2502.00203). Cả hai liên quan tới bộ thưởng học được; SPICE thì không học, nhưng vẫn chơi được độ đo.
- Đa phương thức: SC-Captioner (ICCV 2025) viết DPO "fails to get higher results" trong khi phương pháp RL của bài tăng — [SC-Captioner](https://arxiv.org/abs/2508.06125). Ghi chú dự án có số SFT 40,92 · SFT+DPO 43,13 · SFT+RL 43,70 (BLEU-4, DOCCI500); số 43,13 có vẻ không khớp với câu "fails", cần mở bảng (bài có cả hàng SFT+DPO và SFT+DPO*) trước khi trích.

**Hai mục trong đề bài cần sửa nhãn**
- FlowRL [Pre]: tóm tắt nói về khớp phân phối thưởng với mục tiêu KL ngược, không nhắc cặp ưu tiên; nên không phải phương pháp dựng cặp hay bán trực tuyến theo những gì trang tóm tắt cho thấy — [FlowRL](https://arxiv.org/abs/2509.15207).
- GA-DPO: tra cứu trước đó không thấy phương pháp công bố nào tên này; đây là tên nội bộ của dự án — [ghi chú dự án](../Baseline%20RL%20so%20v%E1%BB%9Bi%20GRPO/rlhf_preference.md).

### Inferences
- [suy] Khuôn chép được cho luận văn là Bridging + QRPO: một nguồn thưởng duy nhất vừa xếp cặp vừa làm thưởng GRPO. Hàng ORPO trực tuyến là phần mở rộng của dự án, không phải tái lập.
- [suy] Bridging dùng cùng một loại mô hình seed và cùng một thưởng, nhưng thưởng của nó không so với một câu chuẩn duy nhất. Không suy thẳng kết quả "bán trực tuyến ngang GRPO" sang SPICE.

### Gaps
- Không thấy bài nào so ORPO với GRPO hay PPO có số trên cùng lần chạy, ngoài Bảng 2–3 của ORPO (PPO, trên OPT).
- Chưa đọc nội dung: Xiong et al. ([arXiv 2312.11456](https://arxiv.org/abs/2312.11456), bài lặp có ràng buộc KL), DPO-Positive/Smaug ([arXiv 2402.13228](https://arxiv.org/abs/2402.13228)), IPO, West-of-N (Pace et al. 2024, chỉ thấy qua trích dẫn của Bridging). Không được dẫn chi tiết của các bài này từ ghi chú này.
- Một trang tổng hợp nói chọn cặp ở vị trí cố định trong phân phối thưởng cho biên tốt hơn cực trị; nguồn gốc không rõ nên tôi không dùng.
- "Meta RLHF with DPO on sampled data" không ứng với bài nào cụ thể mà tôi xác định được, gần nhất là Bridging.

## 3. ORPO trực tuyến so ngoại tuyến, và bằng chứng về cách dựng cặp theo điểm

### Takeaway
Tôi không tìm thấy biến thể "ORPO trực tuyến" nào được công nhận. Tiền lệ dùng mẫu theo chính sách đều là DPO hoặc họ gần đó. Về khoảng cách tối thiểu, hoà và số cặp mỗi câu nhắc, bằng chứng rất ít: chủ yếu là các lựa chọn thiết kế, không phải phép đo so sánh. Vì vậy một hàng ORPO trực tuyến trong luận văn phải được gọi là bản thích nghi của dự án.

### Cited Findings
- Một tra cứu mở rộng cho "online ORPO + on-policy + ngưỡng chênh điểm" không ra bài nào; kết quả gần nhất là các bài ở mục 2 (OPTune, RPO, self-rewarding). Đây là không tìm thấy, không phải chứng minh không có.
- Chênh tối thiểu và hoà: Bridging không đặt ngưỡng, chỉ bỏ câu nhắc không tạo được cặp — [Lanchantin et al.](https://arxiv.org/abs/2506.21495). ORPO lọc y_w = y_l — [ORPO §5.1](https://arxiv.org/abs/2403.07691). OPTune dùng trọng số thay vì ngưỡng — [Chen et al.](https://arxiv.org/abs/2406.07657).
- Câu chosen và rejected quá giống: Razin et al. (ICLR 2025 [S]) chứng minh và đo likelihood displacement: log-xác suất câu ưu tiên có thể **giảm** khi train, do các cặp có nhúng ẩn tương tự (điểm CHES). Với mục tiêu từ chối, tỉ lệ từ chối của Llama-3-8B giảm từ 74,4% xuống 33,4%. Lọc còn 5% (kết quả tương tự tới 15%) mẫu CHES thấp nhất có tác dụng; thêm số hạng SFT cũng chặn việc giảm tỉ lệ từ chối nhưng lọc tăng mạnh hơn. Kết luận là cần tuyển dữ liệu có ưu tiên đủ khác nhau — [Razin et al.](https://arxiv.org/abs/2410.08847), [trang ICLR](https://iclr.cc/virtual/2025/poster/27968). Bài không nhắc ORPO theo tên trong bản HTML v3 tôi đã quét; Phụ lục E phân tích dạng "mất mát cặp − λ·ln π(y⁺)" là dạng gần với ORPO, nhưng hàm cặp của ORPO đi qua odds, nên phải kiểm trước khi nói áp được trực tiếp.
- Số cặp mỗi câu nhắc: Tülu 3 nhân bản UltraFeedback lên 64k/180k/383k cặp bằng cách ghép lại trên cùng câu nhắc; 383k ngang 64k, và giảm nhẹ ở DROP, GSM8k, AlpacaEval khi trùng câu nhắc nhiều hơn — [Tülu 3](https://arxiv.org/abs/2411.15124). Tülu 3 cũng báo thêm dữ liệu theo chính sách giúp DPO tốt hơn dữ liệu hoàn toàn ngoài chính sách (Hình 11) — cùng nguồn.
- Reference và độ dài: bài Bridging thấy tắt cập nhật mô hình tham chiếu làm độ dài câu của online DPO sụp, kéo theo thưởng val giảm — [Lanchantin et al., Hình 2](https://arxiv.org/abs/2506.21495). OAIF ghi nhận câu dài ra và kiểm soát bằng phân nhóm độ dài — [ghi chú dự án](../Baseline%20RL%20so%20v%E1%BB%9Bi%20GRPO/rlhf_preference.md).
- Bằng chứng trực tiếp [nội bộ, số train, không phải văn liệu]: ở cặp lấy từ ck500, sau 5 epoch trên 200 cặp, cặp "giữ" (chosen = greedy, rejected = mẫu thua) đạt acc giữ riêng 0,76, còn cặp "cải thiện" (chosen = mẫu trội greedy) 0,46, ngang tung đồng xu; log-p chosen trên câu nhắc mới giảm −0,261 → −0,457 với NLL λ=1, β=0,1 — `report/314_KET_QUA_GADPO_13_10.md` §5. Đây là DPO + NLL từ ck500, không phải ORPO từ S1.
- Số đo cho thiết kế [nội bộ, val, cấm trích], tính từ `runs/c1/exec8/metric_tung_cau.json` và `runs/c1/c1_mau.jsonl` (S1, 400 bước, 8 mẫu):

| | SPICE | CIDEr-D (thang 0–10) |
|---|---|---|
| Câu nhắc có cả 8 mẫu hoà | 22,8% | 11,2% |
| Mẫu tốt nhất hơn greedy | 37,5% | 44,5% |
| Trung vị chênh tốt nhất − kém nhất | 0,571 | 5,0 |
| Chênh đạt ngưỡng | ≥0,05: 77,2% · ≥0,2: 75,8% · ≥0,3: 72,5% · ≥0,5: 60,2% | ≥0,5: 86,0% · ≥2: 76,2% · ≥3: 68,0% |

  Số câu khác nhau trên 8 mẫu: trung vị 7, trung bình 5,8; greedy có mặt trong mẫu ở 70,5% câu nhắc; độ dài trung bình khoảng 7,2 từ.

### Inferences
- [suy] Với SPICE, ngưỡng dưới khoảng 0,3 gần như không đổi tập cặp (77,2% → 72,5%), vì điểm thưa, không dày. Thứ phải xử là **hoà** (khoảng 23% câu nhắc không có cặp), không phải ngưỡng. Khuyến nghị: bỏ câu nhắc toàn hoà như Bridging và ghi tỉ lệ; ngưỡng chỉ làm độ nhạy (ví dụ ≥0,3).
- [suy] Một câu nhắc một cặp là mặc định đúng: có tiền lệ Bridging, và dữ liệu nhân bản của Tülu 3 không có lợi. Cặp theo thứ hạng hay danh sách (LiPO, LPOI) không có đủ bằng chứng để đưa vào đợt này.
- [suy] Biên độ chênh lớn không có nghĩa tín hiệu chung lớn: số `report/314` cho thấy mẫu trội thắng chủ yếu do dao động lấy mẫu với một câu chuẩn duy nhất. Vậy dự đoán cho cặp mẫu–mẫu là khó học, kể cả trực tuyến. Đây là giả thuyết để kiểm, không được viết thành kết luận.
- [suy] Cặp giống nhau xảy ra thường xuyên ở đây (ví dụ khác đúng một từ cuối). Phép lọc rẻ hơn CHES: ghi khoảng cách sửa chuỗi của từng cặp, báo kết quả phân theo khoảng cách. CHES thì cần gradient/embedding, chỉ chạy nếu thấy log-p chosen giảm.

### Gaps
- Không thấy phép so công bố nào về ngưỡng chênh tối thiểu, cách xử lý hoà, hay số cặp mỗi câu nhắc trên phần thưởng kiểu SPICE/CIDEr. Mọi lựa chọn ở đây là [suy].

## 4. Công cụ: LLaMA-Factory, axolotl, TRL, Unsloth với Qwen2.5-VL

### Takeaway
Chỉ LLaMA-Factory có đường ORPO + Qwen2.5-VL đã chạy thật trong chính dự án. ORPOTrainer của TRL đã ở `trl.experimental` từ v0.26.0 và trong mã không có `pixel_values`. DPOTrainer ở TRL 0.29.1 vẫn ổn định và có vision. Không có công cụ nào sẵn cho "ORPO + sinh 8 mẫu + chọn theo SPICE", nên hướng rẻ nhất là sửa script của dự án.

### Cited Findings
| Công cụ | ORPO | Vision với ORPO | Nguồn |
|---|---|---|---|
| **TRL** | `ORPOTrainer` chuyển sang experimental ở v0.26.0 (9/12/2025, PR #4480); alias deprecated bị xoá ở v0.29.0 (25/2/2026, PR #5050). Tệp `trl/experimental/orpo/orpo_trainer.py` có ở tag v0.29.1. Tham số `beta` mặc định 0,1 | **Không có `pixel_values`** trong tệp ở v0.29.1 lẫn nhánh main (đếm bằng grep 3/11); tài liệu cũng không nhắc vision | [Release notes](https://github.com/huggingface/trl/releases), [mã v0.29.1](https://github.com/huggingface/trl/blob/v0.29.1/trl/experimental/orpo/orpo_trainer.py), [tài liệu](https://github.com/huggingface/trl/blob/main/docs/source/orpo_trainer.md) |
| **TRL DPOTrainer** | Không có odds ratio trong `loss_type` | **Có**: tag v0.29.1 ở `trl/trainer/dpo_trainer.py`, nhận `image`/`images`, tài liệu ví dụ Qwen2.5-VL-3B-Instruct | [Mã v0.29.1](https://github.com/huggingface/trl/blob/v0.29.1/trl/trainer/dpo_trainer.py), [tài liệu](https://github.com/huggingface/trl/blob/main/docs/source/dpo_trainer.md) |
| **TRL OnlineDPOTrainer** | Không; experimental từ v0.26.0 (PR #4473). `num_generations = 2` ghi cứng ở v0.29.1; `reward_funcs` nhận mô hình hoặc hàm | Có `is_vision_model`; đã có lỗi VLM sửa ở bản sau (v1.16.0) | [Mã v0.29.1](https://github.com/huggingface/trl/blob/v0.29.1/trl/experimental/online_dpo/online_dpo_trainer.py), [release notes](https://github.com/huggingface/trl/releases) |
| **LLaMA-Factory** | `pref_loss: orpo`, `pref_beta` mặc định 0,1, `use_ref_model` tự tắt khi orpo/simpo. Log-p chuẩn hoá theo độ dài. `pyproject` nhánh main ghi `trl>=0.18.0,<=0.24.0` | README ghi Qwen2.5-VL và ORPO riêng từng mục, không có câu nào nối hai thứ | [finetuning_args](https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/hparams/finetuning_args.py), [trainer dpo](https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/train/dpo/trainer.py), [README](https://github.com/hiyouga/LLaMA-Factory) |
| **Axolotl** | Có `rl: orpo`, `orpo_alpha` | Mục giới hạn multimodal ghi "Not supported: ORPO, SimPO, EBFT..." | [Tài liệu RLHF](https://docs.axolotl.ai/docs/rlhf.html); trang multimodal không mở được |
| **Unsloth** | Tài liệu nói ORPO chạy được, có notebook Llama 3 | Trang này không nhắc vision; không thấy bằng chứng ORPO + vision | [Tài liệu Unsloth](https://unsloth.ai/docs/basics/reasoning-grpo-and-rl/reinforcement-learning-dpo-orpo-and-kto) |

- Phiên bản hiện tại của TRL là 1.17.1 (30/10/2026), và KTO đã lên gói chính ở v1.8.0; v1.17.0 còn có thay đổi cho ví dụ ORPO — [release notes](https://github.com/huggingface/trl/releases). Dự án đang dùng 0.29.1 — `report/reports/Baseline RL so với GRPO.md`.
- Đường đã chạy [nội bộ]: LLaMA-Factory pin `c4e09c7cbe18…`, `stage: dpo`, `pref_loss: orpo`, `pref_beta: 0.1`, lr 2e-5, trên Qwen2.5-VL-3B với adapter S2, A100 khoảng 21–25 s/bước, cỡ lô 1, trainer ghép cặp zero mọi dropout, liger không kích hoạt — `harness/train_config_orpo.yaml`, `CLAUDE.md` mục trạng thái 23/8.
- Một báo cáo môn học CS231n (không bình duyệt) dùng ORPO cho VQA và theo tóm tắt tìm kiếm không thấy khác DPO về chất lượng; tôi chưa đọc bản đầy đủ — [báo cáo](https://cs231n.stanford.edu/2024/papers/visual-question-and-answering-preference-alignment-with-orpo-and.pdf).

### Inferences
- [suy] Hai đường khả thi. (a) Ngoại tuyến: dựng cặp, đưa vào LLaMA-Factory pin cũ. Rẻ về mã, nhưng khác vòng lặp, khác dtype, khác trainer so với `grpo_luoi.py`, và TRL/transformers cũng khác. (b) Sửa `_scripts/314/ds_gadpo314/ga_dpo.py`, vốn đã có vision + NLL, bỏ tham chiếu, đổi số hạng DPO thành odds ratio với `log1mexp` như TRL, thêm fp16 cho T4. (b) tốt hơn cho hàng so sánh: cùng đường đọc dữ liệu và chấm với các lượt A5/A6, đúng như dòng B6 ở `report/reports/Baseline RL so với GRPO.md`.
- [suy] Công thức có một lỗi số học dễ dính: TRL đã phải sửa "catastrophic cancellation" (PR #4763, v0.27.0). Phải chép `log1mexp`, đừng viết `log(1−exp(x))` trần; LLaMA-Factory dùng `log1p(-exp(x))` trần, nên ở pin cũ cần kiểm số với P gần 1. Với fp16 càng phải tính phần này ở float32.
- [suy] Phải thêm một dòng in tiến trình thật: `[orpo] λ, số cặp, số câu nhắc bỏ vì hoà, log-p chosen, log-p rejected, log OR, acc`, để không rơi vào lỗi câm.

### Gaps
- Chưa kiểm collator ghép cặp của LLaMA-Factory nhánh main có giữ ảnh cho cả hai vế hay không; pin cũ đã chạy nên không chặn việc gì. Chưa mở trang axolotl multimodal.
- Chưa đo VRAM/giây mỗi bước của ORPO trên T4 fp16.

## 5. Phê bình: không tham chiếu với LoRA từ SFT, chế độ hỏng, λ, chosen gần rejected

### Takeaway
Rủi ro lớn nhất ở đây không phải λ mà là cặp quá giống và tín hiệu yếu. Bỏ tham chiếu làm mất phanh KL mà ck500 có, nên phải theo dõi độ dài và log-p chosen. Bằng chứng riêng về ORPO từ SFT + LoRA thì không có; hầu hết là suy từ DPO và từ thí nghiệm nội bộ.

### Cited Findings
- Hiệu năng độc lập không vượt SFT rõ ràng: bảng KTO ở mục 1 cho thấy ORPO thua SFT ở MMLU, GSM8k, HumanEval, chỉ hơn ở BBH — [KTO](https://arxiv.org/abs/2402.01306). Bài ORPO lại báo thắng SFT rõ — [ORPO](https://arxiv.org/abs/2403.07691). Hai nguồn khác nhau về thước (benchmark so với GPT-4 win rate) và về mô hình.
- λ: bài gốc cảnh báo biên quá lớn có thể gây suy thoái và làm kém nhóm câu hỏi có đáp án cứng — [ORPO §7.1, Phụ lục E](https://arxiv.org/abs/2403.07691).
- Cặp giống nhau: likelihood displacement — [Razin et al.](https://arxiv.org/abs/2410.08847) (mục 3). Số hạng SFT đỡ được nhưng không tốt bằng lọc dữ liệu, trong thí nghiệm an toàn của bài.
- Xu et al. nêu nguyên nhân gốc của DPO kém là độ phủ hẹp của tập ưu tiên và lệch phân phối; khắc phục bằng SFT thêm, lọc cặp, hoặc sinh mới — [Xu et al.](https://arxiv.org/abs/2404.10719).
- Chơi độ đo khi tối ưu trực tiếp: PG-SPICE "tends to generate ungrammatical sentences, with a lot of repeated phrases" — [Liu et al.](https://arxiv.org/abs/1612.00370). Cùng rủi ro áp cho cặp xếp theo SPICE, nhưng tôi không thấy phép đo riêng cho ORPO.

### Inferences
- [suy] So với ck500: ck500 có tham chiếu S1 với β=0,04; ORPO không có. Với LoRA khởi tạo B=0 trên S1 đã hoà, ORPO chỉ bị NLL giữ. Nếu chosen là mẫu của chính mô hình thì NLL không còn neo vào câu chuẩn nên có thể tự củng cố phong cách đang lệch. Đây là khác biệt thiết kế cần báo, không phải lỗi. Cần log KL với S1 (chỉ để đo, không cho vào hàm mất mát) và độ dài câu.
- [suy] Điểm mạnh thực dụng của ORPO cho bài này: bỏ được mô hình tham chiếu nên có thể tiết kiệm VRAM; nhưng ck500 dùng adapter tham chiếu nên phần tiết kiệm nhỏ hơn trường hợp hai mô hình trong bài gốc. Không nên viết "ORPO rẻ hơn" trước khi đo.
- [suy] Báo cáo số liệu phải có tiêu chí "có học" đặt trước theo cách ở `report/reports/Baseline RL so với GRPO.md` (A6): acc và biên trên cặp giữ riêng. Không đạt thì viết "không học", không viết "thua".

### Gaps
- Không tìm thấy nghiên cứu ORPO tiếp tục từ điểm SFT với LoRA, hay độ nhạy λ trên câu ngắn, hay chosen rất gần rejected riêng cho odds ratio. Không tìm thấy bài ORPO trên chú thích ảnh.

## 6. Chosen nên là câu chuẩn hay mẫu của mô hình, và cách chạy công bằng nhất

### Takeaway
Hai cách trả lời hai câu hỏi khác nhau và nên chạy cả hai. Chosen = câu chuẩn kiểm tra "SFT tiếp có thêm tương phản với lỗi của mô hình có lợi không", SPICE chỉ đóng vai trò chọn rejected. Chosen = mẫu tốt nhất kiểm tra "cùng tín hiệu SPICE với GRPO, đổi mục tiêu tối ưu thì sao". Chỉ cách thứ hai mới là phép so GRPO với ORPO cùng phần thưởng, và mỗi hàng nên có một hàng song sinh λ=0 để tách đúng công của số hạng odds ratio.

### Cited Findings
- Công bố dùng cả hai: Bridging và OAIF lấy cả hai vế từ mô hình — [Bridging](https://arxiv.org/abs/2506.21495), [OAIF](https://arxiv.org/abs/2402.04792). QRPO dùng một mô hình thưởng làm "equal potential signal source" cho mọi phương pháp, nhưng phần này lấy từ [ghi chú dự án](../Baseline%20RL%20so%20v%E1%BB%9Bi%20GRPO/rlhf_preference.md), chưa mở lại [bài](https://arxiv.org/abs/2507.08068). Tülu 3 thấy dữ liệu theo chính sách trên một vế (rejected hoặc chosen từ mô hình SFT ban đầu) tốt hơn hoàn toàn ngoài chính sách — [Tülu 3](https://arxiv.org/abs/2411.15124).
- Bằng chứng về nguồn cặp từ chính dự án: acc giữ riêng 0,46 khi chosen là mẫu trội, 0,76 khi chosen là greedy, chỉ cho thấy mô hình học "tránh mẫu thua" — `report/314_KET_QUA_GADPO_13_10.md` §5. RAFT từ ck500 cũng thua ck500, exec −0,43 [−0,82; −0,04] — `report/314_KET_QUA_RAFT_12_10.md` (qua `CLAUDE.md`).
- Kế hoạch hiện tại ở `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md`: ORPO ở đợt 3; và B6 ở `report/reports/Baseline RL so với GRPO.md` là "ORPO từ S1, mức câu, cùng cặp A6".

### Inferences
[suy] Toàn bộ thiết kế dưới đây là đề xuất của tôi.

**Ba hàng, mỗi hàng một song sinh λ=0 đã có trong lưới**

| Mã đề xuất | Chosen | Rejected | Cách lấy mẫu | Song sinh λ=0 | Trả lời câu gì | Sức nặng khi so GRPO |
|---|---|---|---|---|---|---|
| ORPO-G | Câu chuẩn | Mẫu SPICE thấp nhất của S1 | Ngoại tuyến, 1 lần | A1 SFT tiếp | Thêm tương phản có hơn SFT thuần không. Hữu ích nếu thầy hỏi "phương pháp ORPO chuẩn" | Yếu: chosen điểm tối đa theo định nghĩa, SPICE chỉ chọn rejected |
| ORPO-S | Mẫu SPICE cao nhất | Mẫu SPICE thấp nhất | Ngoại tuyến, 1 lần | A7 RFT một vòng | Cặp giống A6, đối chiếu ORPO với DPO trên cùng cặp | Trung bình: mẫu không theo chính sách hiện tại |
| ORPO-O | Mẫu cao nhất | Mẫu thấp nhất | Mỗi bước từ chính sách hiện tại, G=8 | A8 Online RFT | Phép so **công bằng nhất với ck500**: cùng tín hiệu, cùng ngân sách mẫu. Bản thích nghi của dự án | Mạnh nhất |

Phiên bản bán trực tuyến (sinh lại mỗi s bước) là độ nhạy, chỉ thêm nếu ORPO-O có tín hiệu; Bridging cho thấy bán trực tuyến gần trực tuyến và rẻ hơn. Nếu chỉ chạy được một lượt, chọn ORPO-O. Nếu chạy được hai, thêm ORPO-G, vì đây là cách đọc gần nhất với bài gốc.

**Điều kiện giữ nguyên với ck500**
- Xuất phát từ S1 đã hoà + LoRA mới, cùng 1.000 câu nhắc, G=8, nhiệt độ 1, thưởng SPICE − 0,02·phạt độ dài y như ck500, hạt 101, 500 bước, chấm điểm lưu cuối, không chọn điểm lưu. Nếu thưởng GRPO có phạt độ dài thì cặp phải xếp bằng đúng thưởng đó, không bằng SPICE trần.
- lr 1e-5 như ck500 làm chính. Nếu không đạt tiêu chí có học thì có thể thử lr cao hơn một lần, nhưng phải khai đổi sau khi thấy log, như đã khai ở `report/314`.
- Cỡ cập nhật: cùng số câu nhắc mỗi update. Các cặp ngoại tuyến chỉ thấy một lần trong 500 bước; đây là điều kiện công bằng về ngân sách nhưng có thể bất lợi cho ngoại tuyến vốn thường chạy nhiều epoch. Lượt 52 bước ở `report/314` không học vì thiếu bước, nên trước khi đọc kết quả phải chạy phép kiểm học thuộc trên ~200 cặp.

**Luật dựng cặp**
- 1 cặp/câu nhắc, tốt nhất–kém nhất; hoà trong nhóm thì lấy ngẫu nhiên theo hạt cố định. Toàn nhóm bằng điểm thì bỏ câu nhắc (như lợi thế 0 của GRPO); y_w = y_l sau chuẩn hoá khoảng trắng thì coi là không có cặp. Không đặt ngưỡng ở lượt chính; báo tỉ lệ bỏ. Độ nhạy: chênh ≥0,3.
- Khai rõ một khác biệt không tránh được: GRPO dùng 8 mẫu cho gradient, ORPO theo khuôn này chỉ dùng 2 trong 8, nên ngân sách **sinh** bằng nhau nhưng ngân sách **gradient** thì không.

**λ**
- λ=0,1 làm lượt chính, không quét trên test: đúng với Mistral của bài, mặc định của TRL và LLaMA-Factory, và MIN-DESC. Vì câu ngắn có P cao (mục 1), λ=0,1 có thể đã mạnh hơn bài gốc. Độ nhạy một lần: λ=1,0 (ở bài gốc có hành vi khác rõ). Nếu thầy hỏi về λ thì có trả lời bằng số thay vì lý thuyết.

**Những gì phải đo**
- Train: số cặp, % bỏ, log-p chosen, log-p rejected, log OR, acc, độ dài câu, KL so S1 chỉ để theo dõi, chênh SPICE của cặp, khoảng cách sửa chuỗi của cặp.
- Test: gói chấm chung như mọi lượt (exec, D.3, AitW đầy đủ trên 4.463 bước; KTC ghép cặp và McNemar so ck500, S1 và **hàng song sinh λ=0**; 7 độ đo văn bản; bước không chạm; đo hình thức câu).

**Cách viết**
- "ORPO" trần chỉ dùng cho ORPO-G ở mức gần gốc, kèm câu "chạy tiếp từ S1, khác bài gốc vốn chạy thẳng từ pretrained". ORPO-O phải viết "ORPO với cặp lấy mẫu theo chính sách (bản thích nghi)". Không viết "ORPO trực tuyến" như một phương pháp đã có.
- Không viết "GRPO hơn ORPO" từ một hạt. Nếu ORPO-O ngang ck500, câu đúng là "không phân biệt được". Nếu không đạt tiêu chí có học, viết "không học" và không có số test.
- MIN-DESC không phải cùng phép so: khác điểm đầu (S2), mức (khai báo, không phải câu), câu y hệt hai vế, không có thưởng liên tục. Người kiểm MIN-DESC sẽ nói rõ hơn.

**Câu trả lời thầy** (gợi ý, chưa có số): ORPO được thiết kế cho cặp có sẵn và không có bản trực tuyến được công nhận, nên không phải lựa chọn hiển nhiên cho thưởng liên tục; dự án đã dùng nó ở mức khai báo, và lưới sẽ thêm ba hàng trên để đo thay vì lập luận.

### Gaps
- Chưa có số nào cho ba hàng này. Câu "ORPO-O công bằng nhất" là lập luận thiết kế, không phải kết quả.
- Chưa xác minh thưởng trong `grpo_luoi.py` có đúng mô tả 0,02·phạt độ dài cho mọi lượt, và số prompt mỗi update; lấy từ `CLAUDE.md` và báo cáo của dự án. Phải đọc mã trước khi viết script.
- Tín hiệu trên `report/314` lấy từ ck500, không phải S1; chưa biết S1 có khác không.
