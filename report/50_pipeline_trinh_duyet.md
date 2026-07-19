# Pipeline sinh hướng dẫn sử dụng phần mềm từ ảnh giao diện

## Bản trình bày xin duyệt thiết kế — chỉ tập trung vào PIPELINE

> **Mục tiêu buổi này:** xin thầy **duyệt phần thiết kế pipeline**. Tài liệu cố ý **không** đi vào
> bộ thước đo, bộ thí nghiệm hay số liệu — chỉ trình bày *hệ thống sinh hướng dẫn hoạt động thế
> nào và vì sao từng bước được thiết kế như vậy*. Mỗi lựa chọn đều kèm **căn cứ** (một là tiền lệ
> đã bình duyệt, hai là một đối chứng thất bại đo được), để không có chỗ nào là "chọn theo cảm
> tính".
>
> Quy ước gọi tên: nói **"một màn / nhiều màn"**, không dùng ký hiệu nội bộ. Viết đủ chữ trước khi
> viết tắt.

---

## 1. Pipeline giải quyết bài toán gì (một đoạn)

Cho **một ảnh** chụp màn hình phần mềm (hoặc **nhiều ảnh** của cùng một luồng thao tác, đã bị xáo
trộn thứ tự) kèm **một câu hỏi** dạng *"làm sao để…"*, hệ thống sinh ra **hướng dẫn thao tác theo
từng bước cho người đọc làm theo**, bám sát đúng những gì có trên ảnh.

Điểm khó trung tâm — và cũng là lý do pipeline phải được thiết kế cẩn thận — là: các mô hình
ngôn ngữ thị giác **hay "bịa" nút không tồn tại** (ví dụ bảo người dùng bấm một nút "Cài đặt"
trong khi màn hình không hề có nút đó). Người dùng làm theo sẽ tắc. Vì vậy pipeline không chỉ
*sinh*, mà còn *tự kiểm và né bịa*.

---

## 2. Sơ đồ tổng quan — MỘT hệ thống, một bộ định tuyến theo số ảnh

Hệ thống là **một pipeline duy nhất**. Một bộ định tuyến ở đầu vào quyết định đường đi:

```
                 ┌─────────────────────────────────────────────┐
   Đầu vào  ──►  │  BỘ ĐỊNH TUYẾN: đếm số ảnh                    │
 (ảnh + câu hỏi) └───────────────┬──────────────────┬───────────┘
                          1 ảnh  │                  │  N ảnh (xáo trộn)
                                 ▼                  ▼
                                 │        ┌──────────────────────┐
                                 │        │ BƯỚC SẮP LẠI THỨ TỰ  │  (chỉ khi nhiều màn)
                                 │        │  các màn (Mục 4)     │
                                 │        └──────────┬───────────┘
                                 │                   │  chuỗi màn đã đúng thứ tự
                                 ▼                   ▼
                    ┌───────────────────────────────────────────┐
                    │  NHÁNH MỘT MÀN — 3 hộp (Mục 3)             │
                    │  ① Sinh mù → ② Đối chiếu → ③ Né bịa        │  (chạy cho từng màn)
                    └───────────────────┬───────────────────────┘
                                        ▼
                            Hướng dẫn từng bước, bám ảnh
```

- **Một ảnh** → đi thẳng vào **nhánh một màn** (3 hộp).
- **Nhiều ảnh** → thêm **một bước sắp lại thứ tự các màn** ở đầu, rồi mới chạy nhánh một màn cho
  từng màn.
- Khi chỉ có một ảnh, bước sắp thứ tự rỗng, hệ về đúng nhánh một màn. **Không có hai hệ tách rời**
  — nhánh nhiều màn *thừa kế trọn* nhánh một màn và chỉ thêm một bước ở đầu.

---

## 3. Nhánh một màn — ba hộp: SINH → ĐỐI CHIẾU → NÉ BỊA

Triết lý: **sinh trước, kiểm sau, chỗ nào bịa thì hạ xuống mô tả** — thay vì tin tưởng mô hình
sinh đúng ngay từ đầu.

### 3.1. Hộp ① — Sinh mù

Mô hình ngôn ngữ thị giác **chỉ nhận ảnh và câu hỏi**, sinh ra bản hướng dẫn nháp. Ở bước này:

- **Không** đưa cho mô hình danh sách nút thật của màn hình.
- **Câu hỏi cũng không chứa tên nút** — nên mô hình buộc phải tự đọc ảnh để gọi tên nút. Đây chính
  là chỗ nó có thể bịa.

> **Vì sao cố tình "bịt mắt" mô hình?** Vì mục tiêu là **đo và chặn được ảo giác**. Nếu ngay từ đầu
> đã đưa danh sách nút thật, mô hình chép lại là xong — ta không còn quan sát được nó *tự* bịa bao
> nhiêu, và cũng không kiểm chứng được cơ chế chống bịa có tác dụng thật hay không. Sinh mù là điều
> kiện để phần "kiểm" phía sau có ý nghĩa.

### 3.2. Hộp ② — Đối chiếu từng bước với giao diện thật

Một **thuật toán so khớp ngữ nghĩa** (không phải mô hình ngôn ngữ thứ hai) đối chiếu **từng bước**
trong bản nháp với **danh sách nút thật của màn** (lấy từ cây phân cấp giao diện — View Hierarchy):

- Tên nút mà bước nhắc tới **khớp** một nút thật (độ tương đồng ≥ ngưỡng) → **giữ nguyên**.
- Không khớp nút nào → đánh dấu là **ảo giác**, chuyển sang hộp ③.

Điểm quan trọng: so khớp bằng **ngữ nghĩa**, không so chuỗi cứng — nên *"Save changes"* và *"Save"*
được coi là cùng một nút, không bị quy oan là bịa.

> **Về ngưỡng so khớp (nói thẳng để không bị bắt hớ):** ngưỡng hiện là **giá trị khởi điểm** đặt từ
> một phép thử nhanh (cặp đồng nghĩa rơi ~0,6–0,69; cặp khác nghĩa ~0,39; cắt ở giữa). Đây **chưa
> phải** ngưỡng đã hiệu chỉnh chặt — bước hiệu chỉnh chuẩn (gán tay 80–120 cặp, chọn điểm đạt độ
> chính xác ≥0,95, đông cứng trước khi nhìn kết quả) đã được thiết kế và sẽ chạy. Ngoài ra kết quả
> sẽ báo theo **đường cong quét nhiều ngưỡng**, không chốt một điểm — nên không thể "vặn ngưỡng cho
> ra số đẹp".

### 3.3. Hộp ③ — Né bịa: CHỈ MÔ TẢ, không đoán nút khác

Với bước bị đánh dấu ảo giác, hệ **viết lại thành một mô tả khái quát bằng lời**, và **tuyệt đối
không suy đoán một nút thật khác để thay vào**.

Ví dụ: màn chỉ có *hour, minute, PM, OK, Cancel*; mô hình lỡ sinh *"Mở Cài đặt"* → hệ viết lại
thành *"Tìm mục cài đặt liên quan trên màn hình"*, **không** tự gán bừa thành "OK" hay "Cancel".

> **Vì sao "chỉ mô tả" mà không "đoán nút gần nhất" — đây là kết luận từ thực nghiệm, không phải
> lựa chọn tuỳ tiện.** Phương án "đoán nút gần nhất" nghe hợp lý nhưng khi chạy thử tạo ra **lỗi
> ngầm**: nó thay bước bịa bằng một nút **có thật nhưng sai chức năng** — hướng dẫn *trông đúng* (vì
> gọi tên một nút tồn tại) nhưng dẫn người dùng **bấm nhầm mà không hay biết**. Lỗi kiểu này **nguy
> hơn cả để nguyên bước bịa**, vì bịa lộ liễu thì người ta còn nghi, còn nút-thật-nhưng-sai thì
> không. Vì đã *đo được* phương án thay thế này thất bại, quyết định "chỉ mô tả" trở thành một kết
> luận nghiên cứu, không phải quy ước. *(Đã quan sát trên mẫu thí điểm; thí nghiệm đối chứng toàn
> mẫu đã thiết kế.)*

### 3.4. Ví dụ chạy đầu–cuối (một màn)

**Màn:** hộp thoại đặt giờ. **Nút thật:** hour, minute, PM, OK, Cancel.
**Câu hỏi:** *"Cần thao tác gì để đặt giờ 20:35 và xác nhận?"*

| Hộp ① — Bản nháp mô hình sinh mù | Hộp ② — Đối chiếu nút thật | Hộp ③ — Kết quả |
|---|---|---|
| "Chọn giờ 8, phút 35" | khớp hour, minute | **giữ nguyên** |
| "Chọn buổi PM" | khớp PM | **giữ nguyên** |
| "Mở **Cài đặt** để lưu" | không có nút Settings → **ảo giác** | **viết lại**: "Tìm mục cài đặt liên quan trên màn hình" |
| "Chọn **OK**" | khớp OK | **giữ nguyên** |

Bản giao cho người đọc: *(1) Chọn giờ 8, phút 35; (2) Chọn buổi PM; (3) [mô tả] Tìm mục cài đặt
liên quan; (4) Chọn OK.* — **Không còn bước nào trỏ tới nút không tồn tại.**

---

## 4. Nhánh nhiều màn — thêm MỘT bước sắp lại thứ tự các màn ở đầu

Khi đầu vào là nhiều ảnh **đã bị xáo trộn**, hệ phải tự khôi phục thứ tự đúng trước khi sinh hướng
dẫn. Bước này gồm bốn phần, đi từ đơn giản đến xử lý mâu thuẫn:

### (a) So từng cặp
Mô hình được hỏi **từng cặp màn một**: *"màn nào diễn ra trước?"*. Hỏi theo cặp cho phán đoán ổn
định hơn hẳn kiểu bắt mô hình xếp cả dãy một lần.

### (b) Tổng hợp bằng điểm Copeland
Đếm, với mỗi màn, **số cặp mà nó thắng** (được xếp đứng trước). Màn thắng nhiều đứng trước. Ví dụ
ba màn A, B, C: nếu A trước B, A trước C, B trước C → A thắng 2, B thắng 1, C thắng 0 → thứ tự
**A < B < C**. Cách này đơn giản, tái lập được, và để lại dấu vết để dò mâu thuẫn.

### (c) Phá vòng mâu thuẫn
Nếu các phán đoán cặp "cắn đuôi nhau" (A trước B, B trước C, nhưng C lại trước A), hệ **cắt ít phán
đoán nhất để hết vòng** rồi mới xếp. Trọng số để quyết cắt cạnh nào lấy từ **mức chênh điểm Copeland
/ tính nhất quán khi hỏi lặp / số cạnh phải bỏ tối thiểu** — **không** dùng độ tin cậy do mô hình tự
khai (mô hình hiệu chỉnh độ tin cậy kém, tin vào nó sẽ sai).

### (d) Năm tín hiệu thứ tự
Để trả lời "mô hình dựa vào đâu mà biết màn nào trước": gating (màn này mở khoá màn kia), nút điều
hướng (Next/Back), thay đổi trạng thái (ô trống → đã điền, công tắc bật/tắt), tiến trình tiêu đề,
và đi sâu vào chi tiết (drill-down).

Sau khi có chuỗi đúng thứ tự, hệ **chạy nguyên nhánh một màn (3 hộp) cho từng màn** — nên mọi bước
vẫn được đối chiếu và né bịa đầy đủ.

> **Một cổng an toàn quan trọng:** trước khi tin vào thứ tự do bước này sinh ra, hệ **đo độ chính xác
> so cặp thô của mô hình**. Nếu nó chỉ đúng xấp xỉ 50% (ngang đoán mò), hệ **tuyên bố bước sắp thứ tự
> vô hiệu và khai thẳng**, thay vì trình bày một kết quả đẹp giả tạo. Đây là cam kết trung thực gắn
> sẵn trong thiết kế.

---

## 5. Luật vàng chống rò rỉ — phân biệt "lúc CHẤM" và "lúc TRIỂN KHAI"

Đây là điểm phòng thủ then chốt, hay bị hiểu nhầm nhất:

- **Danh sách nút thật (View Hierarchy) và đáp án đúng CHỈ được dùng ở bước đánh giá** (để nhà nghiên
  cứu đo hệ bịa bao nhiêu). Chúng **không** được đưa vào lúc sinh hay lúc sắp thứ tự.
- Trong **hệ triển khai thật**, quy trình là **sinh → kiểm → né bịa**. Phần "kiểm" dùng **bất kỳ
  nguồn nút nào có sẵn tại chỗ**. Trên điện thoại Android, hệ điều hành cấp **cây trợ năng theo thời
  gian thực** cho màn đang mở — nên máy người dùng thường vẫn có danh sách nút thật để đối chiếu.
- Khi **hoàn toàn không có nguồn nút nào**, hệ **xuống cấp an toàn**: mô tả việc cần làm bằng lời
  thay vì bịa tên nút, và báo minh bạch tỉ lệ bước phải hạ thành mô tả.

> Nói gọn: *"Chấm baseline"* là một bước **đánh giá**, không phải một bước trong hệ khi chạy thật.
> Hệ khi deploy chỉ gồm **sinh → kiểm → né bịa**. Nhờ tách bạch này, con số ảo giác đo được là ảo
> giác **thật** của mô hình, không phải do ta rò đáp án cho nó.

---

## 6. Vì sao pipeline này "không bắt bẻ được" — mỗi lựa chọn một căn cứ

Đây là phần cốt lõi để thầy duyệt: **không có bước nào đặt ra theo cảm tính**. Mỗi quyết định dựa
trên **một tiền lệ đã bình duyệt** (kèm con số cụ thể của công trình gốc) hoặc **một đối chứng thất
bại đo được**. Bảng dưới là bản tra nhanh; phần sau nói kĩ từng căn cứ.

| # | Lựa chọn thiết kế | Loại căn cứ | Nguồn |
|---|---|---|---|
| 1 | Sinh mù trước, đối chiếu sau (tách nhỏ → kiểm với nguồn ngoài) | tiền lệ | FActScore (EMNLP 2023) + FaithScore (Findings EMNLP 2024) |
| 2 | Khớp tên nút bằng ngữ nghĩa, không so chuỗi cứng | tiền lệ | ALOHa (NAACL 2024) |
| 3 | Chỉ mô tả, KHÔNG đoán nút gần nhất | đối chứng thất bại đo được | quan sát trên mẫu thí điểm |
| 4 | Không coi danh sách nút là chuẩn vàng → hậu kiểm + né bịa | tiền lệ | Chen et al. (ICSE 2020, Distinguished Paper) |
| 5 | So từng cặp thay vì bắt mô hình xếp cả dãy | tiền lệ | Qin et al. (Findings NAACL 2024) |
| 6 | Tổng hợp phán đoán cặp bằng điểm Copeland | tiền lệ | Dwork et al. (WWW 2001) + Saari & Merlin (1996) |
| 7 | Cắt ít phán đoán nhất để phá vòng mâu thuẫn | tiền lệ | Ailon, Charikar & Newman (J. ACM 2008) |
| 8 | Không dùng độ tin cậy mô hình tự khai để phá vòng | đối chứng / nguyên tắc | (giải thích ở dưới) |
| 9 | Cổng đo độ chính xác so cặp trước khi tin bước sắp thứ tự | nguyên tắc trung thực | (giải thích ở dưới) |

### Chi tiết từng căn cứ

**① Sinh mù trước, đối chiếu sau.**
*Nguồn:* **FActScore** (Min et al., EMNLP 2023) và **FaithScore** (Jing et al., Findings EMNLP 2024).
*Nguồn nói gì:* FActScore tách một đoạn văn thành các "sự thật nguyên tử" rồi tính tỉ lệ được một
nguồn tri thức ngoài hậu thuẫn — đo được tiểu sử do ChatGPT sinh chỉ đạt **58%** (tức 42% chi tiết
không có nguồn đỡ), trong khi bộ ước lượng tự động của họ sai **dưới 2%** so với người. FaithScore
là thước **không cần đáp án mẫu** cho mô hình ảnh-ngôn ngữ: tách câu sinh thành sự thật nguyên tử
rồi kiểm nhất quán với ảnh, và tương quan cao với phán đoán trung thực của con người.
*Vì sao hậu thuẫn:* hai bài này hợp thức hoá đúng lối "tách nhỏ đầu ra rồi kiểm từng mảnh với một
nguồn ngoài" — ta áp: tách hướng dẫn thành từng bước, kiểm từng bước với danh sách nút thật.
*Ranh giới (khai thẳng):* cả hai **chỉ chấm văn bản có sẵn, không sinh**. Việc đặt bước *sinh mù*
làm khâu đầu của một pipeline sinh là phần mới của luận văn.

**② Khớp tên nút bằng ngữ nghĩa, không so chuỗi cứng.**
*Nguồn:* **ALOHa** (Petryk et al., NAACL 2024).
*Nguồn nói gì:* dùng mô hình ngôn ngữ đo ảo giác theo **từ vựng mở**, bỏ so-chuỗi cố định kiểu
CHAIR; bắt được **nhiều hơn 13,6%** ảo giác trên tập HAT và **nhiều hơn 30,8%** trên nocaps (đối
tượng ngoài danh mục quen thuộc).
*Vì sao hậu thuẫn:* biện minh cho việc khớp tên nút bằng ngữ nghĩa — nhờ đó *"Save changes"* và
*"Save"* được coi là cùng nút, không bị quy oan là bịa; đồng thời vẫn bắt được nút thật sự không
tồn tại.
*Ranh giới:* ALOHa làm ở miền chú thích ảnh; ta mượn nguyên lý khớp-ngữ-nghĩa, áp vào so tên nút
với cây giao diện.

**③ Chỉ mô tả, KHÔNG đoán nút gần nhất.**
*Loại căn cứ:* **đối chứng thất bại đo được** (không phải quy ước).
*Quan sát được:* trên mẫu thí điểm (10 màn của một app), phương án cũ "đoán nút gần nhất" tạo ra
**lỗi ngầm** — thay bước bịa bằng một nút *có thật nhưng sai chức năng*. Ví dụ ghi lại được: nút
đúng là *"Submit"* bị thay thành *"Navigate up"*; *"ADD LOCATION"* bị thay thành *"Copy project"*
(độ tương đồng chỉ 0,49); *"+"* bị thay thành *"More options"* (0,65). Người làm theo sẽ bấm sai
mà không hề hay biết.
*Vì sao hậu thuẫn:* vì đã *đo được* phương án thay thế thất bại, quyết định "chỉ mô tả" là kết luận
rút từ thực nghiệm. Phương án "chỉ mô tả" có **lỗi ngầm bằng 0 theo cấu trúc** (không bao giờ gán
tên nút mới), đổi lại một tỉ lệ bước phải hạ thành mô tả — cái giá được báo minh bạch.
*Trạng thái:* đã quan sát ở mẫu thí điểm; thí nghiệm đối chứng toàn mẫu (có khoảng tin cậy) đã
thiết kế, sẽ chạy cùng đợt chính. **Không** phát biểu là "đã chứng minh trên toàn bộ".

**④ Không coi danh sách nút là chuẩn vàng.**
*Nguồn:* **Chen et al.** (*Unblind Your Apps*, ICSE 2020, Distinguished Paper).
*Nguồn nói gì:* phân tích quy mô lớn cho thấy phần lớn phần tử bấm-được thiếu nhãn trợ năng — ở cấp
phần tử, **76,68%** ảnh bấm-được và **57,01%** nút-ảnh không có nhãn; ở cấp ứng dụng, khoảng **62%**
app có nút-ảnh không nhãn.
*Vì sao hậu thuẫn:* vì metadata giao diện tự nó đã khuyết nhiều, ta **không** coi nó là chân lý
tuyệt đối mà chỉ dùng ở mức *hậu kiểm rồi né bịa* — có nguồn nút thì rà, thiếu nguồn thì mô tả. Đây
cũng là trụ khái niệm cho luật "chỗ bịa chỉ mô tả": đoán nút dựa trên metadata khuyết nhãn là sai
ngầm.
*Lưu ý gọi số cho đúng:* ~77% là con số ở **cấp phần tử** (ảnh bấm-được), không phải "77% ứng dụng
thiếu nhãn".

**⑤ So từng cặp thay vì bắt mô hình xếp cả dãy.**
*Nguồn:* **Qin et al.** (*Pairwise Ranking Prompting*, Findings NAACL 2024).
*Nguồn nói gì:* đưa hai ứng viên và hỏi cái nào hơn (so cặp). Trên 7 tác vụ BEIR, cách so cặp vượt
ChatGPT **4,2%** và vượt cách chấm từng-cái (pointwise) **hơn 10%** theo NDCG@10.
*Vì sao hậu thuẫn:* hợp thức hoá quyết định hỏi mô hình *từng cặp màn* thay vì bắt nó xếp cả danh
sách một lần — so cặp cho phán đoán ổn định hơn.
*Ranh giới:* họ xếp hạng tài liệu theo độ liên quan; ta áp so-cặp cho *thứ tự thời gian giữa các
màn*, rồi tổng hợp thêm bằng Copeland.

**⑥ Tổng hợp phán đoán cặp bằng điểm Copeland.**
*Nguồn:* bài toán tổng hợp hạng — **Dwork et al.** (*Rank Aggregation Methods for the Web*, WWW
2001); phương pháp Copeland — **Saari & Merlin** (Economic Theory 8:51–76, 1996).
*Nguồn nói gì:* Dwork et al. hình thức hoá bài toán gộp nhiều xếp hạng nguồn thành một, nêu bài
toán Kemeny-Young (NP-hard) và đề xuất thuật toán MC4. Copeland (theo Saari–Merlin) là quy tắc
**đếm số "trận thắng đối đầu"** để xếp hạng.
*Vì sao hậu thuẫn:* trong khung tổng hợp hạng đã bình duyệt, ta chọn Copeland vì nó **đơn giản, tái
lập được và để lại dấu vết bắt mâu thuẫn** (đếm được cặp nào thắng cặp nào).
*Ranh giới (bẫy hay bị hỏi):* Dwork et al. **không** dùng Copeland — chữ ký của họ là Markov-chain/
Kemeny. Ta *chọn* Copeland trong khung đó; trụ đúng-danh cho Copeland là Saari & Merlin.

**⑦ Cắt ít phán đoán nhất để phá vòng mâu thuẫn.**
*Nguồn:* **Ailon, Charikar & Newman** (*Aggregating Inconsistent Information*, J. ACM 55(5), 2008;
bản sơ bộ STOC 2005).
*Nguồn nói gì:* với thông tin mâu thuẫn (dạng giải đấu), tìm thứ tự nhất quán toàn cục *cực tiểu hoá
bất đồng*; kích thước **tập cung phản hồi tối thiểu** bằng số cạnh lùi ít nhất mà một thứ tự tuyến
tính gây ra; bài cho thuật toán xấp xỉ có bảo đảm.
*Vì sao hậu thuẫn:* khi các phán đoán cặp tạo vòng (A trước B, B trước C, C trước A), ta *cắt ít
cạnh nhất để hết vòng* — đúng bài toán này. Ta dùng phát biểu bài toán làm nền cho bước phá vòng.

**⑧ Không dùng độ tin cậy mô hình tự khai để phá vòng.**
*Loại căn cứ:* nguyên tắc dựa trên hạn chế đã biết của mô hình ảnh-ngôn ngữ.
*Lý do:* mô hình ảnh-ngôn ngữ **hiệu chỉnh độ tin cậy kém** — con số "tôi chắc 90%" nó tự khai
không tương ứng với xác suất đúng thật. Nếu lấy đó làm trọng số cắt cạnh sẽ cắt nhầm.
*Ta làm gì thay thế:* lấy trọng số từ **dữ liệu quan sát được** — mức chênh điểm Copeland, tính nhất
quán khi hỏi lặp cùng một cặp, và tiêu chí số cạnh phải bỏ tối thiểu — thay vì tin lời mô hình tự
khai.

**⑨ Cổng đo độ chính xác so cặp trước khi tin bước sắp thứ tự.**
*Loại căn cứ:* nguyên tắc trung thực gắn sẵn trong thiết kế.
*Cơ chế:* trước khi tổng hợp thứ tự, hệ đo độ chính xác so cặp **thô** của mô hình so với đáp án
đúng. Nếu chỉ xấp xỉ 50% (ngang đoán mò), hệ **tuyên bố bước sắp thứ tự vô hiệu và khai thẳng**,
biến kết quả xấu thành một phát hiện hợp lệ về giới hạn của mô hình — thay vì trình bày một thứ tự
đẹp nhưng vô căn cứ.

> **Về nỗi lo "cơ chế đơn giản, đóng góp ở đâu":** phần kiểm và né bịa cố ý giữ đơn giản để **triển
> khai được và độc lập với mô hình**. Giá trị khoa học không nằm ở độ phức tạp mã nguồn, mà ở **phát
> hiện thực nghiệm** (đo được ảo giác trên nhiều đời mô hình, đối chứng được phương án thất bại, đo
> được năng lực sắp thứ tự). Nhiều công trình ở hội nghị hàng đầu có quy trình gọn tương tự mà giá
> trị nằm ở phát hiện và cách đo: G-Eval, SelfCheckGPT, FActScore, RAGAS, ALOHa.

---

## 7. Nền học thuật của pipeline (khai đúng ranh giới)

Pipeline **không sao chép trọn từ một công trình nào**. Nó **kế thừa khung đánh giá không cần đáp
án mẫu** từ Chim, Ive & Liakata (*Computational Linguistics* 51(1), 2025 — bài neo của đề tài), rồi
**mượn kỹ thuật** cho từng bước như bảng Mục 6. Hai chỗ là **đóng góp mới của luận văn**, không mượn
từ ai:

1. **Đặt "sinh mù" làm bước đầu** của một pipeline sinh — để đo được ảo giác. (FActScore/FaithScore
   chỉ *chấm* văn bản có sẵn, không sinh.)
2. **Luật "chỉ mô tả, không đoán nút"** — rút ra từ đối chứng thất bại lỗi ngầm.

Ranh giới phải nói thẳng nếu thầy hỏi: FActScore không sinh (chỉ chấm); Dwork đặt nền bài toán tổng
hợp hạng nhưng **không** dùng Copeland (trụ Copeland là Saari & Merlin); tín hiệu thứ tự trên miền
giao diện là chỗ đóng góp mới, nên năng lực thật được **tự đo lại qua cổng** chứ không mượn kết luận
từ miền khác.

---

## 8. Hỏi–đáp phòng thủ (các đòn hay gặp nhất về pipeline)

**H1 — "Sao không đưa luôn danh sách nút cho mô hình lúc sinh để nó khỏi bịa?"**
Vì mục tiêu là *đo và chặn được ảo giác*. Đưa danh sách nút lúc sinh thì lỗi bị che, không quan sát
được mô hình tự bịa bao nhiêu, và không kiểm chứng được cơ chế chống bịa. Khi *triển khai* có thể
đưa; khi *nghiên cứu* cố ý tách ra.

**H2 — "Bước kiểm chỉ là so tên nút rồi thay bằng mô tả — vậy đâu là nghiên cứu?"**
Đóng góp nằm ở *phát hiện*, không ở độ phức tạp: có đối chứng một phương án thay thế thất bại đo
được (đoán nút → lỗi ngầm), đo ảo giác trên nhiều đời mô hình, và có cổng đo năng lực sắp thứ tự.

**H3 — "Thực tế nhiều app không có sẵn danh sách nút thì hệ chạy kiểu gì?"**
Tách "lúc chấm" và "lúc triển khai" (Mục 5). Trên điện thoại, hệ điều hành cấp cây trợ năng theo
thời gian thực. Khi hoàn toàn không có nguồn nút, hệ xuống cấp an toàn: mô tả bằng lời thay vì bịa
tên nút, và báo tỉ lệ bước phải hạ thành mô tả.

**H4 — "Vì sao chỉ mô tả mà không đoán nút gần nhất cho hướng dẫn cụ thể hơn?"**
Vì đoán nút tạo lỗi ngầm — nút thật nhưng sai chức năng, dẫn người dùng bấm nhầm mà không biết,
nguy hơn cả để nguyên bước bịa. Đây là kết luận rút từ thực nghiệm.

**H5 — "Ngưỡng so khớp lấy con số đó ở đâu, có phải chọn cho đẹp?"**
Hiện là ngưỡng khởi điểm từ một phép thử nhanh, *đã khai thẳng là chưa hiệu chỉnh chặt*. Bước hiệu
chỉnh chuẩn (gán tay, chọn theo độ chính xác, đông cứng trước khi nhìn kết quả) đã thiết kế; kết quả
báo theo đường cong quét nhiều ngưỡng, không chốt một điểm.

**H6 — "Nhiều màn: nhỡ mô hình sắp thứ tự sai bét thì sao?"**
Đã có cổng đo độ chính xác so cặp trước khi tin: nếu ngang đoán mò thì khai thẳng bước sắp thứ tự
vô hiệu, biến kết quả xấu thành một phát hiện hợp lệ về giới hạn của mô hình — không che.

---

## 9. Phạm vi xin duyệt hôm nay

- **Xin thầy duyệt:** *thiết kế pipeline* ở tài liệu này — hợp đồng đầu vào/đầu ra, kiến trúc một
  hệ có bộ định tuyến, ba hộp của nhánh một màn, bốn phần của bước sắp thứ tự nhiều màn, luật vàng
  chống rò rỉ, và các căn cứ ở Mục 6.
- **Chưa bàn hôm nay (sẽ trình riêng):** bộ thước đo chi tiết, bộ thí nghiệm và ngưỡng đậu/rớt, số
  liệu kết quả. Những phần này đã có ở các tài liệu khác và sẽ xin duyệt ở buổi sau.

> **Câu chốt xin duyệt:** *"Pipeline gồm ba hộp sinh–kiểm–né-bịa cho một màn, cộng một bước sắp lại
> thứ tự cho nhiều màn; mỗi lựa chọn thiết kế đều có căn cứ là một tiền lệ đã bình duyệt hoặc một
> đối chứng thất bại đo được; danh sách nút và đáp án chỉ dùng lúc chấm, không rò vào lúc sinh. Em
> xin thầy duyệt phần thiết kế này trước khi triển khai đo đạc."*
