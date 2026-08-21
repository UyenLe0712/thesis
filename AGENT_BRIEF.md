# Đọc file này trước — brief cho người/agent được mời phản biện

Kho này là luận văn thạc sĩ đang làm dở. Chủ đề: **sinh câu hướng dẫn thao tác giao diện từ
ảnh màn hình**, và **một thước đo không cần câu tham chiếu** để chấm câu sinh ra.

Việc cần ở bạn: đọc, hiểu, rồi **phản biện thật** — chỗ nào lập luận hở, chỗ nào số không
đỡ nổi kết luận, chỗ nào có lời giải thích thay thế chưa bị loại. Sau đó góp ý về pipeline,
về thước đo, và về việc nên làm gì tiếp trong quỹ thời gian còn lại.

⚠️ **Trước khi nêu một đòn, đọc mục 4.** Dự án đã qua bốn lượt phản biện độc lập; những đòn
hiển nhiên đều đã bị đánh bằng số đo. Nêu lại chúng không giúp được gì.

---

## 1. Đọc theo thứ tự này

| # | file | trả lời câu gì |
|---|---|---|
| 1 | `README.md` | kho có gì ở đâu |
| 2 | `report/112_HIEU_TOAN_BO_KY_THUAT.md` | cơ chế toàn bộ, từ đầu — **file dày nhất, đáng nhất** |
| 3 | `report/109_BAN_DO_HIEN_TAI.md` | đang ở đâu |
| 4 | `report/106_DANG_KY_TRUOC.md` | thiết kế đã khoá trước khi có điểm + 27 mục sửa đổi |
| 5 | `report/108_DA_LAM_DUOC_GI.md` | số nào tin tới đâu, **số nào đã bị rút và vì sao** |
| 6 | `CLAUDE.md` | nhật ký quyết định, trạng thái mới nhất |
| 7 | `harness/metric_exec.py` | thước đo, **đọc mã chứ đừng đọc mô tả** (xem mục 5) |

Mâu thuẫn giữa các file thì: `106` thắng về *phải làm gì* · `108` về *đã đo được gì* ·
`109` về *đang ở đâu* · `112` về *cơ chế hoạt động*.

## 2. Tóm tắt để bạn có chỗ bấu

**Bài toán.** Cho ảnh màn hình + mục tiêu người dùng, sinh câu kiểu *"Nhấn nút Tiếp tục ở góc
dưới phải"*. Câu đúng ngữ pháp mà gọi sai tên nút thì vô dụng — nên thước đo không hỏi *"câu
này giống câu mẫu bao nhiêu"* mà hỏi **"đưa câu này cho một mô hình định vị, nó có bấm trúng
chỗ không"**. Đó là `executability`.

**Bốn nhánh đã chấm** (mẫu số 4.463 bước chạm, bộ trỏ UGround):

| nhánh | executability |
|---|---|
| câu chuẩn do người viết (trần) | **75,7%** |
| S1 — fine-tune thường (hạt giống 202 / 101) | **59,6 / 59,1%** |
| S2 — mô tả phần tử trước, câu sau (hạt 101) | **57,2%** |
| mô hình gốc chưa fine-tune (Base) | **47,6%** |

**Kết quả bất lợi và dự án không giấu:** S2 là đóng góp chính về mặt mô hình, và nó **thua S1**
(−1,93 pp, KTC95 [−3,06 · −0,75]). Đây là một trong bốn kết cục đã đăng ký trước.

## 3. Tự kiểm số, đừng tin bảng

Kho giữ nguyên tệp thô nên **bạn tính lại được mà không cần GPU**:

```bash
python3 harness/phan_tich_s2.py        # S2 vs S1, ghép cặp McNemar, lát cắt
python3 harness/phan_tich_venus.py     # đổi bộ trỏ sang UI-Venus, đọc lại toàn bộ
python3 harness/phep_a_ghep_cap.py     # phép diễn đạt lại
python3 harness/mde_that.py            # cỡ hiệu ứng nhỏ nhất phát hiện được
python3 harness/rule_sensitivity.py    # đổi luật chấm, xem thứ hạng có đổi không
```

Dữ liệu: `runs/*.jsonl` (câu sinh ra + kết quả chấm từng bước), `harness/dg1_cache/test_ac/test.jsonl`
(tập kiểm 6.958 bước, có câu chuẩn của người). **Ảnh màn hình không nằm trong kho** (~8 GB,
dựng lại bằng `harness/build_test_data.py`) — nên chạy lại bộ trỏ thì cần tải ảnh trước, còn
tính lại thống kê từ tệp thô thì không cần gì thêm.

Nếu bạn tìm ra số nào trong tài liệu không khớp với số bạn tính lại được, **đó là phát hiện
đáng giá nhất bạn có thể mang lại** — dự án đã tự rút 8 con số theo cách đó.

## 4. Đã bị bác bằng số — đừng nêu lại

| đòn | vì sao chết |
|---|---|
| *"thước dễ ăn điểm, sàn chắc khoảng 40%"* | đo thật: câu rỗng `"Tap the button."` chỉ được **12,0%** |
| *"bộ trỏ chấm cao vì quen văn phong, không thật sự đọc câu"* | câu **thật của bước khác** (văn phong hoàn hảo, sai màn) được **6,1%** — *thấp hơn cả câu rỗng*, hai KTC không chồng lấn |
| *"bộ trỏ đã thấy AndroidControl nên thiên vị S1"* | chấm lại toàn bộ bằng **UI-Venus-Ground-7B** (sạch AndroidControl): chứng nhân S1−Base giữ **94%** (+10,35 → +9,68 pp) |
| *"đổi cách diễn đạt là điểm sập"* | 1.139 câu viết lại giữ nghĩa: hiệu ròng **+0,35 pp**, KTC95 [−0,59 · +1,29] |
| *"thước ưu ái văn máy hơn văn người"* | câu người đạt **75,7%**, cao hơn mọi nhánh máy |
| *"mô hình chỉ thắng trên app đã thấy khi huấn luyện"* | app đã thấy **59,1%** vs chưa thấy **59,0%** |
| *"kết quả phụ thuộc thứ tự chạy hay cách gom lô"* | tất định: **0 bất đồng trên 1.625 phép so**, bốn lượt độc lập |
| *"đổi luật chấm là đổi kết luận"* | năm luật khác nhau: trần trôi 56,6→82,2% nhưng **thứ tự ba nhánh không đổi ở luật nào** |

## 5. Ba cái bẫy đã làm dự án này mất nhiều ngày

**① Đọc mã, đừng đọc mô tả.** Tài liệu từng tả sai chính thước đo của mình ba lần: `hit_disk`
thực ra là **hình chữ nhật** (dung sai dọc rộng gấp 2,2× ngang) chứ không phải đĩa Euclid; hạt
Voronoi là **chính điểm chạm** chứ không phải tâm phần tử; và `hit_voronoi` **bao gồm** luật
đĩa nên hai luật đó không ngang hàng. Muốn biết thước làm gì thì mở `harness/metric_exec.py`.

**② Mở nguồn, đừng mở ghi chú.** Hai khẳng định về bộ trỏ sống 18 ngày, đi vào bản thảo, rồi
bị lật bởi một lần mở đúng Bảng 1 của bài gốc. Chữ *"đã xác minh"* trong ghi chú không phải
bằng chứng. Mọi lỗi bắt được đều sinh ra ở khâu **tóm tắt một nguồn thành câu ngắn cho tiện
trích**, rồi câu ngắn sống nhiều tuần vì không ai mở lại nguồn.

**③ Kết quả trùng nhau tới nhiều chữ số giữa các cấu hình *khác nhau* là dấu hiệu HỎNG**, không
phải dấu hiệu bền vững — nó thường có nghĩa phép thử chưa hề diễn ra.

## 6. Chỗ thật sự còn hở — nhắm vào đây

1. **Cùng họ mô hình.** Cả hai bộ trỏ đều thuộc dòng Qwen-VL, cùng họ với mô hình đang bị chấm.
   Đòn *"bộ trỏ quen giọng"* đã đóng, đòn *"cùng họ"* thì **chưa**.
2. **Không có neo người.** Không có ai chấm tay để đối chiếu với thước. Dự án đã quyết không làm.
   Zhao et al. (EACL 2021) cho thấy thước không-tham-chiếu thắng ở **mức câu**, nhưng để xếp hạng
   **hệ thống** thì chính họ khuyên dùng thước có tham chiếu — mà toàn bộ kết luận ở đây là mức hệ thống.
3. **Ngữ cảnh được mớm.** Lịch sử các bước trước trong câu nhắc là **câu chuẩn do người viết**,
   không phải câu mô hình tự sinh. Mọi số tuyệt đối phải đọc kèm điều kiện đó.
4. **S2 mới có một hạt giống.** Luật đã khoá đòi trung bình hai; hạt thứ hai đang chờ train.
   Nhiễu giữa hai hạt giống đo được ±1,3 pp, mà hiệu ứng cần đọc chỉ −1,93 pp.
5. **Chẩn đoán vòng tròn.** Nhóm 325 bước dùng để giải thích vì sao S2 thua được định nghĩa
   **bằng chính hành vi của S2**. Dự án có tự khai điều này, nhưng nó vẫn là chỗ yếu.
6. **Trần 75,7% là giới hạn của dụng cụ, không phải của ngôn ngữ** — 24,3% số bước ngay cả câu
   người cũng trượt. Câu hỏi để ngỏ: một thước bị mù một phần tư số ca thì kết luận được tới đâu.
7. **Một quả mìn chưa nổ:** `test_ac/descriptors.jsonl` vẫn là bản tiếng Việt trong khi tập dạy
   đã đổi sang tiếng Anh; hai nhánh trần `gold|filler` sẽ dùng nhầm nếu chạy mà quên dựng lại.

## 7. Đừng đọc những thứ này — chúng không có trong kho, và đó là cố ý

Kho đã bỏ ~500 tệp thuộc **khung thiết kế cũ đã bị bác từ tháng 7** (khung prompting, cặp
DG1/DG2, nguồn dữ liệu MobileViews). Chúng vẫn nằm trong lịch sử git nếu bạn cần tra *vì sao
hồi đó quyết X*, nhưng nhiều tệp trong đó tự xưng là *"CHỐT"* hoặc *"THIẾT KẾ CUỐI"* nên rất
dễ bị đọc nhầm thành bản hiện hành. Thiết kế đang chạy chỉ nằm ở `report/106` trở lên.

`report/57_related_work.md` giữ lại vì kho trích dẫn còn dùng được, nhưng **cách nó chia hai
bài báo đã lỗi thời** — có nhãn cảnh báo ngay đầu file.

## 8. Bối cảnh để góp ý cho đúng sức

Đây là **luận văn thạc sĩ**, không phải bài hội nghị lớn. Hai bài báo đang chuẩn bị nộp: một
bài tiếng Anh về thước đo, một bài tiếng Việt về nhãn mô tả phần tử. Tài nguyên: máy cá nhân
không GPU, huấn luyện thuê theo giờ, chấm điểm trên Kaggle **30 giờ GPU/tuần** (mỗi lượt chấm
tốn 5,6 giờ). Một lượt huấn luyện ~26 giờ.

⇒ Góp ý kiểu *"nên chấm thêm ba bộ trỏ nữa và thuê người đánh giá"* thì đúng nhưng vô dụng.
Góp ý hữu ích là loại **rẻ mà đổi được kết luận**: chỗ nào tính lại từ tệp thô là ra, chỗ nào
sửa câu chữ trong bài là hết hở, chỗ nào một phép đo nhỏ đóng được một lỗ lớn.

Và nếu bạn thấy kết luận tổng thể **không đứng nổi**, cứ nói thẳng. Đó là thông tin đắt hơn
mọi lời động viên — dự án này đã tự rút 8 con số và tự khai hai lần nới ngưỡng sai.
