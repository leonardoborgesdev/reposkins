"""Helpers shared by all generators - card shell (per-theme gradient
background, rounded corners, watermark) and XML text escaping."""
import json
import os
from xml.sax.saxutils import escape as esc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "themes", "palettes.json"), encoding="utf-8") as f:
    PALETTES = json.load(f)

BRAND = "reposkins.pro"


def theme(name):
    return PALETTES.get(name, PALETTES["midnight"])


def card_shell(width, height, body, theme_name="midnight", radius=20):
    t = theme(theme_name)
    bg0, bg1, bg2 = t["bg"]
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg0}"/>
      <stop offset="40%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="{radius}" fill="url(#bg)" stroke="{t['accent']}66" stroke-width="1.5"/>
  {body}
  <text x="{width-14}" y="{height-12}" font-family="sans-serif" font-size="10" fill="{t['muted']}88" text-anchor="end">{BRAND}</text>
</svg>"""


def xesc(s):
    return esc(str(s or ""))
