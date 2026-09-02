# 132 — KẾ HOẠCH CHẠY SPRINT `gui_sel` VÀ NỘP SOICT 2026

> Viết 1/9/2026. **Mục đích của file: đưa cho một hội đồng phản biện độc lập soi trước khi bấm
> train.** Mọi con số dưới đây đều có nguồn; chỗ nào là ước lượng đều gắn nhãn ⚠️.
>
> Nguồn đã chốt: `report/123` (bản chép ảnh, phủ tới §3.4) · `report/126` (trả lời máy Mac) ·
> **`report/128` (phán quyết cuối — thắng `126` ở backbone và phạm vi lượt)** · `report/125`
> (trạng thái mã trên WSL) · `report/131` (tình trạng FAIR).
>
> ⛔ **Chưa bấm train lượt nào.** File này là thứ cần được duyệt trước.

---

## 0a. NHẬT KÝ THI HÀNH — cập nhật 2/9/2026

### ✅ Đã xong (0 GPU)

| việc | kết quả |
|---|---|
| Kéo `train.jsonl` + `ocr.jsonl` đầy đủ | 64.567 dòng; ocr md5 **`a7ddf93d18c060e995afa841f039e343`** |
| Dựng khối ứng viên tập dạy | 64.567 màn; khối rỗng **906 = 1,4%** (ngưỡng Limitations 15%) |
| **G1** phủ | **96,4%** (30.912/32.061) ✅ · tập kiểm 96,7% |
| **G2** khớp tên ∧ ±140 | **91,1%** (29.198/32.061) ✅ · tập kiểm 91,2% |
| **G3** rò rỉ | GOLD **0** · hạng **0,481** · P(idx=0) **5,0%** · Spearman **0,047** ✅ |
| **G4** độ dài, đo TOÀN BỘ | `gui_sel` max **1.482** chữ + **1.272** ảnh = **2.754**/3.072 · **tràn 0/64.567** ✅ |
| Ba nhánh dữ liệu | 64.567 mẫu mỗi nhánh · **12 bất biến** đạt |
| Probe 200 mẫu dài nhất | **không OOM** · 13,6 s/bước · loss 2,43 → 0,34 |
| Mã mới | `gate_sel_acc.py` (cổng G6) · `train_config_sel.yaml` · `colab_train_sel.md` |

⭐ **`gui_s1_match` trùng khít `s1.json` từng byte trên cả 64.567 mẫu.** Hai hệ quả: bộ OCR dùng
lần này **đúng là bộ đã dựng S1/S2** (bẫy lệch lượt OCR ở `report/125` §5 không xảy ra), và
`Δ_menu` đo đúng một biến vì S1-match chính là S1 cũ, chỉ khác config train.

### ⏳ Đang chạy

**Lượt 1/6 `gui_sel`/101** — ~771/4036 bước, **12,7 s/bước**, xong khoảng 4–5 h sáng 3/9 giờ VN.
Đã resume từ `checkpoint-600` sau một lần chết ở bước 747.
Tốc độ thật khớp ước lượng: sáu lượt ≈ **79 h**, đúng dự tính 69 h của `report/128`.

### ⛔ Sáu bẫy đã trả giá, đã vá — đừng lặp

1. **Mất 16 compute unit.** `subprocess.Popen` thiếu `start_new_session=True` ⇒ train cùng
   process group với kernel ⇒ bấm Stop một ô bất kỳ là gửi SIGINT sang train.
2. **Ô theo dõi đọc `trainer_log.jsonl` trên Drive** — FUSE không cập nhật khi ghi thêm ⇒ số bước
   đứng yên hàng giờ ⇒ tưởng treo ⇒ bấm Stop. Phải đọc **log local**.
3. **Khẳng định điều chưa kiểm** (*"bấm Stop không ảnh hưởng train"*) — chính câu đó giết lượt.
4. **`--limit` ghi đè tệp thật** — một lượt thử `--limit 30` xoá mất bản 4.463 màn của tập kiểm.
   Đã vá: ghi ra `candidates_thu_<n>.jsonl` / `branches_thu_<n>/`.
5. **Đường dẫn ảnh tương đối** trong khi nhánh cũ dùng tuyệt đối ⇒ chết sau 15–25 phút mã hoá
   token. Bắt buộc `--img-prefix /content/ws/thesis/harness/dg1_cache/train_ac/`.
6. **`infer_branch.py` không truyền `cands`** ⇒ chấm `gui_sel` mà thiếu menu: **499/500 mẫu dựng
   sai câu nhắc**, log không báo gì. Đã thêm cờ `--cands`; sau khi vá, câu nhắc dạy vs chấm trùng
   khít 3.000/3.000 ở cả ba nhánh.
7. **`strip_desc()` chỉ bóc `<desc>`, không bóc `<sel>`** ⇒ `pred` của gui_sel sẽ là chính cái thẻ.
   Đã vá, kiểm 6 ca.

⚠️ **Token ảnh = 1.272**, đo bằng chính `AutoProcessor`. Cách tính chia patch cho 4 (merge 2×2)
ra 318 là **sai gấp bốn lần** — processor không merge ở mức token đầu vào. **Đo, đừng tính.**

---

## 0. TÓM TẮT ĐIỀU HÀNH

| | |
|---|---|
| Venue nhắm | **SOICT 2026** — Springer CCIS, Scopus + EI-Compendex, TP.HCM 4–5/12 |
| Mốc | abstract **9/9** · **full paper 16/9** · báo kết quả 12/10 · camera-ready 23/10 |
| Hôm nay | **1/9** ⇒ còn **8 ngày** tới abstract, **15 ngày** tới full paper |
| Nội dung bài | Sprint `gui_sel`: đưa **khối ứng viên** vào câu nhắc và **đầu chọn `<sel>`** vào mục tiêu sinh |
| Số lượt train | **6** (`gui_sel`, `gui_sft_match`, `S1-match` × hạt 101 và 202) |
| Ngân sách máy | **~69 h A100** + **~34 h chấm**. Hạn mức Kaggle **không còn là ràng buộc** (chủ luận văn xác nhận 1/9) |
| Điểm kỳ vọng | `exec` **63,7–65,1%** so với 59,4 của S1 hiện tại; trần cơ chế **67,2%** |
| ⚠️ Rủi ro đã biết trước | **Δ giữa hai nhánh nhiều khả năng TRẮNG** — đây là chủ đích thiết kế, không phải hỏng |

**Một câu định vị bài:** *khối ứng viên nâng điểm tuyệt đối, đầu chọn `<sel>` là biến được đo.*

---

## 1. VÌ SAO LÀ BÀI NÀY, KHÔNG PHẢI BÀI KHÁC

Ba đóng góp của dự án đã được chia hết cho hai bài vừa nộp:

| đã chiếm | bài |
|---|---|
| Base 47,6 · S1 59,1/59,6 · S2 57,2 · CE2 59,4 · MIN 60,0 · bảng chéo 2×2 · lát 7,3% · toàn bộ thước đo (sàn, bơm lỗi, năm luật, tất định, κ) | **FAIR** (đã gửi, `report/131`) |
| nhãn quy chiếu bốn ô · đường ống dựng dữ liệu · hai bộ lọc · chín bất biến · kiểm rò rỉ | **VCL** (đã nộp) |

⇒ Nguyên liệu **duy nhất** chưa dùng là **nhánh ứng viên**, thứ `report/106` mục (x14) đã đăng ký
và luận văn đã ghi vào hướng phát triển. Không có lựa chọn thứ hai nào không trùng lặp.

⛔ **Ràng buộc cứng:** SOICT đòi bài chưa công bố và không đang xét nơi khác. Bài này phải đứng
được **mà không cần trích FAIR/VCL** — xem mục 12.

---

## 2. CÂU HỎI NGHIÊN CỨU VÀ ĐẠI LƯỢNG ĐO

### 2.1 Hai đại lượng phải tách, đây là gốc của toàn bộ thiết kế

| đại lượng | do cái gì quyết định | vai trò |
|---|---|---|
| **Điểm tuyệt đối** `exec` | **khối ứng viên** trong câu nhắc (menu ≤40 dòng, có tên + toạ độ) | thứ mang đi bảo vệ |
| **Δ_component** | **đầu chọn `<sel>`** trong mục tiêu sinh | thứ đi vào bài như đóng góp mô hình |

Khối ứng viên có ở **cả hai** nhánh nên nó **triệt tiêu trong hiệu số**. Đó là chủ đích: Δ đo đúng
một biến.

### 2.2 Ba estimand

```
Δ_menu   = exec(gui_sft_match) − exec(S1-match)     ← công của KHỐI ỨNG VIÊN
Δ_sel    = exec(gui_sel)       − exec(gui_sft_match) ← công của ĐẦU CHỌN  (đại lượng chính)
Δ_system = exec(gui_sel)       − exec(S1-match)      ← tổng của cả hai
```

Mỗi estimand là **trung bình hai hạt giống**, không phải một lượt.

⭐ **Vì sao phải có `S1-match`:** nếu thiếu nó, tầng dưới buộc phải so với S1 cũ — vốn lệch **ba
biến cùng lúc** (2 epoch vs 1 · cutoff 2560 vs 3072 · không có menu). Đó đúng loại so bắc cầu mà
`123` §9.1 cấm. Có `S1-match` thì được bảng phân rã **ba tầng, mỗi tầng đúng một biến**:

```
S1-match  --[thêm menu]-->  gui_sft_match  --[thêm đầu chọn]-->  gui_sel
```

Kể cả khi Δ_sel trắng, bảng này vẫn đọc được — đó là lý do không rút xuống 4 lượt.

---

## 3. THIẾT KẾ BA NHÁNH

Cả ba dùng **cùng backbone, cùng dữ liệu gốc, cùng câu vàng, cùng luật giải mã**. Khác nhau đúng
như bảng:

| nhánh | câu nhắc có khối ứng viên? | mục tiêu sinh |
|---|---|---|
| `S1-match` | **không** | `[câu]` |
| `gui_sft_match` | **có** | `[câu]` |
| `gui_sel` | **có** | `<sel>k</sel>` rồi `[câu]` |

**Câu nhắc của `gui_sft_match` và `gui_sel` phải byte-identical.** Đây là bất biến phải kiểm bằng
mã sau mỗi lần dựng lại, không phải kiểm bằng mắt.

### 3.1 Khối ứng viên — định nghĩa chốt (`123` §5.1, `126` §7.1)

- Khung xương là **cây trợ năng**. `if not nds: return []` — màn không có a11y ⇒ **khối rỗng**.
  **OCR không cứu**; OCR chỉ **đặt tên** cho node (tâm chữ nằm trong hộp).
- **Node không có tên thì bị loại khỏi khối.**
- Luận văn và bài phải viết: *"ứng viên = node trợ năng **có tên**"*. ⛔ Không dùng `icon#k`.
- Khối rỗng ⇒ in dòng `(không có)`, nhãn train là `<sel>none</sel>`.
- ⚠️ **Nếu tỉ lệ khối rỗng > 15% thì phải đưa vào Limitations.**
- Trần độ phủ: **~22% số bước không có tên vàng trong khối** ⇒ chọn vô nghĩa ở phần đó.

### 3.2 Trần của cơ chế — con số phải nói trước

| | |
|---|---|
| G2 có điều kiện trên `n_gold`=3.505 | **91,2%** |
| G2 vô điều kiện (91,2% × 3.505/4.463) | **71,6%** |
| Phần giao *"có ứng viên vàng trong khối ∩ đang chọn sai"* | **≈704 bước** |
| Cứu hết 704 bước ⇒ `exec` | **≈67,2%** ← **trần của cơ chế** |
| Để đạt 65% cần cứu | **484/704 bước (69%)** — stretch |
| Để đạt 70% cần cứu | **973 > 704** ⇒ ⛔ **bất khả**, đừng hứa |

⇒ **Cấm viết mục tiêu 70%.** Dải hợp lệ để phát biểu là **63,7–65,1%**, trần cứng 67,2%.

---

## 4. DỮ LIỆU

### 4.1 ⛔ CHẶN ĐANG CÓ — phải xử trước mọi thứ khác

| tệp | trên WSL | cần |
|---|---|---|
| `train_ac/train.jsonl` | **1.697** bước | 64.567 |
| `train_ac/ocr.jsonl` | **1.697** màn | 64.567 |
| `train_ac/descriptors.jsonl` | ✅ 41.099 | 41.099 |
| `test_ac/*` | ✅ đủ | — |

`_bundles/derived_train_en.tar.gz` **không cứu được** (chỉ có `descriptors.jsonl` + `branches/`).
**Không dựng ngược được từ `s1.json`**: nó chỉ giữ chuỗi OCR đã nối, trong khi `candidates_of()`
cần **hộp** của từng mục OCR để `name_of()` gán tên. Mất hộp là mất tên ứng viên.

⇒ **Việc số 0: kéo `train.jsonl` + `ocr.jsonl` bản đầy đủ từ Drive (`derived.tar.gz`, ~80 MB).**

### 4.2 ⚠️ BẪY ĐÃ PHÁT HIỆN, KHÔNG CÓ TIẾNG ĐỘNG

So câu nhắc dựng lại trên WSL với **chính câu nhắc trong `s1.json` đã dùng để train**, trên 1.697
bước: **26 bước lệch (1,5%)**, nằm trong chuỗi OCR (`Culture & museums` vs `Culture &museums`).
Tức lát trên WSL được OCR bằng **một lượt khác** với lượt đã dựng dữ liệu dạy thật.

⇒ **Luật: dựng dữ liệu SEL từ đúng bộ `ocr.jsonl` đã dựng S1/S2.** Tên ứng viên đi qua `name_of()`
mà `name_of()` đọc OCR ⇒ đổi lượt OCR là đổi tên ứng viên, mà `<sel>` chép nguyên tên ⇒ đổi cả
nhãn `sel` lẫn `sel_acc`. **Loại hỏng này không báo lỗi, không cảnh báo, chỉ ra số khác.**

### 4.3 Mã đã có

| mã | trạng thái |
|---|---|
| `harness/build_candidates.py` | ✅ có; **phải thêm cờ `--all-steps`** (hiện chỉ ghi bước chạm) |
| `harness/build_sel_data.py` | ✅ có, đã kèm cổng G3 và G4; `gold_candidate()` ở đây là **bản duy nhất** — lúc chấm `sel_acc` phải **import lại**, cấm viết bản thứ hai |

---

## 5. CẤU HÌNH TRAIN — CHỐT

| khoá | giá trị | nguồn |
|---|---|---|
| backbone | **Qwen2.5-VL-3B-Instruct** | `128` §3 — đảo quyết định của `126`, giữ 3B |
| lượng hoá | QLoRA 4-bit NF4 | như S1/S2 |
| vision tower + projector | **đóng băng** | |
| cutoff | **3072** (S1/S2 cũ là 2560) | `128` §4 |
| epoch | **1** | |
| lr | 1e-4, cosine | |
| lô hiệu dụng | 16 | |
| hạt giống | **101 và 202, chạy vô điều kiện** | `126` §0 |

⛔ **Không hạ epoch** (đã 1). ⛔ **Không hy sinh hạt giống thứ hai** — đó chính là đòn đã hạ bài
FAIR xuống borderline.

### 5.1 Vì sao **không** đổi sang Qwen3-VL-4B (`128` §3)

① Trần cơ chế **67,2%** bị chặn bởi **độ phủ khối ứng viên**, không phụ thuộc backbone; lát chọn
đúng đã bão hoà (MIN **85,2%** vs người **85,7%**) ⇒ đổi backbone mua tối đa **~2 pp**.
② Căn cứ đổi là ScreenSpot-v2 — benchmark **định vị** — trong khi mô hình này **không định vị**
(UGround làm việc đó).
③ Giữ 3B mới đủ ngân sách cho `S1-match`, tức mới tách được công của menu.
④ 4B chưa từng chạy, giờ/epoch chưa đo, kịch bản xấu 112–148 h là vỡ ngân sách.

---

## 6. BỘ CỔNG — chạy theo thứ tự, cổng nào trượt thì dừng

| cổng | đo gì | ngưỡng | khi nào | GPU |
|---|---|---|---|---|
| **G1** | độ phủ — tên vàng có trong khối | ≥95% | trước dựng data | 0 |
| **G2** | khớp tên ∧ trong ±140 | ≥75% | trước dựng data | 0 |
| **G3** | **rò rỉ**: (a) chuỗi `GOLD`/`gold` trong câu nhắc = **0**; (b) hạng chuẩn hoá của ứng viên vàng, mean ∈ **[0,40 · 0,60]**; (c) **P(idx=0) ≤ 8%**; (d) Spearman \|ρ\| giữa `idx` và `L2(cand,gold)` ≤ **0,10** | như cột trái | sau dựng data, 300 mẫu | 0 |
| **G4** | độ dài token trên **200 mẫu dài nhất**, tokenizer **Qwen2.5-VL**, cutoff **3072** | không tràn | sau dựng data | 0 |
| **G5b** | pilot 200 bước lấy **giờ/epoch thật** | — (chỉ để biết) | trước lượt đầu | ~1 h |
| **G6** | `sel_acc` trên **600 bước DEV** có ứng viên vàng; khớp tên ∧ point ±14%; `<sel>none</sel>` tính **sai** | **≥63,6%** | sau lượt `gui_sel`/101 | chấm |
| **G9** | đọc mù ảnh + mù khối, n ≥ **2.000** | — | phân tích | 0 |
| **G10** | chênh tỉ lệ câu chứa **tên nguyên văn**: \|sel − match\| ≤ **2 pp** | ≤2 pp | phân tích | 0 |
| **G11** | trọng tài **khác họ**: OS-Atlas-Base-4B (Phi-3) hoặc GLM-4.6V-Flash. ⛔ **không** OS-Atlas-7B (vẫn Qwen) | — | nếu còn thời gian | chấm |

⚠️ **G1/G2 đã ĐẠT trên tập kiểm** (96,7% và 91,2%, `report/125` §2) nhưng **chưa chạy trên tập
dạy** vì thiếu dữ liệu — xem mục 4.1.

⚠️ **G10 siết từ 10 pp xuống 2 pp** có lý do số học: artefact 10% × 28,5 pp = **+2,85 pp**, vượt
ngưỡng Dương +2,8 ⇒ một artefact chép tên có thể tự tạo ra "kết quả dương" giả. Phải báo Δ **phân
tầng** theo có/không chép tên nguyên văn.

---

## 7. THƯỚC ĐO VÀ LUẬT ĐỌC KẾT QUẢ

### 7.1 Thước — KHÔNG ĐỔI

`exec` = executability, chấm bằng UGround-V1-2B, luật Voronoi trên tâm phần tử, ngưỡng dung sai
14% theo từng trục. **Cùng thước đã dùng cho Base/S1/S2/CE2/MIN** ⇒ số so được trực tiếp.

⛔ **Không đổi thước, không đổi bộ trỏ.** Hai hướng đó đã có số bác (`128` §5): Voronoi đã là luật
cho trần cao nhất; và bộ trỏ mạnh hơn (UI-Venus-7B) cho điểm **thấp hơn** ở cả ba nhánh.

✅ **Được làm, 0 giờ GPU:** báo thêm `exec` dưới **luật chữ nhật 14% kiểu AITW** làm **thước
đồng-báo**, tính lại từ tệp thô. Để so với quy ước lĩnh vực, **không** để đọc đóng góp.

### 7.2 Luật đọc Δ_sel — phải khoá TRƯỚC khi train

| kết cục | điều kiện | cách viết |
|---|---|---|
| Dương | Δ ≥ **+2,8 pp** và KTC loại 0 | claim đóng góp |
| Dương yếu | **+1,7 ≤ Δ < +2,8** | trend, không claim |
| **Trắng** | **−2,8 < Δ < +1,7** | báo thẳng là chưa phân giải |
| Âm | Δ ≤ −2,8 và KTC loại 0 | báo thẳng |

⚠️ **Δ nhiều khả năng rơi TRẮNG. Đó là chủ đích, không phải hỏng.** Phải nói câu này trong bài,
không giấu.

⛔ **Bốn cách kéo Δ cho đẹp đều bị cấm:**
- bỏ khối ứng viên khỏi đối chứng (so với S1 hoặc 24 dòng OCR) — khác **hai** biến;
- so `gui_sel` thẳng với S1 cũ — `123` §9.1 cấm;
- train ORPO để mong Δ ≥ +2,8 — số của chính dự án đã bác (`128` §2);
- đổi luật Voronoi / ép tên / bỏ vị trí.

### 7.3 Cách trình điểm tuyệt đối (`128` §5.3)

Thước chạy từ **12,0** (câu vô nội dung) tới **75,7** (câu người viết). ⛔ **Đừng đọc 63–65% trên
nền 100.**

| nhánh | exec | % của trần người |
|---|---|---|
| Base | 47,59 | 62,8% |
| S1/101 | 59,11 | 78,0% |
| MIN-DESC | 60,05 | 79,3% |
| **`gui_sel` kỳ vọng** | **63,7–65,1** | **84,1–86,0%** |

Câu đi bảo vệ: *"câu do mô hình sinh ra đạt 84–86% năng lực của câu do người viết, trên cùng một
phép đo"*.

---

## 8. LỊCH — 15 NGÀY, GIẢ ĐỊNH KAGGLE KHÔNG CÒN LÀ RÀNG BUỘC

| ngày | việc | GPU | phụ thuộc |
|---|---|---|---|
| **1/9** | kéo `train.jsonl` + `ocr.jsonl` từ Drive; thêm cờ `--all-steps` | 0 | ⛔ chặn mọi thứ sau |
| **2/9** | `build_candidates.py --split train` → `build_sel_data.py --split train`; chạy **G1 · G2 · G3 · G4** | 0 | |
| **2/9 tối** | **G5b** pilot 200 bước lấy giờ/epoch thật | ~1 h | |
| **3–7/9** | train **6 lượt** tuần tự | ~69 h | ⚠️ Colab mất máy |
| **6–9/9** | chấm cuốn chiếu, lượt nào xong train thì chấm ngay | ~34 h | chạy song song với train |
| **9/9** | 🎯 **nộp abstract SOICT** | 0 | dùng số hạt 101 nếu đã có |
| **10/9** | **G6 · G9 · G10**; phân tích; bảng phân rã ba tầng | 0 | |
| **11–12/9** | viết bài | 0 | |
| **13–15/9** | đệm: mất máy, chạy lại, đọc soát | | |
| **16/9** | 🎯 **nộp full paper** | | |

**Đệm 3 ngày.** Chỗ dễ vỡ nhất là 3–7/9: nếu tới **10/9** mà chưa có đủ 4 lượt về đích thì kích
hoạt phương án lùi (mục 10).

⚠️ Số 69 h là **ước lượng suy ra** (46 h/4 lượt cho cặp chính; `S1-match` suy theo tỉ lệ), **chưa
phải số đo**. G5b sẽ cho số thật — **đó là điểm quyết định đầu tiên**.

---

## 9. NGÂN SÁCH MÁY

| gói | lượt | A100 | chấm |
|---|---|---|---|
| `gui_sel` / `gui_sft_match` × hạt 101, 202 | 4 | ~46 h | ~22 h |
| `S1-match` × hạt 101, 202 | 2 | ~23 h ⚠️ | ~11 h |
| **tổng chốt** | **6** | **~69 h** | **~34 h** |
| *(tuỳ chọn cuối)* MIN/202 + CE2/202 | 2 | ~13,5 h ⚠️ | ~11 h |

MIN/202 + CE2/202 **không nằm trong kế hoạch này**: nó tốn 13,5 h + 11 h để xác nhận một con số
đã biết (+0,63 pp), gần chắc vẫn rơi ô trắng, không nâng điểm, không đổi bảng bảo vệ.

---

## 10. RỦI RO VÀ PHƯƠNG ÁN LÙI

| # | rủi ro | dấu hiệu sớm | phương án |
|---|---|---|---|
| R1 | **Không kéo được dữ liệu Drive** | ngay 1/9 | chạy `build_candidates` + `build_sel_data` trên Colab CPU sau khi bung `derived.tar.gz` |
| R2 | **G5b cho giờ/epoch vượt dự tính** | 2/9 | cắt `S1-match` xuống 1 hạt, hoặc lùi sang venue sau |
| R3 | **Colab mất máy nhiều** (tiền lệ: 8 lần trong 2 lượt S1) | liên tục | đồng bộ Drive mỗi 5 phút; chụp định kỳ sang **tên khác** bằng `cp` |
| R4 | **G3 trượt** (khối ứng viên rò rỉ đáp án) | 2/9 | ⛔ **DỪNG** — kết quả sẽ vô giá trị; phải sửa cách xếp khối rồi chạy lại |
| R5 | **G6 trượt** (`sel_acc` < 63,6%) | sau lượt đầu | báo thẳng là cơ chế không học được; bài đổi thành báo cáo âm |
| R6 | **Tỉ lệ khối rỗng > 15%** | 2/9 | vẫn chạy, nhưng bắt buộc vào Limitations |
| R7 | **Δ trắng** | cuối | ✅ **đã lường trước** — trình theo bảng ba tầng + điểm tuyệt đối |
| R8 | **Không kịp 16/9** | 10/9 | nộp abstract rồi rút; chuyển sang venue sau, chạy đủ 6 lượt |

⚠️ **R4 là cổng dừng thật sự.** Nếu khối ứng viên vô tình nói cho mô hình biết đáp án nằm đâu
(thứ tự, phép cắt, vị trí) thì mọi con số sau đó là rác. G3 phải chạy **trước** khi tiêu một giờ
GPU nào.

---

## 11. PHÙ HỢP VỚI SCOPE LUẬN VĂN KHÔNG?

**Có, và đây là nhánh đã đăng ký sẵn.**

- `report/106` mục **(x14)** đã đăng ký ba nhánh tiếp: **ứng viên · lùi · MIX**. Nhánh này là cái
  thứ nhất.
- Luận văn chương 7 (hướng phát triển) **đã ghi** ba nhánh đó cộng việc hoàn tất hạt giống thứ hai.
- Chương 6 hiện dừng ở MIN-DESC. Kết quả sprint này **bổ sung được một mục** vào chương 6 và
  **chuyển chương 7 từ "dự định" sang "đã làm"**.
- Thước đo không đổi ⇒ số mới **so trực tiếp** được với bảng chính hiện có, không phải đo lại gì.

⚠️ **Chỗ cần chủ luận văn quyết:** sprint này làm luận văn dày thêm nhưng cũng **đẩy lịch bảo vệ**.
Nếu lịch bảo vệ gấp thì cân nhắc chỉ chạy 4 lượt (bỏ `S1-match`) cho luận văn và để bài SOICT lại.

---

## 12. CHỐNG TRÙNG LẶP VỚI FAIR VÀ VCL

SOICT đòi bài **chưa công bố, không đang xét nơi khác**. FAIR đang chờ phản biện, VCL đã nộp.

| nội dung | thuộc bài nào | được dùng ở SOICT? |
|---|---|---|
| Base 47,6 · S1 59,1/59,6 · S2 57,2 · CE2 · MIN · bảng chéo 2×2 · lát 7,3% | FAIR | ⚠️ **chỉ một dòng mốc so sánh**, không tả lại thí nghiệm |
| sàn 12,0/6,1 · bơm lỗi · năm luật · tất định · κ | FAIR | ⚠️ **một câu** mô tả thước + trích, không tả lại hiệu chuẩn |
| nhãn quy chiếu bốn ô · đường ống dữ liệu · chín bất biến | VCL | ⚠️ **một câu**, không tả lại |
| **khối ứng viên · đầu chọn `<sel>` · ba nhánh mới · G1–G11 · bảng phân rã ba tầng** | **SOICT, độc quyền** | ✅ |

⛔ **Vấn đề chưa giải:** cả FAIR lẫn VCL đều chưa có ID/DOI, nên **không trích chéo được**. Bài
SOICT phải tự mô tả đủ thước đo và dữ liệu **mà không viện dẫn hai bài kia** — giống hệt tình
huống vừa gặp ở FAIR khi gỡ `\cite{companion}` (`report/131` mục 6).
⇒ **Câu hỏi cho hội đồng phản biện: cách xử nào đúng ở đây?**

---

## 13. ĐIỀU CẤM — mang nguyên từ các phán quyết đã có

1. ⛔ Không claim **"cơ chế mới"** cho khối ứng viên. Đưa danh sách phần tử vào đầu vào **đã có
   tiền lệ**: bài gốc AndroidControl fine-tune với danh sách a11y làm input; Mind2Web xếp hạng ứng
   viên trước khi sinh; Geng EMNLP 2023.
2. ⛔ Không dùng `icon#k` hay bất kỳ định danh tự chế nào cho node không tên — node không tên **bị
   loại khỏi khối**.
3. ⛔ Không hứa mục tiêu **70%** — cần cứu 973 bước trong khi chỉ có 704.
4. ⛔ Không đổi thước, không đổi bộ trỏ, không nới ngưỡng sau khi thấy điểm. Dự án đã tự khai
   **hai lần** nới ngưỡng sau khi thấy điểm; lần thứ ba là hết tín nhiệm.
5. ⛔ Không đăng ký τ / hai lượt / G7-cổng / abstention làm đóng góp chính (`126` §8).
6. ⛔ Không viết `sel_acc` như headline — nó là **thước phụ**; headline là `exec`.
7. ⛔ Không giấu chuyện Δ có thể trắng.

---

## 14. CÂU HỎI MỞ — GỬI HỘI ĐỒNG PHẢN BIỆN

1. **Bài SOICT có đủ đóng góp không nếu Δ_sel trắng?** Lúc đó bài còn: điểm tuyệt đối 63–65%
   (+4–6 pp so với S1), bảng phân rã ba tầng, `sel_acc`, và trần cơ chế 67,2%. Đủ cho Springer
   CCIS chưa, hay nên đợi có kết quả dương?
2. **Đóng góp chính nên đóng khung là gì** — "khối ứng viên nâng điểm" (đầu vào, có tiền lệ) hay
   "đầu chọn tường minh" (mục tiêu sinh, là biến đo)? Cái thứ nhất mạnh về số nhưng yếu về tính
   mới; cái thứ hai ngược lại.
3. **Không trích chéo được FAIR/VCL thì xử sao?** Tả lại thước đo trong bài SOICT có bị coi là tự
   đạo văn khi FAIR được nhận không?
4. **15 ngày với 6 lượt train có thực tế không**, khi tiền lệ là Colab ăn mất 18 giờ trong hai lượt
   S1?
5. **G6 ngưỡng 63,6% lấy ở đâu ra**, và nếu trượt sát ngưỡng (ví dụ 62%) thì dừng hay chạy tiếp?
6. **Có nên chạy `S1-match` không**, hay 46 h cho bốn lượt rồi dồn thời gian còn lại vào viết bài
   cho kỹ?
7. **Thứ tự ưu tiên khi vỡ lịch**: hy sinh hạt giống thứ hai, hy sinh `S1-match`, hay lùi venue?
   (Tiền lệ FAIR cho thấy hy sinh hạt giống thứ hai là đắt nhất.)
