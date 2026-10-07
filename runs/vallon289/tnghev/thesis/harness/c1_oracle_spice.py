# -*- coding: utf-8 -*-
"""Tính lại lựa chọn của oracle SPICE trên 400 bước C1 (report 251 §1), CPU + Java 8.

Với mỗi bước, trong 9 câu (0 = greedy, 1..8 = mau[k-1]) chọn câu có SPICE từng câu cao nhất
so với câu chuẩn; hoà thì lấy chỉ số nhỏ nhất (greedy thắng khi hoà).
Ghi runs/c1/c1_picks.json = {"picks": "<400 ký tự>", ...} để notebook Kaggle đọc thẳng,
khỏi chép tay chuỗi 400 ký tự từ ảnh.
Chạy:  ~/.venvs/thesis/bin/python harness/c1_oracle_spice.py
"""
import glob, json, os, sys

J = sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))
if J and "JAVA_HOME" not in os.environ:
    os.environ["JAVA_HOME"] = J[-1]
    os.environ["PATH"] = J[-1] + "/bin:" + os.environ["PATH"]
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.spice.spice import Spice

src = sys.argv[1] if len(sys.argv) > 1 else "runs/c1/c1_mau.jsonl"
D = [json.loads(l) for l in open(src, encoding="utf-8")]
n = len(D)
tk = PTBTokenizer()
g = tk.tokenize({i: [{"caption": d["gold"]}] for i, d in enumerate(D)})
cau = [[d["greedy"]] + d["mau"] for d in D]
per = []
for k in range(9):
    c = tk.tokenize({i: [{"caption": cau[i][k]}] for i in range(n)})
    _, s = Spice().compute_score(g, c)
    ids = sorted(g.keys())            # Spice trả theo thứ tự khoá đã sắp
    per.append({i: s[j]["All"]["f"] for j, i in enumerate(ids)})
    print(f"k{k}: SPICE mức kho {100*sum(per[k].values())/n:.2f}", flush=True)
picks = "".join(str(max(range(9), key=lambda k: (per[k][i], -k))) for i in range(n))
tap = [i for i, d in enumerate(D) if d["action_type"] in ("click", "long_press")]
def tb(ix, chon):
    return round(100 * sum(per[chon(i)][i] for i in ix) / len(ix), 2)
out = {
    "picks": picks,
    "spice_greedy_400": tb(range(n), lambda i: 0),
    "spice_oracle_400": tb(range(n), lambda i: int(picks[i])),
    "spice_greedy_click": tb(tap, lambda i: 0),
    "spice_oracle_click": tb(tap, lambda i: int(picks[i])),
    "n_click_theo_action_type": len(tap),
    "doi_cau_400": sum(p != "0" for p in picks),
    "doi_cau_click": sum(picks[i] != "0" for i in tap),
}
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(src), "c1_picks.json"), "w"), ensure_ascii=False, indent=1)
