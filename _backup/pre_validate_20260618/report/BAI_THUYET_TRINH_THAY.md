# BÀI THUYẾT TRÌNH TRÌNH THẦY — KỊCH BẢN ĐẦY ĐỦ (đọc là nói được)

> **Mục tiêu:** trình bày để **được duyệt scope** (*scope = ranh giới những gì luận văn làm/không làm*), người nghe **hiểu 100%**.
> **Mạch trình bày (theo yêu cầu):** Bài toán → **DỮ LIỆU + ví dụ thật** (giới thiệu sớm) → Pipeline (cách máy chạy) → Metric (cách chấm) → Khả thi/Kết luận.
> **Nguyên tắc:** mỗi thuật ngữ giải thích NGAY lần đầu; không dùng từ lạ mà không giải thích.
> **Cấu trúc mỗi slide:** 🖥️ CHIẾU · 🎤 NÓI (đọc gần như nguyên văn) · ❓NẾU THẦY HỎI.
> Cuối bài: **(A) 3 ví dụ dataset thật + cách model xử lý từng bước** (chi tiết), **(B) Từ điển thuật ngữ**.
> ⏱️ 19 slide · ~17–19 phút + 5–10 phút hỏi đáp.

---

## SLIDE 1 — Mở đầu

**🖥️ CHIẾU:** Tên đề tài: *Sinh tự động hướng dẫn sử dụng phần mềm từ ảnh màn hình + câu hỏi, và đánh giá khi không có bản hướng dẫn mẫu* · Học viên · GVHD · 2026

**🎤 NÓI:**
"Em chào thầy. Em xin trình bày đề tài và **xin thầy duyệt phạm vi**. Đề tài: người dùng đưa vào **một ảnh chụp màn hình phần mềm** + **một câu hỏi**, máy **tự sinh ra hướng dẫn bấm từng bước**. Cái khó — và là đóng góp chính — là **chấm điểm chất lượng hướng dẫn đó khi không có *bản hướng dẫn mẫu do người viết sẵn*.** Em sẽ giải thích mọi thuật ngữ ngay khi gặp. Mạch hôm nay: bài toán → **dữ liệu em dùng (kèm ví dụ thật)** → cách máy chạy → cách chấm điểm → tính khả thi."

---

## SLIDE 2 — Bài toán + ví dụ

**🖥️ CHIẾU:** **Vào:** 1 ảnh + 1 câu hỏi → **Ra:** hướng dẫn từng bước · VD (minh hoạ): eTax + *"Kiểm tra đã nộp thuế chưa thì vào đâu?"*

**🎤 NÓI:**
"Đầu vào đúng hai thứ: **một ảnh tĩnh** + **một câu hỏi bằng lời thường**. Đầu ra: **hướng dẫn từng bước** cho người đọc.

Ví dụ — em nói rõ **đây là ví dụ minh hoạ em tự dựng, không phải dữ liệu thật** (dữ liệu thật em cho thầy xem ngay slide sau): ảnh app eTax + câu hỏi *'kiểm tra đã nộp thuế chưa thì vào đâu?'* → máy trả *'1. Bấm Tra cứu nghĩa vụ thuế. 2. Chọn kỳ. 3. Xem trạng thái.'*

Quan trọng: lúc chạy thật máy **chỉ thấy đúng một ảnh + câu hỏi**, không gì thêm."

---

## SLIDE 3 — Vì sao khó (3 thách thức)

**🖥️ CHIẾU:** ① Không có bản hướng dẫn mẫu · ② Máy hay "bịa" nút · ③ Đa bước — làm sao máy biết TRẬT TỰ màn?

**🎤 NÓI:**
"Ba cái khó.
**Một — không có bản hướng dẫn mẫu.** Khác dịch máy (có câu dịch chuẩn để so), ở đây *không ai viết sẵn hướng dẫn chuẩn* cho từng app → câu hỏi lớn: **chấm điểm thế nào khi không có cái để so?**
**Hai — máy hay 'bịa'.** **VLM** = *Vision-Language Model = mô hình AI vừa 'nhìn' ảnh vừa viết chữ* (GPT-4o, Qwen2.5-VL) khi viết tự do hay **'bịa' (hallucination = ảo giác)** — *nhắc nút không có trên màn hình*.
**Ba — đa bước, phải biết TRẬT TỰ.** Một việc đa bước trải trên nhiều màn; **làm sao máy biết màn nào phải làm TRƯỚC, màn nào SAU?** Đây đúng là câu hỏi thầy đặt ra. Em biến nó thành bài toán đo được: đưa máy **nhiều ảnh ĐÃ XÁO TRỘN** của một luồng + mục tiêu, bắt máy **tự xếp lại đúng thứ tự** rồi mới sinh hướng dẫn."

---

## SLIDE 4 — DỮ LIỆU: ba bộ, mỗi bộ một vai (giới thiệu sớm)

**🖥️ CHIẾU:** MobileViews → màn-0 · AndroidControl → đa bước · ScreenSpot → đối chứng grounding · *(thông lệ ≥ 2 bộ)*

**🎤 NÓI:**
"Trước khi nói máy chạy thế nào, em giới thiệu **dữ liệu** — vì cách chấm điểm của em bám hẳn vào dữ liệu này. Em dùng **ba bộ (dataset)** chuẩn quốc tế; thông lệ luận văn dùng **≥2 bộ** để chứng minh tổng quát. Mỗi bộ một vai:

**1) MobileViews** — kho ảnh điện thoại + **View Hierarchy (VH)** = *bản kê khai cấu trúc màn hình do Android xuất ra: liệt kê mọi nút + chữ + toạ độ (bbox)*. Em dùng VH làm **'đáp án để chấm'** màn hình đầu (gọi là 'màn-0'). **VH chỉ dùng lúc CHẤM, không đưa cho máy lúc sinh** (người dùng thật không có VH).

**2) AndroidControl** (hội nghị **NeurIPS 2024** — *hội nghị AI hàng đầu*; 15.283 episode, 833 app) — các **episode** = *phiên thao tác hoàn chỉnh*: mục tiêu + chuỗi (ảnh từng bước, thao tác đúng từng bước). Đây là nơi em đo **đa bước** = bài toán **suy luận trật tự màn** (lấy chuỗi ảnh thật, xáo trộn, bắt máy xếp lại).

**3) ScreenSpot** (hội nghị **ACL 2024**) — bài 'chỉ tay': một câu lệnh → một nút đích. Em dùng **đối chứng** thước đo (so điểm bấm vào nút đúng).

Hai lưu ý em nói thẳng: (a) VH là nhãn **'bạc' (silver)** — *máy xuất tự động, đủ tin để chấm nhưng không hoàn hảo như nhãn 'vàng' do người duyệt* → em **cam kết kiểm tỷ lệ VH thiếu/sai trên ~20 màn**; (b) MobileViews là **preprint** = *bài đăng kho mở, chưa bình duyệt* → em ghép thêm 2 bộ ĐÃ bình duyệt (AndroidControl, ScreenSpot) để bù uy tín."

**❓NẾU THẦY HỎI — 'Sao không có dữ liệu tiếng Việt?'** → "Dạ dataset định lượng đều là app tiếng Anh/Trung — **không tồn tại** dữ liệu tiếng Việt có VH để chấm. Nhưng vẫn ổn vì **thước đo của em độc-lập-ngôn-ngữ** (chấm bằng toạ độ/bbox/định dạng, không phụ thuộc nghĩa tiếng Việt); con validate diện rộng trên EN/ZH + **demo định tính trên app Việt (eTax)** để cho thấy hệ vẫn sinh hướng dẫn tiếng Việt được."

---

## SLIDE 5 — Ví dụ THẬT lấy từ dataset (record trông ra sao + dùng làm gì)

**🖥️ CHIẾU:** 3 record thật: MobileViews (ảnh+VH) · AndroidControl (episode CruiseDeals) · ScreenSpot ("close")

**🎤 NÓI:**
"Để thầy thấy dữ liệu thật trông ra sao (khác ví dụ eTax con tự dựng), đây là **3 record thật**, trích trực tiếp từ tài liệu/trình xem dữ liệu chính chủ:

**① MobileViews — 1 màn** = một ảnh + một **bản liệt kê** mọi nút. Bản liệt kê ghi từng nút bằng lời dễ hiểu kiểu: *«nút tên ‘…’, nằm trong ô từ góc (trái, trên) đến (phải, dưới), bấm được hay không»* — toạ độ tính bằng pixel (cả màn là `[0,0,1080,1920]`). → Em dùng nó để chấm: khi máy nói "bấm ở (x,y)", kiểm (x,y) có rơi trong ô của đúng nút không. *(Chi tiết kỹ thuật của bản liệt kê — gọi là View Hierarchy — ở báo cáo 02.)*

**② AndroidControl — 1 episode thật:** mục tiêu *"On cruisedeals, view cruise schedules for a four-night trip from New York to Canada"* (xem lịch tàu 4 đêm New York→Canada); chuỗi thao tác đúng: **B1** `mở app CruiseDeals` → **B2** `bấm tại (313, 742)` → **B3** `vuốt lên`. → Đây là 'đáp án vàng' (thứ tự đúng). Em **xáo trộn** thứ tự các màn rồi bắt máy **xếp lại** — so với thứ tự vàng này để chấm.

**③ ScreenSpot — 1 mẫu thật:** câu lệnh `"close"`; nút đích có khung `[0.948, 0.144, 0.994, 0.207]` — *toạ độ chuẩn-hoá 0–1 (tính theo tỷ lệ màn, không phải pixel)*; loại `icon`; màn Windows. → Cho câu 'close' + ảnh, máy phải trỏ đúng nút X góc phải-trên.

**Một điểm kỹ thuật quan trọng:** ba bộ dùng **ba kiểu toạ độ khác nhau** — MobileViews là **pixel** `[l,t,r,b]`; ScreenSpot là **0–1**; AndroidControl là **điểm bấm (x,y)**. Nên khi viết code chấm, em **phải quy về cùng một hệ** trước khi so, kẻo sai hàng loạt — em đưa việc này vào checklist."

---

## SLIDE 6 — Hai đóng góp (suy ra trực tiếp từ dữ liệu)

**🖥️ CHIẾU:** ĐG1 — màn-0 (MobileViews: KHÔNG có hướng dẫn mẫu) · ĐG2 — đa bước (AndroidControl: CÓ chuỗi thao tác đúng)

**🎤 NÓI:**
"Hai bộ dữ liệu vừa rồi dẫn thẳng tới **hai đóng góp**, phân biệt bằng câu hỏi: **bộ dữ liệu có sẵn đáp án đúng để so hay không.**

**Đóng góp 1 — đánh giá MÀN-0**, dùng **MobileViews** (không có hướng dẫn mẫu của người). Em gỡ ngay một điểm dễ thắc mắc: **'đáp án để chấm' ở đây KHÔNG phải hướng dẫn do người viết — thứ đó không tồn tại — mà là bản kê khai nút có sẵn (View Hierarchy)**, tức *đáp-án-gián-tiếp do máy xuất ra*, không phải đáp án do người soạn.

**Đóng góp 2 — đánh giá ĐA BƯỚC = SUY LUẬN TRẬT TỰ MÀN**, dùng **AndroidControl** (có sẵn chuỗi thao tác đúng để đối chiếu). Input = **N ảnh đã XÁO TRỘN** + mục tiêu → máy phải (1) **xếp lại đúng thứ tự**, (2) **sinh hướng dẫn từng bước** theo thứ tự đó (slide Đa bước).

Câu đinh: **đóng góp chính là *một cách đánh giá mới* — không phải 'hệ thống của em phải thắng'.**"

**❓NẾU THẦY HỎI — 'Ai soạn câu hỏi use-case? Tự soạn có thiên vị không?'** → "Dạ chỉ **MobileViews** cần tự soạn câu hỏi (AndroidControl/ScreenSpot có sẵn). Chống thiên vị: (1) **đăng ký bộ câu hỏi TRƯỚC khi xem output của hệ**; (2) nhờ **người ngoài duyệt**; (3) 'tự soạn câu hỏi' = chỉ viết *đề bài (input)* cho ảnh có sẵn, *đáp án chấm* vẫn là VH thật — KHÁC hẳn 'bịa đáp án'."

---

## SLIDE 7 — Khảo sát liên quan & điểm mới

**🖥️ CHIẾU:** Đã có: dò nút · agent đa bước · metric hallucination · xếp ảnh/bước xáo (Sort-Story, ACL2022, RankGPT) · **Mới:** xếp trật tự màn GUI + điều kiện-hoá theo mục tiêu → SINH tutorial + truy nguồn tín hiệu

**🎤 NÓI:**
"Đặt đề tài vào bản đồ nghiên cứu. **Đã có sẵn:** (1) công cụ dò nút từ ảnh (OmniParser); (2) cách đánh giá agent đa bước kiểu *teacher-forcing* trên AndroidControl; (3) thước đo 'bịa' như CHAIR, ALOHa; (4) bài toán **xếp lại chuỗi xáo trộn** đã có tiền lệ: **Sort-Story** (EMNLP 2016, xếp ảnh+caption xáo), **Sequencing Multimodal Instructional Manuals** (ACL 2022, xếp bước hướng dẫn đa phương thức xáo), **RankGPT** (EMNLP 2023, LLM sinh permutation theo query).

Em **trung thực: không claim 'xếp ảnh xáo là mới'** — em thừa nhận dòng dõi này. **Điểm mới của em** nằm ở bốn chỗ ghép lại: (a) miền **giao diện GUI màn hình** (không phải truyện/manual); (b) **điều kiện-hoá theo mục tiêu/use-case**; (c) gắn việc xếp trật tự → **SINH ra tutorial** (không chỉ xếp); (d) **truy nguồn tín hiệu** — chỉ ra ảnh có *dấu hiệu* nào giúp xếp đúng. Em đã chạy **kill-test KZ'** (*rà prior-art xếp-ảnh*) → kết luận **GO** với khung claim này: không có công trình trùng khít."

---

## SLIDE 8 — Hệ thống (pipeline): ReOrder-Tutor — xếp trật tự rồi biến "tự luận" thành "trắc nghiệm"

**🖥️ CHIẾU:** **Stage 0 — Xếp trật tự màn** → rồi 5 bước/từng màn: Dò&đánh số → Vẽ số → Sinh có ràng buộc → Kiểm 3 tầng → Đổi số ra toạ độ · *Router: N=1 → bỏ Stage 0; N≥2 → bật*

**🎤 NÓI:**
"Hệ em đề xuất tên **ReOrder-Tutor**. **Pipeline** = *dây chuyền xử lý các bước nối tiếp*. Điểm mới: em **đặt thêm Stage 0 'Xếp trật tự màn'** TRƯỚC dây chuyền 5 bước cũ. **Một bộ định tuyến (router)**: nếu vào **1 ảnh** → bỏ qua Stage 0, chạy như cũ (đơn bước); nếu vào **N≥2 ảnh xáo trộn** → bật Stage 0. Một hệ duy nhất.

**Stage 0 — Xếp trật tự màn** (3 phần nhỏ):
- **S0a — đặc trưng từng màn:** *tái dùng đúng bộ dò nút của bước sau*, không thêm linh kiện.
- **S0b — bộ suy luận trật tự (CHÍNH = hỏi-từng-cặp rồi tổng hợp):** với mỗi **cặp** màn, hỏi VLM *'màn nào trước?'* + **bắt máy trích ≥1 dấu hiệu trật tự** (xem slide ordering cues) → tổng hợp toàn cục bằng **Copeland score** (*ai 'thắng' nhiều cặp hơn thì xếp trước*). Cách *hỏi-một-lần-ép-cả-permutation (listwise)* để làm **đối chứng** chạy cùng ngân sách tính.
- **S0c — bộ kiểm trật tự:** *code thuần, không AI*; nếu có **chu trình mâu thuẫn** (A trước B, B trước C, C trước A) → gỡ bằng thuật toán xấp xỉ (min-feedback-arc-set).

**Rồi 5 bước cũ chạy TRÊN TỪNG màn đã sắp** (ý tưởng cốt lõi chống bịa: biến *'tự luận'* thành *'trắc nghiệm'*):
**B1 — Dò & đánh số nút:** **OmniParser** (*công cụ Microsoft, nhìn ảnh tự tìm vùng bấm được*) + **OCR**. Mỗi nút được gán **một số** + **bbox** (*khung chữ nhật bao quanh nút*).
**B2 — Vẽ số lên ảnh:** **Set-of-Mark** = *vẽ ①②③ đè lên ảnh tại vị trí từng nút*.
**B3 — Sinh có ràng buộc (then chốt):** máy bị **ÉP chỉ trỏ vào số đã có** → **không thể bịa nút MỚI** — cơ chế chống bịa CHÍNH.
**B4 — Kiểm 3 tầng:** **V1** = *code thuần, KHÔNG phải AI* (so số có trong danh sách không); **V2** = *một AI KHÁC* kiểm *'số này có ĐÚNG Ý (intent) câu hỏi không'*; **V3** = *tự sửa, tối đa 2 lần*.
**B5 — Đổi số ra toạ độ** để hiện cho người + chấm điểm.

Nhờ chạy 5 bước trên **mọi màn đã sắp**, grounding được **chấm ĐẦY ĐỦ ở từng màn** (không phải đoán mù)."

**❓NẾU THẦY HỎI — 'Sao dùng OmniParser? Có tốt không?'** → "Vì lúc chạy thật chỉ có 1 ảnh, không có VH, nên cần thứ dò nút THUẦN TỪ ẢNH; OmniParser làm đúng việc đó, có sẵn, không cần train. Con nói thật nó chưa hoàn hảo (grounding ~57% trên màn mobile dày, recall chưa rõ) → là rủi ro số 1, đo bằng K1; nó là *linh kiện thay được*, không phải đóng góp."

**❓NẾU THẦY HỎI — 'Sao vẽ số chứ không bbox / không cho máy tự xuất toạ độ?'** → "Con VẪN có bbox (để chấm), nhưng *số* là giao diện cho model vì: (1) VLM tự xuất toạ độ hay bịa/lệch, chọn một SỐ thì dễ và đúng hơn; (2) số là tập đóng {1..N} nên ÉP được chỉ chọn nút có thật (toạ độ tự do thì rơi đâu cũng được); (3) số vẽ ngay tại nút giúp nhìn-và-trỏ. Xong tra số → bbox để chấm."

---

## SLIDE 9 — ⭐ Đa bước = SUY LUẬN TRẬT TỰ MÀN (ORACLE-ORDER vs SELF-ORDER)

**🖥️ CHIẾU:** *(HÌNH)* hai cột chất-lượng — **ORACLE-ORDER** (đã sắp đúng, cận trên) cao hơn **SELF-ORDER** (tự xếp); khoảng cách = **ordering gap** = "cái giá của việc không biết trật tự"

**🎤 NÓI:**
"Đây là phần lõi đa bước. Bài toán: đưa máy **N ảnh đã XÁO TRỘN** của một luồng + mục tiêu → máy phải **tự xếp lại đúng thứ tự** rồi sinh hướng dẫn theo thứ tự đó. Em đo bằng cách so hai cấu hình:

- **ORACLE-ORDER (mốc trần / skyline):** đưa N ảnh **ĐÃ sắp đúng sẵn** + mục tiêu → máy **chỉ phải sinh** hướng dẫn, không phải tự xếp.
- **SELF-ORDER (thật):** đưa N ảnh **xáo trộn** → máy **tự xếp rồi mới sinh**.
- **ordering gap** = chất-lượng(ORACLE-ORDER) − chất-lượng(SELF-ORDER) = **'cái giá của việc không biết trật tự'**. *Sanity cứng:* ORACLE-ORDER phải **≥** SELF-ORDER ở mọi episode (vi phạm = bug).

Câu đinh: **đóng góp mới = LƯỢNG HOÁ được năng lực suy luận trật tự màn — và cái giá khi máy phải tự xếp.**

Ngoài ra **Tier A teacher-forcing** (*mỗi bước người chấm đưa máy đúng màn thật rồi hỏi 'bấm gì'*) em **vẫn giữ làm trục tham chiếu chuẩn ngành** — để so với công trình khác — **nhưng không còn là 'đa bước chính'**."

**❓NẾU THẦY HỎI — 'Vẫn giữ Tier A làm gì?'** → "Dạ Tier A là *cách chuẩn ngành*, thầy expect, dùng để đối chiếu với bài khác (Action-Type/Grounding@14%/Step-SR). Nhưng con **không claim ngang leaderboard** (setup khác, recall bộ dò chưa công bố rõ — con tự đo ở K1). Trục chính bây giờ là **suy luận trật tự**; ORACLE-ORDER là mốc trên của trục đó."

---

## SLIDE 10 — ⭐ "Làm sao máy biết trật tự?" — 5 dấu hiệu trật tự (ordering cues)

**🖥️ CHIẾU:** gating · nav-affordance · state-delta · title-progression · drill-down · *(đối chứng: GOAL-ONLY, RANDOM-ORDER)*

**🎤 NÓI:**
"Đây là câu hỏi thầy đặt ra — *'máy dựa vào đâu để biết màn nào trước/sau?'*. Em **đặt tên 5 dấu hiệu** mà máy có thể bám vào (và bắt máy phải trích ra ở Stage 0):
- **gating (cổng):** việc bắt buộc làm trước — *vd phải đăng nhập / cấp quyền rồi mới vào màn kết quả*.
- **nav-affordance (dấu điều hướng):** nút **Next/Back/breadcrumb** chỉ chiều đi.
- **state-delta (thay đổi trạng thái):** *toggle off→on*, *ô trống→đã điền*, *badge 0→1* → màn 'sau' là màn có thay đổi.
- **title-progression (tiêu đề tiến triển):** tiêu đề theo phiếu/bước (*Bước 1/3 → 2/3*).
- **drill-down (đào sâu):** màn sau = **chi tiết của item** ở màn trước (*danh sách → chi tiết một mục*).

Để **truy nguồn tín hiệu** (cue nào thực sự giúp xếp đúng), em dùng **phân tầng theo một-cue**: chỉ giữ những **cặp màn phân biệt được bởi ĐÚNG MỘT cue**, đo độ chính xác theo từng nhóm cue. Em **KHÔNG che pixel** (che pixel tạo nhiễu giả) — thay vào đó đọc tay các cặp xếp sai (phân tích lỗi mở).

Hai **đối chứng** quan trọng: **GOAL-ONLY** (*che hết ảnh, chỉ đưa mục tiêu + nhãn trong văn bản* — nếu chỉ-mục-tiêu đã xếp đúng cao thì giao diện KHÔNG phải nguồn tín hiệu); **RANDOM-ORDER** (*xếp ngẫu nhiên làm sàn*)."

**❓NẾU THẦY HỎI — 'N ảnh xáo trộn có phải nhu cầu thật của người dùng không?'** → "Dạ em nói thẳng: **chế độ N-ảnh là BÀI TOÁN em ĐẶT RA ĐỂ ĐO** năng lực suy luận trật tự — trả lời đúng câu hỏi của thầy. Em **không** khẳng định người dùng thường đưa nhiều ảnh xáo. Sản phẩm thật vẫn là **1 ảnh** (router N=1). Đây là *thiết kế đo lường*, trung thực với thầy."

---

## SLIDE 11 — Cách chấm MÀN-0 (Đóng góp 1)

**🖥️ CHIẾU:** Grounding · Hallucination (1−HER) · Coverage · Clarity/Format

**🎤 NÓI:**
"**Quay lại MÀN-0** (phần đánh giá *không có đáp án mẫu*) — chấm 4 mặt:
**Grounding** (bám đúng thực địa): **point-in-bbox** = *điểm máy chỉ có nằm trong khung nút thật không* — như phi tiêu trúng đích. (Con số grounding em báo theo **2 cách** — số thật và số giả định bộ-dò-hoàn-hảo — lý do ở slide rủi ro.)
**Hallucination** (bịa): **HER** = *tỷ lệ nút máy nhắc mà màn hình không có* (ý tưởng từ **CHAIR**, thước đo kinh điển 2018); báo '1−HER' (cao=tốt).
**Coverage** (độ phủ): có **bỏ sót** nút quan trọng không.
**Clarity/Format**: **IFEval** (*luật kiểm bằng máy: có đánh số? có động từ mệnh lệnh?*) + **G-Eval** (*một AI chấm độ rõ 1–5*)."

---

## SLIDE 12 — Cách chấm ĐA BƯỚC: thước đo TRẬT TỰ (Đóng góp 2)

**🖥️ CHIẾU:** HEADLINE = **Kendall τ-b** (chấm theo thứ-tự-bộ-phận) · phụ: pairwise-order-acc, position-acc · + Tier A tham chiếu

**🎤 NÓI:**
"Đa bước dùng **gold trajectory** (*chuỗi thao tác vàng có sẵn*, vd episode CruiseDeals ở slide 5) để biết thứ tự đúng.

**Thước đo CHÍNH (headline) = Kendall τ-b** (*đo độ giống nhau giữa hai thứ tự — máy xếp vs vàng*; nguồn: Kendall 1938 + Gao et al. NAACL 2025). Em **không** dùng 'tỷ lệ cặp đúng' thô làm headline (vòng vo). Phụ: **pairwise-order-accuracy** + **position-accuracy@correct-place**. Bỏ Exact-Order-Match khỏi headline (N=3 thì ~17% đúng do may rủi, N≥6 ~0%).

**Điểm tinh tế — chấm theo thứ-tự-bộ-phận (partial-order-aware):** không phải cặp nào đảo cũng là sai. **Chỉ phạt khi đảo cặp BẮT BUỘC** (gating/drill-down: đảo là sai thật); **cặp TỰ-DO thì đảo vẫn tính ĐÚNG**.
- *Ví dụ tự-do:* điền **Email** trước hay **SĐT** trước đều được → đảo **vẫn đúng**.
- *Ví dụ bắt buộc:* **đăng nhập** phải trước **xem kết quả** → đảo là **sai**.

Headline τ-b chỉ tính trên **cặp bắt buộc**; em báo **thêm τ-b-thô** trên toàn tập làm 'điểm sàn' robustness. **Loại N≤2** (N=2 chỉ 1 cặp → τ-b vô nghĩa); trục N thực tế **N∈[3, ~10]** (em phải tự đếm histogram độ dài episode — việc tuần 1).

**Tier A tham chiếu (vẫn giữ):** Action-Type (*đúng LOẠI thao tác*); Grounding@14% (*điểm bấm lệch ≤14% màn — ngưỡng mượn từ AITW*); Step-SR (*= Task Success*)."

---

## SLIDE 13 — Thước đo đều có nguồn bình duyệt (gồm paper của thầy)

**🖥️ CHIẾU:** bảng Tiêu chí | Thước đo | Nguồn · Khung gốc = paper thầy (Computational Linguistics 2025)

**🎤 NÓI:**
"Em chứng minh **không thước đo nào tự chế**. **Khung tổng kế thừa từ paper thầy gửi:** Chim, Ive, Liakata, **Computational Linguistics 2025** (*journal = tạp chí bình duyệt*) — vốn làm *đánh giá văn bản nhân tạo khi không có đáp án chuẩn*, đúng tình huống của em. Em ánh xạ: *Meaning* → Grounding+Hallucination; *Style* → Clarity/Format; *Extrinsic* → Task Success; cách họ **dùng người chấm** em cũng kế thừa (slide sau).

Mỗi thước đo từ hội nghị hàng đầu: point-in-bbox (ACL 2024), HER/CHAIR (EMNLP 2018), **ALOHa** (NAACL 2024 — *khớp tên nút thông minh, tránh nhầm đồng nghĩa*), IFEval, G-Eval (EMNLP 2023), và headline trật tự **Kendall τ-b** (Kendall 1938 + Gao et al. NAACL 2025).

Còn **công cụ** (OmniParser, Qwen, Set-of-Mark) là **preprint** — chỉ là *hiện vật kỹ thuật em DÙNG*, không trình như đã bình duyệt; xương sống phương pháp chỉ trích bài đã bình duyệt."

---

## SLIDE 14 — Đối chiếu người chấm (kế thừa paper thầy)

**🖥️ CHIẾU:** N ≥ 60–80 · BWS · khớp máy↔người: Spearman/Kendall · đồng thuận người: Krippendorff α

**🎤 NÓI:**
"Thước đo tự động cần được chứng minh **đáng tin** → em làm **pilot** (*chạy thử quy mô nhỏ*) với chuyên gia chấm, theo đúng paper của thầy:
- **BWS** = *Best-Worst Scaling: cho chuyên gia chọn bản TỐT NHẤT & TỆ NHẤT → suy ra thứ hạng* (ổn định hơn chấm điểm tuyệt đối).
- **Spearman / Kendall** = *đo độ KHỚP giữa máy và người* (máy có xếp hạng giống người không).
- **Krippendorff α** = *đo độ ĐỒNG THUẬN giữa các người chấm*.
- Quy mô **N ≥ 60–80**. Em đóng khung trung thực: đây là **kiểm tính khả dĩ**, không hứa tương quan cực chặt."

---

## SLIDE 15 — Thí nghiệm chính: thang bậc C0 → C4

**🖥️ CHIẾU:** bảng C0..C4

**🎤 NÓI:**
"Để biết **từng bộ phận có ích không**, em dùng **ablation** = *bóc tách: thêm từng bộ phận, đo từng nấc* (không so 'đầy đủ vs trần' một phát): **C0** trần · **C1** + tự-sửa = **baseline** (*mốc cơ sở*) · **C2** + đánh số · **C3** + ép-chọn-số + kiểm tồn-tại · **C4** + kiểm đúng-ý (đầy đủ). Nhìn mức cải thiện từng nấc → biết **cơ chế nào trả công**."

**❓NẾU THẦY HỎI — 'Nếu C4 không hơn C1 thì pipeline còn gì?'** → "Vẫn có giá trị: (1) **kết quả null đã đăng ký trước** vẫn là phát hiện hợp lệ; (2) bản thân thang bậc đo được cơ chế nào trả công là đóng góp phương pháp; (3) pipeline vẫn là hệ chạy được, tái dùng cho cả 3 chế độ đo."

---

## SLIDE 16 — Rủi ro lớn nhất + các cổng kill-test (nói thẳng)

**🖥️ CHIẾU:** Rủi ro #1: hệ chỉ giỏi bằng bước dò nút → K1 đo recall (cổng cứng) · báo RAW vs ORACLE · cổng KN/KZ'/KB

**🎤 NÓI:**
"**Rủi ro lớn nhất:** cả hệ **chỉ giỏi bằng bước dò nút**; nút bị bỏ sót thì máy vĩnh viễn không nhắc được. **recall** = *trong 100 nút thật, bộ dò tìm ra bao nhiêu*. Thành thật: recall trên màn mobile dày **chưa được công bố rõ** (tài liệu chỉ có 'grounding accuracy ~57%', là chỉ số khác). Nên **việc đầu tiên — kill-test K1** = **tự đo recall** (cổng cứng). Mọi số grounding kèm 'recall = X%', báo **RAW** (*số thật, gánh lỗi bộ dò = lỗi nhìn*) vs **ORACLE** (*giả định bộ dò hoàn hảo, chỉ còn lỗi suy luận = lỗi nghĩ*).

**Các cổng kill-test khác (em đã chạy sơ bộ):**
- **KN — đếm độ dài episode:** AndroidControl có 15.283 episode, trung bình **~5.5 bước/episode**, percentile-95 = **13 bước**. Sau khi loại N≤2, trục N∈[3,~10] vẫn còn đủ episode → **GO có điều kiện**, em sẽ tự đếm chính xác histogram theo từng N (chưa có sẵn).
- **KZ' — rà prior-art xếp ảnh:** đã khảo (Sort-Story/ACL2022/RankGPT) → **GO** với khung claim 'điểm mới = GUI + điều kiện-hoá mục tiêu + sinh tutorial + truy nguồn tín hiệu'.
- **KB — chống lộ thứ tự:** khi xáo trộn **phải gỡ metadata + mã hoá lại ảnh + đặt tên UUID** để máy không 'đọc lén' số bước; có CI test kiểm bộ dò mù không suy ra thứ tự tốt hơn ngẫu nhiên."

---

## SLIDE 17 — Kết quả xấu vẫn ĐẬU (bảo hiểm khoa học)

**🖥️ CHIẾU:** pre-registration → null result vẫn là đóng góp

**🎤 NÓI:**
"Em dùng **pre-registration** = *đăng ký giả thuyết + ngưỡng TRƯỚC khi chạy* → không thể 'thua thì đổi đề'. Em **dồn power vào một trục chính = Kendall τ-b ordering** (đăng ký trước trục này). Nhờ vậy, kể cả khi ra **null result** (*kết quả 'không khác biệt' — hệ không thắng baseline*), nếu **giải thích được CƠ CHẾ vì sao** thì **vẫn là đóng góp hợp lệ**. Luận văn không phụ thuộc 'hệ phải thắng'."

---

## SLIDE 18 — Phạm vi đề nghị chốt + khả thi

**🖥️ CHIẾU:** Trong-luận-văn vs Future-work · 1 GPU 24GB + ~$100–300 · 6 pha có cổng

**🎤 NÓI:**
"Xin chốt: **Trong luận văn:** chấm màn-0 + đa bước suy-luận-trật-tự (SELF-ORDER vs ORACLE-ORDER + Tier A tham chiếu) + thang bậc C0–C4 + pilot người chấm. **Future-work** (*chỉ thứ không có dữ liệu để chấm*): chấm định lượng tiếng Việt; **world-model tự huấn luyện** (*mô hình 'tưởng tượng' màn kế, cần train*); mở rộng web.
**Khả thi:** không huấn luyện model; 1 card 24GB + **~$100–300** (*đẩy phần chấm-bằng-AI sang model rẻ + chạy theo lô, tập nhỏ 50–100 để dò, full chỉ cho bảng cuối*). Lộ trình **6 pha có cổng**."

---

## SLIDE 19 — Kết luận + đề nghị duyệt

**🖥️ CHIẾU:** 3 đóng góp · "Tuần 1: chạy kill-test (đo recall K1 + đếm N + rà prior-art) rồi báo lại thầy"

**🎤 NÓI:**
"Tóm lại ba thứ: **(1)** một *cách đánh giá* tutorial màn-0 khi không có hướng dẫn mẫu; **(2)** một cách *đo đa bước = suy luận trật tự màn* — headline Kendall τ-b, đo **ordering gap** (ORACLE-ORDER − SELF-ORDER) + truy nguồn 5 ordering cues, có Tier A làm trục tham chiếu chuẩn ngành; **(3)** một *thí nghiệm có kiểm soát* (thang bậc C0–C4) + pilot người chấm. Em xin thầy **duyệt phạm vi**; tuần 1 chạy kill-test (quan trọng nhất: **đo recall K1** + **đếm histogram độ dài KN** + **rà prior-art KZ'**) rồi báo lại. Em cảm ơn thầy."

---
---

# (A) BA VÍ DỤ DATASET THẬT + CÁCH MODEL XỬ LÝ TỪNG BƯỚC (bản chi tiết)

> Slide 5 đã giới thiệu nhanh; phần này là bản đầy đủ cho thầy/ai muốn xem kỹ "máy làm gì với dữ liệu".

## Ví dụ 1 — MobileViews (màn-0): chấm grounding + hallucination
Record = ảnh `screen.jpg` + `state.json` (View Hierarchy). Node: `{viewClass:"Button", text:"...", bounds:[l,t,r,b], clickable:true}`; `bounds` pixel; root `[0,0,1080,1920]`. *(Giá trị `text` từng nút con phải tải 1 'shard' — gói dữ liệu nhỏ — mới xem được.)*
**Máy:** dò nút (OmniParser) → đánh số → vẽ số → sinh có ràng buộc ("bấm ②") → kiểm 3 tầng → đổi ② ra toạ độ. **Chấm:** mở `state.json` → điểm có trong `bounds` nút đúng (grounding)? có nhắc nút không có trong VH (HER)?

## Ví dụ 2 — AndroidControl (đa bước = suy luận trật tự màn)
Record THẬT (nguồn: Google Research `android_control`): goal *"On cruisedeals, view cruise schedules for a four-night trip from New York to Canada"* → thứ tự vàng: B1 `open_app CruiseDeals` → B2 `click (313,742)` → B3 `swipe up`.
**Cách đo (SELF-ORDER):** lấy 3 ảnh màn B1/B2/B3, **xáo trộn** (gỡ metadata, đặt tên UUID — KB), đưa cùng mục tiêu → máy phải **xếp lại** đúng B1→B2→B3 rồi sinh hướng dẫn. Chấm thứ tự bằng **Kendall τ-b** (chỉ phạt cặp BẮT BUỘC, vd 'mở app' phải trước 'vuốt xem lịch'). **ORACLE-ORDER:** đưa 3 ảnh đã sắp đúng → chỉ sinh. **ordering gap** = ORACLE − SELF. **Tier A (teacher-forcing, tham chiếu):** đưa ảnh thật từng bước → máy đoán thao tác → so đáp án (Action-Type/Grounding@14%/Step-SR). *(Lưu ý: kiểm `(313,742)` là pixel hay chuẩn-hoá, quy về cùng hệ với bbox trước khi so.)*

## Ví dụ 3 — ScreenSpot (đối chứng grounding): bài "chỉ tay"
Record THẬT (nguồn: HuggingFace `rootsautomation/ScreenSpot`): `instruction:"close"`, `bbox:[0.948,0.144,0.994,0.207]` (**chuẩn-hoá 0–1**), `data_type:"icon"`, source Windows.
**Máy:** cho "close" + ảnh → trỏ vào nút X góc phải-trên. **Chấm:** đổi bbox 0–1 ra pixel rồi kiểm point-in-bbox.

> **Ba bộ — ba format toạ độ** (dễ gây lỗi khi code): MobileViews = pixel `[l,t,r,b]`; ScreenSpot = chuẩn-hoá 0–1; AndroidControl = điểm click `(x,y)`. Harness **phải quy về cùng hệ** trước khi chấm.

---

# (B) TỪ ĐIỂN THUẬT NGỮ (tra nhanh)

| Thuật ngữ | Giải thích một câu |
|---|---|
| **VLM** | Mô hình AI vừa "nhìn" ảnh vừa viết chữ (GPT-4o, Qwen2.5-VL) |
| **View Hierarchy (VH) / VH-silver** | Bản kê khai cấu trúc màn hình (nút + chữ + toạ độ); nhãn "bạc" (máy xuất, đủ tin nhưng không hoàn hảo); chỉ dùng lúc chấm |
| **bbox / pixel / chuẩn-hoá 0–1** | Khung bao quanh nút; pixel = điểm ảnh tuyệt đối; 0–1 = toạ độ theo tỷ lệ màn |
| **episode / gold trajectory** | Một phiên thao tác hoàn chỉnh / chuỗi thao tác đúng có sẵn |
| **OmniParser / OCR** | Công cụ dò nút từ ảnh / nhận dạng chữ trong ảnh |
| **Set-of-Mark** | Vẽ số ①②③ lên ảnh tại vị trí từng nút |
| **Sinh có ràng buộc (constrained)** | Ép máy chỉ trỏ vào số đã có; chống bịa nút mới ở màn hiện tại |
| **verifier V1/V2/V3 / intent** | V1 = code (không AI); V2 = AI khác kiểm đúng-ý; V3 = tự sửa; intent = mục tiêu câu hỏi |
| **Grounding / point-in-bbox** | Chỗ máy bảo bấm có trúng đúng ô nút thật không |
| **Hallucination / HER / CHAIR** | Bịa nút không có; HER = tỷ lệ bịa (báo 1−HER); CHAIR = thước đo gốc (2018) |
| **Coverage / ALOHa** | Có bỏ sót nút quan trọng không / công cụ khớp tên nút thông minh |
| **IFEval / G-Eval** | Luật định dạng kiểm bằng máy / AI chấm độ rõ 1–5 |
| **reference-free (nghĩa hẹp)** | Không có hướng dẫn mẫu của người; vẫn có VH-silver để chấm |
| **Suy luận trật tự màn (Screen-Order Inference)** | Đưa N ảnh xáo trộn + mục tiêu → máy tự xếp đúng thứ tự rồi sinh hướng dẫn |
| **ReOrder-Tutor / Stage 0** | Tên hệ đề xuất; Stage 0 = bước xếp trật tự màn đặt trước dây chuyền 5 bước |
| **ordering cues (5 dấu hiệu)** | gating (cổng) / nav-affordance (Next-Back) / state-delta (thay đổi trạng thái) / title-progression (tiêu đề tiến triển) / drill-down (đào sâu) |
| **pairwise + Copeland / listwise** | Hỏi từng cặp 'màn nào trước' rồi tổng hợp bằng Copeland score (chính); listwise = ép 1 lần ra cả thứ tự (đối chứng) |
| **Kendall τ-b / partial-order-aware** | Headline đo độ giống thứ tự máy↔vàng; chỉ phạt cặp BẮT BUỘC, cặp tự-do đảo vẫn đúng |
| **ORACLE-ORDER / SELF-ORDER / ordering gap** | Đã sắp đúng (mốc trên) / tự xếp (thật) / hiệu hai cái = giá của việc không biết trật tự |
| **teacher-forcing / Tier A** | Cách đo: mỗi bước cấp màn thật rồi hỏi → chấm độc lập; Tier A = trục tham chiếu chuẩn ngành (không claim ngang leaderboard) |
| **Action-Type / Grounding@14% / Step-SR (Task Success)** | Đúng loại thao tác / điểm bấm lệch ≤14% / đúng cả bước (= hoàn thành tác vụ) |
| **AITW / MobileViews / AndroidControl / ScreenSpot** | Nguồn ngưỡng 14% / 3 dataset dùng (màn-0 / đa bước / đối chứng) |
| **preprint (arXiv) / peer-reviewed / journal** | Đăng kho mở chưa bình duyệt / đã bình duyệt / tạp chí khoa học |
| **ablation / C0–C4 / baseline** | Bóc tách thêm từng bộ phận; C1 = mốc cơ sở |
| **GOAL-ONLY / RANDOM-ORDER** | Đối chứng: che hết ảnh chỉ đưa mục tiêu / xếp ngẫu nhiên làm sàn |
| **BWS / Krippendorff α / Spearman-Kendall** | Người chọn tốt-nhất/tệ-nhất để xếp hạng / đồng thuận người chấm / khớp máy↔người |
| **pre-registration / null result** | Đăng ký giả thuyết (trục τ-b) trước khi chạy / kết quả "không khác biệt" (vẫn là đóng góp nếu giải thích cơ chế) |
| **recall / RAW vs ORACLE** | Bộ dò tìm ra bao nhiêu nút thật / số thật vs số giả định bộ dò hoàn hảo |
| **kill-test (K1, KN, KZ', KB)** | Phép thử nhanh tuần 1: K1 đo recall (cứng), KN đếm histogram độ dài, KZ' rà prior-art xếp ảnh, KB chống lộ thứ tự |
| **prior-art xếp ảnh** | Sort-Story (EMNLP 2016), Sequencing Multimodal Manuals (ACL 2022), RankGPT (EMNLP 2023) — dòng dõi thừa nhận |
| **world-model (AGENT-NSI)** | Mô hình "tưởng tượng" màn kế, cần huấn luyện — để future-work |

*Mạch: Bài toán → Dữ liệu (+ví dụ thật) → Pipeline → Metric → Khả thi. Mọi thuật ngữ giải thích tại lần đầu; record thật ở Phần (A) có nguồn.*
