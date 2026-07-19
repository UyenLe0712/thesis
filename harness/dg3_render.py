# -*- coding: utf-8 -*-
"""
dg3_render.py — BUILD DATA SFT (report/53 §2.6-§2.9). Bien base-runs cua teacher gpt-4o-mini
thanh file train ShareGPT cho LLaMA-Factory. Buoc-khop giu nguyen ten nut that; buoc-bia
duoc VIET LAI TAT DINH thanh mo ta chung (dg3_rewrite_fallback). KHONG goi API luc render
(matcher nomic la LOCAL/free; tu-kiem tiem matcher gia -> khong can Ollama).

Ra:
  dg3_out/sft_train.json   — list ShareGPT record {id, conversations, images}
  dg3_out/sft_meta.jsonl   — 1 dong/record: audit + leakage-check (id, app, split, n_fallback...)

Nguyen tac chong-leak: chi render app thuoc TRAIN (train_apps_30 ∪ train_pool_expanded);
assert giao 12 test-app = rong TRUOC khi ghi (cong K-leak lap lai, report/56 §1).

Chay tu-kiem:  python dg3_render.py --selftest
Chay that   :  python dg3_render.py            (can dg3_cache/runs/*.json tu teacher-gen)
"""
import os, sys, json, glob, argparse, tempfile, shutil
sys.path.insert(0, os.path.dirname(__file__))
from dg3_rewrite_fallback import rewrite_fallback

HERE = os.path.dirname(__file__)
SPLIT_FP = os.path.join(HERE, "train_eval_app_split.json")
RUNS_DIR = os.path.join(HERE, "dg3_cache", "runs")
OUT_DIR = os.path.join(HERE, "dg3_out")
TAU_A = float(os.environ.get("TAU_A", "0.55"))

# Prompt student — GIONG HET o 3 cho (SFT record / eval-co-VH / eval-khong-VH), report/53 §2.7.
# CO Y KHONG chua "don't invent buttons" (khac GEN_PROMPT teacher — diem mau chot pre-reg §3).
STUDENT_USER_PROMPT = ('Write step-by-step instructions for a person to follow on their phone, '
                       'to: "{q}"')


def _title_verb(verb):
    w = (verb or "").strip().split()
    return w[0].capitalize() if w else "Tap"


def render_steps(steps):
    """steps: list {verb, element, status, (text)}. Tra chuoi tutorial danh so."""
    lines = []
    for i, s in enumerate(steps, 1):
        if s["status"] == "fallback":
            lines.append(f'{i}. {s["text"]}')
        else:                                    # matched: giu ten nut that
            lines.append(f'{i}. {_title_verb(s["verb"])} "{s["element"]}"')
    return "\n".join(lines)


def classify_steps(base, labels, matcher, tau_a=TAU_A):
    """
    Chia moi buoc base thanh matched (nomic sim>=tau_a) hoac fallback (viet lai tat dinh).
    matcher(name, labels)->(label, sim). Tra (steps_out, n_matched, n_fallback).
    """
    out, n_m, n_f = [], 0, 0
    for s in base:
        el = (s.get("element") or "").strip()
        if el:
            _, sim = matcher(el, labels)
        else:
            sim = 0.0
        if el and sim >= tau_a:
            out.append({"verb": s.get("verb", ""), "element": el, "status": "matched"})
            n_m += 1
        else:
            text = rewrite_fallback(s.get("verb", ""), el, s.get("note", ""),
                                    labels, tau_a=tau_a, matcher=matcher)
            out.append({"verb": s.get("verb", ""), "element": el,
                        "status": "fallback", "text": text})
            n_f += 1
    return out, n_m, n_f


def render_steps_raw(base):
    """Ban THO (Student-RAW): giu NGUYEN moi buoc teacher, KHONG loc/viet-lai (ke ca buoc bia)."""
    lines = []
    for i, s in enumerate(base, 1):
        el = (s.get("element") or "").strip()
        lines.append(f'{i}. {_title_verb(s.get("verb", ""))} "{el}"' if el
                     else f'{i}. {_title_verb(s.get("verb", ""))}')
    return "\n".join(lines)


def _human_value(rec):
    return "<image>\n" + STUDENT_USER_PROMPT.format(q=rec.get("question", ""))


def _sharegpt(rid, human, gpt, img_rel):
    return {"id": rid,
            "conversations": [{"from": "human", "value": human}, {"from": "gpt", "value": gpt}],
            "images": [img_rel]}


def render_record(rec, matcher, tau_a=TAU_A, image_dir="mv_train_pool"):
    """Mot base-run -> (sharegpt_record, meta_dict). rec theo schema dg1_run.py + optional question_idx."""
    labels = rec.get("elem_labels", [])
    steps, n_m, n_f = classify_steps(rec.get("base", []), labels, matcher, tau_a)
    qidx = rec.get("question_idx", 0)
    screen = rec["screen"]
    app = rec.get("app") or screen.split("_")[0]
    rid = f"mv__{screen}__q{qidx}"
    img_rel = rec.get("image") or f"{image_dir}/{screen}.jpg"
    human = _human_value(rec)
    sharegpt = _sharegpt(rid, human, render_steps(steps), img_rel)          # DA LOC (Student)
    sharegpt_raw = _sharegpt(rid, human, render_steps_raw(rec.get("base", [])), img_rel)  # THO (Student-RAW)
    meta = {
        "id": rid, "source": "mobileviews", "app": app, "screen": screen,
        "teacher_model": rec.get("model", ""), "tau_a": tau_a,
        "n_steps": len(steps), "n_fallback": n_f, "n_matched": n_m,
        "question_idx": qidx, "split": "train",
    }
    return sharegpt, sharegpt_raw, meta


def _load_train_apps():
    d = json.load(open(SPLIT_FP, encoding="utf-8"))["mobileviews"]
    train = set(d.get("train_apps_30", [])) | set(d.get("train_pool_expanded", []))
    test = set(d.get("test_apps_30", []))
    return train, test


def build(records, matcher, out_dir=OUT_DIR):
    """Render nhieu record -> ghi sft_train.json + sft_meta.jsonl. Assert K-leak truoc khi ghi."""
    train_apps, test_apps = _load_train_apps()
    sft, sft_raw, meta_rows, skipped = [], [], [], 0
    for rec in records:
        app = rec.get("app") or rec["screen"].split("_")[0]
        if app in test_apps:
            raise AssertionError(f"K-LEAK: app test '{app}' lot vao data train (screen={rec['screen']})")
        if train_apps and app not in train_apps:     # bo qua app ngoai train set (an toan)
            skipped += 1
            continue
        sr, sr_raw, mt = render_record(rec, matcher)
        sft.append(sr); sft_raw.append(sr_raw); meta_rows.append(mt)
    os.makedirs(out_dir, exist_ok=True)
    json.dump(sft, open(os.path.join(out_dir, "sft_train.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    json.dump(sft_raw, open(os.path.join(out_dir, "sft_train_raw.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, "sft_meta.jsonl"), "w", encoding="utf-8") as f:
        for m in meta_rows:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    return sft, sft_raw, meta_rows, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return 0 if _selftest() else 1
    # Chay that: can matcher nomic that (Ollama local) + base-runs teacher.
    from aloha_match import best_match
    files = sorted(glob.glob(os.path.join(RUNS_DIR, "*.json")))
    if not files:
        print(f"Chua co base-run trong {RUNS_DIR} -> chay teacher-gen (buoc ✱ API) truoc.")
        return 0
    records = [json.load(open(f, encoding="utf-8")) for f in files]
    sft, sft_raw, meta, skipped = build(records, best_match)
    print(f"xong: {len(sft)} record SFT (bo qua {skipped} ngoai train) -> {OUT_DIR}/sft_train.json + sft_train_raw.json")
    nf = sum(m["n_fallback"] for m in meta); nt = sum(m["n_steps"] for m in meta) or 1
    print(f"  buoc: {nt} tong | fallback {nf} ({nf/nt*100:.0f}%) | matched {nt-nf} ({(nt-nf)/nt*100:.0f}%)")


# ----------------------------- TU KIEM (fake data, khong mang) -----------------------------
def _fake_matcher(name, labels):
    """Matcher gia tat dinh: 'khop' neu ten (chuan hoa) TRUNG mot nhan; nguoc lai sim thap."""
    n = (name or "").strip().lower()
    for l in labels:
        if n and n == (l or "").strip().lower():
            return (l, 0.99)
    return (labels[0] if labels else None, 0.10)


def _selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    train_apps, test_apps = _load_train_apps()
    a_train = next(iter(train_apps)) if train_apps else "trainapp"
    a_test = next(iter(test_apps)) if test_apps else "testapp"

    rec = {
        "screen": f"{a_train}_s1", "app": a_train, "model": "gpt-4o-mini",
        "question": "How do I turn on notifications?", "question_idx": 0,
        "elem_labels": ["Settings", "Notifications", "Save"],
        "base": [
            {"verb": "Tap", "element": "Settings", "note": "open settings"},        # matched
            {"verb": "Tap", "element": "Ghost Menu", "note": "to open the hidden menu"},  # bia -> fallback
            {"verb": "Toggle", "element": "Notifications", "note": ""},              # matched
        ],
    }
    sr, sr_raw, mt = render_record(rec, _fake_matcher)

    chk("record: id dung dinh dang", sr["id"] == f"mv__{a_train}_s1__q0")
    chk("record: human co <image> + prompt", sr["conversations"][0]["value"].startswith("<image>\n") and
        "step-by-step" in sr["conversations"][0]["value"])
    chk("record: human KHONG chua 'invent'", "invent" not in sr["conversations"][0]["value"].lower())
    gpt = sr["conversations"][1]["value"]
    chk("render: matched giu ten that 'Settings'", '1. Tap "Settings"' in gpt)
    chk("render: buoc bia KHONG lo ten 'Ghost Menu'", "ghost menu" not in gpt.lower())
    chk("render: buoc bia thanh mo ta chung", "option on this screen" in gpt.lower())
    chk("meta: dem dung 1 fallback / 2 matched", mt["n_fallback"] == 1 and mt["n_matched"] == 2)
    chk("meta: split=train", mt["split"] == "train")
    chk("record: images tro dung anh", sr["images"] == [f"mv_train_pool/{a_train}_s1.jpg"])

    # Ban THO (Student-RAW): giu NGUYEN ten bia 'Ghost Menu' (khong loc) -> khac ban da loc.
    gpt_raw = sr_raw["conversations"][1]["value"]
    chk("raw: giu nguyen ten bia 'Ghost Menu'", '"Ghost Menu"' in gpt_raw)
    chk("raw: khac ban da loc", gpt_raw != gpt)

    outdir = os.path.join(tempfile.gettempdir(), "dg3_render_selftest")   # temp -> khong rac repo

    # K-leak: record app TEST phai bi chan (raise).
    bad = dict(rec, screen=f"{a_test}_s1", app=a_test)
    raised = False
    try:
        build([bad], _fake_matcher, out_dir=outdir)
    except AssertionError:
        raised = True
    chk("K-leak: app test bi chan (raise)", raised)

    # build() ghi file + bo qua app ngoai train.
    sft, sft_raw, meta, skipped = build([rec, dict(rec, screen="zzunknownapp_s1", app="zzunknownapp")],
                                        _fake_matcher, out_dir=outdir)
    chk("build: giu 1 record train, bo 1 ngoai", len(sft) == 1 and skipped == 1)
    chk("build: sft_raw cung 1 record", len(sft_raw) == 1)
    chk("build: file sft_train.json ton tai", os.path.exists(os.path.join(outdir, "sft_train.json")))
    chk("build: file sft_train_raw.json ton tai", os.path.exists(os.path.join(outdir, "sft_train_raw.json")))
    chk("build: file sft_meta.jsonl ton tai", os.path.exists(os.path.join(outdir, "sft_meta.jsonl")))

    shutil.rmtree(outdir, ignore_errors=True)                            # don temp
    print("\n=> " + ("TAT CA PASS" if ok else "CO FAIL — xem tren"))
    return ok


if __name__ == "__main__":
    sys.exit(main() or 0)
