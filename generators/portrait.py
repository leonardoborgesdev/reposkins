"""Retrato ASCII a partir da foto real do usuario - gerado por nos,
sem chamar nenhum servico externo alem da propria API do GitHub pra
pegar o avatar."""
import io
from PIL import Image, ImageOps
from svg_kit import card_shell, theme, xesc
from github_api import get_avatar_bytes

RAMP = " .:-=+*#%@"
COLS = 70
CHAR_W = 8.6
CHAR_H = 15.5


def render(username, data, theme_name="midnight"):
    t = theme(theme_name)
    avatar_url = data["user"].get("avatar_url", "")
    img_bytes = get_avatar_bytes(avatar_url)
    img = Image.open(io.BytesIO(img_bytes)).convert("L")
    img = ImageOps.autocontrast(img, cutoff=2)
    w, h = img.size
    aspect = h / w
    rows = int(COLS * aspect * (CHAR_W / CHAR_H))
    rows = max(20, min(rows, 60))
    small = img.resize((COLS, rows))
    pixels = list(small.getdata())

    lines = []
    for r in range(rows):
        row = "".join(RAMP[int((pixels[r * COLS + c] / 255) * (len(RAMP) - 1))] for c in range(COLS))
        lines.append(row)

    top_pad = 60
    text_elems = []
    for i, line in enumerate(lines):
        y = top_pad + i * CHAR_H
        text_elems.append(
            f'<text x="30" y="{y:.1f}" font-family="ui-monospace,Menlo,Consolas,monospace" '
            f'font-size="{CHAR_H-1.5:.1f}" fill="{t["text"]}" xml:space="preserve">{xesc(line)}</text>'
        )

    width = 860
    height = 60 + rows * CHAR_H + 30
    body = f'''<circle cx="24" cy="24" r="6" fill="#ff5f56"/>
  <circle cx="44" cy="24" r="6" fill="#ffbd2e"/>
  <circle cx="64" cy="24" r="6" fill="#27c93f"/>
  <text x="{width/2}" y="29" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="12.5" fill="{t['muted']}" text-anchor="middle">{xesc(username)}@github: ~$ ./portrait.sh</text>
  {"".join(text_elems)}'''
    return card_shell(width, int(height), body, theme_name, radius=14)
