# CHƯƠNG: DỮ LIỆU SỬ DỤNG — bản chi tiết chuẩn luận văn (số liệu đã verify tận file)

> Bản giới thiệu 3 bộ dữ liệu ở mức luận văn: nguồn gốc, trạng thái bình duyệt, quy mô, cách thu thập,
> cấu trúc mẫu, ví dụ THẬT, vai trò, hạn chế. Số liệu đã kiểm qua web + đối chiếu file thật trong
> `dataset_samples/`. Deliverable từ workflow deep-research + debate `wf_6d07419b` (2026-07-03).
> ⚠ = điểm cần chốt/kiểm trước khi in bản cuối (tổng hợp ở cuối chương).

---

## 1. Vì sao cần ba bộ dữ liệu và cách phân vai

Luận văn giải bài toán **sinh hướng dẫn sử dụng phần mềm từ ảnh giao diện và câu hỏi use-case, đánh giá mà không có bộ hướng dẫn mẫu do người soạn** (no-gold). Không tồn tại một bộ "ảnh giao diện → hướng dẫn chuẩn cho người đọc" để làm đáp án. Vì vậy dùng **ba bộ với vai cố định, tách nhau theo một trục duy nhất: CÓ hay KHÔNG có *quỹ đạo vàng*** (chuỗi thao tác đúng từng bước, có sẵn để làm mốc chấm).

- **Nhánh KHÔNG có quỹ đạo vàng (một màn):** một ảnh + *bảng kê phần tử* (View Hierarchy). Đo khả năng **bám sát màn** — mô hình có "bịa" nút không tồn tại không → **MobileViews**.
- **Nhánh CÓ quỹ đạo vàng (nhiều màn):** chuỗi nhiều màn, mỗi bước có thao tác đúng do người thật làm. Đo **con số năng lực thật** (sắp đúng thứ tự + đúng thao tác — Step-SR) → **AndroidControl**.
- **Đối chứng grounding:** ảnh + hộp bao (bbox) chuẩn đã hiệu đính, kiểm bộ trỏ (x,y) **độc lập** → **ScreenSpot-v2**.

Ba bộ **không đồng nhất nguồn gốc là chủ ý**: bổ sung nhau đúng theo trục trên. Minh bạch ngay từ đầu: **cả ba vốn xây cho mục đích khác** (huấn luyện/đánh giá *tác tử bấm máy* và đo *grounding*), **không bộ nào thiết kế để sinh hướng dẫn cho người**. Luận văn **dùng lại có kiểm soát (repurpose)**: chỉ *mượn* View Hierarchy để đối chiếu khớp/bịa, *mượn* quỹ đạo vàng + bbox làm **tham chiếu chấm**, và **không claim ngang leaderboard tác tử**. Tái dùng dữ liệu khác mục đích gốc là chuẩn mực đã có tiền lệ (G-Eval, FActScore, ALOHa).

---

## 2. MobileViews — bộ MỘT MÀN (ảnh + View Hierarchy)

### 2.1. Nguồn gốc và trạng thái bình duyệt
**MobileViews** (Gao và cộng sự) là **preprint arXiv, CHƯA bình duyệt** — `arXiv:2409.14337` (cs.HC). Không tìm thấy dấu hiệu công bố hội nghị/tạp chí. Trong luận văn luôn trích là **"preprint arXiv"**, đóng vai *hiện vật kỹ thuật* (cung cấp ảnh + bảng kê nút), **không** làm chỗ dựa cho claim phương pháp.

Khai thẳng đặc điểm **đổi tiêu đề + đổi con số theo phiên bản** (chứng tỏ đọc kỹ):
- v1 (22/09/2024), v2 (26/09/2024): *"MobileViews: A **Large-Scale** Mobile GUI Dataset"*.
- v3 (25/11/2025): *"MobileViews: A **Million-scale** and Diverse Mobile GUI Dataset"*.

Cơ quan đã xác minh: **BUPT** và **AIR, Tsinghua University** (Yuanchun Li). ⚠ *Có tin 3 đồng tác giả thuộc Xiaomi/MiLM nhưng không tự xác nhận được — **không khẳng định** trong luận văn.*

### 2.2. Quy mô (nêu rõ mâu thuẫn paper vs bản công khai)
- **Theo bài báo (v3):** hơn **1.200.000** cặp ảnh–VH duy nhất, hơn **30.000** app.
- **Bản phát hành công khai (HuggingFace `mllmTeam/MobileViews`):** là **"MobileViews-600K"** — hơn **600.000** cặp, hơn **20.000** app Google Play (chia dải ID 0–150K, 150K–291K, 300K–400K, 400K–522K; parquet + zip + index CSV).

→ Con số 1,2 triệu là của paper; con số **tải về thực tế** là **~600K**. Luận văn **không khoe "triệu-scale"**: dùng **tập con 600K**, và **thí nghiệm thực tế chỉ dùng 81 màn / 17 app** (mục 5).

### 2.3. Cách thu thập
**Tự động, gần như không có người:** 2 cụm SoC di động cung cấp **200+ môi trường Android "native"** chạy song song; khung **duyệt app tự động tăng cường bằng VLM** (dựa DroidBot tối ưu) tự bấm/duyệt sinh chuỗi tương tác. View Hierarchy bắt qua **Android Accessibility Service** (JSON) + **ADB/uiautomator** (XML). **Khử trùng toàn cục theo image-hash**.

### 2.4. Cấu trúc mỗi mẫu (đối chiếu file thật)
Mỗi mẫu = **1 ảnh `.jpg`** + **1 file `.viewhierarchy.json`**. Đối chiếu file thật `mv_multiapp/*_s1.viewhierarchy.json`:
- **Cấp cao:** `tag, state_str, foreground_activity, activity_stack, background_services, width, height, views`.
- **Mỗi node trong `views`:** `class` *(loại widget — **tên trường là `class`, KHÔNG phải `viewClass`**)*, `text`, `content_description`, `resource_id`, `clickable`, `editable`, `checkable`, `focusable`, `scrollable`, `long_clickable`, `enabled`, `visible`, `child_count`, `children`, `bounds`, `bound_box`, `signature`...
- **Toạ độ `bounds` dạng LỒNG NHAU** `[[x1,y1],[x2,y2]]` (pixel), **không** phải `[x1,y1,x2,y2]` phẳng.

> ⚠ **Bẫy toạ độ (rủi ro kỹ thuật lớn nhất):** trong file thật, trường cấp cao ghi `width=2340, height=1080` nhưng ảnh `.jpg` là **1080×2340 (dọc)** — hai trường **không khớp hướng ảnh**; biên `bounds` chạy tới `y≈1920` (nhỏ hơn 2340) và có giá trị âm/tràn. Vì luận văn tính **point-in-bbox**, **khung toạ độ phải hiệu chỉnh theo từng file** (đối chiếu kích thước ảnh thật) trước khi tính, nếu không metric grounding vô hiệu.

### 2.5. Ví dụ mẫu THẬT
Một node clickable trong app `cc.pacer.androidapp` (rút gọn):
```json
{ "temp_id": 27, "class": "android.widget.TextView", "text": "Following",
  "clickable": true, "enabled": true, "visible": true,
  "bounds": [[113, 216], [310, 336]], "size": "197*120" }
```
Đọc: nhãn chữ "Following" bấm được, hộp (113,216)→(310,336). Khi mô hình nhắc một nút, thuật toán so-embedding đối chiếu tên đó với tập node như trên: khớp (≥ ngưỡng) thì giữ, không khớp thì coi là "bịa" và viết lại thành mô tả.

### 2.6. Vai trò
Bộ **một màn (không-gold)**: cung cấp ảnh để mô hình sinh "mù" + **View Hierarchy để đối chiếu khớp/bịa**. **Không có quỹ đạo vàng.** Giấy phép **MIT**, ngôn ngữ **English**.

### 2.7. Hạn chế + cách xử lý
1. **Preprint** → đóng khung hiện vật kỹ thuật; bù tín nhiệm bằng AndroidControl (NeurIPS24) + ScreenSpot-v2 (ICLR25).
2. **Mâu thuẫn 1,2M vs 600K** → khai version, dùng bản 600K, chỉ 81 màn.
3. **VH sinh tự động → thiếu/nhiễu nhãn** (>77% app thiếu nhãn a11y, Chen ICSE 2020) → **hậu-kiểm + fallback**, loại node nhãn-chung, ⚠ *báo độ-phủ-nhãn thật (chưa tính — việc free đang chờ)*.
4. **Không quỹ đạo vàng** → chỉ nhánh một-màn.
5. **Duyệt bằng bot** → vài trạng thái không phản ánh luồng người-thật.
6. **Chỉ EN, không app VN.**

---

## 3. AndroidControl — bộ NHIỀU MÀN (quỹ đạo vàng người-thật)

### 3.1. Nguồn gốc và trạng thái bình duyệt
**AndroidControl** thuộc bài *"On the Effects of Data Scale on UI Control Agents"* (Li và cộng sự, **Google DeepMind**), `arXiv:2406.03679`, **NeurIPS 2024 — Datasets & Benchmarks Track — ĐÃ bình duyệt** (có slides trên neurips.cc). *(Bản arXiv v1 tên "…Computer Control Agents"; bản NeurIPS đổi "…UI Control Agents" — cùng bài.)* Trích: **Li et al., 2024**.

### 3.2. Quy mô (đã verify chắc)
- **15.283** episode · **14.548** task duy nhất · **833** app · **40** category.
- Độ dài episode: **trung bình 5,5 bước**; phân vị **p5–p95 = 1–13**.
- **Train:** 13.604 episode / 74.722 bước; **val:** 137 episode / 690 bước.
> ⚠ **Bảng split — KHÔNG in số test "2.855"** (số đó sai ở mức episode). Test đúng = 15.283 − 13.604 − 137 = **1.542 episode**. Chỉ in số đã verify chắc; đối chiếu Bảng thống kê PDF gốc nếu cần in bảng split đầy đủ.

### 3.3. Cách thu thập
**Người thao tác thật trên thiết bị vật lý:** điện thoại **Google Pixel** (Android 8.0+), điều khiển qua web bằng **WebUSB + ADB**. Kéo dài **~1 năm**, khoảng **20 annotator** được đào tạo nhiều tuần (nhà thầu trả công theo mức lương chuẩn). Vì là quỹ đạo người-thật, **"gold action" mỗi bước là thao tác đúng do người thực hiện** — chính là mốc chấm.

### 3.4. Cấu trúc mỗi mẫu
Đặc tả gốc: mỗi bước gồm **mục tiêu mức cao** (goal), **chỉ dẫn mức thấp** (step instruction), **screenshot**, **accessibility tree** (nguồn phần tử), **gold action** (loại + tham số). Không gian thao tác **8 loại lõi:** `click, long_press, input_text, scroll, navigate_home, navigate_back, open_app, wait` (+ `status`). 4 nhóm test: in-domain, app-unseen, task-unseen, category-unseen.

Bản làm việc của luận văn (`androidcontrol/*.episode.json`): episode = `{episode_id, goal, num_steps, steps[]}`; step = `{step_id, np, active_application, previous_actions, gold_action, screen_w, screen_h, ...}`; `gold_action` dạng lời gọi hàm, ví dụ `click{"x":275,"y":401}`.
> ⚠ Bản trích cục bộ **giữ `goal` mức episode + `gold_action` từng bước, nhưng CHƯA kèm accessibility tree và chỉ-dẫn-mức-thấp mỗi step** — hai thành phần đó ở bản phát hành đầy đủ, sẽ lấy bổ sung khi cần đối chiếu trung-thực-hoá cho nhánh nhiều-màn.

### 3.5. Ví dụ mẫu THẬT
Episode `ep2_14851`:
> **Goal:** *"Create a shortcut for me of The Queen's Gambit pdf file to the home screen on the Drive app."*
> **Quỹ đạo vàng (5 bước):** `click(1016,866)` → `scroll(down)` → `click(602,2105)` → `click(821,2252)` → `status(successful)`.

Đọc: đây là "quỹ đạo vàng" — thao tác đúng từng bước. Luận văn dùng để (a) suy **cặp thứ tự bắt buộc** theo quy tắc nhân-quả (màn sau chỉ hiện sau gold-action màn trước) → chấm **τ thứ-tự-bộ-phận**; (b) chấm **Step-SR** (bước đúng = đúng loại thao tác + lệch ≤ 14%).

### 3.6. Vai trò
Bộ **nhiều màn (có-gold) + Step-SR**: gold action người-thật từng bước làm ground-truth chấm trật tự + độ đúng thao tác. Chỗ **ra con số năng-lực-thật** cho đóng góp hệ thống. Giấy phép **CC0 1.0**.

### 3.7. Hạn chế + cách xử lý
1. **Xây cho tác tử bấm máy** → chỉ mượn gold trajectory làm tham chiếu, **không claim ngang leaderboard**; nhấn hợp đồng I/O khác (câu hỏi không chứa tên nút, đầu ra = hướng dẫn cho người).
2. **Chưa có histogram số episode theo N** → tự đếm (**cổng KN**).
3. **Rủi ro rò rỉ step-index/metadata** khi xáo trộn → **cổng KB** (strip metadata + tái mã hoá ảnh + che status bar/đồng hồ/pin/badge + loại episode 2-ảnh trùng-pixel).
4. **a11y tree không phải nhãn hoàn hảo** → hậu-kiểm + fallback.
5. **Chủ yếu EN**, không app VN.

---

## 4. ScreenSpot-v2 — bộ ĐỐI CHỨNG grounding (bbox hiệu đính)

### 4.1. Nguồn gốc và trạng thái bình duyệt
**ScreenSpot-v2** là bản **hiệu đính thủ công** của ScreenSpot gốc, **phát hành kèm bài OS-ATLAS** — `arXiv:2410.23218`, **ICLR 2025** (poster; OpenReview `n9PDaFNi8t`). Diễn đạt chính xác: dataset ScreenSpot-v2 **không có bài bình duyệt riêng**, được *mô tả + phát hành kèm* OS-Atlas (đã bình duyệt ICLR 2025). **ScreenSpot gốc** do nhóm **SeeClick** tạo, **ACL 2024** (`2024.acl-long.505`, `arXiv:2401.10935`). ⚠ *Danh sách tác giả đầy đủ OS-Atlas nên đối chiếu OpenReview trước khi in.*

### 4.2. Quy mô (số đã verify + phép cộng khớp)
**1.272 chỉ dẫn** một-bước (giữ nguyên tổng so gốc): **Mobile 502 · Desktop 334 · Web 436** (= 1.272). Mỗi nền tảng chia **Text** và **Icon/Widget**. ScreenSpot gốc: "hơn 600 ảnh" + 1.272 chỉ dẫn (iOS/Android, macOS/Windows, Web).
> **Chất lượng nhãn cao (điểm bù tín nhiệm cho MobileViews):** nhóm OS-Atlas phát hiện **~11,32% lỗi chú thích** trong bản gốc, sửa theo miền **Web 63/436 · Desktop 28/334 · Mobile 53/502** (= 144; 144/1.272 = **11,32%**, khớp nội tại).

### 4.3. Cách thu thập
Kế thừa ảnh + chỉ dẫn của ScreenSpot gốc (SeeClick: chụp màn đa nền tảng, gán chỉ dẫn + hộp bao **thủ công**). v2 = **hiệu đính thủ công**: sửa/viết lại câu lỗi, loại câu trùng, sửa bbox sai; giữ nguyên tổng.

### 4.4. Cấu trúc mỗi mẫu
Bản làm việc (`screenspot/item*.json`): `file_name, platform, instruction, data_type` (text/icon), `data_source` (ios/android/windows/macos/web), **`bbox_normalized_[x1,y1,x2,y2]`**, **`bbox_pixel_[x1,y1,x2,y2]`**, `image_size_[w,h]`, `image_file`.
> **Định dạng bbox đã giải:** dạng **`[x1,y1,x2,y2]`** (trên-trái, dưới-phải), có cả **chuẩn-hoá** lẫn **pixel** + `image_size` → thuận cho point-in-bbox. ⚠ *Bản gốc HuggingFace `OS-Copilot/ScreenSpot-v2` có thể dùng `[x,y,w,h]`; bản làm việc đã chuẩn hoá về `[x1,y1,x2,y2]` — nêu rõ để tái lập.*

### 4.5. Ví dụ mẫu THẬT
```
platform: mobile   data_source: ios   data_type: icon
instruction: "invert the lens"
bbox_pixel_[x1,y1,x2,y2]: [965, 2105, 1110, 2258]
image_size_[w,h]: [1170, 2532]
```
Đọc: cho ảnh + chỉ dẫn "invert the lens", đáp án đúng là hộp `[965,2105,1110,2258]` trên ảnh 1170×2532. Luận văn dùng kiểm bộ trỏ (x,y) **độc lập**: bộ trỏ dự đoán toạ độ từ *tên phần tử + ảnh*, kiểm điểm đó có trong bbox chuẩn không — **không** lấy tâm bbox đã khớp (tránh tautology 100%).

### 4.6. Vai trò
**Đối chứng grounding** độc lập, bbox peer-reviewed đã hiệu đính, hợp lệ-hoá bộ trỏ (x,y) + **bù credibility** cho MobileViews. Giấy phép **apache-2.0**. ⚠ *Giấy phép ScreenSpot GỐC chưa xác minh riêng.*

### 4.7. Hạn chế + cách xử lý
1. **Chỉ grounding một-bước, một màn** → không dùng cho nhánh nhiều-màn.
2. **Chỉ dẫn thường chứa/ám chỉ tên phần tử đích** → khác hợp đồng I/O → **chỉ** làm đối chứng bộ trỏ, không sinh hướng dẫn.
3. **Không kèm VH đầy đủ** → không thay vai một-màn của MobileViews.
4. **Quy mô nhỏ (1.272)** → thống kê hạn chế.
5. **Đã bão hoà** với model mới; ScreenSpot-Pro (hi-res) là **bộ KHÁC**, không dùng ở đây.

---

## 5. Tập con thực dùng trong luận văn (minh bạch lấy mẫu)

Nhánh một-màn **thực tế chỉ chạy trên 81 màn / 17 app** rút từ MobileViews-600K (`mv_multiapp`, đã đếm: **81 màn / 17 app** trong `kept_screens.json`). Quy tắc gộp app: `app = tiền_tố_tên_file` (trước dấu `_`) → **cluster-bootstrap theo app** được. Pipeline lọc **90 → 81 màn** (loại màn rác) qua `dg1_data.py`.

**Khai thẳng giới hạn tính đại diện:** 81 màn là **mẫu chủ ý giai đoạn thiết kế**, không đại diện thống kê cho 600K/1,2M. Kết quả sơ bộ (gpt-4o-mini): bịa bản gốc ~¼ số bước; lớp đối chiếu nâng faithfulness mọi ngưỡng nhưng **CI 95% còn chạm 0** (n nhỏ, ít app); fallback ~19%. **Phòng thủ tính đại diện bằng phương pháp thống kê đúng** (cluster-bootstrap theo app + CI 95% + Holm + seed + pre-register), **không** bằng số mẫu; cam kết chạy bản chính khi có ngân sách API.

**Tái lập:** ghim phiên bản + ngày tải khi in (đặc biệt MobileViews arXiv **v3**). **Cả ba bộ không có app tiếng Việt** → định lượng chạy EN/ZH; tiếng Việt = demo định tính + ~120 mẫu app VN cho chuyên gia (nói rõ: **không có bảng số VN định lượng**).

---

## 6. Bảng so sánh ba bộ dữ liệu

| Tiêu chí | **MobileViews** | **AndroidControl** | **ScreenSpot-v2** |
|---|---|---|---|
| **Vai** | Một màn (không-gold) | Nhiều màn (có-gold) + Step-SR | Đối chứng grounding |
| **Quỹ đạo vàng?** | **Không** | **Có** (người-thật, từng bước) | Không (bbox một-bước) |
| **Nguồn phần tử UI** | View Hierarchy đầy đủ (JSON) | Accessibility tree mỗi bước | Không (ảnh + bbox) |
| **Quy mô** | Paper >1,2M/>30K app; **công khai 600K**/>20K app; **dùng 81 màn/17 app** | 15.283 ep / 833 app / 40 cat; mean 5,5; p95=13 | 1.272 chỉ dẫn (502 mobile/334 desktop/436 web) |
| **Thu thập** | Bot tự động (VLM-traversal) + a11y | **Người thật**, Pixel, ~1 năm | Thủ công + **hiệu đính** (sửa 11,32% lỗi) |
| **Bình duyệt** | **Preprint** arXiv 2409.14337 v3 | **NeurIPS 2024 D&B** | **kèm OS-Atlas ICLR 2025**; gốc SeeClick ACL 2024 |
| **Giấy phép** | MIT | CC0 1.0 | apache-2.0 |
| **Toạ độ** | `bounds=[[x1,y1],[x2,y2]]` (⚠ hiệu chỉnh khung) | gold `{x,y}`, screen_w/h | `[x1,y1,x2,y2]` (chuẩn-hoá + pixel) |

---

## 7. Chống rò rỉ dữ liệu (LUẬT VÀNG)
1. **VH + đáp án vàng CHỈ vào lúc CHẤM**, không vào lúc sinh/sắp. Mô hình sinh "mù" (chỉ ảnh + câu hỏi).
2. **Câu hỏi KHÔNG chứa tên nút** → buộc mô hình tự đọc ảnh (chỗ nó bịa, chỗ ta đo).
3. **"Chấm baseline" là bước ĐÁNH GIÁ**, không phải bước deploy (deploy = sinh → hậu-kiểm → né bịa).
4. **Chống tautology grounding:** (x,y) từ **bộ trỏ độc lập**, không lấy tâm bbox đã khớp.
5. **Chống rò rỉ thứ tự:** nhãn cặp bắt buộc **suy từ GOLD**, không từ model/cue-detector; ảnh strip metadata + che status bar (**cổng KB**).
6. **Chống vòng đo lường:** quyết matched/fallback = nomic; **chấm** = bge-m3 độc lập + LLM-judge khác-họ + token-overlap (3 cơ chế); validate metric bằng perturbation.

---

## 8. ⚠ ĐIỀU KIỆN CẦN CHỐT/KIỂM TRƯỚC KHI IN BẢN CUỐI
1. **KHÔNG in số test "2.855"** cho AndroidControl → dùng **1.542** (hoặc đối chiếu PDF gốc).
2. **Tính con số độ-phủ-nhãn VH** thật trên `mv_multiapp` (`harness/dg1_vh_coverage.py`, chưa chạy).
3. **Hiệu chỉnh khung toạ độ MobileViews** (lệch width/height, bounds lồng nhau) TRƯỚC khi tính grounding.
4. **Đối chiếu danh sách tác giả OS-Atlas** trên OpenReview trước khi in trích dẫn.
5. **KHÔNG khẳng định** affiliation Xiaomi của 3 đồng tác giả MobileViews.

---

**PHÁN QUYẾT (từ debate):** phần dataset **đã đủ vững để trình hội đồng** — ba bộ vai tách bạch theo trục "có/không quỹ đạo vàng", số liệu cốt lõi verify tận file, mọi đòn phản biện (preprint, mẫu nhỏ, lệch mục đích) đều có câu thủ minh bạch. Chỉ cần chốt 5 điều kiện ở §8 trước khi in.

*Nguồn: đối chiếu web (arXiv/HuggingFace/aclanthology/OpenReview/neurips.cc) + file thật `dataset_samples/`. Bản tổng quan toàn đề tài: `report/43`.*
