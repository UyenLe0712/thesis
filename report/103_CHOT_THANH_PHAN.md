# Kế hoạch cuối của luận văn: làm gì, vì sao, và vì sao tin được

> **Cách đọc file này.** Đọc một mình file này là đủ, không cần mở file khác, không cần nhớ những gì đã bàn trước đây. Thuật ngữ nào xuất hiện đều được giải thích ngay tại chỗ. Chi tiết kỹ thuật và công thức nằm trong các khung "Hộp kỹ thuật" — bỏ qua khung vẫn hiểu trọn mạch.
>
> **File này là bản thứ ba, và đã bị soi hai lượt.** Bản đầu viết ngày 1/8 sau bốn vòng tra cứu tài liệu độc lập. Ngày 2/8, ba giám khảo phản biện độc lập đem nó ra "bắn thử" — mục 13 kể họ bắn trúng chỗ nào và bản này đã sửa gì. Ngày 3/8 làm thêm hai việc: rà từng con số trích dẫn bằng cách đọc tận PDF gốc của từng bài, và một vòng hỏi "có phương án nào tốt hơn khung này không" — mục 14 kể kết quả. Mọi con số trong thân file đã sửa theo hai lượt đó.
>
> *(Bản trình bày lại ngày 4/8: nội dung và số liệu giữ nguyên bản 3/8, chỉ viết lại cho dễ đọc — chia đoạn ngắn, thêm ví dụ, giải thích các chỗ mơ hồ.)*

**Bản đồ file — mỗi mục trả lời một câu hỏi:**

| Mục | Câu hỏi nó trả lời |
|---|---|
| 1 | Luận văn làm ra sản phẩm gì? |
| 2 | Đóng góp khoa học là gì? |
| 3 | Vì sao chọn đúng đóng góp đó mà không phải cái khác? |
| 4 | Vậy có mỏng quá cho luận văn thạc sĩ không? |
| 5 | Chứng minh bằng những thí nghiệm nào? |
| 6 | Vì sao kết quả đo ra sẽ tin được? |
| 7 | Dữ liệu dạy lấy đâu ra, sạch tới đâu? |
| 8 | Tốn bao nhiêu tiền, lịch thế nào, kẹt thì làm gì? |
| 9 | Hội đồng sẽ hỏi gì, trả lời sao? |
| 10 | Khác gì các nghiên cứu liền kề? |
| 11 | Rủi ro nào lớn nhất, đỡ thế nào? |
| 12 | Tóm tắt một trang |
| 13–14 | File này đã bị phản biện và kiểm số ra sao (lý do để tin nó) |

---

## 1. Luận văn này làm ra cái gì

Hãy hình dung một người đang bí trong một ứng dụng điện thoại. Họ chụp màn hình, hỏi: *"làm sao để chia sẻ playlist này cho bạn tôi?"*.

Sản phẩm của luận văn là **một mô hình trí tuệ nhân tạo nhỏ, chạy được ngay trên máy, nhìn bức ảnh đó và viết ra câu hướng dẫn cho họ**: *"Chạm vào biểu tượng chia sẻ ở góc trên bên phải màn hình."*

Điểm khác biệt với mọi nghiên cứu cùng mảng: các mô hình giao diện hiện nay được huấn luyện để **tự bấm thay người** — chúng sinh ra lệnh máy như `click(732, 173)`. Mô hình của luận văn sinh ra **câu chữ cho con người đọc**.

Chưa có mô hình nào được *huấn luyện* cho việc này. Có một hệ thống tên GuideMe ở hội nghị CHI 2026 làm việc tương tự, nhưng bằng cách ra lệnh cho mô hình lớn có sẵn — họ không huấn luyện gì (đã kiểm tận nơi ngày 3/8, chi tiết ở mục 10).

**Vài cái tên sẽ gặp suốt file, giải thích một lần ở đây:**

| Tên | Nghĩa |
|---|---|
| **Qwen2.5-VL-3B** | mô hình gốc được chọn: mô hình mở của Alibaba, biết nhìn ảnh và viết chữ, cỡ 3 tỉ tham số — đủ nhỏ để chạy trên máy cá nhân |
| **Fine-tune / huấn luyện tiếp** | lấy mô hình gốc rồi dạy thêm bằng dữ liệu của mình để nó làm đúng việc mình cần |
| **QLoRA** | kỹ thuật huấn luyện tiếp tiết kiệm: chỉ dạy một phần rất nhỏ của mô hình, nhờ vậy thuê một card đồ hoạ rẻ là đủ (mỗi lần huấn luyện trọn bộ dữ liệu tốn khoảng 13–16 đô) |
| **AndroidControl** | bộ dữ liệu công bố tại hội nghị NeurIPS 2024: 15.283 tác vụ trên điện thoại Android do người thật thao tác; mỗi bước có ảnh màn hình, toạ độ điểm người đó chạm, và **một câu mô tả bước đó do chính người thao tác viết ra** |
| **Cây trợ năng** (accessibility tree) | dữ liệu ẩn của mỗi màn hình Android, liệt kê mọi phần tử trên màn: khung bao của từng nút, loại phần tử (nút, ô nhập chữ...). Nhược điểm đã đo: chỉ 12,6% phần tử có ghi tên |
| **OCR** | phần mềm đọc chữ trên ảnh — dùng để lấy tên nút khi cây trợ năng không ghi |
| **Bộ trỏ** (grounding model) | một mô hình *khác*, có sẵn, làm đúng một việc: đọc một câu ("nút chia sẻ ở góc trên phải") rồi chỉ vào vị trí trên ảnh mà câu đó mô tả. Ta dùng nó làm giám khảo chấm điểm |

---

## 2. Đóng góp là gì — một ý, hai mức sâu

Cả luận văn xoay quanh đúng một ý: **buộc mô hình xác định rõ nó đang nói về nút nào, trước khi viết câu hướng dẫn**. Ý đó được cài vào mô hình ở hai mức, mức sau sâu hơn mức trước.

### Mức 1: bắt mô hình "khai" nó đang nhắm vào nút nào, trước khi viết câu

Cách huấn luyện thông thường: đưa ảnh + mục tiêu, dạy mô hình viết thẳng ra câu hướng dẫn, không có gì khác.

Cách của luận văn: dạy mô hình viết **một dòng khai báo trước**, rồi mới tới câu:

```
Cách dạy thường:      Tap the search bar at the top

Cách của luận văn:    <desc>ô nhập liệu | "Search Publications..." | <point>500,80</point> | ô nhập liệu duy nhất trên màn</desc>
                      Tap the Search Publications bar at the top
```

Dòng `<desc>...</desc>` có bốn ô, theo thứ tự cố định. Đối chiếu với ví dụ trên:

1. **Nút đó thuộc loại gì** — "ô nhập liệu" (các giá trị khác: nút bấm, công tắc...).
2. **Tên nó là gì** — `"Search Publications..."`, chữ hiển thị trên nút.
3. **Nó nằm ở toạ độ nào** — `<point>500,80</point>`, lấy từ đúng chỗ người thật đã chạm trong dữ liệu.
4. **Nó khác gì các nút bên cạnh** — "ô nhập liệu duy nhất trên màn": trên màn có mấy nút cùng loại, có nút nào trùng tên không.

Khi chạy thật, dòng khai báo bị cắt bỏ — người dùng chỉ nhận câu hướng dẫn. Dòng đó tồn tại chỉ để *ép mô hình, trong lúc học, phải xác định rõ mục tiêu trước khi mở miệng*.

### Mức 2: phạt thẳng vào cách tính điểm khi câu viết ra mơ hồ

Mức 1 thay đổi *thứ mô hình phải sinh ra*. Mức 2 đi sâu hơn một tầng: thay đổi *cách tính điểm phạt trong lúc học* — tức là sửa hàm mất mát, công thức mà quá trình huấn luyện dùng để biết mô hình đang sai bao nhiêu.

Ý tưởng bằng ví dụ. Màn hình có hai biểu tượng kính lúp giống hệt nhau: một cái tìm danh bạ (bên trái, cạnh chữ Contacts), một cái tìm nhạc (bên phải, cạnh chữ Music). Cần hướng dẫn bấm cái bên trái.

| Câu | Áp vào kính lúp trái | Áp vào kính lúp phải | Kết quả |
|---|---|---|---|
| "Tap the search icon" | xuôi | cũng xuôi | **bị phạt** — câu này không giúp người dùng chọn đúng |
| "Tap the search icon on the left, next to Contacts" | xuôi | không xuôi | không bị phạt |

Cách cài vào huấn luyện, theo ba bước:

1. Với mỗi bước trong dữ liệu dạy, ngoài dòng khai báo **thật** (dựng từ nút người thật đã chạm), dựng sẵn thêm một dòng khai báo **giả** lấy từ một nút hàng xóm trên cùng màn. Trong ví dụ trên: khai báo thật là kính lúp cạnh Contacts, khai báo giả là kính lúp cạnh Music.
2. Lúc huấn luyện, đo xem câu đích "khớp" với từng khai báo tới đâu (khớp = xác suất mô hình gán cho câu đó khi được đưa khai báo tương ứng).
3. Bắt độ khớp với khai báo thật phải cao hơn độ khớp với khai báo giả một khoảng tối thiểu. Câu nào khớp cả hai như nhau nghĩa là câu mơ hồ — bị phạt.

> **Hộp kỹ thuật.** Dạng hàm phạt dự kiến là phạt lề (margin loss): L = max(0, m − [log P(câu | khai báo thật) − log P(câu | khai báo giả)]), cộng vào hàm mất mát thường với một trọng số; giá trị m và trọng số chốt ở bản thử. Cơ chế mượn từ dòng "phạt mô tả mơ hồ" có từ 2016 (mục 3.4) — không nhận mới.

**Một giới hạn của mức 2, tự khai trước thay vì đợi bị hỏi** (vòng phản biện 3/8 tìm ra):

- Lúc học, phép so "khai báo thật với khai báo giả" diễn ra trong điều kiện mô hình **được đưa sẵn** dòng khai báo.
- Lúc chạy thật, mô hình **tự sinh** dòng khai báo — không ai đưa gì cả, nên tình huống "bị đưa khai báo giả" không bao giờ xảy ra. Tín hiệu học vì thế lệch một nhịp so với lúc dùng.
- Cách vá rẻ, ghi luôn vào bản thử: đặt thêm khoản phạt ngay ở **tầng sinh khai báo** — phạt khi mô hình sinh ra dòng khai báo mà đem áp vào nút hàng xóm cũng xuôi — thay vì chỉ phạt ở tầng câu.

Mức 2 **bắt buộc phải có mặt trong luận văn ở dạng thử nghiệm nhỏ** (lý do ở mục 3.4 và mục 4). Chạy nó trên toàn bộ dữ liệu hay không thì quyết sau, dựa vào kết quả thử.

### Vì sao đây là đóng góp về mô hình, không phải về dữ liệu

Vì cả hai mức đều đổi **thứ mô hình bị buộc phải làm trong lúc học**: mức 1 đổi chuỗi phải sinh, mức 2 đổi công thức phạt. Không mức nào là "sửa sang dữ liệu rồi huấn luyện y như cũ".

Và tác dụng đo được riêng: hai phiên bản đem so dùng **y hệt một bộ dữ liệu**, chỉ khác đúng chỗ can thiệp. Chênh lệch điểm giữa chúng, nếu có, là của riêng can thiệp, không lẫn thứ khác.

---

## 3. Vì sao chọn đúng cái này — chuyện thuyết phục nằm ở đây

Mục này trả lời năm câu, mỗi câu một tiểu mục: can thiệp có nhắm trúng bệnh không (3.1) · có bằng chứng nó giúp không (3.2) · có biết cách làm sai để né không (3.3) · chỗ này đã ai chiếm chưa (3.4) · lắp vào có rủi ro kỹ thuật không (3.5).

### 3.1. Nó nhắm trúng đúng bệnh đã chẩn được

Trước khi chọn thuốc thì phải biết bệnh. Bệnh đã đo được bằng số.

**Bệnh KHÔNG phải là bịa.** Soi tay 40 trường hợp mô hình viết sai: lỗi "bịa ra nút không tồn tại trên màn" chỉ chiếm 0–2%.

**Bệnh chính là câu mơ hồ** — câu không sai, nhưng không đủ để người đọc chọn đúng. Kiểu "chạm vào biểu tượng tìm kiếm" trên màn có hai biểu tượng tìm kiếm.

**Con số minh hoạ, kèm luôn cách đo để khỏi phải tra lại.** Phép đo làm ba bước:

1. Lấy 76 câu hướng dẫn *mẫu chuẩn* — câu do người thật viết trong AndroidControl, ở các bước chạm có toạ độ.
2. Đưa từng câu cho bộ trỏ (gpt-4o-mini) đọc rồi chỉ lên ảnh; tính trúng nếu điểm nó chỉ nằm trong dung sai 14% cạnh màn quanh chỗ người thật đã chạm.
3. Chia 76 câu làm hai nửa theo trung vị độ dài câu (8 từ).

Kết quả: nửa câu cộc lốc (kiểu "Click on alerts") được bộ trỏ tìm trúng nút **32%** số lần; nửa câu tả rõ (kiểu "Click on the search bar at the top right corner…") trúng **69%**. Tương quan giữa độ dài câu và tỉ lệ trúng: +0,327. Mã: `harness/ground_pilot.py`, tính lại ngày 3/8 — bản cũ ghi 35% là nhớ lệch, không cách chia nào ra đúng số đó.

Hai điều nói thật kèm theo:

- Cặp số này đo trên câu người viết (câu mẫu chuẩn), chưa phải câu mô hình sinh ra.
- Câu tả rõ thường cũng *dài hơn*, nên một phần chênh lệch có thể do độ dài chứ không phải do độ rõ — vì thế kế hoạch có riêng một nhánh đối chứng cho chuyện độ dài (mục 5). Và mỗi nửa chỉ có 38 câu, con số còn dao động.

Cả hai mức của đóng góp đều nhắm thẳng vào bệnh mơ hồ này. Các hướng khác từng cân nhắc thì hoặc nhắm vào bệnh hiếm (chống bịa), hoặc không nhắm vào bệnh nào cụ thể.

### 3.2. Có bằng chứng từ các nghiên cứu trước rằng kiểu can thiệp này giúp — và bằng chứng gần nhà nhất nằm trên chính bộ dữ liệu mình dùng

Ý tưởng "bắt sinh một bước trung gian trước khi ra đáp án cuối" đã được thử ở nhiều bài nghiên cứu. Bảng dưới gom các con số.

Lưu ý khi đọc bảng: cột cuối ghi rõ mỗi bài đo bằng thước gì. Vì các thước khác nhau, những con số này chỉ nói lên *chiều* (tăng hay giảm) và *cỡ độ lớn*, không so thẳng với nhau được.

| Nghiên cứu | Họ làm gì | Kết quả | Đo bằng gì |
|---|---|---|---|
| **Aguvis (hội nghị ICML 2025)** | huấn luyện có tầng suy nghĩ trung gian, thử **trên chính AndroidControl**; khi bỏ tầng trung gian đi… | điểm **tụt 11,4** ở bài chấm theo từng bước; ở bài chấm theo mục tiêu tổng chỉ tụt 1,2 — tức hiệu ứng dồn đúng vào chỗ mình cần | độ đúng của thao tác (bảng 6 của bài) |
| Shikra (bản thảo) | bắt sinh toạ độ trước khi trả lời | **tăng 5,9** | độ đúng câu trả lời — ⚠ đo trên bộ ảnh hình khối nhân tạo CLEVR, với một mô hình thí nghiệm nhỏ chưa qua tiền huấn luyện: bằng chứng yếu nhất bảng |
| GCoT (bản thảo) | *huấn luyện* sinh định vị trước, trả lời sau | **tăng 4,5 và 5,8** trên hai cỡ mô hình | so khớp đáp án một-từ (⚠ có điểm phải khai kèm, xem 3.4) |
| CogCoM (ICLR 2025) | chuỗi thao tác trung gian | tăng 6,6 ở đọc chữ trong ảnh; các bài kiểm khác cùng bảng chỉ +0,2…+0,9 — trích cả cụm để khỏi mang tiếng chọn số đẹp | đọc chữ trong ảnh (bảng 4 của bài) |
| LLaVA-CoT (ICCV 2025) | bốn tầng suy nghĩ có cấu trúc | tăng 3,4 so với huấn luyện thẳng — nhưng số đó gồm cả một bước dò-lại lúc chạy; phần thuần của cấu trúc là **+1,5** | trung bình 6 bài kiểm (bảng 2 của bài) |
| Puduppully (AAAI 2019) | lập dàn ý trước khi viết văn | tăng 2,88 (trên tập phát triển; tập kiểm là +2,31) | điểm BLEU (đo văn sinh) |

Từng con số trong bảng đã được rà lại tận PDF gốc ngày 3/8 (mục 14). Các chú thích ⚠ là kết quả của lượt rà đó, ghi thẳng vào bảng để khi trình không bị bắt bẻ.

Dòng Aguvis đáng giá nhất, vì ba điều:

1. **Cùng bộ dữ liệu** với luận văn (AndroidControl) và cùng kiểu can thiệp.
2. Hiệu ứng lớn nhất bảng.
3. Bộ ba số của họ — tụt 11,4 khi chấm theo từng bước · chỉ tụt 1,2 khi chấm theo mục tiêu tổng · tụt 5,1 trên bộ ScreenSpot — cho thấy hiệu ứng dồn đúng vào thao tác từng bước, chứ không rải đều mọi chỗ. Đúng chỗ luận văn cần.

Không ứng viên nào khác có bằng chứng gần như vậy.

### 3.3. Và có bằng chứng cho biết phải làm ĐÚNG KIỂU nào — đây là chỗ thiết kế hết tuỳ tiện

Cùng ý tưởng "thêm bước trung gian" nhưng có bài làm ra kết quả **âm**. Nhìn kỹ thì thấy quy luật nằm ở *dạng* của bước trung gian:

| Nghiên cứu | Bước trung gian là văn nói tự do | Bước trung gian có cấu trúc / có toạ độ |
|---|---|---|
| Shikra (cùng một mô hình, cùng bài kiểm) | **tụt 7,39** | **tăng 5,90** |
| UI-Ins (ICLR 2026; cùng bài kiểm ScreenSpot-Pro, đo trên **hai** mô hình nền) | **tụt 3,2** trên mô hình nền thứ nhất, **không giúp gì (0)** trên mô hình nền thứ hai | **tăng 2,5 và 4,7** trên đúng hai mô hình nền đó |

Cùng một bài, hai kết quả ngược dấu. Thứ quyết định: bước trung gian phải **có cấu trúc chặt và chứa toạ độ**, không được là một đoạn văn lan man.

Đó chính là lý do dòng khai báo của luận văn có đúng bốn ô cố định và bắt buộc có ô toạ độ — mỗi ràng buộc thiết kế đều có số đứng sau, không phải chọn theo cảm tính.

Một chỉnh quan trọng từ lượt rà 3/8, để trình cho đúng: ở UI-Ins, **không được ghép "−3,2 vs +4,7" thành một cặp đối chứng trên cùng mô hình**. Đó là hai mô hình nền khác nhau: −3,2 đo trên UI-TARS-1.5-7B, còn +4,7 đo trên Qwen2.5-VL-7B (bài in phần trăm tương đối; số ở đây đã quy về điểm phần trăm). Cách nói an toàn: *"văn tự do làm một mô hình tụt và mô hình kia dậm chân; bước trung gian có cấu trúc nâng cả hai"*. Kết luận về *chiều* không đổi, chỉ đổi cách ghép số.

Thêm một lẽ riêng cho ô toạ độ: trong dữ liệu, toạ độ chỗ người thật chạm là **nhãn sạch tuyệt đối và có ở 100% số bước chạm**. Cách huấn luyện thông thường bỏ phí hoàn toàn nguồn này, trong khi ô "tên nút" chỉ đúng khoảng 70–75% (mục 7).

### 3.4. Đã tra kỹ: chưa ai chiếm chỗ này — và biết chính xác chỗ nào KHÔNG được nhận là mới

Bốn vòng tra cứu tài liệu độc lập (ngày 1/8, kiểm tận trang gốc từng bài) cho bức tranh ba phần: chỗ còn trống · chỗ đã có chủ · và một bằng chứng tưởng ngược chiều hoá ra thuận chiều.

**Chỗ còn trống, kiểm được ở ba phía độc lập:**

- Hai bài mới nhất (5–6/2026) về "cho mô hình thông tin đặc quyền lúc huấn luyện trong giao diện" đều bắt mô hình sinh **thuần toạ độ** — một bài viết nguyên văn rằng phần trả lời *"không chứa lập luận ngôn ngữ nào thêm"*. Không bài nào bắt sinh dòng mô tả chữ.
- Cả dòng nghiên cứu mô hình giao diện: chưa bài nào huấn luyện sinh mô tả văn bản làm sản phẩm được chấm. Bài gần nhất (UI-Ins) làm **ngược vai**: chữ là bước trung gian, toạ độ mới là sản phẩm cuối.
- Trong bài gốc AndroidControl, câu mô tả từng bước của người viết được dùng làm **đầu vào**; luận văn đảo lại, dùng nó làm **đích để sinh** — chưa ai làm.

**Chỗ đã có chủ, phải khai và cấm nhận vơ:**

*Thứ nhất, cơ chế phạt câu mơ hồ (mức 2) là đồ đi mượn.* Ý "phạt câu mô tả nếu nó cũng khớp với vật bên cạnh" đã có từ 2016 ở miền ảnh tự nhiên (bài của Mao và cộng sự, CVPR 2016, cùng các bài nối tiếp 2017). Cái còn trống chỉ là: miền giao diện chưa ai làm. Điều thú vị là bài nền của chính miền này (Widget Captioning, EMNLP 2020) **tự nêu ra** lỗi hai biểu tượng giống nhau, nhưng suốt sáu năm cách tính phạt của cả dòng vẫn y nguyên kiểu cũ — mức 2 lấp đúng khe đó. Vì cơ chế là đồ mượn, mức 2 không đứng một mình làm đóng góp chính được; nó là mức sâu thứ hai của cùng một ý.

*Thứ hai, hướng ép "chú ý" đã bị loại.* Hướng từng được kỳ vọng nhất trước đây là can thiệp vào cơ chế chú ý (attention) bên trong mô hình. Loại vì thua ở ba tiêu chí cùng lúc:

1. Ngay trong lúc tra cứu, phát hiện một bài vừa đăng ở hội nghị WACV 2026 làm đúng cơ chế đó, trên đúng dòng mô hình Qwen2.5-VL — chỗ đứng độ mới không còn.
2. Hiệu ứng của cơ chế này lên chất lượng câu chữ, theo nghiên cứu cũ, chỉ cỡ 1 điểm — quá nhỏ để đo được với lực thống kê của luận văn.
3. Tốn 8–10 ngày công cài đặt.

**Một phát hiện đảo chiều đáng kể trong lúc tra: bài GCoT.** Hồ sơ cũ từng lo GCoT là bằng chứng *chống lại* hướng này, vì họ báo rằng bắt định vị trước làm câu trả lời kém đi. Ngày 3/8 đã tải PDF đọc trọn bài (cả hai phiên bản), và bức tranh đầy đủ như sau — ghi hết ở đây để khỏi phải tra lại:

- **GCoT là bài gì.** Hỏi–đáp trên ảnh đời thường (dựng từ Visual Genome), *không phải* giao diện. Họ bắt mô hình sinh chuỗi toạ độ hộp từng bước ("Bước 1: em bé ở [toạ độ]… Bước 2: con gấu cạnh em bé ở [toạ độ]… Đáp án: Tag") rồi mới trả lời. "Độ đúng" của họ là so khớp chuỗi với đáp án một-từ hoặc Có/Không, trên bộ đề 994 mẫu họ tự dựng. Thước khác hẳn thước của luận văn, nên mọi số của họ chỉ đọc được *chiều*, không so thẳng.
- **Số âm là ở chế độ ra lệnh (prompting) mô hình chưa huấn luyện.** Cả 12 mô hình họ thử đều tụt độ đúng khi bị ép định-vị-trước bằng prompt. Lưu ý trích dẫn: con số "−42,8" hay dùng trong hồ sơ **không có trong bài** — đó là số mình tự trừ hai bảng (71,8 của bảng 3 trừ 29,0 của bảng 4, dòng Qwen2.5-VL-3B). Số bài viết thành chữ là **45,4** (trên nhóm câu hỏi thuộc-tính). Muốn dùng 42,8 phải chú thích "tự tính từ Table 3−4"; an toàn hơn là dùng 45,4. Bài cũng tự nhận một phần điểm rớt là do mô hình không tuân được định dạng, không hẳn là "hiểu kém đi".
- **Khi huấn luyện hẳn theo thứ tự đó thì điểm TĂNG.** Bảng 5 cùng bài: tăng 4,5 và 5,8 trên hai cỡ mô hình; cả định vị lẫn độ nhất quán cùng tăng, không đánh đổi. Số đã kiểm đúng với bảng.
- **Nhưng kèm một điểm yếu của họ, phải chủ động khai.** Cách họ huấn luyện là *thay* bộ dữ liệu dạy gốc bằng dữ liệu cùng phân bố với bộ đề, rồi huấn luyện lại từ đầu. Nên +4,5/+5,8 trộn lẫn hai nguyên nhân — thứ tự định-vị-trước, và được học dữ liệu quen đề — và bài **không có thí nghiệm nào tách hai thứ đó ra**. Đây chính là chỗ phép so S1-với-S2 của luận văn **chặt hơn tiền lệ**: cùng một bộ dữ liệu, chỉ đổi đích sinh, nên chênh lệch đo được là của riêng thứ tự sinh. Chủ động nói ra thì thành điểm cộng; chờ bị hỏi thì thành điểm yếu.

Tức bằng chứng tưởng là ngược chiều thực ra thuận chiều với đúng cách làm của luận văn (huấn luyện, không phải ra lệnh) — với điều kiện trích số cho đúng nguồn và khai kèm điểm yếu trên.

### 3.5. Chi phí lắp đặt gần bằng không, nên rủi ro dồn được vào chỗ đáng dồn

Mức 1 chỉ là đổi định dạng dữ liệu dạy — không đụng vào ruột mô hình, không có chỗ cho lỗi lập trình tinh vi.

Nhờ vậy, toàn bộ rủi ro của luận văn dồn về một câu hỏi duy nhất, trung thực: *can thiệp này có tác dụng đủ lớn để đo thấy không?* Mục 6 dành riêng để bảo đảm rằng: nếu có tác dụng thì sẽ đo thấy, còn nếu không có thì kết quả vẫn đọc được.

---

## 4. Một câu hỏi phải trả lời thẳng: "vậy có mỏng quá cho luận văn thạc sĩ không?"

Câu này đã được đặt cho một "hội đồng giả" — giám khảo đóng vai chủ tịch hội đồng khó tính (mục 13). Phán quyết của họ, tóm lại như sau.

Can thiệp mức 1, **đứng trơ trọi một mình, đúng là mỏng**: bản chất kỹ thuật của nó là một ngày viết mã đổi định dạng. Nhưng luận văn không được chấm trên độ phức tạp của can thiệp; nó được chấm trên **độ chặt của phần chứng minh**. Và gói đầy đủ của luận văn này gồm ba tầng, khai rõ từ đầu:

1. **Một mô hình tự huấn luyện cho tác vụ chưa ai huấn luyện** — thoả yêu cầu cứng của trường (luận văn phải có mô hình do học viên huấn luyện).
2. **Thành phần "khai báo trước, phát ngôn sau" ở hai mức**, chứng minh bằng bộ thí nghiệm đối chứng mà nhiều bài đã công bố còn thiếu — trong đó có một nhánh đối chứng (mục 5, nhánh "khai báo giả") mà theo tra cứu chưa nghiên cứu nào từng chạy.
3. **Chương đo lường**: thước chấm tự dựng, tự kiểm bằng cách bơm lỗi vào xem thước có bắt được không, tự đo cả giới hạn của chính nó. Hội đồng giả nhận xét đây là phần *hiếm nhất* so với mặt bằng luận văn thạc sĩ (đa số luận văn dùng thước có sẵn, không ai hỏi thước có đáng tin không) — và yêu cầu phần này phải đứng trong thân luận văn như một đóng góp có tên, không giấu xuống phụ lục.

Hội đồng giả cũng ra sáu điều kiện để "bỏ phiếu cho qua kể cả khi kết quả chính không như ý". Cả sáu đã nằm trong kế hoạch này:

1. Thử nghiệm mức 2 bắt buộc phải chạy (mục 2).
2. Huấn luyện lặp nhiều hạt giống (mục 6.1).
3. Có nhánh đối chứng "nhét thông tin vào đầu vào lúc chạy" — nhánh B-infer (mục 5).
4. Đăng ký trước rồi mới chạy (việc 1 của bảng mục 8).
5. Chấm tay bằng người + bản trình diễn tiếng Việt + kiểm phần bước không-chạm (mục 5, 6.2 và 8).
6. Chương đo lường có tên trong thân luận văn (tầng 3 vừa nói trên).

---

## 5. Cách chứng minh: các phiên bản đem so với nhau

Kế hoạch huấn luyện các phiên bản sau — tất cả dùng cùng một bộ dữ liệu, cùng mô hình gốc, chỉ khác đúng chỗ ghi trong bảng. Danh sách này **khoá trước khi nhìn bất kỳ kết quả nào**: không được thêm bớt sau, kẻo mang tiếng chọn bảng đẹp.

| Tên | Khác gì | Để trả lời câu hỏi gì |
|---|---|---|
| **S1** — bản thường | học viết thẳng ra câu hướng dẫn, không có bước trung gian (cách huấn luyện thông thường) | mốc so sánh |
| **S2** — bản khai báo | học viết dòng khai báo trước, rồi mới tới câu hướng dẫn | **câu hỏi chính: can thiệp có tác dụng không** |
| **S2r** — bản khai báo giả | dòng khai báo đúng cú pháp nhưng nội dung lấy từ màn hình khác, toạ độ bừa; độ dài ghép cho bằng bản thật từng mẫu một | nếu S2 chỉ thắng nhờ "chuỗi dài thêm" hay "quen cú pháp" thì S2r cũng phải thắng — nhánh đối chứng này chưa nghiên cứu nào từng chạy |
| **S2-nopoint** | khai báo đầy đủ nhưng bỏ ô toạ độ | tách riêng phần công của toạ độ |
| **B-infer** — không huấn luyện gì thêm | lấy bản thường S1, lúc chạy nhét dòng mô tả nút (dựng từ cây trợ năng + OCR) vào đầu vào | đối thủ rẻ nhất: nếu chỉ cần nhét thông tin vào đầu vào mà bằng được S2 thì việc huấn luyện mất lý do tồn tại — phải đo để biết mình đứng đâu |
| **S3-pilot** — thử mức 2 | thêm khoản phạt câu mơ hồ (mục 2), chạy trên lát dữ liệu nhỏ 1.697 bước | can thiệp tầng công-thức-phạt có tín hiệu không |

Nhánh S2r cụ thể trông thế này: nếu mẫu thật có khai báo `<desc>ô nhập liệu | "Search Publications..." | <point>500,80</point> | ô nhập liệu duy nhất trên màn</desc>`, thì mẫu tương ứng của S2r mang một dòng đúng cú pháp đó nhưng nội dung lấy từ màn khác, kiểu `<desc>nút bấm | "Back" | <point>48,1900</point> | nút duy nhất góc dưới trái</desc>`, độ dài ghép cho bằng bản thật từng mẫu. Nếu S2 thắng S1 chỉ vì chuỗi dài thêm hay quen cú pháp thì S2r cũng phải thắng y vậy; S2 thắng mà S2r không thắng thì mới chứng minh được *nội dung* của khai báo có tác dụng.

Kèm ba lớp phân tích bắt buộc (không phải phiên bản huấn luyện, mà là cách mổ xẻ kết quả):

- **Cắt theo độ dài câu**: nếu S2 chỉ thắng ở nhóm câu dài thì phải nghi hiệu ứng là do dài, không phải do rõ.
- **Cắt theo độ dễ nhầm của màn hình**: S2 phải thắng đậm hơn ở các màn có nhiều nút giống nhau — thắng đều cả ở màn chỉ có một nút thì cơ chế không phải như mình nghĩ.
- **Chấm tay 100 câu bằng hai người độc lập** (khung chấm đã dựng sẵn từ trước), để kiểm rằng "máy chấm trúng" và "người thấy rõ ràng" là một chuyện.

Và một phép thử riêng, thêm ngày 3/8, tốn ~2 đô:

**Phép thử nhân quả rẻ trên chính bản thường S1, chạy TRƯỚC khi tiêu tiền huấn luyện S2.** Cách làm:

1. Lấy bản S1 đã huấn luyện xong (đằng nào cũng phải huấn luyện S1 trước — trình tự ở mục 6.1).
2. Lúc chạy thử, nhét vào đầu vào từng mẫu một trong hai thứ để so: (i) dòng khai báo *chuẩn*, dựng sẵn từ đáp án thật; hoặc (ii) một đoạn đệm vô nghĩa cùng độ dài.
3. So điểm giữa hai điều kiện.

Phép thử này đo **mức trần** của can thiệp: nếu đưa tận tay khai báo đúng mà điểm vẫn đứng yên, thì huấn luyện S2 khó có cửa — và biết được điều đó ở tuần hai với 2 đô, thay vì tuần bốn với 30 đô. Quy trình này mượn nguyên từ các nghiên cứu đo xem chuỗi suy nghĩ trung gian có thật sự quyết định câu trả lời hay chỉ là đồ trang trí; trình đúng là đồ nhập khẩu, không nhận mới.

---

## 6. Vì sao kết quả sẽ đọc được — phần này quyết định sống chết, xin đọc chậm

Đây là chỗ vòng phản biện ngày 2/8 bắn trúng nhiều nhất, và bản này sửa nhiều nhất. Có ba nguồn nhiễu có thể làm kết quả không đọc được; tiểu mục 6.1 xử từng nguồn, tiểu mục 6.2 nói về chính cái thước chấm.

### 6.1. Ba nguồn nhiễu, và cách xử từng nguồn

**Nguồn 1 — may rủi của phép đo.**

Đo trên ít mẫu thì con số nhảy loạn. Khái niệm cần nhớ: **MDE** (minimum detectable effect) = *mức chênh lệch nhỏ nhất mà phép đo của mình còn phân biệt được với may rủi*.

Nó quyết định sống chết thế này: nếu tác dụng thật của can thiệp là 5 điểm mà MDE của phép đo là 13 điểm, thì dù can thiệp có tác dụng thật, kết quả vẫn ra "không kết luận được" — tiền huấn luyện coi như đổ sông. Theo các nghiên cứu tương tự (bảng mục 3.2), tác dụng kỳ vọng cỡ 3–8 điểm, nên **phải ép MDE xuống dưới mức đó trước khi tiêu tiền huấn luyện**.

Cách ép: bài đo thử trước đây chỉ chấm 91 bước (trung bình 3,5 bước mỗi ứng dụng) — quá ít, MDE khoảng 11–16 điểm. Kế hoạch mới chấm **toàn bộ khoảng 2.000 bước chạm của tập kiểm**, và xử lý tử tế 268 tác vụ không xác định được thuộc ứng dụng nào (hộp kỹ thuật bên dưới). Ước tính MDE hạ về khoảng **4–7 điểm**.

Nhưng — và đây là chỗ vòng phản biện buộc phải sửa cách nói — con số 4–7 là số **ước chiếu** (tính từ giả định), không phải số đo. Nên kế hoạch khoá một trình tự cứng, không đảo thứ tự:

1. Huấn luyện bản thường S1 trước (hai hạt giống).
2. Chấm đủ toàn tập kiểm.
3. Từ số liệu thật, tính MDE thật.
4. Khoá ngưỡng đậu rớt.
5. Lúc đó mới huấn luyện S2.

**Nguồn 2 — may rủi của chính việc huấn luyện.**

Huấn luyện cùng một công thức hai lần vẫn ra hai mô hình lệch nhau vài điểm, do các yếu tố ngẫu nhiên: điểm khởi đầu, thứ tự trộn dữ liệu — gọi chung là *hạt giống ngẫu nhiên* (seed).

Thành ra nếu mỗi phiên bản chỉ huấn luyện một lần, thì "S2 hơn S1 năm điểm" **không phân biệt được** với "hên hạt giống". Hai giám khảo phản biện độc lập cùng bắn trúng lỗ này.

Cách xử: **S1 và S2 mỗi bản huấn luyện 2–3 lần với hạt giống khác nhau**. Cặp S1 của hai hạt giống còn cho luôn một thước quý: chênh lệch giữa chúng chính là *cỡ của nhiễu huấn luyện đo bằng số thật* — mọi hiệu ứng công bố phải vượt được cỡ đó.

**Nguồn 3 — các màn hình cùng một ứng dụng giống nhau.**

20 bước đo trong cùng một ứng dụng không phải 20 bằng chứng độc lập — chúng na ná nhau (cùng giao diện, cùng phong cách đặt tên nút). Nếu đếm như độc lập thì tự lừa mình rằng có nhiều bằng chứng hơn thực tế. Cách xử chuẩn: gom theo ứng dụng rồi mới tính (chi tiết trong hộp).

> **Hộp kỹ thuật — cho người muốn kiểm công thức.**
> · Đơn vị gom cụm: ứng dụng, với 363/631 tác vụ xác định được ứng dụng (78 ứng dụng); **268 tác vụ không xác định được thì mỗi tác vụ là một cụm riêng** — quy tắc này (i) giữ đúng lời hứa "đo trên toàn tập kiểm" thay vì lặng lẽ bỏ 42% dữ liệu, (ii) nâng tổng số cụm từ 78 lên 346, số cụm hiệu dụng (hiệu chỉnh Kish cho cụm to nhỏ không đều) từ ~35 lên ~98.
> · Ước lượng: hiệu số theo cặp trên cùng bước — cùng ảnh, cùng đáp án chuẩn — trung bình trong cụm rồi gộp giữa cụm; khoảng tin cậy bằng wild cluster bootstrap 10.000 lần, hạt giống cố định; nhiều phép so sánh thì hiệu chỉnh Holm.
> · MDE ước chiếu dùng hệ số 2,80 (chuẩn: mức ý nghĩa 5%, lực 80%); giả định tỉ lệ đúng nền ~30%, nhiễu trong-cụm dạng nhị thức. Số của bản cũ (hệ số 3,077, "31 bước mỗi ứng dụng") có lỗi chia sai quần thể — đã bỏ.
> · Phép so "S2 với S2r" là hiệu-của-hiệu, kỳ vọng nhỏ hơn phép chính và chưa có MDE riêng — khai thẳng: kết luận "không phải do độ dài" mang mức chứng cứ thấp hơn kết luận chính.
> · "Lát khó" (nhóm màn dễ nhầm) định nghĩa bằng phần-ba-dưới của phân bố khoảng-cách-tới-nút-cùng-loại-gần-nhất, tính trước khi chấm bất kỳ phiên bản nào; đọc lát bằng khoảng tin cậy của hiệu-của-hiệu, không so hai con số trần trụi.

### 6.2. Thước chấm là gì, và nó đáng tin tới đâu

**Thước chính — tạm gọi là "chấm bằng bộ trỏ".** Quy trình ba bước:

1. Lấy câu mô hình viết ra (ví dụ "Tap the search icon next to Contacts").
2. Đưa cho một bộ trỏ độc lập — một mô hình khác, không dính gì tới mô hình đang được chấm — đọc câu rồi chỉ một điểm lên ảnh.
3. Nếu điểm nó chỉ đúng là nút mà người thật đã chạm (theo dữ liệu chuẩn), câu được tính đúng.

Lý lẽ đằng sau: một câu hướng dẫn tốt là câu mà *một bên thứ ba chưa biết đáp án vẫn tìm ra đúng nút* — đây cũng chính là cách dòng nghiên cứu mô tả vật thể trong ảnh đã chấm từ 2016.

Ba tinh chỉnh đã cài trong mã (`harness/metric_exec.py`):

1. Chỉ tính trúng khi nút chuẩn là nút **gần nhất** với điểm trỏ. Lý do: dung sai kiểu "trong vòng tròn quanh đáp án" quá dễ dãi — 63% số bước có nút khác lọt vòng.
2. Gom các cách nói cùng nghĩa một cú chạm (tap/click/open/chọn). Bản cũ của thước tách chúng thành các loại riêng nên từng bác oan 28,6% số câu.
3. Một luật bắt cặp từ ngược nghĩa cho công tắc bật/tắt.

**Thước này đã tự kiểm bằng cách bơm lỗi** — cấy các lỗi biết trước vào câu rồi xem thước có bắt được không: đạt **8 trên 10 tiêu chí**. Bài học từ vòng phản biện: bản cũ chỉ khoe 8/10 mà giấu 2 tiêu chí rớt, thế là trình đẹp hơn thực tế. Hai tiêu chí rớt, khai đủ ở đây:

1. **Khi bộ trỏ dùng để chấm còn lệch nhiều, thước kết oan quá nửa số câu đúng** (59,2%). Đường cong đã đo: bộ trỏ lệch trung bình 3% chiều rộng màn → chỉ kết oan 2,6% (chấp nhận được); lệch 5% → oan 25%; lệch 8% → oan 42%. Vì vậy có một **cổng bắt buộc ở tuần đầu**: kiểm bộ trỏ chuyên (một mô hình trỏ mạnh, đã xác minh không từng học trên bộ dữ liệu này) xem sai số của nó trên loại màn hình này có đạt mức ~3% không. Không đạt thì theo kế hoạch B ghi sẵn ở mục 8.
2. **Luật bắt từ-ngược-nghĩa chỉ bắt được các cặp có trong bảng tay** — thử trên 83 ca ngoài bảng, bắt được 0%. Nó là lưới thưa cho một chỗ mù nhỏ, khai đúng như vậy.

Và một giới hạn khai trước thay vì đợi bị hỏi: có nghiên cứu mới (hội nghị EACL 2026) chỉ ra bộ trỏ nhạy với cách diễn đạt — đổi cách nói *hợp lệ* của cùng một nút có thể làm bộ trỏ trượt tới 84%. Đây là đạn hội đồng sẽ bắn vào thước. Lá chắn ba lớp:

- chấm tay 100 câu bằng người (mục 5);
- cắt kết quả theo độ dài câu;
- báo kết quả bằng hai cách chấm song song.

**Thước phụ bắt buộc — kiểm "không gây hại".** Thành phần đóng góp chỉ tác động lên các bước *chạm*, chiếm 59% tổng số bước; 41% còn lại là cuộn trang, gõ chữ, mở ứng dụng, chờ, quay lại. Trên 41% đó, bản S2 không được tệ hơn bản thường quá một biên đã định trước.

---

## 7. Nhãn dạy dựng thế nào, chất lượng ra sao

Dòng khai báo trong dữ liệu dạy được dựng **tự động**, không thuê người dán nhãn. Quy trình cho từng bước:

1. Tìm hộp nhỏ nhất trong cây trợ năng chứa điểm người thật đã chạm.
2. Ô "loại phần tử": lấy từ cây.
3. Ô "tên": lấy từ cây; cây thiếu thì lấy chữ OCR đọc được bên trong hộp.
4. Ô "toạ độ": lấy thẳng từ điểm chạm.
5. Ô "khác gì hàng xóm": tính bằng luật đếm (trên màn có mấy phần tử cùng loại, có phần tử nào trùng tên không).

Chất lượng đã đo trên 1.068 bước thật:

- **77% có tên rõ ràng.** Soi tay thấy đôi chỗ tên dính nhầm, nên con số làm việc thận trọng là 70–75%.
- 76% xác định được loại phần tử.
- 20% không có tên. Với nhóm này, mặc định để trống ô tên thay vì đoán bừa — và đã ghi sẵn tiêu chí bằng số cho việc đổi cách xử nếu mặc định này gây hại.
- Ô toạ độ — ô quan trọng nhất — **sạch 100%**, vì lấy từ hành vi người thật.

Một điều trung thực từ vòng phản biện: đoạn mã đo thử chất lượng hiện tại đo một phiên bản khai báo **cũ hơn** bản chốt — ô vị trí còn ghi theo vùng (chia màn thành lưới 3×3 rồi gọi tên vùng) thay vì toạ độ, và ô trùng-tên chưa cài. Phải nâng đoạn mã đó trước khi dựng nhãn thật. Các con số 77%/76% không bị ảnh hưởng, vì hai ô đó không đổi giữa hai phiên bản.

Dữ liệu nguồn: ghép hai bản công khai của AndroidControl — một bản có câu người viết, một bản có ảnh — theo mã tác vụ và mã bước. Phép ghép đã tự kiểm: đối chiếu chữ OCR tại điểm chạm cho tỉ lệ khớp 47%, trong khi cố tình ghép lệch một bước chỉ 27% — chênh gần gấp đôi, chứng tỏ ghép chuẩn. Đã dựng sẵn 1.697 bước làm lát chạy thử; toàn bộ khoảng 82 nghìn bước (67 GB ảnh) sẽ tải về máy thuê khi bắt đầu.

---

## 8. Lịch, tiền, và điểm quyết định

Đơn giá nền: mỗi lần huấn luyện trọn bộ dữ liệu khoảng 13–16 đô (thuê card A100 giá ~0,72 đô/giờ, hai lượt duyệt dữ liệu); chạy thử trên lát nhỏ chỉ 0,3–2 đô.

| # | Việc | Tiền (đô) |
|---|---|---|
| 1 | Viết bản đăng ký trước (thiết kế + luật đọc kết quả), lưu vết bằng git **trước mọi lệnh huấn luyện** | 0 |
| 2 | **Hẹn thầy ngay ngày đầu** — thầy trả lời mất 3–7 ngày, là chỗ chờ duy nhất ngoài tầm kiểm soát; mang theo ba kịch bản kết quả để chốt trước (kể cả kịch bản xấu) | 0 |
| 3 | Bật tải 67 GB ảnh chạy nền từ ngày đầu | 0 |
| 4 | Kiểm bộ trỏ chuyên (cổng sai-số ~3%) + chấm các mốc nền: câu chuẩn, gpt-4o-mini, B-infer | 4–8 |
| 5 | Huấn luyện **S1 hai hạt giống** → chấm đủ → tính MDE thật + cỡ nhiễu huấn luyện → **phép thử nhân quả trên S1** (nhét khai báo chuẩn / đoạn đệm vô nghĩa, mục 5 — ~2 đô đã gồm) → khoá ngưỡng | 26–34 |
| 6 | Nâng mã dựng nhãn → dựng nhãn toàn bộ → huấn luyện **S2 hai hạt giống** → chấm | 26–32 |
| 7 | S2r + S2-nopoint (mỗi bản một hạt giống) → chấm | 26–32 |
| 8 | **Thử mức 2** trên lát nhỏ (bắt buộc) | 3–6 |
| 9 | Chấm tay 100 câu (hai người) · bản trình diễn sinh tiếng Việt (~10 màn, định tính) · kiểm không-gây-hại | 0–2 |
| 10 | Hạt giống thứ ba cho S1/S2 — chỉ khi dải hai-hạt-giống rộng gần bằng hiệu ứng | 0 hoặc 26–32 |
| 11 | Mở rộng mức 2 toàn dữ liệu — chỉ khi bản thử sống | 0 hoặc 12–18 |
| | **Tổng phần chắc chắn** | **85–112** |
| | **Trần nếu kích hoạt cả mục 10 và 11** | **123–162** |

Dưới trần ngân sách 200 đô. Nếu kẹt tiền, thứ cắt trước là *quy mô dữ liệu* (huấn luyện trên hai phần ba, khai thẳng); không cắt hạt giống thứ hai, không cắt bản thử mức 2, không cắt nhánh đối chứng.

### Ba điểm quyết định, tiêu chí ghi sẵn từ bây giờ

**Sau việc 5 — còn chỗ để chứng minh không?** Đo khoảng cách từ bản thường S1 tới trần. Trần ở đây là một con số đo được, không phải 100% lý thuyết: điểm của chính câu chuẩn (câu người viết) khi chấm qua đúng thước này. Nếu khoảng cách S1-tới-trần nhỏ hơn hai lần MDE thật → không còn chỗ để chứng minh gì → **đổi trọng tâm ngay tại buổi gặp thầy** (chương đo lường lên chính, mô hình thành minh hoạ). Quyết ở tuần một thì còn kịp mọi thứ.

**Sau việc 7 — có chênh không?** Chênh lệch rõ → chạy tiếp các mục điều kiện (10, 11). Chênh gần bằng không → **dừng tiêu tiền cho nhánh mới**, dồn thời gian vào phân tích vì sao: hỏng ở loại nút nào, màn kiểu nào, có phải do nhãn nhiễu. Một luận văn kết quả không chênh nhưng phân tích sâu vẫn bảo vệ được; sáu phiên bản không phân tích thì không.

**Trước khi viết chương kết quả:** đóng băng mọi con số, không chạy thêm bất cứ gì.

### Kế hoạch B nếu bộ trỏ chuyên không đạt cổng sai số 3%

Đây là rủi ro lớn nhất toàn kế hoạch (mục 6.2 giải thích vì sao). Kế hoạch B có ba bậc, dùng lần lượt:

1. **Lệch 3–5%:** đổi cách chấm chính sang kiểu vòng-dung-sai, hạ cách chấm chặt (nút-gần-nhất) xuống vai phụ; khai kèm tỉ lệ kết oan theo đường cong đã đo ở mục 6.2.
2. **Tệ hơn nữa:** thử gộp nhiều bộ trỏ.
3. **Vẫn không xong:** chuyển sang so *thứ hạng tương đối* giữa các phiên bản trên cùng thước nhiễu, và nâng chấm tay lên 200 câu thành thước đồng-chính.

Bậc nào kích hoạt cũng **báo thầy ngay tuần một**, không phải tuần bốn.

Vòng phản biện 3/8 bổ sung thêm một đường dự phòng nữa cho đúng tình huống này: thước **"chọn trong danh sách"**. Ý tưởng: thay vì bắt bộ trỏ chỉ đúng pixel, đưa cho một mô hình đọc **danh sách các phần tử trên màn** (dựng từ cây trợ năng) và bắt nó chọn phần tử mà câu mô tả. Ví dụ: câu "Tap the search icon next to Contacts" + danh sách 15 phần tử của màn → mô hình phải chọn đúng dòng ứng với kính lúp cạnh Contacts. Cách này miễn nhiễm với sai số pixel.

Muốn dùng thước này phải qua hai điều kiện ghi trước — chính vòng 3/8 cũng chỉ ra chỗ hỏng nếu làm ẩu:

1. Luật tính đúng phải là "*mọi* hộp chứa điểm chạm đều tính đúng", không được là "hộp nhỏ nhất". Lý do: nhãn dạy của S2 dựng đúng bằng luật hộp-nhỏ-nhất từ cùng cây trợ năng đó — dùng lại luật ấy để chấm là cho mô hình thi đúng đề nó đã học tủ.
2. Mô hình đọc-danh-sách phải **khác họ** với mô hình đang được huấn luyện: không dùng Qwen2.5-VL cỡ nào, không dùng gpt-4o-mini (vì đã là mốc ngoài).

Kèm một giới hạn khai thẳng: thước này đo "phân biệt trong danh sách đóng" — dạng dễ hơn của bài toán. Câu cộc lốc "tap the search icon" vẫn chọn đúng nếu danh sách chỉ có một kính lúp. Nên nó là thước *dự phòng*, không thay được thước chính.

---

## 9. Những câu hội đồng sẽ hỏi, và câu trả lời chuẩn bị sẵn

| Hội đồng hỏi | Trả lời |
|---|---|
| "Toàn bộ 'đóng góp mô hình' của anh là một script đổi định dạng dữ liệu?" | Trả lời bằng thiết kế thí nghiệm, không bằng khẩu hiệu: bộ đối chứng (khai-báo-giả, bỏ-toạ-độ, nhét-vào-đầu-vào, cắt lớp theo độ dài) cô lập được *vì sao* nó chạy — mức chặt chẽ mà nhiều bài đã đăng còn thiếu. Cộng mục mức 2: công thức phạt tự viết, có mã, có số |
| "Bản S2 được dùng THÊM dữ liệu (cây trợ năng, OCR, toạ độ) lúc học — thắng là nhờ thêm dữ liệu chứ đâu phải nhờ cách huấn luyện?" | Thông tin thêm chỉ có **lúc học**; lúc chạy hai bản nhận đầu vào y hệt nhau. Đây là khung "học với thông tin đặc quyền" có tên tuổi trong ngành (Vapnik 2009). Và nhánh B-infer đo trực tiếp: nhét thông tin đó vào đầu vào lúc chạy thì được bao nhiêu |
| "Mỗi bản huấn luyện một lần thì chênh vài điểm là hên xui" | Đúng, nên cặp chính huấn luyện 2–3 hạt giống, và dải chênh giữa các hạt giống được in ngay cạnh kết quả |
| "Nghiên cứu GCoT chứng minh định-vị-trước làm câu trả lời kém đi mà?" | Số âm đó là khi ra lệnh cho mô hình chưa huấn luyện; bảng 5 cùng bài: huấn luyện theo thứ tự đó thì tăng 4,5–5,8. Và tự khai luôn trước khi bị vặn: bảng 5 của họ huấn luyện kèm dữ liệu quen đề nên không tách được hai nguyên nhân — phép so S1-với-S2 của em cùng một bộ dữ liệu, chỉ đổi đích sinh, tách được. Chỗ này em chặt hơn họ (chi tiết mục 3.4) |
| "Sinh bước trung gian trước — chuyện cũ rồi" | Đúng, và luận văn trích đủ các bài đó. Cái chưa ai làm là đảo vai: mọi bài để chữ làm bước trung gian rồi chấm toạ độ; ở đây chữ là sản phẩm cuối và là thứ duy nhất được chấm |
| "Model thắng vì nói dài, mà thước lại thích câu dài" | Nhánh khai-báo-giả ghép độ dài từng mẫu + cắt lớp theo độ dài + công khai mức tương quan thước–độ dài đã đo (+0,327) |
| "Bộ trỏ chấm điểm dễ bị lừa" | Khai trước bằng chính nghiên cứu EACL 2026 (đổi diễn đạt làm trượt tới 84%), kèm chấm tay 100 câu bằng người và báo hai cách chấm |
| "41% bước không phải bước chạm thì sao — model có hỏng phần đó không?" | Có phép kiểm không-gây-hại riêng cho phần đó, in trong bảng phụ |
| "Hướng dẫn 'cho con người' mà không người nào đánh giá?" | Chấm tay hai người/100 câu có hệ số đồng thuận; khảo sát người dùng đúng nghĩa khai là hướng mở |
| "Tiếng Việt đâu?" | Khai phạm vi từ chương một: dữ liệu chuẩn của mảng này là tiếng Anh nên số liệu chạy trên tiếng Anh; kèm bản trình diễn sinh hướng dẫn tiếng Việt (~10 màn) trong phụ lục |
| "Sao không thử bản 7 tỉ tham số?" | 3 tỉ là điểm triển khai trên máy người dùng — đó là lý do tồn tại của bài toán; nút dự phòng 7B (~30 đô) chỉ bấm nếu bản 3B thua mốc ngoài |
| "Người thật hỏi MỘT câu và cần NHIỀU bước — demo tác vụ trọn vẹn đâu?" | Khai phạm vi: luận văn giải bài toán mức từng-bước; ghép chuỗi nhiều bước là hướng mở đã thiết kế nhưng ngoài phạm vi |
| "Mô hình gốc học sẵn cả đống ảnh giao diện — phép chia dữ-liệu-chưa-thấy còn nghĩa gì, mốc so với gpt-4o-mini có nhiễm không?" | Phép so chính là nội bộ (hai bản cùng nền nên miễn nhiễm); riêng mốc ngoài có đoạn bàn về nhiễm dữ liệu viết sẵn |
| "Nhãn dựng bằng máy, tin được không?" | 77% có tên rõ, đã soi tay, con số làm việc 70–75%; ô toạ độ sạch 100%; tiêu chí đổi cách xử ghi sẵn trước khi chạy |
| "Sao không đưa luôn bộ trỏ vào vòng huấn luyện cho mạnh?" | Vì bộ trỏ đồng thời là giám khảo chấm thi — đưa vào là vừa đá bóng vừa thổi còi |
| "3 tỉ tham số so với GPT-4o làm gì?" | Mốc ngoài là gpt-4o-mini; nếu chỉ hoà thì luận điểm là hoà-nhưng-rẻ-hàng-chục-lần và ảnh màn hình không phải rời khỏi điện thoại; "hoà" có biên tương đương đăng ký trước, không nói suông |

**Chữ bị cấm trong toàn luận văn:** "đầu tiên", "mới", "novel" cho cơ chế sinh-trung-gian và cơ chế phạt-mơ-hồ (cả hai đều có tiền lệ, chỉ chuyển miền). Chữ "đầu tiên" chỉ được gắn vào đúng một chỗ: *"mô hình mở đầu tiên được huấn luyện cho việc sinh hướng dẫn giao diện cho người đọc"*.

---

## 10. Các nghiên cứu liền kề và mình khác họ chỗ nào

| Nghiên cứu | Họ làm | Mình khác |
|---|---|---|
| AndroidControl (NeurIPS 2024) | câu mô tả từng bước là **đầu vào** cho máy đoán thao tác | dùng làm **đích sinh**, thứ duy nhất đem chấm |
| Aguvis (ICML 2025) | mô hình tự sinh suy nghĩ + câu chỉ dẫn + thao tác; câu chỉ là trung gian, **không được đánh giá** | câu là sản phẩm cuối cho người đọc |
| UI-Ins (ICLR 2026) | chữ trong thẻ suy nghĩ, toạ độ là sản phẩm | ngược vai hoàn toàn |
| Hai bài "thông tin đặc quyền trong giao diện" 2026 | thông tin đặc quyền là ảnh vẽ khung; đích sinh thuần toạ độ | đặc quyền dạng văn bản có cấu trúc; đích là câu |
| GCoT (bản thảo) | định-vị-trước với ảnh tự nhiên, chấm đáp án một-từ | miền giao diện, đầu ra là câu hướng dẫn, huấn luyện chứ không ra lệnh — và phép so đối chứng của mình tách nguyên nhân sạch hơn (mục 3.4) |
| Widget Captioning (EMNLP 2020) | đặt tên phần tử giao diện, công thức phạt thường; tự nêu lỗi hai icon giống nhau mà không xử | mức 2 lấp đúng khe này |
| GuideMe (CHI 2026) | ra lệnh cho GPT-5 sinh hướng dẫn cho người cao tuổi — chi tiết ngay dưới bảng | không huấn luyện gì; chữ "đầu tiên" của mình gắn vào *được huấn luyện* |
| Mao/Yu/Luo (CVPR 2016–17) | phạt mô tả mơ hồ ở ảnh tự nhiên | chuyển miền + nút hàng xóm dựng tự động từ cây trợ năng; chủ động trích trước khi bị hỏi |
| Bài WACV 2026 về ép "chú ý" | đúng cơ chế từng định làm, trên đúng dòng mô hình | đã rút hướng đó khỏi luận văn (lý do ở mục 3.4) |

**Nói kỹ thêm về GuideMe, vì đây là bài gần với luận văn nhất** (đã kiểm tận nơi ngày 3/8). Đó là một app chạy đè cho người cao tuổi: gửi ảnh màn hình + cây trợ năng lên GPT-5 qua mạng, sinh hướng dẫn từng bước kèm vòng sáng chỉ vào nút (toạ độ do GPT-5 trả, hậu kiểm bằng luật, sai thì rơi về hướng dẫn chỉ-bằng-chữ); đánh giá bằng khảo sát 18 người dùng — **không có thước nào chấm chất lượng câu hướng dẫn**. Ba chỗ luận văn khác họ:

1. Họ không huấn luyện gì, chỉ ra lệnh cho GPT-5 có sẵn; luận văn huấn luyện một mô hình riêng, nhỏ, chạy tại máy.
2. Họ lệ thuộc cây trợ năng lúc chạy — đúng chỗ cách của họ hỏng, vì cây chỉ có 12,6% phần tử ghi tên; luận văn chạy từ ảnh, không cần cây lúc suy luận.
3. Họ không đo chất lượng câu; luận văn có thước định lượng chấm chính câu.

Cơ chế rơi-về-chữ của họ gần giống fallback mô-tả của luận văn → trích được làm trụ thiết kế.

---

## 11. Rủi ro chính và cách đỡ

| Rủi ro | Biết sớm bằng cách nào | Đỡ thế nào |
|---|---|---|
| **Bộ trỏ chuyên không đạt cổng sai số 3%** — mọi thứ treo trên nó | đo ngay tuần một (việc 4) | kế hoạch B ba bậc + thước "chọn trong danh sách" (cuối mục 8) |
| **Tác dụng thật nhỏ hơn mức đo được** — hội đồng giả ước xác suất 40–50% | thấy sau khi chấm đủ | đã ép MDE xuống hết cỡ; nếu vẫn không đủ thì kết quả trắng (không thấy chênh — trong nghề gọi là *null*) nhưng có đăng ký trước + phân tích sâu vẫn là kết quả khoa học đọc được, và luận văn ba tầng không sập vì một tầng |
| Kết quả trắng kép (cả mức 1 lẫn bản thử mức 2 đều không thấy chênh) | — | vẫn là hai kết quả âm có kiểm soát + chương đo lường; điều kiện sống: thầy đồng ý trước với cách đọc này |
| Nhãn khai báo nhiễu kéo S2 xuống (bệnh "văn rác" của Shikra) | soi 100 mẫu khi dựng nhãn; tiêu chí đổi cách xử ghi sẵn | để trống ô tên thay vì đoán; tách phân tích theo nguồn tên để phân biệt "can thiệp vô dụng" với "nhãn kéo xuống" |
| Mô hình học vẹt cú pháp khai báo mà không dùng thông tin | S2 xấp xỉ S2r | chính nhánh S2r được thiết kế để bắt chuyện này |
| Bản thường đã cao sẵn, hết chỗ chứng minh | cổng sau việc 5 | đổi trọng tâm tại buổi gặp thầy, tuần một |
| Nhiễu hạt giống nuốt hiệu ứng | dải chênh hai hạt giống S1 | hạt giống thứ ba (mục 10 bảng tiền) |
| Tải 67 GB đứt, máy thuê bị ngắt | — | bật tải ngày đầu; lưu điểm kiểm mỗi 50 bước, tự nối lại |

---

## 12. Tóm một trang — nếu chỉ nhớ chừng này là đủ

- **Sản phẩm:** mô hình 3 tỉ tham số chạy trên máy, nhìn ảnh màn hình + câu hỏi, viết hướng dẫn cho người đọc — tác vụ chưa mô hình nào được huấn luyện.
- **Đóng góp:** một ý — *buộc mô hình xác định rõ mục tiêu trước khi phát ngôn* — ở hai mức: mức 1 bắt sinh dòng khai báo (loại nút, tên, toạ độ, dấu hiệu phân biệt) trước câu; mức 2 phạt thẳng vào công thức học khi câu viết ra áp vào nút bên cạnh cũng xuôi.
- **Vì sao tin:** nhắm trúng bệnh số một đã đo (câu mơ hồ); bằng chứng cùng kiểu can thiệp trên chính bộ dữ liệu này (+11,4 khi có, đo bằng thước khác); biết chính xác kiểu làm sai để né (trung gian dạng văn tự do cho kết quả âm); khe đã tra kỹ là còn trống; chi phí lắp gần bằng không.
- **Cách chứng minh:** sáu phiên bản đối chứng khoá trước + huấn luyện lặp nhiều hạt giống + thước tự dựng đã tự kiểm (khai cả hai tiêu chí rớt) + phép thử nhân quả rẻ trên S1 trước khi tiêu tiền S2 + trình tự cứng "đo lực thống kê bằng số thật rồi mới khoá ngưỡng rồi mới huấn luyện bản chính". Mọi con số trích dẫn đã rà tận PDF gốc (mục 14); khung đã qua thêm một vòng "có gì tốt hơn không" — chín phương án thay thế, không cái nào thắng.
- **Tiền:** 85–112 đô phần chắc chắn, trần 123–162 — dưới ngân sách 200.
- **Việc tuần này:** hẹn thầy (mang ba kịch bản kết quả đi chốt trước) · viết bản đăng ký trước và commit · bật tải dữ liệu · kiểm bộ trỏ chuyên.
- **Ba thứ đã bỏ, đừng tiếc:** hướng ép-chú-ý (bị bài WACV 2026 chiếm cơ chế, hiệu ứng nhỏ, đắt công) · hướng chống-bịa (bệnh chỉ 0–2%) · mọi con số "MDE 4,4–6,0 là số chốt" kiểu bản cũ (là số ước chiếu, phải đo lại).

---

## 13. File này đã bị "bắn thử" thế nào — lý do để tin nó

Ngày 2/8, bản đầu của file này bị đem cho **ba giám khảo phản biện độc lập** (không ai thấy bài của ai) tấn công theo ba hướng:

- một người soi từng con số, đối chiếu với file kết quả gốc trong máy;
- một người đánh vào thiết kế thí nghiệm và thống kê;
- một người đóng vai chủ tịch hội đồng, hỏi "có đáng luận văn thạc sĩ không".

Tổng cộng 4 đòn chí mạng, 18 đòn nặng, 18 đòn nhẹ. Mọi đòn chí mạng đã kiểm lại bằng file gốc — trúng thật — và bản này sửa theo:

| Đòn trúng | Bản này sửa thành |
|---|---|
| Con số "31 bước mỗi ứng dụng" lấy tử số của quần thể này chia mẫu số của quần thể khác — chuỗi lập luận về lực thống kê gãy | mục 6.1: quy tắc cụm mới, mọi số MDE gắn nhãn "ước chiếu", trình tự "đo thật rồi mới khoá ngưỡng" |
| Mỗi phiên bản huấn luyện một lần thì không tách được hiệu ứng khỏi may rủi huấn luyện (hai giám khảo bắn trùng — dấu hiệu lỗ thật) | S1/S2 nhân 2–3 hạt giống; cặp hạt giống làm thước nhiễu |
| Không có kế hoạch B nếu bộ trỏ chuyên không đạt cổng 3% — cả kế hoạch treo trên một điểm | kế hoạch B ba bậc, cuối mục 8 |
| Khoe "8/10 bơm lỗi" mà giấu 2 tiêu chí rớt; giấu các cách chấm cho kết quả xấu; cặp 35/69 thiếu chú thích đo trên câu chuẩn | mục 6.2 và 3.1 trình đủ cả số xấu lẫn chú thích |
| Nhánh đối chứng "khai báo giả" định nghĩa mơ hồ ("sai/ngẫu nhiên" là hai đối chứng khác nhau; "cùng độ dài" không có đơn vị) | mục 5: chốt một định nghĩa, ghép độ dài theo từng mẫu, luật đọc ghi sẵn |
| 268 tác vụ không xác định ứng dụng bị lặng lẽ bỏ rơi | thành cụm riêng từng tác vụ — giữ đúng lời hứa đo trên toàn tập kiểm |
| Mã đo thử nhãn đo một phiên bản khai báo cũ hơn bản chốt | khai ở mục 7 + đưa việc nâng mã vào lịch |
| Bảng tiền cộng không ra tổng, thiếu tiền chấm điểm và tiền hạt giống | bảng mục 8 làm lại toàn bộ |
| Thiếu các câu thủ: dùng-thêm-dữ-liệu, tiếng Việt, 41% bước còn lại, người-thật-đánh-giá, 7B, nhiễm dữ liệu | bảng mục 9 bổ sung đủ |

Phán quyết cuối của giám khảo vai chủ tịch: **ĐỦ TẦM LUẬN VĂN THẠC SĨ — CÓ ĐIỀU KIỆN**, sáu điều kiện, cả sáu đã nằm trong kế hoạch này (liệt kê ở mục 4).

Kèm một câu đáng ghi lại nguyên ý: *phần lớn luận văn thạc sĩ là "huấn luyện xong báo một bảng số, không khoảng tin cậy, không đối chứng, không đăng ký trước" — kế hoạch này ở trên mặt bằng đó rõ rệt, và cái làm nó ở trên không phải bản thân can thiệp, mà là bộ máy chứng minh bao quanh can thiệp.*

---

## 14. Vòng kiểm ngày 3/8 — rà số tận PDF gốc + hỏi "có phương án nào tốt hơn không"

Sau bản 2/8, ngày 3/8 làm thêm hai việc. Kết quả đã vá hết vào thân file — mục này chỉ ghi lại *đã kiểm gì và lòi ra gì*, để sau này khỏi kiểm lại.

### Việc một — rà từng con số trích dẫn bằng cách đọc tận PDF gốc

Ba lượt đọc độc lập: bài GCoT trọn vẹn, sáu bài của bảng 3.2, và hồ sơ GuideMe. Kết quả:

- Bốn dòng bảng 3.2 **đúng nguyên số**: Aguvis −11,4 · Shikra +5,9 · CogCoM +6,6 · Puduppully +2,88 (mỗi dòng thêm điều kiện đo vào bảng cho chặt).
- Bốn chỗ **phải sửa cách ghi, và đã sửa**:
  1. Cặp 35/69 thành **32/69**, kèm luật chia (mục 3.1 — bản cũ nhớ lệch số).
  2. Con số −42,8 của GCoT là **số tự tính từ hai bảng, không có trong bài**; bài viết 45,4 (mục 3.4).
  3. Hai số UI-Ins thuộc **hai mô hình nền khác nhau**, không được ghép thành cặp (mục 3.3).
  4. LLaVA-CoT +3,4 gồm cả bước dò-lại lúc chạy; phần thuần cấu trúc chỉ +1,5 (bảng 3.2).
- Một điểm yếu của tiền lệ hoá thành **vũ khí**: bảng 5 của GCoT huấn luyện kèm dữ liệu quen đề nên không tách được nguyên nhân — phép so S1-với-S2 của luận văn tách được, chặt hơn tiền lệ (mục 3.4, hàng Q&A mục 9).
- GuideMe kiểm xong tận nơi: **không huấn luyện gì** (chỉ ra lệnh cho GPT-5 qua mạng), đánh giá bằng khảo sát người dùng chứ không chấm câu, và **có** trả toạ độ — chi tiết ở mục 10. Câu "GuideMe không huấn luyện" hết là suy đoán.

### Việc hai — vòng phản biện chín phương án thay thế

Câu hỏi đặt ra: "có phương án nào phức tạp hơn nhưng kỳ vọng kết quả tốt hơn khung đã chốt không?". Cách chạy: ba người đề xuất độc lập theo ba lăng kính (tầng công-thức-phạt · tận dụng dữ liệu sẵn có · độ dày của luận điểm khoa học); mỗi phương án bị một giám khảo khó tính mổ theo năm trục; giám khảo được quyền đo lại số trên dữ liệu thật trong máy — và họ đã đo thật.

Kết quả: **không phương án nào thắng được khung đã chốt.** Không cái nào được nhận thẳng. Hai cái bị loại hẳn:

- *Biến dòng khai báo thành biến ẩn cho mô hình tự đoán:* thông tin đặc quyền vẫn rò rỉ vào theo đường vòng, và kiểu khẳng định nó cần chứng minh đòi lực thống kê lớn hơn cả phép đo chính.
- *Chạy lại thí nghiệm trên bộ Widget Captioning để lấy tiếng "tái lập":* bên đó phần tử đích được *cho sẵn* ở đầu vào — bài toán khác hẳn, nên chạy lại cũng không phải là tái lập; chưa kể nền dữ liệu của nó đã bị gần như mọi mô hình giao diện hiện đại học qua.

Bảy cái còn lại chỉ ở mức "đáng thử nếu rẻ, kèm điều kiện nặng". Vài đòn tiêu biểu cho thấy vì sao khung hiện tại đứng vững:

- Phương án dựng cặp so sánh từ chính câu chuẩn: chết vì **~73% câu chuẩn không chứa dấu hiệu phân biệt nào để mà thao tác** (giám khảo đếm thẳng trên lát 1.697 bước).
- Phương án nâng trọng số cho từ-phân-biệt trong công thức phạt: chết vì cơ chế **đã có chủ** ở miền ảnh tự nhiên (hai bài ECCV 2020 và ACM MM 2021).
- Phương án dạy kèm nhiệm vụ "nghe": chết vì hiệu ứng kỳ vọng **nằm dưới ngưỡng đo được (MDE)** — về thiết kế không thể ra kết luận dương đọc được.

**Ba thứ giữ lại từ vòng này, đều đã vá vào thân file:** giới hạn lệch-nhịp của mức 2 kèm cách vá ở tầng sinh khai báo (mục 2) · phép thử nhân quả rẻ trên S1 trước khi tiêu tiền S2 (mục 5 + việc 5 mục 8) · thước dự phòng "chọn trong danh sách" kèm hai điều kiện chống tự-chấm (cuối mục 8).

---

## Phụ lục — số gốc và chỗ tra (cho lúc cần kiểm)

- Hồ sơ bước (752 tác vụ / 4.066 bước của tập kiểm): chạm có toạ độ 59,1% · cuộn 14,5% · gõ 7,3% · mở ứng dụng 7,1% · chờ 6,5% · quay lại 5,5%.
- Gán ứng dụng: 363/631 tác vụ xác định được (78 ứng dụng); 268 tác vụ còn lại → cụm riêng; số cụm hiệu dụng ~35 → ~98.
- Hình học (lát 76 bước): nút đích trung bình 189×126 điểm ảnh; nút khác gần nhất cách 69 điểm ảnh; bộ trỏ rẻ lệch trung vị 108,8 điểm ảnh (một phép đo khác cho 15% chiều rộng màn — hai điều kiện đo khác nhau, khai cả hai).
- Kết oan theo sai số bộ trỏ: 3% → 2,6% · 5% → 25% · 8% → 42% · 13% → 61%.
- Chênh trần–sàn của thước theo cách chấm (76 bước): vòng dung sai +44,7 · gộp tâm +32,9 · hộp +19,7 · cây trợ năng +6,6 · cây + bộ dò hình +3,9 (hai số cuối thấp vì đo dụng cụ trỏ, không đo câu — chính là lý do cần bộ trỏ chuyên).
- Nhãn khai báo (1.068 bước): 77% tên rõ (làm việc 70–75%) · 20% không tên · 76% loại phần tử rõ.
- Kiểm ghép dữ liệu dạy: khớp 47% so với ghép-lệch 27%. Lát thử 1.697 bước đã dựng tại `harness/dg1_cache/train_ac/`.
- Mã liên quan: `descriptor_label_pilot.py` (dựng nhãn — cần nâng cấp) · `metric_exec.py` (thước) · `exec_injection_validate.py` (bơm lỗi) · `mde_recompute.py` (lực thống kê) · `build_train_data.py`, `prep_ocr_train.py` (dữ liệu) · `train_config.yaml` (cấu hình huấn luyện — cần đổi 4 chỗ: bộ dữ liệu, số lượt duyệt 3→2, bf16 cho máy thuê, thư mục lưu) · `cv_study/` (khung chấm tay).
- Các phát biểu đã rút, cấm dùng lại: "MDE 4,4–6,0 là số chốt" · "8/10 bơm lỗi" không kèm hai mục rớt · "31 bước mỗi ứng dụng" · "GCoT chứng minh định-vị-trước làm câu kém đi" (chỉ đúng ở chế độ ra lệnh) · "SD 0,362 đo từ pilot" · "bài ép-chú-ý còn là bản thảo, khe còn trống" · "câu cộc 35% vs câu rõ 69%" (số đúng: 32/69, chia trung vị 8 từ — mục 3.1) · "−42,8 là số của bài GCoT" (số tự tính; bài viết 45,4 — mục 3.4) · "UI-Ins: văn tự do −3,2 vs có cấu trúc +4,7" ghép thành một cặp (hai mô hình nền khác nhau — mục 3.3) · "GuideMe không đụng toạ độ" (có — GPT-5 trả toạ độ trực tiếp, mục 10).
