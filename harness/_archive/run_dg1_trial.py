# -*- coding: utf-8 -*-
"""
RUN DG1 TRIAL (design E) — end-to-end trên tập NHỎ, KHÔNG cần GPU.
  ảnh + câu hỏi  --(VLM qua API)-->  tutorial gọi nút theo TÊN
                 --(oracle: View Hierarchy)-->  khớp tên / fallback
                 --(chấm DG1)-->  faithfulness + coverage + grounded-rate

Vì máy hiện tại KHÔNG có GPU NVIDIA, ta chạy bộ SINH qua một endpoint VLM tương thích OpenAI.
Model THAY ĐƯỢC (đúng tinh thần design E) — chỉ cần đổi 3 biến môi trường:

  VLM_BASE_URL  endpoint /chat/completions tương thích OpenAI, ví dụ:
                  - OpenRouter : https://openrouter.ai/api/v1
                  - DashScope  : https://dashscope-intl.aliyuncs.com/compatible-mode/v1
                  - OpenAI     : https://api.openai.com/v1
  VLM_MODEL     tên model, ví dụ:
                  - "qwen/qwen2.5-vl-7b-instruct"  (OpenRouter, RẺ — đúng "Qwen mở" đã chốt)
                  - "qwen-vl-max" / "qwen2.5-vl-7b-instruct" (DashScope)
                  - "gpt-4o" / "gpt-5" / "gemini-2.5-pro" (đối chứng frontier)
  VLM_API_KEY   API key của nhà cung cấp đó.

CÁCH CHẠY (PowerShell):
  $env:VLM_BASE_URL="https://openrouter.ai/api/v1"
  $env:VLM_MODEL="qwen/qwen2.5-vl-7b-instruct"
  $env:VLM_API_KEY="sk-...."
  python harness\run_dg1_trial.py

Cần:  pip install requests
Chi phí tập nhỏ (~3-20 ảnh): vài cent đến ~1-2 USD tuỳ model.
"""
import os, sys, json, base64, glob, re

sys.path.insert(0, os.path.dirname(__file__))
from dg1_scorer import load_screen, match, in_bbox   # tái dùng oracle + matcher đã viết

DATA = os.path.join(os.path.dirname(__file__), "..", "dataset_samples", "mobileviews")

# Câu hỏi use-case TỰ SOẠN cho 3 màn mẫu (MobileViews không kèm câu hỏi -> phải tự viết).
QUESTIONS = {
    "item1_state39":  "Tôi muốn đặt giờ rồi xác nhận thì làm thế nào?",
    "item2_state203": "Tôi muốn điền thông tin rồi gửi biểu mẫu thì bấm vào đâu?",
    "item3_state129": "Tôi muốn tạo một công việc mới và nhập thông tin thì làm sao?",
}

PROMPT = """Bạn là trợ lý viết HƯỚNG DẪN SỬ DỤNG phần mềm cho người dùng, từ ẢNH màn hình.
Yêu cầu của người dùng: "{q}"

Hãy viết hướng dẫn TỪNG BƯỚC, mỗi bước gọi nút/ô THEO ĐÚNG TÊN HIỂN THỊ trên màn hình (không bịa nút không có).
CHỈ trả về JSON đúng định dạng sau, không thêm chữ nào khác:
{{"steps":[{{"verb":"<động từ: Bấm/Chọn/Nhập...>","element":"<tên nút/ô đúng như hiển thị>","note":"<giải thích ngắn>"}}]}}"""

def encode_img(p):
    with open(p, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

def call_vlm(img_path, question):
    import urllib.request          # stdlib — KHONG can pip install gi them
    base = os.environ["VLM_BASE_URL"].rstrip("/")
    payload = {
        "model": os.environ["VLM_MODEL"],
        "temperature": 0,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT.format(q=question)},
                {"type": "image_url", "image_url": {"url": encode_img(img_path)}},
            ],
        }],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        base + "/chat/completions", data=data, method="POST",
        headers={"Authorization": "Bearer " + os.environ.get("VLM_API_KEY", "ollama"),
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:   # CPU cham -> timeout rong
        body = json.loads(resp.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"]

def parse_steps(text):
    m = re.search(r"\{.*\}", text, re.S)          # bắt khối JSON dù model lỡ thêm chữ
    obj = json.loads(m.group(0) if m else text)
    return obj["steps"]

def score_generated(screen, steps):
    elems = screen["elems"]
    actionable = [e for e in elems if e["actionable"]] or elems
    matched, halluc, rows = [], 0, []
    for s in steps:
        name = s.get("element", "")
        e, sc = match(name, elems)
        if e is None:
            halluc += 1
            rows.append((s.get("verb", ""), name, "BIA/FALLBACK (khong khop nut that)"))
        else:
            matched.append(e["label"])
            rows.append((s.get("verb", ""), name, "khop: " + e["label"]))
    n = len(steps) or 1
    return {"rows": rows, "faithfulness": 1 - halluc / n,
            "coverage": len(set(matched)) / len(actionable),
            "grounded_rate": len(matched) / n,
            "n_actionable": len(actionable), "n_matched": len(set(matched))}

def main():
    for v in ("VLM_BASE_URL", "VLM_MODEL"):   # VLM_API_KEY tuy chon (Ollama khong can)
        if not os.environ.get(v):
            print(f"[THIEU] chua dat bien moi truong {v}. Xem huong dan o dau file.")
            return
    vhs = sorted(glob.glob(os.path.join(DATA, "*.viewhierarchy.json")))
    print("=" * 78)
    print(f"DG1 TRIAL  | model = {os.environ['VLM_MODEL']}  | {len(vhs)} man MobileViews")
    print("=" * 78)
    agg = []
    for vh in vhs:
        sc = load_screen(vh)
        q = QUESTIONS.get(sc["name"], "Hãy hướng dẫn tôi dùng màn hình này.")
        img = vh.replace(".viewhierarchy.json", ".jpg")
        print(f"\n### {sc['name']}  | hoi: {q}")
        try:
            steps = parse_steps(call_vlm(img, q))
        except Exception as ex:
            print("   LOI goi/parse model:", repr(ex)[:160]); continue
        r = score_generated(sc, steps)
        for verb, name, res in r["rows"]:
            print(f"     - {verb} '{name}'  ->  {res}")
        print(f"   => faithfulness={r['faithfulness']*100:5.1f}%  "
              f"coverage={r['coverage']*100:5.1f}% ({r['n_matched']}/{r['n_actionable']})  "
              f"grounded={r['grounded_rate']*100:5.1f}%")
        agg.append(r)
    if agg:
        f = sum(a["faithfulness"] for a in agg) / len(agg)
        c = sum(a["coverage"] for a in agg) / len(agg)
        g = sum(a["grounded_rate"] for a in agg) / len(agg)
        print("\n" + "-" * 78)
        print(f"TRUNG BINH {len(agg)} man:  faithfulness={f*100:.1f}%  coverage={c*100:.1f}%  grounded={g*100:.1f}%")
        print("(So sanh voi baseline 'viet tu do' + voi model khac de ra ket luan — xem report/14.)")

if __name__ == "__main__":
    main()
