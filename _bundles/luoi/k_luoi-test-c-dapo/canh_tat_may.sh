#!/bin/bash
# Canh lượt test DAPO ck500 trên Colab T4 (24/11): xong / lỗi / hết hạn thì tải kết quả rồi TẮT MÁY.
# Dựng từ canh_tat_may.sh của test DPO (22/11) + kiểm `colab usage` mỗi 5 phút + kiểm tiến trình không khớp nhầm tmux.
cd /mnt/d/Master/Thesis
S=dapo; L=~/colab_logs/dapo_exec.log; OUT=runs/luoi/20_11/luoi-test-c-dapo; mkdir -p $OUT
W=/kaggle/working; R=dapo_ds_spice_101
NK=$OUT/canh_tat_may.log; log(){ echo "$(TZ='Asia/Ho_Chi_Minh' date +%H:%M:%S) $*" | tee -a $NK; }
HAN=$(TZ='Asia/Ho_Chi_Minh' date -d "${HAN_VN:-2026-11-24 23:30}" +%s)
log "bat dau canh"
exec_song(){ pgrep -af "colab exec -s $S" | grep -qvE "^[0-9]+ (tmux|bash -c)"; }
may_con(){ timeout 60 colab usage 2>/dev/null | grep -q "Active assignments: [1-9]"; }
N=0
while exec_song && [ $(date +%s) -lt $HAN ]; do
  sleep 60; N=$((N+1))
  if [ $((N % 5)) -eq 0 ]; then
    timeout 120 colab ls -s $S $W >/dev/null 2>&1
    if ! may_con && ! may_con; then log "⛔ MAY COLAB DA MAT (Active assignments 0) — ket qua dong bo o Drive MyDrive/thesis/colab_kaggle/luoi-test-c-dapo"; exit 2; fi
  fi
done
if exec_song; then log "HET HAN ma chua xong ⇒ tai phan da co roi tat may"; LYDO=han
elif tr -d '\r' < $L | grep -q "XONG CA NOTEBOOK"; then log "notebook XONG"; LYDO=xong
else log "colab exec thoat KHONG co dong XONG (loi hoac mat ket noi)"; LYDO=loi; fi
if [ $LYDO = loi ] && tr -d '\r' < $L | grep -q "Connection was lost"; then
  dau(){ { timeout 120 colab ls -s $S $W 2>/dev/null; timeout 120 colab download -s $S $W/gen_$R.log /tmp/canh_gen_dapo.log >/dev/null 2>&1 && tail -2 /tmp/canh_gen_dapo.log; } | md5sum | cut -c1-12; }
  A=$(dau); sleep 300; B=$(dau)
  if [ "$A" != "$B" ]; then
    log "may VAN CHAY (chi mat ket noi CLI) ⇒ canh tu xa moi 5 phut"; LAST=$(date +%s); LYDO=han
    while [ $(date +%s) -lt $HAN ]; do
      if timeout 120 colab ls -s $S $W 2>/dev/null | grep -q "ket_qua_test.zip"; then sleep 120; log "thay ket_qua_test.zip ⇒ XONG"; LYDO=xong; break; fi
      C=$(dau); if [ "$C" != "$B" ]; then B=$C; LAST=$(date +%s); fi
      if [ $(( $(date +%s) - LAST )) -gt 3600 ]; then log "60 phut khong doi gi tren may ⇒ coi nhu treo"; LYDO=loi; break; fi
      sleep 300
    done
  else log "may cung dung (5 phut khong doi) ⇒ tat"; fi
fi
tr -d '\r' < $L | grep -v "^\s*$" | cut -c1-200 | tail -15 >> $NK
if [ $LYDO = xong ]; then
  timeout 600 colab download -s $S $W/ket_qua_test.zip $OUT/ket_qua_test.zip >>$NK 2>&1 && log "tai zip OK $(du -h $OUT/ket_qua_test.zip | cut -f1)" || log "tai zip HONG (Drive van co ban dong bo)"
  timeout 300 colab exec -s $S --timeout 120 -f _bundles/luoi/k_luoi-test-c-dapo/xoa_s1_drive.py >>$NK 2>&1 || log "xoa s1_merged tren Drive HONG"
else
  for f in pred_${R}_test.jsonl score_${R}_test_raw.jsonl gen_$R.log; do
    timeout 300 colab download -s $S $W/$f $OUT/$f >>$NK 2>&1 && log "tai $f OK" || log "tai $f HONG"; done
fi
for i in 1 2 3 4 5; do
  timeout 120 colab stop -s $S >>$NK 2>&1
  sleep 20; U=$(timeout 60 colab usage 2>&1); echo "$U" | tail -3 >> $NK
  if echo "$U" | grep -q "Active assignments: 0" || ! timeout 60 colab sessions 2>/dev/null | grep -q "^\[$S\]"; then log "DA TAT MAY ($LYDO)"; exit 0; fi
  log "chua tat duoc, thu lai ($i)"; sleep 60
done
log "⛔ KHONG TAT DUOC MAY — vao colab.research.google.com tat tay"; exit 1
