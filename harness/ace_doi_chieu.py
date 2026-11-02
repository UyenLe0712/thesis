"""Đối chiếu độc lập các số chính của report/327 §3.1 (0 GPU, số test): 402 bước ACE đổi câu so với ck500.

Thay cho script cũ đã bị ghi đè. Tính lại: nhóm đổi câu, exec cứu/phá từng nhóm, mức góp CIDEr-D của từng nhóm, tách theo khối ví dụ
có hay không có câu chuẩn. CIDEr-D chấm từng câu bằng grpo_luoi.CiderD (nhân 100 cho cùng thang 430 của report), df lấy từ chính câu chuẩn tập kiểm và tách từ xấp xỉ PTB, nên
có thể lệch nhẹ so với bộ chấm COCO; phần BLEU-4, SPICE, METEOR chưa tính lại ở đây.
Nhóm "cùng lõi" dùng hàm bỏ từ thao tác xấp xỉ, có thể lệch vài bước so với 132/70 của report/327.

  python ace_doi_chieu.py     # ghi runs/ace_ablation/doi_chieu_327.json
"""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grpo_luoi as GL                                    # noqa: E402

KHO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BO = set("click on tap press select the a an of in at to go open button icon tab option top bottom left right corner screen".split())


def L(p):
    return {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(os.path.join(KHO, p), encoding="utf-8"))}


def main():
    R = L("runs/ra304_luat/score_R3_test_raw.jsonl")
    C = L("runs/grpo_spice/score_ck500_test_raw.jsonl")
    E = L("_scripts/304/ra-sft-script/ex_test_k4.jsonl")
    assert len(R) == len(C) == 4463, (len(R), len(C))
    ch = lambda s: re.sub(r"[^\w\s]", "", (s or "").lower()).split()
    gold = {k: (R[k].get("gold_instruction") or C[k].get("gold_instruction") or "") for k in R}
    cd = GL.CiderD(list(gold.values()))
    ex = lambda x, k: int(x[k].get("executable", 0))
    nhom, kq = {}, {}
    for k in R:
        a, b, g = C[k].get("sent"), R[k].get("sent"), gold[k]
        if (a or "").strip() == (b or "").strip():
            continue
        if ch(a) == ch(b):
            t = "chi_khac_hoa_dau"
        elif ch(b) == ch(g):
            t = "sai_thanh_dung"
        elif ch(a) == ch(g):
            t = "dung_thanh_sai"
        else:
            t = "cung_loi" if {w for w in ch(a) if w not in BO} & {w for w in ch(b) if w not in BO} else "khac_loi"
        nhom.setdefault(t, []).append(k)
    tong_d = 0.0
    for t, ks in sorted(nhom.items()):
        d = sum(cd.score(R[k]["sent"] or "", gold[k]) - cd.score(C[k].get("sent") or "", gold[k]) for k in ks) / len(R)
        tong_d += d
        kq[t] = dict(n=len(ks), d_cider=round(100 * d, 2), cuu=sum(ex(R, k) > ex(C, k) for k in ks), pha=sum(ex(R, k) < ex(C, k) for k in ks))
    kq["tong"] = dict(n=sum(map(len, nhom.values())), d_cider=round(100 * tong_d, 2), exec_ace=round(100 * sum(ex(R, k) for k in R) / len(R), 2),
                      exec_ck500=round(100 * sum(ex(C, k) for k in R) / len(R), 2),
                      action_ok_ace=sum(bool(R[k].get("action_ok")) for k in R), action_ok_ck500=sum(bool(C[k].get("action_ok")) for k in R))
    co = {k for k in R if k in E and any(ch(x["sent"]) == ch(gold[k]) for x in E[k]["exemplars"])}
    for ten, tap in (("khoi_co_chuan", co), ("khoi_khong_chuan", set(R) - co)):
        doi = [k for k in tap if (C[k].get("sent") or "").strip() != (R[k].get("sent") or "").strip()]
        kq[ten] = dict(n=len(tap), doi=len(doi), cuu=sum(ex(R, k) > ex(C, k) for k in doi), pha=sum(ex(R, k) < ex(C, k) for k in doi),
                       exec_ck500=round(100 * sum(ex(C, k) for k in tap) / len(tap), 2), exec_ace=round(100 * sum(ex(R, k) for k in tap) / len(tap), 2))
    for k_, v in kq.items():
        print(k_, v)
    d = os.path.join(KHO, "runs", "ace_ablation")
    os.makedirs(d, exist_ok=True)
    json.dump(kq, open(os.path.join(d, "doi_chieu_327.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
