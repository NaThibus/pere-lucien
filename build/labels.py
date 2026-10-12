"""Visuels « étiquette d'atelier » pour les produits sans photographie.

Une étiquette imprimée, posée de travers sur un papier teinté, avec un tampon « fait main ».
Si une vraie photo est déposée plus tard dans assets/img/martine/<slug>.webp, elle remplace l'étiquette.
"""
import math
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

FONTS = Path(__file__).resolve().parent / "fonts"


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


PALETTES = {
    # fond, encre principale, accent (tampon), papier de l'étiquette
    "rose": ((242, 211, 201), (42, 22, 18), (184, 67, 47), (251, 246, 238)),
    "sage": ((217, 225, 211), (23, 32, 26), (77, 104, 79), (250, 248, 240)),
    "stone": ((228, 224, 214), (30, 26, 22), (148, 82, 52), (252, 249, 242)),
    "kraft": ((214, 190, 152), (38, 28, 18), (150, 58, 38), (250, 245, 234)),
    "blue": ((223, 228, 248), (20, 22, 40), (31, 63, 209), (251, 250, 246)),
}


def paper_noise(size, strength=14, seed=1):
    rnd = random.Random(seed)
    w, h = size
    small = Image.new("L", (w // 4, h // 4))
    small.putdata([128 + rnd.randint(-strength, strength) for _ in range(small.width * small.height)])
    return small.resize(size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.2))


def tint(img, noise, amount=0.5):
    n = noise.convert("RGB")
    return ImageChops.overlay(img, n) if amount >= 1 else Image.blend(img, ImageChops.overlay(img, n), amount)


def circle_text(draw, cx, cy, r, text, fnt, fill, start=-90):
    # le texte est répété puis réparti sur tout le cercle
    circ = 2 * math.pi * r
    unit = sum(draw.textlength(ch, font=fnt) for ch in text)
    text = text * max(1, round(circ / (unit * 1.08)))
    total = sum(draw.textlength(ch, font=fnt) for ch in text)
    angle_per_px = 360 / total
    a = start
    for ch in text:
        w = draw.textlength(ch, font=fnt)
        mid = a + (w / 2) * angle_per_px
        rad = math.radians(mid)
        x, y = cx + r * math.cos(rad), cy + r * math.sin(rad)
        glyph = Image.new("RGBA", (int(w * 3) + 8, fnt.size * 2), (0, 0, 0, 0))
        ImageDraw.Draw(glyph).text((glyph.width / 2, glyph.height / 2), ch, font=fnt, fill=fill, anchor="mm")
        glyph = glyph.rotate(-(mid + 90), resample=Image.BICUBIC, expand=True)
        draw._image.alpha_composite(glyph, (int(x - glyph.width / 2), int(y - glyph.height / 2)))
        a += w * angle_per_px


def stamp(size, ink, words, center):
    s = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    c = size / 2
    d.ellipse((6, 6, size - 6, size - 6), outline=ink + (235,), width=5)
    d.ellipse((30, 30, size - 30, size - 30), outline=ink + (235,), width=2)
    circle_text(d, c, c, size / 2 - 52, words, font("geist-mono.ttf", 21), ink + (235,))
    d.text((c, c + 2), center, font=font("archivo-wide-italic.ttf", 58), fill=ink + (235,), anchor="mm")
    # usure de l'encre
    mask = paper_noise((size, size), 60, seed=7).point(lambda v: 255 if v > 112 else 120)
    alpha = ImageChops.multiply(s.split()[-1], mask)
    s.putalpha(alpha)
    return s


def fit(draw, text, fname, size, maxw):
    f = font(fname, size)
    while draw.textlength(text, font=f) > maxw and size > 12:
        size -= 1
        f = font(fname, size)
    return f


def make_label(dest, brand, name, kind, size_line, palette="rose", seed=0):
    bg, ink, accent, paper = PALETTES[palette]
    W = 1024
    img = Image.new("RGB", (W, W), bg)
    img = tint(img, paper_noise((W, W), 16, seed), 0.55).convert("RGBA")

    # étiquette
    LW, LH = 640, 780
    lab = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lab)
    notch = 34
    poly = [(notch, 0), (LW - notch, 0), (LW, notch), (LW, LH - notch), (LW - notch, LH), (notch, LH), (0, LH - notch), (0, notch)]
    d.polygon(poly, fill=paper + (255,))
    inner = [(notch + 4, 16), (LW - notch - 4, 16), (LW - 16, notch + 4), (LW - 16, LH - notch - 4), (LW - notch - 4, LH - 16),
             (notch + 4, LH - 16), (16, LH - notch - 4), (16, notch + 4)]
    d.line(inner + [inner[0]], fill=ink + (200,), width=2)
    inner2 = [(x + (6 if x < LW / 2 else -6), y + (6 if y < LH / 2 else -6)) for x, y in inner]
    d.line(inner2 + [inner2[0]], fill=ink + (120,), width=1)

    cx = LW / 2
    if brand == "martine":
        d.text((cx, 92), "Mère Martine", font=font("archivo-wide-italic.ttf", 50), fill=accent + (255,), anchor="mm")
        house = "SOINS FAITS MAIN · ALLIER"
        name_font = font("archivo-wide.ttf", 54)
        wrap = 16
    else:
        d.text((cx, 92), "LE PÈRE LUCIEN", font=font("archivo-cond-black.ttf", 52), fill=accent + (255,), anchor="mm")
        house = "SAVONNERIE · TEILLET-ARGENTY"
        name_font = font("archivo-cond-black.ttf", 58)
        name = name.upper()
        wrap = 18
    d.text((cx, 142), house, font=font("geist-mono.ttf", 18), fill=ink + (190,), anchor="mm")
    d.line((120, 176, LW - 120, 176), fill=ink + (160,), width=1)

    lines = textwrap.wrap(name, wrap)[:4]
    lh = name_font.size * 1.12
    y = 300 - (len(lines) - 1) * lh / 2
    for ln in lines:
        d.text((cx, y), ln, font=name_font, fill=ink + (255,), anchor="mm")
        y += lh
    y += 18
    for ln in textwrap.wrap(kind, 30)[:2]:
        d.text((cx, y), ln, font=fit(d, ln, "geist.ttf", 27, LW - 140), fill=ink + (200,), anchor="mm")
        y += 36
    d.line((cx - 40, LH - 214, cx + 40, LH - 214), fill=accent + (220,), width=3)
    size_line = ", ".join(size_line.split(", ")[:2])
    d.text((cx, LH - 176), size_line, font=fit(d, size_line, "geist-mono.ttf", 24, LW - 130), fill=ink + (230,), anchor="mm")
    d.text((cx - 40, LH - 110), "fait main dans l'Allier", font=font("homemade-apple.ttf", 28), fill=accent + (235,), anchor="mm")

    # grain du papier de l'étiquette
    pn = paper_noise((LW, LH), 10, seed + 3).convert("RGB")
    rgb = Image.blend(lab.convert("RGB"), ImageChops.multiply(lab.convert("RGB"), pn.point(lambda v: min(255, v + 120))), 0.35)
    lab = Image.merge("RGBA", (*rgb.split(), lab.split()[-1]))

    rot = (-2.5 if seed % 2 else 2) + (seed % 3) * 0.6
    lab_r = lab.rotate(rot, resample=Image.BICUBIC, expand=True)
    shadow = Image.new("RGBA", lab_r.size, (0, 0, 0, 0))
    shadow.putalpha(lab_r.split()[-1].point(lambda a: int(a * 0.28)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    ox, oy = (W - lab_r.width) // 2, (W - lab_r.height) // 2 - 6
    img.alpha_composite(shadow, (ox + 14, oy + 22))
    img.alpha_composite(lab_r, (ox, oy))

    st = stamp(250, accent, "FAIT MAIN · ALLIER · DEPUIS 2013 · ", "MM" if brand == "martine" else "PL")
    st = st.rotate(-14 + (seed % 5) * 6, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(st, (W - st.width - 34, W - st.height - 30))

    img.convert("RGB").save(dest, "WEBP", quality=84)
    sm = Path(str(dest).replace(".webp", "-sm.webp"))
    im = Image.open(dest)
    im.thumbnail((560, 560), Image.LANCZOS)
    im.save(sm, "WEBP", quality=80)
    return dest


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "site" / "assets" / "img" / "martine"
    make_label(out / "_test-label.webp", "martine", "Lait hydratant parfumé", "Rose et iris, texture fluide", "250 ml · flacon pompe verre", "rose", 3)
    make_label(out / "_test-label2.webp", "lucien", "Savon du barbier traditionnel", "Savon à raser, 200 g", "pot acier rechargeable", "blue", 2)
    print("ok")
