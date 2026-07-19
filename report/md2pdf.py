#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert a report markdown -> PDF with Vietnamese-safe fonts (DejaVu).

Usage:
    python3 report/md2pdf.py                 # default: report/43
    python3 report/md2pdf.py report/38_ban_trinh_bay_bao_ve.md
    python3 report/md2pdf.py 38              # số hiệu -> tự tìm report/38*.md
"""
import sys, re, glob
import markdown
from weasyprint import HTML

def _resolve(arg):
    if arg.endswith(".md"):
        return arg
    hits = sorted(glob.glob(f"report/{arg}_*.md") + glob.glob(f"report/{arg}*.md"))
    if not hits:
        raise SystemExit(f"Không tìm thấy report/{arg}*.md")
    return hits[0]

SRC = _resolve(sys.argv[1]) if len(sys.argv) > 1 else "report/43_ho_so_thuyet_phuc_toan_dien.md"
OUT = SRC[:-3] + ".pdf"

raw = open(SRC, encoding="utf-8").read()

# Emoji not covered by DejaVu -> map to visually-similar covered glyphs (no tofu boxes)
repl = {
    "⭐": "★",   # ⭐ -> ★
    "✅": "✔",   # ✅ -> ✔
    "⏳": "☐",   # ⏳ -> ☐ (pending)
    "\U0001f4ce": "※",  # 📎 -> ※
    "\U0001f4e6": "▣",  # 📦 -> ▣
    "️": "",          # variation selector (invisible)
}
for a, b in repl.items():
    raw = raw.replace(a, b)

# ---- Inline LaTeX ($...$) -> Unicode/HTML so it doesn't render as literal "$\tau$" ----
GREEK = {"tau": "τ", "pi": "π", "kappa": "κ", "rho": "ρ", "phi": "φ",
         "Delta": "Δ", "sigma": "σ", "mu": "μ", "lambda": "λ", "alpha": "α",
         "beta": "β", "gamma": "γ", "epsilon": "ε", "theta": "θ"}
REL = {"ge": "≥", "le": "≤", "geq": "≥", "leq": "≤", "approx": "≈", "ne": "≠",
       "neq": "≠", "to": "→", "leftrightarrow": "↔", "Rightarrow": "⇒",
       "rightarrow": "→", "in": "∈", "notin": "∉", "times": "×", "cdot": "·",
       "pm": "±", "wedge": "∧", "vee": "∨", "sum": "Σ", "prod": "Π", "cup": "∪",
       "cap": "∩", "subseteq": "⊆", "forall": "∀", "exists": "∃", "ldots": "…",
       "dots": "…", "circ": "∘", "star": "⋆", "ell": "ℓ", "infty": "∞"}

def _hat(a):
    return GREEK.get(a, a) + "̂"

def _grab_brace(s, i):
    """s[i] == '{' -> return (inner, index_after_matching_close)."""
    depth = 0
    j = i
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)

def _fracs(s, stacked=True):
    """Replace \\frac{A}{B} (brace-balanced, recursive) with a fraction.
    stacked=True -> HTML stacked fraction (for display blocks);
    stacked=False -> inline slash form A/B (for running text)."""
    out, i = "", 0
    while i < len(s):
        m = re.match(r"\\[tdc]?frac", s[i:])
        if m:
            i += m.end()
            while i < len(s) and s[i] != "{":
                i += 1
            num, i = _grab_brace(s, i)
            while i < len(s) and s[i] != "{":
                i += 1
            den, i = _grab_brace(s, i)
            n, d = _fracs(num, stacked), _fracs(den, stacked)
            if stacked:
                out += ('<span class="frac"><span class="fnum">' + n
                        + '</span><span class="fden">' + d + "</span></span>")
            else:
                nn = "(" + n + ")" if " " in n.strip() else n
                dd = "(" + d + ")" if " " in d.strip() else d
                out += nn + "/" + dd
        else:
            out += s[i]
            i += 1
    return out

def conv_math(s, block=False):
    s = _fracs(s, stacked=block)
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\math\w+\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\operatorname\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\hat\\?(\w+)", lambda m: _hat(m.group(1)), s)
    # sizing/delimiter commands -> drop, keeping the delimiter that follows
    s = re.sub(r"\\(?:left|right|bigg?|Bigg?)", "", s)
    # protect explicit set braces \{ \} from the bare-brace cleanup
    s = s.replace("\\{", "\x01").replace("\\}", "\x02")
    s = s.replace("\\%", "%").replace("\\,", " ").replace("\\;", " ")
    s = s.replace("\\!", "").replace("\\ ", " ").replace("\\|", "|").replace("\\:", " ")
    def _cmd(m):
        w = m.group(1)
        return GREEK.get(w) or REL.get(w) or w
    s = re.sub(r"\\([A-Za-z]+)", _cmd, s)
    s = re.sub(r"\^\{([^}]*)\}", r"<sup>\1</sup>", s)
    s = re.sub(r"\^(\w)", r"<sup>\1</sup>", s)
    s = re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", s)
    s = re.sub(r"_(\w)", r"<sub>\1</sub>", s)
    s = s.replace("{,}", ",").replace("{", "").replace("}", "")
    s = s.replace("\x01", "{").replace("\x02", "}")
    if block:
        return '<div class="mathblock">' + s + "</div>"
    return '<span class="mathin">' + s + "</span>"

# display math $$...$$ first (single-line), then inline $...$
raw = re.sub(r"\$\$(.+?)\$\$", lambda m: conv_math(m.group(1), block=True), raw)
lines, in_code = [], False
for ln in raw.splitlines():
    if ln.lstrip().startswith("```"):
        in_code = not in_code
        lines.append(ln); continue
    if not in_code and ln.count("$") >= 2 and ln.count("$") % 2 == 0:
        ln = re.sub(r"\$([^$]+)\$", lambda m: conv_math(m.group(1)), ln)
    lines.append(ln)
raw = "\n".join(lines)

html_body = markdown.markdown(
    raw,
    extensions=["tables", "fenced_code", "sane_lists", "nl2br", "attr_list"],
)

CSS = """
@page { size: A4; margin: 1.8cm 1.6cm; }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 10.5px; line-height: 1.5;
       color: #1a1a1a; }
h1 { font-size: 19px; border-bottom: 2px solid #333; padding-bottom: 6px;
     margin-top: 0.2em; }
h2 { font-size: 15px; border-bottom: 1px solid #bbb; padding-bottom: 3px;
     margin-top: 1.1em; color: #14395c; }
h3 { font-size: 13px; margin-top: 0.9em; color: #14395c; }
h4 { font-size: 11.5px; margin-top: 0.8em; }
p { margin: 0.35em 0; text-align: left; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 9px;
       background: #f2f2f2; padding: 0.5px 3px; border-radius: 3px; }
pre { background: #f6f8fa; border: 1px solid #ddd; border-radius: 5px;
      padding: 8px 10px; overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; font-size: 8.5px; line-height: 1.35; }
blockquote { border-left: 3px solid #7aa7cc; background: #f4f8fb;
             margin: 0.5em 0; padding: 4px 12px; color: #33475b; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0;
        font-size: 8.7px; page-break-inside: avoid; }
th, td { border: 1px solid #c8c8c8; padding: 3px 5px; text-align: left;
         vertical-align: top; }
th { background: #eaf0f6; font-weight: bold; }
tr:nth-child(even) td { background: #fafbfc; }
ul, ol { margin: 0.3em 0; padding-left: 1.4em; }
li { margin: 0.15em 0; }
hr { border: none; border-top: 1px solid #ccc; margin: 1em 0; }
strong { color: #111; }
a { color: #14395c; text-decoration: none; }
.mathin { font-family: 'DejaVu Serif', serif; font-style: italic; }
.mathblock { font-family: 'DejaVu Serif', serif; font-style: italic;
             text-align: center; margin: 0.6em 0; white-space: nowrap; }
.frac { display: inline-flex; flex-direction: column; text-align: center;
        vertical-align: middle; margin: 0 2px; font-style: italic; }
.frac .fnum { border-bottom: 1px solid currentColor; padding: 0 4px; }
.frac .fden { padding: 0 4px; }
sup, sub { font-size: 0.72em; }
"""

full = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html_body}</body></html>"
HTML(string=full).write_pdf(OUT)
print("WROTE", OUT)
