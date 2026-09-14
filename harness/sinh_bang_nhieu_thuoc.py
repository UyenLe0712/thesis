# -*- coding: utf-8 -*-
"""Sinh hai bảng "nhiều thước" cho ch6 luận văn từ các tệp kết quả đã tính — 0 giây GPU.

    python3 harness/sinh_bang_nhieu_thuoc.py      # ghi thesis/chapters/bang_nhieu_thuoc.tex

Nguồn (không tự tính lại gì, chỉ ghép nên không lệch được với script gốc):
  runs/luat_d3.json            ← harness/luat_d3.py          (luật vị trí)
  runs/text_metrics.json       ← harness/text_metrics.py     (action_ok)
  runs/text_metrics_coco.json  ← harness/text_metrics_coco.py (BLEU-4 · METEOR 1.5 · ROUGE-L · CIDEr-D · SPICE)
  runs/text_metrics_them.json  ← harness/text_metrics_them.py (chrF · BERTScore)
  runs/luat_aitw_day_du.json   ← harness/luat_aitw_day_du.py (luật khớp chạm đầy đủ của AitW)
  runs/d3_ktc.json             ← harness/d3_ktc.py            (KTC95 + McNemar cho ba số chính)
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

    AF = R("luat_aitw_day_du.json")["n4463"]
    AM = R("luat_aitw_moi_hop.json")["n4463"]
    vt = [("AitW", lambda h: AF[h[0]]["aitw_full"]), ("Hộp (D.3)", lambda h: P[h[0]]["d3"]),
          ("Exec.", lambda h: P[h[0]]["vor"]),
          ("$\\pm 14\\%$ trục", lambda h: P[h[0]]["d14_truc"]),
          ("AitW cận trên", lambda h: AM[h[0]]["aitw_moi_khung"]),
          ("Thao tác", lambda h: T[h[1]]["action_ok"])]
    ra += [r"\begin{table}[t]",
           r"\caption{Nhóm thước theo vị trí trên đủ $4.463$ bước chạm, tính lại từ bản ghi từng bước,"
           r" không gọi lại mô hình định vị. AitW là luật khớp chạm trong mã chấm gốc của"
           r" AndroidInTheWild, AitW cận trên là biến thể của luật ấy khi vế khung xét mọi phần tử bấm được (sàn cao hơn, Mục~\ref{sec:donhay}). Hộp (D.3) là luật khớp gốc của"
           r" AndroidControl. Exec.\ là executability (Mục~\ref{sec:donhay}). Thao tác là tỉ lệ gọi đúng loại thao tác. Số in đậm"
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

    # ── bảng 3: KTC95 + phép so ghép cặp dưới ba luật (runs/d3_ktc.json ← harness/d3_ktc.py) ──
    K3 = R("d3_ktc.json")
    def pv(p):
        return "$<0{,}001$" if p < 0.001 else so(p, 3)
    sg = lambda x: ("+" if x >= 0 else "-") + f"{abs(x):.2f}".replace(".", "{,}")
    ci = lambda o: f"{so(o['diem'])} $[{so(o['lo'])[1:-1]}; {so(o['hi'])[1:-1]}]$"
    TEN = {"Base": "Base", "S2/101": "S2", "S1/101": "S1 ($101$)", "S1/202": "S1 ($202$)", "MIN-DESC/101": "MIN",
           "GRPO-point/101": "Chặng ba", "Câu người (trần)": "Câu chuẩn"}
    ra += ["", r"\begin{table}[t]",
           r"\caption{Khoảng tin cậy $95\%$ của ba số chính trên $4.463$ bước (trên) và phép so ghép cặp"
           r" (dưới). Khoảng tin cậy lấy từ bootstrap $10.000$ lần gom cụm theo ứng dụng ($G = 1.091$), giá"
           r" trị $p$ của phép kiểm McNemar. MIN là MIN-DESC.}",
           r"\label{tab:d3ktc}", r"\centering\footnotesize", r"\renewcommand{\arraystretch}{1.15}",
           r"\setlength{\tabcolsep}{3pt}",
           r"\begin{tabular}{@{}llll@{}}", r"\toprule",
           r"Nhánh & AitW đầy đủ & Hộp phần tử (D.3) & Executability \\", r"\midrule"]
    for t in ("Base", "S1/101", "S1/202", "MIN-DESC/101", "GRPO-point/101", "Câu người (trần)"):
        o = K3["ktc"][t]
        ra.append(f"{TEN[t]} & {ci(o['aitwf'])} & {ci(o['d3'])} & {ci(o['vor'])} \\\\")
    ra += [r"\bottomrule", r"\end{tabular}", "", r"\vspace{0.6em}",
           r"\begin{tabular}{@{}llrrr@{}}", r"\toprule",
           r"Phép so & Luật & $\Delta$ & KTC $95\%$ & $p$ \\", r"\midrule"]
    cap = (("S1/101", "Base"), ("S2/101", "S1/101"), ("GRPO-point/101", "S2/101"),
           ("GRPO-point/101", "S1/101"), ("GRPO-point/101", "S1/202"),
           ("MIN-DESC/101", "S1/101"), ("GRPO-point/101", "MIN-DESC/101"))
    for i, (a, b) in enumerate(cap):
        if i:
            ra.append(r"\midrule")
        for j, (c, tl) in enumerate((("aitwf", "AitW đầy đủ"), ("d3", "D.3"), ("vor", "Exec."))):
            o = K3["so_sanh"][f"{a} − {b} · {c}"]
            nhan = f"{TEN[a]} $-$ {TEN[b]}" if j == 0 else ""
            ra.append(f"{nhan} & {tl} & ${sg(o['delta'])}$ & $[{sg(o['lo'])}; {sg(o['hi'])}]$ & {pv(o['p'])} \\\\")
    ra += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]

    out = os.path.join(HERE, "..", "thesis", "chapters", "bang_nhieu_thuoc.tex")
    open(out, "w", encoding="utf-8").write(
        "% SINH TỰ ĐỘNG bởi harness/sinh_bang_nhieu_thuoc.py — đừng sửa tay\n" + "\n".join(ra) + "\n")
    print("ghi", os.path.relpath(out))


if __name__ == "__main__":
    main()
