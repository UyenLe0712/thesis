# -*- coding: utf-8 -*-
"""TRIAD-T — bộ chọn câu lúc suy luận (action 273, 4/10/2026). Mã 0 GPU.

Đầu vào cho mỗi bước click: câu greedy d0 (ck500), các câu mẫu d1…dN, điểm listener L(di)
(thang 0–1000), t = loc_g, t' = loc_d. Luật §4 của 273:

  1. d0 không phải câu chạm ⇒ giữ d0.
  2. loại ứng viên rỗng / lặp bất thường / không phải chạm / listener không đọc được điểm.
  3. near(L(d0), t, r) ⇒ giữ d0.
  4. không near(t, t', r_trust) ⇒ giữ d0.
  5. A = {di, i≥1 : near(L(di), t, r)}; A rỗng ⇒ giữ d0.
  6. nhiều câu ⇒ Euclid L(di)→t nhỏ nhất, hoà thì chỉ số mẫu nhỏ nhất.

⛔ Hàm `chon()` KHÔNG nhận câu chuẩn, điểm vàng hay kết quả chấm. Điểm vàng và `executable`
chỉ được đọc ở `danh_gia()`, sau khi đã chọn xong.

Chế độ:
  --poa  --listener runs/triad_t/listener_showui.jsonl --name showui   (POA, ứng viên = mẫu S1)
  --b3                                                                 (đối chứng vòng tròn:
                                                                        listener = UGround từ tệp chấm sẵn)
  --make-calls --out calls.jsonl     (danh sách (bước, câu) duy nhất cho listener chạy trên Kaggle)
"""

import os, re, sys, json, math, random, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metric_exec import canon_action  # noqa: E402

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C1 = os.path.join(GOC, "runs/c1/exec8")
TV = os.path.join(GOC, "runs/tage_val/that")
TAPT = ("click", "long_press")
R_LUOI = (40, 60, 80, 100)
RT_LUOI = (80, 100, 140, 180)
SEED_BOOT = 20261004


def K(d):
    return (d["episode_id"], d["step_id"])


def nap(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def la_cau_cham(s):
    return canon_action(s) in ("tap", "long_press")


def lap_bat_thuong(s):
    """Khoá trước khi thấy số: > 40 từ, hoặc một bộ ba từ lặp ≥ 3 lần."""
    w = re.findall(r"[a-z0-9]+", (s or "").lower())
    if len(w) > 40:
        return True
    tri = collections.Counter(zip(w, w[1:], w[2:]))
    return bool(tri) and max(tri.values()) >= 3


def near(a, b, r):
    return abs(a[0] - b[0]) <= r and abs(a[1] - b[1]) <= r


def chon(buoc, r, rt):
    """buoc: dict d0, cands=[(i, câu)], L={câu: (x,y)|None}, t, tp. Trả (i_chọn, lý do).
    i_chọn = 0 là giữ d0."""
    d0, L, t, tp = buoc["d0"], buoc["L"], buoc["t"], buoc["tp"]
    if not la_cau_cham(d0):
        return 0, "d0_khong_cham"
    p0 = L.get(d0)
    if p0 is not None and near(p0, t, r):
        return 0, "d0_gan_t"
    if not near(t, tp, rt):
        return 0, "locator_bat_dong"
    A = []
    for i, s in buoc["cands"]:
        s2 = (s or "").strip()
        if not s2 or s2 == d0.strip() or lap_bat_thuong(s2) or not la_cau_cham(s2):
            continue
        p = L.get(s)
        if p is None or not near(p, t, r):
            continue
        A.append((math.hypot(p[0] - t[0], p[1] - t[1]), i))
    if not A:
        return 0, "A_rong"
    return min(A)[1], "doi"


def boot_episode(D, B=2000, seed=SEED_BOOT):
    """KTC95 cho tổng hiệu (bước) / n, bootstrap theo episode."""
    cl = collections.defaultdict(list)
    for k, d in D:
        cl[k[0]].append(d)
    g = list(cl.values())
    n = sum(map(len, g))
    rnd = random.Random(seed)
    bs = []
    for _ in range(B):
        pk = [g[rnd.randrange(len(g))] for _ in g]
        bs.append(100 * sum(map(sum, pk)) / sum(map(len, pk)))
    bs.sort()
    return 100 * sum(map(sum, g)) / n, bs[int(.025 * B)], bs[int(.975 * B)]


# ───────────────────────────── dữ liệu POA ─────────────────────────────

def nap_poa():
    recs = {K(d): d for d in nap(f"{C1}/c1data/c1_recs.jsonl")}
    ck = {K(d): d for d in nap(f"{TV}/score_ck500_l4_raw.jsonl")}
    keys = sorted(ck)
    assert len(keys) == 249
    S = [{K(d): d for d in nap(f"{C1}/c1score/score_k{i}_raw.jsonl")} for i in range(9)]
    P = [{K(d): (d["pred"] or "") for d in nap(f"{C1}/c1preds/k{i}.jsonl")} for i in range(9)]
    lg = {K(d): d["xy"] for d in nap(f"{TV}/loc_val_g.jsonl")}
    ld = {K(d): d["xy"] for d in nap(f"{TV}/loc_val_d.jsonl")}
    # toàn vẹn (§3.1)
    assert all(set(x) >= set(keys) for x in S + P + [lg, ld])
    assert sum(ck[k]["executable"] for k in keys) == 166
    assert sum(S[0][k]["executable"] for k in keys) == 158
    assert sum(d["hit_disk"] for d in nap(f"{TV}/loc_val_g.jsonl")) == 193
    assert sum(d["hit_disk"] for d in nap(f"{TV}/loc_val_d.jsonl")) == 190
    for i in range(9):
        assert all(S[i][k]["sent"].strip() == P[i][k].strip() for k in keys), i
    return recs, ck, keys, S, P, lg, ld


def exec_cua(ck, S, k, i):
    """exec của câu được chọn: i=0 ⇒ ck500; i≥1 ⇒ mẫu S1 k_i (đã chấm UGround sẵn)."""
    return ck[k]["executable"] if i == 0 else S[i][k]["executable"]


def to1000(d):
    return (d["pred_xy"][0] / d["wh"][0] * 1000, d["pred_xy"][1] / d["wh"][1] * 1000) \
        if d.get("pred_xy") else None


def danh_gia(keys, chon_i, ck, S, venus=None):
    """chon_i: {k: i}. Trả bảng cứu/phá so ck500 dưới UGround (và UI-Venus nếu có)."""
    cuu = pha = doi = 0
    D = []
    for k in keys:
        i = chon_i[k]
        e0, e1 = ck[k]["executable"], exec_cua(ck, S, k, i)
        doi += i != 0
        cuu += e1 > e0
        pha += e1 < e0
        D.append((k, e1 - e0))
    tong = sum(exec_cua(ck, S, k, chon_i[k]) for k in keys)
    out = {"dung": tong, "exec": round(100 * tong / len(keys), 2), "cuu": cuu, "pha": pha,
           "net": cuu - pha, "doi": doi, "coverage": round(100 * doi / len(keys), 2)}
    m, lo, hi = boot_episode(D)
    out["delta_pp"], out["ktc95"] = round(m, 2), [round(lo, 2), round(hi, 2)]
    if venus is not None:
        v0 = sum(venus[(k, 0)] for k in keys)
        v1 = sum(venus[(k, chon_i[k])] for k in keys)
        out["venus_ck500"], out["venus_chon"], out["venus_delta"] = v0, v1, v1 - v0
    return out


def khoa_chon(o):
    """Luật §5.3: rescue > break; break ít; net lớn; coverage lớn; (bán kính nhỏ do thứ tự duyệt)."""
    return (o["cuu"] > o["pha"], -o["pha"], o["net"], o["coverage"])


def chay_luoi(keys, buoc_cua, ck, S, co_cong=True, venus=None):
    """Trả {(r, rt): kết quả}. Không cổng ⇒ rt = ∞."""
    R = {}
    for r in R_LUOI:
        for rt in (RT_LUOI if co_cong else (10 ** 9,)):
            ci, ly = {}, collections.Counter()
            for k in keys:
                i, why = chon(buoc_cua(k), r, rt)
                ci[k] = i
                ly[why] += 1
            o = danh_gia(keys, ci, ck, S, venus)
            o["ly_do"] = dict(ly)
            o["chon"] = ci
            R[(r, rt)] = o
    return R


def chon_cau_hinh(R):
    """§5.3: trong từng r chọn rt, rồi chọn r; duyệt bán kính tăng dần, chỉ thay khi hơn hẳn."""
    tot_r = {}
    for (r, rt), o in sorted(R.items()):
        if r not in tot_r or khoa_chon(o) > khoa_chon(R[tot_r[r]]):
            tot_r[r] = (r, rt)
    best = None
    for r in sorted(tot_r):
        if best is None or khoa_chon(R[tot_r[r]]) > khoa_chon(R[best]):
            best = tot_r[r]
    return best, tot_r


def bang(R, best, tieu_de):
    print(f"\n{tieu_de}")
    print("  r   r_trust  cov%  đổi  cứu  phá  net  exec  Δpp [KTC95]")
    for (r, rt), o in sorted(R.items()):
        dau = "◀" if (r, rt) == best else " "
        rts = "—" if rt > 10 ** 8 else rt
        print(f"  {r:<4}{rts:<8} {o['coverage']:5.1f} {o['doi']:4} {o['cuu']:4} {o['pha']:4} "
              f"{o['net']:+4} {o['exec']:5.2f} {o['delta_pp']:+.2f} {o['ktc95']}"
              + (f" Venus {o['venus_delta']:+d}" if "venus_delta" in o else "") + f" {dau}")


def tong_hop(keys, buoc_cua, ck, S, nhan, venus=None):
    R1 = chay_luoi(keys, buoc_cua, ck, S, co_cong=False, venus=venus)
    R2 = chay_luoi(keys, buoc_cua, ck, S, co_cong=True, venus=venus)
    b1, _ = chon_cau_hinh(R1)
    b2, tot2 = chon_cau_hinh(R2)
    bang(R1, b1, f"[{nhan}] B1 — chọn theo loc_g, không cổng loc_d")
    bang(R2, b2, f"[{nhan}] B2 — TRIAD-T đầy đủ (cổng loc_g−loc_d)")
    sach = lambda R: {f"{r}_{'inf' if rt > 10**8 else rt}": {x: y for x, y in o.items() if x != "chon"}
                      for (r, rt), o in R.items()}
    return {"B1": sach(R1), "B2": sach(R2), "B1_chon": list(b1), "B2_chon": list(b2),
            "B2_tot_trong_tung_r": {r: list(v) for r, v in tot2.items()}}, R1[b1]["chon"], R2[b2]["chon"]


def buoc_factory(keys, ck, P, lg, ld, Lfn):
    def buoc_cua(k):
        d0 = ck[k]["sent"]
        cands = [(i, P[i][k]) for i in range(1, 9)]
        L = {s: Lfn(k, s) for s in [d0] + [c for _, c in cands]}
        return {"d0": d0, "cands": cands, "L": L, "t": lg[k], "tp": ld[k]}
    return buoc_cua


def ds_doi(keys, ci, ck, P, lg, ld, Lfn, recs):
    out = []
    for k in keys:
        i = ci[k]
        if i:
            out.append({"episode_id": k[0], "step_id": k[1], "mau": f"k{i}",
                        "ck500": ck[k]["sent"], "chon": P[i][k],
                        "L_ck500": Lfn(k, ck[k]["sent"]), "L_chon": Lfn(k, P[i][k]),
                        "loc_g": lg[k], "loc_d": ld[k]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--b3", action="store_true")
    ap.add_argument("--poa", action="store_true")
    ap.add_argument("--make-calls", action="store_true")
    ap.add_argument("--listener")
    ap.add_argument("--name", default="showui")
    ap.add_argument("--venus-dir", help="thư mục có score_venus_{ck500,k1..k8}_raw.jsonl (UI-Venus chấm sẵn)")
    ap.add_argument("--out")
    a = ap.parse_args()

    recs, ck, keys, S, P, lg, ld = nap_poa()
    print(f"[toàn vẹn] 249 key · S1 158 · ck500 166 · loc_g 193 · loc_d 190 — đạt", flush=True)

    if a.make_calls:
        seen, n = set(), 0
        with open(a.out, "w", encoding="utf-8") as f:
            for k in keys:
                cau = [("ck500", ck[k]["sent"])] + [(f"k{i}", P[i][k]) for i in range(9)] \
                    + [("gold", recs[k]["gold_instruction"])]       # gold: chỉ cho hit_disk độc lập
                for nguon, s in cau:
                    s = (s or "").strip()
                    if not s or (k, s) in seen:
                        continue
                    seen.add((k, s))
                    f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "nguon": nguon,
                                        "sent": s, "image": recs[k]["image"],
                                        "w": recs[k]["w"], "h": recs[k]["h"]},
                                       ensure_ascii=False) + "\n")
                    n += 1
        print(f"[calls] {n} lời gọi duy nhất → {a.out}")
        return

    if a.b3:
        Lu = {}
        for k in keys:
            Lu[(k, ck[k]["sent"].strip())] = to1000(ck[k])
            for i in range(9):
                Lu[(k, S[i][k]["sent"].strip())] = Lu.get((k, S[i][k]["sent"].strip())) or to1000(S[i][k])
        Lfn = lambda k, s: Lu.get((k, (s or "").strip()))
        res, c1, c2 = tong_hop(keys, buoc_factory(keys, ck, P, lg, ld, Lfn), ck, S, "B3 UGround-listener (vòng tròn)")
        res["chu_y"] = "đối chứng vòng tròn: UGround vừa chọn vừa chấm — chỉ chẩn đoán"
    else:
        L = {}
        for d in nap(a.listener):
            L[(K(d), d["sent"].strip())] = tuple(d["xy"]) if d.get("xy") else None
        Lfn = lambda k, s: L.get((k, (s or "").strip()))
        thieu = sum(1 for k in keys for s in [ck[k]["sent"]] + [P[i][k] for i in range(1, 9)]
                    if (s or "").strip() and (k, s.strip()) not in L)
        assert thieu == 0, f"⛔ listener thiếu {thieu} (bước, câu)"
        # listener độc lập: parse + hit_disk (vàng chỉ dùng ở đây)
        rows = nap(a.listener)
        n_ok = sum(1 for d in rows if d.get("xy"))
        hd = {}
        for d in rows:
            if d["nguon"] in ("gold", "ck500", "k0"):
                g = recs[K(d)]["action"]
                gx, gy = g["x"] / recs[K(d)]["w"] * 1000, g["y"] / recs[K(d)]["h"] * 1000
                hd.setdefault(d["nguon"], []).append(int(bool(d.get("xy")) and near(d["xy"], (gx, gy), 140)))
        sec = sorted(d.get("sec", 0) for d in rows)
        solo = {"n_goi": len(rows), "parse_pct": round(100 * n_ok / len(rows), 2),
                "hit_disk_pct": {x: round(100 * sum(v) / len(v), 2) for x, v in hd.items()},
                "hit_disk_n": {x: len(v) for x, v in hd.items()},
                "sec_trung_vi": sec[len(sec) // 2] if sec else None}
        print(f"\n[{a.name} độc lập] {solo}")
        venus = None
        if a.venus_dir:
            venus = {}
            for i, ten in [(0, "ck500")] + [(i, f"k{i}") for i in range(1, 9)]:
                V = {K(d): int(d["executable"]) for d in nap(f"{a.venus_dir}/score_venus_{ten}_raw.jsonl")}
                assert set(V) >= set(keys), f"⛔ UI-Venus {ten} thiếu bước"
                for k in keys:
                    venus[(k, i)] = V[k]
            print(f"[UI-Venus] ck500 {sum(venus[(k, 0)] for k in keys)}/249")
        res, c1, c2 = tong_hop(keys, buoc_factory(keys, ck, P, lg, ld, Lfn), ck, S, a.name, venus)
        res["listener_doc_lap"] = solo
        res["doi_cau_B2"] = ds_doi(keys, c2, ck, P, lg, ld, Lfn, recs)

    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nĐã lưu {a.out}")


if __name__ == "__main__":
    main()
