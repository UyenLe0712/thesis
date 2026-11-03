# 326. Bàn giao lưới so sánh RL (ghi 1/11/2026, 22:00 giờ VN)

Đọc tệp này trước khi làm tiếp phần so sánh GRPO + SPICE. Trạng thái Kaggle dưới đây là của thời điểm ghi, phải kiểm lại bằng lệnh ở mục 3.

## 1. Vì sao có việc này

Thầy chưa cho bảo vệ (1/11), tốt nghiệp dời sang đợt 3/2027. Phải trả lời được bằng số:
1. So GRPO với các thuật toán cùng họ RL.
2. So SPICE với các độ đo khác làm phần thưởng.
3. Nếu GRPO + SPICE vẫn tốt nhất thì giải thích vì sao trên AndroidControl. Kèm câu hỏi về ACE: vì sao chọn, đã khảo sát chưa.

Chỉ đạo của user:
- Chưa sửa luận văn, làm hết rồi mới sửa. Kết quả có số ghi vào `report/320`.
- So càng nhiều phương pháp càng tốt: RL nói chung, cả cổ điển, không chỉ RL cho GUI.
- Kaggle miễn phí thì cứ chạy. Việc cần Colab mà quan trọng thì ghi lại, user quyết sau, không tự chạy Colab.
- Đừng sợ tốn tính toán. Tạm bỏ chạy nhiều hạt giống, làm sau; hiện chỉ hạt 101.
- Không chạy lỗi, mỗi lượt phải chứng minh được điều gì đó.

## 2. Tài liệu cần đọc

| Cần gì | Mở |
|---|---|
| Kế hoạch, dự đoán ghi trước, nhật ký chạy, danh sách lượt | `report/323_…` §8 (action), §9 (dự đoán, số 0 GPU), §10 (nhật ký), §11–12 (danh sách) |
| **Thứ tự chạy theo độ phổ biến và danh sách Colab (mới nhất, thắng mục 4 và 5 về thứ tự)** | `report/329_XEP_HANG_PHO_BIEN_RL_VA_THU_TU_CHAY_1_11.md` |
| Đánh giá GRPO + SPICE: điểm yếu, giả thuyết, câu trả lời theo kết quả lưới, script tái lập ở `runs/danh_gia_328/` | `report/328_DANH_GIA_GRPO_SPICE_VA_THUYET_PHUC_1_11.md` |
| Khảo sát độ đo thay SPICE: độ phổ biến, số đối đầu, debate, câu trả lời cho thầy, lượt nên thêm. Tái lập ở `runs/khao_sat_do_do_330/` | `report/330_KHAO_SAT_DO_DO_THAY_SPICE_1_11.md` |
| Đánh giá ACE: nên so với gì, điểm yếu, đề xuất hạ vai trò (chờ user quyết). Kết quả thô ở `runs/danh_gia_327/`, script chưa còn | `report/327_DANH_GIA_ACE_SO_SANH_VA_THUYET_PHUC_1_11.md` |
| Khảo sát 153 bài và bảng lượt chạy đầy đủ: máy, trạng thái mã, cách viết kết quả, câu cấm viết | `report/reports/Baseline RL so với GRPO.md` |
| Ghi chú gốc của khảo sát, bốn nhóm | `report/research_notes/Baseline RL so với GRPO/` |

Các tệp trên và mã mới **chưa commit**. Chỉ commit khi user cho phép trong chính lượt đó.

## 3. Trạng thái Kaggle

**Cập nhật 3/11, 06:15 (thắng các khối bên dưới).** Ba kernel 2/11 đã xong, số ở `report/320` mục 14, tệp ở `runs/luoi/test_2_11/` và `runs/luoi/lo3/`. Không còn phiên chat nào khác chạy trên máy lúc kiểm.
- Chấm đủ test: SCST + SPICE 60,54 · GRPO + METEOR 60,27 · GRPO + ROUGE-L 60,63. GRPO + CIDEr-D chạm trần 5 h ở lượt đầu; chấm nốt 3/11, đủ 4.463 bước, 60,27.
- `luoi-t2-3`: `sft:spice:101` đủ 500 bước (13,4 s/bước, 10,94 GiB), chưa chấm test. `grpo:spice:101` (A/A) dừng ở trần, khoảng bước 183, điểm lưu cuối 175.
- Độ đo văn bản của bốn lượt xong 3/11 (`trangphngngc/chu-luoi-2-11-cpu`, số ở `report/320` mục 14.4). Không còn kernel nào chạy.
- Chưa giải thích được: GRPO + CIDEr-D thấp hơn ck500 ngay trên CIDEr-D (−5,53, KTC loại 0). Công thức thưởng khớp pycocoevalcap, chỉ khác df và cách tách từ (`report/320` mục 14.4).
- Sau 7/11, theo thứ tự: test SFT tiếp · test RLOO, REINFORCE · nối tiếp A/A.

**Cập nhật 2/11, 19:00. Hai phiên chat cùng làm kho này, phân vai đã chốt; không đẩy thêm khi chưa báo phiên kia.** User đã đồng ý chạy từ từ, phần còn lại sau khi hạn mức làm mới 7/11.

| Tài khoản | Kernel | Việc | Phiên phụ trách |
|---|---|---|---|
| `trang` | `luoi-test-t-1`, đẩy 18:55 | Sinh câu + chấm test METEOR, ROUGE-L, trần 8,7 h | thesis-49 |
| `trang2` | `luoi-t2-3`, đẩy 18:55 | `grpo:spice:101` (A/A) + `sft:spice:101`, trần 7,5 h; A/A dự kiến phải nối tiếp | thesis-49 |
| `uyenle` | `luoi-test-u-1` (`luoi-u-3` đã xong, SCST đủ 500 bước) | Sinh câu + chấm test SCST, CIDEr-D, trần 5,0 h; nếu chạm trần thì nối tiếp sau 7/11 | thesis-72 |

Cả sáu lượt lô đầu đã đủ 500 bước (SCST xong ở `luoi-u-3`). Test RLOO, REINFORCE chờ sau 7/11; `trang2` còn thiếu dataset `thesis-score` và `grpo-spice-script`. Notebook test chuẩn là bản trong `_bundles/luoi/k_luoi-test-t-1/`; `_bundles/luoi/make_test_nb.py` hiện là bản của phiên kia, không dùng, khi dùng lại phải dựng từ notebook và đổi `shutil.copy(p, W)` thành `copyfile` như đã ghi trong tin nhắn cho thesis-72. **User dặn:** việc không cần GPU (độ đo văn bản, đọc từ raw, đo hình thức câu) phải chạy kernel CPU trên Kaggle.

**Cập nhật 2/11, 07:40:** lô 1 dừng đúng trần 11 h (mã thoát −15), không có dòng lỗi, kể cả hai lượt SPICE song song. Đã lưu tới: `scst:spice` 225 · `grpo:cider` 275 · `grpo:meteor` 250 · `grpo:rougel` 250 · `rloo:spice` 250 · `reinforce:spice` 250. Lúc 07:41 đã đẩy **commit 2** (phiên bản 2; phiên bản 1 lúc 07:38 dừng ngay ở phép kiểm vì output kernel trước cũng có `grpo_luoi.py`, đã sửa `make_nb.py`, chưa train nên không mất gì): `uyenle0712/luoi-u-2`, `trangphngngc/luoi-t-2`, `trangphuongngoc/luoi-t2-2`, tự dừng khoảng 18:45 ngày 2/11. SCST chậm hơn (163 s/bước) nên [suy] cần commit 3 ngắn, và lúc đó phải tính hạn mức còn lại vì mới làm mới 7/11. Log lô 1: `runs/luoi/lo1/luoi-*/`. Số thưởng trong log là số train, không trích.

Output đầy đủ của lô 1 ở `runs/luoi/lo1/{u1,t1,t21}`: 60 điểm lưu, 15 GB, đã kiểm đủ tệp sau khi tải lại (2/11 phiên này lỡ xoá lúc đang tải). Ba thư mục này và tệp jar trong `_bundles/luoi/ds*/` đã vào `.gitignore`.

Bảng dưới là lô 1, giữ để tra tên lượt.

Lô 1 đẩy lúc 20:04 ngày 1/11, lúc ghi tệp này cả ba kernel vẫn RUNNING. Mỗi commit tự dừng ở 11 h, tức khoảng 07:00 ngày 2/11.

| Tài khoản `kg` | Kernel | Hai lượt |
|---|---|---|
| `uyenle` | `uyenle0712/luoi-u-1` | `scst:spice:101` · `grpo:cider:101` |
| `trang` | `trangphngngc/luoi-t-1` | `grpo:meteor:101` · `grpo:rougel:101` |
| `trang2` | `trangphuongngoc/luoi-t2-1` | `rloo:spice:101` · `reinforce:spice:101` |

Kiểm trạng thái: `kg uyenle kernels status uyenle0712/luoi-u-1`. Log và output chỉ có sau khi kernel xong. Đồng hồ WSL chạy UTC, đọc giờ bằng `TZ='Asia/Ho_Chi_Minh' date`.

Hạn mức: 30 h GPU mỗi tuần mỗi tài khoản, làm mới 7/11. Mỗi phiên T4×2 chạy hai lượt, mỗi GPU một lượt. Probe đo 158,1 s/bước (SCST) và 149,1 s/bước (GRPO + CIDEr-D), 12,71 GiB, nên [suy] mỗi commit được khoảng 250 bước và SCST có thể cần commit thứ ba ngắn.

## 4. Việc kế, theo thứ tự

1. **(Đã làm cho lô 1 và commit 2)** **Khi lô dừng:** tải output, kiểm log của từng lượt: mã thoát, `[xong]`, `[câu nhắc] trùng`, `Traceback`, `kl`. Riêng `trangphuongngoc/luoi-t2-1` xem kỹ lỗi SPICE: hai lượt SPICE song song dùng chung thư mục cache LMDB của `pycocoevalcap` (`Spice().compute_score`), trường hợp probe chưa thử. Lỗi thì đừng ghép hai lượt SPICE vào một phiên hoặc tách cache. Lượt nối tiếp phải có dòng `[nạp default]` với x > 0 (lỗi 30/9 từng làm policy về lại S1).
2. **Đẩy commit 2,** ví dụ:
   ```
   cd _bundles/luoi
   python3 make_nb.py uyenle0712 luoi-u-2 train scst:spice:101 grpo:cider:101 uyenle0712/luoi-u-1
   kg uyenle kernels push -p k_luoi-u-2 --accelerator NvidiaTeslaT4
   ```
   Hai tài khoản kia làm tương tự. Trước khi đẩy, tính hạn mức còn lại của tuần: `CAT` trong `make_nb.py` là 11 h, [suy] phiên hết hạn mức giữa chừng có thể mất output, nên hạ `CAT` nếu còn dưới 11 h.
3. **Khi đủ 500 bước:** sinh câu test và chấm UGround, độ đo văn bản, rồi ghi số vào `report/320`. Gói chấm chung ở mục "Danh sách lượt chạy đề xuất" của báo cáo khảo sát.
4. **Lượt mới theo ưu tiên:** SFT tiếp · SCST + CIDEr-D · PPO · đo hình thức câu · các lượt cổ điển mã đã xong · phần còn lại.
5. **Việc khác còn lại:** H1, H3, H4, H5 từ log · khảo sát Z1, Z3–Z5 (`report/324`, `report/325`, chưa có) · trình thầy khoảng 1/2027 · user tự kiểm hạn nộp đợt 3/2027 · slide oral SOICT 4–5/12.

### Việc thêm sau hai báo cáo đánh giá (1/11 khuya)

Từ `report/328` (chi tiết §5, §7), đều Kaggle:
- **Lượt tham chiếu `grpo:spice:101` qua `grpo_luoi.py` (T1, lượt A/A)** và **GRPO bỏ chia std**: chạy trước các lượt còn lại của đợt 1.
- **T2:** ck500/202 chấm UI-Venus, Phi-4. **T3:** bước không chạm cho ck500/202, xao101. Rẻ, nên làm sớm.
- **T4:** ACU cho bước không chạm và các nhánh còn thiếu. **T5:** GRPO + thưởng chỉ đúng loại thao tác (chỉ để giải thích). **T6:** SPICE không phạt, chỉ phạt độ dài. **T7:** xuất phát từ S1/202 (thuộc phần nhiều hạt đang hoãn).

Từ `report/327` §6, về ACE, xếp sau lô lưới RL:
- **User chưa quyết:** có hạ ACE xuống phần mở rộng không; có chấm tay mù 100 cặp không.
- **0 GPU:** viết lại script vào `harness/` (script cũ bị ghi đè), đối chiếu số, ghi `runs/ace_ablation/` trước khi đưa số vào `report/320`.
- **T4:** exec của các mốc NN (~2 h) · `cont` + R3 (~3,2 h) · bước không chạm của ACE (~2,1 h) · ACE dưới lịch sử tự sinh (~2 h) · hạt thứ hai của `ra_k4` (~10,7 h).

Từ `report/330` §7–8, trục phần thưởng: BLEU-4 · SPIDEr · BERTScore · **BCMR** · **SPICE có cổng loại thao tác** · **tên phần tử + loại thao tác** · chrF · CIDEr-R (chỉ khi CIDEr-D không thua SPICE). Ba hàng in đậm phải viết mã. Người nghe Phi-4 từ S1 phải probe T4×2. **User quyết sau:** Phi-4 nếu T4 tràn · thưởng bằng UI-Venus · LLM giám khảo.

Cách đọc lưới đã ghi trước ở `report/320` §13. Các câu cần sửa trong luận văn ở `report/328` §7 và `report/327` §3.6, sửa một lượt sau cùng.

## 5. Danh sách lượt (bản đầy đủ ở báo cáo khảo sát)

- **Đang chạy (6):** SCST, RLOO, REINFORCE EMA + SPICE · GRPO + CIDEr-D, METEOR, ROUGE-L.
- **Kế tiếp, mã xong (5):** GRPO bỏ chia std (mã `drgrpo`, chưa phải Dr. GRPO đủ) · GRPO + BLEU-4, chrF, SPIDEr, BERTScore (BERTScore chưa probe).
- **Ưu tiên một:** SFT tiếp · SCST + CIDEr-D · PPO λ=1,0 và 0,95 · DPO trực tuyến và ngoại tuyến từ S1 · RFT một vòng và online từ S1 · DAPO lõi (β=0) · Dr. GRPO đủ · GRPO gộp theo câu · đo hình thức câu (không train).
- **Ưu tiên hai:** B1–B15 (DAPO đủ, chuẩn hoá theo lô, Vanilla PG, A2C, PPO critic đủ cỡ, ORPO, DPO bán trực tuyến, GPG, xuất phát từ Base, BCMR, G=4/16, μ=2, GSPO, Clip-Higher).
- **Cổ điển, mã xong:** `vanilla` · `rft` · `cem` · `awr` · `raml` · `rank` · `mad` (`vanilla`, `rft`, `mad` chính là B3, online RFT, C1).
- **Cổ điển, phải viết mã, chạy Kaggle:** MRT · softmax PG · MIXER rút gọn · trộn RL + CE · SeqGAN · Quark · ES · A2C.
- **User quyết sau:** PPO critic đủ cỡ (quan trọng cao) · TRPO · ILQL · SAC rời rạc.
- **Không áp dụng được:** TD3, DDPG.

Khối lượng [suy]: khoảng 50 lượt, 795 giờ hạn mức, chừng 9 tuần trên ba tài khoản, tới khoảng đầu 1/2027.

## 6. Trạng thái mã

| Tệp | Tình trạng |
|---|---|
| `harness/grpo_luoi.py`, bản trong `_bundles/luoi/ds/` | md5 `92d0a9bc…`. **Không sửa trước khi xong lô 1**: notebook kiểm md5 và dừng nếu lệch |
| `harness/grpo_spice.py` | Không sửa, md5 `8489108f…`, ck500 tái lập bằng tệp này |
| `harness/grpo_codien.py` (mới) | 7 nhánh cổ điển + cờ `--loss-type`, `--scale-rewards`, `--mu`, `--is-level`, `--eps-high`; cho phép SCST + CIDEr-D. Chạy thử CPU đạt. **Chưa probe T4** |
| `harness/grpo_ppo.py` (mới) | PPO và A2C: đầu giá trị nhỏ tách gradient, GAE, lợi thế theo token, lưu và nạp đầu giá trị khi nối tiếp. Selftest GAE và CPU đạt, kể cả nối tiếp. **Đã probe T4 3/11, số ở `report/329` mục 4:** A2C 187 s/bước, PPO μ = 2 299 s/lô sinh, không tràn bộ nhớ, `clip_ratio/region_mean` = 0 cả 12 bước (mới hai dòng ở lr đầy đủ). ppo cần `steps=1000` để giữ 1.000 câu nhắc |
| `harness/sft_tiep.py` (mới) | SFT tiếp từ S1: 500 bước, 2 câu nhắc mỗi bước. CPU đạt, nối tiếp cho đúng cùng loss. **Chưa probe T4** |
| `harness/hinh_thuc_cau.py`, `harness/ace_doi_chieu.py` (mới) | Đã chạy, kết quả `runs/hinh_thuc_cau/ket_qua.json`, `runs/ace_ablation/doi_chieu_327.json` |
| `_bundles/luoi/make_nb.py` | Đã nhận nhánh mới, cú pháp `algo:reward:seed[:k=v,…,tag=…]`, ví dụ `ppo:spice:101:mu=2,lam=0.95,steps=1000,tag=l95` · `sft:spice:101` · `grpo:spice:101:beta=0,loss=dr_grpo,scale=none,tag=drg`. Dừng ngay nếu có kernel trước mà không thấy điểm lưu. Tệp mới đã chép vào `ds/`, nhưng **dataset `grpo-luoi-script` của từng tài khoản chưa cập nhật**: phải đẩy phiên bản mới trước khi chạy nhánh mới |
| TRL 0.29.1 có sẵn | `loss_type="grpo"` hoặc `"dr_grpo"` · `scale_rewards="batch"` · `importance_sampling_level="sequence"` (GSPO) · `epsilon_high` (Clip-Higher). Không có dynamic sampling |
| Sửa từ mã cũ | SFT tiếp: `_scripts/314/ds_raft314/ra_train.py` (đang nối từ ck500, phải đổi thành S1 + LoRA mới, lịch lr đang cosine) · DPO: `_scripts/314/ga313/ga_dpo.py` (dòng 221 `assert` đòi L4/A100) · RFT: `raft_mau.py`, `raft_chon.py` |

Chạy thử CPU: `/tmp/…/scratchpad/thu_cd.py` nằm ở scratchpad của phiên này và có thể mất. Nó dùng `trl-internal-testing/tiny-Qwen2_5_VLForConditionalGeneration`, chạy `GL.train` với 2 bước. Java ở `~/.jdk/jdk8u504-b01/bin`, nhớ thêm vào PATH.

## 7. Bắt buộc khai và không được viết

- ck500 dùng `loss_type="dapo"`, không phải GRPO gộp theo câu.
- Với `num_iterations=1` phép clip không hoạt động: `clip_ratio/region_mean` và `completions/clipped_ratio` bằng 0 ở mọi dòng log đã kiểm (`runs/grpo_spice/train_c1.log`, `train_c3.log`). Vì vậy phần clip của DAPO, GSPO, PPO không được kiểm tra trong lưới hiện tại.
- Dùng đúng tên: mã `drgrpo` là "GRPO bỏ chia std"; `awr`, `raml` là "kiểu AWR", "kiểu RAML"; `rank` không phải ES đầy đủ.
- Liu viết PG-SPICE sinh câu sai ngữ pháp, lặp cụm rồi bỏ cấu hình này, nên phải đo hình thức câu.
- Một hạt giống: hai hạt ck500 chênh 0,72 exec. "Hơn" nghĩa là KTC ghép cặp loại 0 và |Δ exec| ≥ 1, kèm nhãn một hạt giống; +1,55 vẫn dưới MDE 2,11.
- Khoảng 50 phép so nên phải hiệu chỉnh Holm, in cả p gốc lẫn p đã hiệu chỉnh.
- Báo mọi lượt vô điều kiện. **Không được hứa trước GRPO + SPICE đứng đầu**; nếu không đứng đầu thì viết đúng như số đo. Báo cáo khảo sát có sẵn cách viết.
- Số val chỉ để giải thích, không trích. "GA-DPO" là tên nội bộ của dự án, không phải phương pháp công bố.
- Mẫu 153 bài là mẫu có chủ đích, gieo một phần từ tên GRPO: viết "trong mẫu N bài", không viết "ngành dùng".
- Số trích từ các bài chưa đối chiếu bản đăng. Trước khi vào luận văn phải mở lại nguồn và kiểm venue (danh sách chưa kiểm nằm cuối báo cáo khảo sát; còn mâu thuẫn ở hàng RLOO/RAFT k=2).
