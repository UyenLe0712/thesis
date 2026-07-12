// ============================================================================
//  WORKFLOW: thesis-advisor-prep
//  Mục đích: research metric + dataset + pipeline, verify citation bằng web,
//            rồi viết câu trả lời TIẾNG VIỆT cho 3 câu hỏi của thầy.
//
//  Cách chạy (ở phiên Claude Code, trong D:\Master\Thesis):
//     "chạy workflow thesis-advisor-prep"
//  Sửa file này rồi chạy lại -> phần không đổi dùng cache, chỉ chạy phần mới.
// ============================================================================

// --- meta: BẮT BUỘC, phải là literal thuần (không biến, không hàm) ---------
export const meta = {
  name: 'thesis-advisor-prep',
  description: 'Research metric + dataset + pipeline cho luận văn, verify citation, trả lời 3 câu hỏi thầy',
  phases: [
    { title: 'Research'   },   // fan-out song song
    { title: 'Verify'     },   // mỗi finding 1 skeptic, web-check
    { title: 'Synthesize' },   // gộp -> câu trả lời tiếng Việt
  ],
}

// --- Ràng buộc đề tài: nhét vào MỌI agent để không lệch (Đòn bẩy ④) --------
const CONTEXT = `
BỐI CẢNH LUẬN VĂN (tuân thủ tuyệt đối):
- Đề tài: sinh hướng dẫn step-by-step từ 1 ảnh UI + 1 câu hỏi ngôn ngữ tự nhiên (image+text -> text).
- View Hierarchy (VH) CHỈ dùng để CHẤM ĐIỂM, KHÔNG dùng làm input lúc sinh.
- Lúc sinh, UI element phải trích từ CHÍNH BỨC ẢNH (VLM/OCR/grounding), tránh data leakage.
- Khung đánh giá kế thừa: Intrinsic (Grounding / Clarity-Format / Hallucination) + Extrinsic (Task Success).
- Reference-free: KHÔNG có ground-truth hướng dẫn do người viết.
`

// --- Danh sách đầu việc (work-list). Mỗi agent HẸP + có "câu hỏi chấm" (③) -
const TASKS = [
  { key: 'metric-grounding', track: 'metric', prompt:
    `Tìm metric reference-free đánh giá UI GROUNDING: tọa độ [x,y] model định click có nằm trong
     bounding box của element không. Ứng viên: center-point accuracy, IoU, ScreenSpot/-v2 protocol.
     Mỗi metric nêu: cách tính, cần input gì (bbox/VH/tọa độ), paper gốc + năm + tác giả.` },

  { key: 'metric-hallucination', track: 'metric', prompt:
    `Tìm metric/method đánh giá HALLUCINATION: model sinh thao tác trên element KHÔNG tồn tại trong VH.
     Mỗi cái nêu cách tính + paper. XÁC MINH KỸ: "HalluClear 2026" có thật không, nếu không thì
     đề xuất tên metric/paper thật tương đương.` },

  { key: 'metric-format', track: 'metric', prompt:
    `Tìm metric đánh giá CLARITY & FORMAT của hướng dẫn step-by-step: có đánh số (1,2,3),
     có động từ hành động (Click/Nhập), readability. Nêu metric cụ thể + paper.` },

  { key: 'dataset-mobileviews', track: 'dataset', prompt:
    `Khảo sát dataset MobileViews: quy mô, có View Hierarchy + bbox pixel không, có Complete Traces
     (trajectory đa bước) không, license, 1 ví dụ mẫu. Điểm mạnh/yếu cho bài toán "suy luận màn hình
     kế tiếp từ 1 ảnh". CẢNH BÁO: kiểm tra xem "metric Tappability/ScreenQA của MobileViews" có thật
     hay là bịa.` },

  { key: 'dataset-mind2web', track: 'dataset', prompt:
    `Khảo sát dataset Mind2Web: quy mô, có gì ngoài DOM (có bbox pixel không?), license, 1 ví dụ.
     Bộ metric Task Success chuẩn của nó (Step SR / Element Acc / Op F1). So sánh web (Mind2Web) vs
     mobile (MobileViews): cái nào neo được đặc tả "đoán màn hình kế từ 1 ảnh"? Nên scope web hay mobile?` },

  { key: 'pipeline-design', track: 'pipeline', prompt:
    `Đề xuất 1-2 pipeline CỤ THỂ: ảnh+câu hỏi -> trích UI element từ ẢNH (VLM/OCR/grounding, KHÔNG từ VH)
     -> phân tích intent -> CONSTRAINED GENERATION (ép chỉ dùng element đã trích) -> VERIFICATION chống
     hallucination -> output step-by-step. Nêu rõ từng module + model gợi ý (GPT-4o/Claude/Gemini/Qwen2.5-VL)
     + cách xử lý ca đa bước (suy luận màn hình kế).` },
]

// --- Schema: ép agent trả structured, BẮT BUỘC có field paper (Đòn bẩy ①) --
const FINDING_SCHEMA = {
  type: 'object',
  properties: {
    findings: { type: 'array', items: {
      type: 'object',
      properties: {
        name:   { type: 'string', description: 'tên metric/dataset/module' },
        paper:  { type: 'string', description: 'tên paper + tác giả (rỗng nếu không có)' },
        year:   { type: 'string' },
        url:    { type: 'string', description: 'link nguồn' },
        detail: { type: 'string', description: 'cách tính / mô tả / điểm mạnh-yếu' },
        applies:{ type: 'string', description: 'áp dụng vào đề tài thế nào' },
      },
      required: ['name', 'detail'],
    } },
  },
  required: ['findings'],
}

// --- Schema verdict cho khâu verify ----------------------------------------
const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    real:    { type: 'boolean', description: 'citation có thật & đúng như claim không' },
    note:    { type: 'string',  description: 'bằng chứng tìm được / lý do nghi ngờ' },
    fixed:   { type: 'string',  description: 'nếu bịa, đề xuất nguồn thật thay thế' },
  },
  required: ['real', 'note'],
}

// ============================================================================
//  PIPELINE: mỗi task chạy research -> verify NGAY khi research xong.
//  (pipeline() = không có barrier giữa 2 stage; task A verify trong khi task B
//   còn đang research -> tiết kiệm wall-clock.)
// ============================================================================
const results = await pipeline(
  TASKS,

  // STAGE 1 — RESEARCH (Đòn bẩy ①: WebSearch + schema bắt buộc)
  (t) => agent(
    CONTEXT + '\n' + t.prompt +
    '\n\nDÙNG WebSearch để có nguồn THẬT, có link. KHÔNG bịa tên paper.',
    { label: `research:${t.key}`, phase: 'Research', schema: FINDING_SCHEMA }
  ),

  // STAGE 2 — VERIFY đối kháng (Đòn bẩy ②: mặc định nghi ngờ + web-check)
  (research, t) => agent(
    CONTEXT +
    `\nNHIỆM VỤ: PHẢN BIỆN kết quả research "${t.key}". Với MỖI paper/metric/dataset bên dưới:` +
    `\n- Dùng WebSearch xác minh nó CÓ THẬT không, có ĐÚNG nói điều ta claim không.` +
    `\n- MẶC ĐỊNH NGHI NGỜ. Không tìm thấy nguồn -> real=false, và đề xuất nguồn thật ở field "fixed".` +
    `\n\nKẾT QUẢ CẦN VERIFY:\n` + JSON.stringify(research),
    { label: `verify:${t.key}`, phase: 'Verify', schema: VERDICT_SCHEMA }
  ).then((verdict) => ({ key: t.key, track: t.track, research, verdict }))
)

// ============================================================================
//  SYNTHESIZE — 1 agent gộp toàn bộ finding ĐÃ VERIFY -> trả lời 3 câu hỏi.
//  (Đòn bẩy ⑤: chỉ đọc, không research thêm; map 1-1 với 3 câu hỏi thầy.)
// ============================================================================
const clean = results.filter(Boolean)

const answer = await agent(
  CONTEXT +
  `\nBạn là trợ lý luận văn. Dưới đây là các finding ĐÃ qua verify (mỗi cái có verdict.real).` +
  `\nViết câu trả lời TIẾNG VIỆT, mạch lạc, cho ĐÚNG 3 câu hỏi của thầy:` +
  `\n\nQ1 — Framework đánh giá: 3 phương pháp (grounding / hallucination / format) đã ổn chưa,` +
  ` góp ý gì, và METRIC CỤ THỂ nào (có paper) cho từng cái?` +
  `\nQ2 — Dataset: so sánh MobileViews vs Mind2Web (mạnh/yếu, áp dụng), và nên scope WEB hay MOBILE?` +
  `\nQ3 — Pipeline: trình bày 1-2 pipeline cụ thể để thầy góp ý.` +
  `\n\nQUY TẮC: chỉ dùng finding có verdict.real=true. Cái nào real=false -> ghi rõ` +
  ` "CHƯA XÁC MINH ĐƯỢC, cần đọc thêm" thay vì im lặng bỏ qua. Trích link khi có.` +
  `\n\nDỮ LIỆU:\n` + JSON.stringify(clean),
  { label: 'synthesize', phase: 'Synthesize' }
)

return answer
