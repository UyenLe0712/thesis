# -*- coding: utf-8 -*-
"""Bộ chọn câu nhận biết chuyển trạng thái (report/232) — lượt smoke CPU, 0 GPU, không ảnh, không adapter.

S1 đóng băng là bộ sinh. Ở đây chỉ train hai bộ xếp hạng nhỏ (hai lớp Linear, CPU):
  · teacher  : goal + history ngắn + tên phần tử màn HIỆN TẠI + tên phần tử màn SAU + câu ứng viên
  · student  : như teacher nhưng KHÔNG có màn sau
Ba hàng bắt buộc trên cùng tập câu (greedy + 8 mẫu S1 của runs/c1/c1_mau.jsonl):
  hàng 1  S1 greedy
  hàng 2  student chỉ học câu dương/câu âm từ màn hiện tại (không distill)
  hàng 3  student distill thứ hạng của teacher (phương pháp đề xuất; lúc chấm không xem màn sau)
Dòng "teacher" in thêm chỉ để chẩn đoán (dùng màn sau lúc chọn ⇒ KHÔNG hợp lệ lúc chạy, không so tiêu chí).

Luật đạt ghi TRƯỚC khi chạy (report/232 §0, §1, §5), không đổi sau khi thấy số:
  (1) hàng 3 > hàng 1 đồng thời ở BLEU-4, CIDEr-D, SPICE
  (2) hàng 3 > hàng 2 ở ít nhất 2/3 thước đó
  Đạt cả hai ⇒ mới sinh 8 câu S1 trên 4.463 bước test (Kaggle T4). Trượt (1) ⇒ dừng, ghi kết quả âm.
⚠️ 400 bước smoke là val mà S1 đã thấy lúc train ⇒ số val CẤM trích ra báo, chỉ để quyết lượt 2.
Hạt giống cố định 101 (quy ước dự án), chạy một lần.

Dữ liệu: train chỉ lấy bước click thuộc train_tru_val.jsonl có bản ghi bước kế (cùng episode, step+1).
Câu âm: câu chuẩn của 4 bước click KHÁC episode có nhiều tên phần tử trùng màn hiện tại nhất.
Loss: margin ranking 0,2. Distill: cặp câu âm xếp theo điểm teacher, student học đúng thứ tự đó.
Lúc chọn: nhóm = greedy + mẫu; lấy điểm student cao nhất, hoà thì giữ greedy.

Chạy:  ~/.venvs/thesis/bin/python harness/selector_man_sau.py [--mau runs/c1/c1_mau.jsonl]
Ghi:   runs/selector_man_sau/ket_qua_smoke.json · chon_smoke.jsonl
"""
import argparse, ast, glob, json, os, random, re, time, zlib
import numpy as np
from scipy import sparse
import torch
import torch.nn as nn

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.spice.spice import Spice

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DATA = ROOT + "harness/dg1_cache/train_ac/"
SEED, NNEG, MARGIN, HB, HID, EPOCH, BATCH, LR = 101, 4, 0.2, 2 ** 15, 64, 5, 256, 2e-3

SW = set("the a an on in of to at for and or with from your you this that is it by as into click tap "
         "press select open option button icon go back type enter search then now screen".split())
POS = {"top", "bottom", "left", "right", "upper", "lower", "corner", "center", "middle"}
NONCLICK = {"swipe", "scroll", "type", "enter", "back", "wait", "home", "long", "hold", "input"}
w = lambda s: re.findall(r"[a-z0-9]+", (s or "").lower())
cw = lambda s: {t for t in w(s) if t not in SW and len(t) > 1}
key = lambda d: (str(d["episode_id"]), str(d["step_id"]))


def rd(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def atype(a):
    if isinstance(a, dict):
        return a["action_type"]
    try:
        return ast.literal_eval(a)["action_type"]
    except Exception:
        return json.loads(a)["action_type"]


def lit(s):
    if isinstance(s, list):
        return s
    try:
        return ast.literal_eval(s)
    except Exception:
        return []


# ---------- ngữ cảnh một bước ----------
class Ctx:
    def __init__(self, rec, cand, nxt=None):
        self.goal = cw(rec.get("goal", ""))
        h = lit(rec.get("history", "[]"))
        self.hist = cw(h[-1]) if h else set()
        self.names = self._names(cand)
        self.tok = set().union(*[n[1] for n in self.names]) if self.names else set()
        self.nxt = None
        if nxt is not None:
            nn_ = self._names(nxt)
            cur = {n[0] for n in self.names}
            nx = {n[0] for n in nn_}
            self.nxt_tok = set().union(*[n[1] for n in nn_]) if nn_ else set()
            self.new = [n for n in nn_ if n[0] not in cur]
            self.new_tok = set().union(*[n[1] for n in self.new]) if self.new else set()
            gone = [n for n in self.names if n[0] not in nx]
            self.gone_tok = set().union(*[n[1] for n in gone]) if gone else set()
            self.nxt = True

    @staticmethod
    def _names(cand):
        out, seen = [], set()
        for c in lit(cand.get("cands", "[]")) if cand else []:
            nm = (c.get("name") or "").strip().lower()
            if len(nm) < 2 or nm in seen:
                continue
            seen.add(nm)
            out.append((nm, cw(nm)))
        return out


def name_feats(c_low, c_cw, names):
    cov = [len(c_cw & t) / len(t) for _, t in names if t]
    full = sum(1 for _, t in names if t and t <= c_cw)
    sub = any(len(n) >= 3 and n in c_low for n, _ in names)
    return [max(cov) if cov else 0.0, 1.0 if full else 0.0, min(full, 5) / 5, 1.0 if sub else 0.0]


def frac(a, b):
    return len(a & b) / len(a) if a else 0.0


def feats(sent, ctx, teacher):
    """(chỉ số băm uni+bigram của câu, vector đặc trưng dày). Teacher thêm 6 đặc trưng màn sau."""
    t = w(sent)
    c_cw = cw(sent)
    c_low = " ".join(t)
    grams = t + [a + "_" + b for a, b in zip(t, t[1:])]
    idx = sorted({zlib.crc32(g.encode()) % HB for g in grams}) or [0]
    d = [len(t) / 20, len(c_cw) / 10,
         frac(c_cw, ctx.tok), frac(c_cw, ctx.goal), frac(c_cw, ctx.hist),
         frac(c_cw, ctx.goal - ctx.tok),
         1.0 if set(t) & POS else 0.0,
         1.0 if t and t[0] in {"click", "tap", "select", "press", "choose"} else 0.0,
         1.0 if set(t) & NONCLICK else 0.0]
    d += name_feats(c_low, c_cw, ctx.names)
    if teacher:
        d += [frac(c_cw, ctx.nxt_tok), frac(c_cw, ctx.new_tok), frac(c_cw, ctx.gone_tok)]
        d += name_feats(c_low, c_cw, ctx.new)[:3]
    return idx, d


ND_S, ND_T = 13, 19


class Ranker(nn.Module):
    """Hai lớp Linear: lớp 1 = EmbeddingBag (Linear trên vector băm thưa) + Linear dày, ReLU, lớp 2."""

    def __init__(self, nd):
        super().__init__()
        self.emb = nn.EmbeddingBag(HB, HID, mode="sum")
        self.lin = nn.Linear(nd, HID)
        self.out = nn.Linear(HID, 1)

    def forward(self, flat, offs, dense):
        return self.out(torch.relu(self.emb(flat, offs) + self.lin(dense))).squeeze(-1)


def pack(items):
    flat, offs, dense = [], [], []
    for idx, d in items:
        offs.append(len(flat))
        flat += idx
        dense.append(d)
    return torch.tensor(flat), torch.tensor(offs), torch.tensor(dense, dtype=torch.float32)


def score(model, items, bs=4096):
    model.eval()
    out = []
    with torch.no_grad():
        for i in range(0, len(items), bs):
            out.append(model(*pack(items[i:i + bs])))
    return torch.cat(out)


def train(nd, X, T_order=None, tag=""):
    """X[i] = 1 + NNEG mục (dương trước). T_order[i] = cặp (a, b) câu âm, teacher xếp a > b."""
    torch.manual_seed(SEED)
    rng = random.Random(SEED)
    m = Ranker(nd)
    opt = torch.optim.Adam(m.parameters(), lr=LR)
    order = list(range(len(X)))
    for ep in range(EPOCH):
        m.train()
        rng.shuffle(order)
        tot, t0 = 0.0, time.time()
        for b in range(0, len(order), BATCH):
            ids = order[b:b + BATCH]
            s = m(*pack([it for i in ids for it in X[i]])).view(len(ids), 1 + NNEG)
            loss = torch.relu(MARGIN - (s[:, :1] - s[:, 1:])).mean()
            if T_order is not None:
                pa = [(r, 1 + a, 1 + bb) for r, i in enumerate(ids) for a, bb in T_order[i]]
                if pa:
                    r_, a_, b_ = map(torch.tensor, zip(*pa))
                    loss = loss + torch.relu(MARGIN - (s[r_, a_] - s[r_, b_])).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            tot += loss.item() * len(ids)
        print(f"  [{tag}] epoch {ep+1}/{EPOCH} loss {tot/len(order):.4f} ({time.time()-t0:.0f} s)", flush=True)
    return m


def mine_negatives(steps, names_of, ep_of, gold_of):
    """4 câu âm/bước: bước click khác episode có nhiều tên phần tử trùng màn hiện tại nhất."""
    vocab = {}
    rows, cols = [], []
    for i, s in enumerate(steps):
        for nm in names_of[s]:
            j = vocab.setdefault(nm, len(vocab))
            rows.append(i)
            cols.append(j)
    M = sparse.csr_matrix((np.ones(len(rows), np.float32), (rows, cols)), shape=(len(steps), len(vocab)))
    MT = M.T.tocsr()
    eps = np.array([ep_of[s] for s in steps])
    golds = np.array([gold_of[s] for s in steps])
    rng = np.random.default_rng(SEED)
    neg = []
    for a in range(0, len(steps), 1000):
        C = (M[a:a + 1000] @ MT).toarray()
        C += rng.random(C.shape, dtype=np.float32) * 1e-3   # phá hoà ngẫu nhiên có hạt giống
        for r in range(C.shape[0]):
            i = a + r
            C[r, eps == eps[i]] = -1.0
            C[r, golds == golds[i]] = -1.0
            top = np.argpartition(-C[r], NNEG)[:NNEG]
            neg.append(list(top[np.argsort(-C[r, top])]))
    return neg


def coco(gold, hyp):
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": x}] for i, x in enumerate(gold)})
    c = tk.tokenize({i: [{"caption": x}] for i, x in enumerate(hyp)})
    o = {}
    b, _ = Bleu(4).compute_score(g, c, verbose=0)
    for k in range(4):
        o[f"bleu{k+1}"] = round(float(100 * b[k]), 2)
    o["meteor"] = round(float(100 * Meteor().compute_score(g, c)[0]), 2)
    o["rougeL"] = round(float(100 * Rouge().compute_score(g, c)[0]), 2)
    o["cider_d"] = round(float(100 * Cider().compute_score(g, c)[0]), 2)
    o["spice"] = round(float(100 * Spice().compute_score(g, c)[0]), 2)
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mau", default="runs/c1/c1_mau.jsonl")
    ap.add_argument("--outdir", default="runs/selector_man_sau")
    a = ap.parse_args()
    t0 = time.time()
    random.seed(SEED)
    np.random.seed(SEED)

    tr = {key(d): d for d in rd(DATA + "train.jsonl")}
    cand = {key(d): d for d in rd(DATA + "candidates.jsonl")}
    tv = {key(d) for d in rd(DATA + "train_tru_val.jsonl")}
    nxt = lambda k: (k[0], str(int(k[1]) + 1))
    steps = sorted(k for k in tv if atype(tr[k]["action"]) == "click" and nxt(k) in tr)
    print(f"[dữ liệu] train {len(tr)} · train_tru_val {len(tv)} · click có bước kế trong train_tru_val "
          f"{len(steps)}", flush=True)

    ctxS = {k: Ctx(tr[k], cand.get(k)) for k in steps}
    ctxT = {k: Ctx(tr[k], cand.get(k), cand.get(nxt(k), {})) for k in steps}
    names_of = {k: [n for n, _ in ctxS[k].names] for k in steps}
    neg = mine_negatives(steps, names_of, {k: k[0] for k in steps},
                         {k: " ".join(w(tr[k]["target_instruction"])) for k in steps})
    print(f"[câu âm] xong ({time.time()-t0:.0f} s) · ví dụ: {tr[steps[0]]['target_instruction']!r} ↔ "
          f"{[tr[steps[j]]['target_instruction'] for j in neg[0][:2]]}", flush=True)

    sents = [[tr[k]["target_instruction"]] + [tr[steps[j]]["target_instruction"] for j in neg[i]]
             for i, k in enumerate(steps)]
    XS = [[feats(s, ctxS[k], False) for s in sents[i]] for i, k in enumerate(steps)]
    XT = [[feats(s, ctxT[k], True) for s in sents[i]] for i, k in enumerate(steps)]
    assert len(XS[0][0][1]) == ND_S and len(XT[0][0][1]) == ND_T
    print(f"[đặc trưng] xong ({time.time()-t0:.0f} s)", flush=True)

    teacher = train(ND_T, XT, tag="teacher")
    ts = score(teacher, [it for x in XT for it in x]).view(len(XT), 1 + NNEG)
    T_order = [[(p, q) for p in range(NNEG) for q in range(NNEG) if ts[i, 1 + p] > ts[i, 1 + q]]
               for i in range(len(XT))]
    ss_plain = train(ND_S, XS, tag="student-không-distill (hàng 2)")
    ss_dist = train(ND_S, XS, T_order=T_order, tag="student-distill (hàng 3)")
    acc = lambda s: (s[:, :1] > s[:, 1:]).float().mean().item()
    tr_acc = {"teacher": acc(ts)}
    for nm, m in [("hang2", ss_plain), ("hang3", ss_dist)]:
        tr_acc[nm] = acc(score(m, [it for x in XS for it in x]).view(len(XS), 1 + NNEG))
    print(f"[độ đúng cặp trên tập dạy, chẩn đoán] " + " · ".join(f"{k} {v:.3f}" for k, v in tr_acc.items()),
          flush=True)

    # ---------- chọn câu trên 400 bước smoke ----------
    D = rd(ROOT + a.mau)
    assert not any(key(d) in tv for d in D), "bước smoke lẫn vào tập dạy"
    rows = {"hang1_greedy": [], "hang2_student_khong_distill": [], "hang3_student_distill": [],
            "chan_doan_teacher_xem_man_sau": []}
    log = []
    for d in D:
        k = key(d)
        grp = [d["greedy"]] + list(d["mau"])
        cS = Ctx(tr[k], cand.get(k))
        cT = Ctx(tr[k], cand.get(k), cand.get(nxt(k), {}))
        pick = {}
        for nm, m, c, t in [("hang2_student_khong_distill", ss_plain, cS, False),
                            ("hang3_student_distill", ss_dist, cS, False),
                            ("chan_doan_teacher_xem_man_sau", teacher, cT, True)]:
            s = score(m, [feats(x, c, t) for x in grp]).tolist()
            best = 0
            for j in range(1, len(grp)):
                if s[j] > s[best]:   # hoà thì giữ greedy (chỉ số 0)
                    best = j
            pick[nm] = grp[best]
        rows["hang1_greedy"].append(d["greedy"])
        for nm in pick:
            rows[nm].append(pick[nm])
        log.append({"episode_id": d["episode_id"], "step_id": d["step_id"], "gold": d["gold"],
                    "greedy": d["greedy"], **pick})
    gold = [d["gold"] for d in D]
    res = {}
    for nm, hyp in rows.items():
        res[nm] = coco(gold, hyp)
        res[nm]["doi_khoi_greedy"] = sum(h != g for h, g in zip(hyp, rows["hang1_greedy"]))
        print(f"{nm:32s} " + " · ".join(f"{k} {v}" for k, v in res[nm].items()), flush=True)

    ba = ["bleu4", "cider_d", "spice"]
    h1, h2, h3 = res["hang1_greedy"], res["hang2_student_khong_distill"], res["hang3_student_distill"]
    dk1 = bool(all(h3[m] > h1[m] for m in ba))
    dk2 = bool(sum(h3[m] > h2[m] for m in ba) >= 2)
    ket = "ĐẠT" if dk1 and dk2 else "KHÔNG ĐẠT"
    print(f"(1) hàng 3 > hàng 1 cả BLEU-4/CIDEr-D/SPICE: {'ĐẠT' if dk1 else 'KHÔNG ĐẠT'} · "
          f"(2) hàng 3 > hàng 2 ở ≥2/3: {'ĐẠT' if dk2 else 'KHÔNG ĐẠT'} ⇒ SMOKE {ket}", flush=True)
    if dk1 and not dk2:
        print("   ⇒ chỉ được nói 'selector học được có ích', chưa quy công cho màn sau", flush=True)

    os.makedirs(ROOT + a.outdir, exist_ok=True)
    json.dump({"n": len(D), "seed": SEED, "n_train_steps": len(steps), "acc_cap_tap_day": tr_acc,
               "ket_qua": res, "dieu_kien_1": dk1, "dieu_kien_2": dk2, "smoke": ket,
               "canh_bao": "val S1 đã thấy lúc train — cấm trích số ra báo",
               "exec": "không tính được trên CPU (cần bộ trỏ UGround)"},
              open(ROOT + a.outdir + "/ket_qua_smoke.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(ROOT + a.outdir + "/chon_smoke.jsonl", "w", encoding="utf-8") as f:
        for r in log:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"ghi {a.outdir}/ · tổng {time.time()-t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
