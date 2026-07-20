# Planets Nomenclature — V3

> Système de classification planétaire modulaire, inspiré du système spectral Morgan-Keenan.
> Refonte complète du V2 : les axes sont désormais **orthogonaux** (chaque position code une seule chose), et les cumuls sont autorisés.

---

## 1. Principe général

Format complet : **`LETTRE` `degré` `.` `ROMAIN` `.` `XX` `.` `XX` …**

```
        M   1  .  III  .  05  .  14
        │   │      │       │     │
        │   │      │       │     └─ modificateur : biosphère terrestre
        │   │      │       └─────── modificateur : atmosphère respirable
        │   │      └─────────────── sous-type : jungle / tropicale
        │   └────────────────────── degré d'exposition : survie à l'air libre
        └────────────────────────── nature physique : tellurique mature
```

Quatre étages, quatre questions :

| Étage | Position | Question | Nature |
|---|---|---|---|
| **1** | `LETTRE` | *C'est quoi ?* | Nature physique — **un seul axe, exclusif** |
| **2** | `degré` (1–4) | *J'y survis comment ?* | Exposition chronique — **échelle globale** |
| **3** | `ROMAIN` | *Ça ressemble à quoi ?* | Sous-type dominant — **table PAR lettre** |
| **4** | `.XX .XX…` | *Quelles particularités ?* | Modificateurs cumulables — **registre global par plages** |

**Règle d'or :** un même **nombre à deux chiffres** (étage 4) a **toujours le même sens**, quelle que soit la lettre. Seul le **chiffre romain** (étage 3) change de sens selon la lettre. C'est ce qui empêche le système de s'effondrer à l'usage.

---

## 2. Séparateurs et notations spéciales

| Notation | Usage |
|---|---|
| `.` | Sépare les étages et les modificateurs entre eux |
| `( )` | **Danger épisodique** : entoure un modificateur de danger (plages 20–49) pour signifier qu'il est saisonnier/temporaire et non chronique. Il **n'impose pas** de relever le degré. |
| `d(p)` | **Forme longue du degré** (optionnelle) : `d` = degré nominal, `p` = degré de pointe pendant un événement. Ex. `M1(3)` = sûre en temps normal, combinaison intégrale requise pendant les pics. |

> Cohérence trans-systèmes : la parenthèse « circonstancielle » reprend la convention `()` de la nomenclature militaire V4.

---

## 3. Formes tronquées (classification incomplète admise)

Toute partie **à droite** peut être omise si l'information manque ou pour alléger. La lecture se fait de gauche à droite ; ce qui n'est pas écrit est simplement « non renseigné ».

| Forme | Signification |
|---|---|
| `M` | Tellurique mature — rien d'autre de connu |
| `M1` | …et on y survit à l'air libre |
| `M.III` | Tellurique, sous-type jungle — **degré inconnu** (le point directement après la lettre = degré omis) |
| `M1.III` | Tellurique, survivable, jungle |
| `M1.III.05.14` | Forme complète |

**Règle de position :** le degré se loge entre la lettre et le premier point. S'il est omis, la lettre est suivie directement du point : `M.III` (degré inconnu) ≠ `M1.III` (degré 1).

---

## 4. ÉTAGE 1 — Lettre : nature physique

**Exclusive.** Une planète a exactement une lettre. Elle ne change que si la planète change *physiquement* de nature (une tellurique calcinée par son étoile passe de `M`/`B` à `E`).

### Lettres définies

| Lettre | Classe | Description |
|---|---|---|
| **A** | Protoplanète | Embryon en formation : agglomérat, accrétion, océan de magma |
| **B** | Tellurique géo-active | Jeune et/ou très active : volcanisme global, tectonique intense |
| **C** | Chtonienne | Noyau résiduel d'une géante gazeuse soufflée par son étoile |
| **D** | Planétoïde / naine | Trop petite, cortège de corps voisins (Pluton, Cérès) |
| **E** | Calcinée / géo-morte | Surface incendiée par une étoile trop proche (Mercure) |
| **F** | Cryomonde | Recouverte de glace sur des km, active ou non (Europe) |
| **H** | Géante de glace | Eau/ammoniac/méthane + noyau (Uranus, Neptune) |
| **J** | Géante gazeuse | H/He massif (Jupiter, Saturne) |
| **K** | Rocheuse nue | Tellurique sans atmosphère significative (Lune) |
| **M** | Tellurique mature | Climats variés, susceptible d'eau liquide (Terre, Mars nue exclue → K) |
| **O** | Monde océanique | Océan global, pas de fond rocheux émergé (planète-océan / hycéenne) |

> **Distinction M-IX vs O :** une tellurique majoritairement couverte d'eau **avec un fond rocheux et des îles** est `M.IX` (climat océanique). Un monde à **manteau d'eau, sans surface solide accessible**, est la lettre `O`.

### Lettres réservées / libres

Gardées volontairement vides pour extension (comme MK a ajouté W, C, S après coup) :

| Lettre | Statut |
|---|---|
| **G** | Libre *(suggestion : monde exotique / composition rare — carbone, silicium)* |
| **I** | **À éviter** (confusion visuelle avec le chiffre `1` et le romain `I`) |
| **L** | Libre |
| **N** | Libre |
| **P** | Libre *(suggestion : monde-forge naturel / dominé par un composé unique)* |
| **Q** | Libre *(suggestion : inclassable / anomalie dimensionnelle — warp)* |
| **R T U V W** | Libre |
| **X** | Réservée : **planète spéciale / hautement spécifique**, cas unique ne rentrant dans aucune autre catégorie |
| **Y** | Libre |
| **Z** | Libre |

> `T` (terraformée) et `O` (errante) du V2 ont disparu comme lettres : ce sont désormais des **modificateurs** (respectivement 50 et 41), car ce ne sont pas des natures physiques. De même `H`/`Y`/`N` (habitabilité) sont remontés dans le **degré**.

### S — Planète-mégastructure

**Lettre dédiée**, distincte de `X` : la lettre signifie qu'**il n'y a pas de planète naturelle dessous** — l'objet entier est une construction artificielle. À ne pas confondre avec le modificateur `52` (une planète *naturelle* qui *porte* une mégastructure).

| Romain | Type |
|---|---|
| I | Anneau orbital habité (Ringworld) |
| II | Sphère de Dyson habitée (coquille complète autour d'une étoile) |
| III | Essaim de Dyson (mégastructure partielle, non contiguë) |
| IV | Monde-vaisseau (structure artificielle mobile à échelle planétaire) |
| V+ | *Libre* |

> Limite connue : le degré (1–4) garde son sens normal, mais un objet comme un Ringworld peut avoir des sections respirables et d'autres exposées au vide sur le même corps — un seul code peine à représenter des zones aussi contrastées (même limite structurelle que les planètes à gravité très variable par latitude).

---

## 5. ÉTAGE 2 — Degré d'exposition (1–4)

Répond à *« que dois-je porter pour sortir un jour ordinaire ? »*. Mesure l'**environnement chronique en conditions normales**, pas le taux de survie global (une jungle mortelle mais respirable reste degré 1 ; sa létalité passe par un modificateur biosphère).

> **Référentiel fixe : humain non modifié.** L'habitabilité dépend toujours de l'espèce qui classe la planète. Pour ce système, le référentiel est **arbitrairement et systématiquement humain** — jamais celui d'une espèce native. Une atmosphère respirable pour une biosphère locale mais toxique pour un humain reste notée comme toxique (degré 3–4), sans exception ni double lecture par espèce.

| Degré | Signification |
|---|---|
| **1** | Survie **à l'air libre**, sans aucune protection |
| **2** | **Protection légère** : respirateur, combinaison étanche légère |
| **3** | **Combinaison intégrale** / système de survie avancé |
| **4** | **Survie temporaire seulement**, même en combinaison intégrale |
| **0** | *(optionnel)* Non relevé / en attente de classification |

### Règles de cohérence degré ↔ modificateurs

Ces règles pourront être **vérifiées automatiquement** par un futur skill (comme `/astronome` sur l'AstroDB).

1. **Chronique compatible.** Un degré 1 ne peut porter **en dur** aucun modificateur des plages 30–39 (ultra-hostile), ni les plus mortels de 20–29. La plupart des 20–29 chroniques imposent degré ≥ 2 ; tout 30–39 chronique impose degré 4.
2. **Redondance de contrôle.** Certaines lettres ont un degré quasi fixe (`J` et `E` sont presque toujours degré 4). Un `J1` doit se justifier — sinon c'est une erreur de saisie.
3. **Épisodique exempté.** Un danger entre parenthèses (§2) **n'entre pas** dans la règle 1 : `M1.(32)` = monde sûr soumis à des tempêtes radioactives saisonnières, parfaitement licite.

---

## 6. ÉTAGE 3 — Chiffre romain : sous-type dominant

**Une table par lettre.** Le lecteur sait toujours quelle table ouvrir : celle de la lettre. Les tables gardent des créneaux libres et sont extensibles au-delà de X.

### M — Tellurique mature (climat dominant)

| Romain | Climat |
|---|---|
| I | Désertique / aride |
| II | Forêt tempérée |
| III | Jungle / tropicale |
| IV | Savane |
| V | Toundra / steppe froide |
| VI | Taïga / forêt boréale |
| VII | Montagneux / arctique |
| VIII | Marais / monde humide |
| IX | Océanique (océans + îles, fond rocheux) |
| X | Continental composite (variété type Terre) |
| XI+ | *Libre* |

### J — Géante gazeuse (classes de Sudarsky, par température)

| Romain | Type |
|---|---|
| I | Nuages d'ammoniac — froide, type Jupiter |
| II | Nuages d'eau — tempérée |
| III | Sans nuages (« claire ») |
| IV | Métaux alcalins — chaude |
| V | Nuages de silicates — Jupiter chaud, ultra-chaude |

> Rappel physique : au-delà de ~0,5 masse de Jupiter, ajouter de la masse **n'agrandit plus** la géante (le gaz se comprime). L'axe « taille » du V2 était trompeur ; la température/chimie de Sudarsky est bien plus significative.

### H — Géante de glace

| Romain | Type |
|---|---|
| I | Classique méthane, bleutée (Neptune, Uranus) |
| II | Riche en ammoniac / autre chimie |
| III+ | *Libre* |

### F — Cryomonde

| Romain | Type |
|---|---|
| I | Croûte fine + océan sous-glaciaire (Europe) |
| II | Calotte globale épaisse (Ganymède) |
| III | Glaces de volatils exotiques — azote/méthane (Triton, Pluton) |
| IV | Cryovolcanisme actif (Encelade) |
| V+ | *Libre* |

### O — Monde océanique

| Romain | Type |
|---|---|
| I | Océan tempéré, surface liquide |
| II | Surface gelée / océan liquide dessous (hycéen froid) |
| III | Océan brûlant / eau supercritique |
| IV+ | *Libre* |

### K — Rocheuse nue

| Romain | Type |
|---|---|
| I | Régolithe cratérisé (Lune, Mercure) |
| II | Ferreuse (riche en métal) |
| III+ | *Libre* |

### D — Planétoïde / naine

| Romain | Type |
|---|---|
| I | Astéroïdal (rocheux) |
| II | Glacé — objet transneptunien (Pluton) |
| III | Métallique |
| IV+ | *Libre* |

### B — Tellurique géo-active

| Romain | Type |
|---|---|
| I | Volcanique global (océans de lave localisés) |
| II | Tectonique intense |
| III | Jeune en refroidissement |
| IV+ | *Libre* |

### E — Calcinée

| Romain | Type |
|---|---|
| I | Surface fondue face à l'étoile |
| II | Dénoyautée / soufflée |
| III+ | *Libre* |

### C — Chtonienne

| Romain | Type |
|---|---|
| I | Noyau de géante exposé |
| II+ | *Libre* |

### A — Protoplanète

| Romain | Type |
|---|---|
| I | Agglomérat / planétésimal |
| II | Océan de magma (accrétion active) |
| III+ | *Libre* |

### G, P, Q… (lettres réservées)

Tables **à définir** au moment où la lettre sera activée.

### X — Spéciale / hautement spécifique

Pas de table par défaut : chaque cas `X` est par définition unique et se documente au cas par cas en note libre plutôt que par un chiffre romain standardisé.

---

## 7. ÉTAGE 4 — Modificateurs : registre global par plages

**Sens fixe, valable pour toutes les lettres.** Cumulables. On lit les dizaines pour connaître la famille.

| Plage | Famille |
|---|---|
| **00–09** | Atmosphère (physique / composition) |
| **10–19** | Biosphère |
| **20–29** | Conditions hostiles chroniques (→ degré 2–3) |
| **30–39** | Conditions ultra-hostiles chroniques (→ degré 4) |
| **40–49** | Particularités orbitales / astronomiques |
| **50–52** | Terraformation & mégastructure (3 codes utilisés, 53–59 libres sans thème imposé) |
| **60–69** | Histoire / cataclysme subi (état hérité) |
| **70–79** | **Réservé** (familles officielles futures) |
| **80–99** | **Libre** (usage local : secteur, campagne, MJ) |

### 00–09 — Atmosphère

| Code | Description |
|---|---|
| 00 | Nulle / vide |
| 01 | Trace résiduelle (exosphère type Mercure) |
| 02 | Ténue stable (Mars, Triton) |
| 03 | Cryogénique active (sublimation, geysers — Encelade) |
| 04 | Volatils gelés en surface (transition saisonnière possible) |
| 05 | Respirable standard (N₂/O₂, ~1 atm) |
| 06 | Respirable dense (haute pression viable) |
| 07 | Réductrice (méthane / ammoniac — Titan) |
| 08 | *Libre* |
| 09 | Exotique / autre |

### 10–19 — Biosphère

| Code | Description |
|---|---|
| 10 | Stérile (aucune vie) |
| 11 | Composés prébiotiques (acides aminés) |
| 12 | Microbienne |
| 13 | Flore/faune primordiale (faible présence) |
| 14 | Type terrestre (faune/flore comparable à la Terre) |
| 15 | Mégafaune |
| 16 | Exotique (biochimie alternative) |
| 17 | Type jurassique / triasique |
| 18 | *Libre* |
| 19 | *Libre* |

### 20–29 — Conditions hostiles chroniques

| Code | Description |
|---|---|
| 20 | Atmosphère acide / corrosive modérée |
| 21 | Température élevée ou instable (60–200 °C) |
| 22 | Pression écrasante (> 5 atm, exploitable) |
| 23 | Orages violents / foudre / perturbations EM |
| 24 | Activité volcanique ou géothermique importante |
| 25 | Pluies toxiques / huileuses (hydrocarbures, acides faibles) |
| 26 | Vents chargés de particules abrasives (érosion) |
| 27 | Atmosphère respirable mais polluée (nocive à long terme) |
| 28 | Champ magnétique faible (radiations accrues, supportable) |
| 29 | Vie hostile / microbienne toxique (spores, toxines) |

### 30–39 — Conditions ultra-hostiles chroniques *(imposent degré 4)*

| Code | Description |
|---|---|
| 30 | Atmosphère ultra-corrosive (dissout les métaux) |
| 31 | Température extrême (> 500 °C ou < −200 °C) |
| 32 | Radiations ionisantes permanentes (létal sans blindage lourd) |
| 33 | Tempêtes de plasma / orages magnétiques géants |
| 34 | Pression écrasante extrême (> 100 atm) |
| 35 | Surface en fusion (océans de lave) |
| 36 | Atmosphère instable / recombinante (explosions chimiques) |
| 37 | Pluies métalliques / silicates |
| 38 | Monde vitrifié / électrisé (surface fondue refroidie) |
| 39 | Résonances énergétiques / cristaux dangereux (effet inconnu) |

### 40–49 — Particularités orbitales / astronomiques

| Code | Description |
|---|---|
| 40 | Verrouillage de marée (rotation synchrone) |
| 41 | Monde errant / capturé par une étoile |
| 42 | Instabilité orbitale (excentricité forte, orbite chaotique) |
| 43 | Résonance orbitale notable |
| 44 | Lune d'une géante (monde satellite) |
| 45 | Système stellaire multiple (plusieurs soleils) |
| 46 | Anneaux planétaires notables |
| 47 | Obliquité extrême (saisons violentes) |
| 48 | Rotation très lente ou très rapide |
| 49 | *Libre* |

### 50–52 — Terraformation & mégastructure (53–59 libres)

| Code | Description |
|---|---|
| 50 | Terraformée (processus achevé) |
| 51 | En cours de terraformation |
| 52 | Porte une mégastructure artificielle (anneau, structure orbitale majeure, ascenseur spatial, sphère de Dyson partielle autour de l'étoile-hôte…) — simple constat oui/non, sans distinction de type |
| 53–59 | *Libre* — aucun thème imposé sur le reste de la dizaine |

> **Terraformation et lettre :** si le processus réussit totalement, la **lettre elle-même peut changer** (une `K` rocheuse nue devenue réellement tellurique bascule vers `M`). Le modificateur `50` ne disparaît pas pour autant : il reste comme **note d'origine**, pour signaler qu'un `M1…50` est un monde artificiellement rendu habitable, distinct d'un `M1` naturel.
>
> **`52` vs lettre `S` :** `52` = planète **naturelle** qui *porte* une mégastructure (ex. un anneau construit autour d'une tellurique normale). La lettre `S` (§4/§6) = la planète **est** la mégastructure, sans rien de naturel dessous. Les deux ne se cumulent jamais sur un même code.

### 60–69 — Histoire / cataclysme subi

| Code | Description |
|---|---|
| 60 | Post-nucléaire |
| 61 | Stérilisée (arme biologique / virus) |
| 62 | Bombardement orbital cataclysmique (Exterminatus) |
| 63 | Impact d'astéroïde / corps céleste majeur |
| 64 | Cataclysme volcanique |
| 65 | Invasion de toxine planétaire |
| 66 | Mutation aberrante généralisée de la faune/flore |
| 67 | Vie vitrifiée / figée |
| 68 | Guerre dévastatrice (champ de ruines) |
| 69 | *Libre* |

### 70–79 — Réservé / 80–99 — Libre

Laissées vides intentionnellement. 70–79 pour de futures familles officielles ; 80–99 pour l'usage local (un secteur, une campagne, un MJ peut y définir ses propres codes sans casser le standard).

---

## 8. Rôle impérial/politique — tags `[ACR]` (externe, via `/nomenclature-v4`)

Le statut/rôle humain d'une planète **n'est plus un modificateur numérique**. Il se note via un tag entre crochets, emprunté **tel quel** au catalogue « Rôles / Métiers » de `/nomenclature-v4` (ex. `AGR` agricole, `HAB` habitations/monde-ruche, `IND` industriel, `MIL` militaire, `MIN` minage…) — voir ce skill pour la liste complète et ses règles de fusion.

**Format :** le tag se colle en fin de code complet, séparé par une espace : `LETTRE.degré.ROMAIN.modificateurs [ACR]`. Comme le reste du système, il est optionnel (règle des formes tronquées, §3).

**Cumul :** on reprend la syntaxe de fusion `.` déjà définie par `/nomenclature-v4` plutôt que d'en inventer une nouvelle : `[AGR.MIN]` = officiellement agricole **et** minier.

### Deux couches volontairement dissociables

| Couche | Porte quoi | Peut être fausse ? |
|---|---|---|
| Modificateurs numériques (étage 4, ce document) | Constat **physique/scientifique** mesurable | Non — c'est la réalité du terrain |
| Tag `[ACR]` (`/nomenclature-v4`) | **Désignation administrative** attribuée par l'empire/l'Imperium en jeu | **Oui** — un registre peut être obsolète ou erroné |

Exemple : `M1.II.15.29 [HAB]` — une planète physiquement couverte de forêt tempérée dense à mégafaune (donc rien d'un Monde-Ruche au sens strict), mais **officiellement classée Monde-Ruche** par une administration qui n'y a jamais mis les pieds. L'écart entre les deux couches est un levier narratif volontaire, pas une incohérence à corriger.

> Ce document (`/nomenclature-planets`) ne modifie jamais le catalogue de `/nomenclature-v4` ; l'ajout ou la clarification d'acronymes (ex. sens de `HAB` à l'échelle planète) relève exclusivement de ce skill, sur son propre `/maj`.

---

## 9. Exemples travaillés (formes complètes)

| Code | Lecture |
|---|---|
| `M1.III.05.14` | Tellurique, survie à l'air libre, jungle, atmosphère respirable, biosphère terrestre → une « Terre jungle ». |
| `M1.II.15.29 [HAB]` | **Catachan (variante administrative)** : physiquement forêt tempérée dense à mégafaune et biosphère hostile — « Jungle World + Death World » au sens physique — mais **officiellement enregistrée Monde-Ruche**. L'écart illustre les deux couches du §8. |
| `M2.VII.42 [MIL]` | **Fenris** : tellurique, protection légère, montagneux/arctique, instabilité orbitale (orbite très elliptique — canon), désignation administrative militaire. |
| `B4.I.06.21.34.31` | **Vénus** : tellurique active, mortelle même en combinaison, volcanique, atmosphère dense, chaleur, pression extrême, température extrême. |
| `F3.I.12` | **Europe** : cryomonde, combinaison intégrale, océan sous-glaciaire, vie microbienne suspectée. |
| `K3.I.02` | **Mars (nue)** : rocheuse, combinaison intégrale, régolithe cratérisé, atmosphère ténue. |
| `K3.I.02.51` | **Mars en terraformation** : idem + statut « en cours de terraformation ». |
| `J4.I` | **Jupiter** : géante gazeuse, létale, nuages d'ammoniac. |
| `M1.X.05.14.(32)` | Monde-jardin standard, mais **soumis à des tempêtes radioactives épisodiques** (danger non chronique — le degré reste 1). |
| `M1(3).X.05.(24)` | Idem, notation longue : degré 1 nominal, **montant à 3 pendant les épisodes** volcaniques. |
| `M1.X.05.14.52 [AGR]` | Monde tempéré naturel, biosphère terrestre, **ceinturé d'un anneau orbital construit**, officiellement classé agricole. |
| `S1.I.05.14` | Ringworld habité, section respirable, biosphère terrestre — un anneau à la Niven dans sa zone habitable. |
| `M.III` | Forme tronquée : on sait juste « tellurique, jungle » — degré et particularités non relevés. |

---

## 10. Décisions ouvertes (à trancher pour figer la V3)

1. **Lettre `I`** : confirmée « à éviter » pour cause de confusion, ou tu veux la réhabiliter malgré tout ?
2. **Degré `0`** : on l'adopte officiellement (utile en Rogue Trader pour les mondes non explorés) ou on s'en tient à la troncature ?
3. **Lettres suggérées** (G, P, Q) : valider ou réattribuer les suggestions entre parenthèses.
4. **Plage 60–69 vs 30–39** : un monde « post-nucléaire » (60) est aussi typiquement « radiations permanentes » (32). Règle proposée : 60–69 décrit la **cause historique**, 30–39 la **conséquence actuelle mesurable**. On les cumule (`…32.60`) plutôt que de choisir.

## Décisions actées depuis la V3 initiale

- **Degré = référentiel humain fixe**, jamais relatif à l'espèce native (§5).
- **Rôle/statut humain** : sorti des modificateurs numériques, porté par un tag `[ACR]` externe emprunté à `/nomenclature-v4`, en deux couches dissociables physique/administratif (§8).
- **50–52** repris pour terraformation (achevée/en cours) et mégastructure portée ; **53–59 libres sans thème imposé**.
- **Lettre `X`** recadrée sur les cas spéciaux/hautement spécifiques (pas de table par défaut).
- **Lettre `S`** créée pour les planètes-mégastructures (l'objet entier est artificiel), distincte du modificateur `52`.

---

*V3 — refonte orthogonale. Prochaine étape possible : transformer ce document en skill `/planetes` (sur le modèle de `/nomenclature-v4`), avec vérification de cohérence croisée automatique via `/astronome`.*
