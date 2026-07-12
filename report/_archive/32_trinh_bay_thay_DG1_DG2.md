# 🎤 BẢN TRÌNH BÀY LUẬN VĂN (DG1 + DG2) — trình thầy

> **Cách dùng:** mỗi "SLIDE" có **(nói gì)** + **(giải thích cho người chưa biết)** + chỗ nào quan trọng có **(khoa học/nguồn)**. Cuối có **PHẦN THỦ** — bộ câu-hỏi-khó của GS phản biện + câu trả lời chắc. Nguyên tắc: **chủ động nêu cái mình KHÔNG claim** trước khi bị hỏi.
> **Bố cục:** Vấn đề → Khung đánh giá (DG1 + DG2) → DG1 (không gold) → **DG2 (có gold — sức nặng khoa học)** → Pipeline → Dữ liệu & độ chặt → Đóng góp → Thủ.
> **Trung thực:** số liệu cuối đang chạy; hôm nay trình **phương pháp + hướng kết quả sơ bộ**.

---

## 🎯 PITCH MỞ ĐẦU (45 giây — học thuộc)

> *"Em làm hệ **sinh hướng dẫn sử dụng phần mềm** từ ảnh giao diện và câu hỏi người dùng. Đầu vào có thể là **một ảnh** (làm được ngay trên màn) hoặc **nhiều ảnh đã xáo trộn** của một luồng (model phải tự suy ra thứ tự rồi mới hướng dẫn). Hai cái khó: model hay **bịa nút không có thật**, và **không có hướng dẫn mẫu chuẩn** để chấm. Luận văn có **hai đóng góp ngang nhau**: (1) một **phương pháp tạo sinh** hướng dẫn bám-sát-màn, model-agnostic; (2) một **khung đánh giá hai nhánh** — DG1 đánh giá khi **không có đáp án vàng** (neo vào danh sách nút thật của màn), và DG2 đánh giá **năng lực suy luận thứ tự màn** khi **có đáp án vàng** (trên dataset bình duyệt AndroidControl). Em **không** claim hệ mạnh nhất; em chứng minh **cách đo đáng tin** và **lớp sinh giảm bịa**, đều **đăng ký trước**."*

---

# PHẦN A — VẤN ĐỀ & KHUNG TỔNG

## SLIDE 1 — VẤN ĐỀ (cho người chưa biết gì)
**(Nói):**
- Người dùng gặp app lạ hỏi: *"muốn làm việc này thì bấm vào đâu?"*.
- **Mô hình đa phương thức (VLM)** — AI **vừa nhìn ảnh vừa đọc chữ** — nhìn ảnh màn hình + câu hỏi → viết **hướng dẫn từng bước**.
- **Hai chế độ (input router):** **1 ảnh** → trả lời ngay trên màn; **N ảnh đã xáo trộn** của một luồng → model phải **tự suy ra THỨ TỰ đúng** rồi mới hướng dẫn.

**(Giải thích):** "Đa phương thức" = nhìn được cả ảnh lẫn chữ (như GPT-4o). Phần "N ảnh xáo trộn" trả lời đúng câu hỏi thầy hay hỏi: *"làm sao model biết màn nào trước màn nào sau?"* — đó là cái em **đặt ra để ĐO** (DG2).

## SLIDE 2 — BA CÁI KHÓ TRUNG TÂM
**(Nói):**
1. **Ảo giác (hallucination):** VLM nhắc nút/menu **không có trên màn** → người làm theo lạc.
2. **Không có đáp án mẫu:** chẳng ai soạn sẵn "hướng dẫn chuẩn dùng app X" → không biết lấy gì chấm.
3. **Thứ tự màn (đa bước):** đưa N màn xáo trộn, **làm sao biết model xếp đúng thứ tự không** — và nó dựa vào **tín hiệu gì**?

**(Giải thích):** Bài dịch máy có bản dịch chuẩn để so; bài này **không có** → đây là cái khó cốt lõi, và là lý do em phải **chế ra cách đo** thay vì dùng đáp-án-vàng có sẵn.

## SLIDE 3 — HAI ĐÓNG GÓP (ngang nhau)
**(Nói):**
- **① Phương pháp TẠO SINH** hướng dẫn bám-sát-màn (lớp "làm-cho-trung-thực", *cắm model nào cũng chạy*): giảm bịa nút.
- **② KHUNG ĐÁNH GIÁ hai nhánh** đáng tin khi không có / có đáp án vàng (DG1 + DG2).
- **Kế thừa khung đánh giá** từ Chim, Ive, Liakata — *Computational Linguistics 51(1), 2025* (Intrinsic + Extrinsic): văn bản LLM sinh ra = "synthetic text" cần đánh giá khi không có đáp án chuẩn.

---

# PHẦN B — KHUNG ĐÁNH GIÁ (lõi khoa học)

## SLIDE 4 — ⭐ KHUNG HAI NHÁNH: trục phân định = "CÓ đáp án vàng để chấm hay KHÔNG"
| | **DG1** | **DG2** |
|---|---|---|
| Bài toán | Hướng dẫn trên **MỘT màn** | Suy luận **THỨ TỰ N màn** rồi hướng dẫn |
| Đáp án vàng? | **KHÔNG** (neo bằng "đáp án bạc" = View Hierarchy) | **CÓ** (gold trajectory của AndroidControl) |
| Đo gì | Trung thực / không-bịa / đúng-nhãn | **Thứ tự đúng (Kendall τ-b)** + làm-theo-tới-đích (Step-SR) |
| Dataset | MobileViews | AndroidControl (NeurIPS 2024) |
| Vai trò | Bài VCL (nộp trước) | Sức nặng "đúng-ý" + chuẩn ngành |

**(Giải thích):** Hai nhánh **bù nhau**: DG1 đo *"có bịa không"* khi không có gold; DG2 đo *"có đúng-ý / tới-đích không"* khi **có** gold. Chính DG2 trả lời được câu mà DG1 không trả lời được (đúng-ý), nên **trình cả hai mới đủ sức nặng**.

## SLIDE 5 — MỘT HỆ DUY NHẤT (input router)
**(Nói):** `N=1` → chế độ đơn-bước (DG1, Stage-0 rỗng). `N≥2` → bật chế độ sắp-thứ-tự (DG2). Cùng một pipeline.

---

# PHẦN C — DG1 (không có đáp án vàng)

## SLIDE 6 — Ý TƯỞNG: View Hierarchy làm "đáp án bạc"
**(Nói):** Mỗi màn Android có sẵn **cây phân cấp giao diện (View Hierarchy)** — bản kê **mọi nút thật + tên + toạ độ** do hệ điều hành cấp. Dùng nó để chấm *"nút mà hướng dẫn nhắc tới có thật không?"*. **LUẬT VÀNG:** chỉ dùng **lúc CHẤM**, **không** đưa cho model lúc SINH (chống rò rỉ / data leakage).

**(Giải thích):** "Bạc" (không "vàng") vì nhãn **tự động, đủ tin nhưng không hoàn hảo** — em khai thẳng. Nếu mớm danh sách nút lúc sinh thì "không bịa" thành hiển nhiên → kết quả giả.

## SLIDE 7 — PIPELINE DG1 (4 bước)
```
[Ảnh + Câu hỏi] → B1. VLM sinh hướng dẫn BASE (gọi nút theo TÊN)
                → B2. Đối chiếu từng bước với View Hierarchy
                → B3. Lớp hậu kiểm: bước trỏ nút KHÔNG tồn tại → viết lại thành MÔ TẢ BẰNG LỜI
                → B4. Chấm + thống kê
```
**(Giải thích):** "BASE" = bản model viết **tự do** (mốc so). Lớp hậu kiểm **không sửa** bước đúng; chỉ **cách-ly** bước bịa thành mô tả việc-cần-làm bằng lời (thay vì bắt người tìm nút không có thật).

## SLIDE 8 — METRIC DG1 + ⭐ CHỐNG VÒNG-LẬP-LUẬN
**(Nói):** Thước đo: **Trung thực** (không nhắc nút không tồn tại), **Đúng-nhãn** (gọi đúng tên hiển thị), **Định dạng**.
- **Bẫy vòng-lập-luận:** nếu cùng một công cụ vừa **quyết** cách-ly vừa **chấm** → trung thực **đương nhiên 100%** = đẳng thức.
- **Tách đôi:** **QUYẾT** bằng embedding A (`nomic`); **CHẤM** bằng embedding B (`bge-m3`) **+ một LLM-judge KHÁC HỌ** với model sinh.
- **Số thật để báo = tỉ-lệ-bịa của BASE** (độ lớn vấn đề), **không** phải con số 100% sau-lớp.
- **Validate chính thước đo** bằng **perturbation test**: bơm lỗi đã-biết (định nghĩa **độc lập** matcher) → đo tỉ lệ phát hiện. *(Tiền lệ: Sai et al., EMNLP 2021.)*

**(Khoa học/nguồn):** matcher kiểu **ALOHa (NAACL 2024)** = LLM trích + so-nghĩa + ghép một-một (Hungarian). LLM-judge ở đây là **phán đoán hẹp, nhị-phân, neo-tham-chiếu** — vùng đáng tin nhất (Zheng et al., NeurIPS 2023: đưa tham chiếu vào giảm sai judge 70%→15%).

## SLIDE 9 — DG1: PHẠM VI & TRUNG THỰC (lá chắn)
**(Nói — chủ động nêu giới hạn):**
- **Claim DUY NHẤT của DG1:** lớp hậu kiểm **giảm tham chiếu đến nút không tồn tại**, **giá = % bước phải mô tả khái quát** (fallback).
- **KHÔNG claim** "đúng-ý / hữu-ích" — cái đó cần **đáp án vàng → để DG2**.
- **Hai giới hạn em tự khai:** (a) View Hierarchy là **snapshot một-trạng-thái** → nút sau cuộn/menu ẩn có thể bị nhầm là "không tồn tại" → em **lọc/đánh dấu** bước off-screen; (b) độ phủ (recall) của View Hierarchy là **ẩn số → em tự đo (cổng K1)** và đóng khung "số có điều kiện recall".

---

# PHẦN D — DG2 (có đáp án vàng — SỨC NẶNG KHOA HỌC)

## SLIDE 10 — ⭐ BÀI TOÁN DG2: SUY LUẬN TRẬT TỰ MÀN
**(Nói):** Đưa **N ảnh ĐÃ XÁO TRỘN** của một luồng + mục tiêu → model phải (1) **suy ra THỨ TỰ đúng** của các màn, (2) sinh hướng dẫn theo thứ tự đó. Đây là bài **đặt ra để ĐO năng lực suy luận thứ tự** — trả lời thẳng câu hỏi thầy: *"làm sao model biết trật tự?"*.

**(Giải thích):** Khác bản cũ "đoán mù màn kế tiếp". Ở đây **mọi ảnh đều thấy**, chỉ là **bị xáo** → model phải sắp lại. Để chấm công bằng, ta **xáo trộn có kiểm soát**: strip metadata, tái mã hóa ảnh, **che status bar/đồng hồ/pin/badge** (chống model đọc lén thứ tự — cổng KB), và **loại episode có màn gần-trùng**.

## SLIDE 11 — ⭐⭐ METRIC TRỤ: Kendall τ-b CHẤM THEO THỨ-TỰ-BỘ-PHẬN
**(Nói):**
- **Kendall τ-b** ∈ [−1,+1]: +1 = xếp trùng khít đáp án, 0 = như đoán bừa. *(Kendall 1938; tiền lệ headline: Lapata, CL 2006.)*
- **Chấm partial-order-aware:** chỉ **PHẠT cặp BẮT BUỘC** (đăng-nhập-trước-xem-kết-quả); cặp **TỰ DO** (điền email/sđt trước-sau đều được) đảo **vẫn tính ĐÚNG**. *(Fagin et al. — thứ-tự-bộ-phận.)*
- **⭐ Nhãn "cặp bắt buộc" suy từ ĐÁP ÁN VÀNG bằng QUY TẮC NHÂN-QUẢ TẤT ĐỊNH** (màn B chỉ xuất hiện **sau** khi thực thi gold action ở màn A ⇒ cặp (A,B) bắt buộc), **KHÔNG** lấy từ bộ-dò-tín-hiệu mà model dùng → **chống tự-chấm (vòng lập luận)**.

**(Giải thích cho người mới):** "Cặp bắt buộc" = hai màn mà một cái **chắc chắn phải trước** cái kia (vì nhân-quả). "Cặp tự do" = đảo cũng không sai (điền email hay sđt trước đều được). Ta **chỉ trừ điểm khi sai cặp bắt buộc** → công bằng. Và nhãn này **lấy từ đáp án vàng**, không phải từ chính model → **không tự ra đề tự chấm**.

## SLIDE 12 — ⭐ "ORDERING GAP" + model dựa vào TÍN HIỆU gì
**(Nói):**
- **ORACLE-ORDER (cận trên / skyline):** đưa N ảnh **đã sắp đúng** → model chỉ sinh hướng dẫn.
- **SELF-ORDER (thật):** đưa N ảnh **xáo** → model tự sắp rồi sinh.
- **ordering gap = chất-lượng(ORACLE) − chất-lượng(SELF) = "cái giá của việc không biết trật tự".**
- **5 ORDERING CUES** (trả lời "model dựa vào đâu"): *gating* (đăng nhập trước) · *nav-affordance* (Next/Back/breadcrumb) · *state-delta* (toggle off→on, ô trống→đã điền) · *title-progression* (tiêu đề theo phiếu) · *drill-down* (màn sau = chi tiết item màn trước).
- **Signal-attribution = phân tầng theo MỘT cue** (chỉ giữ cặp phân biệt bởi đúng một cue, đo acc theo nhóm) — **KHÔNG che pixel** (che pixel tạo artifact).

**(Giải thích):** "Skyline" = trần lý tưởng (được cho sẵn thứ tự đúng). Khoảng cách giữa "tự sắp" và "được cho sẵn" chính là **năng lực sắp thứ tự** đáng giá bao nhiêu. 5 cue = 5 manh-mối model có thể dựa vào để đoán thứ tự.

## SLIDE 13 — Tier A (teacher-forced): TRỤC THAM CHIẾU CHUẨN NGÀNH = "đúng-ý"
**(Nói):** Mỗi bước, đưa model **màn THẬT của đáp án vàng** rồi để nó đoán thao tác kế. Metric: **Action-Type accuracy** (đúng loại bấm/cuộn/gõ), **Grounding@14%** (*ngưỡng dung sai 14%* trích từ AITW, NeurIPS 2023), **Step-SR** (làm-theo-tới-đích). *(AndroidControl, NeurIPS 2024 D&B — peer-reviewed.)*

**(Giải thích — vì sao quan trọng):** Đây là chỗ **DG2 đo được "ĐÚNG-Ý / tới-đích"** mà DG1 không đo được (vì DG1 không có gold). **Step-SR chính là bằng chứng khó cãi nhất** rằng hướng dẫn **dùng được thật**, không chỉ "không bịa". → đây là **xương sống khoa học** của luận văn.

---

# PHẦN E — PIPELINE ĐỀ XUẤT (ReOrder-Tutor)

## SLIDE 14 — KIẾN TRÚC (Stage-0 sắp thứ tự ⊕ pipeline sinh)
```
N ảnh xáo + mục tiêu
   │
   ▼  STAGE 0 — Screen-Ordering
   ├ S0a per-screen feature (tái dùng parser, không thêm module)
   ├ S0b ordering reasoner = PAIRWISE-then-aggregate:
   │     mỗi cặp hỏi VLM "màn nào trước?" + bắt trích ≥1 cue
   │     → tổng hợp bằng COPELAND score (phá hòa tất định)
   │     [chi phí C(N,2) call; chốt trần N≤6 = 15 call]
   │     [LISTWISE = đối chứng, fair-compute cùng tổng số call]
   ├ S0c order verifier (code thuần; chu trình mâu thuẫn → min-feedback-arc-set xấp xỉ)
   │
   ▼  Chuỗi đã sắp → PIPELINE SINH (design E)
   ├ sinh hướng dẫn GỌI NÚT THEO TÊN (không pixel)
   ├ oracle grounding ĐẶT BÊN CẠNH (không chặn khâu sinh) → chấm + kích fallback
   └ chấm grounding ĐẦY ĐỦ mọi màn
```
**(Giải thích):** "Pairwise" = hỏi từng cặp "màn nào trước" rồi tổng hợp (Copeland = đếm số trận thắng). Off-the-shelf, **không fine-tune** lõi. **N=1** → Stage-0 rỗng → về pipeline DG1.

**(Khoa học):** đặt oracle **BÊN CẠNH** (không đặt-trước) để **recall thấp chỉ hạ độ-tin-phép-đo, không cắt tutorial**. Bộ dò SoM/OmniParser hạ xuống **một bậc ablation + công cụ đo recall**.

---

# PHẦN F — DỮ LIỆU, ĐỘ CHẶT, KHẢ THI

## SLIDE 15 — DATASET (vai cố định)
| Dataset | Vai | Bình duyệt? |
|---|---|---|
| **MobileViews** | DG1 (ảnh + VH + bbox) | preprint (chỉ là hiện vật) |
| **AndroidControl** (NeurIPS 2024) | **DG2 + Tier A** (episode + gold action) | ✅ peer-reviewed |
| **ScreenSpot-v2** (OS-Atlas, ICLR 2025) | đối chứng grounding (point-in-bbox) | ✅ |
| **AITW** (NeurIPS 2023) | nguồn **ngưỡng 14%** (bắt buộc) | ✅ |

**(Khoa học):** xương sống phương pháp chỉ trích **peer-reviewed**; công cụ (Qwen/OmniParser) là preprint nhưng chỉ là hiện vật kỹ thuật. AndroidControl: 15,283 episode / 833 app, mean ~5.5 bước/episode; trục N thực **N∈[3,~10]**, headline **N≤6**.

## SLIDE 16 — ĐỘ CHẶT PHƯƠNG PHÁP (hàm lượng khoa học)
**(Nói):**
- **Chống vòng-lập-luận:** (DG1) matcher chấm ≠ matcher quyết; (DG2) nhãn cặp-bắt-buộc **suy từ gold tất định**, không từ bộ-dò model dùng.
- **Pre-registration:** đăng ký trước giả thuyết + ngưỡng + quy tắc quyết định → chống "chạy tới khi đẹp"; **"null vẫn đậu"**.
- **Thống kê:** **cluster bootstrap theo APP** (màn cùng app không độc lập) + **Holm-Bonferroni** đa-metric + **≥30 episode mỗi mốc N**.
- **Audit người:** 50–80 cặp kiểm quy-tắc-cặp-bắt-buộc khớp đánh-giá-người (báo %); P/R + Cohen's kappa cho matcher.
- **Bốn cổng cứng:** **K1** (đo recall) · **KN** (histogram độ dài episode) · **KZ'** (prior-art sắp-ảnh) · **KB** (chống leak step-index).

**(Giải thích):** "Pre-register" = chốt luật chơi **trước** khi nhìn kết quả → không ai cãi được "chỉnh số". "null vẫn đậu" = kể cả kết quả âm cũng là đóng góp vì đã đăng ký trước.

## SLIDE 17 — KHẢ THI / CHI PHÍ
**(Nói):** Phần lớn đã chạy **miễn phí trên CPU** (Ollama). Quy mô đầy đủ: **1 GPU thuê (Colab) + ~$100–300 API** đối chứng. Chạy **một lần** sau pre-register. *(Máy không GPU → VLM nhìn-ảnh phải API cloud — đã có retry chống 429.)*

---

# PHẦN G — ĐÓNG GÓP & ĐỘ MỚI

## SLIDE 18 — ĐÓNG GÓP (chốt)
**HAI đóng góp NGANG NHAU:**
- **① Phương pháp tạo sinh hướng dẫn bám-sát-màn** (model-agnostic): giảm bịa (DG1) + sắp thứ tự rồi sinh (DG2).
- **② Khung đánh giá hai nhánh:** reference-free neo VH (DG1) + reference-based partial-order τ-b chống-tự-chấm (DG2) + Tier A Step-SR (đúng-ý).

**Độ mới (khai thật — incremental nhưng vững):** áp khung đánh giá vào **tutorial-không-gold** + **partial-order τ-b cho GUI** + **signal-attribution theo cue** + **chống-vòng-lập-luận hai tầng**. **Thừa nhận prior-art** sắp-ảnh (Sort-Story EMNLP 2016, RankGPT EMNLP 2023) — độ mới = **domain GUI + điều-kiện-hoá theo mục tiêu + gắn ordering→sinh tutorial**.

## SLIDE 19 — GIỚI HẠN TỰ NÊU (nêu trước khi thầy bắt)
| Giới hạn (thật) | Cách đỡ |
|---|---|
| DG1 chỉ đo tự-nhất-quán, không đúng-ý | **DG2 + Step-SR (có gold)** đo đúng-ý |
| Faithfulness DG1 ~100% là trần do thiết kế | Báo **tỉ-lệ-bịa-BASE** + % fallback, không trưng 100% |
| 2 embedder không độc lập hoàn toàn | Thêm **LLM-judge khác họ** + đo P/R; DG2 dùng gold (không lệ thuộc embedder) |
| View Hierarchy là snapshot (cuộn/ẩn) | Lọc/đánh dấu bước off-screen; đo recall K1 |
| Lớp sinh = "né khi không chắc" | Khai hẹp "giảm bịa"; đúng-ý chứng ở DG2 |
| Không bảng số tiếng Việt | Định lượng EN/ZH; VN demo định tính (giới hạn **dữ liệu**) |

---

# 🛡️ PHẦN THỦ — CÂU HỎI KHÓ (GS phản biện) & TRẢ LỜI

**❓ "DG1 chỉ đo 'có bịa không', đâu đo 'đúng-ý'? Vậy có tautology không?"**
✅ Đúng, em **thừa nhận**: DG1 đo tự-nhất-quán, và faithfulness sau-lớp ~100% là **trần do thiết kế** (em báo tỉ-lệ-bịa-BASE, không trưng 100%). **Phần 'đúng-ý' em đo ở DG2** bằng **Step-SR trên AndroidControl có đáp án vàng từng bước** — đây là bằng chứng khó cãi rằng hướng dẫn **làm-theo-tới-đích**, không chỉ "không bịa". → Hai nhánh **bù nhau**, không trùng.

**❓ "Có VÒNG LẬP LUẬN (tự ra đề tự chấm) không?"**
✅ Không, ở **cả hai tầng**: (DG1) matcher **CHẤM** (bge-m3 + LLM-judge khác họ) **khác** matcher **QUYẾT** (nomic); (DG2) nhãn "cặp bắt buộc" **suy từ ĐÁP ÁN VÀNG bằng quy tắc nhân-quả tất định**, **KHÔNG** lấy từ bộ-dò-cue mà model dùng. Có **audit người 50–80 cặp** kiểm quy tắc khớp người.

**❓ "Làm sao model biết thứ tự màn? Hay nó đọc lén metadata/thanh trạng thái?"**
✅ Đó **chính là cái em đo** (DG2). Em **chống đọc-lén** bằng cổng **KB**: strip metadata, tái mã hóa ảnh, **che status bar/đồng hồ/pin/badge**, loại episode trùng-pixel — và CI test: detector mù-xem-pixel **không** suy ra thứ tự tốt hơn ngẫu nhiên. Model dựa vào **5 cue giao diện** (gating/nav/state-delta/title/drill-down), và em **phân tầng theo từng cue** để biết cue nào trả công.

**❓ "Bịa nút thì matcher embedding có vu oan đồng nghĩa không? Ngưỡng τ tự chọn?"**
✅ Em **tách 2 trục**: *Bịa* (nút có tồn tại — đồng nghĩa OK, matcher so-nghĩa kiểu ALOHa) vs *Đúng-nhãn* (gọi đúng tên hiển thị — so chuỗi). Ngưỡng τ **hiệu chỉnh trên tập gán-nhãn người rồi FREEZE trước khi chạy**, báo **P/R + Cohen's kappa** và **độ-nhạy theo τ**. (Để đỡ công người: model pre-label, người duyệt ~20–30 cặp vùng-bất-đồng — HITLC.)

**❓ "AI chấm AI (LLM-judge) có đáng tin?"**
✅ Em **không** để AI chấm "hay/dở" (vùng lệch). Em dùng nó cho **phán đoán hẹp, nhị-phân, neo-tham-chiếu** ("tên nút có khớp một nút thật không") — vùng đáng tin nhất; **Zheng et al., NeurIPS 2023**: đưa tham chiếu vào giảm sai judge **70%→15%**. Judge **khác họ** model sinh + **đo P/R với người**.

**❓ "Mẫu/thống kê — sao biết không phải may rủi?"**
✅ **Cluster bootstrap theo app** (màn cùng app không độc lập) + **Holm** + **≥30 episode/mốc N** + **pre-register**. Ngưỡng "vượt random" là **phân phối null EMPIRICAL theo từng N** (sinh hoán vị ngẫu nhiên rồi đo τ-b), không giả định kỳ vọng = 0.

**❓ "Bộ dò sót nút (recall thấp) thì kết quả còn tin được?"**
✅ Em **tự đo recall trước (cổng K1)** và đóng khung mọi số "có điều kiện recall = X%". Quan trọng: oracle đặt **BÊN CẠNH** (không đặt-trước) nên recall thấp **chỉ hạ độ-tin phép đo, không cắt tutorial**.

**❓ "2026 có GPT-5/Gemini-3 rồi, làm cái này còn ý nghĩa?"**
✅ Có. Frontier **vẫn bịa nút, vẫn sai thứ tự**. Đóng góp của em là **cách đánh giá + lớp model-agnostic** (model thay được) → model mạnh hơn chỉ làm **số đẹp hơn**, không làm đề tài lỗi thời. (Lineage được công nhận: lớp grounding là đóng góp, model là mảnh thay được.)

**❓ "Xáo N ảnh bắt sắp lại — thực tế không?"**
✅ Em nói thẳng: đây là **bài đặt ra để ĐO** năng lực suy luận thứ tự (trả lời câu hỏi của thầy), **không** khẳng định là nhu cầu deploy phổ biến. Em **lọc episode màn gần-trùng** để bài đo có nghĩa.

**❓ "Đủ chuẩn thạc sĩ chưa, hay quá đơn giản?"**
✅ Luận văn có **hai đóng góp** + **hai nhánh đánh giá**, trong đó **DG2 dùng dataset bình duyệt + đáp án vàng + Step-SR** cho **sức nặng "đúng-ý"**, cộng **độ chặt phương pháp** (chống-vòng-lập-luận hai tầng, pre-register, cluster bootstrap, audit người, 4 cổng cứng). Em **khai hẹp đúng mức** từng claim nên không overclaim. → Đủ chuẩn; DG1-một-mình thì mỏng, nên em trình **cả hai**.

---

# 📌 MỘT DÒNG KẾT
> *"Luận văn = một **hệ sinh hướng dẫn bám-sát-màn** (giảm bịa, sắp thứ tự rồi sinh) + một **khung đánh giá hai nhánh**: DG1 đo trung thực khi **không có đáp án vàng** (neo View Hierarchy, chống-vòng-lập-luận, validate bằng perturbation), DG2 đo **năng lực suy luận thứ tự** và **đúng-ý** khi **có đáp án vàng** (Kendall τ-b partial-order chống-tự-chấm + Step-SR trên AndroidControl). Mọi giả thuyết **đăng ký trước**, mọi giới hạn **tự nêu** — nên mỗi câu đều đứng vững."*

---

## GHI CHÚ CHO NGƯỜI TRÌNH BÀY
- **Số cuối đang chạy** → khi thầy hỏi số: *"sơ bộ đúng hướng (model mạnh hơn bịa ít hơn; metric phân biệt được tốt/dở); em đang chạy chính để có bảng số + CI"*. **Đừng đọc số chưa có.**
- **Đòn mạnh nhất:** chủ động nói Slide 9 + Slide 19 (cái mình KHÔNG claim + giới hạn) **trước** khi bị hỏi.
- Nếu thầy khen DG2: nhấn **Step-SR (đúng-ý) + τ-b chống-tự-chấm** là phần khoa-học-nặng nhất.
- Thứ tự ưu tiên nếu thiếu giờ: Slide 1–4 (khung) → 10–13 (DG2) → 8 (chống vòng-lập-luận) → 19 (giới hạn).
