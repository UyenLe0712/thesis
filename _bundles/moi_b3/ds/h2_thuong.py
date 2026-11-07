# -*- coding: utf-8 -*-
"""H2 (report/323 §8.4): thưởng tốt = phân biệt được các câu trong nhóm VÀ khớp exec. 0 GPU, CPU + Java.

Dữ liệu: 8 mẫu C1 của S1/101 (runs/c1/c1_mau.jsonl, nhiệt độ 1,0) trên 400 bước val, exec từng mẫu ở
249 bước chạm (runs/c1/exec8/c1score/score_k{1..8}_raw.jsonl, UGround). ⛔ Số VAL: chỉ dùng để giải
thích và xếp hạng phần thưởng, KHÔNG trích ra báo như kết quả.
Mỗi phần thưởng tính ĐÚNG như lúc train (grpo_luoi.lam_thuong, gồm phạt độ dài), nhóm = 8 mẫu (G = 8).
Chỉ số trên mỗi nhóm, rồi lấy trung bình:
  std0      tỉ lệ nhóm mọi thưởng bằng nhau (nhóm không cho gradient)
  hoa       tỉ lệ cặp trong nhóm có thưởng bằng nhau
  conc      trên các cặp exec khác nhau: 1 nếu thưởng xếp đúng chiều, 0,5 nếu hoà, 0 nếu ngược
  p_khong_thap  trên các cặp thưởng khác nhau: P(exec câu thưởng cao ≥ exec câu thưởng thấp)
  tin_hieu  TB nhóm của TB_i[A_i · (e_i − ē)], A = lợi thế GRPO (r − r̄)/(std + 1e-4): lực đẩy về câu exec
  oracle    exec của câu thưởng cao nhất trong 8 (hoà thì lấy TB) − exec TB của 8 mẫu, đơn vị điểm %
Khối khong_cham (151 bước): e = đúng loại thao tác (canon_action strict_back), thay cho exec.
KTC 95% bootstrap theo episode (1.000 lần) cho conc và oracle.

  python h2_thuong.py --c1 C1DIR --bundle B --out ../runs/giai_thich/h2_thuong.json [--rewards spice,loai] [--n 40]
"""
import os, sys, json, glob, argparse, random, time, itertools, collections

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import thuong_moi as TM   # noqa: E402
TM.cai()
GL, ME = TM.GL, TM.ME


def nhom_chiso(R, E):
    """R, E: list nhóm, mỗi nhóm list 8 số. Trả dict chỉ số và list giá trị theo nhóm (để bootstrap)."""
    std0, hoa, conc_g, pk_g, th_g, or_g = [], [], [], [], [], []
    for r, e in zip(R, E):
        G = len(r)
        std0.append(float(max(r) - min(r) < 1e-9))
        P = list(itertools.combinations(range(G), 2))
        hoa.append(sum(abs(r[i] - r[j]) < 1e-9 for i, j in P) / len(P))
        c = [1.0 if (r[i] - r[j]) * (e[i] - e[j]) > 0 else 0.5 if abs(r[i] - r[j]) < 1e-9 else 0.0
             for i, j in P if e[i] != e[j]]
        conc_g.append(c)
        pk = [float((e[i] >= e[j]) if r[i] > r[j] else (e[j] >= e[i])) for i, j in P if abs(r[i] - r[j]) >= 1e-9]
        pk_g.append(pk)
        m = sum(r) / G
        sd = (sum((x - m) ** 2 for x in r) / (G - 1)) ** 0.5
        me = sum(e) / G
        th_g.append(sum((x - m) / (sd + 1e-4) * (y - me) for x, y in zip(r, e)) / G)
        mx = max(r)
        best = [y for x, y in zip(r, e) if abs(x - mx) < 1e-9]
        or_g.append(100 * (sum(best) / len(best) - me))
    flat = lambda L: [x for g in L for x in g]
    tb = lambda x: round(sum(x) / len(x), 4) if x else None
    return dict(n_nhom=len(R), std0=tb(std0), hoa=tb(hoa), conc=tb(flat(conc_g)), n_cap_exec_khac=len(flat(conc_g)),
                p_khong_thap=tb(flat(pk_g)), tin_hieu=tb(th_g), oracle_tru_tb=round(sum(or_g) / len(or_g), 2),
                e_tb=round(100 * sum(map(sum, E)) / (8 * len(E)), 2)), conc_g, or_g


def bootstrap(ep, conc_g, or_g, B=1000, seed=20261106):
    cum = collections.defaultdict(list)
    for i, e in enumerate(ep):
        cum[e].append(i)
    ks = list(cum)
    rd = random.Random(seed)
    cs, os_ = [], []
    for _ in range(B):
        idx = [i for k in (rd.choice(ks) for _ in ks) for i in cum[k]]
        c = [x for i in idx for x in conc_g[i]]
        cs.append(sum(c) / len(c) if c else 0.5)
        os_.append(sum(or_g[i] for i in idx) / len(idx))
    q = lambda v: [round(sorted(v)[int(0.025 * B)], 4), round(sorted(v)[int(0.975 * B) - 1], 4)]
    return dict(conc_ktc95=q(cs), oracle_ktc95=[round(x, 2) for x in q(os_)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--c1", required=True)
    ap.add_argument("--bundle", required=True, help="thư mục có p1_train_rows.jsonl (df CIDEr-D, loại thao tác câu nhắc)")
    ap.add_argument("--keys", default=os.path.join(H, "prompt_keys_ck500.json"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--rewards", default="")
    ap.add_argument("--n", type=int, default=0)
    a = ap.parse_args()
    t0 = time.time()
    out = {"ghi_chu": "SỐ VAL (C1, 400 bước val, S1/101 8 mẫu T=1,0) — chỉ để giải thích, không trích"}

    # ----- tỉ lệ bước không chạm trong câu nhắc của ck500 (report/330 §7 hàng 5 đòi đo) -----
    tr = {f"{r['episode_id']}_{r['step_id']}": r for r in map(json.loads, open(os.path.join(a.bundle, "p1_train_rows.jsonl"), encoding="utf-8"))}
    keys = json.load(open(a.keys))
    def lt(r):
        a_ = r.get("action")
        if isinstance(a_, str):
            import ast
            try:
                a_ = ast.literal_eval(a_)
            except Exception:
                a_ = {}
        return (a_ or {}).get("action_type") or str(r.get("action_type", "?"))
    ck = collections.Counter(lt(tr[k]) for k in keys if k in tr)
    allc = collections.Counter(lt(r) for r in tr.values())
    out["cau_nhac_ck500"] = dict(n_khoa=len(keys), n_tim_thay=sum(ck.values()), loai=dict(ck.most_common()),
                                 ti_le_khong_cham=round(1 - (ck["click"] + ck["long_press"]) / max(1, sum(ck.values())), 4),
                                 p1_train_rows_loai=dict(allc.most_common()))
    print("[câu nhắc ck500]", json.dumps(out["cau_nhac_ck500"], ensure_ascii=False), flush=True)

    # ----- dữ liệu C1 -----
    M = [json.loads(l) for l in open(os.path.join(a.c1, "c1_mau.jsonl"), encoding="utf-8")]
    assert len(M) == 400 and all(len(m["mau"]) == 8 for m in M), len(M)
    EX = {}
    for k in range(1, 9):
        for d in map(json.loads, open(os.path.join(a.c1, "c1score", f"score_k{k}_raw.jsonl"), encoding="utf-8")):
            EX[(d["episode_id"], d["step_id"], k)] = (int(d["executable"]), (d.get("sent") or "").strip())
    cham = [m for m in M if (m["episode_id"], m["step_id"], 1) in EX]
    kc = [m for m in M if (m["episode_id"], m["step_id"], 1) not in EX]
    assert len(cham) == 249, len(cham)
    lech = sum(EX[(m["episode_id"], m["step_id"], k)][1] != (m["mau"][k - 1] or "").strip() for m in cham for k in range(1, 9))
    print(f"[C1] {len(M)} bước · chạm {len(cham)} · không chạm {len(kc)} · câu lệch giữa tệp mẫu và tệp exec: {lech}", flush=True)
    assert lech <= 0.01 * 8 * len(cham), "⛔ tệp mẫu và tệp exec không khớp"
    if a.n:
        cham, kc = cham[:a.n], kc[:a.n]
    out["n_cau_lech_mau_exec"] = lech
    E_ch = [[EX[(m["episode_id"], m["step_id"], k)][0] for k in range(1, 9)] for m in cham]
    E_kc = [[int(bool(s.strip()) and TM.dung_loai(s, m["gold"])) for s in m["mau"]] for m in kc]
    out["ti_le_mau_sai_loai_o_buoc_cham"] = round(sum(not TM.dung_loai(s, m["gold"]) for m in cham for s in m["mau"]) / (8 * len(cham)), 4)

    # ----- tên vàng -----
    TM.nap_ten(H)
    co = [m for m in cham if TM.TEN.get(f"{m['episode_id']}_{m['step_id']}")]
    f_gold = [TM.f1_ten(m["gold"], TM.TEN[f"{m['episode_id']}_{m['step_id']}"]) for m in co]
    f_gold = [x for x in f_gold if x is not None]
    out["ten_vang"] = dict(buoc_cham_co_ten=len(co), n=len(cham), f1_cau_chuan_tb=round(sum(f_gold) / max(1, len(f_gold)), 4),
                           ti_le_cau_chuan_f1_0=round(sum(x == 0 for x in f_gold) / max(1, len(f_gold)), 4))
    print("[tên vàng]", out["ten_vang"], flush=True)

    ten = a.rewards.split(",") if a.rewards else list(GL.REWARDS)
    out["thuong"] = {}
    for name in ten:
        t1 = time.time()
        GL.dung_bo_cham(name, a.bundle)
        th = GL.lam_thuong(name)
        res = {}
        for khoi, ds, E in (("cham", cham, E_ch), ("khong_cham", kc, E_kc)):
            sents = [s for m in ds for s in m["mau"]]
            golds = [m["gold"] for m in ds for _ in range(8)]
            ks = [f"{m['episode_id']}_{m['step_id']}" for m in ds for _ in range(8)]
            r = th(sents, golds, key=ks)
            R = [r[8 * i:8 * i + 8] for i in range(len(ds))]
            cs, conc_g, or_g = nhom_chiso(R, E)
            cs.update(bootstrap([m["episode_id"] for m in ds], conc_g, or_g))
            cs["thuong_tb"] = round(sum(r) / len(r), 4)
            res[khoi] = cs
        g = [m["gold"] for m in cham]
        rg = th(g, g, key=[f"{m['episode_id']}_{m['step_id']}" for m in cham])
        res["cau_chuan_tu_cham_tb"] = round(sum(rg) / len(rg), 4)
        res["giay"] = round(time.time() - t1)
        out["thuong"][name] = res
        print(f"== {name}", json.dumps(res, ensure_ascii=False), flush=True)
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)       # ghi sau mỗi thưởng

    bang = sorted(out["thuong"].items(), key=lambda kv: -kv[1]["cham"]["conc"])
    print("\nthưởng       std0   hoà    conc   p≥     tín_hiệu oracle | không chạm: conc  oracle", flush=True)
    for n, v in bang:
        c, k = v["cham"], v["khong_cham"]
        print(f"{n:11s} {c['std0']:.3f} {c['hoa']:.3f} {c['conc']:.3f} {c['p_khong_thap']:.3f} {c['tin_hieu']:+.4f} {c['oracle_tru_tb']:+6.2f} |"
              f" {k['conc']} {k['oracle_tru_tb']:+6.2f}", flush=True)
    out["n_chay_thu"] = a.n
    out["giay"] = round(time.time() - t0)
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    print("[xong] ghi", a.out, flush=True)


if __name__ == "__main__":
    main()
