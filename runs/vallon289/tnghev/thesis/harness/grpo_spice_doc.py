# -*- coding: utf-8 -*-
"""Đọc kết quả GRPO thưởng SPICE (Phụ lục B của harness/tai_lieu_2026-09-29/253_…md), 0 GPU.

Đặt pred_ck{250,500}.jsonl + score_ck{250,500}_raw.jsonl vào runs/grpo_spice/ rồi chạy
    ~/.venvs/thesis/bin/python harness/grpo_spice_doc.py
Kiểm đường: S1 SPICE phải in 57.30. Số val, cấm trích.
"""
import json, os, random, re
from pathlib import Path

JH = os.path.expanduser("~/.jdk/jdk8u504-b01")
os.environ["JAVA_HOME"] = JH
os.environ["PATH"] = JH + "/bin:" + os.environ["PATH"]

from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.spice.spice import Spice

T = Path("/mnt/d/Master/Thesis")
C1 = [json.loads(l) for l in open(
    T / "runs/c1/c1_mau.jsonl",
    encoding="utf-8",
)]
# greedy S1 chấm lại trong cùng phiên Pha 3 (cùng dụng cụ); chưa có thì lùi về bản của 251
K0P = T / "runs/grpo_spice/score_k0_lai_raw.jsonl"
if not K0P.exists():
    K0P = T / "runs/c1/exec8/c1score/score_k0_raw.jsonl"
K0 = {
    (o["episode_id"], o["step_id"]): o
    for o in map(json.loads, open(K0P, encoding="utf-8"))
}
EX_S1 = 100 * sum(int(o["executable"]) for o in K0.values()) / len(K0)
print(f"mốc S1: {K0P.name} · {len(K0)} bước · exec {EX_S1:.2f} (251: 63.45)")

E = T / "runs/grpo_spice"
W = re.compile(r"[A-Za-z0-9'-]+")
keys = [(d["episode_id"], d["step_id"]) for d in C1]

tk = PTBTokenizer()
g = tk.tokenize({i: [{"caption": d["gold"]}] for i, d in enumerate(C1)})


def spice(sents):
    c = tk.tokenize({i: [{"caption": s or "none"}] for i, s in enumerate(sents)})
    _, sc = Spice().compute_score(g, c)
    return [x["All"]["f"] for x in sc]


sp_s1 = spice([d["greedy"] for d in C1])
eps = sorted({k[0] for k in keys})


def boot(diff, ks):
    th = {e: [k for k in ks if k[0] == e] for e in {k[0] for k in ks}}
    E_ = sorted(th)
    rng = random.Random(101)
    ds = []

    for _ in range(10000):
        qs = [k for e in (rng.choice(E_) for _ in E_) for k in th[e]]
        ds.append(100 * sum(diff[k] for k in qs) / len(qs))

    ds.sort()
    return round(ds[249], 2), round(ds[9749], 2)


for s in (250, 500):
    P = {
        (d["episode_id"], d["step_id"]): d["pred"]
        for d in map(
            json.loads,
            open(E / f"pred_ck{s}.jsonl", encoding="utf-8"),
        )
    }
    assert set(P) == set(keys)

    sp = spice([P[k] for k in keys])
    dsp = {k: sp[i] - sp_s1[i] for i, k in enumerate(keys)}

    R = {
        (o["episode_id"], o["step_id"]): o
        for o in map(
            json.loads,
            open(E / f"score_ck{s}_raw.jsonl", encoding="utf-8"),
        )
    }

    tap = [k for k in keys if k in K0]
    assert len(tap) == 249 and set(R) == set(tap)

    dex = {
        k: int(R[k]["executable"]) - int(K0[k]["executable"])
        for k in tap
    }
    ex = 100 * sum(int(R[k]["executable"]) for k in tap) / 249

    words = sum(len(W.findall(P[k])) for k in keys) / 400
    words_s1 = sum(len(W.findall(d["greedy"])) for d in C1) / 400

    print(
        f"ck{s}: SPICE {100*sum(sp)/400:.2f} "
        f"(S1 {100*sum(sp_s1)/400:.2f}, Δ {100*sum(dsp.values())/400:+.2f}, KTC {boot(dsp, keys)})"
        f" · exec {ex:.2f} (S1 {EX_S1:.2f}, Δ {ex-EX_S1:+.2f}, KTC {boot(dex, tap)})"
        f" · cứu {sum(v == 1 for v in dex.values())} phá {sum(v == -1 for v in dex.values())}"
        f" · số từ {words:.2f} (S1 {words_s1:.2f}) · rỗng {sum(not P[k] for k in keys)}"
        f" · trùng câu S1 {sum(P[k] == C1[i]['greedy'] for i, k in enumerate(keys))}/400"
    )
