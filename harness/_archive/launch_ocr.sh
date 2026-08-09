#!/usr/bin/env bash
cd /mnt/d/Master/Thesis
SP=/tmp/claude-1000/-mnt-d-Master-Thesis/09f4f22c-bd17-4b24-808b-6d65fb3ee3dd/scratchpad
PY=$HOME/.venvs/thesis/bin/python
for k in 0 1 2 3 4 5; do
  nohup "$PY" harness/prep_ocr_train.py --split test --shard "$k" --nshard 6 \
      > "$SP/ocr_t$k.log" 2>&1 &
  echo "mảnh $k -> PID $!"
done
