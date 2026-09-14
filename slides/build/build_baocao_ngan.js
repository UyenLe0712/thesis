// Deck BÁO CÁO NGẮN (9/9/2026) - 3 slide: bìa, phương pháp, kết quả. Dùng lại nguyên style deck bảo vệ.
// Style giữ nguyên bản 16/8: khổ 4:3, thanh tiêu đề chàm, khối xám bo góc, chữ serif, footline 4 ô.
// Nội dung lấy từ thesis/chapters (bản 9/9, có chặng ba và nội suy) + CLAUDE.md. Xuất: ../LUAN_VAN_SLIDE_BAOCAO.pptx
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.defineLayout({ name: "A43", width: 10, height: 7.5 });
pres.layout = "A43";
pres.author = "Le Doan Phuong Uyen";
pres.title = "Phat sinh tu dong huong dan su dung phan mem dua tren LLM - bao cao ngan";

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
let s, PAGE = 0, BPAGE = 0, TOTAL = 3;
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
  text("Luận văn thạc sĩ", { x: 0, y: yy, w: 3.0, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0, fontFace: MONO });
  text("Phát sinh tự động hướng dẫn sử dụng phần mềm dựa trên LLM", { x: 3.0, y: yy, w: 3.7, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
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

function N(i) { }

// ══════════ 1 · BÌA ══════════
slide();
rect(0, 0, W, 0.66, NAVY);
text("ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH  -  TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN", { x: 0, y: 0, w: W, h: 0.66, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
rect(0.8, 1.2, W - 1.6, 2.45, NAVY, { radius: 0.09, shadow: true });
text("Luận văn thạc sĩ  -  Ngành Trí tuệ nhân tạo", { x: 0.8, y: 1.5, w: W - 1.6, h: 0.4, fontSize: 15, bold: true, color: WHITE, align: "center", margin: 0 });
text("PHÁT SINH TỰ ĐỘNG HƯỚNG DẪN SỬ DỤNG PHẦN MỀM\nDỰA TRÊN LLM TỪ CÁC TRƯỜNG HỢP SỬ DỤNG\nVÀ GIAO DIỆN NGƯỜI DÙNG", { x: 0.8, y: 1.95, w: W - 1.6, h: 1.6, fontSize: 21, bold: true, color: WHITE, align: "center", margin: 0, lh: 1.25 });
text("LLM-Based Automatic Generation of Software User Guides from Use Cases and Front-End Structures", { x: 0.8, y: 3.75, w: W - 1.6, h: 0.35, fontSize: 12, italic: true, color: GREY, align: "center", margin: 0 });
text("Học viên thực hiện:   Lê Đoàn Phương Uyên", { x: 0.8, y: 4.4, w: W - 1.6, h: 0.4, fontSize: 15, bold: true, align: "center", margin: 0 });
text("Giáo viên hướng dẫn:   TS. Nguyễn Hồng Bửu Long", { x: 0.8, y: 4.85, w: W - 1.6, h: 0.4, fontSize: 15, bold: true, align: "center", margin: 0 });
text("Mã số ngành: 8480107", { x: 0.8, y: 5.45, w: W - 1.6, h: 0.35, fontSize: 12, color: GREY, align: "center", margin: 0 });
text("TP. Hồ Chí Minh  -  Năm 2026", { x: 0.8, y: 5.85, w: W - 1.6, h: 0.35, fontSize: 12, align: "center", margin: 0 });
foot(); done();


// ══════════ 2 · PHƯƠNG PHÁP ══════════
slide();
bar("Phương pháp: mô tả phân biệt trước, phát ngôn sau");
block(M, 0.85, W - 2 * M, 1.15);
text("Đích sinh của mô hình", { x: M + 0.25, y: 0.92, w: 3.0, h: 0.3, fontSize: 12.5, bold: true, color: NAVY, margin: 0 });
text("<desc>vai trò | tên gọi | <point>x,y</point> | dấu hiệu phân biệt</desc>", { x: M + 0.25, y: 1.22, w: W - 2 * M - 0.5, h: 0.3, fontSize: 12.5, fontFace: MONO, color: BLUE, margin: 0 });
text("rồi xuống dòng, rồi câu hướng dẫn cho người đọc.   Khi chấm chỉ lấy câu, phần mô tả bị cắt bỏ.", { x: M + 0.25, y: 1.55, w: W - 2 * M - 0.5, h: 0.35, fontSize: 12.5, margin: 0 });

[["1", "Tinh chỉnh có giám sát", "S1 chỉ sinh câu. S2 sinh dòng mô tả trước rồi mới sinh câu, để mô hình phải chọn phần tử trước khi viết.", TEAL],
 ["2", "Học theo ưu tiên trên cặp quy chiếu tối thiểu", "Hai vế của một cặp trùng nhau từng ký tự ở phần câu, chỉ khác đúng ô mô tả, nên phần điều chỉnh dồn vào việc chọn phần tử. Kèm nhánh so sánh học thêm đúng bấy nhiêu bước bằng cách thường, để tách công.", NAVY],
 ["3", "Học tăng cường thưởng cho ô toạ độ", "Mỗi câu nhắc sinh bốn phương án, thưởng 1,0 khi ô toạ độ lệch không quá 140 trên lưới 1000. Không có mô hình định vị nào trong phần thưởng, nên không tối ưu thẳng vào thước chấm.", NAVY]].forEach(function (n, i) {
  var yy = 2.2 + i * 1.42;
  block(M, yy, W - 2 * M, 1.3);
  text(n[0], { x: M + 0.14, y: yy + 0.14, w: 0.42, h: 0.42, fontSize: 21, bold: true, color: n[3], align: "center", margin: 0 });
  text(n[1], { x: M + 0.62, y: yy + 0.14, w: W - 2 * M - 0.85, h: 0.34, fontSize: 14, bold: true, color: n[3], margin: 0 });
  text(n[2], { x: M + 0.62, y: yy + 0.52, w: W - 2 * M - 0.85, h: 0.72, fontSize: 12.5, margin: 0, lh: 1.3 });
});
text("Cả ba chặng trên cùng một mô hình nền Qwen2.5-VL ba tỉ tham số, tinh chỉnh bằng ma trận hạng thấp.", { x: M, y: 6.52, w: W - 2 * M, h: 0.35, fontSize: 11.5, italic: true, color: GREY, margin: 0 });
foot(); done();

// ══════════ 3 · KẾT QUẢ ══════════
slide();
bar("Kết quả dưới luật hộp phần tử, trên 4.463 bước chạm");
text("Luật chấm gốc của chính bộ dữ liệu AndroidControl: điểm dự đoán rơi vào bên trong khung của phần tử đúng thì tính trúng.", { x: M, y: 0.72, w: W - 2 * M, h: 0.32, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.2, [5.3, 1.95, 1.64], [
  { cells: ["Nhánh", "Hộp phần tử", ""], bold: true, color: WHITE, fill: NAVY, h: 0.44, fs: 13, align: ["left", "center", "center"] },
  { cells: [{ t: "Câu chuẩn của người chú thích  (trần)", italic: true }, { t: "83,82", bold: true, color: TEAL }, ""], h: 0.48, fs: 13.5, rule: "322164", ruleW: 1.5 },
  { cells: ["Mô hình gốc, chưa tinh chỉnh", "53,60", ""], h: 0.44, fs: 13.5, rule: true },
  { cells: ["S1, chỉ sinh câu, hạt giống 101", "65,49", ""], h: 0.44, fs: 13.5, rule: true },
  { cells: ["S1, hạt giống 202", "66,10", ""], h: 0.44, fs: 13.5, rule: "322164", ruleW: 1.5 },
  { cells: ["S2, sinh mô tả trước", "63,63", { t: "một hạt giống", color: MAROON, italic: true, fs: 11 }], h: 0.44, fs: 13.5, rule: true },
  { cells: ["Nhánh so sánh của chặng hai", "66,03", { t: "một hạt giống", color: MAROON, italic: true, fs: 11 }], h: 0.44, fs: 13.5, rule: true },
  { cells: ["Chặng hai, cặp quy chiếu tối thiểu", "66,55", { t: "một hạt giống", color: MAROON, italic: true, fs: 11 }], h: 0.44, fs: 13.5, rule: true },
  { cells: [{ t: "Chặng ba, thưởng ô toạ độ", bold: true }, { t: "67,04", bold: true, color: NAVY }, { t: "một hạt giống", color: MAROON, italic: true, fs: 11 }], h: 0.46, fs: 13.5 },
], { align: ["left", "center", "center"] });
block(M, 5.35, W - 2 * M, 1.05);
bullets([
  [{ text: "Tinh chỉnh đáng ", options: {} }, { text: "11,89 điểm", options: { bold: true } }, { text: " so với mô hình gốc, lặp lại ở cả hai hạt giống", options: {} }],
  [{ text: "Thứ tự các nhánh không đổi một chỗ nào so với thước chính; khoảng cách còn lại tới câu chuẩn là ", options: {} }, { text: "16,8 điểm", options: { bold: true } }],
], M + 0.2, 5.42, W - 2 * M - 0.4, { fs: 13, gap: 0.5, itemH: 0.46, lh: 1.22 });
text("Luật này được tính lại từ bản ghi từng bước sau khi đã có mọi điểm, nên trình như thước báo kèm; con số của thước chính báo riêng.", { x: M, y: 6.55, w: W - 2 * M, h: 0.35, fontSize: 11, italic: true, color: GREY, margin: 0 });
foot(); done();

// ---- xuất ----
done();
pres.writeFile({ fileName: "../BAO_CAO_NGAN.pptx" }).then(function () {
  var html = '<!doctype html><meta charset="utf-8"><title>Preview - bao cao ngan</title>'
    + '<style>body{background:#555;margin:0;padding:24px;font-family:sans-serif}'
    + '.slide{position:relative;width:960px;height:720px;margin:0 auto 24px;box-shadow:0 3px 14px rgba(0,0,0,.5);overflow:hidden}</style>'
    + htmlSlides.join("\n");
  fs.mkdirSync("_preview", { recursive: true });
  fs.writeFileSync("_preview/preview_baocao_ngan.html", html);
  console.log("Xong: ../BAO_CAO_NGAN.pptx  |  so slide: " + PAGE);
});
