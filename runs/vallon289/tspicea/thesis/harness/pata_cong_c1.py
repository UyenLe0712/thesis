# -*- coding: utf-8 -*-
"""
PATA · đọc CỔNG CUỐI C1 trên val600 (report/185 §8). CHẠY TRÊN CPU, 0 GPU.

⛔ NGƯỠNG KHOÁ TRƯỚC — viết 24/9 ~13:00 VN, TRƯỚC khi có bất kỳ số val600 nào của C1 (C1 chưa train).
Đổi ngưỡng sau khi thấy số là cấm (§8: "không đổi … sau khi xem").

C1 đủ điều kiện chạy C0-Loc khi ĐẠT CẢ NĂM:
 1. câu hợp lệ ≥ 99% (C1 bật bridge) · độ dài TB ≤ 1,5 × của S · tỉ lệ câu rỗng ≤ của S + 1 điểm %.
    (§8 chỉ nói "không phình độ dài hoặc lặp bất thường" — 1,5× và +1 điểm là lựa chọn của phiên thi hành;
     lặp bất thường đã nằm trong định nghĩa "hợp lệ" của pata_eval.fmt_ok: 1–40 từ, một dòng, không thẻ,
     không từ nào lặp > 4 lần.)
 2. chẩn đoán J/final trên val400: CE_val ≤ 1,25 × CE_val(S) · KL_val ≤ 1,10 × KL_val(H) · cận dưới
    KTC một phía 90% của lift so với center prior, train prior VÀ đúng − xáo đều > 0.
 3. exec(C1 bật) ≥ exec(S)                 — ước lượng điểm, trên đủ bước chạm val600.
 4. exec(C1 bật) > exec(C1 tắt bridge)     — ước lượng điểm.
 5. P(về phía D | ép D) − P(về phía D | ép R) có cận dưới KTC một phía 90% > 0 (bootstrap cụm theo
    episode, 10.000 lần, hạt 20260924). "Về phía D" ⇔ điểm UGround trỏ câu sinh ra gần tâm hộp D hơn
    tâm hộp vàng. Điểm trỏ rỗng (câu rỗng) tính là KHÔNG về phía D.

Đầu vào (đặt chung một thư mục, tên do runbook P9/P10 quy định):
  score_C1_on_raw.jsonl · score_C1_off_raw.jsonl · score_C1_swapD_raw.jsonl · score_C1_swapR_raw.jsonl ·
  score_S_on_raw.jsonl        (tệp thô của score_run.py — có `executable`, `pred_xy`)
  preds_C1_val600_on.jsonl · preds_S_val600_on.jsonl       (để kiểm điều kiện 1)
  diag_S_val400.json · diag_H_val400.json · diag_J_val400.json   (pata_eval --mode diag)
Và `pata/val600_swap.jsonl` (hộp D, R).

    ~/.venvs/thesis/bin/python harness/pata_cong_c1.py --dir runs/pata/cong_c1
"""
import os, sys, json, math, random, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SEED = 20260924
B = 10000
NGUONG = {"hop_le_min": 0.99, "do_dai_max_x": 1.5, "rong_them_max": 0.01,
          "ce_max_x": 1.25, "kl_max_x": 1.10}


def doc(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def k(x):
    return (x["episode_id"], x["step_id"])


def exec_map(p):
    return {k(x): int(x.get("executable", 0) or 0) for x in doc(p)}


def boot(pairs, B=B):
    """pairs = [(episode, giá_trị)] → (trung bình, cận dưới 90% một phía, KTC 95% hai phía)."""
    cl = collections.defaultdict(list)
    for e, v in pairs:
        cl[e].append(v)
    g = list(cl.values())
    rnd = random.Random(SEED)
    bs = []
    for _ in range(B):
        pick = [g[rnd.randrange(len(g))] for _ in range(len(g))]
        bs.append(sum(sum(x) for x in pick) / sum(len(x) for x in pick))
    bs.sort()
    m = sum(v for _, v in pairs) / len(pairs)
    return m, bs[int(0.10 * B)], (bs[int(0.025 * B)], bs[int(0.975 * B)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--data-root", default=os.path.join(HERE, "dg1_cache", "train_ac"))
    a = ap.parse_args()
    from pata_eval import fmt_ok
    P = lambda f: os.path.join(a.dir, f)
    kq, dat = {}, {}

    # ── 1 ──
    c1 = {k(x): x["pred"] for x in doc(P("preds_C1_val600_on.jsonl"))}
    s = {k(x): x["pred"] for x in doc(P("preds_S_val600_on.jsonl"))}
    hop = sum(fmt_ok(v) for v in c1.values()) / len(c1)
    dd = lambda d: sum(len(v.split()) for v in d.values()) / len(d)
    rong = lambda d: sum(1 for v in d.values() if not v.strip()) / len(d)
    kq["1"] = {"hop_le": hop, "do_dai_C1": dd(c1), "do_dai_S": dd(s), "rong_C1": rong(c1), "rong_S": rong(s)}
    dat["1"] = (hop >= NGUONG["hop_le_min"] and dd(c1) <= NGUONG["do_dai_max_x"] * dd(s)
                and rong(c1) <= rong(s) + NGUONG["rong_them_max"])

    # ── 2 ──
    dS, dH, dJ = (json.load(open(P(f"diag_{t}_val400.json"))) for t in ("S", "H", "J"))
    lifts = {n: dJ[n]["lower90"] for n in ("lift_center", "lift_train", "dung_vs_xao")}
    kq["2"] = {"CE_val_J": dJ["CE_val"], "CE_val_S": dS["CE_val"], "KL_val_J": dJ["KL_val"],
               "KL_val_H": dH["KL_val"], "lower90": lifts}
    dat["2"] = (dJ["CE_val"] <= NGUONG["ce_max_x"] * dS["CE_val"]
                and dJ["KL_val"] <= NGUONG["kl_max_x"] * dH["KL_val"] and all(v > 0 for v in lifts.values()))

    # ── 3, 4 ──
    e_on, e_off, e_s = (exec_map(P(f"score_{t}_raw.jsonl")) for t in ("C1_on", "C1_off", "S_on"))
    ks = sorted(set(e_on) & set(e_off) & set(e_s))
    ep = {kk: kk[0] for kk in ks}
    for name, other in (("3", e_s), ("4", e_off)):
        m, lo, ci = boot([(ep[kk], e_on[kk] - other[kk]) for kk in ks])
        b_ = sum(1 for kk in ks if e_on[kk] > other[kk]); c_ = sum(1 for kk in ks if e_on[kk] < other[kk])
        kq[name] = {"n": len(ks), "exec_C1_on": sum(e_on[kk] for kk in ks) / len(ks),
                    "exec_so_sanh": sum(other[kk] for kk in ks) / len(ks), "delta": m,
                    "ktc95": ci, "C1_hon": b_, "C1_kem": c_}
    dat["3"] = kq["3"]["exec_C1_on"] >= kq["3"]["exec_so_sanh"]
    dat["4"] = kq["4"]["exec_C1_on"] > kq["4"]["exec_so_sanh"]

    # ── 5 ──
    sw = {k(x): x for x in doc(os.path.join(a.data_root, "pata", "val600_swap.jsonl"))}
    rD = {k(x): x for x in doc(P("score_C1_swapD_raw.jsonl"))}
    rR = {k(x): x for x in doc(P("score_C1_swapR_raw.jsonl"))}
    tam = lambda b: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)

    def ve_D(raw, s_):
        p = raw.get("pred_xy")
        if not p:
            return 0
        cD, cG = tam(s_["box_D"]), tam(s_["box_vang"])
        return int(math.dist(p, cD) < math.dist(p, cG))
    ks5 = sorted(set(sw) & set(rD) & set(rR))
    pairs = [(kk[0], ve_D(rD[kk], sw[kk]) - ve_D(rR[kk], sw[kk])) for kk in ks5]
    m, lo, ci = boot(pairs)
    kq["5"] = {"n": len(ks5), "ve_D_khi_ep_D": sum(ve_D(rD[kk], sw[kk]) for kk in ks5) / len(ks5),
               "ve_D_khi_ep_R": sum(ve_D(rR[kk], sw[kk]) for kk in ks5) / len(ks5),
               "chenh": m, "lower90": lo, "ktc95": ci}
    dat["5"] = lo > 0

    kq["nguong_khoa_truoc"] = NGUONG
    kq["dat"] = dat
    kq["cong_C1_dat"] = all(dat.values())
    json.dump(kq, open(P("cong_c1.json"), "w"), indent=1, ensure_ascii=False)
    print("=" * 76)
    ten = {"1": "câu hợp lệ, không phình/rỗng", "2": "CE/KL không phân kỳ + localizer vượt prior/xáo",
           "3": "exec(C1) ≥ exec(S)", "4": "exec(C1 bật) > exec(C1 tắt bridge)",
           "5": "ép D kéo câu về D hơn ép R (cận dưới 90% > 0)"}
    for i in "12345":
        print(f"  {i}. {'ĐẠT ' if dat[i] else 'KHÔNG'}  {ten[i]}")
        print(f"       {json.dumps(kq[i], ensure_ascii=False)[:300]}")
    print("=" * 76)
    print("⇒ CỔNG C1:", "ĐẠT — được chạy C0-Loc từ đúng H đã niêm phong" if kq["cong_C1_dat"] else
          "KHÔNG ĐẠT — dừng, không chạy C0, không mở test; kết luận 'futility under budget'")


if __name__ == "__main__":
    main()
