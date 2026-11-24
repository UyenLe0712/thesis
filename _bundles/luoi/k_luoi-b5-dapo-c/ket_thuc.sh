#!/bin/bash
# Canh lượt train DAPO nối tiếp trên Colab T4 (24/11): xong / lỗi / hết hạn thì tải điểm lưu + log về máy nhà rồi TẮT MÁY.
# Tín hiệu chính: tiến trình `colab exec -s dapo` kết thúc. Mất kết nối CLI thì kiểm máy còn chạy (log train đổi) rồi canh từ xa.
cd /mnt/d/Master/Thesis
L=~/colab_logs/dapo_exec.log; OUT=runs/luoi/20_11/luoi-b5-dapo-c; mkdir -p $OUT
R=/kaggle/working/dapo_ds_spice_101_dapo
NK=$OUT/canh_tat_may.log; log(){ echo "$(TZ='Asia/Ho_Chi_Minh' date +%H:%M:%S) $*" | tee -a $NK; }
HAN=$(TZ='Asia/Ho_Chi_Minh' date -d "${HAN_VN:-2026-11-24 19:30}" +%s)
GOM=_bundles/luoi/k_luoi-b5-dapo-c/gom_ket_qua.py
log "bat dau canh"
log "ket thuc tay: colab exec da thoat, notebook XONG (pgrep cu khop nham tmux)"; LYDO=xong
tr -d '\r' < $L | grep -v "^\s*$" | cut -c1-200 | tail -15 >> $NK
# gom điểm lưu mới nhất + log thành một zip trên máy rồi tải về (hỏng vẫn đi tiếp tới bước tắt máy; Drive có bản đồng bộ)
timeout 600 colab exec -s dapo --timeout 500 -f $GOM >>$NK 2>&1 || log "gom zip HONG"
timeout 900 colab download -s dapo /kaggle/working/ket_qua_train.zip $OUT/ket_qua_train.zip >>$NK 2>&1 && log "tai zip OK $(du -h $OUT/ket_qua_train.zip | cut -f1)" || log "tai zip HONG (Drive van co ban dong bo)"
# TẮT MÁY: thử tới khi Active assignments = 0
for i in 1 2 3 4 5; do
  timeout 120 colab stop -s dapo >>$NK 2>&1
  sleep 20; U=$(timeout 60 colab usage 2>&1); echo "$U" | tail -3 >> $NK
  if echo "$U" | grep -q "Active assignments: 0" || ! timeout 60 colab sessions 2>/dev/null | grep -q "^\[dapo\]"; then log "DA TAT MAY ($LYDO)"; exit 0; fi
  log "chua tat duoc, thu lai ($i)"; sleep 60
done
log "⛔ KHONG TAT DUOC MAY — vao colab.research.google.com tat tay"; exit 1
