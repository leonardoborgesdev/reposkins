"""Highlights card - real GitSkins template, substituted like hero.py.
The downloaded reference (reference/cards/highlights.svg) only has ONE chip
box, because it was captured with a single item. Its exact styling
(box radius, accent bar, text offsets, chip fade-in animation) is reused
as a repeating unit for however many items the user actually passes -
same real colors and layout math, generalized past what the single
capture shows."""
import os
from xml.sax.saxutils import escape as xesc
from svg_kit import theme

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "..", "reference", "cards", "highlights.svg")

_ORIG_ID_PREFIX = "leonardoborgesdev"

BOX_X, BOX_W, BOX_H, BOX_RX = 28, 804, 96, 16
BOX_GAP = 12
TOP_OFFSET = 60   # distance from svg top to first box (matches the real template)
BOTTOM_MARGIN = 24  # room left below the last box for the watermark


def render(username, data, theme_name="midnight", items_raw=""):
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()

    items = []
    for part in items_raw.split("|"):
        part = part.strip()
        if not part:
            continue
        if "::" in part:
            title, desc = part.split("::", 1)
        else:
            title, desc = part, ""
        items.append((title.strip(), desc.strip()))
    if not items:
        items = [("Open source", "Building in public")]

    height = TOP_OFFSET + len(items) * BOX_H + (len(items) - 1) * BOX_GAP + BOTTOM_MARGIN

    # defs/style/background/title/border come from the real template - swap
    # only the id prefix, the outer <svg> size, and rebuild the chip boxes.
    head, _, _ = template.partition('<g class="aura-chip"')
    head = head.replace(_ORIG_ID_PREFIX, username)
    head = head.replace('width="860" height="180" viewBox="0 0 860 180"',
                         f'width="860" height="{height}" viewBox="0 0 860 {height}"')
    head = head.replace('<rect width="860" height="180" rx="20"',
                         f'<rect width="860" height="{height}" rx="20"')

    chips = []
    for i, (title, desc) in enumerate(items):
        y = TOP_OFFSET + i * (BOX_H + BOX_GAP)
        accent_y = y + 22
        chips.append(f'''<g class="aura-chip" style="animation-delay:{i * 90}ms">
      <rect x="{BOX_X}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="{BOX_RX}" fill="rgba(8,8,12,0.5)" stroke="#818cf8" stroke-opacity="0.7"/>
      <rect x="{BOX_X}" y="{accent_y}" width="4" height="52" rx="2" fill="#7884f7"/>
      <text x="{BOX_X + 24}" y="{y + 38}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="16" font-weight="850" fill="#e0e7ff">{xesc(title)}</text>
      <text x="{BOX_X + 24}" y="{y + 62}" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="12.5" fill="#a5b4fc">{xesc(desc)}</text>
    </g>''')

    watermark_y = height - 11
    tail = (
        "".join(chips)
        + f'\n    <text x="847" y="{watermark_y}" text-anchor="end" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif" font-size="10" font-weight="600" letter-spacing="0.3" fill="#a5b4fc" fill-opacity="0.42">reposkins.pro</text>'
        + f'\n    <rect x="0.5" y="0.5" width="859" height="{height - 1}" rx="19.5" fill="none" stroke="#818cf8" stroke-opacity="0.62"/>'
        + "\n  </g>\n</svg>\n"
    )

    return head + tail
