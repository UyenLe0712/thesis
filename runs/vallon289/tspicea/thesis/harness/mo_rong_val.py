# -*- coding: utf-8 -*-
"""Mở rộng val để đủ BƯỚC CHẠM cho việc chọn điểm lưu ở Phase 2.

    PYTHONIOENCODING=utf-8 python3 harness/mo_rong_val.py

Vì sao cần: `tach_val.py` chia theo MỌI bước, nhưng `score_run.py` chỉ chấm bước **chạm**. val400
có 407 bước mà chỉ 262 chạm, val600 có 604 mà 391 chạm. Sai số chuẩn ghép cặp ở 262 bước là
~1,3 pp, nên chọn argmax trên năm điểm lưu là chọn gần như ngẫu nhiên.

⭐ Ràng buộc thiết kế: val mới phải **BAO TRÙM** val cũ. Lượt Phase 1 đang chạy trên `val400.jsonl`
cũ; nếu val mới không chứa nó thì `train_tru_val` mới sẽ chứa những bước mà Phase 1 đã dùng để
chọn α, và hai chặng không còn so được với nhau.

⛔ Chạy xong PHẢI dựng lại nhánh:
       python3 harness/build_branch_data.py --recs-file train_tru_val.jsonl
   nếu không thì cấu hình VIS-SFT vẫn trỏ vào bộ cũ, tức tập dạy còn chứa val mở rộng.
"""
import collections, json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
SEED = 101
CHAM_A, CHAM_B = 400, 600          # số bước CHẠM cần cho vòng thô và vòng tinh


def loai(r):
    a = r.get("action")
    return (a or {}).get("action_type", "?") if isinstance(a, dict) else "?"


def la_cham(r):
    return loai(r) in ("click", "long_press")


def episode_du_anh(recs):
    co = {(int(e), int(s)) for e, s in json.load(open(os.path.join(ROOT, "khoa_co_anh.json")))}
    buoc = collections.defaultdict(set)
    for r in recs:
        buoc[int(r["episode_id"])].add(int(r["step_id"]))
    return {str(e) for e, ss in buoc.items() if all((e, s) in co for s in ss)}


def them_cho_du(theo_ep, da_chon, n_cham, seed, cam=frozenset()):
    """Giữ nguyên `da_chon`, thêm episode cho tới khi đủ n_cham bước chạm."""
    chon = list(da_chon)
    dem = sum(1 for e in chon for r in theo_ep[e] if la_cham(r))
    con = sorted(set(theo_ep) - set(chon) - set(cam))
    random.Random(seed).shuffle(con)
    for e in con:
        if dem >= n_cham:
            break
        c = sum(1 for r in theo_ep[e] if la_cham(r))
        if c:
            chon.append(e)
            dem += c
    return set(chon), dem


def ghi(ten, rows):
    with open(os.path.join(ROOT, ten), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    c = sum(1 for r in rows if la_cham(r))
    print(f"  {ten:<26}{len(rows):>6} bước · {c:>5} chạm · "
          f"{len({r['episode_id'] for r in rows}):>4} episode")


if __name__ == "__main__":
    R0 = [json.loads(l) for l in open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8")]
    ep_du = episode_du_anh(R0)
    theo_ep = collections.defaultdict(list)
    for r in R0:
        if str(r["episode_id"]) in ep_du:
            theo_ep[str(r["episode_id"])].append(r)

    cu = {}
    for t in ("val400.jsonl", "val600.jsonl"):
        cu[t] = {str(r["episode_id"])
                 for r in map(json.loads, open(os.path.join(ROOT, t), encoding="utf-8"))}
    print(f"val cũ: {len(cu['val400.jsonl'])} + {len(cu['val600.jsonl'])} episode — sẽ giữ trọn\n")

    epA, cA = them_cho_du(theo_ep, cu["val400.jsonl"], CHAM_A, SEED, cam=cu["val600.jsonl"])
    epB, cB = them_cho_du(theo_ep, cu["val600.jsonl"], CHAM_B, SEED, cam=epA)
    vA = [r for e in epA for r in theo_ep[e]]
    vB = [r for e in epB for r in theo_ep[e]]
    val_ep = epA | epB
    day = [r for r in R0 if str(r["episode_id"]) not in val_ep]

    # ⛔⛔ NĂM phép kiểm — hỏng một cái là mọi số val vô nghĩa
    assert not (epA & epB), "RÒ RỈ: hai lát chung episode"
    assert cu["val400.jsonl"] <= epA and cu["val600.jsonl"] <= epB, "KHÔNG bao trùm val cũ"
    assert len(vA) + len(vB) + len(day) == len(R0), "MẤT hoặc NHÂN ĐÔI bản ghi"
    kv = {(r["episode_id"], r["step_id"]) for r in vA + vB}
    assert not (kv & {(r["episode_id"], r["step_id"]) for r in day}), "RÒ RỈ ở mức bước"
    assert cA >= CHAM_A and cB >= CHAM_B, f"chưa đủ bước chạm: {cA}/{cB}"

    ghi("val_cham400.jsonl", vA)
    ghi("val_cham600.jsonl", vB)
    ghi("train_tru_val.jsonl", day)          # ⛔ GHI ĐÈ: nay trừ val MỞ RỘNG

    P = collections.Counter(loai(r) for r in R0)
    for ten, V in (("val_cham400", vA), ("val_cham600", vB)):
        C = collections.Counter(loai(r) for r in V)
        mx = max(abs(100 * C.get(k, 0) / len(V) - 100 * v / len(R0)) for k, v in P.items())
        print(f"  {ten}: lệch phân bố lớn nhất {mx:.2f} pp",
              "OK" if mx < 3 else "KÉM -> đổi SEED")
    print(f"\n⛔ Chạy lại: python3 harness/build_branch_data.py --recs-file train_tru_val.jsonl")
