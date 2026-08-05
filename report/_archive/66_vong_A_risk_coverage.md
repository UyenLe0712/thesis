# report/66 — Vòng A: Thước đo risk-coverage/AURC (kết quả deep-research)

> Kiểm tra xem có nên đổi/bổ sung headline từ cặp số rời (tỉ-lệ-bịa + %fallback) sang một đường risk-coverage duy nhất (AURC/AUARC), và nếu có thì trình bày/ước lượng cho chặt thế nào. Ngày: ___

**Lưu ý đọc trước — về độ tin của Vòng này:** phần *bằng chứng nội dung* dưới đây dựa trên **toàn văn hai bài đã fetch trực tiếp** (CAP bản PMLR + arXiv HTML; SafeGround arXiv HTML) — đây là nguồn gốc, không phải trí nhớ. Riêng **bước verify đối kháng của harness lần này trả về dữ liệu placeholder** (các claim "c1", "test claim", nguồn "s1"/"test source" — verdict UNVERIFIABLE vì không có nội dung thật để đối chiếu). Kết quả phụ duy nhất hợp lệ từ bước verify: **citation SelectiveNet = ICML 2019 được xác nhận đúng venue** (Geifman & El-Yaniv, PMLR 97:2151–2159). Vì vậy các kết luận dưới đây neo vào **hai nguồn đã đọc tận văn bản**, không neo vào bảng verdict.

---

## Trả lời thẳng 3 câu hỏi (A1/A2/A3)

**A1 — Proxy-risk (đo "risk" bằng matcher tự động, không có gold) có tiền lệ trong hai trụ này không?**
KHÔNG. Cả CAP lẫn SafeGround đều đo risk **bằng gold**. CAP dùng trắc nghiệm đóng (mỗi câu chuẩn hoá về 4–6 lựa chọn, gồm "I don't know"/"None of the above"), đúng/sai là exact-match vào đáp án chuẩn Yₜ. SafeGround dùng bbox tay của ScreenSpot-Pro, "đúng ⟺ toạ độ rơi vào vùng ground-truth B\*". Không bài nào thay risk-thật bằng matcher proxy. Đây là **khoảng trống** của thiết kế luận văn (sinh mở, không gold), phải tự thủ chứ không mượn được.

**A2 — AUARC / đường risk-coverage làm headline có trụ peer-reviewed không?**
CÓ, một phần. **CAP (ACML 2025, PMLR v304, tr. 926–941 — peer-reviewed)** dùng AUARC làm số headline và báo song song *đường cong + số vô hướng tại coverage cố định 90%* (CAP giữ đúng 90% coverage, AUARC +21.2%, AUROC-hallucination +22.2%, giảm calibration error >70% so với CP tĩnh). Nhưng lưu ý chiều trục: CAP vẽ **accuracy-rejection** (Y = accuracy trên phần giữ lại, càng cao càng tốt), ngược chiều với **risk-coverage** (Y = tỉ lệ bịa, càng thấp càng tốt) mà luận văn định dùng — hai đường là biến thể của nhau nhưng phải khai đúng, và CAP **không cho công thức tích phân AUARC tường minh** (chỉ mô tả định tính, dẫn về prior-art accuracy-rejection curve). SafeGround (preprint) hậu thuẫn ý "một trục + kiểm soát ngưỡng bằng thống kê" nhưng không dùng AUARC.

**A3 — Ước lượng/trình bày cho chặt thế nào (calibration set riêng, finite-sample bound, held-out theo app)?**
Có mẫu-hình để mô phỏng, nhưng **không dùng lại nguyên xi được** vì ràng buộc 12-app-held-out. CAP tách calibration set theo chuẩn conformal (D_cal riêng, ngưỡng q̂ = phân vị 1−α) nhưng **không nêu tỉ lệ split cụ thể**. SafeGround (preprint) cho khung chặt hơn: **Learn-Then-Test + cận Clopper–Pearson finite-sample** để chọn ngưỡng, đảm bảo Pr(FDR ≤ α) ≥ 1−δ (δ=0.05); nhưng họ **split ngẫu nhiên theo mẫu (20/80, lặp 100 lần)**, giả định i.i.d. Với luận văn: cận Clopper–Pearson sẽ **không còn chặt** vì (a) risk là proxy, không phải risk-thật; (b) held-out theo app + chỉ 12 app → mẫu calibration nhỏ và tương quan cụm-theo-app phá giả định i.i.d. Cần cluster-aware hoặc khai thẳng giới hạn.

---

## Cổng dừng A1 (proxy-risk có tiền lệ không)

**KẾT QUẢ: KHÔNG ĐẠT** cho phần cốt lõi — không tìm được tiền lệ (trong hai trụ đã chọn) dùng **matcher tự động làm thước đo risk** trong khung selective-prediction/risk-coverage. Cả hai đều có gold rời rạc (đáp án trắc nghiệm hoặc bbox tay).

**Hệ quả cho quyết định đổi thước đo:**
- Không thể trình đường risk-coverage của luận văn như thể "cùng loại AUARC của CAP". Nếu đổi headline, phải khai **rõ ràng và ngay tại chỗ**: "risk ở đây = **proxy** đối-chiếu-VH, không phải hallucination-thật; đường cong này kiểm soát **proxy-risk**". Đây chính là chỗ tiến sĩ AI sẽ vặn, và hiện **chưa có trụ peer-reviewed nào cho phép mượn để chống đỡ**.
- SafeGround gần miền GUI nhất nhưng là **preprint (arXiv:2602.02419, chưa bình duyệt)** và vẫn dùng gold → chỉ dùng làm *related-work định vị*, KHÔNG dùng làm trụ phương pháp.
- Vì cổng A1 không đạt, **không nên đổi hẳn headline trong mùa này**. Cặp số rời đã pre-register (report/56) vẫn là phương án phòng thủ tốt hơn về mặt "có gì trích được".

---

## Bảng claim sống / bị bác

Chỉ giữ claim có nguồn đã đọc tận văn bản làm căn cứ. (Bước verify harness lần này chạy trên dữ liệu placeholder → không có verdict SUPPORTED/PARTIAL/REFUTED thực chất nào để đưa vào; các dòng dưới đánh dấu **PRIMARY-FETCH** = xác nhận trực tiếp từ toàn văn, chưa qua verify đối kháng độc lập.)

| Claim | Nguồn | Verdict | Ghi chú |
|---|---|---|---|
| CAP dùng AUARC làm headline + báo song song đường cong và số tại coverage cố định 90% | CAP, ACML 2025, PMLR v304 (peer-reviewed) | PRIMARY-FETCH | Trục là accuracy-rejection (ngược chiều risk-coverage); không có công thức tích phân AUARC tường minh |
| CAP đo correctness bằng GOLD trên trắc nghiệm đóng 4–6 lựa chọn; không dùng proxy | CAP, ACML 2025 (peer-reviewed) | PRIMARY-FETCH | Khác biệt cốt lõi với luận văn (không gold) |
| CAP tách calibration set theo chuẩn conformal (q̂ = phân vị 1−α), không nêu tỉ lệ split | CAP, ACML 2025 (peer-reviewed) | PRIMARY-FETCH | Có bảo đảm "Policy-Calibrated Coverage" |
| SafeGround dùng Learn-Then-Test + Clopper–Pearson để chọn ngưỡng, đảm bảo Pr(FDR≤α)≥1−δ | SafeGround, arXiv:2602.02419 (**PREPRINT**) | PRIMARY-FETCH | Split ngẫu nhiên theo mẫu 20/80 ×100 lần, giả định i.i.d.; KHÔNG split theo app |
| SafeGround đo correctness bằng GOLD (bbox tay ScreenSpot-Pro), không proxy | SafeGround, arXiv:2602.02419 (**PREPRINT**) | PRIMARY-FETCH | Selective = defer sang model mạnh hơn, không phải fallback-thành-mô-tả |
| SelectiveNet = ICML 2019 (Geifman & El-Yaniv, PMLR 97) | SelectiveNet, ICML 2019 | VERIFIED (citation) | Xác nhận venue đúng; nội dung claim gắn kèm là placeholder nên không kiểm được ý |

**Claim bị bác (REFUTED):** không có. **Placeholder/UNVERIFIABLE (loại khỏi căn cứ):** "c1"/s1, "test claim"/"test source 2024" — dữ liệu test của pipeline, không mang nội dung.

---

## Khuyến nghị cho luận văn

**(1) Giữ cặp số rời đúng pre-reg (report/56) + THÊM đường risk-coverage làm biểu đồ PHỤ.** — *Rẻ nhất, an toàn nhất.*
Không đụng pre-registration, không phải tính lại MDE, không lùi lịch. Cặp (tỉ-lệ-bịa, %fallback) vẫn là headline; đường risk-coverage vẽ thêm để *minh hoạ* sự đánh đổi và chặn đòn "ăn gian bằng fallback nhiều" (đường cho thấy toàn hình dạng trade-off, không chỉ một điểm). Khai rõ đây là **proxy-risk-coverage**, dẫn CAP (peer-reviewed) như tiền lệ *về cách trình bày* đường cong, và nói thẳng khác biệt (CAP có gold, ta dùng proxy). Đây là phương án khớp với kết quả cổng A1 KHÔNG ĐẠT.

**(2) Đổi hẳn headline sang AURC/AUARC.** — *Đắt và rủi ro nhất, KHÔNG khuyến nghị cho mùa này.*
Chi phí: sửa lại pre-registration (report/56) → mất tính "khoá trước khi nhìn kết quả"; **tính lại MDE** cho thống kê mới (AURC là summary một-chiều, phân phối lại mẫu/độ mạnh khác hẳn cặp số rời — ô `[MDE = ___ pp]` đang chờ điền sẽ phải làm lại theo estimand mới); phải nghĩ lại calibration set dưới ràng buộc 12-app; và **thiếu trụ peer-reviewed cho proxy-risk** (cổng A1) nên dễ bị vặn ngay ở headline. Với deadline FAIR 15/8 thì đây là nước cờ tải nặng.

**(3) Để sau 15/8 (bài mở rộng).** — Nếu muốn làm nghiêm phần selective-prediction (LTT + cận finite-sample cluster-aware, có thể thêm một mảng gold nhỏ để hiệu chỉnh proxy), để dành cho bài tiếng Anh mở rộng, không nhồi vào mùa này.

**Chốt gợi ý:** đi **phương án (1)**. Nó lấy được lợi ích trình bày của đường cong mà không trả bất kỳ chi phí pre-reg/MDE/lịch nào, và không vượt quá cái mà cổng A1 cho phép trích. **Quyết định cuối là của user, và nên hỏi thầy** — đặc biệt câu "thầy có muốn headline là một-số-tổng-hợp (AURC) hay cặp-số-minh-bạch" vì đây là lựa chọn khẩu vị đánh giá, không thuần kỹ thuật.

---

## Việc phải tự làm (không có tiền lệ để trích)

1. **Chính đáng-hoá proxy-risk.** Không trụ nào (CAP/SafeGround đều gold) cho phép mượn. Phải tự viết luận cứ + giới hạn: đường cong kiểm soát **proxy-risk từ matcher đối-chiếu-VH**, không phải hallucination-thật; nêu độ-phủ-nhãn VH như trần của proxy.
2. **Công thức AURC/AUARC tường minh.** CAP không cho tích phân → nếu báo AURC phải trích **nguồn gốc** accuracy-rejection curve (Nadeem et al.) và tự viết công thức, không trích CAP cho phần công thức.
3. **Calibration/ngưỡng dưới ràng buộc 12-app.** CAP split conformal không nêu tỉ lệ; SafeGround split ngẫu nhiên i.i.d. Cả hai không hợp held-out-theo-app. Phải tự thiết kế: chia calibration theo app, và làm rõ ngưỡng abstain của ta = **τ matcher**, KHÔNG phải quantile conformal.
4. **Cận thống kê cluster-aware.** Clopper–Pearson của SafeGround giả định i.i.d.; với cụm-theo-app + n nhỏ, cận không còn chặt. Cần bản cluster-aware hoặc khai thẳng giới hạn (nối với cluster-bootstrap theo app đã dùng ở report/54).
5. **Tính lại MDE nếu (và chỉ nếu) đổi estimand.** Ô `[MDE = ___ pp]` ở report/56 tính cho cặp số rời; AURC là estimand khác → nếu chọn phương án (2)/(3) phải làm pilot MDE mới.
