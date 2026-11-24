#!/bin/bash
# 24/11: khởi chạy lượt Colab trong tmux (sống qua việc Claude Code bị ngắt) + giữ Windows không ngủ.
# Dùng: bash chay_tmux.sh <tệp _colab_cli.py>   (máy Colab `dapo` đã tạo, Drive đã gắn, khoá Kaggle đã upload)
F=${1:?thieu tep cli}; cd /mnt/d/Master/Thesis
tmux kill-session -t dapo 2>/dev/null
[ -f ~/colab_logs/dapo_exec.log ] && mv ~/colab_logs/dapo_exec.log ~/colab_logs/dapo_exec_$(date +%H%M%S).log
tmux new-session -d -s dapo -n exec "colab exec -s dapo --timeout 0 -f $F > ~/colab_logs/dapo_exec.log 2>&1"
sleep 5
tmux new-window -t dapo -n canh "bash _bundles/luoi/k_luoi-b5-dapo-c/canh_tat_may.sh"
# giữ Windows thức (tiến trình Windows riêng, không phụ thuộc phiên Claude Code)
powershell.exe -NoProfile -Command "if (-not (Get-CimInstance Win32_Process | ? { \$_.CommandLine -like '*keepawake.ps1*' })) { Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','\\\\wsl\$\\Ubuntu\\home\\uyenle\\colab_logs\\keepawake.ps1' }" 2>&1 | tail -2
tmux list-windows -t dapo
