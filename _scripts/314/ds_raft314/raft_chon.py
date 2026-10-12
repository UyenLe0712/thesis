# -*- coding: utf-8 -*-
"""314 - RAFT bước 2: chọn câu đích cho mỗi câu nhắc + CỔNG (CPU, cần Java cho SPICE).

Luật (295 §4): mẫu y thay câu greedy g khi SPICE(y) ≥ SPICE(g) + 0,05 ∧ CIDEr-D(y) ≥ CIDEr-D(g)
∧ chrF(y) ≥ chrF(g) ∧ |số từ(y) − số từ(câu chuẩn)| ≤ 3. Nhiều mẫu thoả thì lấy SPICE cao nhất
(hoà thì CIDEr-D). Không mẫu nào thoả thì giữ greedy. SPICE thang 0–1 (như grpo_spice).
CỔNG: tỉ lệ câu nhắc có mẫu trội < 15% ⇒ thoát mã 2.
Ra: train_raft.jsonl {key, image, body, gold=<câu đích>, gold_nguoi, nguon} — ra_train.py học trường `gold`.

    python raft_chon.py --vao raft_mau_0.jsonl raft_mau_1.jsonl --out train_raft.jsonl --bao raft_chon.json
    python raft_chon.py --tu-kiem
"""
import os, sys, json, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
NGUONG = 0.15
DSPICE = 0.05


def nwords(s):
    import re
    return len(re.findall(r"[A-Za-z0-9'-]+", s or ""))


def diem(cau_list, gold_list, spice_fn):
    """trả (spice, cider, chrf) mỗi câu; CIDEr-D: IDF lấy từ câu chuẩn nên các lượt so được với nhau."""
    import sacrebleu
    from pycocoevalcap.cider.cider import Cider
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    tk = PTBTokenizer()
    G = tk.tokenize({i: [{"caption": g}] for i, g in enumerate(gold_list)})
    C = tk.tokenize({i: [{"caption": c if c else "none"}] for i, c in enumerate(cau_list)})
    _, cid = Cider().compute_score(G, C)
    ch = [sacrebleu.sentence_chrf(c, [g]).score for c, g in zip(cau_list, gold_list)]
    sp = spice_fn(cau_list, gold_list)
    return list(sp), [float(x) for x in cid], ch


def chon(rows, spice_fn):
    G = len(rows[0]["samples"])
    golds = [r["gold"] for r in rows]
    # một lượt SPICE cho mọi câu duy nhất (greedy + mẫu) — mẫu T=0,7 trùng nhau nhiều
    uniq = {}
    for r in rows:
        for c in [r["greedy"]] + r["samples"]:
            uniq.setdefault((c, r["gold"]), None)
    ks = list(uniq)
    sp_u = spice_fn([c if c else "none" for c, _ in ks], [g for _, g in ks])
    SP = {k: (0.0 if not k[0] else v) for k, v in zip(ks, sp_u)}
    # CIDEr theo từng cột (cùng tập câu chuẩn ⇒ cùng IDF)
    def cot(cs):
        _, cid, ch = diem(cs, golds, lambda a, b: [0.0] * len(a))
        return cid, ch
    gcid, gch = cot([r["greedy"] for r in rows])
    mcid, mch = zip(*[cot([r["samples"][j] for r in rows]) for j in range(G)])
    out, bao = [], collections.Counter()
    for i, r in enumerate(rows):
        gs = SP[(r["greedy"], r["gold"])]
        nw = nwords(r["gold"])
        tot = None
        for j, y in enumerate(r["samples"]):
            ys = SP[(y, r["gold"])]
            if not y or y == r["greedy"]:
                continue
            if (ys >= gs + DSPICE and mcid[j][i] >= gcid[i] and mch[j][i] >= gch[i]
                    and abs(nwords(y) - nw) <= 3):
                if tot is None or (ys, mcid[j][i]) > (tot[1], tot[2]):
                    tot = (y, ys, mcid[j][i])
        if tot:
            bao["doi"] += 1
            bao["dspice_sum"] += tot[1] - gs
        dich = tot[0] if tot else r["greedy"]
        if not dich:
            bao["rong_bo"] += 1
            continue
        out.append(dict(key=r["key"], image=r["image"], body=r["body"], gold=dich, gold_nguoi=r["gold"],
                        greedy=r["greedy"], nguon="mau" if tot else "greedy", action_type=r.get("action_type", "")))
    n = len(rows)
    b = dict(n_cau_nhac=n, n_doi=bao["doi"], ty_le_doi=round(bao["doi"] / n, 4),
             dspice_tb_khi_doi=round(bao["dspice_sum"] / max(1, bao["doi"]), 4), bo_rong=bao["rong_bo"],
             n_train=len(out), G=G, nguong=NGUONG)
    return out, b


def tu_kiem():
    rows = [
        dict(key="1_1", image="a", body="b", gold="Click on the search bar", greedy="Click on the search icon",
             samples=["Click on the search bar", "Tap the button", "Click on the search icon", ""]),
        dict(key="1_2", image="a", body="b", gold="Open the Clock app", greedy="Open the Clock app",
             samples=["Open the clock application now please and then wait a bit more", "Open Clock", "", "x"]),
        dict(key="1_3", image="a", body="b", gold="Click on the save button",
             greedy="Click on the button",
             samples=["Click on the save button at the top right of the screen next to the share icon", "", "", ""]),
    ]
    from difflib import SequenceMatcher
    fake = lambda cs, gs: [SequenceMatcher(None, c, g).ratio() if c else 0.0 for c, g in zip(cs, gs)]
    out, b = chon(rows, fake)
    print(b)
    d = {o["key"]: o for o in out}
    assert d["1_1"]["gold"] == "Click on the search bar" and d["1_1"]["nguon"] == "mau"
    assert d["1_2"]["gold"] == "Open the Clock app" and d["1_2"]["nguon"] == "greedy"
    assert d["1_3"]["nguon"] == "greedy", "mẫu lệch độ dài > 3 từ phải bị loại"
    assert d["1_1"]["gold_nguoi"] == "Click on the search bar"
    print("[tự kiểm] ĐẠT")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vao", nargs="+")
    ap.add_argument("--out")
    ap.add_argument("--bao")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        return tu_kiem()
    rows = [json.loads(l) for f in a.vao for l in open(f, encoding="utf-8")]
    import grpo_spice as GS
    out, b = chon(rows, GS.spice_batch)
    with open(a.out, "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    b["dat"] = b["ty_le_doi"] >= NGUONG
    json.dump(b, open(a.bao, "w"), ensure_ascii=False, indent=1)
    print("[RAFT chọn]", json.dumps(b, ensure_ascii=False), flush=True)
    for o in [o for o in out if o["nguon"] == "mau"][:8]:
        print(f"  chuẩn {o['gold_nguoi']!r}\n  greedy {o['greedy']!r}\n  → {o['gold']!r}", flush=True)
    print(f"CỔNG RAFT: {'ĐẠT' if b['dat'] else 'KHÔNG ĐẠT'} ({b['ty_le_doi']:.1%} so ngưỡng {NGUONG:.0%})", flush=True)
    sys.exit(0 if b["dat"] else 2)


if __name__ == "__main__":
    main()
