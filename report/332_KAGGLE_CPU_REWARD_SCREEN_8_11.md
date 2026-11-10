# 332 — Kaggle CPU: reward-screening cho GRPO + SPICE (08/11/2026)

**Trạng thái:** Đã chuẩn bị code + private Kaggle notebook/dataset kit ở Windows. **Đã chạy xong trên Kaggle CPU 9/11, xem mục cuối.** (Bản 8/11 chưa upload vì chưa có xác thực Kaggle.) Kết quả mock không phải kết quả khoa học.

## Tại sao là CPU job đáng làm nhất?

Lưới RL đã có nhiều lượt so test và phân rã vào ngày 08/11. Điều còn thiếu trước khi tốn GPU là kiểm tra các reward SPICE thay thế có sửa đúng lỗi hay không. Job này không train mô hình; chỉ tính điểm reward trên **C1 validation** gồm 400 bước × 8 câu sinh S1/101 (249 bước tap có UGround executability; 151 bước non-tap không có executability và chỉ dùng proxy loại thao tác).

Cùng một notebook sẽ:
1. So R0_historical (SPICE + penalty gốc), R0_capped, R_fixed_spice_chrf, R2_sparse (fallback khi SPICE(gold,gold)=0), R3_action (action gate), R4_sparse_action (kết hợp cả hai).
2. Đo tỷ lệ nhóm G=8 có reward như nhau, tỷ lệ cặp hòa, concordance và oracle uplift trên cached C1 val; chia theo từng action type.
3. Audit reward của câu chuẩn tự so, coverage của action verifier, và 8 phép stress test (synonym, wrong action, wrong target, zero tuple, paraphrase, wrong argument, wrong position, toggle contradiction).

**Cảnh báo:** Kết quả non-tap là proxy action-class dựa trên heuristic và không độc lập với action-aware reward; KHÔNG được trình là executability thực. H2 trên các câu mẫu tĩnh không dự đoán đúng thứ tự sau huấn luyện trong report/320; chỉ dùng để sàng lọc lỗi, KHÔNG để kết luận reward tăng thành công test.

## Các file đã chuẩn bị

- harness/reward_cpu_8_11.py: CPU scoring, group metrics, action abstention và stress tests.
- harness/test_reward_cpu_8_11.py: full-pipeline smoke với FAKE SPICE/chrF để kiểm logic.
- _bundles/luoi/make_reward_cpu_8_11.py: copy lại data C1 và tạo notebook.
- _bundles/reward_cpu_8_11/k/reward-spice-c1-cpu-8-11.ipynb: notebook Kaggle CPU.
- _bundles/reward_cpu_8_11/k/kernel-metadata.json: accelerator OFF, internet ON, PRIVATE.
- _bundles/reward_cpu_8_11/ds/dataset-metadata.json: Kaggle private dataset, license other. Không public khi chưa kiểm điều kiện sử dụng AndroidControl.
- _bundles/reward_cpu_8_11/ds/*: bản sao dữ liệu C1 để upload, sẽ được Git ignore.

Đầu ra dự kiến trên Kaggle: /kaggle/working/reward_cpu_8_11/reward_cpu_c1.json, reward_groups.jsonl, log và ZIP. Notebook xác minh đúng 400 prompt, 249 nhóm tap, 151 nhóm non-tap.

## Kiểm tra đã xong trên máy (KHÔNG phải chạy SPICE thật)

- python3 harness/reward_cpu_8_11.py --selftest: PASS.
- python3 harness/test_reward_cpu_8_11.py: PASS, kiểm toàn bộ 400 nhóm cùng 8 nhãn mỗi nhóm dưới scorer giả.
- python3 _bundles/luoi/make_reward_cpu_8_11.py: PASS; tạo notebook và dataset kit.
- Chưa chạy Java + CoreNLP + pycocoevalcap thật trên Kaggle; không có số kết luận nào về R4.

### Lỗ hổng và kiểm soát sai lệch

C1 chứa nhiều trường hợp action_type=wait trong log nhưng câu chuẩn chỉ dẫn thao tác khác (click/swipe/open). Bộ reward sẽ ABSTAIN thay vì hard-gate khi nhãn câu và log mâu thuẫn. Các mẫu chưa phân loại action cũng không bị gán click ngầm.

SPICE(gold,gold)=0 chỉ là proxy nhận diện thiếu tín hiệu semantic tuple, không được nhầm với tuple count thật. Cơ chế R2/R4 cần kiểm bằng Java thật trên Kaggle.

## Cách push Kaggle khi tài khoản đã xác thực

Metadata chọn account trangphngngc theo các Kaggle CPU notebook sẵn có. Nếu muốn dùng account khác, cập nhật ID trong dataset-metadata.json và kernel-metadata.json trước khi upload. Cần cài Kaggle CLI và cấu hình token/auth trên máy, không commit token.

~~~bash
python3 _bundles/luoi/make_reward_cpu_8_11.py
kaggle datasets create -p _bundles/reward_cpu_8_11/ds
kaggle kernels push -p _bundles/reward_cpu_8_11/k
kaggle kernels status trangphngngc/reward-spice-c1-cpu-8-11
~~~

Notebook cần hai data sources: trangphngngc/grpo-spice-reward-c1-8-11 và trangphngngc/corenlp-360-jars. Kaggle CPU cài pycocoevalcap+sacrebleu, dùng Java và JAR CoreNLP 3.6. Nếu không chạy được, xem log và ghi lý do version, không thay điểm reward âm thầm.

## Sau khi CPU xong

Ưu tiên đo R4 so R2/R3/R0_capped/R_fixed; kiểm gold false rejection và all-zero reward groups. Audit thủ công các mẫu action không chắc, đặc biệt wait, open_app và paraphrase. Chọn tối đa 2–3 finalist trên validation; sau đó mới chạy GRPO/SCST với cùng reward và các seed được chốt trước. Không chọn winner theo test đã nhìn.

Chưa nên tốn CPU để chấm lại các điểm SPICE/CIDEr/ROUGE-L và phân rã ck500/A/A đã hoàn thành ngày 08/11.

## Kết quả Kaggle CPU (9/11/2026)

Kernel `trangphngngc/reward-spice-c1-cpu-8-11` · dataset private `trangphngngc/grpo-spice-reward-c1-8-11` · tệp `runs/luoi/8_11/reward_c1/` (`reward_cpu_8_11/reward_cpu_c1.json`, `doc_c1.json`) · đọc bằng `harness/reward_c1_doc_8_11.py`. Số val C1 (400 bước, 8 mẫu S1/101), cấm trích, một hạt, chỉ để sàng lọc; không phải kết quả sau train.

Trước khi chạy đã sửa `spice_scores`: khoá chuỗi làm điểm SPICE lệch cặp (pycocoevalcap trả theo `sorted(keys)`); thêm phép kiểm câu tự so chỉ ra 0 hoặc 1. Kernel chạy đạt phép kiểm này.

| 249 bước chạm, cặp mẫu khác kết quả exec (1.528) | đồng thuận (hoà tính 0,5) | bỏ cặp hoà | tỉ lệ hoà |
|---|---|---|---|
| R0_historical (SPICE − phạt) | 0,685 | 0,753 | 27,0% |
| R0_capped | 0,675 | 0,772 | 35,5% |
| R_fixed_spice_chrf (0,8 SPICE + 0,2 chrF) | 0,793 | 0,793 | 0,2% |
| R2_sparse | 0,793 | 0,793 | 0,2% |
| R3_action | 0,748 | 0,816 | 21,5% |
| R4_sparse_action | 0,816 | 0,818 | 0,5% |
| chrF một mình (tính thêm, không có trong thiết kế ban đầu) | 0,835 | 0,836 | 0,1% |

Hiệu số, KTC95 bootstrap cụm episode, B = 2.000 (bỏ cặp hoà): R4 − R0 +0,065 [+0,027; +0,105] · R2 − R0 +0,041 [+0,017; +0,065] · R3 − R0 +0,063 [+0,026; +0,103] · chrF − R0 +0,083 [+0,034; +0,135] · R4 − R2 +0,024 [−0,002; +0,054] · R4 − chrF −0,018 [−0,053; +0,018].

- Phần lớn mức tăng của đồng thuận là do hết hoà: R4 − R0 là +0,132 khi tính hoà 0,5, chỉ còn +0,065 khi bỏ cặp hoà.
- chrF một mình không thua R4 và cao hơn R2, nên bằng chứng này chưa ủng hộ giữ SPICE trong thưởng. Trên val này SPICE chiếm 80% trọng số nhưng không đem thêm thứ tự so với chrF.
- R2 và R_fixed trùng trên bước chạm (chỉ 1/249 bước chạm có SPICE(câu chuẩn, câu chuẩn) = 0). Phần dự phòng của R2 chỉ có tác dụng ở bước không chạm (scroll 21,9%, back 20%, wait 6,2%).
- Bước không chạm: R3/R4 đạt 0,883/0,892 nhưng kết quả ở đây là proxy loại thao tác từ chính bộ phân loại câu mà cổng dùng, nên phép đo vòng tròn, không dùng để so.
- Stress test: R4 gán 0 cho cả hai ca sai thao tác và ca `zero_tuple`/`paraphrase`, nhưng không phân biệt được sai phần tử (`wrong_target`: câu đúng 0,254 < câu sai 0,912), sai vị trí (0,495 < 0,519), và câu đảo nghĩa bật/tắt (0,943 vs 0,765, chỉ giảm nhẹ). Đổi đúng loại thao tác được xử lý; chọn đúng phần tử thì vẫn chưa.
- `wait`: 0/32 bước qua kiểm câu chuẩn khớp nhãn, cổng luôn đứng ngoài ở nhóm này.
- Việc kế nếu đi tiếp: thử train R4 và mốc chrF một mình với cùng hạt, chọn trước 2–3 ứng viên. Đồng thuận trên mẫu S1 chưa chứng minh gì về kết quả sau train (tiền lệ: oracle CIDEr-D mạnh hơn SPICE ở `report/252` nhưng GRPO + CIDEr-D không hơn).
