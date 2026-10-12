"""Contrôle qualité du site généré : liens internes, images, balises SEO, pages orphelines.

Usage : python build/check.py
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"


def resolve(page, url):
    """Chemin relatif -> URL absolue du site (/x/y/)."""
    from posixpath import normpath, join
    url = url.split("#")[0].split("?")[0]
    base = "/" + page.parent.relative_to(SITE).as_posix() + "/" if page.parent != SITE else "/"
    out = normpath(join(base, url))
    if url.endswith("/") or url in (".", "./", "") or url.endswith("/."):
        out = out.rstrip("/") + "/"
    return out


def target(url):
    if url.endswith("/"):
        return SITE / url.strip("/") / "index.html" if url != "/" else SITE / "index.html"
    return SITE / url.lstrip("/")


pages = sorted(SITE.rglob("*.html"))
broken = defaultdict(set)
inbound = Counter()
titles = defaultdict(list)
descs = defaultdict(list)
problems = []
for f in pages:
    s = f.read_text(encoding="utf-8")
    rel = "/" + f.relative_to(SITE).as_posix().replace("index.html", "")
    if re.search(r'(href|src)="/(?!/)', s):
        problems.append(f"chemin absolu restant sur {rel}")
    for attr, raw in re.findall(r'(href|src)="([^"#:][^"]*|)"', s):
        if raw.startswith("//") or raw == "" or re.match(r"^[a-z]+:", raw):
            continue
        url = resolve(f, raw)
        if not target(url).exists():
            broken[url].add(rel)
        elif attr == "href" and url.endswith("/"):
            inbound[url.split("#")[0]] += 1
    t = re.search(r"<title>(.*?)</title>", s)
    d = re.search(r'<meta name="description" content="(.*?)">', s)
    noindex = 'content="noindex' in s
    if not noindex:
        if t:
            titles[t.group(1)].append(rel)
            if len(t.group(1)) > 70:
                problems.append(f"title long ({len(t.group(1))}) {rel}")
        if d:
            descs[d.group(1)].append(rel)
            if len(__import__("html").unescape(d.group(1))) > 160:
                problems.append(f"description longue ({len(d.group(1))}) {rel}")
    h1 = len(re.findall(r"<h1[ >]", s))
    if h1 != 1:
        problems.append(f"{h1} h1 sur {rel}")
    for img in re.findall(r"<img [^>]*>", s):
        if 'alt="' not in img:
            problems.append(f"img sans alt sur {rel}")
    for ch in ("—", "–"):
        if ch in re.sub(r"<script.*?</script>", "", s, flags=re.S):
            problems.append(f"tiret {ch!r} sur {rel}")

print(f"{len(pages)} pages contrôlées")
print(f"Liens/images cassés : {len(broken)}")
for u, src in list(broken.items())[:20]:
    print("  ", u, "<-", sorted(src)[:3])
dup_t = {k: v for k, v in titles.items() if len(v) > 1}
dup_d = {k: v for k, v in descs.items() if len(v) > 1}
print(f"Titles en double : {len(dup_t)}", list(dup_t.items())[:5])
print(f"Descriptions en double : {len(dup_d)}", list(dup_d.items())[:3])
orphans = []
for f in pages:
    rel = "/" + f.relative_to(SITE).as_posix().replace("index.html", "")
    if rel.endswith(".html") or rel in ("/",):
        continue
    if inbound[rel] == 0:
        orphans.append(rel)
print(f"Pages orphelines : {len(orphans)}", orphans[:10])
print(f"Autres remarques : {len(problems)}")
for p in problems[:30]:
    print("  ", p)
