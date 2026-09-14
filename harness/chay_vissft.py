# -*- coding: utf-8 -*-
"""Chạy lượt VIS-SFT kèm callback lưới điểm lưu — THAY cho `llamafactory-cli train`.

    python3 harness/chay_vissft.py

⛔ Đừng gọi `llamafactory-cli train harness/train_config_vissft.yaml`: nó không nạp
   grid_callback.py, và grid/ sẽ rỗng sau 20-37 giờ GPU mà không có lỗi nào báo.

⚠️ `run_exp` có nhận `callbacks` hay không tuỳ phiên bản LLaMA-Factory. Kiểm TRƯỚC khi đặt lượt:
       python3 -c "import inspect, llamafactory.train.tuner as t; print(inspect.signature(t.run_exp))"
   Nếu chữ ký không có `callbacks`, đường lùi rẻ và chắc: chạy llamafactory-cli như cũ, rồi mở
   một ô thứ hai chạy vòng lặp copy thư mục checkpoint-* mới xuất hiện sang grid/ mỗi 300 giây.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CFG = os.path.join(HERE, "train_config_vissft.yaml")
GRID = "/content/drive/MyDrive/thesis/ckpt/vissft_seed101/grid"   # ⛔ đường dẫn TUYỆT ĐỐI


def main():
    from llamafactory.train.tuner import run_exp
    from grid_callback import CopyAdapterToGrid

    # ⚠️ LogCallback đổi chỗ giữa các bản LLaMA-Factory. Bản pin c4e09c7cbe18 KHÔNG có
    #    llamafactory.extras.callbacks — dò vài đường, không có thì chạy không kèm nó.
    #    Mất LogCallback chỉ mất trainer_log.jsonl; ô theo dõi G7 vốn đọc log local nên
    #    không phụ thuộc tệp ấy.
    LogCallback = None
    for duong in ("llamafactory.train.callbacks", "llamafactory.extras.callbacks",
                  "llamafactory.extras.misc", "llamafactory.train.trainer_utils"):
        try:
            LogCallback = __import__(duong, fromlist=["LogCallback"]).LogCallback
            print(f"[LogCallback] {duong}", flush=True)
            break
        except (ImportError, AttributeError):
            continue
    if LogCallback is None:
        print("[LogCallback] không tìm thấy — chạy không kèm, theo dõi bằng log local", flush=True)

    cbs = [CopyAdapterToGrid(GRID)] + ([LogCallback()] if LogCallback else [])
    print(f"[cấu hình] {CFG}", flush=True)
    print(f"[lưới]     {GRID}", flush=True)

    # ⛔ run_exp nhận DICT, không nhận đường dẫn chuỗi. Truyền chuỗi thì hf_argparser làm
    #    `file_args + args` với args là str và ném TypeError: can only concatenate list
    #    (not "str") to list — lỗi nổ ở giây thứ 10, trước khi mã hoá gì.
    import yaml
    cfg = yaml.safe_load(open(CFG, encoding="utf-8"))
    run_exp(args=cfg, callbacks=cbs)


if __name__ == "__main__":
    main()
