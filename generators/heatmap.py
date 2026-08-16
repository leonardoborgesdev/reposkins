from svg_kit import card_shell, theme


def render(username, data, theme_name="midnight", style="default"):
    t = theme(theme_name)
    weeks = data["contrib_weeks"]
    cells = []
    x0, y0, cell, gap = 30, 70, 11, 3
    ship_col = None
    if style in ("jet", "snake"):
        for wi, week in enumerate(weeks):
            for di, day in enumerate(week.get("contributionDays", [])):
                if day["contributionCount"] > 0:
                    ship_col = wi
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

    extra = ""
    title = "Contribution Activity"
    if style == "jet":
        title = "Jet — Contribution Game"
        if ship_col is not None:
            sx = x0 + ship_col * (cell + gap)
            extra = f'<text x="{sx}" y="{y0+7*(cell+gap)+14}" font-size="16" fill="{t["accent2"]}">&#9650;</text>'
    elif style == "snake":
        title = "Snake Trail"
        extra = f'<circle cx="{x0+30}" cy="{y0+30}" r="6" fill="{t["accent2"]}"/>'
    elif style == "erased":
        title = "Eraser"

    body = f'''<text x="30" y="38" font-family="sans-serif" font-size="18" font-weight="700" fill="{t['accent']}">{title}</text>
  <text x="30" y="58" font-family="sans-serif" font-size="12" fill="{t['muted']}">{data['contrib_total']} contributions in the last year</text>
  {"".join(cells)}
  {extra}'''
    return card_shell(860, 200, body, theme_name)
