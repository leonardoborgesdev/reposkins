"""Heatmap card - real GitSkins template, substituted like hero.py.
The grid is 53 columns x 7 rows, each cell wrapped in its own
<g transform="translate(x,y)">...</g>, in column-major document order.
Real per-day contribution counts (from GraphQL) are mapped onto that same
371-cell sequence, positionally - week[0] of our data lines up with
column 0 of the template regardless of actual calendar dates, same
assumption the original from-scratch version used.

Style variants (jet/snake/erased) don't have their own real templates the
way "default" does, so they still fall back to a simple from-scratch
render - clearly worse than default, but honest about it rather than
silently reusing the default template with a misleading label."""
import os
import re
from xml.sax.saxutils import escape as xesc
from svg_kit import card_shell, theme

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "..", "reference", "cards", "heatmap-default.svg")

_ORIG = {
    "count_line": "79 contributions in the last year",
    "id_prefix": "leonardoborgesdev",
}

_GROUP_RE = re.compile(r'<g transform="translate\(([0-9.]+),([0-9.]+)\)">.*?</g>', re.S)

# (fill, fill-opacity) per bucket 0..4, matching the template's own "Less...More" legend
_BUCKETS = [
    ("#e0e7ff", "0.07"),
    ("#7884f7", "0.34"),
    ("#7884f7", "0.55"),
    ("#7884f7", "0.78"),
    ("#7884f7", "1"),
]


def _bucket(count):
    if count <= 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 9:
        return 3
    return 4


def _cell_svg(x, y, fill, opacity):
    return f'<g transform="translate({x},{y})"><rect x="-5.5" y="-5.5" width="11" height="11" rx="2.5" fill="{fill}" fill-opacity="{opacity}"/></g>'


def _render_default(username, data, theme_name):
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        svg = f.read()

    weeks = data.get("contrib_weeks") or []
    # flatten to per-column (week) lists of 7 day-counts, positionally matched to the template's 53 columns
    columns = []
    for week in weeks[-53:]:
        days = week.get("contributionDays", [])
        counts = [d.get("contributionCount", 0) for d in days]
        counts += [0] * (7 - len(counts))
        columns.append(counts[:7])
    while len(columns) < 53:
        columns.append([0] * 7)

    groups = list(_GROUP_RE.finditer(svg))
    if len(groups) == 371:
        pieces = []
        last_end = 0
        for i, m in enumerate(groups):
            col, row = i // 7, i % 7
            count = columns[col][row] if col < len(columns) else 0
            fill, opacity = _BUCKETS[_bucket(count)]
            pieces.append(svg[last_end:m.start()])
            pieces.append(_cell_svg(m.group(1), m.group(2), fill, opacity))
            last_end = m.end()
        pieces.append(svg[last_end:])
        svg = "".join(pieces)

    svg = svg.replace(_ORIG["id_prefix"], username)
    count_line = f"{data['contrib_total']} contributions in the last year"
    svg = svg.replace(f">{xesc(_ORIG['count_line'])}<", f">{xesc(count_line)}<", 1)
    svg = svg.replace("gitskins.com", "reposkins.pro")
    return svg


def _render_fallback(username, data, theme_name, style):
    t = theme(theme_name)
    weeks = data["contrib_weeks"]
    cells = []
    x0, y0, cell, gap = 30, 70, 11, 3
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week.get("contributionDays", [])):
            count = day["contributionCount"]
            if count == 0:
                color = 'rgba(255,255,255,0.06)'
            elif count < 3:
                color = f"{t['accent']}4d"
            elif count < 6:
                color = f"{t['accent']}99"
            else:
                color = t["accent"]
            cx, cy = x0 + wi * (cell + gap), y0 + di * (cell + gap)
            cells.append(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" rx="2" fill="{color}"/>')

    title = {"jet": "Jet — Contribution Game", "snake": "Snake Trail (fallback)", "erased": "Eraser"}.get(style, "Contribution Activity")
    body = f'''<text x="30" y="38" font-family="sans-serif" font-size="18" font-weight="700" fill="{t['accent']}">{title}</text>
  <text x="30" y="58" font-family="sans-serif" font-size="12" fill="{t['muted']}">{data['contrib_total']} contributions in the last year</text>
  {"".join(cells)}'''
    return card_shell(860, 200, body, theme_name)


def render(username, data, theme_name="midnight", style="default"):
    if style == "default":
        return _render_default(username, data, theme_name)
    return _render_fallback(username, data, theme_name, style)
