// Deck HỘI NGHỊ VCL2026 - 17 slide chính + 8 slide dự phòng, nhắm 15 phút.
// Style giữ đúng deck luận văn (build_baove.js): khổ 4:3, thanh tiêu đề chàm,
// khối xám bo góc, chữ serif, footline 4 ô.
// Nội dung lấy TỪ paper/vcl2026/main.tex (bản nộp 30/8/2026), không thêm số nào ngoài bài.
// Xuất: ../VCL2026_SLIDE.pptx
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.defineLayout({ name: "A43", width: 10, height: 7.5 });
pres.layout = "A43";
pres.author = "Le Doan Phuong Uyen";
pres.title = "Xay dung ngu lieu quy chieu tu dong cho phan tu giao dien - VCL2026";

const TF = "Cambria", MONO = "Consolas";
const NAVY = "322164", INK = "1A1A1A";
const FOOTA = "191132", FOOTB = "25194B", FOOTC = "4F417A", FOOTD = "7A7099";
const BLOCK = "E9E8EC", TEAL = "006666", BLUE = "1414BE", RED = "B22222", MAROON = "990000";
const GREY = "5A5A66", WHITE = "FFFFFF";
const W = 10, H = 7.5, M = 0.55;

const PX = 96;
const FMAP = { "Cambria": "'DejaVu Serif',Georgia,serif", "Consolas": "'DejaVu Sans Mono',monospace" };
let htmlSlides = [], cur = "";
function esc(t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function plain(c) { return typeof c === "string" ? c : c.map(r => r.text).join(""); }
function hpush(html) { cur += html; }
let s, PAGE = 0, BPAGE = 0, TOTAL = 17;
function slide() { if (cur) htmlSlides.push(cur + "</div>"); s = pres.addSlide(); s.background = { color: WHITE }; cur = `<div class="slide" style="background:#fff">`; }
function done() { if (cur) { htmlSlides.push(cur + "</div>"); cur = ""; } }
function text(content, o) {
  const opt = Object.assign({ x: 0, y: 0, w: 4, h: 1, fontSize: 13, color: INK, fontFace: TF, align: "left", valign: "top", margin: o.margin != null ? o.margin : 4 }, o);
  if (o.lh) opt.lineSpacingMultiple = o.lh;
  s.addText(content, opt);
  const jc = opt.align === "center" ? "center" : opt.align === "right" ? "flex-end" : "flex-start";
  const ai = opt.valign === "middle" ? "center" : opt.valign === "bottom" ? "flex-end" : "flex-start";
  const pad = (opt.margin || 0) / PX;
  const st = `position:absolute;left:${opt.x * PX}px;top:${opt.y * PX}px;width:${opt.w * PX}px;height:${opt.h * PX}px;display:flex;justify-content:${jc};align-items:${ai};padding:${pad}in;box-sizing:border-box;font-family:${FMAP[opt.fontFace] || FMAP[TF]};font-size:${opt.fontSize}px;color:#${opt.color};text-align:${opt.align};line-height:${o.lh || 1.2};` + (opt.bold ? "font-weight:700;" : "") + (opt.italic ? "font-style:italic;" : "");
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
function arrow(x, y, w, c) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || FOOTC, width: 2, endArrowType: "triangle" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX - 1}px;width:${w * PX}px;height:0;border-top:2px solid #${c || FOOTC}"></div>`);
}
function img(path, x, y, w, h) {
  s.addImage({ path, x, y, w, h });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:${w * PX}px;height:${h * PX}px;background:#ddd"></div>`);
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
  text("VCL2026  ·  HUFLIT  ·  27/11/2026", { x: 0, y: yy, w: 3.0, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0, fontFace: MONO });
  text("Xây dựng ngữ liệu quy chiếu tự động cho phần tử giao diện", { x: 3.0, y: yy, w: 3.7, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text("Lê Đoàn Phương Uyên", { x: 6.7, y: yy, w: 1.9, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text(label, { x: 8.6, y: yy, w: 1.4, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
}
function foot() { PAGE++; footRow(`${PAGE}/${TOTAL}`); }
function footB() { BPAGE++; footRow(`dự phòng ${BPAGE}`); }
function block(x, y, w, h) { rect(x, y, w, h, BLOCK, { radius: 0.06, shadow: true }); }

// danh sách gạch đầu dòng, trả về y sau cùng
function bullets(items, x, y, w, o) {
  o = o || {};
  const fs = o.fs || 14, gap = o.gap || 0.62, lh = o.lh || 1.3;
  items.forEach((it, i) => {
    const yy = y + i * gap;
    text("•", { x, y: yy, w: 0.22, h: gap, fontSize: fs, color: o.dot || TEAL, bold: true, margin: 0 });
    text(it, { x: x + 0.25, y: yy, w: w - 0.25, h: o.itemH || gap, fontSize: fs, color: o.color || INK, margin: 0, lh });
  });
  return y + items.length * gap;
}
// bảng tự vẽ: colW là mảng bề rộng, rows là mảng {cells, bold, fill, color, fs, h, rule}
function table(x, y, colW, rows, o) {
  o = o || {};
  const rowH = o.rowH || 0.33, fs = o.fs || 11.5;
  const totalW = colW.reduce((a, b) => a + b, 0);
  let yy = y;
  rows.forEach(r => {
    const h = r.h || rowH;
    if (r.fill) rect(x, yy, totalW, h, r.fill);
    let xx = x;
    r.cells.forEach((c, ci) => {
      const cell = (typeof c === "string" || Array.isArray(c)) ? { t: c } : c;
      text(cell.t, {
        x: xx, y: yy, w: colW[ci], h, fontSize: cell.fs || r.fs || fs,
        bold: cell.bold != null ? cell.bold : r.bold, color: cell.color || r.color || INK,
        align: cell.align || (o.align && o.align[ci]) || "left", valign: "middle", margin: 3
      });
      xx += colW[ci];
    });
    if (r.rule) hline(x, yy + h, totalW, r.rule === true ? "9A94AE" : r.rule, r.ruleW || 1);
    yy += h;
  });
  return yy;
}

const NOTES = require("./notes_vcl.json");
function N(i) { if (NOTES[String(i)]) note(NOTES[String(i)]); }
function NB(k) { if (NOTES[k]) note(NOTES[k]); }


// ══════════ 1 · BÌA ══════════
slide();
rect(0, 0, W, 0.66, NAVY);
text("HỘI THẢO QUỐC GIA LẦN 4 VỀ NGÔN NGỮ HỌC TÍNH TOÁN  -  VCL 2026", { x: 0, y: 0, w: W, h: 0.66, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
rect(0.6, 1.15, W - 1.2, 2.7, NAVY, { radius: 0.09, shadow: true });
text("SINH HƯỚNG DẪN SỬ DỤNG PHẦN MỀM\nTỪ ẢNH CHỤP MÀN HÌNH VÀ MỤC TIÊU NGƯỜI DÙNG", { x: 0.75, y: 1.45, w: W - 1.5, h: 1.1, fontSize: 20, bold: true, color: WHITE, align: "center", margin: 0, lh: 1.25 });
text("Xây dựng ngữ liệu quy chiếu tự động\nkhi phần tử giao diện không có tên cụ thể", { x: 0.75, y: 2.65, w: W - 1.5, h: 1.0, fontSize: 17, color: WHITE, align: "center", margin: 0, lh: 1.3 });
text("Lê Đoàn Phương Uyên   ·   Nguyễn Hồng Bửu Long", { x: 0.6, y: 4.25, w: W - 1.2, h: 0.4, fontSize: 16, bold: true, align: "center", margin: 0 });
text("Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM", { x: 0.6, y: 4.7, w: W - 1.2, h: 0.35, fontSize: 13, color: GREY, align: "center", margin: 0 });
block(2.0, 5.35, 6.0, 0.75);
text("Bộ ngữ liệu GUIRefCorpus  ·  41.099 nhãn dựng hoàn toàn bằng quy tắc", { x: 2.0, y: 5.35, w: 6.0, h: 0.75, fontSize: 13.5, bold: true, color: NAVY, align: "center", valign: "middle", margin: 0 });
N(1); foot(); done();

// ══════════ 2 · NỘI DUNG + BA ĐÓNG GÓP ══════════
slide();
bar("Nội dung trình bày");
block(M, 0.85, W - 2 * M, 0.8);
text([{ text: "Vào:  ", options: { bold: true, color: RED } }, { text: "ảnh màn hình và mục tiêu người dùng.     ", options: { bold: true, color: NAVY } }, { text: "Ra:  ", options: { bold: true, color: RED } }, { text: "một câu đủ để người đọc biết chạm vào đâu.", options: { bold: true, color: NAVY } }], { x: M + 0.25, y: 0.85, w: W - 2 * M - 0.5, h: 0.8, fontSize: 14, valign: "middle", margin: 0 });
["Bài toán quy chiếu trong miền giao diện",
 "Quy trình dựng nhãn tự động cho 41.099 bước",
 "Chiến lược quy chiếu của nhãn và của người chú thích",
 "Kiểm định chất lượng, trong đó có một nguồn ngoài quy trình",
 "Hạn chế và kết luận"].forEach((t, i) => {
  text([{ text: (i + 1) + ".", options: { bold: true, color: TEAL } }, { text: "   " + t, options: { bold: true, color: NAVY } }], { x: 1.35, y: 1.95 + i * 0.6, w: 7.8, h: 0.45, fontSize: 16, margin: 0 });
});
text("Ba đóng góp của bài", { x: M, y: 5.1, w: W - 2 * M, h: 0.32, fontSize: 14, bold: true, color: NAVY, margin: 0 });
bullets([
  "Quy trình tự động dựng nhãn mô tả có cấu trúc, kèm hai bộ lọc thêm vào sau khi đo thấy nhãn bị nhiễu",
  "Quy trình kiểm định chất lượng dùng lại được: đối chứng ghép sai, chín bất biến, kiểm rò rỉ, đối chiếu với câu của người",
  "Phân tích chiến lược quy chiếu trên 41.099 nhãn và 41.084 câu của người chú thích",
], M + 0.1, 5.45, W - 2 * M - 0.2, { fs: 12, gap: 0.42, itemH: 0.4, lh: 1.15 });
N(2); foot(); done();

// ══════════ 3 · BÀI TOÁN ══════════
slide();
bar("1 · Bài toán: viết câu để người khác trỏ đúng một phần tử");
block(M, 0.85, W - 2 * M, 1.45);
text([{ text: "Vào.  ", options: { bold: true, color: BLUE } }, { text: "ảnh màn hình  +  mục tiêu “Chia sẻ playlist này cho bạn tôi”", options: { italic: true } }], { x: M + 0.25, y: 0.95, w: W - 2 * M - 0.5, h: 0.5, fontSize: 14.5, margin: 0 });
text([{ text: "Ra.  ", options: { bold: true, color: BLUE } }, { text: "“chạm vào biểu tượng bút chì ở góc trên bên phải của ghi chú”", options: { italic: true } }], { x: M + 0.25, y: 1.62, w: W - 2 * M - 0.5, h: 0.5, fontSize: 14.5, margin: 0 });
text("Tác tử điều khiển giao diện", { x: M, y: 2.6, w: 4.35, h: 0.35, fontSize: 14.5, bold: true, color: NAVY, align: "center", margin: 0 });
text("Bài toán của chúng tôi", { x: 5.1, y: 2.6, w: 4.35, h: 0.35, fontSize: 14.5, bold: true, color: RED, align: "center", margin: 0 });
block(M, 3.0, 4.35, 1.6); block(5.1, 3.0, 4.35, 1.6);
text("Nhận câu chỉ dẫn, trả về toạ độ\nthao tác tương ứng.", { x: M + 0.25, y: 3.2, w: 3.9, h: 1.2, fontSize: 14, margin: 0, lh: 1.4 });
text("Nhận ảnh và mục tiêu, phải viết ra\nchính câu chỉ dẫn ấy.", { x: 5.35, y: 3.2, w: 3.9, h: 1.2, fontSize: 14, margin: 0, lh: 1.4 });
block(M, 4.85, W - 2 * M, 1.35);
text([{ text: "Về mặt ngôn ngữ, đây là bài toán sinh biểu thức quy chiếu. ", options: { bold: true, color: NAVY } }, { text: "Câu sinh ra phải đủ để người nghe nhận ra đúng một đối tượng, không lẫn với những đối tượng khác cùng có mặt (Dale & Reiter, 1995).", options: {} }], { x: M + 0.25, y: 4.85, w: W - 2 * M - 0.5, h: 1.35, fontSize: 14, valign: "middle", margin: 0, lh: 1.35 });
N(3); foot(); done();

// ══════════ 4 · ĐẶC THÙ MIỀN ══════════
slide();
bar("1 · Miền giao diện đảo ngược thứ tự ưu tiên của quy chiếu");
text("Đo trên 120 màn lấy ngẫu nhiên từ 99.131 màn của cây trợ năng", { x: M, y: 0.85, w: W - 2 * M, h: 0.35, fontSize: 13.5, italic: true, color: GREY, margin: 0 });
[["12,6%", "phần tử có nhãn văn bản trong cây trợ năng", "22 trong 120 màn ấy không có phần tử nào được đặt tên", TEAL],
 ["22,0%", "phần tử cần chạm không có tên cụ thể", "trên 41.099 nhãn đã dựng", RED],
 ["7,6%", "trùng tên với ít nhất một phần tử khác trên cùng màn", "hai nhóm không có phần tử chung", RED]].forEach((c, i) => {
  const yy = 1.3 + i * 1.05;
  block(M, yy, W - 2 * M, 0.92);
  text(c[0], { x: M + 0.2, y: yy, w: 1.3, h: 0.92, fontSize: 22, bold: true, color: c[3], align: "center", valign: "middle", margin: 0 });
  text(c[1], { x: M + 1.6, y: yy + 0.13, w: 6.6, h: 0.38, fontSize: 14.5, bold: true, color: NAVY, margin: 0 });
  text(c[2], { x: M + 1.6, y: yy + 0.5, w: 6.6, h: 0.35, fontSize: 12.5, italic: true, color: GREY, margin: 0 });
});
rect(M, 4.55, W - 2 * M, 0.72, NAVY, { radius: 0.06 });
text("Gộp hai nhóm: 12.162 / 41.099 = 29,6% số bước không quy chiếu được bằng tên", { x: M, y: 4.55, w: W - 2 * M, h: 0.72, fontSize: 15, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
text("Ảnh tự nhiên: đối tượng nào cũng có danh từ để gọi, quan hệ chỉ là phương án bổ sung.\nGiao diện: ở gần một phần ba số trường hợp, quan hệ với chữ lân cận là phương tiện quy chiếu duy nhất còn lại.", { x: M + 0.1, y: 5.45, w: W - 2 * M - 0.2, h: 0.8, fontSize: 13.5, margin: 0, lh: 1.35 });
N(4); foot(); done();

// ══════════ 5 · CÔNG TRÌNH LIÊN QUAN ══════════
slide();
bar("1 · Vị trí của bài so với các dòng nghiên cứu liên quan");
table(M, 0.95, [3.0, 2.95, 2.95], [
  { cells: ["Công trình", "Họ làm gì", "Bài này khác đi"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 13 },
  { cells: ["Dale & Reiter 1995\nDale & Haddock 1991", "Chọn thuộc tính đủ tách đối tượng; mô tả bằng quan hệ khi thuộc tính không đủ", "Đo phân bố nhãn trong miền mà tên gọi gần như không có sẵn"], h: 1.0, fs: 12, rule: true },
  { cells: ["Mao 2016 · Luo 2017\nYu 2017", "Đưa tiêu chí phân biệt vào cách huấn luyện, trên ảnh tự nhiên", "Chuyển khung ấy sang miền giao diện, nơi 22,0% phần tử không có tên"], h: 1.0, fs: 12, rule: true },
  { cells: ["Widget Captioning\nY. Li và cộng sự 2020b", "Sinh mô tả cho phần tử giao diện, nhãn do người viết", "Nhãn dựng bằng quy tắc; tính phân biệt là thuộc tính của cặp phần tử và màn hình"], h: 1.0, fs: 12, rule: true },
  { cells: ["Chen và cộng sự 2020", "Dự đoán nhãn trợ năng còn thiếu", "Chấp nhận nhãn thiếu, chuyển việc quy chiếu sang quan hệ với chữ lân cận"], h: 0.85, fs: 12, rule: true },
  { cells: ["AndroidControl\nW. Li và cộng sự 2024", "Câu chỉ dẫn theo bước là đầu vào", "Chính câu đó là đầu ra mong đợi"], h: 0.72, fs: 12 },
], { align: ["left", "left", "left"] });
block(M, 6.05, W - 2 * M, 0.6);
text("Bài không dùng chữ “đầu tiên” cho ý này: dòng sinh biểu thức quy chiếu đã có từ năm 1995.", { x: M + 0.25, y: 6.05, w: W - 2 * M - 0.5, h: 0.6, fontSize: 12.5, bold: true, color: RED, valign: "middle", margin: 0 });
N(5); foot(); done();

// ══════════ 6 · NGUỒN VÀ PHÉP GHÉP ══════════
slide();
bar("2 · Không bản phát hành nào có đủ ba thành phần cần dùng");
text("Mỗi bước cần: câu chỉ dẫn của người chú thích  ·  ảnh màn hình  ·  cây trợ năng", { x: M, y: 0.82, w: W - 2 * M, h: 0.32, fontSize: 13.5, italic: true, color: GREY, margin: 0 });
table(M, 1.2, [3.5, 2.7, 2.7], [
  { cells: ["Bản phát hành trên Hugging Face", "Có", "Thiếu"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5 },
  { cells: ["HarrytheOrange/\nparsed_AndroidControl", "câu chỉ dẫn đủ 15.283 chuỗi;\ncây trợ năng 99.131 màn", "không có ảnh"], h: 0.85, fs: 12, rule: true },
  { cells: ["ckg/AndroidControl\nParsedWithImages-20k", "ảnh màn hình", "đã chuyển sang định dạng tác tử nên mất câu chỉ dẫn theo bước"], h: 0.9, fs: 12 },
], { align: ["left", "left", "left"] });
text("Ghép theo khoá (episode_id, step_id). Ghép lệch một bước là loại lỗi nguy hiểm nhất: số dòng vẫn đủ, huấn luyện vẫn hội tụ, mọi khâu vẫn chạy, mà mô hình học ảnh của bước A với câu của bước B.", { x: M, y: 3.15, w: W - 2 * M, h: 0.8, fontSize: 13.5, margin: 0, lh: 1.35 });
text("Kiểm định ghép: chạy OCR tại điểm chạm đáp án, xem chuỗi đọc được có nằm trong câu chỉ dẫn không", { x: M, y: 3.95, w: W - 2 * M, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
table(M + 0.5, 4.35, [4.3, 2.3, 2.0], [
  { cells: ["", "Tỉ lệ khớp", "Khoảng tin cậy 95%"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12, align: ["left", "center", "center"] },
  { cells: ["Ghép đúng  (400 bước)", { t: "48,3%", fs: 15 }, "[43,4 ; 53,1]"], h: 0.55, fs: 13, color: TEAL, bold: true, rule: true },
  { cells: ["Đối chứng ghép lệch một bước  (311 bước)", { t: "19,6%", fs: 15 }, "[15,6 ; 24,4]"], h: 0.55, fs: 13, color: RED, bold: true },
], { align: ["left", "center", "center"] });
text("Con số 48% tự nó không nói lên điều gì, vì OCR có lỗi và người chú thích không nhất thiết nhắc lại chữ in trên nút. Kết luận rút ra từ khoảng cách giữa hai con số: 2,5 lần, hai khoảng tin cậy cách nhau 19 điểm phần trăm.", { x: M, y: 5.95, w: W - 2 * M, h: 0.75, fontSize: 12.5, margin: 0, lh: 1.3 });
N(6); foot(); done();

// ══════════ 7 · OCR ══════════
slide();
bar("2 · Cây trợ năng không đủ, nên chữ trên màn phải đọc bằng OCR");
block(M, 0.85, 4.35, 1.6);
text("Cây trợ năng", { x: M + 0.2, y: 0.95, w: 3.9, h: 0.32, fontSize: 14, bold: true, color: NAVY, margin: 0 });
text("Trung vị 86 phần tử một màn, nhưng chỉ 12,6% có nhãn văn bản. Bản kết xuất còn lẫn cả trường mô tả dành cho trình đọc màn hình.", { x: M + 0.2, y: 1.3, w: 3.9, h: 1.1, fontSize: 12.5, margin: 0, lh: 1.3 });
block(5.1, 0.85, 4.35, 1.6);
text("OCR toàn bộ ảnh", { x: 5.3, y: 0.95, w: 3.9, h: 0.32, fontSize: 14, bold: true, color: NAVY, margin: 0 });
text("RapidOCR bản ONNX chạy trên CPU. Thu được 64.567 bản ghi cho tập huấn luyện và 6.958 cho tập kiểm tra, phủ 100%.", { x: 5.3, y: 1.3, w: 3.9, h: 1.1, fontSize: 12.5, margin: 0, lh: 1.3 });
text("Trong 32.061 tên lấy được, 8.581 đến từ cây trợ năng và 23.480 đến từ OCR, tỉ lệ khoảng 1 : 2,7", { x: M, y: 2.6, w: W - 2 * M, h: 0.35, fontSize: 14, bold: true, color: TEAL, margin: 0 });
text("Hai dạng sai sót quan sát được, và cách xử lý khác nhau cho mỗi dạng", { x: M, y: 3.05, w: W - 2 * M, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Biểu tượng bị đọc thành ký tự: nguy hiểm hơn, vì sinh ra một chuỗi trông như tên thật. Không có nhãn chuẩn nên tần suất không đo trực tiếp được",
  "Mất khoảng trắng giữa hai từ, cho ra chuỗi dính liền như Turnon: chỉ đẩy phần tử xuống nhóm không có tên, nhãn vẫn không chứa thông tin sai",
], M + 0.1, 3.45, W - 2 * M - 0.2, { fs: 13, gap: 0.72, itemH: 0.7, lh: 1.3 });
block(M, 5.0, W - 2 * M, 1.2);
text([{ text: "Với dữ liệu huấn luyện, lỗi bỏ sót ít tốn kém hơn hẳn lỗi gán sai. ", options: { bold: true, color: RED } }, { text: "Nhãn để trống chỉ làm mô hình mất một mẫu học, còn nhãn ghi tên sai thì dạy mô hình gọi phần tử bằng một chuỗi không tồn tại trên màn hình.", options: {} }], { x: M + 0.25, y: 5.0, w: W - 2 * M - 0.5, h: 1.2, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.35 });
text("Chạy lại trên hai máy khác nhau, cách nhau năm ngày, kết quả trùng nhau. Vì AndroidControl không có nhãn chuẩn cho chữ trên màn, bài không tuyên bố độ chính xác OCR.", { x: M, y: 6.3, w: W - 2 * M, h: 0.6, fontSize: 11.5, italic: true, color: GREY, margin: 0, lh: 1.25 });
N(7); foot(); done();

// ══════════ 8 · NHÃN BỐN Ô ══════════
slide();
bar("2 · Dòng nhãn bốn ô, dựng hoàn toàn bằng quy tắc");
[["vai trò", "tên lớp Android rút về một từ", TEAL],
 ["tên", "chữ hiển thị; cây trợ năng trước, OCR sau", BLUE],
 ["toạ độ", "điểm chạm quy về thang 0 đến 1.000", GREY],
 ["dấu hiệu phân biệt", "mệnh đề tách phần tử khỏi những phần tử giống nó", RED]].forEach((c, i) => {
  const xx = M + i * 2.24;
  rect(xx, 0.85, 2.14, 1.5, BLOCK, { radius: 0.05 });
  text(c[0], { x: xx + 0.1, y: 0.93, w: 1.94, h: 0.35, fontSize: 13.5, bold: true, color: c[2], align: "center", margin: 0 });
  text(c[1], { x: xx + 0.12, y: 1.3, w: 1.9, h: 0.95, fontSize: 11.5, align: "center", margin: 0, lh: 1.25 });
});
text("Nhãn chỉ dựng cho bước chạm, tức bước mà thao tác đúng là một cú chạm lên màn hình. Phần tử cần chạm xác định bằng hộp bao nhỏ nhất chứa điểm chạm của đáp án.", { x: M, y: 2.45, w: W - 2 * M, h: 0.6, fontSize: 12.5, italic: true, color: GREY, margin: 0, lh: 1.3 });
img("../../paper/vcl2026/hinh/fig_moneo.png", M, 3.05, 8.9, 2.93);
text("<desc>icon | (no name) | <point>111,903</point> | just above the text “Gmail”</desc>", { x: M, y: 6.0, w: W - 2 * M, h: 0.35, fontSize: 12, fontFace: MONO, color: NAVY, align: "center", margin: 0 });
text("Bốn biểu tượng cùng vai trò, không cái nào có tên. Chuỗi OCR gần nhất nằm ngoài hộp bao, cách tâm 114,5 px, được lấy làm mỏ neo. Câu của người chú thích cho cùng bước là “Click on the gmail option”, cũng quy chiếu qua chữ Gmail.", { x: M, y: 6.35, w: W - 2 * M, h: 0.6, fontSize: 11.5, italic: true, color: GREY, align: "center", margin: 0, lh: 1.25 });
N(8); foot(); done();

// ══════════ 9 · HAI BỘ LỌC ══════════
slide();
bar("2 · Hai bộ lọc, mỗi bộ thêm vào sau khi đo thấy nhãn bị nhiễu");
text("Cả hai đều không có trong thiết kế ban đầu, và bài nêu đúng theo thứ tự thời gian đó.", { x: M, y: 0.85, w: W - 2 * M, h: 0.35, fontSize: 13.5, italic: true, color: GREY, margin: 0 });
block(M, 1.25, W - 2 * M, 2.1);
text("Bộ lọc nhãn trợ năng", { x: M + 0.25, y: 1.35, w: 8.4, h: 0.35, fontSize: 15, bold: true, color: NAVY, margin: 0 });
text("Loại bốn loại chuỗi hợp lệ về cú pháp nhưng không dùng được cho việc quy chiếu: định danh lấy từ mã nguồn, chuỗi số dài, hậu tố dành cho trình đọc màn hình, và chuỗi báo rằng phần tử không hề có nhãn, chẳng hạn No label specified.", { x: M + 0.25, y: 1.72, w: 8.4, h: 0.9, fontSize: 13, margin: 0, lh: 1.3 });
text([{ text: "Phạm vi:  ", options: { bold: true } }, { text: "14,7% nhãn tại phần tử cần chạm trên mẫu thử 1.074 nhãn   ·   347 / 8.928 = 3,9% ứng viên lấy từ cây trên toàn bộ ngữ liệu", options: {} }], { x: M + 0.25, y: 2.65, w: 8.4, h: 0.6, fontSize: 12.5, color: TEAL, margin: 0, lh: 1.25 });
block(M, 3.5, W - 2 * M, 1.85);
text("Bộ lọc hình học", { x: M + 0.25, y: 3.6, w: 8.4, h: 0.35, fontSize: 15, bold: true, color: NAVY, margin: 0 });
text("Chỉ cho phép lấy tên từ OCR khi hộp chiếm dưới 25% diện tích màn. Hộp quá lớn thì chữ đọc được bên trong không còn quy chiếu về phần tử cần chạm nữa: một hộp phủ 95% màn cho chuỗi THEFELLOWSHIPOF THE RING.", { x: M + 0.25, y: 3.97, w: 8.4, h: 0.9, fontSize: 13, margin: 0, lh: 1.3 });
text([{ text: "Phạm vi:  ", options: { bold: true } }, { text: "căn cứ chỉ dựa trên 25 trường hợp ở mẫu thử   ·   912 / 41.099 = 2,2% số bước trên toàn bộ ngữ liệu", options: {} }], { x: M + 0.25, y: 4.85, w: 8.4, h: 0.4, fontSize: 12.5, color: TEAL, margin: 0 });
block(M, 5.5, W - 2 * M, 0.72);
text("Khi tên không kiểm chứng được, hai bộ lọc để ô tên trống thay vì điền một chuỗi phỏng đoán.", { x: M + 0.25, y: 5.5, w: 8.4, h: 0.72, fontSize: 13.5, bold: true, color: RED, valign: "middle", margin: 0 });
N(9); foot(); done();

// ══════════ 10 · Ô THỨ TƯ LÀM LẠI ══════════
slide();
bar("2 · Ô dấu hiệu phân biệt: từ 7,3% lên 75,9% sau khi làm lại");
text("Bản đầu của ô thứ tư gần như không dùng được, và điều đó chỉ lộ ra khi đem đọc thủ công mẫu thử 1.074 nhãn.", { x: M, y: 0.85, w: W - 2 * M, h: 0.4, fontSize: 13.5, margin: 0 });
block(M, 1.3, 4.35, 2.2);
text("Bản đầu", { x: M + 0.2, y: 1.4, w: 3.9, h: 0.32, fontSize: 14.5, bold: true, color: RED, margin: 0 });
text("7,3%", { x: M + 0.2, y: 1.75, w: 3.9, h: 0.5, fontSize: 26, bold: true, color: RED, align: "center", margin: 0 });
text("giải quyết được mơ hồ, còn 85,8% chỉ là mệnh đề đếm số lượng, kiểu “một trong bảy phần tử cùng loại”.", { x: M + 0.2, y: 2.3, w: 3.9, h: 1.1, fontSize: 12.5, margin: 0, lh: 1.3 });
block(5.1, 1.3, 4.35, 2.2);
text("Sau khi sắp xếp lại quy tắc", { x: 5.3, y: 1.4, w: 3.9, h: 0.32, fontSize: 14.5, bold: true, color: TEAL, margin: 0 });
text("75,9%", { x: 5.3, y: 1.75, w: 3.9, h: 0.5, fontSize: 26, bold: true, color: TEAL, align: "center", margin: 0 });
text("trên cùng mẫu thử và cùng bảng phân loại; trên toàn bộ 41.099 nhãn là 75,3%, lệch 0,6 điểm phần trăm.", { x: 5.3, y: 2.3, w: 3.9, h: 1.1, fontSize: 12.5, margin: 0, lh: 1.3 });
text("Hai thay đổi", { x: M, y: 3.65, w: W - 2 * M, h: 0.32, fontSize: 14, bold: true, color: NAVY, margin: 0 });
bullets([
  "Sắp xếp lại quy tắc theo tiêu chí mệnh đề có giải quyết được mơ hồ hay không, thay vì theo thứ tự dễ tính trước",
  "Bổ sung mỏ neo chữ: chuỗi OCR gần nhất nằm ngoài hộp bao, cách tâm không quá 350 px, kèm hướng (just above, to the left of)",
], M + 0.1, 4.05, W - 2 * M - 0.2, { fs: 13, gap: 0.72, itemH: 0.7, lh: 1.3 });
block(M, 5.55, W - 2 * M, 0.75);
text("Mỏ neo đúng chiều ở 737/737 trường hợp của mẫu thử, nhưng cách dựng chỉ bảo đảm hướng đúng, không bảo đảm mệnh đề hữu ích.", { x: M + 0.25, y: 5.55, w: 8.4, h: 0.75, fontSize: 13, valign: "middle", margin: 0, lh: 1.3 });
N(10); foot(); done();

// ══════════ 11 · PHÂN BỐ THEO TẦNG TÊN ══════════
slide();
bar("3 · Độ phủ của dấu hiệu lệch theo hướng bất lợi");
table(M, 0.88, [2.2, 0.95, 1.25, 1.0, 1.25, 0.95, 1.3], [
  { cells: ["Tầng tên", "n", "Mỏ neo chữ", "Duy nhất", "Nêu trùng tên", "Chỉ đếm", "Giải quyết được"], bold: true, color: WHITE, fill: NAVY, h: 0.55, fs: 11, align: ["left", "right", "right", "right", "right", "right", "right"] },
  { cells: ["Tên rõ ràng", "30.252", "72,2%", "7,9%", "1,7%", "18,2%", { t: "80,1%", bold: true, color: TEAL }], h: 0.46, fs: 12, rule: true },
  { cells: ["Chỉ có ký hiệu", "1.809", "32,7%", "4,8%", "31,3%", "31,2%", { t: "37,5%", bold: true, color: RED }], h: 0.46, fs: 12, rule: true },
  { cells: ["Không có tên", "9.038", "57,5%", "9,2%", "-", "33,3%", { t: "66,7%", bold: true, color: MAROON }], h: 0.46, fs: 12, rule: true },
  { cells: ["Toàn bộ", "41.099", "67,2%", "8,1%", "2,6%", "22,1%", { t: "75,3%", bold: true }], bold: true, h: 0.46, fs: 12 },
], { align: ["left", "right", "right", "right", "right", "right", "right"] });
text("Hai cột giữa giải quyết được mơ hồ, hai cột sau chỉ nêu rằng có mơ hồ mà không giúp chọn.", { x: M, y: 3.3, w: W - 2 * M, h: 0.3, fontSize: 11.5, italic: true, color: GREY, margin: 0 });
block(M, 3.65, W - 2 * M, 1.2);
text([{ text: "Những phần tử cần dấu hiệu phân biệt nhất lại là những phần tử có tỉ lệ giải quyết được thấp nhất. ", options: { bold: true, color: RED } }, { text: "Tầng tên rõ ràng, nơi bản thân cái tên đã đủ quy chiếu, đạt 80,1%. Tầng chỉ có ký hiệu, nơi dấu hiệu là phương tiện duy nhất còn lại, chỉ đạt 37,5%.", options: {} }], { x: M + 0.25, y: 3.65, w: 8.4, h: 1.2, fontSize: 13, valign: "middle", margin: 0, lh: 1.32 });
text("Nguyên nhân là cơ học chứ không phải khái niệm", { x: M, y: 4.98, w: W - 2 * M, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Mỏ neo chữ cần một chuỗi OCR nằm ngoài hộp và đủ gần, mà vùng dày biểu tượng không nhãn cũng thường là vùng thưa chữ",
  "Trong 3.124 trường hợp trùng tên, 65,7% nhận được mỏ neo, còn 34,3% chỉ được báo là trùng tên",
  "Hướng mỏ neo lệch theo trục ngang: trong 27.628 mỏ neo, to the right of có 8.382 còn to the left of chỉ 2.033, vì nhãn văn bản trên Android thường đặt bên trái phần tử thao tác",
], M + 0.1, 5.32, W - 2 * M - 0.2, { fs: 12.5, gap: 0.5, itemH: 0.48, lh: 1.2 });
N(11); foot(); done();

// ══════════ 12 · NGƯỜI CHÚ THÍCH CŨNG ĐỊNH VỊ ══════════
slide();
bar("3 · Người chú thích và quy trình tự động chọn cùng một chiến lược");
text("Ba số đo đặt cạnh nhau cùng chỉ về một hiện tượng: bên viết câu phải bỏ lối gọi tên mà chuyển sang lối định vị.", { x: M, y: 0.85, w: W - 2 * M, h: 0.4, fontSize: 13.5, margin: 0 });
text("Phía màn hình", { x: M, y: 1.3, w: 4.35, h: 0.32, fontSize: 14, bold: true, color: NAVY, align: "center", margin: 0 });
text("Phía ngôn ngữ", { x: 5.1, y: 1.3, w: 4.35, h: 0.32, fontSize: 14, bold: true, color: NAVY, align: "center", margin: 0 });
block(M, 1.68, 4.35, 2.5); block(5.1, 1.68, 4.35, 2.5);
bullets([
  [{ text: "55,6%", options: { bold: true, color: TEAL } }, { text: " số bước có sẵn ít nhất một phần tử cạnh tranh trong dải 80 đến 350 px quanh phần tử cần chạm", options: {} }],
  [{ text: "91,6%", options: { bold: true, color: TEAL } }, { text: " số bước có ít nhất một phần tử cùng vai trò, trung vị 8 phần tử một màn", options: {} }],
], M + 0.2, 1.85, 3.95, { fs: 12.5, gap: 1.15, itemH: 1.1, lh: 1.3 });
bullets([
  [{ text: "32,5%", options: { bold: true, color: RED } }, { text: " trong 41.084 câu của người chú thích chứa ít nhất một từ chỉ vị trí hoặc thứ tự: top, left, corner, above, first…", options: {} }],
  [{ text: "67,2%", options: { bold: true, color: RED } }, { text: " dấu hiệu của quy trình tự động là quan hệ với chữ lân cận; riêng nhóm không có tên vẫn là 57,5%", options: {} }],
], 5.3, 1.85, 3.95, { fs: 12.5, gap: 1.15, itemH: 1.1, lh: 1.3 });
block(M, 4.35, W - 2 * M, 1.0);
text("Việc phân biệt là bài toán thật của miền này, không phải một yêu cầu chúng tôi tự đặt ra.", { x: M + 0.25, y: 4.35, w: 8.4, h: 1.0, fontSize: 14.5, bold: true, color: NAVY, valign: "middle", margin: 0 });
text("Khác biệt còn lại giữa hai bên: người chú thích nhìn thấy hình dạng của biểu tượng rồi đặt tên cho nó, chẳng hạn gọi thẳng search icon hay Right arrow key, còn quy trình dựng bằng quy tắc thì chỉ đọc được chữ. Chỗ nào tên phải suy ra từ hình vẽ thì nhãn tự động không dựng được, và đó cũng là chỗ một mô hình thị giác về sau phải tự bổ sung.", { x: M, y: 5.5, w: W - 2 * M, h: 1.0, fontSize: 12.5, margin: 0, lh: 1.35 });
N(12); foot(); done();

// ══════════ 13 · QUY MÔ VÀ CHIA TẬP ══════════
slide();
bar("3 · Quy mô, cách chia tập và ba điều cách chia không bảo đảm");
table(M, 0.9, [4.6, 2.15, 2.15], [
  { cells: ["", "Tập huấn luyện", "Tập kiểm tra"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12.5, align: ["left", "right", "right"] },
  { cells: ["Số bước", "64.567", "6.958"], h: 0.36, fs: 12.5, rule: true },
  { cells: ["Bước chạm", "41.191  (63,8%)", "4.463  (64,1%)"], h: 0.36, fs: 12.5, rule: true },
  { cells: ["Số tác vụ", "12.895", "1.432"], h: 0.36, fs: 12.5, rule: true },
  { cells: ["Độ phủ OCR", "100%", "100%"], h: 0.36, fs: 12.5, rule: true },
  { cells: ["Độ phủ nhãn mô tả trên bước chạm", "99,8%", "99,7%"], h: 0.36, fs: 12.5 },
], { align: ["left", "right", "right"] });
text("GUIRefCorpus: 41.099 dòng ở tập huấn luyện và 4.448 dòng ở tập kiểm tra, mỗi dòng một bản ghi JSON, mang khoá (episode_id, step_id) để nối ngược về bước gốc. Chia theo tác vụ, không chia ngẫu nhiên theo dòng. Kiểm rò rỉ chạy trên toàn bộ ngữ liệu: không tác vụ nào trùng giữa hai tập.", { x: M, y: 3.15, w: W - 2 * M, h: 0.85, fontSize: 12.5, margin: 0, lh: 1.3 });
text("Ba điều cách chia này không bảo đảm, và cả ba đều dễ bị diễn giải rộng hơn mức dữ liệu cho phép", { x: M, y: 4.05, w: W - 2 * M, h: 0.32, fontSize: 13.5, bold: true, color: RED, margin: 0 });
bullets([
  "Tách theo tác vụ không phải tách theo cách diễn đạt: 17,3% câu ở bước chạm của tập kiểm tra xuất hiện nguyên văn trong một mẫu chỉ bằng 2,6% tập huấn luyện, và 63,9% có chung ít nhất một cụm bốn từ liên tiếp",
  "Tập kiểm tra không phải tập ứng dụng chưa từng thấy: trong các bước quy được về một ứng dụng có tên, 95,6% thuộc ứng dụng cũng có ở tập huấn luyện",
  "Chỉ 45,0% số bước tập kiểm gán được tên ứng dụng; 3.828 bước còn lại mang nhãn không biết, mà không biết khác hẳn chưa thấy",
], M + 0.1, 4.45, W - 2 * M - 0.2, { fs: 12, gap: 0.62, itemH: 0.6, lh: 1.2 });
N(13); foot(); done();

// ══════════ 14 · KIỂM NGOẠI SINH ══════════
slide();
bar("4 · Phép so với một nguồn nằm ngoài quy trình");
text("Quy trình dựng nhãn không đọc câu chỉ dẫn ở bất kỳ khâu nào: vai trò, tên, toạ độ và dấu hiệu đều tính từ cây trợ năng, hộp bao và kết quả OCR. Vì vậy khi ô tên trùng với chữ người chú thích dùng, đó là so với nguồn bên ngoài chứ không phải phép tự kiểm.", { x: M, y: 0.85, w: W - 2 * M, h: 0.75, fontSize: 13, margin: 0, lh: 1.3 });
table(M + 0.3, 1.75, [5.0, 1.9, 1.9], [
  { cells: ["Trên 3.505 nhãn có tên của tập kiểm tra", "Tỉ lệ khớp", "Khoảng tin cậy"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 12, align: ["left", "center", "center"] },
  { cells: ["Ô tên xuất hiện nguyên văn trong câu của người", { t: "53,5%", fs: 16 }, "[51,8 ; 55,1]"], h: 0.58, fs: 12.5, color: TEAL, bold: true, rule: true },
  { cells: ["Đối chứng: ghép với câu của bước liền sau", { t: "5,4%", fs: 16 }, "[4,7 ; 6,2]"], h: 0.58, fs: 12.5, color: GREY, bold: true, rule: true },
  { cells: ["Đối chứng chặt: bước liền sau trong cùng chuỗi thao tác", { t: "7,6%", fs: 16 }, "[6,5 ; 8,9]"], h: 0.58, fs: 12.5, color: RED, bold: true },
], { align: ["left", "center", "center"] });
text("Đối chứng lỏng có thể bị phản bác là quá dễ, vì hai bước liền nhau trong tệp không nhất thiết cùng một chuỗi. Đối chứng chặt so hai màn hình liên tiếp trong cùng một chuỗi trên cùng ứng dụng, tức hai màn rất giống nhau, và tỉ số vẫn là bảy lần. Cả hai số đo chạy trên toàn tập, không phải trên mẫu thử.", { x: M, y: 4.1, w: W - 2 * M, h: 0.8, fontSize: 12.5, margin: 0, lh: 1.3 });
block(M, 4.95, 4.35, 1.3);
text([{ text: "53,5% là một chặn dưới. ", options: { bold: true, color: NAVY } }, { text: "Người chú thích thường gọi phần tử bằng tên chủng loại, viết the search bar cho ô mang chữ Search here, mà cách so nguyên văn không tính là khớp.", options: {} }], { x: M + 0.2, y: 4.95, w: 3.95, h: 1.3, fontSize: 12, valign: "middle", margin: 0, lh: 1.3 });
block(5.1, 4.95, 4.35, 1.3);
text([{ text: "Chia theo tầng tên thì kết quả đi đúng hướng: ", options: {} }, { text: "55,3%", options: { bold: true, color: TEAL } }, { text: " ở tầng tên rõ ràng, còn tầng chỉ có ký hiệu chỉ ", options: {} }, { text: "24,5%", options: { bold: true, color: RED } }, { text: ".", options: {} }], { x: 5.3, y: 4.95, w: 3.95, h: 1.3, fontSize: 12, valign: "middle", margin: 0, lh: 1.3 });
N(14); foot(); done();

// ══════════ 15 · HẠN CHẾ ══════════
slide();
bar("5 · Hạn chế của bộ ngữ liệu");
[["24,7% dấu hiệu phân biệt chưa giải quyết được mơ hồ",
  "Đây là phần bù của 75,3%. Chừng ấy ô thứ tư chỉ đếm số lượng hoặc chỉ nêu rằng có trùng tên, nên với những bước đó nhãn thực chất chỉ còn ba ô định danh. Nguyên nhân đã xác định được nên chỗ này sửa được: hướng sửa trước tiên là mở rộng nguồn neo ra ngoài chuỗi OCR gần nhất, chẳng hạn dùng quan hệ với các phần tử cùng vai trò, vốn có ở 91,6% số bước."],
 ["So sánh với nguồn bên ngoài mới chạm được một trong bốn ô",
  "Ba ô còn lại, nhất là ô dấu hiệu phân biệt, chưa có nguồn nào bên ngoài để đối chiếu, nên 73,6%, 22,0% và 7,6% vẫn là thuộc tính của chính nhãn chứ không phải phán quyết của người dùng. Cách kiểm đúng nhất là hỏi thẳng người dùng rằng một nhãn có đủ để họ tìm ra phần tử trên ảnh hay không, và chúng tôi chưa làm được điều đó."],
 ["Hai giới hạn đến từ chính bản phát hành gốc",
  "AndroidControl không cung cấp nhãn chuẩn cho OCR, nên bài chỉ báo độ ổn định giữa hai lần chạy và hai dạng sai sót đã quan sát được. Gần như mọi chuỗi mục tiêu cũng bị cắt dở dang ngay từ nguồn."]].forEach((c, i) => {
  const yy = 0.9 + i * 1.78;
  block(M, yy, W - 2 * M, 1.62);
  text(c[0], { x: M + 0.25, y: yy + 0.1, w: 8.4, h: 0.35, fontSize: 14, bold: true, color: RED, margin: 0 });
  text(c[1], { x: M + 0.25, y: yy + 0.47, w: 8.4, h: 1.05, fontSize: 12.5, margin: 0, lh: 1.32 });
});
N(15); foot(); done();

// ══════════ 16 · KẾT LUẬN ══════════
slide();
bar("5 · Kết luận");
bullets([
  [{ text: "Một quy trình hoàn toàn tự động ", options: { bold: true, color: NAVY } }, { text: "chuyển AndroidControl thành bộ ngữ liệu GUIRefCorpus: 41.099 nhãn ở tập huấn luyện và 4.448 ở tập kiểm tra. Không nhãn nào do người soạn, sửa hay chọn; mỗi lần đọc tay thấy sai thì thứ được sửa là bộ quy tắc, rồi dựng lại từ đầu.", options: {} }],
  [{ text: "Đặc thù của miền buộc nhãn phải mang ô dấu hiệu phân biệt: ", options: { bold: true, color: NAVY } }, { text: "12,6% phần tử có tên trong cây trợ năng, 22,0% phần tử cần chạm không có tên, 7,6% trùng tên. Ô đó phải làm lại từ đầu sau khi đo thấy bản đầu chỉ giải quyết được 7,3%, và sau khi làm lại đạt 75,3%.", options: {} }],
  [{ text: "Chỗ dựa chính là phép đối chiếu với nguồn ngoài quy trình: ", options: { bold: true, color: NAVY } }, { text: "53,5% ô tên trùng nguyên văn câu của người chú thích, so với 7,6% ở đối chứng cố ý ghép sai trong cùng một chuỗi thao tác. Đặt cạnh 32,5% câu của người cũng dùng tới từ chỉ vị trí, hai bên đang chọn cùng một chiến lược quy chiếu.", options: {} }],
], M + 0.1, 0.95, W - 2 * M - 0.2, { fs: 13, gap: 1.55, itemH: 1.5, lh: 1.35 });
block(M, 5.75, W - 2 * M, 0.95);
text([{ text: "Nguyên tắc làm việc dùng lại được:  ", options: { bold: true, color: RED } }, { text: "tìm cho ra cơ chế sinh ra một tỉ số bất thường trước khi lấy tỉ số ấy làm căn cứ đổi thiết kế. Bốn lỗi bắt được đều xảy ra trong lúc mọi khâu vẫn chạy bình thường.", options: {} }], { x: M + 0.25, y: 5.75, w: 8.4, h: 0.95, fontSize: 13, valign: "middle", margin: 0, lh: 1.32 });
N(16); foot(); done();

// ══════════ 17 · CẢM ƠN ══════════
slide();
rect(0, 0, W, H - 0.26, NAVY);
text("Xin cảm ơn hội thảo đã lắng nghe", { x: 0.8, y: 2.3, w: W - 1.6, h: 0.7, fontSize: 27, bold: true, color: WHITE, align: "center", margin: 0 });
text("Lê Đoàn Phương Uyên   ·   Nguyễn Hồng Bửu Long", { x: 0.8, y: 3.3, w: W - 1.6, h: 0.4, fontSize: 16, color: WHITE, align: "center", margin: 0 });
text("Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM", { x: 0.8, y: 3.75, w: W - 1.6, h: 0.4, fontSize: 13, color: "C9C3DC", align: "center", margin: 0 });
text("Bộ ngữ liệu GUIRefCorpus  ·  41.099 nhãn  ·  4.448 nhãn tập kiểm tra", { x: 0.8, y: 4.6, w: W - 1.6, h: 0.4, fontSize: 14, bold: true, color: WHITE, align: "center", margin: 0 });
text("Rất mong nhận được câu hỏi và góp ý", { x: 0.8, y: 5.15, w: W - 1.6, h: 0.4, fontSize: 14, italic: true, color: "C9C3DC", align: "center", margin: 0 });
N(17); foot(); done();

// ═══════════════ SLIDE DỰ PHÒNG (mở khi có câu hỏi) ═══════════════

// B1 · chất lượng nhãn toàn bộ so với mẫu thử
slide();
bar("Dự phòng · Chất lượng nhãn không suy giảm khi tăng quy mô");
table(M + 0.8, 1.0, [4.2, 2.0, 2.0], [
  { cells: ["Chỉ số", "Toàn bộ ngữ liệu", "Mẫu thử (n = 1.074)"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 12.5, align: ["left", "right", "right"] },
  { cells: ["Tên rõ ràng", "73,6%", "73,8%"], h: 0.42, fs: 13, rule: true },
  { cells: ["Chỉ có ký hiệu, không có chữ", "4,4%", "2,8%"], h: 0.42, fs: 13, rule: true },
  { cells: ["Không có tên", "22,0%", "23,4%"], h: 0.42, fs: 13, rule: true },
  { cells: ["Vai trò rõ ràng", "75,8%", "76,0%"], h: 0.42, fs: 13, rule: true },
  { cells: ["Trùng tên trên cùng màn", "7,6%", "7,0%"], h: 0.42, fs: 13, rule: true },
  { cells: ["Có phần tử cùng vai trò để so", "91,6%", "92,6%"], h: 0.42, fs: 13 },
], { align: ["left", "right", "right"] });
block(M, 4.1, W - 2 * M, 0.85);
text("Sáu chỉ số đều lệch không quá 1,6 điểm phần trăm giữa hai quy mô, mà mẫu thử nhỏ hơn 38 lần.", { x: M + 0.25, y: 4.1, w: 8.4, h: 0.85, fontSize: 13.5, bold: true, color: TEAL, valign: "middle", margin: 0 });
text("Mẫu thử là 1.074 nhãn được đọc tay để chấm đúng sai, giữ vai trò của một bộ ngữ liệu vàng, khác ở chỗ chúng tôi không sửa nhãn nào. Trong 32.061 tên lấy được, 8.581 đến từ cây trợ năng và 23.480 từ OCR, tỉ lệ 1 : 2,7, là hệ quả trực tiếp của con số 12,6%.", { x: M, y: 5.1, w: W - 2 * M, h: 0.9, fontSize: 12.5, margin: 0, lh: 1.3 });
NB("b1"); footB(); done();

// B2 · tỉ số 3,2 lần
slide();
bar("Dự phòng · Truy nguyên một tỉ số 3,2 lần");
text("Có giai đoạn chúng tôi đã định đảo thứ tự ưu tiên sang lấy tên từ OCR trước, vì đo thấy câu của người khớp với OCR gấp 3,2 lần khớp với nhãn trợ năng.", { x: M, y: 0.9, w: W - 2 * M, h: 0.55, fontSize: 13.5, margin: 0, lh: 1.3 });
bullets([
  "Tỉ số ấy chỉ dựng trên 72 nhãn mà hai nguồn cho hai chuỗi khác nhau, bằng 72/1.074 = 6,7% mẫu thử",
  "Bỏ tiếp 32 nhãn mà chuỗi chữ vốn đã nằm sẵn trong chuỗi mục tiêu của tác vụ, vì ở đó cả hai bên cùng lặp lại chuỗi mục tiêu",
  "Còn 40 nhãn: câu của người khớp OCR ở 12 trường hợp, khớp nhãn trợ năng ở 3, và 25 trường hợp không dùng chuỗi của bên nào",
  "Trong 12 trường hợp nghiêng về OCR thì 11 là do nhãn trợ năng ở đó vốn là chuỗi không dùng được, đúng loại mà bộ lọc về sau loại bỏ",
  "Khi cả hai nguồn đều cho chuỗi dùng được thì chỉ còn 1 trường hợp nghiêng về OCR so với 3 nghiêng về nhãn trợ năng",
], M + 0.1, 1.6, W - 2 * M - 0.2, { fs: 13, gap: 0.72, itemH: 0.7, lh: 1.3 });
block(M, 5.35, W - 2 * M, 0.95);
text("Ưu thế của OCR là ưu thế của việc lọc chuỗi không dùng được, không phải của thứ tự ưu tiên. Chúng tôi giữ nguyên thứ tự và thêm bộ lọc nhãn trợ năng.", { x: M + 0.25, y: 5.35, w: 8.4, h: 0.95, fontSize: 13.5, bold: true, color: NAVY, valign: "middle", margin: 0, lh: 1.3 });
NB("b2"); footB(); done();

// B3 · bốn nhánh dữ liệu
slide();
bar("Dự phòng · Bốn nhánh dữ liệu và chín bất biến cấu trúc");
text("Từ cùng một đầu vào, bốn tập chỉ khác nhau ở đầu ra mong đợi, tức phần văn bản mà mô hình phải học để sinh ra.", { x: M, y: 0.88, w: W - 2 * M, h: 0.4, fontSize: 13, margin: 0 });
table(M, 1.35, [1.6, 7.3], [
  { cells: ["Nhánh", "Đầu ra mong đợi"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12.5 },
  { cells: ["s1", "chỉ gồm câu chỉ dẫn; đây là nhánh đối chứng, ứng với cách huấn luyện thông thường"], h: 0.55, fs: 12.5, rule: true },
  { cells: ["s2", "dòng nhãn mô tả bốn ô đặt trước câu chỉ dẫn; đây là nhánh mà bộ ngữ liệu phục vụ"], h: 0.55, fs: 12.5, rule: true },
  { cells: ["s2r", "nhãn giả lấy từ màn hình khác, toạ độ ngẫu nhiên, chỉ giữ độ dài xấp xỉ nhãn thật"], h: 0.55, fs: 12.5, rule: true },
  { cells: ["s2_nopoint", "như s2 nhưng bỏ ô toạ độ"], h: 0.45, fs: 12.5 },
], { align: ["left", "left"] });
text("Nhánh s2r tồn tại để loại một cách giải thích thay thế: lợi ích của s2 chỉ đến từ việc đầu ra dài thêm. Bản ghép đầu khớp theo ký tự nên cho trung vị lệch 0 và trông như đã đạt, nhưng đo lại theo token thì chỉ 54% số cặp nằm trong hai token, biên độ trải từ −17 tới +14. Hàm mất mát tính trên token, nên phải làm lại theo token; sau đó 99,9% số cặp nằm trong hai token.", { x: M, y: 3.9, w: W - 2 * M, h: 1.1, fontSize: 12.5, margin: 0, lh: 1.3 });
block(M, 5.05, W - 2 * M, 1.2);
text("Bất biến quan trọng nhất: câu được chấm giống hệt nhau từng byte ở cả bốn nhánh, trên toàn bộ 64.567 mẫu, nên mọi chênh lệch quan sát được về sau chỉ có thể quy về phần đứng trước câu.", { x: M + 0.25, y: 5.05, w: 8.4, h: 1.2, fontSize: 13, valign: "middle", margin: 0, lh: 1.32 });
NB("b3"); footB(); done();

// B4 · bốn lỗi bắt được
slide();
bar("Dự phòng · Bốn lỗi bắt được lúc dựng dữ liệu");
text("Cả bốn đều xảy ra trong lúc mọi khâu vẫn chạy hết bình thường, chỉ có con số là sai.", { x: M, y: 0.9, w: W - 2 * M, h: 0.35, fontSize: 13.5, italic: true, color: GREY, margin: 0 });
table(M, 1.35, [4.4, 4.5], [
  { cells: ["Lỗi", "Kiểm định nào bắt được"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5 },
  { cells: ["Cây trợ năng lồng nhau đẩy chỉ số trùng tên lên 30%, trong khi giá trị thật trên mẫu thử là 7,0%", "đọc tay mẫu thử: cùng một nút bị đếm nhiều lần ở nhiều tầng của cây"], h: 0.95, fs: 12, rule: true },
  { cells: ["Tên lớp Android android.widget.TextView lọt vào ô tên phần tử", "đọc tay mẫu thử: chuỗi hợp lệ, đúng cú pháp, nhưng không hiển thị trên màn"], h: 0.85, fs: 12, rule: true },
  { cells: ["Ô dấu hiệu bản đầu chỉ giải quyết được 7,3% số trường hợp", "áp bảng phân loại bốn nhóm lên mẫu thử 1.074 nhãn"], h: 0.8, fs: 12, rule: true },
  { cells: ["Nhãn giả của s2r khớp độ dài theo ký tự, lệch tới ±17 token", "đo lại độ dài theo token, đúng đơn vị mà hàm mất mát dùng"], h: 0.8, fs: 12 },
], { align: ["left", "left"] });
block(M, 5.5, W - 2 * M, 0.8);
text("Thiếu những kiểm định ấy thì bộ ngữ liệu vẫn dựng xong, nhưng sai lệch sẽ còn nguyên trong giá trị của từng ô.", { x: M + 0.25, y: 5.5, w: 8.4, h: 0.8, fontSize: 13.5, bold: true, color: RED, valign: "middle", margin: 0 });
NB("b4"); footB(); done();

// B5 · chuỗi mục tiêu bị cắt
slide();
bar("Dự phòng · Chuỗi mục tiêu bị cắt ngay từ bản phát hành gốc");
text("Chuỗi mục tiêu là câu mô tả mục tiêu chung của cả tác vụ, chẳng hạn ...look for Calvin Kle", { x: M, y: 0.95, w: W - 2 * M, h: 0.4, fontSize: 13.5, margin: 0 });
[["99,4%", "trong 1.424 mục tiêu khác nhau của tập kiểm tra không kết thúc bằng một dấu câu"],
 ["71,3%", "là chặn dưới của tỉ lệ bị cắt ngay giữa một từ, nên chữ cuối chỉ còn là một mẩu không thành từ"]].forEach((c, i) => {
  const yy = 1.55 + i * 1.15;
  block(M, yy, W - 2 * M, 1.0);
  text(c[0], { x: M + 0.2, y: yy, w: 1.5, h: 1.0, fontSize: 22, bold: true, color: RED, align: "center", valign: "middle", margin: 0 });
  text(c[1], { x: M + 1.8, y: yy, w: 6.6, h: 1.0, fontSize: 13, valign: "middle", margin: 0, lh: 1.3 });
});
text("Chúng tôi nói “ít nhất” vì quy tắc đếm chỉ nhận những từ cuối không hề xuất hiện ở vị trí nào khác trong ngữ liệu, nên nó bỏ sót mọi trường hợp mà phần bị cắt tình cờ trùng một từ có thật.", { x: M, y: 3.95, w: W - 2 * M, h: 0.7, fontSize: 12.5, italic: true, color: GREY, margin: 0, lh: 1.3 });
block(M, 4.75, W - 2 * M, 1.45);
text("Phần thiếu mất ngay từ bản phát hành gốc chứ không mất trong khâu xử lý của chúng tôi, nên chúng tôi không khôi phục được. Bốn nhánh dữ liệu đều dùng chung đúng chuỗi đã bị cắt ấy, nên phần bị cắt là như nhau ở cả bốn và không tạo ra chênh lệch nào giữa chúng.", { x: M + 0.25, y: 4.75, w: 8.4, h: 1.45, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.35 });
NB("b5"); footB(); done();

// B6 · đạo đức và giấy phép
slide();
bar("Dự phòng · Nguồn, giấy phép và dữ liệu người dùng lẫn trong ảnh");
bullets([
  "AndroidControl phát hành theo giấy phép CC0, và chúng tôi không thu thập màn hình mới, nên không phát sinh vấn đề riêng tư ngoài những gì bản gốc đã xử lý",
  "Ảnh được ghi trong lúc người thật đang thao tác, nên chứa cả nội dung do người đó nhập vào, chẳng hạn địa chỉ thư điện tử hay tên riêng",
  "Những chuỗi ấy đi qua OCR, mà OCR là nguồn của cả ô tên lẫn ô dấu hiệu, nên chúng có thể đi thẳng vào nhãn",
  "Chúng tôi giữ nguyên theo bản gốc thay vì tự lọc, vì mọi quy tắc lọc tự động ở đây đều sẽ xoá nhầm một phần chữ hợp lệ trên giao diện",
], M + 0.1, 1.0, W - 2 * M - 0.2, { fs: 13.5, gap: 0.85, itemH: 0.82, lh: 1.32 });
block(M, 4.6, W - 2 * M, 1.6);
text("Phần tử không mang nhãn trợ năng vừa là khó khăn kỹ thuật của bài này, vừa là rào cản có thật với người dùng trình đọc màn hình. Trình đọc màn hình chỉ đọc được đúng 12,6% phần tử có nhãn, mà đây cũng là nhóm khó tự phát hiện mình đang bị chỉ sai nhất.", { x: M + 0.25, y: 4.6, w: 8.4, h: 1.6, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.35 });
NB("b6"); footB(); done();

// B7 · ba kiểm định còn lại
slide();
bar("Dự phòng · Ba kiểm định nội bộ còn lại");
[["Lối tắt theo độ dài bị loại trừ ngay từ cách dựng",
  "Nếu nhãn thật luôn dài hơn nhãn của phần tử cạnh tranh thì mô hình có thể tách hai bên chỉ bằng cách đếm độ dài, không cần đọc nội dung và không cần nhìn ảnh. Quy tắc “cứ chọn vế dài hơn” đoán đúng 43,2%, thấp hơn cả mức ngẫu nhiên 50%."],
 ["Quy trình không suy giảm khi tăng quy mô",
  "Sáu chỉ số chất lượng lệch không quá 1,6 điểm phần trăm giữa toàn bộ ngữ liệu và mẫu thử nhỏ hơn 38 lần."],
 ["Đổi khuôn mẫu nhãn sang tiếng Anh chỉ là thay đổi từ vựng",
  "So tổng số phép tính của một lượt huấn luyện trên hai bản: hai con số lệch nhau 0,03%. Tổng số phép tính tỉ lệ với độ dài chuỗi, nên độ dài chuỗi không đổi."]].forEach((c, i) => {
  const yy = 0.95 + i * 1.72;
  block(M, yy, W - 2 * M, 1.55);
  text(c[0], { x: M + 0.25, y: yy + 0.12, w: 8.4, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
  text(c[1], { x: M + 0.25, y: yy + 0.5, w: 8.4, h: 1.0, fontSize: 12.5, margin: 0, lh: 1.32 });
});
NB("b7"); footB(); done();

// B8 · quan hệ với bài đồng hành
slide();
bar("Dự phòng · Phần nằm ngoài phạm vi bài này");
text("Kết quả huấn luyện và đánh giá mô hình trên bộ ngữ liệu này thuộc một bài đồng hành của cùng nhóm tác giả, hiện đang bình duyệt.", { x: M, y: 0.95, w: W - 2 * M, h: 0.5, fontSize: 13.5, margin: 0, lh: 1.3 });
block(M, 1.6, W - 2 * M, 1.9);
text("Một quan sát ở bài đó liên quan trực tiếp tới giả định mà ô dấu hiệu phân biệt dựa vào", { x: M + 0.25, y: 1.72, w: 8.4, h: 0.35, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
text("Khi mô hình gọi sai tên phần tử, 76,5% số trường hợp có khoảng cách từ phần tử nó thực sự mô tả tới phần tử cần chạm nằm ngoài dải 80 đến 350 px đã dùng để dựng cặp quy chiếu.", { x: M + 0.25, y: 2.15, w: 8.4, h: 0.75, fontSize: 13, margin: 0, lh: 1.32 });
text("Với bài toán quy chiếu trên ngữ liệu này, phần khó không nằm ở việc phân biệt hai phần tử giống nhau, mà nằm ở chỗ nhiều phần tử không có sẵn chuỗi chữ nào để gọi tên.", { x: M + 0.25, y: 2.9, w: 8.4, h: 0.55, fontSize: 13, bold: true, color: RED, margin: 0, lh: 1.3 });
text("Cặp quy chiếu và dải 80 đến 350 px", { x: M, y: 3.75, w: W - 2 * M, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Một bước có cặp quy chiếu khi nhãn của phần tử cần chạm và nhãn của phần tử cạnh tranh gần nó nhất khác nhau ở cả ô tên lẫn ô toạ độ, và khoảng cách nằm trong dải 80 đến 350 px",
  "Mốc dưới đến từ khâu chấm điểm ở bài đồng hành, nơi hai phần tử cách nhau dưới 63 px trên màn rộng 1.080 px bị gộp làm một; 80 px là con số đó cộng một khoảng biên an toàn",
  "Mốc trên là bán kính tối đa của mỏ neo chữ. Đo trên 41.099 nhãn, 55,6% số bước có cặp quy chiếu",
], M + 0.1, 4.15, W - 2 * M - 0.2, { fs: 12.5, gap: 0.68, itemH: 0.66, lh: 1.25 });
NB("b8"); footB(); done();

// B9 · ví dụ nhãn thật
slide();
bar("Dự phòng · Bốn nhãn thật, đặt cạnh câu của người chú thích");
table(M, 0.95, [5.5, 3.4], [
  { cells: ["Nhãn tự động", "Câu của người chú thích"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5 },
  { cells: [{ t: "tappable text | Search here | <point>440,91</point> |\njust above the text “Coffee”", fs: 10.5 }, "Click on the search bar"], h: 0.95, fs: 12, rule: true },
  { cells: [{ t: "icon | (no name) | <point>256,524</point> |\njust above the text “Leaf”", fs: 10.5 }, "Choose the leaf option"], h: 0.9, fs: 12, rule: true },
  { cells: [{ t: "icon | Q | <point>920,899</point> |\nshares a name with 1 other elements on screen", fs: 10.5 }, "click on the search icon"], h: 0.9, fs: 12, rule: true },
  { cells: [{ t: "icon | (no name) | <point>920,904</point> |\nmany elements of the same kind on screen", fs: 10.5 }, "Click on the Right arrow key"], h: 0.9, fs: 12 },
], { align: ["left", "left"] });
text("Hai trường hợp đầu: mệnh đề ở ô thứ tư đủ chỉ ra phần tử nào là phần tử cần chạm, và người chú thích cũng chọn đúng chiến lược ấy khi gọi nó là leaf option.", { x: M, y: 5.15, w: W - 2 * M, h: 0.55, fontSize: 12.5, margin: 0, lh: 1.3 });
text("Hai trường hợp cuối: nhãn chỉ nói được rằng có mơ hồ, còn người chú thích gọi thẳng search icon và Right arrow key, vì họ nhìn thấy hình dạng của biểu tượng rồi đặt tên, còn quy trình chỉ đọc được chữ.", { x: M, y: 5.7, w: W - 2 * M, h: 0.6, fontSize: 12.5, color: RED, margin: 0, lh: 1.3 });
NB("b9"); footB(); done();

// B10 · vì sao dựng bằng quy tắc
slide();
bar("Dự phòng · Vì sao dựng nhãn bằng quy tắc");
bullets([
  "Nhãn dựng bằng quy tắc kiểm định lại được và dựng lại được: mỗi lần đọc tay thấy nhãn sai, thứ được sửa là bộ quy tắc, rồi toàn bộ 41.099 nhãn dựng lại từ đầu, chứ chúng tôi không sửa tay từng nhãn",
  "Chi phí thấp hơn nhiều bậc so với nhãn do người viết qua thu thập cộng đồng, nên phủ được quy mô lớn hơn hẳn",
  "Đổi lại thì nghèo hơn về chất lượng ngôn ngữ, mà khoảng cách ấy chúng tôi chưa định lượng được vì không có đánh giá bằng người",
  "Khi tên không kiểm chứng được, quy tắc để ô trống. Với dữ liệu huấn luyện, nhãn để trống chỉ làm mất một mẫu học, còn nhãn ghi tên sai thì dạy mô hình gọi phần tử bằng một chuỗi không tồn tại trên màn",
], M + 0.1, 1.0, W - 2 * M - 0.2, { fs: 13, gap: 0.95, itemH: 0.92, lh: 1.32 });
block(M, 4.85, W - 2 * M, 1.4);
text("Chen và cộng sự (2020) đi hướng ngược lại, dùng mô hình để bù nhãn trợ năng còn thiếu. Chúng tôi chấp nhận nhãn thiếu và chuyển nhiệm vụ quy chiếu sang quan hệ với chữ lân cận, nên chỗ nào không đọc được chữ thì nhãn nói rõ là không có tên, thay vì đoán một cái tên.", { x: M + 0.25, y: 4.85, w: 8.4, h: 1.4, fontSize: 13, valign: "middle", margin: 0, lh: 1.35 });
NB("b10"); footB(); done();

// B11 · bốn khuôn câu của ô dấu hiệu
slide();
bar("Dự phòng · Bốn khuôn câu của ô dấu hiệu phân biệt");
table(M, 0.95, [2.5, 3.6, 2.8], [
  { cells: ["Nhóm", "Khuôn câu", "Chức năng quy chiếu"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5 },
  { cells: ["Mỏ neo chữ", "just above / below,\nto the left / right of", { t: "giải quyết được mơ hồ", color: TEAL, bold: true }], h: 0.75, fs: 12, rule: true },
  { cells: ["Khẳng định duy nhất", "the only … on screen", { t: "giải quyết được mơ hồ", color: TEAL, bold: true }], h: 0.55, fs: 12, rule: true },
  { cells: ["Nêu trùng tên", "shares a name with …", { t: "chỉ nêu rằng có mơ hồ", color: RED }], h: 0.55, fs: 12, rule: true },
  { cells: ["Đếm số lượng", "k of n elements of the same kind", { t: "chỉ nêu rằng có mơ hồ", color: RED }], h: 0.55, fs: 12 },
], { align: ["left", "left", "left"] });
text("Vì bốn khuôn do chính quy tắc sinh nhãn tạo ra nên phép khớp là tất định, không có bước suy đoán nào. Nhưng cũng vì vậy, phép phân loại chỉ đếm loại mệnh đề mà quy tắc đã sinh, chứ tự nó không xác nhận mệnh đề ấy giúp một người dùng tìm ra phần tử.", { x: M, y: 3.9, w: W - 2 * M, h: 0.8, fontSize: 12.5, margin: 0, lh: 1.3 });
text("Hướng của mỏ neo", { x: M, y: 4.75, w: W - 2 * M, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Trong 27.628 mỏ neo chia cho bốn hướng, to the right of chiếm 8.382 còn to the left of chỉ 2.033; theo trục dọc thì hai hướng gần cân nhau",
  "Nhãn tả vị trí của phần tử cần chạm so với chữ neo, nên to the right of nghĩa là chữ dùng để neo nằm bên trái phần tử. Nhãn văn bản trên Android thường đặt bên trái phần tử thao tác, nên lệch này là hệ quả trực tiếp của quy ước bố cục",
], M + 0.1, 5.1, W - 2 * M - 0.2, { fs: 12.5, gap: 0.6, itemH: 0.58, lh: 1.25 });
NB("b11"); footB(); done();

// B12 · ngôn ngữ của ngữ liệu
slide();
bar("Dự phòng · Ngôn ngữ của ngữ liệu và khả năng chuyển sang miền khác");
bullets([
  "Ngữ liệu gốc AndroidControl là tiếng Anh, cả câu chỉ dẫn của người chú thích lẫn chữ hiển thị trên màn, nên nhãn cũng ở tiếng Anh cho khớp",
  "Khuôn mẫu nhãn do quy tắc sinh nên đổi ngôn ngữ khuôn được. Chúng tôi từng dựng bản khuôn tiếng Việt rồi chuyển sang tiếng Anh, và kiểm rằng đó chỉ là thay đổi về từ vựng bằng cách so tổng số phép tính của một lượt huấn luyện trên hai bản: lệch 0,03%, mà tổng số phép tính tỉ lệ với độ dài chuỗi",
  "Ô tên và ô dấu hiệu lấy từ chữ hiển thị trên màn, nên trên một giao diện tiếng Việt thì nhãn sẽ mang chữ tiếng Việt. Phần này chúng tôi chưa đo, vì chưa có ngữ liệu thao tác giao diện tiếng Việt có toạ độ chạm và câu chỉ dẫn theo bước",
  "Quy trình không phụ thuộc vào ngôn ngữ nào ngoài công cụ OCR, nên chỗ cần thay khi chuyển miền là bộ nhận dạng chữ và bảng quy tên lớp về vai trò",
], M + 0.1, 1.0, W - 2 * M - 0.2, { fs: 13, gap: 1.05, itemH: 1.02, lh: 1.32 });
block(M, 5.4, W - 2 * M, 0.85);
text("Chỗ khó nhất khi chuyển miền không phải ngôn ngữ, mà là những phần tử không có sẵn chuỗi chữ nào để gọi tên, vì đó là chỗ nhãn phải suy từ hình vẽ.", { x: M + 0.25, y: 5.4, w: 8.4, h: 0.85, fontSize: 13, valign: "middle", margin: 0, lh: 1.3 });
NB("b12"); footB(); done();

// B13 · bản ghi có gì
slide();
bar("Dự phòng · Một bản ghi của GUIRefCorpus có gì");
text("41.099 dòng ở tập huấn luyện và 4.448 dòng ở tập kiểm tra, mỗi dòng ứng với một bước chạm, lưu ở dạng mỗi dòng một bản ghi JSON.", { x: M, y: 0.9, w: W - 2 * M, h: 0.5, fontSize: 13.5, margin: 0, lh: 1.3 });
bullets([
  "Dòng nhãn bốn ô đã ghép sẵn, và riêng từng ô: vai trò, tên, nguồn của tên, tầng tên, toạ độ đã chuẩn hoá, hộp bao, dấu hiệu phân biệt",
  "Hai cờ cho biết phần tử có trùng tên hoặc trùng vai trò với phần tử khác trên cùng màn hay không",
  "Một nhãn đối chứng dựng trên phần tử hàng xóm, dùng cho các nhánh dữ liệu ở phụ lục",
  "Khoá episode_id và step_id để nối ngược về bước gốc của AndroidControl",
], M + 0.1, 1.5, W - 2 * M - 0.2, { fs: 13, gap: 0.72, itemH: 0.7, lh: 1.3 });
block(M, 4.45, W - 2 * M, 1.75);
text("Ảnh màn hình không đi kèm bản ghi, vì bản phát hành AndroidControl đã cung cấp sẵn theo giấy phép CC0 và bản ghi nối về được bằng khoá. Ảnh được ghi trong lúc người thật thao tác nên có thể chứa nội dung do người đó nhập vào; chuỗi ấy đi qua OCR nên có thể vào nhãn, và chúng tôi giữ nguyên theo bản gốc thay vì tự lọc, bởi mọi quy tắc lọc tự động đều sẽ xoá nhầm một phần chữ hợp lệ trên giao diện.", { x: M + 0.25, y: 4.45, w: 8.4, h: 1.75, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.35 });
NB("b13"); footB(); done();

// ---- xuất ----
done();
pres.writeFile({ fileName: "../VCL2026_SLIDE.pptx" }).then(() => {
  const html = `<!doctype html><meta charset="utf-8"><title>Preview - slide VCL2026</title>
<style>body{background:#555;margin:0;padding:24px;font-family:sans-serif}
.slide{position:relative;width:960px;height:720px;margin:0 auto 24px;box-shadow:0 3px 14px rgba(0,0,0,.5);overflow:hidden}</style>
${htmlSlides.join("\n")}`;
  fs.mkdirSync("_preview", { recursive: true });
  fs.writeFileSync("_preview/preview_vcl.html", html);
  console.log("Xong: ../VCL2026_SLIDE.pptx  |  slide chinh: " + PAGE + "  |  du phong: " + BPAGE);
});
