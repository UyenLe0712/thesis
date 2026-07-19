# KẾ HOẠCH BUILD MODEL — "FAITHFUL DISTILLATION" (Qwen2.5-VL-3B, SFT-LoRA)

> Nguồn: workflow `wf_a4401c9d-f93` (2026-07-10, 23 agent: 5 research + 4 giám khảo "đủ ngưỡng thạc sĩ chưa" + 4 phần kế hoạch build, mỗi phần có agent kiểm tra tính khả thi/chính xác). Đây là kế hoạch build CỤ THỂ, đã sửa theo mọi phát hiện của bước verify (số liệu bịa/case-study gán nhầm đã bị lọc ra — xem mục 6). Đi kèm `report/52` (debate tính-mới) làm nền tảng lý do.
>
> **Cập nhật 2026-07-12** (audit Fable 5, kiểm tra độ vững toàn bộ quyết định + citation/thống kê): đã sửa 3 chỗ trong file này để khớp với `report/54` — (1) §5.6 định nghĩa lại DUY NHẤT `Δ_train` (bỏ mốc mơ hồ "trong-phân-phối, CLAUDE.md §6"); (2) §5.2 thêm ngưỡng đậu/rớt bằng số cho Tier 1 (trước đó chỉ có mô tả định tính); (3) đổi ký hiệu `f_base` → `f_teacher` xuyên suốt để không nhầm với "base-model Qwen chưa fine-tune" dùng ở report/50 §9. Chi tiết đầy đủ + các vá khác: `report/54` (Phụ lục E, G).

---

## 0. Verdict "đủ ngưỡng thạc sĩ chưa" (tóm tắt — xem bản đầy đủ cuối file)

**ĐỦ-CÓ-ĐIỀU-KIỆN.** 4/4 giám khảo (đọc-nghĩa-đen-yêu-cầu-thầy, chuẩn-học-thuật-tổng-quát, rủi-ro-khả-thi, so-sánh-luận-văn-điển-hình) đều hội tụ cùng verdict. Điều kiện quan trọng nhất: **phải tách 2 tầng thực nghiệm** (xem §5.2) — không được gộp thành một phép đo duy nhất, nếu không rủi ro thật không phải "null" mà là "bất định" (CI quá rộng do cỡ mẫu nhỏ), và bất định thì không đóng khung được thành phát hiện gì cả.

---

## 1. TÓM TẮT KIẾN TRÚC + FRAMEWORK ĐÃ CHỐT

**Bài toán:** Distill hành vi "né bịa tên nút" từ teacher gpt-4o-mini (nhìn ảnh+câu hỏi, KHÔNG thấy View Hierarchy) qua lớp lọc dựa-trên-VH, vào trọng số của student Qwen2.5-VL-3B (SFT-LoRA), để student tự sinh hướng dẫn từ CHỈ ảnh+câu hỏi lúc suy luận (on-device, không VH).

**Trụ thực nghiệm số 1 (KHÔNG phải phụ):** đo faithfulness của student khi TẮT HOÀN TOÀN VH lúc suy luận, trên **app chưa từng thấy trong train** (held-out theo app) — câu hỏi "hành vi né-bịa có nội-tại-hoá vào trọng số hay chỉ là pattern bề mặt phụ thuộc bộ lọc ngoài". Có thể ra NULL thật — phải pre-register để null vẫn đậu.

| Hạng mục | Lựa chọn chốt | Lý do |
|---|---|---|
| Model student | Qwen2.5-VL-3B-Instruct | Đã chốt CLAUDE.md §0, có case study thật (ZonUI-3B WACV2026) |
| Framework train | **LLaMA-Factory** | Ví dụ chính thức train Qwen-VL ngay trong repo (`examples/train_lora/`); xử lý sẵn masking multimodal + `train_on_prompt`. Lý do chọn thực sự = phổ biến nhất cộng đồng Qwen-VL + có ví dụ train VL thật, KHÔNG phải "được hãng bảo trợ chính thức" (đã sửa overclaim). |
| Vì sao không TRL/transformers thuần | `assistant_only_loss` của TRL SFTTrainer **chưa hỗ trợ VLM**. Nếu đi route này phải tự viết collator mask token ảnh + prompt — tốn thời gian cho quỹ <3 tháng solo. |
| Quantization | **QLoRA 4-bit (NF4, bitsandbytes) là MẶC ĐỊNH** (không phải fallback) | Colab Pro/Pro+ không đảm bảo GPU cố định (thường rớt về T4 dù xin cao hơn); QLoRA chạy được cả T4 16GB |
| LoRA scope | Freeze **ViT + merger/projector**, LoRA chỉ vào language decoder (`q,k,v,o_proj, gate,up,down_proj`) | Hành vi cần đo là *generation policy* (nói gì), không phải *nhận diện ảnh* (nhìn gì) — freeze vision giữ biến nhiễu tối thiểu cho thí nghiệm trụ chính |
| Data nguồn | MobileViews (train, mở rộng ngoài 30-app hiện có) + AndroidControl (chỉ hiệu chuẩn matcher, KHÔNG train nhiều-màn) + ScreenSpot-v2 (đối chứng) | Đúng CLAUDE.md §5, KHÔNG đổi |

---

## 2. DATA PIPELINE — TỪNG BƯỚC CỤ THỂ + SCHEMA

### 2.1. Đóng băng phân vùng APP (làm ĐẦU TIÊN, trước mọi fetch/API)

File `harness/train_eval_app_split.json`, sinh bởi `harness/dg3_freeze_split.py` (free, không gọi API), **commit git ngay khi sinh**:

```json
{
  "frozen_at_commit": "<git rev-parse HEAD>",
  "seed": 20260710,
  "mobileviews": {
    "eval_apps_30": [ "/* 30 app trong kept_screens_final.json — KHOÁ */" ],
    "train_apps": [ "/* điền sau khi fetch xong, disjoint tuyệt đối với 30 app trên */" ]
  },
  "androidcontrol": {
    "eval_apps_237": [ "/* 237 app trong dg2_episodes.json — KHOÁ */" ],
    "train_apps_optional": []
  }
}
```

Trong 30 app eval này, **thêm bước tách riêng train_apps_30/test_apps_30** (18/12, xem §5) — vì 30-app là bộ DUY NHẤT đã qua gate K1 (recall VH verify), nên chính nó vừa đóng vai trò "nguồn train sạch nhất" vừa đóng vai trò "bộ chấm faithfulness tin cậy" cho trụ thực nghiệm chính.

**Gate K-leak (chạy lại MỖI LẦN trước khi build file SFT cuối):**
- `train_apps` (pool mở rộng ngoài 30-app) ∩ `eval_apps_30` = ∅
- `train_apps` (pool mở rộng, ~231K dòng public MobileViews) ∩ `test_apps_30` (12 app held-out) = ∅ — dedup theo package-name/app-id **bắt buộc, tường minh**. Không dedup → rò rỉ ngầm phá hỏng trụ thực nghiệm chính.
- `androidcontrol.train_apps_optional` ∩ `eval_apps_237` = ∅

### 2.2. Mở rộng pool MobileViews train (free, chỉ tốn băng thông)

Tên shard THẬT trên HuggingFace (`mllmTeam/MobileViews`, thư mục `MobileViews_Screenshots_ViewHierarchies/Parquets/`) chỉ có đúng 4 file:
- `MobileViews_0-150000.parquet` (đã dùng)
- `MobileViews_150001-291197.parquet` (đã dùng)
- `MobileViews_300000-400000.parquet` (CHƯA dùng)
- `MobileViews_400000-522301.parquet` (CHƯA dùng)

Không có shard vượt row-index 522301 qua route Parquet — **pool khả dụng thật ~231.000 dòng mới** (KHÔNG phải "~600K" như README quảng bá — số 600K gộp cả `Apps_CompleteTraces` dạng zip khác cấu trúc, không tương thích code hiện có).

Script: sửa `harness/fetch_mv_expand.py` → `fetch_mv_expand_train.py`, output `dataset_samples/mv_train_pool/`, đọc exclude-list từ `train_eval_app_split.json`.

| Tham số | Giá trị | Ghi chú |
|---|---|---|
| NEW_APPS | ~180-220 | (ước tính, chưa có nguồn xác nhận — cần pilot `SCAN_CAP` lớn hơn) |
| MAX_PER_APP | 5 | Giữ như pilot 127/30 cũ |
| MIN_ACT | 6 | Giữ nguyên logic có sẵn |
| Kỳ vọng ra | ~1.000-1.100 màn / ~200 app | (ước tính, chưa có nguồn xác nhận) |

Sau fetch: dedup perceptual-hash **nội bộ pool train** + **cross-check perceptual-hash train-vs-30-app-eval** (phòng 2 app khác tên nhưng cùng template UI y hệt).

> **✅ THỰC TẾ (đã chạy 2026-07-12):** fetch 2 shard → dedup name+dHash (`fetch_mv_expand_train.py` + `dg3_dedup_pool.py`) → **498 màn / 220 app** (avg ~2.3 màn/app; bỏ 98 màn trùng nội bộ; **0 ca cross-eval → K-leak sạch**). Ít hơn ước tính ~1.000 (per-app mỏng: 92 app 1-màn) nhưng **đủ** (+76 màn train-clean = ~574 màn → ~1.700-2.870 mẫu). Ghi ở `train_eval_app_split.json` → `train_pool_expanded`. Muốn dày hơn: resume fetch (bỏ qua app đã có).

### 2.3. Sinh câu hỏi use-case (free, local Ollama qwen2.5vl:3b)

`harness/dg3_train_questions.py` (mở rộng `dg1_questions.py`): 3 câu hỏi/màn, `temperature=0.6`, dedupe bằng Jaccard token trên câu chuẩn hoá. Giữ cơ chế người duyệt lướt qua trước khi tốn API bước kế.

### 2.4. Gọi teacher gpt-4o-mini sinh BASE (✱ TỐN API — HỎI USER TRƯỚC)

Tái dùng `dg1_run.py`, giữ nguyên `GEN_PROMPT` (CÓ câu "Do NOT invent buttons" — hợp lệ vì đây là teacher, không phải student).

**Chi phí:** pilot 127 màn cũ ~$0.05 → ~1.000 màn × 3 câu ≈ 3.000 lệnh gọi. Nếu giữ tỉ lệ chi phí/lệnh của pilot cũ (~$0.0004/lệnh), tổng có thể chỉ **~$1-2**, không phải $5-20 — chạy `DG1_LIMIT=30` trước để đo cost/màn thật rồi mới quyết định full.

### 2.5. Matcher nomic-embed đối chiếu VH (free, local Ollama)

Tái dùng nguyên `aloha_match.py` + `derive_pa2()` từ `dg1_pa2_score.py`, τA=0.55 (đã freeze). Khác biệt: dùng để **xây target train** (không chỉ đo), nên fallback phải sinh văn bản đọc được, không phải placeholder.

### 2.6. Viết lại bước-bịa thành mô tả chung chung (RULE-BASED, KHÔNG gọi thêm LLM)

**Quyết định thiết kế cốt lõi:** dùng template tất định, KHÔNG dùng LLM rewrite (nếu dùng LLM rewrite, chính lớp lọc lại mở ra nguồn bịa mới — vi phạm luật vàng "không đoán nút khác"). `harness/dg3_rewrite_fallback.py`:

```python
GENERIC_VERB = {"tap": "Tap", "click": "Tap", "toggle": "Toggle", "switch": "Toggle"}
FLOOR_SENTENCES = [  # pool cố định, tự-kiểm không match label thật nào (sim<τA)
    "Look for the option on this screen that matches what you need for this step, and tap it.",
    "Find the relevant control on this screen for this step and use it.",
    "Locate the option on this screen that lets you continue with this step.",
]

def rewrite_fallback(verb, element, note, labels, tau_a=0.55):
    vgen = GENERIC_VERB.get(first_word(verb), "Interact with")
    intent = clean_intent_clause(note)   # cắt cụm dẫn đầu + Title-Case còn sót
    candidate = f"{vgen} the option on this screen that would let you {intent}." if intent \
                else random.Random(hash(element)).choice(FLOOR_SENTENCES)
    _, sim = best_match(candidate, labels)          # TỰ KIỂM không vô tình bịa mới
    if sim >= tau_a:
        candidate = random.Random(hash(element) + 1).choice(FLOOR_SENTENCES)
    return candidate
```

Thay thế placeholder `"(describe) {el}"` chỉ khi build **file SFT train**; logic chấm-điểm (`dg1_pa2_score.py`) giữ nguyên, không đụng.

### 2.7. Render target + prompt kiểm soát biến

```python
STUDENT_USER_PROMPT = 'Write step-by-step instructions for a person to follow on their phone, to: "{q}"'
# KHÔNG có câu "don't invent" — khác GEN_PROMPT của teacher, đây là điểm mấu chốt
```

Dùng **giống hệt** ở 3 chỗ: (a) vế human trong SFT record, (b) prompt eval-có-VH, (c) prompt eval-không-VH — bất biến để không ai cãi kết quả đến từ đổi prompt.

### 2.8. Seed từ AndroidControl (dùng CHÍNH — hiệu chuẩn matcher, an toàn nhất)

Lấy ~100-120 step `click`/`long_press` từ episode **ngoài** 237-app DG2 eval → suy tên-nhãn-thật từ a11y-tree bbox chứa `(x,y)` gold → cặp (tên model đoán, tên gold) → báo P/R + Cohen's κ của nomic τA=0.55, rẻ hơn gán tay thủ công vì nhãn có sẵn từ gold. Làm bước này **trước hết**, ưu tiên hơn dùng AndroidControl làm slice SFT phụ (optional, làm SAU khi có pilot MobileViews-only).

### 2.9. SCHEMA DỮ LIỆU CUỐI CÙNG (LLaMA-Factory, ShareGPT + cột images)

**File 1 — `harness/dg3_out/sft_train.json`:**
```json
{
  "id": "mv__aucommixfm4sss_s1__q0",
  "conversations": [
    {"from": "human", "value": "<image>\nWrite step-by-step instructions for a person to follow on their phone, to: \"How do I turn on notifications for new episodes?\""},
    {"from": "gpt", "value": "1. Tap \"Settings\"\n2. Tap \"Notifications\"\n3. Look for the option on this screen that matches what you need for this step, and tap it.\n4. Toggle \"New episode alerts\""}
  ],
  "images": ["mv_train_pool/aucommixfm4sss_s1.jpg"]
}
```

**File 2 — `harness/dg3_out/sft_meta.jsonl`** (audit/leakage-check, tách riêng khỏi file train): `id, source, app, screen, teacher_model, tau_a, n_steps, n_fallback, n_matched, question_idx, split`.

**`harness/dg3_out/dataset_info.json`** — cần khối `tags` tường minh (entry mẫu chính thức LLaMA-Factory `mllm_demo` luôn kèm khối này, thiếu có thể khiến loader không nhận đúng vai trò human/gpt):
```json
{
  "faithful_gui_train": {
    "file_name": "sft_train.json",
    "formatting": "sharegpt",
    "columns": {"messages": "conversations", "images": "images"},
    "tags": {"role_tag": "from", "content_tag": "value", "user_tag": "human", "assistant_tag": "gpt"}
  }
}
```

Ảnh: copy phẳng `harness/dg3_out/images/`; set tường minh `image_min_pixels=256*28*28`, `image_max_pixels=1280*28*28` cho cả train và eval-không-VH.

---

## 3. CẤU HÌNH TRAIN — MỌI HYPERPARAMETER

| Hạng mục | Giá trị chốt | Độ tin cậy |
|---|---|---|
| Rank / alpha / dropout | **r=8, alpha=16, dropout=0.05** | Case study thật xác nhận trực tiếp: **ZonUI-3B** (đúng Qwen2.5-VL-3B, RTX4090) — chỉ 1 nguồn, không phải 2 nguồn hội tụ |
| Target modules | `q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj` (chỉ LLM decoder) | Hội tụ ms-swift/Unsloth/ZonUI-3B |
| Freeze | `freeze_vision_tower: true`, `freeze_multi_modal_projector: true` | Xác nhận tồn tại thật trong `finetuning_args.py` của LLaMA-Factory |
| Learning rate | **1e-4**, cosine, warmup_ratio=0.05 | (ước tính hợp lý nội suy từ case study Qwen2/2.5-VL khác quy mô — KHÔNG phải benchmark riêng cho scale 1.5-3k mẫu) |
| Epoch | **3**, early-stop theo dev-loss/faithfulness held-out-app, giữ best checkpoint | (ước tính hợp lý — dữ liệu nhỏ, overfitting là rủi ro thật hơn underfitting) |
| Batch × grad-accum | T4: `batch=1, accum=16`; L4: `batch=1-2, accum=8`; A100: `batch=2-4, accum=4-8` | Effective batch 8-16 (ước tính, cần đo pilot) |
| Precision | 4-bit NF4 base + **fp16 trên T4** (Turing, không có bf16 tensor-core) / **bf16 trên L4-A100** | Kiến trúc phần cứng đã công bố |
| Quantization | **QLoRA 4-bit mặc định** | Colab không đảm bảo GPU ≥L4 |
| image_min/max_pixels | **256×28² – 1280×28²** (200.704 – 1.003.520 px) | Set tường minh để khớp dải khuyến nghị Qwen (LLaMA-Factory có default riêng ~589.824, không phải default-hỏng 12,8M của raw HF) |
| Loss masking | `train_on_prompt: false` (mặc định LLaMA-Factory) | Chỉ tính loss trên assistant turn |

**File YAML mẫu** (`harness/train_config.yaml`):
```yaml
model_name_or_path: Qwen/Qwen2.5-VL-3B-Instruct
image_min_pixels: 200704
image_max_pixels: 1003520
trust_remote_code: true

stage: sft
do_train: true
finetuning_type: lora
lora_rank: 8
lora_alpha: 16
lora_dropout: 0.05
lora_target: q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj
freeze_vision_tower: true
freeze_multi_modal_projector: true
quantization_bit: 4
quantization_method: bnb

dataset: faithful_gui_train
template: qwen2_vl        # dùng chung cho Qwen2-VL và Qwen2.5-VL
cutoff_len: 2048
train_on_prompt: false

output_dir: /content/drive/MyDrive/thesis_ckpt/qwen25vl3b_faithful_lora
save_steps: 50             # ~10-15 phút wall-clock — lưu THƯỜNG XUYÊN
save_total_limit: 3
resume_from_checkpoint: auto

per_device_train_batch_size: 1
gradient_accumulation_steps: 16    # đổi 8 nếu chắc chắn L4/A100
learning_rate: 1.0e-4
num_train_epochs: 3.0
lr_scheduler_type: cosine
warmup_ratio: 0.05
bf16: false        # true nếu GPU=L4/A100, rẽ nhánh tự động đầu notebook
fp16: true
gradient_checkpointing: true

val_size: held_out_by_app    # split thủ công theo APP, KHÔNG dùng val_size random-row mặc định
eval_strategy: epoch
```

**Bắt buộc train HAI bản** (xem §5 vì sao Student-RAW không còn optional):
1. **Student** — SFT trên data đã lọc (bước 2.6).
2. **Student-RAW** — SFT trên data BASE gốc chưa lọc, cùng hyperparameter, cùng train_apps.

**Ước tính wall-clock:** (chưa có nguồn xác nhận trực tiếp — cần đo thực tế ở smoke-test) nội suy từ case study nhẹ hơn (~1.250 mẫu/10 epoch≈3h, cấu hình r=4/2 module): ~2.000 mẫu × 3 epoch trên T4/L4 rơi vào khoảng vài giờ đến dưới 1 ngày/lần train.

---

## 4. HẠ TẦNG COLAB

**Gói:** Colab Pro ($9.99) tuần 1 (smoke-test) + tuần 5-7 (dự phòng) → nâng **Colab Pro+ ($49.99)** đúng tuần train chính (tuần 2-4) — lý do chính là **chạy nền chống ngắt phiên** (làm solo, không canh máy 24/7), không phải thiếu VRAM/CU.

**GPU tier:** ưu tiên L4 (24GB, margin gấp đôi cho phép tăng max_pixels đọc rõ chữ nút nhỏ); T4 (16GB) đủ dùng dự phòng; **không cần A100**.

### 4.1. Chống ngắt phiên (checklist bắt buộc)
1. Mount Drive, `output_dir` nằm trên Drive (VM Colab xoá khi ngắt phiên).
2. Rẽ nhánh `fp16`/`bf16` tự động theo `torch.cuda.get_device_name()` đầu notebook.
3. `save_steps=50` + `save_total_limit=3`, `resume_from_checkpoint=auto`.
4. Copy checkpoint local→Drive có retry (gotcha đã biết: ghi Drive thất bại nếu mất kết nối giữa lúc lưu).

### 4.2. Export sau train — rủi ro GGUF export

⚠️ **Rủi ro thực tế:** `save_pretrained_gguf` của Unsloth cho Qwen2.5-VL có lỗi thật đang tồn đọng (TypeError khi convert). Kế hoạch "merge→GGUF→eval free trên Ollama" **không còn coi là chắc ăn**.

**Phương án chính + 2 dự phòng, TEST SỚM đầu tuần 4** (ngay khi có checkpoint LoRA đầu tiên, không đợi tuần 5 mới phát hiện lỗi):
- Chính: `save_pretrained_gguf` → nếu thành công, eval-không-VH chạy free trên Ollama CPU local.
- Dự phòng A: giữ adapter LoRA dạng safetensors (`save_pretrained_merged`) → chạy inference held-out ngay trên Colab GPU thêm ~1-2 giờ.
- Dự phòng B: convert thủ công qua llama.cpp's `qwen2-vl-surgery.py`.

Timeline tuần 5-7: có thể cần thêm ~1-2 giờ Colab GPU dự phòng nếu GGUF export thất bại (vẫn trong ngân sách Pro thường).

### 4.3. Timeline theo tuần

| Tuần | Việc | Hạ tầng | Gói |
|---|---|---|---|
| 1 | Freeze split app · mở rộng pool MobileViews · sinh câu hỏi · teacher BASE (API) · matcher+rewrite → sft_train.json · smoke-test train 20 mẫu | Chủ yếu local; Colab ~30 phút | Pro (T4) |
| 2 | Full SFT run Student (data lọc) + bắt đầu Student-RAW (data thô) | Colab GPU ~4-6h (ước tính) | **Pro+** |
| 3 | Tune/debug, hoàn tất cả 2 run tới hội tụ | Colab GPU ~4-6h (ước tính) + buffer | Pro+ |
| 4 | **Test export GGUF SỚM** (đầu tuần) · merge · chốt checkpoint | Colab GPU ~2-4h buffer | Pro+ (có thể huỷ sớm nếu xong) |
| 5-7 | Eval held-out-app (student vs base vs student-RAW) · chấm 3-cơ-chế · thống kê | Local Ollama CPU (nếu GGUF ok) hoặc +1-2h Colab dự phòng | Không bắt buộc / Pro nếu cần |
| 8-10 | Viết luận văn | — | — |

**Ngân sách tổng:** ~$70-100 (Teacher API $1-20 + LLM-judge local free (llama3.2 qua Ollama) + Colab Pro/Pro+ ~$60-70), khớp cận dưới ước tính CLAUDE.md "$100-150".

### 4.4. Ước tính CÔNG-SỨC quy ra ngày-làm (bổ sung 2026-07-12, giả định 10h/ngày)

> Bảng §4.3 là lịch theo TUẦN (part-time, có buffer). Bảng này quy ra **số ngày làm việc tập trung 10h/ngày** để trả lời câu hỏi "làm liên tục thì mất bao lâu". Cách tính giờ Colab: lúc GPU train (3–6h/lần) KHÔNG phải ngồi canh → chồng lấn với viết script/prep data bước sau, hoặc để chạy qua đêm; nên tính theo **wall-clock ngày-làm-việc thực tế** (train chạy nền), KHÔNG cộng cứng "giờ người + giờ GPU" (đếm trùng).

**Mô hình MỘT MÀN (lõi luận văn):**

| Giai đoạn | Việc | Ngày (10h) |
|---|---|---|
| Data pipeline | freeze split · tải+lọc MobileViews · sinh câu hỏi · teacher BASE · matcher+viết-lại · đóng gói · hiệu chuẩn matcher | ~4–6 |
| Train | dựng Colab/LLaMA-Factory (lần đầu hay vướng) · smoke-test 20 mẫu · train Student + Student-RAW · debug/train lại · test GGUF export | ~3–5 |
| Eval | viết eval-tắt-VH · chạy Tier 1+Tier 2 · chấm 3 cơ chế · thống kê (sign-flip/MDE) · đo hữu-ích | ~3–4 |
| **Cộng một-màn** | | **~10–15 ngày** |

**Mô hình NHIỀU MÀN (bộ sắp-thứ-tự học-được — TUỲ CHỌN, làm sau, cho bài FAIR):**

| Việc | Ngày (10h) |
|---|---|
| Script dựng cặp-pairwise từ gold + tải ảnh AndroidControl + cổng chống-leak | ~1.5–2 |
| Smoke + train 1–2 lần (tái dùng hạ tầng nên nhanh; nhãn FREE từ gold, ~$0 API) | ~1–1.5 |
| Eval: độ-đúng-thứ-tự vs Copeland + cổng K-pair | ~1.5–2 |
| **Cộng nhiều-màn** | **~5–6 ngày** |

**Tổng (10h/ngày):**

| Kịch bản | Ngày |
|---|---|
| Lý tưởng (chạy trơn) | **~15–21 ngày** |
| Thực tế (+30–40% ma sát: cài môi trường, OOM, Colab rớt phiên, lỗi GGUF, train lại) | **~21–28 ngày ≈ 3–4 tuần** |

**Lưu ý:** (1) chưa tính viết luận văn (thêm ~10–15 ngày). (2) Nhiều-màn là TUỲ CHỌN ngoài đường-găng <3 tháng — chỉ cần một-màn cho luận văn thì **~10–15 ngày lý tưởng / ~14–21 ngày thực tế**. (3) Mẹo: xếp lệnh train chạy **qua đêm** → giờ GPU thành wall-clock miễn phí, kéo tổng ngày-người về gần mức lý tưởng. (4) Chi phí thêm cho nhiều-màn ~$0–20 (thực tế ~$10) — xem `report/KE_HOACH_2_BAI_BAO.md` §3.

---

## 5. GIAO THỨC ĐÁNH GIÁ TRỤ CHÍNH (pre-register)

### 5.1. Split app (18 train / 12 test, KHÔNG phải 80/20)

Lý do 60/40: bộ 30-app là bộ DUY NHẤT đã qua gate K1 (verify recall VH) → duy nhất tin cậy để CHẤM faithfulness; khối lượng train bù được từ pool mở rộng 231K dòng ngoài. G=12 (test) nằm an toàn trong vùng wild/sign-flip bootstrap đã validate cho coverage tốt, tăng gần gấp đôi power so với G=6.

Diễn giải ngưỡng G nhỏ: literature cluster-robust cổ điển (không bootstrap) cảnh báo G nhỏ hơn ~40-50; wild/sign-flip bootstrap (Cameron-Gelbach-Miller 2008; Canay-Santos-Shaikh 2021) khắc phục xuống G rất nhỏ (một số mô phỏng ổn tới G≈5-10) — G=12 an toàn trong vùng này, "30" KHÔNG phải ngưỡng cứng có nguồn trực tiếp.

Cách chia: greedy number-partitioning theo số-màn/app + `random.seed()` cố định, commit git TRƯỚC khi chạy generation/training. Trước khi chốt 12-app-test cuối: chạy `dg1_vh_coverage.py` riêng trên ứng viên, loại/hoán app có recall bất thường thấp.

**Bổ sung bước chống leak:** khi mở rộng pool train ngoài 30-app: **bắt buộc dedup theo package-name/app-id** giữa toàn bộ pool mở rộng (~231K dòng) và 12 app test — không chỉ trong phạm vi 30-app đã curate. Chạy script kiểm tra intersection rỗng, log kết quả, coi là một phần mốc pre-registration.

### 5.2. Hai tầng thực nghiệm (BẮT BUỘC tách, theo verdict §0)

- **Tier 1 (lưới an toàn, gần chắc dương):** Student (SFT trên data lọc) vs Student-RAW (SFT trên data thô), đo khi VH **VẪN CÓ** lúc suy luận. Lặp đúng mẫu hình đã chứng minh nhiều lần (CapFilt/KnowAda/VGA, chỉ khác domain) → rủi ro null thấp, tự nó đủ thoả "có model tự train + hiệu ứng đo được".
  **Ngưỡng đậu/rớt Tier 1 (pre-register CÙNG lúc với Tier 2, vì trước bản vá 2026-07-12 mục này từng bị bỏ trống — thiếu ngưỡng số thì "báo cáo độc lập" không có tiêu chí PASS để giám khảo kiểm):** đo trên đúng 12 test-apps dùng chung với Tier 2 (để hai tầng so sánh được), test = exact sign-flip G=12 (§5.4) trên `d_j = f_student_i − f_studentRAW_i`. PASS khi CI 95% của Δ=mean(f_student−f_studentRAW) nằm hoàn toàn trên 0 — KHÔNG cần thêm điều kiện (B) kiểu Tier 2, vì Tier 1 không có rủi ro null theo thiết kế nên chỉ đòi ý nghĩa thống kê là đủ. Nếu Tier 1 cũng null: dừng lại, xem lại toàn bộ pipeline lọc trước khi diễn giải Tier 2 (tín hiệu nghiêm trọng, xác suất thấp theo mọi tiền lệ đã tra).
- **Tier 2 (trụ rủi ro, câu hỏi mới thật):** Student vs Teacher-BASE (gpt-4o-mini gốc), đo khi **TẮT HẲN VH** lúc suy luận, held-out theo app. Đây là câu hỏi chưa ai hỏi — có thể null.
- **Báo cáo 2 tầng ĐỘC LẬP** trong luận văn — để null ở Tier 2 không kéo sập kết luận của Tier 1.
- Lý do nâng Student-RAW thành bắt buộc (không phải optional): đây là nhánh DUY NHẤT tách bạch được "cải thiện nhờ lọc-VH" khỏi "cải thiện nhờ SFT/domain-adaptation nói chung". Thiếu nhánh này, PASS ở Tier 2 không quy kết được nguyên nhân. Nếu ngân sách buộc phải bỏ: hạ cấp diễn giải PASS xuống "chưa tách bạch được lọc-VH khỏi SFT-domain nói chung", ghi rõ giới hạn.

### 5.3. Đo faithfulness không-gold (3 cơ chế, khác matcher-lọc)

1. Trích tên nút được nhắc trong câu trả lời.
2. **Cơ chế 1 — bge-m3:** cosine-sim với nhãn VH của đúng màn (VH CHỈ dùng lúc CHẤM). τB hiệu chuẩn RIÊNG (không lấy lại τA=0.55 của nomic), 80-120 cặp gán tay → báo P/R + Cohen's κ, freeze.
3. **Cơ chế 2 — LLM-judge khác họ:** llama3.2 qua Ollama local (free), prompt nhị phân CÓ/KHÔNG.
4. **Cơ chế 3 — token-overlap** (fuzzy string match).
5. Gộp: "bịa" = đa số 3 cơ chế đồng thuận không-khớp; báo thêm độ đồng thuận liên-cơ-chế.
6. Faithfulness màn = 1 − (lượt-nhắc-bịa / lượt-nhắc-nút), tính riêng student/base/student-RAW trên cùng màn/câu hỏi. Kèm %fallback + silent-error-rate.

### 5.4. Thống kê — Exact sign-flip test (G=12 đủ nhỏ để enumerate)

Trích đúng: Canay, I.A., Santos, A., & Shaikh, A.M., *"The Wild Bootstrap with a Small Number of Large Clusters"*, Review of Economics and Statistics 103(2):346-363, 2021.

```python
d_j = mean_{i in app_j}(f_student_i - f_teacher_i)    # j=1..12, gộp theo Cameron & Miller (2015) JHR 50(2):317-372
t_obs = d.mean() / (d.std(ddof=1) / sqrt(12))

# EXACT: liệt kê toàn bộ 2^12=4096 tổ hợp dấu (đủ nhỏ, không cần Monte Carlo xấp xỉ)
for signs in itertools.product([1, -1], repeat=12):
    ...  # t_flip
p_value = mean(abs(null_stats) >= abs(t_obs))
# CI 95% bằng test-inversion trên chính phân phối exact đó
```

Dùng exact khi G≤~13 (enumerate hết được); dùng wild-bootstrap Rademacher B=9999 khi G lớn hơn (như đã chốt cho DG2).

### 5.5. MDE / Power (bắt buộc trước khi pre-register ngưỡng)

```
MDE = (t_{0.025,df=11} + t_{0.20,df=11}) × SD(d_j) / sqrt(12) = 3.077 × SD(d_j)/sqrt(12)
```

SD(d_j) không ước lượng chỉ từ Var(f_teacher) một mình — dùng cận trên thận trọng `SD(d) ≈ sqrt(Var(f_teacher) + Var(f_student_proxy))` (giả định độc lập) khi có pilot/checkpoint sơ bộ. Quy trình: chạy pilot free (chấm f_teacher trên vài app trong 30-app, chưa cần student) → tính MDE thật, tái ước lượng khi có checkpoint student đầu tiên.

Ví dụ minh hoạ CHỈ để hình dung (SD giả định≈0.15, PHẢI thay bằng SD thật): MDE ≈ 0.133 → thiết kế chỉ phát hiện được chênh lệch ≥~13pp ở power 80%; nếu MDE thật >15-20pp, cân nhắc tăng G test (15/15) TRƯỚC khi commit pre-reg.

### 5.6. Ngưỡng đậu/rớt (pre-register TRƯỚC khi chạy test_apps)

**(A) Ý nghĩa thống kê:** CI 95% của Δ=mean(f_student−f_teacher) nằm hoàn toàn trên 0.

**(B) Ý nghĩa thực tế:** Δ_test ≥ 0.5 × Δ_train. **Định nghĩa DUY NHẤT của Δ_train (chốt 2026-07-12, sửa vì bản trước gây mâu thuẫn với report/54):** Δ_train = Δ đo bằng ĐÚNG cùng công thức và ĐÚNG cùng điều kiện tắt-VH-lúc-suy-luận như Δ_test (so Student vs Teacher-BASE), chỉ khác là tính trên **18 TRAIN-apps** thay vì 12 TEST-apps. (Bỏ định nghĩa cũ "mức cải thiện trong-phân-phối, số sơ bộ CLAUDE.md §6" — số đó là kết quả sơ bộ của pipeline-prompting CŨ, đo ở điều kiện VH-còn-lúc-suy-luận, KHÔNG cùng đơn vị so sánh với Δ_test nên không dùng được làm mẫu số.) Ngưỡng 0.5 là construction tự đề xuất, khai rõ trong luận văn không phải số lấy từ literature.

| Kết cục | Điều kiện | Diễn giải |
|---|---|---|
| PASS đầy đủ | (A)+(B) đúng | Nội tại hoá thật, tổng quát hoá đáng kể sang app mới |
| PASS một phần | (A) đúng, (B) sai | Nội tại hoá có ý nghĩa nhưng suy giảm mạnh — vẫn existence-proof có giá trị |
| NULL | CI chứa 0 hoặc Δ_test≤0 | Báo trung thực kèm MDE — giới hạn tổng quát hoá đáng công bố (khung negative-results), KHÔNG tự động lùi về "chỉ lắp ráp công cụ" nếu đóng góp lọc-VH (Tier 1) vẫn đứng vững độc lập |

Cả ba kết cục viết sẵn trước khi nhìn số — cả ba đều "đậu" theo khung negative-results (nền: NeurIPS 2021 Pre-registration Workshop, PMLR v181 — xem §7).

---

## 6. DANH SÁCH RỦI RO KỸ THUẬT CÒN LẠI + CÁCH NÉ

| # | Rủi ro | Cách né |
|---|---|---|
| 1 | Shard MobileViews đoán sai tên → 404 khi fetch | Dùng đúng tên `MobileViews_300000-400000.parquet` / `MobileViews_400000-522301.parquet`; hạ kỳ vọng pool xuống ~231K dòng (không phải ~600K) |
| 2 | `dataset_info.json` thiếu khối `tags` → loader không nhận đúng vai trò human/gpt | Thêm tường minh khối `tags` |
| 3 | T4 16GB có thể vẫn sát VRAM nếu tăng max_pixels/batch | QLoRA 4-bit mặc định; hạ max_pixels xuống 768×28² nếu pilot vẫn OOM |
| 4 | GGUF export Qwen2.5-VL qua Unsloth có lỗi thật đang tồn đọng | Test export SỚM đầu tuần 4; có 2 dự phòng (LoRA safetensors + inference Colab GPU; hoặc convert thủ công qwen2-vl-surgery.py) |
| 5 | Colab Pro/Pro+ không đảm bảo GPU cố định kể cả trả phí | Luôn kiểm `nvidia-smi`/`torch.cuda.get_device_name()` đầu phiên, rẽ nhánh dtype tự động |
| 6 | Ghi checkpoint vào Drive có thể thất bại giữa chừng | Lưu local trước, copy có retry + assert file tồn tại sau copy |
| 7 | Pool train mở rộng (~231K dòng) có thể vô tình chứa lại app trong 12-app-test ở screen khác → rò rỉ ngầm | Dedup tường minh theo package-name/app-id, assert intersection rỗng, log trước khi train |
| 8 | MDE bị đánh giá thấp giả tạo nếu chỉ dùng Var(f_teacher) làm proxy | Dùng cận trên thận trọng SD(d)≈sqrt(Var(f_teacher)+Var(f_student_proxy)) |
| 9 | Nếu bỏ Student-RAW (vì ngân sách), không tách bạch được nguyên nhân cải thiện | Nâng Student-RAW thành bắt buộc; nếu buộc bỏ, hạ cấp diễn giải PASS + ghi rõ giới hạn |
| 10 | rank r=8 chỉ có 1 case study xác nhận trực tiếp đúng Qwen2.5-VL-3B | Ghi rõ trong luận văn: r=8/alpha=16 là điểm khởi đầu hợp lý cần validate bằng dev-loss, không phải trị số "đã chứng minh tối ưu" |
| 11 | Quy mô ~200 app mới có lấy đủ từ 2 shard mới hay không — chưa chạy thử | Cần pilot `SCAN_CAP` lớn hơn trước khi cam kết số 200 |

**Toàn bộ kế hoạch trên chưa chạm bất kỳ lệnh gọi API/GPU thật nào** — mọi bước ✱ (tốn API/Colab) đã đánh dấu, cần hỏi user trước khi chạy thật, đúng nguyên tắc chi tiền CLAUDE.md §8.

**File/script liên quan (đường dẫn tuyệt đối `/mnt/d/Master/Thesis/`):**
- Tái dùng nguyên: `harness/aloha_match.py`, `dg1_pa2_score.py`, `dg1_independent_score.py`, `dg1_run.py`, `dg1_questions.py`, `dg1_data.py`, `dg1_vh_coverage.py`, `scan_androidcontrol.py`, `dg2_sample.py`, `_http.py`, `_apikey.py`, `kept_screens_final.json`, `dg2_episodes.json`.
- Cần viết mới: `harness/dg3_freeze_split.py`, `harness/fetch_mv_expand_train.py` (sửa từ `fetch_mv_expand.py`, xem §2.2 — KHÔNG phải tái dùng nguyên vì cần thêm exclude-list + dedup perceptual-hash), `harness/dg3_train_questions.py`, `harness/dg3_rewrite_fallback.py`, `harness/dg3_render.py`, `harness/dg3_eval_no_vh.py`, `harness/train_config.yaml`, `harness/dg3_out/dataset_info.json`.
- Tham chiếu quyết định: `report/48_dataset_selection.md`, `report/50_deepresearch_model_centric.md`, `report/52_debate_tinh_moi_faithful_distillation.md`.

---

## 7. VERDICT ĐẦY ĐỦ: "ĐỦ NGƯỠNG THẠC SĨ CHƯA"

### 7.1. Kết luận thẳng

**ĐỦ-CÓ-ĐIỀU-KIỆN.** Cả 4 góc giám khảo (advisor-literal, academic-rigor, feasibility-risk, comparison-typical) đều ra cùng verdict, không góc nào nói "đủ" thẳng và không góc nào nói "chưa đủ". Vòng verify-lại bắt được một số chi tiết trích dẫn bị bịa/gán sai nguồn ở vòng research đầu (đã lọc ra khỏi kế hoạch này) — nhưng không verify nào lật ngược chính verdict. Khung lập luận cốt lõi (2 điểm tính-mới sống theo report/52, model tự train thật, thiết kế thống kê phù hợp quy mô G nhỏ, tiền lệ chấp nhận null ở venue ML chính danh — NeurIPS 2021 Pre-registration Workshop/PMLR v181) đứng vững qua verify.

Chuẩn luận văn thạc sĩ (theo nghiên cứu thu thập, ví dụ Rutgers CS degree requirements, hướng dẫn Auckland/UIC, và Thông tư 23/2021/TT-BGDĐT của Bộ GD&ĐT — "đóng góp về lý luận, học thuật HOẶC phát triển công nghệ, đổi mới sáng tạo") KHÔNG đòi hỏi vượt SOTA, KHÔNG đòi hỏi mức mới ngang tiến sĩ, và chấp nhận đóng góp dạng "constructive/technological" (công cụ, kỹ thuật, mô hình) ngang hàng với đóng góp lý luận thuần.

### 7.2. Việc cần làm thêm để đạt ĐỦ

**(a) Tách tường minh 2 tầng thực nghiệm** — đã đưa vào §5.2 ở trên, đây là thay đổi quan trọng nhất so với kế hoạch trước khi có debate này.

**(b) Pre-register thật trước khi chạy Tier 2:** đóng băng định nghĩa "internalized" vs "surface pattern phụ thuộc bộ lọc ngoài" + ngưỡng đậu/rớt bằng số cụ thể (§5.6) + git commit timestamp trước khi chạy.

**(c) Tính MDE/power TRƯỚC khi full-run** (§5.5) — nếu MDE cho thấy thiếu sức mạnh, mở rộng pool hoặc hạ khung Tier 2 xuống "exploratory".

**(d) Pilot hạ tầng 5-10 app trong 2-3 tuần đầu** — để lộ sớm rủi ro Colab (§6) trước khi cam kết toàn bộ.

**(e) Chủ động trình bày cho thầy, không đợi thầy hỏi lại:**
- Sơ đồ pipeline dán nhãn rõ: hộp nào là "công cụ có sẵn/API" (teacher gpt-4o-mini, matcher nomic-embed, rule viết-lại) vs hộp nào là "model tự train" (student Qwen2.5-VL-3B). Đây là kẽ hở còn sống nhất trong đọc-nghĩa-đen câu "mỗi bước gắn một model" — thầy hoàn toàn có thể hỏi lại nếu không thủ trước.
- Bảng so sánh "khác gì người khác": STaR, KnowAda, VGA, CapFilt (recipe nền) + UI-R1/SE-GUI/GUI-Actor/ZonUI-3B (các bài train Qwen2.5-VL cỡ tương đương nhưng nhắm gold-grounding, không phải no-gold text tự do) — mỗi cái 1 câu "giống ở đâu, khác ở đâu" (xem `report/52` §5 đã có sẵn bảng này).

### 7.3. Rủi ro null ở trụ chính — có sụp không, Plan B

**Có sụp, NHƯNG chỉ nếu không tách tầng.** Rủi ro thật sự nguy hiểm nhất không phải null sạch (null có thể diễn giải như "existence-proof âm", được văn hoá embracing-negative-results hậu thuẫn) mà là **kết quả BẤT ĐỊNH** — CI rộng do G nhỏ. Bất định thì không đóng khung được thành phát hiện gì cả.

**Nếu tách Tier 1/Tier 2 như §5.2: không sụp.** Tier 1 gần như chắc dương (đã có tiền lệ mạnh) và tự nó đủ thoả "có model tự train + hiệu ứng đo được có ý nghĩa" — sàn an toàn tối thiểu.

**Plan B cụ thể (nhỏ, không phá lịch <3 tháng):**
1. Ưu tiên chạy và bank kết quả Tier 1 SỚM (trong ~1 tháng đầu sau pilot hạ tầng) — "bảo hiểm" chính.
2. Nếu Tier 2 null: đóng khung thành phát hiện về giới hạn tổng quát hoá, và **nói trước với thầy về khả năng này ngay từ đề cương**, không đợi có số xấu mới giải thích.
3. Thêm phân tích phụ rẻ, độc lập với kết quả nhị phân: đo faithfulness theo nhiều mức trộn tỉ lệ dữ liệu filtered/raw (dose-response) thay vì chỉ 2 điều kiện nhị phân.
4. Deadline nội bộ cứng (~2/3 thời lượng 3 tháng): nếu tới mốc đó Tier 1 chưa chạy ổn định, tự động hạ Tier 2 xuống exploratory/phụ lục.

### 7.4. Bắt buộc làm trước khi chốt hoàn toàn với thầy

1. Viết lại report/50/43 với cấu trúc Tier 1/Tier 2 tách bạch (§5.2) — đã áp một phần vào report/43, cần rà lại đồng bộ đầy đủ.
2. Chuẩn bị sẵn sơ đồ pipeline dán nhãn + bảng so sánh 7 bài liên quan — mang theo khi gặp thầy.
3. Chạy pilot nhỏ 5-10 app xác nhận Colab/Qwen2.5-VL-3B train được thật trước khi cam kết bằng lời với thầy.
4. Nói thẳng với thầy về khả năng Tier 2 null NGAY TỪ ĐẦU — hành động duy nhất giúp một kết quả null (nếu xảy ra) được đọc như phát hiện khoa học thay vì "lại chỉ lắp ráp công cụ".
