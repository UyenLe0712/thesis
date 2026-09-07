# 145 — Chốt hướng sau lượt GRPO: DỪNG thực nghiệm, chuyển sang viết

*Viết 6/9/2026, sau khi `exec` của lượt GRPO về (Δ = +0,02 pp) và sau một vòng ba luồng phản biện
độc lập (hội đồng · chiến lược thực nghiệm · đóng khung). Trọng tài: trợ lý, có kiểm lại từng số.*

Nguồn số: `report/144` · `report/106` (x19)–(x20) · tệp thô trong `runs/grpo_point/`.
Mọi con số dưới đây đã được **tái lập độc lập từ tệp thô**, không lấy nguyên từ báo cáo của luồng
phản biện.

---

## 1. Con số đóng cửa: trần của họ can thiệp này là **+1,39 pp**, dưới MDE 2,2

Hạch toán của `report/144` §5b cho phần lợi gộp **+62 bước** ở nhóm sửa được khai báo. Nếu triệt
tiêu **hoàn toàn** cả ba nguồn cản (0 bước làm hỏng khai báo, 0 nhiễu ở nhóm giữ nguyên, 0 nhiễu ở
nhóm không có tên vàng) thì `exec` chỉ lên **62/4.463 = +1,39 pp**. ⇒ Ngay cả một phiên bản
**hoàn hảo** của họ can thiệp "thưởng tầng khai báo cộng một số hạng bảo vệ tầng đầu ra" cũng
**không đủ** vượt ngưỡng phát hiện. Vấn đề không phải vá chưa hết lỗi, mà là **phần lợi gốc quá nhỏ**.

Ba chặn độc lập, mỗi cái tự nó đã đủ:
· **KTC của phép đo** [−0,59 · +0,64] loại mọi hiệu ứng ≥ +0,64 pp — bằng chứng đo được.
· **Cần ≈ 260 bước sửa sạch tuyệt đối** để đạt +2,2 pp (98,2 bước ròng ÷ hệ số biên 0,378), so với
  164 bước sửa kèm 75 bước hỏng vừa đạt được. Tức cần **2,9 lần** mức tăng và **đồng thời** triệt
  tiêu cơ chế thiệt hại sinh ra từ chính phép dịch chuyển trọng số tạo ra mức tăng ấy — hai yêu
  cầu ngược nhau.
· **Tín hiệu học đã cạn**: `frac_reward_zero_std` 0,420 → 0,515, `r_point` phẳng +0,0006 ở 100
  bước cuối. Chuyển giao train → test chỉ ≈ 31%.

**Bốn mốc oracle, tái lập từ tệp thô:**

| kịch bản | `exec` | Δ so MIN |
|---|---|---|
| lượt GRPO này nếu 0 thiệt hại 0 nhiễu | 61,44 | +1,39 |
| **oracle MIN ∪ GRPO** (biết trước nhánh nào trúng) | **62,27** | **+2,22** |
| oracle khai báo đúng hết (1.367 bước lên mức 87,1) | ~80,1 | ~+20,0 |
| trần câu chuẩn | 75,73 | +15,68 |

⭐ Oracle trên đúng hai nhánh đã có **chỉ vừa chạm MDE**, và nó đòi một bộ định tuyến biết trước
nhánh nào đúng. Dự án đã đo **hai lần độc lập** rằng tín hiệu đó không tồn tại: quét τ cho AUC
biên **0,69–0,72** với luật null thắng (`report/142`), và nhánh ứng viên bỏ cuộc mù với likelihood
của chính mô hình.

## 2. Hai phép đo mới, 0 GPU, làm mạnh phần chẩn đoán

**(a) Bảng chéo *khai báo đổi × câu đổi*** trên toàn 4.463 bước:

| khai báo | câu | n | b | c | ròng | `exec` MIN → GRPO |
|---|---|---|---|---|---|---|
| không đổi | không đổi | 2.202 | 0 | 0 | 0 | 65,9 → 65,9 |
| không đổi | đổi | 311 | 10 | 5 | −5 | 61,4 → 59,8 |
| **đổi** | **không đổi** | **1.300** | **0** | **0** | **0** | 58,9 → 58,9 |
| đổi | đổi | 650 | 88 | 94 | +6 | 41,8 → 42,8 |

⭐ **1.300/1.950 = 66,7% số bước đổi ô khai báo mà câu không đổi một ký tự.** Thước tất định trên
câu, nên **hai phần ba công của phần thưởng rơi vào chỗ thước không thể nhìn thấy**. Toàn bộ 197
lần lật `exec` nằm gọn trong 961 bước có câu đổi. (Bản mạnh hơn con số 35,4% ở `144` §5b, vì đo
trên toàn quần thể thay vì chỉ nhóm sửa đúng.)

**(b) Tầng viết câu đã hết dư địa.** Ở nhóm khai báo đúng (n=2.106), MIN đạt **87,1** trong khi
**câu chuẩn chỉ 86,3** — mô hình đã ngang mốc câu chuẩn khi nhận đúng phần tử. Toàn bộ khoảng
cách còn lại nằm ở **1.367 bước nhận sai phần tử** (MIN 21,8 so với câu chuẩn 61,4).
⚠️ Lát cắt định nghĩa bằng hành vi của chính mô hình ⇒ **hậu kiểm**, phải gắn nhãn; và ô 87,1 vượt
mốc 86,3 chính là dấu hiệu hiệu ứng chọn mẫu, phải khai chứ đừng trình như năng lực.
⇒ Hệ quả: đòn bẩy ④ của `report/143` (ước "+1,7 tối đa từ nhóm nhận đúng") nay đo lại được là
**≈ 0**. Hướng chi tiền cuối cùng còn lại tự đóng.

## 3. Phán quyết

**DỪNG mọi lượt tiêu GPU.** Căn cứ: trần +1,39 < MDE 2,2 · KTC loại mọi hiệu ứng ≥ +0,64 ·
oracle hai nhánh chỉ +2,22 mà đòi bộ định tuyến đã đo là không dựng được · hệ số chuyển đổi 0,43
đã bị bác (thực tế ≈ 0,01) nên không còn công cụ nào biện minh cho một lượt chi tiền · không còn
hạn nộp nào ép (SOICT đã bỏ, FAIR/VCL đã gửi).
⛔ Muốn chi tiếp là **quyết định mới** theo (x20d), phải mở mục đăng ký riêng và khai rằng nó đi
ngược một trần đã đo được.

**Hai việc còn làm, cả hai đều 0 đồng:**
1. **(x20b) bước KHÔNG chạm** — đã khoá là bắt buộc, ~1,7 h Kaggle T4 miễn phí, chấm 0 GPU ở máy
   nhà. Đóng đòn Đ6, rủi ro duy nhất còn để ngỏ của lượt GRPO, và là rủi ro có tiền lệ nặng
   (MIN-DESC từng lộ giá −19,75 đúng ở nhóm này).
2. **Chấm tay 100 câu, hai người độc lập** — lỗ duy nhất còn lại ở phần đóng góp đứng vững nhất
   (thước đo). `ch7` đã tự khai *"đã lên kế hoạch nhưng chưa tiến hành"*. Thiết kế tối thiểu, khoá
   trước khi chấm: 100 bước lấy ngẫu nhiên phân tầng theo phán quyết của thước (50 trúng, 50
   trượt, giấu nhánh và giấu phán quyết); mỗi người xem ảnh màn hình cùng câu rồi chỉ một điểm
   chạm; báo κ giữa hai người và κ giữa "người trúng" với "thước trúng". Lệch thì báo nguyên trạng.

**Khung viết:** lấy *"dụng cụ đo đã hiệu chuẩn + bản đồ điểm nghẽn"* làm khung tổng, nhúng một mục
riêng ở chương kết luận cho lập luận hội tụ của bốn can thiệp. Trong mục đó dùng chữ **"không xác
nhận được"**, ⛔ không dùng chữ **"bác bỏ"** — với một hạt giống và nhiễu giữa hạt 0,46–0,52, thiết
kế không cho phép phát biểu bác bỏ.
Tiền lệ đã xác minh tận nguồn: **Card và cộng sự, EMNLP 2020, tr. 9263–9274** (lấy mức chênh nhỏ
nhất phát hiện được làm luật đọc) và **Workshop on Insights from Negative Results in NLP**, lần đầu
tại EMNLP 2020, tới lần thứ tư năm 2023.

## 4. Ba lỗi văn bản đang sống trong luận văn

1. ✅ **Đã vá:** `ch3` và `ch7` còn dùng *"mẫu 1.697 bước, tức 2,6% tập huấn luyện"* — số đã rút
   khỏi bài vì không truy được tới script hay tệp đo. Giữ nguyên 17,3%.
2. ⛔ **Chưa vá, cần quyết:** dải *"−2,8 đến +1,7"* ở `ch6` **không được định nghĩa ở bất kỳ đâu**
   trong luận văn (`tab:luatdoc` ở `ch4` không có, `ch5` không có). Đây là chỗ dễ vỡ nhất về thủ
   tục, vì chính dải ấy giữ cho S2 nằm ở ô trắng, trong khi **S2 − S1/202 = −2,44 [−3,53 · −1,34]**
   thoả trọn quy tắc công bố của luận văn theo **chiều gây hại**.
3. ⛔ **Chưa làm:** `ch6` chưa có mục nào cho GRPO, trong khi `ch4` đã tả trọn chặng ba.
