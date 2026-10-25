# -*- coding: utf-8 -*-
"""
FREE · offline — lấy danh sách phần tử THẬT của mỗi màn AndroidControl từ cây trợ năng.

Nguồn: `HarrytheOrange/parsed_AndroidControl` → `all_forest_dict.zip` (99.131 màn).
Mỗi màn là một danh sách cửa sổ, mỗi cửa sổ có `tree` gồm các nút với `bounds_in_screen`,
`class_name`, `text`, `content_description`, và các cờ (`is_clickable`, `is_visible_to_user`…).

Dùng để thay bộ dò hình khi chấm theo nút gần nhất: chấm vị trí chỉ cần HỘP, mà cây trợ năng
cho hộp đầy đủ hơn hẳn (trung vị 86 phần tử/màn so với 24 của bộ dò hình). Ngược lại nó gần
như không cho TÊN (đo được 12,6% phần tử có nhãn) nên không dùng cho việc lấy tên nút.

Chạy trực tiếp để xem thống kê: ~/.venvs/thesis/bin/python harness/a11y_inventory.py
"""
import os, re, json, zipfile, pickle, functools

HERE = os.path.dirname(os.path.abspath(__file__))
_ZIP = None


def _zip():
    global _ZIP
    if _ZIP is None:
        from huggingface_hub import hf_hub_download
        p = hf_hub_download("HarrytheOrange/parsed_AndroidControl", "all_forest_dict.zip",
                            repo_type="dataset")
        _ZIP = zipfile.ZipFile(p)
    return _ZIP


def key_for(rel):
    """Từ tên ảnh kiểu 'episode_17136_screenshot_1.png' → khoá trong zip."""
    m = re.search(r"episode_(\d+)_screenshot_(\d+)\.png", rel)
    if not m:
        return None
    return f"all_forest_dict/android_control_episode_[{m.group(1)}]_{m.group(2)}.pkl"


@functools.lru_cache(maxsize=512)
def _load(key):
    z = _zip()
    if key not in z.namelist():
        return None
    with z.open(key) as f:
        return pickle.loads(f.read())


def elements(rel, only_clickable=False, drop_system_bar=True, min_side=8):
    """Trả danh sách hộp [x1,y1,x2,y2] của các phần tử hiển thị trên màn.

    only_clickable: chỉ giữ phần tử có cờ bấm được (gần với 'nút' hơn, nhưng bỏ sót
                    nhiều phần tử thật vì cờ này hay bị đặt ở nút cha).
    drop_system_bar: bỏ cửa sổ của thanh trạng thái hệ thống (giờ, pin, sóng).
    """
    o = _load(key_for(rel) or "")
    if not o:
        return []
    out = []
    for w in o:
        if drop_system_bar and w.get("window_type") == 3:
            continue
        for n in w.get("tree", []):
            if not n.get("is_visible_to_user"):
                continue
            if only_clickable and not n.get("is_clickable"):
                continue
            b = n.get("bounds_in_screen") or {}
            x1, y1 = b.get("left", 0), b.get("top", 0)
            x2, y2 = b.get("right", 0), b.get("bottom", 0)
            if x2 - x1 < min_side or y2 - y1 < min_side:
                continue
            out.append([float(x1), float(y1), float(x2), float(y2)])
    return out


def labelled(rel):
    """Các phần tử CÓ tên, trả (tên, hộp). Dùng để xem cây trợ năng cho được gì."""
    o = _load(key_for(rel) or "")
    if not o:
        return []
    out = []
    for w in o:
        if w.get("window_type") == 3:
            continue
        for n in w.get("tree", []):
            if not n.get("is_visible_to_user"):
                continue
            name = (n.get("text") or "").strip() or (n.get("content_description") or "").strip()
            if not name:
                continue
            b = n.get("bounds_in_screen") or {}
            out.append((name, [b.get("left", 0), b.get("top", 0), b.get("right", 0), b.get("bottom", 0)]))
    return out


if __name__ == "__main__":
    import statistics as st
    pred = json.load(open(os.path.join(HERE, "dg1_cache", "ground_pilot", "pred.json"), encoding="utf-8"))
    n_all, n_click, n_lab = [], [], []
    miss = 0
    for rel in pred:
        e = elements(rel)
        if not e:
            miss += 1
            continue
        n_all.append(len(e))
        n_click.append(len(elements(rel, only_clickable=True)))
        n_lab.append(len(labelled(rel)))
    print("=" * 66)
    print(f"{len(n_all)} màn có cây trợ năng (thiếu {miss})")
    print(f"  phần tử hiển thị / màn : trung vị {st.median(n_all):.0f}")
    print(f"  trong đó bấm được      : trung vị {st.median(n_click):.0f}")
    print(f"  trong đó có tên        : trung vị {st.median(n_lab):.0f}")
    print("=" * 66)
