# -*- coding: utf-8 -*-
"""Kiểm colab_logic.py bằng tiến trình giả (CPU, Kaggle). Chạy: python kiem_logic.py <thư mục chứa colab_logic.py> <thư mục làm việc>
Phải được gọi trong session riêng (notebook dùng start_new_session=True), vì T7 gửi SIGINT cho chính nhóm tiến trình."""
import os, sys, json, time, shutil, signal, subprocess, ast, zipfile, traceback

SRC, W = sys.argv[1], sys.argv[2]
sys.path.insert(0, SRC)
import colab_logic as C   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FAKE = os.path.join(HERE, "fake_train.py")
PY = sys.executable
KQ = {}
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)


def ghi(ten, dat, chi_tiet=""):
    KQ[ten] = dict(dat=bool(dat), chi_tiet=str(chi_tiet))
    print(f"[{'ĐẠT' if dat else 'TRƯỢT'}] {ten} · {chi_tiet}", flush=True)


def thu(ten):
    def deco(fn):
        try:
            fn()
        except Exception:
            ghi(ten, False, traceback.format_exc()[-800:])
        return fn
    return deco


@thu("T1 dựng lệnh")
def t1():
    ca = {  # lượt → (script, cờ phải có, thư mục)
        "grpo:spice:101": ("grpo_luoi.py", ["--algo", "grpo", "--keys-ck500"], "grpo_spice_101"),
        "scst:cider:101": ("grpo_codien.py", ["--algo", "scst"], "scst_cider_101"),
        "grpo:bleu4:101": ("grpo_luoi.py", ["--reward", "bleu4"], "grpo_bleu4_101"),
        "rft:spice:101": ("grpo_codien.py", [], "rft_spice_101"),
        "grpo:spice:101:beta=0,loss=dapo,tag=dapo": ("grpo_codien.py", ["--beta", "0", "--loss-type", "dapo"], "grpo_spice_101_dapo"),
        "ppo:spice:101:mu=2,lam=1.0,steps=1000,tag=l1": ("grpo_ppo.py", ["--mu", "2", "--lam", "1.0", "--max-steps", "1000"], "ppo_spice_101_l1"),
        "a2c:spice:101": ("grpo_ppo.py", ["--algo", "a2c"], "a2c_spice_101"),
        "gspo:spice:101:steps=1000,tag=s1000": ("grpo_moi_b1.py", ["--algo", "gspo", "--max-steps", "1000"], "gspo_spice_101_s1000"),
        "dpo_on:spice:101:dpo_beta=0.1,tag=b01": ("grpo_moi_b1.py", ["--dpo-beta", "0.1"], "dpo_on_spice_101_b01"),
        "grpo:spice_cong:101": ("thuong_moi.py", ["--reward", "spice_cong"], "grpo_spice_cong_101"),
        "sft:spice:101": ("sft_tiep.py", [], "sft_spice_101"),
        "seqgan:spice:101": ("grpo_moi_b2.py", ["--algo", "seqgan"], "seqgan_spice_101"),
        "grpo:bcmr:101": ("grpo_moi_b2.py", ["--algo", "grpo", "--reward", "bcmr"], "grpo_bcmr_101"),
        "es:spice:101:es_sigma=0.002,tag=s2": ("grpo_moi_b2.py", ["--es-sigma", "0.002"], "es_spice_101_s2"),
        "rlce:spice:101:ce_lam=0.2,tag=c2": ("grpo_moi_b2.py", ["--ce-lam", "0.2"], "rlce_spice_101_c2"),
        "mixer:spice:101": ("grpo_moi_b2.py", [], "mixer_spice_101"),
        "quark:spice:101": ("grpo_moi_b2.py", [], "quark_spice_101"),
    }
    sai = []
    for l, (t, co, d) in ca.items():
        cmd = C.dung_lenh(l, "/B", "/M", f"/O/{C.ten_thu_muc(l)}", keys="/K.json")
        ok = cmd[1] == t and all(x in cmd for x in co) and C.ten_thu_muc(l) == d and "--resume" in cmd and "auto" in cmd
        if not ok:
            sai.append((l, cmd[1], C.ten_thu_muc(l)))
    # probe không truyền keys và không có --train
    cp = C.dung_lenh("grpo:spice:101", "/B", "/M", "/O", probe=True, keys="/K.json")
    if "--probe" not in cp or "--keys-ck500" in cp or C.ten_thu_muc("grpo:spice:101", probe=True) != "probe_grpo_spice_101":
        sai.append(("probe", cp))
    # lượt sai phải bị chặn
    for l in ("ppo:spice:101:mu=2", "grpo:spice:101:lam=0.9,tag=x", "foo:spice:101", "grpo:abc:101",
              "rft:spice_cong:101", "grpo:spice:101:dpo_beta=0.1,tag=x",
              "rloo:bcmr:101", "seqgan:spice:101:es_sigma=0.1,tag=x", "es:spice:101:ce_lam=0.1,tag=x"):
        try:
            C.phan_tich(l); sai.append(("không chặn", l))
        except AssertionError:
            pass
    phu = C.tep_phu_thuoc("grpo:ten_loai:101")
    if "descriptors_ten.jsonl" not in phu or "metric_exec.py" not in phu:
        sai.append(("phụ thuộc thuong_moi", phu))
    if "grpo_codien.py" not in C.tep_phu_thuoc("gspo:spice:101"):
        sai.append(("phụ thuộc b1", C.tep_phu_thuoc("gspo:spice:101")))
    if C.tep_phu_thuoc("es:spice:101")[-2:] != ["grpo_codien.py", "grpo_moi_b2.py"]:
        sai.append(("phụ thuộc b2", C.tep_phu_thuoc("es:spice:101")))
    ghi("T1 dựng lệnh", not sai, f"{len(ca)} lượt + 9 lượt sai bị chặn · lỗi {sai}")


def chay_gia(out, N, extra=()):
    log = os.path.join(out, "train.log")
    os.makedirs(out, exist_ok=True)
    return C.chay([PY, FAKE, "--train", "--out", out, "--max-steps", str(N), "--resume", "auto", *extra], log, W)


OUT, DR = os.path.join(W, "content", "ppo_spice_101_l1"), os.path.join(W, "drive", "luoi_colab", "ppo_spice_101_l1")


@thu("T3 lượt đầu + đồng bộ + trần giờ")
def t3():
    p = chay_gia(OUT, 40)
    khac = os.getpgid(p.pid) != os.getpgrp()
    rc, td, nap = C.theo_doi(p, OUT, DR, 40, time.time(), cat_gio=7 / 3600, in_moi=1, dong_bo_moi=3, on_dinh=1)
    du = [C.buoc_cua(x) for x in C.diem_luu_du(DR)]
    tam = [x for x in os.listdir(DR) if x.startswith(".tam")]
    ok = khac and 0 < td["buoc"] < 40 and du and len(du) <= 3 and not tam and os.path.exists(os.path.join(DR, "train.log.drive")) \
        and du[-1] == max(C.buoc_cua(x) for x in C.diem_luu_du(OUT)) and nap[0] is True
    ghi("T3 lượt đầu + đồng bộ + trần giờ", ok,
        f"pgid riêng {khac} · dừng ở bước {td['buoc']}/40 (mã {rc}) · Drive {du} (giữ ≤3) · tạm {tam} · nạp {nap}")


@thu("T4 mất máy rồi chạy tiếp từ Drive")
def t4():
    du_truoc = C.buoc_cua(C.diem_luu_du(DR)[-1])
    shutil.rmtree(os.path.join(W, "content"))           # máy ảo mới: /content trống
    n = C.khoi_phuc(DR, OUT)
    p = chay_gia(OUT, 40)
    dong = []
    def inra(*x, **k):
        dong.append(" ".join(map(str, x))); print(*x, **k)
    rc, td, nap = C.theo_doi(p, OUT, DR, 40, time.time(), in_moi=1, dong_bo_moi=3, on_dinh=1, inra=inra)
    import re as _re
    chep = [int(v) for l in dong if "chép" in l for g in _re.findall(r"\[([\d, ]+)\]", l) for v in g.split(",") if v.strip()]
    du = [C.buoc_cua(x) for x in C.diem_luu_du(DR)]
    ok = n == du_truoc and td["goc"] == du_truoc and chep and min(chep) > du_truoc and len(chep) == len(set(chep)) and td["resume"] and nap[0] is True and td["buoc"] == 40 and rc == 0 \
        and td["xong"] and du[-1] == 40 and td["n_log"] == 40 - du_truoc
    ghi("T4 mất máy rồi chạy tiếp từ Drive", ok,
        f"khôi phục bước {n} (Drive có {du_truoc}) · tiếp từ {td['goc']} · nạp default {td['nap_default']} → {nap} · "
        f"xong {td['buoc']}/40, {td['n_log']} dòng log mới · Drive {du} · đã chép {chep} · mã {rc}")


@thu("T5 nạp default hỏng thì dừng")
def t5():
    o = os.path.join(W, "content", "hong"); d = os.path.join(W, "drive", "hong")
    shutil.copytree(C.diem_luu_du(DR)[-2], os.path.join(o, "checkpoint-35"))
    p = chay_gia(o, 40, ["--hong-nap"])
    t = time.time()
    rc, td, nap = C.theo_doi(p, o, d, 40, t, in_moi=1, dong_bo_moi=3)
    ok = nap[0] is False and rc != 0 and time.time() - t < 25
    ghi("T5 nạp default hỏng thì dừng", ok, f"kiểm {nap} · mã {rc} · {time.time() - t:.0f} s")


@thu("T6 điểm lưu dở không được dùng")
def t6():
    o = os.path.join(W, "content", "do"); d = os.path.join(W, "drive", "do")
    for n, du in ((10, True), (15, False)):
        q = os.path.join(o, f"checkpoint-{n}"); os.makedirs(q)
        for f in C.TEP_CAN if du else C.TEP_CAN[:2]:
            open(os.path.join(q, f), "w").write("x")
    chua = C.dong_bo_len(o, d)                            # vừa ghi xong: chưa yên 60 s ⇒ không chép
    moi = C.dong_bo_len(o, d, on_dinh=0)
    os.makedirs(os.path.join(d, ".tam_checkpoint-20"))     # dấu vết mất máy giữa lúc chép
    shutil.rmtree(o)
    n = C.khoi_phuc(d, o)
    ok = chua == [] and moi == [10] and [C.buoc_cua(x) for x in C.diem_luu_du(d)] == [10] and n == 10
    ghi("T6 điểm lưu dở không được dùng", ok, f"chưa yên {chua} · chép {moi} · Drive {[C.buoc_cua(x) for x in C.diem_luu_du(d)]} · khôi phục {n}")


@thu("T7 SIGINT vào nhóm notebook không giết lượt train")
def t7():
    o = os.path.join(W, "content", "sig")
    p = chay_gia(o, 30)                                   # start_new_session=True
    q = subprocess.Popen([PY, FAKE, "--train", "--out", o + "_doi_chung", "--max-steps", "30"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)   # đối chứng: cùng nhóm
    time.sleep(3)
    cu = signal.signal(signal.SIGINT, signal.SIG_IGN)
    os.killpg(os.getpgrp(), signal.SIGINT)               # như bấm Stop một ô
    time.sleep(2)
    signal.signal(signal.SIGINT, cu)
    song, chet = p.poll() is None, q.poll() is not None
    C.dung(p, 10); q.wait() if q.poll() is None else None
    ghi("T7 SIGINT vào nhóm notebook không giết lượt train", song and chet,
        f"lượt start_new_session còn sống {song} · đối chứng cùng nhóm đã chết {chet}")


@thu("T8 thăm dò + chọn máy")
def t8():
    o = os.path.join(W, "content", "probe_x")
    os.makedirs(o)
    p = C.chay([PY, FAKE, "--probe", "--out", o, "--ngu", "0.1"], os.path.join(o, "train.log"), W)
    p.wait()
    s, v = C.doc_tham_do(os.path.join(o, "train.log"))
    ca = [(C.chon_may("NVIDIA L4", 14.2, 150)[0], "L4"),
          (C.chon_may("NVIDIA L4", 19.0, 150)[0], "A100"),
          (C.chon_may("NVIDIA L4", 14.2, 150, s_buoc_a100=90)[0], "A100"),   # 1,67 > 1,5
          (C.chon_may("NVIDIA L4", 14.2, 150, s_buoc_a100=110)[0], "L4"),    # 1,36 ≤ 1,5
          (C.chon_may("NVIDIA A100-SXM4-40GB", 14.2, 60, s_buoc_l4=85)[0], "L4"),
          (C.chon_may("NVIDIA A100-SXM4-40GB", 14.2, 60)[0], "?")]
    ok = s is not None and abs(v - 14.2) < 1e-6 and all(a == b for a, b in ca)
    ghi("T8 thăm dò + chọn máy", ok, f"đọc probe s/bước {s} · VRAM {v} · luật {ca}")


@thu("T9 nén kết quả")
def t9():
    z = os.path.join(W, "kq.zip")
    n = C.nen(OUT, z, giu_ck=1)
    ten = zipfile.ZipFile(z).namelist()
    opt = [x for x in ten if x.endswith("optimizer.pt")]
    ok = n > 0 and len(opt) == 1 and "checkpoint-40" in opt[0] and any(x.endswith("train.log") for x in ten)
    ghi("T9 nén kết quả", ok, f"{n} tệp · optimizer chỉ ở {opt}")


@thu("T10 notebook hợp lệ")
def t10():
    nbp = os.path.join(SRC, "colab_luoi_train.ipynb")
    nb = json.load(open(nbp))
    loi = []
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code":
            continue
        s = "".join(c["source"])
        try:
            ast.parse("\n".join(l for l in s.splitlines() if not l.lstrip().startswith(("!", "%"))))
        except SyntaxError as e:
            loi.append((i, str(e)))
    src = "".join("".join(c["source"]) for c in nb["cells"])
    can = ["start_new_session", "theo_doi", "khoi_phuc", "dong_bo_len", "0.29.1", "5.20.2", "0.21.2",
           "0c60a4418d54eaf27bf1d27b895538b7", "nen(", "chon_may", "[nạp default]"]
    thieu = [k for k in can if k not in src]
    khong = [k for k in ("clear_output(",) if k in src]   # lệnh gọi; chữ trong chú thích thì được
    ghi("T10 notebook hợp lệ", not loi and not thieu and not khong,
        f"{sum(c['cell_type'] == 'code' for c in nb['cells'])} ô mã · lỗi cú pháp {loi} · thiếu {thieu} · cấm {khong}")


@thu("T11 phát hiện lượt cũ còn sống")
def t11():
    o = os.path.join(W, "content", "cu")
    p = chay_gia(o, 25)
    time.sleep(2)
    ps = C.tim_tien_trinh(o)
    q = C.TienTrinhCu(ps[0], None) if ps else None
    song = q is not None and q.poll() is None
    C.dung(p, 10)
    q.wait(10) if q else None
    ok = ps == [p.pid] and song and q.poll() is not None and C.tim_tien_trinh(o) == []
    ghi("T11 phát hiện lượt cũ còn sống", ok, f"pgrep {ps} (pid thật {p.pid}) · còn sống {song} · sau khi dừng {C.tim_tien_trinh(o)}")


@thu("T12 PPO: value_head.pt ghi sau vẫn lên Drive đủ")
def t12():
    o = os.path.join(W, "content", "ppo_spice_101_l95"); d = os.path.join(W, "drive", "ppo_spice_101_l95")
    them = C.tep_them("ppo:spice:101:mu=2,lam=0.95,steps=1000,tag=l95")
    # chép vội (on_dinh=0, không đòi value_head) có bắt được điểm lưu thiếu không: đối chứng cho thấy cửa sổ là thật
    p = chay_gia(o, 30, ["--ppo", "--ngu", "0.2"])
    thieu = 0
    while p.poll() is None:
        thieu += sum(1 for x in C.diem_luu_du(o) if not os.path.exists(os.path.join(x, "value_head.pt")))
        time.sleep(0.1)
    shutil.rmtree(o)
    p = chay_gia(o, 30, ["--ppo", "--ngu", "0.2"])
    rc, td, _ = C.theo_doi(p, o, d, 30, time.time(), cat_gio=5 / 3600, in_moi=1, dong_bo_moi=1, them=them, on_dinh=1)
    du = C.diem_luu_du(d, them)
    du_vh = all(os.path.exists(os.path.join(x, "value_head.pt")) for x in C.diem_luu_du(d))
    shutil.rmtree(o)
    n = C.khoi_phuc(d, o, them)
    p = chay_gia(o, 30, ["--ppo", "--ngu", "0.2"])
    rc2, td2, nap2 = C.theo_doi(p, o, d, 30, time.time(), in_moi=1, dong_bo_moi=1, them=them, on_dinh=1)
    ok = them == ("value_head.pt",) and thieu > 0 and du and du_vh and n > 0 and rc2 == 0 and td2["goc"] == n and td2["buoc"] == 30
    ghi("T12 PPO: value_head.pt ghi sau vẫn lên Drive đủ", ok,
        f"đối chứng thấy {thieu} lần điểm lưu đủ 3 tệp mà thiếu value_head · Drive {[C.buoc_cua(x) for x in du]} đều có value_head {du_vh} · "
        f"chạy tiếp từ {td2['goc']} (khôi phục {n}) tới {td2['buoc']}/30 mã {rc2}")


@thu("T13 điểm lưu riêng của B2 (ES không optimizer, SeqGAN có discriminator)")
def t13():
    sai = []
    for luot, co, thieu in (("es:spice:101", ("adapter_model.safetensors", "trainer_state.json", "es_state.json"), "es_state.json"),
                            ("seqgan:spice:101", C.TEP_CAN + ("discriminator.pt",), "discriminator.pt"),
                            ("quark:spice:101", C.TEP_CAN + ("quark_pool.json",), "quark_pool.json")):
        them = C.tep_them(luot)
        o = os.path.join(W, "content", "b2_" + luot.split(":")[0]); d = os.path.join(W, "drive", "b2_" + luot.split(":")[0])
        for n, du in ((10, True), (20, False)):
            q = os.path.join(o, f"checkpoint-{n}"); os.makedirs(q)
            for f in co if du else [x for x in co if x != thieu]:
                open(os.path.join(q, f), "w").write("x")
        moi = C.dong_bo_len(o, d, them=them, on_dinh=0)
        shutil.rmtree(o)
        n = C.khoi_phuc(d, o, them)
        if moi != [10] or n != 10 or sorted(os.listdir(os.path.join(o, "checkpoint-10"))) != sorted(co):
            sai.append((luot, moi, n))
    ghi("T13 điểm lưu riêng của B2 (ES không optimizer, SeqGAN có discriminator)", not sai,
        f"es/seqgan/quark: chỉ điểm lưu đủ tệp riêng được chép và khôi phục · lỗi {sai}")


json.dump(KQ, open(os.path.join(W, "kiem_logic.json"), "w"), ensure_ascii=False, indent=1)
hong = [k for k, v in KQ.items() if not v["dat"]]
print(f"\n===== {len(KQ) - len(hong)}/{len(KQ)} ĐẠT · trượt {hong}", flush=True)
sys.exit(1 if hong else 0)
