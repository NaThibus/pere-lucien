"""Générateur du site statique Le Père Lucien & Mère Martine.

Usage : python build/build.py
Lit data/ et build/*.py, écrit le site complet dans site/ (les assets sont conservés).
"""
import hashlib
import html
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import articles  # noqa: E402
import labels  # noqa: E402
import content_lucien as CL  # noqa: E402
import content_martine as CM  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOMAIN = "https://www.leperelucien.com"
TODAY = date(2026, 10, 12).isoformat()
ICONS_DIR = Path(__file__).resolve().parent / "icons"
SOCIAL = {
    "instagram": "https://www.instagram.com/leperelucien/",
    "facebook": "https://www.facebook.com/leperelucien/",
    "youtube": "https://www.youtube.com/@filslade",
    "pinterest": "https://www.pinterest.fr/leperelucien/",
}

# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=True)


_icon_cache = {}


def icon(name, cls="i"):
    if name not in _icon_cache:
        svg = (ICONS_DIR / f"{name}.svg").read_text(encoding="utf-8")
        svg = svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
        _icon_cache[name] = svg
    return _icon_cache[name].replace("<svg ", f'<svg class="{cls}" ', 1)


def euro(v):
    s = f"{v:,.2f}".replace(",", " ").replace(".", ",")
    return f"{s} €"


def stable(s):
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)


def clip(text, n):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0].rstrip(",;:.") + "…"


def no_dash(s):
    """Pas de tirets cadratins ni demi-cadratins dans le texte visible."""
    return s.replace(" — ", ", ").replace("—", ", ").replace(" – ", " - ").replace("–", "-")


# ---------------------------------------------------------------------------
# Données Le Père Lucien
# ---------------------------------------------------------------------------
raw = []
for i in (1, 2, 3):
    raw += json.loads((Path(__file__).resolve().parent / "raw" / f"p{i}.json").read_text(encoding="utf-8"))
raw_by_slug = {r["slug"]: r for r in raw}
lucien_json = json.loads((ROOT / "data" / "produits-lucien.json").read_text(encoding="utf-8"))
lucien_imgs = json.loads((ROOT / "data" / "images-lucien.json").read_text(encoding="utf-8"))

WC_TO_CAT = {v["wc"]: k for k, v in CL.CATEGORIES.items()}
WC_TO_CAT[369] = "coin-des-affaires"

SCENTS = ["barbershop", "santal", "cuir", "vetiver", "vétiver", "oud", "abricot", "cèdre", "cedre", "fougère", "fougere",
          "traditionnel", "nature", "narcisse", "pushkar", "lavande", "grand cru", "élégance", "rosée", "ebene", "ébène",
          "bay rum", "orange"]

COMPLEMENTS = {
    "rasage/savons-a-raser": ["rasage/blaireaux", "rasage/bols", "rasage/avant-apres-rasage"],
    "rasage/blaireaux": ["rasage/savons-a-raser", "rasage/bols", "rasage/accessoires"],
    "rasage/rasoirs-de-surete": ["rasage/lames", "rasage/savons-a-raser", "rasage/blaireaux"],
    "rasage/lames": ["rasage/rasoirs-de-surete", "rasage/shavettes-coupe-choux", "rasage/savons-a-raser"],
    "rasage/shavettes-coupe-choux": ["rasage/lames", "rasage/accessoires", "rasage/savons-a-raser"],
    "rasage/avant-apres-rasage": ["rasage/savons-a-raser", "parfums", "rasage/blaireaux"],
    "rasage/bols": ["rasage/savons-a-raser", "rasage/blaireaux", "rasage/accessoires"],
    "rasage/accessoires": ["rasage/blaireaux", "rasage/rasoirs-de-surete", "rasage/savons-a-raser"],
    "barbe-moustache/huiles-baumes": ["barbe-moustache/shampoings", "barbe-moustache/peignes-brosses", "barbe-moustache/cires-moustache"],
    "barbe-moustache/shampoings": ["barbe-moustache/huiles-baumes", "barbe-moustache/peignes-brosses", "corps-cheveux"],
    "barbe-moustache/cires-moustache": ["barbe-moustache/peignes-brosses", "barbe-moustache/huiles-baumes", "rasage/savons-a-raser"],
    "barbe-moustache/peignes-brosses": ["barbe-moustache/huiles-baumes", "barbe-moustache/shampoings", "barbe-moustache/cires-moustache"],
    "corps-cheveux": ["barbe-moustache/shampoings", "rasage/savons-a-raser", "parfums"],
    "parfums": ["rasage/avant-apres-rasage", "rasage/savons-a-raser", "corps-cheveux"],
    "accessoires-toilette": ["rasage/accessoires", "barbe-moustache/peignes-brosses", "corps-cheveux"],
    "coin-des-affaires": ["rasage/savons-a-raser", "rasage/blaireaux", "rasage/avant-apres-rasage"],
}


def lucien_cat_url(key):
    return f"/{key}/"


def martine_cat_url(key):
    return f"{CM.BASE}/{key}/"


def parse_lucien_description(name, text):
    """Range la description brute en sections : texte, mot de Cyril, conseils, composition, caractéristiques."""
    out = {"texte": [], "cyril": None, "conseils": [], "composition": None, "specs": []}
    mode = "texte"
    name_l = re.sub(r"\W+", "", name.lower())
    for i, line in enumerate(text.split("\n")):
        l = line.strip()
        if not l:
            continue
        low = l.lower()
        if i == 0 and (re.sub(r"\W+", "", low)[:25] == name_l[:25] or (len(l) < 70 and "." not in l[:-1])):
            continue
        if low.startswith(("ingrédients", "ingredients", "inci", "composition")):
            out["composition"] = re.sub(r"^[^:]*:\s*", "", l)
            mode = "texte"
            continue
        if low.startswith("code ean") or low.startswith("ean"):
            out["specs"].append(l)
            continue
        if low.startswith("le mot de cyril"):
            out["cyril"] = re.sub(r"^[^:]*:\s*", "", l)
            continue
        if low.startswith(("notre astuce", "astuce", "conseil d", "conseils d", "instruction")):
            rest = re.sub(r"^[^:]*:?\s*", "", l) if ":" in l else ""
            if rest:
                out["conseils"].append(rest)
            mode = "conseils"
            continue
        if low.startswith("découvrez") or low.startswith("decouvrez"):
            continue
        if len(l) < 60 and l.endswith(":"):
            mode = "specs"
            continue
        if l.startswith("- ") or l.startswith("• "):
            (out["conseils"] if mode == "conseils" else out["specs"]).append(l[2:].strip())
            continue
        if "recommandons" in low or "nous vous conseillons" in low or low.startswith(("afin d", "pour obtenir")):
            out["conseils"].append(l)
            continue
        if mode == "specs" and len(l) < 90:
            out["specs"].append(l)
            continue
        if mode == "conseils" and len(out["conseils"]) < 6:
            out["conseils"].append(l)
            continue
        mode = "texte"
        out["texte"].append(l)
    return out


PRODUCTS = []          # tous les produits (lucien + martine)
BY_REF = {}            # "p:slug" / "m:slug" -> produit

for p in lucien_json:
    r = raw_by_slug[p["slug"]]
    pr = r["prices"]
    unit = 10 ** int(pr.get("currency_minor_unit") or 2)
    if pr.get("price_range"):
        prix = int(pr["price_range"]["min_amount"]) / unit
        a_partir = int(pr["price_range"]["max_amount"]) != int(pr["price_range"]["min_amount"])
    else:
        prix = int(pr["price"]) / unit
        a_partir = False
    barre = None
    if r["on_sale"] and int(pr["regular_price"] or 0) > int(pr["price"] or 0):
        barre = int(pr["regular_price"]) / unit
    cats = [WC_TO_CAT[c["id"]] for c in r["categories"] if c["id"] in WC_TO_CAT]
    cats = list(dict.fromkeys(cats))
    if not cats:
        cats = ["coin-des-affaires"]
    deep = [c for c in cats if "/" in c]
    if "coffret" in p["nom"].lower() and "coin-des-affaires" in cats:
        main = "coin-des-affaires"
    elif deep:
        main = deep[0]
    else:
        main = cats[0]
    imgs = [f"/assets/produits/{x['file']}" for x in lucien_imgs.get(p["slug"], [])]
    if not imgs:
        lab = SITE / "assets" / "produits" / f"etiquette-{p['slug']}.webp"
        if not (lab.exists() and lab.stat().st_mtime >= (Path(__file__).resolve().parent / "labels.py").stat().st_mtime):
            nm = no_dash(html.unescape(p["nom"]))
            parts = [x.strip() for x in re.split(r",| - ", nm) if x.strip()]
            labels.make_label(lab, "lucien", parts[0], " ".join(parts[1:])[:60], "Teillet-Argenty, Allier", "blue", stable(p["slug"]) % 7)
        imgs = [f"/assets/produits/etiquette-{p['slug']}.webp"]
    sec = parse_lucien_description(p["nom"], p["description"] or p["description_courte"])
    if not sec["texte"] and p["description_courte"]:
        sec["texte"] = [l for l in p["description_courte"].split("\n") if l.strip()][:3]
    variantes = None
    if r.get("attributes"):
        a = r["attributes"][0]
        opts = [html.unescape(t["name"]) for t in a.get("terms", [])]
        if opts:
            variantes = (html.unescape(a["name"]), opts)
    nom = no_dash(html.unescape(p["nom"]))
    accroche = clip(" ".join(sec["texte"][:2]) if sec["texte"] else nom, 150)
    prod = {
        "brand": "lucien", "ref": f"p:{p['slug']}", "slug": p["slug"], "nom": nom,
        "url": f"/produit/{p['slug']}/", "prix": prix, "a_partir": a_partir, "prix_barre": barre,
        "images": imgs, "cat": main, "cats": cats, "sections": sec, "accroche": no_dash(accroche),
        "variantes": variantes, "stock": r["is_in_stock"], "rating": float(r.get("average_rating") or 0),
        "reviews": int(r.get("review_count") or 0), "sku": r.get("sku") or p["slug"], "lies": [],
        "guide": CL.CATEGORIES[main].get("guide"),
    }
    PRODUCTS.append(prod)
    BY_REF[prod["ref"]] = prod

# ---------------------------------------------------------------------------
# Données Mère Martine (+ visuels dérivés)
# ---------------------------------------------------------------------------
IMG = SITE / "assets" / "img"
MIMG = IMG / "martine"


LABELS_SRC = Path(__file__).resolve().parent / "labels.py"
PHOTOS = MIMG / "photos"          # déposez ici <slug>.webp pour remplacer une étiquette
PHOTOS.mkdir(parents=True, exist_ok=True)
PALETTE_CAT = {"corps": "rose", "cheveux": "sage", "coin-des-affaires": "kraft"}


def fresh(path):
    """Vrai si le fichier existe et est plus récent que le générateur d'étiquettes."""
    return path.exists() and path.stat().st_mtime >= LABELS_SRC.stat().st_mtime


def sm_and_detail(base, detail=True):
    src = MIMG / f"{base}.webp"
    sm = MIMG / f"{base}-sm.webp"
    det = MIMG / f"{base}-detail.webp"
    if not sm.exists() or sm.stat().st_mtime < src.stat().st_mtime:
        im = Image.open(src).convert("RGB")
        im.thumbnail((560, 560), Image.LANCZOS)
        im.save(sm, "WEBP", quality=78)
    if detail and (not det.exists() or det.stat().st_mtime < src.stat().st_mtime):
        im = Image.open(src).convert("RGB")
        w, h = im.size
        box = (int(w * .18), int(h * .14), int(w * .82), int(h * .78))
        im.crop(box).resize((900, 900), Image.LANCZOS).save(det, "WEBP", quality=80)
    imgs = [f"/assets/img/martine/{base}.webp"]
    if detail:
        imgs.append(f"/assets/img/martine/{base}-detail.webp")
    return imgs, f"/assets/img/martine/{base}-sm.webp"


def derive_martine_images(p, seed):
    """Photo fournie > photo d'origine > mosaïque (coffrets) > étiquette d'atelier générée."""
    photo = PHOTOS / f"{p['slug']}.webp"
    if photo.exists():
        shutil.copyfile(photo, MIMG / f"photo-{p['slug']}.webp")
        return sm_and_detail(f"photo-{p['slug']}")
    if p["image"] == "mosaique":
        dest = MIMG / f"{p['slug']}.webp"
        W = 1024
        canvas = Image.new("RGB", (W, W), (242, 207, 196))
        gap = 18
        cell = (W - gap * 3) // 2
        for k, s in enumerate(p["contenu"][:4]):
            im = Image.open(SITE / MARTINE_MAIN[s].lstrip("/")).convert("RGB")
            im = im.resize((cell, cell), Image.LANCZOS)
            canvas.paste(im, (gap + (k % 2) * (cell + gap), gap + (k // 2) * (cell + gap)))
        canvas.save(dest, "WEBP", quality=82)
        return sm_and_detail(p["slug"], detail=False)
    if p["image"]:
        return sm_and_detail(p["image"])
    base = f"etiquette-{p['slug']}"
    dest = MIMG / f"{base}.webp"
    if not fresh(dest):
        palette = p.get("palette") or PALETTE_CAT.get(p["categorie"].split("/")[0], "rose")
        head, _, tail = p["nom"].partition(",")
        labels.make_label(dest, "martine", head.strip(), tail.strip() or p.get("etiquette", ""), p["contenance"], palette, seed)
    return [f"/assets/img/martine/{base}.webp"], f"/assets/img/martine/{base}-sm.webp"


MARTINE_MAIN = {}
_ordered = sorted(CM.PRODUITS, key=lambda x: x["image"] == "mosaique")
_derived = {}
for i, p in enumerate(_ordered):
    _derived[p["slug"]] = derive_martine_images(p, i)
    MARTINE_MAIN[p["slug"]] = _derived[p["slug"]][0][0]
    if p.get("contenu") and p.get("prix") is None:
        total = sum(next(x for x in CM.PRODUITS if x["slug"] == s)["prix"] for s in p["contenu"])
        p["prix_barre"] = round(total, 2)
        p["prix"] = float(round(total * 0.85))


for p in CM.PRODUITS:
    imgs, card = _derived[p["slug"]]
    prod = {
        "brand": "martine", "ref": f"m:{p['slug']}", "slug": p["slug"], "nom": p["nom"],
        "url": f"{CM.BASE}/produit/{p['slug']}/", "prix": p["prix"], "a_partir": False,
        "prix_barre": p.get("prix_barre"), "images": imgs, "card_img": card, "cat": p["categorie"],
        "cats": [p["categorie"]] + p["aussi"], "accroche": p["accroche"], "variantes": p.get("variantes"),
        "stock": True, "rating": 0, "reviews": 0, "sku": "MM-" + p["slug"][:24].upper(),
        "lies": [("p:" + r[7:]) if r.startswith("lucien:") else ("m:" + r) for r in p["lies"]], "guide": p["guide"], "data": p,
    }
    PRODUCTS.append(prod)
    BY_REF[prod["ref"]] = prod

LUCIEN = [p for p in PRODUCTS if p["brand"] == "lucien"]
MARTINE = [p for p in PRODUCTS if p["brand"] == "martine"]


def products_in(brand, key):
    """Produits d'une catégorie, sous-catégories comprises."""
    out = []
    for p in (LUCIEN if brand == "lucien" else MARTINE):
        if any(c == key or c.startswith(key + "/") for c in p["cats"]):
            out.append(p)
    return out


def scent_of(name):
    n = name.lower()
    return next((s for s in SCENTS if s in n), None)


# Produits liés Lucien : même senteur d'abord, puis gammes complémentaires.
for p in LUCIEN:
    picks = []
    scent = scent_of(p["nom"])
    for ck in COMPLEMENTS.get(p["cat"], []):
        pool = [q for q in products_in("lucien", ck) if q is not p and q["images"] and q["ref"] not in picks]
        if not pool:
            continue
        same = [q for q in pool if scent and scent_of(q["nom"]) == scent]
        pool = same or sorted(pool, key=lambda q: stable(p["slug"] + q["slug"]))
        picks.append(pool[0]["ref"])
    sibs = [q for q in products_in("lucien", p["cat"]) if q is not p and q["images"]]
    if sibs:
        picks.append(sorted(sibs, key=lambda q: stable(q["slug"] + p["slug"]))[0]["ref"])
    if p["cat"] in ("corps-cheveux",):
        picks.append("m:savon-lait-de-chevre-bio")
    p["lies"] = picks[:4]

# Balises title et description uniques pour chaque fiche
def middle_cut(text, n):
    if len(text) <= n:
        return text
    half = (n - 2) // 2
    head = text[:half].rsplit(" ", 1)[0].rstrip(",;:-")
    tail = text[-half:].split(" ", 1)[-1]
    return f"{head}… {tail}"


for p in PRODUCTS:
    suffix = " | Mère Martine" if p["brand"] == "martine" else " | Le Père Lucien"
    t = p["nom"] + suffix
    if len(t) > 65:
        t = clip(p["nom"], 64)
    p["seo_title"] = t
    src = p["accroche"] if p["brand"] == "martine" else " ".join(p["sections"]["texte"][:2]) or p["accroche"]
    lead = p["nom"].rstrip(".")
    p["seo_desc"] = no_dash(clip(src if src.lower().startswith(lead.lower()[:20]) else f"{lead}. {src}", 155))
for field in ("seo_title", "seo_desc"):
    groups = defaultdict(list)
    for p in PRODUCTS:
        groups[p[field]].append(p)
    for dup in (g for g in groups.values() if len(g) > 1):
        for p in dup:
            tail = p["slug"].rsplit("-", 1)[-1].upper() if len(p["slug"].rsplit("-", 1)[-1]) <= 3 else p["slug"].rsplit("-", 1)[-1].capitalize()
            if field == "seo_title":
                p[field] = f"{clip(p['nom'], 52)} {tail}"
            else:
                p[field] = clip(f"{p['nom']} ({tail}). {p[field][len(p['nom']) + 2:]}", 155)

# Vérification des références
for p in PRODUCTS:
    for ref in p["lies"]:
        if ref not in BY_REF:
            raise SystemExit(f"Référence produit inconnue {ref} dans {p['slug']}")

ART_L = {a["slug"]: a for a in articles.LUCIEN}
ART_M = {a["slug"]: a for a in articles.MARTINE}


def article_url(brand, slug):
    return f"/conseils/{slug}/" if brand == "lucien" else f"{CM.BASE}/conseils/{slug}/"


def resolve_links(body):
    def rep(m):
        kind, target, text = m.group(1), m.group(2), m.group(3)
        if kind in ("p", "m"):
            ref = f"{kind}:{target}"
            if ref not in BY_REF:
                raise SystemExit(f"Lien produit inconnu {ref}")
            url = BY_REF[ref]["url"]
        elif kind == "c":
            if target not in CL.CATEGORIES:
                raise SystemExit(f"Catégorie inconnue {target}")
            url = lucien_cat_url(target)
        elif kind == "mc":
            if target not in CM.CATEGORIES:
                raise SystemExit(f"Catégorie Martine inconnue {target}")
            url = martine_cat_url(target)
        elif kind == "a":
            if target not in ART_L:
                raise SystemExit(f"Article inconnu {target}")
            url = article_url("lucien", target)
        elif kind == "ma":
            if target not in ART_M:
                raise SystemExit(f"Article Martine inconnu {target}")
            url = article_url("martine", target)
        else:
            url = target
        return f'<a href="{url}">{text}</a>'
    return re.sub(r"\[\[(p|m|c|mc|a|ma|u):([^|\]]+)\|([^\]]+)\]\]", rep, body)


# ---------------------------------------------------------------------------
# Gabarit
# ---------------------------------------------------------------------------
PAGES = []   # (chemin, priorité, changefreq) pour le sitemap


def nav_lucien():
    rasage = [(k, v) for k, v in CL.CATEGORIES.items() if v["parent"] == "rasage"]
    barbe = [(k, v) for k, v in CL.CATEGORIES.items() if v["parent"] == "barbe-moustache"]
    tops = [(k, v) for k, v in CL.CATEGORIES.items() if v["parent"] is None]

    def sub(items):
        return "".join(f'<li><a href="{lucien_cat_url(k)}">{esc(v["nom"])}</a></li>' for k, v in items)

    return f"""
<li class="nav-item has-mega">
  <a class="nav-link" href="/boutique/">Boutique {icon('caret-down','i i-xs')}</a>
  <div class="mega"><div class="mega-in">
    <div><p class="mega-h">Toutes les gammes</p><ul>{sub(tops)}</ul></div>
    <div><p class="mega-h">Rasage</p><ul>{sub(rasage)}</ul></div>
    <div><p class="mega-h">Barbe et moustache</p><ul>{sub(barbe)}</ul></div>
    <a class="mega-feat" href="/rasage/savons-a-raser/">
      <img src="/assets/img/lucien-savon-barbier-nature.webp" alt="Savon du barbier Nature posé sur la mousse" loading="lazy" width="320" height="335">
      <span>Le savon du barbier, en pot ou en recharge {icon('arrow-right','i i-xs')}</span>
    </a>
  </div></div>
</li>
<li class="nav-item"><a class="nav-link" href="/rasage/">Rasage</a></li>
<li class="nav-item"><a class="nav-link" href="/barbe-moustache/">Barbe</a></li>
<li class="nav-item"><a class="nav-link" href="/conseils/">Conseils</a></li>
<li class="nav-item"><a class="nav-link" href="/la-maison/">La maison</a></li>"""


def nav_martine():
    corps = [(k, v) for k, v in CM.CATEGORIES.items() if v["parent"] == "corps"]
    cheveux = [(k, v) for k, v in CM.CATEGORIES.items() if v["parent"] == "cheveux"]

    def sub(items):
        return "".join(f'<li><a href="{martine_cat_url(k)}">{esc(v["nom"])}</a></li>' for k, v in items)

    return f"""
<li class="nav-item has-mega">
  <a class="nav-link" href="{CM.BASE}/corps/">Corps {icon('caret-down','i i-xs')}</a>
  <div class="mega mega-sm"><div class="mega-in"><div><p class="mega-h">Produits pour le corps</p><ul>{sub(corps)}</ul></div>
  <a class="mega-feat" href="{CM.BASE}/corps/huiles/"><img src="/assets/img/martine/huile-corps-sm.webp" alt="Huile sèche satinante en flacon ambré" loading="lazy" width="280" height="280"><span>L'huile sèche corps et cheveux {icon('arrow-right','i i-xs')}</span></a></div></div>
</li>
<li class="nav-item has-mega">
  <a class="nav-link" href="{CM.BASE}/cheveux/">Cheveux {icon('caret-down','i i-xs')}</a>
  <div class="mega mega-sm"><div class="mega-in"><div><p class="mega-h">Produits pour les cheveux</p><ul>{sub(cheveux)}</ul></div>
  <a class="mega-feat" href="{CM.BASE}/cheveux/brosses/"><img src="/assets/img/martine/brosse-sm.webp" alt="Brosse à cheveux en poils de sanglier" loading="lazy" width="280" height="280"><span>La brosse en poils de sanglier {icon('arrow-right','i i-xs')}</span></a></div></div>
</li>
<li class="nav-item"><a class="nav-link" href="{CM.BASE}/coin-des-affaires/">Coffrets</a></li>
<li class="nav-item"><a class="nav-link" href="{CM.BASE}/conseils/">Le carnet</a></li>
<li class="nav-item"><a class="nav-link" href="{CM.BASE}/histoire/">Histoire</a></li>"""


def mobile_nav(brand):
    if brand == "martine":
        groups = [("Corps", martine_cat_url("corps"), [(martine_cat_url(k), v["nom"]) for k, v in CM.CATEGORIES.items() if v["parent"] == "corps"]),
                  ("Cheveux", martine_cat_url("cheveux"), [(martine_cat_url(k), v["nom"]) for k, v in CM.CATEGORIES.items() if v["parent"] == "cheveux"])]
        links = [(martine_cat_url("coin-des-affaires"), "Coffrets et cadeaux"), (f"{CM.BASE}/conseils/", "Le carnet de Mère Martine"),
                 (f"{CM.BASE}/histoire/", "Notre histoire"), (f"{CM.BASE}/faq/", "Questions fréquentes")]
        other = ("/", "Le Père Lucien", "Rasage et barbe")
    else:
        groups = [("Rasage", "/rasage/", [(lucien_cat_url(k), v["nom"]) for k, v in CL.CATEGORIES.items() if v["parent"] == "rasage"]),
                  ("Barbe et moustache", "/barbe-moustache/", [(lucien_cat_url(k), v["nom"]) for k, v in CL.CATEGORIES.items() if v["parent"] == "barbe-moustache"])]
        links = [("/corps-cheveux/", "Corps et cheveux"), ("/parfums/", "Nos parfums"), ("/accessoires-toilette/", "Accessoires de toilette"),
                 ("/coin-des-affaires/", "Coin des affaires"), ("/conseils/", "Conseils"), ("/la-maison/", "La maison"), ("/revendeurs/", "Revendeurs")]
        other = (f"{CM.BASE}/", "Mère Martine", "La gamme féminine")
    g = "".join(
        f'<details class="m-group"><summary>{esc(t)}{icon("plus","i i-sm")}</summary><ul><li><a href="{u}">Tout voir</a></li>'
        + "".join(f'<li><a href="{su}">{esc(sn)}</a></li>' for su, sn in subs) + "</ul></details>"
        for t, u, subs in groups)
    l = "".join(f'<a class="m-link" href="{u}">{esc(t)}</a>' for u, t in links)
    return f"""<div class="m-nav" id="m-nav" hidden>
  <div class="m-nav-in">
    {g}{l}
    <a class="m-other" href="{other[0]}"><span><strong>{other[1]}</strong><small>{other[2]}</small></span>{icon('arrow-right')}</a>
  </div>
</div>"""


def logo(brand):
    if brand == "martine":
        return (f'<a class="logo logo-mm" href="{CM.BASE}/" aria-label="La Mère Martine, accueil">'
                f'<img class="logo-badge" src="/assets/img/logo-mere-martine.svg" alt="" width="54" height="54">'
                f'<span class="logo-text"><span class="logo-word">La Mère Martine</span><span class="logo-sub">cosmétique naturelle, par Le Père Lucien</span></span></a>')
    return '<a class="logo" href="/" aria-label="Le Père Lucien, accueil"><img class="logo-face" src="/assets/img/lucien-lelegard-portrait.webp" alt="" width="34" height="34"><span class="logo-word">Le Père Lucien</span></a>'


def header(brand):
    nav = nav_martine() if brand == "martine" else nav_lucien()
    switch = (f'<a class="switch switch-pl" href="/">Le Père Lucien {icon("arrow-up-right","i i-xs")}</a>' if brand == "martine"
              else f'<a class="switch switch-mm" href="{CM.BASE}/">Mère Martine {icon("arrow-up-right","i i-xs")}</a>')
    bar = ("Livraison offerte dès 80 € en France. Coffrets cadeaux avec carte manuscrite." if brand == "martine"
           else "Livraison offerte dès 80 € en France. Expédié sous 48 h depuis l'Allier.")
    return f"""<a class="skip" href="#contenu">Aller au contenu</a>
<p class="topbar">{bar}</p>
<header class="site-header" id="top">
  <div class="hd wrap">
    <button class="icon-btn burger" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="m-nav">{icon('list')}</button>
    {logo(brand)}
    <nav class="main-nav" aria-label="Navigation principale"><ul>{nav}</ul></nav>
    <div class="hd-actions">
      {switch}
      <button class="icon-btn" type="button" data-open-search aria-label="Rechercher">{icon('magnifying-glass')}</button>
      <button class="icon-btn cart-btn" type="button" data-open-cart aria-label="Ouvrir le panier">{icon('handbag-simple')}<span class="cart-count" data-cart-count hidden>0</span></button>
    </div>
  </div>
  {mobile_nav(brand)}
</header>"""


def footer(brand):
    def col(title, items):
        return f'<div class="ft-col"><p class="ft-h">{title}</p><ul>' + "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in items) + "</ul></div>"

    lucien_items = [(lucien_cat_url(k), v["nom"]) for k, v in CL.CATEGORIES.items() if v["parent"] is None]
    martine_items = [(martine_cat_url(k), v["nom"]) for k, v in CM.CATEGORIES.items() if v["parent"] is None] + [
        (f"{CM.BASE}/conseils/", "Le carnet"), (f"{CM.BASE}/histoire/", "Histoire de Mère Martine")]
    maison = [("/la-maison/histoire/", "Notre histoire"), ("/la-maison/atelier/", "L'atelier"), ("/la-maison/engagements/", "Nos engagements"),
              ("/la-maison/presse/", "Presse"), ("/revendeurs/", "Revendeurs"), ("/partenaires/", "Partenaires")]
    aide = [("/conseils/", "Conseils de rasage"), ("/faq/", "Questions fréquentes"), ("/contact/", "Contact"), ("/cgv/", "Conditions de vente"),
            ("/plan-du-site/", "Plan du site")]
    word = "Mère Martine" if brand == "martine" else "Le Père Lucien"
    soc = "".join(f'<a class="soc" href="{u}" rel="noopener" target="_blank" aria-label="{n.capitalize()}">{icon(n + "-logo")}</a>' for n, u in SOCIAL.items())
    tag = "#meremartine" if brand == "martine" else "#leperelucien"
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="ft-top">
      <form class="news" data-fake-form novalidate>
        <label for="news-email" class="news-h">La lettre de l'atelier, une fois par mois.</label>
        <p class="news-p">Nouveaux parfums, recharges et éditions limitées. Pas de publicité tierce.</p>
        <div class="news-row">
          <input id="news-email" name="email" type="email" required autocomplete="email" placeholder="vous@exemple.fr">
          <button class="btn btn-accent" type="submit">S'inscrire</button>
        </div>
        <p class="form-msg" role="status" aria-live="polite"></p>
      </form>
      <div class="ft-social">
        <p class="ft-h">Partagez votre rasage avec {tag}</p>
        <div class="socs">{soc}</div>
      </div>
    </div>
    <div class="ft-grid">
      {col("Le Père Lucien", lucien_items)}
      {col("Mère Martine", martine_items)}
      {col("La maison", maison)}
      {col("Aide", aide)}
    </div>
    {f'<div class="ft-brand"><img src="/assets/img/logo-mere-martine.svg" alt="La Mère Martine, cosmétique naturelle" width="150" height="150" loading="lazy"><p class="ft-word" aria-hidden="true">La Mère Martine</p></div>' if brand == "martine" else f'<p class="ft-word" aria-hidden="true">{word}</p>'}
    <div class="ft-legal">
      <p>Laboratoires Lelégard SAS, ZA de la Souvol, allée des Entreprises, 03380 La Chapelaude. Fabriqué à Teillet-Argenty, Allier.</p>
      <p><a href="/mentions-legales/">Mentions légales</a><a href="/confidentialite/">Confidentialité</a><a href="/cgv/">CGV</a></p>
    </div>
  </div>
</footer>"""


OVERLAYS = f"""
<div class="drawer" id="cart" role="dialog" aria-modal="true" aria-labelledby="cart-title" hidden>
  <div class="drawer-scrim" data-close></div>
  <aside class="drawer-panel">
    <div class="drawer-hd"><p class="drawer-title" id="cart-title">Votre panier</p><button class="icon-btn" type="button" data-close aria-label="Fermer le panier">{icon('x')}</button></div>
    <div class="drawer-ship" data-ship></div>
    <ul class="cart-list" data-cart-list></ul>
    <div class="cart-empty" data-cart-empty>
      <p>Votre panier est vide.</p>
      <a class="btn btn-ghost" href="/rasage/savons-a-raser/">Voir les savons à raser</a>
      <a class="btn btn-ghost" href="{CM.BASE}/">Découvrir Mère Martine</a>
    </div>
    <div class="drawer-ft" data-cart-ft>
      <p class="cart-total"><span>Sous-total</span><strong data-cart-total>0,00 €</strong></p>
      <a class="btn btn-accent btn-block" href="/panier/">Commander</a>
    </div>
  </aside>
</div>
<div class="search" id="search" role="dialog" aria-modal="true" aria-label="Recherche" hidden>
  <div class="search-in wrap">
    <div class="search-row">
      {icon('magnifying-glass')}
      <label class="sr" for="q">Rechercher un produit</label>
      <input id="q" type="search" placeholder="Savon, blaireau, huile, brosse…" autocomplete="off">
      <button class="icon-btn" type="button" data-close aria-label="Fermer la recherche">{icon('x')}</button>
    </div>
    <ul class="search-res" data-search-res></ul>
    <p class="search-hint" data-search-hint>Essayez « santal », « recharge », « lait d'ânesse » ou « coupe-choux ».</p>
  </div>
</div>
<div class="toast" role="status" aria-live="polite" data-toast></div>"""


def head(page):
    canonical = DOMAIN + page["path"]
    og_img = page.get("og") or "/assets/img/og-default.jpg"
    og_img = og_img if og_img.startswith("http") else DOMAIN + og_img
    robots = '<meta name="robots" content="noindex, follow">' if page.get("noindex") else '<meta name="robots" content="index, follow, max-image-preview:large">'
    ld = page.get("ld") or []
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    theme = "#A13D5F" if page["brand"] == "martine" else "#1F3FD1"
    site_name = "Mère Martine" if page["brand"] == "martine" else "Le Père Lucien"
    return f"""<!doctype html>
<html lang="fr" data-brand="{page['brand']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['desc'])}">
{robots}
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="fr" href="{canonical}">
<meta property="og:locale" content="fr_FR">
<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{esc(page.get('og_title', page['title']))}">
<meta property="og:description" content="{esc(page['desc'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page.get('og_title', page['title']))}">
<meta name="twitter:description" content="{esc(page['desc'])}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="{theme}">
<link rel="icon" href="/assets/img/favicon-{page['brand']}.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/geist.woff2" as="font" type="font/woff2" crossorigin>
{'<link rel="preload" href="/assets/fonts/cormorant.woff2" as="font" type="font/woff2" crossorigin>' if page["brand"] == "martine" else ''}
{page.get('preload', '')}
<link rel="stylesheet" href="/assets/css/style.css">
<script src="/assets/js/app.js" defer></script>
{ld_html}
</head>"""


def breadcrumb(items):
    """items: [(nom, url)], le dernier est la page courante."""
    lis = []
    for i, (n, u) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{esc(n)}</li>')
        else:
            lis.append(f'<li><a href="{u}">{esc(n)}</a></li>')
    html_ = f'<nav class="crumbs wrap" aria-label="Fil d\'Ariane"><ol>{"".join(lis)}</ol></nav>'
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + u} for i, (n, u) in enumerate(items)]}
    return html_, ld


def write(page, body):
    PAGES.append((page["path"], page.get("priority", 0.5), page.get("freq", "monthly"), page.get("noindex", False)))
    brand = page["brand"]
    doc = f"""{head(page)}
<body>
{header(brand)}
<main id="contenu">
{body}
</main>
{footer(brand)}
{OVERLAYS}
</body>
</html>
"""
    if "—" in doc:
        raise SystemExit(f"Tiret cadratin trouvé dans {page['path']}")
    out = SITE / page["path"].strip("/") / "index.html" if page["path"] != "/" else SITE / "index.html"
    if page["path"].endswith(".html"):
        out = SITE / page["path"].strip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    # Chemins relatifs : le site fonctionne sur un serveur ET en ouvrant les fichiers directement.
    depth = len(out.relative_to(SITE).parts) - 1
    prefix = "../" * depth

    def rel(m):
        path = m.group(2)
        return f'{m.group(1)}="{(prefix + path) or "./"}"'
    doc = re.sub(r'(href|src|data-thumb)="/(?!/)([^"]*)"', rel, doc)
    out.write_text(doc, encoding="utf-8")


# ---------------------------------------------------------------------------
# Composants
# ---------------------------------------------------------------------------
def price_html(p, cls="price"):
    pre = "dès " if p["a_partir"] else ""
    old = f' <s>{euro(p["prix_barre"])}</s>' if p.get("prix_barre") else ""
    return f'<span class="{cls}">{pre}{euro(p["prix"])}{old}</span>'


MAISON_CATS = ("rasage/savons-a-raser", "rasage/avant-apres-rasage", "barbe-moustache/huiles-baumes", "barbe-moustache/shampoings",
               "barbe-moustache/cires-moustache", "corps-cheveux", "parfums")


def is_maison(p):
    """Produit fabriqué dans l'atelier (et non sélectionné chez un autre artisan)."""
    if p["brand"] == "martine":
        return not p["slug"].startswith(("bol-de-rasage", "rasoir-", "brosse-"))
    n = p["nom"].lower().replace("è", "e")
    return "le pere lucien" in n or (p["cat"] in MAISON_CATS and "parker" not in n and "darwin" not in n)


def seal(brand, cls="seal"):
    """Tampon circulaire « fait main » (texte sur un cercle), qui tourne lentement."""
    txt = "FAIT MAIN · TEILLET-ARGENTY · ALLIER · DEPUIS 2013 · "
    if brand == "lucien":
        center = ('<image href="/assets/img/lucien-lelegard-portrait.webp" x="33" y="28" width="54" height="64" '
                  'preserveAspectRatio="xMidYMid slice" clip-path="url(#seal-clip)"/>')
    else:
        center = '<text x="60" y="70" text-anchor="middle" class="seal-mono">MM</text>'
    return f"""<svg class="{cls}" viewBox="0 0 120 120" role="img" aria-label="Fait main à Teillet-Argenty, Allier, depuis 2013">
  <defs><path id="seal-path" d="M60,60 m-44,0 a44,44 0 1,1 88,0 a44,44 0 1,1 -88,0"/><clipPath id="seal-clip"><circle cx="60" cy="60" r="27"/></clipPath></defs>
  <circle cx="60" cy="60" r="58" class="seal-bg"/><circle cx="60" cy="60" r="31" class="seal-ring"/>
  <g class="seal-spin"><text class="seal-txt"><textPath href="#seal-path" textLength="272">{txt}</textPath></text></g>
  {center}
</svg>"""


def card_img(p):
    if p["brand"] == "martine":
        return p["card_img"]
    return p["images"][0] if p["images"] else None


def cat_label(p):
    if p["brand"] == "martine":
        return CM.CATEGORIES[p["cat"]]["nom"]
    return CL.CATEGORIES[p["cat"]]["nom"]


def product_card(p, eager=False, extra_cls="", types=()):
    img = card_img(p)
    second = p["images"][1] if len(p["images"]) > 1 and p["brand"] == "lucien" else None
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    media = (f'<img src="{img}" alt="{esc(p["nom"])}" width="400" height="400" {load}>' if img
             else f'<span class="ph" aria-hidden="true">{esc(p["nom"][:1])}</span>')
    if second:
        media += f'<img class="alt" src="{second}" alt="" width="400" height="400" loading="lazy" decoding="async">'
    quick = ""
    if p["stock"] and not p["variantes"] and not p["a_partir"]:
        quick = (f'<button class="quick" type="button" data-add data-id="{p["ref"]}" aria-label="Ajouter {esc(p["nom"])} au panier">'
                 f'{icon("plus")}</button>')
    badge = ""
    if p.get("prix_barre"):
        badge = '<span class="badge">Prix réduit</span>'
    elif not p["stock"]:
        badge = '<span class="badge badge-mute">Épuisé</span>'
    tile = f"tile-{stable(p['slug']) % 3}"
    return f"""<article class="card {extra_cls}" data-name="{esc(p['nom'].lower())}" data-price="{p['prix']:.2f}" data-types="{esc('|'.join(types))}">
  <a class="card-media {tile}" href="{p['url']}" tabindex="-1" aria-hidden="true">{media}{badge}</a>
  <div class="card-body">
    <p class="card-cat">{esc(cat_label(p))}{'<span class="handmade">fait main</span>' if is_maison(p) else ''}</p>
    <h3 class="card-title"><a href="{p['url']}">{esc(p['nom'])}</a></h3>
    {price_html(p)}
  </div>
  {quick}
</article>"""


def faq_block(items, title="Questions fréquentes"):
    if not items:
        return "", None
    dets = "".join(f'<details class="faq-item"><summary>{esc(q)}{icon("plus","i i-sm")}</summary><p>{esc(a)}</p></details>' for q, a in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f'<section class="faq wrap reveal"><h2 class="h2">{title}</h2><div class="faq-list">{dets}</div></section>', ld


def share_block(url, title, img):
    u = DOMAIN + url
    from urllib.parse import quote
    links = [
        ("facebook-logo", "Facebook", f"https://www.facebook.com/sharer/sharer.php?u={quote(u)}"),
        ("pinterest-logo", "Pinterest", f"https://pinterest.com/pin/create/button/?url={quote(u)}&media={quote(DOMAIN + (img or ''))}&description={quote(title)}"),
        ("whatsapp-logo", "WhatsApp", f"https://wa.me/?text={quote(title + ' ' + u)}"),
    ]
    a = "".join(f'<a class="share-btn" href="{h}" target="_blank" rel="noopener" aria-label="Partager sur {n}">{icon(i)}</a>' for i, n, h in links)
    a += f'<button class="share-btn" type="button" data-copy="{u}" aria-label="Copier le lien">{icon("link")}</button>'
    return f'<div class="share"><span>Partager</span>{a}</div>'


def article_card(a, brand, big=False):
    img = f"/assets/img/{a['image']}"
    return f"""<a class="post {'post-big' if big else ''}" href="{article_url(brand, a['slug'])}">
  <span class="post-media"><img src="{img}" alt="" loading="lazy" decoding="async" width="600" height="450"></span>
  <span class="post-meta">{a['minutes']} min de lecture</span>
  <span class="post-title">{esc(a['titre'])}</span>
</a>"""


def org_ld():
    return {
        "@context": "https://schema.org", "@type": "Organization", "name": "Le Père Lucien", "url": DOMAIN + "/",
        "logo": DOMAIN + "/assets/img/lucien-lelegard-portrait.webp",
        "founder": {"@type": "Person", "name": "Cyril Lelégard"}, "foundingDate": "2013",
        "address": {"@type": "PostalAddress", "streetAddress": "ZA de la Souvol, allée des Entreprises", "postalCode": "03380",
                    "addressLocality": "La Chapelaude", "addressCountry": "FR"},
        "telephone": "+33659518104", "sameAs": list(SOCIAL.values()),
        "brand": [{"@type": "Brand", "name": "Le Père Lucien"}, {"@type": "Brand", "name": "Mère Martine"}],
    }


def website_ld():
    return {"@context": "https://schema.org", "@type": "WebSite", "name": "Le Père Lucien", "url": DOMAIN + "/",
            "potentialAction": {"@type": "SearchAction", "target": DOMAIN + "/boutique/?q={search_term_string}",
                                "query-input": "required name=search_term_string"}}


def product_ld(p):
    brand = "Mère Martine" if p["brand"] == "martine" else "Le Père Lucien"
    desc = p["accroche"]
    ld = {
        "@context": "https://schema.org", "@type": "Product", "name": p["nom"], "sku": p["sku"],
        "image": [DOMAIN + i for i in p["images"]], "description": desc, "brand": {"@type": "Brand", "name": brand},
        "url": DOMAIN + p["url"],
        "offers": {"@type": "Offer", "priceCurrency": "EUR", "price": f"{p['prix']:.2f}", "url": DOMAIN + p["url"],
                   "availability": "https://schema.org/InStock" if p["stock"] else "https://schema.org/OutOfStock",
                   "itemCondition": "https://schema.org/NewCondition",
                   "shippingDetails": {"@type": "OfferShippingDetails", "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "FR"},
                                       "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "EUR"}}},
    }
    if p["reviews"] > 0 and p["rating"] > 0:
        ld["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": p["rating"], "reviewCount": p["reviews"]}
    return ld


# ---------------------------------------------------------------------------
# Pages produit
# ---------------------------------------------------------------------------
def li_list(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{icon('check','i i-sm')}<span>{esc(x)}</span></li>" for x in items) + "</ul>"


def render_product(p):
    is_m = p["brand"] == "martine"
    if is_m:
        cat = CM.CATEGORIES[p["cat"]]
        parent = CM.CATEGORIES[cat["parent"]] if cat["parent"] else None
        crumbs = [("Accueil", "/"), ("Mère Martine", f"{CM.BASE}/")]
        if parent:
            crumbs.append((parent["nom"], martine_cat_url(cat["parent"])))
        crumbs += [(cat["nom"], martine_cat_url(p["cat"])), (p["nom"], p["url"])]
        cat_url = martine_cat_url(p["cat"])
    else:
        cat = CL.CATEGORIES[p["cat"]]
        crumbs = [("Accueil", "/")]
        if cat["parent"]:
            crumbs.append((CL.CATEGORIES[cat["parent"]]["nom"], lucien_cat_url(cat["parent"])))
        crumbs += [(cat["nom"], lucien_cat_url(p["cat"])), (p["nom"], p["url"])]
        cat_url = lucien_cat_url(p["cat"])
    crumbs_html, crumbs_ld = breadcrumb(crumbs)

    # Galerie
    if p["images"]:
        main = f'<img src="{p["images"][0]}" alt="{esc(p["nom"])}" width="900" height="900" fetchpriority="high" data-main>'
        thumbs = ""
        if len(p["images"]) > 1:
            thumbs = '<div class="thumbs">' + "".join(
                f'<button type="button" class="thumb{" is-on" if i == 0 else ""}" data-thumb="{src}" aria-label="Voir la photo {i + 1}">'
                f'<img src="{src}" alt="" width="120" height="120" loading="lazy"></button>' for i, src in enumerate(p["images"])) + "</div>"
    else:
        main = f'<span class="ph ph-xl" aria-hidden="true">{esc(p["nom"][:1])}</span>'
        thumbs = ""

    # Sections
    if is_m:
        d = p["data"]
        desc_html = "".join(f"<p>{esc(x)}</p>" for x in d["description"])
        benefits = "".join(f'<div class="benefit"><p class="benefit-h">{esc(t)}</p><p>{esc(x)}</p></div>' for t, x in d["bienfaits"])
        usage = d["utilisation"]
        compo = d["composition"]
        specs = [d["contenance"]]
        cyril = None
        kw = d["mots_cles"]
    else:
        s = p["sections"]
        desc_html = "".join(f"<p>{esc(no_dash(x))}</p>" for x in s["texte"][:8]) or f"<p>{esc(p['nom'])}.</p>"
        benefits = ""
        usage = [no_dash(x) for x in s["conseils"]] or CL.CONSEILS_GAMME.get(p["cat"]) or CL.CONSEILS_GAMME.get(cat.get("parent") or "", [])
        compo = s["composition"]
        specs = [no_dash(x) for x in s["specs"]][:12]
        cyril = s["cyril"]
        kw = None

    acc = []
    acc.append(("Description", desc_html, True))
    if usage:
        acc.append(("Conseils d'utilisation", "<ol class='steps'>" + "".join(f"<li>{esc(x)}</li>" for x in usage) + "</ol>", False))
    if compo:
        acc.append(("Composition", f'<p class="inci">{esc(no_dash(compo))}</p>', False))
    if specs:
        acc.append(("Caractéristiques", "<ul class='specs'>" + "".join(f"<li>{esc(x)}</li>" for x in specs) + "</ul>", False))
    acc.append(("Livraison et retours", "<p>Expédition sous 48 h ouvrées en Colissimo, livraison offerte en France dès 80 €. Retour possible sous 14 jours pour un produit non ouvert.</p>", False))
    acc_html = "".join(
        f'<details class="acc" {"open" if o else ""}><summary>{esc(t)}{icon("plus","i i-sm")}</summary><div class="acc-body">{b}</div></details>'
        for t, b, o in acc)

    var_html = ""
    if p["variantes"]:
        label, opts = p["variantes"]
        name = f"v-{p['slug'][:20]}"
        var_html = f'<fieldset class="variants"><legend>{esc(label)}</legend><div class="var-opts">' + "".join(
            f'<label class="var"><input type="radio" name="{name}" value="{esc(o)}" {"checked" if i == 0 else ""}><span>{esc(o)}</span></label>'
            for i, o in enumerate(opts[:30])) + "</div></fieldset>"

    buy = (f'<div class="buy"><div class="qty" data-qty><button type="button" data-step="-1" aria-label="Diminuer la quantité">{icon("minus","i i-sm")}</button>'
           f'<input type="number" value="1" min="1" max="20" aria-label="Quantité" inputmode="numeric"><button type="button" data-step="1" aria-label="Augmenter la quantité">{icon("plus","i i-sm")}</button></div>'
           f'<button class="btn btn-accent btn-buy" type="button" data-add data-id="{p["ref"]}" data-with-options>Ajouter au panier</button></div>'
           if p["stock"] else '<p class="oos">Ce produit est épuisé. Écrivez-nous pour être prévenu de son retour.</p>')

    guide = None
    if p.get("guide"):
        guide = (ART_M if is_m else ART_L).get(p["guide"])
    guide_html = ""
    if guide:
        guide_html = f"""<a class="guide-link" href="{article_url(p['brand'], guide['slug'])}">
  <span class="guide-k">Le guide</span><span class="guide-t">{esc(guide['titre'])}</span>{icon('arrow-right')}</a>"""

    atelier_html = ""
    if is_maison(p):
        lignes = [("Fabriqué à", "Teillet-Argenty, Allier"), ("Méthode", "petits lots, coulés et conditionnés à la main"),
                  ("Formulé par", "Cyril Lelégard, ingénieur chimiste"), ("Contrôlé par", "une docteure en pharmacie")]
        if p["cat"] == "rasage/savons-a-raser":
            lignes[1] = ("Méthode", "saponifié à semi-ébullition, sans conservateur")
        elif p["cat"] in ("corps/savons", "corps-cheveux"):
            lignes[1] = ("Méthode", "saponifié à froid, surgras à 6 %")
        rows = "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in lignes)
        atelier_html = f"""<aside class="atelier-label" aria-label="Fiche d'atelier">
  <p class="al-h">Fiche d'atelier</p><dl>{rows}</dl>
  <p class="al-sign">fait main, avec soin</p>{seal("lucien", "seal seal-sm") if p["brand"] == "lucien" else '<img class="al-logo" src="/assets/img/logo-mere-martine.svg" alt="" width="96" height="96" loading="lazy">'}
</aside>"""
    cyril_html = f'<blockquote class="cyril"><p>« {esc(no_dash(cyril))} »</p><cite>Cyril Lelégard, fondateur</cite></blockquote>' if cyril else ""

    related = [BY_REF[r] for r in p["lies"]]
    rel_html = ""
    if related:
        title = "Complétez votre rituel" if is_m else "Complétez votre rasage"
        rel_html = f"""<section class="rail-sec wrap reveal" aria-labelledby="rel-h">
  <h2 class="h2" id="rel-h">{title}</h2>
  <div class="rail">{''.join(product_card(q) for q in related)}</div>
</section>"""

    benefit_sec = f'<section class="benefits wrap reveal" aria-label="Bienfaits">{benefits}</section>' if benefits else ""
    kw_html = f'<p class="kw">{esc(kw)}</p>' if kw else ""
    cross = ""
    if any(r.startswith("lucien:") for r in (p["data"]["lies"] if is_m else [])):
        pass

    body = f"""{crumbs_html}
<section class="pdp wrap">
  <div class="pdp-media">
    <div class="pdp-main tile-{stable(p['slug']) % 3}">{main}</div>
    {thumbs}
  </div>
  <div class="pdp-info">
    <a class="pdp-cat" href="{cat_url}">{esc(cat['nom'])}</a>
    <h1 class="pdp-title">{esc(p['nom'])}</h1>
    <p class="pdp-price">{price_html(p, 'price price-lg')}<small>TTC</small></p>
    <p class="pdp-lede">{esc(p['accroche'])}</p>
    {var_html}
    {buy}
    <ul class="reassure">
      <li>{icon('truck','i i-sm')}Expédié sous 48 h, offert dès 80 €</li>
      <li>{icon('flask','i i-sm')}{"Formulé et fabriqué à la main dans l'Allier" if is_maison(p) else "Sélectionné par l'atelier chez un artisan"}</li>
      <li>{icon('recycle','i i-sm')}Emballage recyclé, sans plastique</li>
    </ul>
    {guide_html}
    <div class="accs">{acc_html}</div>
    {cyril_html}
    {atelier_html}
    {share_block(p['url'], p['nom'], p['images'][0] if p['images'] else '')}
    {kw_html}
  </div>
</section>
{benefit_sec}
{rel_html}
<div class="sticky-buy" data-sticky-buy hidden>
  <span class="sb-name">{esc(p['nom'])}</span>{price_html(p)}
  <button class="btn btn-accent" type="button" data-scroll-buy>Ajouter</button>
</div>
<script type="application/json" id="product-data">{json.dumps({'id': p['ref'], 'nom': p['nom'], 'prix': p['prix'], 'img': card_img(p), 'url': p['url']}, ensure_ascii=False)}</script>"""

    page = {
        "brand": p["brand"], "path": p["url"], "title": p["seo_title"], "desc": p["seo_desc"],
        "og": p["images"][0] if p["images"] else None, "og_type": "product", "priority": 0.8, "freq": "weekly",
        "ld": [product_ld(p), crumbs_ld],
        "preload": f'<link rel="preload" as="image" href="{p["images"][0]}">' if p["images"] else "",
    }
    write(page, body)


# ---------------------------------------------------------------------------
# Pages catégorie
# ---------------------------------------------------------------------------
# Types de produits à l'intérieur d'une sous-catégorie (filtres), testés sur le nom sans accents.
TYPES = {
    "rasage/savons-a-raser": [("Pots et boîtes", r"(200|150|100|98) ?g", r"recharge"), ("Recharges 98 g", r"recharge", None),
                              ("Au suif", r"suif", None), ("Au lait d'ânesse", r"lainess|anesse|bandi", None), ("Éditions limitées", r"ebene|edition|coffret|premium|limitee", None)],
    "rasage/avant-apres-rasage": [("Lotions du barbier", r"lotion", None), ("Eaux de toilette", r"eau de toilette", None),
                                  ("Eaux de Cologne", r"eau de cologne", None), ("Baumes et après-rasages", r"baume|apres-rasage|apres rasage", r"lotion|eau de"), ("Pierre d'alun et soins", r"alun|pierre|crayon|gel", None)],
    "rasage/blaireaux": [("Fibre synthétique", r"synth|fibre", None), ("Pur blaireau", r"hmw|finest|manchurian|pur blaireau|silvertip|badger|super|best", r"synth"),
                         ("Soie et poils naturels", r"sanglier|soie|porc", None), ("Artisanaux MRed", r"mred", None)],
    "rasage/rasoirs-de-surete": [("Peigne fermé", r"ferme", None), ("Peigne ouvert", r"ouvert", None), ("Papillon", r"papillon", None),
                                 ("Réglables", r"reglable|progress", None), ("Artisanaux MRed", r"mred", None), ("Parker", r"parker", None), ("Voyage", r"voyage", None)],
    "rasage/shavettes-coupe-choux": [("Coupe-choux neufs", r"coupe-choux|coupe choux", r"occasion"), ("Coupe-choux d'occasion", r"occasion", None),
                                     ("Shavettes", r"shavette|non pliant|director", None)],
    "rasage/lames": [("Gillette", r"gillette", None), ("Derby", r"derby", None), ("Astra", r"astra", None), ("Feather", r"feather", None),
                     ("Laser", r"laser", None), ("Autres marques", r"voskhod|treet|big ben|personna|wilkinson|shark|polsilver|bic", r"gillette"), ("Demi-lames", r"demi|injecteur", None)],
    "rasage/bols": [("Grès artisanal", r"gres", None), ("Métal", r"inox|chrome|metal", None)],
    "rasage/accessoires": [("Supports", r"support|stand", None), ("Trousses et étuis", r"trousse|etui|tube|pochette", None),
                           ("Affûtage", r"affut|cuir d", None), ("Pièces détachées", r"tete|protection", None)],
    "barbe-moustache/huiles-baumes": [("Huiles", r"huile", None), ("Baumes", r"baume", None)],
    "barbe-moustache/peignes-brosses": [("Peignes", r"peigne", None), ("Brosses", r"brosse", None)],
    "corps-cheveux": [("Savons de toilette", r"savon|savonnette", None), ("Shampoings douche", r"shampoing", None), ("Soins du corps", r"huile|beurre", None)],
    "parfums": [("Eaux de toilette", r"toilette", None), ("Eaux de Cologne", r"cologne", None)],
    "accessoires-toilette": [("Peignes et brosses", r"peigne|brosse", None), ("Trousses et étuis", r"trousse|etui|pochette|tube", None),
                             ("Pinces à épiler", r"pince", None), ("Manucure", r"manucure", None), ("Pinceaux", r"pinceau", None)],
    "coin-des-affaires": [("Savons déclassés", r"declass", None), ("Coffrets", r"coffret|option", None), ("Coupe-choux d'occasion", r"occasion", None)],
}
SCENT_TYPES = [("Barbershop", r"barbershop"), ("Oud Santal", r"oud"), ("Abricot", r"abricot"), ("Cèdre Patchouli", r"cedre"),
               ("Cologne Fougère", r"fougere"), ("Traditionnel", r"traditionnel"), ("Sans parfum", r"nature|sans parfum"), ("Orange Eucalyptus", r"eucalyptus")]
for _k in ("barbe-moustache/shampoings", "barbe-moustache/cires-moustache"):
    TYPES[_k] = [(n, r, None) for n, r in SCENT_TYPES]
# Mère Martine : filtres par besoin
for _k in ("corps/huiles", "corps/cremes", "corps/baumes-solides", "corps/savons", "corps/rasage-feminin"):
    TYPES[_k] = [("Peaux sensibles", r"sensible|sans parfum|avoine|apaisant", None), ("Peau très sèche", r"tres seche|nourriss|karite|beurre", None),
                 ("Zéro déchet", r"solide|galet|stick|pain|savon|rasoir|bol", r"gel|lotion|creme a raser"), ("Parfumé", r"rose|jasmin|lavande|oranger|tilleul|fleur|neroli|vanille", r"sans parfum")]

BANNERS = {
    "rasage": "ambiance/rasage-savon-blaireau.webp", "rasage/savons-a-raser": "lucien-savon-barbier-mousse.webp",
    "rasage/avant-apres-rasage": "ambiance/parfumeur-flacons.webp", "rasage/blaireaux": "ambiance/rasage-savon-blaireau.webp",
    "rasage/bols": "ambiance/rasage-savon-blaireau.webp", "barbe-moustache": "ambiance/peigne-romarin.webp",
    "barbe-moustache/huiles-baumes": "lucien-atelier-baumes.webp", "barbe-moustache/peignes-brosses": "ambiance/peigne-romarin.webp",
    "barbe-moustache/cires-moustache": "lucien-cire-moustache.webp", "corps-cheveux": "lucien-savons-toilette.webp",
    "parfums": "ambiance/parfumeur-flacons.webp", "coin-des-affaires": "lucien-savon-barbier-nature.webp",
    "m:corps": "ambiance/atelier-lavande-mains.webp", "m:corps/huiles": "ambiance/huile-goutte.webp", "m:corps/cremes": "ambiance/creme-fouettee-mains.webp",
    "m:corps/baumes-solides": "ambiance/baume-mains.webp", "m:corps/savons": "ambiance/savons-panier.webp", "m:corps/rasage-feminin": "ambiance/rasage-vintage-femme.webp",
    "m:cheveux": "ambiance/cheveux-brosse-lavande.webp", "m:cheveux/soins": "ambiance/apothicaire-flacons.webp", "m:cheveux/brosses": "martine/brosse.webp",
    "m:cheveux/pommades-coiffantes": "martine/pommade-apothicaire.webp", "m:coin-des-affaires": "martine/coffret-cadeau.webp",
}


def plain(s):
    import unicodedata
    return "".join(ch for ch in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(ch) != "Mn")


def types_for(key, p):
    rules = TYPES.get(key)
    if not rules:
        return []
    txt = plain(p["nom"] + " " + (p["data"]["mots_cles"] if p["brand"] == "martine" else ""))
    out = []
    for label, inc, exc in rules:
        if re.search(inc, txt) and not (exc and re.search(exc, txt)):
            out.append(label)
    return out or ["Autres"]


def banner(brand, key):
    img = BANNERS.get(("m:" if brand == "martine" else "") + key)
    if img:
        return f"/assets/img/{img}"
    # sinon : la photo d'un produit phare de la catégorie, pour que chaque page ait son image
    for q in ordered(products_in(brand, key)):
        if q["images"] and "etiquette-" not in q["images"][0]:
            return q["images"][0]
    if "/" in key:
        img = BANNERS.get(("m:" if brand == "martine" else "") + key.split("/")[0])
    return f"/assets/img/{img}" if img else None


def cat_header(brand, c, pills, img):
    media = ""
    if img:
        if brand == "martine":
            media = f'<figure class="cat-media cat-arch reveal"><img src="{img}" alt="" width="700" height="900" fetchpriority="high"></figure>'
        else:
            media = f'<figure class="cat-media cat-photo reveal"><span class="tape" aria-hidden="true"></span><img src="{img}" alt="" width="700" height="700" fetchpriority="high"></figure>'
    return f"""<header class="cat-hd wrap{' has-media' if img else ''}">
  <div class="cat-hd-text">
    <h1 class="cat-h1">{esc(c['h1'])}</h1>
    <p class="cat-intro">{esc(c['intro'])}</p>
  </div>
  {media}
  {pills}
</header>"""


def sort_select():
    return """<label class="sort"><span class="sr">Trier les produits</span>
      <select data-sort>
        <option value="">Sélection de l'atelier</option>
        <option value="price-asc">Prix croissant</option>
        <option value="price-desc">Prix décroissant</option>
        <option value="name">Nom, de A à Z</option>
      </select>
    </label>"""


def group_sections(brand, groups, limit):
    """Une section par sous-catégorie : titre, nombre, aperçu des produits et lien « voir tout »."""
    out = []
    for gkey, name, url, prods, intro in groups:
        if not prods:
            continue
        shown = prods[:limit]
        more = (f'<a class="btn btn-ghost" href="{url}">Voir les {len(prods)} {esc(name.lower())} {icon("arrow-right","i i-sm")}</a>'
                if len(prods) > len(shown) else f'<a class="link-arrow" href="{url}">{esc(name)} {icon("arrow-right","i i-sm")}</a>')
        out.append(f"""<section class="subcat wrap" aria-labelledby="sc-{stable(url) % 99999}">
  <div class="subcat-hd">
    <h2 class="subcat-h" id="sc-{stable(url) % 99999}"><a href="{url}">{esc(name)}</a> <small>{len(prods)}</small></h2>
    {f'<p class="subcat-intro">{esc(clip(intro, 150))}</p>' if intro else ''}
  </div>
  <div class="grid">{''.join(product_card(q) for q in shown)}</div>
  <div class="subcat-more">{more}</div>
</section>""")
    return "\n".join(out)


def ordered(prods):
    return sorted(prods, key=lambda q: (not q["stock"], not q["images"], -stable(q["slug"]) % 997))


def render_category(brand, key):
    C = CM.CATEGORIES if brand == "martine" else CL.CATEGORIES
    c = C[key]
    url = martine_cat_url(key) if brand == "martine" else lucien_cat_url(key)
    caturl = martine_cat_url if brand == "martine" else lucien_cat_url
    prods = ordered(products_in(brand, key))
    crumbs = [("Accueil", "/")]
    if brand == "martine":
        crumbs.append(("Mère Martine", f"{CM.BASE}/"))
    if c["parent"]:
        crumbs.append((C[c["parent"]]["nom"], caturl(c["parent"])))
    crumbs.append((c["nom"], url))
    crumbs_html, crumbs_ld = breadcrumb(crumbs)

    kids = [(k, v) for k, v in C.items() if v["parent"] == key]
    sisters = [(k, v) for k, v in C.items() if c["parent"] and v["parent"] == c["parent"]]
    pills_src = kids or sisters
    pills = ""
    if pills_src:
        allurl = url if kids else caturl(c["parent"])
        alln = "Tout" if kids else f"Tout {C[c['parent']]['court'].lower()}"
        pills = f'<nav class="pills" aria-label="Sous-catégories"><a class="pill{" is-on" if kids else ""}" href="{allurl}">{alln}</a>' + "".join(
            f'<a class="pill{" is-on" if k == key else ""}" href="{caturl(k)}">{esc(v["court"])} <small>{len(products_in(brand, k))}</small></a>' for k, v in pills_src) + "</nav>"

    if kids:
        # page parente : une section par sous-catégorie
        groups = [(k, v["nom"], caturl(k), ordered(products_in(brand, k)), v.get("intro")) for k, v in kids]
        in_kids = {q["ref"] for g in groups for q in g[3]}
        rest = [q for q in prods if q["ref"] not in in_kids]
        if rest:
            groups.append((key, "Autres produits", url, rest, ""))
        listing = group_sections(brand, groups, 4 if brand == "lucien" else 8)
    else:
        # sous-catégorie : filtres par type
        facets = ""
        tagged = [(q, types_for(key, q)) for q in prods]
        labels_used = [lab for lab, _, _ in TYPES.get(key, []) + [("Autres", "", None)] if any(lab in t for _, t in tagged)]
        if len(labels_used) >= 2:
            facets = '<div class="facets" role="group" aria-label="Filtrer par type"><button type="button" class="facet is-on" data-facet="">Tout</button>' + "".join(
                f'<button type="button" class="facet" data-facet="{esc(lab)}">{esc(lab)} <small>{sum(1 for _, t in tagged if lab in t)}</small></button>'
                for lab in labels_used) + "</div>"
        cards = "".join(product_card(q, eager=i < 4, types=t) for i, (q, t) in enumerate(tagged))
        listing = f"""<section class="listing wrap" data-listing>
  {facets}
  <div class="toolbar">
    <p class="count"><strong data-count>{len(prods)}</strong> produits</p>
    {sort_select()}
  </div>
  <div class="grid" data-grid>{cards}</div>
  <div class="more"><button class="btn btn-ghost" type="button" data-more hidden>Afficher plus de produits</button></div>
</section>"""

    guide = (ART_M if brand == "martine" else ART_L).get(c.get("guide") or "")
    guide_html = ""
    if guide:
        guide_html = f"""<section class="cat-guide wrap reveal">
  <a class="cat-guide-in" href="{article_url(brand, guide['slug'])}">
    <img src="/assets/img/{guide['image']}" alt="" loading="lazy" width="640" height="480">
    <span class="cg-text"><span class="cg-k">Le guide</span><span class="cg-t">{esc(guide['titre'])}</span><span class="cg-cta">Lire le guide {icon('arrow-right','i i-sm')}</span></span>
  </a>
</section>"""
    faq_html, faq_ld = faq_block(c.get("faq", []))
    lds = [crumbs_ld, {"@context": "https://schema.org", "@type": "CollectionPage", "name": c["h1"], "url": DOMAIN + url,
                       "description": c["desc"], "mainEntity": {"@type": "ItemList", "numberOfItems": len(prods), "itemListElement": [
                           {"@type": "ListItem", "position": i + 1, "url": DOMAIN + q["url"]} for i, q in enumerate(prods[:30])]}}]
    if faq_ld:
        lds.append(faq_ld)

    cross = ""
    if brand == "martine" and key in ("corps/rasage-feminin", "cheveux/brosses", "corps/savons"):
        target = {"corps/rasage-feminin": ("/rasage/bols/", "Les bols de rasage en grès du Père Lucien"),
                  "cheveux/brosses": ("/barbe-moustache/peignes-brosses/", "Peignes en corne et brosses chez Le Père Lucien"),
                  "corps/savons": ("/corps-cheveux/", "Les savons de toilette de Gisèle, chez Le Père Lucien")}[key]
        cross = f'<a class="cross wrap reveal" href="{target[0]}"><span>{esc(target[1])}</span>{icon("arrow-up-right")}</a>'
    elif brand == "lucien" and key in ("corps-cheveux", "rasage/bols", "barbe-moustache/peignes-brosses", "rasage/rasoirs-de-surete"):
        target = {"corps-cheveux": (f"{CM.BASE}/corps/", "Soins du corps pour elle : la gamme Mère Martine"),
                  "rasage/bols": (f"{CM.BASE}/corps/rasage-feminin/", "Le rasage féminin chez Mère Martine"),
                  "barbe-moustache/peignes-brosses": (f"{CM.BASE}/cheveux/brosses/", "Brosse à cheveux en poils de sanglier, chez Mère Martine"),
                  "rasage/rasoirs-de-surete": (f"{CM.BASE}/produit/rasoir-surete-femme-laiton/", "Le rasoir de sûreté femme de Mère Martine")}[key]
        cross = f'<a class="cross wrap reveal" href="{target[0]}"><span>{esc(target[1])}</span>{icon("arrow-up-right")}</a>'

    body = f"""{crumbs_html}
{cat_header(brand, c, pills, banner(brand, key))}
{listing}
{guide_html}
{cross}
{faq_html}"""
    page = {"brand": brand, "path": url, "title": c["title"], "desc": c["desc"], "priority": 0.9, "freq": "weekly", "ld": lds,
            "og": banner(brand, key) or (card_img(prods[0]) if prods and card_img(prods[0]) else None)}
    write(page, body)


def render_boutique():
    crumbs_html, crumbs_ld = breadcrumb([("Accueil", "/"), ("Boutique", "/boutique/")])
    tops = [(k, v) for k, v in CL.CATEGORIES.items() if v["parent"] is None]
    pills = '<nav class="pills" aria-label="Gammes"><a class="pill is-on" href="/boutique/">Tout</a>' + "".join(
        f'<a class="pill" href="{lucien_cat_url(k)}">{esc(v["court"])} <small>{len(products_in("lucien", k))}</small></a>' for k, v in tops) + \
        f'<a class="pill pill-mm" href="{CM.BASE}/">Mère Martine <small>{len(MARTINE)}</small></a></nav>'
    # une section par sous-catégorie, regroupées par gamme
    blocks = []
    for k, v in tops:
        kids = [(kk, vv) for kk, vv in CL.CATEGORIES.items() if vv["parent"] == k]
        groups = ([(kk, vv["nom"], lucien_cat_url(kk), ordered(products_in("lucien", kk)), "") for kk, vv in kids]
                  or [(k, v["nom"], lucien_cat_url(k), ordered(products_in("lucien", k)), "")])
        blocks.append(f"""<div class="range" id="gamme-{k}">
  <div class="range-hd wrap"><h2 class="h2"><a href="{lucien_cat_url(k)}">{esc(v['nom'])}</a></h2><a class="link-arrow" href="{lucien_cat_url(k)}">Toute la gamme {icon('arrow-right','i i-sm')}</a></div>
  {group_sections("lucien", groups, 4)}
</div>""")
    mm_groups = [(k, f"Mère Martine, {v['nom'].lower()}", martine_cat_url(k), ordered(products_in("martine", k)), "")
                 for k, v in CM.CATEGORIES.items() if v["parent"] is None]
    blocks.append(f"""<div class="range range-mm">
  <div class="range-hd wrap"><h2 class="h2"><a href="{CM.BASE}/">Mère Martine</a></h2><a class="link-arrow" href="{CM.BASE}/">La gamme féminine {icon('arrow-right','i i-sm')}</a></div>
  {group_sections("martine", mm_groups, 4)}
</div>""")
    toc = '<nav class="range-toc wrap" aria-label="Aller à une gamme">' + "".join(
        f'<a href="#gamme-{k}">{esc(v["nom"])}</a>' for k, v in tops) + "</nav>"
    body = f"""{crumbs_html}
{cat_header("lucien", {"h1": "La boutique", "intro": f"{len(LUCIEN)} produits pour le rasage traditionnel, la barbe et la toilette, rangés par gamme : nos savons et soins fabriqués dans l'Allier, et le matériel que nous utilisons nous-mêmes."}, pills, "/assets/img/ambiance/rasage-savon-blaireau.webp")}
{toc}
{''.join(blocks)}"""
    write({"brand": "lucien", "path": "/boutique/", "title": "Boutique : rasage traditionnel, barbe et savons | Le Père Lucien",
           "desc": "Tous les produits Le Père Lucien : savons à raser, blaireaux, rasoirs, soins de la barbe, savons de toilette et eaux de Cologne.",
           "priority": 0.9, "freq": "weekly", "ld": [crumbs_ld]}, body)


# ---------------------------------------------------------------------------
# Accueils
# ---------------------------------------------------------------------------
def pick(slugs, brand="lucien"):
    pre = "p:" if brand == "lucien" else "m:"
    return [BY_REF[pre + s] for s in slugs if pre + s in BY_REF]


def process_section():
    steps = [
        ("lucien-atelier-flacons.webp", "Formuler", "Cyril met au point chaque recette. Il a fallu treize prototypes pour le savon du barbier.", "le labo"),
        ("lucien-atelier-baumes.webp", "Saponifier", "Le savon à raser cuit à semi-ébullition, les savons de toilette sont saponifiés à froid.", "en petits lots"),
        ("lucien-savons-toilette.webp", "Laisser sécher", "Les savons reposent plusieurs semaines avant d'être coupés et emballés.", "sans se presser"),
        ("lucien-atelier-etiquetage.webp", "Étiqueter à la main", "Chaque pot est rempli, fermé et étiqueté à l'atelier de Teillet-Argenty.", "un par un"),
    ]
    cards = "".join(f"""<figure class="polaroid reveal" style="--r:{r}deg">
  <span class="tape" aria-hidden="true"></span>
  <img src="/assets/img/{img}" alt="{esc(t)} à l'atelier" loading="lazy" width="600" height="600">
  <figcaption><strong>{esc(t)}</strong><span>{esc(d)}</span><em class="hand">{esc(n)}</em></figcaption>
</figure>""" for (img, t, d, n), r in zip(steps, (-2.5, 1.8, -1.2, 2.4)))
    return f"""<section class="process" aria-labelledby="process-h">
  <div class="wrap">
    <div class="process-hd"><h2 class="h2 reveal" id="process-h">De la cuve au pot.</h2>
    <p class="reveal">Tout ce qui porte notre nom est fabriqué à la main dans l'atelier, en petites séries.</p></div>
    <div class="polaroids">{cards}</div>
    <a class="link-arrow reveal" href="/la-maison/atelier/">Visiter l'atelier {icon('arrow-right','i i-sm')}</a>
  </div>
</section>"""


def render_home_lucien():
    best = pick(["savon-du-barbier-200-g-barbershop", "recharge-savon-du-barbier-au-karite-98g-santal", "huile-du-barbu-jojoba-30ml-traditionnel",
                 "blaireau-de-rasage-fibre-synthetique-charles-yaqi", "lotion-du-barbier-100-ml-barbershop", "le-shampoing-du-barbu-100g-oud-santal",
                 "rasoir-de-securite-metallique-peigne-ferme-tp-gw", "bol-a-raser-artisanal-en-gres-le-pere-lucien-82"])

    def tile(key, cls, img, alt):
        c = CL.CATEGORIES[key]
        n = len(products_in("lucien", key))
        return f"""<a class="bento-cell {cls} reveal" href="{lucien_cat_url(key)}">
  <img src="{img}" alt="{esc(alt)}" loading="lazy" decoding="async" width="800" height="800">
  <span class="bento-label"><span class="bento-name">{esc(c['nom'])}</span><span class="bento-n">{n} produits {icon('arrow-right','i i-sm')}</span></span>
</a>"""

    def first_img(key):
        for q in products_in("lucien", key):
            if q["images"]:
                return q["images"][0]
        return ""

    bento = (tile("rasage/savons-a-raser", "b-xl tile-blue", "/assets/img/lucien-savon-barbier-mousse.webp", "Savon du barbier Nature dans la mousse")
             + tile("barbe-moustache", "b-tall tile-stone", "/assets/img/lucien-cire-moustache.webp", "Cire à moustache Cèdre-Orange")
             + tile("rasage/blaireaux", "b-sq tile-0", first_img("rasage/blaireaux"), "Blaireau de rasage")
             + tile("rasage/rasoirs-de-surete", "b-sq tile-1", BY_REF["p:rasoir-de-securite-metallique-peigne-ferme-tp-gw"]["images"][0], "Rasoir de sûreté à peigne fermé")
             + tile("corps-cheveux", "b-wide tile-sage", "/assets/img/lucien-savons-toilette.webp", "Savons de toilette saponifiés à froid"))

    arts = articles.LUCIEN[:4]
    posts = "".join(f"""<a class="row-post reveal" href="{article_url('lucien', a['slug'])}">
  <span class="rp-n">{a['minutes']} min</span><span class="rp-t">{esc(a['titre'])}</span>
  <span class="rp-img" aria-hidden="true"><img src="/assets/img/{a['image']}" alt="" loading="lazy" width="320" height="240"></span>{icon('arrow-up-right')}
</a>""" for a in arts)

    ugc = ["lucien-savon-barbier-nature.webp", "lucien-atelier-etiquetage.webp", "lucien-cire-moustache.webp",
           "lucien-atelier-baumes.webp", "lucien-savons-toilette.webp", "lucien-atelier-flacons.webp"]
    ugc_html = "".join(f'<a class="ugc-cell reveal" href="{SOCIAL["instagram"]}" target="_blank" rel="noopener" aria-label="Voir sur Instagram"><img src="/assets/img/{u}" alt="" loading="lazy" width="400" height="400"></a>' for u in ugc)

    mm = pick(["huile-seche-satinante-corps-cheveux", "brosse-cheveux-poils-sanglier", "rasoir-surete-femme-laiton"], "martine")

    body = f"""
<section class="hero wrap">
  <div class="hero-copy">
    <h1 class="hero-h1"><span class="line"><span>Le rasage,</span></span><span class="line"><span>fait main</span></span><span class="line"><span>dans l'Allier.</span></span></h1>
    <p class="hero-sub">Savons à raser, soins de barbe et savons de toilette, fabriqués à Teillet-Argenty depuis 2013.</p>
    <div class="hero-ctas">
      <a class="btn btn-accent btn-lg" href="/rasage/savons-a-raser/">Voir les savons {icon('arrow-right','i i-sm')}</a>
      <a class="btn btn-ghost btn-lg" href="/conseils/debuter-rasage-traditionnel/">Débuter le rasage</a>
    </div>
  </div>
  <div class="hero-media">
    <div class="hero-frame tile-blue"><img src="/assets/img/lucien-savon-barbier-nature.webp" alt="Pot de savon du barbier Le Père Lucien, parfum Nature, posé sur de la mousse" width="1331" height="1395" fetchpriority="high"></div>
    {seal("lucien")}
    <a class="hero-tag" href="/produit/savon-du-barbier-200-g-barbershop/"><span>Savon du barbier, 200 g</span><strong>{euro(28.5)}</strong></a>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">
  {''.join('<span>Saponifié à semi-ébullition</span><span>Sans conservateur</span><span>Pots en acier rechargeables</span><span>Fabriqué à Teillet-Argenty</span><span>Vendu dans une vingtaine de pays</span>' for _ in range(2))}
</div></div>

<section class="sec wrap" aria-labelledby="gammes-h">
  <h2 class="h2 reveal" id="gammes-h">Les gammes</h2>
  <div class="bento">{bento}</div>
</section>

<section class="sec rail-sec wrap" aria-labelledby="best-h">
  <div class="sec-hd"><h2 class="h2 reveal" id="best-h">Les plus demandés</h2><a class="link-arrow" href="/boutique/">Toute la boutique {icon('arrow-right','i i-sm')}</a></div>
  <div class="rail">{''.join(product_card(q) for q in best)}</div>
</section>

<section class="story">
  <div class="wrap story-in">
    <figure class="story-img reveal"><img src="/assets/img/lucien-lelegard-portrait.webp" alt="Portrait ancien de Lucien Lelégard, le grand-père" loading="lazy" width="495" height="800"></figure>
    <div class="story-copy">
      <h2 class="story-h reveal">Treize prototypes pour un savon à raser.</h2>
      <p class="reveal">Cyril Lelégard, ingénieur chimiste, se rasait à l'ancienne comme son grand-père Lucien. Déçu par les savons du commerce, il a formulé le sien en 2012. Le treizième prototype a convaincu les membres du forum rasage-traditionnel.com, puis des barbiers d'une vingtaine de pays.</p>
      <dl class="figures reveal">
        <div><dt>2013</dt><dd>création de la savonnerie</dd></div>
        <div><dt>6 %</dt><dd>de surgraissage sur nos savons de toilette</dd></div>
        <div><dt>98 g</dt><dd>la recharge qui évite de jeter le pot</dd></div>
      </dl>
      <p class="signature reveal" aria-label="Signé Cyril Lelégard">Cyril Lelégard</p>
      <a class="link-arrow reveal" href="/la-maison/histoire/">Notre histoire {icon('arrow-right','i i-sm')}</a>
    </div>
  </div>
</section>

{process_section()}

<section class="mm-band" aria-labelledby="mm-h">
  <div class="wrap mm-in">
    <div class="mm-copy">
      <img class="mm-logo reveal" src="/assets/img/logo-mere-martine.svg" alt="" width="120" height="120" loading="lazy">
      <h2 class="mm-h reveal" id="mm-h">La Mère Martine, la gamme pour elle.</h2>
      <p class="reveal">Huiles, savons au lait de chèvre, brosses en poils de sanglier et rasage féminin. Même atelier, mêmes exigences.</p>
      <a class="btn btn-mm reveal" href="{CM.BASE}/">Découvrir Mère Martine {icon('arrow-right','i i-sm')}</a>
    </div>
    <div class="mm-cards">{''.join(product_card(q, extra_cls='card-on-color') for q in mm)}</div>
  </div>
</section>

<section class="sec wrap" aria-labelledby="conseils-h">
  <div class="sec-hd"><h2 class="h2 reveal" id="conseils-h">Le journal du rasage</h2><a class="link-arrow" href="/conseils/">Tous les conseils {icon('arrow-right','i i-sm')}</a></div>
  <div class="rows">{posts}</div>
</section>

<section class="sec ugc wrap" aria-labelledby="ugc-h">
  <div class="ugc-copy">
    <h2 class="h2 reveal" id="ugc-h">Votre rasage, sur Instagram.</h2>
    <p class="reveal">Publiez votre bol, votre mousse ou votre étagère avec <strong>#leperelucien</strong>. Nous repartageons chaque semaine.</p>
    <a class="btn btn-ghost reveal" href="{SOCIAL['instagram']}" target="_blank" rel="noopener">{icon('instagram-logo','i i-sm')} Suivre l'atelier</a>
  </div>
  <div class="ugc-grid">{ugc_html}</div>
</section>

<section class="assure wrap" aria-label="Nos engagements">
  <p>{icon('truck')}<span><strong>Livraison offerte</strong> dès 80 € en France</span></p>
  <p>{icon('recycle')}<span><strong>Recharges</strong> pour garder vos pots</span></p>
  <p>{icon('leaf')}<span><strong>Colis neutres</strong> en carbone avec Colissimo</span></p>
  <p>{icon('map-pin')}<span><strong>Fabriqué</strong> à Teillet-Argenty, Allier</span></p>
</section>"""
    write({"brand": "lucien", "path": "/", "title": "Le Père Lucien : savon à raser artisanal fabriqué en France",
           "desc": "Savonnerie artisanale de l'Allier : savons à raser, soins de barbe, savons de toilette et matériel de rasage traditionnel. Livraison offerte dès 80 €.",
           "priority": 1.0, "freq": "daily", "ld": [org_ld(), website_ld()], "og": "/assets/img/og-default.jpg",
           "preload": '<link rel="preload" as="image" href="/assets/img/lucien-savon-barbier-nature.webp">'}, body)


def render_home_martine():
    cats = [(k, v) for k, v in CM.CATEGORIES.items() if v["parent"] in ("corps", "cheveux")]
    imgs = {"corps/huiles": "huile-corps", "corps/cremes": "creme-corps", "corps/baumes-solides": "baume-fondant", "corps/savons": "savon-chevre",
            "corps/rasage-feminin": "rasoir-laiton", "cheveux/soins": "shampoing-sec", "cheveux/brosses": "brosse", "cheveux/pommades-coiffantes": "pommade-apothicaire"}
    cat_cells = "".join(f"""<a class="mm-cat reveal" href="{martine_cat_url(k)}">
  <span class="mm-cat-img"><img src="/assets/img/martine/{imgs[k]}-sm.webp" alt="" loading="lazy" width="560" height="560"></span>
  <span class="mm-cat-n">{esc(v['nom'])}</span><span class="mm-cat-c">{CM.CATEGORIES[v['parent']]['court']}</span>
</a>""" for k, v in cats)
    best = pick(["huile-seche-satinante-corps-cheveux", "savon-lait-de-chevre-bio", "creme-corps-velours", "brosse-cheveux-poils-sanglier", "pain-fondant-anti-irritations", "shampoing-sec-poudre-saupoudreuse"], "martine")
    coffrets = pick(["coffret-rituel-du-soir", "coffret-rasage-douceur", "coffret-cent-coups-de-brosse"], "martine")
    posts = "".join(article_card(a, "martine", big=(i == 0)) for i, a in enumerate(articles.MARTINE[:5]))
    body = f"""
<section class="hero hero-mm wrap">
  <div class="hero-copy">
    <img class="hero-logo" src="/assets/img/logo-mere-martine.svg" alt="La Mère Martine, cosmétique naturelle" width="132" height="132">
    <h1 class="hero-h1"><span class="line"><span>Des soins faits main,</span></span><span class="line"><span><em>comme autrefois.</em></span></span></h1>
    <p class="hero-sub">Huiles, savons au lait, baumes et brosses en poils de sanglier, préparés à la main dans l'Allier.</p>
    <div class="hero-ctas">
      <a class="btn btn-accent btn-lg" href="{CM.BASE}/corps/">Soins du corps {icon('arrow-right','i i-sm')}</a>
      <a class="btn btn-ghost btn-lg" href="{CM.BASE}/cheveux/">Soins des cheveux</a>
    </div>
  </div>
  <div class="hero-media hero-media-mm">
    <figure class="hero-arch"><img src="/assets/img/ambiance/atelier-lavande-mains.webp" alt="Mains qui préparent un soin à la lavande et aux fleurs fraîches" width="933" height="1400" fetchpriority="high"></figure>
    <figure class="hero-oval"><img src="/assets/img/ambiance/mere-martine-1920-sm.webp" alt="Portrait ancien de Mère Martine" width="360" height="640"></figure>
    <p class="hero-note hand">préparé à la main, en petits lots</p>
  </div>
</section>

<section class="sec wrap" aria-labelledby="mmcat-h">
  <h2 class="h2 reveal" id="mmcat-h">Par besoin</h2>
  <div class="mm-cats">{cat_cells}</div>
</section>

<section class="process process-mm" aria-labelledby="atelier-mm-h">
  <div class="wrap">
    <div class="process-hd"><h2 class="h2 reveal" id="atelier-mm-h">L'atelier, au féminin.</h2>
    <p class="reveal">Les plantes sont infusées, les beurres fondus au bain-marie, les savons coupés au fil. Rien n'est fait à la chaîne.</p></div>
    <div class="polaroids">{"".join(f'''<figure class="polaroid reveal" style="--r:{r}deg"><span class="tape" aria-hidden="true"></span>
      <img src="/assets/img/ambiance/{img}-sm.webp" alt="{esc(t)}" loading="lazy" width="600" height="600">
      <figcaption><strong>{esc(t)}</strong><span>{esc(d)}</span><em class="hand">{esc(n)}</em></figcaption></figure>''' for (img, t, d, n), r in zip([
        ("atelier-calendula", "Faire macérer", "Les fleurs de calendula infusent plusieurs semaines dans l'huile de tournesol.", "patience"),
        ("atelier-herbes-mains", "Piler les plantes", "Les herbes et zestes sont préparés le jour même.", "à la main"),
        ("atelier-versage", "Couler", "Huiles et miels sont versés à la louche, flacon par flacon.", "en petits lots"),
        ("atelier-bocaux", "Conserver", "Les macérats reposent en bocaux, à l'abri de la lumière.", "au calme")], (-2, 1.6, -1.4, 2.2)))}</div>
  </div>
</section>

<section class="sec rail-sec wrap" aria-labelledby="mmbest-h">
  <div class="sec-hd"><h2 class="h2 reveal" id="mmbest-h">Les essentiels</h2><a class="link-arrow" href="{CM.BASE}/corps/">Tous les soins {icon('arrow-right','i i-sm')}</a></div>
  <div class="rail">{''.join(product_card(q) for q in best)}</div>
</section>

<section class="ritual">
  <div class="wrap ritual-in">
    <div class="ritual-copy">
      <h2 class="story-h reveal">Cent coups de brosse, le soir.</h2>
      <p class="reveal">Le poil de sanglier répartit le sébum des racines aux pointes. C'est le plus vieux soin des cheveux, et le moins cher : une brosse dure des années.</p>
      <a class="link-arrow reveal" href="{CM.BASE}/conseils/bienfaits-brosse-poils-sanglier/">Les bienfaits de la brosse en sanglier {icon('arrow-right','i i-sm')}</a>
    </div>
    <div class="ritual-media">
      <figure class="ritual-img reveal"><img src="/assets/img/martine/brosse.webp" alt="Brosse en poils de sanglier posée sur une coiffeuse" loading="lazy" width="1024" height="1024"></figure>
      <div class="recipe reveal">
        <p class="recipe-h">Le soir, pour les cheveux secs</p>
        <ol class="hand">
          <li>deux cuillères de bain d'huile sur les longueurs</li>
          <li>un foulard de soie pour la nuit</li>
          <li>cent coups de brosse au réveil</li>
          <li>un seul shampoing, doux</li>
        </ol>
        <p class="recipe-sign hand">Mère Martine</p>
      </div>
    </div>
  </div>
</section>

<section class="sec wrap" aria-labelledby="coffrets-h">
  <div class="sec-hd"><h2 class="h2 reveal" id="coffrets-h">Coffrets cadeaux</h2><a class="link-arrow" href="{CM.BASE}/coin-des-affaires/">Coin des affaires {icon('arrow-right','i i-sm')}</a></div>
  <div class="grid grid-3">{''.join(product_card(q) for q in coffrets)}</div>
</section>

<section class="sec wrap" aria-labelledby="carnet-h">
  <div class="sec-hd"><h2 class="h2 reveal" id="carnet-h">Le carnet de Mère Martine</h2><a class="link-arrow" href="{CM.BASE}/conseils/">Tous les conseils {icon('arrow-right','i i-sm')}</a></div>
  <div class="posts">{posts}</div>
</section>

<section class="persona" aria-labelledby="persona-h">
  <div class="wrap persona-in">
    <figure class="persona-img reveal"><img src="/assets/img/ambiance/mere-martine-1920.webp" alt="Portrait ancien d'une femme au chapeau cloche, figure de Mère Martine" loading="lazy" width="787" height="1400"></figure>
    <div class="persona-copy">
      <h2 class="h2 reveal" id="persona-h">Qui est Mère Martine ?</h2>
      <p class="reveal">Une grand-mère comme on en a tous eu : un savon au lait sur le rebord de l'évier, une huile pour les cheveux le dimanche, cent coups de brosse avant de dormir. Ses gestes sont devenus nos recettes.</p>
      <p class="signature reveal">Mère Martine</p>
      <a class="link-arrow reveal" href="{CM.BASE}/histoire/">Notre histoire {icon('arrow-right','i i-sm')}</a>
    </div>
  </div>
</section>

<section class="pl-band" aria-labelledby="pl-h">
  <div class="wrap pl-in">
    <div class="pl-copy">
      <h2 class="pl-h reveal" id="pl-h">Fabriqué dans l'atelier du Père Lucien.</h2>
      <p class="reveal">Mère Martine partage l'atelier de Teillet-Argenty, les savons saponifiés à froid de Gisèle et la rigueur de formulation de Cyril.</p>
      <a class="btn btn-pl reveal" href="/">Le Père Lucien {icon('arrow-up-right','i i-sm')}</a>
    </div>
    <figure class="pl-img reveal"><img src="/assets/img/lucien-atelier-etiquetage.webp" alt="Étiquetage à la main des pots dans l'atelier de Teillet-Argenty" loading="lazy" width="617" height="771"></figure>
  </div>
</section>"""
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Mère Martine", "url": DOMAIN + CM.BASE + "/",
           "isPartOf": {"@type": "WebSite", "name": "Le Père Lucien", "url": DOMAIN + "/"},
           "about": {"@type": "Brand", "name": "Mère Martine"}}]
    write({"brand": "martine", "path": f"{CM.BASE}/", "title": "Mère Martine : soins naturels femme, corps et cheveux",
           "desc": "Huile sèche, crème corps parfumée, savon au lait de chèvre, brosse en poils de sanglier et rasage féminin. Soins naturels fabriqués dans l'Allier.",
           "priority": 1.0, "freq": "daily", "ld": ld, "og": "/assets/img/ambiance/atelier-lavande-mains.webp",
           "preload": '<link rel="preload" as="image" href="/assets/img/martine/huile-corps.webp">'}, body)


# ---------------------------------------------------------------------------
# Articles
# ---------------------------------------------------------------------------
def render_article(a, brand):
    url = article_url(brand, a["slug"])
    if brand == "martine":
        crumbs = [("Accueil", "/"), ("Mère Martine", f"{CM.BASE}/"), ("Le carnet", f"{CM.BASE}/conseils/"), (a["titre"], url)]
        others = [x for x in articles.MARTINE if x["slug"] != a["slug"]]
    else:
        crumbs = [("Accueil", "/"), ("Conseils", "/conseils/"), (a["titre"], url)]
        others = [x for x in articles.LUCIEN if x["slug"] != a["slug"]]
    crumbs_html, crumbs_ld = breadcrumb(crumbs)
    prods = [BY_REF[r] for r in a["produits"]]
    others = sorted(others, key=lambda x: stable(a["slug"] + x["slug"]))[:3]
    body = f"""{crumbs_html}
<article class="art">
  <header class="art-hd wrap">
    <p class="art-meta">{a['minutes']} min de lecture</p>
    <h1 class="art-h1">{esc(a['titre'])}</h1>
    <p class="art-lede">{esc(a['desc'])}</p>
  </header>
  <figure class="art-img wrap"><img src="/assets/img/{a['image']}" alt="" width="1600" height="1000" fetchpriority="high"></figure>
  <div class="art-grid wrap">
    <div class="prose">{resolve_links(a['corps'])}
      {share_block(url, a['titre'], '/assets/img/' + a['image'])}
    </div>
    <aside class="art-aside" aria-label="Produits cités">
      <p class="aside-h">Les produits de ce guide</p>
      <div class="aside-list">{''.join(product_card(q) for q in prods)}</div>
    </aside>
  </div>
</article>
<section class="sec wrap reveal" aria-labelledby="more-h">
  <h2 class="h2" id="more-h">À lire ensuite</h2>
  <div class="posts posts-3">{''.join(article_card(x, brand) for x in others)}</div>
</section>"""
    ld = [crumbs_ld, {"@context": "https://schema.org", "@type": "Article", "headline": a["titre"], "description": a["desc"],
                      "image": DOMAIN + "/assets/img/" + a["image"], "datePublished": TODAY, "dateModified": TODAY,
                      "author": {"@type": "Organization", "name": "Mère Martine" if brand == "martine" else "Le Père Lucien"},
                      "publisher": {"@type": "Organization", "name": "Le Père Lucien", "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/img/lucien-lelegard-portrait.webp"}},
                      "mainEntityOfPage": DOMAIN + url}]
    write({"brand": brand, "path": url, "title": a["title"], "desc": a["desc"], "og": "/assets/img/" + a["image"], "og_type": "article",
           "priority": 0.7, "ld": ld}, body)


def render_article_index(brand):
    lst = articles.MARTINE if brand == "martine" else articles.LUCIEN
    url = f"{CM.BASE}/conseils/" if brand == "martine" else "/conseils/"
    h1 = "Le carnet de Mère Martine" if brand == "martine" else "Le journal du rasage"
    intro = ("Des méthodes simples pour la peau, les cheveux et le rasage féminin, écrites dans l'atelier." if brand == "martine"
             else "Les gestes du rasage traditionnel et de l'entretien de la barbe, expliqués par l'atelier.")
    crumbs = [("Accueil", "/")] + ([("Mère Martine", f"{CM.BASE}/")] if brand == "martine" else []) + [(h1, url)]
    crumbs_html, crumbs_ld = breadcrumb(crumbs)
    extra = ""
    if brand == "lucien":
        extra = f'<a class="cross wrap" href="/conseils/videos/"><span>Les tutoriels vidéo, avec Filslade</span>{icon("arrow-right")}</a>'
    body = f"""{crumbs_html}
<header class="cat-hd wrap"><h1 class="cat-h1">{h1}</h1><p class="cat-intro">{intro}</p></header>
<section class="wrap"><div class="posts posts-index">{''.join(article_card(a, brand, big=(i == 0)) for i, a in enumerate(lst))}</div></section>
{extra}"""
    write({"brand": brand, "path": url, "title": f"{h1} : conseils et guides | {'Mère Martine' if brand == 'martine' else 'Le Père Lucien'}",
           "desc": intro, "priority": 0.7, "ld": [crumbs_ld]}, body)


def render_videos():
    vids = [
        ("Quel après-rasage choisir, comment l'utiliser", "https://www.leperelucien.com/%f0%9f%92%88-quel-apres-rasage-choisir-comment-utiliser-un-apres-rasage-avec-filslade/"),
        ("Comment bien faire mousser un savon Le Père Lucien", "https://www.leperelucien.com/comment-bien-faire-mousser-un-savon-le-pere-lucien-avec-filslade/"),
        ("Comment entretenir un savon Le Père Lucien", "https://www.leperelucien.com/comment-entretenir-un-savon-le-pere-lucien-avec-filslade/"),
        ("Comment empoter une recharge", "https://www.leperelucien.com/%f0%9f%92%88-comment-empoter-une-recharge-le-pere-lucien/"),
        ("Test du savon Rose de Pushkar", "https://www.leperelucien.com/test-rose-de-pushkar-filslade/"),
        ("Interview : Pogonotomie, l'art du barbier", "https://www.leperelucien.com/%f0%9f%92%88-interview-pogonotomie-art-du-barbier-%f0%9f%92%88-filslade/"),
        ("Rasage fraîcheur chez MRed, menthe forte", "https://www.leperelucien.com/rasage-fraicheur-chez-mred-menthe-forte-le-pere-lucien-%f0%9f%92%88-filslade/"),
        ("Reportage France 3 dans l'atelier", "https://www.leperelucien.com/reportage-france-3/"),
    ]
    crumbs_html, crumbs_ld = breadcrumb([("Accueil", "/"), ("Conseils", "/conseils/"), ("Tutoriels vidéo", "/conseils/videos/")])
    items = "".join(f'<a class="row-post" href="{u}" target="_blank" rel="noopener"><span class="rp-n">{icon("youtube-logo","i i-sm")}</span><span class="rp-t">{esc(t)}</span>{icon("arrow-up-right")}</a>' for t, u in vids)
    body = f"""{crumbs_html}
<header class="cat-hd wrap"><h1 class="cat-h1">Tutoriels vidéo</h1><p class="cat-intro">Filslade, YouTubeur et partenaire de l'atelier, montre les gestes du rasage traditionnel avec nos savons.</p></header>
<section class="wrap rows">{items}</section>"""
    write({"brand": "lucien", "path": "/conseils/videos/", "title": "Tutoriels vidéo rasage traditionnel avec Filslade | Le Père Lucien",
           "desc": "Vidéos : faire mousser un savon à raser, choisir un après-rasage, empoter une recharge. Avec Filslade.", "priority": 0.5, "ld": [crumbs_ld]}, body)


# ---------------------------------------------------------------------------
# Pages maison et pages simples
# ---------------------------------------------------------------------------
def simple_page(brand, path, title, desc, h1, inner, crumbs, priority=0.5, noindex=False, ld=None):
    crumbs_html, crumbs_ld = breadcrumb(crumbs)
    body = f"""{crumbs_html}
<header class="cat-hd wrap"><h1 class="cat-h1">{esc(h1)}</h1></header>
{inner}"""
    write({"brand": brand, "path": path, "title": title, "desc": desc, "priority": priority, "noindex": noindex,
           "ld": [crumbs_ld] + (ld or [])}, body)


def render_maison():
    M = CL.PAGES_MAISON
    cards = "".join(f'<a class="maison-card reveal" href="/la-maison/{k}/"><span class="mc-n">{esc(v["nom"])}</span><span class="mc-d">{esc(v["desc"])}</span>{icon("arrow-right")}</a>' for k, v in M.items())
    simple_page("lucien", "/la-maison/", "La maison : savonnerie familiale de l'Allier | Le Père Lucien",
                "Une savonnerie familiale fondée en 2013 à Teillet-Argenty : notre histoire, l'atelier, nos engagements et la presse.",
                "La maison", f'<section class="wrap maison-grid">{cards}</section>', [("Accueil", "/"), ("La maison", "/la-maison/")], 0.6)

    def mp(k, inner):
        v = M[k]
        simple_page("lucien", f"/la-maison/{k}/", v["title"], v["desc"], v["h1"], inner,
                    [("Accueil", "/"), ("La maison", "/la-maison/"), (v["nom"], f"/la-maison/{k}/")], 0.6)

    mp("histoire", f"""<section class="wrap split">
  <figure class="split-img reveal"><img src="/assets/img/lucien-lelegard-portrait.webp" alt="Lucien Lelégard, grand-père de Cyril" width="495" height="800" loading="lazy"><figcaption>Lucien Lelégard, qui a donné son nom à la maison.</figcaption></figure>
  <div class="prose">
    <p class="lede">Le Père Lucien est une savonnerie traditionnelle française fondée en 2013 par la famille Lelégard, une mère et son fils.</p>
    <h2>Cyril, le chimiste</h2>
    <p>Ingénieur chimiste et cosméticien, Cyril formule et teste les savons à raser et les soins de la marque. Adepte du rasage traditionnel et déçu par les produits existants, il commence ses essais en décembre 2012. Il faudra treize prototypes pour aboutir au premier savon du barbier.</p>
    <blockquote class="cyril"><p>« C'est ma passion pour le rasage traditionnel, venue de mon grand-père Lucien, qui m'a amené à fabriquer moi-même les produits que j'utilise. On peut être ingénieur chimiste et travailler artisanalement. »</p><cite>Cyril Lelégard</cite></blockquote>
    <h2>Gisèle, les savons de toilette</h2>
    <p>Grande voyageuse, Gisèle glane dans les pays qu'elle parcourt les secrets de beauté que les femmes lui confient. Elle en fait des savons de toilette parfumés. Ce sont ces recettes qui ont donné naissance à la gamme <a href="{CM.BASE}/">Mère Martine</a>.</p>
    <h2>Une pharmacienne pour contrôler</h2>
    <p>Natacha Mamdy, docteur en pharmacie, contrôle l'innocuité de chaque création avant sa mise en vente.</p>
    <p>Aujourd'hui, le catalogue compte une cinquantaine de références fabriquées dans l'atelier et distribuées dans une vingtaine de pays. Voir <a href="/la-maison/atelier/">l'atelier</a> et <a href="/revendeurs/">nos revendeurs</a>.</p>
  </div>
</section>""")
    mp("atelier", f"""<section class="wrap split">
  <div class="prose">
    <p class="lede">L'atelier est installé dans une ancienne bâtisse de lavandière à Teillet-Argenty, un village de l'Allier, au cœur de la France.</p>
    <h2>Les savons de toilette, saponifiés à froid</h2>
    <p>La saponification à froid préserve la glycérine végétale, naturellement hydratante, et les vertus des huiles. La recette marie les huiles d'olive, de coprah, de palme, de colza et de tournesol, pour un savon moussant, nettoyant et conditionnant.</p>
    <p>Chaque savon de toilette est surgras à 6 % afin de respecter le film hydrolipidique de la peau. Ce surgraissage n'emploie que des huiles précieuses, jamais saponifiées : karité, inca inchi, sésame, avocat. Voir les <a href="/corps-cheveux/">savons de toilette</a>.</p>
    <h2>Le savon du barbier, à semi-ébullition</h2>
    <p>Le savon à raser combine huiles végétales, potasse et glycérine végétale, sans conservateur ni agent de blanchiment. Sa mousse abondante, crémeuse et couvrante permet une glisse parfaite de la lame. Il existe avec ou sans huiles essentielles, en pot et en recharge. Voir les <a href="/rasage/savons-a-raser/">savons à raser</a>.</p>
    <h2>Aucun conservateur, aucun colorant</h2>
    <p>Les matières premières viennent, dans la mesure du possible, d'une agriculture locale et responsable.</p>
  </div>
  <div class="split-stack">
    <figure class="split-img reveal"><img src="/assets/img/lucien-atelier-baumes.webp" alt="Pots de baume en cours de coulage à l'atelier" width="1600" height="1061" loading="lazy"></figure>
    <figure class="split-img reveal"><img src="/assets/img/lucien-atelier-etiquetage.webp" alt="Étiquetage à la main des pots de savon du barbier" width="617" height="771" loading="lazy"></figure>
  </div>
</section>""")
    mp("engagements", f"""<section class="wrap split">
  <div class="prose">
    <p class="lede">Depuis 2013, Le Père Lucien choisit des emballages durables et réutilisables.</p>
    <h2>Verre, acier, recharges</h2>
    <p>Nos cosmétiques sont conditionnés en bouteilles de verre et en boîtes d'acier faites pour être réutilisées. Les <a href="/conseils/empoter-une-recharge/">recharges de savon du barbier</a> leur donnent une seconde vie, à un prix plus bas.</p>
    <h2>Pas de suremballage</h2>
    <p>L'emballage est celui nécessaire et suffisant pour conserver et expédier le produit. Les cartons et papiers que nous recevons sont broyés et réutilisés pour caler vos colis.</p>
    <h2>Des colis neutres en carbone</h2>
    <p>Nous confions nos colis à La Poste, qui compense 100 % de leur empreinte carbone. Nous avons obtenu le certificat de neutralité carbone pour les 1 927 colis expédiés en 2020.</p>
  </div>
  <figure class="split-img reveal"><img src="/assets/img/lucien-atelier-flacons.webp" alt="Flacons en verre alignés avant remplissage" width="425" height="531" loading="lazy"></figure>
</section>""")
    press = "".join(f'<a class="row-post" href="{u}" target="_blank" rel="noopener"><span class="rp-n">{esc(n)}</span><span class="rp-t">{esc(t)}</span>{icon("arrow-up-right")}</a>' for n, t, u in CL.PRESSE)
    mp("presse", f'<section class="wrap rows">{press}</section><p class="wrap note">Journaliste ? Écrivez-nous depuis la <a href="/contact/">page contact</a> pour recevoir photos et échantillons.</p>')


def render_misc():
    # FAQ
    faq_html, faq_ld = faq_block(CL.FAQ, "Toutes les questions")
    simple_page("lucien", "/faq/", "Questions fréquentes : livraison, savons, recharges | Le Père Lucien",
                "Livraison, retours, différence entre savon à raser et savon de toilette, recharges : les réponses à vos questions.",
                "Questions fréquentes", faq_html, [("Accueil", "/"), ("Questions fréquentes", "/faq/")], 0.5, ld=[faq_ld])
    mm_faq = []
    for k, v in CM.CATEGORIES.items():
        mm_faq += v.get("faq", [])
    faq_html, faq_ld = faq_block(mm_faq, "Vos questions sur nos soins")
    simple_page("martine", f"{CM.BASE}/faq/", "Questions fréquentes sur nos soins naturels | Mère Martine",
                "Huile sèche, baume solide, savon au lait d'ânesse, rasage féminin, brosse en poils de sanglier : nos réponses.",
                "Questions fréquentes", faq_html, [("Accueil", "/"), ("Mère Martine", f"{CM.BASE}/"), ("Questions fréquentes", f"{CM.BASE}/faq/")], 0.5, ld=[faq_ld])

    # Histoire Mère Martine
    simple_page("martine", f"{CM.BASE}/histoire/", "Mère Martine : l'histoire de la gamme féminine du Père Lucien",
                "Mère Martine est née des recettes de Gisèle Lelégard, dans l'atelier du Père Lucien à Teillet-Argenty.",
                "Les recettes de Gisèle", f"""<section class="wrap split">
  <div class="prose">
    <p class="lede">Mère Martine est la gamme féminine du Père Lucien. Elle est née des savons de toilette de Gisèle Lelégard.</p>
    <h2>Des recettes rapportées de voyage</h2>
    <p>Gisèle, cofondatrice de la savonnerie, a toujours composé les savons de toilette de la maison. Grande voyageuse, elle rapporte les secrets de beauté que les femmes lui confient : un savon au lait, une huile pour les cheveux, une poudre pour les racines.</p>
    <h2>Le même atelier</h2>
    <p>Les soins Mère Martine sont fabriqués à Teillet-Argenty, à côté des savons du Père Lucien. Cyril Lelégard, ingénieur chimiste, formule chaque produit ; une docteure en pharmacie en contrôle l'innocuité.</p>
    <h2>Pourquoi « Mère Martine »</h2>
    <p>Le Père Lucien porte le nom du grand-père de Cyril. Mère Martine lui répond : un nom de famille, simple, pour des soins du quotidien que l'on garde des années.</p>
    <p><a href="{CM.BASE}/corps/">Voir les soins du corps</a> ou <a href="{CM.BASE}/cheveux/">les soins des cheveux</a>.</p>
  </div>
  <div class="split-stack">
    <figure class="split-img reveal"><img src="/assets/img/ambiance/mere-martine-1920.webp" alt="Portrait ancien, figure de Mère Martine" width="787" height="1400" loading="lazy"></figure>
    <img class="histoire-logo reveal" src="/assets/img/logo-mere-martine.svg" alt="La Mère Martine, cosmétique naturelle" width="180" height="180" loading="lazy">
  </div>
</section>""", [("Accueil", "/"), ("Mère Martine", f"{CM.BASE}/"), ("Histoire", f"{CM.BASE}/histoire/")], 0.6)

    # Revendeurs
    rows = "".join(f'<div class="zone reveal"><p class="zone-n">{esc(z)}</p><p>{esc(t)}</p></div>' for z, t in CL.REVENDEURS)
    simple_page("lucien", "/revendeurs/", "Où acheter Le Père Lucien : revendeurs en France et dans le monde",
                "Nos savons à raser sont vendus par des barbiers et boutiques spécialisées en France, en Europe, en Amérique du Nord et en Asie.",
                "Nos revendeurs", f"""<section class="wrap">
  <p class="cat-intro">Le Père Lucien est distribué dans une vingtaine de pays. Pour trouver la boutique la plus proche, ou devenir revendeur, écrivez-nous.</p>
  <div class="zones">{rows}</div>
  <a class="btn btn-accent" href="/contact/">Devenir revendeur</a>
</section>""", [("Accueil", "/"), ("Revendeurs", "/revendeurs/")], 0.5)

    # Partenaires
    pts = "".join(f'<a class="partner reveal" href="{u}" target="_blank" rel="noopener"><span class="pt-n">{esc(n)}</span><span class="pt-d">{esc(d)}</span>{icon("arrow-up-right")}</a>' for n, d, u in CL.PARTENAIRES)
    simple_page("lucien", "/partenaires/", "Nos partenaires : artisans, forum et vidéastes | Le Père Lucien",
                "Les artisans, potiers, vidéastes et marques qui travaillent avec Le Père Lucien.",
                "Nos partenaires", f'<section class="wrap partners">{pts}</section>', [("Accueil", "/"), ("Partenaires", "/partenaires/")], 0.4)

    # Contact
    simple_page("lucien", "/contact/", "Contact et prestations professionnelles | Le Père Lucien",
                "Une question sur un produit, une commande ou une prestation professionnelle ? Écrivez à l'atelier.",
                "Nous écrire", f"""<section class="wrap contact">
  <form class="form" data-fake-form novalidate>
    <div class="field"><label for="c-nom">Votre nom</label><input id="c-nom" name="nom" required autocomplete="name"></div>
    <div class="field"><label for="c-mail">Votre e-mail</label><input id="c-mail" name="email" type="email" required autocomplete="email"></div>
    <div class="field"><label for="c-tel">Téléphone <small>(facultatif)</small></label><input id="c-tel" name="tel" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="c-sujet">Sujet</label><select id="c-sujet" name="sujet"><option>Question pour un achat</option><option>Suivi de commande</option><option>Contact professionnel</option><option>Devenir revendeur</option><option>Presse</option><option>Autre</option></select></div>
    <div class="field"><label for="c-msg">Votre message</label><textarea id="c-msg" name="message" rows="6" required></textarea></div>
    <button class="btn btn-accent" type="submit">Envoyer</button>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form>
  <div class="contact-side">
    <div><p class="aside-h">Adresse</p><p>Laboratoires Lelégard SAS<br>ZA de la Souvol, allée des Entreprises<br>03380 La Chapelaude</p></div>
    <div><p class="aside-h">Téléphone</p><p><a href="tel:+33659518104">06 59 51 81 04</a><br>Du lundi au vendredi, 8 h 30 à 16 h 30. Nous ne répondons pas aux SMS.</p></div>
    <div><p class="aside-h">Professionnels</p><p>Formation, accompagnement réglementaire, fabrication à façon : voir les <a href="https://laboratoireslelegard.com" target="_blank" rel="noopener">Laboratoires Lelégard</a>.</p></div>
  </div>
</section>""", [("Accueil", "/"), ("Contact", "/contact/")], 0.5)

    # Panier (noindex)
    simple_page("lucien", "/panier/", "Votre panier | Le Père Lucien", "Votre panier.", "Votre panier", """<section class="wrap checkout" data-checkout>
  <div class="co-list"><ul class="cart-list cart-list-lg" data-cart-list></ul>
  <div class="cart-empty" data-cart-empty><p>Votre panier est vide.</p><a class="btn btn-accent" href="/boutique/">Voir la boutique</a></div></div>
  <aside class="co-sum" data-cart-ft>
    <p class="cart-total"><span>Sous-total</span><strong data-cart-total>0,00 €</strong></p>
    <p class="cart-total"><span>Livraison</span><strong data-ship-cost>Calculée à l'étape suivante</strong></p>
    <div class="drawer-ship" data-ship></div>
    <button class="btn btn-accent btn-block" type="button" data-checkout-btn>Passer au paiement</button>
    <p class="note">Paiement sécurisé par carte, PayPal ou virement. Démonstration : aucune commande n'est enregistrée.</p>
  </aside>
</section>""", [("Accueil", "/"), ("Panier", "/panier/")], noindex=True)

    legal = {
        "mentions-legales": ("Mentions légales", "<p>Le site leperelucien.com est édité par Laboratoires Lelégard SAS, ZA de la Souvol, allée des Entreprises, 03380 La Chapelaude. Téléphone : 06 59 51 81 04. Directeur de la publication : Cyril Lelégard.</p><p>Hébergeur : à compléter.</p><p>Les photographies des produits et de l'atelier appartiennent au Père Lucien. Toute reproduction est soumise à autorisation.</p>"),
        "cgv": ("Conditions générales de vente", "<h2>Commandes</h2><p>Les prix sont indiqués en euros TTC. La commande est ferme après paiement.</p><h2>Livraison</h2><p>Expédition sous 48 h ouvrées par Colissimo. Livraison offerte en France métropolitaine dès 80 € d'achat.</p><h2>Rétractation</h2><p>Vous disposez de 14 jours à réception pour retourner un produit non ouvert, à vos frais. Le remboursement intervient sous 14 jours après réception du retour.</p>"),
        "confidentialite": ("Politique de confidentialité", "<p>Nous collectons uniquement les données nécessaires au traitement de vos commandes et à l'envoi de la lettre d'information si vous y êtes inscrit. Elles ne sont jamais cédées à des tiers.</p><p>Vous pouvez demander l'accès, la rectification ou la suppression de vos données depuis la <a href=\"/contact/\">page contact</a>.</p>"),
    }
    for slug, (t, inner) in legal.items():
        simple_page("lucien", f"/{slug}/", f"{t} | Le Père Lucien", f"{t} du site Le Père Lucien.", t,
                    f'<section class="wrap prose prose-narrow">{inner}</section>', [("Accueil", "/"), (t, f"/{slug}/")], 0.1)

    # Plan du site HTML : aucune page orpheline
    def ul(items):
        return "<ul>" + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for u, n in items) + "</ul>"
    cols = []
    for k, v in CL.CATEGORIES.items():
        if v["parent"] is None:
            items = [(lucien_cat_url(k), v["nom"])] + [(lucien_cat_url(kk), vv["nom"]) for kk, vv in CL.CATEGORIES.items() if vv["parent"] == k]
            cols.append(f'<div><p class="aside-h">{esc(v["nom"])}</p>{ul(items)}</div>')
    for k, v in CM.CATEGORIES.items():
        if v["parent"] is None:
            items = [(martine_cat_url(k), v["nom"])] + [(martine_cat_url(kk), vv["nom"]) for kk, vv in CM.CATEGORIES.items() if vv["parent"] == k]
            cols.append(f'<div><p class="aside-h">Mère Martine, {esc(v["court"].lower())}</p>{ul(items)}</div>')
    cols.append(f'<div><p class="aside-h">Conseils</p>{ul([(article_url("lucien", a["slug"]), a["titre"]) for a in articles.LUCIEN])}</div>')
    cols.append(f'<div><p class="aside-h">Le carnet</p>{ul([(article_url("martine", a["slug"]), a["titre"]) for a in articles.MARTINE])}</div>')
    cols.append(f'<div><p class="aside-h">La maison</p>{ul([("/la-maison/" + k + "/", v["nom"]) for k, v in CL.PAGES_MAISON.items()] + [("/revendeurs/", "Revendeurs"), ("/partenaires/", "Partenaires"), ("/faq/", "FAQ"), ("/contact/", "Contact"), (CM.BASE + "/histoire/", "Histoire de Mère Martine")])}</div>')
    prods = f'<div class="sitemap-prods"><p class="aside-h">Tous les produits</p>{ul([(p["url"], p["nom"]) for p in PRODUCTS])}</div>'
    simple_page("lucien", "/plan-du-site/", "Plan du site | Le Père Lucien", "Toutes les pages du site Le Père Lucien et Mère Martine.",
                "Plan du site", f'<section class="wrap sitemap-cols">{"".join(cols)}</section><section class="wrap">{prods}</section>',
                [("Accueil", "/"), ("Plan du site", "/plan-du-site/")], 0.3)

    # 404
    crumbs_html, _ = breadcrumb([("Accueil", "/"), ("Page introuvable", "/404.html")])
    write({"brand": "lucien", "path": "/404.html", "title": "Page introuvable | Le Père Lucien", "desc": "Cette page n'existe pas ou plus.", "noindex": True},
          f"""<section class="wrap notfound"><h1 class="cat-h1">Cette page a été rasée de près.</h1><p class="cat-intro">Elle n'existe pas ou plus. Reprenez depuis la boutique ou cherchez un produit.</p>
<div class="hero-ctas"><a class="btn btn-accent" href="/boutique/">La boutique</a><button class="btn btn-ghost" type="button" data-open-search>Rechercher</button></div></section>""")


# ---------------------------------------------------------------------------
# Fichiers techniques
# ---------------------------------------------------------------------------
def write_tech():
    # sitemap.xml
    urls = []
    for path, prio, freq, noindex in PAGES:
        if noindex or path.endswith(".html"):
            continue
        urls.append(f"  <url><loc>{DOMAIN}{path}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{prio:.1f}</priority></url>")
    (SITE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "\n".join(sorted(urls, key=lambda u: -float(re.search(r"<priority>([\d.]+)", u).group(1)))) + "\n</urlset>\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(f"""User-agent: *
Disallow: /panier/
Disallow: /commande/
Disallow: /mon-compte/
Disallow: /*?q=
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
""", encoding="utf-8")
    # index de recherche
    idx = [{"n": p["nom"], "u": p["url"], "i": card_img(p), "p": euro(p["prix"]), "b": "Mère Martine" if p["brand"] == "martine" else cat_label(p),
            "k": (p["data"]["mots_cles"] if p["brand"] == "martine" else " ".join(p["cats"])).lower()} for p in PRODUCTS]
    idx += [{"n": a["titre"], "u": article_url("lucien", a["slug"]), "i": "/assets/img/" + a["image"], "p": "Guide", "b": "Conseils", "k": a["desc"].lower()} for a in articles.LUCIEN]
    idx += [{"n": a["titre"], "u": article_url("martine", a["slug"]), "i": "/assets/img/" + a["image"], "p": "Guide", "b": "Le carnet", "k": a["desc"].lower()} for a in articles.MARTINE]
    (SITE / "assets" / "search.js").write_text("window.PL_SEARCH=" + json.dumps(idx, ensure_ascii=False) + ";", encoding="utf-8")
    # catalogue pour le panier
    cat = {p["ref"]: {"n": p["nom"], "p": p["prix"], "i": card_img(p), "u": p["url"]} for p in PRODUCTS}
    (SITE / "assets" / "catalogue.js").write_text("window.PL_CATALOGUE=" + json.dumps(cat, ensure_ascii=False) + ";", encoding="utf-8")
    # favicons
    (IMG / "favicon-lucien.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1F3FD1"/><text x="32" y="43" text-anchor="middle" font-family="Arial Narrow,Arial,sans-serif" font-weight="700" font-size="30" fill="#F3F2EE">PL</text></svg>', encoding="utf-8")
    (IMG / "favicon-martine.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="32" fill="#B8432F"/><text x="32" y="43" text-anchor="middle" font-family="Arial,sans-serif" font-style="italic" font-size="30" fill="#F7E6E0">MM</text></svg>', encoding="utf-8")
    # Polices embarquées en base64 : chargées seulement en ouverture directe (file://),
    # où Chrome bloque les polices locales.
    import base64
    fonts = SITE / "assets" / "fonts"
    faces = [("Archivo", "archivo", "normal", "100 900", "font-stretch: 62% 125%;"), ("Archivo", "archivo-italic", "italic", "100 900", "font-stretch: 62% 125%;"),
             ("Geist", "geist", "normal", "100 900", ""), ("Geist Mono", "geist-mono", "normal", "400 500", ""), ("Homemade Apple", "homemade-apple", "normal", "400", ""), ("Cormorant", "cormorant", "normal", "300 700", ""), ("Cormorant", "cormorant-italic", "italic", "300 700", "")]
    css = "".join(
        f'@font-face {{ font-family: "{fam}"; src: url(data:font/woff2;base64,{base64.b64encode((fonts / (f + ".woff2")).read_bytes()).decode()}) format("woff2"); '
        f'font-weight: {w}; font-style: {st}; {extra} font-display: swap; }}' + chr(10) for fam, f, st, w, extra in faces)
    (SITE / "assets" / "css" / "fonts-embedded.css").write_text(css, encoding="utf-8")
    og = IMG / "og-default.jpg"
    if not og.exists():
        im = Image.open(IMG / "lucien-savon-barbier-mousse.webp").convert("RGB")
        w, h = im.size
        im = im.crop((0, int(h * .22), w, int(h * .22) + int(w * 630 / 1200))).resize((1200, 630), Image.LANCZOS)
        im.save(og, "JPEG", quality=84)


def clean_output():
    for child in SITE.iterdir():
        if child.name == "assets":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def main():
    clean_output()
    render_home_lucien()
    render_home_martine()
    render_boutique()
    for k in CL.CATEGORIES:
        render_category("lucien", k)
    for k in CM.CATEGORIES:
        render_category("martine", k)
    for p in PRODUCTS:
        render_product(p)
    for a in articles.LUCIEN:
        render_article(a, "lucien")
    for a in articles.MARTINE:
        render_article(a, "martine")
    render_article_index("lucien")
    render_article_index("martine")
    render_videos()
    render_maison()
    render_misc()
    write_tech()
    print(f"{len(PAGES)} pages générées ({len(LUCIEN)} produits Le Père Lucien, {len(MARTINE)} Mère Martine)")


if __name__ == "__main__":
    main()
