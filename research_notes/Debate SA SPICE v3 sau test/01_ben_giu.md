# Bên GIỮ: không đổi reward SA-SPICE-v3 sau khi có số test (15/11/2026)

Lập trường: **giữ nguyên hàm thưởng SA-SPICE-v3** (GRPO, thưởng lấy SPICE làm lõi, α_g theo số tuple, thưởng khớp thao tác 0,2·A, phạt độ dài) làm phương pháp. Việc cần làm tiếp là **củng cố** bằng thêm hạt giống, thêm nhánh đối chứng SPICE thuần cùng điểm xuất phát, chấm độ đo văn bản trên test, và chữa bước back bằng cơ chế **ngoài hàm thưởng**. Đổi hệ số hay đổi công thức lúc này là chọn reward sau khi đã nhìn test.

Nhãn: **[test]** tập kiểm dự án (4.463 bước chạm, 2.495 bước không chạm), trích được · **[dev]** DEV-v3, chỉ để chọn, không trích · **[sàng]** sàng offline 8 mẫu SFT-cont trên TRAIN-v3 · **[tự tính]** tính hôm nay 15/11 từ tệp có sẵn, 0 GPU (script ở scratchpad, nêu ở cuối) · **[suy]** suy luận.

---

## 1. Test nói gì, đọc đúng mốc so

Mốc so đúng của SA-SPICE-v3 là **SFT-cont** (= "SFT tiếp", cùng adapter md5 `113e2a3e…`, report/333 §1), vì đó là điểm xuất phát của lượt GRPO. So với ck500 hay S1 là lệch hai biến (điểm xuất phát và tập câu nhắc).

| phép so exec (test, ghép cặp, cụm app) | Δ [KTC95] | cứu/phá | p | nguồn |
|---|---|---|---|---|
| SA ck400 − SFT-cont | **+1,05 [+0,46; +1,65]** | 116/69 | 6,8e−4 | report/334 Bảng 2.3 (B = 10.000); 00_su_kien_test.md |
| SA ck400 − ck500 | +0,56 [−0,05; +1,17] | 100/75 | 0,069 | như trên |
| SA ck400 − S1/101 | +2,11 [+1,33; +2,89] | 181/87 | 9,5e−9 | như trên |
| ck500 − SFT-cont (để đối chiếu) | +0,49 [−0,09; +1,07] | 97/75 | 0,109 | report/334 §3b |
| ROUGE-L − SFT-cont | +0,47 [−0,14; +1,08] | 101/80 | 0,137 | report/334 §3b |

Ba điều rút ra [test]:

1. **SA là lượt RL đầu tiên hơn SFT tiếp với KTC loại 0.** Trong bảng report/334 §3b có khoảng 30 nhánh so với SFT tiếp. Không nhánh RL nào trước đó (ck500, ROUGE-L, SCST, METEOR, CIDEr-D, PPO, REINFORCE, RLOO, A/A) loại được 0. Nhân p = 6,8e−4 với 30 theo Bonferroni (thô nhất) vẫn còn **0,020** [tự tính từ report/334]. Câu cũ "cấm viết GRPO + SPICE hơn SFT tiếp" (report/320 §18) là câu về ck500; với SA, câu khẳng định hẹp "GRPO với thưởng SA-SPICE-v3 hơn điểm xuất phát SFT-cont" nay có số test chống lưng.
2. **Dev chuyển sang test tốt ở lượt này:** +1,35 [dev] → +1,05 [test], cùng chiều, co lại 22%. So với các lượt trước (ck500 +2,81 val → +1,55 test, report/334 §11), đây là lần dev ít phóng đại nhất. Quy trình "chọn trên dev, chấm test một lần" đã chạy như thiết kế.
3. Cả ba thước vị trí cùng chiều so SFT-cont: D.3 +0,92*, AitW đầy đủ +1,41* (00_su_kien_test.md). Ngoài exec, SA đứng đầu cả D.3 (67,56) và D.3∧14% (63,86) trong mọi nhánh đã train (report/334 §3).

Bước không chạm [test] (đếm lại từ `runs/sa_spice_v3/test/pred_*_nontap.jsonl` bằng đúng hàm `canon_action(strict_back=True)` của `score_run.noharm`, khớp report/333 §14):

| loại | n | SFT-cont | SA ck400 | cứu / phá |
|---|---|---|---|---|
| navigate_back | 270 | 192 | 158 | 3 / 37 |
| scroll | 755 | 580 | 604 | 30 / 6 |
| wait | 505 | 483 | 476 | 2 / 9 |
| input_text | 494 | 397 | 396 | 14 / 15 |
| open_app | 469 | 457 | 461 | 4 / 0 |
| toàn bộ | 2.495 | 2.111 (84,61) | 2.097 (84,05) | −0,56 pp |

**Bỏ riêng back ra, 2.225 bước không chạm còn lại SA hơn SFT-cont +0,90 pp** (net +20 bước) [tự tính, test]. Tác hại không lan ra toàn bộ bước không chạm. Nó dồn vào đúng một lớp, và lớp đó chỉ chiếm 39/1.000 câu nhắc TRAIN-v3 (3,9%). Ở scroll, lớp mà mọi reward trước đó đều làm hại (ck500 −6,23 [−8,30; −4,31] so S1, report/261 §6), SA lại **cải thiện** +3,18* so SFT-cont và +2,25* so ck500.

---

## 2. Luận điểm phương pháp luận: đổi reward bây giờ là đi ngược luật rẽ nhánh đã viết trước test

### 2.1 Chính báo cáo đề xuất đổi reward đã viết sẵn nhánh "giữ SA"

Báo cáo `reports/Reward thay thế SA SPICE v3.md` được viết **trước** khi có số test. Mục "Phương án dự phòng phụ thuộc số test của SA ck400" ghi nguyên văn ý: phương án dự phòng là *giữ nguyên reward SA-SPICE-v3, chỉ đổi phần ngoài reward*, được chọn khi *"SA ck400 hơn SFT-cont ở bước chạm nhưng thua ở bước không chạm. Đổi reward lúc đó là chữa sai chỗ"*. Đề xuất SPICE-chrF-A chỉ là bước kế *"nếu ngược lại SA ck400 không hơn SFT-cont ngay ở bước chạm trên test"*.

Số test rơi đúng vào nhánh thứ nhất: bước chạm +1,05 có ý nghĩa, bước không chạm tụt ở back. **Theo luật do chính phía đề xuất đổi viết trước, kết luận là giữ reward.** Muốn đổi reward bây giờ thì phải bỏ luật rẽ nhánh đã ghi sau khi thấy kết quả rơi vào nhánh nào. Gelman & Loken gọi đúng hiện tượng này là "khu vườn lối rẽ": không cần cố tình câu p, chỉ cần một quyết định phân tích hợp lý được đưa ra *sau khi* thấy dữ liệu là đủ làm mất hiệu lực suy luận (American Scientist 102:460, 2014).

### 2.2 Memo khoá trước cũng cấm đổi hệ số

`report/SA_SPICE_v3_extracted_verified.md`:
- §3: *"không thêm hệ số mới sau C1; không sweep weight trên test"*.
- §8: khi trượt thì *"dừng, báo DEV âm, không đổi 0,8/0,2"*.
- §16 câu 4: *"Có chấp nhận kết quả âm không đổi hệ số không?"* (user đã duyệt mức 2 trên cơ sở memo này, report/333 §8, §11).
- §10: khi non-inferiority bước không chạm trượt thì viết *"tap gain đi kèm trade-off; không nói no-harm"*. Memo đã dự liệu đúng tình huống back tụt và chỉ ra cách **báo cáo**, không phải cách **đổi reward**.

Hệ số 0,5 của SPICE-chrF-A lại được tìm ra sau khi quét trên chính bộ sàng (báo cáo đề xuất tự khai ở mục "Giới hạn", ý thứ hai). Như vậy SPICE-chrF-A vi phạm memo hai lần: chọn hệ số sau khi nhìn sàng, rồi đưa vào sau khi nhìn test.

### 2.3 Test dự án đã bị dùng lại rất nhiều lần, nên càng phải giữ kỷ luật

Tập kiểm 4.463 bước đã chấm khoảng 30 nhánh (report/334 §3). Dwork et al. (Science 2015, "The reusable holdout") chỉ ra rằng khi mô hình được sửa dựa trên điểm holdout đã thấy, giả định độc lập của holdout mất hiệu lực, và việc dùng lại chỉ an toàn khi đi qua một cơ chế kiểm soát. Dự án không có cơ chế đó. Thứ còn giữ được giá trị cho con số 61,21 là chuỗi *chọn trên DEV-v3 → chấm test một lần*. Một reward mới chọn sau khi đã thấy SA ck400 trên test không có tính chất này.

Bằng chứng nội bộ cho thấy chọn giữa các nhánh có chênh lệch cỡ nhiễu thì bị "lời nguyền người thắng":
- Lượt chạy lại đúng cấu hình ck500 (A/A) chỉ đạt 59,74, nên ck500 − A/A = +0,92 [+0,49; +1,37] [test] (report/334 Bảng 2.3). Lượt "thắng" một hạt giống tụt về gần mốc khi chạy lại.
- ck500/101 − ck500/202 = +0,72* [test] (report/334 §3b).
- Val từng phóng đại khoảng cách giữa hai nhánh gần 40 lần (0,76 val so với 0,02 test, CLAUDE.md khối 9/9 V2).

SPICE-chrF-A tự khai kỳ vọng "tối đa khoảng +1 exec, có thể bằng 0, dưới MDE 2,11" (báo cáo đề xuất, đoạn mở). Mức đó nằm gọn trong dải 0,7–0,9 giữa hai lượt cùng cấu hình. Chọn nó thay SA nghĩa là đổi một phương pháp có số test một lần lấy một phương pháp mà lợi thế kỳ vọng không phân biệt được với nhiễu hạt giống.

### 2.4 Bước back đã thấy trên DEV trước khi mở test

Tác hại back được ghi ở report/333 §12 (DEV, 84 → 56–60/104) **trước** khi kernel test xong (15/11 ~16:50, §14). Vì vậy chữa back là phát triển dựa trên DEV, hợp lệ, không phải chỉnh theo test. Ngược lại, chuyển sang SPICE-chrF-A *vì* test cho thấy SA − ck500 chưa có ý nghĩa thì là chỉnh theo test. Ranh giới này nên viết ra để hội đồng thấy.

---

## 3. Back không phải lỗi dấu của reward, nên đổi reward không chữa được back

### 3.1 Lúc xuất phát, SA xếp câu đúng loại back trên câu sai loại

Phép đếm mới hôm nay [tự tính, sàng]: trên 8 mẫu SFT-cont của TRAIN-v3 (`runs/sa_spice_v3/mau_k1/mau_{0,1}.jsonl`, điểm thưởng ở `screen/out/sa3_screen_buoc.jsonl`; lưu ý phần tử 0 của danh sách `R` là câu greedy, 1–8 là 8 mẫu), lấy các nhóm có cả câu đúng lẫn sai loại thao tác theo `classify` của verifier v3, đo xác suất reward xếp câu đúng loại trên câu sai loại:

| loại (số nhóm lẫn) | SA-SPICE-v3 | SPICE-chrF-A (0,8·(0,5s+0,5c)+0,2A−d) | chrF | ROUGE-L | SPICE-MATCH |
|---|---|---|---|---|---|
| back (26/39) | **0,892** | **0,892** | 0,882 | 0,879 | 0,747 |
| scroll (68/135) | **0,938** | 0,935 | 0,849 | 0,912 | 0,718 |
| input_text (28/49) | **0,601** | 0,589 | 0,515 | 0,503 | 0,554 |
| open_app (27/85) | **0,951** | 0,951 | 0,892 | 0,925 | — |

(SPICE-chrF-A tái dựng s, c từ điểm các arm theo cách của `screen_extra.py`.)

Đọc:
- Ở back, SA đã xếp câu "Go back…" trên câu chạm với xác suất 0,892, và **SPICE-chrF-A cho đúng cùng thứ tự (265/32/0 cặp, trùng tuyệt đối)**. Đổi sang SPICE-chrF-A không thay đổi tín hiệu thưởng ở bước back trên mẫu xuất phát.
- Trên mọi lớp không chạm, SA xếp đúng loại tốt nhất hoặc ngang tốt nhất. chrF thuần, thành phần mà đề xuất muốn tăng tỉ trọng, xếp đúng loại **kém hơn** SA ở cả bốn lớp (scroll 0,849 so với 0,938).
- 37/39 nhóm back có ít nhất một mẫu đúng loại (khớp con số 38/39 của báo cáo đề xuất, sai lệch do cách đếm).

Vậy reward có tín hiệu đúng chiều ở back. Back tụt trong lúc train vì lý do khác, khả dĩ nhất là phân bố câu nhắc: back được cập nhật ~39 lần trong 1.000 lượt câu nhắc, click 616 lần, mà cập nhật trên câu chạm kéo cả policy về văn "Click on…" (33/37 câu back bị phá thành câu chạm, 00_su_kien_test.md) [suy]. Giới hạn: đây là mẫu tĩnh lúc xuất phát; sàng đã ba lần xếp sai thứ hạng sau train, nên bảng này chỉ chứng minh "không có lỗi dấu lúc xuất phát", không chứng minh nguyên nhân.

### 3.2 Mọi reward đã thử đều hại back, kể cả thành phần mà đề xuất muốn tăng

- ck500 (SPICE): back 72,96 → 67,04 so S1 (−5,93) [test] (report/334 §5, report/261 §6).
- CTG A2 (CIDEr-D): 65,56; CTG A3 (CIDEr-D + CTG cộng vào advantage): 62,59, tức −10,4 so S1 [test] (report/334 §5). CTG còn làm back xấu hơn A2 −2,96 [−5,32; −0,76] (report/279 §4g): can thiệp vào advantage của lớp hiếm đã từng phản tác dụng.
- chrF ck400 cùng pipeline với SA: back 57/104, SA ck400 60/104 [dev] (report/333 §12). Thành phần mà SPICE-chrF-A muốn tăng gấp đôi tỉ trọng đã hại back ít nhất ngang SA, và tụt bước không chạm nặng hơn (−6,90 so với −2,40 [dev]).

Báo cáo đề xuất tự viết: *"Tác hại ở bước back/scroll xuất hiện với mọi phần thưởng đã thử, nên phải chặn bằng cơ chế ngoài reward chứ không bằng một hệ số nữa."* Hai bên tranh luận đồng ý ở điểm này. Bất đồng chỉ còn ở bước chạm, nơi SA đã có +1,05 [test].

### 3.3 Tài liệu: chữa thoái lui theo lớp/miền mà không đổi reward

| tiền lệ | làm gì | venue (đã kiểm) | áp vào đây |
|---|---|---|---|
| InstructGPT, PPO-ptx (Ouyang et al.) | trộn gradient log-likelihood trên dữ liệu tiền huấn luyện vào PPO để giảm thoái lui trên các tập công khai; làm tốt hơn việc chỉ tăng hệ số KL | NeurIPS 2022 | neo NLL trên câu chuẩn bước không chạm; giữ nguyên reward |
| DISCO (Zhou et al.) | GRPO "tối ưu lệch về miền chiếm đa số" khi dữ liệu nhiều miền mất cân bằng; sửa bằng cân lại theo tần suất miền | Findings of EMNLP 2025 | back là "miền thiểu số" 3,9%; cân lại phân bố câu nhắc hoặc trọng số nhóm theo lớp |
| RL's Razor (Shenfeld, Pari, Agrawal) | mức quên dự đoán được bằng KL giữa policy sau tinh chỉnh và policy gốc trên dữ liệu nhiệm vụ mới | ICLR 2026 | theo dõi KL riêng trên bước back; dừng sớm theo KL (ck400 hại back ít hơn ck500 [dev]) |
| Henderson et al.; Agarwal et al. | xem mục 4 | AAAI 2018; NeurIPS 2021 | — |

Lưu ý: DISCO cân lại *trọng số tối ưu theo miền*, về hình thức là nhân hệ số vào advantage. Đó là gần với CTG đã thất bại nội bộ, nên ưu tiên bản rẻ và ít rủi ro hơn là cân lại **số câu nhắc** (tầng dữ liệu). Chưa tìm được bài đã bình duyệt nào làm đúng việc phân tầng câu nhắc theo loại thao tác cho GRPO trong GUI; UI-R1 (arXiv 2503.21620, có bản trên ojs.aaai.org, chưa kiểm kỹ venue) chọn 136 mẫu gồm năm loại thao tác nhưng tiêu chí công bố là độ khó, không phải cân bằng lớp. Cầu nối từ DISCO sang phân tầng câu nhắc là [suy].

---

## 4. Một hạt giống: đúng là điểm yếu, nhưng thuốc là thêm hạt giống, không phải reward mới

- Henderson et al. (AAAI 2018, tr. 3207–3214) chạy 10 lượt cùng siêu tham số, chia hai nhóm 5 hạt giống, và nhận được hai phân phối khác nhau có ý nghĩa thống kê (t = −9,09, p = 0,0016) chỉ do hạt giống. Họ khuyến cáo chạy nhiều hạt giống khi so phương pháp, và cảnh báo việc chọn lượt tốt nhất hoặc lấy trung bình ít hơn 5 lượt.
- Agarwal et al. (NeurIPS 2021, Outstanding Paper) đề nghị báo KTC bootstrap phân tầng thay cho ước lượng điểm khi số lượt ít.
- Trong kho: hai lượt cùng cấu hình lệch 0,92 (ck500 − A/A) và 0,72 (ck500/101 − 202) [test].

Hệ quả: so SA (1 hạt) với SPICE-chrF-A (1 hạt) là so hai mẫu cỡ 1 từ hai phân phối có độ lệch giữa hạt cỡ 0,7–0,9, trong khi khác biệt kỳ vọng ≤ 1. Phép so đó không quyết được gì. Một lượt SPICE-chrF-A thêm vào chỉ tạo thêm một lối rẽ. Ngược lại, hai hạt giống SA nữa trả lời đúng câu hỏi hội đồng sẽ hỏi: "+1,05 so điểm xuất phát có lặp lại không?". Memo đã khoá sẵn hạt 401/503/907 (§6) và thủ tục trung bình ba hạt (§8–9).

---

## 5. Tự phản biện: điểm yếu lớn nhất và cách trả lời

**(a) Back −12,59 [−16,80; −8,49], cứu 3 phá 37 [test].** Đây là tác hại thật, lớn, và tệ hơn ck500 (SA − ck500 −8,52*). Memo §10 đặt biên non-inferiority back −2 pp; SA trượt xa.
Trả lời: (i) không giấu, báo đúng câu memo §10 "tăng ở bước chạm đi kèm đánh đổi ở bước back". (ii) Tác hại khoanh vùng: bỏ back thì 2.225 bước không chạm còn lại +0,90 pp, scroll +3,18* [test]. (iii) Đổi reward không chữa được: SPICE-chrF-A xếp back y hệt SA lúc xuất phát, chrF đứng một mình hại back ít nhất ngang SA [dev] (mục 3). (iv) Chữa bằng tầng dữ liệu hoặc neo NLL, có tiền lệ (mục 3.3). Điểm còn hở: chưa có số chứng minh phân tầng câu nhắc chữa được back; nếu nó không chữa được thì back là giới hạn của cả họ RL so câu, phải khai như vậy.

**(b) Một hạt giống (101), lệch memo (khoá 401/503/907, "seed 101 không tham gia").** +1,05 chỉ lớn hơn chênh A/A 0,92 một chút. Xác suất SA − SFT-cont thật sự > 0 khi tính cả nhiễu hạt giống thấp hơn mức p = 6,8e−4 gợi ý, vì KTC bootstrap chỉ phản ánh nhiễu mẫu bước, không phản ánh nhiễu huấn luyện [suy].
Trả lời: chạy ngay hai hạt 401, 503 cùng công thức (việc 1 ở mục 6), báo trung bình ba hạt và từng hạt. Điều này đúng hướng Henderson/Agarwal; đổi reward không giải quyết điểm yếu này mà còn nhân nó lên.

**(c) Thiếu arm SPICE thuần (SPICE-MATCH) xuất phát từ SFT-cont.** Không tách được công của α_g, chrF và A so với SPICE thuần cùng điểm xuất phát. ck500 là SPICE thuần nhưng từ S1 và tập câu nhắc khác, nên SA − ck500 +0,56 không phải phép so một biến.
Trả lời: đây là ablation bắt buộc của memo (§6.1, điều kiện mở CONFIRM §8). Nó **không** đòi đổi reward; nó cho biết claim nên hẹp tới đâu. Nếu SPICE-MATCH ngang SA, phương pháp vẫn là GRPO + thưởng lấy SPICE làm lõi và claim hạ về "GRPO + SPICE từ SFT-cont hơn SFT-cont"; nếu SA hơn, claim thiết kế thưởng có chỗ đứng. Cả hai đều giữ lõi SPICE.

**(d) SA − ck500 +0,56, p = 0,069, chưa có ý nghĩa; "cao nhất mọi nhánh RL" là điểm cực đại của ~16 nhánh.**
Trả lời: không cần claim SA hơn ck500 (khác điểm xuất phát). Claim chính là so điểm xuất phát. Câu "cao nhất trong mọi nhánh" là một thống kê cực đại, chịu lời nguyền người thắng, nên **không** dùng làm luận điểm; chỉ nêu như mô tả bảng, kèm KTC ghép cặp.

**(e) Thiết kế SA đã dùng thông tin từ test cũ** (thành phần A sinh ra sau khi thấy ck500 hại bước không chạm trên test, report/261; hệ số khoá từ pilot C1 trên S1/101).
Trả lời: đúng, phải khai. Nhưng con số 61,21 của ck400 là lần chấm test duy nhất của lượt này, điểm lưu chọn trên DEV-v3 mới dựng, episode tách hẳn. Đổi tiếp reward sẽ cộng thêm một vòng dùng test nữa trên đúng tập đó.

**(f) Cách đọc ngưỡng "scroll + back gộp ≤ 5" được chốt sau khi thấy DEV** (report/333 §13). Đọc từng lớp thì mọi nhánh đều trượt và không nhánh nào được lên test.
Trả lời: cách đọc này quyết định *có* chấm test hay không, không quyết định chọn reward nào; nó đã được khai ở §13 trước khi có test. Cho các hạt mới, khoá **trước** một ngưỡng back riêng (đề xuất: back DEV không tụt quá 5 pp so SFT-cont, chỉ để báo và để chọn điểm lưu, không để loại arm).

**(g) Phản biện ngược về test reuse:** Roelofs et al. (NeurIPS 2019) phân tích 120 cuộc thi Kaggle và thấy ít bằng chứng quá khớp do dùng lại holdout. Bên đổi có thể nói một lượt nữa trên test không hại gì.
Trả lời: Kaggle có tập kiểm lớn và khác biệt giữa đội thường lớn hơn nhiễu; ở đây khác biệt giữa các reward (≤ 1 pp) nhỏ hơn nhiễu hạt giống (0,7–0,9), đúng vùng mà chọn theo điểm quan sát bị chi phối bởi nhiễu. Chứng cứ nội bộ (A/A, val phóng đại 40 lần) cho thấy dự án này đã bị lời nguyền người thắng thật. Và vấn đề chính không phải quá khớp test mà là **mất tính chất chọn-trước** của con số báo cáo.

**(h) Điểm hở của chính bảng mục 3.1:** sàng dùng `classify` (regex) trong khi test dùng `canon_action`; hai bộ phân loại khác nhau. Và đó là mẫu tĩnh. Bảng chỉ nên dùng để bác luận điểm "reward sai dấu ở back", không để khẳng định SA tốt hơn.

---

## 6. Việc đề xuất, theo thứ tự ưu tiên

Giả định chi phí [suy]: GRPO trên T4 đo được ~146 s/update (report/333 §11) ⇒ 500 update ≈ **20 h mỗi arm**; một kernel T4×2 chạy song song hai arm ≈ 21 h tường, ~3 phiên (trần 7,5–11 h). Chấm test một mô hình ≈ 8–10 h (kernel `sa3-test-ck400` 06:55 → 16:50 cho SA bước chạm + hai mô hình bước không chạm, có dùng lại 4.112 kết quả chấm cũ). Chấm DEV-v3 ≈ 3–5 h mỗi mô hình. Hạn mức: 30 h/tuần × 3 tài khoản Kaggle; cách Kaggle tính giờ cho T4×2 phải kiểm lại trước khi lên lịch.

| # | việc | máy, chi phí [suy] | vì sao, và có còn "cùng phương pháp" không |
|---|---|---|---|
| 0a | **Độ đo văn bản test của SA ck400** (7 độ đo + KTC ghép cặp với SFT-cont, ck500) | Kaggle CPU, ~20–40 phút (kernel DEV tương tự chạy ~20 phút, report/333 §12b) | thiếu trong report/334 Bảng 2.2; hội đồng sẽ hỏi SPICE có tăng không. Báo vô điều kiện, kể cả khi BLEU-4 giảm như trên DEV |
| 0b | **Khoá kế hoạch phân tích** trước mọi output mới: `protocol_freeze.json` từ DRAFT thành FROZEN (hạt 401/503, luật 1-SE trên trung bình ba hạt, ngưỡng back riêng, họ Holm), commit + giờ | 0 GPU | biến các lượt sau thành xác nhận, không phải thăm dò |
| 1 | **SA-SPICE-v3 hạt 401 và 503**, công thức y hệt (TRAIN-v3 cùng thứ tự, β 0,04, 500 update, bản vá chặn NaN) | 1 kernel T4×2 ≈ 21 h tường, ~40 arm-giờ | trả lời điểm yếu (b). Cùng phương pháp tuyệt đối |
| 2 | **SPICE-MATCH từ SFT-cont** hạt 101 trước (cặp được với lượt SA/101 có sẵn), rồi 401/503 | hạt 101: ghép vào GPU còn trống; đủ ba hạt ≈ 60 arm-giờ | trả lời điểm yếu (c). Là ablation của memo §6.1, không đổi reward chính |
| 3 | **Chấm DEV-v3 ck100–500** cho mọi arm mới (và ck100–300 của SA/101 để xem quỹ đạo back theo số update) | ~3–5 h/mô hình; gộp 2 mô hình/kernel | memo §8 đòi; ck100–300 của SA/101 chỉ để chẩn đoán, **không** chọn lại điểm lưu cho hạt 101 đã chấm test |
| 4 | **Chấm test** điểm lưu đã chọn trên DEV của SA/401, SA/503, SPICE-MATCH ×3 | ~8–10 h/mô hình | bảng chính báo trung bình ba hạt SA − SFT-cont kèm từng hạt |
| 5 | **CONFIRM-v3** (1.500 episode, 5.601 bước, chưa mở) một lần cho SA ×3, SPICE-MATCH ×3, SFT-cont | ~6–8 h/mô hình [suy] | tập sạch duy nhất còn lại cho phép so reward đúng thủ tục. Nếu muốn so SPICE-chrF-A thì đưa vào **ở đây như baseline đăng ký trước**, không như phương pháp thay thế |
| 6 | **Nhánh chữa back: SA + câu nhắc phân tầng** (back và input_text ~8% mỗi lớp lấy từ phần TRAIN-v3 chưa dùng, bớt click, giữ 1.000), hạt 101 | 1 arm ≈ 20 h + DEV | reward và GRPO giữ nguyên ⇒ **cùng hàm thưởng, khác công thức dữ liệu**. Phải đặt tên riêng ("SA-SPICE-v3, câu nhắc phân tầng"), báo cạnh lượt gốc, không thay số của lượt gốc. Hợp lệ vì vấn đề back được phát hiện trên DEV trước test (mục 2.4). Mức 8% là [suy], khoá trước khi chạy |
| 7 | (tuỳ, chỉ khi 6 không đủ) **neo NLL trên câu chuẩn bước không chạm** kiểu PPO-ptx | sửa `sa3_grpo.py`, 1 arm | đổi mô tả phương pháp thành "GRPO + SA-SPICE-v3 kèm neo SFT"; reward vẫn giữ |

Không làm: chỉnh 0,8/0,2, chỉnh α, chuyển sang SPICE-chrF-A làm phương pháp, chấm thêm chrF ck400 hay SA ck500 trên test để chọn lại.

Về câu hỏi "phân tầng câu nhắc có còn là cùng phương pháp không": nếu phương pháp được định nghĩa là *hàm thưởng + thuật toán tối ưu + điểm xuất phát + neo KL*, thì phân tầng câu nhắc là thay đổi **dữ liệu huấn luyện**, không đổi phương pháp, giống như DISCO coi phân bố miền là một tham số của quy trình chứ không phải của hàm thưởng. Nhưng memo §4.2 đã khoá cách dựng TRAIN-v3 (một bước mỗi episode theo băm, không cân lớp), nên về thủ tục đó là một **biến thể** và phải báo như một lượt riêng. Kết quả chính của luận văn vẫn là lượt TRAIN-v3 gốc (ba hạt).

### Câu được phép viết ngay bây giờ (chưa có việc 1–5)

> Trên tập kiểm, GRPO với thưởng SA-SPICE-v3, xuất phát từ SFT-cont, đạt exec 61,21%, hơn chính điểm xuất phát +1,05 điểm [+0,46; +1,65] (một hạt giống, điểm lưu chọn trên DEV-v3 trước khi chấm tập kiểm). Mức tăng đi kèm đánh đổi ở bước quay lại (58,5% so với 71,1%), trong khi các bước không chạm còn lại không giảm.

Không viết: "SA tốt hơn ck500", "SA tốt nhất", "thiết kế thưởng SA tạo ra mức tăng" (chưa có SPICE-MATCH từ SFT-cont), "không gây hại".

---

## Ba luận điểm mạnh nhất

1. **Luật rẽ nhánh viết trước test chỉ định giữ reward.** Báo cáo đề xuất đổi, viết trước khi có số test, đã ghi: nếu SA hơn SFT-cont ở bước chạm mà tụt ở bước không chạm thì giữ reward SA và chữa ngoài reward. Test cho đúng kịch bản đó (+1,05 [+0,46; +1,65] bước chạm; back −12,59). Memo §3, §8, §16 cũng cấm đổi hệ số. Đổi bây giờ là bỏ luật sau khi thấy kết quả (Gelman & Loken 2014; Dwork et al. 2015), và làm mất tính chất "chọn trên DEV, chấm test một lần" của con số duy nhất trong dự án mà dev chuyển sang test tốt.
2. **Đổi reward không chạm tới vấn đề có thật.** Ở bước chạm SA đã là lượt RL duy nhất hơn SFT tiếp có ý nghĩa (Bonferroni ×30 vẫn p ≈ 0,02) [test]. Tác hại dồn ở back; bỏ back ra thì bước không chạm còn lại +0,90 pp, scroll +3,18* [test]. Ở back, SPICE-chrF-A xếp câu đúng loại **y hệt** SA (0,892, cùng 265/32 cặp) [tự tính, sàng], còn chrF đứng một mình hại back ít nhất ngang SA [dev] và mọi reward trong kho đều hại back. Thuốc nằm ở phân bố câu nhắc hoặc neo NLL (InstructGPT NeurIPS 2022; DISCO Findings EMNLP 2025).
3. **Điểm yếu thật là một hạt giống, và thuốc của nó là thêm hạt giống.** Kỳ vọng tự khai của SPICE-chrF-A (≤ +1, có thể 0) nhỏ hơn chênh giữa hai lượt cùng cấu hình (0,72–0,92 [test]); Henderson et al. (AAAI 2018) cho thấy chỉ đổi hạt giống đã ra hai phân phối khác nhau có ý nghĩa. Hai hạt SA cùng công thức và một arm SPICE-MATCH cùng điểm xuất phát trả lời đúng câu hội đồng sẽ hỏi; một reward mới một hạt chỉ thêm lối rẽ.

## Điều sẽ khiến tôi đổi ý

- **Hai hạt 401 và 503 cho SA − SFT-cont trung bình ≤ 0** hoặc KTC ba hạt phủ 0 rõ (ước lượng điểm < +0,3): khi đó +1,05 của hạt 101 là nhiễu, SA không có lợi thế để giữ, và hướng đúng là kết luận "reward không phải đòn bẩy" chứ không phải thử reward thứ mười.
- **SPICE-MATCH từ SFT-cont ngang hoặc hơn SA trên DEV và test**: tôi vẫn giữ lõi SPICE nhưng sẽ đổi phương pháp được nêu thành dạng đơn giản hơn (SPICE thuần), vì các thành phần thêm vào không có công.
- **Nhánh phân tầng câu nhắc (việc 6) và neo NLL (việc 7) đều không kéo được back lên** (DEV back vẫn tụt > 10 pp so SFT-cont) trong khi một reward khác được đăng ký trước trên CONFIRM-v3 giữ được back: khi đó back là lỗi của hàm thưởng chứ không phải của dữ liệu, và luận điểm 2 sai.
- **Một phép đo trên mẫu policy đã train** (ví dụ 8 mẫu của SA ck400 trên các câu nhắc back TRAIN-v3) cho thấy SA xếp câu chạm trên câu "Go back" ở back trong khi SPICE-chrF-A thì không: nghĩa là tín hiệu thưởng ở back hỏng dần theo quá trình train theo cách khác nhau giữa hai reward. Bảng mục 3.1 chỉ đo lúc xuất phát nên không loại được khả năng này.
- **Trên CONFIRM-v3, SPICE-chrF-A (đã đăng ký trước làm baseline) hơn SA với Holm qua ba hạt**: tôi sẽ báo nó vô điều kiện và hạ claim của SA, nhưng vẫn không đổi tên phương pháp sau khi đã nhìn CONFIRM.

---

## Nguồn

Nội bộ: `research_notes/Debate SA SPICE v3 sau test/00_su_kien_test.md` · `reports/Reward thay thế SA SPICE v3.md` (mục "Phương án dự phòng…", "Tác hại ở bước back…", "Giới hạn…") · `report/SA_SPICE_v3_extracted_verified.md` §3, §6, §8, §10, §16 · `report/333_SA_SPICE_V3_PREFLIGHT_11_11.md` §11–14 · `report/334_BANG_KET_QUA_TONG_HOP.md` §2, §3b, §5, §11 · `runs/sa_spice_v3/test/pred_{sa_ck400,sftcont}_test_nontap.jsonl` · `runs/sa_spice_v3/mau_k1/mau_{0,1}.jsonl` · `runs/sa_spice_v3/screen/out/sa3_screen_buoc.jsonl` · `runs/sa_spice_v3/preflight/protocol_freeze.json`.
Script tự tính (scratchpad, sẽ bị xoá; chép vào `harness/` nếu cần tái lập): `/tmp/claude-1000/-mnt-d-Master-Thesis/a826d459-2edf-44cb-b931-82b4bcbff84c/scratchpad/test_back.py` (bảng bước không chạm), `/tmp/claude-1000/-mnt-d-Master-Thesis/a826d459-2edf-44cb-b931-82b4bcbff84c/scratchpad/back_an3.py` và `/tmp/claude-1000/-mnt-d-Master-Thesis/a826d459-2edf-44cb-b931-82b4bcbff84c/scratchpad/back_an4.py` (bảng mục 3.1).

Ngoài (venue đã kiểm ở nguồn trong lượt này, trừ chỗ ghi khác):
- Dwork, Feldman, Hardt, Pitassi, Reingold, Roth. The reusable holdout: Preserving validity in adaptive data analysis. *Science* 349(6248):636, 2015. https://cis.upenn.edu/~aaroth/reusable.html · https://arxiv.org/abs/1506.02629
- Gelman, Loken. The Statistical Crisis in Science. *American Scientist* 102:460, 2014 (tạp chí phổ biến khoa học, không phải hội nghị bình duyệt). https://www.americanscientist.org/node/3579
- Henderson, Islam, Bachman, Pineau, Precup, Meger. Deep Reinforcement Learning that Matters. AAAI 2018, tr. 3207–3214. https://ojs.aaai.org/index.php/AAAI/article/view/11694 · https://ar5iv.labs.arxiv.org/html/1709.06560
- Agarwal, Schwarzer, Castro, Courville, Bellemare. Deep RL at the Edge of the Statistical Precipice. NeurIPS 2021 (Outstanding Paper). https://arxiv.org/abs/2108.13264 · https://blog.neurips.cc/2021/11/30/announcing-the-neurips-2021-award-recipients/
- Roelofs, Shankar, Recht et al. A Meta-Analysis of Overfitting in Machine Learning. NeurIPS 2019. https://papers.nips.cc/paper/9117-a-meta-analysis-of-overfitting-in-machine-learning
- Ouyang et al. Training language models to follow instructions with human feedback (PPO-ptx). NeurIPS 2022 (venue theo hiểu biết chung, chưa mở trang proceedings trong lượt này). https://arxiv.org/abs/2203.02155
- Zhou et al. DISCO Balances the Scales: Adaptive Domain- and Difficulty-Aware RL on Imbalanced Data. Findings of EMNLP 2025 (theo ghi chú trên arXiv). https://arxiv.org/abs/2505.15074
- Shenfeld, Pari, Agrawal. RL's Razor: Why Online Reinforcement Learning Forgets Less. ICLR 2026. https://proceedings.iclr.cc/paper_files/paper/2026/hash/618c95f4557c15b253fb0e6f548ea0c0-Abstract-Conference.html
- Lu et al. UI-R1. arXiv 2503.21620 (có bản trên ojs.aaai.org; venue chưa kiểm kỹ, coi như preprint). https://arxiv.org/abs/2503.21620
