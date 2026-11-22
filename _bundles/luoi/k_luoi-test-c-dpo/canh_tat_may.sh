#!/bin/bash
# Canh lượt test DPO trên Colab (22/11): xong hoặc lỗi thì tải kết quả + TẮT MÁY, không cần người.
# Tín hiệu chính: tiến trình `colab exec` kết thúc (xong hay lỗi đều thoát). Hạn chót 04:00 VN tắt máy bất kể.
cd /mnt/d/Master/Thesis
L=~/colab_logs/dpo_exec.log; OUT=runs/luoi/20_11/luoi-test-c-dpo; mkdir -p $OUT
NK=$OUT/canh_tat_may.log; log(){ echo "$(TZ='Asia/Ho_Chi_Minh' date +%H:%M:%S) $*" | tee -a $NK; }
HAN=$(TZ='Asia/Ho_Chi_Minh' date -d "2026-11-23 04:00" +%s)
log "bat dau canh"
while pgrep -f "colab exec -s dpo" >/dev/null && [ $(date +%s) -lt $HAN ]; do sleep 60; done
if pgrep -f "colab exec -s dpo" >/dev/null; then log "HET HAN 04:00 ma chua xong ⇒ tat may (ket qua toi lan dong bo Drive gan nhat van con)"; LYDO=han
elif tr -d '\r' < $L | grep -q "XONG CA NOTEBOOK"; then log "notebook XONG"; LYDO=xong
else log "colab exec thoat KHONG co dong XONG (loi hoac mat ket noi)"; LYDO=loi; fi
# 22/11: lần đầu chỉ là CLI mất kết nối (RuntimeError: Connection was lost) trong khi máy vẫn sinh câu tốt
# ⇒ trước khi tắt, kiểm máy còn chạy không: dấu vân tay = danh sách tệp + đuôi log sinh câu trên máy.
if [ $LYDO = loi ] && tr -d '\r' < $L | grep -q "Connection was lost"; then
  dau(){ { timeout 120 colab ls -s dpo /kaggle/working 2>/dev/null; timeout 120 colab download -s dpo /kaggle/working/gen_dpo_on_spice_101.log /tmp/canh_gen.log >/dev/null 2>&1 && tail -2 /tmp/canh_gen.log; } | md5sum | cut -c1-12; }
  A=$(dau); sleep 300; B=$(dau)
  if [ "$A" != "$B" ]; then
    log "may VAN CHAY (chi mat ket noi CLI) ⇒ canh tu xa moi 5 phut"; LAST=$(date +%s); LYDO=han
    while [ $(date +%s) -lt $HAN ]; do
      if timeout 120 colab ls -s dpo /kaggle/working 2>/dev/null | grep -q "ket_qua_test.zip"; then sleep 120; log "thay ket_qua_test.zip ⇒ XONG"; LYDO=xong; break; fi
      C=$(dau); if [ "$C" != "$B" ]; then B=$C; LAST=$(date +%s); fi
      if [ $(( $(date +%s) - LAST )) -gt 3600 ]; then log "60 phut khong doi gi tren may ⇒ coi nhu treo"; LYDO=loi; break; fi
      sleep 300
    done
  else log "may cung dung (5 phut khong doi) ⇒ tat"; fi
fi
tr -d '\r' < $L | grep -v "^\s*$" | cut -c1-200 | tail -15 >> $NK
# tải kết quả (mỗi lệnh có timeout; hỏng cũng đi tiếp tới bước tắt máy)
if [ $LYDO = xong ]; then
  timeout 600 colab download -s dpo /kaggle/working/ket_qua_test.zip $OUT/ket_qua_test.zip >>$NK 2>&1 && log "tai zip OK $(du -h $OUT/ket_qua_test.zip | cut -f1)" || log "tai zip HONG (Drive van co ban dong bo)"
  timeout 300 colab exec -s dpo --timeout 120 -f _bundles/luoi/k_luoi-test-c-dpo/xoa_s1_drive.py >>$NK 2>&1 || log "xoa s1_merged tren Drive HONG"
else
  for f in pred_dpo_on_spice_101_test.jsonl gen_dpo_on_spice_101.log; do
    timeout 300 colab download -s dpo /kaggle/working/$f $OUT/$f >>$NK 2>&1 && log "tai $f OK" || log "tai $f HONG"; done
fi
# TẮT MÁY: thử tới khi Active assignments = 0
for i in 1 2 3 4 5; do
  timeout 120 colab stop -s dpo >>$NK 2>&1
  sleep 20; U=$(timeout 60 colab usage 2>&1); echo "$U" | tail -3 >> $NK
  if echo "$U" | grep -q "Active assignments: 0" || ! timeout 60 colab sessions 2>/dev/null | grep -q "^\[dpo\]"; then log "DA TAT MAY ($LYDO)"; exit 0; fi
  log "chua tat duoc, thu lai ($i)"; sleep 60
done
log "⛔ KHONG TAT DUOC MAY — vao colab.research.google.com tat tay"; exit 1
