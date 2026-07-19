# KẾ HOẠCH CHIA ĐỀ TÀI THÀNH 2 BÀI BÁO — FAIR & VCL (trình thầy)

> **Cập nhật 2026-07-12 (bản 3) — CHỐT NỘP CẢ HAI HỘI NGHỊ MÙA NÀY.**
> Bản 1 (24/06): khung cũ prompting, cả 2 bài không model. Bản 2 (07-12 sáng): xoay sang model, giả định "model→VCL nộp trước". **Bản 3 (07-12, sau deep-research venue + trao đổi với user):** đổi lại theo thực tế deadline + độ-fit + mục tiêu user muốn **2 công bố để dễ tốt nghiệp**.
> **Nguồn-sự-thật hướng model:** `report/54` · `report/53` · CLAUDE.md §0. **Nguồn venue:** deep-research `wf_ef24768f` (§0.2 dưới).

---

## §0. BỐI CẢNH & QUYẾT ĐỊNH (đọc trước — ghi lại toàn bộ context đã trao đổi)

### §0.1. Mục tiêu user (đã xác nhận)
- **Muốn NỘP CẢ HAI hội nghị mùa này** (FAIR + VCL) vì nhiều công bố = **điểm cộng để dễ ra tốt nghiệp**.
- Dành **10h/ngày** làm luận văn cho kịp; **không bỏ bước** (giữ nguyên freeze-split + pre-register).
- Hôm nay **12/7/2026**.

### §0.2. Sự thật về 2 venue (deep-research, nguồn chính thức, confidence cao)
| | **FAIR** | **VCL** |
|---|---|---|
| Tên | Hội nghị Quốc gia Nghiên cứu Cơ bản & Ứng dụng CNTT (lần 19) | Hội thảo Quốc gia Ngôn ngữ học Tính toán (HUFLIT + Hội Ngôn ngữ học VN) |
| Deadline | **15/8/2026** (mốc đầu, hay gia hạn) | **~30/8/2026** (user nhớ — ⚠ deep-research CHƯA verify CFP VCL2026, cần kiểm trang HUFLIT) |
| Ngôn ngữ | **CHỈ tiếng Anh** (user xác nhận) | tiếng Việt (hoặc Anh), trình bày tiếng Việt |
| Độ khó | **khó gấp ~2** (user đánh giá), danh giá hơn | dễ hơn |
| Phạm vi | RỘNG toàn CNTT/AI, có track VLM/CV/NLP; kỷ yếu 2025 đã in bài VLM | thuần ngôn-ngữ-học; **không có track CV/VLM** — NHƯNG user xác nhận **"miễn có chất ngôn ngữ là được"** → fit KHÔNG còn là rào cản |
| Chưa có nguồn | tỉ lệ nhận · index Scopus/DBLP · ISBN · chính sách dual-submission | như FAIR (đừng bịa) |

### §0.3. QUYẾT ĐỊNH CHỐT (trục chia mới)
Không nộp trùng 1 bài 2 nơi → tách thành **2 bài nội-dung-khác-nhau**, mỗi bài hợp 1 venue:

- **FAIR (15/8 · tiếng Anh · danh giá) = BÀI MÔ HÌNH (flagship).** Headline = Faithful Distillation: mô hình một-màn Qwen2.5-VL-3B tự-train, kết quả định lượng Tier1/Tier2 trên MobileViews (English). Hợp FAIR (có track VLM). Đây là bài KHÓ + GẤP.
- **VCL (30/8 · tiếng Việt · dễ hơn) = BÀI SINH-HƯỚNG-DẪN-TIẾNG-VIỆT.** Headline = bắt model (train trên English) **sinh hướng dẫn BẰNG TIẾNG VIỆT** trên các màn MobileViews có sẵn + đánh giá không-đáp-án-mẫu; trọng tâm = **chất lượng tiếng Việt + độ trung thực khi chuyển-giao Anh→Việt**. Output tiếng Việt + câu hỏi ngôn-ngữ → hợp VCL. *(Fallback nếu model sinh tiếng Việt kém: lùi về bài PHƯƠNG-PHÁP-ĐÁNH-GIÁ thuần, viết tiếng Việt, thí nghiệm English — xem §3.)*

**⚠ Vì sao ĐỔI khỏi ý "app tiếng Việt" (2026-07-12, sau khi quét dữ liệu):** quét 231 file VH MobileViews local → **chỉ 2 màn có chữ Việt, đều là nội dung lẻ (tên truyện/username), KHÔNG có giao diện app Việt thật**. Không có dataset GUI tiếng Việt công khai + user không tự chụp được → **góc "app tiếng Việt" bất khả thi**. Thay bằng góc "**sinh OUTPUT tiếng Việt trên màn English có sẵn**" — không cần dữ liệu Việt, vẫn giữ chất ngôn ngữ + chuyển-giao. Nút nhắc-tới vẫn so được với VH (tên nút English) nên chấm trung thực tự động vẫn chạy.

**Vì sao 2 bài (không phải kiểu cũ một-màn/nhiều-màn):** nhiều-màn CHƯA kịp build mùa 2026. Chỉ model một-màn kịp → tách theo **ngôn ngữ output + trọng tâm** (FAIR: output-English + train-model · VCL: output-tiếng-Việt + chất-lượng-ngôn-ngữ/đánh-giá).

### §0.4. Fallback BẮT BUỘC (đừng bỏ qua)
**VCL = sàn CHẮC · FAIR = stretch.** Nếu FAIR 15/8 không kịp (model trễ / viết tiếng Anh quá tải) → **BỎ FAIR, GIỮ VCL**, nộp bài mô hình vào FAIR kỳ sau hoặc venue quốc tế. Luận văn vẫn có mô hình dù FAIR ra sao. **Tuyệt đối không để canh bạc FAIR làm hỏng VCL.**

### §0.5. Nhiều-màn (Copeland + min-FAS) đi đâu?
KHÔNG kịp mùa này. Để dành cho **bài tiếng Anh mở rộng sau** (FAIR'2027 / venue quốc tế), gộp với bản mở rộng của bài mô hình. Bộ sắp-thứ-tự học-được (tuỳ chọn, +~$10/+~5-6 ngày — xem §3.4) chỉ làm nếu theo hướng này về sau.

---

## §1. Nguyên tắc chống "trùng"/salami (để CẢ HAI được nhận, không bị soi chẻ-mỏng)

1. **Hai câu hỏi nghiên cứu KHÁC NHAU** + **output khác ngôn ngữ** (FAIR: model sinh tiếng Anh, câu hỏi = train được không · VCL: model sinh tiếng Việt, câu hỏi = chuyển-giao Anh→Việt được không). ⚠ Data nguồn dùng chung (MobileViews English) → overlap cao hơn, bù bằng output + câu hỏi khác.
2. **Không nộp cùng kết quả/bảng số** cho cả hai. FAIR headline = huấn-luyện-mô-hình (Tier1/Tier2); VCL headline = chất-lượng+trung-thực khi xuất tiếng Việt (chuyển-giao).
3. **FAIR ra trước (15/8) ⇒ VCL trích dẫn FAIR** (công trình trước của chính tác giả), nêu rõ phần mới (sinh tiếng Việt + chuyển-giao). *(Nếu FAIR chưa kịp có ID/DOI khi nộp VCL thì trích dạng "under review / manuscript".)*
4. **Phần dùng chung** (mô hình + lớp đối chiếu VH): mỗi bài viết **1 đoạn ngắn + dẫn bài kia**, viết lại câu chữ (VCL tiếng Việt, FAIR tiếng Anh — khác ngôn ngữ nên rủi ro copy thấp).
5. Mỗi bài **tự đứng được**. ⚠️ **Rủi ro salami có thật** (2 bài 1 luận văn nộp cách 2 tuần) — chống bằng khác-dữ-liệu + khác-câu-hỏi + trích-chéo. **Đọc CFP cả 2 venue về chính sách dual-submission/trùng lặp trước khi nộp** (deep-research chưa tra được).

---

## §2. BÀI FAIR (nộp TRƯỚC 15/8 · tiếng Anh · flagship = MÔ HÌNH)

### 2.1. Title (draft — English)
**"Faithful Distillation: Training a Small On-Device Vision-Language Model to Generate Faithful GUI Instructions without Gold References."**

### 2.2. Abstract (draft — English)
> Large VLMs can turn UI screenshots into step-by-step software instructions but frequently **hallucinate non-existent buttons**, misleading users. We present **Faithful Distillation**: we distil from a large teacher (gpt-4o-mini) into a small on-device student (Qwen2.5-VL-3B) via SFT-LoRA, training **only on data whose fabricated button references have been filtered** by matching against the screen's **view hierarchy** and rewritten into faithful generic descriptions. Since no human-authored gold instructions exist, we validate our **reference-free faithfulness metric via automatic perturbation**. We report **two decoupled tiers**: **Tier 1** (student trained on filtered vs raw data, view hierarchy available at inference — safety net) and **Tier 2** (student vs teacher with **view hierarchy switched OFF** at inference, held-out by app — the central question of whether faithfulness *internalises* into the weights). All thresholds are **pre-registered**; null results remain informative.

### 2.3. Đóng góp
- **C1 (headline).** Mô hình nhỏ chạy-trên-máy tự-train qua **Faithful Distillation** (lọc-bịa bằng nguồn ngoài có cấu trúc rồi SFT). *(= yêu cầu train-model của thầy.)*
- **C2.** Giao thức đánh giá no-gold + **kiểm định bằng bơm-lỗi**, chống-vòng-lặp (lọc nomic ≠ chấm bge-m3/judge/token-overlap).
- **C3.** Thiết kế **hai-tầng đăng-ký-trước** (Tier 1 lưới an toàn · Tier 2 nội-tại-hoá khi tắt VH).

### 2.4. Dữ liệu · Thí nghiệm
- MobileViews (English, 18 train/12 test theo app) + ScreenSpot-v2 (đối chứng). Tier 1 + Tier 2 + kiểm-định-bơm-lỗi + thống kê exact sign-flip G=12. Chi tiết: `report/53` §5, `report/54` Phụ lục E.

### 2.5. Vì sao hợp FAIR
Có track VLM/CV/AI; kỷ yếu 2025 đã in bài LLM+VLM; định lượng, tiếng Anh, danh giá → đúng chỗ cho flagship model paper.

---

## §3. BÀI VCL (nộp SAU 30/8 · tiếng Việt · dễ hơn = ỨNG DỤNG TIẾNG VIỆT)

### 3.1. Tựa đề (dự kiến — tiếng Việt)
**"Sinh hướng dẫn sử dụng phần mềm bằng tiếng Việt từ ảnh giao diện và đánh giá không cần đáp án mẫu: khảo sát khả năng chuyển-giao Anh→Việt của mô hình chưng cất trung thực."**

### 3.2. Tóm tắt (nháp — tiếng Việt)
> Sinh hướng dẫn sử dụng phần mềm từ ảnh giao diện gặp hai trở ngại: mô hình dễ **bịa tên nút**, và **không có bộ hướng dẫn mẫu** để chấm. Chúng tôi lấy một mô hình nhỏ chạy-trên-máy (chưng cất trung thực trên dữ liệu tiếng Anh — dẫn bài FAIR) và **yêu cầu nó sinh hướng dẫn BẰNG TIẾNG VIỆT** cho các màn giao diện, rồi đánh giá bằng một **quy trình không-đáp-án-mẫu**: đối chiếu tên nút được nhắc với cấu trúc màn hình (view hierarchy), chấm bằng ba cơ chế khác họ. Câu hỏi trung tâm: **thói quen trung thực học trên tiếng Anh có giữ được khi mô hình xuất tiếng Việt không, và chất lượng tiếng Việt ra sao** (chuyển-giao Anh→Việt). Toàn bộ giả thuyết được đăng-ký-trước; kết quả null vẫn có giá trị.

### 3.3. Đóng góp
- **C1 (headline).** Khảo sát **chuyển-giao ngôn ngữ Anh→Việt**: mô hình trung thực học trên tiếng Anh có sinh được hướng dẫn tiếng Việt trung thực + dùng được không (câu hỏi mới, có thể null).
- **C2.** Quy trình **đánh giá no-gold cho văn bản hướng dẫn tiếng Việt** (đối chiếu VH + 3 cơ chế) — chất ngôn ngữ, hợp VCL.
- **C3.** Phân tích lỗi khi xuất tiếng Việt (bịa nút / lẫn tiếng Anh / dịch sai tên nút) + khuyến nghị.

### 3.4. Dữ liệu · Thí nghiệm
- **KHÔNG cần dữ liệu tiếng Việt** (đã xác nhận: không có bộ GUI tiếng Việt nào + quét MobileViews local 231 file → chỉ 2 màn chữ Việt lẻ, không phải app Việt + user không tự chụp được): dùng **màn MobileViews English có sẵn** (CÓ VH → chấm trung thực tự động; tên nút English vẫn so được dù câu hướng dẫn là tiếng Việt).
- **Việc mới so với FAIR:** prompt model ra **tiếng Việt** (VD 'Chạm vào "Settings"'); đo (a) độ trung thực khi xuất Việt, (b) chất lượng/độ trôi chảy tiếng Việt, (c) so với FAIR (xuất English) để lượng hoá suy giảm do chuyển ngôn ngữ.
- **⚠ SMOKE-TEST BẮT BUỘC tuần 1:** chạy model + prompt tiếng Việt trên ~5 màn. Ra tiếng Việt dùng được → làm bài này. Ra tệ → **fallback: bài PHƯƠNG-PHÁP-ĐÁNH-GIÁ thuần** (viết tiếng Việt, headline = kiểm-định-bơm-lỗi, thí nghiệm English) — vẫn nộp VCL được, chỉ kém chất-Việt + trùng FAIR nhiều hơn (chống bằng headline khác = bơm-lỗi vs Tier1/Tier2).
- *(Tuỳ chọn tương lai, KHÔNG cho VCL mùa này: bộ sắp-thứ-tự nhiều-màn học-được — +~$10, +~5–6 ngày, nhãn free từ gold AndroidControl; chạy cổng K-pair trước xem có đáng. Xem `report/53` §4.4.)*

### 3.5. Vì sao hợp VCL
User xác nhận VCL "**miễn có chất ngôn ngữ là được**"; bài này headline tiếng Việt + đánh giá văn bản → chất ngôn ngữ rõ, hợp track "AI & NLP" / "Ngôn ngữ học tính toán". Dễ hơn + tiếng Việt (viết nhanh) + deadline muộn → an toàn.

---

## §4. Bảng RANH GIỚI — bằng chứng KHÔNG trùng

| Trục | BÀI FAIR (model) | BÀI VCL (tiếng Việt) |
|---|---|---|
| Câu hỏi | **Train** mô hình trung thực (nội-tại-hoá?) | **Chuyển-giao Anh→Việt** của mô hình + đánh giá |
| Dữ liệu | MobileViews English | MobileViews English (dùng chung) — nhưng **OUTPUT khác ngôn ngữ** |
| Ngôn ngữ OUTPUT model | Tiếng Anh | **Tiếng Việt** (điểm khác cốt lõi) |
| Headline | Faithful Distillation + Tier1/Tier2 định lượng | Chất lượng + trung thực khi xuất tiếng Việt + phân tích lỗi |
| Ngôn ngữ bài | Tiếng Anh | Tiếng Việt |
| Venue-fit | track VLM/AI | chất ngôn ngữ (sinh+đánh giá văn bản Việt) |
| Thời điểm | nộp trước 15/8 | nộp sau 30/8 (trích FAIR) |

→ Khác **ngôn ngữ output + câu hỏi (chuyển-giao) + headline + ngôn ngữ bài**. ⚠ Data nguồn dùng chung (đều MobileViews English) → **overlap cao hơn ý "app Việt" cũ**; bù lại bằng output-tiếng-Việt + trọng-tâm-chuyển-giao khác hẳn. Mô hình dùng chung = "công cụ", xử lý theo §1. Nếu fallback về "phương pháp thuần" thì overlap cao nhất → phải tách headline mạnh (bơm-lỗi vs Tier1/Tier2) + đọc kỹ chính sách dual-submission.

---

## §5. Lịch trình (12/7 → 30/8, 10h/ngày)

| Mốc | Việc | Ghi chú |
|---|---|---|
| 12/7 → ~2/8 (~3 tuần) | Build + eval mô hình một-màn | **Giữ freeze-split + pre-register TRƯỚC khi chạy** — gấp mấy cũng không bỏ |
| Tuần 1 | **Smoke-test: model sinh tiếng Việt ~5 màn** | Quyết VCL đi hướng "sinh tiếng Việt" hay fallback "phương pháp thuần" |
| ~2/8 → 15/8 (~13 ngày) | **Viết FAIR (tiếng Anh, model)** — ĐIỂM NGHẼN | Số liệu đã có, chủ yếu viết lại kết quả; 0 buffer |
| ~15/8 → 30/8 (~2 tuần) | Sinh hướng dẫn tiếng Việt trên màn English + đánh giá + **viết VCL (tiếng Việt)** | Không cần thu thập data mới; thoải mái hơn |
| Mốc quyết định 15/8 | Nếu FAIR không kịp → **bỏ FAIR, dồn VCL** (§0.4) | VCL là sàn chắc |

*(Chưa gồm viết luận văn — thêm ~10–15 ngày sau; xem `report/53` §4.4.)*

---

## §6. Rủi ro & cách phòng
| Rủi ro | Phòng |
|---|---|
| Tải nặng (build + 2 bài, 1 tiếng Anh, ~7 tuần) | 10h/ngày; FAIR là điểm nghẽn → viết ngay khi model xong; VCL là fallback nếu FAIR trượt |
| Salami / trùng lặp (2 bài 1 luận văn) | Khác dữ liệu (EN vs VN) + khác câu hỏi + trích chéo; **đọc CFP dual-submission cả 2 venue** |
| FAIR 15/8 quá gấp | Model phải xong ~2/8; nếu trễ → bỏ FAIR giữ VCL, model đi venue sau |
| VCL deadline 30/8 chưa chắc | **Verify CFP VCL2026 trên trang HUFLIT** (deep-research chưa xác nhận) |
| FAIR hay gia hạn deadline | Theo dõi fair.conf.vn sát ngày |
| Viết tiếng Anh (FAIR) chậm | Bài model số liệu sẵn → viết mô tả kết quả; nhờ người rà tiếng Anh nếu cần |

---

## §7. Đoạn NÓI VỚI THẦY

> "Thưa thầy, em đã có mô hình tự huấn luyện (Faithful Distillation) như thầy yêu cầu. Em định tách thành **2 bài không trùng nhau** để có thêm công bố: **(1) FAIR (tiếng Anh, nộp 15/8)** trình mô hình + kết quả định lượng; **(2) VCL (tiếng Việt, nộp 30/8)** cho mô hình **sinh hướng dẫn bằng tiếng Việt** và khảo sát khả năng chuyển-giao Anh→Việt + cách đánh giá không cần đáp án mẫu — câu hỏi và ngôn ngữ output khác hẳn bài FAIR, và bài VCL trích dẫn bài FAIR. Nếu FAIR gấp quá không kịp, em vẫn chắc chắn có bài VCL, còn mô hình để dành nộp venue quốc tế sau ạ."

---

## §8. VIỆC CẦN VERIFY TRƯỚC KHI NỘP (deep-research chưa có nguồn — đừng bịa)
- Deadline + CFP **VCL2026** (trang HUFLIT) — 30/8 mới là trí nhớ user.
- Chính sách **dual-submission / trùng lặp / self-plagiarism** của cả FAIR và VCL.
- Độ dài/template bài · index Scopus/DBLP · ISBN kỷ yếu từng venue.
- FAIR có gia hạn 15/8 không.

*Citation đã verify (dùng cho cả 2 bài): AndroidControl NeurIPS 2024 D&B · ScreenSpot-v2 OS-Atlas ICLR 2025 · Chim/Ive/Liakata CL 51(1) 2025 · ALOHa NAACL 2024 · thứ-tự-bộ-phận (C−D)/|M| = Fagin 2006 + Lapata CL 2006 (KHÔNG "Kendall τ-b") · Sai EMNLP 2021 (perturbation) · UI-R1 AAAI 2026. MobileViews = preprint → chỉ dùng làm nguồn ảnh/nhãn.*
