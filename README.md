# Le Père Lucien v3 (+ Mère Martine)

Site e-commerce statique, un seul domaine (`leperelucien.com`), deux parties : Le Père Lucien (`/`) et Mère Martine (`/mere-martine/`).

## Dossiers

| Chemin | Contenu |
|---|---|
| `produit lucien.md` | Catalogue complet extrait de leperelucien.com (268 produits, par gamme) |
| `arborescence.md` | Arborescence, maillage interne, SEO, réseaux sociaux |
| `data/` | Données brutes : produits Lucien (JSON), images, contenus de marque |
| `build/` | Générateur Python et contenus (Martine, gammes Lucien, articles) |
| `site/` | **Le site généré**, prêt à être mis en ligne |

## Regénérer et vérifier

```
python build/build.py
python build/check.py
```

`check.py` contrôle liens cassés, images, titles et descriptions en double, pages orphelines, un seul h1 par page.

## Voir le site en local

- Le plus simple : double-cliquer sur **`Ouvrir le site.bat`** (lance un petit serveur et ouvre le navigateur).
- Ça marche aussi en ouvrant directement `site/index.html`, mais le serveur reste préférable : c'est ainsi que le site sera servi en ligne.

## Modifier un contenu

- Produits, prix, textes Mère Martine : `build/content_martine.py`
- Textes des gammes, FAQ, pages maison : `build/content_lucien.py`
- Articles de conseils : `build/articles.py` (liens internes `[[p:slug|texte]]`, vérifiés à la génération)
- Style : `site/assets/css/style.css` ; interactions : `site/assets/js/app.js`

## À savoir

- Le panier et le paiement sont une démonstration (localStorage, aucune commande réelle).
- Mère Martine : 43 produits (un par ligne du fichier « produit martine »). 13 ont une photo ; les autres ont un visuel « étiquette d'atelier » généré par `build/labels.py`. Pour remplacer une étiquette par une vraie photo, déposez `site/assets/img/martine/photos/<slug-du-produit>.webp` (carré, 1000 px conseillé) puis relancez `python build/build.py`.
- Logo Mère Martine : `site/assets/img/logo-mere-martine.svg`, redessiné en vectoriel d'après la page Facebook (régénérable avec `python build/logo.py`). Remplacez ce fichier par le logo officiel si vous l'avez.
- Images d'ambiance (dossier `site/assets/img/ambiance/`) : issues du zip fourni. Vérifiez leurs droits d'utilisation avant une mise en ligne publique.
- Les filtres par type des sous-catégories sont définis dans `TYPES` (build/build.py) ; les bannières de catégorie dans `BANNERS`.
- Les coffrets utilisent une mosaïque de leur contenu ; leur prix est calculé à -15 % de la somme des produits.
- Mentions légales : hébergeur à compléter.
