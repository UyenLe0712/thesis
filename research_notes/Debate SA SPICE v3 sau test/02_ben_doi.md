# Bên ĐỔI: nên sửa reward SA-SPICE-v3 ở lớp không chạm, giữ nguyên phần thưởng của bước chạm

Viết 15/11/2026 cho debate "Sau khi có số test, có cần đổi hàm reward SA-SPICE-v3 nữa không?". Lập trường: nên sửa, vẫn giữ GRPO + SPICE làm lõi.

Nhãn: **[test]** tập kiểm (trích được) · **[dev]** DEV-v3 (chỉ để chọn, cấm trích) · **[sàng]** 8 mẫu SFT-cont trên 1.000 câu nhắc TRAIN-v3 (`runs/sa_spice_v3/mau_k1/`, `runs/sa_spice_v3/screen/out/sa3_screen_buoc.jsonl`) · **[tự tính]** tính hôm nay, 0 GPU · **[suy]** suy luận. Script tự tính nằm ở scratchpad phiên này (`back_adv.py`, `variants2.py`, `test_back.py`, sẽ bị xoá khi dọn máy). Nếu số nào vào luận văn thì phải chuyển script sang `harness/`.

---

## 0. Tóm tắt lập trường

Đề xuất cụ thể là **SA-SPICE-v3-NT**. Công thức của mọi câu nhắc có gold là bước chạm, type, open_app, wait, cùng mọi gold không tin được, **giữ nguyên từng byte** như SA-SPICE-v3. Chỉ phần thưởng của câu nhắc có gold *tin được* là back (36 câu nhắc) và scroll (131 câu nhắc) thay đổi, tức 16,7% tập câu nhắc [tự tính]:

- **back** (thao tác không có đối số): R = 1 nếu câu là "quay lại" (lớp `back` của verifier hoặc câu chỉ nút mũi tên back), 0,5 nếu verifier không phân loại được, 0 nếu là loại khác; trừ phạt độ dài d.
- **scroll**: R = 1[loại = scroll] · R_SA, tức cổng cứng trên đúng công thức SA. Hướng cuộn và nội dung vẫn do SPICE/chrF chấm.

Lý do không chọn SPICE-chrF-A 0,5/0,5 của báo cáo trước làm thay đổi chính có ở §4.3. Tóm lại, thay đổi đó đụng vào phần thưởng của bước chạm, trong khi đây là chỗ SA đang thắng [test] mà sàng lại từng xếp sai.

Nếu bản sửa reward chưa đủ thì bước kế là trọng số advantage cân bằng theo loại thao tác (§4.4). Lý do: dưới chuẩn hoá theo nhóm, không phép sửa reward nào nâng được tỉ phần gradient của một lớp hiếm.

Tôi phải nói thẳng ngay từ đầu: phép đo hôm nay **bác một nửa** luận điểm "reward chấm sai câu back". Trong nhóm back, reward SA đã xếp câu đúng loại trên câu sai loại ở 89% số cặp [sàng]. Lỗi thiết kế mà tôi bảo vệ được hẹp hơn, nhưng đo được (§2).

---

## 1. Sự kiện test cần giải thích

| | SA ck400 | SFT-cont | Δ (KTC95) | nguồn |
|---|---|---|---|---|
| exec bước chạm | **61,21** | 60,16 | +1,05 [+0,47; +1,65] | [test] `00_su_kien_test.md`, report/334 §2 |
| SA − ck500 | | | +0,56 [−0,04; +1,19] p=0,069 | [test] như trên |
| không chạm toàn bộ | 84,05 | 84,61 | −0,56 [−1,43; +0,33] | [test] report/334 §5 |
| **navigate_back** (n=270) | **58,52** | 71,11 | **−12,59 [−16,80; −8,49]**, cứu 3 phá 37 | [test] |
| scroll (n=755) | 80,00 | 76,82 | +3,18* | [test] |
| SA − S1, không chạm | | | −1,92 [−2,96; −0,79] (sát ngưỡng −3) | [test] |

Đếm lại 270 câu back test bằng regex động từ [tự tính, xấp xỉ, không trùng tuyệt đối với `strict_back` của `score_run`]. Kết quả: SFT-cont có 186 câu "go back", 46 câu "click/tap", 18 câu "open … app". SA ck400 có **147 câu "go back", 78 câu "click/tap"**, 24 câu "open … app". Phần mất gần như dồn hết sang câu chạm.

Đây **không phải hiện tượng của riêng lượt test này**. Trên DEV-v3, back của SFT-cont là 84/104, còn SA ck500, SA ck400 và chrF ck400 lần lượt là 56, 60, 57 [dev] (report/333 §12). Ở ck500, 22/28 câu back bị phá chỉ sang một phần tử khác, nên đây là lỗi thật, không do bộ phân loại (report/333 §12). Trên test, ck500 (GRPO + SPICE từ S1) cũng làm back tụt 72,96 → 67,04, và CTG A3 xuống 62,59 [test] (report/334 §5). Như vậy **cùng một dạng lỗi lặp lại qua ít nhất năm lượt train, hai điểm xuất phát và hai tập đánh giá**. Một hạt giống không giải thích được điều đó.

---

## 2. Reward SA có ba lỗi thiết kế ở lớp không chạm, đo được trước khi train

### 2.1 Kiểm lại tiền đề "SPICE(Go back) = 0": chỉ đúng một nửa, phần sai còn tệ hơn

Chạy jar SPICE trên máy nhà (Java `~/.jdk`, 546 câu, 11 s) [tự tính]:

| câu sinh | câu chuẩn | SPICE | chrF/100 | K_g | R_SA |
|---|---|---|---|---|---|
| Go back to the previous page | (giống hệt) | **1,00** | 1,00 | 2 | 1,00 |
| Go back | Go back | **0,00** | 1,00 | 0 | 1,00 (α=0 nên chỉ dùng chrF) |
| **Go back to the previous screen** | Go back to the previous page | **0,00** | 0,795 | 2 | **0,497** |
| Click on the close icon at the top right corner | Go back to the previous page | 0,00 | 0,149 | 2 | 0,136 |
| Click on the screen | Go back to the previous page | 0,00 | 0,126 | 2 | 0,147 |

Đọc bảng:

- SPICE("Go back","Go back") = 0 là đúng (report/320 §15–16), nhưng SA đã né ca này nhờ định tuyến theo K_g (K_g = 0 nên α = 0). Phải nói đúng như vậy với bên kia: đây **không** phải lỗi của SA.
- Lỗi thật là **đồng nghĩa page/screen**. Một câu back đúng loại, đúng nghĩa, chỉ khác danh từ "screen" và "page", bị SPICE chấm 0. Khi đó SA chỉ còn 0,497. Trong khi đó, trong câu chuẩn back của TRAIN-v3, "previous page" và "previous screen" cùng là dạng phổ biến nhất (đếm `back_adv.py`: "Go back to the previous page" 6+6+5 lần, "previous screen" 4+2 lần, "home screen of the app" 4 lần) [tự tính].

### 2.2 Lỗi 1: nhiễu từ ngữ làm GRPO đẩy *xuống* câu back đúng loại

Back là thao tác **không có đối số**: luật `strict_back` chỉ chấm loại, không chấm "previous page" hay "previous screen". Vậy mà SA vẫn chấm phần chữ của câu back bằng SPICE/chrF, nên trong một nhóm 8 câu đều đúng loại, phần thưởng vẫn dao động theo cách chọn danh từ. Dưới advantage chuẩn hoá theo nhóm, những câu đúng loại nằm dưới trung bình nhóm nhận advantage âm, và gradient của chúng **kéo xuống cả tiền tố "Go back"**.

Đo trên 39 nhóm back của sàng (8 mẫu SFT-cont, advantage z theo nhóm như `scale_rewards="group"`) [sàng, tự tính, `variants2.py`]:

| reward trên nhóm back | câu đúng loại nhận advantage âm | Σ advantage của câu đúng loại (lực đẩy ròng lên loại back) |
|---|---|---|
| SA-SPICE-v3 hiện tại | **70/197 (36%)** | 52,9 |
| SA, A = 0 khi sai loại | 69/197 | 54,9 |
| SA với cổng cứng (sai loại thì R = 0) | 69/197 | 55,7 |
| **back chỉ chấm loại (đề xuất)** | **8/149 (5%)** | **68,3 (+29%)** |

(Ghi chú: 149 là số câu đúng loại của 36 nhóm có gold tin được và độ lệch chuẩn khác 0. SA đếm cả 3 nhóm không tin được và 12 nhóm toàn câu đúng mà SA vẫn có phương sai do nhiễu chữ. Đúng điều này là một phần của lỗi: ở 12 nhóm toàn câu đúng, SA vẫn sinh gradient thuần nhiễu từ ngữ trên câu back.)

Cơ chế không có gì bí ẩn. Advantage z-score bất biến với mọi phép biến đổi affine của reward trong nhóm, nên "cường độ" tín hiệu loại thao tác bằng *tỉ lệ* giữa chênh lệch do loại và tổng phương sai trong nhóm. Nhiễu từ ngữ trong cùng một loại làm phình mẫu số, nên làm loãng tín hiệu loại. Bỏ nhiễu ấy ở thao tác không có đối số thì toàn bộ phương sai còn lại là phương sai loại [suy, nhưng là hệ quả trực tiếp của công thức chuẩn hoá].

### 2.3 Lỗi 2: thành phần A không bao giờ phạt, nên không gánh được gì

Verifier v3: gold tin được, câu khác loại thì A = 0,5, đúng loại thì A = 1 (`harness/sa3_action_verify.py`, `score_action`). Chênh tối đa trên thang reward là 0,2 × 0,5 = 0,1. Đo trên 7.558 cặp RAFT, toggle bằng 0, nên A ∈ {0,5; 1} trong thực tế (report/333 §11, dòng 135).

Lý do nới A xuống 0,5 là pilot người chấm: 7 dòng lệch là "đường đi khác hợp lý" (report/333 dòng 131). Mở lại chính tệp pilot (`runs/sa_spice_v3/audit_pilot2/human_labels.jsonl` × `audit_key.jsonl`, 40 dòng người chấm) và tách theo loại gold [tự tính]:

| gold | dòng verifier chấm sai loại | người: sai | người: đúng / không rõ |
|---|---|---|---|
| **scroll** | 4 | **4** | 0 |
| **back** | 5 | 3 | 2 (một là "back icon", nay đã do `back_equiv` xử lý; một là "menu icon" dẫn tới cùng chức năng) |
| tap | 5 | 2 | 3 |
| type | 2 | 1 | 1 |
| open_app | 4 | 3 | 1 |

Vậy các "đường đi khác hợp lý" dồn ở gold tap/type. Với gold scroll, 4/4 câu khác loại là sai thật. Với gold back, nếu coi câu chỉ nút back là back thì 3/4 sai thật. Claude-audit trên cùng pilot 2 cũng cho back|known_wrong 29/30, scroll|known_wrong 30/30 (`audit_result.json`).

⇒ **Quyết định nới A = 0,5 cho mọi loại là quyết định dựa trên bằng chứng của tap/type, áp đồng loạt cho cả scroll/back, nơi chính dữ liệu pilot (có từ 11/11, trước mọi số dev/test) nói ngược lại.** Đây là lỗi thiết kế thứ hai, và bằng chứng cho nó có từ trước test.

Trên bước scroll, cổng cứng tăng thứ tự loại từ 0,938 lên 0,968, giảm tỉ lệ câu sai loại nhận advantage dương từ 9,7% xuống 4,4%, và tăng lực đẩy ròng lên loại scroll từ 148,6 lên 174,9 (+18%) [sàng].

### 2.4 Lỗi 3 (cấu trúc): dưới chuẩn hoá nhóm, reward không thể cứu một lớp hiếm

Với chuẩn hoá nhóm, nhân reward của câu nhắc back lên bao nhiêu lần thì advantage cũng không đổi. Tỉ phần khối |advantage| mà nhóm back nhận được trong toàn tập 1.000 câu nhắc chỉ là **3,9%** với SA, còn tap nhận 68,4% [sàng]. Không biến thể reward nào nâng được con số này (bản đề xuất còn hạ xuống 3,0%, vì nhóm back toàn câu đúng nay cho gradient 0).

Trong khi đó, reward vẫn "biết" câu nào đúng ngay ở những bước test bị phá. Trên 39 bước test mà SFT-cont nói back còn SA ck400 không nói back (đếm regex), R_SA của câu SFT-cont là **0,737**, còn của câu SA là **0,169**, chênh 0,568 [tự tính, `test_back.py`]. Vậy điểm hỏng không nằm ở thứ hạng mà nằm ở chỗ: (a) lực đẩy loại thao tác bị nhiễu chữ làm loãng (2.2), (b) A không phạt (2.3), và (c) lớp back chỉ có 39 lần được nhìn thấy trong 500 update, trong khi 616 nhóm tap kéo phong cách "Click on …" lan ra mọi màn hình [suy, chưa đo trực tiếp lan truyền chéo câu nhắc].

Đây chính là hiện tượng mà **MT-GRPO (ICML 2026)** mô tả cho GRPO đa nhiệm: một số nhiệm vụ chiếm hết quá trình tối ưu trong khi nhiệm vụ khác đứng yên, và mỗi nhiệm vụ có tỉ lệ advantage bằng 0 khác nhau nên đóng góp thực của nó bị bóp méo. Cách chữa của họ là trọng số nhiệm vụ thích ứng cộng bộ lấy mẫu giữ tỉ lệ. Họ báo worst-task tăng 16–28 điểm tuyệt đối so với GRPO và 6 điểm so với DAPO ([arXiv 2602.05547](https://arxiv.org/abs/2602.05547), ICML 2026, đã kiểm trang ICML). Ở bài này, loại thao tác đóng vai nhiệm vụ, và back là nhiệm vụ kém nhất.

---

## 3. Tiền lệ cho từng thay đổi

| thay đổi | tiền lệ | trạng thái nguồn |
|---|---|---|
| back chỉ chấm loại, không chấm chữ | UI-R1: R = R_T + R_C + R_F, R_T = 1 khi loại khớp. Back (`navigate_back`) là một trong năm loại, chỉ có phần thưởng loại, còn tọa độ chỉ chấm cho click | [arXiv 2503.21620](https://arxiv.org/html/2503.21620); AAAI-26, Proc. AAAI 40(21):17608–17616 (theo trang OJS/kết quả tìm kiếm; trang OJS chặn bot nên chưa mở trực tiếp) |
| cổng cứng: sai loại thì phần thưởng tham số bằng 0 | InfiGUI-R1: R_param = 1 chỉ khi loại *và* mọi tham số khớp; R_acc chỉ tính khi định dạng đúng (cổng phân tầng). Trọng số loại/tham số 0,2/0,8 | [arXiv 2504.14239](https://arxiv.org/abs/2504.14239), preprint |
| thưởng loại nhị phân trong GRPO cho GUI | GUI-R1: R_acc = R_act + R_point + R_text, R_act nhị phân | [arXiv 2504.10458](https://arxiv.org/abs/2504.10458), preprint |
| cân bằng lớp hiếm khi train GRPO trên AndroidControl | Magma-R1 ("Action Type Proportional Optimization"): lấy mẫu phân tầng theo loại thao tác, P_target(a) > P_orig(a) cho type/scroll…, vì "model over-focus on high-frequency actions". Bài không có bảng ablation riêng cho phần này (đã đọc bản PDF) | [arXiv 2510.18488](https://arxiv.org/abs/2510.18488), preprint |
| trọng số theo nhiệm vụ trong GRPO | MT-GRPO, như §2.4 | ICML 2026 |
| neo chống trôi | Luo & Shakhnarovich CVPR 2017; Lazaridou ACL 2020 (đã trích ở báo cáo trước) | đã bình duyệt |

Không tìm được bài nào nghiên cứu đúng hiện tượng "back/scroll sụp thành câu chạm khi tối ưu độ đo văn bản". Ghi chú cũ `grounding_action_rewards.md` Q4 cũng ghi như vậy, và tra lại hôm nay vẫn thế. Cầu nối từ GUI agent (sinh hành động) sang sinh câu hướng dẫn là [suy].

---

## 4. Đề xuất cụ thể

### 4.1 Đề xuất chính: SA-SPICE-v3-NT (chỉ sửa reward, một họ thay đổi)

Ký hiệu như `harness/sa3_reward_screen.py`: s = SPICE F1, c = chrF/100, d = phạt độ dài, α_g = 0,8·min(1, K_g/3), A theo verifier v3, `cls` = `sa3_action_verify.classify`.

```
R_SA(y)  = clip(0,8·(α_g·s + (1−α_g)·c) + 0,2·A − d, 0, 1)          # giữ nguyên

nếu gold không tin được, hoặc canon(gold) ∉ {back, scroll}:  R = R_SA(y)

nếu canon(gold) = back và gold tin được:
    b(y) = 1    nếu cls(y) = "back" hoặc y khớp BACK_TGT (nút/mũi tên back)
         = 0,5  nếu cls(y) là None
         = 0    còn lại
    R = max(0, b(y) − d)

nếu canon(gold) = scroll và gold tin được:
    R = R_SA(y)  nếu cls(y) = "scroll",   R = 0  nếu cls(y) ∉ {None, "scroll"},   R = R_SA(y) nếu None
câu sinh trống: R = 0
```

Mọi thứ khác giữ nguyên như lượt SA: điểm xuất phát SFT-cont, KL β = 0,04, 1.000 câu nhắc TRAIN-v3 cùng thứ tự, G = 8, `loss_type="dapo"`, `scale_rewards="group"`, 500 update, seed 101, chọn điểm lưu theo tiêu chí khả thi trên DEV-v3.

Mỗi thay đổi gắn với bằng chứng nào:

| thay đổi | bằng chứng | có trước test? |
|---|---|---|
| back chỉ chấm loại | SPICE(screen vs page) = 0; 36% câu back đúng loại nhận advantage âm; `strict_back` chỉ chấm loại | cơ chế đo hôm nay trên dữ liệu sàng có từ 11/11; vấn đề back thấy trên dev 15/11 |
| scroll cổng cứng | người chấm 4/4 câu khác loại ở gold scroll là sai; Claude-audit 30/30 | **có** (pilot 11/11) |
| BACK_TGT tính là back | người chấm "Click on the back icon" là đúng | **có** (pilot 11/11) |
| không đụng gold tap/type/open_app/wait | 3/5 + 1/2 dòng khác loại ở tap/type là đường đi hợp lý; giữ nguyên chỗ SA đang thắng [test] | có |

Tính chất đáng giá nhất khi trình hội đồng: **phần thưởng của 83,3% câu nhắc trùng từng byte với SA**. Nếu exec bước chạm thay đổi, thay đổi ấy chỉ có thể đến gián tiếp qua lớp không chạm. Đây là phép so gần với một biến nhất có thể có, và SPICE vẫn chi phối phần thưởng của mọi bước chạm, nên tên "GRPO + SPICE" vẫn đúng.

### 4.2 Biến thể mềm, nếu hội đồng phản đối việc "bỏ SPICE ở bước back"

R_back = b(y)·(0,5 + 0,5·R_SA(y)). Câu đúng loại có R ∈ [0,5; 1], câu sai loại có R = 0. Biến thể này giữ một phần tín hiệu chữ, nhưng vẫn để lại nhiễu page/screen, chỉ còn một nửa. Tôi không chọn nó làm bản chính, vì §2.2 cho thấy chính nhiễu ấy là cái làm loãng tín hiệu loại.

### 4.3 Vì sao không đổi α sang 0,5/0,5 (SPICE-chrF-A) cùng lúc

- Thay đổi đó sửa *bước chạm*, chỗ SA đã cho số test cao nhất (61,21), dựa trên một sàng đã xếp sai ba lần, trong đó có lần xếp chrF trên SA mà sau train hai bên ngang nhau [dev]. Báo cáo trước tự ghi điều này.
- Gộp hai thay đổi thì không quy công được: back hồi phục mà exec chạm tụt sẽ không biết do cái nào.
- Trên dev, SA còn thắng chrF ở độ đo văn bản (SPICE +1,63, CIDEr-D +18,37 [dev], report/334 §6d). Giảm SPICE xuống 50% là đi ngược bằng chứng sau train duy nhất đang có.

⇒ Nếu muốn thử SPICE-chrF-A thì chạy *sau* NT và *trên nền* NT, như một lượt riêng.

### 4.4 Bước kế nếu 4.1 chưa đủ: trọng số advantage cân bằng theo loại (MT-GRPO tĩnh)

Â_i ← w_k · Â_i, với w_k = min(3, √(p_click / p_k)) tính từ tần suất câu nhắc TRAIN-v3 (click 0,616, scroll 0,135, back 0,039). Kết quả là w_back = 3, w_scroll ≈ 2,1, các lớp khác w = 1 trừ khi công thức cho > 1 [suy, hằng số chọn trước khi có số dev của lượt này, phải khai].

Phép này tương đương kỳ vọng với việc lấy mẫu back nhiều gấp 3 lần mà không cần câu nhắc mới. Nó thuộc mục tiêu GRPO chứ không thuộc hàm reward, nên khi trình phải gọi là "GRPO + SPICE với cân bằng loại thao tác". Đây là chỗ duy nhất có thể nâng tỉ phần 3% của §2.4. Tôi xếp nó sau 4.1 vì nó đổi mô tả phương pháp và chưa có tiền lệ đã bình duyệt trong miền GUI (MT-GRPO là đa nhiệm suy luận).

### 4.5 Luật đi/dừng ghi trước

| bước | máy | luật |
|---|---|---|
| 0 | CPU | chuyển `variants2.py`/`test_back.py` vào `harness/`, thêm selftest cho công thức NT (tap gold cho ra đúng R_SA từng byte) |
| 1 | Kaggle T4, khoảng 3 phiên | train NT 500 update; log riêng tỉ lệ nhóm back/scroll có cả câu đúng lẫn sai loại theo từng 50 update |
| 2 | Kaggle T4 | DEV-v3 ck300/400/500. **Đi tiếp lên test** khi: back ≥ 72/104 (tụt ≤ 12 so với 84 của SFT-cont, thay vì 24–28 như SA/chrF), không chạm toàn bộ tụt ≤ 2, và exec bước chạm ≥ SA ck400 − 0,5 trên dev. **Back dev ≤ 64** ⇒ reward không phải đòn bẩy, chuyển 4.4 |
| 3 | T4, một lần | chấm test, báo vô điều kiện, ghép cặp với SA ck400 và SFT-cont ở cả bước chạm lẫn không chạm |

---

## 5. Lợi ích kỳ vọng, tất cả là [suy]

| đại lượng | SA ck400 [test] | NT kỳ vọng | căn cứ |
|---|---|---|---|
| navigate_back | 58,52 | **65–71** (+6 đến +12,6) | SA phá 37/cứu 3; nếu lấy lại 40–100% phần phá. Mức trên = SFT-cont 71,11 |
| scroll | 80,00 | 80–81 | cổng chỉ tăng lực đẩy loại scroll thêm 18%; SA đã +3,18 so SFT-cont |
| không chạm toàn bộ | 84,05 | **84,7–85,4** | +16 đến +34 bước back trên 2.495 bước |
| không chạm − S1 | −1,92 | khoảng −0,6 đến −1,3 | 85,97 của S1 |
| exec bước chạm | 61,21 | **61,2 ± 0,9** (khoảng A/A) | reward của 83% câu nhắc giữ nguyên; không có cơ chế nào để tăng exec chạm, rủi ro là giảm nhẹ nếu gradient lớp không chạm lan sang |

Nói gọn bằng số: **NT không hứa thêm exec. Nó hứa xoá cái −12,59 ở back mà không trả bằng exec.** Với yêu cầu "số cải thiện nhất", lợi ích nằm ở chỗ mô hình tiêu đề hết còn một tác hại có KTC loại 0 mà hội đồng chắc chắn sẽ hỏi (−12,59 [−16,80; −8,49]). Cộng thêm là SPICE toàn tập: trên dev, SA làm SPICE toàn bộ giảm −1,01, chủ yếu do bước không chạm, trong khi trên bước chạm SPICE chỉ đổi −0,29 và không có ý nghĩa [dev] (report/334 §6d). Một phương pháp lấy SPICE làm lõi mà làm *giảm* SPICE toàn tập thì khó bảo vệ. Sửa bước không chạm có thể gỡ được điều này [suy].

---

## 6. Tự phản biện

**Điểm yếu 1, mạnh nhất: SA đã là số test cao nhất, đổi sau khi thấy test là chọn theo test.**
Trả lời: (a) Tác hại back thấy trên DEV-v3 từ 15/11 *trước* khi mở test (84 → 56–60/104 ở cả ba lượt), và report/333 §13 đã ghi "phải khai" điều đó. Test chỉ xác nhận. (b) Bằng chứng cho cổng scroll/back nằm trong pilot người chấm 11/11, trước cả lúc train. (c) NT không đụng phần thưởng của bước chạm, nên không thể bị cáo buộc "dò thước chạm theo test". (d) Số tiêu đề vẫn là SA ck400 = 61,21, báo vô điều kiện; NT được trình là một lượt sửa có khai rõ thời điểm quyết. Cái không né được: quyết định *chạy* NT được thúc đẩy bởi số test back, và phải viết đúng như vậy.

**Điểm yếu 2: trong nhóm back, reward sửa đổi gần như không đổi thứ tự.** Thứ tự loại chỉ từ 0,892 lên 0,899 [sàng], và reward SA đã chênh 0,568 giữa câu đúng và câu sai ở chính các bước test bị phá. Có thể lỗi hoàn toàn nằm ngoài reward (tần suất 3,9%, lan truyền từ nhóm tap), và báo cáo trước đã kết luận như vậy.
Trả lời: chỉ số đúng để nhìn không phải thứ tự mà là lực đẩy ròng sau chuẩn hoá: câu back đúng loại bị đẩy xuống ở 36% số mẫu, giảm còn 5%, và Σadvantage lên loại back +29%. Dù vậy tôi thừa nhận +29% trên 3% khối gradient có thể vẫn không đủ. Vì thế luật bước 2 có nhánh rẽ rõ sang 4.4, và 4.4 được dẫn từ chính số đo 3,9% này chứ không phải thêm sau.

**Điểm yếu 3: một hạt giống, biến thiên A/A khoảng 0,9 exec.**
Trả lời: hiệu ứng cần đo là back, cỡ −12,59 với KTC hẹp, gấp khoảng 14 lần biến thiên A/A *của exec*. Trên 270 bước ghép cặp, SE khoảng 2 điểm, nên hồi phục ≥ +6 thì một hạt vẫn thấy được. Còn exec chạm, NT chỉ cần "không kém", và đó cũng là câu được phép viết. Điểm yếu còn lại: chưa có số biến thiên giữa lượt *của back* (A/A chưa chấm không chạm). Nếu back dao động ±10 giữa hai lượt cùng cấu hình thì toàn bộ lập luận yếu đi; xem mục "đổi ý".

**Điểm yếu 4: CTG-GRPO (cộng z(đúng loại) vào advantage) làm back xấu hơn −2,96 [test].**
Trả lời: report/279 dòng 162–167 ghi λ_back của A3 **về 0 từ bước 150**, vì đích lấy mẫu 0,707 thấp hơn độ đúng greedy. CTG vì vậy chưa từng thử lực đẩy back trong 85% lượt train, nên không bác được một phần thưởng loại cố định. CTG còn là phần cộng thích ứng vào advantage, không phải cổng trong reward.

**Điểm yếu 5: bỏ chữ ở bước back làm giảm độ đo văn bản của câu back** (mệnh đề mục đích kiểu "to view the share option").
Trả lời: back là 270/6.958 bước test, và đa số câu chuẩn back không có mệnh đề mục đích. Ảnh hưởng lên độ đo văn bản toàn tập nhỏ [suy]. Nếu hội đồng coi trọng điều này thì dùng 4.2.

**Điểm yếu 6: verifier là regex.** "Click on the close icon" có thể là một đường quay lại hợp lệ, và người chấm từng chấm "menu icon" là đúng.
Trả lời: dữ liệu dev cho thấy 22/28 câu bị phá chỉ sang phần tử khác, là lỗi thật (report/333 §12). Thước `strict_back` cũng chấm các câu ấy là sai. Cổng chỉ phạt đúng những gì thước chấm phạt.

---

## Ba luận điểm mạnh nhất

1. **Lỗi lặp lại, không phải nhiễu.** Back tụt ở mọi lượt GRPO đã đo (ck500 test −5,93 so S1, CTG −10,37, SA test −12,59 so SFT-cont, ba lượt dev 84 → 56–60/104). Cùng một dạng lỗi qua năm lượt, hai điểm xuất phát, hai tập đánh giá. Reward hiện tại không có cơ chế nào chặn nó, vì A tối đa chỉ chênh 0,1 và không bao giờ phạt.
2. **Hai lỗi thiết kế đo được, có bằng chứng từ trước test.** (a) Nới A = 0,5 dựa trên các ca tap/type, trong khi chính pilot người chấm 11/11 cho gold scroll 4/4 và gold back 3/4 câu khác loại là sai thật. (b) Chấm chữ cho một thao tác không có đối số khiến SPICE(screen vs page) = 0, và 36% câu back đúng loại bị GRPO đẩy xuống. Sửa cả hai làm Σadvantage lên loại back +29% và loại scroll +18%.
3. **Sửa mà không đụng chỗ đang thắng.** NT giữ nguyên phần thưởng của 83,3% câu nhắc, gồm mọi bước chạm, nên SPICE vẫn là lõi và exec chạm 61,21 không bị đặt cược. Kỳ vọng là xoá phần lớn −12,59 ở back (về 65–71) với exec chạm trong khoảng A/A [suy]. Nếu không đủ, bước kế (cân bằng advantage theo loại) có tiền lệ đã bình duyệt gần nhất là MT-GRPO, ICML 2026.

## Điều sẽ khiến tôi đổi ý

- **Biến thiên back giữa hai lượt cùng cấu hình ≥ 8 điểm.** Chấm không chạm cho A/A, hoặc ck500/202, trên test. Nếu back dao động cỡ đó thì −12,59 của SA không đặc thù cho reward. Phép đo này rẻ (suy luận 2.495 bước, khoảng 1,7 h T4) và nên chạy *trước* NT.
- **Log train cho thấy nhóm back sụp thành toàn câu sai loại rất sớm.** Ví dụ đa số nhóm back sau update 150 không còn câu "back" nào. Khi đó mọi reward đều cho gradient 0, NT vô dụng, và chỉ còn neo SFT hoặc lấy mẫu phân tầng.
- **DEV-v3 của NT có back ≤ 64/104**, tức không khá hơn SA rõ rệt. Khi đó tôi chấp nhận kết luận của báo cáo trước: đòn bẩy nằm ở phân bố câu nhắc, không ở reward.
- **NT làm exec chạm trên dev giảm > 1 so với SA ck400.** Khi đó cái giá ở bước chạm là thật và lớn hơn lợi ích ở back theo tiêu chí "số cải thiện nhất" của user. Giữ SA, khai tác hại back.

---

## Nguồn web đã mở hoặc kiểm hôm nay

- UI-R1, [arXiv 2503.21620 (HTML)](https://arxiv.org/html/2503.21620); kết quả tìm kiếm ghi AAAI-26, Proc. AAAI 40(21):17608–17616, DOI 10.1609/aaai.v40i21.38816 ([OJS](https://ojs.aaai.org/index.php/AAAI/article/view/38816), trang chặn bot, chưa mở trực tiếp được). R_T nhị phân trên Click/Scroll/Back/Open_App/Input_Text; tập train mobile 136 mẫu, Click chiếm 101.
- MT-GRPO, [arXiv 2602.05547](https://arxiv.org/abs/2602.05547), "Accepted at ICML 2026", có trang poster [icml.cc](https://icml.cc/virtual/2026/poster/60544).
- AndroidControl-Curated / Magma-R1, [arXiv 2510.18488](https://arxiv.org/abs/2510.18488), preprint. Đã đọc PDF mục 2.2.2 (Action Type Proportional Optimization: lấy mẫu phân tầng theo P_target), không có ablation số cho phần này.
- InfiGUI-R1 [arXiv 2504.14239](https://arxiv.org/abs/2504.14239) và GUI-R1 [arXiv 2504.10458](https://arxiv.org/abs/2504.10458): preprint, chi tiết reward lấy từ ghi chú `grounding_action_rewards.md` Q3, chưa mở lại hôm nay.
- Danh sách bổ sung chưa mở, không trích: OneThinker (arXiv 2512.03043, chuẩn hoá advantage theo nhiệm vụ bằng EMA std), Chem-R (arXiv 2510.16880).
