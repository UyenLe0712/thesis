# Kaggle — sequence-score 1.400 bước trên HAI T4, hai lượt commit (viết 5/9/2026)

> Thay **ô 7** của `kaggle_SEQSCORE_SAU_O.md`. Ô 1 · 2 · 3 · 4 giữ nguyên, dán y hệt.
> Ô 5 và 6 (probe) **không** đưa vào commit.

## Vì sao phải viết lại ô 7

Probe 5/9 (50 bước) đo được **56,5 s/bước** ở đường chậm, và đường nhanh **đã bị loại** vì phép
kiểm chéo lệch 8,49e-03 > 1e-3 (commit `3b51cc5`: chọn đường chậm, không nới ngưỡng).
⇒ 1.400 bước × 56,5 s = **22,0 giờ** một tiến trình. Ước tính *"khoảng 4,7 giờ"* trong
`kaggle_SEQSCORE_SAU_O.md` **sai**, và 22 h vượt trần 12 h của một lượt commit Kaggle.

Cách xử, không đổi mã: máy ảo có **hai** T4, còn `device_map="auto"` của một tiến trình chỉ
**xẻ** mô hình sang hai card rồi chạy tuần tự (mỗi card bận một nửa thời gian). Chạy **hai tiến
trình**, mỗi tiến trình ghim một card bằng `CUDA_VISIBLE_DEVICES`, mỗi bên 700 bước ⇒ ~11 h
tường. Vẫn sát trần 12 h, nên chia làm **hai commit**, mỗi commit dừng ở **cổng giờ 5,5 h**
rồi lượt sau **nối tiếp** — `seq_score_sel.py` ghi từng dòng + `flush()` và khi mở lại tự bỏ
dòng ghi dở, nên giết tiến trình giữa chừng là an toàn.

Hạn mức máy: mỗi commit ≈ 5,7 h ⇒ hai commit ≈ **11,5 h**, vừa phần còn lại của tuần
(≈ 19 h sau khi đã tiêu ~11 h). Quota Kaggle tính theo **giờ phiên**, không nhân đôi khi dùng
hai card — đó là lý do hai tiến trình song song rẻ đúng bằng một.

⚠️ Khi ghim một card, tiến trình chỉ còn 16 GB thay vì 32 GB. Trọng số fp16 ≈ 7,5 GB, lô 4 span
thêm ≈ 2–3 GB ⇒ đủ; nếu log báo `CUDA out of memory` thì hạ `SPAN_BATCH = 2` và chạy lại.

⛔ **KHÔNG dùng `--limit` để chia bước** — cờ đó cắt danh sách **trước** khi nối tiếp, nên lượt
sau sẽ thấy "Xong sẵn" và dừng dù còn 700 bước. Chia bằng hai tệp `--only`.

---

## Ô 7 — hai tiến trình song song, cổng giờ 5,5 h, nối tiếp được

```python
import os, json, time, glob, shutil, signal, subprocess

SPAN_BATCH = 4            # hạ xuống 2 nếu log báo out of memory
CONG_GIO   = 5.5          # giờ; quá mốc này thì dừng cả hai, để commit sau nối tiếp
p_dev = f"{GOI}/runs/sel/preds_gui_sel_seed101_dev1400.jsonl"     # ĐÚNG gói, không glob mù

# ── chia danh sách bước làm hai nửa CỐ ĐỊNH (700 dòng đầu / 700 dòng sau) ──────────
lines = open(p_dev, encoding="utf-8").read().splitlines()
assert len(lines) == 1400, f"DỪNG: tệp dev có {len(lines)} dòng, phải là 1400"
NUA = {}
for g in (0, 1):
    NUA[g] = f"/kaggle/working/only_dev_gpu{g}.jsonl"
    open(NUA[g], "w", encoding="utf-8").write("\n".join(lines[700*g:700*(g+1)]) + "\n")

# ── nối tiếp: nếu là commit thứ hai, mang tệp dở của commit trước về /kaggle/working ──
# Sau commit 1: Add data ▸ "Your notebook output" ▸ chọn chính notebook này (bản mới nhất).
OUT = {g: f"/kaggle/working/seqscores_gui_sel_seed101_dev1400_gpu{g}.jsonl" for g in (0, 1)}
for g in (0, 1):
    cu = [p for p in glob.glob(f"/kaggle/input/**/{os.path.basename(OUT[g])}", recursive=True)]
    if cu:
        cu = max(cu, key=lambda p: sum(1 for _ in open(p, encoding="utf-8")))   # bản DÀI hơn
        shutil.copy(cu, OUT[g])
        print(f"gpu{g}: nối tiếp từ {cu} · {sum(1 for _ in open(OUT[g]))} dòng")
    else:
        print(f"gpu{g}: lượt mới (không thấy tệp dở trong /kaggle/input)")

# ── phóng hai tiến trình, mỗi tiến trình ghim MỘT card ─────────────────────────────
env0 = {**os.environ, "PYTHONUNBUFFERED": "1", "TQDM_DISABLE": "1",
        "HF_HUB_DISABLE_PROGRESS_BARS": "1"}
P, F = {}, {}
for g in (0, 1):
    F[g] = open(f"/kaggle/working/c3_seqscore_gpu{g}.log", "a")
    P[g] = subprocess.Popen(
        ["python", f"{WS}/harness/seq_score_sel.py",
         "--adapter", AD,
         "--cands", f"{WS}/harness/dg1_cache/test_ac/candidates.jsonl",
         "--only", NUA[g], "--out", OUT[g], "--span-batch", str(SPAN_BATCH)],
        stdout=F[g], stderr=subprocess.STDOUT, start_new_session=True,
        env={**env0, "CUDA_VISIBLE_DEVICES": str(g)}, cwd=WS)
    print(f"gpu{g}: PID {P[g].pid}")

# ── theo dõi cả hai, dừng cả hai ở cổng giờ ────────────────────────────────────────
T0 = time.time()
dem = lambda p: sum(1 for _ in open(p, encoding="utf-8")) if os.path.exists(p) else 0
while any(p.poll() is None for p in P.values()):
    time.sleep(120)
    gio = (time.time() - T0) / 3600
    n0, n1 = dem(OUT[0]), dem(OUT[1])
    print(f"{time.strftime('%H:%M:%S')} · {gio:5.2f} h · gpu0 {n0}/700 · gpu1 {n1}/700 · "
          f"tổng {n0+n1}/1400", flush=True)
    if gio >= CONG_GIO:
        print(f"⏱ quá cổng {CONG_GIO} h — dừng cả hai để commit sau nối tiếp", flush=True)
        for p in P.values():
            if p.poll() is None:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        time.sleep(20)
        break

for g in (0, 1):
    F[g].close()
    print(f"\n=== gpu{g}: mã thoát {P[g].poll()} · {dem(OUT[g])}/700 dòng · 20 dòng log cuối ===")
    print(subprocess.run(["tail", "-20", f"/kaggle/working/c3_seqscore_gpu{g}.log"],
                         capture_output=True, text=True).stdout)

# Mã thoát khác 0 CHỈ chấp nhận được khi là do cổng giờ (-15 = SIGTERM). Lỗi thật thì dừng.
for g in (0, 1):
    rc = P[g].poll()
    assert rc in (0, -15, None), f"DỪNG: gpu{g} thoát mã {rc} — đọc log ở trên"
print("\nTỔNG:", dem(OUT[0]) + dem(OUT[1]), "/ 1400")
```

## Đọc kết quả

- **Trong 10 phút đầu** mỗi log phải có dòng `manifest:` rồi `[20/700] … s/bước`. Không thấy
  ở một trong hai bên sau 10 phút ⇒ mở log, thường là out of memory ⇒ `SPAN_BATCH = 2`.
- Giây/bước mỗi bên ≈ **55–60 s**. Nếu một bên ≈ 110 s thì hai tiến trình đang tranh cùng
  một card — `CUDA_VISIBLE_DEVICES` không có tác dụng; dừng và báo lại.
- Commit 1 kết thúc ở cổng giờ với **≈ 350/700 mỗi bên**. Commit 2 nối tiếp và kết thúc ở
  `mã thoát 0` cả hai bên, `TỔNG: 1400 / 1400`.

## Sau commit 2

Tải hai tệp `seqscores_gui_sel_seed101_dev1400_gpu0.jsonl` và `…_gpu1.jsonl` về `runs/sel/`.
Gộp bằng `cat` là đủ (cùng chữ ký `seqscore:gui-sel-adapter`, khoá không trùng vì hai nửa
rời nhau). Quét τ trên máy nhà, 0 GPU, theo (x16d).
