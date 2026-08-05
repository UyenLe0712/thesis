# -*- coding: utf-8 -*-
"""
Module DUNG CHUNG cho DG1: loc nhan rac + nap nhan tu View Hierarchy (khong mo anh).
- is_junk(s): nhan rac (rong / URL-param-quang-cao / qua dai).
- load_labels(vh): list {label, actionable} (giong dg1_scorer.load_screen nhung KHONG mo .jpg).
- clean_elems / kept_screens: dung de loc truoc khi sinh/cham.
Pre-register: danh sach man = kept_screens.json (khoa truoc khi chay chinh).
"""
import json, os, re

MV_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset_samples", "mv_multiapp")
KEPT_FP = os.path.join(os.path.dirname(__file__), "dg1_cache", "kept_screens.json")

# URL / tham so quang cao / ma hoa % -> nhan rac (de gay match nham trong matcher)
_JUNK = re.compile(r'(&label=|https?://|utm_|video_click|\?[a-zA-Z_]+=|\.com/|\.html|%[0-9a-fA-F]{2})')

def is_junk(s):
    s = (s or "").strip()
    if not s:            return True       # rong
    if len(s) > 80:      return True       # qua dai -> body text, khong phai ten nut
    if _JUNK.search(s):  return True       # URL / param / ad
    return False

def app_of(name):
    return name.split("_")[0]

def load_labels(vh_path):
    """List {label, actionable} — KHONG mo anh (nhe, khong can PIL)."""
    o = json.load(open(vh_path, encoding="utf-8"))
    elems = []
    for n in o.get("views", []):
        if not n.get("bounds"):
            continue
        label = (n.get("text") or n.get("content_description") or "").strip()
        if not label:
            continue
        actionable = bool(n.get("clickable") or n.get("editable") or n.get("long_clickable"))
        leaf = n.get("child_count", 0) == 0
        if actionable or leaf:
            elems.append({"label": label, "actionable": actionable})
    return elems

def clean_elems(elems):
    return [e for e in elems if not is_junk(e["label"])]

def kept_screens():
    """Danh sach man da loc (None neu chua chay dg1_filter_data.py)."""
    try:
        return json.load(open(KEPT_FP, encoding="utf-8"))
    except Exception:
        return None
