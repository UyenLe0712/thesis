#!/usr/bin/env bash
# Xem tiến độ OCR theo thời gian thực, ngay trong terminal. Không tốn gì cả.
#   bash harness/watch_ocr.sh          (Ctrl+C để thoát, không ảnh hưởng OCR)
cd "$(dirname "$0")/.." || exit 1
DIR=harness/dg1_cache/test_ac
TOT=$(wc -l < "$DIR/test.jsonl")
T0=$(date +%s); N0=$(cat "$DIR"/ocr.part*.jsonl 2>/dev/null | wc -l)

while true; do
  N=$(cat "$DIR"/ocr.part*.jsonl 2>/dev/null | wc -l)
  ALIVE=$(ps -eo comm=,args= | awk '$1=="python" && /prep_ocr_train/' | wc -l)
  EL=$(( $(date +%s) - T0 ))
  PCT=$(( N * 100 / TOT ))
  FILL=$(( PCT * 40 / 100 ))

  bar=""
  for ((i=0;i<40;i++)); do [ $i -lt $FILL ] && bar+="█" || bar+="░"; done

  if [ "$EL" -gt 5 ] && [ "$N" -gt "$N0" ]; then
    info=$(awk -v n=$N -v n0=$N0 -v el=$EL -v tot=$TOT 'BEGIN{
      r=(n-n0)/el; left=(tot-n)/r;
      printf "%.2f ảnh/giây   còn %d giờ %02d phút", r, left/3600, (left%3600)/60 }')
  else
    info="đang đo tốc độ..."
  fi

  printf "\033[H\033[J"
  echo "  OCR TẬP KIỂM"
  echo
  echo "  [$bar] ${PCT}%"
  echo
  printf "  %s / %s ảnh\n" "$N" "$TOT"
  echo "  $info"
  echo
  if [ "$ALIVE" -eq 0 ]; then
    echo "  ⚠ KHÔNG CÒN LUỒNG NÀO CHẠY"
    echo "    chạy lại: bash harness/launch_ocr.sh"
  else
    echo "  $ALIVE/6 luồng đang chạy"
  fi
  echo
  echo "  từng mảnh:"
  for f in "$DIR"/ocr.part*.jsonl; do
    [ -e "$f" ] || continue
    printf "    %-16s %5d\n" "$(basename "$f" .jsonl)" "$(wc -l < "$f")"
  done
  echo
  if [ "$N" -ge "$TOT" ]; then
    echo "  ✓ XONG. Việc kế:"
    echo "    python harness/prep_ocr_train.py --split test --merge"
    break
  fi
  echo "  (Ctrl+C để thoát — OCR vẫn chạy tiếp)"
  sleep 60
done
