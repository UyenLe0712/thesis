# -*- coding: utf-8 -*-
"""Dựng lại ba thư mục upload của 288 từ repo + kiểm md5 (B.11 của 288, bản WSL).

    python3 _scripts/288/dung_lai_288.py            # chép + so md5 mọi tệp
    python3 _scripts/288/dung_lai_288.py --kiem     # chỉ so, không ghi

Khác bản gốc (máy Mac): 11 script KHÔNG còn tách từ file bàn giao mà nằm sẵn trong `_scripts/` của repo
(viết lại 6/10/2026 từ bản mô tả Phụ lục B) ⇒ md5 của chúng khác bản gốc; bảng MA dưới đây là md5 bản
viết lại, các ô notebook trong harness/runbook/288_ACTION_NGUOI_NGHE_CLICK_6_10.md dùng đúng bảng này.
Tệp chép từ repo và dữ liệu G0 giữ nguyên md5 của bản gốc.
"""
import argparse, glob, hashlib, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
S = os.path.join(REPO, "_scripts")

# md5 bản viết lại (6/10/2026) — đổi một byte là phải cập nhật cả bảng này lẫn các ô notebook
MA = {
    "288/g0_som_build.py": "155d813a59a0660222330e54ed2fdbb7",
    "288/g0/g0_listener.py": "41662b4cdbd38f3c4f0c1c98948ed165",
    "288/g0/g0_doc.py": "e312f4b479469274ecce2f2ef03bc064",
    "288/nghe/grpo_nghe.py": "f08f42b04b0b9f7b943b960877f7936f",
    "288/nghe/nghe_server.py": "f81cdf27c723f132c918619943149921",
    "288/cham/gieo_tho.py": "7681cc68ad7e0bc9965c73f47ea3aa88",
    "288/cham/val_lon.py": "d2854d13af1c924f44bf2dcb343ae8ca",
    "288/doc_288.py": "2fe67533f939fd52279de3f97514fad0",
    "doc_286.py": "96da21e03bb9046d10dd08cdb7f45090",
    "289/doc_289.py": "12c7836d6b7d2c3fd2a74e16881c5b44",
}
CHEP = [  # (nguồn trong repo, [đích trong _scripts], md5)
    ("harness/som_listener.py", ["288/g0/som_listener.py", "288/nghe/som_listener.py"], "c61ef769e4f1993a7cad3a536e9ca277"),
    ("harness/som_build.py", ["288/g0/som_build.py", "288/nghe/som_build.py"], "2b7d257fccd7378586527b8a65d8b770"),
    ("harness/grpo_spice.py", ["288/nghe/grpo_spice.py", "288/cham/grpo_spice.py"], "07ea87b6d156d1faa391a4274dffd7cf"),
    ("harness/build_branch_data.py", ["288/nghe/build_branch_data.py", "288/cham/build_branch_data.py"], "619e63e123a6dbf60086e65ee94a3912"),
    ("harness/gen_test_grpo.py", ["288/cham/gen_test_grpo.py"], "b18ec1aa3fd037ddffb9411db63c2a3f"),
    ("runs/preds_s1_seed101.jsonl", ["288/cham/preds_s1_seed101.jsonl"], "bc8911912491bb97fd987b3c91a22bda"),
    ("runs/score_s1_seed101_raw.jsonl", ["288/cham/score_s1_seed101_raw.jsonl"], "0681d937d930c952b7ff92e0f24d5189"),
    ("runs/grpo_spice/score_ck500_test_raw.jsonl", ["288/cham/score_ck500_test_raw.jsonl"], "5b9d6d65cb0d2390b126d22463f888ee"),
    ("runs/grpo_spice/pred_ck500_test.jsonl", ["288/cham/pred_ck500_test.jsonl"], "328847ac96fa3104f76cd997f4091bcd"),
    ("runs/venus/preds_venus_s1_2532.jsonl", ["288/cham/preds_venus_s1_2532.jsonl"], "e715a46693f8e6a588d23816a5f75430"),
    ("runs/venus/score_venus_s1_2532_raw.jsonl", ["288/cham/score_venus_s1_2532_raw.jsonl"], "b19b4e834201c8fb22925694dc7bf0a7"),
    ("runs/grpo_spice/score_ck500_raw.jsonl", ["288/cham/score_ck500_c1_raw.jsonl"], "258ced11cad3b6729bbdb25f947dbe78"),
    ("runs/grpo_spice/score_k0_lai500_raw.jsonl", ["288/cham/score_s1_c1_raw.jsonl"], "1c8dbcd5f49ec53ecc655b4b4d2c04c4"),
    ("runs/grpo_spice/pred_ck500.jsonl", ["288/cham/pred_ck500_c1.jsonl"], "eb6162d86730a936beb5ae5a9fd6d652"),
]
MD5_PK, MD5_PV5, MD5_SR = "4bf30d816dc531842495535828dcbb43", "34fa2cf897721fe3155f5d917feb7856", "9100844734d00e4f1851954d25a86220"
G0 = {"288/g0/g0_som.jsonl": "a49789bda073f5629380ad907db31910", "288/g0/g0_cau.jsonl": "656dd46f40bcc2d2f32a84e1c752fe6f"}


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kiem", action="store_true")
    a = ap.parse_args()
    loi, n_ok = [], 0

    def bao(ten, p, h):
        nonlocal n_ok
        if not os.path.exists(p):
            loi.append(f"thiếu {ten}"); print(f"⛔ thiếu {ten}")
        elif h and md5(p) != h:
            loi.append(f"lệch {ten}"); print(f"⛔ lệch md5 {ten}: {md5(p)} ≠ {h}")
        else:
            n_ok += 1

    print("[1] mã viết lại trong _scripts/")
    for f, h in MA.items():
        bao(f, os.path.join(S, f), h)
    print("[2] tệp chép từ repo")
    for src, dsts, h in CHEP:
        for d in dsts:
            p = os.path.join(S, d)
            if not a.kiem:
                os.makedirs(os.path.dirname(p), exist_ok=True); shutil.copy(os.path.join(REPO, src), p)
            bao(d, p, h)
    print("[3] tệp sinh ra")
    hv = os.path.join(S, "288", "cham", "harness_venus")
    if not a.kiem:
        os.makedirs(hv, exist_ok=True)
        for p in glob.glob(os.path.join(REPO, "harness", "*.py")) + glob.glob(os.path.join(REPO, "harness", "*.yaml")):
            shutil.copy(p, hv)
    bao("cham/harness_venus/score_run.py", os.path.join(hv, "score_run.py"), MD5_SR)
    pk = os.path.join(S, "288", "nghe", "prompt_keys_ck500.json")
    if not a.kiem:
        open(pk, "w").write(json.dumps(json.load(open(os.path.join(REPO, "runs", "ctg", "p0", "p0_a3", "prompt_keys.json")))[:1000]))
    bao("nghe/prompt_keys_ck500.json", pk, MD5_PK)
    pv = os.path.join(S, "288", "cham", "preds_venus_ck500_2532.jsonl")
    if not a.kiem:
        C = {(d["episode_id"], d["step_id"]): d["pred"] for d in map(json.loads, open(
            os.path.join(REPO, "runs", "grpo_spice", "pred_ck500_test.jsonl"), encoding="utf-8"))}
        khac = 0
        with open(pv, "w", encoding="utf-8") as f:
            for d in map(json.loads, open(os.path.join(REPO, "runs", "venus", "preds_venus_s1_2532.jsonl"), encoding="utf-8")):
                c = C[(d["episode_id"], d["step_id"])]
                khac += c != d["pred"]
                f.write(json.dumps({**d, "raw": c, "pred": c}, ensure_ascii=False) + "\n")
        print(f"    preds_venus_ck500_2532.jsonl: {khac} câu khác S1")
    bao("cham/preds_venus_ck500_2532.jsonl", pv, MD5_PV5)
    print("[4] dữ liệu G0")
    for f, h in G0.items():
        if not os.path.exists(os.path.join(S, f)):
            print(f"⛔ thiếu {f} — chạy: ~/.venvs/thesis/bin/python _scripts/288/g0_som_build.py "
                  "(cần all_forest_dict.zip của HarrytheOrange/parsed_AndroidControl)")
        bao(f, os.path.join(S, f), h)
    for p in glob.glob(os.path.join(S, "**", "__pycache__"), recursive=True):
        shutil.rmtree(p, ignore_errors=True)
    print(f"{'✅ ĐỦ, mọi md5 khớp' if not loi else '⛔ CHƯA ĐỦ: ' + '; '.join(loi)} ({n_ok} tệp đạt)")
    sys.exit(1 if loi else 0)


if __name__ == "__main__":
    main()
