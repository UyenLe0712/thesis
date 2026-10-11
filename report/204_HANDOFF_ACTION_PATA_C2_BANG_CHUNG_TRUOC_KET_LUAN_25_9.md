# 204 - HANDOFF ACTION: LẤY BẰNG CHỨNG TRƯỚC KHI CHỌN THAY C1

**Ngày:** 25/09/2026.

> Bản chép và tái cấu trúc từ 3 ảnh trong ZIP. Các đoạn trùng đã được gộp. Xem [nguồn và thứ tự ảnh](README.md). Nội dung bên dưới là tài liệu được trích xuất, không phải báo cáo thí nghiệm mới.

**Cho chat sau:** không có ngữ cảnh lượt này. Đọc file này là đủ. Không đọc diff. Không git trừ `clone`.

## 1. Việc đang làm

C1 âm về coupling, không phải thất bại toàn PATA.

- **Giữ:** Stage S, TARGET + localizer H/J (mass box 0,277; hit 52,0%; prompt xáo 0,115).
- **Bỏ:** bridge mean-pool một vector → một token TARGET một lần. On/off exec +1/602; D/R listener 100 vs 102 về D → ngược hướng.
- **Chưa chọn:** RCA hay dual-view crop. File 200/202 chốt RCA quá sớm. File này thắng chúng về thứ tự: đo rồi mới chọn.

**Mục tiêu:** phân biệt thiếu routing hay thiếu pixel, rồi chỉ code đúng một replacement. Val600 không dùng để chọn. Test đóng.

## 2. C1 so với D.3 / BLEU / ROUGE: số đã có

### 2.1. So sánh trên cùng tập val600

So hợp lệ duy nhất: C1 vs S trên cùng val600, n=602. Không so C1 với Pipeline/S1 trên test 4.463 như cùng benchmark.

| Nhánh | exec | D.3 | AitW | BLEU-4 câu | ROUGE-L |
| --- | ---: | ---: | ---: | ---: | ---: |
| S val600 | 60,13 | 66,94 | 75,91 | 35,65 | 67,87 |
| C1 bật | 61,13 | 67,44 | 77,91 | 33,90 | 67,71 |
| C1 tắt bridge | 60,96 | 67,44 | 77,74 | 34,04 | 66,87 |

**C1 − S, KTC95 cụm:**

| Chỉ số | Chênh lệch | KTC95 cụm |
| --- | ---: | --- |
| exec | +1,00 | [−1,74; +4,02] |
| D.3 | +0,50 | [−2,28; +3,55] |
| AitW | +1,99 | [−0,54; +4,85] |
| BLEU-4 | −1,75 | Không ghi trong ảnh |
| ROUGE-L | −0,16 | Không ghi trong ảnh |

Bật/tắt D.3 bằng nhau tuyệt đối (6/6).

### 2.2. Vị trí thang đo, chỉ để biết

Không dùng phần này để claim. Pipeline/GRPO trên test 4.463 có:

- exec: 60,07.
- D.3: 67,04.
- BLEU-4 câu: 37,78.
- ROUGE-L: 68,47.

C1 val600 D.3 67,44 trông ngang, BLEU thấp hơn khoảng 4 điểm; split khác, không được viết “C1 hơn/kém Pipeline”.

COCO corpus BLEU-4 của S1/Pipeline khoảng 50–52. Số C1 33,90 là BLEU-4 trung bình mức câu, không smoothing (`harness/text_metrics.py`). Không trộn với COCO. C1 chưa có artifact COCO.

### 2.3. Định nghĩa BLEU/ROUGE C1

Tính từ `preds_*_val600_*.jsonl`:

```text
token = re.findall(r"\w+", sentence.lower())
BLEU-4 = mean(sentence_bleu([gold], pred, no_smoothing)) * 100
ROUGE-L = mean(F1_LCS(gold, pred)) * 100
```

**Cách đọc:** D.3 không chứng minh C1 thắng; BLEU còn xấu hơn S trên cùng split; bridge không đổi D.3. Không lấy BLEU/ROUGE làm primary.

## 3. Clone và dữ liệu

Clone: `.../thesis/thesis-master` (dùng một lần, sẽ bị xoá).

Train cache không có trên clone: `descriptors.jsonl`, `ocr.jsonl`, `images/`, `pata/train_proper.jsonl` đều gitignore.

Trước mọi GPU:

```bash
python harness/build_train_data.py
python harness/prep_ocr_train.py
# patch descriptor rồi:
python harness/descriptor_label_build.py
python harness/pata_data.py
```

File mã mới phải nằm ngoài `thesis-master/` nếu chưa commit, hoặc người dùng commit trước khi clone lại.

## 4. Action theo thứ tự: dừng ngay khi cổng fail

### 4.1. P0: true-D + audit

**Tài nguyên:** 0 GPU; 1–2 ngày.

1. Patch `harness/descriptor_label_build.py`: `nearest_other()` đã có hộp D trong RAM; ghi thêm `box_neg`, `name_neg`, `role_neg`, `cls_neg`, `point_neg_*`, `area_share_neg`. Không dựng D bằng kích thước hộp vàng quanh `<point>` (`pata_swap.py` hiện làm vậy).
2. Tỷ lệ `box_neg` phải bằng tỷ lệ `desc_neg` (khoảng 55,6%). Lệch = patch sai.
3. Dựng cặp eligible: G/D thật, cùng class, không parent/child, IoU < 0,30, box hợp lệ không quá lớn, câu vàng không đúng cho D, khoảng cách tâm 80–350 px.
4. Cần ≥150 cặp val400 (mục tiêu 300). Dưới 150 → dừng C2.
5. Audit mù 100 mẫu: câu vàng + khung A/B đảo ngẫu nhiên. Đạt nếu chọn đúng G ≥75%, “cả hai đúng” ≤15%, D không phải widget ≤10%. Trượt một lần thì sửa builder + audit mẫu mới; trượt lần 2 → dừng.

Chat mới chỉ có file 204. Viết `pata_true_d.py` / `pata_audit_d.py` / runner P1 theo spec ở đây. Không cần file 201–203. Đừng so mask xám với ảnh tự nhiên.

### 4.2. P1: likelihood 7 nhánh

**Tài nguyên:** T4 2–5 h; val400 only.

Speaker S đóng băng. Cùng prompt + câu vàng. Crop G/D/R cùng kích thước cửa sổ, cùng token count, cùng prompt; không branch ID.

| Nhánh | Ảnh 1 | Ảnh 2 |
| --- | --- | --- |
| O | full | không |
| L_G, L_D, L_R | full | crop từ bản full đã resize (không thêm chi tiết) |
| H_G, H_D, H_R | full | crop từ screenshot gốc (có thêm chi tiết) |

#### Điểm likelihood và các chênh lệch

```text
s = mean log p(y_t | y_<t, nhánh)
ΔL_GD = s(L_G) − s(L_D)     ΔL_GR = s(L_G) − s(L_R)
ΔH_GD = s(H_G) − s(H_D)     ΔH_GR = s(H_G) − s(H_R)
Δres = ΔH − ΔL
```

Bootstrap cụm episode, 10k. Directional đạt khi:

```text
lower90(Δ_GD) > 0 AND lower90(Δ_GR) > 0 AND mean(Δ_GD) ≥ 0,02 nats/token
```

> Ghi chú chuyển đổi: dòng điều kiện directional trong ảnh dùng `Δ_GD` và `Δ_GR`, không ghi chỉ số L/H. Giữ nguyên ký hiệu này; các chênh lệch L/H được định nghĩa ngay phía trên.

Extra-resolution đạt khi:

```text
lower90(Δres_GD) > 0 AND lower90(Δres_GR) > 0 AND mean cả hai ≥ 0,01
```

**Assert:** G=D nhân tạo → gap 0; đổi thứ tự nhánh không đổi score; không dropout; token count khớp trong họ L và họ H.

#### Bảng chọn

Khóa trước, ghi vào `p1_decision.json`:

| Kết quả | Kết luận | Action |
| --- | --- | --- |
| ΔL đạt, Δres không | thiếu routing | RCA `r=128`, 2 tầng |
| ΔL đạt và Δres đạt | routing + pixel; pixel thêm ích | dual-view trước (đơn giản hơn) |
| ΔL không, ΔH+Δres đạt | thiếu pixel | dual-view predicted crop |
| cả ΔL và ΔH không | vùng không đủ | dừng C2 |
| G−D đạt, G−R không | artefact D/R | sửa control, chưa chọn |
| H_G≈H_D≈H_R nhưng >O | thêm ảnh/compute | không claim grounding |

Không so mask xám với ảnh tự nhiên (file 202 sai chỗ đó).

### 4.3. P1b: predicted region

Gold chỉ là trần. Phải dùng α của H/J.

- **Dual-view:** crop = bbox các patch đến Σα≥τ, nới margin. Grid val400: τ∈{0,5; 0,7; 0,8}, margin∈{10; 20; 30}%. Chọn nhỏ nhất có median recall box G ≥0,75 và median area ≤0,35 màn. Predicted phải giữ ≥50% gold Δ.
- **RCA:** 1 tầng `r=128` overfit vài chục cặp; TF=KV; gate có grad; generate không dính state. Rồi mới 2 tầng.

Hit-in-box 52% là argmax, không phải crop recall. Phải đo coverage, đừng bác crop bằng 52%.

### 4.4. P2: generate G/D/R, chưa full train

Chỉ operator thắng P1. Không val600.

**Cổng:** D/R đổi câu ≥15%; listener `P(gần D|D) − P(gần D|R)` point ≥5 pp và lower90>0; format ≥99%. Fail → không A100.

### 4.5. P3-P4

Smoke 100–200 update trên val400. `s_G` không giảm; không chỉ phá `s_D`. Khóa recipe → một full run → val600 một lần. Test đóng.

## 5. Recipe nếu được phép code

**Chỉ sau P1, không trước.**

### 5.1. RCA

- Giữ V_mem+α tại block 17.
- Shared Wq/k/v/o 2048↔128 (khoảng 1,05M).
- 2 tầng; gate tanh init 0; không zero-init Wo.
- G/D cùng forward batch; backbone eval khi adapter-only.
- Logistic `softplus(-(sG-sD)/T)` trên eligible; CE toàn câu.
- Không full-rank, không 3 tầng mặc định. DeepStack không chứng minh chèn 18/20/22.

### 5.2. Dual-view

- H đóng băng trên ảnh 1.
- Train predicted crop (không train gold rồi infer predicted).
- Prompt cố định Ảnh1=full, Ảnh2=phóng vùng.
- Control: gold oracle, true-D, random cùng diện tích, blur nội dung giữ biên.

### 5.3. Phạm vi claim

Claim hẹp: controlled region-prior/evidence effect. Không viết “causal grounding”; không claim kiến trúc mới.

## 6. Kỳ vọng và chi phí

**Judgement, không đo.**

P(exec +3–4 pp, CI loại 0) từ hiện trạng ≈4–12%. Đóng góp khoa học đứng nếu coupling+listener+content control đạt dù exec không tăng.

Trước khi chọn kiến trúc: **3–5 ngày công, 3,5–10 h T4, 0 h A100**. Có thể dừng sau P0/P1.

## 7. Việc chat sau không tự làm nếu không được yêu cầu

- Không train A100, không mở test, không đổi ngưỡng sau khi thấy số.
- Không git trừ `clone`. Không commit/push.
- Không ghi vào `thesis-master/` trừ khi người dùng nói rõ (sẽ mất khi xoá clone).
