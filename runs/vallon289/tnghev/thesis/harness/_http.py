# -*- coding: utf-8 -*-
"""Goi chat/completions co RETRY + BACKOFF (xu ly 429 rate-limit). Khong in key."""
import json, time, urllib.request, urllib.error

def chat(base, model, messages, key, temperature=0, retries=8, timeout=600):
    url = base.rstrip("/") + "/chat/completions"
    data = json.dumps({"model": model, "temperature": temperature, "messages": messages}).encode("utf-8")
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429 and i < retries - 1:
                ra = e.headers.get("Retry-After")
                time.sleep(float(ra) if ra else min(2 ** i + 1, 40))   # cho-lui khi rate-limit
                continue
            raise
        except Exception as e:
            last = e
            if i < retries - 1:
                time.sleep(min(2 ** i, 20)); continue
            raise
    raise last
