# 332 — Kaggle CPU: reward-screening cho GRPO + SPICE (08/11/2026)

**Trạng thái:** Đã chuẩn bị code + private Kaggle notebook/dataset kit ở Windows. **Chưa upload/chạy trên Kaggle**, vì phiên làm việc chưa có xác thực Kaggle. Kết quả mock không phải kết quả khoa học.

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
