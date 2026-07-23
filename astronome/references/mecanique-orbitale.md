# Référence — Mécanique orbitale

Lois et critères pour juger orbites et stabilité. Ordres de grandeur ; les seuils de stabilité sont des règles empiriques.

## Sommaire
- Lois de Kepler
- Équation vis-viva & vitesses
- Excentricité
- Sphère de Hill
- Stabilité des systèmes multi-planètes
- Résonances de moyen mouvement
- Points de Lagrange
- Verrouillage de marée
- Orbites rétrogrades et inclinées

## Lois de Kepler

1. **Ellipses** : chaque planète décrit une ellipse dont l'étoile occupe un foyer.
2. **Aires égales** : le rayon vecteur balaie des aires égales en des temps égaux → la planète va **plus vite au périastre**, plus lentement à l'apoastre.
3. **Période ↔ distance** : `P² ∝ a³`. Forme pratique pour une étoile de 1 M☉ : **`P(années)² = a(UA)³`**.
   - Forme générale : `P² = 4π²a³ / [G(M+m)]` → pour une étoile de masse M☉ différente : `P(an)² = a(UA)³ / (M/M☉)`.
   - Exemples (M = 1 M☉) : a = 0,5 UA → P = 0,5^1,5 ≈ 0,35 an ; a = 4 UA → P = 8 ans.

## Équation vis-viva & vitesses

- **Orbite circulaire** : `v = √(GM/a)`. Pour le Soleil et a en UA : `v ≈ 29,8 / √a(UA)` km/s (≈ 29,8 km/s à 1 UA).
- **Orbite quelconque (vis-viva)** : `v² = GM(2/r − 1/a)` → plus rapide près du foyer.

## Excentricité

- `e = 0` : cercle. `0 < e < 1` : ellipse. `e → 1` : très allongée.
- Distances : **périastre** `a(1−e)`, **apoastre** `a(1+e)`.
- Effet climatique : une forte excentricité fait varier fortement l'éclairement sur une orbite (le flux varie comme 1/r² entre péri- et apoastre). Une planète « au climat stable » avec `e` élevé (≳ 0,3) est douteuse ; les orbites habitables tendent vers de faibles excentricités. Vérifier aussi que le **périastre** ne fait pas entrer la planète dans une zone dangereuse (trop chaud, autre corps, limite de Roche stellaire).

## Sphère de Hill

Région autour d'un corps où **sa** gravité domine celle de l'étoile — donc où une lune peut rester liée.

`r_Hill ≈ a(1−e) × (m / 3M)^(1/3)`

où m = masse de la planète, M = masse de l'étoile, a = demi-grand axe planétaire.

- Une **lune** doit orbiter **bien à l'intérieur** de la sphère de Hill : stabilité pratique jusqu'à ~**0,5 r_Hill** pour une orbite **prograde**, ~**1 r_Hill** pour une orbite **rétrograde**. Au-delà, l'étoile arrache la lune. → Une lune décrite au-delà de la sphère de Hill de sa planète est **impossible** (elle ne serait pas liée).
- Exemple : Terre (m = 3×10⁻⁶ M☉) à 1 UA → r_Hill ≈ 1 UA × (3×10⁻⁶/3)^(1/3) = 1 UA × (10⁻⁶)^(1/3) = 1 UA × 10⁻² = 0,01 UA ≈ 1,5 million de km. La Lune est à ~0,384 million de km → ~0,26 r_Hill : stable. ✔

## Stabilité des systèmes multi-planètes

- Deux planètes voisines restent stables sur le long terme si elles sont séparées d'un nombre suffisant de **rayons de Hill mutuels** : règle empirique `Δ ≳ 8–10 R_Hill,mutuel` entre orbites adjacentes (davantage pour de nombreuses planètes). Trop rapprochées → croisements d'orbites, éjections, collisions.
- Exception : un **verrouillage en résonance** peut stabiliser des planètes plus rapprochées que la règle générale (systèmes compacts type TRAPPIST-1, en chaîne de résonances).
- Signes d'incohérence : planètes aux orbites qui se croisent (sauf résonance protectrice type Neptune–Pluton), empilement de planètes massives très serrées sans résonance, orbites qui se recoupent en projection.

## Résonances de moyen mouvement

Rapports de périodes proches d'entiers simples (2:1, 3:2, 4:3…). Selon la configuration, elles **stabilisent** ou **déstabilisent** :

- **Stabilisantes** : Neptune–Pluton 3:2 (Pluton ne heurte jamais Neptune) ; **résonance de Laplace** Io:Europa:Ganymède = 4:2:1 (entretient le chauffage de marée).
- **Déstabilisantes** : lacunes de Kirkwood dans la ceinture d'astéroïdes (résonances avec Jupiter qui vident certaines orbites).

En fiction, une chaîne de résonances bien posée est un gage de crédibilité pour un système compact.

## Points de Lagrange

Cinq positions d'équilibre dans un système à deux corps (étoile + planète) :
- **L1, L2, L3** : instables (utiles pour des sondes, pas pour un corps naturel durable sans contrôle).
- **L4, L5** : **stables** si le rapport de masse est suffisant (M_primaire/M_secondaire ≳ 25). Y résident les **troyens** (astéroïdes co-orbitaux, ex. troyens de Jupiter). Une planète/lune « troyenne » à 60° d'une autre est plausible si le rapport de masse le permet.

## Verrouillage de marée

Le corps finit par présenter **toujours la même face** à l'objet dominant (comme la Lune vers la Terre).

- Le temps de verrouillage **croît très fortement avec la distance** (grossièrement `∝ a⁶`) : les corps **proches** se verrouillent vite, les lointains lentement, voire jamais.
- Conséquences : autour d'une **étoile peu lumineuse** (K, M), la zone habitable est si proche que les planètes s'y verrouillent → pas de cycle jour/nuit classique, un hémisphère « jour » permanent et un « nuit ». Incohérence fréquente : décrire un cycle jour/nuit normal sur une planète qui devrait être verrouillée.
- Une atmosphère/océan épais peut **redistribuer la chaleur** entre les deux faces et rendre l'habitabilité possible malgré le verrouillage (voir `habitabilite.md`).

## Orbites rétrogrades et inclinées

- La plupart des corps formés dans un même disque orbitent dans le **même sens** et à peu près dans le **même plan** (faible inclinaison, prograde).
- Une orbite **rétrograde** ou **très inclinée** signale presque toujours une **capture** (ex. Triton autour de Neptune) ou une perturbation violente — il faut alors une histoire pour la justifier, et ces orbites sont souvent **moins stables** dans la durée.
- **Kozai–Lidov** : dans un système hiérarchique incliné (ex. planète + compagnon lointain incliné), l'excentricité et l'inclinaison peuvent osciller fortement → déstabilisation possible. À garder en tête pour un corps très incliné avec un compagnon lointain.
