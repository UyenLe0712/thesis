# -*- coding: utf-8 -*-
"""288 G0 — bước 1 (CPU, máy nhà, 0 GPU, KHÔNG mạng): dựng ô SoM + danh sách câu cho người nghe Phi-4.

    ~/.venvs/thesis/bin/python _scripts/288/g0_som_build.py [--zip <all_forest_dict.zip>]

Viết lại 6/10/2026 từ bản mô tả B.3 (mã gốc ở máy Mac) ⇒ md5 mã khác bản gốc; md5 hai tệp RA phải
trùng số khoá ở Phụ lục A (g0_som.jsonl a49789bd…, g0_cau.jsonl 656dd46f…) — script tự so và báo.

Ứng viên/đáp án theo ĐÚNG luật khoá 14/9 của harness/som_build.py (hàm ung_vien), chỉ đổi tập bước:
  · c1   : 249 bước click val C1 (đã có 9 câu S1 chấm UGround) → câu chuẩn + 9 câu mẫu
  · train: 630 bước click trong 1.000 câu nhắc ck500 (prompt_keys[:1000]) → chỉ câu chuẩn
Cây trợ năng đọc từ all_forest_dict.zip có sẵn (gán thẳng A._ZIP → không gọi hf_hub_download).
Ra: _scripts/288/g0/g0_som.jsonl (một dòng một màn) · g0_cau.jsonl (một dòng một cặp (màn, câu) KHÁC NHAU, kèm nhãn).
"""
import argparse, glob, hashlib, json, os, statistics, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "harness"))
import a11y_inventory as A
from som_build import ung_vien

MD5_SOM, MD5_CAU = "a49789bda073f5629380ad907db31910", "656dd46f40bcc2d2f32a84e1c752fe6f"
TAPT = ("click", "long_press")


def tim_zip(p):
    if p:
        return p
    c = glob.glob(os.path.expanduser("~/.cache/huggingface/hub/datasets--HarrytheOrange--parsed_AndroidControl/"
                                     "snapshots/*/all_forest_dict.zip")) + glob.glob(os.path.join(REPO, "..", "all_forest_dict.zip"))
    assert c, "DỪNG: thiếu all_forest_dict.zip (HarrytheOrange/parsed_AndroidControl) — tải về rồi chạy lại với --zip"
    return c[0]


def la_cham(r):
    return r["action"].get("action_type") in TAPT and "x" in r["action"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "g0"))
    a = ap.parse_args()
    A._ZIP = zipfile.ZipFile(tim_zip(a.zip))

    C1 = os.path.join(REPO, "runs", "c1", "exec8")
    c1 = [r for r in map(json.loads, open(os.path.join(C1, "c1data", "c1_recs.jsonl"), encoding="utf-8")) if la_cham(r)]
    assert len(c1) == 249, len(c1)
    mau = []
    for k in range(9):
        mau.append({(str(o["episode_id"]), str(o["step_id"])): (o.get("sent") or "")
                    for o in map(json.loads, open(os.path.join(C1, "c1score", f"score_k{k}_raw.jsonl"), encoding="utf-8"))})
    keys = json.load(open(os.path.join(REPO, "runs", "ctg", "p0", "p0_a3", "prompt_keys.json")))[:1000]
    TR = {f"{r['episode_id']}_{r['step_id']}": r for r in map(json.loads, open(
        os.path.join(REPO, "harness", "dg1_cache", "train_ac", "train.jsonl"), encoding="utf-8"))}
    train = [TR[k] for k in keys if la_cham(TR[k])]
    assert len(train) == 630, len(train)

    os.makedirs(a.out, exist_ok=True)
    som, cau, so_o, phu = [], {}, [], {"c1": 0, "train": 0}
    for tap, ds in (("c1", c1), ("train", train)):
        for r in ds:
            ep, st = str(r["episode_id"]), str(r["step_id"])
            W, H = int(r["w"]), int(r["h"])
            bx = ung_vien(f"episode_{ep}_screenshot_{st}.png", W, H)
            gx, gy = float(r["action"]["x"]), float(r["action"]["y"])
            dap = [i for i, b in enumerate(bx, 1) if b[0] <= gx <= b[2] and b[1] <= gy <= b[3]]
            phu[tap] += bool(dap); so_o.append(len(bx))
            som.append({"tap": tap, "episode_id": ep, "step_id": st, "image_goc": r["image"], "w": W, "h": H,
                        "boxes": [list(b) for b in bx], "dap_an": dap})
            ds_cau = [("chuan", r["target_instruction"])]
            if tap == "c1":
                ds_cau += [(f"k{k}", mau[k][(ep, st)]) for k in range(9)]
            for nhan, s in ds_cau:
                kk = (tap, ep, st, s)
                if kk not in cau:
                    cau[kk] = {"tap": tap, "episode_id": ep, "step_id": st, "sent": s, "nhan": []}
                cau[kk]["nhan"].append(nhan)

    p_som, p_cau = os.path.join(a.out, "g0_som.jsonl"), os.path.join(a.out, "g0_cau.jsonl")
    with open(p_som, "w", encoding="utf-8") as f:
        for o in som:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    with open(p_cau, "w", encoding="utf-8") as f:
        for i, o in enumerate(cau.values()):
            f.write(json.dumps({"id": i, **o}, ensure_ascii=False) + "\n")

    s = sorted(so_o)
    print(f"[som] {len(som)} màn (c1 {len(c1)} · train {len(train)}) · ô/màn trung vị {statistics.median(s):.0f}"
          f" · p90 {s[int(.9 * len(s))]} · không ô {sum(x == 0 for x in s)}")
    print(f"[phủ đáp án] c1: {phu['c1']}/{len(c1)} = {phu['c1']/len(c1):.1%}")
    print(f"[phủ đáp án] train: {phu['train']}/{len(train)} = {phu['train']/len(train):.1%}")
    n_c1 = sum(o["tap"] == "c1" for o in cau.values())
    print(f"[câu] {len(cau)} lời gọi người nghe (c1 {n_c1} · train {len(cau) - n_c1}) · câu rỗng "
          f"{sum(not o['sent'] for o in cau.values())} → {a.out}/")
    md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
    for p, h in ((p_som, MD5_SOM), (p_cau, MD5_CAU)):
        print(f"[md5] {os.path.basename(p)} {md5(p)} · bản khoá {h} · {'✅ khớp' if md5(p) == h else '⚠️ KHÁC'}")


if __name__ == "__main__":
    main()
