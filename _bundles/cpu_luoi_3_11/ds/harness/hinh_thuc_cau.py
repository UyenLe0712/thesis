"""Đo hình thức câu sinh, không train (report/329 đợt 1): trả lời nhận xét của Liu 2017 về thưởng SPICE thuần.

Mặt chữ: số từ, lặp 2-gram, lặp 3-gram, kết thúc treo (hư từ cuối câu, danh sách do dự án chọn), câu > 20 từ, câu ≤ 2 từ, câu thiếu.
Ngữ pháp (cần spaCy en_core_web_sm): ROOT không phải động từ; câu thiếu động từ; câu có nhiều gốc rời (bộ phân tích tách thành ≥ 2 câu).
Đây là chỉ báo từ bộ phân tích cú pháp, KHÔNG phải điểm ngữ pháp đã kiểm định, và câu chuẩn cũng có lỗi nên luôn đọc kèm hàng câu chuẩn.
So từng nhánh với mốc theo cặp bước (bootstrap theo app như các phép so khác của dự án).

  python hinh_thuc_cau.py --out runs/hinh_thuc_cau/ket_qua.json
  python hinh_thuc_cau.py --them ten=duong/dan_raw.jsonl    # thêm nhánh của lưới
"""
import os, re, json, argparse, random

KHO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NHANH = {"câu chuẩn": None, "S1/101": "runs/score_s1_seed101_raw.jsonl", "ck500": "runs/grpo_spice/score_ck500_test_raw.jsonl",
         "ck500/202": "runs/grpo_spice/s202_24_10/score_ck500_s202_test_raw.jsonl", "xao101": "runs/xao101/test/score_ck500_xao101_test_raw.jsonl",
         "A2_500": "runs/a2_test299/score_A2_500_test_raw.jsonl", "ACE": "runs/ra304_luat/score_R3_test_raw.jsonl"}
TREO = set("the a an of on in at to and or with for by from his her my your this that is are then".split())
TIEU = ("n_tu", "lap2", "lap3", "treo", "dai", "ngan", "thieu", "root_khong_dong_tu", "khong_dong_tu", "nhieu_cau")


def mat_chu(s):
    w = re.findall(r"[a-z0-9']+", (s or "").lower())
    ng = lambda n: [tuple(w[i:i + n]) for i in range(len(w) - n + 1)]
    return dict(n_tu=len(w), lap2=int(len(ng(2)) != len(set(ng(2)))), lap3=int(len(ng(3)) != len(set(ng(3)))),
                treo=int(bool(w) and w[-1] in TREO), dai=int(len(w) > 20), ngan=int(len(w) <= 2), thieu=int(not w))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(KHO, "runs", "hinh_thuc_cau", "ket_qua.json"))
    ap.add_argument("--them", action="append", default=[])
    ap.add_argument("--moc", default="S1/101")
    ap.add_argument("--B", type=int, default=1000)
    a = ap.parse_args()
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    nhanh = dict(NHANH)
    nhanh.update(x.split("=", 1) for x in a.them)
    goc = {}
    for ten, p in nhanh.items():
        if p:
            goc[ten] = {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(os.path.join(KHO, p)))}
    khoa = sorted(goc[a.moc])
    app = {k: goc[a.moc][k].get("app") or f"?{k[0]}" for k in khoa}
    S = {ten: {k: ((goc["ck500"][k].get("gold_instruction") or goc[a.moc][k].get("gold_instruction") if p is None else goc[ten].get(k, {}).get("sent")) or "") for k in khoa}
         for ten, p in nhanh.items()}
    cache = {}
    cau = sorted({s for d in S.values() for s in d.values()})
    print(f"[dữ liệu] {len(khoa)} bước · {len(cau)} câu khác nhau", flush=True)
    for s, doc in zip(cau, nlp.pipe(cau, batch_size=256)):
        d = mat_chu(s)
        goc_cau = [t for t in doc if t.dep_ == "ROOT"]
        d.update(root_khong_dong_tu=int(bool(goc_cau) and goc_cau[0].pos_ not in ("VERB", "AUX")),
                 khong_dong_tu=int(bool(s.strip()) and not any(t.pos_ in ("VERB", "AUX") for t in doc)),
                 nhieu_cau=int(len(goc_cau) > 1))
        cache[s] = d
    T = {ten: {k: cache[d[k]] for k in khoa} for ten, d in S.items()}
    kq = {"n": len(khoa), "ghi_chu": "chỉ báo từ bộ phân tích cú pháp, chưa kiểm định; bootstrap theo app", "nhanh": {}}
    for ten in nhanh:
        kq["nhanh"][ten] = {m: round((1 if m == "n_tu" else 100) * sum(T[ten][k][m] for k in khoa) / len(khoa), 3) for m in TIEU}
        print(ten, kq["nhanh"][ten], flush=True)
    theo_app = {}
    for k in khoa:
        theo_app.setdefault(app[k], []).append(k)
    apps = sorted(theo_app)
    rd = random.Random(20261102)
    kq["so_moc"] = {}
    for ten in nhanh:
        if ten in (a.moc,):
            continue
        tong = {m: {ap_: sum(T[ten][k][m] - T[a.moc][k][m] for k in ks) for ap_, ks in theo_app.items()} for m in TIEU}
        n_a = {ap_: len(ks) for ap_, ks in theo_app.items()}
        kq["so_moc"][ten] = {}
        mau = [[rd.choice(apps) for _ in apps] for _ in range(a.B)]
        for m in TIEU:
            bs = sorted((1 if m == "n_tu" else 100) * sum(tong[m][x] for x in c) / sum(n_a[x] for x in c) for c in mau)
            kq["so_moc"][ten][m] = [round((1 if m == "n_tu" else 100) * sum(tong[m].values()) / len(khoa), 3),
                                    round(bs[int(.025 * a.B)], 3), round(bs[int(.975 * a.B)], 3)]
        print(f"{ten} − {a.moc}", kq["so_moc"][ten], flush=True)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(kq, open(a.out, "w"), ensure_ascii=False, indent=1)
    print("→", a.out)


if __name__ == "__main__":
    main()
