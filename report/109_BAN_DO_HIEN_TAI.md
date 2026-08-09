# Bản đồ hiện tại — đọc file này là nắm toàn bộ luận văn

> **Dành cho ai:** chính mình sau vài tuần quên mất, hoặc bất kỳ ai cần hiểu dự án đang ở đâu mà
> không muốn đọc 12 file report.
>
> **Ngày:** 9/8/2026. **Trạng thái:** xong hết phần miễn phí, cổng A đã đạt, sắp thuê máy huấn
> luyện. Chưa tiêu đồng nào cho GPU.
>
> **Ba file kia dùng khi nào:** `report/106` = bản đăng ký trước (thiết kế đã niêm phong, luật
> đọc kết quả) · `report/108` = sổ kê khai (đã làm gì, số nào tin được) · `report/100` = giới
> thiệu pipeline cho người ngoài. File này là **bản đồ**: nối ba file kia lại và nói việc kế tiếp.

---

## 1. Luận văn này làm gì

**Bài toán.** Cho một ảnh màn hình điện thoại và một mục tiêu người dùng ("đổi tên ghi chú
Grocery"), sinh **một câu hướng dẫn cho người đọc** chỉ rõ phải chạm vào đâu.

Khác với dòng nghiên cứu GUI agent hiện nay ở chỗ **người đọc là NGƯỜI, không phải máy**. Các
bài như Aguvis, UI-R1 sinh toạ độ để máy tự bấm; câu chữ ở đó chỉ là bước trung gian và không
được chấm. Ở đây câu chữ là **sản phẩm cuối** và là thứ duy nhất đem chấm.

**Hai đóng góp, ngang nhau.**

1. **MÔ HÌNH** — Qwen2.5-VL-3B tinh chỉnh QLoRA. Thành phần đề xuất: *"mô tả phân biệt trước,
   phát ngôn sau"*. Đích huấn luyện không phải câu trơn mà là:

   ```
   <desc>vai trò | tên | <point>x,y</point> | dấu hiệu phân biệt</desc>  rồi mới tới  câu
   ```

   Lúc chấm cắt bỏ phần `<desc>`, chỉ lấy câu. Headline **không** phải "hơn gpt-4o-mini" mà là
   **ablation nội bộ: S2 có thành phần so với S1 không có**.

2. **ĐÁNH GIÁ** — thước *executability*: đưa câu do mô hình viết cho một **bộ trỏ độc lập**
   (UGround), xem nó trỏ vào đâu, rồi hỏi phần tử đích có phải phần tử **gần điểm trỏ nhất** trên
   màn không (ô Voronoi). Kèm luật khớp loại thao tác và luật chống đảo nghĩa bật/tắt.

**Cấm dùng chữ "đầu tiên" / "mới" cho thành phần mô hình.** Dòng REG phân biệt đã chiếm ý "câu
phải đủ để bên kia trỏ đúng" từ 2016 (Mao CVPR16, Luo CVPR17). Khe còn trống là: đưa tính phân
biệt vào **đích huấn luyện** trong miền GUI, và dùng `step_instructions` của AndroidControl làm
**đích sinh** thay vì đầu vào.

---

## 2. Pipeline một hình

```
AndroidControl (NeurIPS 2024)
   ├─ câu người viết  (HarrytheOrange/parsed_AndroidControl)
   ├─ ảnh màn hình    (ckg/AndroidControlParsedWithImages-20k)
   └─ cây trợ năng    (all_forest_dict.zip, 99.131 màn)
                │
                │  ghép theo (episode_id, step_id) — đã kiểm bằng OCR tại điểm chạm
                ▼
   ┌────────────────────────────────────────────────┐
   │ DỰNG NHÃN KHAI BÁO (tự động, không thuê người) │
   │  toạ độ chạm thật → hộp nhỏ nhất chứa nó       │
   │  → vai trò từ cây · tên từ OCR/cây · dấu hiệu  │
   │    phân biệt tính bằng luật + mỏ neo chữ       │
   └────────────────────────────────────────────────┘
                │
                ▼
   4 nhánh dữ liệu ── s1 · s2 · s2r · s2_nopoint
                │
                ▼
   HUẤN LUYỆN  Qwen2.5-VL-3B + QLoRA r=8, tháp thị giác đóng băng
                │
                ▼
   SINH CÂU trên 4.463 bước chạm của tập kiểm
                │
                ▼
   CHẤM: câu → UGround trỏ toạ độ → so với cây trợ năng bằng ô Voronoi
         + khớp loại thao tác + không đảo nghĩa
                │
                ▼
   Δ = S2 − S1, khoảng tin cậy bằng wild cluster bootstrap gom cụm theo ứng dụng
```

---

## 3. Sáu nhánh, và mỗi nhánh trả lời câu gì

| Nhánh | Đích sinh | Trả lời câu hỏi |
|---|---|---|
| **S1** | câu trơn | nền so sánh |
| **S2** | khai báo thật + câu | **headline** — thành phần có tác dụng không |
| **S2r** | khai báo **giả** cùng độ dài token + câu | điểm tăng có phải chỉ vì chuỗi dài thêm |
| **S2-nopoint** | khai báo bỏ ô toạ độ + câu | công thuộc về toạ độ hay thuộc về tính phân biệt |
| **B-infer** | dùng trọng số S1, lúc chạy nhét danh sách phần tử vào đầu vào | huấn luyện có hơn đưa-thông-tin-lúc-chạy không |
| **Mô hình gốc** | không huấn luyện | bản thân SFT mua được bao nhiêu *(thêm 9/8)* |
| **Phép thử TRẦN** | nối khai báo CHUẨN vào đầu vào lúc chạy, + đối chứng đệm cùng số token | trần trên của thiết kế — nếu phát không công đúng thứ tầng khai báo cố sinh ra thì điểm lên tới đâu |
| ~~S3-pilot~~ | S2 + khoản phạt lề | **chưa có mã hàm mất mát**, nằm sau cổng C |

Mỗi nhánh huấn luyện **hai hạt giống** (101, 202). Cặp hạt giống của S1 làm **null thực nghiệm**:
chênh lệch giữa hai lần chạy cùng thiết kế chính là cỡ nhiễu, và Δ phải lớn hơn cỡ nhiễu đó.

---

## 4. Số đã đo, tin được

### Dữ liệu

| | |
|---|---|
| Tập dạy | 76 shard ≈ 64.500 bước / 15.283 tác vụ *(mới dựng 2 shard tại máy)* |
| Tập kiểm | **6.958 bước / 1.432 tác vụ**, trong đó **4.463 bước chạm** đem chấm |
| Rò rỉ | 0 tác vụ trùng giữa dạy và kiểm |
| ⚠️ Không phải app-unseen | 92% ứng dụng của tập kiểm cũng có trong tập dạy — phải khai lợi thế sân nhà |
| Nhãn khai báo | tên rõ 73,8% · toạ độ sạch 100% · dấu hiệu phân biệt gỡ được 75,9% |

### Dụng cụ đo (đo 9/8, miễn phí trên Kaggle T4)

| | |
|---|---|
| **Cổng A** | **ĐẠT** — sai số bộ trỏ trung vị **0,7%** bề ngang màn, ngưỡng 3% |
| **Trần của thước** | **70,0%** KTC95 [64,5 – 75,3] |
| Ngưỡng 3% có căn cứ | dưới 3% thì **100%** trúng ô Voronoi (n=188) |
| Đĩa dung sai | **vô dụng** — 100% ngay cả khi lệch 8–14% màn. Chỉ báo kèm |
| Cụm tập kiểm | G=1.091, **G hiệu dụng 454,3**, cụm lớn nhất 58 bước |
| MDE **chiếu** | 3,9 – 6,6 pp tuỳ độ lệch chuẩn hiệu số theo cặp |

**Cách đọc trần 70,0%:** một nhánh đạt 45% là đạt **64% của trần**, không phải "kém quá nửa".
Mọi bảng kết quả phải in con số 70,0 cạnh bên.

### Đường ống

| | |
|---|---|
| Cấu hình huấn luyện | LLaMA-Factory nhận; LoRA khớp **14.966.784** tham số (đúng 36 tầng × 7 mô-đun) |
| Tự kiểm lô 1 vs lô 8 | **8/8 trùng nguyên văn** — đệm bên trái đúng |
| Sinh câu · chấm điểm · B-infer | cả ba đã chạy thật trên mô hình gốc |
| Cache khoá-giá trị | bật, **trùng tuyệt đối 50/50** với vết cũ; chấm một nhánh 48h → **5h** |
| Bơm lỗi kiểm thước | 8/10 ngưỡng khoá trước, hai chỗ rớt đã khai |

---

## 5. Giới hạn phải khai — không được im lặng bỏ qua

1. **Trần thước 70%**, không phải 100. Khoảng trống cho S2 hẹp hơn tưởng.
2. **Bộ trỏ bỏ cuộc theo trục ngang** ở 15,3% số bước (không nhận ra phần tử thì trả x = giữa
   màn). Kiểu hỏng thật, đã truy bằng bảng 2×2, không phải lỗi cài đặt.
3. **Tập kiểm không phải app-unseen** — 92% ứng dụng đã thấy lúc dạy. Mốc so với gpt-4o-mini hạ
   xuống tham khảo.
4. **B-infer thiệt thòi ở ba phương diện**: câu nhắc dài gấp 2,4 lần vùng đã dạy (85,7% bản ghi
   vượt 785 token) · danh sách bị cắt còn 40/72 phần tử · chỉ 14,1% phần tử có tên.
5. **Thước mù với lệch dưới ~63 px** — đo được *trỏ nhầm sang nút khác*, không đo được *trỏ hơi
   lệch trong cùng một nút*.
6. **Dấu hiệu phân biệt còn 24,1% không gỡ được**, và việc sửa nhãn **không phải bằng chứng**
   thành phần có tác dụng.
7. *"Do GUI Grounders Truly Understand UI Elements?"* (Findings EACL 2026): đổi cách diễn đạt
   làm bộ trỏ SOTA trượt tới 84% — đạn bắn thẳng vào thước executability, phải nêu trước.

---

## 6. Việc kế tiếp — trình tự cứng, không đảo

```
✅ 1. Commit bản đăng ký              (report/106, đã niêm phong)
✅ 2. Cổng A                          (ĐẠT 0,7%)
✅ 2b. Tiền trạm đường sinh câu       (4 phép, đều đạt — miễn phí)
▶️ 3. Huấn luyện S1 × 2 hạt giống → sinh câu → chấm đủ
   4. Tính MDE THẬT + cỡ nhiễu hạt giống = |S1(101) − S1(202)|
   5. KHOÁ ngưỡng đậu/rớt, ghi vào mục sửa đổi report/106 kèm ngày
   6. Phép thử TRẦN trên S1 (nối khai báo chuẩn vào đầu vào)
   7. Huấn luyện S2 × 2 hạt giống → chấm
   8. S2r, S2-nopoint, B-infer, mô hình gốc → chấm
   9. S3-pilot (nếu kịp viết mã)
  10. Chấm tay 100 câu (2 người) · không-gây-hại · demo tiếng Việt
  11. Đóng băng số, viết chương kết quả
```

**Bước 4 và 5 phải xong trước bước 7.** Đảo thì phải ghi lý do và coi kết quả là thăm dò.

### Chia việc giữa máy thuê và máy miễn phí

| Khâu | Chạy ở đâu | Vì sao |
|---|---|---|
| Dựng dữ liệu + OCR 64.500 ảnh | máy thuê | cần đĩa lớn và nhiều lõi CPU |
| Huấn luyện | máy thuê | không có cách nào khác |
| Sinh câu trên tập kiểm | máy thuê, ngay sau khi train | trọng số đã nằm sẵn trong bộ nhớ |
| **Chấm điểm** | **Kaggle miễn phí** | ~5 giờ/nhánh, hạn mức 30 giờ/tuần |

### Tiền

| khâu | tiền |
|---|---|
| dựng dữ liệu + OCR | $2 |
| S1 × 2 hạt giống | $17–28 |
| S2 × 2 hạt giống | $17–28 |
| S2r + S2-nopoint | $17–28 |
| sinh câu 7 lượt | $8 |
| B-infer + mô hình gốc + S3-pilot | $4 |
| đĩa 100 GB × 5–10 ngày + băng thông | $5–10 |
| **tổng** | **$70–108** |

Trần ngân sách 200 đô. Chấm điểm **không tính tiền** vì chạy trên Kaggle.

### Máy thuê — cấu hình đã chốt

vast.ai, **1 card A100** (40 GB là đủ), **on-demand** (không interruptible: mất máy là mất 67 GB
đã tải và 2 giờ OCR), đĩa **100 GB**, **≥16 lõi CPU**, download ≥500 Mbps, Max Duration ≥7 ngày,
độ tin cậy ≥0,98. Chuyển mã bằng `thesis_rented.zip` (2,7 MB, có sẵn kết quả OCR tập kiểm).

**Dùng đúng một hạng card cho cả sáu lượt** — cỡ lô hiệu dụng phải giữ y hệt, nếu không hiệu số
giữa các nhánh lẫn cả phần do cỡ lô khác nhau. `setup` tự kiểm số card và đĩa trống, khác 1 card
hoặc dưới 90 GB thì dừng hẳn.

**Đổi quyết định 9/8 chiều — chọn Colab Pro, không thuê vast.ai.** Lý do: đo được máy thật
(A100 **80 GB** · đĩa 235,7 GB · local-scratch 368 GB · RAM 167 GB · đốt **6,77 đơn vị/giờ**).
Hai con số trước đó của mình sai: tốc độ đốt không phải 15 mà là 6,77, và card là 80 GB chứ
không phải 40. Quy ra giá: **$0,677/giờ** (giá thường) so với $0,789 của vast.ai — Colab rẻ hơn
và card to gấp đôi. Runbook: `harness/run_on_colab.md`.

**Rủi ro còn lại của đường Colab, và cách chặn:** phiên chết giữa chừng → cho `output_dir` trỏ
vào Drive, LLaMA-Factory tự nối tiếp từ điểm lưu gần nhất · không chắc phiên nào cũng được A100
→ kiểm card ở đầu mỗi phiên, ra L4/T4 thì không train · cỡ lô giữ `4×4` thay vì `16×1` để chạy
được cả trên bản 40 GB nếu bị tụt.

**Lập luận cũ (đã lỗi thời, giữ để tra):** vì sao từng loại Colab (rà lại 9/8 sau đề xuất dùng Colab pay-as-you-go + VPN Thổ Nhĩ Kỳ): ngay
ở giá rẻ nhất nghe được ($6/100 unit), A100 đốt 15 unit/giờ → **$0,90/giờ**, vẫn **đắt hơn**
vast.ai $0,789 mà lại ít quyền kiểm soát hơn. Ba chỗ tiền không mua được: Colab chỉ hứa "L4 và
*thỉnh thoảng* A100" (cỡ lô không giữ được qua sáu lượt) · chạy nền 24 giờ là tính năng của
Pro+ chứ không phải pay-as-you-go, mà một lượt train mất 11-18 giờ · đĩa không chọn được. Lưu
dữ liệu ở R2/HF **không** giải được chỗ thứ ba: lúc train, 67 GB ảnh vẫn phải nằm trên đĩa máy
vì mỗi lượt duyệt đọc lại toàn bộ.

**Runbook: `harness/run_on_colab.md`** — 34 ô mã, **6 mốc dừng** để dán kết quả ra phân tích
trước khi tiêu tiếp, ô kiểm sau mỗi khâu, và bảng đối chiếu từng mục của `report/106` với chỗ nó
chạy. Bốn phép kiểm không nằm trong bản đăng ký nhưng bắt buộc: **rò rỉ tác vụ dạy↔kiểm** (chưa
ai kiểm ở quy mô 76 shard, sai là bỏ cả luận văn) · phủ OCR 100% · 9 bất biến bốn nhánh · **thử
nối tiếp sau khi cố ý giết tiến trình** (cơ chế chống mất phiên chưa từng chạy thử).

**Phần đúng của ý đó đã lấy:** `run_on_rented.sh save` gói lại thứ **đắt-dựng-rẻ-lưu** — kết quả
OCR (~120 MB, tốn 2-4 giờ CPU), nhãn khai báo, dữ liệu bốn nhánh — để `scp` về máy nhà. Mất máy
sau `setup` mà không có gói này là trả lại 2-4 giờ tiền máy cho đúng thứ đã có. `restore` bung
ở máy mới. **Không** gói 67 GB ảnh: tải lại từ HuggingFace nhanh hơn kéo từ bất cứ kho nào.

---

## 7. Luật đọc kết quả — đã viết TRƯỚC khi thấy số, không được sửa

Gọi **Δ = điểm S2 − điểm S1**, trung bình trên các hạt giống, KTC95 bằng wild cluster bootstrap
10.000 lần, gom cụm theo ứng dụng, tác vụ không gán được app thì mỗi tác vụ một cụm.

| Kết cục | Kết luận được phép viết |
|---|---|
| Δ vượt MDE, cận dưới > 0 | thành phần có tác dụng |
| Δ rơi vào **4–9 pp** | **báo chưa kết luận được** — kết luận đổi theo luật gộp cụm |
| Δ ≈ 0 | thành phần không có tác dụng, báo thẳng |
| Δ < 0 | báo kết quả âm, không giấu |

**Ba lát cắt duy nhất được báo**, định nghĩa trước khi chấm: toàn tập · lát khó (bước có phần tử
cùng vai trò gần nhất) · nhóm ứng dụng chưa thấy lúc dạy (67 bước).

**Cấm quy công cho "tính phân biệt" nếu chỉ có S2 > S1** — việc quy công phải đi qua S2-nopoint
và S2r. **Cấm dùng A′ (nguồn tên trong nhãn) giải thích hậu kỳ nếu S2 thắng** — nó nằm dưới mọi
kịch bản MDE.

---

## 8. Đã đăng ký nhưng chưa làm

| | Trạng thái |
|---|---|
| **S3-pilot** (khoản phạt lề, mức 2) | **chưa có mã** hàm mất mát. Cố ý — nằm sau cổng C. Nếu không kịp, phải khai là *đã đăng ký nhưng không chạy*, không được im lặng bỏ. Dữ liệu thì đã sửa xong 9/8: ô thứ tư của khai báo giả từng là hằng số `"phần tử hàng xóm"` ở 99,9% bản ghi, tách được mà không cần nhìn ảnh |
| Chấm tay 100 câu, 2 người | cần câu do mô hình sinh |
| Demo tiếng Việt định tính | cần mô hình đã huấn luyện |
| `report/100`, `101`, `102` | chưa khớp với thiết kế hiện tại (vẫn theo bản trước gia cố) |
| Bìa slide | còn trống tên GVHD và tên trường; `slides/*.tex` chưa khớp bản pptx |

---

## 9. Nguyên tắc làm việc đã rút ra — phần đáng viết vào chương phương pháp

Tới nay đã bắt được **35 lỗi loại "chạy vẫn trơn nhưng kết quả sai"** (bảng đầy đủ ở
`report/108` mục 8). Ba bài học lặp lại:

**Rà dấu vết trên đĩa, đừng hỏi trí nhớ.** `infer_branch.py` được cho là "đã sẵn sàng" suốt nhiều
ngày; một lệnh `find -name "preds_*.jsonl"` cho thấy nó chưa từng chạy lần nào.

**Bản vá cũng phải kiểm.** Bản vá bf16 viết hôm 7/8 hỏi `torch.cuda.is_bf16_supported()`, mà
PyTorch đời mới tính cả đường giả lập nên T4 trả `True` — bản vá tự vô hiệu hoá đúng ở chỗ nó
sinh ra để phục vụ, và vô hiệu **im lặng**.

**Số đẹp bất thường là dấu hiệu xấu.** Bảng đọc cổng A khoá trước ghi rõ: *dưới 0,5% là nghi lỗi
vì quá đẹp*. Cùng logic đã bắt được "AUC = 1,000" hồi tháng 7 (hằng đẳng thức, không phải phép
đo) và "sai số 8% cạnh" hồi tháng 8 (số đã lọc bỏ mọi lần trượt).

---

## 10. Tra ở đâu

| Cần gì | Mở file nào |
|---|---|
| Toàn cảnh + việc kế tiếp | **file này** |
| Thiết kế đã niêm phong, luật đọc kết quả, mọi sửa đổi có ngày | `report/106_DANG_KY_TRUOC.md` |
| Đã làm gì, số nào tin được tới đâu, 26 lỗi đã bắt | `report/108_DA_LAM_DUOC_GI.md` |
| Giới thiệu pipeline cho người chưa biết gì | `report/100_TONG_QUAN_PIPELINE.md` ⚠️ chưa cập nhật |
| Vì sao chốt thành phần này | `report/103_CHOT_THANH_PHAN.md` |
| Vì sao bác việc đảo sang OCR-trước | `report/107_DEBATE_NGUON_TEN.md` |
| Kết quả cổng A dạng thô | `ckpt/gate_A_raw.jsonl`, `ckpt/gate_A_ceiling.json` |
| Lệnh chạy trên máy thuê | `harness/run_on_rented.sh` |
| Chạy trên GPU miễn phí | `harness/run_on_free_gpu.md` |

**Khi hai file mâu thuẫn:** `report/106` (thiết kế) thắng về *phải làm gì*; `report/108` (sổ kê
khai) thắng về *đã đo được gì*; file này thắng về *đang ở đâu*.
