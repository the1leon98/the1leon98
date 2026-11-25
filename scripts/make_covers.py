"""Generates the project cover images in assets/ (pure SVG, 1280x640).

1280x640 is also GitHub's social preview size, so the same files can be uploaded
as the repository's social preview (Repo -> Settings -> Social preview).

Run from the repo root:   python3 scripts/make_covers.py
"""
from html import escape

W, H = 1280, 640
BG, PANEL, BORDER = "#0d1117", "#161b22", "#30363d"
ACCENT, TEXT, MUTED, OK = "#ff8c42", "#e6edf3", "#8b949e", "#3fb950"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def frame(title: str, subtitle: str, tags: list[str], art: str, label: str) -> str:
    """Shared layout: text on the left, illustration on the right."""
    tag_svg, x = [], 80
    for tag in tags:
        w = len(tag) * 11 + 36
        tag_svg.append(
            f'<rect x="{x}" y="430" width="{w}" height="40" rx="20" fill="none" stroke="{BORDER}" stroke-width="2"/>'
            f'<text x="{x + w / 2}" y="456" text-anchor="middle" class="tag">{escape(tag)}</text>'
        )
        x += w + 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">
  <style>
    .t{{font:700 58px {SANS};fill:{TEXT}}} .s{{font:400 28px {SANS};fill:{MUTED}}}
    .tag{{font:500 18px {MONO};fill:{TEXT}}} .m{{font:16px {MONO};fill:{MUTED}}} .mt{{font:16px {MONO};fill:{TEXT}}}
    .k{{font:600 13px {SANS};fill:{MUTED};letter-spacing:.08em}} .v{{font:700 30px {SANS};fill:{TEXT}}}
  </style>
  <defs>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="#ffffff" stroke-opacity=".035"/>
    </pattern>
    <radialGradient id="glow" cx="78%" cy="45%" r="55%">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity=".18"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  <rect x="80" y="170" width="56" height="6" rx="3" fill="{ACCENT}"/>
  <text x="80" y="260" class="t">{escape(title)}</text>
  <text x="80" y="315" class="s">{escape(subtitle[0])}</text>
  <text x="80" y="353" class="s">{escape(subtitle[1])}</text>
  {"".join(tag_svg)}
  {art}
</svg>
'''


def panel(x, y, w, h, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="2" {extra}/>'


def homelab() -> str:
    ox, oy = 700, 110
    art = [panel(ox, oy, 500, 420)]
    art.append(f'<circle cx="{ox + 26}" cy="{oy + 24}" r="6" fill="#ff5f56"/><circle cx="{ox + 46}" cy="{oy + 24}" r="6" fill="#ffbd2e"/><circle cx="{ox + 66}" cy="{oy + 24}" r="6" fill="#27c93f"/>')
    art.append(f'<text x="{ox + 480}" y="{oy + 30}" text-anchor="end" class="m">homeos.local</text>')
    art.append(f'<path d="M{ox} {oy + 48}h500" stroke="{BORDER}" stroke-width="2"/>')
    # CPU cores
    art.append(panel(ox + 24, oy + 72, 220, 150))
    art.append(f'<text x="{ox + 44}" y="{oy + 102}" class="k">CPU CORES</text>')
    for i, v in enumerate([0.55, 0.8, 0.35, 0.65, 0.45, 0.9]):
        h = 80 * v
        art.append(f'<rect x="{ox + 46 + i * 31}" y="{oy + 200 - h}" width="20" height="{h}" rx="4" fill="{ACCENT}" fill-opacity="{0.45 + v / 2:.2f}"/>')
    # RAM ring
    art.append(panel(ox + 256, oy + 72, 220, 150))
    art.append(f'<text x="{ox + 276}" y="{oy + 102}" class="k">MEMORY</text>')
    cx, cy, r = ox + 366, oy + 158, 40
    circ = 2 * 3.14159 * r
    art.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BORDER}" stroke-width="10"/>')
    art.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACCENT}" stroke-width="10" stroke-linecap="round" '
               f'stroke-dasharray="{circ * 0.62:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy})"/>')
    # module tiles
    for i, name in enumerate(["SYSTEM", "FILES", "MEDIA", "AI STUDIO", "WEB IDE", "MUSIC"]):
        tx, ty = ox + 24 + (i % 3) * 152, oy + 240 + (i // 3) * 80
        art.append(panel(tx, ty, 140, 64))
        art.append(f'<rect x="{tx + 16}" y="{ty + 22}" width="20" height="20" rx="6" fill="{ACCENT}" fill-opacity=".85"/>')
        art.append(f'<text x="{tx + 46}" y="{ty + 38}" class="k">{name}</text>')
    return frame("Homelab-Imperium", ("Self-hosted HomeOS dashboard", "for headless Ubuntu Server machines"),
                 ["Python", "FastAPI", "Docker"], "".join(art),
                 "Cover: Homelab-Imperium – self-hosted HomeOS dashboard")


def osint() -> str:
    ox, oy = 700, 110
    art = [panel(ox, oy, 500, 420)]
    art.append(f'<text x="{ox + 28}" y="{oy + 44}" class="mt"><tspan fill="{OK}">$</tspan> recon --target &lt;username&gt;</text>')
    rows = [("github", True), ("reddit", True), ("instagram", False), ("x.com", True), ("twitch", False)]
    for i, (site, hit) in enumerate(rows):
        y = oy + 88 + i * 30
        mark, color = ("found", ACCENT) if hit else ("none", MUTED)
        art.append(f'<text x="{ox + 28}" y="{y}" class="m">[{i + 1}/5] {site:<10}</text>'
                   f'<text x="{ox + 260}" y="{y}" class="mt" style="fill:{color}">● {mark}</text>')
    art.append(f'<path d="M{ox + 28} {oy + 254}h444" stroke="{BORDER}" stroke-width="2" stroke-dasharray="6 6"/>')
    cx, cy, r = ox + 110, oy + 336, 52
    circ = 2 * 3.14159 * r
    art.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BORDER}" stroke-width="14"/>')
    art.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACCENT}" stroke-width="14" stroke-linecap="round" '
               f'stroke-dasharray="{circ * 0.6:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy})"/>')
    art.append(f'<text x="{cx}" y="{cy + 10}" text-anchor="middle" class="v">AI</text>')
    art.append(f'<text x="{ox + 200}" y="{oy + 316}" class="k">RISK ANALYSIS</text>')
    art.append(f'<text x="{ox + 200}" y="{oy + 346}" class="mt">score 0–100 + summary</text>')
    art.append(f'<text x="{ox + 200}" y="{oy + 374}" class="m">→ HTML / PDF report</text>')
    return frame("OSINT Recon Tool", ("Automated OSINT research", "with AI-based risk analysis"),
                 ["Python", "Rich CLI", "HTML/CSS"], "".join(art),
                 "Cover: OSINT Recon Tool – automated OSINT research with AI risk analysis")


if __name__ == "__main__":
    for name, build in (("cover-homelab-imperium", homelab), ("cover-osint-recon-tool", osint)):
        with open(f"assets/{name}.svg", "w", encoding="utf-8") as f:
            f.write(build())
        print("wrote", f"assets/{name}.svg")
