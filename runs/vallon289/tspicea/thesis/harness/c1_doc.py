# -*- coding: utf-8 -*-
"""Đọc cổng C1 (report/208 §4) trên máy nhà, CPU + Java 8 (bộ chấm COCO chính thức).

Luật đạt ghi TRƯỚC khi có số (27/9):
  (a) CIDEr-D mức kho của câu tốt nhất trong K mẫu (chọn theo CIDEr so câu chuẩn) ≥ 1,05 × CIDEr-D greedy
  (b) tỉ lệ nhóm K mẫu có CIDEr từng câu y hệt nhau (độ lệch chuẩn = 0) ≤ 50%
  Cả hai đạt ⇒ C1 ĐẠT. Trượt một ⇒ không đặt lượt GRPO/lọc-mẫu nào.
⚠️ Val là dữ liệu S1 đã thấy lúc dạy ⇒ greedy được ghi nhớ làm đẹp ⇒ luật (a) thiên vị CHỐNG lại việc
đạt. Không trích con số nào ra báo.
Chạy:  ~/.venvs/thesis/bin/python harness/c1_doc.py runs/c1/c1_mau.jsonl
"""
import glob, json, os, sys, statistics

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.cider.cider import Cider


def main(path):
    D = [json.loads(l) for l in open(path, encoding="utf-8")]
    n, K = len(D), len(D[0]["mau"])
    tk = PTBTokenizer()
    g = tk.tokenize({i: [{"caption": d["gold"]}] for i, d in enumerate(D)})
    gr = tk.tokenize({i: [{"caption": d["greedy"]}] for i, d in enumerate(D)})
    ms = [tk.tokenize({i: [{"caption": d["mau"][k]}] for i, d in enumerate(D)}) for k in range(K)]

    def kho(c):
        b, _ = Bleu(4).compute_score(g, c, verbose=0)
        ci, per = Cider().compute_score(g, c)
        return 100 * b[3], 100 * ci, list(per)

    b_g, c_g, per_g = kho(gr)
    per_m = [kho(m)[2] for m in ms]
    best = {i: ms[max(range(K), key=lambda k: per_m[k][i])][i] for i in range(n)}
    b_b, c_b, _ = kho(best)
    tb_m = statistics.mean(kho(m)[1] for m in ms)
    std0 = sum(len({round(per_m[k][i], 9) for k in range(K)}) == 1 for i in range(n)) / n
    same_str = sum(len(set(d["mau"])) == 1 for d in D) / n
    distinct = statistics.mean(len(set(d["mau"])) for d in D)
    greedy_in = sum(d["greedy"] in d["mau"] for d in D) / n

    print(f"n={n} bước · K={K}")
    print(f"greedy          BLEU-4 {b_g:.2f} · CIDEr-D {c_g:.1f}")
    print(f"mẫu (trung bình) CIDEr-D {tb_m:.1f}")
    print(f"best-of-{K}       BLEU-4 {b_b:.2f} · CIDEr-D {c_b:.1f}  (= {c_b/c_g:.3f} × greedy)")
    print(f"nhóm std(CIDEr)=0: {100*std0:.1f}% · nhóm {K} câu y hệt: {100*same_str:.1f}% · "
          f"số câu khác nhau TB/nhóm: {distinct:.2f} · greedy nằm trong mẫu: {100*greedy_in:.1f}%")
    a_ok, b_ok = c_b >= 1.05 * c_g, std0 <= 0.50
    print(f"(a) best-of-{K} ≥ 1,05×greedy: {'ĐẠT' if a_ok else 'KHÔNG ĐẠT'} · "
          f"(b) std0 ≤ 50%: {'ĐẠT' if b_ok else 'KHÔNG ĐẠT'}")
    print("C1 =", "ĐẠT" if a_ok and b_ok else "KHÔNG ĐẠT")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "runs/c1/c1_mau.jsonl")
