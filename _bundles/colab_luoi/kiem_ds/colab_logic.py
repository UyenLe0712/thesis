# -*- coding: utf-8 -*-
"""Phần logic của notebook Colab train một lượt lưới RL (colab_luoi_train.ipynb). Tách ra để kiểm được trên
Kaggle CPU bằng tiến trình giả (kiem/kiem_logic.py), không cần GPU hay Colab.

Hàm chính:
  phan_tich(luot)            "algo:reward:seed[:k=v,...]" → (algo, reward, seed, opt)
  tep_cua(luot)              script phải gọi (grpo_luoi / grpo_codien / grpo_ppo / grpo_moi_b1 / thuong_moi / sft_tiep)
  ten_thu_muc(luot, probe)   tên thư mục ra, trùng quy ước make_nb.py (để điểm lưu Kaggle ↔ Colab dùng chung được)
  dung_lenh(...)             dòng lệnh đầy đủ
  diem_luu_du(d)             điểm lưu đủ ba tệp, xếp theo bước
  dong_bo_len(out, dr)       chép điểm lưu mới lên Drive: copytree sang tên tạm rồi đổi tên, giữ K bản cuối
  khoi_phuc(dr, out)         máy mới: chép điểm lưu đủ mới nhất từ Drive về
  tien_do(log)               đọc train.log: số bước, s/bước, [tiếp từ], [nạp default], lỗi
  chon_may(...)              luật chọn L4 hay A100 (CLAUDE.md: tỉ số giờ ≤ 1,5 thì L4; đỉnh VRAM > 17 GiB thì không L4)
  chay(cmd, log, ...)        Popen start_new_session=True, stdout ghi ra tệp local
  theo_doi(...)              vòng foreground: in mỗi in_moi giây, đồng bộ Drive mỗi dong_bo_moi giây, dừng ở trần giờ
"""
import os, re, ast, glob, json, time, shutil, signal, subprocess, statistics as st

CU = ("grpo", "drgrpo", "rloo", "reinforce", "scst")                       # grpo_luoi.py
CD = ("vanilla", "mad", "rft", "cem", "awr", "raml", "rank")                 # grpo_codien.py
B1 = ("dpo_on", "dpo_off", "rft_off", "mrt", "spg", "drgrpo_full", "grpo_seq", "gspo")   # grpo_moi_b1.py
PP = ("ppo", "a2c")                                                          # grpo_ppo.py
B2 = ("rlce", "mixer", "seqgan", "quark", "es")                              # grpo_moi_b2.py (cùng thưởng bcmr)
THUONG_CU = ("spice", "cider", "bleu4", "rougel", "chrf", "meteor", "bertscore", "spider")
THUONG_B2 = ("bcmr",)                                                        # grpo_moi_b2.py, chỉ với --algo grpo
THUONG_MOI = ("spice_cong", "ten_loai", "loai")                              # thuong_moi.py
CO = {"beta": "--beta", "loss": "--loss-type", "scale": "--scale-rewards", "mu": "--mu", "lam": "--lam",
      "is": "--is-level", "eps": "--eps-high", "steps": "--max-steps", "G": "--G", "lr": "--lr",
      "dpo_beta": "--dpo-beta", "mrt_alpha": "--mrt-alpha", "spg_tau": "--spg-tau", "eps_low": "--eps-low",
      "ce_lam": "--ce-lam", "mixer_rho0": "--mixer-rho0", "mixer_frac": "--mixer-frac", "gan_mix": "--gan-mix",
      "gan_warm": "--gan-warm", "gan_lr": "--gan-lr", "quark_k": "--quark-k", "quark_pool": "--quark-pool",
      "es_pop": "--es-pop", "es_m": "--es-m", "es_sigma": "--es-sigma", "es_lr": "--es-lr", "es_save": "--es-save"}
CO_GL = {"beta", "steps", "G", "lr"}           # cờ mà grpo_luoi.py (và thuong_moi.py) nhận
CO_B1 = {"dpo_beta", "mrt_alpha", "spg_tau", "eps_low"}
CO_B2 = {"ce_lam": "rlce", "mixer_rho0": "mixer", "mixer_frac": "mixer", "gan_mix": "seqgan", "gan_warm": "seqgan",
         "gan_lr": "seqgan", "quark_k": "quark", "quark_pool": "quark", "es_pop": "es", "es_m": "es", "es_sigma": "es",
         "es_lr": "es", "es_save": "es"}
TEP_CAN = ("trainer_state.json", "optimizer.pt", "adapter_model.safetensors")


def phan_tich(luot):
    al, rw, sd, *x = luot.split(":")
    opt = dict(kv.split("=", 1) for kv in x[0].split(",")) if x and x[0] else {}
    assert set(opt) <= set(CO) | {"tag"}, f"cờ lạ trong {luot}: {set(opt) - set(CO) - {'tag'}}"
    assert not (set(opt) - {"tag"}) or "tag" in opt, f"đổi cấu hình thì phải có tag: {luot}"
    assert int(sd) > 0
    assert rw in THUONG_CU + THUONG_MOI + THUONG_B2, f"thưởng lạ: {rw}"
    assert al in CU + CD + B1 + PP + B2 + ("sft",), f"thuật toán lạ: {al}"
    assert rw not in THUONG_B2 or al == "grpo", f"bcmr chỉ đi với --algo grpo (grpo_moi_b2 assert): {luot}"
    sai_b2 = [k for k in opt if k in CO_B2 and CO_B2[k] != al]
    assert not sai_b2, f"cờ {sai_b2} không thuộc {al}: {luot}"
    assert "lam" not in opt or al in PP, f"lam chỉ cho ppo/a2c: {luot}"
    assert not (set(opt) & CO_B1) or al in B1, f"cờ của grpo_moi_b1 chỉ cho {B1}: {luot}"
    if rw in THUONG_MOI:
        assert al in CU and set(opt) - {"tag"} <= CO_GL, f"thưởng mới chạy qua thuong_moi → grpo_luoi: chỉ {CU}, cờ {CO_GL}"
    return al, rw, sd, opt


def tep_cua(luot):
    al, rw, sd, opt = phan_tich(luot)
    if rw in THUONG_MOI:
        return "thuong_moi.py"
    if al in PP:
        return "grpo_ppo.py"
    if al == "sft":
        return "sft_tiep.py"
    if al in B1:
        return "grpo_moi_b1.py"
    if al in B2 or rw in THUONG_B2:
        return "grpo_moi_b2.py"
    # đúng luật của make_nb.tep_cua
    return "grpo_codien.py" if al in CD or set(opt) - {"tag"} - CO_GL or (al != "grpo" and rw != "spice") else "grpo_luoi.py"


def tep_phu_thuoc(luot):
    """Các tệp phải có trong thư mục làm việc để script chạy được."""
    t = tep_cua(luot)
    can = ["grpo_luoi.py", "grpo_spice.py", "build_branch_data.py"]
    can += {"grpo_codien.py": ["grpo_codien.py"], "grpo_ppo.py": ["grpo_codien.py", "grpo_ppo.py"],
            "sft_tiep.py": ["sft_tiep.py"], "grpo_moi_b1.py": ["grpo_codien.py", "grpo_moi_b1.py"],
            "grpo_moi_b2.py": ["grpo_codien.py", "grpo_moi_b2.py"],
            "thuong_moi.py": ["thuong_moi.py", "metric_exec.py", "descriptors_ten.jsonl"]}.get(t, [])
    return can


def ten_thu_muc(luot, probe=False):
    al, rw, sd, opt = phan_tich(luot)
    tag = opt.get("tag")
    return f"{'probe_' if probe else ''}{al}_{rw}_{sd}{'_' + tag if tag else ''}"


def tong_buoc(luot, probe=False):
    return 20 if probe else int(phan_tich(luot)[3].get("steps", 500))


def dung_lenh(luot, bundle, merged, out, probe=False, keys=None, py="python", bs=4, accum=4, gen_chunk=8):
    al, rw, sd, opt = phan_tich(luot)
    cmd = [py, tep_cua(luot), "--probe" if probe else "--train", "--no-q4", "--bs", str(bs), "--accum", str(accum),
           "--gen-chunk", str(gen_chunk), "--algo", al, "--reward", rw, "--seed", sd,
           "--bundle", bundle, "--merged", merged, "--out", out, "--resume", "auto"]
    for k, v in opt.items():
        if k != "tag":
            cmd += [CO[k], v]
    if sd == "101" and not probe and keys:
        cmd += ["--keys-ck500", keys]
    return cmd


def buoc_cua(p):
    return int(p.rstrip("/").rsplit("-", 1)[1])


def tep_them(luot):
    """Tệp bắt buộc thêm trong điểm lưu (ghi SAU ba tệp chính, thiếu thì chạy tiếp sẽ assert hoặc mất trạng thái).
    Mục bắt đầu bằng '-' là tệp chính KHÔNG có ở thuật toán đó (ES không có optimizer)."""
    al = phan_tich(luot)[0]
    return {"ppo": ("value_head.pt",), "a2c": ("value_head.pt",), "seqgan": ("discriminator.pt",),
            "quark": ("quark_pool.json",), "es": ("es_state.json", "-optimizer.pt")}.get(al, ())


def can_cua(them=()):
    bo = {f[1:] for f in them if f.startswith("-")}
    return tuple(f for f in TEP_CAN if f not in bo) + tuple(f for f in them if not f.startswith("-"))


def diem_luu_du(d, them=(), on_dinh=0):
    """Điểm lưu đủ TEP_CAN + `them`; on_dinh > 0: mọi tệp đã yên ≥ on_dinh giây (Trainer còn đang ghi thì bỏ qua)."""
    now = time.time()

    def yen(p):
        if not on_dinh:
            return True
        m = [os.path.getmtime(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs]
        return bool(m) and now - max(m) >= on_dinh

    return sorted((p for p in glob.glob(os.path.join(d, "checkpoint-*"))
                   if os.path.isdir(p) and re.search(r"checkpoint-\d+$", p)
                   and all(os.path.exists(os.path.join(p, f)) for f in can_cua(them)) and yen(p)), key=buoc_cua)


def dong_bo_len(out, dr, giu=3, log_ten="train.log", them=(), on_dinh=60):
    """Chép điểm lưu đủ mà Drive chưa có. Chép sang `.tam_checkpoint-N` rồi os.rename ⇒ trên Drive không bao giờ có
    điểm lưu dở (FUSE chỉ đẩy tệp đã đóng). Giữ `giu` điểm lưu cuối trên Drive. Trả danh sách bước vừa chép."""
    os.makedirs(dr, exist_ok=True)
    co = {buoc_cua(p) for p in diem_luu_du(dr, them)}
    moi = []
    moc = max(co) if co else -1
    for p in diem_luu_du(out, them, on_dinh):
        n = buoc_cua(p)
        if n <= moc:           # đã có, hoặc cũ hơn bản mới nhất trên Drive (đã bị tỉa theo `giu`): không chép lại
            continue
        tam = os.path.join(dr, f".tam_checkpoint-{n}")
        shutil.rmtree(tam, ignore_errors=True)
        shutil.copytree(p, tam)
        dich = os.path.join(dr, f"checkpoint-{n}")
        shutil.rmtree(dich, ignore_errors=True)      # bản dở do lần trước mất máy giữa lúc đổi tên
        os.rename(tam, dich)
        moi.append(n)
    du = diem_luu_du(dr, them)
    for p in du[:-giu] if giu else []:
        shutil.rmtree(p, ignore_errors=True)
    for f in (log_ten, "prompt_keys.json", "log_history.json"):
        s = os.path.join(out, f)
        if os.path.exists(s):
            shutil.copyfile(s, os.path.join(dr, f + ".tam"))
            os.replace(os.path.join(dr, f + ".tam"), os.path.join(dr, f + (".drive" if f == log_ten else "")))
    return moi


def khoi_phuc(dr, out, them=()):
    """Máy mới: chép điểm lưu đủ mới nhất từ Drive về `out` nếu local chưa có bản mới hơn. Trả bước, hoặc 0."""
    os.makedirs(out, exist_ok=True)
    du = diem_luu_du(dr, them)
    if not du:
        return 0
    n = buoc_cua(du[-1])
    co = [buoc_cua(p) for p in diem_luu_du(out, them)]
    if not co or max(co) < n:
        shutil.copytree(du[-1], os.path.join(out, f"checkpoint-{n}"), dirs_exist_ok=True)
    if os.path.exists(os.path.join(dr, "train.log.drive")) and not os.path.exists(os.path.join(out, "train.log")):
        shutil.copyfile(os.path.join(dr, "train.log.drive"), os.path.join(out, "train.log"))   # giữ lịch sử log
    return max(n, max(co) if co else 0)


SO = re.compile(r"^[-\d.e+naif]+$")


def tien_do(log, tu=0):
    """Đọc train.log của lượt chạy NÀY: chỉ phần từ byte `tu` (cỡ log lúc bấm chạy) và sau dòng [tiếp từ] cuối."""
    L = []
    if os.path.exists(log):
        with open(log, encoding="utf-8", errors="ignore") as f:
            f.seek(tu)
            L = f.read().splitlines()
    i = max([k for k, l in enumerate(L) if l.startswith("[tiếp từ]")], default=-1)
    tiep = L[i] if i >= 0 else None
    goc = int(re.findall(r"checkpoint-(\d+)", tiep)[0]) if tiep and "checkpoint-" in tiep else 0
    D = []
    for l in L[i + 1:] if i >= 0 else L:
        if l.startswith("{'loss'") or l.startswith("{'reward'"):
            try:
                D.append({k: float(v) for k, v in ast.literal_eval(l).items() if SO.match(str(v))})
            except Exception:
                pass
    nap = [l for l in L[i + 1:] if l.startswith("[nạp default]")] if i >= 0 else []
    m = re.search(r"→\s*([\d.]+)", nap[-1]) if nap else None
    xong = [l for l in L if l.startswith("[xong]")]
    x = D[-10:]
    st_b = [d["step_time"] for d in x if "step_time" in d]
    return dict(goc=goc, buoc=goc + len(D), n_log=len(D), tiep=tiep, resume=bool(tiep and "checkpoint-" in tiep),
                nap_default=(float(m.group(1)) if m else None), xong=xong[-1] if xong else None,
                s_buoc=(st.mean(st_b) if st_b else None),
                thuong=(st.mean(d["reward"] for d in x if "reward" in d) if any("reward" in d for d in x) else None),
                kl=(st.mean(d["kl"] for d in x if "kl" in d) if any("kl" in d for d in x) else None),
                loi=any(("Traceback" in l or "OutOfMemory" in l or "CUDA out of memory" in l or "Killed" in l) for l in L[-80:]))


def kiem_nap_default(td):
    """Lượt chạy tiếp phải có dòng [nạp default] với |lora_B| sau > 0 (lỗi 30/9). Trả (đạt, lý do)."""
    if td["tiep"] is None:
        return None, "chưa thấy dòng [tiếp từ] (đang nạp mô hình)"
    if not td["resume"]:
        return True, "lượt mới (tiếp từ None), không cần nạp default"
    if td["nap_default"] is None:
        return None, "chưa thấy dòng [nạp default]"
    return td["nap_default"] > 0, f"|lora_B| sau = {td['nap_default']}"


def doc_tham_do(log, tu=0):
    """Dòng [xong] của chế độ --probe: '… s/bước · đỉnh VRAM x GiB …' → (s_buoc, vram)."""
    td = tien_do(log, tu)
    if not td["xong"]:
        return None, None
    s = re.search(r"([\d.]+) s/bước", td["xong"])
    v = re.search(r"đỉnh VRAM ([\d.]+) GiB", td["xong"])
    return (float(s.group(1)) if s else None), (float(v.group(1)) if v else None)


def chon_may(gpu, vram, s_buoc, s_buoc_a100=None, s_buoc_l4=None, tran_l4=17.0, ti_so=1.5):
    """Luật CLAUDE.md (5/9, nới 9/9): CPU → T4 → L4 → A100; L4 khi đỉnh VRAM ≤ ~17 GiB và giờ_L4/giờ_A100 ≤ 1,5."""
    g = (gpu or "").upper()
    if "L4" in g:
        s_buoc_l4 = s_buoc
    if "A100" in g:
        s_buoc_a100 = s_buoc
    if vram is not None and vram > tran_l4 and "A100" not in g:
        return "A100", f"đỉnh VRAM {vram:.1f} GiB > {tran_l4} GiB (biên 25% trên 22 GiB của L4)"
    if s_buoc_l4 and s_buoc_a100:
        r = s_buoc_l4 / s_buoc_a100
        return ("L4" if r <= ti_so else "A100"), f"giờ_L4/giờ_A100 = {r:.2f} ({'≤' if r <= ti_so else '>'} {ti_so})"
    if "L4" in g:
        return "L4", "chưa đo A100; L4 đủ VRAM ⇒ giữ L4 (chỉ lên A100 khi đo được tỉ số > 1,5)"
    if "A100" in g:
        return "?", "chỉ có số A100; chạy thăm dò trên L4 rồi so (luật: thử card rẻ trước)"
    return "L4", f"{gpu}: chạy thăm dò lại trên L4 trước khi chọn"


def chay(cmd, log, cwd, env=None):
    """start_new_session=True: bấm Stop một ô notebook không gửi SIGINT sang tiến trình train (luật Colab ①)."""
    tu = os.path.getsize(log) if os.path.exists(log) else 0
    f = open(log, "a")
    p = subprocess.Popen(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, env=env or os.environ.copy(),
                         start_new_session=True, text=True)
    p.tu_byte = tu      # theo_doi chỉ đọc phần log của lần chạy này
    return p


def gio_vn(t=None):
    return time.strftime("%d/%m %H:%M", time.gmtime((t or time.time()) + 7 * 3600))


def dung(p, cho=120):
    """Dừng nhẹ (SIGTERM cả nhóm tiến trình) để Trainer kịp thoát; quá `cho` giây thì SIGKILL."""
    if p.poll() is not None:
        return p.returncode
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        p.wait(cho)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        p.wait()
    return p.returncode


def theo_doi(p, out, dr, tong, t0, cat_gio=None, in_moi=120, dong_bo_moi=300, log_ten="train.log", inra=print,
             them=(), on_dinh=60):
    """Ô foreground suốt lượt (luật Colab ④). Nhật ký cuộn có mốc giờ VN, không clear_output, flush.
    Trả (mã thoát, td cuối, kiểm nạp default)."""
    log = os.path.join(out, log_ten)
    tu = getattr(p, "tu_byte", 0)
    t_db = time.time()
    da_kiem = False
    kq_nap = (True, "")
    while p.poll() is None:
        time.sleep(in_moi)
        td = tien_do(log, tu)
        con = (tong - td["buoc"]) * td["s_buoc"] / 3600 if td["s_buoc"] else None
        inra(f"{gio_vn()} VN · {(time.time() - t0) / 3600:5.2f} h · bước {td['buoc']}/{tong} (tiếp từ {td['goc']})"
             f" · {td['s_buoc'] or 0:.0f} s/bước · còn {'?' if con is None else f'{con:.1f} h'}"
             f" · thưởng {td['thuong'] if td['thuong'] is not None else float('nan'):.3f}"
             f" · kl {td['kl'] if td['kl'] is not None else float('nan'):.4f}"
             f" · Drive: {', '.join(os.path.basename(x) for x in diem_luu_du(dr, them)[-1:]) or 'chưa có'}", flush=True)
        if not da_kiem:
            kq_nap = kiem_nap_default(td)
            if kq_nap[0] is not None:
                da_kiem = True
                inra(f"   [kiểm nạp default] {'ĐẠT' if kq_nap[0] else '⛔ KHÔNG ĐẠT'} · {kq_nap[1]}", flush=True)
                if not kq_nap[0]:
                    inra("   ⛔ policy về lại S1 (lỗi 30/9) ⇒ dừng lượt", flush=True)
                    dung(p)
                    break
        if td["loi"]:
            inra("   ⚠️ Traceback/OOM ở cuối log", flush=True)
        if time.time() - t_db >= dong_bo_moi:
            moi = dong_bo_len(out, dr, log_ten=log_ten, them=them, on_dinh=on_dinh)
            if moi:
                inra(f"   [Drive] đã chép checkpoint-{moi}", flush=True)
            t_db = time.time()
        if cat_gio and time.time() - t0 > cat_gio * 3600:
            inra("   ⛔ chạm trần giờ đặt trước, dừng nhẹ", flush=True)
            dung(p)
    moi = dong_bo_len(out, dr, log_ten=log_ten, them=them, on_dinh=0)   # tiến trình đã thoát: không còn ai ghi
    td = tien_do(log, tu)
    inra(f"{gio_vn()} VN · KẾT THÚC · mã thoát {p.returncode} · bước {td['buoc']}/{tong} · Drive chép thêm {moi}", flush=True)
    return p.returncode, td, kq_nap


def nen(out, dich, giu_ck=1):
    """Zip thư mục kết quả (luật: ô cuối zip riêng thư mục kết quả). Giữ `giu_ck` điểm lưu cuối kèm optimizer
    (đủ để chạy tiếp), các điểm lưu cũ chỉ giữ adapter + trainer_state. Ghi sang tên tạm rồi đổi tên."""
    import zipfile
    du = diem_luu_du(out)
    giu = {os.path.basename(p) for p in du[-giu_ck:]} if giu_ck else set()
    tam = dich + ".tam"
    n = 0
    with zipfile.ZipFile(tam, "w", zipfile.ZIP_DEFLATED) as z:
        for r, _, fs in os.walk(out):
            for f in fs:
                p = os.path.join(r, f)
                rel = os.path.relpath(p, os.path.dirname(out))
                ck = next((x for x in rel.split(os.sep) if x.startswith("checkpoint-")), None)
                if ck and ck not in giu and f in ("optimizer.pt", "scheduler.pt", "rng_state.pth"):
                    continue
                z.write(p, rel)
                n += 1
    os.replace(tam, dich)
    return n


class TienTrinhCu:
    """Bọc một PID còn sống từ lần chạy ô trước (cùng máy ảo) để theo_doi dùng như Popen."""
    def __init__(self, pid, log):
        self.pid, self.returncode = pid, None
        self.tu_byte = 0
        self.log = log

    def poll(self):
        try:
            os.kill(self.pid, 0)
            return None
        except ProcessLookupError:
            self.returncode = self.returncode if self.returncode is not None else -999   # không biết mã thật
            return self.returncode

    def wait(self, timeout=None):
        t = time.time()
        while self.poll() is None:
            if timeout and time.time() - t > timeout:
                raise subprocess.TimeoutExpired("pid", timeout)
            time.sleep(2)
        return self.returncode


def tim_tien_trinh(out):
    """PID của tiến trình train đang ghi vào `out` (bấm Run all lại khi lượt cũ còn sống thì KHÔNG chạy bản thứ hai)."""
    r = subprocess.run(["pgrep", "-f", "--", f"--out {out} "], capture_output=True, text=True)
    me = os.getpid()
    return [int(x) for x in r.stdout.split() if int(x) != me]
