# -*- coding: utf-8 -*-
"""
Dựng lại các gói chuyển-máy. Chạy vài giây, nên KHÔNG commit gói vào git.

Vì sao có file này: bốn gói zip từng nằm ở thư mục gốc và **được git theo dõi**. Hai
trong số đó nặng 110 MB, và mỗi lần dựng lại là một blob mới nằm vĩnh viễn trong lịch sử —
thư mục `.git` phình lên 370 MB cho thứ tái tạo được trong vài giây. Nay gói bị bỏ khỏi
git; cần thì dựng lại bằng đây.

  python harness/make_bundle.py rented   # mã + cấu hình + tập kiểm (OCR, nhãn) — 3,3 MB
  python harness/make_bundle.py gate     # + 300 ảnh của mẫu cổng A            — 111 MB
  python harness/make_bundle.py infer    # + 300 ảnh, test.jsonl chỉ 300 bản ghi — 110 MB
  python harness/make_bundle.py score    # + đủ 4.463 ảnh bước chạm để CHẤM     — ~1,7 GB
  python harness/make_bundle.py pata_kaggle  # PATA: unit test thật + smoke trên Kaggle T4
  python harness/make_bundle.py pata_colab   # PATA: train S/H/J trên Colab (ảnh lấy từ Drive)
"""
import os, sys, json, random, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEST = os.path.join(HERE, "dg1_cache", "test_ac")
SEED = 20260805          # khoá ở report/106 mục 10
REPORTS = ("106_DANG_KY_TRUOC", "108_DA_LAM_DUOC_GI", "109_BAN_DO_HIEN_TAI",
           "117_QUYET_DINH_MIN_DESC")


def load_test():
    return [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")]


def gate_sample(n=300):
    """Đúng mẫu mà `score_run.py --mode gate --n 300` lấy ra — cùng bộ lọc, cùng hạt giống."""
    taps = [r for r in load_test()
            if r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]]
    random.Random(SEED).shuffle(taps)
    return taps[:n]


def add_code(z):
    for f in sorted(os.listdir(HERE)):
        if f.endswith((".py", ".sh", ".yaml", ".md")):
            z.write(os.path.join(HERE, f), f"thesis/harness/{f}")
    for r in REPORTS:
        z.write(os.path.join(ROOT, "report", f"{r}.md"), f"thesis/report/{r}.md")


def add_test_meta(z, recs=None):
    if recs is None:
        z.write(os.path.join(TEST, "test.jsonl"), "thesis/harness/dg1_cache/test_ac/test.jsonl")
    else:
        z.writestr("thesis/harness/dg1_cache/test_ac/test.jsonl",
                   "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs))
    keep = None if recs is None else {r["image"] for r in recs}
    for name in ("ocr.jsonl", "descriptors.jsonl"):
        p = os.path.join(TEST, name)
        if not os.path.exists(p):
            continue
        if keep is None:
            z.write(p, f"thesis/harness/dg1_cache/test_ac/{name}")
        else:
            z.writestr(f"thesis/harness/dg1_cache/test_ac/{name}",
                       "".join(l for l in open(p, encoding="utf-8")
                               if json.loads(l).get("image") in keep
                               or f"images/ep{json.loads(l).get('episode_id')}_s"
                                  f"{json.loads(l).get('step_id')}.png" in keep))


def add_images(z, recs):
    for r in recs:
        z.write(os.path.join(TEST, r["image"]), f"thesis/harness/dg1_cache/test_ac/{r['image']}")


TRAIN = os.path.join(HERE, "dg1_cache", "train_ac")


def build_pata(kind):
    """PATA (report/185). Hai gói:
      pata_kaggle  mã + pata/*.jsonl + ảnh probe40 + 400 ảnh dạy (smoke) + OCR của đúng các ảnh đó
                   → Kaggle T4: 13 unit test --real + smoke vài chục update. ~200 MB.
      pata_colab   mã + pata/*.jsonl + ocr.jsonl ĐỦ của tập dạy, KHÔNG ảnh (ảnh lấy từ
                   train_images_p*.tar trên Drive) → Colab: train S/H/J.
    """
    out = os.path.join(ROOT, "_bundles", f"thesis_{kind}.zip")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    z = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    add_code(z)
    z.write(os.path.join(ROOT, "report", "185_CHOT_PHUONG_PHAP_ACTION_PATA_CAUSAL_22_9.md"),
            "thesis/report/185_CHOT_PHUONG_PHAP_ACTION_PATA_CAUSAL_22_9.md")
    pd = os.path.join(TRAIN, "pata")
    for f in sorted(os.listdir(pd)):
        if f.endswith((".jsonl", ".json")):
            z.write(os.path.join(pd, f), f"thesis/harness/dg1_cache/train_ac/pata/{f}")
    if kind == "pata_colab":
        z.write(os.path.join(TRAIN, "ocr.jsonl"), "thesis/harness/dg1_cache/train_ac/ocr.jsonl")
    else:
        L = lambda f: [json.loads(l) for l in open(os.path.join(pd, f), encoding="utf-8")]
        imgs = [r["image"] for r in L("probe40.jsonl")]
        tr = [r for r in L("train_proper.jsonl") if os.path.exists(os.path.join(TRAIN, r["image"]))]
        random.Random(20260923).shuffle(tr)
        imgs += [r["image"] for r in tr[:400]]
        keep = set(imgs)
        z.writestr("thesis/harness/dg1_cache/train_ac/ocr.jsonl",
                   "".join(l for l in open(os.path.join(TRAIN, "ocr.jsonl"), encoding="utf-8")
                           if json.loads(l)["image"] in keep))
        for im in sorted(keep):
            z.write(os.path.join(TRAIN, im), f"thesis/harness/dg1_cache/train_ac/{im}")
    z.close()
    print(f"{out}\n  {len(zipfile.ZipFile(out).namelist())} tệp · {os.path.getsize(out)/1e6:.1f} MB")


def build(kind):
    if kind.startswith("pata_"):
        return build_pata(kind)
    out = os.path.join(ROOT, f"thesis_{kind}.zip")
    z = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    add_code(z)
    if kind == "rented":
        add_test_meta(z)
    elif kind == "gate":
        add_test_meta(z); add_images(z, gate_sample())
    elif kind == "infer":
        sel = gate_sample()
        add_test_meta(z, sel); add_images(z, sel)
    elif kind == "score":
        taps = [r for r in load_test()
                if r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]]
        add_test_meta(z); add_images(z, taps)
    else:
        sys.exit("kind phải là: rented | gate | infer | score")
    z.close()
    print(f"{out}\n  {len(zipfile.ZipFile(out).namelist())} tệp · {os.path.getsize(out)/1e6:.1f} MB")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "rented")
