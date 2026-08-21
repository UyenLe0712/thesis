# CLAUDE.md — Bối cảnh luận văn (auto-load mỗi phiên)

> 🗂️ **Bản đồ thư mục = `README.md` ở gốc kho** (tái cấu trúc 16/8/2026).
> Đổi chỗ: `ppt_build/` → `slides/build/` · `ckpt/` → `runs/gate_a/` · `report/_papers/` →
> `report/paper_figures/` · `LUAN_VAN_SLIDE.pptx` → `slides/` · gói zip → `_bundles/`.
> **`harness/` và `report/` giữ nguyên tên** (597 và 1991 tham chiếu; layout gói zip mà
> runbook Colab phụ thuộc cũng dùng tên `harness`). Luận văn LaTeX ở `thesis/`.

> ## ▶️ 18/8/2026 — S2 HẠT GIỐNG 101 ĐANG TRAIN. ĐỪNG KHỞI ĐỘNG LƯỢT KHÁC.
> Runbook dán thẳng: **`harness/S2_DAN_THANG.md`** (10 ô, tự đủ, đã kiểm cú pháp 20/20 khối).
> Bối cảnh và lý do: `harness/colab_train_s2.md`.
>
> **Trạng thái lúc ghi:** bước **2.260/8.072 = 28%** · loss 0,389 · **10,22 s/bước** · A100 ·
> `output_dir = MyDrive/thesis/ckpt/s2_seed101` · dự kiến xong **~13:00 ngày 19/8**.
> Xong 101 thì đổi `SEED = 202` ở ô 5, chạy lại từ ô 5. **Chấm để cuối**, sau khi có cả hai.
>
> **✅ ĐÃ THỰC HIỆN ĐIỀU KIỆN BẮT BUỘC CỦA MỤC SỬA ĐỔI (q).** Mục (q) ngày 14/8 đổi nhãn khai
> báo sang tiếng Anh và ghi *"việc bắt buộc trước khi train s2: dựng lại descriptors và bốn tệp
> nhánh ở quy mô đủ"*. Dữ liệu trên Drive vẫn là bản **tiếng Việt** (`chữ bấm được | … | bên
> phải chữ …`) — phát hiện lúc đọc `labels` của lượt thăm dò, **trước khi train**. Đã dựng lại
> 18/8 và kiểm ba phép: **0 tiếng Việt ở khuôn mẫu** (dấu riêng tiếng Việt, không tính `é/à`
> dùng chung — 1 ca `Save Tôrres to lists` là chữ thật trên màn, hợp lệ) · **9/9 bất biến ĐẠT** ·
> **s2r ghép độ dài token 99,9%** trong 2 token (mốc cũ 99,3%). Cất ở
> `MyDrive/thesis/derived_train_en.tar.gz`; bản tiếng Việt sao lưu ở `branches_vi_0818/`.
> ⚠️ **Phiên đứt thì sau ô 2 PHẢI bung `derived_train_en.tar.gz` đè lên** — ô 2 bung
> `derived.tar.gz` là bản CŨ tiếng Việt, quên bước này là train tiếp trên dữ liệu khác mà log
> không báo gì.
>
> **✅ Thăm dò bộ nhớ trên nhánh nặng nhất ĐẠT** — P9 chạy 20 bước trên 200 mẫu dài nhất của s2,
> `train_runtime` 219,9 s, loss 2,28, không tràn. `total_flos` bản tiếng Anh **10.812.978** vs
> bản tiếng Việt **10.816.688**, lệch **0,03%** ⇒ đổi ngôn ngữ **không đổi độ dài chuỗi**, xác
> nhận mục (q) đúng là thay đổi thuần từ vựng — bằng một con số độc lập.
> · `s2_long.json` **không có trong gói Drive lẫn `branches_backup/`** — ô 5b dựng lại tại chỗ.
> · ⛔ **Ô thăm dò PHẢI `shutil.rmtree("/content/probe_s2long")` trước.** Không xoá thì
> LLaMA-Factory tự chạy tiếp từ checkpoint cũ, **nhảy qua** 20 bước rồi chạy đúng một bước: log
> vẫn in `Training completed`, vẫn có `total_flos`, trông y như đạt. Đọc bằng **hai con số**:
> `train_runtime` ~220 s (không phải ~15) và loss ~2,4 (không phải ~0,1). Đã mắc thật.
>
> **📋 Ô 7b tiền bay (mới) — bảy phép kiểm 10 giây trước khi bấm train:** cfg đúng nhánh · không
> sót `max_steps` · `output_dir` rỗng · 64.567 mẫu · 0 tiếng Việt · **đường dẫn ảnh mở được**
> (sai prefix thì chết SAU 42 phút mã hoá token) · đĩa ≥20 GB · ~8.072 bước.
> ⚠️ Ô 7b in **8.071** do làm tròn; trainer chạy **8.072** (`ceil(64.567/16)=4.036` ×2).
>
> **🔧 `trainer_log.jsonl` — tên trường thật:** `current_steps` · `total_steps` · `loss` ·
> **`lr`** (KHÔNG phải `learning_rate`) · `epoch` · `percentage` · `elapsed_time` ·
> `remaining_time`. **Không có `grad_norm`** — trường đó chỉ ở dòng stdout.
> ⚠️ `elapsed_time`/`remaining_time` **hỏng sau khi chạy tiếp**; ô theo dõi tự tính bằng mốc neo.
> ✅ Đã kiểm `lr` chạy đúng lịch: ở bước 2.260, cosine tính ra 8,622e-05, trainer ghi 8,624e-05
> — **lệch 0,02%**.
>
> **⚠️ "Connecting" / "Not connected to runtime" trên trình duyệt KHÔNG phải máy chết.** Ngày
> 18/8 tưởng đứt và suýt dựng lại; `elapsed_time` 6:24:50 cho 2.260 bước = 10,22 s/bước, khớp
> **liền mạch từ bước 0 trong 0,2%** ⇒ chưa hề đứt. Bằng chứng thật: PID còn sống, hoặc thư mục
> điểm lưu trên Drive có bản mới trong vòng **~34 phút** (200 bước × 10,2 s).
> **Theo dõi không cần nhân Python** — Terminal Colab, hoặc mở Google Drive từ điện thoại.
>
> **🗂️ Mã và runbook mới trong ngày:** `S2_DAN_THANG.md` · `colab_train_s2.md` ·
> `colab_cham_san.md` · `kaggle_cham_san.md` · `kaggle_upload_dataset.md` · `make_floor.py` ·
> `doc_san.py` · `kiem_preds.py` (8 phép kiểm tệp preds trước khi tiêu quota) · `doc_diem_tam.py` ·
> `phan_tich_bon_nhanh.py` · `bien_the_khong_tham_chieu.py` · `mde_that.py` ·
> `phep_a_hieu_chinh.py` · `phep_a_ghep_cap.py`.
> **Dataset Kaggle dựng lại:** `thesis-score` (gói `make_bundle.py score`, 1,69 GB, 4.463 ảnh) và
> `thesis-preds` (`_bundles/preds_upload.zip`, 805 KB).

> ## ✅ 18/8/2026 — ĐÃ TRA TIỀN LỆ. NHAN ĐỀ GIỮ ĐƯỢC, NHƯNG PHẢI PHÂN ĐỊNH.
> Toàn văn + nguyên văn trích: **`report/114`**.
>
> **① ⚠️ Chữ "executability" ĐÃ CÓ CHỦ, có định nghĩa hình thức.** *Open Grounded Planning*,
> **ACL 2024, tr. 4982–5003** (arXiv 2406.02903), mục 3.3.2: *"Executability is the proportion
> of executable cases. Executable cases are actions in the plan that all exist within the given
> action library."*
> **Nhưng khác hẳn ta:** của họ là **tra bảng ký hiệu** trên văn bản — không mô hình, không màn
> hình, miền WikiHow/công cụ/robot, tự khai *"only focuses on the planning generation"*. Của ta
> là **hành vi + thị giác**.
> ⇒ **QUYẾT: GIỮ TÊN.** Đã vá một câu phân định vào Introduction của `main.tex` ngay lần dùng
> đầu. Đổi tên phải sửa nhan đề + abstract + toàn bộ report + luận văn, đắt mà không rõ tốt hơn.
>
> **② ✅ Zhao et al. EACL 2021 (tr. 1302–1316) — vừa hậu thuẫn vừa cảnh báo, đã trích vào bài.**
> · *"BLEU, ROUGE, METEOR and CIDEr are **ineffective** for evaluating grounded navigation
> instructions"* ⇒ hậu thuẫn việc hạ luận cứ đồng thuận BLEU/ROUGE.
> · ⚠️ Họ đề xuất thước **không tham chiếu**, nó thắng ở **mức CÂU**, nhưng để xếp hạng **HỆ
> THỐNG** thì chính họ khuyên dùng SPICE — một thước **có** tham chiếu. **Toàn bộ Mục VII của
> bài ta là khẳng định mức hệ thống.** Đã trích vào *Scope of the construct*.
> · Họ **có** neo người (human wayfinders). Ta không.
>
> **③ ✅ GUITrans2Act (2606.12817) KHÔNG phải scoop** — preprint 6/2026 **không venue**, đầu vào
> là **video**, abstract không nhắc mô hình định vị. Khẳng định của agent về "vòng lặp nhất
> quán-với-bộ-trỏ" **không kiểm được từ abstract**.
>
> **④ ⛔ GCoT: AGENT SAI, GHI CHÚ CỦA TA ĐÚNG.** 2503.12799 **vẫn là preprint không venue**;
> bài ICCV 2025 là bài KHÁC (2507.02859) — đúng như `CLAUDE.md` ghi từ 1/8. Giữ nguyên, đừng sửa.
> ⭐ Lần này **ghi chú của mình thắng agent** ⇒ agent cũng phải kiểm như mọi nguồn khác: không
> tin ngay, cũng không bỏ ngay.

> ## ⛔ 18/8 — BÀI FAIR ĐANG **10 TRANG**, GIỚI HẠN 8. VÀ TRỢ LÝ KHÔNG BIẾT SUỐT CẢ NGÀY.
> Lệnh dựng đúng ghi sẵn ở `paper/fair2026/README.md:76` và `thesis/build.sh`:
> **`tectonic -X compile main.tex --outdir .`**. Trợ lý tự chế `xelatex … >/dev/null 2>&1`;
> máy **không có `xelatex`**, `command not found` bị nuốt, nên mọi lần báo *"8 trang, 0
> overfull"* đều là đọc **PDF cũ ngày 16/8**. Lặp hơn mười lần trong một ngày.
> ⇒ **Luật từ nay: KHÔNG `>/dev/null 2>&1` trên lệnh dựng; và kiểm `ls -la main.pdf` xem mốc
> giờ trước khi tin số trang.** Ghi vào `report/108` mục 8.
>
> **Số thật sau khi dựng bằng tectonic:** bài **10 trang** · luận văn **77 trang** (từ 73, và
> cả sáu mốc nội dung mới đều vào đủ; +1 trang ngày 18/8 tối khi vá `total_flos`). Phần thêm hôm nay (độ tin cậy · sàn · gọi-tên-vs-chỉ-chỗ
> · vá Jandial · khai phụ thuộc câu chuẩn) cộng đúng ~2 trang.
> **⇒ PHẢI CẮT 2 TRANG trước khi nộp.** Ứng viên cắt, theo thứ tự giá trị thấp dần: mục **bơm
> lỗi** (bài tự khai 5/10 hàng là hằng đẳng thức và **0/10 hàng gọi tới bộ trỏ**) · mục **so với
> thước có tham chiếu** (luận cứ đồng thuận BLEU/ROUGE đã tự hạ hôm nay) · chi tiết đường ống
> dữ liệu. **Đừng cắt phần mới** — đó đúng là thứ bốn giám khảo nói đang thiếu.
>
> **⛔ 18/8 tối — VÁ NỐT MỘT SỐ ĐÃ RÚT CÒN SỐNG TRONG LUẬN VĂN.** `ch6_thucnghiem.tex` vẫn ghi
> `total_flos` = **3.857.778.344 GF** kèm lập luận *"khớp ngoại suy 0,32%"* — số sai, và lập
> luận **vòng tròn** (so một con số với chính phép ngoại suy đẻ ra nó). Đã thay bằng
> **4.142.257.957 GF** (513.164 GF/bước) + bằng chứng không vòng tròn: hai lượt đứt **6** vs
> **3** lần mà GF/bước khớp **0,013%**. ⇒ **Quét toàn kho sau mỗi lần rút số** — số đã rút ở
> `CLAUDE.md`/`report/108` vẫn có thể còn sống trong `.tex`.
>
> **📘 LUẬN VĂN ĐÃ CẬP NHẬT (77 trang):** `thesis/chapters/ch5_thuocdo.tex` thêm mục **Sàn của
> thước đo** (ba nhánh đối chứng · bảng sàn/trần · mục con *Thước đo gọi tên, không đo chỉ chỗ*
> với cặp −28,5 vs −3,5) · `ch6_thucnghiem.tex` thêm mục **Lặp lại lượt huấn luyện** (bảng hai
> hạt giống · κ có điều kiện 0,650 · tất định 2.810/2.810 · sáu lát cắt đều tái lập).

> ## ⭐⭐⭐ 18/8/2026 — ĐÃ ĐO SÀN. BA LỖ LỚN NHẤT CỦA BÀI ĐÃ LẤP, CẢ BA THUẬN.
> Chi tiết: **`report/113` mục I** · đọc bằng `python3 harness/doc_san.py` · luật đọc khoá
> trước ở `harness/make_floor.py`. Lát 800 bước, trần trên lát này 74,9%. Kaggle, 3 giờ, 0 đồng.
>
> | nhánh | câu thành gì | điểm | KTC95 |
> |---|---|---|---|
> | **`f1_trong`** | `"Tap the button."` mọi bước | **12,0%** | [9,7 – 14,4] |
> | **`f3_lechman`** | câu **thật** của bước khác — đúng văn phong, **sai màn** | **6,1%** | [4,5 – 7,9] |
> | **`f2_khongten`** | giữ vị trí, **bỏ tên** | 68,0% toàn lát · **61,1%** phần bị đụng | — |
>
> **① SÀN 12,0% ⇒ dải dùng được 62,9 điểm** (không phải 74,9, cũng không phải 35,7 như kịch bản
> xấu). Vị trí trong dải: Base **58,3%** · S1 **74,4%**. Câu *"the metric does not collapse
> towards its floor"* nay **có phép đo chống lưng**.
> ⛔ **Dự đoán "sàn ≈40%" của phản biện BỊ BÁC.** Nó suy từ việc 40,4% số bước cả ba nhánh cùng
> trúng. Sàn thật 12,0% ⇒ những bước ấy **dễ KHI CÓ CÂU THẬT**, không dễ vô điều kiện.
> **Suy sàn từ tỉ lệ đồng thuận là suy sai.**
>
> **② ⭐ `f3` (6,1%) THẤP HƠN `f1` (12,0%), hai KTC KHÔNG chồng lấn — ĐÒN NHIỄM VĂN PHONG BỊ
> GIẾT BẰNG SỐ.** Giả thuyết nhiễm nói bộ trỏ thưởng cho câu **đúng văn phong bất kể nội dung**.
> `f3` có văn phong hoàn hảo, độ dài khớp (34 vs 35 ký tự), **nội dung sai** ⇒ theo giả thuyết
> đó nó phải ăn CAO. Nó ăn **thấp nhất trong mọi thứ đã đo**, dưới cả câu vô nghĩa.
> ⇒ bộ trỏ **thật sự đọc câu**: câu sai dẫn nó đi lạc, câu rỗng để nó rơi về tiên nghiệm thị
> giác yếu. Cộng phép "cùng nội dung khác văn phong" (+0,9…+1,9 pp, không ý nghĩa), giả thuyết
> văn phong nay bị đánh từ **hai hướng độc lập**.
>
> **③ ⭐ GỌI TÊN ĐẮT GẤP 8 LẦN CHỈ CHỖ — nhan đề có số bảo vệ.**
> · bỏ **TÊN**, giữ vị trí: **−28,5 pp** (193 bước, b=58 c=3, χ²=47,8, **p<0,001**)
> · bỏ **VỊ TRÍ**, giữ tên: −3,5 pp (198 bước, b=8 c=1, p=0,046)
> Hai quần thể gần bằng nhau (193 vs 198) nên so trực tiếp được. ⇒ chữ **"Element
> Identification"** ở nhan đề **ĐÚNG**. Ngưỡng khoá trước: *tụt ≥10 pp ⇒ n=193 thừa sức*.
> ⚠️ **Con số của bài là −28,5 pp trên PHẦN BỊ ĐỤNG**, không phải −6,9 pp toàn lát — `f2` chỉ
> đụng 24,1% số bước, pha loãng **4,15 lần**. Cùng bẫy đã mắc ở phép A.
>
> **Đã vá vào bài (vẫn 8 trang, 0 overfull, bản nộp đã làm mới):** abstract thêm 12,0 · 6,1 ·
> cặp 28,5-vs-3,5 · §VII thay đoạn *"floor we have not measured"* bằng phép đo · §VIII thêm
> đoạn gọi-tên-vs-chỉ-chỗ.
>
> **⇒ Trong ba lỗ ghi ở `report/112` §11.3, hai đã đóng (sàn · gọi-tên-hay-chỉ-chỗ).** Còn lại:
> **chưa thay dụng cụ lần nào** (bộ trỏ thứ hai) và **không có neo ngoài nào**.

> ## 🔎 18/8/2026 — BỐN LƯỢT PHẢN BIỆN ĐỘC LẬP. PHÁN QUYẾT: HỢP LỆ, NHƯNG PHẢI HẸP HƠN NHAN ĐỀ
> Toàn văn: **`report/112` §11** · tiền lệ chưa tra: `report/114` · số vắt từ tệp thô:
> `report/113`. Mã mới: `harness/phan_tich_bon_nhanh.py` · `bien_the_khong_tham_chieu.py` ·
> `mde_that.py` · `kiem_preds.py` · `doc_diem_tam.py` · `make_floor.py`.
>
> **⭐ MẪU HÌNH QUAN TRỌNG NHẤT: bảy lỗi bắt được trong hai ngày, KHÔNG lỗi nào ở khâu ĐO.**
> Tất cả nằm ở **câu chữ mô tả**: 84% của Jandial · "bộ trỏ khác họ/sạch AC" · "reference-free"
> ở nhan đề · `hit_disk` là "đĩa" · hạt Voronoi là "tâm phần tử" · κ trình thiếu điều kiện ·
> đếm 14 mục sửa đổi. Trong khi phần **đo** giữ nguyên qua mọi lượt soi: `metric_exec.py` một
> commit từ 5/8 · tệp thô tái lập tới chữ số cuối · hai hạt giống cho +11,5 và +12,0 · sáu lát
> cắt lặp lại cả sáu · thước tất định 1.625 phép so 0 bất đồng.
> ⇒ **Chỗ phải soi tiếp là VĂN BẢN, không phải mã.** Và cụ thể: mọi lỗi đều sinh ra ở khâu
> **tóm tắt một nguồn thành câu ngắn cho tiện trích**, rồi câu ngắn sống nhiều tuần vì không
> ai mở lại nguồn.
>
> **✅ ĐỨNG VỮNG (không lượt nào lật được):** SFT hơn mô hình gốc **+11,52 / +12,03 pp** hai hạt
> giống độc lập · nhiễu hạt giống **0,52 pp** ⇒ tín hiệu gấp **22×** · **cùng nội dung khác văn
> phong: +0,9…+1,9 pp KHÔNG ý nghĩa** (đòn "thắng nhờ văn phong" mất cơ chế chính) · 5 luật
> chấm không đổi thứ tự · thước tất định · 1.139 câu viết lại **+0,35 pp** · **thước KHÔNG xếp
> văn máy trên văn người** (lá chắn tốt nhất, trước nay chưa dùng, đã đưa vào §VII) · không lợi
> thế sân nhà (+14,1/+14,1) · đăng ký trước kiểm được bằng `git log`.
>
> **⛔ CHƯA ĐỨNG — không sửa bằng câu chữ được:**
> · **(a) KHÔNG BIẾT SÀN.** **40,0%** số bước cả ba nhánh cùng trúng, **kể cả mô hình chưa
> huấn luyện** ⇒ dấu hiệu sàn CAO. Nếu sàn ≈40% thì dải dùng được là **35,7 điểm** chứ không
> phải 75,7, và mọi câu *"lấp 41% dư địa"* phải tính lại. Câu *"does not collapse towards its
> floor"* hiện **không có phép đo chống lưng**.
> · **(b) KHÔNG BIẾT thước đo GỌI TÊN hay CHỈ CHỖ.** Bỏ *vị trí* mất 3,5 pp; bỏ *tên* mất bao
> nhiêu thì chưa đo. Nếu xấp xỉ nhau ⇒ **"Element Identification" ở nhan đề SAI**.
> · **(c) Chưa thay dụng cụ lần nào** — bộ trỏ chính là thước, mà nó nhiễm AC + cùng họ Qwen.
> · **(d) Không có neo ngoài nào** (đã quyết không chấm người).
> · **(e) ⚠️ Chữ "executability" có thể ĐÃ CÓ CHỦ** (Open Grounded Planning, ACL 2024) —
> **chưa tra**, và nó đụng nhan đề. `report/114`.
>
> **▶️ VIỆC ĐÁNG NHẤT CÒN LẠI — hai lượt chấm ~1 giờ, tệp ĐÃ DỰNG SẴN, luật đọc ĐÃ KHOÁ TRƯỚC**
> trong `harness/make_floor.py`: `runs/floor/preds_f1_trong.jsonl` (sàn) và
> `preds_f2_khongten.jsonl` (gọi tên hay chỉ chỗ).
> 💡 **Sàn không chỉ là một con số — nó là mảnh ghép TÁCH HAI ĐÓNG GÓP.** Hiện `S1 − Base` gánh
> hai vai: vừa là kết quả mô hình, vừa là bằng chứng thước phân giải được. Cặp *"câu người vs
> câu vô nội dung"* có thứ tự biết trước mà **không dính mô hình nào của ta** ⇒ chứng minh khả
> năng phân giải **độc lập**, giải phóng `S1 − Base` để chỉ còn là kết quả.
>
> **Đã vá vào bài (vẫn 8 trang, 0 overfull):** bản không-tham-chiếu (lấy loại thao tác từ
> `action.action_type`, lệch ≤0,20 pp) · κ có điều kiện **0,650** trên 1.652 bước viết khác
> nhau, cạnh 0,867 toàn tập · sai số bộ trỏ **theo từng nhánh 0,67 / 2,00 / 7,82** ⇒ cổng A chỉ
> chứng nhận cho nhánh trần · điều kiện đảo nghĩa **gần như trơ** (3/4/13 trên 4.462) · đếm mục
> sửa đổi **27, 21 trước điểm đầu tiên** · lát cắt ngoài ba lát đăng ký **gắn nhãn thăm dò** ·
> hạ luận cứ đồng thuận BLEU/ROUGE · tách **mức câu vs mức hệ thống** · tự khai mẫu hình hai
> lần nới ngưỡng sau khi thấy điểm, kèm phản chứng (lần đo lại trần **cắt** "S1 đạt 84,4% của
> trần" xuống 78,4%).

> ## ⛔⛔ 18/8/2026 — CON SỐ "BỘ TRỎ TRƯỢT 84% KHI ĐỔI DIỄN ĐẠT" ĐÃ BỊ RÚT
> **Tra tận nguồn** (aclanthology.org/2026.findings-eacl.144, đọc abstract nguyên văn):
> *"Our agent reports high success rate (**upto 84%**) in **generating instructions that
> fail** the state-of-the-art GUI grounding models."*
>
> ⇒ 84% là **tỉ lệ thành công của một AGENT ĐỐI KHÁNG chuyên đi chế câu phá mô hình**, trên
> **desktop Windows**. Nó **KHÔNG** phải tỉ lệ trượt khi diễn đạt lại, và **KHÔNG** phải trên
> di động — chính bài đó nói benchmark đang lệch về web/mobile và họ vá chỗ desktop.
>
> **Sai từ 29/7, sống 20 ngày, đã vào bản thảo bài báo.** Trớ trêu: ghi chú của chính ta ở
> `report/papers/do_gui_grounders_eacl2026.md` viết đúng từ đầu (*"một agent chẩn đoán có thể
> khiến chúng sai tới 84% bằng các chỉ dẫn hợp lệ nhưng lạ"*) — **cái sai nằm ở khâu tóm tắt
> lại ghi chú, không ở khâu đọc bài.**
>
> **Cách viết đúng, đã vá vào `main.tex` hai chỗ:** trích họ cho luận điểm *"độ chính xác đo
> trên MỘT câu tốt nhất cho mỗi phần tử là thổi phồng năng lực thật"* — đó mới là đóng góp của
> họ và nó vẫn hậu thuẫn ta. Nêu 84% kèm đúng điều kiện: **năng suất của tìm kiếm đối kháng
> trên màn hình desktop**, và **trường hợp di động họ để ngỏ chính là của ta**.
>
> ⇒ Phép diễn đạt lại của ta (**+0,35 pp trên 1.139 bước viết lại**) không còn phải chống một
> tuyên bố sụp đổ 84%; nó **đo cái chưa ai đo** ở miền di động, không đối kháng.
>
> **Bài học, cùng lớp với hai khẳng định UGround:** cái sai không sinh ra lúc đọc bài gốc mà
> lúc **tóm tắt ghi chú thành một câu ngắn cho tiện trích**. Câu ngắn đó rồi được trích lại
> hàng chục lần mà không ai mở lại ghi chú, nói gì tới bài gốc.

> ## ⭐⭐ 17/8/2026 — PHÉP DIỄN ĐẠT LẠI ĐÃ CÓ SỐ: CÁCH NÓI KHÔNG ĐỔI GÌ, LƯỢNG TIN THÌ CÓ
> Chi tiết đầy đủ: **`paper/fair2026/PHEP_A_DIEN_DAT_LAI.md`** · cơ chế và bối cảnh:
> `report/112` §6.7 · đọc số bằng `python3 harness/phep_a_ghep_cap.py` (**đừng** đọc
> `score_para_*.json` trần — con số tổng **bị pha loãng 3,8 lần**).
>
> Đòn Jandial et al. (Findings EACL 2026) ⛔ **CON SỐ 84% ĐÃ BỊ RÚT 18/8, xem khối dưới** là đạn
> bắn thẳng vào thước. Bản thảo cũ **tự khai không trả lời được**. Nay có số: lấy **câu chuẩn
> của người** (trần 74,9% trên lát 800), viết lại giữ nguyên nghĩa **và giữ nguyên tên phần
> tử**, chấm lại bằng UGround trên Kaggle (0 đồng).
>
> | biến thể | đổi gì | phần bị đụng | executability | McNemar |
> |---|---|---|---|---|
> | `p1_verb` | động từ thao tác | 725 bước (90,6%) | 76,8 → **77,0** (+0,1) | b=13 c=14, p=1,000 |
> | `p2_order` | trật tự câu | 211 bước (26,4%) | 89,6 → **90,0** (+0,5) | b=0 c=1, p=1,000 |
> | `p4_both` | `p1`+`p2` **cùng lúc** | 203 bước (25,4%) | 90,1 → **91,1** (+1,0) | **b=0** c=2, p=0,480 |
> | `p3_nopos` | **bỏ** mệnh đề vị trí | 198 bước (24,8%) | 89,4 → **85,9** (−3,5) | b=8 c=1, **p=0,046** |
>
> **⭐ CON SỐ GỘP — đây là con số đi vào bài.** Ba biến thể **bảo toàn nghĩa** (`p1`·`p2`·`p4`):
> **1.139 bước viết lại · 30 bước đổi chiều = 2,6%** (13 xuống · 17 lên) · hiệu ròng
> **+0,35 pp**, KTC95 **[−0,59 · +1,29]** ⇒ mép dưới loại được mọi mức tụt > **0,6 pp**.
> Quy mô 84% mà họ báo cần **~956** bước đổi chiều; thực đo **30**.
> · ⭐ **`p4_both` mạnh nhất trong bốn:** ghép hai phép viết lại là chỗ hiệu ứng cộng dồn thường
> lộ ra, ở đây **0 bước trúng→trượt trên 203**. Cả hai bước đổi chiều đều theo chiều TỐT LÊN.
>
> · **Cơ chế: hỏng tất-cả-hoặc-không.** Bỏ mệnh đề vị trí **không** làm trung vị sai số nhích
> (0,24% → 0,24%) mà làm đuôi bung: p90 **6,88 → 31,16**, p95 **27,54 → 62,38**. 11 bước
> trúng→trượt nhảy từ 0,1–0,6% lên **26–190%**, tức sang phần khác của màn. Khớp *sai số lưỡng
> cực* đã đo 15/8.
> · ⚠️ **Phần bị đụng là phần DỄ NHẤT** — trần ở đó 89,6% vs 74,9% toàn lát, sai số trỏ trung
> vị 0,24% vs 0,69%. Bỏ vị trí ở câu khó có thể đắt hơn, **chưa đo**.
> · ⚠️ **CÂU CHỮ:** viết *"bộ trỏ bền trước việc đổi động từ và đổi trật tự câu"*. **CẤM** viết
> *"bền trước diễn đạt lại"* — Jandial et al. đổi *cách mô tả phần tử*, nặng hơn hẳn; bằng
> chứng là `action_ok` giữ **100%** ở cả ba biến thể ⇒ phép viết lại này không đụng phần bộ trỏ
> phải giải. Và **CẤM** dùng hàng *"paraphrase 0,0%"* của bảng bơm lỗi để phản bác họ — bộ bơm
> lỗi **không gọi bộ trỏ lần nào**.
> · ⛔ **LỖI BỘ DỰNG CÂU, đóng góp 28% hiệu ứng thô, đã vá.** 7/211 câu `p3_nopos` không bỏ
> mệnh đề vị trí mà **xoá luôn tên phần tử**, trơ lại `Tap.` Vì *left/right/center* cũng nằm
> **trong tên** (`the left arrow icon`, `the Right Tick icon`) nên `re.search` khớp-trái-nhất
> bắt đầu ngay ở *"on the left…"* và ngốn cả tên. Vá bằng **hai cổng chặn** (không siết regex —
> siết thì giết ca lành có mệnh đề vị trí giữa câu): cổng A chặn câu trơ động từ, cổng B chặn
> mệnh đề bị bỏ có danh từ chỉ phần tử. Kiểm 7 ca xấu + 8 ca lành: **0 lọt, 0 mất**. Bản vá phủ
> **rộng hơn mà sạch hơn**: 1.159 bước (26,0%) · 0 câu suy biến, so với 1.113 (24,9%) · 35 câu.
> · ⛔ **LỖI THỨ HAI CÙNG TỆP: đường lui không `.strip()`.** Khi biến thể không viết lại được, mã
> giữ nguyên câu chuẩn — bản đầu ghi **nguyên xi**, mà **72/589 câu chuẩn có dấu cách ở cuối**
> trong khi `preds_ceiling_human.jsonl` đã strip sạch (0/6.958). Ở đúng những bước lẽ ra phải
> trùng khít lượt trần, bộ trỏ nhận chuỗi lệch **một ký tự** và trả toạ độ khác ở **6 bước**,
> **1 bước đổi hẳn kết luận** (lệch **1.219 px = 113% bề ngang**). ✅ Số của bài **không ảnh
> hưởng** (bước đó nằm NGOÀI phần viết lại, chỉ đụng tổng 0,125 pp) nhưng nó phá khả năng ghép
> kết quả từ tệp thô. Đã `.strip()` cả hai đường.
> · ⚠️ **CÁCH NÓ BỊ BẮT LÀ ĐIỀU ĐÁNG GHI NHẤT.** Script ghép có `assert` hỏi *"bộ trỏ tất định
> không"*; nó đỏ ngay lần đầu (6/589 lệch toạ độ). Chẩn đoán đầu của trợ lý là *"bộ trỏ không
> tất định"* — **SAI**, vì chính bản `assert` đó so chuỗi bằng `.strip()`, **tự tay che mất đúng
> thứ nó cần thấy**. ⇒ **Phép kiểm dùng chính phép biến đổi mà nó cần phát hiện thì mù.**
> · ⭐⭐ **CHẤM LẠI `p3_nopos_v2` TỐN 0 GIÂY GPU, KHÔNG CẦN UPLOAD GÌ — đã kiểm kĩ 6 phép, SO
> BYTE.** Bản v2 chỉ **bớt** số bước viết lại chứ không sinh câu mới, nên mọi bước của nó đã
> được chấm: bước viết lại lấy từ `score_para_<v>_raw.jsonl`, bước không viết lại lấy từ
> `score_ceiling_human_raw.jsonl`. `harness/phep_a_hieu_chinh.py` cài cả 6 phép thành `assert`:
>
> | # | kiểm gì | kết quả |
> |---|---|---|
> | 1 | câu lượt trần == `gold_instruction.strip()` từng byte | 0/6.958 · 0/4.463 |
> | 2 | bước v2 **viết lại**: chuỗi == chuỗi v1 đã chấm | **0/1.055** |
> | 3 | chuỗi bộ trỏ **thật sự nhận** ở lượt v1 == tệp preds | 0/800 |
> | 4 | bước v2 **không viết lại**: chuỗi == chuỗi lượt trần | **0/602** |
> | 5 | hai lượt cùng `n_buttons` · `gold_xy` · `wh` | 0 cả ba |
> | 6 | **tất định**: cùng chuỗi + cùng ảnh ⇒ cùng toạ độ | **0 trên 1.625 phép so** |
>
> ⭐ **Phép 6 mạnh hơn vẻ ngoài:** lượt trần chấm đủ 4.463 bước, mỗi lượt biến thể chỉ 800 ⇒
> **thứ tự và cách gom lô khác nhau**. Cùng chuỗi mà cùng toạ độ trên 1.625 phép so (66+517+517
> +525, bốn lượt độc lập) ⇒ loại luôn khả năng kết quả phụ thuộc **lô hay thứ tự**, không chỉ
> loại khả năng bộ trỏ ngẫu nhiên. ⇒ **con số v2 không phải ước lượng, là kết quả chính xác.**
> ⚠️ Điều duy nhất nó KHÔNG cho: một lượt **độc lập**. Cần *tái lập độc lập* thì vẫn phải trả 1 giờ.
> **Con số v2 −3,5 pp khớp phép loại tay −3,4 pp** ⇒ việc loại 7 câu vốn có căn cứ, và nay **mã**
> loại chúng chứ không phải người ⇒ hết chỗ cho đòn *"loại mẫu hậu kiểm"*.
> · 💡 **BÀI HỌC: trước khi trả tiền cho một lượt chấm, hỏi xem chuỗi cần chấm đã từng được chấm
> chưa.** Cùng họ với mẹo đo trần không cần GPU. **Tệp thô là tài sản** — giữ nó thì đổi luật
> chấm hay đổi tập câu vẫn tính lại được, miễn bộ trỏ tất định và chuỗi đưa vào trùng khít.
>
> **✅ 17/8 — LƯỢT s1/202 XONG cả train lẫn sinh câu; MDE ĐO ĐƯỢC 2,2 pp; LUẬT CHẤM ĐÃ CHỨNG
> MINH BỀN.** · MDE: hệ số nở do cụm thật ra chỉ **1,10×** (đoán 1,5–2×) ⇒ **2,2 pp**, không
> phải 2,7–4,5. · **Năm luật chấm khác nhau** (`harness/rule_sensitivity.py`, 698 bước): trần
> trôi **56,6 → 82,2%** nhưng **thứ tự ba nhánh không đổi ở luật nào**, chênh S1−Base nằm gọn
> **9,5–13,0 pp** ⇒ lá chắn mạnh nhất của chương đo lường.
> · ⛔ **`total_flos` 3.857.778.344 GF ĐÃ RÚT** — số thật **4.142.257.957** (513.164 GF/bước).
> Bằng chứng "không mất bước nào" đổi sang phép so hai hạt giống: 101 đứt **6** lần, 202 đứt
> **3** lần, `total_flos`/bước khớp **0,013%** (513.164 vs 513.229) — chặt hơn và **không vòng
> tròn** như bản cũ lấy thăm dò làm chuẩn (ngoại suy thăm dò lệch **7,7%** vì `max_samples` lấy
> phần đầu tập chưa trộn). ⚠️ `all_results.json` **KHÔNG hỏng** ở `total_flos`, chỉ hỏng
> `train_loss`/`train_runtime`/`*_per_second` sau resume.
>
> **🗂️ 17/8 — `runs/` CHIA THEO PHÉP KIỂM.** `runs/` = ba nhánh chính · `runs/gate_a/` ·
> `runs/paraphrase/` · `runs/venus/` (chưa chạy). **Tải từ Kaggle về đặt thẳng vào thư mục của
> phép đó** — hôm nay bốn tệp lạc vào `report/papers/` (thư mục ghi chú tài liệu tham khảo có
> sẵn từ tháng 7), mất một lượt dọn để nhận ra. Luật đọc ghi ở `runs/README.md`.
>
> **📘 17/8 — `report/112` CẬP NHẬT, 867 → 1.210 dòng, xuất PDF 19 trang.** Sửa tám chỗ, nặng
> nhất: (a) hai khẳng định về bộ trỏ ở §5.4 · (b) **ba chỗ tả sai dụng cụ** — `hit_disk` là
> **hình chữ nhật** dung sai dọc rộng gấp **2,2×** ngang (336 vs 151 px), hạt Voronoi là **điểm
> chạm** không phải tâm nút, và `hit_voronoi` **bao gồm** luật đĩa chứ không thay nó
> (`if not hit_disk(...): return False`) ⇒ Voronoi là bản **siết chặt** của luật quy ước, cấm
> trình như hai lựa chọn ngang hàng · (c) mục mới **§1.6** `history` là câu chuẩn của người
> (trùng 5.318/5.318) ⇒ chấm **teacher-forced trên ngữ cảnh** · (d) mục mới **§5.7** độ bền luật
> chấm · (e) mục mới **§6.7** phép diễn đạt lại · (f) §7 giới hạn từ 7 lên 12 dòng có cột trạng
> thái · (g) lỗi `canon_action` cố tình không sửa: `go back` quy về *tap* (81 bước S1, 47 Base;
> sửa thì 59,12→58,81 và 47,60→47,40 — chênh gần như không nhích) nên giữ nguyên để ba nhánh đã
> chấm còn tái lập được, thêm cờ `strict_back=True` cho lượt mới + mục sửa đổi (v) ·
> (h) §10 lên **13 điều rút ra**.
>
> **⚠️ BÀI HỌC TRA CỨU ĐẮT NHẤT CỦA DỰ ÁN:** chữ *"đã xác minh"* trong ghi chú của **chính
> mình** không phải bằng chứng. Hai khẳng định về bộ trỏ sống **18 ngày**, đi vào bản thảo bài
> báo, rồi bị lật bởi một lần mở đúng Bảng 1 của bài gốc. Trước khi một khẳng định vào bài, mở
> lại **nguồn**, không mở lại ghi chú. Cùng lớp: tài liệu tả thước phải đọc từ **mã**, không từ
> ý định — cách chặn đã áp là hình trong bài dựng bằng script có `assert` gọi thẳng hàm của
> thước (`harness/make_fig_voronoi.py`) nên hình không thể trái mã.
>
> **▶️ VIỆC KẾ (thứ tự theo GIÁ):** ~~(1) p4_both~~ ✅ · ~~(2) chấm lại p3_nopos_v2~~ ✅ (0 GPU) ·
> (3) **chấm s1/202 (5,6 giờ) — ĐƯỜNG GĂNG**, có nó mới khoá được ngưỡng · (4) phép B
> **UI-Venus-Ground-7B** lát 500, ba nhánh, ~6 giờ — đóng giới hạn nặng nhất còn mở; mốc so đã
> tính sẵn **73,4 / 58,8 / 47,6**, chênh **+11,2 pp** · (5) train S2 ×2 hạt giống (~252 đv).
> ⚠️ **Quota Kaggle 30 giờ/tuần**, đã tiêu ~12 (gồm **7 giờ lượt treo**, xem dưới).
>
> **⛔ 17/8 — BÀI HỌC CHẠY KAGGLE: LƯỢT COMMIT TREO 7 GIỜ VÌ LOG NGẬP.** `tqdm` ngoài terminal
> in **mỗi cập nhật thành một dòng** (riêng nạp mô hình >1.400 dòng × 4 lần nạp); Kaggle chặn
> log khi vượt trần ⇒ **tiến trình kẹt cứng ở lệnh ghi stdout**. Bằng chứng: log chỉ có hai mục
> `59.8s` và `25560.4s`, **nội dung giống hệt nhau**, cùng cụt giữa chữ ở
> `Loading weights: 29% | 213/729` — bảy tiếng mà `tqdm` vẫn ước tính "còn 2 giây". **Không
> phải chạy chậm, cũng không phải chạy CPU** (CPU vẫn nạp xong trọng số).
> · **Vá gốc, không vá phần nhìn thấy:** tắt thanh tiến trình bằng biến môi trường **và** cho
> tiến trình con ghi **ra tệp** (`Popen(stdout=f)`), không in qua ống log Kaggle — ghi ra đĩa
> thì không ai chặn ngược được. Cộng nhịp sống in **từ notebook** mỗi 2 phút, độc lập với log
> con. Runbook: **`harness/kaggle_pheA_CHAY_LAI.md`** (có ô 0 kiểm GPU).
> · **CHẠY TƯƠNG TÁC, ĐỪNG Save Version** cho lượt đầu: commit bị huỷ thì Kaggle **không lưu**
> `/kaggle/working`, kể cả tệp thô đã ghi dần ⇒ dừng là mất trắng.
> · **Dấu hiệu quyết trong 4 phút:** không có dòng nhịp sống nào sau 4 phút thì dừng ngay. Chi
> phí biết mình sai giảm từ 7 giờ xuống 4 phút.
> · ⚠️ **Đừng ước lượng nhịp hỏng bằng cảm giác** — trợ lý ban đầu chẩn "chạy CPU nên chậm 10–20
> lần" và khuyên chờ tới 6 giờ; log nói khác hẳn. Đọc log trước khi chẩn.

> ## ⛔⛔ 16/8/2026 — BỘ TRỎ KHÔNG SẠCH. HAI KHẲNG ĐỊNH CŨ ĐÃ BỊ RÚT.
> Năm phản biện độc lập chấm bài FAIR (`paper/fair2026/PHAN_BIEN_5_AGENT_DOC_LAP.md`)
> lật hai điều dự án tin từ 29/7, **đã tra tận nguồn và xác nhận là sai**:
> · ⛔ *"UGround sạch, không có AndroidControl trong recipe"* → **SAI.** Bảng 1 của
> arXiv 2410.05243 liệt kê **AndroidControl 47K phần tử nhãn người**, cùng Widget
> Caption 41K · UIBert 16K · AITZ 8K.
> · ⛔ *"bộ trỏ khác họ mô hình được chấm"* → **SAI.** UGround-V1-2B dựng trên
> **Qwen2-VL**, cùng dòng với Qwen2.5-VL-3B đang bị chấm (`score_run.py` nạp bằng
> `Qwen2VLForConditionalGeneration`).
>
> **Phần còn đứng:** họ lấy từ **split train**, tập kiểm của ta từ **split test** ⇒
> **không chồng lấn ở mức màn hình**, không phải rò rỉ nhãn. Nhưng bộ trỏ đã thấy
> **văn phong chú thích** của kho này, mà s1 lại được dạy viết đúng văn phong đó ⇒
> **còn một lời giải thích thay thế cho chênh lệch s1−base mà 6 đòn phản biện chưa
> loại được.** Cách duy nhất đóng: chấm lát ≥500 bước bằng bộ trỏ đã xác minh sạch AC
> (ứng viên đã tra 15/8: UI-Venus-Ground-7B).
>
> **Ba lỗi mô tả khác cùng lượt, đều đã xác minh và đã vá vào bài:**
> · `history` trong câu nhắc **là câu chuẩn do người viết** ở các bước trước (trùng
> nguyên văn **5.318/5.318 = 100%**), không phải "ba thao tác gần nhất" ⇒ khâu chấm là
> teacher-forced trên ngữ cảnh, mọi số tuyệt đối phải đọc kèm điều kiện đó.
> · `hit_disk` là **hộp chữ nhật** |dx|≤0,14·W ∧ |dy|≤0,14·H (dọc rộng gấp 2,2 lần),
> không phải đĩa Euclid; `hit_voronoi` lấy **chính điểm chạm g làm hạt**, không phải
> tâm phần tử chứa g.
> · Bộ bơm lỗi **không gọi bộ trỏ lần nào** ⇒ hàng "paraphrase 0,0%" chỉ đo cổng chữ,
> **không phản bác được** kết quả của Jandial et al. như bài từng dùng.
>
> **MDE: 2,7–4,5 pp là số ĐOÁN, số ĐO là 2,2 pp** (bootstrap cụm, SE 0,79 pp, hệ số nở
> do cụm chỉ **1,10×** chứ không phải 1,5–2×). ⇒ luật đã đăng ký gọi dải **4–9 pp là
> "không kết luận được"** sẽ **vứt bỏ một hiệu ứng thật** có KTC loại trừ 0 ở p<0,001.
> Đã ghi mục sửa đổi (r) vào `report/106` trước khi chấm bất kỳ nhánh xử lý nào.

> ## 🎓 NGƯỜI MỚI / CẦN HIỂU CƠ CHẾ → ĐỌC `report/112_HIEU_TOAN_BO_KY_THUAT.md` (16/8/2026)
> Một file tự đủ, thiên về **kỹ thuật**: dữ liệu dựng thế nào (ghép hai kho HF + đối chứng
> lệch 2,4×) · nhãn khai báo `<desc>` · bốn nhánh và vì sao cần cả bốn · QLoRA + ba chốt kỹ
> thuật (liger · 4-bit nhanh hơn bf16 · nghẽn ở bảng logits) · thước executability giải thích
> đủ (Voronoi, cổng A, hai công thức sai số) · **phân tích ba nhánh đã chấm kèm ví dụ câu
> thật** · giới hạn · 10 điều rút ra. Đọc file này rồi mới đọc 109 để biết đang ở đâu.
>
> ## 🗺️ ĐỌC `report/109_BAN_DO_HIEN_TAI.md` TRƯỚC — một file nắm toàn bộ (9/8/2026)
> Bài toán · pipeline · 6 nhánh · số đã đo tin được · giới hạn phải khai · trình tự việc kế tiếp ·
> tiền · luật đọc kết quả · tra ở đâu. Khi mâu thuẫn: `report/106` thắng về *phải làm gì*,
> `report/108` thắng về *đã đo được gì*, `report/109` thắng về *đang ở đâu*,
> `report/112` thắng về *cơ chế hoạt động thế nào*.
>
> **⭐ 9/8 — CỔNG A ĐẠT, và toàn bộ phần miễn phí đã chạy xong trên Kaggle T4 (0 đô).**
> · sai số bộ trỏ trung vị **0,7%** (ngưỡng 3%) · ~~trần của thước 70,0%~~ → **75,7%**
> [74,1–77,3] *(đo lại 15/8 trên đủ 4.462 bước; số 70,0 đo trên mẫu con 300, ĐÃ RÚT)* — mọi
> điểm S1/S2 đọc trên nền **75,7**, không phải 100 · ngưỡng 3% xác nhận bằng dụng cụ thật (dưới 3% → 100%
> trúng Voronoi, n=188) · G hiệu dụng tập kiểm đủ **454,3**, MDE chiếu 3,9–6,6 pp.
> · Bốn mắt xích từng "phải thuê máy mới biết" nay đã chạy: cấu hình train được LLaMA-Factory
> nhận (LoRA khớp 14.966.784 tham số) · tự kiểm lô **8/8** · sinh câu · chấm điểm · B-infer.
> · Bật `use_cache=True` sau khi kiểm **trùng tuyệt đối 50/50** → chấm một nhánh 48h xuống **5h**,
> nên **khâu chấm điểm chạy miễn phí trên Kaggle**, không tốn tiền thuê.
> · Giới hạn mới phải khai: bộ trỏ **bỏ cuộc theo trục ngang 15,3%** số bước · **B-infer thiệt ba
> phương diện** (câu nhắc dài gấp 2,4 lần vùng đã dạy, cắt còn 40/72 phần tử, 14,1% có tên).
> · Đã thêm nhánh tham chiếu **mô hình gốc chưa huấn luyện** (report/106 sửa đổi 9/8 mục k).
> **⚙️ CHỐT MÁY 9-10/8 — dùng GOOGLE COLAB, KHÔNG thuê vast.ai** (`report/108` mục 15). Đo máy
> thật: A100 **80 GB**, đốt **6,77 đơn vị/giờ** → **$0,677/giờ**, rẻ hơn vast.ai $0,789 và card
> to gấp đôi. Hai con số cũ của trợ lý đều sai (tưởng 15 đơn vị/giờ, tưởng 40 GB) → **giá GPU
> phải đo/tra tại thời điểm quyết, cấm nhớ**. Về chỗ lưu: thứ bắt buộc sống qua các phiên chỉ
> ~3 GB (derived.tar.gz 400 MB + ckpt + preds) — 15 GB miễn phí cũng đủ chạy trọn luận văn,
> 67 GB ảnh tải lại từ HuggingFace 20–40 phút ≈ $0,3/phiên. *Phần đắt không phải phần to.*
> (`drive.mount` chỉ gắn Drive của chính tài khoản chạy Colab — cross-account không làm được.)
>
> **✅ 10/8 — ĐÃ MUA Colab** trên tài khoản có sẵn **Drive 5 TB** (cùng tài khoản, đúng điều
> kiện `drive.mount`). Chỗ lưu dư → bật `CAT_ANH_DAY = True` ở ô 0.12, cất luôn 67 GB ảnh dạy.
>
> **✅ 11/8 — PHIÊN 0 CHẠY XONG, QUA MỐC DỪNG 3. Đọc `report/110_PHIEN_0_COLAB_11_8.md`.**
> Dữ liệu dạy **64.567 bước / 41.191 chạm (63,8%) / 12.895 tác vụ** · OCR **phủ 100%** và qua
> kiểm chéo máy (23,6 vs 24,2 chữ/màn so với tập kiểm chạy ở máy khác) · nhãn khai báo ở quy
> mô đủ **khớp cả 5 số tham chiếu dưới 1 điểm** (tên rõ 73,6% · không tên 22,0% · vai trò rõ
> 75,8% · trùng tên 7,6% · có hàng xóm 91,6%) · **9/9 bất biến** · **rò rỉ dạy-kiểm = 0** (lần
> đầu kiểm ở quy mô đủ) · phép ghép **2,4×** (48% vs 20%, n=400) · tập kiểm **6.958 / 4.463 / 99,7%**.
> · **Máy: dùng Colab L4 — 12 lõi, 1,54 đơn vị/giờ, rẻ hơn A100 (5,3) 3,6 lần.** Khâu train
> phải đo lại bằng ô A.3 vì train mới thật sự dùng card.
> · **Bài học đắt nhất: đồng bộ Drive mỗi 5 phút.** Mất máy ảo 10/8 (chưa có) = 42 đơn vị +
> 8 giờ; mất máy ảo 11/8 (đã có) = 3 phút. Nghi do trình duyệt/máy ngủ → phải chặn trước
> phiên train 11-18 giờ.
> · ~~**Việc treo:** `app_seen_in_train` 604 bước chưa-thấy vs hồ sơ 6/8 ghi 67~~ → **đã truy
> ra và vá 12/8**, xem khối 12/8 bên dưới + `report/106` mục sửa đổi (p). Con số 604 cũng bị
> rút: nó tính bằng bản mã có lỗi.
>
> **✅ 11/8 chiều — RÀ SẴN SÀNG TRƯỚC KHI TRAIN, vá 9 chỗ.** Đã đo/kiểm bằng runtime CPU
> miễn phí: **độ dài chuỗi** (0% bị cắt nhưng chỉ dư 31 token ⇒ **nâng `cutoff_len`
> 2048→2560**, miễn phí vì đệm theo lô chứ không theo trần) · **đường dẫn ảnh nướng cứng**
> trong 4 tệp nhánh (0 tên ảnh lạ; **cấm đổi `WS` khỏi `/content/ws`**) · **LLaMA-Factory
> nhận trọn cấu hình**, nạp đúng `gui_s1` 64.567 mẫu, qua được khâu mã hoá token · cờ dòng
> lệnh khớp runbook.
> · **Vá cùng lớp lỗi đã mất 42 đơn vị:** `infer_branch.py` và `score_run.py` đều **ghi kết
> quả một lần ở cuối** ⇒ đứt máy là mất trắng 1,5 giờ sinh câu / 5 giờ chấm. Nay cả hai
> **ghi dần + xả đệm + nối tiếp được**; `score_run` gộp số cuối **từ tệp thô, không từ bộ
> nhớ**, nên chạy cắt khúc vẫn ra số toàn tập.
> · **Vá runbook:** ô A.1 thiếu `makedirs` cho `images` (sẽ chết ngay dòng đầu) · A.1 tìm
> `train_images.tar` một tệp thay vì 4 gói · **thứ tự đổi thành `0.3 → Restart → A.1`** (bản
> cũ bung 30 GB hai lần) · A.1 nay bỏ qua khâu bung nếu đã đủ ảnh · A.3 thêm `max_samples`
> (không thì mỗi lượt thăm dò phải mã hoá 64.567 mẫu, ~25 phút tiền card) · mốc dừng 4 bỏ
> con số 6,77.
> · **Mỗi lượt train chờ 20-30 phút TRƯỚC bước 1** để mã hoá token — không phải treo. Không
> dùng `tokenized_path` để né: bộ đệm cũ lệch cấu hình vẫn chạy và ra số của cấu hình cũ.
> · Mọi ô theo dõi bỏ `clear_output`, đổi sang **nhật ký cuộn có mốc giờ + còn bao lâu**.
>
> **⚙️ 11/8 CHIỀU — MỐC DỪNG 4: ĐÃ CHỐT DÙNG A100, KHÔNG DÙNG L4** (`report/110` mục 4h,
> 4h-2, 4h-3; số đo gom ở `harness/run_on_colab.md` mục "📊 SỐ ĐÃ ĐO 11/8" ngay dưới mốc
> dừng 4). Cả hai card đều đạt ba phép kiểm cơ học: tham số **14.966.784** · cỡ lô hiệu
> dụng **16** · `total_flos` **9.527.912 GF**/20 bước.
> · **P0 (4-bit + gradient checkpointing, 4×4): L4 31,26 s/bước · A100-SXM4-40GB 10,70.**
> Một lượt 8.071 bước = **69,5 giờ (L4)** vs **24,0 giờ (A100)**. Hai lượt S1: 5,8 ngày ·
> $21 vs **2 ngày · $25**. A100 nhanh 2,92× mà giá gấp 3,44× ⇒ **đắt hơn 19% tiền, rẻ hơn
> 3 lần thời gian** — hạn nộp 7 tuần nên chọn theo thời gian.
> · ⛔ **L4 KỊCH TRẦN, 22 GB không đủ cho bf16.** Tắt gradient checkpointing **không mua
> được gì** (31,37 vs 31,26); bỏ 4-bit thì tràn bộ nhớ ở cả ba cách (giữ ckpt · tắt ckpt ·
> hạ `per_device` 4→2). OOM ở forward đầu, **21,54/22,03 GB** ⇒ chật chỗ thật, không phải
> sai cấu hình (log in `Gradient checkpointing enabled`, dtype `bfloat16`). P0 vốn đã sát mép.
> · ✅ **Đổi card KHÔNG đổi kết quả** — cùng `seed 101`, loss 20 bước trùng ba chữ số (L4
> `2,036/0,9686/0,8635/0,9553` · A100 `2,040/0,9679/0,8635/0,9547`), `total_flos` y hệt.
> Dùng được cho câu "tái lập khi đổi máy", cùng loại lập luận với kiểm chéo máy OCR (ô 0.9b).
> · **⭐ CHỐT CẤU HÌNH = P9: `train_config.yaml` giữ nguyên + thêm ĐÚNG MỘT KHOÁ
> `enable_liger_kernel: true`.** 10,38 s/bước ⇒ **23,3 giờ/lượt · 123 đv**; 2 lượt S1 =
> 46,6 giờ · 246 đv ≈ $25; 8 lượt = 186 giờ · 987 đv.
> · ⛔ **P10 (tắt gradient checkpointing, 9,03 s/bước) BỊ LOẠI — TRÀN BỘ NHỚ Ở CHUỖI DÀI.**
> Nó chạy ngọt trên mẫu thường nhưng chết trên 200 mẫu dài nhất của s2; bỏ liger cũng không
> cứu (P11 cũng tràn). **12 phút thăm dò cứu một lượt train 20 giờ.** ⇒ **Bài học: probe
> trên mẫu ĐẦU TẬP không đủ kết luận về bộ nhớ** (chuỗi dài nhất 2.017 vs trung vị 1.524
> token) — mọi cấu hình đụng bộ nhớ phải thử lại trên **nhánh nặng nhất với mẫu dài nhất**.
> · ✅ **Liger KHÔNG đổi phép tính, chứng minh bằng số:** cùng 200 mẫu, cùng `seed 101`,
> loss P0 vs P9 trùng tới **chữ số thứ tư** (3.189/3.188 · 3.014/3.015 · 2.597/2.595 ·
> 2.545/2.545). ⇒ dùng được mà **không phải sửa hồ sơ đăng ký trước**.
> · Ô A.3g để lại `s2_long.json` + khoá `gui_s2_long` ⇒ `branches/` giờ có **7 tệp thay vì
> 6** (vô hại, `cfg.yaml` trỏ `gui_s1`).
> · **Đo 4 biến thể bf16 trên A100 (ô A.3d): đều thua.** P4 bf16+ckpt TRÀN ·
> P5 = P4+liger **14,76 s/bước, chậm hơn P0 38%** · P7 bf16 tắt ckpt TRÀN · P8 `8×2` TRÀN.
> ⛔ **Hai kết luận ngược trực giác, đừng thử lại:** (a) **QLoRA 4-bit NHANH HƠN bf16** ở
> bài này (10,70 vs 14,76) — 3B đủ nhỏ để giải nén không thành nút thắt, còn 4,3 GB tiết
> kiệm được lại đúng chỗ nghẽn là activations ⇒ ✅ **cấu hình `report/106` giữ nguyên, KHÔNG
> phải ghi mục sửa đổi**; (b) **chỗ ngốn bộ nhớ là BẢNG LOGITS chứ không phải trọng số** —
> P4 tràn nhưng P4+liger chạy được, vì liger gộp cross-entropy nên khỏi dựng bảng 151.936
> từ vựng × ~1.500 token × 4 mẫu ở fp32. Đây cũng là lời giải cho việc L4 chết ở mọi biến
> thể bf16. **Tổng thăm dò ~3,5 đơn vị cho 10 phép đo trên 2 card.**
> · **Bài học cách đo:** bản A.3b đầu ghép HAI thay đổi vào một biến thể (bỏ 4-bit + tắt
> ckpt) nên tràn bộ nhớ trước khi trả lời được câu nào. **Mỗi biến thể chỉ đổi MỘT thứ.**
> Và hai suy đoán đều sai, log lật cả hai: dtype tưởng fp32 → thật ra `bfloat16`; khoá tưởng
> bị ghi đè → thật ra CÓ tác dụng.
> · ⚠️ Gói `thesis_rented.zip` trên Drive từng là bản CŨ (3.317.166 B, thiếu vá nối tiếp
> 4f) — **đã tải bản mới lên và ô A.1b xác nhận** `infer 26.062 / score 31.277 / Nối tiếp
> True`, `test.jsonl` 6.958, `descriptors` 4.448, `branches` đủ 6 tệp.
> · **Không phải cam kết 8 lượt lúc này** — trình tự khoá là S1 ×2 hạt giống → chấm → MDE
> thật → khoá ngưỡng → mới train S2. Chỉ cần đủ đơn vị cho 2 lượt đầu.
>
> · ✅ **CƠ CHẾ NỐI TIẾP ĐÃ CHẠY THẬT (ô A.3i, mới thêm vào runbook).** Không đợi
> `checkpoint-200` (1 tiếng) như kế hoạch cũ — dựng lượt 10 bước ghi thẳng Drive rồi chạy
> tiếp lên 20, mất **8 phút**: điểm lưu **182,7 MB**/bản · **có `optimizer.pt`** · log in
> `Resuming training from /content/drive/...` · `global_step = 20` không quay về 10 ·
> `trainer_state.json` giữ đủ lịch sử loss. **Xoá được một trong ba việc treo.**
> · **Đã ghi mục sửa đổi (o) vào `report/106`** trước khi có bất kỳ số kết quả nào: máy +
> cấu hình P9 + bằng chứng liger, `cutoff_len` 2048→2560, và **LUẬT CHỌN ĐIỂM LƯU** (dùng
> bản cuối 2 epoch cho mọi nhánh; bản `_ep1` chỉ là bảo hiểm kỹ thuật, **CẤM chọn theo điểm
> trên tập kiểm**; chỉ dùng khi lượt 2 hỏng độc lập với điểm số và phải khai).
> · **THỜI GIAN: một lượt ~24 giờ** (25 phút mã hoá token + 23,3 giờ train + 25 phút ghi
> điểm lưu) · ~126 đơn vị. **Hai lượt S1 ≈ 48 giờ ≈ 2 ngày · ~252 đơn vị ≈ $25.**
> ⚠️ 24 giờ **dài hơn tuổi thọ một phiên Colab** ⇒ chắc chắn phải nối tiếp; mỗi lần đứt tốn
> thêm ~1 giờ (bung lại 33 GB + mã hoá lại), **phần train đã làm không mất**.
> · **Đã cất lên Drive:** `logs/probe_11_8/` (16 log thăm dò = ~5 đơn vị tiền card) ·
> `branches_backup/` (`dataset_info.json` + `s2_long.json`). Ô **A.4b** đồng bộ
> `train.log` + `cfg.yaml` mỗi 5 phút, có `sync.err` giữ lỗi (bản phiên 0 từng nuốt lỗi
> bằng `2>/dev/null`). Ô **A.5** tự sao bản cuối lượt duyệt 1 trước khi `save_total_limit` xoá.
>
> **▶️ 12/8 — LƯỢT TRAIN ĐẦU TIÊN ĐANG CHẠY: `s1` hạt giống 101, khởi động ~03:14.**
> Đo thật ở bước 20: **10,5 s/bước** (thăm dò cho 10,38 — lệch 1,2%) · `total_steps` 8.072 ·
> **`remaining_time` 23 giờ 34 phút** · loss 2,13. Theo dõi bằng
> `ckpt/s1_seed101/trainer_log.jsonl` **trên Drive** — đọc được từ terminal, phiên khác, hay
> điện thoại; không lệ thuộc nhân Python.
> · **Hai lỗi vấp lúc khởi động, đã vá runbook:** (a) `liger-kernel` chưa cài trên máy ảo
> mới ⇒ `llamafactory-cli` chết ngay lúc kiểm phụ thuộc — **ô kiểm 90 giây bắt được ngay lần
> đầu dùng**; (b) lượt chạy được lại chạy **tiền cảnh** nên nhân Python bận, mọi ô khác xếp
> hàng ⇒ **không ngắt**, dùng Terminal Colab để theo dõi (điểm lưu và `trainer_log.jsonl`
> đều ghi thẳng Drive nên nền hay tiền cảnh không đổi độ an toàn).
> · **Bỏ ô A.5b lượt này** — thử nối tiếp phải giết tiến trình rồi trả 25 phút mã hoá token
> lại, trong khi ô A.3i đã xác nhận cơ chế.
> · **⚠️ MẤT MÁY ẢO LẦN 3 lúc bước 1.780** (12/8 ~07h). Giá chỉ **180 bước ≈ 30 phút train**
> (10/8 mất 42 đơn vị · 11/8 mất 3 phút · 12/8 mất 30 phút) — thiết kế cất Drive hoạt động
> đúng. Đã chạy tiếp từ `checkpoint-1600`, khởi động lại 08:51.
> · **Ba lỗi cách chạy đã sửa vào runbook:** (a) ô A.4 dùng `!… nohup … &` **chạy tiền cảnh**
> → chiếm nhân Python, không chạy được ô theo dõi lẫn canh gác; nay dùng
> `subprocess.Popen(..., start_new_session=True)`. (b) `trainer_log.jsonl` **ghi nối thêm**
> nên sau khi chạy lại vẫn còn dòng cũ — ô A.5 phải đặt `MOC` = bước cuối lần trước, không
> thì nó in số cũ trông y như đang chạy. (c) dòng `Resuming training from…` in **rất sớm**
> lúc phân tích tham số, trước 25 phút mã hoá token ⇒ thấy nó chưa nghĩa là đã chạy tiếp;
> bằng chứng thật là `current_steps` > `MOC`.
> · **Ô A.1c mới — SAO LƯU ĐIỂM LƯU trước khi chạy tiếp** (`ckpt_backup/`). Chặn kịch bản:
> nếu nó không nhận ra điểm lưu và bắt đầu lại từ 0 thì `save_total_limit: 2` **lặng lẽ xoá**
> hai bản cũ khi bản thứ ba ra đời — lúc phát hiện thì hết đường về. 182 MB, 1-2 phút.
> · **Phiên đứt thì:** `0.3 → Restart → A.1 → A.1b → A.1c → A.1d → HF_TOKEN → A.2 → A.4 →
> A.4b → A.5`; ô A.2 phải in `BÊN TRONG output_dir` **CÓ `checkpoint-*`**. **Phần train đã
> làm không mất.**
> · ✅ **12/8 08:51 — NỐI TIẾP ĐÃ CHẠY Ở QUY MÔ THẬT**, không còn là chuyện của lượt 10 bước:
> log in `Resuming training from …/ckpt/s1_seed101/checkpoint-1600`. **Kiểm bằng `grep` ngay
> lúc khởi động, đừng đợi** — không nhận ra điểm lưu thì cái giá là 2,5 giờ mã hoá token rồi
> train lại từ bước 0.
> · ⛔ **MÃ HOÁ TOKEN TỐN 2,5 GIỜ, KHÔNG PHẢI 25 PHÚT** (đo 12/8: 7,11 mẫu/giây). Số cũ là
> **suy ra** từ 7,3 mẫu/giây trên 2 lõi × 12 lõi — giả định "chia được cho số lõi" sai:
> `datasets.map` chạy MỘT tiến trình (`ps` cho 165% CPU trên 12 lõi), vì `train_config.yaml`
> không khai `preprocessing_num_workers`. Đã loại ba nghi ngờ khác bằng số đo: 12 lõi · tải
> 1,93 · ảnh nằm đúng `/content/ws` chứ không qua Drive fuse. ⇒ **mỗi lần đứt phiên tốn ~3
> giờ dựng lại, không phải ~1 giờ.** 🔬 Thử `preprocessing_num_workers: 8` bằng lượt thăm dò
> `max_samples` trước lượt hạt giống 202 — ăn thì bớt ~14 giờ tường cho 7 lượt còn lại, và
> **không đổi dữ liệu ra** nên không phải ghi mục sửa đổi report/106.
> · ⚠️ **Mốc giờ "mất máy ~07h" và "train chạy tiếp 12 phút" trong report/110 mục 4j-2 là
> SAI** — `elapsed_time 5:00:06` ở bước 1.780 kéo lùi thì train bắt đầu ~03:40, chạm 1.780 lúc
> ~08:39, khớp với việc khởi động lại 08:51. Kéo theo: lượt đầu mã hoá token có vẻ chỉ mất
> ~25 phút thật, chênh 6 lần với lượt này — nghi bộ đệm `datasets` còn ấm từ thăm dò 11/8;
> **cứ lấy 2,5 giờ làm số của một máy ảo mới.**
> · ✅ **VIỆC TREO `app_seen_in_train` ĐÃ TRUY RA VÀ VÁ** (12/8, miễn phí — report/110 mục
> 4j-5). `tag_app_seen.py` suy tên app của tập dạy bằng **regex trên câu chữ** trong khi tập
> kiểm đọc trường `app_name`; nó quét `goal` trước rồi `break` nên câu mục tiêu dài lọt vào
> thành tên app và tên sạch trong lịch sử không bao giờ được đọc. Hoá ra `train.jsonl` **có
> sẵn** `action.open_app.app_name`. Đo trên lát 1.697 bước: 42/129 tên là rác → 0/90; khớp
> được 35 → **60** trong 269 app tập kiểm; **27 app có thật bị đếm nhầm thành chưa-thấy**
> (`maps`, `nike`, `citymapper`, `skyscanner`…). Phần còn lại của khoảng cách: con số 67 hôm
> 6/8 là vá tay không có mã, đối chiếu với split train ĐẦY ĐỦ của AndroidControl chứ không
> phải 12.895 tác vụ thật sự dựng. Chỉ đụng lát cắt phụ. **Số thật phải chạy ô A.1d trên
> Colab** với `train.jsonl` đủ 64.567 bước, và bản `test.jsonl` đã gắn nhãn **phải mang sang
> Kaggle** vì `score_run.py:405` đọc nhãn thẳng từ đó.
> · ⚠️ **Nhân Python bận thì dùng Terminal Colab** — ô A.4 chiếm nhân, mọi lệnh theo dõi
> (`grep` log · `tail` `trainer_log.jsonl` · `ps`) đều chạy được từ Terminal.
> · Ảnh tập kiểm 3,2 GB **không cần lúc train** — xoá được để lấy chỗ, bung lại bằng **ô
> A.5c** trước ô A.6. Đĩa máy ảo 113 GB: ảnh dạy 30 + bộ đệm HF 8,3 + **~40 GB ảnh nền
> Colab**. ⚠️ `du -sh /content/drive` báo 40 GB là **nội dung trên Drive**, không phải đĩa
> máy ảo — rất dễ đọc nhầm thành thủ phạm đầy đĩa.
>
> · ✅ **12/8 TRƯA — CHẠY TIẾP ỔN ĐỊNH, ba phép đo tốc độ hội tụ** (`report/110` mục 4j-6).
> **Khâu nhảy qua 1.600 lô dữ liệu chỉ tốn ~17 giây** (94 lô/giây) ⇒ **toàn bộ giá của một
> lần đứt phiên nằm ở mã hoá token, không ở khâu nhảy** — kể cả đứt ở bước 6.000. Tốc độ ở
> quy mô thật **10,29 s/bước** (1.640 lúc 11:33 → 2.060 lúc 12:45), khớp thăm dò 10,38 trong
> 0,9% và số bước-20 là 10,5 trong 2%. ⇒ một lượt trọn = **23,1 giờ train + 25 phút ghi điểm
> lưu + 2,5 giờ mã hoá token nếu máy mới ≈ 26 giờ tường, ~123 đơn vị**. Lượt s1/101 dự kiến
> xong **~05:55 sáng 13/8**. Loss gộp 200 bước: 1,103 (20–200) → 0,690 → 0,701 → 0,650 →
> 0,666 → 0,641 → 0,625 → 0,632 → 0,633 → **0,611** (1.820–2.000). Rơi mạnh 200 bước đầu
> (học định dạng) rồi giảm chậm đều; **chưa chững** vì `lr 9,227e-5` ở bước 1.780 = mới đi
> 8% lịch `cosine`. **Mốc ngó tiếp: bước 4.036 (~18:20 ngày 12/8)** = ranh giới lượt duyệt 2,
> tụt một nấc là bình thường, **tăng dần đều sau đó** mới là học vẹt.
> · ⚠️ **HAI BẪY ĐỌC TIẾN ĐỘ, đều là lỗi ô theo dõi** (`report/110` mục 4j-7): (a) hỏi 60
> giây một lần trên cửa sổ 20 bước (~206 giây) cho ra **răng cưa 9,0/12,0 s/bước**, giờ xong
> nhảy giữa 03:40 và 08:55 — **đo tốc độ phải neo MỘT mốc rồi chia cả quãng**, cách neo sai
> 0,2% thay vì 17%; (b) `trainer_log.jsonl` ghi nối thêm nên **không lọc được bằng ngưỡng
> bước** — sau khi chạy tiếp, dòng mới đầu tiên là 1.620 *thấp hơn* dòng cuối cũ 1.780, đặt
> `MOC=1780` thì câm 35 phút, đặt `MOC=1600` thì in lại dòng cũ. **Đọc DÒNG CUỐI**; dựng
> đường cong thì khử trùng lặp theo số bước giữ lần sau cùng.
> · ⚠️ **Chữ `disconnect` trên trình duyệt KHÔNG phải bằng chứng máy chết** — 12/8 hiện chữ
> đó trong khi train vẫn chạy. Bằng chứng thật: `st_mtime` của log train cách hiện tại dưới
> ~120 giây. Log **không** tên `train.log` mà là `/content/train_{BRANCH}_seed{SEED}.log`
> (ô A.2 sinh `LOG`) → dò bằng `glob("/content/train_*.log")`.
>
> · ⚠️ **MẤT MÁY LẦN 4 (12/8 ~16:30, bước ~3.360)** — chạy tiếp từ `checkpoint-3200` lúc
> 17:06, mất **160 bước ≈ 27 phút**. Máy mới vẫn A100-SXM4-40GB, tốc độ y hệt **10,2 s/bước**
> ⇒ đổi máy ảo cùng loại card không đổi tốc độ.
> · ⭐ **`preprocessing_num_workers: 8` ĂN ĐẬM — mã hoá token 42 phút thay vì 2,5 giờ**
> (`report/110` mục 4j-6c). Log in `num_proc=8`, `Converting format` 48.419 mẫu/giây. Nhanh
> **3,6 lần**. **Áp cho bảy lượt còn lại và mọi lần đứt phiên.** Không đổi dữ liệu ra ⇒ không
> phải ghi mục sửa đổi `report/106`. Cách áp: sau ô A.2, thêm khoá vào `/content/cfg.yaml`
> trước khi chạy A.4.
> · ✅ **Nhịp tụt ở ranh giới lượt duyệt 2 đã xảy ra đúng bước 4.036:** `tb10` từ 0,54–0,575
> (3.260–4.060) xuống **0,495** (4.220) rồi **0,465** (5.100). ⚠️ **KHÔNG phải bằng chứng
> khái quát tốt hơn** — gặp lại dữ liệu lần hai thì loss huấn luyện giảm là đương nhiên; chỉ
> đọc thành "lượt train khoẻ". ⛔ **Rút dự báo sàn 0,548** — mới 5.100 đã 0,465; khớp hàm mũ
> là cận trên vì không mô hình hoá được nhịp epoch 2. **Đừng quyết định gì dựa trên ngoại suy
> loss.**
> · ⚠️ **Ô A.1d đang chạy bản mã CŨ** — `thesis_rented.zip` trên Drive đóng gói TRƯỚC bản vá
> `tag_app_seen.py` sáng 12/8 (nhận ra vì thiếu dòng in `(trường app_name … + suy từ câu chữ
> …)`). ⇒ con số **604 bước chưa-thấy vẫn là số của bản có lỗi** *(đã vá 14/8 → **139 bước /
> 22 app**, xem khối 14/8 bên dưới)*. Không chặn train; phải đóng
> gói lại zip rồi chạy lại A.1d **trước khi chấm**.
>
> · ⛔ **MẤT MÁY LẦN 5 (12/8 tối, bước 5.540) — phép thử "gập nắp mang máy đi làm" THẤT BẠI**
> (`report/110` mục 4j-8). Ba lệnh `powercfg … -dc 0` + lid *Do nothing* + không đóng tab
> **không đủ**: log ngừng ghi ngay sau khi gập nắp, không phải chạy được vài giờ. **Đừng thử
> lại** — để máy chạy tại chỗ có sạc, hoặc chấp nhận đứt và tính luôn 1,8 giờ dựng lại. Giá
> lần này: 140 bước ≈ 24 phút train + 1,4 giờ dựng lại ≈ $0,9. **Cộng dồn 5 lần: ~12 giờ,
> ~60 đơn vị**, còn bảy lượt ~24 giờ ⇒ **phải tra gói Colab có `background execution` không**
> (Pro+ có) — xoá hẳn lớp lỗi này, đáng hơn mọi tối ưu tốc độ đã làm.
> · ⚠️ **`grep "Resuming training from"` TRỐNG ngay sau A.4 là BÁO ĐỘNG GIẢ** — log lúc đó 0
> byte, dòng đó in sau ~40 giây nạp thư viện. **Đừng `pkill` ngay**; hỏi ba thứ trước:
> `getsize(log)` · `ps -p <PID>` · `tail -30`. Suýt giết một lượt chạy lành.
> · ✅ **Phép kiểm rẻ "điểm lưu có trọn không": ghi dở thì bản CUỐI phải NHỎ HƠN bản trước.**
> 13/8 cỡ đổi 182,7 → **191,6 MB** nhưng cả 5200 lẫn 5400 đều 191,6 ⇒ cả hai trọn vẹn.
> Và `yaml.safe_dump` ghi đè `cfg.yaml` **không mất khoá nào** (đủ 34 khoá), chỉ mất chú thích.
>
> **▶️ 13/8 12:47 — CHẠY TIẾP TỪ `checkpoint-5400`**, `preprocessing_num_workers: 8` đã vá vào
> `cfg.yaml` (`Converting format` 33.177 mẫu/giây). Chạy êm 8 giờ tới bước 7.880.
>
> · ⛔ **MẤT MÁY LẦN 6 (13/8 ~20:30, bước 7.880 — cách đích 192 bước).** Điểm lưu cuối
> `checkpoint-7800`, mất 80 bước. Đã dựng lại và chạy nốt 272 bước (~46 phút train + ~1,4
> giờ dựng lại ≈ $1,1). **Chọn chạy nốt thay vì lấy `checkpoint-7800` làm bản cuối** — hai
> bản gần như không khác gì về số (`lr` đoạn đó đã xuống ~1e-8), nhưng `report/106` đăng ký
> trước là *dùng bản cuối 2 lượt duyệt*, nên $1,1 mua được một dòng không phải giải trình.
> · ⚠️ **NHÂN PYTHON RESTART LÀM RỚT GẮN DRIVE — và đó là dấu hiệu nhận biết rẻ nhất.** Ô
> theo dõi văng `FileNotFoundError` trên `trainer_log.jsonl` trong khi tệp vẫn nằm nguyên
> trên Drive web. Thấy lỗi này thì **đừng chạy lại A.4**, chạy ô chẩn đoán (tên máy · `ps` ·
> `st_mtime` của `/content/train_*.log`) rồi mới quyết.
> · ✅ **ĐUÔI LỊCH COSINE ĐÚNG SÁCH.** Từ bước 6.060 → 7.840 (1.780 bước, 5 giờ) `tb10` chỉ
> đi 0,4712 → 0,4554 trong khi `lr` tụt 1,61e-05 → **2,28e-07**. Biên độ `loss` một lô là
> 0,103 còn `tb10` chỉ 0,0215 — hẹp hơn ~5 lần, đúng quy luật √10 ⇒ **cái "nhảy qua nhảy
> lại" là nhiễu giữa các lô, không phải mô hình trồi sụt**. Phẳng ở đây là kết thúc sạch,
> không phải chững vì hỏng.
> · **Cộng dồn 6 lần mất máy: ~14 giờ, ~70 đơn vị.** Đã tra: tài khoản đang dùng **đơn vị
> trả trước, KHÔNG đăng ký Pro/Pro+ ⇒ KHÔNG có `background execution`** — phải sống chung
> với lớp lỗi này, hoặc nâng gói. Còn **~355 đơn vị** sau lượt này.
>
> **✅ 13/8 22:43 — LƯỢT TRAIN ĐẦU TIÊN XONG: `s1` hạt giống 101, đủ 8.072 bước / 2 lượt
> duyệt** (`report/110` mục 4j-10). `adapter_model.safetensors` 59,9 MB.
> · ⛔ **Ba số trong `all_results.json` SAI sau resume, cấm trích:** `train_loss 0,0151`
> (HF cộng loss chỉ từ lúc khởi động lại 272 bước rồi chia cho cả 8.072 — số thật ≈ **0,447**,
> kiểm: 0,01505 × 8.072 ÷ 272), `train_runtime 45:55`, `samples/steps_per_second`. **Mọi số HF
> chia cho `elapsed` đều hỏng sau resume** (cùng lớp với `remaining_time`). Dùng
> `trainer_state.json`, ô A.10 đã bóc sẵn.
> · ⛔ ~~`total_flos` 3.857.778.344 GF khớp ngoại suy từ thăm dò trong 0,32%~~ **SỐ GHI SAI, ĐÃ
> RÚT 17/8.** Đọc lại `trainer_state.json` + `all_results.json` của lượt 101: cả hai cho
> **4.142.257.957 GF** (513.164 GF/bước). Kết luận "cả 8.072 bước chạy thật, không mất cũng
> không lặp" **vẫn đứng** nhưng bằng chứng cứ khác, chặt hơn và **không vòng tròn**: hai lượt
> độc lập với số lần đứt khác hẳn nhau (101 đứt **6** lần · 202 đứt **3** lần) cho `total_flos`
> /bước khớp **0,013%** (513.164 vs 513.229); kế toán sai sau resume thì hai lượt phải lệch
> theo số lần đứt. Ngoại suy từ thăm dò lệch 7,7% vì lượt thăm dò chạy `max_samples` = lấy
> **phần đầu tập chưa trộn**, độ dài chuỗi không đại diện. ⚠️ **`all_results.json` KHÔNG hỏng ở
> trường `total_flos`** — chỉ `train_loss`/`train_runtime`/`*_per_second` hỏng sau resume.
> · **Mốc dừng 5: A.6 ĐẠT 8/8** · **A.7 sạch** (câu mạch lạc, không lặp; 8 câu xem tay: 2
> trùng gần nguyên văn, 1 sai app thật, 1 tả vị trí thay vì gọi tên — n=8, **chưa phải kết
> quả**) · ⛔ **A.7b lộ lỗ: chữ ký lượt chạy KHÔNG hoạt động** — `--ceiling gold` ghi vào tệp
> của lượt lora vẫn in `Xong sẵn`. Nối tiếp thì chạy đúng nhưng in `Nạp …` trước ⇒ **gói
> `thesis_rented.zip` trên Drive là bản TRƯỚC các vá sáng 12/8** (cùng nguyên nhân với A.1d
> ra 604). Không chặn lượt này; **phải đóng gói lại zip trước chiến dịch nhiều nhánh.**
>
> · ✅ **14/8 — `app_seen_in_train` ĐÃ CÓ SỐ THẬT, việc treo cuối cùng của phiên train đã
> xoá** (`report/110` mục 4j-11). Đóng gói lại zip với bản vá (`infer_branch.py` 26.062 →
> **27.443 B**, có chữ ký lượt chạy) rồi chạy A.1d trên runtime CPU **miễn phí**:
> **604 → 139 bước chưa-thấy** (22 app), 465 bản ghi đổi nhãn; app nhận ra ở tập dạy
> 2.766 → **1.717** (phần giảm là rác regex). ⚠️ **PHẢI SỬA TRONG LUẬN VĂN: con số
> "92% app tập kiểm cũng có ở tập dạy" nay là 95,6%** — lợi thế sân nhà **rõ hơn**, không
> nhẹ đi; vẫn kèm cảnh báo 3.828/6.958 bước (55%) *không gán được app* = **không biết**,
> cấm đọc thành *chưa thấy*. Tệp mang sang Kaggle: `MyDrive/thesis/test_jsonl_tagged.jsonl`.
>
> **⭐⭐ 15/8 — TRẦN THẬT LÀ 75,7% [74,1–77,3], KHÔNG PHẢI 70,0%** (`report/110` mục 4j-13).
> Chấm câu chuẩn của người trên **đủ 4.462 bước** thay vì suy từ 300 điểm cổng A. **Cách làm
> rẻ bất ngờ: không cần GPU Colab** — dựng tệp `preds` với `pred = gold_instruction`
> (`runs/preds_ceiling_human.jsonl`) rồi chấm như mọi nhánh, 0 đồng.
> Chênh **+5,7 điểm**, nằm ngoài mép trên KTC cũ; KTC hẹp từ ±5,4 xuống **±1,6**.
> ⛔ **Con số 70,0% ĐÃ BỊ RÚT** — mọi chỗ phải dùng **75,7%, n=4.462**. Đã sửa xong
> `paper/fair2026/main.tex` (abstract · contribution 2 · mục IV-D · bảng chính · Conclusion),
> bài vẫn **8 trang chẵn**, và đã thêm dòng `Base 47,6` vào bảng.
> · **BẢNG BA NHÁNH, cùng 4.462 bước:** Human **75,7%** · S1 **59,1%** · Base **47,6%**
> (hit_voronoi thuần 75,8 / 60,2 / 48,9 · action_ok 100 / 94,4 / **96,5**).
> · Ghép cặp McNemar đều p<0,001: S1−Base **+11,5 pp** (χ²=243) · Human−S1 **+16,6 pp**
> (χ²=580, **c=843 bước người trúng mà S1 trượt** ← đúng vùng S2 có thể ăn) · Human−Base **+28,1**.
> · **MDE ghép cặp 1,8–2,1 pp** (chưa cụm) ⇒ **ước 2,7–4,5 pp có cụm** ⇒ **S2 chỉ cần lấy
> 16–27% room**, trước tính 40–60%. **Room mới: 741 bước = 16,6 pp** (trước 485 = 10,9);
> S1 đạt **78,1% của trần**; SFT lấy **41%** khoảng Base→trần.
> · ⭐ **NĂM ĐÒN PHẢN BIỆN "S1 hơn Base" ĐỀU BỊ BÁC:** phong cách (Base cũng mở đầu `click`
> 84%; động từ chạm 86,0% vs 87,5%) · `action_ok` (bỏ đi vẫn **+11,3 pp**) · loại bước (+15,0
> và +11,0) · độ khó màn (+12,7 / +9,4 / +12,3) · cụm (thắng **395**, hoà 565, thua **131**).
> ⇒ **S1 hơn Base là chắc chắn.**
> · ⚠️ **THƯỚC MÙ 24,3%:** 1.083 bước câu người cũng trượt, **72% do bộ trỏ sai >14% bề ngang
> (bỏ cuộc)**; sai số lưỡng cực (trúng 0,4% · trượt 26,2%). **935 bước (21%) cả ba nhánh cùng
> trượt.** ⇒ **trần 75,7% là giới hạn DỤNG CỤ, không phải của ngôn ngữ.**
> · ✅ Nghi ngờ "câu chuẩn hỏng làm hạ trần" **bị bác**: câu chuẩn ≤3 từ cho trần **77,0%**.
> · ⚠️ **Giới hạn chưa kiểm: chỉ MỘT bộ trỏ (UGround)** — so giữa các nhánh hợp lệ vì cùng
> dụng cụ, nhưng **số tuyệt đối gắn với UGround**.
>
> **▶️ 15/8 21:22 — LƯỢT `s1` HẠT GIỐNG 202 ĐANG CHẠY** (A100, dự kiến xong **~21:30 ngày
> 16/8**). Đây là **đường găng**: cặp hạt giống S1 = **null thực nghiệm**, không có nó thì
> không khoá được ngưỡng và mọi kết luận về S2 đều treo.
> · ⭐ **Ô kiểm vàng đã thành quy trình cố định: `harness/run_on_colab.md` ô A.2b.** So cfg
> lượt này với cfg lượt tham chiếu; **chỉ 4 khoá được phép khác** (`seed` · `output_dir` ·
> `dataset` · `preprocessing_num_workers`), khoá thứ năm là **dừng hẳn**. Lượt 202 kiểm ra
> **38/38 khoá, chỉ khác `seed` và `output_dir`** ⇒ cặp hạt giống hợp lệ. Kèm ô kiểm dữ liệu:
> `s1.json` md5 **641953d75d61ab192b94a559362cce9b** · 64.567 mẫu.
> · ⚠️ **Ô A.1b đã sửa số kỳ vọng: `infer 27.443 / score 34.610`** (bản trước ghi 26.062 /
> 31.277 là của gói cũ). Đã xác nhận **`metric_exec.py` KHÔNG sửa dòng nào** ⇒ luật chấm không
> đổi, mọi nhánh đã chấm vẫn so được với nhau.
>
> **✅ 17/8 00:40 — LƯỢT s1 HẠT GIỐNG 202 XONG, ĐÃ SINH XONG 6.958 CÂU. CẶP HẠT GIỐNG ĐỦ.**
> Chi tiết: `report/110` mục **4j-15**. Tệp: `Drive/thesis/preds/preds_s1_seed202.jsonl`
> (2,3 MB · 6.958 dòng · 0 hỏng · 0 trùng · chữ ký thuần `lora:s1_seed202`).
> · **Cặp hạt giống khớp rất chặt** — `total_flos`/bước **513.164 vs 513.229 (0,013%)** ·
> loss đuôi-20 **0,4486 vs 0,4467** · và lượt 202 mắc **đúng lỗi** của 101 ở cùng bước 18175/0
> (*"Open Tripadvisor app"* thay vì Foursquare, n=8 nên chỉ đọc là "đường ống chạy đúng").
> · **Cả hai lượt bỏ đúng MỘT bước vì câu rỗng, và là CÙNG bước `(18710, 1)`** ⇒ chấm trên
> **cùng 4.462 bước** trong 4.463 bước chạm ⇒ ghép cặp McNemar sạch, không phải trừ bù.
> Đây cũng là nguồn gốc con số 4.462 dùng từ đầu; `score_run.py:516` xử lý sẵn (`bo_qua`).
> · ✅ **A.7b XONG — việc treo từ 13/8 đã đóng.** Nối tiếp khâu sinh câu ghi thêm thật (20→30
> dòng) VÀ chữ ký chặn đúng (`--no-adapter` lên tệp lora → thoát ngay). ⚠️ **Phép thử nối tiếp
> phải xin NHIỀU HƠN số đã có** — lần thử đầu xin đúng 20 khi đã có 20 nên `còn 0`, in
> `Xong sẵn`, trông như đạt mà không chứng minh gì.
> · **Việc kế:** tải preds về → tắt Colab → Kaggle: thêm vào `thesis-preds`, chấm bằng
> `score_run.py --mode score --grounder uground` (5,6 giờ, 0 đồng, Save Version → Commit)
> → **MDE thật tính CẢ HAI CÁCH** → khoá ngưỡng vào `report/106` → mới train S2.
>
> **▶️ 16/8 — LƯỢT 202 MẤT MÁY HAI LẦN (lần 7 và 8), đã chạy tiếp, còn ~9 giờ.**
> Lần 7: chết 05:02 ở bước 2.480, chạy tiếp 05:27 từ `checkpoint-2400` (mất 80 bước).
> Lần 8: chết ~12:45 ở bước 4.880 sau khi chạy được **2.320 bước ≈ 6,6 giờ**, chạy tiếp 13:27
> từ `checkpoint-4800`. Dự kiến xong **~23:30 ngày 16/8**. Cộng dồn 8 lần: ~18 giờ, ~85 đơn vị.
> · ⛔ **`MOC` PHẢI LẤY THEO DÒNG LOG CUỐI, KHÔNG THEO SỐ ĐIỂM LƯU** — bẫy mới, đã vá runbook
> (ô A.1c nay tự chốt vào `/content/MOC.txt`; ô A.5 đọc từ đó). `logging_steps: 20` mà
> `save_steps: 200` ⇒ **log luôn chạy trước điểm lưu tới 180 bước**. Đặt `MOC = 4800` theo
> điểm lưu trong khi phiên chết ở 4.880 ⇒ bộ lọc `> MOC` không chặn được dòng cũ, ô theo dõi
> in `4.880` **ba lần liền suốt 45 phút** mã hoá token, trông y hệt train đang chạy mà đứng yên.
> 💡 Dấu hiệu miễn phí nhận ra phiên mới đã ghi thật: **số bước TỤT XUỐNG** (4.880 → 4.820),
> vì dòng mới đầu tiên = điểm-lưu + `logging_steps`. Thấy số lùi là mừng.
> · ⚠️ **Bài học đọc nhịp mất máy:** trợ lý suy "hai lần cách nhau 1,5 giờ ⇒ dựng lại lâu hơn
> quãng chạy được ⇒ lượt train không bao giờ về đích" rồi đề nghị mua gói mới. **Sai** — đọc
> `checkpoint-4800` mới biết phiên đó chạy 6,6 giờ. **Đừng ước lượng nhịp hỏng bằng cảm giác;
> lấy hiệu số bước giữa hai điểm lưu.**
> · ✅ **Ô kiểm vàng A.2b chạy 3 lần trong ngày, lần nào cũng 38/38 khoá, chỉ khác `seed` và
> `output_dir`** — kể cả `preprocessing_num_workers` cũng khớp, vì cfg tham chiếu của lượt 101
> đã được ô đồng bộ ghi lại lên Drive sau khi vá giữa chừng 12/8.
> · 📘 **ĐÃ VIẾT `report/112_HIEU_TOAN_BO_KY_THUAT.md`** — một file tự đủ giải thích cơ chế
> toàn dự án cho người chưa biết gì, thiên kỹ thuật, kèm ví dụ câu thật lấy từ `runs/*.jsonl`.
>
> · 🔬 **15/8 — ĐÃ TRA XONG BỘ TRỎ THỨ HAI, ĐỪNG TRA LẠI** (`report/110` mục 4j-14).
> **Chọn `inclusionAI/UI-Venus-Ground-7B`** (Apache-2.0): ScreenSpot-v2 mobile **99,0/90,0**,
> **mạnh hơn UGround** (95,0/83,3), sạch AndroidControl, lấy điểm = tâm bbox chuẩn hoá 0–1.
> Ưu tiên **A100 hơn T4** vì NF4 ăn vào đúng thứ cổng A đo. Dự phòng: **Phi-Ground-4B** (ngoài
> họ Qwen nhưng yếu ở mobile 78,1) · **ShowUI-2B** (vừa T4, ⚠️ lỗi tràn số fp16 → NaN).
> ⛔ **Đã loại:** GUI-G2-3B (trùng nền Qwen2.5-VL-3B với generator) · **Jedi (CÓ
> AndroidControl** dù tự quảng bá chỉ dữ liệu tổng hợp) · CogAgent (link chết, vĩnh viễn không
> kiểm được) · Aria-UI (25,3B) · SE-GUI/GUI-G1/GUI-R1/Holo1/POINTS-GUI-G (nhiễm gián tiếp).
> · **Cách chạy: lát 500 bước, chỉ S1 và Base, ~1,2 giờ.** Toàn tập 3 nhánh = 17 giờ quota,
> không đáng. Làm **sau** khi S2 chạy, không chặn gì.
> · ⚠️ **CÂU CHỮ:** viết *"bộ trỏ không được huấn luyện trên AndroidControl"*; **CẤM** viết
> *"chưa từng thấy màn hình di động"* — chúng dùng Widget Captioning/UI RefExp/RICO đều là kho
> Android. Lập luận phụ trợ: ba nguồn đó (2020/2021/2017) **có trước AndroidControl (6/2024)**.
> · ⛔ **Đính chính lời trợ lý:** câu "mọi bộ trỏ GUI mở đều dựng trên họ Qwen-VL" là **SAI**
> (Phi-Ground dựng trên Phi-3.5-Vision). Câu đó đã lỡ vào Limitations của bài, **đã vá**.
>
> **📄 14/8 — BÀI FAIR'2026: HẠN THẬT LÀ 31/8, NỘP QUA EDAS.** (`paper/fair2026/README.md`
> mục 1). Mâu thuẫn 15/8-vs-31/8 đã được **chính hệ thống phân xử**: EasyChair báo
> `Paper submission for FAIR 2026 is closed`; EDAS (`edas.info/index.php?c=35461`) đang mở,
> hiện `Register paper by Aug 31`. ⇒ **17 ngày** kể từ 14/8. Track chọn **Natural Language
> Processing**. Không phản biện ẩn danh ⇒ giữ tên tác giả. Mẫu IEEE, nộp **PDF** nên bản
> `IEEEtran` dùng được, **không phải chuyển Word**. Bản thảo `paper/fair2026/main.tex` đã
> đủ 8 trang, đã điền tác giả (Lê Đoàn Phương Uyên · Nguyễn Hồng Bửu Long · Faculty of
> Information Technology, University of Science, VNU-HCM), đã bỏ mục `Acknowledgment` trống.
> · **Lịch tới 31/8:** chấm s1/101 (Kaggle, 5,6 giờ, 0đ) → train s1 hạt giống **202**
> (~26 giờ, ~126 đv) → chấm → 🛑 **MDE thật, khoá ngưỡng** → train **S2 ×2** (~52 giờ,
> ~252 đv) → chấm ×2 → viết Results. **Đủ thời gian để bảng chính có ablation thật.**
> · ⚠️ **Hai ràng buộc tài nguyên:** đơn vị Colab còn ~355, cần ~378 ⇒ **mua thêm ~$10**;
> **Kaggle chỉ 30 giờ GPU/tuần** mà mỗi lượt chấm 5,6 giờ ⇒ tối đa 5 lượt/tuần, đừng dồn.
>
> **⭐⭐ 14/8 — ĐIỂM SỐ THẬT ĐẦU TIÊN: `s1` hạt giống 101 = executability 59,1%
> KTC95 [57,3–60,8]**, n=4.462 bước chạm, cụm 1.091 · **hiệu dụng 454,3** (khớp đúng con số
> tính trước 9/8). Đĩa dung sai 69,2% [67,6–70,7]. Chấm 5,6 giờ trên Kaggle T4, **0 đồng**.
> Chi tiết + phân tích: **`report/110` mục 4j-12**; tệp: `runs/score_s1_seed101.json` +
> `runs/score_s1_seed101_raw.jsonl` (tệp thô — đổi luật chấm thì chấm lại từ đây, **không
> gọi lại bộ trỏ**, tiết kiệm 5,6 giờ mỗi lần).
> · ✅ **ĐIỀU KIỆN SỐNG CÒN ĐẠT — S1 KHÔNG chạm trần.** Trần **75,7%** [74,1–77,3] vs S1 59,1%
> [57,3–60,8], **hai KTC không chồng lấn**; cũng không suy biến về sàn. Room **16,6 pp** >
> MDE ⇒ **cuộc thí nghiệm còn đáng chạy** (trước 14/8 chưa ai biết chắc). *(Số ban đầu ghi
> trần 70,0 và room 10,9 — đã rút sau khi đo lại 15/8.)*
> · ✅ **15/8 — BÀI ĐÃ CÓ SỐ VÀ ĐÃ ĐÚNG MẪU. Trạng thái một trang ở đầu
> `paper/fair2026/README.md`.** Mục VII đổi từ bảng rỗng thành **Baseline Results** (s1/101
> 59,1%, các nhánh khác `—`) + bảng lát cắt chẩn đoán. Việc còn lại **chỉ đụng Bảng VI**:
> s1/202 → MDE thật (**tính cả hai cách**, độc lập và **ghép cặp McNemar** vì mọi nhánh chấm
> trên cùng 4.462 bước) → khoá ngưỡng; và Base đang chấm.
> · ⛔ **LỖI TEMPLATE ĐÃ BẮT, loại im lặng:** dưới XeTeX họ font `ptm`/`pcr` không dựng được
> nên **PDF không hề dùng Times như mẫu IEEE đòi** — LaTeX thay ngầm bằng Computer Modern,
> log chỉ ghi `defaults substituted`. Vá bằng `fontspec` + TeX Gyre Termes/Heros/Cursor;
> vá chữ xong **số vẫn là CM** nên phải thêm `unicode-math` + `texgyretermes-math`. Kiểm
> bằng cách bung stream PDF đọc `/BaseFont`, đừng tin mắt nhìn.
> · **Đã đối chiếu DBLP + Crossref cả 23 tài liệu** — bắt 5 lỗi: 2 mục thiếu tác giả
> (GuideMe = Fang et al. CHI'26; EACL = Jandial et al.), EACL là **Findings** (DOI
> `2026.findings-eacl.144`), `W. E. Bishop` không phải `W. W.`, AITW trong kỷ yếu tên
> **AndroidInTheWild** viết liền, UI-R1 thiếu chữ *Efficient*.
> · **Đã rà bài ngược lại MÃ và DỮ LIỆU** (`paper/fair2026/KIEM_LAI_MA_VA_DU_LIEU.md`): 18
> khẳng định tái lập được; bắt 3 lỗi nội dung, nặng nhất là **định nghĩa thước trong bài
> không khớp `metric_exec.py`** — mã là hội của BA điều kiện và `hit_voronoi` **vẫn đòi nằm
> trong đĩa 14%**, tức Voronoi là bản SIẾT CHẶT của luật quy ước chứ không phải phương án
> đối lập. Sửa xong bài mạnh hơn.
> · ⭐ **LỢI THẾ SÂN NHÀ KHÔNG XUẤT HIỆN:** app đã-thấy **59,1%** (n=1.737) · CHƯA-thấy
> **59,0%** (n=78) · không-gán-được **59,2%** (n=2.647). Đòn phản biện nặng nhất tự khai từ
> 6/8 (*"95,6% app tập kiểm cũng có ở tập dạy nên điểm bị thổi"*) **không có cơ sở thực
> nghiệm** — nay khai giới hạn kèm số bác bỏ, không khai suông.
> · ✅ **Chỗ hỏng đúng chỗ S2 nhắm:** gọi đúng loại thao tác **94,4%**; trong 1.824 bước
> trượt chỉ **251 do sai thao tác**, **1.573 (86%) là thao tác đúng mà bộ trỏ không tìm ra
> nút** ⇒ lỗi ở **cách gọi tên/tả phần tử**. Đo trên mô hình thật, không phải suy từ pilot.
> · ⚠️ **ROOM THẬT CHỈ ~485 BƯỚC (10,9 pp), KHÔNG PHẢI 1.573.** Trần 70% nghĩa là câu người
> viết cũng trượt 30% (~1.339/4.462) ⇒ phần sửa được về nguyên tắc = 1.824 − 1.339 ≈ **485**.
> **S2 phải sửa 40–60% trong số đó** mới vượt MDE. Hiệu ứng kỳ vọng văn liệu trung vị ~+5 pp
> **nằm ngay trong dải MDE 3,9–6,6** ⇒ P(đọc được) ≈ **50%**, khớp ước ban đầu.
> **Rủi ro cụ thể: S2 − S1 rơi vào 0–4 pp ⇒ kết cục "trắng".**
> · ⚠️ **THIÊN VỊ CÂU DÀI ĐO ĐƯỢC: 5,4 pp** (câu >33 ký tự 61,9% vs ≤33 là 56,5%). **S2r
> kiểm soát độ dài TIỀN TỐ, KHÔNG kiểm soát độ dài CÂU RA** ⇒ **bắt buộc phân tầng độ dài
> khi đọc S2**.
> · 🔬 **MIỄN PHÍ, CÓ THỂ ĐỔI CỤC DIỆN: tính MDE GHÉP CẶP (McNemar), đừng tính hai mẫu độc
> lập.** S1 và S2 chấm trên **cùng 4.462 bước** ⇒ chỉ đếm bước bất đồng; **MDE thật có thể
> xuống dưới 3 pp**. Khi có s1/202 phải tính **cả hai cách** rồi mới khoá ngưỡng.
> · ⚠️ **Chưa kết luận được gì về S1-vs-S2** — một hạt giống, chưa biết nhiễu giữa hạt giống,
> chưa có S2. **Vẫn CẤM viết bảng so sánh.** Viết được: chương dữ liệu · chương đo lường ·
> phương pháp · tái lập · giới hạn · **và nay thêm dòng `S1 (seed 101)` trong bảng chính.**
>
> **▶️ 15/8 — `Base` (mô hình gốc, `--no-adapter`) ĐÃ SINH XONG 6.958 câu, đang chấm trên
> Kaggle.** Xem tay 20 bước: **viết câu tiếng Anh tốt, đúng khuôn, gọi tên nút cụ thể** ⇒ mốc
> so **sạch**, không lẫn với chuyện "không theo khuôn"; nhưng **3/8 câu lạc sang bước khác**
> ⇒ thứ SFT dạy được là **bám đúng bước hiện tại**, không phải khả năng viết.
> · ⚠️ **Base dài trung vị 71 ký tự, S1 chỉ 33** ⇒ thiên vị câu dài 5,4 pp **nghiêng về Base**.
> Cách đọc: **S1 > Base ⇒ kết luận mạnh** (thắng dù chịu bất lợi độ dài) · **Base ≥ S1 ⇒ chưa
> kết luận, phải phân tầng độ dài trước.**
> · **Bài học đã ghi (memory `moc-so-re-nhat-chay-truoc`):** xếp thứ tự thực nghiệm theo
> **GIÁ**. Ba nhánh chỉ-suy-luận còn lại (`--ceiling gold`, `--ceiling filler`, `--b-infer`)
> tổng ~24 đơn vị + chấm miễn phí ⇒ **chạy hết trước khi động tới S2**. Riêng `--ceiling gold`
> đáng nhất: nó đo trần trên đủ 4.463 bước, thay con số 70,0% hiện chỉ dựa trên n=76.
> · **Máy:** phiên 15/8 dùng **L4** (~31 s/bước ⇒ 70 giờ/lượt, so A100 24 giờ). Đổi card
> **không đổi kết quả** (đã chứng minh 11/8) và **nối tiếp được từ điểm lưu**, nên đổi giữa
> chừng an toàn — chỉ tốn ~1,4 giờ dựng lại.
> · **Trạng thái:** s1/101 ✅ train+chấm · Base ✅ sinh, ⏳ chấm · s1/202 ⏳ · S2×2 ⏳ ·
> ba nhánh suy luận ⏳. Đã tiêu ~190 đơn vị ≈ **$19** (gồm ~70 mất vì 6 lần đứt máy).
>
> **▶️ VIỆC KẾ:** `0.3 (cài gói + liger) → Restart → A.1 → A.1b → A.1c → A.1d →
> đặt HF_TOKEN → A.2 → A.4 → A.4b → A.5` (bỏ A.3/A.3d/A.3i — đã đo xong, đừng trả tiền lại)
> → 🛑 **mốc dừng 5** (A.6 tự kiểm lô 8/8 · A.7 xem câu sinh · **A.7b thử nối tiếp sinh câu,
> mã này vẫn CHƯA chạy**) → A.8/A.9/A.10 → chấm (Kaggle, miễn phí) → **MDE thật** → khoá
> ngưỡng → mới train S2.
> **Việc treo còn lại:** (a) chạy ô **A.1d** để lấy con số `app_seen_in_train` thật ở quy mô
> đủ, rồi mang `test.jsonl` đã gắn nhãn sang Kaggle; (b) thử `preprocessing_num_workers: 8`
> trước lượt hạt giống 202; (c) **A.7b** (nối tiếp khâu sinh câu) vẫn chưa chạy lần nào.

> ## 🔒 CHỐT 5/8/2026 — ĐÃ ĐĂNG KÝ TRƯỚC VÀ COMMIT, ĐỌC `report/106_DANG_KY_TRUOC.md`
> **Thầy không gặp được → chạy luôn, không đợi chốt miệng.** Vì mất bước đó, `report/106` gánh vai trò niêm phong thiết kế: khoá 6 nhánh, thước đo, **luật đọc kết quả cho cả 4 kết cục** (dương / dương yếu / trắng / âm), 3 lát cắt, hạt giống 20260805. Đã commit `b93e85c` (SHA cũ `51ddb35`, đổi khi viết lại lịch sử 21/8). Mọi thay đổi về sau **ghi vào mục sửa đổi cuối file, KHÔNG sửa đè**.
>
> **Đã dựng xong, chạy được ngay khi có máy:**
> · `harness/descriptor_label_build.py` — nhãn khai báo bản thật (`<point>` toạ độ, không còn lưới 3×3). Bắt 2 lỗi: cây trợ năng lồng nhau làm "trùng tên" thổi từ 30%→6,9%, và tên class Android lọt vào nhãn.
> · `harness/build_branch_data.py` — 4 nhánh s1/s2/s2r/s2_nopoint, định dạng sharegpt. **Khai báo giả của s2r lệch độ dài trung bình 0,5 ký tự** nên không đổ hiệu ứng cho "chuỗi dài thêm" được. 623/1697 bước không-chạm giữ đích y hệt ở mọi nhánh → phép kiểm không-gây-hại đọc được.
> · `harness/build_test_data.py` — **tập kiểm 6.969 bước / 1.432 tác vụ / 4.465 bước chạm (64,1%)**, ghép chuẩn (khớp 37% vs đối chứng lệch 10%). ⚠️ chỉ **44,9% gán được app** → số cụm hiệu dụng do nhóm cụm-đơn chi phối, MDE thật phải tính lại từ đây.
> · `harness/infer_branch.py` · `harness/score_run.py` (gồm **cổng A**) · `harness/run_on_rented.sh` — ba mắt xích trước đó KHÔNG tồn tại: chưa có script suy luận, `metric_exec.py` hoá ra chỉ là thư viện hàm chấm chứ không có gì gộp số.
> · `harness/train_config.yaml` viết lại: bỏ khung Student/Student-RAW cũ, một file cho mọi nhánh chỉ đổi 3 dòng. Bắt 2 lỗi: **thiếu `seed`** (giao thức 2 hạt giống không có chỗ khai) và `val_size: held_out_by_app` là giá trị không hợp lệ.
>
> **⚖️ QUYẾT ĐỊNH 5/8 — nguồn tên trong nhãn: BÁC việc đảo sang OCR-trước, áp A′.** Chi tiết `report/107_DEBATE_NGUON_TEN.md`. Phát hiện: dump cây trợ năng **không có trường `text`**, chỉ `content_description` (tên chức năng). Tưởng phải đảo sang OCR vì câu chuẩn theo OCR gấp 3,2 lần — nhưng vòng phản biện bóc ra: bán kính thật chỉ **72/1074 = 6,7%**; bỏ 32 ca chuỗi-số-có-sẵn-trong-mục-tiêu còn 40 ca lõi (OCR 12 – trợ năng 3); và **11/12 ca OCR thắng là do nhãn trợ năng RÁC**. ⇒ ưu thế của OCR là ưu thế của **lọc rác**, không phải của thứ tự. Đã áp: cổng `clean_a11y` (14,7% nhãn là rác) + cổng hình học ≤25% màn (25 ca hộp to, **0/25 khớp câu chuẩn**) + luật ghép OCR cùng dòng. Nhãn: tên rõ 77,2%→**73,8%**, không tên 19,9%→**23,4%** (ít tên hơn nhưng sạch hơn). **Cấm dùng A′ giải thích hậu kỳ nếu S2 thắng** — nó nằm dưới mọi kịch bản MDE.
>
> **📒 SỔ KÊ KHAI = `report/108_DA_LAM_DUOC_GI.md`** — mở file này khi cần biết đã làm được gì, số nào tin được tới đâu, mã ở đâu. Có mục riêng liệt kê **24 lỗi đã bắt được** (loại chạy vẫn trơn nhưng kết quả sai) và **danh sách số đã bị rút, cấm dùng lại**.
> **⚠️ SỬA 6/8 — TẬP KIỂM KHÔNG PHẢI APP-UNSEEN:** 92% ứng dụng trong tập kiểm cũng có ở tập dạy (chỉ 21 app unseen = 67 bước chạm). Con số "631 tác vụ app-unseen" của hồ sơ cũ KHÔNG áp dụng cho dữ liệu đang dùng. Phép so chính S1-vs-S2 **vẫn hợp lệ** (hai nhánh đối xứng, 0 tác vụ trùng dạy/kiểm), nhưng **mốc so gpt-4o-mini hạ xuống tham khảo** và bắt buộc khai lợi thế sân nhà. Nhãn `app_seen_in_train` đã ghi sẵn trong test.jsonl. Tập kiểm chốt: **6.958 bước / 4.463 bước chạm / 1.432 tác vụ**.
> **▶️ VIỆC KẾ:** (1) chạy OCR tập kiểm `prep_ocr_train.py --split test` (free, vài tiếng) → (2) thử đường ống bằng bộ trỏ rẻ ~30 bước (~$0.3) → (3) **cổng A** ($4-8, cần GPU) → (4) train s1 ×2 hạt giống → chấm đủ → **MDE thật** → khoá ngưỡng → (5) mới train s2.
> **Slide + script trình bày:** `LUAN_VAN_SLIDE_v9.pptx` (23 slide chính + 4 slide dự phòng ẩn chứa ảnh bảng gốc) · `report/104` (script 15 phút) · `report/105` (nguồn từng con số, ảnh bảng cắt từ PDF gốc). ⚠️ **3/4 số trong bảng bằng chứng là hiệu tự trừ từ bảng của họ, không phải số in sẵn** — khai trước khi bị vặn.

> ## 🧭 NGUỒN-SỰ-THẬT HIỆN TẠI (cập nhật 29/7/2026) — ĐỌC HAI FILE NÀY TRƯỚC
> **`report/100_TONG_QUAN_PIPELINE.md`** = bản cho người CHƯA biết gì, chỉ có bài toán + pipeline + số. Không kể lịch sử. **Đây là file đưa thầy đọc trước** (thầy muốn nghe pipeline, không quan tâm đã làm gì).
> **`report/98_BAN_TRINH_THAY_DAY_DU.md`** = hồ sơ đầy đủ, có cả phần tự kiểm và các chỗ còn hở, dùng khi thầy hỏi sâu. Slide: **`LUAN_VAN_SLIDE_v9.pptx`** (4/8 — 22 slide trọn flow theo report/103, style mẫu bài giảng Lê Văn Luyện: 4:3, chàm 322164, khối xám bo góc, Cambria; build `slides/build/build_v9.js`, preview `slides/build/_preview_v9/preview.html`; bìa còn ô trống học viên/GVHD/trường + chữ "PU © 2026" ở footline phải sửa). Bản PDF LaTeX cùng nội dung: `slides/latex/LUAN_VAN_SLIDE_v9.tex` (build tectonic). v7/v8 pptx cũ → `slides/_archive/`.
>
> ## ⭐⭐ CHỐT 1/8/2026 — THÀNH PHẦN ĐÓNG GÓP ĐÃ KHOÁ, ĐỌC `report/103_CHOT_THANH_PHAN.md`
> **🔎 VÒNG RÀ 3/8 (đã vá thẳng vào 103 v3 + memory `verify-vong-3-8`):** ① −42,8 của GCoT là **số TỰ TÍNH** từ Table 3−4, bài chỉ viết 45,4 — trích phải chú thích; Table 5 (+4,5/+5,8) đúng số NHƯNG họ train from-scratch với data quen đề, không tách được nguyên nhân → ablation S1-vs-S2 của mình chặt hơn, chủ động khoe. ② Cặp "35/69" → số đúng **32/69** (chia trung vị 8 từ, 76 câu gold, `ground_pilot`). ③ UI-Ins −3,2/+4,7 là **hai model nền khác nhau**, cấm ghép cặp. ④ LLaVA-CoT +3,4 gồm retracing, thuần cấu trúc +1,5. ⑤ GuideMe xác nhận: prompting GPT-5, KHÔNG train, chấm bằng user study 18 người, CÓ trả toạ độ. ⑥ Debate 9 phương án gia cố: **0 adopt, khung giữ nguyên**; 3 thứ lấy về đã vá vào 103: lỗ off-policy mức 2 (§2) · phép thử nhân quả trên S1 trước khi train S2 (§5+§8) · thước dự phòng chọn-trong-danh-sách kèm điều kiện chống tự-chấm (cuối §8). Chi tiết: 103 mục 14.
> Bốn vòng tra tài liệu độc lập (fable, 1/8) đã lật 3 điểm. **Chốt MỘT thành phần: "mô tả phân biệt trước, phát ngôn sau"** — đích sinh `[vai trò | tên | <point>x,y</point> | dấu hiệu phân biệt]` rồi mới tới câu; chấm chỉ lấy câu. Headline = ablation S1 (SFT trơn) vs S2.
> · **✅ NỖI LO GCoT TAN**: số âm −42,8 là **prompting zero-shot**; chính bài đó Table 5 cho thấy **TRAIN theo thứ tự grounding-trước thì độ đúng TĂNG +4,5 / +5,8** (LLaVA-7B/13B). Đừng trích một nửa nữa. (2503.12799 = **preprint**; bài ICCV 2025 là bài KHÁC, 2507.02859.)
> · **⛔ GIÁM SÁT CHÚ Ý RÚT KHỎI THÂN**: 2511.12738 KHÔNG còn là preprint — **WACV 2026**, tên thật *"Direct Visual Grounding by Directing Attention of Visual Tokens"*, **fine-tune chính Qwen2.5-VL-7B**, đúng cơ chế định làm (KL trên attention visual token, target Gaussian từ bbox, λ=1). Cộng: Liu AAAI-17 độ lớn thật chỉ **+0,7…+0,9 BLEU-4**; ước công lại **8–10 ngày**; FOCUS (ICML 2026) cũng bbox-attention-loss. → chỉ giữ **đo attention IoU** (~$1, không train) làm mục phân tích tuỳ chọn.
> · **✅ KHE CÒN MỞ 3 PHÍA**: 2606.18101 (*Trust the Right Teacher*) và 2605.00642 (*GUI-SD*) — verify tận nguồn, **cả hai đích sinh THUẦN TOẠ ĐỘ**, PI là ảnh vẽ khung làm INPUT; 2606.18101 nguyên văn *"the target response contains no additional natural-language reasoning or rationale"*.
> · **Ràng buộc thiết kế có căn cứ**: descriptor phải CÓ CẤU TRÚC + CÓ TOẠ ĐỘ, vì văn tự do cho dấu ÂM (Shikra bằng lời −7,39 vs chain-có-point +5,90; UI-Ins free-form −3,2 vs +4,7). Hiệu ứng kỳ vọng +3…+11, trung vị ~+5; bằng chứng gần nhà nhất = **Aguvis bỏ inner monologue → AndroidControl-Low −11,4**.
> · **🔑 ĐIỀU KIỆN TIÊN QUYẾT — LỰC THỐNG KÊ** *(sửa 2/8 sau phản biện: bản cũ chia sai quần thể — 2.400 bước là của 752 ep, còn 78 app chỉ phủ 363/631 ep gán được)*: chấm đủ bước chạm toàn tập kiểm + **quy tắc cụm-đơn cho 268 ep không gán app** (G 78→346, G_eff ~35→~98). MDE **ƯỚC CHIẾU** ~4–7 pp; số chốt PHẢI tính lại từ điểm S1 thật (2 seed) trước khi khoá ngưỡng — trình tự cứng: S1×2 seed → chấm đủ → MDE thật → khoá ngưỡng → mới train S2.
> · **⚖️ VÒNG PHẢN BIỆN ĐỐI KHÁNG 2/8 (3 giám khảo độc lập): ĐỦ-CÓ-ĐIỀU-KIỆN.** 4 đòn chí mạng đã vá vào 103 v2 (§16 = nhật ký đòn→xử): (1) seed — S1/S2 phải **×2–3 seed**, cặp seed S1 làm null thực nghiệm; (2) MDE chiếu ≠ MDE đo; (3) quần thể 31-bước/app sai; (4) **thiếu dự phòng nếu bộ trỏ chuyên rớt Cổng A** → bậc thang 3 mức ở §14. Điều kiện hội đồng giả: **pilot mức-2 (loss) BẮT BUỘC** trong thân · nhánh **B-infer** (descriptor vào input lúc suy luận, không train) · no-harm cho 41% bước không-chạm · chấm tay 100 câu 2 người · demo tiếng Việt định tính · câu thủ LUPI (Vapnik) cho đòn "S2 dùng thêm dữ liệu" · chương đo lường = đóng góp có tên trong thân. Số cũng bị vá: 8/10 bơm lỗi PHẢI kèm 2 mục rớt (fp_paraphrase 59,2% FAIL · đảo-nghĩa held-out 0%) · dải Voronoi phải trình đủ kể cả +6,6/+3,9 · 35/69 đo trên câu GOLD + confound độ dài · pilot descriptor đo bản zone-3×3 chứ CHƯA phải bản `<point>` (phải nâng script). Tiền mới: **$85–112** (trần $123–162 nếu kích hoạt seed 3 + scale mức 2).
> · **Mức 2 (margin/unlikelihood hàng xóm) = cùng thành phần, quyết ở cổng tuần 3 bằng số.** Khe GUI mở (Widget Captioning + Screen2Words CE thuần; LPO ACL26 làm trên toạ độ; DPO-GUI làm trên trajectory) NHƯNG cơ chế bị **Mao CVPR 2016 MMI-MM** chiếm trọn → cấm chữ "mới", phải chủ động trích. TRL DPOTrainer hỗ trợ VLM, ví dụ chính chủ dùng Qwen2.5-VL-3B + QLoRA.
> · **Đối chứng đăng ký trước**: S1 · S2 · **S2r (prefix SAI cùng độ dài — chưa tiền lệ nào chạy)** · S2-nopoint · phân tầng độ dài + độ mơ hồ · chấm tay. Bộ trỏ chấm khác họ, không nhiễm AC.
> · **Giới hạn phải khai**: *"Do GUI Grounders Truly Understand UI Elements?"* (**Findings EACL 2026**) — ⛔ **cách mô tả "trượt 84% khi đổi diễn đạt" ĐÃ BỊ RÚT 18/8**, xem khối đầu file.
>
> **Hai đóng góp:** (1) MÔ HÌNH — Qwen2.5-VL-3B QLoRA, headline = ablation nội bộ SFT-trơn vs SFT+thành-phần; "hơn gpt-4o-mini" chỉ phụ. (2) ĐÁNH GIÁ — executability (bộ trỏ khôi phục toạ độ + control không-câu + luật đảo-nghĩa + chấm nút-gần-nhất) + faithfulness (phụ, trên MobileViews), validate bằng bơm lỗi.
>
> **⭐ THÀNH PHẦN THÊM ĐÃ CHỐT 29/7 (sau 2 vòng debate Fable 5) = HAI LỚP, bỏ hướng RFT làm trụ:**
> · **Lớp 1 "trỏ trước viết sau"** — đích huấn luyện = `<point>x,y</point>` rồi mới tới câu; lúc chấm cắt bỏ phần toạ độ. Dùng toạ độ gold mà SFT trơn bỏ phí. **Sạch nhất về phản biện** (không công cụ ngoài ở cả hai phía dạy/chấm), chi phí ~0.
> · **Lớp 2 "danh sách chữ làm đầu vào"** — OCR ra danh sách chữ + vị trí, nối vào đầu vào lúc dạy VÀ lúc chạy (module đứng trước). Đánh trúng cơ chế hỏng số 1 (gọi sai/mơ hồ tên nút: câu cộc 35% vs câu tả rõ 69%). **Bắt buộc 2 đối chứng**: nhánh chỉ-đưa-lúc-chạy, và nhánh giả dược đưa danh sách của MÀN KHÁC.
> · **RFT tự-sinh-tự-lọc = TUỲ CHỌN**, không làm trụ: bộ trỏ rẻ kết oan 42-59% → tập lọc chỉ sạch ~70% (huấn luyện trên 1/3 nhãn sai); đắt nhất; mang tiếng luyện-đúng-bài-thi. Muốn chạy phải qua cổng riêng (bộ trỏ lọc ≥85% trúng, ≤10% giữ nhầm, khác họ với bộ trỏ chấm).
> · Cả hai lớp đều làm câu DÀI hơn mà thước thiên vị câu dài → **bắt buộc phân tầng theo độ dài câu + báo phân bố độ dài + chấm tay vài chục câu**.
>
> **📊 SỐ ĐÃ ĐO (bản 28-29/7, đã qua phản biện; chi tiết `memory/exec-metric-status-28-7`):** chênh trần−sàn DƯƠNG ở mọi cách chấm nhưng phải trình DẢI: **+44.7 (đĩa) · +32.9 (gộp tâm) · +19.7 (hộp, loại hộp chứa gold = đúng bản chất nhất)**; n=76 nên CI ±10. Bơm lỗi bản 2 **đạt 8/10** ngưỡng khoá trước. Bước chạm 59.1%, gõ/cuộn/mở app 28.9%. Công tắc dùng chung vị trí 1.06%. G=78 app (hiệu dụng 34.8) trên 363/631 ep gán được.
> **⛔ ĐÃ BỊ RÚT, đừng dùng lại:** "dải thật [13…45]" · "chênh 32.9 + hai bộ dò đồng thuận" · "bơm lỗi 9/10 độc lập" (bản 1 có 5 nhánh hằng đẳng thức) · "bộ dò trả nhiều hộp cho cùng một nút" (SAI, 286 cặp hộp sát nhau đều IoU=0) · "SD 0.362 đo từ pilot" (thực ra = √2 × sd một nhánh) · lập luận Material Design 48dp.
> **🚧 CHẶN ĐƯỜNG LỚN NHẤT:** cách chấm chặt kết oan nhiều khi bộ trỏ lệch. Đường cong đo bằng dụng cụ thật (cây trợ năng + Voronoi): lệch 3% kết oan 0%, 5% → 7,5%, 8% → 24,1%, 13% → 55%. → điều kiện tiên quyết Cổng A = **sai số trỏ trung vị ≤3% bề ngang**, KHÔNG phải "trúng 80%".
> **⛔ SỬA 6/8 — "trung vị 8% cạnh" LÀ SỐ SAI, ĐÃ RÚT.** Nó đẻ ra từ `real_offsets()` trong `exec_injection_validate.py:144`, hàm này **chỉ lấy sai số của những ca bộ trỏ ĐÃ TRÚNG dung sai** rồi mới tính trung vị — loại sạch mọi lần trượt. Số không lọc: **15,0%** theo công thức `ground_pilot` (`median_dist` lưu trên đĩa, n=76) và **29,3%** theo công thức cổng A (đo 6/8, n=10 tập kiểm). Thêm nữa hai script dùng hai công thức khác nhau — `ground_pilot` chia lệch dọc cho chiều CAO nên nhẹ đi 2,2 lần, cổng A dùng khoảng cách pixel chia bề NGANG; chênh 1,63 lần trên cùng dữ liệu. Ngưỡng 3% nói theo công thức cổng A. ⇒ **gpt-4o-mini chưa bao giờ gần cổng A**, và khoảng cách tới ngưỡng bị hồ sơ cũ thu nhỏ khoảng 3,5 lần. **MDE chưa khoá được** (pilot 3.5 bước/app, nhiễu > tín hiệu; bảo thủ 10.7-16.0 pp).
>
> **💾 NGUỒN DỮ LIỆU MỚI (29/7) — gỡ hai nút thắt cũ:** `HarrytheOrange/parsed_AndroidControl` (HF) có **`step_instructions` cho cả 15.283 episode** (nguồn dạy cho train split, trước giờ vẫn treo) + **`all_forest_dict.zip` 452MB = cây trợ năng thật 99.131 màn** (bounds/class_name/content_description), không cần GCS + tensorflow. ⚠️ Đo rồi: trung vị **86 phần tử/màn** nhưng **chỉ 12.6% có TÊN** (22/120 màn có 0% nhãn) → **chỉ dùng cho chấm vị trí**, KHÔNG thay được OCR ở khâu lấy tên, KHÔNG đo được faithfulness trên AC. Bản `ckg/AndroidControlParsedWithImages-20k` có ảnh nhưng đã parse thành định dạng agent, **mất step_instructions** — đừng dùng làm nguồn dạy.
>
> **📚 VÒNG TRA TÀI LIỆU 29/7 — KẾT QUẢ BUỘC HẠ GIỌNG (đã verify tận nguồn):**
> · **Lớp 1 có tiền lệ:** **GCoT** (preprint 2503.12799) đã so thẳng "định-vị-trước" với "trả-lời-trước"; Shikra/CogCoM(ICLR25)/Visual CoT(NeurIPS24) cùng dòng sinh toạ độ làm bằng chứng. ⚠️ **GCoT đo được: grounding-first làm ĐỊNH VỊ tốt lên nhưng ĐỘ ĐÚNG CÂU TRẢ LỜI kém đi** — rủi ro ngược chiều, phải nêu. (Phản biện: họ prompting mô hình chưa train, ta TRAIN theo thứ tự đó; và ta đo đúng phần định vị.) Trong GUI, Aguvis(ICML25)/UI-R1 đặt **chữ trước toạ độ sau** → ta ĐẢO VAI. ✅ **ĐÃ VERIFY PDF Aguvis (tr.19)**: khuôn mẫu huấn luyện = `Thought: … / Low-level Instruction: … / Action: pyautogui…` — mô hình TỰ SINH cả câu chỉ dẫn mức thấp. Nên phân định phải nói chính xác: bên họ câu chữ là bước trung gian để ra ACTION cho máy và **chất lượng câu không được đánh giá**; bên ta câu chữ là SẢN PHẨM CUỐI cho người đọc, là thứ duy nhất đem chấm.
> · **⛔ Lớp 2 KHÔNG được kể là đóng góp:** **bài gốc AndroidControl (NeurIPS24) đã fine-tune với danh sách phần tử từ a11y làm INPUT và không dùng screenshot** (verify nguyên văn: *"Our agent implementation does not directly leverage the page screenshot"*). Thêm Mind2Web(NeurIPS23) train trên danh sách ứng viên nhiễu; Widget Captioning(EMNLP20)/Screen2Words(UIST21) train với cây phần tử ở input; **RAFT(COLM24)** đã trả lời "train-với-nhiễu hơn chỉ-đưa-lúc-chạy" ở miền RAG. → hạ xuống **lựa chọn thiết kế có ablation**.
> · **✅ ĐIỂM PHÂN ĐỊNH VẪN VỮNG:** trong bài gốc AC, `step_instructions` là **INPUT** (mớm cho agent đoán action); ta dùng làm **ĐÍCH SINH**. Ngược hướng — đây là chỗ định vị rõ nhất.
> · **Đối chứng THIẾU vừa bổ sung cho lớp 1:** (a) có/không prefix toạ độ · (b) **prefix toạ độ SAI/ngẫu nhiên** (loại khả năng điểm tăng do chuỗi dài thêm) · (c) toạ độ cho sẵn trong prompt làm trần trên. Lưu ý ngân sách token: prefix làm chuỗi dài ra → nhánh đối chứng cần tiền tố giả cùng độ dài.
> · **CẤM DÙNG:** "đầu tiên"/"novel"/"cơ chế mới" cho cả hai lớp · đặt tên kêu cho thứ tự sinh rồi dùng như thuật ngữ chuẩn · nói "GuideMe không đụng toạ độ" (mô tả công khai cho thấy nó CÓ định vị để tô sáng; chỉ chưa rõ có train hay không).
>
> **🔬 ĐO THÊM 29/7 (chiều):** · **Bộ tứ với cây trợ năng THẬT** (62 phần tử/màn, hệ toạ độ đã kiểm khớp ảnh: gold nằm trong hộp 76/76): **trần 6.6% · sàn 0.0% · chênh +6.6**. Chẩn đoán trọn vẹn: phần tử đích **189×126 px**, phần tử KHÁC gần nhất chỉ cách **69 px**, bộ trỏ rẻ lệch trung vị **256 px** → gần như luôn rơi vào ô phần tử khác. **Con số thấp này đo DỤNG CỤ, không đo câu.** Củng cố ngưỡng Cổng A: sai số phải < 69px → đặt 3% cạnh (~32px) là có biên. `harness/a11y_inventory.py` + `voronoi_sensitivity.py`.
> · **✅ DỮ LIỆU DẠY ĐÃ THÔNG:** ghép `HarrytheOrange` (câu người viết, 15.283 ep) với `ckg/…WithImages` (ảnh) theo (episode_id, step_id). Kiểm ghép ĐÚNG bằng OCR tại điểm chạm: khớp **47%** vs đối chứng ghép-lệch-một-bước **27%**. Số ảnh > số bước đúng 1 là **ảnh màn cuối**, không phải lỗi. Đã dựng **1.697 bước / 2 shard** (833 MB) → `harness/dg1_cache/train_ac/` (`train.jsonl` + `images/`). Toàn bộ 76 shard ~67GB → chỉ dựng vài shard ở máy, còn lại tải thẳng trên Colab. Code: `harness/build_train_data.py`, `prep_ocr_train.py` (đang chạy nền).
>
> **🏛️ TRỤ ĐÓNG GÓP MÔ HÌNH ĐÃ CHỐT 29/7 (1 vòng phản biện + 2 vòng tra tiền lệ) — chi tiết `memory/tru-dong-gop-model-chot-29-7`:**
> **"MÔ TẢ TRƯỚC, PHÁT NGÔN SAU"** — đích huấn luyện hai tầng: sinh bộ mô tả có cấu trúc `[vai trò | chữ hoặc hình | vị trí | dấu hiệu phân biệt]` rồi mới sinh câu; nhãn tầng mô tả dựng TỰ ĐỘNG từ hộp a11y tại điểm chạm gold + OCR + caption crop. Lúc chấm chỉ lấy câu. → ứng viên DUY NHẤT mà **mô hình lúc suy luận hành xử khác** ⇒ đóng góp MÔ HÌNH, không phải data.
> **Đã loại:** DPO cặp câu-đúng/tả-nhầm-hàng-xóm (bắn trượt cơ chế hỏng — lỗi số 1 là câu MƠ HỒ 35% vs 69%, không phải nhầm nút vì K2 đo bịa 0-2%; lại ký sinh vào tầng viết lại) · người-nói-người-nghe (tiền lệ trực diện + vòng vo + nhánh "gpt-4o-mini + listener" có thể thắng) · che-ngữ-cảnh (không đổi chữ nào trong đích nên vẫn kẹt câu cụt). **Viết lại nhãn có đặc quyền = GIỮ nhưng hạ xuống TẦNG DỮ LIỆU**, khai thẳng là tiền xử lý.
> **⛔ TIỀN LỆ BẮT BUỘC PHÂN ĐỊNH (đã verify):** dòng REG phân biệt đã chiếm ý "câu phải đủ để bên kia trỏ đúng" **từ 2016 cả ở tầng huấn luyện** (Mao CVPR16 MMI · Luo CVPR17 critic trong vòng train · Yu CVPR17 · White CogSci20) → cấm chữ "đầu tiên"/"mới"; thủ sẵn đòn "sao không đưa bộ trỏ vào vòng train như Luo 2017" = vì bộ trỏ cũng là thước chấm. **Widget Captioning (EMNLP20) — ĐÃ TRÍCH PDF VERIFY: loss chỉ cross-entropy thuần, KHÔNG có thành phần phân biệt** dù họ nêu rõ vấn đề hai icon giống nhau → **ĐÂY LÀ KHE của trụ**. Vẽ dấu gold rồi nhờ mô hình lớn sinh mô tả: **UGround (ICLR25 Oral)** + UI-Ins, nhưng làm ĐẦU VÀO cho grounder. PI trong GUI: **Trust the Right Teacher (2606.18101)** + GUI-SD (2605.00642), đầu ra là TOẠ ĐỘ. **AndroidControl-Curated (2510.18488)** sửa instruction nhưng chỉ mẫu bị mọi agent làm hỏng, để làm sạch benchmark.
> **✅ CHỖ TRỐNG CÒN:** `step_instructions` làm ĐÍCH SINH · đưa tính phân biệt vào MỤC TIÊU huấn luyện trong miền GUI.
> **3 điều kiện để không bị quy về đóng góp DỮ LIỆU:** (1) bảng ablation phải là bảng về MÔ HÌNH (student-không-PI / student-có-PI / teacher-ảnh-sạch / teacher-ảnh-đánh-dấu) · (2) phải **vượt teacher chạy trên ảnh sạch** ở ít nhất một thước · (3) baseline hợp lệ của teacher-có-PI là **cùng mô hình đó trên ảnh trần**. **Rủi ro số 1:** tầng mô tả cần TÊN mà a11y chỉ 12.6% có tên → tầng giữa rác thì hai tầng TỆ HƠN một tầng, phải đo trước. **Việc trước khi khoá framing:** đọc toàn văn 2606.18101 + 2605.00642, nếu có nhánh sinh VĂN BẢN thì khe đóng.
>
> **⏳ QUYẾT ĐỊNH ĐANG CHỜ USER (29/7 chiều) = `report/102_QUYET_DINH_GIA_CO_TRU.md`.** Hai vòng phản biện Fable độc lập (hội đồng khó tính + quét phương án lần cuối) cùng kết luận: GIỮ pipeline nhưng trụ hiện tại KHÔNG gánh nổi vai đóng góp chính (P(S2−S1 vượt MDE) ~20%; GCoT tiền lệ dấu ÂM; loss vẫn là CE thuần = đúng cái mình chê Widget Captioning). **Ba miếng gia cố đề xuất:** (1) toạ độ gold `<point>` vào bộ mô tả — nhãn sạch phủ 100%, chi phí 0; (2) **margin/DPO-descriptor với mô tả giả từ nút hàng xóm** — biến phân-biệt-trong-đích thành phân-biệt-trong-LOSS, lấp đúng khe Widget Captioning; né được lập luận giết DPO cũ (nhắm ambiguity màn hình, không nhắm wrong-neighbor hiếm); khả thi đã đo: 100% bước có hàng xóm, 66% có tên, 45% cùng vai trò; (3) trường phân biệt tính bằng luật + cờ AMBIG (lá chắn đòn thước-thiên-vị-câu-dài). **Thiết kế lực:** ghép cặp từng bước + lát-khó đăng ký trước + chấm đủ 631 ep → P vượt MDE lên ~40-50%. **Đo mới 29/7:** nhãn descriptor dựng được 77% tên rõ / 20% cần caption crop (KHÔNG phải 43% như ước cũ — ghép a11y+OCR-trong-hộp mạnh hơn từng nguồn); ~~UGround SẠCH (không AC trong recipe)~~ ⛔ **RÚT 16/8: SAI** — Bảng 1 arXiv 2410.05243 có AndroidControl 47K (xem khối 16/8 đầu file); GTA1 nghi nhiễm dây chuyền qua OS-Atlas → RL xuống hàng vòng-2. Nhánh mới: S2 (mô tả có point → câu) · S3 (S2+margin, cổng thử tuần 3) · S3r (negative ngẫu nhiên, đối chứng cơ chế). **3 kịch bản phải chốt với thầy TRƯỚC KHI TRAIN** (null / hoà-nhưng-rẻ / B1c thắng) — ghi ở report/102 §7. Code đo: `harness/descriptor_label_pilot.py` · `descriptor_label_results.json`.
>
> **💰 RÀNG BUỘC ĐỔI 29/7 CHIỀU MUỘN (user nói rõ, GHI ĐÈ mọi ràng buộc ngân sách/thời gian cũ):**
> · ⚠️⚠️ **HẠN NỘP = 2 THÁNG (~8 tuần), user xác nhận 29/7.** Câu "không áp lực thời gian" trước đó KHÔNG đúng thực tế — trừ 2-3 tuần viết luận văn + gặp thầy + chuẩn bị bảo vệ thì **phần thực nghiệm chỉ còn ~5-6 tuần**, CHẶT HƠN cả con số "6 tuần" dùng lúc đầu (hồi đó chưa trừ phần viết). **Mọi kế hoạch xây dưới giả định "thời gian thoải mái" PHẢI tính lại** — nhất là hướng giám sát chú ý (rủi ro cài đặt cao nhất: hook nội bộ Qwen2.5-VL, tắt flash-attn chọn lọc, map bbox→visual token qua M-RoPE + merge/pool, dò layer + λ).
> · **Trần 200$ nhưng ƯU TIÊN TIẾT KIỆM** — "tiết kiệm nhất có thể thôi". 200$ là trần, không phải mục tiêu.
> · **Ưu tiên số 1 = ĐỘ MỚI + ĐỘ CHÍNH XÁC** để bảo vệ luận văn. Chấp nhận "cần nhiều máy hơn cũng không sao".
>
> **🔬 VÒNG QUÉT NGÂN SÁCH MỚI (Fable, 29/7) — KẾT QUẢ CHÍNH:**
> · **200$ là THỪA.** Kế hoạch tốt nhất chỉ ~**60-110$**, trần xấu nhất ~150$. Giá tra 29/7: vast.ai A100-80GB **$0.40-0.93/h** (interruptible $0.27-0.40); RunPod A100 $1.39; **Colab Pro+ TỆ NHẤT bảng** (~$1.50/h hiệu dụng, chỉ 33h/gói $50) → **KHÔNG dùng Colab, dùng vast.ai interruptible** (bỏ deadline rồi thì gián đoạn vô hại, chỉ cần checkpoint mỗi 200-500 bước).
> · Chi phí mốc (A100 $0.72/h, Qwen2.5-VL, ~75-85k mẫu-bước, 2 epoch): QLoRA 3B toàn bộ dữ liệu **$13-16** · QLoRA 7B **$29-36** · full-FT 3B $16-20 · 3 seed × 2 nhánh $80-95 · **pilot trên lát 1.697 bước có sẵn = $0.3-2/run (4090 interruptible)** · **chạy UGround-7B chấm toàn bộ 1.543 ep test = $3-6 ← KHOẢN HỜI NHẤT** (hạ MDE mà không cần model tốt hơn).
> · **NÚT THẮT THẬT không phải tiền** mà là (1) công cài đặt/gỡ lỗi, (2) MDE của thước. **Thứ đổi bản chất là BỎ DEADLINE** — cho phép mua độ mới bằng *pilot rẻ* thay vì *canh bạc*.
>
> **⭐ HƯỚNG KIẾN TRÚC MỚI = GIÁM SÁT CHÚ Ý (attention supervision).** Ép attention của token đang sinh dồn vào hộp bbox phần tử đích; nhãn = hộp a11y, **sạch 100%**. Can thiệp CƠ CHẾ NỘI BỘ, không đổi chuỗi output → claim dày hơn hẳn "lược đồ giám sát", khó bị gọi là prompting/data-engineering.
> · **Tiền lệ (đã verify):** **Liu et al. AAAI 2017** (arXiv 1605.09553) "Attention Correctness in Neural Image Captioning" — giám sát attention làm **CHẤT LƯỢNG CAPTION TỐT LÊN**, không chỉ attention đúng hơn. ⭐ **Đây là bằng chứng NGƯỢC CHIỀU với nỗi lo GCoT** (grounding-first làm câu kém đi) — cơ chế khác: GCoT ép sinh thêm bước, attention-sup ép nội bộ. · **arXiv 2511.12738** (KLAL, preprint 11/2025) đã làm attention-sup cho VLM hiện đại **nhưng output là REC/định vị, không phải sinh câu, không GUI** → khe còn: attention-sup bằng bbox a11y khi TRAIN SINH CÂU CHO NGƯỜI trên GUI. · Attention-Driven GUI Grounding (AAAI 2025) = tuning-free, không train.
> · **Cài trên Qwen2.5-VL:** hook 2-4 layer giữa-cuối, tắt flash-attn CHỈ ở layer đó (eager), target map = đều trong bbox / ~0 ngoài, loss KL cộng trọng số λ. Chậm ~1.3-2× → **$20-30/run toàn dữ liệu**.
> · **⭐ ƯU THẾ QUYẾT ĐỊNH: KIỂM RẺ ĐƯỢC.** Có thước trung gian RIÊNG, miễn phí, không đụng bộ chấm = **attention IoU** so với bbox gold. Tách 2 mắt xích kiểm độc lập: (1) "loss có kéo attention vào đúng nút không" → **~$1**; (2) "attention đúng có làm câu phân biệt hơn không" → $2-5. Mọi phương án khác phải train xong mới biết.
> · ⚠️ **KHÔNG có Qwen2.5-VL 0.5B** (nhỏ nhất là 3B; Qwen2-VL có 2B). Đừng đổi họ model để pilot — cơ chế attention không chuyển giao đáng tin giữa các họ.
> · **ĐÃ LOẠI:** đầu phụ heatmap/bbox (GUI-Actor NeurIPS 2025 arXiv 2506.03143 chiếm; phần còn lại là multi-task đổi tên) · adapter riêng cho định vị/viết câu (engineering thuần) · mở vision encoder (siêu tham số, không phải đóng góp).
>
> **📋 CHIẾN LƯỢC CHỐT = C' "pilot rẻ → chỉ scale cái sống".** Giữ trụ mô-tả-trước-phát-ngôn-sau + 2 miếng gia cố (`<point>` + margin-hàng-xóm) làm xương sống; thêm attention-sup làm **mũi nhọn độ mới**, chỉ scale sau khi qua 2 cổng rẻ. **KHÔNG train 7B** trừ khi 3B rớt mốc gpt-4o-mini (nút bấm dự phòng $30). Xác suất ước: P(thắng 2 mốc) ~0.70-0.75 · P(thành phần vượt MDE) **~0.50-0.60** · P(mất trắng) ~0.03.
> **Lộ trình 4 giai đoạn (tiền cộng dồn):** GĐ0 cài + chạy khói 200 mẫu **~$5** (cổng: chạy được cơ học) → GĐ1 thử 4 nhánh trên lát 1.697 bước + quét λ/layer **~$15-25** (cổng: attention IoU tăng rõ VÀ executability không tụt) → GĐ2 scale cái sống lên toàn bộ 15.283 tác vụ + chấm toàn bộ test **~$50-80** (cổng: thắng SFT-trơn) → GĐ3 nhiều seed cho cặp headline **~$90-130**. Rớt cổng nào cũng còn kết quả dùng được (kể cả kết quả âm có kiểm soát về attention-sup).
>
> **📄 FILE QUYẾT ĐỊNH = `report/102_QUYET_DINH_GIA_CO_TRU.md`** (đã viết lại 29/7 cho dễ hiểu: §1 đóng góp là gì · §2 đã làm được gì · §3 vấn đề · §4 ba cách gia cố · §7 quyết định · §8 một trang). ⚠️ **CHƯA thêm phương án attention-sup vào file này** — việc kế tiếp. Và **report/100, 101 chưa khớp với 102** (vẫn theo bản trước gia cố).
>
> **🗂️ ĐÃ DỌN 29/7:** report/ còn 12 file (29 file → `report/_archive/`); harness/ còn 19 script (53 thứ → `harness/_archive/`, gồm toàn bộ khung prompting cũ + 7.6MB emb cache). Slide v5/v6 + 7 build script cũ → `_archive/slides/` và `slides/build/_archive/`. Gộp hết PDF trùng.
>
> **▶️ VIỆC KẾ (thứ tự cứng):** (1) free: đo lại bộ tứ với cây trợ năng thật · khảo sát 91 cặp với NGƯỜI (cần 2 người chấm độc lập, ngưỡng đã khoá) · dựng data dạy + chạy OCR sẵn → (2) **Cổng B: train SFT-trơn TRƯỚC rồi đo** (biết còn bao nhiêu room; hẹp hơn MDE thì kết quả không đọc được) → (3) Cổng A: bộ trỏ chuyên (UGround, KHÔNG OS-Atlas vì nhiễm AC) → (4) gặp thầy → (5) train lớp 1, rồi lớp 2 + 2 đối chứng.
> Khi mâu thuẫn: report/100 + report/98 (bản 29/7) > report/99 > 93/94 > phần dưới.

---

> # ⬇️ TỪ ĐÂY XUỐNG HẾT §0 = LỊCH SỬ (đã bị khối 🧭 trên THAY)
> Chỉ mở khi cần tra "vì sao hồi đó quyết định X". **KHÔNG phải trạng thái hiện tại** — trạng thái hiện tại nằm ở khối 🧭 trên cùng + `report/98`/`report/99`. Mọi "thứ tự đọc mỗi phiên", "việc kế", "đọc đầu tiên" bên dưới đều LỖI THỜI.

> ## 🚨 [LỊCH SỬ] Phản biện đối kháng (2026-07-19)
>
> **Một vòng PHẢN BIỆN ĐỐI KHÁNG (7 giám khảo độc lập bị bịt mắt khỏi file tóm tắt + vòng bác bỏ chéo; 27/39 đòn nặng sống sót) đã LẬT vài kết luận chính. → `report/90_phan_bien_doi_khang.md` (bản đọc được) + `report/90b` (nguyên văn 27 đòn).**
>
> ~~**Thứ tự đọc mỗi phiên: `report/88` → `report/90`.**~~ ⬆️ LỖI THỜI — nay đọc khối 🧭 trên cùng + `report/98`.
>
> **NHỮNG THỨ ĐÃ BỊ RÚT — đừng lặp lại:**
> 1. ⛔ **"metric-gate PASSED / AUC=1.000 / tách (action,target) giải được chỗ K1 chết"** — SAI. Bộ bơm-lỗi dựng nhánh paraphrase bằng cách gọi chính `target_of()` của thước rồi dán lại output (`metric_v1_validate.py:117`) → Jaccard=1 tất yếu; nhánh sai-đích bị ép giao-rỗng token (`:97`) → Jaccard=0 tất yếu. **AUC=1.000 là hằng đẳng thức `P(1.0>0.0)`, phương sai bằng 0; cổng "AUC<0.80 → DỪNG" không có đường kích hoạt.** Đo lại bằng paraphrase THẬT (`filter option`↔`funnel icon`): **kết oan 10/10, AUC=0.35**. Backstop bge-m3 không cứu (`gmail tab`↔`calendar tab` [bịa] 0.717 > `search bar`↔`magnifying glass` [thật] 0.490). Vòng-2 "ca khó" **không có code lẫn JSON** trong repo.
> 2. ⛔ **"MDE 8-9pp @ G=150-250 → đủ lực"** — G đếm từ SAI QUẦN THỂ (`ac_test_200ep.json` = test chung). Trên đúng app_unseen: **41% ep gán được app (không phải 72%), 42 app distinct, tập trung mạnh** (Pinterest 14) chứ không singleton → **MDE thật ≈12.5-14.4pp**. Bộ gán app còn tách 1 app thành nhiều cụm (`The Washington Post` vs `Washington post`) + đẻ cụm rác (`On the Pinerest`) → **G thổi phồng, CI hẹp giả**. Trục TRUNG THỰC (G=12) chưa điền ô MDE, ước **~32pp = thiếu lực**, null sẽ không đọc được gì.
> 3. ⛔ **"model ĐẦU TIÊN sinh hướng dẫn nhiều-bước cho NGƯỜI ĐỌC"** — **GuideMe (CHI 2026, DOI 10.1145/3772318.3791448)** đã chiếm ở mức tác vụ (VLM + screenshot + UI info → hướng dẫn từng bước cho người già). Hạ xuống **"model nhỏ mở đầu tiên được HUẤN LUYỆN cho tác vụ này"**. Bản thảo report/57 sạch (0 hit "first"), overclaim chỉ ở đây.
> 4. ⚠️ **RỦI RO SỐ 1 MỚI — con số headline có thể không diễn giải được:** Student train trên gold AC nói đúng phương ngữ annotator; Teacher zero-shot nói khác nên **bị kết oan có hệ thống** → Δ(Student−Teacher) có thể chỉ đo **khớp giọng**, không đo đúng hơn. Đo được: chỉ đổi lựa chọn bề mặt của thước (gộp tap/open, containment thay Jaccard, bỏ từ chỉ vị trí) làm điểm teacher nhảy **0.286→0.604** mà không đổi chữ nội dung nào. **Bắt buộc thêm nhánh Teacher-STYLE-MATCHED** trước khi train. (Điều này ĐẢO câu cũ "action∧target bớt nhạy phong cách" — token-overlap là thước NHẠY phong cách nhất.)
> 5. ⚠️ **Gold AC không phải "hướng dẫn cho người":** trung vị **6 từ**, 48.9% câu ≤5 từ, 60.4% mở đầu bằng click/tap, **167/842 cặp bước liền nhau trùng y hệt**, có câu hỏng (`Click on the top at the bottom right corner`). Phải chọn: khai thẳng là "sinh mô tả thao tác bằng NL", HOẶC giữ claim "cho người" + thêm tầng viết-lại + eval NGƯỜI.
> 6. ⚠️ Sửa số các kill-test: K1 chạy trên **30 màn/7 app** (không phải 127); K2 trên **80 màn của 1 app**, 40 ca soi tay = **~18 widget distinct**; OCR glyph đếm nhầm substring → đếm lại standalone: `+`=11, `X`=13, mũi tên=**0**, `✓`=**0** ⇒ **OCR không cứu được icon thuần**, bỏ mệnh đề "không cần model dò icon".
>
> **VIỆC KẾ — theo đúng thứ tự, A→D đều FREE, KHÔNG train trước khi xong:**
> **A** dừng overclaim (✅ ĐÃ LÀM 19/7: vá report/84/85/88 + 73/74/75 + file này) → **B** ✅ **ĐÃ CHẠY 19/7 (report/92) → THƯỚC RỚT CỔNG THẬT, AUC=0.336** trên 51 ca thật viết tay (v1 rỗng vì hằng đẳng thức; v2 `harness/metric_v2*.py` vá xong lỗi cơ học vẫn rớt). Lý do BẢN CHẤT: embedding đo gần-chủ-đề nên đặt `inbox↔outbox`=0.76 CAO HƠN `search↔magnifying glass`=0.55 → **không ngưỡng nào tách cùng-nút khỏi khác-nút**. Từ-điển-ký-hiệu kéo lên 0.735 (vẫn <0.80, số lạc quan vì dict overlap test). **⇒ CỔNG RỚT — KHÔNG train cho tới khi thầy quyết 1 trong 3 đường: (1) từ-điển chuẩn hoá dựng độc lập + held-out; (2) đổi thước chính (LLM-judge/grounding); (3) thu hẹp → đẩy trọng tâm sang chương đo-lường.** → **C** construct-validity với NGƯỜI (**bộ chấm đã dựng sẵn: `harness/cv_study/rate_A.html` + `rate_B.html`, 91 cặp teacher, free; phân tích: `harness/cv_analyze.py`** — CÀNG NÊN CHẠY: xác nhận người có coi icon↔tên là "cùng nút" không) → **D** gán app lại cho 631 ep + tính lại G/MDE cả hai trục → **E** GẶP THẦY (mang: thước rớt + 3 đường + framing sau GuideMe) → **F** mới train.
>
> ⚠️ **SCOOP 19/7 (report/92, deep-research verify DOI): vòng cũ (report/82) BỎ SÓT hai bài CHI 2026.** **GuideMe (CHI 2026, 10.1145/3772318.3791448)** làm đúng tác vụ "người cao tuổi hỏi trong app → VLM sinh hướng dẫn từng bước cho người" → **giết claim "tác vụ mới/đầu tiên"** (nhưng nó KHÔNG train model, KHÔNG benchmark, KHÔNG dùng AC → phần model + đánh giá định lượng của ta còn sống). **AskEase (CHI 2026, 10.1145/3772318.3790661)** = desktop screen-reader, lân cận. Đóng góp 1+2 (người-đọc, nhiều-bước) CHẾT như tính-mới độc l*; đóng góp 3 (reference-free VH) + 4 (AC làm đích sinh) SỐNG. **Trục tính-mới = tổ hợp: model nhỏ mở ĐƯỢC-TRAIN + tái lập được × AC-làm-đích × eval-VH-có-cổng-bơm-lỗi.** Việc hở: **lấy PDF GuideMe (ACM chặn 403) TRƯỚC khi khoá framing với thầy** — câu "GuideMe không train" mới là suy đoán.
> **Quyết NGAY tuần này (không đợi E): bỏ hay giữ FAIR 15/8** — 27 ngày, chưa có dòng code train nào, AC train-split chưa tải, abstract FAIR trong KE_HOACH vẫn đang bán đóng góp lọc-bịa ĐÃ CHẾT từ 18/7.
>
> ⚠️ **Mọi dòng §0 bên dưới viết TRƯỚC 19/7 — chỗ nào mâu thuẫn với khối này thì khối này thắng.**

> ## ⚡ [LỊCH SỬ — không còn dùng] điều hướng cũ (mọi con trỏ dưới đây LỖI THỜI: report/88/00/71/72/85 là bối cảnh cũ; trạng thái hiện tại = khối 🧭 đầu file + report/98)
>
> **⚠️ FILE ĐÃ DỌN GỌN 19/7:** report/ giờ chỉ còn bộ hướng LAI đang dùng; khung prompting cũ (00-52) + chuỗi pre-LAI (61-68) + các bản tóm tắt cũ (00/70/71/72/77/80/83) + slide v1-v4 đã dời sang `report/_archive/` (khôi phục được). **Nhiều con trỏ file trong CLAUDE.md phía dưới nay trỏ vào file đã archive — nếu không thấy trong report/, tìm ở report/_archive/.**
>
> **Nguồn-sự-thật TRẠNG THÁI HIỆN TẠI = `report/88_TOAN_CANH_CHI_TIET.md`** — đọc file đó ĐẦU TIÊN mỗi phiên (toàn cảnh chi tiết: đề tài · câu chuyện đổi hướng · 4 phép thử · thiết kế LAI cuối · kế hoạch dựng-data + train · việc tiếp theo · bản đồ file). Kèm: `report/_archive/85` (đăng-ký-trước, đã commit) · `report/89` (review slide + câu thủ) · `LUAN_VAN_SLIDE_v5.pptx` (slide trình thầy). *(report/00 cũ đã archive.)* File CLAUDE.md này = **nhật ký quyết định**, dòng §0 dưới cùng = mới nhất.
>
> **1 dòng trạng thái (2026-07-18):** hướng đã chốt = **"Faithful Distillation"** (train Qwen2.5-VL-3B, SFT-LoRA, chỉ một-màn). **Split 18/12 ĐÃ commit (`3776212`); pool train 498 màn/220 app, K-leak sạch.** ⛔ *report/85 (thay 56) đã bị VÁ 19/7 — cổng thước không hợp lệ, G/MDE tính sai; xem khối 🚨 trên.* **PIPELINE CUỐI ĐÃ CHỐT = `report/71`:** giữ nguyên xương sống + THÊM "trục ĐÚNG" (Step-SR-theo-tên trên AndroidControl, map gold(x,y)→a11y-tree→tên nút) ở **vai phụ + hậu-đăng-ký + phải hỏi thầy**; ưu tiên **B (đọc tay fallback) > A (thêm app test) > trục ĐÚNG thu gọn > C (bịa nhiều teacher)**; 2 vá nhỏ pipeline = OCR-ở-bước-lọc + 10-câu-fallback. **PLAN dán-thẳng-chat-mới = `report/72`.** 3 vòng nâng cấp A/B/C đã chạy 18/7 → `report/66/67/68`. → **Việc kế = VIỆC 0 (K1 kill-test matcher, free) → VIỆC 1 (đọc tay fallback) → VIỆC 2 (pilot MDE + đo bịa teacher mới, ✱$1-2) → HỎI THẦY → mới sang train.** Nộp 2 bài: **FAIR** (15/8, tiếng Anh, model) + **VCL** (30/8, tiếng Việt, sinh-tiếng-Việt).
>
> **⚠️ K1 ĐÃ CHẠY 18/7 (`report/73`, code `harness/k1_matcher_killtest.py`): bộ đối chiếu embedding-đơn RỚT.** Ở τ=0.55: bỏ lọt 47,5% bịa gần-nghĩa + kết oan 47,5% paraphrase (κ=0,38); phân bố paraphrase-thật vs bịa-gần-nghĩa **chồng lấn 40/40 → không τ nào tách được**. bge-m3 đỡ chút, không giải quyết (⇒ OpenAI cũng vậy). So-chuỗi thuần bắt bịa gần-nghĩa (5% bỏ lọt) nhưng giết paraphrase khác-ngôn-ngữ (97,5% kết oan) → **hai chiều lỗi do 2 cơ chế ngược** ⇒ **phải nâng trọng tài đa-tín-hiệu (so-chuỗi + embedding + OCR), KHÔNG chỉ bơm τ = sửa PIPELINE.** VH coverage 62,4% (37,6% nút icon-only → OCR). Với VCL: cân nhắc hướng dẫn GIỮ tên nút hiển thị thay vì dịch.
>
> **⚠️ K2 ĐÃ CHẠY 18/7 (`report/74`, code `harness/k2_hallucination_types.py`, FREE trên 80 output teacher cache): LẬT NGƯỢC lo của K1.** 127 bước teacher thật: verbatim 68,5%; 40 ca không-verbatim soi tay = **0 ca bịa-gần-nghĩa**, mà 35/40 là **NÚT THẬT bị VH bỏ nhãn** (icon `+`/`✓`/mũi tên 20 · field mô tả 11 · chữ-hoa ADD/EXPENSES 4) + 3 artifact `<...>`. → **(1) lỗi thật = KẾT OAN (đánh oan nút thật), KHÔNG phải bỏ lọt → OCR/nhận-icon là FIX SỐ 1** (20/40 là icon); **(2) bộ lọc hiện tại có nguy cơ LÀM HẠI data** (viết-lại nút thật thành mô tả mơ hồ) → phải sửa matcher TRƯỚC build data; **(3) gpt-4o-mini bịa RẤT ÍT (~0-2%), con số "~¼ bịa" cũ nhiều khả năng là kết-oan đọc nhầm → nghi ngờ 5 thành hiện thực: ít bịa thì Tier 1 dễ null tầm thường.** Phải mang K1+K2 lên gặp thầy: sửa trọng tài (OCR) + có thể chỉnh khung đóng góp.
>
> **⚠️ VIỆC OCR ĐÃ CHẠY 18/7 (`report/75`, code `harness/ocr_vh_coverage.py`, RapidOCR ONNX/CPU/free trên 127 màn): OCR giúp KHIÊM TỐN, không đủ một mình.** Độ phủ nhãn nút-cỡ-nút +6 điểm (74→80%; thô +11 micro/+16 macro nhưng ~28% là rác chữ-hiển-thị); khung toạ độ khớp. Cứu được nhãn text (OK/Search/X/tab) NHƯNG **không cứu icon thuần** (`+`/`✓`/mũi tên = 20/40 ca kết-oan K2). → **trọng tài lành mạnh = đa tầng: so-chuỗi → VH → OCR-chặt → TỪ-ĐIỂN-KÝ-HIỆU (+→add, ✓→confirm, ✕→close...) → fallback.** Từ-điển-icon rẻ/tất định, cứu đúng phần OCR chịu thua. **Ba kill-test K1/K2/OCR = `report/73/74/75`.**
>
> **⚠️ VIỆC 1 (đọc tay fallback) ĐÃ CHẠY 18/7 (`report/76`, 127 câu fallback thật): giả định "mô tả chung chung dùng được" ĐỨNG NỬA VỜI.** 0/127 rơi câu-trơ (tốt), nhưng ~80% chỉ LẶP LẠI MỤC TIÊU (không chỉ vị trí/hình), 20% lặp động từ sượng ("Tap...let you tap"). Cộng K2 (fallback thay NÚT THẬT) → fallback thường làm hướng dẫn TỆ ĐI. Fix hiệu quả nhất = fallback ÍT ĐI (nâng matcher), không phải viết câu hay hơn. **→ 4 kill-test free XONG (K1/K2/OCR/VIỆC1 = report/73-76), gói lại thành hồ sơ gặp thầy `report/77`.** Điểm quyết định lớn nhất: **nghi ngờ 5 (teacher bịa ~0-2%, không phải ¼) → tiền đề "lọc bỏ bịa" lung lay, có thể phải chỉnh khung đóng góp.** Việc kế = GẶP THẦY trước, rồi mới pilot MDE/build (đừng đổ tiền train trước khi chốt khung với thầy).
>
> **⚠️ CHỐT NHÁNH 18/7 (`report/78`, debate A-vs-B 5 agent): chọn LAI, NÂNG CẤP report/71.** Trục ĐÚNG (Step-SR-theo-tên trên AndroidControl, TỪNG-BƯỚC-NHƯ-MỘT-MÀN, vẫn MỘT MÀN — KHÔNG phải nhánh nhiều-màn) **LÊN TRỤ CHÍNH**; Tier 1 (LỌC vs THÔ) **xuống readout phụ gần-miễn-phí** (vì K2: teacher bịa ~0 → Tier 1 dễ null tầm thường); K1/K2/OCR/VIỆC1 gói thành **chương đóng-góp đo-lường**. **Xử confound lệch-miền = đóng khung SO SÁNH CẶP (difference-in-differences):** chấm Student-LỌC/Student-THÔ/Teacher-BASE trên CÙNG lát AndroidControl → lệch-miền triệt tiêu trong hiệu-số; estimand = hiệu-cặp, KHÔNG phải Step-SR tuyệt đối. **HAI khe hở chưa dập:** (a) giả định "lệch tác động đồng đều mọi nhánh" không test được (MobileViews không gold); (b) **construct-validity**: Step-SR đo thao-tác-agent, đề tài là hướng-dẫn-cho-NGƯỜI → cần nghiên-cứu-nhỏ đối chiếu "khớp-gold" vs "người-chấm-đúng" vài chục mẫu. **Tính mới KHÔNG phải "3B on-device" (ZonUI/UI-R1/LLaVA-KD đã chiếm) mà là "sinh HƯỚNG DẪN nhiều-bước cho NGƯỜI + đánh giá KÉP no-gold(VH)+gold(Step-SR)".** **CỔNG SỐNG-CHẾT trước khi cam kết: pilot AndroidControl ~10-20 bước — Step-SR không suy biến sàn-0 + tỉ lệ map gold→a11y→tên đủ cao (thừa hưởng đúng bệnh VH-thiếu-nhãn ~20% icon). Hỏng → rơi về "nghiên cứu đo-lường + A-mô-tả".** Thứ tự: pilot AndroidControl (go/no-go) → gặp thầy → khoá report/56+71 → build.
>
> **⚠️ PILOT AndroidControl ĐÃ CHẠY 18/7 đêm (`report/79`, code `harness/pilot_androidcontrol.py`, tự chủ): GO — nhưng ĐỔI CƠ CHẾ trục ĐÚNG.** (1) Khung toạ độ gold↔ảnh KHỚP SẠCH (ảnh 1080×2400 & 1440×3120, gold=pixel; "Search"/"Next"/"+" trúng điểm) → giải toả rủi ro #1 report/71. (2) Cách report/78 giả định (map gold(x,y)→a11y→TÊN nút) YẾU: chỉ 40% (OCR-tại-điểm, cận dưới) / 52% relaxed vì **~48% gold-click nhắm ICON/ẢNH không chữ**; **a11y-tree KHÔNG có ở mirror HF** (chỉ GCS gốc, cần tensorflow+GB). (3) **PHÁT HIỆN THEN CHỐT: AndroidControl có gold `step_instructions` (hướng-dẫn NGƯỜI viết từng bước, đã công bố NeurIPS24)** → **đổi trục ĐÚNG sang so hướng-dẫn-model ↔ gold-step-instruction (văn bản)**: phủ ~100% bước, KHÔNG cần a11y, **gỡ khe construct-validity lớn nhất của report/78** (người↔người). Giữ point-in-bbox grounding làm phụ. Giữ difference-in-differences (student vs teacher trên CÙNG lát AC) + pre-register lát gần-miền. **CHƯA test: Step-SR THỰC (cần model sinh — bước sau); metric so-instruction cần định nghĩa + bơm-lỗi-validate + luật align đa-bước↔đơn-bước.** Việc kế: tải AC-test local → thiết kế+validate metric so-instruction → nghiên-cứu-nhỏ construct-validity → gặp thầy (report/78+79) → generate → đo hiệu-cặp.
>
> **⚠️ CHỐT THIẾT KẾ CUỐI 19/7 (`report/81`, debate 5 agent — user TỰ CHỐT đi LAI, không đợi thầy): LẬT một điểm lớn so report/78.** **Train:** một model, tín hiệu CHÍNH = **gold `step_instructions` của AndroidControl**; MobileViews-distilled = data AUX (ablation bật/tắt, KHÔNG bỏ). **Đo trục ĐÚNG (chính) ngay trên app-unseen split của CHÍNH AndroidControl (IN-DISTRIBUTION held-out, KHÔNG cross-dataset)** — cắt khung difference-in-differences của report/78 vì confound parallel-trends không kiểm định được. Trục TRUNG THỰC (phụ) = student bịa? trên MobileViews (Tier 2, tắt VH). ScreenSpot phụ. **Metric = 3 lớp:** tách mỗi bước thành (action, target) [vá đúng bẫy K1 — "Gmail tab" vs "Calendar tab" là mismatch cứng dù embedding gần]; gióng bằng phủ-tập; headline = coverage-recall target-khớp-CÓ-ĐIỀU-KIỆN-action-đúng + F1 + order-τ partial (Fagin, KHÔNG Kendall τ-b); LLM-judge khác-họ chỉ cross-check. **Validate metric = bơm-lỗi LÀM CỔNG** (pre-register ngưỡng; mấu chốt: tách-phân-phối AUC≥0.80 — chính chỗ K1 chết; rớt → dừng, sửa thước, KHÔNG train). **KHÔNG bỏ MobileViews, KHÔNG cần dataset mới** (nâng cấp tuỳ chọn: tải AC-full nặng có a11y-tree để gom 2 trục cùng màn — phải đếm label-coverage trước). **⚠️ RỦI RO SỐ 1 (report tự khai, không dập bằng số): TÍNH MỚI MỎNG** — train-trên-gold đẩy về gần supervised (SeeClick/UI-R1/Aguvis); K2 đã GIẾT đóng góp lọc-bịa, đừng giả vờ nó sống. Tính mới dời sang: output-type=hướng-dẫn-cho-NGƯỜI + dual-eval(gold+no-gold) + chương đo-lường K1-K2-OCR-VIỆC1. **Cần verify chưa bị scoop + hỏi thầy về framing.** report/56 pre-register PHẢI đối chiếu+commit lại TRƯỚC train. Việc free trước: đối chiếu report/56 · tải AC-test local · build+bơm-lỗi-validate metric (CỔNG) · mini-study construct-validity.
>
> **⚠️ VERIFY TÍNH-MỚI CHỐNG SCOOP 19/7 (`report/82`, deep-research 4 agent): LẤP MỘT PHẦN — seam CÒN TRỐNG ở tổ hợp trọn gói, HẸP.** Không bài nào phủ đủ 4 thành phần: người-đọc-là-NGƯỜI + hướng-dẫn-nhiều-bước-theo-câu-hỏi + đánh-giá-KÉP(reference-free-VH + gold) + VLM-nhỏ-on-device. **TÍNH MỚI PHÒNG-THỦ-ĐƯỢC (đặt làm trục):** (1) reference-free dùng nguồn NGOÀI có cấu trúc (VH) bắt bịa, KHÔNG self-probe — phân định sạch với FaithScore/ALOHa; (2) **AndroidControl step_instruction làm TARGET SINH** (không phải input) — chưa ai làm, mọi bài dùng AC đều để instruction ở INPUT cho action-prediction; (3) tổ hợp 4 thành phần. **KHÔNG ĐƯỢC CLAIM (sẽ bị đập):** "dual-eval là phát kiến" (hybrid-metric RUBER/BLEURT/BARTScore đã có), "sinh hướng-dẫn-GUI-cho-người là mới hoàn toàn" (CHI2023 Wang + GUITrans2Act phải phân định), "small on-device VLM" làm trục chính (yếu nhất → hạ xuống đặc-tính-triển-khai). **Bài phải phân định:** GUITrans2Act (arXiv 2606.12817 preprint — video-input, TQ, agent teach-repeat, không AC), CHI2023 Wang (QA/summ không multi-step how-to), FaithScore (self-probe). **CHƯA đọc full-text GUITrans2Act/HalluClear/TIST2022 + chưa quét CHI/UIST/venue-TQ → phải làm trước khi viết related-work.** Framing chốt để hỏi thầy: trục tính-mới = đánh-giá-kép-VH + AC-as-generation-target; cân đối "đóng góp model" vs "đóng góp đánh giá".
>
> **⚠️ CHỐT 19/7 (user khẳng định lại): LUẬN VĂN NHẤT ĐỊNH PHẢI CÓ ĐÓNG GÓP MODEL — model là một TRỤ, KHÔNG hạ xuống "vật thí nghiệm/nền".** (Có lúc trợ lý hiểu nhầm user nới ràng buộc này — KHÔNG, ràng buộc train-model vẫn CỨNG.) Hoà giải với report/82: đóng góp model KHÔNG dựa vào "VLM 3B nhỏ on-device" (đông: ZonUI/UI-R1/LLaVA-KD) mà dựa vào **TÁC VỤ MỚI = model đầu tiên SINH HƯỚNG DẪN NHIỀU BƯỚC CHO NGƯỜI ĐỌC từ 1 ảnh+câu hỏi** (mọi model GUI khác sinh action-cho-máy) — chính là seam report/82 xác nhận còn trống. → **HAI đóng góp NGANG nhau: (1) MODEL (tác vụ mới) + (2) ĐÁNH GIÁ (cặp thước VH-faithfulness + gold-correctness + phát hiện đo-lường 4 kill-test).** "on-device 3B" = đặc-tính-triển-khai, KHÔNG phải trục tính-mới. Thiết kế report/81 KHÔNG đổi, chỉ chốt cách kể model.
>
> **⚠️ THỰC THI 4 VIỆC FREE 19/7 (tuần tự):** **(2) ✅ tải AndroidControl-test local** — 200 ep/1042 step-instruction (`dataset_samples/androidcontrol_test/ac_test_200ep.json`; repo có 1543 ep). **(3) ⛔ BUILD + BƠM-LỖI-VALIDATE THƯỚC — ~~CỔNG QUA~~ CỔNG KHÔNG HỢP LỆ (vá 19/7)** (`report/84`, code `harness/metric_v1_validate.py`): tách bước thành (action, target), khớp target = chồng-từ-nội-dung + bge-m3 backstop 0.85. ~~AUC=1.000~~ ⛔ **hằng đẳng thức, không phải phép đo; ca thật cho AUC=0.35, kết oan 10/10.** Câu "tách (action,target) giải được đúng chỗ K1 chết" ĐÃ BỊ RÚT. detection 1.0, FP 0.0, bge cứu-nhầm-ca-khó chỉ 5%. Hoài nghi còn: paraphrase-synonym có thể kết-oan (chỉnh backstop khi có output model); parser trích còn thô (validate bộ-trích khi có output). **(1) ✅ viết bản đăng-ký-trước MỚI `report/_archive/85` (thay report/56 v1, giữ 56 làm bản ghi)** — trục ĐÚNG chính (coverage action∧target trên AC app-unseen in-distribution, Student vs Teacher-BASE) + trung thực phụ (MobileViews Tier2) + ngưỡng bơm-lỗi đóng băng + 3 kết cục. **(4) ⏸ construct-validity NGƯỜI = HOÃN** (cần output model thật, chưa train). **→ Xong khâu FREE cốt lõi.** **[số app + lát ✅ chốt vào report/85 19/7]:** test set = **app_unseen split CHÍNH THỨC 631 ep** (reece124); app CỰC đa dạng (~114 distinct/200 ep, phần lớn singleton → G lớn ~150-250) → **trục ĐÚNG dùng wild-cluster bootstrap, KHÔNG exact sign-flip; trục TRUNG THỰC (MV G=12) giữ exact sign-flip**. **BỎ "lát gần-miền"** (hedge cross-dataset, nay in-distribution nên vô nghĩa + tránh cherry-pick). Gán app = open_app+trích-goal (~72%). **[MDE ✅ 19/7 — `report/86`, code `harness/mde_pilot.py`, ✱ đã tốn ~$0.5 gpt-4o-mini vision]:** đo teacher trên ảnh thật AC app-unseen (26 app, ~85 bước): **teacher điểm-đúng = 30% → KHÔNG suy biến sàn-0** (phần này VẪN ĐỨNG); ~~MDE ≈ 8-9 pp @ G=150-200 → đủ lực~~ ⛔ **G đếm sai file → MDE thật ≈12.5-14.4pp** (vẫn dưới ngưỡng nhưng SÁT). Ngưỡng 15-20pp vốn là cơ chế chữa cháy của trục MobileViews, trục ĐÚNG phải có ngưỡng riêng. Hướng hiệu ứng kỳ vọng DƯƠNG (student train-trên-AC-gold có lợi-thế-sân-nhà vs teacher zero-shot). Giới hạn khai: thước per-bước nghiêm (nhiều-bước-hợp-lệ, gold ghi một) → 30% là cận-dưới, headline coverage-episode cao hơn. ⛔ ~~report/85 giờ ĐỦ ĐIỀU KIỆN COMMIT~~ — **KHÔNG đủ điều kiện; đã ra bản-vá-1 ngày 19/7, phải sửa V1-V4 rồi commit lại** (chỉ còn chốt số-app-chính-xác + [MDE trung thực MV] lúc build). ⛔ **Việc kế ĐÃ ĐỔI → xem khối 🚨 đầu file: A→B→C→D→E rồi mới train.** Tóm gần đây: `report/83`; kết quả free-prep: `report/84/85/86`.
>
> **Thứ tự đọc khi cần đào sâu:** `report/00` (đầu tiên) → **`report/70` (TẤT-CẢ-TRONG-MỘT dễ hiểu, có PDF)** hoặc `report/54` (bản kỹ thuật tự-đủ) → **`report/71` (PIPELINE CUỐI đã chốt + plan gốc)** + **`report/72` (PLAN dán-chat-mới)** → `report/56` (ngưỡng đã khoá) → `report/65` (6 nghi ngờ) · `report/63` (vòng nâng cấp) → `report/KE_HOACH_2_BAI_BAO.md` (2 bài) → `report/53` (khi bắt tay code). Kết quả 3 vòng: `report/66/67/68`. Nền: `report/61`+`62`+`64`. Log gốc `report/50/52/55/43/44/48` chỉ mở khi tra "vì sao quyết định X".
>
> **⚠️ "7 vòng debate là ĐỦ, chỉ còn THỰC THI" — câu này viết 12/7, nay đã lỗi thời.** Vòng 16-17/7 tìm được nghi ngờ thật (matcher). Nhưng cách xử vẫn là **kill-test free chạy trước**, KHÔNG mở deep-research/debate mới trước khi K1/K2 có số.
>
> **⚠️ BỘ THÍ NGHIỆM — ĐỪNG DÙNG NHẦM:** bộ thật của khung model = **TN0–TN7 (Tier 1/Tier 2)** ở `report/54` mục "Bộ thí nghiệm đầy đủ" (nguồn gốc: `report/53` §5 + `report/56`). Bộ **E1–E16** ở `report/43` Ch.13 + `report/47` là của **khung prompting CŨ ĐÃ BỊ THẦY BÁC** — chỉ còn nhóm validate-thước-đo (E4–E7) được tái dùng, đã gộp vào TN5/TN6. `report/43:1211` trỏ "M1–M5 ở Chương 0 §0.10" là **CON TRỎ HỎNG** (§0.10 giờ là "Rủi ro"; bảng M1–M5 ở `43:305` thuộc phụ lục RLVR đã bị bác) — đừng đi theo.
>
> **⚠️ NHÁNH ĐA-MÀN (DG2) = NGOÀI PHẠM VI MÙA NÀY** — đã thiết kế xong + có trụ bình duyệt đủ 6 thành phần, nhưng treo trên cổng K-pair chưa chạy → để dành bài mở rộng. `report/54` có mục riêng dán cờ 🚩 để thủ khi thầy hỏi, KHÔNG xin duyệt chạy.
>
> **Nếu §0 (dưới) mâu thuẫn với `report/00`/`report/54` → hai file report thắng** (mới hơn). Các mục §1–§6 khung prompting cũ đã bị §0 đè — chỉ giữ để tham chiếu kỹ thuật.

> Auto-load khi làm việc trong `D:\Master\Thesis`. Trao đổi với user bằng **tiếng Việt**.
> Nội bộ gọi tắt **DG1 = một màn**, **DG2 = nhiều màn**; nhưng **trong SLIDE/thuyết trình phải nói "một màn / nhiều màn", KHÔNG dùng chữ "DG1/DG2"**.

---

## 0. ⚠️ BƯỚC NGOẶT 2026-07-08 — ĐỌC TRƯỚC TIÊN (đè lên khung cũ §2–§4 khi mâu thuẫn)

> **📍 FILE TỔNG HỢP MỚI NHẤT (2026-07-12): `report/00_TONG_HOP_TAT_CA.md`** — gộp trọn context (đề tài · model · 2 bài FAIR/VCL · lịch/chi phí · trạng thái · việc tiếp theo · bản đồ file) vào 1 file, đọc-đầu-tiên. Các bullet §0 dưới là log quyết định chi tiết theo thời gian; file 00 là ảnh chụp gọn tại 2026-07-12.

- **Thầy BÁC khung hiện tại** vì *"chủ yếu prompting (gpt-4o-mini API + so embedding), chưa thấy MODEL đâu"*. Yêu cầu cứng của thạc sĩ trường: **luận văn PHẢI có một MÔ HÌNH do học viên HUẤN LUYỆN**, không chỉ ghép công cụ qua prompting. Thầy góp ý: pipeline vẽ từng-bước-nhỏ · mỗi bước gắn một model · mục tiêu = tạo ra model.
- **ĐÃ CHỐT hướng (2026-07-09, sau 3 DEBATE + 2 deep-research):** **"FAITHFUL DISTILLATION"** — fine-tune (**SFT-LoRA, KHÔNG RL**) một VLM nhỏ **Qwen2.5-VL-3B** làm bộ **SINH hướng dẫn**, chưng cất từ teacher gpt-4o-mini nhưng **chỉ trên dữ liệu ĐÃ LỌC BỊA** (qua lớp trung-thực-hoá). Đóng góp = **quy trình lọc-faithfulness tạo data + model on-device** (KHÔNG phải "distillation" trần). **Đo bằng %fallback↓/hữu-ích + robust-khi-không-VH** (KHÔNG đo faithfulness-sau-hậu-kiểm vì bão hoà); chống vòng lặp (lọc `nomic` ≠ chấm `bge-m3`+judge+người), held-out theo APP, paired design. Ràng buộc user: **model=đóng góp chính, eval no-gold=chương phụ, <3 tháng, cắt nhiều-màn khỏi train**. → **Kiến trúc đầy đủ + trụ citation: `report/43` CHƯƠNG 0** (đã viết lại 2026-07-09); chi tiết debate + 8 điều kiện: `report/50` §9. **ĐÃ BỊ BÁC (đừng làm lại):** grounding-RLVR (§7), generator-RLVR + classifier (§8). Trụ bình-duyệt: VGA (EMNLP24), KnowAda (NAACL25), BLIP-CapFilt (ICML22), ALLaVA, LLaVA-KD (ICCV25), VLsI (CVPR25), Mind-the-Gap (ICLR25). FEWL = **preprint bổ trợ** (chưa xác nhận venue bình duyệt — verify 2026-07-12, đừng xếp chung hàng "trụ bình-duyệt" ở trên).
- **KHÔNG làm lại từ đầu:** 3 dataset + bộ thước đo no-gold + literature **GIỮ NGUYÊN** (tái dùng để train/đo model). Chỉ đổi **TRỤC trình bày** (pipeline-prompting → train-model). Mục tiêu mới ~ *"Xây dựng mô hình sinh hướng dẫn GUI bám-màn"*.
- **Compute:** user sẽ **mua Colab Pro** (đủ LoRA/QLoRA 3B-7B; KHÔNG đủ train from-scratch lớn).
- **⚠️ 2026-07-09 DEBATE VÒNG 4 (tính-mới) XONG** (`wf_0dda570e-48a`) → **`report/52_debate_tinh_moi_faithful_distillation.md`**: pipeline SỐNG nhưng **KHÔNG được nói "quy trình lọc-faithfulness MỚI"** (đã có STaR/KnowAda/CapFilt/VGA). Tính mới thu hẹp về **2 điểm**: (a) lọc bằng nguồn NGOÀI có cấu trúc (VH, không self-probe) cho hành vi rủi-ro-cao; (b) **TRỤ THỰC NGHIỆM SỐ MỘT = faithfulness khi TẮT VH lúc suy luận** (held-out theo app, có thể null thật — đây là nơi quyết định sống-chết của luận văn, phải pre-register ngưỡng trước pilot). Ablation raw-vs-filtered chỉ là điều-kiện-cần, KHÔNG phải trụ. Phải thêm citation: STaR (Zelikman 2022), FaithDial/BEGIN (Dziri TACL22), WinDOM/Trust-the-Right-Teacher/LiteGUI/CORA (dòng GUI-agent 2026). report/43 Chương 0 đã vá theo hướng này.
- **📌 FILE ĐỌC-HIỂU-TRỌN-PIPELINE — TỰ THÂN ĐẦY ĐỦ, KHÔNG CẦN MỞ FILE KHÁC (2026-07-12):** **`report/54_PIPELINE_FINAL_DOC_HIEU_TOAN_BO.md`** — gộp TOÀN BỘ nội dung từ report/50/52/53/55 vào một file: Phần 1 = giọng người-thường dễ hiểu (bối cảnh, ý tưởng, tính mới, đủ-ngưỡng-thạc-sĩ, rủi ro); Phần 2 = phụ lục kỹ thuật đầy đủ (config YAML, data schema, công thức thống kê, 11 rủi ro kỹ thuật, bảng so sánh precedent, lịch sử quyết định). report/43/50/52/53/55 giữ lại làm log gốc, KHÔNG cần đọc nữa — mọi cập nhật nội dung từ nay ưu tiên sửa thẳng vào report/54. **7 vòng debate coi như ĐỦ** — việc còn lại là THỰC THI (pilot hạ tầng + gặp thầy), không phải research thêm.
- **⚠️ 2026-07-12 AUDIT ĐỘ VỮNG PIPELINE (Fable 5, đối chiếu 64 quyết định + xác minh citation/thống kê qua web):** verdict **CẦN-VÁ → ĐÃ VÁ cùng ngày**. Thiết kế đứng vững (60/64 quyết định khớp nhất quán report/50→54, không bị nghiên cứu 2025-2026 nào scoop), nhưng phát hiện 6 lỗ tài liệu/pre-registration đã vá thẳng vào `report/54` (Phụ lục E chủ yếu) + `report/53` §5.2/§5.6: (1) định nghĩa "đủ lớn" (Δ_train) ở Tier 2 từng mâu thuẫn giữa 2 file — giờ CHỈ CÒN một định nghĩa (đo trên 18 train-apps, cùng điều kiện tắt-VH như Tier 2); (2) Tier 1 giờ có ngưỡng đậu/rớt bằng số (trước chỉ định tính); (3) công thức MDE thêm vế cận-trên thận trọng + phương án dự phòng 15/15; (4) thêm bước dedup perceptual-hash (phòng 2 app khác tên cùng template UI); (5) **UI-R1 = AAAI 2026, KHÔNG PHẢI AAAI 2025** (đã sửa ở dòng trên + report/50) — bài được AAAI chính thức chấp nhận cho kỳ 2026, hội nghị họp 1/2026; (6) khoá thứ tự thực thi (freeze split + commit pre-reg TRƯỚC bất kỳ lệnh gọi API/GPU nào, kể cả pilot). **KHÔNG có lỗi thiết kế nào phải làm lại** — chỉ vá tài liệu, tuần 1 vẫn bắt đầu bằng `dg3_freeze_split.py` như kế hoạch.
- **⚠️ 2026-07-10 DEBATE VÒNG 5 (đủ-ngưỡng-thạc-sĩ + build-plan) XONG** (`wf_a4401c9d-f93`) → **`report/53_ke_hoach_build_model.md`**: verdict **ĐỦ-CÓ-ĐIỀU-KIỆN** (chuẩn thạc sĩ KHÔNG đòi SOTA, chấp nhận đóng góp constructive/technological — Rutgers/Auckland/UIC + Thông tư 23/2021/TT-BGDĐT). **Điều kiện bắt buộc: TÁCH 2 TẦNG thực nghiệm** — Tier 1 (Student-lọc vs Student-RAW, VH vẫn có lúc suy luận, gần chắc dương = lưới an toàn) và Tier 2 (Student vs Teacher-BASE, TẮT VH lúc suy luận = trụ chính, có thể null). Báo cáo ĐỘC LẬP để null ở Tier 2 không kéo sập Tier 1. Kế hoạch build CỤ THỂ (framework LLaMA-Factory, QLoRA r=8/alpha=16 freeze-vision, split app 18/12, exact sign-flip test G=12, ngưỡng đậu/rớt pre-register) đã chốt trong report/53, kèm 11 rủi ro kỹ thuật đã rà + cách né. Việc bắt buộc trước khi chốt với thầy: pilot hạ tầng 5-10 app + nói trước khả năng null Tier 2.
- **Deep-research XONG** (`wf_ed61af89`, verify 20/25 claim) → **`report/50_deepresearch_model_centric.md`** (bản chốt: xếp hạng + khuyến nghị + chi phí). **Trụ bình duyệt neo hướng mới:** UI-R1 (arXiv 2503.21620, chấp nhận **AAAI 2026** — KHÔNG PHẢI AAAI 2025, sửa 2026-07-12; reward point-in-bbox, 136 mẫu) · SE-GUI (NeurIPS 2025) · GUI-Actor (NeurIPS 2025) · ZonUI/Qwen-GUI-3B (WACV 2026, LoRA 3B trên 1 GPU 24GB). Còn lại = preprint (verify ID trước khi trích). **Compute:** Colab Pro+ ~$100–150 cả luận văn (hoặc thuê GPU <$50). **⚠ Cảnh báo:** precedent là agent-bấm-nút CÓ gold → đóng góp model đặt ở grounding/verifier, phần sinh hướng dẫn giữ no-gold. Chi tiết: memory `advisor-pivot-must-train-model`.
- **HỆ QUẢ:** §2–§4 bên dưới (khung "hai đóng góp = hệ thống + đánh giá", pipeline prompting) là **bối cảnh CŨ đang chờ tái khung** — *nội dung kỹ thuật (dataset/metric/citation) vẫn đúng & tái dùng*, nhưng "đóng góp A = hệ thống prompting" sẽ đổi thành **"đóng góp = MÔ HÌNH train được"**. Deck v2 (22 slide) + v3 (chỉ-pipeline) + report/38/43 hiện vẫn theo khung cũ → cập nhật SAU khi chốt hướng. **KHÔNG xoá report cũ** (user định xoá nhưng đã can — phần lớn tái dùng được; nếu dọn thì ARCHIVE, không xoá).

---

## 1. Đề tài (CHỐT)

- **Tên:** Sinh tự động hướng dẫn sử dụng phần mềm bằng LLM, từ ảnh giao diện (UI screenshot) + câu hỏi use-case.
- **Hợp đồng I/O:** vào = **1 ảnh** (một màn) **hoặc N ảnh đã xáo trộn** (nhiều màn, qua input router) + 1 câu hỏi ngôn ngữ tự nhiên → ra = **hướng dẫn từng bước** cho người đọc, bám ngữ cảnh ảnh.
- **Tính chất:** multimodal (ảnh+text→text). **KHÔNG** có dataset hướng dẫn chuẩn do người soạn để làm ground truth → đó là cái khó trung tâm.
- **Bài báo neo khung đánh giá:** Chim, Ive, Liakata — *Evaluating Synthetic Data Generation from User Generated Text* (**Computational Linguistics 51(1):191–233, 2025**, tạp chí, KHÔNG phải "ACL 2025"). Ta KHÔNG kế thừa bài toán sinh (họ text→text), chỉ **kế thừa khung ĐÁNH GIÁ** (Intrinsic + Extrinsic) cho "synthetic text không có đáp án chuẩn".

---

## 2. HAI đóng góp NGANG NHAU (BẤT BIẾN — user rất kiên quyết, ĐỪNG ĐỂ TRÔI)

> **⚠️ CẬP NHẬT 2026-07-08 (§0 đè lên phần này):** thầy yêu cầu luận văn phải TRAIN MODEL thật → khung "đóng góp A = hệ thống prompting" đang được tái khung thành **"đóng góp = MÔ HÌNH train được"**. Đóng góp B (phương pháp đánh giá no-gold) GIỮ, thành *tín hiệu train + cách đo model*. Phần dưới là lý lẽ cũ (vẫn hữu ích để hiểu vì sao A không phải "chỉ engineering"), nhưng **trục chính đã đổi** — xem §0.

- **(A) HỆ THỐNG sinh hướng dẫn bám-sát-màn** = **lớp trung-thực-hoá** (đối chiếu accessibility tree/VH → bước bịa thì viết lại thành **mô tả bằng lời, KHÔNG đoán nút khác**; model-agnostic, triển khai được) **+ khối sắp thứ tự màn** (hỏi cặp → Copeland → phá vòng min-feedback-arc-set, dùng 5 cue).
- **(B) PHƯƠNG PHÁP ĐÁNH GIÁ** không-gold, không-tự-chấm (một màn + nhiều màn).
- **Trục phân định hai nhánh = "CÓ gold trajectory để chấm hay KHÔNG"** (*gold trajectory* = chuỗi thao tác đúng có sẵn trong dataset).
- ⚠️ **KHÔNG hạ A xuống "chỉ engineering".** Đòn "faithfulness by-construction" là **câu hỏi cần thủ**, không phải lý do demote. Cách thủ: (1) faithfulness tăng vì hệ ĐẠT MỤC TIÊU THIẾT KẾ; (2) báo trung thực **tỉ-lệ-bịa-bản-gốc + %fallback** (không khoe 100%); (3) A là research nhờ **đối-chứng-thất-bại đo được** (phương án "đoán nút gần nhất" → lỗi ngầm → chốt "chỉ mô tả"); (4) DG2/Step-SR cho **con số năng-lực-thật**.
- **ĐIỀU KIỆN giữ "ngang nhau": DG2/Step-SR PHẢI ra số dương thật.** Trọng lượng A đến từ **PHÁT HIỆN thực nghiệm** (đo bịa nhiều model + đối-chứng-thất-bại + DG2 sắp-thứ-tự + phân-tích-cue), KHÔNG từ độ phức tạp code.
- Vẫn **KHÔNG claim SOTA leaderboard** (setup khác: sinh hướng dẫn cho người, không phải agent bấm máy). "null vẫn đậu" áp cho nhánh B + phần đo-cơ-chế; claim chắc-thắng của A kỳ vọng DƯƠNG.
- **Tách 2 bài — CHỐT 2026-07-12 (bản 3, sau deep-research venue + trao đổi user): NỘP CẢ HAI mùa này, tách theo DỮ LIỆU/GÓC-NHÌN (không phải một-màn/nhiều-màn nữa vì nhiều-màn chưa kịp build):**
  - **FAIR (nộp TRƯỚC 15/8 · TIẾNG ANH · danh giá) = BÀI MÔ HÌNH flagship** (Faithful Distillation, Qwen2.5-VL-3B, Tier1/Tier2 định lượng trên MobileViews-English). Hợp FAIR (có track VLM). = chở yêu-cầu-train-model của thầy. **KHÓ + GẤP.**
  - **VCL (nộp SAU 30/8 · TIẾNG VIỆT · dễ hơn) = BÀI SINH-TIẾNG-VIỆT** (cho model — train English — sinh hướng dẫn BẰNG TIẾNG VIỆT trên màn MobileViews English có sẵn + đánh giá no-gold; câu hỏi = chuyển-giao Anh→Việt). **KHÔNG cần dataset tiếng Việt** (đã quét MobileViews local 231 file → chỉ 2 màn chữ Việt lẻ, không có app Việt; user không tự chụp được → góc "app Việt" bỏ). Output tiếng Việt + câu hỏi khác → phân biệt FAIR; ⚠ data nguồn dùng chung nên overlap cao hơn, bù bằng output+câu-hỏi khác. **Smoke-test tuần 1:** model sinh tiếng Việt dùng được không → nếu tệ, fallback bài "phương-pháp-đánh-giá thuần" (headline bơm-lỗi). User xác nhận VCL "miễn có chất ngôn ngữ là được" → fit OK.
  - **FALLBACK CỨNG: VCL = sàn chắc, FAIR = stretch.** FAIR 15/8 không kịp → BỎ FAIR giữ VCL, model đi venue sau. Không để FAIR làm hỏng VCL.
  - **Nhiều-màn (Copeland+min-FAS) + learned reranker (tuỳ chọn +~$10/+~5-6 ngày)** = để dành bài tiếng Anh mở rộng sau (FAIR'27/quốc tế), KHÔNG kịp mùa này.
  - **⚠ Rủi ro:** tải nặng (build+2 bài, 1 tiếng Anh, ~7 tuần); salami-slicing (chống bằng khác-data+khác-câu-hỏi+trích-chéo). **CHƯA verify (đừng bịa):** CFP/deadline VCL2026 (30/8 = user nhớ), dual-submission policy 2 venue, index/tỉ-lệ-nhận. **Nguồn venue:** deep-research `wf_ef24768f`. Chi tiết đầy đủ: `report/KE_HOACH_2_BAI_BAO.md` (bản 3, §0 = quyết định + context).

---

## 3. Pipeline (CHỐT — một hệ duy nhất, input router)

> **⚠️ KHUNG CŨ — nội dung kỹ thuật vẫn TÁI DÙNG cho hướng model** (VLM-mù → so-embedding vs VH → viết-lại là chính lớp lọc-bịa của Faithful Distillation). **DG2/nhiều-màn = HOÃN** khỏi mùa này. Bản chốt hiện tại: `report/54`.

**DG1 (một màn) = 3 HỘP:**
1. **VLM sinh MÙ** — chỉ thấy ẢNH + CÂU HỎI, **KHÔNG** thấy danh sách nút → bản BASE. (Câu hỏi cũng không chứa tên nút → model phải tự đọc ảnh, đó mới là chỗ nó bịa.)
2. **THUẬT TOÁN so-embedding** đối chiếu từng tên nút với View Hierarchy → khớp (≥τ) / bịa (<τ). Không phải LLM.
3. Bước bịa → **viết lại thành MÔ TẢ bằng lời** (KHÔNG đoán nút khác, KHÔNG tra VH gán tên). Đây là **PA2** (bỏ hẳn "correction" cũ vì correction sửa-bậy → silent error).

**DG2 (nhiều màn) = KẾ THỪA NGUYÊN DG1 + thêm STAGE-0 ở đầu:** N ảnh xáo → hỏi VLM từng CẶP "màn nào trước?" → **Copeland** (đếm cặp thắng, phá hoà tất định) → phá vòng mâu thuẫn (min-feedback-arc-set; **M2 2026-07-02: trọng số từ margin-Copeland/self-consistency/min-cardinality, KHÔNG dùng confidence VLM tự-khai vì calibrate kém**) → chuỗi đã sắp → chạy pipeline DG1 cho từng màn. **N=1 → Stage-0 rỗng → về DG1.** *(Nền peer-reviewed từng thành phần: `report/39` — pairwise Qin NAACL24 · Copeland Dwork WWW01 · min-FAS Ailon JACM08 · tác vụ Sort-Story EMNLP16 · τ Fagin SIAM06/Lapata CL06 · cue-attribution Gardner EMNLP20 [trụ khái niệm].)*

**LUẬT VÀNG (chống leakage):** VH + đáp án vàng **CHỈ vào lúc CHẤM**, không vào lúc sinh/sắp. Câu hỏi không chứa tên nút. "Chấm baseline" là bước ĐÁNH GIÁ, không phải bước trong hệ deploy (deploy = sinh→kiểm→né bịa).

**5 ORDERING CUES** (trả lời "model dựa vào đâu biết thứ tự"): gating · nav-affordance (Next/Back) · state-delta (toggle, ô trống→điền, badge) · title-progression · drill-down. Signal-attribution = **stratification một-cue** (chỉ giữ cặp phân biệt bởi đúng 1 cue), KHÔNG che pixel, KHÔNG tin lời model tự khai.

---

## 4. Metric + tính hợp lệ (CHỐT)

> **⚠️ KHUNG CŨ — metric/thống kê TÁI DÙNG để đo model** (trung-thực ALOHa · anti-circularity nomic-lọc/bge-m3-chấm · perturbation-validate · cluster-bootstrap). Đã bổ sung cho hướng model: exact **sign-flip G=12** + MDE + Tier1/Tier2. Bản chốt hiện tại: `report/54` Phụ lục E.

**DG1 (so View Hierarchy):**
- **Trung thực** = 1 − bịa/(bước-nhắc-nút) [ALOHa, NAACL 2024]. **Headline = TỈ-LỆ-BỊA BẢN GỐC** (~¼), KHÔNG phải ~100% sau sửa (trần do thiết kế). **(M4 2026-07-02: báo dạng "CÓ ĐIỀU KIỆN recall-VH" — loại nút icon-only/nhãn-chung khỏi mẫu số; ~¼ = quan sát sơ bộ 1 model, KHÔNG làm headline-phát-hiện tổng quát.)**
- **Đúng-nhãn (label fidelity)** = gọi đúng tên hiển thị [**TỰ ĐỊNH NGHĨA — khai thẳng**, khớp-chuỗi ≠ clarity].
- **Đúng-chỗ (grounding, point-in-bbox)** = (x,y) trong khung nút [SeeClick, ACL 2024; ngưỡng dung sai 14% từ AITW, NeurIPS 2023]. ⚠️ **(x,y) phải từ bộ trỏ ĐỘC LẬP kiểu ScreenSpot dự đoán từ tên+ảnh, KHÔNG lấy tâm bbox đã khớp** (nếu lấy tâm → tautology 100%). **(M1 2026-07-02: RA KHỎI headline một-màn — chỉ dùng ở DG2 [có gold-coords] hoặc đối chứng ScreenSpot-v2.)**

**DG2 (so đáp án vàng):**
- **τ thứ-tự-bộ-phận** = (C−D)/|M|, chỉ phạt **cặp bắt buộc** [**ĐÚNG TÊN = Fagin 2006 "Comparing partial rankings" + Lapata CL 2006; KHÔNG phải "Kendall τ-b"**]. Nhãn cặp-bắt-buộc **suy từ GOLD** bằng quy tắc nhân-quả (màn B chỉ hiện sau gold-action ở A), KHÔNG từ model/cue-detector (chống tự-chấm). Cặp tự-do (điền email/sđt) đảo vẫn đúng.
- **Step-SR** (teacher-forced) = bước đúng/bước-gold; bước đúng = đúng loại thao tác VÀ sai lệch ≤14% [AndroidControl, NeurIPS 2024]. Trục tham chiếu chuẩn ngành, KHÔNG claim ngang leaderboard.

**Anti-circularity:** QUYẾT matched/fallback = **nomic** (τA); CHẤM = **bge-m3 ĐỘC LẬP** (họ khác) + LLM-judge nhị phân khác-họ + token-overlap = **3 cơ chế**. (gpt-4o-mini là generator → LLM-judge KHÔNG dùng GPT-family.)

**Validate metric = PERTURBATION tự động** (bơm lỗi đã-biết ĐỘC LẬP matcher, đo detection/false-positive/đơn-điệu) [Sai et al., EMNLP 2021]. Thầy KHÔNG ưa chấm-người → human-correlation = future-work, KHÔNG trong đậu/rớt. Đóng khung "perturbation = độ nhạy = điều kiện cần, chưa phải convergent validity".

**Protocol validate matcher/judge (CHỐT — 6 nguyên tắc GIỜ ĐỀU có TRỤ peer-reviewed; chi tiết `report/27` §7 + `report/22` §7):** (1) matcher đo theo NGỮ NGHĨA + validate vs người 80–120 cặp → báo **P/R + Cohen's κ**, freeze τ [trụ: **ALOHa NAACL 2024**; bổ trợ CHAIR EMNLP 2018]; (2) gán-tay tối thiểu = few-pairwise/HITLC → giảm **~80%** [trụ: **Active Evaluation ACL 2022, Outstanding Paper** — số peer-reviewed là 80%, KHÔNG phải "89%"]; (3) judge KHÁC HỌ generator + neo người, KHÔNG validate judge bằng nhãn-LLM [trụ: **Panickssery NeurIPS 2024** + Zheng NeurIPS 2023]; (4) VH/a11y KHÔNG phải ground truth (>77% app thiếu nhãn) → biện minh hậu-kiểm+fallback [trụ: **Chen ICSE 2020** Distinguished Paper]; (5) validate metric CHÍNH = perturbation [trụ: **Sai EMNLP 2021** + Ribeiro ACL 2020]; (6) bỏ human-correlation làm cổng đậu/rớt [trụ: **Clark ACL-IJCNLP 2021**]. Preprint (Han 2510.09738 quy-trình-2-bước; Liu 2505.19176; Spiliopoulou 2508.06709) **chỉ bổ trợ**; nếu chạy 2-bước thì κ người-người **TỰ ĐO lại** (không mượn 0.801).

**Thống kê:** cluster bootstrap theo **APP** (màn cùng app không độc lập) + CI 95% + Holm (đa-metric) + seed cố định + 10k resample + pre-register ngưỡng TRƯỚC khi nhìn kết quả + ≥30 episode/mốc N.

---

## 5. Dataset (3 bộ, VAI CỐ ĐỊNH) + citation đã verify

| Bộ | Nội dung | Gold? | Vai |
|---|---|---|---|
| **MobileViews** (preprint arXiv, ghi rõ v1/v3 khi trích) | ảnh + VH + bbox | KHÔNG | **một màn / DG1** |
| **AndroidControl** (NeurIPS 2024 D&B, peer-reviewed) | episode nhiều màn + a11y tree + gold action mỗi bước | CÓ | **nhiều màn / DG2 + Step-SR** |
| **ScreenSpot-v2** (OS-Atlas, **ICLR 2025**; gốc SeeClick ACL 2024) | ảnh + bbox chuẩn | — | **đối chứng grounding** + bù credibility MobileViews |

- Cả MobileViews LẪN AndroidControl đều CÓ nguồn phần tử (VH / a11y tree). Bộ chỉ-có-ảnh-trần → cần bộ dò (recall-conditioned, **cổng K1**). Thực tiễn: on-device có a11y tree LIVE qua AccessibilityService (trợ năng).
- **AITW (NeurIPS 2023):** nguồn ngưỡng 14% = **trích bắt buộc**; làm dataset đối chứng = tuỳ chọn. **Mind2Web = future-work** (nhánh web, chỉ có DOM không bbox).
- AndroidControl để đo DG2: **episode bị xáo trộn**, model xếp lại, gold verify. Số đã verify: 15,283 episode/833 app; mean ~5.5 step; p95=13. **Chưa có count theo từng N → phải tự đếm histogram (cổng KN).**
- **Citation khác đã verify:** Chim = CL 51(1) 2025; oracle = Barr TSE 2015. Nguyên tắc: xương sống phương pháp chỉ trích peer-reviewed; preprint (OmniParser/Qwen) chỉ là hiện vật kỹ thuật.
- **DATASET đã verify sâu (2026-07-03, deep-research+debate `wf_6d07419b` → chương chuẩn luận văn `report/44`):** MobileViews = **preprint arXiv 2409.14337** (v3 đổi tên "Million-scale"; **giấy phép MIT**; BUPT+Tsinghua; thu-thập TỰ ĐỘNG bằng bot VLM-DroidBot; **paper 1,2M nhưng bản công khai = 600K**, ta dùng **127 màn/30 app** [`kept_screens_final.json`, mở rộng 2026-07-06; pilot cũ 81/17 lỗi thời]; VH schema trường `class`+`bounds`lồng`[[x1,y1],[x2,y2]]`). AndroidControl = **"On the Effects of Data Scale on UI Control Agents", Li et al. Google DeepMind, NeurIPS 2024 D&B** (arXiv 2406.03679; **CC0**; người-thật Pixel ~1 năm; 8 loại thao tác; **test=1.542 KHÔNG phải 2.855**). ScreenSpot-v2 = **kèm OS-Atlas ICLR 2025** (gốc SeeClick ACL 2024; **apache-2.0**; 1.272 chỉ dẫn = 502 mobile/334 desktop/436 web; sửa 11,32% lỗi nhãn; bbox `[x1,y1,x2,y2]`).
- **⚠ 5 ĐIỀU KIỆN CHỐT TRƯỚC KHI IN (report/44 §8):** (1) không in test "2.855"→dùng 1.542; (2) tính độ-phủ-nhãn VH (`dg1_vh_coverage.py`); (3) hiệu chỉnh khung toạ độ MobileViews (lệch width/height) TRƯỚC khi tính grounding; (4) đối chiếu tác giả OS-Atlas trên OpenReview; (5) KHÔNG khẳng định affiliation Xiaomi.
- **5 cổng cứng:** K1 (đo recall detector) · KN (histogram độ dài episode) · KZ' (prior-art sắp-ảnh — đã GO) · KB (chống leak step-index: strip metadata + tái mã hoá ảnh + che status bar/đồng hồ/pin/badge + loại episode 2-ảnh trùng-pixel) · **K-pair (M2 2026-07-02: đo acc-pairwise THÔ của VLM vs gold TRƯỚC khi tổng hợp Copeland — nếu ~0.5 thì Stage-0 vô hiệu, khai thẳng)**. KN + KZ' đã GO.
- **Prior-art phải thừa nhận** (sắp-ảnh): Sort-Story (EMNLP 2016, dùng Spearman), Wu et al. (ACL 2022), RankGPT (EMNLP 2023, listwise). Độ mới ta = miền GUI + điều-kiện-hoá mục tiêu + gắn ordering→sinh hướng dẫn + partial-order từ gold + signal-attribution. Thêm related-work: VLM-SlideEval (2510.22045), Screen-flow (2503.06067), No Free Labels (2503.05061). **+ Must-cite 2025-2026 (freshness scan `report/42`, đã verify):** FaithScore (Findings EMNLP24, reference-free faithfulness LVLM — ta khác: verify với VH có cấu trúc) · Reliability-without-Validity (2606.19544, hậu thuẫn κ-headline) · LLM-as-Meta-Judge (2603.09403, gần ý-tưởng nhánh B → phải phân định miền GUI) · Ref-free-eval survey (2501.12011) · VECTOR/What-Happens-When (2512.08979, "VLM mù thời gian" → luận cứ DG2+anti-leak) · UI-TARS (2501.12326, phân biệt setup) · GUI-Odyssey (ICCV25)/AMEX/ScreenSpot-Pro (acknowledge landscape).
- **Tiền lệ pipeline-đơn-giản-mà-đậu:** G-Eval / SelfCheckGPT / FActScore / RAGAS / ALOHa / BERTScore.

---

## 6. Trạng thái hiện tại (cập nhật 2026-07-08)

> **⛔ TRẠNG THÁI DƯỚI ĐÂY ĐÃ LỖI THỜI (mốc 2026-07-08, khung prompting).** Trạng thái MỚI NHẤT (2026-07-12) = **`report/00_TONG_HOP_TAT_CA.md` §6**. Giữ phần dưới chỉ để tham chiếu kỹ thuật kết-quả-sơ-bộ; ĐỪNG coi là việc-đang-làm.

**Giai đoạn:** đề cương/thiết kế, có kết quả SƠ BỘ. Đã qua review sâu (3 agent) → phát hiện & VÁ circularity: matcher VỪA sửa VỪA chấm → faithfulness ~100% là tautology. Vá = PA2 (chỉ matched/fallback) + chấm bằng bge-m3 độc lập. Claim DG1 thu hẹp: **DUY NHẤT = "giảm tham-chiếu-nút-không-tồn-tại, giá = %fallback"** (bỏ claim đúng-nhãn; "sửa-đúng" để dành DG2/Step-SR).

**Kết quả sơ bộ (gpt-4o-mini, mẫu nhỏ):** tỉ lệ bịa bản gốc ~¼ số bước; lớp đối chiếu nâng faithfulness ở mọi τ nhưng **CI còn chạm 0 (n nhỏ, 1 app cũ)**; fallback ~19%; label-fidelity & format đứng yên (no-harm). Bản chính (**127 màn/30 app**, `kept_screens_final.json`) **chưa chạy** (cần API).

**Deliverables trình thầy:**
- `report/36` — thuyết minh đầy đủ DG1+DG2 (người mới hiểu, ví dụ số + Q&A giám khảo) — **NGUỒN-SỰ-THẬT phần một-màn** (thay `25` cũ đã archive).
- `report/38` — **BẢN TRÌNH BÀY BẢO VỆ** (văn phong học thuật, bám slide, luận điểm + trích dẫn + phụ lục Q&A).
- `LUAN_VAN_SLIDE.pptx` — **deck v11 = 17 slide** (văn phong học thuật, đủ 3 dataset, nói "một màn/nhiều màn"). Build: `slides/build/build.js` (pptxgenjs, ảnh thật `_img/`).

**Debate slide 2026-07-01 (5 phản biện→verify→tổng hợp; 19/32 sống): phán quyết nguyên-trạng THẤP–TB, ĐÃ VÁ 4 blocker vào deck v11 + file 38:**
1. Mâu thuẫn ví dụ Confirm/OK → S9 đổi bước-ảo-giác thành "Mở Cài đặt" (nút không tồn tại); Confirm/OK CHỈ giữ ở label-fidelity; thêm quy tắc τ.
2. Thiếu con số → THÊM slide "Kết quả sơ bộ" (nhãn trung thực: mẫu nhỏ/1 model/CI chạm 0/đang chạy 80+ màn) + hạ "ngang nhau" → có điều kiện DG2 dương.
3. Grounding tautology → nêu rõ (x,y) từ bộ trỏ độc lập, không lấy tâm bbox.
4. VH thiếu/nhiễu nhãn → khai độ-phủ-nhãn + loại nút nhãn-chung khỏi mẫu số + giới hạn.
- **CÒN LÀM (free):** tính CON SỐ độ-phủ-nhãn thật từ mv_multiapp; verify venue citation a11y-tree không đầy đủ (Ross et al.) TRƯỚC khi trích.

**Deep-research validate-metric: ✅ XONG.** (2026-07-01) 6 claim U1–U6 verify (5 SUPPORTED+1 PARTIAL, cả 6 preprint→bổ trợ) → `27` §6. **+ (2026-07-02)** tìm+xác minh **TRỤ peer-reviewed cho cả 6 nguyên tắc** (Panickssery NeurIPS24 · ALOHa NAACL24 · Active-Eval ACL22 · Sai EMNLP21 · Chen ICSE20 · Clark ACL-IJCNLP21) → `27` §7; đính chính số HITLC **89%→80%**. Protocol đầy đủ ở §4 trên + `22` §7.

**+ (2026-07-02) nền peer-reviewed pipeline DG2:** cả 6 thành phần Stage-0 đã có trụ bình-duyệt (5 trụ chính-danh + (e) cue-attribution chỉ trụ KHÁI NIỆM Gardner EMNLP20 = chỗ đóng-góp-mới, không phải lỗ hổng) → **`report/39`**. Caveat: quote Copeland (Dwork) cần đối chiếu PDF; Screen-flow 2503.06067 = preprint.

**+ (2026-07-02) DEBATE giám-khảo với PIPELINE (5 phản biện→verify→chủ-tịch, workflow chạy xong 36 đòn/12 sống): PASS-CÓ-ĐIỀU-KIỆN — KHÔNG lỗi thiết kế; rủi ro = tài liệu + chưa-có-số. 5 MAJOR phải vá (chi tiết `report/40` §4):**
  - **M1** rút point-in-bbox KHỎI metric một-màn → dời DG2 (tránh tautology tâm-bbox).
  - **M2** thêm **cổng K-pair** đo acc-pairwise THÔ vs gold (sàn >0.5) TRƯỚC khi tổng hợp; **BỎ "cắt cạnh ít-chắc-nhất"** (VLM calibrate kém) → margin-Copeland/self-consistency/min-cardinality-FAS + ablation phá-vòng.
  - **M3** thống kê: **wild-cluster bootstrap-t (Cameron-Gelbach-Miller 2008)** + báo G≈17 caveat under-coverage; **timestamp pre-reg = `git init` + commit report/22 TRƯỚC khi chạy** (repo hiện non-git!); số hiện = "exploratory".
  - **M4** tính độ-phủ-nhãn VH → tỉ-lệ-bịa dạng khoảng "có điều kiện recall-VH" + loại nút icon-only/nhãn-chung; xoá overclaim file 36 d.99 ("có sẵn khung nút nên rủi ro bị chặn" — mâu thuẫn Chen ICSE20).
  - **M5** đổi "hai ngang nhau" → **"ngang nhau CÓ ĐIỀU KIỆN (chờ DG2 dương)"** ở 36/38/slide; dời trụ chống-"chỉ-engineering" sang 3 chân ĐÃ CÓ (silent-error · tỉ-lệ-bịa-gốc · %fallback).
  - Lá chắn giữ nguyên: luật-vàng chống-leak · đối-chứng-thất-bại đo được · nền peer-reviewed đầy đủ.
  - **ĐÃ ÁP (2026-07-02, chỉ .md — user review + chạy code mai):** M1/M3/M4/M5 vào framing + pre-register (`report/22` §8) + `report/36` (bỏ overclaim "rủi ro bị chặn", grounding ra khỏi một-màn) + CLAUDE §3/§4/§5. Viết sẵn `harness/dg1_vh_coverage.py` (M4 — CHƯA chạy). **CẦN CHẠY CODE (mai):** M4 tính độ-phủ-nhãn, M3 `git init`+commit, M2 cổng K-pair khi prototype DG2. File A-Z người-mới: **`report/41`**.

**+ (2026-07-03) FRESHNESS SCAN 2025-2026 (`report/42`, `wf_3d7cdc91`): KHÔNG lỗi thời, KHÔNG bị scoop.** Không ai ghép "sinh hướng dẫn cho người + no-gold eval GUI". Chỉ cần: (a) **thêm ~8 cite định vị** vào related-work (đã liệt §5); (b) **✱ nên thêm ≥1 generator đời mới** (GPT-4.1 / Gemini-2.5-Flash / Qwen3-VL) cạnh gpt-4o-mini để bảng số không kẹt model cũ — HỎI USER. Bài gần nhất phải PHÂN ĐỊNH: LLM-as-Meta-Judge (2603.09403) [khác: miền GUI + bơm-lỗi-độc-lập-matcher]. Thiết kế lõi VỮNG 2026 (niche VH-structured-check độc nhất; perturbation-validate đang là dòng sống).

**+ (2026-07-03) DEBATE giám-khảo-2026 "pipeline+metric phù hợp 2026?" (`report/42` §6, `wf_73dfaaf9`, 25 đòn/13 sống): PHÙ-HỢP-CẦN-ĐIỀU-CHỈNH.** Không lỗi thời/scoop nhưng bằng-chứng neo 1 model đời-2024 → **3 PHẢI NÂNG (điều kiện đậu 2026):** **M1** (nguy hiểm nhất, 4/13 đòn) đo bịa trên ≥1 **frontier 2025-26 rẻ** (Gemini-2.5-Flash/GPT-4.1-mini) cạnh gpt-4o-mini → báo tỉ-lệ-bịa **đường-cong per-model** không headline "¼" tĩnh (`env VLM_MODEL` sẵn, không sửa code — ✱API); **M2** thêm **baseline listwise một-shot** (RankGPT-style) chấm cùng τ+Step-SR+cột-chi-phí, reframe pairwise = **substrate-audit** (cho stratification 1-cue + intransitivity audit + partial-order-from-gold, trích VECTOR "VLM mù thời gian"); **M3** reframe A: "model-agnostic BY CONSTRUCTION kiểm trên 3 đời model" + đẩy **niche on-device** (a11y-tree live + model nhỏ không gọi được frontier → nối AskEase CHI26), neo "A ngang B" vào DG2/Step-SR + đối-chứng-thất-bại (KHÔNG vào độ-lớn con số bịa). **ĐÒN NGUY HIỂM NHẤT + thủ sẵn:** xem `report/42` §6 (frontier "chữa bệnh sắp tự khỏi" → thủ bằng đường-cong-bịa >0 ở frontier + niche on-device).

**+ (2026-07-06) DEBATE bộ thí nghiệm (3 phản biện: thừa/trùng · clarity · thiếu/cần-thiết): KHÔNG lỗi thiết kế, KHÔNG trùng khoa học — nhưng phình đếm-số + lỗ trình bày. ĐÃ VÁ TRỌN vào `report/43` Ch.13:** tái-khung "15 TN" → **~7 cốt lõi thật** (E1+E2 = một run hai readout; E6 = mục-con validate-B; E9 = cổng; E10–E13 = contingent); thêm **E16** (kiểm-hữu-ích định tính, RQ7) + **arm "nạp VH lúc sinh"** trong E2 (đo leakage nội bộ); định nghĩa **PMR (Def 5.6)** + silent-error-rate + N_eff/wild-cluster/MDE; thêm **bảng mẫu shell** T3/T8 + ánh xạ RQ→E→T/F + ngưỡng đậu/rớt định lượng; inter-annotator κ người-người cho E5. **DATA MỞ RỘNG:** MobileViews **81/17 → 127/30** (`kept_screens_final.json`, khớp cỡ-mục-tiêu pre-reg + m̄≈4,2); ScreenSpot 501 mobile sẵn; AndroidControl **scan 1.600 ep (nguồn `smolagents/android-control` test=3.051; ckg-parsed BỎ vì 52% gap) + chọn 286 ep** (`dg2_sample.py`→`dg2_episodes.json`, KN PASS N∈{4,5,6}; re-scan app từ `goal`+`open_app` → **237 app / 1 unknown** [số cũ 96/169 lỗi thời]). **Chốt mẫu 3 bộ (GỘP, nguồn-sự-thật): `report/48_dataset_selection.md`** (đã xoá `48_chon_mau`). **G=30 một-màn (G_eff-Kish≈24) / G nhiều-màn=237-app (194 singleton) — đã vá mâu thuẫn G≈17 cũ.** **DEBATE item-selection 4-giám-khảo (2026-07-06): HỢP LÝ-CÓ-ĐIỀU-KIỆN; 3 lỗ CAO = MIN_ACT bias + cắt N≥7 + ScreenSpot iOS/demote; estimand=macro-per-app (cấm "đại diện").**

**Đã dọn file (2026-07-01, cập nhật 2026-07-08):** `report/` có **24 file lõi** (bản đồ §10 — đã thêm 44/45/47/48/49); harness dọn script cũ; mọi file cũ ở `report/_archive/` (37 file) + `harness/_archive/` (khôi phục được). **Git hygiene (2026-07-08):** thêm `.gitignore` + gỡ `slides/build/node_modules` (353 file) & `*.pdf` khỏi git index (vẫn còn trên đĩa).

---

## 7. Môi trường + code harness

- **Máy KHÔNG-GPU** → VLM nhìn-ảnh PHẢI dùng API cloud (`gpt-4o-mini`, key ở `harness/.openai_key` — **KHÔNG in ra**). Ollama local: `nomic-embed-text`, `bge-m3` (chấm độc lập), `llama3.2`, `qwen2.5vl:3b/7b`.
- **⚠️ 2026-07-08: user sẽ MUA Colab Pro** để train/fine-tune model (LoRA/QLoRA 3B-7B) — bù cho việc máy không GPU. Đây là môi trường train chính cho hướng model mới (§0).
- Windows: chạy Python phải `$env:PYTHONIOENCODING="utf-8"`.
- **Dữ liệu:** `dataset_samples/mv_multiapp/` → lọc rác + mở rộng → **127 màn/30 app** (`harness/kept_screens_final.json`, chốt 2026-07-06; pilot cũ 81/17 lỗi thời). ScreenSpot mobile = **501 item** (290 text/211 icon, `screenspot_full/screenspot_mobile_v2.json`). AndroidControl = **đã scan 1.600 ep + chọn 286 ep** (`smolagents/android-control` test; `dg2_sample.py`→`dg2_episodes.json`, 237 app; ảnh tải sau khi chạy). app MobileViews = `screen.split("_")[0]` → cluster-by-app được. **Chốt mẫu chi tiết: `report/48_dataset_selection.md`.**
- **Harness (`harness/`):** `dg1_data.py` (lọc rác), `dg1_run.py` (sinh BASE, PA2, retry-429, resume theo tag), `dg1_pa2_score.py` (derive PA2 + cluster bootstrap + Holm + seed), `dg1_independent_score.py` (chấm bge-m3 + đo silent-error), `dg1_scorer.py` (load VH, point-in-bbox), `aloha_match.py`, `dg1_questions.py`, `dg1_filter_data.py`, `fetch_mobileviews.py`, `_http.py`/`_apikey.py`. *(Đã dọn 2026-07-01: file cũ/superseded chuyển `harness/_archive/` — dg1_score_all [circular, KHÔNG dùng], run_dg1_trial(2), score_v2, effectiveness_ab, generate_cache, trackB, gen_cache/; report cũ ở `report/_archive/`.)*

---

## 8. Việc tiếp theo + nguyên tắc

- **Free (chưa làm):** freeze τA + báo precision/recall matcher (tập gán-tay 80–120 cặp, precision≥0.95); dựng perturbation harness (lỗi bơm độc-lập matcher); module LLM-judge khác-họ; tính con số độ-phủ-nhãn VH. *(Nguồn-trụ peer-reviewed cho protocol validate: ĐÃ XONG — `report/27` §7.)*
- **✱ Tốn API ~$0.05 (HỎI USER TRƯỚC):** sinh câu hỏi affordance-seeded + cổng answerability; sinh BASE 127 màn.
- **Kill-test tuần-1:** K1 (recall) + KN (đếm histogram) + KB (chống leak) → chốt khung với thầy → harness → ablation.
- **NGUYÊN TẮC CHI TIỀN (user nhấn mạnh):** chạy MỘT lần cho đúng; mọi bước ✱ phải HỎI USER TRƯỚC; ưu tiên local/free + cache.

---

## 9. Điểm CHƯA CHỐT

- **Model open/closed:** ~~khuyến nghị bắt đầu VLM API (gpt-4o-mini) làm lõi~~ → **ĐỔI (2026-07-08, §0):** fine-tune model mở (Qwen2.5-VL 3B/7B, LoRA) giờ là **TRUNG TÂM** (không còn tuỳ chọn) vì thầy yêu cầu train model thật; gpt-4o-mini hạ vai thành **teacher để distill**. Hướng train cụ thể chốt sau deep-research (`report/50`).
- **Tiếng Việt:** thầy ưu tiên VN, nhưng dataset chuẩn là EN/ZH → định lượng chạy EN/ZH; VN = demo định tính + ~120 mẫu app VN cho chuyên gia (nói rõ với thầy: KHÔNG có bảng số VN định lượng).
- **Nhánh web (Mind2Web):** future-work.

---

## 10. Bản đồ file `report/` (biết chỗ đào chi tiết)

- **⭐ ĐỌC ĐẦU TIÊN:** `report/00_TONG_HOP_TAT_CA.md` (trạng thái hiện tại) · `report/54_PIPELINE_FINAL_DOC_HIEU_TOAN_BO.md` (pipeline/model tự-đủ) · `report/KE_HOACH_2_BAI_BAO.md` (2 bài FAIR/VCL) · `report/53_ke_hoach_build_model.md` (config/build khi code).

- **Nguồn-sự-thật / tham chiếu:** `05` (final plan — thắng khi mâu thuẫn) · `01` (metrics) · `02` (datasets) · `04` (feasibility + kill-test K1/KN/KZ'/KB) · `12` (runbook chạy thử) · `22` (pre-registration + §7 protocol validate)
- **DG1 lõi:** `36` (nguồn-sự-thật một-màn) · `26` (review 3-agent + đối-chứng-thất-bại correction→silent-error). *(`25` cũ tự-mâu-thuẫn — correction đã bỏ + bảng "100%/80 màn" circular — ĐÃ archive.)*
- **Research / debate:** `27` (deep-research validate-metric — §6 kết quả + §7 trụ peer-reviewed) · `28` (LLM-judge protocol) · `39` (nền peer-reviewed pipeline DG2) · `40` (debate giám-khảo với pipeline — **§4 phán quyết CHÍNH THỨC PASS-có-điều-kiện + 5 fix M1–M5**; §3 interim bù độ phủ) · `42` (freshness scan 2025-2026: KHÔNG lỗi thời/scoop + must-cite)
- **Người mới / thuyết phục:** `41` (giải thích A–Z) · **`43` (HỒ SƠ TOÀN DIỆN — văn phong khoa học, định nghĩa/công thức/mã giả, ví dụ chạy đầu-cuối, thủ-sẵn giám khảo)** · **`44` (CHƯƠNG DỮ LIỆU chuẩn luận văn — 3 bộ verify tận file: nguồn/venue/quy mô/giấy phép/cấu trúc/ví dụ thật/hạn chế + 5 điều kiện chốt)** · `49` (giải đáp thắc mắc theo đợt — Q&A tích luỹ khi đọc 43)
- **Thiết kế TN / dữ liệu:** `45` (verify pipeline progress) · `47` (thiết kế thí nghiệm) · **`48` (CHỐT MẪU 3 bộ — nguồn-sự-thật dataset selection)**
- **Trình bày / nộp:** `30` (abstract VCL) · `36` (thuyết minh đầy đủ) · `38` (bản bảo vệ + Q&A, có PDF font-VN qua `report/md2pdf.py`) · `LUAN_VAN_SLIDE.pptx` (deck v11, build `slides/build/build.js`) · `LUAN_VAN_SLIDE_v2.pptx` (deck v12 từ 43, build `slides/build/build_v2.js`)
- **Kế hoạch / sổ:** `KE_HOACH_2_BAI_BAO` · `RESEARCH_LEDGER`. File cũ/superseded ở `report/_archive/` (37 file).
- **⚠️ HƯỚNG MODEL MỚI (§0):** **`report/50_deepresearch_model_centric.md`** — deep-research chọn phương pháp train-model + 3 vòng debate chốt "Faithful Distillation". **`report/52_debate_tinh_moi_faithful_distillation.md`** — debate vòng 4 kiểm tra tính-mới (2026-07-09): CÓ-NHƯNG-CẦN-VÁ. **`report/53_ke_hoach_build_model.md`** — debate vòng 5 (2026-07-10): verdict ĐỦ-CÓ-ĐIỀU-KIỆN + kế hoạch build model đầy đủ (framework/config/data-pipeline/Colab/thống kê), xem §0 trên. **`report/61_deepresearch_faithful_distillation_verified.md`** (2026-07-16, ĐÃ verify đối kháng — bản chốt của `59`) — 6 câu hỏi mở về DPO-trên-cặp-lọc/mode-collapse/risk-coverage/VH-coverage/xếp-hạng-đóng-góp; **CHƯA thay đổi thiết kế đã pre-register (`56`)**, chỉ là input chờ user quyết định có nâng cấp thước đo (risk-coverage/AURC) hay thêm nhánh DPO hay không. **Chuỗi rà-soát-lại theo yêu cầu user (16-17/7):** `62` (giải thích 61 dễ hiểu) · `63` (plan nâng cấp chia nhỏ 5 vòng A-E: risk-coverage/template/OCR/DPO/so-sánh) · `64` (thiết kế lại từ trang trắng — trùng xương sống, khác 5 điểm, lớn nhất = thiếu trục "ĐÚNG" → đề xuất AndroidControl từng-bước) · **`65` (tự phản biện 6 nghi ngờ + plan kiểm chứng K1-K3/D1-D3/R1-R2 — user sẽ tự thực thi từng vòng; K1 kill-test matcher hai chiều là việc ĐẦU TIÊN, free)**.
- **Tiện ích:** `report/md2pdf.py` (md→PDF font tiếng Việt DejaVu; `python3 report/md2pdf.py <số|đường-dẫn>`, mặc định 43).

---

## Ghi chú làm việc cho trợ lý
- Trao đổi bằng **tiếng Việt**.
- **VĂN PHONG (user nhấn mạnh 2026-07-15):** dùng từ **tự nhiên**, KHÔNG được lộ giọng AI-gen. Cấm tự chế thuật ngữ rồi dùng như thể chuẩn ngành — đã từng mắc: *"bản kê nút"*, *"bản thiết kế màn hình"* (đều là từ tự bịa; tên thật = **View Hierarchy / VH**, thầy là tiến sĩ AI nên biết thuật ngữ), *"trung-thực-hoá"*. Tránh các cụm máy móc: "Nói một câu:", "Điểm mấu chốt", "đáng nói nhất", "gói gọn", lạm dụng gạch ngang dài. **Yêu cầu kép:** vừa dễ hiểu cho người không chuyên, vừa đủ hàm lượng khoa học (công thức + citation đúng venue) để thuyết phục một **tiến sĩ AI khó tính** — cách làm: lời thường trước, "hộp kỹ thuật" kèm công thức/trụ trích dẫn sau.
- **CHỐNG TRÙNG LẮP:** trước khi thêm nội dung vào report/54, kiểm xem đã có ở mục khác chưa — file từng phình vì kể cùng một chuyện 3-5 lần (Tier1/Tier2 4 chỗ, "vừa đá bóng vừa thổi còi" 2 lần cách nhau 40 dòng, cả Phụ lục E là bản sao của mục "Bộ thước đo"). Đã dọn 2026-07-15. Giữ layer: **pitch (trang gặp thầy) → giải thích (Phần 1) → công thức (phụ lục)** — mỗi layer phải THÊM thông tin, không nhắc lại.
- **Sau mọi thay đổi lớn:** cập nhật file report tương ứng + chạy multi-agent debate để kiểm chất lượng (user thích quy trình này); cập nhật CLAUDE.md khi có quyết định mới.
- Tư vấn model/giá/API Claude/Anthropic: đọc tài liệu, KHÔNG trả lời theo trí nhớ.
- Citation: chỉ trình peer-reviewed như đã bình duyệt; verify venue/năm trước khi trích.
