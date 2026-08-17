"""Wordmark card - real GitSkins ASCII block font (see wordmark_font.py),
assembled fresh for any name. Same terminal-window chrome as the original
(traffic-light dots, prompt bar, cursor), rendered as static text (no
flicker animation - the real card blinks each row via a discrete opacity
loop, which doesn't matter for a still screenshot or a settled README)."""
from xml.sax.saxutils import escape as xesc
from .wordmark_font import render_block, ROWS

FONT_SIZE = 14.3
CHAR_WIDTH = 9.31
ROW_STEP = 15.5
LEFT_MARGIN = 18
TOP_MARGIN = 99.8
HEADER_HEIGHT = 41.2
BOTTOM_PAD = 41.2


def render(username, data, theme_name="midnight", label=None):
    name = (label or data["user"].get("name") or username).upper()
    block = render_block(name)

    content_width = max(len(row) for row in block) * CHAR_WIDTH
    width = int(LEFT_MARGIN * 2 + content_width)
    height = int(TOP_MARGIN - HEADER_HEIGHT + ROWS * ROW_STEP + BOTTOM_PAD + HEADER_HEIGHT)

    rows_svg = []
    y = TOP_MARGIN
    for line in block:
        rows_svg.append(
            f'<text xml:space="preserve" x="{LEFT_MARGIN}" y="{y:.1f}" '
            f'font-family="ui-monospace,\'SF Mono\',SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="{FONT_SIZE}" fill="#c9d1d9">{xesc(line)}</text>'
        )
        y += ROW_STEP

    prompt = xesc(f"{username}@github: ~$ ./wordmark.sh --name")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="wm-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0b0e14"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="url(#wm-bg)" stroke="#2a3038"/>
  <path d="M0.5 12 a11 11 0 0 1 11 -11 h{width - 24} a11 11 0 0 1 11 11 v22 h-{width - 2} z" fill="#161b22"/>
  <rect x="0.5" y="34" width="{width - 1}" height="1" fill="#2a3038"/>
  <circle cx="22" cy="17.5" r="6" fill="#ff5f56"/><circle cx="42" cy="17.5" r="6" fill="#ffbd2e"/><circle cx="62" cy="17.5" r="6" fill="#27c93f"/>
  <text x="{width / 2:.1f}" y="22" text-anchor="middle" font-family="ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace" font-size="12.5" fill="#8b949e">{prompt}</text>
  {"".join(rows_svg)}
  <text x="{width - 13}" y="{height - 11}" text-anchor="end" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="10" font-weight="600" letter-spacing="0.3" fill="#8b949e" fill-opacity="0.42">reposkins.pro</text>
</svg>
'''
