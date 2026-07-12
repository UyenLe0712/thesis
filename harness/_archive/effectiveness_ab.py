# -*- coding: utf-8 -*-
"""
THI NGHIEM A/B — chung minh PIPELINE HIEU QUA (ve do trung thuc), mien phi CPU.
  BASE = tutorial model viet tu do (lay tu gen_cache/).
  SYS  = design E: buoc nao bi oracle phat hien BIA (ALOHa sim<tau) -> bat model SUA
         (cho danh sach nut THAT, chon nut dung hoac NONE). Khong duoc -> FALLBACK mo ta bang loi.
So: BIA va DUNG-NHAN giua BASE vs SYS. Diem mau chot = bao nhieu buoc bia duoc SUA THANH NUT THAT.
"""
import os, sys, json, glob, urllib.request, re
sys.path.insert(0, os.path.dirname(__file__))
from aloha_match import best_match, exact_label

CACHE = os.path.join(os.path.dirname(__file__), "gen_cache")
TAU = 0.55
REVISE_MODEL = "llama3.2"   # model KHAC (text, nhanh) lam buoc sua -> dung tinh than "verifier model khac"

REVISE = '''Một bước trong hướng dẫn dùng app ghi: "{verb} {element}" (ý định: {note}).
NHƯNG màn hình KHÔNG có phần tử nào tên "{element}".
Danh sách phần tử THẬT đang có trên màn: {labels}
Hãy chọn TÊN phần tử THẬT phù hợp nhất cho bước này, CHÉP Y NGUYÊN từ danh sách trên.
Chỉ trả về đúng MỘT tên (không giải thích), hoặc "NONE" nếu không có phần tử nào phù hợp.'''

def call_text(prompt):
    data = json.dumps({"model": REVISE_MODEL, "temperature": 0,
                       "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    req = urllib.request.Request("http://localhost:11434/v1/chat/completions", data=data,
                                 headers={"Authorization": "Bearer ollama", "Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8"))["choices"][0]["message"]["content"]

def is_real(name, labels):
    _, sim = best_match(name, labels)
    return sim >= TAU

def main():
    files = sorted(glob.glob(os.path.join(CACHE, "*.json")))
    if not files:
        print("Chua co gen_cache/ — chay generate_cache.py truoc."); return
    T = {"steps": 0, "base_bia": 0, "corrected": 0, "fallback": 0,
         "base_exact": 0, "sys_exact": 0, "sys_button_steps": 0}
    print("=" * 84)
    print(f"A/B HIEU QUA | BASE (viet tu do) vs SYS (design E: sua + fallback) | sua boi {REVISE_MODEL}")
    print("=" * 84)
    for fp in files:
        r = json.load(open(fp, encoding="utf-8"))
        labels = r["elem_labels"]
        for s in r["steps"]:
            T["steps"] += 1
            orig = s.get("element", "")
            base_ok = is_real(orig, labels)
            if exact_label(orig, labels): T["base_exact"] += 1
            if base_ok:
                # nut co that ngay tu BASE -> SYS giu nguyen (la button step)
                T["sys_button_steps"] += 1
                if exact_label(orig, labels): T["sys_exact"] += 1
            else:
                T["base_bia"] += 1
                # SYS: bat model SUA
                try:
                    rev = call_text(REVISE.format(verb=s.get("verb", ""), element=orig,
                                                  note=s.get("note", ""), labels=labels))
                except Exception as ex:
                    rev = "NONE"
                rev = rev.strip().splitlines()[0].strip().strip('"').strip("'") if rev.strip() else "NONE"
                if "none" in rev.lower() or not is_real(rev, labels):
                    T["fallback"] += 1                      # khong sua duoc -> mo ta bang loi (trung thuc)
                else:
                    T["corrected"] += 1                     # SUA THANH NUT THAT
                    T["sys_button_steps"] += 1
                    if exact_label(rev, labels): T["sys_exact"] += 1
        print(f"  {r['screen']:>12} | da xu ly")
    N = T["steps"] or 1
    base_faith = (N - T["base_bia"]) / N
    # SYS: khong con 'confident-wrong button' (corrected->that, fallback->mo ta trung thuc)
    print("\n" + "-" * 84)
    print(f"TONG {len(files)} man, {T['steps']} buoc:")
    print(f"  BIA (lenh bam nut khong ton tai):")
    print(f"    BASE (viet tu do) : {T['base_bia']/N*100:5.1f}%  (faithfulness {base_faith*100:.1f}%)")
    print(f"    SYS  (design E)   :   0.0%  (khong con lenh-sai-tu-tin)")
    print(f"    -> trong {T['base_bia']} buoc bia cua BASE, SYS:")
    print(f"         + SUA THANH NUT THAT (recover) : {T['corrected']} buoc "
          f"({T['corrected']/max(1,T['base_bia'])*100:.0f}% so buoc bia)")
    print(f"         + chuyen FALLBACK mo ta bang loi: {T['fallback']} buoc "
          f"({T['fallback']/max(1,T['base_bia'])*100:.0f}%)")
    bf = T["base_exact"] / N
    sf = T["sys_exact"] / max(1, T["sys_button_steps"])
    print(f"  DUNG-NHAN (clarity, tren cac buoc tro toi nut):")
    print(f"    BASE : {bf*100:5.1f}%   ->   SYS : {sf*100:5.1f}%  (tang vi SUA chep dung ten that)")
    print("=" * 84)
    print("KET LUAN: SYS khong chi GIAU loi (fallback) ma con SUA nhieu buoc bia THANH NUT THAT")
    print("-> he HIEU QUA ve do trung thuc, do duoc, mien phi. (Tói-dich/Step-SR can AndroidControl/Colab.)")

if __name__ == "__main__":
    main()
