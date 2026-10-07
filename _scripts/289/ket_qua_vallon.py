# Bảng kết quả val lớn 289 (1.002 bước click): exec + năm thước văn bản COCO, so ghép cặp, bootstrap theo tác vụ.
# Nhánh nào có tệp thì tự vào bảng (tnghe chưa có thì bỏ qua) — thêm nhánh: đặt pred_<t>_vallon.jsonl và
# score_<t>_vallon_raw.jsonl ở bất kỳ thư mục con nào của runs/vallon289/, chạy lại.
# Chạy từ gốc kho: ~/.venvs/thesis/bin/python _scripts/289/ket_qua_vallon.py   (cần Java 8 ở ~/.jdk, SPICE ~3 phút/nhánh)
# Ra: runs/vallon289/ket_qua_vallon.json. Số val, chỉ để sàng — không trích ra báo.
import json, os, glob, random
J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
os.environ["JAVA_HOME"] = J[-1]; os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.spice.spice import Spice

V = "runs/vallon289"
NHANH = ["S1", "ck500", "tspicea", "tnghe", "tnghev", "tnghem", "tnghevm"]
SO = [("tspicea", "ck500"), ("tspicea", "S1"), ("tnghev", "ck500"), ("tnghev", "tspicea"), ("tnghev", "S1"),
      ("tnghe", "ck500"), ("tnghe", "tspicea"), ("tnghe", "S1"), ("tnghev", "tnghe")]

def tim(mau):
    f = sorted(glob.glob(f"{V}/**/{mau}", recursive=True))
    return f[0] if f else None

def doc(p): return {(r["episode_id"], r["step_id"]): r for r in map(json.loads, open(p))}

R, P = {}, {}
for t in NHANH:
    r, p = tim(f"score_{t}_vallon_raw.jsonl"), tim(f"pred_{t}_vallon.jsonl")
    if r and p:
        R[t], P[t] = doc(r), {k: v["pred"] for k, v in doc(p).items()}
        print(f"[nạp] {t}: {r} · {p}", flush=True)
keys = sorted(R["ck500"]); idx = {k: i for i, k in enumerate(keys)}
for t in R: assert R[t].keys() == P[t].keys() == set(keys) and len(keys) == 1002, f"DỪNG: {t} không cùng 1.002 bước"
ep = [k[0] for k in keys]

def boot(d, B, lo, hi):
    g = {}
    for e, x in zip(ep, d): g.setdefault(e, []).append(x)
    nh = list(g.values()); rd = random.Random(0); bs = []
    for _ in range(B):
        s = [nh[rd.randrange(len(nh))] for _ in nh]; bs.append(sum(map(sum, s)) / sum(map(len, s)))
    bs.sort(); return bs[lo], bs[hi]

out = {"n": len(keys), "tac_vu": len(set(ep)), "nhanh": {}, "so_cap": {}}
gold = {k: R["ck500"][k]["gold_instruction"] for k in keys}
G = PTBTokenizer().tokenize({i: [{"caption": gold[k]}] for k, i in idx.items()})
per = {}
for t in R:
    ex = [100 * int(R[t][k].get("executable") or 0) for k in keys]
    T = PTBTokenizer().tokenize({i: [{"caption": P[t][k] or ""}] for k, i in idx.items()})
    m = {"exec": sum(ex) / len(ex), "action_ok": 100 * sum(int(R[t][k]["action_ok"]) for k in keys) / len(keys),
         "so_tu_TB": sum(len((P[t][k] or "").split()) for k in keys) / len(keys),
         "trung_ck500": sum(P[t][k] == P["ck500"][k] for k in keys)}
    b, _ = Bleu(4).compute_score(G, T, verbose=0); m["BLEU-4"] = 100 * b[3]
    m["METEOR"] = 100 * Meteor().compute_score(G, T)[0]
    m["ROUGE-L"] = 100 * Rouge().compute_score(G, T)[0]
    c, cs = Cider().compute_score(G, T); m["CIDEr-D"] = 100 * c
    s, ss = Spice().compute_score(G, T); m["SPICE"] = 100 * s
    per[t] = {"exec": ex, "CIDEr-D": [100 * x for x in cs], "SPICE": [100 * x["All"]["f"] for x in ss]}
    out["nhanh"][t] = m
    print(t, {k: round(v, 2) for k, v in m.items()}, flush=True)

for a, b in SO:
    if a not in per or b not in per: continue
    o = {}
    for m, B, lo, hi in (("exec", 5000, 124, 4874), ("SPICE", 3000, 74, 2924), ("CIDEr-D", 3000, 74, 2924)):
        d = [x - y for x, y in zip(per[a][m], per[b][m])]
        o[m] = {"delta": sum(d) / len(d), "ktc95": boot(d, B, lo, hi)}
    o["exec"]["cuu"] = sum(x > y for x, y in zip(per[a]["exec"], per[b]["exec"]))
    o["exec"]["pha"] = sum(x < y for x, y in zip(per[a]["exec"], per[b]["exec"]))
    out["so_cap"][f"{a} - {b}"] = o
    print(f"{a} − {b}: " + " · ".join(f"{m} {v['delta']:+.2f} [{v['ktc95'][0]:+.2f}; {v['ktc95'][1]:+.2f}]" for m, v in o.items())
          + f" · cứu {o['exec']['cuu']} phá {o['exec']['pha']}", flush=True)

# luật sàng 288 bản 4: lên test ⇔ Δexec(X − ck500) ≥ +0,5 ∧ Δexec(X − tspicea) > 0
out["sang"] = {}
for x in ("tnghe", "tnghev", "tnghem", "tnghevm"):
    if x in per:
        d1 = out["so_cap"].get(f"{x} - ck500", {}).get("exec", {}).get("delta")
        d2 = out["so_cap"].get(f"{x} - tspicea", {}).get("exec", {}).get("delta")
        if d1 is None:
            d1 = (sum(per[x]["exec"]) - sum(per["ck500"]["exec"])) / len(keys)
        out["sang"][x] = {"d_ck500": d1, "d_tspicea": d2, "len_test": bool(d1 >= 0.5 and (d2 or -1) > 0)}
json.dump(out, open(f"{V}/ket_qua_vallon.json", "w"), ensure_ascii=False, indent=1)
print(f"→ {V}/ket_qua_vallon.json · sàng: {out['sang']}", flush=True)
