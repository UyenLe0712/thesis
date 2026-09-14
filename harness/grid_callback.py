# -*- coding: utf-8 -*-
"""Copy RIÊNG tệp adapter sang grid/ sau mỗi lần lưu — biến một lượt A100 thành 40 quan sát.

Thi hành mã ③ của `report/151` §4. Dùng kèm `chay_vissft.py`.

Vì sao cần: `save_total_limit: 2` xoá checkpoint cũ như thường lệ, nhưng lưới điểm lưu để quét
thì phải còn nguyên. Chỉ copy tệp adapter (~60 MB) chứ không copy cả checkpoint (~220 MB), vì
không cần kéo theo trạng thái bộ tối ưu.

⛔⛔ ĐỊNH NGHĨA XONG LÀ CHƯA ĐỦ — PHẢI ĐĂNG KÝ, nếu không nó không bao giờ chạy.
   `llamafactory-cli train cfg.yaml` KHÔNG tự quét thư mục tìm tệp này và không có khoá YAML nào
   nạp callback ngoài. Lượt train sẽ chạy trơn tru, tốn đủ giờ GPU, và grid/ rỗng — mất trắng 40
   quan sát mà không có lỗi nào báo. Gọi bằng `chay_vissft.py`, đừng gọi llamafactory-cli.

Ba điểm đã đối chiếu thẳng với mã transformers, không phải suy đoán:
 · thư mục tên đúng là checkpoint-{global_step}      (trainer.py, PREFIX_CHECKPOINT_DIR)
 · nó nằm thẳng dưới args.output_dir                 (nhánh không dò siêu tham số — đúng ca này)
 · save_total_limit không xoá mất bản vừa ghi trước khi ta copy, vì việc xoay vòng nằm trong
   _save_checkpoint còn on_save được gọi sau đó.
"""
import os, glob, shutil
from transformers import TrainerCallback


class CopyAdapterToGrid(TrainerCallback):
    def __init__(self, grid_dir):
        self.grid = grid_dir
        os.makedirs(grid_dir, exist_ok=True)

    def on_save(self, args, state, control, **kw):
        src = os.path.join(args.output_dir, f"checkpoint-{state.global_step}")
        dst = os.path.join(self.grid, f"step{state.global_step:05d}")
        try:
            os.makedirs(dst, exist_ok=True)
            # bắt CẢ .safetensors (PEFT mới) LẪN .bin (PEFT cũ) — đừng kết tên cứng
            ten = (glob.glob(os.path.join(src, "adapter_model.*"))
                   + glob.glob(os.path.join(src, "adapter_config.json")))
            if not ten:
                print(f"[grid] CẢNH BÁO bước {state.global_step}: không thấy adapter ở {src}",
                      flush=True)
            for p in ten:
                shutil.copy2(p, dst)
            if ten:
                print(f"[grid] bước {state.global_step}: đã copy {len(ten)} tệp → {dst}",
                      flush=True)
        except Exception as e:                 # ⛔ KHÔNG bao giờ để nó giết lượt train
            print(f"[grid] bỏ qua bước {state.global_step}: {e}", flush=True)
        return control
