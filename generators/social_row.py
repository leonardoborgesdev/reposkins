from svg_kit import card_shell, theme, xesc


def render(username, data, theme_name="midnight", links_raw=""):
    t = theme(theme_name)
    user = data["user"]
    links = []
    for part in links_raw.split("|"):
        if "::" in part:
            label, value = part.split("::", 1)
            links.append((label, value))
    if not links:
        if user.get("blog"):
            links.append(("Website", user["blog"]))
        links.append(("GitHub", f"github.com/{username}"))

    chips = []
    x = 30
    for label, value in links[:4]:
        text = f"{label}: {value}"
        w = 24 + len(text) * 6.5
        chips.append(f'''<rect x="{x}" y="30" width="{w}" height="40" rx="20" fill="#00000030" stroke="{t['accent']}66"/>
  <text x="{x+w/2}" y="55" font-family="sans-serif" font-size="13" fill="{t['text']}" text-anchor="middle">{xesc(text)}</text>''')
        x += w + 14
    body = "".join(chips)
    return card_shell(max(860, int(x) + 20), 100, body, theme_name)
