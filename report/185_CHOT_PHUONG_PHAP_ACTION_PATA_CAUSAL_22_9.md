# ACTION 185 — C1 PATA-CAUSAL, BẢN RÚT GỌN ĐỂ TRIỂN KHAI

> Chép từ 9 ảnh chụp màn hình máy Mac (checkout `thesis-master-new`), nhận 23/9/2026.
> Ảnh gốc: `report/anh_185_pata_causal_23_9/01…09_*.jpg` (đánh số theo thứ tự đọc).
> Phần *Đối chiếu với kho WSL* ở cuối là của phiên chép, không có trong bản gốc.

**Cập nhật:** 23/09/2026
**Trạng thái:** đã audit lại paper và phương pháp; chưa viết custom decoder, chưa train C1.
**Quyết định vận hành (đã chốt):** C1 trước. C0-Loc chỉ chạy sau khi C1 ra kết quả tốt theo cổng §8.
C1 không tốt → dừng, không chạy C0, không mở test.

## 1. Kết luận phải giữ

Không dùng checkpoint S1 cũ. Tạo lại một prefix sạch từ `Qwen/Qwen2.5-VL-3B-Instruct` trên
`train_tru_val`, theo ba chặng:

```
Base
 └ Stage S: speaker CE-only, 2 epoch
    └ Stage H: localizer KL-only, 1 epoch
       ├ C1: CE+KL, bridge bật, 1 epoch       ← chạy trước
       └ C0-Loc: CE+KL, bridge tắt, 1 epoch   ← chỉ chạy sau khi C1 tốt (§8)
```

`C1 − C0-Loc` chỉ ước lượng **hiệu ứng của việc bật learned bridge trong recipe này**. Không gọi đó là
causal mediation phổ quát và không nói attention là lời giải thích.

C1 chạy một mình chỉ trả lời:
- code/optimization có hoạt động không;
- localizer có tìm target không;
- decoder có sử dụng bridge không;
- có đáng trả chi phí chạy C0-Loc không.

C1 chạy một mình **không chứng minh phương pháp tốt hơn đối chứng**. Nếu chưa có C0-Loc, chỉ được viết
"C1 qua/không qua cổng futility", không được viết "PATA tăng X điểm".

## 2. Dữ liệu: sửa quan trọng

Số hiện có:
- full train: 64.567 bước;
- touch train (`click`/`long_press`): 41.191;
- dựng được proxy target box: 41.099/41.191 = 99,78%;
- 92 bước không dựng được box:
  - 50 bước có node usable nhưng click không nằm trong box nào;
  - 42 bước không lấy được node usable sau load/filter;
- test cũ: 4.463 touch steps.

Target box là **weak/proxy label**: accessibility node usable nhỏ nhất chứa điểm chạm. Nó không phải
bounding box do người gán.

### Luật train đúng

Không loại 92 bước khỏi toàn bộ training:

```
mọi touch Train-proper:
    tính sentence CE

chỉ touch có box hợp lệ:
    tính thêm patch KL

touch không có box:
    KL mask = 0
```

Khi batch có mẫu không box, KL phải lấy trung bình trên **số mẫu eligible**, không chia cho toàn batch.
Nếu batch không có mẫu eligible thì `L_KL = 0`.

### Audit box trước train dài

Audit mù 200–300 mẫu:
- có một phần lấy ngẫu nhiên với xác suất biết trước để ước lượng tỷ lệ lỗi;
- oversample widget nhỏ, container, parent-child, overlay, góc/biên và OCR-only để chẩn đoán;
- hai người gán độc lập trên ít nhất một phần mẫu, sau đó adjudication;
- khi báo tỷ lệ chung phải reweight về quần thể 41.099;
- audit riêng 50 outside-box và 42 no-usable-node.

Phân biệt lỗi nhẹ (box child vẫn nhận diện đúng widget) với lỗi nặng (stale box hoặc box thuộc
distractor). Nếu lỗi nặng/stale vượt ngưỡng 5% đã khóa trước, sửa labeler rồi dựng lại dữ liệu.

## 3. Split và validation

- `train_tru_val.jsonl`: nguồn tạo Train-proper; đã loại nguyên episode của cả hai dev set.
- `val_cham400.jsonl`: 400 touch steps, dùng thường xuyên cho loss/localizer diagnostics.
- `val_cham600.jsonl`: tên lịch sử; thực tế khoảng 602 touch steps, chỉ dùng futility/model selection.
- lát 800 cũ: chỉ regression test/calibration, không quyết định hiệu quả.

Luật:

```
Train-proper: forward + backward + optimizer.step
Val:          model.eval() + torch.no_grad(); tuyệt đối không update
```

Trước train phải assert không trùng `episode_id`, `(episode_id, step_id)`, ảnh và OCR giữa
Train-proper, val400 và val600; lưu SHA-256 từng split.

Hai dev set đã được xem trong nghiên cứu trước, nên chỉ gọi là **development sets**, không phải
confirmatory data.

Test 4.463 cũng đã được dùng để phân tích nhiều phương pháp cũ. PATA chưa học test, nhưng toàn chương
trình nghiên cứu đã thích nghi theo kết quả test. Vì vậy:
- không mở test để quyết định C1/C0;
- tốt nhất tạo holdout/external set chưa từng xem trước kết luận cuối;
- nếu không có holdout mới, kết quả trên test 4.463 phải gọi là **retrospective evaluation**, không gọi
  independent confirmation.

## 4. Kiến trúc C1

### Backbone và input
- `Qwen/Qwen2.5-VL-3B-Instruct`, khóa revision cụ thể;
- QLoRA 4-bit NF4, BF16 compute;
- vision tower frozen;
- input: screenshot + goal + 3 gold-history steps + 24 OCR lines;
- output: một câu tiếng Anh hướng dẫn người dùng chạm target;
- listener không tham gia train, filtering hoặc checkpoint selection.

### TARGET token

```
<|im_start|>assistant
<TARGET>Tap the share icon at the top right.<|im_end|>
```

- `<TARGET>` được template ép trước câu;
- label của token là `-100`, không tính CE;
- do causal mask, TARGET không nhìn gold suffix;
- strip TARGET trước khi chấm câu.

### Localizer và bridge

Qwen2.5-VL-3B có 36 decoder blocks. MVP khóa injection sau block 17:

```
hT = hidden state của TARGET sau block 17
vi = hidden states của visual tokens sau block 17

q  = Pq(LN(hT))
ui = Pv(LN(vi))
αi = softmax(q·ui / sqrt(d))
z  = Σ αi vi

hT' = hT + sigmoid(g) · Wo(z)
```

Thay `hT` bằng `hT'`, rồi chạy blocks 18–35. Sentence tokens phía sau có thể attend TARGET đã được điều
kiện hóa bởi target region.

Khởi tạo đã khóa:
- `Wo` zero-init;
- gate bias −2 (`sigmoid(-2) ≈ 0,119`), không còn lựa chọn "−2 hoặc −3";
- TARGET embedding khởi tạo bằng mean vocabulary embedding;
- `Pq`, `Pv`, `Wo`, gate ở BF16/FP32, không quantize;
- block 17 là **preregistered midpoint heuristic**, không claim là layer tối ưu theo paper.

Injection phải nằm trong decoder loop. Cộng residual sau toàn bộ `forward()` không thể đổi logits hoặc
KV-cache đã tạo.

### Patch target
- đọc grid thật từ processor/`image_grid_thw`;
- biến đổi box theo đúng resize của processor;
- một merged visual cell là positive nếu giao box;
- flatten đúng raster order sau spatial merge;
- chuẩn hóa positive cells thành phân phối tổng bằng 1.

Không suy grid trực tiếp từ kích thước screenshot gốc.

## 5. Loss

Stage J:

```
L = mean(CE_sentence trên mọi touch)
  + 1.0 × mean(KL(p_target || α) trên touch có box)
```

`λpatch=1` là fixed paper-informed default từ GUI-Actor, không phải giá trị tối ưu đã được chứng minh
cho dữ liệu này. Log riêng raw CE, raw KL và weighted total.

CE chỉ là training/diagnostic metric:
- có thể tính offline trên tập có câu gold;
- không tính được khi deploy không có gold;
- paraphrase đúng nghĩa vẫn có thể CE cao;
- không dùng CE làm headline metric.

Primary task metric vẫn là `exec`; action validity, câu rỗng/lặp, length, D.3 và listener thứ hai là
supportive/robustness.

## 6. Recipe huấn luyện đã khóa

### Stage S — speaker sạch
- init: Base Qwen2.5-VL-3B-Instruct;
- data: **mọi touch của Train-proper**, gồm cả 92 mẫu thiếu box;
- objective: sentence CE;
- vision frozen, language QLoRA;
- LoRA rank 8, alpha 16, dropout 0.05; 7 modules:
  `q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj`;
- effective batch 16;
- LR `1e-4`, cosine, warmup ratio `0.05`, weight decay 0;
- 2 epochs, dùng checkpoint cuối.

Sau mỗi epoch: tính `CE_val` trên val400 bằng `eval/no_grad`. CE dùng phát hiện overfit/divergence,
không dùng làm kết quả deploy.

Các hyperparameter Stage S là fixed project choices, không nói là copy từ paper.

### Stage H — localizer warm-up
- init: checkpoint cuối Stage S;
- thêm TARGET, `Pq`, `Pv` và action head;
- freeze vision, language backbone và Stage-S LoRA;
- train TARGET embedding + localizer/projections;
- data: chỉ các Train-proper samples có box;
- objective: KL multi-patch, không sentence CE;
- LR `1e-4`, cosine, warmup ratio `0.03`, weight decay 0;
- 1 epoch, dùng checkpoint cuối.

Sau epoch, trên val400 tính:
- `KL_val`;
- Hit-in-box;
- attention mass trong box;
- lift so với center prior và train-location prior;
- correct prompt so với shuffled goal/history.

Đi tiếp khi cận dưới KTC một phía 90% của lift so với prior > 0 và correct prompt tốt hơn shuffled.
Không đạt thì dừng: bridge không thể cứu một localizer chỉ học prior.

Checkpoint H phải lưu bất biến; đây là initialization chung cho C1 và C0-Loc.

### Stage J — C1 chạy trước
- init: đúng checkpoint H;
- enable language LoRA, TARGET/localizer và bridge;
- vision vẫn frozen;
- data: mọi touch Train-proper; KL mask theo box eligibility;
- loss: CE + 1×KL;
- 1 epoch, effective batch 16;
- LoRA + warmed localizer LR `2e-5`;
- bridge mới (`Wo`, gate) LR `1e-4`;
- cosine, warmup ratio `0.03`, weight decay 0;
- checkpoint cuối; không chọn best checkpoint theo listener.

`2e-5/1e-4` là differential-LR heuristic của dự án, không phải hyperparameter đã được paper chứng minh.
Không đổi sau khi xem val.

## 7. Unit tests và smoke bắt buộc

Trước train dài phải pass:
1. số visual tokens khớp `image_grid_thw` sau merge;
2. box ở bốn góc tạo đúng positive cells;
3. đổi gold suffix nhưng giữ prefix không đổi TARGET query/attention;
4. `Wo=0` cho logits khớp baseline trong sai số BF16;
5. bật residual chỉ làm TARGET/suffix đổi, không làm prefix trước TARGET đổi;
6. backward đầu: `Wo`, localizer và TARGET nhận gradient; gate được phép gradient bằng 0 vì `Wo=0`;
7. sau ít nhất một optimizer step: gate phải nhận gradient;
8. vision gradient bằng 0 và weights không đổi;
9. teacher-forced full pass khớp incremental KV-cache;
10. save→reload giữ logits, attention và câu;
11. box nhỏ/sát biên không tạo NaN;
12. overfit 8–32 samples: CE/KL giảm và mass trong box tăng;
13. strip TARGET đúng định dạng evaluator.

Fail KV-cache hoặc save/reload thì cấm train dài.

Chạy smoke 100 updates để đo runtime, VRAM, gradient norms và residual scale. Log tại step 0/1/10/100:
- gradient norm của `Wo`, gate, `Pq`, `Pv`, TARGET embedding và LoRA;
- `sigmoid(g)`;
- `||Wo(z)|| / ||hT||`;
- raw CE, raw KL;
- số positive cells/box.

## 7b. Kiểm sớm trong lúc chạy

Có thể phát hiện **hỏng sớm**. Không thể chứng minh **C1 hiệu quả** trước khi hết Stage J và chấm val600.
Dự án đã từng thấy loss/attention đẹp nhưng `exec` không tăng.

Khóa một **probe 40** từ `val_cham400` trước train (SHA-256, không đổi). Probe này chỉ để xem kỹ
thuật/format và "bridge có được dùng không". Không dùng `val_cham600` hay test trong lúc train. Không
chọn checkpoint theo probe.

### Tín hiệu rẻ, log mỗi 200 updates ở Stage J

| Tín hiệu | Đọc thế nào | Được phép dừng sớm? |
|---|---|---|
| NaN / loss nhảy vọt | lỗi code/ổn định | Có |
| `CE_train` không giảm sau ~400 updates | speaker không học | Có |
| `KL_train` không giảm sau ~400 updates | localizer chết | Có |
| `sigmoid(g)` kẹt ~0 và `‖Wo(z)‖/‖hT‖` ~0 | bridge không mở | Có, sau mốc 800 nếu vẫn vậy |
| gradient `Wo`/LoRA = 0 | graph đứt | Có |
| câu rỗng/lặp/format hỏng trên probe 40 | generation gãy | Có |

Sau mỗi epoch Stage S: `CE_val` trên val400.
Sau Stage H: `KL_val`, Hit-in-box, mass, prior, shuffle trên val400 — **đây là cổng sớm quan trọng
nhất**. H không qua thì không chạy C1.

### Mốc 800 (~1/3 epoch J, teacher-forced val400 + generate probe 40)

Ngoài các lỗi kỹ thuật:
1. `CE_val` và `KL_val` trên val400 không divergence.
2. Disable bridge trên **cùng** probe 40: ≥ 30% câu phải đổi (không tính strip TARGET). Nếu gần như
   không đổi → decoder bỏ qua bridge → **dừng**, không tốn hết epoch.
3. Shuffle goal/history trên probe 40: Hit-in-box/mass phải giảm so với prompt đúng.
4. Format hợp lệ ≥ 95% trên probe 40.

Nếu 1–4 đạt: chạy hết 1 epoch. **Không** suy `exec` cuối từ probe 40.

### Việc đắt, chỉ làm 1 lần sau hết epoch C1

Generation + `exec` trên val600, disable/swap/random-pool đầy đủ. Đây mới là cổng "C1 tốt thì mới chạy
C0". Không chạy `exec` val600 ở giữa epoch để "xem thử": tốn listener và làm nhiễm tập futility.

## 8. Cổng C1-first

### Mốc update 800

Chỉ được dừng vì lỗi kỹ thuật:
- NaN/divergence;
- CE hoặc KL không học;
- format/câu rỗng/lặp hỏng rõ;
- attention không đổi khi shuffle prompt;
- bridge disable/swap không làm output thay đổi;
- save/load hoặc KV-cache sai.

Không được đổi λ, layer, LR hoặc gate init sau khi xem mốc 800. Nếu không có lỗi thảm họa, chạy hết
một epoch.

### Cổng cuối C1 trên val600

C1 đủ điều kiện chạy C0-Loc khi cùng lúc:
1. câu hợp lệ ≥ 99%, không phình độ dài hoặc lặp bất thường;
2. `CE_val`/`KL_val` không divergence và localizer vẫn vượt prior/shuffle;
3. `exec(C1)` không thấp hơn Stage-S speaker theo point estimate;
4. chạy C1 bình thường có `exec` cao hơn chính checkpoint đó khi disable bridge theo point estimate;
5. swap sang matched distractor làm câu đổi về phía distractor nhiều hơn random-pool control, với cận
   dưới KTC một phía 90% của chênh lệch > 0.

Đây là cổng **"C1 tốt mới chạy C0"**, không phải efficacy test:
- đạt hết 5 điều trên → mới chạy C0-Loc từ **đúng checkpoint H đã seal**, không train lại S/H;
- không đạt → dừng, không chạy C0, không mở test;
- khi dừng chỉ kết luận "futility under budget", không kết luận bridge vô ích.

## 9. C0-Loc nếu C1 qua gate

C0-Loc phải:
- load đúng checkpoint H đã niêm phong;
- có cùng data, eligibility mask, seed, sampler order, optimizer steps, CE+KL, LR và decoding;
- khác C1 ở `bridge_enabled=false` và output directory.

Primary dev contrast:

```
Δexec = exec(C1) − exec(C0-Loc)
```

Phân tích ghép cặp theo cùng sample, cluster bootstrap theo episode; báo bảng discordance. Val600 chỉ
dùng gate, không báo như kết quả xác nhận.

Không gọi ablation `λpatch=0` sau checkpoint H là "không spatial supervision", vì H đã học box. Muốn
kiểm spatial supervision thật sự cần một nhánh không đi qua H hoặc factorial design riêng; không làm
trong MVP.

Nếu có ngân sách cho claim ổn định, chạy lại **cả cặp C1/C0-Loc** với seed khác. Một seed chỉ hỗ trợ
claim artifact-level.

## 10. Mức khớp với paper

### Hỗ trợ trực tiếp nhất — GUI-Actor, NeurIPS 2025

GUI-Actor hỗ trợ:
- special action token/context anchor;
- attention lên visual patches;
- mọi patches giao box là positives;
- `KL(target || attention)`;
- joint next-token prediction + action-attention với weight 1:1;
- head-only warm-up 1 epoch, LR `1e-4`, cosine, warmup `0.03`, backbone frozen;
- sau warm-up là joint/full training.

Stage H và dạng `CE+KL` bám paper/repo này. GUI-Actor không đưa pooled target feature ngược lại để điều
kiện hóa câu; bridge C1 vẫn là giả thuyết của luận văn.

### Hỗ trợ từng phần
- **LISA, CVPR 2024 Oral:** frozen vision + LLM LoRA; special token điều khiển spatial decoder; joint
  text/spatial loss. LISA dùng CE + BCE/DICE, không dùng KL.
- **PixelLLM, CVPR 2024:** caption-first rồi joint caption/localization. PixelLLM dùng caption CE + L1
  coordinates; SAM branch frozen nhưng EVA02 branch được tune, nên không nói họ freeze toàn bộ vision.
- **LocCa, NeurIPS 2024:** location-aware training và component ablation; không dùng patch-KL head.
- **Attention is not Explanation, NAACL 2019:** lý do phải có disable/swap/random-pool, không chỉ trình
  bày attention heatmap.

### Phần của luận văn, không được nói là paper-proven
- toàn pipeline S→H→J;
- Stage S 2 epoch và cấu hình LoRA cụ thể;
- injection ở block 17;
- `Wo` zero-init, gate −2 và mean-vocabulary TARGET init;
- differential LR Stage J;
- C0-Loc/C1 paired bridge design.

Claim an toàn:

> We evaluate a GUI-specific grounding-to-generation bridge in which a dedicated target token is
> spatially supervised with multi-patch KL, enriched by a pooled target-region residual inside the
> decoder, and made available to subsequent referring-instruction tokens.

Không claim "first latent visual feedback", "attention proves reasoning" hoặc "causal effect of correct
localization".

Nguồn:
1. GUI-Actor, NeurIPS 2025:
   https://proceedings.neurips.cc/paper_files/paper/2025/file/16130af940e9dabb43c726119bd3b42e-Paper-Conference.pdf
2. GUI-Actor official repo: https://github.com/microsoft/GUI-Actor
3. LISA, CVPR 2024:
   https://openaccess.thecvf.com/content/CVPR2024/html/Lai_LISA_Reasoning_Segmentation_via_Large_Language_Model_CVPR_2024_paper.html
4. PixelLLM, CVPR 2024:
   https://openaccess.thecvf.com/content/CVPR2024/html/Xu_Pixel-Aligned_Language_Model_CVPR_2024_paper.html
5. LocCa, NeurIPS 2024:
   https://papers.nips.cc/paper_files/paper/2024/hash/d303b4f1ef8d8274ae6b152df70f5406-Abstract-Conference.html
6. Attention is not Explanation, NAACL 2019: https://aclanthology.org/N19-1357/

(URL chép từ ảnh; chuỗi hash có thể lệch một ký tự do ảnh mờ — mở lại trước khi trích.)

## 11. Manifest phải seal trước C1

Ghi `runs/pata/manifest_seal.json` trước khi train Stage J:
- base model revision;
- SHA-256 Train-proper/val400/val600;
- data-order, dropout và new-module-init seeds;
- box eligibility rule và KL normalization;
- block 17, shapes `Pq/Pv/Wo`, `Wo=0`, gate bias −2;
- LoRA config;
- S/H/J schedules;
- SHA-256 checkpoint S và H;
- decoding, stop tokens và max tokens;
- các failure/futility gates ở trên.

C1 và C0-Loc config chỉ được khác:

```yaml
bridge_enabled: true|false
output_dir: ...
```

Nếu sửa architecture, loss, LR, eligibility hoặc checkpoint H sau khi chạy C1 thì phải chạy lại cả
Stage-J C1 và C0-Loc; không được dùng C0 mới so với C1 cũ.

## 12. Action theo đúng thứ tự

**A. Chưa tốn lượt train dài**
1. Audit box và 92 ca thiếu box.
2. Dựng Train-proper từ `train_tru_val`; CE giữ mọi touch, KL có eligibility mask.
3. Assert split và lưu hash.
4. Viết custom decoder, patch collator và 13 unit tests.
5. Overfit 8–32 samples; chạy smoke 100 updates.
6. Seal manifest.

**B. Prefix chung**
7. Train Stage S 2 epochs; tính `CE_val` sau mỗi epoch.
8. Train Stage H 1 epoch; chấm KL/Hit/mass/prior/shuffle trên val400.
9. H không qua gate → dừng.

**C. Tạm thời chỉ chạy C1**
10. Khóa probe 40 từ val400; C1 load H, joint CE+KL.
11. Log mỗi 200 updates (§7b). Mốc 800: val400 teacher-forced + generate/disable-bridge trên probe 40.
    Bridge không được dùng → dừng.
12. Hết epoch mới chấm `exec` trên val600 và swap/random-pool đầy đủ.
13. Không qua cổng §8 → dừng, không C0, không mở test.

**D. Chỉ khi C1 tốt theo §8 — lúc đó mới chạy C0**
14. Chạy C0-Loc từ đúng H đã seal; không train lại S/H.
15. So ghép cặp C1−C0-Loc trên val600.
16. Quyết seed tiếp theo và holdout/external evaluation trước khi đọc kết quả cuối.

## 13. Việc chưa làm và cần người dùng/GVHD quyết

Chưa làm:
- chưa sửa code trong clone;
- chưa audit box;
- chưa seal manifest;
- chưa train S/H/C1/C0-Loc;
- chưa có holdout mới cho kết luận xác nhận.

Cần quyết trước kết luận cuối, nhưng **không chặn engineering run C1**:
1. Có tạo holdout/external set chưa từng xem hay chấp nhận báo test cũ là retrospective.
2. Có ngân sách chạy C0-Loc và seed thứ hai nếu C1 qua gate.
3. Có giữ tên "PATA-Causal" hay đổi sang tên hẹp hơn; nếu giữ, phải giải thích "causal" chỉ là hướng
   thông tin và model-internal intervention.

Hai điều không được bỏ:
- không mở test chỉ để "xem thử" sau C1;
- không bỏ C0-Loc nếu muốn claim bridge có hiệu quả.

## 14. Gửi chat implement + ước giờ

File này **đủ làm spec phương pháp**. Chat implement còn cần **clone repo** (trainer S1,
`harness/train_config.yaml`, `train_tru_val.jsonl`, val400/600, collator, `exec`/UGround). Không gửi 185
một mình.

LoRA 7 modules: `q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj`.

Ước A100, Train-proper ~40k touch, batch 16 → ~2.500 updates/epoch. SFT cũ đo **10,3 s/update**. Custom
decoder/KL có thể chậm hơn; dùng 10,3 s cho sàn, 15 s cho trần.

| Chặng | Updates | A100 sàn (10,3 s) | A100 trần (15 s) |
|---|---|---|---|
| Code + unit test + smoke 100 | — | 0 h GPU; 1–3 ngày người | smoke ~0,3–0,4 h |
| Stage S, 2 epoch | ~5.000 | 14 h | 21 h |
| Stage H, 1 epoch | ~2.500 | 7 h | 10 h |
| C1 Stage J, 1 epoch | ~2.500 | 7 h | 10 h |
| Chấm val600 `exec` + disable/swap | — | 1–3 h | 3–5 h |
| **Tổng tới cổng C1** | ~10.000 train | **~29–35 h** | **~42–46 h** |
| C0-Loc, chỉ nếu C1 tốt | ~2.500 | +7 h | +10 h |
| Mốc 800 C1 (có thể dừng) | 800 trong J | ~2,3 h thêm sau S+H | ~3,3 h |

S + H đã xong trước khi biết C1 có đáng. Nếu H fail: dừng sau ~21–31 h, chưa C1. Nếu C1 fail ở mốc
800: đã tốn S+H + ~3 h J.

Không dùng 21 s/update của ORPO. Smoke 100 updates phải thay số thật trước khi tin cột trần.

---

## Đối chiếu với kho WSL (phiên chép, 23/9) — [đo]

- `harness/dg1_cache/train_ac/train_tru_val.jsonl` có, **63.000** bước; trong đó **40.189** bước chạm
  (`click`/`long_press`) ⇒ ~2.512 update/epoch ở batch 16, khớp ước ~2.500 của §14.
- `descriptors.jsonl` có trường `box` ở đủ **41.099/41.099** dòng; giao với Train-proper được
  **40.098** bước có box ⇒ **91** bước chạm trong Train-proper thiếu box (bản gốc nói 92 trên toàn
  64.567; một ca rơi vào val).
- `val_cham400.jsonl` 607 dòng (400 chạm) · `val_cham600.jsonl` 960 dòng (602 chạm) — có sẵn.
- `runs/pata/` chưa tồn tại; chưa có dòng mã nào của custom decoder.

## Quyết định + thi hành 23/9 (phiên WSL)

**User quyết 23/9: Stage S chạy 1 epoch, không phải 2** (lượt thử để xem C1 có đáng làm tiếp).
Hệ quả phải khai: điều kiện 3 của cổng §8 vẫn so đúng vì so C1 với **chính** checkpoint S của
lượt này; nhưng số của S/C1 **không** so thẳng được với S1 cũ (2 epoch, trên cả tập val).
Ước giờ A100 tới cổng C1 hạ còn khoảng S ~7 h + H ≤ 7 h (forward cắt sau block 17, thực tế
ít hơn) + J ~7 h + chấm 1–3 h ⇒ **~20–24 h sàn**, chờ số đo smoke thay vào.

Chặng A (0 GPU) đã làm trên WSL:

| bước §12 | trạng thái | tệp |
|---|---|---|
| A1 audit box | **mẫu + trang gán nhãn đã dựng, chờ người gán** (264 mẫu: U 150 + 5 tầng × 20 + 14 không box; 60 mẫu chồng cho người thứ hai) | `harness/pata_audit.py` → `dg1_cache/train_ac/pata/audit/audit.html` |
| A2 Train-proper | xong: 40.189 chạm, 40.089 có box; 100 thiếu box (91 không có descriptor + 9 điểm chạm vượt khung ảnh khai báo ⇒ KL tắt, CE giữ); 107 box cắt vào biên màn | `harness/pata_data.py` → `dg1_cache/train_ac/pata/*.jsonl` |
| A3 split + hash | xong: rời nhau theo episode · (episode,step) · ảnh/OCR; SHA-256 ở `pata/split_hash.json`; probe40 khoá hash `6c23c1898d85…` | như trên |
| A4 decoder + collator + 13 test | xong, **13/13 ĐẠT trên mô hình tí hon (CPU)**; chờ chạy `--real` trên Kaggle | `harness/pata_model.py` · `pata_test.py` |
| A5 overfit + smoke | overfit tí hon đạt (KL 2,41 → 0,11, mass 0,12 → 0,97); smoke thật chờ Kaggle | `harness/kaggle_pata_test.md` |
| A6 seal manifest | chưa — cần SHA của checkpoint S, H | — |
| trainer S/H/J | xong, chạy thử cả ba chặng + nối tiếp trên CPU | `harness/pata_train.py` |
| đánh giá | `diag` (cổng H, mốc 800) + `gen` bật/tắt bridge; **swap/random-pool (§8 điều 5) chưa viết** — cần hộp distractor, làm trước bước 12 | `harness/pata_eval.py` |

Lựa chọn của phiên thi hành (spec không nói, phải vào manifest): d_k = 2048 · gate là MỘT vô
hướng · "action head" = LN + Pq + Pv · clip grad 1,0 · NF4 double-quant · CE chuẩn hoá theo
token trên cả lô hiệu dụng (khớp LLaMA-Factory của S1) · center prior = Gauss σ = 0,25 bề
rộng/cao · train-location prior = histogram phủ box 32×32 trên Train-proper · xáo prompt = hoán vị
cố định (hạt 20260923), mỗi bước nhận goal/history của episode khác.

### A1 — kết quả audit box (23/9, một người gán: Uyên, 264/264 mẫu) — [đo]

`harness/pata_audit.py doc` · nhãn `dg1_cache/train_ac/pata/audit/audit_Uyên.json`

| tầng | n | lỗi nặng | ghi chú |
|---|---|---|---|
| **U (ngẫu nhiên, ước lượng quần thể)** | 148 (bỏ 2 "không rõ") | **4 = 2,7%** · Wilson95 [1,1; 6,7] | cả 4 là box thuộc phần tử khác |
| S1 widget nhỏ | 20 | 1 = 5% | |
| **S2 container** (area ≥ p95 = 0,089) | 20 | **7 = 35%** | 4 phần tử khác + 3 stale |
| S3 sát biên | 20 | 2 = 10% | cả 2 stale, box phủ 79–87% màn |
| S4 tên từ OCR | 20 | 2 = 10% | |
| S5 không tên | 20 | 2 = 10% | cả 2 stale, box phủ 55–92% màn |
| N không box | 14 | — | **14/14 có phần tử rõ tại điểm chạm** ⇒ thiếu box là do labeler bỏ sót, không phải màn trống |

⇒ Theo luật khoá trước (§2, ngưỡng 5% trên ước lượng quần thể): **2,7% < 5% ⇒ giữ box, đi tiếp.**
⚠️ Cận trên Wilson 6,7% vượt 5% — khai khi viết.
⚠️ Chỉ **một** người gán ⇒ chưa có κ và adjudication như §2 đòi.
⭐ Lỗi nặng dồn vào box rất lớn: box có area ≥ 0,25 lỗi nặng **10/18** (mọi lỗi stale đều ở đây);
phần còn lại 8/230; tầng U còn lại 3/145 = 2,1%. Box ≥ 0,25 chiếm 883/40.089 = **2,20%** Train-proper.
Tắt KL cho nhóm này là một lựa chọn rẻ trước khi train — **chờ user quyết**, vì luật khoá trước
không bắt buộc (điểm ước lượng dưới ngưỡng).
