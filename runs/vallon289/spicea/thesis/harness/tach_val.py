# -*- coding: utf-8 -*-
"""Tách tập val ra khỏi dữ liệu DẠY, chia theo EPISODE — 400 bước (vòng thô) + 600 (vòng tinh).

    PYTHONIOENCODING=utf-8 python3 harness/tach_val.py

Thi hành P4 của `report/151` §4. Ba điều bắt buộc, sai một cái là mọi số val vô nghĩa:
 · Đơn vị chia là EPISODE, không phải bước — cùng episode ở hai bên là RÒ RỈ.
 · Phân tầng theo `action_type` (8 tầng, đủ cả 8), ⛔ KHÔNG theo `app`: trường này rỗng ở 55%
   số bước và có 270 giá trị trên 1.432 episode.
 · ⛔⛔ Cấu hình huấn luyện PHẢI trỏ vào `train_tru_val.jsonl` mà script này ghi ra, không phải
   `train.jsonl`. Quên bước đó là train trên chính tập val, không có lỗi nào báo, và chỉ lộ ra
   khi chấm test — tức sau 20-37 giờ A100. Xem P4bis.

⚠️ Chỉ chọn val trong các episode ĐỦ ẢNH (`keo_anh_val.py` đã kéo 8 shard rải đều). Hệ quả phải
   khai khi viết: val ngẫu nhiên TRONG 8 shard ấy, không phải trên toàn tập dạy.
"""
import os, json, random, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "dg1_cache", "train_ac")
SEED = 101                                   # ⛔ ghim cứng, đổi là mất tính tái lập


def loai(r):
    a = r.get("action")
    return (a or {}).get("action_type", "?") if isinstance(a, dict) else "?"


def episode_du_anh(recs):
    """Episode đủ ảnh = MỌI bước của episode đó đều có ảnh đã kéo về."""
    p = os.path.join(ROOT, "khoa_co_anh.json")
    if not os.path.exists(p):
        raise SystemExit("Thiếu khoa_co_anh.json — chạy harness/keo_anh_val.py trước.")
    co = {(int(e), int(s)) for e, s in json.load(open(p))}
    buoc = collections.defaultdict(set)
    for r in recs:
        buoc[int(r["episode_id"])].add(int(r["step_id"]))
    return {str(e) for e, ss in buoc.items() if all((e, s) in co for s in ss)}


def tach_val(recs, n_buoc, seed, loai_tru=frozenset()):
    """Chọn EPISODE nguyên vẹn cho đủ ~n_buoc, khớp phân bố LOẠI THAO TÁC."""
    theo_ep = collections.defaultdict(list)
    for r in recs:
        if str(r["episode_id"]) not in loai_tru:
            theo_ep[str(r["episode_id"])].append(r)
    eps = sorted(theo_ep)                    # sắp xếp trước nên tái lập được
    tong = collections.Counter(loai(r) for r in recs)
    N = sum(tong.values())
    muc_tieu = {k: v / N for k, v in tong.items()}

    rng = random.Random(seed)
    tot_nhat, diem_tot = None, float("inf")
    for _ in range(200):                     # 200 lần bốc, giữ lần cân phân bố nhất
        thu = eps[:]
        rng.shuffle(thu)
        chon, nb = [], 0
        for e in thu:
            if nb >= n_buoc:
                break
            chon.append(e)
            nb += len(theo_ep[e])
        c = collections.Counter(loai(r) for e in chon for r in theo_ep[e])
        m = sum(c.values())
        diem = sum(abs(c.get(k, 0) / m - p) for k, p in muc_tieu.items())
        if diem < diem_tot:
            diem_tot, tot_nhat = diem, chon
    return set(tot_nhat), [r for e in tot_nhat for r in theo_ep[e]]


def ghi(ten, rows):
    with open(os.path.join(ROOT, ten), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  {ten:<22}{len(rows):>6} bước / {len({r['episode_id'] for r in rows}):>5} episode")


if __name__ == "__main__":
    R0 = [json.loads(l) for l in open(os.path.join(ROOT, "train.jsonl"), encoding="utf-8")]
    print(f"train.jsonl: {len(R0)} bước / {len({r['episode_id'] for r in R0})} episode")

    ep_du = episode_du_anh(R0)
    R = [r for r in R0 if str(r["episode_id"]) in ep_du]
    print(f"đủ ảnh:      {len(R)} bước / {len(ep_du)} episode")

    ep400, v400 = tach_val(R, 400, SEED)                     # val vòng THÔ
    ep600, v600 = tach_val(R, 600, SEED, loai_tru=ep400)     # val vòng TINH
    val_ep = ep400 | ep600
    day = [r for r in R0 if str(r["episode_id"]) not in val_ep]   # ⭐ trừ trên TOÀN tập dạy

    # ⛔⛔ BỐN PHÉP KIỂM — hỏng một cái là mọi con số val đều vô nghĩa
    assert not (ep400 & ep600), "RÒ RỈ: hai lát chung episode"
    assert len(v400) + len(v600) + len(day) == len(R0), "MẤT hoặc NHÂN ĐÔI bản ghi"
    kv = {(r["episode_id"], r["step_id"]) for r in v400 + v600}
    assert not (kv & {(r["episode_id"], r["step_id"]) for r in day}), "RÒ RỈ ở mức bước"
    assert len(kv) == len(v400) + len(v600), "TRÙNG bước trong val"

    ghi("val400.jsonl", v400)
    ghi("val600.jsonl", v600)
    ghi("train_tru_val.jsonl", day)          # ⛔⛔ PHẢI train trên tệp NÀY

    P = collections.Counter(loai(r) for r in R0)
    for ten, V in (("val400", v400), ("val600", v600)):
        C = collections.Counter(loai(r) for r in V)
        mx = max(abs(100 * C.get(k, 0) / len(V) - 100 * v / len(R0)) for k, v in P.items())
        print(f"  {ten}: lệch phân bố lớn nhất {mx:.2f} pp",
              "OK" if mx < 3 else "KÉM -> đổi SEED")
