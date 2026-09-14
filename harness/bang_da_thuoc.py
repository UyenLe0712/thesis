# -*- coding: utf-8 -*-
"""Một bảng duy nhất gộp MỌI thước đã đo cho mọi nhánh — 0 giây GPU.

    python3 harness/bang_da_thuoc.py            # bảng chữ
    python3 harness/bang_da_thuoc.py --latex    # thêm bản LaTeX cho luận văn

Đọc `runs/luat_d3.json` (bảy luật vị trí, sinh bởi `luat_d3.py`) và `runs/text_metrics.json`
(BLEU-4 · ROUGE-L · action_ok, sinh bởi `text_metrics.py`). ⛔ Không tự tính lại gì — hai
script kia là nguồn, file này chỉ ghép, nên không thể lệch với chúng.

⛔⛔ LUẬT ĐỌC, đừng bỏ:
· Cột **TIÊU ĐỀ** duy nhất là `exec` Voronoi ±14%, niêm `b93e85c` 5/8. Mọi cột khác là **báo
  kèm** hoặc **độ nhạy** — in cạnh nhau để định vị, ⛔ KHÔNG được chọn cột cao nhất làm đóng góp.
· ⛔ Cấm cộng dồn hai cột thành một mũi tên: chúng là nhiều luật trên **cùng một lượt chạy**,
  không phải nhiều mức tăng.
· Ba cột `±14% trục` · `AitW` · `hit_disk` cho số cao hơn nhưng **sàn cũng cao hơn**: câu rỗng
  nghĩa được 12,00 dưới Voronoi mà 20,50 dưới ±14% ⇒ dải dùng được HẸP lại (62,88 → 62,50).
  Đó là lý do `151` mục 6 không cho đưa chúng lên tiêu đề.
· Cột dải rộng nhất là **D.3** (68,88) và **D.3 -cont** (69,00) — đó mới là hai cột báo kèm.
"""
import argparse, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "..", "runs")
COT = [("vor", "exec", "TIÊU ĐỀ"), ("d3", "D.3", "báo kèm"),
       ("d3_gate", "D.3∧14%", "báo kèm"), ("d3_nocont", "D.3 -cont", "báo kèm"),
       ("d14_truc", "±14% trục", "độ nhạy"), ("aitw", "AitW", "độ nhạy"),
       ("disk_thuan", "hit_disk", "độ nhạy")]
VAN = [("action_ok", "action_ok"), ("bleu4", "BLEU-4"), ("rougeL", "ROUGE-L")]
# text_metrics.py gọi nhánh trần là "Câu chuẩn", luat_d3.py gọi "Câu người (trần)"
BIDANH = {"Câu người (trần)": "Câu chuẩn"}


def nap():
    P = json.load(open(os.path.join(RUNS, "luat_d3.json"), encoding="utf-8"))["n4463"]
    T = json.load(open(os.path.join(RUNS, "text_metrics.json"), encoding="utf-8"))
    hang = []
    for ten, v in P.items():
        t = T.get(BIDANH.get(ten, ten), {})
        hang.append((ten, v, t))
    return sorted(hang, key=lambda r: -r[1]["vor"])


def main():
    a = argparse.ArgumentParser(); a.add_argument("--latex", action="store_true")
    a = a.parse_args()
    H = nap()
    print(f"{'nhánh':<20}" + "".join(f"{n:>11}" for _, n, _ in COT)
          + "".join(f"{n:>11}" for _, n in VAN))
    print(f"{'vai':<20}" + "".join(f"{v:>11}" for _, _, v in COT)
          + "".join(f"{'văn bản':>11}" for _ in VAN))
    print("-" * (20 + 11 * (len(COT) + len(VAN))))
    for ten, v, t in H:
        print(f"{ten:<20}" + "".join(f"{v[k]:>11.2f}" for k, _, _ in COT)
              + "".join(f"{t[k]:>11.2f}" if k in t else f"{'—':>11}" for k, _ in VAN))
    if a.latex:
        print("\n% ── dán vào luận văn ─────────────────────────────────────────")
        print("\\begin{tabular}{l" + "r" * (len(COT) + len(VAN)) + "}\n\\hline")
        print("Nhánh & " + " & ".join(n for _, n, _ in COT)
              + " & " + " & ".join(n for _, n in VAN) + " \\\\\n\\hline")
        for ten, v, t in H:
            o = [f"{v[k]:.2f}" for k, _, _ in COT]
            o += [f"{t[k]:.2f}" if k in t else "--" for k, _ in VAN]
            print(f"{ten.replace('_', '\\_')} & " + " & ".join(o) + " \\\\")
        print("\\hline\n\\end{tabular}")


if __name__ == "__main__":
    main()
