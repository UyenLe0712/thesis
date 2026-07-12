# SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM TỪ ẢNH GIAO DIỆN VÀ ĐÁNH GIÁ KHÔNG CẦN ĐÁP ÁN MẪU
## Tài liệu thuyết minh toàn diện — trình bày khoa học, giải thích tận gốc, có dữ liệu thật

> **Đối tượng đọc:** người chưa biết gì về AI **và** hội đồng phản biện. Mỗi thuật ngữ đều có định nghĩa
> bằng lời thường; mỗi công thức đều có ký hiệu **và** diễn giải. Dữ liệu minh hoạ trích trực tiếp từ
> `dataset_samples/`. Cập nhật 2026-07-03. *(Quy ước nội bộ: "một màn" = DG1, "nhiều màn" = DG2.)*

---

## TÓM TẮT

Luận văn nghiên cứu bài toán **sinh hướng dẫn sử dụng phần mềm theo từng bước** cho người đọc, từ đầu vào là một hoặc nhiều **ảnh chụp màn hình** kèm một **câu hỏi ngôn ngữ tự nhiên**, sử dụng mô hình ngôn ngữ thị giác (VLM). Hai khó khăn trung tâm là: (i) VLM thường **ảo giác** — tham chiếu tới phần tử giao diện không tồn tại; và (ii) **không có tập hướng dẫn chuẩn** do con người biên soạn để làm mốc đánh giá. Luận văn đề xuất hai đóng góp đặt ngang vai: (A) một **hệ thống sinh** gồm lớp trung-thực-hoá (đối chiếu tên nút với cây phân cấp giao diện, viết lại bước ảo giác thành mô tả) và khối sắp thứ tự màn; (B) một **phương pháp đánh giá** không cần đáp án mẫu và không tự chấm, được kiểm định bằng nhiễu loạn có kiểm soát. Toàn bộ thành phần đều dựa nguồn đã bình duyệt.

---

## MỤC LỤC
- **Chương 1** — Giới thiệu (bối cảnh, phát biểu bài toán, thách thức, đóng góp)
- **Chương 2** — Kiến thức nền & thuật ngữ
- **Chương 3** — Dữ liệu (3 bộ, có ví dụ thật + cấu trúc)
- **Chương 4** — Phương pháp I: hệ thống sinh (pipeline)
- **Chương 5** — Phương pháp II: đánh giá (metric)
- **Chương 6** — Ví dụ chạy đầu–cuối
- **Chương 7** — Tính hợp lệ & thiết kế thực nghiệm
- **Chương 8** — Kết quả sơ bộ
- **Chương 9** — Định vị & công trình liên quan (2026)
- **Chương 10** — Đóng góp, giới hạn, hướng phát triển
- **Phụ lục A** — Bảng thuật ngữ · **B** — Q&A giám khảo · **C** — Nguồn bình duyệt

---

# CHƯƠNG 1 — GIỚI THIỆU

## 1.1. Bối cảnh và động lực
Người dùng phần mềm thường xuyên gặp giao diện lạ và không biết thao tác. Một trợ lý đọc được ảnh màn hình và viết ra hướng dẫn từng bước sẽ hữu ích cho: tài liệu trợ giúp tự động, hướng dẫn người mới (onboarding), và đặc biệt **trợ năng cho người khiếm thị**. Công cụ làm được việc này là **VLM** (mô hình ngôn ngữ thị giác) — hệ thống AI nhận đầu vào gồm ảnh và văn bản, sinh ra văn bản.

> *Định nghĩa 1.1 (VLM).* **Mô hình ngôn ngữ thị giác** là mô hình học máy ánh xạ (ảnh, văn bản) → văn bản. Về bản chất nó **dự đoán chuỗi chữ có xác suất cao** dựa trên dữ liệu huấn luyện, chứ không "hiểu" theo nghĩa con người; chính cơ chế dự đoán này khiến nó đôi khi sinh ra nội dung nghe hợp lý nhưng **không có thật** (ảo giác).

## 1.2. Phát biểu bài toán (hình thức hoá)

> *Định nghĩa 1.2 (Hợp đồng vào–ra).*
> **Đầu vào:** một tập ảnh màn hình $S = \{s_1, s_2, \dots, s_N\}$ với $N \ge 1$ (khi $N \ge 2$, thứ tự các ảnh **bị xáo trộn**), cùng một câu hỏi $q$ bằng ngôn ngữ tự nhiên.
> **Đầu ra:** một hướng dẫn $T = (t_1, t_2, \dots, t_k)$ gồm $k$ bước có thứ tự, mỗi bước $t_i$ là một câu thao tác (ví dụ "Chọn nút OK").
> **Ràng buộc:** câu hỏi $q$ **không chứa tên nút**; tài nguyên chấm điểm **không được cung cấp** ở thì sinh (xem §3.4).
> Trường hợp $N=1$ gọi là **một màn**; $N \ge 2$ gọi là **nhiều màn** (đòi hỏi suy luận thứ tự).

## 1.3. Ba thách thức trung tâm
1. **Ảo giác giao diện** — VLM tham chiếu phần tử không tồn tại trên màn. Đây là dạng lỗi đặc thù, tần suất cao.
2. **Thiếu đáp án mẫu** — không tồn tại tập hướng dẫn chuẩn do người soạn cho mọi ứng dụng ⇒ không có mốc để so. *Đây là khó khăn khoa học trung tâm.*
3. **Suy luận thứ tự** — với nhiều ảnh xáo trộn, hệ phải tự khôi phục thứ tự đúng, và phải đo được năng lực đó.

## 1.4. Đóng góp
- **(A) Hệ thống sinh** giảm ảo giác (Chương 4).
- **(B) Phương pháp đánh giá** không-gold, không-tự-chấm (Chương 5), kiểm định bằng nhiễu loạn (Chương 7).
Hai đóng góp đặt **ngang vai có điều kiện** (§10.1).

---

# CHƯƠNG 2 — KIẾN THỨC NỀN & THUẬT NGỮ

## 2.1. Ảo giác (hallucination)
Hiện tượng mô hình sinh ra phần tử/khẳng định **không có thật** một cách tự tin. Trong bài toán này, biểu hiện là bước hướng dẫn nhắc tới một nút không tồn tại trên màn.

## 2.2. Cây phân cấp giao diện (View Hierarchy — VH)
Android duy trì sẵn một cấu trúc mô tả mọi phần tử đang hiển thị: tên (text/content-description), toạ độ khung, loại (nút/ô chữ/ảnh), thuộc tính (bấm được/nhập được). VH vốn phục vụ công nghệ trợ năng.
> *Định nghĩa 2.1 (VH).* Với màn $s$, $\text{VH}(s) = \{e_1, \dots, e_m\}$ là tập phần tử; mỗi $e_j$ có nhãn $\ell_j$ và khung $\text{box}_j = (l_j, t_j, r_j, b_j)$. **VH là "nhãn bạc"** — mốc tự động đủ tin, thay cho đáp án vàng do người soạn.

## 2.3. Bảng thuật ngữ rút gọn (đầy đủ ở Phụ lục A)
| Thuật ngữ | Nghĩa một dòng |
|---|---|
| Embedding / vector nghĩa | biến một chữ thành dãy số để so được nghĩa |
| Độ tương đồng (similarity) | số 0→1 đo hai chữ gần nghĩa cỡ nào |
| Ngưỡng τ | lằn ranh quyết "cùng nút" hay "bịa" |
| Fallback | thay bước bịa bằng mô tả chung |
| Copeland | xếp hạng bằng đếm số cặp thắng |
| τ thứ-tự-bộ-phận | điểm đo sắp đúng thứ tự (chỉ phạt cặp bắt buộc) |
| Step-SR | tỉ lệ bước làm đúng so quỹ đạo vàng |
| Perturbation | cố tình bơm lỗi đã biết để thử thước đo |
| Circularity | bẫy "vừa ra đề vừa chấm" |

---

# CHƯƠNG 3 — DỮ LIỆU

> 📎 **Bản CHI TIẾT CHUẨN LUẬN VĂN của chương này ở `report/44`** (nguồn gốc, venue, quy mô, giấy phép, cấu trúc, ví dụ thật, hạn chế — số liệu đã verify tận file + qua web). Dưới đây là bản tóm.

Luận văn dùng **3 bộ công khai**, vai cố định. Trước hết, hai khái niệm nền:
- **Bảng kê nút (VH)** — danh sách nút thật của màn (Định nghĩa 2.1); dùng làm mỏ neo thay đáp án.
- **Quỹ đạo vàng** — chuỗi thao tác đúng chuẩn có sẵn cho tác vụ nhiều bước.
> *Định nghĩa 3.1 (Quỹ đạo vàng).* $G = (a_1, \dots, a_n)$, mỗi $a_i$ là một thao tác chuẩn (loại + tham số). Ví dụ $a_i = \text{click}(x,y)$ hoặc $\text{scroll}(\text{down})$.

## 3.1. MobileViews — phần MỘT MÀN
**Mô tả:** kho **~1,2 triệu** cặp (ảnh 1 màn Android; VH của màn đó). **Không** có quỹ đạo vàng. **Trạng thái:** tiền ấn phẩm (preprint — chưa bình duyệt).

**Cấu trúc một mẫu thật.** Mỗi màn gồm ảnh `.jpg` + file `.viewhierarchy.json` chứa: `width`, `height`, `foreground_activity` (app đang mở), và danh sách `views`. Ví dụ thật màn `ccpacerandroidapp_s1` (app mạng-xã-hội chạy bộ) có **127 phần tử**; trích các nút bấm được:

| Nhãn $\ell$ | Loại | Bấm được | Khung $(l,t,r,b)$ |
|---|---|---|---|
| Following | TextView | ✓ | (113, 216, 310, 336) |
| Popular | TextView | ✓ | (432, 216, 647, 336) |
| Groups | TextView | ✓ | (794, 216, 942, 336) |
| Find My Friends | Button | ✓ | (0, 1420, −120, 1516) |
| **Image** | ImageView | ✓ | (30, 102, 114, 186) |

> **Quan sát quan trọng (dòng cuối).** Nút "Image" là **nút chỉ có biểu tượng, không nhãn văn bản**; VH đành ghi nhãn chung "Image". Đây là hiện thân của kết quả **>77% ứng dụng có nút thiếu nhãn** (Chen, ICSE 2020). Hệ quả: nếu AI gọi đúng **chức năng** nút này, bộ khớp vẫn **coi là ảo giác oan** vì không có nhãn để đối chiếu. → Luận văn **loại các nút nhãn-chung khỏi mẫu số** và báo độ trung thực **có điều kiện độ-phủ-nhãn** (§5.1, §7).

**Quy mô sử dụng:** từ tập nhỏ **90 màn / 18 app**, lọc rác còn **81 màn / 17 app**. Nhiều app ⇒ cho phép ước lượng sai số theo cụm-app (§7.4).

## 3.2. AndroidControl — phần NHIỀU MÀN
**Mô tả:** **15.283** quy trình nhiều bước, **833** app, trung bình **~5,5** bước/quy trình (percentile-95 = 13). Mỗi quy trình có **mục tiêu** + **quỹ đạo vàng**. **Đã bình duyệt NeurIPS 2024.**

**Một quy trình thật (`ep2_14851`).**
> **Mục tiêu:** *"Create a shortcut for me of The Queen's Gambit pdf file to the home screen on the Drive app."*

Quỹ đạo vàng $G$ gồm 5 thao tác:

| $i$ | $a_i$ (gold action) | Diễn giải |
|---|---|---|
| 1 | `click(1016, 866)` | chạm nút "⋮" cạnh file |
| 2 | `scroll(down)` | cuộn danh sách tuỳ chọn |
| 3 | `click(602, 2105)` | chọn "Add to Home screen" |
| 4 | `click(821, 2252)` | xác nhận "Add automatically" |
| 5 | `status(successful)` | báo hoàn tất |

**Cách sử dụng (thiết kế thực nghiệm):** xáo trộn các màn của quy trình → hệ tự khôi phục thứ tự (chấm bằng $\tau$, §5.2) → so từng thao tác đề xuất với quỹ đạo vàng (chấm bằng Step-SR). Khi xáo trộn, **che các tín hiệu rò rỉ** (đồng hồ, pin, huy hiệu) để buộc hệ suy luận thật.

## 3.3. ScreenSpot-v2 — ĐỐI CHỨNG
**Mô tả:** chuẩn "định vị nút từ mô tả". **Đã bình duyệt ICLR 2025.**
**Một item thật (`item1`):**
> **Câu lệnh:** *"invert the lens"* · **Loại:** icon · **Ảnh:** 1170×2532 · **Đáp án:** khung pixel **(965, 2105, 1110, 2258)**.

**Vai:** đối chứng độc lập cho thước "bấm đúng chỗ" — vì có đáp án toạ độ chuẩn và đã bình duyệt, dùng để kiểm bộ-trỏ thay vì lấy tâm khung (tránh tautology, §5.1).

## 3.4. Luật vàng chống rò rỉ
> *Nguyên tắc 3.1.* VH và quỹ đạo vàng **chỉ tham gia ở thì CHẤM**, tuyệt đối không cung cấp cho mô hình ở thì sinh/sắp. Câu hỏi không chứa tên nút.
> *Diễn giải:* như không cho thí sinh xem đáp án lúc làm bài — nếu lộ, mô hình "chép" và ta mất khả năng đo **mức tự ảo giác**. Vi phạm nguyên tắc này gọi là **rò rỉ dữ liệu (data leakage)**.

---

# CHƯƠNG 4 — PHƯƠNG PHÁP I: HỆ THỐNG SINH

## 4.1. Tổng quan
Một hệ thống thống nhất có **bộ định tuyến theo số ảnh**: $N=1$ → nhánh một màn; $N \ge 2$ → thêm **Stage-0** (sắp thứ tự) rồi đưa từng màn qua nhánh một màn.

```
Đầu vào (S, q)
   │
   ├─ N = 1 ──────────────► [Nhánh một màn]
   │
   └─ N ≥ 2 ► [Stage-0: sắp thứ tự] ► chuỗi đã sắp ► [Nhánh một màn] cho từng màn
```

## 4.2. Nhánh một màn (ba bước)

**Bước 1 — Sinh mù.** VLM nhận (ảnh, câu hỏi), **không** nhận VH, sinh bản nháp $T^{(0)}$ (baseline).

**Bước 2 — Đối chiếu ngữ nghĩa.** Với mỗi bước $t_i$ có nhắc nút tên $b_i$, tính độ khớp cao nhất với các nút thật:
> *Định nghĩa 4.1 (khớp/ảo giác).* Cho hàm embedding $\phi(\cdot)$ và độ tương đồng cosine $\text{sim}(u,v)$. Bước $t_i$ **khớp** nếu $\max_{e \in \text{VH}(s)} \text{sim}(\phi(b_i), \phi(\ell_e)) \ge \tau$; ngược lại là **ảo giác**.

*Giải thích embedding cho người mới:* $\phi$ biến một chữ thành **dãy số** (vài trăm chiều) sao cho chữ cùng nghĩa cho dãy số **gần nhau**; $\text{sim}$ đo độ gần đó, ra số **0→1**. Ví dụ $\text{sim}(\phi(\text{"Save"}), \phi(\text{"Lưu"})) \approx 0.7$; $\text{sim}(\phi(\text{"Menu"}), \cdot) \le 0.3$. Ngưỡng $\tau = 0.55$ là "lằn ranh": $\ge \tau$ → cùng nút, $< \tau$ → bịa.

**Bước 3 — Fallback.** Bước ảo giác được thay bằng **mô tả khái quát**, không suy đoán nút khác:
> `Bấm "Menu"` → `Tìm và bấm nút phù hợp để mở thêm tuỳ chọn`

**Mã giả:**
```
HÀM SinhMotMan(ảnh s, câu hỏi q):
    T ← VLM_sinh_mù(s, q)                  # bước 1
    cho mỗi bước t trong T:
        nếu t nhắc nút tên b:
            sim ← max{ cosine(φ(b), φ(ℓ_e)) : e ∈ VH(s) }
            nếu sim < τ:                    # bước 2: ảo giác
                t ← "Tìm và bấm nút phù hợp để …"   # bước 3: fallback
    trả về T
```

> *Định lý thiết kế (đối chứng thất bại).* Phương án thay ảo giác bằng **nút thật gần nhất** tạo **lỗi âm thầm (silent error)**: đo được trên 10 màn — ví dụ `✓→Navigate up`, `+→More options`, `ADD LOCATION→Copy project` (thay bằng nút có thật nhưng sai chức năng, người dùng bấm nhầm không hay). Do đó chốt "chỉ mô tả". Đây là **phát hiện thực nghiệm**, cơ sở khoa học của đóng góp A.

## 4.3. Nhánh nhiều màn (Stage-0)
Ba bước con.

**(a) So cặp.** Với $\binom{N}{2}$ cặp, hỏi VLM "màn nào trước?". *(Pairwise ranking — Qin, NAACL 2024.)*

**(b) Tổng hợp Copeland.** Điểm của màn $s_j$ = số cặp mà $s_j$ được đánh giá "đứng trước":
> *Định nghĩa 4.2 (Copeland).* $\text{cop}(s_j) = |\{k : s_j \prec s_k \text{ theo VLM}\}|$. Sắp theo $\text{cop}$ giảm dần; phá hoà tất định.
> *Ví dụ:* 3 màn, VLM cho $A\prec B, A\prec C, B\prec C$ ⇒ $\text{cop}(A)=2, \text{cop}(B)=1, \text{cop}(C)=0$ ⇒ thứ tự $A\to B\to C$.

**(c) Phá vòng.** Nếu phán đoán cặp tạo chu trình ($A\prec B\prec C\prec A$), loại tập cạnh nhỏ nhất để đồ thị phi chu trình. *(Minimum feedback arc set — Ailon, JACM 2008.)*

**Năm tín hiệu thứ tự (cue):** gating · nút điều hướng · biến thiên trạng thái · tiêu đề tiến trình · drill-down. Phân tích quy-kết dùng **stratification một-cue** (chỉ giữ cặp phân biệt bởi đúng một cue).

---

# CHƯƠNG 5 — PHƯƠNG PHÁP II: ĐÁNH GIÁ

## 5.1. Nhóm thước đo một màn

> *Định nghĩa 5.1 (Độ trung thực).* $\displaystyle \text{Faith} = 1 - \frac{|\{\text{bước ảo giác}\}|}{|\{\text{bước có nhắc nút}\}|}$.
> *Ví dụ:* 3 bước nhắc nút, 1 ảo giác ⇒ $\text{Faith}=1-\tfrac{1}{3}=67\%$.
> **Headline báo cáo = tỉ lệ ảo giác của bản gốc** $\approx \tfrac14$, **không** phải $\sim$100% sau fallback (trần do thiết kế). Con số kèm **điều kiện độ-phủ-nhãn VH** (do nút icon-only, §3.1).

> *Định nghĩa 5.2 (Độ đúng nhãn).* tỉ lệ bước gọi **đúng tên hiển thị** trên tổng bước trỏ nút thật. Ví dụ "Đồng ý" ≠ "OK" ⇒ đúng-chỗ nhưng sai-tên. (Thước tự định nghĩa — khai thẳng.)

> *Định nghĩa 5.3 (Bấm đúng chỗ, point-in-bbox).* Điểm bấm $(x,y)$ **trúng** nếu $l\le x\le r \wedge t\le y\le b$, dung sai $\le 14\%$ đường chéo màn (AITW, NeurIPS 2023).
> *Ví dụ thật:* ScreenSpot "invert the lens" → khung $(965,2105,1110,2258)$; bộ trỏ dự đoán $(1030,2180)$ → trúng.
> ⚠️ **Đã chuyển khỏi headline một-màn:** nếu lấy tâm khung nút đã khớp làm $(x,y)$ thì luôn trúng ⇒ tautology 100%. Chỉ dùng ở nhiều màn (có toạ độ vàng) hoặc đối chứng ScreenSpot-v2, và $(x,y)$ phải từ **bộ trỏ độc lập**.

## 5.2. Nhóm thước đo nhiều màn

> *Định nghĩa 5.4 ($\tau$ thứ-tự-bộ-phận).* Gọi $M$ là tập **cặp bắt buộc** (suy từ quỹ đạo vàng theo quy tắc nhân quả: màn B chỉ xuất hiện sau gold-action ở A ⇒ $(A,B)\in M$). $C$ = số cặp trong $M$ mà hệ xếp thuận chiều gold; $D$ = số cặp nghịch.
> $$\tau = \frac{C - D}{|M|} \in [-1, +1].$$
> *Ví dụ:* gold $A<B<C$, ba cặp đều bắt buộc. Hệ xếp $A,C,B$: (A,B) thuận, (A,C) thuận, (B,C) nghịch ⇒ $\tau=\tfrac{2-1}{3}=+0.33$.
> **Cặp tự do** (điền email rồi số điện thoại — trước sau đều đúng) **không** thuộc $M$ ⇒ đảo vẫn tính đúng. Nhãn $M$ suy từ GOLD, **không** hỏi mô hình (chống tự-chấm). *Tên đúng: Fagin 2006 + Lapata CL 2006, KHÔNG phải "Kendall τ-b".*

> *Định nghĩa 5.5 (Step-SR, teacher-forced).* $\displaystyle \text{Step-SR}=\frac{|\{\text{bước làm đúng}\}|}{|\{\text{bước quỹ đạo vàng}\}|}$; một bước "đúng" = **đúng loại thao tác** ∧ **lệch toạ độ $\le 14\%$**.
> *Ví dụ thật (quy trình Drive 5 bước):* hệ khớp 4/5 thao tác vàng ⇒ Step-SR $=80\%$. Đây là bằng chứng **đạt-mục-tiêu** (đúng-ý) mà nhánh một màn không có.

## 5.3. Định vị các thước
| Thước | Nhánh | Đo gì | Nguồn |
|---|---|---|---|
| Độ trung thực | một màn | không tham chiếu nút ma | ALOHa NAACL 2024 |
| Độ đúng nhãn | một màn | gọi đúng tên | tự định nghĩa |
| Bấm đúng chỗ | nhiều màn/ScreenSpot | trỏ trúng khung | SeeClick ACL 2024 |
| $\tau$ bộ phận | nhiều màn | sắp đúng thứ tự | Fagin 2006 |
| Step-SR | nhiều màn | làm tới đích | AndroidControl NeurIPS 2024 |

---

# CHƯƠNG 6 — VÍ DỤ CHẠY ĐẦU–CUỐI

## 6.1. Một màn (đầy đủ, có số)
**Đầu vào:** ảnh màn đặt giờ; $\text{VH}=\{$hour, minute, PM, OK, Cancel$\}$; câu hỏi *"Cần thao tác gì để đặt giờ 20:35 và xác nhận?"*.
**Bước 1 (sinh mù)** → $T^{(0)}$: `1. Chọn giờ và phút` · `2. Chọn "PM"` · `3. Bấm "Menu"`.
**Bước 2 (đối chiếu, $\tau=0.55$):**
| Bước | Nút gần nhất | sim | Kết luận |
|---|---|---|---|
| 1 | hour/minute | 0.85 | khớp |
| 2 | PM | 1.00 | khớp |
| 3 "Menu" | (không) | 0.30 | **ảo giác** |
**Bước 3 (fallback):** bước 3 → `Tìm và bấm nút phù hợp để mở thêm tuỳ chọn`.
**Chấm:** $\text{Faith}$ của bản gốc $=1-\tfrac13=67\%$ (báo cáo tỉ lệ ảo giác gốc $=33\%$ cho màn này); độ-đúng-nhãn: 2/2 nút thật gọi đúng $=100\%$; %fallback $=1/3$.

## 6.2. Nhiều màn (dùng quy trình Drive thật)
**Đầu vào:** 5 màn của quy trình "tạo lối tắt PDF" **xáo trộn**, mục tiêu đã cho.
**Stage-0:** so $\binom{5}{2}=10$ cặp → Copeland → giả sử ra thứ tự $\hat\pi$. Nếu $\hat\pi$ đảo 1 cặp bắt buộc so với gold ⇒ $\tau<1$ (ví dụ $\tau=+0.8$).
**Sinh + chấm:** đưa chuỗi đã sắp qua nhánh một màn; so từng thao tác với quỹ đạo vàng $G$ (click(1016,866), scroll(down), …) ⇒ Step-SR (ví dụ 4/5 $=80\%$).
**Kết quả một quy trình:** $(\tau=+0.8,\ \text{Step-SR}=80\%)$ — cặp số cho biết **vừa sắp gần đúng thứ tự, vừa gần tới đích**.

---

# CHƯƠNG 7 — TÍNH HỢP LỆ & THIẾT KẾ THỰC NGHIỆM

## 7.1. Chống vòng lặp luận lý (circularity)
> *Nguyên tắc 7.1.* Công cụ **QUYẾT** ảo giác (embedding A) ≠ công cụ **CHẤM** (embedding B khác họ) + **LLM-judge khác họ generator** + token-overlap = **ba cơ chế độc lập**. Headline = tỉ-lệ-ảo-giác gốc, không phải trị số sau fallback.
> *Cơ sở:* LLM tự thiên vị đầu ra cùng họ (Panickssery, NeurIPS 2024) ⇒ judge phải khác họ.

## 7.2. Nhiễu loạn có kiểm soát (perturbation)
Bơm lỗi **đã biết** vào hướng dẫn đúng, đo phản ứng thước đo:
- chèn nút ma ⇒ $\text{Faith}$ **phải giảm**;
- thay tên đồng nghĩa ("Save"→"Lưu") ⇒ $\text{Faith}$ **giữ**, đúng-nhãn giảm.
Đóng khung: perturbation chứng minh **độ nhạy = điều kiện cần**, chưa phải convergent validity. *(Sai, EMNLP 2021.)*

## 7.3. Xử lý VH không hoàn hảo
Đo **độ-phủ-nhãn** (tỉ lệ nút actionable có nhãn dùng được), loại nút nhãn-chung khỏi mẫu số, báo tỉ-lệ-ảo-giác **có điều kiện recall-VH**. *(Chen, ICSE 2020.)*

## 7.4. Thiết kế thống kê
- **Cluster bootstrap theo APP:** vì màn cùng app không độc lập, tái chọn mẫu theo cụm-app (10.000 lần) ⇒ tránh khoảng tin cậy hẹp giả tạo. Với ~17 cụm nhỏ, dùng **wild-cluster bootstrap-t** (Cameron–Gelbach–Miller 2008) và khai caveat.
- **Hiệu chỉnh đa kiểm định Holm**; **cố định hạt giống**.
- **Đăng ký trước (pre-registration):** ghi ngưỡng TRƯỚC khi xem kết quả; kết quả "không khác biệt" vẫn báo (đóng góp hợp lệ).

---

# CHƯƠNG 8 — KẾT QUẢ SƠ BỘ (trung thực)

Trên `gpt-4o-mini`, mẫu nhỏ:
- Tỉ lệ ảo giác bản gốc $\approx \tfrac14$ số bước;
- Lớp trung-thực-hoá nâng $\text{Faith}$ ở mọi ngưỡng; giá = **~19% bước** thành mô tả khái quát;
- Bộ chấm độc lập ~**95%** (không phải 100%) ⇒ không tautology.
> **Khai giới hạn:** mẫu nhỏ, một mô hình, **khoảng tin cậy còn chạm 0**. Bản chính (81 màn/17 app) chờ chạy; sẽ **thêm ≥1 mô hình frontier 2025-2026** để có đường-cong-ảo-giác theo đời mô hình.

---

# CHƯƠNG 9 — ĐỊNH VỊ & CÔNG TRÌNH LIÊN QUAN (2026)

Rà soát 2025-2026 cho thấy **không lỗi thời, không bị scoop**. Không công trình nào ghép đúng combo *sinh-hướng-dẫn-cho-người + neo-bằng-VH + đánh-giá-không-gold*.

| Công trình | Họ làm | Khác biệt của ta |
|---|---|---|
| FaithScore (Findings EMNLP 2024) | faithfulness reference-free cho VLM | họ để VLM tự soi ẢNH; ta đối chiếu **inventory VH có cấu trúc** (không tự-chấm) |
| AskEase (CHI 2026) | hướng dẫn cho screen-reader live | họ live-context + chấm người; ta ảnh+câu-hỏi, no-gold |
| LLM-as-Meta-Judge (2026) | validate metric không nhãn người | họ miền text; ta miền GUI + bơm-lỗi-độc-lập + trụ Sai EMNLP 2021 |

Bộ dữ liệu mới (GUI-Odyssey ICCV 2025, AMEX, ScreenSpot-Pro ACM MM 2025) đều là agent-control/element-detection — vai khác.

---

# CHƯƠNG 10 — ĐÓNG GÓP, GIỚI HẠN, HƯỚNG PHÁT TRIỂN

## 10.1. Hai đóng góp — ngang vai CÓ ĐIỀU KIỆN
(A) hệ thống sinh; (B) phương pháp đánh giá. Giữ ngang vai **với điều kiện** nhánh nhiều màn (Step-SR) ra số dương thật. Nếu chưa có, A vẫn vững nhờ ba chân: (1) đạt mục tiêu thiết kế; (2) đo được tỉ-lệ-ảo-giác + %fallback; (3) đối-chứng-thất-bại (silent error). **Không tuyên bố vô điều kiện khi chưa có số.**

## 10.2. Giới hạn (khai chủ động)
- Một màn chỉ đo *không-ảo-giác*, chưa đo *đúng-ý* (→ Step-SR ở nhiều màn).
- Faith ~100% sau fallback là trần thiết kế → báo tỉ-lệ-ảo-giác gốc.
- VH thiếu nhãn → báo "có điều kiện độ-phủ".
- Máy không-GPU → một mô hình, mẫu nhỏ (→ mở rộng + thêm frontier).
- Chưa có bảng số tiếng Việt → định lượng EN/ZH; VN minh hoạ + ~120 mẫu app Việt.

## 10.3. Hướng phát triển
Bộ trỏ grounding độc lập (GUI-Actor/UI-TARS); cổng đo sàn so-cặp (K-pair); đường-cong-ảo-giác đa mô hình; nhánh web.

---

# PHỤ LỤC A — BẢNG THUẬT NGỮ ĐẦY ĐỦ
| Thuật ngữ | Nói nôm na | Ví dụ |
|---|---|---|
| VLM | AI vừa nhìn ảnh vừa viết chữ | ChatGPT xem ảnh |
| Ảo giác | AI nói thứ không có thật | "bấm Cài đặt" khi không có |
| VH / bảng kê nút | danh sách nút thật của màn | {hour,minute,PM,OK,Cancel} |
| Quỹ đạo vàng | chuỗi thao tác đúng chuẩn | click(1016,866)→scroll(down)→… |
| Embedding | biến chữ thành dãy số so nghĩa | "Lưu"≈"Save" |
| Độ tương đồng | số 0→1 đo gần nghĩa | 0.7 = gần |
| Ngưỡng τ | lằn ranh cùng-nút/bịa | 0.55 |
| Matcher | bộ khớp tên nút | — |
| Fallback | thay bịa bằng mô tả chung | — |
| Silent error | sửa thành nút thật-nhưng-sai | Submit→Save |
| Copeland | xếp hạng bằng đếm trận thắng | — |
| Feedback arc set | phá vòng mâu thuẫn | — |
| Bounding box | khung chữ nhật của nút (l,t,r,b) | (100,850,200,900) |
| point-in-bbox | điểm bấm có trong khung không | — |
| τ bộ phận | điểm sắp đúng thứ tự | +0.33 |
| Step-SR | tỉ lệ bước làm đúng | 4/5=80% |
| Perturbation | bơm lỗi thử thước đo | — |
| Circularity | vừa ra đề vừa chấm | — |
| Cluster bootstrap | tính sai số theo cụm-app | — |
| Pre-registration | ghi ngưỡng trước khi xem kết quả | — |
| Peer-reviewed | bài đã được chuyên gia duyệt | ACL, NeurIPS |

# PHỤ LỤC B — Q&A GIÁM KHẢO (11 câu)
| Câu hỏi | Trả lời |
|---|---|
| "Kết quả đâu? ngang nhau?" | Ngang nhau **có điều kiện**; một-màn có số sơ bộ, nhiều-màn đang chạy; nếu chưa có số, A đứng bằng hệ chạy được + đối-chứng-thất-bại. |
| "Sao không đưa VH cho AI?" | Cần đo AI tự bịa bao nhiêu; đưa VH thì nó chép, hết đo được. |
| "VH thiếu nút → oan?" | Đo độ-phủ-nhãn, loại nút không tên (như "Image"), báo "có điều kiện". |
| "Matcher chính xác cỡ nào?" | 80–120 cặp gán tay → báo precision + κ, freeze ngưỡng; headline độc lập ngưỡng. |
| "Grounding tautology?" | Đã bỏ khỏi một-màn; chỉ dùng ở nhiều-màn/ScreenSpot với bộ trỏ độc lập. |
| ⭐ "AI đời cũ; AI 2026 hết bịa, hệ thừa?" | Báo bịa theo **nhiều đời AI kể cả mới nhất** — vẫn >0; on-device chỉ chạy AI nhỏ nên luôn cần. |
| "Chỉ ghép đồ có sẵn?" | Đóng góp ở **phát hiện thí nghiệm + cách đánh giá** — như G-Eval/FActScore/RAGAS. |
| "Long-context làm sắp-cặp thừa?" | So-cặp cho dấu-vết-kiểm-tra + bắt mâu thuẫn; VLM long-context "mù thời gian" (VECTOR 2025). |
| "Bị FaithScore/AskEase/Meta-Judge bao trùm?" | Không cái nào đối chiếu **VH có cấu trúc**; niche còn trống. |
| "Perturbation chưa đủ?" | Điều kiện cần; nâng graded-monotonicity; không lấy AI-tự-chấm làm cổng. |
| "Không có số tiếng Việt?" | Dataset chuẩn EN/ZH; VN minh hoạ + ~120 mẫu. |

# PHỤ LỤC C — NGUỒN BÌNH DUYỆT
ALOHa (NAACL 2024) · SeeClick (ACL 2024) · AITW (NeurIPS 2023) · AndroidControl (NeurIPS 2024) · ScreenSpot-v2/OS-Atlas (ICLR 2025) · Qin (NAACL 2024) · Dwork (WWW 2001) · Ailon (JACM 2008) · Fagin (SIAM J. Discrete Math 2006) · Lapata (Comput. Linguistics 2006) · Sai (EMNLP 2021) · Panickssery (NeurIPS 2024) · Chen (ICSE 2020) · Clark (ACL-IJCNLP 2021) · Chim (Comput. Linguistics 2025). Tiền lệ pipeline-gọn: G-Eval/FActScore/SelfCheckGPT (EMNLP 2023), RAGAS (EACL 2024), BERTScore (ICLR 2020).

*Nguồn đào sâu: `05` (kế hoạch) · `36` (thuyết minh) · `40` (phản biện) · `42` (độ mới 2026). Dữ liệu thật: `dataset_samples/`.*
