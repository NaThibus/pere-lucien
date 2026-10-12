"""Logo Mère Martine : médaillon crème, couronne de feuillage et de fleurs, nom en capitales à empattements.

Redessiné en vectoriel d'après le logo de la page Facebook « La Mère Martine ».
Le texte est converti en tracés : le fichier s'affiche partout sans police installée.
Usage : python build/logo.py  ->  site/assets/img/logo-mere-martine.svg
"""
import math
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = Path(__file__).resolve().parent / "fonts"
OUT = Path(__file__).resolve().parent.parent / "site" / "assets" / "img" / "logo-mere-martine.svg"

INK = "#5A3330"
LEAF = ("#7E9070", "#5F7352", "#98A784")
FLOWERS = ("#D98A9B", "#9C86B8", "#E3A33B", "#E9B7C0")
RING = "#B98B6E"
CREAM = "#FBF4EC"


def text_path(font_file, text, size, cx, baseline, tracking=0.0):
    f = TTFont(str(FONTS / font_file))
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm
    scale = size / upm
    names = [cmap[ord(c)] for c in text]
    widths = [gs[n].width * scale for n in names]
    total = sum(widths) + tracking * size * (len(text) - 1)
    x = cx - total / 2
    d = []
    for n, w in zip(names, widths):
        pen = SVGPathPen(gs)
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x, baseline))
        gs[n].draw(tpen)
        d.append(pen.getCommands())
        x += w + tracking * size
    return " ".join(d)


def leaf(x, y, angle, length=17, width=6.5, color=LEAF[0]):
    return (f'<ellipse cx="0" cy="0" rx="{length / 2:.1f}" ry="{width / 2:.1f}" fill="{color}" '
            f'transform="translate({x:.1f} {y:.1f}) rotate({angle:.1f}) translate({length / 2:.1f} 0)"/>')


def flower(x, y, r, color):
    petals = "".join(f'<circle cx="{x + r * math.cos(math.radians(a)):.1f}" cy="{y + r * math.sin(math.radians(a)):.1f}" r="{r * .78:.1f}" fill="{color}"/>'
                     for a in range(-90, 270, 72))
    return petals + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * .55:.1f}" fill="#F3D27A"/>'


def build():
    C, R = 200, 150
    parts = [f'<circle cx="{C}" cy="{C}" r="196" fill="{CREAM}"/>',
             f'<circle cx="{C}" cy="{C}" r="188" fill="none" stroke="{RING}" stroke-width="1.6"/>',
             f'<circle cx="{C}" cy="{C}" r="182" fill="none" stroke="{RING}" stroke-width=".8" stroke-dasharray="2 4"/>']
    # deux branches qui partent du bas et se rejoignent en haut
    stem = []
    for side in (-1, 1):
        pts = []
        for k in range(0, 33):
            a = math.radians(90 + side * (12 + k * 5.2))
            pts.append((C + R * math.cos(a), C + R * math.sin(a)))
        stem.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts))
        for k in range(1, 32):
            a_deg = 90 + side * (12 + k * 5.2)
            a = math.radians(a_deg)
            x, y = C + R * math.cos(a), C + R * math.sin(a)
            tangent = a_deg + side * 90
            col = LEAF[k % 3]
            parts.append(leaf(x, y, tangent - side * 38, 18 - (k % 3) * 2, 6.5, col))
            parts.append(leaf(x, y, tangent + side * 32 + 180 * 0, 15 - (k % 2) * 2, 5.5, LEAF[(k + 1) % 3]))
    parts.insert(3, f'<path d="{" ".join(stem)}" fill="none" stroke="{LEAF[1]}" stroke-width="1.4" stroke-linecap="round"/>')
    # fleurs
    for i, (deg, r) in enumerate([(130, 9), (175, 7), (218, 10), (262, 7), (300, 8), (345, 10), (30, 7), (65, 9), (100, 6), (80, 6)]):
        a = math.radians(deg)
        parts.append(flower(C + R * math.cos(a), C + R * math.sin(a), r, FLOWERS[i % 4]))
    # fleur centrale en bas, là où les branches se rejoignent
    parts.append(flower(C, C + R + 2, 11, FLOWERS[0]))
    # texte
    t1 = text_path("cormorant-semibold.ttf", "LA MÈRE", 40, C, 180, 0.12)
    t2 = text_path("cormorant-semibold.ttf", "MARTINE", 47, C, 230, 0.09)
    t3 = text_path("cormorant-italic.ttf", "Cosmétique naturelle", 21, C, 262, 0.02)
    parts.append(f'<path d="{t1}" fill="{INK}"/><path d="{t2}" fill="{INK}"/><path d="{t3}" fill="{INK}" opacity=".85"/>')
    parts.append(f'<path d="M{C - 52},{C + 42} H{C + 52}" stroke="{RING}" stroke-width="1"/>')
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" role="img" aria-label="La Mère Martine, cosmétique naturelle">'
           + "".join(parts) + "</svg>")
    OUT.write_text(svg, encoding="utf-8")
    return OUT


if __name__ == "__main__":
    print(build())
