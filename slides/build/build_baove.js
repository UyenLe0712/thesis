// Deck BẢO VỆ (cập nhật 9/9/2026, lượt hai) - 29 slide chính + 15 slide dự phòng, nhắm 25 phút.
// Style giữ nguyên bản 16/8: khổ 4:3, thanh tiêu đề chàm, khối xám bo góc, chữ serif, footline 4 ô.
// Nội dung lấy từ thesis/chapters (bản 9/9, có chặng ba và nội suy) + CLAUDE.md. Xuất: ../LUAN_VAN_SLIDE_BAOCAO.pptx
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.defineLayout({ name: "A43", width: 10, height: 7.5 });
pres.layout = "A43";
pres.author = "Le Doan Phuong Uyen";
pres.title = "Phat sinh tu dong huong dan su dung phan mem dua tren LLM - bao ve luan van";

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
let s, PAGE = 0, BPAGE = 0, TOTAL = 29;
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

const NOTES = require("./notes_baove.json");
function N(i) { if (NOTES[String(i)]) note(NOTES[String(i)]); }

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
N(1); foot(); done();

// ══════════ 2 · NỘI DUNG ══════════
slide();
bar("Nội dung trình bày");
["Bài toán và hai vấn đề",
 "Dữ liệu và nhãn dựng tự động",
 "Phương pháp: mô tả trước, phát ngôn sau",
 "Thước đo executability",
 "Kết quả và phân tích lỗi",
 "Hạn chế và hướng phát triển"].forEach((t, i) => {
  text([{ text: (i + 1) + ".", options: { bold: true, color: TEAL } }, { text: "   " + t, options: { bold: true, color: NAVY } }], { x: 1.7, y: 1.95 + i * 0.66, w: 7.2, h: 0.5, fontSize: 17, margin: 0 });
});
N(2); foot(); done();

// ══════════ 3 · BÀI TOÁN ══════════
slide();
bar("1 · Bài toán: đầu ra là câu chữ, không phải toạ độ");
block(M, 0.9, W - 2 * M, 1.5);
text([{ text: "Đầu vào.  ", options: { bold: true, color: BLUE } }, { text: "ảnh màn hình  +  “Chia sẻ playlist này cho bạn tôi”", options: { italic: true } }], { x: M + 0.25, y: 1.05, w: W - 2 * M - 0.5, h: 0.5, fontSize: 15, margin: 0 });
text([{ text: "Kết quả.  ", options: { bold: true, color: BLUE } }, { text: "“Tap the share icon at the top right of the screen.”", options: { italic: true } }], { x: M + 0.25, y: 1.72, w: W - 2 * M - 0.5, h: 0.5, fontSize: 15, margin: 0 });
text("Tác tử giao diện", { x: M, y: 2.75, w: 4.35, h: 0.4, fontSize: 15, bold: true, color: NAVY, align: "center", margin: 0 });
text("Luận văn này", { x: 5.1, y: 2.75, w: 4.35, h: 0.4, fontSize: 15, bold: true, color: RED, align: "center", margin: 0 });
block(M, 3.2, 4.35, 2.35); block(5.1, 3.2, 4.35, 2.35);
text("Đầu ra là lệnh máy tự bấm,\ndạng click(872, 141).\n\nCâu chữ không được đem chấm.", { x: M + 0.25, y: 3.5, w: 3.9, h: 1.8, fontSize: 14.5, margin: 0, lh: 1.45 });
text("Đầu ra là câu cho người đọc.\n\nCâu là thứ duy nhất\nđược đem chấm.", { x: 5.35, y: 3.5, w: 3.9, h: 1.8, fontSize: 14.5, margin: 0, lh: 1.45 });
text("SeeClick · OS-Atlas · Aguvis", { x: M, y: 5.65, w: 4.35, h: 0.35, fontSize: 11, italic: true, color: GREY, align: "center", margin: 0 });
text("Mô hình ba tỉ tham số, chạy tại máy người dùng", { x: 5.1, y: 5.65, w: 4.35, h: 0.35, fontSize: 11, italic: true, color: GREY, align: "center", margin: 0 });
N(3); foot(); done();

// ══════════ 4 · HAI VẤN ĐỀ ══════════
slide();
bar("1 · Đổi đầu ra kéo theo hai vấn đề");
text("Vấn đề 1 · Không chấm được câu", { x: M, y: 0.9, w: 4.35, h: 0.4, fontSize: 15, bold: true, color: NAVY, align: "center", margin: 0 });
text("Vấn đề 2 · Dạng lỗi không như dự đoán", { x: 5.1, y: 0.9, w: 4.35, h: 0.4, fontSize: 15, bold: true, color: NAVY, align: "center", margin: 0 });
block(M, 1.4, 4.35, 3.4); block(5.1, 1.4, 4.35, 3.4);
text("Một nút có nhiều tên gọi đều đúng.", { x: M + 0.22, y: 1.55, w: 4.0, h: 0.4, fontSize: 13, italic: true, margin: 0 });
bullets([
  [{ text: "So khớp chuỗi loại nhầm ", options: {} }, { text: "97,5%", options: { bold: true, color: RED } }, { text: " số câu diễn đạt khác", options: {} }],
  [{ text: "So vector ngữ nghĩa: AUC ", options: {} }, { text: "0,336", options: { bold: true, color: RED } }, { text: ", kém đoán ngẫu nhiên", options: {} }],
  "inbox / outbox được 0,76, còn search / magnifying glass chỉ 0,55",
], M + 0.22, 2.1, 4.0, { fs: 13, gap: 0.85, itemH: 0.8, lh: 1.3 });
text("Đọc tay 40 trường hợp sinh sai.", { x: 5.32, y: 1.55, w: 4.0, h: 0.4, fontSize: 13, italic: true, margin: 0 });
bullets([
  [{ text: "Bịa ra nút không có trên màn: ", options: {} }, { text: "0 đến 2%", options: { bold: true, color: TEAL } }],
  [{ text: "Phần lớn là ", options: {} }, { text: "câu mơ hồ", options: { bold: true, color: RED } }, { text: ": “biểu tượng tìm kiếm” khi màn hình có hai biểu tượng như vậy", options: {} }],
  "Câu không sai sự thật, nhưng người đọc vẫn không biết chạm đâu",
], 5.32, 2.1, 4.0, { fs: 13, gap: 0.85, itemH: 0.8, lh: 1.3 });
block(M, 5.1, W - 2 * M, 1.1);
text([{ text: "Chỗ đáng sửa là tính phân biệt của câu, ", options: { bold: true, color: RED } }, { text: "không phải việc chống bịa đặt.", options: {} }], { x: M + 0.25, y: 5.1, w: W - 2 * M - 0.5, h: 1.1, fontSize: 15, valign: "middle", margin: 0 });
N(4); foot(); done();

// ══════════ 5 · NGHIÊN CỨU LIÊN QUAN ══════════
slide();
bar("1 · Công trình liên quan");
table(M, 1.0, [2.9, 3.0, 3.0], [
  { cells: ["Công trình", "Họ làm gì", "Luận văn khác đi"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 13 },
  { cells: ["SeeClick, OS-Atlas,\nAguvis", "Sinh toạ độ cho máy tự bấm", "Câu là sản phẩm cuối, và là thứ đem chấm"], h: 0.85, fs: 12.5, rule: true },
  { cells: ["AndroidControl\nNeurIPS 2024", "Câu chuẩn là đầu vào", "Dùng chính câu đó làm đầu ra mong đợi"], h: 0.85, fs: 12.5, rule: true },
  { cells: ["Sinh biểu thức quy chiếu\nMao 2016 · Yu 2017", "Câu phải đủ để bên kia trỏ đúng", "Đặt yêu cầu đó vào miền giao diện"], h: 0.85, fs: 12.5, rule: true },
  { cells: ["Widget Captioning\nEMNLP 2020", "Sinh mô tả, entropy chéo thuần", "Tính phân biệt nằm trong mục tiêu huấn luyện"], h: 0.85, fs: 12.5, rule: true },
  { cells: ["Zhao và cộng sự\nEACL 2021", "BLEU, ROUGE không đo được hướng dẫn có định vị", "Căn cứ để bỏ nhóm thước đồng thuận"], h: 0.9, fs: 12.5 },
], { align: ["left", "left", "left"] });
block(M, 5.55, W - 2 * M, 0.65);
text("Luận văn không dùng chữ “đầu tiên”: ý này đã có từ năm 2016.", { x: M + 0.25, y: 5.55, w: W - 2 * M - 0.5, h: 0.65, fontSize: 13, bold: true, color: RED, valign: "middle", margin: 0 });
N(5); foot(); done();

// ══════════ 6 · BA ĐÓNG GÓP ══════════
slide();
bar("1 · Ba đóng góp và trạng thái thật của từng đóng góp");
[["1", "Thước đo executability", "Kiểm chứng bằng sáu khối phép đo.", "HOÀN TẤT", TEAL],
 ["2", "Đường ống dữ liệu và kết quả thực nghiệm có nhánh so sánh", "Nhánh xử lý chỉ chạy được một hạt giống vì ngân sách máy.", "MỘT HẠT GIỐNG", RED],
 ["3", "Phân tích lỗi ở mức từng bước", "Cơ chế đúng, nhưng bị chặn bởi độ chính xác khai báo. Nhánh ứng viên nối tiếp: điểm nghẽn mới là bỏ cuộc quá mức.", "HOÀN TẤT", TEAL]].forEach((c, i) => {
  const yy = 1.05 + i * 1.65;
  block(M, yy, W - 2 * M, 1.4);
  text(c[0], { x: M + 0.15, y: yy + 0.15, w: 0.5, h: 0.55, fontSize: 26, bold: true, color: NAVY, align: "center", margin: 0 });
  text(c[1], { x: M + 0.72, y: yy + 0.18, w: 5.5, h: 0.45, fontSize: 15, bold: true, color: NAVY, margin: 0, lh: 1.15 });
  text(c[3], { x: W - M - 2.4, y: yy + 0.18, w: 2.2, h: 0.35, fontSize: 12.5, bold: true, color: c[4], align: "right", margin: 0 });
  text(c[2], { x: M + 0.72, y: yy + 0.78, w: W - 2 * M - 0.95, h: 0.5, fontSize: 13.5, margin: 0 });
});
N(6); foot(); done();

// ══════════ 7 · DỮ LIỆU ══════════
slide();
bar("2 · Dữ liệu: dựng bằng máy, không thuê người dán nhãn");
text("Ghép hai kho công khai theo khoá (episode_id, step_id): câu chuẩn và cây trợ năng từ kho thứ nhất, ảnh màn hình từ kho thứ hai.", { x: M, y: 0.9, w: W - 2 * M, h: 0.5, fontSize: 13, margin: 0, lh: 1.3 });
table(M + 0.5, 1.6, [2.6, 2.2, 2.2, 1.6], [
  { cells: ["Tập", "Số bước", "Bước chạm", "Tác vụ"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 13, align: ["left", "center", "center", "center"] },
  { cells: ["Huấn luyện", "64.567", "41.191", "12.895"], h: 0.42, fs: 13.5, rule: true },
  { cells: [{ t: "Kiểm tra", bold: true }, { t: "6.958", bold: true }, { t: "4.463", bold: true }, { t: "1.432", bold: true }], h: 0.42, fs: 13.5 },
], { align: ["left", "center", "center", "center"] });
text("Ba phép kiểm bảo vệ phần này", { x: M, y: 3.15, w: W - 2 * M, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
bullets([
  [{ text: "Phép ghép khớp ", options: {} }, { text: "48%", options: { bold: true, color: TEAL } }, { text: ", phép ghép cố ý lệch một bước chỉ ", options: {} }, { text: "20%", options: { bold: true, color: RED } }],
  [{ text: "Chín bất biến cấu trúc đều đạt: ", options: {} }, { text: "9/9", options: { bold: true, color: TEAL } }],
  [{ text: "Rò rỉ dạy và kiểm: ", options: {} }, { text: "không tác vụ nào trùng", options: { bold: true, color: TEAL } }],
], M + 0.15, 3.6, W - 2 * M - 0.3, { fs: 13.5, gap: 0.55, itemH: 0.5, lh: 1.2 });
block(M, 5.4, W - 2 * M, 0.8);
text("Nhãn không do người dán, cũng không lấy từ một mô hình ngôn ngữ khác.", { x: M + 0.25, y: 5.4, w: W - 2 * M - 0.5, h: 0.8, fontSize: 13.5, valign: "middle", margin: 0 });
N(7); foot(); done();

// ══════════ 8 · NHÃN MÔ TẢ ══════════
slide();
bar("2 · Nhãn mô tả tự động cho phần tử người dùng đã chạm");
block(M, 0.95, W - 2 * M, 0.7);
text([{ text: "Mỗi nhãn gồm bốn ô:   ", options: { bold: true, color: NAVY } }, { text: "vai trò  |  tên  |  toạ độ chạm  |  dấu hiệu phân biệt", options: { bold: true, color: BLUE } }], { x: M + 0.25, y: 0.95, w: W - 2 * M - 0.5, h: 0.7, fontSize: 14, valign: "middle", margin: 0 });
text("Vì sao phải tự dựng ô tên", { x: M, y: 1.9, w: 4.4, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
bullets([
  "Cây trợ năng có 86 phần tử mỗi màn, chỉ 12,6% có tên",
  "Trích chữ trên ảnh bù vào, phủ 100% số bước",
  "Hai bộ lọc thêm: nhãn rác 14,7% và phần tử quá 25% màn",
], M, 2.35, 4.4, { fs: 13, gap: 0.85, itemH: 0.8, lh: 1.3 });
text("Chất lượng ô tên", { x: 5.1, y: 1.9, w: 4.35, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
table(5.1, 2.35, [3.05, 1.3], [
  { cells: ["Có tên dùng được", "73,6%"], h: 0.48, fs: 13.5, rule: true },
  { cells: [{ t: "Không có tên nào", color: RED }, { t: "22,0%", color: RED }], h: 0.48, fs: 13.5, rule: true },
  { cells: [{ t: "Trùng tên với phần tử khác", color: RED }, { t: "7,6%", color: RED }], h: 0.48, fs: 13.5 },
], { align: ["left", "right"] });
block(M, 5.05, W - 2 * M, 1.15);
text([{ text: "Ô toạ độ lấy ngay chỗ người thật đã chạm: ", options: { bold: true, color: RED } }, { text: "nhãn sạch 100%, chi phí bằng không, và đây cũng là chuẩn để chấm điểm.", options: {} }], { x: M + 0.25, y: 5.05, w: W - 2 * M - 0.5, h: 1.15, fontSize: 14, valign: "middle", margin: 0, lh: 1.35 });
N(8); foot(); done();

// ══════════ 9 · PHƯƠNG PHÁP ══════════
slide();
bar("3 · Thành phần đề xuất: mô tả phân biệt trước, phát ngôn sau");
block(M, 0.95, W - 2 * M, 1.35);
text([{ text: "tầng khai báo   ", options: { italic: true, color: GREY } }, { text: "<desc> vai trò | tên | <point>x,y</point> | dấu hiệu phân biệt </desc>", options: { fontFace: MONO, color: BLUE, bold: true } }], { x: M + 0.3, y: 1.2, w: W - 2 * M - 0.5, h: 0.4, fontSize: 12, margin: 0 });
text([{ text: "tầng phát ngôn   ", options: { italic: true, color: GREY } }, { text: "câu hướng dẫn cho người đọc", options: { fontFace: MONO, color: INK, bold: true } }], { x: M + 0.3, y: 1.7, w: W - 2 * M - 0.5, h: 0.4, fontSize: 12, margin: 0 });
text([{ text: "Lúc chấm, tầng khai báo bị cắt bỏ; chỉ câu đi chấm.", options: { bold: true, color: RED } }, { text: "\nVì vậy đây là đóng góp về mô hình, không phải về dữ liệu.", options: {} }], { x: M, y: 2.5, w: W - 2 * M, h: 0.8, fontSize: 14, margin: 0, lh: 1.35 });
text("Ba căn cứ cho thiết kế", { x: M, y: 3.5, w: W - 2 * M, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
bullets([
  "Dạng lỗi đo được là câu mơ hồ",
  [{ text: "Bước trung gian phải có toạ độ: cặp Shikra cho ", options: {} }, { text: "−7,4", options: { bold: true, color: RED } }, { text: " và ", options: {} }, { text: "+5,9", options: { bold: true, color: TEAL } }],
  "Nhãn toạ độ sạch 100% và dựng không tốn gì",
], M + 0.15, 3.95, W - 2 * M - 0.3, { fs: 13.5, gap: 0.62, itemH: 0.58, lh: 1.25 });
block(M, 5.85, W - 2 * M, 0.6);
text("Qwen2.5-VL-3B  ·  QLoRA 4 bit  ·  đóng băng phần thị giác  ·  8.072 bước  ·  23 giờ A100", { x: M + 0.25, y: 5.85, w: W - 2 * M - 0.5, h: 0.6, fontSize: 12, valign: "middle", margin: 0 });
N(9); foot(); done();

// ══════════ 10 · CHẶNG HAI ══════════
slide();
bar("3 · Chặng huấn luyện thứ hai: mục tiêu ưu tiên ở tầng khai báo");
text("Điểm nghẽn nằm ở độ chính xác của tầng khai báo, không ở việc có tầng ấy hay không.", { x: M, y: 0.85, w: W - 2 * M, h: 0.4, fontSize: 13.5, margin: 0 });
text("Cặp quy chiếu tối thiểu, 22.854 cặp", { x: M, y: 1.5, w: W - 2 * M, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
rect(M, 1.92, W - 2 * M, 1.05, "FFFFFF", { line: "9A94AE" });
text([{ text: "được chọn    ", options: { color: TEAL, bold: true } }, { text: "<desc>khai báo ĐÚNG</desc>  +  câu", options: { fontFace: MONO } }], { x: M + 0.25, y: 2.02, w: W - 2 * M - 0.5, h: 0.42, fontSize: 12.5, margin: 0 });
text([{ text: "bị loại        ", options: { color: RED, bold: true } }, { text: "<desc>khai báo SAI</desc>  +  đúng câu đó, từng chữ", options: { fontFace: MONO } }], { x: M + 0.25, y: 2.48, w: W - 2 * M - 0.5, h: 0.42, fontSize: 12.5, margin: 0 });
bullets([
  "Hai vế chỉ khác ô khai báo, nên gradient rơi vào việc chọn phần tử",
  "Khai báo sai là một phần tử thật trên chính màn hình đó",
  "Mục tiêu dạng tỉ số odds, không cần mô hình tham chiếu",
], M + 0.15, 3.15, W - 2 * M - 0.3, { fs: 13.5, gap: 0.62, itemH: 0.58, lh: 1.25 });
block(M, 5.15, W - 2 * M, 1.05);
text([{ text: "Nhánh so sánh CE2-S2 tách phần công của mục tiêu ưu tiên:", options: { bold: true, color: RED } }, { text: " cùng điểm lưu, cùng 800 bước, không có số hạng ưu tiên.", options: {} }], { x: M + 0.25, y: 5.15, w: W - 2 * M - 0.5, h: 1.05, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.35 });
N(10); foot(); done();

// ══════════ 11 · THƯỚC ĐO ══════════
slide();
bar("4 · Thước đo executability");
text("Đưa câu cho một mô hình định vị độc lập, rồi hỏi điểm nó trả về có rơi đúng phần tử người dùng đã chạm hay không.", { x: M, y: 0.85, w: 4.5, h: 0.75, fontSize: 13, margin: 0, lh: 1.3 });
text("Một bước tính đúng khi cả ba điều kiện cùng thoả", { x: M, y: 1.75, w: 4.5, h: 0.32, fontSize: 13, bold: true, color: NAVY, margin: 0 });
[["(i)", "Khớp loại thao tác", "Chạm, gõ, cuộn, nhấn giữ, quay lại."],
 ["(ii)", "Không đảo nghĩa", "Bật và tắt nằm cùng một chỗ chạm."],
 ["(iii)", "Định vị đúng", "Điểm dự đoán nằm trong dung sai 14%, và không phần tử nào khác gần nó hơn chỗ người dùng đã chạm."]].forEach((c, i) => {
  const yy = 2.2 + i * 1.25;
  rect(M, yy, 4.5, 1.15, BLOCK, { radius: 0.05 });
  text(c[0], { x: M + 0.12, y: yy + 0.08, w: 0.5, h: 0.3, fontSize: 12.5, bold: true, color: TEAL, margin: 0 });
  text(c[1], { x: M + 0.62, y: yy + 0.08, w: 3.7, h: 0.3, fontSize: 13, bold: true, color: NAVY, margin: 0 });
  text(c[2], { x: M + 0.16, y: yy + 0.42, w: 4.18, h: 0.7, fontSize: 12, margin: 0, lh: 1.3 });
});
img("../../thesis/figures/fig_voronoi.png", 5.25, 1.15, 4.2, 2.88);
text("Ô Voronoi của phần tử người dùng đã chạm", { x: 5.25, y: 4.08, w: 4.2, h: 0.3, fontSize: 11, italic: true, color: GREY, align: "center", margin: 0 });
block(5.25, 4.5, 4.2, 1.7);
text([{ text: "Đây không phải mô hình tự chấm.", options: { bold: true, color: RED } }, { text: " Chuẩn để chấm là toạ độ một người thật đã chạm. Mô hình định vị không bao giờ được cho biết toạ độ đó.", options: {} }], { x: 5.45, y: 4.5, w: 3.8, h: 1.7, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.35 });
N(11); foot(); done();

// ══════════ 12 · VÌ SAO VORONOI ══════════
slide();
bar("4 · Luật xác định trúng được chọn từ sàn mà nó đạt được");
text("Đặt trước thước một câu cố tình gọi sai tên nút, rồi xem luật nào còn cho điểm.", { x: M, y: 0.95, w: W - 2 * M, h: 0.4, fontSize: 14, margin: 0 });
table(M + 0.7, 1.6, [4.8, 2.0, 1.4], [
  { cells: ["Luật xác định trúng", "Chấm đúng cho câu sai nút", ""], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 12.5, align: ["left", "center", "center"] },
  { cells: ["Ngưỡng dung sai quy ước", { t: "84,3%", fs: 15 }, "không dùng được"], h: 0.62, fs: 13.5, color: RED, bold: true, rule: true },
  { cells: ["Thêm điều kiện ô Voronoi", { t: "2,8%", fs: 15 }, "đã chọn"], h: 0.62, fs: 13.5, color: TEAL, bold: true },
], { align: ["left", "center", "right"] });
text("Ba chi tiết của luật, đọc thẳng từ mã cài đặt", { x: M, y: 3.5, w: W - 2 * M, h: 0.35, fontSize: 14, bold: true, color: NAVY, margin: 0 });
bullets([
  "Vùng dung sai là hình chữ nhật: ±151 điểm ảnh ngang nhưng ±336 dọc",
  "Hạt sinh ra ô Voronoi là chính điểm chạm, không phải tâm hộp phần tử",
  "Điều kiện Voronoi bao gồm cả điều kiện dung sai, nên nó là bản siết chặt",
], M + 0.15, 3.95, W - 2 * M - 0.3, { fs: 13.5, gap: 0.7, itemH: 0.66, lh: 1.25 });
N(12); foot(); done();

// ══════════ 13 · TRẦN VÀ SÀN ══════════
slide();
bar("4 · Trần và sàn đều là đại lượng đo được");
[["Câu chuẩn  (trần)", "75,7%", TEAL, 0.757],
 ["Mô hình sau tinh chỉnh", "59,1%", NAVY, 0.591],
 ["Mô hình chưa tinh chỉnh", "47,6%", FOOTC, 0.476],
 ["Câu chung chung, không nói phần tử nào", "12,0%", RED, 0.12],
 ["Câu thật nhưng của một màn hình khác", "6,1%", MAROON, 0.061]].forEach((g, i) => {
  const yy = 1.0 + i * 0.78;
  text(g[0], { x: M, y: yy, w: 3.6, h: 0.42, fontSize: 13, valign: "middle", margin: 0 });
  rect(4.25, yy + 0.06, 3.9, 0.3, "DCDAE4");
  rect(4.25, yy + 0.06, 3.9 * g[3], 0.3, g[2]);
  text(g[1], { x: 8.25, y: yy, w: 1.2, h: 0.42, fontSize: 15, bold: true, color: g[2], align: "right", valign: "middle", margin: 0 });
});
block(M, 5.05, W - 2 * M, 1.15);
text([{ text: "Câu đúng văn phong mà sai nội dung bị chấm thấp nhất trong mọi phép đo.", options: { bold: true, color: RED } }, { text: "\nDụng cụ đo thật sự đọc nội dung câu, không thưởng cho văn phong.", options: {} }], { x: M + 0.25, y: 5.05, w: W - 2 * M - 0.5, h: 1.15, fontSize: 14, valign: "middle", margin: 0, lh: 1.4 });
N(13); foot(); done();

// ══════════ 14 · SÁU KHỐI KIỂM CHỨNG ══════════
slide();
bar("4 · Sáu khối kiểm chứng của thước");
table(M, 1.0, [4.15, 4.74], [
  { cells: ["Khối kiểm chứng", "Kết quả đo"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 13 },
  { cells: ["Điều kiện sai số dụng cụ, đặt trước", { t: "sai số trung vị 0,7%, ngưỡng 3%", bold: true, color: TEAL }], h: 0.6, fs: 12.5, rule: true },
  { cells: ["Luật trúng chọn từ sàn", { t: "84,3%  →  2,8%", bold: true, color: TEAL }], h: 0.6, fs: 12.5, rule: true },
  { cells: ["Trần và sàn của thước", { t: "75,7  /  12,0  /  6,1", bold: true, color: TEAL }], h: 0.6, fs: 12.5, rule: true },
  { cells: ["Mười phép bơm lỗi, ngưỡng đặt sẵn", { t: "đạt", bold: true, color: TEAL }], h: 0.6, fs: 12.5, rule: true },
  { cells: ["Viết lại 1.139 câu, bảo toàn nghĩa", { t: "+0,35 điểm  [−0,59 ; +1,29]", bold: true, color: TEAL }], h: 0.6, fs: 12.5, rule: true },
  { cells: ["Đổi sang một mô hình định vị thứ hai", { t: "giữ 94% độ lớn phép so S1 với Base", bold: true, color: TEAL }], h: 0.6, fs: 12.5 },
], { align: ["left", "center"] });
block(M, 5.15, W - 2 * M, 1.05);
text([{ text: "Hai phép thử độ bền nữa.", options: { bold: true, color: NAVY } }, { text: " Năm luật chấm khác nhau không đổi thứ tự các hệ thống. Thước tất định: 1.625 phép so, không một bất đồng.", options: {} }], { x: M + 0.25, y: 5.15, w: W - 2 * M - 0.5, h: 1.05, fontSize: 13, valign: "middle", margin: 0, lh: 1.35 });
N(14); foot(); done();

// ══════════ 15 · ĐĂNG KÝ TRƯỚC ══════════
slide();
bar("4 · Thiết kế so sánh và mức chênh nhỏ nhất phát hiện được");
text("Mọi nhánh chấm trên cùng 4.463 bước, nên chênh lệch giữa hai nhánh là hiệu ghép cặp. Hiệu đó đọc theo khoảng tin cậy và theo mức chênh nhỏ nhất phát hiện được (MDE), đo từ nhánh nền.", { x: M, y: 0.92, w: W - 2 * M, h: 0.7, fontSize: 13, margin: 0, lh: 1.3 });
table(M, 1.75, [2.2, 2.6], [
  { cells: ["Kết cục", "Cách đọc"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12 },
  { cells: [{ t: "Δ vượt MDE, KTC loại 0", color: TEAL, bold: true }, "thành phần có tác dụng"], h: 0.5, fs: 12, rule: true },
  { cells: [{ t: "KTC chạm 0", color: TEAL }, "xu hướng, chưa gọi là cải thiện"], h: 0.5, fs: 12, rule: true },
  { cells: [{ t: "|Δ| dưới MDE", color: MAROON, bold: true }, "không kết luận được"], h: 0.5, fs: 12, rule: true },
  { cells: [{ t: "Cận trên KTC < 0", color: RED, bold: true }, "thành phần gây hại"], h: 0.5, fs: 12 },
]);
bullets([
  "Hai hạt giống của nhánh nền cho nhiễu dựng lại: 0,52 điểm",
  "Sai số chuẩn ghép cặp đo được 0,79 điểm, nên MDE là 2,2 điểm; công thức chiếu thông dụng cho 4 đến 9 điểm vì giả định tương quan trong cụm bằng một",
  "Thiết kế một hạt giống có MDE 2,11 điểm",
], 5.1, 1.8, 4.35, { fs: 12, gap: 1.0, itemH: 0.95, lh: 1.3 });
block(M, 4.9, W - 2 * M, 1.3);
text([{ text: "Mức chênh nhỏ nhất phát hiện được là 2,2 điểm.", options: { bold: true, color: RED } }, { text: "\nMọi kết quả ở phần sau đọc trên con số này.", options: {} }], { x: M + 0.25, y: 4.9, w: W - 2 * M - 0.5, h: 1.3, fontSize: 14, valign: "middle", margin: 0, lh: 1.4 });
N(15); foot(); done();

// ══════════ 16 · KẾT QUẢ CHÍNH ══════════
slide();
bar("5 · Kết quả chính trên 4.463 bước chạm");
table(M, 0.95, [3.0, 1.35, 2.05, 1.4, 1.09], [
  { cells: ["Nhánh", "Exec.", "Khoảng tin cậy 95%", "Hộp phần tử", ""], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12, align: ["left", "center", "center", "center", "center"] },
  { cells: [{ t: "Câu chuẩn  (trần)", italic: true }, { t: "75,7", bold: true, color: TEAL }, "[74,1 ; 77,3]", { t: "83,8", bold: true, color: TEAL }, ""], h: 0.44, fs: 12.5, rule: "322164", ruleW: 1.5 },
  { cells: ["Base, chưa tinh chỉnh", "47,6", "[45,9 ; 49,3]", "53,6", ""], h: 0.4, fs: 12.5, rule: true },
  { cells: ["S1, hạt giống 101", "59,1", "[57,3 ; 60,8]", "65,5", ""], h: 0.4, fs: 12.5, rule: true },
  { cells: ["S1, hạt giống 202", "59,6", "[57,9 ; 61,3]", "66,1", ""], h: 0.4, fs: 12.5, rule: "322164", ruleW: 1.5 },
  { cells: ["S2, khai báo trước", "57,2", "[55,4 ; 58,9]", "63,6", { t: "một hạt giống", color: MAROON, italic: true, fs: 10 }], h: 0.4, fs: 12.5, rule: true },
  { cells: ["CE2-S2, nhánh so sánh", "59,4", "[57,7 ; 61,1]", "66,0", { t: "một hạt giống", color: MAROON, italic: true, fs: 10 }], h: 0.4, fs: 12.5, rule: true },
  { cells: ["MIN-DESC, mục tiêu ưu tiên", "60,05", "[58,3 ; 61,8]", "66,5", { t: "một hạt giống", color: MAROON, italic: true, fs: 10 }], h: 0.4, fs: 12.5, rule: true },
  { cells: [{ t: "Chặng ba, thưởng ô toạ độ", bold: true }, { t: "60,07", bold: true, color: NAVY }, "[58,3 ; 61,8]", { t: "67,0", bold: true, color: NAVY }, { t: "một hạt giống", color: MAROON, italic: true, fs: 10 }], h: 0.4, fs: 12.5, rule: "322164", ruleW: 1.5 },
  { cells: ["Nhánh ứng viên, hạt giống 101", "56,1", "[54,5 ; 58,0]", "62,4", { t: "điều kiện khác", color: MAROON, italic: true, fs: 10 }], h: 0.4, fs: 12.5 },
], { align: ["left", "center", "center", "center", "center"] });
text("Năm nhánh dưới vạch chỉ có một hạt giống. Chặng ba hơn chặng hai 0,02 điểm, tức hai nhánh cùng một mức. Cột hộp phần tử là thước báo kèm: điểm dự đoán rơi vào bên trong khung của phần tử đúng, theo luật chấm gốc của bộ dữ liệu. Cột này tính sau khi đã có mọi điểm nên không dùng làm con số chính.", { x: M, y: 5.0, w: W - 2 * M, h: 0.6, fontSize: 11, italic: true, color: GREY, margin: 0, lh: 1.2 });
block(M, 5.62, W - 2 * M, 0.9);
bullets([
  "Ba khoảng tin cậy của Base, S1 và trần rời nhau hoàn toàn",
  "Thứ tự các nhánh không đổi dưới cả hai luật chấm",
], M + 0.2, 5.69, W - 2 * M - 0.4, { fs: 13, gap: 0.44, itemH: 0.4, lh: 1.2 });
N(16); foot(); done();

// ══════════ 17 · GHÉP CẶP ══════════
slide();
bar("5 · So sánh ghép cặp và các cách giải thích thay thế");
table(M, 0.95, [3.4, 1.5, 2.2, 1.79], [
  { cells: ["Phép so (McNemar)", "Δ", "KTC 95%", "p"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12.5, align: ["left", "center", "center", "center"] },
  { cells: [{ t: "S1 − Base", bold: true }, { t: "+11,5", bold: true, color: TEAL }, "[+10,0 ; +13,1]", "<0,001"], h: 0.44, fs: 13, rule: true },
  { cells: ["Trần − S1", "+16,6", "-", "<0,001"], h: 0.42, fs: 13, rule: true },
  { cells: [{ t: "Nhiễu giữa hai hạt giống", italic: true }, "+0,52", "[−0,22 ; +1,26]", "0,194"], h: 0.42, fs: 13 },
], { align: ["left", "center", "center", "center"] });
text("Tín hiệu gấp 22 lần nhiễu. Bỏ hết bước mô hình chép nguyên câu chuẩn thì khoảng cách vẫn còn 8,4 điểm.", { x: M, y: 2.82, w: W - 2 * M, h: 0.6, fontSize: 13.5, bold: true, color: NAVY, margin: 0, lh: 1.3 });
text("Sáu cách giải thích thay thế đã kiểm", { x: M, y: 3.5, w: W - 2 * M, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
[["Chép lại câu chuẩn", "vẫn còn 8,4 điểm", TEAL],
 ["Thiên vị độ dài câu", "nghiêng về phía Base", TEAL],
 ["Trùng ứng dụng dạy và kiểm", "không ghi nhận ảnh hưởng", TEAL],
 ["Luật chấm chọn có lợi", "năm luật không đổi thứ tự", TEAL],
 ["Thước mong manh trước diễn đạt", "+0,35 trên 1.139 câu", TEAL],
 ["Dụng cụ quen văn phong", "chỉ đóng sau khi đổi dụng cụ", MAROON]].forEach((a, i) => {
  const xx = i % 2 === 0 ? M : 5.0, yy = 3.95 + Math.floor(i / 2) * 0.62;
  rect(xx, yy, 4.4, 0.54, BLOCK, { radius: 0.04 });
  text(a[0], { x: xx + 0.12, y: yy, w: 2.5, h: 0.54, fontSize: 11.5, valign: "middle", margin: 0 });
  text(a[1], { x: xx + 2.6, y: yy, w: 1.7, h: 0.54, fontSize: 11, bold: true, color: a[2], align: "right", valign: "middle", margin: 0 });
});
N(17); foot(); done();

// ══════════ 18 · NHÁNH KHAI BÁO ══════════
slide();
bar("5 · Nhánh khai báo: một hạt giống, không kết luận được");
block(M, 0.95, W - 2 * M, 1.0);
text([{ text: "S2 đạt 57,2%, thấp hơn nhánh nền 1,93 điểm.", options: { bold: true, color: RED } }, { text: "  Độ lớn đó dưới mức phát hiện 2,2 nên không kết luận được.", options: {} }], { x: M + 0.25, y: 0.95, w: W - 2 * M - 0.5, h: 1.0, fontSize: 14, valign: "middle", margin: 0, lh: 1.35 });
text("Vì sao không kết luận được", { x: M, y: 2.15, w: 4.4, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Đại lượng chính đòi hai hạt giống; hạt thứ hai bị huỷ vì ngân sách",
  "Luận văn không kết luận thành phần có tác dụng hay gây hại",
  "Cũng không lấy phép so khác để thế chỗ",
], M, 2.6, 4.4, { fs: 12.5, gap: 0.78, itemH: 0.74, lh: 1.3 });
text("Chỗ thiệt hại nằm ở đâu", { x: 5.1, y: 2.15, w: 4.35, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
table(5.1, 2.6, [2.2, 0.7, 0.7, 0.75], [
  { cells: ["Nhóm bước", "S1", "S2", "Δ"], bold: true, color: WHITE, fill: NAVY, h: 0.38, fs: 11, align: ["left", "center", "center", "center"] },
  { cells: ["Có sinh khai báo (4.138)", "62,2", "60,8", { t: "−1,38", color: MAROON }], h: 0.46, fs: 11.5, rule: true },
  { cells: [{ t: "Không sinh (325)", bold: true }, "19,7", "10,8", { t: "−8,92", bold: true, color: RED }], h: 0.46, fs: 11.5 },
], { align: ["left", "center", "center", "center"] });
text("7,3% số bước chiếm 34% chênh lệch.", { x: 5.1, y: 4.05, w: 4.35, h: 0.32, fontSize: 12.5, bold: true, color: RED, margin: 0 });
block(M, 4.9, W - 2 * M, 1.3);
text([{ text: "Tinh chỉnh phải trả một giá.", options: { bold: true, color: RED } }, { text: "  Mô hình gốc gọi đúng loại thao tác nhiều hơn cả hai bản đã huấn luyện: 83,4% so với 55,1% và 38,8%.", options: {} }], { x: M + 0.25, y: 4.9, w: W - 2 * M - 0.5, h: 1.3, fontSize: 13, valign: "middle", margin: 0, lh: 1.35 });
N(18); foot(); done();

// ══════════ 19 · CHẶNG HAI ══════════
slide();
bar("5 · Chặng hai: phần lớn mức tăng không thuộc mục tiêu ưu tiên");
[["S2", "57,2", FOOTC], ["CE2-S2", "59,4", FOOTC], ["MIN-DESC", "60,0", NAVY]].forEach((c, i) => {
  const xx = 1.15 + i * 2.9;
  rect(xx, 1.05, 2.0, 0.95, i === 2 ? NAVY : BLOCK, { radius: 0.06, shadow: true });
  text(c[0], { x: xx, y: 1.12, w: 2.0, h: 0.32, fontSize: 13, bold: true, color: i === 2 ? WHITE : NAVY, align: "center", margin: 0 });
  text(c[1] + "%", { x: xx, y: 1.48, w: 2.0, h: 0.45, fontSize: 19, bold: true, color: i === 2 ? WHITE : INK, align: "center", margin: 0 });
  if (i < 2) arrow(xx + 2.1, 1.52, 0.7, FOOTC);
});
text("+2,24\nhọc có giám sát thuần", { x: 3.15, y: 2.08, w: 2.0, h: 0.62, fontSize: 11.5, color: MAROON, align: "center", margin: 0, lh: 1.2 });
text("+0,63\nriêng mục tiêu ưu tiên", { x: 6.05, y: 2.08, w: 2.0, h: 0.62, fontSize: 11.5, color: MAROON, align: "center", margin: 0, lh: 1.2 });
block(M, 2.9, W - 2 * M, 0.75);
text("78% mức tăng thuộc về nhánh so sánh. Đo ở tầng khai báo, tỉ lệ ấy là 87,7%.", { x: M + 0.25, y: 2.9, w: W - 2 * M - 0.5, h: 0.75, fontSize: 14, bold: true, color: RED, valign: "middle", margin: 0 });
table(M, 3.85, [4.2, 1.5, 2.2, 1.09], [
  { cells: ["Đại lượng", "Δ", "KTC 95%", "p"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12, align: ["left", "center", "center", "center"] },
  { cells: [{ t: "MIN-DESC − CE2-S2", bold: true }, { t: "+0,63", bold: true }, "[+0,16 ; +1,10]", "0,011"], h: 0.46, fs: 12.5, rule: true },
  { cells: ["MIN-DESC − S1", "+0,94", "[−0,09 ; +2,05]", "0,11"], h: 0.46, fs: 12.5 },
], { align: ["left", "center", "center", "center"] });
block(M, 5.3, W - 2 * M, 0.9);
text([{ text: "Không kết luận được:", options: { bold: true, color: MAROON } }, { text: " +0,63 vẫn dưới mức phát hiện 2,11 và chỉ bằng 1,4 lần nhiễu giữa hạt giống.", options: {} }], { x: M + 0.25, y: 5.3, w: W - 2 * M - 0.5, h: 0.9, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.35 });
N(19); foot(); done();

// ══════════ 20 · CHẶNG BA ══════════
slide();
bar("5 · Chặng ba: khai báo tăng rõ, thực thi đứng yên");
text("Học tăng cường thưởng thẳng cho ô toạ độ, học tiếp từ điểm lưu của chặng hai, chấm trên cùng 4.463 bước chạm", { x: M, y: 0.72, w: W - 2 * M, h: 0.32, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.18, [3.75, 1.65, 1.65, 1.84], [
  { cells: ["Đại lượng", "Chặng hai", "Chặng ba", "Chênh"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12, align: ["left", "center", "center", "center"] },
  { cells: [{ t: "Ô khai báo đúng cả tên lẫn toạ độ", color: TEAL }, "60,6", { t: "63,2", bold: true, color: TEAL }, { t: "+2,56", bold: true, color: TEAL }], h: 0.46, fs: 12.5, rule: true },
  { cells: [{ t: "Điểm thực thi  (thước tiêu đề)", bold: true }, "60,05", { t: "60,07", bold: true }, { t: "+0,02", bold: true, color: MAROON }], h: 0.46, fs: 12.5, rule: true },
  { cells: ["Luật hộp phần tử, thước báo kèm", "66,55", "67,04", "+0,49"], h: 0.44, fs: 12.5, rule: true },
  { cells: ["BLEU-4", "37,9", "37,8", "−0,08"], h: 0.44, fs: 12.5 },
], { align: ["left", "center", "center", "center"] });
bullets([
  [{ text: "Mức tăng ở tầng khai báo có ý nghĩa thống kê: ", options: {} }, { text: "p = 1,3·10⁻⁸", options: { bold: true } }, { text: ", khoảng [+1,69 ; +3,44]", options: {} }],
  [{ text: "Mức chênh ở đầu ra: khoảng ", options: {} }, { text: "[−0,59 ; +0,64]", options: { bold: true } }, { text: ", hẹp tới mức loại được mọi mức tăng từ 0,64 điểm trở lên", options: {} }],
  [{ text: "Dự báo ghi trước ", options: {} }, { text: "+1,10 điểm bị bác", options: { bold: true, color: RED } }, { text: ": hệ số chuyển đổi thật xấp xỉ 0,01, nên nó phụ thuộc dạng can thiệp chứ không phải hằng số của bài toán", options: {} }],
  "Câu ở đầu ra không bị bẻ thành chuỗi khó đọc: BLEU-4 và tỉ lệ khớp loại thao tác đều giữ nguyên",
], M + 0.15, 3.5, W - 2 * M - 0.3, { fs: 12.5, gap: 0.6, itemH: 0.56, lh: 1.25 });
block(M, 5.95, W - 2 * M, 0.85);
text([{ text: "Hai phần ba thay đổi không tới được câu.", options: { bold: true, color: NAVY } }, { text: "  Trong 1.950 bước có ô khai báo đổi, 1.300 bước câu không đổi một ký tự, mà thước chỉ đọc câu.", options: {} }], { x: M + 0.25, y: 5.95, w: W - 2 * M - 0.5, h: 0.85, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.25 });
N(20); foot(); done();

// ══════════ 20 · CHẨN ĐOÁN 2x2 ══════════
slide();
bar("5 · Phân tích lỗi: cơ chế đúng, nhưng bị chặn bởi độ chính xác khai báo");
text("Chia 3.473 bước có tên tham chiếu, theo việc dòng khai báo của chính mô hình đúng hay sai", { x: M, y: 0.9, w: W - 2 * M, h: 0.32, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.35, [2.6, 1.7, 1.6, 1.3, 1.4, 0.79], [
  { cells: ["Nhóm", "n", "MIN-DESC", "S1", "Δ", "Trần"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 12, align: ["left", "center", "center", "center", "center", "center"] },
  { cells: [{ t: "Khai báo ĐÚNG", bold: true, color: TEAL }, "2.106  (60,6%)", { t: "87,1", bold: true }, "78,3", { t: "+8,83", bold: true, color: TEAL }, "86,3"], h: 0.62, fs: 13.5, rule: true },
  { cells: [{ t: "Khai báo SAI", bold: true, color: RED }, "1.367  (39,4%)", { t: "21,8", bold: true }, "32,9", { t: "−11,12", bold: true, color: RED }, "61,4"], h: 0.62, fs: 13.5 },
], { align: ["left", "center", "center", "center", "center", "center"] });
bullets([
  "Khai báo đúng thì mô hình vượt cả trần của nhóm đó",
  "Khai báo sai thì nó làm sai câu nặng hơn cả không khai báo",
  [{ text: "Hai chiều triệt tiêu nhau, cộng lại thành ", options: {} }, { text: "+0,94 điểm không có ý nghĩa", options: { bold: true, color: MAROON } }],
], M + 0.15, 3.3, W - 2 * M - 0.3, { fs: 13.5, gap: 0.68, itemH: 0.64, lh: 1.25 });
block(M, 5.35, W - 2 * M, 0.85);
text([{ text: "Cách chia nhóm này là hậu kiểm:", options: { bold: true, color: RED } }, { text: " biến chia nhóm là hành vi của chính mô hình được đo.", options: {} }], { x: M + 0.25, y: 5.35, w: W - 2 * M - 0.5, h: 0.85, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.35 });
N(21); foot(); done();

// ══════════ 21 · PHÂN RÃ NĂM Ô ══════════
slide();
bar("5 · 63% dư địa còn lại nằm gọn trong một ô duy nhất");
table(M, 1.0, [2.7, 1.05, 0.9, 1.1, 1.1, 1.1, 1.04], [
  { cells: ["Trạng thái ô khai báo", "n", "%", "MIN", "S1", "Trần", "Dư địa"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 11.5, align: ["left", "center", "center", "center", "center", "center", "center"] },
  { cells: ["tên đúng, toạ độ đúng", "2.082", "46,7", { t: "87,1", bold: true }, "78,2", "86,3", "−0,36"], h: 0.42, fs: 11.5, rule: true },
  { cells: ["tên đúng, toạ độ sai", "220", "4,9", "26,4", "27,7", "32,3", "+0,29"], h: 0.4, fs: 11.5, rule: true },
  { cells: ["tên sai, toạ độ đúng", "411", "9,2", "57,2", "53,0", "73,0", "+1,46"], h: 0.4, fs: 11.5, rule: true },
  { cells: ["không sinh khai báo", "15", "0,3", "0,0", "0,0", "60,0", "+0,20"], h: 0.4, fs: 11.5, rule: true },
  { cells: [{ t: "tên sai, toạ độ sai", bold: true, color: RED }, { t: "745", bold: true }, { t: "16,7", bold: true }, { t: "3,6", bold: true, color: RED }, { t: "25,8", bold: true }, "64,4", { t: "+10,15", bold: true, color: RED }], h: 0.48, fs: 12, rule: true },
  { cells: ["không có tên tham chiếu", "990", "22,2", "55,3", "54,4", "73,0", "+3,94"], h: 0.4, fs: 11.5 },
], { align: ["left", "center", "center", "center", "center", "center", "center"] });
bullets([
  "Ô đúng cả hai đã hết dư địa: mô hình vượt trần trên 46,7% số bước",
  "Ô sai cả hai giữ 63% dư địa, mà câu chuẩn vẫn đạt 64,4 ở đó",
], M + 0.15, 4.2, W - 2 * M - 0.3, { fs: 13.5, gap: 0.62, itemH: 0.58, lh: 1.25 });
block(M, 5.45, W - 2 * M, 0.75);
text([{ text: "Chặn được thiệt hại ở nhóm khai báo sai thì được +5,4 điểm.", options: { bold: true, color: NAVY } }, { text: "  Bảy cơ chế chọn đã thử đều nằm trong nhiễu, nên phải sửa ở khâu huấn luyện.", options: {} }], { x: M + 0.25, y: 5.45, w: W - 2 * M - 0.5, h: 0.75, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.3 });
N(22); foot(); done();


// ══════════ 22 · HAI KÊNH ══════════
slide();
bar("5 · Điểm nghẽn nằm ở tri giác, không ở diễn đạt");
text("Tách đường đi từ ảnh tới câu thành hai kênh đo được riêng, cùng một luật phán đúng sai (n = 4.442)", { x: M, y: 0.9, w: W - 2 * M, h: 0.32, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.32, [2.5, 1.45, 1.45, 1.45, 1.54], [
  { cells: ["Nhóm", "n", "MIN-DESC", "S1", "Câu chuẩn"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 12, align: ["left", "center", "center", "center", "center"] },
  { cells: [{ t: "Nhìn ĐÚNG phần tử", bold: true, color: TEAL }, "3.114  (70,1%)", { t: "82,37", bold: true }, "74,18", "84,36"], h: 0.6, fs: 13.5, rule: true },
  { cells: [{ t: "Nhìn SAI phần tử", bold: true, color: RED }, "1.328  (29,9%)", { t: "8,43", bold: true, color: RED }, "24,47", "55,72"], h: 0.6, fs: 13.5 },
], { align: ["left", "center", "center", "center", "center"] });
bullets([
  [{ text: "Nhóm nhìn đúng chiếm 70% số bước nhưng chỉ đóng góp ", options: {} }, { text: "9%", options: { bold: true } }, { text: " khoảng cách so với câu chuẩn", options: {} }],
  [{ text: "Nhóm nhìn sai chiếm 30% mà đóng góp ", options: {} }, { text: "91%", options: { bold: true, color: RED } }, { text: " của khoảng cách 15,53 điểm", options: {} }],
  [{ text: "Câu chuẩn cũng giảm 28,64 điểm ở nhóm khó, mô hình giảm 73,94 ", options: {} }, { text: "⇒ thiếu hụt riêng +45,30", options: { bold: true, color: MAROON } }],
], M + 0.15, 3.15, W - 2 * M - 0.3, { fs: 13, gap: 0.66, itemH: 0.62, lh: 1.25 });
block(M, 5.35, W - 2 * M, 0.85);
text([{ text: "Năm can thiệp đã đo đều đặt ở tầng khai báo và ngôn ngữ.", options: { bold: true, color: NAVY } }, { text: "  Không can thiệp nào chạm tới tầng bị nghẽn.", options: {} }], { x: M + 0.25, y: 5.35, w: W - 2 * M - 0.5, h: 0.85, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.35 });
N(23); foot(); done();

// ══════════ 23 · HỆ SỐ TRUYỀN ══════════
slide();
bar("5 · Sửa được tri giác vẫn phải đi qua tầng sinh câu");
text("Chặng ba là can thiệp duy nhất đặt phần thưởng thẳng lên ô toạ độ, nên đo được mức truyền (n = 4.437)", { x: M, y: 0.9, w: W - 2 * M, h: 0.32, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.32, [3.0, 1.5, 1.55, 1.55, 0.79], [
  { cells: ["Ô chéo giữa chặng hai và chặng ba", "n", "MIN-DESC", "Chặng ba", "Chênh"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 11.5, align: ["left", "center", "center", "center", "center"] },
  { cells: ["giữ đúng", "2.997", "83,08", "82,95", "−0,13"], h: 0.4, fs: 12, rule: true },
  { cells: ["giữ sai", "1.143", "6,91", "6,30", "−0,61"], h: 0.4, fs: 12, rule: true },
  { cells: [{ t: "sai chuyển thành đúng", color: TEAL }, { t: "184", bold: true }, "17,93", { t: "58,15", bold: true, color: TEAL }, { t: "+40,22", bold: true, color: TEAL }], h: 0.46, fs: 12, rule: true },
  { cells: [{ t: "đúng chuyển thành sai", color: RED }, { t: "113", bold: true }, "62,83", { t: "8,85", bold: true, color: RED }, { t: "−53,98", bold: true, color: RED }], h: 0.46, fs: 12 },
], { align: ["left", "center", "center", "center", "center"] });
bullets([
  [{ text: "Kênh tri giác lên 1,60 điểm nhưng thực thi chỉ lên 0,045 ", options: {} }, { text: "⇒ mức truyền 0,028", options: { bold: true, color: MAROON } }],
  "Sửa 184 bước với mức lợi 40 điểm, làm sai 113 bước với mức thiệt 54 điểm: hai chiều triệt tiêu",
  "Muốn vượt ngưỡng phát hiện cần 243 bước sửa mà không kèm bước nào bị làm sai, tức 18,3% nhóm nhìn sai",
], M + 0.15, 3.65, W - 2 * M - 0.3, { fs: 13, gap: 0.62, itemH: 0.58, lh: 1.25 });
block(M, 5.6, W - 2 * M, 0.7);
text([{ text: "Tương quan giữa các nhánh là 0,739, gấp 26 lần mức truyền thật.", options: { bold: true, color: RED } }, { text: "  Nó không phải hệ số quy đổi.", options: {} }], { x: M + 0.25, y: 5.6, w: W - 2 * M - 0.5, h: 0.7, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.3 });
N(24); foot(); done();

// ══════════ 22 · NHÁNH ỨNG VIÊN ══════════
slide();
bar("5 · Nhánh ứng viên: cơ chế chọn đúng, điểm nghẽn là bỏ cuộc quá mức");
text("Ô khai báo đổi từ sinh tự do sang chọn một dòng trong danh sách tối đa 40 ứng viên của chính màn hình. Không đạt ngưỡng dừng: độ chính xác chọn 57,5% so với ngưỡng 63,6%. Executability 56,1% [54,5 ; 58,0].", { x: M, y: 0.85, w: W - 2 * M, h: 0.7, fontSize: 12.5, margin: 0, lh: 1.3 });
text("Chia theo việc danh sách có đáp án và mô hình có đưa ra lựa chọn hay không", { x: M, y: 1.6, w: 5.2, h: 0.3, fontSize: 12.5, bold: true, color: NAVY, margin: 0 });
table(M, 1.95, [1.5, 1.35, 0.95, 1.4], [
  { cells: ["Có đáp án", "Mô hình", "n", "Exec."], bold: true, color: WHITE, fill: NAVY, h: 0.38, fs: 11.5, align: ["left", "left", "center", "center"] },
  { cells: ["có", { t: "chọn", color: TEAL, bold: true }, "2.326", { t: "71,4", bold: true, color: TEAL }], h: 0.44, fs: 12.5, rule: true },
  { cells: ["có", { t: "bỏ cuộc (sai)", color: RED, bold: true }, "872", { t: "23,7", bold: true, color: RED }], h: 0.44, fs: 12.5, rule: true },
  { cells: ["không", "chọn (sai)", "264", "37,5"], h: 0.4, fs: 12, rule: true },
  { cells: ["không", "bỏ cuộc (đúng)", "1.001", "53,8"], h: 0.4, fs: 12 },
], { align: ["left", "left", "center", "center"] });
text("Khi đưa ra lựa chọn, kém câu chuẩn 4,3 điểm. Bỏ cuộc sai ở 27,3% số bước có đáp án, tái lập qua hai phép đo.", { x: M, y: 4.1, w: 5.2, h: 0.75, fontSize: 12, bold: true, color: RED, margin: 0, lh: 1.3 });
text("Tỉ lệ nhãn bỏ cuộc theo mẫu số", { x: 6.05, y: 1.6, w: 3.4, h: 0.3, fontSize: 12.5, bold: true, color: NAVY, margin: 0 });
table(6.05, 1.95, [2.45, 0.95], [
  { cells: ["Toàn tập huấn luyện", "54,8%"], h: 0.44, fs: 12, rule: true },
  { cells: ["Chỉ bước chạm, tập huấn luyện", "29,1%"], h: 0.44, fs: 12, rule: true },
  { cells: ["Bước chạm tập kiểm, tỉ lệ đúng", "28,3%"], h: 0.44, fs: 12, rule: true },
  { cells: [{ t: "Mô hình phát ra", bold: true }, { t: "42,0%", bold: true, color: RED }], h: 0.44, fs: 12 },
], { align: ["left", "right"] });
text("Mọi bước không chạm đều mang nhãn bỏ cuộc, nên hơn nửa mẫu huấn luyện dạy mô hình bỏ cuộc. Đây là quan sát, chưa phải nhân quả.", { x: 6.05, y: 3.85, w: 3.4, h: 1.0, fontSize: 11.5, margin: 0, lh: 1.3 });
block(M, 5.1, W - 2 * M, 1.1);
text([{ text: "Không có nhánh so sánh cùng đầu vào, nên luận văn không nói gì về công của đầu chọn hay của danh sách.", options: { bold: true, color: NAVY } }, { text: " Nhánh chỉ so được với Base: +8,54 điểm. Mọi số ở đây là kết quả một hạt giống.", options: {} }], { x: M + 0.25, y: 5.1, w: W - 2 * M - 0.5, h: 1.1, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.35 });
N(25); foot(); done();

// ══════════ 23 · HẠN CHẾ ══════════
slide();
bar("6 · Hạn chế, tự khai kèm số đo");
text("Về kết quả mô hình", { x: M, y: 0.95, w: 4.4, h: 0.32, fontSize: 14, bold: true, color: NAVY, margin: 0 });
bullets([
  "Mọi nhánh xử lý chỉ chạy được một hạt giống",
  "Điều kiện không gây hại không đạt: giảm 19,75 điểm ở bước không chạm",
  "Dữ liệu cặp có lối tắt ở 17,4% số cặp, phát hiện sau khi huấn luyện",
  "Ba nhánh so sánh trong thiết kế không chạy",
  "Nhánh ứng viên không có nhánh so sánh cùng đầu vào",
], M, 1.4, 4.4, { fs: 12.5, gap: 0.68, itemH: 0.64, lh: 1.3 });
text("Về dụng cụ đo và dữ liệu", { x: 5.1, y: 0.95, w: 4.35, h: 0.32, fontSize: 14, bold: true, color: NAVY, margin: 0 });
bullets([
  "Hai dụng cụ đo cùng họ Qwen-VL với mô hình bị chấm",
  "Thước chưa đối chiếu với đánh giá của người thật",
  "Tập kiểm không phải ứng dụng chưa từng xuất hiện: 95,6% trùng",
  "Khâu chấm cho sẵn ngữ cảnh là câu chuẩn của các bước trước",
], 5.1, 1.4, 4.35, { fs: 12.5, gap: 0.82, itemH: 0.78, lh: 1.3 });
block(M, 4.9, W - 2 * M, 1.3);
text("Phạm vi của luận văn gồm một màn hình mỗi lần, giao diện tiếng Anh, một bộ dữ liệu, hai mô hình định vị cùng họ và một mô hình gốc cỡ ba tỉ tham số.", { x: M + 0.25, y: 4.9, w: W - 2 * M - 0.5, h: 1.3, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.4 });
N(26); foot(); done();

// ══════════ 24 · HƯỚNG PHÁT TRIỂN ══════════
slide();
bar("6 · Hướng phát triển");
text("Xếp theo mức cấp thiết với độ tin cậy của kết luận. Hướng đầu là hướng duy nhất chạm vào tầng mà phần phân tích định vị được", { x: M, y: 0.88, w: W - 2 * M, h: 0.32, fontSize: 12, italic: true, color: GREY, margin: 0 });
[["1", "Mở phần thị giác của mô hình nền cho quá trình tinh chỉnh", "Năm can thiệp đã đo đều nằm ở tầng khai báo hoặc ngôn ngữ, trong khi 91% khoảng cách dồn vào nhóm nhìn sai phần tử. Giữ mọi tham số khác để phép so vẫn một biến, mốc đối chiếu 59,11. Kỳ vọng ghi trước: xác suất vượt ngưỡng phát hiện khoảng 0,30.", TEAL],
 ["2", "Huấn luyện lại trên riêng 41.191 bước chạm, với điều kiện đã nêu", "Đưa tỉ lệ nhãn bỏ cuộc từ 54,8% về 29,1%. Dữ liệu đã dựng. Không chạy: thủ tục ngưỡng chỉ cải thiện tối đa 8 trên 1.400 bước, dưới ngưỡng 18/24 đặt trước.", RED],
 ["3", "Học quyết định bỏ cuộc từ tín hiệu ngoài xác suất của mô hình", "Điểm thẻ bỏ cuộc ở bước có vàng và không có vàng trùng nhau, AUC 0,69–0,72. Bỏ cuộc hoàn hảo cho 78,0%: khoảng 14,6 điểm cần một bộ phân loại riêng.", NAVY]].forEach((n, i) => {
  const yy = 1.3 + i * 1.42;
  block(M, yy, W - 2 * M, 1.28);
  text(n[0], { x: M + 0.14, y: yy + 0.12, w: 0.42, h: 0.42, fontSize: 21, bold: true, color: n[3], align: "center", margin: 0 });
  text(n[1], { x: M + 0.62, y: yy + 0.14, w: W - 2 * M - 0.85, h: 0.34, fontSize: 14, bold: true, color: n[3], margin: 0 });
  text(n[2], { x: M + 0.62, y: yy + 0.56, w: W - 2 * M - 0.85, h: 0.66, fontSize: 12.5, margin: 0, lh: 1.3 });
});
text("Còn lại: nhánh so sánh cùng đầu vào rồi hạt giống thứ hai · dạy mô hình lùi khi không chắc · khắc phục điều kiện không gây hại · nối thước với đánh giá của người · bộ liệt kê phần tử tốt hơn · chuỗi nhiều màn", { x: M, y: 5.65, w: W - 2 * M, h: 0.55, fontSize: 11.5, color: GREY, margin: 0, lh: 1.3 });
N(27); foot(); done();

// ══════════ 25 · KẾT LUẬN ══════════
slide();
bar("Kết luận");
[["Thước đo", "Executability, kiểm chứng bằng sáu khối phép đo. Trần 75,7 và sàn 12,0 đều đo được.", TEAL],
 ["Kết quả", "Tinh chỉnh đáng 11,5 điểm và đứng vững sau sáu cách giải thích thay thế. Điểm cao nhất đạt được là 60,07, nhưng không can thiệp nào trong năm can thiệp đã đo vượt được mức chênh nhỏ nhất phát hiện được. Thành phần đề xuất chưa kết luận được ở một hạt giống, và luận văn dừng đúng ở đó.", NAVY],
 ["Phân tích lỗi", "Cơ chế đúng trên 60,6% số bước, nhưng bị chặn bởi độ chính xác khai báo. Nhánh ứng viên: cơ chế chọn đạt 71,4 khi đưa ra lựa chọn, điểm nghẽn mới là bỏ cuộc quá mức.", MAROON]].forEach((c, i) => {
  const yy = 1.05 + i * 1.35;
  rect(M, yy, W - 2 * M, 1.2, BLOCK, { radius: 0.06, shadow: true });
  text(c[0], { x: M + 0.2, y: yy + 0.12, w: 1.6, h: 0.35, fontSize: 14.5, bold: true, color: c[2], margin: 0 });
  text(c[1], { x: M + 0.2, y: yy + 0.5, w: W - 2 * M - 0.4, h: 0.65, fontSize: 12.5, margin: 0, lh: 1.32 });
});
text("Bài báo đã nộp", { x: M, y: 5.15, w: W - 2 * M, h: 0.3, fontSize: 13, bold: true, color: NAVY, margin: 0 });
table(M, 5.5, [2.3, 4.35, 2.25], [
  { cells: ["VCL 2026", "Nhãn quy chiếu tự động khi phần tử không có tên để gọi", { t: "đã nộp 30/8", italic: true, color: GREY }], h: 0.4, fs: 11.5, rule: true },
  { cells: ["FAIR 2026", "Descriptor and Preference Targets for GUI Instruction Generation", { t: "đã gửi 31/8", italic: true, color: GREY }], h: 0.4, fs: 11.5 },
], { align: ["left", "left", "right"] });
N(28); foot(); done();

// ══════════ 26 · CẢM ƠN ══════════
slide();
rect(0, 0, W, H, NAVY);
text("Trân trọng cảm ơn", { x: 0.8, y: 2.6, w: W - 1.6, h: 0.7, fontSize: 26, bold: true, color: WHITE, align: "center", margin: 0 });
text("Hỏi đáp và thảo luận", { x: 0.8, y: 3.5, w: W - 1.6, h: 0.5, fontSize: 16, color: "D8D4E6", align: "center", margin: 0 });
hline(3.6, 4.35, 2.8, "7A7099", 1.5);
text("Lê Đoàn Phương Uyên   ·   TS. Nguyễn Hồng Bửu Long\nTrường Đại học Khoa học Tự nhiên, ĐHQG-HCM", { x: 0.8, y: 4.65, w: W - 1.6, h: 0.8, fontSize: 13, color: "D8D4E6", align: "center", margin: 0, lh: 1.4 });
foot(); done();

// ═══════════════ SLIDE DỰ PHÒNG (mở khi hội đồng hỏi tới) ═══════════════

// B1 · thước đồng thuận
slide();
bar("Dự phòng · Lý do không dùng BLEU, ROUGE hay vector ngữ nghĩa");
table(M, 1.1, [3.5, 1.9, 1.8, 1.69], [
  { cells: ["Nhánh", "Executability", "BLEU-4", "ROUGE-L"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5, align: ["left", "center", "center", "center"] },
  { cells: ["Base", "47,6", "9,9", "40,4"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["S1 (hạt giống 101)", "59,1", "38,7", "67,3"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["CE2-S2", "59,4", "38,1", { t: "68,6", bold: true }], h: 0.4, fs: 12.5, rule: true },
  { cells: ["MIN-DESC", { t: "60,0", bold: true }, "37,9", "68,4"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["Nhánh ứng viên", "56,1", "34,5", "63,0"], h: 0.4, fs: 12.5, rule: true },
  { cells: [{ t: "Câu chuẩn", italic: true }, "75,7", "96,1", "100,0"], h: 0.4, fs: 12.5 },
], { align: ["left", "center", "center", "center"] });
bullets([
  "Ba thước cùng thứ tự ở ba nhánh cách xa nhau; trong cụm 57 đến 60 thì bất đồng: BLEU xếp MIN-DESC dưới S1, ROUGE-L xếp CE2-S2 cao nhất",
  "So khớp chuỗi kết oan 97,5% số câu diễn đạt khác; vector ngữ nghĩa cho AUC 0,336",
  "Zhao và cộng sự (EACL 2021) khuyên dùng thước có tham chiếu khi xếp hạng hệ thống, nên luận văn chỉ phát biểu ở mức hệ thống",
  "Bản thước không tham chiếu cho kết luận lệch không quá 0,20 điểm",
], M, 4.05, W - 2 * M, { fs: 12, gap: 0.62, itemH: 0.6, lh: 1.25 });
footB(); done();

// B2 · đổi dụng cụ
slide();
bar("Dự phòng · Chấm lại bằng UI-Venus-Ground-7B");
text("Lát 2.532 bước, mô hình định vị thứ hai không dùng AndroidControl khi huấn luyện", { x: M, y: 0.85, w: W - 2 * M, h: 0.3, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.25, [3.2, 2.85, 2.84], [
  { cells: ["Phép so", "UGround", "UI-Venus"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5, align: ["left", "center", "center"] },
  { cells: [{ t: "S1 − Base, mốc đối chiếu", bold: true }, { t: "+10,35", color: TEAL, bold: true, fs: 14 }, { t: "+9,68", color: TEAL, bold: true, fs: 14 }], h: 0.55, fs: 12.5, rule: true },
  { cells: ["S2 − S1", { t: "−1,93   p = 0,0005", color: RED }, { t: "−1,21   p = 0,026", color: RED }], h: 0.5, fs: 12.5, rule: true },
  { cells: ["Trần trên lát này", "70,0", "69,3"], h: 0.44, fs: 12.5 },
], { align: ["left", "center", "center"] });
bullets([
  "Mốc đối chiếu giữ 94% độ lớn, nên thang đo không bị nén",
  "Dấu của mọi phép so không đổi dưới cả hai dụng cụ",
  "UI-Venus cho điểm thấp hơn ở cả ba nhánh, nên nó không dễ tính hơn",
  "Chỗ chưa đóng: cả hai dụng cụ đều thuộc họ Qwen-VL",
], M, 3.5, W - 2 * M, { fs: 12.5, gap: 0.68, itemH: 0.64, lh: 1.3 });
footB(); done();

// B3 · độ bền luật chấm
slide();
bar("Dự phòng · Độ bền của luật chấm và tính tất định");
bullets([
  "Ba nhánh được chấm lại dưới năm luật trên 698 bước: trần trôi từ 56,6% lên 82,2%, thứ tự không đổi",
  "Chênh lệch S1 − Base nằm gọn trong khoảng 9,5 đến 13,0 điểm ở cả năm luật",
  "Thước cho kết quả tất định: bốn lượt chạy độc lập, 1.625 phép so, không một bất đồng",
  "Hệ số đồng thuận κ = 0,867 toàn tập, và 0,650 trên 1.652 bước hai nhánh viết câu khác nhau",
  "Luận văn nêu thẳng một lỗi cài đặt: phép chuẩn hoá quy “go back” về lớp chạm. Sửa lại thì điểm đổi 0,3 điểm, và ba nhánh đã chấm không được chấm lại",
  "Luật hộp phần tử của chính AndroidControl (Phụ lục D.3) cho mốc câu chuẩn 83,8, thứ tự tám nhánh không đổi; tính sau khi có điểm nên chỉ là thước báo kèm",
], M, 1.0, W - 2 * M, { fs: 12.5, gap: 0.9, itemH: 0.86, lh: 1.3 });
footB(); done();

// B4 · phép viết lại câu
slide();
bar("Dự phòng · Độ bền của thước trước cách diễn đạt khác");
table(M, 1.0, [2.8, 2.0, 1.9, 2.19], [
  { cells: ["Biến thể", "Phần bị tác động", "Điểm", "p"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12, align: ["left", "center", "center", "center"] },
  { cells: ["Đổi động từ thao tác", "725 bước", "76,8 → 77,0", "1,000"], h: 0.44, fs: 12.5, rule: true },
  { cells: ["Đảo trật tự mệnh đề", "211 bước", "89,6 → 90,0", "1,000"], h: 0.44, fs: 12.5, rule: true },
  { cells: ["Cả hai cùng lúc", "203 bước", "90,1 → 91,1", "0,480"], h: 0.44, fs: 12.5, rule: true },
  { cells: [{ t: "Bỏ mệnh đề vị trí", bold: true, color: RED }, "198 bước", { t: "89,4 → 85,9", bold: true, color: RED }, { t: "0,046", bold: true, color: RED }], h: 0.48, fs: 12.5 },
], { align: ["left", "center", "center", "center"] });
bullets([
  "Gộp ba biến thể bảo toàn nghĩa: 1.139 câu, hiệu ròng +0,35 điểm, KTC [−0,59 ; +1,29]",
  "Bỏ mệnh đề vị trí thì thước phạt đúng, nên đây không phải một thước bất động",
  "Dạng lỗi là tất cả hoặc không: trung vị sai số giữ nguyên, còn p90 bung từ 6,88 lên 31,16",
  "Phần bị tác động là phần dễ nhất, và phép viết lại này chưa đụng vào cách mô tả phần tử",
], M, 3.5, W - 2 * M, { fs: 12.5, gap: 0.7, itemH: 0.66, lh: 1.3 });
footB(); done();

// B5 · sàn và gọi tên vs chỉ chỗ
slide();
bar("Dự phòng · Sàn của thước, và gọi tên so với chỉ vị trí");
table(M, 1.05, [3.6, 3.5, 1.79], [
  { cells: ["Nhánh so sánh", "Câu bị thay thành gì", "Điểm"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12, align: ["left", "left", "center"] },
  { cells: ["Câu chung chung", "“Tap the button.” ở mọi bước", { t: "12,0", bold: true }], h: 0.46, fs: 12.5, rule: true },
  { cells: [{ t: "Câu sai màn hình", bold: true }, "câu thật của bước khác: đúng văn phong, sai nội dung", { t: "6,1", bold: true, color: RED }], h: 0.56, fs: 12.5, rule: true },
  { cells: ["Bỏ tên, giữ vị trí", "chỉ còn mệnh đề vị trí", "61,1"], h: 0.46, fs: 12.5 },
], { align: ["left", "left", "center"] });
bullets([
  "Việc gọi tên đắt gấp tám lần việc chỉ chỗ: bỏ tên mất 28,5 điểm, bỏ vị trí chỉ mất 3,5 điểm",
  "Con số phải trình là 28,5 điểm trên phần bị tác động, vì phép thử chỉ đụng 24,1% số bước",
  "Dải dùng được của thước là 62,9 điểm",
  "Suy đoán sàn khoảng 40% bị loại, vì nó suy từ tỉ lệ ba nhánh cùng trúng",
], M, 3.35, W - 2 * M, { fs: 12.5, gap: 0.72, itemH: 0.68, lh: 1.3 });
footB(); done();

// B6 · cấu hình và chi phí
slide();
bar("Dự phòng · Cấu hình huấn luyện và chi phí máy");
table(M, 1.05, [3.0, 5.89], [
  { cells: ["Hạng mục", "Cấu hình"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12.5 },
  { cells: ["Mô hình gốc", "Qwen2.5-VL-3B-Instruct"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["Cách tinh chỉnh", "QLoRA 4 bit, đóng băng phần thị giác"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["Độ dài và lô", "2.560 token, lô hiệu dụng 16, hai lượt duyệt, 8.072 bước"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["Máy và thời gian", "A100, 10,3 giây mỗi bước, khoảng 23 giờ mỗi lượt"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["Khâu chấm", "Kaggle T4 × 2, khoảng 5,6 giờ mỗi nhánh"], h: 0.4, fs: 12.5 },
]);
bullets([
  "QLoRA 4 bit chạy nhanh hơn bf16 ở bài này: 10,70 so với 14,76 giây mỗi bước",
  "Chỗ ngốn bộ nhớ là bảng logits, không phải trọng số",
  "Đổi loại card không làm đổi kết quả: cùng hạt giống thì mất mát 20 bước đầu trùng ba chữ số",
  "Ngân sách máy là lý do hạt giống thứ hai của nhánh xử lý bị huỷ",
], M, 3.75, W - 2 * M, { fs: 12.5, gap: 0.66, itemH: 0.62, lh: 1.3 });
footB(); done();

// B7 · trạng thái các nhánh
slide();
bar("Dự phòng · Trạng thái cuối của các nhánh trong thiết kế");
table(M, 0.8, [2.6, 1.8, 4.49], [
  { cells: ["Nhánh", "Trạng thái", "Lý do"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12, align: ["left", "center", "left"] },
  { cells: ["S1, hai hạt giống", { t: "đã chạy", color: TEAL, bold: true }, "nhánh nền, cho biết nhiễu là 0,52 điểm"], h: 0.42, fs: 11, rule: true },
  { cells: ["S2, hạt giống 101", { t: "đã chạy", color: TEAL, bold: true }, "một hạt giống, −1,93 điểm so với nhánh nền"], h: 0.42, fs: 11, rule: true },
  { cells: ["S2, hạt giống 202", { t: "huỷ", color: RED, bold: true }, "ngân sách máy; đại lượng chính không hoàn tất"], h: 0.42, fs: 11, rule: true },
  { cells: ["CE2-S2 và MIN-DESC", { t: "đã chạy", color: TEAL, bold: true }, "một hạt giống mỗi nhánh; MIN-DESC đạt 60,05"], h: 0.42, fs: 11, rule: true },
  { cells: ["Chặng ba, thưởng ô toạ độ", { t: "đã chạy", color: TEAL, bold: true }, "60,07, chênh +0,02 so với chặng hai; khai báo +2,56"], h: 0.42, fs: 11, rule: true },
  { cells: ["Nội suy hai bộ trọng số", { t: "xong, không cho gì", color: MAROON, bold: true }, "đường cong đơn điệu, cực đại rơi đúng vào một đầu mút"], h: 0.42, fs: 11, rule: true },
  { cells: ["S2r", { t: "không chạy", color: MAROON, bold: true }, "được thiết kế để chắc chắn thua nên giá trị thông tin thấp"], h: 0.42, fs: 11, rule: true },
  { cells: ["S2-nopoint", { t: "không chạy", color: MAROON, bold: true }, "chi phí gấp đôi chặng hai, mà ô toạ độ đã đo được là ô có ích"], h: 0.42, fs: 11, rule: true },
  { cells: ["MIN-ONPOLICY", { t: "dừng", color: RED, bold: true }, "dựng dữ liệu xong nhưng không đạt tiêu chí khả thi"], h: 0.42, fs: 11, rule: true },
  { cells: ["Nhánh ứng viên, hạt 101", { t: "đã chạy", color: TEAL, bold: true }, "không đạt ngưỡng chọn; executability 56,1, một hạt giống"], h: 0.42, fs: 11, rule: true },
  { cells: ["Nhánh so sánh cùng đầu vào", { t: "huỷ", color: RED, bold: true }, "ngân sách; không quy công được cho danh sách ứng viên"], h: 0.42, fs: 11, rule: true },
  { cells: ["Ngưỡng bỏ cuộc τ", { t: "giữ nguyên thắng", color: MAROON, bold: true }, "tốt nhất +8/1.400, dưới ngưỡng đặt trước"], h: 0.42, fs: 11 },
], { align: ["left", "center", "left"] });
block(M, 6.32, W - 2 * M, 0.62);
text("Luận văn báo mọi nhánh, kể cả nhánh dừng ở tiêu chí khả thi và kể cả khi kết quả đi ngược kỳ vọng.", { x: M + 0.25, y: 6.32, w: W - 2 * M - 0.5, h: 0.62, fontSize: 12.5, bold: true, color: NAVY, valign: "middle", margin: 0 });
footB(); done();

// B7b · nội suy hai bộ trọng số
slide();
bar("Dự phòng · Nội suy giữa hai bộ trọng số, và lý do không trích số trên tập chọn");
text("Ghép nối theo hạng hai bộ trọng số hạng thấp của chặng hai và chặng ba, chấm trên lát chọn 262 bước chạm", { x: M, y: 0.72, w: W - 2 * M, h: 0.32, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.2, [2.6, 1.34, 1.34, 1.34, 1.34, 1.13], [
  { cells: ["Hệ số trộn", "0,00", "0,25", "0,50", "0,75", "1,00"], bold: true, color: WHITE, fill: NAVY, h: 0.44, fs: 12, align: ["left", "center", "center", "center", "center", "center"] },
  { cells: ["Điểm trên lát chọn", "67,56", "67,94", "67,94", "67,94", { t: "68,32", bold: true }], h: 0.46, fs: 12.5, rule: true },
  { cells: [{ t: "Số bước câu đổi so với đầu mút", color: GREY }, { t: "0", color: GREY }, { t: "53", color: GREY }, { t: "95", color: GREY }, { t: "127", color: GREY }, { t: "155", color: GREY }], h: 0.44, fs: 11.5 },
], { align: ["left", "center", "center", "center", "center", "center"] });
bullets([
  "Đường cong đơn điệu, cực đại rơi đúng vào một đầu mút, tức không có điểm trộn nào tốt hơn hai bộ trọng số gốc",
  "Mọi khoảng tin cậy ghép cặp đều phủ 0; theo tiêu chí đặt trước, hệ số được khoá về 0 và bước chấm lại trên tập kiểm không chạy",
  "Số bước có câu thay đổi tăng đều theo hệ số trộn, nên phép ghép chạy đúng: kết quả bằng 0 là kết quả thật, không phải lỗi cài đặt",
], M + 0.15, 2.85, W - 2 * M - 0.3, { fs: 12.5, gap: 0.66, itemH: 0.62, lh: 1.25 });
block(M, 5.0, W - 2 * M, 1.35);
text([{ text: "Vì sao không con số nào trên lát chọn được đưa vào báo cáo.", options: { bold: true, color: RED } }, { text: "\nLát chọn nằm trong phần dữ liệu mà ba nhánh này đã học, nên điểm trên đó cao hơn tập kiểm khoảng 7,5 điểm, và phóng đại khoảng cách giữa hai nhánh gần 40 lần: 0,76 điểm trên lát chọn so với 0,02 điểm trên tập kiểm. Lát chọn chỉ dùng để xếp hạng ứng viên trong cùng một họ.", options: {} }], { x: M + 0.25, y: 5.05, w: W - 2 * M - 0.5, h: 1.25, fontSize: 12.5, margin: 0, lh: 1.3 });
footB(); done();

// B8 · MIN-ONPOLICY
slide();
bar("Dự phòng · Một biến thể đã thiết kế nhưng không dựng được dữ liệu");
bullets([
  "Ý tưởng là thay khai báo sai lấy từ phần tử cạnh bên bằng chính khai báo sai mà mô hình đã sinh ra",
  "Dữ liệu đã dựng thật: 14.000 màn, chỉ được 459 cặp, tức 3,3% so với ngưỡng khả thi 25%",
  "Ngưỡng này đặt trên tỉ lệ chứ không phải trên số lượng, nên sinh thêm dữ liệu không thay đổi kết luận",
  "Khoảng cách tới phần tử người dùng đã chạm có trung vị 351 điểm ảnh, 76,5% ngoài dải 80 đến 350",
  "Lỗi khai báo có hai cực: gọi đúng phần tử bằng tên khác, hoặc nhìn sang vùng khác hẳn",
], M, 1.05, W - 2 * M, { fs: 13, gap: 1.02, itemH: 0.98, lh: 1.3 });
footB(); done();

// B9 · vùng mù
slide();
bar("Dự phòng · Vùng mù của thước, theo cả hai chiều");
bullets([
  "Theo chiều bỏ sót, thước không phát hiện được độ lệch dưới khoảng 63 điểm ảnh",
  "Theo chiều kết oan, 1.083 bước mà chính câu chuẩn cũng không đạt, 72% do dụng cụ sai quá 14% bề màn",
  "935 bước, tức 21% quần thể, cả ba nhánh đều không đạt. Trần 75,7% vì vậy phản ánh năng lực dụng cụ hơn là giới hạn ngôn ngữ",
  "Luật Voronoi chỉ chặt bằng độ đầy đủ của bộ liệt kê phần tử; phép gộp hộp xoá nhầm phần tử riêng biệt ở 8,2% số bước",
  "Mức câu chuẩn cũng không phải chặn trên tuyệt đối: hợp ba nhánh giải được 79,1% số bước",
], M, 1.05, W - 2 * M, { fs: 13, gap: 1.02, itemH: 0.98, lh: 1.3 });
footB(); done();

// B10 · phép kiểm cơ học và bước không chạm
slide();
bar("Dự phòng · Phép kiểm cơ học và thiệt hại ở bước không chạm");
text("Phép kiểm cơ học đo thẳng độ chính xác ô khai báo, không gọi mô hình định vị (3.473 bước)", { x: M, y: 0.85, w: W - 2 * M, h: 0.3, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M + 0.55, 1.25, [3.0, 1.9, 2.9], [
  { cells: ["Điểm lưu", "Khai báo đúng", "Phần tăng thuộc về"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12, align: ["left", "center", "left"] },
  { cells: ["S2", "53,9%", ""], h: 0.44, fs: 12.5, rule: true },
  { cells: ["CE2-S2", "59,8%", { t: "+5,93  học có giám sát thuần", color: MAROON }], h: 0.44, fs: 12.5, rule: true },
  { cells: [{ t: "MIN-DESC", bold: true }, { t: "60,6%", bold: true }, { t: "+0,84  riêng mục tiêu ưu tiên", color: MAROON }], h: 0.44, fs: 12.5 },
], { align: ["left", "center", "left"] });
text("87,7% mức tăng ở tầng khai báo cũng thuộc về nhánh so sánh, khớp với 78% đo ở điểm đầu ra.", { x: M, y: 3.15, w: W - 2 * M, h: 0.32, fontSize: 13, bold: true, color: RED, margin: 0 });
bullets([
  "Một điểm cải thiện ở tầng khai báo đổi được 0,42 điểm executability",
  "Điều kiện không gây hại không đạt: lớp thao tác giảm 19,75 điểm ở bước không chạm, ngưỡng là 3",
  "Nguyên nhân là thiết kế dữ liệu, vì tập cặp chỉ chứa bước chạm",
  "Cách gỡ là trộn bước không chạm dạng entropy chéo thuần vào chặng hai",
], M, 3.6, W - 2 * M, { fs: 12.5, gap: 0.68, itemH: 0.64, lh: 1.3 });
footB(); done();


// B11 · luật hộp phần tử D.3
slide();
bar("Dự phòng · Luật hộp phần tử của chính AndroidControl (Phụ lục D.3)");
text("Điểm dự đoán nằm trong hộp bao của phần tử cần chạm. Tính lại từ bản ghi từng bước ngày 5/9, sau khi đã có mọi điểm, không gọi lại mô hình định vị.", { x: M, y: 0.85, w: W - 2 * M, h: 0.55, fontSize: 12, italic: true, color: GREY, margin: 0, lh: 1.3 });
table(M, 1.5, [3.3, 1.8, 1.9, 1.89], [
  { cells: ["Nhánh", "Ô Voronoi", "Hộp D.3", "D.3 và cửa sổ 14%"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12, align: ["left", "center", "center", "center"] },
  { cells: [{ t: "Câu chuẩn", italic: true }, "75,7", { t: "83,8", bold: true }, "79,2"], h: 0.42, fs: 12.5, rule: true },
  { cells: [{ t: "Chặng ba", bold: true }, "60,07", { t: "67,0", bold: true }, "63,0"], h: 0.42, fs: 12.5, rule: true },
  { cells: ["MIN-DESC", "60,05", "66,5", "62,7"], h: 0.42, fs: 12.5, rule: true },
  { cells: ["S1, hạt giống 101", "59,1", "65,5", "61,7"], h: 0.42, fs: 12.5, rule: true },
  { cells: ["Nhánh ứng viên", "56,1", "62,4", "58,6"], h: 0.42, fs: 12.5, rule: true },
  { cells: ["Base", "47,6", "53,6", "49,8"], h: 0.42, fs: 12.5, rule: "322164", ruleW: 1.5 },
  { cells: ["Sàn: câu chung chung (lát 800)", "12,0", "14,1", "12,1"], h: 0.42, fs: 12.5, rule: true },
  { cells: ["Sàn: câu của màn khác (lát 800)", "6,1", "8,6", "6,6"], h: 0.42, fs: 12.5 },
], { align: ["left", "center", "center", "center"] });
bullets([
  "Nâng trần gần gấp bốn lần mức nâng sàn, nên dải dùng được rộng ra chứ không bị nén",
  "Hộp do luận văn suy từ cây trợ năng: 48% là nút con không nhận chạm, nên chặt hơn nhãn gốc",
  "78% mức tăng đến từ hộp rộng hơn nửa màn; 120 bước rơi vào khung chứa rộng khiến bước đó gần như mặc nhiên được tính đạt",
  "Hiệu MIN-DESC trên S1 vẫn +0,9 đến +1,1 dưới mọi biến thể: luật này không thêm bằng chứng cho đóng góp mô hình",
], M, 5.0, W - 2 * M, { fs: 11.5, gap: 0.5, itemH: 0.46, lh: 1.25 });
footB(); done();

// B12 · nhánh ứng viên: bốn dấu hiệu và thủ tục ngưỡng
slide();
bar("Dự phòng · Nhánh ứng viên: dấu hiệu của bỏ cuộc và thủ tục ngưỡng");
text("Chỉ bước có đáp án trong danh sách", { x: M, y: 0.85, w: 4.6, h: 0.3, fontSize: 12.5, bold: true, color: NAVY, margin: 0 });
table(M, 1.2, [1.7, 0.8, 1.1, 0.9], [
  { cells: ["Số dòng", "n", "Bỏ cuộc", "Exec."], bold: true, color: WHITE, fill: NAVY, h: 0.38, fs: 11.5, align: ["left", "center", "center", "center"] },
  { cells: ["1 đến 5", "178", "18,5%", "70,8"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["6 đến 10", "363", "15,7%", "70,5"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["11 đến 20", "826", "25,9%", "60,3"], h: 0.36, fs: 11.5, rule: true },
  { cells: ["21 đến 39", "1.036", "29,3%", "55,6"], h: 0.36, fs: 11.5, rule: true },
  { cells: [{ t: "40, chạm trần", bold: true }, "795", { t: "33,2%", bold: true, color: RED }, { t: "51,8", bold: true }], h: 0.36, fs: 11.5 },
], { align: ["left", "center", "center", "center"] });
text("Tương quan hậu kiểm, không phải nhân quả: màn nhiều phần tử cũng là màn khó hơn.", { x: M, y: 3.45, w: 4.6, h: 0.6, fontSize: 11, italic: true, color: GREY, margin: 0, lh: 1.3 });
text("Bốn dấu hiệu đi kèm việc bỏ cuộc", { x: 5.45, y: 0.85, w: 4.0, h: 0.3, fontSize: 12.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Câu mang động từ không chạm: 28,3% so với 0,97%, gấp 29 lần",
  "Sai số mô hình định vị: trung vị 19,9% so với 0,78% bề ngang màn",
  "Danh sách càng dài thì tỉ lệ bỏ cuộc càng cao, đơn điệu",
  "Ứng dụng chưa xuất hiện trong tập dạy: 51,3% so với 41,8% (n = 78, chỉ là gợi ý)",
  "Đã loại: độ dài câu, trung vị 33 ký tự ở cả hai nhóm",
], 5.45, 1.25, 4.0, { fs: 11.5, gap: 0.58, itemH: 0.54, lh: 1.25 });
block(M, 4.3, W - 2 * M, 1.95);
text([{ text: "Thủ tục chọn ngưỡng bỏ cuộc, cố định trước khi tính điểm nào.", options: { bold: true, color: NAVY } }, { text: " Ép từng thẻ chọn vào mô hình, lấy log-xác suất trung bình theo token; chọn ứng viên tốt nhất khi biên so với thẻ bỏ cuộc vượt τ. Quét τ chỉ trên lát 1.400, theo độ đúng toàn bộ lát; lưới chứa cả phương án giữ nguyên, cải thiện dưới 18 bước thì giữ nguyên thắng. Kỳ vọng ghi trước: 0 đến 3 điểm. Kết quả: giữ nguyên thắng, tốt nhất +8/1.400, KTC [−11; +27]; điểm thẻ none ở bước có vàng và không có vàng trùng nhau (AUC 0,69–0,72). Huấn luyện lại không chạy.", options: {} }], { x: M + 0.25, y: 4.3, w: W - 2 * M - 0.5, h: 1.95, fontSize: 12, valign: "middle", margin: 0, lh: 1.35 });
footB(); done();

// B13 · tự phản biện trần suy từ lát cắt
slide();
bar("Dự phòng · Một trần suy từ lát cắt theo hành vi mô hình thì trôi theo cách chia nhóm");
text("Cùng một can thiệp giả định, đổi cách định nghĩa nhóm ba lần, giữ nguyên mọi thứ khác (n = 4.437)", { x: M, y: 0.9, w: W - 2 * M, h: 0.32, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.32, [3.45, 0.95, 1.15, 1.15, 1.15, 1.04], [
  { cells: ["Cách định nghĩa nhóm", "n", "MIN", "S1", "Câu chuẩn", "Trần"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 11.5, align: ["left", "center", "center", "center", "center", "center"] },
  { cells: ["mô hình đang đo nhìn sai", "1.327", "8,44", "24,49", "55,69", { t: "+4,80", bold: true, color: RED }], h: 0.44, fs: 11.5, rule: true },
  { cells: ["mô hình khác nhìn sai", "1.256", "11,94", "22,13", "54,70", { t: "+2,88", bold: true }], h: 0.44, fs: 11.5, rule: true },
  { cells: ["bỏ hẳn việc chọn theo lỗi của nó", "113", "62,83", "34,51", "60,18", { t: "−0,72", bold: true, color: TEAL }], h: 0.44, fs: 11.5, rule: true },
  { cells: [{ t: "độ khó đọc từ màn hình", bold: true }, "1.331", "58,53", "56,35", "73,55", { t: "−0,65", bold: true, color: TEAL }], h: 0.46, fs: 11.5 },
], { align: ["left", "center", "center", "center", "center", "center"] });
bullets([
  "Cột trần đi từ +4,80 xuống −0,65, trong khi cột câu chuẩn gần như đứng yên",
  "Đại lượng trôi theo cách chia nhóm là ưu thế giữa hai mô hình cùng họ, không phải dư địa thật",
  "Luận văn áp phép kiểm này cho cả những con số thuận lợi của chính mình",
], M + 0.15, 3.75, W - 2 * M - 0.3, { fs: 13, gap: 0.62, itemH: 0.58, lh: 1.25 });
block(M, 5.7, W - 2 * M, 0.7);
text([{ text: "Phép kiểm này đã ngăn một lượt huấn luyện được đề xuất trên căn cứ 4,80 điểm.", options: { bold: true, color: NAVY } }], { x: M + 0.25, y: 5.7, w: W - 2 * M - 0.5, h: 0.7, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.3 });
footB(); done();

// B14 · đổi luật chấm thì kết luận cũng đổi
slide();
bar("Dự phòng · Đổi luật chấm thì kết luận thống kê cũng đổi");
text("Chặng ba so với nhánh chỉ sinh câu, trên đủ 4.463 bước, ba luật cùng đòi đúng loại thao tác", { x: M, y: 0.9, w: W - 2 * M, h: 0.32, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.35, [3.6, 1.4, 1.5, 2.39], [
  { cells: ["Luật chấm", "Δ", "p", "Sau hiệu chỉnh Holm"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 12, align: ["left", "center", "center", "center"] },
  { cells: ["±14% từng trục", "+2,13", "0,0003", { t: "giữ ý nghĩa", color: TEAL }], h: 0.5, fs: 13, rule: true },
  { cells: ["AitW Euclid", "+1,99", "0,0010", { t: "giữ ý nghĩa", color: TEAL }], h: 0.5, fs: 13, rule: true },
  { cells: [{ t: "Voronoi (thước tiêu đề)", bold: true }, { t: "+0,96", bold: true }, { t: "0,0860", bold: true }, { t: "MẤT ý nghĩa", bold: true, color: RED }], h: 0.54, fs: 13 },
], { align: ["left", "center", "center", "center"] });
bullets([
  "Đổi sang luật dung sai đơn thuần biến một phép so không có ý nghĩa thành có ý nghĩa",
  "Cùng lúc đó nó kéo mức chênh từ 0,96 lên 2,13 điểm",
  [{ text: "Câu rỗng nghĩa đạt 12,00 dưới thước tiêu đề nhưng 20,50 dưới luật lỏng ", options: {} }, { text: "⇒ 86% mức tăng là thứ câu vô nghĩa cũng lấy được", options: { bold: true, color: MAROON } }],
], M + 0.15, 3.55, W - 2 * M - 0.3, { fs: 13, gap: 0.66, itemH: 0.62, lh: 1.25 });
block(M, 5.6, W - 2 * M, 0.7);
text([{ text: "Đó là lý do luật chấm được cố định trước khi có điểm số, và không đổi về sau.", options: { bold: true, color: NAVY } }], { x: M + 0.25, y: 5.6, w: W - 2 * M - 0.5, h: 0.7, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.3 });
footB(); done();

// ---- xuất ----
done();
pres.writeFile({ fileName: "../LUAN_VAN_SLIDE_BAOCAO.pptx" }).then(() => {
  const html = `<!doctype html><meta charset="utf-8"><title>Preview - slide bao ve</title>
<style>body{background:#555;margin:0;padding:24px;font-family:sans-serif}
.slide{position:relative;width:960px;height:720px;margin:0 auto 24px;box-shadow:0 3px 14px rgba(0,0,0,.5);overflow:hidden}</style>
${htmlSlides.join("\n")}`;
  fs.mkdirSync("_preview", { recursive: true });
  fs.writeFileSync("_preview/preview_baove.html", html);
  console.log("Xong: ../LUAN_VAN_SLIDE_BAOCAO.pptx  |  slide chinh: " + PAGE + "  |  du phong: " + BPAGE);
});
