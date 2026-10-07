# -*- coding: utf-8 -*-
"""Đọc G0 của TFVF (report/237 §5) trên máy nhà, CPU + Java 8 (bộ chấm COCO chính thức).

Luật đạt ghi TRƯỚC khi có số (report/237, 28/9), đọc trên 249 bước click, ba thước quyết định là
BLEU-4 · CIDEr-D · SPICE (BLEU-1..3 không tính thành thước độc lập):
  (1) kênh có tác dụng        câu G khác câu O ở ≥ 10% số bước
  (2) đúng chỗ hơn sai chỗ    G > F ở ≥ 2/3 thước  VÀ  CIDEr-D(G) − CIDEr-D(F) ≥ 3
  (3) hơn prior tâm màn       G > C ở ≥ 2/3 thước
  (4) focus hoàn hảo có ích   G ≥ O ở cả 3 thước  VÀ  G > O ở ≥ 2/3 thước
  Đạt cả bốn ⇒ GO. Không nới sau khi thấy số.
Bảng 400 bước (bước không click giữ câu O cho mọi chế độ) chỉ để xem độ pha loãng, không dùng để quyết.
⚠️ Val là dữ liệu S1 đã thấy lúc dạy ⇒ câu O được ghi nhớ làm đẹp ⇒ điều (4) thiên vị CHỐNG lại việc
đạt. Không trích con số nào ra báo hay luận văn.

Chạy:  ~/.venvs/thesis/bin/python harness/tfvf_g0_doc.py <tfvf_g0.jsonl> [runs/c1/c1_mau.jsonl]
          [--json runs/tfvf_g0/g0_doc.json] [--bo-spice]
"""
import argparse, glob, json, os

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

MODES = ["O", "G", "F", "C"]
TRUONG = {"G": "gold_focus", "F": "false_focus", "C": "center_focus"}
QUYET = ["bleu4", "cider_d", "spice"]
COT = ["bleu1", "bleu2", "bleu3", "bleu4", "meteor", "rougeL", "cider_d", "spice"]


def cham(gold, hyp, bo_spice):
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": r}] for i, r in enumerate(gold)})
    c = tk.tokenize({i: [{"caption": h}] for i, h in enumerate(hyp)})
    o = {}
    b, _ = Bleu(4).compute_score(g, c, verbose=0)
    for k in range(4):
        o[f"bleu{k+1}"] = 100 * b[k]
    o["meteor"] = 100 * Meteor().compute_score(g, c)[0]
    o["rougeL"] = 100 * Rouge().compute_score(g, c)[0]
    o["cider_d"] = 100 * Cider().compute_score(g, c)[0]
    o["spice"] = float("nan") if bo_spice else 100 * Spice().compute_score(g, c)[0]
    return o


def in_bang(ten, n, S):
    print(f"\n=== {ten} (n={n}) ===")
    print("chế độ " + " ".join(f"{c:>8s}" for c in COT))
    for m in MODES:
        print(f"{m:6s} " + " ".join(f"{S[m][c]:8.2f}" for c in COT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kq")
    ap.add_argument("c1", nargs="?", default="runs/c1/c1_mau.jsonl")
    ap.add_argument("--json")
    ap.add_argument("--bo-spice", action="store_true", help="chỉ để thử đường đọc; quyết định cần SPICE")
    a = ap.parse_args()

    C1 = [json.loads(l) for l in open(a.c1, encoding="utf-8")]
    K = [json.loads(l) for l in open(a.kq, encoding="utf-8")]
    assert len(C1) == 400 and len({(d["episode_id"], d["step_id"]) for d in C1}) == 400, "C1 phải 400 khoá riêng"
    ck = [d for d in C1 if d["action_type"] == "click"]
    assert len(ck) == 249, f"C1 phải có 249 click, thấy {len(ck)}"
    kq = {(d["episode_id"], d["step_id"]): d for d in K}
    assert len(kq) == len(K), "tệp kết quả có khoá trùng"
    thieu = [(d["episode_id"], d["step_id"]) for d in ck if (d["episode_id"], d["step_id"]) not in kq]
    assert not thieu, f"thiếu {len(thieu)}/249 bước click, ví dụ {thieu[:3]} — chạy nối tiếp cho đủ"
    assert set(kq) == {(d["episode_id"], d["step_id"]) for d in ck}, "tệp kết quả có khoá ngoài 249 click"
    for d in ck:
        r = kq[(d["episode_id"], d["step_id"])]
        assert r["gold"] == d["gold"], f"câu chuẩn lệch ở {(d['episode_id'], d['step_id'])}"
        for t in TRUONG.values():
            assert isinstance(r.get(t), str), f"thiếu trường {t} ở {(d['episode_id'], d['step_id'])}"
    print(f"[khớp] 400 khoá C1 · 249 click · kết quả {len(K)} dòng · câu chuẩn khớp tuyệt đối 249/249")

    def cau(d, m):
        if m == "O" or d["action_type"] != "click":
            return d["greedy"]
        return kq[(d["episode_id"], d["step_id"])][TRUONG[m]]

    rong = {m: sum(not cau(d, m) for d in ck) for m in MODES}
    print("câu rỗng trên 249 click:", rong)

    kqua = {}
    for ten, tap in [("249 click", ck), ("400 bước (không click giữ O)", C1)]:
        gold = [d["gold"] for d in tap]
        S = {m: cham(gold, [cau(d, m) for d in tap], a.bo_spice) for m in MODES}
        in_bang(ten, len(tap), S)
        kqua[ten] = S

    khac = {f"G≠{m}": sum(cau(d, "G") != cau(d, m) for d in ck) for m in ["O", "F", "C"]}
    print("\nsố bước câu khác nhau (249 click): " +
          " · ".join(f"{k} {v} ({100*v/249:.1f}%)" for k, v in khac.items()))

    S = kqua["249 click"]
    hon = lambda p, q: sum(S[p][c] > S[q][c] for c in QUYET)
    dk1 = khac["G≠O"] / 249 >= 0.10
    dk2 = hon("G", "F") >= 2 and S["G"]["cider_d"] - S["F"]["cider_d"] >= 3
    dk3 = hon("G", "C") >= 2
    dk4 = all(S["G"][c] >= S["O"][c] for c in QUYET) and hon("G", "O") >= 2
    print("\nĐiều kiện GO (249 click; thước quyết định BLEU-4 · CIDEr-D · SPICE):")
    print(f"  (1) G≠O ≥ 10%: {100*khac['G≠O']/249:.1f}% ⇒ {'ĐẠT' if dk1 else 'KHÔNG ĐẠT'}")
    print(f"  (2) G>F ở {hon('G','F')}/3 thước, ΔCIDEr-D(G−F) = {S['G']['cider_d']-S['F']['cider_d']:+.2f} ⇒ "
          f"{'ĐẠT' if dk2 else 'KHÔNG ĐẠT'}")
    print(f"  (3) G>C ở {hon('G','C')}/3 thước ⇒ {'ĐẠT' if dk3 else 'KHÔNG ĐẠT'}")
    print(f"  (4) G≥O cả 3: {all(S['G'][c] >= S['O'][c] for c in QUYET)} · G>O ở {hon('G','O')}/3 ⇒ "
          f"{'ĐẠT' if dk4 else 'KHÔNG ĐẠT'}")
    if dk1 and dk2 and dk3 and dk4:
        phan = "GO — TFVF phù hợp; được thiết kế pilot có train"
    elif not dk1:
        phan = "DỪNG — S1 gần như không phản ứng với renderer (trượt 1)"
    elif not (dk2 and dk3):
        phan = "DỪNG — S1 phản ứng với biến đổi ảnh nhưng không theo đúng vị trí (trượt 2 hoặc 3)"
    else:
        phan = "DỪNG — focus chứa tín hiệu nhưng lệch phân phối làm hại S1 (trượt 4); không tự mở SFT để cứu"
    print("\nG0 =", phan)
    if a.bo_spice:
        print("⚠️ chạy --bo-spice: SPICE = nan nên phán quyết trên KHÔNG hợp lệ, chỉ để thử đường đọc")

    if a.json:
        os.makedirs(os.path.dirname(a.json) or ".", exist_ok=True)
        kqua = {t: {m: {c: float(v) for c, v in s.items()} for m, s in S_.items()} for t, S_ in kqua.items()}
        json.dump({"bang": kqua, "khac": khac, "dieu_kien": [bool(x) for x in (dk1, dk2, dk3, dk4)],
                   "phan_quyet": phan,
                   "bo_spice": a.bo_spice, "nguon": [a.kq, a.c1]},
                  open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ghi", a.json)


if __name__ == "__main__":
    main()
