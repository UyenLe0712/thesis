# LLM Evaluators Recognize and Favor Their Own Generations (Panickssery et al.)

- **Link:** https://openreview.net/forum?id=Ns8zGZ0lmM
- **Venue/năm:** NeurIPS 2024.
- **Vai trong luận văn:** trụ cho lá chắn **anti-circularity** — LLM-judge phải KHÁC HỌ với generator (§5.4, §7.1).

## Paper này nói gì (cho người mới)
Khi dùng một LLM để **chấm điểm** đầu ra của các mô hình, người ta phát hiện: LLM có xu hướng **thiên vị chính đầu ra của họ nhà nó** (self-preference bias), và mức thiên vị này **tương quan với khả năng nó "nhận ra" văn bản của chính mình**. Tức là dùng GPT chấm GPT sẽ cho điểm cao thiên lệch.

## Điểm cần biết
- Đây là **thiên lệch đã được đo**, không phải lo xa.
- Hệ quả: nếu generator là họ GPT (gpt-4o-mini) thì **LLM-judge không được dùng họ GPT**.
- Củng cố nguyên tắc "công cụ ra quyết định ≠ công cụ chấm".

## Dùng refer gì cho bài của tôi
- **Trụ chính** cho quy tắc §5.4: judge nhị phân phải **khác họ generator**.
- Cùng luận cứ chống **circularity** (§7.1): tách `nomic` (quyết) ↔ `bge-m3` (chấm) ↔ judge khác họ ↔ token-overlap = 3 cơ chế độc lập.
