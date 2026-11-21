# ACTION — So GRPO với 4 thuật toán RL phổ biến nhất 2024–2026 (DAPO · GSPO · Dr.GRPO · REINFORCE++)

> **Ghi chú chép lại (20/11/2026):** bản này chép tay từ 15 ảnh chụp màn hình Cursor (preview của
> `ACTION_4_THUAT_TOAN_RL_2025_SO_VOI_GRPO_20_11_2026.md`), gói `My Documents [20-11-2026 21_50].zip`.
> Bộ ảnh **không phủ trọn file**; các chỗ không có ảnh được đánh dấu `⚠️ [THIẾU ẢNH]`. Công thức trong
> preview hiện dạng LaTeX thô, ở đây viết lại bằng `$…$`.

**Ngày:** 20/11/2026 · **Trạng thái cuối sau ba phản biện độc lập: CHỐT BỐN TÊN**, nhưng **CHƯA ĐƯỢC GIAO CHẠY** theo thiết kế cũ. Mục **12** là phán quyết cuối và **thắng mục 0, 3, 4, 5, 7, 8, 10, 11 khi có mâu thuẫn**. Chỉ chuyển sang GO sau khi người nhận bàn giao sửa đủ bốn blocker ở mục 12. **Chưa cài, chưa chạy GPU, chưa có số. File này tự chứa và chỉ mô tả, không kèm mã.** Gồm: lý do chọn, tóm tắt từng bài báo, phần tranh luận, mô tả chính xác phần cần cài thêm, kế hoạch chạy theo thứ tự, cách kiểm từng bước, và luật đọc kết quả được chốt **trước** khi có số.

---

## 0. Tóm tắt một phút

- **Chọn 4 thuật toán:** DAPO, GSPO, Dr.GRPO và REINFORCE++ (biến thể *w/ Baseline*). Đây là 4 thuật toán phổ biến nhất trong họ "sau GRPO" giai đoạn 2025–2026. Cả bốn có sẵn trong verl, ba cái có sẵn trong TRL. Trong mẫu 42 bài họ RLVR mà dự án đã khảo sát, số bài lấy chúng làm mốc so là DAPO 15, Dr.GRPO 8, GSPO 5, REINFORCE++ 5. RLOO cũng 5 bài, nhưng đã chạy rồi.
- **Đã tranh luận để chốt (mục 11): giữ đúng 4 thuật toán này.** Không ứng viên nào khác (CISPO, SAPO, GMPO, GDPO, VAPO, GVPO, online DPO…) vừa phổ biến ngang, vừa cho thông tin mới trong cấu hình của bài.
- Xếp theo **giá trị thông tin** cho bài này (sửa ở mục 11): **REINFORCE++ > GSPO > DAPO (lọc nhóm hòa) > Dr.GRPO.**
  - Dr.GRPO trong cấu hình này gần như **trùng RLOO đã chạy**. Vẫn chạy vì nằm trong top phổ biến, và vì nó cho thêm một phép đo độ dao động giữa hai lượt gần như cùng thuật toán.
  - GSPO là thuật toán duy nhất mà cơ chế riêng vẫn hoạt động ở lr này, nhờ khoảng cắt rất hẹp.
- Tổng cộng **5 lượt train, 1 hạt**, trên 3 kernel Kaggle:
  - 4 thuật toán chính;
  - 1 lượt đối chứng GRPO μ=2, bắt buộc vì GSPO chỉ khác GRPO khi μ ≥ 2. DAPO chạy **μ=1** (mục 10). Lượt Dr.GRPO β=0,014 ở bản trước đã **bỏ**, vì REINFORCE++ thực chất đã đóng đúng vai đó (mục 11).
- **Cần cài thêm hai phần nhỏ:** chuẩn hóa advantage kiểu REINFORCE++ và bộ lọc nhóm hòa của DAPO (mô tả ở mục 5). Dr.GRPO, GSPO và GRPO μ=2 chỉ cần cờ cấu hình đã có trong mã lưới.
- **Sửa lỗi của bản trước:** bí danh `gspo` viết ngày 6/11 thiếu `loss_type="grpo"`, nên không phải GSPO đúng nghĩa (mục 6).
- **Kỳ vọng trung thực:** cả bốn nằm trong khoảng ±1 điểm executability quanh GRPO, tức không phân biệt được. Nếu vậy, câu được viết là *"không thuật toán phổ biến nào hơn GRPO có ý nghĩa"*, **không** phải *"GRPO tốt nhất"*.

---

## 1. Bối cảnh cần biết (cho chat không có repo)

- Mô hình: Qwen2.5-VL-3B-Instruct, LoRA. Mỗi màn hình sinh **một câu hướng dẫn ngắn**, khoảng 8–12 token, tối đa 96.
- Phần thưởng: SPICE so với một câu chuẩn, trừ phạt độ dài. Đây là **phần thưởng liên tục**, không phải đúng/sai 0/1.
- Cấu hình GRPO của lưới RL hiện có (mã `harness/grpo_luoi.py` và `grpo_codien.py`, notebook dựng bằng `_bundles/luoi/make_nb.py`):
  - xuất phát từ S1/101, G=8 câu mỗi câu nhắc, 2 câu nhắc mỗi lô sinh (16 câu);
  - lr 1e-5, β KL 0,04 về S1, 1.000 câu nhắc của ck500, 500 bước;
  - `loss_type="dapo"` (gộp theo token), **μ = 1**. Với μ = 1, tỉ số quan trọng luôn bằng 1, nên phép cắt (clip) **không bao giờ hoạt động**. Log ck500 xác nhận `clip_ratio = 0` ở mọi dòng.
- Trong log, **20–31% số nhóm** có cả 8 câu cùng điểm. Trung vị độ lệch chuẩn thưởng trong nhóm khoảng 0,35.
- Mốc đã có trên tập kiểm, cùng 4.463 bước chạm:

| lượt | exec | ghi chú |
|---|---|---|
| GRPO A/A (`grpo_luoi.py`, cùng mã với lưới) | 59,74 | **mốc so công bằng** cho các lượt μ=1 |
| GRPO lượt gốc ck500 (`grpo_spice.py`) | 60,65 | khác mã và thư viện, lệch A/A +0,92 |
| SCST | 60,54 | |
| SFT tiếp (không RL) | 60,16 | |
| PPO λ=1 / λ=0,95 | 60,07 / 59,98 | |
| REINFORCE (mốc EMA) | 60,00 | |
| RLOO | 59,44 | |
| S1 (điểm xuất phát) | 59,11 | |

---

## 2. Deep research — tóm tắt từng bài

### 2.1 DAPO — Yu và cộng sự, 2025, arXiv 2503.14476 (ByteDance Seed và Tsinghua)

- **Bài toán của họ:** RL suy luận chuỗi dài (long-CoT) cho toán, phần thưởng đúng/sai, Qwen2.5-32B **base**. GRPO thường chỉ đạt 30 điểm AIME'24.
- **Bốn kỹ thuật**, Bảng 1 thêm dần từng cái (avg@32 AIME'24): GRPO 30 → lọc câu quá dài 36 (+6) → Clip-Higher 38 (+2) → phạt mềm câu quá dài 41 (+3) → mất mát theo token 42 (+1) → **lấy mẫu động 50 (+8)**.
- Siêu tham số: lr 1e-6, 512 câu nhắc × 16 mẫu, **16 lần cập nhật cho mỗi lô sinh** (off-policy, tỉ số khác 1), ε_low 0,2, ε_high 0,28, tối đa 20.480 token. **Bỏ KL.** Lý do họ nêu ở mục 2.3: *trong RLHF thì mục tiêu là không lệch xa mô hình đầu, nhưng mô hình long-CoT cần lệch xa, nên không cần ràng buộc này.*
- **Lấy mẫu động:** lấy dư mẫu, bỏ câu nhắc có độ chính xác 0 hoặc 1 (nhóm không có gradient), lấy tiếp đến khi đầy lô.
- **Áp vào bài của mình:**
  - lọc và phạt câu quá dài: vô nghĩa với câu 10 token (lưới đã bật `mask_truncated_completions`, chính là lọc câu quá dài);
  - mất mát theo token: **lưới đã dùng sẵn**;
  - Clip-Higher: **không tác dụng khi μ=1**, và theo log PPO μ=2 của dự án thì cũng gần như không tác dụng khi μ=2 ở lr 1e-5 với LoRA (mục 10, điểm 2);
  - **lấy mẫu động: có tác dụng thật**, vì 20–31% nhóm hòa điểm;
  - bỏ KL: chính lý do của bài cho thấy bài mình (xuất phát từ SFT, giống RLHF) **nên giữ KL**.
- Bằng chứng: Bảng 1 là ablation tích lũy trên một mô hình và một lần chạy; mã nguồn mở, đã tái lập trong verl. Venue [chưa xác minh tận nguồn], ghi "arXiv 2503.14476".

### 2.2 GSPO — Zheng và cộng sự, 2025, arXiv 2507.18071 (nhóm Qwen)

- **Bài toán của họ:** RL cho **MoE** (Qwen3-30B-A3B) với câu trả lời dài. Tỉ số quan trọng theo token dao động mạnh vì chuyên gia được kích hoạt thay đổi giữa các lần cập nhật. GRPO phải dùng *Routing Replay* mới hội tụ.
- **Cách làm:** tỉ số theo **cả câu**, $s_i = \left(\pi_\theta(y_i)/\pi_{old}(y_i)\right)^{1/|y_i|}$, và cắt theo cả câu. Khoảng cắt rất hẹp **3e-4 / 4e-4**. Mỗi lô sinh chia 4 mini-batch (μ hiệu dụng = 4). Mốc GRPO được chỉnh khoảng cắt 0,2/0,27 để so công bằng.
- Kết quả: đường cong thưởng và hiệu năng (AIME'24, LiveCodeBench, CodeForces) cao hơn GRPO; không cần Routing Replay. Dùng trong huấn luyện Qwen3.
- **Áp vào bài của mình:** mô hình dense 3B, câu ngắn, nên **cả hai lý do gốc của GSPO đều không có mặt**. Khi μ=1, $s_i = 1$ và GSPO chỉ còn là "GRPO gộp theo câu". Muốn GSPO khác GRPO phải dùng μ=2, và khi đó **cần đối chứng GRPO μ=2**. Trong TRL phải đặt `loss_type="grpo"`: TRL cảnh báo rằng ghép `importance_sampling_level="sequence"` với `dapo`/`bnpo`/`dr_grpo` sẽ trọng số mỗi câu theo độ dài, sai mục tiêu GSPO (TRL PR #6042, issue #3823).

### 2.3 Dr.GRPO — Liu và cộng sự, 2025, arXiv 2503.20783 ("Understanding R1-Zero-Like Training")

- **Chẩn đoán hai thiên lệch của GRPO:**
  1. **thiên lệch độ dài:** chia cho $|o_i|$ đẩy câu đúng ngắn lại và câu sai dài ra;
  2. **thiên lệch độ khó:** chia cho độ lệch chuẩn của nhóm làm tăng trọng số câu nhắc có độ lệch chuẩn nhỏ (quá dễ hoặc quá khó), làm lệch mục tiêu.
- **Cách sửa:** bỏ cả $1/|o_i|$ lẫn std: $A = r - \bar r$; gộp token rồi chia cho một hằng số.
- Thực nghiệm: Qwen2.5-Math-7B, toán (Oat-Zero). Độ chính xác ngang hoặc hơn, câu trả lời sai ngắn hơn.
- **Áp vào bài của mình — điểm mạnh nhất trong bốn:**
  - thiên lệch độ dài gần như không có, vì câu đều khoảng 10 token;
  - **thiên lệch độ khó có mặt rõ.** Nhóm có std nhỏ là màn hình mà S1 viết 8 câu gần giống nhau. SPICE khá thô (22,7% nhóm hòa hẳn), nên chênh lệch nhỏ trong các nhóm đó phần lớn là nhiễu. GRPO chia cho std nhỏ, tức **phóng đại nhiễu** thành advantage cỡ ±1. Dr.GRPO thì không.
- Bằng chứng: venue [chưa xác minh tận nguồn; ghi chú cũ của dự án ghi COLM 2025 theo đầu PDF]. TRL và verl hỗ trợ sẵn.

### 2.4 REINFORCE++ — Hu và cộng sự, 2025, arXiv 2501.03262 (bản v9)

- **Chẩn đoán:** chuẩn hóa cục bộ theo từng câu nhắc (GRPO, RLOO) là ước lượng **có thiên lệch** (Phụ lục A chứng minh: mẫu số phụ thuộc chính mẫu đang xét) và dễ quá khớp.
- **Cách làm:** chuẩn hóa advantage trên **cả lô toàn cục**. Biến thể *w/ Baseline* (cho k>1): trừ trung bình nhóm, rồi chia cho std **của cả lô**. KL dạng k2. Bài nói lô toàn cục "thường lớn, ví dụ 1024 trở lên", nên thống kê gần như hằng số.
- Kết quả: Bảng 1 (Chat-Arena-Hard) REINFORCE++ k=1 46,7 so với GRPO k=4 46,8 (ngang). Bảng 4 (tool-use) RF++-Baseline 24,10 so với GRPO 22,58 và PPO 21,85. Đây là bài tự đề xuất.
- **Áp vào bài của mình:** lô sinh chỉ có 16 câu (2 câu nhắc), nên "toàn cục" gần như trùng "cục bộ". Thiết kế ở mục 5 lấy std trên **cửa sổ trượt 8 lô sinh** (16 câu nhắc, 128 câu) để giữ tinh thần "thống kê ổn định trên nhiều câu nhắc". Đây là **xấp xỉ, phải khai**.

### 2.5 Các thuật toán mới khác — vì sao không chọn

- **CISPO** (MiniMax-M1), **SAPO** (Qwen), **GMPO**, các biến thể cắt kiểu VESPO hay DPPO: chỉ sửa **tỉ số quan trọng hoặc phép cắt**, nên **không tác dụng khi μ=1**. Muốn thử phải chạy μ≥2, tốn gấp đôi.
- **VAPO:** cần critic, thử trên 32B. Lưới đã có PPO đại diện họ có critic.
- **GDPO** (2026, nhiều kênh thưởng): chỉ có nghĩa với phần thưởng ghép như SA-SPICE-v3. Đáng thử **riêng** cho SA-SPICE-v3 sau này, không thuộc phép so thuật toán.
- **GVPO** (NeurIPS 2025): bài tự đề xuất, ít được dùng làm mốc.
- **Online DPO:** đã có mã (`dpo_on`), nằm trong việc user chọn từ 15/11; không phải họ "sau GRPO".

### 2.6 Bốn cách chia điểm khác nhau ra sao — ví dụ số

Lô sinh có 2 nhóm, mỗi nhóm rút gọn còn 4 câu. Nhóm 1 phân hóa mạnh, điểm 0 · 1 · 0 · 1. Nhóm 2 gần hòa, điểm 0,1 · 0,3 · 0,1 · 0,3.

| cách tính | nhóm 1: câu tốt / câu dở | nhóm 2: câu tốt / câu dở |
|---|---|---|
| GRPO: chia std **của từng nhóm** | +0,87 / −0,87 | **+0,87 / −0,87** (chênh 0,2 điểm SPICE bị khuếch đại ngang chênh 1 điểm) |
| Dr.GRPO: chỉ trừ trung bình nhóm | +0,50 / −0,50 | +0,10 / −0,10 |
| REINFORCE++: trừ trung bình nhóm, chia std **chung cả lô** | +1,30 / −1,30 | +0,26 / −0,26 |
| DAPO lọc: như GRPO, nhưng nhóm 8 câu bằng điểm nhau thì bỏ khỏi lô | như GRPO | như GRPO (nhóm này không hòa hẳn nên vẫn giữ) |

Dr.GRPO và REINFORCE++ cùng giữ nguyên tỉ lệ thật giữa hai nhóm. Khác nhau ở thang: Dr.GRPO nhỏ hơn GRPO khoảng 3 lần, nên với cùng β thì KL kéo mạnh hơn tương đối; REINFORCE++ giữ thang gần GRPO.

---

## 3. Tranh luận: cái nào hợp nhất với bài này

| | Bên ủng hộ | Bên phản bác | Phán quyết |
|---|---|---|---|
| **Dr.GRPO** | Thiên lệch độ khó có thật ở đây: nhóm gần hòa có std nhỏ, GRPO phóng đại nhiễu SPICE. Chạy được khi μ=1, không tốn thêm. | Bỏ std làm advantage nhỏ đi khoảng 3 lần (std trung vị 0,35); với cùng β=0,04 thì KL mạnh tương đối gấp khoảng 3 lần, mô hình học dè dặt hơn và có thể thua vì cấu hình. Lưới cũ: RLOO và REINFORCE (cũng không chia std) không hơn A/A. | ~~Hợp nhất~~ → **sửa ở mục 11:** trong cấu hình này Dr.GRPO gần như trùng RLOO (59,44, thấp nhất lưới), nên lập luận lý thuyết chưa được dữ liệu ủng hộ. Vẫn chạy β=0,04, làm lượt lặp của cơ chế "không chia std". |
| **DAPO** | 20–31% nhóm hòa nghĩa là 20–31% tính toán bị bỏ phí. Lấy mẫu động là kỹ thuật lớn nhất của DAPO (+8 AIME). Clip-Higher chống sụp entropy. | Với phần thưởng liên tục, nhóm hòa vốn có advantage = 0. Lọc mà không bù chỉ làm thang gradient lớn lên khoảng 1,3 lần, dưới Adam ảnh hưởng nhỏ. Bù đủ lô thì phải dùng câu nhắc ngoài bộ 1.000 câu của ck500. Clip-Higher chỉ tác dụng khi tỉ số chạm ngưỡng cắt, điều không xảy ra ở lr 1e-5 với LoRA. Bỏ KL không hợp bài xuất phát từ SFT. | **Hợp thứ hai.** μ=1, lọc nhóm hòa, giữ β=0,04; so với GRPO A/A. Clip-Higher không tác dụng trong chế độ này (mục 10, điểm 2). |
| **REINFORCE++** | Thống kê toàn cục ổn định hơn; vừa giữ thang ~1 vừa không phóng đại nhóm gần hòa. | Bài dựa vào lô ≥1024, ở đây chỉ 16, nên cửa sổ trượt là xấp xỉ. Bài báo tự cho thấy ngang GRPO ở tác vụ chung (46,7 so với 46,8). | **Hợp thứ ba.** Cửa sổ 8 lô, khai là xấp xỉ. |
| **GSPO** | Nổi tiếng nhất (Qwen3); thưởng theo câu thì tỉ số theo câu là tự nhiên. | Hai lý do gốc (MoE, câu dài) không có mặt. Khi μ=1 trùng GRPO gộp theo câu. Khoảng cắt 3e-4/4e-4 với LoRA lr 1e-5 có thể cắt gần hết lần cập nhật thứ hai. | **Kém hợp nhất.** Vẫn chạy vì độ phổ biến; μ=2, so với GRPO μ=2. |

**Kết luận tranh luận:** nếu phải chọn một thuật toán có cơ sở lý thuyết để kỳ vọng hơn GRPO trên bài này, đó là **Dr.GRPO**. Dù vậy, bằng chứng chung (MathForge ICLR 2026: GRPO, Dr.GRPO, DAPO, GSPO lệch nhau dưới 0,33 điểm khi kiểm soát chặt; lưới của chính dự án: mọi thuật toán không có critic nằm trong ±1 điểm) cho thấy **khả năng cao nhất là không phân biệt được**.

---

## 4. Nguyên tắc so công bằng (chốt trước khi có số)

User muốn GRPO giữ vị trí tốt nhất. Cách duy nhất bảo vệ được điều đó trước hội đồng là so **công bằng** và báo **mọi** kết quả.

1. **Mốc so:** Dr.GRPO, REINFORCE++ và DAPO (μ=1) so với **GRPO A/A 59,74** (cùng mã). GSPO (μ=2) so với **GRPO μ=2** (lượt đối chứng mới). Bảng vẫn in thêm cột so với ck500, SFT tiếp và S1. ⛔ **Không** lấy ck500 60,65 làm mốc chính. Làm vậy thì GRPO được lợi sẵn 0,92 điểm do khác mã; hội đồng tự tính lại từ bảng là thấy.
2. Giữ chung mọi siêu tham số của lưới: S1/101, đúng 1.000 câu nhắc của ck500 (kiểm trùng thứ tự), G=8, lr 1e-5, **β 0,04**, hạt 101, Kaggle T4 fp16. Lượt μ=2 chạy 1.000 bước để vẫn đi đúng 1.000 câu nhắc. Chấm điểm lưu cuối, không chọn điểm lưu.
3. Không chỉnh siêu tham số riêng cho thuật toán nào sau khi thấy số.
4. **Đọc kết quả:** "hơn" hoặc "kém" chỉ khi KTC95 ghép cặp (bootstrap cụm app) loại 0 **và** vẫn còn ý nghĩa sau Holm trên cả họ phép so với A/A (bảng tổng hợp tự tính). Ngoài ra viết "không phân biệt được". Mọi lượt một hạt, phải gắn nhãn.
5. **Dải GRPO (thêm ở lượt phản biện).** Với 1 hạt, KTC ghép cặp chỉ đo nhiễu của tập kiểm, **không** đo nhiễu giữa các lần train. Nhiễu giữa các lần train đã đo được trên chính GRPO: ba lượt GRPO + SPICE cho **59,74** (A/A/101), **59,94** (ck500/202) và **60,65** (ck500/101). Vì vậy dải **[59,74; 60,65]** là "dải dao động của GRPO". Thuật toán nào có exec **nằm trong dải** thì viết là *"nằm trong dao động của chính GRPO giữa các lần chạy"*, kể cả khi KTC so với A/A loại 0. Lưu ý: A/A là lượt GRPO thấp nhất, nên chuyện một thuật toán mới "hơn A/A có ý nghĩa" là **dễ xảy ra** (SCST đã +0,81†) mà chưa nói được gì về thứ hạng.
6. **Luật hạt thứ hai (thêm ở lượt phản biện).** Chỉ khi một thuật toán **vượt trên dải** (exec > 60,65) **và** hơn A/A có ý nghĩa sau Holm, mới chạy hạt 202 cho đúng thuật toán đó cùng GRPO cùng mã hạt 202, trước khi viết bất kỳ câu nào về "hơn GRPO". Ngoài trường hợp đó, giữ 1 hạt.
7. **Họ Holm:** thêm 5 lượt mới thì họ phép so với A/A ở Bảng 1 tăng từ 8 lên 13. Đã tính thử: các dấu † hiện có vẫn giữ (ck500 p gốc 5,5e-5 × 13 ≈ 0,0007; SCST p gốc 0,001 × 12 ≈ 0,012).

| kết quả | câu được viết |
|---|---|
| Mọi lượt nằm trong dải GRPO [59,74; 60,65] (dự kiến) | "Bốn thuật toán phổ biến nhất sau GRPO (DAPO, GSPO, Dr.GRPO, REINFORCE++) đều nằm trong dao động của chính GRPO giữa các lần chạy; không thuật toán nào vượt GRPO (một hạt)." |
| Có lượt **dưới** dải và kém A/A có ý nghĩa | Như trên, thêm "X kém GRPO Δ [KTC]", kèm lý do cơ chế ở mục 3 và mục 10. |
| Có lượt hơn A/A có ý nghĩa nhưng vẫn **trong** dải | "X hơn lượt GRPO cùng mã nhưng nằm trong dải ba lượt GRPO; chưa xếp hạng được." |
| Có lượt **trên** dải và hơn A/A sau Holm | Chưa viết gì về thứ hạng; chạy hạt 202 theo luật 6, rồi báo đúng như vậy. Có đổi phương pháp chính hay không là **user quyết** (mục 8). |

⛔ Trong mọi trường hợp **không** viết "GRPO là thuật toán tốt nhất".

---

## 5. Phần cần cài thêm — mô tả (người cài tự viết mã theo đây)

### 5.1 Đặt ở đâu

- Viết thành **một module mới** theo đúng khuôn của `harness/grpo_moi_b1.py`: import `grpo_codien`, đăng ký thêm hai tên thuật toán `rpp` và `dapo_ds`, thay hàm tính advantage và lớp trainer của lưới, rồi gọi `main()` của `grpo_codien`. Như vậy điểm xuất phát, 1.000 câu nhắc, G, lr, β, phần thưởng, điểm lưu mỗi 25 bước và dòng log `[nap default]` giữ nguyên.
- **Không sửa** `grpo_luoi.py`, `grpo_codien.py`, `grpo_moi_b1.py`, để các lượt cũ vẫn tái lập được.
- `make_nb.py` cần nhận nhóm thuật toán mới: thêm vào danh sách tên hợp lệ, chọn đúng module khi dựng lệnh, đưa module vào danh sách tệp cần chép, và chạy selftest của module ở ô thứ ba. `make_kit.py` cần chép module mới vào kit của cả ba tài khoản.

### 5.2 REINFORCE++-baseline (`rpp`)

- **Đầu vào** mỗi lô sinh: 16 điểm thưởng, xếp thành 2 nhóm liền nhau, mỗi nhóm 8 câu cùng một câu nhắc.
- **Bước 1:** trong từng nhóm, trừ trung bình của nhóm. Gọi kết quả là advantage đã trừ mốc.
- **Bước 2:** giữ một cửa sổ chứa advantage đã trừ mốc của **8 lô sinh gần nhất** (lô hiện tại tính vào). Tính độ lệch chuẩn của toàn bộ giá trị trong cửa sổ (tối đa 128 số).
- **Bước 3:** advantage cuối = advantage đã trừ mốc chia cho (độ lệch chuẩn đó + 1e-4). Không cần trừ trung bình toàn cục, vì sau bước 1 trung bình đã bằng 0.
- Cửa sổ dài 8 đặt bằng tham số, để có thể chạy kiểm độ nhạy (cửa sổ 1 = chỉ lô hiện tại).
- Cửa sổ **không lưu vào điểm lưu**. Khi chạy tiếp sau khi chạm trần giờ, cửa sổ bắt đầu rỗng và đầy lại sau 8 lô sinh. Ảnh hưởng nhỏ, nhưng phải ghi vào phần khai.
- KL giữ như mọi lượt lưới (ước lượng của TRL, β 0,04), **không** đổi sang KL k2 trong phần thưởng như bài gốc. Phải khai.
- **Ghi log mỗi lô:** độ lệch chuẩn đã dùng và số lô đang có trong cửa sổ.
- **Phép tự kiểm** (chạy CPU, không cần mô hình): với lô có nhóm 0,2 · 0,4 · 0,6 · 0,8 và nhóm 0,5 · 0,5 · 0,5 · 0,5 (G=4, cửa sổ 1), advantage phải là −1,77 · −0,59 · +0,59 · +1,77 và 0 · 0 · 0 · 0. Với lô ở mục 2.6, nhóm gần hòa phải cho advantage nhỏ hơn nhóm phân hóa ít nhất 3 lần. Khi đổi sang tên thuật toán khác (ví dụ `grpo`), kết quả phải trùng hàm cũ.

### 5.3 DAPO — lấy mẫu động dạng lọc (`dapo_ds`)

- **Advantage:** giống hệt GRPO (trừ trung bình nhóm, chia std nhóm + 1e-4).
- **Lọc:** sau khi có điểm thưởng của lô sinh, tìm các nhóm có 8 điểm **bằng nhau hoàn toàn** (lớn nhất trừ nhỏ nhất < 1e-9). Với các nhóm đó:
  - đặt mặt nạ câu sinh (`completion_mask`) về 0, để chúng không góp vào mất mát chính sách và cũng không góp vào KL;
  - **tính lại mẫu số token** của lô (`num_items_in_batch`) bằng tổng mặt nạ mới. Đây là điểm quan trọng nhất: với `loss_type="dapo"`, TRL chia tổng mất mát cho mẫu số này. Nếu chỉ đổi mặt nạ mà không tính lại mẫu số thì bộ lọc gần như không có tác dụng.
- **Không lấy mẫu bù** cho đủ lô như bài gốc, vì bù phải dùng câu nhắc ngoài 1.000 câu nhắc của ck500. Gọi tên trong bài là "DAPO (lọc nhóm hòa, không lấy mẫu bù)".
- Trường hợp cả lô đều hòa: mẫu số về 0, TRL tự chặn ở 1, bước đó có mất mát bằng 0. Chấp nhận, chỉ cần ghi log.
- Phần còn lại của DAPO đặt bằng cờ có sẵn: **μ = 1**, 500 bước, **ε_high = 0,28** (ε_low giữ 0,2 mặc định). Đặt ε_high chỉ để cấu hình đúng như bài gốc; trong chế độ này nó không có tác dụng (mục 10, điểm 2). Gộp theo token và lọc câu bị cắt đã là mặc định của lưới. **Giữ β = 0,04** (bài gốc bỏ KL; lý do giữ ở mục 2.1).
- Vì vậy, thứ duy nhất DAPO thay đổi so với GRPO A/A trong phép so này là **bộ lọc nhóm hòa**. Tên trong bảng phải nói rõ điều đó.
- **Ghi log mỗi lô:** tỉ lệ nhóm bị lọc và tỉ lệ token còn lại.
- **Phép tự kiểm:**
  1. CPU, không mô hình: lô có một nhóm hòa và một nhóm không hòa thì chỉ các dòng của nhóm hòa có mặt nạ 0; mặt nạ của nhóm còn lại giữ nguyên từng ô, kể cả các ô vốn đã bằng 0. Lô không có nhóm hòa thì mặt nạ không đổi.
  2. CPU, mô hình tí hon, vài bước: kiểm rằng hàm tính mất mát của TRL **thật sự nhận** mẫu số đã giảm và các dòng mặt nạ 0. Hai khóa `completion_mask` và `num_items_in_batch` của TRL 0.29.1 đã được `grpo_moi_b1.py` dùng; nếu bản TRL khác cấu trúc này thì phép kiểm phải dừng notebook ngay, không chạy tiếp trong im lặng.

### 5.4 Các lượt còn lại chỉ đổi cấu hình (không cần cài gì)

| lượt | cấu hình TRL cần có (kiểm ở dòng `[đè cấu hình]` của log) |
|---|---|
| Dr.GRPO | `loss_type="dr_grpo"`, `scale_rewards="none"`, μ=1, β 0,04, 500 bước |
| GRPO μ=2 (đối chứng) | mặc định lưới (`loss_type="dapo"`, `scale_rewards="group"`), `num_iterations=2`, 1.000 bước |
| GSPO | bí danh `gspo` (`importance_sampling_level="sequence"`, `epsilon=3e-4`, `epsilon_high=4e-4`, `num_iterations=2`) **cộng** `loss_type="grpo"`, 1.000 bước |

Dr.GRPO và GRPO μ=2 đã qua kiểm thử CPU ngày 6/11; GRPO μ=2 đã smoke trên T4 với khoảng 130 giây/bước.

---

## 6. Sửa lỗi của bản trước (GSPO)

- **Bản trước sai ở đâu:** bí danh `gspo` trong `harness/grpo_moi_b1.py` (6/11) đặt tỉ số theo câu, khoảng cắt 3e-4/4e-4 và μ=2, nhưng giữ `loss_type="dapo"` mặc định của lưới. TRL ghi rõ tổ hợp này *"silently length-weights each sequence's loss instead of applying the per-sequence objective GSPO prescribes"* và chỉ sang `loss_type="grpo"`.
- **Ảnh hưởng:** các lượt `gspo:spice:101:steps=1000,tag=s1000` trong `_bundles/luoi/CHAY_A.md` (dòng #15, #19, Colab C3) **không phải GSPO đúng nghĩa**. Chưa lượt nào trong số đó có kết quả, nên không có số nào phải rút lại.
- **Cách sửa:** thêm `loss=grpo` vào chuỗi mô tả lượt. Trong `grpo_moi_b1`, cấu hình bí danh được ghi trước, rồi cờ `--loss-type` của `grpo_codien` ghi đè lên. Chuỗi lượt đúng là `gspo:spice:101:loss=grpo,steps=1000,tag=s1000g`. Log phải có `'loss_type': 'grpo'` ở dòng `[đè cấu hình]`.

---

## 7. Kế hoạch chạy — theo thứ tự

### 7.1 Năm lượt, 1 hạt (101)

| # | thuật toán | chuỗi lượt cho `make_nb.py` | số bước | mốc so | ước lượng T4 |
|---|---|---|---|---|---|
| 1 | Dr.GRPO | `grpo:spice:101:loss=dr_grpo,scale=none,tag=drg` | 500 | GRPO A/A | 21–22 h (2–3 commit) |
| 2 | REINFORCE++ | `rpp:spice:101` | 500 | GRPO A/A | 21–22 h (2–3 commit) |
| 3 | GRPO μ=2 (đối chứng) | `grpo:spice:101:mu=2,steps=1000,tag=mu2` | 1.000 | GRPO A/A | khoảng 36 h (khoảng 4 commit) |
| 4 | GSPO | `gspo:spice:101:loss=grpo,steps=1000,tag=s1000g` | 1.000 | GRPO μ=2 | khoảng 36 h |
| 5 | DAPO (lọc nhóm hòa) | `dapo_ds:spice:101:eps=0.28,tag=dapo` | 500 | GRPO A/A | 21–22 h |

Tổng: kernel 1 và kernel 3 mỗi cái 2–3 commit, kernel 2 khoảng 4 commit, tức khoảng **9–10 commit × 11 giờ ≈ 100–110 giờ hạn mức**, khoảng **1,2 tuần** trên ba tài khoản Kaggle. GPU thứ hai của kernel 3 để trống; user có thể dùng nó cho online DPO (đã có mã `dpo_on`, user chọn từ 15/11) mà không tốn thêm hạn mức, vì Kaggle tính giờ theo phiên chứ không theo số GPU (mục 8). Các lượt μ=2 có thể chuyển sang Colab theo `_bundles/colab_luoi/HUONG_DAN.md` nếu muốn nhanh hơn.

**Thứ tự ưu tiên nếu thiếu giờ:** kernel 1 (REINFORCE++ và Dr.GRPO), rồi kernel 2 (GSPO và đối chứng), cuối cùng kernel 3 (DAPO). Thứ tự này đã sửa theo giá trị thông tin ở mục 11. DAPO lọc nhóm hòa có tác dụng kỳ vọng gần 0, nên là thứ cắt đầu tiên; GSPO tuy tốn nhưng là lượt duy nhất có cơ chế riêng còn hoạt động.

### 7.2 Bước 1 — cài phần mới và cập nhật kit

- Cài module theo mục 5, sửa `make_nb.py` và `make_kit.py` như mục 5.1.
- Dựng lại kit `luoi-kit` cho cả ba tài khoản (uyenle0712, trangphngngc, trangphuongngoc) và đẩy phiên bản mới lên Kaggle. Notebook kiểm md5 từng tệp, nên kit cũ sẽ làm notebook dừng ngay (đúng ý).

> ⚠️ [THIẾU ẢNH] Ảnh chụp dừng ở hai gạch đầu dòng trên; mục 7.2 có thể còn dòng tiếp theo chưa được chụp.

### 7.3 Bước 2 — probe 20 bước (khoảng 2 giờ mỗi kernel)

- Kernel A (uyenle0712): lượt 2 (REINFORCE++) và lượt 5 (DAPO).
- Kernel B (trangphngngc): lượt 4 (GSPO) và lượt 3 (GRPO μ=2).
- Trần giờ probe 2 giờ, để kịp in dòng đỉnh VRAM.
- **Đạt khi đủ cả:**
  - ô 3 báo selftest của module mới đạt, gồm cả phép kiểm trên mô hình tí hon;
  - log không có Traceback hay OOM, có dòng `[xong]` với tốc độ giây/bước và đỉnh VRAM (khoảng ≤ 14 GiB);
  - dòng `[đè cấu hình]` đúng như bảng mục 5.4; DAPO phải có `epsilon_high 0.28` và `num_iterations 1`;
  - DAPO: tỉ lệ nhóm bị lọc nằm trong (0; 1), dự kiến khoảng 0,15–0,35. Nếu luôn bằng 0 thì bộ lọc không chạy; nếu gần 1 thì phần thưởng đang hỏng;
  - REINFORCE++: độ lệch chuẩn hữu hạn và > 0, số lô trong cửa sổ tăng dần đến 8;
  - GSPO: `clip_ratio` **> 0** ở một số bước. Khoảng cắt 3e-4/4e-4 rất hẹp nên lần cập nhật thứ hai phải bị cắt một phần; nếu luôn bằng 0 thì μ=2 hoặc tỉ số theo câu chưa được áp, phải dừng lại kiểm;
  - GRPO μ=2: `clip_ratio` bằng 0 là **bình thường** (các lượt PPO μ=2 với ε=0,2 cũng bằng 0). Kiểm μ=2 đã áp bằng dòng cấu hình `num_iterations 2` và bằng nhịp thời gian (bước có sinh câu xen kẽ bước không sinh, nhanh hơn rõ).
- Dr.GRPO không cần probe riêng (cùng chi phí với GRPO, cấu hình đã kiểm CPU ngày 6/11).

### 7.4 Bước 3 — train (3 kernel, mỗi kernel 2 GPU)

- Kernel `luoi-b5-1` (uyenle0712): lượt 1 và lượt 2.
- Kernel `luoi-b5-2` (trangphngngc): lượt 3 và lượt 4.
- Kernel `luoi-b5-3` (trangphuongngoc): lượt 5; GPU còn lại để trống hoặc dùng cho online DPO nếu user chọn (mục 8).
- Với kernel 2 (lượt μ=2, 1.000 bước), chỉ giữ 3 điểm lưu mới nhất (biến `GIU_CK=3`). Lượt PPO 1.000 bước từng làm đầy đĩa vì lưu mỗi 25 bước.
- **Nối tiếp khi chạm trần 11 giờ:** dựng kernel mới trỏ tới kernel trước, cùng chuỗi lượt. Log nối tiếp **phải** có dòng `[nap default] … |lora_B| 0 → x>0`; thiếu dòng này là chạy lại từ S1, phải dừng.
- Theo dõi trong log mỗi 2 phút: bước hiện tại, giây/bước, thưởng, KL. KL của các lượt cũ nằm khoảng 0,002–0,05; vượt 0,1 kéo dài thì ghi lại.

### 7.5 Bước 4 — chấm tập kiểm

- Mỗi lượt: tạo một dataset Kaggle chứa adapter ở điểm lưu cuối (`checkpoint-500`, hoặc `checkpoint-1000` với lượt μ=2), làm giống dataset `trangphngngc/ppo-ck1000` ngày 14/11. Ghi lại md5 của tệp adapter.
- Dựng notebook chấm bằng `make_test_nb2.py` theo mẫu lượt PPO 14/11: đặt bước điểm lưu là 500 cho lượt 1, 2, 5, 6 và 1.000 cho lượt 3, 4 (lượt 6 đã bỏ); thêm dataset adapter vào danh sách dataset.
- Log chấm phải có `[kiểm hoà] ≥16/20` và `[kiem bo cham] 10/10`. Đủ 4.463 bước chạm.
- Nên chấm thêm chế độ bước không chạm (`nontap`) để báo riêng scroll và back, vì `navigate_back` là điểm yếu đã biết.
- Tải các tệp `score_<tên>_test_raw.jsonl` về `runs/luoi/<ngày>/test_b5/`. Độ đo văn bản (BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE, chrF, BERTScore) chạy bằng kernel CPU như các lượt PPO.

### 7.6 Bước 5 — đưa vào bảng tổng hợp

- Thêm 5 nhánh vào `harness/bang_tong_hop.py`:
  - danh sách tập kiểm, nhóm "lưới RL";
  - mục 1 "So thuật toán RL", đặt sau hai hàng PPO. Tên hiển thị:
    - "Dr.GRPO (bỏ std, bỏ chia độ dài)";
    - "REINFORCE++-baseline (std cửa sổ 8 lô)";
    - "DAPO (lọc nhóm hoà)";
    - "GRPO, μ = 2 (đối chứng cho GSPO)";
    - "GSPO (tỉ số theo câu, μ = 2)".
- Thêm "GRPO μ=2" vào danh sách mốc so của mục 1, để có cột so GSPO với lượt đối chứng.
- Sửa chú thích dưới bảng:
  - bỏ câu "Dr.GRPO (treo ở checkpoint-475)";
  - thêm: REINFORCE++ lấy std trên cửa sổ 8 lô sinh, là xấp xỉ chuẩn hóa toàn cục; DAPO lọc nhóm hòa, không lấy mẫu bù, μ = 1 nên Clip-Higher không tác dụng, giữ β 0,04 (bài gốc β = 0); trong cấu hình này Dr.GRPO gần như trùng RLOO (chỉ khác một hằng số), còn REINFORCE++ gần như Dr.GRPO với KL được cân lại như GRPO; GSPO và đối chứng μ = 2 chạy 1.000 update để đi đúng 1.000 câu nhắc.
- Thêm một dòng mô tả **dải GRPO [59,74; 60,65]** (ba lượt GRPO + SPICE) ngay trên bảng, để người đọc tự đối chiếu.
- Chạy lại script để sinh lại `report/334_BANG_KET_QUA_TONG_HOP.md`. Holm được tính lại tự động trên họ phép so mới.
- Lượt cũ "GRPO bỏ chia std" (`drgrpo`, dừng ở bước 475, vẫn `loss_type="dapo"`) **không phải Dr.GRPO đầy đủ**. Lượt Dr.GRPO mới thay vai trò đó; lượt cũ để nguyên, không chấm.

### 7.7 Bảng điền kết quả (để trống, điền khi có số)

| thuật toán | mốc so | exec | trong dải GRPO [59,74; 60,65]? | Δ so với mốc [KTC95] | p Holm | Δ so với ck500 | Δ so với SFT tiếp |
|---|---|---|---|---|---|---|---|
| Dr.GRPO | A/A 59,74 | | | | | | |
| REINFORCE++ | A/A 59,74 | | | | | | |
| DAPO (lọc nhóm hòa) | A/A 59,74 | | | | | | |
| GRPO μ=2 | A/A 59,74 | | | | | | |
| GSPO | GRPO μ=2 | | | | | | |

---

## 8. Việc user phải quyết (agent không tự làm)

1. **Có chạy không**, và chạy bản đủ (3 kernel, 5 lượt, khoảng 100–110 giờ T4) hay bản gọn (chỉ kernel 1 và 2: REINFORCE++, Dr.GRPO, GSPO, GRPO μ=2; khoảng 80 giờ). Bản gọn bỏ DAPO, vì sau tranh luận nó là lượt có tác dụng kỳ vọng thấp nhất (mục 11). Đây là thay đổi so với bản trước, vốn đề xuất bỏ GSPO.
2. **Giữ β=0,04 cho mọi lượt** (đề xuất, để đồng bộ lưới) hay theo bài gốc β=0 cho DAPO và Dr.GRPO.
3. **Có dùng GPU trống của kernel 3 cho online DPO không.** Mã `dpo_on` đã có, và việc này không tốn thêm hạn mức. Online DPO không thuộc họ "sau GRPO", nên nếu chạy thì ghi là dòng thêm, không tính vào 4 thuật toán.
4. Nếu có thuật toán **vượt trên dải GRPO** và hơn A/A sau Holm: **có đổi phương pháp chính của luận văn không**. Đề xuất: không đổi khi chỉ có một hạt; chạy hạt 202 theo luật 6 ở mục 4, rồi ghi thành kết quả phụ.
5. Có đưa phép so này vào luận văn và slide không. Nếu có, nên đặt ở Slide 16 (kiểm tra độ bền) dưới dạng một câu: *"thêm bốn thuật toán phổ biến 2025 cũng không vượt GRPO có ý nghĩa"*.
6. Cài mã, mọi thao tác git và Kaggle: user hoặc chat khác tự làm theo mục 5 và 7.

---

## 9. Nguồn

- DAPO: https://arxiv.org/abs/2503.14476 (đã đọc HTML: mục 2.3 bỏ KL, mục 3 bốn kỹ thuật, Bảng 1, siêu tham số mục 4)
- GSPO: https://arxiv.org/abs/2507.18071 · blog Qwen https://qwenlm.github.io/blog/gspo/ (khoảng cắt 3e-4/4e-4, μ=4, Routing Replay, Qwen3-30B-A3B)
- Dr.GRPO: https://arxiv.org/abs/2503.20783 · ICLR Blogposts 2026 "From REINFORCE to Dr. GRPO" https://iclr-blogposts.github.io/2026/blog/2026/llm-post-training/ (hai thiên lệch độ dài và độ khó)
- REINFORCE++: https://arxiv.org/html/2501.03262v9 (chuẩn hóa toàn cục, lô ≥1024, Bảng 1 và 4, Phụ lục A)
- Độ phổ biến: verl (adv_estimator `grpo`, `rloo`, `reinforce_plus_plus(_baseline)`; policy_loss `gspo`, `cispo`, `geo_mean`; DAPO qua `filter_groups`) · TRL `GRPOConfig` (`loss_type` dapo, dr_grpo, cispo, sapo…; `importance_sampling_level`; `scale_rewards`) · TRL PR #6042 và issue #3823 (GSPO cần `loss_type="grpo"`) · "The GRPO Family" survey https://github.com/FredericVAN/GRPO-Family-Survey · mẫu 153 bài của dự án (`report/reports/Baseline RL so với GRPO.md`: RLVR 42 bài, DAPO 15, Dr.GRPO 8, GSPO 5, REINFORCE++ 5, RLOO 5)
- MathForge (ICLR 2026, https://arxiv.org/abs/2601.20614): GRPO, Dr.GRPO, GPG, DAPO, GSPO trung bình 6 bộ đo lần lượt 37,61 · 37,40 · 37,93 · 37,94 · 37,71, tức lệch nhau dưới 0,33 khi kiểm soát chặt.

**Giới hạn của lượt nghiên cứu này:** ba tác tử đọc bài song song bị ngắt giữa chừng, nên không có ghi chú của chúng. Các điểm then chốt ở mục 2 được đối chiếu trực tiếp từ toàn văn DAPO, GSPO và REINFORCE++; với Dr.GRPO thì từ bài phân tích ICLR Blogposts 2026 và ghi chú cũ của dự án. Venue của DAPO và Dr.GRPO chưa xác minh tận trang kỷ yếu. Cách cài ở mục 5.3 dựa trên mã nhánh `main` của TRL và các khóa mà `grpo_moi_b1.py` đã dùng với TRL 0.29.1; phép tự kiểm thứ hai ở mục 5.3 là để bắt trường hợp bản 0.29.1 khác.

---

## 10. Phản biện: action này đã đủ hợp lý để chạy 1 hạt chưa?

**Kết luận: CHẠY ĐƯỢC.** Bản trước còn 4 chỗ sai hoặc thiếu và 2 chỗ nên cải thiện. Cả sáu đã được sửa ngay trong thân file (mục 0, 3, 4, 5.3, 5.4, 7, 8). Dưới đây là từng điểm tranh luận.

### Điểm 1 — Một hạt có đủ không?

- **Phản bác:** nhiễu giữa các lần train của chính GRPO đã đo được là 0,72 (ck500 hạt 101 so với hạt 202) và 0,92 (ck500 so với A/A). Con số này **lớn hơn** khoảng cách thường gặp giữa các thuật toán không dùng critic …

> ⚠️ [THIẾU ẢNH] Phần còn lại của mục 10 (tiếp Điểm 1, Điểm 2 về Clip-Higher/phép cắt ở μ=2 mà các mục 2.1, 3, 5.3 viện dẫn, và các điểm sau) không có trong bộ ảnh.

---

## 11. Tranh luận chốt danh sách 4 thuật toán

**Kết luận: CHỐT DAPO · GSPO · Dr.GRPO · REINFORCE++.** Không ứng viên nào khác đạt cùng lúc bốn tiêu chí bên dưới tốt hơn bốn cái này. Tranh luận có làm đổi **thứ tự giá trị thông tin** và **bỏ lượt Dr.GRPO β=0,014**; cả hai thay đổi đã áp vào thân file.

### 11.1 Bốn tiêu chí

1. **Phổ biến 2024–2026:** có sẵn trong verl/TRL, được báo cáo kỹ thuật lớn dùng, xuất hiện nhiều làm mốc so.
2. **Cho thông tin mới:** trong đúng cấu hình của bài, không trùng một lượt đã chạy (GRPO, SCST, REINFORCE, RLOO, PPO).
3. **Cơ chế còn hoạt động:** với μ=1 (hoặc μ=2), lr 1e-5, LoRA, câu khoảng 10 token, phần thưởng liên tục.
4. **Làm được:** bằng TRL 0.29.1 và lưới có sẵn, trên Kaggle T4.

### 11.2 Phát hiện then chốt: trong cấu hình này, nhiều thuật toán "mới" trùng lượt đã chạy

- **Tỉ số quan trọng gần như bằng 1.** Sau một bước cập nhật, tỉ số mỗi token chỉ lệch cỡ 0,1% [suy luận từ KL 0,002–0,13 sau hàng trăm bước và `clip_ratio` = 0 ở các lượt PPO μ=2]. Hệ quả: mọi thuật toán **chỉ sửa tỉ số hoặc phép cắt** ở ngưỡng cỡ 0,2 đều cho cùng gradient với GRPO:
  - **CISPO:** ngưỡng cắt trên 5,0 không bao giờ chạm, nên trùng GRPO (μ=1) hoặc trùng GRPO μ=2;
  - **SAPO:** cổng mềm ≈ 1 khi tỉ số ≈ 1;
  - **GMPO:** trung bình hình học của các tỉ số ≈ 1, nên trùng GRPO gộp theo câu;
  - **Clip-Higher của DAPO** và **phép cắt của PPO:** không chạm ngưỡng.
- **GSPO là ngoại lệ duy nhất trong nhóm này.** Khoảng cắt 3e-4/4e-4 cùng cỡ với độ lệch thật của tỉ số theo câu, nên phép cắt **thật sự xảy ra** ở lần cập nhật thứ hai. Cơ chế riêng của GSPO vẫn hoạt động.
- **Dr.GRPO ≈ RLOO đã chạy.** Dr.GRPO dùng $A = r - \bar r$; RLOO trong lưới dùng $A = \frac{G}{G-1}(r - \bar r)$, chỉ khác hằng số 8/7. Cách chia mẫu số cũng chỉ khác một hằng số khi các câu dài gần bằng nhau. Adam gần như không phân biệt được hai thứ này. RLOO đã đo được **59,44**, thấp nhất lưới.
- **REINFORCE++ ≈ Dr.GRPO nhưng KL được cân lại như GRPO.** $A = (r - \bar r)/\sigma_{\text{toàn cục}}$, với $\sigma_{\text{toàn cục}}$ thay đổi chậm quanh 0,35. Dưới Adam, nó tương đương Dr.GRPO với β chia cho khoảng 2,9, tức khoảng 0,014. Đó **đúng** là vai của lượt độ nhạy Dr.GRPO β=0,014 ở bản trước, nên lượt đó bỏ được.
- **ReMax ≈ SCST đã chạy** (cùng dùng câu greedy làm mốc).

Phát hiện này có giá trị riêng cho luận văn: nó cho phép trả lời "còn CISPO, SAPO, GMPO, ReMax thì sao?" **bằng lập luận và số đã có**, không cần chạy thêm. Phải ghi rõ đây là [suy luận] từ cấu hình; riêng hoạt động phép cắt của GSPO sẽ được kiểm trong probe.

### 11.3 Từng thuật toán trong danh sách: giữ hay thay?

| | Ủng hộ giữ | Phản bác | Phán quyết |
|---|---|---|---|
| **REINFORCE++** | Phép thử sạch duy nhất cho câu hỏi "chia std **theo từng nhóm** có lợi hay hại", trong khi giữ cân bằng thưởng/KL giống GRPO. Cặp GRPO và REINFORCE++ chỉ khác đúng cách chia. | Cửa sổ 8 lô là xấp xỉ của chuẩn hóa toàn cục. | **Giữ — giá trị thông tin cao nhất.** |
| **GSPO** | Nổi tiếng nhất (Qwen3). Là cái duy nhất có cơ chế riêng còn hoạt động trong cấu hình này. Lượt đối chứng GRPO μ=2 đi kèm cũng là lần đầu dự án đo tác dụng của μ. | Tốn nhất (2 lượt × khoảng 36 giờ). Lý do gốc (MoE, câu dài) không có mặt. | **Giữ — thứ hai.** |
| **DAPO** | Phổ biến nhất sau GRPO (15/42 bài). Lấy mẫu động là thành phần duy nhất chạm vào bài này (20–31% nhóm hòa). | Lọc không bù chỉ đổi thang theo lô; dưới Adam, tác dụng kỳ vọng gần 0. | **Giữ — thứ ba.** Kỳ vọng ≈ A/A, ghi trước. Cắt đầu tiên nếu thiếu giờ. |
| **Dr.GRPO** | Top-3 phổ biến, hội đồng dễ hỏi đúng tên này. Vì gần như trùng RLOO, lượt này cho **một phép đo độ dao động** giữa hai lượt gần cùng thuật toán, thứ dự án đang thiếu khi chỉ chạy 1 hạt. | Gần như không cho thông tin mới về thuật toán; có thể suy ra từ RLOO mà không tốn 22 giờ. | **Giữ — thứ tư.** Viết trong luận văn là "trong cấu hình này Dr.GRPO và RLOO gần như trùng nhau; chênh lệch giữa hai lượt cho thấy độ dao động giữa các lần chạy". |

### 11.4 Các ứng viên thay thế đã xét và bị loại

| ứng viên | phổ biến | thông tin mới / cơ chế còn hoạt động | lý do loại |
|---|---|---|---|
| CISPO (MiniMax-M1; được chọn trong ScaleRL) | cao | không: trùng GRPO vì tỉ số ≈ 1 | trả lời bằng lập luận ở 11.2 |
| SAPO (Qwen, có trong TRL) | trung bình–cao | không: cổng mềm ≈ 1 | như trên |
| GMPO | trung bình | không: ≈ GRPO gộp theo câu | như trên |
| GDPO (2026, nhiều kênh thưởng) | trung bình | chỉ có nghĩa với thưởng ghép (SA-SPICE-v3), không với SPICE đơn | **trục khác**; đáng làm riêng trên SA-SPICE-v3 sau này |
| VAPO | thấp–trung bình | cần critic; thử trên 32B | PPO đã đại diện họ có critic |
| GVPO (NeurIPS 2025) | thấp làm mốc | có | ít được dùng làm mốc so; không thay được bất kỳ cái nào trong bốn về độ phổ biến |

> ⚠️ [THIẾU ẢNH] Bảng 11.4 có thể còn hàng sau GVPO (ví dụ online DPO, ReMax), và có thể có thêm nội dung trước mục 12; bộ ảnh không chụp tới.

---

## 12. PHÁN QUYẾT CUỐI — chốt bốn thuật toán, nhưng sửa thiết kế trước khi chạy

### 12.1 Kết luận dứt khoát

**Chốt đúng bốn họ phương pháp:**

1. **DAPO;**
2. **GSPO;**
3. **Dr.GRPO;**
4. **REINFORCE++ with Baseline.**

Đây là bốn phương pháp hậu-GRPO được dùng rộng rãi và dễ được hội đồng nhận diện nhất sau khi loại:

- RLOO và SCST/ReMax vì dự án đã chạy;
- PPO vì dự án đã chạy;
- CISPO, SAPO, GMPO vì ở cấu hình hiện tại tỉ số gần 1 làm cơ chế riêng gần như bất hoạt;
- GDPO vì chỉ hợp với phần thưởng nhiều kênh như SA-SPICE-v3, không phải SPICE đơn;
- VAPO vì cần critic và PPO đã đại diện họ này;
- online DPO vì là đối chứng hậu huấn luyện khác họ, không phải biến thể hậu-GRPO. Có thể chạy thêm trên GPU trống, nhưng không tính vào bốn thuật toán.

**Cách gọi an toàn:** "bốn phương pháp hậu-GRPO được chọn từ mẫu tài liệu khảo sát", không gọi "bốn thuật toán phổ biến nhất toàn ngành".

**Một hạt 101 được phép cho vòng thăm dò đầu.** Kết quả chỉ được gọi là "kết quả thăm dò ở seed 101"; không xếp hạng thuật toán và không viết "GRPO tốt nhất" hay "không thuật toán nào vượt GRPO" từ một hạt.

### 12.2 Vì sao action cũ chưa được chạy

Ba phản biện độc lập cùng chỉ ra bốn blocker:

1. **DAPO cũ không phải DAPO.** Chỉ mask nhóm hòa mà không lấy mẫu bù không phải dynamic sampling của bài. Khi μ=1, Clip-Higher bất hoạt; token-level loss và lọc câu quá dài đã có sẵn. Tên đúng của cấu hình cũ chỉ là "ablation lọc nhóm phần thưởng đồng nhất lấy cảm hứng từ DAPO".
2. **REINFORCE++ cũ không phải REINFORCE++.** Cửa sổ tám minibatch chứa mẫu từ tám policy khác nhau, lại bị xóa khi resume, không phải global on-policy batch normalization của bài.
3. **Đối chứng GSPO cũ bị confound.** GSPO dùng `loss_type="grpo"`, còn GRPO μ=2 đối chứng dùng `loss_type="dapo"`. Chênh lệch khi đó lẫn cả tỉ số theo câu và cách gộp loss.
4. **"Dải GRPO [59,74; 60,65]" không phải ước lượng nhiễu train.** Ba điểm này trộn hai implementation và hai seed; min–max của ba lượt không phải khoảng tin cậy hoặc khoảng tương đương. Chỉ được in như thông tin mô tả lịch sử, không dùng làm luật suy luận hoặc điều kiện chạy seed thứ hai.

Vì vậy, mục 5.2, 5.3, luật dải ở mục 4 và kế hoạch lượt ở mục 7 của bản cũ không được giao nguyên trạng.

### 12.3 Thiết kế cuối phải bàn giao — sáu lượt, một seed

Muốn giữ đúng bốn tên, cần **4 phương pháp + 2 đối chứng khớp**, tổng cộng sáu lượt:

| # | lượt thăm dò seed 101 | cấu hình chịu lực | mốc so trực tiếp |
|---|---|---|---|
| 1 | GRPO batch lớn | 16 prompt × G=8 = 128 completion được sinh dưới cùng một policy đóng băng; một optimizer step sau toàn batch; group normalization như GRPO | đối chứng cho REINFORCE++ |
| 2 | REINFORCE++-Baseline | cùng đúng 128 completion on-policy của một policy đóng băng; trừ mean trong từng nhóm, rồi chuẩn hóa trên toàn bộ 128 advantage; cùng lịch update và KL với lượt 1 | GRPO batch lớn |
| 3 | GRPO μ=2, sequence-mean control | `loss_type="grpo"`, importance ratio theo token, μ=2; cùng prompt stream, update, KL và batch với GSPO | đối chứng cho GSPO |
| 4 | GSPO | `loss_type="grpo"`, importance ratio theo câu, μ=2, clip 3e-4/4e-4; cùng mọi thứ khác với lượt 3 | lượt 3 |
| 5 | GRPO A/A μ=1 | mốc hiện hành cùng mã lưới; nếu không khóa được đúng phiên bản/mã của A/A lịch sử thì chạy lại trong kit mới | đối chứng cho Dr.GRPO và DAPO |
| 6a | Dr.GRPO + common reference-KL | `loss_type="dr_grpo"`, `scale_rewards="none"`, μ=1, β=0,04; ghi rõ đây là Dr.GRPO objective dưới KL chung, không phải recipe nguyên bản β=0 | lượt 5 |
| 6b | DAPO-style dynamic sampling + common reference-KL | xem mục 12.4; token-level loss, overlong filtering, dynamic sampling thật; β=0,04 để giữ đối chứng, ghi rõ khác recipe gốc β=0 | lượt 5 |

Ghi chú: bảng có bảy hàng vì lượt 6 gồm **hai phương pháp riêng**, nhưng số **train mới** là sáu nếu lượt GRPO A/A lịch sử được xác minh tái sử dụng; là bảy nếu phải chạy lại A/A trong kit mới.

### 12.4 Bốn yêu cầu cài đặt bắt buộc

**A. DAPO phải dùng dynamic sampling thật**

- Khóa trước **cùng pool 1.000 prompt** của ck500; không lấy dữ liệu ngoài pool.
- Tại mỗi optimizer step, sinh nhóm G=8. Nếu std reward của nhóm bằng 0, **không đưa nhóm đó vào batch update và lấy tiếp một prompt khác từ cùng pool**, cho đến khi đủ đúng số nhóm hữu hiệu như GRPO.
- Policy phải giữ nguyên trong toàn bộ quá trình lấy bù của một batch.
- Báo hai ngân sách:
  1. số prompt/completion **được dùng để update**;
  2. tổng prompt/completion **đã rollout**, gồm nhóm bị loại.
- Vì phần lấy mẫu động làm tăng rollout compute, không được nói DAPO và GRPO "cùng compute"; chỉ nói cùng số nhóm update.

> ⚠️ [THIẾU ẢNH] Ảnh cuối dừng ở đây (dòng kế tiếp bị cắt, không đọc được). Phần còn lại của yêu cầu A và ba yêu cầu B, C, D của mục 12.4, cùng mọi nội dung sau đó, không có trong bộ ảnh.
