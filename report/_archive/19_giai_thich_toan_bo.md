# 📖 GIẢI THÍCH TOÀN BỘ — TỪ ĐẦU ĐẾN CUỐI (cho người chưa biết gì)

> **File này là gì?** Bản giải thích **đầy đủ, đọc một mạch là hiểu hết**: đề tài làm gì, vì sao khó, hệ thống chạy ra sao, chấm điểm thế nào, đã thí nghiệm gì, kết quả ra sao, đã quyết gì, còn phải làm gì. **Mọi từ chuyên môn được giải thích NGAY tại chỗ.** Đọc tuần tự từ trên xuống.
> *(Bản tóm-tắt-nhanh: `00_DOC_TU_DAU`. Thiết kế kỹ thuật: `14`. Kết quả chạy: `15`. Metric: `18`. Kế hoạch nguồn-sự-thật: `05`.)*
> **Cập nhật:** 2026-06-26.

---

## PHẦN 1 — BÀI TOÁN LÀ GÌ (từ số 0)

Tưởng tượng một người **không rành dùng app**. Họ chụp màn hình app + hỏi *"muốn làm việc X thì bấm vào đâu?"*. Đề tài này xây một **chương trình tự động viết hướng dẫn bấm từng bước** cho họ.

- **Đầu vào:** một (hoặc nhiều) **ảnh chụp màn hình** + một **câu hỏi**.
- **Đầu ra:** **hướng dẫn từng bước**.

> **Ví dụ xuyên suốt (app thuế eTax):**
> - *Ảnh:* màn hình chính eTax (có các nút: Khai thuế, Nộp thuế, Tra cứu nghĩa vụ thuế, Thông báo…).
> - *Câu hỏi:* "Tôi muốn kiểm tra đã nộp thuế chưa thì vào đâu?"
> - *Hướng dẫn mong muốn:* "1. Bấm **Tra cứu nghĩa vụ thuế**. 2. Chọn **kỳ tính thuế**. 3. Xem **trạng thái** đã nộp/chưa."

**Hai chế độ:**
- **1 ảnh** → viết hướng dẫn ngay trên màn đó (đơn giản).
- **Nhiều ảnh bị XÁO TRỘN** của một quy trình → máy phải **tự xếp lại đúng thứ tự các màn** rồi mới viết. *(Đây là bài ta cố tình đặt ra để ĐO xem máy có "hiểu" được trình tự không — không phải nhu cầu phổ biến.)*

---

## PHẦN 2 — VÌ SAO KHÓ

**Khó 1 — Không có "bài mẫu chuẩn".** Bình thường muốn chấm máy làm đúng/sai, ta so với đáp án mẫu do người soạn. Ở đây **không có** kho hướng dẫn mẫu. → phải **tự nghĩ ra cách chấm điểm** đáng tin mà không có đáp án mẫu. (Đây chính là một nửa đóng góp của luận văn.)

**Khó 2 — Model hay mắc 3 lỗi.** Nếu đưa thẳng ảnh + câu hỏi cho một **VLM** *(VLM = Vision-Language Model: mô hình AI vừa "nhìn" ảnh vừa viết chữ, như GPT-4o/Gemini/Qwen)* và bảo "viết hướng dẫn đi", nó thường:
1. **Bịa nút không có thật** ("bấm nút Cài đặt" trong khi màn không có nút đó) → gọi là *hallucination*.
2. **Chỉ sai chỗ bấm** (nói bấm góc trên, nút thật ở chỗ khác).
3. **Trình bày lộn xộn** (gộp nhiều việc vào 1 câu, không đánh số).

→ Cần một **hệ thống khéo** để ép model tránh 3 lỗi này. Đó là nửa còn lại của đóng góp.

---

## PHẦN 3 — LUẬN VĂN ĐÓNG GÓP GÌ (hai phần ngang nhau)

- **(A) HỆ THỐNG viết hướng dẫn TỐT:** một quy trình thông minh khiến máy viết **đúng nút, ít bịa, dễ làm theo** — và **chứng minh** nó tốt hơn để máy viết tự do.
- **(B) CÁCH ĐÁNH GIÁ đáng tin** khi không có bài mẫu chuẩn.

> Cả hai **ngang nhau**. Ta **KHÔNG** tuyên bố hệ "mạnh nhất thế giới" — mà chứng minh **thêm hệ của mình vào thì hướng dẫn trung thực & dùng được hơn**, và **cách đo của mình đáng tin**.

---

## PHẦN 4 — DÙNG DỮ LIỆU GÌ (3 bộ — thầy đã duyệt)

Để chấm điểm, ta cần dữ liệu có sẵn **danh sách nút + vị trí** (để biết máy đúng/sai). Ba bộ:

| Bộ | Là gì | Vai trò |
|---|---|---|
| **AndroidControl** | ~15.000 **quy trình nhiều bước**, mỗi bước có **mục tiêu thật + đáp án vàng** (thao tác đúng) + ảnh + danh sách nút mỗi màn | **TRỌNG TÂM** — chở phần lớn việc chấm |
| **MobileViews** | ~600.000 ảnh **1 màn** + danh sách nút | kiểm **1 màn** (vai nhẹ) |
| **ScreenSpot** | ảnh + 1 lệnh + vị trí nút đúng | **đối chứng** độ chính xác tìm-nút |

> *Vì sao AndroidControl trọng tâm?* Vì nó có **mục tiêu thật do người dùng đặt** + **đáp án vàng từng bước** → ta chấm được "làm theo có tới đích không", và **không phải tự bịa câu hỏi**. (MobileViews thiếu câu hỏi → phải tự soạn; nên để vai nhẹ.)
> *"đáp án vàng" (gold)* = chuỗi thao tác đúng mà dataset cung cấp sẵn. Chỉ dùng **lúc chấm**, không cho máy xem lúc viết (cho xem = gian lận).

---

## PHẦN 5 — HỆ THỐNG CHẠY THẾ NÀO (design E)

### Ý tưởng cốt lõi (ẩn dụ)
Vấn đề lớn nhất là model **bịa nút**. Mẹo: **đừng để model tự do, mà có một "người kiểm" đứng bên cạnh** đối chiếu với danh sách nút thật của màn, và **sửa** nếu model nói sai.

### Bốn bước (gọi là "lớp làm-cho-trung-thực")
1. **Bộ VIẾT** = model mạnh nhất hiện có, **CÓ THỂ THAY** (Qwen — model mở, miễn phí — làm lõi; sau cắm GPT-5/Gemini-3). Nó viết hướng dẫn **gọi nút theo TÊN** ("bấm nút *Tra cứu*"), vì người đọc cần *tên nút + thứ tự*, không cần toạ độ pixel.
2. **ORACLE** *(= bộ tra-cứu đáng tin = danh sách nút thật của màn)* đặt **BÊN CẠNH**: kiểm "nút *Tra cứu* có thật không, ở đâu?". **Không chen vào lúc model viết** — chỉ để **chấm** và **bắt lỗi**.
3. **SỬA / FALLBACK:** nếu model gọi một nút không khớp nút thật nào → cho **một model KHÁC chọn lại** nút thật đúng nhất; nếu thật sự không có nút hợp → **mô tả bằng lời** ("chọn mục ... ở phía trên") thay vì bịa. → **không bỏ bước, không bịa.**
4. *(Khi nhiều ảnh)* thêm **Bước 0: tự xếp thứ tự màn** trước khi viết.

```
ẢNH + CÂU HỎI
   │  (nhiều ảnh → Bước 0: xếp thứ tự màn)
   ▼
BỘ VIẾT (model thay được)  → hướng dẫn gọi nút theo TÊN
   ▼
ORACLE kiểm "nút có thật? ở đâu?"  (đặt bên cạnh, không chặn)
   ▼
sai → SỬA (model khác chọn lại nút thật) → vẫn không có → FALLBACK mô tả bằng lời
   ▼
HƯỚNG DẪN cuối  …… (chấm điểm bằng oracle; oracle KHÔNG vào lúc viết) ……
```

### Vì sao thiết kế này tốt & không lỗi thời
- **Bản cũ** bắt một "bộ dò nút" chạy TRƯỚC rồi ép model chỉ nhắc nút bộ dò thấy → nếu bộ dò **sót nút**, hướng dẫn thiếu bước. **Bản này (design E)** đặt oracle **bên cạnh** → bộ dò sót chỉ làm *giảm độ tin phép đo*, **không cắt cụt hướng dẫn**.
- Đóng góp nằm ở **"cái lớp" + cách chấm**, model là **mảnh thay được** → GPT-6 ra đời chỉ làm **số đẹp hơn**, khung không đổi. *(Bộ dò + đánh số cũ "Set-of-Mark" nay chỉ còn là một nhánh để so sánh.)*

---

## PHẦN 6 — CHẤM ĐIỂM THẾ NÀO (cách đánh giá)

Ta chấm hướng dẫn theo nhiều **thước đo**. Mỗi cái: *đo gì · ví dụ · cao/thấp*. (Quy ước: **cao = tốt**.)

### Cho MỘT màn:
1. **Bịa (Faithfulness):** "có nhắc nút không tồn tại không?"
   - Khớp tên nút model viết với nút thật bằng **ALOHa** *(= matcher so theo NGHĨA dùng "embedding" — biến chữ thành dãy số đo nghĩa; "Thiết lập" ≈ "Cài đặt" nên không bị coi là bịa)*. Faithfulness = 1 − tỉ-lệ-bịa.
2. **Đúng-nhãn (Clarity):** "có gọi ĐÚNG TÊN hiển thị không?"
   - So **chính xác**. Gọi "Thiết lập" cho nút tên "Cài đặt" → người dùng **khó tìm** → trừ điểm clarity, **nhưng KHÔNG tính bịa** (vì nút có thật). *(Đây là 2 lỗi khác nhau, đo riêng — một điểm tinh tế quan trọng.)*
3. **Đủ ý (Coverage):** "có bỏ sót nút cần thiết không?" — chống mẹo "viết thật ít cho khỏi sai". Đo trên **AndroidControl** (có đáp án vàng → biết nút nào cần).
4. **Đúng chỗ (Grounding):** "điểm bấm có rơi trong khung nút thật không?" (point-in-bbox).
5. **Định dạng (Format):** "có đánh số, động từ hành động, 1 việc/bước không?"

### Cho NHIỀU màn:
6. **Xếp thứ tự (Kendall τ-b):** "model xếp N màn xáo trộn đúng thứ tự tới đâu?" (+1 = trùng khít, 0 = như đoán bừa). **Chỉ phạt cặp BẮT BUỘC** (vd "đăng nhập trước → xem kết quả sau"); cặp **tự do** (điền email/sđt trước-sau đều được) đảo vẫn đúng. *(Cách chấm "thứ-tự-bộ-phận" này có nguồn chuẩn: Fagin et al.; nhãn cặp-bắt-buộc suy từ đáp án vàng để KHÔNG tự-chấm.)*
7. **Làm-theo-tới-đích (Step-SR):** "làm theo hướng dẫn có tới đích không?" — bằng chứng **khó cãi nhất**. Cần đáp án vàng → đo trên AndroidControl.

### Đảm bảo cách chấm đáng tin:
8. **Khớp với người (Track B):** cho người chấm ~60–80 hướng dẫn → xem điểm máy có **xếp hạng giống người** không (đo bằng tương quan + độ-đồng-thuận Krippendorff α).

---

## PHẦN 7 — ĐÃ THÍ NGHIỆM GÌ + KẾT QUẢ THẬT

**Quan trọng:** máy hiện tại **không có GPU**, nên ta dùng **Ollama** *(phần mềm chạy model AI ngay trên máy, dùng CPU)* + model mở **Qwen2.5-VL** → chạy thử **THẬT, hoàn toàn miễn phí**. Đã chạy nhiều lần:

**(a) Hệ chạy được + cách chấm bắt lỗi đúng** (chạy end-to-end trên ảnh thật).

**(b) Cách chấm NHẠY — phân biệt model tốt/dở:**
| | Qwen 3B (nhỏ) | Qwen 7B (lớn hơn) |
|---|---|---|
| Tỉ lệ bịa *(matcher chuỗi)* | 40.7% | **25.0%** |

→ model lớn hơn bịa ít hơn (đúng kỳ vọng). Thước đo phân biệt được = dấu hiệu **đáng tin**.

**(c) Matcher ALOHa đáng tin hơn:** matcher so-chữ-thô vu oan đồng nghĩa → báo bịa 40.7%; dùng **ALOHa (so nghĩa)** còn **33.3%** (2 ca oan được sửa). *(Nên 40.7% và 33.3% chỉ là khác matcher, KHÔNG mâu thuẫn.)*

**(d) ⭐ HỆ CÓ HIỆU QUẢ (thí nghiệm A/B):** so "model viết tự do" vs "model + hệ design E":
| | Viết tự do | **+ design E** |
|---|---|---|
| Faithfulness (không bịa) | 66.7% | **100%** |
| Đúng-nhãn (Clarity) | 59.3% | **92.6%** |
| 9 bước bịa → | — | **sửa 9/9 thành nút THẬT** |

→ Hệ **không chỉ giấu lỗi mà SỬA lỗi** (bước sửa do **một model khác** chọn lại nút thật) → trung thực hơn + đúng-nhãn hơn hẳn. **Đây là bằng chứng cụ thể nhất cho "hệ hiệu quả".**

---

## PHẦN 8 — HỆ CÓ "THẮNG GPT-5" KHÔNG? (trả lời trung thực)

- ❌ **Không thắng về văn hay** — frontier (GPT-5/Gemini-3) viết mượt hơn; đừng cược vào đây.
- ✅ **Thắng về:** **ít bịa hơn + đúng nút hơn + dễ làm theo hơn so với CHÍNH model đó viết tự do**, trên **mọi model**, ở **chi phí thấp**. *(Vì sao còn cửa: nghiên cứu 2026 bình duyệt cho thấy frontier VẪN bịa nút.)*
- **Đã đo (chắc-thắng):** "giảm bịa/đúng-nhãn so model-viết-tự-do" — số ở Phần 7d (trên Qwen).
- **Chưa đo (giả thuyết):** "thắng cả GPT-5/Gemini-3" và "làm-theo-tới-đích (Step-SR) tốt hơn" → cần chạy trên AndroidControl (Colab).
- ✅ **Không lỗi thời:** đóng góp = cách đánh giá + cái lớp (model thay được).

---

## PHẦN 9 — ĐÃ QUYẾT GÌ (6 quyết định đã chốt)
1. Pipeline = **design E** (lớp làm-cho-trung-thực). ✅
2. **Không fine-tune** *(= không huấn luyện lại model)* ở phần lõi — dùng model có sẵn. ✅
3. Model viết = **Qwen mở (lõi)** + GPT-5/Gemini-3 (đối chứng). ✅
4. **Trọng tâm AndroidControl**; MobileViews/ScreenSpot kiểm nhẹ. ✅
5. Tách **2 số: Bịa (đồng-nghĩa-OK) vs Đúng-nhãn (đúng tên)**. ✅
6. **Định lượng tiếng Anh**; **tiếng Việt = demo** *(vì thiếu dataset chuẩn tiếng Việt + model đo nghĩa tiếng Việt còn yếu → để future-work)*. ✅

---

## PHẦN 10 — CÒN PHẢI LÀM GÌ
**Đã xong (miễn phí, CPU):** chứng minh hệ chạy + cách chấm nhạy + matcher ALOHa + A/B hiệu quả + metric rõ ràng.
**Còn lại (cần thuê GPU/Colab, chạy MỘT LẦN sau khi "đăng ký trước"):**
- Đo **Coverage (đủ ý)** + **τ-b (xếp thứ tự)** + **Step-SR (tới-đích)** trên AndroidControl.
- Chạy **quy mô** (vài trăm màn + nhiều quy trình) → con số **có ý nghĩa thống kê**.
- **Người chấm** một ít để kiểm matcher + nhãn cặp-bắt-buộc (Track B).

> **"Đăng ký trước" (pre-registration)** = chốt giả thuyết + ngưỡng + cách quyết định **TRƯỚC khi chạy** → không "chạy lại tới khi số đẹp" (vừa tốn tiền vừa là gian lận khoa học). Nhờ vậy **kết quả null vẫn là đóng góp**.

---

## PHẦN 11 — HẠN CHẾ (nói thẳng để không bị bắt lỗi)
- Phần "viết" nhẹ kỹ thuật (đánh số + prompt + lớp kiểm) — **có chủ ý**; đóng góp nằm ở **cách đánh giá + cái lớp**, không claim mạnh nhất.
- **Không tuyên bố đứng đầu bảng xếp hạng** thế giới (setup khác — viết cho người, không phải robot bấm máy).
- Kết quả **rất nhạy với chất lượng câu hỏi** → phải đầu tư bộ câu hỏi tử tế.
- "Sửa thành nút THẬT" mới chứng minh **trung thực**, chưa chắc nút **ĐÚNG cho mục tiêu** → cần Step-SR (gold) xác nhận.
- Số hiện có là **sơ bộ** (10 màn / 1 app / model nhỏ) — xác nhận đầy đủ cần quy mô + gold.
- Chưa có **bảng số tiếng Việt** (thiếu dữ liệu) → demo định tính.

---

## PHẦN 12 — NÓI GỌN VỚI THẦY (câu "tủ")
> *"Em làm một **lớp trung-thực-hoá** gắn lên bất kỳ model mạnh nào: model viết hướng dẫn theo tên nút, một bộ tra-cứu kiểm bên cạnh, sai thì model khác sửa hoặc mô tả bằng lời. Em **đã chạy thật miễn phí** và đo được hệ làm hướng dẫn **ít bịa hơn (66.7%→100%) và đúng-nhãn hơn (59.3%→92.6%)** so với để model viết tự do. Cộng với một **cách đánh giá đáng tin** khi không có bài mẫu (chống tự-chấm, đo bằng nhiều thước đo có nguồn). Em **đăng ký trước** nên kết quả null vẫn là đóng góp; em **không** claim mạnh nhất thế giới."*

---

## PHẦN 13 — BẢN ĐỒ FILE (đọc gì khi cần)
| Muốn | File |
|---|---|
| Hiểu đầy đủ (file này) | **`19_giai_thich_toan_bo.md`** |
| Tóm tắt nhanh + đã-làm-gì | `00_DOC_TU_DAU.md` |
| Thiết kế kỹ thuật cuối | `14_thiet_ke_cuoi_2026.md` |
| Kết quả chạy thử (bằng chứng) | `15_ket_qua_chay_thu.md` |
| Metric rõ ràng (định nghĩa+ví dụ) | `18_metric_ro_rang.md` |
| Kế hoạch nguồn-sự-thật (chi tiết) | `05_final_plan.md` |
| Cách chạy thử thực tế | `12_trial_run_runbook.md` |
| Chi tiết metric/dataset/pipeline/khả thi | `01`/`02`/`03`/`04` |
| Code chạy thử | thư mục `harness/` |

---

## MỘT DÒNG
**Đề tài: từ ảnh + câu hỏi → máy viết hướng dẫn bám sát ảnh; đóng góp = (A) một "lớp trung-thực-hoá" gắn lên model mạnh (đã chứng minh free: ít bịa hơn 66.7%→100%, đúng-nhãn 59.3%→92.6%) + (B) một cách đánh giá đáng tin khi không có bài mẫu; chạy off-the-shelf, trọng tâm AndroidControl, EN định lượng, "đăng ký trước nên null vẫn đậu", còn lại là chạy quy mô + đo tới-đích trên Colab.**
