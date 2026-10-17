// Deck XIN BẢO VỆ (trình thầy tối 14/10/2026): phương pháp dễ hiểu + thước đo. Số lấy từ thesis/chapters bản 14/10 (123 trang).
// Slide chỉ trình bày nội dung luận văn; lời đề nghị nằm trong ../KICH_BAN_TRINH_THAY.md.
// Mọi số lấy từ thesis/chapters bản 5/10 (153 trang). Style giữ như deck bảo vệ: 4:3, thanh chàm, khối xám, Cambria.
// Chạy: node build_slide.js  ->  ../LUAN_VAN_SLIDE.pptx  +  _preview/preview.html
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const pres = new pptxgen();
pres.defineLayout({ name: "A43", width: 10, height: 7.5 });
pres.layout = "A43";
pres.author = "Le Doan Phuong Uyen";
pres.title = "Phat sinh tu dong huong dan su dung phan mem dua tren LLM - bao cao truoc khi bao ve";

const TF = "Cambria", MONO = "Consolas";
const NAVY = "322164", INK = "1A1A1A";
const FOOTA = "191132", FOOTB = "25194B", FOOTC = "4F417A", FOOTD = "7A7099";
const BLOCK = "E9E8EC", TEAL = "006666", BLUE = "1414BE", RED = "B22222", MAROON = "990000";
const GREY = "5A5A66", WHITE = "FFFFFF", ORANGE = "D9622B", GREEN = "1B8A5A";
const W = 10, H = 7.5, M = 0.5;
const FIG = path.resolve(__dirname, "../../thesis/figures");

const PX = 96;
const FMAP = { "Cambria": "'DejaVu Serif',Georgia,serif", "Consolas": "'DejaVu Sans Mono',monospace" };
let htmlSlides = [], cur = "";
function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function plain(c) { return typeof c === "string" ? c : c.map(r => r.text + (r.options && r.options.breakLine ? "\n" : "")).join(""); }
function hpush(html) { cur += html; }
let s, PAGE = 0, BPAGE = 0, TOTAL = 6;
function slide() { if (cur) htmlSlides.push(cur + "</div>"); s = pres.addSlide(); s.background = { color: WHITE }; cur = `<div class="slide" style="background:#fff">`; }
function done() { if (cur) { htmlSlides.push(cur + "</div>"); cur = ""; } }
function text(content, o) {
  const opt = Object.assign({ x: 0, y: 0, w: 4, h: 1, fontSize: 13, color: INK, fontFace: TF, align: "left", valign: "top", margin: o.margin != null ? o.margin : 4 }, o);
  if (o.lh) opt.lineSpacingMultiple = o.lh;
  s.addText(content, opt);
  const jc = opt.align === "center" ? "center" : opt.align === "right" ? "flex-end" : "flex-start";
  const ai = opt.valign === "middle" ? "center" : opt.valign === "bottom" ? "flex-end" : "flex-start";
  const pad = (opt.margin || 0) / 72;
  // preview: pt -> px nhân 1,333 để ước đúng chỗ tràn chữ
  const st = `position:absolute;left:${opt.x * PX}px;top:${opt.y * PX}px;width:${opt.w * PX}px;height:${opt.h * PX}px;display:flex;justify-content:${jc};align-items:${ai};padding:${pad}in;box-sizing:border-box;font-family:${FMAP[opt.fontFace] || FMAP[TF]};font-size:${(opt.fontSize * 1.333).toFixed(1)}px;color:#${opt.color};text-align:${opt.align};line-height:${o.lh || 1.2};` + (opt.bold ? "font-weight:700;" : "") + (opt.italic ? "font-style:italic;" : "");
  hpush(`<div style="${st}"><div style="white-space:pre-line;width:100%">${esc(plain(content))}</div></div>`);
}
function rect(x, y, w, h, fill, o) {
  o = o || {};
  const shp = o.radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE;
  const p = { x, y, w, h, fill: fill === "none" ? { type: "none" } : { color: fill }, line: o.line ? { color: o.line, width: o.lw || 1 } : { type: "none" } };
  if (o.radius) p.rectRadius = o.radius;
  if (o.shadow) p.shadow = { type: "outer", color: "8C8C99", blur: 5, offset: 2.5, angle: 45, opacity: 0.45 };
  s.addShape(shp, p);
  const st = `position:absolute;left:${x * PX}px;top:${y * PX}px;width:${w * PX}px;height:${h * PX}px;` + (fill === "none" ? "" : `background:#${fill};`) + (o.radius ? `border-radius:${o.radius * PX}px;` : "") + (o.line ? `border:${o.lw || 1}px solid #${o.line};box-sizing:border-box;` : "") + (o.shadow ? "box-shadow:2px 2px 5px rgba(140,140,153,.45);" : "");
  hpush(`<div style="${st}"></div>`);
}
function hline(x, y, w, c, lw) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || "9A94AE", width: lw || 1 } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:${w * PX}px;height:0;border-top:${lw || 1}px solid #${c || "9A94AE"}"></div>`);
}
function vline(x, y, h, c, lw, dash) {
  s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color: c || "9A94AE", width: lw || 1, dashType: dash ? "dash" : "solid" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:0;height:${h * PX}px;border-left:${lw || 1}px ${dash ? "dashed" : "solid"} #${c || "9A94AE"}"></div>`);
}
function arrow(x, y, w, c) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || FOOTC, width: 2, endArrowType: "triangle" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX - 1}px;width:${w * PX}px;height:0;border-top:2px solid #${c || FOOTC}"></div>`);
}
function varrow(x, y, h, c, up) {
  const p = { x, y, w: 0, h, line: { color: c || FOOTC, width: 2 } };
  if (up) p.line.beginArrowType = "triangle"; else p.line.endArrowType = "triangle";
  s.addShape(pres.shapes.LINE, p);
  hpush(`<div style="position:absolute;left:${x * PX - 1}px;top:${y * PX}px;width:0;height:${h * PX}px;border-left:2px solid #${c || FOOTC}"></div>`);
}
function img(file, x, y, w, h) {
  s.addImage({ path: file, x, y, w, h });
  hpush(`<img src="file://${file}" style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:${w * PX}px;height:${h * PX}px">`);
}
// ảnh giữ tỉ lệ, nằm gọn trong khung (x,y,w,h), căn giữa
function imgFit(file, pw, ph, x, y, w, h) {
  const r = Math.min(w / pw, h / ph), ww = pw * r, hh = ph * r;
  img(file, x + (w - ww) / 2, y + (h - hh) / 2, ww, hh);
}
const NOTES = [];
function note(t) { s.addNotes(t.trim()); NOTES.push(t.trim()); }
function bar(t) {
  rect(0, 0, W, 0.6, NAVY);
  text(t, { x: 0.22, y: 0, w: W - 0.44, h: 0.6, fontSize: 19, bold: true, color: WHITE, valign: "middle", margin: 0 });
}
function footRow(label) {
  const yy = H - 0.26, hh = 0.26;
  rect(0, yy, 3.0, hh, FOOTA); rect(3.0, yy, 3.7, hh, FOOTB);
  rect(6.7, yy, 1.9, hh, FOOTC); rect(8.6, yy, 1.4, hh, FOOTD);
  text("Luận văn thạc sĩ", { x: 0, y: yy, w: 3.0, h: hh, fontSize: 8, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, fontFace: MONO });
  text("Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM", { x: 3.0, y: yy, w: 3.7, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text("Lê Đoàn Phương Uyên", { x: 6.7, y: yy, w: 1.9, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text(label, { x: 8.6, y: yy, w: 1.4, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
}
function foot() { PAGE++; footRow(`${PAGE}/${TOTAL}`); }
function footB() { BPAGE++; footRow(`dự phòng ${BPAGE}`); }
function block(x, y, w, h, fill) { rect(x, y, w, h, fill || BLOCK, { radius: 0.06, shadow: true }); }
function box(x, y, w, h, t, o) {
  o = o || {};
  rect(x, y, w, h, o.fill || WHITE, { radius: 0.06, line: o.line || "6E6890", lw: o.lw || 1.2 });
  text(t, { x, y, w, h, fontSize: o.fs || 11.5, align: "center", valign: "middle", bold: o.bold, color: o.color || INK, margin: 3, lh: 1.15 });
}
function bullets(items, x, y, w, o) {
  o = o || {};
  const fs = o.fs || 14, gap = o.gap || 0.62, lh = o.lh || 1.25;
  items.forEach((it, i) => {
    const yy = y + i * gap;
    text("•", { x, y: yy, w: 0.22, h: gap, fontSize: fs, color: o.dot || TEAL, bold: true, margin: 0 });
    text(it, { x: x + 0.25, y: yy, w: w - 0.25, h: o.itemH || gap, fontSize: fs, color: o.color || INK, margin: 0, lh });
  });
  return y + items.length * gap;
}
function table(x, y, colW, rows, o) {
  o = o || {};
  const rowH = o.rowH || 0.33, fs = o.fs || 11.5;
  const totalW = colW.reduce((a, b) => a + b, 0);
  let yy = y;
  rows.forEach(r => {
    const h = r.h || rowH;
    if (r.fill) rect(x, yy, totalW, h, r.fill);
    let xx = x;
    if (r.span) { text(r.span, { x: x + 0.03, y: yy, w: totalW - 0.06, h, fontSize: r.fs || fs, bold: true, color: r.color || NAVY, valign: "middle", margin: 3 }); yy += h; return; }
    r.cells.forEach((c, ci) => {
      const cell = (typeof c === "string" || Array.isArray(c)) ? { t: c } : c;
      text(cell.t, {
        x: xx, y: yy, w: colW[ci], h, fontSize: cell.fs || r.fs || fs,
        bold: cell.bold != null ? cell.bold : r.bold, italic: cell.italic, color: cell.color || r.color || INK,
        align: cell.align || (o.align && o.align[ci]) || "left", valign: "middle", margin: 3
      });
      xx += colW[ci];
    });
    if (r.rule) hline(x, yy + h, totalW, r.rule === true ? "9A94AE" : r.rule, r.ruleW || 1);
    yy += h;
  });
  return yy;
}
const B = (t) => ({ text: t, options: { bold: true } });
const P = (t) => ({ text: t, options: {} });
const C = (t, c) => ({ text: t, options: { bold: true, color: c } });
const FIGSP = FIG + "/fig_vidu_spice.png";
function tile(x, y, w, h, big, small, o) {
  o = o || {};
  block(x, y, w, h);
  text(big, { x: x + 0.15, y: y + 0.08, w: w - 0.3, h: 0.42, fontSize: o.bf || 18, bold: true, color: o.color || NAVY, margin: 0 });
  text(small, { x: x + 0.15, y: y + 0.52, w: w - 0.3, h: h - 0.58, fontSize: o.sf || 11, margin: 0, lh: 1.15 });
}
function circ(x, y, n) {
  rect(x, y, 0.42, 0.42, NAVY, { radius: 0.2 });
  text(String(n), { x, y, w: 0.42, h: 0.42, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
}

// ══════════ 1 · BÌA ══════════
slide();
rect(0, 0, W, 0.66, NAVY);
text("ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  -  TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN", { x: 0, y: 0, w: W, h: 0.66, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
rect(0.8, 1.2, W - 1.6, 2.45, NAVY, { radius: 0.09, shadow: true });
text("Luận văn thạc sĩ  -  Ngành Trí tuệ nhân tạo", { x: 0.8, y: 1.5, w: W - 1.6, h: 0.4, fontSize: 15, bold: true, color: WHITE, align: "center", margin: 0 });
text("PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM\nDỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG\nVÀ GIAO DIỆN NGƯỜI DÙNG", { x: 0.8, y: 1.95, w: W - 1.6, h: 1.6, fontSize: 21, bold: true, color: WHITE, align: "center", margin: 0, lh: 1.25 });
text("LLM-Based Automatic Generation of Software User Guides from Use Cases and Front-End Structures", { x: 0.8, y: 3.75, w: W - 1.6, h: 0.35, fontSize: 12, italic: true, color: GREY, align: "center", margin: 0 });
text("Báo cáo luận văn trước thầy hướng dẫn", { x: 0.8, y: 4.3, w: W - 1.6, h: 0.4, fontSize: 16, bold: true, color: TEAL, align: "center", margin: 0 });
text("Học viên thực hiện:   Lê Đoàn Phương Uyên", { x: 0.8, y: 4.85, w: W - 1.6, h: 0.4, fontSize: 15, bold: true, align: "center", margin: 0 });
text("Giáo viên hướng dẫn:   TS. Nguyễn Hồng Bửu Long", { x: 0.8, y: 5.3, w: W - 1.6, h: 0.4, fontSize: 15, bold: true, align: "center", margin: 0 });
text("TP. Hồ Chí Minh  -  Tháng 10 năm 2026", { x: 0.8, y: 6.05, w: W - 1.6, h: 0.35, fontSize: 12, align: "center", margin: 0 });
note(`(20 giây)
Em chào thầy. Hôm nay em báo cáo nội dung luận văn đã hoàn chỉnh: bài toán, thước đo, phương pháp đề xuất và kết quả. Phần trình bày khoảng mười lăm phút. Cuối buổi em xin ý kiến thầy về việc bảo vệ ở đợt này.`);
foot();

// ══════════ 4 · THƯỚC EXECUTABILITY ══════════
slide();
bar("Thước đo executability");
box(M, 0.9, 1.75, 0.95, "câu do mô hình\nsinh ra", { fs: 11.5 });
arrow(M + 1.8, 1.375, 0.35);
box(M + 2.2, 0.9, 1.9, 0.95, "mô hình định vị\nUGround-V1-2B\n(không biết đáp án)", { fs: 10.5, fill: "EEEAF6", line: NAVY });
arrow(M + 4.15, 1.375, 0.35);
box(M + 4.55, 0.9, 1.25, 0.95, "một điểm\n(x, y)", { fs: 11.5 });
block(M, 2.15, 5.3, 2.75);
text("Một bước được tính là đúng khi đồng thời", { x: M + 0.2, y: 2.25, w: 5.0, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "câu gọi đúng loại thao tác (chạm, cuộn, gõ chữ, quay lại...);",
  "điểm nằm trong dung sai 0,14 bề rộng và bề cao màn quanh điểm người dùng đã chạm;",
  "điểm rơi vào ô Voronoi của điểm chạm, tức gần điểm chạm hơn mọi phần tử bấm được khác trên màn.",
], M + 0.2, 2.7, 4.95, { fs: 12.5, gap: 0.68, itemH: 0.66 });
text("Tập kiểm: 6.958 bước, trong đó 4.463 bước chạm (1.432 tác vụ), không trùng tác vụ nào với tập dạy 64.567 bước. Điểm của một hệ thống là tỉ lệ bước đúng trên 4.463 bước chạm này.", { x: M, y: 5.0, w: 5.3, h: 0.9, fontSize: 12, margin: 0, lh: 1.2 });
text("Mô hình định vị không nằm trong vòng huấn luyện của bất kỳ nhánh nào.", { x: M, y: 5.75, w: 5.3, h: 0.6, fontSize: 12.5, italic: true, color: GREY, margin: 0, lh: 1.2 });
imgFit(FIG + "/fig_voronoi.png", 1080, 740, 6.0, 2.15, 3.5, 2.6);
text("Màn hình thật trong tập kiểm. Câu của S1 dẫn tới đúng ô Birthday, câu của mô hình gốc dẫn sang ô Gender ngay phía trên.", { x: 6.0, y: 4.9, w: 3.55, h: 1.2, fontSize: 10.5, italic: true, color: GREY, margin: 0, lh: 1.2 });
note(`(1 phút 15)
Câu sinh ra được đưa cho UGround, một mô hình định vị không biết đáp án. UGround trả về một điểm. Bước được tính đúng khi ba điều kiện cùng đạt: câu gọi đúng loại thao tác; điểm nằm trong dung sai 0,14 quanh điểm người dùng đã chạm; và điểm rơi vào ô Voronoi của điểm chạm, tức gần điểm chạm hơn mọi phần tử bấm được khác.
Điều kiện thứ ba để loại các câu chỉ sai nút bên cạnh: với những câu đó, luật dung sai đơn thuần vẫn cho điểm 84,3% số ca, còn Voronoi chỉ còn 2,8%.
Ví dụ bên phải là màn hình thật: câu của S1 dẫn tới đúng ô Birthday, câu của mô hình gốc dẫn sang ô Gender.`);
foot();

// ══════════ 7 · PHƯƠNG PHÁP TỔNG QUAN ══════════
slide();
bar("Phương pháp đề xuất: hai thành phần nối tiếp");
const CX = [0.5, 2.95, 5.5];
box(CX[0], 0.95, 2.1, 1.1, "đầu vào của bước:\nảnh, mục tiêu,\nlịch sử, chữ OCR", { fs: 10.5 });
arrow(CX[0] + 2.12, 1.5, 0.3);
box(CX[1], 0.95, 2.3, 1.1, "Thành phần 1\nS1 học tiếp bằng\nhọc tăng cường, thưởng SPICE", { fs: 10.5, fill: "EEEAF6", line: NAVY, lw: 1.6, bold: true });
arrow(CX[1] + 2.32, 1.5, 0.15);
box(CX[2], 0.95, 2.3, 1.1, "câu nháp\n(giải mã tham lam)", { fs: 11.5 });
box(CX[0], 2.85, 2.1, 1.1, "tìm 4 câu chuẩn của\ncác bước giống nhất\ntrong tập dạy", { fs: 10.5 });
arrow(CX[0] + 2.12, 3.4, 0.3);
box(CX[1], 2.85, 2.3, 1.1, "Thành phần 2 (ACE)\nbộ sinh xem 4 câu ví dụ,\nchép hoặc tự viết", { fs: 10.5, fill: "EEEAF6", line: NAVY, lw: 1.6, bold: true });
arrow(CX[1] + 2.32, 3.4, 0.15);
box(CX[2], 2.85, 2.3, 1.1, "luật đồng thuận:\nchép nguyên văn\nvà cùng loại thao tác", { fs: 10.5 });
varrow(CX[2] + 1.15, 2.07, 0.76, FOOTC);
arrow(CX[2] + 2.32, 3.4, 0.3);
box(8.15, 2.85, 1.35, 1.1, "câu\ncuối cùng", { fs: 11.5, bold: true, line: NAVY, lw: 1.6 });
block(M, 4.3, W - 2 * M, 2.6);
bullets([
  "Thành phần 1 dạy mô hình viết câu hay hơn: viết nhiều câu cho cùng một bước, câu nào giống câu chuẩn hơn theo SPICE thì được khuyến khích.",
  "Thành phần 2 tận dụng việc nhiều bước mới rất giống một bước đã có câu chuẩn: mượn nguyên văn câu ấy, nhưng chỉ khi luật đồng thuận cho phép.",
  "Lúc sinh câu không thành phần nào thấy câu chuẩn của bước đang xét, và mô hình định vị dùng để chấm không tham gia huấn luyện hay chọn câu.",
], M + 0.2, 4.45, W - 2 * M - 0.4, { fs: 12.5, gap: 0.78, itemH: 0.76 });
note(`(1 phút 15)
Đây là sơ đồ tổng quan. Điểm xuất phát là S1. Phương pháp cải thiện câu của S1 bằng hai cách bổ sung cho nhau.
Thành phần một cho S1 học tiếp bằng học tăng cường, thưởng là điểm SPICE. Kết quả là một mô hình viết một câu nháp cho mỗi bước.
Thành phần hai tên là ACE. Tập huấn luyện có hơn sáu mươi nghìn câu chuẩn, nhiều bước mới rất giống một bước cũ. ACE tìm bốn câu chuẩn của các bước giống nhất, cho một bộ sinh xem, rồi chỉ thay câu nháp bằng câu của bộ sinh khi câu ấy chép nguyên văn một câu ví dụ và cùng loại thao tác với câu nháp. Ở phần lớn các bước câu nháp vẫn được giữ.
Hai điều cần nhớ: không thành phần nào thấy câu chuẩn của bước đang xét, và mô hình định vị dùng chấm không tham gia vào huấn luyện hay chọn câu.`);
foot();

// ══════════ 8 · THÀNH PHẦN 1 ══════════
slide();
bar("Thành phần 1: học qua việc tự viết nhiều câu rồi chấm điểm");
const ST = [
  ["Viết", "Với mỗi bước, mô hình viết 8 câu khác nhau bằng lấy mẫu ngẫu nhiên."],
  ["Chấm", "Mỗi câu được chấm SPICE so với câu chuẩn, trừ điểm nếu dài hơn câu chuẩn quá ba từ."],
  ["So trong nhóm", "Câu cao hơn trung bình của cả tám câu được khuyến khích, câu thấp hơn bị giảm."],
  ["Cập nhật", "Mô hình viết các câu được khuyến khích thường xuyên hơn, nhưng không đi quá xa S1."],
];
ST.forEach((t, i) => {
  const yy = 0.85 + i * 1.12;
  circ(M, yy + 0.08, i + 1);
  text(t[0], { x: M + 0.55, y: yy, w: 5.2, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
  text(t[1], { x: M + 0.55, y: yy + 0.34, w: 5.2, h: 0.7, fontSize: 12.5, margin: 0, lh: 1.2 });
});
imgFit(FIGSP, 1500, 1660, 6.55, 0.78, 2.95, 3.3);
text("Màn hình thật trong tập kiểm. S1 gọi nút Allow (sai), mô hình học với thưởng SPICE gọi đúng nút Not Now ở cuối màn.", { x: 6.4, y: 4.1, w: 3.2, h: 0.95, fontSize: 10, italic: true, color: GREY, margin: 0, lh: 1.15 });
block(M, 5.3, W - 2 * M, 1.6);
text("SPICE so hai câu theo đối tượng, thuộc tính và quan hệ mà cả hai cùng nêu ra, nên hai câu cùng nói tới một nút vẫn được điểm cao dù dùng từ khác. Mô hình định vị không có mặt trong phần thưởng. Lượt học gồm 500 lần cập nhật, xuất phát từ S1.", { x: M + 0.2, y: 5.38, w: W - 2 * M - 0.4, h: 1.45, fontSize: 12.5, margin: 0, lh: 1.25 });
note(`(1 phút)
Học có giám sát dạy mô hình chép lại câu chuẩn, nhưng không cho biết trong những câu nó có thể viết, câu nào tốt hơn. Học tăng cường bổ sung điều đó, theo cách đã dùng trong sinh chú thích ảnh với CIDEr và SPIDEr.
Bốn bước: một, với mỗi bước mô hình viết tám câu khác nhau. Hai, mỗi câu được chấm SPICE so với câu chuẩn, trừ một khoản nhỏ nếu dài hơn câu chuẩn quá ba từ để mô hình không kể thêm chi tiết thừa. Ba, so điểm từng câu với trung bình của cả nhóm tám câu: cao hơn thì được khuyến khích. Bốn, cập nhật mô hình, có thêm một số hạng phạt độ lệch KL để mô hình không đi quá xa S1.
SPICE chấm theo đối tượng, thuộc tính, quan hệ nên hai câu cùng nói tới một nút vẫn được điểm cao dù khác từ. Ví dụ bên phải: S1 gọi nút Allow, mô hình học với thưởng SPICE gọi đúng nút Not Now.
Mô hình định vị dùng để chấm không có trong phần thưởng, nên thước vẫn độc lập với mục tiêu huấn luyện. Tiền lệ là SCST và SPIDEr trong chú thích ảnh; điểm em nhận là hẹp: áp dụng và đo cho bài toán này, không nhận mới ở thuật toán.`);
foot();

// ══════════ 9 · ACE ══════════
slide();
bar("Thành phần 2 (ACE): mượn câu của bước giống khi chắc chắn");
box(M, 0.85, 2.5, 0.95, "bước đang xét", { fs: 12 });
arrow(M + 2.55, 1.325, 0.4);
box(M + 3.0, 0.85, 3.0, 0.95, "tìm 4 bước giống nhất trong 62.880 bước dạy\n(so mục tiêu và câu trước)", { fs: 10.5 });
arrow(M + 6.05, 1.325, 0.4);
box(M + 6.5, 0.85, 2.5, 0.95, "bộ sinh xem 4 câu ví dụ,\nchép hoặc tự viết", { fs: 10.5, fill: "EEEAF6", line: NAVY });
rect(M, 2.05, W - 2 * M, 1.35, "EEEAF6", { radius: 0.06, line: NAVY, lw: 1.5 });
text("Luật đồng thuận: chỉ thay câu nháp khi cả hai điều kiện cùng đúng", { x: M + 0.2, y: 2.12, w: W - 2 * M - 0.4, h: 0.35, fontSize: 13, bold: true, color: NAVY, margin: 0 });
text("1.  câu của bộ sinh trùng nguyên văn một trong bốn câu ví dụ (bộ sinh chủ động chọn, không tự bịa);\n2.  câu ấy cùng loại thao tác với câu nháp (câu ví dụ đến từ bước khác nên có thể sai thao tác).", { x: M + 0.2, y: 2.52, w: W - 2 * M - 0.4, h: 0.8, fontSize: 12, margin: 0, lh: 1.25 });
block(M, 3.65, 4.4, 3.25, "E3F1EA");
text("Ví dụ 1: nhận câu chép", { x: M + 0.2, y: 3.72, w: 4.0, h: 0.32, fontSize: 13, bold: true, color: GREEN, margin: 0 });
text("Tác vụ: gửi tấm ảnh thứ hai cho một người bạn trên Skype.", { x: M + 0.2, y: 4.08, w: 4.05, h: 0.5, fontSize: 11, italic: true, color: GREY, margin: 0, lh: 1.15 });
text("Câu nháp:  “Click on the first image.”\nBộ sinh chép:  “Select the second photo.”\nCả hai đều là thao tác chạm, luật nhận câu chép. Câu này trùng câu chuẩn của bước.", { x: M + 0.2, y: 4.62, w: 4.05, h: 2.2, fontSize: 11.5, margin: 0, lh: 1.3 });
block(5.1, 3.65, 4.4, 3.25, "F6E6E6");
text("Ví dụ 2: từ chối câu chép", { x: 5.3, y: 3.72, w: 4.0, h: 0.32, fontSize: 13, bold: true, color: RED, margin: 0 });
text("Câu ví dụ lấy từ một bước khác, thuộc loại cuộn.", { x: 5.3, y: 4.08, w: 4.05, h: 0.5, fontSize: 11, italic: true, color: GREY, margin: 0, lh: 1.15 });
text("Câu nháp:  “Click on the close icon”\nBộ sinh chép:  “Swipe up”\nBộ sinh chép đúng nguyên văn nhưng khác loại thao tác với câu nháp, nên luật giữ câu nháp, và câu nháp mới là câu đúng.", { x: 5.3, y: 4.62, w: 4.05, h: 2.2, fontSize: 11.5, margin: 0, lh: 1.3 });
note(`(1 phút)
Nhiều tác vụ trong bộ dữ liệu lặp lại với thay đổi nhỏ, ví dụ cùng một việc trên hai ứng dụng nhắn tin. Vì vậy câu chuẩn của một bước cũ đôi khi dùng được nguyên văn cho bước mới. Nhưng lúc nào cũng chép thì sai nhiều hơn đúng, nên ACE phải quyết định khi nào chép.
Với mỗi bước, ACE tìm bốn bước giống nhất trong tập huấn luyện, chỉ so bằng văn bản. Câu chuẩn của bốn bước ấy là bốn câu ví dụ. Bộ sinh nhận thêm khối ví dụ này. Luật đồng thuận chỉ thay câu nháp khi câu của bộ sinh chép nguyên văn một câu ví dụ và cùng loại thao tác với câu nháp.
Ví dụ một: nháp là "Click on the first image", bộ sinh chép "Select the second photo", cùng là chạm nên nhận, và câu này trùng câu chuẩn. Ví dụ hai: bộ sinh chép "Swipe up" nhưng nháp là thao tác chạm, nên giữ nháp, và nháp mới đúng.`);
foot();

// ══════════ 11 · NHIỀU THƯỚC ══════════
slide();
bar("Bảng số trên tập kiểm: phương pháp đề xuất so với S1");
table(M, 0.85, [3.0, 1.35, 1.35, 1.6, 1.7], [
  { cells: ["Thước", "Mô hình gốc", "S1", "Thưởng SPICE", "Đề xuất (cả hai)"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12 },
  { span: "Theo vị trí (mô hình định vị chấm)", fill: BLOCK, h: 0.3, fs: 11 },
  { cells: ["Executability", "47,6", "59,11", "60,65", { t: "60,68", bold: true }], rule: true },
  { cells: ["Luật hộp phần tử (AndroidControl)", "53,6", "65,49", "67,02", { t: "67,11", bold: true }], rule: true },
  { cells: ["Luật khoảng cách Euclid (AitW)", "63,4", "74,37", "76,25", { t: "76,32", bold: true }], rule: true },
  { span: "So với câu chuẩn (bộ chấm COCO và các thước khác)", fill: BLOCK, h: 0.3, fs: 11 },
  { cells: ["BLEU-4", "15,3", "51,56", "52,36", { t: "53,47", bold: true }], rule: true },
  { cells: ["METEOR", "24,6", "36,79", "37,92", { t: "38,37", bold: true }], rule: true },
  { cells: ["ROUGE-L", "42,3", "67,35", "68,36", { t: "69,08", bold: true }], rule: true },
  { cells: ["CIDEr-D", "88,0", "416,1", "430,0", { t: "442,0", bold: true }], rule: true },
  { cells: ["SPICE", "18,5", "44,37", "45,79", { t: "47,13", bold: true }], rule: true },
  { cells: ["chrF", "40,2", "61,26", "62,86", { t: "63,44", bold: true }], rule: true },
  { cells: ["BERTScore", "40,1", "66,33", "67,07", { t: "67,73", bold: true }] },
], { fs: 12, rowH: 0.36, align: ["left", "center", "center", "center", "center"] });
text("Mọi số trong bảng tính trên 4.463 bước chạm của tập kiểm. CIDEr-D vượt 100 vì mỗi bước chỉ có một câu chuẩn, nên chỉ so được giữa các hàng. Mô hình gốc là Qwen2.5-VL-3B chưa tinh chỉnh; S1 là mô hình tinh chỉnh có giám sát. Câu chuẩn đạt 75,7 theo executability. Executability của phương pháp đề xuất hơn S1 1,57 điểm, KTC 95% [+0,86; +2,31].", { x: M, y: 5.6, w: W - 2 * M, h: 1.2, fontSize: 11.5, italic: true, color: GREY, margin: 0, lh: 1.2 });
note(`(1 phút)
Đây là các thước em dùng để đặt phương pháp cạnh S1. Nhóm trên là ba thước theo vị trí, đều do mô hình định vị chấm: executability, luật hộp phần tử gốc của AndroidControl và luật khoảng cách của AitW. Nhóm dưới là bảy thước so câu chữ với câu chuẩn mà các bài chú thích giao diện như Widget Captioning và Screen2Words vẫn dùng.
Trong ba cột này phương pháp đề xuất cao nhất ở mọi hàng. Điểm đáng nói: phần thưởng chỉ là SPICE nhưng mức tăng không dừng ở SPICE, và các thước vị trí dùng mô hình định vị không hề có trong phần thưởng cũng tăng.
Em xin khai thêm: với các mô hình chênh nhau dưới hai điểm executability, nhóm thước so câu có thể xếp thứ tự khác, nên phép so giữa các mô hình em vẫn đọc trên executability.`);
foot();

// ---- xuất ----
done();
const OUT = "../LUAN_VAN_SLIDE_XIN_BAO_VE.pptx";
pres.writeFile({ fileName: OUT }).then(function () {
  var html = '<!doctype html><meta charset="utf-8"><title>Preview - xin bao ve</title>'
    + '<style>@page{size:960px 720px;margin:0}body{margin:0;font-family:sans-serif}'
    + '.slide{position:relative;width:960px;height:720px;overflow:hidden;page-break-after:always}</style>'
    + htmlSlides.join("\n");
  fs.mkdirSync("_preview", { recursive: true });
  fs.writeFileSync("_preview/preview_xin_bao_ve.html", html);
  let md = "# Kịch bản báo cáo trước thầy: xin bảo vệ đợt này (14/10/2026)\n\nĐi kèm `slides/LUAN_VAN_SLIDE_XIN_BAO_VE.pptx` (" + PAGE + " slide). Sinh bởi `slides/build/build_xin_bao_ve.js` từ phần ghi chú của từng slide; sửa lời dẫn ở script, không sửa tay file này.\n\n";
  NOTES.forEach((n, i) => { md += "## Slide " + (i + 1) + "\n" + n + "\n\n"; });
  fs.writeFileSync("../KICH_BAN_XIN_BAO_VE.md", md);
  console.log("Xong " + OUT + " | slide: " + PAGE);
});
