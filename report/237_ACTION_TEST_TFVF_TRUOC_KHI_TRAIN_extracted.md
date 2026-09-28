# 237 — ACTION: test TFVF trước khi train (28/9/2026)

Đọc file này một mình là đủ. Mục tiêu duy nhất của lượt kế là trả lời:

> Nếu vùng đích được nhấn mạnh trực tiếp trên ảnh, S1 có đọc tín hiệu đó và sinh câu tốt hơn không?

**Không train. Không A100. Không sửa luận văn. Không nạp localizer PATA.** Chạy trên Kaggle T4 bằng adapter và ảnh đã có trong dataset `fgrb-p1-bundle`.

Nếu GO không đạt, dừng TFVF và không train mô-đun. Nếu GO đạt, mới viết kế hoạch pilot có train.

## 1. Vì sao test này đứng trước mọi lượt train

TFVF ở file `236_MODULE_DUNG_TRUOC_S1_DONG_GOP_MO_HINH.md` dựa trên giả thuyết: thay ảnh trước vision encoder sẽ buộc tín hiệu vị trí đi tới câu, khác bridge PATA và cổng FGRB từng bị decoder bỏ qua.

Test rẻ nhất là dùng tọa độ vàng chỉ trong chẩn đoán để tạo ảnh focus hoàn hảo. Nếu ngay cả focus hoàn hảo không giúp S1 hoặc không khác focus sai, train localizer là vô ích.

Đây là Oracle dùng để quyết định, không phải hệ thống lúc chạy và không được đưa số vào luận văn.

## 2. Dữ liệu có sẵn

Kaggle dataset `fgrb-p1-bundle` đã có:

- `adapter_s1_seed101/`;
- 5.567 ảnh;
- `p1_val_rows.jsonl`, 1.567 bước;
- OCR đã lọc.

Dùng đúng 400 bước của C1, chọn bằng `random.Random(20260927).sample(val, 400)`. Trong đó đã đo có 249 bước click. Chỉ biến đổi ảnh của bước click vì các bước khác không có đích phần tử theo cùng nghĩa. GO chấm chính trên 249 bước click. In thêm bảng 400 bước với ảnh gốc giữ nguyên cho bước không click, chỉ để kiểm độ pha loãng.

Greedy ảnh gốc của đúng 400 bước đã có ở `runs/c1/c1_mau.jsonl`; dùng lại sau khi kiểm từng khóa và câu chuẩn khớp. Không gọi lại S1 cho chế độ ảnh gốc.

## 3. Bốn chế độ ảnh

Mọi chế độ giữ nguyên kích thước ảnh và lời nhắc. S1/101 đóng băng, sinh greedy với cùng `max_new_tokens=96`.

### O — ảnh gốc

Dùng câu greedy đã có từ C1.

### G — gold focus

Tọa độ tâm là điểm chạm vàng `((x,y))`. Tạo mặt nạ Gaussian:

\[
M(u,v)=0.35+0.65\exp\left[-\frac12\left(\frac{u-x}{0.18W}\right)^2-\frac12\left(\frac{v-y}{0.12H}\right)^2\right].
\]

Tạo ảnh:

\[
I_G=M\odot I+(1-M)\odot \operatorname{Blur}_{8}(I).
\]

Vùng đích giữ nét. Ngoài vùng đích vẫn còn ít nhất **35% ảnh gốc, không bị xóa**.

### F — false focus

Dùng đúng renderer và diện tích mặt nạ của G, nhưng dời tâm sang nửa màn hình đối diện:

\[
x_F=(x+0.5W)\bmod W,\qquad y_F=(y+0.5H)\bmod H.
\]

Đây là nhánh kiểm sàn. Nếu G không hơn F thì S1 không dùng đúng vị trí focus.

### C — center focus

Tâm cố định `((0.5W,0.5H))`, cùng renderer. Nhánh này kiểm việc làm nét trung tâm hoặc làm mờ nền có tự cho điểm hay không.

Không thử nhiều bán kính, nhiều blur hoặc nhiều mức sàn rồi chọn cái đẹp. Các hằng số trên được giữ cho toàn bộ 400 bước. Thay chúng sau khi thấy số là một thí nghiệm mới.

## 4. Script phải viết

Chỉ tạo hai file mã trong clone cho lượt chạy, rồi kết quả bàn giao cuối vẫn ghi ra ngoài clone:

1. `harness/tfvf_g0.py`
   - dùng cấu trúc nạp model và dựng prompt của `harness/c1_mau_s1.py`;
   - tự dò bundle như `harness/kaggle_c1_da_dang_s1.md`;
   - kiểm có đúng 1.567 val rows và adapter;
   - chọn đúng 400 bước seed `20260927`;
   - chỉ sinh ba chế độ G, F, C; ghi dần, nối tiếp được;
   - mỗi dòng ghi `episode_id`, `step_id`, `action_type`, `gold`, `gold_focus`, `false_focus`, `center_focus`;
   - in cấu hình thật, số ảnh và hash danh sách 400 khóa;
   - thử `--n 5` trước lượt đầy đủ.

2. `harness/tfvf_g0_doc.py`
   - đọc kết quả mới và `runs/c1/c1_mau.jsonl`;
   - assert 400 khóa và câu chuẩn khớp tuyệt đối;
   - chấm BLEU-1..4, METEOR, ROUGE-L, CIDEr-D, SPICE bằng PTBTokenizer và COCO Captions;
   - in bảng cho 249 click và bảng 400 bước;
   - đếm tỉ lệ câu G khác O, G khác F, G khác C;
   - in điều kiện đạt/không đạt bên dưới.

Hai script chỉ là phương tiện. Kết quả duy nhất của lượt phải ghi:

`/Users/P836901/Documents/Self-learning/thesis/238_KET_QUA_G0_TFVF.md`

File 238 phải tự chứa mã nguồn hai script ở phụ lục, vì script nằm trong clone dùng một lần.

## 5. Điều kiện GO

Đọc trên **249 bước click**. G0 đạt khi đồng thời:

1. **Kênh có tác dụng:** câu G khác câu O ở ít nhất 10% bước.
2. **Đúng vị trí tốt hơn sai vị trí:** G cao hơn F ở ít nhất hai trong ba thước BLEU-4, CIDEr-D, SPICE; CIDEr-D của G cao hơn F ít nhất 3 điểm.
3. **Định vị học được có ý nghĩa hơn prior:** G cao hơn C ở ít nhất hai trong ba thước.
4. **Focus hoàn hảo có ích:** G không thấp hơn O ở cả ba thước và cao hơn O ở ít nhất hai trong ba thước.

Điều 4 là điều quyết định. S1 chưa train trên ảnh focus nên đây là tiêu chí chặt, nhưng mục tiêu của G0 là tránh tiêu thêm một lượt train cho một kênh chưa cho dấu hiệu lợi ích.

Không đếm BLEU-1, BLEU-2, BLEU-3 thành ba thước độc lập.

### Cách đọc bốn kết cục

| kết quả | phán quyết |
|---|---|
| đạt cả 1–4 | TFVF phù hợp; mới được thiết kế pilot có train |
| trượt 1 | S1 gần như không phản ứng với renderer; dừng |
| đạt 1 nhưng trượt 2 hoặc 3 | S1 phản ứng với biến đổi ảnh nhưng không theo đúng vị trí; dừng |
| đạt 1–3 nhưng trượt 4 | focus chứa tín hiệu nhưng distribution shift làm hại S1; dừng theo tiêu chí tiết kiệm, không tự mở lượt SFT để cứu |

Không nới điều kiện sau khi thấy số.

## 6. Chi phí ước lượng

- GPU: Kaggle T4 ×1, 0 đồng.
- Model chỉ nạp một lần.
- 747 lượt greedy cho ba chế độ trên 249 bước click; bước không click tái dùng câu O.
- C1 từng sinh 1 greedy + 8 mẫu cho 400 bước trong 142,9 phút. G0 ít chuỗi hơn nhưng xử lý ba ảnh; dự kiến khoảng 1–2 giờ T4. Đây là ước lượng, script phải in thời gian thực mỗi 20 bước.
- Chấm COCO chạy CPU. METEOR và SPICE cần Java 8.

Không dùng A100. Không tải ảnh train 12 GB. Không train lại Qwen.

## 7. Lệnh Kaggle dự kiến

Notebook Add Data:

- `fgrb-p1-bundle`;
- dataset script mới chứa `tfvf_g0.py` và các phụ thuộc `build_branch_data.py`.

Sau khi tự dò `BUNDLE`:

```bash
python /kaggle/working/tfvf_g0.py \
  --bundle "$BUNDLE" \
  --out /kaggle/working/tfvf_g0_thu.jsonl \
  --n 5
```

Kiểm 5 dòng có đủ G/F/C, ảnh mở được, câu không rỗng hàng loạt. Sau đó:

```bash
rm -f /kaggle/working/tfvf_g0.jsonl
python /kaggle/working/tfvf_g0.py \
  --bundle "$BUNDLE" \
  --out /kaggle/working/tfvf_g0.jsonl \
  --n 400
```

Tải `tfvf_g0.jsonl` về máy, đặt tạm ngoài clone, rồi chạy script đọc kết quả bằng CPU.

## 8. Việc chat thực thi không được tự làm

- Không chạy Stage A hoặc Stage B của TFVF.
- Không sửa hằng số renderer sau khi thấy số.
- Không dùng tọa độ vàng như đầu vào hệ thống thật.
- Không báo số val G0 trong luận văn.
- Không sửa `thesis/`.

> Ghi chú: phần cuối mục 8 trong ảnh nguồn bị che/cắt nên có thể còn nội dung chưa được trích xuất.
