# CLAUDE.md — Bối cảnh luận văn (auto-load mỗi phiên)

> **Dọn lần ba 22/11/2026** (1.700 → ~420 dòng). Bỏ nhật ký các hướng tháng 8–10 đã đóng (MIN-DESC,
> `gui_sel`, τ, GRPO `<point>`, VIS-SFT và Phase 0–2, nội suy, DCRP…) vì số và lý do dừng đã có ở
> `report/HUONG_DA_THU.md` và report gốc; gộp các khối chỉ đạo về thước thành một mục; nén mục vận hành.
> Bản đầy đủ trước khi dọn: `report/_archive/CLAUDE_MD_TRUOC_DON_22_11_2026.md`.
> Các lần dọn trước: `…_TRUOC_DON_9_9_2026.md` · `…_TRUOC_DON_18_8_2026.md` (cùng thư mục).
> `_archive/` **không có trên GitHub** (nằm trên máy và trong lịch sử git). Mở các file đó khi cần tra
> *"vì sao hồi đó quyết định X"*, không phải để biết trạng thái hiện tại.

**Trao đổi bằng tiếng Việt.** Văn phong: xem mục cuối file.

⛔⛔ **BẮT BUỘC: trước khi đề xuất hướng mới, viết mã/runbook/notebook, hay đẩy GPU, tra danh sách các
hướng đã thử bên dưới** (nạp tự động). Hướng trùng thì nói rõ đã thử ngày nào, kết quả, lý do dừng; chỉ đề
xuất lại khi có điểm khác cụ thể. Xong hoặc dừng một hướng thì thêm dòng vào file đó.

@report/HUONG_DA_THU.md

---

## 🗂️ Bản đồ kho

`README.md` ở gốc kho = bản đồ thư mục.

| thư mục | chứa gì |
|---|---|
| `harness/` | mã dựng dữ liệu, train, sinh câu, chấm điểm · runbook Colab/Kaggle ở `harness/runbook/` |
| `report/` | ghi chú và báo cáo đánh số; `report/papers/` = ghi chú tài liệu tham khảo |
| `runs/` | kết quả chấm (`runs/README.md` ghi chỗ đặt từng phép đo) |
| `_scripts/` | mã theo action đánh số (296, 299, 304, 308, 314…) |
| `paper/` | `fair2026/` · `vcl2026/` · `soict2026/guistep/` (bài SOICT thật sự nộp) |
| `thesis/` | luận văn LaTeX; sửa ở `thesis/chapters/`, `main.tex` chỉ `\input` |
| `slides/` | deck thuyết trình luận văn · trình thầy · VCL · SOICT · FAIR + kịch bản `.md`; mã dựng ở `slides/build/` |
| `_bundles/` | gói mang lên Colab/Kaggle (`make_bundle.py`, `_bundles/luoi/make_nb.py`…) |

`harness/` và `report/` **giữ nguyên tên** (hàng trăm tham chiếu + layout gói zip runbook phụ thuộc).
**Kết quả tải từ Kaggle đặt thẳng vào thư mục của phép đo đó**, không để lạc vào `report/`.

## 📚 Đọc file nào

| cần biết | mở |
|---|---|
| **⭐ mọi bảng kết quả** (test, DEV-v3, dụng cụ khác, AitZ, ACU, dev vs test). Tự sinh, đừng sửa tay; số mới thì thêm vào script rồi chạy lại | **`report/334_BANG_KET_QUA_TONG_HOP.md`** · `harness/bang_tong_hop.py` (`~/.venvs/thesis/bin/python`) |
| **⭐ số/việc cần vào luận văn** (nối mục mới, không sửa `thesis/` khi chưa được giao) | **`report/320_VIEC_CAN_CAP_NHAT_LUAN_VAN_23_10.md`** |
| **⭐ lưới RL + thưởng đang chạy** (thầy đòi so GRPO với họ RL, SPICE với độ đo khác; bảo vệ dời 3/2027) | **`report/337_TINH_TRANG_KAGGLE_21_11.md`** (đọc trước) · thiết kế đợt B5: `slides/ACTION_4_THUAT_TOAN_RL_2025_SO_VOI_GRPO_20_11_2026.md` §12 · `report/326_BAN_GIAO_LUOI_RL_1_11.md` · `report/323` §8–12 · `harness/grpo_luoi.py` · `harness/grpo_codien.py` |
| việc chưa làm, chờ user chọn | `report/336_VIEC_CAN_LAM_SAU_15_11.md` |
| việc thêm theo phản biện SOICT (xao101, AitZ, 7B, không chạm, lịch sử tự sinh, độ trễ) | `report/322_VIEC_THEM_THEO_PHAN_BIEN_SOICT_25_10.md` |
| ck500 (GRPO + SPICE) — test, 13 cột, bước không chạm | `report/259` · `report/261` · `report/262` · `report/254` (bàn giao train) · `harness/grpo_spice.py` |
| ACE / R3 | `report/304` §4–5 · `_scripts/304/kiem/` · `runs/ra304_luat/` |
| SA-SPICE-v3 · SPICE-MATCH · SFT-cont · DEV-v3 | `report/333` · `research_notes/Debate SA SPICE v3 sau test/` |
| ck500/R3 dưới UI-Venus + Phi-4 | `harness/venus_ck_doc.py` (chạy `python3 -I`) · `runs/venus/ck500_r3_22_10/` · `runs/venus/bu_22_10/` |
| split chính thức (90% tập kiểm thuộc split *train* của AC) | `report/209` · `runs/split_chinh_thuc/` |
| hướng đã dừng (TAGE, CTG, TRIAD, RA-GRPO, CW-RA, RAFT, GA-DPO, 288, FGRB, PATA, ECGR, TFVF, selector, VIS-SFT, MIN-DESC, `gui_sel`…) | `report/HUONG_DA_THU.md` → report gốc ghi ở cột nguồn |
| cơ chế kỹ thuật toàn dự án, từ đầu | `report/112_HIEU_TOAN_BO_KY_THUAT.md` |
| hồ sơ niêm phong 5/8 + mục sửa đổi | `report/106_DANG_KY_TRUOC.md` |
| số đã đo trước 23/8, số nào đã rút | `report/108_DA_LAM_DUOC_GI.md` |
| tiền lệ đã tra (executability, Zhao, GCoT, Jandial) | `report/114` · `report/141` |
| nguồn từng con số trích từ bài khác | `report/105_NGUON_SO_BANG_GOC.md` |

Mâu thuẫn thì: **mã** thắng về *hệ thống đang làm gì* · `report/334` thắng về *số hiện hành* ·
`report/337` về *kernel đang chạy* · `106` về *estimand và ngưỡng đã khoá lịch sử* · `112` về *cơ chế*.
`109`, `116`, `119`, `151`, `152` là bản đồ/kế hoạch **cũ** — chỉ đọc để tra lịch sử.

---

## ⭐ TRẠNG THÁI HIỆN TẠI (22/11/2026)

**Bảo vệ dời sang 3/2027** (thầy 1/11): phải so GRPO với các họ RL khác, SPICE với các độ đo thưởng khác,
và giải thích vì sao. Mục tiêu user (13–14/9, vẫn hiệu lực): *tốt nghiệp với số cao nhất bảo vệ được*.

**Phương pháp trong luận văn** (user chốt 4/10): **GRPO thưởng SPICE từ S1 = ck500** (ch4
§`sec:grpospicethietke`); **ACE/R3** là mở rộng (ch4 §`sec:acethietke`, ch6 §`sec:ace`). Tiền lệ SCST
(CVPR 2017) + SPIDEr (ICCV 2017); điểm mới phát biểu hẹp (không nhận mới ở thuật toán hay ở việc chọn SPICE).

**Số test chính** (4.463 bước chạm, exec chấm bằng UGround-V1-2B; chi tiết + KTC ở `report/334`):

| nhánh | exec | ghi chú |
|---|---|---|
| câu chuẩn (mốc dụng cụ) | 75,73 | D.3 83,8 · AitW đầy đủ 92,1 |
| SA-SPICE-v3 ck400 (từ SFT-cont) | 61,21 | − ck500 +0,56 p=0,069 · back không chạm 71,1 → 58,5 (phải khai) |
| SPICE-MATCH ck400 | 60,88 | ablation của SA, ≈ SA |
| ACE / R3 | 60,68 | 7/7 độ đo văn bản hơn ck500; exec ≈ ck500 |
| **ck500** (hạt 101) | **60,65** | − S1/101 **+1,55 [+0,80; +2,33]**; hạt 202: 59,94 (− S1/202 +0,31) |
| SFT tiếp (cùng câu nhắc) | 60,16 | ck500 − SFT tiếp +0,49 p=0,11 |
| S1/101 · S1/202 | 59,11 · 59,6 | SFT trơn Qwen2.5-VL-3B QLoRA |
| Qwen2.5-VL-7B prompting | 51,51 | mốc ngoài |
| Base | 47,59 | |

Caveat phải khai khi viết về ck500:
- Một hạt có ý nghĩa, hạt 202 dương nhưng không ý nghĩa; mức tăng ~+1,5 dưới MDE ~2,1.
- Bước không chạm: **scroll 83,97 → 77,75** (ck500 dịch về câu chạm), back −5,93.
- Lượt A/A train lại cùng công thức ra 59,74 ⇒ hai lượt cùng công thức lệch 0,7–0,9; phần tái lập được là
  sửa loại thao tác, "đổi đúng phần tử +41" chỉ có ở một lượt.
- ck500 > S1 giữ qua ba dụng cụ: UGround +1,55 · UI-Venus +1,55 [+0,82; +2,30] · Phi-4 +0,69; nhưng Venus
  vẫn họ Qwen ⇒ không viết "kết luận chắc chắn".
- Lưới RL 3/11: ck500 60,65 · GRPO+ROUGE-L 60,63 · SCST+SPICE 60,54 · GRPO+METEOR 60,27 · GRPO+CIDEr-D 60,27
  ⇒ chỉ viết "nhóm dẫn đầu", **cấm "SPICE tốt nhất"**, chưa được viết "SPICE giúp định vị tốt hơn".
- Lịch sử tự sinh (thay câu chuẩn bước trước): ck500 − S1 vẫn +1,48. ACU (phần S1 chưa thấy): +4,58. AitZ
  zero-shot: ck500 ≈ S1.

**Đợt B5 lưới RL (từ S1, hạt 101, cùng 1.000 câu nhắc ck500)** — trạng thái 22/11 tối (`report/337` §11–12,
bảng log train ở `HUONG_DA_THU.md` §2e):
- **Dr.GRPO đầy đủ có số test:** exec 60,00, − ck500 −0,65 [−1,11; −0,18] p=0,009 (thua), − S1 +0,90; độ đo văn
  bản ngang ck500 cả 6 cột (`report/320` §30).
- **Xong train ck500, chờ test (5 lượt):** DPO trực tuyến · GRPO + chrF · + BLEU-4 · + SPIDEr · + BERTScore. Adapter
  đã lên dataset `uyenle0712/b5-ck-22-11`; smoke test Kaggle `luoi-test-u-b5smoke` **đạt** (5/5 tìm đúng adapter,
  kiểm bộ chấm 10/10), số smoke không dùng. Test thật: Kaggle sau 28/11 hoặc Colab (`harness/runbook/colab_test_b5_22_11.md`).
- **DPO trực tuyến test trên Colab T4:** dừng giữa chừng 22/11 22:26 (script canh tắt máy khi CLI mất kết nối, đã vá),
  mới sinh **1.163/4.463 câu** (`runs/luoi/20_11/luoi-test-c-dpo/` + Drive); chạy lại thì nối tiếp, cần user bấm link
  drivemount. Kiểm bộ chấm trên Colab 9/10 (Kaggle 10/10) ⇒ phải khai.
- **Dừng giữa chừng, chờ hạn mức 28/11:** GRPO μ=2 và GSPO ck750/1.000 (thưởng đều không tăng; còn 250 bước,
  PREV=`trangphuongngoc/luoi-b5-t2-3`) · DAPO ck400 · REINFORCE++ lô 64 ck70/125. GRPO/REINFORCE++ lô 128 chết RAM,
  chưa sửa mã (user chưa đồng ý hướng sửa).
- Hạn mức ba tài khoản gần cạn tới 28/11 07:00 VN; theo `report/337` §12 không còn lượt GPU nào đang chạy. Runbook `_bundles/luoi/CHAY_B5.md`.
- Có số test thì ghi vào `HUONG_DA_THU.md`, `report/320`, `report/334` cùng lúc.

---

## 📏 THƯỚC ĐO — đã chốt, đừng mở lại

**Chỉ đạo user 14/9 (thắng mọi luật "không đổi thước / ngưỡng đăng ký trước" cũ):** chọn thước ① đã có tiền
lệ, có trích dẫn, ② trong số đó chọn thước cho số cao. Bỏ khung khoá trước/niêm phong. **Vẫn giữ** vì hội đồng
bắt được: số thật tính từ tệp thô · khai đúng tên và nguồn thước · in mốc câu chuẩn cạnh số mô hình · không bịa
trích dẫn · không tuyên bố "hơn có ý nghĩa" khi bảng trong bài tự mâu thuẫn.

| vai | thước | ghi chú |
|---|---|---|
| tiêu đề, phép kiểm ý nghĩa | **exec** = `action_ok` ∧ ±14% ∧ Voronoi | niêm `b93e85c` 5/8 |
| báo song song (user 13/9) | **D.3** — điểm dự đoán nằm trong hộp phần tử vàng | luật gốc AndroidControl, Li et al. NeurIPS 2024 D&B, Phụ lục D.3 |
| báo kèm | **AitW đầy đủ** (‖Δ‖ ≤ 0,14 ∨ cả hai điểm trong hộp vàng nới 1,4×) | `harness/luat_aitw_day_du.py`; chỉ có hộp vàng ⇒ chỉ có thể thấp hơn luật gốc |
| cận trên | AitW với mọi khung bấm được | sàn câu rỗng 41,6 ⇒ chỉ trình như cặp cận dưới/cận trên |
| văn bản | BLEU-4 · METEOR · ROUGE-L · CIDEr-D · SPICE (bộ chấm COCO, Java 8 ở `~/.jdk/`) · chrF · BERTScore (roberta-large L17 rescaled) | `harness/text_metrics_coco.py` · `text_metrics_them.py`; câu rỗng tính 0 |
| độ bền dụng cụ | UI-Venus-Ground-7B · Phi-4 SoM (người nghe ngoài họ Qwen, trần 54,9) | không làm tiêu đề |

Vì sao:
- **D.3 không phải nới lỏng:** dung sai thích ứng theo cỡ phần tử (chiều dọc trung vị 5,2% màn, chặt hơn ±14%
  tới 5 lần); trên lát 800 trần +8,12 mà sàn câu rỗng chỉ +2,12 ⇒ dải dùng được 62,88 → 68,88. Phản biện
  `report/139`: 48% hộp là nút con, 78% mức tăng từ hộp rộng ⇒ khai.
- **±14% đơn thuần (d14) không làm tiêu đề:** câu rỗng nghĩa `"Tap the button."` 12,00 dưới exec nhưng 20,50
  dưới d14 ⇒ 86% mức tăng là thứ câu rỗng nghĩa cũng lấy được.
- **Bộ trỏ mạnh hơn cho điểm thấp hơn:** UI-Venus (ScreenSpot cao hơn) thua UGround ở cả ba nhánh; 72% ca thước
  mù là bộ trỏ lệch >14% (bỏ cuộc), không phải trỏ nhầm nút bên cạnh. Sai số khoảng cách không dự đoán trần.
- Chặng ba − S1 dưới AitW +2,94 thì +3,11 đến từ 256 bước S1 sai loại thao tác ⇒ **nguồn là cổng loại thao tác,
  không phải định vị** (đã sửa luận văn 21/9).
- ⛔ Cấm cộng dồn exec với D.3 thành một mũi tên. Cấm dùng luật lỏng để tuyên bố một phép so có ý nghĩa khi exec
  không có (ví dụ: Holm cho GRPO − S1/101: ±14% giữ, Voronoi mất).
- ⛔ **Cấm "79,3% năng lực của người"**, cấm gọi 75,73 là "mức người". Cách đúng (Zhao EACL 2021, Nangia &
  Bowman ACL 2019): in hai số tuyệt đối cạnh nhau + khoảng cách còn lại; gọi 75,73 là *"ước lượng thận trọng về
  năng lực của câu chuẩn, đo qua cùng dụng cụ"*.
- Chống lưng khi bị hỏi "60% thấp quá": trần 75,7 là giới hạn dụng cụ; thước chặt hơn quy ước lĩnh vực (câu phải
  đủ để một mô hình độc lập trỏ trúng) ⇒ **cấm so thẳng với 70–80% của bài khớp toạ độ trực tiếp**.
- BLEU-4 COCO (~50) khác BLEU-4 trung bình theo câu (~37,8) — hai tên khác nhau. CIDEr-D >100 vì một câu chuẩn/bước.

**Tả đúng dụng cụ** (đọc từ `harness/metric_exec.py`, từng tả sai ba chỗ):
- `hit_disk` là **hình chữ nhật** |dx|≤0,14·W ∧ |dy|≤0,14·H (dọc rộng gấp 2,2× ngang), không phải đĩa.
- Hạt Voronoi là **chính điểm chạm**, không phải tâm phần tử; `hit_voronoi` bao gồm `hit_disk` ⇒ là bản siết
  chặt, cấm trình như hai lựa chọn ngang hàng.
- `exec_disk` trong JSON của `score_run.py` là `hit_disk` **thuần**, không gated.
- Mẫu số **4.463** cho mọi nhánh (câu rỗng vào quần thể với exec = 0; "4.462 bước" ở file cũ không chính xác).
- `canon_action` cố tình giữ lỗi `go back` → tap (để các nhánh cũ tái lập); cờ `strict_back=True` cho lượt mới.
- Thước tất định: cùng chuỗi + cùng ảnh ⇒ cùng toạ độ (0 bất đồng trên 1.625 phép so).
- Bộ bơm lỗi không gọi bộ trỏ ⇒ hàng "paraphrase 0,0%" chỉ đo cổng chữ.

**Sàn và độ bền** (lát 800 trừ khi ghi khác):
- Sàn câu rỗng nghĩa **12,0** · câu thật của bước khác (sai màn) **6,1** (thấp hơn sàn ⇒ đòn thiên vị văn phong
  bị giết bằng số) · bỏ tên giữ vị trí −28,5 trên phần bị tác động vs bỏ vị trí giữ tên −3,5 ⇒ gọi tên đắt gấp
  8 lần. Dải dùng được 62,9.
- Diễn đạt lại câu chuẩn (đổi động từ, trật tự): 1.139 bước, +0,35 [−0,59; +1,29]. Viết *"bền trước việc đổi
  động từ và trật tự câu"*, **cấm** *"bền trước diễn đạt lại"*.
- Năm luật chấm: trần trôi 56,6 → 82,2 nhưng thứ tự nhánh không đổi. κ 0,867 toàn tập, 0,650 có điều kiện.
- Không lợi thế app đã thấy (59,1 vs 59,0; 55% bước không gán được app = *không biết*, cấm đọc thành *chưa thấy*).
- Thiên vị câu dài 5,4 điểm, nghiêng về Base ⇒ S1 > Base là kết luận mạnh.
- MDE ghép cặp ~2,1 (2,2 là bản làm tròn cũ của cùng đại lượng).

### ⛔ Số đã rút — cấm dùng lại

| số cũ | thật ra |
|---|---|
| trần 70,0% | 75,7% (đo đủ tập) |
| MIN-DESC 60,1 | 60,05 → làm tròn 60,0 |
| MDE 2,7–4,5 | ~2,1–2,2 |
| bộ trỏ trượt 84% khi đổi diễn đạt (Jandial) | 84% = năng suất của agent đối kháng trên desktop |
| "UGround sạch AndroidControl", "bộ trỏ khác họ" | SAI: Bảng 1 có AC 47K; UGround-V1-2B dựng trên Qwen2-VL |
| "tập kiểm tách rời split train ở mức màn hình" | SAI: 90% tác vụ tập kiểm thuộc split train chính thức (`report/209`); số đứng, câu phải sửa |
| trung vị sai số trỏ 8% cạnh | 15,0% / 29,3% (hàm cũ chỉ lấy ca đã trúng) |
| 604 bước app chưa thấy | 139 bước / 22 app |
| "12,6% có tên, đo trên 99.131 màn" | đo trên 120 màn ngẫu nhiên |
| `total_flos` 3.857.778.344 GF | 4.142.257.957 GF |
| `hit_disk` S2 67,5 · `action_ok` 94,9 · `hit_disk` ứng viên 66,4 | 67,4 · 94,8 · 66,3 |
| 89,6% nền của ba lát diễn đạt lại | chỉ của lát đổi trật tự; dải đúng 76,8–90,1 |
| 71,0% ô point S2 · phrase trùng 2,6% | bỏ khỏi bài (không truy được mẫu số) |
| bảng bơm lỗi n=250 | 250 bước × 4 góc = 1.000 lượt |

Danh sách đầy đủ + 24 lỗi đã bắt: `report/108`. ⛔ **Quét toàn kho sau mỗi lần rút số** (số sai từng sống trong
`.tex` nhiều ngày sau khi đã rút ở đây).

---

## 📦 DỮ LIỆU

- **Dạy:** 64.567 bước / 41.191 chạm / 12.895 tác vụ; `train_tru_val.jsonl` 63.000 bước (đã trừ val mở rộng
  `val_cham400` 400 chạm · `val_cham600` 602 chạm). Rò rỉ dạy ∩ kiểm = 0.
- **Kiểm:** 6.958 bước / 4.463 chạm / 1.432 tác vụ. ⚠️ 90% tác vụ thuộc split *train* chính thức của AC
  (`report/209`); exec tách theo split không chênh. Phần S1 chưa thấy: ACU 1.484 bước chạm (`runs/acu/`).
- `history` trong câu nhắc là **câu chuẩn** các bước trước ⇒ chấm teacher-forced trên ngữ cảnh.
- **Nguồn:** ghép `HarrytheOrange/parsed_AndroidControl` (câu người viết + cây trợ năng 99.131 màn) với
  `ckg/AndroidControlParsedWithImages-20k` (ảnh) theo `(episode_id, step_id)`. Bản `ckg` mất `step_instructions`
  ⇒ không dùng làm nguồn dạy. Cây trợ năng chỉ 12,6% phần tử có tên (120 màn) ⇒ chỉ dùng cho vị trí.
  TFRecord gốc: `reece124/android_control` (20 shard, 49,9 GB).
- `harness/dg1_cache/train_ac/`: chín jsonl đã commit; `ocr.jsonl` + ảnh ở Release `data-train-ac-v1`.
  `.gitignore` phải loại bằng `harness/dg1_cache/*` rồi mở từng tầng (loại cả thư mục thì dòng `!` vô hiệu).
- ⚠️ **Val là dữ liệu S1 và các nhánh từ S1 đã thấy** ⇒ lạc quan có hệ thống (val cao hơn test ~7,5 và phóng đại
  khoảng cách hai nhánh gần 40 lần). ⛔ **Không bao giờ trích số val ra báo**; val chỉ để xếp hạng trong một họ.
  Mẫu số exec của val là số bước **chạm**, không phải số bước.

---

## 🎓 TIỀN LỆ VÀ PHÂN ĐỊNH (tra tận nguồn — `report/114`)

1. **"Executability"** đã có ở *Open Grounded Planning* (ACL 2024, tr. 4982–5003) nhưng là tra bảng ký hiệu trên
   văn bản; của ta là hành vi + thị giác ⇒ giữ tên, có câu phân định ở lần dùng đầu.
2. **Zhao et al. EACL 2021:** BLEU/ROUGE/METEOR/CIDEr kém cho chỉ dẫn điều hướng (hậu thuẫn); nhưng xếp hạng hệ
   thống họ khuyên SPICE; họ có neo người, ta không.
3. **GCoT 2503.12799** vẫn là preprint (bài ICCV 2025 là 2507.02859, khác). −42,8 là số tự tính của prompting
   zero-shot; Table 5 cho thấy train grounding-trước thì **tăng** +4,5/+5,8 — đừng trích một nửa.
4. **Jandial et al., Findings of ACL: EACL 2026, tr. 2772–2785:** 84% là tỉ lệ thành công của agent đối kháng
   trên desktop Windows. Trích cho luận điểm "độ chính xác trên một câu tốt nhất thổi phồng năng lực". Bảng 1:
   UGround-V1-7B bền nhất trước diễn đạt khác (dự án dùng bản 2B — khai đúng biến thể).
5. ⛔ **Chữ cấm:** "đầu tiên"/"novel"/"cơ chế mới" cho thứ tự sinh hay cho đưa danh sách phần tử vào đầu vào (AC
   gốc đã dùng a11y làm input; dòng REG Mao CVPR16 · Luo CVPR17 · Yu CVPR17 đã có ý "câu đủ để bên kia trỏ đúng").
   Điểm phân định vững: AC dùng `step_instructions` làm **input**, ta dùng làm **đích sinh**.
6. Luật đọc: nhiều bài 2025–2026 mượn gói dữ liệu có AC (GTA1 ← OS-Atlas · SE-GUI ← UGround) ⇒ truy thêm một tầng.
   Agent tra cứu cũng phải kiểm như mọi nguồn: không tin ngay, không bỏ ngay.

## ⛔ GIỚI HẠN CÒN MỞ

- **Bộ trỏ không sạch:** UGround có AC 47K trong recipe và cùng họ Qwen với mô hình được chấm. Đòn "quen văn
  phong AC" đã đóng bằng UI-Venus (S1 − Base giữ 94%, ck500 − S1 giữ nguyên). Đòn "cùng họ Qwen" đóng phần lớn
  bằng Phi-4 (thứ tự nhánh giữ), chưa đóng hết. Không có neo người (đã quyết không chấm tay, user 6/9).
- Câu chữ: viết *"bộ trỏ không được huấn luyện trên AndroidControl"*, **cấm** *"chưa từng thấy màn hình di
  động"*; câu *"mọi bộ trỏ GUI mở đều dựng trên Qwen-VL"* là SAI (Phi-Ground dựng trên Phi-3.5-Vision).
- Bộ trỏ đã loại: GUI-G2-3B (trùng nền) · Jedi (có AC) · CogAgent · Aria-UI · SE-GUI/GUI-G1/GUI-R1/Holo1.
  Người nghe đã loại vì có AC/AITW: Molmo · InternVL2.5 · Magma · Phi-Ground; vì nền Qwen: InternVL3 · LLaVA-OV.
- ⭐ Mẫu hình: các lỗi bắt được đều ở **câu chữ mô tả** (tóm tắt một nguồn thành câu ngắn rồi câu ngắn sống nhiều
  tuần), không ở khâu đo ⇒ **trước khi một khẳng định vào bài, mở lại NGUỒN, không mở lại ghi chú**.

## 🔒 LỊCH SỬ NIÊM PHONG

`report/106` niêm 5/8 (`b93e85c`), mục sửa đổi ghi nối cuối file, không sửa đè. Khung "đăng ký trước" **đã gỡ
khỏi luận văn** (user 5/9, 14/9) nhưng hồ sơ giữ để tra. ⚠️ SHA mọi commit đổi ngày 21/8 khi viết lại lịch sử
(gỡ khoá API + zip lớn); niêm phong trước đó là `51ddb35`. Bảng ánh xạ ở `.git/filter-repo/commit-map` — **giữ tệp đó**.

---

## 📖 LUẬN VĂN VÀ SLIDE

- **Tên đề tài:** VI *"Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM từ các trường hợp sử dụng và
  giao diện người dùng"* · EN *"LLM-Based Automatic Generation of Software User Guides from Use Cases and
  Front-End Structures"*.
- `bang_nhieu_thuoc.tex` tự sinh bởi `harness/sinh_bang_nhieu_thuoc.py` (đừng sửa tay).
- Sửa luận văn xong thì **dựng lại `thesis/main.pdf`** và cắt lại `chuong_pdf`. Chỉ sửa đúng tài liệu được giao
  (đang làm bài báo thì không tự sửa `thesis/`).
- Bài báo (ch8 luận văn liệt kê VCL + SOICT): **VCL2026** được chấp nhận, hội thảo HUFLIT **27/11/2026** ·
  **SOICT 2026** GUIStep (EasyChair #5577), oral, camera-ready đã nộp, poster A0 + chủ toạ phiên hạn 23/11 ·
  **FAIR'2026** (EDAS #276) có deck `FAIR2026_SLIDE.pptx`. Chi tiết ở README từng bài và memory.
- Deck trong `slides/` (mỗi deck có `KICH_BAN_*.md` đi kèm, sinh từ `slides/build/`): thuyết trình
  `LUAN_VAN_SLIDE_THUYET_TRINH.pptx` · trình thầy `LUAN_VAN_SLIDE_TRINH_THAY_15_11.pptx` · VCL
  `VCL2026_SLIDE_15_11.pptx` · SOICT · FAIR. Deck cũ (bảo vệ 9/9, trình thầy 7/10, VCL 30/8, xin bảo vệ 22/10,
  Beamer) xoá 22/11, còn trong lịch sử git. Deck SOICT: script đọc lời nói từ `KICH_BAN_SOICT_15_11.md` (sửa
  kịch bản đó là đúng chỗ). Xem ảnh slide: PowerPoint qua COM từ `powershell.exe` (máy không có LibreOffice). Kịch bản sinh tự động thì sửa lời trong script rồi dựng lại, đừng sửa tay. Slide không xưng
  "em / thầy cô / hội đồng"; notes là gạch ý ngắn.

### ⛔ Lệnh dựng LaTeX

```
rm -f main.log && tectonic -X compile main.tex --outdir . --keep-logs
grep -oE "Output written on main\.xdv \([0-9]+ page" main.log   # số trang
grep -c Overfull main.log                                        # phải là 0
```
- Máy **không có `xelatex`**. **Không** `>/dev/null 2>&1` trên lệnh dựng; kiểm `ls -la main.pdf` mốc giờ trước khi
  tin số trang. Không `--keep-logs` thì `main.log` là bản cũ (suýt nộp bài quá trang).
- `main.pdf` bị khoá ghi khi user mở PDF (tectonic báo `Permission denied` sau `Writing ./main.pdf`) ⇒ dựng vào
  scratchpad để đọc số trang, nhắc user đóng trình đọc rồi dựng lại.
- Sửa chuỗi cùng độ dài thì PDF có thể ra đúng bằng byte cũ — không phải dựng hụt.
- **Không xuống dòng ngay sau gạch nối** trong nguồn TeX (ra `byte- identical`).

---

## ⚙️ VẬN HÀNH — bài học đã trả giá

⛔⛔ **Đồng hồ WSL chạy UTC, lệch 7 giờ.** Mọi mốc hạn đọc bằng `TZ='Asia/Ho_Chi_Minh' date` (từng lỡ một hạn nộp).

⛔ **Không khẳng định chắc chắn điều chưa kiểm.** Chưa kiểm thì nói *"tôi không chắc, để kiểm đã"*; gắn nhãn
[đo]/[suy]. Câu *"bấm Stop không ảnh hưởng train"* nói ra không kiểm và đã giết một lượt chạy.

**Lỗi câm — phép thử chưa hề diễn ra mà báo như đã diễn ra:**
- Bắt tiến trình **in ra cấu hình nó thật sự dùng** (`[dữ liệu] …`, `[nạp default] …`) rồi kiểm dòng đó; đọc mã
  chỉ chứng minh mã trên máy này. Dataset Kaggle có thể giữ bản mã cũ; bản vá trong `/kaggle/working` chỉ sống
  trong phiên.
- ⭐ Kết quả trùng nhau tới nhiều chữ số giữa các cấu hình KHÁC nhau là **dấu hiệu hỏng**.
- Phép kiểm dùng chính phép biến đổi nó cần phát hiện thì mù (`.strip()` che dấu cách cuối).
- Phép thử nối tiếp phải xin **nhiều hơn** số đã có (xin đúng số thì in `Xong sẵn`, không chứng minh gì).
- Resume adapter: transformers từng chỉ nạp thư mục con `ref/`, bỏ adapter `default` ⇒ policy về lại S1 mà không
  báo (cờ đỏ: KL tụt ~10 lần). Nạp adapter cũ rồi thêm module mới thì PEFT bỏ qua module mới trong im lặng.
- Trộn LoRA: trộn thẳng A với A, B với B là sai (ΔW là tích) ⇒ ghép nối theo hạng; kiểm hai đầu mút trên **câu**.
- ⛔ Đừng chạy `build_train_data.py --shards k` để lấy ảnh (ghi đè `train.jsonl`); `--shards` mặc định 1.

**Colab** (đơn vị trả trước, không có background execution):
1. `subprocess.Popen(..., start_new_session=True)` — thiếu thì bấm Stop ô bất kỳ gửi SIGINT sang train.
2. Không bấm Stop ô nào khi train chạy; cần ô khác thì notebook thứ hai hoặc Terminal Colab.
3. Ô theo dõi đọc log **local** `/content/train_*.log`; FUSE không cập nhật nội dung/mtime khi ghi thêm. Kiểm tệp
   đang ghi bằng `wc -l` hai lần cách 60 giây.
4. Phải có **một ô foreground** suốt lượt train, không thì ngắt vì rỗi ~90 phút.
5. `--out` trỏ thẳng vào Drive **không sống qua mất máy** ⇒ ghi local, chụp định kỳ sang tên khác bằng `cp`, so
   `wc -l` giữ bản dài hơn. Đồng bộ Drive mỗi 5 phút; `save_steps` nhỏ.
6. "Connecting / Not connected" trên trình duyệt chưa chắc là máy chết — kiểm PID, điểm lưu mới trên Drive.
7. Thư mục thăm dò cũ phải `rmtree` trước (không thì LLaMA-Factory chạy tiếp từ checkpoint cũ, log vẫn "completed").
8. `trainer_log.jsonl` khác trường theo stage (`dpo` không có `loss`/`lr`); số học lấy từ stdout. Sau resume,
   `train_loss`/`train_runtime`/`*_per_second` trong `all_results.json` sai — dùng `trainer_state.json`.
9. Notebook 2 GPU: `assert torch.cuda.device_count()==2` trước khâu sinh (một lượt từng treo >16 h không log).

**Kaggle** (30 h GPU/tuần/tài khoản, tối đa 2 phiên GPU cùng lúc, hạn mức làm mới 07:00 VN; CLI
`kg uyenle|trang|trang2|ca`, xem memory). `kernels logs` rỗng khi đang chạy; không có lệnh huỷ ngoài
`kernels delete` (mất log). trang2 không có dataset `thesis-score` ⇒ test chạy ở uyenle/trang.
- Log ngập (tqdm) làm treo commit 7 giờ ⇒ tắt thanh tiến trình, tiến trình con ghi ra tệp, nhịp sống mỗi 2 phút;
  không có nhịp sống sau 4 phút thì dừng.
- Mọi lệnh dài phải in tiến độ định kỳ, cấm `| tail`. Ô cuối zip riêng thư mục kết quả.
- Việc CPU dài đẩy lên Kaggle notebook CPU, không chạy máy nhà (SPICE cần dataset jar CoreNLP riêng).
- `score_run.py` không có cờ `--raw` (tự suy tên từ `--out`); `infer_branch.py`/`score_run.py` nhận
  `--data-root` + `--recs-file`, ghi dần và nối tiếp được, gộp số từ tệp thô.
- Image mới phải gỡ `torchao`. Lượt TRL tiền xử lý 128 ảnh/lô ăn ~9,8 GB RAM (chết -9).

**Tệp thô là tài sản:** giữ `*_raw.jsonl` thì đổi luật chấm không phải gọi lại bộ trỏ. Đo trần không cần GPU:
dựng preds với `pred = gold_instruction`.

### ⭐ THỦ TỤC CHỌN MÁY — bắt buộc trước MỌI lượt GPU (user chốt 5/9, siết 9/9)

User 9/9: *"cái nào chạy được bằng CPU thì ưu tiên CPU, chỉ cái nào cần dùng A100 thì mới dùng Colab A100, còn
cái nào dùng được L4 hay T4 thì vẫn phải ưu tiên dùng."*

**Bước 0:** phân rã lượt chạy thành từng **pha** (bung dữ liệu · mã hoá token · nạp model · train · lưu), gắn bậc
cho từng pha, tách pha CPU/IO ra khỏi phiên GPU đắt (VIS-SFT từng mã hoá token 2,5 h trên A100 với GPU 0%).

| bậc | máy | dùng khi |
|---|---|---|
| 0 | CPU (WSL / Kaggle CPU / Colab CPU) | không gọi GPU lần nào |
| 1 | Kaggle T4 ×2 (0 đồng) | suy luận, chấm, sequence-score, GRPO 3B đã chạy được |
| 2 | L4 (~22 GB) | đỉnh VRAM ≤ ~17 GB đo trên **mẫu nặng nhất** |
| 3 | A100 40 GB | bậc 2 tràn, hoặc chậm hơn > 1,5× |

- Probe trên card rẻ trước (`harness/runbook/chon_may.md`): đo `torch.cuda.max_memory_allocated()` trên mẫu dài
  nhất của nhánh nặng nhất (mẫu đầu tập không đủ) và s/bước.
- **Giờ L4 ≤ 1,5× giờ A100 thì chọn L4/T4.** So theo đơn vị mỗi lượt, không theo giá/giờ; VRAM dư không phải tiền phí.
- Giá GPU tra tại thời điểm quyết, cấm nhớ. Không đổi card giữa lượt. Bước tốn tiền phải hỏi trước, trình bảng
  **tiền · thời gian · ảnh hưởng độ chính xác**. (6/10 user nới: tiền Colab không thành vấn đề khi cần ra số,
  nhưng thứ tự bậc vẫn áp.)
- Cấu hình SFT cũ (P9): QLoRA 4-bit nhanh hơn bf16; bộ nhớ ngốn ở bảng logits (liger gộp CE giải được); tắt
  gradient checkpointing tràn ở chuỗi dài; mỗi biến thể chỉ đổi một thứ.

---

## 💻 Môi trường

Máy WSL2 **không GPU**. Python: `~/.venvs/thesis/bin/python`; chạy Python nhớ `PYTHONIOENCODING=utf-8`.
Train trên Colab/Kaggle, chấm trên Kaggle T4.
`.claude/` nằm trong `.gitignore` ⇒ skill **không có lịch sử git**, sửa lớn phải tự sao lưu. `CLAUDE.md` thắng mọi
skill khi mâu thuẫn (skill `soict-paper`, `vcl-fair-paper` mô tả giai đoạn cũ).

## ❓ CÒN TREO

- ⚠️ **Adapter ck500, ck500/202, sft_final, ra_k4 KHÔNG có Release** (repo public, chưa đẩy): mỗi cái còn đúng hai
  bản trên máy (bản gốc + một bản chép trong `tuantu/` · `nontap_kit_6_11/` · `colab_rl_test/` · `aitz_ace/`) — đừng
  xoá bản chép còn lại khi chưa có Release.
- Adapter S1/202 · S2/101 · CE2-S2 chỉ còn một bản ở `MyDrive/thesis/ckpt/<nhánh>/`. Drive đã dọn 11/10
  (`harness/runbook/colab_don_drive_11_10.md`); runbook cũ trỏ tới đường dẫn đã xoá sẽ báo thiếu tệp.
- Dọn repo 15/11 + 21/11 (chi tiết ở bản lưu trữ và memory `don-repo-15-11`). Luật user: **chỉ xoá đồ của hướng
  không ra số / chỉ ở phụ lục**; kiểm `git ls-files` + md5/Release trước `rm`; `find -delete` phá `-prune` ⇒ xoá
  theo danh sách đã kiểm. Đồ đã xoá lấy lại: `git checkout 24959e6^ -- <đường dẫn>` hoặc Release
  `stopped-fgrb-tage-v1`, `stopped-misc-v1`, `noisuy-adapters-v1`, `data-train-ac-v1`, `data-aitz-*`, `data-acu-build-v1`.
  Kit nào dựng dataset Kaggle từ thư mục `ds/` đã dọn phải chép lại ảnh từ `harness/dg1_cache` (jar CoreNLP:
  `_bundles/luoi/ds/`).
- Máy WSL không có `FINAL_SOLUTION.md` và `report/115` (ở checkout Mac) ⇒ tham chiếu trong `report/116` là chết.

---

## ✍️ Ghi chú làm việc cho trợ lý

- Trao đổi bằng **tiếng Việt**. Commit/push chỉ khi user cho phép trong chính prompt đó.
- **Văn phong:** từ tự nhiên, không lộ giọng AI. Cấm tự chế thuật ngữ rồi dùng như chuẩn ngành (từng mắc *"bản kê
  nút"*, *"bản thiết kế màn hình"* — tên thật là View Hierarchy). Tránh "Nói một câu:", "Điểm mấu chốt", "đáng nói
  nhất", "gói gọn", lạm dụng gạch ngang dài. Không dùng từ "khâu" (cả luận văn lẫn chat).
- **Yêu cầu kép:** dễ hiểu cho người không chuyên, đủ hàm lượng khoa học (công thức + trích dẫn đúng venue) cho
  một tiến sĩ AI khó tính: lời thường trước, hộp kỹ thuật sau.
- Chống trùng lắp khi thêm vào report; mỗi layer pitch → giải thích → công thức phải thêm thông tin.
- Citation chỉ trình peer-reviewed như đã bình duyệt; verify venue/năm trước khi trích. Tư vấn model/giá/API
  Claude: đọc tài liệu, không theo trí nhớ.
- Sau thay đổi lớn: cập nhật report tương ứng, `HUONG_DA_THU.md`, và file này khi có quyết định mới.

### ⭐ Soát giọng văn: tự chọn skill theo việc (user không gõ lệnh skill)

User chỉ nhờ bằng lời thường ("sửa cho tự nhiên", "bớt giọng AI", "soát slide", "humanize"…). Trợ lý tự
gọi skill bằng tool Skill theo bảng dưới, không chờ user gọi tên, và báo một dòng đã dùng skill nào.

| việc | skill |
|---|---|
| slide, ghi chú thuyết trình, kịch bản nói **tiếng Việt** (`slides/build/*.js`, `KICH_BAN_*.md`) | `viet-nhu-nguoi` |
| chương luận văn, report, văn xuôi **tiếng Việt** (`thesis/chapters/*.tex`, `report/*.md`) | `humanizer-vi`; câu dịch sát từ tiếng Anh thì thêm `translationese-cleaner-vi` |
| văn **tiếng Anh**: deck và kịch bản SOICT/FAIR, bài báo `paper/` | `humanizer` |
| email, tin nhắn tiếng Việt | `viet-nhu-nguoi` |

- Luật văn phong trong file này (mục dưới) và memory `van-phong-luan-van` **thắng skill** khi mâu thuẫn.
- Luôn giữ nguyên số liệu, KTC, tên nhánh, caveat; sau khi sửa so số trước/sau. Slide sinh từ script thì sửa
  script rồi dựng lại, không sửa tay `KICH_BAN_*.md` tự sinh.
- Script trong skill (`scan.py`, `check_facts.py`) bị chặn chạy ⇒ áp luật bằng tay, không xin lách.

### ⭐ Quy tắc văn phong luận văn (thắng cách gọi cũ trong ghi chú lịch sử)

Áp cho toàn bộ `thesis/chapters/*.tex` (memory `van-phong-luan-van` có bảng thay từ đầy đủ):
- ⛔ Không **"luận văn"** làm chủ ngữ (dùng "chúng tôi"/"đề tài"). Không "người viết": dùng **"câu chuẩn"**.
  Hạn chế "nó". Gỡ toàn bộ khung "đăng ký trước / khoá / niêm phong / cam kết / thăm dò"; "thăm dò" → "một hạt giống".
- ⛔ Không **"khớp chạm"** → "tiêu chí đánh giá / tiêu chí xác định vị trí / tiêu chí hộp phần tử / AitW đầy đủ".
  Không **"luật"** cho tiêu chí trong văn xuôi → "tiêu chí / cách đánh giá / cách xác định".
- ⛔ Không **"xáo"** → "điểm SPICE được ghép ngẫu nhiên giữa các mẫu". Không **"thước chữ"** → "độ đo dựa trên câu
  chuẩn / độ đo văn bản". Không **"luồng"** → "quy trình". Không "điều kiện đồng thuận" → "điều kiện lựa chọn".
  Ưu tiên "dữ liệu gốc"; tránh "rỗng" khi mô tả dữ liệu/câu.
- Thuật ngữ thống nhất: "đối chứng" → "nhánh so sánh" · "checkpoint" → "điểm lưu" · "cơ chế hỏng" → "dạng lỗi" ·
  "chỗ nghẽn" → "điểm nghẽn" · "quota" → "hạn mức máy" · "trượt" (không đạt tiêu chí) → "không đạt".
- ⛔ Bỏ dấu gạch dài `---` (khoảng số viết "a đến b"; ô trống bảng dùng `-`). Bỏ cụm ghép gạch nối kiểu Anh (chỉ
  giữ nơ-ron, mô-đun, ĐHQG-HCM).
- ⛔ Tiêu đề mục không dạng câu hỏi; không câu hỏi tu từ; không ẩn dụ thể thao/đời thường; không mở đầu lộ giọng
  máy ("Nói gọn:", "Nói cách khác", "Điều đáng nói", "đằng này"…); không nhịp câu lặp cấu trúc.
- Câu dài nhồi số phải tách; thuật ngữ nêu lần đầu giải thích ngay bằng lời thường.
- ⛔ Gỡ chi tiết mã khỏi thân bài (tên file, tham số, cờ). Được giữ vì tả dữ liệu: `<desc>`/`<point>`,
  `(episode_id, step_id)`, `step_instructions`, tên kho HuggingFace. Tên nhánh viết hoa (S1, S2…).
- ✅ In đậm **có chọn lọc** các con số kết quả quan trọng (thắng quy tắc cũ "không in đậm giữa câu"); không in đậm dày đặc.
- ✅ Caption hình/bảng ngắn. Chương 3, 4, 6 ưu tiên ngắn gọn; không bỏ số chính, KTC quan trọng, caveat cần thiết.
- ✅ Trước khi hoàn tất một vòng sửa, grep `thesis/chapters/` cho `khớp chạm`, `thước chữ`, `điều kiện đồng thuận`,
  `luồng`, và kiểm riêng chữ `luật` trong văn xuôi.
