// Deck v5 — trạng thái hiện tại (phương án LAI): bài toán · 4 phép thử · thiết kế · kiểm-bằng-số.
// Soạn từ report/81/83/84/85/86/88. Dual-emit: ../LUAN_VAN_SLIDE_v5.pptx + _preview_v5/preview.html
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
function chip(x, y, w, glyph, gc, t, sub) {
  rect(x, y, w, 1.5, FILL, { radius: 0.09 });
  text(glyph, { x: x + 0.22, y: y + 0.2, w: 0.6, h: 0.6, fontSize: 26, bold: true, color: gc, fontFace: TF, margin: 0 });
  text(t, { x: x + 0.9, y: y + 0.2, w: w - 1.1, h: 0.5, fontSize: 14.5, bold: true, color: INK, fontFace: BF, margin: 0, valign: "middle" });
  text(sub, { x: x + 0.9, y: y + 0.68, w: w - 1.1, h: 0.72, fontSize: 12.5, color: BODY, fontFace: BF, margin: 0, lh: 1.25 });
}

// ===================================================== 1 · TITLE
slide(NAVY);
text("LUẬN VĂN THẠC SĨ · BÁO CÁO TIẾN ĐỘ", { x: M, y: 1.45, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Sinh hướng dẫn sử dụng\nphần mềm cho người đọc", { x: M - 0.02, y: 2.1, w: 9.6, h: 1.9, fontSize: 33, bold: true, color: WHITE, fontFace: TF, lh: 1.08, margin: 0 });
text("Từ một ảnh màn hình + câu hỏi → các bước cho người làm theo", { x: M, y: 4.25, w: 9.4, h: 0.6, fontSize: 16, italic: true, color: "C9D2DC", fontFace: TF, margin: 0 });
text("Học viên · · · · ·        Giảng viên hướng dẫn · · · · ·        2026", { x: M, y: 6.55, w: 11, h: 0.4, fontSize: 13, color: "8FA0B2", fontFace: BF, margin: 0 });
shot("real_mv_1.png", 10.5, 1.9, 1.9, 3.35);
done();

// ===================================================== 2 · BAI TOAN
slide();
head("Bài toán", "Người dùng đưa một màn hình + một câu hỏi");
shot("real_mv_2.png", M, 2.5, 2.5, 4.3);
rect(4.0, 2.55, 8.4, 1.55, TINT, { radius: 0.1 });
text([{ text: "Câu hỏi:  ", options: { bold: true, color: ACCENT } }, { text: "“Làm sao để bật thông báo cho tập mới?”", options: { color: INK, italic: true } }], { x: 4.3, y: 2.55, w: 7.9, h: 0.7, fontSize: 15.5, fontFace: BF, valign: "middle", margin: 0 });
text([{ text: "Trả lời mong muốn:  ", options: { bold: true, color: STEEL } }, { text: "1. Chạm Settings  →  2. Chạm Notifications  →  3. Bật New episode alerts", options: { color: BODY } }], { x: 4.3, y: 3.25, w: 7.9, h: 0.7, fontSize: 14, fontFace: BF, valign: "middle", margin: 0, lh: 1.2 });
text("Hai cái khó cốt lõi", { x: 4.0, y: 4.4, w: 8, h: 0.4, fontSize: 15, bold: true, color: INK, fontFace: TF, margin: 0 });
chip(4.0, 4.9, 4.1, "?", STEEL, "Không có đáp án mẫu", "Không sẵn bộ hướng dẫn chuẩn do\nngười soạn — không chấm kiểu thường được.");
chip(8.3, 4.9, 4.1, "!", BAD, "Bịa nút không có thật", "Nói “chạm Preferences” khi màn chỉ có\n“Settings” — người dùng bấm nhầm.");
note(`Bài toán: vào là 1 ảnh màn hình + 1 câu hỏi, ra là các bước cụ thể cho người đọc làm theo.
Hai cái khó: (1) không có đáp án mẫu do người soạn để chấm; (2) mô hình hay bịa tên nút không tồn tại — lỗi này nguy hiểm vì đọc lên vẫn trơn tru.
Đây cũng là ràng buộc của thầy: luận văn phải có một mô hình do em tự huấn luyện, không chỉ gọi công cụ có sẵn.`);
pageno(); done();

// ===================================================== 3 · HUONG BAN DAU
slide();
head("Hướng ban đầu", "Thầy giáo hay bịa — lọc sạch rồi mới dạy học trò");
rect(M, 2.55, 3.7, 2.5, FILL, { radius: 0.1 });
text("Thầy giáo", { x: M + 0.28, y: 2.75, w: 3.2, h: 0.4, fontSize: 15.5, bold: true, color: STEEL, fontFace: TF, margin: 0 });
text("gpt-4o-mini (gọi qua mạng)\n\nViết nháp hướng dẫn —\nđôi khi bịa tên nút.", { x: M + 0.28, y: 3.2, w: 3.2, h: 1.7, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
arrow(4.75, 3.8, 0.5);
rect(5.4, 2.55, 3.4, 2.5, FILL, { radius: 0.1 });
text("Lọc bịa", { x: 5.68, y: 2.75, w: 2.9, h: 0.4, fontSize: 15.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Đối chiếu tên nút với\nView Hierarchy — danh sách\nnút thật của màn do hệ\nđiều hành cấp.\nChỗ bịa → viết lại chung.", { x: 5.68, y: 3.2, w: 2.9, h: 1.7, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
arrow(8.95, 3.8, 0.5);
rect(9.6, 2.55, 2.8, 2.5, TINT, { radius: 0.1 });
text("Học trò", { x: 9.88, y: 2.75, w: 2.3, h: 0.4, fontSize: 15.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Qwen2.5-VL-3B\ntự huấn luyện, chạy\ntrên máy.\n\n→ sản phẩm chính.", { x: 9.88, y: 3.2, w: 2.3, h: 1.7, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
rect(M, 5.5, W - 2 * M, 1.15, WHITE, { radius: 0.1, line: RULE, lw: 1 });
text([{ text: "Tiền đề: ", options: { bold: true, color: ACCENT } }, { text: "thầy giáo bịa nhiều → lọc bỏ → học trò trung thực hơn.  ", options: { color: INK } }, { text: "Nhưng có đúng không? Phải kiểm trước khi tiêu tiền.", options: { color: BODY, italic: true } }], { x: M + 0.3, y: 5.5, w: W - 2 * M - 0.6, h: 1.15, fontSize: 14.5, fontFace: BF, valign: "middle", lh: 1.3, margin: 0 });
note(`Ý tưởng ban đầu để có mô hình tự train: thầy giáo (gpt-4o-mini) viết nháp, mình đối chiếu với View Hierarchy — file hệ điều hành liệt kê nút thật trên màn — chỗ nào bịa thì viết lại thành câu chung chung, rồi dạy học trò từ phần đã lọc.
Điểm quan trọng để nói với thầy: trước khi tiêu tiền huấn luyện, em chạy mấy phép thử miễn phí để KIỂM cái tiền đề này. Và nó lật ra vài chuyện bất ngờ — slide sau.`);
pageno(); done();

// ===================================================== 4 · BON PHEP THU (buoc ngoat)
slide(NAVY);
text("BƯỚC NGOẶT", { x: M, y: 0.72, w: 11, h: 0.3, fontSize: 12.5, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Hai phép thử lật cả kế hoạch — làm trước khi tiêu tiền", { x: M, y: 1.08, w: 11.5, h: 0.7, fontSize: 25, bold: true, color: WHITE, fontFace: TF, margin: 0 });
rect(M, 2.3, 5.5, 3.7, "1E2C46", { radius: 0.1 });
text("K1 — Bộ đối chiếu YẾU", { x: M + 0.3, y: 2.55, w: 4.9, h: 0.4, fontSize: 16, bold: true, color: "F0C9A8", fontFace: TF, margin: 0 });
text("Sai CẢ HAI chiều:", { x: M + 0.3, y: 3.05, w: 4.9, h: 0.35, fontSize: 13.5, bold: true, color: "D8DEE6", fontFace: BF, margin: 0 });
text("• Cho qua bịa nghe giống thật\n   (“Send” khi màn chỉ có “Save”)\n• Đánh oan nút gọi đúng mà\n   khác chữ (“Tìm kiếm”→“Search”)\n\n→ điểm hai loại trùng nhau\n   → không ngưỡng nào tách được.", { x: M + 0.3, y: 3.45, w: 4.9, h: 2.4, fontSize: 13.5, color: "C6CFDA", fontFace: BF, lh: 1.35, margin: 0 });
rect(6.8, 2.3, 5.6, 3.7, "1E2C46", { radius: 0.1 });
text("K2 — Thầy giáo gần như KHÔNG bịa", { x: 7.1, y: 2.55, w: 5.0, h: 0.4, fontSize: 16, bold: true, color: "F0C9A8", fontFace: TF, margin: 0 });
text("Đếm tay 80 màn thật:", { x: 7.1, y: 3.05, w: 5.0, h: 0.35, fontSize: 13.5, bold: true, color: "D8DEE6", fontFace: BF, margin: 0 });
text("• Chỉ ~0–2% bước là bịa thật,\n   KHÔNG phải “một phần tư”\n• 35 trên 40 ca bị đánh “bịa”\n   thật ra là NÚT CÓ THẬT\n\n→ tiền đề “lọc bịa” lung lay:\n   gần như không có gì để lọc.", { x: 7.1, y: 3.45, w: 5.0, h: 2.4, fontSize: 13.5, color: "C6CFDA", fontFace: BF, lh: 1.35, margin: 0 });
text("(Thêm hai phép thử: OCR bù nhãn chỉ được một nửa · câu chung chung thì mơ hồ, lặp lại câu hỏi.)", { x: M, y: 6.35, w: 11.5, h: 0.5, fontSize: 13, italic: true, color: "9FB0C2", fontFace: BF, margin: 0 });
note(`Đây là slide quan trọng nhất — bước ngoặt của cả luận văn.
K1: em kiểm cái bộ đối chiếu (thuật toán bắt bịa). Nó sai cả hai chiều — vừa bỏ lọt bịa nghe-giống, vừa đánh oan nút gọi-đúng-bằng-từ-khác — và hai loại chồng điểm nhau nên không ngưỡng nào tách được. Đây là hạn chế bản chất của đo-độ-gần-nghĩa.
K2: em đếm tay xem thầy giáo bịa thật bao nhiêu — hoá ra gần như không bịa (~0-2%), không phải một phần tư như tưởng. Những chỗ bị đánh bịa thật ra là nút có thật mà View Hierarchy bỏ sót nhãn.
Hệ quả: tiền đề "lọc bịa" lung lay → phải đổi hướng. Điểm cần nhấn: mấy phép thử này MIỄN PHÍ, và nó cứu em khỏi tiêu tiền train nhầm hướng.`);
pageno(); done();

// ===================================================== 5 · DOI HUONG
slide();
head("Đổi hướng", "Từ “lọc bịa” sang đo “hướng dẫn có ĐÚNG không”");
rect(M, 2.6, 5.35, 3.0, FILL, { radius: 0.1 });
text("Trước", { x: M + 0.3, y: 2.82, w: 4.7, h: 0.4, fontSize: 15, bold: true, color: MUTE, fontFace: TF, margin: 0 });
text("Trụ chính = quy trình lọc bịa.\n\nNhưng thầy giáo không bịa →\nphép so “học từ data lọc vs\ndata thô” dễ ra “không khác gì”\nvì lý do tầm thường.", { x: M + 0.3, y: 3.3, w: 4.75, h: 2.1, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
arrow(6.5, 4.1, 0.55);
rect(7.35, 2.6, 5.05, 3.0, TINT, { radius: 0.1 });
text("Sau (phương án lai)", { x: 7.65, y: 2.82, w: 4.4, h: 0.4, fontSize: 15, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Trụ chính = đo độ ĐÚNG,\ndùng bộ AndroidControl vì nó\nCÓ SẴN đáp án đúng do người\nthật làm.\n\nĐộ trung thực (bịa nút) → trụ phụ.", { x: 7.65, y: 3.3, w: 4.4, h: 2.1, fontSize: 13.5, color: INK, fontFace: BF, lh: 1.35, margin: 0 });
text([{ text: "Hai bộ, hai vai: ", options: { bold: true, color: ACCENT } }, { text: "MobileViews không có đáp án → đo độ trung thực (không cần đáp án). AndroidControl CÓ đáp án người-làm → đo độ đúng.", options: { color: BODY } }], { x: M, y: 6.0, w: W - 2 * M, h: 0.6, fontSize: 13.5, fontFace: BF, align: "center", margin: 0 });
note(`Vì tiền đề lọc-bịa lung lay, em đổi trọng tâm: lấy "độ ĐÚNG" làm trụ chính.
Độ đúng đo được vì bộ AndroidControl có sẵn đáp án đúng do người thật làm — khác MobileViews vốn không có đáp án.
Phân biệt: độ ĐÚNG = hướng dẫn có dẫn tới đích không; độ TRUNG THỰC = có bịa nút không. Hai cái khác nhau. Độ trung thực vẫn giữ nhưng làm trụ phụ.`);
pageno(); done();

// ===================================================== 6 · THIET KE CUOI
slide();
head("Thiết kế cuối", "Một mô hình · hai nguồn · đo trên app chưa từng thấy");
// train row
rect(M, 2.5, 3.5, 1.5, FILL, { radius: 0.09 });
text("AndroidControl", { x: M + 0.2, y: 2.62, w: 3.1, h: 0.35, fontSize: 13.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("ảnh + hướng-dẫn-người\n(tín hiệu CHÍNH)", { x: M + 0.2, y: 3.0, w: 3.1, h: 0.9, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
rect(M, 4.15, 3.5, 1.4, FILL, { radius: 0.09 });
text("MobileViews", { x: M + 0.2, y: 4.27, w: 3.1, h: 0.35, fontSize: 13.5, bold: true, color: STEEL, fontFace: TF, margin: 0 });
text("chưng cất + lọc\n(dữ liệu phụ, bật/tắt)", { x: M + 0.2, y: 4.62, w: 3.1, h: 0.8, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
arrow(4.55, 4.05, 0.55);
rect(5.3, 3.05, 3.0, 2.0, NAVY, { radius: 0.1 });
text("Qwen2.5-VL-3B", { x: 5.45, y: 3.5, w: 2.7, h: 0.5, fontSize: 15, bold: true, color: WHITE, fontFace: TF, align: "center", margin: 0 });
text("QLoRA · trên Colab", { x: 5.45, y: 4.05, w: 2.7, h: 0.4, fontSize: 12.5, color: "C9D2DC", fontFace: BF, align: "center", margin: 0 });
arrow(8.45, 4.05, 0.55);
rect(9.2, 3.05, 3.2, 2.0, TINT, { radius: 0.1 });
text("ĐO độ ĐÚNG", { x: 9.35, y: 3.28, w: 2.9, h: 0.4, fontSize: 14, bold: true, color: ACCENT, fontFace: TF, align: "center", margin: 0 });
text("trên app MỚI của chính\nAndroidControl (cùng phân\nphối, khác app — chuẩn\nngành; cross-dataset để sau)", { x: 9.35, y: 3.72, w: 2.9, h: 1.2, fontSize: 12.5, color: INK, fontFace: BF, align: "center", lh: 1.25, margin: 0 });
rect(M, 5.75, W - 2 * M, 0.95, FILL, { radius: 0.09 });
text([{ text: "So sánh:  ", options: { bold: true, color: ACCENT } }, { text: "Học trò (tự train)  vs  Thầy-giáo-gốc (gpt-4o-mini chưa chỉnh)  —  học trò có lợi thế sân nhà vì train ngay trên AndroidControl.", options: { color: INK } }], { x: M + 0.3, y: 5.75, w: W - 2 * M - 0.6, h: 0.95, fontSize: 13.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
note(`Thiết kế cuối: một mô hình, tín hiệu chính là hướng-dẫn-người của AndroidControl; MobileViews-chưng-cất làm dữ liệu phụ (có thí nghiệm bật/tắt để tách công của nó).
Điểm khác quan trọng so với bản trước: đo NGAY trên app chưa-từng-thấy của chính AndroidControl (in-distribution) — bỏ được lỗ hổng "học một nơi chấm một nơi".
So Học trò với Thầy-giáo-gốc: học trò train ngay trên bộ này nên có lợi thế sân nhà, nên kỳ vọng nó hơn thầy giáo về độ đúng là hợp lý.`);
pageno(); done();

// ===================================================== 7 · THUOC MOI (va bay K1)
slide();
head("Cách chấm độ đúng", "Mượn step-accuracy + thêm luật khớp-đích để né bẫy K1");
rect(M, 2.6, W - 2 * M, 1.5, FILL, { radius: 0.1 });
text([{ text: "“Bấm vào tab Gmail”", options: { bold: true, color: INK } }, { text: "   →   thao-tác = ", options: { color: BODY } }, { text: "chạm", options: { bold: true, color: STEEL } }, { text: "   ·   đích = ", options: { color: BODY } }, { text: "Gmail tab", options: { bold: true, color: ACCENT } }], { x: M + 0.3, y: 2.78, w: W - 2 * M - 0.6, h: 0.5, fontSize: 15.5, fontFace: BF, valign: "middle", margin: 0 });
text([{text:"Đúng ⇔ đúng thao-tác VÀ đúng đích (so từ-lõi). ",options:{color:BODY}},{text:"Đây là proxy tính-ĐÚNG của bước; độ hữu-ích cho người đo riêng bằng người-chấm.",options:{italic:true,color:STEEL}}], { x: M + 0.3, y: 3.35, w: W - 2 * M - 0.6, h: 0.55, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh:1.2 });
rect(M, 4.4, 5.5, 2.25, WHITE, { radius: 0.1, line: BAD, lw: 1.5 });
text("Vì sao K1 chết", { x: M + 0.3, y: 4.6, w: 4.9, h: 0.4, fontSize: 14.5, bold: true, color: BAD, fontFace: TF, margin: 0 });
text("Đo cả câu bằng embedding →\n“tab Gmail” và “tab Calendar”\nrất gần → tưởng khớp → cho qua.", { x: M + 0.3, y: 5.05, w: 4.9, h: 1.4, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
rect(6.9, 4.4, 5.5, 2.25, WHITE, { radius: 0.1, line: GOOD, lw: 1.5 });
text("Vì sao thước mới sống", { x: 7.2, y: 4.6, w: 4.9, h: 0.4, fontSize: 14.5, bold: true, color: GOOD, fontFace: TF, margin: 0 });
text("Tách đích ra rồi so từ-lõi →\nGmail ≠ Calendar → KHÔNG khớp\n→ bắt được lỗi. Cái đo-cả-câu\nkhông làm nổi.", { x: 7.2, y: 5.05, w: 4.9, h: 1.4, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
note(`Thước mới không đo độ-gần-nghĩa cả câu (chỗ K1 chết) mà tách mỗi bước thành thao-tác + đích, rồi khớp đích bằng từ-lõi.
"tab Gmail" và "tab Calendar" chung từ "tab" nhưng khác từ lõi (Gmail vs Calendar) → thước bắt được sự khác biệt, dù embedding thấy chúng gần.
Slide sau: em kiểm cái này bằng số, không chỉ nói suông.`);
pageno(); done();

// ===================================================== 8 · KIEM BANG SO
slide();
head("Hạ tầng đã sẵn — kiểm bằng số", "Số của SETUP (thước, lực, khả thi) — chưa phải kết quả model");
function stat(x, big, bc, lab, sub) {
  rect(x, 2.6, 2.72, 3.4, FILL, { radius: 0.1 });
  text(big, { x: x, y: 3.0, w: 2.72, h: 1.0, fontSize: 40, bold: true, color: bc, fontFace: TF, align: "center", margin: 0 });
  text(lab, { x: x + 0.2, y: 4.15, w: 2.32, h: 0.5, fontSize: 14, bold: true, color: INK, fontFace: BF, align: "center", margin: 0 });
  text(sub, { x: x + 0.2, y: 4.7, w: 2.32, h: 1.15, fontSize: 12, color: BODY, fontFace: BF, align: "center", lh: 1.3, margin: 0 });
}
stat(M, "1.00", GOOD, "Thước qua cổng", "AUC trên tập chuẩn\n(bơm-lỗi, có ca khó\ntự dữ liệu) — chưa\nphải điểm model.");
stat(M + 2.92, "8–9", ACCENT, "Đủ lực (điểm %)", "Mức nhỏ nhất nhìn\nthấy được — dưới\nngưỡng nguy hiểm 15–20.");
stat(M + 5.84, "30%", STEEL, "Không sàn-0", "Thầy giáo đạt 30%\nđộ đúng → trục đo\nđược, không suy biến.");
stat(M + 8.76, "✓", GOOD, "Không bị scoop", "Chỗ trống còn thật;\nđã tra + tải thẳng\nbài đối thủ gần nhất.");
note(`Đây là chỗ em muốn nhấn: mọi giả định lớn đã được ĐO, không phải đoán.
1.00 = thước mới tách sạch lỗi-sai-đích khỏi paraphrase, kể cả ca khó — tức nó giải được đúng chỗ K1 chết.
8-9 điểm phần trăm = mức chênh lệch nhỏ nhất thí nghiệm nhìn thấy được, dưới ngưỡng nguy hiểm → đủ lực thống kê.
30% = thầy giáo đạt 30% độ đúng, không phải 0 → trục đo được.
Không bị scoop = em tra văn liệu + tải thẳng bài gần nhất (GUITrans2Act) để chắc nó khác.`);
pageno(); done();

// ===================================================== 9 · HAI DONG GOP
slide();
head("Hai đóng góp", "Ngang nhau — bổ trợ nhau");
rect(M, 2.7, 5.5, 3.2, TINT, { radius: 0.1 });
circle(M + 0.35, 3.0, 0.55, ACCENT, "1", WHITE);
text("MÔ HÌNH", { x: M + 1.15, y: 3.02, w: 4.2, h: 0.45, fontSize: 16, bold: true, color: ACCENT, fontFace: TF, margin: 0, valign: "middle" });
text("Sinh hướng dẫn nhiều bước CHO\nNGƯỜI ĐỌC + ràng buộc trung thực\n— khác hướng chủ đạo (sinh thao-tác\ncho MÁY tự bấm).\n\nCái mới ở TÁC VỤ + cách đo,\nkhông ở “3B on-device”.", { x: M + 0.35, y: 3.75, w: 4.9, h: 2.4, fontSize: 13.5, color: INK, fontFace: BF, lh: 1.32, margin: 0 });
rect(6.85, 2.7, 5.55, 3.2, FILL, { radius: 0.1 });
circle(7.2, 3.0, 0.55, STEEL, "2", WHITE);
text("ĐÁNH GIÁ", { x: 8.0, y: 3.02, w: 4.2, h: 0.45, fontSize: 16, bold: true, color: STEEL, fontFace: TF, margin: 0, valign: "middle" });
text("Cặp thước: trung thực (đối chiếu\nVH) + đúng (so đáp án).\n\nPhát hiện tái-dùng-được: View\nHierarchy KHÔNG đủ tin làm chuẩn\nvàng — 35/40 ca “bịa” thật ra\nlà VH thiếu nhãn.", { x: 7.2, y: 3.75, w: 5.0, h: 2.4, fontSize: 13.5, color: INK, fontFace: BF, lh: 1.32, margin: 0 });
note(`Hai đóng góp ngang nhau. (1) Mô hình đầu tiên sinh hướng dẫn cho NGƯỜI — mọi mô hình khác sinh thao tác cho máy. Cái mới ở tác vụ, không ở kích thước. Đây là chỗ thoả ràng buộc train-model của thầy. (2) Phương pháp đánh giá kép + phát hiện thực nghiệm về vì sao đo ngây thơ hỏng.
Nếu thầy hỏi "3B on-device có gì mới" — trả lời thẳng: đó không phải điểm mới, điểm mới là tác vụ + cách đánh giá.`);
pageno(); done();

// ===================================================== 10 · DA LAM vs CON LAI
slide();
head("Đang ở đâu", "Chuẩn bị + kiểm chứng xong — còn pha huấn luyện (~3–4 tuần)");
text("ĐÃ XONG (miễn phí)", { x: M, y: 2.5, w: 5.5, h: 0.4, fontSize: 14, bold: true, color: GOOD, fontFace: BF, spacing: 1, margin: 0 });
["Chốt thiết kế + bản đăng-ký-trước (đã lưu)", "Tải dữ liệu AndroidControl về máy", "Kiểm thước qua cổng bơm-lỗi (AUC 1.0)", "Đo đủ lực thống kê (MDE 8–9%)", "Xác nhận không bị scoop"].forEach((t, i) => {
  text("✓", { x: M, y: 3.0 + i * 0.62, w: 0.4, h: 0.4, fontSize: 15, bold: true, color: GOOD, fontFace: BF, margin: 0 });
  text(t, { x: M + 0.42, y: 3.0 + i * 0.62, w: 5.1, h: 0.5, fontSize: 13.5, color: BODY, fontFace: BF, valign: "middle", margin: 0 });
});
text("CÒN LẠI (pha Colab)", { x: 7.1, y: 2.5, w: 5.3, h: 0.4, fontSize: 14, bold: true, color: ACCENT, fontFace: BF, spacing: 1, margin: 0 });
["Dựng dữ liệu huấn luyện", "Chạy thử nhỏ 20 mẫu (rẻ)", "Huấn luyện 2 bản mô hình", "Chấm độ đúng + độ trung thực", "Hiệu chỉnh thước với output thật"].forEach((t, i) => {
  text("○", { x: 7.1, y: 3.0 + i * 0.62, w: 0.4, h: 0.4, fontSize: 15, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
  text(t, { x: 7.52, y: 3.0 + i * 0.62, w: 4.9, h: 0.5, fontSize: 13.5, color: BODY, fontFace: BF, valign: "middle", margin: 0 });
});
note(`Trạng thái: toàn bộ khâu chuẩn bị + kiểm chứng đã xong, đều miễn phí (trừ pilot MDE tốn ~nửa đô).
Còn lại là pha huấn luyện trên Colab — dựng dữ liệu, chạy thử, train hai bản mô hình, chấm. Em sẽ chạy pha này sau khi trao đổi với thầy.`);
pageno(); done();

// ===================================================== 11 · KET
slide(NAVY);
text("XIN Ý KIẾN THẦY", { x: M, y: 2.3, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Thiết kế đã chốt và kiểm được bằng số.\nEm xin ý kiến thầy về cách kể đóng góp", { x: M, y: 2.85, w: 11.2, h: 1.5, fontSize: 25, bold: true, color: WHITE, fontFace: TF, lh: 1.15, margin: 0 });
text("• Đồng ý lấy độ ĐÚNG làm trụ chính, độ trung thực làm trụ phụ?\n• Cách kể tính mới (mô hình cho tác-vụ-mới + đánh giá) đã ổn để bảo vệ chưa?\n• Có nên đầu tư thêm ở đâu trước khi lên Colab huấn luyện?", { x: M, y: 4.6, w: 11, h: 1.8, fontSize: 15.5, color: "D8DEE6", fontFace: BF, lh: 1.5, margin: 0 });
note(`Kết: thiết kế đã chốt và kiểm được bằng số. Em xin ý kiến thầy ba chuyện: (1) đồng ý lấy độ ĐÚNG làm trụ chính không; (2) cách kể tính mới đã đủ bảo vệ chưa; (3) có nên đầu tư thêm chỗ nào trước khi lên Colab.
Đây là mấy câu chỉ thầy quyết được, không đo bằng số được.`);
pageno(); done();

// ---- write ----
fs.mkdirSync("_preview_v5", { recursive: true });
const page = `<!doctype html><meta charset="utf-8"><style>@page{size:${W}in ${H}in;margin:0}*{margin:0;box-sizing:border-box}.slide{position:relative;width:${W}in;height:${H}in;overflow:hidden;page-break-after:always}</style>` + htmlSlides.join("\n");
fs.writeFileSync("_preview_v5/preview.html", page);
pres.writeFile({ fileName: "../LUAN_VAN_SLIDE_v5.pptx" }).then(f => console.log("PPTX ->", f, "| slides:", htmlSlides.length)).catch(e => console.error("ERR", e));
