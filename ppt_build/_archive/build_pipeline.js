// Deck PIPELINE — ban rut gon chi trinh PIPELINE de thay duyet huong.
// Dual-emit: ../LUAN_VAN_PIPELINE.pptx + _preview_pipeline/preview.html
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Luan van thac si";
pres.title = "Pipeline sinh huong dan bam man hinh";

// ---- palette (giong v3, giu nhat quan bo deck) ----
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
function note(t) { s.addNotes(t.trim()); }
function kicker(t) { text(t.toUpperCase(), { x: M, y: 0.62, w: W - 2 * M, h: 0.3, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, spacing: 2.5, margin: 0 }); }
function title(t) { text(t, { x: M, y: 0.98, w: W - 2 * M, h: 1.0, fontSize: 27, bold: true, color: INK, fontFace: TF, margin: 0, lh: 1.05 }); }
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
function divider(kick, big, sub) {
  slide(NAVY);
  text(kick.toUpperCase(), { x: M, y: 3.05, w: W - 2 * M, h: 0.35, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 3, align: "center", margin: 0 });
  text(big, { x: M, y: 3.5, w: W - 2 * M, h: 1.1, fontSize: 32, bold: true, color: WHITE, fontFace: TF, align: "center", margin: 0, lh: 1.1 });
  if (sub) text(sub, { x: 1.8, y: 4.65, w: W - 3.6, h: 0.9, fontSize: 15, italic: true, color: "C9D2DC", fontFace: BF, align: "center", margin: 0, lh: 1.3 });
  done();
}

// ============================================================ 1 · TITLE
slide(NAVY);
text("PIPELINE · TRÌNH ĐỂ DUYỆT HƯỚNG", { x: M, y: 1.5, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Sinh hướng dẫn sử dụng\nbám đúng màn hình đang mở", { x: M - 0.02, y: 2.15, w: 9.6, h: 1.9, fontSize: 32, bold: true, color: WHITE, fontFace: TF, lh: 1.08, margin: 0 });
text("Toàn bộ pipeline, và chỗ đặt mô hình do học viên tự huấn luyện", { x: M, y: 4.3, w: 9.4, h: 0.6, fontSize: 17, italic: true, color: "C9D2DC", fontFace: TF, margin: 0 });
text("Học viên · · · · ·      Giảng viên hướng dẫn · · · · ·      2026", { x: M, y: 6.55, w: 11, h: 0.4, fontSize: 13, color: "8FA0B2", fontFace: BF, margin: 0 });
shot("real_mv_1.png", 10.4, 2.0, 1.95, 3.2);
done();

// ============================================================ 2 · BAI TOAN
slide();
head("Bài toán", "Người dùng đưa ảnh màn hình và một câu hỏi, hệ trả về các bước làm");
shot("real_mv_2.png", M, 2.3, 1.7, 2.85);
rect(M - 0.07, 5.4, 1.84, 0.62, FILL, { radius: 0.07 });
text("“Làm sao thêm việc mới\nvà tính tiền theo giờ?”", { x: M - 0.07, y: 5.4, w: 1.84, h: 0.62, fontSize: 10, italic: true, color: INK, fontFace: BF, align: "center", valign: "middle", lh: 1.18, margin: 0 });
arrow(3.05, 3.7, 0.5, ACCENT);
// dung
rect(3.75, 2.3, 4.2, 2.15, "EAF3EC", { radius: 0.1 });
text("Hướng dẫn bám đúng màn", { x: 4.0, y: 2.45, w: 3.7, h: 0.3, fontSize: 12.5, bold: true, color: GOOD, fontFace: BF, margin: 0 });
text("1.  Chạm “Find or create a task”\n2.  Nhập số giờ vào “Estimated hours”\n3.  Chạm “SAVE & ADD ANOTHER”", { x: 4.0, y: 2.85, w: 3.7, h: 1.3, fontSize: 13, color: INK, fontFace: BF, lh: 1.5, margin: 0 });
// hong
rect(8.2, 2.3, 4.2, 2.15, "FBEAE7", { radius: 0.1 });
text("Câu trả lời hỏng", { x: 8.45, y: 2.45, w: 3.7, h: 0.3, fontSize: 12.5, bold: true, color: "C0392B", fontFace: BF, margin: 0 });
text("1.  Chạm “Find or create a task”\n2.  Chạm “Preferences”\n3.  Chạm “SAVE & ADD ANOTHER”", { x: 8.45, y: 2.85, w: 3.7, h: 1.3, fontSize: 13, color: INK, fontFace: BF, lh: 1.5, margin: 0 });
text("↑ màn này không hề có nút nào tên vậy", { x: 8.45, y: 3.95, w: 3.7, h: 0.3, fontSize: 11, italic: true, color: "C0392B", fontFace: BF, margin: 0 });
// hai cai kho
rect(3.75, 4.75, 8.65, 1.35, FILL, { radius: 0.1 });
text("Hai cái khó của bài toán", { x: 4.0, y: 4.9, w: 8.2, h: 0.3, fontSize: 12.5, bold: true, color: STEEL, fontFace: BF, margin: 0 });
text("1.  Không có bộ hướng dẫn chuẩn do người soạn sẵn để so. Tự soạn thì tốn hàng nghìn giờ người.\n2.  Bịa tên nút là lỗi nguy hiểm mà đọc lên vẫn thấy trơn tru. Chỉ khi đối chiếu đúng màn đó mới lòi ra.", { x: 4.0, y: 5.25, w: 8.2, h: 0.75, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
text("Người dùng làm theo sẽ dò mãi không thấy, hoặc bấm nhầm sang một nút nghe na ná.", { x: M, y: 6.4, w: 11.5, h: 0.35, fontSize: 13.5, color: INK, fontFace: BF, margin: 0 });
note(`Hợp đồng vào/ra: chỉ ảnh + câu hỏi. Câu hỏi cố ý không chứa tên nút, để model phải tự đọc màn hình.
Ảnh bên trái là màn thật trong bộ dữ liệu, không phải ví dụ dựng. Ba nút trong cột xanh đều nhìn thấy được trên ảnh.
Cái khó thứ nhất là lý do phải nghĩ ra cách đo không cần đáp án mẫu. Cái khó thứ hai là lý do đề tài có giá trị: lỗi bịa tên nút khiến người dùng thao tác sai trên máy thật, khác hẳn tả sai một chi tiết trong ảnh.`);
pageno(); done();

// ============================================================ 3 · Y TUONG
slide();
head("Ý tưởng", "Teacher hay bịa. Student được dạy lại cho cẩn thận");
rect(M, 2.5, 5.35, 2.9, FILL, { radius: 0.1 });
text("Teacher", { x: M + 0.3, y: 2.72, w: 4.7, h: 0.4, fontSize: 17, bold: true, color: STEEL, fontFace: TF, margin: 0 });
text("gpt-4o-mini · gọi qua API\n\nChỉ thấy ảnh + câu hỏi.\nKhông được xem danh sách nút.\n\n→ đôi khi bịa ra nút không tồn tại.", { x: M + 0.3, y: 3.15, w: 4.75, h: 2.1, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
arrow(6.55, 3.95, 0.55);
rect(7.4, 2.5, 5.0, 2.9, TINT, { radius: 0.1 });
text("Student", { x: 7.7, y: 2.72, w: 4.4, h: 0.4, fontSize: 17, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Qwen2.5-VL-3B · tự fine-tune\n\nChỉ học phần lời Teacher\nđã lọc sạch bịa.\n\n→ sản phẩm chính của luận văn.", { x: 7.7, y: 3.15, w: 4.4, h: 2.1, fontSize: 13.5, color: INK, fontFace: BF, lh: 1.35, margin: 0 });
rect(M, 5.75, W - 2 * M, 1.15, NAVY, { radius: 0.1 });
text([{ text: "Câu hỏi trọng tâm:  ", options: { bold: true, color: "E4A986" } }, { text: "thói quen thành thật đó có thật sự ngấm vào Student, hay chỉ là vẻ ngoài phụ thuộc vào việc có ai kiểm tra hộ hay không?", options: { color: WHITE } }], { x: M + 0.3, y: 5.75, w: W - 2 * M - 0.6, h: 1.15, fontSize: 14.5, fontFace: BF, valign: "middle", lh: 1.3, margin: 0 });
note(`Teacher là gpt-4o-mini, gọi qua API. Cố ý không cho nó xem danh sách nút, vì ta cần đúng những chỗ nó tự nhiên hay bịa.
Student là Qwen2.5-VL-3B, mô hình mở, em tự fine-tune bằng SFT-LoRA.
Điểm cần nhấn: Student KHÔNG học nguyên xi lời Teacher. Nó chỉ học phần đã lọc sạch bịa. Nên nó không phải bản sao thu nhỏ của Teacher.
Câu hỏi trọng tâm này có thể trả lời là không. Chính vì thế nó mới là câu hỏi nghiên cứu thật.`);
pageno(); done();

// ============================================================ 4 · PIPELINE 5 BUOC
slide();
head("Pipeline lúc chuẩn bị dữ liệu", "Chạy một lần, ngoại tuyến, để tạo dữ liệu dạy Student");
const ST = [
  ["Ảnh + câu hỏi", "Lấy từ kho ảnh màn hình\nứng dụng thật", STEEL],
  ["Teacher viết nháp", "Chỉ thấy ảnh, không thấy\ndanh sách nút", STEEL],
  ["Đối chiếu nút thật", "Thuật toán so từng bước\nvới màn hình", ACCENT],
  ["Viết lại chỗ bịa", "Đổi thành mô tả,\nkhông đoán nút khác", STEEL],
  ["Dạy Student", "Huấn luyện trên đúng\nphần đã lọc sạch", GOOD],
];
ST.forEach((c, i) => {
  const x = M + i * 2.32;
  rect(x, 2.5, 2.05, 2.15, i === 4 ? "EAF3EC" : (i === 2 ? TINT : FILL), { radius: 0.09 });
  circle(x + 0.16, 2.7, 0.5, c[2], String(i + 1));
  text(c[0], { x: x + 0.1, y: 3.32, w: 1.85, h: 0.5, fontSize: 13, bold: true, color: INK, fontFace: BF, align: "center", valign: "middle", lh: 1.1, margin: 0 });
  text(c[1], { x: x + 0.12, y: 3.85, w: 1.82, h: 0.6, fontSize: 10.5, color: BODY, fontFace: BF, align: "center", lh: 1.25, margin: 0 });
  if (i < 4) arrow(x + 2.07, 3.4, 0.22, ACCENT);
});
rect(M, 5.05, 5.5, 1.0, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "Bước 3 không phải AI.  ", options: { bold: true, color: INK } }, { text: "Là thuật toán so nghĩa, đóng băng, chạy miễn phí trên máy.", options: { color: BODY } }], { x: M + 0.25, y: 5.05, w: 5.0, h: 1.0, fontSize: 12.5, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
rect(6.9, 5.05, 5.5, 1.0, WHITE, { radius: 0.09, line: RULE, lw: 1 });
text([{ text: "Bước 4 dùng khuôn mẫu cố định.  ", options: { bold: true, color: INK } }, { text: "Cố ý không gọi AI, vì để AI viết lại thì chính bước lọc mở ra chỗ bịa mới.", options: { color: BODY } }], { x: 7.15, y: 5.05, w: 5.0, h: 1.0, fontSize: 12.5, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
rect(M, 6.3, W - 2 * M, 0.72, NAVY, { radius: 0.09 });
text([{ text: "Kết quả:  ", options: { bold: true, color: "E4A986" } }, { text: "một bộ dữ liệu sạch, dùng để dạy Student thói quen thành thật thay vì cho nó học nguyên xi lời Teacher.", options: { color: WHITE } }], { x: M + 0.3, y: 6.3, w: W - 2 * M - 0.6, h: 0.72, fontSize: 13.5, fontFace: BF, valign: "middle", margin: 0 });
note(`Toàn bộ luồng này chạy một lần, offline, chỉ để tạo tập dữ liệu huấn luyện.
Bước 3 dùng embedding nomic-embed-text, ngưỡng 0.55 đã freeze. Nó là hàm đo khoảng cách, đóng băng, không huấn luyện gì.
Bước 5 là bước duy nhất có huấn luyện. Bốn bước trước chỉ để tạo ra dữ liệu.
Chi phí: bước 2 khoảng 1-2 đô cho vài nghìn lượt gọi. Bước 5 chạy trên Colab.`);
pageno(); done();

// ============================================================ 4b · BUOC 3 KI — DOI CHIEU
slide();
head("Bên trong bước 3: đối chiếu", "Cách một tên nút bị kết luận là bịa");
text("Mỗi ảnh màn hình trong bộ dữ liệu đều đi kèm một file do hệ điều hành Android xuất ra, liệt kê mọi phần tử đang hiển thị. Thuật toán lấy từng tên nút Teacher nhắc tới, so nghĩa với toàn bộ danh sách đó.", { x: M, y: 2.15, w: 11.4, h: 0.5, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });
// danh sach nut that
rect(M, 2.85, 3.5, 3.1, FILL, { radius: 0.1 });
text("Danh sách nút thật của màn", { x: M + 0.25, y: 3.0, w: 3.0, h: 0.3, fontSize: 12, bold: true, color: STEEL, fontFace: BF, margin: 0 });
text("[nút]  “Find or create a task”\n[ô nhập]  “Estimated hours”\n[nút]  “Charge”\n[nút]  “Hourly rate”\n[nút]  “SAVE & ADD ANOTHER”", { x: M + 0.25, y: 3.4, w: 3.1, h: 2.2, fontSize: 11.5, color: INK, fontFace: BF, lh: 1.75, margin: 0 });
arrow(4.65, 4.4, 0.4, ACCENT);
// so nghia
rect(5.3, 2.85, 3.6, 3.1, WHITE, { radius: 0.1, line: RULE, lw: 1 });
text("Teacher nhắc: “Preferences”", { x: 5.55, y: 3.0, w: 3.1, h: 0.3, fontSize: 12, bold: true, color: INK, fontFace: BF, margin: 0 });
text("điểm giống nghĩa với từng nhãn", { x: 5.55, y: 3.32, w: 3.1, h: 0.25, fontSize: 10, italic: true, color: MUTE, fontFace: BF, margin: 0 });
const SC = [["Find or create a task", "0.31"], ["Estimated hours", "0.22"], ["Charge", "0.28"], ["Hourly rate", "0.25"], ["SAVE & ADD ANOTHER", "0.19"]];
SC.forEach((r, i) => {
  const y = 3.68 + i * 0.42;
  text(r[0], { x: 5.55, y, w: 2.4, h: 0.3, fontSize: 11, color: BODY, fontFace: BF, valign: "middle", margin: 0 });
  text(r[1], { x: 8.0, y, w: 0.65, h: 0.3, fontSize: 11.5, bold: true, color: "C0392B", fontFace: BF, align: "right", valign: "middle", margin: 0 });
});
text("ví dụ minh hoạ", { x: 5.55, y: 5.75, w: 3.1, h: 0.2, fontSize: 9, italic: true, color: MUTE, fontFace: BF, margin: 0 });
arrow(9.05, 4.4, 0.4, ACCENT);
// ket luan
rect(9.7, 2.85, 2.7, 3.1, TINT, { radius: 0.1 });
text("Ngưỡng", { x: 9.95, y: 3.0, w: 2.2, h: 0.3, fontSize: 12, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("0.55", { x: 9.95, y: 3.35, w: 2.2, h: 0.6, fontSize: 34, bold: true, color: INK, fontFace: TF, margin: 0 });
text("Không nhãn nào đạt ngưỡng.\n\n⇒ “Preferences” là bịa.", { x: 9.95, y: 4.05, w: 2.2, h: 0.9, fontSize: 12.5, bold: true, color: INK, fontFace: BF, lh: 1.3, margin: 0 });
text("Nếu có một nhãn đạt ngưỡng thì tính là khớp, kể cả khác chữ.", { x: 9.95, y: 5.1, w: 2.2, h: 0.7, fontSize: 10.5, italic: true, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
rect(M, 6.2, W - 2 * M, 0.85, NAVY, { radius: 0.1 });
text([{ text: "So theo NGHĨA, không so chữ.  ", options: { bold: true, color: "E4A986" } }, { text: "“Cài đặt” vẫn khớp được với “Settings”. Ngưỡng 0.55 chốt từ tự kiểm: từ đồng nghĩa rơi vào 0.6–0.69, từ khác nghĩa quanh 0.39.", options: { color: WHITE } }], { x: M + 0.3, y: 6.2, w: W - 2 * M - 0.6, h: 0.85, fontSize: 13, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
note(`Thuật toán: nomic-embed-text, so cosine giữa tên nút Teacher nhắc và từng nhãn trong danh sách nút thật. Lấy điểm cao nhất. Dưới ngưỡng thì kết luận là bịa.
Ngưỡng 0.55 đã freeze trước, chốt từ tự kiểm trên tiếng Anh: cặp đồng nghĩa rơi vào 0.6-0.69, cặp khác nghĩa quanh 0.39. Chọn 0.55 nằm giữa hai vùng.
Các con số 0.31/0.22/... trên slide là minh hoạ cho dễ hình dung, không phải số đo thật.
Điểm quan trọng nếu thầy hỏi: nomic-embed-text là mạng nơ-ron, em không giấu. Nhưng nó chạy đóng băng, chỉ đóng vai hàm đo khoảng cách, không nhận gradient, không cập nhật tham số nào.
Cách này mượn từ ALOHa (NAACL 2024): trích thực thể, so embedding, không cặp nào đủ giống thì tính là bịa.`);
pageno(); done();

// ============================================================ 4c · BUOC 4 KI — VIET LAI + DONG DU LIEU
slide();
head("Bên trong bước 4: viết lại", "Khuôn mẫu cố định, cố ý không gọi AI");
rect(M, 2.2, 5.6, 2.0, "FBEAE7", { radius: 0.1 });
text("Nếu để AI viết lại cho hay", { x: M + 0.3, y: 2.38, w: 5.0, h: 0.3, fontSize: 13, bold: true, color: "C0392B", fontFace: BF, margin: 0 });
text("Chính bước lọc lại mở ra một chỗ bịa mới. Bộ lọc đáng lẽ để chặn bịa thì lại tự sinh ra bịa.", { x: M + 0.3, y: 2.75, w: 5.0, h: 0.7, fontSize: 12.5, color: INK, fontFace: BF, lh: 1.3, margin: 0 });
text("Nên bước này không có AI nào tham gia.", { x: M + 0.3, y: 3.5, w: 5.0, h: 0.4, fontSize: 12.5, bold: true, color: "C0392B", fontFace: BF, margin: 0 });
rect(6.8, 2.2, 5.6, 2.0, "EAF3EC", { radius: 0.1 });
text("Khuôn mẫu dùng ở đây", { x: 7.1, y: 2.38, w: 5.0, h: 0.3, fontSize: 13, bold: true, color: GOOD, fontFace: BF, margin: 0 });
text("“Tìm và chạm vào tuỳ chọn trên màn hình phù hợp với việc bạn cần làm ở bước này.”", { x: 7.1, y: 2.75, w: 5.0, h: 0.7, fontSize: 12.5, italic: true, color: INK, fontFace: BF, lh: 1.3, margin: 0 });
text("Nếu câu này vô tình trùng một tên nút thật, hệ tự đổi sang một câu dự phòng trung tính.", { x: 7.1, y: 3.5, w: 5.0, h: 0.5, fontSize: 11.5, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
text("Một dòng dữ liệu dạy Student trông như thế này", { x: M, y: 4.45, w: 11.4, h: 0.3, fontSize: 13, bold: true, color: INK, fontFace: BF, margin: 0 });
rect(M, 4.85, W - 2 * M, 1.5, "F7F8FA", { radius: 0.09, line: RULE, lw: 1 });
text("ảnh:      mv_train_pool/aucommixfm4sss_s1.jpg\ncâu hỏi:  “Write step-by-step instructions for a person to follow on their phone, to: …”\nđáp án:   1. Tap “Settings”   2. Tap “Notifications”   3. Look for the option on this screen that matches…   4. Toggle “New episode alerts”", { x: M + 0.3, y: 4.85, w: 11.0, h: 1.5, fontSize: 11.5, color: INK, fontFace: BF, valign: "middle", lh: 1.6, margin: 0 });
text("Câu hỏi dùng lúc dạy giống hệt câu hỏi dùng lúc chấm, nên không ai nói được kết quả khác nhau chỉ vì đổi cách hỏi.", { x: M, y: 6.55, w: 11.4, h: 0.35, fontSize: 12.5, italic: true, color: BODY, fontFace: BF, margin: 0 });
note(`Quyết định thiết kế quan trọng: bước viết lại dùng khuôn mẫu cố định, tất định, không gọi LLM. Nếu dùng AI để viết lại cho mượt thì chính bước lọc lại có thể sinh ra chỗ bịa mới.
Một điểm cố ý khác, và là chỗ bịt lỗ hổng có thể bị hỏi: câu hỏi dạy Student KHÔNG chứa dặn dò "đừng bịa ra nút không có thật", trong khi câu nhắc cho Teacher lúc sinh dữ liệu thì CÓ. Nếu Student cũng được nhắc, sẽ không ai chứng minh được thói quen thành thật đến từ việc huấn luyện chứ không phải từ một câu dặn thêm lúc hỏi.
Định dạng thật là ShareGPT của LLaMA-Factory: một ảnh, một câu hỏi, một hướng dẫn đã lọc.`);
pageno(); done();

// ============================================================ 5 · VI DU CHAY THAT
slide();
head("Ví dụ chạy thật", "Một bước bịa bị bắt và viết lại trước khi đưa vào dạy Student");
shot("real_mv_1.png", M, 2.4, 1.62, 2.72, "Màn đặt giờ");
const ER = [
  [{ text: "Teacher viết", options: { bold: true, fill: FILL, color: INK } },
   { text: "Có nút này trên màn không?", options: { bold: true, fill: FILL, color: INK } },
   { text: "Xử lý", options: { bold: true, fill: FILL, color: INK, align: "center" } }],
  [{ text: "Chọn giờ và phút" }, { text: "Có" }, { text: "giữ nguyên", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Chọn buổi “PM”" }, { text: "Có" }, { text: "giữ nguyên", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Mở “Cài đặt”" }, { text: "Không có", options: { color: MUTE } }, { text: "viết lại thành mô tả", options: { align: "center", color: ACCENT, bold: true } }],
];
s.addTable(ER, { x: 3.4, y: 2.5, w: 8.85, colW: [3.0, 3.2, 2.65], rowH: 0.6, fontFace: BF, fontSize: 13, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle", color: BODY });
hpush(tableHTML(ER, 3.4, 2.5, [3.0, 3.2, 2.65], 0.6));
rect(3.4, 4.85, 8.85, 0.95, TINT, { radius: 0.09 });
text([{ text: "Câu được đưa vào dữ liệu dạy:  ", options: { bold: true, color: ACCENT } }, { text: "“Tìm và chạm vào tuỳ chọn trên màn hình phù hợp với việc cần làm ở bước này.”", options: { italic: true, color: INK } }], { x: 3.65, y: 4.85, w: 8.35, h: 0.95, fontSize: 13, fontFace: BF, valign: "middle", lh: 1.25, margin: 0 });
rect(3.4, 5.95, 8.85, 1.1, NAVY, { radius: 0.09 });
text([{ text: "Vì sao không đoán sang một nút thật khác?  ", options: { bold: true, color: "E4A986" } }, { text: "Thay nút bịa bằng một nút thật nhưng sai việc (kiểu bấm “Lưu” thay vì “Gửi”) khiến người dùng làm sai mà không hề hay biết. Lỗi âm thầm đó còn nguy hiểm hơn cả việc bịa.", options: { color: WHITE } }], { x: 3.65, y: 5.95, w: 8.35, h: 1.1, fontSize: 12.5, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
note(`Đây là màn thật trong bộ dữ liệu, không phải ví dụ dựng.
Chỗ đáng nói: bước bịa không bị xoá, cũng không bị sửa thành tên nút khác. Nếu đoán sang nút thật khác mà sai chức năng, người dùng vẫn làm sai mà không hay biết. Lỗi đó âm thầm, không ai phát hiện được.
Nên chọn cách viết lại thành mô tả: mất tính cụ thể nhưng không sai sự thật. Cái giá phải trả là %fallback, và luận văn báo con số đó công khai.`);
pageno(); done();

// ============================================================ 6 · DAU LA MO HINH CUA HOC VIEN
slide();
head("Trong pipeline này, đâu là mô hình do học viên huấn luyện", "Chỉ có đúng một ô, và đó là ô cuối");
const PD = [
  [{ text: "Thành phần", options: { bold: true, fill: FILL, color: INK } },
   { text: "Vai trò", options: { bold: true, fill: FILL, color: INK } },
   { text: "Có trọng số?", options: { bold: true, fill: FILL, color: INK, align: "center" } },
   { text: "Trọng số đổi vì luận văn?", options: { bold: true, fill: FILL, color: INK, align: "center" } }],
  [{ text: "gpt-4o-mini" }, { text: "Teacher, viết nháp để tạo dữ liệu. Không có mặt lúc chạy thật" },
   { text: "có, trên máy chủ OpenAI", options: { align: "center", color: MUTE } }, { text: "KHÔNG", options: { align: "center", bold: true, color: STEEL } }],
  [{ text: "nomic-embed-text" }, { text: "Đối chiếu tên nút với danh sách nút thật" },
   { text: "có, nhưng đóng băng", options: { align: "center", color: MUTE } }, { text: "KHÔNG", options: { align: "center", bold: true, color: STEEL } }],
  [{ text: "Khuôn viết lại" }, { text: "Thay chỗ bịa bằng mô tả" },
   { text: "không", options: { align: "center", color: MUTE } }, { text: "KHÔNG", options: { align: "center", bold: true, color: STEEL } }],
  [{ text: "Qwen2.5-VL-3B", options: { bold: true, color: ACCENT } }, { text: "Bộ sinh hướng dẫn, chạy trên máy người dùng", options: { bold: true } },
   { text: "có, LoRA adapter", options: { align: "center", bold: true, color: ACCENT } }, { text: "CÓ", options: { align: "center", bold: true, color: ACCENT } }],
];
s.addTable(PD, { x: M, y: 2.4, w: W - 2 * M, colW: [2.5, 4.65, 2.2, 2.14], rowH: 0.72, fontFace: BF, fontSize: 12, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle", color: BODY });
hpush(tableHTML(PD, M, 2.4, [2.5, 4.65, 2.2, 2.14], 0.72));
rect(M, 6.05, W - 2 * M, 0.95, TINT, { radius: 0.1 });
text([{ text: "Đọc theo cột cuối:  ", options: { bold: true, color: ACCENT } }, { text: "chỉ có đúng một ô CÓ. Ba thành phần trên là công cụ có sẵn, xoá đi sau khi huấn luyện xong thì hệ vẫn chạy. Xoá Qwen thì không còn gì.", options: { color: INK } }], { x: M + 0.3, y: 6.05, w: W - 2 * M - 0.6, h: 0.95, fontSize: 13.5, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
note(`Đây là slide trả lời thẳng lời phê "chưa thấy mô hình đâu".
Tiêu chí phân định, nếu thầy hỏi: một thành phần chỉ tính là mô hình do học viên train khi (1) có trọng số, (2) trọng số đổi vì dữ liệu của luận văn này, (3) cái đổi đó đo được.
nomic-embed-text đúng là mạng nơ-ron, em không giấu. Nhưng nó chạy đóng băng: đưa hai chuỗi chữ vào, nhận về một con số đo độ giống nghĩa. Không nhận gradient, không cập nhật tham số nào. Trượt ngay tiêu chí 2.
gpt-4o-mini gọi qua API, không sửa được tham số nào, và không có mặt trong sản phẩm cuối.
Phép thử: xoá cả ba thành phần đầu sau khi train xong, hệ vẫn chạy y nguyên vì sản phẩm giao đi chỉ gồm Qwen đã fine-tune.`);
pageno(); done();

// ============================================================ 8 · LUC DUNG THAT
slide();
head("Lúc dùng thật", "Chỉ còn một mình Student. Không Teacher, không mạng");
shot("real_mv_2.png", M + 0.1, 2.35, 1.62, 2.72);
rect(M, 5.22, 1.85, 0.72, FILL, { radius: 0.07 });
text("“Làm sao thêm một việc mới\nvà tính tiền theo giờ?”", { x: M, y: 5.22, w: 1.85, h: 0.72, fontSize: 10.5, italic: true, color: INK, fontFace: BF, align: "center", valign: "middle", lh: 1.2, margin: 0 });
arrow(3.05, 3.7, 0.5, ACCENT);
rect(3.75, 2.95, 2.5, 1.5, TINT, { radius: 0.1 });
text("Student", { x: 3.75, y: 3.2, w: 2.5, h: 0.4, fontSize: 17, bold: true, color: ACCENT, fontFace: TF, align: "center", margin: 0 });
text("chạy ngay trên máy", { x: 3.75, y: 3.62, w: 2.5, h: 0.3, fontSize: 11.5, color: BODY, fontFace: BF, align: "center", margin: 0 });
text("3B tham số", { x: 3.75, y: 3.9, w: 2.5, h: 0.3, fontSize: 11.5, color: MUTE, fontFace: BF, align: "center", margin: 0 });
arrow(6.4, 3.7, 0.5, ACCENT);
rect(7.1, 2.35, 5.3, 2.72, WHITE, { radius: 0.1, line: RULE, lw: 1 });
text("Hướng dẫn trả cho người dùng", { x: 7.35, y: 2.5, w: 3.4, h: 0.3, fontSize: 12, bold: true, color: MUTE, fontFace: BF, margin: 0 });
text("ví dụ minh hoạ", { x: 10.6, y: 2.5, w: 1.6, h: 0.3, fontSize: 10, italic: true, color: MUTE, fontFace: BF, align: "right", margin: 0 });
const OP = [["1.", "Chạm vào “Find or create a task”", INK], ["2.", "Nhập số giờ vào “Estimated hours”", INK],
            ["3.", "Tìm và chạm vào tuỳ chọn trên màn hình phù hợp với việc bạn cần làm ở bước này.", ACCENT],
            ["4.", "Chạm “SAVE & ADD ANOTHER” để lưu", INK]];
OP.forEach((r, i) => {
  const y = 2.9 + i * 0.52;
  text(r[0], { x: 7.35, y, w: 0.3, h: 0.4, fontSize: 12.5, bold: true, color: MUTE, fontFace: BF, margin: 0 });
  text(r[1], { x: 7.68, y, w: 4.5, h: 0.5, fontSize: 12.5, color: r[2], fontFace: BF, lh: 1.18, margin: 0 });
});
text("Ba tên nút đối chiếu được ngay trên ảnh bên trái.", { x: 7.35, y: 4.68, w: 4.85, h: 0.35, fontSize: 10.5, italic: true, color: ACCENT, fontFace: BF, margin: 0 });
const NI = ["Không cần gọi Teacher", "Không cần internet", "Không cần danh sách nút thật của màn hình"];
NI.forEach((t, i) => {
  const y = 5.5 + i * 0.5;
  circle(M + 2.3, y, 0.3, "F1E4DC", "✗", ACCENT);
  text(t, { x: M + 2.75, y: y - 0.05, w: 4.2, h: 0.4, fontSize: 13.5, color: INK, fontFace: BF, valign: "middle", margin: 0 });
});
rect(7.1, 5.4, 5.3, 1.5, TINT, { radius: 0.1 });
text("Vì sao chỗ này mới là chỗ quyết định", { x: 7.35, y: 5.55, w: 4.8, h: 0.3, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("Bộ kiểm tra không còn ở đó. Student vẫn thành thật thì điều đó chỉ có thể đến từ huấn luyện.", { x: 7.35, y: 5.88, w: 4.8, h: 0.95, fontSize: 12.5, color: INK, fontFace: BF, lh: 1.25, margin: 0 });
note(`Đây là hợp đồng vào/ra thật của hệ thống: chỉ ảnh + câu hỏi.
Câu hỏi hỏi Student cố ý KHÔNG chứa dặn dò "đừng bịa nút không có thật", trong khi prompt cho Teacher lúc sinh dữ liệu thì CÓ. Nếu Student cũng được nhắc thì không ai chứng minh được thói quen đến từ huấn luyện chứ không phải từ lời nhắc. Đây là bất đối xứng cố ý, và nó thiên về phía bất lợi cho mình.
Deliverable là checkpoint chạy trên máy. Việc đóng gói lên điện thoại thật là hướng mở rộng, chưa nằm trong luận văn này.`);
pageno(); done();

// ============================================================ 10 · NHIEU MAN — KIEN TRUC
slide();
head("Mở rộng: nhiều màn hình", "Không phải hệ thứ hai, mà là đúng hệ cũ cộng một khối cắm ở đầu");
text("Người dùng chụp cả một quy trình gồm nhiều màn nhưng thứ tự lộn xộn. Hệ phải tự khôi phục đúng thứ tự trước, rồi mới viết hướng dẫn.", { x: M, y: 2.1, w: 11.4, h: 0.4, fontSize: 13.5, color: BODY, fontFace: BF, margin: 0 });
// stage-0
rect(M, 2.7, 5.3, 3.0, TINT, { radius: 0.1 });
text("STAGE-0  ·  khối thêm mới", { x: M + 0.3, y: 2.88, w: 4.7, h: 0.3, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
const S0 = [["1", "Hỏi từng cặp: “màn nào đến trước?”", "4 màn → 6 câu · 5 màn → 10 câu"],
            ["2", "Copeland: đếm số trận thắng", "xếp từ điểm cao xuống thấp"],
            ["3", "Gặp vòng mâu thuẫn thì cắt dây yếu nhất", "đo khách quan, không hỏi model tự khai"]];
S0.forEach((r, i) => {
  const y = 3.3 + i * 0.78;
  circle(M + 0.3, y, 0.32, ACCENT, r[0]);
  text(r[1], { x: M + 0.75, y: y - 0.04, w: 4.3, h: 0.35, fontSize: 12.5, bold: true, color: INK, fontFace: BF, valign: "middle", margin: 0 });
  text(r[2], { x: M + 0.75, y: y + 0.3, w: 4.3, h: 0.3, fontSize: 10.5, italic: true, color: BODY, fontFace: BF, margin: 0 });
});
arrow(6.5, 4.2, 0.45, ACCENT);
// pipeline cu
rect(7.15, 2.7, 5.25, 3.0, FILL, { radius: 0.1 });
text("PIPELINE MỘT MÀN  ·  kế thừa nguyên vẹn", { x: 7.45, y: 2.88, w: 4.7, h: 0.3, fontSize: 12.5, bold: true, color: STEEL, fontFace: BF, margin: 0 });
text("chuỗi màn đã sắp\n↓\nTeacher viết nháp\n↓\nđối chiếu danh sách nút\n↓\nviết lại chỗ bịa\n↓\ndạy Student", { x: 7.45, y: 3.3, w: 4.7, h: 2.2, fontSize: 12.5, color: INK, fontFace: BF, align: "center", lh: 1.5, margin: 0 });
rect(M, 5.95, W - 2 * M, 1.05, NAVY, { radius: 0.1 });
text([{ text: "Khi chỉ có 1 màn, Stage-0 rỗng và mọi thứ trở về đúng hệ một màn.  ", options: { bold: true, color: "E4A986" } }, { text: "Nghĩa là phần làm mùa này không mất đi khi mở rộng, mà được dùng lại nguyên vẹn.", options: { color: WHITE } }], { x: M + 0.3, y: 5.95, w: W - 2 * M - 0.6, h: 1.05, fontSize: 13.5, fontFace: BF, valign: "middle", lh: 1.3, margin: 0 });
note(`PHẠM VI: phần nhiều màn đã thiết kế xong và có trụ khoa học đầy đủ, nhưng KHÔNG nằm trong kế hoạch 3 tháng. Nếu thầy hỏi có làm luôn không, trả lời: nó còn một cổng chưa chạy (K-pair), nếu cổng đó rớt thì cả nhánh vô hiệu. Em không muốn cược ba tháng vào một cổng chưa biết kết quả, trong khi nhánh một màn đã đủ khép kín để thành luận văn. Nhiều màn để dành cho bài mở rộng sau.
Điểm đáng nhấn: đây không phải hệ thứ hai. Stage-0 chỉ cắm thêm ở đầu, phần còn lại dùng lại y nguyên. Khi N=1 thì Stage-0 rỗng.
Bất biến chống rò rỉ: đáp án vàng và danh sách nút chỉ vào lúc CHẤM, không bao giờ vào lúc sắp thứ tự hay lúc sinh. Phải che đồng hồ, mức pin, huy hiệu số trên icon, vì model chỉ cần đọc đồng hồ là biết thứ tự mà không cần hiểu gì về giao diện. Trong dữ liệu đã tìm thấy đồng hồ 5:33 và huy hiệu số thật.`);
pageno(); done();

// ============================================================ 11 · NHIEU MAN — BA NHIP
slide();
head("Bên trong Stage-0", "Ba nhịp, mỗi nhịp có một bài báo bình duyệt đứng sau");
// nhip 1
rect(M, 2.25, 3.6, 2.5, FILL, { radius: 0.1 });
text("① Hỏi từng cặp", { x: M + 0.25, y: 2.42, w: 3.1, h: 0.32, fontSize: 13.5, bold: true, color: INK, fontFace: TF, margin: 0 });
text("“Trong hai màn này, màn nào đến trước?”\n\nCố ý không hỏi kiểu “sắp xếp cả N màn giúp tôi”, vì cách đó là hộp đen, không để lại dấu vết kiểm tra.", { x: M + 0.25, y: 2.8, w: 3.1, h: 1.6, fontSize: 11.5, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });
text("Qin, Findings NAACL 2024", { x: M + 0.25, y: 4.42, w: 3.1, h: 0.25, fontSize: 9.5, italic: true, color: STEEL, fontFace: BF, margin: 0 });
// nhip 2
rect(4.85, 2.25, 3.6, 2.5, FILL, { radius: 0.1 });
text("② Copeland", { x: 5.1, y: 2.42, w: 3.1, h: 0.32, fontSize: 13.5, bold: true, color: INK, fontFace: TF, margin: 0 });
text("Như một giải đấu vòng tròn: mỗi màn là một đội, mỗi câu hỏi cặp là một trận.\n\nĐiểm = số màn khác mà nó được xếp trước. Xếp theo điểm là ra thứ tự.", { x: 5.1, y: 2.8, w: 3.1, h: 1.6, fontSize: 11.5, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });
text("Dwork, WWW 2001", { x: 5.1, y: 4.42, w: 3.1, h: 0.25, fontSize: 9.5, italic: true, color: STEEL, fontFace: BF, margin: 0 });
// nhip 3
rect(8.8, 2.25, 3.6, 2.5, TINT, { radius: 0.1 });
text("③ Phá vòng", { x: 9.05, y: 2.42, w: 3.1, h: 0.32, fontSize: 13.5, bold: true, color: INK, fontFace: TF, margin: 0 });
text("Model có thể tự mâu thuẫn: A trước B, B trước C, nhưng C trước A.\n\nPhải cắt một dây để hết vòng. Cắt dây nào là chỗ có một quyết định đáng nói.", { x: 9.05, y: 2.8, w: 3.1, h: 1.6, fontSize: 11.5, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });
text("Ailon, J. ACM 2008", { x: 9.05, y: 4.42, w: 3.1, h: 0.25, fontSize: 9.5, italic: true, color: ACCENT, fontFace: BF, margin: 0 });
// quyet dinh M2
rect(M, 5.0, W - 2 * M, 1.25, WHITE, { radius: 0.1, line: ACCENT, lw: 1.5 });
text("Cắt dây nào?", { x: M + 0.3, y: 5.15, w: 2.2, h: 0.3, fontSize: 13, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("Cách hiển nhiên là hỏi model “mày chắc bao nhiêu phần trăm?” rồi cắt dây nó tự nhận là yếu. Cách đó đã bị loại: model ngôn ngữ hiệu chỉnh độ tự tin rất kém, nó tự tin ngay cả khi sai. Tin lời tự khai của model là rơi lại đúng cái bẫy để hệ tự chấm mình.", { x: 3.0, y: 5.12, w: 9.1, h: 0.55, fontSize: 11.5, color: BODY, fontFace: BF, lh: 1.28, margin: 0 });
text("Thay vào đó đo bằng ba tín hiệu khách quan:  khoảng cách thắng  ·  hỏi lại nhiều lần xem có lật không  ·  ưu tiên cắt ít dây nhất.", { x: 3.0, y: 5.72, w: 9.1, h: 0.4, fontSize: 11.5, bold: true, color: INK, fontFace: BF, margin: 0 });
text("Không phát minh pairwise, Copeland hay min-FAS. Đóng góp là ráp chúng thành một hệ sắp màn theo mục tiêu, phục vụ sinh hướng dẫn.", { x: M, y: 6.55, w: 11.4, h: 0.35, fontSize: 12.5, italic: true, color: BODY, fontFace: BF, margin: 0 });
note(`Cả sáu thành phần của Stage-0 đều đã xác minh venue: pairwise (Qin, Findings NAACL 2024), Copeland (Dwork, WWW 2001), min feedback arc set (Ailon, J.ACM 2008), tiền lệ tác vụ xáo ảnh rồi sắp lại (Sort Story, EMNLP 2016), thước tau thứ tự bộ phận (Fagin, SIAM J. Discrete Math 2006), tiền lệ dùng tau làm headline (Lapata, Computational Linguistics 2006).
Khai thẳng: luận văn không phát minh cái nào trong số đó. Đóng khung đúng là bài đầu tiên ráp chúng thành hệ sắp màn theo mục tiêu để sinh hướng dẫn, với chấm partial-order suy từ đáp án vàng.
Cổng K-pair: trước khi tin bất kỳ kết quả Copeland nào, phải đo độ chính xác so cặp THÔ của model so với đáp án vàng. Nếu chỉ quanh 0.5, tức bằng đoán mò, thì toàn bộ Stage-0 vô hiệu về nguyên tắc và phải khai thẳng. Cổng này chưa chạy.
Nếu K-pair rớt, nhánh này không bỏ mà chuyển thành một phát hiện âm tính hợp lệ: model so cặp không hơn đoán mò trên miền GUI.`);
pageno(); done();

// ---- write outputs ----
fs.mkdirSync("_preview_pipeline", { recursive: true });
const page = `<!doctype html><meta charset="utf-8"><style>
@page{size:${W}in ${H}in;margin:0}
*{margin:0;box-sizing:border-box}
.slide{position:relative;width:${W}in;height:${H}in;overflow:hidden;page-break-after:always}
</style>` + htmlSlides.join("\n");
fs.writeFileSync("_preview_pipeline/preview.html", page);

pres.writeFile({ fileName: "../LUAN_VAN_PIPELINE.pptx" })
  .then(f => console.log("PPTX ->", f, "| slides:", htmlSlides.length))
  .catch(e => console.error("ERR", e));
