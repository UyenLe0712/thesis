# CHANGELOG — Review đối kháng Đợt 1 (metrics + datasets)

> ⚠️ **DISCLAIMER:** File này ghi lịch sử review TRƯỚC đợt rescope (đổi sang screen-ordering); một số mục phản ánh scope CŨ, giữ làm dấu vết lịch sử.

> Ghi lại thay đổi sau **vòng review thứ 2** (4 reviewer + tầng verify độc lập từng lỗi bằng web).
> Mục đích: minh bạch đã sửa gì, và **đã cố tình GIỮ nguyên gì** (vì verify bác đề xuất sửa) — để bảo vệ trước thầy.

## Thống kê
- Vòng 1 (nghiên cứu): 10 agent, ~152 web search → tạo bản nháp.
- Vòng 2 (review): 15 agent, ~189 web search → 39 findings, verify độc lập các lỗi factual/citation high/medium.

---

## A. ĐÃ SỬA (verify xác nhận đúng)

| # | Vị trí | Lỗi | Sửa thành | Mức |
|---|---|---|---|---|
| 1 | 01, CLAUDE, thesis_context | Chim et al. ghi "ACL 2025" | **Computational Linguistics 51(1):191–233, MIT Press, 2025** (journal, không phải hội nghị) | 🔴 cao |
| 2 | 02, CLAUDE | "MobileViews BỊA metric" | **Nhầm phiên bản:** metric có thật ở **v1**; v3 đổi sang RL grounding ScreenSpot-v2/Pro → đính chính thành "ghi rõ phiên bản" | 🔴 cao |
| 3 | 01 §4 | Task Success bị trình bày như reference-free | Thêm **callout**: đây là chiều DUY NHẤT cần gold trajectory; nêu 2 lối đi (gold từ traces / proxy reachability) | 🟠 cao |
| 4 | 01 §1.2 | ScreenSpot-Pro "(ICLR 2025)" mâu thuẫn niên đại | "(preprint)" | 🟠 cao |
| 5 | 01 (toàn cục) | Không phân biệt màn-thấy vs màn-suy-luận | Thêm **caveat toàn cục** + chính sách chấm tách 2 loại bước | 🟠 cao |
| 6 | 01 §1 | Grounding giả định model xuất tọa độ | Thêm **bước text→element resolution** + Element-match Acc | 🟠 cao |
| 7 | 01 §2 | 11 metric hallucination đếm trùng | Chọn **1 metric tồn-tại chính**, còn lại triangulate; **quy ước hướng điểm** thống nhất | 🟡 vừa |
| 8 | 01 §2 | Thiếu coverage + faithfulness VLM | Thêm **FaithScore** + **coverage/VALOR-EVAL** | 🟡 vừa |
| 9 | 01 §2.7 | FactCC dựng riêng (tốn + circular) | Hạ xuống **learned baseline** trong track HaluEval-UI | 🟡 vừa |
| 10 | 01 §2.4/2.5 | Ví dụ claim FActScore/SAFE là loại chuyển-màn | Giới hạn ví dụ vào **claim một-màn** | 🟡 vừa |
| 11 | 01 §3.4 | Flesch/FKGL làm metric clarity; vô nghĩa cho tiếng Việt | Hạ xuống **thống kê mô tả** + cảnh báo tiếng Việt | 🟡 vừa |
| 12 | 01 §3.2 | G-Eval 0.514 trình bày như bảo chứng | Ghi rõ **SummEval-specific**; mở rộng caveat LLM-judge shared-error | 🟡 vừa |
| 13 | 01 §0 | Ánh xạ Chim→4 tiêu chí chỉ khẳng định | Thêm **bảng mapping** + tái diễn giải trục **Divergence** (§3.5) | 🟠 cao |
| 14 | 01 §B.3 | Chỉ dùng Spearman | Thêm **Kendall τ-b + bootstrap CI** | 🟡 vừa |
| 15 | 01 (cuối) | Lẫn "citation real" vs "metric đáng tin" | Tách rõ 2 nghĩa "High" | 🟡 vừa |
| 16 | 02 | ~9× screen / ~2× app so Rico | **~19× / ~3×** (full-paper; ~9.5× nếu tính bản HF) | 🟡 vừa |
| 17 | 02 bảng | Ô quy mô lẫn paper vs HF | Ghi rõ **Paper 1.21M/30K** vs **HF ~600K/20K** | 🟢 thấp |
| 18 | 02 | "khác WebArena" không trích | Gloss + cite (Zhou et al. 2023) / "online execution success" | 🟢 thấp |
| 19 | 02 khuyến nghị | Bullet 2 oversell "đã giải quyết suy luận" | Hedge: next-screen VH là **anchor**, không phải test-of-inference; đồng bộ với 01 | 🔴 cao |
| 20 | 02 khuyến nghị | Lẫn "động cơ tiếng Việt" với "dữ liệu" (MobileViews EN+ZH) | Tách bạch deployment target vs dữ liệu chấm; **làm mềm con số ~120** | 🟡 vừa |
| 21 | 02 | Mâu thuẫn metric (cần gold) ↔ dataset chính (không gold) | Thêm đoạn **hoà giải**: tính Task Success trên traces bằng AITW-style matching | 🟡 vừa |

---

## B. CỐ TÌNH GIỮ NGUYÊN (verify BÁC đề xuất sửa của reviewer)

| Vị trí | Reviewer đề xuất | Vì sao GIỮ |
|---|---|---|
| 01 §4.3 AndroidControl | Đổi attribution Type/GR/SR về AndroidControl | **Bản gốc đúng:** decomposition + ngưỡng 14% là protocol **OS-Atlas**; AndroidControl native chỉ có step-wise/episode accuracy. Verify 2 nguồn xác nhận. |
| 02 Mind2Web | Bỏ/nghi ngờ số "~580 sau cleaning" | Số **~580 có thật trong paper** (1.135→580, recall 94.7%). Giữ. |
| 02 Mind2Web | "không có bbox pixel" hơi tuyệt đối | Đúng theo nghĩa task/anchor; bản Multimodal có bbox **DOM-derived** (đã thêm footnote ¹), không đổi luận điểm. |

---

## C. Bài học rút ra (đáng nói với thầy)
- **Citation phải verify tận nguồn** — riêng vòng đầu đã có lỗi venue (Chim) và **kết luận "bịa" do đọc nhầm phiên bản** paper. Web search 1 lần chưa đủ; cần đối kháng + phân biệt phiên bản.
- **Reference-free có ngoại lệ:** Task Success không thể reference-free thuần — phải khai báo rõ nguồn gold hoặc hạ xuống proxy.
- **Ràng buộc "1 ảnh"** chi phối toàn bộ chấm điểm: phải tách màn-thấy vs màn-suy-luận ở MỌI metric.
