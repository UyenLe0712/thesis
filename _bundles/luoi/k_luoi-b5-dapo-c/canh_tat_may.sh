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
# 24/11: mỗi 5 phút gọi vào máy (giữ máy "có người dùng") và kiểm máy còn không; mất máy thì ghi rõ rồi thoát
exec_song(){ pgrep -af "colab exec -s dapo" | grep -qvE "^[0-9]+ tmux"; }  # 24/11: tmux giữ nguyên dòng lệnh "colab exec" ⇒ pgrep trơn khớp nhầm, canh tới hết hạn
may_con(){ timeout 60 colab usage 2>/dev/null | grep -q "Active assignments: [1-9]"; }
N=0
while exec_song && [ $(date +%s) -lt $HAN ]; do
  sleep 60; N=$((N+1))
  if [ $((N % 5)) -eq 0 ]; then
    timeout 120 colab ls -s dapo /kaggle/working >/dev/null 2>&1
    if ! may_con && ! may_con; then log "⛔ MAY COLAB DA MAT (Active assignments 0) — xem diem luu tren Drive MyDrive/thesis/colab_kaggle/luoi-b5-dapo-c"; exit 2; fi
  fi
done
if exec_song; then log "HET HAN ma chua xong ⇒ gom diem luu moi nhat roi tat may"; LYDO=han
elif tr -d '\r' < $L | grep -q "XONG CA NOTEBOOK"; then log "notebook XONG"; LYDO=xong
else log "colab exec thoat KHONG co dong XONG (loi hoac mat ket noi)"; LYDO=loi; fi
if [ $LYDO = loi ] && tr -d '\r' < $L | grep -q "Connection was lost"; then
  dau(){ { timeout 120 colab ls -s dapo $R 2>/dev/null; timeout 120 colab download -s dapo $R/train.log /tmp/canh_dapo.log >/dev/null 2>&1 && tail -2 /tmp/canh_dapo.log; } | md5sum | cut -c1-12; }
  A=$(dau); sleep 300; B=$(dau)
  if [ "$A" != "$B" ]; then
    log "may VAN CHAY (chi mat ket noi CLI) ⇒ canh tu xa moi 5 phut"; LAST=$(date +%s); LYDO=han
    while [ $(date +%s) -lt $HAN ]; do
      if timeout 120 colab ls -s dapo $R 2>/dev/null | grep -q "checkpoint-500"; then
        timeout 120 colab download -s dapo $R/train.log /tmp/canh_dapo.log >/dev/null 2>&1
        if grep -q "^\[xong\]" /tmp/canh_dapo.log 2>/dev/null; then sleep 120; log "thay checkpoint-500 + [xong] ⇒ XONG"; LYDO=xong; break; fi
      fi
      C=$(dau); if [ "$C" != "$B" ]; then B=$C; LAST=$(date +%s); fi
      if [ $(( $(date +%s) - LAST )) -gt 3600 ]; then log "60 phut khong doi gi tren may ⇒ coi nhu treo"; LYDO=loi; break; fi
      sleep 300
    done
  else log "may cung dung (5 phut khong doi) ⇒ tat"; fi
fi
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
