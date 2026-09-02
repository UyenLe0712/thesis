# CLAUDE.md — Bối cảnh luận văn (auto-load mỗi phiên)

> Dọn 18/8/2026. Bản đầy đủ trước khi dọn (1.263 dòng, có toàn bộ nhật ký chạy máy
> tháng 7–8 và khung prompting cũ đã bị bác): `report/_archive/CLAUDE_MD_TRUOC_DON_18_8_2026.md`
> (thư mục `_archive/` **không có trong bản GitHub** — tệp vẫn nằm trên máy và trong lịch sử git).
> Mở file đó khi cần tra *"vì sao hồi đó quyết định X"*, không phải để biết trạng thái hiện tại.

**Trao đổi bằng tiếng Việt.** Văn phong: xem mục cuối file.

---

## 🗂️ Bản đồ kho

`README.md` ở gốc kho = bản đồ thư mục (tái cấu trúc 16/8/2026).

| thư mục | chứa gì |
|---|---|
| `harness/` | mã dựng dữ liệu, train, sinh câu, chấm điểm, runbook Colab/Kaggle |
| `report/` | ghi chú và báo cáo đánh số; `report/papers/` = ghi chú tài liệu tham khảo |
| `runs/` | kết quả chấm — ba nhánh chính ở gốc, `gate_a/` · `paraphrase/` · `floor/` · `venus/` (chưa chạy) |
| `paper/fair2026/` | bài FAIR (LaTeX, IEEEtran) |
| `thesis/` | luận văn LaTeX |
| `slides/` | `LUAN_VAN_SLIDE.pptx` (trình thầy) · `LUAN_VAN_SLIDE_BAOCAO.pptx` + `KICH_BAN_BAO_VE.md` (bảo vệ) · `VCL2026_SLIDE.pptx` + `KICH_BAN_VCL.md` (hội nghị VCL) · `build/` · `latex/` |
| `_bundles/` | gói zip mang lên Colab/Kaggle (`make_bundle.py` dựng lại được) |

`harness/` và `report/` **giữ nguyên tên** (597 và 1991 tham chiếu; layout gói zip mà runbook
Colab phụ thuộc cũng dùng tên `harness`).

**Luật đọc kết quả:** tải từ Kaggle về **đặt thẳng vào thư mục của phép đo đó**
(`runs/README.md` ghi rõ). Đã có lần bốn tệp lạc vào `report/papers/`, mất một lượt dọn.

## 📚 Đọc file nào

| cần biết | mở |
|---|---|
| **⭐ TRẠNG THÁI HIỆN TẠI — đọc một mình là hiểu, từ 23/8 trở đi** | **`report/119_TRANG_THAI_SAU_23_8.md`** |
| **đi hướng nào tiếp — tranh luận + tiền lệ + phán quyết (25/8)** | **`report/120_TRANH_LUAN_HUONG_TIEP.md`** |
| kế hoạch tháng 9 (bản chép từ ảnh, phủ tới §3.4 — ⛔ **`126` thắng file này khi mâu thuẫn**) | `report/123_CHOT_CUOI_PIPELINE_CHEP_TU_ANH.md` |
| **tuần 1 tháng 9: đã chạy tới đâu, chặn ở đâu** | **`report/125_TUAN_1_THANG_9.md`** |
| **⭐ PHÁN QUYẾT CUỐI 30/8 — phương pháp, backbone 3B, 6 lượt, VÀ chốt không đổi thước** | **`report/128_CHOT_PHUONG_PHAP_VA_THUOC_30_8.md`** |
| quyết định train tháng 9 bản Mac (⛔ `128` thắng ở backbone + phạm vi lượt) | `report/126_TRA_LOI_MAC_30_8.md` |
| cơ chế kỹ thuật toàn dự án, từ đầu | `report/112_HIEU_TOAN_BO_KY_THUAT.md` |
| đang ở đâu (bản đồ CŨ, trước 23/8) | `report/109_BAN_DO_HIEN_TAI.md` |
| phải làm gì (đăng ký trước, đã niêm phong) | `report/106_DANG_KY_TRUOC.md` |
| đã đo được gì, số nào tin tới đâu, số nào đã rút | `report/108_DA_LAM_DUOC_GI.md` |
| **quyết định đang có hiệu lực về train gì** | **`report/117_QUYET_DINH_MIN_DESC.md`** |
| phiên debate đa-agent 23/8 (bản chép lại 27 ảnh) | `report/116_DEBATE_23_8_FINAL_SOLUTION.md` |
| **hai bài báo: trạng thái, phân số, phản biện bốn giám khảo** | **`report/118_PHAN_BIEN_HAI_BAI_23_8.md`** |
| FAIR vòng giám khảo 30/8, ba đòn CHẶN đã vá (⛔ **`129` thắng file này**) | `report/127_CHOT_FAIR_30_8.md` |
| FAIR vòng phản biện 7 agent 31/8 (⛔ **`130`+`131` thắng file này**) | `report/129_PHAN_BIEN_FAIR_31_8_OCR.md` |
| **⭐ CHỈ ĐẠO VIẾT LẠI FAIR — bản FINAL 31/8, thắng mọi tài liệu khác về bài FAIR** | **`report/130_CHI_DAO_VIET_LAI_FAIR_31_8.md`** |
| **⭐ FAIR ĐÃ VIẾT LẠI + TÌNH TRẠNG NỘP (chưa xác nhận được nhận)** | **`report/131_FAIR_VIET_LAI_VA_NOP_31_8.md`** |
| **phản biện hai bài + phán quyết từng đòn (23/8)** | **`report/118_PHAN_BIEN_HAI_BAI_23_8.md`** |
| phân tích bốn nhánh + sàn | `report/113_PHAN_TICH_BON_NHANH.md` |
| tiền lệ đã tra (executability, Zhao, GCoT) | `report/114_TIEN_LE_CAN_XAC_MINH.md` |
| nhật ký chạy máy Colab chi tiết | `report/110_PHIEN_0_COLAB_11_8.md` |
| script trình bày với thầy | `report/111_SCRIPT_GAP_THAY_12_8.md` + `slides/LUAN_VAN_SLIDE.pptx` |
| nguồn từng con số trong bảng trích từ bài khác | `report/105_NGUON_SO_BANG_GOC.md` |
| cách chia hai bài báo | mục *Hai bài báo* trong file này — ⛔ **KHÔNG** dùng `report/KE_HOACH_2_BAI_BAO.md`, bản đó đã chết |

Mâu thuẫn thì: **mã** thắng tất cả về *hệ thống đang thực sự làm gì* · `106` thắng về *estimand
và ngưỡng đã khoá* · **`119` về *trạng thái hiện tại và số hiện hành*** · `117` về *vì sao chọn
MIN-DESC* · `108` về *đã đo được gì trước 23/8* · `112` về *cơ chế hoạt động*.
⚠️ `109` là bản đồ **trước 23/8**, số điểm trong đó đã bị `119` thay. `116` chỉ là bản chép lại phiên debate — phần *"sẽ train gì"*
của nó **đã bị `117` thay**.

---

## ⭐ TRẠNG THÁI 23/8/2026 — NHÁNH S2 **DỪNG** · ĐÓNG GÓP MÔ HÌNH NAY LÀ **MIN-DESC**

| trần **75,7** | **MIN-DESC 60,0** | **CE2-S2 59,4** | S1/202 **59,6** | S1/101 **59,1** | S2/101 **57,2** | Base **47,6** |

⭐ **`Δ_component` = MIN − CE2 = +0,63 pp** (p=0,011, KTC [+0,16 · +1,10]) — **có ý nghĩa trên nhiễu THƯỚC nhưng dưới MDE 2,11 pp** của thiết kế một hạt giống, và chỉ bằng 1,4× σ giữa hạt giống (0,46) ⇒ ô **TRẮNG**. Quy công: S2→CE2 **+2,24** (SFT thuần) · CE2→MIN **+0,63** (riêng ORPO) ⇒ **78% mức tăng thuộc đối chứng**. Chi tiết `report/106` mục (x12).

⭐ **MIN-DESC/101 = 60,049% (25/8 · làm tròn một chữ số là 60,0 — con số 60,1 từng dùng là do
làm tròn hai lần, đã sửa 30/8)** — cao nhất trong mọi nhánh đã train, nhưng **so S1/101 chỉ
+0,94 pp, p=0,11, KTC [−0,09 · +2,05], dưới MDE 2,2** ⇒ ô **TRẮNG**. `hit_voronoi` thuần **60,4
vs S1 60,2** ⇒ khả năng trỏ **ngang** SFT trơn; cái hơn S2 là sửa thiệt hại của chính S2.
🔬 **Chỗ nghẽn đã định vị (`report/106` mục x10b):** khi ô khai báo ĐÚNG (60,6% số bước) MIN hơn
S1 **+8,83 pp** và vượt cả trần nhóm; khi SAI thì **−11,12 pp**. Cơ chế không hỏng — nó bị chặn
bởi **độ chính xác khai báo**. Triệt tiêu được vế âm ⇒ Δ ≈ **+5,4 pp**.

Mẫu số **4.463** cho mọi nhánh (`score_run.py:516` cho câu rỗng vào quần thể với `exec = 0`;
câu *"cùng 4.462 bước"* ở các file cũ **không chính xác**).

⛔ **S2/202 SẼ KHÔNG CHẠY** — chủ luận văn quyết 23/8, lý do ngân sách (`report/106` mục **(x1)**).
Hệ quả **vĩnh viễn**, không phải tạm thời: estimand (w) không hoàn tất · `−2,19 pp` **ở nguyên dải
trắng**, không được nâng thành kết quả âm về sau · mọi phân tích S2 (kể cả chẩn đoán 4j-18 và phép
B UI-Venus) mang nhãn **thăm dò, một hạt giống** · bốn câu cấm ở `report/116` Mục 2 thành **cấm
vĩnh viễn**.

✅ **Smoke ĐÃ QUA 23/8** (`report/106` mục **(x3c)**): ORPO chạy thật · adapter S2 nạp đúng ·
không tạo reference model · chạy-tiếp-sau-mất-máy đạt · **~21 s/bước** ⇒ 800 bước ≈ 4,7 h ·
cỡ lô GPU 2 chỉ nhanh 2% ⇒ **giữ cỡ lô 1** · **LLaMA-Factory pin ở `c4e09c7cbe18…`**.
⚠️ liger **không** kích hoạt ở stage `dpo` — cấm viết "dùng liger" cho MIN-DESC.

⛔ **BIẾN THỂ MIN-ONPOLICY ĐÃ CHẠY VÀ ĐÃ CHẾT 25/8** (`report/106` mục **(x13)**). O1 sinh khai
báo của chính S2 trên 14.000 màn dạy (4,5 h A100), O2 dựng được **459 cặp** ⇒ eligibility **3,3%**,
ngưỡng khoá trước là 25% ⇒ **DỪNG, không train.** Trượt dưới **mọi** mẫu số (1,1 / 3,3 / 4,4 /
14,1%) nên không có chỗ nới. Chạy lại `--limit` lớn hơn **không cứu được** — cổng ③ là cổng **tỉ
lệ**, không phải cổng số lượng.
⭐ **Lý do đo được, đáng vào bài:** khoảng cách phần-tử-nhầm ↔ gold có **p25 70 px · trung vị 351
· p75 748** ⇒ **76,5% bước S2 sai tên nằm ngoài dải 80–350**. Lỗi khai báo của S2 **lưỡng cực** —
hoặc cùng phần tử gọi khác tên, hoặc nhìn sang vùng khác hẳn màn — **không phải lẫn giữa hai nút
cạnh nhau**. Tiền đề của on-policy giả định một dạng lẫn cục bộ mà mô hình này không mắc.
⇒ Hướng chữa bằng tương phản tinh vi hơn ở tầng khai báo **đã hết chỗ đi**.
📌 Số phụ: **S2 gọi đúng tên 68,5% trên tập DẠY** vs 60,6% tập kiểm — hai phép đo độc lập, khớp.
⚠️ Cam kết (x11d): bài **phải** báo cả ba nhánh, kể cả nhánh dừng ở cổng.
⚠️ Mã có lỗi: `build_min_desc_onpolicy.py:207` ghi cứng mẫu số 41.099 ⇒ dòng in `1,1%` là mẫu số
của một lượt chưa hề chạy. Con số thật là **3,3%**.

### ⭐ CHỐT 30/8 — SPRINT THÁNG 9: `gui_sel` vs `gui_sft_match` trên **2.5-VL-3B**, 6 lượt

Máy Mac đã mở **file gốc `123` §7.5** và trả lời trọn `report/YEU_CAU_GUI_CHAT_MAC.md` ⇒ toàn văn
+ phán quyết ở **`report/126_TRA_LOI_MAC_30_8.md`** (6 ảnh nguồn: `report/anh_123_tra_loi_mac_30_8/`).

⭐ **Phán quyết cuối 30/8 ở `report/128_CHOT_PHUONG_PHAP_VA_THUOC_30_8.md`** — file đó **thắng
`126` ở đúng hai điểm**: backbone và phạm vi lượt chạy. Mọi thứ khác của `126` giữ nguyên.

**Sáu lượt, backbone `Qwen2.5-VL-3B` (user quyết 30/8):**
· `gui_sel` / `gui_sft_match` × hạt **101 và 202** — ~46 h A100 + ~22 h Kaggle;
· **`S1-match`** × hạt **101 và 202** (cùng config, câu nhắc **không** khối ứng viên) — ~23 h + ~11 h.
Tất cả **1 epoch**, **chạy vô điều kiện**, QLoRA 4-bit, freeze vision, cutoff 3072, lr 1e-4, lô
hiệu dụng 16. `Δ = mean_2hạt[exec(gui_sel)] − mean_2hạt[exec(gui_sft_match)]`.
**Tổng ~69 h A100 + ~33 h Kaggle** (chia hai tuần), **còn nguyên 15 h đệm mất máy**.
⏸ MIN/202 + CE2/202 (~13,5 h + 11 h) là **tuỳ chọn cuối**, chỉ chạy nếu xong 6 lượt mà còn đệm.

⭐ **Vì sao thêm `S1-match`:** nó cho bảng phân rã **ba tầng, mỗi tầng đúng một biến** —
`S1-match` →[thêm menu]→ `gui_sft_match` →[thêm đầu chọn]→ `gui_sel`. Không có nó thì tầng dưới
phải so với S1 cũ vốn lệch **ba biến** (2 epoch vs 1 · cutoff 2560 vs 3072 · không menu), đúng
loại so bắc cầu mà `123` §9.1 cấm. Đây là bảng mạnh nhất khi bảo vệ nếu Δ trắng.

⛔ **`gui_orpo_hard` ĐÃ CHẾT** — câu trỏ tới nó ở `123` §2.7 là **leftover**, chính §7.5 bác. Lý do
đo được: hai nhánh ORPO **cùng có** khối ứng viên nên khối triệt tiêu trong hiệu số; và toàn bộ công
của ORPO-khó chồng SFT **đã đo rồi = +0,63 pp exec** (CE2/101 59,42 → MIN/101 60,05; `sel_acc`
65,70 → 66,55), muốn chạm ngưỡng Dương +2,8 phải gấp **4,4×**. Cộng **(x13c)**: lỗi khai báo lệch
trung vị **351 px**, 76,5% ngoài dải vế âm khó ⇒ tiền đề "vế âm khó" sai — **đúng lý do MIN-ONPOLICY
đã chết**.

⚠️ **Δ nhiều khả năng TRẮNG dù exec đẹp (kỳ vọng 63,7–65,1%) — đây là chủ đích, không phải hỏng.**
Khối ứng viên có ở **cả hai** nhánh nên Δ chỉ đo **đầu chọn tường minh**. ⛔ Bốn cách kéo Δ cho đẹp
đều bị cấm (bỏ khối khỏi đối chứng / so vs S1 / train ORPO / đổi luật Voronoi). `sel_acc` **là thước
phụ, không phải headline**.

⛔ **KHÔNG đổi backbone sang Qwen3-VL-4B** (user quyết 30/8, đảo `126`). Bốn lý do đo được:
① trần cơ chế **67,2%** bị chặn bởi **độ phủ khối ứng viên**, không phụ thuộc backbone, mà lát
chọn đúng đã bão hoà (MIN 85,2% vs người 85,7%) ⇒ đổi backbone mua tối đa **~2 pp**; ② căn cứ đổi
là ScreenSpot (benchmark **định vị**) trong khi mô hình này **không định vị** — UGround làm việc
đó; ③ giữ 3B mới có ngân sách cho `S1-match`, tức mới tách được công của menu; ④ 4B chưa từng
chạy, giờ/epoch chưa đo, kịch bản xấu 112–148 h là vỡ ngân sách.
⚠️ Chọn 3B **không phá** quyết định nào của bản Mac — `123` §8.1 đã ghi 3B là nhánh cứu chính
thức (~46 h). **G5b vẫn chạy** để lấy giờ/epoch thật, chỉ không còn dùng để quyết 4B/3B.

**Chặn thật sự hiện nay:** WSL **thiếu `train_ac/train.jsonl` + `train_ac/ocr.jsonl` bản đầy đủ**
(`report/125` mục 5) ⇒ phải kéo từ Drive trước. **G4 đo lại bằng tokenizer Qwen2.5-VL, cutoff
3072** (không còn là Qwen3-VL).

### ⭐⭐ 31/8 TỐI — FAIR VIẾT LẠI TOÀN BÀI VÀ ĐÃ GỬI, NHƯNG **UPLOAD KHÔNG KỊP** (`report/131`)

⛔ **EDAS #276 (ID 1571349424), track NLP, trạng thái `Pending (no manuscript)`.** Đăng ký kịp
trước 23:59 31/8, nhưng bấm upload lúc **00:02 1/9** thì cửa đã đóng. Đã ghi link Drive vào
*Personal notes* và **gửi email kèm PDF** cho **PGS.TS. Trần Văn Lăng (`langtv@vast.vn`,
0903 938 036 — người phụ trách nhận bài)** xin mở lại upload. ⚠️ **Chưa có xác nhận bài được
nhận** — việc kế là theo dõi hồi âm.
File đã gửi: `paper/fair2026/FAIR2026_1571349424.pdf` — **106.258 byte · 7 trang · md5
`ab60520318a8aa34e0f58bcb08f3f035`**. Mốc còn lại: **báo kết quả 15/9**, hội nghị **8–9/10** tại
ĐH Công Thương TP.HCM, kỷ yếu **IEEE Proceedings**.

⛔⛔ **ĐỒNG HỒ MÁY WSL CHẠY GIỜ UTC, LỆCH 7 GIỜ SO VỚI GIỜ VIỆT NAM.** Lúc `date` báo 16:53 thì
ở VN đã là 23:53. Cả phiên tưởng còn 7 tiếng trong khi còn 7 phút, và đó là lý do trực tiếp làm
lỡ giờ upload. ⇒ **Luật: mọi mốc hạn phải đọc bằng `TZ='Asia/Ho_Chi_Minh' date`, không đọc
`date` trần.**

**Bài sau khi viết lại (chỉ đạo `report/130`):** nhan đề **`Descriptor and Preference Targets for
GUI Instruction Generation`** · **7 trang, 0 overfull, 0 tham chiếu hỏng** · Method (`Targets and
a Stage-2 Objective`, có **công thức ORPO + `\bibitem{orpo}`**) **đứng trước** Instrument · hình
**target 3 hàng** thay sơ đồ Voronoi · Table 1 **bỏ cột `% of 75.7`**, thêm nhãn khối *Stage 2* ·
hai bảng mới ở §V (**phép bơm lỗi 1.000 lượt** và **năm luật chấm**) · keywords bỏ
`reference-free`, thêm `preference tuning`/`executability`.

⭐ **Số mới đo, chưa từng có ở đâu** (tokenizer Qwen2.5-VL trên đủ 22.854 cặp, kiểm chéo hai lượt):
độ dài token accepted **44** vs rejected **45** (p5–p95 đều 37–58) · `|Δ|≤2` token **62,8%** ·
đuôi câu trùng token **22.854/22.854** · chuỗi dài nhất **2.002** token ⇒ **0 cặp bị cắt** ở cutoff
2.560. Và từ mã đã pin: **trainer ghép cặp zero mọi dropout lúc dựng model**, gồm LoRA dropout
0,05 mà trainer SFT vẫn giữ ⇒ **MIN và CE2 lệch một biến không kiểm soát**, đã khai vào bài.

⛔ **Bốn yêu cầu văn phong mới của chủ luận văn** (áp cho mọi bài sau): không câu hỏi tu từ **kể cả
khi không có dấu `?`** (mệnh đề nghi vấn gián tiếp làm tiêu đề cũng cấm) · bỏ mẫu *"where…"* kiểu
"nơi mà" · **không kể lể chi phí máy** (gỡ sạch giờ A100, tên card, hạn mức, ngày huỷ lượt chạy) ·
**không nhắc bài đang bình duyệt ở hội nghị khác** (đã gỡ hết `\cite{companion}`).
⚠️ Hệ quả: thống kê nhãn ở §III FAIR nay **không còn nguồn để trỏ**.

⛔ **Lỗi in ấn kiểu mới, phải nhớ:** xuống dòng ngay sau gạch nối trong nguồn TeX làm bản in ra
**`byte- identical`** (thừa dấu cách). Đã lọt vào một bản PDF. **Không xuống dòng sau gạch nối.**

⚠️ **Cân bằng trọng tâm chưa đạt:** §IV 522 từ vs §V 840 từ; tính rộng, phần dụng cụ ≈ 1.270 từ
so với 522 của phương pháp (**2,4 : 1**). Nếu vào camera-ready thì **cắt §V ~180 từ**.

---

### ⭐ 31/8 — VÒNG PHẢN BIỆN 7 AGENT VÀ LƯỢT VÁ CUỐI CỦA FAIR (`report/129`)

Hội đồng chấm clone `598e4ff`; phán **weak reject / reject-as-Registered-Report**, còn cửa nếu
hạ pretension. Toàn văn + phán quyết từng đòn ở **`report/129_PHAN_BIEN_FAIR_31_8_OCR.md`**.
Bản trước lượt vá: `paper/fair2026/main_TRUOC_VA_PHANBIEN_31_8.tex.bak`.
Kết thúc: **8 trang · 0 overfull · 0 tham chiếu hỏng · 0 cảnh báo bookmark · PDF thật đã dựng.**

⭐ **Đòn CHẶN — `report/106` có HAI bản luật đọc, và bài in bản này rồi áp bản kia.**
· gốc 5/8 (dòng 85): Trắng = KTC phủ 0 **VÀ** \|Δ\| < MDE ⇒ S2 có KTC **[−3,06 · −0,75]**
  (cận trên âm) rơi vào ô **ÂM**.
· sửa đổi **(w) 17/8** (dòng 1268): Trắng = dải **−2,8 … +1,7**, chỉ hàng Dương/Âm mới đòi KTC
  loại 0 ⇒ S2 là **TRẮNG**.
✅ **(w) khoá TRƯỚC khi train S2** (nguyên văn mục (w)) nên dải hợp lệ — **không** phải ngưỡng
dời sau khi thấy điểm, đừng để ai đọc thành vậy. Nhưng nó khoá **sau** khi S1/Base/trần đã có
điểm ⇒ câu *"both edges fixed before any score existed"* **SAI**, đã sửa.
⇒ Cách xử: in dải làm luật chính, **khai thẳng** mệnh đề khoảng cho ra nhãn *harm*, và áp **đối
xứng** cho MIN (khoảng `[+0,16 · +1,10]` loại 0 ⇒ mệnh đề khoảng cho phép gọi *positive*, bài
ghi rõ **không** nhận). Câu *"verdict is the same under all three"* đã gỡ (sai với S2).

⭐ **Hai số mới, đo thật từ tệp thô — `harness/o_bi_loai_khoi_bang_cheo.py`** (tái lập trùng khít
bốn ô bảng chéo +5,72 / +0,54 / +1,11 / −25,20):
· **ô bị bảng chéo loại** (có descriptor, không có tên vàng để đối chiếu): **n=881, Δ=+1,48 pp**,
  KTC95 **[−1,16 · +4,10]** — ngược dấu headline nhưng phủ 0. ⚠️ Hội đồng ước *"n=893, Δ≈+1,8"*,
  **số thật thấp hơn**; dùng số của mình.
· **phần bù ô "cả hai đúng"**: **n=1.374, Δ = −13,10 pp** [−15,39 · −10,77]. ⛔ **KHÔNG phải
  −25,2** — con số đó là của riêng ô *"cả hai sai"* (n=738). Kết luận cũ gán nhầm, đã sửa.

**Ba lỗi số đã vá:** ① *"84,3% (injection study, 250 steps)"* — trên n=250 thì 84,3 và 99,7
**bất khả thi**; mẫu số thật là **250 bước × 4 góc bơm = 1.000 lượt** (`106` dòng 270) ⇒ 843/1000
và 997/1000. ② `73,6% + 22,0%` hụt **4,4%** = tầng *chỉ có ký hiệu* (30.252 / 1.809 / 9.038 =
41.099). ③ intro *"six alternative explanations"* trong khi mục §alt chỉ có **bốn**, lại là bốn
mục cho hiệu **S2−S1** chứ không phải S1−Base ⇒ thay bằng phát biểu thẳng (+8,4 pp).

**Hình thức:** title bỏ *"A Pre-Registered Ablation and the Condition Under Which It Pays"*
(⚠️ **giữ phần đầu** vì VCL đã nộp 30/8 có mục trích FAIR theo cụm đó) · gỡ sạch `\sbar` và
kéo theo gói `tikz` · cột *"vs. human level"* → **`% of 75.7`** (75,7 là điểm của **đường ống
chấm câu người**, không phải trần của con người) · sắp **Base → S1 → S2** · một số đậm 59,4 ·
`rather than` **22 → 4** · `$7.3\%$` trong tiêu đề mục bọc `\texorpdfstring` (hết lỗi bookmark).

⛔ **Cố ý KHÔNG làm:** thêm hình screenshot GUI làm Hình 1 (bài kín 8 trang cứng; ảnh dùng lại
được ở `paper/vcl2026/hinh/fig_moneo.png`) · human eval subset · sửa collider bằng stratify ·
S2r/S2-nopoint/S2/202/bộ trỏ khác họ (hội đồng xếp *"bài khác"*) · **dán abstract của Gemini
hoặc copy-editor** — chính chủ tịch hội đồng đã gạt cả hai vì chúng tái phạm đúng đòn đang vá.

### ⛔ CHỐT 30/8 — KHÔNG ĐỔI THƯỚC, KHÔNG ĐỔI BỘ TRỎ (`report/128` mục 5)

Câu hỏi *"60% khó bảo vệ, đổi bộ trỏ cho điểm cao hơn được không"* đã có **hai số bác**:
· ⚠️ **SỬA 30/8 — nhãn năm luật ở đây từng gán SAI, câu "đổi luật không nâng trần" là SAI.**
  Chạy lại `harness/rule_sensitivity.py` (lát 698 bước) cho đúng thứ tự trong mã: đĩa Euclid
  **80,2** · chữ nhật theo trục kiểu AITW **82,2** · **Voronoi đang dùng 74,2** · Voronoi hạt-tâm-hộp
  **56,6** · hộp-gần-nhất **82,2**. Vậy nới từ luật đang dùng sang luật lỏng nhất **CÓ nâng trần
  74,2 → 82,2**. Bảng ở `report/112` §5.7 đặt nhãn theo một bộ luật cũ ("chữ nhật siết 7%/3%") không
  còn khớp mã — đừng đọc bảng đó. Bài FAIR ghi đúng ngay từ đầu.
· **Cái vẫn đứng sau khi sửa:** thứ tự ba nhánh **không đổi ở luật nào**, chênh S1−Base nằm gọn
  **9,5–13,0 pp**; nới luật **nâng cả sàn**; và dưới `hit_disk` thì **MIN ngang S1 (69,2 vs 69,2)**
  ⇒ đổi luật **xoá luôn Δ**. Lập luận "không đổi thước" giữ nguyên hiệu lực, chỉ đổi chỗ dựa.
· ⭐ **Bộ trỏ mạnh hơn cho điểm THẤP hơn** — phép B đã đo: UI-Venus-7B (ScreenSpot-v2 99,0/90,0)
  thua UGround-2B (95,0/83,3) ở **cả ba nhánh** (39,06/48,74/46,60 vs 42,50/52,84/49,45) và trần
  69,3 vs 70,0. Cơ chế: thước phán bằng ngưỡng 14% trước rồi mới Voronoi, và **72% ca thước mù là
  bộ trỏ lệch >14%** tức **bỏ cuộc**, không phải trỏ nhầm nút cạnh bên. Thêm giá: 7B chấm ~14,4 h
  một lượt ⇒ ba tuần quota, và mọi số của hai bài + luận văn phải đo lại.

⭐ **Cách đúng: đổi CÁCH TRÌNH, không đổi thước.** Thước chạy từ **12,0** tới **75,7**, nên đừng
đọc 60% trên nền 100. Tỉ lệ **so trần người**: Base 62,8% · S1 **78,0%** · MIN **79,3%** ·
`gui_sel` kỳ vọng **84,1–86,0%**. Câu đi bảo vệ là *"câu do mô hình sinh ra đạt 84–86% năng lực
của câu do người viết, trên cùng một phép đo"*. Chống lưng: trần 75,7 là **giới hạn dụng cụ**
(72% ca mù do bộ trỏ lệch >14%; lọc câu chuẩn ≤3 từ trần chỉ lên 77,0); thước này **chặt hơn quy
ước lĩnh vực** (thêm một tầng: câu phải đủ để một mô hình độc lập trỏ trúng) nên **cấm so thẳng
60% với 70–80% của bài dùng thước khớp toạ độ trực tiếp**.
✅ **Được làm, 0 giờ GPU:** thêm `exec` dưới **luật chữ nhật 14% kiểu AITW** làm **thước đồng-báo**
(tính từ tệp thô), khai kèm điều kiện *dưới luật lỏng đó Δ co gần 0* ⇒ chỉ để định vị so với
literature, **không** để đọc đóng góp. Headline vẫn `exec`/`hit_voronoi`.

**▶️ VIỆC ĐANG CHỜ (1/9): theo dõi hồi âm của PGS.TS. Trần Văn Lăng về việc mở lại upload cho
FAIR #276 — bài đã gửi qua email nhưng EDAS vẫn `Pending (no manuscript)`, xem `report/131`.
Kèm theo: sửa last name của thầy trên EDAS (`Nguyen` → `Long`) và thống nhất affiliation.**
*(Việc cũ đã xong: đọc soát + nộp hai bài — VCL 30/8 · FAIR 31/8.)* Không còn lượt train
nào trong kế hoạch; đóng góp mô hình chốt ở MIN-DESC (ô TRẮNG), đóng góp còn lại là **chẩn đoán**
(bảng 2×2, hệ số chuyển đổi 0,43, quy công 78/22, và lý do on-policy không dựng được).

✅ **Train xong · suy luận xong · cổng cơ học ĐẠT** — xem `report/106` mục **(x9)**.

### MIN-DESC là gì — một đoạn

ORPO stage-2 nối tiếp từ checkpoint **S2**, trên cặp quy chiếu tối thiểu ở **tầng khai báo**:
`chosen = <desc>đúng</desc> + "\n" + câu`, `rejected = <desc>desc_neg</desc> + "\n" + câu` —
**câu y hệt**, chỉ ô khai báo đổi, nên gradient rơi đúng vào việc chọn phần tử. Đối chứng quy công
là **CE2-S2** (SFT thuần, cùng bước, cùng update). Primary `Δ_component = mean_2seed(MIN−CE2)`.
Bốn lượt × 800 update ≈ **20 h A100, ~110 đơn vị**.

⛔ **KHÔNG train `s2_nopoint`, KHÔNG train `s2r`.** Lý do đo được, không phải cảm tính — xem
`report/117` Mục 1 và 3: ô toạ độ là ô **gánh** (+1,12 pp đứng một mình) chứ không phải ô gây hại,
còn ô tên chỉ đáng +0,54; và `s2r` được thiết kế để chắc chắn thua. `s2_nopoint` lại là SFT đầy đủ
nên **đắt gấp đôi** MIN-DESC (46 h vs 20 h).

⛔ **Đừng** đổi thước · đổi luật cắt `<desc>` · chọn điểm lưu khác · nới cổng sau khi thấy số.
Dự án đã tự khai **hai lần** nới ngưỡng sau khi thấy điểm — đừng có lần thứ ba.

### 🔬 Chẩn đoán: 7,3% số bước gánh 34% chênh lệch (`report/110` 4j-18 · `harness/phan_tich_s2.py`)

Lát cắt **đăng ký trước 19/8**, trước khi có bất kỳ điểm S2 nào:

| nhóm | n | S1 | S2 | Δ |
|---|---|---|---|---|
| **CÓ** kích hoạt (sinh `<desc>`) | 4.138 | 62,2% | 60,8% | **−1,38** |
| **KHÔNG** kích hoạt | 325 | 19,7% | 10,8% | **−8,92** |

Nhóm 325 là chỗ mô hình **đoán sai loại thao tác** — viết *"swipe up"*, *"go back"* thay vì gọi
tên nút. Trần ở đó **68,3%** ⇒ bước giải được, thước không mù. ⭐ **Base gọi đúng loại thao tác
nhiều hơn CẢ HAI bản đã huấn luyện** (83,4% vs S1 55,1% vs S2 38,8%) ⇒ đây là **cái giá của
SFT**, S2 chỉ khuếch đại. Giả thuyết chưa kiểm: tập dạy chỉ gắn khai báo cho bước **chạm** nên
mô hình học tắt *"có khai báo ⇔ là chạm"* ⇒ nhánh **`s2_nopoint`** nay đáng chạy hơn hẳn.

**Bốn lời giải thích thay thế ĐÃ LOẠI:** độ dài câu (âm ở cả lát dài lẫn ngắn; phân bố hai
nhánh như nhau) · lát cắt app (âm cả ba) · lỗi `canon_action` go-back (Δ −1,93 → −1,86 khi
`strict_back`) · khai báo rác OCR (26 bước, Δ **+7,69**, p=0,63 — ngược chiều).
⚠️ Giới hạn phải khai: nhóm 325 định nghĩa bằng **hành vi của chính S2**.

### Bốn bẫy của lượt train, tái diễn mỗi lần dựng lại máy

**① Dữ liệu trên Drive là bản tiếng Việt.** Mục sửa đổi (q) ngày 14/8 đổi nhãn khai báo sang
tiếng Anh; gói `derived.tar.gz` trên Drive vẫn là bản cũ. Đã dựng lại 18/8, cất ở
`MyDrive/thesis/derived_train_en.tar.gz` (bản Việt sao lưu `branches_vi_0818/`).
⚠️ **Phiên đứt thì sau ô 2 PHẢI bung `derived_train_en.tar.gz` đè lên** — ô 2 bung
`derived.tar.gz` là bản CŨ, quên bước này là train trên dữ liệu khác mà log không báo gì.
Kiểm ba phép đã đạt: 0 tiếng Việt ở khuôn mẫu · 9/9 bất biến · s2r ghép độ dài token 99,9%.
`total_flos` bản Anh 10.812.978 vs bản Việt 10.816.688, lệch **0,03%** ⇒ đổi ngôn ngữ không đổi
độ dài chuỗi, xác nhận (q) là thay đổi thuần từ vựng bằng một con số độc lập.

**② Ô thăm dò PHẢI `shutil.rmtree("/content/probe_s2long")` trước.** Không xoá thì
LLaMA-Factory chạy tiếp từ checkpoint cũ, **nhảy qua** 20 bước rồi chạy đúng một bước: log vẫn
in `Training completed`, vẫn có `total_flos`, trông y như đạt. Đọc bằng **hai con số**:
`train_runtime` ~220 s (không phải ~15) và loss ~2,4 (không phải ~0,1).

**③ "Connecting" / "Not connected to runtime" trên trình duyệt KHÔNG phải máy chết.** 18/8
tưởng đứt và suýt dựng lại; `elapsed_time` 6:24:50 cho 2.260 bước = 10,22 s/bước, khớp liền
mạch từ bước 0 trong 0,2% ⇒ chưa hề đứt. Bằng chứng thật: PID còn sống, hoặc thư mục điểm lưu
trên Drive có bản mới trong **~34 phút** (200 bước × 10,2 s). Theo dõi bằng Terminal Colab hoặc
mở Google Drive từ điện thoại, không cần nhân Python.

**④ Tên trường thật trong `trainer_log.jsonl` — ĐỔI THEO PHIÊN BẢN, phải kiểm lại mỗi lần dựng máy.**
· Stack tháng 8 (lượt S1/S2): `current_steps` · `total_steps` · `loss` · **`lr`** · `epoch` ·
  `percentage` · `elapsed_time` · `remaining_time`.
· ⚠️ **Khác nhau theo STAGE, không theo phiên bản** — đo 24/8 trên cùng một máy:
  · stage **`dpo`** (MIN-DESC): CHỈ SÁU trường — `current_steps` · `total_steps` · `epoch` ·
    `percentage` · `elapsed_time` · `remaining_time`. **KHÔNG có `loss`, `lr`, `rewards/*`.**
  · stage **`sft`** (CE2-S2): **CÓ** thêm `loss` và `lr`, đúng như stack tháng 8.
  ⇒ Ô theo dõi nào lọc dòng theo `loss` sẽ **vứt sạch mọi dòng** ở nhánh `dpo` rồi in *"chưa có
  bước nào"* suốt cả lượt train mà không hề báo lỗi — còn ở nhánh `sft` thì chạy bình thường,
  nên lỗi này **chỉ lộ ra ở một nửa số lượt**.
· ⇒ `loss` / `learning_rate` / `rewards/*` chỉ có ở **stdout**, tức tệp `.log`. Ô theo dõi của
  `colab_train_min_desc.md` đọc **hai nguồn**: tiến độ từ `.jsonl`, số học từ `.log`.
**Không có `grad_norm`** trong jsonl — trường đó chỉ ở dòng stdout.
⚠️ `elapsed_time`/`remaining_time` hỏng sau khi chạy tiếp; ô theo dõi tự tính bằng mốc neo.
Đã kiểm `lr` chạy đúng lịch: bước 2.260, cosine tính 8,622e-05, trainer ghi 8,624e-05 (0,02%).

**Ô 7b tiền bay — bảy phép kiểm 10 giây trước khi bấm train:** cfg đúng nhánh · không sót
`max_steps` · `output_dir` rỗng · 64.567 mẫu · 0 tiếng Việt · **đường dẫn ảnh mở được** (sai
prefix thì chết SAU 42 phút mã hoá token) · đĩa ≥20 GB · ~8.072 bước.
⚠️ Ô 7b in **8.071** do làm tròn; trainer chạy **8.072** (`ceil(64.567/16)=4.036` ×2).

---

## ▶️ VIỆC KẾ — một danh sách duy nhất, thứ tự theo giá

Mọi danh sách "việc kế" cũ rải rác trong file đã bị danh sách này thay.

0. ✅ **XONG 24/8 — train cả hai nhánh hạt giống 101 + sinh câu đủ 6.958 bước.**
   `runs/preds_min_desc_seed101.jsonl` · `runs/preds_ce2_s2_seed101.jsonl`, mỗi tệp 6.958 bản
   ghi, một chữ ký, phủ đủ 4.463 bước chạm, 0 câu sót `<desc>`.
1. ✅ **Cổng cơ học ĐẠT 25/8** (`report/106` mục **x9a**) — S2 **53,9** · CE2-S2 **59,8** ·
   MIN-DESC **60,6** trên 3.473 bước có tên vàng. Mốc S2 tái lập trùng con số ghi 23/8.
   ⚠️ **Quy công:** CE2−S2 **+5,90** (SFT thuần) · MIN−CE2 **+0,80** (phần riêng của ORPO) ⇒ 87%
   mức tăng là của nhánh đối chứng. Cấm trình +6,77 như công của mục tiêu ưu tiên.
2. **▶️ ĐANG LÀM: chấm UGround trên 4.463** cho hai checkpoint, `harness/kaggle_cham_min_desc.md`.
   **Hai commit tách rời.** Trước khi bấm Commit: Internet ON · Accelerator GPU T4×2 ·
   `thesis-preds` đã lên version mới · notebook chỉ còn **một** ô 2.
3. **Sau khi có điểm** mới quyết chi ~8 h GPU cho hạt giống 202. Quyết chạy thì phải chạy **cả
   hai** nhánh và **báo trung bình hai hạt giống bất kể nó ra sao** — cam kết **(x8c)**.
4. **Chấm UGround một lần** trên 4.463 cho bốn checkpoint (22,4 h Kaggle, vừa quota một tuần)
   → tính `Δ_component` và `Δ_system` theo `report/106` mục (x5).
5. ✅ **Bài FAIR + VCL: phiên song song 23/8 đã viết xong** — FAIR **8 trang 0 overfull** (nay là
   **bài mô hình**), VCL **9 trang** tiếng Việt. Phản biện bốn giám khảo ở `report/118`.
   Việc còn lại là đọc soát + nộp, **không** phải cắt trang.

✅ **Smoke ORPO ĐÃ QUA 23/8** — không phải chạy lại. Bằng chứng ở `report/106` mục **(x3c)**.

⛔ **Đã bỏ khỏi danh sách, có lý do đo được:** train s2/202 (quyết 23/8) · `s2_nopoint` ·
`s2r`. Xem `report/117` Mục 3.
4. ✅ **Phép B ĐÃ XONG 20/8 — đòn "UGround quen văn phong AC" ĐÃ ĐÓNG.**
   Chấm lát 2.532 bằng `UI-Venus-Ground-7B` (sạch AndroidControl), cả ba nhánh, 8,15 giờ
   Kaggle. Đọc bằng `python3 harness/phan_tich_venus.py`; runbook `harness/kaggle_phepB_uivenus.md`.

   | phép so (lát 2.532) | UGround | UI-Venus |
   |---|---|---|
   | **S1 − Base** (chứng nhân) | **+10,35** [+8,39 · +12,40] | **+9,68** [+7,60 · +11,78] |
   | **S2 − S1** (quy về 4.463) | **−1,93** [−3,08 · −0,78] p=0,0005 | **−1,21** [−2,30 · −0,12] p=0,026 |

   · ⭐ **Chứng nhân giữ 94%** ⇒ thang đo **không bị nén**, Δ đọc được — bẫy pha loãng không
     xảy ra. Trần cổng A: UI-Venus **69,3%** [63,8–74,8] vs UGround **70,0%** [64,5–75,3].
   · ⭐ **S2 thua dưới CẢ HAI dụng cụ**, mép trên KTC đều dưới 0 ⇒ *kết quả âm, tái lập qua hai
     bộ trỏ độc lập*. Đây là hàng 1 của bảng bốn kết cục đã khoá trước khi chạy.
   · ⚠️ **VẪN CHƯA ĐƯỢC KẾT LUẬN** — luật `report/106` (w) đòi **trung bình hai hạt giống**, mà
     S2 mới có hạt 101. Phép B đóng đòn *dụng cụ*, **không** thay được hạt giống thứ hai.
     ⚠️ Câu *"train s2/202 vẫn phải chạy"* ở đây **đã hết hiệu lực** từ 23/8 — nhánh S2 dừng,
     xem `report/106` mục (x1). Kết quả phép B giữ nguyên giá trị, chỉ đổi nhãn thành *thăm dò*.
   · ⭐ **Phép rút gọn lát tự kiểm ĐÚNG TUYỆT ĐỐI:** lát 2.532 quy về 4.463 cho −1,9270 pp,
     tính thẳng trên 4.463 cũng −1,9270 pp, b/c trùng 340/254.
   · ⭐ **Sai số khoảng cách KHÔNG dự đoán được trần:** UI-Venus thua rõ ở khoảng cách (trung vị
     1,56% vs 0,73%, p75 16,35% vs 9,08%) nhưng trần chỉ kém 0,7 điểm — vì thước quyết định
     bằng ngưỡng 14% rồi mới Voronoi. Dùng lại được cho mọi lần đổi dụng cụ.
   · 🔬 **Thăm dò (hậu kiểm, KHÔNG đăng ký trước — phải gắn nhãn thăm dò nếu vào bài):**
     hiệu-của-hiệu ghép cặp trên đúng 2.532 bước, Δ(S2−S1) dưới UI-Venus **+1,26 pp** so với
     dưới UGround, KTC95 **[+0,04 · +2,51]** — mép dưới vừa chạm 0 ⇒ *có dấu hiệu* UGround
     phạt S2 nặng hơn chút, bằng chứng **yếu**. ⛔ Không mở được cửa "UGround thiên vị nên S2
     thua": nếu vậy Δ dưới UI-Venus phải về 0 hoặc dương, đằng này vẫn âm có ý nghĩa. Và một
     phần chênh là **cơ học** — UI-Venus đo thấp hơn 2,8–4,1 pp ở mọi nhánh nên mọi hiệu đều
     co (tỉ lệ: −6,4% vs −4,4%). ⛔ **UI-Venus KHÔNG "cho số đẹp hơn"** — nó cho điểm THẤP hơn
     ở cả ba nhánh (base 39,06 vs 42,50 · s1 48,74 vs 52,84 · s2 46,60 vs 49,45).
   · ⚠️ Cỡ ảnh **3.354 tok OOM trên T4×2**; chốt **1.272 tok** vì KTC hai trần chồng nhau ⇒
     chọn cỡ **nhanh nhất** (4,0 s/bước), phải khai đúng vậy trong bài.

5. ✅ **MÌN ĐÃ GỠ 29/8** — `test_ac/descriptors.jsonl` nay là bản tiếng Anh (bản Việt giữ ở
   `descriptors_VI_0809.bak.jsonl`). So từng bước bản cũ↔mới trên 4.448 bước: `name` ·
   `point_norm` · `tier` · `name_src` · `box` · `dup_name` · `same_role` **lệch 0**, chỉ `role`
   và `hint` đổi ngôn ngữ ⇒ **không con số nào đã công bố phải sửa**. Chi tiết `report/125` mục 1.

**Ràng buộc tài nguyên:** Kaggle **30 giờ GPU/tuần** (mỗi lượt chấm 5,6 giờ ⇒ tối đa 5
lượt/tuần, đừng dồn). Đơn vị Colab: **đếm lại trong phiên**, con số ghi trong file lỗi thời rất
nhanh. Dataset Kaggle đã dựng: `thesis-score` (1,69 GB, 4.463 ảnh) và `thesis-preds` (805 KB).

---

## 📊 SỐ ĐANG DÙNG

Tất cả chấm bằng UGround trên **cùng 4.462 bước chạm** (1 bước bị bỏ vì câu rỗng, cùng một bước
`(18710, 1)` ở cả hai hạt giống ⇒ ghép cặp McNemar sạch).

| nhánh | executability | KTC95 | hit_voronoi thuần | action_ok |
|---|---|---|---|---|
| Câu chuẩn của người (trần) | **75,7%** | [74,1 – 77,3] | 75,8 | 100 |
| S1 hạt giống 101 | **59,1%** | [57,3 – 60,8] | 60,2 | 94,4 |
| Mô hình gốc (Base) | **47,6%** | — | 48,9 | 96,5 |

· McNemar đều p<0,001: S1−Base **+11,5 pp** (χ²=243) · Human−S1 **+16,6 pp** (χ²=580, c=843
bước người trúng mà S1 trượt ← đúng vùng S2 nhắm) · Human−Base **+28,1 pp**.
· **Hai hạt giống:** S1 hơn Base **+11,52 / +12,03 pp**; nhiễu giữa hạt giống **0,52 pp** ⇒ tín
hiệu gấp **22×**. `total_flos`/bước **513.164 vs 513.229 (0,013%)**.
· **MDE thật 2,2 pp** (bootstrap cụm, SE 0,79 pp, hệ số nở do cụm chỉ **1,10×**). Con số ước cũ
2,7–4,5 pp đã rút.
· **Cổng A ĐẠT:** sai số bộ trỏ trung vị **0,7%** (ngưỡng 3%); G hiệu dụng tập kiểm **454,3**.
Sai số **theo từng nhánh 0,67 / 2,00 / 7,82** ⇒ cổng A chỉ chứng nhận cho nhánh trần.

### Sàn của thước (đo 18/8, Kaggle, lát 800 bước, trần trên lát 74,9%)

| nhánh | câu thành gì | điểm | KTC95 |
|---|---|---|---|
| `f1_trong` | `"Tap the button."` mọi bước | **12,0%** | [9,7 – 14,4] |
| `f3_lechman` | câu **thật** của bước khác — đúng văn phong, **sai màn** | **6,1%** | [4,5 – 7,9] |
| `f2_khongten` | giữ vị trí, **bỏ tên** | 68,0% toàn lát · **61,1%** phần bị đụng | — |

· **Dải dùng được 62,9 điểm** (không phải 74,9, cũng không phải 35,7 như kịch bản xấu). Vị trí
trong dải trên lát này: Base **58,3%** · S1 **74,4%**.
· ⛔ **Dự đoán "sàn ≈40%" của phản biện BỊ BÁC.** Nó suy từ việc 40,0% số bước (1.784/4.463 — sửa 31/8, số 40,4% cũ SAI) mà Base, S1 và TRẦN cùng
trúng. **Suy sàn từ tỉ lệ đồng thuận là suy sai.**
· ⭐ `f3` (6,1%) **thấp hơn** `f1` (12,0%), hai KTC không chồng lấn ⇒ **đòn nhiễm văn phong bị
giết bằng số**: câu văn phong hoàn hảo mà sai nội dung ăn thấp nhất trong mọi thứ đã đo. Bộ trỏ
thật sự đọc câu. Cộng phép "cùng nội dung khác văn phong" (+0,9…+1,9 pp, không ý nghĩa), giả
thuyết văn phong bị đánh từ **hai hướng độc lập**.
· ⭐ **Gọi tên đắt gấp 8 lần chỉ chỗ:** bỏ **TÊN** giữ vị trí **−28,5 pp** (193 bước, b=58 c=3,
χ²=47,8, p<0,001) vs bỏ **VỊ TRÍ** giữ tên −3,5 pp (198 bước, b=8 c=1, p=0,046). Hai quần thể
gần bằng nhau nên so trực tiếp được ⇒ chữ **"Element Identification"** ở nhan đề **ĐÚNG**.
⚠️ Con số của bài là **−28,5 pp trên PHẦN BỊ ĐỤNG**, không phải −6,9 pp toàn lát — `f2` chỉ đụng
24,1% số bước, pha loãng 4,15 lần.
Đọc bằng `python3 harness/doc_san.py`; luật đọc khoá trước ở `harness/make_floor.py`.

### Phép diễn đạt lại (17/8, trên câu chuẩn của người, lát 800)

| biến thể | đổi gì | phần bị đụng | executability | McNemar |
|---|---|---|---|---|
| `p1_verb` | động từ thao tác | 725 bước (90,6%) | 76,8 → **77,0** | b=13 c=14, p=1,000 |
| `p2_order` | trật tự câu | 211 bước (26,4%) | 89,6 → **90,0** | b=0 c=1, p=1,000 |
| `p4_both` | `p1`+`p2` cùng lúc | 203 bước (25,4%) | 90,1 → **91,1** | b=0 c=2, p=0,480 |
| `p3_nopos` | **bỏ** mệnh đề vị trí | 198 bước (24,8%) | 89,4 → **85,9** | b=8 c=1, **p=0,046** |

**Con số đi vào bài:** ba biến thể bảo toàn nghĩa (`p1`·`p2`·`p4`) = **1.139 bước viết lại · 30
bước đổi chiều (2,6%)** · hiệu ròng **+0,35 pp**, KTC95 **[−0,59 · +1,29]** ⇒ mép dưới loại được
mọi mức tụt > 0,6 pp. Đọc bằng `python3 harness/phep_a_ghep_cap.py` — **đừng** đọc
`score_para_*.json` trần, con số tổng bị pha loãng 3,8 lần.
· **Cơ chế: hỏng tất-cả-hoặc-không.** Bỏ mệnh đề vị trí không làm trung vị sai số nhích
(0,24% → 0,24%) mà làm đuôi bung: p90 **6,88 → 31,16**, p95 **27,54 → 62,38**.
· ⚠️ Phần bị đụng là phần **dễ nhất** (trần 89,6% vs 74,9% toàn lát). Bỏ vị trí ở câu khó có thể
đắt hơn, **chưa đo**.
· ⚠️ **Câu chữ:** viết *"bộ trỏ bền trước việc đổi động từ và đổi trật tự câu"*. **CẤM** viết
*"bền trước diễn đạt lại"* — Jandial et al. đổi *cách mô tả phần tử*, nặng hơn hẳn; `action_ok`
giữ 100% ở cả ba biến thể ⇒ phép viết lại này không đụng phần bộ trỏ phải giải. Và **CẤM** dùng
hàng *"paraphrase 0,0%"* của bảng bơm lỗi để phản bác họ — bộ bơm lỗi không gọi bộ trỏ lần nào.
Chi tiết: `paper/fair2026/PHEP_A_DIEN_DAT_LAI.md` · cơ chế: `report/112` §6.7.

### Lát cắt và độ bền

· **Năm luật chấm khác nhau** (`harness/rule_sensitivity.py`, 698 bước): trần trôi **56,6 →
82,2%** nhưng **thứ tự ba nhánh không đổi ở luật nào**, chênh S1−Base nằm gọn **9,5–13,0 pp** —
lá chắn mạnh nhất của chương đo lường.
· **Thước tất định:** cùng chuỗi + cùng ảnh ⇒ cùng toạ độ, **0 bất đồng trên 1.625 phép so** qua
bốn lượt độc lập khác thứ tự và cách gom lô ⇒ loại luôn khả năng kết quả phụ thuộc lô hay thứ tự.
· **κ 0,867** toàn tập, **0,650 có điều kiện** trên 1.652 bước viết khác nhau — luôn trình kèm
điều kiện.
· **Không lợi thế sân nhà:** app đã-thấy **59,1%** (n=1.737) · chưa-thấy **59,0%** (n=78) ·
không-gán-được **59,1%** (n=2.648 — sửa 31/8, đo lại từ `runs/score_s1_seed101_raw.jsonl`; số 59,2/2.647 cũ SAI). **95,6% app tập kiểm cũng có ở tập dạy**, nhưng 3.828/6.958
bước (55%) **không gán được app** = *không biết*, cấm đọc thành *chưa thấy*.
· **Thiên vị câu dài 5,4 pp** (câu >33 ký tự 61,9% vs ≤33 là 56,5%). Base dài trung vị 71 ký tự,
S1 chỉ 33 ⇒ thiên vị nghiêng về Base ⇒ **S1 > Base là kết luận mạnh**. S2r kiểm soát độ dài
*tiền tố*, không kiểm soát độ dài *câu ra* ⇒ **bắt buộc phân tầng độ dài khi đọc S2**.
· **Thước mù 24,3%:** 1.083 bước câu người cũng trượt, 72% do bộ trỏ sai >14% bề ngang. Sai số
lưỡng cực (trúng 0,4% · trượt 26,2%). 935 bước (21%) mà Base, S1 và **TRẦN** cùng trượt (⚠️ KHÔNG phải ba nhánh mô hình: Base+S1+S2 cùng trượt là 1.390) ⇒ **trần 75,7% là
giới hạn DỤNG CỤ, không phải của ngôn ngữ.**
· **Chỗ hỏng đúng chỗ S2 nhắm:** trong 1.825 bước S1 trượt, chỉ 252 do sai thao tác, **1.573
(86%) là thao tác đúng mà bộ trỏ không tìm ra nút** ⇒ lỗi ở cách gọi tên/tả phần tử.

### Dữ liệu

**Dạy:** 64.567 bước / 41.191 chạm (63,8%) / 12.895 tác vụ · OCR phủ 100% và qua kiểm chéo máy ·
nhãn khai báo khớp cả 5 số tham chiếu dưới 1 điểm · **9/9 bất biến** · **rò rỉ dạy-kiểm = 0** ·
phép ghép hai kho HF đúng (48% vs đối chứng lệch 20%, n=400).
**Kiểm:** 6.958 bước / 4.463 bước chạm / 1.432 tác vụ · **139 bước chưa-thấy app (22 app)**.
`history` trong câu nhắc **là câu chuẩn do người viết** ở các bước trước (trùng nguyên văn
5.318/5.318) ⇒ khâu chấm là **teacher-forced trên ngữ cảnh**, mọi số tuyệt đối đọc kèm điều kiện đó.

**Nguồn:** ghép hai kho HuggingFace theo `(episode_id, step_id)` —
`HarrytheOrange/parsed_AndroidControl` (câu người viết cho cả 15.283 episode + `all_forest_dict.zip`
= cây trợ năng 99.131 màn) với `ckg/AndroidControlParsedWithImages-20k` (ảnh).
⚠️ Bản `ckg` đã parse thành định dạng agent nên **mất `step_instructions`** — đừng dùng làm nguồn dạy.
⚠️ Cây trợ năng có trung vị 86 phần tử/màn nhưng **chỉ 12,6% có tên** ⇒ chỉ dùng cho vị trí, không
thay được OCR ở khâu lấy tên.
AndroidControl gốc = Li et al., Google DeepMind, **NeurIPS 2024 D&B** (arXiv 2406.03679, CC0).

### ⛔ Số đã rút — cấm dùng lại

| số cũ | thật ra | vì sao |
|---|---|---|
| trần **70,0%** | **75,7%** | đo trên mẫu con 300, đo lại đủ 4.462 bước 15/8 |
| `total_flos` **3.857.778.344 GF** | **4.142.257.957 GF** (513.164/bước) | đọc sai; lập luận "khớp ngoại suy 0,32%" còn **vòng tròn** |
| MDE **2,7–4,5 pp** | **2,2 pp** | hệ số nở do cụm 1,10× chứ không phải 1,5–2× |
| bộ trỏ trượt **84%** khi đổi diễn đạt | 84% = **năng suất của một agent đối kháng** trên desktop | xem mục Tiền lệ |
| "UGround sạch, không có AndroidControl" | **SAI**, Bảng 1 có AC 47K | xem mục Giới hạn |
| "bộ trỏ khác họ mô hình được chấm" | **SAI**, UGround-V1-2B dựng trên Qwen2-VL | như trên |
| trung vị sai số trỏ **8% cạnh** | **15,0%** (`ground_pilot`) / **29,3%** (công thức cổng A) | hàm cũ chỉ lấy sai số của ca ĐÃ TRÚNG |
| app_seen: **604 bước** chưa-thấy | **139 bước / 22 app** | chạy bằng bản mã có lỗi regex |
| "12,6% phần tử có tên, **đo trên 99.131 màn**" | đo trên **120 màn ngẫu nhiên** trong kho 99.131 màn (22/120 màn không có phần tử nào có tên) | `report/100:200` + `harness/a11y_inventory.py:11`. Đã vá ở VCL 29/8; ✅ FAIR cũng đã vá 29/8 (câu *"across the 99,131 trees"* từng bị **thêm lại** vào bản nháp rồi gỡ) |
| room **485 bước (10,9 pp)** | **741 bước (16,6 pp)** | kéo theo trần 75,7 |
| dự báo sàn loss 0,548 | — | ngoại suy hàm mũ không mô hình hoá được nhịp epoch 2 |
| **89,6%** là mức nền của **ba** lát diễn đạt lại | **chỉ của lát `p2_order` (211 bước)**; lát `p1_verb` (725 bước) chỉ **76,8** ⇒ dải đúng là **76,8–90,1** | sửa 31/8, đối chiếu bảng phép diễn đạt lại ở mục dưới |
| **71,0%** ô point S2 trúng cửa sổ 14% | **bỏ khỏi bài** — không truy được mẫu số | `report/117:38` ghi "cùng nguồn" nhưng nguồn là bảng n=3.240, còn bài dùng phân hoạch 3.245/4.126 ⇒ gắn n nào cũng là suy ngược |
| phrase trùng tập trung ở **2,6%** số bước train | **bỏ khỏi bài** (17,3% thì giữ) | chỉ truy được tới ghi chú khẳng định, không script, không tệp đo; `train_ac/train.jsonl` không có trên WSL |
| `hit_disk` của S2 = **67,5** (`report/119:62`) | **67,44** | số thật trong `score_s2_seed101.json`; **bài in đúng, ghi chú sai** |

Danh sách đầy đủ + 24 lỗi đã bắt: `report/108`.

---

## 📰 HAI BÀI BÁO — trạng thái 29/8/2026

**Nộp cả hai, cách nhau một ngày: VCL 30/8 · FAIR 31/8.**

### Cách chia — chốt 23/8, đang có hiệu lực

⛔ **Không còn bài nào lấy THƯỚC ĐO làm đóng góp chính.** FAIR từng là bài thước đo cho tới
23/8; chủ luận văn quyết viết lại thành **bài mô hình** vì FAIR là venue khó hơn. Bản
thước-đo cũ giữ nguyên ở `paper/fair2026/main_v1_metric_backup.tex`.

| | **FAIR'2026** | **VCL2026** |
|---|---|---|
| đóng góp chính | **MÔ HÌNH** | **NHÃN QUY CHIẾU + đường ống dựng dữ liệu** |
| nhan đề | ***Descriptor and Preference Targets for GUI Instruction Generation*** (đổi 31/8, `report/130` mục 2) | *Sinh hướng dẫn sử dụng phần mềm từ ảnh chụp màn hình và mục tiêu người dùng: xây dựng nhãn quy chiếu tự động khi phần tử giao diện không có tên để gọi* |
| trạng thái bản dựng | **7 trang, 0 overfull** (31/8, sau lượt viết lại theo `report/130` — chi tiết `report/131`) | **19 trang, 0 overfull** (29/8, sau khi áp template chính thức) |
| ngôn ngữ | tiếng Anh | tiếng Việt |

⚠️ **Thước đo nay nằm BÊN TRONG FAIR, ở §V *The Instrument*** — đổi vai từ *đối tượng nghiên
cứu* thành *dụng cụ đã hiệu chuẩn*, nén còn một mục rưỡi. **§V không phải phần đóng góp**;
phần đóng góp là §IV, §VI, §VIII. Đã có lần đọc lướt mục cũ của file này rồi tưởng nhầm
"một bài model, một bài thước đo" — chính vì vậy mục cũ đã bị xoá thay vì để lại kèm nhãn.

Phản biện bốn giám khảo + phán quyết từng đòn: **`report/118_PHAN_BIEN_HAI_BAI_23_8.md`**
(Mục 0 giữ bảng phân số đang dùng). Bảng 2×2 kèm cột Base và cột TRẦN: `harness/phan_tich_o_khai_bao.py`.

### Venue

| | **FAIR'2026** | **VCL2026** |
|---|---|---|
| tên đầy đủ | — | **Hội thảo Quốc gia lần 4 về Ngôn ngữ học Tính toán** |
| ngày họp | — | HUFLIT, **27/11/2026** |
| chủ đề | track **Natural Language Processing** | **"AI tạo sinh, Ngôn ngữ và Trách nhiệm xã hội"** |
| hạn nộp | **31/8**, qua EDAS (`edas.info/index.php?c=35461`; EasyChair đã đóng) | **30/8** (`https://vcl.huflit.edu.vn/`) |
| ẩn danh | **không** phản biện ẩn danh ⇒ giữ tên tác giả | — |
| mẫu | IEEE, nộp PDF ⇒ `IEEEtran` dùng được | quy cách đo từ kỷ yếu VCL 2025 — xem mục *CÒN TREO* |

Tác giả: Lê Đoàn Phương Uyên · Nguyễn Hồng Bửu Long · Faculty of Information Technology,
University of Science, VNU-HCM.

⛔ **Rủi ro lớn nhất còn mở: chính sách trùng lặp / nộp đồng thời của VCL vẫn CHƯA kiểm.**
Chi tiết ở mục *CÒN TREO* cuối file.

### ⛔ Lệnh dựng — bài học đắt nhất của hai bài

**`tectonic -X compile main.tex --outdir .`** (ghi sẵn ở `paper/fair2026/README.md:76` và
`thesis/build.sh`). Máy **không có `xelatex`**; trợ lý từng tự chế `xelatex … >/dev/null 2>&1`,
`command not found` bị nuốt, nên mọi lần báo *"8 trang, 0 overfull"* đều là đọc PDF cũ. Lặp
hơn mười lần trong một ngày.
⇒ **Luật: KHÔNG `>/dev/null 2>&1` trên lệnh dựng; kiểm `ls -la main.pdf` mốc giờ trước khi tin
số trang.**
⛔ **`main.log` trong kho là BẢN CŨ — tectonic KHÔNG ghi log trừ khi có `--keep-logs`.** Ngày
29/8 log FAIR còn là bản 25/8, báo *"8 trang"* trong khi bài đã **9 trang**, vượt trần. Suýt nộp
bài quá trang.
⇒ **Cách đúng, dùng cho cả hai bài:**
```
rm -f main.log && tectonic -X compile main.tex --outdir . --keep-logs
grep -oE "Output written on main\.xdv \([0-9]+ page" main.log   # số trang
grep -c Overfull main.log                                        # phải là 0
```
⚠️ **Trần trang: FAIR ≤ 8 (cứng) · VCL không giới hạn.** Bài FAIR luôn kín đúng 8 trang ⇒ **thêm
chữ là phải cắt chữ**, cắt xong dựng lại kiểm ngay chứ đừng ước lượng.
⚠️ Sửa toàn chuỗi cùng độ dài (đổi chữ số) thì **PDF ra đúng bằng byte cũ** — đừng đọc kích
thước tệp không đổi thành "dựng hụt".

### VCL — đóng khung thế nào

Rút từ **`thesis/chapters/ch3_dulieu.tex`** (đã sẵn tiếng Việt, không phải dịch): nguồn và phép
ghép đa nguồn · kiểm phép ghép · quy mô, chia tập, rò rỉ · trích chữ trên màn · nhãn mô tả tự
động · bốn nhánh và bất biến cấu trúc.

✅ **Đặt tên bộ nhãn: `GUIRefCorpus` (chốt 30/8, user quyết).** Đọc thật bốn bài ngữ liệu
trong kỷ yếu VCL2025 (#20 văn bia Hán Nôm tr.305 · #9 gán nhãn ngữ nghĩa tr.112 · #32 corpus
song ngữ tr.440 · #30 đồ thị tri thức tr.418) thấy bốn nếp chung: sản phẩm **có tên** và được
"công bố" ngay ở tóm tắt (HanNomCorpus) · một mục **Số lượng – Định dạng – Chất lượng** liệt
kê tên từng cột · chữ **"bộ ngữ liệu vàng"** cho mẫu đối chiếu · câu **dẫn cấu trúc bài** cuối
phần Giới thiệu. Đã áp cả bốn vào `main.tex`: tên xuất hiện ở tóm tắt, Mục 1, Mục 7, kết luận;
Mục 7 thêm đoạn đặc tả (41.099 dòng tập dạy + **4.448** tập kiểm, JSONL, khoá
`(episode_id, step_id)`, ảnh không kèm vì bản gốc CC0).
⛔ **KHÔNG hứa phát hành** — user quyết chỉ đặt tên, không cam kết ngày mở dữ liệu.
⛔ **KHÔNG viết "có thẩm định chuyên gia"** như bài #20 — lát 1.074 do chính nhóm đọc tay,
và người chỉ **chấm** chứ không sửa nhãn; bài ghi rõ điểm khác đó.
⭐ Bài mình mạnh hơn mặt bằng venue ở KTC Wilson, đối chứng lệch chủ ý, kiểm rò rỉ toàn tập —
bốn bài kia gần như không có phép kiểm định lượng nào cho chính bộ nhãn. Giữ, chỉ gọi bằng
ngôn ngữ cộng đồng. Kỷ yếu đã tải sẵn: scratchpad phiên 30/8, `vcl2025.pdf` (736 trang,
offset trang PDF = trang bài + 11).

⚠️ **Đóng khung theo hướng NGÔN NGỮ, đừng đóng khung "chúng tôi dựng bộ dữ liệu"** — VCL là hội
thảo ngôn ngữ học tính toán. Câu chuyện đúng là **sinh biểu thức quy chiếu cho phần tử giao diện**:
gọi tên thế nào để bên kia trỏ đúng, khi **22% phần tử không có tên** và **7,6% trùng tên**. Đó là
dòng REG (Mao CVPR16 · Yu CVPR17 · Luo CVPR17) đặt vào miền GUI. **Cấm chữ "đầu tiên"/"mới"** cho
ý này — dòng REG chiếm từ 2016.

### Bảng phân số — chống trùng lặp

| số | thuộc bài nào |
|---|---|
| trần 75,7 · sàn 12,0 / 6,1 · cổng A · 5 luật chấm · diễn đạt lại · gọi-tên-vs-chỉ-chỗ · tất định · κ | **FAIR, độc quyền** (dụng cụ, không phải đóng góp) |
| Base 47,6 · S1 59,1/59,6 · S2 57,2 · CE2 59,4 · MIN 60,0 · bảng 2×2 · lát 7,3% | **FAIR, độc quyền** |
| ghép hai kho 2,4× · rò rỉ 0 · OCR phủ 100% · chất lượng nhãn (73,6 / 22,0 / 7,6) · hai cổng lọc · quyết định A′ bị bác · 9 bất biến · bảng dấu hiệu phân biệt · phép so ô tên với câu người (53,5 vs 5,1) | **VCL, độc quyền** |
| quy mô 64.567 / 6.958 / 4.463 | cả hai nêu — **VCL tả đủ, FAIR một câu + trích VCL** |

**Trích chéo dạng *"đang bình duyệt"*** — nộp cách nhau một ngày nên không bài nào có ID/DOI.
Phần dùng chung phải **viết lại câu chữ**, không bê nguyên (khác ngôn ngữ nên rủi ro thấp).

### Đã vá vào FAIR (giữ để khỏi vá lại)

sàn 12,0 · `f3` 6,1 · cặp 28,5-vs-3,5 · §VII thay đoạn *"floor we have not measured"* bằng phép
đo · §VIII đoạn gọi-tên-vs-chỉ-chỗ · bản không-tham-chiếu (lệch ≤0,20 pp) · κ có điều kiện · sai
số bộ trỏ theo nhánh · điều kiện đảo nghĩa · đếm mục sửa đổi **27, 21 trước điểm đầu tiên** · lát
cắt ngoài ba lát đăng ký **gắn nhãn thăm dò** · hạ luận cứ đồng thuận BLEU/ROUGE · tách mức câu vs
mức hệ thống · tự khai hai lần nới ngưỡng sau khi thấy điểm kèm phản chứng.

**Soát số 29/8 (commit `01355e4`) — tám chỗ, đã vá:** FAIR gỡ lại câu *"across the 99,131 trees"*
(bản nháp **thêm lại** một số đã rút) · tỉ lệ S1 trên trần 78,1 → **78,0** (84,4 tính bằng S1/101
nên vế sau phải cùng gốc; **78% ở mục quy công là đại lượng khác**, vẫn đúng) · trung vị độ dài câu
31 → **33 và 34** · điền ô dung sai S1/202 = **69,8**. VCL: *"lát thử nhỏ hơn 24 lần"* → **38 lần**
(lát thử đúng **1.074** nhãn) · đếm hướng mỏ neo 7.768/1.894 → **8.382/2.033** (bốn hướng nay cộng
đúng 27.628) · trùng tên lát thử 6,9 → **7,0%**.

### Luận văn — ĐÃ ĐỒNG BỘ TỚI 30/8, **96 trang, 0 overfull, 0 tham chiếu hỏng**

Bản 18/8 (77 trang) còn dừng ở *"S2 chưa chạy"*; ngày 30/8 đã kéo lên ngang trạng thái hiện tại.
Dựng bằng `tectonic -X compile main.tex --outdir . --keep-logs` (KHÔNG có `xelatex` trên máy).

**Đã thêm/sửa, theo chương:**
· **ch1** — §Đóng góp viết lại thành **ba đóng góp** (thước đo · kết quả đăng ký trước không hoàn
  tất · chẩn đoán chỗ nghẽn). ⭐ **Vá cách trích 84% của Jandial** (số đã rút, xem mục Tiền lệ ⑤).
· **ch3** — mục mới **Tập cặp quy chiếu tối thiểu** (22.854 cặp · dải 80–350 px · lối tắt
  `(no name)` **17,4% = 9,6 + 7,8**, bất đối xứng HAI chiều, đừng viết một chiều) + ghi rõ s2r và
  s2_nopoint chỉ dựng dữ liệu, không train.
· **ch4** — mục mới **§Chặng huấn luyện thứ hai** (`sec:mindescthietke`): cặp tối thiểu, đối chứng
  CE2, hai lệch chuẩn khai ngay tại thiết kế.
· **ch5** — hai mục mới: **§Phép diễn đạt lại** (`sec:phepA`, số bản **v2**: p3 89,4→85,9, b=8 c=1,
  p=0,046; gộp 1.139 câu +0,35 [−0,59;+1,29]) và **§Đổi dụng cụ đo** (`sec:phepB`, UI-Venus, chứng
  nhân giữ 94%). Mục MDE thêm **σ hạt giống 0,46 ⇒ MDE một-hạt-giống 2,11**; phép kiểm no-harm đổi
  từ "chưa chạy" sang **TRƯỢT**.
· **ch6** — bảng chính 7 nhánh · bảng McNemar gộp 12 phép so · ba mục lớn mới: **§Nhánh khai báo**
  (`sec:nhanhs2`, gồm lát 7,3% và bảng 2×2 của S2) · **§Chặng hai** (`sec:mindesc`, cổng cơ học,
  Δ_component +0,63 ô TRẮNG, quy công 78/22 và **88/12** (sửa 31/8: 5,90/6,70 = 88,1%; con số 87/13 cũ là bản làm tròn lỏng), on-policy dừng ở cổng, **§Cái giá ở bước
  không chạm** `sec:khongcham` −19,75) · **§Chỗ nghẽn** (`sec:chonghen`, bảng 2×2 MIN + phân rã 5 ô
  + trần chặn-vế-âm 65,8 ⇒ +5,4). Mục cuối đổi thành **§Trạng thái các nhánh** (`sec:trangthai`).
· **ch7** — hạn chế tách thành ba nhóm, thêm nhóm **Hạn chế của kết quả về mô hình**; hướng phát
  triển nay là **ba nhánh đã đăng ký của (x14)** (ứng viên · lùi · MIX) + hoàn tất hạt giống thứ hai.
· **ch8** — hai bài báo đúng trạng thái 29/8 (FAIR = bài mô hình, VCL = nhãn quy chiếu).
· **02_vietat** thêm ORPO/MIN-DESC/CE2-S2 · **03_trangthongtin** cập nhật cả bản Việt lẫn Anh.

**Rà văn phong 30/8 (lượt hai, theo yêu cầu user):**
· ⛔ **Bỏ sạch dấu gạch dài `---`** (100 chỗ) — phần lớn viết lại câu bằng dấu phẩy, ngoặc
  đơn hoặc dấu hai chấm, không thay bằng gạch ngắn. Khoảng số `$a$--$b$` đổi thành
  `$a$ đến $b$`; chỉ giữ en dash ở số trang tài liệu tham khảo. Ô trống trong bảng dùng `-`.
· ⛔ **Bỏ cụm ghép gạch nối kiểu tiếng Anh trong tiếng Việt:** `không-gây-hại`,
  `câu-sai-màn`, `tất-cả-hoặc-không`, `thị giác--ngôn ngữ`, `dạy--kiểm`, `S1--Base`. Chỉ
  giữ `nơ-ron`, `mô-đun`, `ĐHQG-HCM`.
· **Thuật ngữ đã thống nhất:** `cơ chế hỏng`/`kiểu hỏng` → **dạng lỗi** · `chỗ hỏng`/`chỗ
  nghẽn` → **điểm nghẽn** hoặc viết lại · `checkpoint` → **điểm lưu** · `chứng nhân` →
  **phép so đối chiếu** · `nhiễm văn phong` → **thiên vị theo văn phong** · `phần bị đụng`
  → **phần bị tác động** · `quota` → **hạn mức máy**.
· **Bỏ các mở đầu câu lộ giọng máy:** "Nói gọn:", "Nói cách khác", "Điều đáng nói", "Cái
  mà…", "đằng này", "nghe như", "đáng mang đi nhất", "ăn điểm", "lưới an toàn mỏng", "bê
  nguyên văn", "leo thước".
· **Đã viết dài ra những câu cụt:** "Cổng đạt, với biên rộng" · "Thước cũng không suy biến
  về sàn" · "Đó đúng là thứ một giả thuyết không phải cho ra" · "Hai chiều triệt tiêu nhau"
  · "Vài ví dụ thật" · giải thích ORPO ở ch4 (trước chỉ có một vế "dạng tỉ số odds").

⭐ **Hai số đã rút vẫn sống trong `.tex` tới 30/8, nay đã vá** (đúng mẫu hình đã cảnh báo):
· ch3: *"đo trên 99.131 màn thì 12,6% phần tử có tên"* → **120 màn lấy ngẫu nhiên** từ kho đó;
· ch3: lát thử *"nhỏ hơn 24 lần"* → **1.074 nhãn, nhỏ hơn gần 38 lần**;
· ch5: tỉ lệ S1 trên trần **78,1 → 78,0** (thêm mốc MIN-DESC = 79,3%).

**Rà cách trình bày 30/8 (lượt ba, user chỉ đích danh):**
· ⛔ **Tiêu đề mục KHÔNG viết dạng câu hỏi.** Đã đổi: *"Kết luận này có đứng vững không?"* →
  **Kiểm tra bảy cách giải thích thay thế** · *"Thước có bền trước cách diễn đạt khác
  không?"* → **Độ bền của thước trước các cách diễn đạt khác** · *"Một thước dựa trên câu
  chuẩn sẽ kết luận gì?"* → **Kết luận mà một thước dựa trên câu chuẩn đưa ra** · *"Chọn
  luật trúng: vì sao ngưỡng dung sai quy ước không đủ"* → **Luật xác định trúng và giới hạn
  của ngưỡng dung sai quy ước** · *"Vì sao các thước đo có sẵn không dùng được"* → **Giới
  hạn của các thước đo có sẵn** · *"Lỗi của nhánh nền nằm ở đâu"* → **Phân bố lỗi của nhánh
  nền** · *"Điểm nghẽn nằm ở đâu"* → **Định vị điểm nghẽn của thành phần đề xuất** ·
  *"Tinh chỉnh thực sự dạy được gì"* → **Khác biệt hành vi giữa mô hình gốc và mô hình đã
  tinh chỉnh**.
· ⛔ **Không câu hỏi tu từ trong thân bài.** *"Điều kiện Voronoi có thực sự cần thiết… hay
  không? Câu hỏi này được trả lời bằng đo đạc."* → phát biểu thẳng: điều kiện này làm thước
  chặt hơn nhưng phức tạp hơn, nên sự cần thiết của nó được kiểm bằng đo đạc.
· ⛔ **Không ẩn dụ thể thao / đời thường:** *"lợi thế sân nhà"* → **việc trùng ứng dụng giữa
  tập dạy và tập kiểm** · *"đứng vững qua sáu cách giải thích"* → **giữ nguyên sau khi kiểm
  sáu cách** · *"được ăn cả ngã về không"* → **dồn hết vào đuôi phân bố**.
· Tiêu đề đoạn (`\paragraph`) cũng bỏ giọng đối thoại: *"Vì sao có chặng này"* → **Căn cứ
  của chặng huấn luyện này** · *"Giới hạn phải nêu kèm bảng"* → **Giới hạn của cách chia
  nhóm này** · *"Cái mà bản đăng ký đòi…"* → **Phần mà bản đăng ký yêu cầu nhưng luận văn
  chưa có**.

**Hai hình đã vẽ lại 30/8:**
· **Hình 4.1 (quy trình)** — bỏ khung `\fbox` + `\ttfamily` cũ, vẽ bằng **TikZ**
  (`\usepackage{tikz}` + `positioning,arrows.meta,backgrounds,fit` đã thêm vào
  `thesis/main.tex`). Hộp bo góc, mũi tên thật, nhãn trên mũi tên, khối huấn luyện tô xám.
  Vector, cùng font thân bài. **Không cần Figma/draw.io** cho hình dạng này; nếu sau muốn
  đổi thì chỉ việc thay khối `tikzpicture` bằng `\includegraphics` của một PDF vector.
· **Hình 5.1 (luật chấm)** — vẫn là ảnh màn hình thật có phủ lớp vẽ, nhưng thêm **chú giải
  sáu mục ngay trong hình**, khung viền, dấu to hơn và có viền trắng để không lẫn vào chữ
  trên ảnh. Script bản tiếng Việt: `harness/make_fig_voronoi_vi.py` (chạy bằng
  `~/.venvs/thesis/bin/python`, cần `huggingface_hub` nên **không chạy được với python hệ
  thống**). Bản tiếng Anh của bài FAIR giữ nguyên ở `harness/make_fig_voronoi.py`.

⛔ **`thesis/main.pdf` bị khoá ghi khi user đang mở PDF** — tectonic báo
`error: Permission denied (os error 13)` **sau khi** đã in `Writing ./main.pdf`, và file trên
đĩa vẫn là bản cũ. Cách làm việc: dựng vào thư mục tạm (`--outdir <scratchpad>/build`) để
đọc số trang/overfull, và nhắc user đóng trình đọc PDF rồi dựng lại vào `thesis/`.

**Gỡ chi tiết mã khỏi luận văn (30/8, user yêu cầu):** không để tên file, tên tham số hay
tên cờ của mã trong thân bài. Đã diễn đạt lại bằng lời: `harness/make_floor.py` ·
`total_flos` · `strict_back` · `use_cache` · `max_samples` · `enable_liger_kernel: true` ·
`desc_neg` · trường `pred` · nhãn biến thể `p1`…`p4` (nay gọi thẳng *"đổi động từ thao
tác"*, *"đảo trật tự mệnh đề"*, *"bỏ mệnh đề vị trí"*). Tên nhánh thống nhất viết hoa:
**S1 · S2 · S2r · S2-nopoint** (bỏ dạng `s2\_nopoint`).
✅ **Được giữ** vì là mô tả *dữ liệu* chứ không phải mã: `<desc>`/`<point>` · `(no name)` ·
`(episode_id, step_id)` · `content_description` · `step_instructions` · tên hai kho
HuggingFace · ví dụ chuỗi OCR · `q,k,v,o,gate,up,down` (các ma trận LoRA nhắm tới).

**Viết lại phần đầu 30/8 (user: *"viết như AI vậy á"*):** đã viết lại **lời cam đoan, lời
cảm ơn, danh mục thuật ngữ, trang thông tin (cả bản Việt lẫn bản Anh) và Mục 1.1 Đặt vấn
đề**. Nguyên tắc rút ra, áp cho mọi phần viết tiếp:
· ⛔ **Bỏ nhịp câu lặp cấu trúc** kiểu *"Nó ngắn, nó chỉ nói về màn hình đang mở, và nó
  viết cho một người đọc"* — dấu hiệu máy viết rõ nhất.
· ⛔ **Bỏ từ khẩu ngữ**: *"bí giữa chừng"* · *"soi tay 40 ca"* · *"lỗi áp đảo"* · *"chuyện
  mô hình bịa"*.
· **Câu dài nhồi nhiều số phải tách ra**: một ý một câu, số đặt vào chỗ tự nhiên; bỏ bớt
  ngoặc đơn lồng nhau và chuỗi dấu chấm phẩy.
· **Thuật ngữ nêu lần đầu phải giải thích ngay bằng lời thường**, kể cả khi đã có trong
  danh mục viết tắt.

⚠️ **Chưa đụng:** `\Khoa` vẫn là ô `\CANDIEN` (khoá đào tạo) — cần user điền.
⛔ **Quét toàn kho sau mỗi lần rút số** — `total_flos` sai đã sống trong `.tex` nhiều ngày sau khi
đã rút ở `CLAUDE.md` và `report/108`.

### Phương án đã cân nhắc và gác lại

**VCL đi hướng tiếng Việt thật:** dịch câu chuẩn của người sang tiếng Việt rồi đo lại
executability, xem thước có sống qua đổi ngôn ngữ không. Hợp venue nhất, nhưng tốn thêm một lượt
chấm Kaggle 5,6 giờ + dựng bản dịch. **Gác vì user muốn VCL đơn giản.** Nếu sau này còn thời gian
thì đây là mục thêm đáng giá nhất cho VCL.

### ⛔ Ba thứ đã chết, đừng theo

· **`report/KE_HOACH_2_BAI_BAO.md` (bản 3, 12/7)** định VCL = *sinh hướng dẫn tiếng Việt trên màn
MobileViews*. Chết cả hai vế: MobileViews đã rời khỏi đề tài, và không có thí nghiệm tiếng Việt nào.
File vẫn giữ để tra lịch sử.
· ✅ **Skill `.claude/skills/vcl-fair-paper/SKILL.md` ĐÃ VIẾT LẠI 1/9/2026** — bản cũ tả khung
**DG1/DG2** (ReOrder-Tutor, Copeland, MobileViews, ScreenSpot, "không fine-tune", GPT-4o E2E) tức
khung prompting **đã bị bác 19/7**, và đã sống trong skill hơn hai tháng. Bản mới bao **ba** bài
(FAIR = mô hình · VCL = ngữ liệu quy chiếu · **SOICT = sprint `gui_sel`**, `report/132`), kèm bảng
phân số, luật dựng tectonic, luật văn phong, bảng số đã rút và checklist nộp. Bản cũ cất ở
**`report/_archive/SKILL_vcl-fair-paper_DG1_DG2_TRUOC_VIET_LAI_1_9_2026.md`** — ⚠️ **`.claude/`
nằm trong `.gitignore` từ `b755cc7` nên skill KHÔNG có lịch sử git**, sửa lớn phải tự sao lưu
trước. Sprint `gui_sel` tách ra skill riêng **`soict-paper`** (thiết
kế ba nhánh, cổng G1–G11, cấu hình train, luật đọc Δ_sel, lịch, phương án lùi).
⚠️ **`CLAUDE.md` vẫn thắng cả hai skill khi mâu thuẫn.**
· **Bản 18/8 đặt bài chính ở thước đo** cùng kế hoạch *"FAIR 10 trang, phải cắt 2 trang, cắt §III
rồi trích VCL"* — quyết định 23/8 thay toàn bộ. Lý do của bản 18/8 còn tra được ở lịch sử git của
file này.

---

## 🎓 TIỀN LỆ VÀ PHÂN ĐỊNH (đã tra tận nguồn — `report/114`)

**① Chữ "executability" đã có chủ.** *Open Grounded Planning*, **ACL 2024, tr. 4982–5003**
(arXiv 2406.02903), mục 3.3.2: *"Executability is the proportion of executable cases…"*.
Nhưng của họ là **tra bảng ký hiệu trên văn bản** — không mô hình, không màn hình, miền
WikiHow/công cụ/robot. Của ta là **hành vi + thị giác**. ⇒ **GIỮ TÊN**, đã vá một câu phân định
vào Introduction của `main.tex` ngay lần dùng đầu.

**② Zhao et al. EACL 2021 (tr. 1302–1316)** — vừa hậu thuẫn vừa cảnh báo, đã trích:
*"BLEU, ROUGE, METEOR and CIDEr are ineffective for evaluating grounded navigation
instructions"* ⇒ hậu thuẫn hạ luận cứ đồng thuận BLEU/ROUGE. ⚠️ Nhưng thước không-tham-chiếu của
họ thắng ở **mức CÂU**; để xếp hạng **HỆ THỐNG** chính họ khuyên dùng SPICE (có tham chiếu), mà
toàn bộ Mục VII của ta là khẳng định mức hệ thống — đã trích vào *Scope of the construct*.
Họ **có** neo người, ta không.

**③ GUITrans2Act (2606.12817) không phải scoop** — preprint 6/2026 không venue, đầu vào là
**video**, abstract không nhắc mô hình định vị.

**④ GCoT: 2503.12799 vẫn là preprint không venue**; bài ICCV 2025 là bài KHÁC (2507.02859).
Ghi chú của ta đúng từ 1/8, agent nói sai. ⭐ Lần này ghi chú mình thắng agent ⇒ **agent cũng
phải kiểm như mọi nguồn khác: không tin ngay, cũng không bỏ ngay.**
Về nội dung GCoT: số âm −42,8 là **prompting zero-shot** và là **số tự tính** từ Table 3−4 (bài
chỉ viết 45,4); chính bài đó Table 5 cho thấy **TRAIN theo thứ tự grounding-trước thì tăng +4,5 /
+5,8**. Đừng trích một nửa.

**⑤ Jandial et al. (Findings EACL 2026) — con số 84% đã bị rút.** Nguyên văn abstract: *"Our
agent reports high success rate (upto 84%) in generating instructions that fail the
state-of-the-art GUI grounding models."* ⇒ 84% là **tỉ lệ thành công của một agent đối kháng**
chuyên chế câu phá mô hình, trên **desktop Windows** — không phải tỉ lệ trượt khi diễn đạt lại,
không phải trên di động. Sai từ 29/7, sống 20 ngày, đã vào bản thảo.
**Cách trích đúng (đã vá vào `main.tex` hai chỗ):** trích họ cho luận điểm *"độ chính xác đo trên
MỘT câu tốt nhất cho mỗi phần tử là thổi phồng năng lực thật"*; nêu 84% kèm đúng điều kiện
(năng suất của tìm kiếm đối kháng trên desktop), và **trường hợp di động họ để ngỏ chính là của ta**.

**⑥ Chữ cấm dùng.** Không viết *"đầu tiên"/"novel"/"cơ chế mới"* cho thứ tự sinh hay cho việc đưa
danh sách phần tử vào đầu vào — bài gốc AndroidControl (NeurIPS 24) đã fine-tune với danh sách
a11y làm INPUT; dòng REG phân biệt (Mao CVPR16 · Luo CVPR17 · Yu CVPR17) đã chiếm ý *"câu phải đủ
để bên kia trỏ đúng"* từ 2016. **Điểm phân định còn vững:** trong bài gốc AC `step_instructions`
là **INPUT**, ta dùng làm **ĐÍCH SINH**; và đưa tính phân biệt vào **mục tiêu huấn luyện** trong
miền GUI (Widget Captioning EMNLP20 loss chỉ cross-entropy thuần — đã trích PDF verify).

---

## ⛔ GIỚI HẠN CÒN MỞ

**Bộ trỏ không sạch** (lật 16/8, đã tra tận nguồn, đã vá vào bài):
· UGround **có AndroidControl 47K nhãn người** trong recipe (Bảng 1, arXiv 2410.05243), cùng
Widget Caption 41K · UIBert 16K · AITZ 8K.
· UGround-V1-2B dựng trên **Qwen2-VL**, **cùng dòng** với Qwen2.5-VL-3B đang bị chấm.
· Phần còn đứng: họ lấy từ **split train**, tập kiểm của ta từ **split test** ⇒ không chồng lấn ở
mức màn hình, không phải rò rỉ nhãn. Nhưng bộ trỏ đã thấy **văn phong chú thích** của kho này, mà
s1 được dạy viết đúng văn phong đó ⇒ **còn một lời giải thích thay thế cho chênh lệch S1−Base**.
✅ **ĐÃ ĐÓNG 20/8** bằng phép B: chấm 2.532 bước bằng UI-Venus-Ground-7B, chứng nhân S1−Base
giữ 94% (+10,35 → +9,68 pp) ⇒ chênh lệch S1−Base không phải do bộ trỏ quen giọng.

**Đã thay dụng cụ một lần (phép B, 20/8)** — S1−Base và S2−S1 giữ nguyên dấu và gần nguyên độ
lớn dưới bộ trỏ sạch AndroidControl ⇒ lời giải thích *"bộ trỏ quen văn phong AC"* **không còn
đứng**. ⚠️ Vẫn **cùng họ Qwen2.5-VL** nên đòn *cùng họ* chưa đóng. **Không có neo ngoài nào**
(đã quyết không chấm người). Trong ba lỗ ghi ở `report/112` §11.3, hai đã đóng (sàn · gọi-tên-hay-chỉ-chỗ).

**Bộ trỏ thứ hai đã tra xong 15/8, đừng tra lại:** chọn `inclusionAI/UI-Venus-Ground-7B`
(Apache-2.0, ScreenSpot-v2 mobile 99,0/90,0, mạnh hơn UGround 95,0/83,3, sạch AndroidControl).
Ưu tiên **A100 hơn T4** vì NF4 ăn vào đúng thứ cổng A đo. Dự phòng: Phi-Ground-4B (ngoài họ Qwen
nhưng yếu ở mobile) · ShowUI-2B (⚠️ lỗi tràn số fp16 → NaN).
⛔ **Đã loại:** GUI-G2-3B (trùng nền) · **Jedi (CÓ AndroidControl** dù tự quảng bá chỉ dữ liệu
tổng hợp) · CogAgent (link chết) · Aria-UI (25,3B) · SE-GUI/GUI-G1/GUI-R1/Holo1/POINTS-GUI-G.
⚠️ **Câu chữ:** viết *"bộ trỏ không được huấn luyện trên AndroidControl"*; **CẤM** viết *"chưa
từng thấy màn hình di động"* — chúng dùng Widget Captioning/UI RefExp/RICO đều là kho Android
(và ba nguồn đó 2020/2021/2017 **có trước** AndroidControl 6/2024).
⛔ Câu *"mọi bộ trỏ GUI mở đều dựng trên họ Qwen-VL"* là **SAI** (Phi-Ground dựng trên
Phi-3.5-Vision) — đã lỡ vào Limitations và đã vá.

**Bốn lượt phản biện độc lập (18/8) — phán quyết: hợp lệ, nhưng phải hẹp hơn nhan đề.**
Toàn văn `report/112` §11. Đứng vững, không lượt nào lật được: SFT hơn mô hình gốc hai hạt giống
độc lập · cùng nội dung khác văn phong không ý nghĩa · 5 luật chấm không đổi thứ tự · thước tất
định · 1.139 câu viết lại +0,35 pp · **thước không xếp văn máy trên văn người** (lá chắn tốt nhất,
đã đưa vào §VII) · không lợi thế sân nhà · đăng ký trước kiểm được bằng `git log`.

⭐ **Mẫu hình quan trọng nhất: bảy lỗi bắt được trong hai ngày, KHÔNG lỗi nào ở khâu ĐO.** Tất cả
nằm ở **câu chữ mô tả**: 84% của Jandial · "bộ trỏ khác họ/sạch AC" · "reference-free" ở nhan đề ·
`hit_disk` là "đĩa" · hạt Voronoi là "tâm phần tử" · κ trình thiếu điều kiện · đếm mục sửa đổi.
Phần **đo** giữ nguyên qua mọi lượt soi. ⇒ **Chỗ phải soi tiếp là VĂN BẢN, không phải mã.** Và cụ
thể: mọi lỗi sinh ra ở khâu **tóm tắt một nguồn thành câu ngắn cho tiện trích**, rồi câu ngắn sống
nhiều tuần vì không ai mở lại nguồn.

**Tả đúng dụng cụ** (ba chỗ từng tả sai, đọc từ `harness/metric_exec.py`):
· `hit_disk` là **hình chữ nhật** |dx|≤0,14·W ∧ |dy|≤0,14·H — dung sai dọc rộng gấp **2,2×** ngang
(336 vs 151 px), không phải đĩa Euclid.
· Hạt Voronoi là **chính điểm chạm**, không phải tâm phần tử.
· `hit_voronoi` **bao gồm** luật đĩa (`if not hit_disk(...): return False`) ⇒ Voronoi là bản
**siết chặt** của luật quy ước, **cấm trình như hai lựa chọn ngang hàng**.
· ⛔ **Đừng lấy ngưỡng ±14% của `hit_disk` để suy luận về việc thước có phân biệt được hai phần
tử hay không** — đã mắc 25/8 và suýt dựa vào đó để đổi thiết kế dữ liệu huấn luyện. Voronoi phán
bằng *nút nào GẦN NHẤT*, mà `dedupe_buttons` chỉ gộp nút cách gold dưới **63 px** (màn rộng 1080),
trong khi `hop_le()` đã ép phần tử âm cách **80–350 px** ⇒ **mọi phần tử âm đều phân biệt được**.
Ngưỡng ±140 trong `gate_desc_acc.py` là chuyện của **cổng khai báo**, không phải của thước.
Chi tiết: `report/120` Mục 3b.
· Bộ bơm lỗi **không gọi bộ trỏ lần nào** ⇒ hàng "paraphrase 0,0%" chỉ đo cổng chữ.
· Hình trong bài dựng bằng `harness/make_fig_voronoi.py` có `assert` gọi thẳng hàm của thước nên
hình không thể trái mã.
· Lỗi `canon_action` **cố tình không sửa**: `go back` quy về *tap* (81 bước S1, 47 Base; sửa thì
59,12→58,81 và 47,60→47,40) — giữ nguyên để ba nhánh đã chấm còn tái lập được, thêm cờ
`strict_back=True` cho lượt mới + mục sửa đổi (v).

---

## 🔒 THIẾT KẾ ĐÃ NIÊM PHONG (5/8/2026, commit `b93e85c`)

`report/106_DANG_KY_TRUOC.md` khoá: 6 nhánh · thước đo · **luật đọc kết quả cho cả 4 kết cục**
(dương / dương yếu / trắng / âm) · 3 lát cắt · hạt giống 20260805.
**Mọi thay đổi về sau ghi vào mục sửa đổi cuối file, KHÔNG sửa đè.** Hiện có **27 mục, 21 mục
trước điểm số đầu tiên**. Các mục đáng nhớ: (k) thêm nhánh mô hình gốc · (o) máy + cấu hình P9 +
luật chọn điểm lưu · (p) vá `tag_app_seen` · (q) nhãn khai báo sang tiếng Anh · (r) MDE thật 2,2 pp
⇒ dải "4–9 pp không kết luận được" của luật cũ sẽ vứt bỏ một hiệu ứng thật · (v) `strict_back`.

⚠️ **SHA của mọi commit đã đổi ngày 21/8** khi viết lại lịch sử để gỡ một khoá API và bốn gói
zip (hai gói vượt trần 100 MB của GitHub) ra khỏi các commit cũ. **Số commit, thông điệp và
mốc ngày giữ nguyên** ⇒ lập luận *"đăng ký trước kiểm được bằng `git log`"* vẫn đứng: bản
niêm phong 5/8 nay là `b93e85c`, trước đó là `51ddb35`. Bảng ánh xạ cũ→mới đầy đủ nằm ở
`.git/filter-repo/commit-map` — **giữ tệp đó**, nó là thứ nối hai cách đánh số với nhau.

**Thành phần đóng góp đã chốt 1/8** (`report/103_CHOT_THANH_PHAN.md`): **"mô tả phân biệt trước,
phát ngôn sau"** — đích sinh `[vai trò | tên | <point>x,y</point> | dấu hiệu phân biệt]` rồi mới
tới câu; chấm chỉ lấy câu. Headline = **ablation S1 (SFT trơn) vs S2**.
· Ràng buộc thiết kế có căn cứ: descriptor phải **có cấu trúc + có toạ độ** — văn tự do cho dấu ÂM
(Shikra bằng lời −7,39 vs chain-có-point +5,90; UI-Ins free-form −3,2 vs +4,7, ⚠️ hai model nền
khác nhau, cấm ghép cặp). Hiệu ứng kỳ vọng +3…+11, trung vị ~+5; bằng chứng gần nhà nhất =
Aguvis bỏ inner monologue → AndroidControl-Low **−11,4**.
· Đối chứng đã đăng ký: S1 · S2 · **S2r (tiền tố SAI cùng độ dài)** · S2-nopoint · phân tầng độ
dài và độ mơ hồ.
· **Hai đóng góp:** (1) MÔ HÌNH — Qwen2.5-VL-3B QLoRA, headline là ablation nội bộ; (2) ĐÁNH GIÁ —
executability + validate bằng bơm lỗi.

**Quyết định 5/8 về nguồn tên trong nhãn** (`report/107`): **bác** việc đảo sang OCR-trước, áp A′.
Ưu thế của OCR hoá ra là ưu thế của **lọc rác**, không phải của thứ tự (11/12 ca OCR thắng là do
nhãn trợ năng rác). Đã áp cổng `clean_a11y` (14,7% nhãn là rác) + cổng hình học ≤25% màn + luật
ghép OCR cùng dòng. **Cấm dùng A′ giải thích hậu kỳ nếu S2 thắng.**

---

## ⚙️ VẬN HÀNH — bài học đã trả giá

**Cấu hình train chốt = P9:** `train_config.yaml` + đúng một khoá `enable_liger_kernel: true`.
A100, 4-bit + gradient checkpointing, `cutoff_len` 2560, `preprocessing_num_workers: 8`.
**10,3 s/bước · 8.072 bước · ~23 giờ train · ~123 đơn vị/lượt.**
· ⛔ Hai kết luận ngược trực giác, **đừng thử lại**: **QLoRA 4-bit NHANH HƠN bf16** ở bài này
(10,70 vs 14,76 s/bước) — 3B đủ nhỏ để giải nén không thành nút thắt; và **chỗ ngốn bộ nhớ là
BẢNG LOGITS chứ không phải trọng số** — P4 tràn nhưng P4+liger chạy được, vì liger gộp
cross-entropy nên khỏi dựng bảng 151.936 từ vựng × ~1.500 token × 4 mẫu ở fp32.
· ✅ **Liger không đổi phép tính**: cùng 200 mẫu cùng hạt giống, loss trùng tới chữ số thứ tư ⇒
dùng được mà không phải sửa hồ sơ đăng ký trước.
· ✅ **Đổi card không đổi kết quả**: L4 vs A100 cùng `seed 101`, loss 20 bước trùng ba chữ số,
`total_flos` y hệt.
· ⛔ **P10 (tắt gradient checkpointing) bị loại — tràn bộ nhớ ở chuỗi dài.** Chạy ngọt trên mẫu
thường, chết trên 200 mẫu dài nhất của s2. **12 phút thăm dò cứu một lượt train 20 giờ.**
⇒ **probe trên mẫu ĐẦU TẬP không đủ kết luận về bộ nhớ**; mọi cấu hình đụng bộ nhớ phải thử lại
trên **nhánh nặng nhất với mẫu dài nhất**.
· **Mỗi biến thể chỉ đổi MỘT thứ** — bản đo đầu ghép hai thay đổi nên tràn trước khi trả lời được
câu nào.

**Colab:** tài khoản dùng **đơn vị trả trước, KHÔNG có `background execution`** ⇒ phải sống chung
với mất máy ảo. **Tám lần mất máy trong hai lượt S1, ~18 giờ, ~85 đơn vị.** Thiết kế cất Drive
hoạt động đúng: mỗi lần mất chỉ tốn 80–180 bước + thời gian dựng lại.
· **Đồng bộ Drive mỗi 5 phút.** Mất máy 10/8 (chưa có) = 42 đơn vị + 8 giờ; 11/8 (đã có) = 3 phút.
· Toàn bộ giá của một lần đứt nằm ở **mã hoá token**, không ở khâu nhảy qua lô (1.600 lô ≈ 17 giây).
· **`MOC` phải lấy theo dòng log cuối, KHÔNG theo số điểm lưu** — `logging_steps: 20` mà
`save_steps: 200` ⇒ log chạy trước điểm lưu tới 180 bước. Dấu hiệu phiên mới đã ghi thật: **số
bước TỤT XUỐNG**.
· **`grep "Resuming training from"` trống ngay sau khi khởi động là báo động giả** — dòng đó in
sau ~40 giây nạp thư viện. Hỏi ba thứ trước khi `pkill`: `getsize(log)` · `ps -p <PID>` · `tail`.
· ⛔ **mtime của tệp trên `/content/drive` KHÔNG cập nhật khi ghi thêm** — FUSE chỉ đổi khi đóng
  tệp. Tệp đang được `infer_branch.py` ghi dần có thể hiện mốc giờ cũ **cả tiếng** mà vẫn đang
  chạy bình thường. Kiểm bằng **`wc -l` hai lần cách nhau 60 giây**, đừng đọc `ls -la`.
· **Nhân Python đang chạy ô dài thì MỌI ô khác xếp hàng** ⇒ lúc cần cứu tệp phải dùng **Terminal
  Colab** (tiến trình riêng, cùng máy ảo, cùng thấy `/content/drive`). Hỏi tiến trình đang dùng
  đường dẫn nào bằng `tr '\0' ' ' < /proc/$(pgrep -f infer_branch|head -1)/cmdline`, không đọc
  lại lệnh đã gõ. Ô **T10–T13** của `colab_train_min_desc.md` ghi sẵn toàn bộ.
· ⛔ **`--out` trỏ thẳng vào Drive KHÔNG sống sót qua mất máy — đo thật 24/8.** Lượt CE2 ghi
  thẳng vào `MyDrive/thesis/preds_ce2_s2_seed101.jsonl` suốt 2 giờ; mất máy xong tệp đó **biến
  mất hoàn toàn** khỏi Drive, chỉ bản chụp định kỳ còn (3.616 dòng, cứu ~67 phút GPU). Tệp mở
  chế độ `"a"` chưa đóng lần nào thì FUSE chưa đẩy lên cloud, và `ls` vẫn hiện tệp như thường
  nên **không có dấu hiệu nào báo trước**. Chụp định kỳ sang **tên khác** bằng `cp` (tạo
  rồi đóng tệp mới ⇒ buộc Drive tải lên trọn vẹn). Bản chụp luôn cũ hơn ≤5 phút ⇒ **so `wc -l`,
  giữ bản DÀI HƠN**, đừng chép đè theo phản xạ.
· **Nhân Python restart làm rớt gắn Drive** — ô theo dõi văng `FileNotFoundError` trong khi tệp
vẫn nằm nguyên trên Drive. Thấy lỗi này thì chạy ô chẩn đoán, đừng chạy lại lệnh train.
· **Ô kiểm vàng A.2b** (`harness/run_on_colab.md`): so cfg lượt này với cfg lượt tham chiếu, **chỉ
4 khoá được phép khác** (`seed` · `output_dir` · `dataset` · `preprocessing_num_workers`), khoá
thứ năm là **dừng hẳn**. Chạy 3 lần trong ngày 16/8, lần nào cũng 38/38.
· **Phép kiểm rẻ "điểm lưu có trọn không": ghi dở thì bản CUỐI phải NHỎ HƠN bản trước.**
· ⛔ Ba số trong `all_results.json` **sai sau resume, cấm trích**: `train_loss`, `train_runtime`,
`*_per_second` (HF chia cho `elapsed`). `total_flos` **không** hỏng. Dùng `trainer_state.json`.
· ⛔ Phép thử "gập nắp mang máy đi làm" **thất bại** — ba lệnh `powercfg` + lid *Do nothing* không
đủ, log ngừng ghi ngay. Đừng thử lại.

**Kaggle:** quota **30 giờ GPU/tuần**. Chấm một nhánh ~5,6 giờ, **0 đồng**.
· ⛔ **Lượt commit từng treo 7 giờ vì log ngập.** `tqdm` ngoài terminal in mỗi cập nhật thành một
dòng (>1.400 dòng cho một lần nạp mô hình); Kaggle chặn log khi vượt trần ⇒ tiến trình kẹt cứng ở
lệnh ghi stdout. Bằng chứng: hai mục log `59.8s` và `25560.4s` **nội dung giống hệt nhau**, cùng
cụt giữa chữ.
· **Vá gốc:** tắt thanh tiến trình bằng biến môi trường **và** cho tiến trình con ghi **ra tệp**
(`Popen(stdout=f)`), cộng nhịp sống in từ notebook mỗi 2 phút. Runbook
`harness/kaggle_pheA_CHAY_LAI.md`.
· **Chạy tương tác, đừng Save Version** cho lượt đầu — commit bị huỷ thì Kaggle không lưu
`/kaggle/working`.
· **Không có dòng nhịp sống nào sau 4 phút thì dừng ngay.** Chi phí biết mình sai: 7 giờ → 4 phút.
· ⚠️ **Đừng ước lượng nhịp hỏng bằng cảm giác** — trợ lý từng chẩn "chạy CPU nên chậm 10–20 lần"
và khuyên chờ 6 giờ; log nói khác hẳn. Và từng suy "hai lần mất máy cách nhau 1,5 giờ ⇒ lượt train
không bao giờ về đích" rồi đề nghị mua gói mới; đọc `checkpoint-4800` mới biết phiên đó chạy 6,6
giờ. **Lấy hiệu số bước giữa hai điểm lưu.**

⛔ **Hai lỗi câm ngày 20/8, cùng một mẫu hình — phép thử CHƯA HỀ DIỄN RA mà báo như đã diễn ra:**
· **Dataset Kaggle giữ bản mã cũ.** Ba lượt dò cỡ ảnh ra sai số **trùng tới hai chữ số thập
  phân** vì lớp `UIVenus` trên dataset ghi cứng tham số, chưa đọc biến môi trường.
· **Ô vá sửa nhầm lớp.** `s.index("self.proc = AutoProcessor.from_pretrained(")` lấy lần xuất
  hiện **đầu tiên trong file** = lớp `UGround`, đứng trước `UIVenus`. Chạy `--grounder uivenus`
  thì lớp bị vá không được gọi lần nào ⇒ không lỗi, không cảnh báo, kết quả y như cũ.
⇒ **Cách chặn duy nhất hiệu quả: bắt tiến trình IN RA cấu hình nó thật sự đang dùng, rồi kiểm
dòng đó — đừng kiểm mã nguồn.** Đọc mã chỉ chứng minh mã trên máy này, không chứng minh mã đang
chạy trên máy kia.
⇒ ⭐ **Kết quả trùng nhau tới nhiều chữ số giữa các cấu hình KHÁC nhau là dấu hiệu HỎNG**, không
phải dấu hiệu bền vững. Suýt đọc thành *"cỡ ảnh không ảnh hưởng"*.
⇒ Bản vá trong `/kaggle/working` **chỉ sống trong phiên**; lượt chạy dài phải upload dataset mới.

**Bốn câu hỏi trước khi tiêu tiền GPU:** khâu này có thật sự dùng GPU không · máy chết bây giờ thì
mất bao nhiêu · chuỗi cần chấm đã từng được chấm chưa · mốc so nào rẻ hơn mà chạy trước được.
· ⭐ **Tệp thô là tài sản.** Giữ `*_raw.jsonl` thì đổi luật chấm hay đổi tập câu vẫn tính lại được
**không gọi lại bộ trỏ** — đã tiết kiệm trọn một lượt 5,6 giờ khi chấm lại `p3_nopos_v2` (0 giây
GPU, so byte, 6 phép `assert` trong `harness/phep_a_hieu_chinh.py`).
· ⭐ **Mẹo đo trần không cần GPU:** dựng tệp preds với `pred = gold_instruction` rồi chấm như mọi
nhánh.
· ⚠️ **Phép kiểm dùng chính phép biến đổi mà nó cần phát hiện thì mù** — `assert` hỏi "bộ trỏ tất
định không" tự `.strip()` chuỗi, che mất đúng thứ nó cần thấy (72/589 câu chuẩn có dấu cách cuối,
1 bước đổi hẳn kết luận vì lệch một ký tự).
· ⚠️ **Phép thử nối tiếp phải xin NHIỀU HƠN số đã có** — xin đúng số đã có thì in `Xong sẵn`,
trông như đạt mà không chứng minh gì.
· **Giá GPU phải đo/tra tại thời điểm quyết, cấm nhớ** — hai con số nhớ sai (15 đơn vị/giờ, card
40 GB) suýt dẫn tới thuê nhầm máy.

---

## 💻 Môi trường + harness

**Máy KHÔNG-GPU** (WSL2). Train trên **Colab** (A100), chấm điểm trên **Kaggle** (T4, miễn phí).
Ollama local: `nomic-embed-text`, `bge-m3`, `llama3.2`, `qwen2.5vl:3b/7b`.
Windows/WSL: chạy Python nhớ `PYTHONIOENCODING=utf-8`.
Chỗ lưu: thứ bắt buộc sống qua các phiên chỉ ~3 GB; 67 GB ảnh tải lại từ HuggingFace 20–40 phút.
*Phần đắt không phải phần to.* `drive.mount` chỉ gắn Drive của **chính tài khoản** chạy Colab.

**Mã chính trong `harness/`:**
· dựng dữ liệu — `build_train_data.py` · `build_branch_data.py` · `build_test_data.py` ·
`descriptor_label_build.py` · `prep_ocr_train.py` · `tag_app_seen.py` ·
**`build_min_desc.py`** (dựng 22.854 cặp MIN-DESC + đối chứng CE2-S2, 7 bất biến) ·
**`do_eligibility.py`** (đo cổng eligibility, in CẢ HAI thiết kế cặp, không có cờ tắt bớt) ·
**`gate_desc_acc.py`** (cổng cơ học MIN-DESC — độ chính xác khai báo, KHÔNG gọi bộ trỏ; mốc S2 = **53,9%**) ·
**`build_candidates.py`** (khối ≤40 ứng viên/màn + cổng G1 96,7% · G2 91,2% trên tập kiểm) ·
**`build_sel_data.py`** (dựng hai nhánh `gui_sel` / `gui_sft_match` của `report/123` §3.2–3.3 —
7 bất biến + cổng G3 rò rỉ + G4 độ dài; `gold_candidate()` ở đây là **bản duy nhất**, lúc chấm
`sel_acc` phải import lại chứ đừng viết bản thứ hai)
· train/suy luận/chấm — `train_config.yaml` · **`train_config_orpo.yaml`** (MIN-DESC) ·
**`train_config_ce2.yaml`** (đối chứng) · `infer_branch.py` · `score_run.py` ·
`metric_exec.py` (thư viện hàm chấm — **luật chấm mặc định không đổi từ commit `b93e85c`
ngày 5/8**; bản vá `strict_back` là thêm cờ tuỳ chọn, mặc định tắt, và **hiện chưa commit**) ·
`gate_a_ceiling.py`
· phân tích — `phan_tich_bon_nhanh.py` · `phep_a_ghep_cap.py` · `phep_a_hieu_chinh.py` ·
`mde_that.py` · `rule_sensitivity.py` · `bien_the_khong_tham_chieu.py` · `make_floor.py` ·
`doc_san.py` · `doc_diem_tam.py` · `kiem_preds.py` (8 phép kiểm tệp preds trước khi tiêu quota) ·
`make_fig_voronoi.py`
· runbook — **`colab_smoke_orpo.md`** (cổng kỹ thuật MIN-DESC — chạy TRƯỚC mọi thứ) ·
**`colab_train_min_desc.md`** (bốn lượt train + đồng bộ Drive + ô theo dõi có thanh tiến độ) ·
`S2_DAN_THANG.md` · `colab_train_s2.md` · `run_on_colab.md` · `colab_cham_san.md` ·
`kaggle_cham_san.md` · `kaggle_upload_dataset.md` · `kaggle_pheA_CHAY_LAI.md` · `run_on_rented.sh`

`infer_branch.py` và `score_run.py` đều **ghi dần + xả đệm + nối tiếp được**; `score_run` gộp số
cuối **từ tệp thô, không từ bộ nhớ**, nên chạy cắt khúc vẫn ra số toàn tập.

**Nguyên tắc chi tiền:** chạy MỘT lần cho đúng; ưu tiên local/free + cache; bước tốn tiền phải
hỏi trước. Ưu tiên **độ chính xác**, không ngại tốn thời gian lẫn tốn tiền — nhưng kết quả như
nhau thì chọn chậm-mà-rẻ. Luôn trình bảng **tiền · thời gian · ảnh hưởng độ chính xác**.

---

## ❓ CÒN TREO

- ⛔ **Hai kho đang lệch.** Máy WSL **không có** `FINAL_SOLUTION.md` lẫn
  `report/115_PHUONG_AN_TD_ROI_DA_RUT.md` — phiên debate 23/8 chạy trên một checkout khác (máy
  Mac). Mọi tham chiếu tới hai file đó trong `report/116` hiện là **tham chiếu chết**. Lấy về khi
  tiện; chưa có cũng không chặn việc gì, vì `report/117` đã tự chứa.

- **CFP của VCL — hai trong ba thứ đã chốt 29/8, còn một.**
  · ✅ **giới hạn trang: KHÔNG có** (user xác nhận 29/8) — bài VCL hiện **13 trang**.
  · ✅ **ĐÃ CÓ TEMPLATE CHÍNH THỨC (29/8)** — user gửi
    `VCL_Conference_Paper_Template for authors.docx`, nay chép ở `paper/vcl2026/`.
    Thông số đọc **trực tiếp từ XML** của file đó, đã áp trọn vào `main.tex` ngày 29/8;
    bảng đầy đủ + nguồn từng thông số ở **`paper/vcl2026/README.md`**.
    ⛔ **Quy cách đo từ kỷ yếu VCL 2025 nay ĐÃ BỊ THAY** — template thắng. Ba chỗ khác hẳn:
    trích dẫn **APA 7th author-date** (không phải `[n]`) · bảng **KHÔNG kẻ dọc**, nhan đề
    đặt **TRÊN** bảng (không phải dưới) · mục cấp 1 dùng **số Ả Rập** (không phải La Mã).
    Bản trước khi áp template giữ ở `paper/vcl2026/_archive/main_TRUOC_APA.tex.bak`.
  · ⚠️ **Hai chỗ template mâu thuẫn với thông báo hội thảo, đã xử:**
    giãn dòng thân bài (thông báo 1,5 · template đôi) ⇒ **user quyết 29/8: theo thông báo,
    1,5**; độ dài tóm tắt (thông báo 100–150 từ · template 150–250) ⇒ viết **đúng 150 từ**,
    con số duy nhất thoả cả hai. Script đếm lại có sẵn trong README của thư mục bài.
  · **Bài VCL nay 20 trang, 0 overfull — THÂN BÀI 17 trang** (rút ngày 30/8 từ 24 trang;
    giãn 1,5 làm dài ra từ 13 trang; VCL không giới hạn trang). Mục *Bốn nhánh dữ liệu và
    chín bất biến* đã chuyển xuống **Phụ lục A** (đặt sau tài liệu tham khảo) — nội dung
    giữ nguyên, chỉ dời chỗ; thân bài có một câu trỏ tới nó ở cuối Mục 6.
    ⚠️ **Phụ lục KHÔNG làm giảm tổng số trang**, chỉ giảm phần phản biện phải đọc.
    5 bảng + 1 hình đã xuất ảnh 300 dpi ở
    `paper/vcl2026/bang_anh/` theo yêu cầu *"bảng biểu phức tạp gửi kèm file ảnh"*, dựng
    lại được bằng `bang_anh.tex` (file này sinh tự động bằng cách trích khối `table`/
    `figure` từ `main.tex`, phải chạy lại mỗi khi thêm bớt bảng).
  · ⭐ **Đo độ dài 48 bài kỷ yếu VCL2025** (tải PDF 736 trang, tách theo mục lục): trung vị
    **14 trang / 6.270 từ**, p75 **19 trang / 6.976 từ**, dài nhất 33 trang / 10.755 từ;
    **bài của chính nhóm năm ngoái (#22, tr.325–336) là 12 trang / 5.475 từ, cũng giãn
    1,5**. Bản 24 trang / 10.427 từ xếp **46/48 theo số từ** ⇒ đã rút xuống **21 trang /
    8.827 từ**. Cắt: bỏ Bảng "bốn ô + lý do" (gộp vào danh sách gạch đầu dòng) · bỏ Hình
    cột chồng vì trùng số liệu với Bảng 4 (đưa 80,1/37,5/66,7 vào ghi chú bảng) · gỡ đoạn
    mượn số liệu bài đồng hành (68,5% · 7.067/10.319) ⇒ giảm luôn trùng lặp với FAIR · nén
    phần bình luận phương pháp ở mọi mục. **Không con số chốt nào bị mất**; bản trước khi
    rút ở `paper/vcl2026/_archive/main_TRUOC_RUT_TRANG_30_8.tex.bak`.
  · ✅ **Rà văn phong 30/8 (sau khi cắt): 19 chỗ.** Bỏ khẩu ngữ *trót lọt* · bỏ ẩn dụ thi
    đấu ở Mục 6.4 (*thắng · đối đầu · rác · sạch* → *nghiêng về · hai nguồn cho hai chuỗi
    khác nhau · chuỗi vô dụng*) · bỏ ẩn dụ *giải pháp chữa cháy* và *sức nặng* ở kết luận ·
    bỏ **câu hỏi tu từ** ở Mục 5 và tiêu đề chạy-vào dạng câu hỏi ở Mục 8 · viết *ba đóng
    góp* và *ba điểm phân định* thành câu trọn thay vì chuỗi câu cụt cùng nhịp (dấu hiệu
    máy viết) · bỏ lời dẫn chuyện trò *"Trước hết cần một khái niệm"*, *"Chỗ đáng giữ
    lại"*, *"mong là dùng lại được"* · sửa *"ô sạch 100%"* · sửa *"ba số liệu sau"* (nêu ra
    nhiều hơn ba) · ô trống Bảng 3 đổi `---` thành `-` · gỡ câu trỏ Phụ lục bị lặp.
    ⚠️ Tóm tắt vẫn **đúng 150 từ** sau khi sửa (đã đếm lại), không con số nào mất thêm.
  · ✅ **Rà văn phong lượt hai 30/8 (bỏ ẩn dụ + lối tu từ): 26 chỗ.** Bỏ ẩn dụ đời thường
    (*cái giá không chia đều · đảo tình thế · gánh nặng quy chiếu · miền giao diện **đẩy**
    cả người lẫn quy trình · sức ép · rò rỉ **trá hình** · chốt chặn · siết lại · lỗ hổng ·
    có mặt dày đặc · dồn vào ô thứ tư · bị nuốt · tự bù*), bỏ từ đánh giá theo cảm tính
    (*vô dụng* ×4 → *không dùng được*, *trông tốt hơn* → *cao hơn*), bỏ nhân hoá (*nhãn
    thừa nhận có mơ hồ*), bỏ lối nói chuyện (*Đó đúng là thứ mà…* → *Đây chính là…*), và
    đổi tiêu đề *"Truy một tỉ số 3,2 lần về tận cơ chế"* → *"Truy nguyên một tỉ số 3,2
    lần"*. Ghi chú Bảng 3 nay ghi rõ tầng nào ứng với số nào thay vì ba số nối bằng dấu ·.
  · ✅ **Ba agent quét lần cuối 30/8 (văn phong · số liệu · quy cách): 31 chỗ đã vá.**
    ⭐ **Phần ĐO lại sạch tuyệt đối một lần nữa** — agent dựng lại 25+ phép tính (kể cả
    $8.928-347=8.581$, bình quân trọng số cột mỏ neo ra đúng 27.628, toạ độ pixel Hình 1,
    bốn khoảng Wilson) đều khớp; 32 tham chiếu chéo đúng hết; 15 mục tài liệu tham khảo
    đều được trích, thứ tự APA đúng. **Cắt 4 trang không làm rơi số nào.**
    ⚠️ **Mọi lỗi bắt được đều ở CÂU CHỮ, đúng mẫu hình đã ghi nhận nhiều lần.** Ba lỗi
    nặng nhất là **pre-existing**, có sẵn từ trước khi cắt:
    · **"bài có BA mảnh bằng chứng ngoại sinh"** trong khi một trong ba (tỉ lệ 55,6% bước
      có cặp quy chiếu) tính từ **chính bộ nhãn**, và hai chỗ khác trong bài lại nói "một"
      ⇒ sửa thành **hai mảnh, cả hai đều dựa vào câu do người viết**.
    · **Tóm tắt nói mạnh hơn thân bài:** *"75,3% dấu hiệu nêu đủ thông tin để chỉ ra phần
      tử đích"* trong khi §6 dành nguyên đoạn phủ nhận đúng điều đó ⇒ đổi thành *"thuộc
      loại phân giải được mơ hồ"*.
    · **Tóm tắt gắn nhầm đối chứng:** "gấp bảy lần" là tỉ số của đối chứng **chặt** (7,6%)
      nhưng câu chữ tả đối chứng **lỏng** (5,4%, tỉ số 9,9 lần) ⇒ thêm *"trong cùng một
      chuỗi thao tác"*.
    Còn lại: **7,6% mang HAI nghĩa** (trùng tên · khớp nhầm) cách nhau sáu dòng trong kết
    luận ⇒ đã phá nhập nhằng · claim *"Bảng 2 có đúng một ví dụ"* về dữ liệu người dùng
    **không kiểm chứng được** từ chính bảng đó ⇒ gỡ · *"64.567 bản ghi OCR"* gán cho "toàn
    bộ ảnh" trong khi đó là số bước **tập dạy** ⇒ ghi rõ thêm 6.958 của tập kiểm · chữ
    "nhánh dữ liệu" dùng ở §3 mà định nghĩa nằm ở Phụ lục A ⇒ thêm trỏ · lời hứa *"với
    mỗi phép kiểm nêu cả phần không đạt"* không giữ được ⇒ hạ xuống "hai phép kiểm chính".
    Quy cách: **nhan đề Hình 1 đặt DƯỚI hình** (5 bảng đều đặt trên) ⇒ chuyển lên trên cho
    đúng APA 7th + template · ba tiêu đề cuối bài (TLTK · Phụ lục A · Thông tin tác giả)
    bị **canh trái** do khai lại `\titleformat` thiếu `\centering` ⇒ canh giữa lại.
    Văn phong: tiêu đề dạng câu hỏi cuối cùng · câu cụt không chủ ngữ · tic "Phải nói rõ"
    ba lần · nhịp ba câu cùng khuôn "Phía… Phía… Phía…" · nhân hoá "nhãn không nói điều gì
    sai" · "được phục vụ kém nhất" · "quy mô đủ" dùng 130 dòng trước khi giải nghĩa.
    ⛔ **Một lỗi của chính trợ lý, đã tự bắt và gỡ:** vá chỗ 7,6% nhập nhằng bằng phân số
    `141/1.848` — **tử số đó là suy ngược từ phần trăm đã làm tròn, không có trong dữ
    liệu**. Đúng dạng bịa số mà dự án cấm. Đã gỡ, thay bằng chữ "tỉ lệ khớp nhầm".
  · ✅ **DOI đã tra và vá 30/8 — 14/15 mục** (mục còn lại là bài đồng hành đang bình duyệt,
    chưa có DOI). Tra bằng **Crossref API** rồi **xác minh hai lượt**: `doi.org` trả 302 cho
    cả 14, và content negotiation (`Accept: application/vnd.citationstyles.csl+json`) trả về
    **đúng họ tác giả đầu, đúng năm, đúng tên bài** cho từng mã. ⛔ Không mã nào đoán.
    ⚠️ Ba mục NeurIPS (Deng · W. Li · Rawles) dùng DOI của **kỷ yếu in Curran Associates**
    (`10.52202/…`) vì trang chính thức `proceedings.neurips.cc` không cấp DOI — mã có thật,
    phân giải được, trỏ đúng bài. Script tra để ở scratchpad, chạy lại được.
    ⚠️ Đã thêm `\def\UrlBreaks{\do\/}` vào preamble để URL chỉ ngắt sau dấu gạch chéo,
    không ngắt giữa `doi.org`. Vẫn **20 trang, 0 overfull**.
  · ✅ **Tóm tắt viết lại 30/8 theo feedback user (5 chỗ "hơi tắt"), vẫn ĐÚNG 150 từ.**
    *phần tử đích* → **phần tử cần chạm** · bỏ hẳn cụm *nhãn bốn ô*, liệt kê thẳng bốn ô ·
    câu cụt *"dựng nhãn bốn ô… hoàn toàn bằng luật"* → **"Mỗi bước chạm… được gán tự động
    một dòng mô tả gồm… ; cả 41.099 dòng đều do luật sinh ra, không nhãn nào do người
    viết"** · *phân giải được mơ hồ* → **"tự nó đủ tách"**, và ô thứ tư nay được định
    nghĩa ngay trong tóm tắt là *"dấu hiệu tách nó khỏi các phần tử giống nó"* · *nguồn
    ngoài quy trình* → **"Quy trình không đọc câu chỉ dẫn do người viết, nên đây là phép
    so độc lập"**.
    ⚠️ **ĐÁNH ĐỔI phải nhớ:** trần 150 từ là cứng (thông báo 100–150 ∩ template 150–250),
    mà giải thích thêm tốn ~25 từ ⇒ **đã bỏ con số 12,6% khỏi TÓM TẮT** (vẫn còn 5 chỗ
    trong thân bài). Nếu user muốn giữ 12,6% thì phải bỏ câu cuối về bộ phép kiểm.
  · ✅ **Đổi thuật ngữ tự đặt 30/8:** *"cổng lọc"* → **"bộ lọc"** (13 chỗ, gồm cả tiêu đề
    Mục 5.1 và đoạn đóng góp ở Mục 1). *Cổng* là chữ dự án tự đặt, không phải thuật ngữ
    ngành; *bộ lọc* là cách nói chuẩn. Kèm theo: *"vượt được cổng"* → *"qua được bộ lọc"*,
    *"trượt cổng"* → *"bị loại"*.
  · ✅ **Vá chỗ dễ đọc nhầm ở Mục 1 (user hỏi 30/8, đã tra lại nguồn):** câu *"120 màn ngẫu
    nhiên… 12,6%… 22 màn trong số đó"* **đúng số liệu** — `report/100:200` ghi *"Đã đo trên
    120 màn ngẫu nhiên: trung vị 86 phần tử một màn, nhưng chỉ 12,6% phần tử có tên (22
    trên 120 màn không có phần tử nào có tên)"*, khớp cả ba con số. Nhưng cụm *"trong số
    đó"* đứng gần "99.131 màn" hơn "120 màn" ⇒ đổi thành **"22 trong số 120 màn ấy"**.
  · ✅ **THỐNG NHẤT MỘT TÊN 30/8 (user quyết):** *"phần tử đích"* → **"phần tử cần chạm"**
    ở **cả 23 chỗ**, gồm nhan đề Bảng 3, nhan đề và nhãn trong Hình 1. Không còn chỗ nào
    dùng *"phần tử đích"*. Bộ ảnh gửi kèm đã dựng lại theo.
  · ✅ **Rà thuật ngữ khó đọc, 9 chỗ (cùng lượt).** Nguyên tắc: thuật ngữ phải được giải
    nghĩa **trước hoặc ngay tại** lần dùng đầu, không được tham chiếu xuôi.
    · *cổng lọc* → **bộ lọc** (13 chỗ) · *bộ thước đo* → **phép chấm** (từ tự đặt).
    · Giải nghĩa ngay lần dùng đầu: **ô** (*"tức một trường thông tin trong dòng ấy"*) ·
      **bước chạm** (*"bước mà thao tác đúng là một cú chạm lên màn hình"*) · **chuỗi mục
      tiêu** (*"câu mô tả mục tiêu chung của cả tác vụ"*) · **mỏ neo chữ** (*"chuỗi chữ gần
      nhất nằm bên cạnh, dùng làm mốc để chỉ đường"*) · **phân giải được mơ hồ** (Mục 5.2
      dùng trước khi Mục 6.1 định nghĩa ⇒ thêm *"tức tự mệnh đề ấy đã đủ chỉ ra phần tử
      nào là phần tử cần chạm"*).
    · Gỡ tham chiếu xuôi: Mục 1 bỏ *"quy mô đủ"* và *"ngoại sinh"* (định nghĩa tận Mục 5.1
      và Mục 8) · Mục 5 bỏ *"nhánh đề xuất"* (định nghĩa nằm ở Phụ lục A).
    · *"các lát đọc thủ công"* → **lượt** (dùng sai nghĩa) · định nghĩa vòng tròn *"lát
      thử, tức lát 1.074 nhãn"* → **mẫu 1.074 nhãn**.
  · ✅ **Gỡ tiểu mục lẻ loi 30/8 (user chỉ):** Mục 3 chỉ có đúng **một** tiểu mục 3.1
    (*Phép kiểm ghép…*), chia mục như vậy là sai bố cục ⇒ gỡ `\subsection`, đổi thành tiêu
    đề chạy-vào `\emph{Phép kiểm ghép.}`, đồng bộ với cách Mục 8 đặt tên các phép kiểm.
    Đã quét lại cả bài: **không mục nào còn chỉ có một tiểu mục** (2 có 3 · 5 có 2 · 6 có
    4 · 9 có 2 · còn lại không chia). Không tham chiếu nào trỏ tới 3.1 nên không hỏng gì.
  · ✅ **Lượt rà cấu trúc câu 30/8 (agent thứ tư, user yêu cầu): 75 chỗ đã vá.** Yêu cầu
    của user: bỏ lối viết *"mệnh đề rồi dấu hai chấm rồi kể tiếp"*, mọi câu phải có chủ
    ngữ vị ngữ, câu nào không có chủ ngữ thì thêm trạng ngữ mở đầu.
    ⭐ **Lỗi NỘI DUNG bắt được trong tóm tắt:** *"$75,3\%$… nhưng còn $37,5\%$ ở nhóm chỉ
    mang một ký hiệu"* để người đọc hiểu $37{,}5\%$ là **tỉ trọng của nhóm** trong toàn bộ
    nhãn. Sai. Nhóm ấy chỉ chiếm **$4{,}4\%$** ($1.809/41.099$); $37{,}5\%$ là **tỉ lệ
    phân giải được BÊN TRONG nhóm** ($32{,}7+4{,}8$). Đã sửa thành *"riêng ở nhóm chỉ mang
    một ký hiệu thì tỉ lệ ấy còn $37{,}5\%$"*. Tóm tắt vẫn **đúng 150 từ**.
    · **51 chỗ dấu hai chấm** đã tách thành câu trọn hoặc nối bằng *vì · bởi · nên · gồm*.
      Giữ lại các chỗ hợp lệ: nhan đề bài, *"Từ khoá:"*, khoảng tin cậy Wilson, tỉ số
      $1{:}2{,}7$, và dấu hai chấm dẫn vào danh sách thật (ba thành phần · bốn loại chuỗi ·
      bốn nhóm · ba cỡ lát). Ba tiêu đề đoạn ở Mục 7 đổi `:}` thành `.}` cho đồng bộ Mục 8.
    · **14 câu thiếu chủ ngữ** đã thêm chủ ngữ hoặc trạng ngữ (*Chương trình…*, *Khâu
      này…*, *Bài còn kèm theo…*, *Con số này phải được đọc…*).
    · **21 chỗ viết quá tắt** đã nới: đại từ *nó · đó* trỏ mơ hồ, *"đạt 55,3%"* không nói
      chỉ số gì, *"72 ca"* chưa nói là ca nào, dải $80$–$350$ px và ô dấu hiệu phân biệt
      dùng trước khi định nghĩa, quan hệ từ *vì* dùng ngược ở Mục 9.2.
    ⛔ **Lỗi của chính trợ lý, tự bắt được:** lượt đổi *"phần tử đích"* → *"phần tử cần
    chạm"* trước đó dùng khớp chuỗi thẳng nên **bỏ sót 3 chỗ bị ngắt qua hai dòng**; grep
    báo 0 nên tưởng xong. Đã đổi nốt bằng khớp có `\s+`. **Bài học: mọi lần tìm/thay trên
    tệp `.tex` phải khớp linh hoạt khoảng trắng, vì tex xuống dòng giữa cụm từ.**
    ⚠️ Tách câu làm bài dài ra: **20 → 21 trang**. VCL không giới hạn trang.
  · ⚠️ **Còn treo (cần user quyết):** hậu tố `2020a/2020b` áp cho **hai nhóm tác giả khác nhau**, đúng luật APA §8.19 thì
    phải phân biệt bằng tên đồng tác giả chứ không phải chữ cái (rủi ro thấp, phổ biến
    trên thực tế) · font là **TeX Gyre Termes** chứ không phải Times New Roman thật (máy
    không có font Microsoft; PDF nhúng tên "TeXGyreTermes").
  · ⚠️ Đã chạm sàn: thân bài 17 trang là nội dung thật, mật độ ~490 từ/trang, không trang
    nào phí chỗ. Muốn ngắn hơn nữa phải **bỏ hẳn một phân tích**, không còn chỗ nén câu chữ.
  · ✅ **Mục THÔNG TIN TÁC GIẢ là BẮT BUỘC** — tra lại CFP 30/8, nguyên văn thể lệ:
    *"cuối báo cáo ghi rõ tên thật, bút danh (nếu có), học hàm, học vị, nơi công tác, địa
    chỉ, số điện thoại, email"*. Đừng gỡ để tiết kiệm trang. Cùng lượt tra xác nhận: tóm
    tắt **100–150 từ**, từ khoá **tối thiểu 5**, Times 12 giãn 1,5, APA 7th, bảng phức tạp
    gửi kèm ảnh.
  · ✅ **Mục *Thông tin tác giả* đã xong 30/8** — user quyết **không để số điện thoại của
    thầy Long** (chỉ tác giả 1 có số) và **bỏ dòng "Hướng quan tâm" của cả hai**. Còn lại:
    tên thật · ghi rõ không dùng bút danh · học vị · nơi công tác · địa chỉ · email, đặt ở
    cuối báo cáo đúng thể lệ.
  · ⚠️ **Chưa chuyển được sang `.docx`** — máy không có `pandoc` lẫn `libreoffice`. Thông
    báo không nói rõ bắt buộc Word; nếu ban tổ chức đòi thì phải chuyển trên máy khác.
  · ✅ **ĐÃ KIỂM 29/8 — chính sách trùng lặp: rủi ro ĐÓNG.** Tra tận nguồn cả hai phía:
    · **VCL KHÔNG có điều khoản nào** về bài chưa từng công bố, nộp đồng thời, bản quyền
      hay đạo văn. Kiểm ba lượt độc lập: `vcl.huflit.edu.vn/event/4/` (CFP VCL2026),
      trang overview của chính sự kiện đó, và `event/3` (VCL2025 — cũng không có).
      Thể lệ VCL chỉ nói về quy cách, số báo cáo tối đa và thông tin tác giả.
    · **FAIR CÓ điều khoản**, nguyên văn thể lệ: *"Submissions must be original and not
      under consideration for publication elsewhere"*; bản tiếng Việt ở `fair.conf.vn` nói
      bài phải **chưa từng công bố**, **không gửi đăng đồng thời**, kèm **cam kết bản quyền
      IEEE**.
    · ⭐ **Phán quyết: không vi phạm.** Điều khoản FAIR áp cho *cùng một bài* gửi hai nơi.
      Đây là **hai bài khác nhau** — VCL là nhãn quy chiếu + đường ống dựng dữ liệu (tiếng
      Việt), FAIR là đóng góp mô hình (tiếng Anh) — chia số độc quyền theo bảng phân số ở
      mục *Hai bài báo*, phần chung chỉ là quy mô dữ liệu. Việc **trích chéo dạng "đang bình
      duyệt" chính là cách khai minh bạch**, nên giữ nguyên, đừng gỡ.
  · ⚠️ **Ba thông tin mới lộ ra khi tra CFP, chưa từng ghi ở đâu:**
    · **VCL thu phí 1.000.000 VNĐ cho mỗi báo cáo được duyệt**; tác giả tự lo đi lại.
    · **Hạn FAIR lệch giữa hai cổng:** EasyChair CFP ghi **15/8** (đã đóng), `fair.conf.vn`
      ghi **31/8** qua EDAS. Khớp với ghi chú cũ; nộp qua **EDAS**, không phải EasyChair.
    · **FAIR giới hạn 5 từ khoá** — bài FAIR đang có **đúng 5**, vừa sát trần, đừng thêm.
      Kèm theo: tối đa 8 trang, IEEE MS Word template, tiếng Anh, **một** corresponding
      author, và **tác giả thứ nhất là người trình bày**.
    · ⚠️ Thể lệ VCL2025 ghi **Times 13**, VCL2026 đổi thành **12** — câu "Times 13" ở ghi chú
      cũ hoá ra đúng, nhưng đúng cho **năm ngoái**; năm nay là 12.
  *(Cách chia hai bài đã chốt lại 23/8: FAIR = bài mô hình, VCL = nhãn mô tả phần tử.)*

**Đã chết, đừng hồi sinh:** nhánh **faithfulness trên MobileViews** (đóng góp phụ số 2 theo
`report/103` ngày 1/8). Kiểm 18/8: **0 lần xuất hiện** trong `report/106 · 108 · 109 · 112 · 113 ·
114`, trong `paper/fair2026/main.tex` lẫn `thesis/main.tex`. `report/103` là chỗ cuối cùng còn
nhắc tới nó ⇒ khi 103 mâu thuẫn với các file 106+, **106+ thắng**.

---

## ✍️ Ghi chú làm việc cho trợ lý

- Trao đổi bằng **tiếng Việt**.
- **Văn phong:** dùng từ **tự nhiên**, KHÔNG lộ giọng AI-gen. Cấm tự chế thuật ngữ rồi dùng như
  thể chuẩn ngành — đã từng mắc: *"bản kê nút"*, *"bản thiết kế màn hình"* (tên thật là **View
  Hierarchy / VH**; thầy là tiến sĩ AI nên biết thuật ngữ), *"trung-thực-hoá"*. Tránh các cụm máy
  móc: "Nói một câu:", "Điểm mấu chốt", "đáng nói nhất", "gói gọn", lạm dụng gạch ngang dài.
- **Yêu cầu kép:** vừa dễ hiểu cho người không chuyên, vừa đủ hàm lượng khoa học (công thức +
  citation đúng venue) để thuyết phục một **tiến sĩ AI khó tính**. Cách làm: lời thường trước,
  "hộp kỹ thuật" kèm công thức và trụ trích dẫn sau.
- **Chống trùng lắp:** trước khi thêm nội dung vào một file report, kiểm xem đã có ở mục khác
  chưa. Giữ layer **pitch → giải thích → công thức**; mỗi layer phải THÊM thông tin.
- **Trước khi một khẳng định vào bài, mở lại NGUỒN, không mở lại ghi chú.** Chữ *"đã xác minh"*
  trong ghi chú của chính mình không phải bằng chứng — hai khẳng định về bộ trỏ sống 18 ngày, đi
  vào bản thảo, rồi bị lật bởi một lần mở đúng Bảng 1. Tài liệu tả thước phải đọc từ **mã**,
  không từ ý định.
- Citation: chỉ trình peer-reviewed như đã bình duyệt; verify venue/năm trước khi trích.
- Tư vấn model/giá/API Claude/Anthropic: đọc tài liệu, KHÔNG trả lời theo trí nhớ.
- Sau thay đổi lớn: cập nhật file report tương ứng và cập nhật file này khi có quyết định mới.
