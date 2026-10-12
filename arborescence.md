# Arborescence — Le Père Lucien v3 & Mère Martine

Un seul nom de domaine (`leperelucien.com`, existant : on garde son ancienneté et ses backlinks), deux parties distinctes.

| Partie | Racine | Rôle |
|---|---|---|
| **Le Père Lucien** | `leperelucien.com/` | Rasage traditionnel, barbe, savonnerie, catalogue complet (268 réf.) |
| **Mère Martine** | `leperelucien.com/mere-martine/` | Gamme féminine : corps, cheveux, coffrets. Thème visuel propre, même panier. |

Les deux parties se citent (entrée « Mère Martine » dans le menu principal, bloc dédié sur l'accueil, footer, page Histoire, coffrets croisés). Le répertoire `/mere-martine/` concentre toute l'autorité du domaine sur la gamme féminine.

Légende : `P` = priorité sitemap.xml · `noindex` = exclu de l'indexation (robots + balise meta)

---

## 1. leperelucien.com

```
/                                               Accueil                                  P 1.0
│
├── /boutique/                                  Toute la boutique (filtres)              P 0.9
│   │
│   ├── /rasage/                                Rasage traditionnel                      P 0.9
│   │   ├── /rasage/savons-a-raser/             Savons à raser (41)                      P 0.9
│   │   ├── /rasage/avant-apres-rasage/         Avant et après-rasage (25)               P 0.8
│   │   ├── /rasage/blaireaux/                  Blaireaux de rasage (32)                 P 0.8
│   │   ├── /rasage/rasoirs-de-surete/          Rasoirs de sûreté (41)                   P 0.8
│   │   ├── /rasage/shavettes-coupe-choux/      Shavettes et coupe-choux (16)            P 0.7
│   │   ├── /rasage/lames/                      Lames (20)                               P 0.7
│   │   ├── /rasage/bols/                       Bols de rasage (14)                      P 0.7
│   │   └── /rasage/accessoires/                Accessoires de rasage (20)               P 0.7
│   │
│   ├── /barbe-moustache/                       Barbe et moustache                       P 0.9
│   │   ├── /barbe-moustache/huiles-baumes/     Huiles et baumes (14)                    P 0.8
│   │   ├── /barbe-moustache/shampoings/        Shampoings (8)                           P 0.8
│   │   ├── /barbe-moustache/cires-moustache/   Cires à moustache (7)                    P 0.7
│   │   └── /barbe-moustache/peignes-brosses/   Peignes et brosses (12)                  P 0.7
│   │
│   ├── /corps-cheveux/                         Corps et cheveux (11)                    P 0.8
│   ├── /parfums/                               Nos parfums (8)                          P 0.8
│   ├── /accessoires-toilette/                  Accessoires de toilette (25)             P 0.7
│   └── /coin-des-affaires/                     Coffrets et bonnes affaires (8)          P 0.8
│
├── /produit/{slug}/                            Fiche produit × 268                      P 0.8
│     photos · prix · bienfaits · conseils d'utilisation · composition (INCI)
│     · « Complétez votre rasage » (3-4 produits liés) · guide lié · partage social
│
├── /la-maison/                                 La maison                                P 0.6
│   ├── /la-maison/histoire/                    Une famille savonnière (Cyril, Gisèle, Lucien)
│   ├── /la-maison/atelier/                     L'atelier de Teillet-Argenty, saponification
│   ├── /la-maison/engagements/                 Engagement éco-responsable, recharges
│   └── /la-maison/presse/                      Revue de presse, reportage France 3
│
├── /conseils/                                  Le journal du rasage                     P 0.7
│   ├── /conseils/debuter-rasage-traditionnel/
│   ├── /conseils/faire-mousser-savon-a-raser/
│   ├── /conseils/entretenir-son-savon/
│   ├── /conseils/empoter-une-recharge/
│   ├── /conseils/choisir-son-apres-rasage/
│   ├── /conseils/choisir-son-rasoir-de-surete/
│   ├── /conseils/entretenir-sa-barbe/
│   └── /conseils/videos/                       Tutos vidéo (Filslade, MRed…)
│
├── /revendeurs/                                Points de vente (France, Europe, monde)  P 0.5
├── /partenaires/                               Partenaires (liens sortants qualifiés)   P 0.4
├── /faq/                                       Questions fréquentes (FAQPage)           P 0.5
├── /contact/                                   Contact + prestations pro                P 0.5
│
├── /panier/  /commande/  /mon-compte/                                                   noindex
└── /mentions-legales/  /cgv/  /confidentialite/                                         P 0.1
```

## 2. leperelucien.com/mere-martine/

Catégories reprises **à l'identique** du fichier « produit martine ».

```
/mere-martine/                                       Accueil Mère Martine           P 1.0
│
├── /mere-martine/corps/                             Produits pour le corps         P 0.9
│   ├── /mere-martine/corps/huiles/                  Huiles corps                   P 0.9
│   ├── /mere-martine/corps/cremes/                  Crèmes corps                   P 0.9
│   ├── /mere-martine/corps/baumes-solides/          Baumes solides                 P 0.9
│   ├── /mere-martine/corps/savons/                  Savons                         P 0.9
│   └── /mere-martine/corps/rasage-feminin/          Rasage féminin                 P 0.9
│
├── /mere-martine/cheveux/                           Produits pour les cheveux      P 0.9
│   ├── /mere-martine/cheveux/soins/                 Soins des cheveux              P 0.9
│   ├── /mere-martine/cheveux/brosses/               Brosses cheveux                P 0.9
│   └── /mere-martine/cheveux/pommades-coiffantes/   Pommade coiffante              P 0.9
│
├── /mere-martine/coin-des-affaires/                 Coin des affaires et cadeaux   P 0.9
│
├── /mere-martine/produit/{slug}/                    Fiche produit (43 réf.)      P 0.8
│
├── /mere-martine/conseils/                          Le carnet de Mère Martine      P 0.7
│   ├── utiliser-baume-solide-corps/          ← « comment utiliser un baume solide »
│   ├── routine-hydratation-peau-tres-seche/  ← « huile corps peau très sèche »
│   ├── bienfaits-savon-lait-anesse/          ← « bienfaits savon lait d'ânesse »
│   ├── eviter-irritations-rasage-femme/      ← « éviter les irritations rasage »
│   ├── pourquoi-rasoir-de-surete-femme/      ← « pourquoi passer au rasoir de sûreté »
│   ├── bain-huile-cheveux-secs/              ← « comment faire un bain d'huile »
│   ├── bienfaits-brosse-poils-sanglier/      ← « brosse sanglier bienfaits »
│   ├── volume-cheveux-fins/                  ← « volume cheveux fins »
│   └── idees-cadeaux-femme/                  ← « idée cadeau femme / fête des mères »
│
├── /mere-martine/histoire/                          Mère Martine et l'atelier      P 0.6
├── /mere-martine/faq/                               FAQ                            P 0.5
└── (panier, compte, contact et pages légales communs avec Le Père Lucien)
```

### Produits Mère Martine (43 fiches)

Un produit par ligne « Achat/produit » du fichier « produit martine ».

| Catégorie | Produits |
|---|---|
| **Huiles** (4) | Huile sèche satinante corps & cheveux · Huile de soin corps, rose & camélia · Huile hydratante traditionnelle à l'amande douce · Huile nourrissante corps, peau très sèche |
| **Crèmes** (5) | Crème hydratante velours · Crème corps parfumée, fleurs blanches & jasmin · Lait hydratant parfumé, rose & iris · Crème corps senteur florale, tilleul & violette · Crème hydratante naturelle, sans parfum |
| **Baumes solides** (5) | Pain fondant anti-irritations · Baume corps solide, karité & cacao · Beurre corporel solide, mangue & coco · Galet hydratant corps, fleur d'oranger · Stick hydratant corps, zones sèches |
| **Savons** (4) | Savon au lait de chèvre bio · Savon au lait d'ânesse bio · Savon naturel solide à l'avoine, peaux sensibles · Savon solide traditionnel à la lavande |
| **Rasage féminin** (7) | Huile pré & post-rasage apaisante · Pain de rasage ultra-moussant · Rasoir de sûreté femme en laiton · Crème à raser moussante femme · Gel de rasage femme, aloe & lin · Lotion apaisante après-rasage, hamamélis & bleuet · Bol de rasage en grès émaillé rose |
| **Soins des cheveux** (4) | Shampoing solide naturel · Shampoing sec en poudre · Huile de soin cheveux, ricin & camélia · Bain d'huile avant-shampoing, cheveux secs |
| **Brosses cheveux** (2) | Brosse à cheveux en poils de sanglier · Brosse sanglier démêlante de poche |
| **Pommade coiffante** (5) | Pommade coiffante à la cire d'abeille · Brume de mise en plis au lin · Cire coiffante légère · Pommade styling effet naturel, karité & aloe · Crème volumisante brushing |
| **Coin des affaires et cadeaux** (7) | Coffret rituel du soir · Coffret rasage douceur · Coffret des cent coups de brosse · Coffret cadeau cosmétique traditionnel · Box bien-être femme · Kit routine beauté nuit · Coffret soins cocooning |

---|---|
| **Huiles** | Huile sèche satinante corps · Huile nourrissante peau très sèche · Huile pré & post-rasage (aussi en Rasage féminin) |
| **Crèmes** | Crème corps velours fleur d'oranger · Lait hydratant parfumé rose & iris · Crème hydratante naturelle sans parfum |
| **Baumes solides** | Galet hydratant corps karité · Baume solide anti-irritations · Stick hydratant zones sèches |
| **Savons** | Savon lait de chèvre bio · Savon lait d'ânesse bio (Asinerie de la Vioune) · Savon solide lavande · Savon peaux sensibles avoine |
| **Rasage féminin** | Pain de rasage ultra-moussant · Gel de rasage peaux sensibles · Rasoir de sûreté femme laiton · Bol de rasage en grès |
| **Soins des cheveux** | Huile bain de soin cheveux secs · Shampoing solide naturel · Shampoing sec en poudre (saupoudreuse) · Brume de mise en plis au lin |
| **Brosses cheveux** | Brosse pneumatique poils de sanglier · Brosse de poche sanglier & hêtre |
| **Pommade coiffante** | Pommade coiffante à l'ancienne · Crème volumisante brushing · Cire coiffante légère |
| **Coin des affaires** | Coffret rituel du soir · Coffret cocooning · Box rasage douceur · Coffret fête des mères |

---

## 3. Maillage interne

1. **Vertical** : Accueil → Gamme → Sous-catégorie → Fiche produit, et retour par fil d'Ariane (BreadcrumbList) sur chaque page.
2. **Horizontal produit** : chaque fiche propose 3-4 produits complémentaires de catégories voisines (savon → blaireau → bol → après-rasage ; huile → baume → savon).
3. **Contenu ↔ commerce** : chaque article de conseils pointe vers 2-4 fiches produit avec des ancres descriptives (« notre savon au lait d'ânesse bio ») ; chaque fiche renvoie vers son guide d'utilisation.
4. **Croisé entre les deux parties** : coffrets duo, page Histoire, bandeau « L'autre maison », footer.
5. **Footer** : plan du site complet, donc aucune page orpheline.

## 4. Référencement et indexation

- `title` (≤ 60 car.) et `meta description` (≤ 155 car.) uniques, construits sur les mots-clés du fichier « produit martine » et les noms de gammes.
- Un seul `h1` par page, avec le mot-clé principal.
- Un `sitemap.xml` unique, avec les priorités ci-dessus (accueil 1.0, catégories 0.9, fiches 0.8, éditorial 0.5-0.7, légal 0.1).
- `robots.txt` : blocage de panier, commande et compte ; déclaration du sitemap.
- Données structurées JSON-LD : `Organization`, `WebSite` (SearchAction), `Product` + `Offer` + `AggregateRating`, `BreadcrumbList`, `Article`, `FAQPage`.
- URL canoniques, `hreflang` fr.

## 5. Réseaux sociaux et liens entrants

- Balises Open Graph et Twitter Card sur chaque page (image produit 1200×630, titre, description) : partages Facebook, Instagram, Pinterest et WhatsApp propres.
- Boutons de partage sur fiches et articles (Facebook, Pinterest, WhatsApp, copier le lien).
- Bloc « Vu sur Instagram » avec hashtag de marque (#leperelucien, #meremartine) pour faire remonter le contenu des clients.
- Liens sociaux dans l'en-tête et le footer ; page Presse et Partenaires pour les backlinks sectoriels (rasage-traditionnel.com, artdubarbier.com, Filslade).

## 6. Responsive

Pensé mobile d'abord : 375 px, 768 px, 1024 px, 1440 px. Menu tiroir sur mobile, filtres en panneau, barre « Ajouter au panier » collante sur les fiches produit, images `srcset` en lazy-load.
