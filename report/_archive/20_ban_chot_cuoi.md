# ✅ BẢN CHỐT CUỐI — PIPELINE · METRIC · THÍ NGHIỆM · CẦN CHUẨN BỊ GÌ

> **File này = "tóm lại là sao".** Gọn, dễ hiểu, hành động được. Chi tiết: thiết kế `14`, metric `18`, kế hoạch `05`, giải thích từ-số-0 `19`.
> **Cập nhật:** 2026-06-27.

---

## A. PIPELINE CHỐT (design E) — "lớp làm-cho-trung-thực"

```
ẢNH + CÂU HỎI
   │  (nhiều ảnh → Bước 0: tự xếp thứ tự màn)
   ▼
① BỘ VIẾT = model mạnh, THAY ĐƯỢC → viết hướng dẫn GỌI NÚT THEO TÊN
   ▼
② ORACLE (danh sách nút thật = cây accessibility) đặt BÊN CẠNH: "nút này có thật? ở đâu?"
   ▼
③ Sai → SỬA (một model khác chọn lại nút thật) → vẫn không có → FALLBACK mô tả bằng lời
   ▼
HƯỚNG DẪN cuối  (oracle chỉ dùng lúc CHẤM, không vào lúc viết)
```

- **Bộ viết:** **Qwen mở** (lõi, miễn phí) + **GPT-5/Gemini-3** (chạy ít, đối chứng). **KHÔNG fine-tune.**
- **Oracle** = cây accessibility của Android (chuẩn ngành, app thật đọc được). Chỉ đảm bảo "nút tồn tại".
- **Đối chứng:** thêm nhánh **Set-of-Mark cũ** + nhánh **Qwen ground toạ độ thẳng** để so "có cần detector không".

---

## B. METRIC CHỐT

### Một màn (DG1)
| Thước đo | Đo gì | Cần đáp-án-vàng? | Trạng thái |
|---|---|---|---|
| **Bịa (Faithfulness)** | nhắc nút không tồn tại? (ALOHa, đồng-nghĩa-OK) | không | ✅ đã chạy |
| **Đúng-nhãn (Clarity)** | gọi đúng TÊN hiển thị? (synonym trừ clarity, ko tính bịa) | không | ✅ đã chạy |
| **Đúng chỗ (Grounding)** | bấm trúng khung nút? | không | ✅ đã chạy |
| **Đủ ý (Coverage)** | bỏ sót nút cần? | **có** | ⏳ Colab |
| **Định dạng (Format)** | đánh số/động từ/1-việc? | không | ⏳ |

### Nhiều màn (DG2) — trên AndroidControl
| Thước đo | Đo gì | Trạng thái |
|---|---|---|
| **Xếp thứ tự (Kendall τ-b)** | xếp N màn xáo trộn đúng tới đâu? (chỉ phạt cặp bắt buộc) | ⏳ Colab |
| **Làm-theo-tới-đích (Step-SR)** ⭐ | làm theo có tới đích không? (bằng chứng mạnh nhất) | ⏳ Colab |
| **Action-Type (Tier A)** | đúng loại thao tác? | ⏳ Colab |

### Kiểm cách-chấm-có-đáng-tin
| **Track B** | người chấm ~60–80 mục → xem điểm máy có giống người (tương quan + Krippendorff α) | ⏳ |

> Quy ước: **cao = tốt.** Luôn báo **cặp [Bịa, Coverage]** cùng nhau (chống mẹo "viết ít cho khỏi sai").

---

## C. THÍ NGHIỆM CHỐT CHẠY

Mỗi thí nghiệm: **Hỏi gì → Chạy sao → Trạng thái.**

| TN | Hỏi gì | Chạy sao | Trạng thái |
|---|---|---|---|
| **TN0 — Smoke DG1** | hệ + bộ chấm chạy được không? | ~10 màn MobileViews, model nhỏ, CPU | ✅ **XONG** (free) |
| **TN1 — A/B hiệu quả** ⭐ | hệ design E có tốt hơn "viết tự do"? | so BASE vs +design E trên cùng màn → faithfulness/đúng-nhãn | ✅ **XONG** (66.7%→100%, 59.3%→92.6%) |
| **TN2 — Ablation** | cơ chế nào trả công? | L0(tự do) → L1(+oracle+fallback) → L2(+sửa) + nhánh SoM + nhánh native-grounding | ⏳ Colab |
| **TN3 — So model** | model mạnh hơn có tốt hơn? hệ giúp trên MỌI model? | chạy hệ trên Qwen + 1 chút GPT-5/Gemini-3 → so delta | ⏳ Colab (cần API) |
| **TN4 — DG2 trên AndroidControl** ⭐ | xếp đúng thứ tự + làm-theo-tới-đích? | lọc episode → đo **τ-b** + **Step-SR** + baseline (GOAL-ONLY/VISUAL-ONLY/RANDOM) | ⏳ Colab |
| **TN5 — Track B** | điểm máy có giống người? | người chấm so-đôi ~60–80 mục → tương quan | ⏳ |

> **Nguyên tắc vàng (chống tốn tiền):** **ĐĂNG KÝ TRƯỚC** giả thuyết + ngưỡng + cách quyết định TRƯỚC khi chạy TN2–TN5 → **chạy Colab MỘT LẦN**, không chạy-đi-chạy-lại. Kết quả null vẫn là đóng góp.

---

## D. CẦN CHUẨN BỊ GÌ (checklist)

**Đã có sẵn:**
- ✅ Code harness nền (`harness/`: chấm Bịa/Đúng-nhãn/Grounding + ALOHa + A/B).
- ✅ Ollama + Qwen (chạy CPU free) cho thử nghiệm nhỏ.
- ✅ Thiết kế + metric đã chốt (file này + `14`/`18`/`05`).

**Cần chuẩn bị để chạy lớn (Colab):**
1. **Thuê GPU Colab** (~$10–50 là đủ cho luận văn quy mô nhỏ; có thể dùng Colab free/Pro).
2. **Tải AndroidControl** (TFRecord trên Google Cloud) + **viết code parse cây accessibility** (proto `android_env`, ~30–50 dòng — đã verify khả thi).
3. **Soạn câu hỏi use-case cho MobileViews** (~vài trăm câu "làm sao để X", X làm-được-trên-màn; có người duyệt). *(AndroidControl/ScreenSpot có sẵn, không cần.)*
4. **Mở rộng harness:** thêm coverage (trên gold) + τ-b (Fagin) + Step-SR + lọc episode. *(Nền đã có, chỉ thêm.)*
5. **Bảng PRE-REGISTRATION** (1 trang): liệt giả thuyết bác-được + ngưỡng + quy tắc quyết định cho TN2–TN5.
6. **Người chấm Track B** (2–3 người, ~60–80 mục).
7. *(Tùy chọn)* **API key GPT-5/Gemini-3** cho TN3 (~$5–20).

---

## E. THỨ TỰ LÀM
1. **Soạn câu hỏi MobileViews** + **bảng pre-registration** (free, làm trước).
2. **Tải AndroidControl + parse a11y + mở rộng harness** (free/Colab nhẹ).
3. **Chạy TN2–TN4 trên Colab MỘT LẦN** (sau khi pre-register).
4. **TN5 người chấm** song song.
5. Viết bảng kết quả → luận văn.

> **Đang ở đâu:** TN0 + TN1 **đã xong miễn phí** (chứng minh hệ chạy + hiệu quả về độ-trung-thực). Còn lại (coverage/τ-b/Step-SR/Track B + quy mô) = **một đợt Colab có chuẩn bị**.

---

## MỘT DÒNG
**Pipeline = lớp-trung-thực-hoá (sinh-theo-tên → oracle-bên-cạnh → sửa/fallback, model thay được, không fine-tune); metric = Bịa(ALOHa)/Đúng-nhãn/Coverage/Grounding/Format + τ-b/Step-SR + Track B; thí nghiệm = A/B hiệu quả (ĐÃ XONG free) + ablation + so-model + DG2 + người-chấm (CHỜ Colab); chuẩn bị = câu hỏi MobileViews + parse AndroidControl + mở rộng harness + pre-registration + người chấm, rồi chạy Colab MỘT LẦN.**
