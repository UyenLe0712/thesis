# 📘 ĐỌC FILE NÀY TRƯỚC — TOÀN BỘ ĐỀ TÀI + ĐÃ LÀM GÌ + KẾT QUẢ (cho người chưa biết gì)

> **Chỉ cần đọc file này là nắm hết:** đề tài là gì · đã làm những gì từ đầu tới giờ · thiết kế cuối · cách chấm điểm · **kết quả chạy thử thật** · đi tiếp được không · còn phải làm gì. Mọi từ chuyên môn giải thích ngay tại chỗ. Muốn đào sâu phần nào thì xem file kỹ thuật (có bản đồ ở cuối).
> **Cập nhật:** 2026-06-25.

---

## 1. ĐỀ TÀI LÀ GÌ (3 câu)
- **Vào:** một (hoặc nhiều) **ảnh chụp màn hình** app + một **câu hỏi** (vd *"muốn kiểm tra đã nộp thuế chưa thì bấm đâu?"*).
- **Ra:** **hướng dẫn bấm từng bước** cho người đọc.
- **Cái khó:** **không có "bài mẫu chuẩn" do người soạn** để máy bắt chước → phải tự nghĩ ra **cách chấm điểm** xem hướng dẫn đúng/tốt không.

**Hai đóng góp (ngang nhau):** **(A)** một **hệ viết hướng dẫn bám sát ảnh** (ít bịa, đúng nút, dễ làm theo); **(B)** một **cách đánh giá đáng tin khi không có bài mẫu**.

---

## 2. ĐÃ LÀM NHỮNG GÌ (nhật ký dễ hiểu)

1. **Rà lại pipeline + cách chấm từ đầu** (nhiều "trợ lý AI" tìm song song). Phát hiện thiết kế cũ (bắt một *bộ dò nút* chạy TRƯỚC rồi ép model chỉ nhắc nút bộ dò thấy) **dễ lỗi** — sót nút thì hướng dẫn thiếu.
2. **Cập nhật kiến thức 2026** (đã có GPT-5, Gemini-3). Kết luận từ bài bình duyệt: **model mạnh nhất 2026 VẪN bịa nút, vẫn sai vị trí** → còn chỗ cho một "lớp làm-cho-trung-thực".
3. **Chốt thiết kế cuối "design E"** (mục 3) + các quyết định (mục 8).
4. **Chạy thử THẬT trên máy — miễn phí, không cần GPU** (dùng Ollama chạy CPU): 5 lần thí nghiệm (mục 6) → chứng minh hệ chạy được + cách chấm hoạt động + hệ có hiệu quả thật.
5. **Verify dữ liệu:** xác nhận AndroidControl **chở được** phần lớn việc chấm; sửa các bẫy dữ liệu.

---

## 3. THIẾT KẾ CUỐI (design E) — "lớp làm-cho-trung-thực, độc lập model"
1. **Bộ viết** = model mạnh nhất, **THAY ĐƯỢC** (Qwen mở; sau cắm GPT-5/Gemini-3) → viết hướng dẫn **gọi nút theo TÊN**.
2. **Oracle** (danh sách nút thật của màn) đặt **BÊN CẠNH**, kiểm "nút có thật không, ở đâu" — **không chặn** việc viết.
3. **Fallback:** nút không khớp → **mô tả bằng lời** (không bỏ bước, không bịa). *(Bản đã chạy còn biết SỬA: bắt một model khác chọn lại nút thật.)*
4. *(Nhiều ảnh)* thêm **Bước 0: tự xếp thứ tự màn**.

> **Vì sao tốt & không lỗi thời:** đóng góp = **cái lớp + cách chấm**, model là **mảnh thay được** → GPT-6 ra chỉ làm số đẹp hơn, khung không đổi. *(Bộ dò + đánh số cũ → hạ xuống 1 nhánh đối chứng.)*

---

## 4. DÙNG DỮ LIỆU GÌ (3 bộ — thầy đã duyệt)
| Bộ | Có gì | Vai (đã chốt) |
|---|---|---|
| **AndroidControl** | quy trình nhiều bước + **mục tiêu thật** + **đáp án vàng** + cây nút mỗi màn | **TRỌNG TÂM** — chở phần lớn việc chấm |
| **MobileViews** | ảnh 1 màn + danh sách nút | kiểm **1 màn** (nhẹ; câu hỏi tự soạn) |
| **ScreenSpot** | ảnh + 1 lệnh + vị trí nút | **đối chứng** tìm-nút |

> Phần định lượng nặng dồn vào **AndroidControl** (có mục tiêu thật + đáp án vàng) → khó bị vặn "câu hỏi tự bịa".

---

## 5. CÁCH CHẤM ĐIỂM (metric) — gọn (chi tiết: `18_metric_ro_rang.md`)
- **Bịa (Faithfulness):** nhắc nút không tồn tại không? (matcher **ALOHa** so theo NGHĨA, không vu oan đồng nghĩa).
- **Đủ ý (Coverage):** bỏ sót nút cần không? (đo trên AndroidControl, có đáp án vàng).
- **Đúng chỗ (Grounding):** bấm trúng khung nút không?
- **Đúng nhãn (Clarity):** gọi đúng tên hiển thị không? *(gọi "Thiết lập" cho nút "Cài đặt" → trừ clarity, KHÔNG tính bịa — hai lỗi khác nhau, đo riêng)*.
- **Xếp thứ tự (τ-b)** + **Làm-theo-tới-đích (Step-SR):** cho nhiều màn, trên AndroidControl.
- **Khớp người (Track B):** kiểm máy chấm có giống người không.
> Quy ước: **cao = tốt**. Mỗi metric có công thức + ví dụ rõ ràng trong `18`.

---

## 6. KẾT QUẢ CHẠY THỬ THẬT (bằng chứng — miễn phí, CPU; chi tiết `15`)

**a) Hệ chạy được + cách chấm bắt lỗi đúng:** đã chạy end-to-end; metric phát hiện đúng bịa/sai-chỗ.

**b) Cách chấm NHẠY (phân biệt model tốt/dở):**
| | Qwen 3B | Qwen 7B |
|---|---|---|
| Bịa *(đo bằng matcher CHUỖI)* | 40.7% | **25.0%** |

*(model mạnh hơn bịa ít hơn — đúng kỳ vọng. Lưu ý: 40.7% là số **matcher chuỗi**; nâng lên **ALOHa** còn **33.3%** — xem (c). Hai số khác matcher, **KHÔNG mâu thuẫn**.)*

**c) Matcher ALOHa đáng tin hơn:** matcher chuỗi-thô vu oan đồng nghĩa → báo bịa 40.7%; ALOHa còn **33.3%** (sửa 2 ca oan). Tách **Bịa vs Đúng-nhãn (Clarity 59.3%)**.

**d) ⭐ HỆ HIỆU QUẢ VỀ ĐỘ-TRUNG-THỰC (thí nghiệm A/B):**
| | Model viết tự do | **+ design E** |
|---|---|---|
| Faithfulness (không bịa) | 66.7% | **100%** |
| Đúng-nhãn (Clarity) | 59.3% | **92.6%** |
| 9 bước bịa *(đếm theo ALOHa)* → | — | **SỬA 9/9 thành nút THẬT** |

→ Hệ **không chỉ giấu lỗi mà SỬA lỗi** — bước sửa do **một model KHÁC** chọn lại nút thật *(lần chạy này fallback dùng 0 lần)* → trung thực hơn + đúng-nhãn hơn hẳn. **Bằng chứng cụ thể nhất cho "hệ hiệu quả VỀ ĐỘ-TRUNG-THỰC".**

> ⚠️ **Trung thực:** mới chứng minh hiệu quả **về độ-trung-thực/đúng-nhãn**. "Sửa thành nút THẬT" chưa chắc là nút **ĐÚNG cho mục tiêu** (MobileViews không có đáp án vàng) → "**đúng-mục-tiêu / tới-đích (Step-SR)**" phải đo trên **AndroidControl = phần Colab**.

---

## 7. ĐI TIẾP ĐƯỢC VỚI PIPELINE NÀY KHÔNG?
✅ **ĐƯỢC — tín hiệu sơ bộ MẠNH ủng hộ đi tiếp, chưa cần đổi pipeline.** Các lần chạy (smoke-test miễn phí: 10 màn / 1 app / model 3B–7B) cho thấy hệ chạy thật, cách chấm nhạy + (sau ALOHa) **đáng-tin-hơn**, cơ chế hệ **hiệu quả đo được về độ-trung-thực**. Nhược điểm còn lại là **tinh chỉnh/mở rộng** (câu hỏi tốt, nhiều dữ liệu, model mạnh, hạ tầng), không phải lỗi thiết kế. ⚠️ **Xác nhận ĐẦY ĐỦ (ý nghĩa thống kê + "tới-đích"/Step-SR) cần chạy quy mô + đáp án vàng trên AndroidControl/Colab.**

**Ưu:** khả thi cao (chạy free CPU) · không lỗi thời (model thay được) · metric nhạy + có lá chắn chống gian lận · hiệu quả đo được · nền lý thuyết bình duyệt · "null vẫn đậu" (an toàn).
**Nhược (nói thẳng):** phần sinh nhẹ kỹ thuật (có chủ ý) · kết quả nhạy với chất lượng câu hỏi · coverage/tới-đích cần gold (Colab) · chưa có bảng số tiếng Việt (thiếu dataset) · "thắng frontier" chỉ ở trục hẹp.

---

## 8. CÁC QUYẾT ĐỊNH ĐÃ CHỐT
1. Pipeline = **design E** ✅
2. **Không fine-tune** (huấn luyện lại) ở phần lõi ✅
3. Model viết = **Qwen mở** (lõi) + GPT-5/Gemini-3 (đối chứng) ✅
4. **Trọng tâm AndroidControl**; MobileViews/ScreenSpot = kiểm nhẹ ✅
5. Tách **2 số: Bịa (đồng-nghĩa-OK) vs Đúng-nhãn (đúng tên)** ✅
6. Định lượng **tiếng Anh**; **tiếng Việt = demo** (thiếu dataset chuẩn) ✅

---

## 9. CÒN PHẢI LÀM GÌ
**Miễn phí (đang/đã làm gần xong):** protocol câu hỏi use-case · nâng matcher (đã làm) · metric rõ ràng (đã làm) · A/B hiệu quả (đã làm).
**Cần Colab (một lần, sau khi đăng-ký-trước):**
- Parse cây accessibility AndroidControl → chấm **coverage + τ-b (xếp thứ tự) + Step-SR (tới-đích)**.
- Chạy quy mô (vài trăm màn + nhiều episode) → con số có ý nghĩa thống kê.
- **Audit người** + validate metric với người (Track B).

> **Nguyên tắc chống tốn kém:** **đăng ký trước (pre-registration)** cách làm + ngưỡng → **chạy Colab MỘT LẦN**, không chạy-đi-chạy-lại; kết quả null vẫn là đóng góp.

---

## 10. BẢN ĐỒ FILE (đọc gì khi cần)
| Muốn | File |
|---|---|
| Hiểu nhanh toàn bộ (file này) | **`00_DOC_TU_DAU.md`** ⭐ |
| **Giải thích ĐẦY ĐỦ từ số 0 (đọc-kỹ)** | **`19_giai_thich_toan_bo.md`** ⭐ |
| Thiết kế cuối chi tiết | `14_thiet_ke_cuoi_2026.md` |
| Kết quả chạy thử (bằng chứng) | `15_ket_qua_chay_thu.md` |
| Metric rõ ràng (định nghĩa + ví dụ) | `18_metric_ro_rang.md` |
| Kế hoạch nguồn-sự-thật | `05_final_plan.md` |
| Cách chạy thử thực tế | `12_trial_run_runbook.md` |
| Chi tiết metric/dataset/pipeline/khả thi | `01` / `02` / `03` / `04` |
| Hồ sơ trả lời câu khó (để dành) | `17_ho_so_bao_ve_hoi_dong.md` |
| Tách 2 bài báo (tương lai) | `KE_HOACH_2_BAI_BAO.md` |
| Code chạy thử | `harness/` |

---

## MỘT DÒNG
**Ta chốt thiết kế "lớp làm-cho-trung-thực độc-lập-model" + một cách đánh giá rõ ràng; đã CHẠY THẬT miễn phí trên CPU và chứng minh: hệ hiệu quả (trung thực 66.7%→100%, đúng-nhãn 59.3%→92.6%) và cách chấm nhạy + đáng tin → đi tiếp được, không cần đổi pipeline; chỉ còn chạy quy mô + đo tới-đích trên AndroidControl/Colab (một lần, sau khi đăng-ký-trước).**
