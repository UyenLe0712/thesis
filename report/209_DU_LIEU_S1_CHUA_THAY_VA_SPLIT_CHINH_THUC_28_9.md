# 209 — Dữ liệu S1 chưa thấy, và tập kiểm của dự án so với split chính thức của AndroidControl (28/9/2026)

Câu hỏi ban đầu (sau khi P2 của FGRB trượt, `report/207` §11): AndroidControl còn tác vụ nào S1
**chưa thấy** để train/đo lại FGRB mà không phải train lại S1 không. Khi đối chiếu với split chính
thức thì lộ thêm một chuyện lớn hơn (§2), ảnh hưởng tới một câu trong luận văn.

Mọi số ở đây đo 0 GPU trên WSL. Tái lập: `~/.venvs/thesis/bin/python harness/kiem_split_chinh_thuc.py`
→ `runs/split_chinh_thuc/ket_qua.json`. Split chính thức tải 28/9 từ
`https://storage.googleapis.com/gresearch/android_control/splits.json` (Li et al., NeurIPS 2024 D&B),
lưu ở `runs/split_chinh_thuc/splits.json`. Nhãn: [đo] = đo trong kho · [suy] = suy luận chưa kiểm.

## 1. Tác vụ S1 chưa thấy: có 956 tác vụ, 3.113 bước — nhưng chưa có ảnh [đo]

| | tác vụ | bước |
|---|---|---|
| toàn kho câu hướng dẫn (`HarrytheOrange/parsed_AndroidControl`) | 15.283 | 83.848 |
| tập dạy của dự án (`train_ac/train.jsonl`) | 12.895 | 64.567 |
| tập kiểm của dự án (`test_ac/test.jsonl`) | 1.432 | 6.958 |
| giao dạy ∩ kiểm | 0 | – |
| **còn lại — S1 chưa thấy** | **956** | **3.113** |

Phần còn lại theo loại thao tác: click 1.484 · scroll 1.351 · wait 104 · navigate_back 84 ·
input_text 52 · open_app 36 · long_press 2. Theo split chính thức: 890 tác vụ train · 55 test · 11 validation.

**Vì sao chưa có ảnh:** tập dạy và tập kiểm đều dựng bằng cách ghép câu của `HarrytheOrange` với
ảnh của `ckg/AndroidControlParsedWithImages-20k` (`build_train_data.py` đọc 76 shard `train-*`,
`build_test_data.py` đọc 9 shard `test-*`). 956 tác vụ này có câu nhưng không nằm trong hai phần đó.
Ảnh gốc có trong bản TFRecord của AndroidControl; trên HuggingFace, `reece124/android_control` có đủ
**20 shard, 49,9 GB** (máy nhà đang có sẵn shard 00000, 2,49 GB). Chưa kiểm 956 tác vụ nằm ở shard
nào, việc đó cần quét cả 20 shard.

**Có dùng cho FGRB được không [suy]:** về cỡ thì được (1.484 bước chạm, cùng cỡ với lượt P2 đã chạy:
4.000 bước train, 1.567 bước val). Nhưng phải tách tiếp thành phần train và phần đo, nên mỗi phần chỉ
còn khoảng 700–1.500 bước. Và `report/207` §11 đã chỉ ra CE của S1 trên dữ liệu đã thấy vẫn còn chỗ
giảm (0,5–0,7/token) mà FGRB không dùng được ⇒ đổi sang dữ liệu chưa thấy **chưa chắc** làm cổng tiêm
mở ra. Chi phí: quét 50 GB TFRecord trên Kaggle CPU (0 đồng, vài giờ) + một lượt P2 mới (~5 h T4).

## 2. ⚠️ Tập kiểm của dự án KHÔNG phải split test chính thức [đo]

| split chính thức | số tác vụ | nằm trong tập dạy của dự án | nằm trong tập kiểm của dự án | còn lại |
|---|---|---|---|---|
| train | 13.603 | 11.426 | **1.287** | 890 |
| validation | 137 | 112 | 14 | 11 |
| test | 1.543 | **1.357** | 131 | 55 |

- **90% tác vụ trong tập kiểm (1.287/1.432) thuộc split *train* chính thức.** Tính theo bước chạm:
  3.994/4.463 bước (89,5%) thuộc split train, 469 bước thuộc test + validation.
- Ngược lại, 1.357 tác vụ của split *test* chính thức nằm trong **tập dạy** của dự án.
- Tập kiểm của dự án là **mẫu ngẫu nhiên theo tác vụ, độc lập với split chính thức**: nếu chọn ngẫu
  nhiên 1.432 tác vụ thì kỳ vọng rơi 1.274,6 / 12,8 / 144,6 vào train / validation / test; đo được
  1.287 / 14 / 131. Khớp tỉ lệ này cũng là phép kiểm cho thấy mã tác vụ của `splits.json` và của
  `HarrytheOrange` cùng một hệ đánh số (0/15.283 mã lệch).
- Nguồn gốc: `ckg/AndroidControlParsedWithImages-20k` tự chia train/test của riêng họ; dự án lấy
  nguyên cách chia đó. Tính hợp lệ **bên trong** không đổi: dạy ∩ kiểm = 0 tác vụ.

**Hệ quả với luận văn.** `thesis/chapters/ch5_thuocdo.tex:162–163` viết: UGround lấy 47 nghìn nhãn
AndroidControl *"từ split train"*, còn *"tập kiểm của luận văn tách rời ở mức màn hình nên đây không
phải rò rỉ nhãn"*. **Vế sau không còn đúng.** 90% bước kiểm thuộc chính split train mà UGround lấy dữ
liệu, nên có thể UGround đã thấy một phần màn hình của tập kiểm. Tôi chưa kiểm được UGround lấy đúng
những tác vụ nào trong split train. `CLAUDE.md` mục *GIỚI HẠN CÒN MỞ* chép lại cùng câu sai đó.
Bản sao lưu `paper/fair2026/main_v1_metric_backup.tex` cũng có câu này; grep `main.tex` của FAIR, VCL,
SOICT, GUIStep không thấy.

## 3. Nhưng số đo không thiên về các bước UGround có thể đã học [đo]

exec (Voronoi .14) tách theo split chính thức của bước, KTC95 bootstrap theo tác vụ (1.000 lần, seed 101):

| nhánh | bước thuộc split train (n=3.994, 1.205 tác vụ) | bước thuộc split test+val (n=469, 140 tác vụ) |
|---|---|---|
| câu chuẩn | 75,94 [74,3; 77,5] | 73,99 [69,9; 78,6] |
| S1/101 | 59,09 [57,2; 60,8] | 59,28 [53,9; 64,5] |
| S1/202 | 59,44 [57,7; 61,2] | 61,19 [55,9; 65,9] |
| MIN/101 | 59,76 [58,1; 61,5] | 62,47 [57,2; 67,7] |
| Base | 47,70 [45,9; 49,3] | 46,70 [41,9; 51,8] |

- Mọi cặp KTC chồng lên nhau; bốn nhánh mô hình còn nhỉnh hơn ở phần test+val. Không có dấu hiệu
  bộ trỏ chấm dễ hơn trên màn thuộc split train.
- Câu chuẩn thấp hơn 1,95 điểm ở phần test+val, trong khoảng nhiễu (n=469).
- Cộng với phép B (`CLAUDE.md`, UI-Venus-7B không học AndroidControl giữ 94% phép so S1 − Base),
  **mọi con số đã công bố vẫn đứng**. Phải sửa là **câu mô tả**, không phải số.
- ⚠️ Phần test+val chỉ 469 bước ⇒ phép so này chỉ loại được chênh lệch lớn (cỡ ≥5 điểm), không loại
  được chênh lệch 1–2 điểm.

## 4. Việc cần làm (chưa làm, chờ user)

1. **Sửa câu ở `ch5_thuocdo.tex:162–163`**: bỏ *"tách rời ở mức màn hình nên không phải rò rỉ nhãn"*,
   thay bằng: tập kiểm là mẫu ngẫu nhiên theo tác vụ, 90% thuộc split train chính thức, và exec tách
   theo split không cho thấy chênh lệch (bảng §3). Cập nhật cùng ý ở mục *GIỚI HẠN CÒN MỞ* của `CLAUDE.md`.
2. Mọi chỗ trong luận văn/bài có gọi tập kiểm là *"test split"* của AndroidControl phải ghi rõ là
   *"tập giữ riêng theo tác vụ, chia theo bản trích `ckg`"*. `03_trangthongtin.tex:163` (tóm tắt EN)
   chỉ nói *"no task overlap between the training and test splits"* — câu này **vẫn đúng**.
3. Nếu vẫn muốn thử FGRB trên dữ liệu S1 chưa thấy: quét 20 shard `reece124/android_control` trên
   Kaggle CPU để lấy ảnh cho 956 tác vụ (§1). Theo `report/207` §11 và nhận định 28/9, khả năng FGRB
   ra số vẫn thấp [suy]; khuyến nghị hiện hành là phương án `report/208` (C1 đang chạy).
