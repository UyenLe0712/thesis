# Sự kiện đầu vào cho debate (số TEST, tính 15/11 từ runs/sa_spice_v3/test/, bootstrap cụm app B=2000, p McNemar chính xác)

SA-SPICE-v3 ck400 (GRPO từ SFT-cont, 1.000 câu nhắc TRAIN-v3, seed 101, điểm lưu chọn trên DEV-v3 theo tiêu chí khả thi, chấm test MỘT lần):
- exec (Voronoi, 4.463 bước chạm) **61,21** [59,45; 62,92]; D.3 67,56; AitW đầy đủ 77,12; action_ok 95,79.
- Cao nhất trong mọi nhánh RL đã chấm test (ck500 60,65 · ACE 60,68 · ROUGE-L 60,63 · SCST 60,54 · SFT tiếp 60,16 · A/A 59,74 · S1/101 59,11).

Ghép cặp exec (Δ [KTC95] cứu/phá p):
- SA − SFT-cont (cùng điểm xuất phát, mốc đúng): +1,05 [+0,47; +1,65] 116/69 p=6,8e−4 (D.3 +0,92*, AitW +1,41*)
- SA − ck500 (GRPO+SPICE từ S1): +0,56 [−0,04; +1,19] 100/75 p=0,069 (D.3 +0,54 ns, AitW +0,87*)
- SA − S1/101: +2,11 [+1,31; +2,89] 181/87 p=9,5e−9 (D.3 +2,06*, AitW +2,76*). MDE thiết kế 2,11.
- SA − A/A (GRPO+SPICE chạy lại): +1,48*; SA − ck500 hạt 202: +1,28*; SA − ROUGE-L +0,58 [+0,04; +1,17] p=0,048; SA − SCST+SPICE +0,67*; SA − ACE +0,54 ns.
- Dev đã dự báo SA ck400 − SFT-cont +1,35 (dev); test ra +1,05 ⇒ lần này dev chuyển sang test khá tốt.

Bước không chạm (2.495 bước, tỉ lệ đúng loại thao tác, strict_back):
- toàn bộ: SA 84,05 · SFT-cont 84,61 · ck500 84,29 · S1 85,97. SA − SFT-cont −0,56 [−1,43; +0,33] ns; SA − S1 −1,92 [−2,96; −0,79] (qua ngưỡng không gây hại −3).
- navigate_back (n=270): SA 58,52 · SFT-cont 71,11 · ck500 67,04 · S1 72,96. SA − SFT-cont **−12,59 [−16,80; −8,49]** cứu 3 phá 37; SA − ck500 −8,52*.
- scroll (n=755): SA 80,00 · SFT-cont 76,82 · ck500 77,75 · S1 83,97. SA − SFT-cont +3,18*; SA − ck500 +2,25*.
- wait SA − SFT-cont −1,39*; open_app +0,85*; input_text ≈ 0.
- 37 câu back bị phá: 33 thành câu chạm ("Click on the close icon…", "Click on the screen", "Open the X app"), 4 thành scroll. SFT-cont viết đúng "Go back to the previous page" ở cùng bước.
- TRAIN-v3 chỉ có 39/1.000 câu nhắc back (3,9%). Verifier v3: gold back bấm mũi tên ↔ "go back" ⇒ A=0,5; khác loại ⇒ A=0,5 (không phạt).

Chưa có: độ đo văn bản test của SA ck400 (cần kernel CPU SPICE); chrF arm KHÔNG chấm test (trượt tiêu chí khả thi DEV); không có arm GRPO+SPICE-thuần từ SFT-cont (SPICE-MATCH) ⇒ chưa tách được công của thành phần composite so với SPICE thuần ở cùng điểm xuất phát; chỉ một seed (101), memo gốc đòi 3 seed (401/503/907); biến thiên A/A ~0,9 exec.

Bối cảnh khác: user muốn "hợp lý và làm số cải thiện nhất"; phải giữ GRPO + SPICE làm lõi; bảo vệ dời 3/2027; ngân sách không thành vấn đề; Kaggle T4 miễn phí 30 h/tuần × 3 tài khoản. Báo cáo nghiên cứu trước (trước khi có số test) ở /mnt/d/Master/Thesis/reports/Reward thay thế SA SPICE v3.md, ghi chú ở /mnt/d/Master/Thesis/research_notes/Reward thay thế SA SPICE v3/.
