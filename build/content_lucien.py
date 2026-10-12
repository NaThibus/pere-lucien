"""Contenus Le Père Lucien : gammes, pages maison, FAQ, partenaires.

Les produits viennent de data/produits-lucien.json (extraction du site actuel).
"""

# id WooCommerce -> catégorie du nouveau site
CATEGORIES = {
    "rasage": {
        "faq": [
            ("Que faut-il pour débuter le rasage traditionnel ?", "Un savon à raser, un blaireau, un rasoir de sûreté à peigne fermé et quelques lames. Notre guide détaille le choix de chaque objet."),
            ("Le rasage traditionnel irrite-t-il moins ?", "Oui, en général : une seule lame coupe en un passage, et la mousse au blaireau protège mieux la peau qu'une mousse en bombe."),
        ],
        "wc": 379, "parent": None, "nom": "Rasage traditionnel", "court": "Rasage",
        "h1": "Rasage traditionnel",
        "title": "Rasage traditionnel : savon à raser, blaireau, rasoir | Le Père Lucien",
        "desc": "Savons à raser artisanaux fabriqués dans l'Allier, blaireaux, rasoirs de sûreté, shavettes et après-rasages. Tout le rasage traditionnel.",
        "intro": "Le Père Lucien est né d'un savon à raser : Cyril Lelégard l'a mis au point en 2013, après treize prototypes. Nous fabriquons les savons, lotions et soins à Teillet-Argenty, et nous sélectionnons le matériel qui va avec : blaireaux, rasoirs de sûreté, coupe-choux, bols et lames.",
        "guide": "debuter-rasage-traditionnel",
    },
    "rasage/savons-a-raser": {
        "faq": [
            ("Pot ou recharge : que choisir ?", "Le pot métal de 200 g pour commencer, puis la recharge de 98 g, moins chère, que vous empotez dans le même pot."),
            ("Combien de rasages par pot ?", "Selon votre façon de charger le blaireau, un pot de 200 g dure de six mois à un an en rasage quotidien."),
            ("Faut-il garder le savon fermé ?", "Non, laissez-le ouvert : il sèche, durcit et dure plus longtemps."),
        ],
        "wc": 305, "parent": "rasage", "nom": "Savons à raser", "court": "Savons à raser",
        "h1": "Savons à raser artisanaux",
        "title": "Savon à raser artisanal fabriqué en France | Le Père Lucien",
        "desc": "Savon du barbier saponifié à semi-ébullition, au karité ou au suif. Mousse crémeuse et couvrante, en pot de 200 g ou en recharge de 98 g.",
        "intro": "Le savon du barbier est saponifié à semi-ébullition à partir d'huiles végétales, de potasse et de glycérine végétale, sans conservateur ni agent blanchissant. Sa mousse abondante, crémeuse et couvrante permet une glisse parfaite de la lame. Chaque parfum existe en pot métal de 200 g et en recharge de 98 g, plus économique.",
        "guide": "faire-mousser-savon-a-raser",
    },
    "rasage/avant-apres-rasage": {
        "wc": 306, "parent": "rasage", "nom": "Avant et après-rasage", "court": "Après-rasages",
        "h1": "Avant et après-rasage",
        "title": "Après-rasage, lotion du barbier et eau de Cologne | Le Père Lucien",
        "desc": "Lotions du barbier, eaux de toilette après-rasage et eaux de Cologne fabriquées dans l'Allier, assorties à nos savons à raser.",
        "intro": "Une lotion après-rasage referme les pores, désinfecte les micro-coupures et prolonge le parfum de votre savon. Nos lotions du barbier existent dans les mêmes senteurs que les savons ; les eaux de Cologne se portent seules.",
        "guide": "choisir-son-apres-rasage",
    },
    "rasage/blaireaux": {
        "wc": 310, "parent": "rasage", "nom": "Blaireaux de rasage", "court": "Blaireaux",
        "h1": "Blaireaux de rasage",
        "title": "Blaireau de rasage synthétique et pur blaireau | Le Père Lucien",
        "desc": "Blaireaux en fibre synthétique, pur blaireau et soies, dont des modèles artisanaux MRed. Pour monter une mousse dense en bol ou sur le visage.",
        "intro": "Le blaireau monte la mousse, la fait pénétrer dans la barbe et soulève les poils avant la lame. La fibre synthétique sèche vite et convient aux débutants ; le pur blaireau retient plus d'eau et donne une mousse plus chaude.",
        "guide": "faire-mousser-savon-a-raser",
    },
    "rasage/rasoirs-de-surete": {
        "faq": [
            ("Peigne ouvert ou peigne fermé ?", "Le peigne fermé pour débuter et pour un rasage quotidien ; le peigne ouvert pour une barbe de plusieurs jours."),
            ("Toutes les lames vont-elles sur tous les rasoirs ?", "Oui : tous nos rasoirs de sûreté utilisent la lame double tranchant standard."),
        ],
        "wc": 311, "parent": "rasage", "nom": "Rasoirs de sûreté", "court": "Rasoirs de sûreté",
        "h1": "Rasoirs de sûreté",
        "title": "Rasoir de sûreté : peigne ouvert, fermé, artisanal | Le Père Lucien",
        "desc": "Rasoirs de sûreté Parker, Mühle et rasoirs artisanaux MRed. Peigne fermé pour débuter, peigne ouvert pour les barbes denses.",
        "intro": "Le rasoir de sûreté utilise une lame double tranchant qui coûte quelques centimes. Le peigne fermé protège la peau et convient pour débuter ; le peigne ouvert coupe plus franchement les barbes de plusieurs jours.",
        "guide": "choisir-son-rasoir-de-surete",
    },
    "rasage/shavettes-coupe-choux": {
        "wc": 383, "parent": "rasage", "nom": "Shavettes et coupe-choux", "court": "Coupe-choux",
        "h1": "Shavettes et rasoirs coupe-choux",
        "title": "Rasoir coupe-choux et shavette de barbier | Le Père Lucien",
        "desc": "Coupe-choux neufs de Thiers et Solingen, coupe-choux d'occasion restaurés et shavettes à lame interchangeable.",
        "intro": "Le coupe-choux demande un apprentissage et un entretien (cuir d'affûtage, pierre), mais offre le rasage le plus précis. La shavette garde le geste du coupe-choux avec une lame jetable, sans affûtage.",
        "guide": "choisir-son-rasoir-de-surete",
    },
    "rasage/lames": {
        "wc": 385, "parent": "rasage", "nom": "Lames de rasoir", "court": "Lames",
        "h1": "Lames de rasoir",
        "title": "Lames de rasoir double tranchant | Le Père Lucien",
        "desc": "Lames double tranchant Gillette, Derby, Astra, Voskhod, Laser et demi-lames pour shavette. Testez plusieurs marques pour trouver la vôtre.",
        "intro": "Chaque marque de lame a son tranchant : une lame qui convient à l'un irrite l'autre. Commencez par un assortiment, puis tenez-vous-en à celle qui vous va. Comptez cinq à sept rasages par lame.",
        "guide": "choisir-son-rasoir-de-surete",
    },
    "rasage/bols": {
        "wc": 315, "parent": "rasage", "nom": "Bols de rasage", "court": "Bols",
        "h1": "Bols de rasage",
        "title": "Bol de rasage artisanal en grès | Le Père Lucien",
        "desc": "Bols à raser en grès tournés à la main par un potier, pièces uniques, et bols en inox. Pour monter une mousse dense au blaireau.",
        "intro": "Le bol sert à monter la mousse avant de l'appliquer. Nos bols en grès sont tournés par Adrien Couraud, potier : stries intérieures pour aérer la mousse, chaque pièce est unique.",
        "guide": "faire-mousser-savon-a-raser",
    },
    "rasage/accessoires": {
        "wc": 307, "parent": "rasage", "nom": "Accessoires de rasage", "court": "Accessoires",
        "h1": "Accessoires de rasage",
        "title": "Accessoires de rasage : support, trousse, cuir | Le Père Lucien",
        "desc": "Supports de rasoir et de blaireau, trousses de toilette en cuir, cuirs d'affûtage et têtes de rasoir de rechange.",
        "intro": "Un support garde le blaireau tête en bas pour qu'il sèche, une trousse protège le matériel en voyage, un cuir entretient le fil du coupe-choux.",
        "guide": "debuter-rasage-traditionnel",
    },
    "barbe-moustache": {
        "faq": [
            ("Huile ou baume à barbe ?", "L'huile nourrit la peau et assouplit le poil ; le baume ajoute une tenue légère. Beaucoup de barbus utilisent l'huile le matin et le baume pour coiffer."),
            ("Peut-on laver sa barbe avec un savon de toilette ?", "Mieux vaut un shampoing doux : le savon dessèche la peau sous la barbe et provoque des démangeaisons."),
        ],
        "wc": 354, "parent": None, "nom": "Barbe et moustache", "court": "Barbe",
        "h1": "Soins de la barbe et de la moustache",
        "title": "Huile à barbe, baume, shampoing et cire moustache | Le Père Lucien",
        "desc": "Huiles et baumes pour barbe au jojoba, shampoings solides du barbu, cires à moustache et peignes en corne. Fabriqué en France.",
        "intro": "Une barbe se lave, se nourrit et se discipline. Le shampoing du barbu nettoie sans assécher la peau dessous, l'huile au jojoba assouplit le poil, le baume le maintient. Tous existent dans les parfums de nos savons à raser.",
        "guide": "entretenir-sa-barbe",
    },
    "barbe-moustache/huiles-baumes": {
        "wc": 381, "parent": "barbe-moustache", "nom": "Huiles et baumes", "court": "Huiles et baumes",
        "h1": "Huiles et baumes pour barbe",
        "title": "Huile à barbe au jojoba et baume nourrissant | Le Père Lucien",
        "desc": "Huile du barbu au jojoba 30 ml et baume à barbe nourrissant naturel. Assouplit le poil, apaise les démangeaisons.",
        "intro": "L'huile nourrit la peau sous la barbe et supprime les démangeaisons des premières semaines. Le baume, plus riche, ajoute une tenue légère pour discipliner les poils rebelles.",
        "guide": "entretenir-sa-barbe",
    },
    "barbe-moustache/shampoings": {
        "wc": 380, "parent": "barbe-moustache", "nom": "Shampoings barbe", "court": "Shampoings",
        "h1": "Shampoings solides pour barbe",
        "title": "Shampoing solide pour barbe, le shampoing du barbu | Le Père Lucien",
        "desc": "Shampoing du barbu 100 g : shampoing solide pour barbe et cheveux, doux pour la peau, en huit parfums dont une version sans parfum.",
        "intro": "Un savon de toilette assèche la peau sous la barbe. Le shampoing du barbu nettoie le poil et la peau avec des tensioactifs doux, deux à trois fois par semaine.",
        "guide": "entretenir-sa-barbe",
    },
    "barbe-moustache/cires-moustache": {
        "wc": 382, "parent": "barbe-moustache", "nom": "Cires à moustache", "court": "Cires",
        "h1": "Cires à moustache",
        "title": "Cire à moustache naturelle fixation forte | Le Père Lucien",
        "desc": "Cire à moustache naturelle à fixation forte, en boîte de 15 g. Sept parfums dont une version sans parfum.",
        "intro": "Une cire naturelle à base de cire d'abeille et de beurres végétaux pour friser les pointes d'une moustache et la tenir toute la journée.",
        "guide": "entretenir-sa-barbe",
    },
    "barbe-moustache/peignes-brosses": {
        "wc": 388, "parent": "barbe-moustache", "nom": "Peignes et brosses", "court": "Peignes",
        "h1": "Peignes et brosses à barbe",
        "title": "Peigne à barbe en corne et brosse en sanglier | Le Père Lucien",
        "desc": "Peignes à barbe en corne véritable ou en bois, brosses à barbe en poils de sanglier ou en fibre de cactus.",
        "intro": "La corne et le bois ne créent pas d'électricité statique, contrairement au plastique. La brosse en poils de sanglier répartit l'huile et discipline la barbe.",
        "guide": "entretenir-sa-barbe",
    },
    "corps-cheveux": {
        "wc": 308, "parent": None, "nom": "Corps et cheveux", "court": "Corps",
        "h1": "Savons de toilette et soins du corps",
        "title": "Savon de toilette artisanal saponifié à froid | Le Père Lucien",
        "desc": "Savons de toilette saponifiés à froid surgras à 6 %, savon noir, beurre de karité, huile corporelle et shampoing douche.",
        "intro": "Gisèle Lelégard compose les savons de toilette : huiles d'olive, de coprah, de colza et de tournesol saponifiées à froid, puis un surgraissage à 6 % avec des huiles précieuses jamais saponifiées (karité, sésame, avocat).",
        "guide": "entretenir-son-savon",
    },
    "parfums": {
        "wc": 438, "parent": None, "nom": "Nos parfums", "court": "Parfums",
        "h1": "Eaux de toilette et eaux de Cologne",
        "title": "Eau de Cologne et eau de toilette homme | Le Père Lucien",
        "desc": "Eaux de toilette après-rasage et eaux de Cologne : Lavande royale, Grand cru, Élégance 1911, Rosée orange, Santal, Narcisse.",
        "intro": "Nos eaux de toilette prolongent les senteurs des savons à raser. Les eaux de Cologne, plus légères, se portent seules ou en superposition d'un après-rasage.",
        "guide": "choisir-son-apres-rasage",
    },
    "accessoires-toilette": {
        "wc": 352, "parent": None, "nom": "Accessoires de toilette", "court": "Accessoires",
        "h1": "Accessoires de toilette",
        "title": "Accessoires de toilette : pince à épiler, trousse | Le Père Lucien",
        "desc": "Pinces à épiler de Nogent et Dovo, pochettes manucure en cuir, trousses de toilette et pinceaux.",
        "intro": "Des outils de toilette choisis pour leur durée de vie : inox forgé, cuir tanné végétal, bois.",
        "guide": "debuter-rasage-traditionnel",
    },
    "coin-des-affaires": {
        "wc": 309, "parent": None, "nom": "Coin des affaires", "court": "Affaires",
        "h1": "Coin des affaires et coffrets",
        "title": "Coffret rasage et savons déclassés à prix réduit | Le Père Lucien",
        "desc": "Coffrets cadeaux rasage et savons du barbier déclassés : défaut d'aspect, formule identique, prix réduit.",
        "intro": "Un savon déclassé a un défaut d'aspect (couleur, surface) mais la même formule. Les coffrets réunissent savon, après-rasage et matériel à un prix inférieur à l'achat séparé.",
        "guide": "debuter-rasage-traditionnel",
    },
}

# Conseils d'utilisation affichés sur les fiches selon la gamme, quand la description
# du produit n'en contient pas.
CONSEILS_GAMME = {
    "rasage/savons-a-raser": [
        "Faites tremper le blaireau dans l'eau chaude une minute, puis essorez-le.",
        "Chargez le blaireau en le faisant tourner 20 à 30 secondes sur le savon.",
        "Montez la mousse dans un bol ou sur le visage, de 30 secondes à une minute : elle doit devenir brillante et crémeuse.",
        "Laissez le pot ouvert entre deux rasages : le savon durcit et dure plus longtemps.",
    ],
    "rasage/avant-apres-rasage": [
        "Rincez le visage à l'eau froide après le rasage.",
        "Versez quelques gouttes dans le creux de la main et tapotez sur la peau.",
        "Évitez le contour des yeux.",
    ],
    "rasage/blaireaux": [
        "Avant usage, trempez le blaireau dans l'eau chaude.",
        "Après usage, rincez-le à l'eau claire jusqu'à ce qu'il ne reste plus de savon.",
        "Essorez-le et faites-le sécher tête en bas sur un support.",
    ],
    "rasage/rasoirs-de-surete": [
        "Tenez le rasoir à environ 30 degrés de la peau, sans appuyer.",
        "Rasez d'abord dans le sens du poil, puis en travers si besoin.",
        "Rincez et séchez le rasoir après chaque rasage ; changez la lame toutes les cinq à sept utilisations.",
    ],
    "barbe-moustache/huiles-baumes": [
        "Sur barbe propre et sèche, versez trois à cinq gouttes dans la paume.",
        "Frottez les mains et massez jusqu'à la peau, puis peignez.",
        "Le baume s'applique de la même façon, en noisette chauffée entre les paumes.",
    ],
    "barbe-moustache/shampoings": [
        "Mouillez la barbe et frottez le pain entre vos mains pour faire mousser.",
        "Massez la barbe jusqu'à la peau, puis rincez abondamment.",
        "Deux à trois fois par semaine suffisent.",
    ],
    "barbe-moustache/cires-moustache": [
        "Prélevez un peu de cire avec l'ongle et chauffez-la entre le pouce et l'index.",
        "Peignez la moustache, appliquez la cire du centre vers les pointes.",
        "Torsadez les pointes entre les doigts.",
    ],
    "corps-cheveux": [
        "Faites mousser sur peau mouillée, massez puis rincez.",
        "Laissez sécher le savon sur un porte-savon ajouré entre deux douches.",
    ],
}

PAGES_MAISON = {
    "histoire": {
        "nom": "Notre histoire",
        "title": "Savonnerie artisanale familiale dans l'Allier | Le Père Lucien",
        "desc": "Le Père Lucien, savonnerie fondée en 2013 par Cyril Lelégard, ingénieur chimiste, et sa mère Gisèle, à Teillet-Argenty dans l'Allier.",
        "h1": "Une famille savonnière",
    },
    "atelier": {
        "nom": "L'atelier",
        "title": "L'atelier : saponification à froid | Le Père Lucien",
        "desc": "Savons de toilette saponifiés à froid, surgras à 6 %, savon du barbier à semi-ébullition. Visite de l'atelier de Teillet-Argenty.",
        "h1": "L'atelier de Teillet-Argenty",
    },
    "engagements": {
        "nom": "Nos engagements",
        "title": "Engagement éco-responsable : verre, acier, recharges | Le Père Lucien",
        "desc": "Flacons en verre, boîtes en acier, recharges de savon, cartons recyclés et colis neutres en carbone. Notre démarche depuis 2013.",
        "h1": "Moins d'emballage, plus de recharges",
    },
    "presse": {
        "nom": "Presse",
        "title": "Revue de presse et reportage France 3 | Le Père Lucien",
        "desc": "Le Père Lucien dans la presse : JDE, La Montagne, La Semaine de l'Allier, Reflet de l'Allier et reportage France 3.",
        "h1": "On parle de nous",
    },
}

PRESSE = [
    ("Le JDE", "Le Père Lucien : la success-story du savon artisanal d'Argenty parti à la conquête du monde.", "https://www.leperelucien.com/jde-le-pere-lucien-la-success-story-du-savon-artisanal-dargenty-parti-a-la-conquete-du-monde/"),
    ("La Montagne", "Le « petit cuistot » du savon de barbier.", "https://www.leperelucien.com/la-montagne-le-petit-cuistot-du-savon-de-barbier/"),
    ("La Semaine de l'Allier", "Des savons bien de chez nous.", "https://www.leperelucien.com/la-semaine-de-lallier-des-savons-bien-de-chez-nous/"),
    ("Reflet de l'Allier", "Portrait de la savonnerie de Teillet-Argenty.", "https://www.leperelucien.com/reflet-de-lallier/"),
    ("France 3 Auvergne", "Reportage vidéo dans l'atelier.", "https://www.leperelucien.com/reportage-france-3/"),
]

PARTENAIRES = [
    ("Laboratoires Lelégard", "Formation aux métiers de la cosmétique, accompagnement réglementaire, fabrication à façon et marque blanche.", "https://laboratoireslelegard.com"),
    ("MRed", "Michaël Redondaud fabrique à la main les rasoirs et blaireaux de nos éditions limitées.", "https://www.mred.site"),
    ("Filslade", "YouTubeur qui teste le matériel de rasage traditionnel ; nos tutoriels vidéo viennent de sa chaîne.", "https://www.filslade.com"),
    ("Rasage-traditionnel.com", "Le forum francophone du rasage : conseils techniques, revues de matériel, petites annonces.", "https://www.rasage-traditionnel.com"),
    ("Asinerie de la Vioune", "Gaëlle Blot élève des ânes dans le Bourbonnais. Son lait d'ânesse bio entre dans nos savons Lainess.", "https://www.lainess.com"),
    ("Poterie Adrien Couraud", "Le potier qui tourne nos bols de rasage en grès émaillé.", "https://poterieacouraud.com"),
    ("Darwin", "Marque rennaise de rasage traditionnel et de soins de barbe, contenants réutilisables.", "https://www.rasoirsdarwin.com"),
    ("Ici sont les dragons", "Marque de rasage traditionnel dans la pure tradition française.", "https://www.icisontdesdragons.fr"),
    ("La Source des Fées", "Cosmétiques écologiques du Dr Natacha Mamdy, pharmacienne herbaliste, qui contrôle l'innocuité de nos créations.", "https://www.etsy.com/shop/lasourcedesfees"),
    ("Couleur Savon", "Annuaire des savonneries artisanales et du savon à froid en France.", "https://www.couleur-savon.com"),
    ("Jean-Pierre Giraud", "Photographe de nos produits.", "https://www.jeanpierregiraud.fr"),
    ("Colissimo", "Transporteur de nos colis, avec compensation carbone.", "https://www.laposte.fr/colissimo"),
]

FAQ = [
    ("Où sont fabriqués vos produits ?", "Dans notre atelier de Teillet-Argenty, dans l'Allier. Les savons, lotions et soins sont formulés par Cyril Lelégard, ingénieur chimiste, et contrôlés par le Dr Natacha Mamdy, docteur en pharmacie."),
    ("Quelle est la différence entre un savon à raser et un savon de toilette ?", "Le savon à raser est saponifié à la potasse et à semi-ébullition : il produit une mousse dense et stable qui protège la peau sous la lame. Le savon de toilette, saponifié à froid, mousse moins mais nourrit davantage."),
    ("Comment utiliser une recharge de savon ?", "Placez la recharge dans votre pot vide et tassez-la. Notre guide « Empoter une recharge » montre la méthode pas à pas."),
    ("Quels sont les délais de livraison ?", "Les commandes partent sous 48 h ouvrées par Colissimo. La livraison est gratuite en France dès 80 € d'achat."),
    ("Livrez-vous à l'étranger ?", "Oui, en Europe et dans le monde. Nos produits sont aussi disponibles chez des revendeurs dans une vingtaine de pays."),
    ("Vos produits conviennent-ils aux femmes ?", "Oui. Notre gamme féminine, Mère Martine, propose des soins pour le corps, les cheveux et le rasage féminin."),
    ("Puis-je retourner un produit ?", "Vous disposez de 14 jours après réception pour retourner un produit non ouvert. Les conditions sont détaillées dans nos conditions générales de vente."),
    ("Proposez-vous des prestations aux professionnels ?", "Oui : formation, accompagnement réglementaire et fabrication à façon, via les Laboratoires Lelégard. Écrivez-nous depuis la page contact."),
]

REVENDEURS = [
    ("France", "Barbiers, salons de coiffure, boutiques de rasage traditionnel et épiceries fines, de Paris à Clermont-Ferrand."),
    ("Europe", "Belgique, Suisse, Allemagne, Italie, Espagne, Pays-Bas, Royaume-Uni et pays nordiques."),
    ("Amérique du Nord", "États-Unis et Canada, via des boutiques spécialisées dans le wet shaving."),
    ("Asie", "Corée du Sud, Inde et Russie, nos marchés les plus récents."),
]
