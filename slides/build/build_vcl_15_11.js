// Deck VCL 2026 (bản 15/11) theo slides/KICH_BAN_VCL_15_11.md.
// 17 slide chính + 6 slide dự phòng. Khổ 16:9, style kế thừa build_vcl.js:
// thanh tiêu đề chàm, khối xám bo góc, chữ serif Cambria.
// Chữ trên slide lấy từ mục "Trên slide" của kịch bản; lời nói lấy NGUYÊN từ mục "Lời nói"
// (đọc thẳng tệp kịch bản lúc dựng, không chép tay). Slide dự phòng lấy số từ paper/vcl2026/main.tex.
// Xuất: ../VCL2026_SLIDE_15_11.pptx
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..", "..");
const KB = fs.readFileSync(path.join(__dirname, "..", "KICH_BAN_VCL_15_11.md"), "utf8");
const FIG_MONEO = path.join(ROOT, "paper", "vcl2026", "hinh", "fig_moneo.png");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.author = "Lê Đoàn Phương Uyên";
pres.title = "VCL 2026 - Ngữ liệu quy chiếu cho phần tử giao diện";

const TF = "Cambria", MONO = "Consolas";
const NAVY = "322164", INK = "1A1A1A", BLOCK = "ECEBF0", TEAL = "006666", RED = "B22222";
const GREY = "5A5A66", WHITE = "FFFFFF", LIGHT = "B9B3CC", AMBER = "C77700";
const FOOTA = "191132", FOOTB = "25194B", FOOTC = "4F417A";
const W = 13.333, H = 7.5, M = 0.6;

// ---------- lời nói từ kịch bản ----------
function clean(t) {
  return t.replace(/\*\*/g, "").replace(/`/g, "")
    .split(/\n\s*\n/).map(p => p.replace(/\s*\n\s*/g, " ").trim()).filter(Boolean).join("\n\n");
}
const SAY = {};
KB.split(/\n## Slide /).slice(1).forEach(sec => {
  const n = parseInt(sec, 10);
  const m = sec.match(/\*\*Lời nói:\*\*\n([\s\S]*?)(?:\n---|$)/);
  if (m) SAY[n] = clean(m[1]);
});
// câu trả lời hỏi đáp, dùng làm ghi chú cho slide dự phòng
function QA(code) {
  const re = new RegExp("\\*\\*" + code + "[ ⭐]*\\.\\s*([^\\n]*?)\\*\\*\\n([\\s\\S]*?)(?=\\n\\n)");
  const m = KB.match(re);
  if (!m) throw new Error("không thấy câu " + code);
  return "Dùng cho câu " + code + ": " + m[1].trim() + "\n\n" + clean(m[2]);
}

// ---------- hạ tầng ----------
let s, PAGE = 0, BPAGE = 0;
const TOTAL = 17;
function slide() { s = pres.addSlide(); s.background = { color: WHITE }; }
function text(content, o) {
  const opt = Object.assign({ x: 0, y: 0, w: 4, h: 1, fontSize: 18, color: INK, fontFace: TF, align: "left", valign: "top", margin: 0 }, o);
  if (o.lh) { opt.lineSpacingMultiple = o.lh; delete opt.lh; }
  s.addText(content, opt);
}
function rect(x, y, w, h, fill, o) {
  o = o || {};
  const p = { x, y, w, h, fill: fill === "none" ? { type: "none" } : { color: fill }, line: o.line ? { color: o.line, width: o.lw || 1, dashType: o.dash || "solid" } : { type: "none" } };
  if (o.radius) p.rectRadius = o.radius;
  s.addShape(o.radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, p);
}
function block(x, y, w, h, fill) { rect(x, y, w, h, fill || BLOCK, { radius: 0.08 }); }
function hline(x, y, w, c, lw) { s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || LIGHT, width: lw || 1 } }); }
function arrowR(x, y, w, c) { s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || NAVY, width: 2.5, endArrowType: "triangle" } }); }
function bar(t) {
  rect(0, 0, W, 0.9, NAVY);
  text(t, { x: M, y: 0, w: W - 2 * M, h: 0.9, fontSize: 26, bold: true, color: WHITE, valign: "middle" });
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
function note(t) { s.addNotes(t); }
// bảng tự vẽ
function table(x, y, colW, rows, o) {
  o = o || {};
  const totalW = colW.reduce((a, b) => a + b, 0);
  let yy = y;
  rows.forEach((r, ri) => {
    const h = r.h || o.rowH || 0.5;
    if (r.fill) rect(x, yy, totalW, h, r.fill);
    let xx = x;
    r.cells.forEach((c, ci) => {
      const cell = (typeof c === "string" || Array.isArray(c)) ? { t: c } : c;
      text(cell.t, { x: xx + 0.08, y: yy, w: colW[ci] - 0.16, h, fontSize: cell.fs || r.fs || o.fs || 17,
        bold: cell.bold != null ? cell.bold : r.bold, color: cell.color || r.color || INK,
        fontFace: cell.mono ? MONO : TF, italic: cell.italic,
        align: cell.align || (o.align && o.align[ci]) || "left", valign: "middle" });
      xx += colW[ci];
    });
    if (r.rule !== false) hline(x, yy + h, totalW, r.ruleC || LIGHT, r.ruleW || 1);
    yy += h;
  });
  return yy;
}
// cột dọc tự vẽ: items [{label, v, txt, color}], trục 0..vmax
function vbars(x, y, w, h, items, vmax, o) {
  o = o || {};
  const n = items.length, slot = w / n, bw = slot * (o.bw || 0.5);
  hline(x, y + h, w, GREY, 1.25);
  items.forEach((it, i) => {
    const bh = h * it.v / vmax, bx = x + i * slot + (slot - bw) / 2;
    rect(bx, y + h - bh, bw, bh, it.color || NAVY);
    text(it.txt, { x: bx - 0.4, y: y + h - bh - 0.6, w: bw + 0.8, h: 0.55, fontSize: o.vfs || 26, bold: true, color: it.color || NAVY, align: "center", valign: "bottom" });
    text(it.label, { x: x + i * slot + 0.05, y: y + h + 0.1, w: slot - 0.1, h: o.lh || 0.9, fontSize: o.lfs || 15, color: INK, align: "center", lh: 1.05 });
  });
}

// ══════════ 1 · BÌA ══════════
slide();
rect(0, 0, W, 0.75, NAVY);
text("Hội thảo quốc gia về Ngôn ngữ học tính toán · VCL 2026", { x: 0, y: 0, w: W, h: 0.75, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle" });
rect(0.9, 1.25, W - 1.8, 2.75, NAVY, { radius: 0.1 });
text("Sinh hướng dẫn sử dụng phần mềm từ ảnh chụp màn hình và mục tiêu người dùng", { x: 1.2, y: 1.45, w: W - 2.4, h: 1.15, fontSize: 30, bold: true, color: WHITE, align: "center", valign: "middle", lh: 1.05 });
text("Xây dựng ngữ liệu quy chiếu tự động\nkhi phần tử giao diện không có tên cụ thể", { x: 1.2, y: 2.65, w: W - 2.4, h: 1.15, fontSize: 24, color: WHITE, align: "center", valign: "middle", lh: 1.1 });
text("Lê Đoàn Phương Uyên & Nguyễn Hồng Bửu Long", { x: 0.9, y: 4.45, w: W - 1.8, h: 0.5, fontSize: 24, bold: true, align: "center" });
text("Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM", { x: 0.9, y: 5.05, w: W - 1.8, h: 0.45, fontSize: 19, color: GREY, align: "center" });
text("VCL 2026 · HUFLIT · 27/11/2026", { x: 0.9, y: 5.75, w: W - 1.8, h: 0.5, fontSize: 20, bold: true, color: TEAL, align: "center" });
note(SAY[1]); foot();

// ══════════ 2 · BÀI TOÁN QUA MỘT VÍ DỤ ══════════
slide();
bar("Bài toán: từ ảnh màn hình tới một câu cho người đọc");
// ảnh mỏ neo, tỉ lệ 2096x690
{ const iw = 6.4, ih = iw * 690 / 2096; s.addImage({ path: FIG_MONEO, x: M, y: 2.35, w: iw, h: ih }); }
block(7.45, 1.5, 5.3, 1.65);
text("Đầu vào", { x: 7.75, y: 1.65, w: 4.8, h: 0.45, fontSize: 20, bold: true, color: TEAL });
text("ảnh màn hình + mục tiêu của người dùng", { x: 7.75, y: 2.15, w: 4.8, h: 0.8, fontSize: 20 });
block(7.45, 3.45, 5.3, 2.05);
text("Đầu ra: một câu", { x: 7.75, y: 3.6, w: 4.8, h: 0.45, fontSize: 20, bold: true, color: RED });
text("“Chạm vào biểu tượng bút chì ở góc trên bên phải của ghi chú”", { x: 7.75, y: 4.1, w: 4.8, h: 1.25, fontSize: 20, italic: true, lh: 1.05 });
hline(M, 6.1, W - 2 * M, LIGHT, 1);
text([{ text: "Tác tử giao diện: ", options: { bold: true, color: GREY } }, { text: "câu → toạ độ.      ", options: { color: GREY } },
      { text: "Bài này: ", options: { bold: true, color: NAVY } }, { text: "ảnh + mục tiêu → câu cho người đọc.", options: { color: NAVY } }],
  { x: M, y: 6.25, w: W - 2 * M, h: 0.6, fontSize: 18, align: "center", valign: "middle" });
note(SAY[2]); foot();

// ══════════ 3 · PHẦN TỬ KHÔNG CÓ TÊN ══════════
slide();
bar("Phần tử giao diện thường không có tên");
[["12,6%", "phần tử có nhãn văn bản", "đo trên 120 màn ngẫu nhiên;\n22/120 màn không có phần tử nào có tên", TEAL],
 ["22,0%", "phần tử cần chạm\nkhông có tên", "", RED],
 ["7,6%", "phần tử cần chạm trùng tên\nvới phần tử khác", "", RED]].forEach((c, i) => {
  const x = M + i * 4.1;
  block(x, 1.4, 3.85, 3.6);
  text(c[0], { x, y: 1.6, w: 3.85, h: 1.2, fontSize: 54, bold: true, color: c[3], align: "center", valign: "middle" });
  text(c[1], { x: x + 0.2, y: 2.9, w: 3.45, h: 0.9, fontSize: 20, bold: true, color: NAVY, align: "center", lh: 1.05 });
  if (c[2]) text(c[2], { x: x + 0.2, y: 3.95, w: 3.45, h: 0.9, fontSize: 14, italic: true, color: GREY, align: "center", lh: 1.05 });
});
rect(M, 5.45, W - 2 * M, 0.95, NAVY, { radius: 0.08 });
text("Gộp lại: 29,6% số bước, gần một phần ba.", { x: M, y: 5.45, w: W - 2 * M, h: 0.95, fontSize: 26, bold: true, color: WHITE, align: "center", valign: "middle" });
note(SAY[3]); foot();

// ══════════ 4 · VÌ SAO PHẢI CÓ DỮ LIỆU RIÊNG ══════════
slide();
bar("Miền giao diện cần dữ liệu riêng");
block(M, 1.35, 5.85, 2.75); block(6.88, 1.35, 5.85, 2.75, "E6F0EF");
text("Sinh biểu thức quy chiếu", { x: M + 0.3, y: 1.5, w: 5.3, h: 0.5, fontSize: 21, bold: true, color: NAVY });
text("Mao 2016 · Luo 2017 · Yu 2017", { x: M + 0.3, y: 2.0, w: 5.3, h: 0.4, fontSize: 15, italic: true, color: GREY });
text("Ảnh tự nhiên, đối tượng có danh từ.\nQuan hệ chỉ là phương án bổ sung.", { x: M + 0.3, y: 2.55, w: 5.3, h: 1.3, fontSize: 19, lh: 1.15 });
text("Miền giao diện", { x: 7.18, y: 1.5, w: 5.3, h: 0.5, fontSize: 21, bold: true, color: TEAL });
text("22% không có tên.\nQuan hệ với chữ lân cận thành phương tiện chính.", { x: 7.18, y: 2.55, w: 5.3, h: 1.3, fontSize: 19, lh: 1.15 });
table(M, 4.45, [3.6, 8.53], [
  { cells: [{ t: "Widget Captioning", bold: true }, "nhãn do người viết, mô tả một widget tách rời"], h: 0.55 },
  { cells: [{ t: "AndroidControl", bold: true }, "câu chỉ dẫn là đầu vào"], h: 0.55 },
  { cells: [{ t: "Bài này", bold: true, color: RED }, { t: "câu chỉ dẫn là đầu ra", bold: true, color: RED }], h: 0.55, rule: false },
], { fs: 18 });
note(SAY[4]); foot();

// ══════════ 5 · GHÉP HAI BẢN PHÁT HÀNH ══════════
slide();
bar("Ghép hai bản phát hành, và cách kiểm ghép đúng");
table(M, 1.45, [4.6, 1.85, 1.6], [
  { cells: ["bản phát hành", "có", "thiếu"], bold: true, color: WHITE, fill: NAVY, h: 0.5 },
  { cells: [{ t: "HarrytheOrange/\nparsed_AndroidControl", mono: true, fs: 14 }, "câu chỉ dẫn, cây trợ năng", "ảnh"], h: 1.0 },
  { cells: [{ t: "ckg/AndroidControl\nParsedWithImages-20k", mono: true, fs: 14 }, "ảnh", "câu chỉ dẫn theo bước"], h: 1.0 },
], { fs: 16 });
block(M, 4.35, 8.05, 0.8);
text([{ text: "ghép theo ", options: {} }, { text: "(episode_id, step_id)", options: { fontFace: MONO, bold: true, color: NAVY } }], { x: M, y: 4.35, w: 8.05, h: 0.8, fontSize: 19, align: "center", valign: "middle" });
vbars(9.2, 1.9, 3.5, 3.3, [
  { label: "ghép đúng", v: 48.3, txt: "48,3%", color: TEAL },
  { label: "cố ý ghép lệch", v: 19.6, txt: "19,6%", color: "9A94AE" },
], 55, { bw: 0.6, lfs: 16, vfs: 28 });
note(SAY[5]); foot();

// ══════════ 6 · OCR ══════════
slide();
bar("Cây trợ năng không đủ, nên phải đọc chữ bằng OCR");
const t6 = [
  ["86", "phần tử trên một màn (trung vị),\nchỉ 12,6% có tên"],
  ["100%", "ảnh qua OCR (RapidOCR, CPU):\n64.567 bản ghi huấn luyện, 6.958 kiểm tra"],
  ["1 : 2,7", "tên lấy được: 8.581 từ cây trợ năng,\n23.480 từ OCR"],
];
t6.forEach((c, i) => {
  const x = M + i * 4.1;
  block(x, 1.4, 3.85, 3.4);
  text(c[0], { x, y: 1.6, w: 3.85, h: 1.2, fontSize: 50, bold: true, color: i === 2 ? TEAL : NAVY, align: "center", valign: "middle" });
  text(c[1], { x: x + 0.2, y: 3.0, w: 3.45, h: 1.5, fontSize: 17, align: "center", lh: 1.1 });
});
rect(M, 5.3, W - 2 * M, 1.0, TEAL, { radius: 0.08 });
text("Nguyên tắc: để trống còn hơn ghi sai", { x: M, y: 5.3, w: W - 2 * M, h: 1.0, fontSize: 26, bold: true, color: WHITE, align: "center", valign: "middle" });
note(SAY[6]); foot();

// ══════════ 7 · NHÃN BỐN Ô ══════════
slide();
bar("Nhãn bốn ô");
["vai trò", "tên", "toạ độ", "dấu hiệu phân biệt"].forEach((t, i) => {
  const ws = [2.4, 2.4, 2.4, 4.3], xs = [M, M + 2.55, M + 5.1, M + 7.65];
  rect(xs[i], 1.55, ws[i], 1.3, i === 3 ? TEAL : NAVY, { radius: 0.08 });
  text(t, { x: xs[i], y: 1.55, w: ws[i], h: 1.3, fontSize: 26, bold: true, color: WHITE, align: "center", valign: "middle" });
});
block(M, 3.4, W - 2 * M, 1.4);
text("<desc>tappable text | Search here | <point>440,91</point> | just above the text \"Coffee\"</desc>",
  { x: M + 0.3, y: 3.4, w: W - 2 * M - 0.6, h: 1.4, fontSize: 19, fontFace: MONO, color: NAVY, align: "center", valign: "middle" });
text("Chỉ dựng cho bước chạm.\nPhần tử cần chạm = hộp bao nhỏ nhất chứa điểm chạm.", { x: M, y: 5.2, w: W - 2 * M, h: 1.1, fontSize: 19, color: GREY, align: "center", lh: 1.15 });
note(SAY[7]); foot();

// ══════════ 8 · MỎ NEO CHỮ ══════════
slide();
bar("Ví dụ thật: mỏ neo chữ");
{ const iw = 11.0, ih = iw * 690 / 2096; s.addImage({ path: FIG_MONEO, x: (W - iw) / 2, y: 1.15, w: iw, h: ih }); }
block(M, 4.95, W - 2 * M, 0.8);
text("<desc>icon | (no name) | <point>111,903</point> | just above the text \"Gmail\"</desc>",
  { x: M, y: 4.95, w: W - 2 * M, h: 0.8, fontSize: 19, fontFace: MONO, color: NAVY, align: "center", valign: "middle" });
text([{ text: "Câu của người chú thích: ", options: { bold: true } }, { text: "“Click on the gmail option”", options: { italic: true, color: RED } }],
  { x: M, y: 5.95, w: W - 2 * M, h: 0.6, fontSize: 21, align: "center", valign: "middle" });
note(SAY[8]); foot();

// ══════════ 9 · HAI BỘ LỌC ══════════
slide();
bar("Hai bộ lọc, thêm vào sau khi thấy nhãn nhiễu");
[["Bộ lọc nhãn trợ năng", "Loại tên kiểu mã nguồn, chuỗi số dài,\n“No label specified”, “unlabeled”…", "14,7%", "nhãn bị loại\n(mẫu thử 1.074 nhãn)"],
 ["Bộ lọc hình học", "Chỉ lấy tên OCR khi hộp < 25% màn.\nVí dụ: hộp phủ 95% màn cho chuỗi\n“THEFELLOWSHIPOF THE RING”", "2,2%", "số bước\nbị tác động"]].forEach((c, i) => {
  const x = M + i * 6.2;
  block(x, 1.4, 5.9, 4.9);
  text(c[0], { x: x + 0.3, y: 1.6, w: 5.3, h: 0.55, fontSize: 23, bold: true, color: NAVY });
  text(c[1], { x: x + 0.3, y: 2.3, w: 5.3, h: 1.6, fontSize: 17, lh: 1.15 });
  text(c[2], { x: x + 0.3, y: 4.1, w: 2.6, h: 1.3, fontSize: 48, bold: true, color: TEAL, valign: "middle" });
  text(c[3], { x: x + 2.9, y: 4.1, w: 2.8, h: 1.3, fontSize: 17, color: GREY, valign: "middle", lh: 1.1 });
});
note(SAY[9]); foot();

// ══════════ 10 · Ô THỨ TƯ LÀM LẠI ══════════
slide();
bar("Ô thứ tư phải làm lại: từ 7,3% lên 75,9%");
block(M, 1.4, 5.0, 3.9);
text("Bản đầu", { x: M, y: 1.55, w: 5.0, h: 0.5, fontSize: 22, bold: true, color: GREY, align: "center" });
text("7,3%", { x: M, y: 2.1, w: 5.0, h: 1.1, fontSize: 54, bold: true, color: GREY, align: "center", valign: "middle" });
text("giải quyết được mơ hồ\n85,8% chỉ đếm\n(“một trong bảy phần tử cùng loại”)", { x: M + 0.2, y: 3.3, w: 4.6, h: 1.8, fontSize: 17, align: "center", lh: 1.1 });
arrowR(5.85, 3.3, 1.4, NAVY);
block(7.5, 1.4, 5.23, 3.9, "E6F0EF");
text("Bản làm lại", { x: 7.5, y: 1.55, w: 5.23, h: 0.5, fontSize: 22, bold: true, color: TEAL, align: "center" });
text("75,9%", { x: 7.5, y: 2.1, w: 5.23, h: 1.1, fontSize: 54, bold: true, color: TEAL, align: "center", valign: "middle" });
text("trên mẫu thử\n75,3% trên toàn bộ 41.099 nhãn", { x: 7.7, y: 3.3, w: 4.83, h: 1.8, fontSize: 18, align: "center", lh: 1.15 });
text("737/737 mỏ neo đúng hướng (kiểm tay). Đúng hướng chưa có nghĩa là hữu ích.", { x: M, y: 5.65, w: W - 2 * M, h: 0.7, fontSize: 18, italic: true, color: GREY, align: "center", valign: "middle" });
note(SAY[10]); foot();

// ══════════ 11 · ĐỘ PHỦ CHƯA ĐỀU ══════════
slide();
bar("Độ phủ chưa đều: nhóm cần nhất lại được phủ kém nhất");
{
  const rows = [["tên rõ ràng", "30.252", 80.1, "80,1%", TEAL, true], ["không có tên", "9.038", 66.7, "66,7%", NAVY, false],
    ["chỉ có ký hiệu (vd. “Q”, “?”)", "1.809", 37.5, "37,5%", RED, true], ["toàn bộ", "41.099", 75.3, "75,3%", GREY, false]];
  const x0 = M, y0 = 1.35;
  table(x0, y0, [4.6, 1.7, 5.83], [{ cells: ["tầng tên của phần tử", { t: "số nhãn", align: "right" }, "giải quyết được mơ hồ"], bold: true, color: WHITE, fill: NAVY, h: 0.6 }], { fs: 18 });
  rows.forEach((r, i) => {
    const yy = y0 + 0.6 + i * 1.0;
    text(r[0], { x: x0 + 0.08, y: yy, w: 4.5, h: 1.0, fontSize: 19, bold: i === 3, valign: "middle" });
    text(r[1], { x: x0 + 4.6, y: yy, w: 1.6, h: 1.0, fontSize: 19, align: "right", valign: "middle" });
    const bx = x0 + 6.6, bwMax = 4.0;
    rect(bx, yy + 0.3, bwMax, 0.4, "EEEDF2");
    rect(bx, yy + 0.3, bwMax * r[2] / 100, 0.4, r[4]);
    text(r[3], { x: bx + bwMax + 0.1, y: yy, w: 1.3, h: 1.0, fontSize: 20, bold: r[5], color: r[4], valign: "middle" });
    hline(x0, yy + 1.0, 12.13, LIGHT, 1);
  });
}
note(SAY[11]); foot();

// ══════════ 12 · NGƯỜI VÀ QUY TRÌNH ══════════
slide();
bar("Người chú thích và quy trình tự động chọn cùng chiến lược");
[["Phía màn hình", NAVY, [["55,6%", "số bước có phần tử cạnh tranh trong khoảng 80 đến 350 px"], ["91,6%", "có phần tử cùng vai trò (trung vị 8)"]]],
 ["Phía ngôn ngữ", TEAL, [["32,5%", "câu của người dùng từ chỉ vị trí hoặc thứ tự"], ["67,2%", "dấu hiệu của quy trình là quan hệ với chữ lân cận"]]]].forEach((side, i) => {
  const x = M + i * 6.2;
  text(side[0], { x, y: 1.25, w: 5.9, h: 0.6, fontSize: 24, bold: true, color: side[1], align: "center" });
  side[2].forEach((c, j) => {
    const yy = 2.0 + j * 2.25;
    block(x, yy, 5.9, 2.0);
    text(c[0], { x: x + 0.2, y: yy, w: 2.5, h: 2.0, fontSize: 42, bold: true, color: side[1], valign: "middle" });
    text(c[1], { x: x + 2.75, y: yy, w: 2.95, h: 2.0, fontSize: 18, valign: "middle", lh: 1.1 });
  });
});
note(SAY[12]); foot();

// ══════════ 13 · QUY MÔ ══════════
slide();
bar("Quy mô và cách chia tập");
table(M, 1.35, [3.6, 2.4, 2.4], [
  { cells: ["", { t: "huấn luyện", align: "right" }, { t: "kiểm tra", align: "right" }], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: ["số bước", "64.567", "6.958"], h: 0.7 },
  { cells: ["bước chạm", "41.191", "4.463"], h: 0.7 },
  { cells: ["số tác vụ", "12.895", "1.432"], h: 0.7 },
  { cells: [{ t: "nhãn GUIRefCorpus", bold: true, color: TEAL }, { t: "41.099", bold: true, color: TEAL }, { t: "4.448", bold: true, color: TEAL }], h: 0.7 },
], { fs: 20, align: ["left", "right", "right"] });
[["chia theo tác vụ,", "0 tác vụ trùng", TEAL],
 ["không tách được", "cách diễn đạt", AMBER],
 ["không phải tập ứng dụng chưa thấy", "95,6% ứng dụng có ở tập huấn luyện", AMBER]].forEach((c, i) => {
  const yy = 1.35 + i * 1.32;
  block(9.25, yy, 3.48, 1.17);
  rect(9.25, yy, 0.12, 1.17, c[2]);
  text(c[0] + "\n" + c[1], { x: 9.5, y: yy, w: 3.1, h: 1.17, fontSize: 15, valign: "middle", lh: 1.1 });
});
note(SAY[13]); foot();

// ══════════ 14 · KIỂM BẰNG NGUỒN NGOÀI ══════════
slide();
bar("Kiểm chất lượng bằng một nguồn nằm ngoài quy trình");
vbars(M + 0.3, 1.75, 8.0, 3.35, [
  { label: "ô tên xuất hiện nguyên văn\ntrong câu của người\n(1.875/3.505)", v: 53.5, txt: "53,5%", color: TEAL },
  { label: "ghép với câu của\nbước liền sau (bất kỳ)", v: 5.4, txt: "5,4%", color: "9A94AE" },
  { label: "bước liền sau trong cùng\nchuỗi thao tác\n(đối chứng khó)", v: 7.6, txt: "7,6%", color: "9A94AE" },
], 60, { bw: 0.48, lfs: 14, lh: 1.1 });
block(9.25, 1.7, 3.48, 3.4);
text("Quy trình dựng nhãn không đọc câu chỉ dẫn ở bất kỳ bước nào.", { x: 9.45, y: 1.85, w: 3.1, h: 1.6, fontSize: 18, lh: 1.1 });
text("53,5% là chặn dưới.", { x: 9.45, y: 3.6, w: 3.1, h: 1.2, fontSize: 20, bold: true, color: TEAL, lh: 1.1 });
note(SAY[14]); foot();

// ══════════ 15 · HẠN CHẾ ══════════
slide();
bar("Hạn chế");
[["24,7%", "dấu hiệu chưa giải quyết được mơ hồ", "đã rõ nguyên nhân, sửa được"],
 ["1/4 ô", "so với nguồn ngoài mới chạm ô tên", "ô dấu hiệu chưa được người dùng kiểm"],
 ["Bản gốc", "không có nhãn chuẩn cho OCR", "chuỗi mục tiêu bị cắt (99,4% không kết thúc bằng dấu câu)"]].forEach((c, i) => {
  const yy = 1.35 + i * 1.7;
  block(M, yy, W - 2 * M, 1.5);
  text(c[0], { x: M + 0.2, y: yy, w: 2.8, h: 1.5, fontSize: 36, bold: true, color: RED, align: "center", valign: "middle" });
  text(c[1], { x: M + 3.3, y: yy + 0.2, w: 8.6, h: 0.6, fontSize: 21, bold: true, color: NAVY });
  text(c[2], { x: M + 3.3, y: yy + 0.8, w: 8.6, h: 0.55, fontSize: 18, color: GREY });
});
note(SAY[15]); foot();

// ══════════ 16 · KẾT LUẬN ══════════
slide();
bar("Kết luận");
[["41.099 + 4.448", "nhãn bốn ô GUIRefCorpus, dựng hoàn toàn tự động từ AndroidControl"],
 ["7,3% → 75,3%", "ô dấu hiệu phân biệt"],
 ["53,5% vs 7,6%", "đối chiếu ngoài quy trình (đối chứng khó)"]].forEach((c, i) => {
  const yy = 1.35 + i * 1.55;
  block(M, yy, W - 2 * M, 1.35);
  text(c[0], { x: M + 0.25, y: yy, w: 4.6, h: 1.35, fontSize: 34, bold: true, color: TEAL, valign: "middle" });
  text(c[1], { x: M + 5.0, y: yy, w: 6.9, h: 1.35, fontSize: 21, valign: "middle", lh: 1.1 });
});
text("Phần huấn luyện mô hình: bài đồng hành.", { x: M, y: 6.15, w: W - 2 * M, h: 0.5, fontSize: 17, italic: true, color: GREY, align: "center" });
note(SAY[16]); foot();

// ══════════ 17 · CẢM ƠN ══════════
slide();
rect(0, 0, W, H - 0.32, NAVY);
text("Cảm ơn quý thầy cô và các bạn đã lắng nghe", { x: M, y: 2.2, w: W - 2 * M, h: 1.3, fontSize: 38, bold: true, color: WHITE, align: "center", valign: "middle" });
text("24C15039@student.hcmus.edu.vn", { x: M, y: 3.9, w: W - 2 * M, h: 0.6, fontSize: 22, fontFace: MONO, color: LIGHT, align: "center", valign: "middle" });
note(SAY[17]); foot();

// ══════════════════ DỰ PHÒNG ══════════════════
// B1 · tỉ số 3,2 lần
slide();
bar("Dự phòng · Truy nguyên tỉ số 3,2 lần");
{
  const st = [["72", "nhãn hai nguồn\ncho hai chuỗi khác nhau"], ["−32", "chuỗi đã nằm sẵn\ntrong mục tiêu"], ["40", "nhãn còn lại"]];
  st.forEach((c, i) => {
    const x = M + i * 3.0;
    block(x, 1.5, 2.6, 2.2);
    text(c[0], { x, y: 1.6, w: 2.6, h: 1.0, fontSize: 40, bold: true, color: NAVY, align: "center", valign: "middle" });
    text(c[1], { x: x + 0.1, y: 2.6, w: 2.4, h: 1.0, fontSize: 15, align: "center", lh: 1.05 });
    if (i < 2) arrowR(x + 2.62, 2.6, 0.36);
  });
  table(9.6, 1.5, [2.2, 0.93], [
    { cells: ["khớp OCR", "12"], h: 0.7 }, { cells: ["khớp cây trợ năng", "3"], h: 0.7 }, { cells: ["không bên nào", "25"], h: 0.7, rule: false },
  ], { fs: 18, align: ["left", "right"] });
  block(M, 4.3, W - 2 * M, 1.9, "E6F0EF");
  text("11/12 ca nghiêng về OCR do nhãn trợ năng là chuỗi không dùng được.\nKhi cả hai nguồn đều dùng được: 1 ca nghiêng về OCR, 3 ca nghiêng về cây trợ năng.",
    { x: M + 0.3, y: 4.3, w: W - 2 * M - 0.6, h: 1.9, fontSize: 20, valign: "middle", lh: 1.25 });
}
note(QA("B2")); footB();

// B2 · sáu chỉ số
slide();
bar("Dự phòng · Mẫu thử và toàn bộ ngữ liệu");
table(M + 1.2, 1.35, [5.4, 2.5, 2.0], [
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

// B3 · bốn nhãn thật
slide();
bar("Dự phòng · Bốn nhãn thật và câu của người chú thích");
table(M, 1.35, [8.2, 3.93], [
  { cells: ["nhãn tự động", "câu của người chú thích"], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: [{ t: "tappable text | Search here | <point>440,91</point> | just above the text \"Coffee\"", mono: true, fs: 14 }, { t: "Click on the search bar", italic: true }], h: 1.0 },
  { cells: [{ t: "icon | (no name) | <point>256,524</point> | just above the text \"Leaf\"", mono: true, fs: 14 }, { t: "Choose the leaf option", italic: true }], h: 1.0 },
  { cells: [{ t: "icon | Q | <point>920,899</point> | shares a name with 1 other elements on screen", mono: true, fs: 14 }, { t: "click on the search icon", italic: true }], h: 1.0 },
  { cells: [{ t: "icon | (no name) | <point>920,904</point> | many elements of the same kind on screen", mono: true, fs: 14 }, { t: "Click on the Right arrow key", italic: true }], h: 1.0, rule: false },
], { fs: 18 });
text("Hai dòng đầu: mệnh đề đủ chỉ ra phần tử. Hai dòng sau: chỉ cho biết có phần tử giống nó.", { x: M, y: 5.95, w: W - 2 * M, h: 0.6, fontSize: 17, italic: true, color: GREY, align: "center" });
footB();

// B4 · bảng dấu hiệu đầy đủ
slide();
bar("Dự phòng · Loại dấu hiệu phân biệt theo tầng tên");
table(M, 1.35, [3.4, 1.55, 1.9, 1.7, 2.0, 1.58], [
  { cells: ["tầng tên", "n", "mỏ neo chữ", "duy nhất", "nêu trùng tên", "chỉ đếm"], bold: true, color: WHITE, fill: NAVY, h: 0.65 },
  { cells: ["tên rõ ràng", "30.252", "72,2%", "7,9%", "1,7%", "18,2%"], h: 0.7 },
  { cells: ["chỉ có ký hiệu", "1.809", "32,7%", "4,8%", "31,3%", "31,2%"], h: 0.7 },
  { cells: ["không có tên", "9.038", "57,5%", "9,2%", "-", "33,3%"], h: 0.7 },
  { cells: [{ t: "toàn bộ", bold: true }, { t: "41.099", bold: true }, { t: "67,2%", bold: true }, { t: "8,1%", bold: true }, { t: "2,6%", bold: true }, { t: "22,1%", bold: true }], h: 0.7, rule: false },
], { fs: 19, align: ["left", "right", "right", "right", "right", "right"] });
rect(M + 4.95, 1.35, 3.6, 3.45, "none", { line: TEAL, lw: 2 });
text("Hai cột viền xanh giải quyết được mơ hồ: 80,1% · 37,5% · 66,7% · 75,3%.", { x: M, y: 5.2, w: W - 2 * M, h: 0.6, fontSize: 18, color: TEAL, align: "center" });
note(QA("C3")); footB();

// B5 · một bản ghi
slide();
bar("Dự phòng · Một bản ghi GUIRefCorpus có gì");
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

// B6 · chuỗi mục tiêu bị cắt
slide();
bar("Dự phòng · Chuỗi mục tiêu bị cắt từ nguồn");
block(M, 1.4, W - 2 * M, 1.2);
text("...look for Calvin Kle", { x: M, y: 1.4, w: W - 2 * M, h: 1.2, fontSize: 32, fontFace: MONO, color: RED, align: "center", valign: "middle" });
[["99,4%", "không kết thúc bằng dấu câu"], ["≥ 71,3%", "bị cắt giữa một từ"]].forEach((c, i) => {
  const x = M + 0.8 + i * 5.6;
  text(c[0], { x, y: 3.0, w: 4.9, h: 1.2, fontSize: 52, bold: true, color: NAVY, align: "center", valign: "middle" });
  text(c[1], { x, y: 4.2, w: 4.9, h: 0.6, fontSize: 20, align: "center" });
});
text("Đo trên 1.424 mục tiêu khác nhau của tập kiểm tra.", { x: M, y: 5.5, w: W - 2 * M, h: 0.5, fontSize: 17, italic: true, color: GREY, align: "center" });
footB();

pres.writeFile({ fileName: path.join(__dirname, "..", "VCL2026_SLIDE_15_11.pptx") }).then(() => {
  console.log("Xong: VCL2026_SLIDE_15_11.pptx | chinh " + PAGE + " | du phong " + BPAGE + " | loi noi " + Object.keys(SAY).length);
});
