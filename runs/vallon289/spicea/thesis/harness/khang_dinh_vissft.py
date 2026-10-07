# -*- coding: utf-8 -*-
"""Khẳng định TĨNH trước bước 1 của lượt VIS-SFT — thi hành A3 của `report/151` §1.3.

    python3 harness/khang_dinh_vissft.py          # ~5 phút, 2 lượt dựng model, 1 bước train mỗi lượt

Kiểm đúng một điều: cờ `freeze_vision_tower: false` có thật sự nối dây tới tầng thị giác không.

⛔⛔ BẢN TRƯỚC CỦA TỆP NÀY KHÔNG KIỂM ĐƯỢC GÌ, và phải ghi lại để không ai viết lại như vậy.
   Nó dựng model bằng `get_peft_model` với `target_modules` là bảy tên khối, rồi đếm tensor
   `visual.*` có `requires_grad`. Nhưng `gate_proj`/`up_proj`/`down_proj` **cũng có trong tháp thị
   giác**, nên PEFT luôn khớp chúng và phép kiểm luôn báo ĐẠT — kể cả khi LLaMA-Factory đóng băng
   thị giác. Đó là "phép thử chưa hề diễn ra mà báo như đã diễn ra", đúng dạng lỗi đã trả giá 20/8.

⭐ CÁCH ĐÚNG, và là cách tệp này làm: chạy **chính đường train thật** hai lần, một lần với cờ bật
   và một lần với cờ tắt, rồi so số tham số huấn luyện mà LLaMA-Factory tự in ra. Hai số bằng nhau
   nghĩa là cờ không có tác dụng. Phép so này tự chứng, không cần biết con số tuyệt đối nào.
   Mỗi lượt giới hạn `max_samples` nên chỉ mã hoá vài mẫu, không phải 63.000.
"""
import os, re, shutil, subprocess, sys, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(HERE, "train_config_vissft.yaml")
REPO = os.path.dirname(HERE)


def dem_tham_so(freeze, n_mau=8):
    """Chạy đúng đường train thật 1 bước, trả số tham số huấn luyện LLaMA-Factory tự in."""
    c = yaml.safe_load(open(CFG, encoding="utf-8"))
    c["freeze_vision_tower"] = freeze
    c["output_dir"] = f"/tmp/probe_g4_{freeze}"
    c["max_steps"] = 1
    c["max_samples"] = n_mau        # ⛔ không có dòng này là mã hoá 63.000 mẫu, mất ~42 phút
    c["save_steps"] = 10 ** 6       # đừng lưu gì
    c["logging_steps"] = 1
    shutil.rmtree(c["output_dir"], ignore_errors=True)
    p = f"/tmp/cfg_g4_{freeze}.yaml"
    yaml.safe_dump(c, open(p, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)

    r = subprocess.run(["llamafactory-cli", "train", p], cwd=REPO, capture_output=True,
                       text=True, env={**os.environ, "PYTHONUNBUFFERED": "1"})
    out = r.stdout + r.stderr
    m = re.search(r"trainable params:\s*([\d,]+)", out)
    if not m:
        print(out[-3000:])
        sys.exit(f"⛔ không tìm thấy dòng 'trainable params' ở lượt freeze={freeze}")
    return int(m.group(1).replace(",", "")), out


def main():
    c = yaml.safe_load(open(CFG, encoding="utf-8"))
    assert c["freeze_vision_tower"] is False, "⛔ cấu hình phải có freeze_vision_tower: false"
    print(f"[cấu hình] {CFG}")
    print(f"  lora_rank={c['lora_rank']} · lora_target={c['lora_target']}")
    print("  dựng model hai lần qua chính đường train thật, mỗi lần 1 bước…\n", flush=True)

    mo, _ = dem_tham_so(False)
    print(f"  freeze_vision_tower = false : {mo:>12,} tham số huấn luyện", flush=True)
    dong, _ = dem_tham_so(True)
    print(f"  freeze_vision_tower = true  : {dong:>12,} tham số huấn luyện", flush=True)

    chenh = mo - dong
    print(f"\n  chênh lệch                  : {chenh:>12,}"
          f"   ({100*chenh/dong:.1f}% so với nhánh đóng băng)")

    assert chenh > 0, (
        "⛔ HAI SỐ BẰNG NHAU ⇒ cờ freeze_vision_tower KHÔNG có tác dụng.\n"
        "   Chạy tiếp là 20-37 giờ A100 để lặp lại S1 dưới một cái tên khác.\n"
        "   Kiểm: lora_target có khối nào nằm trong tháp thị giác không, và bản LLaMA-Factory\n"
        "   đang dùng có đọc cờ này ở nhánh finetuning_type=lora hay không.")
    print("\n✅ ĐẠT — cờ đã nối tới tầng thị giác, được phép bắt đầu lượt train.")
    print(f"   Phần chênh {chenh:,} tham số chính là tầng thị giác được mở ra.")


if __name__ == "__main__":
    main()
