# -*- coding: utf-8 -*-
"""SA-SPICE-v3 PREFLIGHT, bước 2b: dựng TRAIN-v3 / DEV-v3 / CONFIRM-v3 theo §4.2 của
report/SA_SPICE_v3_extracted_verified.md và runs/sa_spice_v3/preflight/split_spec.json.

Ba lệnh, không lệnh nào gọi GPU hay mô hình:

  python3 sa3_split.py hash  --out H.jsonl [--forest all_forest_dict.zip]   # SHA-256 + pHash 63 bit + package mỗi bước, nối tiếp được
  python3 sa3_split.py build --hash H.jsonl --excl excl_episodes.json --out DIR
  python3 sa3_split.py selftest

`hash` duyệt mọi bước của train_ac/train.jsonl (pool + phần đã loại) và test_ac/test.jsonl để dò trùng chéo.
`build` dừng (exit 2) khi thiếu lineage, trùng khoá, thiếu ảnh/hash hay pool không đủ quota.
"""
import os, re, sys, io, json, math, gzip, pickle, hashlib, zipfile, argparse, collections, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TA = os.path.join(ROOT, "harness", "dg1_cache", "train_ac")
TE = os.path.join(ROOT, "harness", "dg1_cache", "test_ac")
SRC = "androidcontrol"                       # source_dataset: một nguồn duy nhất (HarrytheOrange ⋈ ckg)
QUOTA = {"DEV": 600, "CONFIRM": 1500, "TRAIN": 1000}
THU_TU = ("DEV", "CONFIRM", "TRAIN")         # thứ tự rút trong mỗi stratum, cố định
HAM = 4                                      # pHash Hamming ≤ 4
GENERIC_EP = 20                              # ảnh near-dup xuất hiện ở ≥20 episode ⇒ màn chung (home, chờ), không tạo cạnh
TXT = 0.90                                   # MinHash token-3gram
LAUNCHER = re.compile(r"(launcher|systemui|^android$|inputmethod|permissioncontroller)")


def stop(msg):
    print(f"⛔ STOP: {msg}", flush=True)
    sys.exit(2)


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "").lower()).strip()


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


# ---------------- pHash 63 bit ----------------
_D = None


def _dct_mat(n=32):
    import numpy as np
    k = np.arange(n)[:, None]; i = np.arange(n)[None, :]
    m = np.cos(math.pi * (2 * i + 1) * k / (2 * n)) * math.sqrt(2 / n)
    m[0] /= math.sqrt(2)
    return m


def phash63(img):
    """Ảnh xám 32×32 (LANCZOS) → DCT-II 2D → khối 8×8 tần thấp bỏ hệ số DC → so trung vị → 63 bit."""
    global _D
    import numpy as np
    from PIL import Image
    if _D is None:
        _D = _dct_mat()
    a = np.asarray(img.convert("L").resize((32, 32), Image.LANCZOS), dtype=np.float64)
    c = (_D @ a @ _D.T)[:8, :8].flatten()[1:]
    bits = c > np.median(c)
    return int("".join("1" if b else "0" for b in bits), 2)


def package_of(forest):
    c = collections.Counter()
    for w in forest or []:
        if w.get("window_type") == 3:
            continue
        for n in w.get("tree", []):
            p = n.get("package_name") or ""
            if p and not LAUNCHER.search(p):
                c[p] += 1
    return c.most_common(1)[0][0] if c else ""


def cmd_hash(a):
    from PIL import Image
    done = set()
    if os.path.exists(a.out):
        done = {(o["split_goc"], o["episode_id"], o["step_id"]) for o in load_jsonl(a.out)}
    z = zipfile.ZipFile(a.forest) if a.forest else None
    names = set(z.namelist()) if z else set()
    jobs = [("train_ac", TA, r) for r in load_jsonl(os.path.join(TA, "train.jsonl"))]
    tp = os.path.join(TE, "test.jsonl")
    if os.path.exists(tp):
        jobs += [("test_ac", TE, r) for r in load_jsonl(tp)]
    print(f"[hash] {len(jobs)} bước · đã có {len(done)}", flush=True)
    with open(a.out, "a", encoding="utf-8") as f:
        for i, (sg, base, r) in enumerate(jobs):
            k = (sg, int(r["episode_id"]), int(r["step_id"]))
            if k in done:
                continue
            p = os.path.join(base, r["image"])
            o = {"split_goc": sg, "episode_id": k[1], "step_id": k[2], "image": r["image"]}
            if os.path.exists(p):
                b = open(p, "rb").read()
                o["sha256"] = hashlib.sha256(b).hexdigest()
                o["phash"] = phash63(Image.open(io.BytesIO(b)))
            pk = f"all_forest_dict/android_control_episode_[{k[1]}]_{k[2]}.pkl"
            if z and pk in names:
                o["package"] = package_of(pickle.loads(z.read(pk)))
            f.write(json.dumps(o) + "\n")
            if (i + 1) % 2000 == 0:
                f.flush(); print(f"  … {i + 1}/{len(jobs)}", flush=True)
    print("[hash] xong", flush=True)


# ---------------- near-dup ----------------
class UF:
    def __init__(s):
        s.p = {}

    def f(s, x):
        s.p.setdefault(x, x)
        while s.p[x] != x:
            s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x

    def u(s, a, b):
        a, b = s.f(a), s.f(b)
        if a != b:
            s.p[max(a, b)] = min(a, b)


def image_edges(H):
    """H: list (ep_node, sha256, phash). Trả cạnh giữa episode + số ảnh 'màn chung' bị bỏ."""
    by_sha = collections.defaultdict(set)
    for ep, s, _ in H:
        by_sha[s].add(ep)
    CH = [(0, 13), (13, 26), (26, 39), (39, 51), (51, 63)]   # ≤4 bit khác ⇒ trùng ≥1 khúc (pigeonhole)
    buckets = collections.defaultdict(list)
    for idx, (ep, _, ph) in enumerate(H):
        for j, (lo, hi) in enumerate(CH):
            buckets[(j, (ph >> lo) & ((1 << (hi - lo)) - 1))].append(idx)
    nb = collections.defaultdict(set)                         # ảnh idx → tập episode near-dup
    for lst in buckets.values():
        if len(lst) > 5000:
            continue                                          # khúc của màn đồng màu; vẫn bắt qua khúc khác
        for x in range(len(lst)):
            i = lst[x]
            for y in range(x + 1, len(lst)):
                j = lst[y]
                if H[i][0] != H[j][0] and bin(H[i][2] ^ H[j][2]).count("1") <= HAM:
                    nb[i].add(H[j][0]); nb[j].add(H[i][0])
    edges, generic = set(), 0
    for i, eps in nb.items():
        eps = eps | by_sha[H[i][1]]
        if len(eps) + 1 >= GENERIC_EP:
            generic += 1; continue
        for e in eps:
            if e != H[i][0]:
                edges.add(tuple(sorted((H[i][0], e))))
    for s, eps in by_sha.items():
        if 1 < len(eps) < GENERIC_EP:
            eps = sorted(eps)
            for e in eps[1:]:
                edges.add((eps[0], e))
    return edges, generic


def item_edges(st):
    """v2 (11/11): st = list (node, phash, gold_norm). Cạnh giữa hai episode khi có MỘT CẶP BƯỚC ảnh pHash ≤ HAM
    (gồm SHA trùng) VÀ cùng câu chuẩn đã chuẩn hoá (khác rỗng) — trùng MỤC, không phải chỉ chung màn của app.
    Không bắc cầu: loại/nhóm tính trên cạnh trực tiếp."""
    CH = [(0, 13), (13, 26), (26, 39), (39, 51), (51, 63)]
    b = collections.defaultdict(list)
    for i, s_ in enumerate(st):
        if s_[2]:
            for j, (lo, hi) in enumerate(CH):
                b[(j, (s_[1] >> lo) & ((1 << (hi - lo)) - 1), s_[2])].append(i)
    edges = set()
    for lst in b.values():
        for x in range(len(lst)):
            for y in range(x + 1, len(lst)):
                i, j = lst[x], lst[y]
                if st[i][0] != st[j][0] and bin(st[i][1] ^ st[j][1]).count("1") <= HAM:
                    edges.add(tuple(sorted((st[i][0], st[j][0]))))
    return edges


def minhash_pairs(texts, perms=128, bands=16):
    """texts: {node: chuỗi đã chuẩn hoá}. Trả cặp có Jaccard token-3gram ≥ TXT (kiểm lại chính xác)."""
    import numpy as np
    P = (1 << 61) - 1
    rng = np.random.RandomState(20261111)
    A = rng.randint(1, 1 << 30, perms).astype(object); B = rng.randint(0, 1 << 30, perms).astype(object)
    sh = {}
    for n, t in texts.items():
        w = t.split()
        s = {" ".join(w[i:i + 3]) for i in range(max(1, len(w) - 2))}
        sh[n] = s
    lsh = collections.defaultdict(list)
    r = perms // bands
    for n, s in sh.items():
        xs = [int.from_bytes(hashlib.blake2b(g.encode(), digest_size=8).digest(), "big") for g in s]
        sig = [min(((a * x + b) % P) for x in xs) for a, b in zip(A, B)]
        for bi in range(bands):
            lsh[(bi, tuple(sig[bi * r:(bi + 1) * r]))].append(n)
    out = set()
    for lst in lsh.values():
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, b = sh[lst[i]], sh[lst[j]]
                if len(a & b) / max(1, len(a | b)) >= TXT:
                    out.add(tuple(sorted((lst[i], lst[j]))))
    return out


# ---------------- chia ----------------
def bucket(n):
    return "1-4" if n <= 4 else ("5-9" if n <= 9 else ">=10")


def dominant(acts):
    c = collections.Counter(acts)
    m = max(c.values())
    return sorted(a for a, v in c.items() if v == m)[0]     # hoà ⇒ tên action nhỏ nhất theo byte


def largest_remainder(sizes, total):
    tot = sum(sizes.values())
    if total > tot:
        stop(f"quota {total} > pool {tot}")
    raw = {k: total * v / tot for k, v in sizes.items()}
    q = {k: int(math.floor(x)) for k, x in raw.items()}
    rest = total - sum(q.values())
    for k in sorted(raw, key=lambda k: (-(raw[k] - q[k]), k.encode()))[:rest]:
        q[k] += 1
    return q


def chia(eps, quota=QUOTA):
    """eps: {episode_id: list[bản ghi]} đã lọc. Trả {split: [episode_id]} và bảng quota."""
    strat = collections.defaultdict(list)
    for e, rs in eps.items():
        strat[f"{dominant([r['action']['action_type'] for r in rs])}|{bucket(len(rs))}"].append(e)
    for k in strat:
        strat[k].sort(key=lambda e: sha(f"sa-spice-v3|{SRC}|{e}"))
    sizes = {k: len(v) for k, v in strat.items()}
    out, bang, con = {s: [] for s in THU_TU}, {}, dict(sizes)
    pos = {k: 0 for k in strat}
    for s in THU_TU:
        q = largest_remainder({k: v for k, v in con.items() if v > 0}, quota[s])
        bang[s] = q
        for k, n in q.items():
            out[s] += strat[k][pos[k]:pos[k] + n]
            pos[k] += n; con[k] -= n
    return out, bang


def train_step(rs):
    ok = [r for r in rs if norm(r.get("target_instruction"))]
    return min(ok, key=lambda r: sha(f"sa-spice-v3-step|{SRC}|{r['episode_id']}|{r['step_id']}")) if ok else None


def cmd_build(a):
    pool_recs = load_jsonl(os.path.join(TA, "train_tru_val.jsonl"))
    keys = [(SRC, int(r["episode_id"]), int(r["step_id"])) for r in pool_recs]
    if len(keys) != len(set(keys)):
        stop("khoá (source_dataset, episode_id, step_id) trùng")
    excl = set(json.load(open(a.excl)))
    H = load_jsonl(a.hash)
    hk = {(o["split_goc"], o["episode_id"], o["step_id"]): o for o in H}
    test = load_jsonl(os.path.join(TE, "test.jsonl")) if os.path.exists(os.path.join(TE, "test.jsonl")) else []
    allrec = [("train_ac", r) for r in load_jsonl(os.path.join(TA, "train.jsonl"))] + [("test_ac", r) for r in test]
    pool_ep = {int(r["episode_id"]) for r in pool_recs}
    node = lambda sg, e: f"{sg}:{e}"
    cand = pool_ep - excl                                              # episode được phép chọn
    tainted = {node("train_ac", e) for e in ({int(r["episode_id"]) for _, r in allrec if _ == "train_ac"} - cand)}
    tainted |= {node("test_ac", int(r["episode_id"])) for r in test}

    miss = [(sg, r["episode_id"], r["step_id"]) for sg, r in allrec
            if (sg, int(r["episode_id"]), int(r["step_id"])) not in hk or "phash" not in hk[(sg, int(r["episode_id"]), int(r["step_id"]))]]
    miss_pool = [m for m in miss if m[0] == "train_ac" and m[1] in cand]
    if miss_pool:
        stop(f"{len(miss_pool)} bước của pool thiếu ảnh/hash, vd {miss_pool[:3]}")
    st = [(node(sg, int(r["episode_id"])), hk[(sg, int(r["episode_id"]), int(r["step_id"]))]["phash"], norm(r.get("target_instruction")))
          for sg, r in allrec if "phash" in hk.get((sg, int(r["episode_id"]), int(r["step_id"])), {})]
    e_img = item_edges(st)
    goals = {}
    for sg, r in allrec:
        goals.setdefault(node(sg, int(r["episode_id"])), norm(r.get("goal")))
    e_txt = minhash_pairs(goals)
    adj = collections.defaultdict(set)
    for x, y in e_img | e_txt:
        adj[x].add(y); adj[y].add(x)
    C = {node("train_ac", e) for e in cand}
    loai_cheo = {int(n.split(":")[1]) for n in C if adj[n] & tainted}            # trùng mục trực tiếp với tập loại/test
    con = {n for n in C if int(n.split(":")[1]) not in loai_cheo}
    loai_nhom = {int(n.split(":")[1]) for n in con if adj[n] & con}              # trùng mục nội pool: loại cả hai phía
    adjud = [{"a": x, "b": y, "goal_a": goals[x], "goal_b": goals[y]} for x, y in sorted(e_txt) if x in C or y in C]
    generic = 0
    ok = cand - loai_cheo - loai_nhom
    eps = collections.defaultdict(list)
    for r in pool_recs:
        if int(r["episode_id"]) in ok:
            eps[int(r["episode_id"])].append(r)
    for e in eps:
        eps[e].sort(key=lambda r: int(r["step_id"]))
    loai_trong = {e for e, rs in eps.items() if any(not norm(r.get("target_instruction")) for r in rs)}
    for e in loai_trong:
        del eps[e]                                                                  # SPICE không chấm câu chuẩn trống
    # package cụm = package đa số (không tính launcher/systemui) trên các bước của episode; hoà ⇒ nhỏ nhất theo byte
    ep_pkg = {}
    for e, rs in eps.items():
        c = collections.Counter(hk[("train_ac", e, int(r["step_id"]))].get("package", "") for r in rs)
        c.pop("", None)
        ep_pkg[e] = sorted(c, key=lambda p: (-c[p], p.encode()))[0] if c else ""
    loai_pkg = {e for e in eps if not ep_pkg[e]}
    for e in loai_pkg:
        del eps[e]                                                                  # §7bis: mọi dòng DEV/CONFIRM phải có package
    sp, bang = chia(eps)
    os.makedirs(a.out, exist_ok=True)
    man = {"spec": "runs/sa_spice_v3/preflight/split_spec.json", "source_dataset": SRC,
           "pool": {"cand_episodes": len(cand), "loai_near_dup_cheo": len(loai_cheo),
                    "loai_nhom_noi_pool": len(loai_nhom), "loai_cau_chuan_trong": len(loai_trong), "loai_thieu_package": len(loai_pkg), "con_chon_duoc": len(eps)},
           "near_dup": {"canh_muc_anh_cau": len(e_img), "cap_goal_minhash": len(e_txt),
                        "luat": "v2: ảnh pHash≤4 ∧ cùng câu chuẩn, hoặc goal MinHash≥0,9; cạnh trực tiếp, không bắc cầu"},
           "quota": bang, "splits": {}}
    for s, lst in sp.items():
        rows = [train_step(eps[e]) for e in lst] if s == "TRAIN" else [r for e in lst for r in eps[e]]
        if any(r is None for r in rows):
            stop(f"{s}: episode không có bước có câu chuẩn")
        pk = [ep_pkg[int(r["episode_id"])] for r in rows]
        fn = os.path.join(a.out, f"{s.lower()}_v3.jsonl")
        with open(fn, "w", encoding="utf-8") as f:
            for r, p in zip(rows, pk):
                f.write(json.dumps({**r, "source_dataset": SRC, "package": p}, ensure_ascii=False) + "\n")
        man["splits"][s] = {"file": os.path.relpath(fn, ROOT), "sha256": hashlib.sha256(open(fn, "rb").read()).hexdigest(),
                            "episodes": len(lst), "steps": len(rows), "thieu_package": sum(1 for p in pk if not p),
                            "packages": len(set(p for p in pk if p)),
                            "action_steps": dict(collections.Counter(r["action"]["action_type"] for r in rows).most_common())}
    a_ep = [set(v) for v in sp.values()]
    assert not (a_ep[0] & a_ep[1] or a_ep[0] & a_ep[2] or a_ep[1] & a_ep[2]), "⛔ split chung episode"
    json.dump(adjud, open(os.path.join(a.out, "minhash_can_xet_tay.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(man, open(os.path.join(a.out, "split_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(man, ensure_ascii=False, indent=1), flush=True)


def selftest():
    from PIL import Image
    import numpy as np
    # pHash: cùng ảnh khác nén ⇒ ≤4 bit; hai ảnh khác hẳn ⇒ >4
    rng = np.random.RandomState(0)
    x = (rng.rand(200, 90) * 255).astype("uint8")
    a = phash63(Image.fromarray(x)); b = phash63(Image.fromarray(np.clip(x.astype(int) + 3, 0, 255).astype("uint8")))
    c = phash63(Image.fromarray((rng.rand(200, 90) * 255).astype("uint8")))
    assert bin(a ^ b).count("1") <= HAM < bin(a ^ c).count("1"), (bin(a ^ b).count("1"), bin(a ^ c).count("1"))
    assert a < (1 << 63)
    # largest remainder: tổng đúng, hoà theo byte
    q = largest_remainder({"b": 1, "a": 1, "c": 1}, 2)
    assert q == {"a": 1, "b": 1, "c": 0}, q
    assert dominant(["scroll", "click", "scroll", "click"]) == "click"
    # chia: tách rời, đủ quota, tất định
    eps = {}
    for e in range(400):
        n = 1 + e % 12
        eps[e] = [{"episode_id": e, "step_id": s, "target_instruction": "x y z",
                   "action": {"action_type": ["click", "scroll", "wait"][(e + s) % 3]}} for s in range(n)]
    sp, _ = chia(eps, {"DEV": 50, "CONFIRM": 100, "TRAIN": 80})
    assert [len(sp[s]) for s in THU_TU] == [50, 100, 80]
    assert not (set(sp["DEV"]) & set(sp["CONFIRM"]) or set(sp["DEV"]) & set(sp["TRAIN"]) or set(sp["CONFIRM"]) & set(sp["TRAIN"]))
    assert chia(eps, {"DEV": 50, "CONFIRM": 100, "TRAIN": 80})[0] == sp
    # minhash: gần trùng bắt, khác không
    pr = minhash_pairs({"u": "open the clock app and set an alarm for 7 am on weekdays please",
                        "v": "open the clock app and set an alarm for 7 am on weekdays please now",
                        "w": "search for running shoes on amazon and add the cheapest to cart"})
    assert ("u", "v") in pr and not any("w" in p for p in pr), pr
    # image_edges: màn chung ở ≥GENERIC_EP episode không tạo cạnh
    X = 0x5555555555555555 & ((1 << 63) - 1)
    H = [(f"e{i}", "s_home", X ^ ((1 << 63) - 1)) for i in range(GENERIC_EP + 1)] + [("x", "s1", X), ("y", "s1b", X ^ 1)]
    ed, g = image_edges(H)
    assert ("x", "y") in ed and not any(p[0].startswith("e") for p in ed) and g >= GENERIC_EP, (ed, g)
    ie = item_edges([("a", X, "click ok"), ("b", X ^ 1, "click ok"), ("c", X ^ 1, "click cancel"), ("d", X ^ 0xFFFF, "click ok")])
    assert ie == {("a", "b")}, ie
    print("selftest ĐẠT", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["hash", "build", "selftest"])
    ap.add_argument("--out"); ap.add_argument("--forest"); ap.add_argument("--hash"); ap.add_argument("--excl")
    a = ap.parse_args()
    {"hash": cmd_hash, "build": cmd_build, "selftest": lambda a: selftest()}[a.cmd](a)
