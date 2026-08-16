"""Social badges via shields.io - no API call, just builds the URL.
Known gotcha: the LinkedIn logo disappears unless the color is the brand
color #0A66C2 - so it's forced there, regardless of the chosen theme."""
from urllib.parse import quote

_SERVICES = {
    "linkedin": {"label": "LinkedIn", "logo": "linkedin", "color": "0A66C2", "force_color": True},
    "instagram": {"label": "Instagram", "logo": "instagram", "color": None},
    "facebook": {"label": "Facebook", "logo": "facebook", "color": None},
    "email": {"label": "Email", "logo": "gmail", "color": None},
    "portfolio": {"label": "Portfolio", "logo": "vercel", "color": None},
    "x": {"label": "X", "logo": "x", "color": "000000", "force_color": True},
}


def _badge_url(label, logo, color):
    return f"https://img.shields.io/badge/{quote(label)}-{color}.svg?style=for-the-badge&logo={logo}&logoColor=white"


def build_badges(links_raw, theme_bg_hex):
    """links_raw: 'linkedin:https://...,instagram:https://...,email:foo@bar.com'"""
    if not links_raw:
        return ""
    bg = theme_bg_hex.lstrip("#")
    entries = []
    for part in links_raw.split(","):
        part = part.strip()
        if ":" not in part:
            continue
        key, url = part.split(":", 1)
        key = key.strip().lower()
        svc = _SERVICES.get(key)
        if not svc:
            continue
        href = f"mailto:{url}" if key == "email" else url
        color = svc["color"] if svc.get("force_color") else bg
        badge = f'<a href="{href}"><img src="{_badge_url(svc["label"], svc["logo"], color)}" /></a>'
        entries.append(badge)
    return "&nbsp;&nbsp;".join(entries)
