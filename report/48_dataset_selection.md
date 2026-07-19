# TRÍCH XUẤT & CHỌN ITEM 3 BỘ DATASET (đa dạng nhất, đúng scope thạc sĩ)

> Làm trực tiếp trên dữ liệu 2026-07-06. Đã tải thêm/đối chiếu qua HuggingFace. Kèm debate kiểm định (§4).
> **⭐ FILE NÀY = NGUỒN-SỰ-THẬT chốt mẫu 3 bộ** (gộp 2026-07-06, thay `48_chon_mau_thi_nghiem.md` đã xoá).

---

## ★ CẬP NHẬT CHỐT CUỐI (2026-07-06, sau re-scan + debate 4 giám khảo)

**Nguồn AndroidControl — ĐÃ ĐỐI CHIẾU split thật (load_dataset_builder):**
- `smolagents/android-control`: **test=3.051 ep**, train=12.232 (tổng 15.283 = khớp official) — episode-level, có `screenshots_b64`+`actions`+`goal`. → **CHỌN NGUỒN NÀY.**
- `ckg/AndroidControlParsed-20k`: test=8.417 **step-row** (format SFT messages/tools), phải ráp lại + 52% gap → **BỎ** (chỉ hợp fine-tune).
- ⚠️ smolagents = **community re-split 80/20** (test 3.051 ≠ official held-out 1.542). Vô hại leakage vì luận văn **zero-shot** (không fine-tune AC) + không claim leaderboard — **khai provenance khi viết**.

**App-diversity — ĐÃ VÁ (re-scan `scan_androidcontrol.py` lấy app từ `goal`+`open_app` trên 1.600 ep):**
- Toàn scan: **430 app xác định** (open_app 570 + goal 374 + unknown 656).
- Mẫu 286 ep (`dg2_sample.py` seed=42 trên meta mới): **237 app, chỉ 1 unknown** (thay số cũ "169 app/42 unknown" ở §3–4 — **số 237 mới đúng**). Phân bố: 194 app 1-ep, 40 app 2-ep, 1 app 4-ep, 1 app 7-ep. Phân bố N = {4:107, 5:103, 6:76}.
- ⚠️ 194/237 app là **singleton (1 ep)** → G danh nghĩa cao nhưng nhiều cụm cỡ-1; báo G thật + N_eff, KHÔNG khoe "G=237 rất mạnh".

**Artifact chốt:** MobileViews `kept_screens_final.json` (127/30) · ScreenSpot `screenspot_mobile_v2.json` (501) · AndroidControl **`harness/dg2_episodes.json`** (286 core N∈{4,5,6}, 237 app) **+ `harness/dg2_episodes_Nlong.json`** (48 ep N∈{7,8,9,10}, 48 app — tầng N-dài báo đường-cong τ/N, vá lỗ "cắt N≥7"). *(File cũ `androidcontrol_selected.json` bỏ.)*
> **CÒN (free, trước khi chi API):** git-track 3 manifest + `report/22` làm timestamp pre-register (M3); verify zero-gap/schema trên chính 286+48 ep; MIN_ACT sensitivity {1,3,5,6} + bảng archetype/label-coverage (strata 55/38/45 đã có §1); freeze revision-hash 3 dataset.

**Debate 4 giám khảo (2026-07-06) TÁI XÁC NHẬN 3 lỗ CAO của §5/§7 (không mới, đã có kế hoạch vá):** MIN_ACT bias (CAO-3) · cắt N≥7 (thêm: bổ 1 tầng N-dài để báo đường-cong τ/N) · ScreenSpot lệch nền (iOS 238/Android 211 → chỉ 211 Android bảo chứng MobileViews) + vai grounding đã demote (chốt: trích số OS-Atlas công bố hoặc hạ khung "tham chiếu ngoài"). Framing bắt buộc: **estimand = macro-average mỗi-app-một-phiếu, CẤM chữ "đại diện app nói chung"**.

---

## 1. MobileViews (một màn) — ✅ ĐÃ CHỌN XONG

**Mở rộng thành công: 90 màn/18 app → 138 màn/30 app** (đạt điểm-ngọt R-09 "30+ app").
- Tải thêm 12 app mới từ shard `MobileViews_0-150000.parquet` (streaming, không tải 40GB), lọc `MIN_ACT≥6`, `MAX_PER_APP=5`.
- Ghi `harness/kept_screens.json` (138 tên màn + hồ sơ đa dạng từng màn).

**Độ đa dạng (đã đo từ VH thật):**
- **Độ-phủ-nhãn trải rộng:** 55 màn *thấp* (<0.5) · 38 *trung* · 45 *cao* (>0.8). Màn phủ-thấp (đặc biệt `mxcomminisoapp` 0.11 — gần như toàn icon) là **ca quý để test xử lý nút icon-only** (M4).
- **55 màn có form** (ô nhập) · **126 màn cuộn được**.
- **Nút-có-nhãn/màn:** min 5 · median 10.5 · max 280.
- **30 miền app khác nhau:** chạy bộ, tuyển việc, game, ảnh, marathon, thermostat, webtoon, dọn-dẹp, livestream, matrimony, fitness, tin-tức, grocery (ocado), công-cụ-hệ-thống, từ-điển, đám-cưới, kế-toán (xero), bán-lẻ (miniso)…

**CHỐT MobileViews (sau dedup — đúng ý debate):** chạy dedup theo **chữ-ký-cấu-trúc-VH** (tập nhãn actionable + activity) → phát hiện **8 nhóm gần-trùng, 11 màn thừa** → **giữ 127 màn DUY NHẤT / 30 app**. Danh sách chốt: `harness/kept_screens_final.json`. Đây là **n-hiệu-dụng** thật (127, không phải 138) — báo đúng con số này.

## 2. ScreenSpot-v2 (đối chứng grounding) — ✅ ĐÃ LẤY METADATA

- Tải `screenspot_mobile_v2.json` (annotation, nhẹ) → `dataset_samples/screenspot_full/`. **501 item mobile.**
- **Đa dạng sẵn (đã đo):** data_type: **icon 211 / text 290**; data_source: **ios 238 / android 211 / shop 52**. Cross đều.
- **CHỐT:** dùng **trọn 501 item** (đây là chuẩn, không subsample). Ảnh (`screenspotv2_image.zip`) tải sau khi chạy E15.

## 3. AndroidControl (nhiều màn) — ✅ CỔNG KN GO (đã đính chính)

**Bản parsed `ckg/AndroidControlParsed-20k` — load ĐẦY ĐỦ (75.746 step-row → 14.417 episode), đếm N = max(step_id)+1.**

> ⚠️ *Bài học nhỏ:* lần đầu tôi *stream một phần* (16k row) → episode bị cắt ngang → histogram N=1-nhiều **SAI (artifact)**. Load đầy đủ mới ra đúng.

**Histogram độ dài N (cổng KN — kết quả THẬT):**
| N | #episode | | N | #episode |
|---|---|---|---|---|
| 1 | 388 | | 7 | 1444 |
| 2 | 1268 | | 8 | 993 |
| 3 | 1532 | | 9 | 686 |
| 4 | 2028 | | 10 | 497 |
| 5 | 2223 | | 11–13 | 781 |
| 6 | 1874 | | ≥14 | ~600 |

- **N: median 5 · mean 6.2 · p95 13 · max 92** → **KHỚP con số chính thức paper** (mean 5.5, p95 13). Mirror HF **đáng tin**.
- **≥30 episode cho MỌI mốc N tới ~20** → thoải mái phân tầng.
- **12.761 episode có N≥3** (dư cho nhánh sắp-thứ-tự).
- **Đa dạng app:** ~**884 app** (Drive, Gmail, Amazon, Recorder, Duolingo, Nike, Adidas, Maps, Notes, Etsy…).

**⚠️ NHƯNG (kiểm sâu + debate bắt) — mirror parsed KHÔNG dùng được cho DG2:**
- **Chỉ 47.9% episode LIÊN TỤC** (step 0..n-1 đủ); **52% có GAP** (thiếu step giữa chừng). Episode thiếu màn → **suy cặp-bắt-buộc nhân-quả SAI → τ chấm trên gold HỎNG**.
- **Không có field app/package** trong mirror này → không khoá-cluster-theo-app bằng metadata được (con số "884 app" tôi ước từ instruction là **SAI** — AndroidControl chỉ có 833 app tổng; parse-từ-câu-lệnh over-split).

**✅ ĐÃ TÌM ĐƯỢC NGUỒN SẠCH (thay mirror hỏng): `smolagents/android-control`, split `test`.**
- Mỗi row = **một episode ĐẦY ĐỦ** (`screenshots_b64` + `actions` + `step_instructions`) → **không có gap**.
- **N khớp paper:** median 5, mean 5.5, max 17 (mẫu 61 ep test).
- **CÓ field `app_name`** trong action `open_app` → **khoá-cluster-theo-app bằng METADATA** (giải quyết CAO-2, không parse instruction nữa).
- **7 loại action:** click, scroll, input_text, wait, navigate_back, open_app, navigate_home → đa dạng.

**✅ CHỐT AndroidControl: 286 episode / 169 app** (`harness/androidcontrol_selected.json`).
- Scan 700 episode test (metadata, không ảnh) → chọn phân tầng.
- **Theo N-bin:** N=2:14 · N=3:27 · **N=4:55 · N=5:46 · N=6:41** (τ-set lõi, ≥30 ✓) · N=7:19 · N=8:29 · **N≥9:55**.
- **169 app phân biệt** (+42 unknown) → **G=169 cụm** → cluster-bootstrap-theo-app **rất mạnh** (vượt xa ngưỡng 42; gỡ hẳn lo "ít-cụm").
- **8 loại action phủ đủ:** click, open_app, input_text, wait, scroll, navigate_back/home, long_press.
- Ảnh tải sau cho 286 episode này (khi chạy E8/E14). Cổng KN: **GO**.
- *Đuôi N=7,8 hơi mỏng (<30) — có thể scan thêm test set để lấp nếu cần ≥30 mọi mốc; core N∈{4,5,6} đã đủ.*

## 4. TỔNG HỢP SỐ LƯỢNG CHỐT (scope thạc sĩ, hiệu-quả-trước)

| Bộ | Chọn | Trạng thái |
|---|---|---|
| MobileViews | **127 màn duy nhất / 30 app** (sau dedup) | ✅ `kept_screens_final.json` |
| ScreenSpot-v2 | **501 item mobile** | ✅ annotation local, ảnh tải sau |
| AndroidControl | **286 ep / 169 app** (N∈{4,5,6} ≥41; N≥9:55) | ✅ `androidcontrol_selected.json`; nguồn sạch smolagents; G=169 |

---

## 5. KẾT QUẢ DEBATE KIỂM ĐỊNH (`wf_4ebb6d96-04c`) — 3 lỗi CAO phải vá

**Phán quyết:** cách chọn "sửa-là-ổn cho exploratory thạc sĩ", NHƯNG có **3 lỗi CAO phải vá TRƯỚC KHI CHẠY**:

- **🔴 CAO-1 (AndroidControl):** mirror parsed 52% episode có gap + không app-field → **bỏ mirror, dùng official test-split**, verify liên tục + cổng KN + khoá-cluster từ metadata official. *(Kiểm này đã xác nhận đúng.)*
- **🔴 CAO-2 (khoá cluster):** KHÔNG parse app từ instruction (over-split, "884">833 bất khả) → dùng package-id official.
- **🔴 CAO-3 (MobileViews filter bias):** `MIN_ACT≥6` + first-5-stream (không seed) + loại icon-only → tỉ-lệ-bịa GIẢM giả tạo. **Vá:**
  1. **KHÔNG headline "¼" tĩnh** → báo faithfulness **phân tầng theo 3 mốc độ-phủ-nhãn** (55/38/45) = *mechanism-check* (phủ↓ ⇒ bịa↑), mạnh hơn "¼".
  2. Thêm **tầng màn THƯA** (MIN_ACT~3) làm sensitivity.
  3. **Random-có-seed** thay first-5 (báo seed).
  4. **Pre-register** tiêu chí lọc + ngưỡng τ (git commit) TRƯỚC khi tính; báo **selection-rate** + profile màn bị loại (Threats-to-Validity).
  5. **KHÔNG gọi "toàn bộ/full"** → "mẫu phân tầng 138 màn rút từ MobileViews-public bằng tiêu chí pre-registered".

**Trung-bình cần khai:**
- **Thống kê:** G=30 vẫn < ngưỡng 42 → khai "ít-cụm bớt nhưng chưa an toàn"; báo **N_eff (~55–80) cạnh 138**, ICC/DEFF; wild-cluster-t null-imposed; **power/MDE tiên nghiệm** + thiết kế **ghép-cặp within-item** (pipeline vs baseline trên cùng màn) để khử variance.
- **Đa dạng:** **tiếng Việt = 0** (99.97% EN) → khai thẳng "headline = tiếng Anh mobile" (VN = định tính ~120 mẫu, KHÔNG bảng số VN); thiên-lệch-bot (vắng login/payment) → thu hẹp scope-claim; **dedup** perceptual-hash + VH-hash → báo n-hiệu-dụng.
- **N=1:** τ dùng **N≥2**; Step-SR **giữ N=1** (đa số tác vụ thật ngắn; loại đi → under-state). Báo 2 lớp AndroidControl: lớp-chuẩn (random-500 Step-SR, protocol Li 2024) + lớp-phân-tích (N-stratified τ + baseline shuffle).

**⚠️ PHẢI TỰ VERIFY (mâu thuẫn citation):** test-split official = **2.855** hay **1.542** episode? Debate thấy xung đột; `report/44` §8 + CLAUDE.md đang ghi 1.542. → **mở arXiv 2406.03679 đối chiếu tay** trước khi in (khả năng 2.855 = #episode test, 1.5xx = subset step-level bài khác trích).

## 6. CHECKLIST CỔNG CỨNG TRƯỚC KHI CHẠY (từ debate §4)
1. AndroidControl: dựng lại từ official + verify liên tục + cổng KN (không khớp → DỪNG).
2. Đối chiếu N official 2.855 vs 1.542 → sửa report/44 + CLAUDE.md.
3. Khoá cluster AndroidControl = app-id official.
4. MobileViews: pre-register MIN_ACT/MAX_PER_APP/ngưỡng + seed cố định.
5. MobileViews: sensitivity trên pool chưa lọc + selection-rate + dedup → n-hiệu-dụng.
6. Power/MDE tiên nghiệm; nếu CI vẫn chạm 0 → **tăng SỐ APP** (đòn bẩy mạnh nhất) hoặc hạ claim.
7. Lấy dữ liệu từ TEST-SPLIT official cả hai nhánh.

---

*File dữ liệu: `harness/kept_screens.json` (MobileViews 138/30) · `dataset_samples/screenspot_full/` (ScreenSpot 501) · script `harness/fetch_mv_expand.py`. AndroidControl: CHƯA lấy (mirror parsed loại; cần official).*

---

## 7. DEBATE LẦN 2 — PHÁN QUYẾT CHỐT (`wf_ebb4fbaf-dbb`, 6 lăng kính)

### ✅ CHỐT-CÓ-ĐIỀU-KIỆN — không có lỗi thiết kế, KHÔNG cần chọn lại mẫu. Giữ 127/501/286.
5/6 phản biện đồng thuận. 3 lỗi CAO lần 1 **đã vá đúng hướng** (mirror→smolagents; cluster→app_name; dedup→127).

### GATE CỨNG duy nhất (thủ tục ~10 phút, làm TRƯỚC khi chi API):
- **Freeze manifest** (127 screen_id + 501 ScreenSpot item + 286 episode_id) ra JSON + **`git init` + commit cùng report/22** (pre-register M3). Không có manifest cố định = không tái tạo được = chưa gọi là "chốt".

### PHẢI LÀM ĐỂ CHỐT (offline/free, trước API):
1. Freeze manifest + git commit (gate cứng trên) + seed cố định.
2. **Verify zero-gap/schema trên chính 286 ep** (mỗi ep: #screenshot khớp #step · có gold action · có a11y tree) — không suy từ tổng thể.
3. **Xử lý 42 unknown-app:** phục hồi app từ `packageName` trong a11y tree (free); nếu không → loại khỏi cluster HOẶC coi singleton + sensitivity. **KHÔNG gộp thành 1 siêu-cụm** (phá giả định wild-cluster-t). Báo lại G thật.
4. **Quyết N=7(19)/N=8(29) <30:** top-up từ 700 đã scan cho đủ ≥30, HOẶC gộp tầng N≥7, HOẶC đánh dấu exploratory (không kết luận per-N). Pre-register TRƯỚC khi nhìn kết quả.
5. **Sửa/khai MIN_ACT bias (nguy hiểm nhất):** MIN_ACT≥6 đếm CHỈ nút-có-nhãn → chọn thẳng trên tử-số coverage M4 dùng → làm nhẹ tỉ-lệ-bịa. Hoặc đếm mọi nút actionable rồi lọc, hoặc **bắt buộc báo phân-phối coverage mẫu-lọc vs không-lọc + khai "¼ = có điều kiện màn-dày-nhãn"**.
6. Verify prefix→package 1:1 cho 30 app (đề phòng va-chạm khoá 20-ký-tự).

### KHAI KHI VIẾT (không cản chạy):
- Provenance: "smolagents = **re-split qua HF, KHÔNG phải test-split official held-out**" (nhưng luận văn **zero-shot, không fine-tune trên AndroidControl** → re-split VÔ HẠI về leakage — nêu rõ lá chắn này).
- Limitations: bot-reachability (thiếu login/checkout/post-auth) · MIN_ACT dense-label bias · EN-only VN=0 · ScreenSpot mobile-only. Nối Chen ICSE20.
- Bảng **selection-funnel** (nguồn→lọc→loại→mẫu cuối) cho cả 3 bộ.
- Thống kê: wild-cluster-bootstrap-t là suy-luận CHÍNH; đo ICC pilot → **N_eff thật** (m̄≈4,23; ρ=0,3→N_eff≈64); per-N {2,3,7,8}=minh-hoạ, dùng **mixed-model trend** (N liên-tục + random-effect app) trên trọn 286; thiết-kế-cặp within-screen (BASE vs PA2 cùng màn); nếu CI chạm 0 → lùi "no-harm".

### CITATION 2.855 vs 1.542 — kết luận được HƯỚNG, còn đếm-tay chữ số cuối:
- **KHÔNG in 2.855 làm kích thước test.** 2.855 = tổng 4 sub-split CHỒNG NHAU (IDD 721 + app-unseen 631 + task-unseen 803 + cat-unseen 700; paper ghi "may overlap"). Duy nhất sau khử trùng ≈ **1.540**.
- Mâu thuẫn nhỏ 1.540 vs 1.542 (2 ep) → **đếm-tay episode_id duy nhất** trước khi in.
- **An toàn khi viết:** *"Test-split gồm 4 sub-split chồng nhau, tổng 2.855; số duy nhất sau khử trùng ≈1.540 (Li et al. NeurIPS 2024 D&B, Table 3); 286 = mẫu phân-tầng con."* KHÔNG in "1.542" như trích nguyên văn.
