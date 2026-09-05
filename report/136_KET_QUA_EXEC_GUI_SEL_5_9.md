# 136 — KẾT QUẢ `exec` CỦA `gui_sel`/101 (đo 5/9/2026)

> Lượt Kaggle commit đêm 4→5/9 chạy trọn cả hai phần. Đây là **lần đầu tiên** nhánh ứng-viên được
> chấm bằng thước primary. Mọi số dưới đây tính từ `runs/sel/score_gui_sel_seed101_raw.jsonl`,
> n = 4.463 bước chạm. Luật đọc: `report/106` mục **(x16)** · khung: `report/134`.
>
> ⚠️ **Chưa có đối chứng `gui_sft_match`/101** (cần một lượt A100). Vì vậy file này báo **mức
> tuyệt đối và chẩn đoán**, **không** báo `Δ_sel`.

## 1. Ba hàng thước

Bootstrap cụm theo app (1.091 cụm, G hiệu dụng 454,3), cùng thủ tục với mọi nhánh trước.

| luật spatial | Human | MIN-DESC/101 | S1/101 | Base | **`gui_sel`/101** | KTC95 cụm |
|---|---|---|---|---|---|---|
| **Voronoi .14** (primary, prereg) | 75,73 | 60,05 | 59,11 | 47,59 | **56,13** | [54,52 · 57,99] |
| nL2 .14 (secondary, nhánh khoảng cách AITW) | 84,09 | 68,32 | 66,92 | 55,28 | **63,52** | [61,88 · 65,32] |
| chữ nhật .14 (hàng khớp mã) | 84,23 | 68,72 | 67,24 | 55,86 | **63,86** | [62,16 · 65,60] |

Thành phần: `action_ok` **90,90%** · `toggle_ok` **99,66%** · `hit_voronoi` thuần **57,36%** ·
`hit_disk` thuần **66,35%**. Câu rỗng **11/4.463** (0,25%), vào quần thể với `exec = 0` đúng luật.

⚠️ **Bẫy tên trường:** `exec_disk` trong tệp JSON của `score_run.py` là `hit_disk` **thuần**,
**không** gated. Hàng "chữ nhật .14" của bảng phải tính lại từ tệp thô với
`action_ok ∧ toggle_ok ∧ hit_disk`. Đã kiểm chéo trên bốn nhánh cũ: bảng `134` §3.1 dùng đúng
số gated (S1 67,24 chứ không phải 69,17), nên bảng đó **không sai**; chỗ dễ nhầm là đọc thẳng
JSON. Con số ungated của `gui_sel` là **66,35**, ⛔ cấm gọi là executability.

**Hai dự đoán trước khi chạy đều đúng hướng** (`134` mục 10): Voronoi ≥ 65 — **không** (56,13);
nL2 ≥ 70 — **không** (63,52). Kỳ vọng cũ 63,7–65,1 pp của kế hoạch tháng 8 đã chết từ lúc G6
trượt, và số thật xác nhận: **56,13**.

## 2. ⭐ Phát hiện chính: cơ chế chọn KHÔNG hỏng, cái hỏng là BỎ CUỘC QUÁ MỨC

Bảng 2×2 chéo giữa *có ứng viên vàng trong khối* và *mô hình có dám chọn*:

| nhóm | n | % tập | `exec` | `action_ok` |
|---|---|---|---|---|
| **HasAns · dám chọn** | 2.326 | 52,1% | **71,41%** [69,54 · 73,21] | 99,14% |
| **HasAns · BỎ CUỘC (sai)** | 872 | 19,5% | **23,74%** [21,03 · 26,67] | 71,22% |
| NoAns · dám chọn (sai) | 264 | 5,9% | 37,50% | 99,62% |
| NoAns · bỏ cuộc (đúng) | 1.001 | 22,4% | 53,75% | 86,61% |

· **Khi mô hình dám chọn và có đáp án, nó đạt 71,41%** — cao hơn MIN-DESC (60,05), cao hơn S1
  (59,11), và chỉ kém mốc câu người **4,3 pp**. Cơ chế đầu chọn hoạt động đúng như thiết kế.
· **27,27% số bước có đáp án vàng vẫn bị bỏ cuộc** (872/3.198). ⭐ Con số này **tái lập chính
  xác** mức 27,1% đo trên lát dev 1.400 hôm 3/9 — hai phép đo độc lập, mẫu chênh nhau ba lần.
· Toàn tập: bỏ cuộc **41,97%** (1.873 bước), `exec` nhóm đó **39,78%** so với **67,95%** ở nhóm
  dám chọn, chênh **+28,18 pp**.

**Nếu triệt tiêu được vế bỏ-cuộc-sai** (nhóm 872 bước đạt `exec` bằng nhóm HasAns-dám-chọn):
`exec` toàn tập **56,13 → 65,44 pp**, tức **+9,31 pp**. Đây là ước trần, không phải kết quả.
Cùng dạng lập luận với chẩn đoán MIN-DESC (`106` mục x10b) vốn cho +5,4 pp.

## 3. Bốn dấu hiệu của bỏ cuộc — cả bốn đều đo được

**① Lẫn loại thao tác.** Câu mang động từ không-chạm (swipe/scroll/back/type/…): **28,30%** ở
nhóm bỏ cuộc so với **0,97%** ở nhóm dám chọn — **gấp 29 lần**. Tái lập chẩn đoán trên lát dev
(39,6% vs 2,0%, gấp 20 lần) và chẩn đoán 4j-18 từ tháng 8. `action_ok` của nhóm HasAns-bỏ-cuộc
chỉ **71,22%** so với 99,14% của nhóm dám chọn.

**② Nhìn sang vùng khác hẳn màn.** Sai số bộ trỏ tính theo phần bề ngang:

| nhóm | n | trung vị | p75 | p90 |
|---|---|---|---|---|
| dám chọn | 2.579 | **0,78%** | 13,22% | 46,46% |
| bỏ cuộc | 1.873 | **19,90%** | 70,73% | 135,94% |

Trung vị chênh **25 lần**, và p90 của nhóm bỏ cuộc vượt 100% bề ngang, tức trỏ sang phần khác
của màn. Đây là dạng lỗi **lưỡng cực** đã gặp ở MIN-DESC (x13c), không phải lẫn giữa hai nút
cạnh nhau.

**③ ⭐ Khối ứng viên càng đông càng dễ bỏ cuộc — đơn điệu, và chưa từng đo trước đây.**
Chỉ tính nhóm HasAns:

| cỡ khối | n | tỉ lệ bỏ cuộc | `exec` |
|---|---|---|---|
| 1–5 | 178 | 18,5% | 70,79% |
| 6–10 | 363 | 15,7% | 70,52% |
| 11–20 | 826 | 25,9% | 60,29% |
| 21–39 | 1.036 | 29,3% | 55,60% |
| **40 (chạm trần cap)** | 795 | **33,2%** | **51,82%** |

Bỏ cuộc tăng đơn điệu từ 15,7% lên 33,2%; `exec` giảm đơn điệu từ 70,8% xuống 51,8%. Nhóm chạm
trần 40 chiếm **17,8%** tập kiểm và là nhóm tệ nhất.
⚠️ Đây là **quan hệ tương quan trên lát cắt hậu kiểm**, không phải phép can thiệp: màn nhiều
phần tử cũng là màn khó hơn về bản chất. Muốn tách hai vế phải chạy một nhánh có prune/rank —
việc đã bị `134` cấm trước 16/9. Gắn nhãn **thăm dò** nếu đưa vào bài.

**④ App chưa thấy lúc dạy thì bỏ cuộc nhiều hơn:** 51,3% so với 41,8% (n = 78, dải hẹp nên chỉ
là gợi ý). `exec` 51,28% so với 56,76%.

**Một cách giải thích đã bị loại:** độ dài câu. Trung vị **33 ký tự ở cả hai nhóm**, p10 22/22,
p90 65 vs 62. Bỏ cuộc không đi kèm câu ngắn hơn hay dài hơn.

## 4. So ghép cặp với các nhánh cũ — ⛔ ĐỌC KÈM ĐIỀU KIỆN

Cùng 4.463 bước, McNemar ghép cặp:

| nhánh | nhánh đó | `gui_sel` | chênh | b | c | p |
|---|---|---|---|---|---|---|
| Human | 75,73 | 56,13 | −19,61 | 101 | 976 | 2,9e−156 |
| MIN-DESC/101 | 60,05 | 56,13 | −3,92 | 270 | 445 | 7,7e−11 |
| CE2-S2/101 | 59,42 | 56,13 | −3,29 | 281 | 428 | 4,2e−08 |
| S1/101 | 59,11 | 56,13 | −2,98 | 207 | 340 | 1,7e−08 |
| S2/101 | 57,18 | 56,13 | −1,05 | 287 | 334 | 6,5e−02 |
| Base | 47,59 | 56,13 | **+8,54** | 731 | 350 | 6,8e−31 |

⛔ **Không hàng nào trong bảng này là `Δ` hợp lệ**, trừ hàng Base đọc như *mức so với mô hình
chưa tinh chỉnh*. Lý do: `gui_sel` lệch **ba biến** so với S1 cũ — `cutoff_len` 3072 vs 2560 ·
đầu vào có khối ứng viên vs 24 dòng OCR · 1 epoch vs 2. Đây đúng loại so bắc cầu mà `123` §9.1
cấm và `106` mục (x15c) điểm 2 cấm lần nữa. Đối chứng hợp lệ duy nhất là **`gui_sft_match`/101**,
cùng ba biến đó, **chưa chạy**.

## 5. Hai phép kiểm toàn vẹn

· **Lát dev đã nhìn vs phần chưa nhìn:** `exec` **55,43%** (n=1.400) so với **56,45%** (n=3.063).
  Chênh 1,02 pp, nằm gọn trong nhiễu. Không có dấu hiệu lát dev bị ưu ái, và cũng cho thấy việc
  đã đọc số trên lát dev hôm 3/9 không làm lệch phần còn lại.
· **Truy nguyên:** bốn tệp mã chạy trên Kaggle (`infer_branch.py`, `score_run.py`,
  `metric_exec.py`, `seq_score_sel.py`) **trùng md5 từng byte** với bản trên máy. Chữ ký lượt
  chạy đồng nhất `lora:gui-sel-adapter` trên cả 4.463 bản ghi. Hai hash artifact đã kiểm ngay
  trong notebook trước khi chạy.

## 6. Đọc kết quả này thế nào

**Được nói:**
· `exec` tuyệt đối **56,13%** [54,52 · 57,99] trên 4.463 bước, đọc trong khung **12,0 → 75,73**
  chứ không đọc trên nền 100.
· Điểm nghẽn là **bỏ cuộc quá mức**, không phải định vị sai: khi dám chọn và có đáp án thì đạt
  **71,41%**, cách mốc câu người 4,3 pp; 27,27% bước có đáp án bị bỏ.
· Bốn dấu hiệu của bỏ cuộc, trong đó ba tái lập hiện tượng đã đo trước đó bằng dữ liệu độc lập.
· Cổng đăng ký trước đã trượt và **không được nới**; số cũng không cứu cổng.

**Không được nói:**
· `Δ_sel` bất kỳ dạng nào — chưa có đối chứng.
· `gui_sel` "kém S1" — lệch ba biến, so bắc cầu bị cấm.
· "khối ứng viên gây hại" — cần `S1-match` mới tách được công của menu, lượt đó đã bị bỏ.
· Lấy hàng nL2 63,52 làm headline vì nó cao hơn Voronoi.
· Gọi quan hệ cỡ-khối ↔ bỏ-cuộc là quan hệ nhân quả.

## 7. Việc kế

1. **Sequence-score trên lát dev 1.400** (`seq_score_sel.py`, T4). Đây là lượt duy nhất còn có
   thể đổi kết luận: nếu ngưỡng τ theo (x16d) kéo được một phần trong 872 bước bỏ-cuộc-sai về
   phía chọn, `exec` có đường lên tới ~65. Khoá τ **trước** khi nhìn bất cứ số nào khác.
2. **Một lượt A100 cho `gui_sft_match`/101** — thứ duy nhất cho phép nói `Δ`.
3. Viết abstract 9/9. Con số headline nay **đã có tệp trên đĩa**: 56,13 · 71,41 · 27,27 · 41,97
   · 28,30/0,97 · +9,31.

---

## 8. DỰ ĐOÁN VỀ NGƯỠNG τ — ghi 5/9, **TRƯỚC** khi tính điểm sequence-score đầu tiên

Ghi ở đây để về sau không đọc ngược kết quả. Thủ tục chọn τ đã khoá ở `106` mục **(x16d)**;
mục này **không** thêm ràng buộc nào, chỉ nêu kỳ vọng.

**Kỳ vọng: τ cải thiện ÍT, khoảng 0 đến 3 pp trên `exec`, và khả năng luật null thắng là thật.**

Ba căn cứ đo được:
1. **Phép ép chọn 3/9 đã cho thấy chiều ngược.** Bỏ hoàn toàn cơ chế bỏ cuộc kéo `sel_acc`
   57,54 → 69,05 (+11,51) nhưng độ đúng trên cả 1.400 bước **tụt** 63,43 → 49,71 (−13,71).
   τ là bản mềm của phép ép đó, nên lợi ích của nó bị chặn trên bởi chính hiện tượng này.
2. **872 bước bỏ-cuộc-sai có `action_ok` chỉ 71,22%.** Gần 29% trong số đó mô hình còn viết sai
   cả loại thao tác. Ép chúng chọn thì câu vẫn sai và `exec` không lên — τ không sửa được lỗi
   nằm ngoài tầng chọn.
3. **Con số +9,31 pp là trần lý thuyết**, ứng với việc vế bỏ-cuộc-sai biến mất hoàn toàn và
   nhóm đó đạt ngang nhóm HasAns-dám-chọn. τ chỉ dịch một ngưỡng, không dựng lại năng lực.

⇒ Nếu τ ra dưới ~1 pp hoặc luật null thắng, đó là **kết quả đã lường trước**, báo cáo bình
thường, và `(x16d)` buộc in cả đường cong. Nếu τ ra trên 3 pp thì đó là kết quả **vượt kỳ vọng**,
và phải soi kỹ hơn bình thường trước khi tin.

## 9. Quyết định 5/9: chạy SONG SONG hai lượt

Chủ luận văn quyết chạy đồng thời, không điều kiện hoá lượt này vào lượt kia.

| lượt | máy | việc | runbook |
|---|---|---|---|
| **τ** | Kaggle T4 | sequence-score lát dev 1.400 | `harness/kaggle_SEQSCORE_SAU_O.md` |
| **đối chứng** | Colab A100 | train `gui_sft_match`/101, ~23–30 h | `harness/colab_train_sel.md` (bỏ phần phạm vi sáu lượt) |

⭐ **Vì sao hai lượt độc lập, không phải nối tiếp:** `gui_sft_match` là đối chứng cho **hệ thống
chính** — mô hình sinh `<sel>` theo lối greedy, không có τ. `Δ_sel = exec(gui_sel) −
exec(gui_sft_match)`, cả hai vế đo trên hệ thống chính, τ không có mặt trong công thức. Để τ
quyết định có chạy đối chứng hay không sẽ biến Δ thành thứ chỉ báo khi có lợi, đúng dạng
chọn-sau-khi-thấy-số mà **(x16g)** cam kết không làm.

Ràng buộc thời gian: cổng giết của lượt đối chứng là **8/9 12:00 ICT** (chưa đạt ≈2.422/4.036
bước thì bỏ, không dùng điểm lưu dở). Quota Kaggle tuần này đã tiêu ~10 h trong 30 h.

---

## 10. Hai lỗi môi trường của lượt τ, đo ngày 4–5/9

**① `peft` 0.20.0 xung khắc `torchao` 0.10.0 của image Kaggle.** `pip -U peft` kéo về 0.20.0;
lớp dispatch LoRA gọi `is_torchao_available()`, và hàm đó **raise `ImportError`** khi thấy
torchao dưới 0.16 thay vì trả `False`. Chết ở `PeftModel.from_pretrained`, tức **sau khi** mô
hình nền đã tải xong. Cách xử: `pip uninstall -y torchao` ngay trong ô cài gói — script không
dùng torchao ở đâu, vắng mặt thì hàm kia trả `False` bình thường.
⚠️ Lệnh gỡ phải nằm **trong ô 1**; đặt ở ô sau thì commit chạy lại từ máy ảo sạch sẽ cài lại
peft rồi vấp y hệt.

**② Tràn bộ nhớ ở đường chậm của `seq_score_sel.py` — bảng logits, không phải trọng số.**
Đường chậm ghép cả câu nhắc vào từng span, nên một lô 8 span cho tensor logits
`[8 × ~1.520 × 151.936]`; riêng bản fp16 đã 3,7 GB và `.float()` nhân đôi ⇒ đòi **9,88 GB**,
tràn T4 16 GB. Đây đúng bài học đã ghi từ tháng 8: *chỗ ngốn bộ nhớ là bảng logits chứ không
phải trọng số* (P4 tràn nhưng P4+liger chạy được vì liger gộp cross-entropy).

**Cách sửa, giữ nguyên phép tính:** chỉ đổi kiểu số ở đúng `mx` vị trí cuối cần dùng
(`logits[:, L-mx-1:L-1, :]`) thay vì cả bảng, `mx` là span dài nhất trong lô. Với kích thước
thật, bảng đi từ ~1.520 vị trí xuống ~25, **giảm khoảng 60 lần**, còn dưới 200 MB.
✅ Đã kiểm chỉ số bằng tensor giả: công thức mới và công thức cũ cho **lệch 0,0 tuyệt đối**.
Kèm theo hạ `--span-batch` mặc định 8 → **4**.

⚠️ Bản vá nằm trong `seq_score_sel.py`, mà mã chạy trên Kaggle lấy từ **dataset**, nên phải
upload version mới (`_bundles/kaggle_sel_5_9.zip`). Ô workspace nay có thêm một `assert` bắt
đúng bản 5/9, để không lặng lẽ chạy bản cũ rồi tràn lần nữa.

**Truy nguyên của lượt probe:** bốn hash in ra trong manifest của script — `candidates.jsonl`,
`test.jsonl`, `ocr.jsonl`, `adapter_model.safetensors` — **khớp tuyệt đối** với bản trên máy.
`DynamicCache.crop` có mặt trên transformers 5.0.0 của Kaggle, nên `--cache-prompt` dùng được.

### 10b. Lỗi thứ ba, và nó ăn mất lượt probe thứ hai

**"New Version" của Kaggle THÊM thư mục, không thay thế.** Sau khi upload gói vá, trong
`/kaggle/input` tồn tại **song song** `kaggle_sel_4_9/` và `kaggle_sel_5_9/`. Ô chọn mã dùng dấu
vân tay `"fail-closed ĐẠT"`, mà chuỗi đó có trong **cả hai**, nên `ok` có hai phần tử và
`PKG = os.path.dirname(ok[0])` lấy phải **bản cũ**. Log in `✅ bản 4/9` hai lần liền nhau — dấu
hiệu duy nhất, và rất dễ đọc lướt qua. Không có lỗi, không có cảnh báo, chỉ là tràn bộ nhớ y hệt
lần trước với cùng con số 9,88 GiB.

⇒ Đây là **cùng một mẫu hình** với hai lỗi câm ngày 20/8: phép thử chưa hề diễn ra mà báo như đã
diễn ra. Và dấu hiệu nhận biết cũng giống hệt: **kết quả trùng khít giữa hai lần chạy lẽ ra phải
khác nhau**.

**Cách xử, đã áp:**
· Dấu vân tay chuyển sang chuỗi **chỉ có trong bản mới nhất**, và kiểm trên chính tệp vừa vá
  (`seq_score_sel.py`) chứ không phải tệp không đổi (`infer_branch.py`).
· Thêm `assert len(ok) == 1` — nhiều bản cùng đạt là **dừng hẳn**, không tự chọn.
· Thêm biến `GOI = os.path.dirname(PKG)` và mọi tệp phụ (`preds_..._dev1400.jsonl`) lấy theo
  `GOI` thay vì `glob` mù toàn `/kaggle/input`, để không ghép mã gói này với dữ liệu gói kia.

⚠️ **Luật rút ra, áp cho mọi lần vá mã về sau:** mỗi lần upload gói mới thì **đổi dấu vân tay**
sang chuỗi chỉ có trong bản đó. Dấu vân tay cũ không sai — nó chỉ hết khả năng phân biệt, mà
hết khả năng phân biệt thì im lặng chọn bừa.
