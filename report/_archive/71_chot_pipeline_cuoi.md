# report/71 — CHỐT pipeline cuối cùng (bản không-áp-lực-thời-gian)

> Bối cảnh: luận văn train Qwen2.5-VL-3B (SFT-LoRA) sinh hướng dẫn sử dụng app cho người đọc, chưng cất từ gpt-4o-mini trên data đã lọc bịa. Thiết kế pre-register (report/56) chỉ có MỘT trục đo = độ trung thực (không bịa tên nút, no-gold). Report này chốt: có thêm "trục ĐÚNG" (đo hướng dẫn có dẫn tới đích không, bằng gold AndroidControl) hay không, và toàn bộ pipeline cuối. Ngày: 2026-07-18.

## Phán quyết 1 dòng

**Trục ĐÚNG = THÊM-CÓ-ĐIỀU-KIỆN** — kỹ thuật đã chứng minh map ĐƯỢC (Mũi 2: lấy toạ độ gold → tra ngược accessibility tree ra TÊN nút thật → so với tên model nói, KHÔNG cần bộ grounder hay tự bịa toạ độ), nên trục này **không bất khả thi**; nhưng nó vào luận văn ở **vai phụ, khai hậu-đăng-ký (exploratory), làm SAU** ba việc rẻ hơn — chứ **KHÔNG** làm trục xác-nhận chính của mùa này.

Thứ tự ưu tiên chốt (theo Mũi 4): **B (đọc tay fallback) > A (thêm app test) > trục ĐÚNG bản thu gọn > C (đường-cong-bịa nhiều teacher)**.

---

## Pipeline cuối — sơ đồ + mô tả

```
                         ┌─────────────────────────────────────────────┐
                         │  A. XÂY DATA (chưng cất có lọc bịa) — GIỮ    │
                         └─────────────────────────────────────────────┘
  ảnh màn MobileViews ─┐
  + câu hỏi use-case   ├─► teacher gpt-4o-mini sinh hướng dẫn thô
  (đã khử tên nút)     ┘            │
                                    ▼
                        ┌───────────────────────────┐
                        │ LỚP LỌC BỊA (so tên nút    │   GIỮ
                        │ với View Hierarchy;         │
                        │ nomic-embed, ngưỡng τ)      │
                        └───────────────────────────┘
                            │ khớp (≥τ)      │ bịa (<τ)
                            ▼                ▼
                      giữ nguyên bước    viết lại thành MÔ TẢ
                                          chung chung = "fallback"
                                    │
                                    ▼
                        DATA-LỌC   ⇄  (đối chứng) DATA-THÔ (không lọc)
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ B. TRAIN — GIỮ                 │
                    │ Qwen2.5-VL-3B, QLoRA r=8/α=16, │
                    │ freeze-vision, LLaMA-Factory   │
                    └───────────────────────────────┘
                       │                        │
              Student-LỌC              Student-THÔ (đối chứng Tier 1)
                       │
        ┌──────────────┴───────────────────────────────────────────────┐
        ▼                          ▼                          ▼
┌────────────────┐   ┌────────────────────────┐   ┌────────────────────────┐
│ TRỤC 1: TRUNG  │   │ TRỤC 2 (phụ, có sẵn):  │   │ TRỤC 3 = "ĐÚNG"        │
│ THỰC — GIỮ     │   │ HỮU-ÍCH — VÁ (nâng)    │   │ THÊM-CÓ-ĐIỀU-KIỆN      │
│ (trụ chính)    │   │                        │   │ (phụ, hậu-đăng-ký)     │
│                │   │                        │   │                        │
│ Tier 1: LỌC vs │   │ B) đọc tay 30-50 câu   │   │ Step-SR-theo-tên trên  │
│  THÔ (VH bật)  │   │    fallback: "chung    │   │ AndroidControl:        │
│ Tier 2: Student│   │    chung" có DÙNG ĐƯỢC │   │  gold(x,y) → a11y-tree │
│  vs Teacher    │   │    không? (kill giả    │   │  → TÊN nút thật →      │
│  BASE, TẮT VH  │   │    định load-bearing)  │   │  so tên model nói      │
│                │   │                        │   │  (teacher-forced,      │
│ đo = so VH,    │   │ đo = người chấm +      │   │  từng-bước-độc-lập)    │
│ KHÔNG gold     │   │ metric mạch-lạc §9/56  │   │  ĐO = có GOLD          │
│ sign-flip G=12 │   │                        │   │  (+ risk-coverage nếu  │
│                │   │                        │   │   dựng được ĐƯỜNG)     │
└────────────────┘   └────────────────────────┘   └────────────────────────┘

LUẬT VÀNG (chống leak) — GIỮ NGUYÊN, mở rộng sang trục 3:
  lúc SINH chỉ nạp (ảnh + goal đã khử tên nút). KHÔNG nạp VH,
  KHÔNG nạp low-level step_instruction, KHÔNG nạp action gold,
  KHÔNG nạp a11y-tree. Tất cả những thứ đó CHỈ vào lúc CHẤM.
```

**Đọc sơ đồ:**
- **GIỮ nguyên** (đã pre-register report/56, không đụng): toàn bộ khối xây-data + lọc bịa + train + Trục 1 (trung thực, Tier 1/Tier 2, sign-flip G=12). Đây là xương sống, không thay đổi một chữ.
- **VÁ NHỎ (nâng cái đã có)**: Trục 2 hữu-ích. report/56 §9 đã có "phép-đo-phụ hữu-ích/mạch-lạc" nhưng mờ; giờ nâng thành việc-B cụ thể (đọc tay 30-50 câu fallback) để kill giả định "mô tả chung chung vẫn dùng được".
- **THÊM MỚI (có điều kiện)**: Trục 3 = ĐÚNG. Chạy trên dataset KHÁC (AndroidControl), app khác, **trực giao** với Tier 2 nên không đụng tính-sạch của trụ chính (Mũi 1 điểm 5). Vào ở vai phụ + khai hậu-đăng-ký.

---

## Bộ thước đo cuối

| Trục | Đo cái gì | Có GOLD? | Dụng cụ đo | Vai | Trạng thái |
|---|---|---|---|---|---|
| **1. Trung thực** (Tier 1) | Student-LỌC bịa ít hơn Student-THÔ? (VH vẫn bật lúc suy luận) | Không (so VH) | so tên nút vs VH (bge-m3 chấm độc lập, LLM-judge khác họ) | lưới an toàn, gần chắc dương | GIỮ, pre-registered |
| **1. Trung thực** (Tier 2) | Student bịa ít hơn Teacher-BASE khi **TẮT VH** lúc suy luận? | Không (so VH) | như trên, sign-flip exact G=12 | **trụ chính**, có thể null | GIỮ, pre-registered |
| **2. Hữu-ích** | Câu "fallback" (mô tả chung chung) có thật sự dùng được cho người, hay là "vô dụng lịch sự"? | Không | người đọc chấm 30-50 câu + metric mạch-lạc | **kill-test giả định load-bearing** | VÁ (nâng từ §9), làm TRƯỚC |
| **3. ĐÚNG** (Step-SR-theo-tên) | Bước model nói có gọi ĐÚNG loại thao tác + ĐÚNG tên nút mà thao tác đúng thật sự chạm? | **CÓ** (AndroidControl) | gold(x,y) → tra a11y-tree ra tên → so tên | phụ, bằng chứng độc-lập lấp lỗ "faithful-mà-vô-dụng" | THÊM-CÓ-ĐK, hậu-đăng-ký |
| **3b. Risk-coverage/AURC** (tuỳ chọn của trục 3) | Fallback né ĐÚNG CHỖ (bước sẽ-sai) hay né đúng TẦN SUẤT? | CÓ (dựa nhãn đúng/sai của 3) | đường risk-coverage, so oracle vs random abstain | phụ của phụ | CHỈ nếu dựng được ĐƯỜNG (xem rủi ro) |

Ghi chú bắt buộc khi in:
- Trục 1 vẫn là **headline** và là chỗ quyết định sống-chết. Trục 3 KHÔNG thay thế nó.
- Trục 3 phải khai thẳng là **"biến thể Step-SR theo tên" (name-grounded variant of relaxed accuracy)**, KHÔNG gọi tắt "Step-SR" trần, KHÔNG claim ngang leaderboard toạ-độ (Mũi 2 điểm 3 + rủi ro).

---

## Vì sao chốt vậy (bằng chứng từ 4 mũi)

**Quyết định 1 — Trục ĐÚNG khả thi về kỹ thuật (nên KHÔNG bỏ hẳn). Neo: Mũi 2.**
Đây là bản lề. Câu hỏi khả-thi lớn nhất là "hướng dẫn-bằng-lời (tên nút) có so được với gold-thao-tác-máy (x,y) không". Mũi 2 trả lời **CÓ**, bằng đúng chiều ngược của grounding: gold click chỉ có (x,y) trần, nhưng mỗi bước AndroidControl còn lưu **accessibility tree** với node có `text`, `content_description`, `bounds_in_screen`, `is_clickable`. Tra (x,y) gold → tìm node clickable chứa điểm đó → đọc `text`/`content_description` = **TÊN nút thật** mà thao tác đúng đã chạm → so với tên model nói. Cách này né hoàn toàn bộ grounder (chính là control M5 hay sai mà Mũi 1 lo), và khớp đúng bản chất output-cho-người. Vì Mũi 2 nói MAP ĐƯỢC, ta không bỏ trục này — nhưng cũng vì nó, ta biết cái giá thật nằm ở đâu (xem QĐ 2, 3).

**Quyết định 2 — nhưng để ở vai PHỤ + hậu-đăng-ký, KHÔNG làm trục xác-nhận chính. Neo: Mũi 1 + Mũi 4.**
- **Lệch task (confound):** model train trên data distill-từ-MobileViews (màn tĩnh, sinh hướng dẫn cho người), chấm trên AndroidControl (tác vụ điều-khiển-agent, người thật bấm Pixel tiến tới goal) = zero-shot xuyên phân bố. Step-SR thấp có thể do dịch-chuyển-phân-bố chứ không phải do hướng dẫn kém (Mũi 1 điểm 3). → chỉ là proxy của độ-đúng, không phải bằng chứng trực tiếp.
- **Mâu thuẫn framing:** headline là "đo trung thực KHÔNG cần gold"; lôi gold về dễ bị vặn "vậy rốt cuộc vẫn cần gold à". Mũi 1 điểm 2 công nhận đây là đánh-đổi thật (giữ story sạch nhưng hở lỗ H4, hay bịt H4 nhưng mờ story), và cả hai mũi đều thừa nhận nếu KHAI RÕ mỗi trục dùng nguồn gì thì báo song song no-gold + có-gold trên dataset khác nhau **không** phải lỗi thiết kế — chỉ là vấn đề trình bày. → giải được bằng cách đặt trục 3 ở vai phụ + hậu-đăng-ký, không nhập vào family Holm của trục chính.
- **Chi phí thật:** phải dựng + validate một bộ đo THỨ HAI (parser trích loại-thao-tác/tên-đích từ văn xuôi + hàm point-in-bbox lookup trên a11y tree + chính bộ đo này phải qua bơm-lỗi của riêng nó, nếu không thì Step-SR là tự-khen — Sai et al. EMNLP 2021). Mũi 1 điểm 1 + Mũi 4 gọi đúng đây là scope creep, không phải "một cột thêm vào bảng".

**Quyết định 3 — thứ tự: B (đọc tay) trước, rồi A (thêm app), rồi trục ĐÚNG thu gọn, C ghép kèm. Neo: Mũi 4.**
- **B > mọi thứ** vì nó kill giả định load-bearing rẻ nhất: toàn bộ lý lẽ "viết lại bịa thành mô tả an toàn" GIẢ ĐỊNH câu đó dùng được — chưa ai xác nhận. Nếu fallback là "vô dụng lịch sự" thì ngay cả Tier 2 PASS cũng rỗng nghĩa (chỉ chứng minh model né NHIỀU hơn). Free, chặn failure-mode sâu nhất.
- **A (thêm app test)** là đòn DUY NHẤT tác động thẳng vào rủi ro số 1 (Tier 2 null vì G=12). Nhưng bị hãm bởi căn-bậc-hai: 12→24 app chỉ giảm MDE ~29%, muốn halve cần ~48 app; nếu Δ thật bé thì không app-count nào cứu (Mũi 4).
- **Trục ĐÚNG thu gọn** làm sau, dạng no-harm ("student-LỌC có giữ Step-SR-theo-tên ≈ student-THÔ không" = lọc không phá độ đúng) — rẻ nhất, phòng thủ nhất.
- **C (đo bịa ≥1 teacher đời mới)** ghép vào pilot MDE (~$1-2), chỉ để thủ đòn "sao không teacher 2026 xịn" — giá trị chiến lược thấp nhất nhưng rẻ nên làm kèm.

**Quyết định 4 — risk-coverage/AURC là HỢP LỆ với gold, nhưng chỉ khi dựng được ĐƯỜNG. Neo: Mũi 3.**
Chuỗi lập luận "(c) gold làm risk-coverage hợp lệ" **đúng và có tiền lệ vững**: trong selective prediction chuẩn (Geifman–El-Yaniv; El-Yaniv & Wiener), "risk" được định nghĩa chính thức là tỉ-lệ-lỗi-so-với-NHÃN-THẬT trên tập được-chấp-nhận. Vòng A bác risk-coverage đo bằng proxy-VH là ĐÚNG (proxy tự-quy-chiếu không phải đúng/sai thật); nhưng một khi risk = "bước cụ-thể-mà-SAI so với gold AndroidControl" thì rơi thẳng vào định nghĩa kinh điển → AURC/coverage-risk chính danh. **NHƯNG** (điểm yếu lớn nhất Mũi 3 nêu): trong thiết kế hiện tại fallback là quyết định NHỊ PHÂN do model tự sinh → chỉ cho MỘT điểm (coverage, risk), KHÔNG phải một ĐƯỜNG, AURC không tính được. Muốn thành đường phải có điểm-tin-cậy quét ngưỡng được (điểm tương đồng matcher với VH, hoặc logprob token tên-nút). Nếu không cài thêm cái đó thì **khiêm tốn gọi "một điểm selective-risk", ĐỪNG gọi "đường/AURC"**.

**Chỗ bằng chứng YẾU / phân biệt peer-reviewed vs preprint (trung thực):**
- Peer-reviewed AN TOÀN để trích: AndroidControl = Li et al. NeurIPS 2024 D&B (arXiv 2406.03679); SeeClick ACL 2024; OS-Atlas/ScreenSpot-v2 ICLR 2025; SelectiveNet Geifman–El-Yaniv **ICML 2019** (đã verify ở Mũi 3, PMLR v97); "Overcoming Common Flaws in Evaluation of Selective Classification" NeurIPS 2024; Ren et al. ICLR 2023 (selective ở mức SINH); Sai et al. EMNLP 2021 (validate metric bằng perturbation); AITW NeurIPS 2023 (ngưỡng dung sai 14%).
- **CHƯA verify — ĐỪNG trích như trụ cho tới khi đọc bản gốc:** Geifman–El-Yaniv **NeurIPS 2017** (Mũi 4 nhớ nhưng chưa verify phiên này — dùng bản ICML 2019 đã verify thay); **CAP ACML 2025 / PMLR 304** (Mũi 3 xác nhận venue có thật nhưng CAP dùng conformal+RL học chính sách abstain, KHÔNG phải "risk=Step-SR" → nếu trích thì chỉ như "bằng chứng selective/abstain đang là dòng sống cho VLM 2025", KHÔNG như "họ làm y hệt ta"); AURC characterization arXiv 2410.15361 = **preprint**, chưa xác nhận bình-duyệt.
- **Số CHƯA đếm tận cùng:** phân bố action per-step thật (tỉ lệ click trong TỔNG bước, tỉ lệ gold-element CÓ text label, tỉ lệ step_id=0) — Mũi 1 ước "30-50% bước dùng được" nhưng khai rõ là ước lượng, phải `dg2_*.py` đếm lại. Mẫu số trục 3 có thể co đáng kể vì chỉ click/long_press/input_text có tên để kiểm; scroll/wait/home/back không có tên nút.

---

## Cái phải hỏi thầy (không tự quyết)

1. **Có chấp nhận thêm trục ĐÚNG dạng phụ + hậu-đăng-ký không?** Vì nó đụng bộ TN đã commit (report/56). Hợp lệ CHỈ KHI làm TRƯỚC khi nhìn kết quả test + khai thẳng exploratory + được thầy đồng ý. Làm sai thứ tự = mất tính pre-registered, thiệt hại uy tín > lợi ích.
2. **Trục hữu-ích (B): dừng ở đọc-tay-một-người (kill giả định) hay nâng thành mẫu-người-nhỏ có κ giữa người chấm (thành con số khai được)?** Cái sau tốn vài chục giờ người + cần thầy cho phép.
3. **Có cho mở rộng app test (A) không, và nếu có thì rút từ pool nào?** Nếu rút từ pool 30 QC thì phải QC thêm app tới cùng chuẩn (không "free"); nếu total pool cố định thì test↑ ⇒ train↓ ⇒ student yếu đi.
4. **Chấp nhận khả năng Step-SR-theo-tên của student-LỌC THẤP** (vì model tối ưu để hedge, không để hành-động) → lộ ra "model trung thực = agent tệ hơn"? Cần thống nhất trước cách reframe (no-harm/tradeoff) TRƯỚC khi chạy.

---

## PLAN — làm gì, theo thứ tự

| Bước | Việc | Free / tốn tiền | Phụ thuộc | Ước công sức |
|---|---|---|---|---|
| **0** | **K1 — kill-test matcher hai chiều** (đo precision/recall lớp lọc bịa trên 80-120 cặp gán tay; freeze τ). Việc ĐẦU TIÊN, chạy NGAY. | Free (local) | không | 0.5-1 ngày |
| 1 | **B — đọc tay 30-50 câu fallback**: "mô tả chung chung" có dùng được không? Đây là kill-test giả định load-bearing. | Free | K1 xong (có data fallback) | 0.5 ngày |
| 2 | **Pilot MDE** (5-10 app) → điền ô `[MDE = ___ pp]` ở report/56 → **commit pre-reg lần 2**. Ghép luôn **C** (đo bịa ≥1 teacher đời mới, ~$1-2) vào pilot này. | Tốn ~$1-2 API | K1 | 1 ngày |
| **⛳ HỎI THẦY** | Trình 4 câu ở mục trên + kết quả B. Chốt: có làm A / trục ĐÚNG không, mức độ nào. **Không chạy bước 3-6 trước khi thầy duyệt.** | — | bước 0-2 | gặp thầy |
| 3 | Nếu thầy OK **A**: QC thêm app test tới cùng chuẩn → nới split (làm TRƯỚC khi nhìn kết quả test, khai trong pre-reg). | Tốn API (teacher-gen + student + chấm) | duyệt thầy | 2-4 ngày |
| 4 | Teacher BASE → build data-LỌC + data-THÔ → **train Student-LỌC + Student-THÔ** (QLoRA). | Tốn Colab GPU | bước 2 (pre-reg chốt) | 3-5 ngày |
| 5 | Chạy **Trục 1** (Tier 1 + Tier 2, sign-flip). Đây là trụ chính, chạy dù các trục khác ra sao. | Tốn GPU/API chấm | bước 4 | 2-3 ngày |
| 6 | Nếu thầy OK **trục ĐÚNG**: (i) fetch bản GỐC AndroidControl (google-research/android_control — bản smolagents đang dùng đã bị lược còn goal+coords, KHÔNG có a11y-tree); (ii) viết parser proto `android_accessibility_forest_pb2` + hàm point-in-bbox lookup; (iii) **kiểm 5-10 bước bằng mắt** xác nhận (x,y) action và bbox a11y cùng khung toạ độ; (iv) đo **sai số của chính cầu trích+lookup** (một X5 thu nhỏ) — nếu tầng đó tự sai >~15-20% thì Step-SR vô nghĩa, **DỪNG trục này**; (v) nếu qua, chạy Step-SR-theo-tên teacher-forced trên click/long_press. | Free lúc chấm (local); fetch data tốn băng thông | duyệt thầy + bước 4 | 3-5 ngày |
| 7 | (Tuỳ chọn của bước 6) Nếu có điểm-tin-cậy quét ngưỡng được → dựng ĐƯỜNG risk-coverage + AURC, so oracle vs random abstain. Nếu không → chỉ báo "một điểm selective-risk". | Free (local) | bước 6 qua | 1-2 ngày |

Mốc "hỏi thầy" nằm **sau bước 2, trước bước 3** — tức là sau khi đã có (a) precision/recall matcher, (b) kết quả đọc-tay hữu-ích, (c) MDE thật. Ba con số đó cho thầy quyết định có đáng mở A / trục ĐÚNG không.

---

## Rủi ro của chính bản chốt này

1. **Mũi 2 có thể lạc quan ở khâu khung toạ độ.** Toàn bộ tính khả-thi của trục ĐÚNG dựa trên giả định action `(x,y)` và `bounds_in_screen` của a11y node cùng khung pixel. Nếu một bên chuẩn hoá [0,1] còn bên kia pixel (hoặc lệch do resize ảnh) thì lookup sai → cùng loại lỗi "lệch khung toạ độ MobileViews" ở report/44 §8. **Bắt buộc kiểm mắt 5-10 bước (bước 6-iii) trước khi tin bất kỳ số nào.** Nếu khâu này hỏng, trục ĐÚNG sập — và đó là lý do nó nằm SAU mốc hỏi thầy, không phải trước.

2. **Mẫu số trục ĐÚNG có thể co quá nhỏ.** Chỉ click/long_press/input_text có tên để kiểm; node tại (x,y) có thể là icon-only rỗng cả `text` lẫn `content_description` (>77% app thiếu nhãn a11y — Chen ICSE 2020). Cộng ràng buộc tiến-độ (chỉ so công bằng ở step_id=0) có thể co mẫu về mức yếu thống kê. **Phải đếm trước (một cổng kiểu K) — con số "30-50%" hiện chỉ là ước lượng chưa verify.**

3. **Trục ĐÚNG có thể tự-bắn-chân.** Student-LỌC (tối ưu để trung thực/hedge) có thể ra Step-SR-theo-tên THẤP hơn Student-THÔ → lộ "model trung thực = agent tệ hơn". Reframe được thành no-harm/tradeoff CHỈ NẾU LỌC ≈ RAW; nếu LỌC < RAW rõ rệt thì đó là negative thật. Phải chấp nhận khả năng này TRƯỚC khi chạy (câu hỏi thầy #4).

4. **Risk-coverage dễ bị overclaim.** Nếu chỉ có một điểm mà gọi "đường/AURC" là sai kỹ thuật (Mũi 3 điểm yếu #1). Và một hướng dẫn toàn-fallback có risk=0/coverage=0 "vô dụng nhưng đẹp trên đường" — phải báo tại coverage tối thiểu có nghĩa, nếu không lại rơi đúng lỗ "trung thực cao mà vô dụng" mà trục này định lấp.

5. **Trục hữu-ích (B) có thể không thành "con số headline".** Đọc-tay-một-người đủ để KILL giả định xấu, nhưng chưa đủ làm bằng chứng dương mạnh (cần κ giữa người chấm). Đừng bán quá lời — nó là lưới an toàn logic, không phải kết quả khoe được.

6. **Rủi ro pre-registration là rủi ro uy tín, không phải kỹ thuật.** A và trục ĐÚNG đều đụng bộ TN đã commit. Chỉ hợp lệ khi làm TRƯỚC khi nhìn kết quả test + khai hậu-đăng-ký + bàn thầy. Làm sai thứ tự thì mất luôn cái giá trị lớn nhất của thiết kế này (tính pre-registered) — thiệt hơn lợi. Đây là lý do PLAN khoá cứng mốc hỏi-thầy trước mọi bước mở rộng.

7. **Bản chốt này giả định lịch không-áp-lực.** Nếu thực tế vẫn kẹt 2 bài + train trước 15/8 với 1 GPU một mình, thì ngay cả "trục ĐÚNG thu gọn" cũng nên hoãn sang bài mở rộng tiếng Anh (nơi nhánh nhiều-màn cũng nằm) — chỉ giữ bước 0-2 + Trục 1 là sàn chắc. Mũi 1 và Mũi 4 đều nghiêng phương án này nếu thời gian eo hẹp.
