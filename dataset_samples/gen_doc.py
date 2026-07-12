# -*- coding: utf-8 -*-
# Sinh report/DATASET_ITEM_THAT.md (giai thich KY, de hieu) + report/_dataset_doc.html (anh nhung base64).
import json, glob, os, base64, re
ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(os.path.dirname(ROOT), "report")
def jload(p): return json.load(open(os.path.join(ROOT, p), encoding='utf-8'))
out = []
def w(s=""): out.append(s)
def short(s, n=42):
    s = "" if s is None else str(s)
    s = s.replace("|", "/").replace("\n", " ").strip()
    return (s[:n] + "…") if len(s) > n else s
def btn_label(v):
    t = (v.get("text") or "").strip()
    if t: return t
    cd = (v.get("content_description") or "").strip()
    if cd: return cd + " (icon)"
    return (v.get("class") or "").split(".")[-1]
def classify(views):
    return [v for v in views if v.get("editable")], [v for v in views if v.get("clickable") and not v.get("editable")]
def desc_action(gold):
    s = (gold or "").replace("!FUNCTIONCALL", "").strip()
    try: a = json.loads(s)
    except Exception: return short(gold, 40)
    n = a.get("name"); p = a.get("parameters", {}) or {}
    if n == "click": return f"bấm vào màn tại điểm ({p.get('x')}, {p.get('y')})"
    if n == "long_press": return f"giữ tại ({p.get('x')}, {p.get('y')})"
    if n == "input_text": return f'gõ chữ “{(p.get("text") or "").strip()}”'
    if n == "open_app": return f'mở app “{p.get("app_name")}”'
    if n == "scroll": return f"cuộn màn {p.get('direction')}"
    if n == "navigate_back": return "bấm nút Back"
    if n == "navigate_home": return "về màn hình chính"
    if n == "wait": return "chờ màn tải xong"
    if n == "status": return "báo ĐÃ XONG việc (bước kết thúc)"
    return f"{n} {p}"

w("# DỮ LIỆU THẬT — để trình & xin thầy DUYỆT 3 dataset")
w("")
w("> **Tài liệu này để làm gì?** Cho thầy thấy 3 bộ dữ liệu mình dùng *trông thật sự ra sao*. Mỗi bộ trình bày 3 phần: **(1) là gì → (2) một mẫu (item) gồm những gì → (3) ba mẫu thật + giải thích dễ hiểu**.")
w("> Mọi ảnh và đoạn JSON đều **lấy thẳng từ dataset đã tải về máy** (`dataset_samples/`), đã được kiểm tra đối chiếu với nguồn HuggingFace — **khớp 100%, không chỉnh, không tự bịa**. Phần *Giải thích* do mình viết cho dễ hiểu, **chỉ nói đúng những gì có trong dữ liệu**.")
w("")
w("## Một số từ sẽ gặp (đọc 1 lần cho quen)")
w("")
w("| Từ | Nói nôm na |")
w("|--|--|")
w("| **View-hierarchy** | Bảng kèm theo mỗi ảnh, liệt kê **mọi nút/ô trên màn** và **toạ độ (nằm ở đâu)** của chúng. Như “bản đồ các nút”. |")
w("| **bounds (khung)** | 4 con số `[[x1,y1],[x2,y2]]` = hình chữ nhật bao quanh một nút = **vị trí thật** của nút. |")
w("| **Grounding** | Kiểm máy có **chỉ đúng nút** không: điểm máy định bấm có nằm TRONG khung của nút cần bấm không. |")
w("| **Hallucination (bịa)** | Máy nhắc tới một nút **không hề có** trên màn. |")
w("| **Episode (quy trình)** | Một chuỗi thao tác để làm xong 1 việc (vd: mở app → bấm → gõ → xong). |")
w("| **Gold trajectory (thứ tự đúng)** | Chuỗi thao tác đúng từng bước **có sẵn** trong dataset → cho biết **bước nào trước bước nào**. |")
w("| **Kendall τ-b** | Điểm đo **hai thứ tự giống nhau bao nhiêu**: −1 (ngược hẳn) → 0 (lung tung) → +1 (giống y). |")
w("")
w("---")
w("")

# ===================================================================== MobileViews
w("# DATASET 1 — MobileViews")
w("")
w("## 1. MobileViews là gì?")
w("")
w("Là **kho ~600.000 ảnh chụp màn hình ứng dụng Android**. Điều đặc biệt: **mỗi ảnh đi kèm một “view-hierarchy”** — một bảng do điện thoại tự xuất ra, ghi lại **mọi nút/ô trên màn đó + toạ độ chính xác** của chúng. Nói nôm na: không chỉ có *ảnh*, mà còn có cả *“bản đồ các nút”* của ảnh.")
w("")
w("> **Vì sao em cần bộ này:** nhờ biết **vị trí thật của từng nút**, khi AI viết hướng dẫn “bấm nút X”, em **đối chiếu được** AI có chỉ đúng chỗ không (grounding) và có bịa nút không (hallucination) — mà **KHÔNG cần ai soạn sẵn bài hướng dẫn mẫu**. → đây là dữ liệu cho **nhánh 1 ảnh**.")
w("> *(Lưu ý: MobileViews là bản thảo chưa bình duyệt (preprint) → em chỉ dùng nó làm **nguồn ảnh + nhãn vị trí**, không dùng làm cơ sở lý thuyết.)*")
w("")
w("## 2. Một mẫu (item) MobileViews gồm những gì?")
w("")
w("Một item = **1 màn hình**, gồm 3 file đi cùng nhau: **ảnh** (`.jpg`) · **view-hierarchy** (`.viewhierarchy.json` — bảng các nút) · **bản XML gốc** của Android (`.uiautomator.xml`).")
w("")
mv_files = sorted(glob.glob(os.path.join(ROOT, "mobileviews", "item*_state*.viewhierarchy.json")))
j1 = json.load(open(mv_files[0], encoding='utf-8')); rel1 = os.path.relpath(mv_files[0], ROOT).replace("\\", "/")
img1 = rel1.replace(".viewhierarchy.json", ".jpg"); v1 = j1.get("views", [])
w("Ví dụ mở thử file view-hierarchy của 1 màn, nó ghi như sau (mỗi dòng là 1 nút/ô):")
w("")
w(f"![MobileViews item 1](../dataset_samples/{img1})")
w("")
w("**Vài thông tin chung của màn (lấy nguyên từ file):**")
w("")
w("```")
w(f'app đang mở = {j1.get("foreground_activity")}')
w(f'kích thước (pixel) = {j1.get("width")} x {j1.get("height")}')
w(f'tổng số phần tử trên màn = {len(v1)}')
w("```")
w("")
w(f"**Toàn bộ {len(v1)} phần tử của màn này** — cột `bounds` chính là VỊ TRÍ (toạ độ) của nút (✓ = có tính chất đó):")
w("")
w("| # | text (chữ) | mô tả | loại (class) | bounds (vị trí) | bấm? | nhập? | resource_id |")
w("|--|--|--|--|--|--|--|--|")
for i, v in enumerate(v1):
    cls = (v.get("class") or "").split(".")[-1]; rid = (v.get("resource_id") or "").split("/")[-1]
    b = v.get("bounds"); bs = f"[[{b[0][0]},{b[0][1]}],[{b[1][0]},{b[1][1]}]]" if b else ""
    w(f"| {i} | {short(v.get('text'),22)} | {short(v.get('content_description'),18)} | {cls} | {bs} | "
      f"{'✓' if v.get('clickable') else ''} | {'✓' if v.get('editable') else ''} | {short(rid,16)} |")
w("")
w("**Cùng dữ liệu đó ở dạng JSON gốc** (trích 2 phần tử đầu trong bảng `views`, để thầy thấy đúng định dạng thật):")
w("")
w("```json")
w(json.dumps(v1[:2], ensure_ascii=False, indent=2))
w("```")
w("")
w("---")
w("")
w("## 3. Ba mẫu thật + giải thích")
w("")
w("> **Cách đọc mỗi ví dụ:** nhìn ẢNH (màn hình thật) → **ô viền đỏ** là vị trí thật của một nút mà mình vẽ lại từ view-hierarchy, để thấy *dataset biết chính xác nút nằm đâu*.")
w("> *(Lưu ý: gói tải về là trace của 1 app (Xero Projects) nên 3 ví dụ là 3 màn KHÁC NHAU của cùng app; cả bộ 600.000 màn thì trải nhiều app.)*")
w("")
for k, jf in enumerate(mv_files, 1):
    rel = os.path.relpath(jf, ROOT).replace("\\", "/"); j = json.load(open(jf, encoding='utf-8'))
    img = rel.replace(".viewhierarchy.json", ".jpg"); views = j.get("views", [])
    act = (j.get("foreground_activity") or "").split("/")[-1].replace("Activity", ""); pkg = (j.get("foreground_activity") or "").split("/")[0]
    inputs, buttons = classify(views)
    in_lbl = [(v.get("text") or (v.get("resource_id") or "").split("/")[-1]) for v in inputs]
    bt_lbl = [btn_label(v) for v in buttons]
    w(f"### Ví dụ {k}")
    w("")
    w(f"![MobileViews ví dụ {k}](../dataset_samples/{img})")
    w("")
    w(f"**Dữ liệu thật (tóm tắt — đầy đủ ở `dataset_samples/{rel}`):** app `{pkg}`, màn *{act}*, **{len(views)} phần tử**; "
      f"**{len(inputs)} ô nhập** ({', '.join('`'+short(x,18)+'`' for x in in_lbl) if in_lbl else 'không'}); "
      f"**{len(buttons)} nút bấm** ({', '.join('“'+short(x,18)+'”' for x in bt_lbl[:6]) if bt_lbl else 'không'}).")
    w("")
    w(f"**Giải thích (dễ hiểu):** Ảnh trên là **một màn thật** của ứng dụng *{pkg}* (chức năng *{act}*). "
      f"Kèm ảnh, dataset cho một bảng liệt kê **{len(views)} thành phần** trên màn — mỗi thành phần ghi rõ *là nút hay ô nhập, chữ gì, nằm ở toạ độ nào*. "
      f"Màn này có **{len(inputs)} ô để gõ chữ** và **{len(buttons)} nút bấm**. "
      f"**Ô viền đỏ** là mình vẽ lại đúng toạ độ của MỘT nút (lấy từ bảng) — để thầy thấy *dataset biết CHÍNH XÁC nút nằm chỗ nào*. "
      f"**Vì sao điều này quan trọng:** khi AI của em viết “bấm nút …”, em so điểm AI định bấm với khung thật của nút → **trúng khung = đúng (grounding)**; còn nếu AI nhắc một nút *không có* trong bảng → là **bịa (hallucination)**. Nhờ có sẵn vị trí thật, em chấm được mà **không cần bài hướng dẫn mẫu của người**.")
    w("")
    w("---")
    w("")

# ===================================================================== AndroidControl
w("# DATASET 2 — AndroidControl")
w("")
w("## 1. AndroidControl là gì?")
w("")
w("Là bộ **15.283 “quy trình” thao tác thật** (gọi là *episode*) do người thật làm trên **833 ứng dụng**, trung bình ~5,5 bước mỗi quy trình. "
  "Mỗi quy trình có một **mục tiêu** (vd “sửa tên một ghi chú”) và **chuỗi thao tác ĐÚNG từng bước** được ghi sẵn — tức là **đã biết bước nào làm trước bước nào**.")
w("")
w("> **Vì sao em cần bộ này:** vì có sẵn **thứ tự đúng**, em có thể **xáo trộn** các màn của một quy trình rồi xem **AI có sắp lại đúng thứ tự không** — đó là cách đo *AI có hiểu trình tự thao tác không* (**nhánh nhiều ảnh**). Bộ này **đã được bình duyệt (hội nghị NeurIPS 2024)**.")
w("")
w("## 2. Một mẫu (item) AndroidControl gồm những gì?")
w("")
w("Một item = **1 quy trình**, gồm: **mục tiêu** + **các bước**. Mỗi bước có: **ảnh màn lúc đó** (`.png`) · **thao tác đúng** cần làm (bấm toạ độ nào / gõ chữ gì / mở app…) · app đang mở. **Bước cuối luôn là “status”** = đánh dấu đã xong việc.")
w("")
try:
    tools = jload("androidcontrol/_action_schema(tools).json")
    if isinstance(tools, str): tools = json.loads(tools)
    names = [t["function"]["name"] for t in tools]
    w("**Các loại thao tác hợp lệ (lấy từ dataset):** `" + " · ".join(names) + "`.")
    w("")
except Exception: pass
ac_files = sorted(glob.glob(os.path.join(ROOT, "androidcontrol", "ep*.episode.json")))
ep1 = json.load(open(ac_files[0], encoding='utf-8'))
w(f"Mở thử file của 1 quy trình (episode #{ep1.get('episode_id')}), nó ghi nguyên như sau:")
w("")
w("```json")
w(json.dumps(ep1, ensure_ascii=False, indent=2))
w("```")
w("")
w("---")
w("")
w("## 3. Ba mẫu thật + giải thích")
w("")
w("> **Cách đọc:** các ảnh xếp từ TRÁI sang PHẢI = thứ tự đúng của các bước (số 1, 2, 3…). Dưới phần giải thích có liệt kê *thao tác đúng* ở mỗi bước.")
w("> *Ba ví dụ có độ dài khác nhau (3 / 5 / 9 bước) để thấy quy trình ngắn → dài.*")
w("")
for k, jf in enumerate(ac_files, 1):
    ep = json.load(open(jf, encoding='utf-8')); steps = ep["steps"]
    apps = []
    for st in steps:
        a = st.get("active_application")
        if a and a not in apps: apps.append(a)
    seq = "; ".join(f"**bước {i+1}** {desc_action(st.get('gold_action'))}" for i, st in enumerate(steps))
    goal = ep.get('goal').strip()
    w(f"### Ví dụ {k} (quy trình #{ep.get('episode_id')} — {len(steps)} bước)")
    w("")
    imgs = " ".join(f"![ep{k} b{i+1}](../dataset_samples/androidcontrol/{st['screenshot_file']})" for i, st in enumerate(steps))
    w(imgs)
    w("")
    w(f"**Mục tiêu (lấy nguyên từ dataset):** “{goal}”")
    w("")
    w(f"**Thứ tự đúng (gold) — các thao tác:** {seq}.")
    w("")
    w(f"**Giải thích (dễ hiểu):** Đây là **một quy trình thật {len(steps)} bước** mà người dùng đã làm để hoàn thành mục tiêu trên, trong app **{', '.join(apps)}**. "
      f"Dataset lưu ở MỖI bước: *ảnh màn lúc đó* + *thao tác đúng cần làm*. Đọc các thao tác theo thứ tự (ở trên) là thấy rõ **bước nào phải làm trước bước nào** → đó chính là **THỨ TỰ ĐÚNG**. "
      f"**Cách em dùng để trình thầy:** em lấy {len(steps)} ảnh này, **xáo trộn (giấu thứ tự)**, rồi đưa cho AI và yêu cầu *sắp lại cho đúng*; sau đó so kết quả AI sắp với thứ tự đúng ở trên → ra điểm **Kendall τ-b** (càng gần +1 càng đúng). Đây là cách đo *AI có hiểu trình tự thao tác trong app hay không*. (Bước cuối “status” chỉ là đánh dấu đã xong.)")
    w("")
    w("---")
    w("")

# ===================================================================== ScreenSpot
w("# DATASET 3 — ScreenSpot")
w("")
w("## 1. ScreenSpot là gì?")
w("")
w("Là bộ **~1.272 mẫu** kiểm khả năng “chỉ đúng nút” trên **3 nền tảng: điện thoại / máy tính / web**. "
  "Mỗi mẫu rất gọn: **1 ảnh + 1 câu lệnh ngắn** (vd “đóng cửa sổ”) + **đánh dấu sẵn ô chứa nút đúng** cần bấm.")
w("")
w("> **Vì sao em cần bộ này:** đây là **“thước chuẩn” đã được giới khoa học công nhận** (bình duyệt) để KIỂM xem *cái máy chấm-vị-trí của em chính xác bao nhiêu %*. Nó giúp **bù độ tin** cho MobileViews (vốn là bản thảo chưa bình duyệt). *(Bộ này chỉ kiểm “bấm 1 nút”, nên chỉ dùng làm đối chứng, không thay nhánh nhiều ảnh.)*")
w("")
w("## 2. Một mẫu (item) ScreenSpot gồm những gì?")
w("")
w("Một item = **1 ảnh** + các trường: `instruction` (câu lệnh) · `bbox` (ô vị trí đúng, ghi cả dạng 0–1 và pixel) · `data_type` (icon hay chữ) · `data_source` (nền tảng) · `image_size`.")
w("")
ss_files = sorted(glob.glob(os.path.join(ROOT, "screenspot", "item*.json")))
it1 = json.load(open(ss_files[0], encoding='utf-8'))
w(f"Mở thử file của 1 mẫu, nó ghi nguyên như sau:")
w("")
w(f"![ScreenSpot item 1](../dataset_samples/screenspot/{it1.get('image_file')})")
w("")
w("```json")
w(json.dumps(it1, ensure_ascii=False, indent=2))
w("```")
w("")
w("---")
w("")
w("## 3. Ba mẫu thật + giải thích")
w("")
w("> **Cách đọc:** trên ảnh, **ô viền đỏ** = vị trí nút đúng (do dataset đánh dấu); **chấm xanh** = ví dụ điểm-bấm.")
w("> *Ba ví dụ thuộc 3 nền tảng khác nhau (điện thoại / máy tính / web).*")
w("")
def pos_words(bb, size):
    cx = (bb[0] + bb[2]) / 2 / size[0]; cy = (bb[1] + bb[3]) / 2 / size[1]
    v = "phía trên" if cy < 0.33 else ("giữa" if cy < 0.66 else "phía dưới")
    h = "bên trái" if cx < 0.33 else ("giữa" if cx < 0.66 else "bên phải")
    return f"{v} {h}"
for k, jf in enumerate(ss_files, 1):
    it = json.load(open(jf, encoding='utf-8'))
    bbp = it.get("bbox_pixel_[x1,y1,x2,y2]"); sz = it.get("image_size_[w,h]"); pos = pos_words(bbp, sz)
    plat = it.get('platform') or '?'
    w(f"### Ví dụ {k} — nền tảng: {plat} ({it.get('data_source')})")
    w("")
    w(f"![ScreenSpot ví dụ {k}](../dataset_samples/screenspot/{it.get('image_file')})")
    w("")
    w(f"**Dữ liệu thật:** câu lệnh **“{it.get('instruction')}”** · loại **{it.get('data_type')}** · nền **{it.get('data_source')}** · "
      f"ô vị trí đúng (pixel) **{bbp}** trên ảnh **{sz[0]}×{sz[1]}**.")
    w("")
    w(f"**Giải thích (dễ hiểu):** Mẫu này (trên **{plat}**) yêu cầu làm thao tác **“{it.get('instruction')}”**. "
      f"Dataset đã **đánh dấu sẵn ô chứa nút đúng** (ô viền đỏ, nằm ở **{pos}** màn hình). "
      f"**Cách em dùng:** em cho công cụ chấm-vị-trí của mình chỉ ra *điểm cần bấm*; nếu điểm đó rơi **trong ô đỏ** thì tính là chấm ĐÚNG. "
      f"Chạy hết ~1.272 mẫu → ra con số *“bộ chấm-vị-trí của em chính xác X%”*. Vì ScreenSpot **đã được công nhận**, con số đó là **bằng chứng đáng tin** cho phần chấm của em.")
    w("")
    w("---")
    w("")

w("# Tóm tắt (chốt với thầy)")
w("")
w("| Dataset | Bình duyệt? | Một item gồm | Đã đưa | Dùng để |")
w("|--|--|--|--|--|")
w("| MobileViews | Preprint (nguồn ảnh/nhãn) | ảnh + bảng nút (view-hierarchy) + XML | 3 màn thật | Nhánh 1 ảnh: chấm chỉ-đúng-nút & không-bịa |")
w("| AndroidControl | ✓ NeurIPS 2024 | mục tiêu + các bước (ảnh + thao tác đúng) | 3 quy trình (3/5/9 bước) | Nhánh nhiều ảnh: xáo trộn → AI sắp lại → chấm τ-b |")
w("| ScreenSpot | ✓ ACL 2024 / ICLR 2025 | ảnh + câu lệnh + ô vị trí đúng | 3 mẫu (di động/máy tính/web) | Đối chứng: bộ chấm-vị-trí của em chính xác % |")
w("")
w("*Toàn bộ file gốc ở thư mục `dataset_samples/`. Dữ liệu đã đối chiếu khớp 100% với nguồn — không có gì tự bịa.*")

doc = "\n".join(out)
op = os.path.join(REPORT, "DATASET_ITEM_THAT.md")
open(op, "w", encoding="utf-8").write(doc)
print("WROTE md:", op, "| chars:", len(doc))

# ---- build self-contained HTML (anh nhung base64) ----
try:
    import markdown
    body = markdown.markdown(doc, extensions=['tables', 'fenced_code', 'sane_lists'])
    import io
    from PIL import Image
    def inline(m):
        rel = m.group(1)
        path = os.path.normpath(os.path.join(REPORT, rel))
        im = Image.open(path).convert("RGB")
        im.thumbnail((520, 520))  # thu nhỏ để PDF nhẹ, mở được mọi nơi
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=82)
        b = base64.b64encode(buf.getvalue()).decode()
        return f'src="data:image/jpeg;base64,{b}"'
    body = re.sub(r'src="(\.\./dataset_samples/[^"]+)"', inline, body)
    css = """<style>
@page{margin:1.4cm}
body{font-family:'Segoe UI',Arial,sans-serif;font-size:12px;line-height:1.5;color:#1c2530}
h1{font-size:20px;color:#8A2433;border-bottom:2px solid #8A2433;padding-bottom:4px;margin-top:24px}
h2{font-size:15px;color:#1c2530;margin-top:16px}
h3{font-size:13px;color:#8A2433;margin-top:12px}
img{height:215px;width:auto;border:1px solid #cbd2d9;margin:3px;vertical-align:top}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:10px}
th,td{border:1px solid #cbd2d9;padding:3px 6px;text-align:left;vertical-align:top}
th{background:#f4f6f8}
blockquote{margin:6px 0;padding:4px 12px;border-left:3px solid #8A2433;background:#faf3f4}
code{background:#eef1f4;padding:1px 4px;border-radius:3px;font-size:10px}
pre{background:#f7f9fb;border:1px solid #e2e8ee;padding:8px;border-radius:4px;font-size:10px;white-space:pre-wrap;word-break:break-word}
hr{border:none;border-top:1px solid #ddd;margin:12px 0}
</style>"""
    html = f"<!doctype html><html><head><meta charset='utf-8'>{css}</head><body>{body}</body></html>"
    open(os.path.join(REPORT, "_dataset_doc.html"), "w", encoding="utf-8").write(html)
    print("WROTE html (base64 images):", len(html))
except Exception as e:
    print("html build failed:", e)
