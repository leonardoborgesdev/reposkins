"""Gerador de avatar - arte deterministica gerada a partir do hash do
username (equivalente a familia 'Originals' do GitSkins). 100% nosso,
sem IA externa nem servico terceiro - so hash + desenho geometrico."""
import hashlib
import io
import math
from PIL import Image, ImageDraw

PALETTES = [
    [(129, 140, 248), (192, 132, 252)],
    [(45, 212, 191), (94, 234, 212)],
    [(34, 211, 238), (96, 165, 250)],
    [(34, 197, 94), (74, 222, 128)],
    [(249, 115, 22), (251, 146, 60)],
    [(236, 72, 153), (244, 114, 182)],
]


def _seed(username):
    h = hashlib.sha256(username.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def render_png(username, size=400):
    seed = _seed(username)
    palette = PALETTES[seed % len(PALETTES)]
    c1, c2 = palette

    img = Image.new("RGB", (size, size), c1)
    draw = ImageDraw.Draw(img)

    for y in range(size):
        ratio = y / size
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b))

    rnd = seed
    cx, cy = size / 2, size / 2
    n_shapes = 5 + (rnd % 4)
    for i in range(n_shapes):
        rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
        angle = (rnd % 360) * math.pi / 180
        rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
        dist = (rnd % (size // 3))
        rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
        radius = 20 + (rnd % (size // 6))
        x = cx + dist * math.cos(angle)
        y = cy + dist * math.sin(angle)
        alpha_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ad = ImageDraw.Draw(alpha_layer)
        ad.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(255, 255, 255, 40))
        img = Image.alpha_composite(img.convert("RGBA"), alpha_layer).convert("RGB")
        draw = ImageDraw.Draw(img)

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    return buf.getvalue()
