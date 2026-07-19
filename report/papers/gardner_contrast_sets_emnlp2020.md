# Evaluating Models' Local Decision Boundaries via Contrast Sets (Gardner et al.)

- **Link:** https://aclanthology.org/2020.findings-emnlp.117/ · ⚠ *xác nhận link trước khi in*
- **Venue/năm:** Findings of EMNLP 2020.
- **Vai trong luận văn:** **trụ khái niệm** cho lối *phân-tầng-một-cue / thay-đổi-một-yếu-tố* trong phân tích tín hiệu thứ tự (§4.3).

## 1. Bối cảnh & vấn đề
Một mô hình đạt điểm cao trên tập test **không** chứng minh nó "hiểu" — có thể nó **bám vào tương quan bề mặt** trong dữ liệu. Làm sao kiểm được nó thật sự nhạy với **yếu tố quyết định** hay chỉ ăn may? Gardner et al. đề xuất **contrast sets**.

## 2. Ý tưởng chính (dễ hiểu)
**Contrast set** = lấy một mẫu test, rồi **thay đổi TỐI THIỂU một yếu tố** sao cho **đáp án đúng đổi theo**, giữ mọi thứ khác gần như nguyên. Ví dụ đổi một từ phủ định để lật nhãn. Nếu mô hình thật sự dựa vào yếu tố đó, điểm của nó phải đổi đúng chiều trên contrast set; nếu nó "đoán mò theo bề mặt", nó sẽ trượt. Đây là cách **khoanh vùng ranh giới quyết định cục bộ** của mô hình bằng phép **can thiệp có kiểm soát vào đúng một biến**.

## 3. Vì sao liên quan tới luận văn
Ý "**đổi đúng một yếu tố, giữ phần còn lại**" chính là nền của **single-cue stratification** ở §4.3: khi phân tích "hệ dựa vào tín hiệu thứ tự nào", ta **chỉ giữ những cặp màn phân biệt bởi ĐÚNG một cue** (gating, nav-affordance, state-delta, title-progression, drill-down) để **cô lập ảnh hưởng của từng cue** — thay vì trộn lẫn.

## 4. Điểm mạnh & giới hạn
- **Mạnh:** khung tư duy chuẩn cho "can thiệp một biến để đo nhân quả cục bộ".
- **Giới hạn (với ta):** Gardner làm ở miền NLP văn bản, **chưa** ai áp đúng vào "cue thứ tự màn GUI" → đây là **chỗ đóng-góp-mới** của ta (ta khai thẳng: chỉ có trụ khái niệm, không có tiền lệ trùng khít).

## 5. Dùng refer gì cho bài của tôi
- **Trụ khái niệm** cho signal-attribution một-cue (§4.3) — biện minh ta KHÔNG che pixel, KHÔNG tin lời model tự khai, mà **phân tầng theo một cue**.
- Củng cố tính khoa học: phân tích cue của ta có gốc từ **contrast-set/can-thiệp-một-biến**, không phải tự chế.
- Ghi rõ ranh giới: áp dụng vào cue-thứ-tự-GUI là phần mới.
