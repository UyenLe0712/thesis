# -*- coding: utf-8 -*-
"""
ALOHa-style matcher (embedding + cosine) cho cot "BIA" — chay qua Ollama (nomic-embed-text), CPU, mien phi.
Y tuong: ten nut model viet va ten nut THAT cung NGHIA -> vector gan nhau -> KHONG tinh la bia.
Tach bach voi cot "CLARITY/dung-nhan" (so chuoi chinh xac) o file scorer.

Toi uu: (1) BATCH nhieu text trong 1 request (~9x nhanh hon goi le tren CPU),
        (2) CACHE embed ra DIA -> lan cham sau tuc thi. Khong doi thuat toan/nguong (tau=0.55 giu nguyen).
"""
import json, os, urllib.request, math, re

EMB_URL = "http://localhost:11434/v1/embeddings"
EMB_MODEL = "nomic-embed-text"
_CACHE_FP = os.path.join(os.path.dirname(__file__), "dg1_cache", "emb_cache.json")

# --- cache dia (text -> vector) ---
def _load_disk():
    try:
        return json.load(open(_CACHE_FP, encoding="utf-8"))
    except Exception:
        return {}
_cache = _load_disk()
_dirty = False

def _save_disk():
    global _dirty
    if not _dirty:
        return
    os.makedirs(os.path.dirname(_CACHE_FP), exist_ok=True)
    tmp = _CACHE_FP + ".tmp"
    json.dump(_cache, open(tmp, "w", encoding="utf-8"))
    os.replace(tmp, _CACHE_FP)
    _dirty = False

def _embed_batch(texts):
    """Goi 1 request cho NHIEU text (input la list) -> list vector cung thu tu."""
    data = json.dumps({"model": EMB_MODEL, "input": [t or "" for t in texts]}).encode("utf-8")
    req = urllib.request.Request(EMB_URL, data=data,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        out = json.loads(r.read().decode("utf-8"))["data"]
    return [d["embedding"] for d in out]

def ensure_embedded(texts):
    """Dam bao moi text co trong cache (batch nhung text con thieu trong 1 cu)."""
    global _dirty
    miss = [t for t in dict.fromkeys(t or "" for t in texts) if t not in _cache]
    if miss:
        for i in range(0, len(miss), 64):           # chia lo de tranh request qua lon
            chunk = miss[i:i + 64]
            for t, v in zip(chunk, _embed_batch(chunk)):
                _cache[t] = v
        _dirty = True
        _save_disk()

def embed(text):
    """Embed 1 text (qua cache)."""
    ensure_embedded([text])
    return _cache[text or ""]

def cos(a, b):
    d = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return d / (na * nb + 1e-9)

def best_match(name, labels):
    """Tra ve (label gan nhat, cosine sim) — semantic, dung cho cot BIA."""
    if not labels:
        return None, 0.0
    ensure_embedded([name] + list(labels))          # BATCH: name + tat ca nhan 1 luot
    e = _cache[name or ""]; best, arg = -1.0, None
    for l in labels:
        s = cos(e, _cache[l or ""])
        if s > best:
            best, arg = s, l
    return arg, best

def norm(s): return re.sub(r"\s+", " ", (s or "").lower().strip())
def exact_label(name, labels):
    """So CHINH XAC (chuan hoa) — dung cho cot CLARITY/dung-nhan."""
    nn = norm(name)
    return any(nn == norm(l) or nn in norm(l) or norm(l) in nn for l in labels)

if __name__ == "__main__":
    print("=== TU KIEM matcher ALOHa (synonym phai gan, khac nghia phai xa) ===")
    # English (giong du lieu that MobileViews/AndroidControl)
    labels_en = ["Settings", "OK", "Submit", "Email address"]
    for q in ["Configure", "Settings", "Log out", "email field"]:
        a, s = best_match(q, labels_en)
        print(f"  EN {q!r:22} -> gan nhat {a!r:16} sim={s:.3f}")
    # Vietnamese (xem nomic co hieu khong)
    labels_vi = ["Cài đặt", "OK", "Gửi", "Địa chỉ email"]
    for q in ["Thiết lập", "Cài đặt", "Đăng xuất", "ô email"]:
        a, s = best_match(q, labels_vi)
        print(f"  VI {q!r:22} -> gan nhat {a!r:16} sim={s:.3f}")
