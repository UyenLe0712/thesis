"""H2/H3 của report/323 §8.4: phần thưởng nào cho TÍN HIỆU HỌC tốt trên AndroidControl — 0 GPU.

Dữ liệu: 249 bước chạm của tập kiểm định C1 (runs/c1/exec8), mỗi bước có câu greedy của S1 (k0) và
8 câu S1 lấy mẫu ở nhiệt độ 1,0 (k1..k8), mỗi câu có nhãn exec (UGround). Đây đúng là một nhóm G = 8
ở bước đầu của GRPO xuất phát từ S1. ⛔ Số val: chỉ dùng để giải thích cơ chế, không trích làm kết quả.

Với mỗi phần thưởng (dạng y hệt lúc train: điểm − phạt câu dài, câu rỗng = 0) đo:
  nhom_std0   tỉ lệ nhóm 8 câu có thưởng bằng nhau hết ⇒ GRPO không có gradient ở nhóm đó
  cap_hoa     tỉ lệ cặp câu trong nhóm có thưởng bằng nhau
  cap_dung    trong các cặp khác exec: P(câu exec = 1 có thưởng cao hơn), hoà tính 0,5
  dau_dung    với lợi thế GRPO A_i ≠ 0 và exec_i ≠ TB exec nhóm: P(dấu A_i = dấu (exec_i − TB))
  oracle      exec khi chọn câu thưởng cao nhất trong 8 câu (hoà lấy câu đứng trước)
Và với phần thưởng SPICE, so năm cách tính lợi thế (H3): tỉ lệ lợi thế = 0, dau_dung.

  python thuong_dac_tinh.py --bundle <thư mục có p1_train_rows.jsonl> [--rewards spice,cider,...]
"""
import os, sys, json, argparse, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_luoi as GL      # noqa: E402
import grpo_spice as GS     # noqa: E402

C1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs", "c1", "exec8")
G = 8


def nap():
    S = []
    for k in range(9):
        S.append({(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(f"{C1}/c1score/score_k{k}_raw.jsonl"))})
    keys = sorted(S[0])
    assert all(set(s) == set(keys) for s in S) and len(keys) == 249, "⛔ lệch bước giữa các mẫu"
    gold = [S[0][k]["gold_instruction"] for k in keys]
    sent = [[S[j][k]["sent"] or "" for j in range(9)] for k in keys]
    ex = [[int(S[j][k]["executable"]) for j in range(9)] for k in keys]
    assert sum(e[0] for e in ex) == 158, "⛔ greedy không tái lập 158/249"
    return keys, gold, sent, ex


def thuong_cua(name, gold, sent):
    f = GL.lam_thuong(name)
    flat_s = [s for row in sent for s in row]
    flat_g = [g for g, row in zip(gold, sent) for _ in row]
    r = f(flat_s, flat_g)
    return [r[i * 9:(i + 1) * 9] for i in range(len(gold))]


def loi_the(algo, r8, rg, ema_b):
    m = sum(r8) / G
    if algo == "grpo":
        sd = (sum((x - m) ** 2 for x in r8) / (G - 1)) ** 0.5
        return [(x - m) / (sd + 1e-4) for x in r8]
    if algo in ("drgrpo", "rloo"):
        return [(x - m) * (G / (G - 1) if algo == "rloo" else 1) for x in r8]
    if algo == "scst":
        return [x - rg for x in r8]
    if algo == "reinforce":
        return [x - ema_b for x in r8]
    raise ValueError(algo)


def do(name, gold, sent, ex):
    R = thuong_cua(name, gold, sent)
    n = len(gold)
    std0 = hoa = cap = dung = 0
    ds_n = 0
    orc = 0
    for r9, e9 in zip(R, ex):
        r, e = r9[1:], e9[1:]
        if max(r) - min(r) < 1e-9:
            std0 += 1
        for i in range(G):
            for j in range(i + 1, G):
                cap += 1
                hoa += abs(r[i] - r[j]) < 1e-9
                if e[i] != e[j]:
                    hi = i if e[i] > e[j] else j
                    lo = j if hi == i else i
                    dung += 1.0 if r[hi] > r[lo] + 1e-9 else (0.5 if abs(r[hi] - r[lo]) < 1e-9 else 0.0)
                    ds_n += 1
        orc += e[max(range(G), key=lambda i: (r[i], -i))]
    # dấu đúng
    dd = dn = 0
    for r9, e9 in zip(R, ex):
        r, e = r9[1:], e9[1:]
        A = loi_the("grpo", r, None, None)
        me = sum(e) / G
        for a, x in zip(A, e):
            if abs(a) > 1e-6 and abs(x - me) > 1e-9:
                dn += 1
                dd += (a > 0) == (x > me)
    return dict(nhom_std0=round(100 * std0 / n, 2), cap_hoa=round(100 * hoa / cap, 2),
                cap_dung=round(100 * dung / ds_n, 2), so_cap_khac_exec=ds_n,
                dau_dung=round(100 * dd / dn, 2), oracle_exec=round(100 * orc / n, 2),
                thuong_tb=round(sum(sum(r[1:]) for r in R) / (n * G), 4)), R


def do_algo(R, ex):
    """H3: cùng thưởng, năm cách tính lợi thế. REINFORCE dùng mốc trượt duyệt theo thứ tự xáo cố định."""
    out = {}
    order = list(range(len(R)))
    random.Random(101).shuffle(order)
    for algo in ("grpo", "drgrpo", "rloo", "reinforce", "scst"):
        z = tot = dd = dn = 0
        b = None
        for idx in order:
            r9, e9 = R[idx], ex[idx]
            r, e = r9[1:], e9[1:]
            m = sum(r) / G
            b0 = m if b is None else b
            A = loi_the(algo, r, r9[0], b0)
            if algo == "reinforce":
                b = GL.EMA * b0 + (1 - GL.EMA) * m
            me = sum(e) / G
            for a, x in zip(A, e):
                tot += 1
                z += abs(a) < 1e-6
                if abs(a) > 1e-6 and abs(x - me) > 1e-9:
                    dn += 1
                    dd += (a > 0) == (x > me)
        out[algo] = dict(loi_the_bang_0=round(100 * z / tot, 2), dau_dung=round(100 * dd / dn, 2), n_xet=dn)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--rewards", default="spice,cider,bleu4,rougel,chrf,meteor,spider")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs", "thuong_dac_tinh"))
    a = ap.parse_args()
    keys, gold, sent, ex = nap()
    trung_greedy = sum(s[j].strip() == s[0].strip() for s in sent for j in range(1, 9)) / (len(sent) * G)
    print(f"[dữ liệu] 249 bước · greedy exec 158 · câu lấy mẫu trùng câu greedy {100*trung_greedy:.1f}%", flush=True)
    os.makedirs(a.out, exist_ok=True)
    kq = {"n_buoc": 249, "G": G, "trung_greedy_pct": round(100 * trung_greedy, 2), "thuong": {}}
    for name in a.rewards.split(","):
        GL.dung_bo_cham(name, a.bundle)
        d, R = do(name, gold, sent, ex)
        kq["thuong"][name] = d
        print(f"[{name}] {d}", flush=True)
        if name == "spice":
            kq["algo_spice"] = do_algo(R, ex)
            print("[algo, thưởng spice]", kq["algo_spice"], flush=True)
        json.dump(kq, open(os.path.join(a.out, "ket_qua.json"), "w"), ensure_ascii=False, indent=1)
    print("→", os.path.join(a.out, "ket_qua.json"))


if __name__ == "__main__":
    main()
