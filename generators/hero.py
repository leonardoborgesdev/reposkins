"""Hero card - clone pixel-perfeito do GitSkins, gerado por template.
Usa o SVG de referencia REAL de CADA tema (baixado uma vez, guardado
em reference/themes/hero_<tema>.svg) como molde e substitui os dados
dinamicos (nome, bio, stars, avatar, linguagens). NAO chama
gitskins.com em nenhum momento - 100% independente."""
import os
import re
import base64
from xml.sax.saxutils import escape as xesc
from github_api import get_avatar_bytes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
THEMES_DIR = os.path.join(BASE_DIR, "..", "reference", "themes")
FALLBACK_PATH = os.path.join(THEMES_DIR, "hero_midnight.svg")

_TEMPLATES = {}


def _load_template(theme_name):
    if theme_name in _TEMPLATES:
        return _TEMPLATES[theme_name]
    path = os.path.join(THEMES_DIR, f"hero_{theme_name}.svg")
    if not os.path.exists(path):
        path = FALLBACK_PATH
    with open(path, encoding="utf-8") as f:
        text = f.read()
    _TEMPLATES[theme_name] = text
    return text


# valores originais capturados no template (username=leonardoborgesdev)
_ORIG = {
    "stars": "4",
    "handle": "@leonardoborgesdev",
    "name": "Borges Dev",
    "bio": "Full-Stack AI Engineer | Founder of ship-safe 🛡️ Building local-first, open-source securit…",
    "langs": ["TypeScript", "HTML", "Python", "JavaScript"],
    "id_prefix": "leonardoborgesdev",
}


def render(username, data, theme_name="midnight"):
    user = data["user"]
    svg = _load_template(theme_name)

    avatar_bytes = get_avatar_bytes(user.get("avatar_url", ""))
    new_avatar_b64 = base64.b64encode(avatar_bytes).decode("ascii")
    svg = re.sub(
        r'(xlink:href="data:image/[a-zA-Z]+;base64,)[^"]+(")',
        lambda m: m.group(1) + new_avatar_b64 + m.group(2),
        svg, count=1,
    )

    svg = svg.replace(_ORIG["id_prefix"], username)
    svg = svg.replace(f">{_ORIG['stars']}<", f">{xesc(str(data['stars']))}<", 1)
    svg = svg.replace(f">{_ORIG['handle']}<", f">@{xesc(username)}<", 1)
    svg = svg.replace(f">{xesc(_ORIG['name'])}<", f">{xesc(user.get('name') or username)}<", 1)
    bio = (user.get("bio") or f"Building on GitHub as @{username}")[:90]
    svg = svg.replace(f">{xesc(_ORIG['bio'])}<", f">{xesc(bio)}<", 1)

    langs = [l["name"] for l in data["langs"][:4]]
    for i, old_lang in enumerate(_ORIG["langs"]):
        new_lang = langs[i] if i < len(langs) else ""
        svg = svg.replace(f">{xesc(old_lang)}<", f">{xesc(new_lang)}<", 1)

    svg = svg.replace("gitskins.com", "reposkins.pro")
    return svg
