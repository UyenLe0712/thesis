"""Dùng lại kết quả UGround cho câu đã chấm trên cùng bước, để bớt 5,4 h chấm mỗi nhánh (thước tất định, CLAUDE.md).

  gieo:  ghi sẵn tệp thô của nhánh từ các tệp thô cũ khi câu TRÙNG TỪNG KÝ TỰ; chừa 40 bước ngẫu nhiên để chấm thật
  kiem:  sau khi chấm, so 40 bước đó với bản cũ; lệch quá 1 bước là dừng, không được dùng số
  python tai_dung_cham.py gieo --preds P --raw R --nguon a_raw.jsonl b_raw.jsonl
  python tai_dung_cham.py kiem --raw R --nguon a_raw.jsonl b_raw.jsonl
"""
import os, json, random, argparse


def nap(ps):
    K = {}
    for p in ps:
        for x in map(json.loads, open(p, encoding="utf-8")):
            if x.get("sent") and x.get("pred_xy") is not None:
                K.setdefault((x["episode_id"], x["step_id"], x["sent"]), x)
    return K


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lenh", choices=("gieo", "kiem"))
    ap.add_argument("--preds")
    ap.add_argument("--raw", required=True)
    ap.add_argument("--nguon", nargs="+", required=True)
    a = ap.parse_args()
    K = nap(a.nguon)
    giu = a.raw + ".chua_lai.json"
    if a.lenh == "gieo":
        if os.path.exists(a.raw):
            print("[gieo] đã có tệp thô, không gieo lại", flush=True)
            return
        P = list(map(json.loads, open(a.preds, encoding="utf-8")))
        trung = [(p["episode_id"], p["step_id"], p["pred"]) for p in P if (p["episode_id"], p["step_id"], p["pred"]) in K]
        rd = random.Random(20261102)
        chua = set(rd.sample(trung, min(40, len(trung))))
        with open(a.raw, "w", encoding="utf-8") as f:
            for k in trung:
                if k not in chua:
                    f.write(json.dumps(K[k], ensure_ascii=False) + "\n")
        json.dump(sorted(map(list, chua)), open(giu, "w"), ensure_ascii=False)
        print(f"[gieo] {len(P)} câu · dùng lại {len(trung) - len(chua)} · chừa kiểm {len(chua)} · phải chấm {len(P) - len(trung) + len(chua)}", flush=True)
        return
    moi = {(x["episode_id"], x["step_id"]): x for x in map(json.loads, open(a.raw, encoding="utf-8"))}
    lech = []
    chua = [tuple(x) for x in json.load(open(giu))]
    for e, s, c in chua:
        x, y = moi[(e, s)], K[(e, s, c)]
        if x.get("pred_xy") != y.get("pred_xy") or x.get("executable") != y.get("executable"):
            lech.append((e, s, x.get("pred_xy"), y.get("pred_xy"), x.get("executable"), y.get("executable")))
    print(f"[kiểm dùng lại] {len(chua) - len(lech)}/{len(chua)} bước trùng tuyệt đối", lech[:3], flush=True)
    assert len(lech) <= 1, "DỪNG: bộ chấm không tái lập bản cũ, không được dùng số gieo"


if __name__ == "__main__":
    main()
