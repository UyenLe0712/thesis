# 274 — Kết quả pilot TRIAD-T (action 273) — bản tình trạng 4/10/2026

> **Bản bàn giao 4/10 tối:** POA xong · POB đã qua lượt thử (TEST=True) và đang/sắp chạy commit Kaggle ·
> POC/P1 chưa chạy. Việc của phiên sau ở **§6b**.
> Đọc một mình là đủ, không cần mở log. Mọi số ở đây là số **val C1** (249 click), cấm trích ra báo.
> Action gốc: `harness/273_ACTION_PILOT_TRIAD_T_P0_P1_4_10.md`. Đường dẫn báo cáo trong action là máy Mac
> (`/Users/P836901/...`); máy WSL không có, nên báo cáo nằm ở đây.

## 0. Tóm tắt một đoạn

TRIAD-T là bộ chọn câu lúc suy luận: ck500 sinh câu greedy `d0` + 8 câu mẫu; listener độc lập (ShowUI-2B) trỏ
điểm cho từng câu; đổi `d0` sang câu mẫu chỉ khi hai locator (`loc_g`, `loc_d`) đồng ý và listener của câu mẫu
trỏ gần `loc_g`. **POA (ứng viên là mẫu S1 có sẵn) rơi vùng xám:** ShowUI là listener tốt (đọc toạ độ 100%,
tự trỏ trúng 79,5% với câu chuẩn) nhưng TRIAD-T đầy đủ chỉ được **net +1 (cứu 2, phá 1)** so với ck500 166/249,
UI-Venus +2. Bảng 177/249 trước đây chủ yếu do vòng tròn: thay UGround-listener bằng listener độc lập thì 5 ca
cứu còn 2. Theo luật §5.4, vùng xám được chạy POB; user chọn chạy (4/10). POB đang chạy trên Kaggle.

## 1. Kiểm toàn vẹn dữ liệu (§3.1) — ĐẠT cả năm mục

| mục | kỳ vọng | đo |
|---|---|---|
| key click `(episode_id, step_id)` ở mọi tệp dùng | 249 | 249 ở `c1_recs` (lọc click), `c1preds/k0…k8`, `c1score/score_k0…k8_raw`, `score_ck500_l4_raw`, `loc_val_g`, `loc_val_d` |
| S1 greedy (`score_k0_raw`) | 158 | 158 |
| ck500 L4 (`score_ck500_l4_raw`) | 166 | 166 |
| `loc_g` hit đĩa | 193 | 193 |
| `loc_d` hit đĩa | 190 | 190 |
| câu trong tệp chấm = câu trong tệp preds (k0…k8) | khớp | 249/249 mỗi tệp |

Mã kiểm: `harness/triad_t.py::nap_poa()` (assert, chạy mỗi lần đọc).

## 2. Cấu hình đã khoá (không đổi giữa POA và POB)

- **Luật chọn (§4)** — `harness/triad_t.py::chon()`. Toạ độ thang 0–1000 trên ảnh gốc, `near` = |Δx|≤r ∧ |Δy|≤r.
  Lọc ứng viên: rỗng · trùng nguyên văn `d0` · lặp bất thường (> 40 từ hoặc một bộ ba từ lặp ≥ 3 lần — khoá
  trước khi thấy số) · không phải câu chạm (`canon_action` ∉ {tap, long_press}) · listener không đọc được điểm.
  Hàm này không nhận câu chuẩn, điểm vàng hay `executable`.
- **Lưới:** `r ∈ {40, 60, 80, 100}`, `r_trust ∈ {80, 100, 140, 180}`. **Luật chọn cấu hình §5.3**: rescue>break →
  break ít → net lớn → coverage lớn → bán kính nhỏ (`triad_t.py::khoa_chon/chon_cau_hinh`).
- **Listener: ShowUI-2B** (`showlab/ShowUI-2B`, processor `Qwen/Qwen2-VL-2B-Instruct`, câu nhắc hệ thống bê nguyên
  thẻ mô hình, `min_pixels=256·28² = 200.704`, `max_pixels=1344·28² = 1.053.696`, **fp32** vì ShowUI fp16 trên T4
  từng ra NaN, giải mã greedy 32 token). Đầu ra `[x, y]` thang 0–1, đọc khi hai số đầu cùng trong [0,1], nhân 1000.
  Mã `harness/triad_listener.py`.
- **Evaluator:** UGround-V1-2B qua `score_run.py` (luật exec hiện hành, không đổi); UI-Venus-Ground-7B qua
  `score_run.py --grounder uivenus`, cỡ ảnh 1.272 token (`VENUS_MIN/MAX_PIXELS = 200704/1003520`, như phép B).
- **Mốc so:** ck500 greedy bản chấm L4 = 166/249 (UGround), 146/249 (UI-Venus, đo ở POA).

## 3. Listener độc lập (ShowUI-2B) — Kaggle T4, commit POA

| chỉ số | giá trị |
|---|---|
| số lời gọi (cặp bước–câu duy nhất) | 1.952 |
| đọc được toạ độ | **100%** (1.952/1.952) |
| hit_disk ±14% trên câu chuẩn (249) | **79,5%** (198) |
| hit_disk trên câu ck500 (249) | 72,3% (180) — UGround trên cùng câu: 73,9% (184) |
| ShowUI và UGround trỏ cùng chỗ (±140) trên câu ck500 | 222/249 |
| thời gian | trung vị 6,5 s/lời gọi (T4, fp32) |
| VRAM đỉnh | 9,34 GiB |

Câu chuẩn chỉ dùng cho dòng hit_disk này; bộ chọn không đọc.

## 4. POA — ứng viên = 8 mẫu S1 (T=1,0) có sẵn, d0 = ck500 greedy

UGround không chạy lại: mọi câu ứng viên đã được chấm trong lượt C1 exec8. Cứu/phá so với ck500 (166/249).
KTC95 bootstrap theo episode, 2.000 lần, seed 20261004.

### B1 — chọn theo `loc_g`, không cổng `loc_d`

| r | cov% | đổi | cứu | phá | net | exec | Δpp [KTC95] | UI-Venus Δ |
|---|---|---|---|---|---|---|---|---|
| 40 | 12,1 | 30 | 7 | 7 | +0 | 66,67 | +0,00 [−2,94; +2,90] | +0 |
| **60** ◀ | 11,7 | 29 | 8 | 5 | **+3** | 67,87 | +1,20 [−1,61; +4,03] | +1 |
| 80 | 12,4 | 31 | 10 | 6 | +4 | 68,27 | +1,61 [−1,64; +5,10] | +2 |
| 100 | 12,4 | 31 | 10 | 8 | +2 | 67,47 | +0,80 [−2,56; +4,56] | +2 |

(r=80 có net cao hơn nhưng luật §5.3 xếp "break ít" trước "net" ⇒ chọn r=60.)

### B2 — TRIAD-T đầy đủ (cổng `loc_g − loc_d`)

| r | r_trust | cov% | đổi | cứu | phá | net | exec | Δpp [KTC95] | UI-Venus Δ |
|---|---|---|---|---|---|---|---|---|---|
| 40 | 80 / 100 | 6,4 | 16 | 1 | 3 | −2 | 65,86 | −0,80 [−2,39; +0,78] | +1 |
| 40 | 140 / 180 | 6,8 | 17 | 1 | 4 | −3 | 65,46 | −1,20 [−2,90; +0,41] | +0 |
| 60 | 80 / 100 | 5,2 | 13 | 1 | 1 | +0 | 66,67 | +0,00 [−1,18; +1,20] | +1 |
| 60 | 140 / 180 | 5,6 | 14 | 1 | 2 | −1 | 66,27 | −0,40 [−1,73; +0,85] | +0 |
| **80** | **80** ◀ | 5,2 | 13 | 2 | 1 | **+1** | 67,07 | +0,40 [−0,82; +1,99] | **+2** |
| 80 | 100 | 5,2 | 13 | 2 | 1 | +1 | 67,07 | +0,40 [−0,82; +1,99] | +2 |
| 80 | 140 / 180 | 5,6 | 14 | 2 | 2 | +0 | 66,67 | +0,00 [−1,57; +1,64] | +1 |
| 100 | 80 / 100 | 4,8 | 12 | 2 | 2 | +0 | 66,67 | +0,00 [−1,53; +1,68] | +2 |
| 100 | 140 / 180 | 5,6 | 14 | 2 | 4 | −2 | 65,86 | −0,80 [−2,73; +1,20] | +1 |

(Các cặp r_trust gộp chung một hàng khi số trùng tuyệt đối.)

### B3 — đối chứng vòng tròn (UGround vừa chọn vừa chấm, chỉ chẩn đoán)

Tốt nhất theo luật: B1 r=60 net **+10** (cứu 13, phá 3, 176/249); B2 r=60 r_trust=180 net **+5** (cứu 5, phá 0,
171/249). Bảng §1.2 của action ghi 177/173; tái lập gần nhưng không trùng (khả năng do bán kính/luật lọc của phép
mô phỏng gốc khác). Tệp `runs/triad_t/b3_uground_vongtron.json`.

### Danh sách 13 bước B2 (r=80, r_trust=80) đổi câu

| bước | UGround ck500→chọn | câu ck500 → câu chọn | loc_g | vàng |
|---|---|---|---|---|
| (188, 8) | 0→1 | Click on search → Click on the ok button. | (500, 869) | (499, 802) |
| (589, 9) | 0→0 | Select the first four recent images → Click on the Import button at the bottom of t… | (500, 921) | (69, 416) |
| (1988, 2) | **1→0** | Set hours to 6 → Set 6 Hours | (500, 674) | (500, 675) |
| (2231, 1) | 1→1 | Click on the Import contacts from a .vcf opti… → With [Click on first option ] the Contacts wi… | (457, 206) | (340, 210) |
| (3308, 4) | 0→0 | Click on the first search result → Click on the first property at the top | (500, 370) | (500, 477) |
| (3652, 0) | 0→1 | Open the Industrybuing app → Click on the search bar on the top of the scr… | (452, 83) | (440, 87) |
| (4427, 4) | 0→0 | Click on the Edit button at the bottom of the… → Click on the edit icon at the bottom of the s… | (500, 930) | (231, 402) |
| (5105, 1) | 1→1 | Click on the Notification Bar option. → Click on the notification bar icon. | (479, 323) | (369, 337) |
| (8461, 2) | 0→0 | Set hours to 7 → Click on the 8 to make it 7 | (246, 323) | (259, 836) |
| (8873, 9) | 0→0 | Select the first option from the list → Click on the screen. | (473, 248) | (275, 254) |
| (14133, 1) | 1→1 | Select the podcasts option → Select the podcast option | (628, 447) | (722, 431) |
| (14437, 2) | 1→1 | Close the drawer → Close the pop up window | (941, 478) | (931, 472) |
| (15249, 7) | 1→1 | Click on the first image of the plant. → Select the first Image. | (135, 248) | (122, 260) |

Toạ độ listener/locator đầy đủ của từng bước: `runs/triad_t/poa_showui.json` → `doi_cau_B2`.

### Cổng POA (§5.4) — **VÙNG XÁM ("tín hiệu yếu")**

| điều kiện | ngưỡng đạt mạnh | đo (B2 chọn) | |
|---|---|---|---|
| parse | ≥ 98% | 100% | ✅ |
| hit_disk độc lập | ≥ 50% | 79,5% (câu chuẩn) · 72,3% (ck500) | ✅ |
| net B2 | ≥ +3 | **+1** | ❌ ⇒ vùng xám (+1/+2) |
| rescue/break | ≥ 2 hoặc break = 0 | 2/1 = 2 | ✅ |
| UI-Venus | không giảm quá 1 | +2 | ✅ |

Không trượt ⇒ không kích hoạt Phi-Ground. Lưu ý: +1 là cấu hình tốt nhất trong 16 ô lưới chọn trên chính 249 bước;
10/16 ô có net ≤ 0.

## 5. Chẩn đoán POA (sau khi thấy số — không dùng để đổi luật)

- **Oracle pool** (ck500 hoặc một trong 8 mẫu S1 được UGround chấm đúng): **197/249** (+31) ⇒ pool có headroom.
- **18 bước "cứu được"** (ck500 sai, `loc_g` trúng vàng ±14%, pool có câu đúng). ShowUI đặt một câu đúng gần
  `loc_g` (r=80) ở **17/18** ⇒ listener làm đúng phần mình. Số phận của 18 bước dưới B2 (80, 80):
  `locator_bat_dong` **9** · `d0_gan_t` **5** · `d0_khong_cham` 2 · đổi đúng **2**.
- **`d0_gan_t` = listener và evaluator bất đồng:** ShowUI đọc câu ck500 trúng chỗ, UGround đọc sai. Ví dụ (3315, 2)
  *"Open the Yummly app."*: ShowUI (250, 940) ≈ vàng (250, 943), UGround (500, 522). Đây không phải ca TRIAD-T sửa
  được: câu đúng, thước đọc sai. ShowUI và UGround lệch nhau ở 27/249 câu ck500 ⇒ trần của mọi bộ chọn dùng
  listener độc lập để tăng exec của UGround.
- Phân bố lý do toàn 249 bước (B2 80/80): `d0_gan_t` 179 · `locator_bat_dong` 39 · `A_rong` 14 · đổi 13 · `d0_khong_cham` 4.
- Cổng tin cậy chặn được phá (B1→B2: phá 5–8 → 1–4) nhưng chặn luôn 9/18 ca cứu.

## 6. POB — ĐANG CHẠY (commit Kaggle, user chọn 4/10)

Runbook `harness/kaggle_triad_pob.md`, dataset `triad-pob-script` (`_bundles/triad-pob-script/`, 12 tệp, md5 ở Ô 2).
Một commit T4 ×2, ước **5–6 h**:

1. hoà S1 → ck500 (`checkpoint-500`, md5 adapter `491fa667…`) sinh **8 mẫu/bước** trên 249 click ở **T=0,7 (GPU0)**
   và **T=1,0 (GPU1)** song song; `top_p=1`, `top_k=0`, `repetition_penalty=1`, `max_new_tokens=96`, không 4-bit;
   seed mỗi bước = 20261004 + chỉ số bước (tất định khi nối tiếp). GPU0 sinh lại greedy để kiểm khớp `pred_ck500`.
2. gom câu duy nhất khác greedy ở mỗi bước ⇒ ShowUI (chia đôi theo bước) + UGround (mọi câu, cần cho oracle C3 và
   mọi ô lưới; chấm theo "lớp" preds để không chấm trùng).
3. bộ chọn C2 trên từng nhiệt độ ⇒ UI-Venus chỉ chấm câu được C2 tốt nhất đổi (ck500 đã có 146 từ POA).
4. máy nhà: `python3 harness/triad_pob.py --bao-cao --dir runs/triad_t/pob/triad_pob_out --out runs/triad_t/pob_ket_qua.json`
   in đủ: đa dạng theo nhiệt độ, oracle C3, lưới C1/C2 kèm KTC và UI-Venus, danh sách bước đổi câu.

Phần CPU của pipeline đã chạy thử bằng dữ liệu giả (mẫu S1 thế chỗ mẫu ck500): ra lại **đúng tuyệt đối** B1/B2
của POA (net +3 / +1, UI-Venus +2, oracle 197).

**Cổng POB (§6.3), sẽ áp nguyên văn:** chọn nhiệt độ theo net C2 → break ít → UI-Venus → hoà thì T=0,7.
Đạt lên P1: UGround net ≥ +3 · rescue/break ≥ 1,5 và break ≤ 3 · UI-Venus Δ ≥ −1 · coverage 1–20% · oracle C3
≥ ck500 + 10 · không lỗi ngôn ngữ nghiêm trọng. Vùng xám (net +1/+2 hoặc UI-Venus −2): **dừng, hỏi user**. Trượt
(net ≤ 0, rescue ≤ break, UI-Venus ≤ −3, headroom < 10): dừng TRIAD-T. Đa dạng thấp (trung vị < 3 câu khác nhau /8)
⇒ được thử N=16 một lần ở nhiệt độ tốt hơn.

Kỳ vọng ghi trước khi có số POB [suy]: thấp. 9/18 ca cứu ở POA bị chặn bởi cổng locator, mà cổng đó không phụ
thuộc ứng viên; mẫu ck500 có thể ít đa dạng hơn mẫu S1.

### 6a. Lượt thử POB (TEST=True, 3 bước) — ĐẠT, 4/10

| kiểm | đo | đọc |
|---|---|---|
| hoà S1 → ck500 | fp16, nạp `checkpoint-500` | đúng |
| `[kiểm hoà ck500]` greedy sinh lại = `pred_ck500` | **3/3** | đường sinh khớp lượt chấm cũ |
| lấy mẫu T=0,7 (GPU0) · T=1,0 (GPU1) | 3/3 bước mỗi bên, mã thoát 0, ~13–17 s/bước | có đa dạng thật (cùng bước ra *"Select the Other electrical equipment category"* và *"…at the bottom of the screen"*) |
| `[lớp]` | 10 câu duy nhất khác greedy · 5 lớp UGround · 8 lời gọi listener mới (2 đã có từ POA) | khâu bỏ trùng với POA chạy |
| listener | 6/8 lời gọi (TEST cắt `--n 6`, đúng thiết kế) · đọc được 100% · ~6 s/lời gọi · VRAM 9,34 GiB | khớp POA |
| UGround | 4/4 câu (TEST chỉ lấy 2 lớp), có `lop00_raw`, `lop01_raw` | chạy |

`raw` của listener ra x = 0,5 ở cả mấy lời gọi thử: không phải lỗi — ở POA 682/1.952 điểm ShowUI (34,9%) có x = 500
(nút/dòng danh sách trải hết bề ngang màn), mà hai bước thử là nút "add to cart" và một dòng danh mục.
Đoạn log user dán bị cắt mất dòng `[cấu hình lấy mẫu]` và `dtype thật` của listener; đã nhờ user liếc lại trên
notebook (phải là `temperature 0.7/1.0 · top_k 0 · num_return_sequences 8` và `float32`) trước khi commit.

### 6b. Việc của phiên sau

1. **Commit Kaggle** (user làm): Ô 2 `TEST = False` → Stop session → Save Version → *Save & Run All (Commit)*.
   Ước **5–6 h** (dải 4,5–7 h). Nhịp sống mỗi 2 phút; quá ~5 phút không có dòng nào ⇒ xem log. Commit đứt giữa
   chừng: thêm Output của commit đó làm Input, Ô 2 tự chép phần đã chạy và làm tiếp.
2. Tải `triad_pob_out.zip` từ Output ⇒ giải nén vào `runs/triad_t/pob/` (luật CLAUDE.md: đặt thẳng vào thư mục phép đo).
3. Chạy `python3 harness/triad_pob.py --bao-cao --dir runs/triad_t/pob/triad_pob_out --out runs/triad_t/pob_ket_qua.json`.
4. Đọc cổng §6.3 **nguyên văn** (mục 6 ở trên), ghi kết quả vào báo cáo này (thêm §6c, sửa đầu file).
   - **Đạt** ⇒ POC: soạn 30 bước cho hai người chấm (user bố trí người).
   - **Vùng xám** ⇒ **dừng, hỏi user**, không tự chạy P1.
   - **Trượt** ⇒ dừng TRIAD-T, ghi kết quả âm.
   - **Đa dạng thấp** (trung vị < 3 câu khác /8) ⇒ được thử N=16 **một lần** ở nhiệt độ tốt hơn.
5. Ràng buộc còn hiệu lực (action §2/§12): UGround/UI-Venus chỉ làm evaluator · không train · không mở tập xác
   nhận 1.484 click · không đưa output editor TAGE vào pool · không dùng câu chuẩn/điểm vàng/kết quả chấm để chọn
   câu · mọi cấu hình đã thử vào bảng · không gọi P1 là test · không sửa luận văn.

Hạn mức Kaggle (4/10): nick hiện tại còn ~23 h trước commit POB (commit dự kiến ăn ~5–6 h); nick thứ hai còn ~30 h.

## 7. Chưa làm và vì sao

| pha | trạng thái |
|---|---|
| POC (kiểm người 30 bước) | chưa — chỉ khi POB đạt; cần hai người chấm (user bố trí) |
| P1 (dev 4.463 click, 5 fold) | chưa — chỉ khi POB **và** POC đạt; cần `loc_d` trên test (chưa có) |
| Phi-Ground | không chạy — POA không trượt |
| Tập xác nhận 1.484 click | không đụng (cấm trong lượt này) |

## 8. Thay đổi so với action 273

1. Listener gọi trên **cặp (bước, câu) duy nhất**: 1.952 lời gọi thay vì 2.241 (+249 câu chuẩn). Giải mã greedy
   tất định ⇒ không đổi số.
2. Thêm 249 câu chuẩn vào lời gọi listener, **chỉ** để đo hit_disk độc lập; bộ chọn không đọc.
3. POA: UI-Venus chấm **mọi** ứng viên (ck500 + k1…k8), không chỉ cấu hình thắng — để một commit là đủ.
   POB: chỉ chấm câu C2 tốt nhất đổi (đúng §6.2: "UI-Venus cho ck500 và hai cấu hình C2").
4. Mốc ck500 dùng bản chấm **L4** (166) như action; câu mẫu S1/ck500 chấm trên T4 fp16. Chấm L4 và T4 lệch ±1 bước
   (đã ghi ở `report/267`).
5. Ứng viên trùng nguyên văn `d0` bị loại khỏi tập A (đổi sang câu giống hệt không phải là đổi).
6. Định nghĩa "lặp bất thường" (> 40 từ hoặc bộ ba từ lặp ≥ 3) tự đặt, khoá trước khi chạy POA.
7. Báo cáo ghi ở `report/274_…` (WSL) thay vì đường dẫn Mac.

## 9. Tệp

| tệp | nội dung |
|---|---|
| `harness/triad_t.py` | luật chọn §4, lưới, §5.3, POA/B3 |
| `harness/triad_listener.py` | listener ShowUI-2B (nối tiếp được, `--shard`) |
| `harness/triad_pob.py` | POB: lấy mẫu ck500, lớp câu duy nhất, chọn, báo cáo |
| `harness/kaggle_triad_poa.md` · `harness/kaggle_triad_pob.md` | runbook commit |
| `runs/triad_t/poa/triad_poa_out/` | output commit POA (listener + UI-Venus raw) |
| `runs/triad_t/poa_showui.json` | bảng POA đầy đủ + bước đổi câu |
| `runs/triad_t/b3_uground_vongtron.json` | đối chứng vòng tròn |
| `runs/triad_t/calls_poa.jsonl` | 1.952 lời gọi listener POA |

| `_bundles/triad-t-script/` · `_bundles/triad-pob-script/` | nội dung hai dataset Kaggle |

Git: action §12 cấm commit/push trong lượt; **user yêu cầu push bản bàn giao 4/10** nên đã commit các tệp TRIAD ở
trên (không kèm các thay đổi luận văn/CLAUDE.md đang dở của phiên khác, không kèm `harness/triad_poa_out.zip` vì
đã giải nén vào `runs/triad_t/poa/`).
