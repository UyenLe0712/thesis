# -*- coding: utf-8 -*-
"""Chấm **loss val** cho từng điểm lưu trong `grid/` — chạy được trên Kaggle T4, 0 đồng.

Vì sao có tệp này (user chốt 10/9/2026): lượt VIS-SFT chạy với `do_eval: false`, nên không có
đường cong loss val và không biết mô hình có quá khớp hay không. Bật `do_eval` giữa lượt thì phải
dừng train, đổi cấu hình và mã hoá lại — khoảng 4 giờ trễ. Chấm ngoài như đây rẻ hơn và cho NHIỀU
hơn: phủ được cả phần đã chạy qua, và làm được cho mọi điểm lưu.

    # ở nhà, 0 GPU — dựng nhánh val một lần
    python3 harness/build_branch_data.py --recs-file val_cham400.jsonl \
        --out harness/dg1_cache/train_ac/branches_val400 \
        --img-prefix /kaggle/working/thesis/harness/dg1_cache/train_ac/

    # trên Kaggle T4
    python3 harness/loss_val_grid.py --grid <thư mục grid> \
        --branches harness/dg1_cache/train_ac/branches_val400 --every 500

⚠️ **Loss val KHÔNG thay được `exec`.** Nó chỉ đo mức khớp chuỗi đích. Dự án đã đo hệ số truyền
từ một proxy gần đích hơn nhiều (độ chính xác khai báo) xuống `exec` chỉ **0,028**. ⇒ Dùng đường
cong này để **chẩn đoán quá khớp** và để **thu hẹp vùng** cần chấm `exec`, không dùng để chọn điểm
lưu cuối cùng. Bước A6 vẫn quyết bằng `exec` trên val.
⛔ Và như mọi số val: không trích ra báo.

⚠️ T4 là Turing, KHÔNG có bf16 ⇒ script tự đổi sang fp16. Mọi điểm lưu đều chấm cùng một cách nên
so với nhau được; nhưng đừng đặt cạnh loss train của lượt A100 (bf16).
"""
import os, re, sys, json, glob, argparse

HERE = os.path.dirname(os.path.abspath(__file__))


def diem_luu(grid, every):
    """Trả [(bước, đường dẫn)] cho các thư mục stepXXXXX là bội của `every`."""
    ra = []
    for d in sorted(glob.glob(os.path.join(grid, "step*"))):
        m = re.search(r"step(\d+)$", d)
        if not m:
            continue
        b = int(m.group(1))
        if every <= 1 or b % every == 0:
            if glob.glob(os.path.join(d, "adapter_model.*")):
                ra.append((b, d))
            else:
                print(f"[bỏ] {d}: không có tệp adapter", flush=True)
    return ra


def cau_hinh(adapter, branches, out_dir, bf16, lo):
    return {
        "model_name_or_path": "Qwen/Qwen2.5-VL-3B-Instruct",
        "trust_remote_code": True,
        "image_min_pixels": 200704,
        "image_max_pixels": 1003520,
        "adapter_name_or_path": adapter,
        "stage": "sft",
        "do_train": False,
        "do_eval": True,
        "finetuning_type": "lora",
        "quantization_bit": 4,
        "quantization_method": "bnb",
        "template": "qwen2_vl",
        "cutoff_len": 2560,
        "train_on_prompt": False,
        "eval_dataset": "gui_s1",
        "dataset_dir": branches,
        "per_device_eval_batch_size": lo,
        "bf16": bf16,
        "fp16": not bf16,
        "output_dir": out_dir,
        "overwrite_output_dir": True,
        "report_to": "none",
        "preprocessing_num_workers": 2,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", required=True, help="thư mục chứa các stepXXXXX")
    ap.add_argument("--branches", required=True, help="thư mục branches_val400 (có dataset_info.json)")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "runs", "loss_val_grid.json"))
    ap.add_argument("--every", type=int, default=500,
                    help="chỉ chấm điểm lưu là bội của số này (500 = ~15 điểm cho lượt 7.876)")
    ap.add_argument("--lo", type=int, default=2, help="cỡ lô eval; T4 16 GB nên để 1-2")
    args = ap.parse_args()

    assert os.path.isfile(os.path.join(args.branches, "dataset_info.json")), \
        f"⛔ {args.branches} không có dataset_info.json — chạy build_branch_data.py trước"

    import torch
    bf16 = torch.cuda.is_bf16_supported()
    print(f"[máy] {torch.cuda.get_device_name(0)} · bf16={bf16} "
          f"⇒ dùng {'bf16' if bf16 else 'fp16'}", flush=True)

    ds = diem_luu(args.grid, args.every)
    print(f"[lưới] {len(ds)} điểm lưu sẽ chấm: {[b for b, _ in ds]}", flush=True)
    assert ds, "⛔ không có điểm lưu nào khớp --every"

    # nối tiếp được: bỏ qua bước đã có trong tệp kết quả
    xong = {}
    if os.path.exists(args.out):
        xong = {int(k): v for k, v in json.load(open(args.out)).items()}
        print(f"[nối tiếp] đã có {sorted(xong)}", flush=True)

    from llamafactory.train.tuner import run_exp
    for b, d in ds:
        if b in xong:
            continue
        od = f"/tmp/lossval_step{b:05d}"
        print(f"\n══ bước {b} · {d}", flush=True)
        try:
            run_exp(args=cau_hinh(d, args.branches, od, bf16, args.lo))
            kq = json.load(open(os.path.join(od, "all_results.json")))
            xong[b] = {k: v for k, v in kq.items() if k.startswith("eval_")}
            print(f"   loss val = {xong[b].get('eval_loss')}", flush=True)
        except Exception as e:
            print(f"   ⛔ lỗi ở bước {b}: {e}", flush=True)
            continue
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in sorted(xong.items())}, f,
                      ensure_ascii=False, indent=1)

    print("\n── ĐƯỜNG CONG LOSS VAL ──", flush=True)
    for b in sorted(xong):
        L = xong[b].get("eval_loss")
        print(f"  bước {b:5d} · loss val {L:.4f}" if L is not None else f"  bước {b:5d} · (thiếu)")
    hop_le = {b: v["eval_loss"] for b, v in xong.items() if v.get("eval_loss") is not None}
    if hop_le:
        bmin = min(hop_le, key=hop_le.get)
        print(f"\n⭐ cực tiểu tại bước {bmin} (loss {hop_le[bmin]:.4f})")
        print("   ⇒ chấm `exec` quanh mốc này ở bước A6. ⛔ Đừng chọn điểm lưu cuối cùng bằng "
              "loss val — thước quyết định vẫn là `exec`.")
    print(f"\nĐã ghi {args.out}", flush=True)


if __name__ == "__main__":
    main()
