# -*- coding: utf-8 -*-
"""Sinh hai bảng "nhiều thước" cho ch6 luận văn từ các tệp kết quả đã tính — 0 giây GPU.

    python3 harness/sinh_bang_nhieu_thuoc.py      # ghi thesis/chapters/bang_nhieu_thuoc.tex

Nguồn (không tự tính lại gì, chỉ ghép nên không lệch được với script gốc):
  runs/luat_d3.json            ← harness/luat_d3.py          (luật vị trí)
  runs/text_metrics.json       ← harness/text_metrics.py     (action_ok)
  runs/text_metrics_coco.json  ← harness/text_metrics_coco.py (BLEU-4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE)
  runs/text_metrics_them.json  ← harness/text_metrics_them.py (chrF · BERTScore)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda f: json.load(open(os.path.join(HERE, "..", "runs", f), encoding="utf-8"))

# (khoá trong luat_d3.json, khoá trong các tệp văn bản, nhãn in, là nhánh mô hình?)
HANG = [
    ("Base", "Base", "Base", True),
    ("S1/101", "S1/101", "S1 ($101$)", True),
    ("S1/202", "S1/202", "S1 ($202$)", True),
    ("S2/101", "S2/101", "S2", True),
    ("CE2-S2/101", "CE2-S2/101", "CE2-S2", True),
    ("MIN-DESC/101", "MIN-DESC/101", "MIN-DESC", True),
    ("GRPO-point/101", "GRPO-point/101", "Chặng ba", True),
    ("gui_sel/101", "gui_sel/101", "Nhánh ứng viên\\textsuperscript{$\\dagger$}", True),
    ("Câu người (trần)", "Câu chuẩn", "\\emph{Câu chuẩn}", False),
]


def so(x, nd=1):
    return f"${x:.{nd}f}$".replace(".", "{,}")


def bang(cot, nguon, nd=1):
    """cot: list (nhãn, hàm lấy số từ hàng). In đậm số lớn nhất trong các nhánh mô hình."""
    def lay(f, h):
        try:
            return f(h)
        except KeyError:          # nhánh chưa tính xong ⇒ in "-"
            return None
    gt = [[lay(f, h) for _, f in cot] for h in nguon]
    mx = [max((gt[i][j] for i, h in enumerate(HANG) if h[3] and gt[i][j] is not None), default=None)
          for j in range(len(cot))]
    dong = []
    for i, h in enumerate(HANG):
        if not h[3]:
            dong.append("\\midrule")
        o = []
        for j, v in enumerate(gt[i]):
            if v is None:
                o.append("-")
                continue
            t = so(v, nd)
            if h[3] and round(v, nd) == round(mx[j], nd):
                t = "$\\mathbf{" + t[1:-1] + "}$"
            o.append(t)
        dong.append(h[2] + " & " + " & ".join(o) + " \\\\")
    return dong


def main():
    P = R("luat_d3.json")["n4463"]
    T = R("text_metrics.json")
    C = R("text_metrics_coco.json")
    M = R("text_metrics_them.json")
    ra = []

    vt = [("Exec.", lambda h: P[h[0]]["vor"]), ("Hộp (D.3)", lambda h: P[h[0]]["d3"]),
          ("D.3 $\\wedge$ $14\\%$", lambda h: P[h[0]]["d3_gate"]),
          ("$\\pm 14\\%$ trục", lambda h: P[h[0]]["d14_truc"]),
          ("AitW", lambda h: P[h[0]]["aitw"]),
          ("Loại thao tác", lambda h: T[h[1]]["action_ok"])]
    ra += [r"\begin{table}[t]",
           r"\caption{Nhóm thước theo vị trí trên đủ $4.463$ bước chạm, tính lại từ bản ghi từng bước,"
           r" không gọi lại mô hình định vị. Exec.\ là executability. Hộp (D.3) là luật khớp gốc của"
           r" AndroidControl (Mục~\ref{sec:donhay}). Cột cuối là tỉ lệ gọi đúng loại thao tác. Số in đậm"
           r" là số cao nhất trong các nhánh mô hình ở cột đó. \textsuperscript{$\dagger$}Nhánh ứng viên lệch ba"
           r" biến so với các nhánh còn lại nên chỉ đọc được so với Base.}",
           r"\label{tab:nhieuthuoc_vitri}", r"\centering\small", r"\renewcommand{\arraystretch}{1.2}",
           r"\setlength{\tabcolsep}{3.5pt}",
           r"\begin{tabular}{@{}l" + "r" * len(vt) + "@{}}", r"\toprule",
           "Nhánh & " + " & ".join(c for c, _ in vt) + r" \\", r"\midrule"]
    ra += bang(vt, HANG)
    ra += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]

    vb = [("BLEU-4", lambda h: C[h[1]]["bleu4"]), ("METEOR", lambda h: C[h[1]]["meteor15"]),
          ("ROUGE-L", lambda h: C[h[1]]["rougeL"]), ("CIDEr-D", lambda h: C[h[1]]["cider_d"]),
          ("SPICE", lambda h: C[h[1]]["spice"]), ("chrF", lambda h: M[h[1]]["chrf"]),
          ("BERTScore", lambda h: M[h[1]]["bertscore_f1_rescaled"])]
    ra += [r"\begin{table}[t]",
           r"\caption{Nhóm thước so với câu chuẩn trên đủ $4.463$ bước chạm. BLEU-4, METEOR~1.5, ROUGE-L,"
           r" CIDEr-D và SPICE tính mức kho bằng bộ chấm chính thức của COCO Captions, sau khi tách từ"
           r" bằng PTBTokenizer. chrF tính bằng sacreBLEU. BERTScore là F1 với \texttt{roberta-large}"
           r" tầng $17$, đã hiệu chỉnh theo đường cơ sở. Mỗi bước chỉ có một câu chuẩn. Số in đậm là số"
           r" cao nhất trong các nhánh mô hình ở cột đó. Chặng ba là MIN-DESC học tiếp với phần thưởng"
           r" đặt trên ô toạ độ. \textsuperscript{$\dagger$}Nhánh ứng viên chỉ đọc được so với Base.}",
           r"\label{tab:nhieuthuoc_vanban}", r"\centering\small", r"\renewcommand{\arraystretch}{1.2}",
           r"\setlength{\tabcolsep}{3.5pt}",
           r"\begin{tabular}{@{}l" + "r" * len(vb) + "@{}}", r"\toprule",
           "Nhánh & " + " & ".join(c for c, _ in vb) + r" \\", r"\midrule"]
    ra += bang(vb, HANG)
    ra += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]

    out = os.path.join(HERE, "..", "thesis", "chapters", "bang_nhieu_thuoc.tex")
    open(out, "w", encoding="utf-8").write(
        "% SINH TỰ ĐỘNG bởi harness/sinh_bang_nhieu_thuoc.py — đừng sửa tay\n" + "\n".join(ra) + "\n")
    print("ghi", os.path.relpath(out))


if __name__ == "__main__":
    main()
