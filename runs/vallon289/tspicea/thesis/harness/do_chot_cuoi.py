# -*- coding: utf-8 -*-
"""Phụ lục A — tái lập mọi con số của bản chốt cuối. Chạy từ GỐC kho, 0 GPU, ~2 phút.

    PYTHONIOENCODING=utf-8 python3 harness/do_chot_cuoi.py

Hai mục:
  A. điểm mọi nhánh dưới BỐN luật chấm, kèm cột action_ok
  B. khoảng tin cậy GHÉP CẶP cho từng so sánh (bootstrap theo cụm tác vụ) + hiệu chỉnh Holm

⛔ Bootstrap phải lấy mẫu theo CỤM (episode), không theo bước: các bước cùng một tác vụ không độc
   lập, lấy mẫu theo bước sẽ cho khoảng tin cậy hẹp giả tạo.
⛔ Mọi phép so là GHÉP CẶP trên cùng tập bước. Sai số của hiệu nhỏ hơn sai số của hai con số
   tuyệt đối cộng lại, vì hai nhánh gặp đúng những bước khó nên phần nhiễu chung triệt tiêu.
"""
import functools, json, math, os, random, statistics as st
# ⛔ Chạy nền hoặc chuyển hướng ra tệp thì Python đệm stdout 8 KB: không thấy dòng nào
#    suốt nhiều phút và dễ đọc nhầm thành treo. Xả đệm mọi lần in.
print = functools.partial(print, flush=True)

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda p: os.path.join(HERE, "..", "runs", p)
DUNG_SAI = 0.14

NHANH = [("Base", "score_base_raw.jsonl"),
         ("S2/101", "score_s2_seed101_raw.jsonl"),
         ("gui_sel/101", "sel/score_gui_sel_seed101_raw.jsonl"),
         ("CE2-S2/101", "score_ce2_s2_seed101_raw.jsonl"),
         ("S1/101", "score_s1_seed101_raw.jsonl"),
         ("S1/202", "score_s1_seed202_raw.jsonl"),
         ("MIN-DESC/101", "score_min_desc_seed101_raw.jsonl"),
         ("GRPO-point/101", "grpo_point/score_grpo_point_seed101_raw.jsonl"),
         ("Câu chuẩn (trần)", "score_ceiling_human_raw.jsonl")]

CAP = [("MIN-DESC/101", "S1/101"), ("GRPO-point/101", "S1/101"),
       ("GRPO-point/101", "S1/202"), ("S1/202", "S1/101"),
       ("GRPO-point/101", "MIN-DESC/101"), ("MIN-DESC/101", "CE2-S2/101"),
       ("CE2-S2/101", "S2/101"), ("GRPO-point/101", "Base")]


def nap(p):
    o = {}
    for l in open(R(p), encoding="utf-8"):
        l = l.strip()
        if l:
            r = json.loads(l)
            for k in ("executable", "action_ok", "toggle_ok", "hit_disk"):
                r.setdefault(k, 0)
            o[(r["episode_id"], r["step_id"])] = r
    return o


I = lambda r, f: int(r.get(f, 0) or 0)
AO = lambda r: I(r, "action_ok") * I(r, "toggle_ok")


def truc14(r):
    """±14% theo TỪNG TRỤC — trùng đúng trường hit_disk đã lưu."""
    p, g, wh = r.get("pred_xy"), r.get("gold_xy"), r.get("wh")
    if not (p and g and wh):
        return 0
    return int(abs(p[0] - g[0]) <= DUNG_SAI * wh[0] and abs(p[1] - g[1]) <= DUNG_SAI * wh[1])


def aitw(r):
    """AitW: Euclid trên toạ độ chuẩn hoá theo TỪNG CHIỀU về [0,1], ngưỡng 0,14."""
    p, g, wh = r.get("pred_xy"), r.get("gold_xy"), r.get("wh")
    if not (p and g and wh):
        return 0
    return int(math.hypot((p[0] - g[0]) / wh[0], (p[1] - g[1]) / wh[1]) <= DUNG_SAI)


LUAT = [("exec Voronoi (tiêu đề)", lambda r: I(r, "executable")),
        ("AO x ±14% từng trục", lambda r: AO(r) * truc14(r)),
        ("AO x AitW Euclid", lambda r: AO(r) * aitw(r)),
        ("hit_disk KHÔNG gated", lambda r: I(r, "hit_disk"))]


def boot(D, K, EPS, a, b, f, B=4000, seed=17):
    rd = random.Random(seed)
    ep = list(EPS)
    d0 = st.mean([f(D[a][x]) for x in K]) - st.mean([f(D[b][x]) for x in K])
    out = []
    for _ in range(B):
        s = n = 0
        for e in (rd.choice(ep) for _ in ep):
            for x in EPS[e]:
                s += f(D[a][x]) - f(D[b][x])
                n += 1
        out.append(s / n)
    out.sort()
    se = st.pstdev(out)
    z = d0 / se if se else 0.0
    p = 2 * (1 - .5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return 100 * d0, 100 * se, 100 * out[int(.025 * B)], 100 * out[int(.975 * B)], p


def main():
    D = {}
    for ten, tep in NHANH:
        if os.path.exists(R(tep)):
            D[ten] = nap(tep)
        else:
            print(f"  (thiếu {tep} — bỏ qua {ten})")
    K = sorted(set.intersection(*[set(v) for v in D.values()]))
    EPS = {}
    for x in K:
        EPS.setdefault(x[0], []).append(x)
    print(f"Quần thể n={len(K)} bước / {len(EPS)} tác vụ\n")

    print("=" * 96)
    print("A. ĐIỂM MỌI NHÁNH DƯỚI BỐN LUẬT — chú ý cột action_ok")
    print("=" * 96)
    # ⚠️ Cột đầu là action_ok THUẦN (câu chuẩn phải ra đúng 100,00), không nhân toggle_ok.
    #    Nhân vào thì câu chuẩn còn 99,93 và mọi hàng lệch ~0,1 pp so với bản đã công bố.
    print(f"  {'nhánh':<18}{'action_ok':>10}" + "".join(f"{t:>24}" for t, _ in LUAT))
    ao = {}
    for ten in D:
        d = D[ten]
        ao[ten] = 100 * st.mean([I(d[x], "action_ok") for x in K])
        print(f"  {ten:<18}{ao[ten]:>10.2f}"
              + "".join(f"{100*st.mean([f(d[x]) for x in K]):>24.2f}" for _, f in LUAT))
    ho = [t for t in ("CE2-S2/101", "MIN-DESC/101", "GRPO-point/101") if t in ao]
    print(f"\n  \u2b50 S1/101 action_ok = {ao['S1/101']:.2f} c\u00f2n h\u1ecd <desc> ~"
          f"{st.mean([ao[t] for t in ho]):.2f}: kh\u1ed1i khai b\u00e1o g\u1ea7n nh\u01b0 "
          f"xo\u00e1 h\u1eb3n hi\u1ec7n t\u01b0\u1ee3ng l\u1eabn lo\u1ea1i thao t\u00e1c.")

    print("\n" + "=" * 96)
    print("B. KHOẢNG TIN CẬY 95% GHÉP CẶP (bootstrap cụm tác vụ, B=4000) + HOLM")
    print("=" * 96)
    P = {}
    for a, b in CAP:
        if a not in D or b not in D:
            continue
        print(f"  {a} − {b}")
        for tl, f in LUAT:
            d, se, lo, hi, p = boot(D, K, EPS, a, b, f)
            P[(a, b, tl)] = p
            print(f"      {tl:<24}{d:>+7.2f}  SE={se:.3f}  KTC[{lo:>+6.2f} · {hi:>+6.2f}]"
                  f"  p={p:.4f} {'loại 0' if lo*hi > 0 else 'TRẮNG'}")

    print("\n  ⭐ HOLM cho GRPO − S1/101 trên ba luật có cùng loại thao tác:")
    bo = [t for t, _ in LUAT[:3]]
    ps = sorted(((P[("GRPO-point/101", "S1/101", t)], t) for t in bo if
                 ("GRPO-point/101", "S1/101", t) in P))
    gh = False
    for i, (p, t) in enumerate(ps):
        ng = .05 / (len(ps) - i)
        ok = (p <= ng) and not gh
        gh = gh or not ok
        print(f"      {t:<24} p={p:.4f}  ngưỡng={ng:.4f}  {'GIỮ' if ok else 'MẤT'} ý nghĩa")


if __name__ == "__main__":
    main()
