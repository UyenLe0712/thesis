==============================================================================
HỒ SƠ TỰ-CHỨA ĐỂ AI KHÁC CHẤM TÊN BÀI + TÓM TẮT (hội nghị VCL)
Mục đích: paste toàn bộ file này vào một chat LLM khác → nhờ nó đóng vai "hội đồng
phản biện" chấm Tên bài + Tóm tắt + Từ khóa ở PHẦN 5. Đọc hết PHẦN 0→4 để hiểu
100% bài toán trước khi chấm. Trả lời bằng TIẾNG VIỆT.
==============================================================================


==============================================================================
PHẦN 0 — VIỆC CỦA BẠN (AI chấm)
==============================================================================
Bạn là một nhà nghiên cứu NLP/đa phương thức khó tính, kiêm reviewer hội nghị.
Hãy chấm phần TÊN BÀI + TÓM TẮT + TỪ KHÓA ở PHẦN 5, dựa trên bối cảnh PHẦN 1→4.
Yêu cầu quan trọng nhất của tác giả: bản tóm tắt phải (a) PHẢN ÁNH ĐÚNG bài toán,
(b) ĐỌC NHƯ NGƯỜI VIẾT — không lộ "mùi AI", (c) TRUNG THỰC (không phóng đại,
không bịa số). Xem rubric chi tiết ở PHẦN 6.


==============================================================================
PHẦN 1 — BỐI CẢNH ĐỀ TÀI
==============================================================================
- Đây là một phần của luận văn thạc sĩ, được tách thành bài báo "VCL" (tiếng Việt,
  nộp trước). Phần này gọi nội bộ là "DG1".
- BÀI TOÁN (DG1, đơn-màn): Cho ĐẦU VÀO gồm (1) MỘT ảnh chụp màn hình ứng dụng
  (screenshot giao diện Android) và (2) MỘT câu hỏi tình huống của người dùng bằng
  ngôn ngữ tự nhiên (ví dụ: "Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?").
  ĐẦU RA: một hướng dẫn thao tác TỪNG BƯỚC trả lời đúng câu hỏi đó, bám sát các nút/
  mục THỰC SỰ có trên màn hình. Đây là bài đa phương thức: ảnh + chữ -> chữ; bản chất
  giống "hỏi–đáp neo trên giao diện" (grounded QA), không phải chỉ "nhìn ảnh tả màn".
- HAI CÁI KHÓ TRUNG TÂM:
  (1) Mô hình ngôn ngữ lớn đa phương thức (VLM) hay "BỊA" — nhắc tới nút/menu KHÔNG
      tồn tại trên màn hình -> người dùng làm theo bị lạc.
  (2) KHÔNG có sẵn "hướng dẫn chuẩn do con người soạn" (gold tutorial) cho mọi ứng
      dụng -> không thể chấm theo cách so-với-đáp-án-mẫu thông thường.
- Mô hình sinh dùng trong thí nghiệm: một VLM thương mại (gpt-4o-mini) do máy không
  có GPU; nhưng PHƯƠNG PHÁP độc lập với model sinh (model thay được).
- Dữ liệu: MobileViews — ảnh chụp màn hình Android THẬT kèm View Hierarchy (cây phân
  cấp giao diện) và toạ độ bbox của từng phần tử. Tập dùng: ~90 màn / 18 ứng dụng
  đa dạng.


==============================================================================
PHẦN 2 — HAI ĐÓNG GÓP CỦA BÀI
==============================================================================
ĐÓNG GÓP A (hệ thống) — "lớp hậu kiểm trung-thực-hoá":
  Sau khi VLM sinh hướng dẫn, đối chiếu TỪNG bước với danh sách nút thật trong View
  Hierarchy. Bước nào trỏ tới phần tử KHÔNG khớp một nút thật nào -> chuyển thành MÔ
  TẢ BẰNG LỜI (fallback) thay vì gọi tên một nút bịa. (Lưu ý: đã CỐ Ý bỏ phương án
  "sửa thành một nút thật khác" vì nó gây lỗi-im-lặng: thay nút-ma bằng nút-thật-
  nhưng-SAI-ý. Nên hệ chỉ còn 2 nhánh: giữ-nguyên / mô-tả-bằng-lời.)

ĐÓNG GÓP B (phương pháp đánh giá) — đánh giá khi KHÔNG có đáp án mẫu:
  - Lấy View Hierarchy làm "nguồn đối chiếu bạc" (silver oracle): nó là danh sách nút
    thật do Android cung cấp tự động — rẻ, có sẵn. CHỈ dùng lúc CHẤM, TUYỆT ĐỐI không
    đưa cho mô hình lúc SINH (tránh rò rỉ/data leakage).
  - Ba thước đo tự động: (i) độ trung thực/faithfulness (bước có trỏ nút không tồn tại
    không), (ii) độ đúng tên nút/label-fidelity (gọi đúng tên hiển thị không), (iii)
    định dạng/format (đánh số, động từ mệnh lệnh...).
  - Kiểm độ tin cậy của chính thước đo bằng PERTURBATION TEST: chủ động "tiêm" lỗi đã
    biết (đổi nút thật -> nút-ma; đổi -> đồng nghĩa; phá format) rồi xem thước đo có
    bắt đúng không. KHÁCH QUAN, tái lập, KHÔNG cần người chấm.


==============================================================================
PHẦN 3 — QUYẾT ĐỊNH PHƯƠNG PHÁP & RÀNG BUỘC (để bạn hiểu vì sao tóm tắt viết vậy)
==============================================================================
- CHỐNG VÒNG-LẬP-LUẬN (anti-circularity): bộ phận QUYẾT "khớp/không khớp" (để chọn
  fallback) và bộ phận CHẤM điểm phải ĐỘC LẬP nhau. Cụ thể: quyết bằng một embedding
  (nomic), chấm bằng embedding KHÁC (bge-m3) + thêm một LLM-as-judge KHÁC HỌ với model
  sinh (vì model sinh là gpt-4o-mini nên judge không dùng họ GPT, tránh tự-thiên-vị).
- CLAIM ĐÃ THU HẸP (rất quan trọng, để không over-claim): bài CHỈ khẳng định
  "lớp hậu kiểm GIẢM số tham chiếu tới nút không tồn tại, đổi lại một phần bước phải
  mô tả chung chung hơn (chi phí = % fallback)". Bài KHÔNG khẳng định hướng dẫn "đúng
  ý / hữu ích" — vì điều đó cần đáp-án-vàng từng-bước (để dành cho bài/phần sau, dùng
  dataset có gold). Đừng để tóm tắt lỡ tay claim "đúng/hữu ích".
- KHÔNG BỊA SỐ: bộ kết quả trên tập đa-app CHƯA chạy xong, nên tóm tắt CỐ Ý không ghi
  con số cụ thể (chỉ nói định tính "giảm rõ"). Đây là lựa chọn TRUNG THỰC, không phải
  thiếu sót — đừng đề xuất nhét số bịa vào.
- VIẾT GIỐNG NGƯỜI: tác giả YÊU CẦU bản tiếng Việt phải đọc như người viết, tránh
  dấu hiệu AI (mở bài sáo "Trong bối cảnh.../Với sự phát triển..."; liệt kê 3 vế đều
  tăm tắp; "không chỉ... mà còn..."; buzzword "đáng kể/vượt trội/mở ra hướng đi mới";
  câu nào cũng dài bằng nhau). Tác giả chấp nhận giọng mộc, cụ thể, có cả nhược điểm.


==============================================================================
PHẦN 4 — BỐI CẢNH HỘI NGHỊ & YÊU CẦU NỘP
==============================================================================
- Hội nghị VCL (tiếng Việt), có 4 tiểu ban:
  1) Lý thuyết và mô hình mới (LLMs và tương lai NLP; ngữ nghĩa tính toán; phân tích
     diễn ngôn; transfer learning/fine-tuning cho tiếng Việt)
  2) AI tạo sinh trong giáo dục (thiết kế học liệu & cá nhân hóa; đánh giá tự động &
     phản hồi thông minh; AI hỗ trợ nghiên cứu-giảng dạy; hệ sinh thái AI lớp học)
  3) Ngôn ngữ và trách nhiệm xã hội (đạo đức AI; bảo tồn ngôn ngữ dân tộc; thiên lệch
     dữ liệu & công bằng; bảo mật & quyền riêng tư)
  4) Ứng dụng liên ngành (NLP y tế/luật/truyền thông; phân tích cảm xúc; ASR/TTS;
     dịch máy & cộng tác người–máy)
- TÁC GIẢ ĐANG CHỌN: Tiểu ban 1 (mục "LLMs và tương lai NLP") — vì lõi là phương pháp
  NLP/LLM + đánh giá. (Phương án thay thế cân nhắc: Tiểu ban 2, nếu nhấn "sinh nội
  dung hướng dẫn + đánh giá tự động"; nhược: hướng-dẫn-phần-mềm không hẳn là "giáo dục".)
- ĐỊNH DẠNG NỘP: Tên bài + Tóm tắt 100–150 TỪ (tiếng Việt) + Từ khóa ≥ 5.


==============================================================================
PHẦN 5 — NỘI DUNG CẦN CHẤM (do AI trước sinh ra)
==============================================================================

[TÊN BÀI — bản chính]
Sinh hướng dẫn sử dụng phần mềm từ ảnh giao diện và câu hỏi của người dùng: đánh giá
và cải thiện độ trung thực khi không có đáp án mẫu

[TÊN BÀI — bản gọn thay thế]
Trả lời câu hỏi sử dụng phần mềm bằng hướng dẫn từng bước từ ảnh giao diện: đo và giảm
tham chiếu sai khi không có đáp án mẫu

[TÓM TẮT — ~135 từ]
Người dùng chưa quen một ứng dụng thường chỉ biết hỏi "muốn làm việc này thì bấm vào
đâu". Bài báo xét bài toán: cho một ảnh chụp màn hình kèm một câu hỏi tình huống bằng
ngôn ngữ tự nhiên, sinh hướng dẫn thao tác từng bước trả lời câu hỏi đó, bám sát những
gì có thật trên màn hình. Mô hình ngôn ngữ lớn đa phương thức làm được việc này, nhưng
hay nhắc tới nút hoặc menu không tồn tại, khiến người làm theo bị lạc; trong khi mỗi
ứng dụng lại gần như không có sẵn hướng dẫn mẫu để đối chiếu. Chúng tôi lấy cây phân
cấp giao diện (View Hierarchy) của Android làm nguồn chấm — chỉ dùng khi đánh giá,
không đưa cho mô hình lúc sinh — để đo tự động độ trung thực và độ đúng tên nút, kèm
một lớp hậu kiểm chuyển các bước trỏ tới phần tử không có thật thành mô tả bằng lời.
Độ tin cậy của thước đo được kiểm bằng cách chủ động tiêm lỗi đã biết, không cần người
chấm. Thử nghiệm trên màn hình Android thực cho thấy cách làm giảm rõ số tham chiếu
sai, đổi lại một số bước phải mô tả chung chung hơn.

[TỪ KHÓA — 7]
mô hình ngôn ngữ lớn đa phương thức · sinh hướng dẫn sử dụng phần mềm · trả lời câu
hỏi tình huống dựa trên giao diện · đánh giá tự động không cần đáp án mẫu · hiện tượng
bịa (hallucination) giao diện · cây phân cấp giao diện (View Hierarchy) · độ trung
thực (faithfulness)


==============================================================================
PHẦN 6 — RUBRIC CHẤM (trả lời từng mục, bằng tiếng Việt)
==============================================================================
1. ĐÚNG BÀI TOÁN? Tóm tắt có phản ánh đúng rằng ĐẦU VÀO = ảnh giao diện + câu hỏi
   tình huống, ĐẦU RA = hướng dẫn từng bước TRẢ LỜI câu hỏi, neo trên màn hình không?
   Có thiếu/sai/thừa vế nào không?
2. TRUNG THỰC? Có chỗ nào over-claim (vd ngầm khẳng định hướng dẫn "đúng ý/hữu ích",
   trong khi bài chỉ dám claim "giảm tham chiếu sai")? Có chỗ nào nên khiêm tốn hơn?
3. "MÙI AI"? Chỉ ra cụ thể câu/cụm nghe máy móc hoặc sáo rỗng, và ĐỀ XUẤT cách viết
   lại tự nhiên hơn theo văn phong học thuật tiếng Việt của người thật.
4. ĐỘ DÀI? Đếm số TỪ tiếng Việt của phần tóm tắt; có nằm trong 100–150 từ không? Nếu
   lệch, chỉ rõ và gợi ý cắt/thêm ở đâu.
5. TÊN BÀI? Bản chính vs bản gọn — bản nào tốt hơn và vì sao? Đề xuất 1–2 phương án
   tên bài tốt hơn nếu có (đúng trọng tâm, không sáo, đủ thông tin: input ảnh+câu hỏi,
   output hướng dẫn, điểm mới = đánh giá không cần đáp án mẫu).
6. TỪ KHÓA? Đủ ≥5 chưa, có trùng/thiếu từ khóa quan trọng không (vd "grounding giao
   diện", "MobileViews", "perturbation/độ tin cậy thước đo")?
7. TIỂU BAN? Với nội dung trên, nên nộp Tiểu ban 1 hay tiểu ban khác? Vì sao?
8. BẢN CẢI TIẾN: Viết lại GIÚP một phương án Tên bài + Tóm tắt (100–150 từ) + Từ khóa
   mà bạn cho là tốt nhất — giữ đúng bài toán & ràng buộc ở PHẦN 1→4, đọc như người
   viết, không bịa số.

(HẾT — nếu cần thêm thông tin để chấm chính xác, hãy nêu rõ bạn cần gì.)
