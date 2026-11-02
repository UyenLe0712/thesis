# 323 — Debate và action final: vì sao GRPO, vì sao SPICE, vì sao ACE (1/11/2026)

> File tự chứa. Viết sau buổi gặp thầy. Câu hỏi của thầy: *đã khảo sát các phương pháp tương tự GRPO
> chưa, vì sao chọn GRPO; vì sao chọn SPICE mà không chọn độ đo khác; vì sao chọn ACE, đã khảo sát
> chưa. Bài này chưa đủ mạnh.*
> **Phạm vi:** chưa sửa luận văn. Làm hết các việc dưới đây, ghi kết quả vào `report/320`, rồi mới sửa
> `thesis/` trong một lượt riêng.
> Nhãn: **[test]** là số test, trích được. **[val]** là số val, chỉ để xếp hạng, không trích.
> **[đã kiểm]** nghĩa là venue đã tra tận nguồn ngày 1/11. **[cần kiểm]** nghĩa là chưa tra.

---

## 0. Kết luận trước

1. Thầy hỏi đúng chỗ yếu. Luận văn **có số** cho từng lựa chọn nhưng mới trình khoảng một phần ba.
   **Phần khảo sát tài liệu gần như chưa có**: ch2 §2.3 chỉ giới thiệu GRPO, còn ch4 có hai câu
   "Cơ sở lựa chọn".
2. Debate tìm ra **ba lỗ thật**. Viết lại câu chữ không vá được ba lỗ này, phải chạy thêm:
   - **(L-SEED)** Phép so SPICE với CIDEr-D (−0,69) **nằm trong nhiễu hạt giống của chính GRPO**.
     Hai hạt ck500 đã chênh nhau 0,72. Trung bình hai hạt SPICE là 60,30, còn CIDEr-D một hạt là
     59,96. Lượt CIDEr-D (A2) còn **lệch ba biến** so với ck500: 2.000 câu nhắc thay vì 1.000,
     A100 bf16 thay vì T4 fp16, và có ghi log CTG.
   - **(L-ALGO)** Chưa có thuật toán RL trực tuyến nào khác chạy **cùng phần thưởng SPICE**.
     RAFT và GA-DPO có chạy nhưng đều xuất phát từ ck500, nên đó là phép so "học thêm sau GRPO",
     không phải "thay GRPO". Phép so hợp lệ nhất là **SCST**, chuẩn ngành của sinh chú thích ảnh.
   - **(L-ACE)** ACE chưa được so với **mốc đơn giản nhất của nhánh truy hồi**: lấy thẳng câu
     ví dụ, không cần mô hình sinh. Thiếu mốc này thì hội đồng có thể nói "ACE chỉ là sao chép".
3. "Chưa đủ mạnh" không sửa được bằng cách đẩy mức tăng +1,55 lên cao. Muốn bài mạnh hơn, mỗi lựa
   chọn phải đứng trên ba chân: **khảo sát tài liệu → phương án thay thế chạy cùng điều kiện → lý
   do cơ chế**. Phần lớn đã có số, chỉ cần thêm 5–6 lượt GPU và 4 phân tích 0 GPU.

---

## 1. Tài sản đã có (để không chạy lại)

| lựa chọn | phương án thay thế đã chạy | kết quả | nguồn |
|---|---|---|---|
| tín hiệu | SPICE ghép ngẫu nhiên (xao101), cùng 500 bước | 59,11 = S1; ck500 − xao101 **+1,55 [+0,81; +2,30]** [test] | `report/320` §2 |
| tín hiệu | CIDEr-D, 500 và 1.000 bước (A2) | 59,96 / 59,98; ck500 − A2_500 +0,69 [+0,02; +1,34] [test]; ⚠️ lệch ba biến | `report/299` |
| tín hiệu | SPICE + người nghe Phi-4 (3 biến thể, train tiếp ck500) | không qua sàng; tnghe exec +0,30, SPICE −1,53 [val] | `report/289` |
| tín hiệu | phần thưởng toạ độ `<point>` (GRPO-point) | exec +0,02 so MIN [test] | PL A.4 |
| tín hiệu | oracle 8 mẫu theo từng độ đo | SPICE +5,22 là oracle **yếu nhất**; CIDEr-D +9,64, ROUGE-L +8,84, BLEU-4 +7,63 [val] | `report/252` |
| thuật toán | RAFT (lọc mẫu tốt rồi SFT, từ ck500) | exec −0,43 [−0,82; −0,04] [test] | `report/314` |
| thuật toán | GA-DPO (cặp ngoại tuyến, từ ck500) | không học; cặp "cải thiện" chỉ 0,46, ngang tung đồng xu | `report/314` GA-DPO |
| thuật toán | ORPO tầng khai báo (MIN-DESC) | +0,94 so S1, p=0,11 [test] | PL A.2 |
| thuật toán | MBR lúc suy luận | thua S1 [val] | `report/208` |
| hậu xử lý | ra_k4 dùng mọi bước (sinh có truy hồi) | exec −1,25 [−2,06; −0,44] [test] | Bảng 6.4 |
| hậu xử lý | luật ghép R0–R4 | chọn R3 trên val; R3 test 60,68, ngang ck500 [test cho R3] | `report/304` §5 |
| hậu xử lý | CW-RA (mô hình tự quyết chép hay viết) | thua 7/7 độ đo văn bản; exec −2,13 [test] | `report/310` |
| hậu xử lý | RA-GRPO | không qua bước kiểm G0 | `report/312` |
| hậu xử lý | RAF (chọn giữa S1 và ck500) | 7/13 cột hơn ck500, 5 cột hành vi âm nhẹ [test] | `report/298` |
| hậu xử lý | TAGE (sửa câu theo vùng ảnh cục bộ) | exec −0,43 so ck500 [test] | PL A.7 |

---

## 2. Debate câu 1 — vì sao GRPO

**Bảo vệ.**
- Phần thưởng là độ đo **không khả vi**, chỉ có điểm cho cả câu. Muốn dùng thì phải học tăng
  cường kiểu policy gradient, như SCST [CVPR 2017, đã có trong bib] và SPIDEr [Liu, ICCV 2017,
  đã kiểm].
- GRPO **không cần mô hình giá trị**. PPO cần thêm một critic cỡ mô hình chính, không vừa T4/L4
  với VLM 3B. Ahmadian và cộng sự [ACL 2024, đã kiểm] cho thấy các phương pháp kiểu REINFORCE
  (RLOO) bằng hoặc hơn PPO, DPO và RAFT trong RLHF, nên bỏ critic là lựa chọn có tiền lệ, không
  chỉ là chuyện tiết kiệm.
- Học theo cặp ngoại tuyến **đã thử và không đạt** (GA-DPO, ORPO). Lý do đo được: với câu hướng
  dẫn ngắn, cặp "mẫu tốt hơn" lấy từ chính mô hình gần như không chứa tín hiệu chung (0,46).
- Lọc mẫu tốt rồi SFT (RAFT) **thua** ck500 [test].
- GRPO đã được dùng cho sinh chú thích ảnh, thắng SCST trên COCO [arXiv 2503.01333, **preprint**],
  và cho GUI agent: UI-R1 [AAAI 2026, đã kiểm], GUI-R1 [arXiv, chưa thấy venue].

**Phản biện (đóng vai thầy).**
- "RAFT và GA-DPO xuất phát từ ck500. Đó là học thêm sau GRPO, không phải thay GRPO. Vậy chưa có
  phép so nào giữ nguyên phần thưởng và chỉ đổi thuật toán."
- "SCST mới là chuẩn của sinh chú thích. Em chưa so với nó."
- "GRPO và RLOO gần như giống nhau. Em chọn GRPO thì được gì?"
- "DeepSeekMath, bài gốc của GRPO, là preprint."

**Phán quyết.**
- Đòn thứ nhất và thứ hai **đúng**. Cần chạy **SCST với phần thưởng SPICE**, cùng điểm xuất phát
  S1/101, cùng 1.000 câu nhắc, cùng 500 bước, cùng β và lr. SCST dùng câu greedy làm mốc thay cho
  trung bình nhóm. Một lượt này trả lời cả hai đòn.
- RLOO **không cần chạy**. Với G = 8, RLOO chỉ khác GRPO ở hai điểm: mốc bỏ-một và không chia độ
  lệch chuẩn. Phần khảo sát nêu điểm này và trích Ahmadian. Nếu hội đồng hỏi thêm thì có câu trả
  lời cơ chế, không cần số.
- PPO **không chạy**. Lý do là bộ nhớ (critic) cộng tiền lệ ACL 2024, ghi thẳng như vậy.
- Về venue: trích GRPO kèm nhãn preprint, đồng thời trích DeepSeek-R1 [Nature 2025, cần kiểm]
  làm nguồn đã bình duyệt cho cùng thuật toán.

## 3. Debate câu 2 — vì sao SPICE

**Bảo vệ.**
- Tiền lệ: SPICE là một nửa của SPIDEr [ICCV 2017]. Zhao và cộng sự [EACL 2021] khuyên dùng SPICE
  để xếp hạng hệ thống sinh chỉ dẫn.
- Cơ chế: câu hướng dẫn ngắn (khoảng 7 từ) và nội dung chính nằm ở **đối tượng + thuộc tính + quan
  hệ** ("the search icon at the top"). SPICE so đúng ba thứ đó trên đồ thị ngữ cảnh. CIDEr-D
  thưởng n-gram hiếm theo TF-IDF, nên với một câu chuẩn mỗi bước dễ thưởng việc chép đúng cụm hiếm
  hơn là gọi đúng phần tử.
- Số [test]: SPICE ghép ngẫu nhiên = S1, tức cái giúp là tín hiệu thật. Thêm một điểm đáng chú ý:
  thưởng SPICE cho **CIDEr-D cao hơn** chính lượt tối ưu CIDEr-D (430,05 so 428,27).

**Phản biện.**
- "Hai hạt ck500 chênh 0,72, mà SPICE chỉ hơn CIDEr-D 0,69. Đó là nhiễu." **Đúng (L-SEED).**
- "A2 khác ck500 ba biến, phép so không sạch." **Đúng.**
- "Oracle của em cho thấy SPICE là độ đo yếu nhất. Sao vẫn chọn?" Câu trả lời có sẵn: oracle đo
  khả năng **chọn** câu tốt trong 8 mẫu, không đo khả năng **dẫn** chính sách. CIDEr-D có oracle
  mạnh hơn nhưng train thật thì không hơn. Cần trình cả hai số cạnh nhau, không giấu oracle.
- "Còn SPIDEr, đúng là cái người ta hay dùng? Còn BERTScore hay độ đo dựa trên embedding?"
  **Chưa có số.**
- "Sao không thưởng thẳng bằng executability?" Có câu trả lời: (1) đưa bộ trỏ dùng để chấm vào
  phần thưởng thì mô hình tối ưu theo đúng dụng cụ chấm, gây Goodhart; (2) mỗi mẫu tốn một lần
  gọi bộ trỏ, 8 mẫu × 500 bước; (3) bản gần nhất đã thử là thưởng người nghe Phi-4, không qua sàng
  [val]. Đủ để trình như lựa chọn đã cân nhắc, không cần chạy.
- "CLIPScore?" Ảnh 224 px không đọc được chữ trên màn hình, nên loại bằng lý do, không cần chạy.

**Phán quyết.** Phải chạy lại phép so phần thưởng **trên cùng một kịch bản** (`grpo_spice.py`,
1.000 câu nhắc, cùng máy), **hai hạt cho mỗi phần thưởng chính**. Mỗi phần thưởng đại diện cho
một họ độ đo:

| họ độ đo | phần thưởng | trạng thái |
|---|---|---|
| đồ thị ngữ cảnh | SPICE | có 101 và 202 |
| n-gram đồng thuận | CIDEr-D | **chạy lại sạch** cho hạt 101 và 202 |
| kết hợp (tiền lệ trực tiếp) | SPIDEr = (SPICE + CIDEr-D/10)/2 | chạy hạt 101, thêm 202 nếu sát |
| embedding | BERTScore (roberta-large, rescaled) | chạy hạt 101, thêm 202 nếu sát |
| hành vi / người nghe | Phi-4 | đã có [val], trình như hướng đã thử |
| kiểm sàn | SPICE ghép ngẫu nhiên | đã có [test] |

Thêm một phân tích **0 GPU** cho cơ chế: trên dữ liệu 8 mẫu C1, với từng độ đo tính (a) tỉ lệ hoà
trong nhóm, (b) tương quan hạng với exec trong nhóm, (c) oracle exec. Từ đó chỉ ra đặc tính nào
của độ đo làm phần thưởng tốt, không chỉ báo một con số oracle.

## 4. Debate câu 3 — vì sao ACE

**Bảo vệ.**
- Tiền lệ: sinh văn bản có truy hồi. SmallCap [CVPR 2023, đã kiểm] và EXTRA [EACL 2023, đã kiểm]
  đưa câu truy hồi vào đầu vào. Chính EXTRA ghi nhận mô hình có lúc **chép nguyên câu** và câu
  truy hồi sai có thể dẫn sai. ACE xử lý đúng rủi ro đó bằng điều kiện lựa chọn. Thêm retrieve-and-
  edit [NeurIPS 2018, đã kiểm] và cơ chế chép (CopyNet ACL 2016, pointer-generator ACL 2017, cần kiểm).
- Đã thử các cách khác [test]: dùng mô hình truy hồi cho mọi bước thì exec −1,25; để mô hình tự
  quyết chép hay viết (CW-RA) thì −2,13; RL có truy hồi (RA-GRPO) không qua G0; sửa câu theo vùng
  ảnh (TAGE) −0,43. Chỉ ACE vừa giữ exec vừa tăng cả bảy độ đo văn bản.

**Phản biện.**
- "ACE không tăng exec, chỉ tăng độ đo văn bản. Đó là mẹo hậu xử lý." Trả lời: ACE được thiết kế
  để **cải thiện câu mà không đụng quyết định thao tác**, và kết quả đúng như thiết kế. Phải viết
  rõ ACE nhắm vào chất lượng văn bản chứ không nhắm vào exec.
- "Chỉ cần lấy thẳng câu ví dụ là được, cần gì mô hình sinh?" **Chưa có số (L-ACE).**
- "Luật R3 chọn trên val trong 4 ứng viên, còn R0, R2, R4 trên test thì sao?" Đã có câu dự đoán
  của cả năm luật trên test. Exec tính được **0 GPU** vì mọi câu đều là câu ck500 hoặc câu ra_k4,
  mà cả hai đã được chấm trên test (cần kiểm khoá (bước, câu) khớp trước khi tin).
- "Vì sao TF-IDF mà không dùng truy hồi dày (embedding)?" Đổi bộ truy hồi phải sinh lại câu, tốn
  GPU. Xếp vào bậc B.

**Phán quyết.** Chạy mốc "chép thẳng câu ví dụ" với hai biến thể:
- **NN-1**: lấy câu ví dụ đứng đầu, chỉ thay khi cùng loại thao tác với câu GRPO-SPICE;
- **NN-vote**: lấy câu xuất hiện nhiều nhất trong 4 câu ví dụ, cùng điều kiện.

Phần dựng câu tốn 0 GPU. Chỉ các câu mới cần UGround chấm trên Kaggle T4. Kèm bảng R0–R4 trên test
khai rõ là R3 được chọn trên val.

## 5. "Bài chưa đủ mạnh" — cái gì làm mạnh hơn, cái gì không

| hướng | quyết | lý do |
|---|---|---|
| bảng "không gian thiết kế": mỗi lựa chọn × phương án × số test | **làm** | biến 15 hướng đã thử thành bằng chứng hệ thống; số đã có gần đủ |
| khảo sát tài liệu có bảng so sánh cho ba thành phần | **làm** | đúng câu thầy hỏi |
| hai hạt cho phép so phần thưởng | **làm** | vá L-SEED, nếu không phép so chính dễ bị bác |
| SCST | **làm** | vá L-ALGO |
| mốc chép thẳng cho ACE | **làm** | vá L-ACE |
| phân tích cơ chế SPICE (tuple đối tượng / thuộc tính / quan hệ nào tăng) | **làm**, 0 GPU, CPU Java | trả lời "SPICE giúp ở đâu" bằng số |
| backbone thứ hai | không | ~23 h A100 SFT + GRPO, đã quyết 25/10, ghi thành giới hạn |
| chấm tay | không, trừ khi user đổi ý | user quyết 6/9 |
| RLOO, PPO, CLIPScore, thưởng exec bằng UGround | không chạy, trình bằng lý do | đã nêu ở §2–§3 |

---

## 6. ACTION FINAL

Thứ tự đi từ rẻ đến đắt. Bậc máy theo thủ tục chọn máy của CLAUDE.md. Mọi kết quả, ra sao cũng
báo, ghi vào `report/320` mục mới. **Không sửa `thesis/`** cho tới khi xong §6.4.

### 6.1 Bậc 0 — không GPU (WSL hoặc Kaggle CPU)

| # | việc | ra | ghi chú |
|---|---|---|---|
| Z1 | Bảng "không gian thiết kế" gom từ §1, mỗi dòng có số + nguồn + nhãn [test]/[val] | `report/324_BANG_KHONG_GIAN_THIET_KE.md` | số val chỉ ghi chiều, không ghi số |
| Z2 | Đặc tính phần thưởng trên 8 mẫu C1: tỉ lệ hoà, Kendall τ với exec trong nhóm, oracle — cho SPICE, CIDEr-D, SPIDEr, BLEU-4, ROUGE-L, METEOR, BERTScore | `runs/thuong_dac_tinh/` | dữ liệu `runs/c1/exec8/`; [val], chỉ dùng để giải thích cơ chế |
| Z3 | ACE: exec + 7 độ đo văn bản cho R0, R2, R4 trên test; dựng câu NN-1 và NN-vote | `runs/ace_ablation/` | trước hết kiểm khoá (bước, câu) của ra_k4 test raw khớp; câu nào chưa chấm thì gom sang G5 |
| Z4 | Phân tích SPICE theo loại tuple (đối tượng / thuộc tính / quan hệ), ck500 so S1 | `runs/spice_tuple/` | Kaggle CPU (jar CoreNLP như lượt trước) |
| Z5 | Khảo sát tài liệu: ba bảng (thuật toán RL · độ đo làm phần thưởng · sinh có truy hồi và chép), **tra venue tận nguồn từng mục [cần kiểm]** ở §7 | `report/325_KHAO_SAT_TAI_LIEU_GRPO_SPICE_ACE.md` | không trích preprint như bài đã bình duyệt |

### 6.2 Bậc 1–2 — GPU (cần user duyệt trước khi đẩy)

> ⛔ **Mục 6.2 đã bị §8 thay (1/11 tối).** Thầy yêu cầu so **cả họ RL** và **nhiều độ đo**, nên lưới
> lượt chạy mở rộng. Đọc §8, chỉ giữ 6.2 để tra lịch sử.

Mọi lượt train dùng **`harness/grpo_spice.py`**, thêm lựa chọn `--reward` (cider, spider,
bertscore) và `--algo scst`. Giữ nguyên: S1/101 hoà làm điểm xuất phát, LoRA mới cùng cỡ,
1.000 câu nhắc hạt 101, G = 8, 500 bước, lr 1e-5, β 0,04, phạt câu dài. **Cùng một loại máy cho
mọi lượt mới.** Trước khi đẩy lượt thật, ô thăm dò đo s/bước và VRAM đỉnh trên mẫu dài nhất ở
T4 và L4, rồi chọn theo luật 1,5×.

| # | lượt | hạt | trả lời | ghi chú |
|---|---|---|---|---|
| G1 | CIDEr-D, kịch bản sạch | 101 | L-SEED | thay A2 làm phép so chính; A2 lùi về phụ |
| G2 | CIDEr-D, kịch bản sạch | 202 | L-SEED | |
| G3 | SPIDEr | 101 | tiền lệ trực tiếp | |
| G4 | BERTScore | 101 | họ embedding | roberta-large trong vòng thưởng, phải đo VRAM |
| G5 | SCST + SPICE | 101 | L-ALGO | mốc = câu greedy của chính chính sách. ⚠️ Không làm được bằng cách trừ mốc trong hàm thưởng vì GRPO trừ trung bình nhóm sẽ khử mất mốc, nên phải viết lớp trainer con. Kiểm trên mô hình tí hon CPU trước |
| G6 | sinh câu + chấm UGround test 4.463 bước cho G1–G5, cộng câu NN của Z3 | — | — | Kaggle T4, chia bốn tài khoản (`kg uyenle|trang|trang2|ca`) |
| G7 | độ đo văn bản cho G1–G5 | — | — | Kaggle CPU |
| G8 | **có điều kiện**: hạt 202 cho G3/G4/G5 nào có exec trong khoảng ±1,0 so trung bình hai hạt SPICE (60,30) | 202 | L-SEED | quyết sau khi có G6 |

Cách đọc, ghi trước khi có số:
- Phép so phần thưởng đọc trên **trung bình hai hạt** khi có hai hạt; phép ghép cặp từng hạt in
  kèm. Nếu CIDEr-D sạch ra ngang SPICE thì báo thẳng: "SPICE không hơn CIDEr-D về exec; ưu thế
  nằm ở độ đo văn bản" (hoặc không có ưu thế), và sửa lập luận ch4 theo số.
- SCST đọc so với ck500 cùng hạt 101 và so với S1.
- Không chọn lại phương pháp tiêu đề theo kết quả này trừ khi một phần thưởng mới hơn SPICE ở
  **cả hai hạt**. Nếu vậy thì báo user quyết, không tự đổi.

### 6.3 Bậc B — chỉ làm khi còn thời gian

- ACE với truy hồi dày (bge-m3) thay TF-IDF: sinh lại ra_k4 + chấm, khoảng 6 h T4.
- Hạt 202 cho phần thưởng không rơi vào luật G8.

### 6.4 Sau khi xong tất cả

Một lượt sửa luận văn duy nhất, theo kế hoạch riêng (không viết ở đây):
- ch2: ba mục khảo sát có bảng;
- ch4: "Cơ sở lựa chọn" viết lại theo ba chân (tiền lệ → phương án → cơ chế);
- ch6: Bảng 6.3 mở rộng thành bảng phần thưởng hai hạt + SCST, Bảng 6.4 thêm NN-1, NN-vote, R0–R4;
- Phụ lục A: bảng không gian thiết kế.

### 6.5 Ước lượng

| phần | máy | thời gian | tiền |
|---|---|---|---|
| Z1–Z5 | WSL / Kaggle CPU | 2–3 ngày làm | 0 |
| G1–G5 train | T4 hoặc L4 theo ô thăm dò | ck500 trên T4 mất ~22 h/lượt (160 s/bước); L4 [chưa đo] | T4: 0 đồng nhưng ~110 h hạn mức, chia bốn tài khoản; L4: trả Colab |
| G6–G7 | Kaggle T4 / CPU | ~5,6 h × 5 lượt + CPU | 0 |
| G8 | như G1 | 0–3 lượt | tuỳ |

Nếu dùng T4 trên bốn tài khoản song song thì G1–G7 xong trong khoảng 1 tuần. Kịp trước phiên
báo cáo SOICT 4–5/12, và trước khi sửa luận văn.

---

## 7. Danh sách tài liệu cho Z5

| tài liệu | dùng cho | venue |
|---|---|---|
| Rennie et al., SCST | RL cho sinh chú thích | CVPR 2017 (có trong bib) |
| Liu et al., SPIDEr | SPICE làm phần thưởng | ICCV 2017 [đã kiểm], có trong bib |
| Ahmadian et al., Back to Basics (RLOO) | REINFORCE ≥ PPO; RLOO > DPO, RAFT | ACL 2024 [đã kiểm] |
| Shao et al., DeepSeekMath (GRPO) | thuật toán | arXiv 2024, **preprint** |
| DeepSeek-R1 | GRPO bản bình duyệt | Nature 2025 [cần kiểm] |
| Liang, GRPO for Image Captioning | GRPO > SCST trên COCO | arXiv 2503.01333, **preprint** |
| UI-R1 | GRPO cho GUI agent | AAAI 2026 [đã kiểm] |
| GUI-R1 | GRPO cho GUI | arXiv 2504.10458, chưa thấy venue |
| Schulman et al., PPO | mốc có critic | arXiv 2017, preprint |
| Rafailov et al., DPO | cặp ngoại tuyến | NeurIPS 2023 [cần kiểm] |
| Hong et al., ORPO | cặp ngoại tuyến | EMNLP 2024 [cần kiểm] |
| Dong et al., RAFT | lọc mẫu rồi SFT | TMLR 2023 [cần kiểm] |
| Singh et al., ReST-EM | lọc mẫu rồi SFT | TMLR 2024 [cần kiểm] |
| Li et al., ReMax | REINFORCE cho LLM | ICML 2024 [cần kiểm] |
| Vedantam et al., CIDEr · Anderson et al., SPICE | độ đo | CVPR 2015 · ECCV 2016 (có trong bib) |
| Zhang et al., BERTScore | họ embedding | ICLR 2020 (có trong bib) |
| Hessel et al., CLIPScore | lý do loại | EMNLP 2021 [cần kiểm] |
| Cho et al., CLIP reward cho captioning | phần thưởng học được | Findings NAACL 2022 [cần kiểm] |
| Zhao et al. | SPICE để xếp hạng hệ thống | EACL 2021 (có trong bib) |
| Ramos et al., SmallCap | truy hồi trong prompt | CVPR 2023 [đã kiểm], có trong bib |
| Ramos et al., EXTRA | truy hồi + hiện tượng chép nguyên câu | EACL 2023 [đã kiểm] |
| Hashimoto et al., Retrieve-and-Edit | truy hồi rồi sửa | NeurIPS 2018 [đã kiểm] |
| Gu et al., CopyNet · See et al., pointer-generator | cơ chế chép | ACL 2016 · ACL 2017 [cần kiểm] |
| Yasunaga et al., RA-CM3 | truy hồi đa phương thức | ICML 2023 [cần kiểm] |
| Khandelwal et al., kNN-LM | truy hồi lúc suy luận | ICLR 2020 [cần kiểm] |

---

## 8. ACTION FINAL v2 — theo yêu cầu cụ thể của thầy (1/11 tối, thay §6.2)

Thầy chưa đồng ý và yêu cầu ba việc:
1. so GRPO với **các thuật toán cùng họ RL**, bằng số;
2. so SPICE với **các độ đo khác** khi làm phần thưởng, bằng số;
3. nếu GRPO + SPICE vẫn tốt nhất thì phải **giải thích vì sao tốt nhất trên AndroidControl**.

Thiết kế dưới đây trả lời cả ba. Nguyên tắc: **mỗi lần chỉ đổi một yếu tố**, mọi thứ khác giữ
đúng như ck500.

### 8.1 Trục 1 — thuật toán (giữ phần thưởng SPICE)

Mọi biến thể trên **cùng một vòng huấn luyện**, chỉ khác cách tính lợi thế (advantage). Phép so
khi đó chỉ còn khác đúng cách dùng các câu đã sinh. Riêng PPO cần thêm mô hình giá trị.

| mã | thuật toán | mốc trừ (baseline) | chuẩn hoá | tiền lệ | ghi chú |
|---|---|---|---|---|---|
| A0 | **GRPO** (ck500) | trung bình nhóm 8 câu | chia độ lệch chuẩn nhóm | DeepSeekMath (preprint), DeepSeek-R1 | đã có 2 hạt |
| A1 | **REINFORCE + mốc trượt** | trung bình trượt của phần thưởng | không | Williams 1992 | mốc không phụ thuộc prompt |
| A2 | **SCST** | điểm câu greedy của chính prompt | không | CVPR 2017 | chuẩn sinh chú thích; 8 mẫu + 1 greedy |
| A3 | **RLOO** | trung bình 7 câu còn lại | không | ACL 2024 | |
| A4 | **Dr. GRPO** | trung bình nhóm | **không** chia độ lệch chuẩn | [cần kiểm venue] | tách riêng tác dụng của việc chia std |
| A5 | **PPO** | mô hình giá trị (đầu giá trị trên LoRA) | GAE, clip | arXiv 2017 + InstructGPT NeurIPS 2022 | đắt nhất, đo VRAM trước; tràn L4 thì ghi lý do, lên A100 nếu user duyệt |

Cách viết mã: thêm `--algo {grpo,reinforce,scst,rloo,drgrpo}` vào `grpo_spice.py` bằng một lớp
trainer con ghi đè phần tính lợi thế. ⚠️ Không làm bằng cách sửa hàm thưởng, vì GRPO trừ trung bình
nhóm sẽ khử mất mốc. Kiểm trên mô hình tí hon CPU: với cùng một lô phần thưởng giả, in lợi thế của
năm biến thể và so với công thức tính tay. PPO là kịch bản riêng.

### 8.2 Trục 2 — phần thưởng (giữ GRPO)

| mã | phần thưởng | họ | ghi chú |
|---|---|---|---|
| R0 | **SPICE** (ck500) | đồ thị ngữ cảnh: đối tượng, thuộc tính, quan hệ | đã có 2 hạt |
| R1 | CIDEr-D | n-gram đồng thuận, TF-IDF | **chạy lại sạch** (A2 cũ lệch ba biến) |
| R2 | BLEU-4 (mức câu, làm mượt) | n-gram chính xác | |
| R3 | ROUGE-L | chuỗi con chung dài nhất | |
| R4 | METEOR | khớp từ có đồng nghĩa, gốc từ | Java, đo tốc độ |
| R5 | chrF | n-gram ký tự | |
| R6 | BERTScore | embedding | roberta-large trong vòng thưởng, đo VRAM |
| R7 | SPIDEr | SPICE + CIDEr-D | tiền lệ trực tiếp ICCV 2017 |
| R8 | SPICE ghép ngẫu nhiên | kiểm sàn | đã có (xao101) |
| — | người nghe Phi-4 | hành vi | đã có [val], chỉ trình như hướng đã thử |

### 8.3 Hạt giống

- Vòng 1: mỗi ô **một hạt (101)**.
- Vòng 2: chạy hạt 202 cho **mọi ô có exec cách GRPO-SPICE dưới 1,0 điểm**, và cho ô đứng thứ hai
  của mỗi trục dù cách xa bao nhiêu. Lý do: hai hạt ck500 đã chênh 0,72, nên dưới 1 điểm thì một hạt
  không phân biệt được.
- Kết luận "tốt nhất" chỉ khi hơn ở **trung bình hai hạt** và ghép cặp từng hạt cùng chiều. Không đạt
  thì viết "ngang nhau" và chuyển phần giải thích sang "vì sao nhóm này ngang nhau".

### 8.4 Trục 3 — giải thích vì sao tốt nhất trên AndroidControl

Phải là **giả thuyết kiểm được bằng số**, nối đặc điểm dữ liệu với cơ chế của phương pháp. Mỗi giả
thuyết có phép đo, và nếu số ngược thì bỏ giả thuyết.

**H1 — Câu chuẩn AndroidControl ngắn, theo khuôn, nội dung nằm ở tên phần tử.** (0 GPU)
- Đo: phân bố độ dài; tỉ lệ câu khớp khuôn ("Click on X", "Open the X app", "Scroll …"); tỉ lệ từ
  thuộc tên phần tử; số khuôn chiếm 80% câu. So với COCO captions (khoảng 10 từ, đa dạng) và AitZ.
- Hệ quả dự đoán: độ đo n-gram (BLEU, CIDEr-D, ROUGE-L) bị chi phối bởi phần khuôn mà mọi mẫu đã
  viết đúng, còn SPICE tách được tuple đối tượng/thuộc tính, tức đúng phần quyết định exec.

**H2 — Phần thưởng tốt là phần thưởng phân biệt được các câu trong nhóm VÀ khớp với exec.** (0 GPU,
dữ liệu 8 mẫu C1 [val], chỉ dùng giải thích)
- Với từng độ đo R0–R7 đo: tỉ lệ nhóm có độ lệch chuẩn bằng 0 (nhóm không cho gradient); tỉ lệ cặp
  hoà; tương quan hạng trong nhóm giữa phần thưởng và exec; xác suất câu có thưởng cao hơn thì exec
  không thấp hơn.
- Dự đoán: SPICE không nhất thiết đứng đầu từng chỉ số, nhưng **cân bằng tốt nhất giữa độ phân biệt
  và độ khớp exec**. Đây cũng là cách giải thích vì sao oracle SPICE yếu mà train vẫn tốt. Nếu số
  không ra như vậy thì phải tìm giải thích khác, không ép.
- Kiểm chéo: thứ tự độ đo theo H2 phải **dự đoán được** thứ tự exec thật của Trục 2. Đây là phép kiểm
  quan trọng nhất; khớp thì phần giải thích có sức nặng, lệch thì khai.

**H3 — Vì sao mốc nhóm (GRPO) hợp hơn mốc greedy (SCST) hay mốc trượt (REINFORCE).** (từ log train
của Trục 1)
- Mô hình S1 sau SFT ít ngẫu nhiên: nhiều câu lấy mẫu trùng câu greedy, nên SCST cho lợi thế bằng 0
  ở nhiều mẫu; mốc trượt không theo độ khó của từng prompt nên lợi thế nhiễu.
- Đo: tỉ lệ mẫu trùng câu greedy; tỉ lệ lợi thế khác 0; phương sai lợi thế; KL tới S1 theo bước.
  So A0 với A4 cho biết việc chia độ lệch chuẩn có đóng góp hay không (nhóm thưởng gần nhau thì chia
  std khuếch đại khác biệt nhỏ).

**H4 — SPICE sửa đúng loại lỗi chiếm đa số của S1.** (0 GPU + CPU Java)
- Đã có: GRPO-SPICE sửa loại thao tác ở +28 bước và đổi phần tử ở +41 bước (`report/259`).
- Thêm: phân rã SPICE theo loại tuple (đối tượng / thuộc tính / quan hệ) cho ck500 so S1 và cho các
  phần thưởng khác; đối chiếu với nhóm lỗi "thao tác đúng nhưng bộ trỏ không tìm ra nút" (86% lỗi của
  S1). Dự đoán: SPICE tăng chủ yếu ở tuple đối tượng/thuộc tính, tức tên phần tử.

**H5 — Giải thích phải dự đoán được cả chỗ phương pháp KHÔNG thắng.**
- AitZ: GRPO-SPICE không hơn S1 (−0,51, KTC phủ 0). Nếu H1 đúng thì câu AitZ phải khác khuôn
  AndroidControl (đo cùng chỉ số H1 trên AitZ). Khớp thì AitZ thành bằng chứng ủng hộ giải thích,
  thay vì chỉ là hạn chế.
- Bước không chạm (cuộn, quay lại): GRPO-SPICE giảm. Kiểm xem SPICE có ít tuple cho câu cuộn hay
  không (câu "Scroll down" gần như không có đối tượng). Có thì đây là giới hạn do chính cơ chế
  SPICE, phải khai.

### 8.5 Khảo sát tài liệu đi kèm

Hai bảng trong `report/325`:
- **Họ RL cho sinh văn bản:** cột = mốc trừ, có mô hình giá trị không, trực tuyến hay ngoại tuyến,
  số mẫu mỗi prompt, chi phí bộ nhớ, đã dùng cho sinh chú thích/GUI chưa. Dòng = REINFORCE, SCST,
  PPO, ReMax, RLOO, GRPO, Dr. GRPO, DAPO, cùng DPO/ORPO/RAFT/ReST-EM để phân biệt trực tuyến với
  ngoại tuyến.
- **Độ đo làm phần thưởng:** cột = bắt cái gì, cần tham chiếu không, tiền lệ làm phần thưởng, điểm yếu
  đã biết (như CIDEr bị khai thác bằng câu lặp). Dòng = BLEU, ROUGE-L, METEOR, CIDEr-D, SPICE,
  SPIDEr, chrF, BERTScore, CLIPScore, phần thưởng học được, người nghe.
- Mỗi dòng tra venue tận nguồn.

### 8.6 Lưới và chi phí

| nhóm | số lượt train (vòng 1) | ước lượng |
|---|---|---|
| Trục 1: A1–A4 | 4 | A1–A4 cùng vòng, ~ như ck500 |
| Trục 1: A5 PPO | 1 | đắt hơn, đo trước |
| Trục 2: R1–R7 | 7 | R4 METEOR, R6 BERTScore chậm hơn |
| Vòng 2 (hạt 202) | dự kiến 3–5 | quyết sau vòng 1 |
| **Tổng** | **~15–17 lượt train** + sinh/chấm test mỗi lượt | |

Mỗi lượt: train ~22 h trên T4 (160 s/bước, số đo ck500), L4 chưa đo; sinh + chấm test ~5,6 h T4.
Tổng khoảng 450 giờ T4 nếu đi toàn bộ trên Kaggle (bốn tài khoản × 30 h/tuần ≈ 120 h/tuần, tức
gần 4 tuần). Song song Colab L4/A100 sẽ rút còn khoảng 1,5–2 tuần nhưng tốn tiền. **User chọn.**

Thứ tự chạy:
1. Bậc 0 (ngay, 0 đồng): H1, H2, H4 phần 0 GPU, khảo sát tài liệu, viết `--algo`/`--reward` + kiểm CPU.
2. Ô thăm dò T4/L4: s/bước + VRAM đỉnh cho SPICE, METEOR, BERTScore, SCST, PPO.
3. Vòng 1 Trục 1 và Trục 2 song song.
4. Đọc vòng 1, kiểm chéo H2 với thứ tự exec thật, quyết vòng 2.
5. Vòng 2, rồi H3 từ log, H5.
6. Ghi tất cả vào `report/320`. Sau đó mới sửa luận văn.

### 8.7 Nếu GRPO + SPICE KHÔNG đứng đầu

Báo đúng như vậy. Phương án đứng đầu ở cả hai hạt thì đưa user quyết có đổi phương pháp chính hay
không. Phần giải thích (H1–H5) vẫn dùng được, vì nó giải thích thứ hạng của cả lưới chứ không chỉ
bảo vệ SPICE.

---

## 9. Kết quả H2/H3 (0 GPU) và DỰ ĐOÁN GHI TRƯỚC khi có số lưới train (1/11/2026)

Script `harness/thuong_dac_tinh.py` → `runs/thuong_dac_tinh/ket_qua.json`. Dữ liệu: 249 bước chạm của
C1, mỗi bước 8 câu S1 lấy mẫu ở nhiệt độ 1,0 + câu greedy, có nhãn exec. Đây đúng là một nhóm G = 8 ở
**bước đầu** của GRPO. ⛔ Số val, chỉ để giải thích cơ chế.

### 9.1 Tín hiệu học của từng phần thưởng (thuật toán GRPO)

| phần thưởng | nhóm thưởng bằng nhau hết | cặp hoà | cặp khác exec xếp đúng | dấu lợi thế đúng | oracle exec |
|---|---:|---:|---:|---:|---:|
| SPICE | **7,23** | **38,21** | **68,46** | **63,37** | 65,46 |
| CIDEr-D | 1,61 | 15,38 | 86,75 | 70,96 | 73,09 |
| BLEU-4 | 1,61 | 17,47 | 80,60 | 69,08 | 69,08 |
| ROUGE-L | 1,61 | 19,35 | 83,54 | 72,18 | 71,08 |
| chrF | 0,80 | 10,61 | 84,29 | 71,24 | 71,49 |
| METEOR | 1,61 | 17,66 | **87,11** | **72,27** | 71,49 |
| SPIDEr | 1,61 | 15,36 | 82,36 | 68,52 | 70,68 |

(greedy = 63,45; câu lấy mẫu trùng câu greedy 18,7%)

**Đọc:** ở bước đầu, **SPICE là phần thưởng có tín hiệu kém nhất** theo mọi chỉ số: nhiều hoà nhất
(SPICE so tuple nên hai câu khác chữ thường cùng điểm), xếp đúng cặp khác exec thấp nhất (68 so với
80–87). Giả thuyết H2 bản đầu ("SPICE cân bằng tốt nhất") **bị bác** ở bước đầu.

### 9.2 Cùng thưởng SPICE, năm cách tính lợi thế

| thuật toán | lợi thế bằng 0 | dấu lợi thế đúng |
|---|---:|---:|
| GRPO / Dr. GRPO / RLOO | 7,53 | 63,37 (cùng dấu, chỉ khác độ lớn) |
| REINFORCE (mốc trượt) | 0,00 | 62,69 |
| SCST (mốc greedy) | **42,72** | **58,07** |

SCST mất tín hiệu ở 43% câu vì câu lấy mẫu thường được điểm bằng đúng câu greedy.

### 9.3 Dự đoán ghi trước (trước khi có bất kỳ số test nào của lưới)

- **D1 (trục thưởng):** nếu "tín hiệu ở bước đầu" quyết định kết quả thì METEOR, CIDEr-D, ROUGE-L, chrF
  phải cho exec test **≥ SPICE**. Nếu SPICE vẫn hơn ở cả hai hạt thì tín hiệu bước đầu KHÔNG giải
  thích được, phải tìm cơ chế khác (ví dụ: thưởng thô làm chính sách trôi ít hơn, giữ hành vi của S1).
- **D2 (trục thuật toán):** SCST < GRPO (mất 43% tín hiệu, dấu đúng 58 so 63). GRPO, Dr. GRPO, RLOO
  cùng dấu lợi thế nên khác nhau chỉ do cỡ bước; dự đoán chênh nhau trong nhiễu hạt giống.
- **Hệ quả phải chấp nhận:** nếu D1 đúng thì **GRPO + SPICE không phải tốt nhất**. Báo đúng như vậy,
  user quyết có đổi phương pháp chính hay không.

---

## 10. Nhật ký chạy lưới (1/11)

**Probe `uyenle0712/luoi-probe-u`** (20 bước, 50 câu nhắc dài nhất, 2 GPU song song; số kỹ thuật, không phải kết quả):

| lượt | mã thoát | s/bước | đỉnh VRAM | RAM phiên |
|---|---|---|---|---|
| SCST + SPICE | 0 | 158,1 | 12,71 GiB | 12/31 GB |
| GRPO + CIDEr-D | 0 | 149,1 | 12,71 GiB | 12/31 GB |

- Loss bước 1 ≈ 1,0 ở cả hai lượt (xao101: 0,039): cùng hạt giống nên sinh cùng một câu dài 88 token, bị phạt độ dài. Trong xao101, |loss| lớn nhất cũng rơi vào bước có câu dài nhất (58 token, −0,31). Không phải lỗi. [suy từ log, chưa tách riêng câu đó]
- `grad_norm` nan một lần ở GRPO + CIDEr-D (bước 17), các bước sau bình thường. xao101 có 2/500 bước như vậy, nên coi là tràn số fp16 mà GradScaler bỏ qua.
- SCST: `luoi/r_greedy` được ghi, lợi thế bằng 0 ở 12,5–100% mẫu tuỳ bước.
- Kiểm thêm trên CPU: METEOR và ROUGE-L với chuỗi khó (`|||`, xuống dòng, emoji, câu rất dài, câu chỉ có dấu câu) không treo; METEOR 1.500 lần gọi liên tiếp hết 9 s.
- Ước lượng thời gian: xao101 thật 143 s/bước. SCST khoảng 152 s/bước [suy], mỗi commit được khoảng 250 bước, vừa đủ hai commit nhưng sát; có thể cần một commit ngắn thứ ba.

**Đợt 1, đẩy 20:04 1/11 (giờ VN), commit 1/2:**

| kernel | GPU 0 | GPU 1 |
|---|---|---|
| `uyenle0712/luoi-u-1` | SCST + SPICE | GRPO + CIDEr-D |
| `trangphngngc/luoi-t-1` | GRPO + METEOR | GRPO + ROUGE-L |
| `trangphuongngoc/luoi-t2-1` | RLOO + SPICE | REINFORCE + SPICE |

Tất cả hạt 101, dùng đúng câu nhắc của ck500 (`--keys-ck500`).

**User chốt 1/11 tối (thắng §8 khi mâu thuẫn):**
- Danh sách so sánh lấy theo khảo sát paper (`reports/Baseline RL so với GRPO.md`): phải so thế nào mới thuyết phục nhất thì ghi lại để chạy, không giới hạn vì lo chi phí tính toán.
- Máy: chạy được trên Kaggle thì chạy Kaggle, không thì Colab.
- Tạm bỏ việc chạy nhiều hạt giống (seed 202), làm sau.


## 11. Danh sách lượt chạy sau khảo sát (1/11 tối)

Nguồn: `report/reports/Baseline RL so với GRPO.md` (mẫu 153 bài, mẫu có chủ đích). Danh sách đầy đủ, máy, trạng thái mã và
cách viết kết quả nằm ở file đó, phần này chỉ ghi thứ tự. Tạm một hạt giống 101, seed khác làm sau. Chạy Kaggle trước,
không được thì Colab và khai đổi máy.

- **Đang chạy (6):** SCST, RLOO, REINFORCE EMA + SPICE · GRPO + CIDEr-D, METEOR, ROUGE-L.
- **Kế tiếp, mã đã xong (5):** GRPO bỏ chia std · GRPO + BLEU-4, chrF, SPIDEr, BERTScore.
- **Mới, ưu tiên một:** SFT tiếp · SCST + CIDEr-D · PPO λ=1,0 và 0,95 · DPO trực tuyến và ngoại tuyến từ S1 · RFT một vòng và
  online từ S1 · DAPO lõi (β=0) · Dr. GRPO đủ · GRPO gộp theo câu · đo hình thức câu (không train).
- **Mới, ưu tiên hai:** 15 lượt B1–B15 (DAPO đủ, chuẩn hoá theo lô, Vanilla PG, actor-critic, PPO critic đủ cỡ, ORPO, DPO bán
  trực tuyến, GPG, xuất phát từ Base, BCMR, G=4/16, μ=2, GSPO, Clip-Higher).
- **Không chạy:** SAC, A2C, A3C, TD3, TRPO, KTO, ReMax riêng, VinePPO. Lý do ở file khảo sát.

Hai việc phải khai khi viết: ck500 dùng `loss_type="dapo"` và với `num_iterations=1` phép clip không hoạt động
(`clip_ratio/region_mean` = 0 ở mọi dòng log kiểm tra). Lượt PPO cần viết mã và đo VRAM trước khi chốt máy.


## 12. Mở rộng: RL nói chung và phương pháp cổ điển (user chốt 1/11 tối)

User: so càng nhiều càng tốt, kể cả cổ điển; Kaggle miễn phí thì cứ chạy; cái cần Colab mà quan trọng thì ghi lại để user quyết.
Chi tiết ở mục *Mở rộng theo yêu cầu 1/11 tối* của `report/reports/Baseline RL so với GRPO.md`.

- **Kaggle, mã xong (`harness/grpo_codien.py`, selftest và CPU đạt, chưa probe T4):** vanilla · rft · cem · awr · raml · rank · mad; β=0 cho A9, A10.
- **Kaggle, phải viết mã:** MRT · softmax PG · MIXER rút gọn · trộn RL + CE · SeqGAN · Quark · ES · A2C.
- **Ghi lại để user quyết (Colab hoặc chưa chắc vừa T4):** PPO critic đủ cỡ · TRPO · ILQL · SAC rời rạc.
- **Không áp dụng được:** TD3, DDPG (hành động liên tục).
- **Đọc kết quả:** hiệu chỉnh Holm vì khoảng 50 phép so; báo vô điều kiện, kể cả khi ck500 thua.
- **Chưa làm:** `make_nb.py` chưa nhận nhánh mới. Không cập nhật dataset `grpo-luoi-script` và không đổi tệp trong `ds/` theo cách làm lệch md5 của `grpo_luoi.py` trước khi xong lô 1.

## 13. Bổ sung sau §12

Thứ tự chạy mới và danh sách Colab: `report/329`. Đánh giá ACE: `report/327`. Đánh giá GRPO + SPICE: `report/328`. Khảo sát độ đo thay SPICE: `report/330`. Việc tiếp theo và trạng thái: `report/326`. Cách đọc lưới ghi trước: `report/320` §13.

## 14. Đính chính §3 theo `report/330` (2/11)

Giữ nguyên §3 để tra lịch sử, nhưng **không dùng các lập luận sau làm lý do chọn SPICE**:
- Zhao EACL 2021 chỉ khuyên SPICE ở mức hệ thống; mức từng chỉ dẫn bài nói không tương quan.
- "SPICE so đối tượng + thuộc tính + quan hệ": quan hệ trung bình chỉ 0,50 tuple mỗi câu chuẩn [đo, val].
- "CIDEr-D dễ thưởng chép cụm hiếm hơn gọi đúng phần tử": phép đổi câu cho thấy ngược lại, CIDEr-D tách câu sai tên mạnh nhất [đo, val]. Chỉ còn là giả thuyết.
- CLIP có số ở `report/330` §5, không còn là "loại bằng lý do".
