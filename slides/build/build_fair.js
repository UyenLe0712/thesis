// FAIR'2026 conference talk (15 min + 5 min Q&A) -- 17 main slides + 10 backup slides.
// Style inherited from the thesis defence deck (build_baove.js): 4:3, indigo title bar,
// rounded grey blocks, serif body, four-cell footline. Content: paper/fair2026/main.tex only.
// Output: ../FAIR2026_SLIDE.pptx
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.defineLayout({ name: "A43", width: 10, height: 7.5 });
pres.layout = "A43";
pres.author = "Le Doan Phuong Uyen";
pres.title = "Descriptor-First Supervision for GUI Instruction Generation - FAIR 2026";

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
  rect(0, yy, 2.4, hh, FOOTA); rect(2.4, yy, 4.3, hh, FOOTB);
  rect(6.7, yy, 1.9, hh, FOOTC); rect(8.6, yy, 1.4, hh, FOOTD);
  text("FAIR'2026", { x: 0, y: yy, w: 2.4, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0, fontFace: MONO });
  text("Descriptor-First Supervision for GUI Instruction Generation", { x: 2.4, y: yy, w: 4.3, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text("Uyen  ·  Long", { x: 6.7, y: yy, w: 1.9, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
  text(label, { x: 8.6, y: yy, w: 1.4, h: hh, fontSize: 8, color: WHITE, align: "center", valign: "middle", margin: 0 });
}
function foot() { PAGE++; footRow(`${PAGE}/${TOTAL}`); }
function footB() { BPAGE++; footRow(`backup ${BPAGE}`); }
function block(x, y, w, h) { rect(x, y, w, h, BLOCK, { radius: 0.06, shadow: true }); }
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
const NOTES = require("./notes_fair.json");
function N(i) { if (NOTES[String(i)]) note(NOTES[String(i)]); }
function NB(i) { if (NOTES["B" + i]) note(NOTES["B" + i]); }

// ══════════ 1 · TITLE ══════════
slide();
rect(0, 0, W, 0.66, NAVY);
text("FAIR'2026  ·  Fundamental and Applied IT Research  ·  Natural Language Processing", { x: 0, y: 0, w: W, h: 0.66, fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
rect(0.7, 1.25, W - 1.4, 2.7, NAVY, { radius: 0.09, shadow: true });
text("Descriptor-First Supervision for\nGUI Instruction Generation", { x: 0.8, y: 1.55, w: W - 1.6, h: 1.35, fontSize: 26, bold: true, color: WHITE, align: "center", margin: 0, lh: 1.22 });
hline(3.9, 3.05, 2.2, "9A94AE", 1.5);
text("A Pre-Registered Ablation and the Condition Under Which It Pays", { x: 0.8, y: 3.2, w: W - 1.6, h: 0.6, fontSize: 15, italic: true, color: "D8D4E6", align: "center", margin: 0, lh: 1.25 });
text("Lê Đoàn Phương Uyên            Nguyễn Hồng Bửu Long", { x: 0.8, y: 4.4, w: W - 1.6, h: 0.4, fontSize: 16, bold: true, align: "center", margin: 0 });
text("Faculty of Information Technology,  University of Science, VNU-HCM\nHo Chi Minh City, Vietnam", { x: 0.8, y: 4.95, w: W - 1.6, h: 0.7, fontSize: 13, color: GREY, align: "center", margin: 0, lh: 1.35 });
block(2.35, 5.85, 5.3, 0.6);
text("Code, pre-registration and amendment log are version-controlled.", { x: 2.35, y: 5.85, w: 5.3, h: 0.6, fontSize: 11.5, italic: true, color: NAVY, align: "center", valign: "middle", margin: 0 });
N(1); foot(); done();

// ══════════ 2 · A DIFFERENT CONSUMER ══════════
slide();
bar("A different consumer of the same input");
block(M, 0.9, W - 2 * M, 0.95);
text([{ text: "Input.   ", options: { bold: true, color: BLUE } }, { text: "one screenshot   +   a user goal, e.g. “Share this playlist with my friend”", options: { italic: true } }], { x: M + 0.25, y: 0.9, w: W - 2 * M - 0.5, h: 0.95, fontSize: 14.5, valign: "middle", margin: 0 });
text("GUI agent", { x: M, y: 2.1, w: 4.35, h: 0.4, fontSize: 15, bold: true, color: NAVY, align: "center", margin: 0 });
text("This work", { x: 5.1, y: 2.1, w: 4.35, h: 0.4, fontSize: 15, bold: true, color: RED, align: "center", margin: 0 });
block(M, 2.55, 4.35, 2.5); block(5.1, 2.55, 4.35, 2.5);
text([{ text: "click(872, 141)", options: { fontFace: MONO, bold: true, color: BLUE } }, { text: "\n\nConsumer is a machine that clicks.\nThe wording, if any, is never scored.", options: {} }], { x: M + 0.25, y: 2.8, w: 3.9, h: 2.0, fontSize: 14, margin: 0, lh: 1.45 });
text([{ text: "“Tap the share icon at the\ntop right of the screen.”", options: { italic: true, bold: true, color: RED } }, { text: "\n\nConsumer is a person who must be told\nwhat to do. The sentence is the only\nscored output.", options: {} }], { x: 5.35, y: 2.8, w: 3.9, h: 2.0, fontSize: 14, margin: 0, lh: 1.45 });
text("SeeClick · OS-Atlas · Aguvis", { x: M, y: 5.15, w: 4.35, h: 0.32, fontSize: 11, italic: true, color: GREY, align: "center", margin: 0 });
text("accessibility and user-support settings", { x: 5.1, y: 5.15, w: 4.35, h: 0.32, fontSize: 11, italic: true, color: GREY, align: "center", margin: 0 });
block(M, 5.6, W - 2 * M, 0.85);
text([{ text: "A coordinate can be checked against a recorded coordinate. ", options: {} }, { text: "A sentence cannot be checked against one reference.", options: { bold: true, color: RED } }], { x: M + 0.25, y: 5.6, w: W - 2 * M - 0.5, h: 0.85, fontSize: 14, valign: "middle", margin: 0, lh: 1.35 });
N(2); foot(); done();

// ══════════ 3 · THE INSTRUMENT IDEA ══════════
slide();
bar("A model paper needs an instrument first");
text("Why a reference-based score fails here", { x: M, y: 0.85, w: 4.4, h: 0.34, fontSize: 14, bold: true, color: NAVY, margin: 0 });
bullets([
  "Many wordings identify the same button, and no dataset enumerates them",
  [{ text: "Content-word F1 charges the branches unequally for register: ", options: {} }, { text: "52.8%", options: { bold: true, color: RED } }, { text: " of accepted untuned sentences fall below 0.5, against ", options: {} }, { text: "13.9%", options: { bold: true, color: TEAL } }],
  "BLEU-4 and ROUGE-L score the references 100 by construction, so neither can locate the remaining headroom",
], M, 1.3, 4.4, { fs: 12.5, gap: 1.15, itemH: 1.1, lh: 1.3 });
text("Executability, in one loop", { x: 5.1, y: 0.85, w: 4.35, h: 0.34, fontSize: 14, bold: true, color: NAVY, margin: 0 });
[["generated sentence", "descriptor stripped before scoring", BLOCK, INK],
 ["independent grounding model", "never sees the gold coordinate", BLOCK, INK],
 ["predicted point", "geometry against the recorded human touch", NAVY, WHITE]].forEach((c, i) => {
  const yy = 1.3 + i * 1.15;
  rect(5.1, yy, 4.35, 0.92, c[2], { radius: 0.05, shadow: c[2] === NAVY });
  text(c[0], { x: 5.25, y: yy + 0.08, w: 4.05, h: 0.32, fontSize: 13.5, bold: true, color: c[3], margin: 0 });
  text(c[1], { x: 5.25, y: yy + 0.44, w: 4.05, h: 0.4, fontSize: 11.5, color: c[2] === NAVY ? "D8D4E6" : GREY, margin: 0 });
  if (i < 2) { text("↓", { x: 5.1, y: yy + 0.9, w: 4.35, h: 0.25, fontSize: 13, bold: true, color: FOOTC, align: "center", margin: 0 }); }
});
block(M, 5.05, W - 2 * M, 1.15);
text([{ text: "This is not LLM-as-judge.", options: { bold: true, color: RED } }, { text: "  The rubric is a coordinate a real person touched. The grounder contributes only a localisation, geometry decides, and the same grounder scores every branch.", options: {} }], { x: M + 0.25, y: 5.05, w: W - 2 * M - 0.5, h: 1.15, fontSize: 13.5, valign: "middle", margin: 0, lh: 1.4 });
N(3); foot(); done();

// ══════════ 4 · CONTRIBUTIONS ══════════
slide();
bar("Four contributions, and the honest status of each");
[["i", "An instrument calibrated at both ends", "Measured ceiling 75.7 and, less usually, a measured floor: 12.0 contentless, 6.1 wrong-screen.", "complete", TEAL],
 ["ii", "Supervision that adds no annotation of its own", "Gain measured at two seeds and replicated under a second, independently trained grounder.", "complete", TEAL],
 ["iii", "A pre-registered ablation of the descriptor prefix", "One of four registered runs was never executed. Reported against the rules that refuse a conclusion.", "permanently incomplete", RED],
 ["iv", "A diagnosis of when the component pays", "The prefix is worth +5.7 points where identification succeeds and −25 where it fails.", "exploratory, one seed", MAROON]].forEach((c, i) => {
  const yy = 0.95 + i * 1.32;
  block(M, yy, W - 2 * M, 1.18);
  text(c[0], { x: M + 0.12, y: yy + 0.14, w: 0.55, h: 0.45, fontSize: 20, bold: true, italic: true, color: NAVY, align: "center", margin: 0 });
  text(c[1], { x: M + 0.75, y: yy + 0.12, w: 5.2, h: 0.42, fontSize: 14, bold: true, color: NAVY, margin: 0, lh: 1.15 });
  text(c[3], { x: W - M - 2.8, y: yy + 0.14, w: 2.6, h: 0.35, fontSize: 12, bold: true, color: c[4], align: "right", margin: 0 });
  text(c[2], { x: M + 0.75, y: yy + 0.6, w: W - 2 * M - 1.0, h: 0.52, fontSize: 12.5, margin: 0, lh: 1.3 });
});
N(4); foot(); done();

// ══════════ 5 · METRIC DEFINITION ══════════
slide();
bar("Executability: three conditions, read from the implementation");
[["(i)", "Action", "Canonicalised action types agree. Twelve surface verbs map to one touch class; type, scroll, long-press and back stay distinct."],
 ["(ii)", "Polarity", "The two sentences do not name opposite states of the same control, checked against nine toggle pairs."],
 ["(iii)", "Localisation", "The returned point is inside the ±14% tolerance and no competing element centre is closer to it than the gold point."]].forEach((c, i) => {
  const yy = 0.9 + i * 1.32;
  rect(M, yy, 4.6, 1.2, BLOCK, { radius: 0.05 });
  text(c[0], { x: M + 0.12, y: yy + 0.07, w: 0.55, h: 0.3, fontSize: 12.5, bold: true, color: TEAL, margin: 0 });
  text(c[1], { x: M + 0.66, y: yy + 0.07, w: 3.8, h: 0.3, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
  text(c[2], { x: M + 0.16, y: yy + 0.42, w: 4.28, h: 0.74, fontSize: 11.5, margin: 0, lh: 1.3 });
});
img("../../paper/fair2026/fig_voronoi.png", 5.35, 0.85, 4.1, 2.77);
text("The user touched the shaded row. The untuned model named the row above; the point lands 128 px away, inside the ±336 px vertical tolerance.", { x: 5.35, y: 3.66, w: 4.1, h: 0.72, fontSize: 10.5, italic: true, color: GREY, align: "center", margin: 0, lh: 1.25 });
block(5.35, 4.45, 4.1, 1.4);
bullets([
  "The tolerance region is a per-axis rectangle, not a disc: ±151 px against ±336 px",
  "The cell seed is the recorded touch point, not the box centre",
], 5.45, 4.55, 3.9, { fs: 11, gap: 0.62, itemH: 0.58, lh: 1.25 });
text("Condition (iii) refines the tolerance test and never accepts a step that test rejects, so the two are not alternatives.", { x: M, y: 4.95, w: 4.6, h: 0.9, fontSize: 12, italic: true, color: NAVY, margin: 0, lh: 1.3 });
N(5); foot(); done();

// ══════════ 6 · CALIBRATION ══════════
slide();
bar("Calibrated at both ends before any model claim");
[["Human references  (ceiling)", "75.7", TEAL, 0.757],
 ["Sentence supervision, two seeds", "59.4", NAVY, 0.594],
 ["Not fine-tuned", "47.6", FOOTC, 0.476],
 ["Contentless: “tap the button”", "12.0", RED, 0.12],
 ["Genuine sentence, wrong screen", "6.1", MAROON, 0.061]].forEach((g, i) => {
  const yy = 0.95 + i * 0.72;
  text(g[0], { x: M, y: yy, w: 3.7, h: 0.4, fontSize: 12.5, valign: "middle", margin: 0 });
  rect(4.35, yy + 0.06, 3.8, 0.28, "DCDAE4");
  rect(4.35, yy + 0.06, 3.8 * g[3], 0.28, g[2]);
  text(g[1], { x: 8.25, y: yy, w: 1.2, h: 0.4, fontSize: 15, bold: true, color: g[2], align: "right", valign: "middle", margin: 0 });
});
block(M, 4.6, W - 2 * M, 0.95);
text([{ text: "A correctly-styled sentence with wrong content scores below the contentless floor, on disjoint intervals.", options: { bold: true, color: RED } }, { text: "  So the grounder reads content, not register, and the usable range is 62.9 points.", options: {} }], { x: M + 0.25, y: 4.6, w: W - 2 * M - 0.5, h: 0.95, fontSize: 13, valign: "middle", margin: 0, lh: 1.35 });
text("The cell condition was chosen from what it refuses  (injection study, 250 steps)", { x: M, y: 5.7, w: W - 2 * M, h: 0.3, fontSize: 12.5, bold: true, color: NAVY, margin: 0 });
table(M + 0.3, 6.02, [4.6, 2.1, 1.6], [
  { cells: ["Answer displaced to the nearest competing element", { t: "84.3% still credited", fs: 12.5 }, "tolerance rule"], h: 0.36, fs: 12, color: RED, bold: true, rule: true },
  { cells: ["Same displacement, ceiling 99.7% under a 3% offset", { t: "2.8% credited", fs: 12.5 }, "cell rule"], h: 0.36, fs: 12, color: TEAL, bold: true },
], { align: ["left", "center", "right"] });
N(6); foot(); done();

// ══════════ 7 · WHAT THE METRIC WEIGHS ══════════
slide();
bar("What the instrument weighs, and what it ignores");
text("Ablating the reference sentences themselves, on near-identical populations", { x: M, y: 0.85, w: W - 2 * M, h: 0.32, fontSize: 12.5, italic: true, color: GREY, margin: 0 });
table(M, 1.25, [4.0, 1.5, 1.9, 1.49], [
  { cells: ["Edit applied to the human reference", "Steps", "Cost", "McNemar"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5, align: ["left", "center", "center", "center"] },
  { cells: [{ t: "Name → “the item”, keep the locative clause", bold: true }, "193", { t: "−28.5 pts", bold: true, color: RED }, "b=3, c=58,  p<0.001"], h: 0.5, fs: 12.5, rule: true },
  { cells: ["Delete the locative clause, keep the name", "198", { t: "−3.5 pts", color: MAROON }, "b=1, c=8,  p=0.046"], h: 0.5, fs: 12.5 },
], { align: ["left", "center", "center", "center"] });
block(M, 2.85, W - 2 * M, 0.7);
text("Naming the element is worth roughly eight times saying where it is.", { x: M + 0.25, y: 2.85, w: W - 2 * M - 0.5, h: 0.7, fontSize: 14.5, bold: true, color: NAVY, valign: "middle", margin: 0 });
text("Insensitive to phrasing, sensitive to content", { x: M, y: 3.75, w: W - 2 * M, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  [{ text: "Meaning-preserving rewrites of 1,139 references (verb substitution, fronting the locative clause) move the score by ", options: {} }, { text: "+0.35 pp  [−0.59, +1.29]", options: { bold: true, color: TEAL } }, { text: ", with 2.6% of steps changing verdict", options: {} }],
  [{ text: "Five hit rules on 698 steps: absolute level moves by up to 26 points, ", options: {} }, { text: "the ordering never does", options: { bold: true, color: TEAL } }, { text: ", and the fine-tuning gain stays between +9.5 and +13.0", options: {} }],
  [{ text: "Determinism: on 2,810 steps where two runs wrote byte-identical sentences, the grounder returned ", options: {} }, { text: "identical verdicts on all 2,810", options: { bold: true, color: TEAL } }],
], M + 0.1, 4.2, W - 2 * M - 0.2, { fs: 12.5, gap: 0.72, itemH: 0.68, lh: 1.3 });
block(M, 6.4, W - 2 * M, 0.72);
text("Intervals are cluster bootstraps (10,000 resamples, G_eff = 454.3). Minimum detectable paired effect: 2.2 points.", { x: M + 0.25, y: 6.4, w: W - 2 * M - 0.5, h: 0.72, fontSize: 12, valign: "middle", margin: 0 });
N(7); foot(); done();

// ══════════ 8 · SUPERVISION AND BRANCHES ══════════
slide();
bar("Supervision assembled without new annotation");
text("No new labels collected, and no labels generated by another language model: the scored target is the per-step instruction the dataset already records, and the descriptor slots are derived by rule.", { x: M, y: 0.82, w: W - 2 * M, h: 0.62, fontSize: 12.5, margin: 0, lh: 1.3 });
table(M + 0.65, 1.55, [2.4, 2.1, 2.1, 1.6], [
  { cells: ["Split", "Steps", "Touch steps", "Tasks"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12.5, align: ["left", "center", "center", "center"] },
  { cells: ["Training", "64,567", "≈ 64%", "12,895"], h: 0.4, fs: 13, rule: true },
  { cells: [{ t: "Test (scored)", bold: true }, { t: "6,958", bold: true }, { t: "4,463", bold: true }, { t: "1,432", bold: true }], h: 0.4, fs: 13 },
], { align: ["left", "center", "center", "center"] });
bullets([
  [{ text: "An off-by-one join would corrupt every label while leaving the pipeline functional, so we test it: OCR at the gold point appears in the reference on ", options: {} }, { text: "48%", options: { bold: true, color: TEAL } }, { text: " of n=400 steps, against ", options: {} }, { text: "20%", options: { bold: true, color: RED } }, { text: " under a shifted control", options: {} }],
  [{ text: "Held out by task, zero task overlap, verified at full scale. Only ", options: {} }, { text: "12.6%", options: { bold: true, color: RED } }, { text: " of elements carry any name, so every screen goes through OCR", options: {} }],
], M, 3.1, W - 2 * M, { fs: 12.5, gap: 0.95, itemH: 0.9, lh: 1.3 });
text("Four branches, identical inputs, different generation target", { x: M, y: 5.0, w: W - 2 * M, h: 0.3, fontSize: 13, bold: true, color: NAVY, margin: 0 });
rect(M, 5.35, W - 2 * M, 0.85, "FFFFFF", { line: "9A94AE" });
text([{ text: "S1  ", options: { bold: true, color: NAVY } }, { text: "sentence only", options: {} }, { text: "        S2  ", options: { bold: true, color: RED } }, { text: "<desc>role | name | <point>x,y</point> | cue</desc> then the same sentence", options: { fontFace: MONO, fontSize: 10.5 } }], { x: M + 0.2, y: 5.42, w: W - 2 * M - 0.4, h: 0.34, fontSize: 12.5, margin: 0 });
text([{ text: "S2r  ", options: { bold: true, color: GREY } }, { text: "false descriptor      ", options: { color: GREY } }, { text: "S2-nopoint  ", options: { bold: true, color: GREY } }, { text: "no coordinate slot      ", options: { color: GREY } }, { text: "registered, not run", options: { italic: true, color: MAROON } }], { x: M + 0.2, y: 5.8, w: W - 2 * M - 0.4, h: 0.34, fontSize: 11.5, margin: 0 });
block(M, 6.35, W - 2 * M, 0.75);
text([{ text: "The scored sentence is byte-identical across branches on all 64,567 examples.", options: { bold: true, color: RED } }, { text: "  A difference between branches is a difference in what precedes the sentence, and nothing else.", options: {} }], { x: M + 0.25, y: 6.35, w: W - 2 * M - 0.5, h: 0.75, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.3 });
N(8); foot(); done();

// ══════════ 9 · PRE-REGISTRATION ══════════
slide();
bar("The design was sealed before the first training run");
text("Committed to version control before any executability score existed. Twenty-seven amendments, dated and appended, twenty-one of them before the first score.", { x: M, y: 0.82, w: W - 2 * M, h: 0.55, fontSize: 12.5, margin: 0, lh: 1.3 });
table(M, 1.5, [2.3, 2.5], [
  { cells: ["Outcome", "Reading rule fixed in advance"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12 },
  { cells: [{ t: "Positive", color: TEAL, bold: true }, "interval excludes zero, above seed noise"], h: 0.52, fs: 11.5, rule: true },
  { cells: [{ t: "Trend", color: TEAL }, "interval touches zero"], h: 0.44, fs: 11.5, rule: true },
  { cells: [{ t: "Inconclusive", color: MAROON, bold: true }, "covers zero, |Δ| below detectable"], h: 0.5, fs: 11.5, rule: true },
  { cells: [{ t: "Harm", color: RED, bold: true }, "negative upper bound"], h: 0.44, fs: 11.5 },
]);
bullets([
  "Registered quantity averages two seeds per branch",
  "Inconclusive band fixed at −2.8 … +1.7 pp",
  "Minimum detectable effect 2.2 pp, computed before any score",
  "Six later amendments each moved the headroom up and the threshold down; we flag rather than hide that pattern",
], 5.15, 1.55, 4.3, { fs: 12, gap: 0.85, itemH: 0.8, lh: 1.3 });
rect(M, 5.05, W - 2 * M, 1.15, "FFFFFF", { line: RED, lw: 1.5 });
text([{ text: "The second seed of the treatment branch was never run.", options: { bold: true, color: RED } }, { text: "  A budget decision taken on 23 August 2026, and it will not be. The registered estimand is permanently incomplete, and no later analysis upgrades a single-seed comparison into the conclusion the two-seed rule would have licensed.", options: {} }], { x: M + 0.25, y: 5.05, w: W - 2 * M - 0.5, h: 1.15, fontSize: 13, valign: "middle", margin: 0, lh: 1.38 });
N(9); foot(); done();

// ══════════ 10 · MAIN TABLE ══════════
slide();
bar("Executability on the 4,463-step touch population");
table(M, 0.95, [4.0, 1.6, 2.2, 1.09], [
  { cells: ["Branch", "Exec.", "95% CI", ""], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5, align: ["left", "center", "center", "center"] },
  { cells: [{ t: "Human references  (ceiling)", italic: true }, { t: "75.7", bold: true, color: TEAL }, "[74.1, 77.3]", ""], h: 0.46, fs: 13, rule: "322164", ruleW: 1.5 },
  { cells: ["Base, not fine-tuned", "47.6", "[45.9, 49.3]", ""], h: 0.44, fs: 13, rule: true },
  { cells: ["S1, sentence only, seed 101", "59.1", "[57.3, 60.8]", ""], h: 0.44, fs: 13, rule: true },
  { cells: ["S1, sentence only, seed 202", "59.6", "[57.9, 61.3]", ""], h: 0.44, fs: 13, rule: true },
  { cells: [{ t: "S1, mean of two seeds", bold: true }, { t: "59.4", bold: true, color: NAVY }, "-", ""], h: 0.44, fs: 13, rule: "322164", ruleW: 1.5 },
  { cells: ["S2, descriptor first, seed 101", "57.2", "[55.4, 58.9]", { t: "exploratory", color: MAROON, italic: true }], h: 0.44, fs: 13, rule: true },
  { cells: ["CE2, stage-2 control", "59.4", "[57.7, 61.1]", { t: "exploratory", color: MAROON, italic: true }], h: 0.44, fs: 13, rule: true },
  { cells: ["MIN, stage-2 preference", { t: "60.0", bold: true }, "[58.3, 61.8]", { t: "exploratory", color: MAROON, italic: true }], h: 0.44, fs: 13, rule: true },
  { cells: [{ t: "Contentless sentence", italic: true }, { t: "12.0", color: RED }, "[9.7, 14.4]", { t: "800-step slice", italic: true, color: GREY, fs: 10.5 }], h: 0.44, fs: 13 },
], { align: ["left", "center", "center", "center"] });
text("Every branch below the second rule carries one seed. Registered but not run: S2 seed 202, S2r, S2-nopoint.", { x: M, y: 5.45, w: W - 2 * M, h: 0.3, fontSize: 11.5, italic: true, color: GREY, margin: 0 });
block(M, 5.82, W - 2 * M, 0.85);
text([{ text: "Read every row against 75.7, not against 100.", options: { bold: true, color: NAVY } }, { text: "  Fine-tuning closes 42% of the distance to the human level; the intervals for Base, S1 and the ceiling are disjoint.", options: {} }], { x: M + 0.25, y: 5.82, w: W - 2 * M - 0.5, h: 0.85, fontSize: 13, valign: "middle", margin: 0, lh: 1.35 });
N(10); foot(); done();

// ══════════ 11 · Q1 ══════════
slide();
bar("Q1  Automatic supervision works, and it replicates");
[["Base", "47.6", FOOTC], ["S1  (2 seeds)", "59.4", NAVY], ["Human", "75.7", TEAL]].forEach((c, i) => {
  const xx = 1.15 + i * 2.9;
  rect(xx, 0.9, 2.0, 0.9, i === 1 ? NAVY : BLOCK, { radius: 0.06, shadow: true });
  text(c[0], { x: xx, y: 0.96, w: 2.0, h: 0.3, fontSize: 12.5, bold: true, color: i === 1 ? WHITE : NAVY, align: "center", margin: 0 });
  text(c[1], { x: xx, y: 1.28, w: 2.0, h: 0.42, fontSize: 19, bold: true, color: i === 1 ? WHITE : (i === 2 ? TEAL : INK), align: "center", margin: 0 });
  if (i < 2) arrow(xx + 2.1, 1.35, 0.7, FOOTC);
});
text("paired +11.5 / +12.0", { x: 3.15, y: 1.85, w: 2.0, h: 0.3, fontSize: 11.5, color: MAROON, align: "center", margin: 0 });
text("42% of the gap closed", { x: 3.15, y: 1.85, w: 2.0, h: 0.62, fontSize: 11, color: MAROON, align: "center", valign: "bottom", margin: 0 });
table(M, 2.55, [3.5, 1.5, 2.2, 1.69], [
  { cells: ["Paired comparison (McNemar)", "Δ", "detail", "p"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12, align: ["left", "center", "center", "center"] },
  { cells: [{ t: "S1 − Base, seed 101", bold: true }, { t: "+11.5", bold: true, color: TEAL }, "b=284, c=798", "<0.001"], h: 0.44, fs: 12.5, rule: true },
  { cells: ["S1 − Base, seed 202", "+12.0", "χ² = 243.2 at 101", "<0.001"], h: 0.42, fs: 12.5, rule: true },
  { cells: [{ t: "Retraining noise, seed 101 vs 202", italic: true }, "+0.52", "[−0.2, +1.3]", "0.19"], h: 0.42, fs: 12.5 },
], { align: ["left", "center", "center", "center"] });
text("The effect is 22 times the movement caused by rebuilding the same branch.", { x: M, y: 4.35, w: W - 2 * M, h: 0.34, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  [{ text: "Not memorisation: on the 3,367 steps where the model writes its own sentence, the gap is still ", options: {} }, { text: "+8.4 points", options: { bold: true, color: TEAL } }],
  [{ text: "No home advantage: ", options: {} }, { text: "59.1 / 59.0 / 59.2", options: { bold: true, color: TEAL } }, { text: " on seen, unseen and unattributable applications", options: {} }],
  [{ text: "Second grounder, not trained on AndroidControl: the positive control keeps ", options: {} }, { text: "94%", options: { bold: true, color: TEAL } }, { text: " of its size (+10.35 → +9.68), so “it only learnt the annotator's register” does not survive", options: {} }],
], M + 0.1, 4.8, W - 2 * M - 0.2, { fs: 12.5, gap: 0.72, itemH: 0.68, lh: 1.3 });
N(11); foot(); done();

// ══════════ 12 · Q2 ══════════
slide();
bar("Q2  The descriptor branch: our own rules refuse a conclusion");
block(M, 0.88, W - 2 * M, 0.85);
text([{ text: "S2 scores 57.2, which is 1.93 points below S1 at the same seed", options: { bold: true, color: RED } }, { text: "   (b = 254, c = 340, interval [−3.06, −0.75]).", options: {} }], { x: M + 0.25, y: 0.88, w: W - 2 * M - 0.5, h: 0.85, fontSize: 13.5, valign: "middle", margin: 0 });
// band diagram: -4.0 .. +3.0 pp
const BX = M, BW = W - 2 * M, LO = -4.0, HI = 3.0, SC = BW / (HI - LO);
text("Registered reading bands for Δ = mean(S2) − mean(S1)", { x: M, y: 1.9, w: BW, h: 0.3, fontSize: 12.5, bold: true, color: NAVY, margin: 0 });
rect(BX, 2.35, BW, 0.42, "DCDAE4");
rect(BX + (-2.8 - LO) * SC, 2.35, (1.7 - (-2.8)) * SC, 0.42, "CFCADE");
rect(BX, 2.35, (-2.8 - LO) * SC, 0.42, "E8C9C9");
rect(BX + (1.7 - LO) * SC, 2.35, (HI - 1.7) * SC, 0.42, "C9DED4");
text("harm", { x: BX, y: 2.35, w: (-2.8 - LO) * SC, h: 0.42, fontSize: 11, bold: true, color: RED, align: "center", valign: "middle", margin: 0 });
text("inconclusive band   −2.8 … +1.7", { x: BX + (-2.8 - LO) * SC, y: 2.35, w: (1.7 + 2.8) * SC, h: 0.42, fontSize: 11, bold: true, color: NAVY, align: "center", valign: "middle", margin: 0 });
text("positive", { x: BX + (1.7 - LO) * SC, y: 2.35, w: (HI - 1.7) * SC, h: 0.42, fontSize: 11, bold: true, color: TEAL, align: "center", valign: "middle", margin: 0 });
rect(BX + (-2.19 - LO) * SC - 0.015, 2.22, 0.03, 0.68, RED);
text("−2.19  measured", { x: BX + (-2.19 - LO) * SC - 1.0, y: 2.92, w: 2.0, h: 0.3, fontSize: 11.5, bold: true, color: RED, align: "center", margin: 0 });
text("0", { x: BX + (0 - LO) * SC - 0.2, y: 2.92, w: 0.4, h: 0.3, fontSize: 11, color: GREY, align: "center", margin: 0 });
text("What the missing run could have changed, by the same thresholds", { x: M, y: 3.45, w: W - 2 * M, h: 0.3, fontSize: 12.5, bold: true, color: NAVY, margin: 0 });
table(M + 0.3, 3.8, [4.3, 2.0, 2.0], [
  { cells: ["To reach the weakly-positive edge, Δ = +1.7", { t: "65.0%", bold: true, color: TEAL }, "16.9 seed-SDs away"], h: 0.42, fs: 12, rule: true },
  { cells: ["To reach the harm band", { t: "≤ 56.0%", bold: true, color: RED }, "2.7 seed-SDs away"], h: 0.42, fs: 12 },
], { align: ["left", "center", "right"] });
text("65.0% is 4.9 points above the best checkpoint we ever measured. The remaining outcome space was inconclusive or negative, so no positive result is being withheld.", { x: M, y: 4.72, w: W - 2 * M, h: 0.5, fontSize: 12, italic: true, color: MAROON, margin: 0, lh: 1.3 });
block(M, 5.3, W - 2 * M, 0.9);
text([{ text: "Two things do not depend on the missing seed.", options: { bold: true, color: NAVY } }, { text: "  The branch is +9.6 points above the untuned model, so the descriptor target does not break fine-tuning; and it emits its coordinate slot well, 71.0% inside the window. Whatever the prefix costs, it does not cost the ability to point.", options: {} }], { x: M + 0.25, y: 5.3, w: W - 2 * M - 0.5, h: 0.9, fontSize: 12, valign: "middle", margin: 0, lh: 1.32 });
N(12); foot(); done();

// ══════════ 13 · 2x2 DIAGNOSIS ══════════
slide();
bar("Where the prefix pays, and where it costs");
text("The branch emits its own descriptor, so its identification is scored against gold labels independently of the sentence (3,245 steps with a gold name and a parsable descriptor).", { x: M, y: 0.82, w: W - 2 * M, h: 0.5, fontSize: 12, italic: true, color: GREY, margin: 0, lh: 1.28 });
table(M, 1.4, [1.5, 1.4, 1.1, 1.2, 1.2, 1.2, 1.29], [
  { cells: ["Name", "Point", "n", "Base", "S1", "S2", "Δ"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12, align: ["left", "left", "center", "center", "center", "center", "center"] },
  { cells: [{ t: "correct", color: TEAL, bold: true }, { t: "inside", color: TEAL, bold: true }, "1,871", "69.0", "81.4", { t: "87.1", bold: true }, { t: "+5.7", bold: true, color: TEAL }], h: 0.5, fs: 12.5, rule: true },
  { cells: ["correct", "outside", "184", "23.4", "25.5", "26.1", "+0.5"], h: 0.44, fs: 12.5, rule: true },
  { cells: ["wrong", "inside", "452", "41.4", "56.4", "57.5", "+1.1"], h: 0.44, fs: 12.5, rule: true },
  { cells: [{ t: "wrong", color: RED, bold: true }, { t: "outside", color: RED, bold: true }, { t: "738", bold: true }, "24.4", "30.8", { t: "5.6", bold: true, color: RED }, { t: "−25.2", bold: true, color: RED }], h: 0.5, fs: 12.5 },
], { align: ["left", "left", "center", "center", "center", "center", "center"] });
bullets([
  [{ text: "The branch matches or exceeds the control in three of four rows. ", options: {} }, { text: "All the damage sits in the fourth", options: { bold: true, color: RED } }, { text: ", 16.5% of the scored population", options: {} }],
  "The cost of the design is commitment: having named the wrong element, the branch writes a sentence faithful to it, while the control, committed to nothing, still retrieves the right element on 30.8% of them",
], M + 0.1, 3.75, W - 2 * M - 0.2, { fs: 12.5, gap: 0.78, itemH: 0.74, lh: 1.3 });
rect(M, 5.35, W - 2 * M, 1.4, "FFFFFF", { line: "9A94AE" });
text([{ text: "The objection, and the column that answers it.", options: { bold: true, color: NAVY } }, { text: "  The stratification conditions on a variable the treatment produces, so the failing row could simply be the hard steps. The human references are not conditioned on the treatment and still reach ", options: {} }, { text: "66.3%", options: { bold: true, color: TEAL } }, { text: " there, against 5.6 for the treatment and 24.4 for the untuned model. The row is harder than average, and that does not account for the collapse. The confound is bounded, not removed.", options: {} }], { x: M + 0.25, y: 5.35, w: W - 2 * M - 0.5, h: 1.4, fontSize: 12, valign: "middle", margin: 0, lh: 1.35 });
N(13); foot(); done();

// ══════════ 14 · ACTIVATION SLICE ══════════
slide();
bar("A third of the difference sits in 7.3% of the steps");
text("Slice registered on 19 August, before any treatment score existed: steps where the branch emits a descriptor against steps where it emits none.", { x: M, y: 0.85, w: W - 2 * M, h: 0.45, fontSize: 12.5, italic: true, color: GREY, margin: 0, lh: 1.28 });
table(M, 1.4, [2.9, 1.1, 1.1, 1.1, 2.7], [
  { cells: ["Group", "n", "S1", "S2", "Δ"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5, align: ["left", "center", "center", "center", "center"] },
  { cells: ["Descriptor emitted", "4,138", "62.2", "60.8", { t: "−1.38  [−2.54, −0.19]", fs: 11.5 }], h: 0.48, fs: 13, rule: true },
  { cells: [{ t: "No descriptor emitted", bold: true, color: RED }, { t: "325", bold: true }, "19.7", { t: "10.8", bold: true }, { t: "−8.92  [−12.57, −5.25]", bold: true, color: RED, fs: 11.5 }], h: 0.48, fs: 13 },
], { align: ["left", "center", "center", "center", "center"] });
text("There the model misjudges the action class, not the element", { x: M, y: 2.75, w: W - 2 * M, h: 0.32, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
rect(M, 3.1, W - 2 * M, 0.8, "FFFFFF", { line: "9A94AE" });
text([{ text: "Reference:  ", options: { color: GREY } }, { text: "“Click on the close icon.”", options: { italic: true } }, { text: "        S2:  ", options: { color: GREY } }, { text: "“Swipe up.”", options: { italic: true, bold: true, color: RED } }], { x: M + 0.25, y: 3.1, w: W - 2 * M - 0.5, h: 0.8, fontSize: 13, valign: "middle", margin: 0 });
bullets([
  [{ text: "The steps are solvable and the instrument is not blind: the human references score ", options: {} }, { text: "68.3%", options: { bold: true, color: TEAL } }, { text: " there", options: {} }],
  [{ text: "The failure is not created by the descriptor. Correct action class on those steps: ", options: {} }, { text: "Base 83.4%", options: { bold: true, color: TEAL } }, { text: "  vs  ", options: {} }, { text: "S1 55.1%", options: { bold: true, color: MAROON } }, { text: "  vs  ", options: {} }, { text: "S2 38.8%", options: { bold: true, color: RED } }],
  "Fine-tuning damages the action prior; the descriptor target amplifies it. The branch registered to test the mechanism, S2-nopoint, is among the cancelled runs",
], M + 0.1, 4.1, W - 2 * M - 0.2, { fs: 12.5, gap: 0.75, itemH: 0.7, lh: 1.3 });
block(M, 6.4, W - 2 * M, 0.72);
text("Declared limitation: the 325 steps are defined by the treatment's own behaviour. What is not definitional is that the control also scores only 19.7% there.", { x: M + 0.25, y: 6.4, w: W - 2 * M - 0.5, h: 0.72, fontSize: 12, valign: "middle", margin: 0, lh: 1.3 });
N(14); foot(); done();

// ══════════ 15 · PREFERENCE STAGE ══════════
slide();
bar("The objective this diagnosis specifies, and what it returned");
rect(M, 0.85, W - 2 * M, 0.95, "FFFFFF", { line: "9A94AE" });
text([{ text: "chosen     ", options: { color: TEAL, bold: true } }, { text: "<desc>gold descriptor</desc>  +  sentence", options: { fontFace: MONO } }], { x: M + 0.25, y: 0.92, w: W - 2 * M - 0.5, h: 0.38, fontSize: 12, margin: 0 });
text([{ text: "rejected  ", options: { color: RED, bold: true } }, { text: "<desc>wrong descriptor</desc>  +  the same sentence, verbatim", options: { fontFace: MONO } }], { x: M + 0.25, y: 1.32, w: W - 2 * M - 0.5, h: 0.38, fontSize: 12, margin: 0 });
text("The preference term can be reduced only by choosing the right element.", { x: M, y: 1.92, w: W - 2 * M, h: 0.3, fontSize: 12.5, italic: true, color: NAVY, margin: 0 });
[["S2", "57.2", FOOTC], ["CE2  control", "59.4", FOOTC], ["MIN  preference", "60.0", NAVY]].forEach((c, i) => {
  const xx = 1.05 + i * 2.95;
  rect(xx, 2.35, 2.1, 0.9, i === 2 ? NAVY : BLOCK, { radius: 0.06, shadow: true });
  text(c[0], { x: xx, y: 2.41, w: 2.1, h: 0.3, fontSize: 12.5, bold: true, color: i === 2 ? WHITE : NAVY, align: "center", margin: 0 });
  text(c[1], { x: xx, y: 2.73, w: 2.1, h: 0.42, fontSize: 18, bold: true, color: i === 2 ? WHITE : INK, align: "center", margin: 0 });
  if (i < 2) arrow(xx + 2.2, 2.8, 0.65, FOOTC);
});
text("+2.24\n800 supervised updates,\nno preference term", { x: 3.15, y: 3.3, w: 2.1, h: 0.75, fontSize: 11, color: MAROON, align: "center", margin: 0, lh: 1.2 });
text("+0.63\nthe preference term\nitself", { x: 6.1, y: 3.3, w: 2.1, h: 0.75, fontSize: 11, color: MAROON, align: "center", margin: 0, lh: 1.2 });
block(M, 4.2, W - 2 * M, 0.72);
text("Of the +2.87 pp the stage gains in total, 78% belongs to the control. At the descriptor layer the split is 88/12.", { x: M + 0.25, y: 4.2, w: W - 2 * M - 0.5, h: 0.72, fontSize: 13.5, bold: true, color: RED, valign: "middle", margin: 0 });
table(M, 5.05, [3.6, 1.5, 2.2, 1.59], [
  { cells: ["Registered contrast", "Δ", "95% CI", "p"], bold: true, color: WHITE, fill: NAVY, h: 0.38, fs: 12, align: ["left", "center", "center", "center"] },
  { cells: [{ t: "MIN − CE2  (primary)", bold: true }, { t: "+0.63", bold: true }, "[+0.16, +1.10]", "0.011"], h: 0.42, fs: 12.5, rule: true },
  { cells: ["MIN − S1", "+0.94", "[−0.09, +2.05]", "0.11"], h: 0.4, fs: 12.5 },
], { align: ["left", "center", "center", "center"] });
block(M, 6.32, W - 2 * M, 0.8);
text([{ text: "Inconclusive again:", options: { bold: true, color: MAROON } }, { text: "  +0.63 sits below the 2.11 pp detectable effect for a one-seed design and is 1.4× the seed term. A registered on-policy variant never trained at all, stopped by its feasibility check at 3.3% usable pairs against a 25% threshold.", options: {} }], { x: M + 0.25, y: 6.32, w: W - 2 * M - 0.5, h: 0.8, fontSize: 12, valign: "middle", margin: 0, lh: 1.3 });
N(15); foot(); done();

// ══════════ 16 · CONCLUSION ══════════
slide();
bar("Conclusion");
[["Instrument", "Executability, calibrated at both ends: a measured ceiling of 75.7 and a measured floor of 12.0, with a wrong-screen control at 6.1 on disjoint intervals.", TEAL],
 ["Result", "Supervision assembled without new annotation moves the model 47.6 → 59.4 over two seeds, 22 times the seed noise, and the sign holds under a second grounder.", NAVY],
 ["Ablation", "Whether the descriptor prefix helps is a question our own reading rules refuse to answer, and the run that would have answered it was never executed.", MAROON],
 ["Condition", "The prefix is worth +5.7 points where identification succeeds and −25 where it fails. What it is worth is conditional on identification accuracy.", RED]].forEach((c, i) => {
  const yy = 0.95 + i * 1.28;
  rect(M, yy, W - 2 * M, 1.15, BLOCK, { radius: 0.06, shadow: true });
  text(c[0], { x: M + 0.2, y: yy + 0.1, w: 2.0, h: 0.32, fontSize: 14, bold: true, color: c[2], margin: 0 });
  text(c[1], { x: M + 0.2, y: yy + 0.46, w: W - 2 * M - 0.4, h: 0.62, fontSize: 12.5, margin: 0, lh: 1.32 });
});
block(M, 6.15, W - 2 * M, 0.85);
text([{ text: "Where the next experiment has to act:", options: { bold: true, color: NAVY } }, { text: "  lifting the failing row to the control's own level on those 738 steps would be worth 4.2 points, the size of effect this study set out to detect.", options: {} }], { x: M + 0.25, y: 6.15, w: W - 2 * M - 0.5, h: 0.85, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.35 });
N(16); foot(); done();

// ══════════ 17 · THANK YOU ══════════
slide();
rect(0, 0, W, H, NAVY);
text("Thank you", { x: 0.8, y: 2.5, w: W - 1.6, h: 0.8, fontSize: 30, bold: true, color: WHITE, align: "center", margin: 0 });
text("Questions welcome", { x: 0.8, y: 3.4, w: W - 1.6, h: 0.5, fontSize: 16, color: "D8D4E6", align: "center", margin: 0 });
hline(3.6, 4.25, 2.8, "7A7099", 1.5);
text("Lê Đoàn Phương Uyên   ·   24C15039@student.hcmus.edu.vn\nNguyễn Hồng Bửu Long   ·   nhblong@fit.hcmus.edu.vn\nFaculty of Information Technology, University of Science, VNU-HCM", { x: 0.8, y: 4.55, w: W - 1.6, h: 1.1, fontSize: 13, color: "D8D4E6", align: "center", margin: 0, lh: 1.45 });
N(17); foot(); done();

// ═══════════════ BACKUP SLIDES ═══════════════

// B1 · reference-based scores
slide();
bar("Backup · Why not BLEU, ROUGE, or an embedding score");
table(M, 1.05, [3.4, 2.0, 1.75, 1.75], [
  { cells: ["Branch", "Executability", "BLEU-4", "ROUGE-L"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5, align: ["left", "center", "center", "center"] },
  { cells: ["Base", "47.6", "9.7", "40.3"], h: 0.44, fs: 13, rule: true },
  { cells: ["S1", "59.1", "38.7", "67.3"], h: 0.44, fs: 13, rule: true },
  { cells: [{ t: "Human references", italic: true }, { t: "75.7", bold: true }, { t: "96.1", color: GREY }, { t: "100.0", color: GREY }], h: 0.44, fs: 13 },
], { align: ["left", "center", "center", "center"] });
text("BLEU-4 and ROUGE-L figures come from the thesis version; the submitted paper states only the ordering.", { x: M, y: 2.85, w: W - 2 * M, h: 0.3, fontSize: 11, italic: true, color: GREY, margin: 0 });
bullets([
  "The three measures agree on the ordering only because the branches are far apart; we draw nothing from that agreement",
  "A reference-based score charges the branches unequally for register: 52.8% of accepted untuned sentences fall below 0.5 content-word F1, against 13.9% for the fine-tuned one",
  "Neither can locate the remaining headroom: they score the references 100 by construction, where executability puts them at 75.7",
  "Zhao et al. (EACL 2021) recommend a reference-based score for ranking systems, so every claim here is made at system level and never per sentence",
], M, 3.3, W - 2 * M, { fs: 12.5, gap: 0.78, itemH: 0.74, lh: 1.3 });
NB(1); footB(); done();

// B2 · second grounder
slide();
bar("Backup · Re-scored with a second, independently trained grounder");
text("2,532-step slice, UI-Venus-Ground-7B, not trained on AndroidControl", { x: M, y: 0.85, w: W - 2 * M, h: 0.3, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M, 1.25, [3.2, 2.85, 2.84], [
  { cells: ["Contrast", "UGround", "UI-Venus"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5, align: ["left", "center", "center"] },
  { cells: [{ t: "S1 − Base  (positive control)", bold: true }, { t: "+10.35  [+8.39, +12.40]", color: TEAL, bold: true }, { t: "+9.68  [+7.60, +11.78]", color: TEAL, bold: true }], h: 0.55, fs: 12, rule: true },
  { cells: ["S2 − S1  (single seed)", { t: "−1.93  [−3.08, −0.78]", color: RED }, { t: "−1.21  [−2.30, −0.12]", color: RED }], h: 0.5, fs: 12, rule: true },
  { cells: ["Adequacy ceiling (n = 300)", "70.0  [64.5, 75.3]", "69.3  [63.8, 74.8]"], h: 0.44, fs: 12 },
], { align: ["left", "center", "center"] });
bullets([
  "The positive control retains 94% of its magnitude, so the scale is not compressed and the second instrument can still see effects",
  "The two adequacy ceilings are within 0.7 points of each other",
  "A paired difference-in-differences puts S2 − S1 1.26 pp less negative under UI-Venus, [+0.04, +2.51]: weak, exploratory, and it cannot carry the reading that the first grounder is what makes S2 lose, which would require the contrast to reach zero",
  "Part of the shrinkage is mechanical: UI-Venus scores 2.8-4.1 points lower on every branch",
  "Not closed: both grounders are built on Qwen-family backbones, and no human evaluation anchors either",
], M, 3.35, W - 2 * M, { fs: 12, gap: 0.68, itemH: 0.64, lh: 1.3 });
NB(2); footB(); done();

// B3 · hit rules
slide();
bar("Backup · Hit-rule sensitivity and determinism");
text("Three branches re-scored on 698 steps under five rules", { x: M, y: 0.85, w: W - 2 * M, h: 0.3, fontSize: 12, italic: true, color: GREY, margin: 0 });
table(M + 0.3, 1.2, [4.0, 2.2, 2.1], [
  { cells: ["Hit rule", "Ceiling", "S1 − Base"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12.5, align: ["left", "center", "center"] },
  { cells: ["Euclidean disc", "80.2", "+12.6"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["Per-axis rectangle (the convention)", "82.2", "+13.0"], h: 0.4, fs: 12.5, rule: true },
  { cells: [{ t: "Cell rule as implemented", bold: true }, { t: "74.2", bold: true }, { t: "+11.7", bold: true }], h: 0.4, fs: 12.5, rule: true },
  { cells: ["Cell rule seeded at the box centre", "56.6", "+9.5"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["Nearest box", "82.2", "+13.0"], h: 0.4, fs: 12.5 },
], { align: ["left", "center", "center"] });
bullets([
  "The absolute level moves by up to 26 points, the ordering of the branches never does, and the fine-tuning gain stays between +9.5 and +13.0",
  "Determinism: on 2,810 steps where two runs emitted byte-identical sentences, the grounder returned identical coordinates and identical verdicts on all 2,810",
  "Step-level agreement across seeds is 93.6% (κ = 0.867), but 63% of those pairs are byte-identical sentences a deterministic instrument must agree on; on the 1,652 steps where the runs wrote something different it is 82.6% (κ = 0.650), the figure we quote",
], M, 4.0, W - 2 * M, { fs: 12, gap: 0.85, itemH: 0.8, lh: 1.3 });
NB(3); footB(); done();

// B4 · paraphrase checklist
slide();
bar("Backup · Is the instrument brittle to phrasing?");
table(M, 1.0, [3.0, 1.9, 2.1, 1.89], [
  { cells: ["Rewrite of the reference", "Steps altered", "Score", "McNemar p"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12, align: ["left", "center", "center", "center"] },
  { cells: ["Verb substitution", "725", "76.8 → 77.0", "1.000"], h: 0.44, fs: 12.5, rule: true },
  { cells: ["Fronting the locative clause", "211", "89.6 → 90.0", "1.000"], h: 0.44, fs: 12.5, rule: true },
  { cells: ["Both at once", "203", "90.1 → 91.1", "0.480"], h: 0.44, fs: 12.5, rule: true },
  { cells: [{ t: "Deleting the locative clause", bold: true, color: RED }, "198", { t: "89.4 → 85.9", bold: true, color: RED }, { t: "0.046", bold: true, color: RED }], h: 0.48, fs: 12.5 },
], { align: ["left", "center", "center", "center"] });
bullets([
  "Pooled over the three meaning-preserving rewrites: 1,139 steps, net +0.35 pp, [−0.59, +1.29], 2.6% of steps changing verdict",
  "Deleting the locative clause does cost, so this is not an inert instrument",
  "The failure is all-or-nothing: the median error is unchanged while p90 moves from 6.88 to 31.16",
  "Declared scope: our rewrites keep the element name verbatim, so we probed phrasing, not the referring expression itself, and the population altered is the easiest quartile",
], M, 3.4, W - 2 * M, { fs: 12, gap: 0.78, itemH: 0.74, lh: 1.3 });
NB(4); footB(); done();

// B5 · floor design
slide();
bar("Backup · How the floor was built, and what it rules out");
table(M, 1.05, [3.3, 3.8, 1.79], [
  { cells: ["Control", "Every sentence replaced by", "Score"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12, align: ["left", "left", "center"] },
  { cells: ["Contentless", "“Tap the button.” at every step", { t: "12.0", bold: true }], h: 0.46, fs: 12.5, rule: true },
  { cells: [{ t: "Wrong screen", bold: true }, "a genuine reference from another step: right register, matched length, wrong content", { t: "6.1", bold: true, color: RED }], h: 0.62, fs: 12.5, rule: true },
  { cells: ["Name removed", "locative clause only, name replaced by “the item”", "61.1"], h: 0.5, fs: 12.5 },
], { align: ["left", "left", "center"] });
bullets([
  "The wrong-screen control scores below the contentless one on disjoint intervals: a wrong sentence actively misleads the instrument where an empty one leaves it to a weak prior",
  "It also disposes of the reading that the metric rewards annotator style, which is exactly what that control preserves",
  "Usable range 62.9 points on a slice whose ceiling is 74.9",
  "Adequacy gate, fixed before any compute: median localisation error ≤ 3% of screen width. Measured 0.7%. The tolerance margin has median 6.2% and 10th percentile 3.6%",
  "Declared weakness: the error distribution is bimodal, so a percentile condition would have been the better gate",
], M, 3.5, W - 2 * M, { fs: 12, gap: 0.66, itemH: 0.62, lh: 1.3 });
NB(5); footB(); done();

// B6 · training configuration
slide();
bar("Backup · Training configuration and cost");
table(M, 1.05, [2.8, 6.09], [
  { cells: ["Item", "Setting"], bold: true, color: WHITE, fill: NAVY, h: 0.4, fs: 12.5 },
  { cells: ["Base model", "Qwen2.5-VL-3B-Instruct"], h: 0.4, fs: 12.5, rule: true },
  { cells: ["Adaptation", "QLoRA, 4-bit NF4, rank 8, α = 16, dropout 0.05, adapters on q,k,v,o,gate,up,down"], h: 0.44, fs: 12, rule: true },
  { cells: ["Frozen", "vision tower and projector; 14,966,784 trainable parameters"], h: 0.4, fs: 12, rule: true },
  { cells: ["Schedule", "context 2560, effective batch 16, lr 1e-4 cosine, two epochs, 8,072 steps"], h: 0.44, fs: 12, rule: true },
  { cells: ["Hardware", "one A100 per run, ≈ 23 h; scoring on 2×T4, ≈ 5.6 h per branch"], h: 0.4, fs: 12, rule: true },
  { cells: ["Inference", "greedy, one sentence per step, descriptor stripped by a fixed regular expression"], h: 0.44, fs: 12 },
]);
bullets([
  "One configuration file serves every branch, with four keys changing: dataset, seed, output directory, dataloader workers",
  "Losses on an L4 and an A100 agree to three digits with identical total_flos, so the hardware is not a variable",
  "The prompt template is byte-identical across branches and between training and inference",
  "Compute budget is the reason the second treatment seed was cancelled, and we report that rather than re-describe the design",
], M, 4.4, W - 2 * M, { fs: 12, gap: 0.68, itemH: 0.64, lh: 1.3 });
NB(6); footB(); done();

// B7 · branch status
slide();
bar("Backup · Status of every registered branch");
table(M, 1.05, [2.7, 1.9, 4.29], [
  { cells: ["Branch", "Status", "Reason"], bold: true, color: WHITE, fill: NAVY, h: 0.42, fs: 12, align: ["left", "center", "left"] },
  { cells: ["S1, two seeds", { t: "run", color: TEAL, bold: true }, "control; gives the seed noise floor of 0.52 pp"], h: 0.46, fs: 11.5, rule: true },
  { cells: ["S2, seed 101", { t: "run", color: TEAL, bold: true }, "exploratory; −1.93 against S1 at the same seed"], h: 0.46, fs: 11.5, rule: true },
  { cells: ["S2, seed 202", { t: "cancelled", color: RED, bold: true }, "compute budget; the registered estimand stays incomplete"], h: 0.46, fs: 11.5, rule: true },
  { cells: ["CE2 and MIN (stage 2)", { t: "run", color: TEAL, bold: true }, "one seed each, labelled exploratory throughout"], h: 0.46, fs: 11.5, rule: true },
  { cells: ["S2r  (false descriptor)", { t: "not run", color: MAROON, bold: true }, "attribution control, dropped with the second seed"], h: 0.46, fs: 11.5, rule: true },
  { cells: ["S2-nopoint", { t: "not run", color: MAROON, bold: true }, "would have tested the descriptor ⇔ touch shortcut"], h: 0.46, fs: 11.5, rule: true },
  { cells: ["MIN on-policy", { t: "stopped at its gate", color: RED, bold: true }, "3.3% usable pairs against a 25% threshold fixed in advance"], h: 0.5, fs: 11.5 },
], { align: ["left", "center", "left"] });
block(M, 4.55, W - 2 * M, 0.9);
text("We mark cancelled branches as registered but not run rather than drop them from the paper.", { x: M + 0.25, y: 4.55, w: W - 2 * M - 0.5, h: 0.9, fontSize: 13, valign: "middle", margin: 0 });
bullets([
  "Twenty-seven amendments, dated and appended, never edited in place; twenty-one of them predate the first executability score",
  "Six later amendments each moved the headroom up and the threshold down; the first also moved against us, cutting the control's share of the ceiling from 84.4% to 78.0%",
], M, 5.6, W - 2 * M, { fs: 12, gap: 0.68, itemH: 0.64, lh: 1.3 });
NB(7); footB(); done();

// B8 · on-policy variant
slide();
bar("Backup · The registered variant stopped by its feasibility check");
bullets([
  "Two negative sources were registered: a heuristic one, the nearest same-role element 80-350 px away, and an on-policy one taking the element the checkpoint itself names when it names the wrong one",
  "The on-policy source was stopped before any training: 14,000 training screens gave 459 usable pairs, 3.3% against a threshold of 25% fixed in advance",
  "The reason is measurable. Over the 3,246 steps carrying a wrong name, the distance from the element named to the element to be touched has quartiles of 70, 351 and 748 px, so the window rejects 76.5% of them",
  "These errors fall into two kinds, the right element under another name or a different region of the screen, and neither is the local confusion an on-policy negative presumes",
  "So the heuristic source does not sample the model's errors so much as construct a neighbour-confusion setting the data rarely contains. We report both because the measurement, not a preference, left one standing",
], M, 1.05, W - 2 * M, { fs: 12.5, gap: 1.08, itemH: 1.04, lh: 1.32 });
NB(8); footB(); done();

// B9 · limitations
slide();
bar("Backup · Limitations, with the numbers attached");
text("Instrument", { x: M, y: 0.9, w: 4.4, h: 0.3, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "The references fail on 1,083 steps, 72% because the grounder lands more than 14% of screen width away; 935 steps defeat all three branches",
  "Below the merge radius the metric is blind: it catches a wrong element named, not a point slightly off inside the right one",
  "Both grounders are Qwen-family, and no human evaluation anchors either",
], M, 1.3, 4.4, { fs: 11.5, gap: 1.1, itemH: 1.05, lh: 1.28 });
text("Data and scope", { x: 5.1, y: 0.9, w: 4.35, h: 0.3, fontSize: 13.5, bold: true, color: NAVY, margin: 0 });
bullets([
  "Held out by task, not by application: 95.6% of attributable applications also occur in training, and 59% of steps cannot be attributed at all, unknown and never read as unseen",
  "17.3% of test references appear verbatim in a 2.6% slice of the training data",
  "Scoring is teacher-forced on context, so absolute scores carry that condition; branch differences do not",
], 5.1, 1.3, 4.35, { fs: 11.5, gap: 1.1, itemH: 1.05, lh: 1.28 });
block(M, 4.75, W - 2 * M, 1.0);
text([{ text: "A system could climb this metric by writing for the grounder rather than for a person.", options: { bold: true, color: RED } }, { text: "  We bound that rather than exclude it: a sentence naming only a screen region scores 89.5% when the region is right and 3.3% when it is wrong.", options: {} }], { x: M + 0.25, y: 4.75, w: W - 2 * M - 0.5, h: 1.0, fontSize: 12.5, valign: "middle", margin: 0, lh: 1.35 });
text("External validity: one screen at a time, English interfaces, one dataset, one 3B base model, one training configuration.", { x: M, y: 5.95, w: W - 2 * M, h: 0.5, fontSize: 12, italic: true, color: GREY, margin: 0, lh: 1.3 });
NB(9); footB(); done();

// B10 · qualitative examples
slide();
bar("Backup · One held-out step from each regime, verbatim");
[["(a)  Identification succeeds, and the prefix pays", "Reference:  “Click on the search icon.”", "S1:  “Click on the text 3.”   — fails", "S2:  <desc>icon button | SEARCH | <point>893,396</point> | the only icon button on screen</desc>  “Click on the search icon.”   — succeeds", TEAL],
 ["(b)  Identification fails, and the prefix binds the sentence to the error", "Reference:  “Click on BMW option on the screen.”", "S1:  “Click on BMW option on the screen.”   — succeeds", "S2:  <desc>item | (no name) | <point>100,294</point> | just below the text “Acura”</desc>  “Click on the first car brand on the screen.”   — fails", RED],
 ["(c)  No descriptor emitted, and the action class is wrong", "Reference:  “click on the Three lines at the top left corner.”", "S1:  “Click on the three lines at the top left corner of the screen.”   — succeeds", "S2:  “Go back to the previous page.”   — fails", MAROON]].forEach((c, i) => {
  const yy = 0.95 + i * 1.85;
  rect(M, yy, W - 2 * M, 1.68, BLOCK, { radius: 0.05 });
  text(c[0], { x: M + 0.18, y: yy + 0.08, w: W - 2 * M - 0.36, h: 0.3, fontSize: 12.5, bold: true, italic: true, color: c[4], margin: 0 });
  text(c[1], { x: M + 0.18, y: yy + 0.42, w: W - 2 * M - 0.36, h: 0.28, fontSize: 11.5, color: GREY, margin: 0 });
  text(c[2], { x: M + 0.18, y: yy + 0.72, w: W - 2 * M - 0.36, h: 0.28, fontSize: 11.5, margin: 0 });
  text(c[3], { x: M + 0.18, y: yy + 1.02, w: W - 2 * M - 0.36, h: 0.6, fontSize: 11, margin: 0, lh: 1.25 });
});
text("The descriptor is stripped before scoring, so only the final sentence is measured. Neither failure is a failure of fluency.", { x: M, y: 6.5, w: W - 2 * M, h: 0.4, fontSize: 12, italic: true, color: NAVY, margin: 0 });
NB(10); footB(); done();

// ---- export ----
done();
pres.writeFile({ fileName: "../FAIR2026_SLIDE.pptx" }).then(() => {
  const html = `<!doctype html><meta charset="utf-8"><title>Preview - FAIR 2026 talk</title>
<style>body{background:#555;margin:0;padding:24px;font-family:sans-serif}
.slide{position:relative;width:960px;height:720px;margin:0 auto 24px;box-shadow:0 3px 14px rgba(0,0,0,.5);overflow:hidden}</style>
${htmlSlides.join("\n")}`;
  fs.mkdirSync("_preview", { recursive: true });
  fs.writeFileSync("_preview/preview_fair.html", html);
  console.log("Done: ../FAIR2026_SLIDE.pptx  |  main: " + PAGE + "  |  backup: " + BPAGE);
});
