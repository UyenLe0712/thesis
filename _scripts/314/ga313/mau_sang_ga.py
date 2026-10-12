# -*- coding: utf-8 -*-
"""313 - chuyển tệp mẫu của raft_mau.py sang định dạng `--mau-file` của ga_dpo.py (file 295), để dựng cặp DPO
trên ĐÚNG bộ mẫu đã dùng cho RAFT. Có thể đổi gốc đường dẫn ảnh (Kaggle → Colab).

    python mau_sang_ga.py --vao raft_mau_0.jsonl raft_mau_1.jsonl --ra mau_ga.jsonl
    python mau_sang_ga.py --vao cap_all.jsonl --ra cap_colab.jsonl --anh-moi /content/bundle/images  # đổi đường dẫn ảnh
    python mau_sang_ga.py --tu-kiem
"""
import os, json, argparse


def doi(d, anh_moi=None):
    o = dict(d)
    if "samples" in o:
        o["mau"] = o.pop("samples")
        o.setdefault("action_type", "")
    if anh_moi:
        o["image"] = os.path.join(anh_moi, os.path.basename(o["image"]))
    return o


def tu_kiem():
    d = dict[str, str | list[str] | float](key="1000_0", image="/kaggle/input/x/images/ep1_s0.png", body="b", gold="g", greedy="h", samples=["a", "b"], T=0.7)
    o = doi(d)
    assert o["mau"] == ["a", "b"] and "samples" not in o and o["greedy"] == "h" and o["action_type"] == ""
    c = dict[str, str](key="1", image="/kaggle/input/x/images/ep1_s0.png", chosen="a", rejected="b")
    assert doi(c, "/content/b/images")["image"] == "/content/b/images/ep1_s0.png" and doi(c)["chosen"] == "a"
    print("[tự kiểm] ĐẠT")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--vao", nargs="+")
    ap.add_argument("--ra")
    ap.add_argument("--anh-moi", default=None)
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        tu_kiem()
    else:
        n = 0
        with open(a.ra, "w", encoding="utf-8") as f:
            for p in a.vao:
                for l in open(p, encoding="utf-8"):
                    f.write(json.dumps(doi(json.loads(l), a.anh_moi), ensure_ascii=False) + "\n"); n += 1
        print(f"[đổi] {n} dòng → {a.ra}")
