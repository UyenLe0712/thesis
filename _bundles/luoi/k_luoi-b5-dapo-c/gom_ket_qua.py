# Gom điểm lưu mới nhất + log train DAPO thành /kaggle/working/ket_qua_train.zip (chạy trên máy Colab qua colab exec)
import glob, os, zipfile
R = "/kaggle/working/dapo_ds_spice_101_dapo"
c = sorted(glob.glob(f"{R}/checkpoint-*"), key=lambda s: int(s.rsplit("-", 1)[1]))
print("diem luu:", [os.path.basename(x) for x in c], flush=True)
with zipfile.ZipFile("/kaggle/working/ket_qua_train.zip", "w", zipfile.ZIP_DEFLATED) as z:
    if c:
        for f in glob.glob(f"{c[-1]}/**/*", recursive=True):
            if os.path.isfile(f): z.write(f, os.path.relpath(f, "/kaggle/working"))
    for f in [f"{R}/train.log"] + glob.glob(f"{R}/*.json*"):
        if os.path.isfile(f): z.write(f, os.path.relpath(f, "/kaggle/working"))
print("zip", os.path.getsize("/kaggle/working/ket_qua_train.zip") // 2**20, "MB", flush=True)
