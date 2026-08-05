# 92 — Giai đoạn B (dựng lại thước) + quét scoop tác vụ — 19/7/2026

> Hai việc free chạy hôm nay: (B) dựng lại bộ kiểm thước cho độc lập với chính thước, rồi đo bằng ca thật; (S) quét văn liệu xem tác vụ "sinh hướng dẫn cho người từ ảnh" còn bị ai chiếm chỗ. Kết quả cả hai đều đáng chú ý và cần bạn quyết.

---

## PHẦN B — THƯỚC RỚT CỔNG TRÊN CA THẬT (kết quả cứng nhất)

### Đã làm gì

Report/90 §B yêu cầu dựng lại bộ bơm-lỗi cho **độc lập** với hàm `target_of()` của thước (bộ cũ gọi chính hàm đó rồi dán lại → AUC=1.000 là hằng đẳng thức). Đã làm:

- **`harness/metric_v2.py`** — thước đã vá 5 lỗi cơ học: (1) nhãn nút `Next/Back/Open/Enter/Go` sống sót (v1 nuốt vào STOP → đích rỗng); (2) đích rỗng không cho khớp; (3) luật cứng cho toggle/số/siêu-tập; (4) ghép 1-1 tối ưu thay phủ-tập; (5) bỏ dấu câu.
- **`harness/metric_v2_validate.py`** — **51 cặp viết tay**, không suy từ thước: 25 cặp *cùng nút khác chữ* (thước phải khớp), 15 cặp *nút khác có chồng token* (phải bác), 11 ca *hiểm* (toggle/số/hướng/cha-con, phải bác).

### Kết quả

| Số | Giá trị | Cổng |
|---|---|---|
| **AUC(cùng-nút > khác-nút)** | **0.336** | ≥ 0.80 → **RỚT** |
| SAME (cùng nút) điểm TB | 0.067 | nên cao |
| DIFF+HIỂM (khác nút) điểm TB | ~0.18 | nên thấp |
| false-positive (cùng nút bị bác oan) | **96%** (24/25) | ≤ 15% |
| ca K1-khó (icon ↔ tên, không chung chữ) bị bác oan | **19/19** | — |

Thước bác **đúng** gần hết ca khác-nút (detection 96%) — nhưng **bác oan gần hết ca cùng-nút**. Nó biến thành cái máy nói "không khớp" với mọi thứ. AUC 0.336 còn **tệ hơn** ước lượng 0.35 của phản biện.

### Vì sao — và vì sao không sửa bằng cách chỉnh ngưỡng

Đo thẳng độ giống bge-m3 giữa hai vế:

| Loại cặp | Ví dụ | bge cos |
|---|---|---|
| **cùng nút** (nên cao) | search ↔ magnifying glass | 0.55 |
| | menu ↔ hamburger | 0.63 |
| | settings ↔ gear | 0.60 |
| | compose ↔ pencil | **0.46** ← thấp nhất |
| **khác nút** (nên thấp) | inbox ↔ outbox | **0.76** ← cao nhất |
| | gmail tab ↔ calendar tab | 0.72 |
| | photos tab ↔ videos tab | 0.74 |

**Cùng-nút trung bình 0.62, khác-nút trung bình 0.67 — khác-nút còn CAO hơn.** Điểm thấp nhất của cùng-nút (0.46) nằm dưới điểm cao nhất của khác-nút (0.76). **Không có ngưỡng bge nào tách được** — hạ ngưỡng chỉ làm khác-nút lọt nhiều hơn.

Lý do bản chất: **embedding đo độ gần chủ đề.** Một icon và tên chức năng của nó (kính lúp ↔ tìm kiếm) xa nhau về chủ đề; còn hai nút trong cùng một app (Gmail ↔ Calendar) thì gần chủ đề. Nên embedding đặt sai thứ tự đúng cái ta cần. Đây chính là **bức tường K1**, giờ được xác nhận nghiêm ngặt bằng số trên ca thật.

### Có đường cứu không? — từ điển ký hiệu: đỡ, chưa đủ

Thử thêm **từ điển chuẩn hoá icon→chức năng** (kính lúp→search, bánh mì kẹp→menu, thùng rác→delete, phễu→filter...) áp lên cả hai vế trước khi so:

| | Trước | Sau từ điển |
|---|---|---|
| AUC | 0.336 | **0.735** |
| cùng-nút bị bác oan | 96% | 48% |

Kéo lên đáng kể nhưng **vẫn dưới cổng 0.80**, và **con số này còn lạc quan** vì từ điển được dựng *sau khi nhìn* đúng mấy ca test (chỉnh thước theo test = circular). Từ điển cũng không cứu được:

- **đồng nghĩa chữ**: `Log in` ↔ `Sign in`, `search bar` ↔ `search field` (không phải icon)
- **cách diễn đạt dài hơn**: `Type your email` ↔ `Enter your email address`

Còn một lỗi cơ học sót: số một chữ số (`quantity 5` vs `quantity 2`) bị lọc mất trước khi luật-số chạy → khớp oan. Dễ vá, nhưng không đổi bức tranh lớn.

### Nghĩa là gì

Đây **đúng là "cổng có thể rớt thật"** mà report/90 đã báo. Khác cổng cũ (hằng đẳng thức, không rớt được), cổng này rớt thật, trên ca thật, với lý do bản chất chứ không phải lỗi vặt.

**Không có nghĩa luận văn chết.** Nghĩa là: cách đo độ-ĐÚNG bằng (thao-tác, đích) + chồng-từ + embedding **không tách sạch được** trên nhóm nút icon/đồng nghĩa — đúng ~20% nút mà K2/OCR đã chỉ. Ba đường đi tiếp, cần thầy quyết (câu 1 và 3 của report/90 Phần 8):

1. **Đầu tư từ điển chuẩn hoá cho tử tế** — dựng từ nguồn độc lập (bảng icon report/75 + glossary UI chung), **đóng băng**, rồi đo trên tập cặp **held-out** (không phải 51 cặp này). Nếu qua 0.80 thật thì thước sống. Rẻ, vài ngày, nhưng chưa chắc đủ vì phần đồng-nghĩa-chữ vẫn hở.
2. **Đổi thước chính** — ví dụ dùng LLM-judge khác họ làm trục chính (chấp nhận đánh đổi về chống-tự-chấm), hoặc đo grounding bằng toạ độ nếu tải được a11y-tree.
3. **Thu hẹp phạm vi** — báo trung thực giới hạn của thước, đẩy trọng tâm luận văn sang **chương đo lường** (bốn phép thử + phát hiện về thước — bản thân việc chứng minh "không thước tự động nào tách được chỗ này" đã là một đóng góp đo-lường).

**Khuyến nghị của tôi:** mang thẳng kết quả này ra gặp thầy, kèm ba đường. Đừng tự chọn — đây là chỗ rẽ lớn. Trong lúc chờ, việc **C (đối chiếu thước với người)** vẫn nên chạy: nếu người chấm cũng thấy icon↔tên là "cùng nút dùng được" thì càng khẳng định thước đang đo sai thứ.

---

## PHẦN S — QUÉT SCOOP: TÁC VỤ CÓ BỊ CHIẾM CHỖ KHÔNG

### Câu trả lời ngắn

**Có — vòng kiểm cũ (report/82) bỏ sót hai bài CHI 2026 đúng trọng tâm.** Nguy hiểm nhất là **GuideMe (CHI 2026)**. Nhưng nó là bài **hệ thống HCI** (prompt VLM lớn + nghiên cứu người dùng), **không train model, không có benchmark, không dùng AndroidControl** — nên phần đóng góp kỹ thuật của luận văn vẫn sống, chỉ có khung *"tác vụ mới hoàn toàn"* là chết.

### Các bài chiếm chỗ / lân cận (đã verify DOI)

| Bài | Venue | Tác vụ | Train? | Đe doạ |
|---|---|---|---|---|
| **GuideMe** | CHI 2026 (10.1145/3772318.3791448) | người cao tuổi hỏi trong app → VLM sinh hướng dẫn từng bước tô sáng tại chỗ | **không** (suy đoán mạnh, chưa đọc full-text) | **chiếm chỗ tác vụ** |
| **AskEase** | CHI 2026 (10.1145/3772318.3790661) | hướng dẫn từng bước cho người dùng screen-reader trên **desktop** | không (prompt GPT-5) | lân cận mạnh |
| **GUITrans2Act** | preprint (2606.12817) | dịch trajectory → tri thức thao tác cho **agent máy** | có | lân cận (máy đọc) |
| Widget Captioning | EMNLP 2020 | mô tả **một** widget | có | xa |
| Screen2Words | UIST 2021 | tóm tắt cả màn thành **một câu** | có | xa |
| OS-Genesis | ACL 2025 | sinh task ngược để train **agent** | có | xa |
| Aguvis | ICML 2025 | agent sinh **action cho máy**, AC ở **đầu vào** | có | xa (đúng cái ta nói "mọi bài khác làm") |
| FaithScore | Findings EMNLP 2024 | metric faithfulness self-probe | — | lân cận đóng-góp-đánh-giá |
| HalluClear | preprint (2604.17284) | đo hallucination của **GUI agent** | — | lân cận đóng-góp-đánh-giá |

### Bốn đóng góp — cái nào sống

1. **"Người đọc là NGƯỜI"** → **chết như tính-mới độc lập** (GuideMe + AskEase đã làm). Hạ xuống *đặc tính bài toán*, không phải đóng góp.
2. **"Nhiều bước theo câu hỏi"** → **chết như tính-mới độc lập** (GuideMe làm đúng query→multi-step).
3. **Đánh giá reference-free bằng View Hierarchy** → **sống có điều kiện, là trụ mạnh nhất còn lại.** Chưa ai dùng VH làm nguồn-ngoài-có-cấu-trúc để bắt bịa tên nút trong *văn bản hướng dẫn sinh* + validate bằng bơm-lỗi + dùng để lọc data train. Phải phân định rõ với FaithScore (tự-hỏi-lại, không nguồn ngoài) và HalluClear (đo agent, không phải generator cho người).
4. **AndroidControl step_instructions làm ĐÍCH SINH** → **sống, sạch nhất, nhưng hẹp.** Không bài nào dùng trường này làm đích sinh; mọi bài để nó ở đầu vào. Nhưng bản thân nó chỉ là "cách dùng dataset", phải đi kèm (3) và phần model.

**Trục tính-mới còn đứng = tổ hợp:** mô hình nhỏ mở **được huấn luyện** + tái lập được (khác GuideMe/AskEase = prompt API + user-study) × dùng AC-step-instructions làm đích × đánh giá reference-free-VH có cổng-bơm-lỗi × chương đo-lường bốn phép thử. Không phải "tác vụ mới", mà là **hiện thực hoá tác vụ đó bằng model nhỏ + đánh giá định lượng tái lập được** — thứ hai bài CHI kia không cung cấp.

### Câu định vị an toàn cho related work

> Các hệ thống HCI gần đây đã cho thấy giá trị của việc sinh hướng dẫn thao tác từng bước cho người dùng cuối từ ảnh giao diện — GuideMe (CHI 2026) cho người cao tuổi trên di động, AskEase (CHI 2026) cho người dùng screen-reader trên desktop — nhưng **cả hai đều prompt một VLM/LLM thương mại lớn và đánh giá bằng nghiên cứu người dùng, không huấn luyện mô hình mở nào và không cung cấp thước faithfulness định lượng tái lập được.** Song song, các bài GUI-agent (Aguvis ICML 2025; OS-Genesis ACL 2025) dùng hướng dẫn từng bước làm *đầu vào/nhãn cho dự đoán hành động của máy*. Luận văn này khác ở (i) **huấn luyện một VLM nhỏ mở** cho tác vụ sinh-hướng-dẫn-cho-người, (ii) dùng `step_instructions` của AndroidControl làm **đích sinh** thay vì đầu vào, (iii) đề xuất khung **đánh giá reference-free dựa trên View Hierarchy, kiểm chứng bằng bơm-lỗi** — khác faithfulness self-probe (FaithScore) và đo-hallucination-cho-agent (HalluClear).

**Cấm nói:** "đầu tiên sinh hướng dẫn cho người", "đánh giá kép là phát kiến", "VLM nhỏ trên máy là trục chính".

### Việc còn hở (khai thẳng)

- **GuideMe full-text bị ACM chặn** → câu "không train, chỉ prompt VLM" vẫn là **suy đoán**, chưa chắc. Đây là bài quyết định — **lấy PDF qua thư viện trường trước khi khoá framing với thầy.**
- GUITrans2Act, HalluClear mới đọc snippet, cần full-text.
- ExplorAR (2508.01282) cũng "trợ giúp người cao tuổi học app" — nên liếc.
- Chưa quét sâu ASSETS / IMWUT / MobileHCI 2024-2026.

---

## GỘP LẠI: VIỆC KẾ ĐỔI GÌ

| | Trước hôm nay | Sau hôm nay |
|---|---|---|
| Giai đoạn B | "dựng lại thước, chấp nhận có thể rớt" | **đã chạy → RỚT (AUC 0.336). Cần thầy quyết ba đường.** |
| Related work | "phải phân định GUITrans2Act" | **thêm GuideMe + AskEase (CHI 2026), hạ claim tác vụ, lấy PDF GuideMe** |
| Gặp thầy (E) | chung chung | **có hai thứ cụ thể mang đi: thước rớt + ba đường; và framing sau GuideMe** |

**Việc C (chấm 91 màn) càng nên chạy** — nó xác nhận độc lập rằng người có coi icon↔tên là "cùng nút dùng được" không. Nếu có, thì kết quả B càng vững: thước đang đo sai thứ luận văn cần.

Bằng chứng: `harness/metric_v2.py`, `metric_v2_validate.py`, `metric_v2_results.json`. Nguồn scoop: agent deep-research 19/7 (đã verify DOI GuideMe/AskEase/Aguvis/OS-Genesis/Widget Captioning/Screen2Words).
