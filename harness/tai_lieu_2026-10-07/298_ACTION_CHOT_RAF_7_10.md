# 298 — ACTION: chốt RAF (7/10/2026)

> Chép từ 4 ảnh chụp màn hình Mac (`anh/`, gửi 7/10 dạng zip, zip đã xoá). Thứ tự ảnh theo chữ số
> cuối tên: `…1.jpg` (§1–2) · `…2.jpg` (§2 cuối–§4) · `…3.jpg` + `…4.jpg` (§5). Chỗ ảnh bị khuất
> hoặc nằm giữa hai ảnh ghi `[không đọc được]`. Script §5 đã chép ra
> **`_scripts/298/cham_raf_wsl_298.py`** (kiểm cú pháp đạt).

Mục tiêu: lấy **2 số chính thức còn thiếu** của RAF trên test (METEOR, BERTScore). Có hai số này thì
biết RAF đạt 7/13 hay 6/13 cột so với ck500. Các số khác đã có (§3).

## 1. Việc bạn làm (trên WSL)

**Bước 1.** Chép 2 file từ Mac sang gốc kho trên WSL:

| file trên Mac | để ở WSL |
|---|---|
| `thesis/_scripts/298/cham_raf_wsl_298.py` (nguyên văn ở §5) | `<gốc kho>/cham_raf_wsl_298.py` |
| `thesis/_scripts/296/lai_test/raw_G4g_test.jsonl` (câu RAF, 4.463 dòng) | `<gốc kho>/raw_G4g_test.jsonl` |

**Bước 2.** Chạy một trong hai lệnh:

```
cd <gốc kho>
# (A) KHÔNG cần Java – chỉ BERTScore (+ chrF):
~/.venvs/thesis/bin/python cham_raf_wsl_298.py --raf raw_G4g_test.jsonl --bo-meteor
# (B) Có Java 8 ở ~/.jdk – METEOR + BERTScore (+ chrF):
~/.venvs/thesis/bin/python cham_raf_wsl_298.py --raf raw_G4g_test.jsonl
```

- Script **không chạy SPICE**: SPICE của RAF đã có số chính xác.
- BERTScore dùng `roberta-large` qua `bert_score`, giống lần chấm 66,33 / 67,07 trước đây.
- Ước thời gian: BERTScore khoảng 15–30 phút trên CPU, vài phút nếu có GPU; METEOR khoảng 5 phút.
  Phần bootstrap chrF mất thêm vài phút.

**Bước 3.** Gửi lại cho chat 10 dòng cuối màn hình, hoặc file `cham_raf_wsl_298.json`.

**Đọc kết quả:**

| BERTScore Δ | METEOR Δ | kết luận |
|---|---|---|
| > 0 | > 0 | RAF hơn ck500 **7/13** cột ⇒ đạt "đa số" |
| một trong hai ≤ 0 | | RAF **6/13** ⇒ báo đúng 6/13, không sửa luật |
| chạy lệnh (A) | proxy +0,4…+0,7 | ghi METEOR là "xấp xỉ, không chính thức" |

Tự kiểm: dòng S1 và ck500 in ra phải khớp số công bố (S1 METEOR 36,79 · BERTScore 66,33 · chrF 61,26;
ck500 37,92 · 67,07 · 62,87). Không khớp thì dừng, đừng dùng số RAF.

> Script đã kiểm cú pháp, nhưng **chưa chạy thử trọn vẹn**: lần chạy thử chế độ chỉ-chrF trên Mac bị
> dừng giữa chừng. Nếu lỗi, gửi nguyên thông báo lỗi cho chat.

## 2. Có ai làm gần giống RAF không? — Có, phải trích

| bài | venue | giống RAF ở đâu | khác RAF ở đâu |
|---|---|---|---|
| Mao et al., m-RNN, §8 "consensus reranking" | ICLR 2015 | **Gần nhất.** Xếp hạng lại 10 câu do mô hình sinh theo CIDEr/BLEU đồng thuận với caption của 60 ảnh láng giềng trong train. COCO test: BLEU-4 27,9 → 29,9; CIDEr 81,9 → 91,7 | ứng viên là n-best của **một** mô hình; láng giềng theo ảnh; không có cổng |
| Mun, Cho, Han, Text-guided attention | AAAI 2017 | dùng lại đúng cách xếp hạng của Mao (CIDEr với caption 60 láng giềng) | như trên |
| Devlin et al., nearest-neighbor captioning | arXiv 2015 | chọn câu "đồng thuận" nhất bằng CIDEr-D | ứng viên là chính các caption truy hồi, không phải câu mô hình sinh |
| Deguchi & Nagata, CBDT decoding | EMNLP 2025 | chấm ứng viên bằng **câu chuẩn thật của ví dụ tương tự** trong bộ nhớ (thay mẫu tự sinh của MBR); dịch máy + caption COCO | n-best của một mô hình, có trọng số tương đồng; không cổng |
| Eriguchi et al., TM + NMT | WAT 2019 | **lùi theo truy hồi**: có câu nhớ đủ giống thì dùng câu nhớ, không thì dùng NMT | chọn giữa câu nhớ và câu máy, không phải giữa hai mô hình |
| RouteLLM (Ong et al.) · Smoothie (Guha et al.) | ICLR 2025 · NeurIPS 2024 | chọn mô hình **theo từng mẫu**; Smoothie không cần nhãn, có bản dùng láng giềng | RouteLLM phải train bộ định tuyến; Smoothie dùng đồng thuận giữa các đầu ra, không dùng câu người |
| SPIBB (Laroche et al.) · DeRa (Liu et al.) | ICML 2019 · ICML 2024 | ý "lùi về chính sách gốc khi thiếu bằng chứng" / trộn SFT ↔ RL | SPIBB là RL ngoại tuyến; DeRa trộn toàn cục bằng λ |

`[không đọc được: phần nằm giữa ảnh 1 và ảnh 2, có thể còn hàng bảng hoặc đoạn văn]`

**Câu nên viết trong luận văn:** RAF không phát minh phép chấm. Phép chấm là consensus reranking của
Mao et al. (2015). Phần của đề tài gồm ba điểm:

1. Áp phép chấm vào việc **chọn giữa chính sách SFT và chính sách RL**, kèm cổng bảo thủ: chỉ mở khi
   hai mô hình bất đồng mà cùng loại thao tác; hoà thì giữ RL.
2. Bộ nhớ là **quỹ đạo GUI căn theo bước** (mục tiêu + câu bước trước), không phải ảnh láng giềng.
3. Bằng chứng rằng cách xếp hạng n-best kiểu Mao **hỏng** trên bài này (−25 … −84 CIDEr-D trên val C1).
   Chỉ chọn giữa hai chính sách mới có lợi (+5,61 CIDEr-D trên test).

**Không được viết:**

- "RAF là phương pháp mới hoàn toàn";
- "RAF tổng quát hoá": 76–89% lợi nằm ở các tác vụ có mục tiêu gần trùng train;
- "chrF tăng có ý nghĩa".

## 3. Số RAF − ck500 đã có (test 4.463 click)

| cột | Δ [KTC95] | trạng thái |
|---|---|---|
| BLEU-4 | +0,72 [+0,31; +1,12] | ✅ |
| ROUGE-L | +0,68 [+0,38; +0,98] | ✅ |
| CIDEr-D | +5,61 [+1,46; +9,61] | ✅ |
| SPICE | +0,53 [+0,03; +0,99] | ✅ chính xác |
| chrF | +0,20 [−0,10; +0,51] | dương, không ý nghĩa |
| METEOR | proxy +0,4 … +0,7 | ⏳ §1 |
| BERTScore | dự báo ≈ +0,18 | ⏳ §1 |
| 5 cột hành vi | −0,13 … −0,38 | âm nhẹ, KTC phủ 0 |
| đúng loại thao tác | 0,00 | hoà |

Chi tiết và cách tính nằm trong `thesis/297_NGHIEN_CUU_RONG_VI_SAO_THUA_VA_DONG_GOP_NAO_7_10.md` (bản Mac).

## 4. Mục tài liệu tham khảo dán sẵn

Dán vào `thesis/chapters/99_tailieu.tex`, trước `\end{thebibliography}`. Các khoá này chưa có trong file.

```tex
\bibitem{mao2015mrnn} J. Mao, W. Xu, Y. Yang, J. Wang, Z. Huang, A. Yuille, ``Deep captioning with multimodal
recurrent neural networks (m-RNN),'' in \emph{Proc. International Conference on Learning Representations (ICLR)}, 2015.

\bibitem{mun2017} J. Mun, M. Cho, B. Han, ``Text-guided attention model for image captioning,'' in \emph{Proc. AAAI
Conference on Artificial Intelligence}, 2017.

\bibitem{devlin2015} J. Devlin, S. Gupta, R. Girshick, M. Mitchell, C. L. Zitnick, ``Exploring nearest neighbor
approaches for image captioning,'' arXiv preprint arXiv:1505.04467, 2015.

\bibitem{deguchi2025cbdt} H. Deguchi, M. Nagata, ``Case-based decision-theoretic decoding with quality memories,'' in
\emph{Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP)}, 2025.

\bibitem{eriguchi2019tm} A. Eriguchi, S. Rarrick, H. Matsushita, ``Combining translation memory with neural machine
translation,'' in \emph{Proc. Workshop on Asian Translation (WAT)}, 2019.

\bibitem{routellm} I. Ong, A. Almahairi, V. Wu, W.-L. Chiang, T. Wu, J. E. Gonzalez, M. W. Kadous, I. Stoica,
``RouteLLM: Learning to route LLMs from preference data,'' in \emph{Proc. International Conference on Learning
Representations (ICLR)}, 2025.

\bibitem{smoothie} N. Guha, M. F. Chen, T. Chow, I. S. Khare, C. R\'e, ``Smoothie: Label free language model
routing,'' in \emph{Advances in Neural Information Processing Systems (NeurIPS)}, 2024.
```

`[không đọc được: các mục SPIBB · DeRa và dòng "Đã kiểm trên trang gốc …" ở chân ảnh 2 bị cắt]`

## 5. Script `cham_raf_wsl_298.py` (nguyên văn)

Đã chép ra `_scripts/298/cham_raf_wsl_298.py`. Script phải chạy từ **gốc kho** (đường dẫn mặc định
`runs/…` và `sys.path.insert(0, "harness")` đều tương đối), nên lệnh trên WSL là:

```
cd /mnt/d/Master/Thesis
~/.venvs/thesis/bin/python _scripts/298/cham_raf_wsl_298.py --raf <đường dẫn raw_G4g_test.jsonl>
```

Không có lệnh git nào được chạy, không commit. File này nằm ngoài `thesis-master/`.

---

## Phụ: dựng `raw_G4g_test.jsonl` trên WSL (script 296-R, ảnh `anh_2/`, nhận 7/10 17:42)

`raw_G4g_test.jsonl` không có trên WSL; user gửi thêm 2 ảnh của `_scripts/296/do_296_R_test_lai.py`
(script dựng tệp đó). Đã chép ra **`_scripts/296/do_296_R_test_lai.py`**, chạy CPU ~1 phút, ra
`_scripts/296/lai_test/raw_G4g_test.jsonl` + `cong_G4g_test.json`.

Khác bản Mac hai chỗ (ghi ở đầu script):
- Bản Mac `exec` phần đầu `_scripts/296/do_296_vallon.py` để lấy `tok` + `CiderD`; tệp đó không có
  trên WSL ⇒ lấy từ `harness/ctg_grpo.py` (CIDEr-D chép nguyên văn Phụ lục A của 276).
  ⚠️ `CiderD.score` của `ctg_grpo` nhận **danh sách** tham chiếu, bản Mac gọi với **một câu** ⇒ phải bọc
  lớp con. Chưa bọc thì chuỗi bị duyệt từng ký tự, 1.299/1.351 cặp ra hoà và chỉ 19 bước lùi.
- Đường dẫn `thesis-master/…` đổi thành tương đối từ gốc kho.

**Kiểm tái lập:** cổng lùi về S1 ở **724/4.463** bước, trùng `assert … <= 724` của script 298.
Tầng lọc: 1.445 bước câu khác token → 1.351 cùng lớp thao tác → 724 lùi.
Ba cột §3 tính lại bằng pycocoevalcap (mức kho): BLEU-4 **+0,69** (Mac +0,72) · ROUGE-L **+0,68**
(trùng) · CIDEr-D **+5,54** (Mac +5,61). Lệch nhỏ chưa truy được: cần `cong_G4g_test.json` của Mac để so
từng bước.

## KẾT QUẢ §1 — chạy WSL 7/10 (lệnh B, có Java), `runs/raf298/`

Tự kiểm ĐẠT: S1 36,79 · 66,33 · 61,26 và ck500 37,92 · 67,07 · 62,87 trùng tuyệt đối số công bố.

| cột | RAF | ck500 | Δ số tổng | KTC95 (bootstrap theo tác vụ) |
|---|---|---|---|---|
| METEOR 1.5 | 38,09 | 37,92 | **+0,17** | [+0,28; +1,03] ⚠️ KTC của trung bình câu, KHÔNG của số tổng |
| BERTScore (rescaled) | 67,62 | 67,07 | **+0,55** | [+0,29; +0,82] |
| chrF | 63,08 | 62,87 | +0,20 | [−0,10; +0,51] |

⇒ Theo bảng đọc §1: METEOR Δ > 0 và BERTScore Δ > 0 ⇒ **RAF hơn ck500 7/13 cột**.
⚠️ METEOR: số tổng của pycocoevalcap do Java gộp từ thống kê khớp toàn kho, không phải trung bình
điểm từng câu, nên KTC script in ra (dựng trên trung bình câu) không chứa Δ số tổng. Chỉ được viết
"METEOR tổng +0,17"; không gắn KTC đó vào số +0,17. Muốn KTC đúng phải bootstrap gọi lại Java.
BERTScore là trung bình câu ⇒ KTC dùng được, loại 0 (dự báo trước là ≈ +0,18).
