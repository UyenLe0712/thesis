# 137 — Prompt research gửi mô hình khác (viết 5/9/2026)

> Dùng khi muốn một mô hình ở phiên khác tra độc lập. Copy trọn khối trong ```` ``` ```` bên dưới.
> Prompt tự chứa: người đọc không cần biết gì về kho này.

```
Bạn là chuyên gia đánh giá mô hình thị giác-ngôn ngữ và đo lường trong NLP. Tôi cần bạn tra
cứu học thuật và tư vấn kỹ thuật cho một luận văn thạc sĩ. Trả lời bằng tiếng Việt.

QUY TẮC CỨNG, ÁP CHO TOÀN BỘ CÂU TRẢ LỜI
- Không bịa citation. Mỗi bài phải có: họ tác giả đầu, năm, TÊN VENUE CHÍNH XÁC, số trang
  hoặc arXiv ID, và một câu trích nguyên văn ngắn chứng minh đúng ý bạn dẫn.
- Phân biệt rõ bài đã bình duyệt với preprint arXiv không venue. Nếu không xác minh được
  venue thì ghi thẳng "chưa xác minh".
- Nếu một hướng không có tiền lệ, nói "không tìm thấy" thay vì suy đoán.
- Ưu tiên độ chính xác hơn số lượng: 6 hướng có bằng chứng chắc hơn 20 hướng phỏng đoán.
- Với mỗi đề xuất, ước chi phí thi hành theo giờ GPU và nói rõ cần train lại hay không.

=== 1. HỆ THỐNG ĐANG CÓ ===

Tác vụ: cho một ảnh chụp màn hình Android, một mục tiêu người dùng, và lịch sử các bước đã
làm, mô hình sinh MỘT câu tiếng Anh mô tả bước thao tác tiếp theo. Mô hình KHÔNG tự bấm,
chỉ viết câu cho người khác đọc.

Dữ liệu: AndroidControl (Li et al., Google DeepMind, NeurIPS 2024 Datasets & Benchmarks,
arXiv 2406.03679, CC0). Tập dạy 64.567 bước, tập kiểm 6.958 bước trong đó 4.463 bước là
thao tác chạm (click hoặc long_press). Mọi điểm số dưới đây tính trên 4.463 bước chạm đó.

Mô hình nền: Qwen2.5-VL-3B-Instruct, tinh chỉnh QLoRA 4-bit, r=8, alpha=16, đóng băng phần
thị giác, cutoff 3072 token, 1 epoch.

Biến thể đang so: một nhánh chỉ sinh câu (SFT trơn); một nhánh sinh thêm ô mô tả phần tử
trước khi viết câu; một nhánh nhận thêm khối tối đa 40 ứng viên phần tử trên màn trong câu
nhắc và phải phát ra thẻ chọn `<sel>tên <point>x,y</point></sel>` hoặc `<sel>none</sel>`
trước khi viết câu.

=== 2. CÁCH CHẤM HIỆN TẠI (gọi là "executability") ===

Không dùng BLEU/ROUGE. Thay vào đó, câu do mô hình sinh được đưa cho một mô hình định vị GUI
ĐỘC LẬP (UGround-V1-2B) cùng ảnh màn hình; mô hình đó trả về MỘT toạ độ (x,y).

Một bước tính là ĐẠT khi ba điều kiện cùng đúng:
  (a) action_ok  — loại thao tác suy ra từ câu khớp loại thao tác vàng;
  (b) toggle_ok  — không lẫn bật/tắt;
  (c) điểm trỏ vừa nằm trong dung sai ±14% bề ngang và ±14% bề dọc màn hình, vừa gần phần tử
      vàng hơn mọi phần tử khác trên màn (ô Voronoi, hạt là chính điểm chạm).

Điều kiện (c) là bản SIẾT CHẶT của quy ước ±14% thường dùng trong lĩnh vực, không phải một
lựa chọn ngang hàng.

=== 3. SỐ ĐÃ ĐO, n = 4.463 ===

  Câu do NGƯỜI viết (mốc trần)          75,73%
  Nhánh mô tả-trước (tốt nhất hiện có)  60,05%
  Nhánh SFT trơn                        59,11%
  Nhánh khối-ứng-viên                   56,13%
  Mô hình nền chưa tinh chỉnh           47,59%
  Sàn: câu rỗng nghĩa                   12,00%
  Sàn: câu đúng văn phong nhưng sai màn  6,12%

Vì sao trần chỉ 75,73%: trong các bước mà câu người viết cũng bị tính trượt, 72% là do mô
hình định vị trỏ lệch quá 14% bề ngang. Tức giới hạn nằm ở DỤNG CỤ ĐO, không nằm ở câu.

Đã thử đổi sang mô hình định vị mạnh hơn trên benchmark: UI-Venus-Ground-7B (ScreenSpot-v2
mobile 99,0/90,0) so với UGround-V1-2B (95,0/83,3). Kết quả: UI-Venus cho điểm THẤP HƠN ở cả
ba nhánh, và trần cũng thấp hơn (69,3 so với 70,0 trên cùng lát cắt 2.532 bước). Thứ tự các
nhánh giữ nguyên dưới cả hai bộ trỏ.

=== 4. CHẨN ĐOÁN ĐÃ CÓ VỀ NHÁNH KHỐI-ỨNG-VIÊN ===

Bảng chéo giữa "phần tử vàng có nằm trong khối ứng viên không" và "mô hình có dám chọn không":

  có vàng + dám chọn      n=2.326 (52,1%)  exec 71,41%   action_ok 99,14%
  có vàng + BỎ CUỘC       n=  872 (19,5%)  exec 23,74%   action_ok 71,22%
  không vàng + dám chọn   n=  264 ( 5,9%)  exec 37,50%
  không vàng + bỏ cuộc    n=1.001 (22,4%)  exec 53,75%

Khi mô hình dám chọn và trên màn có đáp án, nó đạt 71,41%, chỉ kém mốc người 4,3 điểm. Toàn
bộ tổn thất nằm ở 27,27% số bước có đáp án mà mô hình vẫn phát `<sel>none</sel>`.

Bốn dấu hiệu của việc bỏ cuộc, đo được:
  - câu chứa động từ không-chạm (swipe/scroll/back/type): 28,30% ở nhóm bỏ cuộc so với 0,97%
    ở nhóm dám chọn;
  - sai số của bộ trỏ: trung vị 19,90% bề ngang ở nhóm bỏ cuộc so với 0,78% ở nhóm dám chọn,
    phân vị 90 vượt 100% bề ngang (trỏ sang phần khác của màn);
  - khối ứng viên càng đông càng dễ bỏ cuộc, đơn điệu: 15,7% khi khối có 6-10 phần tử, lên
    33,2% khi khối chạm trần 40; exec tương ứng tụt 70,5% xuống 51,8%;
  - độ dài câu KHÔNG liên quan: trung vị 33 ký tự ở cả hai nhóm.

Nguyên nhân nghi ngờ, mới tìm ra: trong tập dạy, nhãn `<sel>none</sel>` chiếm 54,78% tổng số
mẫu, nhưng nếu chỉ tính trên bước CHẠM — loại bước duy nhất được chấm — thì chỉ 29,1%, khớp
tập kiểm (28,34%). Mô hình phát ra 41,97%, nằm giữa hai con số. Lý do: mọi bước không-chạm
(vuốt, quay lại, gõ chữ, mở ứng dụng) đều được gán nhãn `<sel>none</sel>` theo thiết kế, và
nhóm đó chiếm 36,2% tập dạy.

=== 5. HƯỚNG ĐÃ THỬ VÀ CHẾT, KÈM LÝ DO ĐO ĐƯỢC (đừng đề xuất lại) ===

  - Ép mô hình luôn phải chọn (bỏ hẳn cơ chế bỏ cuộc): kéo độ chính xác trên nhóm có đáp án
    từ 57,5% lên 69,1%, nhưng độ đúng trên toàn bộ bước TỤT từ 63,4% xuống 49,7%.
  - Thu nhỏ khối ứng viên xuống 10 phần tử: theo thứ tự đọc chỉ còn phủ 42,91% phần tử vàng,
    xếp theo mức khớp chữ với mục tiêu cũng chỉ 51,74%, so với 71,66% ở trần 40. Mất phủ ăn
    hết lợi ích của khối nhỏ.
  - Nới dung sai toạ độ khi dựng nhãn: tối đa thêm 4,30 điểm phủ.
  - Sửa hoàn hảo lỗi nhận sai loại thao tác: chỉ thêm 1,21 điểm exec.
  - Học tăng cường trên chính đầu ra của mô hình (on-policy preference): tỉ lệ mẫu đủ điều
    kiện chỉ 3,3%, dưới ngưỡng 25% đã khoá trước, nên dừng.
  - Đổi mô hình định vị sang loại mạnh hơn: cho điểm thấp hơn, xem mục 3.

=== 6. HAI CÂU HỎI CẦN BẠN TRA ===

CÂU HỎI A — làm sao đưa exec từ 56-60% lên 65-70%?
Tìm các hướng có tiền lệ đã bình duyệt, phù hợp với ràng buộc ở mục 7. Quan tâm nhất:
  A1. Cách chữa việc mô hình từ chối trả lời quá nhiều khi phân bố nhãn lệch về "không có
      đáp án". Tiền lệ trong hỏi đáp trích xuất, trong quy chiếu biểu thức, hoặc trong
      selective prediction. Có bài nào đo được hiệu quả của việc cân bằng lại phân bố nhãn,
      đổi hàm mất mát, hay hiệu chỉnh ngưỡng sau huấn luyện không, và mức tăng bao nhiêu?
  A2. Tách quyết định thành nhiều tầng (loại thao tác -> có đáp án hay không -> chọn phần tử
      -> viết câu) so với để mô hình quyết một lần. Tiền lệ và mức chênh đã báo cáo.
  A3. Cách đưa danh sách ứng viên vào câu nhắc sao cho mô hình chọn tốt hơn: thứ tự, cách
      đánh số, độ dài danh sách, có nên kèm toạ độ hay không. Có nghiên cứu về hiệu ứng vị
      trí trong danh sách dài với mô hình thị giác-ngôn ngữ không?
  A4. Bất kỳ hướng nào khác bạn thấy có bằng chứng mạnh hơn ba hướng trên.

CÂU HỎI B — có cách nào nâng TRẦN của phép đo mà không nới lỏng tiêu chí đúng/sai?
Trần hiện tại 75,73% bị chặn bởi mô hình định vị, không phải bởi câu. Tìm tiền lệ cho:
  B1. Hợp nhất nhiều mô hình định vị (ensemble, vote, union) thay vì dùng một.
  B2. Cho mô hình định vị trả về một vùng hoặc top-K điểm thay vì một điểm duy nhất.
  B3. Dùng cây phân cấp giao diện (view hierarchy / accessibility tree) làm trọng tài ở mức
      phần tử thay vì mức pixel.
  B4. Dùng mô hình ngôn ngữ làm giám khảo cho tác vụ chỉ dẫn GUI: đã ai hiệu chuẩn với người
      chưa, mức đồng thuận bao nhiêu?
  B5. Các mô hình định vị GUI mạnh nhất tính tới tháng 9/2026 trên benchmark di động, kèm
      giấy phép và việc chúng có dùng AndroidControl trong dữ liệu huấn luyện hay không.

=== 7. RÀNG BUỘC — nói rõ nếu một đề xuất vi phạm ===

  - Không nới dung sai hình học để lấy điểm cao hơn. Đã đo: nới từ luật đang dùng sang luật
    lỏng nhất nâng trần từ 74,2% lên 82,2%, NHƯNG nâng cả sàn, và dưới luật lỏng thì hai
    nhánh mô hình tốt nhất bằng điểm nhau — tức xoá luôn khoảng cách đang là kết quả chính.
  - Trọng tài không được trùng với thứ đang được đánh giá, tránh lập luận vòng tròn.
  - Mọi thay đổi thước phải áp lại cho TẤT CẢ các nhánh đã đo, nên chi phí tính lại là thật:
    mỗi lần chấm lại một nhánh tốn khoảng 5,6 giờ GPU.
  - Mô hình nền cố định là Qwen2.5-VL-3B; đổi mô hình nền không nằm trong phạm vi.

=== 8. ĐỊNH DẠNG TRẢ LỜI ===

Phần 1 — bảng: hướng | tiền lệ (tác giả, năm, venue chính xác, trang/arXiv) | trích nguyên
văn | mức tăng đã báo cáo trong bài gốc | miền của bài gốc có gần miền GUI không | chi phí
ước tính | có vi phạm ràng buộc mục 7 không.

Phần 2 — xếp hạng các hướng theo ba trục, cho điểm và giải thích ngắn: khả năng nâng số
thật; chi phí; rủi ro bị phản biện là chọn phương pháp cho hợp kết quả.

Phần 3 — ba hướng bạn khuyên làm trước, mỗi hướng kèm: thay đổi cụ thể phải làm, phép đo rẻ
nhất để biết hướng đó sống hay chết TRƯỚC khi tiêu giờ GPU, và mức tăng bạn kỳ vọng kèm
khoảng bất định.

Phần 4 — những gì bạn KHÔNG tìm thấy tiền lệ, nói thẳng.
```
