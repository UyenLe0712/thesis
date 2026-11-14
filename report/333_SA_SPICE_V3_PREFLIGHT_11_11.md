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
