# Giải đáp thắc mắc — Đợt 1 (Chương 1 → 4.4 của report/43)

> File này lưu lại **câu hỏi của người làm luận văn + phần trả lời**, để tham chiếu về sau.
> Nguồn số liệu trích trong ngoặc để truy ngược. Ngày lập: 2026-07-08.

---

## Câu 1. Không leo leaderboard agent thì ỨNG DỤNG THỰC TẾ là gì?

**Ngữ cảnh câu hỏi.** Chương 1 nói luận văn *sinh hướng dẫn cho người đọc*, không phải điều khiển agent tự bấm máy, nên không đặt mục tiêu leo bảng xếp hạng benchmark điều khiển agent. Vậy dùng để làm gì?

**Trả lời.** Đầu ra của hệ là **hướng dẫn từng bước cho CON NGƯỜI làm theo**, từ một (hoặc nhiều) ảnh màn hình + một câu hỏi kiểu "làm sao để…". Đây là một lớp bài toán khác hẳn agent tự bấm, và nó có chỗ dùng thật:

- **Trợ giúp ngay trong ứng dụng (in-app help).** Người dùng đang đứng ở một màn, hỏi "làm sao để đổi mật khẩu?" → hệ đọc ảnh màn hiện tại và trả lời bằng các bước bám đúng nút đang có trên màn đó.
- **Tự sinh tài liệu hướng dẫn phần mềm.** Thay vì đội kỹ thuật ngồi viết tay từng bài "how-to" và cập nhật mỗi lần app đổi giao diện, hệ sinh nháp từ ảnh màn.
- **Hỗ trợ khách hàng.** Khách gửi ảnh chụp màn hình kèm câu hỏi → hệ sinh hướng dẫn bám đúng ảnh đó, thay vì trả lời chung chung.
- **Trợ năng & onboarding.** Người mới, người lớn tuổi, hoặc người khiếm thị (đọc màn bằng trình đọc màn hình) được dẫn từng bước. Trên điện thoại, Android có **cây trợ năng (accessibility tree) sống** cấp qua AccessibilityService → hệ có ngay danh sách nút thật để đối chiếu, chạy được **on-device** với model nhỏ.

**Vì sao setup này KHÁC agent tự bấm (và vì sao khác biệt đó là điểm mạnh, không phải điểm yếu):**

| | Agent tự bấm (leaderboard) | Hệ của luận văn |
|---|---|---|
| Ai thực thi | Máy tự bấm | **Con người** làm theo |
| Cần quyền điều khiển thiết bị? | Có | **Không** |
| Rủi ro khi sai | Máy bấm bậy, khó thu hồi | Người còn trong vòng lặp, tự dừng khi thấy vô lý |
| Chấm bằng | Task-success (máy tới đích) | **Chất lượng hướng dẫn cho người** (không có đáp án chuẩn) |

Chính vì chấm khác nên **không so điểm trực tiếp với leaderboard agent** — không phải vì yếu hơn, mà vì đo thứ khác. Đây cũng là lý do đóng góp (B) — *phương pháp đánh giá khi không có đáp án chuẩn* — tồn tại.

*(Nguồn: CLAUDE.md §1–§2; report/43 §1.1, §4.5, §5.3; niche on-device: report/42 §6.)*

---

## Câu 2. Đổi cách gọi cho bớt "giống AI"

**Ngữ cảnh.** Các cụm *"lớp trung thực hoá"*, *"khối sắp thứ tự màn"*, *"đáp án người"* nghe giống văn AI; và viết tắt nhiều quá cũng vậy.

**Trả lời — đề xuất thay bằng lối nói người viết.** Chọn MỘT cách gọi rồi dùng nhất quán cả luận văn:

| Cụm hiện tại | Nên đổi thành (chọn 1) | Ghi chú |
|---|---|---|
| lớp trung thực hoá | **bước đối chiếu với giao diện thật** · *hoặc* **khâu rà nút bịa** · *hoặc* **bước kiểm bám màn hình** | "đối chiếu với giao diện thật" là dễ hiểu nhất cho người ngoài ngành |
| khối sắp thứ tự màn | **bước sắp lại thứ tự các màn** · *hoặc* **khâu khôi phục trình tự màn hình** | dùng động từ ("sắp lại", "khôi phục") nghe tự nhiên hơn danh từ ghép |
| đáp án người | **đáp án do người soạn** · *hoặc* **chuẩn do người gán** · *hoặc* **nhãn của người** | tránh ghép cụt "đáp án người" |

**Nguyên tắc chung để bớt giọng máy (áp cho cả luận văn):**
1. **Ưu tiên động từ + bổ ngữ**, tránh danh-từ-ghép-cụt do dịch máy ("lớp X hoá", "khối Y").
2. **Viết đủ chữ ở lần đầu**, chỉ viết tắt sau khi đã giới thiệu. Ví dụ: viết "hướng dẫn cho **một màn hình**" / "**nhiều màn hình**", KHÔNG dùng "DG1/DG2" trong bài (đây vốn chỉ là tên gọi nội bộ khi trao đổi — bản thân CLAUDE.md cũng quy định slide/bài phải nói "một màn / nhiều màn").
3. **Tránh cụm sáo AI**: "nhằm mục đích", "đóng vai trò then chốt", "một cách hiệu quả", "trong bối cảnh hiện nay". Thay bằng câu ngắn, chủ ngữ rõ.
4. **Đọc to lên**: câu nào đọc lên thấy như bản dịch thì viết lại.

*(Liên quan: quy ước "một màn / nhiều màn" — CLAUDE.md đầu file.)*

---

## Câu 3. Chỉ dataset có View Hierarchy mới kiểm được nút — thực tế nhiều app KHÔNG có nút sẵn thì sao?

**Đây là câu hỏi đúng và quan trọng.** Trả lời gồm ba tầng:

**(a) Phân biệt "lúc CHẤM" và "lúc TRIỂN KHAI".** View Hierarchy (VH) chỉ cần **lúc đánh giá** (để nghiên cứu đo xem hệ bịa bao nhiêu). Đó là công cụ đo của nhà nghiên cứu, không phải điều kiện để hệ chạy. Khi **triển khai thật**, quy trình là *sinh → kiểm → né bịa*, và phần "kiểm" dùng bất kỳ nguồn nút nào **có sẵn tại thời điểm đó**.

**(b) Thực tế nhiều thiết bị CÓ nguồn nút sống.** Trên Android, **AccessibilityService cấp cây trợ năng (a11y tree) theo thời gian thực** cho màn đang hiển thị — tức trên máy người dùng, hệ thường vẫn có danh sách nút thật để đối chiếu, dù bộ dataset gốc không kèm VH. Đây là nền của hướng dùng **on-device**.

**(c) Khi KHÔNG có nguồn nút nào — hệ vẫn xuống-cấp AN TOÀN, không sập.** Đây chính là chỗ thiết kế "chỉ mô tả, không đoán" phát huy: nếu không đối chiếu được, hệ **mô tả việc cần làm bằng lời** thay vì bịa ra tên nút cụ thể. Người đọc vẫn dùng được, chỉ kém cụ thể hơn — và ta **báo minh bạch** tỉ lệ bước phải hạ xuống mô tả (%fallback).

**Khai thẳng giới hạn (không giấu):** chất lượng của phần "kiểm" **chỉ tốt bằng nguồn nút có được**. Thực tế **>77% app thiếu nhãn trợ năng** (Chen et al., ICSE 2020, Distinguished Paper) — nên ta KHÔNG coi VH/a11y là chân lý tuyệt đối, mà dùng nó ở mức *hậu kiểm + fallback*: có nguồn thì rà, thiếu nguồn thì mô tả. Đảm bảo cốt lõi — **"không bao giờ trỏ tới một nút không tồn tại một cách tự tin"** — vẫn giữ được ở mọi mức nguồn.

Nói gọn: **VH là kính hiển vi để nghiên cứu ĐO, không phải bánh xe để hệ CHẠY.** Hệ chạy được cả khi thiếu VH, chỉ là lúc đó nó thận trọng hơn (mô tả thay vì gọi tên).

*(Nguồn: report/43 §4.5 "Chế độ ĐO vs Chế độ TRIỂN KHAI"; CLAUDE.md §3 "Luật vàng" + §5 gạch đầu dòng a11y-tree live; Chen ICSE 2020 = CLAUDE.md §4 nguyên tắc (4).)*

---

## Câu 4. Ngưỡng khớp = 0,55 lấy ở đâu, vì sao có con số này?

**Trả lời thẳng — kèm cả phần chưa hoàn chỉnh (để không overclaim trước thầy).**

**Con số 0,55 đến từ đâu.** Nó là **lằn ranh phân tách** chọn từ một *tự-kiểm nhanh* trên tiếng Anh: khi so bằng embedding `nomic-embed-text`, các cặp **đồng nghĩa** (cùng nút) có độ tương đồng rơi khoảng **~0,60–0,69**, còn các cặp **khác nghĩa** (khác nút) rơi khoảng **~0,39**. **0,55 nằm ở giữa hai cụm đó** → dùng làm ngưỡng cắt: từ 0,55 trở lên coi là cùng nút, dưới thì coi là ảo giác.

**Bằng chứng của mấy con số đó nằm ở đâu (truy nguồn chính xác — hỏi thêm 2026-07-08).** Chúng đến từ **`harness/aloha_match.py`**, khối tự-kiểm ở `if __name__ == "__main__"` (dòng 84–95): script chạy `nomic-embed-text` trên **một dúm cặp EN/VI tự đặt** — ví dụ `"Configure"` ↔ `"Settings"` (đồng nghĩa), `"Log out"` ↔ `"Settings"` (khác nghĩa) — rồi in cosine. Cụm đồng nghĩa rơi ~0,60–0,69, cụm khác nghĩa ~0,39, nên chốt cắt ở giữa = 0,55. ⚠️ **Phải khai thẳng:** đây là **probe ad-hoc cỡ VÀI CẶP, KHÔNG phải bộ hiệu chỉnh chặt** — nó chỉ đủ để *đặt một ngưỡng khởi điểm hợp lý*, chưa phải bằng chứng thống kê. Bộ hiệu chỉnh chuẩn (80–120 cặp gán tay + đường P/R) ở ngay bên dưới — **đã thiết kế nhưng CHƯA chạy**.

**Nói rõ trạng thái (quan trọng, đừng để thầy bắt):** con số 0,55 hiện là **giá trị pre-registered "chốt bằng mắt"**, CHƯA qua bước hiệu chỉnh đầy đủ. Bước hiệu chỉnh chuẩn — **đã thiết kế nhưng CHƯA chạy** — gồm:
1. Gán tay **80–120 cặp** (đúng/sai khớp) làm chuẩn.
2. Vẽ **đường precision/recall theo ngưỡng**, chọn điểm đạt **precision ≥ 0,95**.
3. **Đông cứng (freeze)** ngưỡng đó *trước khi* nhìn kết quả chính (chống "vặn núm cho ra số đẹp").
4. Báo **cả đường P/R** chứ không chỉ một điểm.

**Cách phòng thủ trước giám khảo** (nếu bị hỏi "sao lại 0,55, có phải chọn cho đẹp?"):
- Headline **tỉ-lệ-bịa của bản gốc (~¼)** được tính **ĐỘC LẬP với ngưỡng** (đếm trên bản BASE một lần) → không vặn ngưỡng nào mua được nó.
- Sẽ báo **đường cong faithfulness ↔ %fallback khi quét ngưỡng ∈ {0,50; 0,55; 0,60}** (Pareto), không chốt một điểm.
- Ngưỡng được chốt bằng **precision của matcher so với người** — một trục *trực giao* với kết quả faithfulness → không thể "chọn cho số đẹp".

*(Nguồn: report/22 dòng 30 [gốc con số]; report/40 V8/V11 [phải báo P/R + đường cong, chưa chạy calibration]; harness/dg1_pa2_score.py biến `TAU_A`.)*

---

## Câu 5. "Lỗi âm thầm (silent error)" — sao biết? Đã chứng minh chưa? Có ví dụ chạy thật không?

**Có — đã chạy thật, có ví dụ cụ thể quan sát được.**

**Bối cảnh.** Từng có một phương án cũ tên "correction": khi model viết ra một nút **không tồn tại**, thay vì bỏ, hệ **tra VH tìm nút thật gần nghĩa nhất rồi thay vào**. Nghe hợp lý, nhưng khi chạy thử thì lộ ra vấn đề.

**Lỗi âm thầm là gì.** Phương án đó thay bước bịa bằng một nút **CÓ THẬT nhưng SAI chức năng**. Hậu quả: hướng dẫn *trông đúng* (vì gọi tên một nút thật sự tồn tại trên màn), nhưng dẫn người dùng **bấm nhầm mà không hề hay biết** — cái sai bị *che giấu* thay vì lộ ra. Đó là lý do gọi là "âm thầm" (silent). Nó **nguy hơn cả để nguyên bước bịa**, vì bước bịa lộ liễu thì người ta còn nghi, còn nút-thật-nhưng-sai thì không.

**Bằng chứng thực nghiệm (đã chạy 2026-06-30, 10 màn app1):** phương án cũ tạo ra đúng loại lỗi này, ví dụ thật ghi lại được:

| Màn | Bước bịa gốc | Bị thay nhầm thành | Ghi chú |
|---|---|---|---|
| app1_s1 | `✓` | `Navigate up` | đúng ra là "Submit" |
| app1_s103 | `ADD LOCATION` | `Copy project` | độ tương đồng chỉ 0,49 |
| app1_s121 | `+` | `More options` | độ tương đồng 0,65 |

Mỗi dòng đều là: một nút **có tồn tại** nhưng **sai việc** được nhét vào chỗ bước bịa → người làm theo sẽ bấm sai.

**Vì phát hiện này**, luận văn **loại hẳn phương án "đoán nút gần nhất"** và chốt phương án an toàn **"chỉ mô tả, không đoán"** (gọi là PA2). Đo được: PA2 có **silent-error = 0 theo cấu trúc** (vì không bao giờ gán tên nút mới), đổi lại **~19% bước thành mô tả (fallback)** — cái giá được báo minh bạch.

**Đây có phải "chứng minh" đầy đủ chưa? — Khai thẳng:**
- Ở mức **thí điểm 10 màn / 1 app**: ĐÃ có bằng chứng cụ thể, quan sát trực tiếp được (bảng trên). Đủ để **biện minh quyết định thiết kế**.
- Ở mức **thống kê chặt**: thí nghiệm đầy đủ (đặt tên **E3**) sẽ chạy **"chỉ mô tả" vs "đoán nút" trên TOÀN mẫu + báo khoảng tin cậy**, kỳ vọng **silent-error-rate > 0 với cận dưới CI > 0**. Cái này **chưa chạy ở quy mô lớn**.

Nên phát biểu chuẩn trước thầy là: *"Ta đã quan sát được lỗi âm thầm trên mẫu thí điểm với ví dụ cụ thể; thí nghiệm đối chứng toàn mẫu có khoảng tin cậy là bước đã thiết kế, sẽ chạy cùng đợt chính."* — không nói "đã chứng minh trên toàn bộ".

*(Nguồn: report/26 dòng 126–142 [kết quả chạy thử 10 màn + 3 ví dụ]; report/43 §4.2 "Định lý thiết kế" + §13 E3; report/36 dòng 63.)*

---

### Ghi chú chốt lại cho đợt sau
- Câu 4 & Câu 5 đều dính chung một tinh thần: **phân biệt "đã thiết kế / đã chạy thí điểm" với "đã chứng minh toàn mẫu"** — giữ giọng trung thực này xuyên suốt sẽ chặn được nhiều đòn phản biện.
- Câu 2 (đổi cách gọi) nếu muốn áp vào toàn bộ report/43 + slide thì báo, sẽ rà và đổi đồng loạt cho nhất quán.

---

# Giải đáp thắc mắc — Đợt 2 (Chương 4.3 → 4.5 của report/43)

> Ngày lập: 2026-07-08. Các làm-rõ dưới đây **đã được gấp vào chính report/43** (để chỉ cần đọc 43); file này giữ bản Q&A đầy đủ để truy nguồn.

## Câu 6. "So cặp" là gì, vì sao chọn cách này — có luận điểm khoa học không?

**So cặp (pairwise)** = thay vì đưa cả $N$ màn cho VLM rồi bảo "sắp hết đi" (*listwise*), ta **chỉ hỏi từng lần 2 màn**: *"màn nào đến trước?"*. $N$ màn → $\binom{N}{2}$ cặp ($N=4$ → 6 câu; $N=5$ → 10 câu).

**Ba lý do chọn so cặp — đều có neo:**
1. **Hợp "chế độ" (mạnh nhất).** Qin et al. (Findings NAACL 2024) chứng minh *với model tầm trung*, so cặp cho xếp hạng tốt hơn hẳn listwise. VLM của ta là tầm trung (`gpt-4o-mini`), số màn ít (~5,5) → đúng vùng so cặp thắng.
2. **Dấu vết kiểm tra được.** Mỗi phán đoán cặp soi được đúng/sai riêng lẻ; dãy xuất thẳng là hộp đen.
3. **Phát hiện mâu thuẫn nội tại** (A→B→C→A) mà dãy xuất thẳng che mất.

**Khai thẳng:** ta KHÔNG claim so cặp *luôn* tốt hơn (model rất mạnh thì listwise có thể ngang/hơn) → có **thêm baseline listwise một shot** chấm cùng thước để so sòng phẳng (E8).

*(Nguồn: report/43 §4.3(a); Qin Findings NAACL 2024.)*

## Câu 7. Copeland — nếu VLM phán "đứng trước" số lần BẰNG NHAU (hoà điểm) thì sao?

Điểm Copeland = đếm số màn khác mà nó được phán "đứng trước". Khi **hoà điểm**, có **hai tình huống**:

- **Hoà "lành" (không có vòng):** phá bằng **trận đối đầu trực tiếp (head-to-head)** — xét đúng cặp giữa hai màn đó, ai thắng trận trực tiếp xếp trên. Tất định, tái lập được.
- **Hoà "do vòng cắn đuôi":** ví dụ A→B, B→C, **C→A** → cả ba đều 1 điểm, và head-to-head cũng vô dụng (xét trận trực tiếp vẫn quay vòng). → Copeland bó tay → chuyển sang **bước (c) phá vòng**.

Chính vì Copeland *để lộ* tình huống 2 mà ta phát hiện được mâu thuẫn nội tại.

*(Nguồn: report/43 §4.3(b), hộp "Nếu hai màn BẰNG ĐIỂM".)*

## Câu 8. Phá vòng mâu thuẫn (bước c) — mô tả kĩ hơn

**Ba nhịp:**
1. **Phát hiện vòng.** Phán đoán cắn đuôi nhau (A→B→C→A) → không duỗi thành hàng thẳng → phải gỡ.
2. **Cắt ít "dây" nhất.** Coi mỗi phán đoán là sợi dây; cắt số dây ít nhất để hết mọi vòng = bài toán *minimum feedback arc set* (Ailon, JACM 2008).
3. **Cắt dây YẾU nhất — đo bằng tín hiệu khách quan, KHÔNG hỏi model tự khai** (VLM tự tin cả khi sai): (i) khoảng cách thắng sát nút → yếu; (ii) hỏi lại nhiều lần mà đảo qua đảo lại → yếu; (iii) ưu tiên cắt ít dây nhất.

**Vì sao không hỏi VLM "chắc mấy %"?** Vì VLM **hiệu chỉnh độ tự tin rất kém**; tin lời tự khai = rơi lại bẫy "hệ tự chấm mình". Tiền lệ dùng tín hiệu bất định khách quan: Dodgersort (PAKDD 2026). Ta còn chạy *ablation E11* so với cách phá vòng ngây thơ để chứng minh bằng số.

*(Nguồn: report/43 §4.3(c) + hộp "Tóm tắt bước (c) ba nhịp".)*

## Câu 9. Năm tín hiệu thứ tự lấy ở đâu — có luận điểm khoa học không?

- Năm tín hiệu (gating · nút điều hướng · biến thiên trạng thái · tiêu đề tiến trình · drill-down) **KHÔNG bê từ một bài duy nhất** — là **quan sát/đóng góp của chính luận văn** về nơi quy trình GUI để lại dấu vết thứ tự. Đây là *chỗ mới*.
- **Từng tín hiệu là cơ chế điều hướng chuẩn trong HCI** (Next/Back, drill-down, "Bước 1/3"…) — không bịa.
- **Cái mới là *cách phân tích*, và chỗ này có trụ khái niệm bình duyệt:** Gardner et al. (Findings EMNLP 2020, *contrast sets*) — muốn biết model dựa vào tín hiệu nào thì **cô lập từng tín hiệu** rồi đo. Ta áp đúng: phân tầng một cue.
- **Khai thẳng** đây là trụ *khái niệm* chứ không phải tiền lệ trùng khít — vì có bài y hệt thì hết là đóng góp. Chính chỗ này chứng minh phần sắp thứ tự là *nghiên cứu*, không chỉ ghép thư viện.

*(Nguồn: report/43 §4.3 "Năm tín hiệu thứ tự", hộp provenance; Gardner Findings EMNLP 2020.)*

## Câu 10. Nhiều paper trích từ năm 2000–2008 — có cũ quá không, còn giá trị không?

**Còn nguyên giá trị** — vì có HAI loại trích dẫn:
- **Nền toán học/thuật toán → *nên* trích bài kinh điển gốc.** Copeland (Dwork WWW 2001), min-feedback-arc-set (Ailon JACM 2008), $\tau$ bộ phận (Fagin SIAM 2006 / Lapata CL 2006) là **định lý** — không hết hạn; trích bài đặt nền là chuẩn mực. Trích preprint 2025 cho khái niệm Copeland mới là *lỗi*.
- **Bằng chứng thực nghiệm / xu hướng đánh giá → phải MỚI**, và đã phủ bằng bài 2024–2026 (Qin NAACL 2024, FaithScore EMNLP 2024, Sai EMNLP 2021, EZ-Sort CIKM 2025, Dodgersort PAKDD 2026) + freshness scan (report/42).
- **Nguyên tắc gọn:** nền toán → bài kinh điển; bằng chứng thực nghiệm → bài mới. Trộn đúng chỗ = khảo sát tài liệu *chín*, không phải cũ.

*(Nguồn: report/43 §4.4, hộp "tài liệu 2000–2008".)*

## Câu 11. §4.5 (chế độ ĐO vs TRIỂN KHAI) — trình bày dễ hiểu hơn

**Ẩn dụ chốt — tháo kính đo thị lực.** Muốn đo *thị lực thật*, bác sĩ **bắt bỏ kính ra** — không phải khuyên "sống đừng đeo kính", mà vì đeo kính thì đo ra thị lực của *cái kính*. Sống thì cứ đeo kính (= triển khai *grounded*, cho model xem cây giao diện); nhưng **lúc ĐO** phải tháo kính (= *sinh mù*).

Nếu ĐO mà vẫn "đeo kính" (nạp cây giao diện lúc sinh): model **chép lại** → phần nó tự bịa bị **che** → mất khả năng đo mức ảo giác tự thân. Grounding chỉ *giảm* chứ không xoá ảo giác → đưa vào lúc sinh làm **hỏng phép đo**, không phải "cải tiến".

**Bốn ý chốt:** (1) không đối đầu grounded-gen — triển khai cứ grounded, chỉ tháo ngữ cảnh *lúc ĐO*; (2) grounded lúc sinh làm hỏng phép đo (ảo giác bị che); (3) grounded cũng không "sạch" (>77% app thiếu nhãn — Chen ICSE 2020 → vẫn bịa, lại mất khả năng đo); (4) hậu-kiểm-đối-chiếu-nguồn-ngoài là paradigm chính danh 2024–2026 (FaithScore, CoVe, RARR, CRITIC), và ta dùng tín hiệu NGOÀI/phi-LLM/tất định → đúng nhánh *được chứng minh hợp lệ* (khác "tự sửa nội tại" đã bị Huang ICLR 2024 bác).

**Câu tự trấn an:** câu hỏi này không đâm vào *kiến trúc*, nó đâm vào *cách trình bày kiến trúc* — in rõ §4.5 là vô hiệu hoá.

*(Nguồn: report/43 §4.5, hộp "tháo kính đo thị lực" + hộp Q3 3 tầng.)*

---

### Ghi chú chốt Đợt 2
- Toàn bộ làm-rõ Q6–11 **đã gấp vào report/43** (§1.1, §4.3, §4.4, §4.5) → đọc 43 là đủ; file 49 dùng khi cần bản Q&A gọn.
- Câu 4 đã bổ sung **nguồn chính xác** con số embedding = `harness/aloha_match.py` self-check (probe ad-hoc, chưa phải calibration chặt).
- **Câu 2 — ĐÃ ÁP (2026-07-08):** đổi đồng loạt trong report/43: *"lớp trung thực hoá"* → **"bước đối chiếu với giao diện thật"** (16+ chỗ); *"khối sắp thứ tự (màn)"* → **"bước sắp lại thứ tự các màn"** (8 chỗ); *"đáp án người"* → **"đáp án do người soạn"** (3 chỗ). Giữ nguyên 1 chỗ: tên *construct "trung thực hoá"* ở phần lý-thuyết-đo-lường (đó là tên khái niệm đo, không phải tên thành phần). **Slide (`build_v2.js`) KHÔNG cần sửa** — vốn đã dùng "đối chiếu / sắp thứ tự / độ trung thực", không chứa cụm cũ. **CLAUDE.md giữ nguyên** — "lớp trung-thực-hoá" ở đó là tên gọi tắt nội bộ khi trao đổi, không phải văn bản nộp.
