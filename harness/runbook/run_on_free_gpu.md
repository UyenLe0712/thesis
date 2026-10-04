# Chạy trên GPU miễn phí — làm được ba trong bốn thứ chưa biết, không tốn xu nào

Trước khi thuê máy, ba trong bốn mắt xích chưa ai chạy đều kiểm được trên **Kaggle** (30 giờ
GPU mỗi tuần, T4 ×2 hoặc P100) hoặc **Colab bản miễn phí** (T4, phiên ngắn hơn). Thứ *không*
làm được ở đó là huấn luyện thật trên toàn bộ dữ liệu — cái đó vẫn phải thuê.

Vì sao đáng làm: lỗi bắt được ở đây có giá **0 đô**, còn cùng lỗi đó bắt được trên máy thuê thì
mất tiền theo giờ, và tệ hơn là dễ bị đọc nhầm thành "bộ trỏ kém" hay "mô hình kém".

> **Card miễn phí không có bf16.** T4 là Turing, P100 là Pascal — cả hai đều không hỗ trợ.
> `pick_dtype()` trong `infer_branch.py` và `score_run.py` tự dò và lùi về fp16, nên không phải
> sửa gì. Nhưng `train_config.yaml` thì **phải** đổi `bf16: false` / `fp16: true` nếu chạy thử
> huấn luyện ở đây — và bản chạy đó **chỉ để kiểm cấu hình**, không được lấy số.

---

## Việc 1 — Cổng A với UGround  ·  ~15 phút  ·  giá trị cao nhất

UGround-V1-2B là mô hình 2 tỉ tham số làm suy luận, fp16 chỉ tốn khoảng 4,4 GB. T4 16 GB thừa sức.
300 bước mất chừng 10–15 phút.

```bash
pip install -q transformers accelerate pillow
python harness/kaggle_precheck.py                   # vài giây, không cần mạng
python harness/score_run.py --mode gate --grounder uground --n 300 --out gate_A.json
```

> **⚠ Bản trước ghi `--shards 2` "đủ cho 300 bước" — SAI, đã sửa.** Mẫu 300 bước lấy
> bằng cách xáo TOÀN BỘ 4.463 bước chạm với hạt giống 20260805 rồi cắt 300 đầu. Dựng
> 2 shard cho ra một `test.jsonl` ngắn hơn, nên mẫu xáo ra là một tập KHÁC với tập đã
> đăng ký — mà chương trình vẫn chạy trơn và vẫn in ra một con số. Muốn dựng lại thì
> phải đủ `--shards 9`; hoặc mang sẵn 300 ảnh đó theo, đúng cái `kaggle_precheck.py`
> kiểm ở mục [3].

Đọc kết quả theo đúng bảng đã khoá ở `report/106` sửa đổi 6/8 mục i — **đọc trước khi nhìn số**:
dưới 0,5% là nghi lỗi vì quá đẹp · 0,5–5% đúng kỳ vọng · 5–15% kém nhưng hợp lý · trên 15% là
nghi lỗi cài đặt chứ **không** được đọc thành "bộ trỏ kém". Bốn dấu hiệu lỗi in sẵn ngay dưới con
số chính; rớt cổng chỉ được ghi là "bộ trỏ không đạt" sau khi cả bốn đã im.

## Việc 2 — Tự kiểm lô  ·  ~5 phút

Phép bắt lỗi đệm sai bên. Chạy được trên mô hình gốc, chưa cần bộ trọng số nhánh nào.

```bash
python harness/infer_branch.py --selftest-batch --no-adapter --batch 8
```

Rớt tức đệm sai bên, và mọi con số chấm theo lô đều không tin được.

## Việc 3 — Cấu hình huấn luyện có được LLaMA-Factory nhận không  ·  ~20 phút

Không nhằm lấy trọng số, chỉ nhằm biết cấu hình có chạy trơn không: dữ liệu nạp được, mẫu
sharegpt đúng, ảnh tìm thấy, QLoRA gắn được, mất mát có giảm.

```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory && pip install -e "LLaMA-Factory[torch]"
python - <<'PY'
import yaml
c = yaml.safe_load(open("harness/train_config.yaml"))
c.update({"bf16": False, "fp16": True,          # T4/P100 không có bf16
          "max_steps": 10, "output_dir": "/tmp/smoke",
          "dataset_dir": "harness/dg1_cache/train_ac/branches",
          "per_device_train_batch_size": 1, "gradient_accumulation_steps": 1})
yaml.safe_dump(c, open("/tmp/smoke.yaml", "w"), allow_unicode=True, sort_keys=False)
PY
llamafactory-cli train /tmp/smoke.yaml
```

Chạy được 10 bước là **đủ**. Xoá `/tmp/smoke` sau đó — trọng số này vô giá trị, và giữ lại chỉ
tổ có ngày ai đó lấy nhầm ra chấm.

## Việc 4 — nhánh B-infer, thử câu nhắc  ·  ~10 phút

```bash
python harness/infer_branch.py --b-infer --no-adapter --out /tmp/binfer_smoke.jsonl --limit 20
```

Mô hình gốc chưa huấn luyện nên câu sẽ dở — **không lấy số**. Chỉ để xem câu nhắc có phình quá
`cutoff_len: 2048` không, và danh sách phần tử có đọc được không.

---

## Sau bốn việc này thì còn lại gì cho máy thuê

Huấn luyện thật. 64.500 bước × 2 lượt duyệt × 6 lượt chạy — thứ này T4 không kham nổi trong giới
hạn phiên của bản miễn phí, và cũng không nên chia nhỏ ra chạy chắp vá vì mỗi lần đứt là một lần
rủi ro cho phép so giữa các nhánh.

Nhưng lúc đó **cả bốn mắt xích đều đã chạy ít nhất một lần**, nên tiền thuê chỉ còn dùng vào việc
nó đáng dùng, không dùng vào việc mò lỗi cài đặt.
