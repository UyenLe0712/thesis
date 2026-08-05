// Deck v12 — soan lai tu report/43. Tieu chi: IT CHU, NHIEU HINH, giong nguoi viet.
// Khong ke gach chan duoi tieu de (skill pptx: dau hieu AI). Moi slide co yeu to hinh anh.
// Noi "mot man / nhieu man", khong dung "DG1/DG2". Tranh tu ghep-noi-gach-noi, an du vo thuat.
// Dual-emit: xuat ../LUAN_VAN_SLIDE_v2.pptx  +  _preview/preview.html (de QA bo cuc bang weasyprint).
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Luan van thac si";
pres.title = "Sinh tu dong huong dan su dung phan mem";

// ---- palette (chu de: phan mem di dong / huong dan su dung) ----
const TF = "Cambria", BF = "Segoe UI";
const INK = "1D2733", BODY = "454C55", MUTE = "8B929B";
const ACCENT = "BE5A2E", STEEL = "52657A", GOOD = "1E6B43";
const RULE = "DBE0E6", FILL = "F3F5F7", TINT = "F7EBE3", NAVY = "17233B", WHITE = "FFFFFF";
const W = 13.33, H = 7.5, M = 0.92;

// ---- HTML preview mirror (chi de QA, khong phai ban giao) ----
const PX = 96;
const FMAP = { "Cambria": "'DejaVu Serif',serif", "Segoe UI": "'DejaVu Sans',sans-serif" };
let htmlSlides = [], cur = "";
function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function plain(c) { return typeof c === "string" ? c : c.map(r => r.text).join(""); }
function hpush(html) { cur += html; }

let s, PAGE = 0;
function slide(bg) {
  if (cur) htmlSlides.push(cur);
  s = pres.addSlide(); s.background = { color: bg || WHITE };
  cur = `<div class="slide" style="background:#${bg || WHITE}">`;
}
function done() { if (cur) { htmlSlides.push(cur + "</div>"); cur = ""; } }

// text(content, {x,y,w,h,size,bold,italic,color,align,valign,face,lh,spacing,margin})
function text(content, o) {
  const opt = Object.assign({ x: 0, y: 0, w: 4, h: 1, fontSize: 14, color: BODY, fontFace: BF,
    align: "left", valign: "top", margin: o.margin != null ? o.margin : 4 }, o);
  if (o.lh) opt.lineSpacingMultiple = o.lh;
  if (o.spacing) opt.charSpacing = o.spacing;
  s.addText(content, opt);
  // html
  const jc = opt.align === "center" ? "center" : opt.align === "right" ? "flex-end" : "flex-start";
  const ai = opt.valign === "middle" ? "center" : opt.valign === "bottom" ? "flex-end" : "flex-start";
  const pad = (opt.margin || 0) / PX;
  const st = `position:absolute;left:${o.x * PX}px;top:${o.y * PX}px;width:${o.w * PX}px;height:${o.h * PX}px;`
    + `display:flex;justify-content:${jc};align-items:${ai};padding:${pad}in;box-sizing:border-box;`
    + `font-family:${FMAP[opt.fontFace]};font-size:${opt.fontSize}px;color:#${opt.color};`
    + `text-align:${opt.align};line-height:${o.lh || 1.15};`
    + (opt.bold ? "font-weight:700;" : "") + (opt.italic ? "font-style:italic;" : "")
    + (opt.spacing ? `letter-spacing:${opt.spacing * 0.7}px;` : "");
  hpush(`<div style="${st}"><div style="white-space:pre-line;width:100%">${esc(plain(content))}</div></div>`);
}
function rect(x, y, w, h, fill, o) {
  o = o || {};
  const shp = o.radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE;
  const p = { x, y, w, h, fill: fill === "none" ? { type: "none" } : { color: fill }, line: o.line ? { color: o.line, width: o.lw || 1 } : { type: "none" } };
  if (o.radius) p.rectRadius = o.radius;
  if (o.shadow) p.shadow = { type: "outer", color: "9AA3AD", blur: 7, offset: 3, angle: 90, opacity: 0.28 };
  s.addShape(shp, p);
  const st = `position:absolute;left:${x * PX}px;top:${y * PX}px;width:${w * PX}px;height:${h * PX}px;`
    + (fill === "none" ? "" : `background:#${fill};`)
    + (o.radius ? `border-radius:${o.radius * PX}px;` : "")
    + (o.line ? `border:${o.lw || 1}px solid #${o.line};box-sizing:border-box;` : "")
    + (o.shadow ? "box-shadow:0 3px 9px rgba(140,150,160,.30);" : "");
  hpush(`<div style="${st}"></div>`);
}
function image(path, x, y, w, h) {
  try { s.addImage({ path: "_img/" + path, x, y, w, h, sizing: { type: "contain", w, h } }); } catch (e) {}
  hpush(`<img src="../_img/${path}" style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:${w * PX}px;height:${h * PX}px;object-fit:contain">`);
}
// framed screenshot with optional caption
function shot(path, x, y, w, h, cap) {
  rect(x - 0.07, y - 0.07, w + 0.14, h + (cap ? 0.48 : 0.14), WHITE, { radius: 0.07, line: RULE, lw: 1, shadow: true });
  image(path, x, y, w, h);
  if (cap) text(cap, { x: x - 0.07, y: y + h + 0.03, w: w + 0.14, h: 0.34, align: "center", valign: "middle", fontSize: 12.5, bold: true, color: INK, fontFace: BF, margin: 0 });
}
function circle(x, y, d, fill, glyph, gc) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:${d * PX}px;height:${d * PX}px;border-radius:50%;background:#${fill}"></div>`);
  if (glyph) text(glyph, { x, y, w: d, h: d, align: "center", valign: "middle", fontSize: d * 34, bold: true, color: gc || WHITE, fontFace: TF, margin: 0 });
}
function arrow(x, y, w, c) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || ACCENT, width: 2.5, endArrowType: "triangle" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX - 1}px;width:${w * PX}px;height:0;border-top:2.5px solid #${c || ACCENT}"></div>`
    + `<div style="position:absolute;left:${(x + w) * PX - 5}px;top:${y * PX - 5}px;width:0;height:0;border-left:8px solid #${c || ACCENT};border-top:5px solid transparent;border-bottom:5px solid transparent"></div>`);
}
function kicker(t) { text(t.toUpperCase(), { x: M, y: 0.62, w: W - 2 * M, h: 0.3, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, spacing: 2.5, margin: 0 }); }
function title(t) { text(t, { x: M, y: 0.98, w: W - 2 * M, h: 1.0, fontSize: 28, bold: true, color: INK, fontFace: TF, margin: 0, lh: 1.05 }); }
function head(k, t) { kicker(k); title(t); }
function pageno() { PAGE++; text(String(PAGE).padStart(2, "0"), { x: W - 1.05, y: H - 0.5, w: 0.6, h: 0.3, fontSize: 10, color: MUTE, align: "right", fontFace: BF, margin: 0 }); }
function citeFooter(txt) {
  text("Nền:  " + txt, { x: M, y: 7.06, w: W - 2 * M - 0.55, h: 0.3,
    fontSize: 10, italic: true, color: "8A8A8A", fontFace: BF, valign: "middle", margin: 0 });
}

// ============================================================ 1 · TITLE (dark)
slide(NAVY);
text("LUẬN VĂN THẠC SĨ · KHOA HỌC MÁY TÍNH", { x: M, y: 1.5, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Tự động viết hướng dẫn sử dụng phần mềm\ntừ ảnh màn hình và câu hỏi của người dùng", { x: M - 0.02, y: 2.15, w: 9.6, h: 1.9, fontSize: 34, bold: true, color: WHITE, fontFace: TF, lh: 1.08, margin: 0 });
text("Kèm cách đánh giá khi trong tay không có bản hướng dẫn mẫu", { x: M, y: 4.25, w: 9.4, h: 0.6, fontSize: 18, italic: true, color: "C9D2DC", fontFace: TF, margin: 0 });
text("Học viên · · · · ·      Giảng viên hướng dẫn · · · · ·      2026", { x: M, y: 6.55, w: 11, h: 0.4, fontSize: 13, color: "8FA0B2", fontFace: BF, margin: 0 });
// motif: mot anh dien thoai ben phai (gon, khong chong lap)
shot("real_mv_1.png", 10.4, 2.0, 1.95, 3.2);
done();

// ============================================================ 2 · BÀI TOÁN
slide();
head("Bài toán", "Vào: một ảnh và một câu hỏi — Ra: hướng dẫn từng bước");
shot("real_mv_1.png", M + 0.3, 2.4, 2.05, 3.3, "Ảnh màn hình");
text("Câu hỏi", { x: 4.35, y: 2.5, w: 3.2, h: 0.32, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
rect(4.3, 2.85, 3.35, 1.2, FILL, { radius: 0.08 });
text("“Cần làm gì để đặt giờ 20:35\nrồi xác nhận?”", { x: 4.55, y: 2.95, w: 2.95, h: 1.0, fontSize: 15.5, color: INK, fontFace: BF, valign: "middle", margin: 0, lh: 1.2 });
arrow(7.9, 3.05, 0.55);
rect(8.65, 2.35, 3.85, 3.8, TINT, { radius: 0.1 });
text("Hướng dẫn sinh ra", { x: 8.95, y: 2.6, w: 3.3, h: 0.35, fontSize: 13, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("1.  Chọn giờ “8”, phút “35”\n\n2.  Chọn buổi “PM”\n\n3.  Nhấn “OK”", { x: 8.95, y: 3.15, w: 3.3, h: 2.8, fontSize: 17, color: INK, fontFace: BF, lh: 1.25, margin: 0 });
text("Nếu tác vụ trải nhiều màn, người dùng đưa vào nhiều ảnh — và các ảnh có thể bị xáo trộn.", { x: M, y: 6.5, w: 11.5, h: 0.4, fontSize: 13.5, color: BODY, fontFace: BF, margin: 0 });
pageno(); done();

// ============================================================ 3 · VÌ SAO KHÓ
slide();
head("Bài toán", "Ba điều làm bài toán này khó");
const ch = [
  ["Máy hay nhắc nút không có thật", "Mô hình mô tả một nút không hề xuất hiện trên màn hình, khiến người dùng làm theo không được. Đây gọi là ảo giác giao diện."],
  ["Không có bản hướng dẫn mẫu", "Không ai soạn sẵn hướng dẫn chuẩn cho mọi ứng dụng để làm mốc so sánh khi chấm điểm."],
  ["Các màn bị xáo trộn", "Với nhiều ảnh đưa vào lộn xộn, mô hình phải tự đoán ra màn nào trước, màn nào sau."],
];
ch.forEach((c, i) => {
  const x = M + i * 3.92;
  rect(x, 2.35, 3.62, 3.65, WHITE, { radius: 0.09, line: RULE, lw: 1, shadow: true });
  circle(x + 0.32, 2.7, 0.72, ACCENT, String(i + 1));
  text(c[0], { x: x + 0.32, y: 3.6, w: 3.05, h: 0.85, fontSize: 17, bold: true, color: INK, fontFace: TF, margin: 0, lh: 1.05 });
  text(c[1], { x: x + 0.32, y: 4.55, w: 3.05, h: 1.3, fontSize: 13, color: BODY, fontFace: BF, lh: 1.22, margin: 0 });
});
citeFooter("VLM suy luận trật tự thời gian yếu — TOMATO (ICLR 2025).");
pageno(); done();

// ============================================================ 3B · ĐÓNG GÓP (neu som, khung nghien cuu)
slide();
head("Đóng góp", "Hai kết quả nghiên cứu song song, và vì sao đây là nghiên cứu");
// A
rect(M, 2.3, 5.5, 3.45, FILL, { radius: 0.1 });
circle(M + 0.33, 2.62, 0.72, STEEL, "A");
text("Hệ thống viết hướng dẫn bám sát màn hình", { x: M + 1.3, y: 2.62, w: 3.95, h: 0.85, fontSize: 15.5, bold: true, color: INK, fontFace: TF, valign: "middle", margin: 0, lh: 1.05 });
text("Viết mù trước, rồi đối chiếu với danh sách nút thật; chỗ nào nhắc nút không có thì viết lại thành mô tả, không đoán nút khác.", { x: M + 0.38, y: 3.6, w: 4.85, h: 0.95, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.22, margin: 0 });
text([{ text: "Vì sao là nghiên cứu:  ", options: { bold: true, color: ACCENT } }, { text: "chúng tôi đo được rằng cách đoán nút gần nhất tạo ra lỗi âm thầm (nút có thật nhưng sai việc), nên chọn cách chỉ mô tả — một quyết định dựa trên bằng chứng.", options: { color: INK } }], { x: M + 0.38, y: 4.6, w: 4.85, h: 1.05, fontSize: 12, fontFace: BF, lh: 1.2, margin: 0 });
// B
rect(6.92, 2.3, 5.49, 3.45, TINT, { radius: 0.1 });
circle(7.25, 2.62, 0.72, ACCENT, "B");
text("Cách đánh giá không cần bản hướng dẫn mẫu", { x: 8.22, y: 2.62, w: 3.9, h: 0.85, fontSize: 15.5, bold: true, color: INK, fontFace: TF, valign: "middle", margin: 0, lh: 1.05 });
text("Chấm chất lượng khi không có đáp án mẫu do người soạn, và không để hệ tự chấm chính mình.", { x: 7.3, y: 3.6, w: 4.85, h: 0.95, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.22, margin: 0 });
text([{ text: "Vì sao là nghiên cứu:  ", options: { bold: true, color: ACCENT } }, { text: "đưa khung đánh giá cho văn bản do máy sinh mà không có đáp án mẫu (Chim, Ive & Liakata 2025) sang miền giao diện, rồi tự kiểm thước đo bằng lỗi cố ý — một hướng chưa ai làm.", options: { color: INK } }], { x: 7.3, y: 4.6, w: 4.85, h: 1.05, fontSize: 12, fontFace: BF, lh: 1.2, margin: 0 });
// bottom emphasis
rect(M, 5.95, W - 2 * M, 0.95, NAVY, { radius: 0.1 });
text([{ text: "Giá trị nghiên cứu nằm ở những gì đo được:  ", options: { bold: true, color: "E4A986" } }, { text: "mức bịa trên nhiều đời mô hình, bằng chứng cho thấy cách đoán nút gây hại, kết quả sắp thứ tự nhiều màn, và phân tích mô hình dựa vào đâu để đoán thứ tự — chứ không nằm ở độ phức tạp của thuật toán.", options: { color: "D6DBE2" } }], { x: M + 0.38, y: 5.95, w: W - 2 * M - 0.76, h: 0.95, fontSize: 12.5, fontFace: BF, valign: "middle", lh: 1.2, margin: 0 });
citeFooter("khung đánh giá không đáp án mẫu — Chim, Ive & Liakata (Computational Linguistics 2025).");
pageno(); done();

// ============================================================ 3C · Ý TƯỞNG CHÍNH (dua len truoc pipeline)
slide();
head("Ý tưởng chính", "Không có bản mẫu thì dựa vào chính màn hình để kiểm");
text("Không có đáp án mẫu để chấm, ta lấy chính danh sách nút thật của màn hình làm mốc.", { x: M, y: 2.05, w: 11.3, h: 0.4, fontSize: 16, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
// phep thay the (y tuong loi)
rect(M, 2.9, 4.5, 1.8, FILL, { radius: 0.1 });
text("Cách chấm thông thường", { x: M + 0.3, y: 3.08, w: 4.0, h: 0.3, fontSize: 12.5, bold: true, color: STEEL, fontFace: BF, margin: 0 });
text("Đáp án mẫu do người soạn", { x: M + 0.3, y: 3.52, w: 3.9, h: 0.4, fontSize: 15, bold: true, color: INK, fontFace: TF, margin: 0 });
text("✗  bài toán này không có", { x: M + 0.3, y: 4.05, w: 3.9, h: 0.4, fontSize: 13, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("thay bằng", { x: 5.48, y: 3.42, w: 1.2, h: 0.3, fontSize: 12, italic: true, color: STEEL, fontFace: BF, align: "center", margin: 0 });
arrow(5.5, 3.8, 1.05, ACCENT);
rect(6.75, 2.9, 5.66, 1.8, TINT, { radius: 0.1 });
text("Cách của luận văn", { x: 7.05, y: 3.08, w: 5.0, h: 0.3, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("Danh sách nút thật của màn hình", { x: 7.05, y: 3.52, w: 5.1, h: 0.4, fontSize: 15, bold: true, color: INK, fontFace: TF, margin: 0 });
text("✓  có sẵn trong ứng dụng (siêu dữ liệu trợ năng), không cần ai soạn", { x: 7.05, y: 4.05, w: 5.25, h: 0.55, fontSize: 12.5, color: GOOD, fontFace: BF, lh: 1.15, margin: 0 });
// cach dung
rect(M, 5.05, W - 2 * M, 1.1, WHITE, { radius: 0.1, line: RULE, lw: 1 });
text([{ text: "Cách dùng:  ", options: { bold: true, color: ACCENT } }, { text: "đối chiếu từng bước hướng dẫn với danh sách này; bước nào nhắc một nút không có trên màn thì viết lại thành mô tả, không đoán nút khác.", options: { color: BODY } }], { x: M + 0.3, y: 5.05, w: 11.0, h: 1.1, fontSize: 14, fontFace: BF, valign: "middle", lh: 1.3, margin: 0 });
text("Danh sách nút chỉ dùng lúc kiểm, không đưa cho mô hình lúc viết — để phép thử công bằng.", { x: M, y: 6.4, w: 11.3, h: 0.35, fontSize: 13, color: BODY, fontFace: BF, margin: 0 });
citeFooter("kiểm ảo giác không cần bản mẫu — FaithScore (Findings EMNLP 2024).");
pageno(); done();

// ============================================================ 3D · TOÀN CẢNH HỆ THỐNG (pipeline)
slide();
head("Toàn cảnh hệ thống", "Một hệ duy nhất — chọn nhánh theo số ảnh đưa vào");
// INPUT + router (spanning ca hai lan)
rect(M, 2.95, 2.15, 3.55, NAVY, { radius: 0.1 });
text("VÀO", { x: M, y: 3.12, w: 2.15, h: 0.3, fontSize: 12, bold: true, color: "E4A986", fontFace: BF, align: "center", spacing: 2, margin: 0 });
text("Một hoặc nhiều ảnh\n(có thể xáo trộn)\nkèm câu hỏi", { x: M + 0.12, y: 3.5, w: 1.9, h: 1.55, fontSize: 13, color: WHITE, fontFace: BF, align: "center", valign: "middle", lh: 1.3, margin: 0 });
text("chọn nhánh\ntheo số ảnh", { x: M + 0.1, y: 5.35, w: 1.95, h: 0.95, fontSize: 12, italic: true, color: "C9D2DC", fontFace: BF, align: "center", valign: "middle", lh: 1.2, margin: 0 });
arrow(3.12, 3.55, 0.5, STEEL);
arrow(3.12, 5.55, 0.5, STEEL);
// Lan 1: mot man
text("Chỉ một ảnh — một màn", { x: 3.75, y: 2.9, w: 4, h: 0.3, fontSize: 12.5, bold: true, color: STEEL, fontFace: BF, margin: 0 });
["Viết mù\n(ảnh + câu hỏi)", "Đối chiếu\nnút thật", "Viết lại\nchỗ bịa"].forEach((t, i) => {
  const x = 3.75 + i * 2.28;
  rect(x, 3.28, 1.95, 1.0, FILL, { radius: 0.09 });
  circle(x + 0.12, 3.36, 0.36, i === 1 ? ACCENT : STEEL, String(i + 1));
  text(t, { x: x + 0.02, y: 3.5, w: 1.9, h: 0.72, fontSize: 12, bold: true, color: INK, fontFace: BF, align: "center", valign: "middle", lh: 1.12, margin: 0 });
  if (i < 2) arrow(x + 1.97, 3.78, 0.26, ACCENT);
});
text("→  bản hướng dẫn", { x: 10.6, y: 3.5, w: 2.5, h: 0.56, fontSize: 12.5, bold: true, color: GOOD, fontFace: BF, valign: "middle", margin: 0 });
// Lan 2: nhieu man
text("Từ hai ảnh trở lên — nhiều màn", { x: 3.75, y: 4.95, w: 4.5, h: 0.3, fontSize: 12.5, bold: true, color: STEEL, fontFace: BF, margin: 0 });
rect(3.75, 5.32, 4.35, 1.0, TINT, { radius: 0.09 });
text([{ text: "Bước sắp thứ tự trước:  ", options: { bold: true, color: ACCENT } }, { text: "so từng cặp → đếm phiếu (Copeland) → gỡ vòng mâu thuẫn", options: { color: INK } }], { x: 3.92, y: 5.32, w: 4.05, h: 1.0, fontSize: 12, fontFace: BF, valign: "middle", lh: 1.18, margin: 0 });
arrow(8.15, 5.82, 0.28, ACCENT);
rect(8.5, 5.32, 4.4, 1.0, FILL, { radius: 0.09 });
text("Rồi chạy đúng nhánh một màn cho TỪNG màn đã sắp", { x: 8.66, y: 5.32, w: 4.1, h: 1.0, fontSize: 12.5, bold: true, color: INK, fontFace: BF, valign: "middle", lh: 1.18, margin: 0 });
text([{ text: "Nhánh nhiều màn chính là nhánh một màn, chỉ thêm một bước sắp thứ tự ở đầu.  ", options: { bold: true, color: INK } }, { text: "Khi chỉ có một ảnh, bỏ qua bước sắp và quay về đúng nhánh một màn.", options: { color: BODY } }], { x: M, y: 6.6, w: 11.5, h: 0.35, fontSize: 13, fontFace: BF, margin: 0 });
citeFooter("so cặp — Qin (NAACL 2024) · gộp phiếu Copeland (Saari & Merlin 1996) trong khung rank-aggregation của Dwork et al. (WWW 2001) · gỡ vòng min-FAS — Ailon et al. (JACM 2008).");
pageno(); done();

// ============================================================ 5 · DỮ LIỆU (3 bo, hinh)
slide();
head("Dữ liệu", "Ba bộ dữ liệu, mỗi bộ một vai trò");
const ds = [
  ["real_mv_2.png", "MobileViews", "Một màn kèm danh sách nút thật. Dùng để đo mức bám sát giao diện.", 0.61],
  ["ac_o2.png", "AndroidControl", "Chuỗi nhiều màn kèm thao tác đúng từng bước. Dùng để đo sắp thứ tự và hoàn thành tác vụ.", 0.45],
  ["ss_mobile.png", "ScreenSpot", "Ảnh kèm toạ độ nút chuẩn. Làm bộ đối chứng cho khả năng chỉ đúng nút.", 0.46],
];
ds.forEach((d, i) => {
  const x = M + i * 3.92;
  rect(x, 2.35, 3.62, 3.95, WHITE, { radius: 0.09, line: RULE, lw: 1, shadow: true });
  const iw = 2.35 * d[3], ih = 2.35;
  shot(d[0], x + (3.62 - iw) / 2, 2.55, iw, ih);
  text(d[1], { x: x + 0.3, y: 5.02, w: 3.0, h: 0.35, fontSize: 16, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
  text(d[2], { x: x + 0.3, y: 5.4, w: 3.05, h: 0.85, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.2, margin: 0 });
});
text("Điểm chung: cả ba đều có danh sách nút thật để làm mốc, nên không cần một bản hướng dẫn mẫu do người soạn.", { x: M, y: 6.55, w: 11.5, h: 0.4, fontSize: 13, color: BODY, fontFace: BF, margin: 0 });
pageno(); done();

// ============================================================ 6 · CÁCH LÀM MỘT MÀN
slide();
head("Cách làm · một màn", "Viết trước, rồi đối chiếu với danh sách nút thật");
// buoc 1
rect(M, 2.3, W - 2 * M, 1.35, FILL, { radius: 0.09 });
circle(M + 0.3, 2.62, 0.7, STEEL, "1");
text("Mô hình viết hướng dẫn khi chỉ thấy ảnh và câu hỏi", { x: M + 1.25, y: 2.55, w: 6.2, h: 0.85, fontSize: 16, bold: true, color: INK, fontFace: TF, valign: "middle", margin: 0, lh: 1.1 });
arrow(8.0, 2.98, 0.5);
rect(8.6, 2.62, 3.55, 0.75, TINT, { radius: 0.37 });
text("bản nháp đầu tiên", { x: 8.6, y: 2.62, w: 3.55, h: 0.75, fontSize: 14.5, bold: true, color: INK, fontFace: BF, align: "center", valign: "middle", margin: 0 });
// buoc 2
rect(M, 3.85, W - 2 * M, 2.35, WHITE, { radius: 0.09, line: RULE, lw: 1 });
circle(M + 0.3, 4.15, 0.7, ACCENT, "2");
text("Thuật toán đối chiếu từng bước với danh sách nút thật", { x: M + 1.25, y: 4.12, w: 9.5, h: 0.55, fontSize: 16, bold: true, color: INK, fontFace: TF, valign: "middle", margin: 0 });
text("Bước nhắc một nút có thật", { x: M + 1.25, y: 4.9, w: 4.7, h: 0.4, fontSize: 14, bold: true, color: GOOD, fontFace: BF, margin: 0 });
text("thì giữ nguyên bước đó.", { x: M + 5.9, y: 4.9, w: 5.3, h: 0.4, fontSize: 14, color: BODY, fontFace: BF, margin: 0 });
text("Bước nhắc một nút không có thật", { x: M + 1.25, y: 5.42, w: 4.7, h: 0.4, fontSize: 14, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("thì đổi thành mô tả chung, không đoán nút khác.", { x: M + 5.9, y: 5.42, w: 5.8, h: 0.4, fontSize: 14, color: BODY, fontFace: BF, margin: 0 });
text("Bước đối chiếu là thuật toán so khớp ý nghĩa, không phải thêm một mô hình đoán chồng lên nữa.", { x: M, y: 6.5, w: 11.5, h: 0.4, fontSize: 13.5, color: BODY, fontFace: BF, margin: 0 });
citeFooter("đối chiếu-sau với nguồn ngoài theo lối FActScore (FActScore chỉ chấm, EMNLP 2023) · khớp tên nút theo ngữ nghĩa như ALOHa (NAACL 2024).");
pageno(); done();

// ============================================================ 7 · VÍ DỤ THẬT MỘT MÀN
slide();
head("Cách làm · một màn · ví dụ", "Bắt lỗi khi máy nhắc một nút không có trên màn");
shot("real_mv_1.png", M + 0.1, 2.55, 2.15, 3.52, "Màn đặt giờ");
const er = [
  [{ text: "Máy viết ra", options: { bold: true, fill: FILL, color: INK } }, { text: "Trên màn có nút này?", options: { bold: true, fill: FILL, color: INK } }, { text: "Kết luận", options: { bold: true, fill: FILL, color: INK, align: "center" } }],
  [{ text: "Chọn giờ và phút" }, { text: "Có (giờ, phút)" }, { text: "hợp lệ", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Chọn “PM”" }, { text: "Có (PM)" }, { text: "hợp lệ", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Mở “Cài đặt”" }, { text: "Không có", options: { color: MUTE } }, { text: "nhắc nút không có thật", options: { align: "center", color: ACCENT, bold: true } }],
];
s.addTable(er, { x: 3.55, y: 2.55, w: 8.7, colW: [3.0, 3.15, 2.55], rowH: 0.62, fontFace: BF, fontSize: 14, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
// html mirror of the table (approx)
hpush(tableHTML(er, 3.55, 2.55, [3.0, 3.15, 2.55], 0.62));
rect(3.55, 5.02, 8.7, 1.02, TINT, { radius: 0.09 });
text([{ text: "Lớp kiểm làm gì:  ", options: { bold: true, color: ACCENT } }, { text: "hạ bước sai “Mở Cài đặt” xuống mô tả bằng lời, các bước đúng giữ nguyên. Nó chặn việc chỉ vào nút không có thật — nhưng CHƯA bảo đảm bước đó là thao tác đúng (ở đây đúng ra là “Nhấn OK”); mức làm đúng thao tác được đo riêng bằng Step-SR, nơi có đáp án mẫu (nhánh nhiều màn).", options: { color: INK } }], { x: 3.8, y: 5.02, w: 8.25, h: 1.02, fontSize: 12.5, fontFace: BF, valign: "middle", lh: 1.22, margin: 0 });
rect(3.55, 6.15, 8.7, 0.78, NAVY, { radius: 0.09 });
text([{ text: "Vì sao KHÔNG đoán nút gần nhất?  ", options: { bold: true, color: "E4A986" } }, { text: "thay nút bịa bằng một nút thật nhưng sai việc (kiểu Submit→Save) sẽ khiến người dùng bấm nhầm mà không hay — lỗi âm thầm.", options: { color: "D6DBE2" } }], { x: 3.8, y: 6.15, w: 8.2, h: 0.78, fontSize: 12, fontFace: BF, valign: "middle", lh: 1.18, margin: 0 });
pageno(); done();

// ============================================================ 8 · NHIỀU MÀN — SẮP THỨ TỰ
slide();
head("Cách làm · nhiều màn", "Sắp lại đúng thứ tự bằng cách so từng cặp");
text("Nhiều ảnh đưa vào bị xáo trộn. Trước khi viết hướng dẫn, hệ phải sắp lại đúng thứ tự các màn — làm theo bốn bước:", { x: M, y: 2.2, w: 11.3, h: 0.6, fontSize: 15.5, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
[["ac_o1.png", "Màn A"], ["ac_o2.png", "Màn B"], ["ac_o3.png", "Màn C"]].forEach((im, i) => {
  const x = M + 0.15 + i * 1.95;
  shot(im[0], x, 2.95, 1.55, 2.5, im[1]);
  if (i < 2) arrow(x + 1.62, 4.2, 0.28, STEEL);
});
rect(7.0, 2.95, 5.4, 3.15, FILL, { radius: 0.1 });
text([
  { text: "①  Hỏi từng cặp:  ", options: { bold: true, color: ACCENT } }, { text: "“màn nào đến trước?”\n\n", options: { color: INK } },
  { text: "②  Đếm phiếu, ", options: { bold: true, color: ACCENT } }, { text: "màn thắng nhiều cặp xếp trước:\n     A thắng 2, B thắng 1, C thắng 0\n     nên thứ tự là  A, B, C\n\n", options: { color: INK } },
  { text: "③  Gỡ vòng ", options: { bold: true, color: ACCENT } }, { text: "nếu các phán đoán mâu thuẫn nhau\n\n", options: { color: INK } },
  { text: "④  Có thứ tự rồi, ", options: { bold: true, color: ACCENT } }, { text: "viết hướng dẫn cho từng màn (chạy đúng nhánh một màn)", options: { color: INK } },
], { x: 7.3, y: 3.15, w: 4.85, h: 2.85, fontSize: 13, fontFace: BF, lh: 1.28, margin: 0 });
text("Ở bước ③, khi các phán đoán cắn đuôi nhau (A trước B, B trước C, nhưng C lại trước A), hệ bỏ đi ít phán đoán nhất để hết vòng — chọn phán đoán kém ổn định nhất khi hỏi lại, không dựa vào độ tự tin của mô hình.", { x: M, y: 6.35, w: 11.5, h: 0.5, fontSize: 12, color: BODY, fontFace: BF, lh: 1.2, margin: 0 });
citeFooter("so cặp — Qin (NAACL 2024) · gộp phiếu Copeland (Saari & Merlin 1996) trong khung rank-aggregation của Dwork et al. (WWW 2001) · gỡ vòng min-FAS — Ailon et al. (JACM 2008).");
pageno(); done();

// ============================================================ 8B · CÓ GÌ MỚI (novelty vs prior-art)
slide();
head("Có gì mới", "Công cụ thì có sẵn — cái mới là cách ghép và những gì tìm ra");
// trai: cong cu da co
rect(M, 2.4, 4.85, 4.25, FILL, { radius: 0.1 });
text("Thừa nhận: các công cụ đã có sẵn", { x: M + 0.32, y: 2.6, w: 4.3, h: 0.35, fontSize: 14, bold: true, color: STEEL, fontFace: TF, margin: 0 });
text("·  So cặp để xếp hạng — Qin 2024\n·  Gộp phiếu Copeland — Saari–Merlin 1996 (khung Dwork 2001)\n·  Gỡ vòng min-FAS — Ailon 2008\n·  Khớp tên nút theo nghĩa — ALOHa 2024\n·  Kiểm không cần mẫu — FaithScore 2024", { x: M + 0.32, y: 3.15, w: 4.35, h: 3.3, fontSize: 13, color: BODY, fontFace: BF, lh: 1.65, margin: 0 });
// phai: cai moi
rect(6.05, 2.4, 6.36, 4.25, TINT, { radius: 0.1 });
text("Mới ở luận văn này", { x: 6.37, y: 2.6, w: 5.8, h: 0.35, fontSize: 14, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text([
  { text: "①  Ghép việc chưa ai làm cùng lúc:  ", options: { bold: true, color: INK } },
  { text: "viết hướng dẫn cho người từ ảnh giao diện, rồi đánh giá mà không cần đáp án mẫu, lấy danh sách nút thật làm mốc.\n", options: { color: BODY } },
  { text: "②  Những điều đo được:  ", options: { bold: true, color: INK } },
  { text: "tỉ lệ nhắc sai thay đổi ra sao theo từng đời mô hình; và bằng chứng rằng cách đoán nút tạo lỗi âm thầm.\n", options: { color: BODY } },
  { text: "③  Mô hình dựa vào đâu để đoán thứ tự:  ", options: { bold: true, color: INK } },
  { text: "tách riêng năm loại tín hiệu để xem mô hình dựa vào từng loại nhiều hay ít.\n", options: { color: BODY } },
  { text: "④  Cách chấm thứ tự công bằng:  ", options: { bold: true, color: INK } },
  { text: "chỉ trừ điểm ở những cặp buộc phải đúng thứ tự, không trừ ở cặp làm trước sau đều được.", options: { color: BODY } },
], { x: 6.37, y: 3.15, w: 5.75, h: 3.3, fontSize: 12.5, fontFace: BF, lh: 1.3, margin: 0 });
// bottom
text([{ text: "Cái mới không nằm ở thuật toán lõi, ", options: { bold: true, color: INK } }, { text: "mà ở cách ghép miền giao diện, mục tiêu tác vụ và cách đo lại với nhau — nên không thể quy về “chỉ áp dụng đồ có sẵn”.", options: { color: BODY } }], { x: M, y: 6.78, w: 11.5, h: 0.35, fontSize: 13, fontFace: BF, margin: 0 });
citeFooter("không bị trùng — chưa ai ghép “viết hướng dẫn cho người và đánh giá không cần đáp án mẫu trên giao diện” (rà 2025–2026).");
pageno(); done();

// ============================================================ 9 · ĐO LƯỜNG
slide();
head("Đánh giá", "Các thước đo — công thức và ví dụ");
// helper: mot muc thuoc do (ten + nhan + cong thuc + vi du)
function metric(x, y, w, name, tag, formula, ex) {
  text([{ text: name + "   ", options: { bold: true, color: INK } }, { text: tag, options: { bold: true, color: ACCENT } }], { x, y, w, h: 0.3, fontSize: 13.5, fontFace: BF, margin: 0 });
  text(formula, { x, y: y + 0.32, w, h: 0.3, fontSize: 12.5, color: INK, fontFace: BF, lh: 1.1, margin: 0 });
  text([{ text: "Ví dụ:  ", options: { bold: true, color: STEEL } }, { text: ex, options: { color: STEEL } }], { x, y: y + 0.64, w, h: 0.3, fontSize: 11.5, fontFace: BF, lh: 1.1, margin: 0 });
}
// mot man
rect(M, 2.2, 5.7, 4.15, WHITE, { radius: 0.09, line: RULE, lw: 1, shadow: true });
text("Một màn", { x: M + 0.35, y: 2.38, w: 3.0, h: 0.4, fontSize: 17, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("không có đáp án mẫu", { x: M + 2.2, y: 2.43, w: 3.15, h: 0.3, fontSize: 12.5, color: MUTE, fontFace: BF, align: "right", margin: 0 });
metric(M + 0.35, 2.95, 5.05, "Độ trung thực", "thước chính", "= 1 − (số bước bịa) / (số bước nhắc nút)", "3 bước nhắc nút, 1 sai → 2/3 ≈ 67%");
metric(M + 0.35, 4.0, 5.05, "Độ đúng nhãn", "bổ trợ", "= (bước gọi đúng tên) / (bước trỏ nút thật)", "nút hiện “OK”, viết “Đồng ý” → sai nhãn");
text([{ text: "Lưu ý.  ", options: { bold: true, color: INK } }, { text: "Con số công bố là tỉ lệ nhắc sai của bản nháp gốc, không phải gần 100% sau khi sửa.", options: { color: BODY } }], { x: M + 0.35, y: 5.12, w: 5.05, h: 1.05, fontSize: 12, fontFace: BF, lh: 1.22, margin: 0 });
// nhieu man
rect(6.92, 2.2, 5.49, 4.15, TINT, { radius: 0.09 });
text("Nhiều màn", { x: 7.27, y: 2.38, w: 3.0, h: 0.4, fontSize: 17, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("có đáp án mẫu", { x: 7.27 + 2.0, y: 2.43, w: 2.95, h: 0.3, fontSize: 12.5, color: MUTE, fontFace: BF, align: "right", margin: 0 });
metric(7.27, 2.95, 4.85, "Sắp đúng thứ tự các màn", "τ", "= (cặp thuận − cặp nghịch) / (cặp bắt buộc)", "đáp án A→B→C, hệ xếp A→C→B, được +0,33");
metric(7.27, 4.0, 4.85, "Làm đúng từng bước", "Step-SR", "= (bước làm đúng) / (bước trong đáp án mẫu)", "làm đúng 4/5 bước → 80%");
text([{ text: "episode = một tác vụ trải nhiều màn.  ", options: { bold: true, color: INK } }, { text: "Ngoài hai thước trên còn một chỉ số phụ (PMR — tỉ lệ episode sắp đúng trọn), chưa có số thật; xem bài nói §4.2.", options: { color: BODY } }], { x: 7.27, y: 5.15, w: 4.85, h: 1.05, fontSize: 12, fontFace: BF, lh: 1.25, margin: 0 });
text([{ text: "Riêng việc bấm trúng nút ", options: { color: BODY } }, { text: "được kiểm bằng bộ đối chứng — xem slide sau.", options: { bold: true, color: INK } }], { x: M, y: 6.55, w: 11.5, h: 0.35, fontSize: 13, fontFace: BF, margin: 0 });
citeFooter("khung đánh giá nội tại và ngoại lai — Chim, Ive & Liakata (Computational Linguistics 2025) · điểm từng bước và ngưỡng 14% — AndroidControl (NeurIPS 2024), AITW (NeurIPS 2023).");
pageno(); done();

// ============================================================ 9B · VÍ DỤ TÍNH ĐIỂM BẰNG SỐ
slide();
head("Đánh giá · ví dụ", "Tính thử hai điểm bằng số cụ thể");
// trai: do trung thuc (mot man)
rect(M, 2.35, 5.5, 4.2, WHITE, { radius: 0.09, line: RULE, lw: 1, shadow: true });
text("Độ trung thực — một màn", { x: M + 0.35, y: 2.55, w: 5.0, h: 0.35, fontSize: 16, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text([
  { text: "Hướng dẫn có 3 bước nhắc nút:\n", options: { color: BODY } },
  { text: "  1.  Chọn giờ và phút     ", options: { color: INK } }, { text: "✓ có thật\n", options: { color: GOOD, bold: true } },
  { text: "  2.  Chọn “PM”                ", options: { color: INK } }, { text: "✓ có thật\n", options: { color: GOOD, bold: true } },
  { text: "  3.  Mở “Cài đặt”            ", options: { color: INK } }, { text: "✗ không có (bịa)", options: { color: ACCENT, bold: true } },
], { x: M + 0.35, y: 3.05, w: 5.0, h: 1.75, fontSize: 13.5, fontFace: BF, lh: 1.35, margin: 0 });
rect(M + 0.35, 4.95, 5.0, 1.35, FILL, { radius: 0.09 });
text([{ text: "Độ trung thực = 1 − (bước bịa)/(bước nhắc nút)\n", options: { color: INK } }, { text: "= 1 − 1/3 = 0,67", options: { bold: true, color: ACCENT } }], { x: M + 0.55, y: 4.95, w: 4.7, h: 1.35, fontSize: 14.5, fontFace: BF, valign: "middle", lh: 1.4, margin: 0 });
// phai: tau (nhieu man)
rect(6.72, 2.35, 5.69, 4.2, TINT, { radius: 0.09 });
text("Sắp đúng thứ tự — nhiều màn", { x: 7.05, y: 2.55, w: 5.2, h: 0.35, fontSize: 16, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text([
  { text: "Thứ tự đúng (đáp án mẫu):  ", options: { color: BODY } }, { text: "A → B → C\n", options: { bold: true, color: INK } },
  { text: "Hệ sắp ra:  ", options: { color: BODY } }, { text: "A → C → B\n\n", options: { bold: true, color: INK } },
  { text: "Kiểm ba cặp buộc phải đúng thứ tự:\n", options: { bold: true, color: STEEL } },
  { text: "•  A trước B ?  hệ để A trước B  →  ", options: { color: INK } }, { text: "đúng\n", options: { bold: true, color: GOOD } },
  { text: "•  A trước C ?  hệ để A trước C  →  ", options: { color: INK } }, { text: "đúng\n", options: { bold: true, color: GOOD } },
  { text: "•  B trước C ?  hệ để C trước B  →  ", options: { color: INK } }, { text: "sai", options: { bold: true, color: ACCENT } },
], { x: 7.05, y: 3.0, w: 5.15, h: 1.95, fontSize: 12.5, fontFace: BF, lh: 1.32, margin: 0 });
rect(7.05, 5.0, 5.15, 1.3, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "2 cặp đúng, 1 cặp sai:   ", options: { color: INK } }, { text: "điểm = (2 − 1) / 3 ≈ +0,33\n", options: { bold: true, color: ACCENT } }, { text: "(−1 nếu sai hết thứ tự, +1 nếu đúng hết)", options: { color: MUTE } }], { x: 7.25, y: 5.0, w: 4.75, h: 1.3, fontSize: 13, fontFace: BF, valign: "middle", lh: 1.4, margin: 0 });
text([{ text: "Lưu ý.  ", options: { bold: true, color: INK } }, { text: "Con số công bố cho một màn là tỉ lệ nhắc sai của bản nháp GỐC, không phải trị số gần 100% sau khi đã sửa.", options: { color: BODY } }], { x: M, y: 6.7, w: 11.5, h: 0.35, fontSize: 13, fontFace: BF, margin: 0 });
pageno(); done();

// ============================================================ 10 · CHỈ ĐÚNG NÚT (grounding, hinh)
slide();
head("Đánh giá · đối chứng", "Bấm có trúng đúng nút không — đối chứng ScreenSpot");
[["real_ground_1.png", "“lật ống kính”"], ["real_ground_2.png", "“bắt đầu hẹn giờ”"], ["real_ground_3.png", "“thêm sự kiện lịch”"]].forEach((im, i) => {
  const x = 3.98 + i * 2.05;
  shot(im[0], x, 2.2, 1.1, 2.35, im[1]);
});
// cach lam
rect(M, 5.1, 5.7, 1.4, FILL, { radius: 0.09 });
text("Cách làm", { x: M + 0.3, y: 5.22, w: 5.1, h: 0.3, fontSize: 13.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Một mô hình grounding có sẵn — không thuộc hệ sinh hướng dẫn — nhận tên nút và ảnh rồi tự đoán toạ độ điểm bấm. Không lấy sẵn tâm nút (lấy tâm thì luôn trúng, vô nghĩa). Khung đỏ trên ảnh là nút đúng.", { x: M + 0.3, y: 5.55, w: 5.15, h: 0.9, fontSize: 12, color: BODY, fontFace: BF, lh: 1.18, margin: 0 });
// thuoc do
rect(6.92, 5.1, 5.49, 1.4, TINT, { radius: 0.09 });
text("Thước đo — Tỉ lệ trúng", { x: 7.22, y: 5.22, w: 5.0, h: 0.3, fontSize: 13.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text([{ text: "= (số nút trúng) / (tổng số nút). ", options: { bold: true, color: INK } }, { text: "Một nút trúng nếu điểm rơi trong khung: trái ≤ x ≤ phải, trên ≤ y ≤ dưới. Báo riêng nút chữ / biểu tượng. Dữ liệu: ScreenSpot, 501 nút.", options: { color: BODY } }], { x: 7.22, y: 5.55, w: 4.95, h: 0.9, fontSize: 12, fontFace: BF, lh: 1.18, margin: 0 });
text([{ text: "Ví dụ:  ", options: { bold: true, color: STEEL } }, { text: "nút “lật ống kính” có khung (965, 2105)–(1110, 2258); bộ trỏ đoán (1030, 2180) → nằm trong khung → trúng.", options: { color: STEEL } }], { x: M, y: 6.62, w: 11.5, h: 0.32, fontSize: 12, fontFace: BF, margin: 0 });
citeFooter("point-in-bbox — SeeClick (ACL 2024) · bộ đối chứng ScreenSpot-v2 — OS-Atlas (ICLR 2025).");
pageno(); done();

// ============================================================ 11 · TIN ĐƯỢC KHÔNG (validity)
slide();
head("Đóng góp B · phương pháp đánh giá", "Cách chấm không cần đáp án mẫu, dùng lại được");
text([{ text: "Đây là đóng góp B, đứng độc lập với hệ thống:  ", options: { bold: true, color: ACCENT } }, { text: "một phương pháp đánh giá không cần bản mẫu người soạn và không tự chấm — ba lớp bảo đảm dưới đây làm nó đáng tin.", options: { color: BODY } }], { x: M, y: 1.98, w: 11.5, h: 0.35, fontSize: 13.5, fontFace: BF, margin: 0 });
const va = [
  ["Không tự chấm mình", "Công cụ quyết định một bước đúng hay sai và công cụ chấm điểm là hai công cụ khác nhau, và đều không phải mô hình đã viết ra hướng dẫn."],
  ["Thử bằng lỗi cố ý", "Cố tình chèn lỗi đã biết vào một hướng dẫn đúng, xem thước đo có phát hiện. Thêm nút giả thì điểm phải tụt; đổi tên đồng nghĩa thì điểm giữ nguyên."],
  ["Thống kê cẩn thận", "Gộp theo ứng dụng vì các màn cùng ứng dụng không độc lập; báo khoảng tin cậy; chốt ngưỡng trước khi nhìn kết quả."],
];
va.forEach((v, i) => {
  const y = 2.4 + i * 1.35;
  rect(M, y, W - 2 * M, 1.15, WHITE, { radius: 0.08, line: RULE, lw: 1 });
  circle(M + 0.3, y + 0.28, 0.6, ACCENT, String(i + 1));
  text(v[0], { x: M + 1.15, y: y, w: 3.3, h: 1.15, fontSize: 16, bold: true, color: INK, fontFace: TF, valign: "middle", margin: 0, lh: 1.05 });
  text(v[1], { x: M + 4.5, y: y, w: 6.8, h: 1.15, fontSize: 13.5, color: BODY, fontFace: BF, valign: "middle", lh: 1.22, margin: 0 });
});
citeFooter("dùng bộ chấm khác dòng với mô hình sinh — Panickssery (NeurIPS 2024) · gộp theo ứng dụng — MacKinnon, Nielsen & Webb (J. Econometrics 2023).");
pageno(); done();

// ============================================================ 11C · THỬ THƯỚC ĐO BẰNG LỖI CỐ Ý
slide();
head("Đóng góp B · tự kiểm thước đo", "Thử độ tin của thước đo bằng lỗi cố ý");
text([{ text: "Giống thử máy báo khói bằng cách tạo khói: ", options: { color: BODY } }, { text: "một chương trình tự động", options: { bold: true, color: INK } }, { text: " chèn một lỗi đã biết vào hướng dẫn đúng (không phải người, không phải AI sinh; tách khỏi bộ khớp tên nút). Vì chính mình tạo lỗi nên biết sẵn đáp án — chỉ cần xem thước đo có phản ứng đúng hướng không.", options: { color: BODY } }], { x: M, y: 2.15, w: 11.4, h: 0.9, fontSize: 14, fontFace: BF, lh: 1.25, margin: 0 });
const pr = [
  [{ text: "Lỗi cố ý chèn vào", options: { bold: true, fill: FILL, color: INK } }, { text: "Thước đo phải phản ứng thế nào", options: { bold: true, fill: FILL, color: INK } }],
  [{ text: "Thêm một nút không có trên màn" }, { text: "Độ trung thực phải tụt", options: { bold: true, color: ACCENT } }],
  [{ text: "Đổi tên nút thành một từ đồng nghĩa" }, { text: "Độ trung thực giữ nguyên, nhưng độ đúng nhãn tụt", options: { bold: true, color: ACCENT } }],
  [{ text: "Đảo thứ tự vài bước bắt buộc" }, { text: "Điểm đúng thứ tự (τ) phải tụt", options: { bold: true, color: ACCENT } }],
];
s.addTable(pr, { x: M, y: 3.2, w: W - 2 * M, colW: [5.35, 6.14], rowH: 0.7, fontFace: BF, fontSize: 14, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
hpush(tableHTML(pr, M, 3.2, [5.35, 6.14], 0.7));
rect(M, 6.02, W - 2 * M, 0.82, TINT, { radius: 0.09 });
text([{ text: "Chấm chính thước đo bằng ba con số:  ", options: { bold: true, color: INK } }, { text: "tỉ lệ bắt được lỗi, tỉ lệ báo nhầm (giữ dưới 5%), và mức độ nhất quán (lỗi càng nặng thì điểm càng giảm). Thước nào không đạt thì bị loại, thay cho việc nhờ người chấm.", options: { color: BODY } }], { x: M + 0.3, y: 6.02, w: 11.0, h: 0.82, fontSize: 12.5, fontFace: BF, valign: "middle", lh: 1.2, margin: 0 });
citeFooter("validate bằng nhiễu loạn — Sai et al. (EMNLP 2021) · không lấy chấm-người làm cổng — Clark et al. (ACL-IJCNLP 2021).");
pageno(); done();

// ============================================================ 11B · BỘ THÍ NGHIỆM (7 cau hoi nghien cuu)
slide();
head("Bộ thí nghiệm", "Bảy câu hỏi nghiên cứu và mức cần đạt, chốt trước khi chạy");
const ex = [
  [{ text: "Câu hỏi nghiên cứu", options: { bold: true, fill: FILL, color: INK } }, { text: "TN", options: { bold: true, fill: FILL, color: INK, align: "center" } }, { text: "Mức cần đạt (chốt trước khi xem kết quả)", options: { bold: true, fill: FILL, color: INK } }],
  [{ text: "Mức nhắc sai thay đổi ra sao theo đời mô hình" }, { text: "E1", options: { align: "center", color: STEEL, bold: true } }, { text: "mô hình mới vẫn nhắc sai từ 5% trở lên" }],
  [{ text: "Lớp đối chiếu giúp bao nhiêu, giá bao nhiêu" }, { text: "E2", options: { align: "center", color: STEEL, bold: true } }, { text: "độ trung thực tăng, khoảng 19% bước phải mô tả, chỉ số khác không xấu đi" }],
  [{ text: "Vì sao chỉ mô tả, không đoán nút" }, { text: "E3", options: { align: "center", color: STEEL, bold: true } }, { text: "cách đoán nút thật sự tạo ra lỗi âm thầm" }],
  [{ text: "Cách đánh giá có đáng tin không" }, { text: "E4–7", options: { align: "center", color: ACCENT, bold: true } }, { text: "báo nhầm dưới 5%, lỗi nặng hơn thì điểm thấp hơn, và khớp với người chấm" }],
  [{ text: "Sắp thứ tự nhiều màn có đúng không" }, { text: "E8–13", options: { align: "center", color: ACCENT, bold: true } }, { text: "tốt hơn xếp ngẫu nhiên, ngang cách sắp một lần, mỗi bước đều có ích" }],
  [{ text: "Làm đúng từng bước tới đâu" }, { text: "E14", options: { align: "center", color: ACCENT, bold: true } }, { text: "điểm làm đúng từng bước thật sự dương" }],
  [{ text: "Bấm có trúng nút không" }, { text: "E15", options: { align: "center", color: ACCENT, bold: true } }, { text: "bộ trỏ độc lập bấm trúng khung nút" }],
  [{ text: "Người đọc có làm theo được không" }, { text: "E16", options: { align: "center", color: ACCENT, bold: true } }, { text: "bản có mô tả thay thế vẫn dễ làm theo" }],
];
s.addTable(ex, { x: M, y: 2.15, w: W - 2 * M, colW: [4.75, 0.95, 5.79], rowH: 0.5, fontFace: BF, fontSize: 12, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
hpush(tableHTML(ex, M, 2.15, [4.75, 0.95, 5.79], 0.5));
text([{ text: "Chi tiết bảy thí nghiệm cốt lõi (E1–E16), thứ tự chạy và các cổng kiểm:  ", options: { bold: true, color: INK } }, { text: "bài nói §6 — làm bước miễn phí (kiểm nội bộ) trước, gọi mô hình sau.", options: { color: BODY } }], { x: M, y: 6.72, w: 11.5, h: 0.32, fontSize: 12, fontFace: BF, margin: 0 });
citeFooter("chốt mức đánh giá trước khi chạy, không chỉnh sau khi thấy số · gộp theo ứng dụng — MacKinnon, Nielsen & Webb (J. Econometrics 2023).");
pageno(); done();

// ============================================================ 12 · KẾT QUẢ BƯỚC ĐẦU
slide();
head("Kết quả bước đầu", "Số liệu ban đầu, kèm phạm vi rõ ràng");
// hai o so lieu that (khong bia)
function stat(x, y, num, nc, lab) {
  rect(x, y, 5.5, 1.75, FILL, { radius: 0.1 });
  text(num, { x: x + 0.3, y: y, w: 1.95, h: 1.75, fontSize: 44, bold: true, color: nc, fontFace: TF, align: "center", valign: "middle", margin: 0 });
  text(lab, { x: x + 2.35, y: y, w: 2.95, h: 1.75, fontSize: 14, color: BODY, fontFace: BF, valign: "middle", lh: 1.25, margin: 0 });
}
stat(M, 2.4, "≈ 25%", ACCENT, "số bước có nhắc nút bị nhắc sai, ở bản nháp gốc");
stat(M, 4.35, "≈ 19%", STEEL, "số bước phải chuyển sang mô tả chung — cái giá phải trả");
rect(6.72, 2.4, 5.69, 3.7, TINT, { radius: 0.1 });
text("Quan sát bước đầu", { x: 7.02, y: 2.6, w: 5.1, h: 0.35, fontSize: 15, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("•  Lớp đối chiếu nâng mức bám sát giao diện ở mọi ngưỡng.\n\n•  Cách gọi tên nút và định dạng hầu như không đổi — không gây hại cho các bước vốn đã đúng.\n\n•  Chạy thử mới trên một mô hình, nhánh một màn.", { x: 7.02, y: 3.1, w: 5.1, h: 2.9, fontSize: 14, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });
rect(M, 6.25, W - 2 * M, 0.85, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "Phạm vi: ", options: { bold: true, color: INK } }, { text: "mẫu nhỏ, một mô hình, khoảng tin cậy còn chạm 0. Bản đầy đủ (127 màn của 30 ứng dụng) và nhánh nhiều màn đang chạy.", options: { color: BODY } }], { x: M + 0.3, y: 6.25, w: 11.0, h: 0.85, fontSize: 13, fontFace: BF, valign: "middle", lh: 1.2, margin: 0 });
pageno(); done();

// ============================================================ 13 · GIỚI HẠN
slide();
head("Nói thẳng giới hạn", "Những chỗ chưa làm được");
const li = [
  "Nhánh một màn mới đo mức bám sát giao diện, chưa đo mức đúng ý người dùng; phần đó để nhánh nhiều màn đo qua mức hoàn thành tác vụ.",
  "Danh sách nút thật đôi khi thiếu hoặc nhãn chung chung (kiểu “Button”); các nút như vậy được loại khỏi phép tính để không phạt oan.",
  "Nếu chỉ có ảnh trơn thì cần thêm một bộ dò nút và phải chịu sai số; trên máy thật, hệ điều hành cung cấp sẵn danh sách nút.",
  "Chưa có bảng số tiếng Việt vì thiếu dữ liệu chuẩn; phần đo bằng số chạy trên dữ liệu tiếng Anh, tiếng Việt mới dừng ở minh hoạ.",
];
li.forEach((t, i) => {
  const y = 2.5 + i * 1.05;
  circle(M + 0.03, y + 0.28, 0.16, ACCENT, "");
  text(t, { x: M + 0.5, y: y, w: 11.1, h: 0.85, fontSize: 14, color: BODY, fontFace: BF, valign: "middle", lh: 1.25, margin: 0 });
});
citeFooter("cây giao diện không phải chuẩn vàng: phần lớn nút ảnh thiếu nhãn trợ năng (~77% ảnh bấm được) — Chen et al. (ICSE 2020).");
pageno(); done();

// ============================================================ 14 · NHÌN LẠI ĐÓNG GÓP (recap chot)
slide();
head("Nhìn lại đóng góp", "Hai nhánh — mỗi nhánh một khẳng định chắc");
[["A", "Hệ thống viết hướng dẫn bám màn", "Giảm việc nhắc tới nút không tồn tại; cái giá là tỉ lệ phải chuyển sang mô tả — báo minh bạch, không khoe gần 100%. Chạy được với nhiều đời mô hình.", STEEL, FILL],
["B", "Cách đánh giá không cần đáp án mẫu", "Đo được chất lượng mà không cần bản mẫu người soạn và không để hệ tự chấm mình; bản thân thước đo tự kiểm được bằng lỗi cố ý.", ACCENT, TINT]].forEach((c, i) => {
  const x = M + i * 5.95;
  rect(x, 2.4, 5.5, 3.15, c[5], { radius: 0.1 });
  circle(x + 0.35, 2.72, 0.75, c[3], c[0]);
  text(c[1], { x: x + 1.35, y: 2.72, w: 3.95, h: 0.95, fontSize: 16, bold: true, color: INK, fontFace: TF, valign: "middle", margin: 0, lh: 1.05 });
  text([{ text: "Khẳng định chắc:  ", options: { bold: true, color: c[3] } }, { text: c[2], options: { color: BODY } }], { x: x + 0.4, y: 3.8, w: 4.7, h: 1.6, fontSize: 13.5, fontFace: BF, lh: 1.28, margin: 0 });
});
rect(M, 5.75, W - 2 * M, 1.15, NAVY, { radius: 0.1 });
text([{ text: "Để hai nhánh thật sự ngang nhau:  ", options: { bold: true, color: "E4A986" } }, { text: "điểm sắp thứ tự và điểm làm đúng từng bước phải thật sự dương. Nếu âm, luận văn nói thẳng đó cũng là một kết quả hợp lệ, không tô vẽ.", options: { color: "D6DBE2" } }], { x: M + 0.4, y: 5.75, w: W - 2 * M - 0.8, h: 1.15, fontSize: 13.5, fontFace: BF, valign: "middle", lh: 1.25, margin: 0 });
pageno(); done();

// ============================================================ 14B · TÀI LIỆU THAM KHẢO
slide();
head("Tài liệu", "Nền tài liệu cho các lựa chọn thiết kế — nhấn vào tên bài để mở");
const refCols = [
  ["Khung đánh giá & độ trung thực", [
    ["Chim, Ive & Liakata (Comput. Linguistics 2025)", "https://aclanthology.org/2025.cl-1.6/"],
    ["ALOHa (NAACL 2024)", "https://aclanthology.org/2024.naacl-short.30/"],
    ["FaithScore (Findings EMNLP 2024)", "https://aclanthology.org/2024.findings-emnlp.290/"],
    ["FActScore (EMNLP 2023)", "https://aclanthology.org/2023.emnlp-main.741/"],
    ["Sai et al. (EMNLP 2021)", "https://aclanthology.org/2021.emnlp-main.575/"],
    ["Clark et al. (ACL-IJCNLP 2021)", "https://aclanthology.org/2021.acl-long.565/"],
    ["Panickssery et al. (NeurIPS 2024)", "https://proceedings.neurips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html"],
  ]],
  ["Sắp thứ tự màn", [
    ["Qin et al. (Findings NAACL 2024)", "https://aclanthology.org/2024.findings-naacl.97/"],
    ["Dwork et al. (WWW 2001)", "https://doi.org/10.1145/371920.372165"],
    ["Ailon et al. (J. ACM 2008)", "https://doi.org/10.1145/1411509.1411513"],
    ["Fagin et al. (SIAM J. Discrete Math 2006)", "https://doi.org/10.1137/05063088X"],
    ["Lapata (Comput. Linguistics 2006)", "https://aclanthology.org/J06-4002/"],
    ["TOMATO (ICLR 2025)", "https://arxiv.org/abs/2410.23266"],
  ]],
  ["Dữ liệu, grounding & thống kê", [
    ["AndroidControl (NeurIPS 2024)", "https://arxiv.org/abs/2406.03679"],
    ["AITW (NeurIPS 2023)", "https://arxiv.org/abs/2307.10088"],
    ["SeeClick (ACL 2024)", "https://aclanthology.org/2024.acl-long.505/"],
    ["OS-Atlas / ScreenSpot-v2 (ICLR 2025)", "https://arxiv.org/abs/2410.23218"],
    ["Chen et al. (ICSE 2020)", "https://doi.org/10.1145/3377811.3380327"],
    ["MacKinnon, Nielsen & Webb (J. Econometrics 2023)", "https://doi.org/10.1016/j.jeconom.2022.04.001"],
  ]],
];
refCols.forEach((col, i) => {
  const x = M + i * 3.95;
  rect(x - 0.15, 2.25, 3.78, 4.4, FILL, { radius: 0.1 });
  text(col[0], { x: x + 0.1, y: 2.5, w: 3.45, h: 0.7, fontSize: 14, bold: true, color: ACCENT, fontFace: TF, margin: 0, lh: 1.12 });
  const runs = col[1].map(([nm, url]) => ({ text: "·  " + nm, options: { hyperlink: { url }, color: STEEL, breakLine: true } }));
  text(runs, { x: x + 0.1, y: 3.25, w: 3.5, h: 3.2, fontSize: 11.5, color: STEEL, fontFace: BF, lh: 1.5, margin: 0 });
});
pageno(); done();

// ============================================================ 15 · KẾT LUẬN (dark)
slide(NAVY);
text("KẾT LUẬN", { x: M, y: 2.15, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Khi không có bản hướng dẫn mẫu, ta dựa vào chính danh sách nút thật của màn hình — chỉ dùng lúc kiểm, không đưa cho mô hình lúc viết.", { x: M, y: 2.7, w: 11.3, h: 1.7, fontSize: 23, bold: true, color: WHITE, fontFace: TF, lh: 1.2, margin: 0 });
text("Kết quả gồm một hệ thống viết hướng dẫn ít nhắc nút sai, và một cách đánh giá độc lập, tự kiểm được và nói rõ giới hạn.", { x: M, y: 4.75, w: 11.3, h: 1.2, fontSize: 16, color: "C9D2DC", fontFace: BF, lh: 1.35, margin: 0 });
text("Xin cảm ơn hội đồng.", { x: M, y: 6.2, w: 11, h: 0.5, fontSize: 16, italic: true, color: "8FA0B2", fontFace: TF, margin: 0 });
done();

// ---- helper: HTML table mirror ----
function tableHTML(rows, x, y, colW, rowH) {
  const totalW = colW.reduce((a, b) => a + b, 0);
  let h = `<table style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:${totalW * PX}px;border-collapse:collapse;font-family:${FMAP[BF]};font-size:14px">`;
  rows.forEach(r => {
    h += `<tr>`;
    r.forEach((c, ci) => {
      const o = c.options || {};
      h += `<td style="width:${colW[ci] * PX}px;height:${rowH * PX}px;border:1px solid #${RULE};`
        + (o.fill ? `background:#${o.fill};` : "") + `color:#${o.color || BODY};`
        + (o.bold ? "font-weight:700;" : "") + `text-align:${o.align || "left"};padding:4px 8px;vertical-align:middle">${esc(c.text)}</td>`;
    });
    h += `</tr>`;
  });
  return h + `</table>`;
}

// ---- write outputs ----
fs.mkdirSync("_preview", { recursive: true });
const page = `<!doctype html><meta charset="utf-8"><style>
@page{size:${W}in ${H}in;margin:0}
*{margin:0;box-sizing:border-box}
.slide{position:relative;width:${W}in;height:${H}in;overflow:hidden;page-break-after:always}
</style>` + htmlSlides.join("\n");
fs.writeFileSync("_preview/preview.html", page);

pres.writeFile({ fileName: "../LUAN_VAN_SLIDE_v2.pptx" })
  .then(f => console.log("PPTX ->", f, "| slides:", htmlSlides.length))
  .catch(e => console.error("ERR", e));
