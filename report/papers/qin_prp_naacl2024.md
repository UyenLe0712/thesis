# Large Language Models are Effective Text Rankers with Pairwise Ranking Prompting (Qin et al.)

- **Link:** https://aclanthology.org/2024.findings-naacl.97/
- **Venue/năm:** Findings of NAACL 2024 — ✔ đã xác minh (report/45, nguồn 8)
- **Vai trong luận văn:** trụ cho lựa chọn **so-CẶP thay vì listwise một-shot** ở Stage-0 — §4.3, §4.4.

## Paper này nói gì (cho người mới)
Muốn LLM **xếp hạng** một danh sách, có 3 kiểu hỏi: chấm từng cái (pointwise), xếp cả dãy một lần (listwise), hoặc **so từng cặp** "cái nào hơn?" (pairwise). Bài chỉ ra LLM **không nắm tốt** pointwise/listwise, nên **so-cặp cho kết quả xếp hạng tốt hơn**. Đáng chú ý: một mô hình mở 20B dùng so-cặp **sánh ngang GPT-4** (lớn gấp ~50 lần) và **vượt listwise >10%**.

## Điểm cần biết
- **Pairwise > listwise — nhưng CÓ ĐIỀU KIỆN** (sắc thái quan trọng, R-07): lợi thế này rõ **ở LLM tầm-trung**; trên **model rất mạnh**, listwise (RankGPT/RankZephyr) mới là SOTA. Pairwise còn mắc **non-transitivity** (~35% cặp bị "lật"). → **KHÔNG** claim pairwise *luôn* tốt hơn.
- So-cặp giảm gánh nặng cho mô hình (chỉ phải quyết định giữa 2) + cho **dấu vết kiểm mâu thuẫn**.
- Bài **không** tự bàn Copeland/min-FAS — phần tổng hợp đó ta lấy từ Dwork/Ailon (Copeland là *một-trong-nhiều*; Bradley-Terry/Elo là chuẩn de-facto).

## Dùng refer gì cho bài của tôi
- Trả lời đòn *"sao không listwise một-shot cho rẻ?"*: pairwise chính xác hơn **ở model tầm-trung** (Qin) — đúng chế-độ của ta; **thêm baseline listwise** để so thẳng (không claim tốt hơn phổ quát).
- Biện minh Stage-0 hỏi **từng cặp "màn nào trước"** thay vì bắt VLM sắp cả dãy.
- Kết hợp: Qin (so-cặp) + Dwork (Copeland) + Ailon (min-FAS) = 3 mảnh của Stage-0; reframe Stage-0 = **"một-trong-nhiều, hợp cho VLM tầm-trung + ít màn"**, không "chuẩn duy nhất".
