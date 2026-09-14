# 152 — LỘ TRÌNH THI HÀNH `151`, bản 9/9/2026 (mốc bảo vệ: **trên 6 tuần**)

> Đây là **kế hoạch đang có hiệu lực**. Nguồn khoa học là `report/151`; file này chỉ nói
> *làm gì, theo thứ tự nào, phụ thuộc cái gì, đã xong tới đâu*. Khi `151` và file này mâu
> thuẫn về **nội dung khoa học** thì `151` thắng; về **thứ tự thi hành** thì file này thắng,
> vì nó đã đối chiếu với trạng thái thật của máy WSL.

**Nguyên tắc xếp thứ tự:** bốn mắt xích giải thích phải vào luận văn **trước** khi chạy
VIS-SFT. Nếu VIS-SFT trắng (xác suất 0,70 theo chính `151`), chương 6 vẫn phải đứng vững.

---

## 0. Năm điều đã kiểm trên máy WSL ngày 9/9 — `151` mô tả khác

| # | `151` nói | thực tế WSL | hệ quả cho lộ trình |
|---|---|---|---|
| 1 | `test_ac/descriptors.jsonl` mất, cần dựng lại ~8 GB | **còn, 4.448 dòng** | mục 6.2 bỏ được phần lớn ⇒ **việc 6 đã xong**, xem §1 |
| 2 | `train_ac/` không tồn tại | **có**: `train.jsonl` 64.567 · `ocr.jsonl` 64.567 · `descriptors.jsonl` 41.099 | **P3bis bỏ được**, P4 chạy ngay |
| 3 | P5 chỉ nêu `infer_branch.py` đọc cứng đường dẫn | **`score_run.py:47,437` cũng cứng** `dg1_cache/test_ac` và `test.jsonl` | phải thêm tham số cho **cả hai**, không chỉ một |
| 4 | — (không nêu) | `train_ac/images/` chỉ có **1.697 ảnh**, không phải 64.567 | **chấm val trên Kaggle bị chặn tới khi kéo được ảnh** — xem §3 |
| 5 | — (không nêu) | `build_train_data.py:157` **ghi đè** `train.jsonl` và chỉ lấy `n_shards` **đầu** | ⛔ chạy `--shards 8` là **phá** `train.jsonl` 64.567 dòng. Sao lưu trước |
| 6 | §5.3bis viết `r: 16 -> 32, lora_alpha: 32 -> 64` | bộ adapter thật có **r = 8, lora_alpha = 16** | ⛔ viết số cứng là sai `scaling` gấp đôi mà không có gì báo; `noi_suy.py` đọc từ `adapter_config.json` |
| 8 | §4 viết `run_exp(args="harness/train_config_vissft.yaml", callbacks=[…])` | bản pin **c4e09c7cbe18** nhận **dict**, truyền chuỗi thì `hf_argparser` ném `TypeError: can only concatenate list (not "str") to list` | phải là `run_exp(args=yaml.safe_load(open(CFG)), callbacks=cbs)` |
| 9 | §4 viết `from llamafactory.extras.callbacks import LogCallback` | bản pin để nó ở **`llamafactory.train.callbacks`**; `extras.callbacks` không tồn tại | dò hai đường, không có thì chạy không kèm — chỉ mất `trainer_log.jsonl` |
| 7 | §5.3bis: trộn thẳng `lora_A`/`lora_B` sai **65%** tại α=0,5 | đo thật trên cặp này: **0,0163%** | GRPO học tiếp từ MIN nên chỉ dịch chuyển A **1,39%** và B **6,87%**; số hạng chéo tỉ lệ với tích hai độ lệch. Con số 65% chỉ đúng cho hai adapter huấn luyện độc lập. ⭐ Hệ quả cho V2: hai đầu mút rất gần nhau, nên kỳ vọng +0,2…+0,5 pp của `151` có thể còn lạc quan |

⚠️ Điều thứ sáu, không phải lỗi của `151` mà là tính chất của thiết kế: **S1, MIN, GRPO đều đã
train trên toàn bộ 64.567 bước**, nên val tách ra từ chính tập đó là dữ liệu chúng **đã thấy**.
Điểm val của ba nhánh ấy là điểm *train*, lạc quan có hệ thống. Chấp nhận được cho V1 (phép thử
bắt thảm hoạ) và cho việc **xếp hạng α** (cả 5 ứng viên nội suy đều lạc quan như nhau), nhưng
⛔ không được trích ra báo, và phải khai khi viết. Với A6 (chọn điểm lưu VIS-SFT) thì không còn
vấn đề, vì VIS-SFT sẽ train trên `train_tru_val.jsonl`.

---

## 1. CHẶNG 1 — luận văn, 0 GPU, 0 đồng ⟵ **ĐANG LÀM**

Mục tiêu: đưa bốn mắt xích giải thích của `151` vào luận văn, để dù không chạy thêm gì nữa thì
bài vẫn bảo vệ được.

- [x] **V6. D.3 tái lập được từ kho** — thêm hàng GRPO vào `NHANH` của `harness/luat_d3.py`,
      chạy, ghi `runs/luat_d3.json`. ✅ **xong 9/9**, ra đúng **67,04**, khớp `report/144:127`
      và khớp cả 9 hàng bảng mục 7 của `151`. Dải dùng được: Voronoi 62,88 · D.3 **68,88**.
- [x] **V1. ch6 — mục định vị điểm nghẽn.** ✅ **xong 9/9** — §`sec:haikenh`, bảng `tab:haikenh`. Bảng hai kênh (kênh A 70,10% mô hình tự khai ·
      kênh B 69,36% UGround đọc câu, n=4.442); lát A-đúng 3.114 bước / A-sai 1.328 bước với ba
      cột MIN · S1 · người; khoảng cách người − MIN **+15,53 pp** phân bố **9,0% / 91,0%**;
      thiếu hụt riêng của mô hình **+45,30 pp**. Kết luận: điểm nghẽn là **tri giác**.
- [x] **V2. ch6 — hệ số truyền.** ✅ **xong 9/9** — gộp trong §`sec:haikenh`, bảng `tab:ocheokenh`. d(kênh A) +1,60 pp cho d(exec) +0,045 pp ⇒ **0,028**, so
      tương quan mặt cắt ngang 0,739 (**thấp hơn 26 lần**). Bài học phương pháp: tương quan mặt
      cắt ngang không phải hệ số nhân quả. Kèm bảng ô chéo A(MIN)×A(GRPO) 2997/1143/184/113.
- [x] **V3.** ✅ **ĐÃ CÓ SẴN** ở `ch6:970` trong §`sec:grpo` (1.950 bước đổi khai báo, 1.300 tức 66,7% câu không đổi một ký tự, 197 lần đổi chiều nằm gọn trong 961 bước có câu đổi) ⇒ **không viết trùng**. Đổi `<desc>` ở
      **43,69%** số bước, nhưng trong đó **66,67% câu không đổi một ký tự**; đối chiếu đổi hẳn
      công thức train (MIN so S1) thì câu đổi ở 61,51%. ⇒ hàm mất mát chưa bao giờ so hai **câu**
      khác nhau. Đây là lời giải thích **thống nhất** cho cả năm ô trắng.
- [x] **V4.** ✅ **xong 9/9** — đặt ở ch6 §`sec:tranlat` (không phải ch5), bảng `tab:tranlat` bốn cách định nghĩa nhóm. Trần ORPO tầng câu +4,80 → +2,88 → **−0,65** tuỳ cách
      định nghĩa lát, trong khi cột *người* gần như đứng yên ⇒ chữ ký của hiệu ứng chọn mẫu.
      Nêu như một phép kiểm bắt buộc với **mọi** trần suy từ lát chọn theo hành vi mô hình.
- [x] **V5.** ✅ **xong 9/9** — bảng `tab:anhxa` đầu ch3 + đoạn giải thích vì sao đơn vị là một bước. Hiện *trường hợp sử dụng* / *giao diện người dùng* chỉ
      xuất hiện ở `main.tex`, `03_trangthongtin.tex` và một đoạn `ch1:22-28`; từ ch3 đến ch7
      không dùng lại. Thêm một bảng ánh xạ ở ch3 (use case → `goal` + lịch sử bước · front-end →
      ảnh + OCR + cây trợ năng + khối ứng viên · hướng dẫn → `step_instruction`) và dùng lại từ
      vựng đó ở ch4. Chuẩn bị sẵn câu trả lời cho *"vì sao đơn vị là một bước, không phải cả tài
      liệu hướng dẫn"*.
- [x] **V7.** ✅ **xong 9/9** — VIS-SFT thành hướng đầu tiên, khai thẳng P = 0,30 và hai ràng buộc thiết kế. Thay khung nhánh ứng viên hiện tại (`ch7:245`)
      bằng VIS-SFT, khai thẳng **P(vượt MDE) = 0,30** [0,15 · 0,45].
- [x] **V8.** ✅ **xong 9/9 — 122 trang, 0 overfull, 0 tham chiếu hỏng**, PDF đã chép về `thesis/main.pdf`. Lệnh dùng: dựng lại PDF, kiểm số trang và 0 overfull:
      `rm -f main.log && tectonic -X compile main.tex --outdir . --keep-logs`
      ⛔ không `>/dev/null`; nếu user đang mở PDF thì dựng vào scratchpad.

---

## 2. CHẶNG 2 — Phase 0 của `151`, 0 GPU

Trên WSL bỏ được P2 và P3bis (xem §0 mục 1–2). Còn lại:

- [x] **P1** ✅ **xong 9/9** — ⛔ phải đổi `harness/dg1_cache/` thành `harness/dg1_cache/*` rồi mở
      lại từng tầng: loại cả thư mục thì git **không duyệt vào trong** và mọi dòng `!` bên trong
      vô hiệu. Đã kiểm: `descriptors.jsonl` và `test.jsonl` track được, ảnh và `train_ac/` vẫn bị loại.
- [x] **P3 phần D.3** — đã gộp vào V6 của chặng 1.
- [x] **P4** ✅ **xong 9/9** — `harness/tach_val.py` đã chạy: val400 **407 bước / 90 episode** · val600 **604 / 128** · train_tru_val **63.556 / 12.677**, cộng đúng 64.567; bốn phép kiểm rò rỉ đạt; lệch phân bố 0,78 và 1,14 pp. Tách theo **episode**,
      400 + 600 bước, phân tầng theo `action_type`. ⛔ Không phân tầng theo `app`.
- [x] **P4bis** ✅ **xong 9/9 — 63.556 = 64.567 − 1.011 cho cả bốn nhánh**, ra `branches_tru_val/` với `gui_s1 → s1.json`. — đã thêm `--recs-file`, và thư mục ra tự đổi thành `branches_tru_val` khi dùng tệp khác, nên không thể lẫn hai bộ. Sửa `harness/build_branch_data.py:111` → `train_tru_val.jsonl`, chạy lại để sinh
      bộ `gui_s1` mới. ⭐ Kiểm: bộ mới nhỏ hơn bộ cũ đúng bằng số bước val (≈1.004).
      ⛔ **Chỉ cần trước Phase 2**, không chặn Phase 1.
- [x] **P5** ✅ **xong 9/9** — `--data-root` + `--recs-file` cho cả hai script, mặc định giữ nguyên hành vi cũ, và in dòng `[dữ liệu] …` để kiểm đúng tập. Thêm tham số đường dẫn tệp vào **cả** `infer_branch.py` (dòng 29, 408) **và**
      `score_run.py` (dòng 47, 437) — xem §0 mục 3.
- [x] **P6** ✅ **xong 9/9** — hai tệp user tải về trùng khít md5 với bản đã có sẵn từ 6/9; thiếu `adapter_config.json` của MIN, đã tạo từ config GRPO (hợp lệ vì 504/504 khoá và mọi shape trùng khít). Nguồn: từ `MyDrive/thesis/ckpt/grpo_point_seed101/`:
      `adapter_grpo_point_seed101/` (GRPO) và `adapter_ref_min/` (MIN).
- [x] **P7** ✅ **xong 9/9** — thêm `--alpha` vào `infer_branch.py`: khai `add_argument` quanh dòng 357 **và** chèn
      khối `LoraLayer` sau dòng 516. ⛔ Thiếu khai tham số là `AttributeError` ngay lập tức.
- [~] **P8** ⏳ **gần xong 9/9** — viết lại theo đặc tả rồi đối chiếu với mục *Kết quả mong đợi*
      của `151`, đó là phép kiểm mạnh hơn chép đúng từng ký tự từ ảnh.
      · ✅ **`phu_luc_b.py`** — khớp **tuyệt đối** B.1: n=4.442 · kênh A 70,10 · A-đúng
        3.114/82,37/74,18/84,36 · A-sai 1.328/8,43/24,47/55,72 · khoảng cách +15,53 (9,0/91,0%) ·
        thiếu hụt riêng **+45,30** · hệ số truyền **0,028** · ô chéo 2.997/1.143/184/113 ·
        cần 243 lần lật sạch · sàn 12,00 so 20,50 ⇒ **86%**.
        ⚠️ Phải dùng **HAI** quần thể: mục A và C chỉ đọc `<point>` của MIN (**4.442**), mục B so
        MIN với GRPO nên đòi cả hai đọc được (**4.437**). Gộp làm một là siết nhầm A và C.
      · ✅ **`phu_luc_c.py`** — khớp **tuyệt đối** C.1, cả 24 ô: trần ORPO +4,80 → +2,88 → −0,72
        → −0,65 qua bốn cách định nghĩa nhóm, cột người 55,69/54,70/60,18/73,55.
      · ✅ **`phu_luc_d.py`** — khớp **tuyệt đối** D.1: 1.950 (43,69%) · 1.489 (33,36%) ·
        961 (21,53%) · trong 1.950 thì 1.300 (66,67%) câu y hệt · MIN vs S1 4.280/6.958 = 61,51%.
      · ✅ **`do_chot_cuoi.py`** (Phụ lục A) — mục A khớp **tuyệt đối** bảng mục 7 của `151`:
        `action_ok` Base 96,46 · S1 94,35 · MIN 98,88 · GRPO 98,86 · câu chuẩn 100,00, cùng cả 20
        ô của bốn luật. Mục B khớp **tuyệt đối tới hai chữ số** ở mọi Δ (MIN−S1 +0,94/+1,48/+0,02 ·
        GRPO−S1 +0,96/+2,13/+0,72 · GRPO−S1/202 +0,45/+1,46/+0,11 · S1/202−S1 +0,52/+0,67).
        ⚠️ Giá trị `p` lệch ở chữ số thứ ba, ví dụ 0,0940 so với 0,0953 — đó là **nhiễu bootstrap**
        chứ không phải sai số: `151` không ghi hạt giống nên không tái lập được đúng dãy lấy mẫu.
        Nhãn *loại 0* hay *TRẮNG* không đổi ở ô nào.
      ⭐ **Kết quả MỚI mà `151` không có — hiệu chỉnh Holm cho GRPO − S1/101 trên ba luật:**
        ±14% từng trục p=0,0003 **giữ**, AitW Euclid p=0,0010 **giữ**, Voronoi (thước tiêu đề)
        p=0,0860 **mất** ý nghĩa. Đây là bằng chứng **định lượng và độc lập** cho lập luận giữ
        thước ở `151` mục 6.1: đổi sang luật dung sai đơn thuần biến một phép so không có ý nghĩa
        thành có ý nghĩa, và kéo Δ từ 0,96 lên 2,13. Đã thêm vào luận văn ch5 §`sec:donhay`.
      ⚠️ Hai chỗ phải sửa khi dựng lại, đã trả giá: cột đầu là `action_ok` **thuần**, nhân thêm
      `toggle_ok` thì câu chuẩn còn 99,93 và mọi hàng lệch ~0,1 pp; và bootstrap phải **gộp sẵn
      theo cụm** trước khi lấy mẫu, nếu duyệt từng bước thì 563 triệu phép và không chạy nổi.

⚠️ **P1 vẫn cần** dù `descriptors.jsonl` còn trên đĩa: `.gitignore:111` chặn cả
`harness/dg1_cache/`, nên tệp **chưa được track**. Thêm dòng
`!harness/dg1_cache/test_ac/descriptors.jsonl` thì người khác clone mới tái lập được D.3.

---

## 3. CHẶNG 3 — Phase 1 trên Kaggle T4, **0 đồng** (chạy song song chặng 1)

⛔ **Không song song hoàn toàn:** V1/V2/V3 chấm trên val, mà val chưa tồn tại. Đường tới hạn là
**P4 → kéo ảnh val → P6 → P7 → `noi_suy.py` → upload dataset → V1 → V2 → V3**. Bốn việc đầu đều
0 GPU và làm trong một buổi, nên thực tế vẫn song song được với việc viết luận văn.

Runbook step-by-step: **`harness/kaggle_phase1_noisuy_9_9.md`**.

- [~] **B1** P4 (dựng val) — nhưng phải ràng buộc theo ảnh, xem B2.
- [x] **B2** ✅ **xong 9/9 — 6.774 ảnh / 1.733 episode**, `train.jsonl` md5 vẫn khớp bản sao lưu. ⛔ Trước đó `train_ac/images/` chỉ có 1.697 ảnh. ⛔ Đừng chạy
      `build_train_data.py --shards k` để lấy ảnh: nó **ghi đè** `train.jsonl`. Cách trong
      runbook: tải **8 shard rải đều**, ghi ảnh ra thư mục riêng, rồi cho `tach_val.py` chọn val
      **chỉ trong các episode có ảnh**. ~1.000 ảnh ≈ **187 MB** (trung vị 192 KB/ảnh); đĩa D còn
      210 GB nên thoải mái.
- [x] **B3** ✅ **xong 9/9** — 5 mức α đã dựng ở `runs/noisuy/`, kiểm đại số cho sai số ≤ 2,2e−07 ở mọi α. P6 + P7 + `harness/noi_suy.py` (mã ở `151` §5.3bis), dựng 5 mức α = 0 / 0,25 / 0,5 /
      0,75 / 1,0.
- [x] **B4** ✅ **xong 9/9**, ba dataset đã mount. ⚠️ Hai bài học đường dẫn, đã vá vào runbook:
      Kaggle chèn tầng `datasets/<user>/` và gói `.zip` bung ra **có** thư mục bọc ngoài ⇒ ô dựng
      workspace phải dò theo **tên tệp mốc**, ⛔ đừng ghim tên dataset. Và gói `thesis-val` upload
      lên **mất sạch ảnh** (chỉ còn 3 jsonl) — không upload lại 531 MB mà kéo thẳng 1.011 ảnh từ
      HuggingFace ngay trên Kaggle (Ô 1b, ~5 phút, 0 đồng, dùng lại logic `keo_anh_val.py`).
- [x] **B5 + B6** ✅ **xong 9/9 — V1 ĐẠT, V2 TRẮNG. Toàn văn `report/153`.**
      `exec` val: α=0 **67,56** · ba mức giữa đều **67,94** · α=1 **68,32**, n=**262** bước chạm.
      Điểm giữa **thua** đầu mút tốt hơn 0,38 pp ⇒ **khoá α=0** theo §5.4 của `151`.
      ⭐ Ba phép kiểm chặn đạt: hai đầu mút trong 50–70 · dải 0,76 pp ≪ 9 pp · câu hai đầu mút khác
      nhau 38,1% và **tăng đơn điệu theo α** (53·95·127·155) ⇒ ghép nối theo hạng chạy đúng.
      ⭐ **Phẳng ở cả sáu luật chấm** (Voronoi · D.3 · D.3∧14% · `hit_disk` · chữ nhật ±14% · nL2),
      dải đúng 0,76 pp ở **mọi** luật ⇒ đòn *"đổi thước thì Δ khác"* không mở được (`153` §7.1).
      ⭐ Val cao hơn test **~7,5 pp** và phóng đại khoảng cách hai nhánh **gấp 40 lần** (0,76 so
      0,02) ⇒ luật cấm trích số val nay có số đo chống lưng, không còn là nguyên tắc suông.
      ⚠️ Phép kiểm trùng-từng-ký-tự với `preds_min_desc_seed101.jsonl` **chưa làm được** — hai tệp
      đó sinh trên tập kiểm còn lượt này chạy trên val. Chứng cứ hiện có là đại số (≤ 2,2e−07 ở
      mọi α) cộng bảng khác-câu đơn điệu ở trên.
- [ ] ⛔ **B7 — V3 soup: ĐỀ XUẤT KHÔNG CHẠY** (`153` §7.5). Ba lý do: đường cong phẳng ở **mọi**
      luật chấm · CE2-S2 thấp hơn MIN **0,63 pp** trên test · và **adapter CE2-S2 không có trên
      WSL** (kho chỉ có MIN · GRPO · `gui_sel`), phải kéo từ Drive rồi dựng soup ba khối
      (`r` 8→24, `lora_alpha` 16→48) rồi upload dataset ⇒ không phải "chỉ 4 h T4".
      Quyết định là của chủ luận văn; bỏ thì ghi rõ lý do là kết quả V2, chạy thì báo vô điều kiện.
- [x] **B8** ⛔ **KHÔNG chạy** — argmax-val là α=1, tức đúng GRPO-point vốn đã có điểm test 60,07. Chấm lại là chấm lại chính nó; tiết kiệm ~5,6 h T4. Luật gốc: khoá đúng một α, ghi vào `report/106` **trước khi** chấm test, rồi chấm test
      **một lần** ~5,6 h T4, báo vô điều kiện kèm cả hai đầu mút.

**Đã tiêu: ~4,2 h T4 = 0 đồng** (suy luận 1,7 h + chấm 1,4 h + kéo ảnh và probe ~1 h), so với
dự trù ~17 h. Bỏ V4 tiết kiệm 5,6 h, bỏ V3 tiết kiệm thêm 4 h.
**Kỳ vọng ghi trước là +0,2…+0,5 pp, có thể bằng 0 — kết quả thật còn dưới mức đó** (điểm giữa
âm 0,38 pp so với đầu mút tốt hơn). Không mức nào tới ngưỡng 2,0 pp, nên không có gì lên tiêu đề;
nó vào luận văn như **một hàng bảng và một kết quả âm**, đúng cam kết báo vô điều kiện của
`151` mục 8. Đóng góp mô hình **giữ nguyên ở GRPO-point 60,07**.

---

## 4. CHẶNG 4 — Phase 2, lượt A100 duy nhất

Chỉ bắt đầu sau khi chặng 1 xong và P4bis đã chạy.

- [x] **A1** ✅ **xong 9/9** — `harness/train_config_vissft.yaml`, đúng **ba** dòng khác `train_config.yaml`: `freeze_vision_tower` (biến khoa học duy nhất), `output_dir`, `dataset_dir` (trỏ `branches_tru_val`).
      ⭐ Can thiệp duy nhất: `freeze_vision_tower: false`. ⛔ `weight_decay` giữ **0**.
- [x] **A2** ✅ **xong 9/9** — `harness/grid_callback.py` + `harness/chay_vissft.py`. ⛔ Gọi `run_exp` từ Python, **không**
      gọi `llamafactory-cli`, nếu không `grid/` rỗng và mất 40 quan sát.
- [x] **A3** ✅ **xong 9/9** — `harness/khang_dinh_vissft.py` (chưa chạy được trên WSL vì thiếu `transformers`; chạy trên Colab trước bước 1). Nội dung: tham số huấn luyện > 14.966.784 và có tensor `visual.*` với
      `requires_grad=True`. ⛔ Không dùng cổng `grad_norm` bước 10.
- [x] **Runbook chặng 4** ✅ **xong 9/9** — `harness/colab_vissft_9_9.md`, bảy ô dán kèm bốn điều
      phải đọc trước. Gói dữ liệu `_bundles/vissft_data.tar.gz` (48 MB, md5 `5130635e5493`) đã đóng,
      chờ upload lên `MyDrive/thesis/`.
- [x] **Cơ chế cắt lỗ** ✅ **thiết kế 9/9** — `151` không có cơ chế nào cho việc này. Hai điểm
      kiểm với **hai luật khác nhau**: K1 ở bước 3.200 hỏi *có hỏng nặng không* (so mốc MIN chấm
      trên chính `val_cham400`), K2 ở bước 4.800 hỏi *còn lên nữa không* (so chính K1). Ngưỡng
      **3,0 điểm** ở cả hai, tức ≈3 lần sai số chuẩn ghép cặp.
      ⛔ **Không dùng early stopping theo patience:** trên 400 bước chạm, SE ghép cặp ~1,03 điểm,
      nên một lượt đang tăng đều +0,3 điểm mỗi 800 bước vẫn có ~38% khả năng *trông như* giảm ở
      một lần đánh giá bất kỳ; `patience = 2` gần như chắc chắn dừng oan. Thứ thay thế tốt hơn đã
      có sẵn là 40 điểm lưới, tức chọn điểm lưu **sau** khi thấy toàn bộ đường cong, chi phí 0 giờ
      A100. Early stopping chỉ tiết kiệm giờ máy, không cải thiện kết quả.
      ⭐ Chọn đúng 3.200 và 4.800 vì cả hai nằm trong năm điểm A6 sẽ chấm sau ⇒ công không phí,
      và trả lại ~1,5 h T4 ở khâu A6.
- [ ] **A4** smoke 200 bước (~0,5 h).
- [ ] **A5** VIS-SFT **20–37 h A100**. Mốc so **S1/101 = 59,11**.
- [ ] **A6** chấm `step01600/03200/04800/06400/07800` trên val 400, rồi 2 điểm tốt nhất ±200 bước
      ⛔ **7.876 bước, không phải 8.072** — tập dạy nay 63.000 mẫu; điểm lưới cuối là `step07800`,
      adapter bước cuối nằm ở gốc `output_dir`.
      trên val 600. ⛔ Chọn theo **val 600**.
- [ ] **A7** khoá (điểm lưu, α), chấm test hai cấu hình, khai thứ bậc **trước**.
- [ ] **A8** hạt 202 **chỉ khi** A7 vượt 60,07 (~25 h A100).

---

## 4bis. ⚠️ PHÁT HIỆN 9/9 CHIỀU — mẫu số `exec` của val không bằng số bước val

`tach_val.py` chia theo **mọi** bước, còn `score_run.py:451` chỉ chấm bước **chạm**:

| lát | bước | **chạm** |
|---|---|---|
| `val400.jsonl` | 407 | **262** |
| `val600.jsonl` | 604 | **391** |

Sai số chuẩn ghép cặp ở 262 bước là ~**1,3 pp** thay vì 1,03, nên chọn argmax trên năm điểm lưu
của A6 là chọn gần như ngẫu nhiên. Ảnh hưởng **chặng 4**, không chỉ chặng 3.

✅ **Đã xử bằng `harness/mo_rong_val.py`** (0 GPU):

| lát mới | bước | chạm | episode |
|---|---|---|---|
| `val_cham400.jsonl` | 607 | **400** | 137 |
| `val_cham600.jsonl` | 960 | **602** | 209 |
| `train_tru_val.jsonl` | 63.000 | 40.189 | 12.549 |

⭐ **Ràng buộc thiết kế: val mới BAO TRÙM val cũ.** Lượt Phase 1 đang chạy trên `val400.jsonl` cũ;
nếu val mới không chứa nó thì `train_tru_val` mới sẽ chứa những bước Phase 1 đã dùng để chọn α, và
hai chặng không còn so được với nhau. Script có `assert` cho điều này, cùng bốn phép kiểm rò rỉ khác.
⛔ Đổi val thì **phải dựng lại** `branches_tru_val`, nếu không cấu hình VIS-SFT vẫn trỏ bộ cũ.
⚠️ Lượt Phase 1 đang chạy **không bị ảnh hưởng** — nó dùng `val400.jsonl`, tệp đó không đổi.

---

## 5. Việc treo, không thuộc chặng nào

- [ ] **FAIR #276** — báo kết quả **15/9**, hội nghị 8–9/10. EDAS vẫn `Pending (no manuscript)`;
      nếu tới 15/9 không có hồi âm của PGS.TS. Trần Văn Lăng thì hỏi lại lần nữa. Kèm: sửa last
      name của thầy trên EDAS (`Nguyen` → `Long`), thống nhất affiliation.
- [ ] `\Khoa` trong `thesis/main.tex` vẫn là ô `\CANDIEN`, cần user điền.
