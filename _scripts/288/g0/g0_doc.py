# -*- coding: utf-8 -*-
"""288 G0 — bước 3 (CPU, máy nhà): đọc cổng G0 từ kết quả người nghe Phi-4.

    ~/.venvs/thesis/bin/python _scripts/288/g0/g0_doc.py --nghe <tải_về>/g0_phi4.jsonl
    ~/.venvs/thesis/bin/python _scripts/288/g0/g0_doc.py --gia-lap 0.8,0.3,0.55      # tự kiểm, người nghe giả

Viết lại 6/10/2026 từ bản mô tả B.5 (mã gốc ở máy Mac) ⇒ md5 khác bản gốc (223a4510…).
Luật nguyên văn ở §7.1; bản 4 chỉ dùng G0a, G0b (chặn người nghe) và V4 (chặn tnghev) — §00.4.
Ghi _scripts/288/g0_ket_qua.json (giả lập: g0_ket_qua_GIA.json).
"""
import argparse, json, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "_scripts"))
from doc_286 import cluster_ci

PARSE_FAIL, PHU_TRAIN, KAPPA_MAX, AUC_MIN = 0.05, 0.90, 0.60, 0.65
V2, V3, V4, G0D = 1.0, 0.25, (0.30, 0.85), 3.3
B, HAT_BOOT, HAT_RAND, N_RAND = 10000, 101, 288, 200
O_SP_KHOA = 68.67


def dang_ok(s):
    w = (s or "").split()
    return 3 <= len(w) <= 20 and not re.search(r"\d+\s*[,;]\s*\d+", s) and not re.search(r"\d{3,}", s)


def kappa(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    po = float((x == y).mean())
    pe = x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean())
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def oracle(key, ex):
    """key, ex: mảng (249, 9). Chọn k có (key, −k) lớn nhất → exec của câu được chọn (%), và vector exec."""
    chon = [max(range(key.shape[1]), key=lambda k: (key[j, k], -k)) for j in range(key.shape[0])]
    e = np.array([ex[j, k] for j, k in enumerate(chon)], float)
    return 100 * e.mean(), e


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--nghe")
    g.add_argument("--gia-lap", help="TPR,FPR,P(v)")
    a = ap.parse_args()

    C1 = os.path.join(REPO, "runs", "c1", "exec8")
    recs = [json.loads(l) for l in open(os.path.join(C1, "c1data", "c1_recs.jsonl"), encoding="utf-8")]
    I = [i for i, r in enumerate(recs) if r["action"].get("action_type") in ("click", "long_press") and "x" in r["action"]]
    assert len(recs) == 400 and len(I) == 249
    M = json.load(open(os.path.join(C1, "metric_tung_cau.json")))
    J = len(I)
    ex = np.zeros((J, 9)); SP = np.zeros((J, 9)); sent = [[""] * 9 for _ in range(J)]
    ep = [recs[i]["episode_id"] for i in I]
    for k in range(9):
        R = {(o["episode_id"], o["step_id"]): o for o in
             map(json.loads, open(os.path.join(C1, "c1score", f"score_k{k}_raw.jsonl"), encoding="utf-8"))}
        for j, i in enumerate(I):
            o = R[(recs[i]["episode_id"], recs[i]["step_id"])]
            ex[j, k] = int(o.get("executable") or 0)
            SP[j, k] = M["spice"][k][i]
            sent[j][k] = o.get("sent") or ""
    som = [json.loads(l) for l in open(os.path.join(HERE, "g0_som.jsonl"), encoding="utf-8")]
    cau = [json.loads(l) for l in open(os.path.join(HERE, "g0_cau.jsonl"), encoding="utf-8")]
    SOM = {(o["tap"], o["episode_id"], o["step_id"]): o for o in som}

    gia = bool(a.gia_lap)
    if gia:
        tpr, fpr, pv = map(float, a.gia_lap.split(","))
        print(f"⚠️ GIẢ LẬP người nghe: TPR {tpr} · FPR {fpr} · P(v) {pv} — số dưới đây KHÔNG phải kết quả", flush=True)
        rng = np.random.default_rng(7)
        exs = {(str(recs[i]["episode_id"]), str(recs[i]["step_id"]), sent[j][k]): ex[j, k]
               for j, i in enumerate(I) for k in range(9)}
        KQ = {}
        for c in cau:
            if c["nhan"] == ["chuan"] or c["tap"] == "train":
                p = pv
            else:
                p = tpr if exs[(c["episode_id"], c["step_id"], c["sent"])] == 1 else fpr
            h = rng.random() < p
            pf = rng.random() < 0.02
            KQ[c["id"]] = {**c, "chon": None if pf else 1, "h": 0 if pf else int(h)}
    else:
        KQ = {}
        for l in open(a.nghe, encoding="utf-8"):
            try:
                o = json.loads(l)
            except json.JSONDecodeError:
                continue
            KQ[o["id"]] = o
    assert set(KQ) == {c["id"] for c in cau}, f"DỪNG: kết quả có {len(KQ)} id, cần đủ 2.530 id của g0_cau"
    H = {(o["tap"], str(o["episode_id"]), str(o["step_id"]), o["sent"]): o for o in KQ.values()}

    # G0a
    co_o = [o for o in KQ.values() if o["sent"] and SOM[(o["tap"], str(o["episode_id"]), str(o["step_id"]))]["boxes"]]
    parse_fail = float(np.mean([o["chon"] is None for o in co_o]))
    tr = [o for o in som if o["tap"] == "train"]
    phu_train = float(np.mean([bool(o["dap_an"]) for o in tr]))
    G0a = parse_fail <= PARSE_FAIL and phu_train >= PHU_TRAIN

    # h, v
    key_of = lambda j: (str(recs[I[j]]["episode_id"]), str(recs[I[j]]["step_id"]))
    h_tho = np.array([[H[("c1", *key_of(j), sent[j][k])]["h"] for k in range(9)] for j in range(J)], float)
    ok = np.array([[dang_ok(sent[j][k]) for k in range(9)] for j in range(J)], float)
    h = h_tho * ok
    v = np.array([H[("c1", *key_of(j), recs[I[j]]["target_instruction"])]["h"] for j in range(J)], float)
    TR = {(o["episode_id"], o["step_id"]): o for o in tr}
    v_train = [H[("train", e, s, c["sent"])]["h"] for c in cau if c["tap"] == "train" for e, s in [(c["episode_id"], c["step_id"])]]
    assert len(v_train) == 630 and len(TR) == 630

    # cặp duy nhất
    U, lech = [], 0
    for j in range(J):
        dau = {}
        for k in range(9):
            s = sent[j][k]
            if s in dau:
                lech += int(ex[j, k] != ex[j, dau[s]])
                continue
            dau[s] = k; U.append((j, k))
    hu = np.array([h[j, k] for j, k in U]); eu = np.array([ex[j, k] for j, k in U])
    kap = kappa(hu, eu)
    G0b = kap <= KAPPA_MAX

    # G0c — AUC trong từng bước
    tong, cap, tron = 0.0, 0, 0
    for j in range(J):
        duong = [h[jj, k] for jj, k in U if jj == j and ex[jj, k] == 1]
        am = [h[jj, k] for jj, k in U if jj == j and ex[jj, k] == 0]
        if duong and am:
            tron += 1
            for x in duong:
                for y in am:
                    tong += 1.0 if x > y else 0.5 if x == y else 0.0
                    cap += 1
    auc = tong / cap if cap else float("nan")
    G0c = cap > 0 and auc >= AUC_MIN

    # oracle
    O_SP, e_SP = oracle(SP, ex)
    assert abs(O_SP - O_SP_KHOA) < 0.01, f"DỪNG: O_SP = {O_SP:.2f} khác {O_SP_KHOA} — dữ liệu C1 lệch"
    O_h, e_h = oracle(10 * h + SP, ex)
    O_vh, e_vh = oracle(10 * v[:, None] * h + SP, ex)
    rr = np.random.default_rng(HAT_RAND)
    O_rand = []
    for _ in range(N_RAND):
        mask = (rr.random(J) < v.mean()).astype(float)
        O_rand.append(oracle(10 * mask[:, None] * h + SP, ex)[0])
    O_rand = float(np.mean(O_rand))

    vu = np.array([v[j] for j, k in U])
    tpr_ = lambda m: float(hu[(eu == 1) & m].mean()) if ((eu == 1) & m).any() else float("nan")
    V3v = tpr_(vu == 1) - tpr_(vu == 0)
    dk = {"V1": O_vh - O_h >= 0, "V2": O_vh - O_rand >= V2, "V3": V3v >= V3,
          "V4": V4[0] <= float(np.mean(v_train)) <= V4[1]}
    keep_v = all(dk.values())
    main_ = "vh" if keep_v else "h"
    O_main, e_main = (O_vh, e_vh) if keep_v else (O_h, e_h)
    d, lo, hi = cluster_ci(e_main - e_SP, ep, np.random.default_rng(HAT_BOOT))
    G0d = (O_main - O_SP) >= G0D and lo > 0
    TRAIN = G0a and G0b and G0c and G0d

    D = lambda b: "ĐẠT" if b else "KHÔNG ĐẠT"
    print(f"[dữ liệu] C1 {J} bước · {len(U)} cặp duy nhất (bước, câu) · exec lệch trong cùng câu {lech}")
    print(f"G0a  parse_fail {parse_fail:.4f} (≤ {PARSE_FAIL}) · phủ SoM train {phu_train:.4f} (≥ {PHU_TRAIN}) → {D(G0a)}")
    print(f"G0b  κ(h, exec_UG) {kap:.3f} (≤ {KAPPA_MAX}) → {D(G0b)}")
    print(f"G0c  AUC trong nhóm {auc:.3f} trên {tron} bước exec trộn (≥ {AUC_MIN}) → {D(G0c)}   [bản 4: chỉ ghi]")
    print(f"oracle  O_SP {O_SP:.2f} · O_h {O_h:.2f} · O_vh {O_vh:.2f} · O_rand {O_rand:.2f} (TB {N_RAND} lần)")
    print(f"V1  O_vh − O_h {O_vh - O_h:+.2f} (≥ 0) → {D(dk['V1'])}      [bản 4: chỉ ghi]")
    print(f"V2  O_vh − O_rand {O_vh - O_rand:+.2f} (≥ {V2}) → {D(dk['V2'])}      [bản 4: chỉ ghi]")
    print(f"V3  TPR(v=1) − TPR(v=0) {V3v:+.3f} (≥ {V3}) → {D(dk['V3'])}      [bản 4: chỉ ghi]")
    print(f"V4  TB v train {np.mean(v_train):.3f} (∈ {V4}) · TB v val {v.mean():.3f} → {D(dk['V4'])}      [bản 4: chặn riêng tnghev]")
    print(f"keep_v {keep_v} ⇒ nhánh chính '{main_}'")
    print(f"G0d  O_main − O_SP {O_main - O_SP:+.2f} (≥ {G0D}) · KTC95 [{lo:+.2f}; {hi:+.2f}] → {D(G0d)}   [bản 4: chỉ ghi]")
    if TRAIN:
        print(f"⇒ TRAIN = True (luật cách A) · nhánh chính {'nghe_v' if keep_v else 'nghe'}")
    else:
        print("⇒ TRAIN = False (luật cách A) — cấm đổi người nghe, hạ ngưỡng, đổi W hay dang_ok rồi đo lại")
    arms, arms_m = [("spicea", 101)], []
    if G0a and G0b:
        arms = [("spicea", 101)] + ([("nghev", 101)] if dk["V4"] else []) + [("nghe", 101)]
        arms_m = ([("nghevm", 101)] if dk["V4"] else []) + [("nghem", 101)]      # liều mạnh W = 2 (quyết định 6/10)
    print(f"⇒ BẢN 4 (§00.4): phiên A  ARMS_TRAIN = {arms}")
    print(f"⇒ BẢN 4 (6/10):  phiên B  ARMS_TRAIN = {arms_m if arms_m else '(không — G0 chặn người nghe)'}")

    out = os.path.join(HERE, "..", "g0_ket_qua_GIA.json" if gia else "g0_ket_qua.json")
    json.dump({"gia_lap": gia, "n_cap": len(U), "parse_fail": parse_fail, "phu_train": phu_train, "kappa": kap,
               "auc": auc, "n_tron": tron, "O_SP": O_SP, "O_h": O_h, "O_vh": O_vh, "O_rand": O_rand, "V3": V3v,
               "v_val": float(v.mean()), "v_train": float(np.mean(v_train)), "keep_v": keep_v, "main": main_,
               "G0d": {"d": d, "lo": lo, "hi": hi}, "G0": {"a": G0a, "b": G0b, "c": G0c, "d": G0d},
               "V": dk, "TRAIN": TRAIN, "ARMS_TRAIN_ban4": arms, "ARMS_TRAIN_phien_B": arms_m},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=bool)
    print("ghi", os.path.abspath(out))


if __name__ == "__main__":
    main()
