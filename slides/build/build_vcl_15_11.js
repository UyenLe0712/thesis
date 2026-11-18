// Deck VCL 2026 (bản 15/11, viết lại cho dễ hiểu) theo slides/KICH_BAN_VCL_15_11.md.
// 16 slide chính (bốn phần) + 11 slide dự phòng. Khổ 16:9, style kế thừa build_vcl.js:
// thanh tiêu đề chàm, khối xám bo góc, chữ serif Cambria.
// Tiêu đề slide chính và lời nói đọc thẳng từ tệp kịch bản lúc dựng (không chép tay).
// Chữ trên slide theo mục "Trên slide". Slide dự phòng theo danh sách cuối kịch bản,
// số lấy từ kịch bản và paper/vcl2026/main.tex.
// Xuất: ../VCL2026_SLIDE_15_11.pptx
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..", "..");
const KB = fs.readFileSync(path.join(__dirname, "..", "KICH_BAN_VCL_15_11.md"), "utf8");
const FIG_MONEO = path.join(ROOT, "paper", "vcl2026", "hinh", "fig_moneo.png");
const MONEO_R = 690 / 2096;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.author = "Lê Đoàn Phương Uyên";
pres.title = "VCL 2026 - Ngữ liệu quy chiếu cho phần tử giao diện";

const TF = "Cambria", MONO = "Consolas";
const NAVY = "322164", INK = "1A1A1A", BLOCK = "ECEBF0", TEAL = "006666", RED = "B22222";
const GREY = "5A5A66", WHITE = "FFFFFF", LIGHT = "B9B3CC", AMBER = "C77700", SOFT = "A3A3AD";
const MINT = "E6F0EF", FOOTA = "191132", FOOTB = "25194B", FOOTC = "4F417A";
const W = 13.333, H = 7.5, M = 0.6;

// ---------- tiêu đề + lời nói từ kịch bản ----------
function clean(t) {
  return t.replace(/\*/g, "").replace(/`/g, "")
    .split(/\n\s*\n/).map(p => p.replace(/\s*\n\s*/g, " ").trim()).filter(Boolean).join("\n\n");
}
const SAY = {}, TITLE = {};
KB.split(/\n## Slide /).slice(1).forEach(sec => {
  const n = parseInt(sec, 10);
  const t = sec.match(/^\d+ · (.*?) \(~/);
  if (t) TITLE[n] = t[1].trim();
  const m = sec.match(/\*\*Lời nói:\*\*\n([\s\S]*?)(?:\n---|$)/);
  if (m) SAY[n] = clean(m[1]);
});
function QA(code) {
  const re = new RegExp("\\*\\*" + code + "[ ⭐]*\\.\\s*([^\\n]*?)\\*\\*\\n([\\s\\S]*?)(?=\\n\\n)");
  const m = KB.match(re);
  if (!m) throw new Error("không thấy câu " + code);
  return "Dùng cho câu " + code + ": " + m[1].trim() + "\n\n" + clean(m[2]);
}

// ---------- hạ tầng ----------
let s, PAGE = 0, BPAGE = 0;
const TOTAL = 16;
function slide() { s = pres.addSlide(); s.background = { color: WHITE }; }
function text(content, o) {
  const opt = Object.assign({ x: 0, y: 0, w: 4, h: 1, fontSize: 18, color: INK, fontFace: TF, align: "left", valign: "top", margin: 0 }, o);
  if (o.lh) { opt.lineSpacingMultiple = o.lh; delete opt.lh; }
  s.addText(content, opt);
}
function rect(x, y, w, h, fill, o) {
  o = o || {};
  const p = { x, y, w, h, fill: fill === "none" ? { type: "none" } : { color: fill }, line: o.line ? { color: o.line, width: o.lw || 1 } : { type: "none" } };
  if (o.radius) p.rectRadius = o.radius;
  s.addShape(o.shape || (o.radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE), p);
}
function block(x, y, w, h, fill, line) { rect(x, y, w, h, fill || BLOCK, { radius: 0.08, line }); }
function hline(x, y, w, c, lw) { s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || LIGHT, width: lw || 1 } }); }
function arrow(x1, y1, x2, y2, c) {
  const o = { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), line: { color: c || NAVY, width: 2.5, endArrowType: "triangle" } };
  if (x2 < x1) o.flipH = true;
  if (y2 < y1) o.flipV = true;
  s.addShape(pres.shapes.LINE, o);
}
function bar(t) {
  rect(0, 0, W, 0.95, NAVY);
  const fs = t.length > 62 ? 21 : t.length > 52 ? 23 : 26;
  text(t, { x: M, y: 0, w: W - 2 * M, h: 0.95, fontSize: fs, bold: true, color: WHITE, valign: "middle" });
}
function footRow(label) {
  const yy = H - 0.32, hh = 0.32;
  rect(0, yy, 6.0, hh, FOOTA); rect(6.0, yy, 5.3, hh, FOOTB); rect(11.3, yy, W - 11.3, hh, FOOTC);
  const o = { y: yy, h: hh, fontSize: 11, color: WHITE, align: "center", valign: "middle" };
  text("Lê Đoàn Phương Uyên & Nguyễn Hồng Bửu Long", Object.assign({ x: 0, w: 6.0 }, o));
  text("VCL 2026 · HUFLIT · 27/11/2026", Object.assign({ x: 6.0, w: 5.3 }, o));
  text(label, Object.assign({ x: 11.3, w: W - 11.3 }, o));
}
function foot() { PAGE++; footRow(`${PAGE}/${TOTAL}`); }
function footB() { BPAGE++; footRow(`B${BPAGE}`); }
function note(t) { if (t) s.addNotes(t); }
function moneo(x, y, w) { s.addImage({ path: FIG_MONEO, x, y, w, h: w * MONEO_R }); }
function table(x, y, colW, rows, o) {
  o = o || {};
  const totalW = colW.reduce((a, b) => a + b, 0);
  let yy = y;
  rows.forEach(r => {
    const h = r.h || o.rowH || 0.5;
    if (r.fill) rect(x, yy, totalW, h, r.fill);
    let xx = x;
    r.cells.forEach((c, ci) => {
      const cell = (typeof c === "string" || Array.isArray(c)) ? { t: c } : c;
      text(cell.t, { x: xx + 0.1, y: yy, w: colW[ci] - 0.2, h, fontSize: cell.fs || r.fs || o.fs || 17,
        bold: cell.bold != null ? cell.bold : r.bold, color: cell.color || r.color || INK,
        fontFace: cell.mono ? MONO : TF, italic: cell.italic,
        align: cell.align || (o.align && o.align[ci]) || "left", valign: "middle", lh: cell.lh || 1.0 });
      xx += colW[ci];
    });
    if (r.rule !== false) hline(x, yy + h, totalW, r.ruleC || LIGHT, r.ruleW || 1);
    yy += h;
  });
  return yy;
}
// cột dọc: items [{label, v, txt, color}]
function vbars(x, y, w, h, items, vmax, o) {
  o = o || {};
  const n = items.length, slot = w / n, bw = slot * (o.bw || 0.5);
  hline(x, y + h, w, GREY, 1.25);
  items.forEach((it, i) => {
    const bh = h * it.v / vmax, bx = x + i * slot + (slot - bw) / 2;
    rect(bx, y + h - bh, bw, bh, it.color || NAVY);
    text(it.txt, { x: bx - 0.5, y: y + h - bh - 0.75, w: bw + 1.0, h: 0.7, fontSize: o.vfs || 30, bold: true, color: it.color || NAVY, align: "center", valign: "bottom" });
    text(it.label, { x: x + i * slot + 0.05, y: y + h + 0.12, w: slot - 0.1, h: o.lh || 1.0, fontSize: o.lfs || 16, color: INK, align: "center", lh: 1.05 });
  });
}

// ---------- thanh tiến độ + sơ đồ bốn bước thu nhỏ ----------
const PARTS = ["Bài toán", "Tạo nhãn", "Kiểm tra", "Kết luận"];
function main(n, title, part) {
  slide();
  rect(0, 0, W, 0.95, NAVY);
  text(title, { x: M, y: 0, w: 8.6, h: 0.95, fontSize: 24, bold: true, color: WHITE, valign: "middle" });
  const runs = [];
  PARTS.forEach((p, i) => {
    if (i) runs.push({ text: "  ·  ", options: { color: "7A7099" } });
    runs.push({ text: p, options: i === part ? { bold: true, color: WHITE } : { color: "8F87AD" } });
  });
  text(runs, { x: 9.2, y: 0, w: W - 9.2 - 0.25, h: 0.95, fontSize: 13, align: "right", valign: "middle" });
  NOTE_N = n;
}
let NOTE_N = 0;
const STEPS = ["① Ghép dữ liệu", "② Xác định phần tử", "③ Lấy tên", "④ Tìm dấu hiệu phân biệt"];
function miniSteps(active) {
  const y = 1.1, h = 0.5, gap = 0.3, w = (W - 2 * M - 3 * gap) / 4;
  STEPS.forEach((t, i) => {
    const x = M + i * (w + gap), on = active.includes(i + 1);
    rect(x, y, w, h, on ? TEAL : "F2F1F5", { radius: 0.06, line: on ? TEAL : "D5D2DE" });
    text(t, { x, y, w, h, fontSize: 14, bold: on, color: on ? WHITE : "8C8899", align: "center", valign: "middle" });
    if (i < 3) arrow(x + w + 0.03, y + h / 2, x + w + gap - 0.03, y + h / 2, on || active.includes(i + 2) ? TEAL : "C9C5D4");
  });
}
// số lớn + chú thích
function bigNum(v, cap, x, y, w, color, fs) {
  text(v, { x, y, w, h: 1.25, fontSize: fs || 66, bold: true, color: color || TEAL, align: "center", valign: "middle" });
  text(cap, { x, y: y + 1.25, w, h: 0.9, fontSize: 18, color: INK, align: "center", valign: "top", lh: 1.05 });
}

// ══════════ 1 · BÌA ══════════
slide();
rect(0, 0, W, 0.75, NAVY);
text("Hội thảo quốc gia về Ngôn ngữ học tính toán · VCL 2026", { x: 0, y: 0, w: W, h: 0.75, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle" });
rect(0.9, 1.25, W - 1.8, 2.75, NAVY, { radius: 0.1 });
text("Sinh hướng dẫn sử dụng phần mềm từ ảnh chụp màn hình và mục tiêu người dùng:\nxây dựng ngữ liệu quy chiếu tự động\nkhi phần tử giao diện không có tên cụ thể",
  { x: 1.2, y: 1.4, w: W - 2.4, h: 2.45, fontSize: 26, bold: true, color: WHITE, align: "center", valign: "middle", lh: 1.15 });
text("Lê Đoàn Phương Uyên & Nguyễn Hồng Bửu Long", { x: 0.9, y: 4.45, w: W - 1.8, h: 0.5, fontSize: 24, bold: true, align: "center" });
text("Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM", { x: 0.9, y: 5.05, w: W - 1.8, h: 0.45, fontSize: 19, color: GREY, align: "center" });
text("VCL 2026 · HUFLIT · 27/11/2026", { x: 0.9, y: 5.75, w: W - 1.8, h: 0.5, fontSize: 20, bold: true, color: TEAL, align: "center" });
note(SAY[1]); foot();

// ══════════ 2 · MỤC TIÊU ══════════
main(2, "Bài toán: sinh câu hướng dẫn thao tác", 0);
s.addShape(pres.shapes.ROUNDED_RECTANGULAR_CALLOUT, { x: M, y: 1.5, w: 5.9, h: 1.45, fill: { color: BLOCK }, line: { color: SOFT, width: 1 } });
text("“Con ơi, muốn gửi thư thì bấm vào đâu?”", { x: M + 0.3, y: 1.5, w: 5.3, h: 1.45, fontSize: 22, italic: true, valign: "middle" });
s.addShape(pres.shapes.ROUNDED_RECTANGULAR_CALLOUT, { x: M + 0.6, y: 3.85, w: 5.9, h: 1.45, fill: { color: MINT }, line: { color: TEAL, width: 1 }, flipH: true });
text("“Mẹ bấm vào cái biểu tượng ngay trên chữ Gmail.”", { x: M + 0.9, y: 3.85, w: 5.3, h: 1.45, fontSize: 22, italic: true, color: TEAL, valign: "middle" });
{
  const bx = 8.0, bw = 4.73;
  block(bx, 1.3, bw, 1.25);
  text("ảnh màn hình\n+ mục tiêu người dùng", { x: bx + 0.2, y: 1.3, w: bw - 0.4, h: 1.25, fontSize: 20, align: "center", valign: "middle", lh: 1.05 });
  arrow(bx + bw / 2, 2.6, bx + bw / 2, 3.15);
  rect(bx, 3.2, bw, 1.1, NAVY, { radius: 0.08 });
  text("mô hình", { x: bx, y: 3.2, w: bw, h: 1.1, fontSize: 24, bold: true, color: WHITE, align: "center", valign: "middle" });
  arrow(bx + bw / 2, 4.35, bx + bw / 2, 4.9);
  block(bx, 4.95, bw, 1.1, MINT, TEAL);
  text("câu hướng dẫn", { x: bx, y: 4.95, w: bw, h: 1.1, fontSize: 22, bold: true, color: TEAL, align: "center", valign: "middle" });
}
note(SAY[2]); foot();

// ══════════ 3 · NÚT KHÔNG CÓ TÊN ══════════
main(3, "Phần tử giao diện thường không có tên", 0);
moneo(M, 1.65, 7.7);
text("Cả bốn biểu tượng đều không có tên trong cây trợ năng.", { x: M, y: 4.35, w: 7.7, h: 0.5, fontSize: 18, color: GREY, align: "center" });
bigNum("22%", "nút cần bấm không có tên", 8.7, 1.75, 4.03, RED, 84);
hline(M, 5.6, W - 2 * M, LIGHT, 1);
text("Thêm 7,6% trùng tên với phần tử khác: tổng cộng 29,6% số bước.", { x: M, y: 5.7, w: W - 2 * M, h: 0.55, fontSize: 16, italic: true, color: GREY, align: "center", valign: "middle" });
note(SAY[3]); foot();

// ══════════ 4 · CHỈ QUA VẬT BÊN CẠNH ══════════
main(4, "Quy chiếu qua phần tử lân cận", 0);
[["Ảnh tự nhiên", "“con mèo đen bên trái”", "đối tượng thường có danh từ để gọi", NAVY, BLOCK],
 ["Màn hình điện thoại", "“biểu tượng ngay trên chữ Gmail”", "nhiều phần tử không có tên", TEAL, MINT]].forEach((c, i) => {
  const x = M + i * 6.2;
  block(x, 1.3, 5.9, 2.2, c[4]);
  text(c[0], { x: x + 0.3, y: 1.4, w: 5.3, h: 0.5, fontSize: 20, bold: true, color: c[3], align: "center" });
  text(c[1], { x: x + 0.3, y: 1.95, w: 5.3, h: 0.75, fontSize: 23, italic: true, align: "center", valign: "middle" });
  text(c[2], { x: x + 0.3, y: 2.8, w: 5.3, h: 0.5, fontSize: 17, color: GREY, align: "center" });
});
text("1/3", { x: M, y: 3.75, w: 2.4, h: 1.2, fontSize: 64, bold: true, color: TEAL, align: "center", valign: "middle" });
text("câu của người chú thích có từ chỉ vị trí\n(“trên”, “dưới”, “góc phải”…)", { x: M + 2.6, y: 3.75, w: 9.5, h: 1.2, fontSize: 21, valign: "middle", lh: 1.1 });
rect(M, 5.3, W - 2 * M, 0.85, NAVY, { radius: 0.08 });
text([{ text: "Biểu thức quy chiếu: ", options: { bold: true } }, { text: "mô tả giúp người nghe xác định đúng một đối tượng giữa các đối tượng tương tự.", options: {} }],
  { x: M + 0.3, y: 5.3, w: W - 2 * M - 0.6, h: 0.85, fontSize: 19, color: WHITE, align: "center", valign: "middle" });
text("Dale & Reiter, 1995", { x: W - M - 3, y: 6.2, w: 3, h: 0.35, fontSize: 12, italic: true, color: GREY, align: "right" });
note(SAY[4]); foot();

// ══════════ 5 · CẦN DỮ LIỆU ══════════
main(5, "Dữ liệu sẵn có và phần còn thiếu", 0);
block(M, 1.3, W - 2 * M, 1.85);
text([{ text: "AndroidControl ", options: { bold: true, color: NAVY } }, { text: "(Li và cộng sự, 2024): 15.283 chuỗi thao tác thật; mỗi bước có ảnh, toạ độ chạm, câu chỉ dẫn.", options: {} }],
  { x: M + 0.35, y: 1.42, w: W - 2 * M - 0.7, h: 0.75, fontSize: 18.5, valign: "middle" });
text([{ text: "Chưa có: ", options: { bold: true, color: RED } }, { text: "mô tả phần tử cần chạm và dấu hiệu phân biệt nó với phần tử tương tự.", options: {} }],
  { x: M + 0.35, y: 2.2, w: W - 2 * M - 0.7, h: 0.75, fontSize: 20, valign: "middle" });
text("Dàn ý", { x: M, y: 3.5, w: 4, h: 0.5, fontSize: 21, bold: true, color: TEAL });
rect(M, 4.0, W - 2 * M, 2.35, "none", { line: TEAL, lw: 1.5 });
[["1", "Tạo nhãn", "cấu trúc nhãn và quy trình dựng tự động"], ["2", "Kiểm tra", "đối chiếu với câu của người chú thích"], ["3", "Kết luận", "hạn chế và hướng phát triển"]].forEach((c, i) => {
  const yy = 4.15 + i * 0.7;
  text([{ text: c[0] + ".  ", options: { bold: true, color: TEAL } }, { text: c[1], options: { bold: true, color: NAVY } }, { text: ": " + c[2], options: {} }],
    { x: M + 0.4, y: yy, w: W - 2 * M - 0.8, h: 0.65, fontSize: 20, valign: "middle" });
});
note(SAY[5]); foot();

// ══════════ 6 · NHÃN BỐN Ô ══════════
main(6, "Nhãn mô tả bốn ô", 1);
moneo(M, 2.85, 4.0);
text("phần tử cần chạm: biểu tượng Gmail", { x: M, y: 4.25, w: 4.0, h: 0.45, fontSize: 14, italic: true, color: GREY, align: "center" });
table(4.95, 1.35, [2.05, 2.7, 3.03], [
  { cells: ["ô", "ví dụ trên màn Gmail", "nghĩa"], bold: true, color: WHITE, fill: NAVY, h: 0.65 },
  { cells: [{ t: "loại", bold: true }, { t: "icon", mono: true }, "nút, ô nhập, biểu tượng…"], h: 0.95 },
  { cells: [{ t: "tên", bold: true }, "(không có tên)", "chữ hiển thị trên phần tử"], h: 0.95 },
  { cells: [{ t: "vị trí", bold: true }, { t: "111, 903", mono: true }, "điểm chạm, thang 0 đến 1.000"], h: 0.95 },
  { cells: [{ t: "dấu hiệu phân biệt", bold: true, color: WHITE }, { t: "ngay trên chữ “Gmail”", bold: true, color: WHITE }, { t: "phân biệt với phần tử tương tự", bold: true, color: WHITE }], h: 1.15, fill: TEAL, rule: false },
], { fs: 18 });
note(SAY[6]); foot();

// ══════════ 7 · BỐN BƯỚC ══════════
main(7, "Quy trình dựng nhãn", 1);
{
  const subs = ["ghép hai bản phát hành", "hộp bao nhỏ nhất chứa điểm chạm", "cây trợ năng, sau đó OCR", "chuỗi chữ gần nhất làm mốc"];
  const names = ["Ghép dữ liệu", "Xác định phần tử", "Lấy tên", "Tìm dấu hiệu phân biệt"];
  const gap = 0.45, w = (W - 2 * M - 3 * gap) / 4, y = 1.8;
  names.forEach((t, i) => {
    const x = M + i * (w + gap);
    rect(x, y, w, 1.9, i === 3 ? TEAL : NAVY, { radius: 0.1 });
    text("①②③④"[i], { x, y: y + 0.15, w, h: 0.6, fontSize: 30, bold: true, color: WHITE, align: "center", valign: "middle" });
    text(t, { x: x + 0.15, y: y + 0.8, w: w - 0.3, h: 0.95, fontSize: 21, bold: true, color: WHITE, align: "center", valign: "middle", lh: 1.0 });
    text(subs[i], { x: x + 0.05, y: y + 2.05, w: w - 0.1, h: 1.0, fontSize: 17, color: INK, align: "center", lh: 1.05 });
    if (i < 3) arrow(x + w + 0.05, y + 0.95, x + w + gap - 0.05, y + 0.95);
  });
  rect(M, 5.35, W - 2 * M, 0.85, BLOCK, { radius: 0.08 });
  text("Dựng hoàn toàn bằng quy tắc", { x: M, y: 5.35, w: W - 2 * M, h: 0.85, fontSize: 21, bold: true, color: NAVY, align: "center", valign: "middle" });
}
note(SAY[7]); foot();

// ══════════ 8 · BƯỚC 1 ══════════
main(8, "Bước 1. Ghép hai bản phát hành", 1);
miniSteps([1]);
[["Bản 1", "có câu chỉ dẫn và cây trợ năng, thiếu ảnh"], ["Bản 2", "có ảnh, thiếu câu chỉ dẫn"]].forEach((c, i) => {
  const yy = 2.1 + i * 1.05;
  block(M, yy, 6.6, 0.85);
  text([{ text: c[0] + ": ", options: { bold: true, color: NAVY } }, { text: c[1], options: {} }], { x: M + 0.3, y: yy, w: 6.1, h: 0.85, fontSize: 20, valign: "middle" });
});
text("Ghép hai bản để có đủ ba thành phần", { x: M + 0.3, y: 4.3, w: 6.3, h: 0.7, fontSize: 21, bold: true, color: TEAL, valign: "middle" });
vbars(8.3, 2.55, 4.4, 2.55, [
  { label: "ghép đúng", v: 48, txt: "48%", color: TEAL },
  { label: "ghép lệch (đối chứng)", v: 20, txt: "20%", color: SOFT },
], 55, { bw: 0.55, lfs: 17, vfs: 32, lh: 0.5 });
text("tỉ lệ chữ tại điểm chạm xuất hiện trong câu chỉ dẫn", { x: 8.0, y: 5.8, w: 5.0, h: 0.45, fontSize: 15, italic: true, color: GREY, align: "center" });
note(SAY[8]); foot();

// ══════════ 9 · BƯỚC 2 VÀ 3 ══════════
main(9, "Bước 2 và 3. Xác định phần tử và lấy tên", 1);
miniSteps([2, 3]);
block(M, 2.0, 5.4, 3.0);
text("Bước 2", { x: M + 0.3, y: 2.15, w: 4.8, h: 0.5, fontSize: 20, bold: true, color: TEAL });
text("Hộp bao nhỏ nhất chứa điểm chạm", { x: M + 0.3, y: 2.75, w: 4.8, h: 1.8, fontSize: 24, bold: true, color: NAVY, valign: "middle", lh: 1.1 });
arrow(6.1, 3.5, 6.75, 3.5);
block(6.85, 2.0, 5.88, 3.0);
text("Bước 3", { x: 7.15, y: 2.15, w: 5.3, h: 0.5, fontSize: 20, bold: true, color: TEAL });
text("12,6%", { x: 7.0, y: 2.65, w: 2.5, h: 1.0, fontSize: 44, bold: true, color: RED, valign: "middle" });
text("phần tử có tên trong cây trợ năng", { x: 9.45, y: 2.65, w: 3.15, h: 1.0, fontSize: 16, valign: "middle", lh: 1.05 });
text("Bổ sung bằng OCR (nhận dạng chữ trong ảnh)", { x: 7.15, y: 3.85, w: 5.4, h: 0.8, fontSize: 21, bold: true, color: NAVY, valign: "middle" });
rect(M, 5.35, W - 2 * M, 0.9, TEAL, { radius: 0.08 });
text("Tên không xác định được thì để trống", { x: M, y: 5.35, w: W - 2 * M, h: 0.9, fontSize: 24, bold: true, color: WHITE, align: "center", valign: "middle" });
note(SAY[9]); foot();

// ══════════ 10 · BƯỚC 4 ══════════
main(10, "Bước 4. Mỏ neo chữ", 1);
miniSteps([4]);
moneo((W - 10.6) / 2, 1.8, 10.6);
block(M, 5.45, W - 2 * M, 0.95);
text([{ text: "Nhãn: ", options: { color: GREY } }, { text: "ngay trên chữ \"Gmail\"", options: { fontFace: MONO, color: TEAL, bold: true } },
      { text: "        Câu của người chú thích: ", options: { color: GREY } }, { text: "“Click on the gmail option”", options: { color: NAVY, bold: true, italic: true } }],
  { x: M, y: 5.45, w: W - 2 * M, h: 0.95, fontSize: 22, align: "center", valign: "middle" });
note(SAY[10]); foot();

// ══════════ 11 · LÀM LẠI ══════════
main(11, "Bước 4. Hai phiên bản quy tắc", 1);
miniSteps([4]);
[["Bản đầu", "“một trong bảy biểu tượng cùng loại”", "7,3%", GREY, BLOCK],
 ["Bản làm lại", "“ngay trên chữ Gmail”", "75,3%", TEAL, MINT]].forEach((c, i) => {
  const x = i === 0 ? M : 7.5, w = i === 0 ? 5.25 : 5.23;
  block(x, 2.0, w, 4.25, c[4]);
  text(c[0], { x, y: 2.15, w, h: 0.55, fontSize: 24, bold: true, color: c[3], align: "center" });
  text(c[1], { x: x + 0.3, y: 2.75, w: w - 0.6, h: 0.9, fontSize: 21, italic: true, align: "center", valign: "middle", lh: 1.05 });
  text(c[2], { x, y: 3.7, w, h: 1.3, fontSize: i === 0 ? 54 : 70, bold: true, color: c[3], align: "center", valign: "middle" });
  text("dấu hiệu xác định được đúng phần tử", { x, y: 5.1, w, h: 0.6, fontSize: 18, align: "center" });
});
arrow(6.05, 4.3, 7.3, 4.3);
note(SAY[11]); foot();

// ══════════ 12 · KIỂM BẰNG CÂU NGƯỜI VIẾT ══════════
main(12, "Đối chiếu với câu của người chú thích", 2);
vbars(M + 1.0, 1.95, 7.0, 2.85, [
  { label: "tên trong nhãn xuất hiện\ntrong câu của đúng bước đó", v: 53.5, txt: "53,5%", color: TEAL },
  { label: "cùng tên, so với câu\ncủa bước kế tiếp (đối chứng)", v: 7.6, txt: "7,6%", color: SOFT },
], 60, { bw: 0.45, lfs: 17, vfs: 38 });
block(8.95, 1.9, 3.78, 2.9, MINT);
text("Quy trình dựng nhãn không sử dụng câu của người chú thích.", { x: 9.15, y: 1.9, w: 3.38, h: 2.9, fontSize: 19, color: NAVY, valign: "middle", lh: 1.1 });
note(SAY[12]); foot();

// ══════════ 13 · CHỖ CÒN YẾU ══════════
main(13, "Độ phủ theo loại phần tử", 2);
text("Tỉ lệ dấu hiệu xác định được đúng phần tử", { x: M, y: 1.3, w: W - 2 * M, h: 0.55, fontSize: 20, color: GREY });
[["có tên rõ ràng", 80, "80%", TEAL, true], ["không có tên", 67, "67%", NAVY, false], ["chỉ có một ký hiệu\n(ví dụ “Q”, “?”)", 38, "38%", RED, true]].forEach((r, i) => {
  const yy = 2.15 + i * 1.35, bx = 4.6, bwMax = 6.8;
  text(r[0], { x: M, y: yy, w: 3.8, h: 1.0, fontSize: 21, bold: r[4], align: "right", valign: "middle", lh: 1.05 });
  rect(bx, yy + 0.15, bwMax, 0.7, "EEEDF2");
  rect(bx, yy + 0.15, bwMax * r[1] / 100, 0.7, r[3]);
  text(r[2], { x: bx + bwMax * r[1] / 100 + 0.15, y: yy, w: 1.3, h: 1.0, fontSize: r[4] ? 30 : 24, bold: r[4], color: r[3], valign: "middle" });
});
note(SAY[13]); foot();

// ══════════ 14 · HẠN CHẾ ══════════
main(14, "Hạn chế", 3);
[[{ text: "Khoảng ", options: {} }, { text: "1/4", options: { bold: true, color: RED } }, { text: " dấu hiệu chưa xác định được đúng phần tử", options: {} }],
 [{ text: "Chưa đánh giá với người dùng thật", options: {} }]].forEach((c, i) => {
  const yy = 1.7 + i * 1.9;
  block(M, yy, W - 2 * M, 1.5);
  rect(M, yy, 0.14, 1.5, AMBER);
  text(c, { x: M + 0.5, y: yy, w: W - 2 * M - 0.8, h: 1.5, fontSize: 25, valign: "middle" });
});
note(SAY[14]); foot();

// ══════════ 15 · KẾT LUẬN ══════════
main(15, "Kết luận", 3);
[["Bài toán", [{ text: "gần ", options: {} }, { text: "1/3", options: { bold: true, color: TEAL } }, { text: " phần tử cần chạm không có tên hoặc trùng tên, phải quy chiếu qua phần tử lân cận", options: {} }]],
 ["Tạo nhãn", [{ text: "tự động ", options: {} }, { text: "41.099 + 4.448", options: { bold: true, color: TEAL } }, { text: " nhãn bốn ô; dấu hiệu phân biệt ", options: {} }, { text: "7,3% → 75,3%", options: { bold: true, color: TEAL } }]],
 ["Kiểm tra", [{ text: "53,5%", options: { bold: true, color: TEAL } }, { text: " tên trùng câu của người chú thích, so với ", options: {} }, { text: "7,6%", options: { bold: true, color: GREY } }, { text: " ở đối chứng", options: {} }]]].forEach((c, i) => {
  const yy = 1.35 + i * 1.5;
  block(M, yy, W - 2 * M, 1.25);
  rect(M, yy, 2.2, 1.25, NAVY, { radius: 0.08 });
  text(c[0], { x: M, y: yy, w: 2.2, h: 1.25, fontSize: 21, bold: true, color: WHITE, align: "center", valign: "middle" });
  text(c[1], { x: M + 2.45, y: yy, w: W - 2 * M - 2.7, h: 1.25, fontSize: 19.5, valign: "middle", lh: 1.05 });
});
text("Kết quả huấn luyện mô hình: bài đồng hành.", { x: M, y: 5.95, w: W - 2 * M, h: 0.5, fontSize: 17, italic: true, color: GREY, align: "center" });
note(SAY[15]); foot();

// ══════════ 16 · CẢM ƠN ══════════
slide();
rect(0, 0, W, H - 0.32, NAVY);
text("Cảm ơn quý thầy cô và các bạn đã lắng nghe", { x: M, y: 2.2, w: W - 2 * M, h: 1.3, fontSize: 38, bold: true, color: WHITE, align: "center", valign: "middle" });
text("24C15039@student.hcmus.edu.vn", { x: M, y: 3.9, w: W - 2 * M, h: 0.6, fontSize: 22, fontFace: MONO, color: LIGHT, align: "center", valign: "middle" });
note(SAY[16]); foot();

// ══════════════════ DỰ PHÒNG ══════════════════
function backup(t) { slide(); bar("Dự phòng · " + t); }

// B1 · hai bản phát hành
backup("Hai bản phát hành và cách kiểm ghép đúng");
table(M, 1.35, [4.0, 2.6, 1.9], [
  { cells: ["bản phát hành", "có", "thiếu"], bold: true, color: WHITE, fill: NAVY, h: 0.55 },
  { cells: [{ t: "HarrytheOrange/\nparsed_AndroidControl", mono: true, fs: 14 }, "câu chỉ dẫn, cây trợ năng", "ảnh"], h: 1.0 },
  { cells: [{ t: "ckg/AndroidControl\nParsedWithImages-20k", mono: true, fs: 14 }, "ảnh", "câu chỉ dẫn theo bước"], h: 1.0, rule: false },
], { fs: 17 });
block(M, 4.2, 8.5, 0.8);
text([{ text: "ghép theo ", options: {} }, { text: "(episode_id, step_id)", options: { fontFace: MONO, bold: true, color: NAVY } }], { x: M, y: 4.2, w: 8.5, h: 0.8, fontSize: 19, align: "center", valign: "middle" });
vbars(9.45, 1.85, 3.3, 3.0, [
  { label: "ghép đúng\n400 bước", v: 48.3, txt: "48,3%", color: TEAL },
  { label: "ghép lệch\n311 bước", v: 19.6, txt: "19,6%", color: SOFT },
], 55, { bw: 0.6, lfs: 15, vfs: 26 });
text("KTC95: [43,4; 53,1] · [15,6; 24,4]", { x: 9.2, y: 5.95, w: 3.8, h: 0.45, fontSize: 14, italic: true, color: GREY, align: "center" });
note(QA("C5")); footB();

// B2 · hai bộ lọc
backup("Hai bộ lọc");
[["Bộ lọc nhãn trợ năng", "loại tên kiểu mã nguồn, chuỗi số dài, “unlabeled”…", "14,7%", "nhãn bị loại trên mẫu thử 1.074 nhãn\n3,9% ứng viên trên toàn bộ"],
 ["Bộ lọc hình học", "chỉ lấy tên OCR khi hộp < 25% màn\nvd. hộp 95% màn: “THEFELLOWSHIPOF THE RING”", "2,2%", "số bước bị tác động"]].forEach((c, i) => {
  const x = M + i * 6.2;
  block(x, 1.4, 5.9, 4.9);
  text(c[0], { x: x + 0.3, y: 1.6, w: 5.3, h: 0.55, fontSize: 23, bold: true, color: NAVY });
  text(c[1], { x: x + 0.3, y: 2.3, w: 5.3, h: 1.6, fontSize: 17, lh: 1.15 });
  text(c[2], { x: x + 0.3, y: 4.1, w: 2.4, h: 1.4, fontSize: 46, bold: true, color: TEAL, valign: "middle" });
  text(c[3], { x: x + 2.75, y: 4.1, w: 2.95, h: 1.4, fontSize: 16, color: GREY, valign: "middle", lh: 1.1 });
});
note(QA("B3")); footB();

// B3 · tỉ số 3,2 lần
backup("Truy nguyên tỉ số 3,2 lần");
[["72", "nhãn hai nguồn\ncho hai chuỗi khác nhau"], ["−32", "chuỗi đã nằm sẵn\ntrong mục tiêu"], ["40", "nhãn còn lại"]].forEach((c, i) => {
  const x = M + i * 3.0;
  block(x, 1.5, 2.6, 2.2);
  text(c[0], { x, y: 1.6, w: 2.6, h: 1.0, fontSize: 40, bold: true, color: NAVY, align: "center", valign: "middle" });
  text(c[1], { x: x + 0.1, y: 2.6, w: 2.4, h: 1.0, fontSize: 15, align: "center", lh: 1.05 });
  if (i < 2) arrow(x + 2.62, 2.6, x + 2.98, 2.6);
});
table(9.6, 1.5, [2.2, 0.93], [
  { cells: ["khớp OCR", "12"], h: 0.7 }, { cells: ["khớp cây trợ năng", "3"], h: 0.7 }, { cells: ["không bên nào", "25"], h: 0.7, rule: false },
], { fs: 18, align: ["left", "right"] });
block(M, 4.3, W - 2 * M, 1.9, MINT);
text("11/12 ca nghiêng về OCR: nhãn trợ năng ở đó không dùng được.\nKhi cả hai nguồn dùng được: OCR 1 ca, cây trợ năng 3 ca.",
  { x: M + 0.3, y: 4.3, w: W - 2 * M - 0.6, h: 1.9, fontSize: 20, valign: "middle", lh: 1.25 });
note(QA("B2")); footB();

// B4 · sáu chỉ số
backup("Mẫu thử và toàn bộ ngữ liệu");
table(M + 0.9, 1.35, [5.2, 2.6, 2.6], [
  { cells: ["chỉ số", { t: "toàn bộ (41.099)", align: "right" }, { t: "mẫu thử (1.074)", align: "right" }], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: ["tên rõ ràng", "73,6%", "73,8%"], h: 0.62 },
  { cells: ["chỉ có ký hiệu, không có chữ", "4,4%", "2,8%"], h: 0.62 },
  { cells: ["không có tên", "22,0%", "23,4%"], h: 0.62 },
  { cells: ["vai trò rõ ràng", "75,8%", "76,0%"], h: 0.62 },
  { cells: ["trùng tên trên cùng màn", "7,6%", "7,0%"], h: 0.62 },
  { cells: ["có phần tử cùng vai trò để so", "91,6%", "92,6%"], h: 0.62 },
], { fs: 19, align: ["left", "right", "right"] });
text("Sáu chỉ số lệch không quá 1,6 điểm phần trăm; mẫu thử nhỏ hơn 38 lần.", { x: M, y: 6.0, w: W - 2 * M, h: 0.55, fontSize: 18, italic: true, color: GREY, align: "center" });
note(QA("C4")); footB();

// B5 · bốn nhãn thật
backup("Bốn nhãn thật và câu của người chú thích");
table(M, 1.35, [8.2, 3.93], [
  { cells: ["nhãn tự động", "câu của người chú thích"], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: [{ t: "tappable text | Search here | <point>440,91</point> | just above the text \"Coffee\"", mono: true, fs: 14 }, { t: "Click on the search bar", italic: true }], h: 1.0 },
  { cells: [{ t: "icon | (no name) | <point>256,524</point> | just above the text \"Leaf\"", mono: true, fs: 14 }, { t: "Choose the leaf option", italic: true }], h: 1.0 },
  { cells: [{ t: "icon | Q | <point>920,899</point> | shares a name with 1 other elements on screen", mono: true, fs: 14 }, { t: "click on the search icon", italic: true }], h: 1.0 },
  { cells: [{ t: "icon | (no name) | <point>920,904</point> | many elements of the same kind on screen", mono: true, fs: 14 }, { t: "Click on the Right arrow key", italic: true }], h: 1.0, rule: false },
], { fs: 18 });
text("Hai dòng đầu chỉ ra được nút; hai dòng sau chỉ báo có nút giống nó.", { x: M, y: 5.95, w: W - 2 * M, h: 0.6, fontSize: 17, italic: true, color: GREY, align: "center" });
footB();

// B6 · bảng dấu hiệu đầy đủ
backup("Loại dấu hiệu phân biệt theo tầng tên");
table(M, 1.35, [3.4, 1.55, 1.9, 1.7, 2.0, 1.58], [
  { cells: ["tầng tên", "n", "mỏ neo chữ", "duy nhất", "nêu trùng tên", "chỉ đếm"], bold: true, color: WHITE, fill: NAVY, h: 0.65 },
  { cells: ["tên rõ ràng", "30.252", "72,2%", "7,9%", "1,7%", "18,2%"], h: 0.7 },
  { cells: ["chỉ có ký hiệu", "1.809", "32,7%", "4,8%", "31,3%", "31,2%"], h: 0.7 },
  { cells: ["không có tên", "9.038", "57,5%", "9,2%", "-", "33,3%"], h: 0.7 },
  { cells: [{ t: "toàn bộ", bold: true }, { t: "41.099", bold: true }, { t: "67,2%", bold: true }, { t: "8,1%", bold: true }, { t: "2,6%", bold: true }, { t: "22,1%", bold: true }], h: 0.7, rule: false },
], { fs: 19, align: ["left", "right", "right", "right", "right", "right"] });
rect(M + 4.95, 1.35, 3.6, 3.45, "none", { line: TEAL, lw: 2 });
text("Hai cột viền xanh chỉ ra được nút. Cộng lại: 80,1% · 37,5% · 66,7% · 75,3% (theo thứ tự hàng).",
  { x: M, y: 5.1, w: W - 2 * M, h: 0.9, fontSize: 18, color: TEAL, align: "center", lh: 1.1 });
note(QA("C3")); footB();

// B7 · công trình liên quan
backup("Vị trí so với các công trình liên quan");
table(M, 1.35, [4.3, 7.83], [
  { cells: ["công trình", "khác bài này ở đâu"], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: [{ t: "Dale & Reiter 1995 · Dale & Haddock 1991\nMao 2016 · Luo 2017 · Yu 2017", lh: 1.1 }, "ảnh tự nhiên"], h: 1.2 },
  { cells: [{ t: "Widget Captioning", bold: true }, "nhãn do người viết, một widget tách rời"], h: 1.0 },
  { cells: [{ t: "AndroidControl", bold: true }, "câu chỉ dẫn là đầu vào; ở đây là đầu ra"], h: 1.0, rule: false },
], { fs: 19 });
note(QA("A2")); footB();

// B8 · quy mô chi tiết
backup("Quy mô và cách chia tập");
table(M, 1.35, [5.33, 3.4, 3.4], [
  { cells: ["", { t: "huấn luyện", align: "right" }, { t: "kiểm tra", align: "right" }], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: ["số bước", "64.567", "6.958"], h: 0.65 },
  { cells: ["bước chạm", "41.191", "4.463"], h: 0.65 },
  { cells: ["số tác vụ", "12.895", "1.432"], h: 0.65, rule: false },
], { fs: 20, align: ["left", "right", "right"] });
text("Ba điều cách chia không bảo đảm", { x: M, y: 4.1, w: W - 2 * M, h: 0.5, fontSize: 19, bold: true, color: AMBER });
["cách diễn đạt lặp lại", "95,6% ứng dụng có ở tập huấn luyện", "55% số bước không gán được ứng dụng"].forEach((t, i) => {
  const xx = M + i * 4.1;
  block(xx, 4.7, 3.93, 1.3);
  rect(xx, 4.7, 0.12, 1.3, AMBER);
  text(t, { x: xx + 0.3, y: 4.7, w: 3.5, h: 1.3, fontSize: 18, valign: "middle", lh: 1.1 });
});
note(QA("D4")); footB();


// B9 · một bản ghi
backup("Một bản ghi GUIRefCorpus có gì");
text("Mỗi dòng JSON ứng với một bước chạm", { x: M, y: 1.2, w: W - 2 * M, h: 0.55, fontSize: 21, bold: true, color: NAVY });
[["nhãn", "dòng bốn ô đã ghép, và riêng từng ô"],
 ["tên", "tên, nguồn của tên, tầng tên"],
 ["vị trí", "toạ độ đã chuẩn hoá, hộp bao"],
 ["cờ", "trùng tên, trùng vai trò trên cùng màn"],
 ["đối chứng", "nhãn của phần tử hàng xóm"],
 ["khoá", "(episode_id, step_id) nối về bước gốc"]].forEach((c, i) => {
  const col = i % 2, row = Math.floor(i / 2), x = M + col * 6.15, yy = 1.95 + row * 1.05;
  block(x, yy, 5.95, 0.88);
  text(c[0], { x: x + 0.2, y: yy, w: 1.6, h: 0.88, fontSize: 19, bold: true, color: TEAL, valign: "middle" });
  text(c[1], { x: x + 1.85, y: yy, w: 3.95, h: 0.88, fontSize: 17, valign: "middle" });
});
block(M, 5.25, W - 2 * M, 0.7);
text("<desc>icon | (no name) | <point>111,903</point> | just above the text \"Gmail\"</desc>", { x: M, y: 5.25, w: W - 2 * M, h: 0.7, fontSize: 17, fontFace: MONO, color: NAVY, align: "center", valign: "middle" });
text("Ảnh không đi kèm: AndroidControl đã phát hành ảnh theo CC0.", { x: M, y: 6.15, w: W - 2 * M, h: 0.5, fontSize: 16, italic: true, color: GREY, align: "center" });
note(QA("D3")); footB();


// B10 · người và máy chọn cùng chiến lược
backup("Chiến lược quy chiếu: người chú thích và quy trình");
[["32,5%", "câu của người chú thích có từ chỉ vị trí", NAVY], ["67,2%", "dấu hiệu của quy trình là mỏ neo chữ", TEAL],
 ["55,6%", "số bước có nút cạnh tranh trong khoảng 80 đến 350 px", GREY], ["91,6%", "số bước có nút cùng vai trò (trung vị 8)", GREY]].forEach((c, i) => {
  const x = M + (i % 2) * 6.2, yy = 1.4 + Math.floor(i / 2) * 2.35;
  block(x, yy, 5.9, 2.05, i < 2 ? MINT : BLOCK);
  text(c[0], { x, y: yy + 0.15, w: 5.9, h: 1.0, fontSize: 44, bold: true, color: c[2], align: "center", valign: "middle" });
  text(c[1], { x: x + 0.3, y: yy + 1.2, w: 5.3, h: 0.7, fontSize: 18, align: "center", valign: "middle" });
});
note(QA("D5")); footB();

// B11 · chuỗi mục tiêu bị cắt
backup("Chuỗi mục tiêu bị cắt từ nguồn");
block(M, 1.4, W - 2 * M, 1.2);
text("...look for Calvin Kle", { x: M, y: 1.4, w: W - 2 * M, h: 1.2, fontSize: 32, fontFace: MONO, color: RED, align: "center", valign: "middle" });
[["99,4%", "không có dấu câu cuối"], ["≥ 71,3%", "cắt giữa từ"]].forEach((c, i) => {
  const x = M + 0.8 + i * 5.6;
  text(c[0], { x, y: 3.0, w: 4.9, h: 1.2, fontSize: 52, bold: true, color: NAVY, align: "center", valign: "middle" });
  text(c[1], { x, y: 4.2, w: 4.9, h: 0.6, fontSize: 20, align: "center" });
});
text("Đo trên 1.424 mục tiêu khác nhau của tập kiểm tra.", { x: M, y: 5.5, w: W - 2 * M, h: 0.5, fontSize: 17, italic: true, color: GREY, align: "center" });
footB();


pres.writeFile({ fileName: path.join(__dirname, "..", "VCL2026_SLIDE_15_11.pptx") }).then(() => {
  console.log("Xong: VCL2026_SLIDE_15_11.pptx | chinh " + PAGE + " | du phong " + BPAGE + " | loi noi " + Object.keys(SAY).length);
});
