# -*- coding: utf-8 -*-
"""
PATA · A1 — audit mù proxy box (report/185 §2 "Audit box trước train dài"). 0 GPU, chạy trên WSL.

    ~/.venvs/thesis/bin/python harness/pata_audit.py build      # dựng mẫu + trang gán nhãn
    ~/.venvs/thesis/bin/python harness/pata_audit.py doc        # đọc nhãn, tính tỉ lệ lỗi

Quần thể lấy mẫu = các bước chạm Train-proper CÓ ẢNH trên máy (8 shard rải đều do keo_anh_val.py
kéo về, ~3.900 bước). ⚠️ Phải khai khi báo: tỉ lệ ước lượng trên 8/76 shard, không phải trên
toàn 41.099 — nhưng các shard rải đều theo thứ tự thu thập nên không có lý do nghiêng hệ thống.

Thiết kế mẫu (hạt 20260923, khoá trong tệp audit/manifest.json):
  U   150  ngẫu nhiên đều trong các bước có box      → xác suất chọn biết trước = 150/N ⇒ ƯỚC LƯỢNG
  S1   20  widget nhỏ (area_share ≤ p10)             ┐
  S2   20  container (area_share ≥ p95)              │ lấy DƯ để CHẨN ĐOÁN, không gộp vào tỉ lệ
  S3   20  sát biên màn (≤ 10 px)                    │ chung (khi gộp phải reweight — `doc` làm)
  S4   20  tên chỉ từ OCR (name_src = ocr)           │
  S5   20  không có tên (name_src rỗng)              ┘
  N   mọi  bước KHÔNG có box nhưng có ảnh             → xem có phần tử rõ ràng tại điểm chạm không
Trang gán nhãn ẨN tầng của từng mẫu (mù) và xáo thứ tự. 60 mẫu đầu (trong thứ tự đã xáo) là
phần CHỒNG cho người gán thứ hai (mở trang với `#overlap`).

Nhãn:
  dung        box đúng phần tử mà câu hướng dẫn nhắm tới
  nhe         lỗi nhẹ: box là con/cha của phần tử đúng nhưng vẫn nhận ra đúng widget
  nang_dis    lỗi nặng: box thuộc phần tử KHÁC (distractor)
  nang_stale  lỗi nặng: box lệch/không khớp nội dung màn (stale)
  khong_ro    không xác định được
  (mẫu N) co_node / khong_node: tại điểm chạm có / không có một phần tử rõ ràng

Ngưỡng khoá trước (§2): lỗi nặng (nang_dis + nang_stale) trên tầng U > 5% ⇒ sửa labeler, dựng lại.
"""
import os, sys, json, math, random, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
OUT = os.path.join(ROOT, "pata", "audit")
SEED = 20260923
N_U, N_S, N_OVERLAP = 150, 20, 60
NGUONG_NANG = 0.05


def render(r, path):
    from PIL import Image, ImageDraw
    im = Image.open(os.path.join(ROOT, r["image"])).convert("RGB")
    W, H = im.size
    sx, sy = W / r["w"], H / r["h"]
    x, y = r["action"]["x"] * sx, r["action"]["y"] * sy
    full = im.copy()
    d = ImageDraw.Draw(full)
    lw = max(3, W // 200)
    if r["box"]:
        x1, y1, x2, y2 = r["box"][0] * sx, r["box"][1] * sy, r["box"][2] * sx, r["box"][3] * sy
        d.rectangle([x1, y1, x2, y2], outline=(255, 0, 0), width=lw)
    rad = max(10, W // 60)
    d.ellipse([x - rad, y - rad, x + rad, y + rad], outline=(0, 200, 0), width=lw)
    th = 720
    left = full.resize((int(W * th / H), th))
    # khung phóng quanh box (hoặc quanh điểm chạm nếu không có box)
    if r["box"]:
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        half = max(x2 - x1, y2 - y1, 200) * 1.2
    else:
        cx, cy, half = x, y, 250
    crop = full.crop((int(max(0, cx - half)), int(max(0, cy - half)),
                      int(min(W, cx + half)), int(min(H, cy + half))))
    s = min(480 / crop.width, th / crop.height)
    right = crop.resize((max(1, int(crop.width * s)), max(1, int(crop.height * s))))
    can = Image.new("RGB", (left.width + right.width + 12, th), (40, 40, 40))
    can.paste(left, (0, 0)); can.paste(right, (left.width + 12, 0))
    can.save(path, quality=82)


HTML = r"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Audit box PATA</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#fff;--fg:#1a1a1a;--mut:#666;--card:#f5f5f4;--acc:#b91c1c}
@media (prefers-color-scheme:dark){:root{--bg:#161616;--fg:#eee;--mut:#aaa;--card:#222;--acc:#f87171}}
body{background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;margin:0 auto;max-width:1100px;padding:16px}
.it{background:var(--card);border-radius:8px;padding:12px;margin:14px 0}
.it img{max-width:100%;height:auto;display:block;margin:8px 0}
.meta{color:var(--mut);font-size:13px}.ins{font-size:17px;font-weight:600}
label{display:inline-block;margin:4px 14px 4px 0;cursor:pointer}
.done{outline:2px solid #16a34a}
#bar{position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--mut);z-index:2}
button{font:inherit;padding:6px 14px;margin-right:8px}
</style></head><body>
<div id="bar">Người gán: <input id="who" size="10"> · <span id="cnt"></span>
<button onclick="save()">Tải nhãn (.json)</button> <span class="meta">Khung đỏ = box proxy · vòng xanh = điểm chạm thật. Hỏi: khung đỏ có đúng phần tử mà câu hướng dẫn nhắm tới không?</span></div>
<div id="list"></div>
<script>
const ITEMS = __ITEMS__;
const OV = location.hash === "#overlap";
const KEY = "pata_audit_" + (OV ? "ov" : "all");
let lab = {}; try { lab = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}
const L1 = [["dung","Đúng"],["nhe","Lỗi nhẹ (con/cha, vẫn đúng widget)"],["nang_dis","Lỗi nặng: phần tử KHÁC"],["nang_stale","Lỗi nặng: lệch/stale"],["khong_ro","Không rõ"]];
const L2 = [["co_node","Có phần tử rõ ràng tại điểm chạm"],["khong_node","Không có"],["khong_ro","Không rõ"]];
const list = document.getElementById("list");
const show = ITEMS.filter(x => !OV || x.overlap);
show.forEach((x, i) => {
  const d = document.createElement("div"); d.className = "it"; d.id = "i" + x.id;
  const opts = (x.has_box ? L1 : L2).map(([v, t]) =>
    `<label><input type="radio" name="r${x.id}" value="${v}" ${lab[x.id]===v?"checked":""}> ${t}</label>`).join("");
  d.innerHTML = `<div class="meta">#${i+1}/${show.length} · mã ${x.id}</div>
    <div class="ins">${x.instr}</div><div class="meta">Mục tiêu: ${x.goal}</div>
    <img loading="lazy" src="${x.img}"><div>${opts}</div>`;
  d.querySelectorAll("input").forEach(el => el.onchange = () => { lab[x.id] = el.value; persist(); d.classList.add("done"); });
  if (lab[x.id]) d.classList.add("done");
  list.appendChild(d);
});
function persist(){ try { localStorage.setItem(KEY, JSON.stringify(lab)); } catch (e) {} cnt(); }
function cnt(){ document.getElementById("cnt").textContent = show.filter(x => lab[x.id]).length + "/" + show.length + " đã gán"; }
function save(){
  const who = document.getElementById("who").value.trim() || "annotator";
  const blob = new Blob([JSON.stringify({who, overlap_only: OV, labels: lab}, null, 1)], {type: "application/json"});
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
  a.download = `audit_${who}${OV ? "_overlap" : ""}.json`; a.click();
}
cnt();
</script></body></html>"""


def build():
    recs = [json.loads(l) for l in open(os.path.join(ROOT, "pata", "train_proper.jsonl"), encoding="utf-8")]
    loc = [r for r in recs if os.path.exists(os.path.join(ROOT, r["image"]))]
    boxed = sorted((r for r in loc if r["kl_ok"]), key=lambda r: (r["episode_id"], r["step_id"]))
    nobox = sorted((r for r in loc if not r["kl_ok"]), key=lambda r: (r["episode_id"], r["step_id"]))
    rnd = random.Random(SEED)
    U = rnd.sample(boxed, N_U)
    ids_u = {(r["episode_id"], r["step_id"]) for r in U}
    rest = [r for r in boxed if (r["episode_id"], r["step_id"]) not in ids_u]
    a = sorted(r["area_share"] for r in boxed)
    p10, p95 = a[int(0.10 * len(a))], a[int(0.95 * len(a))]
    edge = lambda r: (r["box"][0] <= 10 or r["box"][1] <= 10 or r["box"][2] >= r["w"] - 10
                      or r["box"][3] >= r["h"] - 10)
    tang = {"S1_nho": lambda r: r["area_share"] <= p10, "S2_container": lambda r: r["area_share"] >= p95,
            "S3_bien": edge, "S4_ocr": lambda r: r["name_src"] == "ocr",
            "S5_khongten": lambda r: r["name_src"] is None}
    chosen = [("U", r) for r in U]
    used = set(ids_u)
    for t, f in tang.items():
        pool = [r for r in rest if f(r) and (r["episode_id"], r["step_id"]) not in used]
        pick = rnd.sample(pool, min(N_S, len(pool)))
        used |= {(r["episode_id"], r["step_id"]) for r in pick}
        chosen += [(t, r) for r in pick]
    chosen += [("N_khongbox", r) for r in nobox]
    rnd.shuffle(chosen)
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    items, key = [], []
    for i, (t, r) in enumerate(chosen):
        fn = f"img/{i:03d}.jpg"
        render(r, os.path.join(OUT, fn))
        items.append({"id": i, "img": fn, "instr": r["target_instruction"].strip(),
                      "goal": r["goal"].strip(), "has_box": r["kl_ok"], "overlap": i < N_OVERLAP})
        key.append({"id": i, "tang": t, "episode_id": r["episode_id"], "step_id": r["step_id"],
                    "area_share": r["area_share"], "name_src": r["name_src"], "box": r["box"]})
        if i % 50 == 0:
            print(f"  vẽ {i}/{len(chosen)}", flush=True)
    html = HTML.replace("__ITEMS__", json.dumps(items, ensure_ascii=False))
    open(os.path.join(OUT, "audit.html"), "w", encoding="utf-8").write(html)
    json.dump({"seed": SEED, "N_local_boxed": len(boxed), "N_local_nobox": len(nobox),
               "N_U": N_U, "p_chon_U": N_U / len(boxed), "p10_area": p10, "p95_area": p95,
               "ngưỡng_lỗi_nặng": NGUONG_NANG, "key": key},
              open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
    c = collections.Counter(t for t, _ in chosen)
    print(f"Dựng {len(chosen)} mẫu: {dict(c)} · quần thể có ảnh {len(boxed)} có box + {len(nobox)} không box")
    print(f"→ mở {OUT}/audit.html   (người gán thứ hai: audit.html#overlap — {N_OVERLAP} mẫu)")


def doc():
    man = json.load(open(os.path.join(OUT, "manifest.json")))
    key = {k["id"]: k for k in man["key"]}
    files = sorted(glob.glob(os.path.join(OUT, "audit_*.json")))
    if not files:
        sys.exit(f"chưa có tệp nhãn audit_*.json trong {OUT}")
    lab = {}
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        lab[os.path.basename(f)] = {int(k): v for k, v in d["labels"].items()}
        print(f"  {os.path.basename(f)}: {len(d['labels'])} nhãn · người gán {d['who']}")
    main = max(lab, key=lambda k: len(lab[k]))
    L = lab[main]
    print(f"Bộ nhãn chính: {main}")
    nang = lambda v: v in ("nang_dis", "nang_stale")
    by = collections.defaultdict(list)
    for i, v in L.items():
        by[key[i]["tang"]].append(v)
    print("-" * 70)
    for t in sorted(by):
        c = collections.Counter(by[t])
        n = len(by[t])
        if t == "N_khongbox":
            print(f"  {t:14} n={n:3}  " + " ".join(f"{k}={c[k]}" for k in ("co_node", "khong_node", "khong_ro")))
            continue
        e = sum(nang(v) for v in by[t])
        print(f"  {t:14} n={n:3}  nặng {e:3} = {e / n:6.1%}  nhẹ {c['nhe']:3}  đúng {c['dung']:3}  không rõ {c['khong_ro']}")
    u = [v for v in by.get("U", []) if v != "khong_ro"]
    if u:
        e = sum(nang(v) for v in u); n = len(u); p = e / n
        # Wilson 95%
        z = 1.96
        den = 1 + z * z / n
        c0 = (p + z * z / (2 * n)) / den
        hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
        print("-" * 70)
        print(f"TẦNG U (ước lượng quần thể): lỗi nặng {e}/{n} = {p:.1%}  Wilson95 [{max(0, c0 - hw):.1%}; {c0 + hw:.1%}]")
        print(f"⇒ {'VƯỢT' if p > NGUONG_NANG else 'DƯỚI'} ngưỡng khoá trước {NGUONG_NANG:.0%}"
              + (" — sửa labeler rồi dựng lại dữ liệu (§2)" if p > NGUONG_NANG else " — giữ box, đi tiếp"))
    if len(lab) >= 2:
        ks = list(lab)
        a, b = lab[ks[0]], lab[ks[1]]
        common = sorted(set(a) & set(b))
        if common:
            ag = sum(a[i] == b[i] for i in common) / len(common)
            cats = sorted({a[i] for i in common} | {b[i] for i in common})
            pe = sum((sum(a[i] == c for i in common) / len(common)) * (sum(b[i] == c for i in common) / len(common))
                     for c in cats)
            kappa = (ag - pe) / (1 - pe) if pe < 1 else 1.0
            dis = [i for i in common if a[i] != b[i]]
            print(f"Hai người gán: {len(common)} mẫu chung · đồng thuận {ag:.1%} · κ Cohen {kappa:.2f}")
            print(f"  cần adjudication {len(dis)} mẫu: {dis}")


if __name__ == "__main__":
    {"build": build, "doc": doc}[sys.argv[1] if len(sys.argv) > 1 else "build"]()
