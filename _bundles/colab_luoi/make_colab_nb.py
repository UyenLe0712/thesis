# -*- coding: utf-8 -*-
"""Dựng colab_luoi_train.ipynb: notebook Colab train MỘT lượt bất kỳ của lưới RL, chọn bằng biến LUOT ở ô 1.

  python make_colab_nb.py [tài khoản kaggle chứa dữ liệu, mặc định uyenle0712]

md5 của script nhúng vào notebook lấy từ bản trên máy nhà: _bundles/luoi/ds_<tk> (grpo_luoi, grpo_spice, build_branch_data,
prompt_keys) và _bundles/luoi/kit_<tk> (các tệp còn lại). Kit hay dataset script đổi thì DỰNG LẠI notebook này, nếu không
ô 4 dừng ở bước kiểm md5 (cố ý). Logic (colab_logic.py) nhúng nguyên văn vào ô 2 nên notebook tự chứa.
"""
import os, sys, json, hashlib

TK = sys.argv[1] if len(sys.argv) > 1 else "uyenle0712"
H = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(H, "..", "luoi")
DS = os.path.join(L, {"uyenle0712": "ds_uyenle", "trangphngngc": "ds_trang", "trangphuongngoc": "ds_trang2"}[TK])
KIT = os.path.join(L, f"kit_{TK}")
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
MD5 = {f: md5(os.path.join(DS, f)) for f in ("grpo_luoi.py", "grpo_spice.py", "build_branch_data.py", "prompt_keys_ck500.json")}
MD5.update({f: md5(os.path.join(KIT, f)) for f in ("grpo_codien.py", "grpo_ppo.py", "sft_tiep.py", "grpo_moi_b1.py",
                                                   "grpo_moi_b2.py", "thuong_moi.py", "metric_exec.py", "descriptors_ten.jsonl")})
LOGIC = open(os.path.join(H, "colab_logic.py"), encoding="utf-8").read()
assert "'''" not in LOGIC

MD0 = f"""# Train một lượt lưới RL trên Colab (bản dựng từ `_bundles/colab_luoi/make_colab_nb.py`, dữ liệu của `{TK}`)

Dành cho lượt dài mà Kaggle phải nối nhiều commit, ví dụ PPO 1.000 bước (khoảng 41 h trên T4 [suy, probe 3/11]), GSPO 1.000 bước, DPO.
Cùng script, cùng tên thư mục ra như notebook Kaggle (`make_nb.py`), nên điểm lưu hai bên dùng chung được.

**Cách chạy**
1. Sửa ô 1: `LUOT` (cú pháp `algo:reward:seed[:k=v,...,tag=...]`) và `CHE_DO`.
2. Lần đầu với một lượt: `CHE_DO = "tham_do"` trên **L4** → Run all (khoảng 30–60 phút). Ô 5 in s/bước, đỉnh VRAM trên 50 câu nhắc dài nhất và khuyến nghị máy.
   Muốn so với A100 thì đổi máy, chạy thăm dò lại; kết quả hai lần lưu trên Drive và ô 5 tự tính tỉ số. Luật: tỉ số giờ L4/A100 ≤ 1,5 thì dùng L4.
3. Đổi `CHE_DO = "train"` → Run all. Ô 6 chạy foreground suốt lượt: giữ tab mở, đừng bấm Stop. Stop cũng không giết tiến trình train (`start_new_session=True`),
   nhưng ô theo dõi mất thì Colab ngắt máy sau khoảng 90 phút không tương tác.
4. **Mất máy:** bật lại đúng máy cũ, Run all. Ô 6 chép điểm lưu mới nhất từ Drive về rồi chạy tiếp, và kiểm dòng `[nạp default] … → x>0`.
   Nếu tiến trình cũ còn sống (nhân Python restart nhưng máy chưa mất), ô 6 chỉ theo dõi tiếp, không chạy bản thứ hai.
5. Xong: ô 7 zip kết quả lên `MyDrive/thesis/luoi_colab/<lượt>/`. Tải zip đó về, đặt vào `runs/luoi/<đợt>/`.

Điểm lưu: mỗi 25 bước (mặc định của script); đồng bộ lên Drive mỗi 5 phút bằng chép sang tên tạm rồi đổi tên; Drive giữ 3 điểm lưu cuối.
Khoá Kaggle chỉ ghi vào `/root/.kaggle`, không in, không lưu vào Drive hay notebook. Đặt sẵn ở Colab Secrets tên `KAGGLE_TOKEN` cho khỏi gõ.
"""
C1 = '''# Ô 1. Cấu hình — chỉ sửa ô này
LUOT = "ppo:spice:101:mu=2,lam=1.0,steps=1000,tag=l1"   # ví dụ khác: "gspo:spice:101:steps=1000,tag=s1000" · "dpo_on:spice:101" · "grpo:spice_cong:101" · "seqgan:spice:101" · "grpo:bcmr:101" · "es:spice:101:es_sigma=0.002,tag=s2"
CHE_DO = "tham_do"            # "tham_do" (20 bước trên 50 câu nhắc dài nhất, không lưu) hoặc "train"
CAT_GIO = None                # trần giờ của phiên (None = chạy tới hết); chạm trần thì dừng nhẹ và điểm lưu cuối đã lên Drive
TK = "%s"              # tài khoản Kaggle chứa dữ liệu (fgrb-p1-bundle, grpo-luoi-script, luoi-kit)
DRIVE_GOC = "/content/drive/MyDrive/thesis/luoi_colab"
''' % TK
C2 = "# Ô 2. Logic (nhúng từ colab_logic.py) + kiểm cấu hình, chưa cài gì\nimport os, sys, time\nT0 = time.time()\nW = '/content/w'; os.makedirs(W, exist_ok=True)\nopen(f'{W}/colab_logic.py', 'w', encoding='utf-8').write('''" + LOGIC.replace("\\", "\\\\") + "''')\nsys.path.insert(0, W)\nimport importlib, colab_logic as C\nimportlib.reload(C)\n" + '''assert CHE_DO in ("tham_do", "train"), CHE_DO
PROBE = CHE_DO == "tham_do"
al, rw, sd, opt = C.phan_tich(LUOT)
TEN = C.ten_thu_muc(LUOT, probe=PROBE)
TONG = C.tong_buoc(LUOT, probe=PROBE)
CAN = C.tep_phu_thuoc(LUOT)
print(f"lượt {LUOT} · script {C.tep_cua(LUOT)} · thư mục {TEN} · {TONG} bước · cần {CAN}", flush=True)
if al in ("gspo",) and "steps" not in opt:
    print("⚠️ gspo ép μ=2: muốn đi qua đủ 1.000 câu nhắc như ck500 thì đặt steps=1000", flush=True)
'''
C3 = '''# Ô 3. Môi trường (khoảng 5 phút)
import subprocess
from google.colab import drive
drive.mount("/content/drive")
os.makedirs(DRIVE_GOC, exist_ok=True)
def sh(c, duoi=1500):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-duoi:], flush=True); return r.returncode
GPU = subprocess.run("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader", shell=True, capture_output=True, text=True).stdout.strip()
print("GPU:", GPU, flush=True); assert GPU, "DUNG: chua bat GPU"
if "T4" in GPU:
    print("⚠️ T4 chạy fp16 như Kaggle; L4/A100 chạy bf16 nên số có thể lệch nhẹ so với lượt Kaggle cùng tên, phải khai khi báo", flush=True)
sh("apt-get -qq update && apt-get -qq install -y openjdk-8-jre-headless")
sh("update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java")
assert "1.8" in subprocess.run("java -version", shell=True, capture_output=True, text=True).stderr, "DUNG: SPICE can Java 8"
sh(f"{sys.executable} -m pip install -q 'transformers==5.20.2' 'peft==0.21.2' 'trl==0.29.1' accelerate bitsandbytes 'kaggle==2.2.4' "
   f"pycocoevalcap sacrebleu scipy{' bert_score' if rw == 'bertscore' else ''} 2>&1 | tail -3")
sh(f"{sys.executable} -m pip uninstall -y torchao 2>&1 | tail -1")
assert sh(f"""{sys.executable} -c "import trl, transformers, peft, torch; print(trl.__version__, transformers.__version__, peft.__version__, torch.__version__, torch.cuda.get_device_name(0)); assert (trl.__version__, transformers.__version__, peft.__version__) == ('0.29.1', '5.20.2', '0.21.2'), 'lech phien ban'" """) == 0, "DUNG: moi truong loi"
print("✅ môi trường", flush=True)
'''
C4 = '''# Ô 4. Dữ liệu + kiểm md5 + tự kiểm + hoà S1 (khoảng 15 phút; hoà xong thì lần sau bỏ qua nếu máy chưa mất)
import getpass, stat, glob, shutil, hashlib, json, importlib.util
KD = "/root/.kaggle"; os.makedirs(KD, exist_ok=True); TKF = f"{KD}/access_token"
if not os.path.exists(TKF):
    tok = None
    try:
        from google.colab import userdata
        tok = userdata.get("KAGGLE_TOKEN")
    except Exception:
        pass
    tok = tok or getpass.getpass(f"Khoa Kaggle cua {TK} (KGAT_...): ")
    with open(TKF, "w") as f: f.write(tok.strip())
    os.chmod(TKF, stat.S_IRUSR | stat.S_IWUSR); del tok
ENV_K = {**os.environ, "KAGGLE_CONFIG_DIR": KD, "KAGGLE_API_TOKEN": TKF}
def tai(ds, dich):
    if os.path.exists(dich + "/.xong"): print("đã có", ds, flush=True); return
    os.makedirs(dich, exist_ok=True); t = time.time()
    r = subprocess.run(["kaggle", "datasets", "download", ds, "-p", dich, "--unzip"], env=ENV_K, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-300:], flush=True); assert r.returncode == 0, f"DUNG: khong tai duoc {ds}"
    for z in glob.glob(dich + "/*.zip"):
        d = z[:-4]; os.makedirs(d, exist_ok=True); shutil.unpack_archive(z, d); os.remove(z)
    open(dich + "/.xong", "w").close(); print(f"tải {ds} · {(time.time()-t)/60:.1f} phút", flush=True)
D = "/content/ds"
tai(f"{TK}/grpo-luoi-script", f"{D}/script")
tai(f"{TK}/luoi-kit", f"{D}/kit")
tai(f"{TK}/fgrb-p1-bundle", f"{D}/bundle")                  # khoảng 2,7 GB
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BUNDLE = next(r for r, d, f in os.walk(f"{D}/bundle") if "adapter_s1_seed101" in d and "images" in d)
assert md5(f"{BUNDLE}/adapter_s1_seed101/adapter_model.safetensors") == "0c60a4418d54eaf27bf1d27b895538b7", "DUNG: adapter S1 lech"
MD5 = %r
def nguon(f):
    k = glob.glob(f"{D}/script/**/{f}", recursive=True) + glob.glob(f"{D}/kit/**/{f}", recursive=True)
    assert len(k) >= 1, f"DUNG: thieu {f}"
    return k[0]
for f in CAN:
    shutil.copy(nguon(f), f"{W}/{f}")
    assert md5(f"{W}/{f}") == MD5[f], f"DUNG: {f} lech ban da kiem (kit/script doi thi dung lai notebook bang make_colab_nb.py)"
KEYS = nguon("prompt_keys_ck500.json"); assert md5(KEYS) == MD5["prompt_keys_ck500.json"]
SPL = list(importlib.util.find_spec("pycocoevalcap").submodule_search_locations)[0] + "/spice/lib"
for j, sz in {"stanford-corenlp-3.6.0.jar": 7270741, "stanford-corenlp-3.6.0-models.jar": 378116526}.items():
    if not (os.path.exists(f"{SPL}/{j}") and os.path.getsize(f"{SPL}/{j}") == sz):
        shutil.copy(nguon(j), f"{SPL}/{j}")
    assert os.path.getsize(f"{SPL}/{j}") == sz, f"DUNG: {j} sai kich thuoc"
def py(*a):
    r = subprocess.run([sys.executable, *a], cwd=W, capture_output=True, text=True)
    print((r.stdout + r.stderr)[-1200:], flush=True); return r.returncode
assert py("grpo_luoi.py", "--selftest-algo") == 0, "DUNG: selftest algo"
for f, co in (("grpo_codien.py", "--selftest-algo"), ("grpo_ppo.py", "--selftest-algo"), ("grpo_moi_b1.py", "--selftest-algo"),
              ("grpo_moi_b2.py", "--selftest-algo")):
    if f in CAN:
        assert py(f, co) == 0, f"DUNG: selftest {f}"
if "thuong_moi.py" in CAN:
    assert py("thuong_moi.py", "--selftest-moi", "--bundle", W) == 0, "DUNG: selftest thuong moi"
else:
    assert py("grpo_moi_b2.py" if rw == "bcmr" else "grpo_luoi.py", "--selftest-thuong", "--bundle", BUNDLE, "--rewards", rw) == 0, "DUNG: selftest thuong"
MERGED = "/content/s1_merged"
if not os.path.exists(f"{MERGED}/config.json"):
    assert py("grpo_spice.py", "--merge", "--bundle", BUNDLE, "--merged", MERGED) == 0, "DUNG: hoa loi"
print(f"✅ dữ liệu · BUNDLE {BUNDLE} · {(time.time()-T0)/60:.0f} phút từ đầu", flush=True)
''' % MD5
C5 = '''# Ô 5. Thăm dò (chỉ khi CHE_DO = "tham_do"): 20 bước trên 50 câu nhắc dài nhất ⇒ s/bước, đỉnh VRAM, chọn máy
THEM = C.tep_them(LUOT)          # tệp riêng của điểm lưu: value_head.pt (PPO/A2C) · discriminator.pt · quark_pool.json · es_state.json (ES không có optimizer)
ENV = {**os.environ, "CUDA_VISIBLE_DEVICES": "0", "TQDM_DISABLE": "1", "HF_HUB_DISABLE_PROGRESS_BARS": "1", "PYTHONUNBUFFERED": "1",
       "PYTORCH_ALLOC_CONF": "expandable_segments:True", "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
TD_JSON = f"{DRIVE_GOC}/tham_do_{C.ten_thu_muc(LUOT)}.json"
if PROBE:
    OUT = f"{W}/{TEN}"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    p = C.chay(C.dung_lenh(LUOT, BUNDLE, MERGED, OUT, probe=True, py=sys.executable), f"{OUT}/train.log", W, ENV)
    rc, td, _ = C.theo_doi(p, OUT, f"{DRIVE_GOC}/{TEN}", TONG, T0, in_moi=60, dong_bo_moi=300, them=THEM)
    s, v = C.doc_tham_do(f"{OUT}/train.log", p.tu_byte)
    if rc != 0 or s is None:
        print(open(f"{OUT}/train.log", errors="ignore").read()[-3000:], flush=True)
        raise SystemExit("DUNG: tham do loi (OOM thi doc dinh VRAM o tren; L4 tran thi chay lai tren A100)")
    D_TD = json.load(open(TD_JSON)) if os.path.exists(TD_JSON) else {}
    D_TD[GPU.split(",")[0]] = dict(s_buoc=s, vram=v, luc=C.gio_vn())
    json.dump(D_TD, open(TD_JSON + ".tam", "w"), ensure_ascii=False, indent=1); os.replace(TD_JSON + ".tam", TD_JSON)
    sa = next((x["s_buoc"] for g, x in D_TD.items() if "A100" in g), None)
    sl = next((x["s_buoc"] for g, x in D_TD.items() if "L4" in g), None)
    may, ly_do = C.chon_may(GPU, v, s, s_buoc_a100=sa, s_buoc_l4=sl)
    tong = C.tong_buoc(LUOT)
    print(f"\\n===== THĂM DÒ {LUOT} trên {GPU}: {s:.1f} s/bước · đỉnh VRAM {v:.2f} GiB", flush=True)
    print(f"   {tong} bước ≈ {tong * s / 3600:.1f} h máy này [suy: s/bước đo trên câu nhắc DÀI NHẤT nên là cận trên]", flush=True)
    print(f"   các máy đã đo: {D_TD}", flush=True)
    print(f"   ⇒ khuyến nghị: {may} · {ly_do}", flush=True)
    print("   Đơn vị Colab = giờ × đơn vị/giờ đang hiện ở Colab lúc chạy (giá phải đọc tại chỗ, đừng nhớ).", flush=True)
else:
    print("bỏ qua thăm dò (CHE_DO = train) · đã đo:", json.load(open(TD_JSON)) if os.path.exists(TD_JSON) else "chưa có", flush=True)
'''
C6 = '''# Ô 6. Train (chỉ khi CHE_DO = "train") — FOREGROUND suốt lượt, đừng bấm Stop, giữ tab mở
if not PROBE:
    OUT, DR = f"{W}/{TEN}", f"{DRIVE_GOC}/{TEN}"
    os.makedirs(DR, exist_ok=True)
    if os.path.exists(f"{DR}/final/adapter_model.safetensors"):
        print(f"✅ lượt đã xong từ trước: {DR}/final — không chạy lại", flush=True)
    else:
        cu = C.tim_tien_trinh(OUT)
        if cu:
            print(f"⚠️ tiến trình train cũ còn sống (pid {cu}) ⇒ chỉ theo dõi tiếp, KHÔNG chạy bản thứ hai", flush=True)
            p = C.TienTrinhCu(cu[0], f"{OUT}/train.log")
        else:
            n = C.khoi_phuc(DR, OUT, THEM)
            print(f"khôi phục từ Drive: {'checkpoint-' + str(n) if n else 'không có, chạy từ đầu'} · Drive có {[os.path.basename(x) for x in C.diem_luu_du(DR, THEM)]}", flush=True)
            cmd = C.dung_lenh(LUOT, BUNDLE, MERGED, OUT, keys=KEYS, py=sys.executable)
            print("lệnh:", " ".join(cmd), flush=True)
            p = C.chay(cmd, f"{OUT}/train.log", W, ENV)
        rc, td, nap = C.theo_doi(p, OUT, DR, TONG, T0, cat_gio=CAT_GIO, in_moi=120, dong_bo_moi=300, them=THEM)
        print("\\n".join(l for l in open(f"{OUT}/train.log", errors="ignore").read().splitlines()[-25:]
                        if not l.startswith(("PTB", "Parsing", "Threads", "Loading"))), flush=True)
        if os.path.exists(f"{OUT}/final/adapter_model.safetensors"):
            shutil.rmtree(f"{DR}/.tam_final", ignore_errors=True)
            shutil.copytree(f"{OUT}/final", f"{DR}/.tam_final"); shutil.rmtree(f"{DR}/final", ignore_errors=True)
            os.rename(f"{DR}/.tam_final", f"{DR}/final")
            print(f"✅ XONG {LUOT} · {td['buoc']}/{TONG} bước · final đã lên Drive", flush=True)
        else:
            print(f"⏸ chưa xong ({td['buoc']}/{TONG}, mã {rc}, kiểm nạp {nap}) · điểm lưu cuối trên Drive: "
                  f"{[os.path.basename(x) for x in C.diem_luu_du(DR, THEM)][-1:]} · Run all lại để chạy tiếp", flush=True)
'''
C7 = '''# Ô 7. Zip kết quả lên Drive (giữ optimizer của điểm lưu cuối để còn chạy tiếp)
OUT, DR = f"{W}/{TEN}", f"{DRIVE_GOC}/{TEN}"
if os.path.isdir(OUT):
    z = f"/content/{TEN}_ket_qua.zip"
    n = C.nen(OUT, z, giu_ck=1)
    os.makedirs(DR, exist_ok=True)
    shutil.copyfile(z, f"{DR}/{TEN}_ket_qua.zip.tam"); os.replace(f"{DR}/{TEN}_ket_qua.zip.tam", f"{DR}/{TEN}_ket_qua.zip")
    print(f"✅ {n} tệp · {os.path.getsize(z)/2**20:.0f} MB → {DR}/{TEN}_ket_qua.zip", flush=True)
'''

code = lambda s: {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.splitlines(True)}
md = lambda s: {"cell_type": "markdown", "metadata": {}, "source": s.splitlines(True)}
nb = {"cells": [md(MD0), code(C1), code(C2), code(C3), code(C4), code(C5), code(C6), code(C7)],
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                   "accelerator": "GPU", "colab": {"provenance": []}}, "nbformat": 4, "nbformat_minor": 5}
p = os.path.join(H, "colab_luoi_train.ipynb")
json.dump(nb, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("đã dựng", p, "· tài khoản", TK, "· md5", {k: v[:8] for k, v in MD5.items()})
