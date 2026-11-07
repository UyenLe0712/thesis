# -*- coding: utf-8 -*-
"""H5 (report/323 §8.4): giải thích phải dự đoán được cả chỗ GRPO + SPICE KHÔNG thắng — 0 GPU, CPU + Java (Kaggle CPU).

Giả thuyết: câu chuẩn ở bước không chạm ("Scroll down", "Go back", "Open the X app") có rất ít tuple SPICE,
nên thưởng SPICE ít tín hiệu để giữ đúng loại thao tác ở các bước này; đó là cơ chế khả dĩ cho việc ck500 giảm ở cuộn.
Đo (câu chuẩn và câu đã sinh sẵn, không sinh mới):
  A. Số tuple của câu chuẩn theo loại thao tác vàng (All/Object/Attribute/Relation = tp + fn khi chấm câu chuẩn với chính nó),
     cho AndroidControl test (6.958) và AitZ bước chạm (2.736).
  B. SPICE(câu mô hình, câu chuẩn) của S1/101 và ck500, tách theo {bước chạm, bước không chạm} × {đúng loại, sai loại thao tác}.
     Khoảng cách SPICE giữa câu đúng loại và câu sai loại là độ mạnh tín hiệu thưởng cho loại thao tác.
  C. Tỉ lệ câu chuẩn có 0 tuple Object theo loại thao tác.
"Đúng loại" dùng canon_action(strict_back=True) của metric_exec, như phép kiểm noharm. Số là mô tả, hậu kiểm, một hạt.

  python h5_spice_khong_cham.py --out ../runs/giai_thich/h5_spice_khong_cham.json [--n 200]
"""
import os, sys, json, argparse, collections, statistics as st, ast, time

H = os.path.dirname(os.path.abspath(__file__))
K = os.path.join(H, "..")
sys.path.insert(0, H)
import metric_exec as M  # noqa: E402

TAPT = ("click", "long_press")
CAT = ("All", "Object", "Attribute", "Relation")


def act(r):
    a = r.get("action")
    return ast.literal_eval(a) if isinstance(a, str) else (a or {})


def spice_tung_cau(hyp, ref):
    """Trả list dict {cat: {f, tp, fn, ...}} theo đúng thứ tự đầu vào. Tách từ bằng PTBTokenizer như text_metrics_coco."""
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    from pycocoevalcap.spice.spice import Spice
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
    c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
    t0 = time.time()
    _, S = Spice().compute_score(g, c)
    print(f"  [spice] {len(hyp)} câu · {time.time() - t0:.0f} s", flush=True)
    assert len(S) == len(hyp)
    return S


def n_tuple(s, cat):
    x = s.get(cat, {})
    tp, fn = x.get("tp"), x.get("fn")
    return None if tp is None or fn is None or tp != tp or fn != fn else tp + fn


def tb(x):
    x = [v for v in x if v is not None and v == v]
    return (round(st.mean(x), 4), len(x)) if x else (None, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=0, help="chỉ N bước đầu mỗi kho (chạy thử)")
    a = ap.parse_args()
    out = {}

    # ---------- AndroidControl ----------
    R = [json.loads(l) for l in open(f"{K}/harness/dg1_cache/test_ac/test.jsonl", encoding="utf-8")]
    assert len(R) == 6958
    key = lambda r: (str(r["episode_id"]), str(r["step_id"]))
    loai = {key(r): act(r).get("action_type", "?") for r in R}
    cham = {key(r): act(r).get("action_type") in TAPT and "x" in act(r) for r in R}
    assert sum(cham.values()) == 4463
    gold = {key(r): (r.get("gold_instruction") or "").strip() for r in R}
    S1 = {(str(d["episode_id"]), str(d["step_id"])): d.get("pred") or "" for d in map(json.loads, open(f"{K}/runs/preds_s1_seed101.jsonl", encoding="utf-8"))}
    assert len(S1) == 6958, len(S1)
    CK = {(str(d["episode_id"]), str(d["step_id"])): d.get("sent") or "" for d in map(json.loads, open(f"{K}/runs/grpo_spice/score_ck500_test_raw.jsonl", encoding="utf-8"))}
    CK.update({(str(d["episode_id"]), str(d["step_id"])): d.get("pred") or "" for d in map(json.loads, open(f"{K}/runs/grpo_spice/pred_ck500_test_nontap.jsonl", encoding="utf-8"))})
    ks = [key(r) for r in R if key(r) in CK]
    print(f"[AC] {len(R)} bước · ck500 phủ {len(ks)} · S1 phủ {sum(k in S1 for k in ks)}", flush=True)
    assert len(ks) == 6958, "ck500 thiếu bước (cần 4.463 chạm + 2.495 không chạm)"
    if a.n:
        ks = ks[:a.n]

    G = [gold[k] for k in ks]
    print("A. câu chuẩn với chính nó", flush=True)
    SG = spice_tung_cau(G, G)
    print("   khoá điểm SPICE mẫu:", sorted(SG[0].get("All", {}).keys()), flush=True)
    A = collections.defaultdict(lambda: collections.defaultdict(list))
    for k, s in zip(ks, SG):
        for c in CAT:
            A[loai[k]][c].append(n_tuple(s, c))
    out["A_so_tuple_cau_chuan_ac"] = {l: {c: tb(v) for c, v in d.items()} for l, d in sorted(A.items(), key=lambda x: -len(x[1]["All"]))}
    out["C_ti_le_0_object_ac"] = {l: round(sum(1 for v in d["Object"] if v == 0) / max(1, len(d["Object"])), 4) for l, d in A.items()}
    print(json.dumps(out["A_so_tuple_cau_chuan_ac"], ensure_ascii=False), flush=True)
    print(json.dumps(out["C_ti_le_0_object_ac"], ensure_ascii=False), flush=True)

    print("B. câu mô hình với câu chuẩn", flush=True)
    B = {}
    for ten, P in (("s1_101", S1), ("ck500", CK)):
        H_ = [P[k] for k in ks]
        SP = spice_tung_cau(H_, G)
        nh = collections.defaultdict(lambda: collections.defaultdict(list))
        for k, h, s in zip(ks, H_, SP):
            ok = int(bool(h) and M.canon_action(h, strict_back=True) == M.canon_action(gold[k], strict_back=True))
            nhom = ("cham" if cham[k] else "khong_cham") + ("_dung_loai" if ok else "_sai_loai")
            for c in ("All", "Object"):
                nh[nhom][c].append(s.get(c, {}).get("f"))
            nh[("cham" if cham[k] else "khong_cham") + "_tong"]["All"].append(s.get("All", {}).get("f"))
            nh["khong_cham_" + loai[k] if not cham[k] else "cham"]["dung_loai"].append(ok)
        B[ten] = {g: {c: tb(v) for c, v in d.items()} for g, d in sorted(nh.items())}
        for vung in ("cham", "khong_cham"):
            d, s_ = B[ten].get(f"{vung}_dung_loai", {}).get("All", (None, 0)), B[ten].get(f"{vung}_sai_loai", {}).get("All", (None, 0))
            if d[0] is not None and s_[0] is not None:
                B[ten][f"{vung}_khoang_cach_spice_dung_tru_sai"] = round(d[0] - s_[0], 4)
        print(ten, json.dumps(B[ten], ensure_ascii=False), flush=True)
    out["B_spice_theo_loai_ac"] = B

    # ---------- AitZ (chỉ bước chạm có câu chuẩn, 2.736 bước) ----------
    p = f"{K}/runs/aitz/build_v3_25_10/out/test.jsonl"
    Z = [json.loads(l) for l in open(p, encoding="utf-8")]
    Zg = [(r.get("gold_instruction") or "").strip() for r in Z if act(r).get("action_type") == "click"]
    if a.n:
        Zg = Zg[:a.n]
    print(f"[AitZ] {len(Z)} bước · chạm {len(Zg)}", flush=True)
    SZ = spice_tung_cau(Zg, Zg)
    out["A_so_tuple_cau_chuan_aitz_cham"] = {c: tb([n_tuple(s, c) for s in SZ]) for c in CAT}
    out["A_so_tuple_cau_chuan_ac_cham"] = {c: tb([n_tuple(s, c) for k, s in zip(ks, SG) if cham[k]]) for c in CAT}
    print(json.dumps({k: out[k] for k in ("A_so_tuple_cau_chuan_aitz_cham", "A_so_tuple_cau_chuan_ac_cham")}, ensure_ascii=False), flush=True)
    out["n_chay_thu"] = a.n
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    print("[xong] ghi", a.out, flush=True)


if __name__ == "__main__":
    main()
