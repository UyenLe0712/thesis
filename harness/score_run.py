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
  openai    gpt-4o-mini vision qua API — RẺ nhưng lệch trung vị ~8% cạnh, tức nằm ở
            vùng kết oan 42% theo đường cong đã đo. Chỉ dùng để chạy thử đường ống.

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
            path, torch_dtype=torch.bfloat16, device_map="auto").eval()

    def point(self, img, sentence):
        import re
        from PIL import Image
        msg = [{"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text":
                f"Trong ảnh này, hãy chỉ vào phần tử mà câu sau mô tả. Trả lời DUY NHẤT "
                f"một cặp toạ độ dạng (x, y) trong thang 0-1000.\nCâu: {sentence}"}]}]
        text = self.proc.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        inp = self.proc(text=[text], images=[img], return_tensors="pt").to(self.model.device)
        with self.torch.no_grad():
            g = self.model.generate(**inp, max_new_tokens=32, do_sample=False)
        out = self.proc.decode(g[0][len(inp["input_ids"][0]):], skip_special_tokens=True)
        m = re.findall(r"(\d+(?:\.\d+)?)", out)
        if len(m) < 2:
            return None
        x, y = float(m[0]), float(m[1])
        return (x / 1000 * img.width, y / 1000 * img.height)


class OpenAIGrounder:
    """gpt-4o-mini vision. ✱ TỐN API. Lệch trung vị ~8% cạnh — vùng kết oan 42%."""
    NAME = "openai"

    BASE = "https://api.openai.com/v1"
    MODEL = "gpt-4o-mini"

    def __init__(self):
        from _http import chat
        from _apikey import get_key
        self.chat, self.key = chat, get_key()

    def point(self, img, sentence):
        import base64, io as _io, re
        b = _io.BytesIO(); img.save(b, format="PNG")
        d = base64.b64encode(b.getvalue()).decode()
        r = self.chat(self.BASE, self.MODEL, [{"role": "user", "content": [
            {"type": "text", "text":
                f"Chỉ vào phần tử mà câu sau mô tả. Trả lời DUY NHẤT 'x,y' theo pixel "
                f"của ảnh (rộng {img.width}, cao {img.height}).\nCâu: {sentence}"},
            {"type": "image_url",
             "image_url": {"url": f"data:image/png;base64,{d}"}}]}], self.key, temperature=0)
        m = re.findall(r"(\d+(?:\.\d+)?)", r or "")
        return (float(m[0]), float(m[1])) if len(m) >= 2 else None


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["gate", "score"], required=True)
    ap.add_argument("--grounder", default="uground", choices=["uground", "openai"])
    ap.add_argument("--preds", help="tệp dự đoán (chế độ score)")
    ap.add_argument("--out")
    ap.add_argument("--n", type=int, default=0, help="chỉ chạy N bước (0 = tất cả)")
    a = ap.parse_args()

    from PIL import Image
    recs = [json.loads(l) for l in open(os.path.join(TEST, "test.jsonl"), encoding="utf-8")]
    taps = [r for r in recs if r["action"].get("action_type") in ("click", "long_press")
            and "x" in r["action"]]

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
               "median_err": med, "p75_err": p75, "pass": ok}
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
