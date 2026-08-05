# BÁO CÁO 12 — RUNBOOK CHẠY THỬ PIPELINE TRÊN 3 DATASET

> **Mục đích:** kế hoạch + quy tắc **chạy thử thực tế** ReOrder-Tutor trên MobileViews / AndroidControl / ScreenSpot (thầy yêu cầu chạy thử). Mọi điều ở đây **đã kiểm trên record THẬT** trong `dataset_samples/` (deep-research 2026-06-24), không phải giả định.
> **Khi mâu thuẫn:** file 05 thắng về *phạm vi/khung*; file 12 thắng về *chi tiết vận hành/format dữ liệu*.

---

## TÓM TẮT 30 GIÂY

- **Pipeline CHẠY ĐƯỢC** trên cả 3 bộ. DG1 + ScreenSpot + Tier A **sẵn sàng** sau khi sửa bẫy toạ độ. **DG2 phải LỌC episode trước** (nếu không, τ-b vô nghĩa).
- **Lỗ hổng lớn nhất (DG2):** nhiều episode có **các màn gần trùng nhau** → xáo trộn rồi xếp lại là bài **suy biến**. *Bằng chứng đo thật:* `ep1` (sửa tiêu đề Keep Notes, 3 bước) — cả 3 màn MAE pixel chỉ **0.5–0.8/255** (gần như giống hệt). Phải thêm **bộ lọc độ-phân-biệt-thị-giác** + loại bước `status`/`wait` + đếm **N theo "màn phân biệt được"** chứ không phải số bước thô.
- **3 bẫy toạ độ phải sửa trong harness** (nếu không → chấm sai mà không báo lỗi): (1) MobileViews field `width/height` = **RÁC**, dùng kích thước ảnh thật; (2) MobileViews `bounds` = **`[[l,t],[r,b]]` lồng** (có thêm `bound_box`="l,t,r,b"); (3) AndroidControl `gold_action` có tiền tố **`!FUNCTIONCALL`** phải strip.
- **Môi trường:** Windows + 1 GPU 24GB **chạy được**; nên dùng **WSL2** cho phần serving (tránh 2 blocker: `flash-attn` không có wheel Windows + vLLM không chạy native Windows).

---

## 1. FORMAT DỮ LIỆU THẬT (đã verify từ `dataset_samples/`)

### 1.1. MobileViews (DG1 — màn-0)
File mỗi màn: `*.jpg` + `*.viewhierarchy.json` (+ `*.uiautomator.xml`).
- VH JSON keys: `state_str, foreground_activity, width, height, views[]`.
- ⚠️ **`width`/`height` trong JSON = RÁC** (mẫu ghi `2340×1080` nhưng ảnh thật `1080×1920`). **→ luôn lấy kích thước từ chính ảnh (PIL `Image.open(...).size`), KHÔNG đọc field này.**
- Mỗi node `views[i]` có: `bounds`, `bound_box`, `text`, `content_description`, `class`, `clickable`, `editable`, `scrollable`, `long_clickable`, `checkable`, `visible`, `enabled`, `child_count`, `temp_id`, `parent`, `children`.
- ⚠️ **`bounds` = `[[left,top],[right,bottom]]` (cặp lồng nhau)**, KHÔNG phải `[l,t,r,b]` phẳng. Có thêm **`bound_box` = chuỗi `"left,top,right,bottom"`** → parse chuỗi này tiện hơn. Toạ độ là **pixel khớp ảnh** (item root = `[[0,0],[1080,1920]]`).
- **Định nghĩa LÁ tương tác** (mẫu số coverage / tập tham chiếu HER): `child_count==0` **VÀ** (`text`/`content_description` ≠ rỗng HOẶC có cờ tương tác). *Đo thật:* 8–11 lá/màn → mẫu số coverage CÓ NGHĨA.

### 1.2. AndroidControl (DG2 ordering + Tier A)
File mỗi episode: `*.episode.json` + `*_stepK.png`.
- Keys: `episode_id, goal, num_steps, steps[]`. Mỗi `step`: `step_id, np` (liên tục 0..k), `active_application, previous_actions, gold_action, screen_w, screen_h, screenshot_file`.
- **`screen_w × screen_h = 1080 × 2400`** (toạ độ click là pixel trong hệ này).
- ⚠️ **`gold_action` = `!FUNCTIONCALL{...json...}`** → phải `re.sub(r'^!FUNCTIONCALL','',s).strip()` rồi `json.loads`.
- **Không gian action (9 loại):** `click{x,y}` · `long_press{x,y}` · `input_text{text}` · `scroll{direction}` · `navigate_home` · `navigate_back` · `open_app{app_name}` · `wait` · `status{goal_status}`.
- **Bước cuối luôn là `status`** (terminal, không phải màn của luồng); `wait` cũng không phải transition. **→ loại `status`/`wait` khỏi tập màn-cần-xếp.**
- Screenshot mỗi step = **màn TRƯỚC khi thực thi gold action** của step đó (cấu trúc N+1: ảnh trước & sau mỗi action) → đủ để suy **cặp BẮT BUỘC** tất định.
- ⚠️ **Cây accessibility (element list + bbox + cờ) CÓ trong FULL dataset** (dạng proto `android_env`, parse ~30–50 dòng) **nhưng KHÔNG nằm trong sample đã trích ở đây** (chỉ có các key liệt kê trên). → **Step-SR + grounding-vs-gold KHÔNG cần** cây này (đã có (x,y) gold); chỉ **coverage + hallucination per-màn** mới cần → parse khi chạy Colab. (Đã verify khả thi: `report/14`.)

### 1.3. ScreenSpot / ScreenSpot-v2 (đối chứng grounding)
File mỗi mẫu: `*.png` + `*.json`. Keys: `file_name, platform, instruction, data_type, data_source, bbox_normalized_[x1,y1,x2,y2], bbox_pixel_[x1,y1,x2,y2], image_size_[w,h]`.
- **Sạch nhất** — có sẵn cả bbox chuẩn-hoá 0–1 lẫn pixel + image_size → point-in-bbox tính ngay.
- ⚠️ **Cảnh báo mirror HF:** các mirror khác nhau dùng format khác (HongxinLi = 0–1 `[l,t,r,b]` vs Voxel51 = pixel `[x,y,w,h]`). **Pin 1 mirror + assert format trong code.** (Bản trong `dataset_samples/` đã chuẩn-hoá đủ cả hai.)

### 1.4. Ba hệ toạ độ — bảng convert (BẮT BUỘC trước point-in-bbox)
| Bộ | Dạng | Hệ | Ghi chú |
|---|---|---|---|
| MobileViews | bbox `[[l,t],[r,b]]` (+`bound_box` "l,t,r,b") | **pixel theo ẢNH** (1080×1920) | KHÔNG dùng field width/height |
| AndroidControl | điểm `(x,y)` | pixel 1080×2400 | strip `!FUNCTIONCALL` |
| ScreenSpot | bbox `[x1,y1,x2,y2]` | có sẵn 0–1 **và** pixel | pin mirror |
→ **Adapter mỗi bộ → 1 hệ chuẩn (đề xuất: normalized 0–1 `[x_min,y_min,x_max,y_max]` + điểm normalized) + assert range(0..1) + 2–3 unit-test/bộ.**

---

## 2. 🔴 SÀNG LỌC EPISODE DG2 (BẮT BUỘC — nếu không, τ-b vô nghĩa)

**Vấn đề (đo thật):** độ phân biệt thị giác giữa các màn phụ thuộc action+nội dung và **thường THẤP**. `ep1` cả 3 màn MAE 0.5–0.8/255 (sửa tiêu đề chỉ đổi vài pixel) → **unorderable bằng thị giác**. `ep3` scroll lại đổi nhiều (MAE 75–80) nhưng `input_text`/`wait` gần trùng (MAE ~3).

**Quy trình lọc (chạy TRƯỚC khi đo τ-b, là một phần cổng KN + KB):**
1. Dựng tập màn-cần-xếp = các screenshot **trừ** bước `status`/`wait`.
2. **Loại episode "màn gần trùng":** tính độ-khác mọi cặp màn liên tiếp (MAE ảnh xám resize, hoặc perceptual-hash). **Pre-register ngưỡng** (sơ bộ đo được: MAE < ~6/255 trên ảnh xám resize 180×360 = "gần trùng"). Episode có BẤT KỲ cặp dưới ngưỡng → **loại** (hoặc gộp màn trùng thành 1).
3. **Đếm KN theo "N màn phân biệt được"**, KHÔNG theo `num_steps` thô. **N-xếp-được thường < num_steps** → N≥5–6 có thể mỏng hơn dự kiến → báo histogram số episode sống sót mỗi N.
4. Loại N≤2 như cũ.

> **Nói với thầy:** DG2 cần bước sàng lọc episode này thì τ-b mới đo đúng *năng lực suy luận trật tự*; không lọc thì con số là nhiễu. Đây là một phần đóng góp phương-pháp-đánh-giá (định nghĩa rõ "episode đo được").

---

## 3. MÔI TRƯỜNG (Windows 10 + 1 GPU 24GB)

**Khuyến nghị: serving model trong WSL2; harness chấm chạy đâu cũng được.**
- **OmniParser V2:** clone + pip (conda py3.12), tải weights `huggingface-cli download microsoft/OmniParser-v2.0`. Fit 24GB dư (~5GB weights, ~0.6–1s/ảnh). **Rủi ro #1 = `flash-attn`** (không có wheel Windows) → WSL2, hoặc wheel prebuilt, hoặc patch Florence-2 `attn_implementation="sdpa"` (flash-attn chỉ cần lúc cài, không bắt buộc runtime). **Cài torch CUDA TRƯỚC** kẻo dính torch CPU-only (chậm 50×). Sanity-check trước trên HF Space `microsoft/OmniParser-v2`.
- **Qwen2.5-VL-7B:** fit 24GB (BF16 ~16GB; có bản **AWQ ~4.5GB** để dư KV-cache). **vLLM KHÔNG chạy native Windows** (kẹt `uvloop`) → **WSL2 + vLLM** (1 server vừa làm generator vừa làm baseline native-grounding), hoặc native Windows dùng **Ollama/transformers**. **Cap `max_pixels` (≈1280·28·28)** để khỏi OOM vì ảnh UI dày.
- **Constrained decode:** vLLM `guided_choice` cho enum ID (hoạt động với VLM vì chỉ mask logit luồng text) **+ luôn kèm vòng validate-and-repair** (constrained ~96–98%, không 100%; preamble reasoning có thể phá `guided_choice`). API GPT-4o: `response_format` json_schema strict + enum (chạy được kèm ảnh; giới hạn ~1000 enum — dùng ID số ngắn). **Enum BẮT BUỘC có `none/abstain`** (recall-miss → tránh ép bịa click).
- **Ngân sách:** GPT-4o ~$2.5/1M in, $10/1M out → vài nghìn ảnh = vài chục USD. Trong $100–300 thoải mái.

---

## 4. KẾ HOẠCH CHẠY THỬ — 4 MỐC CÓ CỔNG

| Mốc | Việc | Đầu ra / DoD |
|---|---|---|
| **M0 — Env** | Dựng WSL2 + OmniParser V2 + Qwen2.5-VL-7B (vLLM) + harness chấm | parse được 1 ảnh trên HF Space; OmniParser chạy GPU <2s/ảnh; Qwen serve OK; enum guided_choice + validate-repair thông |
| **M1 — DG1 smoke** | ~20 màn MobileViews: OmniParser→SoM→Qwen sinh (constrained, có `none`)→resolver→**point-in-bbox + HER + coverage**; ScreenSpot ~50 mẫu làm đối chứng resolver | **bảng số DG1 ra được** (mỗi caption kèm "recall=?"); convert toạ độ 3-bộ qua unit-test; point-in-bbox khớp ảnh |
| **M2 — K1 recall (cổng cứng)** | đo recall OmniParser vs lá VH tương tác trên 30–50 màn | có số recall X%; mọi số grounding đóng khung "conditioned on recall=X%" |
| **M3 — DG2 đúng quy trình** | (a) **lọc episode** (§2) + đếm KN theo N-màn → pool hợp lệ; (b) **rồi mới** đo **τ-b** SELF-ORDER vs ORACLE-ORDER (pairwise+Copeland, có `none`/cycle-resolve) + baseline GOAL-ONLY/VISUAL-ONLY/RANDOM (null empirical theo N); (c) Tier A teacher-forced (Action-Type/Grounding@14% point-to-point, không cần a11y-tree) | histogram N sống sót; τ-b ra số trên pool đã lọc; KHÔNG đo τ-b trước khi lọc |

> **Thứ tự cứng:** M0→M1 chứng minh lõi chạy + metric ra số (đem trình thầy được ngay). M2 cổng recall. M3 chỉ chạy sau khi **lọc episode** xong.

---

## 5. RỦI RO VẬN HÀNH & CÁCH CHẶN (gọn)
| Rủi ro | Chặn bằng |
|---|---|
| MV width/height rác → chấm lệch trục | Dùng kích thước ẢNH; assert bounds ⊆ ảnh |
| `bounds` lồng / `gold_action` có tiền tố | Parser riêng mỗi bộ + unit-test |
| ScreenSpot khác format theo mirror | Pin 1 mirror + assert |
| DG2 màn gần-trùng → τ-b nhiễu | Bộ lọc độ-phân-biệt-thị-giác (§2) + báo episode sống sót |
| N-xếp-được < num_steps → N lớn mỏng | KN đếm theo N-màn phân biệt; thu/gộp mốc N nếu thiếu |
| flash-attn không cài được Windows | WSL2 / wheel prebuilt / patch sdpa |
| vLLM không chạy native Windows | WSL2, hoặc Ollama/transformers |
| torch CPU-only / Qwen OOM ảnh dày | Cài torch CUDA trước; cap `max_pixels` |
| constrained không 100% / recall-miss ép bịa | validate-and-repair + enum có `none/abstain` |

---

## 6. NGUỒN
Format dữ liệu: verify trực tiếp từ `dataset_samples/` (MobileViews `mllmTeam/MobileViews` arXiv:2409.14337; AndroidControl `google-research/android_control` NeurIPS 2024 D&B arXiv:2406.03679; ScreenSpot-v2 OS-Atlas ICLR 2025 arXiv:2410.23218). Env: OmniParser `microsoft/OmniParser` + V2 weights + MS Research blog (0.6s/A100); flash-attn không có wheel Windows (PyPI); vLLM không hỗ trợ native Windows (RFC #14981, uvloop #14813), official path = WSL2 + CUDA-on-WSL (NVIDIA); Qwen2.5-VL-7B model card + AWQ; vLLM structured outputs (`guided_choice`/XGrammar); OpenAI Structured Outputs (enum + vision). Ngưỡng 14% = AITW (NeurIPS 2023, đã verify). *(Chi tiết link xem nhật ký deep-research 2026-06-24.)*
