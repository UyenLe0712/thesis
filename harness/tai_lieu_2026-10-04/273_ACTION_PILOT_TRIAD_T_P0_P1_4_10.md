# 273 — ACTION: pilot TRIAD-T trước khi chạy xác nhận (4/10/2026)

## 0. Lệnh cho chat thực thi

Đây là file duy nhất được gửi cho chat thực thi. Chat có thêm nội dung clone `thesis-master/`, nhưng không có ngữ cảnh của các cuộc trò chuyện trước.

**Nhiệm vụ:** triển khai và chạy các phép kiểm P0 theo thứ tự trong file này. Chỉ chạy P1 nếu P0 đạt cổng. Không train mô hình mới. Không chạy trên tập xác nhận 956 episode / 1.484 click. Không dùng UGround làm listener lúc suy luận.

> Kết quả mỗi pha phải được lưu dần để có thể nối tiếp khi Kaggle hết phiên. Khi kết thúc viết đúng một báo cáo bàn giao tự chứa ngoài clone:
>
> `/Users/P836901/Documents/Self-Learning/thesis/274_KET_QUA_PILOT_TRIAD_T_<ngày>.md`

Báo cáo phải in toàn bộ bảng số, cấu hình, cổng đạt/trượt và việc chưa làm. Không chỉ trỏ tới log.

## 1. Quyết định đã chốt và câu hỏi của pilot

### 1.1 Phương pháp đang kiểm: TRIAD-T

TRIAD-T là bộ chọn câu lúc suy luận, không phải editor và không đổi trọng số ck500:

1. ck500 sinh câu greedy `d0` và `N=8` câu mẫu `d1…d8`.
2. Một listener độc lập đọc từng câu trên toàn màn hình và trả điểm mà câu đó muốn người dùng chạm.
3. Locator `loc_g` đọc ảnh + goal + history và dự đoán điểm đích `t`.
4. Locator `loc_d` đọc thêm câu greedy và dự đoán điểm `t'`.
5. Giữ `d0` nếu listener của `d0` đã gần `t`, hoặc `t` và `t'` không đồng ý.
6. Chỉ đổi sang một câu mẫu nếu hai locator đồng ý và listener của câu mẫu trỏ gần `t`.
7. Không có câu đạt thì giữ nguyên `d0`.

Tên đầy đủ: **TRIAD-T — Triangulated Listener–Locator Selection with Trust gate.**

### 1.2 Vì sao phải pilot

Trên val C1 249 click, mô phỏng bằng dữ liệu có sẵn:

| cấu hình | đúng /249 | cứu / phá |
|---|---:|---:|
| ck500 | 166 | — |
| Chọn câu bằng UGround-listener theo `loc_g` | 177 | +15 / −4 |
| Thêm cổng `loc_g − loc_d` | 173 | +7 / −0 |
| Thêm câu do TAGE editor viết vào tập ứng viên | 174 | +18 / −10 |
| Chọn bằng độ giống chữ, không listener | 166 | +5 / −5 |

Nhưng phép 177/249 bị vòng tròn: UGround vừa chọn câu vừa chấm `exec`. Cả 15 ca cứu đều là ca `loc_g` đúng và câu được chọn khiến UGround trỏ tới `loc_g`. Vì vậy chưa được gọi đây là kết quả của TRIAD-T.

Pilot phải trả lời ba câu:

1. Listener **khác UGround** có hiểu các câu mẫu đủ tốt để giữ lại tín hiệu không?
2. Khi lấy mẫu từ **ck500 thật**, không phải S1 cũ, TRIAD-T có cứu nhiều hơn phá không?
3. Kết quả có cùng dấu dưới UGround, UI-Venus và kiểm tra người hay chỉ tối ưu một bộ trỏ?

## 2. Luật chống tự lừa mình

1. UGround-V1-2B chỉ là evaluator. Cấm dùng tọa độ, logit hoặc `executable` của UGround trong quyết định chọn câu lúc suy luận.
2. UI-Venus-Ground-7B là evaluator phụ. Cấm dùng nó làm listener.
3. Listener chính mặc định là ShowUI-2B. Model này không SFT trên AndroidControl và xuất điểm chuẩn hóa 0–1. Quy đổi về thang 0–1000 trước khi so.
4. Chỉ thử Phi-Ground-7B nếu ShowUI lỗi kỹ thuật, không đọc được tọa độ quá nhiều hoặc trượt cổng POA. Nếu thử Phi-Ground phải giữ và báo cả số ShowUI; không được chỉ giữ số đẹp hơn. Phi-Ground có liên hệ gián tiếp với dữ liệu OS-Atlas, phải ghi giới hạn này.
5. Không dùng UGround-7B, GUI-Actor, OS-Atlas, Jedi, UI-TARS hoặc Aguvis làm listener chính vì cùng họ/dữ liệu AndroidControl với thước chấm ở các mức khác nhau.
6. Không đưa câu do TAGE editor viết vào tập ứng viên.
7. Không dùng câu chuẩn, điểm vàng hay kết quả chấm để chọn câu ở inference. Điểm vàng chỉ dùng sau cùng để tính số cho báo cáo.
8. Mọi cấu hình đã thử phải nằm trong bảng kết quả, kể cả cấu hình xấu.
9. Tập test 4.463 click cũ đã bị xem và chỉ được dùng như dev. Không gọi kết quả P1 là test.
10. Cấm đọc/chạy tập xác nhận 1.484 click trong lượt này.

## 3. Nguồn có sẵn trong clone

Chat thực thi phải tự kiểm đường dẫn, số dòng và schema trước khi viết pipeline.

### 3.1 Val C1 và câu mẫu S1 cũ

- `runs/c1/exec8/c1data/c1_recs.jsonl`: 400 bước C1; lọc được 249 click.
- `runs/c1/exec8/c1preds/k0.jsonl`: S1 greedy.
- `runs/c1/exec8/c1preds/k1.jsonl … k8.jsonl`: tám mẫu S1 ở nhiệt độ 1,0.
- `runs/c1/exec8/c1score/score_k0_raw.jsonl … score_k8_raw.jsonl`: UGround đã chấm.
- `runs/c1/exec8/c1_exec_tong.json`: sổ tổng hợp.
- `runs/tage_val/that/score_ck500_l4_raw.jsonl`: ck500 trên 249 click, mốc 166 theo bản L4.
- `runs/tage_val/that/loc_val_g.jsonl`: locator theo goal, thang 0–1000.
- `runs/tage_val/that/loc_val_d.jsonl`: locator đọc thêm draft, thang 0–1000.

Phép kiểm toàn vẹn bắt buộc:

- đủ 249 key click `(episode_id, step_id)` ở mọi tệp dùng;
- S1 greedy 158/249;
- ck500 L4 166/249;
- `loc_g` hit đĩa 193/249;
- `loc_d` hit đĩa 190/249.

Lưu ý: ảnh C1 có thể không nằm vật lý trong clone. Cách dựng ảnh/dữ liệu Kaggle nằm trong `harness/tai_lieu_2026-10-02/265_ACTION_KIEM_THU_TAGE_VAL_2_10_checked.md` và các runbook C1.

### 3.2 ck500 và locator

- Mã ck500: `harness/grpo_spice.py`.
- Adapter ck500: dataset Kaggle `grpo-spice-ck500`, checkpoint `checkpoint-500`.
- Nền S1 đã hòa: dựng theo runbook TAGE/GRPO trong clone.
- Mã locator: `harness/tage_val.py`.
- Adapter `loc_g`, `loc_d`: dataset Kaggle `tage-adapters`.
- Trên P0, tọa độ locator C1 đã có sẵn nên không cần chạy locator lại.
- Trên P1, `loc_g` của test cũ đã có ở `runs/tage_test/loc_test.jsonl`; `loc_d` chưa có, phải chạy adapter `loc_d` trên đúng ảnh/goal/history/câu greedy ck500.

### 3.3 Evaluator

- UGround: dùng pipeline `harness/score_run.py`, cùng luật `exec` hiện hành.
- UI-Venus: runbook `harness/runbook/kaggle_phepB_uivenus.md`.
- Không thay luật ±14%, Voronoi, action type hoặc cách ghép key.

## 4. Định nghĩa thuật toán để chat tự triển khai

Tất cả tọa độ phải quy về thang 0–1000 trên ảnh gốc, không phải ảnh đã resize.

Ký hiệu:

- `L(di) = pi`: listener độc lập trỏ điểm cho câu `di`;
- `t = loc_g`;
- `t' = loc_d`;
- `near(a,b,r): |ax−bx| ≤ r và |ay−by| ≤ r`;
- `r`: bán kính câu–locator;
- `r_trust`: bán kính hai locator.

Quy tắc cho mỗi bước:

1. Nếu câu greedy không phải hành động chạm, giữ câu greedy và không chạy TRIAD-T.
2. Loại ứng viên rỗng, lặp bất thường, không phải câu chạm hoặc listener không parse được điểm.
3. Nếu `near(L(d0), t, r)`, giữ `d0`.
4. Nếu không `near(t, t', r_trust)`, giữ `d0`.
5. Lập tập `A = {di, i≥1: near(L(di), t, r)}`.
6. Nếu A rỗng, giữ `d0`.
7. Nếu A có nhiều câu, chọn câu có khoảng cách Euclid `L(di)` tới `t` nhỏ nhất; hòa thì chọn chỉ số mẫu nhỏ nhất.

Không dùng độ giống câu, SPICE, CIDEr, UGround hay câu chuẩn để phá hòa.

## 5. POA — kiểm listener độc lập bằng câu mẫu S1 có sẵn

### 5.1 Mục tiêu

Đây là phép thử rẻ để biết listener có chạy đúng trên ảnh Android dọc và có giữ được tín hiệu speaker–listener hay không. Chưa phải đánh giá phương pháp cuối vì ứng viên vẫn là mẫu S1.

### 5.2 Việc chạy

1. Chạy ShowUI-2B trên 9 câu S1 của mỗi 249 click: tổng 2.241 lời gọi listener.
2. Lưu raw output, điểm 0–1 gốc, điểm 0–1000 sau quy đổi, parse status và thời gian.
3. Chạy các nhánh cố định:
   - `B0`: ck500, không đổi;
   - `B1`: chọn theo `loc_g`, không cổng `loc_d`;
   - `B2`: TRIAD-T đầy đủ, có cổng `loc_g−loc_d`;
   - `B3`: đối chứng vòng tròn bằng UGround-listener từ file có sẵn; chỉ ghi diagnostic.
4. Với `B1/B2`, thử lưới nhỏ, chốt trước:
   - `r ∈ {40, 60, 80, 100}`;
   - `r_trust ∈ {80, 100, 140, 180}`.
5. Chấm câu cuối bằng UGround. Chỉ với cấu hình ShowUI tốt nhất theo luật §5.3, chấm thêm UI-Venus.
6. In số listener tự trỏ trúng vàng (`hit_disk`) để kiểm nó có dùng được, nhưng không lấy số này làm inference gate.

### 5.3 Luật chọn cấu hình trong POA

Trong từng `r`, với `B2`, chọn `r_trust` theo thứ tự:

1. rescue > break;
2. break ít nhất;
3. net `rescue − break` lớn nhất;
4. coverage lớn nhất;
5. nếu vẫn hòa, chọn bán kính nhỏ hơn.

Sau đó chọn `r` bằng cùng luật. Không tối ưu thước văn bản.

### 5.4 Cổng POA

Đạt mạnh khi đồng thời:

- listener parse được ≥ 98% lời gọi;
- listener standalone hit_disk ≥ 50% trên câu chuẩn/greedy thích hợp;
- `B2` có net ≥ +3 bước so với ck500;
- rescue/break ≥ 2 hoặc break = 0;
- UI-Venus không giảm quá 1 bước so với ck500 trên 249 click.

**Vùng xám** khi net là +1 hoặc +2, hoặc UI-Venus giảm đúng 2 bước: vẫn được chạy POB nhưng phải ghi **“tín hiệu yếu”**.

**Trượt** khi net ≤ 0, rescue ≤ break, parse < 95%, hoặc UI-Venus giảm ≥ 3 bước.

Nếu trượt vì lỗi parse/định dạng, sửa quy đổi tọa độ rồi chạy lại cùng model một lần. Nếu vẫn trượt, chạy Phi-Ground-7B đúng một lần với cùng lưới. Nếu cả hai trượt thì dừng toàn bộ, kết luận TRIAD-T chưa có listener độc lập dùng được; không chạy POB/P1.

## 6. POB — sinh câu mẫu từ ck500 thật

Chỉ chạy khi POA đạt mạnh hoặc vùng xám.

### 6.1 Sinh ứng viên

Trên đúng 249 click C1:

- câu mặc định là greedy ck500 đã có;
- sinh `N=8` mẫu ck500 ở `T=0,7`, `top_p=1`, `top_k=0`;
- sinh thêm `N=8` mẫu ở `T=1,0` để so nhiệt độ;
- cố định seed và ghi seed;
- không dùng S1 samples trong phương pháp cuối.

Lưu mọi câu, kể cả câu lỗi. Báo:

- số câu khác greedy;
- số câu khác nhau duy nhất trong 8 mẫu;
- tỉ lệ câu chạm hợp lệ;
- độ dài trung vị/max;
- số câu rỗng, tiếng Việt, lặp, không phải chạm.

### 6.2 Chạy listener và TRIAD-T

Chỉ dùng listener đã thắng POA. Chạy từng nhiệt độ độc lập:

- `C0`: ck500 greedy;
- `C1`: chọn theo listener–`loc_g`, không trust gate;
- `C2`: TRIAD-T đầy đủ với `loc_g−loc_d`;
- `C3`: oracle diagnostic “có ít nhất một ứng viên được UGround chấm đúng”; cấm dùng làm phương pháp.

Giữ lưới `r`, `r_trust` và luật chọn ở POA. Không chọn lại listener.

Chấm:

- UGround cho toàn bộ câu cuối;
- UI-Venus cho ck500 và hai cấu hình `C2` ở hai nhiệt độ;
- bảng cứu/phá ghép cặp;
- KTC95 bootstrap theo episode, tối thiểu 2.000 lần.

### 6.3 Cổng POB

Chọn nhiệt độ theo thứ tự:

1. TRIAD-T net lớn hơn;
2. break ít hơn;
3. UI-Venus tốt hơn;
4. nếu hòa, chọn `T=0,7`.

Đạt để lên P1 khi:

- UGround net ≥ +3 bước;
- rescue/break ≥ 1,5 và break ≤ 3;
- UI-Venus delta ≥ −1 bước;
- coverage đổi câu nằm trong 1–20%;
- oracle `C3` cao hơn ck500 ít nhất 10 bước, chứng minh pool còn headroom;
- không có lỗi ngôn ngữ nghiêm trọng.

**Vùng xám:** UGround net +1 hoặc +2, hoặc UI-Venus giảm 2 bước. Dừng và báo người dùng; không tự chạy P1 vì chi phí P1 lớn.

**Trượt:** net ≤ 0, rescue ≤ break, UI-Venus giảm ≥ 3 bước, hoặc oracle headroom < 10. Dừng TRIAD-T.

Nếu diversity quá thấp (trung vị < 3 câu khác nhau trong 8 mẫu), được thử `N=16` đúng một lần ở nhiệt độ tốt hơn. Không được thay prompt hoặc thử thêm nhiệt độ sau khi xem số.

## 7. POC — kiểm tra người trước khi mở P1

Nếu POB đạt:

1. Xuất tối đa 30 bước TRIAD-T đổi câu; nếu có ít hơn thì lấy toàn bộ.
2. Mỗi dòng phải có ảnh, goal, history, câu ck500, câu được chọn và **không hiện câu chuẩn/điểm vàng cho người chấm**.
3. Hai người chấm độc lập ba nhãn:
   - câu được chọn tốt hơn ck500;
   - tương đương;
   - tệ hơn/sai mục tiêu.
4. Báo agreement thô và Cohen's kappa nếu đủ mẫu.

**Đạt:** ≥ 70% được cả hai người xem là tốt hơn hoặc tương đương, và số “tệ hơn” ≤ 20%.

Nếu không có hai người ngay, chat chỉ chuẩn bị gói 30 bước và dừng; đây là việc cần người dùng quyết, không tự bỏ qua.

## 8. P1 — dev lớn trên test cũ 4.463 click

Chỉ chạy khi POB và POC đạt. Nếu chưa có người chấm, không tự chạy.

### 8.1 Cấu hình bị khóa từ P0

- listener;
- nhiệt độ;
- `N=8` hoặc `N=16` nếu đã kích hoạt đúng luật;
- prompt sinh;
- prompt listener;
- quy đổi tọa độ;
- tập lưới `r`, `r_trust`;
- luật lọc câu chạm.

Không đổi các mục trên sau khi nhìn P1.

### 8.2 Dữ liệu và chạy

1. Sinh mẫu ck500 cho 4.463 click của test cũ.
2. Dùng `loc_g` đã có trong `runs/tage_test/`.
3. Chạy `loc_d` trên toàn bộ bước bằng adapter trong `tage-adapters`.
4. Chạy listener độc lập trên greedy và các mẫu.
5. Chia episode tất định thành 5 fold.
6. Với mỗi fold: chọn `r`, `r_trust` trên 4 fold còn lại theo luật §5.3; áp nguyên vào fold giữ lại.
7. Ghép năm fold để có số cross-fitted. Vì đây là test cũ đã xem, vẫn phải gọi là **dev P1**.
8. Chấm UGround và UI-Venus trên câu cuối; bootstrap theo đúng cụm đang dùng trong luận văn.

### 8.3 Cổng P1

TRIAD-T được phép khóa để chuẩn bị lượt xác nhận mới khi đồng thời:

- UGround delta > 0 và cận dưới KTC95 > 0;
- rescue/break ≥ 2;
- UI-Venus delta ≥ −0,3 điểm phần trăm;
- coverage đổi câu trong 1–15%;
- không fold nào có net âm quá 0,5 điểm;
- kiểm người 60 bước đổi câu: ≥ 70% tốt hơn hoặc tương đương, ≤ 20% tệ hơn.

Nếu UGround dương nhưng KTC phủ 0: ghi **“tín hiệu chưa chắc”**; báo người dùng; không mở confirmatory. Nếu UGround tăng nhưng UI-Venus giảm quá ngưỡng hoặc người chấm trượt: coi là metric gaming, dừng.

## 9. Nếu các cổng trượt

| điểm trượt | hành động |
|---|---|
| ShowUI lỗi/parse kém | sửa quy đổi một lần; sau đó thử Phi-Ground một lần |
| Cả hai listener trượt POA | dừng TRIAD-T, giữ ck500 |
| POA đạt nhưng ck500 samples trượt POB | dừng; không được quay lại dùng S1 samples để báo kết quả |
| Diversity ck500 thấp | thử N=16 một lần; vẫn thấp thì dừng |
| UGround tăng, UI-Venus giảm | dừng vì tối ưu riêng UGround |
| Kiểm người trượt | dừng claim câu tốt hơn |
| P1 KTC phủ 0 | không mở tập xác nhận; báo người dùng |

Không tự quay lại TRACE-S/editor trong lượt này. Nếu TRIAD-T trượt, kết luận trung thực là ck500 vẫn là phương pháp cuối tốt nhất hiện có.

## 10. Thời gian và tài nguyên ước lượng

| pha | A100/L4 ước lượng |
|---|---:|
| P0A: ShowUI 2B × 2.241 lời gọi | 0,5–2 giờ |
| P0B: sinh ck500 hai nhiệt độ | 1–3 giờ |
| P0B: listener + UGround + UI-Venus | 2–5 giờ |
| P0C | thời gian người chấm |
| P1 đầy đủ nếu đạt | khoảng 1–2 ngày GPU A100; L4 chậm hơn |

Chạy smoke 10 bước trước mọi lượt dài để kiểm ảnh, prompt, parse và tọa độ. Không đọc số smoke thành kết quả.

## 11. Bảng bắt buộc trong báo cáo 274

1. Kiểm toàn vẹn dữ liệu.
2. Listener standalone: parse rate, hit_disk, latency, VRAM.
3. POA: từng `r`, `r_trust`, coverage, cứu, phá, net, UGround và UI-Venus.
4. POB: diversity theo nhiệt độ; oracle headroom; từng nhánh C0–C3; KTC theo episode.
5. Danh sách key của mọi bước đổi câu cùng ck500/câu chọn/listener point/locator points.
6. POC: bảng người chấm.
7. Nếu có P1: số từng fold, aggregate, KTC, hai evaluator và risk–coverage.
8. Phán quyết đúng luật: đạt, vùng xám hay trượt; pha nào chưa chạy và vì sao.
9. Mọi thay đổi so với action này.

## 12. Việc chat thực thi không được tự làm

- Không mở hoặc tải kết quả tập xác nhận 956 episode / 1.484 click.
- Không sửa ngưỡng sau khi xem confirmatory.
- Không dùng UGround/UI-Venus làm listener.
- Không train editor, locator hoặc ck500.
- Không đưa output TAGE editor vào pool.
- Không bỏ cổng chỉ vì nhánh không cổng có số đẹp hơn.
- Không gọi P1 là test.
- Không sửa luận văn, không commit, không push.

## 13. Việc cần người dùng quyết

1. Cung cấp/chọn GPU và các Kaggle dataset chứa adapter ck500, `tage-adapters`, ảnh C1/test.
2. Bố trí hai người chấm POC/P1.
3. Nếu POB rơi vùng xám, người dùng quyết có đáng tốn P1 hay không.
4. Nếu P1 đạt, phải viết một action mới rồi mới chuẩn bị tập xác nhận; file này không cấp phép chạy confirmatory.

## 14. Phán quyết kỳ vọng

Không hứa TRIAD-T sẽ hơn ck500. Ước lượng trước pilot:

- xác suất điểm ước trên tập xác nhận mới cao hơn ck500: khoảng 44%;
- xác suất KTC95 không phủ 0: khoảng 26%.

P0 tồn tại để loại sớm khả năng mức tăng trước đây chỉ do UGround vừa chọn vừa chấm. Nếu P0 trượt, đó là kết quả khoa học hữu ích và phải dừng, không phải lý do nới luật.
