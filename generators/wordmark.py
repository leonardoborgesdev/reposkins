from svg_kit import card_shell, theme, xesc


def render(username, data, theme_name="midnight", label=None):
    t = theme(theme_name)
    text = xesc((label or data["user"].get("name") or username).upper())
    body = f'''<text x="430" y="30" font-family="monospace" font-size="12" fill="{t['muted']}" text-anchor="middle">{xesc(username)}@github: ~$ ./wordmark.sh --name</text>
  <text x="430" y="130" font-family="sans-serif" font-size="54" font-weight="800" fill="{t['text']}" text-anchor="middle" letter-spacing="3">{text}</text>
  <text x="430" y="165" font-family="monospace" font-size="13" fill="{t['accent']}" text-anchor="middle">&gt; _</text>'''
    return card_shell(860, 190, body, theme_name)
