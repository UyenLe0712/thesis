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

---

## 15. Cache token — cắt 41 phút mỗi lần dựng lại máy (soạn 3/9, CHƯA ÁP)

**Vấn đề đo được.** Mỗi lần mất máy, khâu đắt nhất không phải số bước train mất đi mà là
**mã hoá token lại từ đầu: 41 phút** cho 64.567 mẫu (đo 2/9, 11:58 → 12:39, `num_proc=8`).
Với `save_steps: 100` thì bước mất chỉ ~21 phút ⇒ **khâu mã hoá đắt gấp đôi phần train mất**.
Đêm 2–3/9 trả giá này hai lần.

**Cách chữa.** LLaMA-Factory có `tokenized_path`: chưa có thì mã hoá rồi lưu, đã có thì nạp
thẳng. Đặt trên Drive để sống qua mất máy:

```yaml
tokenized_path: /content/drive/MyDrive/thesis/tokcache/<nhánh>_cut3072_qwen25vl
```

**⛔ Ba rủi ro phải chặn trước khi bật — đây là đúng loại lỗi câm dự án đã trả giá nhiều lần
(dataset Kaggle giữ bản mã cũ, ô vá sửa nhầm lớp):**

1. **LLaMA-Factory KHÔNG kiểm cache có khớp cfg hay không.** Đổi `cutoff_len`, đổi `dataset`,
   đổi `template` mà giữ nguyên path ⇒ nó nạp cache cũ, train trên dữ liệu khác, **log không
   báo gì**. Chặn bằng cách nhét cả ba thứ vào tên thư mục, và **một nhánh một thư mục**.
2. **Cache của nhánh này không được dùng cho nhánh kia.** Ba nhánh khác nhau ở câu nhắc và
   đích sinh, tức khác từ token đầu tiên. Trộn cache là hỏng toàn bộ Δ.
3. **Dung lượng.** Ước ~0,5–1 GB một nhánh (64.567 mẫu × ~1.800 token). Ba nhánh ⇒ tối đa
   ~3 GB trên Drive. Phải kiểm chỗ trống trước, và ghi lần đầu qua FUSE mất thêm ~5–10 phút.

**Phép kiểm bắt buộc trước khi tin cache** (một lượt sạch, không tiêu GPU train):
· lần chạy đầu phải in `Saving tokenized dataset to ...` và thư mục phải có tệp Arrow;
· lần chạy sau phải in `Loading tokenized dataset from ...` và **bỏ qua** thanh
  `Running tokenizer`;
· mẫu in ra ở đầu log (LLaMA-Factory in một mẫu đã token hoá) phải **trùng** giữa hai lần —
  so bằng mắt đúng dòng `input_ids` đầu.

**Khi nào áp:** từ **lượt 2** (`gui_sft_match`/101) trở đi. ⛔ Không áp giữa chừng cho lượt 1
đang chạy — đổi cfg của một lượt dở là thêm một biến không kiểm soát, đúng thứ mục §9.1 cấm.

**Khoá cfg:** `tokenized_path` phải vào danh sách khoá được phép đổi giữa lượt của ô S3
(cùng nhóm với `dataset` / `seed` / `output_dir`), vì nó đổi theo nhánh.

---

## 16. ⛔ CỔNG G6 TRƯỢT — kết quả đo 3/9/2026, sprint DỪNG theo luật §5

**`sel_acc` = 580/1008 = 57,5%**, ngưỡng khoá trước là **63,6%** ⇒ **TRƯỢT, kém 6,1 điểm.**
Không phải trường hợp sát ngưỡng mà mục 14 câu 5 để ngỏ. ⛔ Không nới.

Tệp: `runs/sel/preds_gui_sel_seed101_dev1400.jsonl` (1.400 bước chạm, chữ ký
`lora:gui-sel-adapter`). Chấm bằng `SEL_SPLIT=test python3 harness/gate_sel_acc.py`.

### Ba phép xác minh trước khi tin con số

| phép | kết quả |
|---|---|
| `raw` có thẻ `<sel>` | **1400/1400 = 100%** — định dạng đúng như dạy |
| tên chọn nằm trong khối ứng viên | **814/817 = 99,6%** — câu nhắc CÓ menu, mô hình thật sự chọn từ danh sách |
| cỡ mẫu trong phạm vi cổng | **1.008** bước, lớn hơn 600 mà §5 yêu cầu |

⚠️ `--limit 1400` cho **1.400 bước CHẠM** rải trong 2.221 bước đầu, không phải 1.400 bước
đầu — nên n=1008 chứ không phải 694 như ước lượng trước lúc chạy.

### ⭐ Cơ chế CÓ học được — đây là phần đáng viết nhất

| nhóm | n | mô hình trả `none` | nhãn đúng |
|---|---|---|---|
| chạm · **không** có tên vàng | 288 | **80,2%** | `none` ✓ |
| chạm · có tên, không khớp ứng viên nào | 104 | **74,0%** | `none` ✓ |
| chạm · **có** ứng viên vàng | 1.008 | **27,1%** | CHỌN ✓ |

Khoảng cách **80,2% so với 27,1%** loại bỏ giả thuyết *"mô hình tái tạo prior"* — prior của
bước chạm trong tập dạy là 29,1% `none`, mà mô hình cho ra hai tỉ lệ khác hẳn nhau tuỳ nhóm.
Đọc như bộ phân loại nhị phân *"có nên chọn không"*: recall **72,9%** · specificity **78,6%**
· đúng **74,5%** trên 1.400 bước.

### Phân rã điểm mất

```
sel_acc 57,5%  =  72,9% (dám chọn)  ×  78,9% (chọn đúng khi đã dám)
```

Trong 735 lần dám chọn: **580 đúng cả tên lẫn điểm** · 46 điểm đúng tên sai · **4 tên đúng
điểm sai** · 103 sai cả hai. Con số 4 đáng chú ý: khi đã nhận ra phần tử thì lấy toạ độ gần
như luôn chuẩn ⇒ điểm nghẽn nằm ở **nhận diện**, không ở định vị.

Để chạm 63,6% cần một trong hai: giữ 78,9% đúng thì phải dám chọn **≥80,6%**; hoặc giữ 72,9%
dám chọn thì phải đúng **≥87,2%**. Cả hai cách hiện tại 8 điểm.

### Điều gì phân biệt bước bỏ cuộc với bước dám chọn

| trục | bỏ cuộc (n=273) | dám chọn (n=735) | chênh |
|---|---|---|---|
| số ứng viên trong khối | 26,5 | 22,2 | **+4,3** |
| thứ tự ứng viên vàng trong khối | 11,2 | 8,5 | **+2,6** |
| tên vàng **có chữ số** | 24,2% | 13,6% | **+10,6 pp** |
| tầng `ky_hieu` (n=34) | — | — | bỏ cuộc **52,9%** |
| độ dài tên · trùng tên · cùng vai · nguồn tên (OCR/a11y) | — | — | **không khác** |

Nguồn tên **không** phân biệt (OCR 27,1% · a11y 27,0%) ⇒ không phải lỗi của khâu lấy tên.
Ba trục có tín hiệu đều chỉ về một hướng: **khối càng đông và tên càng khó đọc thì càng bỏ cuộc**.

### Dữ liệu dạy KHÔNG tự mâu thuẫn

`build_sel_data.py:139` gán `none` **chỉ khi** `gold_candidate()` trả None ⇒ mọi bước có ứng
viên vàng đều mang nhãn chọn. Đo trên tập dạy: 41.191 bước chạm · 77,8% có tên vàng · 70,9%
có ứng viên vàng ⇒ **8,9% số bước có tên vàng vẫn mang nhãn `none`** vì tên không khớp ứng
viên nào. Đó là nhiễu có thật nhưng nhỏ, không đủ giải thích 27,1%.

Cấu tạo 54,8% nhãn `none` của tập dạy: 36,2% bước không chạm · 14,1% chạm không tên vàng ·
4,4% chạm có tên mà không khớp.

### Hệ quả

⛔ **Năm lượt còn lại KHÔNG chạy** (~55 giờ Kaggle + ~46 giờ A100 không phải tiêu). Cổng làm
đúng việc nó sinh ra để làm.
⛔ **Không có `Δ_sel`** — `gui_sft_match` chưa train nên không có đối chứng. Mọi con số ở đây
là **mô tả một nhánh**, không phải hiệu số. Cấm so `gui_sel` với S1 cũ: lệch ba biến
(2 epoch vs 1 · cutoff 2560 vs 3072 · không menu), đúng loại so bắc cầu mà §9.1 cấm.
⚠️ Một hạt giống, một lượt. Mọi số mang nhãn **thăm dò**.

---

## 17. Phép thử ÉP CHỌN và điều nó phát hiện (3/9/2026)

**Câu hỏi:** 273 ca bỏ cuộc là *dè dặt quá mức* hay *thật sự không biết*?
**Cách làm:** cờ `--force-sel` của `infer_branch.py` cấm mọi cách viết `none` lúc sinh, chạy
lại đúng 273 khoá đó (`runs/sel/bo_cuoc_273.jsonl`), ~12 phút Kaggle T4, 0 đồng.
**Kết quả:** `sel_acc` **116/273 = 42,5%**. Nằm giữa hai thái cực ⇒ bỏ cuộc là **tín hiệu
thật** (42,5% thấp hơn hẳn 78,9% của nhóm tự nguyện chọn) nhưng **quá tay** (42,5% vẫn hơn
0% mà `none` mang lại). Tệp: `runs/sel/preds_gui_sel_forcesel_273.jsonl`, chữ ký
`lora:gui-sel-adapter+forcesel`.

### ⛔ Ép chọn LỖ ở mọi ngưỡng — hướng này đã chết

| chỉ ép khi khối ≥ | số ca bị ép | lãi nhóm A | lỗ nhóm B+C | so nền |
|---|---|---|---|---|
| 0 (ép tất) | 581 | +116,0 | −308 | **−13,7 pp** |
| 15 | 440 | +90,0 | −226 | −9,7 pp |
| 25 | 312 | +70,0 | −162 | −6,6 pp |
| 35 | 223 | +50,0 | −122 | −5,1 pp |
| **không ép** | 0 | 0 | 0 | **0,0 pp ← tốt nhất** |

Nền: **888/1400 = 63,4%** đúng trên bước chạm. Lý do lỗ: trong 581 ca abstain chỉ **47%**
thuộc nhóm A, mà điều kiện hoà vốn đòi **69,4%** (mỗi ca chuyển được thêm 0,44 điểm kỳ vọng,
mỗi ca abstain đúng bị phá mất 1,00). ⇒ Quy tắc cứng dựa trên đặc trưng bề mặt không cứu
được; phải có **điểm tin cậy liên tục**.

### ⭐ Điểm nghẽn là NHẬN DIỆN, không phải ĐỊNH VỊ — tỉ số 34:1

Phân rã 273 ca ép chọn: đúng cả hai **116** · **điểm đúng tên sai 34** · **tên đúng điểm sai
1** · sai cả hai 122. Ở nhóm tự nguyện chọn cũng vậy: 580 đúng · 46 điểm-đúng-tên-sai · **4**
tên-đúng-điểm-sai. Hai lát độc lập cùng cho tỉ số ~34:1 và ~11:1 nghiêng về lỗi tên.
⇒ Khi mô hình nhận ra phần tử thì toạ độ gần như luôn chuẩn. Cấm viết *"điểm nghẽn ở định vị
thị giác"* — số liệu bác thẳng.

### ⭐⭐ TÁI LẬP ĐỘC LẬP dạng lỗi lưỡng cực của MIN-DESC

122 ca sai cả hai: khoảng cách tới ứng viên vàng **p25 268 · trung vị 398 · p75 570** trên
lưới 1000 (dung sai 140). Chỉ **25,8%** nằm trong hai lần dung sai ⇒ khi sai, mô hình
**không lẫn sang nút bên cạnh mà nhìn sang vùng khác hẳn màn hình**.

Đối chiếu `report/106` mục (x13c) đo trên nhánh MIN-DESC ngày 25/8: khoảng cách phần-tử-nhầm
↔ gold có **p25 70 px · trung vị 351 · p75 748**, và **76,5%** nằm ngoài dải 80–350.
⇒ **Hai can thiệp khác nhau, hai cơ chế khác nhau, hai lượt train khác nhau, cùng một dạng
lỗi.** Đây là bằng chứng mạnh hơn bất kỳ con số âm nào, và nó giải thích luôn vì sao
MIN-ONPOLICY chết ở cổng eligibility 3,3%: tiền đề "vế âm khó là nút cạnh bên" sai ở cả hai
nhánh.

⚠️ 98,2% tên mô hình chọn nằm trong khối ứng viên ⇒ nó thật sự đọc danh sách, không bịa.

### Đặc trưng nào dự báo bỏ cuộc

| trục | bỏ cuộc | dám chọn | phán |
|---|---|---|---|
| **cỡ khối** | 18,8% → 25,0% → 32,9% → **34,9%** theo bốn tầng | — | **biến thật, đơn điệu, chênh 16 pp** |
| vị trí tương đối trong danh sách | 0,478 | 0,471 | **vô can** (chênh 0,006) |
| tên có chữ số | 24,2% | 13,6% | tín hiệu yếu |
| độ dài tên · trùng tên · cùng vai · nguồn tên | — | — | không khác |

⚠️ Hiệu ứng vị trí thô (11,2 vs 8,5) **hoàn toàn do cỡ khối** — khối đông thì vị trí trung
bình tự động sâu hơn. Phải phân tầng trước khi đọc. Dấu vết *lost in the middle* còn lại rất
nhẹ: bỏ cuộc theo ngũ phân vị vị trí là 25,7 / 24,4 / 31,7 / 34,8 / 24,2%.

**Nghịch lý dùng được:** khối lớn khiến bỏ cuộc nhiều nhất (34,9%) nhưng khi ép chọn trên
khối lớn lại đúng nhiều nhất (**49,5%** so với 31,2% ở khối 15–24) ⇒ ở đúng chỗ khó nhất,
mô hình dè dặt quá tay.

---

## 18. ⭐ VÌ SAO MÔ HÌNH BỎ CUỘC — hai nguồn, nguồn lớn nhất tái lập chẩn đoán 4j-18

Phép kiểm 0 GPU, đọc chính câu hướng dẫn mà mô hình sinh kèm mỗi ca `<sel>none</sel>` sai.

| | 273 ca **bỏ cuộc** | 735 ca **dám chọn** | chênh |
|---|---|---|---|
| câu mang động từ **không chạm** (swipe · back · type · scroll) | **108 = 39,6%** | 15 = **2,0%** | **+37,5 pp, gấp 20 lần** |
| câu mang động từ chạm (tap · click · select) | 142 = 52,0% | — | — |
| không rõ | 23 = 8,4% | — | — |

Ví dụ thật ở nhóm bỏ cuộc: *"Swipe up to view the Symphony of the Seas Cruise."* ·
*"Type 9877655532 in the phone number section."* · *"Go back to the previous page"* — trong
khi thao tác vàng của cả ba bước ấy là một cú **chạm**.

⭐ **Tái lập chẩn đoán 4j-18** (`report/110`, đo tháng 8 trên nhánh S2): nhóm 325 bước không
kích hoạt khai báo cũng đúng kiểu này, và **Base đoán đúng loại thao tác nhiều hơn CẢ HAI bản
đã huấn luyện** (83,4% vs S1 55,1% vs S2 38,8%) ⇒ đây là **cái giá của SFT**, nay thấy lại
trên một nhánh khác, một cơ chế khác, một lượt train khác.

### Nhưng đó KHÔNG phải nguyên nhân duy nhất

Ép chọn, tách theo việc lượt gốc có lẫn loại thao tác hay không:

| nhóm | ép chọn đúng |
|---|---|
| có lẫn loại thao tác (n=108) | **37,0%** |
| không lẫn (n=165) | **46,1%** |
| *(mốc so: nhóm tự nguyện chọn)* | *78,9%* |

Chênh chỉ **9 pp**, và nhóm không lẫn vẫn xa 78,9% ⇒ bỏ cuộc thừa có **ít nhất hai nguồn
chồng lên nhau**: lẫn loại thao tác (dấu hiệu mạnh, chiếm 39,6% số ca) và không nhận ra phần
tử (phần còn lại). Cấm viết *"bỏ cuộc là do lẫn loại thao tác"* — số liệu chỉ cho phép nói
*"lẫn loại thao tác là dấu hiệu mạnh nhất đo được của việc bỏ cuộc"*.

### Hệ quả thiết kế, dành cho bài sau

Nhãn `<sel>none</sel>` hiện **gộp hai tình huống khác bản chất**: bước không chạm (36,2% tập
dạy) và bước chạm nhưng không có tên vàng (18,5%). Mô hình không được cho biết loại thao tác,
mà chính SFT lại làm hỏng khả năng đoán loại thao tác. Tách `none` thành hai đích là hướng
chữa có căn cứ, nhưng đòi dựng lại dữ liệu và train lại cả hai nhánh ⇒ **ngoài ngân sách hiện
tại**, ghi vào hướng phát triển.

## 19. PHÁN QUYẾT HƯỚNG ĐI (chốt 3/9, sau năm hướng research và một vòng phản biện)

### Việc phải làm, theo thứ tự

| # | việc | giờ GPU | cơ sở |
|---|---|---|---|
| 1 | **Ngưỡng τ kiểu Devlin** trên `log p(none) − log p(ứng viên tốt nhất)` tại bước quyết định. Quét τ trên lát 1.400 (dev), chọn theo **đúng toàn bộ** chứ không theo `sel_acc`, áp **một lần** lên 3.063 bước hold-out | 0 A100 · ~2 h T4 | Devlin et al. NAACL 2019 (SQuAD 2.0, `ŝ_null + τ` chọn trên dev) · Kamath ACL 2020 (+8 pp coverage) |
| 2 | **Đếm tên ngoài khối** ở 149 ca chọn sai | 0 | ✅ đã đo trên lát ép chọn: **98,2% nằm trong khối** ⇒ trie gần như vô giá trị |
| 3 | **Chấm executability** cho `gui_sel`/101 trên 4.463 bước | 5,6 h Kaggle | G6 chỉ là cổng proxy; `exec` mới là estimand thật |
| 4 | ✅ **Kiểm giả thuyết lẫn loại thao tác** | 0 | xong, mục 18 |

### ⛔ Không làm, mỗi thứ một lý do đo được

· **focal loss** — Li et al. ACL 2020 đo ở tỉ lệ 82:1 chỉ được +0,30 F1, dưới σ hạt giống 0,46
· **loại bớt mẫu lớp đa số** — Tayyar Madabushi NLP4IF 2019: −1,1 pp khi train/test cùng phân bố; Henning EACL 2023: ROS thắng RUS
· **đánh số ứng viên rồi sinh số** — lệch train-test, và Robinson & Wingate ICLR 2023 báo mô hình cỡ nhỏ nằm sát mức đoán ngẫu nhiên ở năng lực này
· **tách hai giai đoạn** — không có bằng chứng bình duyệt so trực tiếp, tốn 1–2 lượt
· **trie** — 98,2% tên đã nằm trong khối, không còn gì để cấm
· **self-consistency** — thừa khi đã có xác suất trực tiếp từ logits
· **ép chọn** — lỗ ở cả bốn ngưỡng (mục 17)

### Phân bổ hai lượt train còn lại

⚠️ Luật khoá nói trượt G6 thì **dừng sprint sáu lượt**, và điều đó giữ nguyên. Nhưng luật dừng
*sprint*, không cấm dùng ngân sách cho câu hỏi khác — **với điều kiện ghi thành mục sửa đổi và
commit TRƯỚC khi bấm train**.

| lượt | nhánh | giờ | vì sao |
|---|---|---|---|
| 1 | **`gui_sft_match`/101** | ~23 h | không có nó thì báo cáo âm chỉ nói được "trượt một ngưỡng", không nói được đầu chọn có làm `exec` tệ đi hay không |
| 2 | **`gui_sel`/202** | ~23 h | σ giữa hạt giống trên `sel_acc` **chưa ai đo**; con số trung tâm của bài (57,5% và bỏ cuộc thừa) cần hạt thứ hai |
| 3 | **không chạy** | — | giữ làm đệm mất máy; 46 giờ trước 16/9 đã hết chỗ trượt |

⛔ Bỏ `S1-match` và `gui_sft_match`/202. Δ_sel một hạt giống nằm dưới MDE 2,11 **theo thiết
kế**, phải khai là trắng ngay từ đầu.

### Trục đóng góp SOICT — nộp bản SHORT 8–11 trang

*(i)* Kiểm định theo thiết kế đăng ký trước một đầu chọn tường minh trên khối ứng viên cho
Qwen2.5-VL-3B ở miền di động; nó **trượt cổng đã khoá** (57,5% so với 63,6%).
*(ii)* Dạng lỗi là **bỏ cuộc thừa**: 27,1% `none` trên bước có đáp án, tỉ lệ `none` phát ra
vượt tỉ lệ thật **13,5 điểm**; và thước `sel_acc` chỉ đếm cột HasAns nên **cộng 11,9 điểm cho
việc bỏ hẳn abstain trong khi độ đúng toàn bộ tụt 13,3 điểm**.
*(iii)* Thay bằng bộ thước kiểu **SQuAD 2.0** (toàn bộ · HasAns · NoAns) cộng risk–coverage,
và một ngưỡng τ chỉnh trên dev, đo **một lần** trên hold-out.

**Đóng góp là (ii) và (iii).** (i), Δ_sel, `exec` và hạt 202 là **bằng chứng**.
⚠️ Câu (ii) phải viết là *thước do chính chúng tôi đăng ký đã dẫn chúng tôi sai*, **không**
viết như phát hiện về thước của người khác.
Tiền lệ tổ chức bài: Kaushik & Lipton (EMNLP 2018) · Michel, Levy, Neubig (NeurIPS 2019) —
đóng góp phát biểu là **phát hiện về cơ chế**, số âm chỉ là bằng chứng.

### Ranh giới trung thực — phải khai

lát 1.400 đã chạm **hai lần** (G6, ép chọn) ⇒ mọi số trên đó là dev · G6 trượt và **giữ
nguyên trượt**, τ là luật đọc hậu kiểm chứ không thay cổng · τ chỉnh trên dev, hold-out 3.063
bước chạm **một lần**, in kết quả **kể cả khi τ = ∞** (không nên dời ngưỡng cũng là kết quả
hợp lệ) · train **không chừa val** · 42,5% ép chọn, cỡ khối, vị trí đều là **hậu kiểm một hạt
giống** · Δ_sel một hạt giống, dưới MDE · kế hoạch sáu lượt bị thay ở đâu, ngày nào, commit
nào · `sel_acc` là thước **do chính dự án đăng ký**.

### ⛔ Câu không được viết

*"điểm nghẽn ở định vị thị giác"* (tỉ số 34:1 bác thẳng) · *"focal loss gây hại cho sinh văn
bản"* (không có nguồn bình duyệt) · *"đầu tiên"* cho khối ứng viên ở miền di động · so số với
Chi et al. hay Pezeshkpour (họ đo trên mô hình prompting, ta đã fine-tune) · *"mô hình học
prior 54,8%"* (bằng chứng ngược: 80,2% vs 27,1%) · *"τ cải thiện hệ thống"* trước khi có số
hold-out · trong abstract 9/9 **không hứa số chưa đo**.
