# 226 — Brief để chat kia đọc và làm: ECGR (27/9/2026)

## 0. Việc bạn làm

1. Đọc hết file này trước khi đề xuất hướng khác.
2. Phương pháp đã chốt cho luận văn là **ECGR**: kiến trúc hai lượt kiểu MM-SeR, cộng một module
   mới là **Element-Consistency Gate (ECG)**.
3. Việc làm ngay, 0 GPU: chạy G0 rồi G1 trên file điểm có sẵn. Trượt một cổng thì dừng, báo người
   dùng, không đổi sang pointer, crop, retrieval hay fine-tune.
4. Nếu cả hai cổng đạt, viết một file thiết kế cài đặt ECGR ngoài clone. Chưa train.

## 1. Bài toán

Bài trong clone: `paper/soict2026/main.tex`. Hệ thống tên GUIStep.

Từ screenshot, goal, tối đa 3 câu lịch sử và tối đa 24 chuỗi OCR, model sinh một câu tiếng Anh bảo
người dùng chạm phần tử nào tiếp theo.

- Backbone: Qwen2.5-VL-3B-Instruct, QLoRA rank 8, alpha 16, dropout 0,05. Vision tower và
  projector đóng băng.
- Dữ liệu: AndroidControl. 64.567 bước train. Đánh giá 4.463 bước chạm, một câu tham chiếu mỗi
  bước.
- Ba cấu hình đã có trong bài là **cách train**, không phải module mới:
  - GUIStep-S, gọi là **S1**: học thẳng câu. Đây là mốc metric.
  - GUIStep-D: khai báo phần tử rồi viết câu.
  - GUIStep-P: ORPO trên khai báo. Executability 66,5 so với S 65,5, chênh +1,05, p=0,078, không
    đáng kể. Không claim P thắng S.

S1 là mốc cần vượt, không phải checkpoint bắt buộc. ECGR được train lại từ Qwen2.5-VL-3B gốc.

## 2. Ràng buộc

| Ràng buộc | Cách hiểu |
| --- | --- |
| Đóng góp mô hình | Thêm một thành phần vào forward graph. Fine-tune thuần, đổi loss, DPO/ORPO/GRPO, đổi decoding không tính |
| Một model lúc chấm | Không gắn UI-TARS hay UGround lúc suy luận |
| Metric câu hơn S1 | Executability chỉ là cột phụ |

Đóng góp luận văn khi viết bài gồm ba phần, không phình kiến trúc thêm:

1. **Model:** ECG trong ECGR.
2. **Dữ liệu:** pipeline đã có, dựng câu và khai báo từ AndroidControl cùng accessibility tree,
   không thu nhãn mới.
3. **Thước:** executability đã có trong `main.tex`. Listener đóng băng đọc câu, kiểm tra loại thao
   tác, cực tính và điểm có rơi vào hộp phần tử.

Đừng biến (2) và (3) thành việc làm lại. Chúng đã nằm trong bài.

## 3. Mốc S1

Nguồn: `runs/text_metrics_coco.json` và `runs/text_metrics_them.json`. 4.463 bước, greedy, một câu
tham chiếu. METEOR trong file coco là `meteor15`.

| Model | BLEU-4 | METEOR | ROUGE-L | CIDEr-D | SPICE | chrF | BERTScore rescale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1/101 | 51,56 | 36,79 | 67,35 | 416,12 | 44,37 | 61,26 | 66,33 |
| S1/202 | 51,66 | 37,17 | 67,71 | 419,19 | 44,23 | 61,92 | 66,75 |
| S2/101 | 48,68 | 35,75 | 65,97 | 387,68 | 41,28 | 59,94 | 65,07 |
| CE2-S2/101 | 50,12 | 37,31 | 68,62 | 402,24 | 42,27 | 61,85 | 66,83 |
| MIN-DESC/101 | 49,92 | 37,26 | 68,47 | 401,01 | 42,24 | 61,79 | 66,73 |

S2, CE2 và MIN-DESC xuất phát từ model có khai báo, không phải continued-SFT của S1. Continued-SFT
từ S1 chưa chạy.

Seed 202 đã hơn seed 101 mà không có phương pháp mới. Mốc tính là tăng thật:

| Điều kiện | Ngưỡng |
| --- | --- |
| BLEU-4 | ≥ 52,1 |
| CIDEr-D | ≥ 421 |
| Số cột trong 7 metric tăng so với S1/101 | ≥ 4 |
| SPICE | ≥ 44,1 |
| BERTScore | ≥ 66,0 |

So với MM-SeR không có ECG, cùng backbone và cùng ngân sách, phải hơn trên **cả** BLEU-4 và
CIDEr-D.

CIDEr COCO khoảng 120–145 không cùng thang với CIDEr-D 416. COCO thường có 5 câu tham chiếu. Không
cộng delta COCO vào 416.

## 4. MM-SeR là gì

Song, Jo, Min, Xie, Kim, Bisk, Choo. *MM-SeR: Multimodal Self-Refinement for Lightweight Image
Captioning*. CVPR 2026, poster, không phải oral.

- PDF: `https://openaccess.thecvf.com/content/CVPR2026/papers/Song_MM-SeR_Multimodal_Self-Refinement_for_Lightweight_Image_Captioning_CVPR_2026_paper.pdf`
- arXiv: `https://arxiv.org/abs/2508.21451`
- Trang: `https://june-page.github.io/mmser/`

Cách họ sửa câu, trên ảnh thường:

1. Lượt 1 sinh câu nháp.
2. **SeR-Connector**, vài khối Transformer, nhận embedding câu nháp và đặc trưng ViT nhiều tầng.
   Các tầng được nối theo chiều channel.
3. Lượt 2, cùng language model, viết lại cả câu. Không sửa từng token kiểu KEEP/REPLACE.
4. Lúc train họ không dùng câu nháp của chính model, vì câu đó thường lệch quá xa câu đúng, model
   sẽ bỏ nháp và viết lại từ đầu. Họ nhờ GPT-4o-mini đổi nhẹ tên vật, thuộc tính hoặc quan hệ của
   câu đúng, rồi bắt model sửa về câu đúng.

Số của họ, OPT-125M, COCO, một lượt tinh chỉnh: BLEU-4 39,4 → 39,9, CIDEr 129,6 → 133,5. Chỉ đưa
ảnh nhiều tầng: CIDEr 132,3. Sửa lần 2 và lần 3 không lợi với OPT-125M. Connector thêm khoảng 50M
tham số và một lượt suy luận.

Họ đã thử loại connector, có hay không câu nháp, có hay không ảnh nhiều tầng, và chọn tầng ViT nào.
Trong bài họ ghi việc chưa làm: tự chỉnh số lượt tinh chỉnh. Đừng nhận ý "có refine hay không" nói
chung là của mình. Phần của mình hẹp hơn, mục 5.

Code công bố chưa gồm đủ phần refinement. Phải tự cài connector. README trên GitHub nói bản phát
hành tập trung vào captioner gốc.

## 5. Phần của luận văn: ECG trong ECGR

ECGR (Element-Consistent GUI Refinement) là hệ hoàn chỉnh cho câu hướng dẫn GUI.

- Nền hai lượt và SeR-Connector: của MM-SeR, phải trích.
- ECG: module mới. Một cổng trước lượt sửa.

Ảnh màn hình khác ảnh COCO. Câu S1 thường đúng kiểu câu nhưng gọi nhầm nút. MM-SeR luôn viết lại.
Viết lại một câu đã gọi đúng nút dễ làm hỏng câu đó. ECG chặn việc này.

### Forward

```
screenshot + goal + history + OCR
      │
      ▼
Qwen2.5-VL-3B, lượt 1 ──────────────► câu nháp d

q: phần tử model định chạm      p: phần tử câu nháp đang gọi
              │                          │
              └────────────┬─────────────┘
                            ▼
                   ECG: cổng g ∈ [0,1]

g nhỏ: giữ d, không chạy lượt 2
g lớn: H' = H + g · C(H, V)  rồi lượt 2 viết câu cuối
```

$$g = \sigma\Big(\mathrm{MLP}\big[q;\, p;\, |q-p|;\, \mathrm{JS}(q,p)\big]\Big)$$

- $q$: phân phối trên patch ảnh, phần tử định chạm, đọc từ goal, history và ảnh.
- $p$: phân phối trên patch, phần tử mà câu nháp đang mô tả.
- $C$: SeR-Connector. $V$: đặc trưng ảnh nhiều tầng.
- $g$ nhỏ khi $q$ và $p$ trùng. $g$ lớn khi lệch.
- Lúc test chỉ còn một Qwen2.5-VL-3B cùng các head nhỏ. Không box vàng, không câu vàng, không
  model thứ hai.

### Loss, chỉ lúc train

$$\mathcal{L} = \mathcal{L}_{\mathrm{CE}}(\text{câu cuối}) + \lambda_q\,\mathrm{KL}(b,q)
+ \lambda_p\,\mathrm{KL}\big(b, p(y^\star)\big)
+ \lambda_{\mathrm{keep}}\,\mathbb{1}[d = y^\star]\cdot \mathrm{KL}(P_2, P_1)$$

- $b$: patch của hộp phần tử được chạm. Hộp là nút accessibility nhỏ nhất chứa điểm chạm.
- $p$: học trên câu người ($y^\star$), lúc chạy áp lên câu nháp.
- Số hạng cuối phạt lượt 2 khi nó sửa một câu nháp đã đúng.
- $g$ không có nhãn riêng. Nó học qua loss câu cuối.

Nhãn lấy tự động từ AndroidControl. Không thu nhãn mới.

### Ablation, cùng backbone, seed, số update, số tham số

| Nhánh | Câu nó trả lời |
| --- | --- |
| Lịch S1 từ backbone, hoặc số S1 có sẵn | Mốc |
| MM-SeR, luôn chạy lượt 2, không ECG | Nền đã công bố có tự hơn S1 không |
| MM-SeR + cổng ngẫu nhiên hoặc MLP cùng số tham số | Có phải chỉ thêm tham số |
| MM-SeR + ECG chỉ có $q$, bỏ $p$ | Phép so hai phần tử có cần không |
| ECGR = MM-SeR + ECG đủ $q$ và $p$ | Phương pháp |

Claim ECG chỉ đứng khi ECGR hơn MM-SeR không cổng **và** hơn cổng ngẫu nhiên trên cả BLEU-4 và
CIDEr-D, đồng thời đạt mốc mục 3. Nếu ECGR chỉ hơn S1 mà bằng MM-SeR, phần tăng thuộc MM-SeR.

### Câu được phép viết

> Chúng tôi dùng cơ chế tinh chỉnh hai lượt của MM-SeR và đề xuất Element-Consistency Gate, một
> cổng quyết định có viết lại câu nháp hay không dựa trên độ khớp giữa phần tử dự định chạm và
> phần tử câu nháp đang gọi.

Không viết "kiến trúc hoàn toàn mới", "lần đầu tinh chỉnh câu", hay "lần đầu tự quyết định có
refine". Không lấy +0,5 BLEU và +3,9 CIDEr trên COCO làm dự báo.

## 6. Không đề xuất lại

| Hướng | Lý do |
| --- | --- |
| Fine-tune thuần, nhân trọng số câu gần đúng | Không phải thành phần kiến trúc |
| MA-DMT, DMO, ORPO, GRPO trên metric | Objective. DMO trên GIT-large đã mạnh còn giảm: CIDEr 140,9→140,6, BLEU-4 42,5→42,0 |
| Hai model lúc chấm | Không phải một model |
| Target attention, crop, ảnh thứ hai, OCR pointer | Prior art, và probe nội bộ không thấy câu đổi theo vùng. Gold trừ distractor cùng vai trò khoảng +0,0045 nat/token, dưới ngưỡng +0,02. Crop độ phân giải cao trừ thấp khoảng −0,0007 |
| Retrieval / prototype memory | Đã có. App trùng train và test nên dễ copy câu |
| MoE action/target/relation | TFSGC, RS-MoE, DTNet đã có |
| Sửa từng token KEEP/REPLACE | Show-Edit-Tell, Tiger, DECap, LaserTagger, Felix đã có |
| Non-autoregressive | NARVL thua teacher autoregressive |
| MBR | Đã đo +0,09 BLEU-4 và +1,69 ROUGE-L |
| Chỉ đổi tầng ViT, loại connector, hoặc thêm OCR vào connector | MM-SeR đã ablation connector và tầng. Thêm OCR là nối input |
| Đổi nhãn "cat/dog" thành "button/icon" rồi gọi là kiến trúc | Đó là dữ liệu train, không phải forward graph |

## 7. Số nội bộ

Đo trên `runs/score_s1_seed101_raw.jsonl`, 4.463 dòng. Câu model: `sent`. Câu tham chiếu:
`gold_instruction`.

| Phép đo | Kết quả |
| --- | --- |
| Trùng câu tham chiếu, không phân biệt hoa thường | 954 / 4.463 = 21,38% |
| Gần đúng, Jaccard token ≥ 0,6, chưa trùng | 1.274 |
| Khác đúng một block, ≥ 3 token giữ, ≤ 1 token mới | 958 |
| Proxy BLEU-4 / ROUGE-L / CIDEr của S1 | 51,77 / 67,29 / 419,41 |
| Oracle thay 958 câu đó bằng câu vàng | proxy BLEU-4 56,88; ROUGE-L 71,65; CIDEr proxy 527,71 |
| PATA localizer trúng hộp | 52,0% (prior 5,3%) |
| Bật/tắt bridge đổi câu | 15% |
| Exec bật trừ tắt | +0,17, trong nhiều |
| D.3 bật trừ tắt | 0,00 |
| OCR token câu tham chiếu còn thiếu trong S1 | 12,23% bước |
| Cả cụm OCR còn thiếu | 10,66% bước |
| MBR | +0,09 BLEU-4; +1,69 ROUGE-L |

Proxy sát official nhưng không thay bộ chấm COCO. Oracle 56,88 dùng câu vàng để biết câu nào được
sửa. Nó **không** chứng minh ECG tìm được những câu đó.

Khoảng 101 trong 958 câu một-block, nếu sửa đúng, đủ mua +0,54 BLEU-4 theo nội suy tuyến tính. Đó
là trần, không phải kết quả train.

## 8. Cổng và action cụ thể

File: `runs/score_s1_seed101_raw.jsonl`.

`pred_xy` là điểm UGround đọc câu model. `hit_disk = 1` khi điểm đó nằm trong vùng chấp nhận quanh
điểm chạm. Đây là proxy "câu có đang chỉ đúng phần tử", có sẵn, không cần GPU.

Định nghĩa 958 câu một-block:

- token = `\w+`, chữ thường;
- `difflib.SequenceMatcher` giữa câu model và câu vàng;
- đúng một opcode không phải `equal`;
- số token mới phía câu vàng ≤ 1;
- số token `equal` ≥ 3;
- hai chuỗi lower không trùng.

| Cổng | Việc | Đạt | Trượt thì dừng ECG |
| --- | --- | --- | --- |
| G0 — chạy ngay, 0 GPU | Trong 958 câu một-block, đếm `hit_disk` = 0 bằng script Phụ lục A | ≥ 250 | Ít hơn 250: lỗi chủ yếu là cách nói, cổng phần tử không có việc |
| G1 — chưa đủ đầu vào | Sau khi có checkpoint/pilot, lưu $q$ và $p$ cho holdout. Dùng score độc lập với nhãn, ví dụ $\mathrm{JS}(q\|p)$, để phân loại `hit_disk`=0/1 | AUROC ≥0,80; precision ≥0,80 tại recall ≥0,40; giữ ≥97% câu exact | Không đạt thì dừng ECG |

Đối chiếu trước khi tin script: `exact` phải ra 954, `one_block` phải ra 958. Số `hit_disk`=0 trong
958 câu chưa đo. Đó là số bạn phải in.

### Action sau G0

1. Chạy script Phụ lục A.
2. Nếu `one_block_hit_disk_0` < 250: ghi NO-GO ECG, dừng.
3. Nếu đạt: chia tiếp 958 câu theo loại opcode `replace/delete/insert`, `action_ok`, `app`; in 10
   ví dụ `hit_disk`=0 và 10 ví dụ `hit_disk`=1.
4. Ghi rõ: G0 đạt không có nghĩa G1 đạt. `hit_disk` là nhãn đánh giá, không phải feature cho gate.
5. Không thể chạy G1 chỉ bằng file score. Muốn chạy G1 phải có checkpoint hoặc pilot xuất:
   - $q$: vector xác suất trên cùng lưới patch từ goal/history + ảnh;
   - $p$: vector xác suất trên cùng lưới patch từ câu nháp + ảnh;
   - `episode_id`, `step_id`, `sent`, `hit_disk`;
   - không đưa `gold_xy`, gold box hay `gold_instruction` vào feature.
6. Sau khi có vector, khóa score trước khi nhìn nhãn: $\mathrm{JS}(q\|p)$. Báo AUROC, AUPRC,
   precision/recall và false-trigger trên 954 câu exact.

G0 và G1 không chứng minh ECGR thắng. G0 chỉ đo lỗi đúng loại có đủ dày không; G1 mới đo tín hiệu
mà gate thật sự dùng có phát hiện được lỗi đó hay không.

G2 trở đi chưa làm: cài MM-SeR, so ECG với MM-SeR và cổng ngẫu nhiên trên holdout, rồi mới test
một lần. Clone không có adapter S1 và không có tập train. Checkpoint từng ghi ở
`MyDrive/thesis/ckpt/s1_seed101`. Không có dữ liệu train thì không train được. Train lại S1 khoảng
23 giờ A100, ngoài việc này.

## 9. File clone được đọc

| Việc | Đường dẫn |
| --- | --- |
| Bài | `paper/soict2026/main.tex` |
| Điểm S1/101 | `runs/score_s1_seed101_raw.jsonl` |
| Điểm S1/202 | `runs/score_s1_seed202_raw.jsonl` |
| Prediction | `runs/preds_s1_seed101.jsonl` |
| Bảng COCO | `runs/text_metrics_coco.json` |
| chrF, BERTScore | `runs/text_metrics_them.json` |
| Bộ chấm | `harness/text_metrics_coco.py`, `harness/text_metrics_them.py` |

## 10. Không được tự làm

2. Không đề xuất lại mục 6.
3. Không sửa `paper/soict2026/main.tex`.
4. Không train ECG khi G0 chưa đạt hoặc G1 chưa có/không đạt. Pilot chỉ xuất $(q,p)$ là bước đo,
   không được gọi là train phương pháp.
5. Không chạy git.
6. Không ghi kết quả vào `thesis-master/` (thư mục clone).
7. Không nâng xác suất 5–10% thành cam kết.
8. Kết quả G0/G1 ghi một file ngoài clone, có bảng số và script.

## Phụ lục A — script G0

Chạy từ thư mục cha của `thesis-master`, hoặc sửa `p`.

```python
import json, re, difflib

p = "thesis-master/runs/score_s1_seed101_raw.jsonl"
rows = [json.loads(x) for x in open(p, encoding="utf-8")]

def tok(s):
    return re.findall(r"\w+", (s or "").lower())

def one_block(h, g, max_new=1, min_equal=3):
    a, b = tok(h), tok(g)
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    bad = [x for x in ops if x[0] != "equal"]
    equal = sum(i2 - i1 for tag, i1, i2, j1, j2 in ops if tag == "equal")
    return (h.lower() != g.lower() and len(bad) == 1
            and bad[0][4] - bad[0][3] <= max_new and equal >= min_equal)

n = len(rows)
exact = 0
block = []
for r in rows:
    h = (r.get("sent") or "").strip()
    g = (r.get("gold_instruction") or "").strip()
    if h.lower() == g.lower():
        exact += 1
    elif one_block(h, g):
        block.append(r)

miss = sum(1 for r in block if not r.get("hit_disk"))
print("n", n)
print("exact", exact, round(100 * exact / n, 2))
print("one_block", len(block))
print("one_block_hit_disk_0", miss)
print("G0", "DAT" if miss >= 250 else "TRUOT")
```

Kỳ vọng đối chiếu: `n` 4463, `exact` 954, `one_block` 958. Nếu lệch các số này, dừng và báo, đừng
diễn giải cổng.

## Phụ lục B — đầu ra bắt buộc của chat kia

Tạo đúng một file ngoài clone, gồm:

1. nguyên văn output script G0;
2. bảng `one_block_hit_disk_0/1`, tỉ lệ và khoảng tin cậy bootstrap theo episode;
3. phân rã `replace/delete/insert`, `action_ok` và app;
4. 10 ví dụ `hit_disk`=0 cùng 10 ví dụ `hit_disk`=1;
5. phán quyết G0 ĐẠT/TRƯỢT;
6. mục G1 CHƯA CHẠY — thiếu q/p, trừ khi người dùng đã cung cấp checkpoint/pilot thật;
7. nguyên văn script đã dùng.
