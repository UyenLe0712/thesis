# -*- coding: utf-8 -*-
"""288 G0 — bước 2 (Kaggle GPU): người nghe Phi-4 chấm 2.530 cặp (màn, câu) của g0_cau.jsonl.

    python g0_listener.py --backend phi4 --som g0_som.jsonl --cau g0_cau.jsonl --out g0_phi4_s0.jsonl --shard 0/2

Viết lại 6/10/2026 từ bản mô tả B.4 (mã gốc ở máy Mac) ⇒ md5 khác bản gốc.
Giao thức 14/9 (som_listener.py): người nghe chỉ thấy ảnh đã vẽ số + câu, không mục tiêu, không lịch
sử; tham lam 8 token; lấy số nguyên đầu tiên. Câu rỗng hoặc màn không có ô: không gọi mô hình.
Ghi dần + nối tiếp được (bỏ id đã có). Thiếu ảnh ⇒ dừng TRƯỚC khi nạp mô hình.
"""
import argparse, glob, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["phi4", "gia"], required=True)
    ap.add_argument("--som", required=True)
    ap.add_argument("--cau", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--img-glob", default="/kaggle/input/**/images/*.png")
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    som = {(o["tap"], o["episode_id"], o["step_id"]): o for o in map(json.loads, open(a.som, encoding="utf-8"))}
    cau = [json.loads(l) for l in open(a.cau, encoding="utf-8")]
    assert len(som) == 879 and len(cau) == 2530, (len(som), len(cau))

    anh = {}
    for p in glob.glob(a.img_glob, recursive=True):
        anh.setdefault(os.path.basename(p), p)
    thieu = sorted({os.path.basename(o["image_goc"]) for o in som.values()} - anh.keys())
    print(f"[ảnh] {len(anh)} tệp trong {a.img_glob} · thiếu {len(thieu)} / {len(som)} màn", flush=True)
    assert not thieu, f"DỪNG: thiếu ảnh, ví dụ {thieu[:5]}"

    si, sn = map(int, a.shard.split("/"))
    viec = [c for c in cau if c["id"] % sn == si]
    if a.limit:
        viec = viec[:a.limit]
    xong = set()
    if os.path.exists(a.out):
        for l in open(a.out, encoding="utf-8"):
            try:
                xong.add(json.loads(l)["id"])
            except (json.JSONDecodeError, KeyError):
                pass
    con = [c for c in viec if c["id"] not in xong]
    print(f"[cấu hình] g0-288 · backend={a.backend} · shard={a.shard} · việc {len(viec)} · đã xong {len(viec) - len(con)}"
          f" · crops={os.environ.get('SOM_PHI4_CROPS', 'mặc định')} · ra={a.out}", flush=True)
    if not con:
        print("đã xong hết", flush=True); return

    import som_listener as SL
    from som_build import ve
    from PIL import Image
    mo = {"phi4": SL.Phi4, "gia": SL.Gia}[a.backend]()
    print(f"[mô hình] {mo.ten}", flush=True)
    t0, n, n_oom = time.time(), 0, 0
    with open(a.out, "a", encoding="utf-8") as f:
        for c in con:
            r = som[(c["tap"], c["episode_id"], c["step_id"])]
            s = c["sent"]
            if not s or not r["boxes"]:
                raw, chon = "", None
            else:
                img = ve(Image.open(anh[os.path.basename(r["image_goc"])]), r["boxes"])
                try:
                    raw = mo.hoi(img, SL.CAU_HOI.format(s=s))
                except Exception as e:
                    if "out of memory" not in str(e).lower():
                        raise
                    import torch; torch.cuda.empty_cache()
                    raw, n_oom = "__OOM__", n_oom + 1
                    print(f"  ⚠️ OOM id {c['id']} (n_o={len(r['boxes'])}) · tổng {n_oom}", flush=True)
                m = re.search(r"\d+", raw) if raw != "__OOM__" else None
                chon = int(m.group()) if m else None
            h = int(chon is not None and chon in r["dap_an"])
            f.write(json.dumps({"id": c["id"], "tap": c["tap"], "episode_id": c["episode_id"], "step_id": c["step_id"],
                                "nhan": c["nhan"], "sent": s, "raw": raw, "chon": chon, "h": h,
                                "n_o": len(r["boxes"])}, ensure_ascii=False) + "\n")
            f.flush(); n += 1
            if n % 50 == 0:
                dt = (time.time() - t0) / n
                print(f"  {n}/{len(con)} · {dt:.2f} s/câu · còn ~{dt * (len(con) - n) / 60:.0f} phút · OOM {n_oom}", flush=True)
    print(f"xong {n} câu mới → {a.out} · OOM {n_oom}", flush=True)


if __name__ == "__main__":
    main()
