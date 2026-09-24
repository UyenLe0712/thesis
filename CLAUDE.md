# CLAUDE.md — Bối cảnh luận văn (auto-load mỗi phiên)

> **Dọn lần hai 9/9/2026** (2.043 → ~1.400 dòng): nén nhật ký của những việc đã đóng — sprint sáu
> lượt `gui_sel`, nhật ký "chương nào thêm mục nào" của ba bản luận văn — rồi **bỏ hẳn hai mục về
> hai bài báo FAIR và VCL vì cả hai đã nộp** (user quyết 9/9). Số đo, luật đọc và bài học TeX nằm
> trong hai mục ấy đã được chuyển sang các mục tương ứng, **không mất cái nào**; chi tiết hai bài
> nay tra ở chính thư mục bài. Bản đầy đủ trước khi dọn:
> `report/_archive/CLAUDE_MD_TRUOC_DON_9_9_2026.md`.
> Lần dọn trước 18/8/2026: `report/_archive/CLAUDE_MD_TRUOC_DON_18_8_2026.md` (có nhật ký chạy máy
> tháng 7–8 và khung prompting cũ đã bị bác).
> (thư mục `_archive/` **không có trong bản GitHub** — tệp vẫn nằm trên máy và trong lịch sử git).
> Mở hai file đó khi cần tra *"vì sao hồi đó quyết định X"*, không phải để biết trạng thái hiện tại.

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
| **⭐⭐⭐⭐⭐⭐⭐ PATA-C1: KẾT QUẢ CUỐI 25/9 — localizer học được vị trí (hit 52% vs prior 5%) nhưng CỔNG CUỐI KHÔNG ĐẠT (bridge không đổi nội dung câu) ⇒ dừng, không C0-Loc — tự chứa, đọc §5b–5c trước** | **`report/194_TIEN_DO_PATA_C1_VA_QUYET_DINH_MOC_800_24_9.md`** · cổng H ĐẠT · C1 hết epoch 24/9 · ⛔ **CỔNG CUỐI C1 KHÔNG ĐẠT 25/9 (§5c)**: đk 5 trượt (−0,37 điểm), bật−tắt bridge chỉ +0,17 điểm exec ⇒ bridge không truyền vị trí vào câu; **không chạy C0-Loc, không mở test** |
| **⭐⭐⭐⭐⭐⭐ KL BOX LỚN — CHỐT `area_share ≥ 0,50` thì tắt KL (CE giữ), THẮNG 186 §4b (0,25 là sai: 10/18 từ mẫu lấy dư, không nhân với 883)** | **`report/193_QUYET_DINH_KL_BOX_LON_PATA_C1_23_9.md`** · đã thi hành: Train-proper kl_ok 39.432 |
| **⭐⭐⭐⭐⭐⭐ TÌNH HÌNH PATA 23/9 (mã chặng A, test, audit 2,7%, việc kế)** | **`report/186_TINH_HINH_PATA_C1_23_9.md`** |
| **⭐⭐⭐⭐⭐⭐ PHƯƠNG PHÁP ĐANG CHỐT 23/9 — PATA-Causal (TARGET token + localizer KL + bridge ở block 17), prefix sạch S(2 ep)→H(1 ep)→C1(1 ep); C1 chạy trước, C0-Loc chỉ khi C1 qua cổng §8. **User 23/9: S chỉ 1 epoch.** Chặng A (0 GPU) đã viết + 13/13 test đạt trên mô hình tí hon; việc kế = audit box (tay) + Kaggle `harness/kaggle_pata_test.md`** | **`report/185_CHOT_PHUONG_PHAP_ACTION_PATA_CAUSAL_22_9.md`** (chép từ 9 ảnh, gốc ở `report/anh_185_pata_causal_23_9/`) |
| **⭐⭐⭐⭐⭐ BÀN GIAO 22/9 — THƯỚC ĐÃ CHỐT + DCRP; KẾT QUẢ G0 = FAIL (trần +0,97) ⇒ rút preference, không train; việc còn lại: UI-Venus 5 nhánh + viết chẩn đoán âm** | **`report/183_BAN_GIAO_METRIC_VA_DCRP_CHAY_THU_22_9.md`** (chép từ ảnh; mục *KẾT QUẢ G0*) · mã `harness/g0_mention_x_exec.py` · `m9_khop_mem.py` · `m2_m3_compare.py` · log `runs/g0/` |
| **⭐⭐⭐⭐ BÀN GIAO 14/9 CHO PHIÊN DEBATE CHỐT ĐÓNG GÓP MÔ HÌNH — tự chứa: bộ ba số chính (AitW 77,3 · D.3 67,0 · exec 60,1), mọi phép so ghép cặp kể cả S2, điểm nghẽn, mọi hướng đã thử, ràng buộc, luật chơi mới về thước** | **`report/155_HANDOFF_DEBATE_DONG_GOP_MO_HINH_14_9.md`** (thắng `146`) |
| **⭐⭐⭐ LỘ TRÌNH ĐANG THI HÀNH (9/9) — bốn chặng, phụ thuộc, checkbox; §0 ghi năm chỗ `151` mô tả khác máy WSL** | **`report/152_LO_TRINH_SAU_151_9_9.md`** · runbook chặng 3: `harness/kaggle_phase1_noisuy_9_9.md` |
| **⭐⭐⭐ BẢN THI HÀNH 8/9 — THẮNG MỌI FILE VỀ *việc làm tiếp* VÀ *thước để báo*: phương pháp mới **VIS-SFT** (mở băng thị giác, một biến so S1/101), thước ba vai (tiêu đề `exec` 60,07 · báo kèm D.3 67,04), ba phase, bốn bẫy mất buổi** | **`report/151_BAN_CHOT_CUOI_PHUONG_PHAP_VA_THUOC_7_9.md`** (bản chép từ 31 ảnh; ảnh gốc `report/anh_chot_phuongphap_metric_9_9/`) |
| **⭐ TRẠNG THÁI HIỆN TẠI — đọc một mình là hiểu, từ 23/8 trở đi** | **`report/119_TRANG_THAI_SAU_23_8.md`** |
| **⭐⭐⭐ NGUỒN THẮNG 4/9 — chốt thi hành + khoa học sau G6, thắng 124·128·132·133** | **`report/134_CHOT_4_9_HANDOFF_CHAT.md`** (đọc một mình là đủ; §14 là phần đo trên WSL) |
| **⭐⭐ KẾT QUẢ `exec` CỦA `gui_sel`/101 — đo 5/9, n=4.463** | **`report/136_KET_QUA_EXEC_GUI_SEL_5_9.md`** |
| **⭐⭐⭐ TRỤC MỚI 5/9 CHIỀU — bỏ SOICT, tra cứu nâng số + ba phép đo 0 GPU, ba việc theo thứ tự** | **`report/138_RESEARCH_NANG_SO_5_9.md`** |
| **⭐⭐ LƯỢT GRPO `<point>` — khai báo +2,56 pp (p=1,3e−08) nhưng `exec` chỉ +0,02 ⇒ 60,07 = điểm tiêu đề hiện hành; tám đòn phản biện** | **`report/144_KET_QUA_GRPO_POINT_6_9.md`** · `report/106` (x19)+(x19d)+(x20) · `harness/doc_exec_grpo.py` |
| **⭐⭐⭐ DEBATE NÂNG SỐ MÔ HÌNH 5/9 TỐI — 65 cần 82,1% khai báo đúng (ngang UI-TARS-72B), 70 cần 89% (vượt mọi agent); khối ứng viên KHÔNG thêm thông tin nhận diện (sel đúng chỗ MIN sai chỉ 3,8%); ⭐ KHUYẾN NGHỊ CUỐI §4.3 = RLVR-GRPO tiếp từ MIN, thưởng `<point>` đúng ±14% (miễn phí, không Goodhart), kỳ vọng +2…+4; đường lùi ORPO ngoại tuyến cặp lấy mẫu** | **`report/143_DEBATE_NANG_SO_MO_HINH_5_9.md`** |
| **⭐⭐⭐ KẾT QUẢ τ 5/9 TỐI — null thắng (C +8/1.400), lượt ② KHÔNG chạy, nhánh ứng viên ĐÓNG; chẩn đoán khâu bỏ cuộc mù (AUC 0,69–0,72), trần bỏ cuộc hoàn hảo 78,0** | **`report/142_KET_QUA_TAU_5_9.md`** |
| **⭐ PHẢN BIỆN luật D.3 — 48% hộp là nút con, 78% mức tăng từ hộp rộng, 120 bước container; con số nên dùng là D.3∧14% = 79,23** | **`report/139_PHAN_BIEN_LUAT_D3_5_9.md`** |
| **⭐ TIỀN LỆ THƯỚC BỘ TRỎ (tra 5/9): cơ chế đã có ở REG/VLN, miền GUI chưa thấy ai chấm câu-cho-người bằng bộ trỏ; bảng 10 họ thước khác; §6 = BLEU/ROUGE/action_ok đủ 8 nhánh (`harness/text_metrics.py`)** | **`report/141_TIEN_LE_THUOC_BO_TRO_5_9.md`** |
| **⭐ LUẬT QUYẾT lượt ② đã khoá trước khi có điểm τ (x17)** | `report/106` mục **(x17)** · mã: `harness/quet_tau.py` · `harness/luat_d3.py` |
| **⭐⭐ NÂNG TRẦN THƯỚC — luật D.3 gốc của AndroidControl, đo 5/9, 0 giây GPU** | **`report/140_NANG_TRAN_LUAT_D3.md`** |
| **⭐ LUẬN VĂN + DECK BẢO VỆ đã đồng bộ tới 5/9 (114 trang · 26+12 slide)** | mục *Luận văn — ĐÃ ĐỒNG BỘ TỚI 5/9* trong file này · `thesis/chapters/` · `slides/build/build_baove.js` |
| **bài SOICT 2026 (21/9, EasyChair mở tới 25/9) — thước: tách cổng loại thao tác khỏi hình học; nguồn chép từ 15 ảnh; ĐÃ NỘP 21/9, EasyChair #5577 (còn thêm đồng tác giả trước 25/9)** | `paper/soict2026/README.md` · `paper/soict2026/main.tex` |
| hai bài báo đã nộp (FAIR · VCL) — chỉ còn chờ hồi âm EDAS | mục *HAI BÀI BÁO — ĐÃ NỘP* trong file này · `report/118` (phân số) · `report/129·130·131` (FAIR) · `paper/vcl2026/README.md` |
| prompt research gửi mô hình phiên khác (tự chứa) | `report/137_PROMPT_RESEARCH_CHO_FABLE.md` |
| tiền lệ cho trục bỏ cuộc / risk-coverage của SOICT (tra 4/9) | `report/135_TIEN_LE_ABSTENTION_SOICT.md` |
| SPRINT `gui_sel`: context debate ngay sau G6 (3/9) — ⛔ **`134` thắng file này** | `report/133_CONTEXT_DEBATE_SAU_G6.md` · nhật ký thi hành ở `report/132` mục 16–19 |
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
| phân tích bốn nhánh + sàn | `report/113_PHAN_TICH_BON_NHANH.md` |
| tiền lệ đã tra (executability, Zhao, GCoT) | `report/114_TIEN_LE_CAN_XAC_MINH.md` |
| nhật ký chạy máy Colab chi tiết | `report/110_PHIEN_0_COLAB_11_8.md` |
| script trình bày với thầy | `report/111_SCRIPT_GAP_THAY_12_8.md` + `slides/LUAN_VAN_SLIDE.pptx` |
| nguồn từng con số trong bảng trích từ bài khác | `report/105_NGUON_SO_BANG_GOC.md` |

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

### ⛔ SPRINT `gui_sel` 30/8 — ĐÃ DỪNG Ở G6, giữ lại ba quyết định còn hiệu lực

Sprint sáu lượt (`gui_sel` / `gui_sft_match` / `S1-match` × hạt 101+202) **không còn chạy** — cổng
G6 trượt 3/9, rồi `134` thu còn một lượt, rồi `151` bác luôn `gui_sft_match` bằng số. Toàn văn ở
`report/126` · `report/128`. Ba điều **vẫn áp**:

⛔ **KHÔNG đổi backbone sang Qwen3-VL-4B** (user quyết 30/8). Bốn lý do đo được: ① trần cơ chế
**67,2%** bị chặn bởi **độ phủ khối ứng viên**, không phụ thuộc backbone, mà lát chọn đúng đã bão
hoà (MIN 85,2% vs người 85,7%) ⇒ đổi backbone mua tối đa **~2 pp**; ② căn cứ đổi là ScreenSpot
(benchmark **định vị**) trong khi mô hình này **không định vị** — UGround làm việc đó; ③ giữ 3B mới
có ngân sách cho nhánh tách công của menu; ④ 4B chưa từng chạy, kịch bản xấu 112–148 h là vỡ
ngân sách.

⛔ **`gui_orpo_hard` ĐÃ CHẾT.** Hai nhánh ORPO **cùng có** khối ứng viên nên khối triệt tiêu trong
hiệu số; và toàn bộ công của ORPO-khó chồng SFT **đã đo rồi = +0,63 pp exec** (CE2/101 59,42 →
MIN/101 60,05; `sel_acc` 65,70 → 66,55), muốn chạm ngưỡng Dương +2,8 phải gấp **4,4×**. Cộng
**(x13c)**: lỗi khai báo lệch trung vị **351 px**, 76,5% ngoài dải vế âm khó ⇒ tiền đề "vế âm khó"
sai — **đúng lý do MIN-ONPOLICY đã chết**.

⛔ **Bốn cách kéo Δ cho đẹp vẫn bị cấm** (bỏ khối khỏi nhánh so sánh / so vs S1 / train ORPO / đổi
luật Voronoi). `sel_acc` **là thước phụ, không phải headline**.

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

### ⭐⭐ 5/9 — LUẬT D.3 NÂNG TRẦN 75,73 → 83,82 MÀ KHÔNG NỚI LỎNG (`report/140`)

Nguồn: **Li et al., AndroidControl, NeurIPS 2024 D&B, Phụ lục D.3** — luật GỐC của chính bộ dữ
liệu: *"if the target element's coordinates are within the bounding box of the ground truth
target element, it is considered as matching"*. Hộp có sẵn trong `descriptors.jsonl` (phủ
4.448/4.448) ⇒ tính lại từ `*_raw.jsonl`, **0 giây GPU**. Bảng đủ 9 hàng ở khối *9/9 — D.3 tái
lập được* bên dưới; `runs/luat_d3.json` · `harness/luat_d3.py`.

⭐ **Thứ tự tám nhánh không đổi chỗ nào**, S1−Base giữ 11,89 (Voronoi 11,52).
⭐ **Phép kiểm quyết định — D.3 KHÔNG nâng sàn** (cùng lát 800): trần 74,88 → **83,00** (+8,12)
trong khi sàn câu rỗng 12,00 → 14,12 (+2,12) và sàn sai màn 6,12 → 8,62 (+2,50) ⇒ **dải dùng
được nới từ 62,88 lên 68,88**. Đối chiếu: luật chữ nhật kéo sàn lên **20,50** — đó mới là nới
lỏng thật, và đó là lý do nó bị bác 30/8.
⭐ **Vì sao không phải nới lỏng:** dung sai của D.3 **thích ứng theo cỡ phần tử**. Theo chiều dọc
hộp thật có trung vị **5,2%** màn, chặt hơn cửa sổ ±14% tới **5 lần**; nó chỉ lỏng hơn ở phần tử
thật sự rộng, và lỏng đúng nghĩa vật lý (chạm chỗ nào trong phần tử cũng kích hoạt).
⛔ Nhưng nó vẫn được tính **sau khi đã thấy mọi điểm** ⇒ trình như **thước báo kèm** cạnh
Voronoi, khai rõ nguồn và thời điểm tính; **giữ Voronoi làm headline** vì đó là thước niêm 5/8.
⚠️ Phản biện ở `report/139`: 48% hộp là nút con · 78% mức tăng từ hộp rộng · 120 bước container
⇒ **không bỏ, không đưa vào bảng chính**; con số nên dùng kèm là D.3∧14%.

⛔⛔ **BỎ cách trình "79,3% năng lực của người"** (`report/140` mục 2) — **đã gỡ khỏi luận văn 5/9,
đừng đưa lại**. Chuẩn ngành trong sinh ngôn ngữ có mốc người là **hai số tuyệt đối cạnh nhau +
chữ headroom**, không chia tỉ lệ — Zhao et al. EACL 2021 in **Human 75,1** cạnh EnvDrop 47,7;
AndroidWorld ICLR 2025 in mốc người 80,0 cạnh M3A 30,6. Và 79,3% có **hai lỗi**: nếu viện công
thức chuẩn hoá hai mốc của Mnih et al. (Nature 2015) thì phải trừ sàn ⇒ MIN-DESC là **75,4%**;
mà 75,4% cũng sai vì sàn 12,0 đo trên lát 800 còn 60,05 đo trên 4.463. Cộng bẫy: Mnih thao tác
hoá *"ngang người"* = **≥75%**, in 75,4% là tự tuyên bố ngang người.
✅ Cách đúng: gọi 75,73 là **"ước lượng thận trọng về năng lực của câu chuẩn, đo qua cùng dụng
cụ"** (Nangia & Bowman ACL 2019), in hai số cạnh nhau.
⭐ **Chống lưng khi bị hỏi "60% thấp quá":** trần 75,7 là **giới hạn dụng cụ** (72% ca mù do bộ
trỏ lệch >14%; lọc câu chuẩn ≤3 từ trần chỉ lên 77,0), và thước này **chặt hơn quy ước lĩnh vực**
— thêm một tầng, câu phải đủ để một mô hình độc lập trỏ trúng ⇒ **cấm so thẳng 60% với 70–80% của
bài dùng thước khớp toạ độ trực tiếp**.

⭐ **Jandial et al. nay xác minh được venue: Findings of ACL: EACL 2026, tr. 2772–2785.** Bảng 1
cho căn cứ MỚI để giữ UGround: **UGround-V1-7B bền nhất trước cách diễn đạt khác nhau**
(s_mean 0,3176) dù ScreenSpot-Pro chỉ 31,1. ⚠️ Dự án dùng bản **2B** (0,6218) — khai đúng biến thể.
⭐ **Phi-Ground-4B (MIT, nền Phi-3.5-Vision)** là ứng viên **duy nhất** đóng được đồng thời đòn
"quen AndroidControl" và đòn "cùng họ Qwen"; chạy trên đúng lát 2.532 của phép B.
⚠️ Luật đọc mới: nhiều bài 2025–2026 không nhắc AndroidControl nhưng **mượn gói dữ liệu** của mô
hình khác vốn có nó (GTA1 ← OS-Atlas · SE-GUI ← UGround) — phải truy thêm một tầng.

**▶️ SPRINT `gui_sel` (3/9): ⛔ CỔNG G6 TRƯỢT, sprint sáu lượt DỪNG.** `sel_acc` **57,5%**
(580/1008) so với ngưỡng khoá trước **63,6%** — kém 6,1 điểm. Đã xác minh ba lượt: 100% có thẻ
`<sel>` · 99,6% tên nằm trong khối ứng viên · n=1008.

⭐ **Hai phát hiện đáng giá hơn con số cổng, cả hai tái lập hiện tượng đã biết:**
· **Điểm nghẽn là NHẬN DIỆN, không phải ĐỊNH VỊ — tỉ số 34:1** (điểm-đúng-tên-sai 34 vs
  tên-đúng-điểm-sai 1). Khi sai, mô hình nhìn sang **vùng khác hẳn màn** (khoảng cách trung vị
  398/1000, chỉ 25,8% trong hai lần dung sai) ⇒ tái lập dạng lỗi lưỡng cực của MIN-DESC (x13c).
· **Lẫn loại thao tác là dấu hiệu mạnh nhất của bỏ cuộc**: 39,6% ca bỏ cuộc có câu mang động từ
  không-chạm so với **2,0%** ở ca đưa ra lựa chọn — gấp 20 lần ⇒ tái lập chẩn đoán 4j-18.

⛔ **Cái bẫy của thước:** `sel_acc` chỉ đếm nhóm có ứng viên vàng (đúng cột *HasAns* của SQuAD 2.0
báo một mình) nên **bỏ abstain hoàn toàn kéo nó 57,5 → 69,5 trong khi độ đúng trên cả 1.400 bước
giảm 63,3 → 50,0**. Thước do chính dự án đăng ký đã dẫn dự án sai.

**⭐ CHỐT 4/9 (`report/134`)** — sáu quyết định vi mô M1–M4 (phương pháp) + E1–E2 (thước) đã khoá.
Còn hiệu lực: headline là **exec Voronoi gated .14 trên n=4.463** · `sel_acc` là thước phụ ·
readout **bộ ba kiểu SQuAD 2.0 + risk tại coverage cố định** · **3.062 bước là one-look hậu kiểm,
KHÔNG phải hold-out đăng ký trước** (`132`–`133` gọi sai thuật ngữ). ⛔ Vế lịch SOICT và lượt A100
đối chứng **đã huỷ 5/9**.

⭐ **Đo trên WSL 4/9 (`report/134` §14), 0 giây GPU:** cổng **Sel-B ĐẠT** — md5 `train_ac/ocr.jsonl`
khớp tuyệt đối, `train.jsonl` 64.567 dòng, prompt hai nhánh trùng byte **64.567/64.567**, target
trùng 0/64.567. Vế *artifact → câu nhắc* của **Sel-A cũng đóng**: SHA-256 của 1.400 câu nhắc tái
dựng = `30012d53fdbc…`, 0 bước thiếu khoá ứng viên. Hash pin ở
**`runs/sel/manifest_selA_selB_4_9.json`**. Ba số tái lập độc lập: bước chạm `click` 4.446 +
`long_press` 17 = **4.463** · lát dev 1.400 nằm trong 2.222 bản ghi đầu · phần còn lại 3.063 →
**3.062 / 891** sau khi loại đúng một episode trùng (`18852`, 1 bước).

✅ **Đã vá 4/9:** `infer_branch.py` nay **fail-closed** khi thiếu khoá ứng viên — kiểm phủ toàn tập
**trước khi nạp mô hình** (hỏng thì hỏng trong 2 giây, không phải sau 5,6 giờ Kaggle) + `assert`
tại chỗ dựng câu nhắc. Trước bản vá, `cands.get()` trả `None` im lặng và câu nhắc tụt về bản 24
dòng OCR mà không có gì báo lỗi.

### ⭐⭐ 5/9 — `gui_sel`/101 ĐÃ CÓ ĐIỂM `exec`: **56,13%** [54,24 · 57,99], n=4.463

Suy luận 3.063 bước mất ~2,1 h trên Kaggle T4, chấm 4.463 bước xong trong cùng commit. Toàn văn:
**`report/136`**.

| luật | Human | MIN | S1 | Base | **gui_sel** |
|---|---|---|---|---|---|
| Voronoi .14 (primary) | 75,73 | 60,05 | 59,11 | 47,59 | **56,13** |
| nL2 .14 (secondary) | 84,09 | 68,32 | 66,92 | 55,28 | **63,52** |
| chữ nhật .14 (gated) | 84,23 | 68,72 | 67,24 | 55,86 | **63,86** |

⭐ **Cơ chế chọn KHÔNG hỏng — cái sai là bỏ cuộc quá mức.** Bảng 2×2: **HasAns · đưa ra lựa chọn
đạt `exec` 71,41%** (n=2.326) [69,54 · 73,21], chỉ kém mốc câu chuẩn 4,3 pp và cao hơn mọi nhánh
đã train; **HasAns · bỏ cuộc sai chỉ 23,74%** (n=872). Over-abstention trên HasAns = **27,27%**,
**tái lập chính xác** mức 27,1% đo trên lát dev 1.400 hôm 3/9 (hai phép đo độc lập, mẫu chênh ba
lần). Triệt tiêu được vế bỏ-cuộc-sai ⇒ `exec` **56,13 → 65,44 (+9,31 pp)**.

⭐ **Bốn dấu hiệu của bỏ cuộc, ba cái tái lập hiện tượng đã biết:** động từ không-chạm **28,30%
vs 0,97%** (gấp 29 lần) · sai số bộ trỏ trung vị **19,90% vs 0,78%** bề ngang, p90 vượt 100% màn
(lỗi lưỡng cực) · **khối ứng viên càng đông càng bỏ cuộc, đơn điệu** 15,7% → 33,2% khi cỡ khối đi
từ 6–10 lên 40, `exec` giảm 70,5 → 51,8 (⚠️ tương quan hậu kiểm, không phải nhân quả) · app chưa
thấy bỏ cuộc 51,3% vs 41,8% (n=78). ⛔ **Đã loại:** độ dài câu — trung vị 33 ký tự ở cả hai nhóm.

⚠️ **Bẫy tên trường:** `exec_disk` trong JSON của `score_run.py` là `hit_disk` **thuần**, KHÔNG
gated. Hàng "chữ nhật .14" phải tính lại từ tệp thô (66,35 ungated vs 63,86 gated).

⛔ **Không có `Δ_sel`** — nhánh so sánh `gui_sft_match`/101 không chạy. Bảng McNemar so với
S1/MIN/CE2 (−2,98 / −3,92 / −3,29) **KHÔNG phải Δ hợp lệ**: lệch ba biến (cutoff 3072 vs 2560 ·
có menu vs 24 dòng OCR · 1 epoch vs 2). Hàng đọc được là **so Base: +8,54 pp** (p=6,8e−31).

**⛔⛔ QUYẾT ĐỊNH 5/9 CHIỀU — BỎ HẠN SOICT 16/9, KHÔNG CHẠY A100 ĐỐI CHỨNG (user quyết).**
Lý do user nêu: *"cái tôi cần là số cao"*. ⇒ Mọi ràng buộc *"không làm trước 16/9"* của
`report/134` mất hiệu lực (chúng bảo vệ hạn SOICT), nhưng **luật khoa học của `106` giữ nguyên**:
không đổi thước headline, không nới ngưỡng sau khi thấy điểm, một hạt giống = TRẮNG.

⭐ **Trục `report/138_RESEARCH_NANG_SO_5_9.md`** — tra cứu 28 nguồn + ba phép đo 0 GPU:
· ghép `gui_sel`; `none` → MIN = **60,72** (kịch trần của đồ đã có, vẫn TRẮNG; mọi luật ghép tinh
  vi hơn đều thấp hơn) · hợp nhất hai bộ trỏ UGround ∪ UI-Venus: trần câu chuẩn **79,0 → 87,7**
  (300 bước, luật 14%), S1 **52,84 → 56,71** trên 2.532, **giữ nguyên S1−Base** · bỏ cuộc theo vị
  trí ứng viên vàng trong khối có **hình chữ U** (giữa 31,4% vs đầu/cuối 27,2/24,3) — tái lập
  "lost in the middle".
· ⛔ Không có thước hợp lệ nào cho trần 95%; hợp nhất bộ trỏ tối đa ~87,7–90 và nâng **đều** mọi
  nhánh, nên tỉ lệ mô-hình/trần gần như không đổi.
· Ba việc của trục này **đã đóng cả ba**: ① τ (null thắng, xem khối 5/9 tối) · ② `gui_sel_cham`
  không chạy theo (x17b) · ③ D.3 đã tính.

### ⭐⭐⭐ 8/9 — BẢN THI HÀNH `151`: MỞ LẠI **MỘT** LƯỢT A100, PHƯƠNG PHÁP MỚI **VIS-SFT**, THƯỚC BA VAI

Nguồn: **`report/151_BAN_CHOT_CUOI_PHUONG_PHAP_VA_THUOC_7_9.md`** (chép từ 31 ảnh nhận 9/9; ảnh
gốc ở `report/anh_chot_phuongphap_metric_9_9/`). File đó **thắng mọi tài liệu khác** về *việc phải
làm tiếp* và *thước để báo*. Ngân sách: **50 h A100** + T4 miễn phí 30 h/tuần.

⭐ **PHƯƠNG PHÁP MỚI — VIS-SFT, can thiệp đúng MỘT biến:** `freeze_vision_tower: false` trong
`harness/train_config_vissft.yaml` (copy từ `train_config.yaml`, ⛔ không sửa tại chỗ), xuất phát
từ **model gốc Qwen2.5-VL-3B-Instruct**, dataset giữ `gui_s1`, `lora_target` giữ 7 khối ngôn ngữ
(MLP thị giác dùng `gate/up/down_proj` nên **32 tầng MLP thị giác đã học**), `weight_decay = 0`,
`val_size 0.0`, `do_eval false`. **Mốc so là S1/101 = 59,11.**
⭐ **Căn cứ — chẩn đoán hai kênh** (kênh A = mô hình tự khai `<point>` trong `<desc>` 70,10% ·
kênh B = UGround đọc câu 69,36%, n=4.442): khoảng cách người − MIN **+15,53 pp**, **91% dồn vào
29,9% số bước mô hình tự khai sai đích**; trên lát đó câu chuẩn giảm 84,36 → 55,72 (−28,64) còn mô
hình giảm −73,94 ⇒ **thiếu hụt riêng của mô hình +45,30 pp**. ⇒ Điểm nghẽn là **tri giác**, không
phải diễn đạt.
⚠️ **Hệ số truyền thì nhỏ:** đo bằng chính GRPO đã chạy, kênh A +1,60 pp chỉ cho `exec` +0,045 pp
⇒ **d(exec)/d(A) = 0,028**, thấp hơn tương quan mặt cắt ngang 0,739 **26 lần**. ⛔ Cấm dùng 0,739
làm hệ số quy đổi. Cần **243 lần lật sạch** (18,3% lát A-sai) mới vượt MDE.
⛔ **KHÔNG xuất phát từ checkpoint GRPO** (mục 2.1bis) — ba lý do: không quy được công (mất phép so
một biến với 59,11) · **bẫy PEFT** nạp adapter cũ rồi thêm module mới thì PEFT **bỏ qua module mới
trong im lặng**, tầng thị giác không hề được học mà lượt train vẫn chạy trơn · lệch tập dữ liệu
(GRPO sống nhờ `<desc>` của `gui_s2`, train tiếp trên `gui_s1` là dạy model vứt bỏ thẻ đó).
✅ Được hồi sinh **chỉ khi** A7 về dưới 59,11, và khi đó phải hoà bằng `merge_and_unload` ở
fp16/bf16 → chấm lại xác nhận đúng 60,07 → train adapter **MỚI hoàn toàn** → đổi `dataset` sang
`gui_s2`.

⭐⭐ **THƯỚC — ba vai, chốt, đừng mở lại** (`151` mục 6):

| vai | thước | GRPO/101 |
|---|---|---|
| **TIÊU ĐỀ** | `exec` = `action_ok` ∧ ±14% ∧ Voronoi, niêm `b93e85c` 5/8 | **60,07** |
| **BÁO KÈM** | **D.3** — luật gốc AndroidControl: điểm dự đoán nằm trong hộp phần tử vàng | **67,04** |
| BÁO KÈM | D.3 ∧ ±14% | **62,96** |
| ĐỘ NHẠY | ±14% từng trục 69,37 · AitW Euclid 68,90 · `hit_disk` thuần 69,89 | — |

⛔ **KHÔNG nâng luật ±14% lên tiêu đề — lý do là SÀN, không phải trần:** câu rỗng nghĩa
`"Tap the button."` đạt **12,00** dưới `exec` nhưng **20,50** dưới `d14` ⇒ **86% mức tăng của d14
là thứ câu rỗng nghĩa cũng lấy được**, dải hữu dụng hẹp lại. D.3 thì mở rộng dải (62,88 → 68,88).
Đổi sang d14 còn biến hai phép so vốn không có ý nghĩa (MIN−S1, GRPO−S1) thành có ý nghĩa — đó là
**đi chợ thước**. ✅ D.3 hợp lệ vì là luật của chính bộ dữ liệu, khớp
`descriptor_label_build.py:334` (*"nhiều nút thoả thì chọn nút diện tích nhỏ nhất"*).
⛔ Cấm cộng dồn `exec` với D.3 thành một mũi tên (hai luật trên cùng một lượt chạy). ⛔ Cấm gọi
75,73 là *"mức người"* — nói *"mức mà chính dụng cụ này đạt được khi nhận câu do người viết"*.

**Ba phase, thứ tự không đảo:**
· **Phase 0 (0 GPU, chặn cứng)** P1 `.gitignore` → P2 cache kiểm (**hai** lệnh) → P3 descriptors +
  thêm hàng GRPO vào `luat_d3.py` → P3bis cache dạy (⛔ **`--shards 76`**, mặc định là 1) →
  **P4 viết mới `harness/tach_val.py`** tách val theo **episode** 400 + 600 bước, phân tầng theo
  **`action_type`** (⛔ không theo `app`: rỗng 55%, 270 giá trị) → **P4bis nối
  `train_tru_val.jsonl` vào `build_branch_data.py:111`** → P5 script chấm val → P6 tải hai adapter
  → P7 `--alpha` cho `infer_branch.py` → P8 ghi bốn phụ lục ra tệp.
· **Phase 1 (0 giờ A100)** V1 hiệu chuẩn val ~3 h T4 · **V2 nội suy MIN ↔ GRPO 5 mức α** ~4 h ·
  **V3 soup đều ba adapter họ `<desc>` (MIN·GRPO·CE2-S2, mỗi cái 1/3)** ~4 h · V4 khoá một α rồi
  chấm test **một lần** ~5,6 h.
· **Phase 2 (lượt A100 duy nhất)** A3 khẳng định tĩnh (assert tham số > 14.966.784 và có tensor
  `visual.*` với `requires_grad=True`; ⛔ đừng dùng cổng `grad_norm` bước 10 — LoRA khởi tạo B=0
  nên báo động giả) → A4 smoke 200 bước → **A5 VIS-SFT 20–37 h** → A6 chấm 5 điểm lưu
  (`step01600/03200/04800/06400/07800`) trên val 400 rồi 2 điểm tốt nhất ±200 bước trên val 600
  ⛔ **VIS-SFT chạy 7.876 bước, KHÔNG phải 8.072** — tập dạy là 63.000 mẫu đã trừ val
  (successive halving, Jamieson & Talwalkar AISTATS 2016) → A7 khoá (điểm lưu, α), chấm test hai
  cấu hình. **Tổng 20,5–37,5 h A100 · ~28 h T4.**
· **Phase 3** chỉ chạy hạt 202 nếu A7 **vượt 60,07**; không vượt thì dừng, tiêu đề vẫn 60,07.

⛔⛔ **BỐN BẪY "MẤT BUỔI":**
① **P4bis** — quên trỏ cấu hình vào `train_tru_val.jsonl` thì **train trên chính tập val**, mọi số
val đẹp một cách vô nghĩa, **không lỗi nào báo**, chỉ lộ khi chấm test, tức **sau 20–37 h A100**.
Kiểm: `wc -l` bộ `gui_s1` mới phải nhỏ hơn bộ cũ đúng bằng số bước val (≈1.004).
② **`--shards 76`** — mặc định 1 ⇒ dựng 1/76 dữ liệu (~850 bước thay vì 64.567), không báo lỗi.
Kiểm ngay: `wc -l harness/dg1_cache/train_ac/train.jsonl` phải ra **64567**.
③ **`grid_callback.py` phải đăng ký bằng cách gọi `run_exp` từ Python**, không gọi
`llamafactory-cli` — nếu không, lượt train tốn đủ giờ A100 mà `grid/` **rỗng**, mất trắng 40 quan
sát. Kiểm chữ ký `run_exp` **trước** khi đặt lượt; đường lùi là ô Colab thứ hai copy `checkpoint-*`
mỗi 300 s.
④ **Trộn adapter**: trộn thẳng `lora_A` với `lora_A`, `lora_B` với `lora_B` **sai 65% ở α=0,5**
(ΔW = scaling·B·A là **tích**), mà phép kiểm hai đầu mút α=0/α=1 **vẫn đạt tuyệt đối** nên không
bắt được. Cách đúng: **ghép nối theo hạng** — B′=[(1−α)B_MIN | αB_GRPO], A′=[A_MIN ; A_GRPO], rồi
nhân đôi **cả** `r` lẫn `lora_alpha`. Phép kiểm bắt buộc làm trên **CÂU** (trùng từng ký tự với
`preds_grpo_point_seed101.jsonl` ở α=1 và `preds_min_desc_seed101.jsonl` ở α=0), ⛔ không trên
điểm — MIN và GRPO chênh 0,02 pp nên nạp lẫn hai đầu mút thì điểm không phát hiện được.

⚠️ **Hai quy ước số của `151`:** MDE = **2,11 pp** (2,2 là bản làm tròn cũ của **cùng đại lượng**,
không phải ngưỡng thứ hai) · **Δ(MIN − S1) = +0,95**.
⭐ **Luật đọc val:** ⛔ **không bao giờ trích một con số val nào ra báo** — val chỉ để xếp hạng ứng
viên trong cùng một họ. V1 là phép thử **bắt thảm hoạ**, không phải phép thử xếp hạng: ba nhánh
phải rơi trong 50–70 và không cách nhau > 3 SE. Khoảng cách MIN ↔ GRPO là **1/51 của một SE ghép
cặp** (SE ghép cặp ở val 400 = 1,03 pp cho GRPO−MIN, 1,88 pp cho MIN−S1; SE **không** ghép cặp là
2,45 pp — dùng nhầm loại là sai). Argmax-val chỉ được lấy nếu vượt α=0 **≥ 2,0 pp**, không đạt thì
khoá α=0.
⭐ **Khai trung thực (mục 8):** **0/5** can thiệp đã chấm vượt MDE 2,11 (S2 −1,93 · MIN +0,95 ·
CE2 +2,24 so S2 · `gui_sel` −2,98 · GRPO +0,02 so MIN) · **P(vượt MDE) = 0,30** [0,15 · 0,45] ·
nhánh mới ra thấp hơn thì báo **vô điều kiện** như kết quả âm, tiêu đề vẫn 60,07 ·
**Phase 2 là phần cộng thêm, KHÔNG phải phần chống đỡ.**

⛔ **Đã bị bác BẰNG SỐ, đừng hồi sinh** (`151` mục 2.2): ORPO tầng câu (trần +4,80 là **hiệu ứng
chọn mẫu** — đổi lát sang A(GRPO) còn +2,88, lát không dùng hành vi mô hình thì **−0,65**;
Phụ lục C là script **tự phản biện** bắt được chính con số này) · `gui_sft_match` (phản thực ghép
cặp **59,44 < 60,07**, trần 65,44 là nguỵ biện chọn mẫu ⇒ **tiết kiệm 23 h A100**) · OCR/cây trợ
năng vào đầu vào · vá tên bằng OCR (68,6% tên mô hình sinh **đã là chuỗi thật** trên màn — đúng
chuỗi của **sai** phần tử) · chưng cất qua bộ trỏ thứ hai · đa nhiệm thêm đích hộp/toạ độ · RL
trực tuyến · Spatial CoT · gộp nhánh ở **ĐẦU RA** (oracle 8 nhánh 72,80 nhưng mọi bộ chọn
không-oracle ≤ 60,45).
⚠️⚠️ **Đừng đọc dòng cuối thành "mọi cách gộp đều bị bác"** — gộp ở **KHÔNG GIAN TRỌNG SỐ** tạo ra
một checkpoint mới nên là đóng góp mô hình, và **chưa từng thử**. Đó chính là V2 và V3.
⛔ Cắt vì bất khả thi/vượt ngân sách: daemon chấm bất đồng bộ T4 (Kaggle không mount được Drive) ·
quét lưới 200 ứng viên (~390 h T4 = 13 tuần hạn mức) · lát dev 1.400 (lấy từ tập kiểm) ·
`lora_dropout` · Qwen2.5-VL-7B (≥ 46 h A100, phá bảng 8 nhánh).
⭐ **Phụ lục D, số phải nhớ:** đổi `<desc>` thì **66,67% số bước câu không nhúc nhích một ký tự**
(khai báo đổi ở 43,69% số bước — ⛔ hai đại lượng khác nhau, bản cũ ghi lẫn). ⇒ hàm mất mát của mọi
lượt học ưu tiên **chưa bao giờ so hai CÂU khác nhau**; đó là bằng chứng cho việc cắt ORPO tầng câu.

✅ **ĐÃ LÀM 9/9 — D.3 nay tái lập được từ kho.** Thêm hàng
`("GRPO-point/101", "grpo_point/score_grpo_point_seed101_raw.jsonl")` vào `NHANH` của
`harness/luat_d3.py`, chạy lại, ghi `runs/luat_d3.json`. Ra đúng **67,04**, khớp `report/144:127`
và khớp **cả 9 hàng** bảng mục 7 của `151` (người 83,82 · GRPO 67,04 · MIN 66,55 · S1/202 66,10 ·
CE2 66,03 · S1/101 65,49 · S2 63,63 · `gui_sel` 62,38 · Base 53,60). Dải dùng được trên lát 800:
Voronoi 62,88 · **D.3 68,88** · D.3∧14% 66,62.
⚠️ Vẫn cần **P1** (`!harness/dg1_cache/test_ac/descriptors.jsonl` vào `.gitignore`) thì người khác
clone mới tái lập được — tệp có trên đĩa nhưng **chưa được track**.

⭐ **LỘ TRÌNH BỐN CHẶNG, mốc bảo vệ trên 6 tuần (user xác nhận 9/9) — `report/152`:**
**Chặng 1** (0 GPU, đang làm) đưa bốn mắt xích giải thích của `151` vào luận văn: định vị điểm
nghẽn · hệ số truyền 0,028 · Phụ lục D 66,67% · phép tự phản biện; cộng nối tên đề tài xuyên suốt
và viết lại hướng phát triển. **Chặng 2** Phase 0 (P4 · P4bis · P5 · P6 · P7 · P8). **Chặng 3**
Phase 1 trên Kaggle T4 **0 đồng**, ~17 h — chạy song song chặng 1, runbook
`harness/kaggle_phase1_noisuy_9_9.md`. **Chặng 4** Phase 2, lượt A100 duy nhất.
⛔ Thứ tự này không đảo được: nếu VIS-SFT trắng (xác suất **0,70** theo chính `151`) thì chương 6
vẫn phải đứng vững, nên bốn mắt xích phải vào luận văn **trước**.
⚠️ **Hai chặn của chặng 3 mà `151` không nêu**, đã ghi ở `152` §0: `score_run.py:47,437` **cũng**
đọc cứng `dg1_cache/test_ac/test.jsonl` (P5 phải sửa **cả hai** script, không chỉ `infer_branch`);
và `train_ac/images/` chỉ có **1.697 ảnh** nên chấm val bị chặn tới khi kéo ảnh về.
⛔⛔ **Đừng chạy `build_train_data.py --shards k` để lấy ảnh val** — `build()` (dòng 157) **ghi
đè** `train.jsonl` và chỉ lấy `k` shard **đầu** ⇒ phá tệp 64.567 dòng, không có gì báo. Dùng
`harness/keo_anh_val.py` (đặc tả ở runbook chặng 3): 8 shard **rải đều**, ~1,3 GB, chỉ ghi ảnh.
⚠️ **Val là dữ liệu S1/MIN/GRPO ĐÃ THẤY** (chúng train trên trọn 64.567 bước) ⇒ điểm val của ba
nhánh ấy lạc quan có hệ thống; dùng được cho V1 và cho xếp hạng α, ⛔ không được trích ra báo.
Thiên lệch kèm theo: điểm α giữa mất phần ghi nhớ val nhanh hơn mất năng lực thật ⇒ val **thiên vị
chống lại** điểm giữa, nên điểm giữa **thắng** là bằng chứng mạnh, **thua** thì không kết luận được.

### ⭐⭐ 9/9 — KẾT QUẢ V2 (nội suy MIN↔GRPO): ĐƯỜNG CONG ĐƠN ĐIỆU, KHÔNG CHO GÌ (`report/153`)

| α | 0,00 (MIN) | 0,25 | 0,50 | 0,75 | 1,00 (GRPO) |
|---|---|---|---|---|---|
| `exec` trên val | 67,56 | 67,94 | 67,94 | 67,94 | **68,32** |

n = **262** bước chạm / 85 tác vụ. Điểm giữa cao nhất **thua đầu mút 0,38 pp**; mọi KTC ghép cặp
phủ 0 (α1−α0 = +0,76 [−1,06 · +2,69]). ⇒ **Khoá α = 0** theo §5.4 của `151`.
⛔ **V4 KHÔNG chạy** — argmax-val là α=1, tức đúng GRPO-point vốn đã có điểm test **60,07**; chấm
lại là chấm lại chính nó. **Tiết kiệm ~5,6 h T4.** Đóng góp mô hình giữ nguyên ở **60,07**.
⭐ **Dự đoán ghi trước ĐÚNG.** `151` §5.1 nêu thẳng khả năng *"đường cong có thể đơn điệu, cực đại
đúng tại α=1, và khi đó thu được 0"*; `152` §0 mục 7 (ghi **trước** khi có kết quả) làm hẹp kỳ vọng
thêm bằng số đo: GRPO chỉ dịch `lora_A` 1,39% và `lora_B` 6,87% so MIN.
✅ **Hai phép kiểm bắt thảm hoạ đạt** ⇒ đường chấm val lành, dùng lại được cho A6 của Phase 2.
⭐ **Phép kiểm hai đầu mút trên CÂU đạt theo cách đẹp:** 155/407 bước (38,1%) câu khác nhau, và số
bước câu đổi **tăng đơn điệu** 53 · 95 · 127 · 155 ⇒ mã ghép nối theo hạng hoạt động đúng, tạo dãy
mô hình chuyển dần chứ không nhảy giữa hai bộ trọng số. Kết quả bằng 0 là thật, không phải hỏng.
⭐⭐ **Bằng chứng định lượng cho luật CẤM trích số val:** val cao hơn test ~**7,5 pp** ở cả hai
nhánh, và **phóng đại khoảng cách giữa hai nhánh gần 40 lần** (0,76 trên val so với 0,02 trên
test). Luật *"không bao giờ trích một con số val nào ra báo"* nay có số đo chống lưng.
✅ Đã vào luận văn: **ch6 §`sec:noisuy`** (124 trang, 0 overfull). Báo vô điều kiện theo cam kết,
nhưng **không trích con số val nào** — chỉ báo hình dạng đường cong và quyết định.
⚠️ **V3 (soup ba adapter) vẫn chạy được** nhưng kỳ vọng phải hạ: nội suy hai adapter cùng họ đã
đơn điệu thì soup ba adapter cùng họ khó cho khác. Đây là suy luận **sau** khi thấy số ⇒ chạy thì
báo vô điều kiện, bỏ thì ghi rõ lý do.

### ⭐⭐⭐⭐ 14/9 — CHỈ ĐẠO CỦA USER VỀ THƯỚC, THẮNG MỌI LUẬT "KHÔNG ĐỔI THƯỚC / NGƯỠNG ĐĂNG KÝ TRƯỚC" TRONG FILE NÀY

Nguyên văn user 14/9: *"Quan trọng là metric nào đó vừa hợp lý (ưu tiên metric đã có sẵn cho thuyết
phục hội đồng) vừa cho số cao, còn mấy cái mà ngưỡng đăng ký trước hay gì đó bạn cứ bỏ đi, ko quan
trọng đâu."* Trước đó 13/9: *"Tôi chỉ cần tốt nghiệp"*.
⇒ **Mục tiêu hiện hành là tốt nghiệp với số cao nhất có thể bảo vệ được.** Khi chọn thước:
① ưu tiên thước **đã có tiền lệ, có trích dẫn** (luật của chính bộ dữ liệu, của AitW, bộ chấm COCO…);
② trong các thước hợp lý đó, **chọn thước cho số cao** để làm số chính;
③ **bỏ** các ràng buộc "khoá trước / ngưỡng đăng ký trước / không đổi thước headline / không nới sau
khi thấy điểm" — mọi dòng ⛔ kiểu đó ở các khối cũ bên dưới **hết hiệu lực** về mặt *chọn thước để báo*.
**Vẫn giữ** (vì hội đồng bắt được, không phải vì thủ tục): số phải là số thật tính từ tệp thô, khai đúng
tên và nguồn của thước, in kèm mốc câu chuẩn cạnh số mô hình, không bịa trích dẫn, không tuyên bố một
nhánh "hơn có ý nghĩa" khi hội đồng tự tính lại từ bảng trong bài là thấy mâu thuẫn.

⭐ **Luật khớp chạm ĐẦY ĐỦ của AitW** (`harness/luat_aitw_day_du.py` → `runs/luat_aitw_day_du.json`,
đo 14/9, 0 GPU, chép từ `google-research/android_in_the_wild/action_matching.py`): chạm khớp khi
**‖Δ‖ chuẩn hoá ≤ 0,14 HOẶC cả hai điểm nằm trong hộp phần tử nới 1,4×** (∧ đúng loại thao tác).
Cột `aitw` cũ chỉ là vế khoảng cách. Kết quả: **chặng ba 77,30** · MIN 76,41 · S1/101 74,37 · Base 63,39 ·
câu chuẩn **92,14**. Lát 800: trần 90,75 · sàn câu rỗng 25,87 (dải 64,9, rộng hơn exec 62,9) · ⚠️ bỏ tên giữ
vị trí 86,25 (luật gần như không phạt thiếu tên). Xấp xỉ phải khai: chỉ có hộp vàng, không có mọi hộp chú
thích ⇒ chỉ có thể THẤP hơn luật gốc.
✅ **ĐÃ VÀO LUẬN VĂN 14/9 (user duyệt), bộ ba số chính: 77,3 AitW · 67,0 D.3 · 60,1 exec** ở tóm tắt VI/EN,
ch1, ch5 (đoạn *Luật khớp chạm của AitW*), ch6 `sec:nhieuthuoc`, ch7. KTC chặng ba AitW **[75,8; 78,8]**.
⭐ **Phép so dưới AitW đầy đủ (`runs/d3_ktc.json`):** chặng ba − S1/101 **+2,94 [+1,77; +4,08] p<0,001**
(vượt MDE 2,11) · chặng ba − S1/202 **+1,99 [+0,84; +3,13] p<0,001** · MIN − S1/101 **+2,04 p<0,001** ·
chặng ba − MIN **+0,90 p=0,007**. Dưới D.3: chặng ba − S1/101 +1,55 p=0,008; dưới exec +0,96 p=0,090. Bài
ghi cả ba, giải thích: AitW/D.3 thưởng việc chạm tới gần đúng phần tử, exec còn đòi tách khỏi phần tử sát bên.
⛔ Cấm viết "chặng ba vượt MDE so với S1" mà không kèm hạt 202 (+1,99, dưới MDE) — bảng in cả hai.
· **Sửa lỗi mô tả cũ 14/9:** ch1/ch2/ch5 từng viết AitW dùng cửa sổ **chữ nhật theo từng trục** — SAI theo mã
  gốc (Euclid trên toạ độ chuẩn hoá ∨ hộp nới 1,4×). Nay ghi cửa sổ ±14% từng trục là *biến thể* luận văn dùng.
· Chưa dựng lại `thesis/main.pdf` (user dặn); bản dựng thử ở scratchpad **131 trang, 0 overfull, 0 undefined**.
· **Tra cứu thước nâng số 14/9 (agent, venue đã kiểm):** không có luật toạ độ chuẩn nào lỏng hơn AitW. Hướng
  còn lại đều cần GPU: ① **người nghe trắc nghiệm** trên khối ≤40 ứng viên (comprehension accuracy — Mao CVPR
  2016, Luo CVPR 2017, Seq2Act ACL 2020, Mind2Web NeurIPS 2023): kỳ vọng ≥77, bẫy = người nghe cùng họ/đã học
  định dạng khối (Mao: người nghe chung tham số chấm câu máy 0,848 > câu người 0,695) ② agent AndroidControl-Low
  (OS-Atlas ICLR 2025 giao thức ≤14% bề ngang) làm người thực hiện: trần ~88–89 nhưng **sàn có thể ~80** vì có
  mục tiêu ⇒ phải bỏ mục tiêu ③ VLM giám khảo so cặp với câu chuẩn (MT-Bench NeurIPS 2023, MLLM-as-a-Judge
  ICML 2024) ④ nhiều người nghe: chỉ **trung bình** có tiền lệ (Zhao EACL 2021), "bất kỳ bộ nào trúng" thì không.
  Không hợp: nDTW/SDTW (nhiều bước) · COMET (nguồn là văn bản) · CLIPScore (224 px không đọc chữ).
· ▶️ **HƯỚNG ① ĐANG THI HÀNH 14/9 — người nghe trắc nghiệm (Set-of-Mark).** Runbook
  **`harness/kaggle_som_listener.md`** (Ô 0–9) · gói `_bundles/thesis_som.zip` (0,85 MB) + dataset ảnh
  `thesis-score` · mã `harness/som_build.py` (ứng viên = nút trợ năng có action CLICK 16/LONG_CLICK 32, ≤50%
  màn, gộp IoU≥0,9, không cắt, đánh số thứ tự đọc; đáp án = ô chứa điểm chạm vàng) · `som_cau.py` (7 tệp câu từ
  trường `sent` của tệp thô) · `som_listener.py` (backend phi4/pixtral/gia; không mục tiêu, không lịch sử; nối
  tiếp được; `SOM_PHI4_CROPS` chỉ hạ khi OOM) · `som_doc.py` (KTC bằng `score_run.cluster_bootstrap`).
  Số đo trên WSL: ứng viên trung vị **15**/màn, p90 49, 50 màn không có ứng viên, **phủ đáp án 95,7%**.
  Người nghe (kiểm nguồn): **Phi-4-multimodal-instruct** (MIT) và **Pixtral-12B** (Apache-2.0); đã LOẠI vì có
  AndroidControl/AITW trong dữ liệu: Molmo · InternVL2.5 · Magma · Phi-Ground; loại vì nền Qwen: InternVL3 ·
  LLaVA-OV. ⛔ Luật chọn khoá trước: lát 200 bước cố định (seed 20260914), **câu chuẩn** cao hơn thì thắng.
  Kỳ vọng [suy]: ≥77 nhưng CHƯA ĐO.
  ⚠️ **Đo 14/9 Ô 4:** Phi-4 với 36 mảnh ảnh (mặc định) **OOM trên T4** ở vision encoder (trọng số ~12 GB/14,56). Chốt
  **`PHI4_CROPS = 16`** + `expandable_segments` cho MỌI nhánh (đặt trong hàm `chay` của Ô 3), trước khi có điểm nào.
  ⚠️ **Đo 14/9 tối:** Ô 4 (8 bước, 16 mảnh, eager) CHẠY ĐƯỢC — ra số, đúng 3/8, nạp+8 bước ~1,5 phút. Lát 200 bước
  **OOM ở attention phần ngôn ngữ** (`modeling_phi4mm.py:1157`, eager dựng ma trận fp32). Mã `14/9-b`: `sdpa` (lùi eager
  nếu không nhận) + **bắt OOM từng bước** (`raw="__OOM__"`, tính trượt, đếm và khai). Gói mới `_bundles/thesis_som_v2.zip`
  → dataset **`thesis-som-v2`** (không New Version dataset cũ).
  ✅ **Kiểm 30 bước 14/9 tối:** `sdpa` nhận, **OOM 0, 3,13 s/bước** trên 1 T4 ⇒ một nhánh đủ chia 2 GPU ≈ 2,1 h. User chạy phần G (commit qua đêm).
  ⚠️ **Lát thử 200 bước (commit đêm 14/9, log 0,29 h):** Phi-4 **câu chuẩn 50,5%** · câu rỗng **18,0%** · 3,36 s/bước · OOM 0.
  Dải 32,5 điểm ⇒ qua phép kiểm an toàn (≥20), commit chạy tiếp. ⛔ **Trần 50,5 THẤP hơn xa exec 75,7 / AitW 92,1** ⇒ thước này
  **KHÔNG nâng số tiêu đề** (mô hình dự kiến ~40 [suy]). Giá trị còn lại: người nghe **ngoài họ Qwen, không học AndroidControl**
  ⇒ đóng đòn "cùng họ Qwen" còn mở ở mục GIỚI HẠN, nếu thứ tự nhánh giữ nguyên.
  ✅ **KẾT QUẢ ĐỦ 15/9 (`report/155` §2.4, `runs/som/`, `harness/som_phan_tich.py`):** Pixtral lát 200 chỉ **8,0** vì lỗi định
  dạng (164/200 trả lời dài bị cắt ở 8 token, không phải kém hiểu) ⇒ chọn Phi-4. Phi-4 trên 4.463 bước: câu chuẩn **54,94** ·
  chặng ba **45,78** · S1/101 **44,63** · Base 38,56 (chỉ 3.566 bước, cắt ở trần giờ) · câu rỗng 15,86 · đoán ngẫu nhiên 10,06.
  ⭐ **Thứ tự nhánh giữ nguyên**, chặng ba nằm ở **45–48% dải Base→câu chuẩn dưới cả bốn thước** (người nghe · exec · D.3 · AitW)
  ⇒ đòn "cùng họ Qwen" **đóng phần lớn**. ⭐ Chặng ba − S1/101 dưới người nghe **+1,14 [+0,23; +2,10] p=0,020** (exec +0,96
  p=0,090). κ với UGround chỉ 0,25–0,44 ⇒ hai dụng cụ sai ở bước khác nhau. Kiểm tất định: lát 200 chạy lại trùng tuyệt đối.
  Còn nợ: Base 897 bước · MIN · S1/202 (~5 h T4, một commit). ⛔ Không làm số tiêu đề (trần 54,9).
· **Đo 14/9 đêm, 0 GPU (`harness/luat_aitw_moi_hop.py` → `runs/luat_aitw_moi_hop.json`):**
  ① AitW với **mọi khung phần tử bấm được** (thay vì chỉ khung vàng): chặng ba **85,01** · MIN 84,36 · S1/101 81,04 · Base 73,36 ·
  câu chuẩn 96,17. ⛔ **Sàn nhảy vọt:** câu rỗng **41,62** (khung vàng 25,88) · câu sai màn 35,88 ⇒ dải 54,3, HẸP hơn exec 62,9.
  Nguyên nhân: khung ≤50% màn nới 1,4× gần phủ cả màn, lỏng hơn khung chú thích nhỏ của AitW gốc ⇒ đây là **cận trên lỏng**,
  không phải luật gốc. Chỉ nên trình như cặp cận dưới/cận trên (77,3 · 85,0) kèm sàn, không làm số chính.
  ② Toạ độ `<point>` tự khai: GRPO trong khung vàng (ScreenSpot) **65,52**, AitW khung vàng **78,53**; MIN 65,20 / 77,26.
  Chỉ nhỉnh hơn câu (77,3) và không phải đầu ra của bài ⇒ không đáng đổi số chính.
· ✅ **14/9 đêm, user duyệt: cặp 77,3 → 85,0 (cận dưới/cận trên AitW) ĐÃ VÀO luận văn** — tóm tắt VI/EN, ch1, ch5 (đoạn
  *Cận trên của luật khớp chạm của AitW*, có sàn 41,6/35,9 và dải 54,3), ch6, ch7; cột "AitW cận trên" trong `tab:nhieuthuoc_vitri`.
· ⭐ **S2 dưới ba luật (`runs/d3_ktc.json`, thêm 14/9 đêm):** S2 − S1/101: exec **−1,93** p<0,001 · D.3 −1,86 p<0,001 · **AitW −0,96
  [−2,18; +0,29] p=0,100** (hết ý nghĩa). Chuỗi đóng góp trên nền S2: CE2 − S2 AitW **+2,69** · MIN − S2 **+3,00** · **chặng ba − S2
  +3,90 [+2,90; +4,90]** (exec +2,89), đều p<0,001 · MIN − CE2 AitW **+0,31 p=0,215** (riêng ORPO không ý nghĩa dưới AitW). Đã
  thêm hai hàng S2 vào `tab:d3ktc` và một đoạn ở ch6. Bản dựng thử scratchpad **132 trang, 0 overfull, 0 undefined**.

### ⭐⭐⭐⭐⭐ 22/9 — BÀN GIAO `183` (thước chốt + DCRP) VÀ CỔNG G0 **FAIL**

Nguồn: `report/183_…` (chép từ 9 ảnh do phiên Mac soạn). Thước chốt ở đó: `exec` primary · D.3
confirmatory · UI-Venus robustness **bắt buộc, còn thiếu 5/9 nhánh** · AitW/BLEU/BERTScore xuống phụ
lục · Phi-4 SoM ưu tiên bỏ. ⚠️ Lệch với chỉ đạo 14/9 (bộ ba AitW·D.3·exec ở luận văn) — **chưa sửa
luận văn**, chờ user quyết.
Phương pháp đề xuất **DCRP** (cặp ưu tiên target-vs-distractor chấm bằng bộ chấm ký hiệu a11y+OCR,
ORPO/DPO, không bộ trỏ trong thưởng) có cổng G0 chặn trước mọi GPU.
⛔ **G0 đo 22/9 trên WSL, 16 s CPU: FAIL.** Trần suy ra = Δ%nhắc-tên (người − mô hình) × Δ`exec`
(nhắc vs không) = **+0,97** (vs S1) / **+0,98** (vs CE2), ngưỡng pass 3,0, fail < 2,0. Quét ngưỡng biên
từ 2,9 xuống 0,01: trần cao nhất **+2,8**, không ngưỡng nào chạm 3,0 ⇒ FAIL không do scorer.
⇒ **Rút preference: không G2, không train DCRP.** Việc còn: UI-Venus 5 nhánh × 4.463 · viết chẩn đoán âm.
⭐ Mã chép từ ảnh tái lập đúng số Mac: `m2_loose` sau gộp nút = **3.975** (khớp §3.2).
⚠️ Mã G0 import `score()` của `m9` (3×F1, có bậc) chứ không phải ranker nhị phân §3 nói đã chọn ⇒ ở
ngưỡng 2,9 %nhắc-tên người chỉ 9,5% (không phải 33,1%). Đã kiểm độ nhạy, không đổi kết luận.
⚠️ `runs/noisuy/*/adapter_model.safetensors` (115 MB/tệp) đã vào `.gitignore`; bản lưu ở **GitHub Release `noisuy-adapters-v1`** (kèm SHA256SUMS, lệnh tải trong ghi chú release).

### ⭐⭐⭐ 21/9 — NGUỒN CỦA +2,94 DƯỚI AitW LÀ CỔNG LOẠI THAO TÁC, KHÔNG PHẢI ĐỊNH VỊ (đã sửa luận văn)

`harness/phan_ra_cong_thao_tac.py` → `runs/phan_ra_cong_thao_tac.json`, 0 GPU. Chặng ba − S1/101 dưới AitW
**+2,94 = +3,11 từ 256 bước (5,7%) S1 viết sai loại thao tác + 0,11 từ 4.189 bước cả hai đúng loại thao
tác** (trúng 79,04 vs 78,92). So S1/202: +3,09 và **−0,67**. Dưới exec nhóm cả hai đúng cho −0,81 (S1/101).
⇒ Câu cũ ở ch6 *"cải thiện thể hiện rõ nhất ở việc đưa lần chạm tới gần đúng phần tử"* là **SAI**, đã thay
21/9 (ch6 · tóm tắt VI/EN · ch1 · ch7; ch7 nay kèm hạt 202 +1,99 dưới MDE). Số 77,3 và +2,94 vẫn giữ.
Bài SOICT (`paper/soict2026/`) nói cùng kết luận. Dựng thử scratchpad **133 trang, 0 overfull, 0 undefined**;
chưa dựng lại `thesis/main.pdf`.

### ⭐⭐⭐ 13/9 — USER QUYẾT: HAI SỐ SONG SONG (exec · D.3) + NHÓM THƯỚC VĂN BẢN — THẮNG các dòng "giữ Voronoi làm headline / D.3 chỉ báo kèm" bên dưới

Nguyên văn user: *"thêm D.3, 2 số song song với nhau và nghiên cứu thêm metric khác nữa để cho số
cao nha"* · *"Tôi chỉ cần tốt nghiệp"*. Đã thi hành:
· **Số chính in song song ở tóm tắt VI/EN, ch1, ch7:** chặng ba **60,1% exec · 67,0% D.3**, câu chuẩn
  **75,7 · 83,8**; S1 **59,1 · 65,5**, Base **47,6 · 53,6**; `action_ok` **98,9%** (chỉ bước chạm).
· **ch5 §`sec:donhay`** viết lại: luật dung sai đơn thuần vẫn không dùng để kết luận phép so (lý do
  sàn 20,50 + Holm); D.3 báo **song song**, khai rõ tính sau khi có điểm; **phép kiểm ý nghĩa vẫn
  đọc trên exec**. ⛔ Vẫn cấm dùng luật lỏng để tuyên bố GRPO/MIN hơn S1 có ý nghĩa.
· **ch6 §`sec:nhieuthuoc`** mới + hai bảng sinh tự động `thesis/chapters/bang_nhieu_thuoc.tex` bởi
  `harness/sinh_bang_nhieu_thuoc.py` (⛔ đừng sửa tay). Nguồn: `runs/luat_d3.json` ·
  `runs/text_metrics.json` · **`runs/text_metrics_coco.json`** (`harness/text_metrics_coco.py`, bộ
  chấm COCO chính thức, cần Java 8 ở `~/.jdk/`) · **`runs/text_metrics_them.json`**
  (`harness/text_metrics_them.py`, chrF + BERTScore roberta-large L17 rescaled, CPU ~20 phút/nhánh).
  Hai script ghi sau mỗi nhánh, chạy lại tự bỏ qua nhánh đã xong.
· **Số COCO (4.463 bước, mức kho):** BLEU-4 Base 15,3 · S1 51,6/51,7 · MIN 49,9 · GRPO 49,9 ·
  SPICE Base 18,5 · S1 44,4 · GRPO 42,5 · ROUGE-L max 68,6 (CE2) · CIDEr-D ~400 (>100 vì một câu
  chuẩn/bước). ⚠️ **Nhóm văn bản xếp S1 TRÊN MIN/GRPO** — đã khai trong bài, phép so vẫn đọc exec.
· ⚠️ BLEU-4 COCO (~50) **khác** BLEU-4 trung bình theo câu ở `tab:chinh` (37,8) — hai tên khác nhau.
· Thêm 5 tài liệu (venue kiểm tận nguồn 13/9): `meteor` (WMT 2014) · `cider` (CVPR 2015) · `spice`
  (ECCV 2016) · `chrf` (WMT 2015) · `bertscore` (ICLR 2020). Luận văn dựng thử **128 trang, 0 overfull**.
· **BERTScore (rescaled) + chrF xong 14/9:** Base 40,1 · 40,2 · S1/101 66,3 · 61,3 · GRPO **66,8** · 61,9 ·
  gui_sel 62,8 · 57,7. Bản thô 93,5–94,4 cho mọi nhánh đã tinh chỉnh (không tách được). ⚠️ Câu rỗng
  tính **0** ở cả hai bản (vá trong script; `bert_score` 0.3.12 + transformers 5 ném AttributeError
  với câu rỗng). Luận văn **128 trang, 0 overfull, 0 undefined** (dựng 14/9).
· **KTC95 + McNemar cho D.3 xong 14/9** (`harness/d3_ktc.py` → `runs/d3_ktc.json`, bảng `tab:d3ktc`
  trong `bang_nhieu_thuoc.tex`, ~3 phút CPU). Dùng **đúng** `score_run.cluster_bootstrap` nên KTC exec tái
  lập tuyệt đối `ci_voronoi` của 5 nhánh. D.3: chặng ba **67,0 [65,3; 68,7]** · S1 65,5 [63,8; 67,2] ·
  Base 53,6 [51,9; 55,3] · câu chuẩn 83,8 [82,5; 85,1]. S1−Base D.3 **+11,90** p<0,001.
  ⚠️ **Chặng ba − S1 dưới D.3 = +1,55 [+0,40; +2,69], p=0,008 — CÓ ý nghĩa, còn dưới exec +0,96 p=0,090
  thì không.** Vẫn dưới MDE 2,11, trong dải −2,8…+1,7, một hạt ⇒ đã ghi trong ch6 là **không kết luận
  được**, và là ví dụ thứ hai của "đổi luật biến phép so thành có ý nghĩa". ⛔ Cấm viết "chặng ba hơn S1".
· Deck bảo vệ **chưa** cập nhật theo hai số song song.

### ⛔ 10/9 — K1 CỦA VIS-SFT VƯỢT NGƯỠNG DỪNG: `step03200` thấp hơn MIN **−7,50** trên val

Trên `val_cham400` (n=400): MIN **67,25** [61,6 · 73,1] · VIS-SFT `step03200` **59,75** [54,6 · 65,1].
Luật K1 khoá trước là dừng khi thấp hơn quá **3,0** ⇒ **đã chạm ngưỡng dừng**. Phép so thiên vị
chống VIS-SFT (mốc MIN không phải S1, MIN đã thấy val, điểm lưu mới 41%) nhưng ⛔ không nới.
Chi tiết + trạng thái quyết định ở `harness/colab_vissft_9_9.md` mục *KẾT QUẢ K1*. Số val, cấm trích.
**13/9:** lượt **không chạy tới cuối** (`grid/` không có `step07800`) và không chạy tiếp ⇒ VIS-SFT **không có điểm test**, dừng ở điểm kiểm K1; tiêu đề giữ **60,07**.

### ✅ 9/9 — CHẶNG 1 XONG · PHASE 0 XONG · PHASE 1 ĐANG CHẠY TRÊN KAGGLE

**Luận văn nay 122 trang, 0 overfull, 0 tham chiếu hỏng.** Bốn mắt xích giải thích của `151` đã vào:
· **ch6 §`sec:haikenh`** — tách kênh tri giác khỏi kênh diễn đạt. Kênh A 70,10% · kênh B 69,36%
  (n=4.442); **91% khoảng cách so với câu chuẩn dồn vào 29,9% số bước** mô hình nhìn sai phần tử;
  câu chuẩn giảm 28,64 điểm còn mô hình giảm 73,94 ⇒ **thiếu hụt riêng của mô hình +45,30 pp**.
  Kèm bảng ô chéo chặng hai × chặng ba ⇒ **mức truyền 0,028**, và đoạn bác việc dùng tương quan
  mặt cắt ngang 0,739 làm hệ số quy đổi.
· **ch6 §`sec:tranlat`** — mục tự phản biện. Trần 4,80 cho một can thiệp tầng câu **giảm còn 2,88
  rồi đổi dấu** tuỳ cách định nghĩa nhóm, trong khi cột câu chuẩn gần như đứng yên ⇒ chữ ký của
  hiệu ứng chọn nhóm. Rút thành luật đọc, áp cho cả `sec:chonghen`.
· **ch3 `tab:anhxa`** — bảng ánh xạ ba khái niệm ở tên đề tài, kèm lý do đơn vị sinh và chấm là
  một bước. Trước đó *trường hợp sử dụng* và *giao diện người dùng* chỉ sống ở bìa và một đoạn ch1.
· **ch7** — hướng mở phần thị giác thành hướng **đầu tiên**, khai thẳng P(vượt ngưỡng) ≈ **0,30**.
· **ch5 §`sec:donhay`** — ⭐ **kết quả MỚI, `151` không có:** hiệu chỉnh Holm cho GRPO − S1/101 trên
  ba luật: ±14% từng trục p=0,0003 **giữ**, AitW Euclid p=0,0010 **giữ**, **Voronoi p=0,0860 MẤT**
  ý nghĩa. Đổi sang luật dung sai đơn thuần biến một phép so không có ý nghĩa thành có ý nghĩa và
  kéo Δ từ 0,96 lên 2,13 ⇒ bằng chứng định lượng cho việc **không đổi thước tiêu đề**.
· V3 (66,7% câu không đổi khi khai báo đổi) **đã có sẵn** ở `ch6:970`, không viết trùng.

**Phase 0 xong trọn** (P1 · P4 · P4bis · P5 · P6 · P7 · P8). Ba chỗ phải nhớ:
· **P1**: `.gitignore` phải loại bằng `harness/dg1_cache/*` rồi mở lại từng tầng — loại cả thư mục
  thì git **không duyệt vào trong** và mọi dòng `!` bên trong vô hiệu.
· **P5**: `infer_branch.py` **và** `score_run.py` nay nhận `--data-root` + `--recs-file`, mặc định
  giữ nguyên hành vi cũ, và **in dòng `[dữ liệu] …`** — chỗ duy nhất kiểm được đang đọc tập nào.
· **P4bis**: `build_branch_data.py` nhận `--recs-file`, thư mục ra tự đổi thành `branches_tru_val`
  nên không thể lẫn hai bộ.
· **P8**: bốn phụ lục `phu_luc_b/c/d.py` + `do_chot_cuoi.py` **tái lập khớp tuyệt đối** mọi số đã
  công bố. ⚠️ Phụ lục B cần **HAI** quần thể: mục A và C chỉ đọc `<point>` của MIN (**4.442**),
  mục B so MIN với GRPO nên đòi cả hai (**4.437**). Cột đầu là `action_ok` **thuần**. Bootstrap
  phải **gộp sẵn theo cụm** trước khi lấy mẫu.

⚠️⚠️ **PHÁT HIỆN 9/9 CHIỀU — mẫu số `exec` của val KHÔNG bằng số bước val.** `tach_val.py` chia
theo **mọi** bước còn `score_run.py` chỉ chấm bước **chạm**: val400 có 407 bước mà chỉ **262 chạm**,
val600 có 604 mà **391**. Sai số chuẩn ghép cặp ở 262 bước là ~1,3 pp thay vì 1,03 ⇒ chọn argmax
trên năm điểm lưu là chọn gần như ngẫu nhiên.
✅ **Đã xử bằng `harness/mo_rong_val.py`:** dựng `val_cham400.jsonl` (607 bước · **400 chạm** · 137
episode) và `val_cham600.jsonl` (960 bước · **602 chạm** · 209 episode), **bao trùm trọn val cũ**
để lượt Phase 1 đang chạy vẫn nằm ngoài tập dạy. `train_tru_val.jsonl` nay 63.000 bước.
⛔ Đổi val thì **phải dựng lại** `branches_tru_val` bằng `build_branch_data.py --recs-file
train_tru_val.jsonl`, nếu không cấu hình VIS-SFT vẫn trỏ bộ cũ và tập dạy còn chứa val mở rộng.

⚠️⚠️ **BA CHỖ `151` MÔ TẢ KHÔNG ĐÚNG VỚI MÁY WSL NÀY — đã kiểm 9/9, đều theo hướng có lợi:**
· `151` nói `harness/dg1_cache/test_ac/descriptors.jsonl` **mất khi clone lại 7/9** và dành cả mục
  6.2 cho 6 bước dựng lại ~8 GB. Trên WSL tệp **vẫn còn**, **4.448 dòng**, và `runs/luat_d3.json`
  cũng có ⇒ phần lớn mục 6.2 có thể bỏ, chỉ còn P1 (`.gitignore`) + bước 4 (thêm hàng GRPO vào
  `luat_d3.py`) + bước 5–6.
· `151` nói `harness/dg1_cache/train_ac/` **không tồn tại**, chặn P4 và V1. Trên WSL có đủ:
  `train.jsonl` **64.567** dòng, `ocr.jsonl` 64.567 dòng ⇒ **P3bis có thể bỏ**, P4 chạy được ngay.
· `test_ac/ocr.jsonl` ở đây là **6.969** dòng — đúng cái *"di tích của bản `test.jsonl` cũ"* mà
  `151` cảnh báo, không phải 6.958 của bản dựng lại sạch.
⇒ **Xác minh bằng md5 trước khi tin**, rồi mới quyết bỏ bước nào của Phase 0.

### ⭐⭐ 6/9 — LƯỢT GRPO `<point>`: khai báo +2,56 pp nhưng `exec` chỉ **+0,02** (`report/144`)

500/500 bước (5,63 h A100) · suy luận 4.463 bước chạm trên Kaggle T4, 3,1 h · tệp ở
`runs/grpo_point/`. **Cổng khai báo tăng có ý nghĩa:** cả hai đúng **60,6 → 63,2 (+2,56 pp)**,
b=75 c=164, p=1,3e−08, KTC [+1,69 · +3,44]; tên +2,51 · point +2,22. BLEU-4 **−0,09** ⇒ câu không
bị bẻ thành mật mã. **`exec` đo được: 60,05 → 60,07, Δ +0,02** (b=98 c=99, p=1, KTC [−0,59 ·
+0,64]) ⇒ ô **TRẮNG**, và đây là **điểm tiêu đề hiện hành của luận văn**.
⭐ **Dự báo ghi trước bị bác:** (x19d) ghi +1,10 pp (hệ số 0,43), đo được +0,02 ⇒ hệ số thực
≈0,01, **không phải hằng số của bài toán**. Bảng hạch toán bốn nhóm +62/−30/−14/−17 = +1 bước.
⭐ **Cơ chế là đổi hẳn phần tử, không phải nhích qua ngưỡng thưởng:** 66,5% point đứng yên tuyệt
đối, và trong 184 bước GRPO trúng mà MIN trượt thì MIN vốn lệch **trung vị 359** với 51,6% lệch
quá 350 (chỉ 17,9% sát ngưỡng 140–200).
⭐ **66,7% thay đổi khai báo không tới được câu** (1.300/1.950) — số này vào ch6 luận văn.
⛔ **Đòn mạnh nhất chưa đóng: KHÔNG có nhánh so sánh "train thêm 500 bước"** ⇒ mọi con số lẫn công
của GRPO với công của việc học thêm. Tiền lệ MIN vs CE2: 78–88% mức tăng thuộc nhánh so sánh.
⛔ **Cổng khai báo KHÔNG độc lập với hàm thưởng** — ngưỡng ±140 của `gate_desc_acc.py` trùng khít
cửa sổ ±140 của `r_point`. Thước độc lập duy nhất là `exec`.
**Cấu hình đã chạy (để tái lập):** TRL **0.29.1** GRPO, học tiếp adapter MIN, β=0,04 với tham
chiếu = bản sao adapter MIN (`add_adapter("ref")`), G=4, temp 1,0, lr 1e-5, lô 4×4, **500 update
= 2.000 câu nhắc = 1 epoch** trên tập thưởng (2.000/41.090 bước chạm train, seed 101). Thưởng:
r_point 1,0 nếu `<point>` trong ±140 quanh `point_norm` vàng · r_format 0,2 · r_name 0,1 —
**không bộ trỏ nào trong phần thưởng** ⇒ không Goodhart lên UGround. Mã `harness/grpo_point.py`,
runbook `harness/colab_grpo_point.md`.
⭐ **(x20) khoá 6/9 TRƯỚC khi có `exec`:** **(x20a)** nhánh so sánh `min_ce_tiep_seed101` (SFT tiếp
125 update trên đúng 2.000 câu nhắc tập thưởng, lr 1e-5) **chỉ chạy nếu `exec` ≥ +2,2 pp** ⇒ **đo
được +0,02 nên KHÔNG chạy** · **(x20c)** hạt 202 cùng điều kiện ⇒ **không chạy** · **(x20b)** bước
KHÔNG chạm 2.495 bước **đo vô điều kiện**, thước `--mode noharm`, ngưỡng không thấp hơn MIN quá
3 pp, suy luận ~1,7 h Kaggle còn chấm 0 GPU ở máy nhà (gói ảnh `test_images_nontap.tar`, 1,54 GB,
đã đóng sẵn) — **việc này vẫn còn nợ**. Đọc kết quả bằng `harness/doc_exec_grpo.py`.

### ⭐⭐⭐ 5/9 TỐI — τ: **LUẬT NULL THẮNG, LƯỢT ② KHÔNG CHẠY, NHÁNH ỨNG VIÊN ĐÓNG** (`report/142` · `106` (x18))

Đủ 1.400 bước dev (hai commit Kaggle nối tiếp, 7/7 phép kiểm toàn vẹn đạt; tệp
`runs/sel/seqscores_gui_sel_seed101_dev1400_gpu0/1.jsonl`, kết quả `runs/sel/tau_scan.json`).
Null greedy đúng **888/1.400 = 63,43%**. Lift: **X (x16d) −360** [−397·−322] · **A +1** [0·+4] ·
**B −52** [−83·−21] · **C +8** [−11·+27]; ngưỡng 18/24 ⇒ **không nhánh nào đạt**. τ₀ = −0,633 áp
lên B: −143, lên C: +1. Dự đoán ghi trước (0–3 pp, null có thể thắng) **đúng**: tốt nhất +0,57 pp.
⇒ **Áp (x17b), không nới: `gui_sel_cham`/101 KHÔNG chạy.** Hạt 202 vô hiệu. (x17c) không áp dụng.

⭐ **Chẩn đoán, đáng giá hơn con số:**
· **Xếp hạng ứng viên không hỏng, phép chia số token mới hỏng:** top-1 theo TỔNG log-prob đúng
  **67,5%** HasAns (680/1.008), trùng ứng viên greedy tự chọn 701/814; theo điểm/token chỉ
  **38,3%** (ưu ái span dài, trung vị 25 vs 20 token). Tái lập probe (x17f) đúng chiều, đúng cỡ.
· **Khâu bỏ cuộc mù với likelihood của chính mô hình:** trong 583 bước greedy nói `none`, điểm
  thẻ `none` ở 275 bước có vàng (trung vị −1,706) **trùng** 308 bước không có vàng (−1,710);
  AUC biên **0,69–0,72** ⇒ mỗi bước cứu được trả ~1 bước lật sai. Trần nếu bỏ cuộc hoàn hảo
  **78,0%** trên dev ⇒ **14,6 pp nằm trọn ở khâu bỏ cuộc** và không sửa được ở suy luận.
· Chỉ 120/275 (43,6%) bước bỏ-cuộc-sai có vàng đứng đầu theo tổng; **32,5%** trong 120 đó câu
  mang động từ không chạm ⇒ lật thẻ cũng không tăng `exec`.
· Mô hình bỏ cuộc theo **độ đông khối** (30,6% → 50,2%) trong khi tỉ lệ HasAns phẳng (74 → 67%).
⚠️ **Lý do đến sau khi thấy số, KHÔNG dùng để mở lại ②:** τ₀ không mô phỏng được việc lượt ② bỏ
2.495 bước không chạm. Ghi ở (x18); nếu về sau train theo hướng đó thì là **quyết định mới**.

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
⭐ **Đo trên đủ 22.854 cặp bằng tokenizer Qwen2.5-VL** (kiểm chéo hai lượt): độ dài token accepted
**44** vs rejected **45** (p5–p95 đều 37–58) · `|Δ|≤2` token **62,8%** · đuôi câu trùng token
**22.854/22.854** · chuỗi dài nhất **2.002** token ⇒ **0 cặp bị cắt** ở cutoff 2.560.
⚠️ Từ mã đã pin: **trainer ghép cặp zero mọi dropout lúc dựng model**, gồm LoRA dropout 0,05 mà
trainer SFT vẫn giữ ⇒ **MIN và CE2 lệch một biến không kiểm soát**, phải khai khi báo Δ.


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
⭐ **Hai ô của bảng chéo, đo thật từ tệp thô — `harness/o_bi_loai_khoi_bang_cheo.py`** (tái lập
trùng khít bốn ô +5,72 / +0,54 / +1,11 / −25,20):
· **ô bị bảng chéo loại** (có descriptor, không có tên vàng để đối chiếu): **n=881, Δ=+1,48 pp**,
  KTC95 **[−1,16 · +4,10]** — ngược dấu headline nhưng phủ 0.
· **phần bù ô "cả hai đúng"**: **n=1.374, Δ = −13,10 pp** [−15,39 · −10,77]. ⛔ **KHÔNG phải
  −25,2** — con số đó là của riêng ô *"cả hai sai"* (n=738); một kết luận cũ đã gán nhầm.


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

## ▶️ VIỆC KẾ — lấy ở lộ trình bốn chặng của `report/152`, không lấy ở đây

⚠️ Danh sách "việc kế" từng nằm ở mục này **đã hết hiệu lực toàn bộ** (SOICT bỏ · lượt A100 đối
chứng huỷ · τ xong · hạt 202 vô hiệu theo (x20c)). Việc đang làm đọc ở khối *8/9 — BẢN THI HÀNH
`151`* và *9/9 — CHẶNG 1 XONG · PHASE 0 XONG* bên trên. Ba thứ của mục cũ còn giá trị:

⭐ **Cổng cơ học (đo 25/8, `report/106` mục x9a)** — trên 3.473 bước có tên vàng: S2 **53,9** ·
CE2-S2 **59,8** · MIN-DESC **60,6**.
⚠️ **Quy công:** CE2−S2 **+5,93** (SFT thuần) · MIN−CE2 **+0,84** (riêng ORPO) ⇒ tổng **6,7665**,
ORPO chiếm **12,34%**. ⬅ sửa 9/9: ba số cũ 5,90 / 0,80 / 6,70 tính bằng cách **trừ hai số đã làm
tròn**; số đúng lấy từ đếm bước (2077−1871=206 và 2106−2077=29 trên 3.473). Quy công cho nhánh so
sánh là **87,66%**, không phải 88,1%; hệ số chuyển đổi thành **0,42**, dự báo ≈+0,35 không đổi.
⛔ Cấm trình +6,77 như công của mục tiêu ưu tiên.

⭐ **Phép B ĐÃ XONG 20/8 — đòn "UGround quen văn phong AC" ĐÃ ĐÓNG.** Chấm lát 2.532 bằng
`UI-Venus-Ground-7B` (sạch AndroidControl), cả ba nhánh, 8,15 giờ Kaggle. Đọc bằng
`harness/phan_tich_venus.py`; runbook `harness/kaggle_phepB_uivenus.md`.

| phép so (lát 2.532) | UGround | UI-Venus |
|---|---|---|
| **S1 − Base** (phép so đối chiếu) | **+10,35** [+8,39 · +12,40] | **+9,68** [+7,60 · +11,78] |
| **S2 − S1** (quy về 4.463) | **−1,93** [−3,08 · −0,78] p=0,0005 | **−1,21** [−2,30 · −0,12] p=0,026 |

· ⭐ **Phép so đối chiếu giữ 94%** ⇒ thang đo **không bị nén**, Δ đọc được — bẫy pha loãng không
  xảy ra. Trần cổng A: UI-Venus **69,3%** [63,8–74,8] vs UGround **70,0%** [64,5–75,3].
· ⭐ **S2 thua dưới CẢ HAI dụng cụ**, mép trên KTC đều dưới 0 ⇒ *kết quả âm, tái lập qua hai bộ
  trỏ độc lập*. ⚠️ Nhãn vẫn là **một hạt giống** — phép B đóng đòn *dụng cụ*, không thay được hạt
  giống thứ hai, mà S2/202 thì không chạy (x1).
· ⭐ **Phép rút gọn lát tự kiểm ĐÚNG TUYỆT ĐỐI:** lát 2.532 quy về 4.463 cho −1,9270 pp, tính
  thẳng trên 4.463 cũng −1,9270 pp, b/c trùng 340/254.
· ⭐ **Sai số khoảng cách KHÔNG dự đoán được trần:** UI-Venus thua rõ ở khoảng cách (trung vị
  1,56% vs 0,73%, p75 16,35% vs 9,08%) nhưng trần chỉ kém 0,7 điểm — vì thước quyết định bằng
  ngưỡng 14% rồi mới Voronoi. Dùng lại được cho mọi lần đổi dụng cụ.
· 🔬 Hậu kiểm (một hạt giống): hiệu-của-hiệu ghép cặp, Δ(S2−S1) dưới UI-Venus **+1,26 pp** so với
  dưới UGround, KTC95 **[+0,04 · +2,51]** ⇒ bằng chứng **yếu**. ⛔ Không mở được cửa "UGround
  thiên vị nên S2 thua": nếu vậy Δ dưới UI-Venus phải về 0 hoặc dương, đằng này vẫn âm có ý nghĩa;
  và một phần chênh là **cơ học** vì UI-Venus đo thấp hơn 2,8–4,1 pp ở mọi nhánh. ⛔ **UI-Venus
  KHÔNG "cho số đẹp hơn"** — điểm THẤP hơn ở cả ba nhánh (39,06 / 48,74 / 46,60 vs 42,50 / 52,84
  / 49,45).
· ⚠️ Cỡ ảnh **3.354 tok OOM trên T4×2**; chốt **1.272 tok** vì KTC hai trần chồng nhau ⇒ chọn cỡ
  **nhanh nhất** (4,0 s/bước), phải khai đúng vậy trong bài.

✅ **MÌN ĐÃ GỠ 29/8** — `test_ac/descriptors.jsonl` nay là bản tiếng Anh (bản Việt giữ ở
`descriptors_VI_0809.bak.jsonl`). So từng bước bản cũ↔mới trên 4.448 bước: `name` · `point_norm` ·
`tier` · `name_src` · `box` · `dup_name` · `same_role` **lệch 0**, chỉ `role` và `hint` đổi ngôn
ngữ ⇒ **không con số nào đã công bố phải sửa**. Chi tiết `report/125` mục 1.

⛔ **Đã bỏ khỏi danh sách, có lý do đo được:** train s2/202 (quyết 23/8) · `s2_nopoint` · `s2r`
(`report/117` Mục 3). ✅ Smoke ORPO đã qua 23/8, không phải chạy lại (`106` mục x3c).

**Ràng buộc tài nguyên:** Kaggle **30 giờ GPU/tuần** (mỗi lượt chấm 5,6 giờ ⇒ tối đa 5 lượt/tuần,
đừng dồn). Đơn vị Colab: **đếm lại trong phiên**, con số ghi trong file lỗi thời rất nhanh.
Dataset Kaggle đã dựng: `thesis-score` (1,69 GB, 4.463 ảnh) và `thesis-preds` (805 KB).

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
⚠️ **Hai mẫu số hay bị ghi nhầm, đã vá 31/8:** bảng bơm lỗi có mẫu số **250 bước × 4 góc bơm =
1.000 lượt** (`106` dòng 270) ⇒ 843/1000 và 997/1000, **không phải n=250** (trên 250 thì 84,3%
và 99,7% là bất khả thi). Và `73,6% + 22,0%` hụt **4,4%** = tầng *chỉ có ký hiệu*: ba tầng nhãn
là **30.252 / 1.809 / 9.038 = 41.099**.


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
| `hit_disk` của S2 = **67,5** · `action_ok` = **94,9** (`report/119:62`) | **67,44** và **94,85** | ⚠️ **SỬA 9/9: câu "bài in đúng" là SAI.** Luận văn `tab:phanra` in **cả hai** ô sai, thừa kế thẳng từ `119`; tính lại từ tệp thô ra 3010/4463 = 67,443 ⇒ **67,4** và 4233/4463 = 94,846 ⇒ **94,8**. Cùng lượt bắt được ô thứ ba: `hit_disk` nhánh ứng viên 2961/4463 = 66,346 ⇒ **66,3**, bài in 66,4. Cả ba đã vá 9/9 |

Danh sách đầy đủ + 24 lỗi đã bắt: `report/108`.

---

## 📰 HAI BÀI BÁO — ĐÃ NỘP, ĐÓNG LẠI

Chi tiết nằm trong các tệp của chính hai bài, **không nhắc lại ở đây**: `paper/fair2026/` +
`report/129 · 130 · 131` (FAIR) · `paper/vcl2026/` + `paper/vcl2026/README.md` (VCL, có bảng quy
cách template) · `report/118` (phản biện bốn giám khảo, bảng phân số giữa hai bài). Skill
`vcl-fair-paper` giữ checklist nộp. Luận văn tả hai bài ở **ch8**.

· **VCL2026** — nộp **30/8**, tiếng Việt, đóng góp là nhãn quy chiếu + quy trình dựng dữ liệu.
  21 trang, 0 overfull. Hội thảo tại HUFLIT **27/11/2026**; phí **1.000.000 VNĐ/báo cáo được
  duyệt**. Ba việc nhỏ chưa xử: hậu tố APA `2020a/2020b`, font là TeX Gyre Termes chứ không phải
  Times thật, và chưa chuyển được sang `.docx` (máy không có `pandoc` lẫn `libreoffice`).
· **FAIR'2026** — nhan đề *Descriptor and Preference Targets for GUI Instruction Generation*,
  7 trang, đóng góp mô hình.
  ⛔ **VIỆC CÒN TREO DUY NHẤT CỦA CẢ HAI BÀI: EDAS #276 (ID 1571349424) vẫn `Pending (no
  manuscript)`.** Đăng ký kịp 31/8 nhưng bấm upload lúc 00:02 1/9 thì cửa đã đóng; đã gửi email
  kèm PDF cho **PGS.TS. Trần Văn Lăng (`langtv@vast.vn`)** xin mở lại upload và **chưa có hồi âm**.
  Kèm theo: sửa last name của thầy trên EDAS (`Nguyen` → `Long`) và thống nhất affiliation.
  File đã gửi: `paper/fair2026/FAIR2026_1571349424.pdf` — 106.258 byte, md5
  `ab60520318a8aa34e0f58bcb08f3f035`. Mốc: **báo kết quả 15/9**, hội nghị **8–9/10**, kỷ yếu IEEE.
· ✅ **Chính sách trùng lặp: rủi ro ĐÓNG** (kiểm 29/8). VCL không có điều khoản nào về nộp đồng
  thời; FAIR có, nhưng áp cho *cùng một bài*, mà đây là hai bài khác nhau theo bảng phân số. Trích
  chéo dạng "đang bình duyệt" chính là cách khai minh bạch.

### ⛔ Lệnh dựng LaTeX — bài học đắt nhất, áp cho luận văn lẫn hai bài đã nộp

**`tectonic -X compile main.tex --outdir .`** (ghi sẵn ở `thesis/build.sh`). Máy **không có
`xelatex`**; trợ lý từng tự chế `xelatex … >/dev/null 2>&1`, `command not found` bị nuốt, nên mọi
lần báo *"n trang, 0 overfull"* đều là đọc PDF cũ. Lặp hơn mười lần trong một ngày.
⇒ **Luật: KHÔNG `>/dev/null 2>&1` trên lệnh dựng; kiểm `ls -la main.pdf` mốc giờ trước khi tin
số trang.**
⛔ **`main.log` trong kho là BẢN CŨ — tectonic KHÔNG ghi log trừ khi có `--keep-logs`.** Ngày 29/8
log FAIR còn là bản 25/8, báo *"8 trang"* trong khi bài đã 9 trang. Suýt nộp bài quá trang.
⇒ **Cách đúng:**
```
rm -f main.log && tectonic -X compile main.tex --outdir . --keep-logs
grep -oE "Output written on main\.xdv \([0-9]+ page" main.log   # số trang
grep -c Overfull main.log                                        # phải là 0
```
⚠️ Sửa toàn chuỗi cùng độ dài (đổi chữ số) thì **PDF ra đúng bằng byte cũ** — đừng đọc kích thước
tệp không đổi thành "dựng hụt".
⛔ **Lỗi in ấn phải nhớ:** xuống dòng ngay sau gạch nối trong nguồn TeX làm bản in ra
**`byte- identical`** (thừa dấu cách). Đã lọt vào một bản PDF. **Không xuống dòng sau gạch nối.**

### 📖 LUẬN VĂN — nhật ký đồng bộ đã nén; **luật viết dưới đây còn hiệu lực toàn bộ**

Trạng thái hiện tại (124 trang) ghi ở hai khối 9/9 bên trên. Phần này giữ **luật viết** và các
quyết định về nội dung, đã bỏ nhật ký "chương nào thêm mục nào" của các bản 30/8 · 5/9 · 6/9.

**Nội dung đã chốt, đừng mở lại:**
· **Tên đề tài chính thức (user gửi 5/9):** VI *"Phát sinh tự động hướng dẫn sử dụng phần mềm dựa
  trên LLM từ các trường hợp sử dụng và giao diện người dùng"* · EN *"LLM-Based Automatic
  Generation of Software User Guides from Use Cases and Front-End Structures"*. Đã thay ở
  `main.tex` (`\TenDeTai` ngắt 4 dòng cho vừa bìa), README, bìa + footline deck. Tên cũ *"Sinh
  hướng dẫn sử dụng phần mềm từ ảnh màn hình"* chỉ còn ở deck trình thầy 16/8 (chưa đụng).
· **ch4 có định nghĩa dải bốn ô** (≥+2,8 / +1,7…+2,8 / −2,8…+1,7 / ≤−2,8, khoá 17/8/2026). Trước
  6/9 dải này được DÙNG ở ch6 mà **không định nghĩa ở đâu** — lỗ thủ tục do lượt phản biện bắt
  được. Kèm đoạn khai thẳng: **S2 − S1/202 = −2,44 [−3,53;−1,34] thoả cả hai điều kiện theo chiều
  gây hại**, không đọc thành kết luận vì đại lượng đòi trung bình hai hạt giống.
· **ch5 đã bỏ hẳn "78,0% / 79,3% của trần"**, thay bằng nếp Zhao EACL 2021 (hai số cạnh nhau +
  "khoảng cách còn lại", gọi 75,7 là *ước lượng thận trọng* theo Nangia & Bowman ACL 2019).
· ⛔ **Chấm tay 100 câu: user quyết KHÔNG làm (6/9)** — giữ nguyên cách khai hạn chế ở ch7.
· ⚠️ **`\Khoa` vẫn là ô `\CANDIEN`** (khoá đào tạo) — cần user điền.
· ⛔ **`thesis/main.pdf` bị khoá ghi khi user đang mở PDF** — tectonic báo `Permission denied`
  **sau khi** đã in `Writing ./main.pdf`, và file trên đĩa vẫn là bản cũ. Cách làm: dựng vào
  `--outdir <scratchpad>/build` để đọc số trang, rồi nhắc user đóng trình đọc và dựng lại.

**⭐ BA CHỈ ĐẠO VĂN BẢN 5/9 — mọi đoạn viết mới phải theo** (memory `van-phong-luan-van`):
① **"người viết" bỏ hẳn**: "câu (do) người viết" → **"câu chuẩn"** (có mục giải nghĩa trong danh
mục thuật ngữ), "câu hướng dẫn do người viết" → "do người chú thích viết"; **hạn chế "nó"** (đã
giảm 157 → 17 chỗ, thay bằng danh từ).
② **Gỡ toàn bộ khung "đăng ký trước"**: không còn "đăng ký / khoá / niêm phong / kho phiên bản /
mục sửa đổi / cam kết / thăm dò"; §4 nay tên là **"Tiêu chí đọc kết quả"** (giữ bảng bốn kết cục
+ MDE); nhãn "thăm dò" → **"một hạt giống"**; "cổng chặn" → "điều kiện / tiêu chí / ngưỡng dừng".
Lý do user: *"người ta chỉ quan tâm phương pháp, metric, hiệu quả, thực nghiệm"*.
③ **Cắt phần rối/hội đồng không cần** — đã bỏ §ghi nhận lượt train chi tiết (total_flos, resume),
hai phép kiểm cơ học, đoạn B-infer, "phương án OCR-trước đã loại", số đã rút 70,0, ước lượng 65,0
của S2/202, bốn bullet hạn chế yếu.

**⭐ THUẬT NGỮ THỐNG NHẤT TOÀN KHO** (grep cuối 5/9 đã về 0 cho nhóm bên trái):
· "đối chứng" → **"nhánh so sánh"** (CE2-S2, gui_sft_match) / **"nhánh kiểm sàn"** / **"mốc so
  sánh lệch chủ ý"** · "dám chọn" → **"đưa ra lựa chọn"** · "đường ống" → **"quy trình"** ·
  "thước đồng báo" → **"thước báo kèm"** · "barem" → **"mốc đối chiếu"** · "Cổng" (tiêu chí kiểm)
  → **"tiêu chí"** · "nơi" (dịch *where*) → **"trong đó / theo đó"** · `sel_acc` trong văn xuôi →
  **"độ chính xác chọn"** · "card" → **"GPU"** · "trượt" nghĩa *không đạt tiêu chí* → **"không
  đạt"** (giữ "trúng/trượt" nghĩa lệch mục tiêu) · giữ "bỏ cuộc" và "tức".
· Từ 30/8: `cơ chế hỏng`/`kiểu hỏng` → **dạng lỗi** · `chỗ hỏng`/`chỗ nghẽn` → **điểm nghẽn** ·
  `checkpoint` → **điểm lưu** · `chứng nhân` → **phép so đối chiếu** · `nhiễm văn phong` →
  **thiên vị theo văn phong** · `phần bị đụng` → **phần bị tác động** · `quota` → **hạn mức máy**.
· Bảng thay từ đầy đủ (tụt→giảm, hỏng→sai/lỗi/điểm nghẽn, lọt→lẫn, gánh→chiếm, miễn phí→không
  tính phí, kiểu→dạng, cái→điều…) ở memory `van-phong-luan-van`; chuẩn tham khảo `thesis/_reference/`.

**⭐ LUẬT TRÌNH BÀY (30/8, user chỉ đích danh):**
· ⛔ **Bỏ sạch dấu gạch dài `---`** — viết lại câu bằng dấu phẩy, ngoặc đơn hoặc dấu hai chấm.
  Khoảng số `$a$--$b$` đổi thành `$a$ đến $b$`; chỉ giữ en dash ở số trang tài liệu tham khảo.
  Ô trống trong bảng dùng `-`.
· ⛔ **Bỏ cụm ghép gạch nối kiểu tiếng Anh trong tiếng Việt** (`không-gây-hại`, `câu-sai-màn`,
  `tất-cả-hoặc-không`, `dạy--kiểm`, `S1--Base`). Chỉ giữ `nơ-ron`, `mô-đun`, `ĐHQG-HCM`.
· ⛔ **Tiêu đề mục KHÔNG viết dạng câu hỏi**, và **không câu hỏi tu từ trong thân bài** — kể cả
  mệnh đề nghi vấn gián tiếp không có dấu `?`.
· ⛔ **Không ẩn dụ thể thao / đời thường** ("lợi thế sân nhà", "được ăn cả ngã về không", "giám
  khảo đã học đề thi"). Tiêu đề `\paragraph` cũng bỏ giọng đối thoại.
· ⛔ **Bỏ mở đầu câu lộ giọng máy:** "Nói gọn:", "Nói cách khác", "Điều đáng nói", "Cái mà…",
  "đằng này", "nghe như", "ăn điểm", "bê nguyên văn", "leo thước". Bỏ nhịp câu lặp cấu trúc kiểu
  *"Nó ngắn, nó chỉ nói về…, và nó viết cho…"* — dấu hiệu máy viết rõ nhất.
· **Câu dài nhồi nhiều số phải tách ra**; câu cụt phải viết đủ chủ ngữ vị ngữ; thuật ngữ nêu lần
  đầu phải giải thích ngay bằng lời thường, kể cả khi đã có trong danh mục viết tắt.
· ⛔ **Gỡ chi tiết mã khỏi thân bài** — không tên file, tên tham số, tên cờ (`total_flos`,
  `strict_back`, `use_cache`, `max_samples`, `desc_neg`, nhãn `p1`…`p4` nay gọi thẳng *"đổi động
  từ thao tác"*…). Tên nhánh viết hoa: **S1 · S2 · S2r · S2-nopoint**.
  ✅ **Được giữ** vì tả *dữ liệu* chứ không phải mã: `<desc>`/`<point>` · `(no name)` ·
  `(episode_id, step_id)` · `content_description` · `step_instructions` · tên hai kho HuggingFace ·
  ví dụ chuỗi OCR · `q,k,v,o,gate,up,down`.
· **Hai hình:** Hình 4.1 (quy trình) vẽ bằng **TikZ** ngay trong `main.tex`
  (`positioning,arrows.meta,backgrounds,fit`); Hình 5.1 (luật chấm) là ảnh màn hình thật có phủ
  lớp vẽ + chú giải sáu mục, dựng bằng `harness/make_fig_voronoi_vi.py` (chạy bằng
  `~/.venvs/thesis/bin/python`, cần `huggingface_hub`); bản tiếng Anh `make_fig_voronoi.py`.
· ⛔ **Quét toàn kho sau mỗi lần rút số** — `total_flos` sai đã sống trong `.tex` nhiều ngày sau
  khi đã rút ở `CLAUDE.md` và `report/108`; hai số đã rút khác (12,6% "trên 99.131 màn", lát thử
  "nhỏ hơn 24 lần") cũng sống tới 30/8 mới bị bắt.

**Deck bảo vệ `LUAN_VAN_SLIDE_BAOCAO.pptx` (cập nhật 9/9 lượt hai): 29 slide chính + 15 dự phòng**,
lời nói **23:45** ở 135 từ/phút (mốc giây trong notes tính tự động từ số từ) ⇒ ⚠️ **chỉ còn ~1 phút
đệm cho 25 phút**, muốn giãn thì cắt slide 25 (nhánh ứng viên, 85 s — nhánh đã đóng, đã có dự phòng
B12) hoặc slide 15. Lượt hai thêm: **slide 20 chặng ba** (khai báo +2,56 nhưng exec +0,02, dự báo
+1,10 bị bác, 66,7% đổi khai báo không tới câu) · hàng **60,07** vào bảng kết quả slide 16 · hướng
phát triển xếp lại theo ch7 (**mở thị giác đứng đầu, P≈0,30**) · kết luận nêu 60,07 và 0/5 vượt MDE
· B7 thêm hàng chặng ba + nội suy · **B7b mới** (đường cong nội suy + lý do cấm trích số val).
Dự phòng
gồm B1 (BLEU/ROUGE) · B3 + B11 (D.3) · B6 (*"hai lượt duyệt"*, không phải "một epoch") · B7 ·
B12 (dấu hiệu bỏ cuộc + thủ tục τ). `make_kichban.py` sinh kịch bản. Slide không xưng "em / thầy
cô / hội đồng"; notes là gạch ý ngắn để user tự nói. Deck trình thầy `LUAN_VAN_SLIDE.pptx` (16/8)
**chưa đụng**, vẫn là bản trước MIN-DESC.

### ⛔ Ba thứ đã chết, đừng theo

· **`report/KE_HOACH_2_BAI_BAO.md` (bản 3, 12/7)** và **bản 18/8 đặt bài chính ở thước đo** — cả
hai đã bị quyết định 23/8 thay toàn bộ. Giữ để tra lịch sử, đừng đọc như kế hoạch.
· **Khung prompting DG1/DG2** (ReOrder-Tutor, Copeland, MobileViews, ScreenSpot, "không
fine-tune", GPT-4o E2E) **đã bị bác 19/7** nhưng còn sống trong skill `vcl-fair-paper` hơn hai
tháng trước khi viết lại 1/9. Bản cũ ở `report/_archive/SKILL_vcl-fair-paper_DG1_DG2_TRUOC_VIET_LAI_1_9_2026.md`.
⚠️ **`.claude/` nằm trong `.gitignore` từ `b755cc7` nên skill KHÔNG có lịch sử git** — sửa lớn
phải tự sao lưu trước. ⚠️ **`CLAUDE.md` thắng mọi skill khi mâu thuẫn.**
· **Nhánh faithfulness trên MobileViews** (đóng góp phụ số 2 theo `report/103` ngày 1/8). Kiểm
18/8: **0 lần xuất hiện** trong `report/106 · 108 · 109 · 112 · 113 · 114`, trong `main.tex` của
cả hai bài lẫn luận văn ⇒ khi `103` mâu thuẫn với các file 106+, **106+ thắng**.

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
**Mọi thay đổi về sau ghi vào mục sửa đổi cuối file, KHÔNG sửa đè.** Hiện có **28 mục, 21 mục
trước điểm số đầu tiên** (mục **(x16)** thêm 4/9: thu hẹp còn một lượt A100, hạ `sel_acc` xuống
thước phụ, **đăng ký trước thủ tục chọn ngưỡng τ**, và sửa thuật ngữ *hold-out* → *one-look hậu kiểm*). Các mục đáng nhớ: (k) thêm nhánh mô hình gốc · (o) máy + cấu hình P9 +
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
⭐ **`report/106` có HAI bản luật đọc — biết cả hai, đừng in bản này rồi áp bản kia.**
· gốc 5/8 (dòng 85): Trắng = KTC phủ 0 **VÀ** \|Δ\| < MDE ⇒ S2 có KTC **[−3,06 · −0,75]**
  (cận trên âm) rơi vào ô **ÂM**.
· sửa đổi **(w) 17/8** (dòng 1268): Trắng = dải **−2,8 … +1,7**, chỉ hàng Dương/Âm mới đòi KTC
  loại 0 ⇒ S2 là **TRẮNG**.
✅ **(w) khoá TRƯỚC khi train S2** nên dải hợp lệ — **không** phải ngưỡng dời sau khi thấy điểm.
Nhưng nó khoá **sau** khi S1/Base/trần đã có điểm ⇒ câu *"cả hai mép khoá trước khi có bất kỳ
điểm nào"* là **SAI**. ⇒ In dải làm luật chính, **khai thẳng** rằng mệnh đề khoảng cho ra nhãn
*gây hại* với S2, và áp **đối xứng** cho MIN (khoảng `[+0,16 · +1,10]` loại 0 ⇒ mệnh đề khoảng
cho phép gọi *dương*, nhưng **không** nhận).


## ⚙️ VẬN HÀNH — bài học đã trả giá

⛔⛔ **ĐỒNG HỒ MÁY WSL CHẠY GIỜ UTC, LỆCH 7 GIỜ SO VỚI GIỜ VIỆT NAM.** Lúc `date`
báo 16:53 thì ở VN đã là 23:53. Một phiên đã tưởng còn 7 tiếng trong khi còn 7 phút, và đó là lý
do trực tiếp làm lỡ một hạn nộp. ⇒ **Mọi mốc hạn phải đọc bằng `TZ='Asia/Ho_Chi_Minh' date`,
không đọc `date` trần.**

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

⛔⛔ **BỐN LUẬT COLAB — VI PHẠM LÀ MẤT TIỀN THẬT. Đã trả giá 2–3/9/2026: mất 16 compute
unit, rồi mất máy thêm hai lần trong một đêm.**

**① `subprocess.Popen` phải có `start_new_session=True`.** Thiếu nó thì tiến trình train nằm
**cùng process group** với kernel notebook, và **mọi lần bấm Stop một ô bất kỳ** — kể cả ô theo
dõi — đều gửi SIGINT sang train. Lượt `gui_sel`/101 chết ở bước **747/4036** vì đúng chuyện này;
log ghi `KeyboardInterrupt`.

✅ **ĐÃ KIỂM CHỨNG 3/9, 03:5x — luật ① chạy đúng như thiết kế.** Bấm Stop ô S7 rồi đo ngay:
tiến trình `llamafactory-cli` vẫn còn, `grep -c KeyboardInterrupt` = **0**, log tăng **+107
byte/phút**. ⇒ Với `start_new_session=True`, Stop một ô KHÔNG giết train. Đổi lại bằng 60
giây kiểm, không phải bằng một lượt train. ⚠️ Đo trong khâu mã hoá token; SIGINT lan theo
process group nên kết luận không phụ thuộc giai đoạn, nhưng vẫn nên hạn chế bấm Stop.

**② KHÔNG bấm Stop ô nào khi train đang chạy.** Cần chạy ô khác thì mở **notebook thứ hai**
hoặc dùng **Terminal Colab**. Ô vòng lặp vô hạn (theo dõi) làm mọi ô khác **xếp hàng**, nên
phản xạ tự nhiên là bấm Stop — và đó là cái bẫy.

**③ Ô theo dõi phải đọc log LOCAL `/content/train_*.log`, KHÔNG đọc `trainer_log.jsonl` trên
Drive.** FUSE không cập nhật nội dung khi ghi thêm, nên số bước **đứng yên hàng giờ** dù train
vẫn chạy. Đọc nhầm chỗ ⇒ tưởng treo ⇒ bấm Stop ⇒ mất lượt. Ba lỗi này nối nhau đúng theo thứ tự
đó ngày 2/9.

**④ PHẢI có MỘT ô notebook chạy foreground suốt lượt train (ô S7 của runbook).** Ô S5 (đồng
bộ Drive) và S6 (cảnh báo) đều dùng `daemon=True` nên **ô kết thúc ngay**; nếu lại theo dõi
bằng Terminal thì trình duyệt cũng không có tương tác nào ⇒ notebook rỗi ⇒ Colab ngắt máy vì
**inactivity sau ~90 phút**. Đêm 2–3/9 mất máy **hai lần** đúng kiểu này: dựng lại ~02:00,
chết trước 03:28 — chừng 88 phút, khớp ngưỡng. Lượt chiều 2/9 sống nhiều giờ chỉ vì lúc đó
liên tục có người bấm ô. ⚠️ Đây là suy luận từ mốc giờ khớp, chưa phải bằng chứng trực tiếp;
phép kiểm là lượt kế có sống qua 90 phút với S7 chạy hay không.
⇒ Kèm theo: `save_steps` hạ **200 → 100** ngày 3/9 (thiệt hại mỗi lần mất máy còn tối đa
~21 phút). Đây là **hằng số cho cả sáu lượt**, không phải khoá đổi giữa lượt, nên phép kiểm ②
của ô S3 vẫn xanh.

⚠️ **Và luật chung, đắt hơn cả bốn:** ⛔ **KHÔNG khẳng định chắc chắn một điều chưa kiểm.**
Câu *"bấm Stop không ảnh hưởng gì tới train"* được nói ra mà không kiểm, và chính nó giết lượt
chạy. Chưa kiểm thì nói *"tôi không chắc, để kiểm đã"* — đúng nguyên tắc dự án đã ghi ở mục
*"'Đã xác minh' không phải bằng chứng"*.

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
· sequence-score — **`seq_score_sel.py`** (thi hành hợp đồng `report/134` §6.1 và mục **(x16d)**
của `106`: teacher-force từng span ứng viên + `none`, chia số token, margin `m = s(c*) − s(none)`,
nối tiếp được, `--probe`. Cờ `--cache-prompt` là đường nhanh gấp 5–7 lần, **ba bước đầu bắt buộc
so với đường chậm**, lệch quá 1e-3 là dừng. ⛔ Tệp này **không** quét τ và **không** đọc kết quả)
· train/suy luận/chấm — `train_config.yaml` · **`train_config_orpo.yaml`** (MIN-DESC) ·
**`train_config_ce2.yaml`** (đối chứng) · `infer_branch.py` · `score_run.py` ·
`metric_exec.py` (thư viện hàm chấm — **luật chấm mặc định không đổi từ commit `b93e85c`
ngày 5/8**; bản vá `strict_back` là thêm cờ tuỳ chọn, mặc định tắt, và **hiện chưa commit**) ·
`gate_a_ceiling.py`
· phân tích — `phan_tich_bon_nhanh.py` · `phep_a_ghep_cap.py` · `phep_a_hieu_chinh.py` ·
`mde_that.py` · `rule_sensitivity.py` · `bien_the_khong_tham_chieu.py` · `make_floor.py` ·
`doc_san.py` · `doc_diem_tam.py` · `kiem_preds.py` (8 phép kiểm tệp preds trước khi tiêu quota) ·
**`loss_val_grid.py`** (chấm **loss val** cho từng điểm lưu trong `grid/` trên Kaggle T4, 0 đồng —
bù cho việc lượt VIS-SFT chạy `do_eval: false` nên không có đường cong loss val; nối tiếp được;
⛔ chỉ để **chẩn đoán quá khớp** và thu hẹp vùng cần chấm `exec`, KHÔNG chọn điểm lưu bằng loss,
KHÔNG trích số val ra báo. Lượt train MỚI thì bật thẳng `eval_dataset`/`eval_steps` từ đầu —
đổi sau khi đã mã hoá là cache mất hiệu lực. Chi tiết ở `harness/colab_vissft_9_9.md` mục LOSS VAL) ·
`make_fig_voronoi.py`
· runbook — **`colab_keo_adapter_4_9.md`** (kéo adapter `gui_sel_seed101` khỏi Drive, pin hash,
đóng gói cho Kaggle; kèm cách probe `seq_score_sel.py` trên CPU máy nhà) ·
**`kaggle_commit_sel_4_9.md`** (⭐ chạy Kaggle dạng **commit** để gập máy đi ngủ — §0 là lượt
gộp C1+C2 của đêm 4/9, có **cổng giờ 5,5 h** chặn vượt trần 12 h; bảy khác biệt so với chạy
tương tác; ⚠️ `score_run.py` **không có cờ `--raw`**, nó tự suy tên từ `--out`) ·
**`colab_smoke_orpo.md`** (cổng kỹ thuật MIN-DESC — chạy TRƯỚC mọi thứ) ·
**`colab_train_min_desc.md`** (bốn lượt train + đồng bộ Drive + ô theo dõi có thanh tiến độ) ·
`S2_DAN_THANG.md` · `colab_train_s2.md` · `run_on_colab.md` · `colab_cham_san.md` ·
`kaggle_cham_san.md` · `kaggle_upload_dataset.md` · `kaggle_pheA_CHAY_LAI.md` · `run_on_rented.sh`

`infer_branch.py` và `score_run.py` đều **ghi dần + xả đệm + nối tiếp được**; `score_run` gộp số
cuối **từ tệp thô, không từ bộ nhớ**, nên chạy cắt khúc vẫn ra số toàn tập.

**Nguyên tắc chi tiền — ⭐ ƯU TIÊN TIẾT KIỆM CHI PHÍ (user chốt 5/9/2026):** mặc định chọn
phương án **rẻ nhất cho cùng kết quả**; ưu tiên local/free + cache (Kaggle T4 miễn phí trước
Colab trả tiền); chạy MỘT lần cho đúng; bước tốn tiền phải hỏi trước. Chỉ chi thêm khi cột
*ảnh hưởng độ chính xác* ghi rõ **đổi ở chỗ nào, kèm bằng chứng** — không phỏng đoán, và không
đổi thước hay giảm cỡ mẫu để rẻ. Luôn trình bảng **tiền · thời gian · ảnh hưởng độ chính xác**.

⛔ **So card bằng ĐƠN VỊ MỖI LƯỢT, không bằng đơn vị mỗi giờ.** Card rẻ hơn theo giờ mà chậm
hơn đúng tỉ lệ thì không tiết kiệm được đồng nào. Đo thật 11/8 (`report/110` mục 4h): L4
**31,26 s/bước** vs A100 **10,70** (nhanh 2,92×) trong khi giá gấp **3,44×**; ở cấu hình P10,
tám lượt tốn **858 đơn vị trên A100 vs 856 trên L4** — ngang nhau về tiền, nhưng L4 mất **3,4×
thời gian tường** nên thêm hàng chục mối nối phiên, mỗi mối một lần rủi ro mất bước. Kết luận
*"chuyện chọn card đóng lại"* của 11/8 vẫn đứng.
⛔ **VRAM dư KHÔNG phải tiền phí.** Thấy lượt chỉ dùng 17,5/40 GB trên A100 không có nghĩa là
đang trả thừa — Colab tính theo **giờ**, không theo GB. Và L4 chỉ có ~22 GB dùng được: biên
4,5 GB đo trên mẫu thường **không** kết luận được, vì luật P10 đã ghi *mọi cấu hình đụng bộ nhớ
phải thử lại trên mẫu dài nhất*; L4 từng tràn ở đúng bài này khi bỏ 4-bit.
⚠️ Với lượt **GRPO** còn thêm khâu sinh (bám băng thông bộ nhớ — L4 ~300 GB/s vs A100 ~1.555
GB/s) nên tỉ lệ chậm nhiều khả năng **tệ hơn** 2,92× của train thuần; **chưa đo**, đừng khẳng
định theo cả hai chiều.
✅ **Ba chỗ tiết kiệm thật đã kiểm chứng:** khâu không đụng GPU chạy runtime **CPU** (phiên 0:
0 đơn vị thay vì 43) · khâu **suy luận/chấm** chạy **Kaggle T4 miễn phí** (30 h/tuần) thay vì
Colab trả tiền · giữ `*_raw.jsonl` để đổi luật chấm mà **không gọi lại bộ trỏ** (đã cứu trọn
một lượt 5,6 h).
⛔ Giá GPU phải **tra tại thời điểm quyết, cấm nhớ** — hai con số nhớ sai từng suýt dẫn tới
thuê nhầm máy.

### ⭐ THỦ TỤC CHỌN MÁY — bắt buộc chạy trước MỌI lượt GPU (user chốt 5/9/2026, siết 9/9/2026)

*"Cái nào không cần GPU thì dùng CPU. Cần GPU thì đo RAM trước: card rẻ đủ RAM thì dùng card
rẻ, vượt mới lên A100 — chứ cái nào cũng A100 sao chịu nổi."*

⛔⛔ **SIẾT 9/9/2026 — user nhắc lần hai, nguyên văn:** *"cái nào chạy được bằng CPU thì ưu tiên
CPU, chỉ cái nào cần dùng A100 thì mới dùng Colab A100, còn cái nào dùng được L4 hay T4 thì vẫn
phải ưu tiên dùng. Chứ bạn rút kinh nghiệm hoài tôi không đủ tiền để theo đâu."*

⇒ **BƯỚC 0 MỚI, làm TRƯỚC khi viết bất kỳ runbook nào: phân rã lượt chạy thành từng PHA, gắn bậc
cho từng pha, và tách pha bậc 0/1 ra khỏi phiên A100.** Một lượt train không phải một khối
đồng nhất — nó gồm *bung dữ liệu · mã hoá token · nạp model · train · lưu*, và chỉ **hai** pha
giữa cần GPU. Không được để pha bậc 0 nằm trong phiên bậc 3 chỉ vì tiện tay viết chung một
notebook.

⛔ **Giá đã trả cho đúng lỗi này, 9/9/2026 (lượt VIS-SFT):** khâu mã hoá token 63.000 mẫu chạy
**2,5 h trên A100 với GPU đứng 0 % và bộ nhớ 428 MiB suốt lượt** — trả giá bậc 3 cho việc của
bậc 0, và vì lần đầu quên bật `tokenized_path` nên còn suýt phải trả lần thứ hai. Runbook
`harness/colab_vissft_9_9.md` nay ghi thứ tự đúng: **G1–G4b + G5 trên T4 miễn phí hoặc runtime
CPU** cho tới khi `tok_cache_vissft` nằm trên Drive, **rồi mới** bật A100 chạy G6.
⚠️ Và **không sửa giữa lượt**: đổi máy khi đã chạy thì phải mount lại Drive, bung lại ảnh, mã hoá
lại từ 0 — ăn hết phần định tiết kiệm. Quyết ở bước 0, không quyết lúc đang cháy tiền.

**Bậc thang, luôn đi từ trên xuống, dừng ở bậc đầu tiên chạy được:**

| bậc | máy | giá | dùng khi |
|---|---|---|---|
| 0 | **CPU** (Colab/WSL) | 0 đơn vị | khâu không gọi GPU lần nào — dựng dữ liệu, OCR (onnxruntime CPU), tính lại từ `*_raw.jsonl`, mọi phép đo 0 GPU |
| 1 | **Kaggle T4** (×2, 16 GB/card) | **0 đồng**, 30 h/tuần | suy luận, chấm điểm, sequence-score — đường đã đi nhiều lần |
| 2 | **L4** (~22 GB dùng được) | ~1/3,4 giá A100 mỗi giờ | lượt train/sinh có **đỉnh VRAM ≤ ~17 GB đo trên mẫu nặng nhất** và không bị chậm quá tỉ lệ giá |
| 3 | **A100 40 GB** | đắt nhất | chỉ khi bậc 2 tràn bộ nhớ, **hoặc** đo được là chậm hơn nhiều hơn tỉ lệ giá |

⛔ **Mặc định probe trên card RẺ trước; A100 phải có số đo biện minh** (user nhắc 5/9: *"mốt
bạn nên chạy thử trước rồi quyết định A100 tại vì tốn tiền"*). Ô thăm dò dùng lại được cho mọi
lượt: **`harness/chon_may.md`**.
⭐ **Luật quyết theo tỉ số thời gian `giờ_L4 / giờ_A100`** (user chốt 5/9, **nới lên 1,5× ngày
9/9**): **≤ 1,5× thì CHỌN L4/T4**. Nguyên văn user 9/9: *"cái nào cần chạy A100 mới chạy, còn GPU
vẫn ưu tiên chạy L4 T4 nếu vẫn match. Ví dụ A100 chạy 10 tiếng còn L4 chạy 15 tiếng thì chọn L4."*
⇒ A100 5 h mà L4 7,5 h vẫn chọn L4; A100 10 h mà L4 15 h vẫn chọn L4. **Chỉ > 1,5× mới lên A100.**
Train SFT đo được 2,92× nên vẫn nằm ở ô A100, quyết định 11/8 không đổi.
⭐ **Phân loại chỗ nghẽn trước khi đo:** khâu nghẽn **CPU/IO** (dựng dữ liệu, OCR, mã hoá token)
thì L4 **ngang** A100 vì card nằm không — đo 11/8, cùng 12 lõi, L4 rẻ hơn 3,6 lần cho cùng thời
gian; chỉ khâu nghẽn **GPU compute** (train, sinh mẫu) mới cần đo s/bước.

**Hai phép đo phải có TRƯỚC khi chọn (không đoán):**
① **đỉnh VRAM** `torch.cuda.max_memory_allocated()/2**30` — đo trên **mẫu nặng nhất của nhánh
nặng nhất**, không phải mẫu đầu tập (luật P10, đã trả giá: L4 chạy ngọt mẫu thường rồi tràn ở
200 mẫu dài nhất). Chốt bậc 2 khi đỉnh ≤ ~17 GB, tức chừa biên ≥ 25% trên 22 GB.
② **s/bước** ở cùng cấu hình trên cả hai card, rồi so **đơn vị mỗi lượt** = giá/giờ × giờ/lượt.
Chi phí của cả hai phép đo là **vài đơn vị** (12 phép đo trên 2 card ngày 11/8 tốn ~4 đơn vị).

⛔ **Không đổi card giữa một lượt đang chạy** — mất tiến độ từ điểm lưu gần nhất, cộng 15–25
phút dựng lại dữ liệu và ảnh. Quyết chọn card ở **ô thăm dò**, trước khi bấm lượt thật.

---

## ❓ CÒN TREO

- ⛔ **Hai kho đang lệch.** Máy WSL **không có** `FINAL_SOLUTION.md` lẫn
  `report/115_PHUONG_AN_TD_ROI_DA_RUT.md` — phiên debate 23/8 chạy trên một checkout khác (máy
  Mac). Mọi tham chiếu tới hai file đó trong `report/116` hiện là **tham chiếu chết**. Lấy về khi
  tiện; chưa có cũng không chặn việc gì, vì `report/117` đã tự chứa.

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
