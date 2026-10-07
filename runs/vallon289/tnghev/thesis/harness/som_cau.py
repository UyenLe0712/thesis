# -*- coding: utf-8 -*-
"""Xuất câu cần chấm cho phép người nghe trắc nghiệm — chạy CPU, vài giây.

    python3 harness/som_cau.py        # ghi harness/dg1_cache/som/cau_<nhánh>.jsonl

Câu lấy từ trường `sent` của CHÍNH tệp thô đã chấm executability, nên mọi thước dùng cùng một câu
(đã cắt <desc>, đã chuẩn hoá như lúc chấm). `action_ok`/`toggle_ok` chép theo để tính bản có điều kiện
đúng loại thao tác. Nhánh sàn "Tap the button." đặt action_ok = toggle_ok = 1 (câu đúng loại thao tác,
chỉ thiếu thông tin phần tử), đúng như nhánh sàn f1 của executability.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "..", "runs")
OUT = os.path.join(HERE, "dg1_cache", "som")
NHANH = {"grpo": "grpo_point/score_grpo_point_seed101_raw.jsonl",
         "min": "score_min_desc_seed101_raw.jsonl",
         "s1_101": "score_s1_seed101_raw.jsonl",
         "s1_202": "score_s1_seed202_raw.jsonl",
         "base": "score_base_raw.jsonl",
         "chuan": "score_ceiling_human_raw.jsonl"}


def main():
    som = [json.loads(l) for l in open(os.path.join(OUT, "som.jsonl"), encoding="utf-8")]
    K = [(str(r["episode_id"]), str(r["step_id"])) for r in som]
    for ten, tep in NHANH.items():
        R = {(str(o["episode_id"]), str(o["step_id"])): o
             for o in map(json.loads, open(os.path.join(RUNS, tep), encoding="utf-8"))}
        assert set(R) == set(K), f"{ten}: quần thể lệch som.jsonl"
        with open(os.path.join(OUT, f"cau_{ten}.jsonl"), "w", encoding="utf-8") as f:
            for k in K:
                o = R[k]
                f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "sent": (o.get("sent") or "").strip(),
                                    "action_ok": int(o.get("action_ok", 0)), "toggle_ok": int(o.get("toggle_ok", 0))},
                                   ensure_ascii=False) + "\n")
        print(f"cau_{ten}.jsonl: {len(K)} câu · rỗng {sum(1 for k in K if not (R[k].get('sent') or '').strip())}")
    with open(os.path.join(OUT, "cau_san.jsonl"), "w", encoding="utf-8") as f:
        for k in K:
            f.write(json.dumps({"episode_id": k[0], "step_id": k[1], "sent": "Tap the button.",
                                "action_ok": 1, "toggle_ok": 1}) + "\n")
    print(f"cau_san.jsonl: {len(K)} câu \"Tap the button.\"")


if __name__ == "__main__":
    main()
