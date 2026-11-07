# -*- coding: utf-8 -*-
"""Ba phần thưởng mới cho lưới GRPO (report/330 §7 hàng 5–6, report/326 T5). KHÔNG sửa grpo_luoi.py:
tệp này nạp grpo_luoi, đăng ký thêm tên vào --reward rồi gọi đúng main() của nó.

  spice_cong  r = SPICE · a − phạt độ dài          a = 1 nếu đúng loại thao tác, A_SAI (mặc định 0,1) nếu sai
  ten_loai    r = 0,5 · F1(tên) + 0,5 · a − phạt    a ∈ {0, 1}; bước không có tên vàng: r = a − phạt
  loai        r = a − phạt                           (T5, chỉ để giải thích: thưởng đúng loại thao tác)

· Loại thao tác: metric_exec.canon_action(·, strict_back=True) của câu sinh so với của câu chuẩn
  (đúng phép so của kiểm noharm).
· Phạt độ dài như mọi thưởng của lưới: 0,02 · max(0, số từ − số từ câu chuẩn − 3); câu rỗng = 0.
· Tên vàng: `descriptors_ten.jsonl` (dựng từ harness/dg1_cache/train_ac/descriptors.jsonl, chỉ tầng
  `ten_ro`, 30.233 bước; tầng ký hiệu và không tên coi như không có tên). Tra theo cột `key` mà TRL
  chuyển vào hàm thưởng. F1 tính trên tập token: R = phần token của tên có trong câu; P = phần token
  "nội dung" của câu có trong tên, với token nội dung = token câu trừ mạo từ/giới từ, động từ thao tác,
  từ vai trò chung (button, icon…) và từ vị trí, để câu không bị phạt vì nói vai trò hay vị trí.

  python thuong_moi.py --selftest-moi [--bundle B]                       # CPU, không cần GPU
  python thuong_moi.py --train --reward spice_cong --bundle B --merged M --out O --resume auto
  (mọi cờ khác y như grpo_luoi.py)
"""
import os, sys, json, glob, time

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import grpo_luoi as GL          # noqa: E402
import grpo_spice as GS         # noqa: E402
import metric_exec as ME        # noqa: E402

MOI = ("spice_cong", "ten_loai", "loai")
A_SAI = float(os.environ.get("THUONG_A_SAI", "0.1"))
STOP = {"the", "a", "an", "on", "of", "to", "in", "at", "for", "and", "with", "from", "into", "onto", "is", "it",
        "this", "that", "then", "its", "your", "my", "there", "here", "which", "named", "called", "labelled",
        "labeled", "option", "button", "icon", "tab", "text", "field", "bar", "link", "menu", "item", "screen",
        "page", "app", "application", "symbol", "box", "key"}
STOP |= set(ME.ACTION_MAP) | set(ME.POSITION_WORDS) | {"corner", "top", "bottom", "right", "left"}
TEN = {}


def nap_ten(bundle=None):
    if TEN:
        return
    c = [os.environ.get("THUONG_TEN", "")] + ([os.path.join(bundle, "descriptors_ten.jsonl")] if bundle else [])
    c += [os.path.join(H, "descriptors_ten.jsonl")]
    c += [p for p in glob.glob("/kaggle/input/**/descriptors_ten.jsonl", recursive=True) if "/notebooks/" not in p]
    p = next((x for x in c if x and os.path.exists(x)), None)
    assert p, "⛔ ten_loai cần descriptors_ten.jsonl (đặt THUONG_TEN hoặc để cạnh thuong_moi.py)"
    for l in open(p, encoding="utf-8"):
        d = json.loads(l)
        TEN[d["key"]] = d["name"]
    print(f"[ten_loai] {len(TEN)} tên vàng từ {p}", flush=True)


def dung_loai(s, g):
    return ME.canon_action(s, strict_back=True) == ME.canon_action(g, strict_back=True)


def f1_ten(s, name):
    tn = set(GL.tok(name)) - {""}
    if not tn:
        return None
    ts = set(GL.tok(s))
    nd = ts - STOP
    r = len(tn & ts) / len(tn)
    p = len(nd & tn) / len(nd) if nd else 0.0
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)


def diem_moi(name, sents, golds, keys):
    if name == "spice_cong":
        sp = GS.spice_batch(sents, golds)
        return [x * (1.0 if dung_loai(s, g) else A_SAI) for x, s, g in zip(sp, sents, golds)]
    out = []
    for s, g, k in zip(sents, golds, keys):
        a = 1.0 if dung_loai(s, g) else 0.0
        if name == "loai":
            out.append(a)
            continue
        f = f1_ten(s, TEN.get(k, "")) if k is not None else None
        out.append(a if f is None else 0.5 * f + 0.5 * a)
    return out


_goc_dung, _goc_lam = GL.dung_bo_cham, GL.lam_thuong
STAT = {"n": 0}


def dung_bo_cham(name, bundle):
    if name == "ten_loai":
        return nap_ten(bundle)
    if name in MOI:
        return None
    return _goc_dung(name, bundle)


def lam_thuong(name):
    if name not in MOI:
        return _goc_lam(name)

    def thuong(completions, gold, **kw):
        t0 = time.time()
        sents = [GS._text(c).strip() for c in completions]
        keys = kw.get("key") or [None] * len(sents)
        idx = [i for i, s in enumerate(sents) if s]
        sc = diem_moi(name, [sents[i] for i in idx], [gold[i] for i in idx], [keys[i] for i in idx]) if idx else []
        f = dict(zip(idx, sc))
        out = [0.0 if not s else f[i] - GS.MU * max(0, GS.nwords(s) - GS.nwords(g) - 3)
               for i, (s, g) in enumerate(zip(sents, gold))]
        GL.LAST["r"] = list(out)
        STAT["n"] += 1
        sai = sum(1 for i in idx if not dung_loai(sents[i], gold[i]))
        print(f"[{name}] lần {STAT['n']} · {len(sents)} câu · {time.time() - t0:.1f}s · thưởng TB {sum(out)/len(out):.3f}"
              f" · sai loại {sai} · rỗng {len(sents) - len(idx)}", flush=True)
        return out
    thuong.__name__ = f"r_{name}"
    return thuong


def cai():
    if "spice_cong" not in GL.REWARDS:
        GL.REWARDS = tuple(GL.REWARDS) + MOI
    GL.dung_bo_cham, GL.lam_thuong = dung_bo_cham, lam_thuong


def selftest_moi(bundle=None):
    cai()
    TEN.update({"t_1": "Search here", "t_2": "Settings"})
    gold = ["Click on the search bar", "Scroll down", "Click on the Settings icon", "Go back", "Open the Clock app"]
    keys = ["t_1", None, "t_2", None, None]
    ca = {
        "dung":        ["Click on the search bar", "Scroll down", "Click on the Settings icon at the top", "Go back", "Open the Clock app"],
        "sai_loai":    ["Swipe up to the search bar", "Click on the down arrow", "Swipe up on the Settings", "Click on the home icon", "Scroll down"],
        "sai_phan_tu": ["Click on the play button", "Scroll down", "Click on the Wi-Fi icon", "Go back", "Open the Clock app"],
    }
    assert all(dung_loai(s, g) for s, g in zip(ca["dung"], gold)) and not any(dung_loai(s, g) for s, g in zip(ca["sai_loai"], gold))
    R = {}
    for name in MOI:
        dung_bo_cham(name, bundle) if name != "ten_loai" else None
        R[name] = {k: GL.lam_thuong(name)(v, gold, key=keys) for k, v in ca.items()}
        print(f"  {name:10s}", {k: [round(x, 3) for x in v] for k, v in R[name].items()}, flush=True)
    # 1) câu rỗng = 0, mọi thưởng
    for name in MOI:
        assert GL.lam_thuong(name)(["", "Scroll down"], ["Scroll down", "Scroll down"], key=[None, None])[0] == 0.0, name
    # 2) sai loại thao tác thấp hơn đúng loại ở MỌI bước, mọi thưởng mới
    #    (spice_cong: chỉ đòi chặt ở bước SPICE câu đúng > 0; đo 6/11: SPICE("Scroll down","Scroll down") = 0
    #     vì câu không có tuple, nên cổng không hạ được gì ở đó — xem report/320 mục 16)
    sp_d = GS.spice_batch(ca["dung"], gold)
    print("  SPICE câu đúng:", [round(x, 3) for x in sp_d], flush=True)
    for name in MOI:
        d, s = R[name]["dung"], R[name]["sai_loai"]
        chat = [i for i in range(len(d)) if name != "spice_cong" or sp_d[i] > 0]
        assert all(d[i] > s[i] for i in chat) and all(x >= y - 1e-9 for x, y in zip(d, s)), \
            f"⛔ {name} không phạt sai loại: {d} vs {s}"
    # 3) spice_cong = spice khi đúng loại; = A_SAI·spice khi sai loại
    sp = GS.spice_batch(ca["sai_loai"], gold)
    assert all(abs(r - (x * A_SAI - GS.MU * max(0, GS.nwords(c) - GS.nwords(g) - 3))) < 1e-9
               for r, x, c, g in zip(R["spice_cong"]["sai_loai"], sp, ca["sai_loai"], gold)), "⛔ cổng spice"
    # 4) ten_loai phân biệt phần tử ở bước có tên; loai thì KHÔNG (đúng thiết kế T5)
    for i in (0, 2):
        assert R["ten_loai"]["dung"][i] > R["ten_loai"]["sai_phan_tu"][i] + 0.2, R["ten_loai"]
        assert abs(R["loai"]["dung"][i] - R["loai"]["sai_phan_tu"][i]) < 0.05, R["loai"]
    # 5) bước không tên: ten_loai = loai
    for i in (1, 3, 4):
        assert abs(R["ten_loai"]["dung"][i] - R["loai"]["dung"][i]) < 1e-9
    # 6) F1 tên: nêu vai trò/vị trí không bị phạt
    assert f1_ten("Click on the Settings icon at the top right corner", "Settings") == 1.0
    assert f1_ten("Click on the search bar", "Search here") == 2 * 1 * 0.5 / 1.5
    # 7) đăng ký vào --reward của grpo_luoi
    assert set(MOI) <= set(GL.REWARDS) and GL.lam_thuong is lam_thuong
    TEN.pop("t_1"), TEN.pop("t_2")
    print("✅ selftest thưởng mới ĐẠT:", MOI, "· A_SAI =", A_SAI, flush=True)


if __name__ == "__main__":
    if "--selftest-moi" in sys.argv:
        b = sys.argv[sys.argv.index("--bundle") + 1] if "--bundle" in sys.argv else None
        selftest_moi(b)
    else:
        cai()
        GL.main()
