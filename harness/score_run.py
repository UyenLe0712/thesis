# -*- coding: utf-8 -*-
"""
Chấm một tệp dự đoán, và chạy CỔNG A — mắt xích còn thiếu giữa suy luận và con số.

`metric_exec.py` chỉ là thư viện hàm chấm từng bước. File này lo phần còn lại:
gọi bộ trỏ để lấy điểm trỏ cho từng câu, lấy danh sách nút của từng màn từ cây trợ
năng, chấm bằng metric_exec, rồi gộp thành con số có khoảng tin cậy — gom cụm theo
ứng dụng, tác vụ không gán được app thì mỗi tác vụ một cụm (report/106 mục 6).

HAI CHẾ ĐỘ:

  --mode gate   CỔNG A. Đưa bộ trỏ câu CHUẨN của người viết, đo xem nó trỏ lệch bao
                nhiêu so với điểm chạm thật. Đây là phép đo DỤNG CỤ, không phải đo mô
                hình. Điều kiện dùng thước chính: sai số trung vị ≤ 3% chiều rộng màn.

  --mode score  Chấm câu do một nhánh sinh ra. Headline = Ô-VORONOI TÂM: tính trúng khi
                phần tử gold là phần tử GẦN ĐIỂM TRỎ NHẤT trong số mọi phần tử trên màn
                (hàm hit_voronoi). Đĩa dung sai báo kèm để minh bạch, KHÔNG phải headline
                — đo được: sàn của nó là 84,3%, tức trỏ nhầm sang nút bên cạnh vẫn cho
                qua 84% số ca, gần như không phân biệt được gì (report/106 mục sửa đổi 6/8).

BỘ TRỎ cắm rời qua --grounder, vì cổng A tồn tại chính là để chọn cái nào:
  uground   mô hình chuyên định vị, chạy tại máy (khuyến nghị cho thước chính)
  openai    gpt-4o-mini vision qua API — RẺ nhưng lệch xa, chỉ dùng để chạy thử
            đường ống. ĐO ĐƯỢC 6/8 trên 10 bước tập kiểm: trung vị 29,3% bề ngang
            màn, không bước nào vào nổi 3%. Bốn trong mười lần nó trả đúng giữa
            màn theo TRỤC NGANG (x=500 trong thang 0-1000) ở 6/10 lần, và toạ độ
            bội của 50 ở 10/10 lần — tức là đoán trên lưới thô, không phải trỏ.

            ⚠ Con số "~8% cạnh" của các bản ghi trước là SAI, đã rút. Kết quả pilot
            lưu trên đĩa ghi median_dist = 0,150 — MƯỜI LĂM phần trăm. "8" nhiều
            khả năng chép nhầm từ "trung vị 8 TỪ", chỗ chia đôi câu ngắn/câu dài
            nằm ngay câu bên cạnh trong cùng đoạn.

Chạy:
  python harness/score_run.py --mode gate  --grounder uground --n 300
  python harness/score_run.py --mode score --preds ckpt/preds_s1_seed101.jsonl \
                              --grounder uground --out ckpt/score_s1_seed101.json
"""
import os, sys, json, math, random, argparse, statistics, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import metric_exec as M
import a11y_inventory as A11Y

TEST = os.path.join(HERE, "dg1_cache", "test_ac")
SEED = 20260805                      # khoá ở report/106 mục 10

def pick_dtype():
    """Chọn kiểu số theo card ĐANG CÓ, đừng ép bf16.

    A100 có bf16; T4 (Turing) và P100 (Pascal) — hai card của Colab/Kaggle bản miễn phí —
    thì KHÔNG. Ép bf16 ở đó sẽ lỗi hoặc rơi vào đường giả lập chậm khủng khiếp, rồi ta
    ngồi đổ oan cho bộ trỏ hay cho mô hình. Với suy luận, fp16 không đổi kết luận.

    ⚠ ĐỪNG hỏi `torch.cuda.is_bf16_supported()`. PyTorch đời mới trả True cho cả T4 vì
    mặc định nó tính luôn đường GIẢ LẬP — đo được trên Kaggle ngày 9/8: Tesla T4 báo
    True. Hỏi thẳng đời kiến trúc: bf16 chạy thật từ Ampere (sm_80) trở lên.
    """
    import torch
    if not torch.cuda.is_available():
        return torch.float32
    return torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16


def dtype_kw():
    """transformers 5 đổi tên tham số `torch_dtype` thành `dtype`; bản 4.x chỉ hiểu tên
    cũ. Kaggle ngày 9/8 cài sẵn 5.0.0, máy nhà thì 4.x — cùng một dòng mã phải chạy
    được ở cả hai chỗ, không thì lại sinh ra một khác biệt môi trường vô hình."""
    import transformers
    major = int(transformers.__version__.split(".")[0])
    return {("dtype" if major >= 5 else "torch_dtype"): pick_dtype()}



# ─────────────────────────── bộ trỏ ───────────────────────────
class UGround:
    """Bộ trỏ chuyên. Khác họ với mô hình được chấm, và đã xác minh recipe huấn luyện
    của nó không chứa AndroidControl (report/103) — nếu không thì giám khảo từng học
    chính đề thi."""
    NAME = "uground"

    def __init__(self, path="osunlp/UGround-V1-2B"):
        import torch
        from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
        self.torch = torch
        self.proc = AutoProcessor.from_pretrained(path)
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            path, device_map="auto", **dtype_kw()).eval()

    # Câu nhắc BÊ NGUYÊN VĂN từ thẻ mô hình chính chủ (osunlp/UGround-V1-2B). Đây là
    # câu nhắc mô hình được huấn luyện cùng; tự chế câu khác — nhất là bằng tiếng Việt —
    # sẽ làm nó trỏ tệ đi, rồi cổng A rớt vì lý do sai và ta đổ oan cho bộ trỏ.
    # Đầu ra theo thang [0,1000), quy về pixel bằng x/1000*rộng.
    PROMPT = """
  Your task is to help the user identify the precise coordinates (x, y) of a specific area/element/object on the screen based on a description.

  - Your response should aim to point to the center or a representative point within the described area/element/object as accurately as possible.
  - If the description is unclear or ambiguous, infer the most relevant area or element based on its likely context or purpose.
  - Your answer should be a single string (x, y) corresponding to the point of the interest.

  Description: {desc}

  Answer:"""

    def point(self, img, sentence):
        import re
        from PIL import Image
        msg = [{"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": self.PROMPT.format(desc=sentence)}]}]
        text = self.proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        inp = self.proc(text=[text], images=[img], return_tensors="pt").to(self.model.device)
        with self.torch.no_grad():
            # use_cache=True nói THẲNG, không để mặc định quyết: `generation_config` của
            # UGround-V1-2B đặt use_cache=False, và trên T4 điều đó làm 32 token mất 38,7 s
            # thay vì 4,2 s — chậm 9,3 lần cho một phép biến đổi bảo toàn kết quả. Đã kiểm
            # chứ không suy luận: 50 bước đầu của mẫu cổng A chạy lại với cache bật cho
            # toạ độ TRÙNG TUYỆT ĐỐI 50/50 với vết đã lưu (ckpt/cache_check.jsonl).
            g = self.model.generate(**inp, max_new_tokens=32, do_sample=False,
                                    use_cache=True)
        out = self.proc.decode(g[0][len(inp["input_ids"][0]):], skip_special_tokens=True)
        m = re.findall(r"(\d+(?:\.\d+)?)", out)
        if len(m) < 2:
            return None
        x, y = float(m[0]), float(m[1])
        return (x / 1000 * img.width, y / 1000 * img.height)


class OpenAIGrounder:
    """gpt-4o-mini vision. ✱ TỐN API. Chỉ để chạy thử đường ống, KHÔNG chấm được.

    ⚠ HAI CÔNG THỨC SAI SỐ, ĐỪNG SO THẲNG VỚI NHAU:
      · `ground_pilot.py` tính  hypot((px-gx)/W, (py-gy)/H)  — lệch dọc chia cho
        H=2400 nên nhẹ đi 2,2 lần so với lệch ngang. Đo được trung vị 0,150.
      · cổng A ở dưới tính  dist(p,g)/W  — khoảng cách pixel thật, quy ra phần trăm
        bề ngang. Đây mới là đại lượng mà ngưỡng 3% nói tới, vì ngưỡng đó suy ra từ
        "phần tử khác gần nhất cách 69 px".
    Trên cùng 10 bước, cách sau ra số lớn hơn cách trước 1,63 lần. Nên khi hồ sơ ghi
    một con số phần trăm cho bộ trỏ, phải hỏi ngay: đo bằng công thức nào.

    Câu nhắc, cỡ ảnh và cách đọc toạ độ BÊ NGUYÊN từ `ground_pilot.py` — chính script
    đã đẻ ra cặp số 32%/69%. Đổi bất kỳ chỗ nào trong ba thứ đó là số mới không so
    được với số cũ:
      · xin toạ độ CHUẨN HOÁ 0-1000, không xin pixel thô. Mô hình đọc số lớn kém, mà
        ảnh cao 2400 thì pixel thô toàn số lớn.
      · thu ảnh về bề ngang 512 rồi nén JPEG: đủ để trỏ, rẻ hơn nhiều, và né rate-limit.
    """
    NAME = "openai"

    BASE = "https://api.openai.com/v1"
    MODEL = "gpt-4o-mini"
    MAXW = 512
    PROMPT = ("This is a screenshot of a mobile app. A user is told: \"{instr}\". "
              "Give the location to tap to follow this instruction, as two integers 'x,y' "
              "in a 0-1000 normalized grid (x=0 left, x=1000 right, y=0 top, y=1000 bottom). "
              "Answer with ONLY 'x,y', nothing else.")

    def __init__(self):
        from _http import chat
        from _apikey import get_key
        self.chat, self.key = chat, get_key()
        if self.key == "ollama":
            raise SystemExit("Không thấy khoá API (harness/.openai_key) — không gọi được.")

    def point(self, img, sentence):
        import base64, io as _io, re
        from PIL import Image
        w, h = img.size
        sc = img.resize((self.MAXW, int(h * self.MAXW / w)), Image.LANCZOS) if w > self.MAXW else img
        b = _io.BytesIO(); sc.save(b, "JPEG", quality=85)
        uri = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
        r = self.chat(self.BASE, self.MODEL, [{"role": "user", "content": [
            {"type": "text", "text": self.PROMPT.format(instr=sentence)},
            {"type": "image_url", "image_url": {"url": uri}}]}], self.key, temperature=0)
        m = re.findall(r"-?\d+\.?\d*", r or "")
        if len(m) < 2:
            return None
        # 0-1000 chuẩn hoá → pixel của ảnh GỐC
        return (float(m[0]) / 1000 * w, float(m[1]) / 1000 * h)


def make_grounder(name):
    return {"uground": UGround, "openai": OpenAIGrounder}[name]()


# ─────────────────────────── nút trên màn ───────────────────────────
def buttons_of(rec):
    """Tâm mọi phần tử hiển thị của màn — cần cho cách chấm nút-gần-nhất."""
    rel = f"episode_{rec['episode_id']}_screenshot_{rec['step_id']}.png"
    o = A11Y._load(A11Y.key_for(rel) or "")
    if not o:
        return []
    pts = []
    for w in o:
        if w.get("window_type") == 3:
            continue
        for n in w.get("tree", []):
            if not n.get("is_visible_to_user"):
                continue
            b = n.get("bounds_in_screen") or {}
            x1, y1 = b.get("left", 0), b.get("top", 0)
            x2, y2 = b.get("right", 0), b.get("bottom", 0)
            if x2 - x1 < 8 or y2 - y1 < 8:
                continue
            pts.append(((x1 + x2) / 2, (y1 + y2) / 2))
    return pts


# ─────────────────────────── gộp số ───────────────────────────
def cluster_bootstrap(units, key, val, B=10000, seed=SEED):
    """Khoảng tin cậy 95% gom cụm theo ứng dụng.

    Gom cụm vì các bước cùng một app na ná nhau, đếm như độc lập là tự cho mình nhiều
    bằng chứng hơn thực có. Tác vụ không gán được app: mỗi tác vụ một cụm riêng — giữ
    đúng lời hứa đo trên toàn tập thay vì lặng lẽ bỏ 42% dữ liệu.
    """
    cl = collections.defaultdict(list)
    for u in units:
        cl[key(u)].append(val(u))
    groups = list(cl.values())
    if not groups:
        return 0.0, (0.0, 0.0), 0, 0.0
    point = sum(sum(g) for g in groups) / sum(len(g) for g in groups)
    rnd = random.Random(seed)
    G = len(groups)
    boots = []
    for _ in range(B):
        pick = [groups[rnd.randrange(G)] for _ in range(G)]
        num = sum(sum(g) for g in pick); den = sum(len(g) for g in pick)
        if den:
            boots.append(num / den)
    boots.sort()
    lo = boots[int(.025 * len(boots))]; hi = boots[int(.975 * len(boots))]
    sizes = [len(g) for g in groups]
    g_eff = sum(sizes) ** 2 / sum(s * s for s in sizes)      # hiệu chỉnh Kish
    return point, (lo, hi), G, g_eff


def load_preds(path):
    p = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            p[(r["episode_id"], r["step_id"])] = r.get("pred") or ""
    return p


def noharm(a, recs):
    """Thước phụ BẮT BUỘC — không gây hại trên bước KHÔNG phải bước chạm.

    Bản đăng ký (`report/106` mục 3) yêu cầu: trên các bước cuộn / gõ / mở ứng dụng /
    chờ / quay lại — 41% tập kiểm — nhánh khai báo không được thấp hơn nhánh thường quá
    **3 điểm phần trăm** ở tỉ lệ khớp loại thao tác. Đây là lá chắn cho đòn "dạy mô hình
    tả nút trước khi nói thì nó hỏng ở những bước chẳng có nút nào để tả".

    Cho tới 6/8 **không có dòng mã nào chạy phép kiểm này** — `score_run --mode score`
    lọc sẵn chỉ còn bước chạm. Đúng loại lỗi đã bắt một lần (thiếu hẳn script suy luận
    và script chấm): thước nằm trong hồ sơ, tới lúc cần thì không có số.

    Cách chấm dùng đúng hàm của thước chính: so `canon_action` của câu mô hình với
    `canon_action` của câu chuẩn — hai câu, không phải câu với mã thao tác. Nhờ vậy
    không đẻ ra một định nghĩa "khớp thao tác" thứ hai lệch với định nghĩa đang dùng.
    """
    if not a.preds:
        sys.exit("Chế độ noharm cần --preds")
    non_tap = [r for r in recs
               if r["action"].get("action_type") not in ("click", "long_press")
               or "x" not in r["action"]]
    P = load_preds(a.preds)
    rows = [r for r in non_tap if (r["episode_id"], r["step_id"]) in P]
    if not rows:
        sys.exit("Không có bước không-chạm nào trong tệp dự đoán.")

    def unit(r, P):
        s = P[(r["episode_id"], r["step_id"])]
        g = r["gold_instruction"]
        return {"episode_id": r["episode_id"], "app": r.get("app", ""),
                "action_ok": int(bool(s) and M.canon_action(s) == M.canon_action(g)),
                "toggle_ok": int(bool(s) and not M.toggle_conflict(s, g)),
                "empty": int(not s), "gold_type": r["action"].get("action_type", "?")}

    U = [unit(r, P) for r in rows]
    key = lambda u: u["app"] or f"ep{u['episode_id']}"
    pt, ci, g, geff = cluster_bootstrap(U, key, lambda u: u["action_ok"])
    print("=" * 70)
    print(f"KHÔNG GÂY HẠI — {os.path.basename(a.preds)}  ·  {len(U)} bước KHÔNG chạm")
    print("=" * 70)
    print(f"  khớp loại thao tác : {pt:6.1%}   KTC95 [{ci[0]:.1%}, {ci[1]:.1%}]  "
          f"(G={g}, G hiệu dụng={geff:.0f})")
    print(f"  không đảo nghĩa    : {sum(u['toggle_ok'] for u in U)/len(U):6.1%}")
    print(f"  câu rỗng           : {sum(u['empty'] for u in U):6}")
    by = collections.defaultdict(lambda: [0, 0])
    for u in U:
        by[u["gold_type"]][0] += u["action_ok"]; by[u["gold_type"]][1] += 1
    print("  theo loại thao tác chuẩn:")
    for k, (h, n) in sorted(by.items(), key=lambda t: -t[1][1]):
        print(f"     {k:16}{h/n:7.1%}  (n={n})")

    res = {"mode": "noharm", "preds": a.preds, "n": len(U), "action_match": pt,
           "ci": list(ci), "G": g, "G_eff": geff,
           "by_type": {k: {"rate": h / n, "n": n} for k, (h, n) in by.items()}}

    if a.baseline:
        Q = load_preds(a.baseline)
        both = [r for r in rows if (r["episode_id"], r["step_id"]) in Q]
        D = []
        for r in both:
            u1, u0 = unit(r, P), unit(r, Q)
            D.append({**u1, "d": u1["action_ok"] - u0["action_ok"]})
        dpt, dci, _, _ = cluster_bootstrap(D, key, lambda u: u["d"])
        print("-" * 70)
        print(f"  so với nền {os.path.basename(a.baseline)} trên {len(D)} bước chung:")
        print(f"  hiệu số Δ = {dpt:+.1%}   KTC95 [{dci[0]:+.1%}, {dci[1]:+.1%}]")
        ok = dci[0] >= -0.03
        print("  " + ("ĐẠT — cận dưới không thấp hơn nền quá 3 điểm phần trăm."
                      if ok else
                      "RỚT — cận dưới thấp hơn nền quá 3 điểm phần trăm. Phải khai là\n"
                      "     thành phần gây hại trên bước không chạm, kể cả khi thước chính thắng."))
        res.update({"baseline": a.baseline, "delta": dpt, "delta_ci": list(dci), "pass": ok})

    if a.out:
        json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nĐã lưu {a.out}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["gate", "score", "noharm"], required=True)
    ap.add_argument("--baseline", help="chế độ noharm: tệp dự đoán của nhánh nền (thường S1) "
                                       "để tính hiệu số theo cặp")
    ap.add_argument("--grounder", default="uground", choices=["uground", "openai"])
    ap.add_argument("--preds", help="tệp dự đoán (chế độ score)")
    ap.add_argument("--out")
    ap.add_argument("--n", type=int, default=0, help="chỉ chạy N bước (0 = tất cả)")
    a = ap.parse_args()

    from PIL import Image
    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")]
    taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
            and "x" in r["action"]]

    if a.mode == "noharm":
        sys.exit(0 if noharm(a, recs) else 1)

    if a.mode == "score":
        if not a.preds:
            sys.exit("Chế độ score cần --preds")
        preds = {}
        with open(a.preds, encoding="utf-8") as f:
            for line in f:
                p = json.loads(line)
                preds[(p["episode_id"], p["step_id"])] = p
        taps = [r for r in taps if (r["episode_id"], r["step_id"]) in preds]
    if a.n:
        random.Random(SEED).shuffle(taps)
        taps = taps[:a.n]

    G = make_grounder(a.grounder)
    units, errs, raw = [], [], []
    for i, r in enumerate(taps):
        img = Image.open(os.path.join(TEST, r["image"])).convert("RGB")
        wh = (img.width, img.height)
        gold_xy = (float(r["action"]["x"]), float(r["action"]["y"]))
        sent = (r["gold_instruction"] if a.mode == "gate"
                else preds[(r["episode_id"], r["step_id"])]["pred"])
        if not sent:
            units.append({**r, "exec": 0, "disk": 0})
            raw.append({"episode_id": r["episode_id"], "step_id": r["step_id"],
                        "pred_xy": None, "gold_xy": list(gold_xy), "bo_qua": "câu rỗng"})
            continue
        pt = G.point(img, sent)
        if pt is None:
            units.append({**r, "exec": 0, "disk": 0})
            raw.append({"episode_id": r["episode_id"], "step_id": r["step_id"],
                        "pred_xy": None, "gold_xy": list(gold_xy), "sent": sent,
                        "bo_qua": "bộ trỏ không trả toạ độ"})
            continue

        if a.mode == "gate":
            # sai số DỤNG CỤ: lệch bao nhiêu phần trăm chiều rộng màn
            errs.append(math.dist(pt, gold_xy) / wh[0])
            raw.append({"episode_id": r["episode_id"], "step_id": r["step_id"],
                        "pred_xy": list(pt), "gold_xy": list(gold_xy), "wh": list(wh),
                        "err_frac": math.dist(pt, gold_xy) / wh[0]})
        else:
            btns = buttons_of(r)
            s = M.score_step(sent, r["gold_instruction"], pt, gold_xy, btns, wh)
            units.append({**r, "exec": int(s["executable"]), "disk": int(s["hit_disk"])})
            # GHI THÔ từng bước. Bộ trỏ là khoản đắt nhất trong khâu chấm; không lưu
            # lại thì mỗi lần đổi luật chấm, đổi dung sai hay thêm một lát cắt đều
            # phải gọi lại nó trên 4.463 ảnh cho MỖI nhánh — 12-20 đô cho một việc lẽ
            # ra làm offline trong vài giây.
            raw.append({"episode_id": r["episode_id"], "step_id": r["step_id"],
                        "app": r.get("app", ""), "app_seen_in_train": r.get("app_seen_in_train"),
                        "pred_xy": list(pt), "gold_xy": list(gold_xy), "wh": list(wh),
                        "n_buttons": len(btns), "sent": sent,
                        "gold_instruction": r["gold_instruction"],
                        **{k: int(v) for k, v in s.items()}})
        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(taps)}")

    if a.mode == "gate":
        med = statistics.median(errs) if errs else 1.0
        p75 = statistics.quantiles(errs, n=4)[2] if len(errs) > 3 else med
        print("=" * 70)
        print(f"CỔNG A — bộ trỏ '{a.grounder}' trên {len(errs)} bước của tập kiểm")
        print("=" * 70)
        print(f"  sai số TRUNG VỊ : {med:6.1%} chiều rộng màn")
        print(f"  phân vị 75      : {p75:6.1%}")
        print(f"  ≤3% (đạt cổng)  : {sum(1 for e in errs if e <= .03)/max(len(errs),1):6.1%} số bước")

        # ── bốn dấu hiệu LỖI CÀI ĐẶT (report/106 sửa đổi 6/8 mục i) ──────────────
        # Rớt cổng chỉ được ghi là "bộ trỏ không đạt" SAU KHI bốn dấu hiệu này đã
        # loại trừ. Không in ra thì cam kết đó rỗng, nên in ngay cạnh con số chính.
        n_try = len(raw)
        n_fail = sum(1 for x in raw if x.get("pred_xy") is None)
        pts = [tuple(x["pred_xy"]) for x in raw if x.get("pred_xy")]
        top = collections.Counter(pts).most_common(1)
        # Bội số phải xét trên thang CHUẨN HOÁ 0-1000, không phải pixel: bộ trỏ trả số
        # trong thang đó rồi mới quy về pixel, nên "500,400" tròn trịa biến thành
        # (540, 960) — chẳng chia hết cho 50 nào. Kiểm trên pixel là kiểm nhầm thang,
        # bộ dò sẽ im lặng đúng lúc cần kêu.
        norm = [(round(x["pred_xy"][0] / x["wh"][0] * 1000), round(x["pred_xy"][1] / x["wh"][1] * 1000))
                for x in raw if x.get("pred_xy") and x.get("wh")]
        round50 = sum(1 for p in norm if p[0] % 50 == 0 and p[1] % 50 == 0)
        # Kiểu hỏng thật quan sát được ở gpt-4o-mini không phải "rơi vào tâm màn" mà là
        # "bỏ cuộc theo trục ngang": trả x = đúng giữa rồi đoán y. Đo trên 10 bước thử,
        # 6/10 có x = 540 = 1080/2. Bắt trục ngang nhạy hơn hẳn bắt cả điểm tâm, vì
        # chiều dọc mô hình vẫn đoán lung tung nên điểm không rơi vào tâm.
        midx = sum(1 for p in norm if abs(p[0] - 500) <= 5)
        print("-" * 70)
        print("  DẤU HIỆU LỖI CÀI ĐẶT — kiểm trước khi kết luận rớt cổng:")
        print(f"    không đọc được toạ độ : {n_fail}/{n_try} = {n_fail/max(n_try,1):5.1%}"
              f"   {'⚠ vượt 5%' if n_fail/max(n_try,1) > .05 else 'ổn'}")
        if top:
            (tp, tn) = top[0]
            print(f"    toạ độ lặp nhiều nhất : {tp} xuất hiện {tn}/{len(pts)} = {tn/len(pts):5.1%}"
                  f"   {'⚠ dồn một chỗ' if tn/len(pts) > .10 else 'ổn'}")
        print(f"    toạ độ bội của 50     : {round50}/{len(norm)} = {round50/max(len(norm),1):5.1%}"
              f"   {'⚠ trỏ theo lưới thô' if round50/max(len(norm),1) > .25 else 'ổn'}")
        print(f"    x đúng giữa màn       : {midx}/{len(norm)} = {midx/max(len(norm),1):5.1%}"
              f"   {'⚠ bỏ cuộc theo trục ngang' if midx/max(len(norm),1) > .20 else 'ổn'}")
        print("-" * 70)
        ok = med <= 0.03
        # Bậc dự phòng viết lại 6/8 sau khi đo trần và sàn của cả ba ứng viên.
        # Bậc cũ ("rớt thì đổi sang đĩa dung sai") đã bị BÁC: đĩa có sàn 84,3%, tức
        # trỏ nhầm sang nút bên cạnh vẫn cho qua 84% số ca.
        if ok:
            print("  ĐẠT — dùng Voronoi làm thước chính, chạy tiếp theo kế hoạch.")
        elif med <= 0.05:
            print("  5% ≥ lệch > 3% — VẪN giữ Voronoi (trần 93,3%, sàn 2,8%).\n"
                  "     Bắt buộc in kèm bảng trần ở report/106 và đọc mọi số như CẬN DƯỚI.")
        elif med <= 0.08:
            print("  8% ≥ lệch > 5% — vẫn giữ Voronoi (trần 74,4%, sàn 2,8%, dải 71,6 điểm:\n"
                  "     vẫn tốt hơn mọi ứng viên khác). Đọc như cận dưới, khai kết oan 24,1%.")
        else:
            print("  lệch > 8% — ĐỪNG đổi sang thước yếu hơn (đo được: top-2 sàn 61,4%,\n"
                  "     đĩa dung sai sàn 84,3%). Nâng chấm tay lên 200 câu thành thước\n"
                  "     đồng-chính, và chỉ báo THỨ HẠNG tương đối giữa các nhánh.")
        res = {"mode": "gate", "grounder": a.grounder, "n": len(errs),
               "median_err": med, "p75_err": p75, "pass": ok,
               "bug_signals": {"parse_fail": n_fail / max(n_try, 1),
                               "top_point_share": (top[0][1] / len(pts)) if top and pts else 0.0,
                               "grid50_share": round50 / max(len(norm), 1),
                               "mid_x_share": midx / max(len(norm), 1)}}
    else:
        pt_e, ci_e, g, geff = cluster_bootstrap(
            units, lambda u: u["app"] or f"ep{u['episode_id']}", lambda u: u["exec"])
        pt_d, ci_d, _, _ = cluster_bootstrap(
            units, lambda u: u["app"] or f"ep{u['episode_id']}", lambda u: u["disk"])
        print("=" * 70)
        print(f"CHẤM — {os.path.basename(a.preds)}  ·  {len(units)} bước chạm")
        print("=" * 70)
        print(f"  ô-Voronoi tâm (headline): {pt_e:6.1%}   KTC95 [{ci_e[0]:.1%}, {ci_e[1]:.1%}]")
        print(f"  đĩa dung sai (báo kèm) : {pt_d:6.1%}   KTC95 [{ci_d[0]:.1%}, {ci_d[1]:.1%}]")
        print(f"  cụm: {g} (hiệu dụng {geff:.1f})")
        res = {"mode": "score", "preds": a.preds, "n": len(units),
               "exec_voronoi": pt_e, "ci_voronoi": ci_e,
               "exec_disk": pt_d, "ci_disk": ci_d, "clusters": g, "g_eff": geff}

    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rawp = a.out.rsplit(".", 1)[0] + "_raw.jsonl"
        with open(rawp, "w", encoding="utf-8") as f:
            for x in raw:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
        print(f"\nĐã lưu {a.out}\n         {rawp}  ({len(raw)} bước — đổi luật chấm hay "
              f"thêm lát cắt thì chấm lại từ tệp này, KHÔNG gọi lại bộ trỏ)")


if __name__ == "__main__":
    main()
