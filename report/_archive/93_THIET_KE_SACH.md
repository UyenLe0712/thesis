# 93 — Thiết kế sạch (bản chốt hướng, 20/7/2026)

> Viết lại từ đầu sau chuỗi trao đổi 19-20/7. Thay cho đống report chắp vá làm tài liệu "đây là luận văn, đây là việc". Khi mâu thuẫn với report cũ → file này thắng. Kèm: report/90 (phản biện), report/92 (thước rớt + scoop), report/91 (bản gộp cho thầy).

---

## 1. Đề tài (không đổi)

Một model nhận **ảnh chụp màn hình app + câu hỏi/mục tiêu người dùng** → sinh **hướng dẫn nhiều bước cho NGƯỜI đọc và tự làm** (không phải action cho máy bấm).

## 2. Ràng buộc cố định

- Bắt buộc **train một model**, tốt nhất là **hơn baseline** (yêu cầu hội đồng).
- **Không chấm-người** (thầy không muốn) → mọi thước phải khách quan, tự động.
- Một người, ~7 tuần, GPU thuê Colab.

## 3. Luật vàng — xương sống chống ăn gian

> **Lúc CHẤM (test), model chỉ nhận ẢNH + MỤC TIÊU.** Không View Hierarchy, không đáp án. App test là app **chưa từng thấy lúc train**.
>
> View Hierarchy (VH) và đáp án gold **chỉ** dùng để (a) **dạy** lúc train và (b) **chấm điểm** lúc đánh giá — **không bao giờ** đưa cho model lúc sinh.

Đây là thứ làm luận văn thành đóng góp thật: model phải **tự hiểu màn hình lạ**, không được mớm đáp án. "Dùng dataset lúc train = học (bình thường); đưa đáp án lúc test = ăn gian."

## 4. Hai đóng góp ngang nhau

### 4.1. Đóng góp MODEL

Train **Qwen2.5-VL-3B** (SFT-LoRA) trên **hướng dẫn GOLD người-viết** của AndroidControl. Cho ra một model nhỏ, chạy offline, nhìn app lạ **tự sinh hướng dẫn faithful + thực-thi-được**, hơn baseline.

**Ba (–bốn) model:**

| Model | Vai | Học từ |
|---|---|---|
| (mốc sàn) Qwen-3B chưa fine-tune | sàn tham chiếu | — |
| **gpt-4o-mini zero-shot** | baseline NGOÀI (mạnh) | không học |
| **Qwen-3B SFT-trơn** | baseline TRONG (ablation) | gold người-viết |
| **Qwen-3B SFT + thành phần** | **đóng góp** | gold người-viết + thành phần |

- Đánh bại gpt-4o-mini → "3B offline ngang/hơn model API lớn". Được **nhờ luyện đúng-miền trên gold người-viết**, không phải nhờ học từ gpt-4o.
- Đánh bại SFT-trơn → "thành phần em thêm có tác dụng thật" (ablation chứng minh đóng góp, không phải chỉ chứng minh "SFT thì tốt").

> ⚠️ **Bẫy trần bắt chước:** KHÔNG dạy model chính bằng output gpt-4o rồi lấy gpt-4o làm baseline — học từ ai thì cùng lắm bằng người đó. Thầy dạy = **GOLD người-viết**; gpt-4o = **chỉ baseline**. Vì vậy "thành phần thêm" cũng KHÔNG nên là "chưng cất từ gpt-4o".

**Thành phần thêm — CHỐT SAU bằng phép thử rẻ (Cổng B)** (đừng gắn bừa vào chỗ không có room). Danh sách ứng viên đầy đủ + phản biện: `report/95`. Ba nhóm:

- **Nhóm mạnh nhất — TỰ-CẢI-THIỆN bằng tín hiệu cấu trúc** (bộ-trỏ + toạ-độ gold + VH, KHÔNG bằng gpt-4o): mô hình tự sinh nhiều câu → giữ câu được bộ-trỏ+VH duyệt → huấn luyện lại (**RFT/STaR**), hoặc học từ cặp tốt-xấu tự chấm (**self-DPO/KTO**), hoặc chọn bản tốt nhất lúc chạy (**best-of-N**). Đây là nhóm **duy nhất được phép claim "vượt gpt-4o"** (học từ toạ-độ-người, không bắt chước gpt-4o). *Ưu tiên nếu kham nổi ràng buộc chống-circular (xem 4.2).*
- **Nhóm faithfulness (rẻ, ít bẫy hơn):** DPO âm-bản-bịa đúc tất định từ VH, hoặc giải mã ràng-buộc theo OCR-màn. Nhắm thẳng "bớt bịa nút".
- **Nhóm cũ:** vòng kiểm-sửa lúc suy luận; làm giàu câu gold cộc lốc bằng toạ-độ+VH.

> **Cổng B quyết:** 3B **bịa nhiều** → nhóm faithfulness (an toàn, nhanh, ít bẫy). 3B **trỏ kém** → RFT / best-of-N / vòng-kiểm.
> **Khai liêm chính:** cơ chế RFT/RLVR-point-in-bbox đã có trên GUI-agent (UI-R1 AAAI 2026, SE-GUI NeurIPS 2025) nhưng cho *action*, chưa ai cho *sinh-hướng-dẫn-người* → kể là "áp dụng vào tác vụ mới", KHÔNG claim máy móc mới.

### 4.2. Đóng góp ĐÁNH GIÁ (chỗ có chất mới)

Cặp thước khách quan, không cần người, làm cho "hơn baseline" đo được và đáng tin.

**Thước 1 — Executability (độ ĐÚNG: trỏ đúng chỗ không).**
1. Đưa **chỉ câu model sinh + ảnh** (giấu mục tiêu) cho một **bộ trỏ đông cứng**.
2. Bộ trỏ trả toạ độ (x,y).
3. So với **toạ độ nút đúng có sẵn của AndroidControl**; rơi trong dung sai → thực-thi-được.
4. Điểm = % bước thực-thi-được.
- **Control chống vặn:** chạy bộ trỏ **không có câu** (chỉ ảnh) làm sàn. Giá trị câu = có-câu − không-câu. Màn dễ mà không-câu cũng trúng → lộ ra, không ăn gian điểm.
- **Ít nhạy giọng:** bộ trỏ ánh xạ *nghĩa → vị trí*, không thưởng từ vựng. "Tap filter" và "Tap the funnel icon" nếu cùng rõ thì cùng trỏ trúng → "hơn" nghĩa là *rõ/đúng hơn*, không phải *giống gold hơn*. Đây là lá chắn cho đòn nguy hiểm nhất (report/90 §1.3).

**Thước 2 — Faithfulness (độ TRUNG THỰC: có bịa nút không).**
- Mỗi tên nút model nhắc → kiểm có thật trên màn không (đối chiếu VH). Bịa → trừ. Điểm = 1 − bịa/nhắc-nút. Đo trên MobileViews.
- (VH dùng lúc chấm, không đưa model lúc sinh — luật vàng.)

**Validate chính hai thước = bơm-lỗi** (nhét lỗi đã biết, xem thước có bắt). Đây là phương pháp thầy đã duyệt, và là thứ đã **lật được thước cũ** (report/92).

> ⚠️ **RÀNG BUỘC CHỐNG "DẠY ĐỂ THI" (bắt buộc nếu chọn thành phần nhóm tự-cải-thiện — RFT/DPO/best-of-N).** Nếu thành phần dùng bộ-trỏ+VH làm *tín hiệu huấn luyện*, mà lúc chấm cũng dùng bộ-trỏ+VH → số executability lên là **hiển nhiên**, không phải năng lực thật (hội đồng đập ngay). Ba khoá bắt buộc, đóng băng trong pre-register:
> 1. **Bộ-trỏ lúc TRAIN ≠ bộ-trỏ lúc CHẤM** (khác họ / khác checkpoint) — đúng tinh thần "nomic lọc, bge-m3 chấm" của luận văn.
> 2. **Một thước thứ ba NGOÀI reward** (LLM-judge hữu-ích khác-họ, hoặc vài chục mẫu chấm tay) phải KHÔNG tụt.
> 3. **Đối trọng "hữu-ích-cho-người":** canh câu không bị đẩy về nhãn cộc lốc (dễ cho máy, tệ cho người) — vì đề tài là hướng-dẫn-cho-NGƯỜI.
> Nếu chọn thành phần nhóm faithfulness thuần (DPO-âm-bản-VH, OCR-ràng-buộc) thì bẫy này nhẹ hơn nhiều.

**Vì sao đây là chỗ trống thật:** GuideMe/AskEase (HCI) chấm bằng nghiên-cứu-người; dòng GUI-agent chấm hành-động-của-chính-nó. **Chưa ai chấm tính-thực-thi-được của hướng-dẫn-sinh-cho-người bằng thước khách quan tái-lập-được.** (Trung thực: executability/round-trip không phải ta phát minh — code-gen chấm "chạy qua test", dịch máy có back-translation; cái mới là **mang sang sinh-hướng-dẫn-GUI**.)

## 5. Cổng sống-chết còn lại: bộ trỏ

Cả trục executability đứng ở "có bộ trỏ đủ tốt không". Phép thử 20/7: bộ trỏ rẻ (gpt-4o-mini, ảnh thu nhỏ) chỉ **51%** trên câu gold — **chưa đủ**.

- **Việc phải làm:** lấy bộ trỏ **chuyên** (OS-Atlas / UGround / SeeClick / Qwen bản grounding) trên Colab, validate trên câu gold, phải ~80%+.
- **Cứu cánh thống kê:** cái cần là **hiệu Student − Baseline đo qua CÙNG bộ trỏ** → lỗi bộ trỏ phần lớn triệt tiêu trong hiệu → ngưỡng để *so sánh* dễ hơn ngưỡng đo tuyệt đối. Bộ trỏ 70% vẫn so được.
- **Đường lui:** cả bộ trỏ chuyên cũng <80% → tụt về chấm nhóm **nút-có-chữ** (thước v2 chạy tốt) + khai giới hạn; biến "không thước tự động nào trỏ nổi icon" thành một phát hiện đo-lường.

## 6. GuideMe (CHI 2026) — xử framing

GuideMe làm đúng tác vụ ở mức khái niệm nhưng: prompt VLM lớn (không train), không benchmark, chấm-người. → **không dùng làm baseline được** (không tái lập, và chấm-người thì thầy cấm).

- **Hạ claim:** không nói "tác vụ/model đầu tiên". Nói "model nhỏ mở **được huấn luyện** đầu tiên + khung đánh giá định lượng tái-lập-được".
- **GuideMe thành động cơ:** giới HCI đã cần tác vụ này (chứng minh nó đáng làm), nhưng chưa có model tái-lập + thước định lượng → **đó là chỗ ta lấp**.
- Phải trích GuideMe + AskEase trong related work. Lấy full-text GuideMe (ACM chặn) trước khi khoá framing.

## 7. Dữ liệu

- **Giữ AndroidControl** — vì nó có cả (a) hướng dẫn người-viết để SFT, và (b) toạ độ + action gold để đo executability. Đổi dataset = vứt mỏ neo đo lường.
- Test = app-unseen split (app chưa thấy lúc train).
- MobileViews = đo faithfulness (có VH, không có action gold).

## 8. Rủi ro + đường lui (không nhánh nào là ngõ cụt)

| Rủi ro | Đường lui |
|---|---|
| Bộ trỏ không đạt ~80% | chấm nhóm nút-có-chữ + khai giới hạn (phát hiện đo-lường) |
| Student chỉ *hoà* gpt-4o | "3B offline ngang model API lớn" vẫn bảo vệ được |
| Thành phần thêm ra null | phép-thử-chọn-thành-phần trước khi train, gắn vào chỗ có room |
| Tính mới bị vặn | trục mới = thước executability cho hướng-dẫn-sinh, không phải "tác vụ đầu tiên" |

## 9. Việc theo thứ tự

1. **(free) Phép thử chọn thành phần** — đo SFT-trơn yếu ở đâu (bịa? trỏ kém?) → chốt thành phần thêm.
2. **(Colab) Cổng bộ trỏ** — validate grounder chuyên trên câu gold, ~80%+ → go/no-go trục executability.
3. Gặp thầy: chốt thước (executability + faithfulness), baseline (gpt-4o-mini + SFT-trơn), "hoà thì sao", framing GuideMe. *(Thuyết phục, không xin phép — hướng đã tự chốt.)*
4. Dựng data (gold AC) → train ba model → đo hai thước + bơm-lỗi validate.
5. Trung thực phụ (MobileViews) + viết.

## 10. Một câu tóm

> Luận văn = **(1)** một model 3B mở, nhìn app lạ chỉ-bằng-ảnh, sinh hướng dẫn thực-thi-được + faithful, **hơn baseline** (gpt-4o-mini zero-shot & SFT-trơn) nhờ luyện trên gold người-viết + một thành phần thêm; **(2)** một khung đánh giá **executability + faithfulness** khách quan, không-người, validate bằng bơm-lỗi — chỗ mà HCI (chấm-người) lẫn dòng agent (chấm-action-của-mình) đều bỏ trống. Model là một trụ, thước là trụ kia và là chỗ có chất mới.
