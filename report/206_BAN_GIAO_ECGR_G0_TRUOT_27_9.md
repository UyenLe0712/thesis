# 206 — Bàn giao: ECGR đề xuất 27/9 ⇒ G0 TRƯỢT, DỪNG ngay ở cổng đầu

Nguồn: `harness/tai_lieu_2026-09-27/226_BRIEF_ECGR_CHO_CHAT_LAM_27_9.md` (chép từ 7 ảnh, ZIP nguồn
đã xoá sau khi trích xuất — xem `harness/tai_lieu_2026-09-27/README.md`). Chi phí: 0 GPU, ~1 giây
CPU.

## 1. Đề xuất là gì

**ECGR** (Element-Consistent GUI Refinement) = nền hai lượt kiểu **MM-SeR** (Song et al., CVPR
2026 poster — lượt 1 sinh câu nháp, SeR-Connector nối đặc trưng ViT nhiều tầng, lượt 2 viết lại cả
câu) **cộng một module mới: Element-Consistency Gate (ECG)** — một cổng $g \in [0,1]$ so khớp phần
tử model định chạm ($q$) với phần tử câu nháp đang gọi ($p$); $g$ nhỏ thì giữ câu nháp (không chạy
lượt 2), $g$ lớn mới cho viết lại. Backbone giữ Qwen2.5-VL-3B-Instruct + QLoRA, train lại từ gốc
(không tiếp tục từ S1/S2/MIN-DESC). Chi tiết công thức, loss, bảng ablation dự kiến: xem file 226.

Mốc cần vượt: **S1/101** (BLEU-4 51,56 · CIDEr-D 416,12 · SPICE 44,37 · BERTScore 66,33), không
phải MIN-DESC hay GRPO. Nếu ECGR chỉ hơn S1 mà bằng MM-SeR-không-cổng, phần tăng thuộc MM-SeR,
không phải ECG.

## 2. Việc đã làm: cổng G0 (0 GPU)

G0 hỏi: trong các bước S1 sai câu tham chiếu đúng **một khối duy nhất** ("one-block" — chỉ một
opcode `replace/delete/insert` khác `equal`, ≤1 token mới, ≥3 token giữ nguyên — tức lỗi *cách
diễn đạt gần đúng*, không phải trật khác hẳn), có đủ dày bước mà **bộ trỏ đọc câu model ra sai vị
trí** (`hit_disk=0`) hay không. Logic: nếu phần lớn nhóm này vẫn `hit_disk=1` (bộ trỏ vẫn tìm đúng
phần tử dù câu hơi khác chữ), nghĩa là lỗi chỉ nằm ở *cách nói*, không nằm ở *chỉ sai phần tử* — mà
ECG chỉ can thiệp được vào loại lỗi thứ hai. Ngưỡng khoá trước: **≥ 250/958** thì ĐẠT.

Chạy verbatim script trong file 226 (Phụ lục A) trên `runs/score_s1_seed101_raw.jsonl` (4.463 bước,
S1 hạt giống 101):

```
n 4463
exact 954 21.38
one_block 958
one_block_hit_disk_0 147
G0 TRUOT
```

Ba số đối chiếu (n=4463, exact=954, one_block=958) khớp tuyệt đối kỳ vọng ghi sẵn trong tài liệu
gốc ⇒ script tin được.

**one_block_hit_disk_0 = 147/958 (15,34%), KTC95 bootstrap cụm theo `episode_id` [13,12% ; 17,65%]
(652 episode)** — thấp hơn ngưỡng 250 rất xa, kể cả mép trên KTC95 (~169 câu) cũng chưa chạm ngưỡng.

Phân rã (không nhánh nào giải thích được khoảng cách tới ngưỡng):
- theo opcode: replace 15,48% (491) · delete 14,85% (377) · insert 16,67% (90) — gần như bằng nhau.
- theo `action_ok`: 1 → 15,29% (955); 0 → n=3, quá nhỏ để đọc.
- theo app: không app nào trong top-10 (7–12 câu một-block/app) tập trung đủ lỗi để kéo tổng lên.

Đọc 20 ví dụ ngẫu nhiên (seed 20260927): nhóm `hit_disk=0` phần lớn là đổi mạo từ / "option"↔"list"
/ rút gọn cụm vị trí — đúng như tài liệu gốc lo ngại ("lỗi chủ yếu là cách nói"), chỉ 2/10 ví dụ là
gọi sai hẳn phần tử.

## 3. Phán quyết

**G0 TRƯỢT, không sát ngưỡng.** Theo đúng luật đã khoá trước trong tài liệu gốc (mục 0.3, mục 8,
mục 10): trượt một cổng thì **dừng ngay**, không chạy G1 (vốn cũng không chạy được — kho này không
có checkpoint/pilot xuất được vector $(q,p)$), không đổi sang pointer/crop/retrieval/fine-tune,
không train ECG dưới bất kỳ hình thức nào.

⇒ **ECGR đóng lại ở cổng G0, 27/9/2026.** Không phải kết quả âm cần báo trong luận văn (đây là một
đề xuất mới chưa từng vào bài, không phải nhánh đã đăng ký trước theo `report/106`) — chỉ là một
hướng đã cân nhắc và loại trước khi tốn GPU.

## 4. File liên quan

| việc | đường dẫn |
|---|---|
| Brief gốc (chép từ 7 ảnh) | `harness/tai_lieu_2026-09-27/226_BRIEF_ECGR_CHO_CHAT_LAM_27_9.md` |
| Ảnh gốc | `harness/tai_lieu_2026-09-27/anh_goc/` |
| Kết quả G0 đầy đủ (bảng, phân rã, 20 ví dụ, script) | `/mnt/d/Master/ECGR_G0_27_9/ket_qua_g0_ecgr.md` (ngoài kho git, theo đúng mục 6/8 của brief gốc) |
| Script G0 | verbatim trong hai file trên; không thêm bản thứ ba |

## 5. Dọn dẹp cùng lượt (không liên quan ECGR, gộp chung vì cùng phiên)

- Xoá 4 ZIP "My Documents"/`p1_out.zip` đã xử lý xong: nội dung đã nằm ở
  `harness/tai_lieu_2026-09-25/anh_goc/`, `paper/soict2026/guistep/`, `runs/pata/p1/`.
- **Vá lỗi `.gitignore`:** dòng `runs/noisuy/*/adapter_model.safetensors   # ở GitHub Release …` có
  comment nối trực tiếp sau pattern trên cùng dòng — `.gitignore` không có cú pháp comment cuối
  dòng, nên toàn bộ chuỗi kể cả phần `# ở GitHub Release …` bị hiểu là một phần của pattern, và
  pattern đó không bao giờ khớp file thật. Hệ quả: 5 tệp `adapter_model.safetensors` (119,8 MB/tệp,
  vượt trần 100 MB của GitHub) **chưa từng được git bỏ qua thật sự**, dù `CLAUDE.md` đã ghi "đã vào
  .gitignore" từ 22/9. Đã tách comment ra dòng riêng, `git check-ignore` xác nhận khớp lại.
