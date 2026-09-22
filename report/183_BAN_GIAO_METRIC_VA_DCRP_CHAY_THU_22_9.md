# Bàn giao: thước đã chốt + DCRP cần chạy thử — 22/09/2026

> **Bản chép từ 9 ảnh** (`report/anh_183_ban_giao_22_9/01…09`, zip gốc cùng thư mục). Bản gốc
> soạn trên máy Mac (`/Users/P836901/Documents/Self-learning/thesis/`), **không có trong kho WSL**,
> cũng như 180/181/182. Chữ nào mờ trong ảnh được đánh dấu `[?]`.

> File tự chứa. Gửi nguyên file là đủ. Không cần 180/181/182, không cần lịch sử chat.
>
> **Trạng thái:** metric đã chốt, không debate lại. DCRP đã chốt hướng, chưa train, chưa chạy G0.
> Init S1 vs CE2 chưa chốt trên giấy, chốt bằng đo ở G2.
>
> **Bác ba kết luận cũ:** (i) thước chính = Phi-4, (ii) init buộc CE2, (iii) 82,57% xếp hạng ký hiệu = same-policy.

**Workspace:** `/Users/P836901/Documents/Self-learning/thesis/`. Clone dùng một lần: `thesis-master/`
(sẽ bị xoá). Script CPU ngoài clone: `m9_khop_mem.py`, `m2_m3_compare.py`, `all_forest_dict.zip`.

## 0. Chat nhận file làm gì

| Khi | Việc | Máy |
|---|---|---|
| Ngay | G0 (phụ lục A). In bảng mention × `exec`, pass/fail theo §6. Không train. | CPU |
| G0 pass | G2: sinh `k=8` trên cả hai S1/101 và CE2-S2/101, 300–500 prompt train, dev held-out, không test. Áp luật init §6.4 [§4]. Đăng ký nhiệt trước khi sinh (số chưa chốt). | inference GPU |
| G2 pass + người dùng cho phép | Một seed DCRP + 3 đối chứng §5, rồi G6. Liều `N = P/16` (§4). | A100 |
| Song song, bắt buộc metric | UI-Venus 5 nhánh còn thiếu × 4.463. Tra backbone UGround / UI-Venus / speaker trước nếu tính thuê listener 3. | GPU / đọc tài liệu |

**Cấm trừ khi người dùng nói rõ:** train đầy đủ trước G0 · mở lại metric · UGround/UI-Venus làm
reward hoặc filter · GUI-Actor / selector+ROI / unfreeze vision · IA uniqueness · ORPO trên `<desc>` · git.

**Người dùng phải tự làm (không git):**
1. Hỏi GV: đóng góp mô hình có bắt buộc layer/head mới không. Có → DCRP không thoả; hướng D (chẩn đoán âm) vẫn bảo vệ được.
2. Duyệt luật init §6.4 trước khi xem số G2.
3. Cho phép G0 (mở `runs/`). Chat in pass/fail vào file sau.

**Fail bất kỳ cổng:** không train đầy đủ. Viết chẩn đoán âm: 90,4 vs 39,5; point→câu +0,02; khe
imitation Phi-4; SFT liều phẳng +0,05; 66,7% byte-identical.

## 1. Bài toán

Qwen2.5-VL-3B-Instruct QLoRA, vision đóng băng. Ảnh + mục tiêu + lịch sử → một câu. Model không
sinh toạ độ. Listener UGround đóng băng đọc chỉ ảnh + câu → `(x,y)`.

`exec` = Voronoi gated ±14%: gần điểm chạm đích hơn mọi phần tử khác. n = 4.463. MDE ≈ 2,11.
Trần câu người cùng dụng cụ: 75,73 — không đọc trên nền 100.

Không người. Không LLM-as-judge.

## 2. Metric đã chốt

| Vai | Metric | Trạng thái |
|---|---|---|
| Primary | `exec` | ✅ 9 nhánh |
| Confirmatory | `D.3` (điểm trong hộp) | ✅ 9 nhánh. r ≈ 0,99995 với `exec` — báo vì tiền lệ, không vì thông tin mới |
| Robustness bắt buộc | UI-Venus — đọc chênh lệch giữa nhánh | ⚠️ THIẾU 5/9: S1/202, CE2, MIN-DESC, gui_sel, Pipeline |
| Secondary bắt buộc | `action_ok` · độ dài từ (`\b\w+\b`) · SPICE hệ thống | ✅ 9 nhánh |
| Diagnostic | Trần · 2 sàn · ablation TÊN–VỊ TRÍ · paraphrase động từ/trật tự · `exec` theo `n_buttons` | ✅ |
| Diagnostic | Paraphrase chạm tên phần tử | ❌ |
| Appendix | AitW · BLEU-4 COCO · METEOR · ROUGE-L · CIDEr-D · BERTScore | ✅ |
| Appendix | Phi-4 SoM | ⚠️ THIẾU 5/9; trần 54,94 vs 75,73. Ưu tiên bỏ |
| Exploratory | E1 · E2 | ❌ sau UI-Venus |

**Cấm:** người · LLM-as-judge · CLIPScore · BLEU primary · mừng khi sát trần 75,7 (viết cho listener).

Hai BLEU-4: COCO S1 ≈ 51,6 ≠ trung bình mức câu S1 ≈ 38,7. Không trộn.

### 2.1. Nhánh

| Nhánh | Là gì |
|---|---|
| Base | Qwen gốc |
| **S1** | Đường cơ sở chính. SFT 2 epoch. Hạt 101/202 |
| S2 | S1 + ô `<desc>` (cắt trước khi chấm) |
| **CE2-S2** | S2 + 800 cập nhật SFT trên vế chosen của cặp MIN-DESC. Cross-Entropy stage-2. **Không phải SFT song song S1** |
| MIN-DESC | ORPO, cặp chỉ khác `<desc>`, câu y hệt. Vs CE2 lệch **dropout** (trainer DPO zero dropout) — khai khi báo Δ cũ |
| Pipeline / GRPO-point | + GRPO thưởng `<point>`. Đóng góp cũ, dưới MDE |
| gui_sel | Lệch ba biến ⇒ chỉ so Base |
| Câu chuẩn | Trần dụng cụ |

### 2.2. Tầng lõi — n = 4.463

| Nhánh | `exec` | `D.3` | `action_ok` | SPICE | Từ/câu |
|---|---|---|---|---|---|
| Base | 47,59 | 53,60 | 96,46 | 18,48 | 14,10 |
| S1/101 | 59,11 | 65,49 | 94,35 | 44,37 | 7,86 |
| S1/202 | 59,62 | 66,10 | 94,58 | 44,23 | 7,93 |
| S1 avg | 59,37 | 65,80 | 94,47 | 44,30 | 7,90 |
| S2/101 | 57,18 | 63,63 | 94,85 | 41,28 | 8,01 |
| CE2-S2/101 | 59,42 | 66,03 | 98,86 | 42,27 | 8,12 |
| MIN-DESC/101 | 60,05 | 66,55 | 98,88 | 42,24 | 8,13 |
| gui_sel/101 *(chỉ so Base)* | 56,13 | 62,38 | 90,90 | 39,28 | 7,92 |
| Pipeline/101 | 60,07 | 67,04 | 98,86 | 42,50 | 8,13 |
| Trần | 75,73 | 83,82 | 100,00 | — | 7,86 |

Pipeline − S1 = **+0,70**. Pipeline − CE2 = **+0,65**. Cả hai dưới MDE. S1→S2→CE2: `exec` −2,19
rồi +2,24 = net +0,05; `action_ok` +4,39. Prefix mua định dạng, không mua `exec`. Viết một dòng SFT backbone.

Độ dài (cùng n): trung vị 6, P90 13 mọi nhánh fine-tune. Pipeline − CE2 = +0,009 từ [−0,040; 0,058].
~37% câu ≤ 5 từ (S1 và CE2) ⇒ rủi ro `k=8` sập về 1 câu.

`exec` theo `n_buttons`: Pipeline − S1 ở `>80` (n=1.892) = +1,85 [0,22; 3,47]. Vs CE2 và MIN-DESC: mọi lát KTC chứa 0.

### 2.3. Trần / sàn / ablation (lát 800, trần lát 74,9)

| Đầu vào | Điểm | KTC |
|---|---|---|
| Câu chuẩn | 74,9 | — |
| "Tap the button." | 12,0 | [9,7; 14,4] |
| Câu chuẩn màn khác | 6,1 | [4,5; 7,9] |

Sàn 2 < sàn 1 ⇒ dụng cụ đọc nội dung. Dải ≈ 62,9. Bỏ TÊN (n=193) −28,5 pp; bỏ VỊ TRÍ (n=198)
−3,5 pp. Paraphrase bảo toàn nghĩa 1.139 câu: đổi chiều 2,6%, ròng +0,35.

### 2.4. UI-Venus — lát 2.532, 8,15 h GPU

| Phép so | UGround | UI-Venus |
|---|---|---|
| S1 − Base | +10,35 [+8,39; +12,40] | +9,68 [+7,60; +11,78] |
| S2 − S1 | −1,93 | −1,21 |

Điểm: Base 39,1 · S1 48,7 · S2 46,6. Thang không nén. **Không claim CE2/Pipeline khi còn thiếu 5 ô.**

### 2.5. Appendix (đủ 9 nhánh)

AitW lower/upper: Base 63,39/73,36 · S1 avg 74,84/81,48 · S2 73,40/80,78 · CE2 76,09/83,93 ·
MIN-DESC 76,41/84,36 · gui_sel 71,16/77,91 · Pipeline 77,30/85,01 · trần 92,14/96,17.

BLEU-4/METEOR/ROUGE-L/CIDEr-D/BERTScore (COCO, BERT rescaled): Base 15,34/24,58/42,31/88,01/40,10 ·
S1 avg 51,61/36,98/67,53/417,65/66,54 · S2 48,68/35,75/65,97/387,68/65,07 · CE2
50,12/37,31/68,62/402,24/66,83 · MIN-DESC [?]9,92/37,26/68,47/401,01/66,73 · gui_sel
46,89/34,23/63,32/370,62/62,75 · Pipeline 49,86/37,31/68,54/402,91/66,85.

Phi-4: Base 38,56 *(3.566/4.463)* · S1/101 44,63 · Pipeline 45,78 · trần 54,94 · sàn rỗng 15,86.

### 2.6. Luật đọc

`exec`↑ `D.3`↑ dấu giữ dưới UI-Venus → claim communicative, kèm độ dài + SPICE. Dấu đổi/mất dưới
UI-Venus → không claim. Câu dài mạnh → nghi gaming. Không hơn continued-SFT cùng init → gain
compute. BLEU↑ `exec` không↑ → imitation.

## 3. DCRP

Không kiến trúc, ROI, unfreeze, custom trainer. LLaMA-Factory + sample (vLLM / `infer_branch`)
+ scorer `m9_khop_mem.py`.

```
INIT ∈ {S1/101, CE2-S2/101}   # chốt G2; sample và train CÙNG checkpoint
 → k=8 câu scored (cùng ảnh, cùng gold widget)
 → khung action identical; chỉ NP/câu chỉ định khác
 → rank ký hiệu: gold vs same-role distractor (a11y+OCR)
 → giữ cặp: không hoà, |Δ từ| ≤ 1, rejected = widget cùng vai thật
     (ưu tiên widget model thực sự hay nhầm)
 → ORPO/DPO; listener KHÔNG reward/filter
 → eval: exec + D.3 + UI-Venus + action_ok + length + SPICE
 → cùng batch: continued-SFT, chosen-only SFT, shuffled
```

Đóng góp = dựng cặp target-vs-hard-distractor **kiểm toán được**. Không phải ORPO, không phải Qwen.

ISR (ACL 2025) dùng **grounder làm reward**. DCRP cấm điều đó.

> We post-train a GUI referring speaker with length-matched, same-policy preferences over scored
> sentences, ranked by a frozen accessibility/OCR target-distractor scorer that never touches the
> evaluation listeners, and we report pass@1 frozen-listener execution against a dose-matched
> extra-SFT control.

**Không claim:** kiến trúc mới · paradigm speaker–listener mới · khe Phi-4 = headroom UGround ·
82,57% = same-policy · uniqueness = faithfulness · trần 75,73 = human ceiling · app unseen (~92% overlap train/test).

P(Δ`exec` ≥ 2,11 vs continued-SFT) **~0,30**. Không dùng Gemini 0,65. ArXiv 2603.20100: DPO không
phải thắng lớn tin cậy trên SFT đã tinh.

**Ranker (nhị phân):** tên +3 / OCR hộp +3 / role +0,5 / vùng +0,3. Không biên độ liên tục (bin
0,6–2,9 tệ hơn 0–0,6). Khớp mềm F1+stem giảm hoà, `r` không tăng. Cross-policy (người vs S1 vs
Pipeline, Phi-4 bất đồng): 1.184/1.434 = **82,57%** [80,61; 84,52]. Lạc quan. Same-policy = G3, chưa đo.

### 3.1. Kênh chết — đừng đề xuất lại

| Kênh | Số |
|---|---|
| IA uniqueness → `exec` | +0,19 |
| S2 | 57,18 vs S1 59,37 = −1,93 [sic: hiệu hai số in là −2,19; −1,93 là S2 − S1/101] |
| GRPO-point → `exec` | +0,02 (khai báo +2,56 pp) |
| VIS-SFT | −7,50 vs MIN val; không test |
| gui_sel | 56,13; 27,3% over-abstain |
| CE2 − S1 | +0,05 `exec` |
| True-miss | trần ≈ +1,05 |
| Consensus 6 nhánh | −0,45 / −1,01 AitW |
| Đổi `<desc>`, câu scored trùng byte | 1.300/1.950 = 66,7% |

`<point>` sai vẫn trên nút bấm được thật **90,4%** (441/488) vs đối chứng 39,5%. True-miss 9,6%.
Nghẽn = chọn đúng phần tử. Selector+ROI chết: listener không thấy ROI (+0,02) hoặc trần true-miss < MDE.

### 3.2. Khe mention Phi-4 — lý do G0 (chưa đo UGround)

3.975 bước mô tả vàng duy nhất:

| | Đích dạy | S1 | Chênh |
|---|---|---|---|
| Listener Phi-4 | 57,08 | 46,79 | khe 10,29 (Pipeline 47,60 → khe 9,48) |
| % nhắc tên/OCR (biên ≥ 2,9) | 33,1 | 27,5 | −5,6 |
| Phi-4 đúng khi đã nhắc | 71,65 | 70,61 | −1,04 |

5,6 × (70,61 − ~33) ≈ 2,1 = MDE. Không chứng minh headroom UGround.

## 4. Init và con 800

Same-policy (DPO): sample = train = cùng checkpoint. `(S1,S1)` và `(CE2,CE2)` cùng hợp lệ. Trộn =
off-policy. `exec` 59,37 vs 59,42 — MDE không đổi theo init.

| | CE2 | S1 |
|---|---|---|
| `action_ok` sẽ in | 98,86 | 94,47 (dưới Base 96,46) |
| UI-Venus | ❌ | ✅ 48,7 |
| Hạt | chỉ 101 | 101/202, dải 0,51 |
| `<desc>` | có (G1 cấm dụng) | không |
| Liều nói ra được | 800 bước = 0,56 epoch, tự khai ngân sách | hai epoch |

**800 là gì:** 800 cập nhật × 16 cặp = 12.800 / 22.854 = 0,56 epoch. ~21 s/bước ≈ 4,7 h A100. CE2
800 vì khớp liều MIN. 1 epoch tập cũ = 1.428–1.429 bước. Cosine đóng ở 800 ⇒ chu kỳ hoàn tất, chỉ
ngắn; liều cố định trước khi chấm, hai nhánh giống nhau ⇒ không thiên vị MIN vs CE2. ORPO Hong EMNLP
2024: không chế độ < 1 epoch; đối chứng 10 epoch + val-loss. Lệch hai trục. Không sửa hồi tố (điểm
100–600 đã xoá). Đổi init không xoá MIN−CE2 = +0,63 `exec` (p=0,008).

**DCRP:** `N = P/16`, một epoch trên bộ cặp, chọn checkpoint theo val loss. Dưới ~50% năng suất cặp,
`N` rẻ hơn 800 (25% → ~357 bước, ~4,2 h hai nhánh, cận trên 21 s).

**Luật init sau G2:** chỉ một qua → lấy cái đó. Cả hai qua, chênh < 10 pp → **S1**. CE2 hơn ≥ 10 pp
→ **CE2**. Cả hai fail → rút DCRP.

## 5. Đối chứng (FormulaSPIN)

Cùng init: (i) backbone (ii) continued-SFT khớp `N`/LR/batch/dropout — báo dù phẳng/âm (iii)
chosen-only SFT (iv) shuffled (v) DCRP.

## 6. Cổng

Thứ tự: G0 → G2 cả hai init → §4 chốt init → G1 xác nhận cặp · G3 · G5 → một seed + đối chứng →
G6. Không mở test UGround tới khi G0–G5 đóng.

**G0** CPU, phụ lục A. Trần suy ra = Δ(%mention người vs S1/CE2) × Δ(`exec` | mention vs không) của
nhánh so. Pass ≥ 3,0 pp. 2,0–3,0 → G4. Fail < 2,0 → rút preference. Không phụ thuộc init.

**G1** 0 GPU. Cặp trên câu scored. Khung action identical. Không thưởng độ dài thô.

**G2** từng init: ≥25% prompt có cặp hợp lệ; ≥40% có ≥3 câu khác nhau; oracle best-of-8 `exec` (dev,
diagnostic) ≥ greedy +6 pp. UI-Venus dev nếu có: rerank ≥ +4,22. Không test.

**G3** same-policy pairwise khi listener bất đồng. CI lower bound ≥ 60%. Dưới 55% = nhiễu. 82,57% không thay.

**G4** chỉ nếu G0 yếu hoặc G3 sát. Grounder 2B held-out: OS-Atlas / ShowUI / SeeClick / Aria-UI.
Không UGround, không UI-Venus. CI ≥ 65%. Báo κ với UGround trên câu đã có.

**G5** reward-top-1 không dài hơn greedy > 0,5 từ. SPICE không giảm. Token ảo không tăng.

**G6** sau một seed: ≥50% khác greedy init. Treatment > chosen-only cùng liều. Nếu ≤ → dừng.

## 7. Văn liệu

GROKE ACL 2026 long · RefOI COLM 2025 · AndroidControl-Curated arXiv 2510.18488 · TrueMatch TMLR 2025
· Anderson EACL 2021 · Wright & Suhr COLM 2026 · ISR ACL 2025 https://aclanthology.org/2025.acl-long.1483/
· Jandial Findings EACL 2026 · FormulaSPIN arXiv 2607.19354 · SFT–DPO arXiv 2603.20100 · DPO NeurIPS
2023 · ORPO EMNLP 2024 · Mao CVPR 2016 · GUI-Actor NeurIPS 2025 không chứng minh ROI cải thiện câu
REG · Dale & Reiter 1995 đã đo (+0,19 `exec`) — không làm lại.

## 8. Đoạn Anh

**Init S1:** *All post-training starts from QLoRA Qwen2.5-VL-3B-Instruct, vision frozen, two epochs
on AndroidControl REG targets. SFT reduces `action_ok` 96.46 → 94.47; an intermediate-description
format recovers 98.86 but costs 2.19 `exec` that 800 extra steps recover (net +0.05). We report the
plain backbone; format variant in appendix.*

**Init CE2:** một artefact "2 epoch + 800 steps + `<desc>`"; net +0,05 `exec`, +4,39 `action_ok`;
từng chặng = appendix.

**Dose:** one epoch over preference set, `N=P/16`, checkpoint by val loss (Hong et al. EMNLP 2024).
Limitation: MIN-DESC/CE2 used 800 updates = 0.56 epoch, final checkpoint, budget-fixed, identical arms.

**Vs ISR:** no grounder in reward/filter.

## 9. Bản trước sai

Primary = người/Phi-4 → `exec`. Init buộc CE2 → sample=train, không ghim CE2. 82,57% = same-policy
→ cross-policy. Khe 9,48 = headroom UGround → G0. Pipeline = kiến trúc → +0,65 dưới MDE. Thứ hạng
bất biến mọi luật → chỉ mức thô. `n_buttons` = distractor → mật độ hộp.

## Phụ lục A — G0

```
cd /Users/P836901/Documents/Self-learning/thesis
# lưu khối python dưới thành g0_mention_x_exec.py rồi:
python3 g0_mention_x_exec.py
```

Cần `score_{ceiling_human,s1_seed101,ce2_s2_seed101}_raw.jsonl`, `descriptors.jsonl`, `ocr.jsonl`,
`all_forest_dict.zip`, `m2_m3_compare.py`, `m9_khop_mem.py`. Mention = biên ≥ 2,9. `exec` =
`executable`. Fail → không G2.

Mã: chép nguyên ở `harness/g0_mention_x_exec.py` (chỉ đổi `RUNS` sang `runs/` của kho WSL).

## Phụ lục B — Đường dẫn

```
thesis/m9_khop_mem.py · m2_m3_compare.py · all_forest_dict.zip
thesis-master/runs/score_{s1_seed101,s1_seed202,s2_seed101,ce2_s2_seed101,
  min_desc_seed101,ceiling_human,base}_raw.jsonl
thesis-master/runs/grpo_point/score_grpo_point_seed101_raw.jsonl
thesis-master/runs/venus/score_venus_{base,s1,s2}_2532_raw.jsonl
thesis-master/harness/dg1_cache/test_ac/{descriptors,ocr}.jsonl
thesis-master/harness/{train_config_orpo,train_config_ce2,infer_branch}.py|.yaml
```

---

## KẾT QUẢ G0 — chạy trên WSL 22/9, CPU 16 giây ⇒ **FAIL**

Mã: `harness/g0_mention_x_exec.py` + `harness/m9_khop_mem.py` + `harness/m2_m3_compare.py`, cả ba
chép nguyên từ ảnh (`report/anh_183_ban_giao_22_9/`, `report/anh_183_ma_nguon_22_9/`); chỉ đổi đường
dẫn `RUNS`/`REPO`/`ZIP` sang kho WSL (`all_forest_dict.zip` đọc từ cache HF, ghi đè bằng biến
`FOREST_ZIP`). Log: `runs/g0/g0_mention_x_exec.log`.

| nhánh | n | %mention | `exec`\|mention | `exec`\|không | `exec` toàn bộ |
|---|---|---|---|---|---|
| người | 4.448 | 9,53 | 89,39 | 74,33 | 75,76 |
| S1/101 | 4.448 | 6,81 | 92,41 | 56,74 | 59,17 |
| CE2-S2/101 | 4.448 | 6,54 | 90,03 | 57,30 | 59,44 |

Trần suy ra: người vs S1 = 2,72 × 35,67 / 100 = **+0,97 pp** · người vs CE2 = 2,99 × 32,73 / 100 =
**+0,98 pp**. Cả hai < 2,0 ⇒ **FAIL — rút preference** theo §6. Không sang G2.

Kiểm chéo: `exec` toàn bộ khớp số đã công bố (75,73 / 59,11 / 59,42) trong 0,06 điểm; lệch vì
`descriptors.jsonl` phủ 4.448 chứ không phải 4.463 bước.

### Độ nhạy theo ngưỡng biên (`runs/g0/g0_do_nhay_nguong.log`) — chẩn đoán, KHÔNG thay kết luận cổng

⚠️ Ở ngưỡng 2,9 chỉ 9,5% câu người được tính là "nhắc", trong khi §3.2 ghi 33,1% ở cùng ngưỡng. Lý do:
`score()` của `m9` là **3,0 × F1** (điểm có bậc), nên biên ≥ 2,9 gần như đòi F1 ≈ 1; con số 33,1% của
§3.2 đo bằng ranker **nhị phân** (tên +3 / OCR +3 …) mà §3 ghi là ranker đã chọn. Tức là mã G0 trong
bàn giao import scorer khác với scorer của §3.2. Quét ngưỡng để xem kết luận có phụ thuộc vào đó không:

| ngưỡng biên | %mention người / S1 | trần vs S1 | trần vs CE2 |
|---|---|---|---|
| 2,9 (khoá) | 9,53 / 6,81 | +0,97 | +0,98 |
| 2,0 | 21,27 / 17,90 | +1,05 | +0,93 |
| 1,5 | 27,81 / 22,19 | +1,84 | +1,69 |
| 1,0 | 36,69 / 30,26 | +2,33 | +2,01 |
| 0,5 | 41,91 / 34,49 | +2,66 | +2,53 |
| 0,01 (chỉ cần biên dương) | 44,18 / 36,38 | +2,78 | +2,81 |

⇒ **Không ngưỡng nào chạm 3,0.** Nới tới mức lỏng nhất (bất kỳ biên dương nào) trần cũng chỉ lên
2,8, tức ô "nằm giữa → G4" chứ không phải PASS. Ở vùng ngưỡng gần với 33,1% của §3.2 (1,0–1,5) trần
là 1,7–2,3. Vậy FAIL không phải do lệch scorer. Và trần này là **cận trên tương quan** (giả định
đưa %nhắc tên của mô hình lên bằng người thì `exec` tăng đúng theo chênh có điều kiện), nên số thật
chỉ có thể thấp hơn.

Theo §0: *"Fail bất kỳ cổng: không train đầy đủ. Viết chẩn đoán âm."*

### Chạy kèm hai script phụ thuộc (0 GPU, để kiểm mã chép từ ảnh có tái lập số của Mac không)

**`m2_m3_compare.py`** (`runs/g0/m2_m3_compare.log`, 25 s) — M2 = lọc theo (role, name, hint) của mô tả
vàng; M3 = Incremental Algorithm (Dale & Reiter 1995), cùng không gian ứng viên:

| không gian | ứng viên/màn (TB · max) | m2_loose | m2_strict | m3_strict | m3_practical |
|---|---|---|---|---|---|
| gộp nút lồng nhau | 31,2 · 162 | **3.975 = 89,37%** | 4.048 = 91,01% | 4.435 = 99,71% | 4.448 = 100,00% |
| không gộp (thô) | 86,3 · 269 | 3.512 = 78,96% | 3.596 = 80,85% | 4.223 = 94,94% | 4.430 = 99,60% |

⭐ **Tái lập:** m2_loose sau gộp = **3.975**, trùng đúng "3.975 bước mô tả vàng duy nhất" ở §3.2 ⇒ mã
chép từ ảnh chạy giống bản trên Mac. Target bị gộp mất: 0. IA (practical, gộp) dừng ở: name 3.047 ·
anchor 511 · role 375 · extremum 301 · zone 201 · ordinal 13. (Nhắc lại §3.1: IA uniqueness → `exec`
chỉ +0,19, kênh đã chết; bảng này chỉ là kiểm mã.)

**`m9_khop_mem.py`** (`runs/g0/m9_khop_mem.log`, 17 s) — khớp mềm F1+stem vs khớp nguyên văn M7,
người nghe Phi-4 (`runs/som/chon_phi4_*.jsonl`), n = 4.448:

| nhánh | ký hiệu "duy nhất" (khớp mềm) | r(biên, Phi-4 đúng) | M7 nguyên văn: duy nhất / r |
|---|---|---|---|
| người | 44,18% | 0,169 | 39,01% / 0,191 |
| S1/101 | 36,38% | 0,282 | 33,16% / 0,269 |
| Pipeline (GRPO) | 37,86% | 0,293 | 34,76% / 0,307 |

⇒ khớp với câu ở §3 *"khớp mềm F1+stem giảm hoà, `r` không tăng"*: tỉ lệ duy nhất tăng 3–5 điểm nhưng
r không tăng (người còn giảm 0,191 → 0,169).

Phi-4 đúng khi ký hiệu duy nhất vs mơ hồ: người 67,33% (n=1.965) vs 45,47% (n=2.483), chênh **+21,86** ·
S1 65,33% (1.618) vs 33,04% (2.830), **+32,29** · Pipeline 65,50% (1.684) vs 34,01% (2.764), **+31,49**.

Phi-4 đúng theo ngũ phân vị biên (không đơn điệu ở ba phân vị dưới, nhảy bậc khi biên > 0):

| nhánh | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| người | 47,36 [−3,00..−0,75] | 44,04 [−0,75..0] | 49,04 [0..+0,64] | 67,19 [+0,64..+2,00] | 67,98 [+2,00..+3,00] |
| S1 | 31,38 [−3,00..−1,20] | 34,16 [−1,20..0] | 32,51 [0..0] | 57,87 [0..+1,50] | 67,98 [+1,50..+3,00] |
| Pipeline | 29,13 [−3,00..−1,50] | 35,28 [−1,50..0] | 37,68 [0..0] | 59,66 [0..+1,50] | 67,87 [+1,50..+3,00] |

⇒ tín hiệu của scorer ký hiệu gần như **nhị phân (biên ≤ 0 hay > 0)**, khớp nhận xét §3 "bin 0,6–2,9 tệ
hơn 0–0,6 / không biên độ liên tục". Q5 bão hoà ~68% ở cả ba nhánh: khi đã nhắc tên duy nhất, người và
mô hình ngang nhau ⇒ khoảng cách nằm ở **tần suất** nhắc tên, không ở chất lượng khi đã nhắc.

### Đọc G0 cho phiên debate (tóm tắt để dán sang bên kia)

1. **G0 = FAIL**, trần suy ra +0,97 (vs S1) / +0,98 (vs CE2) ở ngưỡng khoá 2,9; cận trên lỏng nhất
   +2,8 < 3,0. Theo §0 & §6: **rút preference, không G2, không train DCRP**.
2. Vì sao nhỏ: chênh %nhắc tên người − mô hình chỉ **2,7–3,0 pp** ở ngưỡng khoá (5,4–7,8 pp ở ngưỡng lỏng),
   dù `exec` có điều kiện chênh rất lớn (+30…+37 pp). Tích hai số mới là trần; hệ số truyền thật
   (xem 0,028 của `151`) còn nhỏ hơn giả định tuyến tính này.
3. Đáng chú ý: khi câu **đã** nhắc tên duy nhất, `exec` của S1 (92,41) và CE2 (90,03) **cao hơn** người
   (89,39) ⇒ mô hình không kém ở chất lượng câu nhắc tên; nó kém vì **ít khi** chọn được phần tử có tên
   để nhắc (và trên 90%+ số bước còn lại `exec` 56–57 vs 74 của người). Nhất quán với chẩn đoán 4/9–8/9:
   điểm nghẽn là **chọn/nhìn đúng phần tử**, không phải diễn đạt.
4. Không lấy được G0 thành PASS bằng đổi scorer: tăng %mention bằng ngưỡng lỏng làm Δ(%mention) tăng
   nhưng trần vẫn < 3,0.
5. Việc còn lại theo §0 không phụ thuộc cổng: **UI-Venus 5 nhánh còn thiếu × 4.463** (S1/202, CE2,
   MIN-DESC, gui_sel, Pipeline) — robustness bắt buộc của bộ thước đã chốt; và **viết chẩn đoán âm**:
   90,4 vs 39,5 · point→câu +0,02 · khe imitation Phi-4 · SFT liều phẳng +0,05 · 66,7% byte-identical ·
   **+ G0 trần +0,97**.
6. Còn phải hỏi GV (§0 việc 1): đóng góp mô hình có bắt buộc layer/head mới không — nếu DCRP đã rút thì
   câu hỏi này quyết luôn việc hướng D (chẩn đoán âm) có đủ làm đóng góp chính hay không.

### Tái lập

```
cd harness
python3 g0_mention_x_exec.py          # 16 s, in bảng + PASS/FAIL
python3 m9_khop_mem.py                # 17 s, cần runs/som/chon_phi4_{chuan,s1_101,grpo}.jsonl
python3 m2_m3_compare.py              # 25 s
# all_forest_dict.zip: mặc định đọc cache HF HarrytheOrange/parsed_AndroidControl; đổi bằng FOREST_ZIP=...
```
Quét ngưỡng: đặt `G.THR` rồi gọi `G.main()` (log ở `runs/g0/g0_do_nhay_nguong.log`).

## Ghi chú khi chép trên WSL (22/9)

- ~~G0 chưa chạy được~~ → đã có mã nguồn từ ảnh 22/9 tối, đã chạy (mục trên). Ghi chú cũ: `m9_khop_mem.py` (hàm `content`, `score`) và `m2_m3_compare.py`
  (`D`, `TEST`, `ZIP`, `raw_nodes`, `collapse`, `area`) **không có trên máy này, không có trên
  remote**. `M.D` gần như chắc là `harness/descriptor_label_build.py` (có `name_of` và `SCREEN_AREA`
  đúng chữ ký). `all_forest_dict.zip` có ở cache HF
  (`~/.cache/huggingface/hub/datasets--HarrytheOrange--parsed_AndroidControl/…`). Ba tệp `score_*_raw.jsonl`
  và `descriptors.jsonl`/`ocr.jsonl` đều có.
- Chưa dựng lại `m9`/`m2_m3` từ mô tả ranker ở §3 vì G0 đặt ngưỡng cứng 2,0/3,0 lên kết quả của
  chính scorer đó: bản dựng lại lệch một chi tiết là cổng đọc sai.
- ⚠️ Mâu thuẫn so với `CLAUDE.md`: file này khoá lại `exec` làm primary và D.3 là confirmatory,
  trong khi chỉ đạo 14/9 đưa bộ ba AitW 77,3 · D.3 67,0 · exec 60,1 vào luận văn. Mục 2 ở đây ghi AitW
  là Appendix.
