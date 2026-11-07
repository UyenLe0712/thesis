# -*- coding: utf-8 -*-
"""H3 (report/323 §8.4): vì sao mốc nhóm (GRPO) hợp hơn mốc greedy (SCST) hay mốc trượt (REINFORCE) — chỉ đọc log train đã có.

Đọc các dòng dict mà TRL in ra stdout (`{'loss': ...}`) trong train.log của mỗi lượt, gộp các commit nối tiếp theo `epoch`
(bỏ dòng trùng epoch). Chỉ số theo bước: frac_reward_zero_std (tỉ lệ nhóm có mọi thưởng bằng nhau ⇒ lợi thế 0 ở GRPO),
luoi/frac_adv_zero (tỉ lệ mẫu có lợi thế đúng bằng 0 ở SCST/RLOO/REINFORCE…), luoi/adv_abs_mean, luoi/r_greedy, reward,
reward_std, kl, entropy, completions/mean_length. Báo trung bình toàn lượt và theo bốn phần tư số bước.
Dự đoán ghi trước (report/323): S1 ít ngẫu nhiên ⇒ SCST có nhiều mẫu lợi thế 0 (mẫu trùng greedy); mốc trượt nhiễu.

  python h3_log_train.py --out ../runs/giai_thich/c/h3_log_train.json
"""
import os, json, argparse, ast, glob, re, collections

K = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CS = ["frac_reward_zero_std", "luoi/frac_adv_zero", "luoi/adv_abs_mean", "luoi/r_greedy", "reward", "reward_std",
      "kl", "entropy", "completions/mean_length", "luoi/v_ev", "luoi/v_loss"]


def doc(p):
    R = []
    for l in open(p, encoding="utf-8", errors="ignore"):
        l = l.strip()
        i = l.find("{'loss'")
        if i < 0:
            continue
        try:
            d = ast.literal_eval(l[i:l.rfind("}") + 1])
        except Exception:
            continue
        if "epoch" in d and ("reward" in d or "kl" in d):
            R.append({k: float(v) for k, v in d.items() if _so(v)})
    return R


def _so(v):
    try:
        float(v); return True
    except Exception:
        return False


def tom(R):
    o = dict(n_dong=len(R))
    q = max(1, len(R) // 4)
    for c in CS:
        v = [r[c] for r in R if c in r]
        if not v:
            continue
        o[c] = round(sum(v) / len(v), 4)
        o[c + "__4phan"] = [round(sum(x) / len(x), 4) for x in (v[i * q:(i + 1) * q] if i < 3 else v[3 * q:] for i in range(4)) if x]
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    nhom = collections.defaultdict(list)
    for p in sorted(glob.glob(f"{K}/runs/luoi/**/train.log", recursive=True)):
        if "smoke" in p or "moi_b" in p:
            continue
        nhom[os.path.basename(os.path.dirname(p))].append(p)
    nhom["ck500_grpo_spice"] = [f"{K}/runs/grpo_spice/train_c1.log", f"{K}/runs/grpo_spice/train_c3.log"]
    out = {}
    for ten, ps in sorted(nhom.items()):
        R = {}
        for p in ps:
            if not os.path.exists(p):
                continue
            for r in doc(p):
                R.setdefault(round(r["epoch"], 4), r)
        R = [R[e] for e in sorted(R)]
        if not R:
            continue
        o = tom(R)
        o["tep"] = [os.path.relpath(p, K) for p in ps]
        o["epoch_dau_cuoi"] = [R[0]["epoch"], R[-1]["epoch"]]
        out[ten] = o
        print(ten, json.dumps({k: v for k, v in o.items() if "__" not in k and k != "tep"}, ensure_ascii=False), flush=True)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    print("[xong] ghi", a.out, flush=True)


if __name__ == "__main__":
    main()
