# Công cụ train PPO cho Qwen2.5-VL-3B (LoRA) với thưởng là độ đo câu — kiểm ngày 3/11/2026

Nhãn: **[nguồn]** là đã mở mã hoặc bài gốc · **[đo-kho]** là số đo của dự án · **[suy]** là suy luận hoặc ước lượng của tôi, chưa chạy. Không chạy GPU, không đẩy gì lên Kaggle. Phiên bản đã đọc: TRL tag `v0.29.1` và `v1.17.1` · veRL `184687b` (0.10.0.dev) · OpenRLHF `2649449` (0.11.3) · SkyRL `bd35ce1` · Molt `a2f3fe9` · AReaL nhánh main 3/11 · transformers nhánh main 3/11.

**Kết luận chung:** không có công cụ nào đang được bảo trì mà có PPO + critic nhìn được ảnh + Qwen2.5-VL + chạy được trên 16–22 GB theo đường đã kiểm chứng. Khuyến nghị: **giữ TRL 0.29.1, tiếp tục lớp con của `GRPOTrainer`** (`harness/grpo_ppo.py`), thêm critic bằng adapter LoRA thứ hai và huấn luyện trước critic. Nếu cần chặn câu hỏi "critic quá nhỏ", chạy thêm **một** nhánh critic tách riêng trên A100 80 GB hoặc G4. Chi tiết ở mục cuối.

## 1. TRL: PPOTrainer bị chuyển, gỡ khi nào, dùng được với VLM không

### Takeaway
PPOTrainer chuyển sang `trl.experimental.ppo` ở v0.26.0, gỡ đường import cũ ở v0.29.0, **xoá hẳn ở v1.13.0**. Bản trong v0.29.1 vẫn import được nhưng **không dùng được cho Qwen2.5-VL**: không có đường truyền ảnh, không có hàm thưởng tuỳ ý, không có lớp value cho kiến trúc này.

### Cited Findings
- **Mốc phiên bản.** v0.26.0: "Move PPOTrainer to trl.experimental.ppo" (#4482) — [release v0.26.0](https://github.com/huggingface/trl/releases/tag/v0.26.0). v0.29.0: "Remove deprecated PPO after moved to experimental" (#5051) — [release v0.29.0](https://github.com/huggingface/trl/releases/tag/v0.29.0). v1.13.0: "⚠️ PPO is removed": `PPOTrainer`, `PPOConfig`, `modeling_value_head.py` cùng test, tài liệu, ví dụ — [release v1.13.0](https://github.com/huggingface/trl/releases/tag/v1.13.0).
- **Kiểm bằng cây mã theo tag [nguồn]:** `trl/experimental/ppo/` còn ở v0.26.0 đến v1.12.0 (ngày tag 26/8/2026), không còn ở v1.13.0 (9/9/2026) đến v1.17.1 (30/10/2026, bản mới nhất trên PyPI hôm nay). Tệp `trl/trainer/ppo_trainer.py` (đường cũ) còn ở v0.28.0, mất ở v0.29.0. `trl/__init__.py` của v0.29.1 không có dòng nào chứa `ppo`. — [cây v0.29.1](https://github.com/huggingface/trl/tree/v0.29.1/trl/experimental/ppo) · [commit xoá 700b845c, 4/9/2026](https://github.com/huggingface/trl/pull/7020)
- **Lý do gỡ, nguyên văn của người bảo trì:** "It's unmaintained. No feature work in over a year"; "PPO still takes tokenized `input_ids`"; "We record basically no usage"; "a magnet for automated bug hunters" — [PR #7020](https://github.com/huggingface/trl/pull/7020).
- **Mâu thuẫn nguồn:** PR #7020 và release v1.13.0 viết `from trl import PPOTrainer` "already stopped working in v1.10"; cây mã cho thấy đường đó mất từ v0.29.0 — [release v1.13.0](https://github.com/huggingface/trl/releases/tag/v1.13.0), [cây v0.29.0](https://github.com/huggingface/trl/tree/v0.29.0/trl/trainer). Tin mã.
- **Vì sao không dùng cho VLM (v0.29.1, [nguồn]):** đầu vào là `queries = data["input_ids"]`; `generate()` chỉ truyền `input_ids` và `attention_mask`; `forward()` tự tính `position_ids = attention_mask.cumsum(1) - attention_mask.long()` rồi gọi model chỉ với `input_ids, attention_mask, position_ids`. Không có `pixel_values`, `image_grid_thw`. Tài liệu trang PPO không nhắc đến đa phương thức — [ppo_trainer.py](https://github.com/huggingface/trl/blob/v0.29.1/trl/experimental/ppo/ppo_trainer.py) · [ppo_trainer.md](https://github.com/huggingface/trl/blob/v0.29.1/docs/source/ppo_trainer.md)
- **Thưởng:** chữ ký `__init__` đòi `reward_model: nn.Module`, điểm lấy qua `get_reward(reward_model, ...)`; không có tham số hàm thưởng Python — [ppo_trainer.py](https://github.com/huggingface/trl/blob/v0.29.1/trl/experimental/ppo/ppo_trainer.py)
- **Thiết kế critic trong trainer:** `PolicyAndValueWrapper` giữ hai mô hình, `critic_backbone = getattr(value_model, value_model.base_model_prefix)`, giá trị là `value_model.score(output.hidden_states[-1])`; ví dụ dựng `value_model = AutoModelForSequenceClassification.from_pretrained(..., num_labels=1)` ⇒ critic đầy đủ, tách riêng — [ppo_trainer.py](https://github.com/huggingface/trl/blob/v0.29.1/trl/experimental/ppo/ppo_trainer.py) · [examples/scripts/ppo/ppo.py](https://github.com/huggingface/trl/blob/v0.29.1/examples/scripts/ppo/ppo.py)
- **Không có lớp cho kiến trúc này:** bảng `MODEL_FOR_SEQUENCE_CLASSIFICATION` và `MODEL_FOR_TOKEN_CLASSIFICATION` của transformers có `qwen2`, `qwen2_moe`, **không có `qwen2_5_vl`**; `qwen2_5_vl` chỉ nằm ở bảng image-text-to-text — [modeling_auto.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/auto/modeling_auto.py)
- **Lớp cũ `AutoModelForCausalLMWithValueHead`:** đầu `ValueHead` là dropout + `nn.Linear(hidden_size, 1)` đặt trên `hidden_states[-1]` của chính mô hình, tôi không thấy `detach` trong tệp ⇒ chung backbone, gradient giá trị đi vào backbone — [modeling_value_head.py](https://github.com/huggingface/trl/blob/v0.29.1/trl/experimental/ppo/modeling_value_head.py)
- **Lỗi đã biết không có trong v0.29.1** (kiểm bằng `git merge-base`): sửa thiếu `gradient_checkpointing_enable/disable` của `PolicyAndValueWrapper` (#5245, vào v1.0.0) — [release v1.0.0](https://github.com/huggingface/trl/releases/tag/v1.0.0); entropy log âm do tính cả token đệm (#6121, chỉ ảnh hưởng số log) — [PR #6121](https://github.com/huggingface/trl/pull/6121). Hai sửa thống kê 3–4/9/2026 ngay trước khi xoá không vào bản phát hành nào có PPO — [lịch sử tệp](https://github.com/huggingface/trl/commits/v1.12.0/trl/experimental/ppo/ppo_trainer.py).
- **Đường đang dùng hợp lệ:** `GRPOTrainer` v0.29.1 cố ý nhận lợi thế (B, T): "To support subclasses that provide advantages with shape (B, T) (e.g., MiniLLM), we *conditionally* unsqueeze" (dòng 2140–2143); clip đi qua `num_iterations` và `epsilon` — [grpo_trainer.py](https://github.com/huggingface/trl/blob/v0.29.1/trl/trainer/grpo_trainer.py). `harness/grpo_ppo.py` đặt `out["advantages"]` cỡ (B, T) nên đi đúng nhánh này, không bị broadcast sai [nguồn: đọc mã kho].

### Inferences
- [suy] Vá `PPOTrainer` v0.29.1 cho VLM phải viết lại rollout, forward, reward, lớp value và gradient checkpointing; nhiều hơn phần đã có ở `grpo_ppo.py`. Đừng đi đường này.
- [suy] Câu trả lời cho thầy có thể dùng: công cụ PPO quen thuộc nhất của hệ sinh thái Hugging Face chưa từng hỗ trợ ảnh và đã bị gỡ 9/2026, nên PPO trong đề tài phải tự cài và phải khai.

### Gaps
- Chưa chạy `trl.experimental.ppo` thật; kết luận dựa trên đọc mã.

## 2. Framework khác

### Takeaway
Ba framework lớn có PPO và có VLM nhưng **không ghép được hai thứ đó một cách đã kiểm chứng**: OpenRLHF cấm thẳng, SkyRL và AReaL có dấu hiệu chỉ cho critic chạy không ảnh hoặc không nạp được, veRL có đường dự phòng chưa ai công bố kết quả. Molt là nơi duy nhất có mã critic đa phương thức rõ ràng nhưng đòi CUDA 13 và không nhắm máy nhỏ.

### Cited Findings

| Công cụ | PPO + critic | Qwen2.5-VL | Critic có thấy ảnh | Máy nhỏ / 4-bit | Giấy phép · hoạt động (GitHub API 3/11) | Công dựng |
|---|---|---|---|---|---|---|
| **TRL 0.29.1 `experimental.ppo`** | Có, critic tách riêng | Không | Không | 4-bit qua `get_quantization_config` | Apache-2.0 · 19,7k sao · PPO đã bị xoá khỏi nhánh chính | Thấp, nhưng vô dụng cho VLM |
| **TRL 0.29.1 `GRPOTrainer` + lớp con** (đường kho) | Tự cài | Đang chạy thật trong kho | Theo cách cài | Đang chạy T4 12,7–13,2 GiB [đo-kho] | như trên | Đã có |
| **veRL** | Có, ví dụ PPO chỉ văn bản | Script GRPO cho 2.5-VL-7B | Có đường mã, chưa có kết quả công bố | Không thấy nạp 4-bit; công thức 1 GPU 24 GB còn là PR mở | Apache-2.0 · 24,1k · hôm nay | Cao: Ray + vLLM + transformers 5 |
| **OpenRLHF** | Có | "VLM like Qwen3.5" | **Cấm** bằng `assert` | Có 4-bit trong `get_llm`; cần Ray + DeepSpeed + vLLM | Apache-2.0 · 10,1k · hôm nay | Cao |
| **SkyRL** | Có (`CriticWorkerBase`, `ppo_critic_loss`) | FSDP "mọi model HF + vLLM" | `forward` của critic không có tham số ảnh | Có 4-bit ở wrapper policy | Apache-2.0 · 2,5k · 2/11 | Cao |
| **AReaL** | Có (`examples/math/gsm8k_ppo.yaml`) | Có trong bảng model | Critic nạp bằng `AutoModelForTokenClassification` | Không kiểm | Apache-2.0 · 5,9k · hôm nay | Cao |
| **Molt (NVIDIA)** | Có, tuỳ chọn (`--algo.advantage.estimator gae`) | Có nhắc Qwen2.5-VL trong mã | **Có mã** | Đòi CUDA 13; không thấy 4-bit | Apache-2.0 · 1,2k · hôm nay | Rất cao |
| **RL4LMs** | Có PPO, A2C, TRPO, NLPO; có thưởng metric | Không (GPT-2, T5, BART) | Không | — | Apache-2.0 · 2,4k · **đẩy cuối 3/2024** | Trung bình, cũ |
| **Unsloth** | **Không** (PPO chỉ là nền) | Có vision RL theo GRPO | — | Mục tiêu máy nhỏ | Apache-2.0 · 79k · hôm nay | Thấp |
| **Tinker** | Có `ppo` loss, **không có critic** | **Không** có trong danh sách | — | Dịch vụ thuê theo token | Apache-2.0 (SDK) | Thấp nhưng sai model |
| **TorchRL** | Mục `objectives/llm` chỉ có GRPO, SFT, distillation, reward | Không thấy | — | — | MIT · 3,6k · hôm nay | Cao |
| **CleanRL** | Có, cho Gym, "not meant to be imported" | Không | — | — | README không khẳng định được qua API · 10,6k · 4/2026 | Không phù hợp |
| **RLlib** | Chưa xác minh được cho LLM | — | — | — | Apache-2.0 · 44,2k | Không phù hợp [suy] |

Dẫn chứng từng dòng:
- **OpenRLHF, nguyên văn:** `"VLM training does not support critic model. Use --advantage_estimator other than 'gae' (e.g., reinforce_baseline, rloo, group_norm)."` — [train_ppo_ray.py, dòng 661–666](https://github.com/OpenRLHF/OpenRLHF/blob/26494490bc237f6c3af62dab6117e6bbb0a78dba/openrlhf/cli/train_ppo_ray.py#L661). README hiện đẩy người dùng sang Molt ("Recommended: Molt") và ghi PPO là "Full critic network", thưởng tuỳ ý qua `--reward.remote_url` — [README](https://github.com/OpenRLHF/OpenRLHF/blob/main/README.md).
- **veRL, critic:** `load_valuehead_model` thử `AutoModelForTokenClassification`, không được thì dùng `AutoModelForVision2Seq` + `AutoModelForCausalLMWithValueHead` **của TRL**, import từ `trl.experimental.ppo` rồi đến `trl` — [utils/model.py, dòng 467–510](https://github.com/verl-project/verl/blob/184687b/verl/utils/model.py#L467). Extras của veRL ghim `trl<=0.9.6` trong khi lõi đòi `transformers>=5.5.3,!=5.6.0,<5.17` — [setup.py](https://github.com/verl-project/verl/blob/184687b/setup.py). PR #7020 của TRL cũng ghi veRL ghim `trl<=0.9.6` — [PR #7020](https://github.com/huggingface/trl/pull/7020).
- **veRL, tình trạng VLM + critic:** câu hỏi "qwen2.5-vl as critic model in ppo" mở từ 28/3/2025; bình luận 4/7/2026 nói mô hình chuẩn có thể đi đường dự phòng nhưng "không thấy ví dụ đầu cuối hay kết quả công khai của Qwen2.5-VL làm critic PPO", khuyên smoke test (người viết không rõ có phải nhóm bảo trì, tôi coi là bằng chứng yếu) — [issue #804](https://github.com/verl-project/verl/issues/804). PR vá critic + VLM với Ulysses vẫn mở từ 28/11/2025 — [PR #4344](https://github.com/verl-project/verl/pull/4344). Ví dụ PPO hiện là `run_qwen3_8b_fsdp.sh` trên GSM8K + MATH — [examples/ppo_trainer](https://github.com/verl-project/verl/tree/184687b/examples/ppo_trainer). Script VLM dùng GRPO — [run_qwen2_5_vl_7b_fsdp.sh](https://github.com/verl-project/verl/blob/184687b/examples/grpo_trainer/run_qwen2_5_vl_7b_fsdp.sh).
- **veRL, tiện ích khác:** thưởng tuỳ ý bằng `custom_reward_function.path` — [reward_function.rst](https://github.com/verl-project/verl/blob/184687b/docs/preparation/reward_function.rst); LoRA qua `lora_rank`, kể cả cấu hình critic — [critic.py](https://github.com/verl-project/verl/blob/184687b/verl/workers/config/critic.py).
- **veRL, máy nhỏ:** PR mở 27/10/2026 ghi công thức chính thức giả định "8x80G class"; một RTX 4090 24 GB chạy GRPO + LoRA cho **Qwen2.5-Math-1.5B văn bản**, đỉnh ~18–20 GB, `gpu_memory_utilization=0.45` — [PR #8405](https://github.com/verl-project/verl/pull/8405) (tự báo, chưa gộp).
- **SkyRL:** critic nạp qua `get_llm_for_sequence_regression` (`AutoModel._model_mapping[type(config)]`); `forward` của critic nhận `input_ids, num_actions, attention_mask, return_output`, không có `pixel_values`, còn `forward` của policy có — [model_wrapper.py](https://github.com/NovaSky-AI/SkyRL/blob/bd35ce1/skyrl/backends/skyrl_train/workers/model_wrapper.py) · [worker.py](https://github.com/NovaSky-AI/SkyRL/blob/bd35ce1/skyrl/backends/skyrl_train/workers/worker.py). Cấu hình ghi critic chỉ dùng được với FSDP — [config.py](https://github.com/NovaSky-AI/SkyRL/blob/bd35ce1/skyrl/train/config/config.py).
- **AReaL:** `if self.config.is_critic: model_class = AutoModelForTokenClassification` — [fsdp_engine.py](https://github.com/areal-project/AReaL/blob/main/areal/engine/fsdp_engine.py); README liệt kê Qwen2.5-VL, mục VLM ghi "with GRPO" — [README](https://github.com/areal-project/AReaL/blob/main/README.md).
- **Molt:** critic là "`NeMoAutoModelForCausalLM` + a scalar value head", cụm Ray riêng, mặc định cùng GPU với actor, có optimizer và LR riêng, clip giá trị — [README dòng 269](https://github.com/NVIDIA-NeMo/labs-molt/blob/main/README.md); `critic_actor.py` trộn `mm_train_inputs` vào forward critic nếu `is_vlm` — [critic_actor.py](https://github.com/NVIDIA-NeMo/labs-molt/blob/a2f3fe9/molt/trainer/workers/critic_actor.py). "Requires CUDA 13 (`torch==2.13.0+cu130`); a CUDA-12 environment will not work" — [README](https://github.com/NVIDIA-NeMo/labs-molt/blob/main/README.md).
- **Unsloth:** hỗ trợ GRPO, GSPO, Dr. GRPO và vision RL; trang không nói có PPO — [RL guide](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide).
- **Tinker:** 24 model, model thị giác duy nhất là Nemotron-3.5-Super-VL, không có Qwen2.5-VL — [Tinker](https://thinkingmachines.ai/tinker/). RL loss nhận "exactly `target_tokens`, `logprobs`, and `advantages`"; `forward_backward_custom` là "arbitrary loss over logprobs" ⇒ không thấy đường train critic — [Losses](https://tinker-docs.thinkingmachines.ai/tinker/losses).
- **RL4LMs:** "On-policy algorithms of PPO, A2C, TRPO and novel NLPO"; hỗ trợ causal LM và seq2seq; ví dụ thưởng Rouge-1 — [README](https://github.com/allenai/RL4LMs/blob/main/README.md).
- **TorchRL:** thư mục `objectives/llm` có `grpo.py, sft.py, distillation.py, reward.py` — [objectives/llm](https://github.com/pytorch/rl/tree/main/torchrl/objectives/llm).
- **CleanRL:** "CleanRL is *not* a modular library and therefore it is not meant to be imported" — [README](https://github.com/vwxyzjn/cleanrl/blob/master/README.md).

### Inferences
- [suy] SkyRL với ảnh: critic sẽ chạy trên chuỗi token có placeholder ảnh mà không có đặc trưng ảnh, có thể không báo lỗi. AReaL: không có lớp token classification cho `qwen2_5_vl` nên critic nhiều khả năng không nạp được. Cả hai cần smoke test mới khẳng định.
- [suy] veRL: nhánh dự phòng phụ thuộc lớp TRL đã bị xoá khỏi TRL ≥ 1.13 và một bản ghim rất cũ; khả năng tương thích `trl<=0.9.6` với transformers 5 là rủi ro lớn, chưa kiểm.
- [suy] Mọi framework Ray + vLLM dùng thêm bộ nhớ cho engine rollout. Đường rẻ nhất trong đó tự báo 18–20 GB cho model 1,5B văn bản, nên 3,75B VLM + critic trên T4 16 GB không thực tế; và mỗi lần chuyển là phải chứng minh lại tính tương đương với ck500 (fp16, đường sinh, dữ liệu).
- [suy] Quan trọng cho so sánh: dự án đã tốn công khoá đường sinh và đo kiểm hoà; đổi framework làm lẫn biến "thuật toán" với biến "công cụ", đúng thứ phép so lưới muốn tránh.

### Gaps
- RLlib: trang tài liệu tôi tải về trống, không có bằng chứng về LLM.
- EasyR1: kết quả tìm kiếm nói danh sách việc của họ còn "support PPO" cho VLM, nhưng tôi không mở được kho `hkust-nlp/EasyR1` để xác nhận, nên coi là chưa xác minh.
- CUDA hiện tại trên Colab và Kaggle chưa kiểm, nên chưa kết luận Molt có cài nổi không.
- Không có framework nào ở trên được chạy thử.

## 3. Reference implementation dựng critic thế nào, cái gì là "chuẩn"

### Takeaway
Chuẩn mà người phản biện chờ đợi là **mô hình tách riêng, khởi tạo từ checkpoint đã huấn luyện, thay lớp unembedding bằng đầu vô hướng**. Nhưng critic không cần cùng cỡ với policy (InstructGPT có tiền lệ), và các bài GRPO, RLOO chính là phản ứng với giá của critic đó.

### Cited Findings
- **InstructGPT (NeurIPS 2022):** "The value function is initialized from the RM"; "For the reward models and value functions, the unembedding layer of the original model is replaced with a projection layer to output a scalar value"; "we trained a single 6B reward model which we used for all PPO models of all sizes", 175B RM "less suitable for use as initializations for the PPO value functions" và "greatly increase the compute requirements of PPO"; "6B RMs ... led to equally strong PPO models" — [arXiv 2203.02155](https://arxiv.org/abs/2203.02155).
- **Stiennon et al. (NeurIPS 2020):** "a Transformer with completely separate parameters from the policy. This prevents updates to the value function from partially destroying the pretrained policy early in training"; "reward model, policy, and value function are the same size". Phụ lục G.1: "using separate networks outperforms" mạng chung, đổi lại "increases the memory requirements" — [arXiv 2009.01325](https://arxiv.org/abs/2009.01325).
- **N+ Details (Huang et al., arXiv 2024, không thấy venue trên arXiv):** "Value model initializes from the reward model"; khởi tạo ấm "can greatly improve initial gradients" — [arXiv 2403.17031](https://arxiv.org/abs/2403.17031).
- **VinePPO (ICML 2025):** mạng giá trị "typically a separate model initialized from a pretrained checkpoint"; "often initialized using the initial SFT policy πref (or the reward model when available), with the language modeling head swapped out for a scalar head"; "PPO uses double GPU memory — the value network needs **112GB for a 7B LLM**, considering both model and its optimizer"; thêm "a forward pass for value prediction and a forward-backward pass for value network training" — [arXiv 2410.01679](https://arxiv.org/abs/2410.01679).
- **RLOO, *Back to Basics* (ACL 2024, tr. 12248–12267):** "PPO typically requires loading up to 4 models simultaneously: the generator, the reference ..., the critic, and the reward model"; phương pháp của họ tải ít hơn một bản sao vì bỏ mạng giá trị — [ACL Anthology](https://aclanthology.org/2024.acl-long.662) · [arXiv 2402.14740](https://arxiv.org/abs/2402.14740).
- **DeepSeekMath (preprint, arXiv không ghi venue):** "GRPO foregoes the critic model, instead estimating the baseline from group scores, significantly reducing training resources"; Hình 4 vẽ PPO có Value Model, GRPO không có — [arXiv 2402.03300](https://arxiv.org/abs/2402.03300). Trong phần tôi trích không có con số bộ nhớ.
- **DeepSeek-R1 (Nature 645, 633–638, 2025):** GRPO "originally proposed to simplify the training process and reduce the resource consumption of" PPO; phụ lục A.3 so hai thuật toán — [arXiv 2501.12948](https://arxiv.org/abs/2501.12948). Tôi chỉ đọc đoạn đầu A.3.
- **UI-TARS-2 (preprint):** "trained using Proximal Policy Optimization"; thêm Decoupled GAE, Length-Adaptive GAE (α = 0,05), **Value Pretraining** ("offline training of the value model to convergence under a fixed policy", GAE λ = 1,0), Clip Higher. "PPO consistently outperforms GRPO by a clear margin" ở "preliminary evaluation" — [arXiv 2509.02544](https://arxiv.org/abs/2509.02544). Trong đoạn đã đọc, bài không nêu kích thước mạng giá trị; miền và trần thưởng khác đề tài (tác vụ dài nhiều lượt).
- **VC-PPO, VAPO (preprint):** khởi tạo từ reward model là nguồn "value initialization bias"; VAPO: "value network was initialized using a reward model", λ = 0,95, γ = 1,0, ε = 0,2 — [arXiv 2503.01491](https://arxiv.org/abs/2503.01491) · [arXiv 2504.05118](https://arxiv.org/abs/2504.05118).
- **RL thường (Andrychowicz et al., ICLR 2021):** "Separate value and policy networks ... appear to lead to better performance on four out of five environments" — [arXiv 2006.05990](https://arxiv.org/abs/2006.05990).

### Inferences
- [suy] Thứ hạng mức chấp nhận khi bị phản biện: (1) copy riêng, train toàn bộ, khởi từ SFT · (2) copy riêng, nhỏ hơn hoặc train một phần (có tiền lệ InstructGPT về cỡ, tiền lệ về LoRA thì tôi chưa thấy) · (3) adapter riêng trên backbone đóng băng dùng chung: tham số train được tách hoàn toàn, nhưng đây là cách cài của đề tài, phải khai · (4) đầu nhỏ tách gradient: gọi đúng là "bản rút gọn".
- [suy] `harness/grpo_ppo.py` nói đúng khi ghi "đầu giá trị nhỏ, KHÔNG phải critic đủ cỡ" (mục 5 `report/329`). Không bài nào ở trên dùng cấu hình này nên phải trình như rút gọn.
- Không có bài nào ở trên huấn luyện critic bằng LoRA theo những gì tôi đọc; đó là khoảng trống cần khai.

### Gaps
- Chưa kiểm cách critic được cài trong mã của DeepSeek hay UI-TARS-2 (mã huấn luyện không công khai, hoặc không tìm thấy).
- Venue của InstructGPT (NeurIPS 2022): không ghi trên trang arXiv, theo hiểu biết chung, chưa mở trang NeurIPS.

## 4. Chất lượng critic khi thưởng chỉ có ở cuối câu, và đầu giá trị trên đặc trưng tách gradient

### Takeaway
Bằng chứng nghiêng về: critic trên LLM dễ tệ dù chỉ số đẹp, λ cao an toàn hơn, huấn luyện trước critic đáng làm. UI-TARS-2 cho thấy chiều ngược: critic hiệu chỉnh tốt thì PPO có thể hơn GRPO. **Không tìm thấy nghiên cứu trực tiếp về đầu giá trị trên đặc trưng tách gradient cho LLM.**

### Cited Findings
- VinePPO: explained variance của critic đạt **0,7–0,9** nhưng khi chọn bước tiếp theo trong năm khả năng, mạng giá trị "performs near chance levels for most of the training" ⇒ explained variance cao không chứng minh critic xếp hạng được hành động — [arXiv 2410.01679](https://arxiv.org/abs/2410.01679). Miền: suy luận toán, câu dài.
- VC-PPO: "In scenarios with long sequences and rewards at the end, the value function fails to propagate the reward signal to the preceding tokens" với GAE có suy giảm; chữa bằng tách λ actor và critic — [arXiv 2503.01491](https://arxiv.org/abs/2503.01491).
- RLOO, Hình 1: trong RLHF, "a higher emphasis on variance reduction at the cost of bias (low λ) performs worse" — [arXiv 2402.14740](https://arxiv.org/abs/2402.14740). Bài ghi: "modeling partial sequences is unnecessary in the context of RLHF".
- UI-TARS-2: "the value estimates of PPO-trained models were often negatively correlated with the obtained rewards"; sau khi huấn luyện trước "consistently higher rewards" — [arXiv 2509.02544](https://arxiv.org/abs/2509.02544).
- SCST (CVPR 2017), đúng thưởng CIDEr: "estimating the reward signal (as actor-critic methods must do) and estimating normalization ... is avoided" — [arXiv 1612.00563](https://arxiv.org/abs/1612.00563).
- Bahdanau et al. (*An Actor-Critic Algorithm for Sequence Prediction*): với bài toán có giám sát, "we condition the critic network on the ground-truth output" và "Receiving intermediate rewards may ease the learning for the critic" — [arXiv 1607.07086](https://arxiv.org/abs/1607.07086). Trang arXiv không ghi venue; tôi không xác minh ICLR 2017 tại nguồn.
- Chung so với tách: Stiennon G.1 và Andrychowicz ở mục 3 là bằng chứng gần nhất, cả hai so *mạng chung có gradient* với *mạng tách*, không so đầu tách gradient.

### Inferences
- [suy] Đầu tách gradient thoả mối lo của Stiennon (không phá policy), nhưng đặc trưng thay đổi theo policy và nó không tự học biểu diễn được; khả năng biểu diễn thấp hơn mọi phương án có thân riêng.
- [suy] **Điểm dễ bỏ sót:** thưởng SPICE, CIDEr-D phụ thuộc câu chuẩn. Critic không thấy câu chuẩn thì không thể biết tiền tố đang trúng hay trật, nên phần sai số không giảm được có thể lớn. Bahdanau cho tiền lệ đưa câu chuẩn vào critic lúc train. Đầu nhỏ không làm được việc này vì chỉ đọc đặc trưng của policy; adapter hoặc copy riêng thì làm được bằng cách thêm câu chuẩn vào đầu vào **của critic**.
- [suy] Câu của dự án ngắn (trung bình khoảng 7 từ ở lượt ck250, `CLAUDE.md`), nên vấn đề suy giảm tín hiệu của VC-PPO nhẹ, và với λ = 1 thì hết hẳn. Vì vậy λ = 1,0 là nhánh chính hợp lý, λ = 0,95 là nhánh thử. Với λ = 1 critic chỉ đóng vai trò baseline; lợi thế token là r − V(s_t).
- [suy] Khởi tạo bằng 0 như `grpo_ppo.py` làm những bước đầu xấp xỉ REINFORCE chuẩn hoá theo lô chứ chưa phải PPO có critic. Huấn luyện trước đầu giá trị trên mẫu S1 (không cập nhật policy) gần như miễn phí nếu cache đặc trưng.
- [suy] Báo cáo critic cần **hai** chỉ số: explained variance (đã có `luoi/v_ev`) và một phép xếp hạng trên cùng tiền tố nếu đủ rẻ. Chỉ in EV sẽ bị đòn của VinePPO.

### Gaps
- Không tìm được bài đo critic cho thưởng độ đo câu ngắn trên VLM. Mọi số trên là suy luận toán, tóm tắt, tác vụ agent.
- Chưa đọc Phasic Policy Gradient, DAAC và các bài RL cổ điển về chia sẻ đặc trưng; đề xuất tra riêng nếu cần trích về đặc trưng tách gradient.

## 5. Bộ nhớ và thời gian của critic thêm trên VLM 3B

### Takeaway
Critic toàn phần theo công thức của VinePPO cần ~56 GiB (không vừa A100 40 GB). LoRA critic trên backbone dùng chung ước vừa T4; copy đóng băng + LoRA cần T4×2 hoặc A100; 4-bit + LoRA vừa L4. **Tất cả cột ước lượng phải đo bằng probe.**

### Cited Findings
- Qwen2.5-VL-3B-Instruct: **3.754.622.976 tham số**, BF16, 7.509.245.952 byte — [HF API](https://huggingface.co/api/models/Qwen/Qwen2.5-VL-3B-Instruct) · [index](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/raw/main/model.safetensors.index.json). Đọc header safetensors: `visual.*` **668.684.288**, phần còn lại **3.085.938.688**; hidden size 2048 — [config](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/raw/main/config.json).
- Số đo kho [đo-kho]: GRPO trên T4 12,71 GiB ở lượt GRPO + CIDEr-D, SFT tiếp 10,94 GiB (`report/326` mục 3); `grpo_spice` 13,22 GiB, 160,6 s/bước (`CLAUDE.md`). VRAM thật T4 trong kho ~14,56 GiB (`CLAUDE.md`). GRPO 500 bước, G = 4 trên A100: 5,63 h (`CLAUDE.md` mục 6/9, `report/144`). LoRA 14.966.784 tham số (`CLAUDE.md`). Lượt PPO đầu nhỏ **chưa có số probe**: `_bundles/luoi/k_luoi-probe-ppo/` chỉ có notebook, chưa có log.
- Quy đổi từ VinePPO: 112 GB / 7B = **16 byte/tham số** (fp32: trọng số + grad + 2 trạng thái Adam, theo cách tôi hiểu "model and its optimizer") — [arXiv 2410.01679](https://arxiv.org/abs/2410.01679).

Ước lượng [suy], lấy nền policy ~13 GiB, giả định critic chạy tuần tự nên kích hoạt của policy và critic không cộng dồn:

| Thiết kế critic | Thấy ảnh | Thêm vào bộ nhớ (tính) | Đỉnh ước | T4 ~14,6 | T4×2 | L4 ~22 | A100 40 | A100 80 / G4 |
|---|---|---|---|---|---|---|---|---|
| Đầu nhỏ MLP (1.049.601 tham số, đang có) | Qua đặc trưng policy | ~0,02 GiB | ~13 GiB | Vừa | Vừa | Vừa | Vừa | Vừa |
| Adapter LoRA thứ hai trên backbone chung | Có | 16 B × 14,97M = ~0,22 GiB | ~13,3 GiB | Vừa, biên ~1 GiB | Vừa | Vừa | Vừa | Vừa |
| Copy NF4 đóng băng + LoRA | Có | 0,5 B/tham số ≈ 1,75 GiB tối thiểu; ~2,5–3 GiB thực tế + 0,22 | ~16 GiB | **Không** | Vừa | Vừa, sát giới hạn 17 GB của thủ tục chọn máy | Vừa | Vừa |
| Copy fp16 đóng băng + LoRA | Có | 6,99 + 0,22 GiB | ~20,5 GiB | **Không** | Vừa nếu đặt critic ở GPU 2 | Sát, vượt mức 17 GB | Vừa | Vừa |
| Copy train toàn bộ, tất cả fp16, đóng băng thị giác | Có | ~24 GiB | ~37 GiB | Không | Không | Không | Sát | Vừa |
| Copy train toàn bộ, tất cả fp16 | Có | 8 B × 3,75B = ~28 GiB | ~41 GiB | Không | Không | Không | **Không/rất sát** | Vừa |
| Copy train toàn bộ, fp32 (như VinePPO) | Có | 16 B × 3,75B = ~56 GiB | ~69 GiB | Không | Không | Không | Không | Sát trên 80 GB; vừa G4 ~96 |

Thời gian [suy]: thêm một forward không gradient cho mỗi lô sinh và một forward-backward cho mỗi lô cập nhật, theo mô tả của VinePPO. Với T4 đang 150–160 s/bước mà phần lớn nằm ở sinh mẫu thì adapter critic có thể thêm ~10–30%; đầu nhỏ thêm một forward không gradient. Chưa đo, không dùng con số này để quyết.

Chi phí [suy], từ 5,63 h GRPO G = 4 trên A100 và giá mục 6: G = 8 + critic khoảng 15–25 h, tức 80–135 đơn vị (~8–14 USD) trên A100 40 GB; 130–220 đơn vị (~13–22 USD) trên G4 nếu tốc độ như A100 (giả định chưa kiểm).

### Inferences
- [suy] 4-bit: kho đã chốt `--no-q4` trên T4 vì kiểm hoà 14/20 và thăm dò không qua (ghi chú 29/9 trong runbook). Lý do đó áp cho policy; critic không cần tái lập chính xác S1 nên 4-bit vẫn hợp lệ cho critic, nhưng trộn 4-bit và fp16 trong một tiến trình là phần việc mới, cần thử.
- [suy] T4×2 đặt critic ở GPU 2 khiến mỗi phiên chỉ chạy một lượt thay vì hai, tức gấp đôi hạn mức trên mỗi lượt. Chỉ dùng khi đã chọn được.
- [suy] Adapter critic đi cùng cấu trúc đã có: TRL đã dùng adapter `ref` bên cạnh policy trên cùng backbone (`add_adapter("ref")`, `CLAUDE.md` mục 6/9). Bẫy cần kiểm: đổi adapter chủ động giữa các forward với gradient checkpointing; chỉ tham số adapter critic được vào optimizer riêng; và lần nạp lại phải in `[nạp …]` như bài học 30/9.

### Gaps
- Không có nguồn đo VRAM của critic cho VLM 3B. Bảng trên là tính toán.
- Phân bổ thời gian giữa sinh và backward trên T4 chưa đo.

## 6. GPU và giá Colab, kiểm 3/11/2026

### Takeaway
Giá gói và giá đơn vị đã kiểm tại trang chính thức hôm nay. Tốc độ đốt đơn vị theo từng GPU Google không công bố công khai trong phần tôi truy cập được; số dưới đây là đo của cộng đồng (3/2026) và đo của kho (8/2026).

### Cited Findings
- **Trang chính thức (HTML tải không đăng nhập, 3/11):** Colab Pro **9,99 USD**, Pro+ **49,99 USD**, Pay As You Go **100 đơn vị 9,99 USD · 500 đơn vị 49,99 USD**. Cấu hình trang liệt kê bộ tăng tốc `T4, A100, G4, H100, L4, V5E1, V6E1` — [Colab signup](https://colab.research.google.com/signup). Giá hiển thị có thể tuỳ khu vực.
- FAQ: "The types of GPUs and TPUs that are available in Colab vary over time"; không ghi giá và không định nghĩa đơn vị — [FAQ](https://research.google.com/colaboratory/faq.html).

| GPU | VRAM | Đơn vị/giờ (McCormick, 10/3/2026) | Đo trong kho | USD/giờ tính từ 9,99 USD/100 đơn vị |
|---|---|---|---|---|
| T4 | 16 GB, 15 GB dùng được | 1,19 | ~14,56 GiB VRAM | ~0,12 |
| L4 | 22,5 GB | 1,71 | 1,54 đơn vị/h (11/8/2026) | ~0,15–0,17 |
| A100 | 40 GB | 5,40 | 5,3 đơn vị/h (11/8/2026) | ~0,53 |
| A100 | 80 GB | 7,52 | Chưa thấy | ~0,75 |
| G4 (RTX PRO 6000) | ~96 GB | 8,71 | Chưa thấy | ~0,87 |
| H100 | 80 GB | Chưa đo | Chưa thấy | — |

Nguồn bảng: [McCormick](https://mccormickml.com/2024/04/23/colab-gpus-features-and-pricing/), bảng ghi vùng nam California, tác giả lưu ý giá có thể dao động · `report/110_PHIEN_0_COLAB_11_8.md`. Tin rao ở Đức xác nhận có A100 80 GB và G4 96 GB trong gói: [mydealz](https://www.mydealz.de/deals/google-ai-pro-200-google-colab-compute-units-wert-21eur-monatlich-inklusive-auch-im-5eurmonat-promo-abo80gb-nvidia-a100-96gb-g4-gpu-2857205) (nguồn thứ cấp).

### Inferences
- [suy] So card theo đơn vị mỗi lượt: L4 rẻ hơn A100 khoảng 3,2–3,4 lần; nếu probe cho thấy L4 chậm hơn quá 1,5× theo luật 9/9 thì lên A100.

### Gaps
- Tốc độ đốt đơn vị hiện tại, và tài khoản của dự án có truy cập được A100 80 GB, G4 hay không: cần xem trong phiên đã đăng nhập.
- Quota Pro+ (500 hay 600 đơn vị) các nguồn thứ cấp mâu thuẫn; trang chính thức trong HTML không ghi rõ số đơn vị của Pro, Pro+.

## 7. Khuyến nghị

### Takeaway
**Giữ TRL 0.29.1 và tự cài PPO theo bậc thang bốn nhánh, đặt tên trung thực từng nhánh; không đổi framework.**

### Cited Findings
- Căn cứ ở mục 1–6: OpenRLHF cấm critic với VLM — [dòng 661](https://github.com/OpenRLHF/OpenRLHF/blob/26494490bc237f6c3af62dab6117e6bbb0a78dba/openrlhf/cli/train_ppo_ray.py#L661); veRL chưa có kết quả công bố — [issue #804](https://github.com/verl-project/verl/issues/804); TRL `GRPOTrainer` nhận lợi thế (B, T) — [grpo_trainer.py](https://github.com/huggingface/trl/blob/v0.29.1/trl/trainer/grpo_trainer.py); huấn luyện trước critic có bằng chứng — [UI-TARS-2](https://arxiv.org/abs/2509.02544).

### Inferences
Thứ tự đề xuất [suy], từ rẻ đến đắt:

| Bậc | Việc | Máy | Tên khi báo |
|---|---|---|---|
| 0 | Probe `grpo_ppo.py` như đã định: VRAM, s/bước, `clip_ratio`, `v_ev`. Lưu ý μ = 1 thì clip không hoạt động; PPO đúng nghĩa cần μ ≥ 2 | T4 | — |
| 1 | PPO đầu nhỏ λ = 1,0 và 0,95; thêm **huấn luyện trước đầu giá trị** trên mẫu S1, không đổi policy | T4 | "PPO, đầu giá trị nhỏ tách gradient (bản rút gọn)" |
| 2 | **Nhánh chính cho câu hỏi của thầy:** adapter LoRA riêng cho critic trên backbone S1 đóng băng, có ảnh, optimizer riêng, huấn luyện trước, đầu vô hướng. Tuỳ chọn thêm một biến thể critic thấy câu chuẩn (Bahdanau) | T4 nếu probe ≤ ~14 GiB; không thì L4 | "PPO, critic LoRA (tham số train tách khỏi policy, chung phần đóng băng)" |
| 3 | Chỉ nếu bậc 2 có số đáng xem hoặc thầy đòi đúng chuẩn: copy critic riêng khởi từ S1, chạy một lần | A100 80 GB hoặc G4, hoặc A100 40 GB nếu đóng băng thị giác | "PPO, critic tách riêng" |

Đọc kết quả, cũng là câu trả lời "vì sao GRPO hay PPO tốt hơn":
- Nếu PPO thua ck500: chưa kết luận được thuật toán thua nếu chỉ có bậc 1. Có bậc 2 hoặc 3 kèm critic đạt chất lượng đo được thì mới có căn cứ, và phù hợp VinePPO, RLOO.
- Nếu PPO thắng: phù hợp UI-TARS-2, nhưng miền khác; khai hạt giống, MDE như các nhánh khác.
- Phải khai: cài đặt tự viết trên `GRPOTrainer`, không phải PPOTrainer của thư viện; và lý do (mục 1). Có đơn vị kiểm thử GAE trong `selftest_ppo`, nên giữ và trích được.

Không khuyên: chuyển veRL hoặc Molt cho đề tài này (chi phí dựng lớn, lẫn biến công cụ, chưa có kết quả tham chiếu); thử Tinker, Unsloth (không có critic hoặc không có model); dùng VinePPO cho T4 (bản thân bài ghi mỗi bước chậm tới 2–5 lần so với PPO do sinh thêm mẫu, trên nền 150–160 s/bước của dự án là không kham nổi).

### Gaps
- Xác suất PPO hơn ck500 trên bài toán này: không có căn cứ để định lượng.
- Tiền lệ cho "critic LoRA trên backbone đóng băng" trong LLM RL: tôi không tìm thấy trong những nguồn đã đọc và chưa tra riêng. Nên tra thêm trước khi viết vào luận văn.
