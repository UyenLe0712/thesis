# -*- coding: utf-8 -*-
"""Đọc kết quả TAGE trên val C1 (file 265 §6, 2/10/2026) — 0 GPU, không bộ trỏ, vài giây.

    python3 harness/tage_doc.py [--dir runs/tage_val/that]

Mốc: ck500 = `runs/grpo_spice/score_ck500_raw.jsonl` (249 bước click val C1). Mỗi nhánh có
`score_<nhánh>_raw.jsonl` trong --dir: exec, Δ ghép cặp so ck500, KTC95 bootstrap theo episode,
cứu/phá, số câu đổi. Nhánh có `pred_<nhánh>_meta.jsonl` thêm dòng `+cổng`: sửa khi
lp_edit − lp_draft > τ, τ chọn chéo theo episode (chọn trên nửa này, áp lên nửa kia). Bộ định vị
(`loc_val_*.jsonl`): trúng ±14% trên 249 / 84 bước ck500 sai / 80 bước ck500 trỏ sai.
Cuối cùng in phán quyết V1–V3 theo §3. ⛔ Số val — không trích vào luận văn.
"""
import argparse, glob, json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B, SEED = 10000, 20261002


def nap(p):
    return {(d["episode_id"], d["step_id"]): d for d in map(json.loads, open(p, encoding="utf-8"))}


def ktc(keys, diff):
    """Bootstrap theo episode cho tổng hiệu số ghép cặp, quy ra điểm phần trăm trên len(keys)."""
    ep = {}
    for k in keys:
        ep.setdefault(k[0], []).append(diff[k])
    tong = [sum(v) for v in ep.values()]
    rng, n, E = random.Random(SEED), len(keys), list(tong)
    bs = sorted(sum(rng.choice(E) for _ in E) for _ in range(B))
    return 100 * bs[int(0.025 * B)] / n, 100 * bs[int(0.975 * B) - 1] / n


def cong(keys, ck, br, meta):
    """exec sau cổng, τ chọn chéo theo hai nửa episode. Trả (exec theo bước, [τ hai nửa], số câu được sửa)."""
    ep = sorted({k[0] for k in keys})
    random.Random(SEED).shuffle(ep)
    nua = {e: i % 2 for i, e in enumerate(ep)}
    g = {k: meta[k]["lp_edit"] - meta[k]["lp_draft"] for k in keys}

    def ap(K, t):
        return {k: (br[k] if g[k] > t else ck[k]) for k in K}

    taus, kq, sua = [], {}, 0
    for h in (0, 1):
        chon = [k for k in keys if nua[k[0]] == h]
        ap_len = [k for k in keys if nua[k[0]] != h]
        ung = sorted({g[k] for k in chon} | {float("inf")})
        t = max(ung, key=lambda t: (sum(ap(chon, t).values()), t))   # hoà thì chọn τ lớn (sửa ít hơn)
        taus.append(t)
        kq.update(ap(ap_len, t))
        sua += sum(g[k] > t and meta[k]["edit"] != meta[k]["draft"] for k in ap_len)
    return kq, taus, sua


def dong(ten, keys, ck, x, n_doi=None):
    d = {k: x[k] - ck[k] for k in keys}
    lo, hi = ktc(keys, d)
    s = sum(x.values())
    print(f"{ten:12s} exec {100*s/len(keys):6.2f} ({s}/{len(keys)}) · Δ {100*(s-sum(ck.values()))/len(keys):+6.2f} "
          f"[{lo:+.2f}; {hi:+.2f}] · cứu {sum(v > 0 for v in d.values())} phá {sum(v < 0 for v in d.values())}"
          + (f" · đổi câu {n_doi}" if n_doi is not None else ""))
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ck500", default=os.path.join(ROOT, "runs/grpo_spice/score_ck500_raw.jsonl"))
    ap.add_argument("--dir", default=os.path.join(ROOT, "runs/tage_val/that"))
    a = ap.parse_args()
    C = nap(a.ck500)
    keys = sorted(C)
    ck = {k: int(C[k]["executable"]) for k in keys}
    sai = [k for k in keys if not ck[k]]
    tro = [k for k in sai if C[k]["action_ok"]]
    print(f"ck500 exec {100*sum(ck.values())/len(keys):.2f} ({sum(ck.values())}/{len(keys)}) · sai {len(sai)} · "
          f"trỏ sai phần tử {len(tro)}")
    assert (len(keys), sum(ck.values()), len(sai), len(tro)) == (249, 165, 84, 80), "⛔ đọc sai mốc ck500 — dừng"

    kl = {}
    for ten in ("k0_lai", "gold", "neg", "none", "pred"):
        p = os.path.join(a.dir, f"score_{ten}_raw.jsonl")
        if not os.path.exists(p):
            continue
        R = nap(p)
        if set(R) != set(keys):
            print(f"{ten:12s} ⚠️ {len(R)}/249 bước — bỏ qua (lượt thử hoặc chưa chấm đủ)")
            continue
        x = {k: int(R[k]["executable"]) for k in keys}
        mp = os.path.join(a.dir, f"pred_{ten}_meta.jsonl")
        M = nap(mp) if os.path.exists(mp) else None
        n_doi = sum(M[k]["edit"] != M[k]["draft"] for k in keys) if M else None
        kl[ten] = dong(ten, keys, ck, x, n_doi)
        if ten == "k0_lai" and abs(kl[ten] - 158) > 2:
            print("⛔ k0_lai phải ra exec 158 (±2: nhiễu T4 fp16 ↔ L4 bf16) — dụng cụ chấm lệch, dừng đọc")
            return
        if M and set(M) >= set(keys):
            xg, taus, n_sua = cong(keys, ck, x, M)
            kl[ten + "+cổng"] = dong(ten + "+cổng", keys, ck, xg, n_sua)
            print(f"{'':12s} τ chọn chéo: {taus[0]:.3f} · {taus[1]:.3f}")

    loc = {}
    for p in sorted(glob.glob(os.path.join(a.dir, "loc_val_*.jsonl"))):
        L = nap(p)
        if set(L) != set(keys):
            print(f"{os.path.basename(p)}: ⚠️ {len(L)}/249 bước — bỏ qua")
            continue
        h = lambda K: sum(L[k]["hit_disk"] for k in K)
        ten = os.path.basename(p)[8:-6]
        loc[ten] = h(tro)
        print(f"bộ định vị {ten}: trúng ±14% {h(keys)}/249 · trên {len(sai)} bước sai {h(sai)} · "
              f"trên {len(tro)} bước trỏ sai {h(tro)} · không đọc được {sum(L[k]['xy'] is None for k in keys)}")

    ck0 = sum(ck.values())
    tot = lambda t: kl.get(t)
    print()
    if tot("gold") is not None and tot("neg") is not None:
        g = max(tot("gold"), tot("gold+cổng") or 0)
        if g - ck0 >= 10 and tot("gold") - tot("neg") >= 10:
            print("[V1] ĐI TIẾP: gold hơn ck500 ≥ 10 bước ròng và hơn neg ≥ 10 bước")
        elif (tot("gold+cổng") if tot("gold+cổng") is not None else tot("gold")) <= ck0 + 2.49:
            print("[V1] DỪNG TAGE: crop hoàn hảo không giúp (gold+cổng ≤ ck500 + 1 điểm)")
        else:
            print("[V1] GIỮA HAI CỘT — báo người dùng quyết")
    if loc:
        b = max(loc.values())
        print(f"[V2] bộ định vị tốt hơn trúng {b}/{len(tro)} bước trỏ sai ⇒ "
              + ("ĐI TIẾP" if b >= 20 else "cần train trên 41 nghìn bước click, báo người dùng" if b < 10
                 else "giữa hai cột, báo người dùng"))
    if tot("pred+cổng") is not None and tot("none+cổng") is not None:
        ok = tot("pred+cổng") - ck0 >= 0.015 * 249 and tot("pred+cổng") > tot("none+cổng")
        print("[V3] " + ("ĐẠT (chỉ là tín hiệu hướng, KTC ±4–5 điểm)" if ok else "chưa đạt — báo người dùng"))


if __name__ == "__main__":
    main()
