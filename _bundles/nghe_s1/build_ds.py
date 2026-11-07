"""Dựng dataset nhỏ `nghe-s1-kit` cho lượt probe "người nghe Phi-4 từ S1" (report/330 §7 hàng 7).

    python3 -I build_ds.py [tài khoản kaggle, mặc định trangphuongngoc]
    → ds_<tài khoản>/ (8 tệp chép NGUYÊN VĂN từ _scripts/288/nghe/, kiểm md5) + dataset-metadata.json
    rồi:  kg trang2 datasets create -p ds_trangphuongngoc        (lần đầu)
          kg trang2 datasets version -p ds_trangphuongngoc -m "..."  (khi đổi tệp)

Không chép jar SPICE: notebook lấy jar từ dataset `<tài khoản>/grpo-luoi-script` đã có của lưới.
Ảnh màn train + adapter S1 lấy từ `<tài khoản>/fgrb-p1-bundle` (đã có trên cả ba tài khoản).
"""
import hashlib, json, os, shutil, sys

U = sys.argv[1] if len(sys.argv) > 1 else "trangphuongngoc"
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(H, "..", "..", "_scripts", "288", "nghe")
MD5 = {   # md5 bản 288 (runbook 288 Ô C2) — chép nguyên văn, không sửa
    "grpo_nghe.py": "f08f42b04b0b9f7b943b960877f7936f",
    "grpo_spice.py": "07ea87b6d156d1faa391a4274dffd7cf",
    "build_branch_data.py": "619e63e123a6dbf60086e65ee94a3912",
    "nghe_server.py": "f81cdf27c723f132c918619943149921",
    "som_listener.py": "c61ef769e4f1993a7cad3a536e9ca277",
    "som_build.py": "2b7d257fccd7378586527b8a65d8b770",
    "prompt_keys_ck500.json": "4bf30d816dc531842495535828dcbb43",
    "bang_nghe.json": "212dfc30b6f7356b524a7d8d436ed2b3",
}
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
d = os.path.join(H, f"ds_{U}")
os.makedirs(d, exist_ok=True)
for f, h in MD5.items():
    shutil.copy(os.path.join(SRC, f), d)
    assert md5(os.path.join(d, f)) == h, f"DỪNG: {f} lệch md5 bản 288 ({md5(os.path.join(d, f))})"
json.dump({"title": "nghe-s1-kit", "id": f"{U}/nghe-s1-kit", "licenses": [{"name": "CC0-1.0"}]},
          open(os.path.join(d, "dataset-metadata.json"), "w"))
print("đã dựng", d, "·", len(MD5), "tệp, md5 khớp bản 288")
