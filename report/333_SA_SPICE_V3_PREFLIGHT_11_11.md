# SA-SPICE-v3 — PREFLIGHT 11/11/2026

Thi hành mục 17 của `report/SA_SPICE_v3_extracted_verified.md` (gọi tắt **memo**): chỉ PREFLIGHT, 0 GPU, không đụng C1/test để chọn gì.

> **Kết luận: NO-GO GPU.** Hai blocker cứng của bản ACTION 10/11 (thiếu SFT-cont, thiếu ảnh) đã **gỡ được**. Còn năm việc chặn: dựng split (cần duyệt 4 diễn giải + ~100 phút CPU), audit verifier (gán nhãn tay), probe merge SFT-cont, protocol freeze (5 câu §16 của memo) và ngân sách 27 lượt.

Mọi tệp ở `runs/sa_spice_v3/preflight/`. Nhãn: **[đo]** = chạy ra số hôm nay, **[suy]** = ước lượng.

## 1. SFT-cont weights / ảnh / metadata

| hạng mục | trạng thái | bằng chứng |
|---|---|---|
| SFT-cont adapter | ✅ có ở máy | `_bundles/colab_rl_test/kit/sft_final/`, md5 `113e2a3e…` **trùng** md5 kernel `luoi-test-u-3` đã chấm test (exec 60,16, report/320 §18) [đo] |
| S1 adapter | ✅ | `kit/adapter_s1_seed101/`, tree `c76169db…` |
| 1.000 câu nhắc SFT-cont | ✅ | `_bundles/luoi/ds/prompt_keys_ck500.json` (sft_tiep.py assert trùng thứ tự ck500); 630 click · 120 scroll · 81 type · 69 wait · 65 open_app · 35 back [đo] |
| Base Qwen2.5-VL-3B, UGround-V1-2B | ✅ HF cache | tree hash trong `input_manifest.json` |
| Ảnh pool | ✅ **64.567/64.567** ảnh ở `harness/dg1_cache/train_ac/images` (30 GB) | [đo]. Bản ACTION 10/11 ghi "repo không có ảnh pool" — ảnh không ở trong git nhưng có trên đĩa |
| Package ID | ✅ từ cây trợ năng `all_forest_dict.zip` (HF cache) | Gate B 10/11: 31.159/31.187 bước chạm có package. Bước 0 màn home không có package ⇒ lấy package theo episode |
| Scorer | ✅ local: pycocoevalcap + spice-1.0.jar + lib, Java 1.8.0_504, Python 3.12.3, sacrebleu 2.6.0 | ⚠️ CoreNLP jars chỉ có trên Kaggle (`trangphngngc/corenlp-360-jars`), phải ghim hash trong log lượt chạy |
| `sft_cont_merged` | ❌ chưa dựng | cần probe S1-hoà + adapter bật vs bản đã hoà, so logits/greedy (bậc T4, ~15 phút [suy]) |

## 2. Lineage + split spec

**Lineage** (`harness/sa3_lineage.py` → `lineage.json`, `excl_episodes.json`) [đo]:

- Kiểm tách episode: val400 · val600 · val_cham400 (chứa C1) · val_cham600 · test_ac đều **0 episode chung** với pool `train_tru_val.jsonl`.
- Quét 3.744 tệp json/jsonl ở `runs/ _bundles/ _scripts/`, cộng `p1_sample_keys.json` (pool 4.000 câu nhắc gốc của ck500) và 2.000 câu nhắc GRPO-point **tái dựng bằng chính `grpo_point.dung_hang`** (không có tệp khoá).
- 133 artifact "tập con" ⇒ **loại 4.633 episode**. Pool còn **31.442 bước / 7.916 episode** (19.213 click · 3.718 scroll · 2.529 open_app · 2.448 wait · 2.204 type · 1.228 back · 86 long_press). Đủ cho 600 + 1.500 + 1.000 = 3.100 episode.
- 10 artifact phủ ≥50% pool (bản sao train, `descriptors_ten`, `tage_neg`, dữ liệu RA-SFT) không loại được: đúng phạm vi "S1-seen" của memo §4.3.
- ⚠️ Lineage chỉ thấy artifact có trên máy. Lượt nào chỉ để lại output trên Kaggle/Drive mà dùng tập câu nhắc khác ck500 thì không bắt được; theo log hiện có, mọi lượt lưới RL dùng chung `prompt_keys_ck500`.

**Split spec** (`split_spec.json`) + mã `harness/sa3_split.py` (selftest ĐẠT; đã thử pHash + package trên ảnh và cây thật). Bám §4.2 của memo: khoá `(source_dataset, episode_id, step_id)`, strata dominant action × {1–4, 5–9, ≥10}, sort SHA256 cố định, largest remainder, TRAIN một bước/episode theo SHA256 bước, pHash DCT 63 bit Hamming ≤4, MinHash 3-gram ≥0,90, manifest in sha256 + đếm theo action.

Bốn chỗ memo không nói đủ, **cần user duyệt trước khi build**:

1. **Màn chung**: ảnh near-dup xuất hiện ở ≥20 episode (home, launcher, màn chờ) không tạo cạnh. Không có luật này thì bước 0 màn home của mọi episode open_app nối gần hết pool thành một cụm.
2. Nhóm near-dup nội pool bị loại cả nhóm (thay vì giữ cùng split), để quota đếm đúng.
3. Cặp MinHash ≥0,90 mặc định loại; xét tay chỉ được khôi phục, không thêm loại sau khi thấy split.
4. Package cụm theo episode (đa số, bỏ launcher/systemui).

Chạy: `sa3_split.py hash` (~43 phút cho ảnh pool, ~100 phút nếu băm cả ảnh đã loại + test để dò trùng chéo [đo trên 150 ảnh: 82 ms/ảnh]) rồi `sa3_split.py build` (vài phút). Theo luật "việc CPU dài lên Kaggle", lượt hash phải đẩy 30 GB ảnh lên Kaggle — rẻ hơn là chạy máy nhà một lần, **user chọn**.

## 3. Action verifier — kế hoạch audit

**Độ phủ trusted đo trên pool** (gold-text action theo `classify` của Gate B so action log) [đo]:

| action | n | khớp | lệch | không suy được |
|---|---|---|---|---|
| tap | 19.299 | 93,4% | 2,1% | 4,5% |
| scroll | 3.718 | 97,6% | 0,3% | 2,1% |
| open_app | 2.529 | 96,4% | 2,4% | 1,2% |
| back | 1.228 | 91,9% | 0,9% | 7,2% |
| type | 2.204 | 73,5% | 0,6% | 25,9% |
| **wait** | 2.448 | 0,4% | **95,3%** | 4,3% |

⇒ Câu chuẩn ở bước `wait` gần như không bao giờ nói "wait", nên điều kiện 3 (§5) làm **mọi bước wait thành untrusted, A = 0,5**. Đây là thiết kế đúng memo, không phải lỗi; khai trong bài.

**Thiết kế audit** (khoá trước, mù với output verifier):

- Tập audit lấy từ **TRAIN-v3 và DEV-v3**, không từ CONFIRM-v3. Ứng viên = 8 mẫu SFT-cont (T = 1,0) trên bước được chọn; cần một lượt sinh T4 [suy ~1–2 h].
- Tầng: action gold ∈ {tap, scroll, back, type, open_app} × nhãn verifier ∈ {correct, known-wrong}; toggle (enable/disable/turn on/off) là tầng riêng trong tap.
- Cỡ mẫu từ cận Clopper–Pearson một phía 95% [đo, `input_manifest.json`]:

| mục tiêu | 0 lỗi | 1 lỗi | 2 lỗi | 3 lỗi |
|---|---|---|---|---|
| cận dưới PPV > 98% (mỗi nhãn) | **149** | 236 | 313 | 386 |
| cận trên false reject / false accept < 5% (mỗi action) | **59** | 93 | 124 | 153 |

- Kế hoạch đơn giản nhất: mỗi tầng (nhãn × action) gán **236 mẫu** (chịu được 1 lỗi cho PPV), hai người gán độc lập, bất đồng xử lý trước khi mở verifier. 5 action × 2 nhãn ⇒ ~2.360 câu gán tay [suy]. Tầng nào không đủ mẫu (vd back known-wrong hiếm) thì gate của action đó không đạt được ⇒ action đó buộc A = 0,5, và nếu tap/scroll không đạt thì **SA-SPICE-v3 NO-GO** (§5).
- ⚠️ Gate này là việc gán nhãn tay lớn nhất của cả nghiên cứu; trước đây user đã quyết không chấm tay 100 câu (6/9). Nếu không gán tay được ⇒ NO-GO theo §5, không có đường vòng.

## 4. Đóng băng formula / seed / checkpoint / analysis

`protocol_freeze.json` chép nguyên công thức §2, sáu arm factorial + ba baseline, seed 401/503/907 (cấm 101), recipe GRPO §7, contract evaluator §7bis, checkpoint 100–500 + luật one-SE, feasibility, sáu phép primary Holm, ba biên NI, stop rules. Trạng thái **DRAFT**: thành FROZEN khi user trả lời §16 và có commit + timestamp trước mọi rollout DEV-v3.

## 5. Ngân sách [suy]

- GRPO G = 8 trên T4 đã đo 148–163 s/bước ⇒ ~21–22 h mỗi lượt 500 bước ⇒ 27 lượt ≈ **570–600 giờ T4**.
- Chấm DEV: ~2.400 bước/checkpoint (7.916 episode trung bình ~4 bước) × 5 checkpoint × 27 lượt ⇒ thêm ~130 giờ T4.
- Tổng ~700 giờ T4 ≈ **8 tuần dùng trọn hạn mức ba tài khoản Kaggle** (90 h/tuần), chưa tính CONFIRM, audit và lượt hỏng. Mốc bảo vệ 3/2027 còn ~16 tuần.

## 6. GO/NO-GO

**NO-GO GPU.** Theo stop rule §13 của memo:

| điều kiện §13 | trạng thái |
|---|---|
| split/manifest/hash | ❌ spec + mã xong, chưa build (chờ duyệt §2 + chạy hash) |
| SFT-cont weights / ảnh | ✅ |
| action verifier gate | ❌ chưa audit |
| SPICE parse fail-open | ⚠️ chưa có `spice_failclosed.py`; viết ở Phase 1 code CPU |
| smoke/resume/merge/logits | ❌ chưa probe `sft_cont_merged` |

## 7. User phải quyết (memo §16, agent không tự quyết)

1. Chấp nhận dừng RGTC và đăng ký SA-SPICE-v3?
2. SFT-cont/ảnh/metadata: **đã có trên máy**, chỉ cần xác nhận dùng `kit/sft_final` (md5 `113e2a3e…`).
3. Duyệt ~700 giờ T4 cho 27 lượt?
4. Chấp nhận kết quả âm, không đổi 0,8/0,2?
5. Có người gán nhãn audit verifier (~2.400 câu) / human eval 300 prompt / grounder thứ hai?

Cộng: duyệt bốn diễn giải split (§2) và chọn chỗ chạy hash (Kaggle hay máy nhà).

## 8. Sửa memo §5 + chạy thử audit (11/11, user quyết)

**User 11/11:** "ngân sách thì ko cần lo" ⇒ câu 3 §16 đã duyệt. "Claude chấm thay đi nha, rồi chạy thử đã, người chấm mẫu nhỏ thôi" ⇒ **sửa memo §5 trước khi có bất kỳ output DEV-v3 nào**: người gán nhãn audit là Claude (mù với nhãn verifier), người chấm lại một mẫu nhỏ để kiểm Claude. Phải khai trong bài; claim "audit độc lập bởi người" không còn dùng được.

Mã: `harness/sa3_action_verify.py` (verifier + build/score audit). Nguồn câu ứng viên chạy thử: 8 mẫu + greedy của **ck500** trên 2.000 bước train của RAFT 314 (`runs/rd314/R/raft_mau_{0,1}.jsonl`). Các episode này đều nằm trong `excl_episodes.json` nên không thuộc split nào. Audit thật phải dùng mẫu SFT-cont trên TRAIN/DEV-v3.

| lượt | verifier | mẫu | Claude khớp verifier | ghi chú |
|---|---|---|---|---|
| pilot 1 | v1 (= `classify` của R4/C1) | 300 (30/ô) | 292/300; ô tap‑known_wrong **22/30** | lỗi: từ khoá phía sau thắng động từ đầu câu ("Click on the **pause** button" → wait, "click on the **type** filter" → type) |
| pilot 2 | **v2** (động từ chạm đầu câu ⇒ tap; câu chuẩn bấm mũi tên back ↔ ứng viên "go back" ⇒ A = 0,5) | 252 mẫu **mới** (bỏ mọi cặp pilot 1) | **250/252**, 0 lỗi rõ, 2 ca mơ hồ | nguồn chỉ có 2 câu type‑known_wrong, 10 open_app‑known_wrong |

Giới hạn phải khai:
- n = 30 mỗi ô thì cận dưới PPV tối đa 0,905, **không thể** chạm 98% (cần ≥149). Đây chỉ là chạy thử.
- Claude vừa viết verifier vừa chấm, và biết luật regex ⇒ người chấm không độc lập với verifier. Mẫu người chấm lại dùng để kiểm điểm này.
- v2 được sửa sau khi thấy pilot 1. Pilot 2 dùng mẫu mới nên con số 250/252 không bị lạc quan do sửa cho khớp, nhưng v2 phải khoá version/hash (`sa3-verify-2`) trước audit thật.

Mẫu người chấm: `runs/sa_spice_v3/audit_pilot2/CHAM_TAY_MAU_NHO.md` (40 dòng, 4 dòng/ô + 2 ca mơ hồ, mù với cả Claude lẫn verifier).

## 9. Người chấm mẫu nhỏ + verifier v3 (11/11)

**Người chấm 40 dòng** (trang `audit_pilot2/CHAM_TAY.html`, mù với Claude và verifier; nhãn ở `audit_pilot2/human_labels.jsonl`):

| verifier v2 | người: cùng loại | khác loại | không rõ |
|---|---|---|---|
| A = 1, 20 dòng | **20** | 0 | 0 |
| A = 0, 20 dòng | 5 | 13 | 2 |

Người = Claude 33/40. Cả 7 dòng lệch là **đường đi khác hợp lý** (bấm ô nhập ↔ gõ chữ, quay lại ↔ bấm nút back/menu, quay lại ↔ mở app): người chấm theo "câu này có làm được việc trên màn hình không", Claude/verifier chấm theo động từ. Claude đọc lại 242 dòng v2 chấm 0 (cả hai pilot, kèm mục tiêu + bước trước): trong **cùng một cặp** thao tác lẫn cả đường khác hợp lý lẫn sai thật (vd. gõ → bấm: "Click on the search bar" hợp lý, "Click on the save icon" trước khi gõ thì sai), nên luật theo chữ không tách được.

**Quyết định (user duyệt 11/11: "bạn thấy hợp lý thì làm"):** verifier **v3** (`sa3-verify-3`):
- cùng loại → A = 1; khác loại → **A = 0,5**; chỉ toggle ngược chiều → A = 0; untrusted/unknown → 0,5 như cũ.
- Đo trên 7.558 cặp RAFT: correct 6.008 · untrusted 738 · mismatch 554 · unknown 248 · back_equiv 10 · **toggle 0** ⇒ thực tế A ∈ {0,5; 1}. Phần action của reward thành **thưởng khớp thao tác** (+0,1 so với Sparse-SPICE), không còn phạt.
- Gate §5 còn lại: cận dưới PPV của nhãn A = 1 > 98% mỗi action (≥149 câu/action nếu 0 lỗi). Gate "known wrong" không có mẫu ⇒ nếu audit thật không đủ 149 ca toggle thì toggle cũng về 0,5. Pilot hiện có: Claude 150/150 + người 20/20 trên nhãn A = 1.
- Phải khai: đây là sửa memo **trước** mọi output DEV-v3; R4 của pilot C1 dùng cổng cứng nên càng khác v3.

**Giới hạn không sửa:** thước exec chính chỉ so với một đáp án, nên cũng chấm thấp đường đi khác hợp lý. Giới hạn chung của đánh giá offline từng bước trên AndroidControl; khai trong bài, không đổi thước.

## 10. Split v3 đã dựng + sàng reward mức 1 (11/11)

**Băm ảnh** 71.525 bước (train_ac + test_ac), `runs/sa_spice_v3/preflight/hash_steps.jsonl`, ~1,5 h CPU máy nhà (ảnh 30 GB chỉ có ở đây).

**Sửa luật near-dup (spec v2), trước mọi output mô hình.** Luật memo nguyên văn (pHash ≤4 ⇒ loại, bắc cầu) nối 9.203 episode thành một cụm và loại 5.270/7.916 episode, vì AndroidControl lặp màn chính của cùng một app qua nhiều tác vụ. Tính cạnh trực tiếp vẫn loại 4.619. Luật dùng: **trùng mục** = một cặp bước ảnh pHash ≤4 **và cùng câu chuẩn** (chuẩn hoá), hoặc goal MinHash 3-gram ≥0,90; cạnh trực tiếp, không bắc cầu. Bỏ luật "màn hình chung ≥20 episode" (không cần nữa). Thêm hai luật lọc trước quota: loại episode có câu chuẩn trống (44), loại episode không xác định được package (46), để mọi dòng DEV/CONFIRM có cụm (§7bis).

| | episode | bước | package | click / scroll / type / back / open_app / wait |
|---|---|---|---|---|
| TRAIN-v3 | 1.000 | 1.000 | 369 | 616 / 135 / 49 / 39 / 85 / 70 |
| DEV-v3 | 600 | 2.223 | 275 | 1.328 / 290 / 143 / 109 / 170 / 172 |
| CONFIRM-v3 | 1.500 | 5.601 | 451 | 3.341 / 776 / 356 / 234 / 415 / 460 |

Loại: trùng mục với tập loại/test 1.341 · trùng mục nội pool 679 · câu chuẩn trống 44 · thiếu package 46 ⇒ còn 5.806 episode chọn được. SHA-256 từng split ở `runs/sa_spice_v3/split/split_manifest.json`. 1.034 cặp goal MinHash ≥0,90 chờ xét tay (`minhash_can_xet_tay.json`); xét tay chỉ được khôi phục episode. CONFIRM-v3 chưa mở (chỉ đếm).

**Sàng reward mức 1 (user duyệt 11/11).** Câu hỏi: reward nào xếp câu exec = 1 trên câu exec = 0 trong nhóm 8 mẫu SFT-cont, trên TRAIN-v3 (không dùng C1). Chỉ để quyết đi/dừng trước 27 lượt GPU, không chỉnh hệ số.
1. Kernel 1 `trangphuongngoc/sa3-mau-k1` (T4×2): hoà S1 → probe ghép SFT-cont (logits + greedy) → greedy + 8 mẫu (T = 1,0) trên 1.000 câu nhắc. Mã `harness/sa3_mau.py`, `_bundles/sa3_mau/`.
2. Kernel 2 (T4×2): UGround chấm exec 9 câu × 622 bước chạm. `_bundles/sa3_cham/make_k2.py` (khuôn runbook 251).
3. Kaggle CPU: `harness/sa3_reward_screen.py`: 9 reward + concordance / zero-std / oracle uplift + KTC95 cụm package cho SA − từng reward; kèm phân bố K_g và A.

**Kết quả sàng mức 1 (11/11, kernel `trangphngngc/sa3-screen-k3` v2, Kaggle CPU).** 622 bước chạm · 263 package · greedy exec 61,41 · trung bình 8 mẫu 55,55 · A = 1 ở 6.025/8.000 câu, A = 0,5 ở 1.975. v1 lỗi do gửi câu chuẩn sang SPICE dạng list (đã sửa `sa3_reward_screen.py:159`, kiểm SPICE thật trên WSL).

| reward | concordance | zero-std | oracle uplift | SA − reward: concordance [KTC95 cụm package] | SA − reward: oracle pp |
|---|---|---|---|---|---|
| SPICE-MATCH | 0,6766 | 5,79% | +7,22 | **+0,094** [+0,069; +0,119] | +1,86 [+0,66; +3,06] |
| Action-SPICE | 0,7162 | 4,18% | +8,18 | **+0,055** [+0,035; +0,074] | +0,90 [−0,14; +1,90] |
| FIXED | 0,7470 | 0,96% | +8,60 | **+0,024** [+0,012; +0,037] | +0,48 [−0,32; +1,36] |
| FIXED+A | 0,7567 | 0,96% | +8,92 | **+0,014** [+0,005; +0,025] | +0,16 [−0,52; +0,92] |
| Sparse-SPICE | 0,7634 | 0,96% | +8,76 | **+0,007** [+0,003; +0,012] | +0,32 [0,00; +0,81] |
| **SA-SPICE-v3** | 0,7708 | 0,96% | +9,08 | — | — |
| chrF | **0,7941** | 1,13% | **+10,85** | **−0,023** [−0,046; −0,002] | **−1,77** [−3,09; −0,58] |
| SPIDEr-like | 0,7788 | 1,93% | +9,73 | −0,008 [−0,030; +0,012] | −0,64 [−1,74; +0,36] |
| ROUGE-L | 0,7802 | 2,25% | +9,93 | −0,009 [−0,035; +0,016] | −0,85 [−2,41; +0,61] |

Đọc: mỗi thành phần của SA-SPICE-v3 (action, chrF trộn, sparse fallback, phạt độ dài) đều cộng thêm concordance có ý nghĩa so với các bản SPICE con, nhưng **chrF đứng một mình xếp câu exec tốt hơn SA-SPICE-v3**, có ý nghĩa ở cả hai đại lượng; SPIDEr-like và ROUGE-L ngang. Tái lập đúng chiều pilot C1 (chrF 0,8355 > R4 0,8161). Sàng này chỉ chẩn đoán offline (memo §13 không có luật dừng theo sàng); quyết chạy mức 2 (27 lượt) là của user. Tệp: `runs/sa_spice_v3/screen/out/`.

## 11. Mức 2: lượt đầu (11/11, user quyết)

User quyết chạy mức 2 trước **một seed**, hai arm song song trên hai GPU của cùng một kernel: **SA-SPICE-v3** (GPU0) và **chrF** (GPU1, đối chứng mạnh nhất theo sàng mức 1). **Seed 101** theo quyết định của user ("cho dễ báo cáo"), **lệch memo §6** (memo khoá 401 · 503 · 907 và ghi "Seed 101/C1 không tham gia"). Phải khai khi báo: thiết kế reward đã nhìn pilot C1 trên mẫu S1/101; seed chỉ đổi thứ tự xáo câu nhắc và lấy mẫu, không đổi dữ liệu, và không ghép cặp được với ck500 (khác điểm xuất phát và tập câu nhắc).

Mã `harness/sa3_grpo.py`: vòng train của `grpo_luoi.py` (GRPO, LoRA mới cỡ S1, KL β 0,04 về sft_cont_merged, DAPO, group std, G 8, 2 câu nhắc/update, lr 1e-5, 500 update), thay tập câu nhắc = 1.000 câu TRAIN-v3 và reward = đúng hàm `rewards()` của sàng. Kiểm WSL: selftest 9 arm đạt; reward SA-SPICE-v3 trên 8 mẫu thật của một bước khớp điểm sàng tuyệt đối (lệch 0).

**Phiên 1 (kernel `uyenle0712/sa3-grpo-u-1`, 11/11 21:00 → 12/11 ~04:30 VN, T4×2) COMPLETE, cắt ở trần 7,5 h.** Kiểm hoà greedy trùng kernel 1 **3/3**; `[LoRA mới]` 14.966.784 tham số học, bằng S1; 1.000 câu nhắc. Số train, không phải số đánh giá:

| arm | update đã chạy | điểm lưu | thưởng 1–25 → 76–100 → 151–cuối | KL cuối | s/update | số từ TB đầu → cuối |
|---|---|---|---|---|---|---|
| SA-SPICE-v3 | 182 | ck100 · ck150 · ck175 | 0,571 → 0,573 → 0,605 | 0,013 | 146 | 6,9 → 7,8 |
| chrF | 189 | ck100 · ck150 · ck175 | 0,565 → 0,556 → 0,633 | 0,032 | 140 | 7,0 → 8,5 |

Không sụp độ dài, không rỗng. Còn ~325 update mỗi arm (~13 h trên T4). Hạn mức Kaggle của cả ba tài khoản hết tới 14/11 ⇒ chạy tiếp trên Colab bằng `_bundles/sa3_grpo/k_sa3-grpo-c-2/sa3-grpo-c-2_colab.ipynb` (dựng bằng `_bundles/colab_tu_kaggle.py` từ notebook Kaggle cùng mã, tiếp từ ck175 trong output phiên 1). Log ở `runs/sa_spice_v3/grpo/u_1/`. Nếu kiểm hoà trên GPU Colab lệch 1/3 câu thì phải khai ở đây.

**Phiên 2 (kernel `uyenle0712/sa3-grpo-u-2`, 14/11 07:25 → 17:15 VN, T4×2) dừng vì LỖI, không phải trần giờ.** `[tiếp từ] checkpoint-175` · `[nạp default] |lora_B| 0 → 5,94 / 6,22` đúng. Cả hai arm chạy tới khoảng bước 415 rồi chết ở bước lấy mẫu: `probability tensor contains either inf, nan or element < 0` (logit fp16 NaN, cùng lỗi `sa3-mau-k1`). Trước đó có hai bước `grad_norm` nan mỗi arm (SA 12/188, chrF 98/398) nhưng trọng số mọi điểm lưu đều lành: 0/504 tensor NaN, `|lora_B|` tăng đều (SA 0,31 → 0,68; chrF 0,33 → 0,70 ở ck100 → ck400). Điểm lưu ck100/200/300/400 ở dataset `uyenle0712/sa3-ck-u2` (máy nhà `_bundles/sa3_grpo/ck_u2/`, gitignore); log ở `runs/sa_spice_v3/grpo/u_2/`.
Vá 14/11: `sa3_grpo.py` bọc `model.generate` thêm `remove_invalid_values=True` (mặc định bật, cờ tắt `--khong-chan-nan`; chỉ thay logit đã hỏng, in `[chặn NaN]`). **Phải khai:** từ ck400 tới ck500 lấy mẫu có bản vá này, trước đó không. Phiên 3 `uyenle0712/sa3-grpo-u-3` (trần 11 h) chạy tiếp từ ck400, còn 100 update (~4 h).

**Phiên 3 (kernel `uyenle0712/sa3-grpo-u-3`, 14/11 ~18:00 → ~22:15 VN, T4×2) COMPLETE, cả hai arm tới bước 500.** Log có `[tiếp từ] checkpoint-400` · `[chặn NaN]` · `[nạp default] |lora_B| 0 → 9,02 / 9,39` · `[LoRA mới]` 14.966.784. Trọng số ck400 · ck500 · final: 0/504 tensor NaN. `log_history.json` đủ 500 bước, khớp số tính từ log phiên 1–2 ở ck100–400. Điểm lưu ở máy nhà `_bundles/sa3_grpo/ck_u3/` (gitignore, 3,1 GB); log ở `runs/sa_spice_v3/grpo/u_3/`.

Số train (thưởng = TB 50 bước trước điểm lưu, sai số ~±0,025; KL = TB 20 bước cuối):

| arm | ck100 | ck200 | ck300 | ck400 | ck500 |
|---|---|---|---|---|---|
| SA-SPICE-v3 thưởng | 0,608 | 0,618 | 0,575 | 0,615 | 0,609 |
| SA-SPICE-v3 KL | 0,004 | 0,025 | 0,025 | 0,042 | 0,043 |
| chrF thưởng | 0,596 | 0,644 | 0,593 | 0,654 | 0,628 |
| chrF KL | 0,009 | 0,036 | 0,072 | 0,045 | **0,114** |

Thưởng train phẳng trong nhiễu ⇒ không dùng để chọn điểm lưu. **chrF ck500 vượt ngưỡng KL 0,10 của memo §8 ⇒ không feasible**; SA-SPICE-v3 mọi điểm lưu ≤ 0,08.

Kế hoạch DEV-v3 (user 14/11): chấm trước **một điểm lưu mỗi arm** — SA-SPICE-v3 ck500, chrF ck400 (điểm feasible muộn nhất) — cùng SFT-cont làm mốc; chỉ khi kết quả ổn mới chấm đủ ck100–500 và chọn chính thức theo luật 1 SE. **Lệch memo §8 (chấm thử một điểm trước), phải khai.** Một seed (101), memo đòi ba ⇒ kết quả chỉ chỉ hướng, chưa mở CONFIRM-v3.

**Chấm DEV-v3 lượt đầu (14/11 22:36 VN):** kernel `uyenle0712/sa3-dev-a` (SFT-cont · SA-SPICE-v3 ck500) và `trangphngngc/sa3-dev-b` (SA-SPICE-v3 ck400 · chrF ck400), mỗi GPU một mô hình: greedy 2.223 bước DEV-v3 (`harness/sa3_dev.py`, cùng câu nhắc/giải mã với `sa3_mau.py`, mô hình = sft_cont_merged đã kiểm hoà + adapter GRPO) rồi UGround chấm exec 1.338 bước chạm. Thêm SA ck400 để có phép so cùng số bước với chrF ck400. Bước không chạm đọc ở máy nhà từ tệp câu.

## 12. Kết quả DEV-v3 lượt đầu (15/11)

Kernel `uyenle0712/sa3-dev-a` và `trangphngngc/sa3-dev-b` COMPLETE. Tệp ở `runs/sa_spice_v3/dev/{a,b}/` (câu `dev_*.jsonl`, chấm UGround `score/score_dev_*_raw.jsonl`, log). Đọc bằng `python3 -I harness/sa3_dev_doc.py` → `runs/sa_spice_v3/dev/doc_dev.json`. **Số DEV, một seed (101), cấm trích ra bài.** Bootstrap cụm như `score_run` (540 cụm).

| | exec (1.338 bước chạm) | đúng loại thao tác, bước không chạm (667 bước gold tin được) | back |
|---|---|---|---|
| SFT-cont | 62,93 [60,04; 65,79] | 83,96% | 84/104 |
| SA-SPICE-v3 ck500 | **64,35** [61,43; 67,27] | 78,41% | 56/104 |
| SA-SPICE-v3 ck400 | 64,28 [61,36; 67,19] | 81,56% | 60/104 |
| chrF ck400 | 63,98 [61,06; 66,87] | 77,06% | 57/104 |

Ghép cặp exec: SA ck500 − SFT-cont **+1,42 [+0,29; +2,59]** cứu 40 phá 21 p=0,020 · SA ck400 − SFT-cont +1,35 [+0,37; +2,38] p=0,013 · chrF ck400 − SFT-cont +1,05 [−0,22; +2,33] p=0,11 · **SA ck400 − chrF ck400 +0,30 [−0,57; +1,20] p=0,61** · SA ck500 − ck400 +0,07.

Bước không chạm (đúng loại theo `classify` của verifier v3, gold tin được): SA ck500 − SFT-cont **−5,55 [−8,17; −3,12]** (cứu 17 phá 54) · SA ck400 −2,40 [−4,67; −0,29] · chrF ck400 −6,90 [−9,29; −4,71]. Phần tụt gần như toàn ở **back** (84 → 56–60): ở ck500, 28 câu back của SFT-cont thành câu chạm, chỉ 6/28 còn nói "back/arrow" ⇒ 22 câu chỉ sang phần tử khác, lỗi thật, không phải do bộ phân loại. input_text cũng giảm ở ck500 (88 → 78) và chrF (→ 75); scroll giữ hoặc tăng nhẹ.

Đọc: SA-SPICE-v3 tăng exec có ý nghĩa so SFT-cont (~+1,4, cùng cỡ ck500 − S1 trên test), nhưng **không hơn chrF** (thứ tự giữ như sàng mức 1 về tín hiệu yếu), và tái lập đúng tác hại back của ck500 trên test (`report/261` §6). ck400 ít hại back hơn ck500 với exec gần như bằng. Câu trùng nguyên văn gold: SFT-cont 706/2.223 · SA ck500 633 · ck400 650 · chrF 612. Độ đo văn bản: đang tính trên Kaggle CPU (§12b).

### 12b. Độ đo văn bản DEV-v3 (xong 15/11 ~07:00 VN, kernel chạy ~20 phút)
15/11 đẩy `trangphngngc/chu-sa3-dev-15-11-cpu` (Kaggle CPU, dataset `trangphngngc/chu-sa3-dev-15-11` + `corenlp-360-jars`), mã `harness/chu_sa3_dev_15_11.py` (dùng lại `ktc_chu_27_10.tung_buoc`): BLEU-4 · ROUGE-L · CIDEr-D · SPICE · chrF · BERTScore có KTC ghép cặp bootstrap cụm episode (B = 2.000), METEOR mức kho; trên cả 2.223 bước và tập con 1.338 bước chạm. Gói `_bundles/chu_sa3_dev_15_11/`. Xong tải về `runs/sa_spice_v3/dev/chu/`.

**Kết quả** (`runs/sa_spice_v3/dev/chu/chu_sa3_dev_15_11.json`; tự kiểm chrF trọn kho đạt; 600 cụm episode; số dev, không trích):

| nhánh (2.223 bước) | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| SFT-cont | 60,17 | 43,16 | 74,62 | 539,27 | 55,47 | 69,79 | 73,69 |
| SA ck500 | 57,53 | 42,34 | 73,24 | 518,85 | 53,72 | 69,03 | 72,25 |
| SA ck400 | 57,02 | 42,88 | 73,76 | 525,45 | 54,46 | 69,76 | 72,61 |
| chrF ck400 | 54,46 | 42,38 | 72,62 | 507,08 | 52,83 | 69,43 | 71,69 |

| nhánh (1.338 bước chạm) | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| SFT-cont | 56,79 | 40,66 | 71,98 | 463,70 | 48,39 | 66,57 | 70,85 |
| SA ck500 | 56,25 | 41,12 | 72,30 | 463,43 | 48,10 | 67,19 | 70,88 |
| SA ck400 | 54,85 | 41,29 | 71,97 | 461,58 | 48,09 | 67,57 | 70,56 |
| chrF ck400 | 52,91 | 41,32 | 71,69 | 449,02 | 47,11 | 67,90 | 70,31 |

Ghép cặp (KTC95; * = loại 0):
- Toàn bộ: SA ck400 − SFT-cont BLEU-4 −3,15* · ROUGE-L −0,87* · CIDEr-D −13,82* · SPICE −1,01* · chrF −0,04 · BERT −1,08*. SA ck500 − SFT-cont: cả sáu âm*. chrF ck400 − SFT-cont: năm âm* (chrF −0,37 phủ 0).
- Toàn bộ: SA ck400 − chrF ck400 BLEU-4 +2,57* · ROUGE-L +1,14* · CIDEr-D +18,37* · SPICE +1,63* · chrF +0,33 · BERT +0,92*. SA ck400 − ck500: ROUGE-L, CIDEr-D, SPICE, chrF đều nghiêng về ck400*.
- Bước chạm: SA ck400 − SFT-cont BLEU-4 −1,94* · chrF +1,00* · bốn độ đo còn lại phủ 0. SA ck400 − chrF ck400 BLEU-4 +1,94* · CIDEr-D +12,55* · SPICE +0,99 [−0,22; +2,10].

Đọc: phần tụt so SFT-cont trên toàn bộ chủ yếu ở bước không chạm (cùng chỗ tụt đúng loại thao tác ở §12); trên bước chạm SA ≈ SFT-cont, chỉ BLEU-4 thấp hơn. SA hơn chrF rõ ở BLEU-4/CIDEr-D (cả hai phạm vi) và SPICE (toàn bộ), dù exec hai nhánh ngang nhau. Trên toàn bộ ck400 hơn ck500 ở 4/6 độ đo có KTC ⇒ thêm căn cứ cho việc chọn ck400 ở §13.

## 13. Chọn điểm lưu và chấm tập kiểm (15/11)

**Chọn SA-SPICE-v3 ck400, chấm một nhánh trên tập kiểm.** Căn cứ, theo các tiêu chí đã viết sẵn trong `protocol_freeze.json` (bản DRAFT, một seed thay vì ba ⇒ phải khai):
- Tiêu chí khả thi so SFT-cont: bước không chạm tụt tối đa 3 điểm, scroll + back gộp tụt tối đa 5 điểm, KL ≤ 0,10.
  - SA ck400: −2,40 không chạm · scroll+back 80,36 → 76,74 (−3,6) · KL 0,042 ⇒ **khả thi**.
  - SA ck500: −5,55 · −5,2 ⇒ không khả thi. chrF ck400: −6,90 · −7,2 ⇒ không khả thi (chrF ck500 KL 0,114 cũng không).
  - Đọc "scroll_back_drop_max_pp" là ngưỡng gộp scroll + back; nếu đọc từng loại thì back của mọi nhánh đều trượt (84 → 56–60/104). Phải khai cách đọc này.
- Luật một SE: ck400 sớm hơn và exec ngang ck500 (+0,07 [−0,60; +0,77]) ⇒ chọn ck400. ck100–300 chưa chấm DEV (lệch memo §8, đã khai ở §11).
- Không chấm chrF ck400 trên tập kiểm vì nhánh này không qua tiêu chí khả thi trên DEV. Không chấm cả ck400 lẫn ck500 rồi chọn theo tập kiểm.
- Không mở CONFIRM-v3: điều kiện mở (SA > SPICE-MATCH, SA > Sparse-SPICE) cần hai arm chưa train. Tập kiểm 4.463 bước là nơi mọi nhánh lưới RL đã báo số, nên dùng để so với ck500 / SFT tiếp / PPO.

**Kernel `trangphngngc/sa3-test-ck400`** (T4×2, đẩy 15/11 06:55 VN, trần 11 h, builder `_bundles/sa3_test/make_k.py`, không dataset mới): hoà S1 → hoà SFT-cont (kiểm 3/3) → sft_cont_merged trên 20 bước chạm test phải trùng ≥16/20 câu SFT tiếp đã chấm (60,16) → kiểm bộ chấm 10 bước S1. GPU0: SA ck400 sinh 4.463 bước chạm, dùng lại tệp thô cho câu trùng, UGround chấm, kiểm 40 bước. GPU1: SA ck400 rồi SFT-cont sinh 2.495 bước không chạm, chấm noharm. Kết quả về `runs/sa_spice_v3/test/`. Mốc so exec: SFT tiếp (`runs/luoi/7_11/test_u_3/`), ck500, S1/101.

## 14. Kết quả tập kiểm SA-SPICE-v3 ck400 (kernel `sa3-test-ck400`, xong 15/11 ~16:50 VN)

Số **test**, một seed (101), một điểm lưu chọn trên DEV trước khi chấm test. Tệp ở `runs/sa_spice_v3/test/` (mã đã chạy ở `ma_kernel/`). Bảng đầy đủ, có đánh dấu, ở `report/334` §1–§5.

**Kiểm:** hoà S1 rồi hoà SFT-cont, greedy trùng kernel 1 **3/3** · sft_cont_merged trùng câu SFT tiếp đã chấm **19/20** (ngưỡng 16) · bộ chấm tái lập 10 bước S1 (10/10 hit_voronoi và hit_disk trùng tệp thô cũ) · 4.112 câu trùng tệp thô cũ dùng lại kết quả chấm, 40 bước chừa ra chấm lại trùng tuyệt đối **40/40** · adapter gắn thật: câu SA khác SFT-cont ở 606/2.495 bước không chạm. Log in "13/4463 trùng" là 13/20 câu mẫu SFT tiếp (mẫu số in sai, chỉ 20 khoá được so).

**Bước chạm (4.463):** exec **61,21** [59,45; 62,92] · D.3 67,56 · AitW đầy đủ 77,12 · đúng loại thao tác 95,79. Cao nhất mọi nhánh đã train ở exec, D.3, D.3∧14%.

| phép so exec (ghép cặp, cụm app, B = 1.000 bản thử; bản B = 10.000 ở report/334) | Δ [KTC95] | hơn/kém | p |
|---|---|---|---|
| SA ck400 − SFT tiếp (cùng điểm xuất phát) | **+1,05** [+0,48; +1,66] | 116/69 | 0,0007 |
| SA ck400 − ck500 | +0,56 [−0,04; +1,22] | 100/75 | 0,069 |
| SA ck400 − A/A | +1,48 [+0,86; +2,21] | 130/64 | 2,5e−6 |
| SA ck400 − S1/101 | +2,11 [+1,34; +2,89] | 181/87 | 9,5e−9 |

DEV − test: SA ck400 − SFT-cont +1,35 trên DEV-v3, +1,05 trên test (cùng chiều, nhỏ hơn).

**Bước không chạm (2.495, tỉ lệ đúng loại thao tác %):**

| | toàn bộ | scroll | wait | input_text | open_app | navigate_back |
|---|---|---|---|---|---|---|
| SFT-cont | 84,61 | 76,82 | 95,64 | 80,36 | 97,44 | 71,11 |
| SA-SPICE-v3 ck400 | 84,05 | 80,00 | 94,26 | 80,16 | 98,29 | **58,52** |
| S1/101 | 85,97 | 83,97 | 90,69 | 81,58 | 96,16 | 72,96 |

So S1 (score_run noharm): SA −1,92 [−2,98; −0,89], SFT-cont −1,36 [−2,31; −0,44]; cả hai ĐẠT ngưỡng −3. Tiêu chí khả thi so SFT-cont: toàn bộ −0,56 (≤3) · scroll+back gộp 75,32 → 74,34 (−0,98, ≤5) ⇒ **đạt trên test**; nhưng back tách riêng −12,6 điểm (192 → 158/270), cùng dạng đã thấy trên DEV (84 → 60/104). Phải khai.

**Cách đọc:** so với điểm xuất phát của chính nó (SFT tiếp), SA-SPICE-v3 hơn +1,05 có ý nghĩa; so ck500 thì chưa tách được (+0,56, KTC phủ 0). +2,11 so S1/101 cộng dồn hai bước (SFT tiếp +1,05 rồi GRPO +1,05), chạm đúng MDE 2,11 nhưng là một seed. Chưa có: độ đo văn bản test (cần kernel CPU SPICE), seed thứ hai, hai arm đối chứng SPICE-MATCH / Sparse-SPICE ⇒ chưa được viết "thiết kế thưởng SA tạo ra mức tăng", chỉ được viết "GRPO với thưởng SA-SPICE-v3 từ SFT-cont".

### 14b. Độ đo văn bản tập kiểm SA-SPICE-v3 ck400 (kernel CPU `trangphngngc/chu-sa3-test-15-11-cpu`, xong 15/11)

Tệp `runs/sa_spice_v3/test/chu/chu_sa3_test_15_11.json` + `chu.log`. 4.463 bước chạm, bộ chấm COCO + chrF + BERTScore (rescaled); tự kiểm tái lập 10 nhánh đã lưu. KTC95 bootstrap cụm app, B = 2.000, * = KTC loại 0. Số test, một seed.

| | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| SA ck400 | 51,24 | **38,90** | **69,31** | 429,12 | 45,76 | **64,40** | 67,59 |

| phép so | BLEU-4 | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|
| SA − SFT tiếp | −0,82* | +0,76* | +3,33 | +0,43 | +1,77* | +0,54* |
| SA − ck500 | −1,12* | +0,95* | −0,93 | −0,03 | +1,53* | +0,52* |
| SA − S1/101 | −0,31 | +1,96* | +13,01* | +1,39* | +3,14* | +1,26* |
| SA − A/A | −1,73* | +0,87* | −1,79 | −0,24 | +2,01* | +0,50* |

Đọc: SA ck400 cao nhất mọi nhánh ở METEOR, ROUGE-L, chrF. SPICE ngang ck500 và không tăng có ý nghĩa so SFT tiếp (+0,43) ⇒ phần tăng văn bản đi qua chrF/ROUGE-L. Cần nhánh SPICE thuần từ SFT-cont (SPICE-MATCH) mới được nói gì về vai trò của SPICE trong thưởng composite. Đã thêm vào report/334 §4.

## 15. SPICE-MATCH: train Colab L4 và DEV-v3 (15–16/11)

**Train.** Arm SPICE-MATCH (thưởng clip(0,8·SPICE + 0,1 − d), SPICE thuần, không action/chrF) từ SFT-cont, seed 101, 500 update, cùng 1.000 câu nhắc TRAIN-v3 và cùng `sa3_grpo.py` như SA. Khác SA duy nhất ở máy: **Colab L4, ép fp16** (SA chạy Kaggle T4 fp16) ⇒ phải khai. Máy ảo mất hai lần (gập máy 15/11 ~23:15; bị thu hồi 16/11 ~16:28), chạy tiếp từ ck125 và ck425, cả hai lần kiểm `[tiếp từ]`, `[nạp default] |lora_B| > 0`, bước đầu = điểm lưu + 1. fp16: 3 bước `grad_norm nan` (GradScaler bỏ qua), 1 bước `kl nan` (bước 416, nửa số câu bị cắt ở 96 token); ck500 0 tensor NaN. Thưởng TB theo khối 100 bước 0,456 · 0,483 · 0,458 · 0,509 · 0,461 (phẳng như SA); KL tại ck400 0,020, ck500 0,039. Điểm lưu ck400/ck500 ở `_bundles/sa3_grpo/ck_match/`, đủ ck75–500 trên Drive `thesis/colab_kaggle/sa3-match-c-1/`.

**DEV-v3** (kernel `uyenle0712/sa3-dev-match`, cùng builder `_bundles/sa3_dev/make_k.py`, xong 16/11 ~22:25 VN, `runs/sa_spice_v3/dev/match/`, đọc bằng `harness/sa3_dev_doc.py`). Số dev, cấm trích.

| nhánh | exec (1.338 chạm) | Δ − SFT-cont | không chạm đúng loại (/667) | Δ − SFT-cont | back /104 | scroll /283 | scroll+back | KL |
|---|---|---|---|---|---|---|---|---|
| SFT-cont | 62,93 | — | 560 (83,96) | — | 84 | 227 | 80,36 | — |
| SA ck400 | 64,28 | +1,35* | 544 | −2,40* | 60 | 237 | 76,74 | 0,042 |
| SA ck500 | 64,35 | +1,42* | 523 | −5,55* | 56 | 235 | 75,19 | 0,043 |
| MATCH ck400 | 64,65 | +1,72* [+0,86; +2,61] (29/6) | 535 | −3,75* | 56 | 234 | 74,94 | 0,020 |
| MATCH ck500 | 64,28 | +1,35* | 539 | −3,15* | 65 | 235 | 77,52 | 0,039 |

So cùng điểm lưu: exec SA − MATCH ck400 **−0,37 [−1,15; +0,38]** p=0,46 · ck500 +0,07 p=1,0. Không chạm SA ck400 − MATCH ck400 +1,35 [+0,00; +2,66] (17/8) p=0,11.

**Tiêu chí khả thi §13** (không chạm tụt ≤3, scroll+back tụt ≤5, KL ≤0,10): MATCH ck400 trượt cả hai (−3,75; −5,43); MATCH ck500 trượt không chạm sát ngưỡng (−3,15, tức 21 bước thay vì 20) và qua scroll+back (−2,84). ⇒ Theo đúng thủ tục đã áp cho SA, **không điểm lưu MATCH nào khả thi**.

Đọc (một hạt, số dev):
- Trên exec, thưởng composite **không hơn** SPICE thuần (MATCH ck400 nhỉnh hơn SA ck400, KTC phủ 0). Phần exec tăng so SFT-cont không đến từ action/chrF trong thưởng.
- Thứ composite có thể mua là bớt tác hại ở bước không chạm: ở ck400 SA tụt ít hơn MATCH 1,35 điểm (KTC chạm 0, p=0,11) và là nhánh duy nhất qua tiêu chí khả thi. Bằng chứng yếu, lẫn khác máy (L4 vs T4).
- Back tụt ở mọi nhánh GRPO (84 → 56–65) ⇒ tác hại back không do thành phần nào riêng của SA.

Chưa chấm test MATCH: chờ user chọn (xem §16 nếu có).

## 16. Tập kiểm SPICE-MATCH ck400 (kernel `trangphngngc/sa3-test-match`, xong 17/11 ~02:50 VN)

User chọn chấm test dù MATCH trượt tiêu chí khả thi DEV (§15) — phải khai. Chọn ck400 vì cùng số bước với SA ck400. Builder `_bundles/sa3_test/make_k_match.py` (chép `make_k.py`, chỉ đổi adapter, md5 `e7ab0390…`). Kết quả `runs/sa_spice_v3/test/match/`.

**Kiểm:** hoà greedy 3/3 · sft_cont_merged trùng SFT tiếp 19/20 · bộ chấm 10 bước S1 · câu MATCH khác SFT-cont ở 428/2.495 bước không chạm (adapter gắn thật; SA 606) · SFT-cont không chạm sinh lại trùng **2.495/2.495** câu lượt `sa3-test-ck400` (tất định). Chạy 3,9 h.

**Exec (4.463 bước chạm, bootstrap cụm app, McNemar chính xác):** MATCH ck400 **60,88**.

| phép so | Δ [KTC95] | cứu / phá | p |
|---|---|---|---|
| MATCH − SA ck400 (61,21) | −0,34 [−0,76; +0,07] | 39 / 54 | 0,15 |
| MATCH − SFT tiếp (60,16) | +0,72* [+0,25; +1,20] | 77 / 45 | 0,005 |
| MATCH − ck500 (60,65) | +0,22 [−0,34; +0,81] | 85 / 75 | 0,48 |
| MATCH − S1/101 (59,11) | +1,77* [+1,13; +2,42] | 149 / 70 | <0,001 |

Câu MATCH trùng SA ở 3.448/4.463 bước.

**Không chạm (2.495, đúng loại thao tác, `canon_action` strict_back như noharm):** MATCH 83,57 · SA 84,05 · SFT-cont 84,61. Theo loại MATCH: scroll 78,94 · wait 95,25 · input_text 78,74 · open_app 99,15 · back 56,30.

| phép so | toàn bộ | back (270) | scroll (755) |
|---|---|---|---|
| MATCH − SFT-cont | −1,04* [−1,86; −0,23] p=0,013 | −14,81* (2/42) | +2,12* |
| SA − SFT-cont | −0,56 [−1,46; +0,32] p=0,24 | −12,59* (3/37) | +3,18* |
| SA − MATCH | +0,48 [−0,08; +1,07] p=0,13 | +2,22* [+0,36; +4,40] (7/1) p=0,07 | +1,06 [0,00; +2,19] |

Đọc (một hạt; MATCH chạy L4, SA chạy T4):
- Thứ tự exec trên test đảo so với DEV (DEV MATCH nhỉnh hơn 0,37, test SA nhỉnh hơn 0,34), cả hai lần KTC phủ 0 ⇒ **thưởng composite và SPICE thuần cho exec ngang nhau**. Phần SA hơn SFT tiếp (+1,05*) phần lớn đã có ở SPICE thuần (+0,72*).
- Composite bớt tác hại không chạm một chút và nhất quán trên DEV lẫn test (DEV +1,35, test +0,48, back +2,22 với KTC loại 0 nhưng chỉ 8 bước bất đồng, McNemar p=0,07). Bằng chứng yếu, chưa đủ để viết "thành phần action trong thưởng chữa bước back": back vẫn tụt −12,6 ở SA.
- Back tụt ở cả hai nhánh (−12,6 / −14,8) ⇒ tác hại back đến từ GRPO + SPICE nói chung, không do thành phần riêng của SA. Khớp phán quyết debate 15/11: chữa back ngoài reward.

**Độ đo văn bản test (kernel `trangphngngc/chu-match-17-11-cpu`, 17/11, `harness/chu_match_17_11.py`, `runs/sa_spice_v3/test/match/chu/`).** 4.463 bước chạm, bootstrap cụm app B=2000, tự kiểm 4 nhánh cũ tái lập số đã lưu.

| nhánh | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|---|
| SFT tiếp | 52,07 | 37,75 | 68,55 | 425,79 | 45,33 | 62,64 | 67,05 |
| ck500 | 52,36 | 37,92 | 68,36 | 430,05 | 45,79 | 62,87 | 67,07 |
| SA ck400 | 51,24 | 38,90 | 69,31 | 429,12 | 45,76 | 64,40 | 67,59 |
| **MATCH ck400** | 52,59 | 38,74 | 69,51 | 436,26 | 46,41 | 64,07 | 67,96 |

| phép so | BLEU-4 | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore |
|---|---|---|---|---|---|---|
| MATCH − SA | +1,35* | +0,20 | +7,14* | +0,65* | −0,34 [−0,70; 0,00] | +0,37* |
| MATCH − SFT tiếp | +0,52* | +0,95* | +10,47* | +1,08* | +1,43* | +0,91* |
| MATCH − ck500 | +0,23 | +1,14* | +6,21* | +0,61 [0,00; +1,20] | +1,20* | +0,90* |

Đọc: ở độ đo văn bản, SPICE thuần **hơn** composite ở BLEU-4, CIDEr-D, SPICE, BERTScore (KTC loại 0); composite chỉ nhỉnh ở chrF (thành phần có trong thưởng của SA, KTC chạm 0) và METEOR (không KTC). MATCH cao nhất lưới RL ở ROUGE-L, CIDEr-D, SPICE, BERTScore (ACE vẫn cao hơn ở CIDEr-D/SPICE/BLEU-4). Gộp với exec (≈) và không chạm (SA nhỉnh rất ít): **thành phần action + chrF trong SA-SPICE-v3 không mua được gì rõ ràng trên test**, trừ chrF và một chút ở bước không chạm. Một hạt, khác máy (L4 vs T4).
