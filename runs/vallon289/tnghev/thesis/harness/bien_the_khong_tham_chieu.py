# -*- coding: utf-8 -*-
"""FREE · 0 GPU — đo bản KHÔNG-THAM-CHIẾU của thước, và ba số độ tin cậy có điều kiện.

## Vì sao có script này

Nhan đề bài là *"A Reference-Free Metric"*, nhưng `metric_exec.score_step` nhận
`gold_instr` và **hai trong ba điều kiện đọc câu chuẩn của người**:

    action_ok = canon_action(model_instr) == canon_action(gold_instr)
    toggle_ok = not toggle_conflict(model_instr, gold_instr)

Chỉ điều kiện định vị (`hit_voronoi`) là không tham chiếu. Đây là chỗ nhan đề bán quá,
và một phản biện đọc mã sẽ bắt trong năm phút.

**Vá được mà gần như không mất gì**: loại thao tác lấy thẳng từ trường
`action.action_type` của kho — một **nhãn đã ghi lúc thu dữ liệu**, không phải câu do
người viết — nên bản này không cần câu tham chiếu nào.

⚠️ **KHÔNG đổi thước đã đăng ký.** Hồ sơ `report/106` niêm phong `metric_exec.py` từ 5/8
và nó chỉ có **một commit duy nhất**; sửa thước sau khi đã thấy điểm là đúng thứ hồ sơ
sinh ra để chặn, **kể cả khi sửa làm bài trung thực hơn**. Cách xử đúng: giữ bản đã đăng
ký làm số chính, **báo bản không-tham-chiếu như một hàng độ bền**, và sửa cách nói ở nhan
đề cho khớp thứ mã thật sự làm.

Chạy: python3 harness/bien_the_khong_tham_chieu.py
"""
import os, json, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import metric_exec as M                                            # noqa: E402

R = os.path.abspath(os.path.join(HERE, "..", "runs"))
TEST = os.path.join(HERE, "dg1_cache", "test_ac", "test.jsonl")
NHANH = [("tran", "ceiling_human"), ("s101", "s1_seed101"),
         ("s202", "s1_seed202"), ("base", "base")]
# ánh xạ nhãn kho → lớp thao tác của thước. Bước chạm chỉ có hai loại.
TU_KHO = {"click": "tap", "long_press": "long_press"}


def nap(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        o = json.loads(l)
        if "bo_qua" not in o:
            d[(o["episode_id"], o["step_id"])] = o
    return d


def main():
    T = {}
    for l in open(TEST, encoding="utf-8"):
        o = json.loads(l)
        T[(o["episode_id"], o["step_id"])] = o
    D = {n: nap(f"{R}/score_{f}_raw.jsonl") for n, f in NHANH}
    K = sorted(set.intersection(*[set(v) for v in D.values()]))
    print(f"{len(K)} bước ghép cặp bốn nhánh\n")

    print("① BẢN KHÔNG-THAM-CHIẾU — loại thao tác lấy từ `action.action_type`")
    diem = {}
    for n, _ in NHANH:
        cu = sum(D[n][k]["executable"] for k in K) / len(K) * 100
        moi = sum(1 for k in K
                  if M.canon_action(D[n][k]["sent"]) == TU_KHO.get(
                      T[k]["action"]["action_type"], "tap")
                  and D[n][k]["toggle_ok"] and D[n][k]["hit_voronoi"]) / len(K) * 100
        diem[n] = (cu, moi)
        print(f"   {n:5s} đăng ký {cu:5.2f}%  →  không tham chiếu {moi:5.2f}%  ({moi-cu:+.2f})")
    print(f"   chênh S1−Base: {diem['s101'][0]-diem['base'][0]:.2f} → "
          f"{diem['s101'][1]-diem['base'][1]:.2f} pp")
    print("   ⇒ phụ thuộc câu chuẩn là DANH NGHĨA, không thực chất")

    print("\n② Điều kiện (ii) đảo nghĩa có tác dụng đo được không?")
    for n, _ in NHANH:
        print(f"   {n:5s} toggle_ok=0 ở {sum(1 for k in K if D[n][k]['toggle_ok'] == 0):3d}"
              f"/{len(K)} bước")
    print("   ⇒ gần như trơ; phải khai, đừng trình như một cổng đang gác")

    print("\n③ ĐỘ TIN CẬY có điều kiện — κ toàn tập bị thổi bởi câu trùng byte")
    for nhan, KK in [("toàn bộ", K),
                     ("chỉ bước hai lượt viết KHÁC nhau",
                      [k for k in K if D["s101"][k]["sent"].strip()
                       != D["s202"][k]["sent"].strip()])]:
        a = sum(1 for k in KK if D["s101"][k]["executable"] == D["s202"][k]["executable"])
        p1 = sum(D["s101"][k]["executable"] for k in KK) / len(KK)
        p2 = sum(D["s202"][k]["executable"] for k in KK) / len(KK)
        po, pe = a / len(KK), p1 * p2 + (1 - p1) * (1 - p2)
        print(f"   {nhan:34s} n={len(KK):4d} · đồng thuận {po:.3f} · κ={(po-pe)/(1-pe):.3f}")
    print("   ⇒ κ=0,867 là số của một thước TẤT ĐỊNH gặp 63% câu giống hệt nhau."
          "\n     Số đáng trích là κ=0,650 trên phần hai lượt thật sự viết khác.")

    print("\n④ PHÂN TÍCH ITEM — 4.462 bước mua được bao nhiêu bước có phân biệt?")
    ba = ["tran", "s101", "base"]
    tr = [k for k in K if all(D[n][k]["executable"] == 1 for n in ba)]
    ro = [k for k in K if all(D[n][k]["executable"] == 0 for n in ba)]
    print(f"   cả ba TRÚNG  {len(tr):4d} = {len(tr)/len(K):5.1%}  ← kể cả mô hình chưa dạy")
    print(f"   cả ba TRƯỢT  {len(ro):4d} = {len(ro)/len(K):5.1%}")
    print(f"   có phân biệt {len(K)-len(tr)-len(ro):4d} = {(len(K)-len(tr)-len(ro))/len(K):5.1%}")
    print("   ⇒ 40% quần thể qua được kể cả khi chưa huấn luyện gì. Đây là dấu hiệu SÀN CAO,"
          "\n     và là lý do phép chấm `runs/floor/preds_f1_trong.jsonl` phải chạy.")


if __name__ == "__main__":
    main()
