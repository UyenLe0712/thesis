# -*- coding: utf-8 -*-
"""
C1 — Nghiên cứu nhỏ construct-validity (report/90 Giai đoạn C).
Dựng bộ chấm-tay từ 91 cặp teacher đã có trong cache pilot. HOÀN TOÀN OFFLINE, KHÔNG gọi API.

Mục đích: hỏi người "câu hướng dẫn này có giúp bạn chạm đúng nút trên màn hình này không?"
rồi đối chiếu với điểm của thước (action, target). Nếu tương quan thấp → thước không đo
thứ luận văn tuyên bố đo, và mọi kết quả phía sau mất ý nghĩa.

Sinh ra: harness/cv_study/rate_A.html, rate_B.html (hai người chấm, thứ tự khác nhau)
         harness/cv_study/items.json (đáp án + điểm thước, NGƯỜI CHẤM KHÔNG ĐƯỢC MỞ)

Chạy: ~/.venvs/thesis/bin/python harness/cv_build_items.py
"""
import os, sys, json, re, glob, base64, random, io, html
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from metric_v1_validate import canon_action, target_of, target_score

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, "dg1_cache", "mde_pilot", "gen.json")
OUT = os.path.join(HERE, "cv_study")
os.makedirs(OUT, exist_ok=True)
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")
IMG_W = 640          # đủ đọc nhãn nút, đủ nhẹ để nhúng thẳng vào HTML
JPEG_Q = 82


def find_episode(eid):
    hits = glob.glob(os.path.join(HF, "*", "test_output_json", "*", f"episode_{eid}.json"))
    return hits[0] if hits else None


def find_png(rel):
    hits = glob.glob(os.path.join(HF, "*", rel))
    return hits[0] if hits else None


def app_of(goal, actions):
    for a in actions or []:
        if a.get("action_type") == "open_app" and a.get("app_name"):
            return a["app_name"]
    m = re.search(r"\b(?:the |using |on |open )?([A-Z][A-Za-z0-9&\.\- ]{1,20}?) app\b", goal or "")
    return m.group(1).strip() if m else None


def img_datauri(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    im = im.resize((IMG_W, int(h * IMG_W / w)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_Q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def build():
    gen = json.load(open(GEN, encoding="utf-8"))
    items, skipped = [], []
    for rel, teacher in gen.items():
        m = re.search(r"episode_(\d+)_screenshot_(\d+)\.png", rel)
        if not m:
            skipped.append((rel, "tên ảnh lạ")); continue
        eid, si = int(m.group(1)), int(m.group(2))
        epath, ipath = find_episode(eid), find_png(rel)
        if not epath or not ipath:
            skipped.append((rel, "thiếu episode json hoặc ảnh")); continue
        o = json.load(open(epath, encoding="utf-8"))
        insts = o.get("step_instructions") or []
        if si >= len(insts):
            skipped.append((rel, f"si={si} ngoài tầm {len(insts)}")); continue
        gold = insts[si]
        goal = o.get("goal")
        app = app_of(goal, o.get("actions"))

        # điểm của thước — đúng công thức đang dùng ở trục ĐÚNG
        a_ok = canon_action(teacher) == canon_action(gold)
        ts = target_score(target_of(teacher), target_of(gold))
        match = bool(a_ok and ts >= 0.5)

        items.append({
            "id": f"{eid}_{si}", "png": rel, "eid": eid, "si": si,
            "goal": goal, "app": app,
            "gold": gold, "teacher": teacher,
            "metric": {"a_ok": a_ok, "target_score": round(ts, 4), "match": match,
                       "t_target_teacher": target_of(teacher), "t_target_gold": target_of(gold),
                       "t_action_teacher": canon_action(teacher), "t_action_gold": canon_action(gold)},
            "img": img_datauri(ipath),
        })
    return items, skipped


TPL_HEAD = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chấm hướng dẫn — người {rater}</title><style>
:root{{--bg:#faf9f7;--fg:#1a1a1a;--mut:#666;--line:#ddd;--card:#fff;--acc:#2d5f8a}}
@media(prefers-color-scheme:dark){{:root{{--bg:#16181c;--fg:#e8e6e3;--mut:#999;--line:#333;--card:#1e2126;--acc:#7aa9d4}}}}
*{{box-sizing:border-box}}
body{{margin:0;font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--fg)}}
header{{position:sticky;top:0;background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px;z-index:9;display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
header b{{font-size:15px}} .prog{{color:var(--mut);font-size:13px}}
button{{font:inherit;padding:7px 14px;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:7px;cursor:pointer}}
button.pri{{background:var(--acc);color:#fff;border-color:var(--acc)}}
main{{max-width:1000px;margin:0 auto;padding:16px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;margin-bottom:22px;display:grid;grid-template-columns:300px 1fr;gap:22px}}
@media(max-width:760px){{.card{{grid-template-columns:1fr}}}}
.shot img{{width:100%;border:1px solid var(--line);border-radius:8px;cursor:zoom-in}}
.shot img.zoom{{position:fixed;inset:2vh auto 2vh 50%;transform:translateX(-50%);width:auto;height:96vh;z-index:99;cursor:zoom-out;box-shadow:0 8px 40px #0009}}
.goal{{font-size:13px;color:var(--mut);margin-bottom:14px}}
.goal b{{color:var(--fg);font-weight:600}}
.cand{{border:1px solid var(--line);border-radius:9px;padding:13px;margin-bottom:12px}}
.cand .txt{{font-size:16px;margin-bottom:11px}}
.cand .tag{{display:inline-block;font-size:11px;color:var(--mut);border:1px solid var(--line);border-radius:4px;padding:1px 6px;margin-right:8px;vertical-align:2px}}
.opts{{display:flex;gap:6px;flex-wrap:wrap}}
.opts label{{flex:1;min-width:118px;font-size:13px;border:1px solid var(--line);border-radius:6px;padding:7px 9px;cursor:pointer}}
.opts input{{margin-right:6px}}
.opts label:has(input:checked){{border-color:var(--acc);background:color-mix(in srgb,var(--acc) 12%,transparent)}}
.flag{{margin-top:9px;font-size:13px;color:var(--mut)}}
.done{{opacity:.5}}
#bar{{position:fixed;left:0;bottom:0;width:100%;background:var(--card);border-top:1px solid var(--line);padding:9px 16px;display:flex;gap:12px;align-items:center}}
</style></head><body>
<header><b>Chấm hướng dẫn — người {rater}</b>
<span class="prog" id="prog">0/{n}</span>
<button onclick="save()">Lưu tạm</button>
<button class="pri" onclick="exp()">Xuất kết quả</button></header>
<main>
<div class="card" style="grid-template-columns:1fr">
<h3 style="margin:0 0 8px">Bạn cần làm gì</h3>
<p style="margin:0 0 10px">Mỗi thẻ có <b>một ảnh màn hình</b>, <b>mục tiêu</b> của người dùng, và <b>hai câu hướng dẫn</b> cho bước kế tiếp. Nhìn ảnh rồi trả lời cho từng câu: <b>câu này có giúp bạn chạm đúng chỗ trên màn hình này không?</b></p>
<p style="margin:0 0 10px">Chấm theo cảm nhận của người dùng thật, đừng cố đoán câu nào "chuẩn hơn". Hai câu có thể cùng tốt, cùng tệ, hoặc một tốt một tệ. Thứ tự A/B đã xáo trộn, không có câu nào là đáp án mẫu.</p>
<p style="margin:0 0 10px"><b>Thang điểm:</b><br>
<b>0</b> — không biết phải chạm vào đâu.<br>
<b>1</b> — đoán được nhưng mơ hồ, dễ chạm nhầm.<br>
<b>2</b> — chỉ đúng chỗ, nhưng có chỗ lấn cấn (thừa/thiếu chữ, gọi tên hơi sai).<br>
<b>3</b> — rõ ràng, làm theo được ngay.</p>
<p style="margin:0 0 10px"><b>Ô "chỉ vào thứ không có trên màn"</b> — tick khi câu nhắc tới một nút/mục mà bạn <b>không tìm thấy</b> trên ảnh.</p>
<p style="margin:0"><b>Ô "hai bước khác nhau"</b> — tick khi A và B không phải hai cách nói của cùng một việc, mà là <b>hai việc khác nhau</b> (ví dụ một câu bảo chạm vào ô tìm kiếm, câu kia bảo gõ chữ vào ô đó). Cả hai vẫn có thể cùng hợp lý.</p>
<p style="margin:10px 0 0;color:var(--mut);font-size:13px">Bấm vào ảnh để phóng to. Kết quả tự lưu trong trình duyệt; xong thì bấm <b>Xuất kết quả</b> và gửi lại file.</p>
</div>
<div id="app"></div>
</main>
<div id="bar"><span class="prog" id="prog2">0/{n}</span><button class="pri" onclick="exp()">Xuất kết quả</button></div>
<script>
const RATER={rater_js};
const D={data};
"""

TPL_TAIL = """
const KEY='cv_rate_'+RATER;
let R=JSON.parse(localStorage.getItem(KEY)||'{}');
function prog(){const n=Object.values(R).filter(x=>x.a!=null&&x.b!=null).length;
 document.getElementById('prog').textContent=n+'/'+D.length;
 document.getElementById('prog2').textContent=n+'/'+D.length;}
function set(id,slot,v){R[id]=R[id]||{};R[id][slot]=v;save();prog();
 document.getElementById('c_'+id).classList.toggle('done',R[id].a!=null&&R[id].b!=null);}
function flag(id,slot,v){R[id]=R[id]||{};R[id]['f'+slot]=v;save();}
function diff(id,v){R[id]=R[id]||{};R[id].diff=v;save();}
function save(){localStorage.setItem(KEY,JSON.stringify(R));}
function exp(){const blob=new Blob([JSON.stringify({rater:RATER,ratings:R},null,1)],{type:'application/json'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='cv_ratings_'+RATER+'.json';a.click();}
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
function cand(id,slot,txt){
 const r=R[id]||{};let o='';
 for(let v=0;v<=3;v++){o+=`<label><input type="radio" name="${id}_${slot}" value="${v}" ${r[slot]==v?'checked':''}
   onchange="set('${id}','${slot}',${v})">${v}</label>`;}
 return `<div class="cand"><div class="txt"><span class="tag">${slot.toUpperCase()}</span>${esc(txt)}</div>
  <div class="opts">${o}</div>
  <div class="flag"><label><input type="checkbox" ${r['f'+slot]?'checked':''}
   onchange="flag('${id}','${slot}',this.checked)"> chỉ vào thứ không có trên màn</label></div></div>`;}
document.getElementById('app').innerHTML=D.map((d,i)=>`
 <div class="card" id="c_${d.id}">
  <div class="shot"><img src="${d.img}" onclick="this.classList.toggle('zoom')"></div>
  <div><div class="goal">Màn ${i+1}/${D.length} &nbsp;·&nbsp; Mục tiêu người dùng: <b>${esc(d.goal)}</b></div>
   ${cand(d.id,'a',d.a)}${cand(d.id,'b',d.b)}
   <div class="flag" style="border-top:1px solid var(--line);padding-top:10px">
    <label><input type="checkbox" ${(R[d.id]||{}).diff?'checked':''}
     onchange="diff('${d.id}',this.checked)"> Hai câu nói về <b>hai bước khác nhau</b> (không phải cùng một bước viết khác đi)</label>
   </div></div></div>`).join('');
Object.keys(R).forEach(id=>{const e=document.getElementById('c_'+id);
 if(e&&R[id].a!=null&&R[id].b!=null)e.classList.add('done');});
prog();
</script></body></html>"""


def write_html(items, rater, seed):
    rng = random.Random(seed)
    order = items[:]
    rng.shuffle(order)
    data = []
    for it in order:
        # xáo A/B: người chấm không biết câu nào của teacher, câu nào là gold
        swap = rng.random() < 0.5
        data.append({"id": it["id"], "goal": it["goal"], "img": it["img"],
                     "a": it["teacher"] if swap else it["gold"],
                     "b": it["gold"] if swap else it["teacher"],
                     "_a_is": "teacher" if swap else "gold"})
    key = {d["id"]: d.pop("_a_is") for d in data}
    head = TPL_HEAD.format(rater=rater, rater_js=json.dumps(rater), n=len(data),
                           data=json.dumps(data, ensure_ascii=False))
    p = os.path.join(OUT, f"rate_{rater}.html")
    open(p, "w", encoding="utf-8").write(head + TPL_TAIL)
    return p, key


if __name__ == "__main__":
    items, skipped = build()
    print(f"Dựng được {len(items)} màn (bỏ {len(skipped)})")
    for r, why in skipped[:5]:
        print("   bỏ:", r, "—", why)

    keys = {}
    for rater, seed in [("A", 101), ("B", 202)]:
        p, k = write_html(items, rater, seed)
        keys[rater] = k
        print(f"  → {p}  ({os.path.getsize(p)/1e6:.1f} MB)")

    slim = [{kk: v for kk, v in it.items() if kk != "img"} for it in items]
    json.dump({"items": slim, "ab_key": keys},
              open(os.path.join(OUT, "items.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    n_match = sum(1 for i in items if i["metric"]["match"])
    print(f"\nThước hiện tại: {n_match}/{len(items)} = {n_match/len(items):.1%} bước được tính ĐÚNG")
    print("→ harness/cv_study/items.json (đáp án + điểm thước — NGƯỜI CHẤM ĐỪNG MỞ)")
