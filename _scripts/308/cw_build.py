# -*- coding: utf-8 -*-
"""308 - dựng dữ liệu CW-RA (chép hay viết, có truy hồi) từ p1_train_rows (CPU, ~10-20 phút).

Mỗi hàng: câu nhắc S1 + khối k = 4 câu mẫu dựng ĐÚNG như lúc chấm (`Kho.cho_test`, bỏ chính tác vụ).
Đích:
  "[COPY i]"              nếu câu mẫu thứ i trùng nguyên văn câu chuẩn (sau tách từ) - i nhỏ nhất
  "[WRITE] " + câu ck500  còn lại; câu ck500 là câu greedy của chính ck500 trên câu nhắc KHÔNG khối (tự chưng cất)
Ra --out/train_cw.jsonl (key, image, body, gold) - đưa thẳng vào ra_train.py, không sửa gì ở ra_train.py.

  python cw_build.py --bundle B --kho train_tru_val.jsonl --ck500-train pred_ck500_train.jsonl --out O
  python cw_build.py --tu-kiem                 # kiểm logic trên dữ liệu giả, không cần gói
"""
import os, sys, json, random, argparse, collections, time

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)

import ra_exemplars as RA
from build_branch_data import prompt_body

TAG_W = "[WRITE]"
tag_c = lambda i: f"[COPY {i}]"


def doc(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def ocr_toks(o):
    return {w for it in (o or {"items": []})["items"][:24] for w in RA.tok(it.get("text", ""))}


def nhan(gold, exs, ck):
    g = RA.tok(gold)
    for i, e in enumerate(exs, 1):
        if RA.tok(e["sent"]) == g:
            return tag_c(i), "copy"
    if not (ck or "").strip():
        return None, "ck500_rong"
    return f"{TAG_W} {ck.strip()}", "write"


def dung(rows, kho, ocr, CK, img_of, kiem_anh=True):
    out, st = [], collections.Counter()
    for r in rows:
        gold = (r.get("target_instruction") or "").strip()
        k = (r["episode_id"], r["step_id"])
        if not gold:
            st["bo_rong"] += 1
            continue
        if k not in CK:
            st["bo_thieu_ck500"] += 1
            continue
        img = img_of(r)
        if kiem_anh and not os.path.exists(img):
            st["bo_thieu_anh"] += 1
            continue
        x = dict(goal=r["goal"], history=r.get("history") or [])
        exs = kho.cho_test(x, 4, ocr_toks(ocr.get(r["image"])), own=r["episode_id"])
        body = prompt_body(x, ocr.get(r["image"]))
        body = RA.chen(body, exs) if exs else body
        lab, loai = nhan(gold, exs, CK[k])
        if lab is None:
            st["bo_" + loai] += 1
            continue
        st[loai] += 1
        st["ck500_dung_trong_write"] += loai == "write" and RA.tok(CK[k]) == RA.tok(gold)
        out.append(dict(key=f"{k[0]}_{k[1]}", image=img, body=body, gold=lab))
    return out, st


def tu_kiem():
    kho_recs = []
    for e in range(40):
        for s in range(4):
            kho_recs.append(dict(episode_id=e, step_id=s, goal=f"open app {e % 5} and buy item {e % 7}",
                                 history=[f"step {s - 1} of {e % 5}"] if s else [], image=f"x{e}_{s}.png",
                                 target_instruction=f"Click on button {e % 5} {s}", action={"action_type": "click"}))
    kho = RA.Kho(kho_recs)
    rows = kho_recs[:30]
    CK = {(r["episode_id"], r["step_id"]): ("" if i == 3 else f"Tap item {i}") for i, r in enumerate(rows)}
    out, st = dung(rows, kho, {}, CK, lambda r: r["image"], kiem_anh=False)
    print("[tự kiểm]", dict(st))
    k3 = f"{rows[3]['episode_id']}_{rows[3]['step_id']}"
    o3 = [o for o in out if o["key"] == k3]
    assert st["copy"] > 0 and st["write"] > 0, st
    assert (o3 and o3[0]["gold"].startswith("[COPY ")) or (not o3 and st["bo_ck500_rong"] == 1), (o3, st)
    for o in out:
        assert o["gold"].startswith("[COPY ") or o["gold"].startswith(TAG_W + " "), o["gold"]
        if o["gold"].startswith("[COPY "):
            i = int(o["gold"][6:-1])
            sent = [l for l in o["body"].split("\n") if l.startswith(f"{i}. ")][0].split("Bước kế: ", 1)[1]
            r = next(x for x in rows if f"{x['episode_id']}_{x['step_id']}" == o["key"])
            assert RA.tok(sent) == RA.tok(r["target_instruction"]), (sent, r["target_instruction"])
        assert o["body"].endswith(RA.LAST)
    print("[tự kiểm] ĐẠT — nhãn COPY trỏ đúng câu mẫu trùng câu chuẩn, nhãn WRITE mang câu ck500")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle")
    ap.add_argument("--kho")
    ap.add_argument("--ck500-train", help="pred greedy của ck500 trên p1_train_rows, câu nhắc không khối (cw_gen.py --mode tu)")
    ap.add_argument("--out")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        return tu_kiem()
    t0 = time.time()
    tr = doc(os.path.join(a.bundle, "p1_train_rows.jsonl"))
    va = doc(os.path.join(a.bundle, "p1_val_rows.jsonl"))
    vep = {r["episode_id"] for r in va}
    ocr = {o["image"]: o for o in doc(os.path.join(a.bundle, "ocr.jsonl"))}
    kho = RA.Kho(doc(a.kho), loai_ep=vep)
    CK = {(d["episode_id"], d["step_id"]): d["pred"] for d in doc(a.ck500_train)}
    tr = [r for r in tr if r["episode_id"] not in vep]
    random.Random(20261010).shuffle(tr)
    out, st = dung(tr, kho, ocr, CK, lambda r: os.path.join(a.bundle, r["image"]))
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "train_cw.jsonl"), "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    S = dict(hang=len(out), copy=st["copy"], write=st["write"], copy_pct=round(100 * st["copy"] / max(1, len(out)), 1),
             ck500_dung_trong_write=st["ck500_dung_trong_write"], bo={k: v for k, v in st.items() if k.startswith("bo_")},
             kho_buoc=len(kho.tr), phut=round((time.time() - t0) / 60, 1))
    json.dump(S, open(os.path.join(a.out, "cw_stats.json"), "w"), ensure_ascii=False, indent=1)
    print("[xong]", json.dumps(S, ensure_ascii=False))
    assert 8 <= S["copy_pct"] <= 25, "⛔ tỉ lệ COPY lệch xa 13-16% đã đo ở val/test - kiểm lại kho hoặc own"


if __name__ == "__main__":
    main()
