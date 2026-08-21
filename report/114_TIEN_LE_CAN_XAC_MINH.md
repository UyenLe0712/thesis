# 114 — Tiền lệ do phản biện trả về: CHƯA XÁC MINH, cấm trích thẳng (17/8/2026)

> ⛔ **Mọi mục dưới đây do agent phản biện trả về, TÔI CHƯA TRA TẬN NGUỒN.** Dự án này đã
> mất 18 ngày vì tin chữ *"đã xác minh"* trong ghi chú của chính mình (xem `report/108` mục 9,
> hai khẳng định về UGround). Không mục nào được vào `main.tex` hay `thesis/` trước khi mở
> đúng bài, đúng bảng, đúng số trang.
>
> Ghi ở đây vì **nội dung** của chúng đã đổi cách tôi sửa bài, kể cả khi citation chưa chắc.

## A. Tiền lệ NÂNG ĐỠ bài — nếu đúng thì phải trích

| bài (theo agent) | nói gì | dùng để làm gì |
|---|---|---|
| Belz, Kow, Viethen, Gatt — **GREC Main Subject Reference Generation Challenge 2009**, Workshop on Language Generation and Summarisation, ACL-IJCNLP 2009, tr. 79–87 | chấm văn sinh bằng **công cụ giải đồng tham chiếu**; dùng **HAI công cụ và lấy trung bình** *"to counteract the possibility of results being a function of a specific tool"* | ⇒ **bộ trỏ thứ hai là CHUẨN TỐI THIỂU của họ này từ 2009**, không phải cẩn thận thêm. Đổi hẳn cách trình phép chấm chéo UI-Venus |
| Luo, Price, Cohen, Shakhnarovich — CVPR 2018, tr. 6964–6974 | cột **`Acc-new`** = mô hình truy hồi **thứ hai train riêng**, để chứng minh không overfit vào mô hình dùng lúc train | khuôn mẫu trực tiếp cho phép chấm chéo |
| Cohn-Gordon et al. — NAACL 2018 | **chia đôi dữ liệu**: listener lúc sinh ≠ listener lúc chấm, *"otherwise this S1 production model effectively has access to the system evaluating it"* | ta đang ở tình huống **xấu hơn** (cùng họ nền + đã thấy văn phong). Trích để cho thấy biết chuẩn và biết mình lệch ở đâu |

## B. Tiền lệ ĐÁNH vào bài — nặng nhất trong cả lượt phản biện

| bài (theo agent) | nói gì | vì sao nguy |
|---|---|---|
| Luo & Shakhnarovich — CVPR 2017, tr. 3125–3134 | cùng bộ câu: máy chấm **97,23** vs người chấm **66**; trên RefCOCO+ TestA thước máy **ĐẢO thứ hạng**. Tự cảnh báo: *"expressions would do 'well' on comprehension model, but no longer be intelligible to human"* | thứ tự do máy nghe xếp **có thể đảo** so với người nghe — trong đúng họ REG mà bài tự xếp mình vào |
| Zhao et al. — EACL 2021 | thước dựa-trên-agent tương quan tốt ở **mức câu**, nhưng ở **mức hệ thống** *"lack the desired correlation… unable to reliably rank these out-of-domain systems"* | ⚠️ **toàn bộ Mục VII của bài là khẳng định MỨC HỆ THỐNG.** Điểm phân định có sẵn: các nhánh của ta cùng mô hình nền, cùng dữ liệu, cùng tập kiểm ⇒ **trong phân bố với nhau**, khác 9 hệ ngoài phân bố của họ. **Đã vá vào bài** (mục *Scope of the construct*) |
| Reiter & Belz — *Computational Linguistics* 35(4):529–558, 2009 | *"a meaningless test which is well correlated with another meaningless test remains meaningless"* | giết luận cứ *"BLEU/ROUGE xếp hạng giống executability nên thước không vô dụng"*. **Đã hạ trong bài** |
| Belz & Gatt — ACL-08:HLT, tr. 197–200 | tương quan BLEU với hiệu năng tác vụ người: .39 / .04 / −.08; ROUGE-2: .05 / −.33 / −.36 | cùng chiều với trên |
| Dessì et al. — *Communication breakdown*, EMNLP 2022, tr. 7998–8007 | caption người / máy đọc **12,8%** vs caption máy / máy đọc **50,0%** | phân ly gần hoàn toàn giữa hai loại người đọc |

## C. Lá chắn tốt nhất của bài, trước nay chưa dùng

Nhiều thước loại này **xếp văn máy TRÊN văn người** — dấu hiệu thước hỏng, vì lúc đó bộ sinh
tối ưu về phía giám khảo chứ không về phía người đọc:

| (theo agent) | máy chấm |
|---|---|
| Luo et al. CVPR 2018 | caption người 74,30 · `ATTN+CIDER+DISC(10)` **79,75** |
| Talk the Walk (*preprint* CoRR abs/1807.03367, **không có bản hội nghị**) | người **16,17%** · "emergent language" **69,85%** |
| Mao et al. CVPR 2016 | câu máy 0,799 · câu người 0,607 |

**Thước của ta KHÔNG mắc lỗi này:** trần 75,7 > S1 59,1/59,6 > Base 47,6, bốn KTC rời nhau, và
thứ tự đó **được kỳ vọng trước khi chấm**. ✅ **Đã đưa vào bài** (§VII, đoạn "One outcome would
have ended the study") — nhưng viết ở dạng *phép kiểm ta vượt qua*, **chưa** khẳng định các
thước khác trượt, vì phần đó cần citation đã xác minh.

## D. Việc phải làm trước khi trích bất cứ dòng nào ở trên

1. Mở đúng bài, đúng bảng, đối chiếu từng con số (97,23/66 · 12,8/50,0 · 74,30/79,75…).
2. Xác nhận **venue và năm** — riêng Talk the Walk agent đã tự khai là preprint không có bản
   hội nghị, đúng loại chi tiết dễ trích sai.
3. Với Zhao et al. EACL 2021: đọc kỹ phần *mức hệ thống*, vì đây là đòn nặng nhất và phần
   phân định của ta phụ thuộc vào việc họ đo trên **hệ ngoài phân bố**.
4. ⚠️ Agent tự khai: vòng tra **không thấy** bài nào trong miền GUI chấm hướng dẫn sinh ra bằng
   cách đưa cho bộ trỏ thực thi — nhưng đó là **kết quả âm của MỘT vòng tìm**, **chưa đủ để
   viết "chưa ai làm"** vào bài.

---

# ✅ ĐÃ TRA TẬN NGUỒN — 18/8/2026

Bốn mục dưới đây **không còn là "chưa xác minh"**. Tra bằng WebFetch/WebSearch trên ACL
Anthology và arXiv, đọc abstract và mục đánh giá nguyên văn.

## 1. ⚠️ Chữ "executability" ĐÃ CÓ CHỦ — và có định nghĩa hình thức

**Guo, Deng, Lin, Bai, Guo, Cheng — *"Open Grounded Planning: Challenges and Benchmark
Construction"*, ACL 2024, Long Papers, tr. 4982–5003** (arXiv 2406.02903).

Mục **3.3.2** định nghĩa ba thước: **Executability · Quality · Pass Rate**. Nguyên văn:

> *"Executability is the proportion of executable cases. Executable cases are actions in the
> plan that all exist within the given action library."* — công thức `# executable / # all`

**Nhưng khác hẳn thước của ta:**

| | Open Grounded Planning | luận văn này |
|---|---|---|
| bản chất | **tra bảng ký hiệu** trên văn bản | **hành vi + thị giác** |
| có mô hình trong vòng lặp không | không | có (bộ trỏ đọc câu rồi trỏ) |
| có màn hình không | không | có |
| miền | WikiHow · công cụ · robot | GUI di động |
| tự khai | *"only focuses on the planning generation"* | — |

**⇒ QUYẾT: GIỮ TÊN, không đổi.** Hai cấu trúc khác nhau rõ ràng; một câu phân định là đủ và
cho thấy biết văn liệu. Đổi tên phải sửa nhan đề · abstract · toàn bộ report · luận văn —
đắt mà không rõ tốt hơn.

**Đã vá vào `main.tex`** ngay lần dùng đầu trong Introduction:
> *"The term is used differently in open grounded planning~\cite{ogp}, where executability is
> the share of plans whose every action appears in a given action library — a symbolic lookup
> over text. Ours is behavioural and visual: a model reads the sentence, looks at the screen,
> and points."*

## 2. ✅ Zhao et al. EACL 2021 — vừa hậu thuẫn vừa cảnh báo, đã trích

**Zhao, Anderson, Jain, Wang, Ku, Baldridge, Ie — *"On the Evaluation of Vision-and-Language
Navigation Instructions"*, EACL 2021, tr. 1302–1316.**

Abstract nguyên văn, hai câu quan trọng:

> *"we discover that BLEU, ROUGE, METEOR and CIDEr are **ineffective** for evaluating grounded
> navigation instructions"*

⇒ **hậu thuẫn** việc hạ luận cứ đồng thuận BLEU/ROUGE (đã hạ 18/8).

> *"Our model shows the highest correlation with human wayfinding outcomes when scoring
> **individual instructions**. For ranking instruction generation **systems**, if reference
> instructions are available we recommend using SPICE."*

⇒ Họ đề xuất một thước **không tham chiếu**, nó thắng ở **mức câu**, nhưng để **xếp hạng hệ
thống** thì chính họ khuyên dùng một thước **có** tham chiếu. **Toàn bộ Mục VII của bài ta là
khẳng định mức hệ thống.** Đã trích vào mục *Scope of the construct*.

⚠️ Họ **có** neo người (human wayfinders). Ta không. Đó là khác biệt phải khai, không lấp được
bằng lập luận.

## 3. ✅ GUITrans2Act KHÔNG phải scoop

arXiv **2606.12817**, **preprint 6/2026, KHÔNG có venue**. Đầu vào là **video** demo
(*"demonstration videos"*, *"mobile screen trajectories"*), không phải một ảnh màn hình.
Abstract **không nhắc gì** tới mô hình định vị dùng làm kiểm chứng.

⚠️ Khẳng định của agent — *"cùng vòng lặp nhất quán-với-bộ-trỏ, dùng làm bộ lọc dữ liệu"* —
**KHÔNG kiểm được từ abstract**. Muốn trích điều đó phải đọc thân bài.

Điểm phân định với ta: họ **video → tri thức thao tác cho máy**; ta **một ảnh → câu hướng dẫn
cho người**.

## 4. ⛔ GCoT: agent SAI, ghi chú của ta ĐÚNG

Agent nói *"cập nhật GCoT thành CVPR 2026"*. Tra ra: **2503.12799 vẫn là preprint, không
venue**. Bài ICCV 2025 là **bài KHÁC** — *"Bootstrapping Grounded Chain-of-Thought in
Multimodal LLMs for Data-Efficient Model Adaptation"* (2507.02859).

`CLAUDE.md` đã ghi đúng điều này từ 1/8: *"2503.12799 = **preprint**; bài ICCV 2025 là bài
KHÁC, 2507.02859"*. ⇒ **giữ nguyên cách ghi hiện tại**, đừng sửa theo agent.

⭐ Đây là lần **ghi chú của mình thắng agent**, ngược với bài học 16/8. Rút ra: agent cũng cần
được kiểm như mọi nguồn khác — không tin ngay, cũng không bỏ ngay.

---

## Còn lại chưa tra

Ba mục dưới đây vẫn ở trạng thái **chưa xác minh**, và chúng chỉ là *hậu thuẫn*, không phải
*đe doạ*, nên ưu tiên thấp hơn:

· GREC-MSR 2009 (dùng hai công cụ rồi lấy trung bình — nếu đúng thì bộ trỏ thứ hai là **chuẩn
tối thiểu của họ này từ 2009**, không phải cẩn thận thêm)
· Luo & Shakhnarovich CVPR 2017 (máy chấm 97,23 vs người 66, và đảo thứ hạng)
· Cohn-Gordon et al. NAACL 2018 (chia đôi dữ liệu để listener lúc sinh ≠ listener lúc chấm)
