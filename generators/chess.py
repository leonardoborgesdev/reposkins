"""Replay de xadrez automatico - decorativo (nao e um jogo real, so
uma cena bonita pro README, no mesmo espirito do card original)."""
from svg_kit import card_shell, theme

PIECES = {
    "r": "&#9820;", "n": "&#9822;", "b": "&#9821;", "q": "&#9819;", "k": "&#9818;", "p": "&#9823;",
    "R": "&#9814;", "N": "&#9816;", "B": "&#9815;", "Q": "&#9813;", "K": "&#9812;", "P": "&#9817;",
}

START = [
    "rnbqkbnr",
    "pppppppp",
    "........",
    "........",
    "........",
    "....P...",
    "PPPP.PPP",
    "RNBQKBNR",
]


def render(username, data, theme_name="midnight"):
    t = theme(theme_name)
    size = 78
    x0, y0 = 60, 60
    squares = []
    pieces = []
    for r in range(8):
        for c in range(8):
            light = (r + c) % 2 == 0
            color = f"{t['accent']}22" if light else "#00000040"
            x, y = x0 + c * size, y0 + r * size
            squares.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}"/>')
            ch = START[r][c]
            if ch != ".":
                glyph = PIECES[ch]
                fill = t["text"] if ch.isupper() else t["accent"]
                pieces.append(
                    f'<text x="{x+size/2}" y="{y+size*0.72}" font-size="{size*0.7}" '
                    f'fill="{fill}" text-anchor="middle">{glyph}</text>'
                )
    board_w = 8 * size
    body = f'''<text x="30" y="38" font-family="sans-serif" font-size="18" font-weight="700" fill="{t['accent']}">Automatic Chess Replay</text>
  <rect x="{x0-4}" y="{y0-4}" width="{board_w+8}" height="{board_w+8}" rx="10" fill="none" stroke="{t['accent']}66" stroke-width="2"/>
  {"".join(squares)}
  {"".join(pieces)}'''
    return card_shell(board_w + 120, y0 + board_w + 60, body, theme_name)
