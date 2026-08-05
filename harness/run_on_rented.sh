#!/usr/bin/env bash
# Chạy trọn quy trình trên máy thuê (vast.ai A100-80GB, ảnh nền PyTorch + CUDA).
#
# Máy thuê tính tiền theo giờ nên mọi thứ mò mẫm đều thành tiền. Script này để dán
# một lệnh là chạy, và chạy lại được sau khi máy rẻ bị ngắt giữa chừng.
#
#   bash run_on_rented.sh setup          # cài + kéo dữ liệu   (~15 phút, làm một lần)
#   bash run_on_rented.sh gate           # CỔNG A: đo sai số bộ trỏ  ← chạy TRƯỚC khi train
#   bash run_on_rented.sh train s1 101   # huấn luyện một nhánh, một hạt giống
#   bash run_on_rented.sh infer s1 101   # sinh câu trên tập kiểm
#   bash run_on_rented.sh score s1 101   # chấm
#
# TRÌNH TỰ BẮT BUỘC (report/106 mục 5), đừng đảo:
#   gate → train s1 101 → train s1 202 → infer+score cả hai → đo MDE thật
#        → khoá ngưỡng → rồi mới train s2.
set -euo pipefail

WS=${WS:-/workspace}
REPO=${REPO:-$WS/thesis}
DATA=$WS/data
CKPT=$WS/ckpt
LF=$WS/LLaMA-Factory

cmd=${1:-help}

case "$cmd" in

setup)
  echo "── cài đặt ──"
  pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets \
      huggingface_hub pyarrow pillow rapidocr_onnxruntime
  [ -d "$LF" ] || git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory "$LF"
  pip install -q -e "$LF[torch,metrics]"

  echo "── kéo dữ liệu ──"
  mkdir -p "$DATA" "$CKPT"
  cd "$REPO"
  # tập dạy: 76 shard là ~67GB; mặc định lấy đủ, đổi --shards nếu muốn chạy thử trước
  python harness/build_train_data.py --shards "${SHARDS:-76}"
  python harness/prep_ocr_train.py
  python harness/descriptor_label_build.py
  python harness/build_branch_data.py --img-prefix "$REPO/harness/dg1_cache/train_ac/"
  # tập kiểm
  python harness/build_test_data.py --shards 9
  python harness/prep_ocr_train.py --split test
  cp -r harness/dg1_cache/train_ac/branches "$DATA/"
  echo "Xong. Dữ liệu ở $DATA/branches, ảnh ở $REPO/harness/dg1_cache/"
  ;;

gate)
  # CỔNG A — điều kiện dùng thước chính: sai số trung vị ≤ 3% chiều rộng màn.
  # Rớt cổng thì KHÔNG train tiếp theo kế hoạch cũ; mở report/106 mục 8 chọn bậc dự phòng.
  echo "── cổng A: đo sai số bộ trỏ chuyên trên tập kiểm ──"
  cd "$REPO"
  python harness/score_run.py --mode gate --grounder "${GROUNDER:-uground}" \
      --n "${GATE_N:-300}" --out "$CKPT/gate_A.json" | tee "$CKPT/gate_A.log"
  echo
  echo "ĐỌC KẾT QUẢ: sai số trung vị ≤3% → chạy tiếp. >3% → dừng, xem report/106 mục 8."
  ;;

train)
  branch=${2:?thiếu tên nhánh: s1 | s2 | s2r | s2_nopoint}
  seed=${3:?thiếu hạt giống: 101 | 202 | 303}
  out="$CKPT/${branch}_seed${seed}"
  echo "── huấn luyện $branch, hạt giống $seed → $out ──"
  cd "$REPO"
  # sinh bản config riêng cho lượt này: đổi ĐÚNG ba dòng, không đụng gì khác
  python - "$branch" "$seed" "$out" "$DATA/branches" <<'PY'
import sys, yaml, os
b, s, out, dd = sys.argv[1:5]
c = yaml.safe_load(open("harness/train_config.yaml", encoding="utf-8"))
c["dataset"] = f"gui_{b}"; c["seed"] = int(s)
c["output_dir"] = out; c["dataset_dir"] = dd
os.makedirs("/tmp/cfg", exist_ok=True)
p = f"/tmp/cfg/{b}_{s}.yaml"
yaml.safe_dump(c, open(p, "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
print(p)
PY
  llamafactory-cli train "/tmp/cfg/${branch}_${seed}.yaml" 2>&1 | tee -a "$out.log"
  echo "Xong → $out"
  ;;

infer)
  branch=${2:?}; seed=${3:?}
  cd "$REPO"
  python harness/infer_branch.py \
      --adapter "$CKPT/${branch}_seed${seed}" \
      --out "$CKPT/preds_${branch}_seed${seed}.jsonl" \
      ${LIMIT:+--limit $LIMIT}
  ;;

score)
  branch=${2:?}; seed=${3:?}
  cd "$REPO"
  python harness/score_run.py --mode score \
      --grounder "${GROUNDER:-uground}" \
      --preds "$CKPT/preds_${branch}_seed${seed}.jsonl" \
      --out "$CKPT/score_${branch}_seed${seed}.json"
  ;;

*)
  sed -n '1,20p' "$0"
  ;;
esac
