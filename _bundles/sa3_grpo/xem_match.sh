#!/bin/bash
# Xem tiến độ SPICE-MATCH trên Colab (phiên CLI "match"). Chạy: ! bash _bundles/sa3_grpo/xem_match.sh
for lan in 1 2 3; do
OUT=$(timeout 90 colab ssh -s match -- '
L=/kaggle/working/sa3_spicematch_101/train.log
n=$(grep -c "^\[SPICE-MATCH\] lần" $L)
t=$(grep -o "step_time.: .[0-9.]*" $L | tail -20 | grep -o "[0-9.]*$" | awk "{s+=\$1} END {if (NR) printf \"%.0f\", s/NR}")
echo "Đã train: $n / 500 update"
echo "Tốc độ: ${t:-?} giây/update · còn khoảng $(( (500-n)*${t:-85}/3600 )) giờ $(( (500-n)*${t:-85}%3600/60 )) phút"
echo "Điểm lưu trên Drive: $(ls /content/drive/MyDrive/thesis/colab_kaggle/sa3-match-c-1/sa3_spicematch_101 2>/dev/null | grep checkpoint | tr "\n" " ")"
echo "Thưởng 5 lần gần nhất: $(grep "^\[SPICE-MATCH\] lần" $L | tail -5 | grep -o "thưởng TB [0-9.]*" | grep -o "[0-9.]*$" | tr "\n" " ")"
grep -E "Traceback|OutOfMemory|STOP|nan" $L | tail -2
echo "GPU: $(nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader)"
' 2>&1 | grep -v "exited with")
echo "$OUT" | grep -q "Đã train" && { echo "$OUT"; break; }
echo "(kết nối rớt, thử lại lần $((lan+1))...)"; sleep 5
done
timeout 60 colab usage 2>&1 | grep -E "balance|rate"
