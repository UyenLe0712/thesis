#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C1 reward-screen audit on CPU. VAL ONLY; never a held-out test claim.

Usage:
  python reward_cpu_8_11.py --data /path/to/c1-dataset --out /path/to/out --bootstrap 500
  python reward_cpu_8_11.py --selftest
Requires pycocoevalcap + Java/CoreNLP for real SPICE, and sacrebleu for chrF.
All candidates, labels and coordinates are from saved C1 val runs; NO model inference.
"""
import argparse
import collections
import itertools
import json
import math
import random
import re
import statistics
import time
from pathlib import Path

PENALTY = 0.02
CAP = 0.05
STRESS = [
    ("Click on Settings", "Tap Settings", "Swipe on Settings", "wrong_action"),
    ("Click on Cancel", "Tap Cancel", "Click on Delete", "wrong_target"),
    ("Scroll down", "Scroll down", "Click on the down arrow", "zero_tuple"),
    ("Go back", "Return to the previous screen", "Click the back icon", "paraphrase"),
    ("Open the Clock app", "Launch the Clock app", "Swipe to the Clock app", "wrong_action"),
    ("Type Hello in the search field", "Enter Hello in the search field", "Type Goodbye in the search field", "wrong_argument"),
    ("Click the icon at the top right", "Tap the upper-right icon", "Click the icon at the bottom left", "wrong_position"),
    ("Enable notifications", "Turn on notifications", "Disable notifications", "toggle_contradiction"),
]

def normalize_action(label):
    return {"click": "tap", "long_press": "tap", "scroll": "scroll",
            "navigate_back": "back", "input_text": "type",
            "open_app": "open_app", "wait": "wait"}.get(label)

def classify(sentence):
    """Conservative parser: unknown is never silently converted to click."""
    s = " ".join(re.findall(r"[a-z0-9']+", (sentence or "").lower()))
    if not s:
        return None
    if re.search(r"\b(go back|navigate back|return to (the )?(previous|last) screen|press (the )?back (button|key))\b", s):
        return "back"
    if re.search(r"\b(scroll|swipe)\b", s):
        return "scroll"
    if re.search(r"\b(wait|pause|let (it|the page) load)\b", s):
        return "wait"
    if re.search(r"\b(type|enter|input|fill in|write)\b", s):
        return "type"
    if re.search(r"\b(open|launch|start)\b.*\bapp\b", s):
        return "open_app"
    if re.search(r"\b(tap|click|press|select|choose|check|enable|disable|turn on|turn off|open)\b", s):
        return "tap"
    return None

def length_penalty(s, g, cap=True):
    words = lambda t: len(re.findall(r"[A-Za-z0-9'-]+", t))
    d = PENALTY * max(0, words(s) - words(g) - 3)
    return min(CAP, d) if cap else d

def reward_variant(name, sentence, gold, action_label, spice, chrf, gold_self_spice):
    if not sentence.strip():
        return 0.0
    p = length_penalty(sentence, gold, cap=name != "R0_historical")
    s = spice
    if name == "R0_historical":
        return s - p
    if name == "R0_capped":
        return max(0.0, s - p)
    q = chrf if gold_self_spice <= 1e-9 else 0.8 * s + 0.2 * chrf
    if name == "R2_sparse":
        return max(0.0, q - p)
    if name == "R_fixed_spice_chrf":
        return max(0.0, 0.8 * s + 0.2 * chrf - p)
    if name in ("R3_action", "R4_sparse_action"):
        val = s if name == "R3_action" else q
        expected = normalize_action(action_label)
        ref_act = classify(gold)
        pred_act = classify(sentence)
        trusted = expected is not None and expected == ref_act
        if trusted and pred_act is not None:
            if pred_act != expected:
                return 0.0
            return max(0.0, 0.2 + 0.8 * val - p)
        return max(0.0, val - p)
    raise ValueError(name)

REWARDS = ["R0_historical", "R0_capped", "R_fixed_spice_chrf",
           "R2_sparse", "R3_action", "R4_sparse_action"]

def selftest():
    # The self-score of "Scroll down" can be 0 in SPICE; fallback must fix it.
    a = reward_variant("R2_sparse", "Scroll down", "Scroll down", "scroll", 0.0, 1.0, 0.0)
    b = reward_variant("R4_sparse_action", "Scroll down", "Scroll down", "scroll", 0.0, 1.0, 0.0)
    c = reward_variant("R4_sparse_action", "Click on the arrow", "Scroll down", "scroll", 0.7, 0.4, 0.0)
    assert abs(a - 1) < 1e-9 and abs(b - 1) < 1e-9 and c == 0, (a, b, c)
    # Contradictory reference vs trajectory: gate must abstain.
    x = reward_variant("R4_sparse_action", "Click Next", "Click Next", "wait", 0.3, 1, 0.3)
    assert x > 0
    assert classify("Return to the previous screen") == "back"
    assert classify("Press the Back button") == "back"
    assert classify("Swipe up") == "scroll"
    assert classify("Scroll down") == "scroll"
    assert classify("Open the Clock app") == "open_app"
    assert classify("Type Hello in the box") == "type"
    assert classify("Click Settings") == "tap"
    assert classify("no actionable verb here") is None
    assert length_penalty("Tap Settings", "Tap Settings") == 0
    print("SELFTEST_OK: score fallback, hard gate, abstention, action parsing")

def spice_scores(pairs, batch_size):
    from pycocoevalcap.spice.spice import Spice
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
    engine = Spice()
    tokenizer = PTBTokenizer()
    unique = list(dict.fromkeys(pairs))
    result = {}
    for start in range(0, len(unique), batch_size):
        block = unique[start:start+batch_size]
        # Khoá số nguyên: Spice.compute_score trả điểm theo sorted(keys); khoá chuỗi xếp "0","1","10",... làm lệch zip dưới đây.
        gts = {i: [{"caption": r}] for i, (_, r) in enumerate(block)}
        res = {i: [{"caption": s}] for i, (s, _) in enumerate(block)}
        gts, res = tokenizer.tokenize(gts), tokenizer.tokenize(res)
        _, scores = engine.compute_score(gts, res)
        assert len(scores) == len(block), "SPICE returned a partial batch"
        for pair, score in zip(block, scores):
            f = score.get("All", {}).get("f", 0)
            result[pair] = float(f) if f is not None and math.isfinite(float(f)) else 0.0
            if pair[0] == pair[1]:   # câu tự so chỉ có thể 1 (hoặc 0 khi không có tuple); khác đi là điểm bị lệch cặp
                assert result[pair] in (0.0, 1.0), ("SPICE misaligned", pair, result[pair])
        print(f"[SPICE] {min(start+batch_size,len(unique))}/{len(unique)} pairs", flush=True)
    return result

def load_c1(data):
    with (data/"c1_mau.jsonl").open(encoding="utf8") as f:
        rows = [json.loads(line) for line in f]
    assert len(rows) == 400 and all(len(x["mau"]) == 8 for x in rows)
    exec_rows = {}
    for i in range(1, 9):
        p = data/f"score_k{i}_raw.jsonl"
        assert p.is_file(), f"Missing {p}"
        for ln in p.open(encoding="utf8"):
            r = json.loads(ln)
            key = (r["episode_id"], r["step_id"], i)
            assert key not in exec_rows
            exec_rows[key] = r
    observed = 0
    for m in rows:
        key0 = (m["episode_id"], m["step_id"])
        for i, sent in enumerate(m["mau"], start=1):
            r = exec_rows.get((*key0,i))
            if r:
                assert r.get("sent","").strip() == (sent or "").strip(), "C1 sentence/exec mismatch"
                observed += 1
    assert observed == 249*8, ("Expected 249 tap groups",observed)
    return rows, exec_rows

def group_stats(groups, outcome):
    ties = []
    zero = []
    conc = []
    uplift = []
    for rewards, e in zip(groups, outcome):
        assert len(rewards)==len(e)==8
        zero.append(float(max(rewards)-min(rewards)<1e-9))
        pairs=list(itertools.combinations(range(8),2))
        ties.append(sum(abs(rewards[i]-rewards[j])<1e-9 for i,j in pairs)/len(pairs))
        for i,j in pairs:
            if e[i] != e[j]:
                d=(rewards[i]-rewards[j])*(e[i]-e[j])
                conc.append(1.0 if d>0 else 0.0 if d<0 else 0.5)
        mx=max(rewards)
        max_out=[v for r,v in zip(rewards,e) if abs(r-mx)<1e-9]
        uplift.append(100*(sum(max_out)/len(max_out)-sum(e)/len(e)))
    mean=lambda a: round(statistics.mean(a),4) if a else None
    return dict(n=len(groups), std0=mean(zero), tie=mean(ties), concordance=mean(conc),
                n_pairs_different_outcomes=len(conc), oracle_uplift_pp=round(mean(uplift),2),
                mean_outcome=round(100*statistics.mean(y for e in outcome for y in e),2))

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--data",type=Path)
    a.add_argument("--out",type=Path)
    a.add_argument("--batch-size",type=int,default=350)
    a.add_argument("--selftest",action="store_true")
    args=a.parse_args()
    selftest()
    if args.selftest:
        return
    assert args.data and args.out
    rows, exe=load_c1(args.data)
    from sacrebleu.metrics import CHRF
    chrf=CHRF()
    pairs=[(s or "",m["gold"]) for m in rows for s in m["mau"]]
    pairs += [(m["gold"],m["gold"]) for m in rows]
    pairs += [(s,g) for g,good,bad,_ in STRESS for s in (g,good,bad)]
    spice=spice_scores(pairs,args.batch_size)
    char={pair:chrf.sentence_score(pair[0], [pair[1]]).score/100 for pair in dict.fromkeys(pairs)}
    assert all(0<=v<=1.000001 for v in spice.values())
    assert all(0<=v<=1.000001 for v in char.values())
    records=[]
    for m in rows:
        k=(m["episode_id"],m["step_id"])
        act=m["action_type"]
        trusted=int(classify(m["gold"]) == normalize_action(act))
        rs={name:[] for name in REWARDS}
        gold_self=spice[(m["gold"],m["gold"])]
        outs=[]
        for i,s in enumerate(m["mau"],1):
            sent=s or ""
            sp=spice[(sent,m["gold"])]
            cf=char[(sent,m["gold"])]
            for name in REWARDS:
                rs[name].append(reward_variant(name,sent,m["gold"],act,sp,cf,gold_self))
            if act == "click":
                outs.append(int(exe[(*k,i)]["executable"]))
            else:
                outs.append(int(bool(classify(sent)) and classify(sent)==normalize_action(act)))
        records.append(dict(episode_id=m["episode_id"],step_id=m["step_id"],action=act,
                            trusted_gold_action=trusted,gold_self_spice=gold_self,rs=rs,outcomes=outs))
    results={
        "metadata":{
          "scope":"400 C1 VALIDATION prompts, S1/101 8 samples each; NO model training, NO test evaluation",
          "tap_outcome":"UGround V1 2B held C1 step executability (249 prompts)",
          "non_tap_proxy":"conservative text action-type match, NOT end-to-end executability",
          "warning":"H2 rank predictive validity for post-training performance is not established",
          "formulas":"R2 sparse-fallback only when SPICE(g,g)==0; R3 hard action gate; R4 both",
          "n_prompts":len(rows), "n_tap":sum(r["action"]=="click" for r in records)},
        "trust_coverage":{},
        "gold_self":{},
        "rewards":{},
        "stress":[]
    }
    for act in sorted({x["action"] for x in records}):
        subset=[x for x in records if x["action"]==act]
        results["trust_coverage"][act]=dict(n=len(subset),verified=sum(x["trusted_gold_action"] for x in subset),
                                            frac_verified=round(statistics.mean(x["trusted_gold_action"] for x in subset),3))
        results["gold_self"][act]=dict(zero_spice=sum(x["gold_self_spice"]<=1e-9 for x in subset),
                                       fraction_zero=round(statistics.mean(x["gold_self_spice"]<=1e-9 for x in subset),3))
    for name in REWARDS:
        dic={}
        for act in ("all","tap","non_tap","scroll","navigate_back","input_text","wait","open_app"):
            group=[r for r in records if act=="all" or (act=="tap" and r["action"]=="click") or
                   (act=="non_tap" and r["action"]!="click") or r["action"]==act]
            if group:
                dic[act]=group_stats([r["rs"][name] for r in group],[r["outcomes"] for r in group])
        results["rewards"][name]=dic
    for gold,good,bad,tag in STRESS:
        action="navigate_back" if classify(gold)=="back" else ("open_app" if classify(gold)=="open_app" else
                 "scroll" if classify(gold)=="scroll" else "input_text" if classify(gold)=="type" else "click")
        ss=spice[(gold,gold)]
        rr={n:[round(reward_variant(n,s,gold,action,spice[(s,gold)],char[(s,gold)],ss),4)
               for s in (gold,good,bad)] for n in REWARDS}
        results["stress"].append(dict(tag=tag,gold=gold,good=good,bad=bad,reward=rr))
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"reward_cpu_c1.json").write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding="utf8")
    with (args.out/"reward_groups.jsonl").open("w",encoding="utf8") as f:
        for r in records:
            f.write(json.dumps(r,ensure_ascii=False)+"\n")
    print(json.dumps(results["trust_coverage"],indent=2,ensure_ascii=False))
    print(json.dumps(results["gold_self"],indent=2,ensure_ascii=False))
    for name,d in results["rewards"].items():
        print(f"{name:22s} TAP={d['tap']['concordance']} STD0={d['tap']['std0']} "
              f"NON_TAP={d['non_tap']['concordance']} STD0={d['non_tap']['std0']}",flush=True)
    print("OUTPUT",args.out.resolve())

if __name__=="__main__":
    main()
