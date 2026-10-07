exec(open("/mnt/d/Master/Thesis/harness/cong_metric_cau.py").read().split("per = {}")[0])
import itertools
per = {n: list(Cider().compute_score(g, ht[n])[1]) for n in names}
# 1) cặp câu KHÁC nhau cùng bước, exec khác nhau: CIDEr xếp ngược exec bao nhiêu?
tot = nguoc = hoa = 0
for i in range(N):
    for a, b in itertools.combinations(names, 2):
        if hyp[a][i] == hyp[b][i] or ex[a][i] == ex[b][i]: continue
        tot += 1
        da = per[a][i] - per[b][i]
        if abs(da) < 1e-9: hoa += 1
        elif (da > 0) != (ex[a][i] > ex[b][i]): nguoc += 1
print(f"cặp khác câu, khác exec: {tot} · CIDEr xếp NGƯỢC exec: {100*nguoc/tot:.1f}% · hoà: {100*hoa/tot:.1f}%")
# 2) trong các bước S1 trượt: câu CIDEr cao nhất của 7 nhánh có trỏ trúng không
def orc(key): return [max(names, key=lambda n: key(n, i)) for i in range(N)]
o_c = orc(lambda n, i: (per[n][i], n == "S1/101"))
o_lex = orc(lambda n, i: (ex[n][i], per[n][i], n == "S1/101"))
print("oracle CIDEr-only      :", corpus(o_c))
print("oracle exec→CIDEr (lex):", corpus(o_lex))
same = [i for i in range(N) if ex[o_c[i]][i] == 0 and any(ex[n][i] for n in names)]
print(f"bước có ≥1 câu trúng nhưng câu CIDEr-cao-nhất lại TRƯỢT: {len(same)} ({100*len(same)/N:.1f}%)")
# 3) chỉ trong 2 hạt S1 (proxy 'mẫu của cùng một mô hình')
S = ["S1/101", "S1/202"]
o2c = [max(S, key=lambda n: (per[n][i], n == "S1/101")) for i in range(N)]
o2l = [max(S, key=lambda n: (ex[n][i], per[n][i], n == "S1/101")) for i in range(N)]
print("2 hạt S1, CIDEr-only:", corpus(o2c), "· lex:", corpus(o2l))
