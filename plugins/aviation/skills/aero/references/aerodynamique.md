# Référence — Aérodynamique fondamentale

Les forces aérodynamiques et ce qui les gouverne. Formules exploitables avec de vrais nombres (unités SI sauf mention).

## Sommaire
- Portance et équation fondamentale
- Angle d'incidence / angle d'attaque
- Coefficient de portance et décrochage
- Traînée : parasite + induite, polaire
- Allongement et traînée induite
- Finesse L/D et vitesse de finesse max
- Couche limite et nombre de Reynolds
- Compressibilité et effets de Mach
- Effet de sol

## Portance et équation fondamentale

`L = ½ ρ V² S CL`

- `L` portance (N), `ρ` masse volumique de l'air (kg/m³, ≈ 1,225 au niveau de la mer ISA), `V` vitesse air vraie (m/s), `S` surface alaire de référence (m²), `CL` coefficient de portance (sans dimension).
- Le terme `½ ρ V²` est la **pression dynamique** `q`. Doubler la vitesse quadruple la portance à CL constant.
- La traînée suit la même forme : `D = ½ ρ V² S CD`.
- **Conséquence pilotage** : la portance dépend de V² *et* de CL (donc de l'incidence). À basse vitesse on maintient la portance en augmentant CL (cabrer, sortir les volets) ; à l'incidence critique, CL plafonne → décrochage.

## Angle d'incidence / angle d'attaque

**Angle d'attaque (α)** = angle entre la corde de l'aile et le **vent relatif** (la trajectoire air). C'est *lui* qui commande CL, pas l'assiette.

- Ne pas confondre avec l'**assiette** (angle par rapport à l'horizon) ni le **calage** (angle de montage de l'aile sur le fuselage, fixe). En descente rapide on peut avoir une assiette faible et une forte incidence.
- **Point-clé** : un avion décroche **toujours à la même incidence critique**, quelle que soit la vitesse, l'assiette ou le facteur de charge. D'où les décrochages « à grande vitesse » en virage serré.

## Coefficient de portance et décrochage

- `CL` croît quasi **linéairement** avec α jusqu'au décrochage. Pente typique ≈ **0,1 par degré** (≈ 2π par radian, théorie de l'aile mince) pour une aile d'allongement moyen.
- `CLmax` atteint à l'**incidence critique**, souvent **~15–16°** pour un profil classique. Au-delà, la couche limite décolle massivement, CL chute → **décrochage**.
- **Volets** (becs, fentes) augmentent CLmax et décalent la courbe : on vole plus lentement pour la même portance. **Becs de bord d'attaque** repoussent l'incidence critique.
- Vitesse de décrochage en palier : `Vs = √( 2W / (ρ S CLmax) )` (voir mécanique-du-vol pour l'usage). Plus lourd, plus haut (ρ faible), moins de volets → Vs plus élevée.

## Traînée : parasite + induite, polaire

Traînée totale = **traînée parasite** + **traînée induite**.

- **Parasite** (`CD0`) : frottement + forme + interférence. Croît avec V² → **domine à haute vitesse**.
- **Induite** : prix à payer pour créer de la portance (tourbillons de bout d'aile). `CDi = CL² / (π · AR · e)`. Comme CL est grand à basse vitesse, la traînée induite **domine à basse vitesse**.
- **Polaire de l'avion** : `CD = CD0 + CL² / (π · AR · e)`, avec `AR` allongement et `e` coefficient d'Oswald (≈ 0,7–0,85).
- La courbe de traînée totale en fonction de V a un **minimum** : c'est là que parasite = induite, à la vitesse de **finesse maximale**.
- **Courbe de puissance** (puissance requise vs V) : son minimum (vitesse de taux de chute mini / d'endurance) est **plus lent** que la vitesse de finesse max. En dessous, on est sur le **régime arrière** (« backside of the power curve ») : voler plus lentement demande *plus* de puissance — piège en approche.

## Allongement et traînée induite

`AR = b² / S` (envergure² / surface). Grand allongement (planeur, AR 20–40) → faible traînée induite → **excellente finesse**. Faible allongement (chasseur delta, AR 2–4) → forte traînée induite mais bonne tenue à grande incidence et en supersonique.

- **Conséquence sim** : un planeur plane loin (finesse 40+) parce que sa traînée induite est minuscule ; un warbird trapu paie cher chaque g en virage (traînée induite ∝ CL² ∝ n²).

## Finesse L/D et vitesse de finesse max

- **Finesse** = `L/D = CL/CD`. En vol plané non motorisé, elle donne directement la **distance parcourue par unité d'altitude perdue** : finesse 10 → 10 km parcourus pour 1 km de perte.
- Finesse max atteinte à un CL précis (donc **une vitesse précise** pour une masse donnée), là où traînée parasite = traînée induite.
- Cette vitesse de meilleur plané **augmente avec la masse** (∝ √masse) et est **indépendante du vent** (mais on l'ajuste vent de face/arrière pour maximiser la distance sol).
- Ordres de grandeur : avion léger 8–12 ; jet de ligne 15–18 ; planeur 30–50+.

## Couche limite et nombre de Reynolds

- **Couche limite** : fine pellicule d'air ralentie au contact de l'aile. Laminaire (lisse, peu traînante, fragile) puis turbulente (plus traînante mais plus résistante au décollement). Son **décollement** = décrochage.
- **Nombre de Reynolds** : `Re = ρ V L / μ = V L / ν` (`L` corde, `ν` viscosité cinématique ≈ 1,46×10⁻⁵ m²/s au niveau mer). Rapport forces d'inertie / forces visqueuses.
- Re élevé (gros avion rapide, ~10⁷) → couche limite turbulente stable, CLmax élevé. Re faible (drone, maquette, ~10⁴–10⁵) → décollement précoce, CLmax dégradé, comportement « pâteux ».
- **Conséquence** : un profil qui marche à taille réelle peut mal se comporter réduit ; pertinent pour les sims de modélisme ou de très petits appareils.

## Compressibilité et effets de Mach

- **Nombre de Mach** `M = V / a`, `a` vitesse du son (≈ 340 m/s au niveau mer, décroît avec la température en altitude, ≈ 295 m/s en haute croisière).
- Jusqu'à **M ≈ 0,3**, l'air se comporte comme incompressible. Au-delà, la compressibilité compte.
- **Mach critique (Mcrit)** : Mach de vol auquel l'écoulement atteint localement M = 1 sur l'extrados (là où l'air accélère). Au-delà : **onde de choc** locale → décollement (« tremblement »/buffet), **divergence de traînée**, perte d'efficacité des gouvernes, phénomènes de tuck.
- **Flèche** (ailes en flèche) retarde ces effets → jets rapides. Profils supercritiques idem.
- **Conséquence sim** : en piqué prolongé un chasseur d'époque peut atteindre la compressibilité, gouvernes qui durcissent et tendance à s'enfoncer — récupérer en réduisant Mach (aérofreins, réduire, laisser reprendre de la densité en altitude plus basse).

## Effet de sol

Près du sol (à moins d'~1 envergure de hauteur), les tourbillons de bout d'aile sont bridés → **traînée induite réduite**, portance effective accrue.

- Effet : l'avion **flotte** à l'arrondi, décolle « tôt » puis peine à accélérer hors de l'effet de sol, et l'assiette de tangage varie (souvent tendance à piquer/cabrer selon l'appareil).
- **Conséquence pilotage** : à l'arrondi, anticiper le flottement (réduire franchement les gaz) ; au décollage court, ne pas s'arracher du sol sous la vitesse de sécurité en comptant sur l'effet de sol.
