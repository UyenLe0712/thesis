# -*- coding: utf-8 -*-
"""311 — RA-GRPO: chạy ĐÚNG công thức ck500 (grpo_spice.py của lượt 304, không sửa) nhưng câu nhắc có khối 4 câu mẫu.

Khác ck500 đúng một biến: `grpo_spice.body_of` được bọc để chèn khối `ra_exemplars.chen(body, Kho.cho_test(x, 4, ocr, own=tác vụ))`.
Kho = train_tru_val.jsonl bỏ mọi tác vụ của p1_val_rows. Cùng 1.000 câu nhắc, cùng hạt, cùng G/lô/B/lr/500 bước,
cùng S1 hoà làm điểm xuất phát và làm mốc KL (lúc tính KL, mốc cũng thấy khối).
Thêm: dừng êm sau --gio giờ (lưu điểm lưu rồi thoát) để nối commit Kaggle; khối của mỗi câu nhắc ghi đệm ra --out/ra_cache.json.

    python ra_grpo.py --kho train_tru_val.jsonl --gio 10.3 -- --train --bundle B --merged M --out O --resume auto --no-q4?
    (mọi đối số sau "--" chuyển nguyên cho grpo_spice.main; dùng đúng lệnh train của ck500)
    python ra_grpo.py --tu-kiem        # kiểm phần chèn khối trên CPU, không cần GPU
"""
import os, sys, json, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, "/kaggle/working/ra", os.path.join(HERE, "..", "..", "thesis-master", "_scripts", "304", "ra-sft-script"),
          os.path.join(HERE, "..", "..", "_scripts", "304", "ra-sft-script")):
    if os.path.isdir(p):
        sys.path.insert(0, p)
import ra_exemplars as RA


def ocr_toks(o):
    return {w for it in (o or {"items": []})["items"][:24] for w in RA.tok(it.get("text", ""))}


def boc_body(goc, kho, cache, dem):
    def body_of(r, ocr):
        b = goc(r, ocr)
        key = f"{r['episode_id']}_{r['step_id']}"
        if key not in cache:
            x = dict(goal=r["goal"], history=r.get("history") or [])
            cache[key] = kho.cho_test(x, 4, ocr_toks(ocr.get(r["image"])), own=r["episode_id"])
        exs = cache[key]
        dem["n"] += 1
        dem["co_khoi"] += bool(exs)
        return RA.chen(b, exs) if exs else b
    return body_of


def dem_chep(completions, keys, golds, cache):
    """Tỉ lệ câu sinh trùng nguyên văn một câu mẫu của khối, và trong số đó tỉ lệ trùng câu chuẩn."""
    chep = dung = 0
    for c, k, g in zip(completions, keys, golds):
        s = (c[0].get("content") if isinstance(c, list) and c else c) or ""
        t = RA.tok(s)
        if t and any(RA.tok(e["sent"]) == t for e in cache.get(k, [])):
            chep += 1
            dung += t == RA.tok(g)
    return chep, dung, len(completions)


def boc_thuong(goc, cache):
    def r_spice(completions, gold, **kw):
        out = goc(completions, gold, **kw)
        try:
            chep, dung, n = dem_chep(completions, kw.get("key") or [], gold, cache)
            print(f"[chép] {chep}/{n} câu trùng câu mẫu - trong đó trùng câu chuẩn {dung}", flush=True)
        except Exception as e:
            print(f"[chép] không đếm được: {e!r}", flush=True)
        return out
    return r_spice


def tu_kiem():
    from build_branch_data import prompt_body
    KHO = next(p for p in ("/mnt/d/Master/Thesis", "/Users/P836901/Documents/Self-learning/thesis/thesis-master") if os.path.isdir(p))
    recs = [json.loads(l) for l in open(f"{KHO}/harness/dg1_cache/train_ac/train_tru_val.jsonl", encoding="utf-8")]
    kho = RA.Kho(recs)
    goc = lambda r, ocr: prompt_body({"goal": r["goal"], "history": r.get("history") or []}, ocr.get(r["image"]))
    cache, dem = {}, dict(n=0, co_khoi=0)
    f = boc_body(goc, kho, cache, dem)
    r = next(t for t in kho.tr if t.get("history"))
    b = f(r, {})
    assert RA.HEADER in b and b.endswith(RA.LAST) and b.startswith(goc(r, {})[:-len(RA.LAST)]), b
    lay = cache[f"{r['episode_id']}_{r['step_id']}"]
    assert 1 <= len(lay) <= 4, lay
    cua_minh = {(t["target_instruction"].strip(), t["goal"], RA._hlast(t)) for t in kho.eps[r["episode_id"]].values()}
    assert not any((e["sent"], e["goal"], e["prev"]) in cua_minh for e in lay), "⛔ khối lấy bước của chính tác vụ"
    k = f"{r['episode_id']}_{r['step_id']}"
    c3 = [[{"content": lay[0]["sent"]}], [{"content": "something else"}], [{"content": lay[0]["sent"]}]]
    assert dem_chep(c3, [k, k, k], [lay[0]["sent"], "x", "y"], cache) == (2, 1, 3)
    thuong = boc_thuong(lambda c, g, **kw: [0.5] * len(c), cache)
    assert thuong(c3, ["a", "b", "c"], key=[k, k, k]) == [0.5, 0.5, 0.5] and thuong.__name__ == "r_spice"
    print(f"[tự kiểm] ĐẠT - khối chèn đúng chỗ, phần đầu câu nhắc giữ nguyên, {len(lay)} câu mẫu (≤ 4 sau khử trùng), "
          "bỏ chính tác vụ; bộ đếm chép đúng; bọc thưởng giữ nguyên giá trị thưởng")
    print(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kho")
    ap.add_argument("--gio", type=float, default=10.3)
    ap.add_argument("--tu-kiem", action="store_true")
    if "--" in sys.argv:
        i = sys.argv.index("--")
        mine, rest = sys.argv[1:i], sys.argv[i + 1:]
    else:
        mine, rest = sys.argv[1:], []
    a = ap.parse_args(mine)
    if a.tu_kiem:
        return tu_kiem()

    import grpo_spice as GS
    g = argparse.ArgumentParser(add_help=False)
    g.add_argument("--bundle")
    g.add_argument("--out")
    ga, _ = g.parse_known_args(rest)
    va = [json.loads(l) for l in open(os.path.join(ga.bundle, "p1_val_rows.jsonl"), encoding="utf-8")]
    kho = RA.Kho([json.loads(l) for l in open(a.kho, encoding="utf-8")], loai_ep={r["episode_id"] for r in va})
    print(f"[kho] {len(kho.tr)} bước - {len(kho.eid)} tác vụ - bỏ {len({r['episode_id'] for r in va})} tác vụ val", flush=True)
    assert len(kho.tr) > 60000, "⛔ kho quá nhỏ - sai tệp train_tru_val?"

    cache_p = os.path.join(ga.out, "ra_cache.json") if ga.out else None
    cache = json.load(open(cache_p)) if cache_p and os.path.exists(cache_p) else {}
    dem = dict(n=0, co_khoi=0)
    GS.body_of = boc_body(GS.body_of, kho, cache, dem)
    GS.r_spice = boc_thuong(GS.r_spice, cache)

    import transformers, trl
    T0 = time.time()

    class DungGio(transformers.TrainerCallback):
        def on_step_end(self, args, state, control, **kw):
            if (time.time() - T0) / 3600 > a.gio:
                control.should_save = True
                control.should_training_stop = True
                print(f"[dừng giờ] {a.gio} h ở bước {state.global_step} - lưu điểm lưu rồi thoát; chạy lại với --resume auto",
                      flush=True)
            return control

    Goc = trl.GRPOTrainer

    class Trainer(Goc):
        def __init__(self, *x, **k):
            super().__init__(*x, **k)
            self.add_callback(DungGio())
            print(f"[RA] câu nhắc đã dựng {dem['n']} - có khối {dem['co_khoi']} - đệm {len(cache)}", flush=True)
            if cache_p:
                os.makedirs(ga.out, exist_ok=True)
                json.dump(cache, open(cache_p, "w"), ensure_ascii=False)

    trl.GRPOTrainer = Trainer
    sys.argv = [GS.__file__] + rest
    GS.main()


if __name__ == "__main__":
    main()
