# -*- coding: utf-8 -*-
"""
Tao trang web TRACK B (cham so-doi BASE vs design-E, AN DANH) tu cac run gpt-4o-mini.
Nguoi cham: nhin anh + 2 tutorial -> chon "A tot hon / B tot hon / hoa". Tai ket qua JSON cuoi cung.
Chay: python harness/trackB_html.py  -> mo harness/trackB.html bang trinh duyet.
"""
import os, json, glob, base64, io, random
from PIL import Image

HERE = os.path.dirname(__file__)
RUNS = os.path.join(HERE, "dg1_cache", "runs")
FOLDER = os.path.join(HERE, "..", "dataset_samples", "mv_dg1")
OUT = os.path.join(HERE, "trackB.html")
N = int(os.environ.get("TRACKB_N", "40"))
MODELTAG = os.environ.get("TRACKB_MODEL", "gpt-4o-mini").replace(":", "_")

def render(steps):
    lis = []
    for s in steps:
        el = s.get("element", ""); v = s.get("verb", ""); note = s.get("note", "")
        extra = f' <span style="color:#888">— {note}</span>' if note else ""
        lis.append(f"<li>{v} <b>{el}</b>{extra}</li>")
    return "<ol>" + "".join(lis) + "</ol>"

def img_b64(path, w=440):
    im = Image.open(path).convert("RGB")
    im = im.resize((w, int(im.height * w / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def main():
    files = sorted(f for f in glob.glob(os.path.join(RUNS, "*.json")) if MODELTAG in os.path.basename(f))
    files = files[:N]
    if not files:
        print(f"Chua co run model {MODELTAG}. Chay dg1_run.py truoc."); return
    cards = []; mapping = {}
    rnd = random.Random(42)   # deterministic an-danh
    for idx, fp in enumerate(files):
        r = json.load(open(fp, encoding="utf-8"))
        name = r["screen"]
        img = os.path.join(FOLDER, name + ".jpg")
        if not os.path.exists(img): continue
        base_html = render(r["base"]); sysE_html = render(r["sysE"])
        # an danh: random A=base hay A=sysE
        if rnd.random() < 0.5:
            A, B, mapping[name] = base_html, sysE_html, "A=BASE"
        else:
            A, B, mapping[name] = sysE_html, base_html, "A=designE"
        cards.append(f'''
        <div class="card" data-screen="{name}">
          <div class="q">#{idx+1} · {name} — <i>{r["question"]}</i></div>
          <div class="row">
            <img src="{img_b64(img)}">
            <div class="opts">
              <div class="opt"><h4>Lựa chọn A</h4>{A}</div>
              <div class="opt"><h4>Lựa chọn B</h4>{B}</div>
              <div class="choose">
                Hướng dẫn nào TỐT HƠN (đúng nút, dễ làm theo)?
                <label><input type="radio" name="{name}" value="A"> A tốt hơn</label>
                <label><input type="radio" name="{name}" value="B"> B tốt hơn</label>
                <label><input type="radio" name="{name}" value="tie"> Ngang nhau</label>
              </div>
            </div>
          </div>
        </div>''')
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Track B — chấm so-đôi</title>
    <style>
      body{{font-family:system-ui,Arial;max-width:980px;margin:20px auto;padding:0 16px;color:#222}}
      .card{{border:1px solid #ddd;border-radius:10px;padding:14px;margin:18px 0;box-shadow:0 1px 4px #0001}}
      .q{{font-size:15px;margin-bottom:10px}}
      .row{{display:flex;gap:16px}}
      .row img{{width:300px;height:auto;border:1px solid #ccc;border-radius:6px;align-self:flex-start}}
      .opts{{flex:1}}
      .opt{{background:#f7f7f9;border-radius:8px;padding:8px 12px;margin-bottom:8px}}
      .opt h4{{margin:4px 0;color:#3556a3}}
      .choose{{margin-top:8px;font-weight:600}}
      .choose label{{font-weight:400;margin-right:14px}}
      #bar{{position:sticky;top:0;background:#fff;padding:10px 0;border-bottom:1px solid #eee;z-index:9}}
      button{{background:#2f6;border:0;padding:10px 18px;border-radius:8px;font-size:15px;cursor:pointer}}
      #cnt{{margin-left:12px;color:#555}}
    </style></head><body>
    <div id="bar"><b>TRACK B — chấm so-đôi (BASE vs design-E, ẩn danh)</b><br>
      Với mỗi màn, chọn hướng dẫn nào TỐT HƠN. Xong bấm <b>Tải kết quả</b> gửi lại.
      <button onclick="save()">⬇ Tải kết quả JSON</button><span id="cnt"></span>
    </div>
    {''.join(cards)}
    <script>
      const MAP = {json.dumps(mapping, ensure_ascii=False)};
      function upd(){{const t=document.querySelectorAll('.card').length;
        const d=[...document.querySelectorAll('.card')].filter(c=>c.querySelector('input:checked')).length;
        document.getElementById('cnt').textContent=` đã chấm ${{d}}/${{t}}`;}}
      document.addEventListener('change',upd); upd();
      function save(){{
        const res={{}};
        document.querySelectorAll('.card').forEach(c=>{{
          const s=c.dataset.screen; const x=c.querySelector('input:checked');
          res[s]={{choice:x?x.value:null, mapping:MAP[s]}};
        }});
        const blob=new Blob([JSON.stringify(res,null,2)],{{type:'application/json'}});
        const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
        a.download='trackB_results.json'; a.click();
      }}
    </script></body></html>'''
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"Da tao {OUT} ({len(cards)} man). Mo bang trinh duyet de cham.")

if __name__ == "__main__":
    main()
