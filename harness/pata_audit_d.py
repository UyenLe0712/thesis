# -*- coding: utf-8 -*-
"""
PATA C2 · P0 bước 5 — audit MÙ 100 cặp (G, D) thật (harness/tai_lieu_2026-09-25/204 §4.1). 0 GPU, WSL.

    ~/.venvs/thesis/bin/python harness/pata_audit_d.py build            # lần 1: dựng 100 mẫu + trang gán
    ~/.venvs/thesis/bin/python harness/pata_audit_d.py doc              # đọc nhãn, tính ba tỉ lệ, in cổng
    ~/.venvs/thesis/bin/python harness/pata_audit_d.py build --lan 2    # CHỈ khi lần 1 trượt và đã sửa builder

Mỗi mẫu: câu vàng + ảnh màn có HAI khung, A (cam) và B (xanh). Khung nào là G do hạt quyết định, đảo
ngẫu nhiên, lưu ở manifest (người gán không thấy). ⛔ KHÔNG vẽ điểm chạm — vẽ ra là lộ đáp án.

Người gán trả lời hai câu:
  1. Câu hướng dẫn nhắm tới khung nào?  A · B · cả hai đều đúng · không khung nào · không rõ
  2. Khung nào KHÔNG phải một phần tử bấm được (widget)?  ô tick A / B (có thể không tick)

Cổng khoá trước (204 §4.1 bước 5), mẫu số = mọi mẫu đã gán (kể cả "không rõ" — tính là KHÔNG đúng G):
  chọn đúng G ≥ 75%  ∧  "cả hai đều đúng" ≤ 15%  ∧  D không phải widget ≤ 10%
Trượt lần 1 ⇒ sửa pata_true_d.py, dựng lại, `build --lan 2` (mẫu MỚI, không trùng lần 1).
Trượt lần 2 ⇒ DỪNG C2.
"""
import os, sys, json, math, random, glob, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
SEED = 20260925
N_AUDIT = 100
NG_DUNG, NG_CAHAI, NG_KWIDGET = 0.75, 0.15, 0.10
MAU = {"A": (255, 128, 0), "B": (0, 110, 255)}


def outdir(lan):
    return os.path.join(ROOT, "pata", f"audit_trueD_lan{lan}")


def render(r, g_letter, path):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(os.path.join(ROOT, r["image"])).convert("RGB")
    W, H = im.size
    sx, sy = W / r["w"], H / r["h"]
    boxes = {g_letter: r["box_G"], ("B" if g_letter == "A" else "A"): r["box_D"]}
    full = im.copy()
    d = ImageDraw.Draw(full)
    lw = max(4, W // 180)
    try:
        font = ImageFont.load_default(size=max(28, W // 22))
    except TypeError:
        font = ImageFont.load_default()
    for L in ("A", "B"):
        b = boxes[L]
        x1, y1, x2, y2 = b[0] * sx, b[1] * sy, b[2] * sx, b[3] * sy
        d.rectangle([x1, y1, x2, y2], outline=MAU[L], width=lw)
        tb = d.textbbox((0, 0), L, font=font)
        tw, th_ = tb[2] - tb[0] + 12, tb[3] - tb[1] + 12
        # nhãn đặt NGOÀI khung (phía trên, không có chỗ thì phía dưới) để không che nội dung phần tử
        ly = y1 - th_ - 2 if y1 - th_ - 2 >= 0 else min(H - th_, y2 + 2)
        lx = min(max(0, x1), W - tw)
        d.rectangle([lx, ly, lx + tw, ly + th_], fill=MAU[L])
        d.text((lx + 6 - tb[0], ly + 6 - tb[1]), L, fill=(255, 255, 255), font=font)
    th = 760
    left = full.resize((int(W * th / H), th))
    # khung phóng quanh hợp hai hộp
    G, D = r["box_G"], r["box_D"]
    ux1, uy1 = min(G[0], D[0]) * sx, min(G[1], D[1]) * sy
    ux2, uy2 = max(G[2], D[2]) * sx, max(G[3], D[3]) * sy
    cx, cy = (ux1 + ux2) / 2, (uy1 + uy2) / 2
    half = max(ux2 - ux1, uy2 - uy1, 300) * 0.75
    crop = full.crop((int(max(0, cx - half)), int(max(0, cy - half)),
                      int(min(W, cx + half)), int(min(H, cy + half))))
    s = min(560 / crop.width, th / crop.height)
    right = crop.resize((max(1, int(crop.width * s)), max(1, int(crop.height * s))))
    can = Image.new("RGB", (left.width + right.width + 12, th), (40, 40, 40))
    can.paste(left, (0, 0)); can.paste(right, (left.width + 12, 0))
    can.save(path, quality=85)


HTML = r"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Audit cặp G/D</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#fff;--fg:#1a1a1a;--mut:#666;--card:#f5f5f4}
@media (prefers-color-scheme:dark){:root{--bg:#161616;--fg:#eee;--mut:#aaa;--card:#222}}
body{background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;margin:0 auto;max-width:1150px;padding:16px}
.it{background:var(--card);border-radius:8px;padding:12px;margin:14px 0}
.it img{max-width:100%;height:auto;display:block;margin:8px 0}
.meta{color:var(--mut);font-size:13px}.ins{font-size:18px;font-weight:600}
label{display:inline-block;margin:4px 14px 4px 0;cursor:pointer}
.q{margin-top:6px}.done{outline:2px solid #16a34a}
.A{color:#ff8000;font-weight:700}.B{color:#006eff;font-weight:700}
#bar{position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--mut);z-index:2}
button{font:inherit;padding:6px 14px;margin-right:8px}
</style></head><body>
<div id="bar">Người gán: <input id="who" size="10"> · <span id="cnt"></span>
<button onclick="save()">Tải nhãn (.json)</button>
<div class="meta">Mỗi mẫu có hai khung <span class="A">A (cam)</span> và <span class="B">B (xanh)</span>. Đọc câu hướng dẫn rồi trả lời:
(1) câu nhắm tới khung nào; (2) khung nào không phải một phần tử bấm được. Không có đáp án gợi ý trên ảnh.</div></div>
<div id="list"></div>
<script>
const ITEMS = __ITEMS__;
const KEY = "pata_audit_trueD___LAN__";
let lab = {}; try { lab = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}
const C = [["A","Khung A"],["B","Khung B"],["ca_hai","Cả hai đều đúng"],["khong_cai_nao","Không khung nào"],["khong_ro","Không rõ"]];
const list = document.getElementById("list");
ITEMS.forEach((x, i) => {
  const L = lab[x.id] || (lab[x.id] = {c: null, na: false, nb: false});
  const d = document.createElement("div"); d.className = "it";
  const r1 = C.map(([v, t]) => `<label><input type="radio" name="c${x.id}" value="${v}" ${L.c===v?"checked":""}> ${t}</label>`).join("");
  d.innerHTML = `<div class="meta">#${i+1}/${ITEMS.length} · mã ${x.id}</div>
    <div class="ins">${x.instr}</div><div class="meta">Mục tiêu: ${x.goal}</div>
    <img loading="lazy" src="${x.img}">
    <div class="q"><b>(1) Câu nhắm tới:</b> ${r1}</div>
    <div class="q"><b>(2) Không phải widget:</b>
      <label><input type="checkbox" data-k="na" ${L.na?"checked":""}> <span class="A">A</span></label>
      <label><input type="checkbox" data-k="nb" ${L.nb?"checked":""}> <span class="B">B</span></label></div>`;
  d.querySelectorAll("input[type=radio]").forEach(el => el.onchange = () => { L.c = el.value; upd(); });
  d.querySelectorAll("input[type=checkbox]").forEach(el => el.onchange = () => { L[el.dataset.k] = el.checked; upd(); });
  function upd(){ d.classList.toggle("done", !!L.c); persist(); }
  if (L.c) d.classList.add("done");
  list.appendChild(d);
});
function persist(){ try { localStorage.setItem(KEY, JSON.stringify(lab)); } catch (e) {} cnt(); }
function cnt(){ document.getElementById("cnt").textContent = ITEMS.filter(x => lab[x.id] && lab[x.id].c).length + "/" + ITEMS.length + " đã gán"; }
function save(){
  const who = document.getElementById("who").value.trim() || "annotator";
  const done = {}; for (const k in lab) if (lab[k].c) done[k] = lab[k];
  const blob = new Blob([JSON.stringify({who, lan: __LAN__, labels: done}, null, 1)], {type: "application/json"});
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
  a.download = `audit_trueD_lan__LAN___${who}.json`; a.click();
}
cnt();
</script></body></html>"""


def build(a):
    out = outdir(a.lan)
    if os.path.exists(os.path.join(out, "manifest.json")) and not a.force:
        sys.exit(f"{out}/manifest.json đã có — audit lần {a.lan} đã dựng. Dựng lại sẽ đổi mẫu; thêm --force nếu chắc.")
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "pata", "val400_trueD.jsonl"), encoding="utf-8")]
    recs.sort(key=lambda r: (r["episode_id"], r["step_id"]))
    da_dung = set()
    for lan in range(1, a.lan):
        m = json.load(open(os.path.join(outdir(lan), "manifest.json")))
        da_dung |= {(k["episode_id"], k["step_id"]) for k in m["key"]}
    pool = [r for r in recs if (r["episode_id"], r["step_id"]) not in da_dung]
    rnd = random.Random(SEED + a.lan - 1)
    n = min(N_AUDIT, len(pool))
    if n < N_AUDIT:
        print(f"⚠️ chỉ còn {len(pool)} cặp chưa audit — dựng {n} mẫu")
    pick = rnd.sample(pool, n)
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    items, key = [], []
    for i, r in enumerate(pick):
        g = rnd.choice("AB")
        fn = f"img/{i:03d}.jpg"
        render(r, g, os.path.join(out, fn))
        items.append({"id": i, "img": fn, "instr": r["target_instruction"].strip(), "goal": r["goal"].strip()})
        key.append({"id": i, "G": g, "episode_id": r["episode_id"], "step_id": r["step_id"],
                    "cls": r["cls"], "name_G": r["name_G"], "name_D": r["name_D"], "dist_px": r["dist_px"]})
    html = HTML.replace("__ITEMS__", json.dumps(items, ensure_ascii=False)).replace("__LAN__", str(a.lan))
    open(os.path.join(out, "audit.html"), "w", encoding="utf-8").write(html)
    json.dump({"seed": SEED + a.lan - 1, "lan": a.lan, "n_pool": len(pool), "n": n,
               "nguong": {"dung_G_min": NG_DUNG, "ca_hai_max": NG_CAHAI, "D_khong_widget_max": NG_KWIDGET},
               "key": key}, open(os.path.join(out, "manifest.json"), "w"), indent=1, ensure_ascii=False)
    c = collections.Counter(k["G"] for k in key)
    print(f"Dựng {n} mẫu (G ở A: {c['A']}, ở B: {c['B']}) từ {len(pool)} cặp eligible")
    print(f"→ mở {out}/audit.html · gán xong bấm 'Tải nhãn' rồi chép tệp .json vào {out}/")


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - hw), min(1.0, c + hw)


def doc(a):
    out = outdir(a.lan)
    man = json.load(open(os.path.join(out, "manifest.json")))
    key = {k["id"]: k for k in man["key"]}
    files = sorted(glob.glob(os.path.join(out, "audit_trueD_*.json")))
    if not files:
        sys.exit(f"chưa có tệp nhãn audit_trueD_*.json trong {out}")
    f = max(files, key=lambda p: len(json.load(open(p, encoding="utf-8"))["labels"]))
    lab = {int(k): v for k, v in json.load(open(f, encoding="utf-8"))["labels"].items()}
    n = len(lab)
    print(f"Tệp nhãn: {os.path.basename(f)} · {n}/{len(key)} mẫu đã gán")
    if n < len(key):
        print(f"⚠️ còn {len(key) - n} mẫu chưa gán — cổng chỉ đọc khi gán đủ")
    dung = sum(v["c"] == key[i]["G"] for i, v in lab.items())
    ca_hai = sum(v["c"] == "ca_hai" for i, v in lab.items())
    # D không phải widget: tick đúng ô của khung D
    kw_D = sum(v["nb"] if key[i]["G"] == "A" else v["na"] for i, v in lab.items())
    kw_G = sum(v["na"] if key[i]["G"] == "A" else v["nb"] for i, v in lab.items())
    c = collections.Counter(("G" if v["c"] == key[i]["G"] else "D" if v["c"] in ("A", "B") else v["c"])
                            for i, v in lab.items())
    print("-" * 70)
    print(f"  phân bố trả lời: {dict(c)}")
    rows = [("chọn đúng G", dung, NG_DUNG, ">="), ("cả hai đều đúng", ca_hai, NG_CAHAI, "<="),
            ("D không phải widget", kw_D, NG_KWIDGET, "<=")]
    ok_all = n == len(key)
    for ten, k, ng, op in rows:
        lo, hi = wilson(k, n)
        ok = (k / n >= ng) if op == ">=" else (k / n <= ng)
        ok_all &= ok
        print(f"  {ten:22} {k:3}/{n} = {k / n:6.1%}  Wilson95 [{lo:.1%}; {hi:.1%}]  "
              f"ngưỡng {op} {ng:.0%}  {'ĐẠT' if ok else 'KHÔNG ĐẠT'}")
    print(f"  (tham khảo) G không phải widget: {kw_G}/{n}")
    sai = [i for i, v in lab.items() if v["c"] != key[i]["G"]]
    print(f"  mẫu không chọn đúng G: {sai}")
    print("-" * 70)
    if ok_all:
        print(f"⇒ AUDIT LẦN {a.lan}: ĐẠT — P0 xong, sang P1 (harness/kaggle_pata_p1.md)")
    elif a.lan == 1:
        print("⇒ AUDIT LẦN 1: KHÔNG ĐẠT — sửa pata_true_d.py theo các mẫu sai, dựng lại, rồi `build --lan 2`")
    else:
        print("⇒ AUDIT LẦN 2: KHÔNG ĐẠT — DỪNG C2 (204 §4.1)")
    json.dump({"lan": a.lan, "n": n, "dung_G": dung, "ca_hai": ca_hai, "D_khong_widget": kw_D,
               "G_khong_widget": kw_G, "dat": ok_all, "tep_nhan": os.path.basename(f)},
              open(os.path.join(out, "ket_qua.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "doc"])
    ap.add_argument("--lan", type=int, default=1)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    {"build": build, "doc": doc}[a.cmd](a)
