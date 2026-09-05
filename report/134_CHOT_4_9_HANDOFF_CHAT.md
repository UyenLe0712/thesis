# 134 — CHỐT 4/9/2026 + BÀN GIAO CHO CHAT KHÁC

> **Nguồn:** chép lại từ 8 ảnh chụp màn hình bản gốc viết trên **máy Mac**
> (`/Users/P836901/Documents/Self-learning/thesis/thesis-master/`), giải nén từ
> `My Documents [04-09-2026 20_48].zip` ngày 4/9/2026. Ảnh gốc giữ ở
> `harness/debate_04_09/`. Phần **§14 (Đối chiếu trên WSL)** là phần **thêm mới của máy
> WSL**, không có trong bản Mac.

Đọc file này trước mọi file khác nếu nhiệm vụ là chạy thí nghiệm, viết abstract/full SOICT,
hoặc sửa mã chấm. File này **thắng** `124` (bản kể chuyện), `128` (chốt 30/8), `132` (kế hoạch
1/9), `133` (debate ngay sau G6) về **phương pháp, thước, ngân sách GPU, và lịch còn lại**.

`106_DANG_KY_TRUOC.md` **vẫn thắng** về **ngưỡng đã niêm**: Voronoi primary, một hạt = TRẮNG,
Dương +2,8 pp, MDE ~2,11. Chốt 4/9 **không nới** các ngưỡng đó.

Mã nguồn `harness/` và `runs/*.jsonl` **thắng mọi văn bản** về hành vi thật.

**Ngày chốt:** Thứ Sáu 4/9/2026 (ICT). **Hạn: abstract 9/9 · full 16/9 · khóa số 13/9 12:00 ICT.**

Clone GitHub `thesis-master/` là **disposable**. File sinh (PDF, HTML, zip, canvas dump) **không
ghi vào trong clone** — để `_pdfbuild/`, `_exports/`, `thesis_local_backup_*`.
Git ở `/Users/P836901` là home dir, **không phải** repo luận văn. Repo luận văn: `UyenLe0712/thesis`.

---

## 0. Chat mới cần làm gì (một trang)

**Đã khóa** (không debate lại trừ khi mã/số thô đảo kết luận): thước · constructor menu · giữ
`<sel>` đã train · loss · đúng **một lượt A100 còn lại** · **G6 giữ trượt**.

**Việc thi hành còn lại (thứ tự phụ thuộc):**

0. Kéo artifact Drive; pin hash; **fail-closed nếu thiếu key**. **Sel-B:** `ocr.jsonl` md5
   `a7ddf93d18c060e995afa841f039e343`, `train.jsonl` = 64.567. Prompt `gui_sft_match`
   **byte-identical** với `gui_sel` trên 3.000/3.000. Tên Sel-A/Sel-B dùng để tránh lẫn với
   **Cổng A/B trong `106`**.
1. **T4:** suy luận nốt + `exec(gui_sel/101)` đủ **n = 4.463** (Voronoi gated là số quyết định).
2. **A100 song song:** train `gui_sft_match`/101 (~23–30 h). `start_new_session=True`,
   `save_steps: 100`, cell foreground. **Sel-B trượt → 0 A100 vĩnh viễn cho bài này.**
3. **Sequence-score** length-normalized mọi ứng viên + `none` trên 1.400; **khóa τ trước khi
   nhìn exec đối chứng hoặc 3.062**.
4. **One-look 3.062** (hậu kiểm, **không phải** hold-out đăng ký trước).
5. Suy luận + exec `sft_match`/101 → `Δ_sel` **một hạt, dưới MDE, nhãn exploratory**, **không**
   rule-(w) Dương/Âm.
6. Viết. **Abstract 9/9 chỉ số đã có trên đĩa.** Full 16/9 chỉ nếu đã có exec + artifact truy
   nguyên + Voronoi không bị đảo.

**Không làm trước 16/9:** prune/retrieval/ID · đầu mới · đổi loss · `gui_sel`/202 (mặc định tắt)
· `S1-match` · nới G6 · săn Human 90% · bbox / AITW-OR · lấy nL2 làm headline khi Voronoi trắng.

### 0.1 Artifact và trạng thái hiện tại

- Drive root: `/content/drive/MyDrive/thesis/`.
- Gói train/nhánh theo runbook: `derived.tar.gz` (nguồn `train_ac/train.jsonl` + đúng
  `train_ac/ocr.jsonl`), `branches_sel.tar.gz`, bốn `train_images_p{i}.tar`, source snapshot
  `thesis_rented.zip`; adapter đã train ở `MyDrive/thesis/ckpt/gui_sel_seed101/`.
  Sau bung, **không tin tên gói**: kiểm lại md5/count Sel-B.
- Khi đưa adapter lên Kaggle, lấy **thư mục gốc** (có `adapter_model.safetensors` +
  `adapter_config.json`), **không lấy `checkpoint-*` dở**.
- Kaggle gắn ba input: `thesis-score`, `thesis-sel-infer` (phải chứa đúng test `candidates.jsonl`
  đã pin), `gui-sel-adapter`. Internet ON, T4×2.
- Clone (Mac) **không có** `candidates.jsonl` và train JSON đầy đủ. Trên đĩa chỉ có pred G6 1.400
  + force-273, **chưa có pred full 4.463**. "Suy luận nốt" = 3.063 bước chạm còn lại nếu Sel-A
  chứng minh 1.400 tái sử dụng được; nếu không, **infer lại đủ 4.463**.
- Dựng candidates phải dùng `build_candidates.py --all-steps --max 40`; dựng branch phải truyền
  đúng `--img-prefix`. **Không dựng lại từ OCR khác hash.**
- Chưa có SHA candidates để ghi sẵn: chat thi hành phải tính SHA-256 sau khi khôi phục, ghi
  manifest, rồi pin chính file đó.

---

## 1. Câu trả lời ngắn cho chủ luận văn

**Có.** Sáu quyết định vi mô (M1–M4 phương pháp, E1–E2 thước) đã debate bằng nhiều họ mô hình,
rồi hội đồng tích hợp khóa ngày 4/9. **Không khóa lại trừ bằng chứng mới từ file thô.**

Còn thiếu debate = **chủ yếu thi hành và câu chữ**, không phải thiết kế khoa học (mục 8 dưới).

## 2. Bối cảnh một đoạn

Luận văn: sinh **một câu tiếng Anh** chỉ bước tiếp theo trên ảnh Android (REG trên GUI),
**không tự bấm**. Chấm bằng bộ trỏ độc lập UGround-V1-2B. Backbone: Qwen2.5-VL-3B-Instruct.
Sprint SOICT: nhét **menu ≤40 ứng viên** vào prompt và dạy thẻ `<sel>`.

Luận văn 96 trang **đã đủ scope thạc sĩ**, không cần sprint này. Sprint là thí nghiệm đã đăng ký
+ bài short SOICT. FAIR/VCL đã nộp nội dung khác; **SOICT phải tự đứng**, không tái dùng hiệu
chuẩn thước như đóng góp.

---

## 3. Số đã đo — không trộn gated / ungated

Mọi hàng `exec` dưới đây = `action_ok ∧ toggle_ok ∧ hit_<luật spatial>`, **n = 4.463 bước chạm**
(cặp bootstrap thường n = 4.462). Trong mã, headline chính xác là
`action_ok ∧ toggle_ok ∧ hit_voronoi`. Tập test có 6.958 bước; vuốt/gõ **không** vào mẫu số này.

### 3.1 Gated (được gọi executability)

| luật spatial | Human | MIN-DESC/101 | S1/101 | Base | sàn rỗng n=800 | sai màn n=800 |
|---|---|---|---|---|---|---|
| **Voronoi .14** (primary, đã prereg) | 75,73 | **60,05** | 59,11 | 47,59 | 12,00 | 6,12 |
| nL2 .14 (secondary; nhánh khoảng cách AITW, **không phải AITW đầy đủ**) | 84,09 | 68,32 | 66,92 | 55,28 | 20,12 | 11,62 |
| chữ nhật .14 (`hit_disk` trong code — **không phải đĩa**) | 84,23 | 68,72 | 67,24 | 55,86 | 20,50 | 12,75 |

L2 theo bề ngang (L2W) gated MIN ~65,63 / Human ~82,32 — **không dùng làm hàng báo cáo đã khóa**.
Ungated "chỉ vị trí" chữ nhật Human 84,27 / MIN 69,19 — **cấm gọi executability**.
Toàn bộ 4.463 màn portrait. L2W ⊂ ellipse nL2 ⊂ chữ nhật.

### 3.2 Khớp n=800 (FCE derived, không primary)

Human Vor 74,875 · MIN 59,5 · rỗng 12. nL2 82,875 / 68,375 / 20,125. rect 83 / 68,75 / 20,50.
FCE MIN ≈ 75,55 / 76,89 / 77,20 — **không đủ bất biến để làm thước chính**.

### 3.3 Bootstrap cụm (1.345 episode, n=4.462)

Theo nguồn niêm `106`: MIN−S1 Vor **+0,94**, CI [−0,09, +2,05], p=0,11 (chứa 0). nL2 +1,412
[0,266, 2,577]. rect +1,479 [0,338, 2,632]. MIN−Base ~+12,5–13 pp, CI dương. MDE ~2,11 pp một
hạt. Để claim Dương theo luật khóa cần ~+2,8 trên **trung bình hai hạt**.

### 3.4 AITW official (không chạy, không pretent)

Action type **AND** (`nL2 ≤ .14` **OR** cùng box mở rộng 2,4×, `augment_fraction=1.4`).
Chữ nhật ±14% **không phải AITW**. Hàng nL2 chỉ được gọi **nhánh khoảng cách AITW**.
`nL2 = sqrt(((x_pred-x_gold)/W)^2 + ((y_pred-y_gold)/H)^2)`. Hàng nL2 **hiện chưa có hàm đóng gói
trong `metric_exec.py`**; chat thi hành phải thêm phép tái tính từ raw (hoặc script riêng), đối
chiếu các số §3.1 trước khi dùng.

### 3.5 Trần / phủ

Gold-in-menu vô điều kiện ~71,6%. Trần cơ chế exec ~67,2%. Cap-40: 1.185/4.463. 98,2% tên được
chọn đã nằm trong menu. Named-gold G1/G2 ~96,7 / 91,2.

### 3.6 Lát MIN (chẩn đoán cũ, vẫn đúng)

Lát khai đúng 2.970: MIN 85,2 · người 85,7. Lát khai sai 1.493: MIN 10,0 · S1 25,1 · người 55,9.
Thổi phồng nội sinh 11,50 pp CI [9,40, 13,37].

---

## 4. G6 — TRƯỢT, không mở lại cổng

Adapter `gui_sel`/101 đã train. Cổng: `sel_acc ≥ 63,6%` trên bước HasAns của lát 1.400.

| số | giá trị | ghi chú |
|---|---|---|
| `sel_acc` G6 | **580/1008 = 57,54%** | trượt 6,1 pp; **giữ trượt** |
| đúng toàn bước 1.400 | 888/1400 = 63,43% | không phải cổng |
| force-all đúng toàn bộ | 696/1400 = 49,71% (−13,71 pp) | diagnostic |
| force-all HasAns | 696/1008 = 69,05% (+11,51 pp) | **bẫy thước** |
| force 273 abstain sai | 116/273 = 42,5% | thua mọi ngưỡng cỡ khối |
| over-abstain HasAns | 27,1% | |
| emit `none` | 581/1400 vs 392 true none | |
| commit sai trên NoAns | 84 | |
| recognition : localization | ~34:1 | |
| verb không-tap | 39,6% (abstain sai) vs 2,0% (chọn) | |
| đóng `</sel>` | 1398/1400 | 2 thẻ không đóng: `18410/1`, `18747/9` |
| `conf` | **không có trong pred jsonl** | first-token ≠ full-sequence score |

Lát 1.400: `--limit 1400` trên **2.221 bước chạm đầu** của test — hậu kiểm, đã chạm (G6 + force).
Mọi số trên 1.400 là **dev**.

Phần còn lại: 3.063 bước / 892 episode; **1 episode trùng (1 bước)**; sau loại: **3.062 / 891**.
`report/132`–`133` gọi 3.063 là "hold-out" — **sai thuật ngữ**. Được dùng như **one-look hậu kiểm
sau khi khóa τ**, không phải confirmatory split đăng ký trước. Exec luôn n = 4.463.

**Kỳ vọng 63,7–65,1 đã chết:** giả định đầu chọn đạt cổng; trần cơ chế 67,2; G6 57,5.

---

## 5. Thước đã khóa (E1 + E2)

| vai trò | thước | được phép |
|---|---|---|
| Confirmatory / quyết Δ / headline | **Voronoi gated .14, n=4.463** | luôn |
| Literature secondary | gated nL2 .14 | interval-only; **không cứu Δ Voronoi trắng**; wording "AITW distance clause only" |
| Hàng khớp mã | gated chữ nhật .14 (`hit_disk`) | interval-only; **không gọi AITW** |
| FCE | derived, chỉ n=800 matched | không primary |
| Human ≥90 bằng nới τ | **cấm** | sàn rỗng/sai-màn leo ~31 / ~22 |
| bbox / AITW-OR / point-in-box | **hoãn** đến khi validation riêng | |
| Holm / secondaries cứu primary | **cấm** | |

Thuật ngữ: **mốc câu người dưới dụng cụ / proxy executability**. Không viết "human ceiling 75,7%"
như giới hạn nhận thức.

**Khóa Voronoi trước khi thấy điểm `gui_sel` exec.** Nếu Voronoi 61–63 mà nL2 70–71, **cấm dẫn nL2**.

---

## 6. Phương pháp đã khóa (M1–M4)

**M1 constructor.** Max-40, thứ tự đọc, tên a11y+OCR; merge **cùng tên** overlap only. **Không**
prune, rank, semantic retrieval, ID, merge khác tên. Thiếu key → **fail-closed** (không im lặng
`cands=None`). Pin SHA file candidates/OCR.

**M2 đầu.** Giữ generative `<sel>` trên ckpt hiện có. Force-sel = **diagnostic, không phải hệ
thống**. Readout exploratory: **length-normalized full-sequence score** mọi ứng viên + `none`.
Khóa τ trên 1.400 theo **đúng toàn bộ bước** (không theo `sel_acc`); tie-break ít false `none`.
One-look 3.062. In cả khi τ=∞ thắng. Optional `p_none` diagnostic. **First-token không đủ để gọi
Devlin.**

### 6.1 Hợp đồng sequence-score (đủ để chat khác implement)

Với prompt cố định (x), mỗi phương án (c) là **toàn bộ span chọn**. Candidate phải lấy nguyên văn
từ artifact và render bằng `build_candidates.block_str` / `build_sel_data.sel_str`; **không tự
format lại tên/tọa độ**:

`<sel>{candidate name} <point>x,y</point></sel>` hoặc `<sel>none</sel>`.

Teacher-force từng span, chỉ cộng log-probability của token thuộc span đó (không cộng prompt,
không cộng câu hướng dẫn):

`s(c|x) = sum_t log p(token_t | x, token_<t) / số_token(span_c)`

Gọi `c* = argmax` trên các ứng viên thật; margin `m = s(c*) − s(none)`. Emit `c*` khi `m > τ`,
ngược lại emit `none`. Quét τ **chỉ trên 1.400**, gồm cả luật null "giữ greedy hiện tại"; chọn
theo **đúng toàn bộ 1.400**, hòa thì ít false-`none` hơn. Nếu lift tốt nhất < khoảng 18/1.400
(~1 binomial SE), **khóa luật null**. In toàn đường cong kể cả khi null thắng.

Yêu cầu thi hành: probe 50 bước; batch teacher-forcing; output JSONL có key, từng score, length
token, margin, prediction; chunk + resume; **cùng tokenizer/model/adapter với G6**. Không force-sel
trong hệ thống chính. `p_none` first-step nếu chạy chỉ là diagnostic nhị phân, không phải xác suất
candidate. **Hợp đồng này thay first-token τ trong `133`.**

**M3 train còn lại.** Uniform assistant-token CE, **cùng yaml** (chỉ đổi `dataset` / `seed` /
`output_dir`). **Không** weight loss, oversample, focal, split-none, unfreeze vision.

**M4 GPU.** Đúng **một A100**: `gui_sft_match`/101, prompt byte-identical, target chỉ câu.
`gui_sel`/202 **mặc định tắt**. `S1-match` sau 16/9 (S1 cũ lệch 2 epoch + cutoff 2560 → **so bắc
cầu cấm**). Δ_sel một hạt, dưới MDE → **trắng theo thiết kế**; không verdict bốn-ô Dương/Âm.

**Không claim:** công của khối ứng viên (thiếu `S1-match`). Chỉ Δ_sel vs `sft_match` nếu train xong.

**Future (≤ ~200 chữ, 0 GPU trước 16/9):** factored `action → has_candidate → candidate →
sentence`; tách nhãn `none` (nontap vs touch-không-tên); listwise K+2 là arm đăng ký **sau**.
Không rebuild data.

---

## 7. Lịch ICT và cổng giết

A100 và T4 **không tranh GPU**. Đường găng = **trông Colab** (cell ~90 phút; tiền lệ 8 crash /
2 lượt S1).

| khi | việc |
|---|---|
| **4/9 tối** | Drive pull; commit freeze M1 + amendment "2 A100 → 1 control" + **pre-register τ** (định nghĩa score, split, tiêu chí, single-look) **trước** scoring pass |
| **5/9 AM** | **Sel-A:** deterministic replay đúng manifest 1.400 bằng adapter + code/env khôi phục; `raw` phải **byte-identical 1.400/1.400** (nếu không thì không tái dùng G6 và **chết dòng τ**). G6 cũ không lưu prompt nên **không được tuyên bố "prompt hash khớp"** nếu chưa có replay. **Sel-B:** ocr md5 + train 64.567 + prompt match 3.000/3.000. Không lẫn với Cổng A/B của `106` |
| 5–6/9 | T4: infer nốt + exec 4.463 |
| 6/9 | Launch A100 sau pre-flight 7 mục |
| 6–7/9 | T4: sequence-score 1.400 (chunk + resume). `report/133` ghi ~2 h là **lạc quan** — pred không có logprob từng ứng viên |
| **8/9** | **Đóng băng abstract.** Chỉ số trên đĩa: 57,54 · 63,6 · 63,43 · 27,1 · 42,5 · 34:1 · 39,6/2,0 · **+11,51/−13,71**. **Không** exec, τ, control nếu chưa có file |
| **9/9** | **Nộp abstract.** Rồi T4 infer+exec control nếu adapter sẵn |
| 10/9 | **Khóa τ** (cổng F) |
| 11/9 | One-look 3.062. Trước đó verify overlap episode (đã đo: 1 bước) |
| 12–13/9 | Viết. **Khóa số 13/9 12:00**; job còn chạy thì bỏ |
| 14/9 | Audit prosa: mọi số → file trên đĩa |
| **15/9 18:00** | **Nộp**, dư một ngày. FAIR-result check tối đa 1 giờ |

**Kill:** control chưa ≥60% của 4.036 bước train (≈2.422 bước, đọc từ global step/log) tới **8/9
12:00** → **giết**, không dùng adapter dở. **Sel-A trượt** → chết dòng τ, bài = G6 + force-sel +
exec. **Sel-B trượt** → **0 A100**.

**Pre-flight A100 (bảy dòng đều xanh):** dataset đúng `gui_sft_match`; chỉ các khóa cho phép đổi;
không `max_steps`; output dir rỗng nếu lượt mới / có checkpoint nếu resume; 64.567 mẫu; cutoff
3.072 + 1 epoch; ảnh đầu tiên mở được. Dùng LLaMA-Factory commit `c4e09c7cbe18…`. Giữ
`start_new_session=True`, log local unbuffered, cell giám sát foreground, `save_steps: 100`;
không append log trực tiếp qua Drive FUSE.

**Giờ (ước, không đo):** exec ~5,6 h T4; infer nốt ~4 h; sequence-score 1.400 ~5,6–11 h; 3.062
~12–24 h; `sft_match` ~23–30 h A100; infer+exec control ~11 h T4. **Gói 6 lượt cũ (~69 h A100) đã
hủy.**

Runbook `colab_train_sel.md`, `kaggle_infer_sel.md` và comment đầu `train_config_sel.yaml` vẫn
nói "sáu lượt / hai hạt" — **bỏ qua phần phạm vi đó**, chỉ dùng ô kỹ thuật. Nguồn phạm vi thắng
là file `134`.

---

## 8. Chưa debate / chưa xong — chat kia không được tự khóa giúp

Đây **không phải lỗ thiết kế thước/phương pháp**. Là việc vận hành hoặc câu chữ:

1. Chữ abstract/full từng câu — abstract dùng danh sách đóng băng ở mục 7; full chỉ thêm số đã
   có file trước khóa 13/9.
2. Commit amendment vào `106` (một A100, G6 trượt giữ, τ exploratory, 3.062 hậu kiểm) **trước**
   train đối chứng.
3. Khôi phục artifact + so md5; nếu lệch thì **dừng**, không improvise OCR mới.
4. Implement sequence-score (teacher-forced, length-norm, resume, probe 50 bước trước hold-out).
5. Fail-closed `infer_branch.py` (cấm `cands=None` → 24 dòng OCR).
6. `build_candidates` mặc định chỉ tap — đã biết; **không đổi constructor trước 16/9**; infer
   phải truyền `--cands`.
7. `build_sel_data` default 1080×2400 khi miss `w,h` (~4,75% ảnh test khác size) — **ghi
   limitation, không rebuild**.
8. Quota Kaggle 30 h/tuần nếu thật sự chặt: subsample hold-out **đăng ký trước 7/9**, không cắt
   sau khi thấy số.
9. Đơn vị Colab còn lại — nếu < ~120–150 thì Sel-B/control chết.
10. Cấu trúc 8–11 trang short (bảng nào, appendix nào) — chưa khóa outline.
11. G11 trọng tài khác họ — không bắt buộc trước 16/9.
12. Listwise vs factored — chỉ Future Work, không chọn một sprint sau 16/9 trong file này.

Đã đo, khỏi "kiểm lại cho vui": overlap episode 1.400 vs remainder = **1 bước**; 3.062 vs 3.063.

---

## 9. Claim được / không được

**Được (khi có file):** cổng đăng ký trước trượt; ngưỡng không nới; kiểm ≥3 cách. **Failure =
over-abstention, không phải mis-localization.** Thước tự đăng ký là bẫy (`sel_acc` ≈ cột HasAns
SQuAD 2.0; bỏ abstain làm HasAns 57,54→69,05 trong khi đúng-cả-bước 63,43→49,71). Readout thay:
bộ ba SQuAD-style + risk at fixed coverage + τ sequence-score. Exec tuyệt đối Voronoi trên 4.463
trong khung 12,0–75,73; nL2/rect interval.

**Không được:** công của menu; Δ_sel Dương; 65/70 như kết quả đã đo trong abstract; gọi 3.062 là
hold-out prereg; gọi chữ nhật là AITW; gọi 75,73 là human ceiling nhận thức; so `gui_sel` với S1
cũ như Δ sạch; nới G6; dùng adapter dở.

## 10. Xác suất chủ quan (không phải đo)

Hai dải từng được nêu; **không biến thành số trong bài**.

| sự kiện | dải hội đồng (thấp hơn) | dải PI Claude (cao hơn) |
|---|---|---|
| Voronoi exec ≥ 65 | ~8–15% | 0,12–0,25 |
| nL2 ≥ 70 | ~18–28% | 0,40–0,55 |
| Δ_sel ≤ −2,8 (đối chứng hại) | — | 0,30–0,40 |
| accept SOICT unconditional | — | 0,40–0,52 |
| accept nếu có exec+control | ~45–60% | — |
| accept nếu chỉ exec | ~25–40% / 0,30–0,42 | — |

Dải PI **không được in như kết quả**. Điều kiện accept phụ thuộc control nhiều hơn 1–2 điểm exec.

## 11. Bug mã bắt buộc biết

| bug | hậu quả | xử trước 16/9 |
|---|---|---|
| `infer_branch.py` thiếu cand key → `cands=None` | 24 dòng OCR, câm | **vá fail-closed** |
| `build_candidates` default taps-only | menu lệch nếu quên cờ | không đổi default; truyền đúng file đã pin |
| `build_sel_data` `w,h` = 1080×2400 | ~4,75% ảnh | limitation |
| parser `pred` rỗng nếu `</sel>` không đóng | 2/1400 | ghi; G6 vẫn trượt cả khi +2 |
| strip `<sel>` trước chấm | đúng thiết kế; cổng đọc `pred` từng vỡ | đã vá một lần — đừng hoàn |

Touch exec hợp lệ **chỉ khi mọi tap key có trong candidates**.

---

## 12. File, đường dẫn, transcript

| file | vai trò sau 4/9 |
|---|---|
| `134` (file này) | ⭐ **thi hành + chốt khoa học** |
| `124_GIAI_THICH_CHO_NGUOI_DOC.md` | bản giải thích 4/9 đã viết lại; nội dung sáu lượt lỗi thời đã xóa |
| `106_DANG_KY_TRUOC.md` | ngưỡng niêm; **cần amendment commit** |
| `128` | lịch sử 30/8 (3B, cấm đổi thước, 6 lượt — **6 lượt đã hủy**) |
| `132` | lịch sử 1/9; số G6/hold-out/AITW **lỗi thời** |
| `133` | ngữ cảnh sau G6; τ ~2 h và 3.063-as-holdout **lỗi thời** |
| `harness/metric_exec.py`, `rule_sensitivity.py` | định nghĩa gated |
| `harness/colab_train_sel.md` | ô kỹ thuật A100; **bỏ chỉ dẫn "sáu lượt"** |
| `harness/kaggle_infer_sel.md` | ô kỹ thuật G6/infer; **bỏ chỉ dẫn "sáu lượt"** |
| `harness/train_config_sel.yaml` | config gốc; lượt còn lại chỉ đổi `dataset=gui_sft_match`, `seed=101`, `output_dir` |
| `harness/build_candidates.py`, `build_sel_data.py` | constructor + branch; phải `--all-steps`, đúng `--img-prefix` |
| `harness/infer_branch.py` | infer; **phải vá fail-closed cand key trước full** |
| `harness/gate_sel_acc.py`, `score_run.py` | G6 và pipeline UGround |
| `runs/score_*_raw.jsonl` | điểm nhánh cũ |
| `runs/sel/preds_gui_sel_seed101_dev1400.jsonl` | G6 |
| `runs/sel/preds_gui_sel_forcesel_273.jsonl` | force diagnostic |

Output mới phải đặt tên **không đè artifact cũ**, tối thiểu: full predictions
`preds_gui_sel_seed101_touch4463.jsonl`; raw exec `score_gui_sel_seed101_raw.jsonl`; dev sequence
scores `seqscores_gui_sel_seed101_dev1400.jsonl` (JSON/YAML có timestamp + SHA input); one-look
`seqscores_gui_sel_seed101_onelook3062.jsonl`; và tương tự cho `gui_sft_match` nếu chạy; rule τ đã khóa.

Workspace (Mac): `/Users/P836901/Documents/Self-learning/thesis/thesis-master/`.
Transcript khóa: chốt thước và phương pháp.
Canvas (ngoài clone): `.../canvases/SOICT-metric-method-verdict.canvas.tsx`. Canvas
`gui-sel-final-verdict.canvas.tsx` ghi "không nộp SOICT / 0 A100" — **stale**.

---

## 13. Prompt dán vào chat mới (copy)

```
Đọc report/134_CHOT_4_9_HANDOFF_CHAT.md trước. Đó là nguồn thắng 4/9/2026.

Không debate lại M1-M4 / E1-E2. G6 57,54% giữ trượt. Một A100: gui_sft_match/101.
sel/202 tắt. Exec n=4463 Voronoi gated primary. τ sequence-score khóa trên 1400
trước khi nhìn control hoặc 3062. 3062 là hậu kiểm, không phải hold-out prereg.
Đọc hợp đồng sequence-score ở §6.1 và runbook §12. Không làm theo phạm vi sáu-lượt
trong header runbook cũ. Gọi cổng mới Sel-A/Sel-B để không lẫn Cổng A/B của 106.

Nhiệm vụ: [ĐIỀN: recover artifacts / infer+exec / train sft_match / sequence-score / viết abstract / vá infer fail-closed]

Generated files không ghi vào thesis-master/. Không commit trừ khi được yêu cầu.
Không nới ngưỡng. Không so gui_sel với S1 cũ như Δ sạch.
```

**Hết 134. Mọi số chưa có file trên đĩa thì chưa được in ra bài.**

---

## 14. ĐỐI CHIẾU TRÊN MÁY WSL — đo ngày 4/9/2026 (phần thêm, không có trong bản Mac)

Bản Mac viết từ **clone disposable** `thesis-master/` nên báo thiếu nhiều artifact. Kho **WSL**
(`/mnt/d/Master/Thesis`) **có đủ**. Đây là thay đổi thật về đường găng, không phải ghi chú.

### 14.1 ⭐ Cổng **Sel-B ĐÃ ĐẠT** — đo trên WSL, 0 giây GPU

| phép kiểm của §7 | yêu cầu | đo được trên WSL | kết |
|---|---|---|---|
| md5 `train_ac/ocr.jsonl` | `a7ddf93d18c060e995afa841f039e343` | `a7ddf93d18c060e995afa841f039e343` | ✅ **khớp tuyệt đối** |
| số dòng `train_ac/train.jsonl` | 64.567 | 64.567 | ✅ |
| prompt `gui_sft_match` ≡ `gui_sel` | 3.000/3.000 | **64.567/64.567** | ✅ **vượt yêu cầu 21,5 lần** |
| target hai nhánh phải khác | — | trùng **0/64.567** | ✅ đúng thiết kế |

Phép so prompt tính trên **toàn bộ khối `messages` không phải assistant + trường `images`**, so
chuỗi JSON, không lấy mẫu. Nghĩa là điều kiện "prompt byte-identical" của M4 không còn là ước
lượng trên mẫu 3.000 mà là **bất biến đo trên toàn tập**.

⇒ **Sel-B không còn là rủi ro.** Điều kiện "Sel-B trượt → 0 A100" đã được gỡ khỏi đường găng.

### 14.2 SHA-256 candidates — pin ngay, khỏi chờ khôi phục

Bản Mac ghi "chưa có SHA candidates để ghi sẵn". Đã tính trên WSL:

```
f10b69411a28e4a9b78aa309241d4a68440e8c463072788c541e887e2e1914f8  test_ac/candidates.jsonl   (6.958 dòng, 8.601.956 byte)
b99586167f9dc2c62c1f9b5d0c2d9ba99cacf625b28edcf97902a360432c669c  train_ac/candidates.jsonl  (64.567 dòng, 79.143.783 byte)
9c526b6f70c6985a5fcb2a597d1708ce…  branches/gui_sel.json
f168a2de3b22a9884ce517f7223f49ff…  branches/gui_sft_match.json
```

Gói `_bundles/branches_sel.tar.gz` chứa đủ **ba** nhánh: `gui_sel.json` · `gui_sft_match.json`
· `gui_s1_match.json` + `dataset_info.json`.

### 14.3 Cái WSL **không** có

- **Adapter `gui_sel_seed101`** — chỉ trên Drive. Mọi việc GPU vẫn phải kéo Drive trước.
- **`preds_gui_sel_seed101_touch4463.jsonl`** — chưa tồn tại; `runs/sel/` mới có dev-1400,
  force-273 và `bo_cuoc_273.jsonl`.
- **Bất kỳ tệp `score_*` nào của `gui_sel`** — `exec` cho nhánh này **chưa chạy lần nào**.

### 14.4 Sel-A — rẻ hơn bản Mac ước

Xác nhận `preds_gui_sel_seed101_dev1400.jsonl` chỉ có các khoá `episode_id · step_id · image ·
app · gold_instruction · action · raw · pred · run` — **không lưu prompt**, đúng như §7 cảnh báo.

Nhưng câu nhắc là **hàm tất định** của (`candidates.jsonl`, `ocr.jsonl`, bản ghi test, mã dựng),
và cả ba đầu vào đó nay đã pin hash. Mà mã dựng câu nhắc **không đổi từ lúc chạy G6**:
`build_candidates.py` và `build_sel_data.py` đứng ở `0c03973` (2/9); commit `f624a48` (3/9) có
sửa `infer_branch.py` nhưng **chỉ thêm ba cờ** `--save-conf` · `--force-sel` · `--only`, không
đụng `prompt_body`.

⇒ **Đã tái dựng 1.400 câu nhắc và hash, 0 giây GPU (làm xong 4/9).** Vế *artifact → prompt* của
Sel-A **đóng**; vế *prompt → raw* vẫn cần adapter + GPU. Nếu vế một trượt thì khỏi tốn GPU cho vế hai.

```
SHA-256 nối 1.400 câu nhắc: 30012d53fdbc6e4704973b8713b5de221014e396638c56ef3bb682ea34bf6b81
thiếu key candidates trong 1.400: 0
```

Cách tính: nối `prompt_body(rr, ocr[image], cands=cands[image])` theo **đúng thứ tự bản ghi
trong tệp pred**, ngăn nhau bằng byte `0x00`. Toàn bộ hash đầu vào + hash mã ghi ở
**`runs/sel/manifest_selA_selB_4_9.json`**.

### 14.4b Hai phép kiểm độc lập đi kèm — cùng khớp

- **Mẫu số 4.463 tái lập từ `test.jsonl`:** `click` 4.446 + `long_press` 17 = **4.463** / 6.958.
  Nghĩa là "bước chạm" gồm cả nhấn giữ, không chỉ click — ai lọc bằng `click` đơn thuần sẽ ra
  **4.446** và lệch 17 bước.
- **Lát 1.400 đúng như §4 mô tả:** 1.400 bước chạm (1.392 `click` + 8 `long_press`) nằm trong
  **2.222 bản ghi đầu** của `test.jsonl`, chỉ số tăng đơn điệu, 0 bản ghi thiếu.
- `candidates.jsonl` tập kiểm phủ **6.958/6.958 màn**, không màn nào thiếu key.
- **Phần còn lại tái lập trùng khít §4:** 4.463 − 1.400 = **3.063 bước / 892 episode**; đúng
  **một** episode trùng với lát dev (`18852`, **1 bước**); sau loại còn **3.062 / 891**.
  Không phải ước lượng — đếm lại từ `test.jsonl` và tệp pred.

### 14.5 Hai bug ở §11 — đã xác minh trên mã, chưa vá

- `infer_branch.py:548` — `cands=cands.get(r["image"]) if a.cands else None`. Key thiếu thì
  `.get()` trả `None` **im lặng**, câu nhắc tụt về bản 24 dòng OCR, không có gì báo lỗi. Đúng
  dạng "lỗi câm" đã trả giá ngày 20/8. **Vá fail-closed là việc 0 GPU, làm được ngay.**
- `metric_exec.py` có `hit_disk` · `hit_nearest_box` · `hit_voronoi`, **không có hàm nL2** —
  xác nhận §3.4. Hàng nL2 phải tái tính từ raw bằng script riêng.

### 14.6 Kho WSL sạch

`git status` không có gì chờ commit ngoài `report/134` này và `harness/debate_04_09/` (8 ảnh
nguồn). Mọi mã của sprint đã nằm trong `f624a48`.
