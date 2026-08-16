"""Card 'system-scan': mini retrato ASCII (VISUAL.MAP) + painel de
dados reais (SYSTEM.INFO), nosso, sem chamar servico externo."""
import io
from PIL import Image, ImageOps
from svg_kit import card_shell, theme, xesc
from github_api import get_avatar_bytes

RAMP = " .:-=+*#%@"
COLS, ROWS = 34, 28


def _mini_ascii(avatar_url):
    img_bytes = get_avatar_bytes(avatar_url)
    img = Image.open(io.BytesIO(img_bytes)).convert("L")
    img = ImageOps.autocontrast(img, cutoff=2)
    small = img.resize((COLS, ROWS))
    pixels = list(small.getdata())
    lines = []
    for r in range(ROWS):
        row = "".join(RAMP[int((pixels[r * COLS + c] / 255) * (len(RAMP) - 1))] for c in range(COLS))
        lines.append(row)
    return lines


def render(username, data, theme_name="midnight"):
    t = theme(theme_name)
    user = data["user"]
    lines = _mini_ascii(user.get("avatar_url", ""))
    map_text = []
    for i, line in enumerate(lines):
        y = 100 + i * 11.6
        map_text.append(
            f'<text x="36" y="{y:.1f}" font-family="ui-monospace,Menlo,Consolas,monospace" '
            f'font-size="10" fill="{t["accent"]}" xml:space="preserve">{xesc(line)}</text>'
        )

    info_rows = [
        ("Subject", user.get("name") or username),
        ("Handle", f"@{username}"),
        ("Bio", (user.get("bio") or "")[:40]),
        ("Repositories", data["repos_count"]),
        ("Contributions", data["contrib_total"]),
        ("Stars", data["stars"]),
        ("Followers", data["followers"]),
        ("Contact", f"github.com/{username}"),
    ]
    info_text = []
    for i, (label, value) in enumerate(info_rows):
        y = 100 + i * 32
        info_text.append(f'''<text x="544" y="{y}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" font-weight="800" fill="{t['accent']}">{xesc(label)}</text>
  <text x="544" y="{y+16}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="{t['text']}">{xesc(value)}</text>''')

    body = f'''<text x="30" y="27" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="12" fill="{t['accent']}" text-anchor="middle" transform="translate(560,0)">{xesc(username)}@github ~ $ ./profile-scan --live</text>
  <text x="{860-40}" y="26" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="10" font-weight="800" fill="{t['accent2']}" text-anchor="end">LIVE</text>
  <rect x="30" y="60" width="480" height="{110+ROWS*11.6}" rx="10" fill="#00000030" stroke="{t['accent']}4d"/>
  <text x="38" y="84" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="10" font-weight="800" letter-spacing="2" fill="{t['accent']}">VISUAL.MAP</text>
  {"".join(map_text)}
  <rect x="524" y="60" width="306" height="{110+ROWS*11.6}" rx="10" fill="#00000030" stroke="{t['accent']}4d"/>
  <text x="544" y="84" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="10" font-weight="800" letter-spacing="2" fill="{t['accent']}">SYSTEM.INFO</text>
  {"".join(info_text)}'''
    return card_shell(860, int(140 + ROWS * 11.6), body, theme_name)
