// Deck v7 — bản gọn soạn từ report/98 (bản 28/7 sau vòng phản biện) + report/99.
// Khác v6: ít chữ hơn hẳn; bỏ khoe 44.7, trình DẢI 19.7-44.7 tuỳ độ chặt của cách chấm;
// thêm kết quả bơm lỗi bản 2 (8/10 ngưỡng) và điều kiện tiên quyết của Cổng A
// (bộ trỏ phải lệch dưới 3% cạnh, vì ở mức 8% cách chấm chặt chấm oan 59% câu đúng);
// Cổng A chốt UGround (OS-Atlas nhiễm AndroidControl), bỏ chữ "đầu tiên".
// 29/7 (bản 2): trụ đóng góp mô hình = "mô tả trước, phát ngôn sau"; slide 5B viết lại,
// thêm slide 5C về tính mới (nói phần không mới trước); câu hỏi cuối rút còn 4.
// Xuất: ../LUAN_VAN_SLIDE_v7.pptx + _preview_v7/preview.html
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Luan van thac si";
pres.title = "Sinh huong dan su dung phan mem cho nguoi doc";

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
  if (cap) text(cap, { x: x - 0.07, y: y + h + 0.03, w: w + 0.14, h: 0.34, align: "center", valign: "middle", fontSize: 12, bold: true, color: INK, fontFace: BF, margin: 0 });
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
function kicker(t) { text(t.toUpperCase(), { x: M, y: 0.64, w: W - 2 * M, h: 0.3, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, spacing: 2.5, margin: 0 }); }
function title(t) { text(t, { x: M, y: 1.0, w: W - 2 * M, h: 0.9, fontSize: 27, bold: true, color: INK, fontFace: TF, margin: 0, lh: 1.05 }); }
function head(k, t) { kicker(k); title(t); }
function pageno() { PAGE++; text(String(PAGE).padStart(2, "0"), { x: W - 1.05, y: H - 0.5, w: 0.6, h: 0.3, fontSize: 10, color: MUTE, align: "right", fontFace: BF, margin: 0 }); }

// ══════════════════════════════════════════════ 1 · BÌA
slide(NAVY);
text("LUẬN VĂN THẠC SĨ · BÁO CÁO TIẾN ĐỘ", { x: M, y: 1.5, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Sinh hướng dẫn sử dụng\nphần mềm cho người đọc", { x: M - 0.02, y: 2.15, w: 9.6, h: 1.9, fontSize: 34, bold: true, color: WHITE, fontFace: TF, lh: 1.08, margin: 0 });
text("Một ảnh màn hình, một câu hỏi, trả về các bước để người tự làm theo", { x: M, y: 4.3, w: 9.4, h: 0.6, fontSize: 16, italic: true, color: "C9D2DC", fontFace: TF, margin: 0 });
text("Học viên · · · · ·        Giảng viên hướng dẫn · · · · ·        2026", { x: M, y: 6.55, w: 11, h: 0.4, fontSize: 13, color: "8FA0B2", fontFace: BF, margin: 0 });
shot("real_mv_1.png", 10.5, 1.95, 1.9, 3.35);
done();

// ══════════════════════════════════════════════ 2 · BÀI TOÁN
slide();
head("Bài toán", "Một màn hình, một câu hỏi, các bước cho người làm theo");
shot("real_mv_2.png", M, 2.4, 2.45, 4.2);
rect(3.9, 2.45, 8.5, 1.45, TINT, { radius: 0.1 });
text([{ text: "Hỏi:  ", options: { bold: true, color: ACCENT } }, { text: "“Làm sao thêm một việc mới rồi lưu lại?”", options: { color: INK, italic: true } }], { x: 4.2, y: 2.5, w: 8, h: 0.6, fontSize: 16, fontFace: BF, valign: "middle", margin: 0 });
text([{ text: "Đáp:  ", options: { bold: true, color: STEEL } }, { text: "1. Nhập tên việc   2. Điền số giờ   3. Chạm SAVE & ADD ANOTHER", options: { color: BODY } }], { x: 4.2, y: 3.1, w: 8, h: 0.7, fontSize: 14, fontFace: BF, valign: "middle", margin: 0 });

rect(3.9, 4.15, 8.5, 0.85, FILL, { radius: 0.1 });
text([{ text: "Chỗ khác với các mô hình giao diện đang có:  ", options: { bold: true, color: INK } }, { text: "chúng sinh thao tác để máy tự bấm, ở đây sinh câu cho người đọc.", options: { color: BODY } }], { x: 4.2, y: 4.15, w: 7.9, h: 0.85, fontSize: 13.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });

text("Khó không nằm ở chỗ sinh câu, mà ở chỗ CHẤM", { x: 3.9, y: 5.2, w: 8.5, h: 0.45, fontSize: 17, bold: true, color: INK, fontFace: TF, margin: 0 });
rect(3.9, 5.72, 4.15, 0.9, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text("Không có bộ hướng dẫn mẫu\nnào để đối chiếu.", { x: 4.15, y: 5.72, w: 3.7, h: 0.9, fontSize: 13, color: BODY, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
rect(8.25, 5.72, 4.15, 0.9, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text("Thuê người ngồi chấm thì\ntốn và khó lặp lại.", { x: 8.5, y: 5.72, w: 3.7, h: 0.9, fontSize: 13, color: BODY, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
note(`Vào là một ảnh màn hình cộng một câu hỏi, ra là các bước để người tự làm theo.
Khác biệt cốt lõi so với mọi mô hình giao diện khác: chúng sinh thao tác để máy tự bấm (toạ độ, mã lệnh), ở đây sinh câu chữ cho con người đọc.
Cái khó nằm ở chỗ chấm: không có bộ hướng dẫn chuẩn do người soạn, mà thuê người chấm thì tốn kém và khó lặp lại. Đây là lý do luận văn có hai phần ngang nhau: mô hình, và cách chấm.`);
pageno(); done();

// ══════════════════════════════════════════════ 3 · ĐỔI HƯỚNG
slide();
head("Vì sao trục chính là đo độ ĐÚNG", "Hướng đầu tiên bị chính số liệu bác bỏ");
rect(M, 2.45, 5.3, 3.0, FILL, { radius: 0.1 });
text("Nghĩ ban đầu", { x: M + 0.3, y: 2.65, w: 4.7, h: 0.4, fontSize: 15, bold: true, color: MUTE, fontFace: TF, margin: 0 });
text("Mô hình lớn hay bịa tên nút.\nLọc bỏ chỗ bịa rồi dạy mô hình\nnhỏ, nó sẽ trung thực hơn.\n\nXem việc lọc đó là đóng góp.", { x: M + 0.3, y: 3.1, w: 4.7, h: 2.1, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.4, margin: 0 });
arrow(6.45, 3.95, 0.6);
rect(7.25, 2.45, 5.15, 3.0, TINT, { radius: 0.1 });
text("Đọc tay 80 màn để kiểm", { x: 7.55, y: 2.65, w: 4.5, h: 0.4, fontSize: 15, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Mô hình gần như không bịa,\nchỉ 0 tới 2%.\n\nChỗ tưởng bịa hoá ra là nút có\nthật, chỉ do danh sách nút của\nAndroid bỏ sót nhãn.", { x: 7.55, y: 3.1, w: 4.5, h: 2.1, fontSize: 13.5, color: INK, fontFace: BF, lh: 1.4, margin: 0 });
rect(M, 5.75, W - 2 * M, 1.0, NAVY, { radius: 0.1 });
text([{ text: "Nên đổi:  ", options: { bold: true, color: "F0C9A8" } }, { text: "không còn gì để lọc, nên bỏ hướng chống bịa. Mô hình tự huấn luyện vẫn là trung tâm, nhưng trục chính chuyển sang đo độ ĐÚNG: hướng dẫn có dẫn tới đúng nút cần bấm hay không.", options: { color: WHITE } }], { x: M + 0.3, y: 5.75, w: W - 2 * M - 0.6, h: 1.0, fontSize: 14, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
note(`Chỗ này cho thấy cách làm việc. Sau góp ý của thầy là cần một mô hình tự huấn luyện chứ không chỉ prompting, hướng đầu tiên nghĩ tới là: mô hình lớn hay bịa tên nút, nên lọc bịa rồi dạy mô hình nhỏ, coi đó là đóng góp.
Nhưng kiểm trước bằng cách đọc tay 80 màn do gpt-4o-mini sinh: nó gần như không bịa, chỉ 0 tới 2%. Trong 40 ca tưởng là bịa thì 35 ca là nút có thật mà View Hierarchy bỏ sót nhãn, phần lớn là nút hình như dấu cộng, dấu tích.
Vì vậy bỏ hẳn khung lọc bịa, chuyển trục chính sang đo độ đúng. Sẵn sàng bỏ một khung đã dày công dựng khi số liệu nói nó sai, đó là tinh thần muốn giữ suốt luận văn.`);
pageno(); done();

// ══════════════════════════════════════════════ 4 · BA LUỒNG
slide();
head("Hệ thống chạy thế nào", "Ba luồng: dạy, chạy thật, và chấm");
const col = [
  ["① DẠY", ACCENT, "ảnh một bước + mục tiêu\n→ câu người viết", "Qwen2.5-VL-3B học viết cho\ngiống người thật, bằng QLoRA."],
  ["② CHẠY THẬT", STEEL, "1 ảnh + 1 câu hỏi\n→ hướng dẫn", "Chỉ cần ảnh màn hình. Không\ncần danh sách nút, không đáp án."],
  ["③ CHẤM", GOOD, "câu → bộ trỏ → (x, y)\n→ so với toạ độ đúng", "Phần có chất mới nhất.\nChi tiết ở slide sau."],
];
let cx = M;
col.forEach((c, i) => {
  rect(cx, 2.45, 3.7, 2.85, i === 2 ? TINT : FILL, { radius: 0.1 });
  text(c[0], { x: cx + 0.25, y: 2.65, w: 3.3, h: 0.4, fontSize: 15.5, bold: true, color: c[1], fontFace: TF, margin: 0 });
  rect(cx + 0.25, 3.12, 3.2, 0.88, WHITE, { radius: 0.07, line: RULE, lw: 1 });
  text(c[2], { x: cx + 0.4, y: 3.12, w: 2.95, h: 0.88, fontSize: 12, bold: true, color: INK, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
  text(c[3], { x: cx + 0.25, y: 4.12, w: 3.25, h: 1.0, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
  if (i < 2) arrow(cx + 3.78, 3.85, 0.32);
  cx += 4.1;
});
rect(M, 5.5, W - 2 * M, 0.68, WHITE, { radius: 0.09, line: ACCENT, lw: 1.4 });
text([{ text: "Chống ăn gian:  ", options: { bold: true, color: ACCENT } }, { text: "danh sách nút và đáp án chỉ dùng lúc dạy và lúc chấm, không bao giờ đưa lúc sinh. App đem chấm chưa từng xuất hiện lúc dạy.", options: { color: BODY } }], { x: M + 0.3, y: 5.5, w: W - 2 * M - 0.6, h: 0.68, fontSize: 13, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
rect(M, 6.26, W - 2 * M, 0.68, NAVY, { radius: 0.09 });
text([{ text: "Dữ liệu.  ", options: { bold: true, color: "F0C9A8" } }, { text: "Dạy: chỉ AndroidControl, lấy câu người viết sẵn. Chấm: AndroidControl 631 episode app lạ cho độ đúng, MobileViews cho độ bịa, ScreenSpot cho bộ trỏ.", options: { color: WHITE } }], { x: M + 0.3, y: 6.26, w: W - 2 * M - 0.6, h: 0.68, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
note(`Ba luồng nối tiếp nhau. Một là dạy: mỗi bước trong AndroidControl cho một cặp gồm ảnh màn hình của bước đó cộng mục tiêu, đáp án là câu hướng dẫn người thật đã viết. Train Qwen2.5-VL-3B bằng QLoRA, tức fine-tune nhẹ chạy được trên một GPU thuê rẻ.
Hai là lúc chạy thật: người dùng chỉ đưa một ảnh cộng một câu hỏi. Không cần View Hierarchy, không cần đáp án, nên dùng được ngoài đời vì điện thoại nào cũng có ảnh màn hình.
Ba là chấm, phần có chất mới nhất, nói kỹ ở slide sau.
Nguyên tắc chống ăn gian: View Hierarchy và đáp án chỉ vào lúc dạy và lúc chấm. App test tách hẳn khỏi app train, nên làm đúng trên app lạ nghĩa là học được kỹ năng thật chứ không học thuộc.`);
pageno(); done();

// ══════════════════════════════════════════════ 5 · MÔ HÌNH
slide();
head("Phần thứ nhất: mô hình", "Qwen2.5-VL-3B, mở, chạy offline, huấn luyện bằng LoRA");
const rows = [
  ["gpt-4o-mini", "mốc ngoài, không huấn luyện", STEEL, false],
  ["Qwen-3B huấn luyện thường", "mốc trong", STEEL, false],
  ["trên câu đích đã viết lại", "tầng nền, là dữ liệu", STEEL, false],
  ["mô tả trước, phát ngôn sau", "TRỤ đóng góp mô hình", ACCENT, true],
];
let ry = 2.45;
rows.forEach(r => {
  rect(M, ry, 6.6, 0.72, r[3] ? TINT : FILL, { radius: 0.08 });
  text(r[0], { x: M + 0.22, y: ry, w: 3.5, h: 0.72, fontSize: 13.5, bold: r[3], color: r[3] ? ACCENT : INK, fontFace: BF, valign: "middle", margin: 0 });
  text(r[1], { x: M + 3.75, y: ry, w: 2.7, h: 0.72, fontSize: 11.5, color: r[2], fontFace: BF, valign: "middle", margin: 0, lh: 1.15 });
  ry += 0.82;
});
rect(7.9, 2.45, 4.5, 2.98, NAVY, { radius: 0.1 });
text("Hai phép so", { x: 8.15, y: 2.62, w: 4.0, h: 0.4, fontSize: 15, bold: true, color: "F0C9A8", fontFace: TF, margin: 0 });
text("Đóng góp mô hình đo ở đâu:\nhiệu số giữa hàng cuối và hàng\ntrên nó. Cùng dữ liệu, cùng giọng,\nchỉ khác việc mô hình có phải\nphát ngôn qua tầng mô tả không.", { x: 8.15, y: 3.08, w: 4.05, h: 1.4, fontSize: 12.5, color: WHITE, fontFace: BF, lh: 1.35, margin: 0 });
text("Nhờ vậy phần dữ liệu không lẫn\nvào phần mô hình.", { x: 8.15, y: 4.6, w: 4.05, h: 0.8, fontSize: 12.5, color: "C9D2DC", fontFace: BF, lh: 1.35, margin: 0 });

rect(M, 5.65, W - 2 * M, 1.05, FILL, { radius: 0.1 });
text([{ text: "Cả bốn nhánh Qwen-3B đều huấn luyện thật, chỉnh trọng số bằng QLoRA.  ", options: { bold: true, color: INK } }, { text: "Mô hình lớn chỉ chạy một lần để viết lại câu đích rồi bỏ, không nằm trong hệ chạy thật. Trụ đóng góp nằm ngay trong đích huấn luyện, không phải cách ra lệnh cho một mô hình có sẵn.", options: { color: BODY } }], { x: M + 0.3, y: 5.65, w: W - 2 * M - 0.6, h: 1.05, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
note(`Chọn Qwen2.5-VL-3B vì bốn ràng buộc: phải là mô hình mở để tự huấn luyện được và chạy offline; phải nhỏ để train nổi trên Colab thuê, bản 3B với QLoRA vừa một GPU 24GB; phải đọc được ảnh giao diện dày chữ, Qwen xử lý ảnh phân giải cao; và đã có tiền lệ ngay trên miền giao diện, như UI-R1 ở AAAI 2026 hay ZonUI ở WACV 2026 đều dựng trên Qwen 3B.
Nếu thầy hỏi 3B nhỏ vậy có gì mới: chọn 3B không phải điểm mới, mô hình giao diện nhỏ đã đông. Cái mới nằm ở tác vụ và ở cách đánh giá.
Hai phép so cần phân định rõ. Kết luận chính đặt ở phép so với bản huấn luyện thường, vì cùng gốc cùng dữ liệu chỉ khác một yếu tố nên sạch. Phép so với gpt-4o-mini chỉ để minh hoạ, vì mô hình mình train ngay trên AndroidControl nên thuộc cả cách chia bước của bộ đó, có lợi thế cấu trúc ngoài chất lượng.
Một bẫy tránh: không dạy bằng đầu ra của gpt-4o rồi lại lấy chính gpt-4o làm mốc để vượt, vì học từ ai thì cùng lắm bằng người đó. Nên tín hiệu dạy là câu người viết.`);
pageno(); done();

// ══════════════════════════════════════════════ 5B · TRỤ ĐÓNG GÓP
slide();
head("Trụ đóng góp mô hình", "Bắt mô hình nêu phần tử là cái gì, rồi mới cho viết câu");

rect(M, 2.35, W - 2 * M, 0.6, FILL, { radius: 0.08 });
text([{ text: "Vì sao cần:  ", options: { bold: true, color: INK } }, { text: "câu người viết trung vị chỉ 6 từ, mô hình học đúng giọng cụt đó nên tự chặn trần của mình. Câu cộc lốc trỏ trúng 35%, câu tả rõ trỏ trúng 69%.", options: { color: BODY } }], { x: M + 0.28, y: 2.35, w: W - 2 * M - 0.56, h: 0.6, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0 });

// so đích huấn luyện
rect(M, 3.12, 5.5, 2.25, FILL, { radius: 0.1 });
text("Bản thường học", { x: M + 0.28, y: 3.28, w: 5.0, h: 0.36, fontSize: 14.5, bold: true, color: MUTE, fontFace: TF, margin: 0 });
rect(M + 0.28, 3.7, 4.95, 0.72, WHITE, { radius: 0.07, line: RULE, lw: 1 });
text("Click on the search bar at the top", { x: M + 0.42, y: 3.7, w: 4.7, h: 0.72, fontSize: 11.5, color: BODY, fontFace: BF, valign: "middle", margin: 0 });
text("Không có chỗ nào buộc nó nêu ra\nphần tử là cái gì trước khi viết.", { x: M + 0.28, y: 4.52, w: 5.0, h: 0.75, fontSize: 12, color: BODY, fontFace: BF, lh: 1.32, margin: 0 });

rect(6.9, 3.12, 5.5, 2.25, TINT, { radius: 0.1 });
text("Bản có trụ học", { x: 7.18, y: 3.28, w: 5.0, h: 0.36, fontSize: 14.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
rect(7.18, 3.7, 4.95, 0.72, WHITE, { radius: 0.07, line: ACCENT, lw: 1.2 });
text("[ô nhập liệu | “Search Publications…” |\ntrên đỉnh, giữa] → Tap the “Search\nPublications…” bar at the top", { x: 7.32, y: 3.7, w: 4.7, h: 0.72, fontSize: 10, color: INK, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
text("Nhãn tầng mô tả dựng TỰ ĐỘNG từ hộp\nphần tử tại đúng chỗ người thật chạm,\ncộng chữ đọc được trong hộp đó.", { x: 7.18, y: 4.52, w: 5.0, h: 0.75, fontSize: 12, color: INK, fontFace: BF, lh: 1.32, margin: 0 });

rect(M, 5.52, W - 2 * M, 0.72, NAVY, { radius: 0.1 });
text([{ text: "Vì sao là đóng góp MÔ HÌNH:  ", options: { bold: true, color: "F0C9A8" } }, { text: "đây là thứ duy nhất làm mô hình lúc chạy hành xử khác — nó buộc phải phát ngôn qua một tầng trung gian được giám sát. Lúc chấm, phần mô tả cắt bỏ, chỉ lấy câu.", options: { color: WHITE } }], { x: M + 0.3, y: 5.52, w: W - 2 * M - 0.6, h: 0.72, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });

rect(M, 6.36, W - 2 * M, 0.62, WHITE, { radius: 0.09, line: BAD, lw: 1.2 });
text([{ text: "Rủi ro lớn nhất, phải đo trước:  ", options: { bold: true, color: BAD } }, { text: "tầng mô tả cần TÊN phần tử, mà cây trợ năng chỉ 12,6% có tên. Tầng giữa mà rác thì hai tầng tệ hơn một tầng.", options: { color: BODY } }], { x: M + 0.3, y: 6.36, w: W - 2 * M - 0.6, h: 0.62, fontSize: 12, fontFace: BF, valign: "middle", margin: 0 });
note(`Đây là phần lõi của đóng góp mô hình, nên nói kỹ.
Vấn đề: câu người viết trong bộ dữ liệu trung vị chỉ 6 từ, gần nửa dưới 5 từ, có câu hỏng hẳn. Mô hình học bắt chước nên học đúng giọng cụt đó, tự chặn trần của chính nó. Số đo: câu cộc lốc trỏ trúng 35%, câu tả rõ phần tử trỏ trúng 69%.
Cách làm: đích huấn luyện có hai tầng. Mô hình phải sinh trước bộ mô tả có cấu trúc gồm vai trò, chữ hoặc hình, vị trí, dấu hiệu phân biệt, rồi mới sinh câu. Nhãn tầng mô tả dựng tự động từ hộp phần tử tại đúng điểm người thật chạm, cộng chữ đọc được trong hộp, nút hình thì mô tả bằng cách cắt ảnh. Không cần người gán, không cần mô hình đóng.
Cơ chế: mô hình sinh chữ theo thứ tự, mỗi chữ sinh ra thành ngữ cảnh cho chữ sau. Khi bắt nó nêu tên và vị trí trước, tới lúc viết câu thì thông tin định danh đã nằm trong ngữ cảnh do chính nó tạo ra, nên không viết được câu cụt nữa.
Vì sao là đóng góp mô hình chứ không phải dữ liệu: đây là thứ duy nhất trong các phương án làm mô hình lúc chạy hành xử khác. Các phương án khác chỉ đổi dữ liệu rồi huấn luyện như thường.
Rủi ro phải nói trước: tầng mô tả cần tên phần tử, mà cây trợ năng chỉ 12,6% có tên và bộ đọc chữ không đọc được nút hình thuần. Nên việc đầu tiên là đo chất lượng tầng giữa trên mẫu soi tay, trước khi tiêu tiền.`);
pageno(); done();

// ══════════════════════════════════════════════ 5C · TÍNH MỚI
slide();
head("Tính mới nằm ở đâu", "Nói phần không mới trước, rồi mới nói phần mới");

rect(M, 2.4, 5.5, 2.7, FILL, { radius: 0.1 });
text("Không mới, và sẽ nói thẳng", { x: M + 0.28, y: 2.58, w: 5.0, h: 0.36, fontSize: 14.5, bold: true, color: MUTE, fontFace: TF, margin: 0 });
["Lập dàn ý rồi mới viết, có từ lâu",
 "Ý “câu phải đủ để bên kia lần ra đúng chỗ”,\ndòng nghiên cứu khác đã chiếm từ 2016",
 "Khoanh dấu chỗ đúng rồi nhờ mô hình lớn\nviết mô tả, đã có trong miền giao diện",
 "Mô hình 3 tỉ tham số cho giao diện, đã đông"].forEach((t, i) => {
  text("·", { x: M + 0.3, y: 3.02 + i * 0.5, w: 0.2, h: 0.4, fontSize: 14, bold: true, color: MUTE, fontFace: BF, margin: 0 });
  text(t, { x: M + 0.5, y: 3.0 + i * 0.5, w: 4.8, h: 0.5, fontSize: 11.5, color: BODY, fontFace: BF, margin: 0, lh: 1.2 });
});

rect(6.9, 2.4, 5.5, 2.7, TINT, { radius: 0.1 });
text("Mới — ba chỗ cụ thể", { x: 7.18, y: 2.58, w: 5.0, h: 0.36, fontSize: 14.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
["Đưa thông tin định danh vào MỤC TIÊU\nhuấn luyện, không chỉ vào đầu vào",
 "Nguồn giám sát tầng giữa rút TỰ ĐỘNG từ\nthao tác của người thật, không cần ai gán",
 "Dùng câu hướng dẫn người viết làm ĐÍCH SINH,\nmọi bài khác để nó ở đầu vào"].forEach((t, i) => {
  text(String(i + 1), { x: 7.2, y: 3.02 + i * 0.62, w: 0.25, h: 0.4, fontSize: 13, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
  text(t, { x: 7.5, y: 3.0 + i * 0.62, w: 4.8, h: 0.62, fontSize: 11.5, color: INK, fontFace: BF, margin: 0, lh: 1.25 });
});

rect(M, 5.3, W - 2 * M, 0.95, NAVY, { radius: 0.1 });
text([{ text: "Bằng chứng cứng nhất cho chỗ số 1:  ", options: { bold: true, color: "F0C9A8" } }, { text: "bài gần nhất trong miền này đã NÊU RÕ vấn đề — trên một màn có hai biểu tượng kính lúp gần giống hệt nhau — nhưng cách họ xử là đưa ngữ cảnh vào đầu vào, còn hàm mất mát vẫn là cross entropy thuần.", options: { color: WHITE } }], { x: M + 0.3, y: 5.3, w: W - 2 * M - 0.6, h: 0.95, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });

text("Tính mới ở mức tổ hợp, nguồn giám sát và miền áp dụng. Không phải kiến trúc mới, và luận văn nói đúng mức đó.", { x: M, y: 6.45, w: 10.6, h: 0.5, fontSize: 12.5, italic: true, color: STEEL, fontFace: TF, margin: 0 });
note(`Trình tự nói: phần KHÔNG mới trước, phần mới sau. Nói trước thì thành thẳng thắn, để hội đồng phát hiện thì thành nói quá.
Phần không mới: lập dàn ý rồi viết có từ lâu trong sinh văn bản; ý câu phải đủ để bên kia lần ra đúng chỗ đã bị dòng sinh biểu thức quy chiếu chiếm từ 2016, kể cả ở tầng huấn luyện; khoanh dấu rồi nhờ mô hình lớn viết mô tả đã có trong chính miền giao diện ở một hội nghị lớn 2025; mô hình 3 tỉ tham số cho giao diện thì đã đông.
Phần mới, ba chỗ. Một, đưa thông tin định danh vào mục tiêu huấn luyện chứ không chỉ vào đầu vào. Đây là chỗ có bằng chứng cứng nhất: bài Widget Captioning ở EMNLP 2020 đã nêu rõ vấn đề hai biểu tượng kính lúp giống nhau nên ngữ cảnh là thiết yếu, nhưng họ chỉ đưa ngữ cảnh vào đầu vào, hàm mất mát vẫn là cross entropy thuần, không có gì ép câu phải phân biệt được. Hai, nguồn giám sát tầng giữa rút tự động từ toạ độ người thật chạm, không cần người gán và không cần mô hình đóng. Ba, dùng câu hướng dẫn người viết làm đích sinh, trong khi mọi công trình dùng bộ dữ liệu này đều để nó ở đầu vào.
Nếu bị hỏi sao không đưa bộ trỏ vào vòng huấn luyện như một bài 2017 đã làm: vì bộ trỏ cũng chính là thước chấm, đưa vào thành tự chấm. Đây là lựa chọn có chủ đích.`);
pageno(); done();

// ══════════════════════════════════════════════ 6 · THƯỚC
slide();
head("Phần thứ hai: cách chấm độ đúng", "Câu có đủ rõ để lần ra đúng nút hay không");
shot("real_ground_1.png", M, 2.5, 1.62, 3.45, "“invert the lens” → trúng nút");
rect(2.95, 2.5, W - M - 2.95, 1.75, FILL, { radius: 0.1 });
text("Ba bước", { x: 3.2, y: 2.66, w: 8.5, h: 0.4, fontSize: 15, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("1.  Giấu mục tiêu đi, chỉ đưa cho bộ trỏ một ảnh và một câu.\n2.  Bộ trỏ chấm một điểm nên chạm, là chấm xanh trong ảnh bên.\n3.  Điểm rơi trúng vùng nút cần bấm, khung đỏ, thì câu đó đúng.", { x: 3.2, y: 3.1, w: W - M - 3.25, h: 1.1, fontSize: 13, color: INK, fontFace: BF, lh: 1.45, margin: 0 });

rect(2.95, 4.4, 4.55, 1.35, WHITE, { radius: 0.1, line: GOOD, lw: 1.4 });
text("Không chấm theo câu chữ", { x: 3.2, y: 4.55, w: 4.1, h: 0.35, fontSize: 13.5, bold: true, color: GOOD, fontFace: BF, margin: 0 });
text("Gọi tên kiểu gì cũng được, miễn\nbộ trỏ lần ra đúng nút.", { x: 3.2, y: 4.92, w: 4.1, h: 0.75, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });
rect(7.85, 4.4, 4.55, 1.35, WHITE, { radius: 0.1, line: GOOD, lw: 1.4 });
text("Chống màn quá dễ", { x: 8.1, y: 4.55, w: 4.1, h: 0.35, fontSize: 13.5, bold: true, color: GOOD, fontFace: BF, margin: 0 });
text("Chạy thêm một lượt không đưa câu\nlàm sàn. Giá trị thật là phần chênh.", { x: 8.1, y: 4.92, w: 4.1, h: 0.75, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });

rect(2.95, 5.9, W - M - 2.95, 0.85, TINT, { radius: 0.1 });
text([{ text: "Một chỗ phải nói rõ:  ", options: { bold: true, color: ACCENT } }, { text: "bộ trỏ vẫn hơi thiên vị câu dài (câu ngắn trúng 35%, câu dài 69%). Nên phép so chính đặt ở hai mô hình cùng giọng, khi đó nhiễu này triệt tiêu.", options: { color: INK } }], { x: 3.2, y: 5.9, w: W - M - 3.25, h: 0.85, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
note(`Bộ trỏ là một mô hình chuyên: đưa nó một ảnh và một câu như "chạm nút tìm kiếm", nó chỉ ra điểm x y nên chạm. Dùng nó như một người dùng máy móc làm theo hướng dẫn.
Ví dụ trong ảnh: câu "invert the lens", bộ trỏ chấm một điểm rơi đúng vào nút lật camera. Sai lệch phải nằm trong dung sai 14% cạnh màn, đây là ngưỡng chuẩn của AITW ở NeurIPS 2023.
Tính chất quan trọng nhất: thước không chấm theo câu chữ, nên "funnel icon" hay "Filter button" viết khác nhau mà cùng trỏ trúng thì đều đúng. Quan trọng vì mô hình học trên gold hay nói giọng gold, nếu chấm theo chữ thì nó được thưởng oan.
Nhưng phải nói thật là bộ trỏ chưa miễn nhiễm với giọng văn: đo trên 76 câu thì câu ngắn trúng 35%, câu dài trúng 69%, tương quan 0.327. Nên phép so chính đặt ở hai mô hình cùng giọng, tức bản huấn luyện thường với bản có thành phần thêm.`);
pageno(); done();

// ══════════════════════════════════════════════ 7 · SỐ ĐO
slide();
head("Đo thử trước khi tin", "Câu tốt hơn hẳn đoán bừa ở mọi cách chấm; danh sách nút càng đầy đủ thì thước càng chặt");
// bang 4 cach cham
const cols = [["Chấm rộng\n(đĩa dung sai)", "51.3%", "6.6%", "+44.7", MUTE],
              ["Chặt, nút từ\nbộ đọc chữ", "35.5%", "2.6%", "+32.9", STEEL],
              ["Chặt, nút từ\nbộ dò hình", "19.7%", "0.0%", "+19.7", STEEL],
              ["Chặt, nút THẬT\ntừ hệ điều hành", "6.6%", "0.0%", "+6.6", ACCENT]];
text("Đưa câu đáp án chuẩn", { x: M - 0.15, y: 3.12, w: 2.6, h: 0.35, fontSize: 12, bold: true, color: INK, fontFace: BF, margin: 0 });
text("Không đưa câu (sàn)", { x: M - 0.15, y: 3.62, w: 2.6, h: 0.35, fontSize: 12, bold: true, color: INK, fontFace: BF, margin: 0 });
text("Chênh lệch", { x: M - 0.15, y: 4.14, w: 2.6, h: 0.35, fontSize: 12, bold: true, color: INK, fontFace: BF, margin: 0 });
let bx = 3.55;
cols.forEach((c, i) => {
  const hl = i === 3;
  rect(bx, 2.45, 2.05, 2.2, hl ? TINT : FILL, { radius: 0.09 });
  text(c[0], { x: bx + 0.08, y: 2.55, w: 1.89, h: 0.55, fontSize: 10.5, bold: true, color: hl ? ACCENT : STEEL, fontFace: BF, align: "center", margin: 0, lh: 1.2 });
  text(c[1], { x: bx, y: 3.12, w: 2.05, h: 0.35, fontSize: 13.5, color: BODY, fontFace: BF, align: "center", margin: 0 });
  text(c[2], { x: bx, y: 3.62, w: 2.05, h: 0.35, fontSize: 13.5, color: BODY, fontFace: BF, align: "center", margin: 0 });
  text(c[3], { x: bx, y: 4.08, w: 2.05, h: 0.45, fontSize: 17.5, bold: true, color: c[4], fontFace: TF, align: "center", margin: 0 });
  bx += 2.15;
});
rect(M, 4.85, W - 2 * M, 0.95, NAVY, { radius: 0.1 });
text([{ text: "Vì sao cột cuối tụt mạnh.  ", options: { bold: true, color: "F0C9A8" } }, { text: "Phần tử cần chạm rộng 189×126 pixel, phần tử KHÁC gần nhất chỉ cách 69 pixel, mà bộ trỏ giá rẻ lệch tới 256 pixel. Nó lệch xa hơn cả khoảng cách sang nút bên cạnh nên gần như luôn rơi vào ô nút khác. Con số thấp đó đo DỤNG CỤ, không đo câu hướng dẫn.", options: { color: WHITE } }], { x: M + 0.3, y: 4.85, w: W - 2 * M - 0.6, h: 0.95, fontSize: 12.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.3 });
rect(M, 5.95, 5.55, 0.85, FILL, { radius: 0.09 });
text([{ text: "8/10  ", options: { bold: true, color: GOOD, fontFace: TF } }, { text: "ngưỡng đạt khi bơm lỗi, ngưỡng khoá trước khi chạy. Hai chỗ rớt giữ nguyên, không nới cho vừa.", options: { color: BODY } }], { x: M + 0.25, y: 5.95, w: 5.05, h: 0.85, fontSize: 12, fontFace: BF, valign: "middle", margin: 0, lh: 1.28 });
rect(6.85, 5.95, 5.55, 0.85, FILL, { radius: 0.09 });
text([{ text: "69 px  ", options: { bold: true, color: BAD, fontFace: TF } }, { text: "là khoảng cách giữa hai nút cạnh nhau. Bộ trỏ phải lệch dưới mức đó thì cách chấm chặt mới dùng được.", options: { color: BODY } }], { x: 7.1, y: 5.95, w: 5.05, h: 0.85, fontSize: 12, fontFace: BF, valign: "middle", margin: 0, lh: 1.28 });
note(`Đây là bằng chứng cứng nhất tới giờ, và cũng là chỗ phải nói cho thật.
Cách chấm rộng tay là chấm theo đĩa dung sai 151 pixel: trần 51.3, sàn 6.6, chênh 44.7. Từng lo sàn cao làm hiệu số bị nén, đo ra thì ngược lại, sàn chỉ 6.6 vì một màn có khoảng 24 vùng chữ, đoán bừa mà trúng đúng cái nút cần thì hiếm.
Nhưng khi siết lại bằng cách chấm theo nút gần nhất, tức chỉ tính trúng khi nút đúng là nút gần điểm chấm nhất, thì chênh sụp còn 30.3 nếu lấy danh sách nút bằng OCR, và còn 13.2 nếu lấy bằng bộ dò phần tử OmniParser bắt được cả nút hình.
Nên 44.7 là cận trên lạc quan, không đem khoe. 13.2 là cận dưới bi quan, vì bộ trỏ đang dùng là loại rẻ và bộ dò đếm cả chữ không bấm được. Dải thật nằm giữa 13 và 45, tuỳ độ chính xác của bộ trỏ. Chính vì vậy Cổng A là điểm sống còn: bộ trỏ chuyên chính xác thì giữ được dải, bộ trỏ yếu thì sụp.
Hai con số dưới: 63% số bước có nút khác trong dung sai, đây là chuyện khác với sàn, nó nói cách chấm rộng tay còn dễ dãi. Và 0.34 là điểm của cách đo đầu tiên bằng so chữ, cần từ 0.80 nên đã tự bỏ.`);
pageno(); done();

// ══════════════════════════════════════════════ 8 · TỰ KIỂM
slide();
head("Bốn chỗ hở, sau đợt đo lại", "Hai chỗ vá xong, hai chỗ hoá ra sâu hơn tưởng");
const holes = [
  ["Bật với tắt · đã vá", "bắt hết cặp trong bảng, không kêu oan câu nào. Còn mù với cặp kiểu next / previous", "loại thật sự nguy hiểm chỉ chiếm 1% số bước"],
  ["Bước gõ và cuộn · đã có cách chấm", "trước chỉ là lời hứa. Nay bắt gõ sai nội dung 93%, cuộn sai hướng 100%", "vẫn báo tách hai con số, không gộp"],
  ["Bộ trỏ trúng thì người có làm được không", "vẫn chưa kiểm. Đúng kiểu sai lầm đã làm hỏng cách đo trước", "khảo sát 91 cặp, hai người chấm, ngưỡng khoá trước"],
  ["Chấm chặt · chạy được, chưa dùng được", "với bộ trỏ hiện tại nó chấm oan 59% câu đúng, vì bộ trỏ lệch quá nhiều", "chuyển thành điều kiện tiên quyết của Cổng A"],
];
let hy = 2.45;
holes.forEach((h, i) => {
  rect(M, hy, W - 2 * M, 1.02, i === 2 ? TINT : FILL, { radius: 0.08 });
  circle(M + 0.22, hy + 0.3, 0.42, i === 2 ? ACCENT : STEEL, String(i + 1), WHITE);
  text(h[0], { x: M + 0.82, y: hy, w: 3.9, h: 1.02, fontSize: 13, bold: true, color: INK, fontFace: BF, valign: "middle", margin: 0, lh: 1.2 });
  text(h[1], { x: M + 4.85, y: hy, w: 3.65, h: 1.02, fontSize: 11.5, color: BODY, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
  text([{ text: "→ ", options: { bold: true, color: GOOD } }, { text: h[2], options: { color: INK } }], { x: M + 8.65, y: hy, w: 2.8, h: 1.02, fontSize: 11.5, fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
  hy += 1.1;
});
text("Cách làm xuyên suốt: kiểm cái thước trước khi tin nó. Chính phép kiểm đó vừa bắt được một lỗi nặng của mình.", { x: M, y: 6.88, w: 10.4, h: 0.4, fontSize: 13, italic: true, color: STEEL, fontFace: TF, margin: 0 });
note(`Nêu cả những chỗ còn hở, không giấu.
Một, thước không phân biệt được bật với tắt vì công tắc nằm cùng một toạ độ. Xử bằng cách kiểm thêm trạng thái đích, hoặc nói rõ giới hạn kèm tỉ lệ bước là công tắc.
Hai, chỉ khoảng 53% số bước là chạm, phần còn lại là gõ và cuộn, chấm bằng cách so nội dung chứ không có bộ trỏ bảo chứng, nên báo tách hai con số.
Ba, đây là chỗ đáng lo nhất: giả định bộ trỏ trúng thì người làm theo được vẫn chưa kiểm. Đúng kiểu sai lầm đã giết cách đo trước, tức tin mà chưa kiểm. Nên đưa hẳn khảo sát 91 cặp với người thật vào cổng, bộ chấm đã dựng sẵn trong harness, tự chấm được, miễn phí.
Bốn, bản AndroidControl công khai không kèm toạ độ từng nút, nên phải lấy bằng bộ dò phần tử rồi đo độ phủ trước khi tin.`);
pageno(); done();

// ══════════════════════════════════════════════ 9 · HAI CỔNG
slide();
head("Hai cổng chạy trước khi tiêu tiền", "Chỉ chạy mô hình, chưa huấn luyện, nên rẻ và nhanh");
rect(M, 2.45, 5.5, 2.35, TINT, { radius: 0.1 });
text("Cổng A · bộ trỏ có đủ tốt và có sạch không", { x: M + 0.28, y: 2.63, w: 5.0, h: 0.4, fontSize: 14.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Điều kiện đầu tiên: bộ trỏ phải lệch dưới\n3% cạnh màn, tức khoảng 32 pixel. Căn cứ:\nhai nút cạnh nhau chỉ cách 69 pixel, còn\nbộ trỏ rẻ đang lệch 256 pixel.\n\nDùng UGround chứ không dùng OS-Atlas,\nvì OS-Atlas đã học ngay trên AndroidControl.", { x: M + 0.28, y: 3.08, w: 5.05, h: 1.75, fontSize: 12.5, color: INK, fontFace: BF, lh: 1.34, margin: 0 });
rect(6.9, 2.45, 5.5, 2.35, FILL, { radius: 0.1 });
text("Cổng B · gắn thành phần vào đâu", { x: 7.18, y: 2.63, w: 5.0, h: 0.4, fontSize: 14.5, bold: true, color: STEEL, fontFace: TF, margin: 0 });
text("Đo xem mô hình nền còn yếu ở đâu:\nhay bịa nút, hay trỏ mơ hồ.\n\nYếu chỗ nào thì gắn thành phần vào\nchỗ đó, không gắn theo cảm tính.", { x: 7.18, y: 3.08, w: 5.0, h: 1.65, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.38, margin: 0 });

text("Không nhánh nào là ngõ cụt", { x: M, y: 5.0, w: 8, h: 0.4, fontSize: 15, bold: true, color: INK, fontFace: TF, margin: 0 });
const fb = [
  ["Bộ trỏ không đạt 80%", "chấm riêng nhóm nút có chữ và nêu giới hạn, bản thân chuyện không thước nào trỏ nổi nút hình cũng là một phát hiện"],
  ["Mô hình chỉ hoà mốc ngoài", "vẫn bảo vệ được bằng mô hình 3B chạy offline ngang một mô hình lớn gọi qua mạng"],
  ["Lớp 2 tăng điểm vì lý do sai", "đã có sẵn nhánh giả dược đưa danh sách của màn khác, cộng phân tầng theo độ dài câu"],
];
let fy = 5.42;
fb.forEach(r => {
  rect(M, fy, W - 2 * M, 0.46, WHITE, { radius: 0.06, line: RULE, lw: 1 });
  text([{ text: r[0] + "  ", options: { bold: true, color: BAD } }, { text: "→ " + r[1], options: { color: BODY } }], { x: M + 0.25, y: fy, w: W - 2 * M - 0.5, h: 0.46, fontSize: 12, fontFace: BF, valign: "middle", margin: 0 });
  fy += 0.52;
});
text("Chi phí: hai cổng khoảng 10 đô, cả pha huấn luyện khoảng 60 tới 70 đô trên Colab.", { x: M, y: 6.98, w: 10.4, h: 0.35, fontSize: 12, italic: true, color: STEEL, fontFace: TF, margin: 0 });
note(`Hai cổng go no go, chạy trước khi tiêu tiền huấn luyện, chỉ chạy mô hình nên rẻ. Notebook đã dựng sẵn.
Cổng A: bộ trỏ chuyên phải trúng khoảng 80% khi lần vị trí từ câu đúng, và ngưỡng đó phải tính theo cách chấm nút gần nhất chứ không phải đĩa dung sai. Chọn UGround chứ không phải OS-Atlas, vì OS-Atlas train thẳng trên AndroidControl nên nhiễm, còn UGround train trên ảnh web nên sang mobile là zero-shot.
Một việc mới nhận ra là quan trọng: nguyên tắc app chưa từng thấy chỉ bảo vệ mô hình học trò, không bảo vệ bộ trỏ. Bộ trỏ có thể đã thấy chính màn test. Nên trước khi chấm phải đối chiếu danh sách app của bộ trỏ với 631 episode test và loại app trùng.
Cổng B: đo mô hình nền yếu ở đâu để chọn thành phần cho đúng chỗ.
Nhẹ gánh cho Cổng A: cái luận văn cần là hiệu số giữa hai mô hình đo qua cùng một bộ trỏ, lỗi bộ trỏ phần lớn triệt tiêu trong hiệu số, nhưng chỉ đúng khi hai mô hình cùng giọng.`);
pageno(); done();

// ══════════════════════════════════════════════ 10 · CÂU HỎI
slide(NAVY);
text("NHỮNG ĐIỂM XIN TRAO ĐỔI", { x: M, y: 1.7, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Một hướng đã kiểm được bằng số,\nbốn điểm còn cần thầy quyết", { x: M, y: 2.15, w: 11.4, h: 1.4, fontSize: 25, bold: true, color: WHITE, fontFace: TF, lh: 1.12, margin: 0 });
const qs = [
  "Khung đóng góp: một mô hình fine-tune kèm một thành phần trong đích huấn luyện, cộng cách chấm khách quan. Thầy thấy đủ chưa, phần nào nên là chính?",
  "Mọi con số trong bảng kết quả đều do máy chấm. Chỉ có một bước hiệu chuẩn dụng cụ làm đúng một lần với người đọc. Thầy đồng ý giữ bước đó không?",
  "Nếu mô hình chỉ hoà mốc ngoài, thì mô hình 3 tỉ tham số chạy offline ngang mô hình lớn gọi qua mạng có đủ để bảo vệ không?",
  "Thành phần này không phải kiến trúc mới, mà là đưa tính phân biệt phần tử vào mục tiêu huấn luyện. Thầy thấy mức đó đủ cho luận văn thạc sĩ chưa?",
];
let qy = 3.85;
qs.forEach((q, i) => {
  circle(M, qy, 0.42, ACCENT, String(i + 1), WHITE);
  text(q, { x: M + 0.62, y: qy - 0.06, w: 11.2, h: 0.55, fontSize: 14, color: "E6ECF2", fontFace: BF, valign: "middle", margin: 0, lh: 1.25 });
  qy += 0.64;
});
note(`Kết lại: một hướng đã kiểm được bằng số, còn năm điểm chỉ thầy quyết được.
Một, khung hai phần và phần nào là chính. Hai, chấm tự động thay chấm người. Ba, kịch bản hoà thì có đủ bảo vệ không. Bốn, định vị sau GuideMe. Lưu ý là bỏ hẳn chữ đầu tiên, vì cách đánh giá kiểu sinh câu rồi cho mô hình khác trỏ vùng đã có tiền lệ từ Mao ở CVPR 2016, phải phân định chứ không nhận là mới hoàn toàn. Năm, đã đủ tầm luận văn thạc sĩ chưa.
Đây là những chuyện không đo bằng số được, cần thầy định hướng trước khi lên Colab tiêu tiền.`);
pageno(); done();

// ---- write ----
fs.mkdirSync("_preview_v7", { recursive: true });
const page = `<!doctype html><meta charset="utf-8"><style>@page{size:${W}in ${H}in;margin:0}*{margin:0;box-sizing:border-box}.slide{position:relative;width:${W}in;height:${H}in;overflow:hidden;page-break-after:always}</style>` + htmlSlides.join("\n");
fs.writeFileSync("_preview_v7/preview.html", page);
pres.writeFile({ fileName: "../LUAN_VAN_SLIDE_v7.pptx" }).then(f => console.log("PPTX ->", f, "| slides:", htmlSlides.length)).catch(e => console.error("ERR", e));
