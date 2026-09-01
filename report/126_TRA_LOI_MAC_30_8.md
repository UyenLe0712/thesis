# 126 — TRẢ LỜI TỪ MÁY MAC (30/8/2026): quyết định train cặp nhánh nào

> **Đây là câu trả lời cho `report/YEU_CAU_GUI_CHAT_MAC.md`.** Máy Mac mở **file gốc**
> `report/123_CHOT_CUOI_PIPELINE.md` (bản vòng 5, không phải bản chép từ ảnh) và trả lời trọn bốn
> câu hỏi mà WSL treo. Nguồn: 6 ảnh chụp màn hình, nay ở `report/anh_123_tra_loi_mac_30_8/`.
>
> ⭐ **Câu trả lời một dòng:** train **`gui_sel` vs `gui_sft_match`**, 1 epoch × 2 hạt giống, chạy
> vô điều kiện. **KHÔNG train `gui_orpo_hard`** — phương án đó đã bị chính §7.5 bác, câu trỏ tới
> nó ở `123` §2.7 là **leftover đã chết**.
>
> ⛔ **Cảnh báo đọc:** `report/123_CHOT_CUOI_PIPELINE_CHEP_TU_ANH.md` dòng **453–454** hiện vẫn
> ghi *"Xem §7.5 cho phương án được khuyến nghị (`gui_orpo_hard`…)"*. Câu đó **không thi hành**.
> Bản chép từ ảnh không sai — nó chép trung thực một câu mà file gốc đã tự bác ở mục sau.

| ảnh | nội dung |
|---|---|
| `01_muc0_muc1.jpg` | §0 train cặp nào · §1 · §1.1 leftover đã chết · §1.2 ORPO chưa bao giờ tách khối |
| `02_muc1.3_1.4.jpg` | §1.3 dự án đã đo đúng đại lượng đó · §1.4 Δ có bắt được khối ứng viên không |
| `03_muc2_lich_ngansach.jpg` | §2 lịch + bảng ngân sách `123` §8.1 + lịch §8.2 tuần 0 |
| `04_muc2cuoi_muc3_muc4.jpg` | tuần 1–6 · §3 việc không tốn GPU · §4 giờ/epoch là ước lượng |
| `05_muc5_muclucA123_muc6.jpg` | §5 **mục lục `123` §4–§16** · §6.1 khối ứng viên · §6.2 ~704 bước |
| `06_muc6.3_muc7_muc8_muc9.jpg` | §6.3 cổng G3/G5b/G6/G10 · §7 mẫu (x16) · §8 chỗ yếu · §9 xác nhận |

---

## 1. §0 — TRAIN CẶP NÀO (bản chép nguyên văn)

Train đúng **hai nhánh, bốn lượt**:

| nhánh | hạt | epoch | backbone mặc định |
|---|---|---|---|
| `gui_sel` | 101 | 1 | `Qwen3-VL-4B-Instruct` |
| `gui_sft_match` | 101 | 1 | cùng |
| `gui_sel` | 202 | 1 | cùng |
| `gui_sft_match` | 202 | 1 | cùng |

**Chạy vô điều kiện** — không chờ hạt 101 đẹp mới chạy hạt 202.

⛔ Không train `gui_orpo_hard` làm hướng chính · ⛔ không τ, không suy luận hai lượt, không
`calibrate_tau.py` · ⛔ **không hy sinh hạt 2**. Nếu **G5b > 27 h/epoch** thì **hy sinh backbone**
(về `Qwen2.5-VL-3B`), không hy sinh hạt.

```
Δ = mean_2hạt[exec(gui_sel)] − mean_2hạt[exec(gui_sft_match)]
```

---

## 2. §1 — VÌ SAO `gui_orpo_hard` BỊ LOẠI

**Không, ORPO không "bắt" được đóng góp của khối ứng viên. Và phương án đó đã bị loại.**

### 2.1 Ảnh WSL đang đọc một câu đã chết (§1.1)

`123` §2.7 còn một câu leftover ở cuối mục, ngay trước §3, kiểu *"xem §7.5 cho `gui_orpo_hard`:
tách đúng một biến, đủ hai hạt trong ~40 h"*. Câu đó **mâu thuẫn với chính §7.5 vòng 5**. Luật đọc
file (`123` §1): mục nhãn vòng 5 thắng ⇒ **§7.5 / §7.5b thắng, leftover ở §2.7 không thi hành.**

### 2.2 ORPO chưa bao giờ tách khối ứng viên ra khỏi đối chứng (§1.2)

Ngay cả bản cũ, **hai nhánh ORPO cùng có khối ứng viên**. Biến bị tách không phải "có/không khối",
mà là:

```
Δ_orpo = exec(ORPO vế âm KHÓ) − exec(ORPO vế âm NGẪU NHIÊN)
```

Khối ứng viên **triệt tiêu trong hiệu số**, y hệt SEL vs SFT-match. ORPO **không** giải quyết rủi
ro *"điểm tuyệt đối đẹp, Δ TRẮNG"*. Nó chỉ hỏi một câu **hẹp hơn**: tương phản khó có hơn tương
phản ngẫu nhiên không.

### 2.3 Dự án đã đo đúng đại lượng đó rồi (§1.3, từ tệp thô — `123` §7.5a)

| checkpoint | `sel_acc` | `exec` |
|---|---|---|
| CE2/101 — SFT thuần, tầng 2 | **65,70%** | **59,42%** |
| MIN/101 — ORPO vế âm khó, tầng 2 | **66,55%** | **60,05%** |

**Toàn bộ công của ORPO-khó chồng lên SFT = +0,85 pp `sel_acc` = +0,63 pp `exec`.**

Mà estimand của `gui_orpo_hard` còn là **tập con** của +0,63 (*khó trừ ngẫu nhiên*, không phải
*khó trừ không có gì*). Muốn chạm ngưỡng Dương **+2,8 pp** thì phải **lớn gấp ~4,4 lần** mức đã đo.

Tiền lệ ngoài: **WEPO (AAAI 2025)** — hard vs random, 1 negative = **+1,1 pp** trên thước của họ;
quy qua độ dốc thật **0,456** → ~**+0,50 pp exec**. Không có bằng chứng peer-reviewed nào cho
hard-vs-random ≥ +2,8 trên tác vụ gần.

**Ba lỗi của bàn ORPO cũ** (đã kiểm trong §7.5a):
- ngân sách *"~40 h / 5 h mỗi hạt"* ngoại suy sai config — **thật là 52–91 h**;
- eligibility *"≈100%"* là **mẫu số có điều kiện**; vô điều kiện ≤ **77,8%**;
- `106` mục **(x13c)** đã kết luận lỗi khai báo **không phải** lẫn hai phần tử cạnh nhau
  (trung vị lệch **351 px**; **76,5%** nằm ngoài dải vế âm khó 80–350).

⛔ **Không dùng `S2r` làm đối chứng** — `106` đã đăng ký nó là thiết kế chắc chắn thua.

### 2.4 Δ **không** bắt khối ứng viên — và đó là chủ đích (§1.4, thiết kế chốt `123` §7.5b)

- **Cả hai nhánh:** cùng backbone, **cùng khối ≤40 ứng viên** (câu nhắc **byte-identical**), cùng
  câu vàng.
- **Chỉ khác:** `gui_sel` sinh `<sel>…</sel>` rồi câu; `gui_sft_match` chỉ câu.

```
Δ_component = công của ĐẦU CHỌN TƯỜNG MINH
            ≠ công của khối ứng viên
```

Khối ứng viên là **đòn điểm tuyệt đối** (cả hai nhánh đều hưởng). Đầu `<sel>` là **đóng góp mô
hình** GVHD đòi — đúng một biến, nên mới so được.

> ⭐ **Hệ quả phải nói thẳng trước khi bấm train:** rất có thể `exec` tuyệt đối **đẹp** (kỳ vọng
> **63,7–65,1%**) trong khi **Δ rơi Dương yếu (+1,7…+2,8) hoặc TRẮNG**. Đó **không** phải thất bại
> vận hành của pipeline — đó là **ước lượng trung thực của đúng biến đã đăng ký**.

**Cách KHÔNG được làm để "kéo Δ cho đẹp":**
- ⛔ Bỏ khối ứng viên khỏi đối chứng (so với S1 / 24 dòng OCR) — khác **hai** biến; `123` §9.1 cấm
  đọc Δ vs S1.
- ⛔ Train ORPO để mong Δ ≥ +2,8 — số của chính dự án đã bác.
- ⛔ Đổi luật Voronoi / ép tên / bỏ vị trí — đã chết ở §2.

**Cách được trình bày với thầy nếu Δ trắng:** điểm tuyệt đối + `sel_acc` + lát chọn đúng đã bão hoà
(**85,2% ≈ 85,7%** của người) + Δ là công của **đầu chọn**, không phải của **menu ứng viên**. Menu
là thay đổi **đầu vào**, có tiền lệ (Geng EMNLP 2023) ⇒ **không claim "cơ chế mới"**.

**ORPO chỉ còn là thí nghiệm phụ có điều kiện** (`123` §7.5c): sau khi đã có Δ hạt 101, **nếu** còn
GPU **và** Δ không âm. Không phải chỗ đặt luận văn.

---

## 3. §2 — LỊCH VÀ ĐIỂM QUYẾT ĐỊNH: dùng `123` §8, **không** dùng `121` §7

`121` §7 (9 tuần, G1–G7, D1/D2/D3, ~140 h) **không còn hiệu lực** cho sprint này.

| thứ trong `121` | trạng thái trong `123` vòng 5 |
|---|---|
| D1 (quyết từ chối / G7) | **không còn đối tượng** — G7 không thi hành, từ chối không còn là đóng góp chính |
| D2/D3 lịch 9 tuần | thay bằng **lịch 6 tuần** ở §8.2 |
| ~140 h kịch bản đầy đủ | thay bằng **72–88 h** lạc quan / **112–148 h** nếu G5b xấu / **~46 h** nếu về 3B |
| thiết kế sàng lọc 1 hạt rồi mới hạt 2 | **bỏ** (§7.1b không thi hành) |

### Bảng ngân sách — `123` §8.1 (paste nguyên)

| việc | A100-40GB | Kaggle T4 |
|---|---|---|
| `gui_sel` hạt 101, 1 epoch, seq 3072 | 16–20 h | — |
| `gui_sft_match` hạt 101, 1 epoch | 16–20 h | — |
| `gui_sel` hạt 202, 1 epoch | 16–20 h | — |
| `gui_sft_match` hạt 202, 1 epoch | 16–20 h | — |
| suy luận 4 lượt (một lượt sinh) | ~8 h | — |
| chấm UGround 4.463 × 4 | — | ~22 h |
| G9 nhiễm (n ≥ 2.000, mù ảnh + mù khối) | ~0,5 h | ~0,6 h |
| G11 trọng tài khác họ | — | ~2 h |
| **TỔNG lạc quan** | **~72–88 h + 15 h đệm** | **~25 h** |
| nếu G5b xấu (26–35 h/epoch) | 112–148 h | 25 h |
| cứu: Qwen2.5-VL-3B, 4 lượt × 1 epoch | ~46 h | ~25 h |

**Thứ tự hy sinh GPU:** epoch 2 (đã hy sinh) → **backbone 4B→3B** → nhánh phụ.
⛔ **Không hy sinh hạt 2.**

**Không có ngân sách cho:** hạt 3 · rerun Base/S1 ở 4B · 7B · mở vision · LÙI · MIX · Venus full ·
chấm người 100 câu · ORPO GĐ2 (chỉ xét sau Δ).

### Lịch `123` §8.2

**Tuần 0 (0 GPU, xong mới được train):** dán **(x16)** vào `106` **sau khi có số G1/G2 train**,
đừng dán khống · G1/G2 **test đã xong** (96,7% / 91,2% có điều kiện, `n_gold`=3.505; vô điều kiện
71,6%) · còn **G1/G2 TRAIN + tỉ lệ khối RỖNG** trên Drive · **G3** · `prompt_body(..., cands=None)`
+ `--selftest` · `build_sel_data.py` hai file cùng n · **dev ~500 theo episode** · **G4** tokenizer
Qwen3-VL · hai yaml `num_train_epochs: 1`.

**Tuần 1:** G5 smoke 20 bước · **G5b pilot 200 bước** (≤27 h/epoch giữ 4B; >27 h → 3B) · train
`gui_sel` ≥ 2.000 update → **G6 trên dev** (mốc **63,6%**, luật `gate_desc_acc.py`) · G9 song song.
**Trượt G6 = STOP.**

**Tuần 2–5:** bốn lượt 1 epoch. Suy luận **greedy một lượt**. Chấm. Δ = trung bình 2 hạt.
G8/G10/G11. ⛔ Không G7, không τ.

**Tuần 6:** viết. Mọi bảng lát **báo hai lần** (nội sinh + ngoại sinh).

**Không có D1/D2/D3.** Điểm dừng thật: trượt G1/G2/G3 trước data · trượt G4 · trượt G5 · G5b quyết
4B vs 3B · **trượt G6 STOP train**.

---

## 4. §3 — VIỆC THÁNG 9 KHÔNG TỐN GPU: `123` **CÓ** xếp thứ tự

Có xếp, **không để "tự quyết"**. Nguồn: §8.2 tuần 0 + §14 + §2.6.

**Trước train (bắt buộc, 0 GPU train; một phần cần Drive):**
1. **G1/G2 TRAIN + đếm khối rỗng** — ⭐ việc Drive quan trọng nhất; **nếu phủ train vô điều kiện
   < 70% thì dừng, báo lại**.
2. **G3** (300 mẫu mù).
3. **Dán (x16)** — sau khi có số trên, không dán khống.
4. `prompt_body` + `build_sel_data.py` + dev theo episode + **G4**.

**Độc lập với việc Δ có trắng hay không** (viết / đo mô tả, 0 GPU train):

| việc | ưu tiên | ghi chú |
|---|---|---|
| Cảnh báo lát nội sinh **11,50 pp**, KTC95 [9,40 · 13,37] | **đã đo xong** | đưa vào luận văn / Limitations **ngay**, không chờ train |
| Đường **risk–coverage** | tuần 6 / song song sau khi có logprob | G0 **không phải cổng**; 0 h train nếu dùng adapter MIN-DESC; với `gui_sel` thì log `conf` lúc suy luận rồi vẽ hậu kiểm |
| Cập nhật **luận văn** (chẩn đoán lát, trần 70% không tới, chữ cấm §9) | song song tuần 0–6 | `123` §9.4: **Δ trắng vẫn là luận văn đo được**; ⛔ không đổi thước |

**Thứ tự ấn định:** Drive G1/G2/rỗng → **(x16)** → dựng data → G5/G5b → bốn lượt train.
Risk–coverage và lát nội sinh **không được nhảy lên trước** G1/G2 train, nhưng **cũng không bị
chặn** bởi kết quả GPU — làm song song lúc chờ máy / sau chấm.

---

## 5. §4 — 16–20 / 26–35 h/epoch là **ƯỚC LƯỢNG**, chưa đo Qwen3-VL-4B

**Chưa có lượt đo thật nào trên Qwen3-VL-4B trong dự án này.** `123` §13.14 nguyên văn:
*"Giờ/epoch 4B chưa đo trên máy này."*

| con số | bản chất |
|---|---|
| **16–20 h/epoch** lạc quan | ước lượng thiết kế 1 epoch, bản vòng 5 |
| **26–35 h/epoch** bi quan | cùng loại; phản ánh regression 3DConv `torch ≥ 2.9` (issue LLaMA-Factory **#9380**, đo trên **8B/7B**, không phải 4B của ta) |
| 31–39 vs 46–70 h | ước lượng **2 epoch** — ⛔ không dùng để quyết |
| ngưỡng **G5b 27 h/epoch** | **ngưỡng ngân sách đặt trước**, chưa phải số đo. 4 × 27 ≈ 108 h (+ suy luận + đệm) là lúc phải về 3B (~46 h) để còn đủ 2 hạt |
| **G5b** | **phép đo sẽ chạy**: pilot 200 bước → giây/bước → ngoại suy giờ/epoch |

**Bắt buộc trước khi cam kết cả lượt:** ghim `torch==2.8.0`, Python 3.10; **xoá `tokenized_cache`**;
chạy G5b.

---

## 6. §5 — MỤC LỤC `123` phần ảnh cũ không phủ (§4 trở đi)

```
§4  Backbone Qwen3-VL-4B + rủi ro giờ (G5b)
§5  Dựng dữ liệu (5.1 khối ứng viên = a11y có tên, không phải OCR∪a11y;
    5.1b --all-steps; 5.2 phủ; 5.3 build_sel_data; 5.4 dev theo episode)
§6  Thước: 1 chính + 4 đồng-báo; khoá luật sel_acc; trọng tài khác họ
§7  Δ, dải 106, cổng; ⛔ 7.0 G0 không còn cổng; ⛔ 7.1b hai-giai-đoạn không thi hành
    7.2 mục tiêu tuyệt đối; 7.3 cổng; 7.5 CHỐT
§8  Ngân sách + lịch 6 tuần
§9  Chữ cấm / được / câu đóng góp
§10 Bẫy vận hành
§11 File mã đụng / không đụng
§12 Mẫu (x16) — dán 106 TRƯỚC dựng data
§13 Việc còn mở (phải ĐO)
§14 10 việc đầu
§15 Citation
§16 Tự kiểm + chỗ yếu tự khai
```

⛔ **Không thi hành:** §3.4 (hai lượt + τ) · §7.0-như-cổng · §7.1b · leftover `gui_orpo_hard` ở
cuối §2.7.

---

## 7. §6 — ĐỊNH NGHĨA ĐỂ VIẾT MÃ (rút từ gốc)

### 7.1 Khối ứng viên (`123` §5.1)

Khung xương là **cây trợ năng**. `if not nds: return []` — màn không có a11y ⇒ **khối rỗng**, OCR
**không cứu**. OCR chỉ **đặt tên** node (tâm chữ trong hộp). **Node không tên bị loại.**
Luận văn phải viết: *"ứng viên = node trợ năng **có tên**"*. ⛔ Không `icon#k`.
Khối rỗng: dòng `(không có)` + nhãn train `<sel>none</sel>`. **Nếu tỉ lệ rỗng > 15% → Limitations.**

`build_candidates.py` hiện **chỉ ghi bước chạm** → phải thêm `--all-steps`. Một bản ghi /
(episode, step); `cands: []` là hợp lệ.

### 7.2 ~704 bước (`123` §2.7 + §7.2)

G2 **91,2%** là **có điều kiện** trên `n_gold` = 3.505. Vô điều kiện:
`91,2% × 3.505/4.463 = 71,6%`. **~22% bước không có tên vàng** ⇒ chọn vô nghĩa.
Phần giao *"có ứng viên vàng trong khối ∩ đang chọn sai"* ≈ **704 bước**.
Cứu hết → `exec` ≈ **67,2%** (trần độ phủ). **65%** cần cứu **484** bước (69% của 704) — stretch.
**70%** cần **973 > 704** ⇒ **bỏ**.

### 7.3 Bốn cổng WSL đã hỏi (`123` §7.3)

**G3** (trước dựng data, 300 mẫu): (a) chuỗi `GOLD`/`gold` trong câu nhắc = **0**; (b) hạng chuẩn
hoá của ứng viên vàng, mean ∈ **[0,40 · 0,60]**; (c) **P(idx=0) ≤ 8%**; (d) Spearman |ρ| giữa `idx`
và `L2(cand, gold)` ≤ **0,10**.

**G5b:** pilot 200 bước; ≤27 h/epoch **giữ 4B**, >27 h → **3B**. Không hạ epoch (đã 1). Không hy
sinh hạt 2. `torch==2.8.0`.

**G6:** `gate_desc_acc.py`, **600 bước DEV** có ứng viên vàng, **khớp tên ∧ point ±14%**,
`<sel>none</sel>` = **sai**, ngưỡng **≥ 63,6%**. **Không dùng test.** `sel_acc` (L2, mẫu 4.463)
**chỉ log, không phải cổng**.

**G10:** chênh tỉ lệ câu chứa **tên nguyên văn** `|sel − match| ≤ 2 pp` (siết từ 10: artefact
10% × 28,5 = **+2,85 > ngưỡng Dương +2,8**). Báo Δ **phân tầng** có/không chép tên.

Còn: **G9** n ≥ 2.000 **mù ảnh + mù khối**; **G11** trọng tài khác họ = **OS-Atlas-Base-4B (Phi-3)**
hoặc **GLM-4.6V-Flash**, ⛔ **không** OS-Atlas-7B (vẫn Qwen).

---

## 8. §7 — MẪU (x16) dán vào `106` **khi có số G1/G2 train**

**Không dán khống.** Nội dung khoá (rút `123` §12):

- Cặp `gui_sel` / `gui_sft_match`, **1 epoch × hạt 101 và 202 vô điều kiện**, Qwen3-VL-4B,
  **QLoRA 4-bit, freeze vision, cutoff 3072, lr 1e-4, lô hiệu dụng 16**.
- Ghim `torch 2.8.0`. G5b: ≤27 h giữ 4B, >27 h → 3B.
- ⛔ Không đăng ký τ / hai lượt / G7-cổng / abstention là đóng góp chính.
- **Δ dải `106` (w):** Dương ≥ **+2,8**; dương yếu **+1,7…+2,8**; trắng **−2,8…+1,7**.
  **Một hạt = TRẮNG.**
- `sel_acc`: L2 ≤ 0,14·W, mẫu 4.463, `none` = sai. **G6 = luật lịch sử trên dev.**
- **Headline Voronoi không đổi. Mục tiêu 70% bỏ.**

Chi tiết từng dòng ở `123` §12 — Mac có file gốc; WSL lấy từ git sau khi Mac push 122/123/124,
hoặc copy nguyên văn mục §12.

---

## 9. §8 — CHỖ YẾU CÒN THẬT (`123` §16), phải nói với thầy **trước** khi train

**Đã đóng ở vòng 5:** lời nguyền người thắng (hai hạt vô điều kiện) · bất đối xứng hai lượt.

**Còn phải khai:**
1. **1 epoch chưa từng chạy trong dự án** (mọi nhánh cũ 2 epoch) — ước mất **0,5–2 pp** tuyệt đối.
2. **Δ có thể TRẮNG dù `exec` đẹp** — khối ứng viên có ở cả hai nhánh.
3. **Trần độ phủ 67,2%**; ~22% bước không có tên.
4. **Giờ/epoch 4B chưa đo.**
5. **Mật độ `<sel>none</sel>` nếu > 50% phải cân lại TRƯỚC train** (`123` §13.5).

**Kiểm toán số:** không có số nào lệch **có lợi** cho kế hoạch.

---

## 10. §9 — XÁC NHẬN KIỂM CHÉO CỦA WSL: giữ nguyên, không làm lại

Các verify từ `descriptor_build_stats*.json` và `build_candidates.py:138–148` / `prompt_body`
**khớp bản Mac**. `build_sel_data.py` **chưa có ở bản Mac — phải viết mới** (WSL đã viết xong
29/8, xem `report/125` mục 3). `calibrate_tau.py` **không viết**.

> *Hết phần chép. Câu cuối của bản Mac: **"Quyết định train: `gui_sel` vs `gui_sft_match`, 1×2 hạt,
> không ORPO."***

---

---

# PHẦN CỦA WSL — kiểm chéo và phán quyết

## 11. Kiểm chéo: cái gì khớp, cái gì mới, cái gì chưa kiểm được

### ✅ Khớp với thứ đã có trên kho (kiểm được ngay)

| khẳng định của Mac | đối chiếu |
|---|---|
| Thiết kế chốt = SEL vs SFT-match, 1 epoch × 2 hạt vô điều kiện | `123_..._CHEP_TU_ANH.md` **dòng 207** *"⭐ Chốt vòng 5 (§7.5b)"* đã ghi **y hệt**. Hai bản chép độc lập khớp nhau ⇒ đây **không phải kế hoạch mới**, mà là phần còn thiếu của kế hoạch WSL đã biết một nửa |
| MIN − CE2 = **+0,63 pp exec** | `CLAUDE.md`: *"Δ_component = MIN − CE2 = +0,63 pp (p=0,011, KTC [+0,16 · +1,10])"* ✅ |
| MIN/101 exec **60,05%** | `CLAUDE.md`: *"MIN-DESC/101 = 60,05% (25/8)"* ✅ |
| Lỗi khai báo **không phải** lẫn hai phần tử cạnh nhau — trung vị **351 px**, **76,5%** ngoài dải | `CLAUDE.md` mục on-policy (x13): *"p25 70 px · trung vị 351 · p75 748 ⇒ 76,5% bước S2 sai tên nằm ngoài dải 80–350"* ✅ **Đây là đòn giết `gui_orpo_hard`, và nó là số của chính dự án** |
| Δ một hạt = TRẮNG | `CLAUDE.md`: *"luật `106` (w) đòi trung bình hai hạt giống"* ✅ |
| Mọi nhánh cũ 2 epoch | `CLAUDE.md`: `~8.072 bước` = `ceil(64.567/16)=4.036 ×2` ✅ |
| G1 96,7% / G2 91,2% / vô điều kiện 71,6% | `report/125` mục 2 — WSL đã tự chạy lại và tái lập ✅ |
| `calibrate_tau.py` không viết | `report/125` mục 6 ✅ |
| `build_sel_data.py` phải viết mới | ✅ — và WSL **đã viết xong** 29/8 |

### 🆕 Số/luật mới, chưa từng có trên kho WSL

- `sel_acc`: **CE2/101 = 65,70%** · **MIN/101 = 66,55%** (+0,85 pp). Khác với con số cổng cơ học
  đã ghi ở `CLAUDE.md` (CE2-S2 **59,8** · MIN-DESC **60,6** trên 3.473 bước có tên vàng) — **hai
  thước khác nhau, khác mẫu số**, không mâu thuẫn nhưng **đừng trộn**.
- **WEPO (AAAI 2025)** hard-vs-random 1 negative = +1,1 pp; độ dốc quy đổi **0,456**.
- Ngưỡng **G6 = 63,6%** trên dev (mốc S2 cũ ở `gate_desc_acc.py` là 53,9%).
- **G10** siết từ 10 pp xuống **2 pp**, có lý do số học: artefact 10% × 28,5 = +2,85 > ngưỡng
  Dương +2,8.
- **G11** = OS-Atlas-Base-4B (Phi-3) hoặc GLM-4.6V-Flash — **cả hai chưa từng được tra trong
  `report/114`**; danh sách bộ trỏ đã loại ở `CLAUDE.md` cũng chưa nhắc hai model này.
- Issue **LLaMA-Factory #9380** (regression 3DConv `torch ≥ 2.9`).

### ⚠️ Chưa kiểm được từ WSL — phải mở nguồn trước khi vào bài

Theo luật của chính dự án (*"mở lại NGUỒN, không mở lại ghi chú"*):
1. **WEPO AAAI 2025** — venue/năm/con số +1,1 pp.
2. **Model card `Qwen3-VL-4B-Instruct`** — ScreenSpot-v2 93,08 / ScreenSpot-Pro 59,50.
   `123` tự khai đây là *"quyết định vận hành tạm"*.
3. **Geng EMNLP 2023** — tiền lệ "menu là thay đổi đầu vào".
4. **OS-Atlas-Base-4B** và **GLM-4.6V-Flash** — có sạch AndroidControl không (đúng câu hỏi đã
   giết Jedi ở `CLAUDE.md`).
5. **LLaMA-Factory #9380**.

---

## 12. ⭐ PHÁN QUYẾT: theo bản Mac. Nhưng kèm hai chỗ phải xử trước khi bấm train.

### 12.1 Theo bản Mac — vì sao

**Ba lý do, không phải cảm tính:**

**(1) `gui_orpo_hard` chết bằng số của chính dự án, không phải bằng lập luận.** Toàn bộ công của
ORPO-khó chồng SFT đã đo được rồi: **+0,63 pp exec**. Estimand của `gui_orpo_hard` còn **nhỏ hơn**
số đó (khó − ngẫu nhiên ⊂ khó − không có gì). Ngưỡng Dương là +2,8. Muốn đạt phải gấp **4,4 lần**
một đại lượng đã đo. Cộng thêm **(x13c)**: lỗi khai báo lưỡng cực, trung vị lệch **351 px**, 76,5%
nằm **ngoài** dải vế âm khó ⇒ tiền đề của "vế âm khó" giả định một dạng lẫn cục bộ mà mô hình này
**không mắc**. Đây **đúng y** lý do MIN-ONPOLICY đã chết ở cổng 3,3%. Đi lại đường đó là lần thứ ba.

**(2) Bản Mac sửa đúng cái khuyết tật đã làm MIN-DESC không đọc được.** MIN-DESC ra 60,05% — cao
nhất mọi nhánh — mà vẫn phải đọc là **TRẮNG**, vì chỉ có **một hạt giống**. Bản Mac trả tiền cho
**hạt thứ hai trước**, bằng cách hạ 2 epoch → 1 epoch, và bắt chạy **vô điều kiện**. Đó là đổi
**0,5–2 pp điểm tuyệt đối** lấy **quyền được kết luận**. Với một dự án đã có sẵn một Δ trắng vì
thiếu hạt, đây là phép đổi đúng.

**(3) Nó trả lời thẳng câu hỏi WSL hỏi, và trả lời "không".** WSL hỏi *"§7.5 tách biến nào để Δ
bắt được khối ứng viên?"* — Mac trả lời: **không tách, và cố ý không tách**; Δ đo **đầu chọn tường
minh**, không đo menu. Kèm luôn dự báo khó chịu (*exec đẹp, Δ có thể TRẮNG*) và **cấm** bốn cách
kéo Δ cho đẹp. Một bản kế hoạch tự khai trước rằng đại lượng chính của nó có thể ra trắng, rồi vẫn
chốt chạy, là bản kế hoạch **không tự lừa** — cùng nếp với đăng ký trước `106` mà dự án đã giữ 25
ngày.

⇒ **Không có phương án nào khác trên bàn đáng theo.** `gui_orpo_hard` đã chết bằng số; `s2r`,
`s2_nopoint`, τ/hai lượt/abstention đều đã chết trước đó; giữ nguyên hiện trạng thì đóng góp mô
hình dừng vĩnh viễn ở một ô TRẮNG một-hạt-giống.

### 12.2 ⛔ Chỗ tôi **không đồng ý** với bản Mac: đổi backbone làm hỏng đúng cái phao mà chính nó dựa vào

Bản Mac nói: nếu Δ trắng thì **trình bằng điểm tuyệt đối** (63,7–65,1%) + `sel_acc`.
Nhưng nó **đồng thời** đổi backbone sang **Qwen3-VL-4B**, và ngân sách ghi rõ **"không có ngân sách
cho rerun Base/S1 ở 4B"**. Hệ quả:

> **Mọi số tuyệt đối của dự án — Base 47,6 · S1 59,1 · S2 57,2 · CE2 59,4 · MIN 60,1 — đều đo trên
> Qwen2.5-VL-3B.** Nếu bốn lượt mới chạy trên 4B mà **không có mốc 4B nào**, thì câu *"64% so với
> 60,1% trước đây"* là **so bắc cầu qua hai biến** (backbone + đầu chọn) — đúng loại lỗi mà chính
> `123` §9.1 cấm khi nói về Δ vs S1.

⇒ Phao "điểm tuyệt đối" **xẹp đúng lúc cần nó nhất**, tức lúc Δ trắng.

Thêm một điểm đáng ngờ về **lý do** đổi backbone: căn cứ là ScreenSpot-v2 **93,08 vs 80,9** — đó là
benchmark **định vị**. Nhưng trong pipeline này mô hình được train **không định vị**; nó **viết câu**
và **chọn một mục trong khối ứng viên đã có sẵn tên + toạ độ**. Việc định vị do **UGround** làm.
Kỹ năng ScreenSpot vì thế chỉ liên quan **gián tiếp**. `123` cũng tự khai số này *"phải xác minh
model card"* và *"hiện dùng làm quyết định vận hành tạm"*.

**Ba cách xử, xếp theo giá:**

| cách | tiền · thời gian | ảnh hưởng độ chính xác |
|---|---|---|
| **(a) ⭐ Giữ 4B + thêm MỘT mốc Base trên 4B** | **~2 h A100 (suy luận, KHÔNG train) + ~5,6 h Kaggle** | Phục hồi trọn vẹn phao "điểm tuyệt đối": có `Base@4B` thì đọc được *"đầu chọn + menu nâng từ X lên Y **trên cùng backbone**"*. Rẻ nhất trong ba cách vì Base **không cần train** |
| **(b) Giữ nguyên backbone Qwen2.5-VL-3B** | **~46 h thay vì 72–88 h** (tiết kiệm ~30 h) | Mọi số so thẳng được với toàn bộ dự án. Mất phần "backbone mạnh hơn" — nhưng phần đó **chưa bao giờ được đo**, chỉ là ước lượng thiết kế |
| **(c) Theo đúng bản Mac, không thêm gì** | 0 | Δ vẫn hợp lệ (nội bộ, cùng backbone hai vế). Nhưng nếu Δ trắng thì **không còn gì để trình**, vì số tuyệt đối treo lơ lửng không mốc |

**Đề nghị: (a).** Nó giữ nguyên toàn bộ quyết định của bản Mac, chỉ thêm **~2 h A100 + 5,6 h
Kaggle** — chưa tới **3%** ngân sách sprint — và mua lại đúng thứ mà kịch bản-xấu cần. Kaggle
5,6 h này phải **xếp sang tuần khác** (22 + 0,6 + 2 = 24,6 h đã gần trần 30 h/tuần).

⚠️ Nếu user chọn (c) thì phải **viết trước vào `106` mục sửa đổi**: *số tuyệt đối của bốn lượt
Qwen3-VL-4B không được so với bất kỳ nhánh 2.5-VL-3B nào* — khoá trước khi thấy điểm, đúng nếp
đăng ký trước.

### 12.3 Chỗ thứ hai: đừng để "chấp nhận Δ trắng" trượt thành "không cần Δ"

Bản Mac nói Δ trắng *"không phải thất bại vận hành"* — **đúng**. Nhưng phải khoá kèm một câu, nếu
không thì sau khi thấy điểm rất dễ trượt sang *"vậy thì báo `sel_acc` làm headline"*:

> `sel_acc` **là thước phụ, không phải headline** (`123` §6: 1 chính + 4 đồng-báo; §7.3: `sel_acc`
> **chỉ log, không phải cổng**). Headline vẫn là **`exec` / `hit_voronoi`**, không đổi.

Dự án đã tự khai **hai lần nới ngưỡng sau khi thấy điểm**. Đây là chỗ dễ có lần thứ ba nhất.

---

## 13. Việc phải làm, theo thứ tự — hợp nhất bản Mac với trạng thái thật của WSL

**Trước hết, không quên:** hôm nay **30/8 là hạn VCL**, mai **31/8 là hạn FAIR**. Toàn bộ kế hoạch
này là **sprint tháng 9**, không đụng gì tới hai bài. `CLAUDE.md` còn ghi VCL thiếu **số điện thoại
hai tác giả** — đó mới là việc của hôm nay.

| # | việc | chặn cái gì | trạng thái |
|---|---|---|---|
| 0 | Nộp VCL (30/8) · FAIR (31/8) | — | ⛔ **ưu tiên tuyệt đối hôm nay** |
| 1 | Kéo `train_ac/train.jsonl` + `train_ac/ocr.jsonl` **bản đầy đủ** từ Drive (~80 MB) | **mọi thứ ở dưới** | ⛔ chặn — `report/125` mục 5 |
| 2 | `build_candidates.py --split train --all-steps` → **G1/G2 TRAIN + tỉ lệ khối RỖNG** | (x16), dựng data | ⚠️ **luật trượt: phủ train vô điều kiện < 70% ⇒ DỪNG, báo lại**; khối rỗng > 15% ⇒ Limitations |
| 3 | **Đọc mù 300 mẫu G3** (tệp đã xuất sẵn `branches/g3_mau300_doc_mu.txt`) | dựng data | phần người, script không thay được |
| 4 | Dán **(x16)** vào `report/106` — **sau** khi có số ở #2 | train | ⛔ không dán khống |
| 5 | `build_sel_data.py --split train` **từ đúng `ocr.jsonl` đã dựng S1/S2** | train | ⚠️ `report/125` mục 5: lát WSL lệch **26/1.697 = 1,5%** ở chuỗi OCR ⇒ đổi lượt OCR là **đổi cả `<sel>` lẫn `sel_acc`**, **không có tiếng động** |
| 6 | `prompt_body(..., cands=None)` + `--selftest` · dev ~500 theo episode · **G4** đo bằng **tokenizer Qwen3-VL** (kể cả token ảnh) | train | G4 cũ đo bằng processor 2.5-VL ⇒ **không chuyển sang được** |
| 7 | **Quyết backbone** — theo §12.2 (a) / (b) / (c) | ngân sách | ⚠️ **cần user quyết** |
| 8 | Ghim `torch==2.8.0`, Python 3.10, xoá `tokenized_cache` → **G5 smoke 20 bước** → **G5b pilot 200 bước** | 4B vs 3B | G5b là **phép đo thật đầu tiên** của giờ/epoch |
| 9 | Train `gui_sel` ≥ 2.000 update → **G6 trên dev ≥ 63,6%**. **Trượt = STOP** | ba lượt còn lại | |
| 10 | Bốn lượt 1 epoch → suy luận greedy → chấm → Δ = trung bình 2 hạt → G8/G10/G11 | — | |

**Làm song song, không chờ GPU** (`123` §3): đưa **cảnh báo lát nội sinh 11,50 pp [9,40 · 13,37]**
vào luận văn/Limitations **ngay** · cập nhật luận văn theo `123` §9 (chẩn đoán lát, **trần 70%
không tới**, chữ cấm) · risk–coverage để tuần 6.

**Verify nguồn** (mục 11.3) — làm lúc chờ máy, **trước** khi bất kỳ số nào vào luận văn.

---

## 14. Một câu để nhớ

Bản Mac không hứa Δ sẽ dương. Nó hứa **đo đúng một biến, đủ hai hạt, và không đổi luật sau khi
thấy điểm**. Với dự án này — đã có một Δ trắng vì thiếu hạt, một nhánh chết ở cổng eligibility, và
hai lần tự khai nới ngưỡng — **đó là thứ đáng mua bằng 72–88 giờ A100.**
