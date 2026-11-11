# -*- coding: utf-8 -*-
"""SA-SPICE-v3 PREFLIGHT: input manifest (§2bis, ACTION §5.1) + bảng cỡ mẫu audit verifier (§5).

Tree hash: sắp theo đường dẫn tương đối POSIX (bytewise), SHA256 của các dòng "path<TAB>sha256(file)<LF>".
Chỉ đọc, không gọi GPU. Ghi một tệp JSON.

  ~/.venvs/thesis/bin/python harness/sa3_manifest.py --out runs/sa_spice_v3/preflight/input_manifest.json
"""
import os, sys, json, glob, hashlib, platform, subprocess, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HF = os.path.expanduser("~/.cache/huggingface/hub")


def fsha(p, n=1 << 22):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(n), b""):
            h.update(b)
    return h.hexdigest()


def tree(d, skip=(".git", "__pycache__", ".no_exist")):
    if not os.path.isdir(d):
        return {"path": d, "MISSING": True}
    rows, size = [], 0
    for dp, dn, fn in os.walk(d, followlinks=True):
        dn[:] = [x for x in dn if x not in skip]
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, d).replace(os.sep, "/")
            rows.append((rel.encode("utf-8"), fsha(p)))
            size += os.path.getsize(p)
    rows.sort()
    h = hashlib.sha256("".join(f"{r.decode()}\t{s}\n" for r, s in rows).encode("utf-8")).hexdigest()
    return {"path": d, "files": len(rows), "bytes": size, "tree_sha256": h}


def file_(p):
    if not os.path.exists(p):
        return {"path": p, "MISSING": True}
    return {"path": p, "bytes": os.path.getsize(p), "sha256": fsha(p)}


def snap(repo):
    s = sorted(glob.glob(os.path.join(HF, "models--" + repo.replace("/", "--"), "snapshots", "*")))
    if not s:
        return {"repo": repo, "MISSING": True}
    t = tree(s[-1]); t["repo"] = repo; t["revision"] = os.path.basename(s[-1])
    return t


def cp_lower(k, n, a=0.05):
    from scipy.stats import beta
    return 0.0 if k == 0 else float(beta.ppf(a, k, n - k + 1))


def cp_upper(k, n, a=0.05):
    from scipy.stats import beta
    return 1.0 if k == n else float(beta.ppf(1 - a, k + 1, n - k))


def n_min(f, ok):
    n = 1
    while not ok(n):
        n += 1
    return n


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); a = ap.parse_args()
    TA = os.path.join(ROOT, "harness", "dg1_cache", "train_ac")
    kit = os.path.join(ROOT, "_bundles", "colab_rl_test", "kit")
    import pycocoevalcap, sacrebleu, peft, transformers
    pcc = list(pycocoevalcap.__path__)[0]
    jv = subprocess.run([glob.glob(os.path.expanduser("~/.jdk/*/bin/java"))[0], "-version"], capture_output=True, text=True).stderr.splitlines()[0]
    m = {
        "scope": "LOCAL (WSL). Lượt GPU/CPU trên Kaggle phải in lại đúng các hash này trong log trước khi chạy; lệch ⇒ STOP.",
        "base_model": snap("Qwen/Qwen2.5-VL-3B-Instruct"),
        "grounder_primary": snap("osunlp/UGround-V1-2B"),
        "s1_adapter": tree(os.path.join(kit, "adapter_s1_seed101")),
        "sft_cont_adapter": {**tree(os.path.join(kit, "sft_final")),
                             "md5_model": hashlib.md5(open(os.path.join(kit, "sft_final", "adapter_model.safetensors"), "rb").read()).hexdigest(),
                             "nguon": "kernel uyenle0712/luoi-test-u-3 chấm test sft_tiep_101 với md5 113e2a3e… (report/320 §18: exec 60,16)"},
        "sft_cont_prompt_keys": file_(os.path.join(ROOT, "_bundles", "luoi", "ds", "prompt_keys_ck500.json")),
        "pool": file_(os.path.join(TA, "train_tru_val.jsonl")),
        "train_all": file_(os.path.join(TA, "train.jsonl")),
        "ocr": file_(os.path.join(TA, "ocr.jsonl")),
        "a11y_forest": file_(os.path.realpath(glob.glob(os.path.join(HF, "datasets--HarrytheOrange--parsed_AndroidControl", "snapshots", "*", "all_forest_dict.zip"))[0])),
        "image_root": {"path": os.path.join(TA, "images"), "files": len(os.listdir(os.path.join(TA, "images"))),
                       "tree_sha256": "CHƯA TÍNH — do `sa3_split.py hash` ghi sha256 từng ảnh; tree hash rút từ tệp đó"},
        "scorers": {
            "pycocoevalcap_tree": tree(pcc),
            "spice_jar": file_(os.path.join(pcc, "spice", "spice-1.0.jar")),
            "spice_lib_tree": tree(os.path.join(pcc, "spice", "lib")),
            "corenlp_jars": "KHÔNG có ở máy nhà; trên Kaggle dùng dataset trangphngngc/corenlp-360-jars — phải ghim hash trong log",
            "java": jv, "python": platform.python_version(), "sacrebleu": sacrebleu.__version__,
            "peft": peft.__version__, "transformers": transformers.__version__,
        },
    }
    # cỡ mẫu audit: n nhỏ nhất để bound đạt khi số lỗi quan sát = k
    tab = {}
    for k in (0, 1, 2, 3):
        tab[f"PPV>98%_k{k}"] = n_min(None, lambda n, k=k: n > k and cp_lower(n - k, n) > 0.98)
        tab[f"rate<5%_k{k}"] = n_min(None, lambda n, k=k: n > k and cp_upper(k, n) < 0.05)
    m["audit_sample_size_one_sided_95"] = tab
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(m, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(tab), flush=True)
    for k, v in m.items():
        if isinstance(v, dict):
            print(k, "MISSING" if v.get("MISSING") else (v.get("tree_sha256") or v.get("sha256") or "")[:16], flush=True)


if __name__ == "__main__":
    main()
