// SOICT 2026 talk deck (GUIStep, paper 5590), following slides/KICH_BAN_SOICT_15_11.md.
// 13 main slides + Thank-you + 7 backup slides. 16:9, same visual family as the VCL deck
// (indigo title bar, rounded grey blocks, Cambria).
// On-slide text comes from "On the slide"; speaker notes are read verbatim from "Say" at build
// time (the "(ý chính …)" line is kept at the end of the notes as a Vietnamese reminder).
// Backup numbers come from paper/soict2026/guistep/camera_ready_5590/Source/main.tex.
// Output: ../SOICT2026_SLIDE.pptx
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..", "..");
const KB = fs.readFileSync(path.join(__dirname, "..", "KICH_BAN_SOICT_15_11.md"), "utf8");
const FIG1 = path.join(ROOT, "paper", "soict2026", "guistep", "camera_ready_5590", "Source", "fig1_screen.png");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Uyen Le Doan Phuong";
pres.title = "GUIStep - SOICT 2026";

const TF = "Cambria", MONO = "Consolas";
const NAVY = "322164", INK = "1A1A1A", BLOCK = "ECEBF0", TEAL = "006666", RED = "B22222";
const GREY = "5A5A66", WHITE = "FFFFFF", LIGHT = "B9B3CC", SOFT = "9A94AE", AMBER = "C77700";
const FOOTA = "191132", FOOTB = "25194B", FOOTC = "4F417A";
const W = 13.333, H = 7.5, M = 0.6;

// ---------- notes from the script ----------
function clean(t) {
  return t.replace(/\*\*/g, "").replace(/`/g, "")
    .split(/\n\s*\n/).map(p => p.replace(/\s*\n\s*/g, " ").trim()).filter(Boolean).join("\n\n");
}
const SAY = {};
KB.split(/\n## Slide /).slice(1).forEach(sec => {
  const n = parseInt(sec, 10);
  const m = sec.match(/\*\*Say:\*\*\n([\s\S]*?)(?:\n---|$)/);
  if (m) SAY[n] = clean(m[1].replace(/^\*\((ý chính:[\s\S]*?)\)\*\s*$/m, "($1)"));
});
function QA(code) {
  const re = new RegExp("\\*\\*" + code + "[ ⭐]*\\.\\s*([^\\n]*?)\\*\\*\\n([\\s\\S]*?)(?=\\n\\n)");
  const m = KB.match(re);
  if (!m) throw new Error("missing " + code);
  return "For question " + code + ": " + m[1].trim() + "\n\n" + clean(m[2].replace(/\*\((VN:[\s\S]*?)\)\*/, "($1)"));
}

// ---------- helpers ----------
let s, PAGE = 0, BPAGE = 0;
const TOTAL = 14;
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
  s.addShape(o.radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, p);
}
function block(x, y, w, h, fill, line) { rect(x, y, w, h, fill || BLOCK, { radius: 0.08, line }); }
function hline(x, y, w, c, lw) { s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: c || LIGHT, width: lw || 1 } }); }
function vline(x, y, h, c, lw, dash) { s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color: c || LIGHT, width: lw || 1, dashType: dash || "solid" } }); }
function arrow(x1, y1, x2, y2, c) {
  const o = { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), line: { color: c || NAVY, width: 2, endArrowType: "triangle" } };
  if (x2 < x1) o.flipH = true;
  if (y2 < y1) o.flipV = true;
  s.addShape(pres.shapes.LINE, o);
}
function bar(t) {
  rect(0, 0, W, 0.9, NAVY);
  text(t, { x: M, y: 0, w: W - 2 * M, h: 0.9, fontSize: 26, bold: true, color: WHITE, valign: "middle" });
}
function footRow(label) {
  const yy = H - 0.32, hh = 0.32;
  rect(0, yy, 5.0, hh, FOOTA); rect(5.0, yy, 6.3, hh, FOOTB); rect(11.3, yy, W - 11.3, hh, FOOTC);
  const o = { y: yy, h: hh, fontSize: 11, color: WHITE, align: "center", valign: "middle" };
  text("Uyen Le Doan Phuong", Object.assign({ x: 0, w: 5.0 }, o));
  text("SOICT 2026 · GUIStep", Object.assign({ x: 5.0, w: 6.3 }, o));
  text(label, Object.assign({ x: 11.3, w: W - 11.3 }, o));
}
function foot() { PAGE++; footRow(`${PAGE}/${TOTAL}`); }
function footB() { BPAGE++; footRow(`B${BPAGE}`); }
function note(t) { s.addNotes(t); }
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
function box(x, y, w, h, t, o) {
  o = o || {};
  rect(x, y, w, h, o.fill || BLOCK, { radius: 0.08, line: o.line || SOFT, lw: 1 });
  text(t, { x: x + 0.05, y, w: w - 0.1, h, fontSize: o.fs || 14, align: "center", valign: "middle", bold: o.bold, color: o.color || INK, fontFace: o.mono ? MONO : TF, lh: 1.0 });
}

// ══════════ 1 · TITLE ══════════
slide();
rect(0, 0, W, 0.75, NAVY);
text("SOICT 2026", { x: 0, y: 0, w: W, h: 0.75, fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle" });
rect(0.9, 1.35, W - 1.8, 2.5, NAVY, { radius: 0.1 });
text("GUIStep", { x: 1.2, y: 1.55, w: W - 2.4, h: 0.95, fontSize: 44, bold: true, color: WHITE, align: "center", valign: "middle" });
text("A Compact Vision-Language Model for\nGUI Step Instruction Generation", { x: 1.2, y: 2.5, w: W - 2.4, h: 1.15, fontSize: 26, color: WHITE, align: "center", valign: "middle", lh: 1.05 });
text("Uyen Le Doan Phuong", { x: 0.9, y: 4.3, w: W - 1.8, h: 0.55, fontSize: 26, bold: true, align: "center" });
text("Faculty of Information Technology\nUniversity of Science, VNU-HCM", { x: 0.9, y: 4.95, w: W - 1.8, h: 0.9, fontSize: 19, color: GREY, align: "center", lh: 1.1 });
text("SOICT 2026", { x: 0.9, y: 6.05, w: W - 1.8, h: 0.5, fontSize: 20, bold: true, color: TEAL, align: "center" });
note(SAY[1]); foot();

// ══════════ 2 · THE TASK (Figure 1) ══════════
slide();
bar("The task: write the next step for a person");
text([{ text: "Agents: ", options: { bold: true, color: GREY } }, { text: "sentence → action.      ", options: { color: GREY } },
      { text: "GUIStep: ", options: { bold: true, color: NAVY } }, { text: "screen + goal → sentence for a person.", options: { color: NAVY } }],
  { x: M, y: 1.0, w: W - 2 * M, h: 0.5, fontSize: 20, align: "center", valign: "middle" });
block(M, 1.62, W - 2 * M, 1.1);
text([{ text: "Goal. ", options: { bold: true } }, { text: "I travel with Aer Lingus Airlines regularly and like their service, so look up the flight details in the booking.com app and sort by the cheapest direct flight", options: {} },
      { text: "\nPrevious steps. ", options: { bold: true, breakLine: false } }, { text: "Click on the airlines option at the top of the screen → Click on Aer Lingus option → Click on done option", options: {} }],
  { x: M + 0.2, y: 1.62, w: W - 2 * M - 0.4, h: 1.1, fontSize: 13.5, valign: "middle", lh: 1.05 });
{
  const ih = 4.25, iw = ih * 720 / 736, ix = M, iy = 2.85;
  s.addImage({ path: FIG1, x: ix, y: iy, w: iw, h: ih });
  rect(ix, iy, iw, ih, "none", { line: SOFT, lw: 1 });
  const cx = ix + 0.142 * iw, cy = iy + 0.332 * ih, r = 0.0879 * iw;
  s.addShape(pres.shapes.OVAL, { x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, fill: { type: "none" }, line: { color: RED, width: 2.5 } });
  const my = iy + ih / 2;
  arrow(ix + iw + 0.15, my, ix + iw + 0.8, my);
  box(ix + iw + 0.85, my - 0.55, 2.0, 1.1, "GUIStep", { fs: 22, bold: true, color: NAVY, fill: BLOCK });
  arrow(ix + iw + 2.9, my, ix + iw + 3.55, my);
  const tx = ix + iw + 3.65, tw = W - M - tx;
  text([{ text: "generated\n", options: { bold: true, color: TEAL } }, { text: "“Click on the sort by option”", options: { italic: true } }],
    { x: tx, y: my - 1.35, w: tw, h: 1.1, fontSize: 19, valign: "bottom", lh: 1.05 });
  text([{ text: "reference\n", options: { bold: true, color: GREY } }, { text: "“Click on sort by option at the top left of the screen”", options: { italic: true } }],
    { x: tx, y: my + 0.15, w: tw, h: 1.3, fontSize: 19, lh: 1.05 });
}
note(SAY[2]); foot();

// ══════════ 3 · WHY IT IS HARD TO EVALUATE ══════════
slide();
bar("One button, many correct sentences");
box(M, 1.3, 5.0, 0.9, "“Click on the search bar”", { fs: 20, fill: WHITE });
box(M, 2.55, 5.0, 0.9, "“Tap the magnifying glass at the top”", { fs: 20, fill: WHITE });
arrow(M + 5.05, 1.75, 6.75, 2.3); arrow(M + 5.05, 3.0, 6.75, 2.55);
// magnifying-glass button
rect(6.85, 1.85, 1.15, 1.15, NAVY, { radius: 0.12 });
s.addShape(pres.shapes.OVAL, { x: 7.08, y: 2.03, w: 0.55, h: 0.55, fill: { type: "none" }, line: { color: WHITE, width: 4 } });
s.addShape(pres.shapes.LINE, { x: 7.56, y: 2.52, w: 0.26, h: 0.26, line: { color: WHITE, width: 5 } });
[["97.5%", "of valid rewordings rejected by word overlap", "(small pilot)"],
 ["0.336", "AUC of embedding similarity", "below chance 0.5"],
 ["0.76 > 0.55", "cosine: inbox / outbox  vs\nsearch / magnifying glass", ""]].forEach((c, i) => {
  const x = M + i * 4.1;
  block(x, 3.95, 3.85, 2.85);
  text(c[0], { x, y: 4.1, w: 3.85, h: 1.0, fontSize: i === 2 ? 38 : 46, bold: true, color: RED, align: "center", valign: "middle" });
  text(c[1], { x: x + 0.2, y: 5.15, w: 3.45, h: 0.95, fontSize: 17, align: "center", lh: 1.05 });
  if (c[2]) text(c[2], { x: x + 0.2, y: 6.1, w: 3.45, h: 0.5, fontSize: 14, italic: true, color: GREY, align: "center" });
});
note(SAY[3]); foot();

// ══════════ 4 · EXECUTABILITY ══════════
slide();
bar("Our score: executability");
box(M, 1.45, 3.4, 1.3, "generated sentence\n+ screenshot", { fs: 19 });
arrow(M + 3.45, 2.1, M + 4.25, 2.1);
box(M + 4.3, 1.45, 3.6, 1.3, "frozen listener\nUGround-V1-2B", { fs: 19, bold: true, color: WHITE, fill: NAVY, line: NAVY });
arrow(M + 7.95, 2.1, M + 8.75, 2.1);
box(M + 8.8, 1.45, 3.33, 1.3, "point", { fs: 22, bold: true, color: RED });
[["(i)", "action class matches"], ["(ii)", "no polarity inversion\n(enable vs disable)"], ["(iii)", "point inside the target box\n(AndroidControl App. D.3)"]].forEach((c, i) => {
  const x = M + i * 4.1;
  block(x, 3.25, 3.85, 1.85, "E6F0EF");
  text(c[0], { x, y: 3.35, w: 3.85, h: 0.5, fontSize: 22, bold: true, color: TEAL, align: "center" });
  text(c[1], { x: x + 0.15, y: 3.9, w: 3.55, h: 1.1, fontSize: 18, align: "center", lh: 1.05 });
});
rect(M, 5.55, W - 2 * M, 0.95, NAVY, { radius: 0.08 });
text("Executability = share of steps passing all three", { x: M, y: 5.55, w: W - 2 * M, h: 0.95, fontSize: 25, bold: true, color: WHITE, align: "center", valign: "middle" });
note(SAY[4]); foot();

// ══════════ 5 · CHECKING THE SCORE ══════════
slide();
bar("Checking the score");
table(M, 1.3, [5.4, 1.5], [
  { cells: ["sentence given to listener", { t: "D.3", align: "right" }], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: ["human reference (ceiling)", { t: "83.0", bold: true, color: TEAL }], h: 0.65 },
  { cells: ["“Tap the button.”", "14.1"], h: 0.65 },
  { cells: ["reference from a different screen", "8.6"], h: 0.65 },
  { cells: [{ t: "usable range", bold: true }, { t: "68.9", bold: true, color: TEAL }], h: 0.65, rule: false },
], { fs: 19, align: ["left", "right"] });
block(7.65, 1.3, 5.08, 3.2);
[["−34.2 pts", "delete element name"], ["−4.1 pts", "delete position"], ["−0.09", "1,139 verb/word-order rewrites"]].forEach((c, i) => {
  const yy = 1.45 + i * 0.98;
  text(c[0], { x: 7.85, y: yy, w: 2.0, h: 0.9, fontSize: 24, bold: true, color: i === 0 ? RED : NAVY, valign: "middle" });
  text(c[1], { x: 9.9, y: yy, w: 2.7, h: 0.9, fontSize: 17, valign: "middle", lh: 1.05 });
});
block(M, 5.0, W - 2 * M, 1.4, "FFF4E5");
text("Injection suite: passes 6/10 under D.3 (8/10 under stricter Voronoi).\nWeak on neighbouring elements.", { x: M + 0.3, y: 5.0, w: W - 2 * M - 0.6, h: 1.4, fontSize: 19, valign: "middle", lh: 1.15 });
note(SAY[5]); foot();

// ══════════ 6 · OTHER LISTENERS ══════════
slide();
bar("The ranking holds with other listeners");
[["Stricter Voronoi rule", "same ranking of all 5 systems", "same"],
 ["UI-Venus-Ground-7B", "not trained on AndroidControl\nS − backbone", "+11.14 → +11.02"],
 ["Phi-4-multimodal", "other model family, multiple choice\nS − backbone", "+6.4 [+5.1, +7.7]"]].forEach((c, i) => {
  const yy = 1.3 + i * 1.8;
  block(M, yy, W - 2 * M, 1.6);
  text(c[0], { x: M + 0.3, y: yy, w: 4.0, h: 1.6, fontSize: 22, bold: true, color: NAVY, valign: "middle" });
  text(c[1], { x: M + 4.4, y: yy, w: 3.9, h: 1.6, fontSize: 17, valign: "middle", lh: 1.1 });
  text(c[2], { x: M + 8.3, y: yy, w: 3.6, h: 1.6, fontSize: i === 0 ? 30 : 28, bold: true, color: TEAL, align: "right", valign: "middle" });
});
note(SAY[6]); foot();

// ══════════ 7 · GUIStep (Figure 2 + configurations) ══════════
slide();
bar("GUIStep: supervision without new labels");
{
  const y0 = 1.1, fs = 12.5;
  box(M, y0 + 0.45, 1.95, 1.45, "recorded step\nscreenshot, goal,\nhistory, instruction,\ntouch point, UI tree", { fs: 11.5 });
  const mids = [["sentence target", y0], ["declaration by rule", y0 + 0.68], ["preference pair:\ntarget vs. competitor", y0 + 1.36]];
  mids.forEach(m => {
    box(3.05, m[1], 2.55, 0.58, m[0], { fs, fill: WHITE });
    arrow(M + 1.97, y0 + 1.17, 3.03, m[1] + 0.29);
    arrow(5.62, m[1] + 0.29, 6.28, y0 + 1.17);
  });
  box(6.3, y0 + 0.62, 1.75, 1.1, "VLM adaptation\nS, D or P", { fs, bold: true });
  arrow(8.07, y0 + 1.17, 8.37, y0 + 1.17);
  box(8.4, y0 + 0.77, 1.35, 0.8, "generated\nsentence", { fs, fill: WHITE });
  arrow(9.77, y0 + 1.17, 10.07, y0 + 1.17);
  box(10.1, y0 + 0.77, 1.05, 0.8, "frozen\nlistener", { fs, bold: true, color: WHITE, fill: NAVY, line: NAVY });
  arrow(11.17, y0 + 1.17, 11.42, y0 + 1.17);
  box(11.45, y0 + 0.62, 1.28, 1.1, "point in box,\naction class?", { fs: 11.5, fill: WHITE });
}
table(M, 3.25, [2.15, 6.95, 3.03], [
  { cells: ["", "training target", "objective"], bold: true, color: WHITE, fill: NAVY, h: 0.45, fs: 16 },
  { cells: [{ t: "GUIStep-S", bold: true }, "sentence", "cross-entropy"], h: 0.45 },
  { cells: [{ t: "GUIStep-D", bold: true }, "declaration, then sentence", "cross-entropy"], h: 0.45 },
  { cells: [{ t: "GUIStep-P", bold: true, color: TEAL }, "preferred vs rejected declaration, same sentence", { t: "ORPO", bold: true, color: TEAL }], h: 0.45 },
  { cells: [{ t: "control", italic: true }, "same as P, no rejected", "cross-entropy"], h: 0.45, rule: false },
], { fs: 16 });
block(M, 5.75, W - 2 * M, 0.75);
text("<desc>item | Close | <point>274,285</point> | just below \"3:09\"</desc>", { x: M, y: 5.75, w: W - 2 * M, h: 0.75, fontSize: 18, fontFace: MONO, color: NAVY, align: "center", valign: "middle" });
note(SAY[7]); foot();

// ══════════ 8 · MAIN RESULTS (horizontal bars) ══════════
slide();
bar("Main results: executability (D.3), 4,463 touch steps");
{
  const rows = [["untuned 3B backbone", 53.6, SOFT], ["Qwen2.5-VL-7B, prompted", 57.7, SOFT], ["select-then-verbalise variant", 62.4, SOFT],
    ["GUIStep-D", 63.6, NAVY], ["GUIStep-S", 65.5, NAVY], ["control", 66.0, NAVY], ["GUIStep-P", 66.5, TEAL], ["human reference", 83.8, AMBER]];
  const lx = M, lw = 3.6, bx = M + 3.7, bwMax = 5.4, vmax = 90, y0 = 1.2, rh = 0.62;
  rows.forEach((r, i) => {
    const yy = y0 + i * rh, best = r[0] === "GUIStep-P";
    text(r[0], { x: lx, y: yy, w: lw, h: rh, fontSize: 17, bold: best, color: r[0] === "human reference" ? AMBER : INK, align: "right", valign: "middle" });
    rect(bx, yy + 0.1, bwMax * r[1] / vmax, rh - 0.2, r[2]);
    text(r[1].toFixed(1), { x: bx + bwMax * r[1] / vmax + 0.08, y: yy, w: 0.9, h: rh, fontSize: 17, bold: best || r[0] === "human reference", color: r[2] === SOFT ? GREY : r[2], valign: "middle" });
  });
  vline(bx, y0, rows.length * rh, GREY, 1.25);
  block(10.3, 2.2, 2.43, 2.6, "E6F0EF");
  text("P − backbone", { x: 10.4, y: 2.35, w: 2.23, h: 0.45, fontSize: 17, bold: true, color: TEAL, align: "center" });
  text("+13.0", { x: 10.4, y: 2.8, w: 2.23, h: 0.9, fontSize: 40, bold: true, color: TEAL, align: "center", valign: "middle" });
  text("[+11.5, +14.4]\np < 0.001", { x: 10.4, y: 3.75, w: 2.23, h: 0.9, fontSize: 16, align: "center", lh: 1.1 });
}
note(SAY[8]); foot();

// ══════════ 9 · ABLATION (CI chart) ══════════
slide();
bar("Ablation: where the gain comes from");
{
  const rows = [["D − S", -1.9, -3.0, -0.7, "−1.9 [−3.0, −0.7]  p = 0.003", RED],
    ["P − S", 1.05, -0.11, 2.20, "+1.05 [−0.11, +2.20]  p = 0.073 (n.s.)", GREY],
    ["P − control", 0.52, 0.02, 1.00, "+0.52 [+0.02, +1.00]  p = 0.043", TEAL]];
  const ax = 2.9, aw = 5.4, vmin = -3.5, vmax = 2.5, y0 = 1.45, rh = 1.05;
  const X = v => ax + aw * (v - vmin) / (vmax - vmin);
  // axis
  const ay = y0 + rows.length * rh + 0.1;
  hline(ax, ay, aw, GREY, 1.25);
  [-3, -2, -1, 0, 1, 2].forEach(v => {
    vline(X(v), ay, 0.08, GREY, 1);
    text((v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v), { x: X(v) - 0.3, y: ay + 0.1, w: 0.6, h: 0.35, fontSize: 14, color: GREY, align: "center" });
  });
  vline(X(0), y0 - 0.15, rows.length * rh + 0.25, GREY, 1.25, "dash");
  rows.forEach((r, i) => {
    const yy = y0 + i * rh + rh / 2;
    text(r[0], { x: M, y: yy - 0.35, w: 2.15, h: 0.7, fontSize: 21, bold: true, color: NAVY, align: "right", valign: "middle" });
    hline(X(r[2]), yy, X(r[3]) - X(r[2]), r[5], 4);
    vline(X(r[2]), yy - 0.15, 0.3, r[5], 2.5); vline(X(r[3]), yy - 0.15, 0.3, r[5], 2.5);
    s.addShape(pres.shapes.OVAL, { x: X(r[1]) - 0.11, y: yy - 0.11, w: 0.22, h: 0.22, fill: { color: r[5] }, line: { color: r[5] } });
    text(r[4], { x: 8.55, y: yy - 0.35, w: 4.2, h: 0.7, fontSize: 16, color: r[5] === GREY ? INK : r[5], bold: r[5] !== GREY, valign: "middle" });
  });
}
block(M, 5.35, W - 2 * M, 1.15);
text("Control recovers 2.4 of the 2.9 points P gains over D.\nSecond seed of S: 66.1 (+0.6).", { x: M + 0.3, y: 5.35, w: W - 2 * M - 0.6, h: 1.15, fontSize: 19, valign: "middle", lh: 1.15 });
note(SAY[9]); foot();

// ══════════ 10 · REPEATED VS UNSEEN ══════════
slide();
bar("Repeated vs unseen sentences");
table(M + 0.9, 1.5, [3.4, 3.4, 3.4], [
  { cells: ["", { t: "repeated (2,347)", align: "right" }, { t: "unseen (2,116)", align: "right" }], bold: true, color: WHITE, fill: NAVY, h: 0.7 },
  { cells: ["S − backbone", "+15.0", { t: "+8.4", bold: true, color: TEAL }], h: 0.9 },
  { cells: ["P − S", "+0.3 (p = 0.75)", "+1.9 (p = 0.031)"], h: 0.9, rule: false },
], { fs: 22, align: ["left", "right", "right"] });
block(M, 4.9, W - 2 * M, 1.2);
text("52.6% of test references equal a training sentence (after lower-casing).", { x: M + 0.3, y: 4.9, w: W - 2 * M - 0.6, h: 1.2, fontSize: 20, align: "center", valign: "middle" });
note(SAY[10]); foot();

// ══════════ 11 · TEXT METRICS AND ERRORS ══════════
slide();
bar("Text metrics and errors");
table(M, 1.3, [2.05, 1.35, 1.35, 1.45, 1.6], [
  { cells: ["", "BLEU-4", "SPICE", "ROUGE-L", "BERTScore"], bold: true, color: WHITE, fill: NAVY, h: 0.6, fs: 15 },
  { cells: ["backbone", "15.3", "18.5", "42.3", "40.1"], h: 0.65 },
  { cells: ["S", { t: "51.6", bold: true }, { t: "44.4", bold: true }, "67.3", "66.3"], h: 0.65 },
  { cells: ["D", "48.7", "41.3", "66.0", "65.1"], h: 0.65 },
  { cells: ["P", "49.9", "42.2", { t: "68.5", bold: true }, { t: "66.7", bold: true }], h: 0.65, rule: false },
], { fs: 18, align: ["left", "right", "right", "right", "right"] });
block(8.85, 1.3, 3.88, 3.2);
text("P fails on 1,493 steps", { x: 9.0, y: 1.4, w: 3.58, h: 0.5, fontSize: 18, bold: true, color: NAVY, align: "center" });
text("96.3%", { x: 9.0, y: 1.9, w: 3.58, h: 1.0, fontSize: 46, bold: true, color: RED, align: "center", valign: "middle" });
text("fail localisation\n50 wrong action · 5 polarity", { x: 9.0, y: 2.95, w: 3.58, h: 1.0, fontSize: 17, align: "center", lh: 1.1 });
block(M, 5.0, W - 2 * M, 1.4, WHITE, SOFT);
text([{ text: "select minutes 00", options: { fontFace: MONO, color: RED, bold: true } }, { text: "      vs ref      ", options: { color: GREY } }, { text: "click on the OK option", options: { fontFace: MONO, color: NAVY } }],
  { x: M + 0.3, y: 5.0, w: W - 2 * M - 0.6, h: 1.4, fontSize: 21, align: "center", valign: "middle" });
note(SAY[11]); foot();

// ══════════ 12 · LIMITATIONS ══════════
slide();
bar("Limitations");
["Score not validated against human judgement; fails 4/10 injection criteria (neighbouring elements)",
 "One dataset (AndroidControl, English), one backbone, touch steps only",
 "D, P, control: one seed each",
 "90% of test tasks are in AndroidControl's official training split; history = reference instructions"].forEach((t, i) => {
  const yy = 1.3 + i * 1.3;
  block(M, yy, W - 2 * M, 1.12);
  rect(M, yy, 0.14, 1.12, i === 0 ? RED : AMBER);
  text(t, { x: M + 0.45, y: yy, w: W - 2 * M - 0.7, h: 1.12, fontSize: 20, valign: "middle", lh: 1.05 });
});
note(SAY[12]); foot();

// ══════════ 13 · CONCLUSION ══════════
slide();
bar("Conclusion");
[["+13.0", "Records already in a GUI dataset are enough to train a compact instruction writer: points over the backbone"],
 ["listener", "A frozen listener can score such sentences without listing valid wordings (with known gaps)"],
 ["sentence", "Most of the gain comes from learning the sentence; declaration + preference add little"]].forEach((c, i) => {
  const yy = 1.3 + i * 1.5;
  block(M, yy, W - 2 * M, 1.3);
  text(c[0], { x: M + 0.25, y: yy, w: 2.7, h: 1.3, fontSize: i === 0 ? 40 : 26, bold: true, color: TEAL, valign: "middle" });
  text(c[1], { x: M + 3.1, y: yy, w: 8.8, h: 1.3, fontSize: 20, valign: "middle", lh: 1.08 });
});
text("Next: a second dataset, human evaluation, rewards that act on the sentence itself.", { x: M, y: 5.95, w: W - 2 * M, h: 0.55, fontSize: 18, italic: true, color: GREY, align: "center" });
note(SAY[13]); foot();

// ══════════ 14 · THANK YOU ══════════
slide();
rect(0, 0, W, H - 0.32, NAVY);
text("Thank you", { x: M, y: 2.2, w: W - 2 * M, h: 1.3, fontSize: 54, bold: true, color: WHITE, align: "center", valign: "middle" });
text("24C15039@student.hcmus.edu.vn", { x: M, y: 3.8, w: W - 2 * M, h: 0.6, fontSize: 22, fontFace: MONO, color: LIGHT, align: "center", valign: "middle" });
foot();

// ══════════════════ BACKUP ══════════════════
// B1 · validation table (Table 3)
slide();
bar("Backup · Validation of the listener (Table 3)");
{
  const R = (a, b, c, d, e, fail) => ({ cells: [{ t: a, bold: fail }, b, c, d, { t: e, bold: fail, color: fail ? RED : TEAL }], h: 0.43 });
  table(M, 1.1, [5.4, 2.0, 1.45, 1.45, 1.83], [
    { cells: ["check", "threshold", "D.3", "Voronoi", "D.3 verdict"], bold: true, color: WHITE, fill: NAVY, h: 0.48, fs: 15 },
    { cells: ["median localisation error of the listener", "≤ 3% of width", { t: "0.7% (n = 300)", align: "center" }, "", { t: "pass", color: TEAL }], h: 0.43 },
    R("false rejection of paraphrases", "≤ 10%", "6.5%", "0.0%", "pass"),
    R("false rejection under the action check", "≤ 15%", "0.0%", "0.0%", "pass"),
    R("false rejection by the polarity check", "≤ 5%", "0.0%", "0.0%", "pass"),
    R("catching a wrong action class", "≥ 80%", "100.0%", "100.0%", "pass"),
    R("catching wrong content", "≥ 90%", "91.1%", "91.1%", "pass"),
    R("catching a wrong scroll direction", "≥ 90%", "100.0%", "100.0%", "pass"),
    R("catching a neighbouring element (30 to 80 px)", "≥ 80%", "25.6%", "33.1%", "fail", true),
    R("catching a nearby element (80 to 150 px)", "≥ 90%", "82.0%", "99.6%", "fail", true),
    R("catching a distant element (≥ 25% of width)", "≥ 95%", "94.5%", "100.0%", "fail", true),
    Object.assign(R("catching negation absent from the table", "≥ 50%", "20.0%", "20.0%", "fail", true), { rule: false }),
  ], { fs: 15, align: ["left", "left", "right", "right", "center"] });
  text("Thresholds fixed before either run; same 398 steps and seed.", { x: M, y: 6.45, w: W - 2 * M, h: 0.4, fontSize: 15, italic: true, color: GREY, align: "center" });
}
note(QA("A3")); footB();

// B2 · rule choice (Table 2)
slide();
bar("Backup · Choosing the localisation rule (Table 2)");
table(M, 1.35, [5.6, 2.15, 2.15, 2.23], [
  { cells: ["sentence given to the listener", "D.3", "Voronoi", "window ±14%"], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: ["reference instruction (ceiling)", "83.0", "74.9", "83.0"], h: 0.62 },
  { cells: ["“Tap the button.”", "14.1", "12.0", "20.5"], h: 0.62 },
  { cells: ["reference of a different screen", "8.6", "6.1", "12.8"], h: 0.62 },
  { cells: ["element name deleted, position kept", "74.8", "68.0", "78.9"], h: 0.62 },
  { cells: [{ t: "usable range", bold: true }, { t: "68.9", bold: true, color: TEAL }, "62.9", "62.5"], h: 0.62, rule: false },
], { fs: 19, align: ["left", "right", "right", "right"] });
text("One random slice of 800 steps. Usable range = ceiling minus the generic sentence.", { x: M, y: 5.4, w: W - 2 * M, h: 0.5, fontSize: 16, italic: true, color: GREY, align: "center" });
note(QA("A4")); footB();

// B3 · other listeners in detail
slide();
bar("Backup · Listener checks in detail");
block(M, 1.2, 5.95, 2.4);
text("UI-Venus-Ground-7B", { x: M + 0.25, y: 1.3, w: 5.5, h: 0.5, fontSize: 20, bold: true, color: NAVY });
text("not trained on AndroidControl · 2,532 steps\nS − backbone: +11.14 (UGround) → +11.02 (UI-Venus)\nretains 99% of the gap", { x: M + 0.25, y: 1.85, w: 5.5, h: 1.6, fontSize: 16, lh: 1.15 });
block(6.78, 1.2, 5.95, 2.4);
text("Phi-4-multimodal (Set-of-Mark)", { x: 7.03, y: 1.3, w: 5.5, h: 0.5, fontSize: 20, bold: true, color: NAVY });
text("median 15 boxes per screen · 95.7% coverage\nreference 54.9 · S 44.6 · backbone 38.2\nS − backbone +6.4 [+5.1, +7.7], p < 0.001", { x: 7.03, y: 1.85, w: 5.5, h: 1.6, fontSize: 16, lh: 1.15 });
text("Voronoi rule, all 4,463 steps", { x: M, y: 3.9, w: W - 2 * M, h: 0.5, fontSize: 20, bold: true, color: NAVY });
table(M, 4.45, [2.0, 2.0, 2.0, 2.0, 2.0, 2.13], [
  { cells: ["backbone", "GUIStep-D", "GUIStep-S", "control", "GUIStep-P", "reference"], bold: true, color: WHITE, fill: NAVY, h: 0.55, fs: 16 },
  { cells: ["47.6", "57.2", "59.1", "59.4", { t: "60.0", bold: true, color: TEAL }, "75.7"], h: 0.65, rule: false },
], { fs: 20, align: ["center", "center", "center", "center", "center", "center"] });
text("S − backbone under Voronoi: +11.5 [+10.0, +13.1]. Other listeners were not run on P or the control.", { x: M, y: 5.95, w: W - 2 * M, h: 0.5, fontSize: 15, italic: true, color: GREY, align: "center" });
note(QA("A2")); footB();

// B4 · text metrics (Table 5)
slide();
bar("Backup · Reference-overlap metrics (Table 5)");
table(M, 1.35, [2.6, 1.35, 1.35, 1.4, 1.45, 1.3, 1.3, 1.38], [
  { cells: ["", "BLEU-4", "METEOR", "ROUGE-L", "CIDEr-D", "SPICE", "chrF", "BERTScore"], bold: true, color: WHITE, fill: NAVY, h: 0.6, fs: 15 },
  { cells: ["untuned backbone", "15.3", "24.6", "42.3", "88.0", "18.5", "40.2", "40.1"], h: 0.62 },
  { cells: ["GUIStep-S", { t: "51.6", bold: true }, "36.8", "67.3", { t: "416.1", bold: true }, { t: "44.4", bold: true }, "61.3", "66.3"], h: 0.62 },
  { cells: ["GUIStep-D", "48.7", "35.8", "66.0", "387.7", "41.3", "59.9", "65.1"], h: 0.62 },
  { cells: ["GUIStep-P", "49.9", { t: "37.3", bold: true }, { t: "68.5", bold: true }, "401.0", "42.2", { t: "61.8", bold: true }, { t: "66.7", bold: true }], h: 0.62 },
  { cells: [{ t: "reference", italic: true }, "100.0", "100.0", "100.0", "988.7", "98.6", "100.0", "100.0"], h: 0.62, rule: false, color: GREY },
], { fs: 17, align: ["left", "right", "right", "right", "right", "right", "right", "right"] });
text("4,463 steps, one reference per step. CIDEr-D exceeds 100 and is comparable only within this table.", { x: M, y: 5.4, w: W - 2 * M, h: 0.5, fontSize: 16, italic: true, color: GREY, align: "center" });
note(QA("A1")); footB();

// B5 · training details
slide();
bar("Backup · Training details");
[["Backbone", "Qwen2.5-VL-3B-Instruct, 4-bit NF4 QLoRA, LLaMA-Factory"],
 ["LoRA", "rank 8, scale 16, dropout 0.05, seven decoder projections"],
 ["Frozen", "vision tower and projector; context length 2,560"],
 ["S and D", "2 epochs = 8,072 updates, batch 16, lr 1e-4, cosine, 5% warm-up"],
 ["P (ORPO)", "β = 0.1, 800 updates, lr 2e-5; control: same updates, preferred outputs only"],
 ["Inference", "greedy decoding"]].forEach((c, i) => {
  const yy = 1.25 + i * 0.85;
  block(M, yy, W - 2 * M, 0.72);
  text(c[0], { x: M + 0.25, y: yy, w: 2.4, h: 0.72, fontSize: 19, bold: true, color: TEAL, valign: "middle" });
  text(c[1], { x: M + 2.7, y: yy, w: 9.3, h: 0.72, fontSize: 18, valign: "middle" });
});
note(QA("B3")); footB();

// B6 · prompt (Appendix A)
slide();
bar("Backup · Generation prompt (Appendix A)");
block(M, 1.2, W - 2 * M, 1.15);
text([{ text: "System. ", options: { bold: true, color: NAVY } }, { text: "“You look at a phone screenshot and write ONE short English instruction for the user that says where to touch in order to continue.”", options: { italic: true } }],
  { x: M + 0.25, y: 1.2, w: W - 2 * M - 0.5, h: 1.15, fontSize: 17, valign: "middle", lh: 1.1 });
block(M, 2.6, W - 2 * M, 2.4, WHITE, SOFT);
text("[image]\nGoal: <goal>\nDone so far: <step 1> → <step 2> → <step 3>\nText read on the screen: <OCR 1> · <OCR 2> · ...\nWrite the instruction for the next step.",
  { x: M + 0.4, y: 2.6, w: W - 2 * M - 0.8, h: 2.4, fontSize: 18, fontFace: MONO, color: NAVY, valign: "middle", lh: 1.2 });
text("History = last three reference instructions · at most 24 OCR detections (RapidOCR, confidence ≥ 0.5).\nThe listener sees only the screenshot and the generated sentence.", { x: M, y: 5.25, w: W - 2 * M, h: 0.9, fontSize: 16, italic: true, color: GREY, align: "center", lh: 1.15 });
footB();

// B7 · repeated / unseen (Table 4)
slide();
bar("Backup · Repeated and unseen sentences (Table 4)");
table(M + 0.5, 1.25, [3.0, 4.3, 4.3], [
  { cells: ["", "repeated (n = 2,347)", "unseen (n = 2,116)"], bold: true, color: WHITE, fill: NAVY, h: 0.58 },
  { cells: ["backbone", "58.7 [56.5, 60.9]", "47.9 [45.4, 50.5]"], h: 0.52 },
  { cells: ["GUIStep-S", "73.7 [71.8, 75.7]", "56.3 [53.8, 58.9]"], h: 0.52 },
  { cells: ["GUIStep-D", "71.7 [69.7, 73.5]", "54.7 [52.2, 57.3]"], h: 0.52 },
  { cells: ["control", "73.8 [72.0, 75.7]", "57.4 [54.9, 59.8]"], h: 0.52 },
  { cells: ["GUIStep-P", "74.0 [72.1, 75.9]", "58.3 [55.8, 60.8]"], h: 0.52, ruleC: NAVY, ruleW: 1.5 },
  { cells: [{ t: "S − backbone", bold: true }, "+15.0 [+13.1, +17.0]", { t: "+8.4 [+6.0, +11.0]", bold: true, color: TEAL }], h: 0.52 },
  { cells: [{ t: "P − S", bold: true }, "+0.3 [−1.3, +1.8] (p = 0.75)", "+1.9 [+0.2, +3.7] (p = 0.031)"], h: 0.52 },
  { cells: [{ t: "P − control", bold: true }, "+0.2 [−0.5, +0.8] (p = 0.64)", "+0.9 [+0.2, +1.6] (p = 0.015)"], h: 0.52, rule: false },
], { fs: 17, align: ["left", "right", "right"] });
text("Subgroup split made after seeing the overall result; not corrected for multiple comparisons.", { x: M, y: 6.25, w: W - 2 * M, h: 0.45, fontSize: 15, italic: true, color: GREY, align: "center" });
note(QA("B6")); footB();

pres.writeFile({ fileName: path.join(__dirname, "..", "SOICT2026_SLIDE.pptx") }).then(() => {
  console.log("Done: SOICT2026_SLIDE.pptx | main " + PAGE + " | backup " + BPAGE + " | notes " + Object.keys(SAY).length);
});
