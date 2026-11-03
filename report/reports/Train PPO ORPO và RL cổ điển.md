# Giữ TRL, tự cài PPO, đo ORPO

Đến 3/11/2026 đề tài **chưa có số test nào cho PPO, cho ORPO tầng câu hay cho các nhánh cổ điển vừa viết mã**, nên câu trả lời đúng với thầy là "chưa đo, đây là kế hoạch đo", không phải "chúng kém". Về công cụ, tôi không tìm thấy framework nào đang bảo trì có đủ PPO, critic nhìn được ảnh và Qwen2.5-VL theo một đường đã có kết quả, nên nên **giữ TRL 0.29.1 và lớp con của `GRPOTrainer`**; Colab chỉ là chỗ mở rộng bộ nhớ cho critic, không phải lý do đổi công cụ. Đầu giá trị nhỏ tách gradient hiện có không phải critic chuẩn, và phải báo là bản rút gọn; muốn chặn đòn này cần một nhánh critic riêng, ước tính 5 đến 22 USD trên Colab [suy]. Với ORPO, nên sửa script DPO đã có của dự án thành ORPO mức câu từ S1, chạy ba hàng có song sinh λ = 0. Hàng công bằng nhất với ck500, dùng cặp lấy mẫu theo chính sách và xếp bằng SPICE, là **bản thích nghi của chính đề tài**, vì tôi không tìm thấy biến thể "ORPO trực tuyến" nào đã công bố. Với RL cổ điển, sáu hàng đáng chạy là REINFORCE, SCST, A2C, PPO, soft Q off-policy và TRPO (không vừa thì thay bằng ES), còn DDPG và TD3 chỉ nêu lý do không áp dụng. Trên test hiện có, ck500 đạt exec 60,65 và bốn lượt lưới cùng nằm cách dưới một điểm, một hạt giống, không phép so nào với ck500 loại được 0, nên GRPO + SPICE mới chỉ thuộc nhóm dẫn đầu của những gì đã chấm.

Quy ước trong báo cáo: **[đo]** là số từ tệp hoặc log của dự án, **[suy]** là ước lượng hay suy luận chưa chạy. Venue ghi cạnh tên bài; "preprint" nghĩa là tôi chưa thấy venue. Số trích từ bài khác lấy chủ yếu từ bản arXiv, chưa đối chiếu bản đăng, nên phải mở lại trước khi vào luận văn. Số val không xuất hiện ở đây; chỗ nào cơ chế dựa vào val thì chỉ tả định tính.

## Bốn lượt lưới và ck500 cách nhau dưới một điểm exec

Mọi số dưới đây là test, UGround, hạt 101, 500 bước, cùng câu nhắc với ck500 [đo] (`report/320` §14.1). Hai hạt ck500 đã chênh nhau 0,72 exec, MDE là 2,11, và tiêu chí "hơn" của dự án đòi KTC ghép cặp loại 0 cùng |Δ| ≥ 1, kèm nhãn một hạt giống (`report/326` §7).

| nhánh | exec | D.3 | AitW đầy đủ | đúng loại thao tác | so ck500 (exec) | so S1/101 (exec) |
|---|---:|---:|---:|---:|---|---|
| S1/101 | 59,11 | 65,49 | 74,37 | 94,35 | | |
| ck500 (GRPO + SPICE) | **60,65** | 67,02 | 76,25 | 95,97 | | +1,55 [+0,80; +2,33] |
| GRPO + ROUGE-L | 60,63 | 67,04 | 76,79 | 96,86 | −0,02 [−0,54; +0,49] | +1,52 [+0,78; +2,29] |
| mốc greedy kiểu SCST + SPICE | 60,54 | 66,88 | 76,14 | 96,08 | −0,11 [−0,56; +0,35] | +1,43 [+0,79; +2,11] |
| GRPO + METEOR | 60,27 | 66,75 | 76,27 | 96,28 | −0,38 [−0,95; +0,19] | +1,17 [+0,39; +1,97] |
| GRPO + CIDEr-D (số tạm, 4.428 bước) | 60,25 | 66,44 | 75,97 | 96,05 | −0,36 [−0,87; +0,14] | +1,17 [+0,43; +1,96] |

Bảng này cho phép nói ba điều và cấm nói một điều. Mọi lượt đều hơn S1 nhưng dưới MDE, và với bốn lượt lưới thì chưa tách được công của RL khỏi công của việc train thêm, vì SFT tiếp đã train đủ 500 bước mà chưa chấm test. Về độ đo văn bản, **ck500 không dẫn đầu cột nào**, và GRPO + CIDEr-D còn thấp hơn ck500 ngay trên CIDEr-D, −5,53 [−10,21; −1,20], chưa giải thích được (`report/320` §14.4). Tính cả bước không chạm, lợi ích exec của ck500 giảm còn +0,39 [−0,21; +0,99] (`report/328`). Điều bị cấm là xếp hạng các hàng trên.

Riêng ck500 có thêm ba phép kiểm mà các hàng khác chưa có [đo] (`report/320` §1). Nhánh kiểm sàn `xao101`, cùng 500 bước GRPO nhưng điểm SPICE được ghép ngẫu nhiên giữa các mẫu, cho exec 59,11, bằng đúng S1; ck500 − `xao101` **+1,55 [+0,81; +2,30]** p = 2e−5, nên mức tăng gắn với tín hiệu thưởng chứ không chỉ với vòng lặp GRPO. Hạt GRPO thứ hai ck500/202 đạt 59,94, hơn S1/101 +0,83 p = 0,036. Trên tác vụ S1 chưa thấy (ACU, 1.484 bước) ck500 − S1 là +4,58 [+3,17; +6,05], vượt MDE của tập kiểm chính. Ngược lại, ở bước scroll ck500 giảm −6,23 so với S1, là tác hại phải khai. Các phép kiểm này ủng hộ việc GRPO + SPICE có tác dụng so với S1, nhưng không so nó với thuật toán khác nên không hỗ trợ một xếp hạng.

Trạng thái mã cũng cần nói rõ: probe PPO `trangphngngc/luoi-probe-ppo` vẫn đang chạy lúc 21:14 ngày 3/11 và chưa có đầu ra, nên VRAM, s/bước và `v_ev` của PPO đều chưa biết. Bảy nhánh cổ điển mới qua selftest và chạy thử CPU, chưa probe T4. ORPO mức câu chưa có mã.

## PPO: giữ TRL, đặt tên trung thực từng loại critic

### Công cụ phổ biến nhất đã bỏ PPO, các framework mới chưa ghép được critic với ảnh

`PPOTrainer` của TRL chuyển sang `trl.experimental.ppo` ở [v0.26.0](https://github.com/huggingface/trl/releases/tag/v0.26.0) và **bị xoá hẳn ở [v1.13.0](https://github.com/huggingface/trl/releases/tag/v1.13.0)**; người bảo trì nêu lý do là không còn ai bảo trì và gần như không có người dùng ([PR #7020](https://github.com/huggingface/trl/pull/7020)). Bản còn trong v0.29.1 cũng không dùng được cho đề tài: `generate()` và `forward()` chỉ truyền `input_ids`, `attention_mask`, không có `pixel_values` hay `image_grid_thw`, và thưởng phải là một `reward_model` chứ không phải hàm Python ([mã v0.29.1](https://github.com/huggingface/trl/blob/v0.29.1/trl/experimental/ppo/ppo_trainer.py)). Transformers cũng không có lớp `SequenceClassification` hay `TokenClassification` cho `qwen2_5_vl` ([modeling_auto](https://github.com/huggingface/transformers/blob/main/src/transformers/models/auto/modeling_auto.py)), nên cách dựng critic quen thuộc không đi thẳng được.

| Công cụ | PPO có critic | Qwen2.5-VL | Critic thấy ảnh | Đánh giá |
|---|---|---|---|---|
| TRL 0.29.1 + lớp con `GRPOTrainer` | Tự cài; trainer cố ý nhận lợi thế cỡ (B, T) ([mã](https://github.com/huggingface/trl/blob/v0.29.1/trl/trainer/grpo_trainer.py)) | Đang chạy trong dự án | Tuỳ cách cài | **Chọn**: T4 12,71 GiB [đo], cùng đường sinh với ck500 |
| OpenRLHF | Có | Có VLM | **Cấm bằng `assert`**: "VLM training does not support critic model" ([dòng 661](https://github.com/OpenRLHF/OpenRLHF/blob/26494490bc237f6c3af62dab6117e6bbb0a78dba/openrlhf/cli/train_ppo_ray.py#L661)) | Loại |
| veRL | Có, ví dụ PPO chỉ văn bản | Script GRPO cho 2.5-VL-7B | Có đường dự phòng qua lớp TRL đã bị xoá; chưa thấy kết quả công khai ([issue #804](https://github.com/verl-project/verl/issues/804)) | Dựng đắt, công thức 1 GPU 24 GB còn là PR mở và chỉ cho mô hình văn bản 1,5B ([PR #8405](https://github.com/verl-project/verl/pull/8405)) |
| SkyRL | Có | Qua FSDP | `forward` của critic không có tham số ảnh ([mã](https://github.com/NovaSky-AI/SkyRL/blob/bd35ce1/skyrl/backends/skyrl_train/workers/model_wrapper.py)) | Có thể chạy mà critic mù ảnh [suy] |
| AReaL | Có | Có trong bảng model | Critic nạp bằng `AutoModelForTokenClassification` ([mã](https://github.com/areal-project/AReaL/blob/main/areal/engine/fsdp_engine.py)) | Nhiều khả năng không nạp được [suy] |
| Molt (NVIDIA) | Có, tuỳ chọn | Có nhắc trong mã | **Có mã** ([critic_actor.py](https://github.com/NVIDIA-NeMo/labs-molt/blob/a2f3fe9/molt/trainer/workers/critic_actor.py)) | Đòi CUDA 13 ([README](https://github.com/NVIDIA-NeMo/labs-molt/blob/main/README.md)); CUDA trên Colab chưa kiểm |
| RL4LMs | Có PPO, A2C, TRPO, NLPO, có thưởng metric ([README](https://github.com/allenai/RL4LMs/blob/main/README.md)) | Không | Không | Lần đẩy cuối 3/2024, chỉ văn bản |
| Unsloth · Tinker | Không ([Unsloth](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide)) · có `ppo` loss nhưng không thấy đường train critic ([Tinker](https://tinker-docs.thinkingmachines.ai/tinker/losses)) | Unsloth có vision RL theo GRPO · Tinker không có model này ([danh sách](https://thinkingmachines.ai/tinker/)) | Không | Loại |

Lý do quan trọng hơn cả tiện lợi: dự án đã khoá đường sinh, dtype và dữ liệu của ck500 rồi đo kiểm hoà. Đổi framework làm lẫn biến "thuật toán" với biến "công cụ", đúng thứ phép so muốn tránh [suy]. Khi viết phải khai đây là cài đặt tự viết trên `GRPOTrainer`, và dùng lý do ở đoạn trên để giải thích. Không có framework nào trong bảng được chạy thử; các kết luận dựa trên đọc mã.

### Đầu giá trị nhỏ hiện có không phải critic chuẩn, và critic chuẩn đắt hơn nhiều lần

Chuẩn mà người phản biện chờ đợi là mô hình tách riêng, khởi tạo từ điểm lưu đã huấn luyện, thay lớp unembedding bằng đầu vô hướng: [InstructGPT](https://arxiv.org/abs/2203.02155) mô tả đúng vậy, [Stiennon et al.](https://arxiv.org/abs/2009.01325) tách hoàn toàn để cập nhật giá trị không phá policy và báo mạng tách hơn mạng chung, [VinePPO](https://arxiv.org/abs/2410.01679) (ICML 2025) gọi đó là cách làm điển hình. Nhưng critic không buộc phải cùng cỡ: InstructGPT dùng RM 6B cho PPO mọi cỡ và báo kết quả mạnh ngang. Các bài bỏ critic cũng phản ứng với đúng chi phí này: [RLOO](https://aclanthology.org/2024.acl-long.662) (ACL 2024) nêu PPO có thể phải nạp tới bốn mô hình, [DeepSeekMath](https://arxiv.org/abs/2402.03300) (preprint) nói GRPO bỏ critic để giảm tài nguyên.

`harness/grpo_ppo.py` thì khác hẳn: MLP `Linear(2048, 512) → ReLU → Linear(512, 1)`, **1.049.601 tham số**, đọc trạng thái ẩn đã `detach`, khởi tạo V = 0, không huấn luyện trước, mọi đặc trưng đều đến từ policy. Chính docstring ghi đây không phải critic đủ cỡ. Tôi không thấy bài nào ở trên dùng cấu hình này, cũng không tìm được nghiên cứu trực tiếp về đầu giá trị trên đặc trưng tách gradient cho LLM, nên phải trình như bản rút gọn. Đọc mã cho thấy công thức GAE, căn hàng V(s_t), đích V và thứ tự trộn lô đều đúng, và không có lỗi làm sai gradient; vấn đề nằm ở khả năng biểu diễn, không ở cài đặt.

Bảng dưới là tính toán, không phải đo, lấy nền policy ~13 GiB và giả định critic chạy tuần tự nên kích hoạt không cộng dồn [suy]. Quy đổi 16 byte/tham số lấy từ con số 112 GB cho 7B của VinePPO. Qwen2.5-VL-3B có [3.754.622.976 tham số](https://huggingface.co/api/models/Qwen/Qwen2.5-VL-3B-Instruct), LoRA 14.966.784.

| Thiết kế critic | Thấy ảnh | Đỉnh ước [suy] | T4 ~14,6 | L4 ~22 | A100 40 | A100 80 / G4 ~96 | Tên khi báo |
|---|---|---:|---|---|---|---|---|
| Đầu MLP nhỏ (đang có) | Qua đặc trưng policy | ~13 GiB | Vừa | Vừa | Vừa | Vừa | "PPO, đầu giá trị nhỏ tách gradient (bản rút gọn)" |
| Adapter LoRA thứ hai trên backbone đóng băng | Có | ~13,3 GiB | Vừa, biên ~1 GiB | Vừa | Vừa | Vừa | "PPO, critic LoRA (tham số train tách khỏi policy, chung phần đóng băng)" |
| Bản sao NF4 đóng băng + LoRA | Có | ~16 GiB | Không | Sát 17 GB | Vừa | Vừa | như trên, ghi rõ bản sao riêng |
| Bản sao fp16 đóng băng + LoRA | Có | ~20,5 GiB | Không | Vượt mức 17 GB | Vừa | Vừa | như trên |
| Bản sao train toàn bộ, fp16, đóng băng thị giác | Có | ~37 GiB | Không | Không | Sát | Vừa | "PPO, critic tách riêng" |
| Bản sao train toàn bộ, fp16 | Có | ~41 GiB | Không | Không | Không | Vừa | "PPO, critic tách riêng" |
| Bản sao train toàn bộ, fp32 như VinePPO | Có | ~69 GiB | Không | Không | Không | Sát 80; vừa G4 | "PPO, critic tách riêng" |

Tôi không thấy tiền lệ critic bằng LoRA trong các nguồn đã đọc, và chưa tra riêng, nên hàng thứ hai là cách cài của đề tài, phải khai. Adapter thứ hai đi cùng cấu trúc `add_adapter("ref")` đã có, nhưng cần kiểm việc đổi adapter dưới gradient checkpointing, và lần nạp lại phải in `[nạp …]` như bài học 30/9.

### Clip nhiều khả năng vẫn không hoạt động ở μ = 2

Đây là điểm dễ bị thầy hỏi nhất. Với `num_iterations = 1` như ck500, tỉ số PPO luôn bằng 1 và `clip_ratio/region_mean` bằng 0 ở mọi dòng log đã kiểm [đo]. Nâng μ lên 2 vẫn chưa đủ: bước lẻ tỉ số bằng 1 theo cấu tạo, bước chẵn chỉ phản ánh một lần cập nhật, trong khi muốn chạm vùng clip ε = 0,2 thì |log ratio| phải vượt khoảng 0,18 đến 0,22. Log các lượt cùng lr 1e-5 cho KL trung bình mỗi token **so với S1** là 2e-5 đến 3e-5 ở bước 20 [đo], tương ứng RMS log ratio cỡ 0,006, và chỉ lên khoảng 0,12 đến 0,26 sau khoảng 260 bước cộng dồn [suy]. Vậy PPO μ = 2 ở lr này có thể gần với "actor-critic cập nhật hai lần trên mỗi lô", và phép so với ck500 đo chủ yếu mốc học được và số cập nhật, không đo clip [suy].

Hai hệ quả thực tế. Yêu cầu ở `report/326` là thấy `clip_ratio/region_mean > 0` khi probe khó đạt, và số 0 ở probe không phân biệt được clip lỗi với tỉ số chưa đủ lớn. Probe đang chạy còn bị cắt ở 39 phút, [suy] được khoảng 11 đến 12 bước và dòng `[xong]` chứa đỉnh VRAM có thể không in, nên VRAM phải đọc từ `memory.used`. Vì vậy nên thêm log `approx_kl` và phân vị |log ratio|, kiểm clip cơ học bằng `eps` rất nhỏ (cờ hiện chỉ đặt `epsilon_high`), và nếu muốn clip thật sự hoạt động thì chạy lượt độ nhạy riêng với lr hoặc μ lớn hơn, không thay lượt chính.

So với ck500, PPO hiện đổi cùng lúc: mốc học được, lợi thế theo token, chuẩn hoá theo lô thay theo nhóm, bỏ chia std nhóm, μ và gấp đôi số cập nhật. A2C (μ = 1) chỉ tách được μ, ba yếu tố còn lại vẫn đi cùng nên phải khai.

### Critic trên câu ngắn nên bắt đầu từ λ = 1 và huấn luyện trước

Bằng chứng trực tiếp cho thưởng độ đo câu ngắn trên VLM thì tôi không tìm thấy; mọi nguồn dưới đây là toán, tóm tắt hoặc tác vụ agent. VinePPO báo explained variance 0,7 đến 0,9 mà khi chọn bước tiếp theo critic vẫn gần mức ngẫu nhiên, nên **chỉ in EV sẽ không đủ**. UI-TARS-2 (preprint) ghi giá trị ước lượng của PPO thường tương quan âm với thưởng, huấn luyện trước critic cho thưởng cao hơn, rồi báo PPO hơn GRPO ở đánh giá sơ bộ ([arXiv](https://arxiv.org/abs/2509.02544)); bài này chỉ có đường cong train trên tác vụ dài nhiều lượt, nhưng là bài GUI duy nhất tôi biết trong mẫu đã khảo sát chạy cả hai và chọn PPO, nên là đòn phải có câu trả lời. [VC-PPO](https://arxiv.org/abs/2503.01491) (preprint) nêu GAE có suy giảm không truyền được thưởng cuối về token đầu; [RLOO](https://arxiv.org/abs/2402.14740) cho thấy λ thấp kém hơn; [DeepSeek-R1](https://arxiv.org/abs/2501.12948) (Nature 2025) cũng cho biết PPO λ = 1,0 gần GRPO còn λ = 0,95 kém rõ. [SCST](https://arxiv.org/abs/1612.00563) (CVPR 2017) lập luận đúng trên thưởng CIDEr rằng tránh được việc ước lượng thưởng như actor-critic phải làm.

Từ đó [suy] nên: lấy λ = 1,0 làm nhánh chính, 0,95 làm nhánh thử; huấn luyện trước critic trên mẫu S1 mà không đổi policy, vì V = 0 ban đầu làm những bước đầu gần REINFORCE chuẩn hoá theo lô; báo cả EV lẫn một phép xếp hạng trên cùng tiền tố. Có một điểm dễ bỏ sót: SPICE và CIDEr-D phụ thuộc câu chuẩn, nên critic không thấy câu chuẩn thì không thể biết tiền tố đang trúng hay trật. [Bahdanau et al.](https://arxiv.org/abs/1607.07086) có tiền lệ đưa câu chuẩn vào critic lúc train; đầu nhỏ không làm được, còn adapter hay bản sao riêng thì làm được. Đây là biến thể đáng thử khi đã có critic riêng.

### Colab mở thêm một bậc, nhưng phải giữ dtype

Trang chính thức ngày 3/11 ghi 100 đơn vị 9,99 USD, 500 đơn vị 49,99 USD và có `T4, A100, G4, H100, L4` ([Colab](https://colab.research.google.com/signup)). Google không công bố tốc độ đốt đơn vị trong phần tôi truy cập được; số dưới đây là đo cộng đồng 10/3/2026 ([McCormick](https://mccormickml.com/2024/04/23/colab-gpus-features-and-pricing/)) đối chiếu đo của kho 11/8/2026. Tài khoản có truy cập được A100 80 GB hay G4 không thì phải xem trong phiên đã đăng nhập.

| GPU | Đơn vị/giờ | USD/giờ | PPO đầu nhỏ μ = 2, 1.000 bước [suy] | PPO critic riêng [suy] |
|---|---:|---:|---|---|
| Kaggle T4 | miễn phí | 0 | ~41 h, 4 commit | Không vừa |
| Colab L4 | 1,71 (kho 1,54) | ~0,15 đến 0,17 | ~24 h, ~37 đơn vị | Chỉ bản đóng băng, sát giới hạn |
| Colab A100 40 GB | 5,40 (kho 5,3) | ~0,53 | ~10 h, ~54 đơn vị | 10 đến 25 h, 54 đến 135 đơn vị, 5 đến 14 USD, buộc đóng băng thị giác |
| Colab A100 80 GB | 7,52 | ~0,75 | | 75 đến 188 đơn vị, 8 đến 19 USD |
| Colab G4 ~96 GB | 8,71 | ~0,87 | | 87 đến 218 đơn vị, 9 đến 22 USD, giả định tốc độ như A100 |

Dải 10 đến 25 h ghép hai cách ước lượng lệch nhau: tính từ 36,4 s/bước A100 đã đo ở lượt CTG (G = 8) ra khoảng 10 h chưa kể critic, còn nhân đôi từ 5,63 h của lượt GRPO G = 4 rồi cộng critic ra 15 đến 25 h. Phải probe để thu hẹp. Thời gian thêm cho critic chưa đo; VinePPO chỉ mô tả thêm một forward và một forward-backward.

Kaggle vẫn là bậc đầu cho những gì vừa T4, nhưng ba nhánh PPO λ = 1, λ = 0,95 và A2C đã ăn khoảng 65 h phiên T4 cộng ~13 h chấm, gần trọn hạn mức một tuần của ba tài khoản [suy]. Đo CTG cho L4 chậm hơn A100 2,37× nên theo quy tắc 1,5× của dự án thì việc nghẽn GPU đi thẳng A100 khi đã rời T4. Bẫy là dtype: `grpo_luoi.py` tự chọn bf16 hoặc fp16, còn ck500 chạy T4 fp16, và dự án đã đo L4 bf16 lệch T4 fp16 ±1 bước. Vì vậy trên Colab nên **ép fp16 và chạy lại kiểm hoà**, hoặc khai đổi dtype.

Tôi đề xuất bốn bậc, từ rẻ đến đắt: (0) đọc probe, kiểm clip; (1) PPO đầu nhỏ λ = 1,0 và 0,95 trên T4, có huấn luyện trước đầu giá trị; (2) critic LoRA trên T4 nếu probe ≤ ~14 GiB, không thì L4; (3) một lần critic tách riêng khởi từ S1 trên A100 80 GB hoặc G4, nếu không có thì A100 40 GB với thị giác đóng băng. Ghi chú nghiên cứu đặt bậc 3 ở dạng tuỳ chọn; quan điểm của tôi là khi Colab đã được phép, với mức ước tính dưới 22 USD, nên chạy, vì đây là hàng duy nhất đóng được câu "critic của em không chuẩn" [suy]. Lý do đọc kết quả nằm ở đó: nếu PPO thua ck500 mà chỉ có bậc 1 thì chưa kết luận được thuật toán thua. VinePPO cho T4 thì không nên thử, vì chính bài ghi mỗi bước chậm hơn PPO 2 đến 5 lần do sinh thêm mẫu.

## ORPO: mức câu từ S1 chưa từng chạy, và hàng công bằng nhất là bản thích nghi

### Dự án mới có một lượt ORPO, khác hẳn cấu hình đang được hỏi

Lượt có điểm test duy nhất là MIN-DESC: tầng khai báo, nối tiếp từ S2, cặp dựng bằng heuristic với câu y hệt hai vế, không có phần thưởng, λ = 0,1, 800 update. Một hạt giống: 60,05 so với CE2-S2 59,42, **+0,63 [+0,16; +1,10]** p = 0,011, dưới MDE; so S1/101 +0,94 [−0,09; +2,05] p = 0,11 [đo] (`report/106`). Biến thể lấy vế âm từ lỗi của chính S2 dừng ở điều kiện dựng dữ liệu vì chỉ 3,3% bước đủ điều kiện, ngưỡng 25%. Lượt so với ck500: ck500 − MIN-DESC +0,60 [−0,52; +1,73] p = 0,30, chưa phân biệt được.

Vì vậy câu "ORPO đã chết" trong ghi chú dự án **mở rộng quá tầm** nếu áp cho ORPO mức câu [suy]. Cái gọi là "ORPO tầng câu bị bác" ở `report/151` không phải một lượt train mà là phép thay exec của S1 trên một lát tệp thô (`harness/phu_luc_c.py`), lại phụ thuộc kênh `<desc>` mà S1 không có. Số 66,67% (trong 1.950 bước đổi `<desc>` giữa MIN và GRPO, 1.300 bước câu giữ nguyên) đúng hơn nên đọc là ORPO cũ chưa bao giờ so hai câu khác nhau, không phải bằng chứng chống tầng câu. Bằng chứng bất lợi thật còn lại là gián tiếp: lượt GA-DPO (tên nội bộ, không phải phương pháp công bố) từ ck500 **không đạt tiêu chí có học nên không có số test**, và phép kiểm 200 cặp cho acc giữ riêng 0,46 ở cặp "cải thiện", 0,76 ở cặp "giữ", log-p chosen giảm −0,261 → −0,457 trên câu nhắc giữ riêng [đo, chẩn đoán học] (`report/314_KET_QUA_GADPO_13_10.md`). RAFT từ ck500 cũng thấp hơn ck500, −0,43 [−0,82; −0,04]. Cả hai đo trên ck500, không phải S1, và không được viết "GA-DPO thua ck500".

### Bài gốc không quy định cách đổi điểm liên tục thành cặp

[ORPO](https://aclanthology.org/2024.emnlp-main.626/) (EMNLP 2024) định nghĩa L = E[L_SFT + λ·L_OR], với L_OR = −log σ(log(odds(y_w|x)/odds(y_l|x))), odds(y|x) = P/(1−P), và log P là **trung bình log-xác suất theo token** ([arXiv](https://arxiv.org/abs/2403.07691)). Bài dùng λ từ 0,1 đến 0,25 cho kết quả chính; Phụ lục E cảnh báo λ = 1,0 làm cả hai log-p cùng giảm khi biên rộng ra, nhưng cũng nói λ nhỏ hơn không phải lúc nào cũng hơn. Cặp lấy sẵn từ tập ngoại tuyến; bài chạy thẳng từ pretrained, còn DPO và PPO trong thí nghiệm chạy từ SFT. Bài báo cáo thắng SFT rõ theo win rate GPT-4, nhưng trong bảng của [KTO](https://proceedings.mlr.press/v235/ethayarajh24a.html) (ICML 2024, bài đề xuất phương pháp khác) ORPO thấp hơn SFT ở MMLU, GSM8k, HumanEval, chỉ cao hơn ở BBH ([arXiv](https://arxiv.org/abs/2402.01306)). Không nên chép câu văn của bài rằng mẫu số 1−P khuếch đại gradient khi P thấp, vì công thức cho thấy ngược lại [suy].

Khuôn đổi điểm thành cặp rõ nhất là [Bridging](https://arxiv.org/abs/2506.21495) (preprint, DPO, không phải ORPO): lấy n mẫu, xếp theo điểm, dùng tốt nhất và kém nhất, câu nhắc không tạo được cặp thì bỏ, tương tự lợi thế bằng 0 của GRPO. Trên AlpacaEval với GPT-4-1106, DPO ngoại tuyến 53,2, bán trực tuyến s = 10 81,6, trực tuyến 83,1, GRPO 75,2; nhưng ArenaHard với GPT-4o cho 38,2, 43,0, 50,4 và GRPO 54,3, tức bộ chấm đảo được thứ tự. Toán thì gần ngang: Math500 53,7 ngoại tuyến, 58,7 trực tuyến, 58,1 GRPO. Trực tuyến không luôn thắng: [Tülu 3](https://arxiv.org/abs/2411.15124) (chưa kiểm venue) thấy online DPO gần như không tăng trên toán, và [RPO](https://arxiv.org/abs/2502.00203) (chưa kiểm venue) báo cải thiện rất ít với mô hình thưởng học được; SPICE thì không học, nhưng vẫn chơi được độ đo ([Liu et al.](https://arxiv.org/abs/1612.00370) báo PG-SPICE sinh câu sai ngữ pháp, lặp cụm). [Razin et al.](https://arxiv.org/abs/2410.08847) (ICLR 2025) còn chứng minh log-xác suất câu ưu tiên có thể giảm khi hai vế quá giống, đúng rủi ro của mẫu chỉ khác một từ ở đây. Tôi **không tìm thấy** biến thể ORPO trực tuyến được công nhận, phép so ORPO với GRPO có số, hay bằng chứng so sánh về ngưỡng chênh, xử lý hoà, số cặp mỗi câu nhắc trên thưởng kiểu SPICE. Đây là không tìm thấy, không phải chứng minh không có.

### Công cụ: sửa script DPO đã có, vì TRL ORPO không có ảnh

| Công cụ | ORPO | Với ảnh | Kết luận |
|---|---|---|---|
| LLaMA-Factory | `pref_loss: orpo` ([mã](https://github.com/hiyouga/LLaMA-Factory/blob/main/src/llamafactory/hparams/finetuning_args.py)) | Dự án đã chạy ở pin `c4e09c7cbe18…`, ~21 s/bước A100 [đo]; README không có câu nối hai thứ | Có sẵn nhưng khác vòng lặp, dtype và TRL; `pyproject` ghi `trl<=0.24.0` |
| TRL `ORPOTrainer` | Có, ở experimental | **Không có `pixel_values`** trong [mã v0.29.1](https://github.com/huggingface/trl/blob/v0.29.1/trl/experimental/orpo/orpo_trainer.py) | Không dùng |
| TRL `DPOTrainer`, `OnlineDPOTrainer` | Không có odds ratio | [DPO](https://github.com/huggingface/trl/blob/v0.29.1/trl/trainer/dpo_trainer.py) có ví dụ Qwen2.5-VL; [online](https://github.com/huggingface/trl/blob/v0.29.1/trl/experimental/online_dpo/online_dpo_trainer.py) ghi cứng `num_generations = 2` | Không khớp G = 8 |
| Axolotl | `rl: orpo` | Tài liệu ghi Limitations không hỗ trợ ORPO với VLM, trong khi DPO, KTO, GRPO thì có ([RLHF](https://docs.axolotl.ai/docs/rlhf.html)) | Loại |
| Unsloth | Có notebook văn bản ([tài liệu](https://unsloth.ai/docs/basics/reasoning-grpo-and-rl/reinforcement-learning-dpo-orpo-and-kto)) | Không thấy bằng chứng | Loại |

Tôi khuyên đường **sửa `_scripts/314/ds_gadpo314/ga_dpo.py`**: đã có vision và NLL, bỏ tham chiếu, đổi số hạng DPO thành odds ratio, thêm fp16 cho T4 (bản gần nhất ở `_scripts/314/ga313/ga_dpo.py:221` còn `assert` đòi L4 hoặc A100). Như vậy ORPO đi cùng đường dữ liệu và chấm với các lượt DPO khác. Hai chi tiết kỹ thuật: phải dùng `log1mexp` như TRL đã sửa lỗi triệt tiêu số ([release](https://github.com/huggingface/trl/releases)), đừng viết `log(1−exp(x))` trần, và tính phần này ở float32 khi train fp16; đồng thời in mỗi bước λ, số cặp, số câu nhắc bỏ vì hoà, log-p hai vế, log OR, acc. Chi phí [suy]: ngoại tuyến sinh 8 mẫu 2,7 đến 5,3 h cộng train ~3,7 h trên T4; trực tuyến ~65 s/bước, ~9 h T4 hoặc ~1,5 h A100. Chưa đo, và không nên viết "ORPO rẻ hơn" trước khi đo, vì ck500 dùng adapter tham chiếu nên phần tiết kiệm nhỏ hơn trường hợp hai mô hình của bài gốc.

### Ba hàng, mỗi hàng một song sinh λ = 0

Thiết kế dưới đây là đề xuất, chưa có số. Hai cách chọn chosen trả lời hai câu hỏi khác nhau, nên nên tách.

| Mã | Chosen | Rejected | Lấy mẫu | Song sinh λ = 0 | Trả lời câu gì |
|---|---|---|---|---|---|
| ORPO-G | Câu chuẩn | Mẫu SPICE thấp nhất của S1 | Ngoại tuyến | SFT tiếp | Tương phản có hơn SFT thuần không; gần bài gốc nhất, nhưng SPICE chỉ chọn rejected |
| ORPO-S | Mẫu SPICE cao nhất | Mẫu SPICE thấp nhất | Ngoại tuyến | RFT một vòng từ S1 | Đối chiếu ORPO với DPO ngoại tuyến trên cùng cặp |
| ORPO-O | Mẫu cao nhất | Mẫu thấp nhất | Mỗi bước từ chính sách hiện tại, G = 8 | Online RFT | **Phép so gần nhất với ck500: cùng tín hiệu, cùng ngân sách sinh. Bản thích nghi của đề tài** |

Nếu chỉ chạy được một lượt thì chọn ORPO-O; hai lượt thì thêm ORPO-G. Điều kiện giữ như ck500: S1 đã hoà + LoRA mới, cùng 1.000 câu nhắc, G = 8, nhiệt độ 1, hạt 101, lr 1e-5, 500 bước, chấm điểm lưu cuối. Thưởng xếp cặp phải trùng thưởng của ck500: r = SPICE − 0,02·max(0, số từ câu − số từ câu chuẩn − 3), câu không có nội dung tính 0, theo đầu tệp `harness/grpo_luoi.py`. Quy tắc dựng cặp: một cặp mỗi câu nhắc, hoà trong nhóm lấy ngẫu nhiên theo hạt cố định, toàn nhóm bằng điểm hoặc hai câu trùng sau chuẩn hoá thì bỏ và báo tỉ lệ bỏ; không đặt ngưỡng ở lượt chính, ngưỡng chênh ≥ 0,3 chỉ làm độ nhạy. Thống kê trên 8 mẫu S1 ở tập kiểm định (không trích số, `runs/c1/exec8/`) cho thấy ở SPICE, thứ cần xử là hoà, vì điểm thưa nên ngưỡng nhỏ gần như không đổi tập cặp.

Lấy λ = 0,1 làm lượt chính, không quét trên test, λ = 1,0 làm độ nhạy một lần. Lưu ý λ không chuyển thẳng từ bài sang được: câu của dự án ngắn nên P cao, log-p/token trước train ở cặp ck500 là −0,26 và −0,37 (`report/314`), và hệ số 1/(1−P) lớn hơn ở bài gốc, nên [suy] cùng λ = 0,1 mạnh hơn khoảng 2 đến 3 lần, ước lượng tại điểm đầu.

Bốn điều phải khai, kể cả khi số đẹp. Thứ nhất, chạy ORPO sau S1 đã khác thiết kế gốc của bài vốn chạy từ pretrained, và ORPO-O phải viết "ORPO với cặp lấy mẫu theo chính sách (bản thích nghi)", không viết "ORPO trực tuyến" như phương pháp đã có. Thứ hai, ngân sách sinh bằng nhau nhưng ngân sách gradient thì không: GRPO dùng cả 8 mẫu, ORPO dùng 2. Thứ ba, ORPO không có phanh KL của ck500, và khi chosen là mẫu của chính mô hình thì NLL không còn neo vào câu chuẩn, có thể tự củng cố phong cách đang lệch; phải log KL so S1 (chỉ để theo dõi) và độ dài câu. Thứ tư, nhánh `rft` hiện có giữ β = 0,04 và `loss_type="dapo"`, nên chưa phải song sinh λ = 0 đúng nghĩa của ORPO-O không tham chiếu [suy]; phải chạy thêm bản β = 0 hoặc khai lệch. Trước khi đọc kết quả phải chạy phép kiểm học thuộc trên ~200 cặp và đặt trước tiêu chí "có học"; không đạt thì viết "không học", không có số test, không viết "thua". Dự đoán [suy] là cặp mẫu với mẫu khó học, do mẫu trội thường thắng vì dao động lấy mẫu với một câu chuẩn duy nhất; đây là giả thuyết để kiểm.

## RL cổ điển: mỗi hàng phải thay đúng một cơ chế

### Bảy nhánh đã có mã phần lớn chỉ được gọi "kiểu"

`harness/grpo_codien.py` chỉ đổi trọng số A từng câu mẫu trong khung ck500, giữ KL về S1, μ = 1. `vanilla` (A = r) và `mad` là sát tên nhất, dù `mad` phải đối chiếu công thức DGPO trong [MathForge](https://arxiv.org/abs/2601.20614) trước khi gọi tên. `rft` là online RFT; `cem` chọn elite trên câu chứ không phải CEM trên tham số; `awr`, `raml` phải viết "kiểu AWR", "kiểu RAML" vì không có V, không replay, mẫu lấy từ chính sách; `rank` chỉ là fitness shaping, không phải ES. Nhóm này trả lời "đổi trọng số mẫu có đáng không", chưa trả lời "thuật toán cổ điển X có tốt không". Riêng `rft`, `cem`, `rank` nên sửa cách xử lý hoà trước khi chạy, vì SPICE hoà nhiều mà thứ tự hiện lấy theo vị trí sinh mẫu. Thang của A khác GRPO cũng làm tỉ trọng so với β·KL khác đi, nên kết quả lẫn cả yếu tố cỡ bước [suy].

### Số hành động không phải trở ngại của DQN, thống kê mới là trở ngại

`report/329` §3 ghi logits của S1 không phải giá trị Q nên thang đo lệch; câu này **cần sửa**. [Guo et al.](https://arxiv.org/abs/2106.07704) (Findings of EMNLP 2022 theo OpenAlex) đặt thẳng Q ≡ logit và chạy soft Q-learning. [Schulman, Chen, Abbeel](https://arxiv.org/abs/1704.06440) (preprint) chứng minh trong RL điều chuẩn entropy, soft Q-learning tương đương chính xác một policy gradient. [PCL](https://arxiv.org/abs/1702.08892) (NIPS 2017) thống nhất on-policy và off-policy. Trở ngại thật được [Bahdanau et al.](https://arxiv.org/abs/1607.07086) mô tả: chỉ token được lấy mẫu mới có nhãn, token hiếm bị đánh giá quá cao, thưởng chỉ ở bước cuối quá thưa cho critic, phải dùng mạng đích và phạt phương sai.

Phép tính sau là của tôi [suy], cần kiểm lại trước khi trích. Đặt π₀ = S1 và mục tiêu E[R] − αKL(π‖π₀), nghiệm là π*(y) ∝ π₀(y)exp(R(y)/α), và ở mức token Q/α = f_θ − f_S1 tới một hằng số, nên lúc bắt đầu Q = 0, V = 0 và **không còn lệch thang đo**. Dự án đã chạy forward adapter tham chiếu để tính KL nên có thể không tốn thêm. Nhưng nếu lấy trọn câu và cập nhật on-policy, thay V(s₀) bằng trung bình nhóm thì gradient quy về PG có mốc trung bình nhóm, không chia std, cộng KL theo câu. Tức chạy bản này rồi gọi "họ Q-learning" **không thêm thông tin**, và thầy biết RL sẽ nhận ra. Phần khác thật so với GRPO chỉ ở dữ liệu off-policy và V(s) theo tiền tố, nên hàng này phải dùng kho mẫu cũ. Đắt là đầu Q riêng: 2048 × 151.936 ≈ 311 triệu tham số, gấp ~21 lần LoRA, ~593 MiB fp16 mỗi đầu; SAC rời rạc cần bốn đầu, ~2,4 GiB, còn dùng chung logits thì SAC trở thành soft Q [suy].

### TRPO: vector rẻ, đồ thị bậc hai mới đắt

CG trên 15 triệu tham số chỉ tốn dưới 0,3 GiB [suy], nên bộ nhớ vector không chặn. [TRPO](https://arxiv.org/abs/1502.05477) (ICML 2015) cần k = 10 vòng CG và lấy mẫu con 10% cho Fisher, nhưng dự án chỉ có vài chục câu mỗi bước nên không giảm sâu được. Ước lượng rất thô: 500 bước từ ~20,6 h lên 40 đến 60 h T4, hoặc 25 đến 30 h với lô con một phần tư [suy]; A100 nhanh khoảng 4× theo đo CTG, nên hàng này hợp với Colab. Rủi ro là `create_graph=True` qua checkpoint trên GPU đã ở 12,71 GiB, và dưới fp16 KL rất nhỏ dễ chạm vùng số học kém. Có hai đường bậc nhất: FVP sai phân giữ được tên TRPO nếu còn CG, KL cứng, line search; Fisher hạng thấp thì phải gọi "xấp xỉ NPG hạng thấp", gần ý [ISOPO](https://arxiv.org/abs/2512.23353) (preprint). Riêng LoRA khởi tạo B = 0 thì score theo A bằng 0, nên Fisher có hàng và cột 0, phải có damping ở bước đầu [suy]. RL4LMs nêu có TRPO trong thư viện nhưng tôi không thấy bài nào báo số TRPO trên mô hình ngôn ngữ, nên hàng này không có mốc để đối chiếu cài đặt.

### Quyết định từng thuật toán

| Thuật toán | Venue đã kiểm | Quyết định | Tên chỉ đúng khi |
|---|---|---|---|
| REINFORCE không mốc | [RLOO](https://aclanthology.org/2024.acl-long.662) dùng làm mốc (ACL 2024) | **Chạy**, mã xong | Khai giữ KL hay không |
| SCST | [CVPR 2017](https://arxiv.org/abs/1612.00563) | **Chạy CIDEr-D**, SPICE đã có số | "mốc greedy kiểu SCST trong khung GRPO" |
| A2C | [A3C, ICML 2016](https://proceedings.mlr.press/v48/mniha16.html) | **Chạy**, mã xong | Critic thật; đầu nhỏ thì khai. A3C chỉ khác cách chạy song song |
| PPO | [arXiv 2017](https://arxiv.org/abs/1707.06347) không venue | **Chạy**, nhiều bậc critic | `approx_kl`, clip được báo; gọi đúng loại critic |
| Soft Q (PCL, off-policy) | [NIPS 2017](https://arxiv.org/abs/1702.08892) | **Chạy nhỏ trước**: selftest CPU, probe T4 20 bước (chỉ VRAM, không NaN), rồi 125 bước ~5,2 h | Có dữ liệu off-policy; khai là soft Q, không phải DQN |
| TRPO / NPG | [ICML 2015](https://proceedings.mlr.press/v37/schulman15.html) / [NIPS 2001](https://proceedings.neurips.cc/paper/2001/hash/4b86abe48d358ecf194c56c69108433e-Abstract.html) | **Probe trên Colab**; không qua thì thay bằng ES | KL cứng, CG, line search |
| ES | [Qiu et al.](https://arxiv.org/abs/2509.24372), PDF in ICML 2026, tự báo | Dự phòng cho TRPO | Nhiễu tham số, không backprop |
| MIXER | [Bài gốc](https://arxiv.org/abs/1511.06732) | Có thể bỏ: curriculum để khởi động mô hình chưa có chính sách tốt, Rennie cho thấy bỏ được; bản rút gọn trùng A2C [suy] | Chỉ khi có curriculum |
| MRT · softmax PG · RAML | [ACL 2016](https://aclanthology.org/P16-1159/) · [NIPS 2017](https://arxiv.org/abs/1709.09346) · [NIPS 2016](https://arxiv.org/abs/1609.00150) | Sau sáu hàng chính; softmax PG cần thưởng theo tiền tố nên hợp CIDEr-D, đắt với SPICE [suy] | "kiểu RAML" nếu mẫu từ chính sách |
| ILQL | [ICLR 2023](https://arxiv.org/abs/2206.11871) | Hàng thứ bảy, nếu còn ngân sách; đổi cách suy luận nên không còn một adapter duy nhất [suy] | Giữ V, Q, mạng đích |
| Quark · SeqGAN | [NeurIPS 2022](https://arxiv.org/abs/2205.13636) · [AAAI 2017](https://arxiv.org/abs/1609.05473) | Đọc như phép đo về thưởng hoặc câu nhắc, không phải thuật toán. [Caccia et al.](https://arxiv.org/abs/1811.02549) (ICLR 2020) cho MLE vượt GAN văn bản trên toàn dải | Thưởng SPICE thì không còn là SeqGAN |
| DQN, Double DQN, Rainbow | Chưa xác nhận venue ở trang nguồn trong lượt này | Không chạy riêng; soft Q đại diện | Cần max cứng, replay, mạng đích, ε-greedy |
| SAC rời rạc | [SAC, ICML 2018](https://proceedings.mlr.press/v80/haarnoja18b/haarnoja18b.pdf); bản rời rạc [preprint](https://arxiv.org/abs/1910.07207) | Không chạy; không thấy tiền lệ trên LLM | |
| DDPG, TD3, DPG | [ICLR 2016 qua arXiv](https://arxiv.org/abs/1509.02971), [ICML 2018](https://proceedings.mlr.press/v80/fujimoto18a.html), [ICML 2014](https://proceedings.mlr.press/v32/silver14.html) | Không áp dụng | Chỉ khi hành động là vector ẩn, như [Gu et al.](https://aclanthology.org/D17-1210/) (EMNLP 2017, chỉ đọc tóm tắt) |
| GAIL | [NIPS 2016](https://proceedings.neurips.cc/paper/2016/hash/cc7e2b878868cbae992d1fb743995d8f-Abstract.html) | Không chạy: bỏ mất SPICE | |

SFT tiếp là nhánh so sánh, không tính vào sáu hàng. Lý do DDPG không áp dụng cần viết chính xác hơn "vì hành động liên tục": DPG dùng ∇ₐQ(s,a)·∇θμ(s), token không có đạo hàm đó và SPICE không khả vi, nên sai số của critic học được sẽ trở thành toàn bộ tín hiệu. Nới bằng Gumbel-softmax buộc mô hình đã SFT đọc hỗn hợp nhúng chưa từng thấy, tên thuật toán không còn đúng [suy].

### Tiền lệ cho thấy mốc quan trọng hơn tên thuật toán

Trong [Rennie et al.](https://arxiv.org/abs/1612.00563), Att2all, bốn hạt: REINFORCE 110,4 ±0,5, mốc học được 113,2 ±0,2, SCST 113,8 ±0,3; XE 90,9 so MIXER 104,9 và SCST 106,3 ở FC-2K. Mức tăng do RL lớn hơn hẳn chênh giữa các thuật toán RL. [Bahdanau et al.](https://arxiv.org/abs/1607.07086) cho thứ tự đổi theo tác vụ: IWSLT REINFORCE có critic 22,24 hơn actor-critic 21,66, WMT14 thì AC+LL 30,85 hơn RF-C+LL 29,83. Back to Basics báo trên TL;DR RLOO k = 4 77,9, REINFORCE mốc 70,7, PPO 67,6, DPO 66,6, nhưng [REBEL](https://arxiv.org/abs/2404.16767) chép PPO 77,6 ở dòng khác, nên biên PPO phụ thuộc cài đặt; đừng trích câu mở đầu "3,2% đến 20,3%" vì tính lại từ bảng lệch. [RL4LMs](https://arxiv.org/abs/2210.01241) (ICLR 2023): người chấm xếp Supervised+NLPO > Supervised ≥ Supervised+PPO > NLPO ≥ PPO, và Supervised thắng Supervised+PPO ở 2/5 tác vụ dù metric tự động nói ngược. Trên Countdown với Qwen2.5-3B, Qiu tự báo PPO 20,1, GRPO(8) 30,9, ES 60,5; miền xa và là số của tác giả ES. [ILQL](https://arxiv.org/abs/2206.11871) có bảng so offline RL trên ngôn ngữ, Visual Dialogue: ILQL −5,57, single-step −5,91, DT −6,70, CQL −7,32, fine-tuning −10,85. Khảo sát khung các họ này cho văn bản có [Keneshloo et al.](https://arxiv.org/abs/1805.09461) (IEEE TNNLS 2020); nhưng tôi không thấy khảo sát nào đặt DQN, SAC, TRPO cạnh nhau cho sinh câu có số. Rà soát của tôi không hệ thống, nên không được viết "chưa có ai".

## Trả lời thầy: nói rõ phần đã đo và phần chưa đo

Các câu dưới đây dùng được hôm nay; khi có số thì thay. Thầy là tiến sĩ AI nên nên đưa cơ chế trước, kèm tên bài khi được hỏi tiếp.

**"Sao không dùng PPO?"**

> "Tụi em chọn GRPO lúc đầu vì không cần mô hình giá trị, có tiền lệ và rẻ, chứ không phải vì đã thắng PPO; văn liệu cũng không cho căn cứ nói GRPO hơn PPO, chênh lệch đổi dấu theo bài và UI-TARS-2 trên GUI còn chọn PPO, dù đó là preprint chỉ có đường cong train. PPOTrainer của TRL không truyền ảnh và đã bị xoá ở bản 1.13, OpenRLHF cấm critic với VLM, nên em tự cài trên GRPOTrainer. Mã xong, đang probe, chưa có số. Bản hiện tại chỉ là đầu giá trị nhỏ tách gradient, em gọi là bản rút gọn, và thua cũng chưa kết luận được PPO kém. Vì vậy em sẽ chạy thêm critic LoRA và một critic tách riêng trên Colab, có huấn luyện trước, báo explained variance và phép xếp hạng. Còn GRPO trong ck500 với μ = 1 thì clip không hoạt động, thực chất là policy gradient có mốc trung bình nhóm, với gộp mất mát theo token kiểu DAPO."

**"PPO của em có clip thật không?"**

> "Ở lr 1e-5 và μ = 2, em ước lượng tỉ số gần 1 nên clip gần như không hoạt động. Em sẽ log approx_kl và phân vị log ratio. Nếu đúng vậy, phép so này đo mốc học được và số cập nhật, không đo clip; muốn đo clip em chạy lượt độ nhạy riêng."

**"Sao không dùng ORPO?"**

> "Đã dùng một lần ở tầng khai báo, từ S2, cặp heuristic, không có thưởng: 60,05 so 59,42 của nhánh SFT cùng số bước, +0,63 [+0,16; +1,10], dưới MDE, một hạt, so S1 không có ý nghĩa. ORPO mức câu từ S1 chấm SPICE thì chưa chạy, nên em không nói ORPO kém. ORPO được thiết kế cho cặp có sẵn, bài gốc không nói cách đổi điểm liên tục thành cặp và em không tìm thấy bản trực tuyến được công nhận. Em sẽ chạy ba hàng với song sinh λ = 0; hàng sát ck500 nhất lấy cặp tốt nhất, kém nhất mỗi bước theo khuôn Bridging, và em ghi rõ đó là bản thích nghi của đề tài. Không học thì em báo không học."

**"Sao không thử thuật toán cổ điển?"**

> "Em đang thử theo nguyên tắc mỗi hàng thay đúng một cơ chế: REINFORCE không mốc, mốc greedy SCST, A2C, PPO, soft Q off-policy, TRPO nếu qua probe, thiếu thì ES. Một hàng đã có số là mốc greedy kiểu SCST trong khung GRPO, 60,54, không phân biệt được với ck500. DDPG, TD3 cần đạo hàm của Q theo hành động liên tục, token và SPICE không có, nới bằng Gumbel thì không còn là thuật toán đó. DQN em đại diện bằng soft Q với logits làm Q; on-policy trên trọn câu thì về lý thuyết nó gần trùng policy gradient, theo Schulman và phép tính em sẽ kiểm lại, nên em phải cho nó dữ liệu off-policy mới thành hàng riêng. SAC rời rạc dùng chung logits thì quy về soft Q, đầu Q riêng thì gấp khoảng 21 lần LoRA, và em chưa thấy tiền lệ trên mô hình ngôn ngữ."

**"Vậy GRPO + SPICE có phải lựa chọn hay nhất không?"**

> "Em chưa đủ căn cứ để nói vậy. Ck500 hơn S1 +1,55 [+0,80; +2,33], dưới MDE trên tập kiểm chính, và nhánh ghép ngẫu nhiên điểm SPICE cho bằng đúng S1, nên mức tăng gắn với tín hiệu thưởng. Nhưng trong lưới một hạt giống, bốn lượt khác cách dưới 1 điểm, không phép so nào với ck500 loại 0, hai hạt ck500 chênh 0,72, và SFT tiếp chưa chấm. Muốn giải thích vì sao thì còn phải đợi SFT tiếp và PPO."

Những câu không nên nói: "ORPO đã chết" mà không kèm tầng; "GA-DPO thua ck500"; "GRPO hơn PPO"; "bỏ critic làm kết quả tốt hơn"; "nhờ clip"; gọi GRPO + SPICE là "tốt nhất" từ một hạt; viết "SCST", "DAPO", "Dr. GRPO" trần cho các lượt chỉ là một phần phương pháp; bất kỳ số val nào; so thẳng 60,65 với số của bài khác.

Về venue, các chi tiết sau tôi chưa xác nhận ở nguồn gốc nên chưa được viết như sự thật trong luận văn: NeurIPS 2022 của InstructGPT, ICLR 2017 của Bahdanau, CVPR 2017 của SCST (lấy qua ghi chú), Findings EMNLP 2022 của Guo (qua OpenAlex), ICML 2026 của Qiu (chỉ trong PDF), cùng năm và nơi đăng của DQN, Double DQN, Rainbow, IQL, ACKTR. Số VinePPO trích từ hình và số online so ngoại tuyến của OAIF chưa đối chiếu nên tôi không dùng ở đây.

## Kết luận

Ba điều làm đổi cách trình với thầy. Thứ nhất, câu hỏi "sao không dùng PPO" hoá ra nhỏ hơn câu hỏi "PPO nào": từ đầu giá trị 1 triệu tham số đến bản sao 3,75 tỉ tham số là các phép so khác nhau, và ở lr hiện tại có thể không phép nào kiểm tra clip, nên mỗi số PPO chỉ có nghĩa khi đi kèm tên critic, chất lượng critic đo được và `approx_kl`. Thứ hai, nhiều họ tưởng xa nhau lại chung một đích: GRPO không chia std có KL, soft Q on-policy, RAML và KL-control cùng nhắm π₀ exp(R/α) [suy]. Nếu lưới ra một dải hẹp, đó có thể là hệ quả của cấu trúc này chứ không phải thiếu sức mạnh thống kê đơn thuần, và đó là phần giải thích theo cơ chế mà thầy đang đòi; các hàng khác thật về thông tin là hàng dùng dữ liệu off-policy, critic theo tiền tố, hoặc mục tiêu tương phản.

Thứ tự rẻ nhất để có câu trả lời: đọc probe và kiểm clip, chấm test SFT tiếp, chạy PPO đầu nhỏ cùng A2C, dựng critic LoRA và một critic riêng trên Colab với fp16, rồi ORPO-O và ORPO-G có tiêu chí học đặt trước, sau cùng là probe soft Q và TRPO. Có hai điều nên hỏi thầy ngay trong buổi trình, vì chúng đổi ngân sách: thầy có chấp nhận critic LoRA như một bước trung gian hay đòi critic tách riêng, và thầy có cần một hàng mang đúng tên DQN (max cứng, replay, ε-greedy) hay soft Q là đủ.
