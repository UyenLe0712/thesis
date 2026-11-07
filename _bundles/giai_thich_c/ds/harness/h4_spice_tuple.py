# -*- coding: utf-8 -*-
"""H4 (report/323 §8.4): SPICE tăng ở loại tuple nào — 0 GPU, CPU + Java (Kaggle CPU).

Dự đoán ghi trước (report/323): GRPO + SPICE (ck500) tăng SPICE chủ yếu ở tuple đối tượng/thuộc tính, tức tên phần tử.
Đo trên 4.463 bước chạm test, câu đã sinh sẵn trong tệp raw (trường sent, gold_instruction, action_ok, executable):
  1. Mỗi nhánh: SPICE từng câu với -detailed (giữ danh sách tuple), cộng gộp tp/fp/fn theo loại
     Object / Attribute / Relation (ba loại này chia hết All) → recall vi mô = tp/(tp+fn), precision, F.
  2. Δ so S1/101: Δtp theo loại và tỉ phần của Δtp_All; Δrecall theo loại; KTC95 bootstrap cụm theo episode.
  3. Tuple "phổ biến" (xuất hiện ở ≥1% câu chuẩn) và "hiếm": Δtp theo hai nhóm.
  4. Đối chiếu exec: trong nhóm S1 đúng loại thao tác mà exec trượt, so ΔSPICE Object ở bước nhánh cứu được
     (exec 0→1) với bước không cứu; và ở bước nhánh phá (1→0).
Số mô tả, hậu kiểm, một hạt giống.

  python h4_spice_tuple.py --out ../runs/giai_thich/c/h4_spice_tuple.json [--n 200]
"""
import os, sys, json, argparse, collections, random, subprocess, tempfile, time, glob, importlib.util

H = os.path.dirname(os.path.abspath(__file__))
K = os.path.join(H, "..")
LOAI = ("Object", "Attribute", "Relation")


def _spl():
    return list(importlib.util.find_spec("pycocoevalcap").submodule_search_locations)[0] + "/spice"


def spice_chi_tiet(hyp, ref, nhan="spice"):
    """SPICE từng câu, gọi thẳng jar với -detailed. Trả list dict(scores, test, ref):
    test = list (tuple_str, khớp bool), ref = list tuple_str. Tách từ bằng PTBTokenizer như pycocoevalcap."""
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(ref)})
    c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
    d = _spl()
    inp = [{"image_id": i, "test": c[i][0], "refs": g[i]} for i in range(len(hyp))]
    td = tempfile.mkdtemp(dir=os.path.join(d, "tmp") if os.path.isdir(os.path.join(d, "tmp")) else None)
    fi, fo = os.path.join(td, "in.json"), os.path.join(td, "out.json")
    json.dump(inp, open(fi, "w"))
    cache = os.path.join(d, "cache")
    os.makedirs(cache, exist_ok=True)
    t0 = time.time()
    lenh = ["java", "-jar", "-Xmx8G", "spice-1.0.jar", fi, "-cache", cache, "-out", fo, "-subset", "-detailed", "-silent"]
    r = subprocess.run(lenh, cwd=d, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-3000:], flush=True)
        raise SystemExit(f"DUNG: jar SPICE lỗi ({nhan})")
    out = json.load(open(fo))
    print(f"  [{nhan}] {len(hyp)} câu · {time.time() - t0:.0f} s", flush=True)
    if not getattr(spice_chi_tiet, "_da_in", False):
        x = out[0]
        print("  [khoá jar]", sorted(x.keys()), "· mẫu test_tuples:", json.dumps(x.get("test_tuples", [])[:2])[:300], flush=True)
        spice_chi_tiet._da_in = True
    by = {o["image_id"]: o for o in out}
    R = []
    for i in range(len(hyp)):
        o = by[i]
        tt = [(" | ".join(t["tuple"]), bool(t.get("truth_value"))) for t in o.get("test_tuples", [])]
        rt = [" | ".join(t["tuple"]) for t in o.get("ref_tuples", [])]
        R.append(dict(scores=o["scores"], test=tt, ref=rt))
    return R


def loai_tuple(t):
    n = t.count(" | ") + 1
    return {1: "Object", 2: "Attribute", 3: "Relation"}.get(n, "Relation")


def gop(S, idx=None):
    idx = range(len(S)) if idx is None else idx
    o = {}
    for c in ("All",) + LOAI:
        tp = sum(S[i]["scores"][c]["tp"] for i in idx)
        fp = sum(S[i]["scores"][c]["fp"] for i in idx)
        fn = sum(S[i]["scores"][c]["fn"] for i in idx)
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        o[c] = dict(tp=tp, fp=fp, fn=fn, P=round(p, 4), R=round(r, 4), F=round(2 * p * r / (p + r), 4) if p + r else 0.0)
    fs = [S[i]["scores"]["All"]["f"] for i in idx]
    fs = [f for f in fs if isinstance(f, (int, float)) and f == f]
    o["All_f_tb"] = round(sum(fs) / max(1, len(fs)), 4)
    return o


def boot(ep, f, B=1000, seed=20261106):
    """KTC95 bootstrap cụm theo episode cho hàm f(list chỉ số)."""
    cum = collections.defaultdict(list)
    for i, e in enumerate(ep):
        cum[e].append(i)
    ks = list(cum)
    rd = random.Random(seed)
    v = []
    for _ in range(B):
        idx = [i for k in (rd.choice(ks) for _ in ks) for i in cum[k]]
        v.append(f(idx))
    v.sort()
    return [round(v[int(0.025 * B)], 4), round(v[int(0.975 * B) - 1], 4)]


def nap_raw(p):
    D = {}
    for l in open(p, encoding="utf-8"):
        d = json.loads(l)
        D[(str(d["episode_id"]), str(d["step_id"]))] = d
    return D


NHANH = [
    ("s1_101", "runs/score_s1_seed101_raw.jsonl"),
    ("ck500", "runs/grpo_spice/score_ck500_test_raw.jsonl"),
    ("grpo_rougel", "runs/luoi/test_2_11/score_grpo_rougel_101_test_raw.jsonl"),
    ("scst_spice", "runs/luoi/test_2_11/score_scst_spice_101_test_raw.jsonl"),
    ("grpo_meteor", "runs/luoi/test_2_11/score_grpo_meteor_101_test_raw.jsonl"),
    ("grpo_cider", "runs/luoi/test_2_11/score_grpo_cider_101_test_raw.jsonl"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=0)
    a = ap.parse_args()
    RAW = {t: nap_raw(f"{K}/{p}") for t, p in NHANH if os.path.exists(f"{K}/{p}")}
    print("nhánh có tệp:", {t: len(v) for t, v in RAW.items()}, flush=True)
    ks = sorted(RAW["s1_101"])
    assert len(ks) == 4463, len(ks)
    for t, v in RAW.items():
        assert set(v) == set(ks), (t, len(v))
    if a.n:
        ks = ks[:a.n]
    TG = {(str(r["episode_id"]), str(r["step_id"])): (r.get("gold_instruction") or "")
          for r in map(json.loads, open(f"{K}/harness/dg1_cache/test_ac/test.jsonl", encoding="utf-8"))}
    G = [TG[k] for k in ks]
    for t, v in RAW.items():
        lech = sum(1 for k, g in zip(ks, G) if "gold_instruction" in v[k] and v[k]["gold_instruction"].strip() != g.strip())
        thieu = sum(1 for k in ks if "gold_instruction" not in v[k])
        print(f"  {t}: câu chuẩn lệch test.jsonl {lech} · dòng bỏ qua (câu rỗng) {thieu}", flush=True)
        assert lech == 0, t
        for k in ks:  # dòng bỏ qua của score_run: câu rỗng, exec = 0
            v[k].setdefault("sent", ""); v[k].setdefault("action_ok", 0); v[k].setdefault("executable", 0)
    ep = [k[0] for k in ks]

    print("câu chuẩn với chính nó (lấy tuple chuẩn)", flush=True)
    SG = spice_chi_tiet(G, G, "chuan")
    df = collections.Counter(t for s in SG for t in set(s["ref"]))
    nguong = max(2, int(0.01 * len(ks)))
    pho_bien = {t for t, c in df.items() if c >= nguong}
    occ = [t for s in SG for t in s["ref"]]
    out = dict(n=len(ks), nguong_pho_bien=nguong, n_tuple_khac=len(df), n_pho_bien=len(pho_bien),
               ti_le_lan_xuat_hien_pho_bien=round(sum(t in pho_bien for t in occ) / max(1, len(occ)), 4),
               top15_tuple=[(t, c) for t, c in df.most_common(15)])
    print(json.dumps(out, ensure_ascii=False)[:1500], flush=True)

    S = {}
    for t, v in RAW.items():
        S[t] = spice_chi_tiet([v[k]["sent"] or "" for k in ks], G, t)
    out["gop"] = {t: gop(s) for t, s in S.items()}
    for t, s in S.items():
        tr = [s[i]["scores"]["All"]["f"] for i, k in enumerate(ks) if RAW[t][k]["executable"] == 1]
        tt = [s[i]["scores"]["All"]["f"] for i, k in enumerate(ks) if RAW[t][k]["executable"] == 0]
        out["gop"][t]["spice_trung_tru_truot"] = round(sum(tr) / max(1, len(tr)) - sum(tt) / max(1, len(tt)), 4)
        out["gop"][t]["exec"] = round(len(tr) / len(ks), 4)
    for t, s in out["gop"].items():
        print(t, json.dumps(s, ensure_ascii=False), flush=True)

    def tp_nhom(s, idx, nhom):
        return sum(1 for i in idx for tt, ok in s[i]["test"] if ok and ((tt in pho_bien) == (nhom == "pho_bien")))

    D = {}
    s1 = S["s1_101"]
    for t, s in S.items():
        if t == "s1_101":
            continue
        dd = {}
        dtp_all = out["gop"][t]["All"]["tp"] - out["gop"]["s1_101"]["All"]["tp"]
        dd["dtp_All"] = dtp_all
        for c in LOAI:
            x = out["gop"][t][c]["tp"] - out["gop"]["s1_101"][c]["tp"]
            dd[f"dtp_{c}"] = x
            dd[f"ti_phan_{c}"] = round(x / dtp_all, 4) if dtp_all else None
            dd[f"dR_{c}"] = round(out["gop"][t][c]["R"] - out["gop"]["s1_101"][c]["R"], 4)
            dd[f"dR_{c}_ktc"] = boot(ep, lambda idx, c=c: gop(s, idx)[c]["R"] - gop(s1, idx)[c]["R"], B=300)
        dd["dF_All_ktc"] = boot(ep, lambda idx: gop(s, idx)["All"]["F"] - gop(s1, idx)["All"]["F"], B=300)
        for nh in ("pho_bien", "hiem"):
            dd[f"dtp_{nh}"] = tp_nhom(s, range(len(ks)), nh) - tp_nhom(s1, range(len(ks)), nh)
        # đối chiếu exec
        A0 = [RAW["s1_101"][k] for k in ks]
        B0 = [RAW[t][k] for k in ks]
        nhom = collections.defaultdict(list)
        for i, (x, y) in enumerate(zip(A0, B0)):
            if x["action_ok"] == 1 and x["executable"] == 0:
                nhom["s1_dungloai_truot__" + ("cuu" if y["executable"] == 1 else "khong_cuu")].append(i)
            if x["executable"] == 1 and y["executable"] == 0:
                nhom["pha"].append(i)
            if x["action_ok"] == 0 and y["action_ok"] == 1:
                nhom["sua_loai"].append(i)
        dd["doi_chieu_exec"] = {}
        for g, idx in nhom.items():
            r = dict(n=len(idx))
            for c in ("All", "Object", "Attribute"):
                a1 = [s1[i]["scores"][c]["f"] for i in idx]
                b1 = [s[i]["scores"][c]["f"] for i in idx]
                pr = [(u, w) for u, w in zip(a1, b1) if isinstance(u, (int, float)) and isinstance(w, (int, float)) and u == u and w == w]
                r[f"dF_{c}_tb"] = round(sum(w - u for u, w in pr) / max(1, len(pr)), 4)
            r["dtp_Object"] = sum(s[i]["scores"]["Object"]["tp"] - s1[i]["scores"]["Object"]["tp"] for i in idx)
            dd["doi_chieu_exec"][g] = r
        D[t] = dd
        print(t, json.dumps(dd, ensure_ascii=False), flush=True)
    out["delta_so_s1"] = D
    out["n_chay_thu"] = a.n
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    print("[xong] ghi", a.out, flush=True)


if __name__ == "__main__":
    main()
