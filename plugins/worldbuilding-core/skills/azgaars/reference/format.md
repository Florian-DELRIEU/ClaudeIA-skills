# Format .map — Azgaar's Fantasy Map Generator (référence détaillée)

Vérifié empiriquement sur deux versions réelles : **v1.108.12** (39 blocs) et **v1.134.0** (46 blocs). L'ordre des blocs est stable ; deux dispositions coexistent selon la version. Sources : fichiers réels + wiki officiel (Data model).

## Deux dispositions de blocs

| Version FMG | Nb blocs | Différence |
|---|---|---|
| v1.9x → v1.11x | **39** | pas de module économie ; `zones` au bloc 38 |
| v1.13x+ | **46** | ajout du **module Économie** (rebels, ice, goods, markets, trades + 2 tableaux de cellules) ; `zones` décalé au bloc 45 |

**Les blocs 0-37 sont identiques entre les deux dispositions.** La lib détecte la disposition d'après le nombre de blocs (`AzgaarMap.n_blocks`, `.has_economy`). Quelques champs se sont enrichis en v1.13x+ sans changer d'index : `features[]` gagne `shoreline`/`height`, `states[]` gagne `salesTax`/`pollTax`/`treasury`.

## Structure globale

- Fichier **texte UTF-8**, sans BOM.
- Blocs séparés par `\r\n` (CRLF).
- ⚠️ Le bloc SVG (index 5) contient des `\n` (LF) en interne. **Toujours splitter sur `\r\n` exactement**, jamais sur `\n` seul, et jamais ouvrir en mode texte Python par défaut (universal newlines détruit la distinction) → lire en binaire puis `.decode('utf-8')`.
- Les blocs JSON sont écrits par `JSON.stringify` : **compact, sans espaces** (`separators=(",", ":")` en Python, `ensure_ascii=False`).
- Un bloc JSON peut être **vide** (`""`) si la carte n'a pas l'entité (ex. aucune zone custom) → traiter comme liste vide.
- FMG charge le fichier par index de bloc : **ne jamais ajouter/supprimer un bloc**, ne jamais changer leur ordre.

## Table des blocs 0-37 (communs aux deux formats)

| # | Nom | Type | Contenu |
|---|-----|------|---------|
| 0 | params | `\|` | `version\|tip\|date\|seed\|graphWidth\|graphHeight\|mapId` |
| 1 | settings | `\|` + JSON | voir détail ci-dessous |
| 2 | mapCoordinates | JSON | `{latT, latN, latS, lonT, lonW, lonE}` |
| 3 | biomesData | `\|` | `couleurs(,)\|habitabilité(,)\|noms(,)` |
| 4 | notes | JSON | `[{id, name, legend(html)}]` — fiches régiments (`regiment{état}-{i}`), marqueurs (`marker{i}`), burgs (`burg{i}`)... |
| 5 | svg | SVG | rendu complet : labels, blasons, reliefs, styles. Multi-lignes LF |
| 6 | grid | JSON | `{spacing, cellsX, cellsY, boundary[[x,y]], points[[x,y]], features[]}` |
| 7 | grid.cells.h | CSV int | altitude 0-100 (`>=20` = terre) |
| 8 | grid.cells.prec | CSV int | précipitations |
| 9 | grid.cells.f | CSV int | id de feature |
| 10 | grid.cells.t | CSV int | distance field : `1,2..` terre, `-1,-2..` mer, `0` non marqué |
| 11 | grid.cells.temp | CSV int | température (°C) |
| 12 | pack.features | JSON | `[0, {i, type: ocean/island/lake, group, land, border, cells, firstCell, vertices[], area, name?}]` |
| 13 | cultures | JSON | élément 0 = Wildlands |
| 14 | states | JSON | élément 0 = Neutrals ; contient `military[]`, `diplomacy[]`, `campaigns[]` |
| 15 | burgs | JSON | élément 0 = `{}` |
| 16 | pack.cells.biome | CSV int | id de biome par cellule |
| 17 | pack.cells.burg | CSV int | id de burg par cellule |
| 18 | pack.cells.conf | CSV int | flux aux confluences |
| 19 | pack.cells.culture | CSV int | id de culture par cellule |
| 20 | pack.cells.fl | CSV int | flux d'eau |
| 21 | pack.cells.pop | CSV float | population rurale (points de population) |
| 22 | pack.cells.r | CSV int | id de rivière par cellule |
| 23 | (obsolète) | vide | ancien `cells.road` |
| 24 | pack.cells.s | CSV int | score de cellule (placement des burgs) |
| 25 | pack.cells.state | CSV int | id d'état par cellule |
| 26 | pack.cells.religion | CSV int | id de religion par cellule |
| 27 | pack.cells.province | CSV int | id de province par cellule |
| 28 | (obsolète) | vide | ancien `cells.crossroad` |
| 29 | religions | JSON | élément 0 = No religion |
| 30 | provinces | JSON | élément 0 = `0` |
| 31 | namesData | `\|` `/` | bases de noms : `nom\|min\|max\|dupl\|mult\|` séparées par `/` (la liste `b` des noms d'entraînement n'est pas sauvegardée) |
| 32 | rivers | JSON | `i` ≠ index du tableau |
| 33 | rulers | texte | `Ruler: x,y x,y; Ruler: ...` (outils de mesure) |
| 34 | fonts | JSON | `[{family, src?, unicodeRange?}]` |
| 35 | markers | JSON | `i` ≠ index ; note liée = `marker{i}` |
| 36 | pack.cells.routes | JSON | `{cellId: {voisinId: routeId, ...}}` |
| 37 | routes | JSON | `[{i, group: roads/trails/searoutes, feature, points[[x,y,cellId]]}]` |

### Queue format 39 blocs (v1.9x–1.11x)

| # | Nom | Type | Contenu |
|---|-----|------|---------|
| 38 | zones | JSON | `[{i, name, type, color, cells[]}]` — inclut les ressources custom |

### Queue format 46 blocs (v1.13x+, module Économie)

| # | Nom | Type | Contenu |
|---|-----|------|---------|
| 38 | rebels | JSON | soulèvements/prosélytisme : `[{i, name, type: Rebels/Proselytism, cells[], color}]` |
| 39 | ice | JSON | glaciers/icebergs : `[{i, points[[x,y]], type: glacier/iceberg}]` |
| 40 | cells_resource | CSV int | ⚠️ **déduit, non confirmé via code source** : probable id de ressource visible par cellule (réf. `goods`), très majoritairement 0 |
| 41 | goods | JSON | biens économiques : `[{i, name, tags[], icon, color, value, chance, distribution, unit, demandCoverage, multipliers, biomeOutput, visible}]` |
| 42 | markets | JSON | marchés par burg : `[{i, centerBurgId, color, goods:{goodId:{stock, price}}}]` |
| 43 | trades | JSON | transactions : `[{i, seller, sellerType, buyer, buyerType, good, units, price, tax}]` — **peut être très volumineux** (des milliers d'entrées) |
| 44 | cells_econ | CSV int | ⚠️ **déduit, non confirmé** : champ par cellule lié à l'économie/production (catégories ~0-17) |
| 45 | zones | JSON | `[{i, name, type, color, cells[]}]` — **décalé de 38 → 45** |

> ⚠️ Les blocs **40 et 44** sont des tableaux de cellules dont le rôle exact n'a pas été confirmé via le code source de FMG (déductions par élimination). Ils sont préservés à l'octet en round-trip, mais **ne pas les éditer** sans validation empirique préalable. Tous les autres blocs 46-format sont confirmés par lecture directe du fichier Comia (v1.134.0).

## Bloc 1 (settings) en détail

Format : `champs "|" ... | optionsJSON | mapName | hideLabels | stylePreset | rescaleLabels | ...`

⚠️ Le JSON d'options est au milieu et **peut contenir des `|` dans ses strings** : parser par équilibrage d'accolades, pas par split naïf.

Champs de tête (index) :
- 0 `distanceUnit` (km), 1 `distanceScale` (km/px), 2 `areaUnit`, 3 `heightUnit`, 4 `heightExponent`, 5 `temperatureScale`
- 6–11 : options de la barre d'échelle (souvent vides)
- 12 `populationRate` — **1 point de population = populationRate habitants**
- 13 `urbanization`, 14 `mapSizeOutput`, 15 `latitudeOutput`, 16–19 : divers/réservés

Options JSON notables : `year`, `era`, `eraShort`, `military[]` (types d'unités : name, icon, rural, urban, crew, power, type, separate), `winds[]`, `temperatureEquator/NorthPole/SouthPole`, `villageMaxPopulation`, `stateLabelsMode`.

Queue après le JSON : `mapName | hideLabels(0/1) | stylePreset | rescaleLabels(0/1) | ...` (champs suivants variables selon version — ne pas modifier à l'aveugle).

## Population

`habitants = points × populationRate` (champ 12 des settings).
- Burg : `burg.population` (points).
- État/culture/religion/province : `urban` + `rural` (points).
- `pack.cells.pop` : population rurale par cellule.

## Régiments (military)

Dans `states[i].military[]` : `{i, a(effectif total), cell, x, y, bx, by, u:{typeUnité: nombre}, n(0/1 unité navale/séparée), name, state, icon}`.
La fiche descriptive est dans `notes` avec `id = "regiment{stateId}-{regimentId}"`.

⚠️ **CORRECTIF (découvert empiriquement, ex-erreur de cette doc)** : contrairement à ce qu'on pourrait croire, les régiments **ne sont PAS redessinés depuis les données au chargement**. FMG bake un rendu figé dans `<g id="army{stateId}"><g id="regiment{s}-{i}">...<text>{effectif}</text>...</g></g>` au moment de la sauvegarde. Éditer `states[i].military` en JSON seul laisse ce cache SVG obsolète : l'éditeur de régiment dans FMG (qui lit les données en direct) affichera la bonne composition, **mais la boîte visible sur la carte gardera l'ancien nom et l'ancien effectif affiché**, incohérents entre eux. Symptôme observé : des régiments au JSON identique affichant des nombres différents sur la carte (résidus de l'ancienne armée, positionnés différemment). **`set_state_military()` purge automatiquement le cache via `clear_army_svg()`** — toujours passer par cette méthode plutôt que d'assigner `state["military"]` directement.

**Invariants à respecter** (vérifiés par `set_state_military`) :
- `i` == index dans le tableau `military` ; `state` == id de l'état
- `a` == somme des valeurs de `u`
- chaque clé de `u` doit exister dans `options.military[].name`
- `n = 1` pour les unités navales/séparées (`separate` du type)

### Types d'unités (`options.military`)

Chaque type : `{icon, name, rural, urban, crew, power, type, separate}`.
- `rural`/`urban` : taux de recrutement par population (utilisés si l'on régénère dans FMG)
- `crew` : personnel par unité ; `power` : valeur de combat
- `type` : `melee`, `ranged`, `mounted`, `machinery`, `armored`, `aviation`, `naval`, `magical`
- `separate = 1` : forme ses propres régiments (flottes, aviation)
- `icon` : émoji court OU image en data-URI base64 (peut faire des dizaines de Ko — ne jamais afficher brut). Remplacer les types via `set_military_types()` (édition chirurgicale du bloc settings).

## ⚠️ Piège : surrogates UTF-16 isolés dans les notes

Certaines cartes contiennent des notes avec des caractères volontairement corrompus (ex. inscriptions antiques intraduisibles), stockés dans le JSON sous forme d'échappements `\udcXX` **sans moitié haute de paire**. `json.loads` les matérialise en codepoints isolés que Python **ne peut pas ré-encoder en UTF-8** (crash à la sauvegarde). `dumps_fmg()` gère ce cas en ré-échappant tout surrogate isolé en `\uXXXX`, à l'identique du fichier source. **Toujours sérialiser les blocs JSON via `dumps_fmg`, jamais via `json.dumps` directement.**

## Couche d'interprétation stratégique

Au-delà de la lecture brute des blocs, `AzgaarMap` expose une couche qui **interprète**
les données pour les skills qui en ont besoin (au premier chef `/gm-worlds`, mais
utilisable par tout autre skill) — puissance militaire, posture diplomatique, biomes
dominants d'un territoire, etc. Objectif : un seul endroit qui sait *lire* un `.map`
en profondeur, pour que les skills consommateurs n'aient pas à réimplémenter leur
propre interprétation (et risquer de diverger sur des formules subtilement
différentes).

| Méthode | Renvoie |
|---|---|
| `m.active_states()` | États actifs (hors Neutrals/supprimés) |
| `m.unit_powers()` | `{nom_type: valeur_de_combat}` d'après `options.military` |
| `m.state_power(state, powers=None)` | Puissance militaire totale d'un état (Σ count×power) |
| `m.state_effectif(state)` | Effectif total (personnel), tous régiments |
| `m.state_provinces(state)` | Ids des provinces actives d'un état |
| `m.dominant_biomes(state, top=3)` | `[{"biome": nom, "cellules": n, "part": fraction}]`, triés décroissant |
| `m.dominant_cultures(state, top=3)` | Idem pour les cultures — `part` du 1er élément proche de 1 = territoire homogène, plusieurs parts comparables = tension culturelle latente |
| `m.dominant_religions(state, top=3)` | Idem pour les religions |
| `m.biomes_names()` | Noms de biomes dans l'ordre de leurs ids (bloc `biomesData`) |
| `m.approx_relief(state)` | ⚠️ Approximation (voir plus bas) : altitude/précipitations/température moyennes échantillonnées aux villes de l'état |
| `m.market_value_by_state()` | Valeur économique par état (stock×valeur des marchés, cartes 46 blocs) |
| `m.good_stock_by_state()` | `{stateId: {goodId: stock total}}` — base pour détecter raretés/abondances relatives (cartes 46 blocs) |
| `m.trade_flows_by_state()` | `{"i-j": valeur échangée}` — agrège les VRAIES transactions du bloc `trades` entre états (cartes 46 blocs, pas une estimation) |
| `m.diplomacy_matrix()` | `{"i-j": statut}` (i<j), lu directement dans `states[].diplomacy` |
| `m.current_wars()` | `[(i, j), ...]` paires en guerre (statut `Enemy` dans un sens ou l'autre) |
| `m.aggression_of(state)` | Posture agressive synthétique 0,1-1,6 (expansionism/alert/type) |
| `m.stability_of(state, at_war=False)` | Stabilité synthétique 0,05-1,0 (alerte + guerre) |
| `m.strategic_snapshot()` | Photographie complète : assemble tout ce qui précède, par état, plus guerres et diplomatie globales |

### Pourquoi il n'y a pas de vrai relief par état

`m.approx_relief()` est explicitement une approximation, pas une couverture du
territoire. Raison structurelle vérifiée empiriquement : le fichier `.map` contient
deux maillages distincts sans correspondance stockée entre eux.

- La **grille** (`grid`, blocs `grid_h`/`grid_prec`/`grid_f`/`grid_t`/`grid_temp`) a
  des coordonnées (`grid.points`) et porte l'altitude/précipitations/température —
  mais c'est une grille régulière brute (~50 000 cellules sur une carte de taille
  moyenne), pas la carte politique.
- Le maillage **pack** (`cells_state`, `cells_biome`, `cells_culture`...) est
  beaucoup plus grossier (souvent ~4x moins de cellules), recalculé par
  retriangulation à partir de la grille — mais ses cellules n'ont **ni coordonnées
  stockées, ni index vers leur cellule de grille parente** dans le fichier.

Reconstruire cette correspondance exigerait de ré-implémenter l'algorithme de
retriangulation Delaunay/Voronoi interne de FMG — trop fragile pour la fiabilité
recherchée. `approx_relief()` contourne le problème en cherchant, pour chaque burg
de l'état, le point de grille le plus proche (plus proche voisin, vectorisé numpy,
mis en cache par carte) — un indice basé sur les zones habitées, pas une carte du
relief complet d'un grand état sauvage.

Toutes ces méthodes sont des **lectures pures** (aucune écriture), et **stateless** :
`aggression_of`/`stability_of` ne mémorisent rien d'un appel à l'autre — elles
dérivent uniquement des champs natifs présents dans le fichier au moment de l'appel.
C'est un choix délibéré : la source de vérité reste toujours le `.map` tel qu'il est,
jamais une mémoire cachée qui pourrait diverger de ce que l'utilisateur y a
réellement mis.

`approx_relief()` importe `numpy` localement (pas de dépendance au niveau du
module) ; disponible dans l'environnement d'exécution standard des skills.

## Diplomatie

`states[i].diplomacy` : tableau de statuts vis-à-vis de chaque état (`Ally`, `Friendly`, `Neutral`, `Suspicion`, `Enemy`, `Rival`, `Vassal`, `Suzerain`, `Unknown`, `x` pour soi-même). Élément 0 (Neutrals) : `diplomacy` contient l'historique des guerres (`string[][]`).

## Ce qui est rendu depuis le SVG vs depuis les données

Au chargement, FMG **réutilise le SVG sauvegardé** pour la plupart des couches. Conséquences pour l'édition :

| Édition | Données suffisent ? |
|---|---|
| Renommer burg/état/province/culture/religion | ⚠️ Non — le label est dans le SVG (`<text id="burgLabel{i}">`, `<text id="stateLabel{i}">`, parfois `<textPath>/<tspan>`). Patcher les deux (cf. `sync_svg_label`) |
| Régiments (`states[i].military`) | ⚠️ **Non** — boîte figée dans `<g id="army{s}">`. Utiliser `set_state_military()` (purge auto via `clear_army_svg()`), jamais une assignation directe |
| Population, diplomatie, notes (hors régiments) | ✅ Oui |
| Couleur d'état/culture/religion | ⚠️ Les polygones remplis sont dans le SVG (`<g id="statesBody">` etc.) — modifier la donnée ET les `fill` correspondants, ou laisser l'utilisateur re-render dans FMG |
| Déplacer/ajouter burg | ⚠️ Icône + label + ancrage dans SVG ; complexe. Préférer l'édition dans FMG |
| Ajouter marqueur | ✅ Données (markers + note) ; FMG redessine les marqueurs au chargement |
| Cellules (state/culture/biome par cellule) | ⚠️ Les frontières/remplissages sont pré-rendus dans le SVG |

Après avoir vidé un groupe `army{s}` (boîtes manquantes tant que FMG n'a pas redessiné), le layer Military doit se régénérer à l'affichage/interaction dans FMG. Si les boîtes n'apparaissent pas spontanément après chargement, utiliser le bouton de recalcul du panneau Military **avec précaution : cela régénère aussi la composition depuis la population, écrasant potentiellement une composition custom** — préférer d'abord un simple toggle du layer (`M`) ou un pan/zoom.

Règle d'or : après toute édition, **recharger le fichier dans FMG et vérifier visuellement**. En cas de doute sur un rendu, se limiter aux éditions "données pures" (diplomatie, populations, options, année/ère, notes hors régiments).

## Validation minimale avant sauvegarde

1. Toujours 39 blocs, séparés par `\r\n`.
2. Chaque bloc JSON re-parse sans erreur.
3. Les tableaux indexés (cultures, states, burgs, religions, provinces) gardent `i == index` et leurs éléments 0 réservés ; suppression = ajouter `"removed": true`, jamais retirer l'élément.
4. Les tableaux de cellules (blocs 16–27) gardent exactement le même nombre de valeurs.
5. Test ultime : rechargement dans azgaar.github.io/Fantasy-Map-Generator.
