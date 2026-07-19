// Deck v3 — CHI FOCUS PIPELINE (de thay chot khung xu ly truoc). It chu, nhieu hinh.
// Dual-emit: ../LUAN_VAN_SLIDE_v3.pptx + _preview_v3/preview.html (QA bo cuc bang weasyprint).
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Luan van thac si";
pres.title = "Pipeline sinh huong dan su dung phan mem";

// ---- palette ----
const TF = "Cambria", BF = "Segoe UI";
const INK = "1D2733", BODY = "454C55", MUTE = "8B929B";
const ACCENT = "BE5A2E", STEEL = "52657A", GOOD = "1E6B43";
const RULE = "DBE0E6", FILL = "F3F5F7", TINT = "F7EBE3", NAVY = "17233B", WHITE = "FFFFFF";
const W = 13.33, H = 7.5, M = 0.92;

// ---- HTML preview mirror ----
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

function text(content, o) {
  const opt = Object.assign({ x: 0, y: 0, w: 4, h: 1, fontSize: 14, color: BODY, fontFace: BF,
    align: "left", valign: "top", margin: o.margin != null ? o.margin : 4 }, o);
  if (o.lh) opt.lineSpacingMultiple = o.lh;
  if (o.spacing) opt.charSpacing = o.spacing;
  s.addText(content, opt);
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

// ============================================================ 1 · TITLE
slide(NAVY);
text("QUY TRÌNH XỬ LÝ · PIPELINE", { x: M, y: 1.5, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Sinh hướng dẫn sử dụng phần mềm\ntừ ảnh giao diện và câu hỏi", { x: M - 0.02, y: 2.15, w: 9.6, h: 1.9, fontSize: 33, bold: true, color: WHITE, fontFace: TF, lh: 1.08, margin: 0 });
text("Bản trình bày quy trình xử lý — xin thầy chốt khung trước", { x: M, y: 4.35, w: 9.4, h: 0.6, fontSize: 18, italic: true, color: "C9D2DC", fontFace: TF, margin: 0 });
text("Học viên · · · · ·      Giảng viên hướng dẫn · · · · ·      2026", { x: M, y: 6.55, w: 11, h: 0.4, fontSize: 13, color: "8FA0B2", fontFace: BF, margin: 0 });
shot("real_mv_1.png", 10.4, 2.0, 1.95, 3.2);
done();

// ============================================================ 2 · VÀO / RA
slide();
head("Vào và ra", "Một ảnh và một câu hỏi, ra hướng dẫn từng bước");
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

// ============================================================ 3 · TOÀN CẢNH PIPELINE
slide();
head("Toàn cảnh quy trình", "Một hệ duy nhất — chọn nhánh theo số ảnh đưa vào");
rect(M, 2.95, 2.15, 3.55, NAVY, { radius: 0.1 });
text("VÀO", { x: M, y: 3.12, w: 2.15, h: 0.3, fontSize: 12, bold: true, color: "E4A986", fontFace: BF, align: "center", spacing: 2, margin: 0 });
text("Một hoặc nhiều ảnh\n(có thể xáo trộn)\nkèm câu hỏi", { x: M + 0.12, y: 3.5, w: 1.9, h: 1.55, fontSize: 13, color: WHITE, fontFace: BF, align: "center", valign: "middle", lh: 1.3, margin: 0 });
text("chọn nhánh\ntheo số ảnh", { x: M + 0.1, y: 5.35, w: 1.95, h: 0.95, fontSize: 12, italic: true, color: "C9D2DC", fontFace: BF, align: "center", valign: "middle", lh: 1.2, margin: 0 });
arrow(3.12, 3.55, 0.5, STEEL);
arrow(3.12, 5.55, 0.5, STEEL);
text("Chỉ một ảnh — một màn", { x: 3.75, y: 2.9, w: 4, h: 0.3, fontSize: 12.5, bold: true, color: STEEL, fontFace: BF, margin: 0 });
["Viết mù\n(ảnh + câu hỏi)", "Đối chiếu\nnút thật", "Viết lại\nchỗ bịa"].forEach((t, i) => {
  const x = 3.75 + i * 2.28;
  rect(x, 3.28, 1.95, 1.0, FILL, { radius: 0.09 });
  circle(x + 0.12, 3.36, 0.36, i === 1 ? ACCENT : STEEL, String(i + 1));
  text(t, { x: x + 0.02, y: 3.5, w: 1.9, h: 0.72, fontSize: 12, bold: true, color: INK, fontFace: BF, align: "center", valign: "middle", lh: 1.12, margin: 0 });
  if (i < 2) arrow(x + 1.97, 3.78, 0.26, ACCENT);
});
text("→  bản hướng dẫn", { x: 10.6, y: 3.5, w: 2.5, h: 0.56, fontSize: 12.5, bold: true, color: GOOD, fontFace: BF, valign: "middle", margin: 0 });
text("Từ hai ảnh trở lên — nhiều màn", { x: 3.75, y: 4.95, w: 4.5, h: 0.3, fontSize: 12.5, bold: true, color: STEEL, fontFace: BF, margin: 0 });
rect(3.75, 5.32, 4.35, 1.0, TINT, { radius: 0.09 });
text([{ text: "Bước sắp thứ tự trước:  ", options: { bold: true, color: ACCENT } }, { text: "so từng cặp → đếm phiếu → gỡ vòng mâu thuẫn", options: { color: INK } }], { x: 3.92, y: 5.32, w: 4.05, h: 1.0, fontSize: 12, fontFace: BF, valign: "middle", lh: 1.18, margin: 0 });
arrow(8.15, 5.82, 0.28, ACCENT);
rect(8.5, 5.32, 4.4, 1.0, FILL, { radius: 0.09 });
text("Rồi chạy đúng nhánh một màn cho TỪNG màn đã sắp", { x: 8.66, y: 5.32, w: 4.1, h: 1.0, fontSize: 12.5, bold: true, color: INK, fontFace: BF, valign: "middle", lh: 1.18, margin: 0 });
text([{ text: "Nhánh nhiều màn chính là nhánh một màn, chỉ thêm một bước sắp thứ tự ở đầu.  ", options: { bold: true, color: INK } }, { text: "Khi chỉ có một ảnh, bỏ qua bước sắp.", options: { color: BODY } }], { x: M, y: 6.62, w: 11.5, h: 0.35, fontSize: 13, fontFace: BF, margin: 0 });
pageno(); done();

// ============================================================ 4 · Ý TƯỞNG CỐT LÕI
slide();
head("Ý tưởng cốt lõi", "Không có bản mẫu thì dựa vào chính màn hình để kiểm");
text("Không có đáp án mẫu để chấm, ta lấy chính danh sách nút thật của màn hình làm mốc.", { x: M, y: 2.05, w: 11.3, h: 0.4, fontSize: 16, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
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
rect(M, 5.05, W - 2 * M, 1.1, WHITE, { radius: 0.1, line: RULE, lw: 1 });
text([{ text: "Cách dùng:  ", options: { bold: true, color: ACCENT } }, { text: "đối chiếu từng bước hướng dẫn với danh sách này; bước nào nhắc một nút không có trên màn thì viết lại thành mô tả, không đoán nút khác.", options: { color: BODY } }], { x: M + 0.3, y: 5.05, w: 11.0, h: 1.1, fontSize: 14, fontFace: BF, valign: "middle", lh: 1.3, margin: 0 });
text("Danh sách nút chỉ dùng lúc kiểm, không đưa cho mô hình lúc viết — để phép thử công bằng.", { x: M, y: 6.4, w: 11.3, h: 0.35, fontSize: 13, color: BODY, fontFace: BF, margin: 0 });
pageno(); done();

// ============================================================ 5 · NHÁNH MỘT MÀN (3 buoc)
slide();
head("Nhánh một màn", "Ba bước: viết mù, đối chiếu, viết lại chỗ bịa");
const st1 = [
  ["Viết mù", "Mô hình chỉ thấy ảnh và câu hỏi, tự viết ra bản nháp hướng dẫn — chưa được xem danh sách nút.", STEEL],
  ["Đối chiếu nút thật", "Thuật toán so từng bước với danh sách nút thật của màn: bước này khớp một nút có thật hay không.", ACCENT],
  ["Viết lại chỗ bịa", "Bước nào nhắc nút không có trên màn thì đổi thành mô tả bằng lời, không đoán sang nút khác.", STEEL],
];
st1.forEach((c, i) => {
  const x = M + i * 3.92;
  rect(x, 2.7, 3.6, 3.2, i === 1 ? TINT : FILL, { radius: 0.1 });
  circle(x + 0.32, 3.0, 0.72, c[2], String(i + 1));
  text(c[0], { x: x + 1.2, y: 3.0, w: 2.3, h: 0.72, fontSize: 16.5, bold: true, color: INK, fontFace: TF, valign: "middle", margin: 0, lh: 1.05 });
  text(c[1], { x: x + 0.35, y: 4.05, w: 2.95, h: 1.7, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.32, margin: 0 });
  if (i < 2) arrow(x + 3.66, 4.3, 0.2, ACCENT);
});
text([{ text: "Lưu ý:  ", options: { bold: true, color: ACCENT } }, { text: "bước đối chiếu là thuật toán so nghĩa (so tên nút), không phải thêm một mô hình đoán chồng lên — nên không sinh thêm ảo giác.", options: { color: BODY } }], { x: M, y: 6.35, w: 11.5, h: 0.45, fontSize: 13.5, fontFace: BF, margin: 0 });
pageno(); done();

// ============================================================ 6 · VÍ DỤ MỘT MÀN
slide();
head("Nhánh một màn · ví dụ", "Bắt lỗi khi máy nhắc một nút không có trên màn");
shot("real_mv_1.png", M + 0.1, 2.55, 2.15, 3.52, "Màn đặt giờ");
const er = [
  [{ text: "Máy viết ra", options: { bold: true, fill: FILL, color: INK } }, { text: "Trên màn có nút này?", options: { bold: true, fill: FILL, color: INK } }, { text: "Kết luận", options: { bold: true, fill: FILL, color: INK, align: "center" } }],
  [{ text: "Chọn giờ và phút" }, { text: "Có (giờ, phút)" }, { text: "hợp lệ", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Chọn “PM”" }, { text: "Có (PM)" }, { text: "hợp lệ", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Mở “Cài đặt”" }, { text: "Không có", options: { color: MUTE } }, { text: "nhắc nút không có thật", options: { align: "center", color: ACCENT, bold: true } }],
];
s.addTable(er, { x: 3.55, y: 2.55, w: 8.7, colW: [3.0, 3.15, 2.55], rowH: 0.62, fontFace: BF, fontSize: 14, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
hpush(tableHTML(er, 3.55, 2.55, [3.0, 3.15, 2.55], 0.62));
rect(3.55, 5.02, 8.7, 1.02, TINT, { radius: 0.09 });
text([{ text: "Lớp kiểm làm gì:  ", options: { bold: true, color: ACCENT } }, { text: "hạ bước sai “Mở Cài đặt” xuống mô tả bằng lời, các bước đúng giữ nguyên. Nó chặn việc chỉ vào nút không có thật — nhưng CHƯA bảo đảm bước đó là thao tác đúng (ở đây đúng ra là “Nhấn OK”); mức làm đúng thao tác được đo riêng ở nhánh nhiều màn, nơi có đáp án mẫu.", options: { color: INK } }], { x: 3.8, y: 5.02, w: 8.25, h: 1.02, fontSize: 12.5, fontFace: BF, valign: "middle", lh: 1.22, margin: 0 });
rect(3.55, 6.15, 8.7, 0.78, NAVY, { radius: 0.09 });
text([{ text: "Vì sao KHÔNG đoán nút gần nhất?  ", options: { bold: true, color: "E4A986" } }, { text: "thay nút bịa bằng một nút thật nhưng sai việc (kiểu Submit→Save) sẽ khiến người dùng bấm nhầm mà không hay — lỗi âm thầm.", options: { color: "D6DBE2" } }], { x: 3.8, y: 6.15, w: 8.2, h: 0.78, fontSize: 12, fontFace: BF, valign: "middle", lh: 1.18, margin: 0 });
pageno(); done();

// ============================================================ 7 · NHÁNH NHIỀU MÀN (4 buoc)
slide();
head("Nhánh nhiều màn", "Sắp lại đúng thứ tự trước, rồi viết cho từng màn");
text("Nhiều ảnh đưa vào bị xáo trộn. Trước khi viết hướng dẫn, hệ sắp lại đúng thứ tự các màn — làm theo bốn bước:", { x: M, y: 2.2, w: 11.3, h: 0.6, fontSize: 15.5, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
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
pageno(); done();

// ============================================================ 8 · CHỐT PIPELINE (dark)
slide(NAVY);
text("CHỐT QUY TRÌNH", { x: M, y: 1.35, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Toàn bộ pipeline trong một dòng", { x: M, y: 1.85, w: 11.3, h: 0.7, fontSize: 26, bold: true, color: WHITE, fontFace: TF, lh: 1.1, margin: 0 });
// flow strip
const fl = ["Ảnh + câu hỏi", "Sắp thứ tự\n(nếu nhiều màn)", "Viết mù", "Đối chiếu\nnút thật", "Viết lại\nchỗ bịa", "Hướng dẫn\ncho người"];
fl.forEach((t, i) => {
  const x = M + i * 1.95;
  rect(x, 3.0, 1.7, 1.15, i === fl.length - 1 ? "234A32" : "24334F", { radius: 0.1 });
  text(t, { x: x + 0.05, y: 3.0, w: 1.6, h: 1.15, fontSize: 12, bold: true, color: WHITE, fontFace: BF, align: "center", valign: "middle", lh: 1.15, margin: 0 });
  if (i < fl.length - 1) arrow(x + 1.73, 3.57, 0.17, "E4A986");
});
text("Danh sách nút thật chỉ dùng ở bước đối chiếu, không đưa cho mô hình lúc viết.", { x: M, y: 4.45, w: 11.3, h: 0.4, fontSize: 14, italic: true, color: "C9D2DC", fontFace: BF, margin: 0 });
rect(M, 5.35, W - 2 * M, 1.15, "20304C", { radius: 0.1 });
text([{ text: "Xin thầy chốt khung xử lý này.  ", options: { bold: true, color: "E4A986" } }, { text: "Sau khi chốt, em sẽ trình phần thước đo đánh giá và kế hoạch thí nghiệm ở buổi sau.", options: { color: WHITE } }], { x: M + 0.35, y: 5.35, w: W - 2 * M - 0.7, h: 1.15, fontSize: 15, fontFace: BF, valign: "middle", lh: 1.3, margin: 0 });
done();

// ---- write outputs ----
fs.mkdirSync("_preview_v3", { recursive: true });
const page = `<!doctype html><meta charset="utf-8"><style>
@page{size:${W}in ${H}in;margin:0}
*{margin:0;box-sizing:border-box}
.slide{position:relative;width:${W}in;height:${H}in;overflow:hidden;page-break-after:always}
</style>` + htmlSlides.join("\n");
fs.writeFileSync("_preview_v3/preview.html", page);

pres.writeFile({ fileName: "../LUAN_VAN_SLIDE_v3.pptx" })
  .then(f => console.log("PPTX ->", f, "| slides:", htmlSlides.length))
  .catch(e => console.error("ERR", e));
