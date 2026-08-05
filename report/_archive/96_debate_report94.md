# report/96 — Debate report/94: pipeline + metric đã đủ hợp lý chưa

> Ngày 2026-07-21. Ba góc soi độc lập (SOI 1 pipeline-số-gốc · SOI 2 model/chống-vòng-vo · SOI 3 lật-từng-lỗ-report/90) + verify harness. Đối tượng: report/94 (bản đã sửa sau report/90). Đối chiếu report/90, report/93.

---

## Phán quyết 1 dòng

**CẦN VÁ VÀI CHỖ** — executability là bước tiến THẬT (hoà tan phần lớn Phần 1 của report/90 từ gốc, không phải dời chỗ), đủ hợp lý để đi tiếp; nhưng nó **chưa đủ làm trụ chính một mình**: mang theo 1-2 lỗi đo thật chưa ai khai, để nguyên 2 lỗ nặng ngoài Phần 1, và cả trục treo trên một cổng CHƯA chạy. Không phải "còn lỗ nặng" kiểu phải làm lại, nhưng cũng chưa "sạch".

---

## report/94 đã tiến bộ gì thật — công nhận

Cả ba góc soi đồng thuận đây là vá thật, không phải đổi nhãn:

- **Bỏ hẳn cái nền gây bệnh.** Thước cũ (so chuỗi Jaccard trên action∧target) bị report/90 §1.1-1.2 vạch là cổng AUC giả (perturbation tự-dựng tái dùng `target_of()`) + rớt AUC 0.34 trên 51 ca paraphrase thật. report/94 §5.1 khai thẳng con số 0.34 và **vứt thước**. Đây là câu trả lời đúng cho đòn nặng nhất.
- **Đòn chạm-tim (§1.3 report/90: headline chỉ đo khớp-giọng-annotator) được vá by-construction.** Grounder ánh xạ *nghĩa → toạ độ*, không thưởng trùng từ vựng gold: "funnel icon" và "Filter button" cùng trỏ về ~(855,2273) → cùng trúng. Lợi-thế-sân-nhà kiểu token-overlap tan.
- **Loạt lỗ Phần 1 khác dissolved:** §1.5 (đích rỗng Next/Back cos=1.0), §1.7 (thưởng câu cộc lốc), phần cha/con của §1.4 — đều biến mất vì không còn tokenize-rồi-so.
- **Chính trực pre-reg tiến bộ.** Bài học report/90 Phần 2 đã ngấm: khai thẳng thước cũ chết + grounder rẻ chỉ 51%; Cổng A/B là cổng **rớt-được-thật**, đặt go/no-go TRƯỚC khi tiêu tiền train (đúng tinh thần Giai đoạn A report/90).
- **Novelty hạ claim đúng hướng** (report/90 §5.1): GuideMe thành động-cơ-nhu-cầu, khai thẳng round-trip mượn từ back-translation + code-gen-test.

---

## Chỗ CÒN HỞ

Phân ba loại: **[LỖI THẬT]** phải sửa · **[TỰ KHAI]** report/94 đã nhận nhưng chưa đóng · **[CHƯA CHẮC]** cơ chế suy luận, xem mục cuối.

| # | Vấn đề | Mức | Vá cụ thể |
|---|---|---|---|
| 1 | **Đảo nghĩa on/off — lỗ §1.4 carry-over, KHÔNG ai khai.** "Turn OFF notifications" và "Turn ON notifications" trỏ **cùng toạ độ công tắc** → executability chấm cả hai executable. §4(b) chỉ kiểm "động từ khớp loại thao-tác" mà on/off cùng là tap. report/90 gọi chiều này "nguy hiểm hơn vì thổi phồng điểm, không triệt tiêu trong hiệu-số". Executability KHÔNG vá được. | **[LỖI THẬT] nặng vừa** | Với toggle: thêm kiểm trạng-thái-đích (on/off) ngoài toạ độ, hoặc khai thẳng executability mù với đảo-nghĩa-toggle + báo tỉ lệ bước toggle. |
| 2 | **Gộp con số click (grounder) với type/scroll (so-khớp cũ) thành một "% executable".** Pilot AC: chỉ ~53% bước là click (100 click/long_press trên 188 quét). Nửa còn lại (type/scroll/navigate/open_app/wait) KHÔNG qua grounder → rơi về so-khớp loại-thao-tác + nội dung = đúng họ thước report/90 vừa lật (§1.4 đảo up/down vẫn khớp; §1.5 đích rỗng). Trụ "mới" chỉ gánh nửa số bước; nửa kia thừa hưởng rủi ro cũ, báo như đại lượng đồng nhất. | **[LỖI THẬT] nặng** | **Tách hai con số**: %exec-click (grounder-kiểm-chứng) và %match-type/scroll (so-khớp) — báo riêng, đừng gộp headline. |
| 3 | **Construct validity người (grounder-trỏ-trúng ≈ người-làm-theo-được) mới là khẩu hiệu, chưa có số, mà Cổng A/B KHÔNG chứa bước kiểm này.** §4 liệt nó ở một dòng bảng nhưng Cổng A chỉ đo grounder-đúng-~80%, Cổng B đo gắn-thành-phần-đâu — cả hai đo *độ chính xác grounder*, không đo *grounder có đo đúng thứ người cần không*. report/90 §C1 đòi nghiên-cứu-nhỏ (91 cặp teacher đã có, free). → construct validity thước MỚI đang ở đúng trạng thái thước CŨ lúc bị lật: được khẳng định, chưa được kiểm, mà PASS/NULL sắp neo lên nó. | **[LỖI THẬT] nặng** | Đưa nghiên-cứu-người 91-cặp vào **Cổng** (không để ở bảng); ĐỪNG hoãn — nó là mỏ neo duy nhất cho cả LLM-judge-hữu-ích lẫn executability. |
| 4 | **Dung sai 14% (~151px) nuốt ~nửa số bước.** Đo trên VH 127 màn MobileViews (1080px, gộp node lồng trùng tâm): TB ~16 nút phân biệt/màn; **55.2% bước có ≥1 nút khác trong đĩa 151px, 31.2% có ≥2**. → câu vớ vẩn/trỏ nhầm nút cạnh vẫn trúng-giả; và bộ trỏ "không câu" cũng trúng cao → **sàn Exec(∅) cao → dải động (Exec(s)−Exec(∅)) bị nén** = đúng nỗi lo report/90 §9 (headline không diễn giải được), chỉ đổi cơ chế. Ví dụ 72−30=42 ở §4 là số bịa lạc quan; sàn thật sẽ cao hơn 30 nhiều. | **[LỖI THẬT] nặng** | **Báo Exec(∅) sàn THẬT trước khi khoe hiệu số**; cân nhắc dung sai chặt hơn hoặc chấm theo nút-gần-nhất-đúng thay vì đĩa. (Caveat: mật độ đo trên MobileViews, chưa đo được AC vì bản HF thiếu bbox.) |
| 5 | **Nhánh control Teacher-STYLE-MATCHED (report/90 §F4 bắt buộc) đã bị bỏ.** report/94 §3 liệt đúng 3 model, không có nhánh style-matched. Việc bỏ *một phần* chính đáng (executability khử token-style), NHƯNG còn **lợi-thế-cấu-trúc**: Student SFT trên gold AC học luôn độ-hạt-bước benchmark (gold trung vị 6 từ, một-thao-tác-một-bước); gpt-4o-mini zero-shot không biết → sinh câu gộp/dài → bị ép vào ranh-giới-bước chưa từng học. Một phần "Student > Teacher" đo *thuộc-bài-phân-đoạn*, không phải *hướng dẫn tốt hơn*. report/90 §F4: "không có nhánh này thì headline không diễn giải được." | **[LỖI THẬT] nặng vừa** | Giữ lại control STYLE-MATCHED rẻ (teacher bị ép về giọng/độ-hạt gold) làm dây an toàn; dẫn claim chính bằng **ablation nội bộ** (Student-trơn vs Student+thành-phần, cùng base, sạch), để "hơn gpt-4o-mini" làm phụ. |
| 6 | **Tín-hiệu-train ≡ phép-toán-eval — coupling chặt hơn ẩn dụ "nomic lọc / bge-m3 chấm" mà thiết kế viện.** RFT/STaR lọc câu tự sinh bằng "grounder_train trỏ trong dung sai gold-coord"; executability chấm bằng "grounder_eval trỏ trong dung sai gold-coord" = **cùng một operationalization**, chỉ tráo checkpoint. Reward-hack "viết mơ hồ cho bộ-trỏ dễ khớp" (report/95 tự nêu) **chuyển giao qua cả hai grounder** (cùng bám salient gần nhất). Hai grounder "khác họ" chưa ai đo agreement chéo — phần độc-lập-còn-lại chính là toàn bộ ngân sách-trung-thực của thước. | **[LỖI THẬT] nặng nếu chọn RFT** | Cổng A báo thêm **agreement chéo grounder_train vs grounder_eval**; biến đối-trọng-hữu-ích thành **cổng cứng ≥ ngưỡng** (không phải "không được tụt"). Đường sạch nhất: chọn thành phần **DPO-âm-bản-từ-VH** — tín-hiệu-train="tên nút có trong VH" khác THẬT với eval. |
| 7 | **faithfulness MDE ~32pp bị demote-bằng-nhãn, không khai lực.** report/90 §3.4 rõ: G=12, 3.077×0.362/√12 = 32.2pp, gấp đôi ngưỡng 15-20 → null không đọc được gì. report/94 hạ faithfulness xuống "trục phụ" (phản ứng hợp lý) NHƯNG không nêu con số 32pp, không nói "underpowered/null không diễn giải", ngược lại trưng nó với công thức + ví dụ chạy tay (§4 Thước 2) **ngang hàng executability**. Đổi nhãn ≠ khai lực. | **[LỖI THẬT] nhẹ-vừa** | Khai thẳng "faithfulness chỉ báo mô tả, MDE~32pp, null không kiểm định"; đừng để nó trông như trục đo thật ngang executability. |
| 8 | **coverage/F1/thứ-tự mâu thuẫn với teacher-forced-một-câu-mỗi-bước.** §4 bảng đầu liệt "coverage + F1 + thứ tự" (thuộc chế độ sinh-tự-do rồi gióng-tập, có Hungarian) nhưng §4(a) chốt teacher-forced per-step. Hai khung chấm mâu thuẫn trong cùng mục; nếu `coverage()` cũ còn dùng cho F1 thì lỗ §1.6 (một gold phủ gold khác) sống lại ở nhánh đó. | **[LỖI THẬT] nhẹ (làm rõ)** | Chốt một khung chấm; bỏ coverage/F1/order khỏi bảng nếu đã teacher-forced per-step, hoặc mô tả rõ cơ chế F1. |
| 9 | **Novelty: chưa quét dòng gần nhất + tiền đề load-bearing chưa verify.** §311 trích GuideMe/AskEase/Aguvis/OS-Genesis nhưng **không nhắc Widget Captioning (EMNLP 2020) / Screen2Words (UIST 2021)** — đúng dòng "sinh-văn-cho-người-trên-GUI" gần nhất report/90 §5.2 đã dặn phân định. Claim "benchmark đầu tiên" hở đúng chỗ. Và "first **trained** small model" treo trên GuideMe-KHÔNG-train, mà §313 tự khai chưa lấy được full-text (ACM chặn). | **[TỰ KHAI phần 2] + [LỖI THẬT phần 1]** | Thêm phân định Widget Captioning + Screen2Words; đóng tiền đề GuideMe-không-train trước khi khoá framing. |
| 10 | **Grounder rẻ đã lỗi-trung-vị VƯỢT dung sai; cả trục treo trên Cổng A chưa chạy.** `hit_14=0.513` nhưng `median_dist=0.150 > 0.14` (n=76) — nửa số câu GOLD (đúng tuyệt đối) đã trượt. Đường lui "chỉ chấm nút-có-chữ" lại chính là vùng thước cũ vốn chạy được → nếu Cổng A rớt, đóng góp đo-lường co gần bằng 0. | **[TỰ KHAI]** (§5.2, §6 report/94 đã nhận) | Rủi ro treo, không phải lỗi thiết kế; chạy Cổng A trên grounder chuyên trước mọi thứ. |
| 11 | **Khả thi: giữ CẢ HAI bài + RFT + 2-grounder + 3-4 model mâu thuẫn kiểm kê report/90 §7.** Chưa script train, chưa config LLaMA-Factory, AC train-split ~13k ep + ảnh chưa tải, matcher faithfulness chưa build, thước vừa sập phải dựng lại, chưa gặp thầy. Mỗi khoá chống-circular thêm cho đúng lại làm build đắt hơn. report/90 §7 đã chốt "FAIR 15/8 gần chắc trượt, quyết bỏ/giữ NGAY". report/94 §9 vẫn "giữ cả hai + ~$60-70 + lịch nhẹ" — mâu thuẫn chưa gỡ. | **[LỖI THẬT] về lịch** | Cắt về bản khả thi: VCL trước (30/8), thành phần **DPO-faithfulness** (né yêu-cầu-hai-grounder), MỘT grounder, 2-3 model. Quyết bỏ/giữ FAIR tuần này. |

---

## Câu thủ / việc phải làm TRƯỚC khi train

Ba việc rẻ để executability đủ tư cách làm trụ chính (đều làm được không tốn GPU train):

1. **Đưa construct-validity-người vào cổng** (không để ở bảng): 91 cặp teacher đã có sẵn, free — nối grounder-trúng với người-làm-theo-được. Đây là mỏ neo duy nhất; **đừng hoãn**.
2. **Báo Exec(∅) sàn THẬT trước khi khoe hiệu số**, và **tách con số click (grounder) khỏi type/scroll (so-khớp)** — không gộp thành một "% executable".
3. **Chốt một thành phần MẶC ĐỊNH = DPO-âm-bản-từ-VH** đem trình thầy (rẻ, tất định, chống-circular sạch vì train-signal=VH khác eval-signal=coord, nhắm đúng trục faithfulness có room đo được K2/VH-coverage 0.624). Khung Cổng B thành "có thể nâng lên RFT nếu đủ điều-kiện agreement-grounder + neo-người". Đừng bê nguyên menu 11 ứng viên ra hội đồng — đóng góp trung tâm không nên là ô trống.

Câu thủ trước hội đồng:
- **HOÀ chỉ đậu nếu trụ đánh giá đã dựng lại + validate xong** — mà trụ vừa sập một lần (report/90/92) và neo-người đang hoãn. Câu hỏi 3 gặp thầy phải hỏi KÈM điều kiện "trụ 2 phải vững đã". "Hoà kèm lợi-thế-cấu-trúc" bị hội đồng tinh ý đọc là dưới cơ.
- Chốt **luật-quyết-thành-phần thành hàm tất định** TRƯỚC khi nhìn số Cổng B (report/93 §51 mới map tới *nhóm*, còn researcher-degrees-of-freedom).

---

## Chỗ chưa đủ dữ kiện để kết luận

- **Đảo nghĩa on/off (#1):** suy luận grounder trỏ cùng toạ độ cho toggle-một-nút; UI tách nút on/off riêng thì phân biệt được — chưa chạy grounder thật xác nhận. Với toggle-một-nút (phổ biến) thì lỗ chắc chắn.
- **Mật độ 55%/1.24 nút-cạnh (#4):** đo trên MobileViews (127 màn, đo faithfulness), KHÔNG phải AndroidControl (bản HF local thiếu bbox phần tử) — chỉ báo hợp lý, không phải bằng chứng trực tiếp trên bộ executability thật chạy.
- **Agreement chéo grounder_train vs grounder_eval (#6):** suy từ corpus ScreenSpot chồng lấn, CHƯA đo. Nếu tương quan thấp thì phần (a) nhẹ đi đáng kể — chính là thứ Cổng A nên báo thêm.
- **Dư-lượng-giọng của grounder** (Student ăn điểm nhờ phương ngữ "Tap X" quen grounder): giả thuyết cơ chế, chưa đo; cần một run STYLE-MATCHED để bác/xác nhận — đúng thứ report/94 đã bỏ.
- **Mức confound structure/granularity thật (#5):** suy luận, chưa pilot. Một run gpt-4o-mini teacher-forced trên vài chục ep AC (đếm tỉ lệ trượt do gộp-bước) sẽ định lượng.
- **Grounder chuyên (OS-Atlas/UGround) trên câu dài-giàu-ngữ-cảnh tốt/tệ hơn người thế nào:** câu hỏi thực nghiệm; median_dist=0.15 là của gpt-4o-mini, không suy ra được cho grounder chuyên. Con số grounder n=76/pilot, chưa có CI.
- **coverage/F1 còn dùng code cũ không (#8):** không xác định được từ văn bản — cần tác giả làm rõ.
- **GuideMe có train hay không (#9):** ACM chặn full-text, chưa fetch — ẩn số load-bearing cả report/90 lẫn report/94 đều chưa đóng.
