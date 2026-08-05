# -*- coding: utf-8 -*-
"""
FREE · offline — gán app cho TOÀN BỘ episode của lát app-unseen (631 ep) rồi tính lại G và MDE.

Vá lỗ report/98 §4: "G trục chính chưa chốt cứng — bộ gán app tự động mới phủ ~41% episode".
Ba nguồn gán, xếp theo độ tin:
  1. action open_app  → app_name do chính dataset ghi (chắc chắn nhất)
  2. goal có mẫu "... the X app" / "open X"                (khá chắc)
  3. goal có tên riêng viết hoa đứng đầu                    (yếu, đánh dấu riêng)
Gộp biến thể hoa/thường và khoảng trắng thừa để không tách một app thành nhiều cụm — đúng lỗi
report/90 đã chỉ ra (`The Washington Post` vs `Washington post`).

Chạy: ~/.venvs/thesis/bin/python harness/ac_app_assign.py
"""
import os, re, json, glob, collections, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.expanduser("~/.cache/huggingface/hub/datasets--wangyuanlei--android_control_test/snapshots")
OUT = os.path.join(HERE, "ac_app_assign_results.json")

GOAL_PATTERNS = [
    re.compile(r"\b(?:in|on|using|open|from|with)\s+(?:the\s+)?([A-Z][\w&'\.\-]*(?:\s+[A-Z][\w&'\.\-]*){0,3})\s+app\b"),
    re.compile(r"\bopen\s+(?:the\s+)?([A-Z][\w&'\.\-]*(?:\s+[A-Z][\w&'\.\-]*){0,3})\b"),
    re.compile(r"^([A-Z][\w&'\.\-]*(?:\s+[A-Z][\w&'\.\-]*){0,2})\s+app\b"),
]
STOP = {"the", "a", "an", "my", "this", "that", "it", "go", "to", "and", "then", "please"}


def norm(name):
    """Chuẩn hoá tên app để không tách một app thành nhiều cụm."""
    s = re.sub(r"^(the)\s+", "", (name or "").strip(), flags=re.I)
    s = re.sub(r"\s+", " ", s).strip(" .,'\"").lower()
    s = re.sub(r"\s+(app|application)$", "", s)
    return s


def app_of(o):
    for a in o.get("actions") or []:
        if a.get("action_type") == "open_app" and a.get("app_name"):
            return norm(a["app_name"]), "open_app"
    goal = o.get("goal") or ""
    for pat in GOAL_PATTERNS:
        m = pat.search(goal)
        if m:
            cand = norm(m.group(1))
            if cand and cand not in STOP and len(cand) > 1:
                return cand, "goal"
    return None, None


def mde(sd, g, alpha_t=3.077):
    """MDE ≈ t·SD/√G. 3.077 = hệ số dùng ở report/85 (hai phía, cỡ cụm nhỏ)."""
    return alpha_t * sd / (g ** 0.5)


def main():
    ids = None
    try:
        from datasets import load_dataset
        ids = set(next(iter(load_dataset("reece124/android_control", split="test", streaming=True)))["app_unseen"])
    except Exception as e:
        print("Không lấy được danh sách app_unseen:", e)
        return

    local = {}
    for p in glob.glob(os.path.join(HF, "*", "test_output_json", "*", "episode_*.json")):
        m = re.search(r"episode_(\d+)\.json", p)
        if m:
            local[int(m.group(1))] = p

    have = [i for i in ids if i in local]
    apps = collections.Counter()
    src = collections.Counter()
    unassigned = 0
    steps_per_app = collections.Counter()
    for eid in have:
        try:
            o = json.load(open(local[eid], encoding="utf-8"))
        except Exception:
            continue
        a, s = app_of(o)
        if a:
            apps[a] += 1
            src[s] += 1
            steps_per_app[a] += len(o.get("actions") or [])
        else:
            unassigned += 1

    n_ep = len(have)
    G = len(apps)
    assigned = sum(apps.values())
    sizes = sorted(apps.values(), reverse=True)
    # G hiệu dụng (Kish): phạt việc vài app chiếm phần lớn episode
    n = sum(sizes)
    g_eff = (n * n) / sum(s * s for s in sizes) if sizes else 0

    print("=" * 72)
    print(f"Lát app-unseen: {len(ids)} episode · có sẵn trong cache local: {n_ep}")
    print(f"Gán được app : {assigned} ({assigned/max(n_ep,1):.1%})   không gán được: {unassigned}")
    print(f"  nguồn gán: open_app={src['open_app']}  goal={src['goal']}")
    print(f"G (app phân biệt) = {G}   ·   G hiệu dụng (Kish) = {g_eff:.1f}")
    print(f"  app lớn nhất: " + ", ".join(f"{a}({c})" for a, c in apps.most_common(6)))
    print(f"  app chỉ có 1 episode: {sum(1 for s in sizes if s == 1)}")
    print("-" * 72)
    # SD lấy từ pilot thật (mde_pilot_results.json): sd_diff = độ lệch của HIỆU giữa hai nhánh
    try:
        pil = json.load(open(os.path.join(HERE, "mde_pilot_results.json"), encoding="utf-8"))
        sd_real = pil.get("sd_diff")
    except Exception:
        sd_real = None
    for sd, tag in ([(sd_real, "sd_diff đo từ pilot")] if sd_real else []) + [(0.25, "giả định"), (0.30, "giả định")]:
        print(f"  MDE với SD={sd:.3f} ({tag}):  G={G} → {mde(sd,G)*100:.1f} pp   |   "
              f"G_eff={g_eff:.0f} → {mde(sd,g_eff)*100:.1f} pp")
    print("=" * 72)

    json.dump({"n_app_unseen": len(ids), "n_local": n_ep, "assigned": assigned,
               "rate": assigned / max(n_ep, 1), "unassigned": unassigned,
               "source": dict(src), "G": G, "G_eff_kish": g_eff,
               "singletons": sum(1 for s in sizes if s == 1),
               "top_apps": apps.most_common(20),
               "sd_diff_pilot": sd_real,
               "mde": {str(sd): {"G": mde(sd, G), "G_eff": mde(sd, g_eff)}
                       for sd in ([sd_real] if sd_real else []) + [0.25, 0.30]}},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Đã lưu", OUT)


if __name__ == "__main__":
    main()
