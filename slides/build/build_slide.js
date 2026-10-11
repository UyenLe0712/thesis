// Deck TRÌNH THẦY (báo cáo tiến độ, tháng 10/2026). Bản 16/8 cất ở _archive/build_slide_16_8.js.
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
pres.title = "Phat sinh tu dong huong dan su dung phan mem dua tren LLM - bao cao tien do";

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
let s, PAGE = 0, BPAGE = 0, TOTAL = 24;
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
function note(t) { s.addNotes(t.trim()); }
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

// ══════════ 1 · BÌA ══════════
slide();
rect(0, 0, W, 0.66, NAVY);
text("ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  -  TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN", { x: 0, y: 0, w: W, h: 0.66, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
rect(0.8, 1.2, W - 1.6, 2.45, NAVY, { radius: 0.09, shadow: true });
text("Luận văn thạc sĩ  -  Ngành Trí tuệ nhân tạo", { x: 0.8, y: 1.5, w: W - 1.6, h: 0.4, fontSize: 15, bold: true, color: WHITE, align: "center", margin: 0 });
text("PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM\nDỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG\nVÀ GIAO DIỆN NGƯỜI DÙNG", { x: 0.8, y: 1.95, w: W - 1.6, h: 1.6, fontSize: 21, bold: true, color: WHITE, align: "center", margin: 0, lh: 1.25 });
text("LLM-Based Automatic Generation of Software User Guides from Use Cases and Front-End Structures", { x: 0.8, y: 3.75, w: W - 1.6, h: 0.35, fontSize: 12, italic: true, color: GREY, align: "center", margin: 0 });
text("Báo cáo tiến độ luận văn", { x: 0.8, y: 4.3, w: W - 1.6, h: 0.4, fontSize: 16, bold: true, color: TEAL, align: "center", margin: 0 });
text("Học viên thực hiện:   Lê Đoàn Phương Uyên", { x: 0.8, y: 4.85, w: W - 1.6, h: 0.4, fontSize: 15, bold: true, align: "center", margin: 0 });
text("Giáo viên hướng dẫn:   TS. Nguyễn Hồng Bửu Long", { x: 0.8, y: 5.3, w: W - 1.6, h: 0.4, fontSize: 15, bold: true, align: "center", margin: 0 });
text("TP. Hồ Chí Minh  -  Tháng 10 năm 2026", { x: 0.8, y: 6.05, w: W - 1.6, h: 0.35, fontSize: 12, align: "center", margin: 0 });
note(`- chào thầy, mục đích buổi gặp: báo cáo luận văn đã hoàn chỉnh tới đâu
- phần nói thêm và lời đề nghị nằm ở kịch bản riêng, không lên slide`);
foot();

// ══════════ 2 · NỘI DUNG ══════════
slide();
bar("Nội dung");
const MUC = [
  ["1", "Bài toán và khó khăn khi chấm câu"],
  ["2", "Thước đo executability và kiểm chứng thước"],
  ["3", "Dữ liệu và mô hình nền"],
  ["4", "Các hướng đã thử và phân tích lỗi"],
  ["5", "Phương pháp đề xuất: học tăng cường thưởng SPICE"],
  ["6", "Đóng góp, hạn chế và hướng phát triển"],
  ["7", "Tình trạng luận văn và các bài báo"],
];
MUC.forEach((m, i) => {
  const yy = 1.0 + i * 0.8;
  rect(1.3, yy, 0.6, 0.6, NAVY, { radius: 0.08 });
  text(m[0], { x: 1.3, y: yy, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text(m[1], { x: 2.15, y: yy, w: 6.6, h: 0.6, fontSize: 17, valign: "middle", margin: 0 });
});
foot();

// ══════════ 3 · BÀI TOÁN ══════════
slide();
bar("Bài toán: cùng đầu vào, đổi người nhận đầu ra");
// hàng trên: tác tử giao diện
text("Tác tử giao diện (dòng nghiên cứu hiện có)", { x: M, y: 0.8, w: 6, h: 0.32, fontSize: 13, bold: true, color: GREY, margin: 0 });
box(M, 1.15, 2.6, 0.85, "ảnh màn hình\n+ mục tiêu", { fs: 12 });
arrow(M + 2.65, 1.575, 0.55);
box(M + 3.25, 1.15, 2.1, 0.85, "mô hình", { fs: 12 });
arrow(M + 5.4, 1.575, 0.55);
box(M + 6.0, 1.15, 3.0, 0.85, "toạ độ (x, y)\nđể phần mềm tự bấm", { fs: 12, color: GREY });
// hàng dưới: đề tài
text("Đề tài này", { x: M, y: 2.3, w: 6, h: 0.32, fontSize: 13, bold: true, color: NAVY, margin: 0 });
box(M, 2.65, 2.6, 1.25, "mục tiêu + các bước đã làm\n(trường hợp sử dụng)\n\nảnh màn hình + chữ trên màn\n(giao diện người dùng)", { fs: 10.5, line: NAVY, lw: 1.6 });
arrow(M + 2.65, 3.275, 0.55, NAVY);
box(M + 3.25, 2.65, 2.1, 1.25, "Qwen2.5-VL-3B\ntinh chỉnh", { fs: 12, bold: true, fill: "EEEAF6", line: NAVY, lw: 1.6 });
arrow(M + 5.4, 3.275, 0.55, NAVY);
box(M + 6.0, 2.65, 3.0, 1.25, "một câu tiếng Anh cho người đọc\n\n“Click on the Not Now button\nat the bottom of the screen”", { fs: 10.5, line: NAVY, lw: 1.6 });
block(M, 4.3, W - 2 * M, 2.65);
text("Đầu vào.", { x: M + 0.25, y: 4.42, w: 1.3, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
text("Mục tiêu người dùng đang thực hiện, các câu hướng dẫn của những bước đã làm, ảnh màn hình đang mở và chữ đọc được trên ảnh.", { x: M + 1.45, y: 4.42, w: W - 2 * M - 1.7, h: 0.6, fontSize: 13, margin: 0, lh: 1.2 });
text("Kết quả.", { x: M + 0.25, y: 5.12, w: 1.3, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
text("Một câu nói rõ cần làm thao tác gì và chạm vào phần tử nào trên màn hình hiện tại.", { x: M + 1.45, y: 5.12, w: W - 2 * M - 1.7, h: 0.6, fontSize: 13, margin: 0, lh: 1.2 });
text("Khác bài gốc.", { x: M + 0.25, y: 5.82, w: 1.2, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
text("Trong AndroidControl (NeurIPS 2024) câu hướng dẫn từng bước là đầu vào của tác tử. Ở đây câu đó là đích mô hình phải sinh ra, và là đầu ra duy nhất được đem chấm.", { x: M + 1.45, y: 5.82, w: W - 2 * M - 1.7, h: 0.95, fontSize: 13, margin: 0, lh: 1.2 });
note(`- dòng tác tử: ảnh -> toạ độ cho máy; đề tài giữ đầu vào, đổi đầu ra thành câu cho người
- ánh xạ tên đề tài: trường hợp sử dụng = mục tiêu + các bước đã làm; giao diện = ảnh + chữ trên màn
- điểm khác bài gốc AndroidControl: câu từng bước là đích sinh, không phải đầu vào`);
foot();

// ══════════ 4 · KHÓ KHĂN KHI CHẤM ══════════
slide();
bar("Khó khăn chính nằm ở việc chấm câu");
block(M, 0.85, 4.35, 3.0);
text("Một phần tử, nhiều cách gọi", { x: M + 0.2, y: 0.95, w: 4.0, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
["“Tap the search bar”", "“Tap the magnifier icon at the top”", "“Click on the search field”"].forEach((t, i) => {
  text(t, { x: M + 0.35, y: 1.45 + i * 0.5, w: 3.9, h: 0.4, fontSize: 12.5, fontFace: MONO, color: BLUE, margin: 0 });
});
text("Bộ dữ liệu chỉ có một câu chuẩn cho mỗi bước.", { x: M + 0.2, y: 3.0, w: 4.0, h: 0.6, fontSize: 12.5, italic: true, color: GREY, margin: 0, lh: 1.2 });
block(5.15, 0.85, 4.35, 3.0);
text("Thước so chữ với câu chuẩn", { x: 5.35, y: 0.95, w: 4.0, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
text("BLEU, ROUGE, METEOR, CIDEr, SPICE chấm độ trùng từ với câu chuẩn, nên phạt cách gọi khác dù vẫn đúng phần tử, và cho điểm câu trùng nhiều từ dù gọi nhầm nút bên cạnh.", { x: 5.35, y: 1.4, w: 3.95, h: 1.5, fontSize: 12.5, margin: 0, lh: 1.25 });
text("Zhao và cộng sự (EACL 2021): các thước này không hiệu quả khi chấm câu chỉ đường có gắn với môi trường.", { x: 5.35, y: 2.85, w: 3.95, h: 0.9, fontSize: 11.5, italic: true, color: GREY, margin: 0, lh: 1.2 });
rect(M, 4.2, W - 2 * M, 1.35, "EEEAF6", { radius: 0.06, line: NAVY, lw: 1.5 });
text("Hướng của đề tài", { x: M + 0.25, y: 4.3, w: 4, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
text("Không hỏi câu sinh ra giống câu chuẩn tới đâu, mà kiểm xem câu ấy có dẫn được một người nghe độc lập tới đúng phần tử người dùng đã chạm hay không.", { x: M + 0.25, y: 4.68, w: W - 2 * M - 0.5, h: 0.8, fontSize: 13.5, margin: 0, lh: 1.22 });
text("Ý tưởng người nghe có gốc từ dòng sinh biểu thức quy chiếu (Mao CVPR 2016, Luo CVPR 2017, Yu CVPR 2017). Phần việc của đề tài là đo và hiệu chuẩn thước này cho miền giao diện di động.", { x: M, y: 5.8, w: W - 2 * M, h: 0.9, fontSize: 12, color: GREY, margin: 0, lh: 1.2 });
note(`- một nút có nhiều tên đúng; mỗi bước chỉ có một câu chuẩn
- thước so chữ phạt cách gọi khác và tha cho câu gọi nhầm nút cạnh bên
- vì thế phần lớn công sức của đề tài dành cho thước đo`);
foot();

// ══════════ 5 · THƯỚC EXECUTABILITY ══════════
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
text("Điểm của một hệ thống là tỉ lệ bước đúng trên 4.463 bước chạm của tập kiểm.", { x: M, y: 5.1, w: 5.3, h: 0.6, fontSize: 12.5, margin: 0, lh: 1.2 });
text("Mô hình định vị không nằm trong vòng huấn luyện của bất kỳ nhánh nào.", { x: M, y: 5.75, w: 5.3, h: 0.6, fontSize: 12.5, italic: true, color: GREY, margin: 0, lh: 1.2 });
imgFit(FIG + "/fig_voronoi.png", 1080, 740, 6.0, 2.15, 3.5, 2.6);
text("Màn hình thật trong tập kiểm. Câu của S1 dẫn tới đúng ô Birthday, câu của mô hình gốc dẫn sang ô Gender ngay phía trên.", { x: 6.0, y: 4.9, w: 3.55, h: 1.2, fontSize: 10.5, italic: true, color: GREY, margin: 0, lh: 1.2 });
note(`- câu -> mô hình định vị không biết đáp án -> điểm
- ba điều kiện: đúng loại thao tác, trong dung sai 0,14, trong ô Voronoi
- vì sao thêm Voronoi: luật dung sai đơn thuần cho điểm câu sai nút ở 84,3% số ca, Voronoi còn 2,8% (dự phòng 1)`);
foot();

// ══════════ 6 · KIỂM CHỨNG THƯỚC ══════════
slide();
bar("Kiểm chứng thước trước khi dùng để kết luận");
// thang 0-100
const X0 = 0.9, XW = 8.2, YS = 2.05;
function xs(v) { return X0 + XW * v / 100; }
text("Vị trí các mốc trên thang executability (%)", { x: M, y: 0.78, w: 7, h: 0.32, fontSize: 13, bold: true, color: NAVY, margin: 0 });
rect(xs(12.0), YS - 0.12, xs(75.7) - xs(12.0), 0.24, "DCD6EA");
hline(X0, YS, XW, "6E6890", 2);
[0, 25, 50, 75, 100].forEach(v => { vline(xs(v), YS - 0.08, 0.16, "6E6890", 1.2); text(String(v), { x: xs(v) - 0.3, y: YS + 0.1, w: 0.6, h: 0.25, fontSize: 9.5, color: GREY, align: "center", margin: 0 }); });
const MOC = [
  [6.1, "câu của\nmàn khác", RED, -1],
  [12.0, "câu chung\nchung", RED, 1],
  [47.6, "Base", GREY, -1],
  [59.1, "S1", TEAL, 1],
  [60.6, "đề xuất", NAVY, -1],
  [75.7, "câu chuẩn\n(trần)", GREEN, 1],
];
MOC.forEach(m => {
  const x = xs(m[0]);
  rect(x - 0.06, YS - 0.06, 0.12, 0.12, m[2]);
  if (m[3] < 0) { vline(x, YS - 0.52, 0.46, m[2], 1); text(m[1] + " " + m[0].toFixed(1).replace(".", ","), { x: x - 0.75, y: YS - 1.0, w: 1.5, h: 0.48, fontSize: 9.5, bold: true, color: m[2], align: "center", valign: "bottom", margin: 0, lh: 1.05 }); }
  else { vline(x, YS + 0.36, 0.3, m[2], 1); text(m[1] + " " + m[0].toFixed(1).replace(".", ","), { x: x - 0.75, y: YS + 0.66, w: 1.5, h: 0.48, fontSize: 9.5, bold: true, color: m[2], align: "center", margin: 0, lh: 1.05 }); }
});
// sáu ô số
const TILE = [
  ["0,7%", "sai số trung vị của mô hình định vị, trong khi phần tử gần nhất thường cách xa hơn 3% bề ngang"],
  ["75,7%", "trần: chấm chính câu chuẩn trên đủ 4.463 bước, KTC [74,1; 77,3]"],
  ["12,0%  ·  6,1%", "sàn: câu chung chung và câu thật của màn khác; văn phong đúng mà nội dung sai không được điểm"],
  ["5 luật", "chấm lại dưới năm luật trúng khác nhau, thứ tự các hệ thống không đổi"],
  ["94%", "chấm lại bằng UI-Venus-Ground-7B (không học AndroidControl): giữ 94% chênh lệch S1 so với Base"],
  ["+0,35", "viết lại 1.139 câu chuẩn theo ba cách giữ nghĩa, điểm gần như không đổi, KTC [−0,59; +1,29]"],
];
TILE.forEach((t, i) => {
  const cx = M + (i % 2) * 4.55, cy = 3.35 + Math.floor(i / 2) * 1.27;
  block(cx, cy, 4.45, 1.18);
  text(t[0], { x: cx + 0.15, y: cy + 0.08, w: 4.15, h: 0.4, fontSize: 17, bold: true, color: NAVY, margin: 0 });
  text(t[1], { x: cx + 0.15, y: cy + 0.48, w: 4.2, h: 0.68, fontSize: 11, margin: 0, lh: 1.15 });
});
note(`- mọi điểm đọc trên nền trần 75,7, không phải 100; dải dùng được từ sàn 12 tới trần
- câu của màn khác thấp hơn cả câu chung chung: thước chấm nội dung, không chấm văn phong
- thêm: người nghe trắc nghiệm Phi-4 (ngoài họ Qwen) giữ nguyên thứ tự các nhánh`);
foot();

// ══════════ 7 · DỮ LIỆU ══════════
slide();
bar("Dữ liệu: dựng tự động từ AndroidControl");
const DL = [["HuggingFace\nparsed_AndroidControl", "câu chuẩn từng bước\n+ cây trợ năng"], ["HuggingFace\nAndroidControl…20k", "ảnh màn hình"]];
box(M, 0.95, 2.6, 0.85, DL[0][0] + "\n" + DL[0][1], { fs: 10 });
box(M, 2.0, 2.6, 0.85, DL[1][0] + "\n" + DL[1][1], { fs: 10 });
arrow(M + 2.65, 1.9, 0.45);
box(M + 3.15, 1.25, 2.4, 1.3, "ghép theo\n(episode_id, step_id)\n+ OCR trên ảnh\n+ nhãn mô tả phần tử", { fs: 10.5, fill: "EEEAF6", line: NAVY });
arrow(M + 5.6, 1.9, 0.45);
box(M + 6.1, 1.25, 2.9, 1.3, "64.567 bước huấn luyện\n12.895 tác vụ\nkhông thuê người gán nhãn", { fs: 11.5, bold: true, line: NAVY, lw: 1.6 });
table(M, 3.3, [4.3, 4.7], [
  { cells: ["Phép kiểm", "Kết quả"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12.5 },
  { cells: ["Ghép đúng hai kho", "48% khớp, so với 20% của phép ghép cố ý lệch một bước"], h: 0.5, fs: 12, rule: true },
  { cells: ["Bất biến cấu trúc", "9/9 bất biến đạt ở quy mô đầy đủ"], h: 0.42, fs: 12, rule: true },
  { cells: ["Rò rỉ giữa tập dạy và tập kiểm", "0 tác vụ trùng nhau"], h: 0.42, fs: 12, rule: true },
  { cells: ["Tập kiểm", "6.958 bước, trong đó 4.463 bước chạm, 1.432 tác vụ"], h: 0.42, fs: 12 },
], {});
text("Cây trợ năng có trung vị 86 phần tử mỗi màn nhưng phần lớn không có tên, nên tên phần tử lấy thêm từ chữ đọc được trên ảnh. Chi tiết ở Chương 3.", { x: M, y: 5.75, w: W - 2 * M, h: 0.8, fontSize: 12, italic: true, color: GREY, margin: 0, lh: 1.2 });
note(`- không có bộ dữ liệu sẵn cho bài toán này, nên dựng từ AndroidControl
- ba phép kiểm: ghép, bất biến, rò rỉ
- phần dữ liệu đã viết thành bài VCL 2026`);
foot();

// ══════════ 8 · MÔ HÌNH NỀN ══════════
slide();
bar("Mô hình nền: tinh chỉnh có giám sát (S1)");
block(M, 0.85, 4.1, 3.5);
text("Cấu hình", { x: M + 0.2, y: 0.95, w: 3.7, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Qwen2.5-VL-3B-Instruct",
  "QLoRA 4-bit trên phần ngôn ngữ, phần thị giác đóng băng",
  "hai lượt duyệt, 8.072 bước, GPU A100",
  "hai hạt giống: 101 và 202",
], M + 0.2, 1.38, 3.75, { fs: 12.5, gap: 0.72, itemH: 0.7 });
// cột điểm
const BX = 5.2, BY = 4.0, BH = 3.0; // đáy BY, cao tối đa cho 80
function bcol(i, v, lab, col) {
  const w = 0.75, x = BX + i * 1.05, h = BH * v / 80;
  rect(x, BY - h, w, h, col);
  text(v.toFixed(1).replace(".", ","), { x: x - 0.2, y: BY - h - 0.32, w: w + 0.4, h: 0.3, fontSize: 12, bold: true, color: col, align: "center", margin: 0 });
  text(lab, { x: x - 0.25, y: BY + 0.05, w: w + 0.5, h: 0.45, fontSize: 10.5, align: "center", margin: 0, lh: 1.05 });
}
hline(BX - 0.1, BY, 4.35, "6E6890", 1.2);
bcol(0, 47.6, "Base", "8A8798");
bcol(1, 59.1, "S1\nhạt 101", TEAL);
bcol(2, 59.6, "S1\nhạt 202", TEAL);
bcol(3, 75.7, "câu\nchuẩn", GREEN);
text("executability (%)", { x: BX, y: 0.85, w: 4, h: 0.3, fontSize: 11, italic: true, color: GREY, margin: 0 });
block(M, 4.6, W - 2 * M, 2.25);
bullets([
  [P("S1 hơn Base "), B("11,5 điểm"), P(" (ghép cặp, p < 0,001); hai hạt giống cho 11,5 và 12,0, nhiễu giữa hai hạt 0,46 điểm.")],
  [P("Chênh lệch giữ nguyên sau khi kiểm sáu cách giải thích thay thế; bỏ hẳn những câu chép nguyên văn câu chuẩn vẫn còn 8,4 điểm.")],
  [P("Theo luật hộp phần tử của chính AndroidControl: Base 53,6, S1 65,5, câu chuẩn 83,8.")],
], M + 0.2, 4.72, W - 2 * M - 0.4, { fs: 12.5, gap: 0.7, itemH: 0.68 });
note(`- S1 là nền của mọi nhánh sau và là mốc so của phương pháp đề xuất
- khoảng tin cậy của Base, S1, trần rời nhau: thước tách được ba mức
- sáu cách giải thích thay thế ở ch6, trong đó có đổi bộ trỏ`);
foot();

// ══════════ 9 · CÁC HƯỚNG ĐÃ THỬ ══════════
slide();
bar("Các hướng đã thử trước phương pháp đề xuất");
table(M, 0.8, [2.35, 3.85, 2.8], [
  { cells: ["Hướng", "Ý tưởng", "Kết quả trên tập kiểm"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12 },
  { cells: [{ t: "Đích khai báo (S2)", bold: true }, "viết dòng khai báo vai trò, tên, toạ độ, dấu hiệu phân biệt rồi mới viết câu", "57,2 · thấp hơn S1 1,93 điểm"], h: 0.66, fs: 11, rule: true },
  { cells: [{ t: "Mục tiêu ưu tiên (MIN-DESC)", bold: true }, "học tiếp bằng ORPO trên cặp chỉ khác ô khai báo", "60,0 · 78% mức tăng thuộc nhánh so sánh học có giám sát"], h: 0.66, fs: 11, rule: true },
  { cells: [{ t: "Thưởng ô toạ độ (chặng ba)", bold: true }, "học tăng cường, thưởng khi toạ độ khai báo trúng phần tử", "60,1 · AitW 77,3 · D.3 67,0; mức hơn S1 đến từ bước S1 gọi sai loại thao tác"], h: 0.78, fs: 11, rule: true },
  { cells: [{ t: "Chọn trong danh sách ứng viên", bold: true }, "chọn phần tử trong danh sách lấy từ chính màn hình", "56,1 · chọn đúng 71,4% khi đưa ra lựa chọn, nhưng bỏ cuộc quá mức"], h: 0.78, fs: 11, rule: true },
  { cells: [{ t: "Đưa thông tin vị trí vào bộ sinh câu", bold: true }, "bốn cách: mô-đun định vị và cầu nối, vùng cắt làm ảnh thứ hai, tiêm vai trò và vùng, làm nét ảnh quanh đích", "dừng ở tập kiểm định nội bộ: vị trí học được nhưng phần sinh câu bỏ qua"], h: 0.78, fs: 11, rule: true },
  { cells: [{ t: "Mở phần thị giác", bold: true }, "huấn luyện cả các tầng thị giác, mọi thứ khác như S1", "dừng ở 41% số bước, thấp hơn rõ trên tập kiểm định"], h: 0.66, fs: 11 },
], {});
text("Mọi nhánh huấn luyện thêm chỉ có một hạt giống. Các hướng này được trình bày đầy đủ ở Chương 4 và Chương 6, kể cả những hướng không cải thiện.", { x: M, y: 5.85, w: W - 2 * M, h: 0.7, fontSize: 12, italic: true, color: GREY, margin: 0, lh: 1.2 });
note(`- các hướng đều tác động vào một tầng trung gian giữa ảnh và câu
- điểm chung: tầng trung gian thay đổi được, nhưng câu ở đầu ra thay đổi rất ít
- đây là căn cứ cho phương pháp đề xuất ở slide 11`);
foot();

// ══════════ 10 · PHÂN TÍCH LỖI ══════════
slide();
bar("Phân tích lỗi: điểm nghẽn nằm ở tầng tri giác");
block(M, 0.85, 4.4, 3.35);
text("Đích khai báo so với S1, chia theo dòng khai báo", { x: M + 0.2, y: 0.95, w: 4.1, h: 0.55, fontSize: 12.5, bold: true, color: NAVY, margin: 0, lh: 1.15 });
// hai cột âm dương
const ZY = 2.75;
hline(M + 0.4, ZY, 3.6, "6E6890", 1.2);
rect(M + 0.8, ZY - 8.83 * 0.1, 1.1, 8.83 * 0.1, GREEN);
text("+8,83", { x: M + 0.7, y: ZY - 8.83 * 0.1 - 0.32, w: 1.3, h: 0.3, fontSize: 13, bold: true, color: GREEN, align: "center", margin: 0 });
text("khai báo đúng\n(60,6% số bước)", { x: M + 0.5, y: ZY + 0.08, w: 1.7, h: 0.5, fontSize: 10.5, align: "center", margin: 0, lh: 1.05 });
rect(M + 2.5, ZY, 1.1, 11.12 * 0.1, RED);
text("−11,12", { x: M + 2.4, y: ZY + 11.12 * 0.1 + 0.02, w: 1.3, h: 0.3, fontSize: 13, bold: true, color: RED, align: "center", margin: 0 });
text("khai báo sai", { x: M + 2.2, y: ZY - 0.4, w: 1.7, h: 0.3, fontSize: 10.5, align: "center", margin: 0 });
block(5.1, 0.85, 4.4, 3.35);
text("Tách hai kênh", { x: 5.3, y: 0.95, w: 4.0, h: 0.35, fontSize: 12.5, bold: true, color: NAVY, margin: 0 });
bullets([
  [B("91%"), P(" khoảng cách tới câu chuẩn dồn vào "), B("29,9%"), P(" số bước mô hình nhìn sai phần tử ngay từ đầu")],
  [P("trên nhóm ấy, phần thiếu hụt riêng của mô hình là "), B("45,30"), P(" điểm")],
  [P("mức truyền từ tầng tri giác sang điểm câu, đo bằng một can thiệp đã chạy, chỉ "), B("0,028")],
], 5.3, 1.4, 4.0, { fs: 12, gap: 0.9, itemH: 0.88 });
rect(M, 4.5, W - 2 * M, 1.6, "EEEAF6", { radius: 0.06, line: NAVY, lw: 1.5 });
text("Hệ quả cho thiết kế", { x: M + 0.25, y: 4.6, w: 4, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
text("Cơ chế của đích khai báo hoạt động, nhưng bị chặn bởi độ chính xác của chính dòng khai báo. Mọi thay đổi ở tầng trung gian truyền sang câu rất yếu, nên phương pháp đề xuất đặt phần thưởng thẳng lên câu ở đầu ra.", { x: M + 0.25, y: 4.98, w: W - 2 * M - 0.5, h: 1.05, fontSize: 13, margin: 0, lh: 1.22 });
note(`- khai báo đúng thì tốt hơn cả S1, khai báo sai thì kém hẳn
- 91% khoảng cách nằm ở nhóm nhìn sai phần tử
- mức truyền 0,028: dự báo dùng tương quan giữa các nhánh từng sai 26 lần`);
foot();

// ══════════ 11 · PHƯƠNG PHÁP ĐỀ XUẤT ══════════
slide();
bar("Phương pháp đề xuất: học tăng cường thưởng SPICE");
// vòng lặp
box(M, 0.95, 2.3, 0.9, "ảnh + mục tiêu\n+ các bước đã làm + OCR", { fs: 10.5 });
arrow(M + 2.35, 1.4, 0.4);
box(M + 2.8, 0.85, 2.6, 1.1, "S1 đã hoà\n+ LoRA mới (B = 0)\nphần duy nhất được cập nhật", { fs: 10.5, bold: true, fill: "EEEAF6", line: NAVY, lw: 1.6 });
arrow(M + 5.45, 1.4, 0.4);
box(M + 5.9, 0.95, 3.1, 0.9, "8 câu mẫu cho mỗi câu nhắc\ny1, …, y8", { fs: 10.5 });
varrow(M + 7.45, 1.9, 0.5);
box(M + 5.9, 2.45, 3.1, 0.9, "phần thưởng r(yi)\nso với câu chuẩn g", { fs: 10.5 });
arrow(M + 5.9, 2.9, -0.4);
box(M + 2.8, 2.45, 2.6, 0.9, "lợi thế chuẩn hoá\ntrong nhóm 8 câu", { fs: 10.5 });
varrow(M + 4.1, 1.95, 0.48, NAVY, true);
text("cập nhật", { x: M + 4.15, y: 2.0, w: 1.0, h: 0.3, fontSize: 9.5, italic: true, color: NAVY, margin: 0 });
box(M, 2.45, 2.3, 0.9, "S1 đóng băng\n(tham chiếu KL, β = 0,04)", { fs: 10.5, line: "9A94AE" });
arrow(M + 2.35, 2.9, 0.4, "9A94AE");
rect(M, 3.55, W - 2 * M, 0.75, "F6F5F8", { radius: 0.06, line: "9A94AE" });
text("r(s) = SPICE(s, g) − 0,02 · max(0, |s| − |g| − 3)", { x: M, y: 3.55, w: W - 2 * M, h: 0.45, fontSize: 15, fontFace: MONO, color: BLUE, align: "center", valign: "middle", margin: 0 });
text("|·| là số từ; chỉ phạt câu dài hơn câu chuẩn quá ba từ; câu rỗng nhận 0", { x: M, y: 3.95, w: W - 2 * M, h: 0.3, fontSize: 10.5, italic: true, color: GREY, align: "center", margin: 0 });
block(M, 4.45, 4.4, 2.55);
text("Thiết lập", { x: M + 0.2, y: 4.53, w: 4, h: 0.32, fontSize: 13, bold: true, color: NAVY, margin: 0 });
bullets([
  "GRPO, 500 bước, 2 câu nhắc mỗi bước, tức 1.000 câu nhắc gồm mọi loại thao tác",
  "nhiệt độ 1,0, tốc độ học 1e-5, GPU T4 không thu phí",
  "điểm lưu 500 được chấm trên tập kiểm đúng một lần",
], M + 0.2, 4.9, 4.05, { fs: 11.5, gap: 0.7, itemH: 0.68 });
block(5.1, 4.45, 4.4, 2.55);
text("Căn cứ", { x: 5.3, y: 4.53, w: 4, h: 0.32, fontSize: 13, bold: true, color: NAVY, margin: 0 });
bullets([
  "tiền lệ thưởng theo câu trong chú thích ảnh: SCST (CVPR 2017), SPIDEr (ICCV 2017)",
  "trên tập kiểm định, chọn câu SPICE cao nhất trong 9 câu của S1 nâng rõ executability",
  "mô hình định vị không nằm trong phần thưởng, nên thước chấm vẫn độc lập",
], 5.3, 4.9, 4.05, { fs: 11.5, gap: 0.7, itemH: 0.68 });
note(`- xuất phát thẳng từ S1 để phép so chỉ còn một biến là học tăng cường
- LoRA mới với B = 0: bước đầu mô hình trùng S1, tham chiếu KL cũng là S1
- phần đóng góp mới hẹp: áp và đo cho bài toán này, không nhận mới ở thuật toán hay ở việc chọn SPICE`);
foot();

// ══════════ 12 · KẾT QUẢ CHÍNH ══════════
slide();
bar("Kết quả chính trên 4.463 bước chạm của tập kiểm");
imgFit(FIG + "/fig_ba_luat.png", 1480, 720, M, 0.75, W - 2 * M, 4.4);
block(M, 5.3, W - 2 * M, 1.6);
bullets([
  [P("Phương pháp đề xuất đạt executability "), B("60,6"), P(", cao nhất trong mọi mô hình đã đo, và bằng chặng ba dưới luật hộp phần tử (67,0).")],
  [P("Chặng ba cao nhất dưới luật khớp chạm của AitW (77,3). Câu chuẩn: 92,1 · 83,8 · 75,7.")],
], M + 0.2, 5.42, W - 2 * M - 0.4, { fs: 12.5, gap: 0.7, itemH: 0.68 });
note(`- ba luật: AitW (lỏng nhất), hộp phần tử của AndroidControl, executability (chặt nhất)
- mọi số đọc cạnh mức câu chuẩn ở cột cuối
- bảng đủ mọi nhánh, gồm BLEU/ROUGE: dự phòng 2`);
foot();

// ══════════ 13 · NHÓM VỊ TRÍ, ĐỦ NHÁNH ══════════
slide();
bar("Nhóm thước theo vị trí, đủ các nhánh");
{
  const hd = { cells: ["Nhánh", "AitW", "Hộp (D.3)", "Exec.", "±14% trục", "AitW cận trên", "Đúng thao tác"], bold: true, color: WHITE, fill: NAVY, h: 0.5, fs: 11 };
  const r = (c, o) => Object.assign({ cells: c, h: 0.4, fs: 11.5, rule: true }, o || {});
  const bd = (t) => ({ t, bold: true, color: NAVY });
  table(M, 0.8, [2.55, 0.95, 1.05, 0.9, 1.1, 1.3, 1.15], [hd,
    r(["Base", "63,4", "53,6", "47,6", "55,9", "73,4", "96,5"]),
    r(["S1 (hạt 101)", "74,4", "65,5", "59,1", "67,2", "81,0", "94,3"]),
    r(["S1 (hạt 202)", "75,3", "66,1", "59,6", "67,9", "81,9", "94,6"], { rule: "322164", ruleW: 1.5 }),
    r(["S2 (đích khai báo)", "73,4", "63,6", "57,2", "65,7", "80,8", "94,8"]),
    r(["CE2-S2", "76,1", "66,0", "59,4", "68,5", "83,9", bd("98,9")]),
    r(["MIN-DESC", "76,4", "66,5", "60,0", "68,7", "84,4", bd("98,9")]),
    r(["Chặng ba", bd("77,3"), bd("67,0"), "60,1", bd("69,4"), bd("85,0"), bd("98,9")]),
    r(["Nhánh ứng viên", "71,2", "62,4", "56,1", "63,9", "77,9", "90,9"], { rule: "322164", ruleW: 1.5 }),
    r([{ t: "Thưởng SPICE (đề xuất)", bold: true }, "76,2", bd("67,0"), bd("60,6"), "68,9", "82,9", "96,0"]),
    r(["  + TAGE", "76,1", "66,4", "60,2", "68,7", "82,7", "96,6"], { rule: "322164", ruleW: 1.5 }),
    r([{ t: "Câu chuẩn (trần)", italic: true }, "92,1", "83,8", "75,7", "84,2", "96,2", "100,0"], { rule: false }),
  ], { align: ["left", "center", "center", "center", "center", "center", "center"] });
}
text("4.463 bước chạm, tính lại từ bản ghi từng bước, không gọi lại mô hình định vị. Số đậm là cao nhất trong các nhánh mô hình ở cột đó. Ở năm cột vị trí, Base thấp nhất, câu chuẩn cao nhất và S1 hơn Base 11 đến 12 điểm; chặng ba và phương pháp đề xuất đổi chỗ tuỳ luật.", { x: M, y: 6.0, w: W - 2 * M, h: 0.95, fontSize: 11, italic: true, color: GREY, margin: 0, lh: 1.18 });
note(`- AitW: luật trong mã chấm gốc của AndroidInTheWild; cận trên: xét mọi khung bấm được (sàn cao hơn, 41,6)
- D.3: luật gốc của AndroidControl; ±14% theo trục: dung sai đơn thuần
- cột đúng thao tác chỉ tính bước chạm, phải đọc cùng bước không chạm`);
foot();

// ══════════ 14 · NHÓM CÂU CHỮ, ĐỦ NHÁNH ══════════
slide();
bar("Nhóm thước so với câu chuẩn, đủ các nhánh");
{
  const hd = { cells: ["Nhánh", "BLEU-4", "METEOR", "ROUGE-L", "CIDEr-D", "SPICE", "chrF", "BERTScore"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 11 };
  const r = (c, o) => Object.assign({ cells: c, h: 0.4, fs: 11.5, rule: true }, o || {});
  const bd = (t) => ({ t, bold: true, color: NAVY });
  table(M, 0.8, [2.55, 0.9, 0.95, 0.95, 0.95, 0.85, 0.8, 1.05], [hd,
    r(["Base", "15,3", "24,6", "42,3", "88,0", "18,5", "40,2", "40,1"]),
    r(["S1 (hạt 101)", "51,6", "36,8", "67,3", "416,1", "44,4", "61,3", "66,3"]),
    r(["S1 (hạt 202)", "51,7", "37,2", "67,7", "419,2", "44,2", "61,9", "66,8"], { rule: "322164", ruleW: 1.5 }),
    r(["S2 (đích khai báo)", "48,7", "35,8", "66,0", "387,7", "41,3", "59,9", "65,1"]),
    r(["CE2-S2", "50,1", "37,3", bd("68,6"), "402,2", "42,3", "61,9", "66,8"]),
    r(["MIN-DESC", "49,9", "37,3", "68,5", "401,0", "42,2", "61,8", "66,7"]),
    r(["Chặng ba", "49,9", "37,3", "68,5", "402,9", "42,5", "61,9", "66,8"]),
    r(["Nhánh ứng viên", "46,9", "34,2", "63,3", "370,6", "39,3", "57,7", "62,8"], { rule: "322164", ruleW: 1.5 }),
    r([{ t: "Thưởng SPICE (đề xuất)", bold: true }, bd("52,4"), bd("37,9"), "68,4", bd("430,1"), bd("45,8"), bd("62,9"), bd("67,1")]),
    r(["  + TAGE", "-", "-", "-", "-", "45,7", "-", "-"], { rule: "322164", ruleW: 1.5 }),
    r([{ t: "Câu chuẩn", italic: true }, "100,0", "100,0", "100,0", "988,7", "98,6", "100,0", "100,0"], { rule: false }),
  ], { align: ["left", "center", "center", "center", "center", "center", "center", "center"] });
}
text("BLEU-4, METEOR, ROUGE-L, CIDEr-D, SPICE: bộ chấm COCO Captions, mức kho. chrF: sacreBLEU. BERTScore: F1 roberta-large, đã hiệu chỉnh. Một câu chuẩn mỗi bước nên CIDEr-D vượt 100 và chỉ so được giữa các hàng. Đây là các thước mà Widget Captioning và Screen2Words báo.", { x: M, y: 5.95, w: W - 2 * M, h: 1.0, fontSize: 11, italic: true, color: GREY, margin: 0, lh: 1.18 });
note(`- phương pháp đề xuất cao nhất ở 6/7 cột, ROUGE-L kém CE2-S2 0,2
- nhóm thước này xếp S1 trên MIN-DESC và chặng ba, ngược chiều executability; phép so vẫn đọc trên executability
- SPICE: thước Zhao (EACL 2021) khuyên dùng để xếp hạng hệ thống`);
foot();

// ══════════ 15 · PHÂN RÃ EXECUTABILITY ══════════
slide();
bar("Phân rã executability theo từng điều kiện");
{
  const hd = { cells: ["Nhánh", "Executable", "Chỉ ô Voronoi", "Khớp thao tác", "Cửa sổ dung sai"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 11.5 };
  const r = (c, o) => Object.assign({ cells: c, h: 0.4, fs: 12, rule: true }, o || {});
  table(M, 0.8, [3.0, 1.45, 1.55, 1.5, 1.5], [hd,
    r([{ t: "Câu chuẩn (trần)", italic: true }, "75,7", "75,8", "100,0", "84,3"], { rule: "322164", ruleW: 1.5 }),
    r([{ t: "Thưởng SPICE (đề xuất)", bold: true }, { t: "60,6", bold: true }, "61,4", "96,0", "70,3"]),
    r(["  + TAGE", "60,2", "61,0", "96,6", "70,1"]),
    r(["Chặng ba", "60,1", "60,5", "98,9", "69,9"]),
    r(["MIN-DESC", "60,0", "60,4", "98,9", "69,2"]),
    r(["S1 (hạt 202)", "59,6", "60,7", "94,6", "69,8"]),
    r(["CE2-S2", "59,4", "59,8", "98,9", "68,9"]),
    r(["S1 (hạt 101)", "59,1", "60,2", "94,4", "69,2"]),
    r(["S2 (hạt 101)", "57,2", "58,1", "94,8", "67,4"]),
    r(["Nhánh ứng viên", "56,1", "57,4", "90,9", "66,3"]),
    r(["Base", "47,6", "48,9", "96,5", "57,6"], { rule: false }),
  ], { align: ["left", "center", "center", "center", "center"] });
}
text("Executable đòi cả ba điều kiện. Chỉ ô Voronoi bỏ điều kiện loại thao tác. Cửa sổ dung sai là luật ±14% theo trục khi chưa xét loại thao tác. Khoảng cách tới trần nằm chủ yếu ở cột Voronoi, tức ở việc trỏ đúng phần tử.", { x: M, y: 5.75, w: W - 2 * M, h: 1.1, fontSize: 11.5, italic: true, color: GREY, margin: 0, lh: 1.18 });
note(`- khớp thao tác của mọi nhánh đã ở 94 đến 99 trên bước chạm
- vì thế executability gần như bằng cột Voronoi; điểm nghẽn là định vị phần tử`);
foot();

// ══════════ 16 · KIỂM CHÉO BẰNG DỤNG CỤ KHÁC ══════════
slide();
bar("Thước kiểm chéo bằng dụng cụ khác");
block(M, 0.8, 4.4, 5.3);
text("Người nghe trắc nghiệm Phi-4 (ngoài họ Qwen)", { x: M + 0.15, y: 0.88, w: 4.1, h: 0.55, fontSize: 12.5, bold: true, color: NAVY, margin: 0, lh: 1.1 });
text("Mọi phần tử bấm được được đánh số lên ảnh; người nghe chỉ nhận một câu, chọn số ô cần chạm.", { x: M + 0.15, y: 1.45, w: 4.1, h: 0.65, fontSize: 10.5, color: GREY, margin: 0, lh: 1.15 });
table(M + 0.1, 2.15, [2.35, 0.75, 1.1], [
  { cells: ["Câu đưa vào", "Đúng", "KTC 95%"], bold: true, color: WHITE, fill: NAVY, h: 0.36, fs: 10.5 },
  { cells: ["Câu chuẩn", "54,9", "[53,1; 56,8]"], h: 0.36, fs: 10.5, rule: true },
  { cells: ["Chặng ba", "45,8", "[44,1; 47,5]"], h: 0.36, fs: 10.5, rule: true },
  { cells: ["S1 (hạt 101)", "44,6", "[42,9; 46,4]"], h: 0.36, fs: 10.5, rule: true },
  { cells: ["Base (3.566 bước)", "38,6", "[36,7; 40,4]"], h: 0.36, fs: 10.5, rule: true },
  { cells: ["“Tap the button.”", "15,9", "[14,7; 17,0]"], h: 0.36, fs: 10.5, rule: true },
  { cells: ["Đoán ngẫu nhiên", "10,1", ""], h: 0.36, fs: 10.5 },
], { align: ["left", "center", "center"] });
text("Thứ tự giữ nguyên; chặng ba − S1 = +1,14 [+0,23; +2,10].", { x: M + 0.15, y: 4.85, w: 4.1, h: 0.6, fontSize: 11, margin: 0, lh: 1.15 });
text("κ với UGround 0,25 đến 0,44: sai ở bước khác nhau mà vẫn cùng thứ tự.", { x: M + 0.15, y: 5.4, w: 4.1, h: 0.6, fontSize: 11, margin: 0, lh: 1.15 });
block(5.1, 0.8, 4.4, 5.3);
text("Mô hình định vị thứ hai: UI-Venus-Ground-7B (không học AndroidControl)", { x: 5.25, y: 0.88, w: 4.1, h: 0.55, fontSize: 12.5, bold: true, color: NAVY, margin: 0, lh: 1.1 });
text("Chấm lại 2.532 bước mà các nhánh viết câu khác nhau.", { x: 5.25, y: 1.45, w: 4.1, h: 0.4, fontSize: 10.5, color: GREY, margin: 0 });
table(5.2, 2.15, [1.6, 1.3, 1.3], [
  { cells: ["Nhánh", "UGround", "UI-Venus"], bold: true, color: WHITE, fill: NAVY, h: 0.36, fs: 10.5 },
  { cells: ["Base", "42,5", "39,1"], h: 0.36, fs: 10.5, rule: true },
  { cells: ["S1", "52,8", "48,7"], h: 0.36, fs: 10.5, rule: true },
  { cells: ["S2", "49,5", "46,6"], h: 0.36, fs: 10.5, rule: true },
  { cells: ["Trần trên mẫu", "70,0", "69,3"], h: 0.36, fs: 10.5 },
], { align: ["left", "center", "center"] });
table(5.2, 4.1, [1.6, 1.3, 1.3], [
  { cells: ["Phép so", "UGround", "UI-Venus"], bold: true, color: WHITE, fill: NAVY, h: 0.36, fs: 10.5 },
  { cells: ["S1 − Base", "+10,35", "+9,68"], h: 0.36, fs: 10.5, rule: true },
  { cells: ["S2 − S1", "−1,93", "−1,21"], h: 0.36, fs: 10.5 },
], { align: ["left", "center", "center"] });
text("Chênh lệch S1 − Base giữ 94%; S2 − S1 giữ dấu âm.", { x: 5.25, y: 5.3, w: 4.1, h: 0.6, fontSize: 11, margin: 0, lh: 1.15 });
text("Thang của người nghe hẹp hơn (câu chuẩn chỉ 54,9) nên chỉ dùng để kiểm thứ tự và hướng của phép so, không làm số chính.", { x: M, y: 6.25, w: W - 2 * M, h: 0.7, fontSize: 11, italic: true, color: GREY, margin: 0, lh: 1.15 });
note(`- hai dụng cụ độc lập với UGround, đều giữ thứ tự các nhánh
- UI-Venus chấm thấp hơn ở mọi nhánh, nên không phải chọn dụng cụ để có số đẹp
- phương pháp đề xuất chưa được chấm bằng hai dụng cụ này`);
foot();

// ══════════ 17 · MƯỜI BA THƯỚC ══════════
slide();
bar("Mười ba thước dùng để so phương pháp đề xuất với S1");
{
  const G = (t) => ({ span: t, fs: 11, h: 0.3, fill: "F1EFF6" });
  const R = (a, b, c, d, e, f, o) => Object.assign({ cells: [a, { t: b, fs: 9.5, color: GREY }, c, d, { t: e, color: GREEN, bold: true }, { t: f, fs: 9.5 }], h: 0.36, fs: 10.5, rule: true }, o || {});
  table(0.3, 0.72, [1.75, 3.95, 0.75, 0.8, 0.7, 1.45], [
    { cells: ["Thước", "Đo gì", "S1", "Đề xuất", "Δ", "KTC 95%"], bold: true, color: WHITE, fill: NAVY, h: 0.36, fs: 11 },
    G("Theo vị trí, chấm bằng mô hình định vị đọc câu"),
    R({ t: "Executability", bold: true }, "đúng loại thao tác, trong dung sai 0,14, trong ô Voronoi", "59,11", "60,65", "+1,55", "[+0,80; +2,33]"),
    R("Hộp phần tử (D.3)", "điểm trỏ nằm trong hộp phần tử cần chạm", "65,49", "67,02", "+1,52", "[+0,77; +2,29]"),
    R("Khớp chạm AitW", "cách ≤ 0,14 hoặc cùng trong hộp nới 1,4 lần (AitW)", "74,37", "76,25", "+1,88", "[+1,17; +2,63]"),
    R("AitW cận trên", "như trên, xét mọi khung phần tử bấm được trên màn", "81,04", "82,90", "+1,86", "[+1,17; +2,60]"),
    R("±14% theo trục", "lệch ≤ 0,14 bề rộng và ≤ 0,14 bề cao, đúng loại thao tác", "67,24", "68,90", "+1,66", "[+0,90; +2,46]"),
    R("Đúng loại thao tác", "câu quy về đúng loại thao tác của bước", "94,35", "95,97", "+1,61", "[+1,17; +2,08]", { rule: false }),
    G("Theo câu chữ, so với câu chuẩn (bộ chấm COCO, mức kho)"),
    R("SPICE", "khớp đồ thị ngữ nghĩa: đối tượng, thuộc tính, quan hệ", "44,37", "45,79", "+1,42", "[+0,69; +2,16]"),
    R("BLEU-4", "độ chính xác cụm 1 đến 4 từ", "51,56", "52,36", "+0,80", ""),
    R("METEOR", "khớp từ có tính gốc từ và đồng nghĩa", "36,79", "37,92", "+1,13", ""),
    R("ROUGE-L", "chuỗi con chung dài nhất, F1", "67,35", "68,36", "+1,01", ""),
    R("CIDEr-D", "cụm từ có trọng số TF-IDF theo độ hiếm của cụm", "416,12", "430,05", "+13,93", ""),
    R("chrF", "F-score trên cụm ký tự", "61,26", "62,87", "+1,61", ""),
    R("BERTScore", "tương đồng biểu diễn ngữ cảnh (roberta-large)", "66,33", "67,07", "+0,74", "", { rule: false }),
  ], { align: ["left", "left", "center", "center", "center", "center"] });
}
text("4.463 bước chạm, ghép cặp theo bước, KTC bootstrap theo cụm tác vụ. BLEU-4 ở đây là mức kho, khác BLEU-4 trung bình mức câu ở dự phòng 2.", { x: 0.3, y: 6.55, w: 9.4, h: 0.55, fontSize: 10.5, italic: true, color: GREY, margin: 0, lh: 1.15 });
note(`- sáu thước vị trí và bảy thước câu chữ, đều cao hơn S1
- sáu thước vị trí có KTC nằm hẳn trên 0; mô hình định vị không có trong phần thưởng
- phần thưởng là SPICE nhưng mức tăng không dừng ở SPICE`);
foot();

// ══════════ 18 · SO VỚI S1 ══════════
slide();
bar("Nguồn của mức tăng so với S1");
block(M, 0.85, 5.6, 6.05);
bullets([
  [P("Executability "), B("+1,55"), P(" điểm, p = 1,6 × 10⁻⁵; so với S1 hạt 202 vẫn hơn "), B("1,03"), P(" điểm (p = 0,014).")],
  [P("Cứu 159 bước, phá 90 bước.")],
  [P("Tính ròng, "), B("41"), P(" bước là đổi sang đúng phần tử ở những bước cả hai cùng đúng loại thao tác, tức định vị thật; "), B("28"), P(" bước là sửa loại thao tác.")],
  [P("Câu gần như giữ độ dài (7,83 → 7,96 từ); 2.795/4.463 câu trùng S1 từng ký tự.")],
  [P("Khác chặng ba, vốn có toàn bộ mức hơn S1 ở các bước S1 gọi sai loại thao tác.")],
], M + 0.2, 1.05, 5.2, { fs: 12.5, gap: 1.0, itemH: 0.95 });
imgFit(FIG + "/fig_vidu_spice.png", 1500, 1660, 6.25, 0.8, 3.3, 6.1);
note(`- mô hình đầu tiên của đề tài hơn S1 có ý nghĩa thống kê ngay dưới executability
- hơn một nửa mức tăng là định vị thật, khác chặng ba
- ví dụ bên phải: S1 gọi nút Allow, phương pháp đề xuất gọi đúng Not Now ở cuối màn`);
foot();

// ══════════ 14 · TÁC DỤNG PHỤ ══════════
slide();
bar("Tác dụng phụ đo được ở bước không chạm");
imgFit(FIG + "/fig_khongcham.png", 1320, 580, M, 0.75, W - 2 * M, 3.95);
block(M, 4.85, W - 2 * M, 2.05);
bullets([
  [P("Trên 2.495 bước không chạm, tỉ lệ gọi đúng loại thao tác giảm 1,68 điểm; dồn vào bước cuộn ("), C("−6,23", RED), P(") và quay lại ("), C("−5,93", RED), P(").")],
  [P("Cơ chế: mô hình nghiêng về câu chạm. Trong 51 bước cuộn bị phá, 47 bước câu đổi từ “Swipe up” sang “Click on …”.")],
  [P("Đã loại cách giải thích SPICE không phân biệt câu cuộn ngắn. Cách sửa trực tiếp: thêm số hạng đúng loại thao tác vào phần thưởng.")],
], M + 0.2, 4.97, W - 2 * M - 0.4, { fs: 12, gap: 0.64, itemH: 0.62 });
note(`- đây là cái giá của phương pháp, báo cạnh mọi số trên bước chạm
- cùng một cơ chế cho cả phần được (sửa swipe thành click ở bước chạm) và phần mất
- tính trên toàn 6.958 bước: được 72 bước ở bước chạm, mất 42 bước ở bước không chạm`);
foot();

// ══════════ 15 · TAGE ══════════
slide();
bar("Mở rộng: bộ sửa câu theo vùng cắt quanh phần tử (TAGE)");
const TG = ["câu nháp\ncủa phương pháp\nđề xuất", "bộ định vị\nđoán điểm\ncần chạm", "cắt vùng\n40% bề ngang\nquanh điểm", "bộ biên tập\nLoRA\nviết lại câu", "bộ chọn\ngiữ câu nháp\nhay câu sửa"];
TG.forEach((t, i) => {
  const x = M + i * 1.86;
  box(x, 0.9, 1.6, 1.1, t, { fs: 10.5, fill: i === 3 ? "EEEAF6" : WHITE, line: i === 3 ? NAVY : "6E6890" });
  if (i < 4) arrow(x + 1.62, 1.45, 0.22);
});
table(M, 2.35, [3.0, 1.2, 1.2, 1.2, 2.4], [
  { cells: ["Thước", "S1", "Câu nháp", "TAGE", "TAGE − câu nháp"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 11.5 },
  { cells: ["Executability", "59,11", "60,65", "60,23", { t: "−0,43 [−0,87; +0,02]", color: RED }], h: 0.38, fs: 11.5, rule: true },
  { cells: ["Hộp phần tử (D.3)", "65,49", "67,02", "66,44", { t: "−0,58 [−1,07; −0,09]", color: RED }], h: 0.38, fs: 11.5, rule: true },
  { cells: ["Đúng loại thao tác", "94,35", "95,97", "96,64", { t: "+0,67 [+0,44; +0,92]", color: GREEN }], h: 0.38, fs: 11.5 },
], { align: ["left", "center", "center", "center", "center"] });
block(M, 4.15, W - 2 * M, 2.75);
bullets([
  "Trên tập kiểm định, bộ biên tập đọc vùng cắt thật: vùng cắt đúng chỗ nâng câu rõ rệt, vùng cắt lệch sang phần tử lân cận làm câu kém đi.",
  "Trên tập kiểm, bộ chọn dựa trên xác suất của chính bộ biên tập nhận câu sửa đúng ở những bước vùng cắt sai: chỉ 36,5% vùng cắt đúng chỗ trong nhóm được nhận, so với 67,7% đến 74,0% ở các nhóm không được nhận.",
  "Hướng tiếp theo là một bộ chọn độc lập với vùng cắt.",
], M + 0.2, 4.27, W - 2 * M - 0.4, { fs: 12, gap: 0.8, itemH: 0.78 });
note(`- TAGE trình bày là phần mở rộng, không phải đóng góp chính
- kết quả âm nhỏ nhưng có lý do đo được: bộ chọn chọn ngược
- giá trị chọn trên 11 câu của tập kiểm định không chuyển sang tập kiểm`);
foot();

// ══════════ 16 · ĐÓNG GÓP ══════════
slide();
bar("Đóng góp của luận văn");
const DG = [
  ["1", "Thước đo", "Executability: chấm câu bằng một người nghe độc lập, không cần câu chuẩn làm đáp án. Sai số dụng cụ, trần 75,7 và sàn 12,0 / 6,1 đều được đo trực tiếp; thứ tự các hệ thống giữ nguyên qua năm luật, một mô hình định vị thứ hai và một người nghe ngoài họ Qwen."],
  ["2", "Dữ liệu và phương pháp", "Tập 64.567 bước dựng hoàn toàn tự động từ AndroidControl. Học tăng cường thưởng SPICE đưa executability từ 59,1 lên 60,6 (+1,55, p < 0,001), tăng ở cả 13 thước, kèm tác dụng phụ ở bước cuộn đã đo."],
  ["3", "Phân tích lỗi qua các hướng đã thử", "Điểm nghẽn nằm ở tầng tri giác: 91% khoảng cách tới câu chuẩn ở 29,9% số bước nhìn sai phần tử, mức truyền sang câu chỉ 0,028, thông tin vị trí gắn thêm bị phần sinh câu bỏ qua. Đây là căn cứ để đặt phần thưởng lên câu."],
];
DG.forEach((d, i) => {
  const yy = 0.85 + i * 2.0;
  block(M, yy, W - 2 * M, 1.8);
  rect(M, yy, 0.65, 1.8, NAVY, { radius: 0.06 });
  text(d[0], { x: M, y: yy, w: 0.65, h: 1.8, fontSize: 24, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text(d[1], { x: M + 0.85, y: yy + 0.1, w: 7.9, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
  text(d[2], { x: M + 0.85, y: yy + 0.48, w: 8.0, h: 1.25, fontSize: 12, margin: 0, lh: 1.2 });
});
note(`- ba đóng góp độc lập về lập luận
- thước đo là phần đầu tư nhiều nhất
- phương pháp: điểm mới hẹp, ở chỗ áp và đo cho bài toán sinh câu hướng dẫn giao diện`);
foot();

// ══════════ 17 · HẠN CHẾ ══════════
slide();
bar("Hạn chế");
block(M, 0.85, 4.4, 5.95);
text("Về dụng cụ đo", { x: M + 0.2, y: 0.95, w: 4, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Hai mô hình định vị cùng họ Qwen-VL với mô hình được chấm; người nghe Phi-4 ngoài họ mới chấm bốn nhánh.",
  "Mới kiểm độ bền khi đổi động từ và trật tự câu, chưa kiểm khi viết lại tên gọi phần tử.",
  "Thước đo người nghe là mô hình; mức đồng thuận với người thật chưa được đo.",
  "Phần lớn tác vụ của tập kiểm thuộc phần huấn luyện chính thức của AndroidControl; tách điểm theo phần chia không thấy chênh lệch.",
], M + 0.2, 1.4, 4.05, { fs: 11.5, gap: 1.2, itemH: 1.15 });
block(5.1, 0.85, 4.4, 5.95);
text("Về kết quả mô hình", { x: 5.3, y: 0.95, w: 4, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Mọi nhánh huấn luyện thêm chỉ có một hạt giống.",
  "Chưa có nhánh so sánh học có giám sát thêm cùng số bước cho phương pháp đề xuất.",
  "Đường sinh câu của phương pháp đề xuất khác S1 công bố; một phần nhỏ chênh lệch có thể đến từ đó.",
  "Tác dụng phụ ở bước cuộn và quay lại chưa được sửa.",
], 5.3, 1.4, 4.05, { fs: 11.5, gap: 1.2, itemH: 1.15 });
note(`- mọi hạn chế đều đã viết trong ch7 kèm số đo
- hạt giống thứ hai bị cắt vì ngân sách máy`);
foot();

// ══════════ 18 · HƯỚNG PHÁT TRIỂN ══════════
slide();
bar("Hướng phát triển");
const HP = [
  ["Hoàn tất đánh giá phương pháp đề xuất", "hạt giống thứ hai, nhánh so sánh cùng số bước, sinh lại S1 qua cùng đường sinh; thêm số hạng đúng loại thao tác vào phần thưởng"],
  ["Bộ chọn độc lập với vùng cắt cho TAGE", "so điểm định vị theo câu nháp với điểm của bộ định vị, chọn trên toàn tập kiểm định"],
  ["Học kênh vị trí cùng lúc với phần sinh câu", "thay vì gắn vào một bộ sinh câu đã học xong"],
  ["Nối thước với đánh giá của người", "hai người chấm 100 câu, đo mức đồng thuận với executability"],
  ["Mở rộng phạm vi", "phần kiểm chính thức của AndroidControl, chuỗi nhiều màn, giao diện tiếng Việt, bộ dữ liệu thứ hai"],
];
HP.forEach((h, i) => {
  const yy = 0.85 + i * 1.18;
  block(M, yy, W - 2 * M, 1.02);
  text(String(i + 1), { x: M + 0.1, y: yy, w: 0.5, h: 1.02, fontSize: 20, bold: true, color: TEAL, align: "center", valign: "middle", margin: 0 });
  text(h[0], { x: M + 0.75, y: yy + 0.1, w: 8.1, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
  text(h[1], { x: M + 0.75, y: yy + 0.46, w: 8.1, h: 0.52, fontSize: 11.5, margin: 0, lh: 1.15 });
});
note(`- xếp theo mức cần thiết với độ tin cậy của kết luận
- hai hướng đầu nối tiếp phương pháp đề xuất`);
foot();

// ══════════ 19 · TÌNH TRẠNG ══════════
slide();
bar("Tình trạng luận văn và các bài báo");
block(M, 0.85, 4.4, 4.0);
text("Bản luận văn", { x: M + 0.2, y: 0.95, w: 4, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
table(M + 0.15, 1.4, [0.7, 3.25], [
  { cells: ["Ch. 1", "Giới thiệu"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["Ch. 2", "Tổng quan"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["Ch. 3", "Xây dựng bộ dữ liệu"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["Ch. 4", "Phương pháp tiếp cận"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["Ch. 5", "Thước đo executability"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["Ch. 6", "Thực nghiệm và kết quả"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["Ch. 7", "Kết luận"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["Ch. 8", "Các công trình nghiên cứu"], h: 0.36, fs: 11.5 },
], {});
text("153 trang, đã dựng bản PDF đầy đủ", { x: M + 0.2, y: 4.35, w: 4, h: 0.35, fontSize: 12, bold: true, color: TEAL, margin: 0 });
block(5.1, 0.85, 4.4, 4.0);
text("Bài báo tách từ luận văn", { x: 5.3, y: 0.95, w: 4, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
const BB = [
  ["FAIR 2026", "tiếng Anh, mẫu IEEE · phần mô hình · gửi 31/8/2026"],
  ["VCL 2026", "tiếng Việt · nhãn quy chiếu và quy trình dựng dữ liệu · nộp 30/8/2026"],
  ["SOICT 2026", "tiếng Anh, Springer · tách điều kiện loại thao tác khỏi phần định vị · nộp 21/9/2026"],
];
BB.forEach((b, i) => {
  const yy = 1.45 + i * 1.08;
  text(b[0], { x: 5.3, y: yy, w: 4, h: 0.32, fontSize: 12.5, bold: true, color: TEAL, margin: 0 });
  text(b[1], { x: 5.3, y: yy + 0.32, w: 4.05, h: 0.68, fontSize: 11, margin: 0, lh: 1.15 });
});
rect(M, 5.1, W - 2 * M, 1.75, "EEEAF6", { radius: 0.06, line: NAVY, lw: 1.5 });
text("Đang chạy thêm, chưa đưa vào luận văn", { x: M + 0.25, y: 5.2, w: 6, h: 0.35, fontSize: 13, bold: true, color: NAVY, margin: 0 });
bullets([
  "Học tiếp phương pháp đề xuất với phần thưởng có thêm người nghe Phi-4: trên tập kiểm định chưa nhánh nào vượt rõ điểm lưu 500.",
  "Chấm trên tập kiểm nhánh thưởng CIDEr-D cùng thiết lập, để so trực tiếp hai lựa chọn phần thưởng.",
], M + 0.25, 5.6, W - 2 * M - 0.5, { fs: 11.5, gap: 0.6, itemH: 0.58 });
note(`- luận văn đã đủ chương, số trên slide khớp bản PDF
- các lượt đang chạy chỉ bổ sung; nếu không vượt thì mô hình chính giữ nguyên`);
foot();

// ══════════ DỰ PHÒNG 1 · LUẬT TRÚNG ══════════
slide();
bar("Dự phòng: lý do dùng ô Voronoi thay cho dung sai đơn thuần");
block(M, 0.85, W - 2 * M, 2.4);
text("Đưa vào một câu gọi đúng loại phần tử nhưng sai nút (nút cạnh bên)", { x: M + 0.2, y: 0.95, w: 8.5, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
rect(M + 0.4, 1.55, 84.3 * 0.085, 0.5, ORANGE);
text("84,3%", { x: M + 0.45 + 84.3 * 0.085, y: 1.55, w: 1.0, h: 0.5, fontSize: 14, bold: true, color: ORANGE, valign: "middle", margin: 0 });
text("luật dung sai quy ước vẫn cho điểm", { x: M + 0.5, y: 1.55, w: 6, h: 0.5, fontSize: 11.5, bold: true, color: WHITE, valign: "middle", margin: 0 });
rect(M + 0.4, 2.25, 2.8 * 0.085 + 0.02, 0.5, NAVY);
text("2,8%   luật ô Voronoi cho điểm", { x: M + 0.75, y: 2.25, w: 6, h: 0.5, fontSize: 12, bold: true, color: NAVY, valign: "middle", margin: 0 });
bullets([
  "Luật trúng được chọn dựa trên sàn đo được: luật nào chấp nhận nhiều câu chỉ sai nút thì bị loại.",
  "Voronoi là bản siết chặt của luật dung sai: điểm phải nằm trong dung sai và gần điểm chạm hơn mọi phần tử khác.",
  "Luật hộp phần tử của AndroidControl (D.3) và luật khớp chạm của AitW được báo kèm, thứ tự các hệ thống không đổi.",
], M + 0.2, 3.55, W - 2 * M - 0.4, { fs: 12.5, gap: 0.85, itemH: 0.8 });
footB();

// ══════════ DỰ PHÒNG 2 · BẢNG ĐỦ ══════════
slide();
bar("Dự phòng: bảng kết quả đủ các nhánh");
table(M, 0.8, [3.3, 0.85, 1.35, 0.8, 0.8, 0.95, 0.95], [
  { cells: ["Nhánh", "Exec.", "KTC 95%", "D.3", "AitW", "BLEU-4", "ROUGE-L"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 11 },
  { cells: ["Base (chưa tinh chỉnh)", "47,6", "[45,9; 49,3]", "53,6", "63,4", "9,9", "40,4"], h: 0.38, fs: 11, rule: true },
  { cells: ["S1 (hạt giống 101)", "59,1", "[57,3; 60,8]", "65,5", "74,4", "38,7", "67,3"], h: 0.38, fs: 11, rule: true },
  { cells: ["S1 (hạt giống 202)", "59,6", "[57,9; 61,3]", "66,1", "75,3", "39,0", "67,6"], h: 0.38, fs: 11, rule: "322164", ruleW: 1.5 },
  { cells: ["S2 (đích khai báo)", "57,2", "[55,4; 58,9]", "63,6", "73,4", "36,4", "65,9"], h: 0.38, fs: 11, rule: true },
  { cells: ["CE2-S2 (nhánh so sánh)", "59,4", "[57,7; 61,1]", "66,0", "76,1", "38,1", "68,6"], h: 0.38, fs: 11, rule: true },
  { cells: ["MIN-DESC (mục tiêu ưu tiên)", "60,0", "[58,3; 61,8]", "66,5", "76,4", "37,9", "68,4"], h: 0.38, fs: 11, rule: true },
  { cells: ["Chặng ba (thưởng ô toạ độ)", "60,1", "[58,3; 61,8]", "67,0", "77,3", "37,8", "68,5"], h: 0.38, fs: 11, rule: true },
  { cells: ["Nhánh ứng viên", "56,1", "[54,2; 58,0]", "62,4", "71,2", "34,5", "63,0"], h: 0.38, fs: 11, rule: "322164", ruleW: 1.5 },
  { cells: [{ t: "Thưởng SPICE (đề xuất)", bold: true }, { t: "60,6", bold: true }, "[58,9; 62,4]", "67,0", "76,2", "40,1", "68,3"], h: 0.38, fs: 11, rule: true },
  { cells: ["  + TAGE (sửa câu)", "60,2", "[58,5; 62,0]", "66,4", "76,1", "40,1", "68,4"], h: 0.38, fs: 11, rule: "322164", ruleW: 1.5 },
  { cells: [{ t: "Câu chuẩn (trần)", italic: true }, "75,7", "[74,1; 77,3]", "83,8", "92,1", "96,1", "100,0"], h: 0.38, fs: 11 },
], { align: ["left", "center", "center", "center", "center", "center", "center"] });
text("4.463 bước chạm. BLEU-4 trung bình mức câu. Mọi nhánh trừ S1 chỉ có một hạt giống. Nhánh ứng viên lệch ba biến so với các nhánh khác nên chỉ so được với Base.", { x: M, y: 5.6, w: W - 2 * M, h: 0.9, fontSize: 11.5, italic: true, color: GREY, margin: 0, lh: 1.2 });
footB();

// ---- xuất ----
done();
pres.writeFile({ fileName: "../LUAN_VAN_SLIDE.pptx" }).then(function () {
  var html = '<!doctype html><meta charset="utf-8"><title>Preview - trinh thay</title>'
    + '<style>@page{size:960px 720px;margin:0}body{margin:0;font-family:sans-serif}'
    + '.slide{position:relative;width:960px;height:720px;overflow:hidden;page-break-after:always}</style>'
    + htmlSlides.join("\n");
  fs.mkdirSync("_preview", { recursive: true });
  fs.writeFileSync("_preview/preview.html", html);
  console.log("Xong: ../LUAN_VAN_SLIDE.pptx  |  slide chinh: " + PAGE + "  |  du phong: " + BPAGE);
});
