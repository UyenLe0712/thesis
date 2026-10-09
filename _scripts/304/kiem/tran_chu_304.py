# 304 — cận trên/cận dưới thước chữ của việc "chép câu mẫu" trên test (CPU, không mô hình).
import json, sys, collections, glob, os
J=sorted(glob.glob(os.path.expanduser("~/.jdk/jdk8*")))[-1]; os.environ["JAVA_HOME"]=J; os.environ["PATH"]=J+"/bin:"+os.environ["PATH"]
sys.path.insert(0,"_scripts/304/ra-sft-script"); import ra_exemplars as RA
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
import sacrebleu
D=json.load(open("_scripts/304/kiem/ex_test_k4_kiem.json"))
REF=[d["gold"].strip() for d in D]; T=RA.tok
tk=PTBTokenizer(); G=tk.tokenize({i:[{"caption":r}] for i,r in enumerate(REF)})
def cham(H):
    C=tk.tokenize({i:[{"caption":h}] for i,h in enumerate(H)})
    return dict(bleu4=round(100*Bleu(4).compute_score(G,C,verbose=0)[0][3],2), rougeL=round(100*Rouge().compute_score(G,C)[0],2),
                cider=round(100*Cider().compute_score(G,C)[0],2), chrf=round(sacrebleu.CHRF().corpus_score(H,[REF]).score,2))
ck=[d["ck"] for d in D]
V={"ck500":ck}
V["oracle_chep_khi_khoi_co_dich"]=[d["gold"] if any(T(e["sent"])==T(d["gold"]) for e in d["exemplars"]) else d["ck"] for d in D]
V["luon_chep_vd1"]=[d["exemplars"][0]["sent"] if d["exemplars"] else d["ck"] for d in D]
for c in (2,3):
    V[f"chep_vd1_khi_cnt>={c}"]=[d["exemplars"][0]["sent"] if d["exemplars"] and d["exemplars"][0]["cnt"]>=c else d["ck"] for d in D]
    n=sum(1 for d in D if d["exemplars"] and d["exemplars"][0]["cnt"]>=c)
    dung=sum(1 for d in D if d["exemplars"] and d["exemplars"][0]["cnt"]>=c and T(d["exemplars"][0]["sent"])==T(d["gold"]))
    ckd=sum(1 for d in D if d["exemplars"] and d["exemplars"][0]["cnt"]>=c and T(d["ck"])==T(d["gold"]))
    print(f"cnt>={c}: {n} bước · ví dụ 1 đúng chuẩn {dung} · ck500 đúng chuẩn {ckd}")
for k,H in V.items(): print(f"{k:32s}", cham(H), flush=True)
