# -*- coding: utf-8 -*-
"""Kéo NỐT ảnh tập DẠY còn thiếu, quét cả 76 shard trên HuggingFace.

Vì sao quét cả 76: đo thật 27/9 cho thấy episode_id của shard 1 và shard 40 chồng lấn gần như
toàn bộ dải (116-18154 vs 142-18166) — 76 shard KHÔNG chia theo episode_id, coi như xáo trộn.
Không có cách suy ra ảnh nào nằm ở shard nào mà không tải, nên phải quét hết.

    ~/.venvs/thesis/bin/python harness/keo_anh_train_day_du.py

Ghi dần + xả đệm để coi tiến độ qua log; xoá parquet ngay sau khi trích ảnh (mỗi shard chỉ đọc
một lần). Bỏ qua ảnh đã có sẵn trên đĩa (không tải lại, không ghi đè).
"""
import os, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
IMG = os.path.join(ROOT, "images")
IMG_REPO = "ckg/AndroidControlParsedWithImages-20k"
N_SHARDS = 76


def main():
    from huggingface_hub import hf_hub_download
    import pyarrow.parquet as pq

    have = set(os.listdir(IMG))
    all_rows = [json.loads(x) for x in open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8")]
    need = {}
    for r in all_rows:
        fn = r["image"].split("/")[-1]
        if fn not in have:
            need[(int(r["episode_id"]), int(r["step_id"]))] = fn
    print(f"train.jsonl {len(all_rows)} dòng, đã có ảnh {len(have)}, còn thiếu {len(need)}", flush=True)

    t0 = time.time()
    got_total = 0
    for i in range(N_SHARDS):
        ts = time.time()
        p = hf_hub_download(IMG_REPO, f"data/train-{i:05d}-of-00076.parquet", repo_type="dataset")
        pf = pq.ParquetFile(p)
        n = 0
        for b in pf.iter_batches(batch_size=200):
            for r in b.to_pylist():
                j = r["json"]
                if isinstance(j, (bytes, str)):
                    j = json.loads(j)
                k = (int(j["episode_id"]), int(j["step_id"]))
                fn = need.get(k)
                if fn is None:
                    continue
                with open(os.path.join(IMG, fn), "wb") as f:
                    f.write(r["png"]["bytes"])
                del need[k]
                n += 1
        del pf
        try:
            os.remove(p)
        except OSError as e:
            print(f"   (khong xoa duoc {p}: {e})", flush=True)
        got_total += n
        elapsed = time.time() - t0
        rate = (i + 1) / elapsed
        eta = (N_SHARDS - i - 1) / rate if rate > 0 else 0
        print(f"shard {i:02d}/{N_SHARDS-1}: +{n} anh (cong don {got_total}), con thieu {len(need)}, "
              f"{time.time()-ts:.1f}s, da {elapsed/60:.1f} phut, con lai ~{eta/60:.1f} phut", flush=True)
        if not need:
            print("HET can lay, dung som.", flush=True)
            break

    print(f"XONG. Tong ảnh lấy thêm: {got_total}. Con thieu sau cung: {len(need)}", flush=True)
    if need:
        print("Danh sach con thieu (toi da 20 dong dau):", flush=True)
        for k in list(need)[:20]:
            print("  ", k, need[k], flush=True)


if __name__ == "__main__":
    main()
