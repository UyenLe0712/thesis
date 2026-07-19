# report/82 — Verify tính mới (chống scoop): seam còn trống không?

> Tổng hợp 3 mũi kiểm scoop độc lập cho chỗ-trống mà report/81 tự nhận "MỎNG". Ngày: 2026-07-19.

## Phán quyết 1 dòng

**LẤP MỘT PHẦN — seam CÒN TRỐNG ở tổ hợp trọn gói, nhưng HẸP và có tiền lệ lân cận sát sườn phải phân định (nặng nhất: GUITrans2Act 2026 + CHI 2023 Wang et al.).** Không bài nào phủ đủ bốn thành phần cùng lúc: (i) người đọc là NGƯỜI, (ii) đầu ra = hướng dẫn NHIỀU BƯỚC bám câu hỏi use-case, (iii) đánh giá KÉP (reference-free đối chiếu VH + gold correctness), (iv) VLM NHỎ on-device. Tính mới nằm ở TỔ HỢP + hai điểm hẹp (nguồn-verify-có-cấu-trúc VH thay self-probe; AndroidControl step_instruction làm TARGET SINH), KHÔNG nằm ở riêng "dual eval" hay "small VLM".

## Bài gần nhất + giống/khác luận văn

| Bài | Venue | Peer-reviewed? | Giống gì | Khác gì (điểm phân định) |
|---|---|---|---|---|
| **GUITrans2Act / "Teach VLM"** (arXiv 2606.12817) | arXiv 06/2026 | ❌ preprint | Sinh câu NL mô tả thao tác GUI (loại thao tác, phần tử đích, tham số, thứ tự bước); tự nhận "procedural reference cho người" | Đầu vào = VIDEO demo / chuỗi state, KHÔNG phải 1 ảnh + câu hỏi; dataset tiếng Trung tự dựng (KHÔNG dùng AndroidControl); mục tiêu chính = Teach-and-Repeat cho AGENT thực thi; eval = độ chính xác ngữ nghĩa thao tác + Task Success Rate (KHÔNG có reference-free-VH, KHÔNG tách trung-thực/đúng); không claim ≤4B. **Bài phải phân định số 1.** |
| **Enabling Conversational Interaction with Mobile UI using LLMs** (Wang, Li, Li) | CHI 2023 | ✅ | Dùng LLM đọc UI phục vụ người: screen QA / summarization / question-generation | 4 tác vụ là QA-một-đáp-án / tóm-tắt / sinh-câu-hỏi — KHÔNG có "sinh quy trình nhiều bước để người tự làm"; prompting LLM text-only (không train VLM nhỏ); không faithfulness-vs-VH, không gold-step. **Bài "đã có ai sinh ngôn ngữ cho người từ UI" gần nhất.** |
| **FaithScore** | Findings EMNLP 2024 | ✅ | Reference-free faithfulness: tách atomic facts rồi verify | Verify bằng chính ẢNH qua VQA (self-probe nội mô hình), miền captioning tổng quát; KHÔNG dùng nguồn cấu-trúc-ngoài (VH), KHÔNG có nửa gold. **Đối thủ phân định của nửa reference-free — phân định SẠCH bằng luận điểm VH-ngoài.** |
| **ALOHa** | NAACL 2024 | ✅ | Reference-free hallucination mức đối tượng | Caption ảnh đời-thường, không GUI/VH/gold-pairing. Là TRỤ đo trung thực của ta, không phải đối thủ scoop. |
| **MobileVLM (Xiaomi)** | Findings EMNLP 2024 | ✅ | VLM hiểu UI di động, có XML/VH mỗi màn | Data tiếng Trung (Mobile3M); eval = ACTION accuracy; không sinh hướng dẫn cho người; không faithfulness reference-free. |
| **AndroidControl** (Li et al.) | NeurIPS 2024 D&B | ✅ | Nguồn low/high-level step_instructions | Instruction luôn là ĐẦU VÀO cho action-prediction (LoRA 86.6% low-level), KHÔNG PHẢI output cần SINH. **Bằng chứng mạnh: dùng step_instruction làm TARGET-SINH chưa ai làm.** |
| **Screen2Words** | UIST 2021 | ✅ | Sinh tóm-tắt-màn cho người | 1 câu tóm tắt (không nhiều bước, không theo câu hỏi); eval CHỈ reference-based (BLEU/CIDEr…), không faithfulness reference-free. |
| **Widget Captioning** | EMNLP 2020 | ✅ | Sinh mô tả phần tử UI | Đơn-phần-tử, không quy trình; eval reference-based thuần. |
| **PixelHelp / Seq2Act** | ACL 2020 | ✅ | Miền chỉ dẫn ↔ UI di động | Chiều NGƯỢC: nhận chỉ dẫn SẴN CÓ → ánh xạ sang action; không SINH chỉ dẫn. |
| **HelpViz** | UIST 2021 | ✅ | Sản phẩm cuối = tutorial cho người dùng | Chiều NGƯỢC: đầu vào = text instruction có sẵn → render ảnh/video minh hoạ; không sinh chữ từ ảnh, không đánh giá faithfulness ngôn ngữ. |
| **Describing UI Screenshots in NL** | ACM TIST 2022 | ✅ | Sinh NL mô tả màn app cho người | Captioning mô tả nội dung, không hướng dẫn tác vụ nhiều bước theo câu hỏi. ⚠ chưa đọc full-text (403). |
| HalluClear (2604.17284), Faithful Mobile GUI Agents (2605.01208), VeriOS, AppVLM, UI-R1, OS-Atlas, ShowUI, Aguvis | arXiv 2025–26 / AAAI26 / ICLR25 / CVPR25 | ❌ phần lớn preprint; UI-R1=AAAI26, OS-Atlas=ICLR25, ShowUI=CVPR25 ✅ | VLM nhỏ / GUI-hallucination đang nóng | ĐỀU nhắm AGENT sinh ACTION/grounding cho máy, eval = action-fidelity / success-rate. Chỉ dùng để định vị "tiền lệ đều là action-cho-máy". |

## Tính mới PHÒNG-THỦ-ĐƯỢC vs KHÔNG nên claim

**PHÒNG-THỦ-ĐƯỢC (giữ, đặt làm trục chính):**
1. **Nửa reference-free dùng nguồn NGOÀI CÓ CẤU TRÚC (View Hierarchy) để bắt bịa tên nút, thay vì self-probe từ chính ảnh.** Phân định SẠCH với FaithScore/ALOHa — đây là chỗ mạnh nhất, không ai đụng.
2. **AndroidControl step_instruction làm TARGET SINH (output), không phải input điều-kiện-hoá cho action.** Cả 3 mũi xác nhận chưa thấy ai làm — luận điểm này mạnh và dễ chứng minh (mọi bài dùng AndroidControl đều để instruction ở phía input).
3. **TỔ HỢP 4 thành phần** (người đọc + đa bước + đánh giá kép + VLM nhỏ on-device) — chưa bài nào phủ trọn. Tính mới ở giao điểm, không ở từng mảnh.

**KHÔNG nên claim (sẽ bị đập):**
- ❌ "Đánh giá KÉP reference-free + reference-based là phát kiến." SAI — đây là dòng "hybrid metric" đã có tên (RUBER / BLEURT / BARTScore), được survey 2501.12011 xếp thành loại chuẩn. Chỉ bán như "áp khung hybrid ĐÃ BIẾT vào output-type + nguồn-verify chưa ai ghép trên GUI".
- ❌ "Quy trình sinh hướng dẫn GUI cho người là mới hoàn toàn." Rủi ro bị CHI 2023 (Wang et al.) + GUITrans2Act làm mỏng. Phải phân định, không lờ đi.
- ❌ "VLM nhỏ on-device sinh text-GUI" làm trục chính. Yếu nhất — dễ bị GUITrans2Act/MobileVLM/AppVLM bào mòn. Đẩy xuống thành đặc-tính-triển-khai, KHÔNG phải trục tính-mới.

## Câu chốt nên nói với hội đồng

"Đóng góp không nằm ở việc sinh chữ từ UI (đã có captioning/summarization) hay ở việc ghép hai loại metric (hybrid đã có tên), mà ở chỗ **lần đầu đặt step_instruction do người viết của AndroidControl làm MỤC TIÊU SINH cho hướng dẫn nhiều-bước phục vụ NGƯỜI ĐỌC, rồi đo nó bằng một cặp thước chưa ai ghép trên GUI: trung thực reference-free đối chiếu View Hierarchy (nguồn cấu-trúc-ngoài, không self-probe) song song với đúng-đắn so gold.** Mọi tiền lệ GUI-VLM gần nhất — kể cả bài mới nhất 2026 — đều sinh action/plan cho MÁY tiêu thụ và đo bằng success-rate của agent; không bài nào tách bạch trục 'trung thực' khỏi trục 'đúng' cho văn bản độc lập mà con người tự thao tác theo."

## Rủi ro còn lại + phải hỏi thầy

- **Reviewer sẽ ép phân định với "high-level instruction generation" của agent** (AndroidControl-High, bài sinh sub-goal/plan). Thủ sẵn: đầu ra của họ là plan NỘI BỘ đi kèm action-token, đo bằng success-rate; của ta là văn bản độc lập cho người, đo bằng faithfulness ngôn ngữ. → **Hỏi thầy:** luận cứ phân định này đủ mạnh chưa, hay cần thêm bằng chứng định lượng (ví dụ đo readability/độ-tự-đủ của output cho người)?
- **Công cụ thương mại** (MagicHow, Scribe, DocsBot, ScreenApp) đã làm đúng ứng dụng "screenshot → how-to". Không scoop học thuật (không có phương pháp/đánh giá công bố) nhưng reviewer có thể hỏi "khác gì sản phẩm ngoài thị trường". Thủ: đóng góp = model nhỏ + đánh giá kép có kiểm chứng, không phải tính năng.
- **Trọng tâm framing:** cả 3 mũi khuyên dịch trục tính-mới sang **đánh-giá-kép + AndroidControl-as-generation-target**, KÉO trọng tâm khỏi "on-device small VLM". → **Hỏi thầy** có đồng ý đổi trọng tâm không (vì thầy yêu cầu train-model thật, cần cân đối giữa "đóng góp model" và "đóng góp đánh giá").

## Chỗ chưa tìm hết (trung thực)

1. **Chưa đọc full-text 3 bài gần-nhất/nóng nhất:** GUITrans2Act (2606.12817, PDF lớn — chưa chắc 100% nó có đụng AndroidControl ở phụ lục hay nêu size ≤4B); HalluClear (2604.17284, 47 trang — chưa chắc không có arm eval "mô tả cho người"); Describing UI Screenshots (ACM TIST 2022 — bị chặn 403, chưa verify tác giả). **Phải fetch lại trước khi trích trong related work.**
2. **Chưa quét hệ thống CHI/UIST/MobileHCI/ASE 2024–2026 và workshop** — cộng đồng HCI có thể có bài "đánh giá mô tả/hướng dẫn UI" mà search thiên-arXiv bỏ sót. Nên chạy một vòng ACM DL / Google Scholar cho "UI summarization/instruction faithfulness evaluation 2025".
3. **Chưa quét kiệt venue/paper TIẾNG TRUNG** (MobileVLM, GUITrans2Act đều Trung Quốc — mảng này đông và ra nhanh).
4. **Dòng hybrid-metric gốc** (RUBER/BLEURT/BARTScore) chưa truy từng bài để chắc không có biến thể GUI — nếu hội đồng đào, điểm yếu nằm đây.
5. **Preprint 2026 (2604.*, 2605.*, 2606.*) chưa qua bình duyệt** — KHÔNG xếp ngang trụ peer-reviewed; verify trạng thái venue trước khi trích.

> **✅ CẬP NHẬT 19/7 — đã fetch trực tiếp GUITrans2Act (2606.12817):** KHÔNG scoop. Tên thật *"GUITrans2Act: Understanding User Operational Behaviors from Mobile GUI Interactions with VLMs"* (Zhang et al.). Đầu vào = **VIDEO demo** (không phải 1 ảnh + câu hỏi); mục đích = teach-and-repeat, output làm "procedural reference cho AGENT thực thi downstream"; dataset = **benchmark tiếng Trung tự dựng, KHÔNG dùng AndroidControl**; đánh giá = **Task Success Rate của agent** (Android World), không reference-free-VH. → phân định SẠCH trên 4 trục (input · người-vs-agent · dataset · eval). Đối thủ gần nhất đã được gỡ. Còn HalluClear + TIST2022 chưa fetch.

**Khuyến nghị hành động:** (a) fetch full-text HalluClear + TIST 2022 để chốt phân định (GUITrans2Act đã xong); (b) chạy thêm 1 vòng deep-research hẹp trên "workflow/procedure description generation" ngoài mobile + workshop HCI 2025-26 + "accessibility narration" học thuật; (c) trong paper, đặt trục tính-mới = đánh-giá-kép-VH + AndroidControl-as-target, hạ "on-device small VLM" xuống đặc-tính-triển-khai.