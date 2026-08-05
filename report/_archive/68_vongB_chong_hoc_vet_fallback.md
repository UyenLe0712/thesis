# report/68 — Vòng B: Chống học vẹt template fallback (kết quả deep-research)

> Vòng B kiểm cái nguy cơ mode-collapse khi student học vẹt đúng câu fallback template lặp trong data train (report/65 NGHI 4, report/63). Ba mũi: B1 = metric đo đa dạng + ngưỡng collapse, B2 = số biến thể paraphrase đủ, B3 = có nên gắn abstention token. Ngày: 2026-07-18.

**Lưu ý độ tin:** research + kiểm chứng đối kháng đều trả nội dung THẬT (không placeholder). Mọi con số/venue dưới đây đã qua bước verify; chỗ nào verify hạ verdict xuống PARTIAL/UNVERIFIABLE thì ghi rõ và không nâng lên thành sự-thật. Ba đính chính số/tên tác giả mà verify bắt được đã sửa thẳng trong bảng claim.

---

## Trả lời thẳng 3 câu hỏi (B1/B2/B3)

**B1 — Metric đo đa dạng + ngưỡng collapse + có nghiên cứu before/after SFT không.**
Dùng bộ ba, đều free/local, tính offline:
- **Distinct-1 và distinct-2** (Li et al., NAACL 2016) — tỉ lệ n-gram duy nhất trên tổng số token. Càng gần 0 = càng lặp. **Bắt buộc dùng bản EAD (Expectation-Adjusted Distinct, Liu et al., ACL 2022)** khi so output trước/sau train, vì distinct-n gốc phạt chuỗi dài — mà độ dài output rất dễ đổi sau SFT, không chuẩn hoá thì lệch giả.
- **Self-BLEU** (Zhu et al., Texygen, SIGIR 2018) — báo dưới dạng `100 − Self-BLEU` cho đọc thuận chiều (cao = đa dạng cao), đúng cách GEM trình.
- **Entropy phân phối sinh** — con số trực tiếp nhất, chính là chỉ số GEM dùng.

Có tiền lệ đo before/after SFT trên đúng loại rủi ro này, và nó rất mạnh cho luận văn: **GEM (Preserving Diversity in SFT, ICLR 2025)** đo được entropy đầu ra tụt còn **0.42 (CE thường), 0.41 (weight-decay), 0.43 (NEFTune) so với 0.76 (GEM)** — bốn số này verify khớp nguyên văn — do cơ chế "all-to-one probability transfer" dồn hết khối xác suất vào token đích. Bổ trợ (preprint): Karouzos et al. 2026 cho thấy mất đa dạng bị "khắc vào trọng số" tại bước SFT, không cứu được bằng đổi decoding lúc suy luận — **nhưng chỉ trong distillation hẹp một-teacher** (đúng kịch bản của ta), nên phải đo trước/sau train chứ không chỉ chỉnh nhiệt độ.

**Ngưỡng "collapse": KHÔNG có cutoff tuyệt đối chuẩn ngành** (distinct/self-BLEU phụ thuộc corpus + độ dài). Cách đúng = so tương đối student-BASE vs student-sau-SFT trên cùng tập prompt held-out. Cờ đỏ cụ thể: đo RIÊNG trên các bước fallback — nếu **exact-duplicate-rate của câu fallback tăng vọt** hoặc **distinct-2 trên tập câu fallback tụt gần 0** sau train, đó là mode-collapse. Trần đối chiếu = distinct/entropy của chính tập paraphrase gốc; sau train nhánh fallback nên xấp xỉ trần đó, không sụp về 1 câu.

**B2 — Số biến thể paraphrase đủ.**
Không có con-số-vàng peer-reviewed riêng cho "bao nhiêu paraphrase của MỘT câu fallback là đủ" (không ai quét {5,10,50} cho câu hedge/từ-chối). Nhưng **~10 là mức chuẩn phòng-thủ-được**, neo vào **FLAN (Wei et al., ICLR 2022)**: FLAN "manually composed ten unique templates" cho mỗi task, bốc ngẫu nhiên một cái mỗi mẫu — verify khớp nguyên văn. Lưu ý sắc thái: đó là 10 template cho instruction của một task, không phải 10 paraphrase của một câu → là tiền lệ tương tự (analogy), không phải trụ trực tiếp. Điểm quyết định thật không phải con số mà là **ĐỘ TRẢI**: 10 câu thật khác chữ + khác cấu trúc tốt hơn nhiều câu gần-trùng (Instruction Diversity, 2402.10891 — preprint). Và cổng cứng cuối cùng là **số đo đa dạng trên output student** (GEM), không phải niềm tin vào con số biến thể.

**B3 — Abstention token hay paraphrase-set.**
**Khuyến nghị: paraphrase-set (B2) làm TRỤC CHÍNH; abstention token chỉ là nhánh mở rộng tuỳ chọn.** Token abstain học-được đã kiểm chứng nhưng gần như toàn bộ ở LLM chỉ-văn-bản ([IDK] token, NeurIPS 2024; Refusal Tokens, preprint 2024 trên Llama-3/Mistral). Ở VLM nhỏ ≤7B, cái đang có là probe tầng ẩn / activation-steering (không sửa vocab) trên Qwen2.5-VL-7B/Gemma-3-12B — **chưa tìm thấy** tiền lệ gắn token abstain học-được vào VLM nhỏ kiểu Qwen-VL/LLaVA. Với budget luận văn (3B, LoRA, Colab, eval free, KHÔNG có gold cho fallback), token riêng đòi phẫu thuật tokenizer + một tập calibration để chứng minh "biết mình không chắc" (mà ta không có gold để chứng minh), lại thêm rủi ro over-refusal ở scale 3B. Paraphrase-set giải đúng vấn đề thật (mode-collapse do 1 câu lặp) với chi phí gần bằng 0, không đụng kiến trúc, đo được bằng metric free/local. Nếu muốn có chất khoa học chạm tới dòng refusal-token: cho khuôn fallback bắt đầu bằng prefix neo cố định (vd `[MÔ TẢ]`) rồi đọc xác suất prefix đó như tín hiệu abstain lúc suy luận — không thêm token mới vào vocab, vẫn nêu liên hệ được trong related work.

---

## Cổng dừng B2

**Verdict: ĐẠT-CÓ-ĐIỀU-KIỆN** → có thể áp thẳng vào script build data, **B3 không phải trục** (đã trả lời: paraphrase-set thắng abstention token cho budget này).

- **Đạt ở đâu:** tìm được con-số phòng-thủ-được = **10 biến thể**, neo peer-reviewed FLAN (ICLR 2022). Đủ để chốt tham số script mà không bị hỏi "vì sao 10 mà không phải số khác".
- **Điều kiện (vì sao không ĐẠT tuyệt đối):** 10 là analogy từ task-template, KHÔNG phải con-số-vàng đo trực tiếp cho câu fallback (claim "không tồn tại ablation {5,10,50}" là mệnh đề phủ-định-tồn-tại → verify để UNVERIFIABLE, không xác lập được). Nên 10 là **mức khởi điểm, không phải cổng cứng**.
- **Hệ quả:** cổng cứng thật dời sang **số đo đa dạng trên output student** (distinct-n/self-BLEU/entropy đo before/after train — đúng B1). Nghĩa là: build data với 10 paraphrase viết-tay đa dạng ngay bây giờ; nếu sau train đo thấy nhánh fallback vẫn collapse (distinct-2 gần 0 / exact-dup-rate cao) thì mới tăng số/tăng độ trải. Không chặn tiến độ chờ một con số hoàn hảo.

---

## Bảng claim sống / bị bác

| Claim | Nguồn | Peer-reviewed? | Verdict | Ghi chú (đã sửa venue/số sai) |
|---|---|---|---|---|
| Distinct-1/2 = n-gram duy nhất / tổng token; cặp mặc định đo đa dạng | Li et al., NAACL 2016 | Có | SUPPORTED | Mẫu số bản GỐC = tổng số **TỪ** (không phải tổng n-gram); "chia cho tổng n-gram" là biến thể đời sau. Khi in công thức ghi rõ dùng bản nào. |
| Distinct-n phạt chuỗi dài; EAD chuẩn hoá theo kỳ vọng, tương quan người tốt hơn → dùng khi so trước/sau train | Liu et al., ACL 2022 (short) | Có | SUPPORTED | Khớp nguyên văn. |
| Self-BLEU cao = đa dạng thấp; báo `100 − Self-BLEU` | Zhu et al., Texygen, **SIGIR 2018** | Có | SUPPORTED | Venue đúng SIGIR 2018 (ACM DL 10.1145/3209978.3210080); arXiv 1802.01886 chỉ là preprint cùng bài. |
| CE-SFT: entropy 0.42 (CE) / 0.41 (WD) / 0.43 (NEFT) vs 0.76 (GEM); cơ chế all-to-one | GEM, ICLR 2025 (arXiv 2408.16673) | Có | SUPPORTED | Bốn số khớp CHÍNH XÁC bản HTML v2. Bản v1 arXiv tên khác ("Entropic Distribution Matching…") — bản chính thức = ICLR 2025. |
| Mất đa dạng khắc vào trọng số tại SFT, decoding không cứu → phải đo before/after | Karouzos et al., 2026 (arXiv 2604.16027) | **Không (preprint)** | SUPPORTED (có điều kiện) | Chỉ đúng trong **distillation hẹp một-teacher** (SFT cliff, mất 62%); multi-source thì điểm sụp dời sang DPO. Ta rơi đúng nhánh SFT cliff. Trích có-điều-kiện, đừng nói "SFT luôn là nơi collapse". |
| FLAN dùng đúng 10 template/task, bốc ngẫu nhiên → 10 là mức chuẩn có trụ | Wei et al., FLAN, ICLR 2022 | Có | SUPPORTED | Khớp "manually composed ten unique templates". Là analogy task-template, KHÔNG phải trụ trực tiếp cho paraphrase câu fallback. |
| Không tồn tại ablation {5,10,50} paraphrase cho câu hedge → không có con-số-vàng riêng | Tổng hợp | — | **UNVERIFIABLE** (hợp lý) | Mệnh đề phủ-định-tồn-tại, không chứng minh dứt điểm được. Không tìm thấy phản chứng. Trình ở mức "chưa tìm thấy", đừng xác lập. |
| Đa dạng ngữ nghĩa > số lượng thô → 10 câu trải rộng > nhiều câu gần-trùng | Instruction Diversity, arXiv 2402.10891 | **Không (preprint)** | PARTIAL | Cốt lõi đúng nhưng trục là số TASK/loại-instruction, KHÔNG phải paraphrase của một câu → ngoại suy hợp lý về tinh thần, không phải điều bài đo trực tiếp. |
| SFT sụp đa dạng → phải ĐO (entropy/self-BLEU) rồi kiểm soát, không tin con-số biến thể | GEM, ICLR 2025 | Có | SUPPORTED | self-BLEU là chỉ số phổ quát research gợi ý, không nhất thiết riêng GEM (nhưng không sai). |
| Template từ-chối cố định gây overfit/dễ bẻ; đa dạng hoá ~10 biến thể/style giảm rõ | Attack-via-Overfitting, arXiv 2510.02833 | **Không (preprint)** — cần verify NeurIPS 2025 | PARTIAL | Nửa đầu (template cố định gây overfit) đúng. Nửa sau (~10 biến thể/style giảm rõ) là suy diễn của research — bài phía TẤN CÔNG, không đo biến-thể-vs-robustness. Có dấu hiệu đã nhận NeurIPS 2025 → verify venue trước khi trích. |
| Token abstain học-được kiểm ở LLM văn-bản; chưa có tiền lệ VLM nhỏ ≤7B | [IDK] NeurIPS 2024; Refusal Tokens preprint | Một phần (Có / Không) | PARTIAL | **Sửa tên tác giả [IDK]: Roi Cohen, Konstantin Dobler, Eden Biran, Gerard de Melo** (KHÔNG phải "Biemann, Kalinsky"); **arXiv id [IDK] = 2412.06676**. Vế "chưa có tiền lệ VLM" là phủ-định → hạ giọng "chưa tìm thấy". |
| Refusal Tokens: chỉnh ngưỡng lúc suy luận bằng softmax token, không train lại; ECE token-level 0.12→0.08 | Refusal Tokens, arXiv 2412.06748 | Không (preprint) | PARTIAL | Cơ chế đúng. **Số SAI/gộp nhãn: token-level ECE 0.12→0.11 (temp-scaling τ=2); 0.08 là "adjusted ECE" (min-max rescale) đi từ 0.13→0.08 — chỉ số KHÁC.** Sửa trước khi trích. |
| Abstention VLM nhỏ làm bằng probe/steering (không sửa vocab) trên Qwen2.5-VL-7B/Gemma-3-12B | arXiv 2511.19806; 2602.07013 | Không (preprint) | SUPPORTED | Khớp hoàn toàn. Cả hai preprint — khai đúng khi trích. |
| SFT dạy abstain 7B → over-refusal + bóp kiến thức; LoRA giảm nhẹ so full-finetune | RAIT survey 2407.18418; Know Your Limits (TACL) | Một phần (Không / Có) | PARTIAL | Vế over-refusal đúng, có trụ. Vế "LoRA < full-finetune về over-refusal" CHƯA có so-sánh head-to-head trong nguồn (chỉ thấy "LoRA giữ năng lực chung") → nêu như quan sát định tính, không phải đối chứng. |

**REFUTED:** không có claim nào bị bác hoàn toàn. Các điểm cần sửa đều là đính chính số/tên/venue hoặc hạ verdict, không phải claim sai bản chất.

---

## Khuyến nghị cho luận văn (cụ thể, actionable)

1. **Metric đo đa dạng — chốt 3 con số, đo 2 cấp:**
   - `distinct-1`, `distinct-2` **bản EAD** (Liu ACL 2022) — chuẩn hoá độ dài, tránh lệch giả khi output đổi độ dài sau train.
   - `100 − Self-BLEU` (Zhu SIGIR 2018) — đọc thuận chiều.
   - `entropy` phân phối sinh (theo GEM ICLR 2025) — con số then chốt so trực tiếp với 0.42→0.76 của GEM.
   - **Cấp corpus:** gom tất cả bước sinh → tính cả ba.
   - **Cấp fallback riêng (quan trọng nhất):** lọc riêng các câu bị viết-lại-thành-mô-tả-chung → distinct-2 + **exact-duplicate-rate** + entropy. Mode-collapse lộ ở đây trước.

2. **Số biến thể paraphrase: 10**, viết-tay/duyệt-tay bảo đảm khác chữ + khác cấu trúc (không phải 10 bản gần-trùng), neo FLAN (ICLR 2022). Coi là mức khởi điểm, không cổng cứng.

3. **Đo before/after train:** so student-BASE vs student-sau-SFT trên **cùng tập prompt held-out theo app**. Trần đối chiếu = distinct/entropy của chính tập 10 paraphrase gốc. Tiêu chí collapse (pre-register trước khi nhìn kết quả): trên nhánh fallback, nếu exact-dup-rate tăng vọt hoặc distinct-2 tụt gần 0 so với BASE → cờ đỏ mode-collapse.

4. **Abstention token: KHÔNG dùng làm trục.** Chọn paraphrase-set. Nếu muốn liên hệ khoa học với dòng refusal-token: dùng prefix neo cố định `[MÔ TẢ]` mở đầu khuôn fallback, đọc xác suất prefix như tín hiệu abstain lúc suy luận (rẻ, không sửa vocab, nêu được trong related work). Ghi rõ đây là lựa chọn tuỳ chọn, không phải đóng góp.

5. **Bước tiếp cho script build data:** trong khối viết-lại-bịa-thành-mô-tả, thay 1 câu template cố định bằng **danh sách 10 paraphrase, bốc ngẫu nhiên (seed cố định) khi viết lại**. Ghi lại phân phối câu nào được bốc để tính trần đa dạng.

> **Quyết định cuối thuộc về user** — báo cáo này neo con số + trụ, nhưng chọn dùng 10 hay đo rồi tăng, có làm nhánh prefix `[MÔ TẢ]` hay không là do user chốt.

---

## Việc phải tự làm (gaps)

- **[PRE-REG]** Ghi ngưỡng collapse (exact-dup-rate / distinct-2 cutoff cho nhánh fallback) vào pre-registration TRƯỚC khi chạy đo before/after — vì không có cutoff chuẩn ngành, phải tự đặt và khoá trước khi nhìn kết quả (nhất quán report/56).
- **[CODE]** Viết tập 10 paraphrase tiếng Việt (VCL) + tiếng Anh (FAIR) cho khuôn fallback; sửa khối viết-lại để bốc ngẫu nhiên có seed.
- **[CODE]** Harness đo đa dạng: distinct-n (bản EAD), `100−Self-BLEU`, entropy — 2 cấp corpus + fallback-riêng; chạy trên output student-BASE và student-sau-SFT.
- **[CITATION]** Sửa trước khi in: tên tác giả [IDK] = Cohen, Dobler, Biran, de Melo (arXiv 2412.06676); Refusal Tokens ECE token-level = 0.12→0.11 (KHÔNG phải 0.08); mẫu số distinct-n gốc Li 2016 = tổng số **từ**.
- **[CITATION]** Verify venue Attack-via-Overfitting (2510.02833) — nghi đã nhận NeurIPS 2025; nếu đúng thì nâng từ preprint lên peer-reviewed.
- **[CITATION]** Karouzos 2604.16027 và các bài abstain VLM (2511.19806, 2602.07013), Refusal Tokens (2412.06748), Instruction Diversity (2402.10891) đều là **preprint** — trích ở mức bổ trợ, không xếp chung hàng trụ peer-reviewed (GEM ICLR 2025, FLAN ICLR 2022, Li NAACL 2016, Liu ACL 2022, Zhu SIGIR 2018, [IDK] NeurIPS 2024, Know Your Limits TACL).
