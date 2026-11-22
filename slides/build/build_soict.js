// SOICT 2026 talk deck (GUIStep, paper 5590), following slides/KICH_BAN_SOICT_15_11.md.
// 12 content slides (five parts) + Thank-you + 10 backup slides. 16:9, same visual family as the VCL deck
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
const MINT = "E6F0EF";
const FOOTA = "191132", FOOTB = "25194B", FOOTC = "4F417A";
const W = 13.333, H = 7.5, M = 0.6;

// ---------- notes from the script ----------
function clean(t) {
  return t.replace(/\*/g, "").replace(/`/g, "")
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
const TOTAL = 13;
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
  const o = { y: yy, h: hh, fontSize: 14, color: WHITE, align: "center", valign: "middle" };
  text("Uyen Le Doan Phuong", Object.assign({ x: 0, w: 5.0 }, o));
  text("SOICT 2026 · GUIStep", Object.assign({ x: 5.0, w: 6.3 }, o));
  text(label, Object.assign({ x: 11.3, w: W - 11.3 }, o));
}
function foot() { PAGE++; footRow(`${PAGE}/${TOTAL}`); }
function footB() { BPAGE++; footRow(`B${BPAGE}`); }
function note(t) { s.addNotes(t); }
// footnote: left-aligned, one place, one size
function caption(t, y, o) { text(t, Object.assign({ x: M, y, w: W - 2 * M, h: 0.4, fontSize: 14, color: GREY, valign: "middle" }, o || {})); }
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

// ---------- progress bar ----------
const PARTS = ["Task", "Method", "Evaluation", "Results", "Conclusion"];
function main(title, part) {
  slide();
  rect(0, 0, W, 0.95, NAVY);
  text(title, { x: M, y: 0, w: 7.45, h: 0.95, fontSize: title.length > 40 ? 21 : 24, bold: true, color: WHITE, valign: "middle" });
  const runs = [];
  PARTS.forEach((p, i) => {
    if (i) runs.push({ text: " · ", options: { color: "7A7099" } });
    runs.push({ text: p, options: i === part ? { bold: true, color: WHITE } : { color: "9A93B8" } });
  });
  text(runs, { x: 8.1, y: 0, w: W - 8.1 - 0.25, h: 0.95, fontSize: 14, align: "right", valign: "middle" });
}
function vbars(x, y, w, h, items, vmax, o) {
  o = o || {};
  const n = items.length, slot = w / n, bw = slot * (o.bw || 0.5);
  hline(x, y + h, w, GREY, 1.25);
  items.forEach((it, i) => {
    const bh = h * it.v / vmax, bx = x + i * slot + (slot - bw) / 2;
    rect(bx, y + h - bh, bw, bh, it.color || NAVY);
    text(it.txt, { x: bx - 0.5, y: y + h - bh - 0.6, w: bw + 1.0, h: 0.55, fontSize: o.vfs || 26, bold: true, color: it.color || NAVY, align: "center", valign: "bottom" });
    text(it.label, { x: x + i * slot + 0.02, y: y + h + 0.1, w: slot - 0.04, h: o.lh || 0.9, fontSize: o.lfs || 15, color: INK, align: "center", lh: 1.0 });
  });
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
text("Session 6B, 5 December 2026", { x: 0.9, y: 6.05, w: W - 1.8, h: 0.5, fontSize: 18, color: TEAL, align: "center" });
note(SAY[1]); foot();

// ══════════ 2 · TASK ══════════
main("Task: write the next step for a person", 0);
text([{ text: "GUI agents: ", options: { bold: true, color: GREY } }, { text: "instruction → action.      ", options: { color: GREY } },
      { text: "GUIStep: ", options: { bold: true, color: NAVY } }, { text: "screen + goal → instruction for a person.", options: { color: NAVY } }],
  { x: M, y: 1.05, w: W - 2 * M, h: 0.5, fontSize: 19, align: "center", valign: "middle" });
{
  const ih = 5.15, iw = ih * 720 / 736, ix = M, iy = 1.7;
  s.addImage({ path: FIG1, x: ix, y: iy, w: iw, h: ih });
  rect(ix, iy, iw, ih, "none", { line: SOFT, lw: 1 });
  const cx = ix + 0.142 * iw, cy = iy + 0.332 * ih, r = 0.0879 * iw;
  s.addShape(pres.shapes.OVAL, { x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, fill: { type: "none" }, line: { color: RED, width: 3 } });
  const bx = ix + iw + 0.45, bw = W - M - bx;
  [["Goal", "find Aer Lingus flights, sort by cheapest direct flight", BLOCK, NAVY, false],
   ["Generated", "“Click on the sort by option”", MINT, TEAL, true],
   ["Reference", "“Click on sort by option at the top left of the screen”", BLOCK, GREY, true]].forEach((c, i) => {
    const yy = 1.75 + i * 1.5;
    block(bx, yy, bw, 1.3, c[2]);
    text(c[0], { x: bx + 0.25, y: yy + 0.1, w: bw - 0.5, h: 0.4, fontSize: 17, bold: true, color: c[3] });
    text(c[1], { x: bx + 0.25, y: yy + 0.48, w: bw - 0.5, h: 0.75, fontSize: 19, valign: "middle", lh: 1.0 });
  });
  text("Five filter chips are on screen, and the sentence names the right one.", { x: bx, y: 6.25, w: bw, h: 0.5, fontSize: 16, color: GREY });
}
note(SAY[2]); foot();

// ══════════ 3 · CONTRIBUTIONS ══════════
main("Three contributions", 0);
[["Method", "a 3B model trained only on what GUI datasets already record"],
 ["Evaluation", "executability, which checks whether someone can follow the sentence"],
 ["Results", "+13.0 over the untuned backbone and above a prompted 7B model"]].forEach((c, i) => {
  const yy = 1.5 + i * 1.6;
  block(M, yy, W - 2 * M, 1.3);
  rect(M, yy, 0.95, 1.3, TEAL, { radius: 0.08 });
  text(String(i + 1), { x: M, y: yy, w: 0.95, h: 1.3, fontSize: 32, bold: true, color: WHITE, align: "center", valign: "middle" });
  text([{ text: c[0] + ": ", options: { bold: true, color: NAVY } }, { text: c[1], options: {} }],
    { x: M + 1.3, y: yy, w: W - 2 * M - 1.6, h: 1.3, fontSize: 24, valign: "middle", lh: 1.05 });
});
note(SAY[3]); foot();

// ══════════ 4 · TRAINING SIGNAL ══════════
main("Training data comes from existing records", 1);
{
  const y = 1.45, h = 1.4;
  box(M, y, 4.6, h, "recorded step:\nscreenshot, human instruction,\ntouch point, UI tree", { fs: 18 });
  arrow(M + 4.65, y + h / 2, M + 5.35, y + h / 2);
  box(M + 5.4, y, 2.9, h, "training targets", { fs: 20, bold: true, fill: WHITE });
  arrow(M + 8.35, y + h / 2, M + 9.05, y + h / 2);
  box(M + 9.1, y, 3.03, h, "Qwen2.5-VL-3B\n+ QLoRA", { fs: 20, bold: true, color: WHITE, fill: NAVY, line: NAVY });
}
caption("We add no labels. Other GUI datasets record the same fields.", 3.0, { fontSize: 17 });
block(M, 3.7, W - 2 * M, 2.45);
text("From the UI tree we build a declaration of the target element", { x: M + 0.3, y: 3.8, w: W - 2 * M - 0.6, h: 0.55, fontSize: 20, bold: true, color: NAVY, valign: "middle" });
{
  // one box per field, label underneath, instead of one long tagged string
  const F = [["item", "role", 1.7], ["Close", "name", 1.9], ["<point>274,285</point>", "position", 4.3], ["just below \"3:09\"", "nearby text", 3.33]];
  let x = M + 0.3;
  F.forEach(f => {
    const w = f[2];
    rect(x, 4.5, w, 0.85, WHITE, { radius: 0.06, line: SOFT, lw: 1 });
    text(f[0], { x, y: 4.5, w, h: 0.85, fontSize: 18, fontFace: MONO, color: NAVY, align: "center", valign: "middle" });
    text(f[1], { x, y: 5.45, w, h: 0.45, fontSize: 17, color: GREY, align: "center", valign: "middle" });
    x += w + 0.1;
  });
}
note(SAY[4]); foot();

// ══════════ 5 · THREE VERSIONS ══════════
main("Three versions of GUIStep, plus a control", 1);
table(M, 1.5, [1.3, 7.7, 3.13], [
  { cells: ["", "learns to write", "training"], bold: true, color: WHITE, fill: NAVY, h: 0.65, fs: 20 },
  { cells: [{ t: "S", bold: true }, "the sentence", "cross-entropy"], h: 0.85 },
  { cells: [{ t: "D", bold: true }, "the declaration, then the sentence", "cross-entropy"], h: 0.85 },
  { cells: [{ t: "P", bold: true, color: TEAL }, "D + preference: right vs wrong element declared", { t: "ORPO", bold: true, color: TEAL }], h: 0.85, rule: false },
], { fs: 22 });
block(M, 5.2, W - 2 * M, 1.2, MINT);
text([{ text: "Control: ", options: { bold: true, color: TEAL } }, { text: "P's extra updates, on correct examples only.\n", options: {} },
      { text: "P minus control is what the preference objective adds.", options: { color: GREY, fontSize: 19 } }],
  { x: M + 0.3, y: 5.2, w: W - 2 * M - 0.6, h: 1.2, fontSize: 22, valign: "middle", lh: 1.1 });
note(SAY[5]); foot();

// ══════════ 6 · WORD OVERLAP ══════════
main("Word overlap cannot judge these sentences", 2);
box(M, 1.4, 5.6, 0.9, "“Click on the search bar”", { fs: 21, fill: WHITE });
box(M, 2.7, 5.6, 0.9, "“Tap the magnifying glass at the top”", { fs: 21, fill: WHITE });
arrow(M + 5.65, 1.85, 7.45, 2.4); arrow(M + 5.65, 3.15, 7.45, 2.65);
rect(7.55, 1.9, 1.2, 1.2, NAVY, { radius: 0.12 });
s.addShape(pres.shapes.OVAL, { x: 7.79, y: 2.08, w: 0.58, h: 0.58, fill: { type: "none" }, line: { color: WHITE, width: 4 } });
s.addShape(pres.shapes.LINE, { x: 8.29, y: 2.59, w: 0.27, h: 0.27, line: { color: WHITE, width: 5 } });
text("same button", { x: 8.95, y: 2.2, w: 2.5, h: 0.6, fontSize: 19, bold: true, color: NAVY, valign: "middle" });
[["97.5%", "valid rewordings rejected by word overlap (pilot)"], ["AUC 0.34", "embedding similarity telling the same element from a different one (chance is 0.5)"]].forEach((c, i) => {
  const x = M + i * 6.2;
  block(x, 4.15, 5.9, 2.2);
  text(c[0], { x, y: 4.25, w: 5.9, h: 1.1, fontSize: 52, bold: true, color: RED, align: "center", valign: "middle" });
  text(c[1], { x: x + 0.3, y: 5.35, w: 5.3, h: 0.85, fontSize: 18, align: "center", valign: "middle", lh: 1.05 });
});
note(SAY[6]); foot();

// ══════════ 7 · EXECUTABILITY ══════════
main("Executability: a model follows the sentence", 2);
{
  // same screen as slide 2, so the audience already knows the example
  const ih = 4.5, iw = ih * 720 / 736, ix = M, iy = 1.2;
  s.addImage({ path: FIG1, x: ix, y: iy, w: iw, h: ih });
  rect(ix, iy, iw, ih, "none", { line: SOFT, lw: 1 });
  const cx = ix + 0.142 * iw, cy = iy + 0.332 * ih, r = 0.0879 * iw;
  s.addShape(pres.shapes.OVAL, { x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, fill: { type: "none" }, line: { color: RED, width: 3 } });
  text([{ text: "red circle: ", options: { bold: true, color: RED } }, { text: "the element the user tapped", options: { color: GREY } }], { x: ix, y: iy + ih + 0.02, w: iw + 0.4, h: 0.26, fontSize: 13, valign: "middle" });
  const bx = ix + iw + 0.45, bw = W - M - bx;
  block(bx, 1.2, bw, 1.05);
  text([{ text: "1  ", options: { bold: true, color: TEAL } }, { text: "The listener (UGround, frozen) gets\n", options: { bold: true, color: NAVY } },
        { text: "the screenshot and “Click on the sort by option”", options: {} }],
    { x: bx + 0.25, y: 1.2, w: bw - 0.5, h: 1.05, fontSize: 18, valign: "middle", lh: 1.05 });
  block(bx, 2.4, bw, 0.75);
  text([{ text: "2  ", options: { bold: true, color: TEAL } }, { text: "It taps one point ", options: { bold: true, color: NAVY } },
        { text: "without seeing the answer.", options: {} }],
    { x: bx + 0.25, y: 2.4, w: bw - 0.5, h: 0.75, fontSize: 18, valign: "middle" });
  text([{ text: "3  ", options: { bold: true, color: TEAL } }, { text: "The step counts as correct if:", options: { bold: true, color: NAVY } }],
    { x: bx + 0.25, y: 3.25, w: bw - 0.5, h: 0.5, fontSize: 18, valign: "middle" });
  const cw = (bw - 0.3) / 3;
  [["right action", "click, not scroll"], ["same meaning", "not enable ↔ disable"], ["point inside", "the element the user tapped"]].forEach((c, i) => {
    const x = bx + i * (cw + 0.15);
    block(x, 3.85, cw, 1.85, MINT);
    text(c[0], { x: x + 0.1, y: 3.95, w: cw - 0.2, h: 0.6, fontSize: 19, bold: true, color: TEAL, align: "center", valign: "middle" });
    text(c[1], { x: x + 0.1, y: 4.55, w: cw - 0.2, h: 1.0, fontSize: 16, align: "center", valign: "middle", lh: 1.0 });
  });
}
block(M, 6.0, W - 2 * M, 0.75, MINT);
text([{ text: "Executability ", options: { bold: true, color: TEAL } }, { text: "= share of test steps that pass all three checks", options: {} }],
  { x: M + 0.3, y: 6.0, w: W - 2 * M - 0.6, h: 0.75, fontSize: 22, valign: "middle" });
note(SAY[7]); foot();

// ══════════ 8 · SCORE VALIDATED ══════════
main("The score separates good and bad sentences", 2);
text("executability (%)", { x: M, y: 1.15, w: 6.0, h: 0.45, fontSize: 16, color: GREY });
vbars(M + 0.1, 1.8, 6.1, 2.9, [
  { label: "human reference\n(ceiling)", v: 83.8, txt: "83.8", color: AMBER },
  { label: "“Tap the button.”", v: 14.1, txt: "14.1", color: SOFT },
  { label: "reference from\nanother screen", v: 8.6, txt: "8.6", color: SOFT },
], 90, { bw: 0.5, lfs: 16, vfs: 26, lh: 0.75 });
text("A fluent sentence written for another screen scores below “Tap the button.”", { x: M, y: 5.7, w: 6.3, h: 0.6, fontSize: 17, valign: "middle" });
caption("Ceiling on all 4,463 steps; the two floors on a random slice of 800.", 6.35, { w: 6.3 });
[["Other listeners", "UI-Venus, not trained on AndroidControl, keeps 99% of the gain. Phi-4, from another model family, shows it too."],
 ["Stricter localisation rule", "The Voronoi rule ranks all systems in the same order."],
 ["Rewording", "1,139 rewrites with another verb or word order: −0.09 points [−0.93, +0.79]"]].forEach((c, i) => {
  const yy = 1.3 + i * 1.7;
  block(7.3, yy, 5.43, 1.5);
  text(c[0], { x: 7.55, y: yy + 0.12, w: 5.0, h: 0.45, fontSize: 19, bold: true, color: NAVY });
  text(c[1], { x: 7.55, y: yy + 0.55, w: 5.0, h: 0.85, fontSize: 17, valign: "top", lh: 1.0 });
});
note(SAY[8]); foot();

// ══════════ 9 · MAIN RESULTS ══════════
main("Main results: +13.0 over the backbone", 3);
text("executability (%), point-inside-element rule, 4,463 test touch steps", { x: M, y: 1.1, w: 9, h: 0.45, fontSize: 17, color: GREY });
{
  const rows = [["untuned 3B", 53.6, SOFT], ["prompted 7B", 57.7, SOFT], ["select-then-verbalise", 62.4, SOFT], ["GUIStep-D", 63.6, NAVY], ["GUIStep-S", 65.5, NAVY],
    ["control*", 66.0, NAVY], ["GUIStep-P", 66.5, TEAL], ["human reference", 83.8, AMBER]];
  const lw = 2.6, bx = M + 2.75, bwMax = 5.8, vmax = 90, y0 = 1.6, rh = 0.585;
  rows.forEach((r, i) => {
    const yy = y0 + i * rh, hl = r[0] === "GUIStep-P" || r[0] === "human reference";
    text(r[0], { x: M, y: yy, w: lw, h: rh, fontSize: 17, bold: hl, color: r[0] === "human reference" ? AMBER : INK, align: "right", valign: "middle" });
    rect(bx, yy + 0.1, bwMax * r[1] / vmax, rh - 0.2, r[2]);
    text(r[1].toFixed(1), { x: bx + bwMax * r[1] / vmax + 0.08, y: yy, w: 0.9, h: rh, fontSize: 18, bold: hl, color: r[2] === SOFT ? GREY : r[2], valign: "middle" });
  });
  vline(bx, y0, rows.length * rh, GREY, 1.25);
  block(9.75, 2.3, 2.98, 2.7, MINT);
  text("+13.0", { x: 9.85, y: 2.45, w: 2.78, h: 1.2, fontSize: 48, bold: true, color: TEAL, align: "center", valign: "middle" });
  text("GUIStep-P over the untuned 3B model\n95% CI [+11.5, +14.4]", { x: 9.95, y: 3.65, w: 2.58, h: 1.25, fontSize: 16, align: "center", valign: "middle", lh: 1.05 });
}
caption("* Control: P's extra updates, correct examples only. 95% CIs: bootstrap clustered by app. A second run of S lands within 0.6.", 6.38);
note(SAY[9]); foot();

// ══════════ 10 · KEY FINDING ══════════
main("Most of the gain comes from learning the sentence", 3);
{
  // step chart: backbone -> S -> P
  const steps = [["untuned 3B", 53.6, SOFT], ["GUIStep-S\nsentence only", 65.5, NAVY], ["GUIStep-P", 66.5, TEAL]];
  const x0 = M + 0.3, y0 = 1.35, hh = 3.9, vmin = 45, vmax = 70, slot = 2.15, bw = 1.25;
  const Y = v => y0 + hh * (1 - (v - vmin) / (vmax - vmin));
  hline(x0, y0 + hh, slot * 3, GREY, 1.25);
  steps.forEach((st, i) => {
    const bx = x0 + i * slot + (slot - bw) / 2;
    rect(bx, Y(st[1]), bw, y0 + hh - Y(st[1]), st[2]);
    text(st[1].toFixed(1), { x: bx - 0.3, y: Y(st[1]) - 0.55, w: bw + 0.6, h: 0.5, fontSize: 24, bold: true, color: st[2] === SOFT ? GREY : st[2], align: "center", valign: "bottom" });
    text(st[0], { x: x0 + i * slot, y: y0 + hh + 0.08, w: slot, h: 0.75, fontSize: 15, align: "center", lh: 1.0 });
  });
  text("+11.9", { x: x0 + (slot + bw) / 2 + 0.02, y: Y(59.5) - 0.2, w: slot - bw - 0.04, h: 0.4, fontSize: 17, bold: true, color: NAVY, align: "center" });

  block(7.4, 1.45, 5.33, 2.3, MINT);
  text("> 90%", { x: 7.4, y: 1.55, w: 5.33, h: 1.0, fontSize: 48, bold: true, color: TEAL, align: "center", valign: "middle" });
  text("of the +13.0 gain is already in GUIStep-S, trained on the sentence alone", { x: 7.65, y: 2.6, w: 4.83, h: 1.0, fontSize: 18, align: "center", valign: "middle", lh: 1.05 });
  block(7.4, 4.0, 5.33, 2.05);
  text("+0.52", { x: 7.4, y: 4.1, w: 5.33, h: 0.9, fontSize: 36, bold: true, color: NAVY, align: "center", valign: "middle" });
  text("added by the preference objective over the matched control (p = 0.043)", { x: 7.65, y: 5.0, w: 4.83, h: 0.9, fontSize: 17, align: "center", valign: "middle", lh: 1.05 });
}
caption("Vertical axis starts at 45.", 6.45);
note(SAY[10]); foot();

// ══════════ 11 · UNSEEN ══════════
main("The gain holds on sentences never seen in training", 3);
[["+15.0", "58.7 → 73.7", "test sentences that also occur in training (52.6% of test)", NAVY, BLOCK],
 ["+8.4", "47.9 → 56.3", "test sentences never seen in training", TEAL, MINT]].forEach((c, i) => {
  const x = M + i * 6.2;
  block(x, 1.5, 5.9, 4.3, c[4]);
  text(c[0], { x, y: 1.7, w: 5.9, h: 1.6, fontSize: 72, bold: true, color: c[3], align: "center", valign: "middle" });
  text(c[1], { x, y: 3.3, w: 5.9, h: 0.6, fontSize: 24, color: c[3], align: "center", valign: "middle" });
  text(c[2], { x: x + 0.4, y: 4.0, w: 5.1, h: 1.3, fontSize: 20, align: "center", valign: "middle", lh: 1.1 });
});
caption("Untuned model → GUIStep-S, executability (%).", 6.2);
note(SAY[11]); foot();

// ══════════ 12 · CONCLUSION ══════════
main("Conclusion", 4);
[["0 new labels", "what GUI datasets already record is enough to train a 3B instruction writer"],
 ["83.8 vs 14.1", "executability separates human references from a generic sentence, and holds under other listeners and a stricter rule"],
 ["+13.0", "over the backbone and above a prompted 7B; over 90% of it comes from learning the sentence"]].forEach((c, i) => {
  const yy = 1.4 + i * 1.45;
  block(M, yy, W - 2 * M, 1.2);
  text(c[0], { x: M + 0.2, y: yy, w: 2.9, h: 1.2, fontSize: c[0].length > 6 ? 27 : 36, bold: true, color: TEAL, align: "center", valign: "middle" });
  text(c[1], { x: M + 3.3, y: yy, w: W - 2 * M - 3.55, h: 1.2, fontSize: 21, valign: "middle", lh: 1.05 });
});
text([{ text: "Next: ", options: { bold: true, color: NAVY } }, { text: "a second dataset, a human study, and rewards that act on the sentence.", options: {} }],
  { x: M, y: 5.95, w: W - 2 * M, h: 0.5, fontSize: 19 });
note(SAY[12]); foot();

// ══════════ 13 · THANK YOU ══════════
slide();
rect(0, 0, W, H - 0.32, NAVY);
text("Thank you · Questions?", { x: M, y: 2.2, w: W - 2 * M, h: 1.3, fontSize: 50, bold: true, color: WHITE, align: "center", valign: "middle" });
text("24C15039@student.hcmus.edu.vn", { x: M, y: 3.8, w: W - 2 * M, h: 0.6, fontSize: 22, fontFace: MONO, color: LIGHT, align: "center", valign: "middle" });
foot();

// ══════════════════ BACKUP ══════════════════
// B1 · validation table (Table 3)
slide();
bar("Validation of the listener (Table 3)");
{
  const R = (a, b, c, d, e, fail) => ({ cells: [{ t: a, bold: fail }, b, c, d, { t: e, bold: fail, color: fail ? RED : TEAL }], h: 0.43 });
  table(M, 1.1, [5.4, 2.0, 1.45, 1.45, 1.83], [
    { cells: ["check", "threshold", "D.3", "Voronoi", "D.3 verdict"], bold: true, color: WHITE, fill: NAVY, h: 0.48, fs: 15 },
    { cells: ["median localisation error of the listener", "≤ 3% of width", "0.7%", "0.7%", { t: "pass", color: TEAL }], h: 0.43 },
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
  caption("Thresholds fixed before either run, on the same 398 steps and seed. Listener error measured once (n = 300).", 6.45);
}
note(QA("A3")); footB();

// B2 · rule choice (Table 2)
slide();
bar("Choosing the localisation rule (Table 2)");
table(M, 1.35, [5.6, 2.15, 2.15, 2.23], [
  { cells: ["sentence given to the listener", "D.3", "Voronoi", "window ±14%"], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: ["reference instruction (ceiling)", "83.0", "74.9", "83.0"], h: 0.62 },
  { cells: ["“Tap the button.”", "14.1", "12.0", "20.5"], h: 0.62 },
  { cells: ["reference of a different screen", "8.6", "6.1", "12.8"], h: 0.62 },
  { cells: ["element name deleted, position kept", "74.8", "68.0", "78.9"], h: 0.62 },
  { cells: [{ t: "usable range", bold: true }, { t: "68.9", bold: true, color: TEAL }, "62.9", "62.5"], h: 0.62, rule: false },
], { fs: 19, align: ["left", "right", "right", "right"] });
caption("One random slice of 800 steps. Usable range = ceiling minus the generic sentence.", 5.4);
note(QA("A4")); footB();

// B3 · other listeners in detail
slide();
bar("Listener checks in detail");
block(M, 1.2, 5.95, 2.4);
text("UI-Venus-Ground-7B", { x: M + 0.25, y: 1.3, w: 5.5, h: 0.5, fontSize: 20, bold: true, color: NAVY });
text("Not trained on AndroidControl; 2,532 steps.\nS − backbone: +11.14 (UGround), +11.02 (UI-Venus).\n99% of the gap is kept.", { x: M + 0.25, y: 1.85, w: 5.5, h: 1.6, fontSize: 16, lh: 1.15 });
block(6.78, 1.2, 5.95, 2.4);
text("Phi-4-multimodal (Set-of-Mark)", { x: 7.03, y: 1.3, w: 5.5, h: 0.5, fontSize: 20, bold: true, color: NAVY });
text("Median 15 boxes per screen, 95.7% coverage.\nReference 54.9, S 44.6, backbone 38.2.\nS − backbone +6.4 [+5.1, +7.7], p < 0.001.", { x: 7.03, y: 1.85, w: 5.5, h: 1.6, fontSize: 16, lh: 1.15 });
text("Voronoi rule, all 4,463 steps", { x: M, y: 3.9, w: W - 2 * M, h: 0.5, fontSize: 20, bold: true, color: NAVY });
table(M, 4.45, [2.0, 2.0, 2.0, 2.0, 2.0, 2.13], [
  { cells: ["backbone", "GUIStep-D", "GUIStep-S", "control", "GUIStep-P", "reference"], bold: true, color: WHITE, fill: NAVY, h: 0.55, fs: 16 },
  { cells: ["47.6", "57.2", "59.1", "59.4", { t: "60.0", bold: true, color: TEAL }, "75.7"], h: 0.65, rule: false },
], { fs: 20, align: ["center", "center", "center", "center", "center", "center"] });
caption("S − backbone under Voronoi: +11.5 [+10.0, +13.1]. Other listeners were not run on P or the control.", 5.95);
note(QA("A2")); footB();

// B4 · ablation with full CIs
slide();
bar("Ablation with full intervals");
table(M + 0.5, 1.4, [3.2, 4.3, 2.2, 2.4], [
  { cells: ["comparison", "difference [95% CI]", "p", "note"], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: ["D − S", "−1.9 [−3.0, −0.7]", "0.003", "significant"], h: 0.7 },
  { cells: ["P − S", "+1.05 [−0.11, +2.20]", "0.073", "not significant"], h: 0.7 },
  { cells: ["P − control", "+0.52 [+0.02, +1.00]", "0.043", "significant, small"], h: 0.7 },
  { cells: ["second seed of S", "+0.6 [−0.2, +1.4]", "", "S = 66.1"], h: 0.7, rule: false },
], { fs: 20 });
caption("D, P and the control were each trained once.", 5.2, { x: M + 0.5 });
note(QA("B5")); footB();

// B5 · other baselines
slide();
bar("Other baselines");
[["62.4", "select-then-verbalise variant", "abstains on 27.3% of steps whose target is in the list; differs from S in 3 settings"],
 ["57.7", "Qwen2.5-VL-7B, prompted", "+4.1 over the 3B backbone, −7.8 vs GUIStep-S"]].forEach((c, i) => {
  const yy = 1.4 + i * 2.4;
  block(M, yy, W - 2 * M, 2.1);
  text(c[0], { x: M + 0.2, y: yy, w: 2.8, h: 2.1, fontSize: 48, bold: true, color: NAVY, align: "center", valign: "middle" });
  text(c[1], { x: M + 3.2, y: yy + 0.3, w: 8.7, h: 0.6, fontSize: 22, bold: true, color: NAVY });
  text(c[2], { x: M + 3.2, y: yy + 0.95, w: 8.7, h: 0.9, fontSize: 18, lh: 1.05 });
});
note(QA("B4")); footB();
// B4 · text metrics (Table 5)
slide();
bar("Reference-overlap metrics (Table 5)");
table(M, 1.35, [2.6, 1.35, 1.35, 1.4, 1.45, 1.3, 1.3, 1.38], [
  { cells: ["", "BLEU-4", "METEOR", "ROUGE-L", "CIDEr-D", "SPICE", "chrF", "BERTScore"], bold: true, color: WHITE, fill: NAVY, h: 0.6, fs: 15 },
  { cells: ["untuned backbone", "15.3", "24.6", "42.3", "88.0", "18.5", "40.2", "40.1"], h: 0.62 },
  { cells: ["GUIStep-S", { t: "51.6", bold: true }, "36.8", "67.3", { t: "416.1", bold: true }, { t: "44.4", bold: true }, "61.3", "66.3"], h: 0.62 },
  { cells: ["GUIStep-D", "48.7", "35.8", "66.0", "387.7", "41.3", "59.9", "65.1"], h: 0.62 },
  { cells: ["GUIStep-P", "49.9", { t: "37.3", bold: true }, { t: "68.5", bold: true }, "401.0", "42.2", { t: "61.8", bold: true }, { t: "66.7", bold: true }], h: 0.62 },
  { cells: [{ t: "reference" }, "100.0", "100.0", "100.0", "988.7", "98.6", "100.0", "100.0"], h: 0.62, rule: false, color: GREY },
], { fs: 17, align: ["left", "right", "right", "right", "right", "right", "right", "right"] });
caption("4,463 steps, one reference per step. CIDEr-D goes above 100 here and is comparable only within this table.", 5.4);
note(QA("A1")); footB();

// B7 · error analysis
slide();
bar("Error analysis of GUIStep-P");
block(M, 1.35, 5.2, 3.3);
text("96.3%", { x: M, y: 1.5, w: 5.2, h: 1.3, fontSize: 60, bold: true, color: RED, align: "center", valign: "middle" });
text("of the 1,493 failed steps miss the localisation check; 50 fail on the action, 5 on polarity", { x: M + 0.3, y: 2.9, w: 4.6, h: 1.5, fontSize: 18, align: "center", lh: 1.1 });
table(6.2, 1.35, [3.3, 3.23], [
  { cells: ["model wrote", "reference"], bold: true, color: WHITE, fill: NAVY, h: 0.6 },
  { cells: [{ t: "select minutes 00", mono: true, fs: 16 }, { t: "click on the OK option" }], h: 1.1 },
  { cells: [{ t: "Click on the Air India flight option", mono: true, fs: 16 }, { t: "Click on the Sort filter" }], h: 1.1, rule: false },
], { fs: 18 });
caption("We did not inspect failures by hand, so the sentence, the listener and the box are all possible causes.", 5.1);
note(QA("B12")); footB();
// B5 · training details
slide();
bar("Training details");
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
bar("Generation prompt (Appendix A)");
block(M, 1.2, W - 2 * M, 1.15);
text([{ text: "System. ", options: { bold: true, color: NAVY } }, { text: "“You look at a phone screenshot and write ONE short English instruction for the user that says where to touch in order to continue.”", options: {} }],
  { x: M + 0.25, y: 1.2, w: W - 2 * M - 0.5, h: 1.15, fontSize: 17, valign: "middle", lh: 1.1 });
block(M, 2.6, W - 2 * M, 2.4, WHITE, SOFT);
text("[image]\nGoal: <goal>\nDone so far: <step 1> → <step 2> → <step 3>\nText read on the screen: <OCR 1> · <OCR 2> · ...\nWrite the instruction for the next step.",
  { x: M + 0.4, y: 2.6, w: W - 2 * M - 0.8, h: 2.4, fontSize: 18, fontFace: MONO, color: NAVY, valign: "middle", lh: 1.2 });
caption("History = the last three reference instructions. At most 24 OCR detections (RapidOCR, confidence ≥ 0.5).\nThe listener sees only the screenshot and the generated sentence.", 5.25, { h: 0.8, lh: 1.15, valign: "top" });
footB();

// B7 · repeated / unseen (Table 4)
slide();
bar("Repeated and unseen sentences (Table 4)");
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
caption("We chose this split after seeing the overall result and did not correct for multiple comparisons.", 6.25);
note(QA("B6")); footB();


pres.writeFile({ fileName: path.join(__dirname, "..", "SOICT2026_SLIDE.pptx") }).then(() => {
  console.log("Done: SOICT2026_SLIDE.pptx | main " + PAGE + " | backup " + BPAGE + " | notes " + Object.keys(SAY).length);
});
