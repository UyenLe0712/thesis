# -*- coding: utf-8 -*-
"""Doc API key an toan: uu tien env VLM_API_KEY/OPENAI_API_KEY, roi file harness/.openai_key.
KHONG bao gio in key ra. Mac dinh 'ollama' (Ollama local khong can key)."""
import os
def get_key():
    for v in ("VLM_API_KEY", "OPENAI_API_KEY"):
        k = os.environ.get(v)
        if k and k.strip():
            return k.strip()
    p = os.path.join(os.path.dirname(__file__), ".openai_key")
    if os.path.exists(p):
        return open(p, encoding="utf-8").read().strip()
    return "ollama"
