# PIPELINE & PHƯƠNG PHÁP ĐÁNH GIÁ — LÝ THUYẾT · VÍ DỤ · CĂN CỨ KHOA HỌC
### (bản trình bày cho thầy — mỗi phần theo mạch: lý thuyết → ví dụ step-by-step → vì sao chọn, dựa vào đâu → tiền lệ đã được công nhận)

---

## 0. ĐỊNH VỊ ĐỀ TÀI (đọc trước)

Luận văn có **hai đóng góp**, một mang giá trị **thực tiễn** và một mang giá trị **khoa học**:

- **(A) Hệ thống sinh hướng dẫn bám sát màn (thực tiễn).** Nhận ảnh + câu hỏi → sinh hướng dẫn từng bước **không trỏ tới nút không tồn tại**, và khi có nhiều màn thì **tự sắp đúng thứ tự**. Gắn được vào bất kỳ mô hình nào. Ứng dụng thật: trợ năng, hướng dẫn người mới dùng phần mềm, sinh tài liệu trợ giúp tự động.
- **(B) Phương pháp đánh giá khi không có đáp án mẫu (khoa học).** Đo độ trung thực mà không cần bản hướng dẫn chuẩn, không rơi vào "tự chấm"; và đo năng lực suy luận thứ tự + mức làm tới đích trên dữ liệu có đáp án vàng.

> **Trả lời thẳng nỗi lo "pipeline đơn giản":** cơ chế pipeline **cố ý đơn giản** (dùng mô hình có sẵn + một tầng hậu kiểm). Đây là **lựa chọn hợp chuẩn**, không phải điểm yếu — mục 3 và mục 6 dưới đây dẫn ra các công trình pipeline **đơn giản tương đương hoặc hơn** đã được nhận ở UIST/ACL/EMNLP/ICLR. Giá trị của luận văn nằm ở **đóng khung bài toán + đánh giá nghiêm**, đúng chỗ cộng đồng thưởng điểm.

---
# PHẦN A — PIPELINE ĐỀ XUẤT

## A1. Lý thuyết (kiến trúc)

Hệ thống có hai chế độ, dùng chung một dây chuyền (bộ định tuyến chọn theo số ảnh).

**Nhánh một màn (DG1) — ba khối nối tiếp:**
1. **Sinh (VLM, mù):** mô hình chỉ nhận **ảnh + câu hỏi**, viết hướng dẫn gọi nút theo tên. Không được cung cấp danh sách nút.
2. **Đối chiếu (thuật toán):** so từng tên nút với **danh sách nút thật** (View Hierarchy). Khớp → hợp lệ; không khớp → bịa.
3. **Hậu kiểm:** bước bịa được **viết lại thành mô tả bằng lời** (không đoán một nút thật khác).

**Nhánh nhiều màn (DG2) = nhánh một màn + một khối đặt trước:**
0. **Sắp thứ tự (Stage-0):** N ảnh xáo trộn → hỏi mô hình từng **cặp** "màn nào trước?" → tổng hợp bằng **Copeland** (đếm số lần được xếp trước) → phá vòng mâu thuẫn → xuất chuỗi màn đã sắp → đưa vào đúng ba khối của DG1.

> **Luật vàng xuyên suốt:** danh sách nút thật và đáp án vàng **chỉ dùng lúc chấm**, không lúc sinh hay lúc sắp thứ tự. Câu hỏi cũng không chứa tên nút. Đây là điều kiện để phép đo không bị "mớm bài".

## A2. Ví dụ chạy step-by-step

**Ví dụ DG1** — màn app chi tiêu, nút thật: `Add expense · Amount · Category · Save · Settings · Back`; câu hỏi *"làm sao thêm khoản chi mới?"*.
1. VLM (mù) viết: `1. Bấm Add expense · 2. Nhập Amount · 3. Bấm Submit · 4. Bấm Save changes`.
2. Đối chiếu: Add expense ✓ · Amount ✓ · **Submit ✗ (không có)** · Save changes ≈ Save ✓.
3. Hậu kiểm: "Bấm Submit" → *"Tìm và bấm nút để lưu khoản chi"*. Ba bước kia giữ nguyên.

**Ví dụ DG2** — luồng `A = Đăng nhập → B = Trang chủ → C = Hồ sơ`, đưa 3 ảnh **đã xáo** + mục tiêu.
0. Stage-0 hỏi cặp: A trước B, A trước C, B trước C → Copeland: A thắng 2, B thắng 1, C thắng 0 → sắp **A→B→C**.
   Rồi chuỗi A→B→C đi vào ba khối DG1 như trên.

## A3. Vì sao đề xuất pipeline này — căn cứ khoa học + tiền lệ

| Lựa chọn thiết kế | Vì sao (căn cứ) | Tiền lệ đã được công nhận |
|---|---|---|
| **Sinh rồi HẬU-KIỂM đối-chiếu-nguồn** (không sửa từ trong mô hình) | Mô hình mạnh vẫn bịa; một tầng kiểm-sau đối chiếu nguồn tham chiếu là cách giảm bịa mà không cần huấn luyện lại | **RARR** (Gao et al., **ACL 2023**): sinh → tra nguồn → sửa phần không được nguồn hỗ trợ, giữ phần còn lại — gần như chính cấu trúc của ta. **Chain-of-Verification** (Dhuliawala et al., **Findings ACL 2024**): draft → tự kiểm → viết lại. |
| **Oracle đặt BÊN CẠNH (chỉ để chấm + kích hậu kiểm), không đặt TRƯỚC** | Nếu đặt trước và lọc đầu vào cho mô hình thì bịa "biến mất" một cách giả tạo; đặt bên cạnh thì độ phủ thấp của nguồn chỉ **hạ độ tin phép đo**, không cắt bước | Nguyên tắc đo lường: giữ tình huống lỗi có cơ hội xảy ra mới đo được nó. |
| **Hậu kiểm CHỈ mô tả, KHÔNG đoán một nút thật khác** | Đã thử phương án "đoán nút gần nhất" và **đo được** nó gây lỗi ngầm (đổi Submit→Save trong khi đúng là nút khác) → nguy hơn để nguyên | Đây là một **đối chứng thất bại đo được** → biến lựa chọn thiết kế thành kết quả thực nghiệm. |
| **Sắp thứ tự bằng hỏi-từng-cặp + Copeland** (thay vì bắt mô hình phun cả dãy) | So từng cặp ổn định hơn, dễ phá vòng mâu thuẫn | **RankGPT** (Sun et al., **EMNLP 2023 — Outstanding Paper**): dùng LLM để xếp hạng — lineage kỹ thuật, được giải thưởng cao nhất. |
| **Bài "xáo ảnh rồi bắt xếp lại"** để đo năng lực suy luận thứ tự | Là bài chẩn đoán (diagnostic) trả lời "mô hình dựa vào đâu để biết thứ tự" | **VLM-SlideEval** (Kang et al., **NeurIPS 2025 Workshop**): xáo slide rồi bắt khôi phục thứ tự + perturbation — đối xứng trực tiếp. |
| **Sinh tutorial từng bước từ UI** là bài toán đáng làm | Nhu cầu thật (trợ năng, onboarding) | **HelpViz** (Zhong et al., **UIST 2021**), **ILuvUI** (Apple, **IUI 2025**) — sinh hướng dẫn/hiểu UI từ ảnh, pipeline đơn giản, đậu venue top. |

> **Thông điệp mục A3:** không có khối nào của pipeline là "tự nghĩ ra mà không có nền". Mỗi khối kế thừa một motif **đã được công nhận**; cái mới là **ghép chúng cho GUI mobile, neo bằng View Hierarchy, và gắn với đánh giá không-gold** — một khoảng trống chưa ai lấp đúng như vậy.

---
# PHẦN B — PHƯƠNG PHÁP ĐÁNH GIÁ (METRIC)

## B1. Lý thuyết từng thước đo

Ký hiệu: "danh sách nút thật" = View Hierarchy của màn; "đáp án vàng" = quỹ đạo đúng của AndroidControl.

**Nhóm một màn — chấm SO VỚI danh sách nút thật (không cần đáp án mẫu):**
- **Trung thực (Faithfulness):** `1 − (bước nhắc nút không tồn tại)/(bước có nhắc tên nút)`. Đo mức không-bịa.
- **Đúng nhãn:** `(bước gọi đúng tên hiển thị)/(bước trỏ nút có thật)`. Kiểm-tra-phụ.
- **Đúng chỗ (grounding):** nếu có toạ độ, kiểm điểm bấm rơi trong khung nút (`l≤x≤r, t≤y≤b`).

**Nhóm nhiều màn — chấm SO VỚI đáp án vàng:**
- **Thứ tự (τ thứ-tự-bộ-phận):** τ là hệ số tương quan thứ hạng Kendall (từ −1 đến +1). Công thức `τ = (C−D)/|M|`, chỉ tính **cặp bắt buộc** M (cặp mà một màn chắc chắn phải trước); C cặp thuận, D cặp nghịch.
- **Làm tới đích (Step-SR):** `(bước làm đúng)/(số bước đáp án vàng)`; một bước đúng = đúng loại thao tác **và** bấm trong dung sai 14% (hoặc cùng khung nút). Chấm kiểu teacher-forced (mỗi bước đưa màn vàng).

## B2. Ví dụ cụ thể (thế nào là 1 điểm, thế nào là 0 điểm)

| Thước đo | 1 điểm | 0 điểm |
|---|---|---|
| Trung thực | "Bấm **Save**" — có nút Save | "Bấm **Submit**" — không có |
| Đúng nhãn | Viết "Save" đúng tên | Viết "Save changes" (có nút Save nhưng sai tên) |
| Đúng chỗ | Bấm `(120,880)` trong khung `[100,850,200,900]` | Bấm `(240,880)` ngoài khung |
| τ (một cặp) | "Đăng nhập trước Hồ sơ" | "Hồ sơ trước Đăng nhập" |
| Step-SR (một bước) | Vàng "bấm Login (cx,cy)"; hệ "bấm Login" đúng loại + trong 14% | Hệ "bấm Settings" (sai đối tượng) hoặc lệch >14% |

*Ví dụ tính:* baseline DG1 = `1 − 1/4 = 75%`; sau hậu kiểm ≈ `95%` (chấm bằng bộ độc lập), cái giá fallback `25%`. DG2: vàng A<B<C, hệ sắp A,C,B → `τ = (2−1)/3 = +0.33`.

## B3. Vì sao chọn các thước đo này — căn cứ + tiền lệ

| Thước đo | Vì sao chọn (căn cứ) | Nguồn đã verify |
|---|---|---|
| **Faithfulness bằng khớp-nghĩa + ghép** | So chữ cứng sẽ tính oan đồng nghĩa ("Save changes"↔"Save"); so nghĩa mới đúng | **ALOHa** (Petryk et al., **NAACL 2024**): LLM trích đối tượng + embedding + **Hungarian** — chính cơ chế matcher của ta |
| **Grounding point-in-bbox** | Chuẩn ngành để chấm "bấm có trúng nút" | **SeeClick / ScreenSpot** (Cheng et al., **ACL 2024**) |
| **Ngưỡng dung sai 14%** | Để một cú bấm "đủ gần tâm nút" được tính đúng | **AITW** (Rawles et al., **NeurIPS 2023**) |
| **τ cho đo thứ tự (không dùng khớp-tuyệt-đối)** | Khớp-thứ-tự-tuyệt-đối với N=3 đã ~17% đúng do ngẫu nhiên, vô nghĩa; τ đo mức-độ-giống | **Lapata, Computational Linguistics 2006** (tiền lệ dùng τ chấm ordering); gốc **Kendall 1938** |
| **Partial-order (chỉ phạt cặp bắt buộc)** | Cặp tự do (điền email/sđt trước-sau đều được) đảo vẫn hợp lệ, không nên phạt oan | **Fagin et al., 2003 & 2006** (SIAM J. Discrete Math.) |
| **Step-SR / Action-Type** | Đo "làm theo có tới đích không" = đúng-ý, thứ chỉ có khi có đáp án vàng | **AndroidControl** (Li et al., **NeurIPS 2024**) |
| **Đánh giá không cần đáp án mẫu** | Với hướng dẫn UI, tạo đáp-án-vàng-toàn-văn là bất khả; đây là hướng chính đáng | Survey riêng: **Ito et al., "Reference-free Evaluation Metrics for Text Generation", 2025**; tiền lệ no-gold: **SelfCheckGPT (EMNLP 2023)**, **RAGAS (EACL 2024)** |
| **Validate chính thước đo bằng perturbation** | Chứng minh thước đo nhạy với lỗi mà không cần chấm-người | **Sai et al., "Perturbation CheckLists...", EMNLP 2021** |
| **Chống tự-chấm: tách công cụ QUYẾT khỏi công cụ CHẤM (ba cơ chế)** | Cộng đồng đã chỉ ra "AI tự chấm không neo người thì không đáng tin"; tách công cụ là câu trả lời trực tiếp | **"No Free Labels" (2025)**, **"Reliability without Validity" (2026)** — chứng minh vấn đề này khó & đáng giải |

> **Thông điệp mục B3:** **5/6 nhóm thước đo là peer-reviewed** (NAACL/ACL/NeurIPS/CL journal/SIAM/EMNLP); riêng "đúng nhãn" là tự-định-nghĩa và ta khai thẳng, dùng làm kiểm-tra-phụ. Không có thước đo nào "tự chế mà không nền".

---
# PHẦN C — ĐỊNH VỊ SO VỚI TIỀN LỆ (ta khác gì)

| Công trình được công nhận | Họ làm gì | Ta kế thừa / khác gì |
|---|---|---|
| **RARR** (ACL 2023), **CoVe** (ACL 2024) | Sinh → kiểm-chứng-nguồn → sửa phần không có nguồn | Kế thừa **motif hậu-kiểm**; khác: neo bằng **View Hierarchy của GUI**, và **mô tả-không-đoán** (có đối chứng thất bại) |
| **HelpViz** (UIST 2021), **ILuvUI** (IUI 2025) | Sinh/hiểu hướng dẫn từ UI, pipeline đơn giản | Cùng dòng; khác: **đánh giá không-gold + chống-tự-chấm** (họ chưa làm) |
| **RankGPT** (EMNLP 2023 Outstanding), **VLM-SlideEval** (NeurIPS 2025 WS) | LLM sắp thứ tự / xáo-rồi-khôi-phục | Kế thừa **motif sắp-thứ-tự**; khác: **GUI mobile + điều kiện theo mục tiêu + partial-order-aware + gắn vào sinh tutorial** |
| **ALOHa** (NAACL 2024), **G-Eval/FActScore/SelfCheckGPT** (EMNLP 2023), **RAGAS** (EACL 2024) | Metric / phương pháp đánh giá, pipeline đơn giản | Kế thừa **cơ chế đo**; khác: áp cho **hướng dẫn UI không-gold** + **tách quyết/chấm chống tautology** + **validate bằng perturbation** |

**Khoảng trống hợp pháp mà luận văn lấp:** chưa ai ghép "hậu-kiểm-đối-chiếu-View-Hierarchy + sắp-thứ-tự-màn-theo-mục-tiêu + đánh-giá-không-gold-chống-tự-chấm" cho bài **sinh hướng dẫn sử dụng phần mềm**.

---
# PHẦN D — GIÁ TRỊ THỰC TIỄN & KHOA HỌC

- **Thực tiễn (nói đúng phạm vi):** hệ thống hữu ích nhất ở **kịch bản chạy TRÊN máy (on-device) / trợ năng**, nơi **accessibility tree có sẵn LIVE** (Android cấp qua AccessibilityService — trình đọc màn hình và công cụ trợ năng đều dùng). Ở đó tầng hậu kiểm chạy được thật, **giảm rủi ro dẫn người dùng tới nút không tồn tại**. Với kịch bản **chỉ có một ảnh** (không truy cập máy), cần một bộ dò phần tử (recall không hoàn hảo) → độ trung thực thành *"có điều kiện recall"* (đo bằng cổng K1). Chi phí thấp (không huấn luyện lại, không GPU cho phần lõi).
  - *Lưu ý phân biệt:* "chấm baseline rồi so" là bước ĐÁNH GIÁ (nghiên cứu), không phải một bước trong hệ khi deploy. Hệ deploy chỉ gồm: sinh → kiểm từng bước với danh sách nút → né bước bịa.
- **Khoa học:** (1) một **phương pháp đánh giá đáng tin khi không có đáp án mẫu**, chống tự-chấm — đúng một mối quan tâm nóng 2025–2026; (2) các **phát hiện thực nghiệm**: tỉ lệ VLM bịa nút UI, đối chứng "đoán-nút gây lỗi ngầm", và (ở DG2) **mô hình dựa vào tín hiệu nào** để suy ra thứ tự.

---
# PHẦN E — GIỚI HẠN & ĐIỀU KIỆN ĐỂ CHẮC ĐẬU

**Giới hạn tự nêu:** một màn chỉ đo *không bịa*, chưa đo *đúng ý* (đẩy sang Step-SR ở đa màn); độ trung thực sau hậu kiểm phần lớn tất yếu do thiết kế (nên báo tỉ lệ bịa của bản gốc); hậu kiểm đổi độ-cụ-thể lấy độ-an-toàn (một phần bước thành mô tả khái quát); Step-SR là cận dưới (so một quỹ đạo); "đúng nhãn" là tự-định-nghĩa.

**Ba việc để chắc đậu (theo đúng gương các bài trên):**
1. **DG2 phải ra số dương thật** (τ + Step-SR trên AndroidControl) — vì đây là con số *năng lực thật*, không by-construction; đây là trụ nặng nhất.
2. **Validate thước đo nghiêm** — perturbation-test kiểu Sai 2021 + **một mảnh neo-người nhỏ** (các bài G-Eval/RAGAS đều có tương quan-người); đây là chỗ reviewer thưởng điểm.
3. **Đo trên vài mô hình** (cross-model hallucination) để phát hiện có bề rộng.

> **Một dòng để trình thầy:** *"Pipeline của em cố ý đơn giản theo đúng mẫu đã được công nhận (RARR/CoVe/HelpViz/RankGPT); đóng góp không nằm ở độ phức tạp kỹ thuật mà ở (i) một hệ thống thực tiễn giảm bịa nút, và (ii) một phương pháp đánh giá đáng tin khi không có đáp án mẫu — một hướng có survey riêng và đang là mối quan tâm nóng 2025–2026. Em chứng minh giá trị bằng đánh giá nghiêm, đúng chỗ cộng đồng thưởng điểm."*
