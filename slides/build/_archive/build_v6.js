// Deck v6 — bản trình thầy, soạn từ report/98. Thiết kế executability + bằng chứng số đo thật.
// Dual-emit: ../LUAN_VAN_SLIDE_v6.pptx + _preview_v6/preview.html
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Luan van thac si";
pres.title = "Sinh huong dan su dung phan mem cho nguoi";

const TF = "Cambria", BF = "Segoe UI";
const INK = "1D2733", BODY = "454C55", MUTE = "8B929B";
const ACCENT = "BE5A2E", STEEL = "52657A", GOOD = "1E6B43", BAD = "B23B3B";
const RULE = "DBE0E6", FILL = "F3F5F7", TINT = "F7EBE3", NAVY = "17233B", WHITE = "FFFFFF";
const W = 13.33, H = 7.5, M = 0.92;

const PX = 96;
const FMAP = { "Cambria": "'DejaVu Serif',serif", "Segoe UI": "'DejaVu Sans',sans-serif" };
let htmlSlides = [], cur = "";
function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function plain(c) { return typeof c === "string" ? c : c.map(r => r.text).join(""); }
function hpush(html) { cur += html; }
let s, PAGE = 0;
function slide(bg) { if (cur) htmlSlides.push(cur + "</div>"); s = pres.addSlide(); s.background = { color: bg || WHITE }; cur = `<div class="slide" style="background:#${bg || WHITE}">`; }
function done() { if (cur) { htmlSlides.push(cur + "</div>"); cur = ""; } }
function text(content, o) {
  const opt = Object.assign({ x: 0, y: 0, w: 4, h: 1, fontSize: 14, color: BODY, fontFace: BF, align: "left", valign: "top", margin: o.margin != null ? o.margin : 4 }, o);
  if (o.lh) opt.lineSpacingMultiple = o.lh;
  if (o.spacing) opt.charSpacing = o.spacing;
  s.addText(content, opt);
  const jc = opt.align === "center" ? "center" : opt.align === "right" ? "flex-end" : "flex-start";
  const ai = opt.valign === "middle" ? "center" : opt.valign === "bottom" ? "flex-end" : "flex-start";
  const pad = (opt.margin || 0) / PX;
  const st = `position:absolute;left:${o.x * PX}px;top:${o.y * PX}px;width:${o.w * PX}px;height:${o.h * PX}px;display:flex;justify-content:${jc};align-items:${ai};padding:${pad}in;box-sizing:border-box;font-family:${FMAP[opt.fontFace]};font-size:${opt.fontSize}px;color:#${opt.color};text-align:${opt.align};line-height:${o.lh || 1.15};` + (opt.bold ? "font-weight:700;" : "") + (opt.italic ? "font-style:italic;" : "") + (opt.spacing ? `letter-spacing:${opt.spacing * 0.7}px;` : "");
  hpush(`<div style="${st}"><div style="white-space:pre-line;width:100%">${esc(plain(content))}</div></div>`);
}
function rect(x, y, w, h, fill, o) {
  o = o || {};
  const shp = o.radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE;
  const p = { x, y, w, h, fill: fill === "none" ? { type: "none" } : { color: fill }, line: o.line ? { color: o.line, width: o.lw || 1 } : { type: "none" } };
  if (o.radius) p.rectRadius = o.radius;
  if (o.shadow) p.shadow = { type: "outer", color: "9AA3AD", blur: 7, offset: 3, angle: 90, opacity: 0.28 };
  s.addShape(shp, p);
  const st = `position:absolute;left:${x * PX}px;top:${y * PX}px;width:${w * PX}px;height:${h * PX}px;` + (fill === "none" ? "" : `background:#${fill};`) + (o.radius ? `border-radius:${o.radius * PX}px;` : "") + (o.line ? `border:${o.lw || 1}px solid #${o.line};box-sizing:border-box;` : "") + (o.shadow ? "box-shadow:0 3px 9px rgba(140,150,160,.30);" : "");
  hpush(`<div style="${st}"></div>`);
}
function image(path, x, y, w, h) {
  try { s.addImage({ path: "_img/" + path, x, y, w, h, sizing: { type: "contain", w, h } }); } catch (e) {}
  hpush(`<img src="../_img/${path}" style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:${w * PX}px;height:${h * PX}px;object-fit:contain">`);
}
function shot(path, x, y, w, h, cap) {
  rect(x - 0.07, y - 0.07, w + 0.14, h + (cap ? 0.48 : 0.14), WHITE, { radius: 0.07, line: RULE, lw: 1, shadow: true });
  image(path, x, y, w, h);
  if (cap) text(cap, { x: x - 0.07, y: y + h + 0.03, w: w + 0.14, h: 0.34, align: "center", valign: "middle", fontSize: 12.5, bold: true, color: INK, fontFace: BF, margin: 0 });
}
function arrow(x, y, w, c) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || ACCENT, width: 2.5, endArrowType: "triangle" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX - 1}px;width:${w * PX}px;height:0;border-top:2.5px solid #${c || ACCENT}"></div><div style="position:absolute;left:${(x + w) * PX - 5}px;top:${y * PX - 5}px;width:0;height:0;border-left:8px solid #${c || ACCENT};border-top:5px solid transparent;border-bottom:5px solid transparent"></div>`);
}
function circle(x, y, d, fill, glyph, gc) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:${d * PX}px;height:${d * PX}px;border-radius:50%;background:#${fill}"></div>`);
  if (glyph) text(glyph, { x, y, w: d, h: d, align: "center", valign: "middle", fontSize: d * 34, bold: true, color: gc || WHITE, fontFace: TF, margin: 0 });
}
function note(t) { s.addNotes(t.trim()); }
function kicker(t) { text(t.toUpperCase(), { x: M, y: 0.62, w: W - 2 * M, h: 0.3, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, spacing: 2.5, margin: 0 }); }
function title(t) { text(t, { x: M, y: 0.98, w: W - 2 * M, h: 1.0, fontSize: 26, bold: true, color: INK, fontFace: TF, margin: 0, lh: 1.05 }); }
function head(k, t) { kicker(k); title(t); }
function pageno() { PAGE++; text(String(PAGE).padStart(2, "0"), { x: W - 1.05, y: H - 0.5, w: 0.6, h: 0.3, fontSize: 10, color: MUTE, align: "right", fontFace: BF, margin: 0 }); }

// ===================================================== 1 · TITLE
slide(NAVY);
text("LUẬN VĂN THẠC SĨ · BÁO CÁO TIẾN ĐỘ", { x: M, y: 1.45, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Sinh hướng dẫn sử dụng\nphần mềm cho người đọc", { x: M - 0.02, y: 2.1, w: 9.6, h: 1.9, fontSize: 33, bold: true, color: WHITE, fontFace: TF, lh: 1.08, margin: 0 });
text("Từ một ảnh màn hình + câu hỏi → các bước cho người tự làm theo", { x: M, y: 4.25, w: 9.4, h: 0.6, fontSize: 16, italic: true, color: "C9D2DC", fontFace: TF, margin: 0 });
text("Học viên · · · · ·        Giảng viên hướng dẫn · · · · ·        2026", { x: M, y: 6.55, w: 11, h: 0.4, fontSize: 13, color: "8FA0B2", fontFace: BF, margin: 0 });
shot("real_mv_1.png", 10.5, 1.9, 1.9, 3.35);
done();

// ===================================================== 2 · BAI TOAN
slide();
head("Bài toán", "Một màn hình + một câu hỏi → hướng dẫn cho NGƯỜI");
shot("real_mv_2.png", M, 2.5, 2.5, 4.3);
rect(4.0, 2.55, 8.4, 1.5, TINT, { radius: 0.1 });
text([{ text: "Câu hỏi:  ", options: { bold: true, color: ACCENT } }, { text: "“Làm sao thêm một việc mới rồi lưu lại?”", options: { color: INK, italic: true } }], { x: 4.3, y: 2.55, w: 7.9, h: 0.65, fontSize: 15.5, fontFace: BF, valign: "middle", margin: 0 });
text([{ text: "Trả lời:  ", options: { bold: true, color: STEEL } }, { text: "1. Nhập tên việc  →  2. Điền số giờ  →  3. Chạm SAVE & ADD ANOTHER", options: { color: BODY } }], { x: 4.3, y: 3.2, w: 7.9, h: 0.7, fontSize: 14, fontFace: BF, valign: "middle", margin: 0, lh: 1.2 });
rect(4.0, 4.25, 8.4, 0.9, FILL, { radius: 0.1 });
text([{ text: "Khác mọi mô hình giao diện hiện có:  ", options: { bold: true, color: INK } }, { text: "mô hình khác sinh thao tác cho MÁY bấm; ở đây sinh câu cho CON NGƯỜI đọc.", options: { color: BODY } }], { x: 4.3, y: 4.25, w: 7.8, h: 0.9, fontSize: 13.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
text("Cái khó không ở việc SINH câu — mà ở việc CHẤM", { x: 4.0, y: 5.35, w: 8.4, h: 0.4, fontSize: 15, bold: true, color: INK, fontFace: TF, margin: 0 });
rect(4.0, 5.8, 4.1, 1.0, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "?  ", options: { bold: true, color: STEEL, fontFace: TF } }, { text: "Không có đáp án mẫu để đối chiếu.", options: { color: BODY } }], { x: 4.22, y: 5.8, w: 3.7, h: 1.0, fontSize: 13, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
rect(8.3, 5.8, 4.1, 1.0, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "✗  ", options: { bold: true, color: BAD, fontFace: TF } }, { text: "Chấm bằng người: tốn kém, khó lặp lại.", options: { color: BODY } }], { x: 8.52, y: 5.8, w: 3.7, h: 1.0, fontSize: 13, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
note(`Bài toán: vào là 1 ảnh + 1 câu hỏi, ra là các bước cho người tự làm.
Điểm khác biệt cốt lõi so với mọi mô hình GUI khác: chúng sinh thao tác cho MÁY tự bấm; ta sinh câu cho NGƯỜI đọc.
Cái khó nằm ở việc CHẤM: không có đáp án mẫu do người soạn, và chấm bằng người thì tốn kém, khó lặp lại. Đây chính là chỗ luận văn có chất nghiên cứu, và là lý do có hai đóng góp: mô hình + phương pháp chấm.`);
pageno(); done();

// ===================================================== 3 · DA DOI GI
slide();
head("Vì sao trục chính là ĐO ĐỘ ĐÚNG", "Thử hướng “lọc bịa” → kiểm chứng bằng số → chuyển sang đo độ đúng");
rect(M, 2.5, 5.35, 3.15, FILL, { radius: 0.1 });
text("Hướng thử đầu tiên", { x: M + 0.3, y: 2.72, w: 4.7, h: 0.4, fontSize: 15, bold: true, color: MUTE, fontFace: TF, margin: 0 });
text("Giả thuyết: mô hình lớn hay BỊA\ntên nút → lọc bỏ chỗ bịa → dạy\nmô hình nhỏ trung thực hơn.\n\nXem “lọc bịa” là đóng góp.", { x: M + 0.3, y: 3.2, w: 4.75, h: 2.3, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
arrow(6.5, 4.05, 0.55);
rect(7.35, 2.5, 5.05, 3.15, TINT, { radius: 0.1 });
text("Kiểm chứng → loại bỏ", { x: 7.65, y: 2.72, w: 4.4, h: 0.4, fontSize: 15, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Đọc tay 80 màn gpt-4o sinh →\ngần như KHÔNG bịa (~0–2%).\nChỗ tưởng “bịa” là nút CÓ THẬT\nmà danh sách nút bỏ sót nhãn.\n\n→ không còn gì để lọc.", { x: 7.65, y: 3.2, w: 4.4, h: 2.3, fontSize: 13.5, color: INK, fontFace: BF, lh: 1.35, margin: 0 });
rect(M, 5.9, W - 2 * M, 0.9, NAVY, { radius: 0.1 });
text([{ text: "Hướng đề xuất:  ", options: { bold: true, color: "F0C9A8" } }, { text: "giữ mô hình tự huấn luyện làm trung tâm, nhưng trục chính là đo ĐỘ ĐÚNG — hướng dẫn có dẫn tới đúng nút không — chứ không phải “chống bịa”.", options: { color: WHITE } }], { x: M + 0.3, y: 5.9, w: W - 2 * M - 0.6, h: 0.9, fontSize: 14, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
note(`Đây là chỗ cho thầy thấy cách em làm việc. Sau góp ý của thầy (cần một mô hình tự huấn luyện, không chỉ prompting), em bắt tay làm. Hướng đầu tiên em nghĩ tới: mô hình lớn hay bịa tên nút, nên lọc bịa rồi dạy mô hình nhỏ — coi đó là đóng góp.
Nhưng em kiểm chứng trước (miễn phí, đọc tay 80 màn): mô hình gần như không bịa (0-2%). Chỗ tưởng bịa thật ra là nút có thật mà View Hierarchy bỏ sót nhãn.
Nên em bỏ hướng "lọc bịa", chuyển trục chính sang đo ĐỘ ĐÚNG. Mô hình tự huấn luyện vẫn là trung tâm — đúng điều thầy yêu cầu.`);
pageno(); done();

// ===================================================== 4 · HE THONG + LUAT VANG
slide();
head("Hệ thống chạy thế nào", "Dạy bằng câu mẫu người viết · chấm trên app CHƯA TỪNG THẤY");
rect(M, 2.5, 5.5, 1.55, FILL, { radius: 0.1 });
text("Lúc DẠY (train)", { x: M + 0.28, y: 2.68, w: 5.0, h: 0.4, fontSize: 15, bold: true, color: STEEL, fontFace: TF, margin: 0 });
text("Đưa cặp (ảnh một bước + mục tiêu) → (câu hướng dẫn do NGƯỜI viết).\nNguồn người viết = bộ AndroidControl.", { x: M + 0.28, y: 3.1, w: 5.0, h: 0.95, fontSize: 13, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });
rect(6.9, 2.5, 5.5, 1.55, TINT, { radius: 0.1 });
text("Lúc CHẤM (test)", { x: 7.18, y: 2.68, w: 5.0, h: 0.4, fontSize: 15, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Đưa MỘT ảnh app LẠ + mục tiêu. Không danh sách nút, không đáp án.\nNó phải tự nhìn màn lạ mà sinh.", { x: 7.18, y: 3.1, w: 5.0, h: 0.95, fontSize: 13, color: INK, fontFace: BF, lh: 1.3, margin: 0 });
rect(M, 4.35, W - 2 * M, 1.35, WHITE, { radius: 0.1, line: ACCENT, lw: 1.5 });
text("NGUYÊN TẮC CHỐNG ĂN GIAN", { x: M + 0.3, y: 4.5, w: 10, h: 0.4, fontSize: 14.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("View Hierarchy + đáp án: CHỈ để dạy & chấm, KHÔNG đưa lúc sinh. App test khác app train.", { x: M + 0.3, y: 4.95, w: W - 2 * M - 0.6, h: 0.7, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });
rect(M, 5.95, W - 2 * M, 0.85, FILL, { radius: 0.09 });
text([{ text: "Vì sao vậy:  ", options: { bold: true, color: INK } }, { text: "đúng trên app LẠ = học được kỹ năng thật, không học thuộc. Chạy thật chỉ cần ảnh.", options: { color: BODY } }], { x: M + 0.3, y: 5.95, w: W - 2 * M - 0.6, h: 0.85, fontSize: 13.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
note(`Tách bạch chỗ nào là học, chỗ nào là chấm. Lúc dạy: cặp (ảnh bước + mục tiêu) → câu người viết của AndroidControl. Lúc chấm: app chưa từng thấy, chỉ ảnh + mục tiêu, không mớm đáp án.
Nguyên tắc chống ăn gian: View Hierarchy và đáp án chỉ để dạy + chấm, không đưa lúc sinh. App test khác app train. Nhờ vậy làm đúng trên app lạ = thật sự học được kỹ năng.`);
pageno(); done();

// ===================================================== 4B · PIPELINE (3 luong)
slide();
head("Luồng chạy", "Ba luồng: huấn luyện · lúc chạy · chấm");
// 3 cot
const col = [
  ["① HUẤN LUYỆN", ACCENT, "(ảnh bước + mục tiêu)\n→ câu người viết", "Qwen2.5-VL-3B học viết\nhướng dẫn giống người thật\n(QLoRA). Có thể dạy thêm\nbằng cặp câu đúng / câu bịa."],
  ["② LÚC CHẠY", STEEL, "1 ảnh + 1 câu hỏi\n→ hướng dẫn", "Không cần VH, không\nđáp án — chỉ ẢNH.\nĐiện thoại nào cũng\ncó sẵn → dùng thật được."],
  ["③ CHẤM (chỗ mới)", GOOD, "câu → bộ trỏ → (x,y)\n→ so gold", "Đưa câu cho bộ trỏ:\ncó trỏ tới đúng nút\nkhông? Trúng = câu\nđúng. (chi tiết slide sau)"],
];
let cx = M;
col.forEach((c, i) => {
  rect(cx, 2.5, 3.7, 3.15, i === 2 ? TINT : FILL, { radius: 0.1 });
  text(c[0], { x: cx + 0.25, y: 2.7, w: 3.3, h: 0.4, fontSize: 15, bold: true, color: c[1], fontFace: TF, margin: 0 });
  rect(cx + 0.25, 3.18, 3.2, 0.92, WHITE, { radius: 0.07, line: RULE, lw: 1 });
  text(c[2], { x: cx + 0.4, y: 3.18, w: 2.95, h: 0.92, fontSize: 12, bold: true, color: INK, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
  text(c[3], { x: cx + 0.25, y: 4.2, w: 3.25, h: 1.3, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.32, margin: 0 });
  if (i < 2) arrow(cx + 3.78, 4.05, 0.32);
  cx += 4.1;
});
// dai quy mo du lieu
rect(M, 5.95, W - 2 * M, 0.85, NAVY, { radius: 0.1 });
text([{ text: "DẠY:  ", options: { bold: true, color: "F0C9A8" } }, { text: "chỉ AndroidControl (gold người viết).   ", options: { color: WHITE } }, { text: "CHẤM:  ", options: { bold: true, color: "F0C9A8" } }, { text: "AndroidControl app lạ 631 ep = độ ĐÚNG · MobileViews = độ BỊA · ScreenSpot = bộ trỏ.", options: { color: WHITE } }], { x: M + 0.3, y: 5.95, w: W - 2 * M - 0.6, h: 0.85, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
note(`Ba luồng nối tiếp: (1) huấn luyện — mỗi bước AndroidControl cho một cặp (ảnh + mục tiêu) → câu người viết, train Qwen-3B qua QLoRA (fine-tune nhẹ). (2) lúc chạy — người dùng chỉ đưa ảnh + câu hỏi, mô hình sinh hướng dẫn, không cần VH hay đáp án nên dùng thật được. (3) chấm — chỗ có chất mới: câu → bộ trỏ → toạ độ → so gold; lượt không-câu làm sàn; bơm lỗi kiểm thước.
Dữ liệu: AndroidControl có toạ độ gold nên đo được độ đúng (test app lạ 631 ep); MobileViews có View Hierarchy nên đo được độ bịa (127 màn/30 app). Hai bộ bù cho nhau.`);
pageno(); done();

// ===================================================== 5 · DONG GOP 1 - MO HINH
slide();
head("Đóng góp 1 — Mô hình", "Huấn luyện Qwen2.5-VL-3B, chạy offline · so với ba mốc");
rect(M, 2.0, W - 2 * M, 0.46, TINT, { radius: 0.07 });
text([{ text: "Train trên:  ", options: { bold: true, color: ACCENT } }, { text: "train split của AndroidControl — lấy câu hướng dẫn người viết sẵn làm đáp án. App đem chấm là app KHÁC, chưa thấy lúc train.", options: { color: INK } }], { x: M + 0.25, y: 2.0, w: W - 2 * M - 0.5, h: 0.46, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0 });
const rows = [
  ["Qwen-3B chưa fine-tune", "mốc sàn tham chiếu", "—", MUTE],
  ["gpt-4o-mini (không train)", "mốc ngoài — mô hình lớn", "không học", STEEL],
  ["Qwen-3B SFT thường", "mốc trong — để so", "người viết", STEEL],
  ["Qwen-3B SFT + thành phần", "ĐÓNG GÓP luận văn", "người viết\n+ thành phần", ACCENT],
];
let ry = 2.62;
rows.forEach((r, i) => {
  const hl = i === 3;
  rect(M, ry, 7.3, 0.82, hl ? TINT : FILL, { radius: 0.08 });
  text(r[0], { x: M + 0.22, y: ry, w: 3.0, h: 0.82, fontSize: 13.5, bold: hl, color: hl ? ACCENT : INK, fontFace: BF, valign: "middle", margin: 0 });
  text(r[1], { x: M + 3.25, y: ry, w: 2.7, h: 0.82, fontSize: 11.5, color: r[3], fontFace: BF, valign: "middle", margin: 0, lh: 1.15 });
  text(r[2], { x: M + 5.95, y: ry, w: 1.25, h: 0.82, fontSize: 11, italic: true, color: BODY, fontFace: BF, valign: "middle", margin: 0 });
  ry += 0.94;
});
rect(8.6, 2.62, 3.8, 3.51, NAVY, { radius: 0.1 });
text("Hai phép so", { x: 8.85, y: 2.8, w: 3.3, h: 0.4, fontSize: 15, bold: true, color: "F0C9A8", fontFace: TF, margin: 0 });
text("CHÍNH — hơn SFT-trơn\n→ ablation sạch: thành phần thêm\nvào có tác dụng thật.", { x: 8.85, y: 3.25, w: 3.35, h: 1.15, fontSize: 12.5, color: WHITE, fontFace: BF, lh: 1.3, margin: 0 });
text("Phụ — hơn gpt-4o-mini\n→ minh hoạ, không phải kết luận chính\n(mô hình mình có lợi thế sân nhà).", { x: 8.85, y: 4.5, w: 3.35, h: 1.1, fontSize: 12.5, color: "C9D2DC", fontFace: BF, lh: 1.3, margin: 0 });
rect(M, 6.35, W - 2 * M, 0.75, WHITE, { radius: 0.09, line: BAD, lw: 1.2 });
text([{ text: "Tránh bẫy “học ai chỉ bằng người đó”:  ", options: { bold: true, color: BAD } }, { text: "KHÔNG học từ gpt-4o rồi lại lấy chính gpt-4o làm mốc để vượt. Dạy bằng câu mẫu người viết; gpt-4o chỉ để so.", options: { color: BODY } }], { x: M + 0.3, y: 6.35, w: W - 2 * M - 0.6, h: 0.75, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.2 });
note(`Đóng góp mô hình: train Qwen2.5-VL-3B bằng SFT-LoRA, so với ba mốc. Hai phép so quan trọng: hơn gpt-4o-mini = 3B offline ngang mô hình API lớn; hơn SFT-trơn = thành phần thêm có tác dụng (ablation).
Bẫy phải tránh: không học từ gpt-4o rồi lại lấy chính gpt-4o làm mốc để vượt (học ai thì chỉ bằng người đó). Tín hiệu dạy là gold người viết.
Thành phần thêm chưa quyết cứng — chọn bằng Cổng B; hiện nghiêng về cách dạy bằng cặp câu đúng/sai (rẻ, an toàn). Chi tiết ở slide sau.`);
pageno(); done();

// ===================================================== 5B · THANH PHAN THEM
slide();
head("Thành phần thêm vào mô hình", "Thứ làm mô hình mình hơn bản SFT thường — chọn sau bằng phép thử rẻ (Cổng B)");
const cand = [
  ["① Tự cải thiện", STEEL, false, "Mô hình tự sinh nhiều câu cho một màn → giữ lại câu nào TRỎ TRÚNG nút thật → đem chính phần đó dạy lại nó.", "Mạnh nhất. Phức tạp hơn — cần hai bộ trỏ khác nhau để khỏi “dạy để thi”."],
  ["② Dạy bằng cặp đúng / sai", ACCENT, true, "Đưa từng cặp: “câu gọi nút CÓ THẬT” và “câu gọi nút BỊA” (đúc từ View Hierarchy) → dạy mô hình chuộng câu đúng.", "Rẻ, an toàn, ít bẫy → ĐỀ XUẤT chọn cái này."],
  ["③ Kiểm & sửa lúc chạy", STEEL, false, "Câu còn mơ hồ (“chạm nút”) → hệ nhắc “nói rõ nút nào” → mô hình viết lại cho rõ.", "Không cần huấn luyện thêm. Chỉ bổ trợ."],
];
let px = M;
cand.forEach((c) => {
  rect(px, 2.5, 3.7, 3.35, c[2] ? TINT : FILL, { radius: 0.1 });
  text(c[0], { x: px + 0.25, y: 2.72, w: 3.3, h: 0.4, fontSize: 15, bold: true, color: c[1], fontFace: TF, margin: 0 });
  text(c[3], { x: px + 0.25, y: 3.22, w: 3.25, h: 1.75, fontSize: 12.5, color: INK, fontFace: BF, lh: 1.34, margin: 0 });
  text(c[4], { x: px + 0.25, y: 5.0, w: 3.25, h: 0.8, fontSize: 12, italic: true, color: c[2] ? ACCENT : BODY, fontFace: BF, lh: 1.3, margin: 0 });
  px += 4.1;
});
rect(M, 6.05, W - 2 * M, 0.78, NAVY, { radius: 0.1 });
text([{ text: "Chọn cái nào?  ", options: { bold: true, color: "F0C9A8" } }, { text: "Cổng B đo mô hình yếu ở đâu — hay bịa nút thì lấy cách ②, hay trỏ mơ hồ thì lấy cách ①. Hiện nghiêng về ② vì rẻ và ít rủi ro nhất.", options: { color: WHITE } }], { x: M + 0.3, y: 6.05, w: W - 2 * M - 0.6, h: 0.78, fontSize: 13, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
note(`Đây chính là "thành phần thêm" — thứ làm mô hình của mình hơn bản SFT thường, tức là phần lõi của đóng góp model.
Ba cách: (1) Tự cải thiện — mô hình tự sinh nhiều câu rồi tự giữ lại câu trỏ trúng để học lại; mạnh nhất nhưng phải dùng hai bộ trỏ khác nhau để tránh "dạy để thi". (2) Dạy bằng cặp đúng/sai (kỹ thuật tên là DPO) — rẻ, an toàn, nhắm thẳng chuyện bớt bịa nút; đây là cái em đề xuất. (3) Kiểm & sửa lúc chạy — không train thêm, chỉ bổ trợ.
Chưa quyết cứng cái nào: em sẽ chạy Cổng B để biết mô hình yếu ở đâu rồi mới gắn đúng chỗ.`);
pageno(); done();

// ===================================================== 6 · DONG GOP 2 - THUOC EXEC
slide();
head("Đóng góp 2 — Thước Executability", "Câu có đủ rõ để lần ra đúng nút không?");
text("Giấu mục tiêu, đưa bộ trỏ CHỈ câu + ảnh → nó chấm một điểm nên chạm. Điểm rơi trúng nút cần → câu ĐÚNG.", { x: M, y: 2.35, w: W - 2 * M, h: 0.45, fontSize: 14, color: BODY, fontFace: BF, margin: 0, lh: 1.25 });
// ảnh thật: câu → bộ trỏ chấm điểm (xanh) → rơi trúng nút (khung đỏ)
shot("real_ground_1.png", M, 2.95, 1.6, 3.4, "“invert the lens” → trúng nút");
// cột phải: cách chấm 3 bước
rect(3.05, 2.95, W - M - 3.05, 1.62, FILL, { radius: 0.1 });
text("Cách chấm — 3 bước", { x: 3.3, y: 3.12, w: 8.5, h: 0.4, fontSize: 14.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("1. Đưa bộ trỏ CHỈ câu + ảnh (giấu mục tiêu, giấu đáp án).\n2. Nó chấm một điểm nên chạm — chấm xanh trong ảnh.\n3. Điểm rơi trong vùng nút đúng (khung đỏ) → TRÚNG.", { x: 3.3, y: 3.56, w: W - M - 3.35, h: 1.0, fontSize: 13, color: INK, fontFace: BF, lh: 1.42, margin: 0 });
// khối xanh: không ăn gian
rect(3.05, 4.8, W - M - 3.05, 2.0, WHITE, { radius: 0.1, line: GOOD, lw: 1.5 });
text("Vì sao thước này không ăn gian được", { x: 3.3, y: 4.97, w: 8.5, h: 0.4, fontSize: 14, bold: true, color: GOOD, fontFace: TF, margin: 0 });
text([{ text: "Không chấm theo câu chữ: ", options: { bold: true, color: INK } }, { text: "gọi tên kiểu gì cũng được, miễn bộ trỏ lần ra đúng nút. “funnel icon” hay “Filter button” đều trỏ trúng → đều ĐÚNG.", options: { color: BODY } }], { x: 3.3, y: 5.4, w: W - M - 3.35, h: 0.75, fontSize: 12.5, fontFace: BF, margin: 0, lh: 1.32 });
text([{ text: "Chống “màn dễ”: ", options: { bold: true, color: INK } }, { text: "chạy thêm lượt KHÔNG đưa câu làm SÀN → giá trị thật = (có câu) − (không câu).", options: { color: BODY } }], { x: 3.3, y: 6.2, w: W - M - 3.35, h: 0.5, fontSize: 12.5, fontFace: BF, margin: 0, lh: 1.28 });
note(`Thước executability: giấu mục tiêu, đưa chỉ câu cho bộ trỏ, xem nó lần ra đúng nút không. Ví dụ trong ảnh: câu "invert the lens" → bộ trỏ chấm một điểm (chấm xanh) rơi đúng vào nút lật camera (khung đỏ) → trúng. Sai lệch phải trong vùng cho phép của nút (dung sai 14% cạnh màn).
Tính chất quan trọng nhất (lá chắn cho đòn nguy hiểm nhất): thước không chấm theo câu chữ. "funnel icon" và "Filter button" viết khác nhau nhưng cùng trỏ trúng. Nên "hơn" nghĩa là rõ hơn, không phải viết giống đáp án hơn — quan trọng vì mô hình học trên gold hay nói giọng gold.
Chống màn dễ: lượt không đưa câu làm sàn.`);
pageno(); done();

// ===================================================== 7 · BANG CHUNG SO DO (thay slide so cu)
slide();
head("Thước phân biệt được câu tốt/dở", "Mức tối thiểu đã đạt · còn kiểm với người xem có đo đúng cái cần");
function stat(x, big, bc, lab, sub) {
  rect(x, 2.55, 2.72, 2.55, FILL, { radius: 0.1 });
  text(big, { x: x, y: 2.85, w: 2.72, h: 0.95, fontSize: 38, bold: true, color: bc, fontFace: TF, align: "center", margin: 0 });
  text(lab, { x: x + 0.15, y: 3.9, w: 2.42, h: 0.45, fontSize: 13.5, bold: true, color: INK, fontFace: BF, align: "center", margin: 0 });
  text(sub, { x: x + 0.15, y: 4.35, w: 2.42, h: 0.7, fontSize: 11.5, color: BODY, fontFace: BF, align: "center", lh: 1.25, margin: 0 });
}
stat(M, "6.6%", STEEL, "SÀN (đoán bừa)", "không đưa câu, bộ\ntrỏ đoán → hiếm trúng");
stat(M + 2.85, "51%", STEEL, "TRẦN (có câu)", "đưa câu đáp án-chuẩn\n(bộ trỏ rẻ)");
stat(M + 5.7, "+44.7", GOOD, "ĐỘ CHÊNH", "= trần − sàn → câu\nđóng góp rõ rệt");
stat(M + 8.55, "0.34", BAD, "Cách đo đơn giản", "so chữ — thử trước,\nkhông tách nổi nút");
rect(M, 5.35, W - 2 * M, 1.4, NAVY, { radius: 0.1 });
text([{ text: "Nghĩa là gì:  ", options: { bold: true, color: "F0C9A8" } }, { text: "sàn thấp (6.6%) → thước phân biệt được câu tốt/dở (mức tối thiểu). Còn “người có làm theo được không” thì khảo sát 91 cặp với người thật (chưa chạy).", options: { color: WHITE } }], { x: M + 0.3, y: 5.5, w: W - 2 * M - 0.6, h: 0.8, fontSize: 13, fontFace: BF, margin: 0, lh: 1.35 });
text([{ text: "Khai thẳng lỗ còn lại:  ", options: { italic: true, color: "C9D2DC" } }, { text: "63% bước có nút cạnh trong dung sai → thước còn dễ dãi; sẽ vá bằng chấm theo nút đúng gần nhất.", options: { italic: true, color: "C9D2DC" } }], { x: M + 0.3, y: 6.25, w: W - 2 * M - 0.6, h: 0.5, fontSize: 11.5, fontFace: BF, margin: 0, lh: 1.25 });
note(`Đây là bằng chứng thước phân biệt được câu tốt với câu dở.
Sàn 6.6% = không đưa câu, bộ trỏ đoán bừa thì hiếm khi trúng đúng cái nút cần. Trần 51% = đưa câu đáp án (với bộ trỏ rẻ; bộ trỏ chuyên sẽ cao hơn). Chênh 44.7 = câu đóng góp rõ rệt.
Em từng LO sàn cao làm hiệu số bị nén — đo thật thì ngược lại, sàn thấp. Con số minh hoạ 72-30=42 hoá ra còn thận trọng.
0.34 = cách đo đơn giản (so chữ) em thử trước, không tách nổi nút → nên mới làm executability. Cho thấy em kiểm trước khi tin.
Giới hạn thành thật: 63% bước có nút cạnh trong dung sai, nên thước hơi rộng tay; xử bằng báo kèm sàn.`);
pageno(); done();

// ===================================================== 8 · TU KIEM TU SUA
slide();
head("Tự kiểm — tự sửa", "Bốn lỗ còn hở của thước + cách xử (nêu rõ, không giấu)");
const holes = [
  ["Mù đảo nghĩa Bật/Tắt", "công tắc “bật”/“tắt” cùng một toạ độ → câu ngược nghĩa vẫn trúng", "kiểm thêm trạng thái đích, hoặc khai + báo % bước là toggle"],
  ["~53% bước là “chạm”", "chỉ bước chạm mới chấm bằng bộ trỏ; gõ/cuộn phải chấm kiểu cũ", "TÁCH hai con số, báo riêng — không gộp thành một con số"],
  ["“Bộ trỏ trúng ≈ người làm được” chưa kiểm", "đây đúng là kiểu sai lầm làm hỏng cách đo trước của em: tin mà chưa kiểm", "đưa khảo sát với người thật 91 cặp VÀO CỔNG (bộ chấm đã dựng, free)"],
  ["Dung sai 14% hơi rộng", "63% bước có nút cạnh → dễ chấm nhầm sang nút bên", "chấm thêm theo nút đúng gần nhất, không chỉ đĩa 151px"],
];
let hy = 2.5;
holes.forEach((h, i) => {
  rect(M, hy, W - 2 * M, 0.98, i === 2 ? TINT : FILL, { radius: 0.08 });
  circle(M + 0.2, hy + 0.28, 0.42, i === 2 ? ACCENT : STEEL, String(i + 1), WHITE);
  text(h[0], { x: M + 0.8, y: hy + 0.1, w: 4.0, h: 0.8, fontSize: 13.5, bold: true, color: INK, fontFace: BF, valign: "middle", margin: 0, lh: 1.15 });
  text(h[1], { x: M + 4.9, y: hy + 0.1, w: 3.7, h: 0.8, fontSize: 11.5, color: BODY, fontFace: BF, valign: "middle", margin: 0, lh: 1.2 });
  text([{ text: "→ ", options: { bold: true, color: GOOD } }, { text: h[2], options: { color: INK } }], { x: M + 8.7, y: hy + 0.1, w: 2.75, h: 0.8, fontSize: 11.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.2 });
  hy += 1.06;
});
note(`Nêu cả các lỗ còn hở, không giấu. (1) mù đảo nghĩa bật/tắt → kiểm trạng thái đích. (2) chỉ ~53% bước là chạm → tách hai con số. (3) lỗ đáng lo nhất: "bộ trỏ trúng ≈ người làm được" chưa kiểm — đúng là kiểu sai lầm làm hỏng cách đo trước → em đưa khảo sát với người thật 91 cặp vào cổng, bộ chấm đã dựng, tự chấm được, miễn phí. (4) dung sai rộng → chấm thêm theo nút đúng gần nhất.
Điểm nhấn: quy trình của em là KIỂM trước khi tin, chấp nhận cổng có thể rớt.`);
pageno(); done();

// ===================================================== 9 · HAI CONG + DUONG LUI
slide();
head("Hai cổng trước khi tiêu tiền", "Chỉ chạy mô hình, không huấn luyện — rẻ, nhanh");
rect(M, 2.55, 5.5, 2.15, FILL, { radius: 0.1 });
text("Cổng A — bộ trỏ đủ tốt?", { x: M + 0.28, y: 2.75, w: 5.0, h: 0.4, fontSize: 15, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Bộ trỏ chuyên (OS-Atlas / UGround)\nlần vị trí từ câu ĐÚNG, phải ~80%.\nRớt → trục executability chưa dùng\nđược → rẽ đường lui.", { x: M + 0.28, y: 3.2, w: 5.0, h: 1.4, fontSize: 13, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
rect(6.9, 2.55, 5.5, 2.15, FILL, { radius: 0.1 });
text("Cổng B — gắn thành phần đâu?", { x: 7.18, y: 2.75, w: 5.0, h: 0.4, fontSize: 15, bold: true, color: STEEL, fontFace: TF, margin: 0 });
text("Đo mô hình nền yếu ở đâu (bịa\nnút nhiều hay trỏ kém) → quyết\ngắn thành phần cho có tác dụng,\nkhông gắn theo cảm tính.", { x: 7.18, y: 3.2, w: 5.0, h: 1.4, fontSize: 13, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
text("Không nhánh nào là ngõ cụt", { x: M, y: 5.0, w: 8, h: 0.4, fontSize: 14, bold: true, color: INK, fontFace: TF, margin: 0 });
const fb = [
  ["Bộ trỏ không đạt ~80%", "chấm nhóm nút có chữ + nêu giới hạn (tự nó thành một phát hiện)"],
  ["Mô hình chỉ HOÀ baseline", "“3B offline ngang mô hình API lớn” vẫn bảo vệ được"],
  ["Tính mới bị vặn", "trục mới = thước executability cho hướng dẫn sinh ra, không phải “tác vụ đầu tiên”"],
];
let fy = 5.45;
fb.forEach(r => {
  rect(M, fy, W - 2 * M, 0.44, WHITE, { radius: 0.06, line: RULE, lw: 1 });
  text([{ text: r[0] + "  ", options: { bold: true, color: BAD } }, { text: "→ " + r[1], options: { color: BODY } }], { x: M + 0.25, y: fy, w: W - 2 * M - 0.5, h: 0.44, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0 });
  fy += 0.5;
});
note(`Hai cổng go/no-go chạy trước khi tiêu tiền huấn luyện, chỉ chạy mô hình nên rẻ. Cổng A: bộ trỏ chuyên phải ~80% trên câu đúng. Cổng B: đo mô hình nền yếu ở đâu để chọn thành phần.
Nhẹ gánh cho Cổng A: cái cần là HIỆU SỐ Student − baseline qua cùng bộ trỏ, lỗi bộ trỏ phần lớn triệt tiêu → bộ trỏ 70% vẫn so được.
Đường lui: không nhánh nào là ngõ cụt — bộ trỏ yếu, mô hình chỉ hoà, hay tính mới bị vặn đều có lối.`);
pageno(); done();

// ===================================================== 10 · DANG O DAU
slide();
head("Đang ở đâu", "Phần đo/kiểm miễn phí đã làm xong — còn phần huấn luyện trên Colab");
text("ĐÃ XONG (miễn phí)", { x: M, y: 2.5, w: 5.5, h: 0.4, fontSize: 14, bold: true, color: GOOD, fontFace: BF, spacing: 1, margin: 0 });
["Định hình thiết kế + chọn trục độ ĐÚNG", "Tự loại cách đo đơn giản đầu tiên (so chữ, AUC 0.34)", "Đo thước mới: phân biệt rõ câu tốt/dở (sàn 6.6% · chênh 44.7)", "Đo mật độ nút trên AndroidControl (63%)", "Xác nhận chỗ trống còn thật (sau GuideMe)"].forEach((t, i) => {
  text("✓", { x: M, y: 3.0 + i * 0.6, w: 0.4, h: 0.4, fontSize: 15, bold: true, color: GOOD, fontFace: BF, margin: 0 });
  text(t, { x: M + 0.42, y: 3.0 + i * 0.6, w: 5.3, h: 0.5, fontSize: 13, color: BODY, fontFace: BF, valign: "middle", margin: 0 });
});
text("CÒN LẠI (theo thứ tự)", { x: 7.1, y: 2.5, w: 5.3, h: 0.4, fontSize: 14, bold: true, color: ACCENT, fontFace: BF, spacing: 1, margin: 0 });
["Khảo sát với người thật, 91 cặp (free, tự chấm)", "Phép thử chọn thành phần (Cổng B)", "Cổng bộ trỏ trên Colab (~$10)", "Gặp thầy — thống nhất hướng", "Dựng data → train → chấm hai thước"].forEach((t, i) => {
  text("○", { x: 7.1, y: 3.0 + i * 0.6, w: 0.4, h: 0.4, fontSize: 15, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
  text(t, { x: 7.52, y: 3.0 + i * 0.6, w: 4.9, h: 0.5, fontSize: 13, color: BODY, fontFace: BF, valign: "middle", margin: 0 });
});
rect(M, 6.25, W - 2 * M, 0.55, FILL, { radius: 0.08 });
text([{ text: "Chi phí:  ", options: { bold: true, color: INK } }, { text: "cổng ~$10 · huấn luyện QLoRA 3B ~$60–70 cả pha (Colab).", options: { color: BODY } }], { x: M + 0.3, y: 6.25, w: W - 2 * M - 0.6, h: 0.55, fontSize: 13, fontFace: BF, valign: "middle", margin: 0 });
note(`Trạng thái: phần đo và kiểm miễn phí đã làm xong — hướng đã định hình, tự loại cách đo đơn giản ban đầu, đo thước mới phân biệt được câu tốt/dở, đo mật độ trên AndroidControl, xác nhận chỗ trống còn thật.
Còn lại theo thứ tự: khảo sát với người thật 91 cặp (tự chấm, free), phép thử chọn thành phần, cổng bộ trỏ trên Colab, gặp thầy, rồi mới train. Chi phí toàn pha chỉ ~$70.`);
pageno(); done();

// ===================================================== 11 · NAM CAU HOI
slide(NAVY);
text("NHỮNG ĐIỂM XIN TRAO ĐỔI", { x: M, y: 1.7, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Một hướng đề xuất, đã kiểm bằng số —\nNăm điểm xin trao đổi thêm", { x: M, y: 2.15, w: 11.4, h: 1.4, fontSize: 24, bold: true, color: WHITE, fontFace: TF, lh: 1.12, margin: 0 });
const qs = [
  "Khung hai trụ (mô hình + đánh giá) — có hợp lý không? Trụ nào nên là chính?",
  "Dùng đánh giá tự động (executability + bơm lỗi) làm cổng đậu/rớt, không lệ thuộc chấm người — hướng này ổn không?",
  "Nếu mô hình chỉ HOÀ mốc ngoài → “3B chạy offline ngang mô hình API lớn” có đủ không?",
  "Định vị sau GuideMe: “mô hình nhỏ ĐƯỢC HUẤN LUYỆN + bộ đánh giá tái lập được đầu tiên” — đủ mới?",
  "Với khung này, đã đủ tầm luận văn thạc sĩ chưa, hay thêm/bớt đâu?",
];
let qy = 3.75;
qs.forEach((q, i) => {
  circle(M, qy, 0.42, ACCENT, String(i + 1), WHITE);
  text(q, { x: M + 0.62, y: qy - 0.06, w: 11.2, h: 0.55, fontSize: 14.5, color: "E6ECF2", fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
  qy += 0.62;
});
note(`Kết: một hướng đề xuất, đã kiểm được bằng số. Năm câu chỉ thầy quyết được:
1. Khung hai trụ, trụ nào chính. 2. Đồng ý dùng đánh giá tự động (executability + bơm lỗi) làm cổng. 3. Kịch bản hoà thì "3B ngang API lớn" có đủ không. 4. Định vị sau GuideMe đã đủ mới chưa. 5. Đủ tầm thạc sĩ chưa.
Đây là những chuyện không đo bằng số được, cần thầy định hướng trước khi lên Colab.`);
pageno(); done();

// ---- write ----
fs.mkdirSync("_preview_v6", { recursive: true });
const page = `<!doctype html><meta charset="utf-8"><style>@page{size:${W}in ${H}in;margin:0}*{margin:0;box-sizing:border-box}.slide{position:relative;width:${W}in;height:${H}in;overflow:hidden;page-break-after:always}</style>` + htmlSlides.join("\n");
fs.writeFileSync("_preview_v6/preview.html", page);
pres.writeFile({ fileName: "../LUAN_VAN_SLIDE_v6.pptx" }).then(f => console.log("PPTX ->", f, "| slides:", htmlSlides.length)).catch(e => console.error("ERR", e));
