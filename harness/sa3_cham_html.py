# -*- coding: utf-8 -*-
"""Dựng trang HTML tự chứa để người chấm mù audit verifier thao tác (SA-SPICE-v3).

  ~/.venvs/thesis/bin/python harness/sa3_cham_html.py --dir runs/sa_spice_v3/audit_pilot2 --ids human_ids.json --out CHAM_TAY.html

Mỗi dòng: ảnh màn hình (vòng đỏ = chỗ chạm đúng nếu có), mục tiêu, các bước đã làm, việc người dùng thật sự
làm ở bước này (đáp án), câu mô hình viết, ba nút. Không hiện nhãn verifier lẫn nhãn Claude.
Kết quả tải về dạng jsonl {"id", "label"} với label ∈ correct | wrong | unclear — đúng định dạng `sa3_action_verify.py score --human`.
"""
import os, io, json, base64, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TA = os.path.join(ROOT, "harness", "dg1_cache", "train_ac")
VI = {"tap": "Chạm / bấm", "scroll": "Cuộn / vuốt", "back": "Quay lại", "type": "Gõ chữ", "open_app": "Mở ứng dụng"}

CSS = """
:root{--bg:#f6f6f4;--card:#fff;--fg:#1d1d1b;--mut:#6b6b66;--line:#e2e2dc;--soft:#f0f0ec;--ok:#1f7a3a;--no:#b3261e;--un:#8a6d00;--acc:#2f5bd3;--gold:#eef3ff;--cand:#fff6e6}
@media (prefers-color-scheme:dark){:root{--bg:#161615;--card:#21211f;--fg:#ececea;--mut:#9a9a94;--line:#34342f;--soft:#2a2a27;--ok:#4cc26f;--no:#ff7a70;--un:#e0b23a;--acc:#7c9cff;--gold:#1f2740;--cand:#3a2f1a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{position:sticky;top:0;z-index:2;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
h1{font-size:17px;margin:0;flex:1 1 auto}.bar{height:6px;background:var(--line);border-radius:3px;width:160px;overflow:hidden}.bar i{display:block;height:100%;background:var(--acc)}
button{font:inherit;cursor:pointer;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:8px;padding:6px 12px}
.guide{max-width:1040px;margin:14px auto;padding:12px 16px;background:var(--card);border:1px solid var(--line);border-radius:12px}
.guide p{margin:4px 0}.guide table{border-collapse:collapse;font-size:14px;margin-top:6px}.guide td{padding:3px 10px;border-top:1px solid var(--line)}
.card{max-width:1040px;margin:14px auto;background:var(--card);border:1px solid var(--line);border-radius:12px;display:flex;gap:18px;padding:14px;scroll-margin-top:70px}
.card.cur{outline:2px solid var(--acc)}.card img{width:200px;height:auto;border-radius:8px;border:1px solid var(--line);cursor:zoom-in;flex:none;align-self:flex-start}
.card img.big{width:400px}.body{flex:1;min-width:0}
.ctx{background:var(--soft);border-radius:8px;padding:8px 10px;font-size:14px}.ctx b{color:var(--mut);font-weight:600}
.ctx ol{margin:4px 0 0;padding-left:20px;color:var(--mut)}
.box{border-radius:8px;padding:8px 10px;margin-top:10px}.gold{background:var(--gold)}.cand{background:var(--cand)}
.box .h{font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.03em}.box .t{font-size:16px;font-weight:600}
.act{display:inline-block;font-size:13px;font-weight:600;padding:1px 9px;border-radius:12px;background:var(--line);margin-left:6px;vertical-align:1px}
.q{margin-top:12px;font-weight:600}.btns{display:flex;gap:8px;margin-top:6px;flex-wrap:wrap}.btns button{min-width:120px}
.b-ok.on{background:var(--ok);color:#fff;border-color:var(--ok)}.b-no.on{background:var(--no);color:#fff;border-color:var(--no)}.b-un.on{background:var(--un);color:#fff;border-color:var(--un)}
@media (max-width:680px){.card{flex-direction:column}.card img,.card img.big{width:100%}}
"""

GUIDE = """<div class="guide">
<p><b>Bối cảnh.</b> Một người đang dùng điện thoại để làm một <b>mục tiêu</b> (vd. đặt khách sạn). Ở mỗi bước, người chú thích đã ghi lại <b>việc người đó thật sự làm</b> (khung xanh, đây là đáp án). Mô hình nhìn cùng màn hình và viết <b>một câu hướng dẫn</b> (khung vàng).</p>
<p><b>Câu hỏi duy nhất:</b> câu mô hình viết có bảo làm <b>cùng loại thao tác</b> với đáp án không? Năm loại: <b>bấm</b> · <b>cuộn/vuốt</b> · <b>quay lại</b> · <b>gõ chữ</b> · <b>mở ứng dụng</b>. Chỉ nhìn động từ. Bấm sai nút, gõ sai chữ, cuộn sai hướng vẫn tính là <b>cùng loại</b> (phần đó có thước khác chấm).</p>
<table>
<tr><td>Click on the search icon → Click on Dance Classes</td><td><b>1</b> cùng loại (đều bấm)</td></tr>
<tr><td>Swipe up → Click on Filters</td><td><b>2</b> khác loại (vuốt ≠ bấm)</td></tr>
<tr><td>Go back → Open the vimeo app</td><td><b>2</b> khác loại</td></tr>
<tr><td>Type Berlin → Type Toronto</td><td><b>1</b> cùng loại</td></tr>
<tr><td>Swipe down → Scroll up</td><td><b>1</b> cùng loại (không xét hướng)</td></tr>
<tr><td>Click the back arrow → Go back</td><td><b>3</b> không rõ (cùng tác dụng, khác thao tác)</td></tr>
</table>
<p style="color:var(--mut);margin-top:8px">Phím tắt 1 / 2 / 3 (tự sang dòng kế), ↑ ↓ để di chuyển. Bấm ảnh để phóng to. Tiến độ tự lưu trong trình duyệt. Xong thì bấm “Tải kết quả”.</p>
</div>"""

JS = r"""
const D=__DATA__;const KEY="__KEY__";let L={};try{L=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
let cur=0;const list=document.getElementById("list");
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
D.forEach((r,n)=>{const c=document.createElement("div");c.className="card";c.id="c"+n;
const hist=r.hist.length?`<ol>${r.hist.map(h=>`<li>${esc(h)}</li>`).join("")}</ol>`:` <span style="color:var(--mut)">(chưa làm gì, đây là bước đầu)</span>`;
c.innerHTML=`<img src="${r.img}" alt="ảnh màn hình" title="${esc(r.note)}"><div class="body">
<div class="ctx"><b>Mục tiêu:</b> ${esc(r.goal)}<br><b>Đã làm trước đó:</b>${hist}</div>
<div class="box gold"><div class="h">Việc người dùng thật sự làm ở bước này <span class="act">${esc(r.actvi)}</span></div><div class="t">${esc(r.gold)}</div></div>
<div class="box cand"><div class="h">Câu mô hình viết</div><div class="t">${esc(r.cand)}</div></div>
<div class="q">Câu mô hình có bảo làm cùng loại thao tác không?</div>
<div class="btns"><button class="b-ok">1 · Cùng loại</button><button class="b-no">2 · Khác loại</button><button class="b-un">3 · Không rõ</button></div>
<div style="color:var(--mut);font-size:12px;margin-top:6px">#${r.id} · ${esc(r.note)}</div></div>`;
c.querySelector("img").onclick=e=>{e.stopPropagation();e.target.classList.toggle("big")};
[["b-ok","correct"],["b-no","wrong"],["b-un","unclear"]].forEach(([k,v])=>c.querySelector("."+k).onclick=e=>{e.stopPropagation();cur=n;set(v)});
c.onclick=()=>{cur=n;paint()};list.appendChild(c)});
function save(){try{localStorage.setItem(KEY,JSON.stringify(L))}catch(e){}}
function paint(){D.forEach((r,n)=>{const c=document.getElementById("c"+n),v=L[r.id];c.classList.toggle("cur",n===cur);
c.querySelector(".b-ok").classList.toggle("on",v==="correct");c.querySelector(".b-no").classList.toggle("on",v==="wrong");c.querySelector(".b-un").classList.toggle("on",v==="unclear")});
const k=D.filter(r=>L[r.id]).length;document.getElementById("cnt").textContent=k+"/"+D.length+" dòng";document.getElementById("pg").style.width=(100*k/D.length)+"%"}
function go(n){cur=n;paint();document.getElementById("c"+cur).scrollIntoView({behavior:"smooth",block:"start"})}
function set(v){L[D[cur].id]=v;save();if(cur<D.length-1)go(cur+1);else paint()}
document.addEventListener("keydown",e=>{const m={"1":"correct","2":"wrong","3":"unclear"}[e.key];if(m){e.preventDefault();set(m)}
if(e.key==="ArrowDown"&&cur<D.length-1){e.preventDefault();go(cur+1)}if(e.key==="ArrowUp"&&cur>0){e.preventDefault();go(cur-1)}});
document.getElementById("dl").onclick=()=>{const out=D.map(r=>({id:r.id,label:L[r.id]||null}));const miss=out.filter(o=>!o.label).length;
if(miss&&!confirm("Còn "+miss+" dòng chưa chấm. Vẫn tải?"))return;
const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([out.map(o=>JSON.stringify(o)).join("\n")+"\n"],{type:"application/json"}));a.download="__FN__";a.click()};
paint();
"""


def main():
    from PIL import Image, ImageDraw
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True); ap.add_argument("--ids", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    D = a.dir
    ids = json.load(open(os.path.join(D, a.ids)))
    B = {r["id"]: r for r in map(json.loads, open(os.path.join(D, "audit_blind.jsonl"), encoding="utf-8"))}
    K = {r["id"]: r for r in map(json.loads, open(os.path.join(D, "audit_key.jsonl"), encoding="utf-8"))}
    need = {K[i]["key"] for i in ids}
    A = {}
    for l in open(os.path.join(TA, "train.jsonl"), encoding="utf-8"):
        r = json.loads(l); k = f"{r['episode_id']}_{r['step_id']}"
        if k in need:
            A[k] = r
    items = []
    for i in ids:
        r = A[K[i]["key"]]
        im = Image.open(os.path.join(TA, r["image"])).convert("RGB"); W, H = im.size
        s = 400 / W; im = im.resize((400, int(H * s)))
        act, note = r["action"], "ảnh màn hình lúc đó"
        if "x" in act:
            d = ImageDraw.Draw(im); x, y = act["x"] * s, act["y"] * s
            d.ellipse([x - 14, y - 14, x + 14, y + 14], outline=(230, 30, 30), width=4); d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(230, 30, 30))
            note = "vòng đỏ = chỗ người dùng đã chạm"
        b = io.BytesIO(); im.save(b, "JPEG", quality=72)
        items.append({"id": i, "actvi": VI[B[i]["gold_action"]], "gold": B[i]["gold"], "cand": B[i]["cand"],
                      "goal": r.get("goal", ""), "hist": r.get("history", []),
                      "img": "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode(), "note": note})
    name = os.path.basename(os.path.normpath(D))
    js = JS.replace("__DATA__", json.dumps(items, ensure_ascii=False)).replace("__KEY__", f"sa3_cham_tay_{name}").replace("__FN__", f"cham_tay_{name}.jsonl")
    page = (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Chấm loại thao tác</title><style>{CSS}</style></head><body>'
            f'<header><h1>Chấm loại thao tác · <span id="cnt"></span></h1><div class="bar"><i id="pg"></i></div><button id="dl">Tải kết quả (.json)</button></header>'
            f'{GUIDE}<main id="list"></main><script>{js}</script></body></html>')
    out = os.path.join(D, a.out)
    open(out, "w", encoding="utf-8").write(page)
    print(out, f"{os.path.getsize(out) / 1e6:.2f} MB", len(items), "dòng", flush=True)


if __name__ == "__main__":
    main()
