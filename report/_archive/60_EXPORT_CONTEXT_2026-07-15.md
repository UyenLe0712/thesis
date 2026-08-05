# EXPORT TOÀN BỘ BỐI CẢNH LUẬN VĂN — chụp tại 2026-07-15

> File này viết để **dán nguyên vào một cuộc trò chuyện AI khác** và hỏi tiếp được ngay — không giả định người đọc có quyền mở file nào khác trong máy. Mọi thứ cần biết đều nằm trong đây.
>
> Nếu quay lại làm việc trong đúng thư mục dự án (`D:\Master\Thesis`), file nguồn-sự-thật vẫn là `report/54_PIPELINE_FINAL_DOC_HIEU_TOAN_BO.md` (pipeline) + `CLAUDE.md` (quyết định) + `report/KE_HOACH_2_BAI_BAO.md` (2 bài báo). File export này là ảnh chụp, không phải tài liệu sống — nếu có gì mâu thuẫn với ba file đó, ba file đó thắng vì mới hơn.

---

## MỤC LỤC

1. Đề tài là gì, tóm 1 phút
2. Vì sao đổi hướng (bối cảnh bắt buộc phải biết)
3. Thiết kế hiện tại — Faithful Distillation (đầy đủ)
4. Ba bộ dữ liệu
5. Trạng thái thực thi — đã làm gì, còn gì
6. Kế hoạch 2 bài báo — và vì sao bài thứ hai đang yếu
7. Deep research đang dở — phát hiện sơ bộ (CHƯA verify)
8. Phân tích "nếu không giới hạn thời gian, sẽ đóng góp gì" — câu hỏi mới nhất, quan trọng nhất
9. Việc cần quyết / câu hỏi còn mở
10. Cách làm việc với AI trong dự án này (để chat mới hiểu tôi muốn gì)

---

## 1. Đề tài là gì, tóm 1 phút

**Bài toán:** người dùng đưa một tấm ảnh chụp màn hình ứng dụng + một câu hỏi ngôn ngữ tự nhiên (ví dụ *"Làm sao bật thông báo cho tập mới?"*). Hệ thống phải trả lời bằng các bước cụ thể (*"1. Chạm vào Settings — 2. Chạm vào Notifications — …"*).

**Hai cái khó cốt lõi:**
1. **Không có bộ hướng dẫn chuẩn** do người soạn sẵn để so sánh — tự soạn thì tốn hàng nghìn giờ người, ngoài tầm luận văn. Phải nghĩ ra cách đo không cần đáp án mẫu.
2. **AI hay bịa ra tên nút không tồn tại** trên màn hình đó — lỗi nguy hiểm vì đọc lên vẫn nghe trơn tru, chỉ khi đối chiếu đúng màn mới lòi ra. Người dùng làm theo sẽ bấm nhầm hoặc dò mãi không thấy.

**Trạng thái đề tài:** đây là **luận văn thạc sĩ AI tại Việt Nam, năm 2026**, thời hạn khoảng 3 tháng, học viên làm một mình, không có GPU riêng (dùng Google Colab thuê theo tháng).

---

## 2. Vì sao đổi hướng (bối cảnh bắt buộc phải biết)

Bản đầu tiên của luận văn: gọi gpt-4o-mini đọc ảnh + viết hướng dẫn, dùng thuật toán so embedding kiểm tra có bịa tên nút không. **Giảng viên hướng dẫn bác thẳng**: *"Đây chủ yếu là gọi API và so chuỗi ký tự — chưa thấy đâu là mô hình do chính học viên huấn luyện."* Quy định thạc sĩ của trường bắt buộc luận văn phải có **một mô hình do học viên tự train**, không chỉ ghép công cụ có sẵn qua prompting.

→ Sau lời phê đó, hướng đã đổi sang **"Faithful Distillation"** (mô tả chi tiết ở mục 3): giữ nguyên phần lõi (bài toán, 3 bộ dữ liệu, cách đo không-đáp-án-mẫu), nhưng thêm **một mô hình thật được huấn luyện** làm trung tâm. gpt-4o-mini hạ vai xuống thành "teacher" chỉ dùng để tạo dữ liệu, không còn là sản phẩm cuối.

**Đã qua 7 vòng debate/kiểm chứng đối kháng** (dựng lập luận rồi cố tình tìm cách bẻ gãy bằng cách tra cứu và để nhiều góc nhìn công kích) + 1 vòng audit độc lập rà lại 64 quyết định. Không vòng nào phát hiện lỗi buộc phải làm lại từ đầu — chỉ có chỗ phải nói khiêm tốn hơn, đo thêm cho chắc, hoặc thống nhất định nghĩa.

**Ba hướng khác đã bị cân nhắc và loại** (đừng đề xuất lại nếu không có lý do mới):
- **Train một mô hình "bấm đúng nút" (grounding) bằng RLVR**, lấy chính thước đo không-đáp-án-mẫu làm phần thưởng. Bị loại: (a) vừa huấn luyện vừa chấm chính mình dễ rơi vào vòng lặp tự-khen; (b) "bấm nút" không phải bước thầy chê thiếu — bước thầy chê là *viết ra hướng dẫn*; (c) trùng nhiều với các nghiên cứu GUI-agent-bấm-máy đã có (UI-R1, SE-GUI, GUI-Actor).
- **Một mô hình nhỏ chuyên "học phát hiện bịa"** từ dữ liệu tự bơm lỗi. Bị loại: mô hình chỉ học lại đúng cách mình bơm lỗi giả, không chắc bắt được lỗi bịa thật.
- **Học tăng cường lấy điểm-trung-thực làm phần thưởng để train thẳng phần viết-hướng-dẫn.** Bị loại: model học cách "lách luật" — không bao giờ nêu tên nút cụ thể nữa, mô tả chung chung mọi lúc để tối đa điểm trung thực giả tạo. Điểm cao nhưng hướng dẫn vô dụng.

---

## 3. Thiết kế hiện tại — Faithful Distillation (đầy đủ)

### 3.1. Ý tưởng cốt lõi: một "Teacher" hay bịa, một "Student" được dạy lại cho cẩn thận

- **Teacher** = gpt-4o-mini, gọi qua API. Chỉ được nhìn ảnh + câu hỏi, **cố ý không cho xem danh sách nút thật** của màn hình — vì cần đúng những chỗ nó tự nhiên hay bịa. Kết quả: khoảng 1/4 số bước có bịa (quan sát sơ bộ, chưa phải số đo chính thức).
- **Student** = Qwen2.5-VL-3B-Instruct, mô hình mở, **học viên tự fine-tune bằng SFT-LoRA**. Đây là sản phẩm chính của luận văn — thứ trả lời trực tiếp lời phê "chưa thấy model đâu".
- Student **không học nguyên xi lời Teacher**. Nó chỉ học từ phần lời Teacher **đã được lọc sạch bịa**.
- **Câu hỏi trung tâm của cả luận văn:** thói quen thành thật đó có thật sự **ngấm vào trọng số** của Student, hay chỉ là vẻ ngoài phụ thuộc vào việc có ai kiểm tra hộ hay không?

### 3.2. Pipeline 5 bước (chạy một lần, offline, chỉ để tạo dữ liệu huấn luyện)

1. **Ảnh + câu hỏi** — lấy từ kho ảnh màn hình ứng dụng thật (MobileViews).
2. **Teacher viết nháp** — chỉ thấy ảnh, không thấy danh sách nút. (Bước tốn tiền duy nhất trong nhóm này, ước tính $1–2 cho vài nghìn lượt gọi.)
3. **Đối chiếu nút thật** — thuật toán so nghĩa (không phải AI): lấy tên nút Teacher nhắc tới, so cosine-similarity bằng embedding `nomic-embed-text` với từng nhãn trong View Hierarchy (VH) của màn hình đó. Ngưỡng **0.55** (đã freeze, chốt từ tự kiểm: từ đồng nghĩa rơi vào 0.6–0.69, từ khác nghĩa quanh 0.39). Dưới ngưỡng → kết luận là bịa. Thuật toán này **đóng băng hoàn toàn**, không nhận gradient, không được huấn luyện — vai trò của nó đúng bằng một hàm đo khoảng cách.
4. **Viết lại chỗ bịa** — bằng **khuôn mẫu cố định** ("Tìm và chạm vào tuỳ chọn trên màn hình phù hợp với việc bạn cần làm ở bước này"), **cố ý không gọi AI** để viết lại. Lý do: nếu để AI viết lại cho hay, chính bước lọc lại có thể mở ra một chỗ bịa mới.
5. **Dạy Student** — huấn luyện SFT-LoRA trên đúng phần dữ liệu đã lọc sạch.

**Điểm bịt lỗ hổng quan trọng:** câu hỏi dùng để huấn luyện Student **không** chứa dặn dò "đừng bịa nút không có thật", trong khi prompt cho Teacher lúc sinh dữ liệu **có** đúng câu đó. Nếu Student cũng được nhắc, sẽ không ai chứng minh được thói quen thành thật đến từ huấn luyện chứ không phải từ lời nhắc thêm.

**View Hierarchy (VH) là gì:** mỗi ảnh chụp màn hình Android trong bộ dữ liệu đều đi kèm một file do hệ điều hành xuất ra, liệt kê chính xác mọi phần tử đang hiển thị (loại, tên hiển thị, toạ độ). VH **chỉ có mặt lúc chuẩn bị dữ liệu và lúc chấm điểm** — không bao giờ đưa cho Student thấy, kể cả lúc học lẫn lúc chạy thật. Đó chính là điều làm cho câu hỏi trung tâm có ý nghĩa.

### 3.3. Đâu là mô hình do học viên thật sự huấn luyện

Tiêu chí phân định (dùng khi thầy hỏi "mô hình của em đâu"): một thành phần chỉ tính là "mô hình do học viên train" khi trả lời **có** cho cả ba câu — (1) nó có trọng số không? (2) trọng số đó có đổi vì dữ liệu của luận văn này không? (3) cái đổi đó có đo được không?

| Thành phần | Vai trò | Có trọng số? | Trọng số đổi vì luận văn? |
|---|---|---|---|
| gpt-4o-mini (Teacher) | Viết nháp để tạo dữ liệu, không có mặt lúc chạy thật | Có, trên máy chủ OpenAI | **KHÔNG** |
| nomic-embed-text (matcher) | Đối chiếu tên nút với VH | Có, nhưng đóng băng | **KHÔNG** |
| Khuôn viết lại | Thay chỗ bịa bằng mô tả | Không (khuôn chữ cố định) | **KHÔNG** |
| **Qwen2.5-VL-3B (Student)** | **Bộ sinh hướng dẫn, chạy trên máy người dùng** | **Có — LoRA adapter** | **CÓ** |

Chỉ đúng một ô "CÓ". Phép thử để thấy rõ ranh giới: xoá ba thành phần đầu sau khi huấn luyện xong, hệ vẫn chạy y nguyên vì sản phẩm giao đi chỉ gồm Qwen đã fine-tune. Xoá Qwen thì không còn gì.

**Cấu hình huấn luyện đã chốt:** framework LLaMA-Factory; QLoRA 4-bit làm mặc định (Colab không đảm bảo GPU cố định); LoRA rank 8, alpha 16, chỉ gắn vào nhánh ngôn ngữ (q/k/v/o + gate/up/down projection), **đóng băng hoàn toàn vision encoder** (vì hành vi cần dạy là "nói gì khi không chắc", không phải "nhìn thấy gì"); ~1.500–3.000 mẫu; lr 1e-4, 3 epoch (ước tính, cần smoke-test xác nhận). Tiền lệ duy nhất xác nhận trực tiếp cấu hình này: **ZonUI-3B / Qwen-GUI-3B (arXiv 2506.23491, WACV 2026)** — LoRA đúng Qwen2.5-VL-3B trên một GPU 24GB, khai thẳng đây là **1 nguồn duy nhất, không phải nhiều nguồn hội tụ**.

**Bắt buộc train HAI bản:**
- **Student** — học từ dữ liệu đã lọc.
- **Student-RAW** — học từ dữ liệu thô, y hệt cấu hình, khác đúng một biến là dữ liệu. Đây là nhánh **duy nhất** tách được "giỏi lên nhờ lọc" khỏi "giỏi lên nhờ fine-tune nói chung".

### 3.4. Thiết kế hai tầng thí nghiệm

| Tầng | So sánh | Điều kiện lúc suy luận | Ý nghĩa |
|---|---|---|---|
| **Tier 1 — lưới an toàn** (gần chắc dương) | Student vs Student-RAW | Chấm trên output THÔ (trước lớp viết-lại), ở cả hai bên | Existence proof: có mô hình thật được train + việc lọc tạo hiệu ứng đo được → đã thoả yêu cầu của thầy, độc lập với Tier 2 |
| **Tier 2 — trụ chính** (có thể null) | Student vs Teacher-BASE (gpt-4o-mini chạy thô) | **Tắt hẳn VH**, held-out theo app (12 app chưa từng thấy) | Câu hỏi mới: thói quen thành thật có nội-tại-hoá vào Student không |

**Vì sao Tier 1 chấm trên output thô chứ không phải sau lớp viết-lại:** nếu chấm sau viết-lại thì cả Student lẫn Student-RAW đều "sạch" như nhau (vì lớp viết-lại chữa bịa cho mọi bản), Δ ≈ 0 → null giả tạo, thí nghiệm tự huỷ. Lợi ích của lớp viết-lại được báo riêng qua %fallback, không trộn vào con số faithfulness.

**Bất đối xứng cố ý ở Tier 2 (khai thẳng, không giấu):** `f_Teacher` chấm trên output sinh bằng prompt gốc của Teacher — **có** câu "đừng bịa nút không có thật"; Student bị hỏi bằng prompt **không** có câu đó. Student phải thắng dù bị nhắc ít hơn — đây là sai lệch theo hướng **an toàn** (bất lợi cho phía mình), nên nếu Student vẫn thắng thì kết luận càng mạnh.

**Ngưỡng đậu/rớt đã pre-register (khoá trước khi nhìn số, commit git `2c84ce8` ngày 12/7):**
- Tier 1: CI 95% của Δ = mean(f_Student − f_Student-RAW) nằm **hoàn toàn trên 0**. Không cần điều kiện "đủ lớn". Nếu Tier 1 cũng null → DỪNG, rà lại toàn bộ pipeline lọc trước khi diễn giải Tier 2.
- Tier 2: **(A)** CI 95% của Δ hoàn toàn trên 0 **VÀ (B)** Δ_test ≥ 0.5 × Δ_train (Δ_train đo cùng công thức, cùng điều kiện tắt-VH, nhưng trên 18 app train thay vì 12 app test — đo mức cải thiện tốt nhất có thể trông đợi, rồi hỏi: sang app lạ giữ được bao nhiêu phần). **Hệ số 0.5 là tự đề xuất, khai rõ, không lấy từ literature.**
- **Ba kết cục:** PASS đầy đủ (A+B) / PASS một phần (A đúng, B sai) / NULL (CI chứa 0). Cả ba đều có diễn giải viết sẵn trước khi chạy — NULL không có nghĩa là "luận văn thất bại", vì Tier 1 đứng độc lập.

### 3.5. Bộ thước đo đầy đủ

**Bài học nền tảng (khai thẳng vì đã từng sai thật):** bản đầu của luận văn mắc lỗi "vừa đá bóng vừa thổi còi" — bộ lọc vừa sửa dữ liệu vừa chấm điểm chính dữ liệu đó, khiến độ trung thực vọt lên gần 100% một cách vô nghĩa (tautology). Đã vá bằng cách tách triệt để: **thứ dùng để lọc lúc chuẩn bị dữ liệu (nomic, ngưỡng 0.55) tuyệt đối không được dùng lại để chấm điểm lúc đánh giá.**

- **Thước chính — faithfulness:** `f = 1 − (số lần nhắc nút BỊA / tổng số lần nhắc nút)`, theo ALOHa (Petryk et al., NAACL 2024 Short). Gộp trung bình theo từng app trước (macro-per-app), vì các màn cùng app không độc lập.
- **Chấm bằng 3 cơ chế khác họ** (không dùng lại nomic): (1) embedding **bge-m3**, ngưỡng τB hiệu chuẩn riêng bằng 80–120 cặp gán tay (precision ≥ 0.95); (2) LLM-judge **llama3.2** local, khác họ với Teacher (Teacher là GPT-family → judge không được dùng GPT-family, tránh self-preference bias — Panickssery et al., NeurIPS 2024); (3) token-overlap, phi-neural. Một bước bị coi là bịa khi **≥2/3 đồng ý không khớp**. Khai thẳng giới hạn: ba cơ chế chỉ **giảm** chứ không **loại** tương quan sai số, vì bge-m3 và LLM-judge đều là mạng nơ-ron.
- **Ba thước đi kèm bắt buộc** (chống ăn gian — nói chung chung mọi lúc thì tỉ lệ bịa = 0 nhưng vô dụng): **%fallback** (tỉ lệ bước rơi vào mô tả chung chung); **tỉ lệ lỗi-ngầm** (bước bịa bị thay bằng một nút CÓ THẬT nhưng sai chức năng — nguy hiểm hơn fallback vì không lộ ra); **tỉ lệ màn 0-nhắc-nút**.
- **Grounding (điểm bấm đúng vị trí) cố ý loại khỏi headline một-màn**: nếu lấy tâm của khung nút đã khớp làm toạ độ thì luôn đúng 100% — tautology. Chỉ giữ làm đối chứng trên ScreenSpot-v2.
- **Kiểm định độ tin của chính thước đo = bơm lỗi tự động độc lập với matcher** (Sai et al., EMNLP 2021): 4 loại lỗi (đổi tên nút thật → tên không có; đổi sang nút thật nhưng sai màn; chèn bước nhắc nút bịa; hoán tên nút giữa hai màn). Ngưỡng: detection ≥ 0.80, false-positive ≤ 0.10, đơn điệu (Spearman < 0, p < 0.05). Phạm vi khai thẳng: đây là điều kiện CẦN (độ nhạy), KHÔNG phải bằng chứng hội tụ với đánh giá của người — human-correlation là việc tương lai, không phải cổng đậu/rớt (Clark et al., ACL-IJCNLP 2021).
- **Thống kê:** cỡ mẫu chỉ 12 app test → dùng **exact sign-flip test** (liệt kê hết toàn bộ 2¹² = 4.096 tổ hợp đổi dấu, không xấp xỉ) thay vì thống kê thông thường giả định mẫu lớn. Trụ: Canay-Santos-Shaikh (REStat 2021), Cameron & Miller (JHR 2015). MDE (mức chênh lệch tối thiểu phát hiện được) tính bằng số liệu pilot thật trước khi khoá ngưỡng — **ô này hiện còn TRỐNG**, là ô duy nhất được phép điền sau khi đã commit pre-registration.

### 3.6. Bộ thí nghiệm — sáu thí nghiệm, mỗi cái chặn một câu vặn

| # | So gì với gì | Ngưỡng đậu | Chặn được câu vặn |
|---|---|---|---|
| 1 | Student vs Student-RAW | CI 95% của Δ trên 0 | "Giỏi lên nhờ fine-tune nói chung, đâu phải nhờ lọc?" |
| 2 | Student vs Teacher-BASE, tắt VH, app chưa từng thấy | CI 95% trên 0 VÀ Δ_test ≥ 0.5×Δ_train | "Thói quen đó có ngấm vào trọng số không?" — trụ chính, có thể null |
| 3 | %fallback · lỗi ngầm · màn 0-nhắc-nút | báo kèm bắt buộc | "Cứ nói chung chung là bịa=0, ăn gian thước!" |
| 4 | Độ hữu ích: Student vs Student-RAW | trong family Holm | "Sạch nhưng mơ hồ, vô dụng thì sao?" |
| 5 | Bộ chấm bge-m3 vs người, 80–120 cặp | precision ≥ 0.95 | "Lấy gì bảo đảm bộ chấm đúng?" |
| 6 | Bơm lỗi đã biết vs thước đo | bắt ≥0.80, báo nhầm ≤0.10 | "Phép đo có thật sự nhạy không?" |

Thí nghiệm 1 và 2 mang kết luận. 3–6 là lá chắn — không tạo kết luận mới, chỉ để mỗi câu vặn đều có sẵn con số trả lời.

### 3.7. Nhánh nhiều màn hình — đã thiết kế xong, NGOÀI PHẠM VI mùa này

Bài toán: người dùng chụp cả một quy trình gồm N ảnh nhưng thứ tự bị xáo trộn. Hệ phải tự khôi phục đúng thứ tự trước, rồi mới chạy đúng pipeline một-màn cho từng ảnh.

**Điểm thiết kế quan trọng nhất:** đây **không phải một hệ thứ hai**. Nó là đúng hệ một-màn, cộng thêm một khối cắm ở đầu gọi là **Stage-0**. Khi N=1, Stage-0 rỗng và mọi thứ trở về đúng hệ một-màn. Công sức bỏ vào nhánh một-màn không mất đi khi mở rộng.

**Stage-0 — ba nhịp:**
1. **Hỏi từng cặp** — "màn nào đến trước?" (N=4 → 6 câu, N=5 → 10 câu). Cố ý không hỏi kiểu "sắp cả N màn giúp tôi" vì đó là hộp đen, không để lại dấu vết kiểm tra.
2. **Tổng hợp bằng Copeland** — như một giải đấu vòng tròn, điểm = số màn khác được xếp trước, sắp theo điểm.
3. **Phá vòng mâu thuẫn** — nếu model tự mâu thuẫn (A trước B, B trước C, nhưng C trước A), phải cắt một dây. **Quyết định quan trọng:** KHÔNG hỏi model tự khai "mày chắc bao nhiêu %" rồi cắt dây yếu nhất — vì model ngôn ngữ hiệu chỉnh độ tự tin rất kém, tin lời tự khai là rơi vào bẫy tự-chấm-mình. Thay vào đó đo bằng ba tín hiệu khách quan: khoảng cách thắng, tính ổn định khi hỏi lại nhiều lần, ưu tiên cắt ít dây nhất.

Cả sáu thành phần đều có trụ bình duyệt xác minh venue: pairwise (Qin, Findings NAACL 2024), Copeland (Dwork, WWW 2001), min feedback arc set (Ailon, J.ACM 2008), tiền lệ tác vụ (Sort Story, EMNLP 2016), thước τ (Fagin, SIAM J. Discrete Math 2006), tiền lệ dùng τ làm headline (Lapata, CL 2006). **Khai thẳng: không phát minh cái nào, đóng góp là ráp chúng thành một hệ sắp-màn-theo-mục-tiêu phục vụ sinh hướng dẫn.**

**Đo bằng:** thước τ thứ-tự-bộ-phận (chỉ phạt cặp bắt buộc phải đúng thứ tự, suy từ quỹ đạo vàng bằng quy tắc nhân quả) + Step-SR (tỉ lệ bước đúng, teacher-forced).

**Bốn cổng phải qua trước khi tin bất kỳ số nào:** K-pair (độ chính xác so-cặp thô của model vs gold phải > 0.5, nếu ≈0.5 thì toàn bộ nhánh vô hiệu về nguyên tắc — **cổng này CHƯA CHẠY**), KN (histogram độ dài quy trình — ✅ GO), KZ' (prior-art — ✅ GO), KB (chống rò rỉ chỉ số bước: che đồng hồ/pin/huy hiệu, vì đã tìm thấy đồng hồ hiện giờ thật trong dữ liệu — model có thể đọc lỏm thứ tự mà không cần hiểu gì về giao diện).

**Vì sao cắt khỏi mùa này:** ba lý do — (1) còn cổng K-pair chưa chạy, rớt thì cả nhánh vô hiệu; (2) lịch 3 tháng đã kín cho nhánh một-màn; (3) nhánh một-màn đã tự khép kín thành một câu chuyện hoàn chỉnh. Để dành cho bài mở rộng sau. Nếu K-pair rớt, đây không phải "bỏ" mà là một **phát hiện âm tính hợp lệ**.

**⚠️ Có một tuỳ chọn KHÔNG làm mùa này:** train một bộ sắp-thứ-tự học-được riêng (dùng nhãn cặp suy từ quỹ đạo vàng của AndroidControl, miễn phí, +~5–6 ngày, +~$10). Nếu làm, đó mới thực sự là "train model thứ hai". Hiện tại Stage-0 chỉ là prompting + thuật toán tổng hợp, không có gì được huấn luyện ở nhánh nhiều-màn.

---

## 4. Ba bộ dữ liệu

| Bộ | Nơi công bố | Vai trò | Ghi chú quan trọng |
|---|---|---|---|
| **MobileViews** | ⚠️ **Preprint arXiv 2409.14337, CHƯA bình duyệt** — đóng khung là hiện vật kỹ thuật, không phải trụ khoa học | Nguồn ảnh + VH — **bộ DUY NHẤT dùng để train** | Thu thập tự động bằng bot. Giấy phép MIT. Có mâu thuẫn quy mô công bố (paper nói 1,2 triệu, bản tải công khai chỉ ~600K) — phải khai khi trích |
| **AndroidControl** | ✅ NeurIPS 2024 Datasets & Benchmarks (đã bình duyệt), Li et al., Google DeepMind | Có quỹ đạo vàng do người thật thao tác → dùng làm đáp án cho nhánh nhiều-màn (chấm, không train) + hiệu chuẩn bộ đối chiếu | CC0. **KHÔNG in "2.855" làm cỡ test** (đó là tổng 4 sub-split chồng nhau) — số duy nhất sau khử trùng ≈1.540, chưa tự đếm lại chính xác |
| **ScreenSpot-v2** | ✅ Phát hành kèm OS-Atlas (ICLR 2025); gốc ScreenSpot từ SeeClick (ACL 2024) | Đối chứng grounding, đã hạ vai — không dùng headline | 501 item mobile trong bản làm việc |

**Split đã khoá (commit git `3776212`, ngày 12/7, seed=20260710):** 30 app MobileViews đã qua lọc chất lượng → **18 app để dạy Student / 12 app chỉ để chấm** (127 màn tổng: 76 màn train + 51 màn test). Chia theo APP chứ không theo màn (màn cùng app quá giống nhau, không phải bằng chứng độc lập).

**Mở rộng pool train — ĐÃ CHẠY 12/7/2026:** fetch thêm 2 shard chưa dùng từ kho MobileViews công khai → dedup (theo tên app + perceptual-hash của ảnh) → kết quả thật **498 màn / 220 app mới**. Kiểm rò rỉ chéo với 12 app test: **0 ca** (đã tự kiểm lại bằng code, không chỉ tin lời báo cáo). Cộng 76 màn train cũ → tổng ~574 màn → kỳ vọng ~1.700–2.870 mẫu huấn luyện (574 màn × 3–5 câu hỏi/màn) — **nhưng bước sinh câu hỏi và gọi Teacher CHƯA CHẠY**, đây là con số kỳ vọng, không phải dữ liệu đã có.

**Không có dataset GUI tiếng Việt nào tồn tại** — đã quét MobileViews local 231 file, chỉ tìm được 2 màn có chữ Việt lẻ (tên riêng), không phải giao diện app Việt thật.

---

## 5. Trạng thái thực thi — đã làm gì, còn gì (tính đến 15/7/2026)

**✅ Đã xong:**
- 7 vòng debate + 1 vòng audit độ vững (không phát hiện lỗi thiết kế phải làm lại).
- Khoá split 18/12 app — commit git `3776212`.
- Pre-registration ngưỡng Tier1/Tier2 — viết ở `report/56`, commit git `2c84ce8`, đã vá 4 lỗ từ một vòng rà soát riêng.
- Mở rộng pool train: 498 màn/220 app mới, kiểm rò rỉ 0 ca.
- Bộ slide trình bày pipeline cho giảng viên hướng dẫn (đã build, đã rà nhiều lượt để bỏ giọng "AI-gen", bỏ giải thích thừa, chuyển phần dặn dò xuống note thuyết trình).

**⏳ Thứ tự việc tiếp theo — KHÔNG được đảo:**
1. Pilot baseline (chạy Teacher trên vài chục màn) → tính MDE thật → điền vào `report/56` → **commit lần hai**. (Đây là bước tốn tiền API đầu tiên, cần hỏi ý kiến trước khi chạy.)
2. Nếu MDE > 15–20 điểm phần trăm → đổi chia 18/12 thành 15/15 **trước khi** khoá — không được đổi sau khi đã nhìn kết quả.
3. Sinh câu hỏi tình huống cho mỗi màn (mô hình nhỏ chạy local, miễn phí).
4. Gọi Teacher sinh bản nháp đầy đủ (~$1–2, cần duyệt trước).
5. Chạy matcher + viết-lại → đóng gói tập SFT.
6. Smoke-test train 20 mẫu trên Colab → train đầy đủ 2 bản (Student + Student-RAW) → eval Tier 1 + Tier 2.
7. Smoke-test sinh tiếng Việt (~5 màn) — quyết hướng cho bài VCL (xem mục 6).

**Nguyên tắc chi tiền:** chạy một lần cho đúng; mọi bước tốn API/GPU phải hỏi trước; ưu tiên local/free.

---

## 6. Kế hoạch 2 bài báo — và vì sao bài thứ hai đang yếu

**Mục tiêu của học viên:** nộp **cả hai** hội nghị mùa này (nhiều công bố → dễ ra tốt nghiệp hơn).

| | **FAIR** | **VCL** |
|---|---|---|
| Deadline | 15/8/2026 | ~30/8/2026 (chưa verify CFP thật) |
| Ngôn ngữ | Tiếng Anh (venue chỉ nhận Anh) | Tiếng Việt |
| Độ khó / danh giá | Khó hơn, danh giá hơn | Dễ hơn |
| Venue | Hội nghị Quốc gia CNTT (rộng, có track VLM) | Hội thảo Ngôn ngữ học Tính toán (thuần NLP) |
| Nội dung dự kiến | **Bài mô hình** (flagship): Faithful Distillation, Tier1/Tier2 trên MobileViews tiếng Anh | Cùng model đó, **đổi prompt sang tiếng Việt**, đo lại độ trung thực + chất lượng tiếng Việt (khảo sát chuyển-giao Anh→Việt) |
| Vai trò | Bắt buộc phải kịp (stretch) | Sàn chắc, fallback nếu FAIR trễ |

**Fallback cứng:** nếu FAIR không kịp 15/8 → bỏ FAIR, giữ VCL, model đi venue quốc tế sau. Không để canh bạc FAIR làm hỏng VCL.

### Phê bình của tôi về bài VCL (quan điểm cá nhân, chưa qua debate với giảng viên)

Tôi nghĩ bài VCL đang **yếu về cấu trúc**, không phải yếu về câu chữ:

1. **Không có gì được huấn luyện thêm.** Bài FAIR train model. Bài VCL lấy đúng model đó, đổi prompt sang tiếng Việt, đo lại. Đó là *prompting*, đúng thứ giảng viên đã bác một lần ở vòng đầu tiên.
2. **"Chất ngôn ngữ" mỏng hơn vẻ ngoài.** Output sẽ dạng `Chạm vào "Settings"` — phần tiếng Việt chỉ là chữ nối, phần chịu lực (tên nút) vẫn tiếng Anh vì VH gán nhãn tiếng Anh. Một hội đồng ngôn ngữ học sẽ hỏi: đóng góp ngôn ngữ nằm ở đâu?
3. **Câu hỏi nghiên cứu ít bất ngờ.** Qwen2.5-VL vốn đã đa ngữ; "model đa ngữ có xuất được tiếng Việt không" gần như biết trước là có.
4. **Rủi ro salami là thật, và kế hoạch tự thừa nhận điều đó** (dùng chung dữ liệu, chung model, chung thước đo, nộp cách nhau 2 tuần).
5. Nó tốn ~2 tuần lẽ ra có thể dùng để làm FAIR mạnh hơn.

**Điều tôi nghĩ đáng cân nhắc nhất:** trục chia **cũ** (một-màn / nhiều-màn) sạch hơn hẳn — khác dữ liệu (MobileViews vs AndroidControl), khác câu hỏi (sinh hướng dẫn vs sắp thứ tự), khác thước đo (trung thực vs τ/Step-SR), gần như không có chỗ để bị soi là chẻ nhỏ một nghiên cứu. Trục đó bị gạt **chỉ vì không kịp thời gian trong 3 tháng**. Nếu không giới hạn thời gian (xem mục 8), bài thứ hai nên là **nhiều màn**, không phải bản tiếng Việt của bài một.

**Việc cần verify, chưa có nguồn xác nhận:** deadline CFP VCL2026 thật; chính sách dual-submission/self-plagiarism của cả hai venue; tỉ lệ chấp nhận, index Scopus/DBLP, độ dài bài quy định.

---

## 7. Deep research đang dở — phát hiện sơ bộ (CHƯA verify đối kháng)

Đã chạy một deep-research để trả lời 6 câu hỏi về tính mới và điểm yếu của thiết kế, nhưng **workflow bị dừng giữa chừng** — xong bước tìm kiếm + trích claim từ ~26 nguồn, **chưa chạy bước verify đối kháng (3 phiếu phản biện mỗi claim) và chưa tổng hợp**. Toàn bộ nguyên liệu thô đã lưu vào file `report/59_deepresearch_dang_do.md` để chạy tiếp.

**⚠️ Mọi phát hiện dưới đây CHƯA qua kiểm chứng đối kháng — không được trích thẳng vào luận văn/bài báo.** Nhưng đáng nói ngay vì liên quan trực tiếp tới các đề xuất ở mục 8:

**Phát hiện 1 — ý tưởng "DPO trên cặp thô/lọc" nhiều khả năng KHÔNG mới.** Một nguồn (HA-DPO, Zhao et al.) trích rõ: *"the pair-from-filtering idea is NOT novel in itself"*. HA-DPO đã dựng đúng cặp (bản bịa, bản đã sửa) trên cùng một ảnh, bản sửa cũng là *rewrite* của bản bịa — rất gần ý tưởng "dùng cặp thô/lọc sinh miễn phí từ bước lọc để train bằng DPO thay vì SFT". Delta còn lại có thể chỉ là "verifier là nguồn ngoài có cấu trúc (VH) thay vì để GPT-4 tự chấm" — mà đó **đúng bằng delta luận văn đã claim sẵn cho phần SFT**, tức không thêm được gì mới nếu chỉ dừng ở đó.

**Phát hiện 2 — nhưng HA-DPO xác nhận một điểm yếu thật của thiết kế hiện tại.** Nguồn ghi: HA-DPO chỉ đích danh nguy cơ lệch *phong cách* giữa output thô và output đã sửa khiến DPO học **phong cách thay vì học tính trung thực**. Đây chính xác là mối lo "template degeneracy" — nếu mọi bước không chắc đều bị thay bằng đúng MỘT câu cố định, Student rất có thể chỉ học thuộc câu đó chứ không học được thói quen hiệu chỉnh độ không chắc thật sự. HA-DPO có sẵn cách vá: viết lại **cả hai phía** về cùng một phong cách để chúng chỉ khác nhau ở nội dung bịa — cách này dùng được ngay dù đi hướng SFT hay DPO.

**Phát hiện 3 — một trụ peer-reviewed nghiêng về ủng hộ thiết kế hiện tại.** *"Does Object Grounding Really Reduce Hallucination of Large Vision-Language Models?"* (EMNLP 2024 Main) kết luận: grounding objectives có **"little to no effect on object hallucination"** trong sinh caption tự do — tức nghiêng về phía chiến lược "sinh tự do rồi lọc sau" (đang dùng), chống lại phương án "ép model bám nguồn có cấu trúc ngay lúc sinh" (kiểu VGA). Nếu claim này sống qua verify, đây là một trụ tốt để bảo vệ lựa chọn thiết kế hiện tại.

**Việc còn lại khi chạy tiếp deep-research:** (a) verify đối kháng toàn bộ ~155 claim đã trích; (b) chốt xem risk–coverage / selective prediction đã có ai áp cho hallucination LLM/VLM chưa (câu hỏi 3 trong bộ 6 câu, quyết định đề xuất "đổi khung sang selective prediction" ở mục 8 có đứng được không); (c) tổng hợp theo đúng 6 câu hỏi gốc.

---

## 8. Phân tích "nếu không giới hạn thời gian, sẽ đóng góp gì" — câu hỏi mới nhất, quan trọng nhất

Đây là câu hỏi trực tiếp nhất mà học viên vừa đặt ra, tách khỏi mọi ràng buộc 3-tháng-1-GPU. Dưới đây là phân tích, xếp theo mức độ tôi tin, **có phân biệt rõ đâu là sự thật đã kiểm và đâu là phán đoán cá nhân**.

### #1 — Đổi khung bài toán thành "học chính sách từ chối có hiệu chỉnh" (tôi tin nhất)

Hiện luận văn tự mô tả là "giảm bịa". Nhưng nhìn kỹ, thứ đang xây thực chất là một **chính sách từ chối (abstention policy)**: model được quyền không nêu tên nút cụ thể, và câu hỏi thật là **nó từ chối có đúng chỗ không**. Đây chính là bài toán **selective prediction**, một nhánh có lý thuyết và thước đo sẵn (đường cong risk–coverage, AURC).

Đổi khung này giải quyết một lúc ba việc:
- **Vá điểm yếu chí mạng đã nói ở mục 7:** hiện mọi chỗ không chắc đều thành đúng MỘT câu cố định → Student có thể chỉ học thuộc template. Khung abstention buộc phải có **mức độ** không chắc (hedge nhẹ / mô tả vị trí / từ chối hẳn), không phải một câu duy nhất.
- **Thay hai con số rời** ("tỉ lệ bịa" + "%fallback", phải giải thích lòng vòng khi nào cái này thấp mà cái kia cao thì không tính) bằng **một đường cong** so được công bằng ở mọi mức coverage.
- **Làm Tier 2 sắc hơn:** câu hỏi không còn là "faithfulness có ngấm không" chung chung, mà là "chính sách từ chối học được có sống sót khi rút verifier lúc suy luận không" — cụ thể hơn, đo được hơn.

Đây là đề xuất tôi tin nhất vì **không cần thêm dữ liệu hay compute**, chỉ cần nghĩ đúng khung toán học cho cùng một thí nghiệm đã thiết kế.

**⚠️ Cần deep-research xác nhận:** risk–coverage đã có ai dùng cho hallucination của LLM/VLM chưa — đây là câu 3 trong bộ 6 câu ở mục 7, chưa verify xong.

### #2 — DPO trên cặp thô/lọc (khả năng KHÔNG mới, cần verify trước khi theo)

Bước lọc tự sinh ra cặp (bản có bịa, bản đã sạch) miễn phí — thứ người ta thường phải thuê người gán nhãn mới có. SFT hiện tại là bắt chước bản sạch; DPO trên đúng cặp đó dạy thẳng *sự tương phản*.

**Nhưng phát hiện sơ bộ ở mục 7 cho thấy HA-DPO đã làm gần giống việc này.** Nếu verify xác nhận đúng, ý này **không tính là đóng góp mới** — chỉ còn giá trị như một kỹ thuật bổ trợ (thêm sau SFT), không phải một claim tính mới độc lập.

### #3 — Đo và vá độ tin cậy của View Hierarchy làm ground truth (nền móng đang lung lay)

Luận văn tự trích Chen et al. (ICSE 2020): **>77% app thiếu nhãn trợ năng**. Nhưng lại dùng chính VH làm "sự thật" để lọc dữ liệu. Hệ quả: nút thật, hiển thị đàng hoàng, mà VH không có nhãn → matcher kết luận "bịa" → **một bước vốn đúng bị viết lại thành mô tả chung chung**. Dữ liệu huấn luyện nhiễm lỗi ngay từ nguồn, và Student bị dạy né tránh ở đúng những chỗ lẽ ra nên nói cụ thể.

Có thời gian, tôi sẽ hợp nhất **VH + OCR đọc chữ trên ảnh + bộ dò icon** để tăng recall của "danh sách phần tử thật", đo trên một tập người kiểm tay xem recall thật là bao nhiêu. Đây vừa vá lỗ hổng của chính luận văn, vừa là một đóng góp dùng được cho bất kỳ ai lấy accessibility tree làm chuẩn cho GUI.

### #4 — So sánh trực tiếp "lọc sau" với "ràng buộc trước lúc sinh"

Thiết kế hiện tại chọn "để Teacher sinh tự do rồi lọc", biện minh là giữ được đúng chỗ model lớn tự nhiên hay sai. Nghe hợp lý nhưng **chưa ai trong đề tài này kiểm bằng thực nghiệm**. Đối thủ hiển nhiên: đưa VH cho Teacher ngay từ đầu (kiểu VGA) để nó bám nguồn ngay lúc viết, khỏi cần lọc sau.

**Có một trụ peer-reviewed sơ bộ ủng hộ chọn lựa hiện tại** (phát hiện 3, mục 7 — EMNLP 2024 Main, grounding có tác dụng rất ít lên hallucination), nhưng đó là claim **chưa qua verify**. Nếu không giới hạn thời gian, tôi sẽ chạy cả hai nhánh (lọc-sau vs ràng-buộc-trước) và so trực tiếp trên đúng tập dữ liệu này — câu hỏi có giá trị thật, và giờ nằm trong tầm tay vì đã có cả hai thành phần cần thiết.

### #5 — Nhiều màn hình như một bài báo độc lập

Đã thiết kế xong, trụ bình duyệt đầy đủ (mục 3.7). Nhưng đây là một bài toán *khác* (sắp thứ tự thời gian) ghép vào một bài toán đã đủ khó (sinh hướng dẫn không đáp án mẫu). Trộn hai câu hỏi vào một bài thì cả hai đều nông. Với tôi, nó xứng đáng là **bài báo thứ hai độc lập**, không phải một mục phụ hay bản dịch tiếng Việt của bài một (xem phê bình ở mục 6).

### Tóm một câu

Nếu không bị ép thời gian, tôi sẽ làm **một bài mạnh thay vì hai bài mỏng**: đổi khung sang *học chính sách từ chối có hiệu chỉnh* (đóng góp #1), vá chỗ VH-không-đáng-tin (#3), thêm thực nghiệm so lọc-sau-vs-ràng-buộc-trước (#4), nhắm venue quốc tế bình duyệt thay vì hội nghị quốc gia. Bài thứ hai để dành cho **nhiều màn** (#5) — trục chia sạch, không sợ bị coi là chẻ nhỏ nghiên cứu.

---

## 9. Việc cần quyết / câu hỏi còn mở

1. **Chạy tiếp deep-research** (`report/59`) để chốt: (a) DPO-trên-cặp-lọc có thật sự mới không; (b) risk–coverage đã có tiền lệ cho hallucination LLM/VLM chưa. Hai câu này quyết định đóng góp #1 và #2 ở mục 8 có đứng được không.
2. **Có nên trình bày hướng "không giới hạn thời gian" này cho giảng viên không**, hay giữ nguyên kế hoạch 3-tháng đã pre-register và để dành các ý ở mục 8 cho luận văn tiến sĩ / bài báo mở rộng sau?
3. **Bài thứ hai: giữ VCL (tiếng Việt) hay đổi sang nhiều-màn?** — nếu đổi thì phải tính lại lịch, vì nhiều-màn cần chạy cổng K-pair trước (chưa chạy).
4. **MDE thật là bao nhiêu** — chưa đo, đang chờ pilot baseline. Quyết định 12 app test có đủ hay phải tăng lên 15 phụ thuộc con số này.
5. Xác nhận thật CFP + deadline VCL2026, chính sách dual-submission của cả hai venue.

---

## 10. Cách làm việc với AI trong dự án này (để chat mới hiểu tôi muốn gì)

- Trao đổi bằng **tiếng Việt**, văn phong tự nhiên, **không được lộ giọng AI-gen** (tránh cụm máy móc kiểu "Nói một câu:", gạch ngang dài lặp lại, thanh "chốt" cuối mọi đoạn).
- Cấm tự chế thuật ngữ rồi dùng như chuẩn ngành — dùng đúng tên thật (ví dụ "View Hierarchy / VH", không bịa ra "bản kê nút").
- Khi làm slide thuyết trình: **ít chữ trên slide, phần giải thích dài đưa xuống note thuyết trình**; không viết slide theo giọng "dặn học viên" (vì người nói slide là chính học viên, không phải AI đang hướng dẫn học viên).
- Mọi con số/claim phải kiểm chứng được — nếu chưa đo thì nói rõ là ước tính/kỳ vọng, không trình bày như đã có.
- Trước khi thêm nội dung vào tài liệu tổng hợp, kiểm xem đã có chỗ khác nói rồi chưa — tránh lặp cùng một chuyện nhiều lần.
- Khi có phát hiện từ deep-research: phân biệt rõ **đã verify đối kháng** vs **chỉ mới trích claim thô, chưa kiểm chứng** — không được trộn lẫn hai mức độ tin cậy này khi trình bày.
