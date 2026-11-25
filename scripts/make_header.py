"""Generates assets/header.svg – a terminal window with a typing animation.

Pure SVG + CSS, no external dependencies. To change the text, edit the `script`
list below, then run from the repo root:   python3 scripts/make_header.py
"""
from html import escape

CW = 9.0           # character width at 15px monospace (~0.6em)
TYPE = 0.065       # seconds per typed character
PAUSE = 0.45       # pause between lines
X0, Y0, LH = 32, 78, 26
W, H = 860, 210

ACCENT, MUTED, TEXT, PROMPT = "#ff8c42", "#8b949e", "#e6edf3", "#3fb950"

script = [
    ("cmd", "whoami"),
    ("out", "Leon · Apprentice IT Specialist for Application Development"),
    ("cmd", "cat interests.txt"),
    ("out", "Cybersecurity · Homelab · Linux · Python"),
    ("cmd", ""),
]

css, body = [], []
t, y = 0.4, Y0
for i, (kind, text) in enumerate(script):
    if kind == "cmd":
        body.append(f'<text x="{X0}" y="{y}" class="p p{i}">leon@hamburg:~$</text>')
        css.append(f".p{i}{{animation:show .01s {t - 0.25:.2f}s both}}")
        cx = X0 + 16 * CW
        if text:
            n = len(text)
            dur = n * TYPE
            body.append(f'<text x="{cx}" y="{y}" class="c">{escape(text)}</text>')
            # a cover slides right one character at a time -> typing effect
            body.append(f'<rect class="cv cv{i}" x="{cx - 1}" y="{y - 16}" width="{n * CW + 4}" height="22"/>')
            css.append(f".cv{i}{{transform:translateX({n * CW + 4:.0f}px);animation:type{i} {dur:.2f}s steps({n},end) {t:.2f}s both}}"
                       f"@keyframes type{i}{{from{{transform:translateX(0)}}to{{transform:translateX({n * CW + 4:.0f}px)}}}}")
            t += dur + PAUSE
        else:
            body.append(f'<rect class="cur" x="{cx}" y="{y - 14}" width="9" height="18"/>')
            css.append(f".cur{{animation:show .01s {t:.2f}s both,blink 1s steps(1) {t:.2f}s infinite}}")
    else:
        body.append(f'<text x="{X0}" y="{y}" class="o o{i}">{escape(text)}</text>')
        css.append(f".o{i}{{animation:show .01s {t:.2f}s both}}")
        t += PAUSE
    y += LH

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">leon@hamburg — Terminal</title>
  <desc id="desc">whoami: Leon, apprentice IT specialist for application development. Interests: cybersecurity, homelab, Linux, Python.</desc>
  <style>
    text{{font:15px ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;white-space:pre}}
    .p{{fill:{PROMPT};font-weight:600}} .c{{fill:{TEXT}}} .o{{fill:{MUTED}}} .o1{{fill:{TEXT}}}
    .cv{{fill:#0d1117}} .cur{{fill:{ACCENT}}}
    {"".join(css)}
    @keyframes show{{from{{opacity:0}}to{{opacity:1}}}}
    @keyframes blink{{50%{{opacity:0}}}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
  </style>
  <defs><clipPath id="win"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12"/></clipPath></defs>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
  <path d="M1 40h{W - 2}" stroke="#30363d"/>
  <circle cx="24" cy="20" r="6" fill="#ff5f56"/><circle cx="44" cy="20" r="6" fill="#ffbd2e"/><circle cx="64" cy="20" r="6" fill="#27c93f"/>
  <text x="{W / 2}" y="25" text-anchor="middle" style="font-size:13px;fill:{MUTED}">leon@hamburg: ~</text>
  <g clip-path="url(#win)">
    {chr(10).join("    " + b for b in body).strip()}
  </g>
</svg>
'''
import sys
out = sys.argv[1] if len(sys.argv) > 1 else "assets/header.svg"
open(out, "w", encoding="utf-8").write(svg)
print("ok", round(t, 2), "s")
