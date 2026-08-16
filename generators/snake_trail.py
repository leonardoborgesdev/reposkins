"""Snake Trail card - real GitSkins template, substituted like hero.py.
The snake's motion path sweeps a fixed zigzag route over the grid geometry
(same for any user - it's decorative, not literally "eating" specific
contribution days), so only the id prefix, watermark and headline count
need substitution to get a pixel-perfect, per-user result."""
import os
from xml.sax.saxutils import escape as xesc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "..", "reference", "cards", "heatmap-snake.svg")

_ORIG = {
    "count_line": "79 contributions, one continuous run",
    "id_prefix": "leonardoborgesdev",
}


def render(username, data, theme_name="midnight"):
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        svg = f.read()

    svg = svg.replace(_ORIG["id_prefix"], username)
    count_line = f"{data['contrib_total']} contributions, one continuous run"
    svg = svg.replace(f">{xesc(_ORIG['count_line'])}<", f">{xesc(count_line)}<", 1)
    svg = svg.replace("gitskins.com", "reposkins.pro")
    return svg
