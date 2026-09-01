# 131 — FAIR: LƯỢT VIẾT LẠI THEO CHỈ ĐẠO 31/8 VÀ TÌNH TRẠNG NỘP

> Nguồn lệnh: **`report/130_CHI_DAO_VIET_LAI_FAIR_31_8.md`** (chép từ 11 ảnh trong
> `paper/fair2026/My Documents [31-08-2026 22_43].zip`).
> Bản trước lượt này: **`paper/fair2026/main_TRUOC_VIET_LAI_MODEL_31_8.tex.bak`**.
> File này ghi *đã làm gì* và *nộp tới đâu*; muốn biết *vì sao* thì mở `130`.

---

## 1. TÌNH TRẠNG NỘP — ĐỌC TRƯỚC

| | |
|---|---|
| Hệ thống | EDAS `edas.info/index.php?c=35461` |
| Mã bài | **#276 (EDAS ID 1571349424)** |
| Tiểu ban | **Natural Language Processing** |
| Trạng thái EDAS | ⛔ **Pending (no manuscript)** — đăng ký kịp, **upload không kịp** |
| Hạn | 23:59 31/8/2026 (Asia/Ho_Chi_Minh). Bấm upload lúc **00:02 1/9** ⇒ cửa đã đóng |
| Đã xử | Ghi link Drive vào *Personal notes*; **gửi email** kèm PDF cho PGS.TS. Trần Văn Lăng xin mở lại upload |
| File đã gửi | `paper/fair2026/FAIR2026_1571349424.pdf` — **106.258 byte · 7 trang · md5 `ab60520318a8aa34e0f58bcb08f3f035`** |

⚠️ **Chưa xác nhận bài được nhận.** Phải theo dõi hồi âm; nếu tới hết 1/9 chưa có thì gọi
**0903 938 036**.

### Đầu mối FAIR'2026 (tra từ `fair.conf.vn/vi/index.php/gioi-thieu.html`, 31/8)

| việc | người | liên hệ |
|---|---|---|
| **nhận bài / nộp bài** | **PGS.TS. Trần Văn Lăng** | **langtv@vast.vn** · 0903 938 036 |
| chương trình | TS. Lê Quang Minh | quangminh@vnu.edu.vn · 0989 736 464 |
| tổ chức địa phương | TS. Nguyễn Thị Định | dinhnt@huit.edu.vn |

**Mốc:** nộp 31/8 · **báo kết quả 15/9** · **hội nghị 8–9/10/2026** tại ĐH Công Thương TP.HCM.
Kỷ yếu in trong **IEEE Proceedings**. Chủ đề: *"Trí tuệ nhân tạo và các xu thế trong tương lai"*.

### ⛔ BÀI HỌC ĐẮT NHẤT CỦA PHIÊN — đồng hồ máy lệch 7 giờ

**Máy WSL chạy giờ UTC.** Lúc WSL báo `16:53` thì giờ Việt Nam đã là **23:53**. Cả phiên làm
việc dưới ấn tượng "còn 7 tiếng" trong khi thực tế **còn 7 phút**.
⇒ **Luật: mọi mốc hạn nộp phải đọc bằng `TZ='Asia/Ho_Chi_Minh' date`, không đọc `date` trần.**
Con số footer của EDAS (`+0700`) là nguồn đúng, đồng hồ máy không phải.

---

## 2. BÀI SAU KHI VIẾT LẠI

**Dựng:** `rm -f main.log && tectonic -X compile main.tex --outdir . --keep-logs`
⇒ **7 trang · 0 Overfull · 0 tham chiếu hỏng · 0 citation hỏng · 3 Underfull (vô hại)**.
US Letter 8,5×11 · 6 font nhúng đủ · **không số trang/header/footer** (EDAS đòi) ·
metadata `pdftitle`/`pdfauthor` đã set. Thân bài ~4.950 từ.

**Đổi lớn so với bản trước:**

| | trước | sau |
|---|---|---|
| nhan đề | *Descriptor-First Supervision for GUI Instruction Generation* | **Descriptor and Preference Targets for GUI Instruction Generation** |
| §IV | *Descriptor-First Supervision*, ~250 từ, không công thức | **Targets and a Stage-2 Objective**, 4 tiểu mục, **có công thức ORPO + `\bibitem{orpo}`** |
| thứ tự | Method sau Data, Instrument dài hơn Method | **Method trước Instrument** |
| hình | sơ đồ Voronoi | **hình target 3 hàng** (`fig:targets`), dựng bằng `tabular`, không TikZ |
| Table 1 | có cột `% of 75.7` | **bỏ cột đó**, thêm nhãn khối *Stage 2*, một `\textbf` duy nhất (59,4 của S1 mean) |
| keywords | có `reference-free evaluation`, `pre-registration` | **preference tuning, executability** |

**Hai bảng mới ở §V:** `tab:inject` (phép bơm lỗi, **1.000 lượt** = 250 bước × 4 góc) và
`tab:rules` (năm luật chấm trên 698 bước). Cả hai là bằng chứng đã đo, trước nay nằm ngoài bài.

---

## 3. SỐ MỚI ĐO TRONG PHIÊN — chưa từng có ở đâu khác

Đo bằng tokenizer `Qwen2.5-VL-3B-Instruct` trên đủ **22.854 cặp** của
`harness/dg1_cache/train_ac/branches/min_desc.json`. **Đã kiểm chéo hai lượt độc lập, trùng khít.**

| đại lượng | giá trị |
|---|---|
| độ dài token vế **accepted** (min/p5/p50/p95/max) | 33 / 37 / **44** / 58 / 101 |
| độ dài token vế **rejected** | 33 / 37 / **45** / 58 / 114 |
| hiệu ch−rj (min/p5/p50/p95/max) | −35 / −8 / **0** / +7 / +41 |
| `\|Δ\| ≤ 2` token | **62,8%** |
| đuôi câu tách token **trùng khít** hai vế | **22.854 / 22.854** |
| chuỗi đầy đủ dài nhất (kèm 1.272 token ảnh) | **2.002** token, cutoff 2.560 ⇒ **0 cặp bị cắt** |

⚠️ `build_min_desc.py:127-132` chỉ đo lệch theo **ký tự**, không theo **token** — đây là lần đầu
đại lượng token được đo.

**Cài đặt tra được từ mã đã pin** (LLaMA-Factory `c4e09c7cbe18…`, kéo thẳng từ SHA đó):
· `train_on_prompt: false` + descriptor và câu nằm trong **một** message assistant ⇒ **câu nằm
  trong cả hai log-likelihood** của preference score;
· công thức ORPO trong bài **khớp nguyên mã** `odds_ratio_loss`;
· ⭐ **trainer ghép cặp zero mọi dropout lúc dựng model**, gồm cả LoRA dropout 0,05 mà trainer
  SFT vẫn giữ ⇒ **MIN và CE2 lệch một biến không kiểm soát**. Đã khai thẳng vào §IV-D.
  ⚠️ Đây là bằng chứng về **mã tại SHA đã pin**, không phải log của lượt chạy thật.

---

## 4. SỐ ĐÃ SỬA / ĐÃ BỎ TRONG PHIÊN

| số | phán quyết |
|---|---|
| `2,19 pp` (S2 − S1 mean) | ⇒ **2,18** (59,3659 − 57,1813 = 2,1846). 2,19 là làm tròn hai lần |
| `the other 1,374` | ⇒ **1.374 of the 3.245 crossed steps**. Phần bù thật của 1.871 trên toàn quần thể là **2.592** |
| `+1,48` gắn với n=109 | ⇒ gắn đúng **n=881** |
| cổng adequacy trộn `0,7 / 2,00 / 7,82` | ⇒ tách: cổng **n=300** trung vị **0,73%** (nhánh human); bộ ba trên giao **n=4.462**: human **0,67** · S1/101 **2,00** · Base **7,82**; **Base TRƯỢT cổng 3%** |
| `89,6%` gán cho **ba** lát diễn đạt lại | ⛔ **SAI, đã sửa.** 89,6 là mức nền của riêng lát `p2_order` (211 bước); lát `p1_verb` (725 bước) chỉ **76,8**. Bài nay ghi **dải 76,8–90,1** vs 74,9 toàn lát |
| `71,0%` (ô point S2 trúng cửa sổ 14%) | ⛔ **BỎ khỏi bài** — không truy được mẫu số. `report/117:38` ghi "cùng nguồn" nhưng nguồn là bảng n=3.240, còn bài dùng phân hoạch 3.245/4.126 ⇒ gắn n nào cũng là suy ngược |
| `2,6% of steps` (tập con train chứa phrase trùng) | ⛔ **BỎ** — chỉ truy được tới ghi chú khẳng định (`report/118:238`, `report/129:451`), không có script, không có tệp đo, `train_ac/train.jsonl` không có trên WSL. **17,3% thì giữ** |
| `three empty sentences` | ✅ **GIỮ, đã truy được**: đúng 3 bản ghi thiếu trường `executable` — S1/101 (18710,1) · S1/202 (18710,1) · S2 (20011,2) |
| `hit_disk` của S2 | ⚠️ `report/119:62` ghi **67,5**; số thật trong `score_s2_seed101.json` là **67,44** ⇒ **bài đúng, ghi chú sai** |

⭐ **Toàn bộ phần ĐO tái lập được.** Một giám khảo dựng lại từ tệp thô: cả 21 ô Bảng 1, cả 24 ô
bảng chéo (kể cả số đếm nguyên 1523/1871, 227/738…), toàn bộ bảng Venus, mọi McNemar (b, c, χ², p),
mọi phân hoạch, mọi phân rã. **Không số nào bịa, không số đã rút nào tái xuất.**

---

## 5. VÒNG PHẢN BIỆN — NĂM GIÁM KHẢO

Bốn giám khảo song song (đóng góp mô hình · soát số · liêm chính · văn phong+ngân sách trang),
rồi một giám khảo cuối săn lỗi **do chính quá trình vá sinh ra**.

**Phán quyết:** weak reject → **borderline** sau khi vá.

**Đòn CHẶN đã vá (6 lỗi cuối, đều là câu chữ, không phải đo):**
1. ⛔ **`byte- identical` bị tách đôi trong PDF** — xuống dòng sau gạch nối trong nguồn TeX.
   Lỗi *nhìn thấy được* trên bản in. **Luật: không xuống dòng ngay sau gạch nối.**
2. Bài tuyên bố "ước lượng 70,0% đã rút" ở §V trong khi Bảng 2 vẫn in 70,0 ⇒ caption nay ghi rõ
   đó là phép kiểm adequacy n=300, không phải ước lượng quần thể.
3. Kết luận khẳng định một **null** (`buys no executability`) từ một lượt train, trong khi
   Limitations vừa nói không phát biểu được ⇒ hạ về đúng phạm vi.
4. §IX nói *"phép viết lại giữ nguyên tên phần tử"* trong khi §V có hẳn phép **thay tên** (−28,5 pp).
5. Câu gãy `on a cell too small to resolve one`.
6. Con số 89,6% gán sai lát (mục 4).

**Đòn đã vá ở vòng trước:** câu cụt giữa §VIII · chữ `gain` cho nhánh thua ròng (đổi cả tiêu đề
mục) · gọi quyết định hậu kiểm là `registered` ngay cạnh caption thú nhận ngược lại · khẳng định
null trên n=78 · dùng `zhao2021` ngược khuyến nghị của chính họ · `\cite{ogp}` gắn vào định nghĩa
của mình · `3.473` vs `3.245` không nói khác nhau chỗ nào · Bảng 1 chưa từng được `\ref` · ngưỡng
2,11 không có xuất xứ · mẫu số 14,1% · `MIN−S1` không ghi là **S1/101**.

**⛔ Rủi ro nền, không cứu được bằng câu chữ:** không can thiệp nào **vừa mang tên đóng góp vừa
thắng có ý nghĩa**. S2 57,2 < S1 59,4 · MIN−CE2 +0,63 dưới MDE 2,11 · MIN−S1 p=0,11 và ngang
S1/101 ở 69,2 dưới luật dung sai · 78% mức tăng stage-2 thuộc đối chứng. Bài tối ưu để review ghi
*"evidence is incomplete"*, **không** phải *"claims exceed evidence"*.

⚠️ **Cân bằng trọng tâm chưa đạt:** §IV = 522 từ, §V = 840 từ (+2 bảng). Tính rộng, phần dụng cụ
(§V + §VII-B + ba mục Limitations) ≈ **1.270 từ** so với **522** của phương pháp ⇒ **2,4 : 1**.
`report/130` §1 chốt "không để thước dài hơn Method". **Nếu có vòng camera-ready thì cắt §V ~180
từ** (bỏ đoạn Birthday/Gender và đoạn tự nhận "percentile would have been better").

---

## 6. YÊU CẦU MỚI CỦA CHỦ LUẬN VĂN (áp trong phiên, giữ cho các bài sau)

1. ⛔ **Không câu hỏi tu từ — kể cả khi không có dấu `?`.** Mệnh đề nghi vấn gián tiếp làm tiêu đề
   cũng bị cấm: *What is held fixed* ⇒ **Invariants across branches**; *Where the Gain
   Concentrates* ⇒ **The Descriptor Contrast by Identification Outcome**.
2. ⛔ **Bỏ mẫu "where …" kiểu "nơi mà"** — nghe như máy dịch. Từ 12 lần xuống **2**, và 2 chỗ còn
   lại là ký hiệu toán (`where $d^{+}$ records…`).
3. ⛔ **Không kể lể chi phí máy.** Gỡ sạch giờ A100, tên card, hạn mức Kaggle, ngày huỷ lượt chạy.
   Đoạn *Registered, not run* viết lại thành **An incomplete registered estimand** — chỉ khai
   **kết quả** (mỗi nhánh một lượt, hai đối chứng không chạy, contrast là thăm dò), **không khai
   nguyên nhân**.
4. ⛔ **Không nhắc bài đang bình duyệt ở hội nghị khác.** Gỡ hết `\cite{companion}` và bibitem.
   ⚠️ **Hệ quả phải biết:** các thống kê nhãn ở §III (41.099 · 73,6/4,4/22,0/7,6 · lát audit 1.074)
   nay **không còn nguồn để trỏ**; chỉ 12,6% còn `\cite{chen2020}`.

---

## 7. VIỆC CÒN LẠI

- [ ] **Theo dõi hồi âm của PGS.TS. Trần Văn Lăng.** Chưa có xác nhận nào là bài đã được nhận.
- [ ] Sửa trên EDAS: last name của thầy đang là **`Nguyen`**, phải là **`Long`** (hiện hiển thị
      *Nguyen Hong Buu Nguyen*); affiliation hai tác giả đang khác nhau, nên thống nhất
      `Faculty of Information Technology, University of Science, VNU-HCM, Vietnam`.
- [ ] Nếu được mở lại upload: đẩy đúng `FAIR2026_1571349424.pdf` (md5 ở mục 1).
- [ ] Nếu vào camera-ready: cắt §V ~180 từ để lấy lại tỉ lệ Method/Instrument (mục 5).
