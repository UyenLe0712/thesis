# -*- coding: utf-8 -*-
"""
PATA · bước A2 + A3 + khoá probe 40 (report/185 §2, §3, §7b, §12A). CHẠY TRÊN CPU, 0 GPU.

Dựng ba tập bước CHẠM (click / long_press) cho PATA:
    train_proper  ← train_tru_val.jsonl      (mọi bước chạm; CE tính trên tất cả)
    val400        ← val_cham400.jsonl        (chẩn đoán loss/localizer thường xuyên)
    val600        ← val_cham600.jsonl        (chỉ dùng cho cổng cuối C1, §8)
Mỗi bản ghi có thêm `box` (khung phần tử proxy lấy từ descriptors.jsonl, toạ độ pixel ảnh
gốc) hoặc `box: null` ⇒ `kl_ok: false` (KL mask = 0, §2 "Luật train đúng").

Phép kiểm cứng (assert, hỏng là dừng):
  · ba tập rời nhau theo episode_id, (episode_id, step_id), ảnh, khoá OCR
  · mọi box hợp lệ: x1<x2, y1<y2, nằm trong ảnh, CHỨA điểm chạm (đúng luật dựng box)
  · số bước chạm Train-proper khớp đếm độc lập từ tệp nguồn
Ghi SHA-256 từng tệp ra `pata/split_hash.json` — mục "SHA-256 Train-proper/val400/val600"
của manifest §11 đọc thẳng từ đây.

Probe 40 (§7b): 40 bước lấy từ val400 CÓ box, hạt giống cố định, ghi SHA-256. Chạy lại
phải ra đúng tệp cũ; nếu tệp đã tồn tại mà hash khác thì DỪNG (không được đổi probe).

Chạy:
    ~/.venvs/thesis/bin/python harness/pata_data.py
"""
import os, sys, json, hashlib, random, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
OUT = os.path.join(ROOT, "pata")
TOUCH = ("click", "long_press")
SEED_PROBE = 20260923
N_PROBE = 40


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(fn):
    return [json.loads(l) for l in open(os.path.join(ROOT, fn), encoding="utf-8")]


def clip_box(b, r):
    """Khung a11y có thể thò ra ngoài màn (đo 23/9: 117/41.099 dòng, toàn bộ tập dạy).
    Cắt vào khung ảnh; phần ngoài màn không có ô thị giác nào nên không đổi đích KL."""
    x1, y1, x2, y2 = b
    return [max(0, x1), max(0, y1), min(r["w"], x2), min(r["h"], y2)]


def box_ok(b, r):
    x1, y1, x2, y2 = b
    x, y = r["action"]["x"], r["action"]["y"]
    return (0 <= x1 < x2 <= r["w"] and 0 <= y1 < y2 <= r["h"]
            and x1 <= x <= x2 and y1 <= y <= y2)


def build(recs, desc, split):
    out, st = [], collections.Counter()
    for r in recs:
        if r["action"]["action_type"] not in TOUCH:
            continue
        st["cham"] += 1
        d = desc.get((r["episode_id"], r["step_id"]))
        box = d["box"] if d else None
        a = r["action"]
        if box is not None and not (0 <= a["x"] <= r["w"] and 0 <= a["y"] <= r["h"]):
            # đo 23/9: 9 bước chạm có toạ độ vượt w×h khai báo (x=2163 trên màn 1080 — nhiều
            # khả năng màn ngang). Không biết ảnh thật xoay thế nào ⇒ box không tin được:
            # tắt KL, vẫn giữ CE (đúng luật §2 cho bước không có box).
            st["diem_ngoai_anh"] += 1
            box = None
        if box is not None:
            cb = clip_box(box, r)
            if cb != box:
                st["cat_bien"] += 1
            box = cb
            assert box_ok(box, r), f"box sai luật ở {split} {r['episode_id']},{r['step_id']}: {box}"
            st["co_box"] += 1
        out.append({
            "episode_id": r["episode_id"], "step_id": r["step_id"], "image": r["image"],
            "goal": r["goal"], "history": r.get("history") or [],
            "target_instruction": r["target_instruction"], "action": r["action"],
            "w": r["w"], "h": r["h"], "box": box, "kl_ok": box is not None,
            "area_share": d.get("area_share") if d else None,
            "name_src": d.get("name_src") if d else None,
        })
    return out, st


def dump(rows, fn):
    p = os.path.join(OUT, fn)
    with open(p, "w", encoding="utf-8") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    return p


def main():
    os.makedirs(OUT, exist_ok=True)
    desc = {}
    for l in open(os.path.join(ROOT, "descriptors.jsonl"), encoding="utf-8"):
        d = json.loads(l)
        desc[(d["episode_id"], d["step_id"])] = d
    ocr_keys = {json.loads(l)["image"] for l in open(os.path.join(ROOT, "ocr.jsonl"), encoding="utf-8")}

    src = {"train_proper": "train_tru_val.jsonl", "val400": "val_cham400.jsonl",
           "val600": "val_cham600.jsonl"}
    sets, stats = {}, {}
    for k, fn in src.items():
        recs = load(fn)
        print(f"[dữ liệu] {fn}: {len(recs)} bước", flush=True)
        sets[k], stats[k] = build(recs, desc, k)
        # đếm độc lập, không qua build()
        n_indep = sum(1 for r in recs if r["action"]["action_type"] in TOUCH)
        assert n_indep == len(sets[k]) == stats[k]["cham"]

    # ── rời nhau ────────────────────────────────────────────────────────────────
    names = list(sets)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = sets[names[i]], sets[names[j]]
            for key, f in (("episode_id", lambda r: r["episode_id"]),
                           ("(episode_id, step_id)", lambda r: (r["episode_id"], r["step_id"])),
                           ("ảnh / khoá OCR", lambda r: r["image"])):
                chung = {f(r) for r in a} & {f(r) for r in b}
                assert not chung, f"TRÙNG {key} giữa {names[i]} và {names[j]}: {list(chung)[:5]}"
    # rời nhau ở mức EPISODE cả với bước không chạm của tập kia (val lấy nguyên episode)
    ep_all = {k: {r["episode_id"] for r in load(fn)} for k, fn in src.items()}
    assert not (ep_all["train_proper"] & ep_all["val400"])
    assert not (ep_all["train_proper"] & ep_all["val600"])
    assert not (ep_all["val400"] & ep_all["val600"])
    thieu_ocr = sum(1 for k in sets for r in sets[k] if r["image"] not in ocr_keys)

    paths = {k: dump(v, f"{k}.jsonl") for k, v in sets.items()}

    # ── probe 40 ───────────────────────────────────────────────────────────────
    pool = sorted((r for r in sets["val400"] if r["kl_ok"]),
                  key=lambda r: (r["episode_id"], r["step_id"]))
    probe = random.Random(SEED_PROBE).sample(pool, N_PROBE)
    probe.sort(key=lambda r: (r["episode_id"], r["step_id"]))
    pp = os.path.join(OUT, "probe40.jsonl")
    old = sha256(pp) if os.path.exists(pp) else None
    tmp = dump(probe, "probe40.tmp.jsonl")
    new = sha256(tmp)
    if old is not None and old != new:
        os.remove(tmp)
        sys.exit(f"⛔ probe40.jsonl đã khoá với hash {old[:12]}…, bản dựng lại ra {new[:12]}…. "
                 f"Không được đổi probe (report/185 §7b).")
    os.replace(tmp, pp)

    hashes = {os.path.basename(p): sha256(p) for p in list(paths.values()) + [pp]}
    hashes["_nguon"] = {fn: sha256(os.path.join(ROOT, fn)) for fn in
                        list(src.values()) + ["descriptors.jsonl", "ocr.jsonl"]}
    json.dump(hashes, open(os.path.join(OUT, "split_hash.json"), "w"), indent=1)

    print("=" * 72)
    for k in sets:
        s = stats[k]
        print(f"  {k:13} chạm {s['cham']:6}  có box {s['co_box']:6}  "
              f"thiếu box {s['cham'] - s['co_box']:4}  ({s['co_box'] / s['cham']:.2%})  "
              f"cắt biên {s['cat_bien']}  điểm ngoài ảnh {s['diem_ngoai_anh']}")
    print(f"  probe40      40 bước từ val400 có box, hạt {SEED_PROBE}")
    print(f"  thiếu OCR    {thieu_ocr} bước (prompt vẫn dựng được, chỉ thiếu dòng chữ)")
    print(f"  rời nhau     episode · (episode,step) · ảnh/OCR : ĐẠT")
    print("-" * 72)
    for k, v in hashes.items():
        if k != "_nguon":
            print(f"  {k:22} {v[:16]}…")
    print(f"→ {OUT}/")


if __name__ == "__main__":
    main()
