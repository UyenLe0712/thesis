# MIN-ONPOLICY trên Colab — dán thẳng, tự đủ

Biến thể đăng ký trước ở `report/106` mục **(x11)**. Đổi đúng **một** thứ so với MIN-DESC:
nguồn vế âm. Mọi khoá cấu hình khác giữ nguyên — đã `diff` xác nhận chỉ `dataset` và
`output_dir` khác.

**Tổng: ~13,5 giờ GPU Colab · 0 giờ quota Kaggle** cho tới khi qua cổng khai báo.

| ô | việc | giá | dừng được không |
|---|---|---|---|
| **O1** | S2 tự sinh khai báo trên màn tập dạy | ~3,5 h | ✅ nối tiếp được |
| **O2** | dựng cặp + **ba cổng (x11c)** | vài phút CPU | ⛔ **trượt cổng ⇒ DỪNG HẲN** |
| **O3** | train MIN-ONPOLICY | ~5 h | ✅ chạy tiếp từ checkpoint |
| **O4** | train CE2-ONPOLICY | ~3 h | ✅ |
| **O5** | sinh câu trên lát tập kiểm, hai nhánh | ~2 h | ✅ |
| **O6** | cổng khai báo `gate_desc_acc.py` | vài giây CPU | quyết có chấm Kaggle không |

---

## O0 — chuẩn bị máy

Chạy **y nguyên** ô **T1 → Restart → T2 → T3** của `harness/colab_train_min_desc.md`.
Không có gì mới. Ba dòng phải đúng ở T2: ảnh dạy **64.567** · khai báo **41.099** ·
`ckpt S2 = True`.

⚠️ O1 cần **ảnh tập dạy** (31 GB), đó là khâu lâu nhất của T2. Đừng bỏ.
⚠️ Sau T2 **phải chạy T3** — `derived.tar.gz` ghi đè `dataset_info.json`.

---

## O1 — S2 tự sinh khai báo trên màn tập dạy

```python
import subprocess, os
D, REPO = "/content/drive/MyDrive/thesis", "/content/ws/thesis"
OUT = "/content/desc_train_s2.jsonl"      # ⚠️ ghi vào ĐĨA MÁY ẢO, không phải Drive

# ⛔ Bài học 24/8: --out trỏ thẳng vào Drive KHÔNG sống sót qua mất máy (tệp mở chế độ "a"
#    chưa đóng lần nào thì FUSE chưa đẩy lên cloud, mà `ls` vẫn hiện tệp như thường).
#    Ghi đĩa máy ảo rồi chụp định kỳ sang Drive bằng cp — cp tạo rồi ĐÓNG tệp mới.
os.makedirs(f"{D}/onpolicy", exist_ok=True)
subprocess.Popen(["bash","-lc",
    f'while true; do cp -f {OUT} {D}/onpolicy/ 2>/dev/null; sleep 300; done'])
print("đã bật chụp Drive 5 phút/lần")

!cd {REPO} && python3 harness/sinh_desc_train.py \
    --adapter {D}/ckpt/s2_seed101 --out {OUT} --limit 14000
```

· `--limit 14000` đủ cho ~12.800 mẫu mà 800 bước × tích luỹ 16 sẽ đi qua. Muốn phủ rộng hơn
  thì bỏ cờ này (41.099 bước ≈ 10 h) — nhưng **chất lượng cặp quan trọng hơn số lượng**, xem
  `report/120` Mục 1.4.
· `--max-new 64`: chỉ sinh tới hết `</desc>`, không sinh câu ⇒ rẻ hơn `infer_branch` nhiều.
· Mất máy: dựng lại máy rồi gõ **y nguyên** lệnh trên, phải thấy `Nối tiếp: đã có N bước`.
  Bản chính mất thì chép về từ `{D}/onpolicy/`, **so `wc -l` giữ bản dài hơn**.

---

## O2 — dựng cặp và ĐỌC BA CỔNG  ⛔ chốt chặn quan trọng nhất

```python
!cd {REPO} && python3 harness/build_min_desc_onpolicy.py {OUT}
```

Lần đầu chạy sẽ tải `all_forest_dict.zip` từ HuggingFace (cây trợ năng 99.131 màn) — vài phút.

**Đọc kết quả — ba cổng của (x11c), trượt cái nào cũng DỪNG:**

| dòng in ra | ĐẠT | TRƯỢT ⇒ dừng, không train |
|---|---|---|
| `① lối tắt độ dài — luật 'vế NGẮN hơn là chosen' đoán đúng` | **< 55%** | ≥ 55% |
| `① lối tắt chuỗi — tách được bằng '(no name)'` | **0%** | khác 0 |
| `③ eligibility` | **≥ 25%** | < 25% |
| `BẤT BIẾN` — năm dòng | **tất cả ✅** | có ⛔ |

⚠️ Cổng ② (false negative) đã ép ngay lúc dựng: mọi cặp có phần tử nhầm cách gold 80–350 px và
không chồng lấn hộp gold.

⛔ **Trượt thì dừng thật, đừng nới ngưỡng.** Dự án đã tự khai hai lần nới ngưỡng sau khi thấy
số; hồ sơ (x11c) khoá con số này trước khi có dữ liệu. Trượt là một kết quả, ghi lại rồi báo.

---

## O3 · O4 — train hai nhánh

Dùng **y nguyên** ô **T4 → T7** của `colab_train_min_desc.md`, chỉ sửa hai dòng ở T4:

```python
NHANH, SEED = "min_onpolicy", 101      # O4 đổi thành ("ce2_onpolicy", 101)
CFG_GOC = {"min_desc": "train_config_orpo.yaml",
           "ce2_s2":   "train_config_ce2.yaml",
           "min_onpolicy": "train_config_orpo_onpolicy.yaml",   # ★ thêm
           "ce2_onpolicy": "train_config_ce2_onpolicy.yaml"}[NHANH]
```

Mọi cảnh báo của runbook cũ áp nguyên: `output_dir` phải RỖNG ở lượt mới · stage `dpo` **không**
ghi `loss`/`lr` vào `trainer_log.jsonl` còn stage `sft` thì có · ô theo dõi đọc **hai nguồn**.
Cổng cơ học sau train: `global_step` = **800** ở cả hai.

---

## O5 — sinh câu trên lát tập kiểm

```python
for ten in ("min_onpolicy_seed101", "ce2_onpolicy_seed101"):
    !cd {REPO} && python3 harness/infer_branch.py --adapter {D}/ckpt/{ten} \
        --out /content/preds_{ten}.jsonl --limit 3000
    !cp /content/preds_{ten}.jsonl {D}/onpolicy/
```

⚠️ Cần **ảnh tập kiểm**: `!tar xf {D}/test_images.tar -C {REPO}/harness/dg1_cache/test_ac`
(3,2 GB, ~3 phút) nếu máy ảo chưa bung.

---

## O6 — cổng khai báo, và luật quyết đã khoá ở (x11d)

```python
!cd {REPO} && python3 harness/gate_desc_acc.py \
    {D}/preds_s2_seed101.jsonl \
    /content/preds_ce2_onpolicy_seed101.jsonl \
    /content/preds_min_onpolicy_seed101.jsonl
```

**Đại lượng chính:** `Δ_desc = MIN-ONPOLICY − CE2-ONPOLICY` ở cột **CẢ HAI ĐÚNG**.
Mốc so là MIN-DESC hiện tại: **MIN 60,6 − CE2 59,8 = +0,80 pp**.

| kết quả | làm gì |
|---|---|
| `Δ_desc` ≥ **+2,80** (tức hơn mốc +0,80 ít nhất 2,0) | ✅ chi 10,8 h Kaggle chấm executability |
| `Δ_desc` < +2,80 | ⛔ **KHÔNG chấm.** Ghi vào bài như một nhánh của ablation nguồn cặp |

⛔ Ngưỡng +2,0 pp khoá ở **(x11d)**, trước khi có số. Không nới.
⛔ Dù ra chiều nào cũng **báo cả ba nhánh** (heuristic · on-policy · CE2) — cam kết (x11d).

---

## Nếu O2 trượt cổng

Đó **không** phải thất bại của phiên. Nó là kết quả: *nguồn vế âm on-policy không dựng được
tập cặp hợp lệ dưới ràng buộc đã khoá*. Ghi vào `report/106` mục (x11) phần kết quả, và bài vẫn
có ablation hai nhánh (heuristic · CE2) như hiện tại. Chi phí biết mình sai: **4 giờ, không phải
13,5 giờ.**
