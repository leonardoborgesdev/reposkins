from svg_kit import card_shell, theme, xesc


def render(username, data, theme_name="midnight", items_raw=""):
    t = theme(theme_name)
    items = []
    for part in items_raw.split("|"):
        if "::" in part:
            title, desc = part.split("::", 1)
            items.append((title, desc))
    if not items:
        items = [("Open source", "Building in public")]
    cards = []
    w = (860 - 60 - (len(items) - 1) * 15) / len(items)
    for i, (title, desc) in enumerate(items):
        x = 30 + i * (w + 15)
        cards.append(f'''<rect x="{x}" y="65" width="{w}" height="100" rx="12" fill="#00000030" stroke="{t['accent']}4d"/>
  <rect x="{x}" y="65" width="4" height="100" rx="2" fill="{t['accent']}"/>
  <text x="{x+20}" y="100" font-family="sans-serif" font-size="15" font-weight="700" fill="{t['text']}">{xesc(title)}</text>
  <text x="{x+20}" y="122" font-family="sans-serif" font-size="12" fill="{t['muted']}">{xesc(desc[:35])}</text>''')
    body = f'''<text x="30" y="35" font-family="sans-serif" font-size="11" font-weight="700" fill="{t['accent']}" letter-spacing="2">HIGHLIGHTS</text>
  {"".join(cards)}'''
    return card_shell(860, 185, body, theme_name)
