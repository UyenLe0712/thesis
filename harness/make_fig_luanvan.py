# -*- coding: utf-8 -*-
"""Sinh các hình mới của luận văn (đợt 4/10/2026) từ tệp kết quả đã có — 0 giây GPU.

    ~/.venvs/thesis/bin/python harness/make_fig_luanvan.py     # ghi thesis/figures/*.png

Mọi con số đọc thẳng từ tệp JSON/JSONL trong runs/, không gõ tay:
  fig_ba_luat.png      ← runs/luat_d3.json · luat_aitw_day_du.json · hang_ck500_tage.json
  fig_khongcham.png    ← runs/grpo_spice/nontap_ck500_doc.json
  fig_tage_cong.png    ← runs/tage_test/{pred_test_s*_meta,loc_test}.jsonl + score_pred_cong_raw
  fig_vidu_spice.png   ← runs/score_s1_seed101_raw.jsonl · grpo_spice/score_ck500_test_raw.jsonl
  fig_vidu_tage.png    ← runs/tage_test/*  (một bước sửa đúng, một bước sửa hỏng)
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

H = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(H, "..", "runs")
OUT = os.path.join(H, "..", "thesis", "figures")
IMG = os.path.join(H, "dg1_cache", "test_ac", "images")
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"   # cùng cỡ chữ với Times của thân bài
FONTB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

# bảng màu tham chiếu (đã kiểm phân biệt mù màu ở ba ô đầu); xám cho mốc
XANH, CAM, NGOC, XAM, CHU = "#2a78d6", "#eb6834", "#1baf7a", "#9a9993", "#0b0b0b"
from matplotlib import font_manager
for _f in (FONT, FONTB):
    font_manager.fontManager.addfont(_f)
plt.rcParams.update({"font.family": "Liberation Serif", "mathtext.fontset": "stix", "font.size": 10, "axes.edgecolor": "#52514e",
                     "axes.labelcolor": CHU, "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "axes.spines.top": False, "axes.spines.right": False})
J = lambda f: json.load(open(os.path.join(RUNS, f), encoding="utf-8"))
key = lambda r: (str(r["episode_id"]), str(r["step_id"]))
JL = lambda f: {key(r): r for r in map(json.loads, open(os.path.join(RUNS, f), encoding="utf-8"))}
from decimal import Decimal, ROUND_HALF_UP
# làm tròn kiểu thập phân (60,654 → 60,7), tránh lỗi dấu phẩy động của f-string
vn = lambda x, nd=1: str(Decimal(str(x)).quantize(Decimal(1).scaleb(-nd), ROUND_HALF_UP)).replace(".", ",")


def fig_ba_luat():
    P, A, N = J("luat_d3.json")["n4463"], J("luat_aitw_day_du.json")["n4463"], J("hang_ck500_tage.json")
    N = dict(N, ace=J("hang_ace.json"))
    hang = [("Base", "Mô hình\ngốc"), ("S1/101", "S1/101"), ("MIN-DESC/101", "MIN-DESC"),
            ("GRPO-point/101", "Giai đoạn\nba"), ("ck500", "GRPO-\nSPICE"), ("ace", "Phương pháp\nđề xuất"),
            ("Câu người (trần)", "Câu tham\nchiếu")]
    def v(k, c):
        if k in ("ck500", "ace"):
            return {"aitw": N[k]["aitw_full"], "d3": N[k]["d3"], "vor": N[k]["vor"]}[c]
        return A[k]["aitw_full"] if c == "aitw" else P[k][c]
    luat = [("vor", "Executability", CAM), ("d3", "Hộp phần tử (AndroidControl)", NGOC),
            ("aitw", "Khoảng cách Euclid (AndroidInTheWild)", XANH)]
    fig, ax = plt.subplots(figsize=(7.8, 3.7), dpi=200)
    w = 0.26
    for j, (c, ten, mau) in enumerate(luat):
        xs = [i + (j - 1) * w for i in range(len(hang))]
        ys = [v(k, c) for k, _ in hang]
        ax.bar(xs, ys, w - 0.03, color=mau, label=ten, zorder=2)
        for x, y in zip(xs, ys):
            ax.text(x, y + 1.0, vn(y), ha="center", va="bottom", fontsize=6.4, color=CHU)
    ax.set_xticks(range(len(hang)))
    ax.set_xticklabels([t for _, t in hang])
    ax.set_ylim(0, 100)
    ax.set_ylabel("% số bước có thao tác chạm (n = 4.463)")
    ax.yaxis.grid(True, color="#e6e5e0", zorder=0)
    ax.axvspan(len(hang) - 1.5, len(hang) - 0.5, color="#f0efec", zorder=0)
    ax.legend(frameon=False, ncol=3, loc="upper left", fontsize=8.5, bbox_to_anchor=(0, 1.08))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_ba_luat.png"))
    plt.close(fig)


def fig_khongcham():
    D = J("grpo_spice/nontap_ck500_doc.json")["theo_loai"]
    ten = {"TOÀN BỘ": "toàn bộ", "scroll": "cuộn", "navigate_back": "quay lại", "input_text": "gõ chữ",
           "open_app": "mở ứng dụng", "wait": "chờ"}
    thu = ["wait", "open_app", "input_text", "navigate_back", "scroll", "TOÀN BỘ"]
    fig, ax = plt.subplots(figsize=(6.6, 2.9), dpi=200)
    for i, k in enumerate(thu):
        o = D[k]
        mau = XANH if o["delta"] > 0 else CAM
        ax.barh(i, o["delta"], 0.6, color=mau, zorder=2)
        ax.errorbar(o["delta"], i, xerr=[[o["delta"] - o["lo"]], [o["hi"] - o["delta"]]],
                    fmt="none", ecolor=CHU, elinewidth=1, capsize=2.5, zorder=3)
        x = o["hi"] + 0.3 if o["delta"] > 0 else o["lo"] - 0.3
        ax.text(x, i, f"{'+' if o['delta'] > 0 else '−'}{vn(abs(o['delta']), 2)}",
                va="center", ha="left" if o["delta"] > 0 else "right", fontsize=8, color=CHU)
    ax.set_yticks(range(len(thu)))
    ax.set_yticklabels([f"{ten[k]} (n = {D[k]['n']:,})".replace(",", ".") for k in thu])
    ax.axvline(0, color="#52514e", lw=0.8)
    ax.set_xlim(-11.5, 9)
    ax.set_xlabel("GRPO-SPICE − S1/101, chênh lệch tỉ lệ đúng loại thao tác (điểm), KTC 95%")
    ax.xaxis.grid(True, color="#e6e5e0", zorder=0)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_khongcham.png"))
    plt.close(fig)


def fig_tage_cong():
    meta = {}
    for f in ("tage_test/pred_test_s0_meta.jsonl", "tage_test/pred_test_s1_meta.jsonl"):
        meta.update(JL(f))
    loc = {}
    for f in ("tage_test/loc_test_s0.jsonl", "tage_test/loc_test_s1.jsonl"):
        loc.update(JL(f))
    bins = [(-1e9, 0, "≤ 0"), (0, 0.4, "(0; 0,4]"), (0.4, 0.73767, "(0,4; 0,74]"), (0.73767, 1e9, "> 0,74\n(bộ chọn nhận)")]
    dem = [[0, 0] for _ in bins]
    for k, m in meta.items():
        if m["edit"] == m["draft"]:
            continue
        d = m["lp_edit"] - m["lp_draft"]
        for i, (a, b, _) in enumerate(bins):
            if a < d <= b:
                dem[i][0] += 1
                dem[i][1] += int(loc[k]["hit_disk"])
    ti = [100 * h / n for n, h in dem]
    # đối chiếu report/269 §3: nhóm cổng nhận = 219 câu, bộ định vị trúng 80 (bảng tách theo điểm vàng).
    # Bảng Δlp của 269 in 36,9% / n = 217 vì cắt ở 0,74 đã làm tròn; ở đây cắt đúng τ = 0,73767.
    assert dem[-1] == [219, 80], dem
    fig, ax = plt.subplots(figsize=(5.2, 2.9), dpi=220)
    xs = range(len(bins))
    ax.bar(xs, ti, 0.55, color=[XANH, XANH, XANH, CAM], zorder=2)
    for x, t, (n, _) in zip(xs, ti, dem):
        ax.text(x, t + 1.5, f"{vn(t)}%\nn = " + f"{n:,}".replace(",", "."), ha="center", va="bottom", fontsize=8)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([b[2] for b in bins])
    ax.set_ylim(0, 100)
    ax.set_xlabel("Δlp = lp(câu sửa) − lp(câu ban đầu), chỉ tính các câu bị đổi")
    ax.set_ylabel("% bước bộ định vị trỏ đúng\n(trong dung sai 14%)")
    ax.yaxis.grid(True, color="#e6e5e0", zorder=0)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_tage_cong.png"))
    plt.close(fig)


VANG = (255, 193, 7)   # điểm người dùng chạm: vòng vàng viền đen, thấy rõ trên cả nền sáng lẫn nền tối


def ve_buoc(path, gold, diem, cat=None, cao=None, to=1.0):
    """Ảnh màn hình + điểm người dùng chạm (vòng vàng) + các điểm định vị (vòng xanh lá = đạt, X đỏ = không đạt)."""
    nen = Image.open(path).convert("RGBA")
    d0 = ImageDraw.Draw(nen)
    if cat:   # ô cắt vẽ đậm, không phủ trong suốt
        (cx, cy), s = cat, 0.4 * nen.size[0]
        W0, H0 = nen.size
        x0, y0 = max(5, cx - s / 2), max(5, cy - s / 2)
        x1, y1 = min(W0 - 5, cx + s / 2), min(H0 - 5, cy + s / 2)
        if cao:
            y1 = min(y1, cao[3] - 6); x0 = max(x0, cao[0] + 6)
        d0.rectangle([x0, y0, x1, y1], outline=(235, 104, 52), width=9)
    im = Image.new("RGBA", nen.size, (0, 0, 0, 0))   # điểm định vị: lớp riêng, phủ bán trong suốt để chữ bên dưới vẫn đọc được
    d = ImageDraw.Draw(im)
    for p, col, dang in diem:
        if dang == "x":
            for s in ((1, 1), (1, -1)):
                for wd, c in ((int(11 * to), (255, 255, 255)), (int(6 * to), col)):
                    d.line([p[0] - 26 * to * s[0], p[1] - 26 * to * s[1], p[0] + 26 * to * s[0], p[1] + 26 * to * s[1]], fill=c, width=wd)
        else:
            r = 24 * to
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], outline=(255, 255, 255), width=int(12 * to))
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], outline=col, width=int(7 * to))
    im.putalpha(im.getchannel("A").point(lambda v: v * 0.8))
    im = Image.alpha_composite(nen, im)
    d = ImageDraw.Draw(im)
    r, w = 44 * to, int(8 * to)   # vòng vàng to hơn vòng xanh lá nên hai vòng không che nhau
    d.ellipse([gold[0] - r, gold[1] - r, gold[0] + r, gold[1] + r], outline=(0, 0, 0), width=w + int(6 * to))
    d.ellipse([gold[0] - r + 3 * to, gold[1] - r + 3 * to, gold[0] + r - 3 * to, gold[1] + r - 3 * to], outline=VANG, width=w)
    im = im.convert("RGB")
    if cao:
        im = im.crop(cao)
    return im


def chu_giai(w, dong, co=34, x0=18):
    f, fb = ImageFont.truetype(FONT, co), ImageFont.truetype(FONTB, co)
    h = 30 + len(dong) * (co + 20)
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    y = 18
    for ky, col, nhan, txt in dong:
        x = x0
        if ky == "vang":
            d.ellipse([x, y + 4, x + co - 6, y + co - 2], outline=(0, 0, 0), width=9)
            d.ellipse([x + 3, y + 7, x + co - 9, y + co - 5], outline=VANG, width=5)
        elif ky == "o":
            d.ellipse([x, y + 4, x + co - 6, y + co - 2], outline=col, width=6)
        elif ky == "x":
            d.line([x, y + 4, x + co - 6, y + co - 2], fill=col, width=7)
            d.line([x, y + co - 2, x + co - 6, y + 4], fill=col, width=7)
        elif ky == "dot":
            d.ellipse([x + 2, y + 6, x + co - 8, y + co - 4], outline=col, width=6)
        elif ky == "sq":
            d.rectangle([x, y + 4, x + co - 6, y + co - 2], outline=col, width=6)
        d.text((x + co + 10, y), nhan, font=fb, fill=(11, 11, 11))
        lx = x + co + 10 + d.textlength(nhan, font=fb) + 12
        d.text((lx, y), txt, font=f, fill=(11, 11, 11))
        y += co + 20
    return im


def ghep_doc(a, b):
    im = Image.new("RGB", (max(a.size[0], b.size[0]), a.size[1] + b.size[1]), (255, 255, 255))
    im.paste(a, (0, 0)); im.paste(b, (0, a.size[1]))
    return im


def fig_vidu_spice():
    k = ("18239", "3")
    s1, ck = JL("score_s1_seed101_raw.jsonl")[k], JL("grpo_spice/score_ck500_test_raw.jsonl")[k]
    assert s1["executable"] == 0 and ck["executable"] == 1
    im = ve_buoc(os.path.join(IMG, "ep18239_s3.png"), s1["gold_xy"],
                 [(s1["pred_xy"], (227, 73, 72), "x"), (ck["pred_xy"], (27, 175, 122), "dot")],
                 cao=(60, 1000, 1020, 2330))
    W = 1500
    g = s1["gold_instruction"].strip()
    assert g == "Click on the Not now button to remove this pop up notification", g
    cg = chu_giai(W, [("vang", None, "Vòng vàng:", "điểm người dùng đã chạm"),
                      ("", None, "Câu tham chiếu:", "“Click on the Not now button"),
                      ("", None, "", "     to remove this pop up notification”"),
                      ("x", (227, 73, 72), "S1/101:", f"“{s1['sent']}”  → không đạt"),
                      ("dot", (27, 175, 122), "GRPO-SPICE:", "“Click on the Not Now button"),
                      ("", None, "", f"     at the bottom of the screen”  → đạt")], co=42, x0=(W - im.size[0]) // 2)
    assert ck["sent"] == "Click on the Not Now button at the bottom of the screen", ck["sent"]
    can = Image.new("RGB", (W, im.size[1]), (255, 255, 255))
    can.paste(im, ((W - im.size[0]) // 2, 0))
    ghep_doc(can, cg).save(os.path.join(OUT, "fig_vidu_spice.png"))


def fig_vidu_tage():
    meta = {}
    for f in ("tage_test/pred_test_s0_meta.jsonl", "tage_test/pred_test_s1_meta.jsonl"):
        meta.update(JL(f))
    ck, tg = JL("grpo_spice/score_ck500_test_raw.jsonl"), JL("tage_test/score_pred_cong_raw.jsonl")
    tam = []
    for k, ok in ((("18815", "4"), True), (("18386", "3"), False)):
        m = meta[k]
        assert ck[k]["executable"] == (0 if ok else 1) and tg[k]["executable"] == (1 if ok else 0)
        im = ve_buoc(os.path.join(IMG, f"ep{k[0]}_s{k[1]}.png"), ck[k]["gold_xy"],
                     [(ck[k]["pred_xy"], (227, 73, 72) if ok else (27, 175, 122), "x" if ok else "dot"),
                      (tg[k]["pred_xy"], (27, 175, 122) if ok else (227, 73, 72), "dot" if ok else "x")],
                     cat=m["crop_xy"], cao=(0, 1100, 1080, 2400))
        tam.append((im, m, ok))
    w = sum(i.size[0] for i, _, _ in tam) + 60
    anh = Image.new("RGB", (w, tam[0][0].size[1] + 70), (255, 255, 255))
    d = ImageDraw.Draw(anh)
    fb = ImageFont.truetype(FONTB, 48)
    x = 0
    for nhan, (im, _, _) in zip(("(a) Ô cắt chứa phần tử mục tiêu", "(b) Ô cắt rơi vào phần tử khác"), tam):
        d.text((x + 10, 10), nhan, font=fb, fill=(11, 11, 11))
        anh.paste(im, (x, 70)); x += im.size[0] + 60
    (_, ma, _), (_, mb, _) = tam
    cg = chu_giai(w, [("sq", (235, 104, 52), "Khung cam:", "ô cắt rộng 40% bề ngang quanh điểm mà bộ định vị dự đoán"),
                      ("vang", None, "Vòng vàng:", "điểm người dùng đã chạm"),
                      ("dot", (27, 175, 122), "Vòng xanh lá:", "điểm định vị cho câu đạt, (a) câu sửa, (b) câu ban đầu"),
                      ("x", (227, 73, 72), "Dấu X đỏ:", "điểm định vị cho câu không đạt, (a) câu ban đầu, (b) câu sửa"),
                      ("", None, "(a) câu ban đầu:", f"“{ma['draft']}”"),
                      ("", None, "      câu sửa:", f"“{ma['edit']}”"),
                      ("", None, "(b) câu ban đầu:", f"“{mb['draft']}”"),
                      ("", None, "      câu sửa:", f"“{mb['edit']}”")], co=46)
    ghep_doc(anh, cg).save(os.path.join(OUT, "fig_vidu_tage.png"))


def fig_bai_toan():
    """Ảnh nền cho Hình 1.1 (phần chữ viết bằng TikZ trong luận văn)."""
    k = ("18794", "3")
    ace, base = JL("ra304_luat/score_R3_test_raw.jsonl")[k], JL("score_base_raw.jsonl")[k]
    assert ace["executable"] == 1 and base["executable"] == 0
    assert ace["sent"] == "Click on the bin icon at the bottom right corner of the screen", ace["sent"]
    im = ve_buoc(os.path.join(IMG, "ep18794_s3.png"), ace["gold_xy"],
                 [(base["pred_xy"], (227, 73, 72), "x"), (ace["pred_xy"], (27, 175, 122), "dot")], to=2.0)
    im.save(os.path.join(OUT, "fig_bai_toan_anh.png"))


def fig_chenh_lech():
    """Hình 6.2: chênh lệch so với S1/101 theo ba tiêu chí, kèm KTC 95% (runs/chenh_so_s1_25_10.json)."""
    C = J("chenh_so_s1_25_10.json")
    hang = [("ACE", "Phương pháp đề xuất"), ("GRPO-SPICE", "GRPO-SPICE"), ("GRPO-SPICE/202", "GRPO-SPICE (seed 202)"),
            ("S1/202", "S1/202 (chỉ đổi seed)"),
            ("GRPO-point/101", "Giai đoạn ba/101"), ("MIN-DESC/101", "MIN-DESC/101"), ("CE2-S2/101", "CE2-S2/101"),
            ("S2/101", "S2/101")]
    cot = [("vor", "Executability", CAM, "o"), ("d3", "Hộp phần tử", NGOC, "s"), ("aitwf", "Khoảng cách Euclid", XANH, "D")]
    fig, ax = plt.subplots(figsize=(6.0, 3.9), dpi=220)
    y = list(range(len(hang)))[::-1]
    for (c, ten, mau, dang), dy in zip(cot, (0.22, 0, -0.22)):
        for yi, (k, _) in zip(y, hang):
            d, lo, hi = C[f"{k}|{c}"]
            ax.plot([lo, hi], [yi + dy] * 2, color=mau, lw=1.6, zorder=2)
            ax.plot(d, yi + dy, dang, color=mau, ms=5, zorder=3, label=ten if k == "ACE" else None)
    ax.axvline(0, color="#52514e", lw=0.9, zorder=1)
    ax.axhspan(y[2] - 0.5, y[0] + 0.5, color="#f3f2ee", zorder=0)
    for yy in (y[2] - 0.5, y[3] - 0.5):
        ax.axhline(yy, color="#b9b8b2", lw=0.7, ls=(0, (4, 3)), zorder=1)
    ax.set_yticks(y)
    ax.set_yticklabels([t for _, t in hang])
    ax.set_xlabel("Chênh lệch so với S1/101 (điểm), khoảng tin cậy 95%")
    ax.xaxis.grid(True, color="#e6e5e0", zorder=0)
    ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=8.5)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_chenh_lech.png"))
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in (fig_ba_luat, fig_khongcham, fig_tage_cong, fig_vidu_spice, fig_vidu_tage, fig_bai_toan, fig_chenh_lech):
        f(); print("xong", f.__name__)
