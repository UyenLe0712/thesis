# 🛡️ HỒ SƠ BẢO VỆ HỘI ĐỒNG — câu hỏi khó & câu trả lời (kèm bằng chứng)

> **Hồ sơ này là gì?** Một bộ **"câu hỏi khó hội đồng hay hỏi" + "câu trả lời chắc chắn"**, để khi bảo vệ bạn không bị dồn vào góc. Mỗi câu trả lời **có bằng chứng** (kết quả ta đã chạy thật, hoặc bài báo bình duyệt, hoặc thiết kế đã chốt). Phần cuối **tự nêu điểm yếu + cách đỡ** và **những lỗ hổng cần vá trước khi bảo vệ**. Viết dễ hiểu cho người chưa quen.
> **Cách dùng:** đọc Phần 1 (câu phòng thủ tủ) → lướt Phần 2 (Q&A) → đọc Phần 3–4 (điểm yếu + việc cần làm). Khi tập bảo vệ, người khác hỏi bạn theo các câu này.

---

## PHẦN 1 — CÂU PHÒNG THỦ "TỦ" (học thuộc 1 đoạn này)

> *"Đề tài có **hai đóng góp**: (1) một **hệ sinh hướng dẫn bám sát ảnh** — gắn 'lớp làm-cho-trung-thực' lên bất kỳ model mạnh nào để giảm bịa nút và tăng độ làm-theo-được; (2) một **phương pháp đánh giá đáng tin khi không có bài mẫu chuẩn**. Em **không** tuyên bố hệ mạnh nhất thế giới; em chứng minh — **bằng thí nghiệm đã chạy thật** — rằng lớp của em làm hướng dẫn trung thực hơn so với để chính model đó viết tự do, đúng trên nhiều model, và **cách đo của em phân biệt được model tốt/dở**. Mọi giả thuyết đều **đăng ký trước**, nên kết quả dù dương hay null đều là đóng góp."*

---

## PHẦN 2 — CÂU HỎI KHÓ & CÂU TRẢ LỜI

### NHÓM A — Đóng góp & độ mới

**❓ "Đề tài chỉ là đánh số nút rồi prompt model, có gì mới?"**
✅ Đóng góp **không** nằm ở phần sinh (cố ý dùng đồ có sẵn), mà ở **(1) phương pháp ĐÁNH GIÁ** khi không có đáp án mẫu — gồm 4 cái mới: chống-vòng-lập-luận (nhãn "cặp bắt buộc" suy từ đáp án vàng, không tự chấm), truy-nguồn-tín-hiệu theo từng loại cue, chấm-thứ-tự-bộ-phận, và audit người; **(2) "lớp làm-cho-trung-thực" độc-lập-model** mà em đã **đo được giá trị**: nó biến các "lệnh bấm nút sai mà tự tin" thành mô tả trung thực.

**❓ "2026 có GPT-5/Gemini-3 rồi, làm cái này còn ý nghĩa?"**
✅ Có. Bài bình duyệt 2026 (*"Do GUI Grounders Truly Understand UI Elements?"*, Findings of EACL 2026) chỉ ra **các model mạnh nhất VẪN bịa nút, vẫn đặt sai vị trí**. Em đã **đo trên máy**: model mạnh hơn (7B) bịa **ít hơn** model nhỏ (3B) — 25% so 40.7% — **nhưng vẫn >0**. Vì đóng góp của em là **cách đánh giá + cái lớp (model thay được)**, nên GPT-6 ra đời chỉ làm **số đẹp hơn**, **không làm đề tài lỗi thời**.

**❓ "Pipeline chỉ là wrap model, sao gọi là đóng góp?"**
✅ Vì (a) **cái lớp** đã chứng minh có giá trị đo được (xem Nhóm E), (b) nó **model-agnostic** (cắm model nào cũng chạy) — đây là kiểu đóng góp **bền** mà literature công nhận (vd SeeAct ICML 2024, VDGD ICLR 2025: lớp grounding là đóng góp, model là mảnh thay được), (c) đóng góp **chính** vẫn là phương pháp đánh giá.

### NHÓM B — Cách đánh giá (đóng góp lõi)

**❓ "Không có đáp án mẫu thì lấy gì chấm? Có đáng tin không?"**
✅ Neo bằng **cây phần tử thật của màn (View Hierarchy / accessibility tree)** — gọi là "đáp án bạc" — chỉ dùng **lúc chấm**, không cho model xem lúc sinh. Độ tin được **chứng minh 3 lớp**: (1) đã chạy thật → metric **phân biệt được** model 3B vs 7B (40.7% vs 25% bịa) → metric "có răng"; (2) **validate với người** (Track B: BWS + Krippendorff α + tương quan); (3) **đăng ký trước** ngưỡng.

**❓ "Có bị VÒNG LẬP LUẬN (tự ra đề tự chấm) không?"**
✅ Không. Nhãn "cặp bắt buộc" để chấm thứ tự **suy từ ĐÁP ÁN VÀNG của AndroidControl bằng quy tắc nhân-quả tất định** (màn B chỉ xuất hiện sau khi làm đúng thao tác ở màn A), **KHÔNG** lấy từ chính bộ dò-tín-hiệu mà model dùng → tránh tự chấm. Có **audit người 50–80 cặp** để kiểm.

**❓ "Matcher khớp tên có vu oan đồng nghĩa là 'bịa' không?"**
✅ Đã xử và **chứng minh bằng số**: matcher chuỗi-thô **thổi phồng bịa 40.7%**; đổi sang **ALOHa (so theo NGHĨA)** còn **33.3%** — 2 bước là synonym của nút thật bị vu oan đã được sửa. Hơn nữa em **tách 2 số**: **Bịa** (nút có tồn tại không — đồng nghĩa OK) vs **Đúng-nhãn/Clarity** (gọi đúng tên hiển thị không — gọi "Thiết lập" cho nút "Cài đặt" thì trừ clarity vì người dùng khó tìm, **không** tính bịa).

**❓ "Coverage (đủ ý) chia cho cái gì? Tutorial tập trung mà bị phạt thì oan?"**
✅ Đúng — nên coverage **đo trên AndroidControl** (có **đáp án vàng từng bước** → biết nút nào THỰC SỰ cần), **có trọng số bước quan trọng**; và em **đăng ký trước quy tắc lọc element**. MobileViews (không gold) chỉ là proxy nhẹ.

### NHÓM C — Dataset

**❓ "Tự soạn câu hỏi cho MobileViews — có bịa dữ liệu không?"**
✅ **Chỉ MobileViews** thiếu câu hỏi → tự soạn theo **protocol công khai** (mỗi màn 1–2 câu "làm sao để X", X làm được trên màn, có người duyệt). **AndroidControl có `goal` THẬT** và **ScreenSpot có instruction THẬT** → không tự soạn. **Phần định lượng NẶNG dồn vào AndroidControl** (dataset bình duyệt + goal thật) → claim chính không dựa câu-hỏi-tự-soạn. Quan trọng: tự soạn **câu hỏi (input)** ≠ bịa **đáp án (để chấm)** — đáp án vẫn là dữ liệu thật.

**❓ "Dataset tiếng Anh mà đề tài hướng tiếng Việt?"**
✅ Pipeline/metric **vốn ngôn-ngữ-độc-lập** (chấm bằng toạ độ/khớp tên). Em **chứng minh định lượng trên tiếng Anh** (có dataset chuẩn) trước, **tiếng Việt làm demo định tính** (app VN thật). Em **trung thực**: không có bảng số tiếng Việt vì **thiếu dataset chuẩn VN có sẵn nhãn+toạ độ** — đây là giới hạn dữ liệu, không phải pipeline không làm được (em đã đo: embedder tiếng Việt yếu → cần bản đa ngữ, để future-work).

**❓ "Xáo trộn N ảnh rồi bắt xếp lại — bài toán này thực tế không?"**
✅ Em nói thẳng: đây là **bài toán ĐẶT RA để ĐO** năng lực suy luận trật tự (trả lời đúng câu hỏi 'làm sao model biết thứ tự màn'), **không** khẳng định là nhu cầu deploy phổ biến. Em còn **lọc bỏ episode có các màn gần-trùng** (xáo rồi cũng không phân biệt được) để bài đo **có nghĩa**.

### NHÓM D — Pipeline / kỹ thuật

**❓ "Sao bỏ Set-of-Mark/bộ-dò khỏi đường chính?"**
✅ Vì 2026 các model ground toạ độ **trực tiếp tốt hơn** SoM trên giao diện mobile (UGround ICLR 2025: native 46.8% vs SoM 25.6%), và bộ-dò đặt-trước **chặn trần** tutorial (sót nút → thiếu bước). Em đổi sang **oracle đặt BÊN CẠNH** (chỉ để chấm + kích fallback) → recall thấp chỉ hạ **độ tin phép đo**, không cắt tutorial. SoM **giữ làm 1 nhánh đối chứng (ablation)**.

**❓ "Bộ dò sót nút (recall thấp) thì kết quả còn tin được không?"**
✅ Em **tự đo recall trước (cổng K1)** và mọi số grounding ghi rõ "trong điều kiện recall = X%". Và design E **không** để recall chặn việc sinh → ảnh hưởng nhỏ hơn bản cũ.

**❓ "Literature nói LLM không tự sửa được — sao còn dùng verifier/self-refine?"**
✅ Đúng với **tự-sửa-không-có-tín-hiệu-ngoài** (Huang ICLR 2024). Nhưng verifier của em (V2) là **một model KHÁC** đọc lại → đây là **phản hồi từ bên ngoài**, đúng điều kiện mà literature nói là **có tác dụng** (CRITIC ICLR 2024). Em còn **ablation từng tầng** để chứng minh tầng nào thực sự đáng giữ ("null vẫn đậu" nếu tầng nào không có ích).

### NHÓM E — Kết quả & khả thi (mạnh nhất — có bằng chứng đã chạy)

**❓ "Đã chạy thử chưa? Có bằng chứng gì hệ chạy được?"**
✅ **Có — đã chạy THẬT, miễn phí, trên CPU** (Ollama + Qwen2.5-VL): (1) pipeline chạy end-to-end; (2) metric **nhạy** — phân biệt 3B (bịa 40.7%) vs 7B (bịa 25%); (3) **lớp fallback** biến mọi "lệnh bấm nút sai-tự-tin" → 0%; (4) **matcher ALOHa** cho con bịa đáng tin hơn (sửa 40.7%→33.3%). *(Chi tiết: `report/15`.)*

**❓ "Chứng minh hệ tốt hơn GPT-5 kiểu gì?"**
✅ **Không** so văn hay (frontier hay hơn). Em so trên **trục trung-thực / đúng-chỗ / làm-theo-được**, **trên cùng một model** (model + lớp của em > model viết tự do), trên **nhiều model**, ở **chi phí thấp**. Và đóng khung trung thực: giá trị lớp **giảm khi model mạnh lên nhưng vẫn dương** (đã đo: 40.7%→25%).

**❓ "Lỡ kết quả không đẹp / hệ không thắng baseline thì luận văn hỏng à?"**
✅ Không. Em **đăng ký trước (pre-registration)** giả thuyết + ngưỡng → **kết quả null vẫn là đóng góp** ("đã kiểm soát X, cơ chế Y không cải thiện — và đây là lý do"). Luận văn có **HAI đóng góp ngang nhau** (hệ + cách đánh giá); nguyên tắc "null vẫn đậu" áp cho **nhánh đánh giá + phần đo-cơ-chế của hệ** → không lệ thuộc "hệ phải thắng".

**❓ "Chi phí/khả thi? Cần siêu máy tính không?"**
✅ Không. Đã chạy phần lớn **miễn phí trên CPU**. Chạy quy mô lớn chỉ cần **1 GPU thuê (Colab) + ~$100–300 API** đối chứng. Em **đăng ký trước để chạy MỘT LẦN**, không chạy-đi-chạy-lại tốn kém.

### NHÓM F — Thống kê / nghiêm ngặt

**❓ "Mẫu bao nhiêu? Có ý nghĩa thống kê không? Sao biết không phải may rủi?"**
✅ Kế hoạch: **≥30 episode mỗi mốc N**, vài trăm màn cho DG1, **kiểm định ghép cặp (paired permutation + bootstrap CI) + effect size + hiệu chỉnh đa-kiểm-định Holm-Bonferroni**. Chống may rủi/"chạy tới khi đẹp" bằng **pre-registration** (đăng ký trước cách làm + ngưỡng). *(3 lần chạy vừa rồi là smoke-test sơ bộ, đã nói rõ.)*

---

## PHẦN 3 — ĐIỂM YẾU TỰ NÊU (nêu trước khi hội đồng bắt) + CÁCH ĐỠ

| Điểm yếu (thật) | Cách đóng khung / đỡ |
|---|---|
| Phần sinh nhẹ kỹ thuật (đánh số + prompt + lớp) | **Có chủ ý** — đóng góp ở đánh giá + lớp model-agnostic, không claim SOTA. |
| Kết quả nhạy với chất lượng câu hỏi (đã thấy 91.7% vs 59.3%) | Có **protocol câu hỏi** + dồn claim nặng vào AndroidControl (có goal thật). |
| Coverage trên màn không-gold chỉ là proxy | Đo coverage + làm-theo-được (Step-SR) **trên AndroidControl** (có gold). |
| Recall bộ dò chưa công bố rõ | **Tự đo (K1)** + đóng khung "có điều kiện recall"; design E giảm phụ thuộc. |
| Không có bảng số tiếng Việt | Giới hạn **dữ liệu** (thiếu dataset VN có nhãn), không phải pipeline; VN = demo. |
| "Thắng frontier" chỉ ở trục hẹp + giảm khi model mạnh | Nói thẳng, có số (40.7%→25%); claim 2 mức (chắc-thắng vs bonus). |
| Ngưỡng matcher (τ) là lựa chọn | **Pre-register + audit người** để chốt; báo độ nhạy theo ngưỡng. |

---

## PHẦN 4 — LỖ HỔNG CẦN VÁ TRƯỚC KHI BẢO VỆ (việc còn lại)
1. **Protocol câu hỏi use-case** cho MobileViews (đang làm tiếp). ⏳
2. **Chạy quy mô đủ** (vài trăm màn DG1 + AndroidControl DG2) trên Colab — **một lần**, sau khi pre-register. ⏳
3. **Parse cây accessibility AndroidControl** (proto `android_env`) — đã verify khả thi, cần code + chạy. ⏳
4. **Audit người** một subset (kiểm matcher + nhãn cặp bắt buộc) → báo % khớp. ⏳
5. **Validate metric với người (Track B)** — BWS + Krippendorff α. ⏳
6. **Bảng pre-registration chính thức** (giả thuyết + ngưỡng + quy tắc quyết định). ⏳
> Trạng thái: 1–6 là việc còn lại; phần **"logic chạy được + metric đáng tin"** đã **chứng minh miễn phí** (Phần 5).

---

## PHẦN 5 — BẰNG CHỨNG (cầm ra hội đồng được)

**Đã chạy thật (Ollama/CPU, miễn phí) — `report/15`:**
- Pipeline design E chạy end-to-end trên dữ liệu MobileViews thật.
- Metric **nhạy**: bịa 3B = 40.7% vs 7B = 25.0% (model mạnh hơn bịa ít hơn — đúng kỳ vọng).
- Lớp **fallback**: lệnh-sai-tự-tin 40.7% → **0%**.
- Matcher **ALOHa**: bịa 40.7% (chuỗi) → 33.3% (đáng tin hơn); tách **Bịa vs Đúng-nhãn (Clarity 59.3%)**.

**Nền lý thuyết (bình duyệt):** EACL 2026 (frontier vẫn bịa) · SeeClick ACL 2024 (point-in-bbox) · ALOHa NAACL 2024 (khớp theo nghĩa) · VALOR-EVAL ACL 2024 (đo coverage cùng faithfulness) · UGround/OS-Atlas ICLR 2025 (native grounding) · AndroidControl NeurIPS 2024 (goal + gold) · Lapata CL 2006 + Fagin (chấm thứ tự) · Huang ICLR 2024 / CRITIC ICLR 2024 (verifier ngoài mới có tác dụng) · AITW NeurIPS 2023 (ngưỡng 14%).

**Thiết kế đã chốt + verify:** `report/14` (design E + 3 tinh chỉnh) · `report/00_DOC_TU_DAU` (toàn cảnh + đi-tiếp-được + ưu/nhược) · AndroidControl a11y **đã verify chở được** metric.

---

## MỘT DÒNG
**Hồ sơ này = bộ câu-hỏi-khó + câu-trả-lời-có-bằng-chứng để bạn bảo vệ tự tin: đóng góp rõ (đánh giá + lớp model-agnostic), độ tin đã chứng minh (metric nhạy + ALOHa + chống-vòng-lập-luận + đăng-ký-trước), khả thi đã chạy thật miễn phí, điểm yếu tự nêu kèm cách đỡ, và 6 việc còn phải làm trước khi bảo vệ.**
