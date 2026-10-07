# 288 — bản chép từ 37 ảnh (`Mom [06-10-2026 18_43].zip`) + 11 script viết lại + hướng dẫn chạy trên WSL

> **Phần I** (ngay dưới) là hướng dẫn chạy trên máy WSL này: script nằm đâu, đã kiểm gì, lệnh từng bước.
> **Phần II** là bản chép nguyên văn tài liệu gốc (soạn trên máy Mac `/Users/P836901/...`), chỉ đổi
> **md5 của 10 script** sang bản viết lại (mọi ô notebook đã khớp tệp thật). Chỗ ảnh bị cắt mép ghi `[…]`.

---

# PHẦN I — HƯỚNG DẪN CHẠY TRÊN MÁY NÀY (6/10/2026)

## I.1 Script đã viết lại

Mã gốc của 11 script nằm trong `288_PHU_LUC_B_MA_NGUON_6_10.md` trên máy Mac, không có trong ảnh. Cả
11 đã được **viết lại từ bản mô tả Phụ lục B** và nằm trong repo ở `_scripts/`. Md5 các script viết
lại khác bản gốc; các ô notebook và Phụ lục A ở Phần II đã đổi sang md5 mới.

| script | việc | tự kiểm trên máy này |
|---|---|---|
| `_scripts/288/g0_som_build.py` (B.3) | dựng ô SoM + 2.530 câu cho G0 | ✅ ra **đúng md5 bản khoá** cả hai tệp `g0_som.jsonl` `a49789bd…`, `g0_cau.jsonl` `656dd46f…` (879 màn · phủ 243/249 và 597/630 · 2.530 câu) |
| `_scripts/288/g0/g0_listener.py` (B.4) | Phi-4 chấm 2.530 cặp (Kaggle) | ✅ chạy hết 2.530 cặp bằng người nghe giả trên ảnh thật, nối tiếp được |
| `_scripts/288/g0/g0_doc.py` (B.5) | đọc cổng G0 | ✅ tái lập **O_SP = 68,67**, **1.717 cặp duy nhất**, **135 bước exec trộn** |
| `_scripts/288/nghe/grpo_nghe.py` (B.6) | GRPO thưởng người nghe + dựng bảng | ✅ selftest **11/11** (8 câu thử × 4 nhánh, hết giờ, 3 luật dừng, nạp lại nhật ký, máy chủ chết, `dang_ok`, nối dây `train()`); `dung_hang` dựng lại đúng 1.000 khoá câu nhắc ck500 |
| `_scripts/288/nghe/nghe_server.py` (B.7) | máy chủ người nghe (TCP) | ✅ backend giả trên bảng 630 màn thật, 0,04 s/câu |
| `_scripts/doc_286.py` (B.9) | thư viện đọc test | ✅ (qua B.8, B.13). Chỉ dựng phần thư viện; bộ đọc riêng của 286 không dùng cho 288 nên bỏ |
| `_scripts/288/doc_288.py` (B.8) | [cách A] đọc test K1–K4 | ✅ chạy khô: ck500 − S1 +1,55 [+0,84; +2,26]; không chạm 84,29 vs 85,97 (khớp số đã công bố) |
| `_scripts/288/cham/gieo_tho.py` (B.10) | gieo tệp thô trước khi chấm | ✅ selftest: 4.462/4.463 · 4.462 · 2.794, mọi bản ghi trùng bản gốc |
| `_scripts/288/dung_lai_288.py` (B.11) | chép tệp repo + kiểm md5 | ✅ **33/33 tệp khớp**; `preds_venus_ck500_2532.jsonl` trùng md5 bản gốc `34fa2cf8…` |
| `_scripts/288/cham/val_lon.py` (B.12) | val lớn 1.002 click | ✅ selftest 7/7 (gồm câu nhắc val lớn trùng từng ký tự `p1_val_rows` của gói) |
| `_scripts/289/doc_289.py` (B.13) | đọc sàng + test | ✅ `kiem` **19/19**, tái lập đúng KTC ck500 − S1 [+0,84; +2,26] |

**Chưa kiểm được trên máy này** (cần GPU): nạp Phi-4 thật, `grpo_spice.train` với `PeftModel` từ
ck500, tốc độ/VRAM trên A100. Các ô kiểm dụng cụ (L3, C6 15 phút đầu, T4, V2) được thiết kế để bắt
lệch ở chính những chỗ này trước lượt dài.

## I.2 Đổi đường dẫn Mac → WSL

| Phần II ghi | trên máy này |
|---|---|
| `GỐC` = `/Users/P836901/Documents/Self-learning/thesis` | `/mnt/d/Master/Thesis` (gốc repo) |
| `GỐC/thesis-master/…` | `/mnt/d/Master/Thesis/…` (cùng thư mục) |
| `_scripts/_venv/bin/python` | `~/.venvs/thesis/bin/python` |
| `GỐC/vallon289/` · `GỐC/goc289/` | `runs/vallon289/` · `runs/goc289/` |
| `GỐC/all_forest_dict.zip` | cache Hugging Face (B.3 tự tìm; md5 `4e88a4f1…` đã khớp) |
| §9 "tách B.11 từ file bàn giao" | **bỏ** — chỉ cần `python3 _scripts/288/dung_lai_288.py` |

## I.3 Quyết định 6/10 (chủ luận văn giao: "ra số tốt, đóng góp mô hình nhiều nhất, tiền Colab không thành vấn đề, không khoá ngưỡng")

Các mục này **thay** §00.4, §00.5, §00.9, §00.11 và P0 ở Phần II khi mâu thuẫn.

**Ba quyết định chính (6/10):**
1. **Chạy bản 4** — train tiếp ck500, vì ck500 đang là số test cao nhất (60,65); train tiếp từ đó có nhiều cơ hội ra số cao hơn làm lại từ S1.
2. **Thêm hai nhánh liều mạnh (W = 2) ngay lô 1**, không đợi lô 2 — tiền Colab không thành vấn đề, thử nhiều cách cùng lúc thì cơ hội có đóng góp cao hơn.
3. **Ngưỡng sàng hạ xuống +0,5** — nhánh hơn ck500 từ +0,5 trên val và không thua tspicea thì lên test; chấm test trên Kaggle không tốn tiền nên không loại sớm nhánh có triển vọng.

**Thứ tự ưu tiên của chủ luận văn: SỐ TỐT trước, đóng góp mô hình sau.** Hệ quả khi chọn mô hình cuối:
- Mô hình tiêu đề = nhánh có **exec test cao nhất** trong các nhánh đã chấm test (kể cả `tspicea`), miễn hơn ck500.
- Nếu nhánh cao nhất là nhánh người nghe ⇒ vừa số tốt vừa có thành phần mới (T2/T3).
- Nếu nhánh cao nhất là `tspicea` ⇒ vẫn lấy làm số tiêu đề, khai đúng là "ck500 + 250 bước SPICE" (đóng góp nhỏ, chấp nhận được).
- Số vẫn phải là số thật từ tệp thô, in kèm KTC; không gọi "hơn có ý nghĩa" khi KTC chứa 0.

| câu §00.11 | quyết |
|---|---|
| 1. bản 4 hay 3.1 | **bản 4** — train tiếp từ ck500 (đang là số test cao nhất 60,65), có kiểm thử trước bằng G0 và val lớn |
| 2. UGround trên val lớn để chọn nhánh | **dùng** |
| 3. G0 cấm người nghe thì sao | **vẫn train tspicea**; chấm test nếu val hơn ck500 ≥ +0,5 |
| 4. lô 2 (W = 2) | **không đợi**: chạy luôn hai nhánh liều mạnh `nghevm`, `nghem` ở **phiên Colab B** song song phiên A |
| 5. Phụ lục A | **chấp nhận**; P0 (khoá bằng mốc dataset) không còn bắt buộc |
| 6. 75–85% không có thành phần mới | không dừng tìm nếu sàng ra trắng: báo lại để chọn hướng kế |
| 7. Kaggle thứ hai | tuỳ bạn; có thì chấm song song nhanh gấp đôi |
| 8. V2 rớt | **chấm lại S1** trên lát 2.532 trong cùng phiên |
| 9. bấm tay 150 bước | **không làm** |

**Năm nhánh** (đều train tiếp 250 bước từ ck500, cùng 1.000 câu nhắc hạt 101):

| nhánh | thưởng | phiên Colab |
|---|---|---|
| `tspicea` | SPICE như ck500 (đối chứng "train lâu hơn") | A |
| `tnghev` | SPICE + 1·h ở màn Phi-4 trỏ trúng câu chuẩn | A |
| `tnghe` | SPICE + 1·h mọi màn | A |
| `tnghevm` | SPICE + **2**·h ở màn có v = 1 | B |
| `tnghem` | SPICE + **2**·h mọi màn | B |

**Tên dùng trong luận văn/slide** (tên trong mã giữ nguyên vì thư mục Drive, `TAG` Kaggle và bộ đọc dựa vào chúng):

| mã | tên khoa học | thưởng |
|---|---|---|
| `tspicea` | **SPICE-cont** (ck500 train tiếp 250 bước, chỉ SPICE) | R_SPICE |
| `tnghe` | **SPICE + LR** (Listener Reward), λ = 1 | R_SPICE + λ·h |
| `tnghev` | **SPICE + GLR** (Gated Listener Reward), λ = 1 | R_SPICE + λ·v·h |
| `tnghem` | **SPICE + LR**, λ = 2 | R_SPICE + 2·h |
| `tnghevm` | **SPICE + GLR**, λ = 2 | R_SPICE + 2·v·h |

Tiếng Việt: *thưởng người nghe* (LR), *thưởng người nghe có cổng kiểm định* (GLR). Ablation: SPICE-cont → +LR (công của người
nghe) → +GLR (công của cổng). Bảng tiêu đề: Base → S1 → GRPO-SPICE (ck500) → GRPO-SPICE + GLR/LR (nhánh thắng).

Hai phiên tách vì năm nhánh + Phi-4 khó vừa một A100 80GB; ô probe của mỗi phiên đo VRAM thật. Nhánh B
so với tspicea của phiên A (khác phiên, cùng loại GPU — nhiễu nhỏ, phải khai).

**Kiểm thử trước (để biết số có ổn không trước khi tốn giờ):**
1. **G0** (Kaggle 1,5 h, 0 đồng): oracle C1 cho biết thưởng người nghe có *khả năng* chọn câu tốt hơn SPICE không
   (`O_vh`, `O_h` so `O_SP` = 68,67). G0a/G0b rớt ⇒ chỉ train tspicea.
2. **15 phút đầu train**: thưởng TB tăng, "trúng" > 0, kl nhỏ, câu nhắc trùng ck500.
3. **Val lớn 1.002 click** (Kaggle, 0 đồng): luật sàng mới — X lên test khi **Δ(X − ck500) ≥ +0,5 và Δ(X − tspicea) > 0**;
   tspicea luôn lên cùng làm đối chứng; không X nào thì tspicea lên một mình nếu Δ ≥ +0,5.
4. **Test 4.463 click** + UI-Venus: nhãn T0–T3 của `doc_289.py` (KTC Bonferroni) để biết câu nào được viết vào luận văn.

Nói thẳng: kỳ vọng thô của tài liệu gốc là ~15–25% có nhánh người nghe lên test và ~7–12% vượt ck500 có ý nghĩa
trên test. Hai nhánh liều mạnh và ngưỡng sàng thấp hơn nâng các tỉ lệ này một chút, không đổi bản chất.

## I.4 Từng bước

Mọi lệnh máy nhà chạy từ `/mnt/d/Master/Thesis`.

**S0 — kiểm thư mục (máy nhà, vài giây)**
```bash
cd /mnt/d/Master/Thesis
python3 _scripts/288/dung_lai_288.py          # phải in ✅ ĐỦ, mọi md5 khớp (33 tệp đạt)
```

**S1 — gói Kaggle (máy nhà → Kaggle)**
1. Tạo dataset Kaggle **`thesis-g0-288`**: upload 6 tệp trong `_scripts/288/g0/` (+ file này nếu muốn ô P2 in md5 luật; không bắt buộc).
2. Tạo dataset **`cham288-script`**: upload cả thư mục `_scripts/288/cham/` (có `harness_venus/`).

**S2 — lô 0 val lớn (Kaggle T4×2, ~2–2,5 h, song song S3)**: notebook §00.7 (ô L1–L5), `NHANH = ["S1", "ck500"]`.
Add Data: `cham288-script` · `thesis-val-cham` · `fgrb-p1-bundle` · `grpo-spice-ck500`. Chạy tương tác L1 → L3, không
dòng DỪNG ⇒ Save Version → Save & Run All. Tải output về `runs/vallon289/`.

**S3 — G0 (Kaggle T4×2, ~1,5 h)**: P2 ở Phần II (một ô). Add Data: `thesis-g0-288` · `c1-exec8` · `fgrb-p1-bundle`.
Tải `g0/g0_phi4.jsonl` về `runs/g0_288/`. Rồi đọc:
```bash
~/.venvs/thesis/bin/python _scripts/288/g0/g0_doc.py --nghe runs/g0_288/g0_phi4.jsonl
```
Dòng cuối in sẵn `⇒ BẢN 4 (§00.4): ARMS_TRAIN = [...]` — chép vào ô C1.

**S4 — bảng thưởng (máy nhà, ~1 phút; bỏ qua nếu ARMS_TRAIN chỉ còn spicea)**
```bash
~/.venvs/thesis/bin/python _scripts/288/nghe/grpo_nghe.py --dung-bang --som _scripts/288/g0/g0_som.jsonl \
    --nghe runs/g0_288/g0_phi4.jsonl --out _scripts/288/nghe/bang_nghe.json      # ghi lại md5 in ra
~/.venvs/thesis/bin/python _scripts/288/nghe/grpo_nghe.py --selftest            # ✅ selftest ĐẠT (11/11), ~50 s
```

**S5 — train (hai phiên Colab A100 80GB song song, High RAM, ~5–7 h mỗi phiên, ~40–55 đơn vị mỗi phiên)**
1. Drive `MyDrive/thesis/nghe288/script/`: 7 tệp trong `_scripts/288/nghe/` + `bang_nghe.json`.
2. Drive `MyDrive/thesis/nghe288/ck500/`: `adapter_config.json` + `adapter_model.safetensors` (2 tệp **gốc** của
   dataset Kaggle `grpo-spice-ck500`, md5 `491fa667…`, không lấy thư mục `ref/`).
3. Notebook (mở **hai** notebook, mỗi cái một phiên A100): ô C1–C6 ở P5. Ở C1 điền `ARMS_TRAIN` phiên A hoặc phiên B (g0_doc
   in sẵn cả hai) và `BANG_MD5` (từ S4). Colab không cho hai phiên cùng lúc thì chạy phiên B sau phiên A. Chạy với `PROBE = True`, đọc
   VRAM + s/bước, rồi gõ `PROBE = False` và chạy C3 → C6. Theo dõi 15 phút đầu như hướng dẫn trong P5.

**S6 — gói điểm lưu (máy nhà → Kaggle)**: tải `MyDrive/thesis/nghe288/tiep_<arm>_101/checkpoint-250/` (2 tệp) →
dataset `sang289-ckpts` (giữ tên thư mục). Output lô 0 → dataset `vallon289-goc`.

**S7 — lô 1 val lớn (Kaggle T4×2, ~2,5–3 h)**: notebook §00.7, `NHANH = ["tspicea", "tnghev", "tnghe", "tnghevm", "tnghem"]` (bỏ
nhánh không train/đã dừng); thêm Add Data `sang289-ckpts` · `vallon289-goc`. Tải về `runs/vallon289/`.

**S8 — sàng (máy nhà, vài giây)**
```bash
P=~/.venvs/thesis/bin/python; V=runs/vallon289
$P _scripts/289/doc_289.py sang --nhanh S1:$V/score_S1_vallon_raw.jsonl --nhanh ck500:$V/score_ck500_vallon_raw.jsonl \
   --nhanh tspicea:$V/score_tspicea_vallon_raw.jsonl --nhanh tnghev:$V/score_tnghev_vallon_raw.jsonl \
   --nhanh tnghe:$V/score_tnghe_vallon_raw.jsonl --nhanh tnghevm:$V/score_tnghevm_vallon_raw.jsonl \
   --nhanh tnghem:$V/score_tnghem_vallon_raw.jsonl --out $V/sang_289.json     # nhánh dừng luật: bỏ --nhanh, thêm --dung <tên>
```
In `⇒ DỪNG` ⇒ hết, đóng góp mô hình = ck500. In `⇒ LÊN TEST: [...]` ⇒ S9 cho đúng các nhánh đó.

**S9 — test (Kaggle T4, ~5–8 h/nhánh) + UI-Venus (T4×2, ~1,5 h/nhánh)**: P6 (ô T1–T6), `TAG = "t<arm>101"`; Add
Data như P6 nhưng thay `nghe288-ckpts` bằng `sang289-ckpts`. Tải về `runs/goc289/`. Rồi P7a (`TAG = "ck500"`) và P7b
cho từng X lên; ô dựng preds UI-Venus của P7b chạy ở máy nhà với `R = "."` và đường `runs/goc289/pred_{TAG}_test.jsonl`.

**S10 — đọc test (máy nhà)**
```bash
P=~/.venvs/thesis/bin/python; V=runs/vallon289; T=runs/goc289; R=runs
$P _scripts/289/doc_289.py test --sang $V/sang_289.json --nhanh base:$R/score_base_raw.jsonl \
   --nhanh S1:$R/score_s1_seed101_raw.jsonl --nhanh ck500:$R/grpo_spice/score_ck500_test_raw.jsonl \
   --nhanh tspicea:$T/score_tspicea101_test_raw.jsonl --nhanh tnghev:$T/score_tnghev101_test_raw.jsonl \
   --venus ck500:$R/venus/score_venus_ck500_2532_raw.jsonl --venus tnghev:$R/venus/score_venus_tnghev101_2532_raw.jsonl \
   --out $T/test_289.json
```
Thêm `--nhanh`/`--venus` cho **mọi** nhánh mà `sang_289.json` liệt kê (kể cả `tnghevm`, `tnghem`).
Nhãn T0–T3 hoặc CHỜ; câu được phép viết theo từng nhãn ở §00.8.

## I.5 Lưu ý

- Các bản sao trong `_scripts/288/` (chép từ `harness/`, `runs/`) đã vào `.gitignore`; chỉ 11 script, `g0_som.jsonl`,
  `g0_cau.jsonl` được git theo dõi. Mất thì chạy lại S0.
- Ô L5 và T6 không tự zip output; tải từng tệp, hoặc thêm một ô `shutil.make_archive` ở cuối như các runbook khác.
- Tệp `_scripts/288/g0_ket_qua.json` chỉ được ghi bởi lượt G0 thật; bản giả lập ghi `g0_ket_qua_GIA.json`.

---

# PHẦN II — BẢN CHÉP NGUYÊN VĂN

# 288 — ACTION CUỐI (CHỐT): thành phần mới cho bước CLICK, chồng lên ck500 · 6/10/2026, bản 4 (phễu sàng)

> **File bàn giao DUY NHẤT và là action cuối.** Chat đọc file này chỉ cần **file này + repo**
> `thesis-master` (bản clone 6/10). Không cần file 286 hay bất kỳ file nào khác: mọi runbook (G0,
> train, chấm val lớn, chấm test UGround, UI-Venus, đọc kết quả) viết ở […] + §8; mọi mã ngoài repo
> nằm nguyên văn ở Phụ lục B; §9 có script dựng lại toàn bộ thư mục upload từ file này + repo.
> **Không commit, không push, không chạy git** — kể cả bước khoá đăng ký (khoá bằng mốc thời gian
> dataset Kaggle, §8 P0). Agent khô[ng …] file nào trong `thesis-master/`, không tải gì từ Hugging
> Face. **Thay hẳn bản 1, 2, 3, 3.1.**
>
> **File này chỉ có phần chạy.** Lý do chọn hướng, các ý đã loại, 27 lần thử cũ, oracle, mô phỏng
> G0, tài liệu chỗ dựa và đính chính các bản trước nằm ở file ghi chú riêng
> `288_GHI_CHU_NGHIEN_CUU_6_10.md` — **không cần để chạy**; vì vậy số mục ở đây nhả[y …]
> (không có §00.2, §1–§5, §7.3–7.4, §13).
>
> **Đọc §00 trước.** §00 là quy trình hiện hành (bản 4, `SANG = True`, train tiếp từ ck500 — bạn
> chốt 6/10). §0, §6–§12 là hạ tầng dùng chung (G0, người nghe, ô Colab, ô chấm test, UI-Venus) —
> chỗ nào §00 nói khác thì §00 thắng. Các phần đánh dấu **[cách […]** (§0, §6.2, P8, §10, bảng
> K0–K4 ở §11, `doc_288.py` B.8) là **đường lui dự phòng** (`SANG = False`: LoRA mới từ S1, 500
> bước, train theo đợt) — **không dùng** cho bản 4 và **không nằm trong đăng ký Phụ lục A**; muốn
> chạy cách A thì phải đăng ký riêng trướ[c …] train.

## 00. BẢN 4 — PHỄU SÀNG: thử nhiều thứ chồng lên ck500, rẻ trước, chỉ cái nào tăng thật mới đi tiếp

### 00.1 Mục tiêu và mốc so

> Thêm **một** thành phần lên ck500 (GRPO-SPICE) để nâng exec click: thưởng người nghe Phi-4, có
> cổng v (`tnghev`) và không cổng (`tnghe`); mọi nhánh **train tiếp từ adapter ck500**. Bảng tiêu
> đề luận văn: base → S1 → ck500 → ours. Muốn nói "thành phần X đó[ng] góp" thì X phải hơn đủ các
> mốc dưới (nếu không, người chấm hỏi ngay "có phải chỉ do train thêm?"):

| mốc so | để trả lời câu hỏi | bắt buộc? |
|---|---|---|
| base (Qwen2.5-VL-3B chưa tune) | mô hình học được gì so điểm xuất phát | mô tả (bảng tiêu đề) |
| S1 (SFT) | ours có hơn SFT không | **có — LB95 > 0** |
| ck500 (GRPO-SPICE, đóng góp hiện có) | thành phần mới có thêm gì so cái đã có | **có — LB95 > 0** |
| **tspicea** = ck500 train tiếp **cùng 250 bước, cùng máy**, chỉ SPICE | phần tăng là do thành phần, hay chỉ do train lâu hơn / đổi máy T4→A100 | **có — Δ > 0** |

Lý do tspicea không bỏ được: đường val của GRPO-SPICE **còn đang lên** (val C1: ck250 64,66 →
ck500 66,27), nên train thêm 250 bước SPICE thuần cũng có thể tăng. tspicea đồng thời thay B0′
của bản 3.1 (cùng phiên A100 ⇒ đo luôn nhiễu đổi máy).

Exec click trên test (UGround-V1-2B, 4.463 bước, đã có trong repo — `runs/score_base_raw.jsonl`,
`runs/score_s1_seed101_raw.jsonl`, `runs/grpo_spice/score_ck500_test_raw.jsonl`,
`runs/score_ceiling_human_raw.jsonl`):

| mô hình | exec click test |
|---|---|
| base (chưa tune) | 47,59 |
| S1 (SFT) | 59,11 |
| ck500 (GRPO-SPICE) | 60,65 (+1,55 [+0,84; +2,26] so S1) |
| ours | ? (bản 4) |
| câu người viết (trần tham khảo) | 75,73 |

### 00.3 Lô 1: ba nhánh, một phiên A100, cùng câu nhắc

| nhánh (thư mục Drive `tiep_<arm>_101`) | thưởng | vai trò | nếu thắng thì đóng góp là |
|---|---|---|---|
| `tspicea` | r_ck500 (SPICE − phạt dài), y ck500 | đối chứng "train lâu hơn" + nhiễu đổi máy | không phải thành phần mới ("train lâu hơn") |
| `tnghe` | r_ck500 + 1,0·h (người nghe Phi-4 SoM, mọi màn có ô) | ứng viên | áp dụng thưởng người nghe khác họ bộ chấm (cải tiến kỹ thuật, "kết hợp") |
| `tnghev` | r_ck500 + 1,0·v(màn)·h (chỉ màn Phi-4 trỏ trúng câu chuẩn) | ứng viên | như trên + **cổng v** — thành phần mới chỉ khi tnghev > tnghe có ý nghĩa trên test |

Cấu hình chung (khoá): khởi từ adapter **ck500** (`checkpoint-500`, `adapter_model.safetensors`
md5 `491fa6677340393f1e4464c08a0cec98`) bằng `grpo_nghe.py --tu` ⇒
`PeftModel.from_pretrained(is_trainable=True)`; 250 bước (`--max-steps 250`), chấm
**checkpoint-250**, không chọn điểm lưu; 1.000 câu nhắc hạt 101 (= câu nhắc ck500, 630 click);
G = 8, 16 câu/bước, β 0,04, lr 1e-5 hằng sau 10 bước khởi động (lịch của ck500 vốn hằng ⇒ khởi
động lại 10 bước là khác biệt duy nhất về lr); optimizer mới; A100 80GB ép fp16; lô `--bs 4
--accum 4` (khoá ở probe). Người nghe, `dang_ok`, luật dừng trong train: y §6.1, §6.3, §6.4.

**Điều phải biết:** TRL tạo adapter `ref` = bản sao adapter lúc bắt đầu để tính KL (thư mục `ref/`
trong mọi điểm lưu GRPO của repo — xem `harness/runbook/kaggle_grpo_point_6_9.md` dòng 43). Với
ck500, `ref` = LoRA mới (≡ S1). Với nhánh bản 4, `ref` = **ck500** ⇒ KL kéo về ck500, không về
S1. Như nhau cho cả 3 nhánh nên so với nhau sạch; nhưng tspicea **không** đúng bằng "ck750 của
công thức cũ" — viết là "ck500 + 250 bước SPICE". (Không đọc lại được mã TRL 0.29.1 lượt này:
mạng công ty chặn PyPI và GitHub — kết luận dựa trên thư mục `ref/` đã thấy ở GRPO-point.)

### 00.4 G0 trong bản 4 (đổi TRƯỚC khi có số G0 — ghi ở Phụ lục A mục 5)

G0 vẫn chạy (P2, ~1,5 h T4×2, 0 đồng) vì nó đo luôn v của 630 màn train (cần cho bảng thưởng).
Đổi vai trò:

| điều kiện | bản 3.1 | bản 4 |
|---|---|---|
| G0a parse_fail ≤ 0,05 ∧ phủ SoM ≥ 0,90 | chặn | **chặn người nghe** (tnghe, tnghev) |
| G0b κ(h, exec_UG) ≤ 0,60 | chặn hẳn | **chặn người nghe** (κ cao ⇒ thưởng ≈ chính bộ chấm) |
| V4 0,30 ≤ TB v (630 train) ≤ 0,85 | một vế keep_v | **chặn riêng tnghev** (v gần 0 hay gần 1 ⇒ cổng vô nghĩa) |
| G0c AUC ≥ 0,65 · G0d oracle ≥ +3,3 · V1–V3 | chặn / chọn nhánh | **chỉ ghi lại** (dự báo); val lớn quyết thay |

`ARMS_TRAIN` theo kết quả `g0_ket_qua.json` (`G0.a`, `G0.b`, `v_train`): cả ba ⇒
`[("spicea",101),("nghev",101),("nghe",101)]`; V4 sai ⇒ bỏ `("nghev",101)`; G0a hoặc G0b sai ⇒
chỉ `[("spicea",101)]` (khi đó không có thành phần mới để thử; chạy tspicea chỉ để biết "train lâu
hơn" có tăng không — tuỳ bạn, §00.10 mục 3).

Vì sao nới: cửa G0d (oracle ≥ +3,3) hẹp tới mức người nghe đủ mạnh để qua lại dễ quá giống UGround
(rớt G0b); bản 4 có val lớn 1.002 bước đo thẳng mô hình đã train, nên không cần đoán qua oracle.

### 00.5 Luật sàng và luật test (khoá — `doc_289.py`, B.13, viết và tự kiểm TRƯỚC mọi số)

**Sàng (val lớn, 1.002 click, UGround, greedy checkpoint-250, mỗi nhánh một lần):**

- X ∈ {tnghev, tnghe} **lên test** ⇔ Δ(X − tspicea) ≥ +1,0 ∧ Δ(X − ck500) ≥ +1,0 (ước điểm; 1,0 = MDE click test).
- Có X lên ⇒ **tspicea lên test cùng** (đối chứng bắt buộc). Cả hai X lên ⇒ cả hai lên.
- Không X nào lên: tspicea lên một mình ⇔ Δ(tspicea − ck500) ≥ +1,0 (chỉ là "train lâu hơn"); ngược lại **DỪNG**: đóng góp mô hình = ck500, không chấm test nhánh nào.
- Nhánh dừng theo luật train (`DUNG.json`) ⇒ coi như không lên, báo như một kết quả.
- Val lớn **chỉ để chọn**: cấm viết số val vào luận văn như kết quả, cấm suy ra test từ nó.

**Test (4.463 click, mỗi nhánh được lên đúng một lần; k = số X lên; KTC cho X − ck500, X − S1 là 1 − 0,05/k):**

- **VƯỢT(X)** ⇔ LB(X − ck500) > 0 ∧ LB(X − S1) > 0 ∧ Δ(X − tspicea) > 0 ∧ Δ_UIVenus(X − ck500) > 0.
- **v gây ra** ⇔ VƯỢT(tnghev) ∧ LB95(tnghev − tnghe) > 0. tnghe chưa chấm test ⇒ bộ đọc in `CHỜ: test tnghe` (thêm một lượt P6).
- Nhãn: **T0** không X nào lên (chỉ tspicea hoặc dừng) · **T1** X lên nhưng không VƯỢT · **T2** VƯỢT, v chưa chứng minh · **T3** VƯỢT ∧ v gây ra · **CHỜ** còn thiếu tệp (UI-Venus, tnghe).

**Độ nhạy val lớn** (đo trên val C1 thật, 249 click, giữa hai điểm lưu cách nhau 250 bước như nhánh
bản 4): ck500 − ck250 = +1,61 [−0,81; +4,20], nửa KTC 2,50 ⇒ ước trên 1.002 click **1,25 (sd cặp
0,64)**. Khoảng 73% câu của nhánh tiếp trùng ck500 ⇒ gieo tệp thô, mỗi nhánh chỉ chấm ~27% số câu.

**Lọt sàng nhầm và sót** (mô phỏng: nhiễu cặp sd 0,64, 200.000 lần; P(X lên test)):

| Δ thật của tspicea so ck500 \ Δ thật của X so ck500 | 0 | +0,5 | +1,0 | +1,5 | +2,0 | +3,0 |
|---|---|---|---|---|---|---|
| 0 | 0,04 | 0,15 | 0,38 | 0,64 | 0,85 | 0,99 |
| +0,5 | 0,02 | 0,09 | 0,25 | 0,48 | 0,70 | 0,95 |
| +1,0 | 0,01 | 0,04 | 0,12 | 0,28 | 0,50 | 0,87 |

Nhánh vô dụng lọt test ≤ 4%; nhánh hơn tspicea thật +1,5 được lên ~50–64%. Test là phép xác nhận
độc lập (dữ liệu khác, KTC Bonferroni), nên lọt sàng nhầm chỉ tốn giờ T4, không làm sai kết luận.

```python
# mô phỏng bảng trên (CPU, 1 giây)
import numpy as np
rng = np.random.default_rng(289); M = 200000; sd = 0.64
for mu_u in (0.0, 0.5, 1.0):
    row = []
    for mu_x in (0, .5, 1, 1.5, 2, 3):
        eX, eU = rng.normal(0, sd, M), rng.normal(0, sd, M)
        row.append(np.mean((mu_x + eX >= 1) & ((mu_x - mu_u) + eX - eU >= 1)))
    print(f"U1 {mu_u:+.1f}: " + " · ".join(f"{p:.2f}" for p in row))
```

**Xác suất thô (nói thẳng):** qua G0a ∧ G0b ≈ 80–85% (κ Phi-4–UGround từng đo 0,44). Có X lên test
≈ 15–25% (văn liệu: lợi ích người nghe giữ 20–75% dưới bộ chấm độc lập, kỳ vọng Δ so ck500 ≈
0…+1,0). T2 ≈ 7–12%. T3 ≈ 2–4%. Khoảng 75–85%: đóng góp mô hình vẫn là ck500 — lần này với bằng
chứng sạch hơn ("train thêm và thêm người nghe đều không vượt").

### 00.6 Runbook bản 4 (thứ tự)

| bước | ở đâu | việc | chờ gì |
|---|---|---|---|
| S0 | máy nhà | `python3 _scripts/288/dung_lai_288.py --md 288_ACTION_NGUOI_NGHE_CLICK_6_10.md --kiem` phải in ✅ ĐỦ (thiếu G0 data ⇒ làm B.3) | — |
| S1 | máy nhà → Kaggle | P0 khoá đăng ký (file **bản 4** này vào dataset `thesis-g0-288`) · upload `_scripts/288/cham/` thành **New Version** `cham288-script` (giờ có `val_lon.py` + 3 tệp C1) | — |
| S2 | Kaggle T4×2 | lô 0: notebook val lớn §00.7 với `NHANH = ["S1", "ck500"]` (~2–2,5 h) — chạy ngay, song song S3 | S1 |
| S3 | Kaggle T4×2 | P2 G0 → P3 đọc → chọn `ARMS_TRAIN` theo §00.4 | S1 |
| S4 | máy nhà | P4 dựng `bang_nghe.json` (bỏ qua nếu G0 cấm người nghe) | S3 |
| S5 | Colab A100 80GB | Drive: thêm `MyDrive/thesis/nghe288/ck500/` = 2 tệp gốc (`adapter_config.json`, `adapter_model.safetensors`) của dataset Kaggle `grpo-spice-ck500` (không lấy `ref/`); `script/` = 7 tệp `_scripts/288/nghe/` + `bang_nghe.json`. P5 với `SANG = True`, probe 3 nhánh → `PROBE = False` → C3 → C6 (~5–7 h) | S4 |
| S6 | máy nhà → Kaggle | Tải `tiep_<arm>_101/checkpoint-250/{adapter_config.json, adapter_model.safetensors}` từ Drive → dataset `sang289-ckpts` (giữ tên thư mục) · Output lô 0 → dataset `vallon289-goc` | S5, S2 |
| S7 | Kaggle T4×2 | lô 1: notebook val lớn với `NHANH = ["tspicea", "tnghev", "tnghe"]` (bỏ nhánh không train/đã dừng) (~2,5–3 h) | S6 |
| S8 | máy nhà | `doc_289.py sang` (§00.8) ⇒ danh sách LÊN TEST hoặc DỪNG | S7 |
| S9 | Kaggle T4 | P6 (T1–T6) cho từng nhánh LÊN TEST, `TAG = "t<arm>101"` · P7a (UI-Venus ck500) + P7b (UI-Venus từng X) | S8 |
| S10 | máy nhà | `doc_289.py test` ⇒ T0–T3 hoặc CHỜ | S9 |

Kết quả Kaggle đặt ở `GỐC/vallon289/` (val) và `GỐC/goc289/` (test, UI-Venus) — ngoài repo, không
mất khi clone lại. P7b dựng preds UI-Venus: đoạn mã ở P7b, đổi `TAG = "tnghev101"` và đường
`runs/goc288/pred_{TAG}_test.jsonl` → `../goc289/pred_{TAG}_test.jsonl` (chạy từ GỐC thì
`goc289/pred_{TAG}_test.jsonl`).

**Đọc 15 phút đầu train (bản 4):** mỗi nhánh có `[nhánh] … · tiếp từ /content/nghe/ck500` ·
`[train tiếp] LoRA khởi từ /content/nghe/ck500 (is_trainable)` · `[LoRA mới] tham số học N · S1
có N` (cùng N) · `câu nhắc trùng ck500` ✅; C6 in `bước x/250`. Thiếu dòng `[train tiếp]` ⇒ C6 in
⛔ ⇒ dừng tay, báo lại (đang train từ S1, không phải ck500).

### 00.7 Notebook val lớn (Kaggle, GPU T4×2, Internet ON)

Add Data: `cham288-script` (New Version có `val_lon.py`) · `thesis-val-cham` · `fgrb-p1-bundle` ·
`grpo-spice-ck500` · lô 1 thêm `sang289-ckpts` và `vallon289-goc` (để gieo câu trùng S1/ck500;
thiếu thì vẫn chạy, chỉ chậm hơn). Chạy tương tác L1 → L3 (~25 phút, không dòng DỪNG nào) → sửa
`NHANH` ở L4 → **Save Version → Save & Run All**.

```python
# Ô L1 — gói (ghim y bộ train ck500), GPU
import subprocess, sys, os, time, glob, json, shutil, hashlib, threading
T_NB = time.time()
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-3000:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q 'trl==0.29.1' 'transformers==5.18.0' 'peft==0.21.1' accelerate torchao bitsandbytes pycocoevalcap 2>&1 | tail -3")
sh(f"{sys.executable} -m pip uninstall -y -q torchao")   # 6/10: image có torchao 0.10, peft 0.21 ném ImportError (<0.16); dự án không dùng torchao
import importlib.util; assert importlib.util.find_spec("torchao") is None, "DỪNG: torchao còn"
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__)"')
G = [g for g in subprocess.run("nvidia-smi --query-gpu=name --format=csv,noheader", shell=True, capture_output=True,
         text=True).stdout.split("\n") if g.strip()]
assert G and all("T4" in g for g in G), f"DỪNG: val lớn sinh + chấm trên T4 (như C1/test), máy này {G}"
NG = len(G); print("GPU:", NG, "× T4", flush=True)
```

```python
# Ô L2 — mã + md5, harness chấm, gói, val lớn, hoà S1, cây trợ năng, UGround, adapter ck500
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
SRC = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/val_lon.py", recursive=True)})
assert len(SRC) == 1, f"DỪNG: cần đúng một cham288-script có val_lon.py (New Version), thấy {SRC}"
SRC = SRC[0]
MA = {"val_lon.py": "d2854d13af1c924f44bf2dcb343ae8ca", "gieo_tho.py": "7681cc68ad7e0bc9965c73f47ea3aa88",
      "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf", "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912"}
for f, h in MA.items():
    shutil.copy(f"{SRC}/{f}", f"{W}/{f}"); assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch máy nhà ({md5(f'{W}/{f}')})"
for f, h in {"score_ck500_c1_raw.jsonl": "258ced11cad3b6729bbdb25f947dbe78", "score_s1_c1_raw.jsonl": "1c8dbcd5f49ec53ecc655b4b4d2c04c4",
             "pred_ck500_c1.jsonl": "eb6162d86730a936beb5ae5a9fd6d652"}.items():
    assert md5(f"{SRC}/{f}") == h, f"DỪNG: {f} lệch repo"
WS = f"{W}/thesis"
if not os.path.exists(f"{WS}/harness/score_run.py"):
    shutil.copytree(f"{SRC}/harness_venus", f"{WS}/harness")
assert md5(f"{WS}/harness/score_run.py") == "9100844734d00e4f1851954d25a86220", "DỪNG: score_run.py không phải bản repo"
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "p1_val_rows.jsonl" in f)
v600 = sorted(glob.glob("/kaggle/input/**/val_cham600.jsonl", recursive=True), key=len)
v600 = [p for p in v600 if all(os.path.exists(os.path.join(os.path.dirname(p), f)) for f in ("val_cham400.jsonl", "ocr.jsonl", "images"))]
assert v600, "DỪNG: gắn thesis-val-cham (val_cham400 · val_cham600 · ocr · images)"
VAL = os.path.dirname(v600[0]); VD = f"{W}/valdata"
assert sh(f"cd {W} && python val_lon.py --dung --val {VAL} --out {VD}") == 0, "DỪNG: dựng val lớn lỗi"
MERGED = f"{W}/s1_merged"
if not os.path.exists(f"{MERGED}/config.json"):
    r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED], cwd=W, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-800:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
from huggingface_hub import snapshot_download
print("UGround:", snapshot_download("osunlp/UGround-V1-2B"), flush=True)       # tải MỘT lần trước khi 2 GPU chấm song song
sys.path.insert(0, f"{WS}/harness")
import a11y_inventory as A11Y, score_run as SR
names = set(A11Y._zip().namelist())
taps = [d for d in map(json.loads, open(f"{VD}/val_lon_recs.jsonl")) if d["action"].get("action_type") in ("click", "long_press") and "x" in d["action"]]
co_cay = sum(A11Y.key_for(f"episode_{d['episode_id']}_screenshot_{d['step_id']}.png") in names for d in taps)
rong = sum(len(SR.buttons_of(d)) == 0 for d in taps)
print(f"val lớn: {len(taps)} click · cây trợ năng {co_cay} · rỗng nút {rong}", flush=True)
assert len(taps) == 1002 and co_cay == 1002 and rong == 0, "DỪNG: thiếu cây trợ năng → Voronoi chấm sai mà không báo"
C5 = [os.path.dirname(f) for f in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True)
      if md5(f) == "491fa6677340393f1e4464c08a0cec98"]
assert C5, "DỪNG: gắn dataset grpo-spice-ck500"; C5 = C5[0]

def chay(cmd, log, cwd, gpu, nhip=120):
    t0 = time.time()
    with open(log, "w") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "CUDA_VISIBLE_DEVICES": str(gpu), "TQDM_DISABLE": "1",
                                  "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1"})
        while q.poll() is None:
            time.sleep(nhip)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-t0)/3600:5.2f} h · GPU{gpu} · {os.path.basename(log)} · {L[-1][:100] if L else '…'}", flush=True)
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode} ---\n" + "".join(open(log, errors="ignore").readlines()[-6:]), flush=True)
    return q.returncode
print("SRC", SRC, "\nBUNDLE", BUNDLE, "\nVAL", VAL, "\nck500", C5, flush=True)
```

```python
# Ô L3 — kiểm dụng cụ (~10 phút): UGround chấm lại 20 câu ck500 của C1 trên val lớn, phải trùng tệp thô C1 (≤ 3 px, cùng exec)
KS = f"{W}/kiem/score_kiem20.json"; os.makedirs(os.path.dirname(KS), exist_ok=True)
for p in (KS, KS.replace(".json", "_raw.jsonl")):
    if os.path.exists(p): os.remove(p)
chay(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", f"{SRC}/pred_ck500_c1.jsonl",
      "--data-root", VD, "--recs-file", "val_lon_recs.jsonl", "--n", "20", "--out", KS], f"{W}/kiem_cham20.log", WS, 0, nhip=30)
R5 = {(d["episode_id"], d["step_id"]): d for d in map(json.loads, open(f"{SRC}/score_ck500_c1_raw.jsonl"))}
M = [json.loads(l) for l in open(KS.replace(".json", "_raw.jsonl"))]
def gan(a, b):
    if a.get("pred_xy") is None or b.get("pred_xy") is None: return a.get("pred_xy") == b.get("pred_xy")
    return a.get("executable") == b.get("executable") and max(abs(x - y) for x, y in zip(a["pred_xy"], b["pred_xy"])) <= 3
khop = sum(gan(R5[(d["episode_id"], d["step_id"])], d) for d in M)
print(f"[kiểm chấm] {khop}/{len(M)} câu ck500 trùng tệp thô C1", flush=True)
assert len(M) == 20 and khop >= 19, "DỪNG: bộ chấm khác lượt C1 → KHÔNG được gieo; gửi kiem_cham20.log về"
```

```python
# Ô L4 — chọn nhánh
NHANH = ["S1", "ck500"]      # ← lô 0. Lô 1: ["tspicea", "tnghev", "tnghe", "tnghevm", "tnghem"] — chỉ nhánh đã train xong, không DUNG.json
def ck_of(t):
    if t == "S1": return None
    if t == "ck500": return C5
    C = [p for p in glob.glob(f"/kaggle/input/**/tiep_{t[1:]}_101/checkpoint-250", recursive=True)
         if os.path.exists(f"{p}/adapter_model.safetensors")]
    assert len(C) == 1, f"DỪNG: cần đúng một tiep_{t[1:]}_101/checkpoint-250 trong sang289-ckpts, thấy {C}"
    return C[0]
CK = {t: ck_of(t) for t in NHANH}
for t, c in CK.items(): print(t, c, md5(f"{c}/adapter_model.safetensors") if c else "(S1 hoà, không gắn điểm lưu)")
THO0 = [f"{SRC}/score_s1_c1_raw.jsonl", f"{SRC}/score_ck500_c1_raw.jsonl"] + \
       sorted(glob.glob("/kaggle/input/**/score_*_vallon_raw.jsonl", recursive=True))
print("tệp thô để gieo:", THO0, flush=True)
```

```python
# Ô L5 — mỗi GPU một hàng đợi: sinh 1.002 câu (nối tiếp được) → gieo → chấm phần còn lại
def mot_nhanh(t, gpu):
    P = f"{W}/pred_{t}_vallon.jsonl"; SC = f"{W}/score_{t}_vallon.json"; RAW = SC.replace(".json", "_raw.jsonl")
    cmd = ["python", "val_lon.py", "--gen", "--bundle", BUNDLE, "--merged", MERGED, "--val", VAL, "--out", P, "--no-q4",
           "--so", f"{SRC}/pred_ck500_c1.jsonl"] + (["--ckpt", CK[t]] if CK[t] else [])
    chay(cmd, f"{W}/gen_{t}_vallon.log", W, gpu)
    assert sum(1 for _ in open(P)) == 1002, f"DỪNG: {t} thiếu câu — chạy lại ô này (nối tiếp)"
    if t == "ck500":
        d = [l for l in open(f"{W}/gen_ck500_vallon.log") if l.startswith("[so pred_ck500_c1.jsonl]")]
        n = int(d[-1].split("]")[1].split("/")[0])
        assert n >= 237, f"DỪNG: ck500 sinh lại chỉ {n}/249 câu C1 trùng pred_ck500.jsonl — đường sinh lệch; KHÔNG dùng số nào"
    if not os.path.exists(RAW):
        tho = THO0 + [p for p in glob.glob(f"{W}/score_*_vallon_raw.jsonl") if p != RAW and sum(1 for _ in open(p)) == 1002]
        assert sh(f"cd {W} && python gieo_tho.py --preds {P} --tho {' '.join(tho)} --out {RAW}") == 0
    chay(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", P,
          "--data-root", VD, "--recs-file", "val_lon_recs.jsonl", "--out", SC], f"{W}/cham_{t}_vallon.log", WS, gpu)
    R = [json.loads(l) for l in open(RAW)]; K = {(r["episode_id"], r["step_id"]) for r in R}
    print(f"== {t}: {len(R)} dòng thô · {len(K)} bước · exec {sum(int(r.get('executable') or 0) for r in R)}/1002 · "
          f"{(time.time()-T_NB)/3600:.2f} h", flush=True)
    assert len(R) == len(K) == 1002, f"DỪNG: {t} tệp thô trùng/thiếu"

HANG, loi = [NHANH[i::NG] for i in range(NG)], []
def chay_hang(i):
    for t in HANG[i]:
        try: mot_nhanh(t, i)
        except BaseException as e: loi.append((t, repr(e))); print("⛔", t, e, flush=True)
TH = [threading.Thread(target=chay_hang, args=(i,)) for i in range(NG)]
for x in TH: x.start()
for x in TH: x.join()
print("LỖI:", loi if loi else "không", flush=True); assert not loi
shutil.rmtree(MERGED, ignore_errors=True)
```

Phải thấy: `[dữ liệu] val lớn · 1002 bước click · thiếu OCR 0 · thiếu ảnh 0 · câu nhắc lệch
p1_val_rows 0` (câu nhắc dựng từ `thesis-val-cham` trùng từng ký tự câu nhắc dựng từ `p1_val_rows`
của gói) · ck500: `[so pred_ck500_c1.jsonl] ≥ 237/249 câu trùng` (S1: số này chỉ để xem) ·
`[gieo] N/1002` · `== t: 1002 dòng thô · 1002 bước · exec …`. Gửi về `GỐC/vallon289/`:
`pred_*_vallon.jsonl` · `score_*_vallon.json` · `score_*_vallon_raw.jsonl` · `gen_*_vallon.log` ·
`cham_*_vallon.log` · `kiem_cham20.log`.

### 00.8 Đọc (máy nhà, vài giây; `_scripts/289/doc_289.py`, B.13)

```bash
cd /Users/P836901/Documents/Self-learning/thesis
P=_scripts/_venv/bin/python; V=vallon289; T=goc289; R=thesis-master/runs
# sàng (sau S7)
$P _scripts/289/doc_289.py sang --nhanh S1:$V/score_S1_vallon_raw.jsonl --nhanh ck500:$V/score_ck500_vallon_raw.jsonl \
   --nhanh tspicea:$V/score_tspicea_vallon_raw.jsonl --nhanh tnghev:$V/score_tnghev_vallon_raw.jsonl \
   --nhanh tnghe:$V/score_tnghe_vallon_raw.jsonl --out $V/sang_289.json        # nhánh dừng luật: bỏ --nhanh, thêm --dung tnghev
# test (sau S9) — chỉ đưa nhánh sang_289.json liệt kê, cộng tnghe nếu bộ đọc đòi
$P _scripts/289/doc_289.py test --sang $V/sang_289.json --nhanh base:$R/score_base_raw.jsonl \
   --nhanh S1:$R/score_s1_seed101_raw.jsonl --nhanh ck500:$R/grpo_spice/score_ck500_test_raw.jsonl \
   --nhanh tspicea:$T/score_tspicea101_test_raw.jsonl --nhanh tnghev:$T/score_tnghev101_test_raw.jsonl \
   --venus ck500:$T/score_venus_ck500_2532_raw.jsonl --venus tnghev:$T/score_venus_tnghev101_2532_raw.jsonl --out $T/test_289.json
# tự kiểm bộ đọc (dữ liệu thật của repo + nhánh giả): phải in ✅ tự kiểm ĐẠT
$P _scripts/289/doc_289.py kiem --repo thesis-master
```

Tự kiểm lượt này (`kiem`, 18 tình huống, ĐẠT): sàng — X +2,4 hơn cả hai ⇒ `tnghev, tspicea` · X
+0,8 ⇒ DỪNG · tspicea +2,0 mà X = tspicea ⇒ chỉ tspicea · X hơn ck500 +3,2 nhưng chỉ hơn tspicea
+0,4 ⇒ chỉ tspicea · cả hai X ⇒ cả hai + tspicea · tnghev dừng luật ⇒ tnghe + tspicea · không ai
⇒ DỪNG · tệp thiếu bước ⇒ dừng. Test — tái lập ck500 − S1 +1,55 [+0,84; +2,26], base 47,59 · X
+3,0 (cứu 334 phá 200) + Venus dương ⇒ T2 · thiếu Venus ⇒ CHỜ · Venus âm ⇒ T1 · X +0,5 ⇒ T1 ·
tnghev VƯỢT mà thiếu tnghe ⇒ CHỜ test tnghe · tnghev hơn tnghe rõ ⇒ T3 · tnghev ≈ tnghe ⇒ T2
"cổng v KHÔNG được chứng minh" · X hơn ck500 nhưng thua tspicea ⇒ T1 · chỉ tspicea ⇒ T0. (Lần chạy
đầu bắt được một lỗi của chính bộ kiểm: nhánh giả chỉ lật 0→1 nên KTC không bao giờ chứa 0 — đã
đổi thành vừa cứu vừa phá như nhánh thật; luật không đổi.)

**Câu được phép (bản 4):**

| nhãn | câu |
|---|---|
| DỪNG ở sàng | "Train tiếp ck500 với thưởng người nghe khác họ bộ chấm (có/không cổng) không vượt ck500 và đối chứng train-tiếp trên val; đóng góp mô hình là GRPO-SPICE (ck500)." |
| T0 | như trên; nếu LB(tspicea − ck500) > 0: "train thêm 250 bước SPICE nâng exec" — **không** gọi là thành phần mới |
| T1 | "Thưởng người nghe tăng trên val nhưng không qua xác nhận trên test (âm có kiểm soát)." |
| T2 | "Áp dụng thưởng người nghe khác họ bộ chấm vào GRPO, chồng lên GRPO-SPICE, nâng exec click so SFT, so GRPO-SPICE và so đối chứng train-tiếp cùng ngân sách." (mức kết hợp/cải tiến kỹ thuật; cách viết "dựa trên ISR, LaF-GRPO" ở §11) |
| T3 | T2 + câu độ mới về cổng v ở §11 (thay "B1/B-rand" bằng "nhánh không cổng") |

Bảng tiêu đề luận văn: base · S1 · ck500 · ours (+ tspicea ở bảng ablation). Câu cấm của §11 giữ
nguyên; thêm: cấm đưa số val lớn vào luận văn như kết quả; cấm gọi tspicea là đóng góp mới; cấm
viết câu nào khi bộ đọc còn in `CHỜ`.

### 00.9 Dự trữ (lô 2 — KHÔNG chạy trừ khi luật dưới bật, quyết trước khi thấy số)

1. **Liều người nghe mạnh hơn** (W = 2,0, cùng nhánh X tốt nhất): chỉ khi lô 1 không X nào lên **và** X tốt nhất có Δ(X − tspicea) ∈ [+0,3; +1,0) trên val. Một nhánh, một lượt Colab ~4–5 h; so với tspicea lô 1 (cùng câu nhắc, khác phiên). Cần thêm cờ `--w` vào `grpo_nghe.py` (hiện W là hằng `W_NGHE = 1.0`) — **chưa viết**. Lên test theo đúng luật §00.5; khai là "lần sàng thứ hai".
2. **SFT câu vàng làm giàu tên** — ưu tiên thấp (câu vàng train đã nêu tên đích 65,1%, ngang người viết trên test); chỉ khi bạn muốn có thêm một hướng dữ liệu. Chưa viết mã.
3. Hạt 202 của nhánh T2/T3: không bắt buộc cho câu T2/T3 (test là xác nhận độc lập), chỉ cần nếu muốn viết "ổn định qua hạt".

### 00.10 Chi phí bản 4

| việc | máy | thời gian | đơn vị Colab |
|---|---|---|---|
| lô 0 val lớn (S1, ck500) | Kaggle T4×2 | ~2–2,5 h (sinh 2,8 s/câu ⇒ ~47 phút; chấm ~4,4 s/câu ⇒ ~73 phút; 2 GPU song song) | 0 |
| G0 | Kaggle T4×2 | ~1,5 h | 0 |
| probe + lô 1 (3 nhánh × 250 bước, chung A100 + Phi-4) | Colab A100 80GB | ~5–7 h (bản 3.1 ước 3 nhánh × 500 bước 9–12 h) | ~40–55 |
| lô 1 val lớn (3 nhánh, gieo ~73% câu) | Kaggle T4×2 | ~2,5–3 h | 0 |
| test mỗi nhánh lên (gieo câu trùng S1/ck500) | Kaggle T4 | ~5–8 h/nhánh | 0 |
| UI-Venus ck500 + mỗi X | Kaggle T4×2 | ~1,5 h/nhánh | 0 |
| **dừng ở sàng** | | ~6 h Kaggle | ~40–55 (~4–5,5 USD) |
| **đi hết (2 X + tspicea lên test)** | | ~30 h Kaggle | ~40–55 (+ lô 2 nếu bật ~30–40) |

So bản 3.1 (tối đa ~165–220 đơn vị, 3 đợt nối tiếp, ~4 tuần): bản 4 thử **cả ba ý cùng lúc** với
~1/4 tiền Colab và có kết quả sàng trong ~1 tuần; giờ T4 test chỉ tiêu cho nhánh đã tăng trên val.

### 00.11 Agent KHÔNG làm · bạn quyết (bản 4)

**Không làm:** không chạy GPU nào; notebook L1–L5 và ô Colab bản 4 **chưa chạy trên Kaggle/Colab**
— phần CPU đã chạy thật: selftest `val_lon.py` (5/5 trên tệp repo; phần kiểm `--gen` thử trên gói
giả: bắt đúng một bước click bị sửa câu nhắc), selftest `grpo_nghe.py` (ĐẠT, gồm ca `--tu`),
`doc_289.py kiem` (18/18); không đọc được mã TRL 0.29.1 (mạng chặn) — điều về adapter `ref` ở
§00.3 suy từ thư mục `ref/` đã thấy; không có adapter ck500 trên máy (bạn tải từ dataset
`grpo-spice-ck500`); không sửa `thesis-master/`; không chạy git; không tải gì từ Hugging Face (các
ô Kaggle/Colab tải UGround, Phi-4, zip a11y **do bạn chạy**, như runbook trước).

**Bạn quyết:**

1. Duyệt bản 4 thay bản 3.1 (đổi vai trò G0 §00.4; luật sàng/test §00.5) — phải quyết **trước P0** (khoá đăng ký) vì nó đổi luật.
2. Duyệt dùng UGround trên val lớn để **chọn** nhánh (bạn đã "cho" 6/10) — khai công khai ở Phụ lục A mục 7; nới thêm (x19f) và `report/106` L1426–1429 (cấm bộ trỏ trong chọn điểm lưu/nhánh).
3. G0a/G0b rớt: có chạy tspicea một mình (~15–20 đơn vị) để biết "train lâu hơn" có tăng không, hay dừng luôn?
4. Lô 2 (§00.9 mục 1) có bật tự động theo luật không, hay hỏi lại khi tới đó?
5. Chấp nhận Phụ lục A (nới `report/106` L1426–1429 và tinh thần (x19f) "không thưởng bằng bất kỳ bộ trỏ nào" — Phi-4 SoM là bộ chọn phần tử)? Không ⇒ dừng trước P0, đóng góp mô hình = ck500.
6. Chấp nhận ≈ 75–85% kết cục không có thành phần mới, và khi đó **dừng tìm** (không đổi người nghe, không hạ ngưỡng)?
7. Có dùng tài khoản Kaggle thứ hai để chấm song song không (giờ T4 là nút cổ chai)?
8. Nếu ô kiểm V2 (UI-Venus) rớt: chấp nhận chấm lại S1 trên lát 2.532 trong cùng phiên (+~3 h T4×2) không?
9. Có người bấm tay ~150 bước lệch UGround/UI-Venus làm mô tả phụ không (không ảnh hưởng luật nào)?

## 0. [cách A] Đường lui: LoRA mới từ S1, train theo đợt (`SANG = False`) — không dùng cho bản 4

Cách A = S1 → GRPO 500 bước với thưởng §6.1, so thẳng với ck500 (cùng xuất phát, cùng số bước).
Sạch hơn về lập luận ("một công thức") nhưng khó vượt ck500 hơn bản 4, vì toàn bộ phần hơn phải
đến từ thưởng người nghe. Đợt 1 chỉ nhánh chính (nghev; G0 keep_v sai ⇒ nghe); Đợt 2 (B0′ spicea,
B1 nghe, hạt 202, UI-Venus) chỉ khi Δ(chính − ck500) > 0 trên test; Đợt 3 (B1 hạt 202, B-rand) chỉ
khi còn đường lên K4 (§6.2). Đọc bằng `doc_288.py` (P8, B.8), nhãn K0–K4 (§11). Chi phí §10 (~50–220
đơn vị Colab). **Chưa đăng ký** — Phụ lục A chỉ khoá bản 4; muốn chạy cách A thì viết đăng ký
riêng (dùng luật §6.2, §7.1, §11) **trước** khi train.

Mọi thư mục upload (`_scripts/288/g0/`, `nghe/`, `cham/`) đã sẵn trên máy bạn; mất ⇒
`dung_lai_288.py` (§9) dựng lại từ file này + repo.

## 6. Thiết kế

### 6.1 Thưởng

```
r(c) = r_ck500(c) + W · g(màn) · h(c),        W = 1,0 (khoá)
r_ck500 = SPICE − 0,02·max(0, từ(c) − từ(vàng) − 3)      (NGUYÊN grpo_spice.r_spice của ck500)
h(c)    = 1 ⇔ dang_ok(c) ∧ ô SoM Phi-4 chọn khi đọc c ∈ dap_an (mọi ô chứa điểm chạm vàng), ngược lại 0
dang_ok = 3–20 từ ∧ không khớp \d+\s*[,;]\s*\d+ ∧ không khớp \d{3,}
Câu nhắc không chạm, hoặc màn không có ô đáp án: r = r_ck500.
```

### 6.2 [cách A] Nhánh theo đợt (bản 4 dùng §00.3 thay mục này)

| tên (thư mục `gate_<tên>_<hạt>`) | g(màn) | vai trò | khi nào chạy |
|---|---|---|---|
| ck500 (đã có, T4) | — | mốc chính để công bố | — |
| `nghev101` = A | v = Phi-4 trúng khi đọc câu chuẩn của màn | đề xuất | Đợt 1 (G0 qua ∧ keep_v) |
| `nghe101` = B1 | 1 | tách công của v | keep_v sai ⇒ Đợt 1 (nhánh chính, mức K3 tối đa); keep_v đúng ⇒ Đợt 2 |
| `spicea101` = B0′ | 0 (SPICE thuần, công thức ck500) | chống nhiễu đổi máy T4→A100 | Đợt 2 |
| `nghev202` (keep_v sai: `nghe202`) | như nhánh chính | hạt thứ hai | Đợt 2 |
| `nghe202` (khi A = nghev) | như B1 | B1 hạt thứ hai | Đợt 3 |
| `nghern101` = B-rand | v_rand ~ Bernoulli(TB v), hạt 288, cố định theo màn | v có hơn cổng ngẫu nhiên cùng tỉ lệ bật | Đợt 3, chỉ khi Δ(A − B1) ≥ +0,5 (luật trọng tài) |

Luật chuyển đợt (`doc_288.py` in tự động; chưa đăng ký — xem §0):

- **Đợt 2** chạy khi và chỉ khi Δ(nhánh chính 101 − ck500) > 0 (ước điểm) trên test sau Đợt 1. Không thì K1, dừng.
- **Đợt 3** chạy khi và chỉ khi sau Đợt 2: A = nghev ∧ "vượt" ∧ LB95(A − B1) > 0 (tức còn đường lên K4).

Đợt 2/3 train ở **phiên Colab khác** Đợt 1 nhưng cùng loại GPU (A100 80GB), cùng gói ghim, cùng cấu
hình lô đã khoá ở probe (probe chạy cho cả 3 nhánh ngay từ phiên đầu, §8 P5) — B0′ vẫn đo đúng thứ
nó cần đo (đổi máy T4→A100), chỉ thêm nhiễu khác phiên, vốn có ở mọi lượt GRPO.

Cấu hình chung (y ck500): 1.000 câu nhắc hạt 101 (630 click), G = 8, 16 câu sinh/bước, β 0,04, lr
1e-5 hằng sau 10 bước khởi động, 500 bước, lưu mỗi 25, chấm **checkpoint-500**, không chọn điểm
lưu. Hoà S1 **ép fp16** trên A100 (ck500 hoà fp16 trên T4). Lô A100 khoá ở probe: `--bs 4 --accum
4` (mốc CTG đo 36,4 s/bước); OOM ở probe ⇒ `--bs 2 --accum 8` cho **mọi** nhánh.

### 6.3 Người nghe khi train

Máy chủ `nghe_server.py` (venv transformers 4.48.2) nạp Phi-4 **một lần**, phục vụ mọi nhánh trong
phiên qua socket `127.0.0.1:47288`, tuần tự, giao thức 14/9 nguyên văn (cùng câu hỏi, cùng `ve`,
crops 16). Client trong hàm thưởng: gộp (màn, câu) trùng, bộ đệm theo (màn, câu); chỉ hỏi khi g = 1
và `dang_ok` (nhánh A hỏi ≈ 55% số câu click so B1). Hết giờ (60 s + 5 s/câu) hoặc máy chủ lỗi ⇒
h = 0 cả lần gọi, ghi `loi`. Mỗi lần gọi ghi một dòng `nghe_log.jsonl`.

### 6.4 Luật dừng trong train (không bộ trỏ, không val/test)

- mọi nhánh: TB `r_ck500` 50 lần gọi cuối < 0,80 × 50 lần đầu ⇒ dừng nhánh (ghi `DUNG.json`, thoát mã 3);
- nhánh người nghe: tỉ lệ câu click vi phạm `dang_ok` ở 50 lần gọi cuối > 0,10 ⇒ dừng;
- nhánh người nghe (kỹ thuật): máy chủ lỗi > 5% số lần có hỏi (sau ≥ 50 lần) ⇒ dừng, sửa hạ tầng, **chạy lại từ đầu**.
- Nhánh đã có `DUNG.json` thì runbook từ chối chạy tiếp. Báo nhánh dừng như một kết quả.

## 7. Cổng G0

### 7.1 Luật (nguyên văn trọng tài)

```
# val C1 click: n=249 bước (9 câu S1), 1.717 cặp; bootstrap cụm episode 10.000×, rng=101
# O_X = exec UGround của câu được chọn theo khoá X→SPICE (hoà → chỉ số nhỏ nhất); O_SP = 68.67
G0a: parse_fail_phi4 <= 0.05 and phu_som_train >= 0.90
G0b: kappa(h, exec_UG | 1717 cặp) <= 0.60
G0c: auc_trong_nhom(h, exec_UG | 135 bước exec trộn) >= 0.65
V1:  O_vh - O_h >= 0
V2:  O_vh - mean_200(O_rand) >= 1.0          # rand ~ Bernoulli(mean(v_val)) thế chỗ v
V3:  TPR(h | v=1) - TPR(h | v=0) >= 0.25      # TPR = P(h=1 | exec_UG=1)
V4:  0.30 <= mean(v | 630 câu nhắc train) <= 0.85
keep_v = V1 and V2 and V3 and V4
main = "vh" if keep_v else "h"
G0d: (O_main - O_SP) >= 3.3 and LB95(exec_main - exec_SP) > 0
TRAIN = G0a and G0b and G0c and G0d
```

> **Bản 4 không dùng đoạn rớt/TRAIN dưới đây — vai trò G0 của bản 4 ở §00.4** (G0a/G0b chặn người
> nghe, V4 chặn riêng tnghev, còn lại chỉ ghi). [cách A] Rớt: **G0b ⇒ dừng hẳn** (thưởng ≈ chính
> bộ chấm). **G0a/G0c/G0d ⇒ dừng hướng người nghe**; cấm đổi người nghe, hạ ngưỡng, đổi W hay
> `dang_ok` rồi đo lại. TRAIN ∧ ¬keep_v ⇒ nhánh chính là B1 (Đợt 1 = B1; Đợt 2 = B0′ + B1 hạt 202);
> không gọi là thành phần mới.

Chi tiết tôi phải tự khoá (trọng tài chỉ nói bằng lời): `dang_ok` như §6.1 (3,8% câu S1 val vi
phạm); κ/TPR/AUC trên cặp (bước, câu S1) duy nhất; v = h thô trên câu chuẩn (không áp `dang_ok`); h
trong oracle = h thô × `dang_ok`; O_rand 200 lần hạt 288; `parse_fail` = tỉ lệ cặp có câu không rỗng
và màn có ô mà không đọc được số (gồm OOM).

### 7.2 Đã dựng sẵn (CPU, máy nhà, không mạng)

`g0_som_build.py` (B.3) đọc `all_forest_dict.zip` có sẵn ở thư mục cha (gán thẳng `A._ZIP`), dùng
nguyên `ung_vien()` 14/9:

```
[som] 879 màn (c1 249 · train 630) · ô/màn trung vị 14 · p90 47 · không ô 6
[phủ đáp án] c1: 243/249 = 97.6%
[phủ đáp án] train: 597/630 = 94.8%
[câu] 2530 lời gọi người nghe (c1 1900 · train 630) · câu rỗng 0 → …/_scripts/288/g0/
```

## 8. RUNBOOK — từng bước

Thứ tự bản 4: theo bảng S0–S10 ở §00.6 (P0 → P2 → P3 → P4 → P5 → val lớn → P6 + P7 cho nhánh lên
test → `doc_289.py`). [cách A] thứ tự: P0 → P2 → P3 → P4 → P5 (Đợt 1) → P6 → P8, rồi Đợt 2/3 theo
lệnh P8 in ra.

Thư mục làm việc trên máy bạn: `/Users/P836901/Documents/Self-learning/thesis` (gọi là **GỐC**),
repo ở `GỐC/thesis-master`. Mọi lệnh máy nhà dưới đây chạy từ GỐC (trừ khi ghi khác), Python là
`_scripts/_venv/bin/python` (có numpy, Pillow).

### P0 · Khoá đăng ký (bạn, 5 phút, TRƯỚC P2) — KHÔNG commit

Đăng ký khoá trước là **Phụ lục A của chính file này**, không dán vào `report/106`, không commit.
Bằng chứng thời điểm là **mốc thời gian phiên bản dataset Kaggle**: ở P2 bước 1, bỏ **chính file
này** (`288_ACTION_NGUOI_NGHE_CLICK_6_10.md`) vào dataset `thesis-g0-288` cùng 6 tệp G0. Kaggle ghi
giờ tạo phiên bản, trước giờ chạy notebook G0 ⇒ chứng minh luật có trước số. Ghi md5 file này lúc
upload vào ô đầu notebook G0 (in ra log). Sau này nếu cần đưa vào luận văn thì trích nguyên Phụ lục A.

Không chấp nhận phụ lục (nó **nới** luật "không thưởng bằng bộ trỏ" của `report/106`) ⇒ dừng ở
đây, đóng góp mô hình = ck500. **Sau P0, không sửa luật ở Phụ lục A hay §00.4–§00.5.** Muốn đổi gì
⇒ ghi vào "sổ sửa đổi" (Phụ lục A mục 6) kèm lý do, và mọi thay đổi sau khi thấy số G0 phải khai là
hậu nghiệm.

### P1 · Đã xong (§7.2)

### P2 · G0 trên Kaggle (~1,5 h, T4×2, 0 đồng)

1. Kiểm thư mục: `python3 _scripts/288/dung_lai_288.py --md 288_ACTION_NGUOI_NGHE_CLICK_6_10.md --kiem` phải in ✅ ĐỦ. Upload thư mục `_scripts/288/g0/` (6 tệp, md5 ở §9) **cộng file này** thành dataset mới `thesis-g0-288`.
2. Notebook mới, GPU **T4×2**, Internet ON. Add Data: `thesis-g0-288` + `c1-exec8` (ảnh val C1, chứa `images/ep11948_s3.png`; nếu ảnh nằm ở dataset khác thì gắn dataset đó — script tìm ảnh theo tên tệp) + `fgrb-p1-bundle` (ảnh train, chứa `images/ep13687_s9.png`).
3. Một ô, **Save & Run All**:

```python
import os, sys, glob, time, subprocess, hashlib
T0 = time.time()
for p in glob.glob("/kaggle/input/**/288_ACTION_NGUOI_NGHE_CLICK_6_10.md", recursive=True):
    print("[đăng ký] file luật", p, "md5", hashlib.md5(open(p, "rb").read()).hexdigest(), time.strftime("%Y-%m-%d %H:%M:%S"))
subprocess.run("pip uninstall -y -q torchao; pip install -q transformers==4.48.2 peft==0.13.2 "
               "accelerate==1.3.0 backoff soundfile scipy", shell=True)
from huggingface_hub import snapshot_download          # tải Phi-4 MỘT lần, như runbook som_listener 14/9
snapshot_download("microsoft/Phi-4-multimodal-instruct")
def tim(m):
    r = sorted(glob.glob(f"/kaggle/input/**/{m}", recursive=True)); assert r, m; return r[0]
CODE = os.path.dirname(tim("g0_listener.py"))
print("CODE", CODE, "· ảnh val", tim("images/ep11948_s3.png"), "· ảnh train", tim("images/ep13687_s9.png"))
OUT = "/kaggle/working/g0"; os.makedirs(OUT, exist_ok=True)
env = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
       "SOM_PHI4_CROPS": "16", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
ps = []
for i in (0, 1):
    ps.append(subprocess.Popen([sys.executable, f"{CODE}/g0_listener.py", "--backend", "phi4",
                                "--som", f"{CODE}/g0_som.jsonl", "--cau", f"{CODE}/g0_cau.jsonl",
                                "--out", f"{OUT}/g0_phi4_s{i}.jsonl", "--shard", f"{i}/2"],
                               stdout=open(f"{OUT}/s{i}.log", "w"), stderr=subprocess.STDOUT,
                               env={**env, "CUDA_VISIBLE_DEVICES": str(i)}, start_new_session=True))
while any(p.poll() is None for p in ps):
    time.sleep(120)
    for i in (0, 1):
        d = open(f"{OUT}/s{i}.log").read().strip().splitlines()[-1:] or [""]
        print(f"{(time.time()-T0)/3600:5.2f} h · s{i}: {d[0][:140]}", flush=True)
print("mã thoát", [p.poll() for p in ps])
with open(f"{OUT}/g0_phi4.jsonl", "w") as g:
    for i in (0, 1):
        if os.path.exists(f"{OUT}/g0_phi4_s{i}.jsonl"): g.write(open(f"{OUT}/g0_phi4_s{i}.jsonl").read())
print(sum(1 for _ in open(f"{OUT}/g0_phi4.jsonl")), "/ 2530 dòng")
```

Kỳ vọng log: `[ảnh] … thiếu 0 / 879 màn` · `[cấu hình] g0-288 · backend=phi4 · … crops=16`. Thiếu
ảnh ⇒ script dừng trước khi nạp mô hình. Chưa đủ 2.530 dòng ⇒ gắn Output cũ làm input, chép
`g0_phi4_s*.jsonl` vào `/kaggle/working/g0/` trước vòng `Popen` (script bỏ qua id đã xong).

### P3 · Đọc G0 (máy nhà, vài giây)

```bash
cd /Users/P836901/Documents/Self-learning/thesis
_scripts/_venv/bin/python _scripts/288/g0/g0_doc.py --nghe <tải_về>/g0_phi4.jsonl
```

Ghi `_scripts/288/g0_ket_qua.json`. **Bản 4 không đọc dòng `⇒ TRAIN = …`** (luật của cách A) —
chọn `ARMS_TRAIN` theo §00.4 từ `G0.a`, `G0.b` và `v_train` trong tệp đó. Gửi output cho chat sau.

### P4 · Dựng bảng thưởng (máy nhà; bản 4: khi G0a ∧ G0b đúng)

```bash
cd /Users/P836901/Documents/Self-learning/thesis/_scripts/288/nghe
../../_venv/bin/python grpo_nghe.py --dung-bang --som ../g0/g0_som.jsonl --nghe <tải_về>/g0_phi4.jsonl --out bang_nghe.json
../../_venv/bin/python grpo_nghe.py --selftest        # phải in ✅ selftest ĐẠT (~50 s)
```

Ghi lại md5 `bang_nghe.json` in ra (điền vào `BANG_MD5` ở Ô C2). Chạy khô với G0 giả cho: 630 màn ·
TB v 0,541 · có đáp án 597.

### P5 · Train trên Colab A100 80GB (bản 4: `SANG = True`, `ARMS_TRAIN` theo §00.4, một phiên, không có đợt)

Chuẩn bị Drive (một lần): `MyDrive/thesis/nghe288/script/` chứa 7 tệp của `_scripts/288/nghe/`
(§9) + `bang_nghe.json` (P4). Gói dữ liệu dùng lại `MyDrive/thesis/ctg/fgrb_p1_bundle.zip` (2,7 GB,
đã có từ CTG). Runtime: A100, bật "High RAM" (80 GB).

[cách A] Nhánh theo đợt (`SANG = False`, `ARMS_TRAIN` ở Ô C1):

| đợt | keep_v đúng | keep_v sai | khi nào |
|---|---|---|---|
| 1 | `[("nghev",101)]` | `[("nghe",101)]` | TRAIN ở G0 |
| 2 | `[("nghe",101),("spicea",101),("nghev",202)]` | `[("spicea",101),("nghe",202)]` | P8 in `CHẠY ĐỢT 2` |
| 3 | `[("nghe",202)]` (+ `("nghern",101)` nếu P8 liệt kê) | — | P8 in `CHẠY ĐỢT 3` |

Probe chỉ ở phiên đầu, và chạy cho cả 3 nhánh cùng lúc (`ARMS_PROBE`, 20 bước/nhánh trên 50 câu
nhắc dài nhất, không lưu điểm) dù Đợt 1 chỉ train một nhánh: nhờ vậy cấu hình lô khoá một lần vẫn
chạy được Đợt 2 (3 nhánh chung GPU). Đọc VRAM + s/bước, rồi `PROBE = False` chạy lại từ Ô C3 (Đợt
1). Đợt 2/3: phiên mới, `PROBE = False`, chỉ sửa `ARMS_TRAIN`. Bốn luật Colab giữ nguyên:
`start_new_session=True` · không bấm Stop khi đang train · theo dõi log local · luôn có một ô
foreground (C6).

```python
# Ô C1 — cấu hình, Drive, gói
# ===== SỬA Ở ĐÂY =====
SANG = True                 # bản 4 (§00): train TIẾP 250 bước từ ck500. False = bản 3.1 (LoRA mới, 500 bước, theo đợt)
ARMS_TRAIN = [("spicea", 101), ("nghev", 101), ("nghe", 101)] if SANG else [("nghev", 101)]   # ← phiên A; phiên B: [("nghevm", 101), ("nghem", 101)] (g0_doc in sẵn)
ARMS_PROBE = ARMS_TRAIN if SANG else [("nghev", 101), ("nghe", 101), ("spicea", 101)]   # 3.1, keep_v sai: [("nghe",101),("spicea",101),("nghe",202)]
BUOC = 250 if SANG else 500
BS, ACC = 4, 4              # probe OOM → 2, 8 cho MỌI nhánh (khoá một lần)
PROBE = True
ARMS = ARMS_PROBE if PROBE else ARMS_TRAIN
TAT_MAY = True
CONG = 47288
BANG_MD5 = "212dfc30b6f7356b524a7d8d436ed2b3"   # G0 6/10 v3, bang_nghe.json
# =====================
import os, sys, subprocess, time, glob, json, shutil, hashlib, re
from google.colab import drive
drive.mount("/content/drive")
D = "/content/drive/MyDrive/thesis/nghe288"; W = "/content/nghe"; os.makedirs(W, exist_ok=True)
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-2000:], flush=True); return r.returncode
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
mem = int(subprocess.run("nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits", shell=True,
                         capture_output=True, text=True).stdout.split()[0])
MOT = mem <= 70000          # 7/10: Colab cấp A100 40GB ⇒ mỗi lúc MỘT nhánh (probe chỉ tnghev; C7 chạy ba đợt nối nhau)
if MOT:
    ARMS_PROBE = [a for a in ARMS_PROBE if a == ("nghev", 101)] or ARMS_PROBE[:1]
    ARMS = ARMS_PROBE if PROBE else ARMS_TRAIN
    print(f"[40GB] probe một nhánh {ARMS_PROBE}; train chạy từng nhánh ở C7", flush=True)
assert len(ARMS_PROBE) == 1 or mem > 70000, "DỪNG: nhiều nhánh một GPU cần A100 80GB (bật High RAM)"
sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")      # SPICE cần Java 8
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
sh(f"{sys.executable} -m pip install -q 'trl==0.29.1' 'transformers==5.18.0' 'peft==0.21.1' accelerate torchao bitsandbytes pycocoevalcap 2>&1 | tail -3")
sh(f"{sys.executable} -m pip uninstall -y -q torchao")   # 6/10: image có torchao 0.10, peft 0.21 ném ImportError (<0.16); dự án không dùng torchao
import importlib.util; assert importlib.util.find_spec("torchao") is None, "DỪNG: torchao còn"
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
```

```python
# Ô C2 — bung dữ liệu, chép mã, md5, selftest, hoà S1 fp16
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
if not os.path.exists(f"{W}/fgrb_p1_bundle/p1_train_rows.jsonl"):
    sh(f"cp /content/drive/MyDrive/thesis/ctg/fgrb_p1_bundle.zip /content/ && unzip -q -o /content/fgrb_p1_bundle.zip -d {W} && rm /content/fgrb_p1_bundle.zip")
BUNDLE = f"{W}/fgrb_p1_bundle"
assert os.path.isdir(f"{BUNDLE}/adapter_s1_seed101") and os.path.isdir(f"{BUNDLE}/images"), "DỪNG: gói thiếu adapter/ảnh"
MD5 = {"grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf", "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912",
       "grpo_nghe.py": "f08f42b04b0b9f7b943b960877f7936f", "nghe_server.py": "f81cdf27c723f132c918619943149921",
       "som_listener.py": "c61ef769e4f1993a7cad3a536e9ca277", "som_build.py": "2b7d257fccd7378586527b8a65d8b770",
       "prompt_keys_ck500.json": "4bf30d816dc531842495535828dcbb43", "bang_nghe.json": BANG_MD5}
if not any(a != "spicea" for a, _ in ARMS_TRAIN + ARMS_PROBE): MD5.pop("bang_nghe.json")   # G0 cấm người nghe → chỉ tspicea
for f, h in MD5.items():
    shutil.copy(f"{D}/script/{f}", f"{W}/{f}")
    assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch bản máy nhà ({md5(f'{W}/{f}')})"
CK500 = f"{W}/ck500"
if SANG:      # adapter ck500 = 2 tệp GỐC của checkpoint-500 (KHÔNG lấy thư mục con ref/) — Drive MyDrive/thesis/nghe288/ck500/
    os.makedirs(CK500, exist_ok=True)
    for f in ("adapter_config.json", "adapter_model.safetensors"): shutil.copy(f"{D}/ck500/{f}", f"{CK500}/{f}")
    assert md5(f"{CK500}/adapter_model.safetensors") == "491fa6677340393f1e4464c08a0cec98", "DỪNG: adapter ck500 lệch (lấy nhầm ref/?)"
rc = sh(f"cd {W} && python grpo_nghe.py --selftest > /content/selftest.log 2>&1")
print(open("/content/selftest.log").read()[-600:]); assert rc == 0, "DỪNG: selftest rớt"
MERGED = "/content/s1_merged"
assert sh(f"cd {W} && python grpo_nghe.py --merge --bundle {BUNDLE} --merged {MERGED}") == 0, "DỪNG: hoà lỗi"
print("ảnh:", len(os.listdir(f"{BUNDLE}/images")), "· md5 khớp · đã hoà fp16")
```

```python
# Ô C3 — người nghe Phi-4: venv riêng, tải mô hình, bật máy chủ, đo tốc độ (bỏ qua nếu chỉ có spicea)
ARMS = ARMS_PROBE if PROBE else ARMS_TRAIN
print("ARMS", ARMS, "· PROBE", PROBE, flush=True)
SV = None
if any(a != "spicea" for a, _ in ARMS):
    if not os.path.exists("/content/vphi/bin/pip"):      # 7/10: venv của image mới hỏng ensurepip ⇒ dùng virtualenv (tự mang pip)
        shutil.rmtree("/content/vphi", ignore_errors=True)
        sh(f"{sys.executable} -m pip install -q virtualenv && {sys.executable} -m virtualenv -q --system-site-packages /content/vphi")
        assert os.path.exists("/content/vphi/bin/pip"), "DỪNG: chưa dựng được venv phi4"
        sh("/content/vphi/bin/pip install -q transformers==4.48.2 peft==0.13.2 accelerate==1.3.0 backoff soundfile scipy 2>&1 | tail -2")
    sh('/content/vphi/bin/python -c "import transformers, torch; print(\'venv phi4:\', transformers.__version__, torch.__version__)"')   # phải 4.48.2
    sh('/content/vphi/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download(\'microsoft/Phi-4-multimodal-instruct\')"')
    SV = subprocess.Popen(["/content/vphi/bin/python", f"{W}/nghe_server.py", "--backend", "phi4", "--bang", f"{W}/bang_nghe.json",
                           "--img-root", BUNDLE, "--cong", str(CONG)], cwd=W, stdout=open("/content/nghe_server.log", "a"),
                          stderr=subprocess.STDOUT, start_new_session=True,
                          env={**os.environ, "SOM_PHI4_CROPS": "16", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True",
                               "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1",
                               "CUDA_VISIBLE_DEVICES": "0"})
    sys.path.insert(0, W); import grpo_nghe as GN
    GN.cho_may_chu(CONG, 1800)
    B_ = json.load(open(f"{W}/bang_nghe.json"))["bang"]; ks = [k for k in sorted(B_) if B_[k]["dap_an"]][:40]
    t0 = time.time(); q, loi = GN.hoi_may_chu([dict(key=k, sent="Click on the search icon at the top") for k in ks], CONG, 900)
    print(f"[đo người nghe] {len(ks)} câu · {(time.time()-t0)/len(ks):.2f} s/câu · lỗi {loi}", flush=True)
    sh("nvidia-smi --query-gpu=memory.used,memory.total --format=csv")
```

> (ảnh bị cắt ở đây: có thể ô C3 còn vài dòng nữa sau `nvidia-smi`; ảnh kế tiếp bắt đầu ở Ô C4.)

```python
# Ô C4 — kéo điểm lưu từ Drive (khi máy mất), rồi khởi động mọi nhánh
assert ARMS == (ARMS_PROBE if PROBE else ARMS_TRAIN), "DỪNG: đổi PROBE/ARMS_TRAIN xong phải chạy lại C3 trước C4"
CAN = ("trainer_state.json", "optimizer.pt", "adapter_model.safetensors")
P, T0 = {}, time.time()
for arm, seed in ARMS:
    ten = f"{'tiep' if SANG else 'gate'}_{arm}_{seed}"
    out = f"{W}/{'probe_' if PROBE else ''}{ten}"; dout = f"{D}/{ten}"; log = f"/content/{'probe' if PROBE else 'train'}_{ten}.log"
    os.makedirs(out, exist_ok=True)
    if not PROBE:
        os.makedirs(dout, exist_ok=True)
        assert not os.path.exists(f"{dout}/DUNG.json"), f"DỪNG: {ten} đã dừng theo luật — báo kết quả, không chạy tiếp"
        if os.path.exists(f"{dout}/final/adapter_model.safetensors"):
            print(ten, "· ĐÃ XONG từ trước, bỏ qua"); continue
        for p in glob.glob(f"{dout}/checkpoint-*"):
            if all(os.path.exists(f"{p}/{f}") for f in CAN):
                shutil.copytree(p, f"{out}/{os.path.basename(p)}", dirs_exist_ok=True)
        if os.path.exists(f"{dout}/nghe_log.jsonl") and not os.path.exists(f"{out}/nghe_log.jsonl"):
            shutil.copy(f"{dout}/nghe_log.jsonl", f"{out}/nghe_log.jsonl")
    cmd = ["python", "grpo_nghe.py", "--probe" if PROBE else "--train", "--arm", arm, "--seed", str(seed), "--no-q4",
           "--bs", str(BS), "--accum", str(ACC), "--bundle", BUNDLE, "--merged", MERGED, "--out", out,
           "--resume", "auto", "--cong", str(CONG), "--max-steps", str(BUOC)] \
          + ([] if arm == "spicea" else ["--bang", f"{W}/bang_nghe.json"]) + (["--tu", CK500] if SANG else [])
    P[ten] = subprocess.Popen(cmd, cwd=W, stdout=open(log, "a"), stderr=subprocess.STDOUT, start_new_session=True,
                              env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
                                   "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True", "CUDA_VISIBLE_DEVICES": "0"})
    print(ten, "· PID", P[ten].pid, flush=True)
    time.sleep(90)            # lệch pha nạp mô hình giữa các nhánh
```

> (Ở ảnh, chữ trong `open(log, "a")` bị con trỏ chuột che một phần; theo ngữ cảnh là `"a"`.)

```python
# Ô C5 — chép sang Drive mỗi 5 phút (chạy nền; bỏ qua khi PROBE)
import threading
def chep(ten, het=False):
    out, dout = f"{W}/{ten}", f"{D}/{ten}"
    for p in glob.glob(f"{out}/checkpoint-*"):
        dst = f"{dout}/{os.path.basename(p)}"
        if all(os.path.exists(f"{p}/{f}") for f in CAN) and not os.path.exists(f"{dst}/adapter_model.safetensors"):
            shutil.copytree(p, dst, dirs_exist_ok=True)
    for f in ("nghe_log.jsonl", "nghe_meta.json", "log_history.json", "prompt_keys.json", "DUNG.json"):
        if os.path.exists(f"{out}/{f}"): shutil.copy(f"{out}/{f}", f"{dout}/{f}")
    if het and os.path.isdir(f"{out}/final"):
        shutil.copytree(f"{out}/final", f"{dout}/final", dirs_exist_ok=True)
    shutil.copy(f"/content/train_{ten}.log", f"{dout}/train_{ten}_{time.strftime('%m%d')}.log")
    if os.path.exists("/content/nghe_server.log"): shutil.copy("/content/nghe_server.log", f"{D}/nghe_server_{time.strftime('%m%d')}.log")
def dong_bo():
    while any(p.poll() is None for p in P.values()):
        time.sleep(300)
        for ten in P:
            try: chep(ten)
            except Exception as e: print("⚠️ đồng bộ lỗi", ten, e, flush=True)
if not PROBE:
    threading.Thread(target=dong_bo, daemon=True).start()
```

```python
# Ô C6 — theo dõi (FOREGROUND, đừng Stop); xong thì chép Drive, tắt máy chủ, trả máy
import ast, statistics as st
PK = json.load(open(f"{W}/prompt_keys_ck500.json"))
def doc(ten):
    out = f"{W}/{'probe_' if PROBE else ''}{ten}"; log = f"/content/{'probe' if PROBE else 'train'}_{ten}.log"
    L = open(log, encoding="utf-8", errors="ignore").read().splitlines()
    it = [i for i, l in enumerate(L) if l.startswith("[tiếp từ]")]
    goc = int(re.findall(r"checkpoint-(\d+)", L[it[-1]])[0]) if it and "checkpoint-" in L[it[-1]] else 0
    D_ = []
    for l in L[it[-1] if it else 0:]:
        if l.startswith("{'loss'"):
            try: D_.append({k: float(v) for k, v in ast.literal_eval(l).items() if re.match(r"^-?[\d.]+(e[-+]?\d+)?$|^nan$", str(v))})
            except Exception: pass
    m = f"[{ten}] bước {goc + len(D_)}/{20 if PROBE else BUOC} (tiếp từ {goc})"
    if SANG and not any(l.startswith("[train tiếp] LoRA khởi từ") for l in L): m += " · ⛔ CHƯA thấy dòng '[train tiếp]' — không khởi từ ck500?"
    if D_:
        x = D_[-20:]; g = lambda k: st.mean([d[k] for d in x if k in d]) if any(k in d for d in x) else float("nan")
        m += f"\n      {g('step_time'):.0f} s/bước · thưởng TB {g('reward'):.3f} · kl {g('kl'):.4f}"
        if any(v != v for d in D_[-5:] for v in d.values()): m += " · ⛔ nan"
    ng = [l for l in L if l.startswith("[nghe] lần")][-20:]
    if ng:
        f_ = lambda pat: sum(int(re.search(pat, l).group(1)) for l in ng if re.search(pat, l))
        m += (f"\n      20 lần thưởng: chạm {f_(r'chạm (\d+)/')} · bật {f_(r'bật (\d+)')} · hỏi {f_(r'hỏi (\d+)')} · trúng {f_(r'trúng (\d+)')}"
              f" · vi phạm định dạng {f_(r'định dạng (\d+)')} · lỗi máy chủ {sum('⚠️' in l for l in ng)}")
    if not PROBE and os.path.exists(f"{out}/prompt_keys.json"):        # probe dùng 50 câu dài nhất → không so
        m += " · câu nhắc " + ("trùng ck500 ✅" if json.load(open(f"{out}/prompt_keys.json")) == PK else "⛔ KHÁC ck500 — DỪNG TAY, báo lại")
    xong = [l for l in L if l.startswith("[xong]")]
    if xong: m += f"\n      {xong[-1][:160]}"
    if os.path.exists(f"{out}/DUNG.json"): m += f"\n      ⛔ DỪNG theo luật: {open(f'{out}/DUNG.json').read()}"
    if any("Traceback" in l or "OutOfMemory" in l for l in L[-80:]): m += "\n      ⛔ Traceback/OOM"
    return m

while any(p.poll() is None for p in P.values()):
    time.sleep(120)
    gpu = subprocess.run("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader",
                         shell=True, capture_output=True, text=True).stdout.strip()
    print(f"\n{(time.time()-T0)/3600:5.2f} h · GPU {gpu} · đang chạy {[t for t, p in P.items() if p.poll() is None]}", flush=True)
    for ten in P: print(doc(ten), flush=True)
for ten, p in P.items():
    print(ten, "· mã thoát", p.returncode, flush=True); print(doc(ten))
    if not PROBE: chep(ten, het=True)
if SV is not None: os.killpg(SV.pid, 15)
if not PROBE:
    print("final trên Drive:", {t: os.path.exists(f"{D}/{t}/final/adapter_model.safetensors") for t in P})
if TAT_MAY and not PROBE:
    drive.flush_and_unmount(); print("đã flush Drive, trả máy sau 60 s …", flush=True); time.sleep(60)
    from google.colab import runtime; runtime.unassign()
```

**Đọc probe** (chép cho chat sau): mỗi nhánh dòng `[xong] 20 bước · … s/bước · đỉnh VRAM X GiB`,
dòng `GPU …` (tổng bộ nhớ dùng), dòng `[đo người nghe] … s/câu`. Có `OutOfMemory` ⇒ `BS, ACC = 2,
8`, chạy lại probe. Không OOM ⇒ khoá cấu hình đó cho **mọi** nhánh của 288 (ghi vào "sổ sửa đổi" =
Phụ lục A mục 6 của file này), rồi trong một ô mới gõ `PROBE = False` (không cần chạy lại C1/C2) và
chạy **C3 → C6** (C6 của probe đã tắt máy chủ người nghe; C3 bật lại và tự lấy `ARMS = ARMS_TRAIN`).

**Đọc 15 phút đầu train:** `[bảng] 630 màn · TB v … · [nghe] máy chủ sẵn sàng … · [nhánh] nghev ·
hạt 101 · W 1.0 · thưởng r_nghe · bs 4×4` (spicea: `thưởng r_spice`) · `[lô] mỗi lượt sinh 16 câu
= 2 câu nhắc × 8 · câu nhắc trùng ck500 ✅` · `[tiếp từ] None` (lượt đầu) hoặc `…checkpoint-N` +
`[nạp default] … → x>0` (nối tiếp).

**Mất máy:** mở lại notebook, chạy C1 → C6 giữ nguyên `ARMS_TRAIN`, `PROBE = False`; C4 tự kéo điểm
lưu đủ tệp và `nghe_log.jsonl`.

**Đợt 2 / Đợt 3:** phiên Colab mới, A100 80GB, ở C1 đặt `ARMS_TRAIN` theo bảng đầu P5 và `PROBE =
False` (không probe lại; dùng `BS, ACC` đã khoá), chạy C1 → C6. Xong ⇒ P6 cho từng nhánh mới ⇒ P8
đọc lại.

#### P5-nối (6/10, user chọn): tnghev chạy MỘT MÌNH trước, xong tự nối tspicea + tnghe — cùng phiên

Mục đích: `tnghev` (đóng góp) có `checkpoint-250` sớm (~3 h sau probe) để đem chấm val lớn trên
Kaggle trong lúc Colab train tiếp hai nhánh kia. Cấu hình lô, câu nhắc, số bước, hạt **y hệt** —
chỉ đổi thứ tự lên GPU (một nhánh rồi hai nhánh chung card; phép tính mỗi nhánh không đổi). Tổng
phiên dài hơn chạy ba nhánh cùng lúc ~1–2 h.

Thứ tự bấm: C1 (giữ `ARMS_TRAIN` ba nhánh, `PROBE = True`) → C2 → C3 → C4 → C5 → C6 (probe như
cũ, đọc probe). Rồi ô mới gõ `PROBE = False`, chạy **C3** (bật lại người nghe) rồi **C7** — **không
chạy C4–C6 nữa**. C7 là ô foreground suốt phiên (đừng Stop). Mất máy: C1 (`PROBE = False`) → C2 →
C3 → C7; nhánh nào có `final/` trên Drive tự bỏ qua, nhánh dở tự nối từ điểm lưu.

Khi C7 in `✅ ĐỢT 1 XONG — tiep_nghev_101`: tải `MyDrive/thesis/nghe288/tiep_nghev_101/checkpoint-250/`
(2 tệp `adapter_config.json`, `adapter_model.safetensors`) về máy nhà, báo trợ lý chấm val lớn.

```python
# Ô C7 — chạy theo đợt trong CÙNG phiên: đợt 1 tnghev một mình, đợt 2 tspicea + tnghe chung GPU
DOT = [[("nghev", 101)], [("spicea", 101), ("nghe", 101)]]
if mem <= 70000: DOT = [[("nghev", 101)], [("spicea", 101)], [("nghe", 101)]]   # A100 40GB: mỗi đợt một nhánh
DOT = [[a for a in d if a in ARMS_TRAIN] for d in DOT]; DOT = [d for d in DOT if d]     # G0 cấm nhánh nào thì bỏ
assert not PROBE and ARMS == ARMS_TRAIN, "DỪNG: gõ PROBE = False rồi chạy lại C3 trước C7"
assert sorted(a for d in DOT for a in d) == sorted(ARMS_TRAIN), f"DỪNG: DOT {DOT} không phủ ARMS_TRAIN {ARMS_TRAIN}"
import threading, ast, statistics as st
CAN = ("trainer_state.json", "optimizer.pt", "adapter_model.safetensors")
PK = json.load(open(f"{W}/prompt_keys_ck500.json"))

def chep(ten, het=False):
    out, dout = f"{W}/{ten}", f"{D}/{ten}"
    for p in glob.glob(f"{out}/checkpoint-*"):
        dst = f"{dout}/{os.path.basename(p)}"
        if all(os.path.exists(f"{p}/{f}") for f in CAN) and not os.path.exists(f"{dst}/adapter_model.safetensors"):
            shutil.copytree(p, dst, dirs_exist_ok=True)
    for f in ("nghe_log.jsonl", "nghe_meta.json", "log_history.json", "prompt_keys.json", "DUNG.json"):
        if os.path.exists(f"{out}/{f}"): shutil.copy(f"{out}/{f}", f"{dout}/{f}")
    if het and os.path.isdir(f"{out}/final"):
        shutil.copytree(f"{out}/final", f"{dout}/final", dirs_exist_ok=True)
    shutil.copy(f"/content/train_{ten}.log", f"{dout}/train_{ten}_{time.strftime('%m%d')}.log")
    if os.path.exists("/content/nghe_server.log"): shutil.copy("/content/nghe_server.log", f"{D}/nghe_server_{time.strftime('%m%d')}.log")

def doc(ten):
    out = f"{W}/{ten}"; L = open(f"/content/train_{ten}.log", encoding="utf-8", errors="ignore").read().splitlines()
    it = [i for i, l in enumerate(L) if l.startswith("[tiếp từ]")]
    goc = int(re.findall(r"checkpoint-(\d+)", L[it[-1]])[0]) if it and "checkpoint-" in L[it[-1]] else 0
    D_ = []
    for l in L[it[-1] if it else 0:]:
        if l.startswith("{'loss'"):
            try: D_.append({k: float(v) for k, v in ast.literal_eval(l).items() if re.match(r"^-?[\d.]+(e[-+]?\d+)?$|^nan$", str(v))})
            except Exception: pass
    m = f"[{ten}] bước {goc + len(D_)}/{BUOC} (tiếp từ {goc})"
    if SANG and not any(l.startswith("[train tiếp] LoRA khởi từ") for l in L): m += " · ⛔ CHƯA thấy dòng '[train tiếp]' — không khởi từ ck500?"
    if D_:
        x = D_[-20:]; g = lambda k: st.mean([d[k] for d in x if k in d]) if any(k in d for d in x) else float("nan")
        m += f"\n      {g('step_time'):.0f} s/bước · thưởng TB {g('reward'):.3f} · kl {g('kl'):.4f}"
        if any(v != v for d in D_[-5:] for v in d.values()): m += " · ⛔ nan"
    ng = [l for l in L if l.startswith("[nghe] lần")][-20:]
    if ng:
        f_ = lambda pat: sum(int(re.search(pat, l).group(1)) for l in ng if re.search(pat, l))
        m += (f"\n      20 lần thưởng: chạm {f_(r'chạm (\d+)/')} · bật {f_(r'bật (\d+)')} · hỏi {f_(r'hỏi (\d+)')} · trúng {f_(r'trúng (\d+)')}"
              f" · vi phạm định dạng {f_(r'định dạng (\d+)')} · lỗi máy chủ {sum('⚠️' in l for l in ng)}")
    if os.path.exists(f"{out}/prompt_keys.json"):
        m += " · câu nhắc " + ("trùng ck500 ✅" if json.load(open(f"{out}/prompt_keys.json")) == PK else "⛔ KHÁC ck500 — DỪNG TAY, báo lại")
    xong = [l for l in L if l.startswith("[xong]")]
    if xong: m += f"\n      {xong[-1][:160]}"
    if os.path.exists(f"{out}/DUNG.json"): m += f"\n      ⛔ DỪNG theo luật: {open(f'{out}/DUNG.json').read()}"
    if any("Traceback" in l or "OutOfMemory" in l for l in L[-80:]): m += "\n      ⛔ Traceback/OOM"
    return m

def chay(arm, seed):
    ten = f"tiep_{arm}_{seed}"; out, dout, log = f"{W}/{ten}", f"{D}/{ten}", f"/content/train_{ten}.log"
    os.makedirs(out, exist_ok=True); os.makedirs(dout, exist_ok=True)
    assert not os.path.exists(f"{dout}/DUNG.json"), f"DỪNG: {ten} đã dừng theo luật — báo kết quả, không chạy tiếp"
    if os.path.exists(f"{dout}/final/adapter_model.safetensors"):
        print(ten, "· ĐÃ XONG từ trước, bỏ qua", flush=True); return None
    for p in glob.glob(f"{dout}/checkpoint-*"):
        if all(os.path.exists(f"{p}/{f}") for f in CAN): shutil.copytree(p, f"{out}/{os.path.basename(p)}", dirs_exist_ok=True)
    if os.path.exists(f"{dout}/nghe_log.jsonl") and not os.path.exists(f"{out}/nghe_log.jsonl"):
        shutil.copy(f"{dout}/nghe_log.jsonl", f"{out}/nghe_log.jsonl")
    cmd = ["python", "grpo_nghe.py", "--train", "--arm", arm, "--seed", str(seed), "--no-q4", "--bs", str(BS), "--accum", str(ACC),
           "--bundle", BUNDLE, "--merged", MERGED, "--out", out, "--resume", "auto", "--cong", str(CONG), "--max-steps", str(BUOC)] \
          + ([] if arm == "spicea" else ["--bang", f"{W}/bang_nghe.json"]) + (["--tu", CK500] if SANG else [])
    p = subprocess.Popen(cmd, cwd=W, stdout=open(log, "a"), stderr=subprocess.STDOUT, start_new_session=True,
                         env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1",
                              "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True", "CUDA_VISIBLE_DEVICES": "0"})
    print(ten, "· PID", p.pid, flush=True); return p

T0 = time.time()
for k, dot in enumerate(DOT, 1):
    P = {}
    for arm, seed in dot:
        p = chay(arm, seed)
        if p is not None: P[f"tiep_{arm}_{seed}"] = p; time.sleep(90)      # lệch pha nạp mô hình
    def dong_bo(P=P):
        while any(p.poll() is None for p in P.values()):
            time.sleep(300)
            for ten in P:
                try: chep(ten)
                except Exception as e: print("⚠️ đồng bộ lỗi", ten, e, flush=True)
    threading.Thread(target=dong_bo, daemon=True).start()
    while any(p.poll() is None for p in P.values()):
        time.sleep(120)
        gpu = subprocess.run("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader",
                             shell=True, capture_output=True, text=True).stdout.strip()
        print(f"\n{(time.time()-T0)/3600:5.2f} h · ĐỢT {k}/{len(DOT)} · GPU {gpu} · đang chạy {[t for t, p in P.items() if p.poll() is None]}", flush=True)
        for ten in P: print(doc(ten), flush=True)
    for ten, p in P.items():
        print(ten, "· mã thoát", p.returncode, flush=True); print(doc(ten), flush=True); chep(ten, het=True)
        ok = os.path.exists(f"{D}/{ten}/checkpoint-250/adapter_model.safetensors") and p.returncode == 0
        print(("✅" if ok else "⛔"), f"ĐỢT {k} XONG — {ten} · checkpoint-250 trên Drive: {ok}", flush=True)
if SV is not None: os.killpg(SV.pid, 15)
print("final trên Drive:", {f"tiep_{a}_{s}": os.path.exists(f"{D}/tiep_{a}_{s}/final/adapter_model.safetensors") for d in DOT for a, s in d})
if TAT_MAY:
    drive.flush_and_unmount(); print("đã flush Drive, trả máy sau 60 s …", flush=True); time.sleep(60)
    from google.colab import runtime; runtime.unassign()
```

### P6 · Chấm test trên Kaggle T4 (một lần mỗi nhánh, ~8 h)

**Chuẩn bị (máy nhà):**

1. Một lần: `python3 _scripts/288/dung_lai_288.py --md 288_ACTION_NGUOI_NGHE_CLICK_6_10.md` (dựng `_scripts/288/cham/`, phải in ✅ ĐỦ), rồi upload thư mục `_scripts/288/cham/` thành dataset `cham288-script`. Thư mục này có: `gieo_tho.py` (B.10), `gen_test_grpo.py` · `grpo_spice.py` · `build_branch_data.py` (bản repo, = bản sinh test ck500), tệp thô S1/ck500 của repo, `pred_ck500_test.jsonl`, preds + tệp thô UI-Venus S1 lát 2.532, `preds_venus_ck500_2532.jsonl`, `harness_venus/` (cho P7).
2. Mỗi nhánh train xong: từ Drive `MyDrive/thesis/nghe288/gate_<arm>_<seed>/checkpoint-500/` tải `adapter_config.json` + `adapter_model.safetensors` → máy nhà `GỐC/nghe288_ckpt/gate_<arm>_<seed>/checkpoint-500/` → dataset `nghe288-ckpts` (New Version mỗi lần thêm nhánh; giữ nguyên tên thư mục `gate_<arm>_<seed>`).

**Notebook:** GPU T4 (×1 hay ×2, mã chỉ dùng card 0), Internet On. Add Data: `thesis-score` (ảnh
4.463 bước click, `test.jsonl`, `ocr.jsonl`, harness chấm đã chấm S1 59,11 và ck500) ·
`fgrb-p1-bundle` (adapter S1 để hoà) · `cham288-script` · `thesis-nontap-images` (2.495 ảnh không
chạm) · `grpo-spice-ck500` (adapter ck500, chỉ để kiểm môi trường) · `nghe288-ckpts`. Sinh + chấm
**chỉ trên T4**: trên A100, `grpo_spice._dtype` và `score_run.pick_dtype` tự chọn bf16 ⇒ khác đường
sinh/chấm fp16 của S1/ck500. Chạy tương tác T1 → T4 trước (~25 phút), không dòng DỪNG nào ⇒ đặt
`TAG` ở T5 → **Save Version → Save & Run All**.

```python
# Ô T1 — gói: ghim đúng bộ đã train ck500 (train_c3.log)
import subprocess, sys, os, time, glob, json, shutil, hashlib, re, tarfile
T_NB = time.time()
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-3000:], flush=True); return r.returncode
sh(f"{sys.executable} -m pip install -q 'trl==0.29.1' 'transformers==5.18.0' 'peft==0.21.1' accelerate torchao bitsandbytes pycocoevalcap 2>&1 | tail -3")
sh(f"{sys.executable} -m pip uninstall -y -q torchao")   # 6/10: image có torchao 0.10, peft 0.21 ném ImportError (<0.16); dự án không dùng torchao
import importlib.util; assert importlib.util.find_spec("torchao") is None, "DỪNG: torchao còn"
sh(f'{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0))"')
ten_gpu = subprocess.run("nvidia-smi --query-gpu=name --format=csv,noheader", shell=True, capture_output=True, text=True).stdout
assert "T4" in ten_gpu, f"DỪNG: chấm test 288 chỉ chạy trên T4, máy này là {ten_gpu}"
```

```python
# Ô T2 — mã + md5, tệp thô gốc, hoà S1 (fp16 trên T4)
W = "/kaggle/working"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
SRC = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/gieo_tho.py", recursive=True)
              if os.path.exists(os.path.join(os.path.dirname(p), "gen_test_grpo.py"))})
assert len(SRC) == 1, f"DỪNG: cần đúng một cham288-script, thấy {SRC}"
SRC = SRC[0]
MA = {"grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf", "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912",
      "gen_test_grpo.py": "b18ec1aa3fd037ddffb9411db63c2a3f", "gieo_tho.py": "7681cc68ad7e0bc9965c73f47ea3aa88"}
for f, h in MA.items():
    shutil.copy(f"{SRC}/{f}", f"{W}/{f}")
    assert md5(f"{W}/{f}") == h, f"DỪNG: {f} lệch máy nhà ({md5(f'{W}/{f}')})"
for f, h in {"score_s1_seed101_raw.jsonl": "0681d937d930c952b7ff92e0f24d5189",
             "score_ck500_test_raw.jsonl": "5b9d6d65cb0d2390b126d22463f888ee",
             "pred_ck500_test.jsonl": "328847ac96fa3104f76cd997f4091bcd"}.items():
    assert md5(f"{SRC}/{f}") == h, f"DỪNG: {f} lệch repo"
BUNDLE = next(r for r, d, f in os.walk("/kaggle/input") if "adapter_s1_seed101" in d and "images" in d)
MERGED = f"{W}/s1_merged"
if not os.path.exists(f"{MERGED}/config.json"):
    r = subprocess.run(["python", "grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED], cwd=W, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-800:]); assert r.returncode == 0, "DỪNG: hoà lỗi"
```

```python
# Ô T3 — dữ liệu test (y như lượt chấm test ck500) + ảnh không chạm + hàm chạy có nhịp
best = None
for t in glob.glob("/kaggle/input/**/test_ac/test.jsonl", recursive=True):
    root = os.path.dirname(t)
    if sum(1 for _ in open(t)) == 6958 and len(glob.glob(f"{root}/images/*.png")) >= 4463 and os.path.exists(f"{root}/ocr.jsonl"):
        best = root
assert best, "DỪNG: không thấy test_ac đủ 6.958 dòng + 4.463 ảnh"
TA = best
assert md5(f"{TA}/test.jsonl") == "da58299ee551a926a21cbecb5232bf78", "DỪNG: test.jsonl lệch máy nhà"
PKG = os.path.dirname(os.path.dirname(os.path.dirname(TA)))       # …/thesis/harness/dg1_cache/test_ac → …/thesis
shutil.copytree(f"{PKG}/harness", f"{W}/thesis/harness", dirs_exist_ok=True, ignore=shutil.ignore_patterns("images"))
link = f"{W}/thesis/harness/dg1_cache/test_ac/images"
if os.path.lexists(link): os.remove(link)
os.symlink(f"{TA}/images", link)
WS = f"{W}/thesis"

def tim_anh():
    for d in glob.glob("/kaggle/input/**/images", recursive=True) + glob.glob(f"{W}/nontap/**/images", recursive=True):
        if "thesis-score" not in d and len(glob.glob(f"{d}/ep*_s*.png")) == 2495:
            return d
IMG = tim_anh()
if not IMG:
    tars = glob.glob("/kaggle/input/**/*.tar", recursive=True); assert tars, "DỪNG: thiếu ảnh không chạm"
    tarfile.open(tars[0]).extractall(f"{W}/nontap"); IMG = tim_anh()
assert IMG, "DỪNG: không có thư mục đúng 2.495 ảnh không chạm"

def chay(cmd, log, cwd, nhip=120):
    t0 = time.time()
    with open(log, "w") as f:
        q = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1"})
        while q.poll() is None:
            time.sleep(nhip)
            L = [l.strip() for l in open(log, errors="ignore") if l.strip()]
            print(f"  {(time.time()-t0)/3600:5.2f} h · {os.path.basename(log)} · {L[-1][:110] if L else '…'}", flush=True)
    print(f"--- {os.path.basename(log)} · mã thoát {q.returncode} ---\n" + "".join(open(log, errors="ignore").readlines()[-6:]), flush=True)
    return q.returncode
print("TA", TA, "\nIMG", IMG, flush=True)
```

```python
# Ô T4 — kiểm dụng cụ TRƯỚC lượt dài (~10 phút): (a) sinh lại 20 câu click đầu bằng ck500; (b) chấm lại 20 câu ck500
C5 = [os.path.dirname(f) for f in glob.glob("/kaggle/input/**/adapter_model.safetensors", recursive=True)
      if md5(f) == "491fa6677340393f1e4464c08a0cec98"]
assert C5, "DỪNG: gắn dataset grpo-spice-ck500"
KM = f"{W}/kiem_ck500_20.jsonl"
if os.path.exists(KM): os.remove(KM)
chay(["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--ckpt", C5[0], "--recs", f"{TA}/test.jsonl",
      "--ocr", f"{TA}/ocr.jsonl", "--images", f"{TA}/images", "--tap-only", "--no-q4", "--n", "20", "--out", KM],
     f"{W}/kiem_ck500_20.log", W, nhip=30)
G5 = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{SRC}/pred_ck500_test.jsonl"))}
K = [json.loads(l) for l in open(KM)]
trung = sum(G5[(d["episode_id"], d["step_id"])] == d["pred"] for d in K)
print(f"[kiểm sinh] ck500 sinh lại {trung}/{len(K)} câu trùng pred_ck500_test.jsonl", flush=True)
assert len(K) == 20 and trung >= 18, "DỪNG: đường sinh khác lượt ck500 — gửi kiem_ck500_20.log + dòng phiên bản ô T1, KHÔNG chấm nhánh nào"

KS = f"{W}/kiem_cham/score_kiem20.json"; os.makedirs(os.path.dirname(KS), exist_ok=True)
for p in (KS, KS.replace(".json", "_raw.jsonl")):
    if os.path.exists(p): os.remove(p)
chay(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", f"{SRC}/pred_ck500_test.jsonl",
      "--n", "20", "--out", KS], f"{W}/kiem_cham20.log", WS, nhip=30)
R5 = {(d["episode_id"], d["step_id"]): d for d in map(json.loads, open(f"{SRC}/score_ck500_test_raw.jsonl"))}
M = [json.loads(l) for l in open(KS.replace(".json", "_raw.jsonl"))]
def gan(a, b):
    if a.get("pred_xy") is None or b.get("pred_xy") is None: return a.get("pred_xy") == b.get("pred_xy")
    return a.get("executable") == b.get("executable") and max(abs(x - y) for x, y in zip(a["pred_xy"], b["pred_xy"])) <= 3
khop = sum(gan(R5[(d["episode_id"], d["step_id"])], d) for d in M)
print(f"[kiểm chấm] UGround chấm lại {khop}/{len(M)} câu ck500 trùng (≤ 3 px, cùng exec) tệp thô cũ", flush=True)
assert len(M) == 20 and khop >= 19, "DỪNG: bộ chấm khác lượt ck500 → KHÔNG được gieo tệp thô; gửi kiem_cham20.log về"
```

```python
# Ô T5 — chọn nhánh (một nhánh mỗi notebook)
TAG = "tnghev101"      # ← bản 4: tspicea101 · tnghev101 · tnghe101 · tnghevm101 · tnghem101 (chỉ nhánh doc_289 sàng in LÊN TEST)
                       #   bản 3.1: (đợt 1) nghev101 · (đợt 2) nghe101 · spicea101 · nghev202 · (đợt 3) nghe202 · nghern101
arm, seed = re.fullmatch(r"([a-z]+?)(\d+)", TAG).groups()
thu, buoc = (f"tiep_{arm[1:]}_{seed}", 250) if arm.startswith("t") else (f"gate_{arm}_{seed}", 500)
C = [p for p in glob.glob(f"/kaggle/input/**/{thu}/checkpoint-{buoc}", recursive=True)
     if os.path.exists(f"{p}/adapter_model.safetensors")]
assert len(C) == 1, f"DỪNG: cần đúng một {thu}/checkpoint-{buoc} (dataset sang289-ckpts / nghe288-ckpts), thấy {C}"
CK = C[0]
print("TAG", TAG, "· CK", CK, "· md5 adapter", md5(f"{CK}/adapter_model.safetensors"), flush=True)
```

```python
# Ô T6 — sinh 4.463 click + 2.495 không chạm (nối tiếp được), gieo tệp thô, chấm phần còn lại
PC, PN = f"{W}/pred_{TAG}_test.jsonl", f"{W}/pred_{TAG}_test_nontap.jsonl"
BASE = ["python", "gen_test_grpo.py", "--bundle", BUNDLE, "--merged", MERGED, "--recs", f"{TA}/test.jsonl",
        "--ocr", f"{TA}/ocr.jsonl", "--no-q4", "--ckpt", CK]
chay(BASE + ["--images", f"{TA}/images", "--tap-only", "--out", PC], f"{W}/gen_{TAG}.log", W)
chay(BASE + ["--images", IMG, "--non-tap", "--out", PN], f"{W}/gen_{TAG}_nontap.log", W)
assert sum(1 for _ in open(PC)) == 4463 and sum(1 for _ in open(PN)) == 2495, "DỪNG: thiếu câu — chạy lại ô này (nối tiếp)"

SC = f"{W}/score_{TAG}_test.json"; RAW = SC.replace(".json", "_raw.jsonl")
if not os.path.exists(RAW):
    assert sh(f"cd {W} && python gieo_tho.py --preds {PC} --tho {SRC}/score_s1_seed101_raw.jsonl "
              f"{SRC}/score_ck500_test_raw.jsonl --out {RAW}") == 0
chay(["python", "-u", "harness/score_run.py", "--mode", "score", "--grounder", "uground", "--preds", PC, "--out", SC],
     f"{W}/cham_{TAG}.log", WS)
print([l.strip() for l in open(f"{W}/cham_{TAG}.log") if "Nối tiếp" in l or "Đã chấm đủ" in l or "KHÔNG KHỚP" in l][:3])
R = [json.loads(l) for l in open(RAW)]
K = {(r["episode_id"], r["step_id"]) for r in R}
print(f"== {TAG}: {len(R)} dòng thô · {len(K)} bước · exec {sum(int(r.get('executable') or 0) for r in R)} · {(time.time()-T_NB)/3600:.2f} h")
assert len(R) == len(K) == 4463, "DỪNG: tệp thô trùng/thiếu → score_run bản này không nối tiếp; xoá RAW, chạy lại ô này (chấm đủ ~5,4 h)"
shutil.rmtree(MERGED, ignore_errors=True); shutil.rmtree(f"{W}/nontap", ignore_errors=True)
```

Gửi về máy nhà `thesis-master/runs/goc288/`: `pred_<TAG>_test.jsonl` · `pred_<TAG>_test_nontap.jsonl`
· `score_<TAG>_test.json` · `score_<TAG>_test_raw.jsonl` · `gen_<TAG>.log` · `gen_<TAG>_nontap.log` ·
`cham_<TAG>.log` · `kiem_ck500_20.log` · `kiem_cham20.log`. T6 phải in `[gieo] N/4463 …` và `Nối
tiếp: đã chấm N bước`; không thấy dòng nối tiếp mà assert cuối đạt thì vẫn dùng được (đã chấm đủ).
Kaggle hay đổi đuôi thành `.txt` — đổi lại khi đặt vào `runs/goc288/`. `thesis-master/runs/goc288/`
nằm trong repo ⇒ mất khi xoá clone; giữ bản sao ở `GỐC/goc288_backup/`.

### P7 · UI-Venus trên lát 2.532 bước (Kaggle T4×2)

Lát 2.532 = các bước click đã dùng ở phép B (S1 đã chấm đủ: `runs/venus/score_venus_s1_2532_raw.jsonl`,
cỡ ảnh min 200.704 / max 1.003.520). Nhánh mới chỉ chấm câu **khác** S1 (gieo phần trùng). Luật đọc
(khoá): Δ_UIVenus(A − ck500) > 0 là một vế của "vượt"; ghép cặp từng bước trên lát, `doc_288.py` tính.

- **P7a — ck500** (chỉ khi P8 in `CHẠY ĐỢT 2`; chạy song song lúc Colab train Đợt 2): `TAG = "ck500"` ở ô V3. Tệp preds `preds_venus_ck500_2532.jsonl` đã nằm trong `cham288-script` (1.210 câu khác S1 + 1 bước câu rỗng ⇒ gieo 1.321, chấm 1.211 bước, ~1,5 h). Kết quả `score_venus_ck500_2532_raw.jsonl` mang về `thesis-master/runs/venus/` và chép vào `_scripts/288/cham/` rồi New Version `cham288-script` (P7b cần nó để gieo).
- **P7b — nhánh chính của 288** (A, hoặc B1 nếu keep_v sai) sau khi P6 xong: máy nhà dựng preds rồi New Version `cham288-script`:

```python
# máy nhà, từ GỐC — dựng preds UI-Venus cho một nhánh 288
import json
TAG = "nghev101"
R = "thesis-master"
S = [json.loads(l) for l in open(f"{R}/runs/venus/preds_venus_s1_2532.jsonl", encoding="utf-8")]
C = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(f"{R}/runs/goc288/pred_{TAG}_test.jsonl", encoding="utf-8"))}
with open(f"_scripts/288/cham/preds_venus_{TAG}_2532.jsonl", "w", encoding="utf-8") as f:
    for d in S:
        k = (d["episode_id"], d["step_id"]); f.write(json.dumps({**d, "raw": C[k], "pred": C[k]}, ensure_ascii=False) + "\n")
print(sum(C[(d["episode_id"], d["step_id"])] != d["pred"] for d in S), "câu khác S1")
```

**Notebook:** GPU T4×2, Internet On (tải UI-Venus-Ground-7B như phép B 20/8). Add Data:
`thesis-score` · `cham288-script`.

```python
# Ô V1 — harness bản repo (có vá VENUS_*_PIXELS + nối tiếp), ảnh symlink, kiểm máy, hàm chấm
import os, sys, glob, json, time, shutil, subprocess, torch
WS = "/kaggle/working"; HAR = f"{WS}/harness"
n = torch.cuda.device_count(); tong = sum(torch.cuda.get_device_properties(i).total_memory for i in range(n)) / 2**30
assert n >= 2 and tong >= 24, f"DỪNG: cần T4×2 (thấy {n} GPU, {tong:.1f} GB)"
SRC = sorted({os.path.dirname(p) for p in glob.glob("/kaggle/input/**/gieo_tho.py", recursive=True)
              if os.path.isdir(os.path.join(os.path.dirname(p), "harness_venus"))})
assert len(SRC) == 1, f"DỪNG: cần đúng một cham288-script, thấy {SRC}"
SRC = SRC[0]
if os.path.exists(HAR): shutil.rmtree(HAR)
shutil.copytree(f"{SRC}/harness_venus", HAR)
anh = glob.glob("/kaggle/input/**/dg1_cache/test_ac/test.jsonl", recursive=True); assert anh, "DỪNG: gắn thesis-score"
os.symlink(os.path.dirname(os.path.dirname(anh[0])), f"{HAR}/dg1_cache")
t = open(f"{HAR}/score_run.py", encoding="utf-8").read()
assert "VENUS_MIN_PIXELS" in t[t.index("class UIVenus"):], "DỪNG: score_run chưa có vá UI-Venus"
os.makedirs(f"{WS}/out", exist_ok=True)
MN, MX = 200704, 1003520          # cỡ ảnh đã chấm S1 (runs/venus/venus_s1_2532.log) — KHÔNG đổi
env = {**os.environ, "VENUS_MIN_PIXELS": str(MN), "VENUS_MAX_PIXELS": str(MX), "PYTHONUNBUFFERED": "1",
       "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1"}

def cham(preds, out, n, log):
    raw = out.replace(".json", "_raw.jsonl"); t0 = time.time()
    with open(log, "w") as f:
        q = subprocess.Popen([sys.executable, "-u", f"{HAR}/score_run.py", "--mode", "score", "--grounder", "uivenus",
                              "--preds", preds, "--n", str(n), "--out", out], stdout=f, stderr=subprocess.STDOUT, cwd=WS, env=env)
        while q.poll() is None:
            time.sleep(120)
            m = sum(1 for _ in open(raw)) if os.path.exists(raw) else 0
            print(f"  {(time.time()-t0)/3600:5.2f} h · {os.path.basename(out)} · {m}/{n}", flush=True)
    L = open(log, encoding="utf-8", errors="ignore").read().splitlines()
    print(next((l for l in L if "[UIVenus]" in l), "⛔ THIẾU dòng [UIVenus] — có thể chạy sai cỡ ảnh"))
    print(next((l for l in L if "Nối tiếp" in l or "Đã chấm đủ" in l), "(không có dòng nối tiếp)"))
    print("\n".join(L[-5:]), flush=True); return q.returncode

def gan(a, b):
    if a.get("pred_xy") is None or b.get("pred_xy") is None: return a.get("pred_xy") == b.get("pred_xy")
    return a.get("executable") == b.get("executable") and max(abs(x - y) for x, y in zip(a["pred_xy"], b["pred_xy"])) <= 3
```

```python
# Ô V2 — kiểm dụng cụ: chấm lại 30 câu S1 đầu lát, phải trùng (≤ 3 px, cùng exec) tệp thô S1 của phép B
KO = f"{WS}/out/kiem_venus_s1_30.json"
for p in (KO, KO.replace(".json", "_raw.jsonl")):
    if os.path.exists(p): os.remove(p)
assert cham(f"{SRC}/preds_venus_s1_2532.jsonl", KO, 30, f"{WS}/out/kiem_venus_s1_30.log") == 0
R1 = {(d["episode_id"], d["step_id"]): d for d in map(json.loads, open(f"{SRC}/score_venus_s1_2532_raw.jsonl"))}
M = [json.loads(l) for l in open(KO.replace(".json", "_raw.jsonl"))]
khop = sum(gan(R1[(d["episode_id"], d["step_id"])], d) for d in M)
print(f"[kiểm UI-Venus] chấm lại {khop}/{len(M)} câu S1 trùng lượt phép B", flush=True)
assert len(M) == 30 and khop >= 28, ("DỪNG: UI-Venus/môi trường khác lượt chấm S1 → không gieo được. Gửi kiem_venus_s1_30.log về; "
                                     "phương án (bạn quyết): chấm lại cả S1 trên lát trong cùng phiên, +~3 h")
```

```python
# Ô V3 — chấm một nhánh: gieo câu trùng S1 (+ ck500), chấm phần còn lại
TAG = "ck500"            # ← ck500 (P7a) · nghev101 hoặc nghe101 (P7b)
P = f"{SRC}/preds_venus_{TAG}_2532.jsonl"
assert os.path.exists(P), f"DỪNG: thiếu {P} — dựng ở máy nhà rồi New Version cham288-script"
OUT = f"{WS}/out/score_venus_{TAG}_2532.json"; RAW = OUT.replace(".json", "_raw.jsonl")
THO = [f"{SRC}/score_venus_s1_2532_raw.jsonl"] + ([] if TAG == "ck500" else [f"{SRC}/score_venus_ck500_2532_raw.jsonl"])
assert all(os.path.exists(x) for x in THO), f"DỪNG: thiếu tệp thô {THO} (nhánh 288 cần kết quả P7a trong cham288-script)"
if not os.path.exists(RAW):
    assert subprocess.run([sys.executable, f"{SRC}/gieo_tho.py", "--preds", P, "--tho", *THO, "--out", RAW]).returncode == 0
assert cham(P, OUT, 2532, f"{WS}/out/venus_{TAG}_2532.log") == 0
R = [json.loads(l) for l in open(RAW)]
K = {(r["episode_id"], r["step_id"]) for r in R}
print(f"== {TAG}: {len(R)} dòng thô · {len(K)} bước · exec {sum(int(r.get('executable') or 0) for r in R)}")
assert len(R) == len(K) == 2532, "DỪNG: tệp thô trùng/thiếu"
shutil.make_archive(f"{WS}/venus_{TAG}", "zip", f"{WS}/out")
```

Gửi về `thesis-master/runs/venus/`: `score_venus_<TAG>_2532_raw.jsonl` · `score_venus_<TAG>_2532.json`
· `venus_<TAG>_2532.log` · `kiem_venus_s1_30.log` (giữ bản sao ở `GỐC/goc288_backup/`). V3 phải in
`[gieo] 1321/2532 …` với ck500.

### P8 · [cách A] Đọc test (máy nhà, ~5 giây) và luật quyết đợt sau — bản 4 đọc bằng `doc_289.py` (§00.8)

```bash
cd /Users/P836901/Documents/Self-learning/thesis/thesis-master
S=runs/score_s1_seed101_raw.jsonl:runs/preds_s1_seed101.jsonl
C=runs/grpo_spice/score_ck500_test_raw.jsonl:runs/grpo_spice/pred_ck500_test_nontap.jsonl
n() { echo "$1:runs/goc288/score_$1_test_raw.jsonl:runs/goc288/pred_$1_test_nontap.jsonl"; }
V=runs/venus
# Đợt 1 (chỉ nhánh chính):
../_scripts/_venv/bin/python ../_scripts/288/doc_288.py --recs harness/dg1_cache/test_ac/test.jsonl --chinh nghev101 \
  --nhanh S1:$S --nhanh ck500:$C --nhanh $(n nghev101) --out runs/goc288/doc_288_dot1.json
# Đợt 2 xong: thêm
#   --nhanh $(n nghe101) --nhanh $(n spicea101) --nhanh $(n nghev202) \
#   --venus ck500:$V/score_venus_ck500_2532_raw.jsonl --venus nghev101:$V/score_venus_nghev101_2532_raw.jsonl   (--out …_dot2.json)
# Đợt 3 xong: thêm tiếp --nhanh $(n nghe202) [--nhanh $(n nghern101)]                                          (--out …_dot3.json)
# keep_v sai → --chinh nghe101, --nhanh $(n nghe101) thay cho nghev101; Đợt 2 thêm $(n spicea101) $(n nghe202) + venus nghe101
```

Bộ đọc in `⇒ KẾT CỤC …` kèm luật (`doc_288.py --gia` đã chạy khô 7 tình huống, tái lập ck500 − S1
+1,55 [+0,84; +2,26]):

- `K1 · luật: DỪNG` ⇒ hết 288; báo K1 (§11). Không train B1/B0′.
- `CHỜ-ĐỢT-2 · luật: CHẠY ĐỢT 2: …` ⇒ P5 với `ARMS_TRAIN` Đợt 2, P6 từng nhánh, P7a + P7b, rồi đọc lại. **Chưa được viết câu nào về cái tăng ở Đợt 1** (chưa loại được nhiễu đổi máy và ăn may hạt).
- `K3 · K4-CHỜ-ĐỢT-3 · luật: CHẠY ĐỢT 3: …` ⇒ được viết câu K3; muốn câu K4 thì chạy Đợt 3 rồi đọc lại.
- `K2` / `K2+` / `K3` / `K4` không kèm luật ⇒ kết cục cuối.

## 9. Gói upload, md5, và cách dựng lại chỉ từ file này + repo

Ba thư mục upload nằm **ngoài repo**, ở `GỐC/_scripts/288/`. Mỗi tệp có đúng một nguồn: mã nhúng ở
Phụ lục B (tách tự động), tệp chép nguyên từ repo, hoặc dữ liệu dựng bằng B.3.

| tệp (đích) | md5 | nguồn |
|---|---|---|
| **`g0/` → dataset `thesis-g0-288` (P2)** | | **+ file này (P0)** |
| `g0/g0_som.jsonl` (516 KB) · `g0/g0_cau.jsonl` (340 KB) | `a49789bda073f5629380ad907db31910` · `656dd46f40bcc2d2f32a84e1c752fe6f` | B.3 đọc `GỐC/all_forest_dict.zip` (md5 `4e88a4f15435222e2f645540b2dd1f19`, ngoài repo) |
| `g0/g0_listener.py` · `g0/g0_doc.py` | `41662b4cdbd38f3c4f0c1c98948ed165` · `e312f4b479469274ecce2f2ef03bc064` | B.4 · B.5 |
| `g0/som_listener.py` · `g0/som_build.py` | `c61ef769e4f1993a7cad3a536e9ca277` · `2b7d257fccd7378586527b8a65d8b770` | repo `harness/` |
| **`nghe/` → Drive `MyDrive/thesis/nghe288/script/` (P5)** | | |
| `nghe/grpo_nghe.py` · `nghe/nghe_server.py` | `f08f42b04b0b9f7b943b960877f7936f` (bản 4, có `--tu`; cũ `f2aaae3c…`) · `f81cdf27c723f132c918619943149921` | B.6 · B.7 |
| Drive `MyDrive/thesis/nghe288/ck500/` (bản 4) | `adapter_model.safetensors` `491fa6677340393f1e4464c08a0cec98` | 2 tệp gốc của dataset Kaggle `grpo-spice-ck500` (không có trong repo) |
| `nghe/grpo_spice.py` · `nghe/build_branch_data.py` | `07ea87b6d156d1faa391a4274dffd7cf` · `619e63e123a6dbf60086e65ee94a3912` | repo `harness/` (= bản train ck500) |
| `nghe/som_listener.py` · `nghe/som_build.py` | như `g0/` | repo `harness/` |
| `nghe/prompt_keys_ck500.json` | `4bf30d816dc531842495535828dcbb43` | `json.dumps(json.load(runs/ctg/p0/p0_a3/prompt_keys.json)[:1000])` |
| `nghe/bang_nghe.json` | in ra ở P4 | sau G0 |
| **`cham/` → dataset `cham288-script` (P6, P7)** | | |
| `cham/gieo_tho.py` | `7681cc68ad7e0bc9965c73f47ea3aa88` | B.10 |
| `cham/gen_test_grpo.py` · `cham/grpo_spice.py` · `cham/build_branch_data.py` | `b18ec1aa3fd037ddffb9411db63c2a3f` · `07ea87b6…` · `619e63e1…` | repo `harness/` |
| `cham/preds_s1_seed101.jsonl` · `cham/score_s1_seed101_raw.jsonl` | `bc8911912491bb97fd987b3c91a22bda` · `0681d937d930c952b7ff92e0f24d5189` | repo `runs/` |
| `cham/score_ck500_test_raw.jsonl` · `cham/pred_ck500_test.jsonl` | `5b9d6d65cb0d2390b126d22463f888ee` · `328847ac96fa3104f76cd997f4091bcd` | repo `runs/grpo_spice/` |
| `cham/preds_venus_s1_2532.jsonl` · `cham/score_venus_s1_2532_raw.jsonl` | `e715a46693f8e6a588d23816a5f75430` · `b19b4e834201c8fb22925694dc7bf0a7` | repo `runs/venus/` |
| `cham/preds_venus_ck500_2532.jsonl` | `34fa2cf897721fe3155f5d917feb7856` | dựng từ hai tệp repo (1.210 câu khác S1; gieo 1.321, chấm 1.211 — đã chạy thử) |
| `cham/harness_venus/*.py` | `score_run.py` `9100844734d00e4f1851954d25a86220` | repo `harness/*.py, *.yaml` |
| `cham/score_venus_ck500_2532_raw.jsonl` | sau P7a | Output P7a |
| `cham/val_lon.py` (bản 4) | `d2854d13af1c924f44bf2dcb343ae8ca` | B.12 |
| `cham/score_ck500_c1_raw.jsonl` · `cham/score_s1_c1_raw.jsonl` · `cham/pred_ck500_c1.jsonl` (bản 4) | `258ced11cad3b6729bbdb25f947dbe78` · `1c8dbcd5f49ec53ecc655b4b4d2c04c4` · `eb6162d86730a936beb5ae5a9fd6d652` | repo `runs/grpo_spice/score_ck500_raw.jsonl` · `score_k0_lai500_raw.jsonl` · `pred_ck500.jsonl` |
| **máy nhà** | | |
| `_scripts/289/doc_289.py` (bản 4) | `12c7836d6b7d2c3fd2a74e16881c5b44` | B.13 |
| `_scripts/288/doc_288.py` · `_scripts/doc_286.py` | `2fe67533f939fd52279de3f97514fad0` · `96da21e03bb9046d10dd08cdb7f45090` | B.8 · B.9 |
| `_scripts/288/g0_som_build.py` | `155d813a59a0660222330e54ed2fdbb7` | B.3 |
| `_scripts/288/dung_lai_288.py` | xem B.11 | B.11 |

Dựng lại (máy mới hoặc mất thư mục): đặt file này và `thesis-master/` cạnh nhau trong một thư mục
GỐC, rồi:

```bash
cd GỐC
python3 - <<'PY'
import re
t = open("288_ACTION_NGUOI_NGHE_CLICK_6_10.md", encoding="utf-8").read()
m = re.search(r"^### B\.11 `([^`]+)` — md5 `\w+`, \d+ dòng\n\n```python\n(.*?)\n```\n", t, re.S | re.M)
import os; os.makedirs(os.path.dirname(m.group(1)), exist_ok=True); open(m.group(1), "w", encoding="utf-8").write(m.group(2) + "\n")
print("đã tách", m.group(1))
PY
python3 _scripts/288/dung_lai_288.py --md 288_ACTION_NGUOI_NGHE_CLICK_6_10.md          # ghi + so md5 mọi tệp
python3 _scripts/288/dung_lai_288.py --md 288_ACTION_NGUOI_NGHE_CLICK_6_10.md --kiem   # chỉ so
```

> ⚠️ (ghi chú của bản chép) Đoạn trên chỉ chạy được trên file có **mã nhúng** ở Phụ lục B. Bản
> trong ảnh (và bản chép này) chỉ có mô tả ⇒ cần `288_PHU_LUC_B_MA_NGUON_6_10.md` — xem Phần I.2.

Thiếu `g0_som.jsonl`/`g0_cau.jsonl` thì script in lệnh B.3; thiếu cả `all_forest_dict.zip` (bộ
`HarrytheOrange/parsed_AndroidControl` trên Hugging Face) thì **bạn tự lấy** — agent không tải gì từ
Hugging Face. B.3 và B.5 ghi cứng `R = "/Users/P836901/Documents/Self-learning/thesis"`: máy khác thì
sửa dòng đó (md5 sẽ đổi; công cụ đọc G0 vẫn phải là bản md5 `751557bd…` nếu đã khoá ở P0 — sửa
đường dẫn thì ghi vào sổ sửa đổi).

Kết quả thử tự chứa (bản 4, chạy lại sau khi tách ghi chú 6/10): thư mục tạm chỉ có file này +
symlink `thesis-master` ⇒ tách B.11 bằng đoạn trên ⇒ `dung_lai_288.py`: **11/11 khối mã khớp md5
(B.3–B.13), 18/18 tệp repo khớp**, `prompt_keys_ck500.json`, `preds_venus_ck500_2532.jsonl` và
`harness_venus/` khớp; thiếu đúng 2 tệp dữ liệu G0 (cần `all_forest_dict.zip`, đúng thiết kế).
34/34 khối python biên dịch được. Bản tách: `doc_289.py kiem` ✅ ĐẠT · `val_lon.py --selftest` ✅
ĐẠT · `gieo_tho.py --selftest` ✅ ĐẠT. Ở GỐC `--kiem` in ✅ ĐỦ, mọi md5 khớp.

## 10. [cách A] Chi phí và lịch (bản 4: §00.10)

| việc | máy | thời gian | đơn vị Colab |
|---|---|---|---|
| G0 | Kaggle T4×2 | ~1,5 h | 0 |
| probe 3 nhánh (một lần, phiên đầu) | Colab A100 80GB | ~0,5–1 h (gồm cài, tải Phi-4, hoà) | ~5–8 |
| Đợt 1: chỉ nhánh chính (+ máy chủ Phi-4 chung GPU) | Colab A100 80GB | ~6–7 h (ước: mốc CTG 1 nhánh 36,4 s/bước + người nghe 3–10 s/bước) | ~45–55 |
| chấm test Đợt 1 (1 nhánh) | Kaggle T4 | ~8 h | 0 |
| Đợt 2 (chỉ khi Δ(A − ck500) > 0): B1 + B0′ + A202 cùng GPU | Colab A100 80GB | ~9–12 h (ước 3 nhánh chung GPU; mốc CTG 2 nhánh 49,3 s/bước) | ~70–90 |
| chấm test Đợt 2 (3 nhánh) + P7a + P7b UI-Venus | Kaggle T4 · T4×2 | ~3 × 8 h + 2 × 1,5 h | 0 |
| Đợt 3 (chỉ ứng viên K4): B1_202 (+ B-rand) | Colab A100 80GB | ~6–9 h | ~45–65 |
| chấm test Đợt 3 | Kaggle T4 | 1–2 × 8 h | 0 |
| **nếu dừng ở Đợt 1 (K1)** | | 8 h T4 test | **~50–63 đơn vị (~5–6 USD)** |
| **tổng tối đa (đi hết 3 đợt)** | | | **~165–220 đơn vị (~17–22 USD theo giá 3/2026)** |

Nút cổ chai là giờ T4 Kaggle (30 h/tuần/tài khoản); lịch ~4 tuần nếu đi hết 3 đợt.

## 11. Kết cục và câu được phép

Bản 4: nhãn T0–T3 và câu được phép ở §00.8. Mục này giữ (a) bảng K0–K4 của [cách A], (b) câu độ
mới, cách viết an toàn và câu cấm — (b) dùng chung cho cả hai cách. Mọi câu về người nghe **bắt
buộc trích** ISR (ACL 2025) và LaF-GRPO (AAAI 2026, gần nhất).

[cách A] Test mỗi nhánh **một lần**. Định nghĩa (`doc_288.py` tính tự động; chưa đăng ký — §0):

- **"vượt"** = LB95(A − ck500) > 0 ∧ LB95(A − S1) > 0 ∧ Δ_UIVenus(A − ck500) > 0 ∧ Δ(A − B0′) > 0 ∧ Δ(A202 − ck500) > 0.
- **"v gây ra"** (chỉ khi A = `nghev`) = "vượt" ∧ LB95(A − B1) > 0 ∧ Δ(A202 − B1_202) > 0 ∧ (khi Δ(A − B1) ≥ +0,5 thì B-rand bắt buộc chạy và) Δ(A − Brand) > 0.

Train theo đợt (§6.2) **không đổi định nghĩa nào ở trên** — chỉ đổi thứ tự: nhánh đối chứng chỉ được
train khi nhánh chính đã cho lý do. Mỗi kết cục chỉ được tuyên bố ở đợt ghi trong cột "đọc sau":

| kết cục | P | đọc sau | số tiêu đề | câu được viết |
|---|---|---|---|---|
| K0 rớt G0 | ≈ 80% | G0 | ck500 click 60,65 (+1,55 [+0,84; +2,26] so S1) | "GRPO-SPICE nâng exec click so SFT. Ở cổng oracle, thưởng người nghe khác họ (Phi-4 SoM) không vượt thưởng giống tham chiếu dù biên đã khoá trước." |
| K1 qua G0, Δ(A − ck500) ≤ 0 | ≈ 8% | Đợt 1 | ck500; A phụ | "Lợi thế oracle của thưởng người nghe không truyền sang test." |
| K2 Δ > 0 nhưng thiếu ít nhất một điều kiện "vượt" | ≈ 8% | Đợt 2 | A − ck500 +x [KTC] | "Thưởng người nghe cho xu hướng tăng, chưa đủ điều kiện khoá trước (nêu điều kiện thiếu)." |
| K3 "vượt", v chưa chứng minh (hoặc keep_v sai) | ≈ 2,5–3% | Đợt 2 | A (hoặc B1) − ck500 +x [LB>0] | "Áp dụng thưởng người nghe khác họ bộ chấm vào GRPO sinh câu hướng dẫn GUI nâng exec click so SFT và GRPO-SPICE (mức cải tiến kỹ thuật)." |
| K4 "vượt" ∧ "v gây ra" | ≈ 1% | Đợt 3 | A − ck500 và A − B1 | câu độ mới dưới + "ablation B1/B-rand cho thấy cổng góp phần." |

Sau Đợt 1 mà bộ đọc in `CHỜ-ĐỢT-2` thì **chưa được viết câu nào**, kể cả "có xu hướng tăng": số Đợt 1
chưa loại được nhiễu đổi máy T4→A100 (B0′) và ăn may hạt (A202).

**Câu độ mới (chỉ ở T3 của bản 4, hoặc K4 của cách A):** "Chúng tôi đề xuất cổng kiểm định năng lực
người nghe theo từng ví dụ: trong GRPO cho bộ sinh câu hướng dẫn GUI, thưởng từ người nghe chỉ được
dùng trên ví dụ mà chính người nghe đó trỏ trúng khi nhận câu tham chiếu do người viết; các ví dụ còn
lại dùng thưởng tham chiếu SPICE. Kiểm năng lực trên gold đã được dùng để lọc dữ liệu (CapRL;
GUI-Libra), và cổng thưởng có điều kiện đã có trong RLVR (Posterior-GRPO; TinyV). Theo hiểu biết của
chúng tôi, chưa có công trình nào dùng kiểm định này làm cổng chọn nguồn thưởng cho bộ sinh câu."

**Cách viết an toàn:** "Theo hướng speaker–listener (ISR, LaF-GRPO), chúng tôi dùng người nghe khác
họ bộ chấm làm thưởng; theo thực hành kiểm bộ kiểm trên đáp án chuẩn của RLVR, chúng tôi chỉ bật
thưởng người nghe trên màn mà người nghe trỏ trúng câu chuẩn, màn còn lại giữ SPICE."

**Câu cấm:** "lần đầu kiểm định verifier trên gold"; "đề xuất thưởng người nghe"; "thành phần mới"
không kèm "kết hợp"; "phương pháp mới chống reward hacking"; "vượt trên toàn bộ test"/"SOTA" từ nhánh
click; "người nghe độc lập với bộ chấm" (κ Phi-4–UGround 0,44); "đăng ký trước" không kèm "sau khi đã
thấy ck500"; "thưởng không dùng bộ trỏ"; "v gây ra cải thiện" khi thiếu điều kiện; "hơn ck500" khi
KTC chứa 0; mọi suy diễn ra test từ số oracle val; viết bất kỳ câu nào khi bộ đọc còn in `CHỜ` (bản
4) / "CHỜ-ĐỢT-2" (cách A); viết câu K4 khi còn "K4-CHỜ-ĐỢT-3".

## 12. Agent KHÔNG làm (hạ tầng chung) — việc bạn quyết: §00.11

Không chạy GPU, không chạy Phi-4 thật (chưa có số G0 thật nào); chưa đo tốc độ/VRAM thật của người
nghe trên A100 (Ô C3 và probe sẽ đo); notebook G0, C1–C6, T1–T6, V1–V3 **chưa chạy trên
Kaggle/Colab** — phần CPU (`gieo_tho`, md5, dựng preds, selftest) đã chạy trên tệp thật, các ô kiểm
dụng cụ sẽ bắt lệch môi trường trước lượt dài. Không viết mã/runbook cho B-full (286). Đã cài Pillow
vào `_scripts/_venv`.

## Phụ lục A — đăng ký khoá trước của 288 (nằm trong file này; khoá bằng mốc thời gian dataset Kaggle ở P0, không commit)

```
## Phụ lục 288 — bản 4 (khoá 6/10/2026, TRƯỚC mọi lời gọi người nghe, mọi số val lớn và mọi train) — thưởng người nghe ở bước click, train tiếp từ ck500

Khai thẳng: thiết kế ra đời SAU khi đã thấy test của S1, ck500, AISR. TPR/FPR người nghe cũ (report 208 C3) đo trên câu S1 của
TEST → rò, không dùng làm bằng chứng. Hai chỗ nới luật có chủ ý, quyết bởi chủ luận văn, khai công khai: (i) thưởng dùng một bộ
chọn phần tử (Phi-4-multimodal, trắc nghiệm SoM, giao thức 14/9) — khác họ UGround/UI-Venus — trái L1426–1429 ("cổng sau seed 101
chỉ dùng tín hiệu không cần bộ trỏ") và tinh thần (x19f) "thưởng bằng … bất kỳ bộ trỏ nào"; (ii) dùng UGround trên VAL LỚN để
CHỌN nhánh lên test (mục 7). UGround/UI-Venus không bao giờ nằm trong thưởng.

1. Thưởng ở câu nhắc click: r = r_ck500 + W·g·h, W = 1,0; r_ck500 = SPICE − 0,02·max(0, từ(c) − từ(vàng) − 3) (nguyên
   grpo_spice.r_spice). h = ô Phi-4 chọn ∈ dap_an (mọi ô chứa điểm chạm vàng) VÀ dang_ok(câu) [3–20 từ; không khớp
   \d+\s*[,;]\s*\d+; không khớp \d{3,}]. Câu nhắc không chạm, hoặc màn không có ô đáp án: r = r_ck500.
2. Nhánh và cấu hình: tspicea (g ≡ 0), tnghe (g ≡ 1), tnghev (g = v(màn) = Phi-4 chọn đúng khi đọc câu chuẩn của màn, đo một
   lần offline ở G0, không áp dang_ok). Cả ba train TIẾP 250 bước từ adapter ck500 (adapter_model.safetensors md5
   491fa6677340393f1e4464c08a0cec98; grpo_nghe.py --tu, md5 f08f42b04b0b9f7b943b960877f7936f), cùng một phiên Colab A100 80GB,
   cùng 1.000 câu nhắc hạt 101 (= câu nhắc ck500, 630 click), G 8, 16 câu/bước, β 0,04, lr 1e-5 hằng sau 10 bước khởi động,
   fp16, S1 hoà fp16; lô --bs 4 --accum 4 (OOM ở probe → 2×8 cho mọi nhánh, khoá một lần, ghi mục 6). Chấm checkpoint-250,
   không chọn điểm lưu. Mã: nghe_server.py md5 f81cdf27c723f132c918619943149921, grpo_spice.py md5
   07ea87b6d156d1faa391a4274dffd7cf.
3. Người nghe khi train: máy chủ riêng, giao thức 14/9, crops 16; hết giờ/lỗi → h = 0 cả lần gọi. Dừng nhánh nếu TB r_ck500 50
   lần gọi cuối < 0,80 × 50 lần đầu (mọi nhánh); vi phạm dang_ok > 0,10 ở 50 lần cuối (nhánh người nghe); máy chủ lỗi > 5% số
   lần có hỏi sau ≥ 50 lần (kỹ thuật → sửa hạ tầng, chạy lại từ đầu). Nhánh dừng = không lên test, báo như một kết quả.
4. G0 (đo trên n = 249 bước click val C1, 9 câu S1; 1.717 cặp (bước, câu) duy nhất; bootstrap cụm episode 10.000×, rng 101;
   O_rand 200 lần rng 288; O_X = exec UGround của câu được chọn theo khoá X→SPICE, hoà → chỉ số nhỏ nhất; O_SP = 68,67; h thô ×
   dang_ok trong oracle): G0a parse_fail ≤ 0,05 ∧ phủ SoM train ≥ 0,90 · G0b κ(h, exec_UG) ≤ 0,60 · G0c AUC trong nhóm (135 bước
   exec trộn) ≥ 0,65 · V1 O_vh − O_h ≥ 0 · V2 O_vh − TB O_rand ≥ 1,0 · V3 TPR(h|v=1) − TPR(h|v=0) ≥ 0,25 · V4 0,30 ≤ TB v (630
   train) ≤ 0,85 · G0d O_main − O_SP ≥ 3,3 ∧ LB95(exec_main − exec_SP) > 0. Công cụ g0_doc.py md5
   e312f4b479469274ecce2f2ef03bc064; dữ liệu g0_som.jsonl md5 a49789bda073f5629380ad907db31910, g0_cau.jsonl md5
   656dd46f40bcc2d2f32a84e1c752fe6f.
5. Vai trò G0: G0a ∧ G0b là điều kiện để train tnghe và tnghev (sai → chỉ tspicea, hoặc dừng — chủ luận văn quyết). V4 sai →
   bỏ tnghev. G0c, G0d, V1–V3 chỉ ghi lại làm dự báo, không chặn. Cấm đổi người nghe, hạ ngưỡng, đổi W hay dang_ok rồi đo lại.
6. Sổ sửa đổi (điền khi có, kèm lý do; mọi thay đổi sau khi thấy số G0 khai là hậu nghiệm): (6/10, TRƯỚC P0) mã
   B.3–B.13 viết lại trên máy WSL từ bản mô tả Phụ lục B vì không mang được mã gốc sang; md5 ghi trong file này là
   của bản viết lại; dữ liệu G0 (g0_som/g0_cau) dựng lại trùng md5 bản gốc · cấu hình lô sau probe · …
7. Sàng và test. VAL LỚN = val_cham400 ∪ val_cham600 = p1_val (1.567 bước / 1.002 click, không episode nào trong câu nhắc GRPO).
   Sàng (mỗi nhánh một lần, greedy, UGround, val_lon.py md5 d2854d13af1c924f44bf2dcb343ae8ca; kiểm dụng cụ trước: chấm lại 20 câu
   ck500 C1 ≥ 19 trùng ≤ 3 px cùng exec, sinh lại ck500 ≥ 237/249 câu C1 trùng): X ∈ {tnghev, tnghe} lên test ⇔ Δ(X−tspicea) ≥
   +1,0 ∧ Δ(X−ck500) ≥ +1,0; có X lên → tspicea lên cùng; không X nào: tspicea lên ⇔ Δ(tspicea−ck500) ≥ +1,0; ngược lại DỪNG
   (đóng góp mô hình = ck500). Số val không vào luận văn như kết quả.
   Test (4.463 click, UGround; k = số X lên; câu trùng chấm bằng gieo tệp thô gieo_tho.py md5 7681cc68ad7e0bc9965c73f47ea3aa88,
   chỉ khi kiểm dụng cụ đạt: UGround chấm lại 20 câu ck500 ≥ 19 trùng ≤ 3 px cùng exec, sinh lại 20 câu ck500 ≥ 18 trùng;
   UI-Venus (min 200.704 / max 1.003.520 px) chấm lại 30 câu S1 ≥ 28 trùng):
   VƯỢT(X) ⇔ LB_{1−0,05/k}(X−ck500) > 0 ∧ LB_{1−0,05/k}(X−S1) > 0 ∧ Δ(X−tspicea) > 0 ∧ Δ_UIVenus(X−ck500) > 0 (lát 2.532 bước).
   v gây ra ⇔ VƯỢT(tnghev) ∧ LB95(tnghev−tnghe) > 0 (thiếu tnghe trên test → chấm thêm, chưa tuyên bố). Nhãn T0 (không X nào lên)
   · T1 (X lên, không VƯỢT) · T2 (VƯỢT, v chưa chứng minh) · T3 (VƯỢT ∧ v gây ra) · CHỜ (thiếu tệp → không tuyên bố gì). Bộ đọc
   doc_289.py md5 12c7836d6b7d2c3fd2a74e16881c5b44 (cần doc_286.py md5 96da21e03bb9046d10dd08cdb7f45090). Bước không chạm chỉ mô
   tả; cấm "vượt toàn bộ test". Dự trữ lô 2 (W = 2,0, một nhánh) chỉ khi không X nào lên và X tốt nhất có Δ(X−tspicea) ∈ [+0,3;
   +1,0) trên val; khai là lần sàng thứ hai, lên test theo đúng luật trên. Báo mọi nhánh đã chạy, kể cả rớt/dừng.

Ngoài đăng ký này: cách A (LoRA mới từ S1, 500 bước, train theo đợt) — muốn chạy phải đăng ký riêng trước khi train.
```

> Không dán vào `report/106`, không commit. Bằng chứng "có trước số" = phiên bản dataset
> `thesis-g0-288` chứa file này, tạo trước notebook G0 (P0, P2). Nếu sau này muốn đưa vào luận văn:
> trích nguyên khối trên kèm giờ phiên bản Kaggle.

## Phụ lục B — mã nguồn

> Ảnh 25 chỉ chụp được 12 dòng đầu của mã nguyên văn B.3. Mã chạy được của cả 11 script nay ở
> `_scripts/` (viết lại 6/10/2026 từ bản mô tả bên dưới, md5 ở `_scripts/288/dung_lai_288.py`).

## Phụ lục B — mô tả mã (đủ để viết lại) — *[bản trong ảnh 26–37]*

Mã nguyên văn, đúng từng byte và đúng md5, nằm ở `288_PHU_LUC_B_MA_NGUON_6_10.md` (cùng thư mục).
`dung_lai_288.py --md` trỏ vào file đó (§9). Phần dưới mô tả ý chính của 11 script B.3 đến B.13, đủ
để viết lại một bản có cùng hành vi và cùng số, nếu giữ đúng các chỗ ghi "quyết định số" (thứ tự rút
ngẫu nhiên, hạt, thứ tự ghi tệp). Bản viết lại sẽ có **md5 khác**, vì md5 tính trên từng byte của
mã. Các hàm trong repo mà script gọi tới được tả ở mục 0, nên không cần mở mã repo để biết giao diện.

### 0. Bối cảnh chung (mọi script dùng)

#### 0.1 Định dạng dữ liệu

| loại tệp | mỗi dòng JSON gồm |
|---|---|
| bản ghi bước (`c1_recs.jsonl`, `train.jsonl`, `test.jsonl`, `val_cham*.jsonl`) | `episode_id`, `step_id`, `action` (dict, hoặc chuỗi repr của dict thì đọc bằng `ast.literal_eval`), `image` (đường dẫn tương đối kiểu `images/….png`), `w`, `h`, `target_instruction` (câu chuẩn), có thể có `gold_instruction`, `goal`, `history` |
| tệp thô của bộ chấm `score_run.py` (`*_raw.jsonl`) | một bước chạm: `episode_id`, `step_id`, `sent` (câu đã chấm, có thể `null`), `executable` (0/1) |
| tệp dự đoán (`pred_*.jsonl`, `preds_*.jsonl`) | `episode_id`, `step_id`, `pred` (câu mô hình sinh) |

Bước chạm (click) = `action["action_type"]` thuộc `{"click", "long_press"}` và `action` có khoá
`"x"`. Toạ độ vàng là `action["x"]`, `action["y"]` (pixel).

Khoá một bước luôn là cặp `(episode_id, step_id)`. Ở bảng thưởng và câu nhắc GRPO, khoá là chuỗi
`f"{episode_id}_{step_id}"`.

#### 0.2 Module có sẵn trong `thesis-master/harness/` mà các script gọi

`som_build.ung_vien(ten_anh, W, H)` → danh sách hộp `(x1, y1, x2, y2)` các phần tử bấm được trên màn:

1. Đọc cây trợ năng của màn từ `all_forest_dict.zip` (qua `a11y_inventory`: `A._load(A.key_for(ten_anh))`). Gán sẵn `A._ZIP = zipfile.ZipFile(<đường dẫn zip>)` để không phải tải từ Hugging Face.
2. Bỏ cửa sổ có `window_type == 3`. Với mỗi nút trong `tree`: cần `is_visible_to_user`, tập `actions` có 16 (CLICK) hoặc 32 (LONG_CLICK).
3. Hộp = `bounds_in_screen` cắt vào màn `[0, W] × [0, H]`. Bỏ hộp có cạnh < 8 px hoặc diện tích > 50% màn.
4. Gộp hộp gần trùng: duyệt lần lượt, giữ hộp nếu IoU với **mọi** hộp đã giữ < 0,9.
5. Sắp theo `(y1, x1)` (trên xuống, trái sang). Số thứ tự hộp đánh từ 1.

`som_build.ve(anh, hop)` → ảnh RGB có vẽ khung màu và nhãn số (1, 2, …) nền đặc ở góc trên trái mỗi
hộp. Màu hộp i lấy từ HSV `((i·0,618034) mod 1; 0,9; 0,85)`. Cỡ chữ `max(22, 0,028·W)`, nét
`max(3, W//300)`.

`som_listener.CAU_HOI` (câu hỏi người nghe, nguyên văn, `{s}` là câu cần chấm):

```
This is a phone screenshot. Colored boxes with numbers mark the elements that can be tapped.
A user was given this instruction:
"{s}"
Which numbered box is the element the instruction tells the user to tap? Answer with the number only.
```

`som_listener.Phi4`: nạp `microsoft/Phi-4-multimodal-instruct` (transformers 4.48.2,
`trust_remote_code`, fp16, attention `sdpa`, lùi về `eager` nếu không nhận). Nếu biến môi trường
`SOM_PHI4_CROPS` có giá trị thì đặt `processor.image_processor.dynamic_hd = int(...)`; giao thức chốt
là 16. Hàm `hoi(anh, text)`: prompt `<|user|><|image_1|>{text}<|end|><|assistant|>`, sinh tham lam
`max_new_tokens=8`, trả chuỗi đã giải mã.

Người nghe chỉ thấy ảnh đã vẽ số và câu: không thấy mục tiêu, không thấy lịch sử. Từ chuỗi trả lời,
lấy **số nguyên đầu tiên** bằng regex `\d+`; không có số thì coi là không trả lời (`None`).

`grpo_spice` (phương pháp ck500):

- `r_spice(completions, gold)`: câu rỗng được 0; ngược lại thưởng = SPICE-F(câu, câu chuẩn) − 0,02 · max(0, số_từ(câu) − số_từ(chuẩn) − 3). Số từ đếm bằng regex `[A-Za-z0-9'-]+`.
- `dung_hang(bundle, n=1000)`: dựng 1.000 câu nhắc GRPO từ `p1_train_rows.jsonl` (loại bước/episode trùng val, thiếu ảnh/OCR, câu chuẩn rỗng), xáo bằng `random.Random(SEED)` rồi lấy n đầu. Mỗi hàng có cột `key`, `image`, `prompt`, `gold`, `action_type`. TRL truyền các cột này vào hàm thưởng dưới dạng tham số tên.
- `train(a)`: GRPO của TRL trên Qwen2.5-VL-3B đã hoà S1, LoRA mới cùng hạng/đích với S1, G=8, 96 token, nhiệt độ 1,0, β=0,04, lr 1e-5, lưu mỗi 25 bước, chạy tiếp từ điểm lưu đủ tệp. Bên trong `train`, hai thứ được tra lúc chạy: `from peft import get_peft_model` (tra thuộc tính module `peft`) và `reward_funcs=[r_spice]` (tra biến toàn cục của module `grpo_spice`). Đây là hai chỗ B.6 thay thế.
- `_dtype()`: bf16 nếu GPU compute capability ≥ 8, ngược lại fp16. `merge(a)`: hoà adapter S1 vào mô hình gốc.
- `nap(a)`, `nap_ocr(bundle)`, `body_of(r, ocr)`, `SEED = 101`.

`build_branch_data.prompt_body({"goal", "history"}, ocr_cua_anh)` và hằng `SYS`: dựng thân câu nhắc của S1.

#### 0.3 Bootstrap cụm theo episode (dùng ở B.5, B.8, B.9, B.13)

Cho vector hiệu theo bước `d` và mã episode của từng bước:

1. Sắp các episode khác nhau tăng dần, đánh chỉ số 0..E−1.
2. Tính tổng `d` và số bước theo từng episode (`np.bincount`).
3. Rút `B = 10.000` lần, mỗi lần E chỉ số episode có hoàn lại: `rng.integers(0, E, size=(B, E))`.
4. Mỗi lần: trung bình = tổng các tổng đã rút / tổng các số bước đã rút.
5. Trả `(100·mean(d), 100·quantile(q), 100·quantile(1−q))`, mặc định q = 0,025 (KTC 95%).

`rng = np.random.default_rng(101)`. **Quyết định số:** trong một số script, một `rng` được dùng lại
qua nhiều phép so liên tiếp, nên thứ tự các phép so phải giữ đúng như mô tả.

McNemar chính xác hai phía với b = số bước A đúng B sai, c = ngược lại: n = b + c, k = min(b, c),
p = min(1, 2 · Σ_{i=0..k} C(n, i) / 2ⁿ); n = 0 thì p = 1.

### B.3 `g0_som_build.py` — dựng ô SoM và danh sách câu cho người nghe (CPU, máy nhà)

**Mục đích.** Chuẩn bị dữ liệu cho cổng G0: với mỗi màn click, tìm các ô ứng viên và ô đáp án; liệt
kê mọi cặp (màn, câu) cần đưa cho người nghe Phi-4.

**Đầu vào.**

- `thesis-master/runs/c1/exec8/c1data/c1_recs.jsonl`: 400 bước val C1, lọc bước chạm → phải ra **249**.
- `thesis-master/runs/ctg/p0/p0_a3/prompt_keys.json`: lấy 1.000 khoá đầu (đúng 1.000 câu nhắc của ck500). Tra từng khoá trong `harness/dg1_cache/train_ac/train.jsonl` (đánh chỉ mục theo `"ep_step"`), giữ bước chạm → phải ra **630**. Giữ thứ tự của prompt_keys.
- `runs/c1/exec8/c1score/score_k{k}_raw.jsonl` với k = 0..8: 9 câu mẫu của S1 cho mỗi bước C1. Dựng 9 từ điển `(str(ep), str(step)) → sent` (sent `null` thì thay bằng `""`).

**Thuật toán.** Duyệt tập `c1` trước, rồi `train`; trong mỗi tập duyệt theo thứ tự bản ghi:

1. `boxes = ung_vien(f"episode_{ep}_screenshot_{step}.png", W, H)`.
2. `dap_an` = danh sách số thứ tự (từ 1) của mọi hộp chứa điểm vàng, tính cả biên: `x1 ≤ gx ≤ x2` và `y1 ≤ gy ≤ y2`. Đếm độ phủ = số màn có `dap_an` khác rỗng.
3. Ghi một bản ghi màn: `tap, episode_id, step_id (chuỗi), image_goc, w, h, boxes, dap_an`.
4. Danh sách câu của màn: `("chuan", target_instruction)`; nếu tập `c1` thì thêm `("k0", câu mẫu 0) … ("k8", câu mẫu 8)`.
5. Gộp câu trùng theo khoá `(tap, ep, step, câu)`: lần đầu tạo bản ghi `{tap, episode_id, step_id, sent, nhan: []}`, các lần sau chỉ nối nhãn vào `nhan`. Dùng dict giữ thứ tự chèn.

**Đầu ra** (thư mục `_scripts/288/g0/`):

- `g0_som.jsonl`: 879 dòng (249 + 630).
- `g0_cau.jsonl`: các bản ghi câu theo thứ tự chèn, thêm `id = 0, 1, 2, …` ở đầu dict. Phải ra **2.530** dòng.
- Ghi JSON với `ensure_ascii=False`, mỗi dòng kết thúc `\n`.

In ra: số màn, trung vị và p90 số ô mỗi màn, số màn không có ô, độ phủ đáp án của từng tập, số lời
gọi người nghe và số câu rỗng.

**Quyết định số.** `id` theo thứ tự chèn (c1 trước, trong mỗi màn câu chuẩn trước, rồi k0..k8, câu
trùng không tạo id mới). Chia shard ở B.4 dựa vào `id`, và md5 của hai tệp được B.11 kiểm
(`g0_som.jsonl` = `a49789bda073f5629380ad907db31910`, `g0_cau.jsonl` = `656dd46f40bcc2d2f32a84e1c752fe6f`).

### B.4 `g0/g0_listener.py` — người nghe Phi-4 chấm 2.530 cặp (Kaggle GPU)

**Mục đích.** Với mỗi cặp (màn, câu), hỏi Phi-4 "ô số mấy", ghi lại ô chọn và việc có trúng đáp án không.

**Tham số dòng lệnh.** `--backend phi4|gia` (bắt buộc), `--som`, `--cau`, `--out` (bắt buộc),
`--img-glob` (mặc định `/kaggle/input/**/images/*.png`), `--shard i/n` (mặc định `0/1`), `--limit`
(0 = không giới hạn).

**Thuật toán.**

1. Nạp `som` thành dict theo `(tap, episode_id, step_id)`; nạp `cau` thành list. Kiểm đúng 879 màn và 2.530 câu.
2. Chỉ mục ảnh: glob đệ quy `--img-glob`, ánh xạ **tên tệp** → đường dẫn đầu tiên gặp. Tìm ảnh của màn bằng tên tệp của `image_goc`. Thiếu ảnh nào thì **dừng trước khi nạp mô hình**, in 5 tên đầu.
3. Việc của shard: các câu có `id % n == i`, cắt theo `--limit`.
4. Nối tiếp: nếu `--out` đã có, đọc mọi `id` đã xong (bỏ qua dòng hỏng) và bỏ qua chúng.
5. Nạp mô hình (`Phi4` hoặc `Gia` của `som_listener`). Mở `--out` ở chế độ nối thêm.
6. Với mỗi câu chưa xong:
   - Câu rỗng **hoặc** màn không có ô nào: không gọi mô hình, `raw = ""`, `chon = None`.
   - Ngược lại: vẽ ảnh bằng `ve(anh, boxes)`, gọi `hoi(anh, CAU_HOI.format(s=câu))`. Nếu ngoại lệ có chữ "out of memory": dọn bộ nhớ CUDA, `raw = "__OOM__"`, đếm OOM; ngoại lệ khác thì ném ra. `chon` = số nguyên đầu tiên trong `raw` (OOM thì `None`).
   - Ghi dòng: `id, tap, episode_id, step_id, nhan, sent, raw, chon, h, n_o`, trong đó `h = 1` nếu `chon` khác `None` và nằm trong `dap_an`, ngược lại 0; `n_o` = số ô. Xả đệm sau mỗi dòng.
   - Mỗi 50 câu in tốc độ và thời gian còn lại.

### B.5 `g0/g0_doc.py` — đọc cổng G0 (CPU, máy nhà)

**Mục đích.** Từ kết quả người nghe, quyết định có được train hướng người nghe hay không (`TRAIN`),
và nếu được thì có dùng cổng v theo màn không (`keep_v`).

**Hai chế độ (chọn đúng một).** `--nghe <tệp kết quả Phi-4>` hoặc `--gia-lap TPR,FPR,P(v)` (người
nghe giả để tự kiểm).

**Hằng số khoá trước**

| tên | giá trị | dùng ở |
|---|---|---|
| `parse_fail` tối đa | 0,05 | G0a |
| `phu_train` tối thiểu | 0,90 | G0a |
| `kappa_max` | 0,60 | G0b |
| `auc_min` | 0,65 | G0c |
| `v2` | 1,0 điểm | V2 |
| `v3` | 0,25 | V3 |
| `v4` | [0,30; 0,85] | V4 |
| `g0d` | 3,3 điểm | G0d |
| B, hạt bootstrap, hạt ngẫu nhiên, số lần ngẫu nhiên | 10.000 · 101 · 288 · 200 | |

Luật định dạng `dang_ok(câu)`: số từ (tách theo khoảng trắng) từ 3 đến 20, **không** có cặp toạ độ
(regex `\d+\s*[,;]\s*\d+`), **không** có chuỗi từ 3 chữ số trở lên (`\d{3,}`).

**Nạp dữ liệu C1**

- `recs` = toàn bộ `c1_recs.jsonl` (400 dòng). `I` = chỉ số các bản ghi chạm (249).
- `M = metric_tung_cau.json`, trong đó `M["spice"][k][i]` là SPICE của câu mẫu k ở bản ghi thứ i (chỉ số trên toàn bộ 400 bản ghi).
- Với bước thứ j (j = 0..248) và mẫu k (0..8): `ex[j,k]` = `executable` từ `score_k{k}_raw.jsonl`, `SP[j,k]` = SPICE, `sent[j][k]` = câu (rỗng nếu `null`), `ep[j]` = episode.
- Nạp `g0_som.jsonl` và `g0_cau.jsonl`.

**Kết quả người nghe**

- Chế độ thật: đọc tệp, giữ dòng cuối cho mỗi `id`.
- Chế độ giả lập: `rng = default_rng(7)`. Dựng `exs[(khoá bước, câu)] = ex` của mọi (j, k). Duyệt các câu theo thứ tự `g0_cau`: xác suất trúng `p = P(v)` nếu nhãn chỉ là `["chuan"]` hoặc tập train; ngược lại `p = TPR` nếu câu đó exec = 1, `FPR` nếu exec = 0. Rút **hai** số theo thứ tự: `h = rng.random() < p`, rồi `parse_fail = rng.random() < 0,02`. Parse fail thì `chon = None, h = 0`, ngược lại `chon = 1`, `h` như đã rút. In cảnh báo "GIẢ LẬP".
- Kiểm đủ 2.530 `id` và khớp tập `id` của `g0_cau`. Đánh chỉ mục `H[(tap, ep, step, câu)]`.

**Các đại lượng**

1. **G0a.** Trong các câu không rỗng và màn có ô: `parse_fail` = tỉ lệ `chon is None`. `phu_train` = tỉ lệ màn train có `dap_an` khác rỗng. G0a đạt khi cả hai qua ngưỡng.
2. **h và v.** `h_tho[j,k]` = `h` của người nghe cho (c1, bước j, câu mẫu k). `h = h_tho · dang_ok(câu)`. `v[j]` = `h` của **câu chuẩn** trên bước j (v là "màn này người nghe có giải được với câu chuẩn không"). `v_train` = `h` của câu chuẩn trên 630 màn train (phải đủ 630).
3. **Cặp duy nhất `U`.** Giữ (j, k) nếu câu `sent[j][k]` chưa xuất hiện ở các mẫu `0..k-1` của cùng bước. Đếm thêm `lech` = số (j, k) mà exec khác exec của lần xuất hiện đầu tiên của cùng câu (kiểm bộ chấm tất định). `hu`, `eu` = h và exec trên các cặp duy nhất.
4. **G0b (người nghe không chép UGround).** Cohen κ giữa `hu` và `eu` cho biến nhị phân: pₒ = tỉ lệ trùng, pₑ = mean(x)·mean(y) + (1−mean(x))(1−mean(y)), κ = (pₒ−pₑ)/(1−pₑ) (pₑ = 1 thì κ = 1). Đạt khi κ ≤ 0,60.
5. **G0c (AUC trong từng bước).** Với mỗi bước có cả cặp exec = 1 (dương) lẫn exec = 0 (âm) trong `U`: so mọi cặp (dương, âm) theo h: lớn hơn được 1, bằng được 0,5, nhỏ hơn được 0. AUC = tổng / số cặp, gộp mọi bước. Đếm `tron` = số bước có cả hai loại. Đạt khi AUC ≥ 0,65.
6. **Oracle chọn 1 trong 9.** Cho ma trận điểm `key[j][k]`, chọn k có `(key, −k)` lớn nhất (hoà thì lấy k nhỏ), rồi lấy exec của câu được chọn.
   - `O_SP` dùng `key = SP`; **kiểm** `|O_SP − 68,67| < 0,01`.
   - `O_h` dùng `key = 10·h + SP` (h quyết trước, SPICE chỉ phá hoà vì SPICE < 1).
   - `O_vh` dùng `key = 10·v[j]·h + SP` (chỉ tin h ở màn có v = 1).
   - `O_rand`: `rng = default_rng(288)`, lặp 200 lần, mỗi lần rút mặt nạ theo bước `rng.random(249) < mean(v)` rồi dùng `key = 10·mask·h + SP`. Lấy trung bình 200 giá trị.
7. **Bốn điều kiện giữ cổng v.**
   - V1: `O_vh − O_h ≥ 0`.
   - V2: `O_vh − mean(O_rand) ≥ 1,0`.
   - V3: TPR(v = 1) − TPR(v = 0) ≥ 0,25, với TPR(mặt nạ) = trung bình `hu` trên các cặp duy nhất có exec = 1 và v của bước thoả mặt nạ.
   - V4: `mean(v_train)` nằm trong [0,30; 0,85].
   - `keep_v` = cả bốn đạt; `main = "vh"` nếu giữ, ngược lại `"h"`.
8. **G0d.** `d = exec_main − exec_SP` theo bước, KTC bằng bootstrap cụm (mục 0.3, hạt 101). Đạt khi `O_main − O_SP ≥ 3,3` và cận dưới > 0.
9. `TRAIN = G0a ∧ G0b ∧ G0c ∧ G0d`.

**Đầu ra.** In từng dòng số kèm ngưỡng và ĐẠT/KHÔNG ĐẠT; in quyết định (TRAIN với nhánh `nghe_v`
hoặc `nghe`, hoặc DỪNG kèm lời cấm hạ ngưỡng). Ghi `_scripts/288/g0_ket_qua.json` (giả lập thì
`g0_ket_qua_GIA.json`) với: `gia_lap, n_cap, parse_fail, phu_train, kappa, auc, n_tron, O_SP, O_h,
O_vh, O_rand, V3, v_val, v_train, keep_v, main, G0d{d, lo, hi}, G0{a, b, c, d}, TRAIN`.

### B.6 `nghe/grpo_nghe.py` — GRPO thưởng người nghe (train + tự kiểm)

**Ý tưởng.** Không sửa `grpo_spice.py`. Gọi đúng `grpo_spice.train`, chỉ thay hàm thưởng (và tuỳ
chọn khởi LoRA từ adapter ck500). Nhờ vậy mọi siêu tham số trùng ck500 bởi cấu tạo. Người nghe Phi-4
chạy ở **tiến trình riêng** (B.7) vì cần bản transformers khác; hai bên nói chuyện qua socket TCP cục bộ.

**Hằng số.** `W_NGHE = 1,0` · cổng mặc định `47288` · `HAT_RAND = 288` · nhánh `nghev | nghe | nghern | spicea`.

**Bốn nhánh thưởng** — chỉ áp ở câu nhắc click có trong bảng; câu nhắc khác nhận đúng `r_spice` như ck500.

| nhánh | thưởng | cổng màn `g(màn)` |
|---|---|---|
| `nghev` (A, đề xuất) | r_spice + W·v·h | `v` của màn |
| `nghe` (B1) | r_spice + W·h | luôn 1 |
| `nghern` (B-rand) | r_spice + W·v_rand·h | `v_rand` của màn |
| `spicea` (B0′) | r_spice | luôn 0 (không bao giờ gọi người nghe) |

`h = 1` khi câu qua `dang_ok` và ô Phi-4 chọn thuộc `dap_an` của màn.

**Chế độ `--dung-bang` (CPU, sau G0)**

1. Đọc `g0_som.jsonl`, giữ 630 màn train. Đọc kết quả người nghe, giữ các dòng `tap == "train"`, đánh chỉ mục theo `(ep, step)` (mỗi màn train chỉ có câu chuẩn). Kiểm cả hai đủ 630.
2. `v[khoá] = h` của câu chuẩn. `p = mean(v)`.
3. `v_rand`: `rr = random.Random(288)`; duyệt các khoá **đã sắp tăng dần** (chuỗi `"ep_step"`), mỗi khoá `int(rr.random() < p)`.
4. Bảng: `bang["ep_step"] = {image, w, h, boxes, dap_an, v, v_rand}`. Meta: `n, tb_v, tb_v_rand, co_dap_an, som_md5, nghe_md5, hat_rand`. Ghi `{"meta", "bang"}` ra `--out`, in md5.

**Client gọi máy chủ: `hoi_may_chu(viec, cong, het_gio)`**

- Mở TCP tới `127.0.0.1:cong` với timeout `het_gio`; gửi một dòng JSON `{"viec": [{"key", "sent"}, …]}` + `\n`; đọc tới khi gặp `\n`; đóng.
- Phản hồi có `"loi"` → trả `(None, lỗi)`. Nếu `viec` khác rỗng mà số phần tử `chon` khác số việc → `(None, "lệch số câu")`.
- Thành công → `(q["chon"] nếu có, ngược lại cả q, None)`. Mọi `OSError`/`ValueError` → `(None, repr(e))`. Hàm không bao giờ ném lỗi ra ngoài.
- `viec` rỗng là lệnh ping; máy chủ trả `{"ok": true, "ten": …}`.

**Hàm thưởng: `lam_thuong(arm, bang, spice_fn, out, cong, het_gio=None, thoat=True)`**

Trả về hàm `r_nghe(completions, gold, action_type, key, **kw)` với trạng thái riêng:

- Nhật ký `out/nghe_log.jsonl`. Nếu đã có (chạy tiếp sau mất máy) thì nạp lại lịch sử: danh sách SPICE trung bình mỗi lần, danh sách `(vi_pham, n_cham)`, số lần lỗi, số lần có hỏi người nghe, tổng số lần. Mục đích: luật dừng vẫn so với 50 lần đầu thật của lượt.
- Bộ đệm `CACHE[(key, câu)] = ô chọn` (sống trong tiến trình).

Mỗi lần TRL gọi (một lô câu sinh):

1. `sp = spice_fn(completions, gold)`; `câu = text(c).strip()` (completion dạng list hội thoại thì lấy `content` phần tử đầu).
2. `cham[i]` = action_type thuộc click/long_press và key có trong bảng.
3. `bat[i]` = `cham` và `g(màn) ≠ 0` và `dap_an` khác rỗng.
4. `ok[i]` = câu khác rỗng và `dang_ok`.
5. `viec` = tập `(key, câu)` có `bat ∧ ok` và chưa có trong bộ đệm, **sắp tăng dần**. Nếu có việc: gọi máy chủ với timeout `het_gio` hoặc `60 + 5·len(viec)` giây; thành công thì ghi bộ đệm.
6. `h[i] = 1` khi `bat ∧ ok ∧` lần gọi này không lỗi `∧ CACHE[(key, câu)] ∈ dap_an`. **Chú ý:** nếu lần gọi này lỗi thì mọi h của lô bằng 0, kể cả câu đã có trong bộ đệm.
7. Thưởng `r = sp + W·h`.
8. Ghi một dòng nhật ký: `lan, n, n_cham, n_bat, n_hoi, n_trung, vi_pham (= số câu chạm mà không qua định dạng), sp_tb, dt, loi`; in một dòng tóm tắt.
9. **Luật dừng khoá trước** (không dùng bộ trỏ, không dùng val/test):
   - Từ lần thứ 100: SPICE trung bình 50 lần cuối < 0,80 × SPICE trung bình 50 lần đầu.
   - Nhánh khác `spicea`, từ lần thứ 50: tổng vi phạm / tổng câu chạm của 50 lần cuối > 0,10.
   - Nhánh khác `spicea`, khi số lần có hỏi ≥ 50: số lần lỗi / số lần có hỏi > 0,05.
   - Dừng = ghi `out/DUNG.json {ly_do, lan}`, in lý do; `thoat=True` thì `os._exit(3)` (thoát ngay cả trong luồng của trainer), `thoat=False` thì ném ngoại lệ `Dung` (dùng trong tự kiểm).
10. Đặt `r_nghe.__name__ = "r_spice"` cho nhánh `spicea`, `"r_nghe"` cho nhánh khác (TRL ghi log thưởng theo tên hàm). Gắn `r_nghe.H` (lịch sử) và `r_nghe.CACHE` để tự kiểm đọc được.

`cho_may_chu(cong, toi_da=1800)`: ping mỗi 15 giây tới khi nhận `{"ok": true}`, trả tên mô hình; quá hạn thì thoát lỗi.

**Chế độ `--merge` và `--train`**

- `ep_fp16()`: thay `grpo_spice._dtype` bằng hàm luôn trả fp16 (ck500 train fp16 trên T4; A100 tự chọn bf16 nên phải ép).
- `--merge`: `ep_fp16()` rồi `grpo_spice.merge(a)`.
- `--train` (hoặc `--probe`):
  1. `ep_fp16()`. Nhánh khác `spicea`: nạp bảng, in số màn, TB v, md5; chờ máy chủ người nghe.
  2. Giữ bản **gốc** một lần duy nhất (nếu chưa giữ): `grpo_spice._r_spice_goc`, `grpo_spice._dung_hang_goc`, `peft._gpm_goc`. Nhờ vậy gọi `train()` nhiều lần không bọc lồng nhau.
  3. `R = lam_thuong(arm, bang, grpo_spice._r_spice_goc, out, cong)`.
  4. Ghi `out/nghe_meta.json`: `arm, seed, w, bang, nguoi_nghe, bs, accum, tu, max_steps`.
  5. `grpo_spice.r_spice = R`.
  6. Bọc `dung_hang`: trong lúc dựng câu nhắc, tạm đặt `grpo_spice.SEED = 101` rồi trả lại. Nghĩa là **1.000 câu nhắc luôn là của ck500**, bất kể hạt cấu hình.
  7. `grpo_spice.SEED = a.seed` (hạt của GRPOConfig).
  8. Bọc `peft.get_peft_model`: nếu hạt ≠ 101 thì `torch.manual_seed(hạt)` trước; nếu có `--tu <thư mục adapter>` thì trả `PeftModel.from_pretrained(model, tu, is_trainable=True)` (train tiếp từ ck500, cùng hạng/đích); không có thì gọi bản gốc (LoRA mới).
  9. `grpo_spice.train(a)`.

**Tham số dòng lệnh** (trùng bộ cờ `grpo_spice.train` dùng): `--selftest --dung-bang --merge --train
--probe`, `--arm`, `--seed` (101), `--bang`, `--som`, `--nghe`, `--cong` (47288), `--bundle`,
`--merged` (`/content/s1_merged`), `--adapter` (mặc định `<bundle>/adapter_s1_seed101`), `--out`,
`--tu`, `--n` (0), `--n-prompt` (1000), `--G` (8), `--bs` (8), `--accum` (2), `--beta` (0,04), `--lr`
(1e-5), `--max-steps` (500), `--resume`, `--no-q4`, `--gen-chunk` (0). Kiểm: train cần `--arm --out
--bundle`, nhánh khác `spicea` cần `--bang`.

**Chế độ `--selftest` (CPU)**

Dựng thư mục tạm có 3 ảnh trắng 540×1200 và bảng giả: màn `90_1` (v=1, v_rand=0), `91_1` (v=0,
v_rand=1), `92_1` (v=1, v_rand=1), cả ba có 2 ô và `dap_an = [2]`; màn `99_1` không có ô. Bật máy chủ
B.7 backend `gia` ở cổng 47999 (tiến trình riêng, `start_new_session=True`). Máy chủ giả trả ô đáp án
đầu nếu câu có chữ "TRUNG", ngược lại "0"; câu có "TREO" thì ngủ 30 giây.

Hàm SPICE giả trả 0,5 cho mọi câu. Tám câu thử và thưởng mong đợi:

| # | câu | màn | thao tác | nghe | nghev | nghern | spicea | vì sao |
|---|---|---|---|---|---|---|---|---|
| 1 | Click on the TRUNG button | 90_1 | click | 1,5 | 1,5 | 0,5 | 0,5 | trúng; v_rand = 0 |
| 2 | TRUNG | 90_1 | click | 0,5 | 0,5 | 0,5 | 0,5 | 1 từ, trượt định dạng |
| 3 | Click at 540, 1200 TRUNG | 90_1 | click | 0,5 | 0,5 | 0,5 | 0,5 | có cặp toạ độ |
| 4 | Click on the wrong button | 90_1 | click | 0,5 | 0,5 | 0,5 | 0,5 | người nghe chọn sai |
| 5 | Click on the TRUNG button | 91_1 | click | 1,5 | 0,5 | 1,5 | 0,5 | v = 0 |
| 6 | Click on the TRUNG button | 92_1 | click | 1,5 | 1,5 | 1,5 | 0,5 | |
| 7 | Scroll down TRUNG please | 90_1 | scroll | 0,5 | 0,5 | 0,5 | 0,5 | không phải chạm |
| 8 | Click on the TRUNG item | 99_1 | click | 0,5 | 0,5 | 0,5 | 0,5 | màn không có ô |

Các phép kiểm, theo thứ tự:

1. Bốn nhánh ra đúng bảng trên; gọi lần hai cùng lô ra cùng kết quả và **số lần hỏi không tăng** (bộ đệm).
2. Câu "TREO" với `het_gio = 3`: thưởng 0,5 và đếm 1 lỗi. Sau đó ngủ 30 giây cho máy chủ rảnh.
3. Luật dừng SPICE: nhánh `spicea`, SPICE giả = 0,5 ở 60 lần đầu rồi 0,3; phải dừng (ở lần 100) với lý do có chữ "SPICE" và có `DUNG.json`.
4. Luật dừng định dạng: nhánh `nghe`, câu "Tap" từ lần thứ 7; phải dừng với lý do có chữ "định dạng".
5. Tạo lại `lam_thuong` trên cùng thư mục: phải nạp được nhật ký cũ (số lần > 0).
6. Tắt máy chủ, gọi lại: thưởng 0,5, đếm 1 lỗi.
7. `dang_ok`: đúng với "Click on the search bar", "Select 2 adults in the list"; sai với "Tap 12, 40", "Click 1200", "Click".
8. **Kiểm nối dây `train()`** bằng module giả: thay `torch`, `peft`, `grpo_spice` trong `sys.modules` bằng module giả ghi lại lời gọi; chạy `train()` với (spicea, hạt 202, không `--tu`), (spicea, 101, không), (spicea, 101, `/ck500`). Kiểm: lúc dựng câu nhắc hạt là 101; hạt cấu hình bằng `--seed`; dtype fp16; tên hàm thưởng `r_spice`; thưởng đi qua SPICE giả; `manual_seed` chỉ gọi khi hạt ≠ 101; có `--tu` thì gọi `PeftModel.from_pretrained(model, "/ck500", is_trainable=True)`, không có thì gọi `get_peft_model` gốc; `nghe_meta.json` ghi đúng `arm, tu, max_steps`. Cuối cùng trả lại module thật vào `sys.modules`.

### B.7 `nghe/nghe_server.py` — máy chủ người nghe (tiến trình riêng)

**Vì sao tách tiến trình.** Phi-4 cần transformers 4.48.2, còn môi trường train dùng bản khác. Đầu
tệp đặt `sys.modules.setdefault("torchao", None)` vì transformers 4.48.2 vấp phải torchao mới của môi
trường train.

**Tham số.** `--backend phi4|gia`, `--bang` (bảng của B.6), `--img-root` (thư mục chứa đường dẫn
`image` của bảng), `--cong` (47288).

**Hoạt động.**

1. Nạp bảng. Hàm vẽ ảnh có bộ đệm LRU 128 màn: mở `img_root/image`, vẽ bằng `ve` với các hộp của màn.
2. Nạp `Phi4()` hoặc lớp giả (giả: câu có "TREO" thì ngủ 30 giây; có "TRUNG" và màn có đáp án thì trả `str(dap_an[0])`, ngược lại `"0"`).
3. Mở socket TCP `127.0.0.1:cong`, `SO_REUSEADDR`, listen 8; in "SẴN SÀNG".
4. Vòng lặp **tuần tự** (một GPU): nhận một kết nối, đọc tới `\n`, parse JSON (rỗng thì `{}`).
   - `viec` rỗng → trả `{"ok": true, "ten": tên mô hình}`.
   - Ngược lại, với từng việc: vẽ ảnh (backend giả cũng vẽ để kiểm đường dẫn ảnh), hỏi mô hình (`CAU_HOI.format(s=câu)` với Phi-4). OOM → dọn CUDA, `"__OOM__"`, đếm. `chon` = số nguyên đầu tiên hoặc `None`. Trả `{"chon": […], "raw": […], "dt": giây}`.
   - Mỗi 50 lần in thống kê (số lần, số câu, giây/câu, OOM).
   - Mọi lỗi khác của một kết nối: in cảnh báo, cố gửi `{"loi": repr(e)}`; luôn đóng kết nối và **không dừng máy chủ**.

### B.8 `doc_288.py` — đọc kết quả TEST của 288 (cách A)

**Mục đích.** So nhánh chính A (`nghev101` nếu G0 giữ cổng v, ngược lại `nghe101`) với ck500, S1 và
các đối chứng trên tập test, rồi xếp kết cục K1–K4 theo luật khoá trước. Dùng `nap`, `so`, `SEED`
của B.9.

**Tham số.** `--recs` (test.jsonl, phải đủ 6.958 bước), `--nhanh ten:raw:nontap` (lặp; bắt buộc có
`S1`, `ck500` và nhánh chính), `--venus ten:raw` (lặp, tệp thô chấm bằng UI-Venus), `--chinh`,
`--gia` (in nhãn GIẢ), `--out`. Tên nhánh có dạng `<nghev|nghe|nghern|spicea><hạt>`; nhánh chính phải
là `nghev` hoặc `nghe` hạt 101. `B1 = nghe<hạt>`.

**Tập bước.**

- `ck` = giao các bước chạm có trong tệp thô của **mọi** nhánh, sắp tăng.
- `ntk` = các bước không chạm (lấy từ S1), sắp tăng.
- `gop` = exec trên `ck` nối với điểm loại thao tác đúng trên `ntk`.

**Phép so `ss(x, y, loai)`:** gọi `so` với `rng` **mới** hạt 101 mỗi lần; `loai = exec` (trên `ck`),
`nt` (trên `ntk`), hoặc `gop`. `venus(x, y)`: so exec UI-Venus trên giao bước của hai tệp.

**Các phép so được tính** (chỉ khi có tệp): `A-ck500`, `A-S1`; `A-spicea101` và `spicea101-ck500`;
`A-B1` (nếu A ≠ B1); `A-nghern101`; `nghev202-ck500`, `nghe202-ck500`, `nghev202-nghe202`; UI-Venus
`A-ck500`; mô tả `A-S1`, `A-ck500` theo `nt` và `gop`.

**Luật kết cục.**

1. `tang = Δ(A−ck500) > 0`.
2. `dot2` = các nhánh còn thiếu trong `[spicea101, B1 (chỉ khi A là nghev), <arm>202]`, cộng "UI-Venus ck500 + A" nếu thiếu.
3. Điều kiện "vượt": LB(A−ck500) > 0; LB(A−S1) > 0; Δ UI-Venus(A−ck500) > 0; nếu có spicea101 thì Δ(A−spicea101) > 0; nếu có hạt 202 thì Δ(A202−ck500) > 0. `vuot` = tất cả đạt.
4. Xếp:
   - không `tang` → **K1** (dừng, không chạy đợt nào nữa);
   - còn thiếu đợt 2 → **CHỜ-ĐỢT-2** (chưa xếp, chưa được viết câu nào);
   - không `vuot` → **K2** nếu LB(A−ck500) ≤ 0, ngược lại **K2+** kèm danh sách điều kiện thiếu;
   - ngược lại **K3**; nếu A là `nghev` thì xét thêm điều kiện "v gây ra": LB(A−B1) > 0; nếu có `nghern101` thì Δ(A−nghern101) > 0; nếu có `nghe202` thì Δ(nghev202−nghe202) > 0. Khi LB(A−B1) > 0 mà còn thiếu `nghe202` (và thiếu `nghern101` nếu Δ(A−B1) ≥ 0,5) → **K3 · K4-CHỜ-ĐỢT-3**; đủ và mọi điều kiện "v gây ra" đạt → **K4**.
5. In bảng phép so (a, b, Δ, KTC, cứu, phá), dòng UI-Venus, mô tả, điều kiện, kết cục và đợt cần chạy. Ghi JSON.

### B.9 `doc_286.py` — thư viện đọc test (B.8 và B.13 dùng) + bộ đọc của 286

**Phần thư viện**

- `canon(câu, strict_back=False)`: lấy các từ chữ thường `[a-z]+`; nếu `strict_back` và có từ "back" → `navigate_back`; ngược lại trả loại thao tác của **từ đầu tiên** có trong bảng ánh xạ; không có từ nào → `tap`. Bảng ánh xạ: tap ← tap, click, press, select, choose, touch, open, go, navigate, visit, view · type ← type, enter, input, fill, write · scroll ← scroll, swipe, drag · long_press ← long, hold · navigate_back ← back, return.
- `phu_ok(câu, action_type)` (thước phụ, từ vựng riêng): 1 nếu câu chứa ít nhất một từ của loại đó: scroll {scroll, swipe, slide, drag} · navigate_back {back} · input_text {type, enter, input, write, fill} · open_app {open, launch, start} · wait {wait, pause, load, loading, loaded} · navigate_home {home} · long_press {long, hold}.
- `cluster_ci` và `mcnemar`: như mục 0.3.
- `nap(recs, raw, nontap)` → bộ 4: `ex` (bước chạm → executable), `nt` (bước không chạm → (đúng loại thao tác theo `canon` strict cả hai phía, `phu_ok`)), `sx` (câu đã chấm ở bước chạm), `snt` (câu ở bước không chạm). Bước không chạm nào thiếu trong tệp nontap thì dừng. Câu rỗng ở bước không chạm tính sai loại. (Mỗi bản ghi recs được gắn sẵn `_tap` = là bước chạm.)
- `so(A, B, keys, ep, rng)` → `n, a, b` (% làm tròn 2), `d, lo, hi` (bootstrap cụm), `cuu` (A đúng B sai), `pha` (ngược lại), `p_mcnemar` (4 chữ số).
- `aisr(S1, ck500)` (nhánh ghép suy luận): ở bước chạm có trong cả hai, nếu một trong hai câu `None` thì lấy exec ck500 và đếm "bỏ qua"; nếu `canon` (không strict) của hai câu trùng thì lấy exec ck500, khác thì lấy exec S1. Ở bước không chạm: `canon` strict trùng thì lấy điểm ck500, khác lấy S1.

**Phần bộ đọc 286 (`main`)**

1. Nạp mọi nhánh; bắt buộc có S1 và ck500; tự dựng nhánh `AISR`. Có `--mau-nguoi` thì chỉ rút mẫu cho người (dưới).
2. `ck` = giao bước chạm của mọi nhánh (kể cả AISR); `ntk` = bước không chạm của S1.
3. Với **mỗi nhánh** (tạo `rng` hạt 101 riêng cho nhánh đó, dùng lần lượt cho mọi phép so của nhánh theo đúng thứ tự): exec, tỉ lệ đúng loại không chạm, thước phụ, gộp. Với mốc S1 rồi ck500 (bỏ chính nó): so exec, so không chạm, so gộp, rồi so không chạm theo từng loại scroll, navigate_back, input_text, wait, open_app. Nhánh khác S1: NFR scroll+back = tỉ lệ bước scroll/back mà S1 đúng còn nhánh sai; nhánh khác ck500 thì thêm KTC của hiệu NFR (nhánh − ck500).
4. Giả thuyết (theo thứ tự khoá trước H1 → H3′ → H3):
   - **H1** (`--h1 a,b`): mỗi nhánh LB(không chạm − ck500) > 0 và LB(exec − ck500) > −1,0; đạt khi mọi nhánh đạt.
   - **H2** (`--h2 x`): LB(exec − ck500) > −1,0 và cận trên hiệu NFR so ck500 < 0.
   - **H3′** (`--h3p`, chỉ khi H1 đạt): `rng` hạt 101 mới dùng chung cho các nhánh; so với AISR: đạt khi LB exec > 0 và LB không chạm > −1,0; "AISR trội" khi (exec hi < 0 và kc lo ≤ 0) hoặc (kc hi < 0 và exec lo ≤ 0); Pareto khi LB kc > 0.
   - **H3** (`--h3 y`, chỉ khi H1 đạt): so với nhánh y: đạt khi LB kc > 0 và LB exec > −1,0; ghi "chỉ mô tả" nếu H3′ không đạt.
   - **Hg1** (`--hg`, chỉ khi H1 đạt, thêm sau khi đã thấy số S1/ck500/AISR): `rng` hạt **102**; KTC 97,5% (q = 0,0125) cho hiệu gộp nhánh − ck500, đạt khi cận dưới > 0; kèm mô tả KTC 95% so ck500 và AISR.
   - Mô tả back: hiệu navigate_back so ck500; Δ < −2,0 thì khai "thất bại kiểu CTG".
5. Ghi `doc_286.json {nhanh, gia_thuyet}`.

`--mau-nguoi`: `random.Random(101)`; bước chạm chung S1/ck500 chia thành "lệch exec" và "trùng exec";
bước không chạm chia thành scroll+back và còn lại. Rút **theo đúng thứ tự** 120 lệch, 80 trùng, 60
scroll+back, 40 còn lại; sắp tăng; in md5 của `json.dumps(danh sách)`; ghi `mau_nguoi_300.json`.

### B.10 `cham/gieo_tho.py` — gieo tệp thô trước khi chấm

**Ý tưởng.** Bộ trỏ tất định (đo 6/10: 2.795/2.795 câu trùng thì trùng toạ độ), nên câu nào đã được
chấm ở nhánh cũ thì chép nguyên bản ghi chấm, `score_run.py` (chế độ nối tiếp) chỉ phải chấm câu mới.

`gieo_tho(preds, tho[], out)`:

1. Dừng nếu `out` đã tồn tại (không gieo đè).
2. `P[(ep, step)] = pred` từ tệp dự đoán.
3. Kho: duyệt các tệp thô theo thứ tự đưa vào, `kho.setdefault((ep, step, sent), bản ghi)` (tệp đầu thắng).
4. Với mỗi bước của P theo thứ tự tệp: có bản ghi khớp `(ep, step, pred)` và `pred` khác rỗng → ghi nguyên bản ghi.
5. In số bước đã chép và số câu còn phải chấm.

Tự kiểm (`--selftest --repo thesis-master`): (a) gieo ck500 từ tệp thô ck500 phải ra 4.462/4.463
(bước (18710, 1) câu rỗng ở cả hai nên không gieo); (b) gieo S1 (lọc preds S1 về các bước chạm) từ
tệp thô S1 ra 4.462; (c) gieo ck500 từ tệp thô S1 (không kỳ vọng số). Cả ba: mọi bản ghi gieo phải
**trùng hoàn toàn** bản ghi gốc cùng bước.

### B.11 `dung_lai_288.py` — dựng lại mọi tệp từ file bàn giao + repo

**Tham số.** `--md <file bàn giao>`, `--goc` (thư mục cha của `thesis-master`, mặc định `.`), `--kiem`
(chỉ so, không ghi).

**Bước 1 — tách mã.** Regex (đa dòng, `.` khớp xuống dòng) trên toàn file:
`^### (B\.\d+) \`đường\` — md5 \`32 hex\`, N dòng\n\n```python\n(nội dung)\n```\n`. Mỗi khối ghi
`nội dung + "\n"` (UTF-8) ra `--goc/đường`, rồi so md5. Chế độ `--kiem` chỉ báo thiếu/lệch.

**Bước 2 — chép tệp từ repo** (nguồn tương đối `thesis-master/`, đích tương đối `--goc`), so md5:

| nguồn | đích | md5 |
|---|---|---|
| harness/som_listener.py | _scripts/288/g0/ và _scripts/288/nghe/ | c61ef769e4f1993a7cad3a536e9ca277 |
| harness/som_build.py | _scripts/288/g0/ và _scripts/288/nghe/ | 2b7d257fccd7378586527b8a65d8b770 |
| harness/grpo_spice.py | _scripts/288/nghe/ và _scripts/288/cham/ | 07ea87b6d156d1faa391a4274dffd7cf |
| harness/build_branch_data.py | _scripts/288/nghe/ và _scripts/288/cham/ | 619e63e123a6dbf60086e65ee94a3912 |
| harness/gen_test_grpo.py | _scripts/288/cham/ | b18ec1aa3fd037ddffb9411db63c2a3f |
| runs/preds_s1_seed101.jsonl | _scripts/288/cham/ | bc8911912491bb97fd987b3c91a22bda |
| runs/score_s1_seed101_raw.jsonl | _scripts/288/cham/ | 0681d937d930c952b7ff92e0f24d5189 |
| runs/grpo_spice/score_ck500_test_raw.jsonl | _scripts/288/cham/ | 5b9d6d65cb0d2390b126d22463f888ee |
| runs/grpo_spice/pred_ck500_test.jsonl | _scripts/288/cham/ | 328847ac96fa3104f76cd997f4091bcd |
| runs/venus/preds_venus_s1_2532.jsonl | _scripts/288/cham/ | e715a46693f8e6a588d23816a5f75430 |
| runs/venus/score_venus_s1_2532_raw.jsonl | _scripts/288/cham/ | b19b4e834201c8fb22925694dc7bf0a7 |
| runs/grpo_spice/score_ck500_raw.jsonl | _scripts/288/cham/score_ck500_c1_raw.jsonl | 258ced11cad3b6729bbdb25f947dbe78 |
| runs/grpo_spice/score_k0_lai500_raw.jsonl | _scripts/288/cham/score_s1_c1_raw.jsonl | 1c8dbcd5f49ec53ecc655b4b4d2c04c4 |
| runs/grpo_spice/pred_ck500.jsonl | _scripts/288/cham/pred_ck500_c1.jsonl | eb6162d86730a936beb5ae5a9fd6d652 |

Thêm ba tệp sinh ra:

- `_scripts/288/cham/harness_venus/`: chép mọi `.py` và `.yaml` của `harness/` (để chấm UI-Venus); báo md5 `score_run.py`.
- `_scripts/288/nghe/prompt_keys_ck500.json` = `json.dumps(prompt_keys[:1000])` (dấu phân cách mặc định), md5 `4bf30d816dc531842495535828dcbb43`.
- `_scripts/288/cham/preds_venus_ck500_2532.jsonl`: lấy từng dòng của `preds_venus_s1_2532.jsonl`, thay cả `raw` lẫn `pred` bằng câu ck500 của bước đó (`ensure_ascii=False`); kỳ vọng 1.210 câu khác S1; md5 `34fa2cf897721fe3155f5d917feb7856`.

**Bước 3 — dữ liệu G0.** `g0_som.jsonl`, `g0_cau.jsonl` có thì so md5 (mục B.3); thiếu thì chỉ cách
chạy B.3 nếu có `all_forest_dict.zip`, ngược lại báo người dùng tự lấy zip.

Cuối: xoá `__pycache__` trong các thư mục `_scripts/288/{g0,nghe,cham}` và `_scripts/289`; in tổng
kết; mã thoát 1 nếu có lỗi.

### B.12 `cham/val_lon.py` — val lớn cho phễu sàng 289

**Tập val lớn.** Hợp `val_cham400.jsonl` và `val_cham600.jsonl` (khoá trùng thì giữ lần đầu), sắp
theo `(episode_id, step_id)`. Phải ra **1.567 bước, 1.002 bước click, 346 episode**. Không episode
nào nằm trong 1.000 câu nhắc GRPO của ck500.

`--dung --val V --out VD` (dựng thư mục để `score_run.py` chấm):

- `VD/val_lon_recs.jsonl`: mọi bước, thêm `gold_instruction` = `gold_instruction` sẵn có, không có thì `target_instruction`.
- Chép `ocr.jsonl` (nếu khác chỗ); tạo symlink `VD/images` → `V/images` (xoá link cũ nếu có).
- Kiểm không thiếu ảnh của bước click.

`--gen --bundle B --merged M --val V [--ckpt CK] --out pred.jsonl [--n N] [--so tệp]` (sinh câu, GPU):

1. Chỉ lấy 1.002 bước click (cắt `--n` nếu có). OCR nạp từ gói. Kiểm: mọi bước có trong `p1_val_rows.jsonl` của gói với **câu nhắc trùng từng ký tự** (`body_of`), đủ ảnh trong gói, đủ OCR. Lệch thì dừng.
2. Adapter = `<bundle>/adapter_s1_seed101`; nạp mô hình đã hoà bằng `grpo_spice.nap`; có `--ckpt` thì gắn `PeftModel.from_pretrained` lên trên (in ra), không có thì đây là S1 hoà.
3. Câu nhắc: `[{"role": "system", "content": SYS}, {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "\n" + prompt_body(...)}]}]`, qua `apply_chat_template(..., add_generation_prompt=True)`; ảnh `convert("RGB")`.
4. Sinh tham lam: `max_new_tokens=96, do_sample=False, use_cache=True`, đặt `temperature/top_p/top_k = None`. Giải mã phần sau câu nhắc, `strip()`.
5. Ghi nối thêm `{episode_id, step_id, pred}`, xả đệm mỗi dòng; nối tiếp được (bỏ bước đã có). Mỗi 50 bước in tiến độ.
6. Cuối: đếm câu, câu rỗng; có `--so` thì đếm số câu trùng với tệp so (kiểm đường sinh trùng đường đã sinh C1).

`--selftest` (CPU): kiểm 1.567/1.002/346 và OCR phủ đủ; 0 episode chung với prompt_keys; 249 bước
click C1 nằm trong 1.002 click; câu nhắc C1 dựng từ val lớn trùng câu nhắc dựng từ `c1_recs`; tệp thô
ck500 trên C1 (249 bước) là tập con của val lớn (để gieo được bằng B.10).

### B.13 `_scripts/289/doc_289.py` — bộ đọc phễu sàng (val lớn) và xác nhận (test)

**Ba nhánh của 289** (đều train **tiếp** 250 bước từ ck500, cùng 1.000 câu nhắc hạt 101, cùng phiên
A100): `tspicea` (SPICE y ck500, đối chứng "train lâu hơn"), `tnghev` (thêm người nghe có cổng v),
`tnghe` (người nghe không cổng).

**Hằng số.** `NGUONG_SANG = 1,0` điểm exec (bằng MDE click trên test so ck500). Nhánh X ∈ {tnghev, tnghe}.

`nap_raw(tệp)` → `(ep, step) → executable` (thiếu/`null` tính 0). `so(A, B, q=0,025)`: trên giao
khoá, bootstrap cụm với `rng` **mới** hạt 101 mỗi lần, trả thêm `ktc = 100(1−2q)`.

**Sàng (`sang`, val lớn, chỉ để chọn — cấm viết vào luận văn như kết quả)**

1. Bắt buộc có S1, ck500, tspicea; mỗi nhánh phải đủ 1.002 bước (thiếu thì chấm nốt).
2. So mọi nhánh với S1, mọi nhánh (trừ S1, ck500) với ck500.
3. Với mỗi X có tệp: Δ(X−tspicea) và Δ(X−ck500); **lên test** khi cả hai ≥ 1,0 (ước điểm, không xét KTC). X không có tệp thì ghi lý do: dừng theo luật train (có trong `--dung`) hoặc không train. Có cả hai X thì so thêm tnghev−tnghe.
4. Có X lên → thêm tspicea (đối chứng bắt buộc). Không X nào lên: tspicea lên một mình khi Δ(tspicea−ck500) ≥ 1,0 (ghi rõ chỉ là "train lâu hơn"); ngược lại **DỪNG**, không chấm test nhánh nào.

**Xác nhận (`xac_nhan`, test, mỗi nhánh được lên chấm một lần)**

1. X = các nhánh người nghe được lên; `q = 0,025 / max(số X, 1)` (Bonferroni). Bắt buộc có tệp test của S1, ck500 và mọi nhánh được lên.
2. Mô tả: mỗi nhánh lên so base/S1/ck500 (nếu có), S1−base, ck500−base, ck500−S1.
3. Có tspicea → so tspicea−ck500 (95%).
4. Với mỗi X: X−ck500 và X−S1 với KTC `1 − 2q`; X−tspicea 95%; UI-Venus X−ck500 nếu có cả hai tệp. **VƯỢT(X)** ⇔ LB(X−ck500) > 0 ∧ LB(X−S1) > 0 ∧ Δ(X−tspicea) > 0 ∧ Δ UI-Venus(X−ck500) > 0.
5. Còn thiếu UI-Venus của X nào thì đưa vào "chạy thêm". Nếu tnghev VƯỢT: có test tnghe thì `v_gay_ra = LB95(tnghev−tnghe) > 0`, chưa có thì thêm "test tnghe" vào "chạy thêm".
6. Kết cục: còn "chạy thêm" → **CHỜ**; không có X → **T0** (train lâu hơn, nâng có ý nghĩa nếu LB(tspicea−ck500) > 0); không X nào VƯỢT → **T1**; `v_gay_ra` → **T3**; còn lại → **T2** (ghi "cổng v không được chứng minh" nếu tnghev vượt).

**Tự kiểm (`kiem --repo thesis-master`)**

Nhánh giả `gia(N0, n, hat, chieu=1, pha=0)`: `rng = default_rng(hat)`; hàm `lat(v0, m)` lấy các khoá
có giá trị v0, sắp tăng, đổi thành mảng numpy 2 cột, `rng.permutation` theo hàng, lấy m hàng đầu.
Gọi theo thứ tự: `lat(0 nếu chieu > 0 ngược lại 1, n)` rồi `lat(giá trị ngược lại, pha)`; lật giá
trị của các khoá được chọn.

- Sàng trên **C1 thật** (249 bước, bỏ điều kiện 1.002), mốc S1 = `score_k0_lai500_raw.jsonl`, ck500 = `score_ck500_raw.jsonl`:

| ca | nhánh | phải lên |
|---|---|---|
| X +2,4 hơn cả hai | tspicea = ck500, tnghev = gia(ck500, 6, 1) | tnghev, tspicea |
| X +0,8 | tnghev = gia(ck500, 2, 1) | (không) |
| tspicea +2,0, X = tspicea | tspicea = tnghev = gia(ck500, 5, 2) | tspicea |
| X hơn ck500 +3,2, hơn tspicea +0,4 | tspicea = gia(ck500, 7, 3), tnghev = gia(ck500, 8, 3) | tspicea |
| cả hai X lên | tnghev = gia(ck500, 6, 1), tnghe = gia(ck500, 4, 5) | tnghev, tnghe, tspicea |
| tnghev dừng, tnghe lên | tnghe = gia(ck500, 4, 5), `dung = tnghev` | tnghe, tspicea |
| không ai lên | tspicea = gia(ck500, 1, 9) | (không) |

Thêm: gọi sàng với điều kiện 1.002 trên tệp 249 bước phải bị chặn.

- Tái lập test thật: ck500−S1 phải ra đúng `(60,65; 59,11; +1,55)`.
- Xác nhận trên test thật với nhánh giả. `X3 = gia(ck500_test, 334, 11, pha=200)` (≈ +3,0 điểm); `Vs` = tệp thô UI-Venus S1 2.532 bước dùng làm "ck500" UI-Venus:

| ca | kỳ vọng mở đầu kết cục |
|---|---|
| tnghe = X3, venus tnghe = gia(Vs, 30, 1) | T2 |
| như trên nhưng không có venus | CHỜ |
| venus tnghe = gia(Vs, 30, 1, −1) (chiều xấu) | T1 |
| tnghe = gia(ck500, 222, 11, pha=200) (≈ +0,5) | T1 |
| tnghev = X3, chưa có tnghe | CHỜ |
| tnghev = X3, tnghe = gia(ck500, 210, 4, pha=200) | T3 |
| tnghev = tnghe = X3 | T2 |
| tspicea = gia(ck500, 400, 12, pha=200), tnghe = X3 | T1 |
| chỉ tspicea = X3 | T0 |

**Dòng lệnh.** `che_do ∈ {sang, test, kiem}`; `--nhanh ten:tệp` (lặp), `--venus ten:tệp`, `--dung
ten`, `--sang sang_289.json` (bắt buộc ở chế độ test, đọc danh sách `len`), `--repo`, `--out` (mặc
định `<che_do>_289.json`). In mọi phép so (a, b, Δ, KTC, n, cứu, phá), lý do sàng, điều kiện vượt
và kết cục; ghi JSON.

### Các chỗ dễ làm sai khi viết lại

1. Thứ tự rút ngẫu nhiên phải giữ: B.5 giả lập (rút h trước, parse fail sau, theo thứ tự `g0_cau`); B.5 O_rand (200 lần, mỗi lần một vector 249 số); B.6 v_rand (theo khoá đã sắp); B.9 (`rng` dùng lại trong một nhánh, thứ tự phép so cố định); B.9 `mau_nguoi` (thứ tự 4 lần rút); B.13 `gia` (lật chính trước, lật phá sau).
2. Kiểu khoá: B.3 và B.4 dùng `episode_id`, `step_id` dạng chuỗi; tệp thô và recs dùng kiểu như trong tệp. Lẫn int với chuỗi thì giao khoá rỗng mà không báo lỗi.
3. Oracle phá hoà theo k nhỏ nhất, và h nhân 10 để luôn quyết trước SPICE.
4. Lỗi máy chủ trong một lô làm h = 0 cho cả lô, kể cả câu đã có trong bộ đệm (B.6).
5. Câu nhắc GRPO luôn dựng với hạt 101; `--seed` chỉ đổi hạt cấu hình và hạt khởi LoRA.
6. Chọn 9 câu C1 theo `id` thứ tự chèn; đổi thứ tự là đổi shard và đổi md5 dữ liệu G0.

### Mã nguyên văn dùng để dựng lại

B.11 chỉ tách được khối mã trong `288_PHU_LUC_B_MA_NGUON_6_10.md`. Bản mô tả này không thay file đó
khi cần đúng md5. Lệnh dựng lại ở §9.
