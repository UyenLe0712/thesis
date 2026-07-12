# -*- coding: utf-8 -*-
"""
CHAM DOC LAP + PHAT HIEN SILENT-ERROR (review 2026-06-30).
Muc dich: pha vong lap-luan (matcher cham != matcher sua) + DO dinh luong moi lo "sua thanh nut-SAI".

KHAC dg1_score_all.py:
  - Matcher CHAM = bge-m3 (DOC LAP voi nomic-embed-text da dung de SUA trong design-E).
  - KHONG dat headline "faithfulness 100%": bao cao trung thuc 3 thu scorer-robust:
      (1) ti-le-bia BASE o NHIEU nguong (robustness, khong chot 1 tau bang mat),
      (2) % fallback + % corrected (cai gia),
      (3) ⭐ SILENT-ERROR: voi moi buoc 'corrected', so cos(ten-GOC model muon, ten-BI-SUA) bang bge-m3;
          thap => design-E thay bang nut-THAT-nhung-XA-NGHIA => kha nang sai im lang.
  - Seed co dinh; cache key theo model (vá bug S1); KHONG dung exact_label rong (vá T4).
  - DG1_LIMIT=N de chay thu N man dau (free, dung cache sinh san co — KHONG goi API sinh moi).

Chay:  DG1_LIMIT=10 python dg1_independent_score.py
"""
import os, sys, json, glob, math, urllib.request, random

RUNS = os.path.join(os.path.dirname(__file__), "dg1_cache", "runs")
EMB_URL = "http://localhost:11434/v1/embeddings"
SCORER_MODEL = os.environ.get("SCORER_EMB", "bge-m3")     # DOC LAP voi nomic (matcher SUA)
CACHE_FP = os.path.join(os.path.dirname(__file__), "dg1_cache", f"emb_cache__{SCORER_MODEL.replace(':','_')}.json")
SEED = 20260630

# ---------- embedding doc lap (cache key GAN model) ----------
def _load():
    try: return json.load(open(CACHE_FP, encoding="utf-8"))
    except Exception: return {}
_cache = _load()

def _save():
    os.makedirs(os.path.dirname(CACHE_FP), exist_ok=True)
    tmp = CACHE_FP + ".tmp"; json.dump(_cache, open(tmp, "w", encoding="utf-8")); os.replace(tmp, CACHE_FP)

def _embed_batch(texts):
    data = json.dumps({"model": SCORER_MODEL, "input": [t or " " for t in texts]}).encode()
    req = urllib.request.Request(EMB_URL, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        return [d["embedding"] for d in json.loads(r.read().decode())["data"]]

def ensure(texts):
    miss = [t for t in dict.fromkeys((t or "") for t in texts) if t not in _cache]
    if miss:
        for i in range(0, len(miss), 32):
            chunk = miss[i:i+32]
            for t, v in zip(chunk, _embed_batch(chunk)): _cache[t] = v
        _save()

def cos(a, b):
    d = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(y*y for y in b))
    return d/(na*nb + 1e-9)

def max_sim(name, labels):
    if not labels or not (name or "").strip(): return 0.0
    ensure([name] + list(labels))
    e = _cache[name]
    return max(cos(e, _cache[l or ""]) for l in labels)

def sim2(a, b):
    if not (a or "").strip() or not (b or "").strip(): return 0.0
    ensure([a, b]); return cos(_cache[a], _cache[b])

# ---------- phan tich ----------
def main():
    files = sorted(glob.glob(os.path.join(RUNS, "*.json")))
    lim = int(os.environ.get("DG1_LIMIT", "0"))
    if lim: files = files[:lim]
    if not files: print("Khong co run."); return
    random.seed(SEED)

    TAUS = [0.50, 0.60, 0.70]
    base_sims, base_steps_total = [], 0          # max-sim moi buoc BASE (de tinh ti-le-bia o nhieu nguong)
    corrected = []                                # (orig, corr, sim, screen, question)
    n_fallback = n_corrected = n_matched = 0
    apps = set()

    for fp in files:
        r = json.load(open(fp, encoding="utf-8"))
        apps.add(r["screen"].split("_")[0])
        labels = r["elem_labels"]
        for s in r["base"]:
            base_sims.append(max_sim(s.get("element",""), labels)); base_steps_total += 1
        for i, s in enumerate(r["sysE"]):
            st = s.get("status")
            if st == "matched": n_matched += 1
            elif st == "fallback": n_fallback += 1
            elif st == "corrected":
                n_corrected += 1
                orig = r["base"][i].get("element","") if i < len(r["base"]) else ""
                corr = s.get("element","")
                corrected.append((orig, corr, sim2(orig, corr), r["screen"], r.get("question","")))

    print("="*82)
    print(f"CHAM DOC LAP bang '{SCORER_MODEL}' (doc lap voi nomic da dung de SUA) | {len(files)} man | app={sorted(apps)}")
    print("="*82)
    if len(apps) == 1:
        print(f"  ⚠️  CHI 1 APP ({sorted(apps)[0]}) -> CI gia-chat, ngoai-suy yeu. Ban chay chinh PHAI nhieu app.\n")

    # (1) ti-le-bia BASE o nhieu nguong (robustness)
    print("(1) TI-LE-BIA BASE (buoc co max-sim < nguong) — do robustness theo nguong:")
    for t in TAUS:
        rate = sum(1 for x in base_sims if x < t) / (base_steps_total or 1)
        print(f"     nguong {t:.2f}:  {rate*100:5.1f}%  ({sum(1 for x in base_sims if x<t)}/{base_steps_total} buoc)")
    print(f"     (max-sim BASE: min={min(base_sims):.2f} trung-binh={sum(base_sims)/len(base_sims):.2f} max={max(base_sims):.2f})")

    # (2) cai gia
    tot = n_matched + n_corrected + n_fallback or 1
    print(f"\n(2) HANH VI design-E:  matched {n_matched} ({n_matched/tot*100:.0f}%) | "
          f"corrected {n_corrected} ({n_corrected/tot*100:.0f}%) | fallback {n_fallback} ({n_fallback/tot*100:.0f}%)")

    # (3) SILENT-ERROR: corrected co xa nghia khong
    print(f"\n(3) ⭐ SILENT-ERROR — voi {n_corrected} buoc 'corrected', do cos(ten-GOC, ten-BI-SUA) bang {SCORER_MODEL}:")
    if corrected:
        sims = [c[2] for c in corrected]
        for thr in [0.5, 0.6, 0.7]:
            bad = sum(1 for x in sims if x < thr)
            print(f"     sim < {thr:.1f} (kha nang SUA-BAY): {bad}/{len(sims)} = {bad/len(sims)*100:.0f}%")
        print(f"     (sim sua: min={min(sims):.2f} trung-binh={sum(sims)/len(sims):.2f} max={max(sims):.2f})")
        print("\n     VI DU corrected XA-NGHIA nhat (nghi sua-bay):")
        for orig, corr, s, scr, q in sorted(corrected, key=lambda c: c[2])[:8]:
            print(f"       [{scr}] '{orig}'  ->  '{corr}'  (sim={s:.2f})  | hoi: {q[:55]}")
    else:
        print("     (khong co buoc corrected trong tap nay)")

    print("\nDOC KET QUA: faithfulness design-E ~100% la CO-DINH-CAU-TRUC (chep nguyen ten that), KHONG bao headline.")
    print("Gia tri thuc = ti-le-bia BASE (1) + cai gia fallback (2) + ti-le sua-bay (3). Sua-bay cao => design-E NGUY HIEM.")

if __name__ == "__main__":
    main()
