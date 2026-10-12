"""Télécharge les photos produits Le Père Lucien (2 max par produit) et les convertit en WebP.

Usage : python build/fetch_images.py
Lit data/produits-lucien.json, écrit site/assets/produits/{slug}-{n}.webp
et data/images-lucien.json (slug -> liste des fichiers + dimensions).
"""
import io
import json
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "assets" / "produits"
OUT.mkdir(parents=True, exist_ok=True)
MAX_SIDE = 900
PER_PRODUCT = 2

products = json.loads((ROOT / "data" / "produits-lucien.json").read_text(encoding="utf-8"))
raw = []
for i in (1, 2, 3):
    p = Path(__file__).resolve().parent / "raw" / f"p{i}.json"
    if p.exists():
        raw += json.loads(p.read_text(encoding="utf-8"))
srcsets = {r["slug"]: [img.get("srcset", "") for img in r["images"]] for r in raw}


def pick(src, srcset):
    """Plus petite variante >= 600 px de large, sinon l'original."""
    best = None
    for part in srcset.split(","):
        m = re.match(r"\s*(\S+)\s+(\d+)w", part)
        if not m:
            continue
        url, w = m.group(1), int(m.group(2))
        if w >= 600 and (best is None or w < best[1]):
            best = (url, w)
    return best[0] if best else src


def job(args):
    slug, n, url = args
    dest = OUT / f"{slug}-{n}.webp"
    if dest.exists():
        im = Image.open(dest)
        return slug, n, dest.name, im.size
    try:
        req = urllib.request.Request(urllib.parse.quote(url, safe=":/?=&%"), headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=40).read()
        im = Image.open(io.BytesIO(data))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        im.save(dest, "WEBP", quality=80, method=5)
        return slug, n, dest.name, im.size
    except Exception as e:  # noqa: BLE001
        print("ECHEC", slug, url, e)
        return slug, n, None, None


jobs = []
for p in products:
    sets = srcsets.get(p["slug"], [])
    for n, src in enumerate(p["images"][:PER_PRODUCT]):
        url = pick(src, sets[n] if n < len(sets) else "")
        jobs.append((p["slug"], n + 1, url))

result = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    for slug, n, name, size in ex.map(job, jobs):
        if name:
            result.setdefault(slug, []).append({"n": n, "file": name, "w": size[0], "h": size[1]})

for v in result.values():
    v.sort(key=lambda x: x["n"])
(ROOT / "data" / "images-lucien.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(jobs), "images demandées,", sum(len(v) for v in result.values()), "OK")
