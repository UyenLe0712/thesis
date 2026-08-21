# Bài FAIR'2026 — trạng thái bản thảo

> ## ⚡ TRẠNG THÁI MỘT TRANG (15/8/2026) — đọc khối này là đủ để làm tiếp
>
> **Nộp:** hạn **31/8**, qua **EDAS** (`edas.info/index.php?c=35461`), track NLP, không ẩn
> danh. **Mẫu IEEE conference · ≤8 trang · ≤5 từ khoá · tiếng Anh.**
> **Bản hiện tại: 8 trang · 0 lỗi · 0 tràn lề · 0 trích dẫn treo · 23 tài liệu · US Letter ·
> font Times (TeX Gyre Termes) cả chữ lẫn công thức.**
> Build: `tectonic -X compile main.tex --outdir .` → `main.pdf` → chép sang
> `FAIR2026_executability.pdf`.
>
> **Cấu trúc:** I Introduction · II Related Work · III Task and Dataset · IV Executability
> Metric · V Model and Experimental Design · VI Reproducibility · **VII Baseline Results** ·
> VIII Limitations · IX Conclusion. 7 bảng, 1 hình (đường cong độ nhạy).
>
> **⛔ RÀNG BUỘC — vi phạm là hỏng bài:**
> · mọi điểm số đọc trên nền **trần 75,7%** *(số 70,0 đã rút 15/8)*, không phải 100, và phải nhắc tại chỗ
> · **chưa được** viết bảng so sánh S1-vs-S2, MDE thật, cỡ nhiễu hạt giống
> · **cấm chữ "đầu tiên"/"mới"** cho cả hai lớp đóng góp
> · số nào `report/108` mục 9 đã rút thì cấm dùng lại; mọi số phải đo hoặc tra
>
> **▶️ VIỆC CÒN LẠI — cả hai chỉ đụng Bảng VI, không phải viết lại mục nào:**
> 1. **s1 hạt giống 202** → cỡ nhiễu + MDE thật (**tính cả hai cách**: độc lập và ghép cặp
>    McNemar, vì mọi nhánh chấm trên cùng 4.462 bước) → khoá ngưỡng vào `report/106`
> 2. **Base** đang chấm → điền nốt Bảng VI
> 3. Nếu train S2: **phải dựng lại nhãn + 4 nhánh ở quy mô đủ trên Colab** (ô 0.10 → 0.11)
>    vì nhãn đã đổi sang tiếng Anh — `report/106` mục sửa đổi **(q)**
>
> **Tệp trong thư mục này:** `main.tex` (bản thảo) · `SO_LIEU_NGUON.md` (mỗi số → report nào)
> · `KIEM_LAI_MA_VA_DU_LIEU.md` (18 khẳng định tái lập từ mã/dữ liệu + 4 lỗi đã bắt) ·
> **`PHAN_BIEN_5_GIAM_KHAO.md`** (chấm bài theo thang ARR + việc nên làm xếp theo
> lợi/chi phí + câu thủ sẵn) · file này (thể lệ + nhật ký 6 lượt rà).
>
> **✅ 16/8 — LƯỢT 8, VÒNG 2 PHẢN BIỆN: KHÔNG CÒN PHIẾU TỪ CHỐI.**
> Trung bình soundness **2,9 → 3,6**; trưởng tiểu ban và thống kê đều cho **4,0/nhận**.
> Chi tiết + 10 lỗi vòng 2 (nặng nhất: **`b`/`c` đảo** ở phép kiểm học thuộc, đọc theo
> định nghĩa của chính bài thành *S1 thua 8,4 điểm*) ở `PHAN_BIEN_5_AGENT_DOC_LAP.md`.
> **Hai việc mới làm được, không cần người và không cần GPU:**
> · **Bảng độ nhạy 5 luật chấm** (698 bước): trần 80,2/82,2/74,2/56,6/82,2 · S1−Base
> +12,6/+13,0/+11,7/+9,5/+13,0 ⇒ **mức tuyệt đối trôi 26 điểm nhưng thứ tự không đổi ở
> luật nào**. Bịt đúng đòn chí mạng "bài mô tả một thước, mã chạy thước khác".
> · **Chồng lấn ngôn ngữ dạy–kiểm**: 17,3% câu chuẩn kiểm trùng nguyên văn, 66,5% chung
> 4-gram — trên lát dạy chỉ 2,6%. "Rò rỉ tác vụ = 0" ≠ "rò rỉ cụm từ = 0".
> **⭐ ĐỔI KHUNG BÀI** (user chốt 16/8, không làm chấm người): tên bài từ *"An Instrument
> for Evaluating GUI Instructions Written for Human Readers"* → **"A Reference-Free
> Metric for Element Identification in Generated GUI Instructions"**; bỏ **toàn bộ** lời
> hứa nghiên cứu người; mục Giới hạn đổi thành *Scope of the construct* — nói thẳng
> thước không đo tính trôi chảy/hữu ích, đó là **phạm vi**, không phải món nợ.
>
> **⛔ 16/8 — LƯỢT 7, NĂM PHẢN BIỆN ĐỘC LẬP: `PHAN_BIEN_5_AGENT_DOC_LAP.md`.**
> Một phiếu **từ chối**, bốn sát mép. Không ai bắt được số bịa (hơn 80 đại lượng được
> tính lại, gần như tất cả khớp chữ số cuối), nhưng **8 chỗ bài mô tả sai so với mã/sự
> thật** — đã tự xác minh từng cái và vá hết:
> · ⛔ **bộ trỏ CÓ AndroidControl 47K trong dữ liệu huấn luyện** (Bảng 1 arXiv
> 2410.05243) và **cùng họ Qwen-VL** với mô hình được chấm. Họ dùng split train, ta
> chấm trên split test ⇒ không chồng lấn màn, nhưng còn thiên vị văn phong.
> · ⛔ `history` = **câu chuẩn của người** (100%, 5.318/5.318), không phải nhật ký thao tác
> · ⛔ `hit_disk` là **hộp chữ nhật** (dọc gấp 2,2 lần), Voronoi lấy **g làm hạt**
> · ⛔ "(i),(ii) đúng theo cấu tạo" sai — 3 câu chuẩn rớt luật đảo nghĩa vì thiếu "on"
> · ⛔ **bơm lỗi không gọi bộ trỏ** ⇒ không phản bác được Jandial et al.
> · ⛔ "wild cluster bootstrap" thực ra là bootstrap gom cụm theo cặp
> · **MDE 2,7–4,5 là số đoán; đo được 2,2 pp** ⇒ luật cũ vứt bỏ hiệu ứng thật →
> `report/106` mục sửa đổi **(t)**; chuyện bộ trỏ → mục **(u)**
> · "trần" 75,7% bị **hợp ba nhánh 79,05%** vượt; "lấp 41% khoảng cách" chỉ còn **26%**
> trên các bước mô hình tự viết
> **Đã thay hình:** bỏ đường cong độ nhạy (3 bin n=12/16/21), thêm **hình ca thật**
> (`fig_voronoi.png`) — dòng Birthday, câu mô hình gốc tả nhầm dòng Gender, lệch 128 px
> nên đĩa dung sai vẫn cho đúng còn luật ô thì không. Bỏ 3 bảng lấy chỗ. Vẫn **8 trang**.
>
> **16/8 — lượt 6:** vá lỗi mất 8 dấu tick ở Bảng V (glyph không có trong font) ·
> thêm mục IV-F so với thước tham chiếu · thêm đòn phản biện thứ sáu (học thuộc câu
> chuẩn: bỏ 24,5% bước trùng nguyên văn, S1 vẫn hơn Base **8,4 pp**) · thêm bằng
> chứng chống "chơi thước" (0,04% câu chứa toạ độ, bằng người). Vẫn 8 trang.


Build: `cd paper/fair2026 && tectonic -X compile main.tex --outdir .`
Hiện tại: **8 trang chẵn (đúng trần), 0 lỗi tràn lề, 0 lỗi biên dịch.**

---

## 1. Thể lệ hội nghị — ✅ ĐÃ XÁC MINH TẬN HỆ THỐNG (14/8/2026)

> **CHỐT: nộp qua EDAS `edas.info/index.php?c=35461`, hạn 31/8/2026, track
> `Natural Language Processing`.**
>
> Mâu thuẫn hai nguồn đã được **chính hệ thống phân xử**, không phải suy luận:
> · EasyChair (`easychair.org/conferences/?conf=fair2026`) đăng nhập vào thì báo
> **`Paper submission for FAIR 2026 is closed`** — kênh cũ, đã đóng.
> · EDAS **đang mở**, đủ 7 track, hiện `Register paper by Aug 31` và
> `Review manuscript deadline Aug 31`.
> ⇒ Con số 15/8 của CFP EasyChair **không còn hiệu lực**. Có **17 ngày** tính từ 14/8.
>
> Hệ quả cho nội dung bài: kịp chạy hạt giống 202 + S2 ×2 ⇒ **bảng chính có ablation
> thật thay vì toàn dấu `—`**. Xem lịch ở `CLAUDE.md` khối đầu.

| | CFP trên EasyChair (đã đóng) | **EDAS — kênh thật** |
|---|---|---|
| Hạn nộp toàn văn | ~~15/8/2026~~ | **31/8/2026** |
| Nộp qua | ~~EasyChair~~ đã đóng | **EDAS** (`edas.info/index.php?c=35461`) |
| Kỷ yếu | NXB Khoa học và Công nghệ (VAST), có ISBN | **IEEE Proceedings** |

**Đã chốt thêm 14/8:** không có phản biện ẩn danh ⇒ **giữ khối tên tác giả**. Mẫu là
**mẫu IEEE**; trang hướng dẫn ghi "provided in MS Word format" nhưng link trỏ trang mẫu
IEEE (phát hành cả Word lẫn LaTeX) và EDAS nhận **PDF**, nên bản `IEEEtran` dùng được,
**không phải chuyển sang Word**.

**Tác giả đã điền vào `main.tex`:**
Lê Đoàn Phương Uyên · Faculty of Information Technology · University of Science, VNU-HCM ·
`24C15039@student.hcmus.edu.vn` — và Nguyễn Hồng Bửu Long · cùng đơn vị ·
`nhblong@fit.hcmus.edu.vn`. Tên tiếng Việt render đủ dấu qua tectonic. Mục
`Acknowledgment` đã **bỏ hẳn** (trước đó là `[To be completed.]`, thứ không được lọt vào
bản nộp). Tên tiếng Anh của trường xác minh tại `en.hcmus.edu.vn/overview`.

Nhất quán ở hai nguồn: hội nghị lần thứ **XIX**, ngày **8–9/10/2026**, tại **ĐH Công
Thương TP.HCM**; báo chấp nhận **15/9/2026**; chủ đề chính "Trí tuệ nhân tạo và xu
hướng tương lai" nhưng **không giới hạn nội dung**.

Từ trang hướng dẫn nộp bài (bản gần nhất đọc được — của kỳ 2025, cần kiểm lại cho 2026):
- **Mẫu IEEE, bản MS Word**
- **Tối đa 8 trang**
- **Tối đa 5 từ khoá**
- Bài vào IEEE proceedings phải **tiếng Anh**; bài tiếng Việt phải có tên bài, tóm tắt,
  tên tác giả, đơn vị **kèm tiếng Anh**
- Tên tác giả nhập theo tiếng Việt, không dịch; chỉ định một tác giả liên hệ;
  **tác giả thứ nhất là người trình bày**; bài phải là bài gốc, chưa nộp nơi khác

> ⚠️ **Việc phải làm ngay, tôi không tự làm được:** vào EDAS/EasyChair xác nhận
> (a) hạn thật là 15/8 hay 31/8, (b) mẫu là IEEE hay mẫu riêng của FAIR, (c) có phản
> biện ẩn danh không — nếu **có** thì phải bỏ mọi chỗ tự nhận diện trong bài.
> Bản hiện tại chưa ẩn danh (có ô tên tác giả và đơn vị).

Bản `main.tex` đang dùng `\documentclass[conference]{IEEEtran}`. Nếu FAIR bắt nộp
Word thì vẫn dùng bản này làm bản thảo nội dung rồi chuyển sang Word — nội dung là
phần tốn thời gian, không phải định dạng.

---

## 2. Bài viết gì — và cố ý KHÔNG viết gì

**Trục bài:** đóng góp 2 (đo lường) làm xương sống, kèm quy trình dựng dữ liệu và
thiết kế ablation đã đăng ký trước. Toàn bộ số trong bài đều đã đo.

**Mục VII (Results) nay có ba nhánh thật** (Base 47,6 · S1 59,1 · trần 75,7); các
dòng chưa chạy vẫn để dấu `—`, không có "kết quả sơ bộ cho thấy…", không có số ước.

Ba chỗ trong bài chủ động nêu giới hạn thay vì để phản biện tìm ra:
- **Trần thước 75,7%** *(bản trước ghi 70,0%, đã sửa hết 15/8)* xuất hiện ở tóm tắt, mục IV-D, bảng kết quả và mục giới hạn.
  Mỗi chỗ có điểm số đều nhắc nền 75,7.
- **Bơm lỗi 8/10** luôn đi kèm bảng đầy đủ có **cột n** (có tiêu chí n=755, có
  tiêu chí n=15) và mô tả rõ hai chỗ rớt.
- **Tập kiểm không phải app-unseen** — nêu ở mục III-B, và nói thẳng là phép so
  giữa các nhánh không bị ảnh hưởng còn phép so với mô hình ngoài thì có.

**Ba chữ cấm đã tuân thủ:** không có `first`, `novel`, `new mechanism` cho cả hai lớp
đóng góp. Cụ thể:
- Mục II ghi thẳng rằng đưa danh sách phần tử vào đầu vào **là lựa chọn thiết kế có
  tiền lệ**, và trích chính bài gốc AndroidControl (họ fine-tune với danh sách a11y
  làm input và không dùng screenshot), cộng Mind2Web, Widget Captioning, Screen2Words.
  Câu chốt: *"We therefore make no contribution claim for this layer."*
- Lớp "mô tả phân biệt trước" ghi rõ dòng REG đã chiếm ý từ 2016 (Mao CVPR16, Luo
  CVPR17, Yu CVPR17) và chỉ tuyên bố một khe hẹp: đưa tính phân biệt vào **đích
  huấn luyện** trong miền GUI, cho câu viết cho **người đọc**.
- Câu mở bài phân định với Aguvis: bên họ câu chữ là bước trung gian và **không được
  chấm**; bên mình câu chữ là sản phẩm cuối và là thứ duy nhất đem chấm.

---

## 3. Việc còn thiếu — không tự điền được

| # | Việc | Ghi chú |
|---|---|---|
| 1 | Tên tác giả, đơn vị, email, mục Acknowledgment | đang là chỗ trống |
| 2 | ~~Xác minh tác giả~~ | ✅ **XONG 13/8** — cả 26 tài liệu đã đối chiếu DBLP/Crossref, xem mục 6 |
| 3 | ~~Xác minh venue/năm~~ | ✅ **XONG 13/8** |
| 4 | ~~Hình minh hoạ~~ | ✅ **XONG 13/8** — Hình 1 (đường cong độ nhạy) + Bảng II (ví dụ 4 đích sinh). Nếu muốn thêm hình chụp màn hình thật kèm ô Voronoi thì phải cắt ~0,3 trang |
| 5 | Hạn/format/ẩn danh | xem mục 1 |

---

## 3b. ⭐ SỐ THẬT ĐÃ CÓ (cập nhật 16/8/2026) — ĐÃ CHÈN VÀO BÀI

Nguồn và phân tích đầy đủ: **`report/110` mục 4j-12, 4j-13**. Tệp: `runs/` (có `README.md`).

### Ba nhánh đã chấm, cùng 4.462 bước

| | executable | KTC95 | hit_voronoi | action_ok |
|---|---|---|---|---|
| **Human (trần)** | **75,7%** | [74,1 – 77,3] | 75,8% | 100% |
| **S1 seed 101** | **59,1%** | [57,3 – 60,8] | 60,2% | 94,4% |
| **Base** | **47,6%** | [45,9 – 49,3] | 48,9% | 96,5% |

⛔ **TRẦN 70,0% ĐÃ BỊ RÚT** — đo trên mẫu con 300 bước, thấp hơn 5,7 điểm và nằm ngoài mép
trên KTC của chính nó. Bài **đã sửa xong** ở 5 chỗ: abstract · contribution 2 · mục IV-D ·
bảng `tab:main` · Conclusion. Kéo theo hai số cũng đã sửa: room **741 bước / 16,6 pp** (không
phải 485 / 10,9) và S1 đạt **78,1% của trần** (không phải 84,4%).

### Đã chèn vào bài

- Bảng `tab:main` có dòng **Base 47,6** và **S1 59,1**, trần **75,7 · n=4.462**
- Mục `Baseline Results` viết lại cho ba nhánh + **bảng ghép cặp McNemar**
  (S1−Base +11,5 χ²=243 · Human−S1 +16,6 χ²=580 · Human−Base +28,1 χ²=1.078)
- Tiểu mục mới **"Does the conclusion survive scrutiny?"** — năm đòn phản biện
- Limitations: trần mới · **vùng mù 24,3%** · **phụ thuộc bộ trỏ** · split composition nay có
  số bác bỏ (+14,1 ở app chưa thấy so với +11,9 ở app đã thấy)
- Abstract nhắc cả hai nhánh và "sống sót năm phép kiểm"

Bài vẫn **8 trang chẵn**. Chỗ đã cắt để nhường chỗ: đoạn ô thứ tư của mục III-D, và ba đoạn
được nén lại (ceiling · blind region · robustness).

### ⚠️ Ranh giới không được vượt

⛔ **Cấm viết bất cứ câu nào về hiệu quả của "mô tả trước, phát ngôn sau"** — S2 chưa train.
⛔ **Không được để Base-vs-S1 thay chỗ ablation đã đăng ký** trong cách kể. `report/106` đăng
ký **S1 vs S2**; Base chỉ là nhánh tham chiếu thêm 9/8. Đổi câu hỏi sau khi thấy dữ liệu là
đúng thứ hồ sơ đăng ký trước sinh ra để chặn. Mục "Status of the ablation" phải giữ.
✅ **Được viết:** thước phân giải được hai hệ thống thật (11,5 pp, p<0,001, sống sót 5 đòn) ·
đường ống dữ liệu tự động cho supervision đủ để mô hình 3B đạt 78,1% của trần · thước không
suy biến (ba nhánh trải 47,6→75,7, khoảng tin cậy tách bạch).

### Đang chạy / chưa có

- **`S1` hạt giống 202** — bắt đầu 15/8 21:22 trên A100, dự kiến xong **~21:30 ngày 16/8**.
  Cho **nhiễu giữa hai hạt giống** = null thực nghiệm, cần trước khi khoá ngưỡng.
- **S2 ×2** · ba nhánh chỉ-suy-luận (`--ceiling filler`, `--b-infer`, `--ceiling gold`) —
  chưa chạy.

### Ghi chú cho mục thiết kế thống kê

MDE phải tính theo **ghép cặp (McNemar)**, không phải hai mẫu độc lập: các nhánh chấm trên
cùng tập bước nên chỉ đếm bước bất đồng. Đo được trên cặp Base-vs-S1: SE của hiệu **0,64–0,75
pp** so với 0,94 nếu coi là độc lập ⇒ **MDE 1,8–2,1 pp** chưa cụm, ước **2,7–4,5 pp có cụm**.

---

## 4. Khi có kết quả thì sửa ở đâu

Bài đang **kín đúng 8 trang**, nên điền kết quả vào là phải cắt chỗ khác. Đề xuất
thứ tự cắt, ít mất mát nhất trước:

1. Mục III-D (nhãn khai báo) — bỏ đoạn kể chi tiết ô thứ tư bản đầu: **~0,2 trang**
2. Mục IV-B — gộp bảng chọn luật chấm còn 3 dòng (0%, 8%, SÀN): **~0,1 trang**
3. Bảng II (ví dụ 4 đích sinh) — rút còn s1 và s2: **~0,15 trang**
4. Mục VI — bỏ hẳn câu về 37 lỗi: **~0,05 trang** (đã rút gọn một lần rồi)

Khi điền bảng `tab:main`, **phải giữ dòng cuối** (Human reference = **75,7**) — đó là
điều kiện đọc mọi ô còn lại.

Trình tự cứng của `report/106` mục 5 vẫn áp: chấm s1 hai hạt giống → **MDE thật** →
khoá ngưỡng → mới train S2. Bài không được đi trước trình tự đó.

---

## 5. Quan hệ với luận văn

Bài này ≈ chương đo lường + chương dữ liệu + chương phương pháp của luận văn, nén lại
và dịch sang tiếng Anh. Dịch ngược sang tiếng Việt cho luận văn thì phần lập luận
dùng lại được gần như nguyên; chỗ phải viết dài thêm là mục III (dữ liệu) và mục IV-F
(lực thống kê), vì trong luận văn không bị ép 8 trang.

Không trùng với `report/104`/`report/111` (script trình thầy) — hai file đó là bản
nói, file này là bản viết.


---

## 6. Xác minh danh mục tài liệu (13/8/2026) — đối chiếu DBLP + Crossref

Không dùng trí nhớ. Mỗi mục tra thẳng `dblp.org/search/publ/api`; riêng GuideMe tra
`api.crossref.org` theo DOI. **26/26 mục đã đối chiếu.** Năm lỗi bắt được:

| Lỗi trong bản đầu | Sự thật |
|---|---|
| `[AUTHORS TO VERIFY]` ở 2 mục | **GuideMe** = Kairong Fang, Jiesi Zhang, Shi-Ting Ni, Pan Hui, Yuyang Wang, *"GuideMe: A VLM-Based System Assisting Independent Smartphone Learning for Older Adults"*, CHI 2026. **EACL** = Surgan Jandial, Yinheng Li, Justin Wagle, Kazuhito Koishida |
| Ghi *"Findings of the ACL: EACL"* mà chưa chắc | DOI `10.18653/v1/2026.findings-eacl.144` → **đúng là Findings**, không phải main track |
| `W. Bishop` | **W. E. Bishop** (bản NeurIPS 2024; bản arXiv ghi `W. W. Bishop` — hai bản khác nhau) |
| AITW ghi *"Android in the Wild"* | Tên trong kỷ yếu NeurIPS 2023 là **"AndroidInTheWild"** (viết liền) |
| UI-R1 ghi *"Enhancing action prediction"* | Tên đầy đủ: *"Enhancing **Efficient** Action Prediction of GUI Agents by Reinforcement Learning"*, AAAI 2026, doi `10.1609/AAAI.V40I21.38816` |

Xác nhận đúng như hồ sơ đã ghi: AndroidControl NeurIPS'24 · SeeClick ACL'24 ·
OS-Atlas ICLR'25 · UGround ICLR'25 · Aguvis ICML'25 · GUI-Actor NeurIPS'25 ·
Mind2Web NeurIPS'23 · Widget Captioning EMNLP'20 · Screen2Words UIST'21 ·
Mao CVPR'16 · Luo CVPR'17 · Yu CVPR'17 · ALOHa NAACL'24 (Short) · Sai EMNLP'21 ·
Clark ACL-IJCNLP'21 · Chen ICSE'20 · QLoRA NeurIPS'23 · LlamaFactory ACL'24 Demos.
Qwen2.5-VL chỉ có bản arXiv — đã để nguyên dạng technical report, **không** xếp
chung hàng bình duyệt.

## 7. Về mấy skill viết paper trên mạng — đã tra, KHÔNG dùng

Ứng viên tra được: `Imbad0202/academic-research-skills` (Deep Research 13 agent +
Academic Paper 12 agent + Reviewer 7 agent + Pipeline 10 chặng), *Academic LaTeX
Paper Drafter*, *Claude Scholar*, *Paper Writing pipeline*.

**Chưa cài cái nào, và khuyên không cài**, ba lý do:

1. **Thứ đáng giá nhất của chúng đã làm xong bằng tay, và làm chuẩn hơn.** Điểm bán
   chính là "verify citation qua Semantic Scholar / OpenAlex / Crossref". Mục 6 ở
   trên làm việc đó qua **DBLP** — chỉ mục chuyên ngành máy tính, chính xác hơn hẳn
   cho tên hội nghị (Crossref không phân biệt Findings với main track; DBLP có DOI
   phân biệt được, và đó chính là chỗ vừa bắt lỗi).
2. **Nguy hiểm đúng ở chỗ dự án này sợ nhất.** Chúng là bộ sinh bài tổng quát,
   không biết ràng buộc của mình: chưa có điểm executability · trần thước 70 · cấm
   chữ "đầu tiên"/"mới" · danh sách số đã bị rút. Một agent viết bài không biết mấy
   luật đó sẽ điền Bảng VI bằng số nghe hợp lý — đúng loại lỗi mà `report/108` mục 8
   ghi 37 lần.
3. **Sai thể loại.** Chúng mặc định APA/luận văn dài; bài này là IEEE 8 trang. Và
   `Academic Paper Reviewer` chấm điểm 0–100 theo rubric chung, không thay được việc
   đọc đối chiếu với `report/106`/`108` — mà đó mới là phản biện thật của bài này.

Thứ duy nhất đáng mượn từ chúng là **ý tưởng có một lượt phản biện đối kháng**; đã
làm bằng tay, kết quả ở mục 8.

## 8. Kết quả review lượt 2 (13/8) — đã sửa

**Văn phong** (đếm bằng script, so bản đầu → bản hiện tại):

| | bản đầu | hiện tại |
|---|---|---|
| `rather than` | 20 | **2** |
| `instead of` | 9 (sau khi sửa lần 1) | **4** |
| gạch ngang dài `---` | 33 | **1** |
| tóm tắt | 284 từ | **244** |
| tên mục dạng câu hỏi | 3 | **0** |
| hình | 0 | **1** |
| ví dụ dữ liệu cụ thể | 0 | **1 bảng** |

Đã đổi: mở bài kiểu tạp chí → bối cảnh + khe hở + **danh sách 4 đóng góp đánh số**
(đúng quy ước bài IT); tên mục → cụm danh từ; bỏ kiểu in đậm dẫn đoạn giữa thân bài;
bỏ đoạn kể "37 lỗi… ba thói quen" (sai thể loại) còn 2 câu đặt trong mục Tái lập.

**Bốn lỗ nội dung phản biện sẽ hỏi ngay, đã vá:**

1. **Chống vòng lặp.** Thêm đoạn ở mục IV-A: bộ trỏ khác họ mô hình được chấm, không
   tinh chỉnh trên dữ liệu của mình, không thấy `g`; và **vì mọi nhánh dùng chung một
   bộ trỏ nên thiên lệch của nó là thiên lệch chung, triệt tiêu phần lớn trong hiệu
   số giữa các nhánh** — đây là lập luận mạnh nhất mà bản đầu bỏ sót.
2. **Vì sao không lấy chấm người làm thước chính.** 4.463 bước × 8 nhánh; chấm người
   100 câu hai người là **kiểm chéo**, không phải bản thay thế.
3. **Không có ví dụ dữ liệu.** Thêm Bảng II: cùng một đầu vào, bốn đích sinh s1 / s2 /
   s2r / s2\_nopoint. Ghi rõ là ví dụ minh hoạ.
4. **Hình.** Thêm Hình 1: đường cong độ nhạy hai luật chấm theo sai số bộ trỏ, vẽ từ
   số đo thật (n = 188/21/16/12/63). Hình này cho thấy ngay vì sao đĩa dung sai vô
   dụng — nó cho 100% cả ở mức lệch 8–14%.

**Rủi ro còn lại, không sửa được bằng cách viết:** bài không có kết quả mô hình. Tôi
đã đóng khung mục VII thành *"Status of the Ablation Study"* và đưa phần đặc tả dụng
cụ lên làm kết quả thật của bài, nên bài đứng được như một **bài phương pháp đo
lường**. Nhưng nếu phản biện tìm bảng số so sánh mô hình thì vẫn không có. Cách duy
nhất giảm rủi ro này là chấm xong s1 hai hạt giống trước hạn nộp.


---

## 9. Rà lượt 3 (13/8) — đối chiếu bài với MÃ và DỮ LIỆU, không đối chiếu với report

Chi tiết đầy đủ: **`KIEM_LAI_MA_VA_DU_LIEU.md`**. Tóm tắt:

**Tái lập được, khớp tới chữ số cuối (18 khẳng định):** cỡ tập kiểm · tỉ lệ
không-chạm · G / G hiệu dụng / số app / cụm lớn nhất · cổng A (trung vị, p75, cả 5
phân vị, 5 dải sai số) · trần thước và hai khoảng tin cậy · 10 ngưỡng bơm lỗi · số
tham số LoRA · lưới toạ độ · cổng hình học · phân bố nhãn lát thử · bán kính gộp
63,07 px · siêu tham số.

**Ba lỗi bắt được, đã sửa:**
1. Bảng ví dụ do tôi bịa và **bịa sai ngôn ngữ** — nhãn thật là tiếng Việt. Thay bằng
   bản ghi thật, thêm khai báo scaffold song ngữ.
2. **Định nghĩa thước trong bài không khớp `metric_exec.py`** — thiếu điều kiện chống
   đảo nghĩa, và Voronoi thật ra **vẫn đòi nằm trong đĩa 14%** nên là bản siết chặt
   của luật quy ước, không phải phương án thay thế. Sửa xong bài mạnh hơn.
3. Lập luận ngưỡng 3% dùng số của mẫu **n=76**; thay bằng phép đo 1.496 bước đã có
   trong bản đăng ký.

**Văn phong, đo lượt 3:** câu trung vị **33 → 24 từ**, câu dài >35 từ **62 → 37**,
câu ngắn <12 từ **8 → 33**, biến thiên độ dài đoạn CV **0,47** (dưới 0,35 mới là
đều bất thường kiểu máy sinh).

## 10. ~~QUYẾT ĐỊNH CÒN TREO~~ — ĐÃ CHỐT 14/8: nhãn đổi sang TIẾNG ANH

**Đã làm:** sửa `descriptor_label_build.py` (chỉ chuỗi xuất ra), dựng lại lát 1.697
bước, đối chiếu từng trường với bản cũ — **đúng 4 trường đổi** (`desc`/`role`/`hint`/
`desc_neg`), **17 trường giữ nguyên 100%**, phân bố nhãn trùng khít, **0 ký tự tiếng
Việt còn lại**. Ghi mục sửa đổi **(q)** vào `report/106`. Bài FAIR nay **không còn
ký tự tiếng Việt nào**.

**Còn phải làm trước khi train s2:** dựng lại nhãn + 4 nhánh ở **quy mô đủ trên
Colab** (ô 0.10 → 0.11) rồi chạy lại 9 bất biến và phép ghép token của S2r. Lát ở máy
nhà chỉ chứng minh được thay đổi là thuần từ vựng.

**Không phải train lại s1** — đích của s1 là câu trơn, không chứa khai báo.

**Một thứ cố ý GIỮ tiếng Việt:** câu nhắc đưa vào mô hình (`SYS` + nhãn trường
*Mục tiêu / Đã làm / Chữ đọc được trên màn*). Nó **giống hệt ở mọi nhánh và ở cả khâu
chấm**, nên là hằng số, không giải thích được chênh lệch giữa các nhánh; đổi thì phải
train lại s1 (~24 giờ, ~$12) mà không mua được tính hợp lệ nào. Bài đã khai thẳng ở
mục V-A.

<details><summary>Lập luận gốc khi còn treo (giữ để tra)</summary>

### (bản cũ) ngôn ngữ của nhãn khai báo

Phát hiện ở mục 9 kéo theo một câu hỏi thiết kế, **không phải câu hỏi trình bày**:
đích huấn luyện của s2 là *khai báo tiếng Việt* rồi mới tới *câu tiếng Anh*. Nghĩa là
s2 khác s1 ở **hai** thứ cùng lúc: có khai báo, và có chuyển ngữ.

- Phần **khử được**: s2r cũng là khai báo tiếng Việt ⇒ hiệu `s2 − s2r` không dính yếu
  tố ngôn ngữ. Bài đã viết đúng câu này.
- Phần **không khử được**: hiệu `s2 − s1` — tức con số headline — vẫn lẫn yếu tố
  chuyển ngữ.
- Thêm rủi ro thực thi: mô hình 3B phải sinh từ vựng vai trò tiếng Việt (`chữ bấm
  được`, `hình/biểu tượng`) mà nó ít gặp, rồi chuyển sang tiếng Anh.

**Chưa train s2 nên vẫn đổi được**, và đây là thời điểm hợp lệ duy nhất — `report/106`
mục sửa đổi 11/8 (o) đã có tiền lệ: đổi `cutoff_len` trước lượt train đầu. Ba đường:

| | Làm gì | Giá |
|---|---|---|
| **A. Giữ nguyên** | khai vào Giới hạn (bài đang thế) | 0. Đổi lại: headline có confound phải khai suốt |
| **B. Đổi nhãn sang tiếng Anh** | dựng lại `descriptors.jsonl` + 4 nhánh, ghi mục sửa đổi | vài giờ CPU, **không tốn tiền card**; s1 đang chạy không phải train lại vì s1 không có khai báo |
| **C. Giữ tiếng Việt, đổi headline** | lấy `s2 − s2r` làm phép so chính thay cho `s2 − s1` | 0 tiền, nhưng `report/106` mục 6 đã khoá headline là `s2 − s1` ⇒ đổi là đụng thiết kế đã niêm phong |

Tôi nghiêng về **B**: rẻ, làm trước khi có bất kỳ điểm số nào nên hợp lệ tuyệt đối,
và xoá hẳn một confound khỏi con số headline. Nhưng đây là quyết định của bạn, không
phải của tôi — nó đụng bản đăng ký trước.


</details>


---

## 11. Rà lượt 5 (15/8) — template IEEE và văn phong

### 11.1. LỖI TEMPLATE, đã sửa

Log biên dịch báo `Font shape TU/ptm/... undefined — defaults substituted`. Nghĩa là
**PDF không hề dùng font Times mà mẫu IEEE yêu cầu**: dưới XeTeX, các họ font cũ
`ptm` (Times) và `pcr` (Courier) không dựng được nên LaTeX âm thầm thay bằng
Computer Modern. Nhìn PDF thì vẫn "đẹp", nên rất dễ nộp mà không biết.

Đã vá bằng `fontspec` + họ **TeX Gyre** (cùng metric với Times/Helvetica/Courier, và
Termes có đủ dấu tiếng Việt cho tên tác giả), rồi `unicode-math` +
`texgyretermes-math` cho phần công thức — vì sau khi vá chữ, **toàn bộ số trong bài
vẫn là Computer Modern** (`$59.1\%$`, `$[57.3, 60.8]$`…), lệch hẳn kiểu chữ so với
thân bài.

Kiểm bằng cách bung stream trong PDF ra đọc `/BaseFont`:

| | trước | sau |
|---|---|---|
| Font chữ | Computer Modern (thay ngầm) | **TeXGyreTermes** Regular/Bold/Italic/BoldItalic |
| Font công thức | CMR · CMMI · CMSY · MSAM | **TeXGyreTermesMath** |
| Font mã | — | **TeXGyreCursor** |
| Khổ giấy | | **8,5 × 11 inch (US Letter)** ✅ |

### 11.2. Đối chiếu thể lệ

| Yêu cầu | Bản nộp |
|---|---|
| Mẫu IEEE conference | `\documentclass[conference]{IEEEtran}` ✅ |
| Tối đa 8 trang | **8** ✅ |
| Tối đa 5 từ khoá | **5** ✅ |
| Tiếng Anh | ✅ — tiếng Việt chỉ còn ở **tên hai tác giả**, đúng yêu cầu giữ nguyên không dịch |
| Nộp PDF qua EDAS | PDF hợp lệ, US Letter, font nhúng đủ ✅ |

### 11.3. Văn phong sau lượt 5

| | lượt 1 | nay |
|---|---|---|
| câu trung vị | 33 từ | **22** |
| câu <12 từ | 8 | **40** |
| gạch ngang dài | 33 | **0** |
| `rather than` | 20 | **1** |
| tóm tắt | 284 từ | **~250** |

Sửa nội dung trong lượt này: mục Results viết *"Three observations"* nhưng liệt kê
**bốn** mục — sai đếm, đã sửa. Đổi tên mục VII thành **"Baseline Results"** (tên cũ
"First Measurement" không phải cách đặt của bài IEEE). Kết luận tách làm hai đoạn,
bỏ câu mở đầu liệt kê 5 vế. Bỏ cụm vụng *"reported alongside as throughout"*,
*"on free GPU quota"*.

---

## 12. Rà lượt 6 (16/8) — theo chuẩn "bài thuyết phục" + phản biện 5 giám khảo

Kết quả chấm đầy đủ: **`PHAN_BIEN_5_GIAM_KHAO.md`**.

### 12.1. Một lỗi template nữa, cùng lớp với lỗi font lượt 5

`\checkmark` (U+2713) **không có trong TeX Gyre Termes** → LaTeX lặng lẽ bỏ ký tự,
nên **8 dấu tick của Bảng V biến mất khỏi PDF**: bảng bơm lỗi hiện ra với 2 dấu ×
và 8 ô trống, đọc thành "8 tiêu chí không có kết quả" — ngược hẳn ý (8/10 đạt).
Cảnh báo chỉ nằm trong log (`Missing character`), nhìn PDF không thấy.
Đã thay bằng chữ `PASS` / `FAIL` (small caps), không phụ thuộc glyph.

Đối chiếu thể lệ lại: trang chủ `fair.conf.vn` ghi **hạn 31/8**, **6–8 trang**, mẫu
IEEE, kỷ yếu IEEE, nộp EDAS. Bản hiện tại: 8 trang · US Letter · 5 từ khoá · font
Termes/Cursor/TermesMath (không còn Computer Modern) · 0 tràn lề · 0 tham chiếu treo
· 0 bảng mồ côi · 23 tài liệu.
⚠️ CFP cũ trên EasyChair vẫn ghi 15/8 — **phải vào EDAS xác nhận hạn trước khi nộp**.

### 12.2. Ba thứ thêm vào bài, đều từ dữ liệu đã có (0 đồng)

1. **Mục IV-F "What a reference-based score would conclude"** — lấp lỗ *"thước mới
   không so với thước nào"*, lỗi rớt bài kinh điển của bài đề xuất thước. Đo trên
   chính `runs/*_raw.jsonl`: trong 2.124 câu Base mà executability chấp nhận,
   **52,8% bị F1 tham chiếu cho dưới 0,5** (S1 chỉ 13,9%) ⇒ thước tham chiếu không
   chỉ ồn mà **lệch giữa hai nhánh**, vì fine-tune kéo câu về giọng annotator.
2. **Đòn phản biện thứ sáu — học thuộc câu chuẩn.** 1.095/4.462 câu S1 (24,5%) trùng
   nguyên văn (từ nội dung) câu chuẩn. Bỏ hết nhóm đó, S1 **vẫn hơn Base 8,4 pp**
   (b=547, c=264, χ²=98,1, p<0,001); trên nhóm trùng thì chênh +21,1. ⇒ một phần lợi
   ích là giọng annotator, **nhưng kết luận không dựa vào đó**.
3. **Bằng chứng chống "chơi thước"** — S1 sinh chuỗi toạ độ ở **0,04%** số câu, đúng
   bằng tỉ lệ của câu người; từ chỉ vị trí 26,8% so với 26,4%. Đặt trong mục
   Limitations mới *Construct validity*.

Sửa thêm: trần **không còn được gọi là cận trên** (một hệ có thể vượt bằng cách viết
cho máy trỏ) · giải thích hằng số 2,8 = z₀,₉₇₅+z₀,₈₀ · biện minh quy tắc cụm ·
ghi rõ 84,3% trần-đĩa trùng 84,3% sàn-đĩa là **trùng ngẫu nhiên** · bỏ chữ `first`
khỏi đóng góp 5 · giả định mật độ 2,625 cho 24 dp.

Kiểm lại toàn bộ số của mục VII từ `runs/*_raw.jsonl`: **khớp tới chữ số cuối** —
59,12 / 47,60 / 75,73 · McNemar b/c/χ² cả ba cặp · 1.824 lỗi trong đó 251 sai thao
tác · 935 bước cả ba cùng trượt. Bản ghi bị bỏ đúng **1** (S1 sinh câu rỗng), nên
n=4.462 như bài ghi.

### 12.3. Chỗ đã cắt để giữ đúng 8 trang

Thêm ~45 dòng nên phải cắt tương đương: bảng ví dụ 4 đích sinh → ví dụ nội dòng ·
bảng chẩn đoán (trùng với văn) → bỏ, số đưa vào câu · danh mục tài liệu rút theo
đúng quy ước IEEE (>6 tác giả dùng *et al.*, viết tắt tên hội nghị) · nén III-C,
III-D, V-A, VI, Limitations.

### 12.4. Văn phong sau lượt 6

câu trung vị **24 từ** · câu <12 từ **38** · gạch ngang dài **1** · `rather than`
**3** · tóm tắt ~245 từ. Không có cụm máy móc (`furthermore`, `moreover`,
`comprehensive`, `crucial`, `delve`, `it is important to note`) — đếm bằng script.

---
