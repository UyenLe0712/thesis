# -*- coding: utf-8 -*-
"""SA-SPICE-v3 PREFLIGHT, bước 2a: lineage của pool (report/SA_SPICE_v3_extracted_verified.md §4.1).

Quét MỌI tệp .json/.jsonl/.jsonl.gz dưới runs/, _bundles/, _scripts/ và rút mọi khoá (episode_id, step_id)
theo ba dạng: dict có `episode_id` (+`step_id`), chuỗi "EP_STEP", đường dẫn ảnh "epEP_sSTEP". Mỗi artifact
được xếp vào một trong hai loại:

  · TẬP CON  : chạm < NGUONG_PHU (mặc định 50%) số episode của pool ⇒ mọi episode nó chạm bị LOẠI khỏi pool.
               Đây là prompt_keys, tập thưởng RL, cặp ưu tiên, ứng viên chấm, lát thử, cache phần thưởng…
  · PHỦ POOL : chạm ≥ NGUONG_PHU ⇒ bản sao dữ liệu dạy / chỉ mục truy hồi toàn tập. Không loại được (S1 đã
               dạy trên toàn bộ), chỉ liệt kê để khai trong claim (§4.3 "S1-seen").

Không gọi GPU, không đọc ảnh. Không đổi tệp nào ngoài --out.

  python3 harness/sa3_lineage.py --out runs/sa_spice_v3/preflight/lineage.json
"""
import os, re, sys, json, gzip, glob, hashlib, argparse, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TA = os.path.join(ROOT, "harness", "dg1_cache", "train_ac")
TE = os.path.join(ROOT, "harness", "dg1_cache", "test_ac")
RE_KEY = re.compile(r"^(\d{1,6})_(\d{1,3})$")
RE_IMG = re.compile(r"ep(\d{1,6})_s(\d{1,3})\b")
NGUONG_PHU = 0.50


def sha256(p, n=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(n), b""):
            h.update(b)
    return h.hexdigest()


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def walk(o, out, depth=0):
    if depth > 8:
        return
    if isinstance(o, dict):
        if "episode_id" in o:
            try:
                out.add((int(o["episode_id"]), int(o["step_id"]) if "step_id" in o else -1))
            except (TypeError, ValueError):
                pass
        for k, v in o.items():
            if isinstance(k, str):
                walk(k, out, depth + 1)
            walk(v, out, depth + 1)
    elif isinstance(o, list):
        for v in o:
            walk(v, out, depth + 1)
    elif isinstance(o, str) and len(o) < 400:
        m = RE_KEY.match(o)
        if m:
            out.add((int(m.group(1)), int(m.group(2))))
        for m in RE_IMG.finditer(o):
            out.add((int(m.group(1)), int(m.group(2))))


def keys_of(path):
    out = set()
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8", errors="replace") as f:
        if path.endswith(".json"):
            try:
                walk(json.load(f), out)
            except Exception:
                return None
        else:
            for l in f:
                l = l.strip()
                if not l:
                    continue
                try:
                    walk(json.loads(l), out)
                except Exception:
                    continue
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-mb", type=float, default=600)
    a = ap.parse_args()

    pool_recs = load_jsonl(os.path.join(TA, "train_tru_val.jsonl"))
    pool_ep = {int(r["episode_id"]) for r in pool_recs}
    keys = [(int(r["episode_id"]), int(r["step_id"])) for r in pool_recs]
    assert len(keys) == len(set(keys)), "⛔ STOP: khoá (episode_id, step_id) trùng trong pool"

    # tầng 1: tập val/C1 và tập kiểm phải tách episode khỏi pool (kiểm, không phải loại)
    tach = {}
    for name in ("val400.jsonl", "val600.jsonl", "val_cham400.jsonl", "val_cham600.jsonl"):
        ep = {int(r["episode_id"]) for r in load_jsonl(os.path.join(TA, name))}
        tach[name] = {"episodes": len(ep), "giao_pool": len(ep & pool_ep)}
    te = os.path.join(TE, "test.jsonl")
    if os.path.exists(te):
        ep = {int(r["episode_id"]) for r in load_jsonl(te)}
        tach["test_ac/test.jsonl"] = {"episodes": len(ep), "giao_pool": len(ep & pool_ep)}
    for k, v in tach.items():
        assert v["giao_pool"] == 0, f"⛔ STOP: {k} chung episode với pool"
    print("[tách]", json.dumps(tach, ensure_ascii=False), flush=True)

    files = []
    for d in ("runs", "_bundles", "_scripts"):
        for pat in ("**/*.json", "**/*.jsonl", "**/*.jsonl.gz"):
            files += glob.glob(os.path.join(ROOT, d, pat), recursive=True)
    files = sorted(set(f for f in files if "__pycache__" not in f and "/.git/" not in f))
    print(f"[quét] {len(files)} tệp", flush=True)

    tap_con, phu_pool, bo_qua = [], [], []
    loai_ep = collections.defaultdict(list)
    for i, f in enumerate(files):
        rel = os.path.relpath(f, ROOT)
        mb = os.path.getsize(f) / 2 ** 20
        if mb > a.max_mb:
            bo_qua.append({"file": rel, "ly_do": f"> {a.max_mb} MB"})
            continue
        ks = keys_of(f)
        if ks is None:
            bo_qua.append({"file": rel, "ly_do": "json hỏng"})
            continue
        ep = {e for e, _ in ks} & pool_ep
        if i % 300 == 0:
            print(f"  … {i}/{len(files)}", flush=True)
        if not ep:
            continue
        rec = {"file": rel, "pool_episodes": len(ep), "frac": round(len(ep) / len(pool_ep), 4)}
        if len(ep) >= NGUONG_PHU * len(pool_ep):
            phu_pool.append(rec)
        else:
            tap_con.append(rec)
            for e in ep:
                loai_ep[e].append(rel)

    # nguồn tường minh ngoài ba thư mục quét
    p1 = os.path.join(TA, "p1_sample_keys.json")
    if os.path.exists(p1):
        # khoá dạng cặp [ep, step]; chỉ đọc dạng này ở tệp này (ở tệp khác [x, y] là toạ độ)
        ep = {int(e) for e, _ in json.load(open(p1))["sample_keys"]} & pool_ep
        tap_con.append({"file": os.path.relpath(p1, ROOT), "pool_episodes": len(ep),
                        "frac": round(len(ep) / len(pool_ep), 4), "ghi_chu": "pool 4.000 câu nhắc gốc của bundle grpo_spice/ck500"})
        for e in ep:
            loai_ep[e].append(os.path.relpath(p1, ROOT))
    try:
        sys.path.insert(0, os.path.join(ROOT, "harness"))
        import grpo_point as GP
        rows, _ = GP.dung_hang()
        ep = {int(r["key"].split("_")[0]) for r in rows} & pool_ep
        tap_con.append({"file": "TAI_DUNG:harness/grpo_point.py dung_hang(seed=101,n=2000)", "pool_episodes": len(ep),
                        "frac": round(len(ep) / len(pool_ep), 4), "n_keys": len(rows)})
        for e in ep:
            loai_ep[e].append("grpo_point")
    except Exception as ex:
        print(f"⛔ STOP: không tái dựng được câu nhắc GRPO-point: {ex!r}", flush=True)
        raise

    excl = set(loai_ep)
    con = [r for r in pool_recs if int(r["episode_id"]) not in excl]
    act = collections.Counter(r["action"]["action_type"] for r in con)
    rep = {
        "spec": "report/SA_SPICE_v3_extracted_verified.md §4.1",
        "pool_goc": {"file": "harness/dg1_cache/train_ac/train_tru_val.jsonl",
                     "sha256": sha256(os.path.join(TA, "train_tru_val.jsonl")),
                     "steps": len(pool_recs), "episodes": len(pool_ep)},
        "tach_episode": tach,
        "nguong_phu_pool": NGUONG_PHU,
        "artifact_tap_con": sorted(tap_con, key=lambda r: -r["pool_episodes"]),
        "artifact_phu_pool": phu_pool,
        "bo_qua": bo_qua,
        "episodes_loai": len(excl),
        "con_lai": {"steps": len(con), "episodes": len({r['episode_id'] for r in con}),
                    "action_steps": dict(act.most_common())},
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(rep, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(sorted(excl), open(os.path.join(os.path.dirname(a.out), "excl_episodes.json"), "w"))
    print(f"[xong] tập con {len(tap_con)} · phủ pool {len(phu_pool)} · bỏ qua {len(bo_qua)} · "
          f"loại {len(excl)} episode · còn {rep['con_lai']['steps']} bước / {rep['con_lai']['episodes']} episode", flush=True)


if __name__ == "__main__":
    main()
