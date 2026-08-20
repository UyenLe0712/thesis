# -*- coding: utf-8 -*-
"""FREE · 0 GPU — dựng kết quả bản v2 của cả BỐN biến thể từ tệp thô đã có.

## Vì sao ghép được, và vì sao nó hợp lệ

Bản v2 khác v1 ở đúng hai chỗ, **cả hai đều không sinh ra chuỗi nào chưa từng được chấm**:

1. `p3_nopos` thêm **hai cổng chặn** → chỉ *bớt* số bước viết lại, không đổi câu nào. Đã kiểm:
   `v2 \\ v1 = 0` bước, và trên phần giao câu **trùng từng byte**.
2. Đường lui nay `.strip()` → ở bước không viết lại được, câu **khớp khít** tệp trần
   (`preds_ceiling_human.jsonl` đã strip sạch, 0/6.958 có dấu cách cuối).

Nên mỗi bước của v2 lấy được kết quả từ một trong hai lượt đã chấm:

| bước | câu của v2 | lấy từ |
|---|---|---|
| v2 viết lại được | y hệt câu v1 đã chấm | `score_para_<v>_raw.jsonl` |
| v2 không viết lại được | câu chuẩn đã strip | `score_ceiling_human_raw.jsonl` |

Điều kiện: **bộ trỏ tất định** — cùng chuỗi + cùng ảnh ⇒ cùng toạ độ. `tu_kiem()` kiểm lại
trên chính dữ liệu này, và nó **so chuỗi nguyên xi, không `.strip()`** — đúng chỗ bản trước
của script này mắc bẫy: `.strip()` che mất khác biệt một dấu cách, rồi 6 bước lệch toạ độ bị
đọc thành "bộ trỏ không tất định".

⇒ Bốn con số v2 lấy được **không tốn giây GPU nào**, và `p3_nopos` không còn phải *loại 7 câu
sau khi đã thấy kết quả*.

Chạy: python3 harness/phep_a_hieu_chinh.py
Ra:   runs/paraphrase/score_para_<v>_v2{,_raw}.{json,jsonl}
"""
import os, json, math

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "runs"))
P = os.path.join(R, "paraphrase")
BIEN_THE = ["p1_verb", "p2_order", "p3_nopos", "p4_both"]


def nap(p, key=None):
    d = {}
    for l in open(p, encoding="utf-8"):
        o = json.loads(l)
        d[(o["episode_id"], o["step_id"])] = o[key] if key else o
    return d


def mcnemar(K, a, b, key="executable"):
    nb = sum(1 for k in K if a[k][key] == 1 and b[k][key] == 0)
    nc = sum(1 for k in K if a[k][key] == 0 and b[k][key] == 1)
    n = nb + nc
    chi = (abs(nb - nc) - 1) ** 2 / n if n else 0.0
    return nb, nc, n, chi, (math.erfc(math.sqrt(chi / 2)) if n else 1.0)


def tu_kiem(v1_raw, ceil_raw):
    """Sáu phép kiểm phải ĐẠT trước khi ghép. Mọi phép so chuỗi là **so byte**, tuyệt đối
    không `.strip()` — bản đầu của script này dùng `.strip()` trong đúng phép kiểm tất định,
    tức tự tay xoá đúng thứ nó cần phát hiện (thủ phạm là một dấu cách cuối câu), rồi báo
    sai thành "bộ trỏ không tất định".
    """
    lat = [k for k in v1_raw if k in ceil_raw]

    # (5) hai lượt chấm phải thấy CÙNG màn hình: cùng danh sách nút, cùng đích, cùng cỡ ảnh.
    for truong in ["n_buttons", "gold_xy", "wh"]:
        l = [k for k in lat if v1_raw[k][truong] != ceil_raw[k][truong]]
        assert not l, f"DỪNG: {len(l)} bước lệch `{truong}` giữa hai lượt ⇒ khác dữ liệu nền"

    # (6) TẤT ĐỊNH. Mạnh hơn vẻ ngoài: lượt trần chấm đủ 4.463 bước, lượt biến thể chỉ 800 ⇒
    # thứ tự và cách gom lô KHÁC nhau. Cùng chuỗi mà cùng toạ độ ⇒ loại luôn khả năng kết quả
    # phụ thuộc lô hay thứ tự, không chỉ loại khả năng bộ trỏ ngẫu nhiên.
    same = [k for k in lat if v1_raw[k]["sent"] == ceil_raw[k]["sent"]]
    lech = [k for k in same if v1_raw[k]["pred_xy"] != ceil_raw[k]["pred_xy"]]
    assert not lech, (f"DỪNG: {len(lech)}/{len(same)} bước cùng chuỗi (byte) cùng ảnh mà khác "
                      f"toạ độ ⇒ phép ghép mất căn cứ. Phải chấm lại thật.")
    return len(same)


def main():
    # (1) chuỗi gốc: câu của lượt trần phải ĐÚNG BẰNG gold_instruction đã strip, từng byte.
    # Không kiểm chỗ này thì cả phép ghép treo trên một giả định về cách tệp trần được dựng.
    goc = {}
    for l in open(os.path.join(os.path.dirname(__file__),
                               "dg1_cache", "test_ac", "test.jsonl"), encoding="utf-8"):
        o = json.loads(l)
        goc[(o["episode_id"], o["step_id"])] = o["gold_instruction"]
    gold = nap(f"{R}/preds_ceiling_human.jsonl", "pred")
    ceil_raw = nap(f"{R}/score_ceiling_human_raw.jsonl")
    l1 = [k for k in gold if gold[k] != goc[k].strip()]
    l2 = [k for k in ceil_raw if ceil_raw[k]["sent"] != goc[k].strip()]
    assert not l1 and not l2, (f"DỪNG: câu lượt trần không bằng gold.strip() "
                               f"({len(l1)} ở preds, {len(l2)} ở tệp thô)")

    tong = {}
    for v in BIEN_THE:
        v1_raw = nap(f"{P}/score_para_{v}_raw.jsonl")
        v2_pred = nap(f"{P}/preds_para_{v}_v2.jsonl", "pred")
        v1_pred = nap(f"{P}/preds_para_{v}.jsonl", "pred")

        n_giu = tu_kiem(v1_raw, ceil_raw)

        # (3) chuỗi bộ trỏ THẬT SỰ nhận ở lượt v1 phải bằng chuỗi trong tệp preds — nếu khâu
        # chấm có chuẩn hoá gì thêm thì giả định "cùng chuỗi" nói về chuỗi khác.
        l3 = [k for k in v1_raw if v1_raw[k]["sent"] != v1_pred[k]]
        assert not l3, f"{v}: {len(l3)} bước 'sent' trong tệp thô khác tệp preds"

        # (2) mọi bước v2 viết lại: chuỗi phải TRÙNG BYTE chuỗi v1 đã chấm.
        S2 = {k for k in v2_pred if v2_pred[k] != gold[k]}
        la = [k for k in S2 if v1_pred[k] != v2_pred[k]]
        assert not la, f"{v}: {len(la)} bước câu v2 khác v1 ⇒ chưa từng được chấm, phải chấm thật"

        # (4) mọi bước v2 KHÔNG viết lại: chuỗi phải TRÙNG BYTE chuỗi lượt trần.
        lb = [k for k in v1_raw if k in ceil_raw and k not in S2
              and v2_pred[k] != ceil_raw[k]["sent"]]
        assert not lb, f"{v}: {len(lb)} bước đường lui khác câu lượt trần ⇒ phải chấm thật"

        lat = [k for k in v1_raw if k in ceil_raw]
        v2m, tu_v1 = {}, 0
        for k in lat:
            if k in S2:
                v2m[k] = v1_raw[k]; tu_v1 += 1
            else:
                v2m[k] = ceil_raw[k]
        doi = [k for k in lat if k in S2]

        def ty(K, d): return sum(d[k]["executable"] for k in K) / max(len(K), 1) * 100
        b, c, n, chi, p = mcnemar(doi, ceil_raw, v2m)
        bt, ct, nt, chit, pt = mcnemar(lat, ceil_raw, v2m)

        print(f"\n=== {v} (v2) · lát {len(lat)} · viết lại {len(doi)} "
              f"({len(doi)/len(lat):.1%}) · tự kiểm tất định {n_giu} bước ✔ ===")
        print(f"  toàn lát      {ty(lat, ceil_raw):5.1f} → {ty(lat, v2m):5.1f} "
              f"({ty(lat, v2m)-ty(lat, ceil_raw):+.1f})   b={bt} c={ct} p={pt:.3f}")
        print(f"  phần bị đụng  {ty(doi, ceil_raw):5.1f} → {ty(doi, v2m):5.1f} "
              f"({ty(doi, v2m)-ty(doi, ceil_raw):+.1f})   b={b} c={c} χ²={chi:.2f} p={p:.3f}")

        with open(f"{P}/score_para_{v}_v2_raw.jsonl", "w", encoding="utf-8") as f:
            for k in lat:
                o = dict(v2m[k]); o["sent"] = v2_pred[k]
                f.write(json.dumps(o, ensure_ascii=False) + "\n")
        json.dump({"mode": "score", "preds": f"preds_para_{v}_v2.jsonl (ghép từ tệp thô, 0 GPU)",
                   "n": len(lat), "exec_voronoi": ty(lat, v2m) / 100,
                   "n_rewritten": len(doi), "exec_rewritten": ty(doi, v2m) / 100,
                   "ceil_rewritten": ty(doi, ceil_raw) / 100,
                   "mcnemar_b": b, "mcnemar_c": c, "chi2": chi, "p": p},
                  open(f"{P}/score_para_{v}_v2.json", "w"), indent=1, ensure_ascii=False)
        tong[v] = (len(doi), b, c)

    # gộp ba biến thể BẢO TOÀN NGHĨA (p3 bỏ thông tin nên không gộp vào)
    N = sum(tong[v][0] for v in ["p1_verb", "p2_order", "p4_both"])
    B = sum(tong[v][1] for v in ["p1_verb", "p2_order", "p4_both"])
    C = sum(tong[v][2] for v in ["p1_verb", "p2_order", "p4_both"])
    rong = (C - B) / N * 100
    se = math.sqrt(B + C) / N * 100
    print(f"\n=== GỘP ba biến thể bảo toàn nghĩa (p1 + p2 + p4) ===")
    print(f"  {N} bước viết lại · đổi chiều {B+C} = {(B+C)/N:.1%} (xuống {B} · lên {C})")
    print(f"  hiệu ròng {rong:+.2f} pp · SE {se:.2f} ⇒ KTC95 [{rong-1.96*se:+.2f}, {rong+1.96*se:+.2f}]")
    print(f"  quy mô 84% cần ~{int(N*0.84)} bước đổi chiều; thực đo {B+C}")


if __name__ == "__main__":
    main()
