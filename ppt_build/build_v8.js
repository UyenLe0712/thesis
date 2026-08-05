// Deck v8 — soạn từ report/101_PIPELINE_MODEL_CHI_TIET.md (29/7).
// Bản 3 (29/7) theo góp ý: bỏ slide khâu 0 (nguyên liệu gộp vào slide toàn cảnh),
// viết lại khâu 3 cho rõ "dùng làm gì", khâu 4 nói thẳng đây là NHÃN ghép sẵn thành
// bộ dữ liệu rồi mới đưa sang khâu 5, bỏ bảng giá tiền, bỏ slide "chưa chốt",
// slide bốn nhánh đổi thành "huấn luyện bốn lần".
// Xuất: ../LUAN_VAN_SLIDE_v8.pptx + _preview_v8/preview.html
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Luan van thac si";
pres.title = "Pipeline mo hinh - sinh huong dan su dung phan mem";

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
  rect(x - 0.07, y - 0.07, w + 0.14, h + (cap ? 0.46 : 0.14), WHITE, { radius: 0.07, line: RULE, lw: 1, shadow: true });
  image(path, x, y, w, h);
  if (cap) text(cap, { x: x - 0.07, y: y + h + 0.03, w: w + 0.14, h: 0.34, align: "center", valign: "middle", fontSize: 11, bold: true, color: INK, fontFace: BF, margin: 0, lh: 1.15 });
}
function arrow(x, y, w, c) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || ACCENT, width: 2.5, endArrowType: "triangle" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX - 1}px;width:${w * PX}px;height:0;border-top:2.5px solid #${c || ACCENT}"></div><div style="position:absolute;left:${(x + w) * PX - 5}px;top:${y * PX - 5}px;width:0;height:0;border-left:8px solid #${c || ACCENT};border-top:5px solid transparent;border-bottom:5px solid transparent"></div>`);
}
function vArrow(x, y, h, c) {
  s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color: c || ACCENT, width: 2.5, endArrowType: "triangle" } });
  hpush(`<div style="position:absolute;left:${x * PX - 1}px;top:${y * PX}px;height:${h * PX}px;width:0;border-left:2.5px solid #${c || ACCENT}"></div><div style="position:absolute;left:${x * PX - 5}px;top:${(y + h) * PX - 5}px;width:0;height:0;border-top:8px solid #${c || ACCENT};border-left:5px solid transparent;border-right:5px solid transparent"></div>`);
}
function circle(x, y, d, fill, glyph, gc) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" } });
  hpush(`<div style="position:absolute;left:${x * PX}px;top:${y * PX}px;width:${d * PX}px;height:${d * PX}px;border-radius:50%;background:#${fill}"></div>`);
  if (glyph) text(glyph, { x, y, w: d, h: d, align: "center", valign: "middle", fontSize: d * 34, bold: true, color: gc || WHITE, fontFace: TF, margin: 0 });
}
function note(t) { s.addNotes(t.trim()); }
function kicker(t) { text(t.toUpperCase(), { x: M, y: 0.64, w: W - 2 * M, h: 0.3, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, spacing: 2.5, margin: 0 }); }
function title(t) { text(t, { x: M, y: 1.0, w: W - 2 * M, h: 0.9, fontSize: 27, bold: true, color: INK, fontFace: TF, margin: 0, lh: 1.05 }); }
function head(k, t) { kicker(k); title(t); }
function pageno() { PAGE++; text(String(PAGE).padStart(2, "0"), { x: W - 1.05, y: H - 0.5, w: 0.6, h: 0.3, fontSize: 10, color: MUTE, align: "right", fontFace: BF, margin: 0 }); }
function kết(t, y) {
  text(t, { x: M, y: y || 6.55, w: W - 2 * M, h: 0.5, fontSize: 15, bold: true, color: INK, fontFace: TF, margin: 0, lh: 1.2 });
}
function stat(x, y, w, num, label, color, hl) {
  rect(x, y, w, 1.05, hl ? TINT : FILL, { radius: 0.09 });
  text(num, { x, y: y + 0.1, w, h: 0.5, fontSize: 25, bold: true, color: color, fontFace: TF, align: "center", margin: 0 });
  text(label, { x: x + 0.1, y: y + 0.63, w: w - 0.2, h: 0.35, fontSize: 11, color: BODY, fontFace: BF, align: "center", margin: 0, lh: 1.15 });
}

// ══════════════════════════════════════════════ 1 · BÌA
slide(NAVY);
text("LUẬN VĂN THẠC SĨ · PHẦN MÔ HÌNH", { x: M, y: 1.5, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Mô hình được dựng ra\nnhư thế nào", { x: M - 0.02, y: 2.15, w: 9.6, h: 1.9, fontSize: 34, bold: true, color: WHITE, fontFace: TF, lh: 1.08, margin: 0 });
text("Từ thao tác của người thật tới câu hướng dẫn chạy trên điện thoại", { x: M, y: 4.35, w: 9.4, h: 0.6, fontSize: 16, italic: true, color: "C9D2DC", fontFace: TF, margin: 0 });
text("Học viên · · · · ·        Giảng viên hướng dẫn · · · · ·        2026", { x: M, y: 6.55, w: 11, h: 0.4, fontSize: 13, color: "8FA0B2", fontFace: BF, margin: 0 });
shot("real_mv_1.png", 10.5, 1.95, 1.9, 3.35);
done();

// ══════════════════════════════════════════════ 2 · TOÀN CẢNH
slide();
head("Toàn cảnh", "Bốn khâu dựng dữ liệu, một khâu huấn luyện, rồi chạy thật");
rect(M, 2.35, W - 2 * M, 0.62, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "Nguyên liệu — bộ AndroidControl:  ", options: { bold: true, color: INK } }, { text: "ảnh màn hình  ·  toạ độ người thật chạm  ·  câu hướng dẫn người viết", options: { color: BODY } }], { x: M + 0.3, y: 2.35, w: W - 2 * M - 0.6, h: 0.62, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0 });

const steps = [["1", "Đọc chữ trên ảnh"], ["2", "Viết lại câu"], ["3", "Dựng phần mô tả"], ["4", "Ghép thành bộ dữ liệu"], ["5", "Huấn luyện"]];
steps.forEach((t, i) => {
  const x = M + (i % 3) * 3.95, y = 3.25 + Math.floor(i / 3) * 1.3;
  rect(x, y, 3.66, 1.0, FILL, { radius: 0.1 });
  circle(x + 0.24, y + 0.26, 0.5, STEEL, t[0], WHITE);
  text(t[1], { x: x + 0.88, y, w: 2.6, h: 1.0, fontSize: 14, bold: true, color: INK, fontFace: BF, valign: "middle", margin: 0, lh: 1.2 });
  if (i % 3 < 2) arrow(x + 3.72, y + 0.5, 0.18, MUTE);
});
rect(M + 7.9, 4.55, 3.66, 1.0, TINT, { radius: 0.1 });
circle(M + 8.14, 4.81, 0.5, ACCENT, "6", WHITE);
text("Chạy thật", { x: M + 8.78, y: 4.55, w: 2.6, h: 1.0, fontSize: 14, bold: true, color: ACCENT, fontFace: BF, valign: "middle", margin: 0 });

rect(M, 5.85, 7.4, 0.62, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text("Khâu 1–4 chạy một lần trên máy cá nhân, miễn phí.", { x: M + 0.3, y: 5.85, w: 6.8, h: 0.62, fontSize: 12.5, color: BODY, fontFace: BF, valign: "middle", margin: 0 });
kết("Bốn khâu đầu chỉ để chế ra bộ dữ liệu. Mô hình chỉ xuất hiện ở khâu 5.", 6.7);
note(`Đây là bản đồ cả phần mô hình. Nguyên liệu là bộ AndroidControl: người thật thao tác trên điện thoại Pixel khoảng một năm, mỗi bước có ảnh màn hình, toạ độ chỗ họ chạm, và một câu hướng dẫn do người viết.
Bốn khâu đầu đều là chế biến dữ liệu, chưa động tới mô hình mình train: khâu 1 đọc chữ trên ảnh, khâu 2 viết lại câu cho tự đủ, khâu 3 dựng phần mô tả phần tử, khâu 4 ghép tất cả thành bộ dữ liệu huấn luyện. Bốn khâu này chạy một lần trên máy cá nhân, không tốn tiền, nên rủi ro kiểm được trước.
Khâu 5 mới là huấn luyện. Khâu 6 là lúc chạy thật trên máy người dùng.`);
pageno(); done();

// ══════════════════════════════════════════════ 3 · KHÂU 1
slide();
head("Khâu 1 · đọc chữ trên ảnh", "Chọn bộ đọc chữ chạy được trên điện thoại — và biết nó yếu chỗ nào");
shot("real_mv_2.png", M, 2.5, 2.2, 3.6);
rect(3.5, 2.5, 8.9, 0.8, FILL, { radius: 0.1 });
text("Chạy trên CPU, ngay trên điện thoại, miễn phí.", { x: 3.8, y: 2.5, w: 8.35, h: 0.8, fontSize: 13, bold: true, color: INK, fontFace: BF, valign: "middle", margin: 0 });
const ocr = [["22", "dòng chữ mỗi màn", STEEL, false], ["40%", "có chữ ngay tại nút", STEEL, false], ["57%", "có chữ gần nút", GOOD, false], ["43%", "không có chữ nào gần", BAD, true]];
let ox = 3.5;
ocr.forEach(c => { stat(ox, 3.55, 2.13, c[0], c[1], c[2], c[3]); ox += 2.26; });
rect(3.5, 4.85, 8.9, 0.8, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "Chữ đọc ra không sạch:  ", options: { bold: true, color: INK } }, { text: "“Corn syrup .nd Jam”   ·   “11:35M”   ·   kính lúp thành “Q”", options: { color: BODY } }], { x: 3.8, y: 4.85, w: 8.35, h: 0.8, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0 });
kết("Nhiễu thì để nguyên nhiễu — mô hình học với chính danh sách này.", 6.4);
note(`Dùng RapidOCR trên nền ONNX. Không phải vì chính xác nhất, mà vì nó khớp câu chuyện triển khai: chạy trên CPU, chạy được ngay trên điện thoại, miễn phí. Đổi sang dịch vụ đọc chữ trên mạng thì sạch hơn nhưng hỏng luận điểm chạy offline, mà ảnh màn hình thường có thông tin riêng tư.
Kết quả trả về là từng dòng chữ kèm toạ độ tâm và vị trí theo lưới ba nhân ba, ví dụ trên đỉnh giữa. Ghi vị trí thô thay vì số pixel vì mô hình ngôn ngữ xử lý kiểu đó tự nhiên hơn và không phụ thuộc kích thước màn.
Số đo trên 1.069 bước chạm: trung vị 22 dòng chữ mỗi màn, 40% có chữ ngay tại nút, 57% có chữ gần nút, và 43% không có chữ nào gần. Con số 43% đó là nút hình: dấu cộng, mũi tên, biểu tượng chia sẻ. Nó ảnh hưởng thẳng tới khâu 3.
Danh sách nhiễu là cố ý giữ nguyên, vì mô hình được huấn luyện với chính danh sách đó nên phải học cả khi nào không nên tin.`);
pageno(); done();

// ══════════════════════════════════════════════ 4 · KHÂU 2
slide();
head("Khâu 2 · viết lại câu", "Câu người viết quá cụt để làm đáp án mẫu");
shot("ac_o1.png", M, 2.5, 1.9, 3.4, "khoanh dấu tại chỗ\nngười thật chạm");
rect(3.2, 2.5, 4.3, 1.35, FILL, { radius: 0.1 });
text("Câu gốc  ·  trung vị 6 từ", { x: 3.45, y: 2.62, w: 3.85, h: 0.3, fontSize: 11.5, bold: true, color: MUTE, fontFace: BF, margin: 0 });
text("“Click on the search bar”", { x: 3.45, y: 3.0, w: 3.85, h: 0.6, fontSize: 14, italic: true, color: BODY, fontFace: TF, margin: 0, lh: 1.25 });
arrow(7.6, 3.18, 0.35);
rect(8.1, 2.5, 4.3, 1.35, TINT, { radius: 0.1 });
text("Sau khi viết lại", { x: 8.35, y: 2.62, w: 3.85, h: 0.3, fontSize: 11.5, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("“Tap the ‘Search Publications,\nStories & Interest’ bar at the top”", { x: 8.35, y: 3.0, w: 3.85, h: 0.7, fontSize: 12.5, italic: true, color: INK, fontFace: TF, margin: 0, lh: 1.3 });

rect(3.2, 4.05, 9.2, 0.8, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "Ai viết lại:  ", options: { bold: true, color: INK } }, { text: "một mô hình lớn, xem ảnh đã khoanh dấu. Chạy một lần lúc dựng dữ liệu.", options: { color: BODY } }], { x: 3.45, y: 4.05, w: 8.7, h: 0.8, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0 });

text("Ba điều bắt buộc", { x: 3.2, y: 5.0, w: 5, h: 0.32, fontSize: 13.5, bold: true, color: INK, fontFace: TF, margin: 0 });
["Mô hình viết lại phải khác họ với mốc đem so",
 "Có nhánh viết lại mù ảnh — tách thông tin khỏi độ dài",
 "Soi tay 100 câu, đếm tỉ lệ bịa tên"].forEach((t, i) => {
  rect(3.2, 5.38 + i * 0.48, 9.2, 0.42, i === 1 ? TINT : FILL, { radius: 0.06 });
  text(t, { x: 3.45, y: 5.38 + i * 0.48, w: 8.7, h: 0.42, fontSize: 12, color: i === 1 ? ACCENT : BODY, bold: i === 1, fontFace: BF, valign: "middle", margin: 0 });
});
text("Khâu này là tiền xử lý dữ liệu, không kể vào tính mới.", { x: M, y: 6.95, w: 10.5, h: 0.32, fontSize: 12, italic: true, color: STEEL, fontFace: TF, margin: 0 });
note(`Câu hướng dẫn người viết trong bộ dữ liệu quá cụt để làm đáp án mẫu: trung vị 6 từ, gần nửa dưới 5 từ, nhiều câu mơ hồ kiểu Tap the app, có câu hỏng hẳn như Click on the top at the bottom right corner. Mô hình học bắt chước sẽ học đúng giọng cụt đó và tự chặn trần của mình — đo được là câu cộc lốc trỏ trúng 35%, câu tả rõ phần tử trỏ trúng 69%.
Cách làm: lấy toạ độ chỗ người thật chạm, khoanh dấu lên ảnh tại đúng chỗ đó, đưa ảnh có dấu cộng câu gốc cho một mô hình lớn, yêu cầu viết lại thành câu tự đủ và giữ nguyên nghĩa thao tác. Lúc huấn luyện thì dùng ảnh sạch, không có dấu.
Vì sao hợp lệ: mô hình viết lại được cầm đáp án, nó thấy dấu khoanh nên chỉ mô tả một chỗ đã được chỉ sẵn. Cái truyền lại là chất lượng câu chữ, không phải năng lực định vị.
Ba điều bắt buộc. Một, mô hình viết lại phải khác họ với mốc đem so, nếu không thì phản biện nói ngay học từ ai thì cùng lắm bằng người đó. Hai, phải có nhánh viết lại mù ảnh: cùng mô hình, cùng yêu cầu viết dài hơn, nhưng không cho xem ảnh và dấu — để tách thông tin khỏi độ dài. Ba, soi tay khoảng 100 câu đếm tỉ lệ bịa tên phần tử.
Và nói rõ ngay: khâu này là tiền xử lý dữ liệu, cách khoanh dấu rồi nhờ mô hình lớn viết mô tả đã có người làm trong miền giao diện, nên không kể vào tính mới.`);
pageno(); done();

// ══════════════════════════════════════════════ 5 · KHÂU 3
slide();
head("Khâu 3 · dựng phần mô tả", "Chế thêm một dòng đứng TRƯỚC câu, tả phần tử cần chạm là cái gì");
// bang chuyen: toa do -> hop -> bon truong
rect(M, 2.45, 3.0, 0.85, FILL, { radius: 0.09 });
text("toạ độ chỗ người chạm", { x: M, y: 2.45, w: 3.0, h: 0.85, fontSize: 12.5, bold: true, color: INK, fontFace: BF, align: "center", valign: "middle", margin: 0, lh: 1.25 });
arrow(4.05, 2.87, 0.4);
rect(4.6, 2.45, 3.2, 0.85, FILL, { radius: 0.09 });
text("hộp phần tử tại đó\n(từ cây trợ năng)", { x: 4.6, y: 2.45, w: 3.2, h: 0.85, fontSize: 12.5, bold: true, color: INK, fontFace: BF, align: "center", valign: "middle", margin: 0, lh: 1.25 });
arrow(7.9, 2.87, 0.4);
rect(8.45, 2.45, 3.95, 0.85, TINT, { radius: 0.09 });
text("bốn trường mô tả", { x: 8.45, y: 2.45, w: 3.95, h: 0.85, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, align: "center", valign: "middle", margin: 0 });

rect(M, 3.5, W - 2 * M, 0.75, WHITE, { radius: 0.09, line: ACCENT, lw: 1.3 });
text("[  vai trò   |   chữ hoặc hình   |   vị trí trên màn   |   dấu hiệu phân biệt  ]", { x: M, y: 3.5, w: W - 2 * M, h: 0.75, fontSize: 16, bold: true, color: ACCENT, fontFace: TF, align: "center", valign: "middle", margin: 0 });

rect(M, 4.45, 5.6, 0.75, WHITE, { radius: 0.09, line: GOOD, lw: 1.3 });
text([{ text: "Ô tìm kiếm:  ", options: { bold: true, color: GOOD } }, { text: "[ô nhập liệu | “Search Publications…” | trên đỉnh, giữa]", options: { color: BODY } }], { x: M + 0.25, y: 4.45, w: 5.1, h: 0.75, fontSize: 11.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
rect(6.8, 4.45, 5.6, 0.75, WHITE, { radius: 0.09, line: BAD, lw: 1.3 });
text([{ text: "Kính lúp:  ", options: { bold: true, color: BAD } }, { text: "[nút | ? | trên đỉnh, bên phải]", options: { color: BODY } }], { x: 7.05, y: 4.45, w: 5.1, h: 0.75, fontSize: 11.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });

rect(M, 5.42, 7.4, 0.85, NAVY, { radius: 0.09 });
text([{ text: "Dùng làm gì:  ", options: { bold: true, color: "F0C9A8" } }, { text: "ghép vào trước câu, thành nửa đầu của đáp án mẫu — mô hình phải tả phần tử rồi mới được viết câu.", options: { color: WHITE } }], { x: M + 0.3, y: 5.42, w: 6.8, h: 0.85, fontSize: 12, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
stat(8.6, 5.42, 3.8, "43%", "bước không lấy được tên từ đâu cả", BAD, true);
kết("Rủi ro: tầng giữa mà rỗng thì hai tầng tệ hơn một tầng.", 6.65);
note(`Khâu này chế ra nửa đầu của đáp án mẫu, nên nói rõ nó dùng làm gì.
Cách dựng, ba bước, hoàn toàn tự động: lấy toạ độ chỗ người thật chạm, tra ra hộp phần tử nằm tại đúng chỗ đó trong cây trợ năng của hệ điều hành, rồi rút thành bốn trường.
Bốn trường là: vai trò lấy từ class_name của hộp, ví dụ EditText là ô nhập liệu; chữ hoặc hình lấy từ bộ đọc chữ nhưng chỉ tính chữ nằm trong hộp; vị trí quy về lưới ba nhân ba; dấu hiệu phân biệt là xem có phần tử nào khác cùng loại cùng chữ ở gần không, ví dụ có một kính lúp nữa bên phải.
Dùng làm gì: dòng bốn trường này ghép vào TRƯỚC câu hướng dẫn, thành nửa đầu của đáp án mẫu ở khâu 4. Nhờ vậy mô hình bị buộc phải nói ra phần tử là cái gì, ở đâu, rồi mới được viết câu. Lúc chấm thì cắt bỏ dòng đó đi, chỉ lấy câu.
Rủi ro lớn nhất của cả pipeline nằm ở đây: cây trợ năng chỉ 12,6% phần tử có tên, bộ đọc chữ chỉ phủ 57% bước chạm, cộng lại còn khoảng 43% bước không lấy được tên từ đâu cả. Nút hình thì xử bằng cách cắt ảnh vùng hộp ra nhờ mô hình mô tả ngắn. Nhưng nếu tầng giữa mà rỗng thì mô hình chẳng có gì để chép, hai tầng hoá ra tệ hơn một tầng. Nên việc đầu tiên, miễn phí, là dựng thử vài trăm bước rồi soi tay đếm bao nhiêu phần trăm dùng được.`);
pageno(); done();

// ══════════════════════════════════════════════ 6 · KHÂU 4
slide();
head("Khâu 4 · ghép thành bộ dữ liệu", "Chưa mô hình nào sinh gì ở đây — đây là nhãn ghép sẵn");
rect(M, 2.45, 5.85, 2.55, FILL, { radius: 0.1 });
text("ĐỀ BÀI", { x: M + 0.28, y: 2.56, w: 5.3, h: 0.3, fontSize: 11.5, bold: true, color: STEEL, fontFace: BF, spacing: 1.5, margin: 0 });
rect(M + 0.28, 2.92, 1.0, 0.8, WHITE, { radius: 0.06, line: RULE, lw: 1 });
text("ảnh\nSẠCH", { x: M + 0.28, y: 2.92, w: 1.0, h: 0.8, fontSize: 10.5, bold: true, color: MUTE, fontFace: BF, align: "center", valign: "middle", margin: 0, lh: 1.2 });
text("Mục tiêu:  tìm bài “Saudis to host\nUkraine’s peace summit”", { x: M + 1.45, y: 3.0, w: 4.2, h: 0.65, fontSize: 11, color: INK, fontFace: BF, margin: 0, lh: 1.3 });
text("Chữ nhìn thấy:  “Search Publications, Stories & Interest”\n(trên đỉnh, giữa)  ·  “Recommended”  ·  …", { x: M + 0.28, y: 3.9, w: 5.5, h: 0.7, fontSize: 10.5, color: BODY, fontFace: BF, margin: 0, lh: 1.35 });
text("← khâu 1", { x: M + 4.55, y: 4.62, w: 1.2, h: 0.28, fontSize: 10, italic: true, color: MUTE, fontFace: BF, margin: 0 });

arrow(6.95, 3.7, 0.35);
rect(7.5, 2.45, 4.9, 2.55, TINT, { radius: 0.1 });
text("ĐÁP ÁN MẪU", { x: 7.78, y: 2.56, w: 4.4, h: 0.3, fontSize: 11.5, bold: true, color: ACCENT, fontFace: BF, spacing: 1.5, margin: 0 });
rect(7.78, 2.92, 4.35, 0.95, WHITE, { radius: 0.07, line: ACCENT, lw: 1.3 });
text("[ô nhập liệu | “Search Publications…”\n| trên đỉnh, giữa]", { x: 7.9, y: 2.92, w: 4.1, h: 0.95, fontSize: 10.5, color: ACCENT, fontFace: BF, valign: "middle", margin: 0, lh: 1.35 });
text("← khâu 3 dựng", { x: 7.78, y: 3.9, w: 2.2, h: 0.26, fontSize: 10, italic: true, color: MUTE, fontFace: BF, margin: 0 });
rect(7.78, 4.16, 4.35, 0.75, WHITE, { radius: 0.07, line: RULE, lw: 1 });
text("Tap the “Search Publications…” bar\nat the top", { x: 7.9, y: 4.16, w: 4.1, h: 0.75, fontSize: 10.5, color: INK, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
text("← khâu 2 viết", { x: 7.78, y: 4.94, w: 2.2, h: 0.26, fontSize: 10, italic: true, color: MUTE, fontFace: BF, margin: 0 });

vArrow(6.6, 5.15, 0.3);
rect(M, 5.5, W - 2 * M, 0.72, NAVY, { radius: 0.09 });
text("một dòng dữ liệu   ×   hàng nghìn bước   =   bộ dữ liệu huấn luyện   →   khâu 5", { x: M, y: 5.5, w: W - 2 * M, h: 0.72, fontSize: 14, bold: true, color: WHITE, fontFace: TF, align: "center", valign: "middle", margin: 0 });
kết("Lúc huấn luyện, mô hình tập viết ra đúng đáp án mẫu này.\nLúc chạy thật nó tự viết, không ai đưa gì.", 6.4);
note(`Slide này quan trọng nhất, và cũng là chỗ dễ hiểu nhầm nhất, nên nói thật rõ.
Ở khâu 4 chưa có mô hình nào sinh ra cái gì cả. Đây thuần tuý là ghép nhãn. Bên trái là đề bài: ảnh sạch không có dấu khoanh, mục tiêu của tác vụ, các bước đã làm, và danh sách chữ nhìn thấy do khâu 1 đọc ra. Bên phải là đáp án mẫu, gồm hai nửa ghép lại: nửa trên là dòng bốn trường do khâu 3 dựng tự động, nửa dưới là câu do khâu 2 viết lại.
Một cặp đề bài và đáp án mẫu là một dòng dữ liệu. Hàng nghìn bước cho hàng nghìn dòng, gộp lại thành bộ dữ liệu huấn luyện, rồi mới đưa sang khâu 5.
Lúc huấn luyện, mô hình tập viết ra đúng chuỗi đáp án mẫu đó. Lúc chạy thật thì không ai đưa đáp án, mô hình tự viết cả hai phần — và đó chính là chỗ nó hành xử khác so với bản huấn luyện thường.
Ba chi tiết đáng nêu: ảnh trong đề bài là ảnh sạch, dấu khoanh chỉ tồn tại ở khâu 2. Dòng mô tả nằm ở đáp án chứ không nằm ở đề bài, nên mô hình phải tự sinh chứ không được mớm. Và toạ độ đúng không xuất hiện ở đâu trong dòng dữ liệu này, nó chỉ dùng để dựng nhãn rồi biến mất.`);
pageno(); done();

// ══════════════════════════════════════════════ 7 · KHÂU 5
slide();
head("Khâu 5 · huấn luyện", "Qwen2.5-VL-3B, chỉnh nhẹ bằng QLoRA trên một card thuê");
const why = [["Mô hình mở", "để tự huấn luyện được và chạy offline"],
             ["Nhỏ", "3 tỉ tham số vừa một card 24GB"],
             ["Đọc được ảnh dày chữ", "mô hình nhỏ khác nén ảnh, mất chữ nút"],
             ["Có tiền lệ cùng miền", "nhiều mô hình giao diện dựng trên nền này"]];
let wy = 2.6;
why.forEach(r => {
  rect(M, wy, W - 2 * M, 0.82, FILL, { radius: 0.08 });
  text(r[0], { x: M + 0.3, y: wy, w: 4.0, h: 0.82, fontSize: 14, bold: true, color: INK, fontFace: BF, valign: "middle", margin: 0 });
  text(r[1], { x: M + 4.4, y: wy, w: 6.8, h: 0.82, fontSize: 12.5, color: BODY, fontFace: BF, valign: "middle", margin: 0, lh: 1.2 });
  wy += 0.9;
});
rect(M, 6.3, W - 2 * M, 0.72, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "QLoRA:  ", options: { bold: true, color: INK } }, { text: "chỉ chỉnh một lượng nhỏ tham số thêm vào, giữ nguyên phần lớn mô hình gốc. Nhờ vậy vừa một card thuê rẻ.", options: { color: BODY } }], { x: M + 0.3, y: 6.3, w: W - 2 * M - 0.6, h: 0.72, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.28 });
note(`Mô hình nền Qwen2.5-VL-3B, giấy phép Apache-2.0. Bốn lý do chọn: phải là mô hình mở vì đề tài buộc tự huấn luyện và triển khai là chạy offline, mô hình đóng thì không fine-tune được; phải nhỏ vì máy thuê một card 24GB, bản 3 tỉ với QLoRA vừa khít; phải đọc được ảnh giao diện dày chữ, đây là chỗ nhiều mô hình nhỏ khác đuối vì nén ảnh làm mất chữ nút; và đã có tiền lệ ngay trên miền giao diện cùng cỡ.
QLoRA nghĩa là chỉ chỉnh một lượng nhỏ tham số thêm vào, giữ nguyên phần lớn mô hình gốc ở dạng nén. Dự kiến đóng băng phần thị giác, chỉ chỉnh phần ngôn ngữ và lớp nối. Hàm mất mát là cross entropy trên từng chữ của phần đáp án, gồm cả dòng mô tả lẫn câu. Một lượt huấn luyện ước 6 tới 10 giờ card A100.
Chỗ chưa chốt là mức thu nhỏ ảnh: ảnh điện thoại 1080 nhân 2400 rất cao, giữ lớn thì đọc được chữ nút nhỏ nhưng chuỗi dài và tốn, thu nhỏ thì nhanh nhưng mất chữ nút, đúng thứ tác vụ này cần. Phải thử vài mức.`);
pageno(); done();

// ══════════════════════════════════════════════ 8 · KHÂU 6
slide();
head("Khâu 6 · lúc chạy thật", "Chỉ hai thứ nằm trên máy người dùng");
rect(M, 2.6, 2.55, 0.95, FILL, { radius: 0.09 });
text("một ảnh\n+ một câu hỏi", { x: M, y: 2.6, w: 2.55, h: 0.95, fontSize: 12.5, bold: true, color: INK, fontFace: BF, align: "center", valign: "middle", margin: 0, lh: 1.3 });
arrow(3.6, 3.07, 0.4);
rect(4.2, 2.6, 2.4, 0.95, WHITE, { radius: 0.09, line: STEEL, lw: 1.3 });
text("bộ đọc chữ", { x: 4.2, y: 2.6, w: 2.4, h: 0.95, fontSize: 12.5, bold: true, color: STEEL, fontFace: BF, align: "center", valign: "middle", margin: 0 });
arrow(6.68, 3.07, 0.4);
rect(7.28, 2.6, 2.75, 0.95, TINT, { radius: 0.09, line: ACCENT, lw: 1.3 });
text("Qwen-3B đã huấn luyện", { x: 7.28, y: 2.6, w: 2.75, h: 0.95, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, align: "center", valign: "middle", margin: 0, lh: 1.25 });
vArrow(8.65, 3.62, 0.35);
rect(5.9, 4.08, 5.6, 0.9, WHITE, { radius: 0.08, line: RULE, lw: 1 });
text("[ô nhập liệu | “Search Publications…” | trên đỉnh, giữa]\nTap the “Search Publications…” bar at the top", { x: 6.05, y: 4.08, w: 5.3, h: 0.9, fontSize: 11, color: BODY, fontFace: BF, valign: "middle", margin: 0, lh: 1.4 });
text("cắt bỏ dòng mô tả", { x: 8.9, y: 5.06, w: 2.4, h: 0.3, fontSize: 10.5, italic: true, color: MUTE, fontFace: BF, margin: 0 });
vArrow(8.65, 5.06, 0.35);
rect(5.9, 5.5, 5.6, 0.72, NAVY, { radius: 0.08 });
text("người dùng nhận: câu hướng dẫn", { x: 5.9, y: 5.5, w: 5.6, h: 0.72, fontSize: 13, bold: true, color: WHITE, fontFace: BF, align: "center", valign: "middle", margin: 0 });

rect(M, 4.08, 4.6, 0.9, WHITE, { radius: 0.09, line: GOOD, lw: 1.3 });
text([{ text: "Cần:  ", options: { bold: true, color: GOOD } }, { text: "bộ đọc chữ và mô hình. Không cần mạng.", options: { color: BODY } }], { x: M + 0.25, y: 4.08, w: 4.1, h: 0.9, fontSize: 12, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
rect(M, 5.15, 4.6, 1.07, FILL, { radius: 0.09 });
text([{ text: "Không cần:  ", options: { bold: true, color: INK } }, { text: "toạ độ đúng, cây trợ năng, mô hình lớn, bộ trỏ.", options: { color: BODY } }], { x: M + 0.25, y: 5.15, w: 4.1, h: 1.07, fontSize: 12, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
kết("Mô tả sai thì câu sai theo. Cách phát hiện: so mô tả mô hình sinh ra với nhãn đã dựng.", 6.55);
note(`Lúc chạy thật rất gọn. Người dùng đưa một ảnh màn hình và một câu hỏi. Bộ đọc chữ chạy trên máy cho ra danh sách chữ kèm vị trí. Cả hai đi vào mô hình. Mô hình tự sinh dòng mô tả rồi tới câu. Cắt bỏ dòng mô tả, đưa câu cho người dùng.
Chỉ hai thứ nằm trên máy người dùng: bộ đọc chữ và mô hình. Không cần mạng, không phải gửi ảnh màn hình đi đâu, mà ảnh màn hình thường có thông tin riêng tư.
Không cần toạ độ đúng, cây trợ năng, mô hình lớn hay bộ trỏ — những thứ đó chỉ tồn tại lúc dựng dữ liệu và lúc chấm.
Câu hỏi phải chủ động nêu: nếu mô hình mô tả sai thì câu sai theo, nhìn nhầm sang nút bên cạnh rồi hướng dẫn bấm nút đó, gọi là lỗi lan truyền. Cách phát hiện là so phần mô tả mô hình sinh ra với nhãn đã dựng sẵn, đếm tỉ lệ nêu đúng phần tử. Nếu tỉ lệ đó thấp mà điểm câu vẫn cao thì phải giải thích được chứ không lờ đi.`);
pageno(); done();

// ══════════════════════════════════════════════ 9 · BỐN LẦN HUẤN LUYỆN
slide();
head("Huấn luyện bốn lần", "Bốn mô hình, cùng nền cùng dữ liệu — chỉ khác đáp án mẫu");
text("Đáp án mẫu gồm gì", { x: M + 5.0, y: 2.42, w: 3.2, h: 0.3, fontSize: 11, bold: true, color: MUTE, fontFace: BF, spacing: 1, margin: 0 });
text("Để làm gì", { x: M + 8.5, y: 2.42, w: 2.8, h: 0.3, fontSize: 11, bold: true, color: MUTE, fontFace: BF, spacing: 1, margin: 0 });
const br = [["Bản thường", "câu người viết", "mốc trong", false],
            ["Trên câu viết lại", "câu viết lại", "tầng nền để so", false],
            ["Trên câu viết lại mù ảnh", "câu viết lại mù", "đối chứng độ dài", false],
            ["Có thêm dòng mô tả", "mô tả + câu viết lại", "phần đóng góp", true]];
let by = 2.8;
br.forEach(r => {
  rect(M, by, W - 2 * M, 0.85, r[3] ? TINT : FILL, { radius: 0.08 });
  text(r[0], { x: M + 0.3, y: by, w: 4.6, h: 0.85, fontSize: 14, bold: true, color: r[3] ? ACCENT : INK, fontFace: BF, valign: "middle", margin: 0 });
  text(r[1], { x: M + 5.0, y: by, w: 3.3, h: 0.85, fontSize: 13, bold: r[3], color: r[3] ? ACCENT : BODY, fontFace: BF, valign: "middle", margin: 0 });
  text(r[2], { x: M + 8.5, y: by, w: 2.8, h: 0.85, fontSize: 12.5, color: r[3] ? ACCENT : STEEL, fontFace: BF, valign: "middle", margin: 0 });
  by += 0.93;
});
kết("So hàng cuối với hàng thứ hai: cùng dữ liệu, cùng giọng,\nchỉ khác việc mô hình có phải tả phần tử trước khi viết câu hay không.", 6.5);
note(`Bốn lần huấn luyện ra bốn mô hình, dùng chung mô hình nền, chung cách huấn luyện, chung bộ ảnh. Chỉ khác đúng một thứ: đáp án mẫu gồm những gì.
Lần một, đáp án là câu người viết nguyên bản — đây là bản thường, làm mốc trong. Lần hai, đáp án là câu đã viết lại ở khâu 2 — đây là tầng nền. Lần ba, đáp án là câu viết lại nhưng mô hình lớn không được xem ảnh, tức câu dài tương đương mà không có thông tin đặc quyền — dùng làm đối chứng để tách thông tin khỏi độ dài. Lần bốn, đáp án có thêm dòng mô tả đứng trước câu — đây là phần đóng góp.
Kết luận đọc ở hiệu số giữa lần bốn và lần hai, vì hai lần đó cùng dữ liệu cùng giọng, chỉ khác đúng một yếu tố là mô hình có phải tả phần tử trước khi viết câu hay không. Bố trí như vậy để phần dữ liệu không lẫn vào phần mô hình, tránh đòn phản biện rằng đóng góp thực ra chỉ là đóng góp dữ liệu.`);
pageno(); done();

// ---- write ----
fs.mkdirSync("_preview_v8", { recursive: true });
const page = `<!doctype html><meta charset="utf-8"><style>@page{size:${W}in ${H}in;margin:0}*{margin:0;box-sizing:border-box}.slide{position:relative;width:${W}in;height:${H}in;overflow:hidden;page-break-after:always}</style>` + htmlSlides.join("\n");
fs.writeFileSync("_preview_v8/preview.html", page);
pres.writeFile({ fileName: "../LUAN_VAN_SLIDE_v8.pptx" }).then(f => console.log("PPTX ->", f, "| slides:", htmlSlides.length)).catch(e => console.error("ERR", e));
