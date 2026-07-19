// Deck v4 — PIPELINE + THUOC DO + BO THI NGHIEM, soan tu report/54 (huong model-centric moi).
// Dual-emit: ../LUAN_VAN_SLIDE_v4.pptx + _preview_v4/preview.html (QA bo cuc bang weasyprint).
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Luan van thac si";
pres.title = "Pipeline, thuoc do va bo thi nghiem - Faithful Distillation";

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
text("PIPELINE · THƯỚC ĐO · BỘ THÍ NGHIỆM", { x: M, y: 1.5, w: 11, h: 0.4, fontSize: 13, bold: true, color: "E4A986", fontFace: BF, spacing: 2.5, margin: 0 });
text("Dạy một mô hình nhỏ\nthói quen thành thật", { x: M - 0.02, y: 2.15, w: 9.6, h: 1.9, fontSize: 34, bold: true, color: WHITE, fontFace: TF, lh: 1.08, margin: 0 });
text("Cách xây pipeline, cách đo, và cách kiểm chứng", { x: M, y: 4.35, w: 9.4, h: 0.6, fontSize: 17, italic: true, color: "C9D2DC", fontFace: TF, margin: 0 });
text("Học viên · · · · ·      Giảng viên hướng dẫn · · · · ·      2026", { x: M, y: 6.55, w: 11, h: 0.4, fontSize: 13, color: "8FA0B2", fontFace: BF, margin: 0 });
shot("real_mv_1.png", 10.4, 2.0, 1.95, 3.2);
done();

// ============================================================ 2 · Y TUONG COT LOI
slide();
head("Ý tưởng cốt lõi", "Teacher hay bịa. Student được dạy lại cho cẩn thận");
rect(M, 2.55, 5.35, 3.15, FILL, { radius: 0.1 });
text("Teacher", { x: M + 0.3, y: 2.78, w: 4.7, h: 0.4, fontSize: 16.5, bold: true, color: STEEL, fontFace: TF, margin: 0 });
text("gpt-4o-mini · gọi qua API\n\nChỉ thấy ảnh + câu hỏi.\nKhông được xem danh sách nút.\n\n→ đôi khi bịa ra nút không tồn tại.", { x: M + 0.3, y: 3.25, w: 4.75, h: 2.3, fontSize: 14, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
arrow(6.55, 4.1, 0.55);
rect(7.4, 2.55, 5.0, 3.15, TINT, { radius: 0.1 });
text("Student", { x: 7.7, y: 2.78, w: 4.4, h: 0.4, fontSize: 16.5, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("Qwen2.5-VL-3B · tự fine-tune\n\nChỉ học phần lời Teacher\nđã lọc sạch bịa.\n\n→ sản phẩm chính của luận văn.", { x: 7.7, y: 3.25, w: 4.4, h: 2.3, fontSize: 14, color: BODY, fontFace: BF, lh: 1.35, margin: 0 });
rect(M, 6.0, W - 2 * M, 1.0, WHITE, { radius: 0.1, line: RULE, lw: 1 });
text([{ text: "Câu hỏi trọng tâm:  ", options: { bold: true, color: ACCENT } }, { text: "thói quen thành thật đó có thật sự ngấm vào Student, hay chỉ là vẻ ngoài phụ thuộc vào việc có ai kiểm tra hộ hay không?", options: { color: INK } }], { x: M + 0.3, y: 6.0, w: W - 2 * M - 0.6, h: 1.0, fontSize: 14.5, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
note(`Teacher là gpt-4o-mini, gọi qua API. Nó chỉ được nhìn ảnh + câu hỏi, cố tình KHÔNG cho xem danh sách nút — vì ta cần đúng những chỗ nó tự nhiên hay bịa.
Student là Qwen2.5-VL-3B, mô hình mở, em tự fine-tune bằng SFT-LoRA. Đây là sản phẩm chính của luận văn.
Điểm cần nhấn: Student KHÔNG học nguyên xi lời Teacher. Nó chỉ học phần đã lọc sạch bịa. Nên nó không phải bản sao thu nhỏ của Teacher.`);
pageno(); done();

// ============================================================ 3 · TOAN CANH PIPELINE (train time)
slide();
head("Pipeline lúc chuẩn bị dữ liệu", "Chạy một lần, ngoại tuyến, để tạo dữ liệu dạy Student");
const st1 = [
  ["Ảnh + câu hỏi", "Lấy từ kho ảnh màn hình ứng dụng có sẵn", STEEL],
  ["Teacher viết nháp", "Chỉ thấy ảnh, không thấy danh sách nút", STEEL],
  ["Đối chiếu nút thật", "Thuật toán so từng bước với màn hình", ACCENT],
  ["Viết lại chỗ bịa", "Đổi thành mô tả, không đoán nút khác", STEEL],
  ["Dạy Student", "Huấn luyện trên đúng phần đã lọc sạch", GOOD],
];
st1.forEach((c, i) => {
  const x = M + i * 2.32;
  rect(x, 2.85, 2.05, 1.85, i === 4 ? "EAF3EC" : (i === 2 ? TINT : FILL), { radius: 0.09 });
  circle(x + 0.16, 3.05, 0.5, c[2], String(i + 1));
  text(c[0], { x: x + 0.1, y: 3.65, w: 1.85, h: 0.55, fontSize: 13, bold: true, color: INK, fontFace: BF, align: "center", valign: "middle", lh: 1.1, margin: 0 });
  text(c[1], { x: x + 0.12, y: 4.22, w: 1.82, h: 0.44, fontSize: 10.5, color: BODY, fontFace: BF, align: "center", lh: 1.18, margin: 0 });
  if (i < 4) arrow(x + 2.07, 3.75, 0.22, ACCENT);
});
rect(M, 6.0, W - 2 * M, 1.0, NAVY, { radius: 0.1 });
text([{ text: "Kết quả:  ", options: { bold: true, color: "E4A986" } }, { text: "~1.700–2.870 mẫu huấn luyện đã lọc sạch bịa.", options: { color: WHITE } }], { x: M + 0.3, y: 6.0, w: W - 2 * M - 0.6, h: 1.0, fontSize: 14, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
note(`Toàn bộ luồng này chạy một lần, offline, chỉ để tạo ra tập dữ liệu huấn luyện.
Bước 3 dùng embedding nomic-embed-text, ngưỡng 0.55 đã freeze. Nó là hàm đo khoảng cách, đóng băng, không huấn luyện gì.
Bước 4 dùng khuôn mẫu cố định, cố ý KHÔNG gọi LLM — nếu để AI viết lại cho hay thì chính bước lọc lại mở ra chỗ bịa mới.
Chi phí: bước 2 khoảng 1-2 đô cho vài nghìn lượt gọi. Bước 5 là Colab.`);
pageno(); done();

// ============================================================ 4 · VI DU CU THE
slide();
head("Ví dụ cụ thể", "Một bước bịa được bắt và viết lại trước khi đưa vào dạy Student");
shot("real_mv_1.png", M + 0.1, 2.5, 2.05, 3.35, "Màn đặt giờ");
const er = [
  [{ text: "Teacher viết", options: { bold: true, fill: FILL, color: INK } }, { text: "Có nút này trên màn không?", options: { bold: true, fill: FILL, color: INK } }, { text: "Xử lý", options: { bold: true, fill: FILL, color: INK, align: "center" } }],
  [{ text: "Chọn giờ và phút" }, { text: "Có" }, { text: "giữ nguyên", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Chọn buổi “PM”" }, { text: "Có" }, { text: "giữ nguyên", options: { align: "center", color: GOOD, bold: true } }],
  [{ text: "Mở “Cài đặt”" }, { text: "Không có", options: { color: MUTE } }, { text: "viết lại thành mô tả", options: { align: "center", color: ACCENT, bold: true } }],
];
s.addTable(er, { x: 3.4, y: 2.5, w: 8.85, colW: [3.0, 3.2, 2.65], rowH: 0.6, fontFace: BF, fontSize: 13.5, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
hpush(tableHTML(er, 3.4, 2.5, [3.0, 3.2, 2.65], 0.6));
rect(3.4, 4.85, 8.85, 0.95, TINT, { radius: 0.09 });
text([{ text: "Câu được đưa vào dữ liệu dạy:  ", options: { bold: true, color: ACCENT } }, { text: "“Tìm và chạm vào tuỳ chọn trên màn hình phù hợp với việc cần làm ở bước này.”", options: { italic: true, color: INK } }], { x: 3.65, y: 4.85, w: 8.35, h: 0.95, fontSize: 13, fontFace: BF, valign: "middle", lh: 1.25, margin: 0 });
rect(3.4, 5.95, 8.85, 1.15, NAVY, { radius: 0.09 });
text([{ text: "Vì sao không đoán sang một nút thật khác gần đó?  ", options: { bold: true, color: "E4A986" } }, { text: "Thay nút bịa bằng một nút thật nhưng sai việc (kiểu bấm “Lưu” thay vì “Gửi”) khiến người dùng làm sai mà không hề hay biết. Lỗi âm thầm đó còn nguy hiểm hơn cả việc bịa.", options: { color: "D6DBE2" } }], { x: 3.65, y: 5.95, w: 8.35, h: 1.15, fontSize: 12.5, fontFace: BF, valign: "middle", lh: 1.24, margin: 0 });
note(`Đây là màn thật trong bộ dữ liệu, không phải ví dụ dựng.
Chỗ đáng nói: bước bịa không bị xoá, cũng không bị sửa thành một tên nút khác. Nếu đoán sang nút thật khác mà sai chức năng, người dùng vẫn làm sai mà không hề hay biết — lỗi đó âm thầm, còn nguy hiểm hơn cả bịa vì không ai phát hiện được.
Nên chọn cách viết lại thành mô tả: mất tính cụ thể nhưng không sai sự thật.`);
pageno(); done();

// ============================================================ 5 · LUC DUNG THAT (inference)
slide();
head("Lúc dùng thật", "Chỉ còn một mình Student. Không Teacher, không mạng");
// vao: anh that + cau hoi
shot("real_mv_2.png", M + 0.1, 2.35, 1.62, 2.72);
rect(M, 5.22, 1.85, 0.72, FILL, { radius: 0.07 });
text("“Làm sao thêm một việc mới\nvà tính tiền theo giờ?”", { x: M, y: 5.22, w: 1.85, h: 0.72, fontSize: 10.5, italic: true, color: INK, fontFace: BF, align: "center", valign: "middle", lh: 1.2, margin: 0 });
arrow(3.05, 3.7, 0.5, ACCENT);
// hoc tro
rect(3.75, 2.95, 2.5, 1.5, TINT, { radius: 0.1 });
text("Student", { x: 3.75, y: 3.2, w: 2.5, h: 0.4, fontSize: 17, bold: true, color: ACCENT, fontFace: TF, align: "center", margin: 0 });
text("chạy ngay trên máy", { x: 3.75, y: 3.62, w: 2.5, h: 0.3, fontSize: 11.5, color: BODY, fontFace: BF, align: "center", margin: 0 });
text("3B tham số", { x: 3.75, y: 3.9, w: 2.5, h: 0.3, fontSize: 11.5, color: MUTE, fontFace: BF, align: "center", margin: 0 });
arrow(6.4, 3.7, 0.5, ACCENT);
// ra: huong dan that
rect(7.1, 2.35, 5.3, 2.72, WHITE, { radius: 0.1, line: RULE, lw: 1 });
text("Hướng dẫn trả cho người dùng", { x: 7.35, y: 2.5, w: 3.4, h: 0.3, fontSize: 12, bold: true, color: MUTE, fontFace: BF, margin: 0 });
text("ví dụ minh hoạ", { x: 10.6, y: 2.5, w: 1.6, h: 0.3, fontSize: 10, italic: true, color: MUTE, fontFace: BF, align: "right", margin: 0 });
const outp = [["1.", "Chạm vào “Find or create a task”", INK], ["2.", "Nhập số giờ vào “Estimated hours”", INK],
              ["3.", "Tìm và chạm vào tuỳ chọn trên màn hình phù hợp với việc bạn cần làm ở bước này.", ACCENT],
              ["4.", "Chạm “SAVE & ADD ANOTHER” để lưu", INK]];
outp.forEach((r, i) => {
  const y = 2.9 + i * 0.52;
  text(r[0], { x: 7.35, y, w: 0.3, h: 0.4, fontSize: 12.5, bold: true, color: MUTE, fontFace: BF, margin: 0 });
  text(r[1], { x: 7.68, y, w: 4.5, h: 0.5, fontSize: 12.5, color: r[2], fontFace: BF, lh: 1.18, margin: 0 });
});
text("Ba tên nút đối chiếu được ngay trên ảnh bên trái.", { x: 7.35, y: 4.68, w: 4.85, h: 0.4, fontSize: 10.5, italic: true, color: ACCENT, fontFace: BF, lh: 1.2, margin: 0 });
// khong can gi
const notin = ["Không cần gọi Teacher", "Không cần internet", "Không cần danh sách nút thật của màn hình"];
notin.forEach((t, i) => {
  const y = 5.5 + i * 0.5;
  circle(M + 2.3, y, 0.3, "F1E4DC", "✗", ACCENT);
  text(t, { x: M + 2.75, y: y - 0.05, w: 4.2, h: 0.4, fontSize: 13.5, color: INK, fontFace: BF, valign: "middle", margin: 0 });
});
rect(7.1, 5.4, 5.3, 1.5, TINT, { radius: 0.1 });
text("Vì sao chỗ này mới là chỗ quyết định", { x: 7.35, y: 5.55, w: 4.8, h: 0.3, fontSize: 12.5, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("Bộ kiểm tra không còn ở đó. Student vẫn thành thật thì điều đó chỉ có thể đến từ huấn luyện.", { x: 7.35, y: 5.88, w: 4.8, h: 0.95, fontSize: 12.5, color: INK, fontFace: BF, lh: 1.25, margin: 0 });
note(`Đây là hợp đồng vào/ra thật của hệ thống: chỉ ảnh + câu hỏi.
Câu hỏi hỏi Student cố ý KHÔNG chứa dặn dò "đừng bịa nút không có thật", trong khi prompt cho Teacher lúc sinh dữ liệu thì CÓ. Nếu Student cũng được nhắc thì không ai chứng minh được thói quen đến từ huấn luyện chứ không phải từ lời nhắc.
Đây là bất đối xứng cố ý, và nó thiên về phía bất lợi cho mình — Student phải thắng dù bị nhắc ít hơn.`);
pageno(); done();

// ============================================================ 5b · TINH MOI (khac gi bai da co)
slide();
head("Khác gì những bài đã có", "Công thức chung đã có từ trước. Điểm mới nằm ở hai chỗ");
// cot trai: khong moi
rect(M, 2.3, 5.55, 3.3, FILL, { radius: 0.1 });
text("Đã có từ trước", { x: M + 0.3, y: 2.5, w: 4.95, h: 0.35, fontSize: 15, bold: true, color: STEEL, fontFace: TF, margin: 0 });
text("Ý tưởng “cho AI viết → lọc chỗ sai → lấy phần sạch dạy lại AI nhỏ hơn” đã có tên riêng trong giới nghiên cứu từ 2022.", { x: M + 0.3, y: 2.9, w: 4.95, h: 0.6, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
const prior = [["STaR", "2022", "đặt tên cho công thức sinh–lọc–học lại"],
               ["BLIP CapFilt", "ICML 2022", "đo riêng giá trị của bước lọc"],
               ["VGA", "EMNLP-F 2024", "dùng đúng loại danh sách nút để giảm bịa"],
               ["KnowAda", "NAACL 2025", "viết lại chỗ không chắc thành mô tả chung"]];
prior.forEach((r, i) => {
  const y = 3.6 + i * 0.47;
  text(r[0], { x: M + 0.3, y, w: 1.5, h: 0.35, fontSize: 12, bold: true, color: INK, fontFace: BF, margin: 0 });
  text(r[1], { x: M + 1.8, y, w: 1.15, h: 0.35, fontSize: 11, color: MUTE, fontFace: BF, margin: 0 });
  text(r[2], { x: M + 2.95, y, w: 2.35, h: 0.35, fontSize: 11, color: BODY, fontFace: BF, lh: 1.15, margin: 0 });
});
// cot phai: cai con lai
rect(6.85, 2.3, 5.55, 3.3, TINT, { radius: 0.1 });
text("Điểm mới của luận văn", { x: 7.15, y: 2.5, w: 4.95, h: 0.35, fontSize: 15, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
circle(7.15, 3.0, 0.34, ACCENT, "1");
text([{ text: "Bộ lọc dựa vào một nguồn bên ngoài\n", options: { bold: true, color: INK } },
      { text: "KnowAda để mô hình tự hỏi rồi tự chấm mình. Ở đây đối chiếu với danh sách nút thật, không phụ thuộc mô hình có tự biết mình sai hay không.", options: { color: BODY } }],
  { x: 7.62, y: 2.98, w: 4.5, h: 1.15, fontSize: 12, fontFace: BF, lh: 1.28, margin: 0 });
circle(7.15, 4.25, 0.34, ACCENT, "2");
text([{ text: "Một câu hỏi chưa ai đặt\n", options: { bold: true, color: INK } },
      { text: "Thói quen đó có ngấm vào mô hình nhỏ không, khi lúc dùng thật đã tắt hẳn bộ kiểm tra? Có thể trả lời là không. Chính vì thế nó mới là câu hỏi nghiên cứu.", options: { color: BODY } }],
  { x: 7.62, y: 4.23, w: 4.5, h: 1.2, fontSize: 12, fontFace: BF, lh: 1.28, margin: 0 });
rect(M, 5.9, W - 2 * M, 1.05, NAVY, { radius: 0.1 });
text([{ text: "Tóm lại:  ", options: { bold: true, color: "E4A986" } },
      { text: "công thức sinh, lọc, huấn luyện lại thì đã có. Cái chưa ai làm là hỏi xem thói quen né bịa có sống sót được khi nén xuống một mô hình nhỏ, lúc không còn gì để kiểm tra nữa hay không.", options: { color: WHITE } }],
  { x: M + 0.3, y: 5.9, w: W - 2 * M - 0.6, h: 1.05, fontSize: 13.5, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
note(`Nếu thầy hỏi kỹ từng bài:
- STaR (Zelikman 2022): đặt tên cho vòng lặp sinh-lọc-học lại.
- BLIP CapFilt (ICML 2022): có đo tách riêng giá trị bước lọc, giống thí nghiệm tầng một. Nhưng chưa từng hỏi hành vi còn giữ được không khi bỏ bộ lọc lúc dùng thật.
- VGA (Findings EMNLP 2024): cũng dùng VH giảm bịa cho GUI, nhưng ép model bám VH ngay từ lúc sinh. Mình để sinh tự do rồi mới lọc — giữ được đúng chỗ model lớn tự nhiên hay sai.
- KnowAda (NAACL 2025): cơ chế viết lại gần giống nhất, nhưng tự-hỏi-tự-chấm.
Không giấu chỗ trùng — cả bốn đều cite đầy đủ trong luận văn.`);
pageno(); done();

// ============================================================ 6 · MO HINH HUAN LUYEN RA SAO (LoRA)
slide();
head("Mô hình được huấn luyện ra sao", "Chỉ dạy lại một phần nhỏ, giữ nguyên phần còn lại");
text("Chỉ gắn thêm và dạy một phần nhỏ, phần còn lại đóng băng. Vừa một GPU Colab.", { x: M, y: 2.05, w: 11.3, h: 0.65, fontSize: 15, color: BODY, fontFace: BF, lh: 1.28, margin: 0 });
rect(M, 3.0, 5.3, 3.15, FILL, { radius: 0.1, line: RULE, lw: 1 });
text("Phần “nhìn”", { x: M + 0.3, y: 3.2, w: 4.7, h: 0.4, fontSize: 16, bold: true, color: STEEL, fontFace: TF, margin: 0 });
circle(M + 0.3, 3.75, 0.85, "DCE1E7");
text("Giữ nguyên hoàn toàn. Việc cần dạy là thói quen nói gì khi không chắc, không phải nhìn thấy gì.", { x: M + 1.4, y: 3.75, w: 3.55, h: 1.15, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.28, margin: 0 });
rect(6.5, 3.0, 5.9, 3.15, TINT, { radius: 0.1 });
text("Phần “nói”", { x: 6.8, y: 3.2, w: 5.3, h: 0.4, fontSize: 16, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
circle(6.8, 3.75, 0.85, ACCENT, "+", WHITE);
text("Gắn một miếng dán nhỏ có thể học được, và chỉ huấn luyện đúng miếng dán đó. Rẻ hơn hàng trăm lần, nhưng đủ để đổi thói quen viết.", { x: 7.9, y: 3.75, w: 4.4, h: 1.15, fontSize: 12.5, color: INK, fontFace: BF, lh: 1.28, margin: 0 });
text("Có hai bản được huấn luyện song song: một bản dạy từ dữ liệu đã lọc sạch, một bản đối chứng dạy từ đúng dữ liệu thô. Nhờ vậy mới tách được đâu là công của việc lọc.", { x: M, y: 6.35, w: 11.3, h: 0.65, fontSize: 13, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
note(`Cấu hình: LoRA rank 8, alpha 16, gắn vào q/k/v/o + gate/up/down projection của nhánh ngôn ngữ. Vision encoder đóng băng hoàn toàn.
Tiền lệ: ZonUI-3B (WACV 2026) fine-tune đúng Qwen2.5-VL-3B với đúng cấu hình này trên một GPU 24GB. Khai thẳng: đây là tiền lệ DUY NHẤT xác nhận trực tiếp, không phải nhiều nguồn hội tụ — nên coi là điểm khởi đầu hợp lý cần tự validate bằng dev-loss, không phải trị số đã chứng minh tối ưu.
QLoRA 4-bit là mặc định vì Colab không đảm bảo GPU cố định.
Bằng chứng có train thật: Δ trọng số adapter, loss curve theo epoch trên held-out, hai checkpoint độc lập.`);
pageno(); done();

// ============================================================ 7 · DU LIEU & CACH CHIA
slide();
head("Dữ liệu và cách chia", "Khoá danh sách ứng dụng trước, không sửa sau khi đã nhìn kết quả");
// anh that
shot("real_mv_1.png", M, 2.3, 1.62, 2.72, "Ảnh màn hình thật");
text("kèm sẵn danh sách nút thật", { x: M - 0.07, y: 5.48, w: 1.8, h: 0.4, fontSize: 10.5, color: MUTE, fontFace: BF, align: "center", margin: 0 });
// so do chia 30 -> 18 / 12
rect(3.9, 2.3, 2.5, 0.82, FILL, { radius: 0.09, line: RULE, lw: 1 });
text("30 ứng dụng", { x: 3.9, y: 2.4, w: 2.5, h: 0.36, fontSize: 16.5, bold: true, color: INK, fontFace: TF, align: "center", margin: 0 });
text("đã qua vòng lọc chất lượng", { x: 3.9, y: 2.76, w: 2.5, h: 0.26, fontSize: 10.5, color: MUTE, fontFace: BF, align: "center", margin: 0 });
rect(5.13, 3.12, 0.03, 0.3, STEEL);              // doc
rect(4.18, 3.4, 1.95, 0.03, STEEL);              // ngang
rect(4.18, 3.4, 0.03, 0.3, STEEL);               // nhanh trai
rect(6.1, 3.4, 0.03, 0.3, STEEL);                // nhanh phai
rect(3.28, 3.7, 1.8, 1.0, NAVY, { radius: 0.09 });
text("18", { x: 3.28, y: 3.82, w: 1.8, h: 0.46, fontSize: 24, bold: true, color: WHITE, fontFace: TF, align: "center", margin: 0 });
text("để dạy Student", { x: 3.28, y: 4.28, w: 1.8, h: 0.28, fontSize: 11, color: "C9D2DC", fontFace: BF, align: "center", margin: 0 });
rect(5.23, 3.7, 1.8, 1.0, ACCENT, { radius: 0.09 });
text("12", { x: 5.23, y: 3.82, w: 1.8, h: 0.46, fontSize: 24, bold: true, color: WHITE, fontFace: TF, align: "center", margin: 0 });
text("chỉ để chấm", { x: 5.23, y: 4.28, w: 1.8, h: 0.28, fontSize: 11, color: "F7DECB", fontFace: BF, align: "center", margin: 0 });
text("Student không bao giờ thấy 12 ứng dụng này lúc học", { x: 3.28, y: 4.82, w: 3.75, h: 0.3, fontSize: 10.5, italic: true, color: MUTE, fontFace: BF, align: "center", margin: 0 });
// mo rong da chay
rect(7.65, 2.3, 4.76, 2.4, "EAF3EC", { radius: 0.1 });
text("✓  Lấy thêm dữ liệu dạy · đã chạy 12/7", { x: 7.95, y: 2.48, w: 4.2, h: 0.3, fontSize: 13, bold: true, color: GOOD, fontFace: BF, margin: 0 });
text([{ text: "498", options: { fontSize: 27, bold: true, color: INK, fontFace: TF } }, { text: "  màn hình mới,  ", options: { fontSize: 13.5, color: BODY } },
      { text: "220", options: { fontSize: 27, bold: true, color: INK, fontFace: TF } }, { text: "  ứng dụng mới", options: { fontSize: 13.5, color: BODY } }],
  { x: 7.95, y: 2.85, w: 4.2, h: 0.5, fontFace: BF, margin: 0 });
rect(7.95, 3.5, 4.16, 0.98, WHITE, { radius: 0.07 });
text([{ text: "0 ca rò rỉ.  ", options: { bold: true, color: GOOD, fontSize: 13 } }, { text: "Kiểm bằng cả tên app lẫn perceptual-hash của ảnh.", options: { color: BODY, fontSize: 11.5 } }],
  { x: 8.08, y: 3.5, w: 3.9, h: 0.98, fontFace: BF, valign: "middle", lh: 1.24, margin: 0 });
// chu thich duoi
text("Chia theo APP, không theo màn. Màn cùng app quá giống nhau.", { x: 3.28, y: 5.25, w: 9.1, h: 0.4, fontSize: 13, color: BODY, fontFace: BF, margin: 0 });
note(`Split khoá bằng git commit ngày 12/7, seed 20260710, trước mọi lệnh gọi API. Tổng 127 màn / 30 app đã qua lọc chất lượng, cộng pool mở rộng thành ~574 màn để dạy.
MobileViews: preprint arXiv 2409.14337, giấy phép MIT, thu thập tự động bằng bot. Khai thẳng nó là preprint chưa bình duyệt — đóng khung là hiện vật kỹ thuật, không phải trụ khoa học.
Vì sao 18/12 chứ không 80/20: 30 app này là bộ duy nhất đã qua vòng lọc chất lượng; 20% của 30 chỉ còn 6 app, quá mỏng để kết luận.
Việc mở rộng đã chạy 12/7: 498 màn/220 app. Kiểm rò rỉ bằng cả tên app lẫn perceptual-hash của ảnh — phòng hai app khác tên dùng chung khuôn giao diện. Kết quả 0 ca.`);
pageno(); done();

// ============================================================ 8 · DIVIDER: THUOC DO
divider("Phần hai", "Thước đo", "Không có đáp án mẫu để chấm. Vậy làm sao biết Student có thành thật?");

// ============================================================ 9 · VI SAO KHO DO
slide();
head("Vì sao việc đo lại khó", "Bộ lọc không được đi chấm chính nó");
// TRAI: ban dau — con so ao
rect(M, 2.25, 5.5, 3.5, FILL, { radius: 0.1 });
text("Bản đầu của luận văn", { x: M + 0.35, y: 2.5, w: 4.8, h: 0.35, fontSize: 14, bold: true, color: STEEL, fontFace: BF, margin: 0 });
text("~100%", { x: M + 0.35, y: 2.95, w: 4.8, h: 1.0, fontSize: 54, bold: true, color: "C0392B", fontFace: TF, margin: 0 });
text("điểm trung thực", { x: M + 0.35, y: 3.95, w: 4.8, h: 0.3, fontSize: 13, color: MUTE, fontFace: BF, margin: 0 });
rect(M + 0.35, 4.4, 4.8, 1.05, WHITE, { radius: 0.07 });
text("Con số này vô nghĩa. Bộ lọc vừa sửa dữ liệu vừa chấm chính dữ liệu đó, nên nó chỉ đang đồng ý với chính mình.", { x: M + 0.5, y: 4.4, w: 4.5, h: 1.05, fontSize: 12.5, color: INK, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
// PHAI: ban nay — tach doi
rect(7.15, 2.25, 5.25, 3.5, TINT, { radius: 0.1 });
text("Bản này: tách hẳn hai vai", { x: 7.5, y: 2.5, w: 4.6, h: 0.35, fontSize: 14, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
rect(7.5, 2.95, 4.6, 1.05, WHITE, { radius: 0.07 });
text("LỌC  lúc dạy", { x: 7.65, y: 3.05, w: 4.3, h: 0.3, fontSize: 11.5, bold: true, color: MUTE, fontFace: BF, margin: 0 });
text("nomic-embed-text · ngưỡng 0.55", { x: 7.65, y: 3.38, w: 4.3, h: 0.35, fontSize: 13.5, color: INK, fontFace: BF, margin: 0 });
rect(7.5, 4.15, 4.6, 1.3, WHITE, { radius: 0.07 });
text("CHẤM  lúc kiểm tra", { x: 7.65, y: 4.25, w: 4.3, h: 0.3, fontSize: 11.5, bold: true, color: MUTE, fontFace: BF, margin: 0 });
text("bge-m3  ·  llama3.2  ·  token-overlap", { x: 7.65, y: 4.58, w: 4.3, h: 0.35, fontSize: 13.5, color: INK, fontFace: BF, margin: 0 });
text("khác họ nhau, và đều khác họ Teacher", { x: 7.65, y: 4.95, w: 4.3, h: 0.3, fontSize: 11.5, italic: true, color: ACCENT, fontFace: BF, margin: 0 });
text("Thứ dùng để lọc dữ liệu lúc dạy, tuyệt đối không được dùng lại để chấm điểm lúc kiểm tra.", { x: M, y: 6.05, w: 11.5, h: 0.4, fontSize: 14, bold: true, color: INK, fontFace: BF, margin: 0 });
note(`Đây là lỗi bản đầu đã mắc và bị bắt trong một vòng rà soát nội bộ: bộ lọc vừa sửa dữ liệu vừa chấm chính dữ liệu đó, nên faithfulness vọt lên gần 100%. Con số đó là tautology, không phải kết quả.
Cách vá: nomic (ngưỡng 0.55 đã freeze) chỉ dùng lúc lọc. Lúc chấm dùng ba cơ chế khác họ, ngưỡng hiệu chuẩn riêng.
Khai thẳng giới hạn: ba cơ chế chỉ GIẢM chứ không LOẠI tương quan sai số. bge-m3 và llama3.2 đều là mạng nơ-ron, vẫn có thể sai giống nhau. Chỉ token-overlap là trục thực sự khác cơ chế. Nên luận văn báo hệ số tương quan giữa các bộ chấm, thay vì tuyên bố chúng độc lập.`);
pageno(); done();

// ============================================================ 10 · BA CACH CHAM DOC LAP
slide();
head("Ba cách chấm độc lập", "Một bước chỉ bị coi là bịa khi đa số đồng ý");
const j = [
  ["Một mô hình so nghĩa khác họ", "Không cùng dòng với công cụ đã dùng để lọc dữ liệu lúc dạy"],
  ["Một mô hình giám khảo khác dòng", "Không cùng dòng với Teacher, để tránh thiên vị"],
  ["Một phép so khớp từ ngữ đơn giản", "Làm đối chứng, không phụ thuộc một mô hình nào"],
];
j.forEach((c, i) => {
  const x = M + i * 3.92;
  rect(x, 2.75, 3.6, 2.5, i === 1 ? TINT : FILL, { radius: 0.1 });
  circle(x + 0.28, 3.02, 0.62, i === 1 ? ACCENT : STEEL, String(i + 1));
  text(c[0], { x: x + 0.3, y: 3.78, w: 3.0, h: 0.75, fontSize: 14, bold: true, color: INK, fontFace: BF, lh: 1.2, margin: 0 });
  text(c[1], { x: x + 0.3, y: 4.55, w: 3.0, h: 0.6, fontSize: 12, color: BODY, fontFace: BF, lh: 1.22, margin: 0 });
});
rect(M, 5.55, W - 2 * M, 1.15, NAVY, { radius: 0.1 });
text([{ text: "Quy tắc quyết định:  ", options: { bold: true, color: "E4A986" } }, { text: "một bước bị coi là bịa khi ít nhất hai trong ba cách trên cùng đồng ý là không khớp. Không cách nào tự quyết một mình.", options: { color: WHITE } }], { x: M + 0.3, y: 5.55, w: W - 2 * M - 0.6, h: 1.15, fontSize: 14, fontFace: BF, valign: "middle", lh: 1.28, margin: 0 });
note(`Ba cơ chế: bge-m3 (khác họ nomic), llama3.2 chạy local làm judge (khác họ generator gpt-4o-mini — vì generator là GPT-family thì judge không được dùng GPT-family, trụ: Panickssery NeurIPS 2024 về self-preference bias), và token-overlap phi-neural.
Quy tắc: một bước bị kết luận là bịa khi ít nhất 2/3 đồng ý không khớp.
τB phải hiệu chuẩn riêng bằng 80-120 cặp gán tay, KHÔNG được tái dùng ngưỡng 0.55 của nomic — hai mô hình nhúng khác nhau, không có lý do gì ngưỡng trùng.`);
pageno(); done();

// ============================================================ 11 · NHUNG CON SO SE BAO CAO
slide();
head("Những con số sẽ báo cáo", "Ba con số chính, mỗi con số kèm ý nghĩa thật của nó");
const numRows = [
  [{ text: "Con số", options: { bold: true, fill: FILL, color: INK } }, { text: "Ý nghĩa", options: { bold: true, fill: FILL, color: INK } }, { text: "Ước tính sơ bộ*", options: { bold: true, fill: FILL, color: INK, align: "center" } }],
  [{ text: "Tỉ lệ bịa của Teacher" }, { text: "Bao nhiêu phần bước nhắc một nút không tồn tại" }, { text: "khoảng 1/4 số bước", options: { align: "center", bold: true, color: ACCENT } }],
  [{ text: "Tỉ lệ phải viết lại" }, { text: "Bao nhiêu phần bước bị đổi thành mô tả chung chung vì bị lọc" }, { text: "khoảng 1/5 số bước", options: { align: "center", bold: true, color: ACCENT } }],
  [{ text: "Tỉ lệ lỗi âm thầm" }, { text: "Nếu đoán đại nút khác thay chỗ bịa: bao nhiêu bước bị thay bằng nút CÓ THẬT nhưng sai việc" }, { text: "đang đo tiếp", options: { align: "center", color: MUTE } }],
];
s.addTable(numRows, { x: M, y: 2.55, w: W - 2 * M, colW: [3.3, 5.9, 2.29], rowH: 0.72, fontFace: BF, fontSize: 13, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
hpush(tableHTML(numRows, M, 2.55, [3.3, 5.9, 2.29], 0.72));
text("* Đo từ một lần thử nhỏ trước đó, trên một mô hình và một tập ảnh giới hạn. Dùng để ước lượng quy mô dữ liệu cần lọc, chưa phải kết quả cuối của Student sau huấn luyện.", { x: M, y: 5.5, w: 11.5, h: 0.5, fontSize: 12, italic: true, color: MUTE, fontFace: BF, lh: 1.25, margin: 0 });
rect(M, 6.15, W - 2 * M, 0.85, FILL, { radius: 0.1 });
text([{ text: "Con số của Student sau khi huấn luyện  ", options: { bold: true, color: INK } }, { text: "là con số quyết định, nằm ở phần bộ thí nghiệm tiếp theo.", options: { color: BODY } }], { x: M + 0.3, y: 6.15, w: W - 2 * M - 0.6, h: 0.85, fontSize: 13.5, fontFace: BF, valign: "middle", lh: 1.25, margin: 0 });
note(`Faithfulness = 1 − (số lần nhắc nút bịa / tổng số lần nhắc nút), theo ALOHa (NAACL 2024). Gộp trung bình theo từng app trước, ra 12 con số — vì các màn cùng app không độc lập.
Con số ~1/4 là quan sát sơ bộ trên MỘT model, một tập ảnh giới hạn. Không phải headline, sẽ đo lại.
Ba điều kiện phải khai khi báo: độ phủ nhãn VH; mẫu chỉ giữ màn dày nhãn nên tỉ lệ bịa quan sát được là hạ thấp có hệ thống; và con số hiện có mới trên một model.
Estimand là trung bình đều trên app — cấm viết "đại diện cho ứng dụng nói chung".`);
pageno(); done();

// ============================================================ 12 · KIEM TRA DO TIN CUA PHEP DO
slide();
head("Kiểm tra độ tin của phép đo", "Trước khi tin một con số, phải biết phép đo có thật sự nhạy hay không");
rect(M, 2.6, 5.5, 3.15, FILL, { radius: 0.1 });
text("Cách làm", { x: M + 0.3, y: 2.8, w: 4.9, h: 0.35, fontSize: 14, bold: true, color: STEEL, fontFace: BF, margin: 0 });
text("Chèn 4 loại lỗi đã biết trước, độc lập với matcher, rồi xem phép đo có bắt được không.", { x: M + 0.3, y: 3.25, w: 4.9, h: 2.3, fontSize: 13.5, color: BODY, fontFace: BF, lh: 1.3, margin: 0 });
rect(7.15, 2.6, 5.25, 3.15, TINT, { radius: 0.1 });
text("Ngưỡng đăng ký trước", { x: 7.45, y: 2.8, w: 4.65, h: 0.35, fontSize: 14, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("Bắt được ≥ 80% lỗi đã chèn.\nBáo nhầm ≤ 10% trên bước đúng.\nChèn càng nhiều lỗi, điểm phải giảm đều (Spearman < 0, p < 0.05).\n\nKhông đạt thì rút claim, không hứa suông.", { x: 7.45, y: 3.25, w: 4.65, h: 2.3, fontSize: 13.5, color: INK, fontFace: BF, lh: 1.3, margin: 0 });
rect(M, 6.0, W - 2 * M, 1.0, NAVY, { radius: 0.1 });
text([{ text: "Việc này làm độc lập với bộ lọc dữ liệu lúc dạy  ", options: { bold: true, color: "E4A986" } }, { text: "lỗi bơm vào không do cùng cơ chế tạo ra lỗi thật, để tránh phép đo chỉ giỏi bắt đúng loại lỗi nó quen thuộc.", options: { color: WHITE } }], { x: M + 0.3, y: 6.0, w: W - 2 * M - 0.6, h: 1.0, fontSize: 13.5, fontFace: BF, valign: "middle", lh: 1.25, margin: 0 });
note(`Bốn loại lỗi bơm vào: đổi tên nút thật thành tên không có trên màn; đổi sang nút có thật nhưng sai màn; chèn thêm bước nhắc nút bịa; hoán tên nút giữa hai màn.
Quan trọng: lỗi được bơm ĐỘC LẬP với matcher, nếu không lại rơi vào vòng tự kiểm.
Trụ: Sai et al. EMNLP 2021.
Phạm vi phải khai: đây là điều kiện CẦN (độ nhạy), KHÔNG phải convergent validity với đánh giá của người. Human-correlation là future work, không phải cổng đậu/rớt (Clark ACL-IJCNLP 2021).`);
pageno(); done();

// ============================================================ 13 · DIVIDER: BO THI NGHIEM
divider("Phần ba", "Bộ thí nghiệm", "Khi không còn ai kiểm tra hộ nữa, thói quen thành thật của Student có còn giữ được không?");

// ============================================================ 14 · HAI TANG THI NGHIEM
slide();
head("Hai tầng thí nghiệm", "Tách riêng phần chắc thắng và phần câu hỏi mới");
rect(M, 2.55, 5.5, 3.55, "EAF3EC", { radius: 0.1 });
text("Tầng một · lưới an toàn", { x: M + 0.3, y: 2.75, w: 4.9, h: 0.4, fontSize: 15, bold: true, color: GOOD, fontFace: TF, margin: 0 });
text("So sánh:", { x: M + 0.3, y: 3.25, w: 4.9, h: 0.3, fontSize: 12, bold: true, color: STEEL, fontFace: BF, margin: 0 });
text("Student dạy từ dữ liệu sạch\nvới\nStudent dạy từ dữ liệu thô", { x: M + 0.3, y: 3.55, w: 4.9, h: 0.6, fontSize: 13, color: INK, fontFace: BF, lh: 1.25, margin: 0 });
text("Chấm trên bản model tự viết ra, chưa qua lớp viết lại.", { x: M + 0.3, y: 4.2, w: 4.9, h: 0.4, fontSize: 12.5, color: BODY, fontFace: BF, margin: 0 });
text("Gần như chắc thắng.", { x: M + 0.3, y: 4.72, w: 4.9, h: 0.35, fontSize: 14, bold: true, color: GOOD, fontFace: BF, margin: 0 });
text("Việc lọc dữ liệu có tạo ra khác biệt đo được hay không.", { x: M + 0.3, y: 5.08, w: 4.9, h: 0.5, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
rect(7.15, 2.55, 5.25, 3.55, TINT, { radius: 0.1 });
text("Tầng hai · câu hỏi mới", { x: 7.45, y: 2.75, w: 4.65, h: 0.4, fontSize: 15, bold: true, color: ACCENT, fontFace: TF, margin: 0 });
text("So sánh:", { x: 7.45, y: 3.25, w: 4.65, h: 0.3, fontSize: 12, bold: true, color: STEEL, fontFace: BF, margin: 0 });
text("Student\nvới\nchính Teacher", { x: 7.45, y: 3.55, w: 4.65, h: 0.6, fontSize: 13, color: INK, fontFace: BF, lh: 1.25, margin: 0 });
text("Cả hai đều bị tắt danh sách nút. Cùng một đề thi.", { x: 7.45, y: 4.2, w: 4.65, h: 0.4, fontSize: 12.5, color: BODY, fontFace: BF, margin: 0 });
text("Có thể ra kết quả rỗng.", { x: 7.45, y: 4.72, w: 4.65, h: 0.35, fontSize: 14, bold: true, color: ACCENT, fontFace: BF, margin: 0 });
text("Thói quen thành thật có ngấm vào trọng số hay không.", { x: 7.45, y: 5.08, w: 4.65, h: 0.5, fontSize: 12.5, color: BODY, fontFace: BF, lh: 1.25, margin: 0 });
text("Hai tầng báo cáo độc lập. Tầng hai rỗng thì tầng một vẫn đứng.", { x: M, y: 6.35, w: 11.5, h: 0.4, fontSize: 13.5, color: BODY, fontFace: BF, margin: 0 });
note(`Vì sao tách hai tầng thay vì gộp một con số: với 12 app, rủi ro lớn nhất không phải null mà là kết quả mơ hồ — không đủ tin cậy để nói lên điều gì. Mơ hồ thì không kể được câu chuyện nào.
Tách ra thì tầng một luôn có chuyện chắc chắn để kể, bất kể tầng hai ra sao.
Chi tiết dễ bị vặn: cả hai tầng đều chấm trên output THÔ, trước lớp viết lại. Vì lớp viết lại chữa bịa cho MỌI bản — chấm sau viết lại thì cả Student lẫn Student-RAW đều sạch, Δ ≈ 0, null giả tạo. Lợi ích của lớp viết lại báo riêng qua %fallback.`);
pageno(); done();

// ============================================================ 15 · BA KET CUC + CACH KIEM DINH
slide();
head("Ba kết cục, và cách kiểm chứng", "Cả ba cách diễn giải đã chốt trước khi nhìn số");
const outc = [
  [{ text: "Kết cục", options: { bold: true, fill: FILL, color: INK } }, { text: "Ý nghĩa", options: { bold: true, fill: FILL, color: INK } }],
  [{ text: "Thắng đầy đủ", options: { bold: true, color: GOOD } }, { text: "Thói quen thành thật đã ngấm thật vào Student" }],
  [{ text: "Thắng một phần", options: { bold: true, color: ACCENT } }, { text: "Có ngấm, nhưng còn yếu. Vẫn là một phát hiện có giá trị" }],
  [{ text: "Không thấy khác biệt", options: { bold: true, color: STEEL } }, { text: "Giới hạn thật của phương pháp. Không phải cả luận văn thất bại, vì tầng một đứng độc lập" }],
];
s.addTable(outc, { x: M, y: 2.55, w: 6.6, colW: [2.4, 4.2], rowH: 0.72, fontFace: BF, fontSize: 12.5, border: { type: "solid", color: RULE, pt: 1 }, valign: "middle" });
hpush(tableHTML(outc, M, 2.55, [2.4, 4.2], 0.72));
rect(8.0, 2.55, 4.4, 3.0, FILL, { radius: 0.1 });
text("Cách kiểm chứng cho mẫu nhỏ", { x: 8.25, y: 2.75, w: 3.9, h: 0.4, fontSize: 13, bold: true, color: STEEL, fontFace: BF, margin: 0 });
text("Chỉ 12 ứng dụng để kiểm tra. Mẫu nhỏ, nên không ước lượng gần đúng.\n\nMáy liệt kê hết 4.096 cách đổi dấu 12 con số chênh lệch, rồi xem kết quả thật nổi bật tới đâu so với toàn bộ khả năng ngẫu nhiên.", { x: 8.25, y: 3.2, w: 3.9, h: 2.2, fontSize: 12, color: BODY, fontFace: BF, lh: 1.28, margin: 0 });
pageno(); done();

// ============================================================ 16 · BO THI NGHIEM DAY DU
slide();
head("Bộ thí nghiệm", "Sáu thí nghiệm, mỗi cái trả lời một câu vặn khác nhau");
const EXP = [
  [{ text: "#", options: { bold: true, fill: FILL, color: INK, align: "center" } },
   { text: "So gì với gì", options: { bold: true, fill: FILL, color: INK } },
   { text: "Ngưỡng đậu", options: { bold: true, fill: FILL, color: INK } },
   { text: "Chặn được câu vặn", options: { bold: true, fill: FILL, color: INK } }],
  [{ text: "1", options: { align: "center", bold: true, color: GOOD } },
   { text: "Student  vs  Student-RAW", options: { bold: true } },
   { text: "CI 95% của Δ nằm trên 0" },
   { text: "“Giỏi lên là nhờ fine-tune nói chung, đâu phải nhờ lọc?”" }],
  [{ text: "2", options: { align: "center", bold: true, color: ACCENT } },
   { text: "Student  vs  Teacher-BASE\ntắt VH · app chưa từng thấy", options: { bold: true } },
   { text: "CI 95% trên 0  VÀ\nΔ_test ≥ 0.5 × Δ_train" },
   { text: "“Thói quen đó có ngấm vào trọng số không?”  ← trụ chính, có thể null" }],
  [{ text: "3", options: { align: "center", color: STEEL } },
   { text: "%fallback · lỗi ngầm · màn 0-nhắc-nút" },
   { text: "báo kèm bắt buộc" },
   { text: "“Cứ nói chung chung là bịa = 0, ăn gian thước!”" }],
  [{ text: "4", options: { align: "center", color: STEEL } },
   { text: "Độ hữu ích:  Student vs Student-RAW" },
   { text: "trong family Holm" },
   { text: "“Sạch nhưng mơ hồ, vô dụng thì sao?”" }],
  [{ text: "5", options: { align: "center", color: STEEL } },
   { text: "Bộ chấm bge-m3  vs  người · 80–120 cặp" },
   { text: "precision ≥ 0.95, báo κ" },
   { text: "“Lấy gì bảo đảm bộ chấm đúng?”" }],
  [{ text: "6", options: { align: "center", color: STEEL } },
   { text: "Bơm lỗi đã biết  vs  thước đo" },
   { text: "bắt ≥ 0.80 · báo nhầm ≤ 0.10" },
   { text: "“Phép đo có thật sự nhạy không?”" }],
];
s.addTable(EXP, { x: M, y: 2.05, w: W - 2 * M, colW: [0.45, 3.45, 2.85, 4.74], rowH: 0.57, fontFace: BF, fontSize: 11,
  border: { type: "solid", color: RULE, pt: 1 }, valign: "middle", color: BODY, autoPage: false });
hpush(tableHTML(EXP, M, 2.05, [0.45, 3.45, 2.85, 4.74], 0.57));
rect(M, 6.35, W - 2 * M, 0.7, NAVY, { radius: 0.09 });
text([{ text: "1 và 2 mang kết luận.  ", options: { bold: true, color: "E4A986" } },
      { text: "3–6 là lá chắn, để mỗi câu vặn đều có sẵn một con số trả lời.", options: { color: WHITE } }],
  { x: M + 0.3, y: 6.35, w: W - 2 * M - 0.6, h: 0.7, fontSize: 13, fontFace: BF, valign: "middle", margin: 0 });
note(`KÝ HIỆU (nếu cần nói rõ):
Δ = chênh lệch điểm trung thực giữa hai bên đang so. Mỗi app test cho một con số Δ → 12 app → 12 con số. Δ dương nghĩa là Student tốt hơn.
CI 95% = khoảng tin cậy. Ví dụ Δ trung bình 12 điểm, CI = [4, 20] → khá chắc giá trị thật nằm giữa 4 và 20. CI nằm HOÀN TOÀN trên 0 nghĩa là kể cả kịch bản bi quan nhất Student vẫn hơn ⇒ khác biệt là thật. CI còn chứa 0 thì chưa loại trừ được khả năng hai bên bằng nhau.
Δ_train = mức chênh lệch đo trên 18 app ĐÃ học (điều kiện thuận lợi nhất). Δ_test = trên 12 app lạ. Điều kiện Δ_test ≥ 0.5 × Δ_train đòi sang app lạ phải giữ được ít nhất một nửa mức cải thiện đó. Ví dụ app đã học hơn 20 điểm thì app lạ phải hơn ít nhất 10 điểm.

Trước khi chạy bất kỳ cái nào: một cổng bắt buộc — tính MDE bằng số liệu pilot thật. Nếu MDE lớn hơn 15-20 điểm phần trăm thì phải đổi chia 18/12 thành 15/15 TRƯỚC khi khoá ngưỡng, vì lúc đó thiết kế không đủ sức phát hiện khác biệt.
Thí nghiệm 1 gần như chắc dương theo tiền lệ — đó là lưới an toàn. Nếu ngay cả nó cũng null thì dừng lại rà toàn bộ pipeline lọc, không diễn giải tiếp thí nghiệm 2.
Thí nghiệm 2 là chỗ có thể null thật. Nếu null: báo trung thực kèm MDE, đó là giới hạn tổng quát hoá — không phải luận văn thất bại, vì 1 đứng độc lập.
Hệ số 0.5 ở thí nghiệm 2 là tự đề xuất, khai rõ trong luận văn, không lấy từ literature nào.
Thí nghiệm 6 nếu không kịp dựng thì rút claim tương ứng khỏi bài báo, không hứa suông.
Còn một thí nghiệm phụ (trộn 25/50/75% dữ liệu lọc) chưa đăng ký trước nên chỉ báo dạng thăm dò.`);
pageno(); done();

// ---- write outputs ----
fs.mkdirSync("_preview_v4", { recursive: true });
const page = `<!doctype html><meta charset="utf-8"><style>
@page{size:${W}in ${H}in;margin:0}
*{margin:0;box-sizing:border-box}
.slide{position:relative;width:${W}in;height:${H}in;overflow:hidden;page-break-after:always}
</style>` + htmlSlides.join("\n");
fs.writeFileSync("_preview_v4/preview.html", page);

pres.writeFile({ fileName: "../LUAN_VAN_SLIDE_v4.pptx" })
  .then(f => console.log("PPTX ->", f, "| slides:", htmlSlides.length))
  .catch(e => console.error("ERR", e));
