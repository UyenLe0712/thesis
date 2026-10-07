# -*- coding: utf-8 -*-
"""Đối chiếu tập dạy / tập kiểm của dự án với split CHÍNH THỨC của AndroidControl — 0 GPU.

Nguồn split: https://storage.googleapis.com/gresearch/android_control/splits.json (Li et al.,
NeurIPS 2024 D&B), bản tải 28/9/2026 lưu ở runs/split_chinh_thuc/splits.json.
Trả lời ba câu (report/209):
  1. tập dạy (12.895 tác vụ) và tập kiểm (1.432 tác vụ) của dự án rơi vào split chính thức nào;
  2. còn bao nhiêu tác vụ/bước S1 CHƯA thấy (không ở tập dạy, không ở tập kiểm);
  3. exec của các nhánh đã chấm có khác nhau giữa bước thuộc split train chính thức và bước thuộc
     split test/validation chính thức không (dấu hiệu bộ trỏ UGround đã học các màn đó).

    ~/.venvs/thesis/bin/python harness/kiem_split_chinh_thuc.py
Ghi: runs/split_chinh_thuc/ket_qua.json
"""
import collections, glob, json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "runs", "split_chinh_thuc")
NHANH = [("cau chuan", "runs/score_ceiling_human_raw.jsonl"),
         ("S1/101", "runs/score_s1_seed101_raw.jsonl"),
         ("S1/202", "runs/score_s1_seed202_raw.jsonl"),
         ("MIN/101", "runs/score_min_desc_seed101_raw.jsonl"),
         ("Base", "runs/score_base_raw.jsonl")]


def jl(p):
    return [json.loads(x) for x in open(os.path.join(ROOT, p), encoding="utf-8")]


def main():
    sp = json.load(open(os.path.join(OUT, "splits.json")))
    lab = {int(e): k for k, v in sp.items() for e in v}
    harry = glob.glob(os.path.expanduser(
        "~/.cache/huggingface/hub/datasets--HarrytheOrange--parsed_AndroidControl/snapshots/*/"
        "parsed_android_control.jsonl"))[0]
    allep = {}
    for line in open(harry, encoding="utf-8"):
        o = json.loads(line)
        allep[int(o["episode_id"])] = o
    tr = {int(r["episode_id"]) for r in jl("harness/dg1_cache/train_ac/train.jsonl")}
    te_rows = jl("harness/dg1_cache/test_ac/test.jsonl")
    te = {int(r["episode_id"]) for r in te_rows}
    rest = set(allep) - tr - te
    out = {"so_tac_vu": {"harry": len(allep), "day": len(tr), "kiem": len(te), "giao_day_kiem": len(tr & te),
                         "con_lai": len(rest)},
           "split_chinh_thuc": {k: len(v) for k, v in sp.items()},
           "id_split_khong_co_trong_harry": sum(len(set(map(int, v)) - set(allep)) for v in sp.values())}
    print(out)

    bang = {}
    for k, v in sp.items():
        v = set(map(int, v))
        bang[k] = {"trong_tap_day": len(v & tr), "trong_tap_kiem": len(v & te), "con_lai": len(v & rest),
                   "buoc_con_lai": sum(len(allep[e]["step_instructions"]) for e in v & rest)}
        print(k, bang[k])
    out["giao_split"] = bang
    # kỳ vọng nếu tập kiểm của dự án là mẫu NGẪU NHIÊN theo tác vụ, độc lập với split chính thức
    out["ky_vong_neu_ngau_nhien"] = {k: round(len(te) * len(v) / len(allep), 1) for k, v in sp.items()}
    out["buoc_tap_kiem_theo_split"] = dict(collections.Counter(lab[int(r["episode_id"])] for r in te_rows))

    acts = collections.Counter()
    for e in rest:
        for a in allep[e]["actions"]:
            acts[a["action_type"]] += 1
    out["con_lai_theo_thao_tac"] = dict(acts)
    out["con_lai_buoc"] = sum(acts.values())

    exec_ = {}
    for nm, f in NHANH:
        g = collections.defaultdict(lambda: collections.defaultdict(list))
        for r in jl(f):
            e = int(r["episode_id"])
            v = 0 if "bo_qua" in r else int(bool(r.get("executable")))
            g["train" if lab[e] == "train" else "test+val"][e].append(v)
        o = {}
        for k, by in g.items():
            eps = sorted(by)
            n = sum(len(by[e]) for e in eps)
            m = 100 * sum(sum(by[e]) for e in eps) / n
            rng = random.Random(101)
            bs = []
            for _ in range(1000):
                s = c = 0
                for e in (rng.choice(eps) for _ in eps):
                    s += sum(by[e]); c += len(by[e])
                bs.append(100 * s / c)
            bs.sort()
            o[k] = {"n_buoc": n, "n_tac_vu": len(eps), "exec": round(m, 2),
                    "ktc95": [round(bs[25], 2), round(bs[974], 2)]}
        exec_[nm] = o
        print(nm, o)
    out["exec_theo_split"] = exec_
    json.dump(out, open(os.path.join(OUT, "ket_qua.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ghi runs/split_chinh_thuc/ket_qua.json")


if __name__ == "__main__":
    main()
