"""Articles de conseils (le journal du rasage + le carnet de Mère Martine).

Liens internes : [[p:slug|texte]] produit Lucien, [[m:slug|texte]] produit Martine,
[[c:chemin|texte]] catégorie Lucien, [[mc:chemin|texte]] catégorie Martine,
[[a:slug|texte]] article Lucien, [[ma:slug|texte]] article Martine.
Le générateur vérifie que chaque cible existe.
"""

LUCIEN = [
    {
        "slug": "debuter-rasage-traditionnel",
        "titre": "Débuter le rasage traditionnel : le matériel et les gestes",
        "title": "Débuter le rasage traditionnel : matériel et gestes | Le Père Lucien",
        "desc": "Savon à raser, blaireau, rasoir de sûreté : ce qu'il faut acheter pour débuter le rasage traditionnel et comment se raser sans irritation.",
        "image": "lucien-savon-barbier-mousse.webp",
        "minutes": 6,
        "corps": """
<p>Le rasage traditionnel demande quatre objets : un savon à raser, un blaireau, un rasoir à lame unique et une lotion après-rasage. Le reste (bol, support, trousse) vient ensuite.</p>
<h2>Le kit de départ</h2>
<ul>
<li><strong>Un savon à raser</strong> : notre [[p:savon-du-barbier-200-g-barbershop|savon du barbier Barbershop]] produit une mousse dense même en eau calcaire.</li>
<li><strong>Un blaireau synthétique</strong> : il sèche vite et ne demande aucun rodage. Le [[p:blaireau-de-rasage-fibre-synthetique-marcel-yaqi|blaireau Marcel]] est un bon premier choix.</li>
<li><strong>Un rasoir de sûreté à peigne fermé</strong>, le plus indulgent. Voir [[c:rasage/rasoirs-de-surete|nos rasoirs de sûreté]].</li>
<li><strong>Un assortiment de lames</strong> pour trouver celle qui vous convient : [[c:rasage/lames|nos lames]].</li>
</ul>
<h2>Les gestes, dans l'ordre</h2>
<p>Rasez-vous après la douche : la vapeur a déjà assoupli le poil. Montez la mousse au blaireau pendant 30 secondes à une minute (voir [[a:faire-mousser-savon-a-raser|comment bien faire mousser un savon]]), appliquez-la en couche épaisse.</p>
<p>Tenez le rasoir à environ 30 degrés et laissez son poids faire le travail : n'appuyez pas. Une première passe dans le sens du poil suffit les premières semaines. Rincez à l'eau froide, puis appliquez une lotion après-rasage.</p>
<h2>Les erreurs des débutants</h2>
<p>Appuyer sur le rasoir, garder une lame trop longtemps, et monter une mousse trop sèche. Si la peau chauffe, ajoutez quelques gouttes d'eau dans la mousse et changez de lame.</p>
""",
        "produits": ["p:savon-du-barbier-200-g-barbershop", "p:blaireau-de-rasage-fibre-synthetique-marcel-yaqi", "p:rasoir-de-securite-metallique-peigne-ferme-tp-gw", "p:lotion-du-barbier-100-ml-barbershop"],
    },
    {
        "slug": "faire-mousser-savon-a-raser",
        "titre": "Comment bien faire mousser un savon à raser",
        "title": "Comment faire mousser un savon à raser au blaireau | Le Père Lucien",
        "desc": "Charger le blaireau, doser l'eau, monter la mousse au bol ou sur le visage : la méthode pour une mousse crémeuse et couvrante.",
        "image": "lucien-savon-barbier-nature.webp",
        "minutes": 4,
        "corps": """
<p>Une bonne mousse de rasage est brillante, dense et tient sur le blaireau retourné. Elle se travaille de 30 secondes à une minute : son changement d'aspect vous indique qu'elle est prête.</p>
<h2>Préparer le blaireau</h2>
<p>Trempez le blaireau dans l'eau chaude pendant que vous vous lavez le visage. Essorez-le d'une pression : il doit rester humide sans goutter.</p>
<h2>Charger le savon</h2>
<p>Faites tourner le blaireau sur le [[c:rasage/savons-a-raser|savon à raser]] pendant 20 à 30 secondes, sans écraser les poils. Le blaireau ressort couvert d'une pâte épaisse.</p>
<h2>Monter la mousse</h2>
<p>Dans un [[c:rasage/bols|bol de rasage]], fouettez en ajoutant de l'eau une demi-cuillère à la fois. La mousse passe de bulles grossières à une crème lisse. Arrêtez quand elle brille et que les bulles ne se voient plus.</p>
<p>Sur le visage, le principe est le même : petits cercles, eau ajoutée au bout des poils du blaireau.</p>
<h2>Trop sèche, trop mouillée</h2>
<p>Une mousse qui sèche sur la peau manque d'eau. Une mousse qui retombe en bulles manque de savon : rechargez quelques secondes.</p>
<p>Le savon du barbier se conserve ouvert : il sèche, durcit et dure plus longtemps. Lire aussi [[a:entretenir-son-savon|comment entretenir son savon]].</p>
""",
        "produits": ["p:savon-du-barbier-200-g-cuir", "p:bol-a-raser-artisanal-en-gres-le-pere-lucien-82", "p:blaireau-de-rasage-fibre-synthetique-charles-yaqi"],
    },
    {
        "slug": "entretenir-son-savon",
        "titre": "Comment entretenir un savon Le Père Lucien",
        "title": "Entretenir son savon à raser et son savon de toilette | Le Père Lucien",
        "desc": "Laisser le pot ouvert, sécher le savon de toilette, ranger le blaireau : les gestes pour faire durer vos savons artisanaux.",
        "image": "lucien-savons-toilette.webp",
        "minutes": 3,
        "corps": """
<p>Un savon artisanal ne contient ni conservateur ni durcisseur. Bien rangé, il dure pourtant plus longtemps qu'un savon industriel.</p>
<h2>Le savon à raser</h2>
<p>Laissez le pot ouvert en permanence. Le savon sèche, devient plus dur et plus économique, et sa fragrance parfume la salle de bain. Ne laissez pas d'eau stagner à sa surface.</p>
<h2>Le savon de toilette</h2>
<p>Nos [[c:corps-cheveux|savons de toilette]] sont saponifiés à froid et surgras à 6 % : ils sont plus tendres. Posez-les sur un porte-savon ajouré, hors du jet de la douche. Un savon qui sèche entre deux usages dure deux fois plus longtemps.</p>
<h2>Le blaireau</h2>
<p>Rincez-le jusqu'à ce que l'eau soit claire, essorez-le et faites-le sécher tête en bas. Voir [[c:rasage/accessoires|nos supports de blaireau]].</p>
<p>Quand votre pot est vide, ne le jetez pas : [[a:empoter-une-recharge|empotez une recharge]].</p>
""",
        "produits": ["p:support-de-blaireau-resine-transparent", "p:savon-de-toilette-huile-avocat", "p:recharge-savon-du-barbier-barbershop-98g"],
    },
    {
        "slug": "empoter-une-recharge",
        "titre": "Comment empoter une recharge de savon à raser",
        "title": "Empoter une recharge de savon du barbier | Le Père Lucien",
        "desc": "Les recharges de 98 g se glissent dans votre pot en métal. La méthode pour tasser la recharge et réutiliser le même pot pendant des années.",
        "image": "lucien-atelier-etiquetage.webp",
        "minutes": 3,
        "corps": """
<p>Nos boîtes en acier sont faites pour durer. La recharge de 98 g permet de les réutiliser, à un prix plus bas que le pot complet.</p>
<h2>La méthode</h2>
<ul>
<li>Nettoyez le pot à l'eau chaude et séchez-le.</li>
<li>Coupez la recharge en deux ou trois morceaux.</li>
<li>Passez les morceaux 15 secondes au micro-ondes : le savon devient malléable.</li>
<li>Tassez-les au fond du pot avec le dos d'une cuillère, puis lissez la surface.</li>
<li>Laissez reposer une nuit, couvercle ouvert.</li>
</ul>
<p>Toutes nos senteurs existent en recharge : [[p:recharge-savon-du-barbier-au-karite-98g-santal|Santal]], [[p:recharge-savon-du-barbier-98-g-vetiver|Vétiver]], [[p:recharge-savon-du-barbier-barbershop-98g|Barbershop]] et les autres dans [[c:rasage/savons-a-raser|les savons à raser]].</p>
<p>C'est une partie de [[u:/la-maison/engagements/|notre engagement]] : moins d'emballages jetés.</p>
""",
        "produits": ["p:recharge-savon-du-barbier-au-karite-98g-santal", "p:recharge-savon-du-barbier-98-g-vetiver", "p:recharge-savon-du-barbier-barbershop-98g"],
    },
    {
        "slug": "choisir-son-apres-rasage",
        "titre": "Quel après-rasage choisir et comment l'utiliser",
        "title": "Quel après-rasage choisir : lotion, eau de toilette | Le Père Lucien",
        "desc": "Lotion du barbier, eau de toilette alcoolisée ou baume : choisir un après-rasage selon votre peau, et l'appliquer correctement.",
        "image": "lucien-atelier-flacons.webp",
        "minutes": 4,
        "corps": """
<p>Un après-rasage referme les pores, désinfecte les micro-coupures et prolonge le parfum du savon. Il se choisit selon votre peau.</p>
<h2>Peau normale : la lotion du barbier</h2>
<p>Légère, elle rafraîchit sans tirer. Nos [[c:rasage/avant-apres-rasage|lotions du barbier]] existent dans les mêmes senteurs que les savons, comme la [[p:lotion-du-barbier-100-ml-barbershop|lotion Barbershop]].</p>
<h2>Peau grasse : l'eau de toilette alcoolisée</h2>
<p>Plus astringente, elle pique quelques secondes puis assainit. Voir l'[[p:eau-de-toilette-apres-rasage-100-ml-santal|eau de toilette Santal]].</p>
<h2>Peau sèche ou sensible : le baume</h2>
<p>Sans alcool, il nourrit. Les barbus peuvent utiliser un [[c:barbe-moustache/huiles-baumes|baume à barbe]] sur les zones rasées.</p>
<h2>L'application</h2>
<p>Rincez à l'eau froide, séchez en tamponnant, versez quelques gouttes dans la paume et tapotez. Ne frottez pas.</p>
""",
        "produits": ["p:lotion-du-barbier-100-ml-barbershop", "p:eau-de-toilette-apres-rasage-100-ml-santal", "p:eau-de-cologne-100-ml-lavande-royale"],
    },
    {
        "slug": "choisir-son-rasoir-de-surete",
        "titre": "Choisir son rasoir de sûreté : peigne ouvert ou fermé",
        "title": "Choisir son rasoir de sûreté : peigne ouvert, fermé | Le Père Lucien",
        "desc": "Peigne fermé, peigne ouvert, papillon, shavette : les différences entre les rasoirs à lame unique et lequel choisir pour débuter.",
        "image": "lucien-cire-moustache.webp",
        "minutes": 5,
        "corps": """
<p>Tous les rasoirs de sûreté utilisent la même lame double tranchant. Ce qui change, c'est la quantité de lame exposée et la façon de la charger.</p>
<h2>Peigne fermé</h2>
<p>Une barre continue protège la peau. C'est le modèle le plus doux, idéal pour débuter, comme le [[p:rasoir-de-securite-metallique-peigne-ferme-tp-gw|rasoir à peigne fermé TP-GW]].</p>
<h2>Peigne ouvert</h2>
<p>Des dents laissent passer les poils longs. Plus efficace sur une barbe de plusieurs jours, il demande une main plus légère : [[p:rasoir-de-surete-a-peigne-ouvert-vert-tp-v|peigne ouvert TP-V]].</p>
<h2>Papillon</h2>
<p>La tête s'ouvre en tournant le manche : le changement de lame est plus rapide. Voir le [[p:rasoir-de-surete-papillon-classy-rose-gold-pap-r|papillon Classy]].</p>
<h2>Shavette et coupe-choux</h2>
<p>Une seule arête, tenue à la main : le geste du barbier. La [[c:rasage/shavettes-coupe-choux|shavette]] utilise une demi-lame jetable ; le coupe-choux s'affûte au cuir.</p>
<h2>Les lames</h2>
<p>Chaque marque coupe différemment. Testez un assortiment de [[c:rasage/lames|lames]] avant de choisir.</p>
""",
        "produits": ["p:rasoir-de-securite-metallique-peigne-ferme-tp-gw", "p:rasoir-de-surete-a-peigne-ouvert-vert-tp-v", "p:rasoir-de-surete-papillon-classy-rose-gold-pap-r", "p:lames-de-rasoir-derby-blue"],
    },
    {
        "slug": "entretenir-sa-barbe",
        "titre": "Entretenir sa barbe : laver, nourrir, discipliner",
        "title": "Entretenir sa barbe : shampoing, huile, baume | Le Père Lucien",
        "desc": "Shampoing du barbu, huile au jojoba, baume et peigne en corne : la routine d'entretien d'une barbe douce et sans démangeaisons.",
        "image": "lucien-atelier-baumes.webp",
        "minutes": 4,
        "corps": """
<p>Une barbe qui gratte est une barbe dont la peau manque de soin. La routine tient en trois gestes.</p>
<h2>Laver deux à trois fois par semaine</h2>
<p>Le [[c:barbe-moustache/shampoings|shampoing du barbu]] nettoie le poil et la peau sans les dessécher, contrairement au savon de toilette.</p>
<h2>Nourrir chaque jour</h2>
<p>Trois à cinq gouttes d'[[p:huile-du-barbu-jojoba-30ml-traditionnel|huile du barbu au jojoba]] sur barbe sèche, massées jusqu'à la peau. Les démangeaisons des premières semaines disparaissent.</p>
<h2>Discipliner</h2>
<p>Le [[c:barbe-moustache/huiles-baumes|baume à barbe]] ajoute une tenue légère. Coiffez avec un [[c:barbe-moustache/peignes-brosses|peigne en corne]] : il ne crée pas d'électricité statique. Pour la moustache, une noisette de [[c:barbe-moustache/cires-moustache|cire]].</p>
""",
        "produits": ["p:le-shampoing-du-barbu-100g-traditionnel", "p:huile-du-barbu-jojoba-30ml-traditionnel", "p:baume-barbe-nourrissant-naturel-traditionnel", "p:peigne-a-barbe-droit-en-corne-veritable-p3"],
    },
]

MARTINE = [
    {
        "slug": "utiliser-baume-solide-corps",
        "titre": "Comment utiliser un baume solide pour le corps",
        "title": "Comment utiliser un baume solide pour le corps | Mère Martine",
        "desc": "Le baume corps solide s'applique sur peau tiède, directement ou entre les mains. La méthode, zone par zone, et comment le conserver.",
        "image": "martine/baume-fondant.webp",
        "minutes": 4,
        "corps": """
<p>Un baume solide est un beurre corporel sans eau. Il ne contient pas de conservateur et dure environ deux mois. Le seul secret : la chaleur.</p>
<h2>Sur peau tiède</h2>
<p>Sortez de la douche et appliquez le baume dans les deux minutes. La peau encore chaude le fait fondre au contact : passez le galet directement sur les jambes et les bras, puis massez.</p>
<h2>Entre les mains, pour le visage et le cou</h2>
<p>Frottez le galet entre vos paumes, puis appliquez par pressions. Une petite quantité suffit.</p>
<h2>Zones très sèches</h2>
<p>Coudes, genoux, talons : appliquez le soir et laissez agir la nuit. Le [[m:baume-corps-solide-karite-cacao|baume corps solide]], le [[m:beurre-corporel-solide-mangue-coco|beurre corporel]], le [[m:galet-hydratant-corps-fleur-oranger|galet]] et le [[m:stick-hydratant-corps|stick]] s'utilisent tous ainsi. Pour une peau très sèche, combinez avec l'[[m:huile-seche-satinante-corps-cheveux|huile sèche satinante]] (voir [[ma:routine-hydratation-peau-tres-seche|notre routine hydratation]]).</p>
<h2>Après le rasage</h2>
<p>Le [[m:pain-fondant-anti-irritations|pain fondant anti-irritations]] a été formulé pour calmer la peau après le passage de la lame.</p>
<h2>Le conserver</h2>
<p>Rangez-le au sec dans son étui, loin de la douche. S'il ramollit en été, placez-le dix minutes au réfrigérateur.</p>
""",
        "produits": ["m:baume-corps-solide-karite-cacao", "m:galet-hydratant-corps-fleur-oranger", "m:stick-hydratant-corps", "m:pain-fondant-anti-irritations"],
    },
    {
        "slug": "routine-hydratation-peau-tres-seche",
        "titre": "Routine hydratation du corps pour peau très sèche",
        "title": "Routine hydratation corps, huile pour peau très sèche | Mère Martine",
        "desc": "Savon surgras, huile sur peau humide, crème le soir : une routine hydratation corps en trois gestes pour peau très sèche.",
        "image": "martine/huile-corps.webp",
        "minutes": 5,
        "corps": """
<p>Une peau très sèche perd son eau plus vite qu'elle ne la retient. L'objectif d'une routine hydratation corps : nettoyer sans décaper, puis enfermer l'eau dans la peau.</p>
<h2>1. Une douche courte et un savon surgras</h2>
<p>L'eau très chaude dissout les lipides de la peau. Préférez l'eau tiède et un savon saponifié à froid comme le [[m:savon-lait-de-chevre-bio|savon au lait de chèvre bio]].</p>
<h2>2. L'huile sur peau humide</h2>
<p>C'est le geste qui change tout. Sans vous sécher complètement, appliquez quelques gouttes d'[[m:huile-seche-satinante-corps-cheveux|huile sèche corporelle]] ou, si la peau tire beaucoup, de l'[[m:huile-nourrissante-corps-peau-tres-seche|huile nourrissante pour peau très sèche]] : l'eau restée sur la peau est retenue par le film d'huile. Une huile pour hydrater la peau ne fonctionne jamais aussi bien que sur peau mouillée.</p>
<h2>3. La crème sur les zones qui tirent</h2>
<p>Le soir, une [[m:creme-corps-velours|crème hydratante qui ne colle pas]] sur les tibias, les coudes et les mains.</p>
<h2>Une fois par semaine</h2>
<p>Un [[m:pain-fondant-anti-irritations|baume solide]] sur les zones les plus sèches, laissé toute la nuit.</p>
""",
        "produits": ["m:huile-nourrissante-corps-peau-tres-seche", "m:huile-seche-satinante-corps-cheveux", "m:creme-hydratante-naturelle-sans-parfum", "m:savon-naturel-solide-avoine-peaux-sensibles"],
    },
    {
        "slug": "bienfaits-savon-lait-anesse",
        "titre": "Les bienfaits du savon au lait d'ânesse",
        "title": "Bienfaits du savon au lait d'ânesse bio | Mère Martine",
        "desc": "Pourquoi le lait d'ânesse et le lait de chèvre conviennent aux peaux sensibles, au visage et aux peaux à imperfections.",
        "image": "martine/savon-chevre.webp",
        "minutes": 4,
        "corps": """
<p>Dans un savon au lait, le lait remplace une partie de l'eau de la recette. Il apporte des lipides, des protéines et des sucres qui rendent la mousse plus crémeuse et plus douce.</p>
<h2>Le lait d'ânesse</h2>
<p>Riche en vitamines et en acides gras, il est connu depuis l'Antiquité pour adoucir la peau. Notre [[m:savon-lait-d-anesse-bio|savon au lait d'ânesse bio]] est fabriqué avec le lait de l'Asinerie de la Vioune, dans le Bourbonnais.</p>
<h2>Le lait de chèvre</h2>
<p>Son pH est proche de celui de la peau. Un [[m:savon-lait-de-chevre-bio|savon au lait de chèvre]] convient au visage, y compris aux peaux à imperfections qui réagissent mal aux nettoyants détergents.</p>
<h2>Pour les peaux sensibles</h2>
<p>La saponification à froid garde la glycérine naturelle, et le surgraissage à 6 % laisse des huiles non saponifiées sur la peau. C'est ce qui fait d'un savon naturel solide un bon choix pour les peaux sensibles. Le [[m:savon-naturel-solide-avoine-peaux-sensibles|savon à l'avoine, sans parfum]], est le plus doux.</p>
<p>Après la douche, terminez par une [[m:creme-corps-velours|crème corps]] ou une [[m:huile-seche-satinante-corps-cheveux|huile sèche]].</p>
""",
        "produits": ["m:savon-lait-d-anesse-bio", "m:savon-lait-de-chevre-bio", "m:savon-naturel-solide-avoine-peaux-sensibles", "p:savon-du-barbier-le-pere-lucien-lainess-200-g-bandi"],
    },
    {
        "slug": "eviter-irritations-rasage-femme",
        "titre": "Rasage féminin : éviter les irritations et les poils incarnés",
        "title": "Éviter les irritations du rasage, peaux sensibles femme | Mère Martine",
        "desc": "Préparer la peau, choisir une mousse dense, raser dans le bon sens et apaiser : la méthode pour un rasage féminin sans irritation.",
        "image": "martine/huile-rasage.webp",
        "minutes": 5,
        "corps": """
<p>Le feu du rasoir vient de trois causes : une peau mal préparée, une lame qui accroche et trop de passages. On les corrige une par une.</p>
<h2>Préparer</h2>
<p>Rasez-vous en fin de douche, peau chaude. Appliquez trois gouttes d'[[m:huile-pre-post-rasage-apaisante|huile pré-rasage]] : elle assouplit le poil et forme un film protecteur.</p>
<h2>Une mousse dense, pas un gel</h2>
<p>Le [[m:pain-de-rasage-ultra-moussant|pain de rasage]] ou la [[m:creme-a-raser-moussante-femme|crème à raser moussante]] donnent une mousse épaisse qui amortit la lame. Pour les peaux très sensibles, le [[m:gel-de-rasage-peaux-sensibles|gel aloe et lin]], sans savon.</p>
<h2>Une seule lame, dans le sens du poil</h2>
<p>Les rasoirs à cinq lames repassent cinq fois sur la même zone. Un [[m:rasoir-surete-femme-laiton|rasoir de sûreté]] coupe en un passage. Lire [[ma:pourquoi-rasoir-de-surete-femme|pourquoi passer au rasoir de sûreté]].</p>
<h2>Apaiser</h2>
<p>Rincez à l'eau froide, vaporisez la [[m:soin-apres-rasage-apaisant|lotion apaisante]], puis l'huile post-rasage ou le [[m:pain-fondant-anti-irritations|pain fondant anti-irritations]].</p>
<h2>Les poils incarnés</h2>
<p>Massez l'huile chaque soir, même sans vous raser. Un gant de crin une fois par semaine libère les poils coincés.</p>
""",
        "produits": ["m:huile-pre-post-rasage-apaisante", "m:pain-de-rasage-ultra-moussant", "m:rasoir-surete-femme-laiton", "m:pain-fondant-anti-irritations"],
    },
    {
        "slug": "pourquoi-rasoir-de-surete-femme",
        "titre": "Pourquoi passer au rasoir de sûreté quand on est une femme",
        "title": "Pourquoi passer au rasoir de sûreté femme | Mère Martine",
        "desc": "Moins d'irritations, zéro cartouche jetable, une lame à 30 centimes : les raisons de passer au rasoir de sûreté femme réutilisable.",
        "image": "martine/rasoir-laiton.webp",
        "minutes": 4,
        "corps": """
<p>Le rasoir de sûreté a été le rasoir de nos grands-mères avant l'arrivée des cartouches multi-lames. Il revient pour trois raisons.</p>
<h2>Moins d'irritations</h2>
<p>Une lame unique coupe le poil à ras en un passage. Les rasoirs multi-lames soulèvent puis coupent le poil sous la surface de la peau : c'est l'origine de nombreux poils incarnés.</p>
<h2>Un rasoir réutilisable</h2>
<p>Le [[m:rasoir-surete-femme-laiton|rasoir de sûreté femme en laiton]] dure des décennies. Seule la lame se change, et elle se recycle avec les métaux.</p>
<h2>Une économie réelle</h2>
<p>Une lame coûte environ 30 centimes et sert cinq à sept fois. Voir [[p:lames-de-rasoir-derby-blue|les lames Derby]] chez Le Père Lucien.</p>
<h2>Comment débuter</h2>
<p>Commencez par les jambes, sans appuyer, rasoir incliné à 30 degrés. Les aisselles viendront après quelques semaines. Pour la mousse, un [[m:pain-de-rasage-ultra-moussant|pain de rasage]] et, si vous voulez, notre [[m:bol-de-rasage-femme-gres|bol de rasage en grès rose]].</p>
<p>Le [[m:coffret-rasage-douceur|coffret rasage douceur]] réunit tout le nécessaire.</p>
""",
        "produits": ["m:rasoir-surete-femme-laiton", "m:coffret-rasage-douceur", "m:pain-de-rasage-ultra-moussant"],
    },
    {
        "slug": "bain-huile-cheveux-secs",
        "titre": "Comment faire un bain d'huile pour cheveux secs",
        "title": "Comment faire un bain d'huile cheveux secs | Mère Martine",
        "desc": "Quelle huile, combien de temps, comment la rincer : la méthode du bain d'huile pour nourrir les cheveux secs et les pointes abîmées.",
        "image": "martine/shampoing.webp",
        "minutes": 4,
        "corps": """
<p>Un bain d'huile nourrit la fibre en profondeur avant le shampoing. Une fois par semaine, il suffit à transformer des longueurs sèches.</p>
<h2>Le dosage</h2>
<p>Une cuillère à café pour des cheveux courts, deux pour des cheveux mi-longs, trois pour des cheveux longs. Le [[m:bain-huile-cheveux-secs|bain d'huile avant-shampoing]] est formulé pour cela ; l'[[m:huile-seche-satinante-corps-cheveux|huile sèche corps et cheveux]] convient aussi, plus légère.</p>
<h2>L'application</h2>
<p>Sur cheveux secs, appliquez mèche par mèche, des pointes vers la mi-longueur. Évitez les racines si votre cuir chevelu graisse vite. Brossez avec une [[m:brosse-cheveux-poils-sanglier|brosse en poils de sanglier]] pour répartir.</p>
<h2>Le temps de pose</h2>
<p>Trente minutes minimum, une nuit au maximum, cheveux enroulés dans une serviette chaude.</p>
<h2>Le rinçage</h2>
<p>Appliquez le [[m:shampoing-solide-naturel|shampoing solide]] sur cheveux secs d'abord, massez, puis mouillez. Faites un second shampoing. Les cheveux ne doivent pas rester gras.</p>
""",
        "produits": ["m:bain-huile-cheveux-secs", "m:huile-soin-cheveux-ricin-camelia", "m:shampoing-solide-naturel", "m:brosse-cheveux-poils-sanglier"],
    },
    {
        "slug": "bienfaits-brosse-poils-sanglier",
        "titre": "Brosse en poils de sanglier : bienfaits et utilisation",
        "title": "Brosse en poils de sanglier : bienfaits | Mère Martine",
        "desc": "Pourquoi la brosse en poils de sanglier nourrit et fait briller les cheveux, comment démêler des cheveux fragiles sans les casser.",
        "image": "martine/brosse.webp",
        "minutes": 4,
        "corps": """
<p>Les « cent coups de brosse » du soir n'étaient pas une coquetterie : ils répartissaient le sébum du cuir chevelu sur toute la longueur des cheveux.</p>
<h2>Ce que fait le poil de sanglier</h2>
<p>Le poil de sanglier a, comme le cheveu, une surface en écailles. Il capte le sébum aux racines et le dépose sur les longueurs : les pointes sont nourries, les écailles lissées, les cheveux brillent.</p>
<h2>Démêler sans casser</h2>
<p>Commencez toujours par les pointes, puis remontez. Le coussin pneumatique de notre [[m:brosse-cheveux-poils-sanglier|brosse à cheveux en poils de sanglier]] absorbe la pression : c'est la brosse la plus adaptée aux cheveux fragiles. Pour les cheveux épais, la [[m:brosse-sanglier-demelante-poche|brosse sanglier démêlante]] ajoute des picots souples.</p>
<h2>Espacer les lavages</h2>
<p>En répartissant le sébum, la brosse évite l'effet racines grasses et pointes sèches. Avec un [[m:shampoing-sec-poudre-saupoudreuse|shampoing sec en poudre]], on gagne deux à trois jours entre deux shampoings.</p>
<h2>L'entretien</h2>
<p>Une fois par semaine, retirez les cheveux au peigne, lavez à l'eau tiède savonneuse, poils vers le bas, et laissez sécher à plat.</p>
<p>Le Père Lucien utilise le même poil pour ses [[p:brosse-a-barbe-manche-pur-poil-de-sanglier-le-pere-lucien-brossman|brosses à barbe]].</p>
""",
        "produits": ["m:brosse-cheveux-poils-sanglier", "m:coffret-cent-coups-de-brosse", "m:shampoing-sec-poudre-saupoudreuse"],
    },
    {
        "slug": "volume-cheveux-fins",
        "titre": "Donner du volume aux cheveux fins",
        "title": "Volume cheveux fins : brushing, shampoing sec | Mère Martine",
        "desc": "Brume au lin avant le séchage, séchage tête en bas, shampoing sec aux racines : la méthode pour structurer un brushing volumineux.",
        "image": "martine/brume-lin.webp",
        "minutes": 4,
        "corps": """
<p>Les cheveux fins retombent parce qu'ils manquent de structure, pas de produit. L'erreur courante est de les alourdir avec des soins trop riches.</p>
<h2>Avant le séchage</h2>
<p>Vaporisez la [[m:brume-mise-en-plis-lin|brume de mise en plis au lin]] sur cheveux essorés. Le mucilage de lin gaine la fibre et lui donne de la mémoire de forme : elle remplace une crème volumisante brushing.</p>
<h2>Le séchage</h2>
<p>Séchez tête en bas jusqu'à 80 %, puis terminez à la brosse ronde en soulevant les racines. Enroulez les mèches du dessus sur des bigoudis pendant que vous vous préparez.</p>
<h2>Les racines</h2>
<p>Une pincée de [[m:shampoing-sec-poudre-saupoudreuse|shampoing sec]] aux racines, même sur cheveux propres, texturise et donne du corps.</p>
<h2>Pour finir</h2>
<p>Un grain de [[m:cire-coiffante-legere|cire coiffante légère]], chauffé entre les doigts, sur les pointes seulement. Ou, avant le séchage, la [[m:creme-volumisante-brushing|crème volumisante brushing]].</p>
""",
        "produits": ["m:brume-mise-en-plis-lin", "m:creme-volumisante-brushing", "m:shampoing-sec-poudre-saupoudreuse", "m:cire-coiffante-legere"],
    },
    {
        "slug": "idees-cadeaux-femme",
        "titre": "Idées cadeaux pour femme : anniversaire, fête des mères",
        "title": "Idée cadeau femme anniversaire, coffret fête des mères | Mère Martine",
        "desc": "Coffret rituel du soir, coffret cheveux, box rasage : nos idées cadeaux bien-être pour un anniversaire ou la fête des mères.",
        "image": "martine/coffret-cadeau.webp",
        "minutes": 3,
        "corps": """
<p>Un cadeau bien-être réussi s'utilise vraiment. Voici nos coffrets, selon la personne à qui vous l'offrez.</p>
<h2>Pour celle qui prend son temps le soir</h2>
<p>Le [[m:coffret-rituel-du-soir|coffret rituel du soir]] : savon au lait de chèvre, huile sèche et crème velours. Un coffret soins cocooning, notre coffret cadeau fête des mères le plus demandé.</p>
<h2>Pour celle qui soigne ses cheveux</h2>
<p>Le [[m:coffret-cent-coups-de-brosse|coffret des cent coups de brosse]] : brosse en poils de sanglier, huile, shampoing sec et pommade.</p>
<h2>Pour celle qui veut changer ses habitudes</h2>
<p>Le [[m:coffret-rasage-douceur|coffret rasage douceur]] : un rasoir de sûreté en laiton pour des années, et les soins qui vont avec. Un cadeau bien-être haut de gamme et durable.</p>
<h2>Pour celle qui aime être chouchoutée</h2>
<p>La [[m:box-bien-etre-femme|box bien-être femme]] : huile rose et camélia, beurre corporel, savon au lait d'ânesse et galet. Ou le [[m:coffret-soins-cocooning|coffret soins cocooning]] pour les soirées d'hiver, et le [[m:kit-routine-beaute-nuit|kit routine beauté nuit]] avec sa trousse.</p>
<h2>Pour celle qui aime les classiques</h2>
<p>Le [[m:coffret-cadeau-cosmetique-traditionnel|coffret cadeau cosmétique traditionnel]] réunit quatre savons de l'atelier.</p>
<h2>Un petit budget</h2>
<p>Un [[m:savon-lait-d-anesse-bio|savon au lait d'ânesse]] et une [[m:cire-coiffante-legere|cire coiffante légère]] font un joli duo pour moins de 30 €.</p>
<p>Chaque commande peut être accompagnée d'une carte écrite à la main. Voir tout le [[mc:coin-des-affaires|coin des affaires et cadeaux]].</p>
""",
        "produits": ["m:coffret-rituel-du-soir", "m:box-bien-etre-femme", "m:coffret-soins-cocooning", "m:coffret-cadeau-cosmetique-traditionnel"],
    },
]
