# -*- coding: utf-8 -*-
"""Kéo ảnh tập DẠY cho các bước nằm trong 8 shard rải đều, để dựng tập val.

    ~/.venvs/thesis/bin/python harness/keo_anh_val.py        # ~1,3 GB, 10-20 phút

⛔ KHÔNG ghi đè train.jsonl. Chỉ ghi ảnh + một danh sách khoá.
   (`build_train_data.py:157` thì CÓ ghi đè và chỉ lấy n_shards ĐẦU — đừng dùng nó cho việc này.)

Vì sao 8 shard rải đều chứ không phải toàn bộ 76: val chỉ cần ~1.000 bước, mà `train_ac/images/`
hiện chỉ có 1.697 ảnh của lát thử 29/7. Kéo trọn 76 shard là ~12 GB; ràng buộc val vào 8 shard
chỉ tốn ~1,3 GB. Chọn shard rải đều để giảm tương quan với thứ tự thu thập dữ liệu.
⚠️ Hệ quả phải khai khi viết: val ngẫu nhiên TRONG 8 shard, không phải trên toàn tập dạy.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
IMG = os.path.join(ROOT, "images")
SHARDS = [0, 10, 21, 32, 43, 54, 65, 75]
IMG_REPO = "ckg/AndroidControlParsedWithImages-20k"   # khớp build_train_data.py:28


def main():
    from huggingface_hub import hf_hub_download
    import pyarrow.parquet as pq

    can = {(int(r["episode_id"]), int(r["step_id"]))
           for r in map(json.loads, open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8"))}
    print(f"train.jsonl có {len(can)} bước", flush=True)
    os.makedirs(IMG, exist_ok=True)

    co = []
    for i in SHARDS:
        p = hf_hub_download(IMG_REPO, f"data/train-{i:05d}-of-00076.parquet", repo_type="dataset")
        pf = pq.ParquetFile(p)
        n = 0
        for b in pf.iter_batches(batch_size=100):
            for r in b.to_pylist():
                j = r["json"]
                if isinstance(j, (bytes, str)):
                    j = json.loads(j)
                k = (int(j["episode_id"]), int(j["step_id"]))
                if k not in can:
                    continue
                with open(os.path.join(IMG, f"ep{k[0]}_s{k[1]}.png"), "wb") as f:
                    f.write(r["png"]["bytes"])
                co.append(k)
                n += 1
        del pf
        try:                                  # parquet ~1,5 GB/shard, đừng giữ lại
            os.remove(p)
        except OSError as e:
            print(f"   (không xoá được {p}: {e})", flush=True)
        print(f"  shard {i:02d}: +{n} ảnh  (cộng dồn {len(co)})", flush=True)

    json.dump([list(k) for k in co], open(os.path.join(ROOT, "khoa_co_anh.json"), "w"), indent=0)
    print(f"TỔNG {len(co)} ảnh / {len({k[0] for k in co})} episode → khoa_co_anh.json", flush=True)


if __name__ == "__main__":
    main()
