# 138 — Nâng trần phép đo bằng luật gốc của AndroidControl (đo 5/9/2026)

> Hai lượt tra độc lập + một phép đo trên máy, tất cả trong đêm 5/9. Kết quả chính: **có một
> luật chấm nâng trần từ 75,73% lên 83,82% mà KHÔNG phải nới lỏng tiêu chí do nhóm tự chọn**,
> vì nó là luật gốc của chính bộ dữ liệu đang dùng.

## 1. ⭐ Luật D.3 — đo được ngay, 0 giây GPU

**Nguồn:** Li et al., *AndroidControl*, **NeurIPS 2024 Datasets & Benchmarks**, Phụ lục D.3.
Nguyên văn: *"For element-based actions (click, long press, type), if the target element's
coordinates are within the bounding box of the ground truth target element, it is considered as
matching. This relaxation matches the behavior on Android devices where a touch gesture will
activate an element as long as it falls within the element's bounds."*

Tức: điểm bộ trỏ trả về chỉ cần **nằm trong hộp bao của phần tử vàng**. Hộp có sẵn trong
`descriptors.jsonl` (trường `box`, phủ **4.448/4.448 = 100%**), nên tính lại từ `*_raw.jsonl`
mà không gọi bộ trỏ lần nào.

### 1.1 Tám nhánh, n = 4.463

| nhánh | Voronoi .14 (đang dùng) | chữ nhật .14 | **D.3 trong hộp** | chênh D3−Vor |
|---|---|---|---|---|
| **Câu người (trần)** | 75,73 | 84,23 | **83,82** | **+8,09** |
| MIN-DESC/101 | 60,05 | 68,72 | **66,55** | +6,50 |
| CE2-S2/101 | 59,42 | 68,45 | 66,03 | +6,61 |
| S1/202 | 59,62 | 67,91 | 66,10 | +6,48 |
| S1/101 | 59,11 | 67,24 | 65,49 | +6,39 |
| S2/101 | 57,18 | 65,72 | 63,63 | +6,45 |
| `gui_sel`/101 | 56,13 | 63,86 | 62,38 | +6,25 |
| Base | 47,59 | 55,86 | 53,60 | +6,00 |

⭐ **Thứ tự tám nhánh không đổi một chỗ nào.** Khoảng cách S1−Base giữ nguyên (11,89 dưới D.3 so
với 11,52 dưới Voronoi); MIN−S1 là 1,06 so với 0,94.

### 1.2 ⭐ Phép kiểm quyết định: D.3 có nâng sàn không

Đây là chỗ đã giết hướng nới luật ngày 30/8 — luật lỏng nâng trần nhưng nâng cả sàn. Đo trên
**cùng lát 800 bước** của bộ sàn:

| | Voronoi .14 | **D.3** | chênh |
|---|---|---|---|
| trần (câu người) | 74,88 | **83,00** | **+8,12** |
| sàn `f1` — câu rỗng nghĩa | 12,00 | 14,12 | **+2,12** |
| sàn `f3` — câu đúng văn phong, sai màn | 6,12 | 8,62 | **+2,50** |
| `f2` — bỏ tên, giữ vị trí | 68,00 | 74,75 | +6,75 |
| **dải dùng được (trần − sàn `f1`)** | 62,88 | **68,88** | **+6,00** |

⇒ **D.3 nâng trần gấp gần 4 lần mức nó nâng sàn**, tức nó **mở rộng** dải phân biệt chứ không
nén. Đối chiếu: luật chữ nhật ±14% kéo sàn `f1` lên **20,50** — đó mới là nới lỏng thật.

### 1.3 Vì sao nó không phải là "nới lỏng"

Dung sai của D.3 **thích ứng theo cỡ phần tử thật**, còn ±14% là hằng số:

| | hộp phần tử vàng | cửa sổ ±14% hiện tại |
|---|---|---|
| bề ngang | trung vị **23,1%** màn · p10 7,3 · p90 92,2 | 28% màn, cố định |
| bề dọc | trung vị **5,2%** màn · p10 2,2 · p90 8,8 | 28% màn, cố định |

Theo **chiều dọc**, hộp thật hẹp hơn cửa sổ hiện tại tới **5 lần** ở trung vị — tức D.3 **chặt
hơn** ở nút nhỏ. Nó chỉ lỏng hơn ở những phần tử thật sự rộng (hàng danh sách, thanh ngang), và
lỏng đúng theo nghĩa vật lý: chạm chỗ nào trong phần tử cũng kích hoạt được nó.

### 1.4 Cách dùng, và cái phải giữ

· Rủi ro bị phản biện *"chọn thước cho hợp kết quả"* là **thấp nhất trong mọi hướng đã tra**, vì
  luật này do **tác giả bộ dữ liệu** đặt ra và đã qua bình duyệt NeurIPS 2024, không phải nhóm chế.
· ⛔ Nhưng nó vẫn được tính **sau khi đã thấy mọi điểm**. Cách trung thực: trình D.3 như **thước
  đồng-báo** cạnh Voronoi, khai rõ nguồn và khai rõ thời điểm tính, **giữ Voronoi làm headline**
  vì đó là thước đã niêm từ 5/8. Nếu đổi headline thì phải khai đó là quyết định sau khi thấy số.
· Lá chắn mạnh thêm một bậc: nay có **bốn** luật cho cùng một kết luận (Voronoi · nL2 · chữ nhật ·
  D.3), thứ tự nhánh không đổi ở luật nào.

---

## 2. Cách trình kết quả — tra ngược lại ý định ban đầu

⛔ **Chuẩn ngành trong sinh ngôn ngữ có mốc người là báo HAI SỐ TUYỆT ĐỐI cạnh nhau kèm chữ
*headroom*, KHÔNG chia tỉ lệ.**

| nguồn | cách trình |
|---|---|
| ⭐ **Zhao et al., EACL 2021, tr. 1302–1316** (bài dự án đã trích) | Bảng 1: **Human 75,1** · EnvDrop 47,7 · Speaker-Follower 42,3. *"they are far worse than human instructors. This leaves much headroom for better instruction generation."* Mốc người **75,1** gần trùng 75,73 của dự án — tiền lệ đúng bài toán sinh câu chỉ đường |
| Tang, Mao, Suhr, **EMNLP 2024** | *"human-human pairs achieve an average communicative success rate of 87,6"*; GPT-4o 64,9; *"all models lag far behind humans"* |
| **AndroidWorld, ICLR 2025** | M3A 30,6% *"remains significantly lower than the human success rate of 80,0%"* — cùng miền GUI Android, in cạnh nhau |
| **SuperGLUE, NeurIPS 2019** | *"nearly 20 point gap"* |
| ⚠️ Nangia & Bowman, **ACL 2019** | gọi mốc người là *"a conservative estimate of human performance"* — cách gọi an toàn nhất |
| ⚠️ Tedeschi et al., **ACL 2023** | phê phán chính diện việc ước lượng *"human baseline"* một cách mơ hồ |
| ⚠️ Läubli et al., **EMNLP 2018** + Toral et al., **WMT 2018** | mốc người do **người không chuyên** viết thì kết luận đảo chiều — trúng dự án, vì câu AndroidControl do crowdworker viết |

⛔ **Con số "79,3% năng lực của người" đang dùng có hai lỗi:**
1. Nếu viện dẫn công thức chuẩn hoá hai mốc của Mnih et al. (*Nature* 518:529–533, 2015) thì
   phải **trừ sàn**: `100 × (điểm − sàn)/(trần − sàn)`. Với sàn 12,0 thì MIN-DESC là **75,4%**
   chứ không phải 79,3%.
2. Mà ngay cả 75,4% cũng chưa dùng được: sàn 12,0 đo trên **lát 800** có trần riêng 74,9, còn
   60,05 đo trên **4.463**. Trộn hai mẫu số vào một công thức chuẩn hoá là lỗi.
   ⛔ Thêm một bẫy: chính Mnih et al. thao tác hoá *"ngang người"* là **≥75%**. Công bố 75,4% theo
   công thức đó là vô tình tự tuyên bố ngang người — đúng thứ Läubli/Toral giết bằng số.

⇒ **Bỏ cách trình theo tỉ lệ.** Dùng nếp Zhao et al.: in hai số cạnh nhau, gọi 75,73 (hoặc 83,82
dưới D.3) là **"ước lượng thận trọng về năng lực của câu người viết, đo qua cùng dụng cụ"**, và
dùng chữ *headroom* cho khoảng cách.

---

## 3. Bộ trỏ — chỉ một ứng viên đóng được đòn "cùng họ Qwen"

| mô hình | venue | mobile SSv2 | giấy phép | có AndroidControl? | ngoài họ Qwen? |
|---|---|---|---|---|---|
| **Phi-Ground-4B** (nền Phi-3.5-Vision) | arXiv 2507.23779 — **preprint** | 78,1 (câu ngắn) / 92,4 (câu dài) | **MIT** | **KHÔNG** (Bảng 8) | **CÓ** |
| UI-Venus-Ground-7B | preprint | 99,0 / 90,0 | Apache-2.0 | không ở nhánh grounding | không |
| UGround-V1-2B (đang dùng) | **ICLR 2025 Oral** | — | Apache-2.0 | **CÓ, 47K** | không |
| OS-Atlas-Base-4B | **ICLR 2025 Spotlight** | 87,24 / 59,72 | chưa xác minh | **CÓ, 47,7K** | có |
| Jedi-7B | **NeurIPS 2025 D&B Spotlight** | 96,9 / 87,2 | chưa xác minh | **CÓ, 54.678 ảnh** | không |
| GTA1-7B · SE-GUI-7B | ICLR 2026 / NeurIPS 2025 | 99,0 / 95,2 | chưa xác minh | **CÓ, gián tiếp** | không |

⚠️ **Luật đọc mới:** nhiều bài 2025–2026 không nhắc AndroidControl nhưng **mượn gói dữ liệu của
mô hình khác** vốn có nó (GTA1 ← OS-Atlas · SE-GUI ← UGround · POINTS-GUI-G ← OS-Atlas). Phải
truy thêm một tầng mới kết luận được "sạch".

⭐ **Hai tiền lệ mới cho hiện tượng dự án đã gặp** (bộ trỏ mạnh hơn nhưng chấm thấp hơn):
· Phi-Ground §6.1: *"some models perform well on ScreenSpot-V2 but do not demonstrate the same
  significant advantages on newly emerging benchmarks… a result of developers optimizing their
  models based on a single benchmark"*. Kèm số: đổi từ câu ngắn sang **câu dài do máy sinh**,
  OS-Atlas-4B tụt **71,9 → 57,4** trong khi UI-TARS-7B lại tăng ⇒ **thứ hạng bộ trỏ đảo khi câu
  chuyển từ người viết sang máy sinh**.
· **Jandial et al. nay xác minh được venue: Findings of ACL: EACL 2026, tr. 2772–2785.** Bảng 1:
  **UGround-V1-7B bền NHẤT trước cách diễn đạt khác nhau** (s_mean 0,3176) dù ScreenSpot-Pro chỉ
  31,1; Jedi-7B-1080p bền kém nhất (1,0426) dù SS-Pro 39,5. ⇒ Đây là lý lẽ mạnh nhất để **giữ
  UGround**, mạnh hơn lập luận đang dùng. ⚠️ Con số đó là của biến thể **7B**; dự án dùng **2B**
  (s_mean 0,6218) nên phải khai đúng biến thể.

---

## 4. Những hướng đã tra và LOẠI

| hướng | vì sao loại |
|---|---|
| hợp nhất nhiều lượt lấy mẫu của một bộ trỏ (GUI-RC, **AAAI 2026**) | tác giả tự khai *"relatively limited improvements for models with point-style outputs"* — đúng UGround; và cột mobile chỉ +1,1…+1,6 pp |
| hợp nhất nhiều khung nhìn (MVP, **CVPR 2026**) | chỉ đo trên ScreenSpot-Pro / UI-Vision / OSWorld-G, **không có mẫu di động nào** |
| Oracle@K làm điểm | Hit@K thô **là** nới tiêu chí. Bản hợp lệ (đề xuất K rồi một bộ thẩm định chọn một) thì đắt. ⚠️ Trên ScreenSpot-**v2**, khoảng cách Oracle@5 − Top-1 chỉ **0,5–0,6 pp** ⇒ gần như không có gì để thu |
| hợp nhất **nhiều bộ trỏ khác nhau** | **không tìm thấy tiền lệ đã bình duyệt trong miền GUI** |
| LLM làm giám khảo | ⛔ **AgentRewardBench (COLM 2025)**: precision cao nhất của giám khảo LLM chỉ **69,8%**, **thấp hơn trần dụng cụ hiện tại 75,73%** ⇒ đổi sang LLM-judge là **hạ trần**. Cộng tự-ưu-ái đã chứng minh ở **NeurIPS 2024 Oral** (Panickssery et al.) nếu giám khảo cùng họ mô hình bị chấm |
| luật hợp 14% **hoặc** cùng hộp mở rộng 240% (AITW, **NeurIPS 2023 D&B**) | **có** nới, nâng cả sàn. Nhưng là quy ước ngành nên dùng được làm thước đồng-báo. ⓘ Chi tiết **240%** là thứ dự án chưa từng ghi ở đâu |
| lọc lại tập kiểm (Northcutt, **NeurIPS 2021 D&B**) | ⚠️ rủi ro cao nhất: tiêu chí lọc phải khoá **trước** khi nhìn điểm. Dự án đã tự khai hai lần nới ngưỡng sau khi thấy điểm |

---

## 5. Ba việc làm được ngay, 0 giây GPU

1. **Đưa hàng D.3 vào bảng chính** cho cả tám nhánh, khai rõ nguồn (Phụ lục D.3 của AndroidControl)
   và khai rõ nó được tính sau khi đã thấy điểm. Giữ Voronoi làm headline.
2. **Bỏ cách trình "79,3% năng lực của người"**, thay bằng nếp Zhao et al. — hai số cạnh nhau,
   chữ *headroom*, và gọi mốc người là *ước lượng thận trọng*.
3. **Vá citation Jandial** thành Findings of ACL: EACL 2026, tr. 2772–2785, và thêm số Bảng 1 của
   bài đó làm căn cứ giữ UGround (nhớ khai đúng biến thể 2B).

Sau 16/9, nếu còn ngân sách: **Phi-Ground-4B** làm phép đổi dụng cụ thứ hai trên đúng lát 2.532
của phép B. ⚠️ Nó chỉ có `.bin`, cần `trust_remote_code`, và T4 là Turing (không bf16, không
flash-attn 2) — đúng tổ hợp đã làm ShowUI-2B ra NaN. Probe một lát nhỏ và bắt tiến trình in ra
`dtype` thật trước khi đặt lượt 5,6 giờ.
