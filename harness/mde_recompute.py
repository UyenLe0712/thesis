# -*- coding: utf-8 -*-
"""
FREE · offline — tính lại MDE cho tử tế.

Ba lỗi của con số cũ (MDE 12.6–18.9 pp, "SD = 0.362 đo từ pilot"):
  1. 0.362 KHÔNG phải số đo — `mde_pilot.py` đặt sd_diff = √2 · sd_1arm, tức giả định hai
     nhánh độc lập. Thiết kế thật là ghép cặp trên cùng app nên độ lệch của HIỆU nhỏ hơn.
  2. Pilot chỉ ~3.5 bước mỗi app, nên phần lớn phương sai giữa các app là **nhiễu lấy mẫu**
     chứ không phải khác biệt thật giữa app. Phải trừ phần nhiễu nhị thức ra.
  3. Bảng điểm pilot còn cụm rác và app bị tách đôi (`Washington post` với
     `The Washington Post`) — đúng lỗi đã sửa cho G nhưng chưa sửa ngược cho SD.

Chạy: ~/.venvs/thesis/bin/python harness/mde_recompute.py
"""
import os, re, json, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
PILOT = os.path.join(HERE, "mde_pilot_results.json")
ASSIGN = os.path.join(HERE, "ac_app_assign_results.json")
OUT = os.path.join(HERE, "mde_recompute_results.json")
T = 3.077

# cụm rác: tên do bộ trích cắt sai từ câu mục tiêu, không phải tên app
JUNK = {"on the pinerest", "knoxville on the cnn", "inspire in this", "in this"}


def norm(name):
    s = re.sub(r"^(the)\s+", "", (name or "").strip(), flags=re.I)
    s = re.sub(r"\s+", " ", s).strip(" .,'\"").lower()
    s = re.sub(r"\s+(app|application)$", "", s)
    # gộp vài biến thể chính tả người viết
    s = s.replace("newyork times", "nytimes").replace("new york times", "nytimes")
    s = s.replace("art & culture", "arts & culture")
    return s


def main():
    pil = json.load(open(PILOT, encoding="utf-8"))
    scores = pil["app_scores"]
    n_steps = pil.get("n_steps") or 91
    print("=" * 74)
    print(f"Pilot gốc: {len(scores)} app, điểm trung bình {pil['mean']:.3f}, "
          f"SD một nhánh {pil['sd_1arm']:.3f} (sd_diff {pil['sd_diff']:.3f} = √2 · SD, tức GIẢ ĐỊNH)")

    # gộp trùng + loại rác
    merged = {}
    for k, v in scores.items():
        nk = norm(k)
        if nk in JUNK:
            continue
        merged.setdefault(nk, []).append(v)
    clean = {k: sum(v) / len(v) for k, v in merged.items()}
    G_pilot = len(clean)
    vals = list(clean.values())
    sd_obs = st.pstdev(vals) if len(vals) > 1 else 0.0
    mean = sum(vals) / len(vals)
    print(f"Sau khi gộp trùng + bỏ cụm rác: {G_pilot} app, SD quan sát {sd_obs:.3f}")

    # trừ nhiễu lấy mẫu: mỗi app chỉ vài bước nên p̂ dao động mạnh quanh p thật
    n_bar = n_steps / max(len(scores), 1)
    var_obs = sd_obs ** 2
    var_noise = mean * (1 - mean) / max(n_bar, 1e-9)
    var_true = max(var_obs - var_noise, 0.0)
    sd_true = var_true ** 0.5
    print(f"  bước mỗi app trung bình: {n_bar:.1f}")
    print(f"  phương sai quan sát {var_obs:.4f} = phần thật {var_true:.4f} + nhiễu đo {var_noise:.4f}")
    print(f"  → SD THẬT giữa các app ≈ {sd_true:.3f} "
          f"({var_noise/max(var_obs,1e-9):.0%} phương sai quan sát chỉ là nhiễu)")

    asg = json.load(open(ASSIGN, encoding="utf-8"))
    G, Geff = asg["G"], asg["G_eff_kish"]

    print("-" * 74)
    print(f"{'kịch bản SD':44}{'G=' + str(G):>13}{'G hiệu dụng':>15}")
    rows = []
    for tag, sd in [("bảo thủ: √2 · SD quan sát (giả định độc lập)", sd_obs * 2 ** 0.5),
                    ("SD quan sát, thiết kế ghép cặp", sd_obs),
                    ("SD thật (đã trừ nhiễu đo), ghép cặp", sd_true)]:
        a, b = T * sd / G ** 0.5, T * sd / Geff ** 0.5
        rows.append({"scenario": tag, "sd": sd, "mde_G": a, "mde_Geff": b})
        print(f"{tag:44}{a*100:>12.1f}pp{b*100:>14.1f}pp")
    print("=" * 74)
    print("Đọc: con số cũ 12.6/18.9 pp ứng với dòng ĐẦU, là kịch bản bảo thủ nhất và dựa trên")
    print("một giả định chứ không phải số đo. Dải trung thực nằm giữa dòng đầu và dòng cuối.")
    print("⚠️ Pilot chỉ ~3.5 bước/app nên mọi ước lượng SD ở đây đều thô; phải đo lại với")
    print("   ít nhất 15 bước mỗi app trước khi khoá đăng ký trước.")

    json.dump({"G_pilot_clean": G_pilot, "sd_obs": sd_obs, "sd_true": sd_true,
               "var_noise_share": var_noise / max(var_obs, 1e-9), "n_bar": n_bar,
               "G": G, "G_eff": Geff, "scenarios": rows},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Đã lưu", OUT)


if __name__ == "__main__":
    main()
