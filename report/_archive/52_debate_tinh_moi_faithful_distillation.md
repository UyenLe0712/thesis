# DEBATE VÒNG 4 (2026-07-09) — KIỂM TRA TÍNH MỚI CỦA "FAITHFUL DISTILLATION"

> Nguồn: workflow `wf_0dda570e-48a` (16 agent: 5 research song song + 5 góc tấn công tính-mới + 5 kiểm chứng đối kháng + 1 tổng hợp). Đây là vòng debate THỨ 4 về hướng model-centric (nối tiếp `report/50` §7–§9). Mục tiêu: trước khi tiêu tiền/thời gian train, kiểm tra xem "Faithful Distillation" có còn tính mới thật sau khi soi bằng deep-research 2024-2026, hay chỉ là recipe cũ khoác áo GUI.

**KẾT LUẬN TỔNG: CÓ-NHƯNG-CẦN-VÁ.** Pipeline sống sót, nhưng tính mới bị thu hẹp đáng kể so với cách report/43 Chương 0 đang trình bày — không được nói "quy trình lọc-faithfulness MỚI", phải dồn trọng tâm về **một câu hỏi thực nghiệm cụ thể có thể ra kết quả null**.

---

## 1. Research: rà quét prior-art (5 mũi song song)

Không tìm thấy paper nào (2024–2026, kể cả quét riêng 2-3 tháng gần nhất) trùng đủ tổ hợp: *sinh hướng dẫn cho NGƯỜI ĐỌC từ ảnh GUI + fine-tune VLM nhỏ + lọc bằng đối chiếu accessibility-tree/VH có cấu trúc + bịa được viết lại thành mô tả chung chung (không xoá, không đoán nút khác) + đánh giá no-gold qua %fallback*.

Precedent gần nhất theo từng trục (đều CHỈ trùng một phần):

| Paper | Trùng gì | Khác gì |
|---|---|---|
| **VGA** (Findings EMNLP 2024, arXiv 2406.14056) | VH làm ground-truth, fine-tune VLM giảm ảo giác cho câu trả lời GUI **cho người đọc** | Ràng buộc **lúc SINH** (Referent Method ép câu trả lời chứa toạ độ/màu từ VH), KHÔNG PHẢI lọc **hậu-kiểm** sau khi sinh mù; không có kiến trúc teacher→filter→student |
| **KnowAda** (NAACL 2025, arXiv 2411.09018) | Lọc/viết-lại caption trước khi fine-tune, CÓ ablation raw-vs-filtered trên cùng base model | Lọc bằng **self-probe VQA của chính model** (circular), không phải đối chiếu nguồn ngoài có cấu trúc; domain caption ảnh tĩnh, rủi ro bịa vô hại (không phải bấm sai nút) |
| **BLIP-CapFilt** (ICML 2022, arXiv 2201.12086) | Sinh + lọc (bootstrapping), CÓ ablation F-only cô lập giá trị bước lọc | Không đo robust-khi-thiếu-nguồn-lọc-lúc-suy-luận; domain caption chung |
| **FaithDial/BEGIN** (Dziri, TACL 2022, arXiv 2204.10757) | Viết lại phát ngôn bịa dựa trên đối chiếu tri thức nền có cấu trúc | Coi "generic/mơ hồ" là **lỗi cần sửa**, KHÔNG PHẢI chiến lược né-bịa có chủ đích như luận văn |
| **WinDOM** (arXiv 2606.25964, 6/2026) · **Trust-the-Right-Teacher** (arXiv 2606.18101, 6/2026) · **LiteGUI** (arXiv 2605.07505, 5/2026) · **CORA** (arXiv 2604.09155) | Lọc/self-distill xuống model nhỏ on-device cho GUI, có khái niệm "quality-aware"/né-bịa | Verify bằng **hình học liên tục** (click-in-bbox) cho **agent bấm-máy**, recovery chỉ nhị phân execute/abstain — khác họ bài toán với verify **ngữ-nghĩa-cấu-trúc** (tên nút so với VH) cho văn bản tự do người-đọc |
| **AskEase** (CHI 2026, arXiv 2601.18092) | Đúng bài toán: hướng dẫn từng bước cho người dùng khi thao tác máy tính | KHÔNG train/fine-tune model — dùng LLM lúc suy luận (prompting), đúng thứ thầy đã bác |

**STaR/RFT/ReST** (Zelikman 2022, arXiv 2203.14465) — meta-pattern "generate → filter → retrain" đã 4 năm tuổi, không riêng GUI, phải thừa nhận đây là khung sườn đã có tên.

---

## 2. Debate: 5 góc tấn công + kiểm chứng đối kháng

| # | Góc tấn công | Verdict giám khảo | Kết quả kiểm chứng |
|---|---|---|---|
| 1 | **Domain-repackaging** — chỉ là STaR+KnowAda+VGA ghép lại | novelty at risk | **Đứng vững** — mọi trích dẫn/cơ chế đều verify đúng, không bịa |
| 2 | **Ablation-triviality** — raw-vs-filtered là sanity-check tầm thường | novelty at risk | **Đứng vững** — 2/7 precedent (KnowAda, CapFilt) đã làm đúng dạng này, và ở CẢ HAI chỉ là bảng phụ hỗ trợ, chưa từng là trụ đóng góp chính |
| 3 | **Structural-filter-novelty** — lọc bằng ground-truth có cấu trúc không đặc biệt | novelty at risk | **Đứng vững** (2 trích dẫn scene-graph bị đánh giá là suy diễn quá, nên loại; nhưng FaithDial/KnowAda/CapFilt đủ để giữ đòn tấn công) |
| 4 | **Human-facing-framing** — "người đọc vs agent" chỉ là đổi nhãn | novelty at risk (ban đầu) | **KHÔNG đứng vững** — trụ cột chính của đòn này trích dẫn SAI/BỊA một tiêu chí không có thật từ arXiv 2508.10795; sau khi loại phần bịa, các precedent GUI-agent 2026 (WinDOM/Trust-the-Right-Teacher/LiteGUI/CORA) thực ra CỦNG CỐ ranh giới người-đọc/agent chứ không xoá nó |
| 5 | **Eval-recycling** — thước đo no-gold cũ không bù được cho model thiếu mới | novelty at risk | **Đứng vững, nhưng bị thu hẹp rõ** — còn sống đúng 2 điểm: (a) bộ lọc đối chiếu CÓ CẤU TRÚC qua VH (khác similarity-văn-bản của KnowAda), (b) phép đo robust-khi-tắt-hậu-kiểm (vô nghĩa với hệ prompting cũ, có ý nghĩa thật với model đã train) |

**4/5 đòn đứng vững** (cần vá framing, không phải vá cơ chế) — **1/5 tự sụp vì trích dẫn bịa** (đúng loại lỗi dự án từng cảnh giác, ví dụ vụ đọc nhầm teacher/student ở VLsI trước đây — quy trình kiểm chứng đối kháng đã bắt được).

---

## 3. Câu tuyên bố tính mới (dùng khi trình thầy)

> "Chúng tôi không phát minh ra công thức 'sinh rồi lọc rồi distill' — công thức đó đã có ở STaR, BLIP-CapFilt, KnowAda; và việc dùng accessibility-tree để giảm ảo giác khi fine-tune VLM cho GUI cũng đã có ở VGA. Đóng góp thực nghiệm của luận văn là trả lời một câu hỏi mà không ai trong các tiền lệ đó đặt ra: khi bộ lọc dùng một NGUỒN XÁC NHẬN BÊN NGOÀI, có cấu trúc, không tự-quy-chiếu (View Hierarchy, không phải model tự probe chính nó như KnowAda) để ràng buộc một hành vi có RỦI RO CAO (bịa tên nút khiến người dùng thao tác sai, không phải bịa chi tiết caption vô hại), thì tín hiệu 'né bịa' đó có SỐNG SÓT khi bị NÉN xuống một model 3B chạy on-device, và quan trọng nhất — có được NỘI TẠI HOÁ đủ để tự phát huy tác dụng ngay cả khi, tại thời điểm suy luận, không còn accessibility-tree nào để dựa vào nữa hay không? Đây là câu hỏi có thể ra kết quả ÂM (null), nên nó là một giả thuyết kiểm chứng được, chứ không phải một bước lắp ráp công cụ đã biết trước kết quả."

---

## 4. Việc PHẢI SỬA trong report/43 / slide / CLAUDE.md

1. **Xoá mọi cụm "quy trình lọc-faithfulness MỚI"** → đổi thành "thích-nghi có chủ đích của filter-then-distill (họ STaR) cho actionable-GUI on-device".
2. **Không neo đóng góp vào SỰ TỒN TẠI của ablation raw-vs-filtered** — hạ xuống vai trò điều-kiện-cần/robustness-check. **Headline chuyển thành trụ #1 = robust-khi-tắt-VH lúc suy luận** (held-out theo app) — thí nghiệm này phải là trụ cột số một, không phải mục phụ, vì đây là chỗ có thể null thật.
3. **Reframe việc tái dùng thước đo cũ (nomic/bge-m3/judge/%fallback) thành ĐIỂM MẠNH**: pre-register TRƯỚC khi có ý tưởng train model → chống p-hacking/look-elsewhere.
4. **Bổ sung related-work bắt buộc:** STaR/RFT (Zelikman 2022, arXiv 2203.14465), FaithDial/BEGIN (Dziri, TACL 2022, arXiv 2204.10757), WinDOM (arXiv 2606.25964), Trust-the-Right-Teacher (arXiv 2606.18101), LiteGUI (arXiv 2605.07505), CORA (arXiv 2604.09155) — kèm câu phân định (bảng ở §1 trên).
5. **KHÔNG dùng** bất kỳ khung "Application-vs-Modeling theo arXiv 2508.10795" nếu sau này có ai đề xuất — đã verify đây là trích dẫn bịa cho một paper có thật nhưng không nói vậy.
6. **Pre-register rõ:** câu hỏi robust-khi-không-VH có thể null; nếu null → báo trung thực là "tín hiệu lọc chưa nội-tại-hoá được ở scale 3B" (vẫn là phát hiện có giá trị, không phải thất bại phải giấu).

---

## 5. Mức tự tin & rủi ro lớn nhất còn lại

**Tự tin: trung bình.** Quy trình kiểm-chứng-đối-kháng hoạt động đúng (bắt được 1 trích dẫn bịa trong 5 đòn), nhưng cho thấy ranh giới giữa "tấn công thật" và "tấn công thuyết phục nhưng dựa trên nguồn bịa" khá mong manh — mọi citation đưa vào bản chính thức phải verify lại, không tin bất kỳ agent nào ở lượt đầu.

**Rủi ro lớn nhất:** toàn bộ tính mới đã dồn về **một** phép đo duy nhất (faithfulness của student khi tắt hoàn toàn VH lúc suy luận, held-out theo app). Nếu ra null (model 3B không đủ để nội-tại-hoá hành vi né-bịa, chỉ học pattern bề mặt của tập train) → tụt về đúng phê bình ban đầu của thầy ("chỉ lắp ráp công cụ có sẵn"). Do đó thí nghiệm này cần cỡ mẫu đủ lớn + ngưỡng đậu/rớt pre-register rõ ràng TRƯỚC khi chạy pilot.

*(Toàn bộ transcript research + debate + verify chi tiết: journal của workflow `wf_0dda570e-48a`, có thể trích thêm nếu cần khi viết luận văn chính thức.)*
