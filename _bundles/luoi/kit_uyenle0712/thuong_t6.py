# -*- coding: utf-8 -*-
"""Hai phần thưởng cho phép đo T6 (report/328 §5, điểm yếu 9): tách SPICE khỏi phần phạt độ dài.
Nhánh kiểm xao101 ghép ngẫu nhiên cả phần phạt (r_spice xáo SAU khi trừ phạt), nên "công của SPICE"
đo bằng ck500 − xao101 thật ra là công của SPICE + phạt. T6 chạy riêng từng phần:

  spice_kp   r = SPICE(câu, câu chuẩn)                          KHÔNG phạt độ dài
  phat_dai   r = −0,02 · max(0, số từ câu − số từ câu chuẩn − 3)  KHÔNG có SPICE (hệ số = GS.MU)
  câu rỗng = 0 ở cả hai, như mọi thưởng của lưới.

Hệ quả phải khai của phat_dai: mọi câu dài không quá số từ câu chuẩn + 3, kể cả câu rỗng và câu
sai hoàn toàn, đều được 0 ⇒ thưởng chỉ phân biệt câu DÀI; nhóm G câu cùng ngắn có độ lệch chuẩn 0
nên lợi thế bằng 0 (chỉ còn KL), còn nhóm có một câu dài thì GRPO chuẩn hoá theo nhóm phóng phần
phạt nhỏ (−0,02) lên cỡ lợi thế ±1. Câu rỗng ngang câu đúng độ dài, nên thưởng này không chặn được
việc mô hình thu câu về rỗng; theo dõi cột "rỗng" trong log.

KHÔNG sửa grpo_luoi.py: nạp grpo_luoi, đăng ký thêm tên vào --reward, thay GL.dung_bo_cham và
GL.lam_thuong (tên cũ chuyển tiếp cho bản trước) rồi gọi đúng GL.main(). Đi chung được với
thuong_moi.py theo cả hai thứ tự nạp (xem cai()).

  python thuong_t6.py --selftest-t6 [--bundle B] [--gia]     # CPU; --gia: SPICE giả, không cần Java
  python thuong_t6.py --train --reward spice_kp --bundle B --merged M --out O --resume auto
  (mọi cờ khác y như grpo_luoi.py)
"""
import os, sys, time, glob, shutil, subprocess

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import grpo_luoi as GL          # noqa: E402
import grpo_spice as GS         # noqa: E402

T6 = ("spice_kp", "phat_dai")
STAT = {"n": 0}
TRUOC = {}                      # bản dung_bo_cham / lam_thuong đứng trước trong chuỗi, chốt lúc cai()


def phat(s, g):
    return GS.MU * max(0, GS.nwords(s) - GS.nwords(g) - 3)


def diem_t6(name, sents, golds):
    """Thưởng cho câu KHÔNG rỗng."""
    if name == "spice_kp":
        return GS.spice_batch(sents, golds)
    if name == "phat_dai":
        return [0.0 - phat(s, g) for s, g in zip(sents, golds)]
    raise ValueError(name)


def dung_bo_cham(name, bundle):
    if name in T6:
        return None             # SPICE dùng GS.spice_batch, phat_dai không cần bộ chấm
    return TRUOC["dung"](name, bundle)


def lam_thuong(name):
    if name not in T6:
        return TRUOC["lam"](name)

    def thuong(completions, gold, **kw):
        t0 = time.time()
        sents = [GS._text(c).strip() for c in completions]
        idx = [i for i, s in enumerate(sents) if s]
        sc = diem_t6(name, [sents[i] for i in idx], [gold[i] for i in idx]) if idx else []
        f = dict(zip(idx, sc))
        out = [f[i] if s else 0.0 for i, s in enumerate(sents)]
        GL.LAST["r"] = list(out)
        STAT["n"] += 1
        bi_phat = sum(1 for i in idx if phat(sents[i], gold[i]) > 0)
        print(f"[{name}] lần {STAT['n']} · {len(sents)} câu · {time.time() - t0:.1f}s · thưởng TB {sum(out)/len(out):.3f}"
              f" · số từ TB {sum(map(GS.nwords, sents))/len(sents):.1f} · bị phạt {bi_phat} · rỗng {len(sents) - len(idx)}",
              flush=True)
        return out
    thuong.__name__ = f"r_{name}"
    return thuong


def cai():
    """Chèn T6 vào chuỗi thưởng của GL, chỉ một lần.

    thuong_moi.py chốt bản đứng trước NGAY LÚC NẠP (_goc_dung/_goc_lam) chứ không lúc cai(), nên nếu
    nó đã nạp mà chưa cai() thì lần cai() sau của nó sẽ đè mất T6. Khi đó T6 đứng SAU thuong_moi:
    trỏ _goc của thuong_moi vào T6, T6 chuyển tiếp cho bản gốc mà thuong_moi đã chốt.
    """
    if TRUOC:
        return
    M = sys.modules.get("thuong_moi")
    if M is not None and GL.lam_thuong is not M.lam_thuong:
        TRUOC["dung"], TRUOC["lam"] = M._goc_dung, M._goc_lam
        M._goc_dung, M._goc_lam = dung_bo_cham, lam_thuong
    else:
        TRUOC["dung"], TRUOC["lam"] = GL.dung_bo_cham, GL.lam_thuong
    if "spice_kp" not in GL.REWARDS:
        GL.REWARDS = tuple(GL.REWARDS) + T6
    GL.dung_bo_cham, GL.lam_thuong = dung_bo_cham, lam_thuong


# ============================ tự kiểm (CPU) ============================
def spice_gia(cands, refs):
    """SPICE giả để kiểm logic khi không có Java: Jaccard trên tập token, trong [0, 1]."""
    out = []
    for c, r in zip(cands, refs):
        a, b = set(GL.tok(c)), set(GL.tok(r))
        out.append(len(a & b) / len(a | b) if a | b else 0.0)
    return out


def _co_java():
    if shutil.which("java"):
        return True
    for b in sorted(glob.glob(os.path.expanduser("~/.jdk/*/bin"))):
        if os.path.exists(os.path.join(b, "java")):
            os.environ["PATH"] = b + os.pathsep + os.environ["PATH"]
            print(f"  [java] thêm {b} vào PATH", flush=True)
            return True
    return False


def kiem_chuoi(co_moi):
    """Gọi sau khi mọi bộ thưởng đã cai(): mọi tên đều tới đúng hàm, không vòng lặp."""
    gold = ["Click on the search bar", "Scroll down"]
    dai = "Click on the search bar at the top of the screen and then wait for it"     # 16 từ vs 5, phạt 0,02·8
    c = [dai, ""]
    assert set(T6) <= set(GL.REWARDS), GL.REWARDS
    for name in ("spice",) + T6 + (("loai", "spice_cong") if co_moi else ()):
        GL.dung_bo_cham(name, None)
        r = GL.lam_thuong(name)(c, gold, key=[None, None])
        assert r[1] == 0.0, (name, r)
        sp = GS.spice_batch([dai], gold[:1])[0]
        ky_vong = {"spice": sp - 0.16, "spice_kp": sp, "phat_dai": -0.16,
                   "loai": 1.0 - 0.16, "spice_cong": sp - 0.16}[name]
        assert abs(r[0] - ky_vong) < 1e-9, (name, r, ky_vong)
    if co_moi:
        M = sys.modules["thuong_moi"]
        assert set(M.MOI) <= set(GL.REWARDS), GL.REWARDS
    assert len(set(GL.REWARDS)) == len(GL.REWARDS), f"⛔ tên trùng: {GL.REWARDS}"


THU_TU = {   # bốn thứ tự nạp/cai(), chạy mỗi cái ở một tiến trình riêng để GL sạch
    "moi_cai_truoc":        "import thuong_moi as M, thuong_t6 as T; M.cai(); T.cai()",
    "t6_cai_truoc":         "import thuong_moi as M, thuong_t6 as T; T.cai(); M.cai()",
    "t6_cai_roi_nap_moi":   "import thuong_t6 as T; T.cai(); import thuong_moi as M; M.cai()",
    "nap_t6_truoc_moi_cai": "import thuong_t6 as T; import thuong_moi as M; M.cai(); T.cai(); T.cai()",
}


def selftest_t6(bundle=None, gia=False):
    that = (not gia) and _co_java()
    if not that:
        GS.spice_batch = spice_gia
        print("  ⚠️ SPICE GIẢ (Jaccard token) — chỉ kiểm logic, không kiểm SPICE thật", flush=True)
    cai()
    # 0) đăng ký
    assert set(T6) <= set(GL.REWARDS) and GL.lam_thuong is lam_thuong
    gold = ["Click on the search bar", "Scroll down", "Click on the Settings icon at the top right corner", "Go back"]
    cand = ["Click on the search bar",
            "",
            "Click on the Settings icon at the top right corner of the screen and then wait for it to open fully",
            "Click on the back arrow"]
    kp = GL.lam_thuong("spice_kp")(cand, gold)
    sp = GL.lam_thuong("spice")(cand, gold)          # bản gốc của lưới, qua chuỗi chuyển tiếp
    pd = GL.lam_thuong("phat_dai")(cand, gold)
    ph = [0.0 if not s else phat(s, g) for s, g in zip(cand, gold)]
    print("  spice_kp:", [round(x, 4) for x in kp], flush=True)
    print("  spice   :", [round(x, 4) for x in sp], flush=True)
    print("  phat_dai:", [round(x, 4) for x in pd], flush=True)
    print("  phạt    :", ph, flush=True)
    # 1) câu rỗng = 0
    assert kp[1] == 0.0 and pd[1] == 0.0 and sp[1] == 0.0
    # 2) spice_kp = spice + phạt, trên cùng câu (câu 3 bị phạt 0,02·(21 − 10 − 3) = 0,16)
    assert abs(ph[2] - 0.16) < 1e-12, ph
    assert all(abs(a - (b + p)) < 1e-9 for a, b, p in zip(kp, sp, ph)), "⛔ spice_kp ≠ spice + phạt"
    # 3) phat_dai đúng công thức, không có SPICE
    assert all(abs(a - b) < 1e-12 for a, b in zip(pd, [0.0, 0.0, -0.16, 0.0])), pd
    assert GL.lam_thuong("phat_dai")(["Tap the button."], ["Click on the search bar"]) == [0.0]   # câu sai mà ngắn = 0
    # 4) SPICE thật: câu trùng câu chuẩn ≈ 1, câu sai phần tử thấp hơn
    k2 = GL.lam_thuong("spice_kp")(["Click on the search bar", "Click on the play button"],
                                   ["Click on the search bar", "Click on the search bar"])
    assert k2[0] > 0.9 and k2[0] > k2[1], k2
    # 5) thứ tự nạp với thuong_moi.py, cả hai chiều (SPICE giả trong tiến trình con, chỉ kiểm chuỗi)
    if os.path.exists(os.path.join(H, "thuong_moi.py")):
        for ten, ma in THU_TU.items():
            code = (f"import sys; sys.path.insert(0, {H!r}); import grpo_spice as GS, thuong_t6 as X; "
                    f"GS.spice_batch = X.spice_gia; {ma}; X.kiem_chuoi(True); print('ok')")
            r = subprocess.run([sys.executable, "-c", code], cwd=H, capture_output=True, text=True)
            dong = (r.stdout + r.stderr).strip().splitlines()
            print(f"  thứ tự {ten:22s} → {'ĐẠT' if r.returncode == 0 and dong[-1:] == ['ok'] else 'HỎNG'}", flush=True)
            assert r.returncode == 0, "\n".join(dong[-15:])
    else:
        print("  ⚠️ không có thuong_moi.py cạnh tệp này: bỏ phép kiểm thứ tự nạp", flush=True)
    kiem_chuoi(False)
    print(f"✅ selftest T6 ĐẠT: {T6} · SPICE {'THẬT (Java)' if that else 'GIẢ'}", flush=True)


if __name__ == "__main__":
    if "--selftest-t6" in sys.argv:
        b = sys.argv[sys.argv.index("--bundle") + 1] if "--bundle" in sys.argv else None
        selftest_t6(b, gia="--gia" in sys.argv)
    else:
        cai()
        GL.main()
