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
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# bảng màu tham chiếu (đã kiểm phân biệt mù màu ở ba ô đầu); xám cho mốc
XANH, CAM, NGOC, XAM, CHU = "#2a78d6", "#eb6834", "#1baf7a", "#9a9993", "#0b0b0b"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": "#52514e",
                     "axes.labelcolor": CHU, "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "axes.spines.top": False, "axes.spines.right": False})
J = lambda f: json.load(open(os.path.join(RUNS, f), encoding="utf-8"))
key = lambda r: (str(r["episode_id"]), str(r["step_id"]))
JL = lambda f: {key(r): r for r in map(json.loads, open(os.path.join(RUNS, f), encoding="utf-8"))}
vn = lambda x, nd=1: f"{x:.{nd}f}".replace(".", ",")


def fig_ba_luat():
    P, A, N = J("luat_d3.json")["n4463"], J("luat_aitw_day_du.json")["n4463"], J("hang_ck500_tage.json")
    hang = [("Base", "Base"), ("S1/101", "S1 (101)"), ("MIN-DESC/101", "MIN-DESC"),
            ("GRPO-point/101", "Chặng ba"), ("ck500", "Thưởng\nSPICE"), ("Câu người (trần)", "Câu chuẩn")]
    def v(k, c):
        if k == "ck500":
            return {"aitw": N[k]["aitw_full"], "d3": N[k]["d3"], "vor": N[k]["vor"]}[c]
        return A[k]["aitw_full"] if c == "aitw" else P[k][c]
    luat = [("aitw", "Luật khớp chạm AitW", XANH), ("d3", "Hộp phần tử (D.3)", NGOC), ("vor", "Executability", CAM)]
    fig, ax = plt.subplots(figsize=(7.4, 3.6), dpi=200)
    w = 0.26
    for j, (c, ten, mau) in enumerate(luat):
        xs = [i + (j - 1) * w for i in range(len(hang))]
        ys = [v(k, c) for k, _ in hang]
        ax.bar(xs, ys, w - 0.03, color=mau, label=ten, zorder=2)
        for x, y in zip(xs, ys):
            ax.text(x, y + 1.0, vn(y), ha="center", va="bottom", fontsize=6.6, color=CHU)
    ax.set_xticks(range(len(hang)))
    ax.set_xticklabels([t for _, t in hang])
    ax.set_ylim(0, 100)
    ax.set_ylabel("% bước chạm (n = 4.463)")
    ax.yaxis.grid(True, color="#e6e5e0", zorder=0)
    ax.axvspan(len(hang) - 1.5, len(hang) - 0.5, color="#f0efec", zorder=0)
    ax.legend(frameon=False, ncol=3, loc="upper left", fontsize=8.5)
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
    ax.set_xlabel("Thưởng SPICE − S1 (101), điểm khớp loại thao tác, KTC 95%")
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
    bins = [(-1e9, 0, "≤ 0"), (0, 0.4, "(0; 0,4]"), (0.4, 0.73767, "(0,4; 0,74]"), (0.73767, 1e9, "> 0,74\n(cổng nhận)")]
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
    fig, ax = plt.subplots(figsize=(6.2, 2.9), dpi=200)
    xs = range(len(bins))
    ax.bar(xs, ti, 0.55, color=[XANH, XANH, XANH, CAM], zorder=2)
    for x, t, (n, _) in zip(xs, ti, dem):
        ax.text(x, t + 1.5, f"{vn(t)}%\nn = " + f"{n:,}".replace(",", "."), ha="center", va="bottom", fontsize=8)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([b[2] for b in bins])
    ax.set_ylim(0, 100)
    ax.set_xlabel("Δlp = lp(câu sửa) − lp(câu nháp), chỉ các câu bị đổi")
    ax.set_ylabel("% vùng cắt đúng chỗ")
    ax.yaxis.grid(True, color="#e6e5e0", zorder=0)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_tage_cong.png"))
    plt.close(fig)


def ve_buoc(path, gold, diem, cat=None, cao=None):
    """Ảnh màn hình + điểm vàng (vòng đen) + các điểm (màu, dạng). Trả ảnh RGB."""
    im = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(im)
    if cat:
        (cx, cy), s = cat, 0.4 * im.size[0]
        d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], outline=(235, 104, 52), width=9)
    def vong(p, col, r=34, w=9):
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], outline=(255, 255, 255), width=w + 6)
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], outline=col, width=w)
    vong(gold, (0, 0, 0), 44, 10)
    for p, col, dang in diem:
        if dang == "x":
            for s in ((1, 1), (1, -1)):
                for wd, c in ((22, (255, 255, 255)), (12, col)):
                    d.line([p[0] - 30 * s[0], p[1] - 30 * s[1], p[0] + 30 * s[0], p[1] + 30 * s[1]], fill=c, width=wd)
        else:
            d.ellipse([p[0] - 22, p[1] - 22, p[0] + 22, p[1] + 22], fill=col, outline=(255, 255, 255), width=6)
    if cao:
        im = im.crop(cao)
    return im


def chu_giai(w, dong, co=34):
    f, fb = ImageFont.truetype(FONT, co), ImageFont.truetype(FONTB, co)
    h = 30 + len(dong) * (co + 20)
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    y = 18
    for ky, col, nhan, txt in dong:
        x = 18
        if ky == "o":
            d.ellipse([x, y + 4, x + co - 6, y + co - 2], outline=col, width=6)
        elif ky == "x":
            d.line([x, y + 4, x + co - 6, y + co - 2], fill=col, width=7)
            d.line([x, y + co - 2, x + co - 6, y + 4], fill=col, width=7)
        elif ky == "dot":
            d.ellipse([x + 4, y + 8, x + co - 10, y + co - 6], fill=col)
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
    cg = chu_giai(W, [("o", (0, 0, 0), "Câu chuẩn:", "“Click on the Not now button"),
                      ("", None, "", "     to remove this pop up notification”"),
                      ("x", (227, 73, 72), "S1 (101):", f"“{s1['sent']}”  → trượt"),
                      ("dot", (27, 175, 122), "Thưởng SPICE:", "“Click on the Not Now button"),
                      ("", None, "", f"     at the bottom of the screen”  → trúng")], co=40)
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
    fb = ImageFont.truetype(FONTB, 40)
    x = 0
    for nhan, (im, _, _) in zip(("(a) cổng nhận, vùng cắt đúng chỗ", "(b) cổng nhận, vùng cắt sai chỗ"), tam):
        d.text((x + 10, 10), nhan, font=fb, fill=(11, 11, 11))
        anh.paste(im, (x, 70)); x += im.size[0] + 60
    (_, ma, _), (_, mb, _) = tam
    cg = chu_giai(w, [("sq", (235, 104, 52), "Ô cam:", "vùng cắt 40% bề ngang quanh điểm bộ định vị đoán"),
                      ("o", (0, 0, 0), "Vòng đen:", "điểm người dùng đã chạm"),
                      ("dot", (27, 175, 122), "Chấm xanh / dấu đỏ:", "câu trúng / câu trượt dưới mô hình định vị"),
                      ("", None, "(a) nháp:", f"“{ma['draft']}”  →  sửa: “{ma['edit']}”"),
                      ("", None, "(b) nháp:", f"“{mb['draft']}”  →  sửa: “{mb['edit']}”")], co=32)
    ghep_doc(anh, cg).save(os.path.join(OUT, "fig_vidu_tage.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in (fig_ba_luat, fig_khongcham, fig_tage_cong, fig_vidu_spice, fig_vidu_tage):
        f(); print("xong", f.__name__)
