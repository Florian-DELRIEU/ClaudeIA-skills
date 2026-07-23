# Référence — Commandes et pilotage

Les gouvernes, leurs effets, les phases de vol et les situations particulières. Toujours relier la technique à la cause physique (voir les autres fichiers).

## Sommaire
- Gouvernes et effets primaires/secondaires
- Lacet inverse et vol coordonné
- Trims
- Dispositifs hypersustentateurs et aérofreins
- Phases de vol
- Décrochage et récupération
- Vrille et récupération (PARE)
- Vent de travers
- Gestion trajectoire/énergie en approche

## Gouvernes et effets primaires/secondaires

- **Ailerons** (manche gauche/droite) : effet primaire **roulis**. Effet secondaire : **lacet inverse** (voir plus bas).
- **Profondeur** (manche avant/arrière) : effet primaire **tangage** (via l'incidence → la portance → la trajectoire et la vitesse). Le manche « commande l'incidence », donc à puissance donnée, **la vitesse**.
- **Direction** (palonnier) : effet primaire **lacet**. Effet secondaire : **roulis** (le lacet crée un dérapage qui, par le dièdre, incline). Réciproquement, la direction sert surtout à **coordonner** et contrer le lacet, pas à tourner.
- Idée fausse : « on tourne au palonnier » → non, on tourne en **inclinant** (ailerons) ; le palonnier **coordonne**.

## Lacet inverse et vol coordonné

Quand on braque les ailerons pour incliner, l'aileron **abaissé** (aile qui monte) crée **plus de traînée** que l'aileron levé → un **lacet vers l'extérieur du virage** (lacet inverse), qui freine l'entrée en virage et déséquilibre.

- Parade : **conjuguer le pied** dans le sens du virage à l'entrée (aileron + direction ensemble) → **virage coordonné** (bille au centre). Atténué sur les avions à ailerons différentiels ou couplés.
- **Conséquence sim** : bille qui part à l'entrée de virage, avion qui « glisse » → manque de pied conjugué. Un vol non coordonné dégrade les performances et peut amorcer une vrille au décrochage.

## Trims

Le **trim** (compensateur) annule l'effort permanent sur une gouverne pour une configuration donnée.

- Trim de **profondeur** = régler une **assiette / une vitesse** : bien trimé, l'avion tient sa vitesse mains libres (retour naturel via la stabilité). Le trim ne change pas la vitesse d'équilibre à puissance donnée — il supprime juste l'effort pour la tenir.
- **Conséquence sim** : re-trimer à **chaque** changement de configuration/puissance (volets, train, gaz). Un avion mal trimé fatigue et masque les vraies tendances.

## Dispositifs hypersustentateurs et aérofreins

- **Volets (flaps)** : augmentent **CLmax** (et souvent la cambrure) → **vole plus lentement** (Vs plus basse), pente d'approche plus forte. Aussi **plus de traînée** (surtout aux grands braquages) → utile pour descendre et ralentir. Sortir par paliers sous **Vfe**.
- **Becs (slats)** : repoussent l'**incidence critique** → décrochage plus tardif, précieux à basse vitesse/forte incidence.
- **Aérofreins / spoilers** : **détruisent la portance** et/ou ajoutent de la **traînée** → descendre vite sans accélérer, « casser » la portance à l'arrondi (destructeurs de portance), freiner au sol.
- **Conséquence sim** : gérer la traînée est un outil de trajectoire à part entière — volets/aérofreins pour tenir une pente d'approche raide sans survitesse.

## Phases de vol

- **Roulage** : direction au sol (palonnier/roulette), gaz doux, anticiper les tendances moteur.
- **Décollage** : plein petit pas (hélice CS), monter la puissance **progressivement** (warbirds), tenir l'axe au **pied** (tendances moteur, voir hélices-pales), rotation à **Vr**, puis monter à **Vx** (obstacle) ou **Vy**.
- **Montée** : Vy en général ; re-trimer ; surveiller température moteur.
- **Croisière** : réduire (grand pas + admission de croisière), trimer, gérer la richesse/altitude.
- **Descente** : réduire l'admission avant le régime ; gérer la vitesse à l'assiette + aérofreins/volets.
- **Approche** : configuration (volets/train), **vitesse stabilisée** ~1,3 Vso (Vref), pente et vitesse tenues (voir énergie ci-dessous).
- **Arrondi (flare)** : réduire les gaz, **casser la descente** en cabrant progressivement pour toucher **train principal d'abord**, à vitesse minimale, en gérant le **flottement** (effet de sol). Trop haut → chute dure ; trop tôt/fort → remise de gaz de rebond.
- **Roulement** : maintenir l'axe, freinage progressif, (reverse si dispo).

## Décrochage et récupération

Le décrochage survient à l'**incidence critique**, pas à une vitesse fixe (voir aérodynamique). Signes : mou aux commandes, avertisseur, tremblement, enfoncement.

- **Récupération** : **réduire l'incidence** — pousser franchement sur le manche pour décoller l'incidence sous le critique (geste primordial), **plein régime** (petit pas), **ailes à plat** au besoin, **coordonné au pied** pour ne pas partir en vrille. Puis reprendre le vol en douceur sans re-décrocher.
- Erreur classique : tenter de rattraper au **moteur seul** en gardant l'assiette cabrée → on reste décroché. C'est l'**incidence** qui prime.
- **Décrochage dissymétrique** (une aile décroche avant l'autre, souvent en virage non coordonné) → départ en roulis/vrille : d'où l'importance de la **coordination** à basse vitesse.

## Vrille et récupération (PARE)

La **vrille (spin)** = autorotation, une aile plus décrochée que l'autre, l'avion descend en tournant, incidence très élevée. Différent d'une spirale (là, l'aile vole encore et la vitesse monte — voir stabilité).

- Récupération standard **PARE** : **P**uissance réduite (ralenti) ; **A**ilerons neutres ; **R**udder (direction) **à fond à l'opposé** de la rotation ; **E**levator (profondeur) **vers l'avant** pour casser l'incidence. Dès l'arrêt de la rotation : neutraliser la direction et **ressource en douceur** (sans re-décrocher ni survitesse).
- **Attention** : la procédure exacte dépend de l'appareil — se référer au comportement modélisé du sim ; certains avions se récupèrent seuls en lâchant tout, d'autres non.

## Vent de travers

Deux techniques pour rester dans l'axe piste malgré le vent latéral :

- **Crabe** : le nez pointe **dans le vent** d'un angle qui compense la dérive → la trajectoire reste dans l'axe, mais l'avion n'est pas aligné avec la piste. À l'arrondi, **décraber** (pied pour aligner le nez) juste avant de toucher.
- **Aile basse (glissade)** : incliner **dans le vent** (aileron) pour contrer la dérive et **pied opposé** (direction) pour aligner le nez → l'avion est aligné en permanence, on touche du train principal **côté au vent d'abord**. Technique classique pour toucher aligné.
- **Conséquence sim** : composante de vent traversier au-delà de la limite de l'appareil → décollage/atterrissage périlleux ; anticiper au pied et à l'aileron, corriger tôt.

## Gestion trajectoire/énergie en approche

Deux paramètres à tenir ensemble : la **pente/trajectoire** (où on va) et la **vitesse** (l'énergie cinétique).

- Technique usuelle **régime normal (front side)** : **manche pour la vitesse** (assiette), **gaz pour la trajectoire/altitude** (le taux de descente/plan). C'est la coordination d'approche stabilisée classique.
- Sur le **régime arrière** (backside, très basse vitesse, sous la vitesse de finesse) : la logique **s'inverse** (plus lent = plus de puissance requise) → approche de brousse/porte-avions gérée différemment, à la puissance.
- **Approche stabilisée** = configuration figée, vitesse Vref tenue, pente constante, gaz stabilisés, alignée : si l'un dérive (trop haut/vite), corriger tôt ou **remettre les gaz** plutôt que forcer un rattrapage. Un avion « rapide et haut » à courte finale ne se rattrape pas en piquant sans survitesse.
