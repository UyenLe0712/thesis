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
#   bash run_on_rented.sh binfer s1 101  # nhánh B-infer: không train, nhét danh sách phần tử
#   bash run_on_rented.sh base           # mốc tham chiếu: mô hình gốc, không huấn luyện
#   bash run_on_rented.sh ceiling s1 101 # phép thử TRẦN (bước 6) + đối chứng độ dài
#   bash run_on_rented.sh noharm s2 101 s1 101   # thước phụ: không gây hại
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
  # KIỂM MÁY TRƯỚC KHI LÀM GÌ TỐN THỜI GIAN. Ba thứ dưới đây nếu sai thì hoặc hỏng phép
  # so (nhiều card → cỡ lô bị nhân lên), hoặc chết giữa chừng sau nhiều giờ (hết đĩa).
  # Biết trong 5 giây rẻ hơn biết sau 3 tiếng.
  echo "── kiểm máy ──"
  nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
  NGPU=$(nvidia-smi -L 2>/dev/null | wc -l)
  FREE=$(df -BG --output=avail "$WS" 2>/dev/null | tail -1 | tr -dc '0-9')
  FREE=${FREE:-0}
  echo "   card: $NGPU · lõi: $(nproc) · đĩa trống ở $WS: ${FREE} GB"
  if [ "$NGPU" -ne 1 ]; then
    echo "   ⚠️  THẤY $NGPU CARD. LLaMA-Factory sẽ tự chạy song song và NHÂN cỡ lô lên"
    echo "      (đo được trên Kaggle T4x2: đặt batch 1 mà nó báo Total train batch size = 2)."
    echo "      Cỡ lô hiệu dụng PHẢI giữ y hệt giữa các nhánh, nếu không hiệu số S2-S1 lẫn"
    echo "      cả phần do cỡ lô khác nhau. Đặt CUDA_VISIBLE_DEVICES=0 rồi chạy lại."
    exit 1
  fi
  if [ "$FREE" -lt 90 ]; then
    echo "   ✗ ĐĨA DƯỚI 90 GB — dừng. Đỉnh cần ~70 GB cho ảnh, cộng cache mô hình ~12 GB."
    exit 1
  fi

  echo "── cài đặt ──"
  pip install -q -U "transformers>=4.49" accelerate peft bitsandbytes datasets \
      huggingface_hub pyarrow pillow rapidocr_onnxruntime pyyaml
  [ -d "$LF" ] || git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory "$LF"
  pip install -q -e "$LF[torch,metrics]"

  echo "── kéo dữ liệu ──"
  mkdir -p "$DATA" "$CKPT"
  cd "$REPO"
  # tập dạy: 76 shard là ~67GB; mặc định lấy đủ, đổi --shards nếu muốn chạy thử trước
  python harness/build_train_data.py --shards "${SHARDS:-76}"

  # OCR — CHẠY SONG SONG THEO SỐ LÕI, đừng để rơi về một luồng.
  # Đo trên máy 8 lõi: 0,53 ảnh/giây mỗi luồng. Tập dạy đủ ~64.500 ảnh, nên một
  # luồng mất ~34 giờ còn sáu luồng mất ~5,7 giờ. Trên máy thuê tính tiền theo giờ
  # thì khoảng chênh đó là hơn 20 đô cho một việc chỉ dùng CPU, trong khi card đồ
  # hoạ nằm không. prep_ocr_train.py bỏ qua ảnh đã có kết quả nên chạy lại vô hại.
  # Số tiến trình = min(số lõi, RAM_GB/2, 24). Mỗi tiến trình RapidOCR ăn ~0,5-1 GB;
  # lấy đúng bằng số lõi trên máy nhiều lõi ít RAM là chuốc lấy OOM giữa chừng, mà OOM
  # ở đây giết cả lượt và phải chạy lại từ đầu.
  _cores=$(nproc)
  _ramgb=$(( $(awk '/MemAvailable/{print $2}' /proc/meminfo) / 1024 / 1024 ))
  _byram=$(( _ramgb / 2 )); [ "$_byram" -lt 1 ] && _byram=1
  NP=${OCR_PROCS:-$(( _cores < _byram ? _cores : _byram ))}
  [ "$NP" -gt 24 ] && NP=24
  echo "   ($_cores lõi, ${_ramgb}GB RAM trống → dùng $NP tiến trình)"
  echo "   OCR tập dạy bằng $NP luồng"
  for k in $(seq 0 $((NP - 1))); do
    python harness/prep_ocr_train.py --shard "$k" --nshard "$NP" &
  done
  wait
  python harness/prep_ocr_train.py --merge

  python harness/descriptor_label_build.py
  python harness/build_branch_data.py --img-prefix "$REPO/harness/dg1_cache/train_ac/"

  # tập kiểm: ảnh phải tải, nhưng KHÔNG OCR lại. Kết quả OCR tập kiểm đã chạy xong
  # ở máy nhà và nằm sẵn trong repo (harness/dg1_cache/test_ac/ocr.jsonl, 6.969 ảnh,
  # phủ đủ 6.958 bước). Tập kiểm đã khoá nên tệp này không đổi nữa.
  python harness/build_test_data.py --shards 9
  if [ ! -s harness/dg1_cache/test_ac/ocr.jsonl ]; then
    echo "   !! thiếu OCR tập kiểm trong repo — chạy lại, mất thêm ~6 giờ"
    for k in $(seq 0 $((NP - 1))); do
      python harness/prep_ocr_train.py --split test --shard "$k" --nshard "$NP" &
    done
    wait
    python harness/prep_ocr_train.py --split test --merge
  else
    echo "   OCR tập kiểm: dùng bản có sẵn ($(wc -l < harness/dg1_cache/test_ac/ocr.jsonl) ảnh)"
  fi

  # Nhãn "ứng dụng này đã thấy lúc dạy chưa" là HÀM CỦA TẬP DẠY THẬT SỰ DÙNG, nên chỉ
  # tính đúng được ở đây — sau khi biết dựng bao nhiêu shard. Bỏ bước này thì lát phụ
  # đã-thấy/chưa-thấy đọc theo một tập dạy khác với tập vừa train.
  python harness/tag_app_seen.py

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
  # Phép tự kiểm [3] chỉ chạy được ở đây vì cần GPU: lô 1 và lô n phải ra CÙNG câu.
  # Lệch tức đệm sai bên — lỗi không báo gì, chỉ làm điểm tụt không đều theo thứ tự
  # bản ghi. Chạy một lần trước lượt sinh đầu tiên là đủ cho mọi nhánh về sau.
  if [ ! -f "$CKPT/.selftest_batch_ok" ]; then
    python harness/infer_branch.py --selftest-batch \
        --adapter "$CKPT/${branch}_seed${seed}" --batch 8 \
      && touch "$CKPT/.selftest_batch_ok" \
      || { echo "TỰ KIỂM LÔ RỚT — dừng, đừng chấm."; exit 1; }
  fi
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

binfer)
  # Nhánh B-infer: KHÔNG huấn luyện gì thêm, dùng trọng số S1, lúc chạy nhét DANH SÁCH
  # phần tử của màn vào đầu vào. Không đánh dấu đích, không dùng toạ độ chuẩn — nhét
  # khai báo của đúng nút đích là phép thử TRẦN, một thí nghiệm khác (report/106 sửa
  # đổi 7/8 mục c).
  #   bash run_on_rented.sh binfer s1 101
  branch=${2:-s1}; seed=${3:-101}
  cd "$REPO"
  python harness/infer_branch.py --b-infer \
      --adapter "$CKPT/${branch}_seed${seed}" \
      --out "$CKPT/preds_binfer_from_${branch}_seed${seed}.jsonl" \
      ${LIMIT:+--limit $LIMIT}
  python harness/score_run.py --mode score --grounder "${GROUNDER:-uground}" \
      --preds "$CKPT/preds_binfer_from_${branch}_seed${seed}.jsonl" \
      --out "$CKPT/score_binfer_${branch}_seed${seed}.json"
  ;;

base)
  # NHÁNH THAM CHIẾU (đăng ký 9/8, report/106 mục k): mô hình GỐC, không huấn luyện gì.
  # Trả lời câu mà sáu nhánh kia không trả lời: bản thân việc SFT mua được bao nhiêu.
  # Nếu S1 xấp xỉ mốc này thì tiền đề của cả thiết kế lung lay, và nên biết TRƯỚC khi
  # diễn giải Δ giữa S1 và S2. Chỉ tốn suy luận, không tốn huấn luyện.
  #   bash run_on_rented.sh base
  cd "$REPO"
  python harness/infer_branch.py --no-adapter \
      --out "$CKPT/preds_base.jsonl" ${LIMIT:+--limit $LIMIT}
  python harness/score_run.py --mode score --grounder "${GROUNDER:-uground}" \
      --preds "$CKPT/preds_base.jsonl" --out "$CKPT/score_base.json"
  ;;

ceiling)
  # PHÉP THỬ TRẦN — report/106 mục 5 BƯỚC 6, chạy trên S1 trước khi train S2.
  # Nối khai báo CHUẨN của đúng phần tử đích vào đầu vào lúc suy luận: nếu phát không
  # công cho mô hình đúng thứ mà tầng khai báo cố sinh ra, điểm lên tới đâu. Nhánh
  # 'filler' là đối chứng độ dài — đoạn đệm vô nghĩa cùng số token, để loại khả năng
  # điểm tăng chỉ vì đầu vào dài thêm.
  #
  # ⚠ KHÔNG phải B-infer. B-infer nhét DANH SÁCH phần tử, không chỉ ra cái nào là đích.
  # Phép này nhét thẳng lời giải. Đọc lẫn hai thứ sẽ ra kết luận sai (sửa đổi 7/8 mục c).
  #   bash run_on_rented.sh ceiling s1 101
  branch=${2:-s1}; seed=${3:-101}
  cd "$REPO"
  # nhãn khai báo cho TẬP KIỂM — chỉ phép này cần, dựng một lần
  [ -s harness/dg1_cache/test_ac/descriptors.jsonl ] || \
      python harness/descriptor_label_build.py --split test
  for m in gold filler; do
    echo "── trần: $m ──"
    python harness/infer_branch.py --ceiling "$m" \
        --adapter "$CKPT/${branch}_seed${seed}" \
        --out "$CKPT/preds_ceiling_${m}_${branch}_seed${seed}.jsonl" ${LIMIT:+--limit $LIMIT}
    python harness/score_run.py --mode score --grounder "${GROUNDER:-uground}" \
        --preds "$CKPT/preds_ceiling_${m}_${branch}_seed${seed}.jsonl" \
        --out "$CKPT/score_ceiling_${m}_${branch}_seed${seed}.json"
  done
  echo "ĐỌC: hiệu số gold − filler mới là trần. gold − S1 gồm cả phần do đầu vào dài thêm."
  ;;

noharm)
  # Thước phụ BẮT BUỘC (report/106 mục 3): trên bước KHÔNG chạm, nhánh khai báo
  # không được thấp hơn nhánh nền quá 3 điểm phần trăm. Không tốn bộ trỏ nên rẻ,
  # nhưng thiếu nó là thiếu một thước đã đăng ký.
  #   bash run_on_rented.sh noharm s2 101 s1 101
  branch=${2:?}; seed=${3:?}; bbranch=${4:-s1}; bseed=${5:-101}
  cd "$REPO"
  python harness/score_run.py --mode noharm \
      --preds "$CKPT/preds_${branch}_seed${seed}.jsonl" \
      --baseline "$CKPT/preds_${bbranch}_seed${bseed}.jsonl" \
      --out "$CKPT/noharm_${branch}_seed${seed}.json"
  ;;

*)
  sed -n '1,20p' "$0"
  ;;
esac
