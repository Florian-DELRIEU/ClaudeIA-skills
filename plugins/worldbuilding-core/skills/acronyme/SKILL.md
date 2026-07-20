---
name: acronyme
description: >
  Système de nomenclature militaire modulaire V4 (et extensions V5 en cours).
  Déclencher IMPÉRATIVEMENT dès que Florian tape /acronyme, ou dès que l'utilisateur
  mentionne un acronyme militaire, un code de véhicule, une unité, un navire, un aéronef,
  une structure, un personnage, ou demande de nommer / classifier / identifier / vérifier /
  étendre un élément dans ce système — y compris à partir d'un matériel réel (nom de
  véhicule, ORBAT à convertir). Également applicable au projet sci-fi Cosmotter pour la
  classification de vaisseaux spatiaux. Utiliser même si la demande semble simple
  (ex: "c'est quoi le code pour X ?", "est-ce que Y entre en conflit avec Z ?",
  "comment noter un transport de troupes ?").
---

# Système de Nomenclature Militaire V4

## Principe général

Format de base : `{Type(Précision)} - {Rôle/Armement} - {Rôle/Armement} - …`

La section **Type** identifie la catégorie du véhicule/unité/structure.
La section **Rôle/Armement** précise la mission principale puis secondaire, par ordre d'importance décroissant.

> ⚠️ L'ordre des rôles est sémantique : `L.AA-REC` ≠ `REC-L.AA`

---

## Séparateurs

### Hiérarchie de disponibilité (Rôles & Armements)

Les trois séparateurs `-`, `/`, `.` encodent un seul critère unifié : **la disponibilité simultanée en combat**.

| Séparateur | Signification | Exemple | Interprétation |
|-----------|---|---|---|
| **`-`** | **Rupture de configuration** | `AA - CAS - REC` | Trois missions, mais reconditionnement/réarmement **obligatoire** entre les deux. Jamais deux en même temps. L'unité passe d'une posture à l'autre. |
| **`/`** | **Coexistence distincte** | `REC / MG` ou `HC / CAC` | Deux choses **séparées physiquement mais présentes simultanément** en combat, sans reconditionnement. Utilisables ensemble ou alternativement, mais restent distinctes. |
| **`.`** | **Fusion** | `SW.PW` ou `HCA.MG` | **Un seul objet** aux deux propriétés fusionnées. Une épée énergétique n'est pas "une épée + quelque chose d'énergétique" — c'est un seul objet qui est *à la fois*. |

### Délimiteurs (structure générale)

| Séparateur | Usage |
|-----------|-------|
| `-` | Aussi : délimiteur entre Type et Rôle(s), ou entre Rôle et Armement(s) — voir exemples ci-dessus pour le sens de rupture de config |
| `()` | **Précisions circonstancielles** (ex : type de propulsion aérienne `(J)`, cargaison chimique `(H₂O)`, variante `(6)`) |

### Groupement

- La hiérarchie de groupement reste : `/` sépare les **blocs**, `.` lie **à l'intérieur** d'un bloc.  
- Exemple : `AA.REC / CAS` = deux configurations : (chasse+reco ensemble) vs (bombardement seul).

### Exemples fusionnés (illustrant les trois niveaux)

| Acronyme | Décomposition | Sens |
|---|---|---|
| `SW.PW` | Épée (SW) + Énergétique (PW) | Une épée énergétique : un seul objet, deux natures |
| `SW / PW` | Épée (SW) / Arme énergétique (PW) | Deux armes distinctes, montées ensemble, utilisables simultanément |
| `SW - PW` | Épée (SW) - Arme énergétique (PW) | Épée OU arme énergétique, reconditionnement obligatoire pour passer de l'une à l'autre |
| `CA.MG` | Canon auto (CA) + Mitrailleuse (MG) | Un système de feu unique où canon et coaxiale travaillent en tandem |
| `LZ / SW.PW` | Laser (LZ) / (Épée + Énergie) | Laser (bras 1) et épée énergétique (bras 2) : deux systèmes distincts, montés ensemble |

---

## Règles de duplication

- **Pas de doublon** au sein des Types
- **Pas de doublon** au sein des Rôles/Armements
- Un même acronyme **peut apparaître** dans Type ET dans Rôle/Armement sans conflit
- La **position** (Type vs Rôle) suffit à désambiguïser

### Non-redondance Type → Rôle

Un **Type porte déjà un rôle implicite**, surtout s'il vient d'une fusion. Ne pas répéter dans la section Rôle un rôle que le Type contient déjà — c'est une **faute**, pas seulement une lourdeur.

| Type | Rôle implicite | Ne pas écrire |
|---|---|---|
| `VBCI` (VB + CI) | Combat d'infanterie | ~~`VBCI-CI`~~ → `VBCI` |
| `TD` | Anti-char | ~~`TD-AT`~~ → `TD` |
| `SPG` | Soutien-feu direct (canon d'assaut) | ~~`SPG-ART`~~ → voir exclusion ci-dessous |
| `SPART` / (SP en rôle `ART`) | Tir indirect longue portée | ~~`SPART-ART`~~ → `SPART` |
| `VCI` (V + CI) | Combat d'infanterie | ~~`VCI-CI`~~ → `VCI` |

Le rôle n'est réécrit que s'il **précise ou nuance** ce que le Type ne dit pas (ex. un rôle secondaire réel, un `REC` sur un châssis qui n'est pas dédié reco).

### Exclusion `SPG` ↔ `ART`

`SPG` et `ART` sont **mutuellement exclusifs** — ils décrivent deux doctrines opposées :

- **`SPG`** = canon d'assaut / soutien-feu **direct**, va tirer relativement près, appui rapproché. *Ex. : StuH, M44.*
- **`ART`** (ou `SP-ART` / `SPART`) = **tir indirect longue portée**, reste en retrait. *Ex. : Hummel, M109, AuF1.*

Un véhicule est l'un **ou** l'autre, jamais `SPG-ART`. Choisir selon la **vocation d'emploi** :
- Vocation appui rapproché direct → `SPG` (ex. `SPG-C155/MG` pour le M44)
- Vocation tir indirect longue portée → `SP-ART` ou `SPART` (ex. `SP-ART/MG` pour l'AuF1, tourelle à débattement limité)

---

## Cas d'application — Choisir entre `-`, `/`, `.`

### Pour les **rôles et missions**

**Utiliser `-` si :**
- Passer d'un rôle à l'autre exige un reconditionnement (retour à la base, changement de configuration, adaptation tactique)
- Les deux rôles sont **mutuellement exclusifs à l'instant T**
- Exemple : `AA - CAS - REC` = avion multi-rôle, mais chasse, soutien rapproché et reconnaissance ne peuvent pas coexister sans perte d'efficacité

**Utiliser `/` si :**
- Les deux rôles coexistent **sans reconditionnement**, l'unité les assume simultanément
- Exemple : `AA / REC` = chasseur avec capteurs de reconnaissance intégrés, peut engager ET observer en même temps

**Utiliser `.` si :**
- Les deux rôles sont **fusionnés en un seul concept inséparable**
- Rare pour les rôles, plus courant dans les armements (voir ci-dessous)

### Pour les **armements**

**Utiliser `-` si :**
- Passer d'une arme à l'autre exige un reconditionnement/démontage (réarmement en atelier, reconfiguration majeure)
- Exemple : `HCA - LM` = tank avec canon OU lance-roquettes, jamais les deux (exige retour en base pour changer)

**Utiliser `/` si :**
- Deux armes sont montées **simultanément et utilisables ensemble** sans reconditionnement
- Elles restent physiquement distinctes mais présentes en combat
- Exemple : `HC / CAC` = canon ET lame, utilisables en même temps · `LZ / SW.PW` = laser ET épée énergétique

**Utiliser `.` si :**
- **Un seul objet** possède intrinsèquement deux propriétés fusionnées
- L'objet n'existe que par la fusion de ces deux propriétés
- Exemples : `SW.PW` (épée énergétique = 1 objet) · `HCA.MG` (canon + coaxiale inséparable = 1 système de feu)

### Arbre de décision rapide

```
"Puis-je utiliser les deux simultanément sans modification ?"
├─ Non, reconditionnement/démontage obligatoire → utiliser `-`
├─ Oui, mais ce sont deux choses distinctes → utiliser `/`
└─ Oui, c'est la même chose ayant deux natures → utiliser `.`
```

---

## Gabarits (modificateurs de taille)

Utilisables en complément du Type ou du Rôle :

`L` Léger · `M` Moyen · `H` Lourd · `SH` Super-Lourd  
`2L / 2M / 2H` À deux mains (L/M/H)  
`U` Unnamed / Drone — véhicule sans équipage

> **Sur les Types véhicules composés (`V`+locomotion, voir `terrestres.md`) :** `L`/`M` peuvent s'infixer directement (`VBL`, `VHM`...), mais **`H`/`SH` s'écrivent toujours en suffixe** (`.H` / `.SH`), jamais infixés — pour éviter toute confusion avec les marqueurs de locomotion `H` (semi-chenillé) et `B` (chenillé). Ex. : `VBTT.H`, pas `VBHTT`.

---

## Portée

`SRG` Court · `MRG` Moyen · `LRG` Long · `SLRG` Super-long · `XRG` Extrême (quasi-illimité)

---

## Compétences

`-` Inférieur au standard · `+` Standard · `*` Supérieur au standard  
*(Une valeur numérique peut préciser davantage)*

---

## Sections détaillées

Pour les tables complètes d'acronymes, consulter :

- `references/terrestres.md` — Véhicules terrestres & hélicoptères
- `references/aeriens.md` — Véhicules aériens
- `references/maritimes.md` — Navires & vaisseaux spatiaux
- `references/infanterie.md` — Personnages, grades, rôles, armes, munitions
- `references/structures.md` — Bâtiments, zones, structures
- `references/groupements.md` — Échelons, types d'unités
- `references/materiaux.md` — Matériaux et ressources

---

## Identifier l'acronyme d'un véhicule/personnel réel (toute nation, toute époque)

Quand la tâche part d'un **matériel réel** (nom de véhicule, description d'un ORBAT
historique, catalogue à convertir…) plutôt que d'un acronyme déjà posé, consulter
**`identification/`** avant de composer un code à la main :

- `identification/METHODE.md` — le raisonnement : principe du châssis (une même
  plateforme garde le même Type à travers ses variantes), pipeline en 6 étapes, règles
  d'arbitrage pour choisir l'acronyme **le plus évident** quand plusieurs sont
  défendables.
- `identification/chassis-types.md` — table châssis → Type par archétype, multi-nations
  et multi-époques (extensible).
- `identification/personnel.md` — codage des éléments de personnel (escouade/équipe/
  binôme + rôle dominant).
- `identification/lexique.json` — registre `désignation réelle ↔ code v4`, à consulter
  en premier (cohérence inter-fichiers) et à enrichir à chaque nouveau cas résolu.
- `identification/entrainement.md` — protocole du **mode entraînement** : Florian donne
  un ou plusieurs noms de véhicules/personnels (souvent sans autre consigne — c'est le
  signal en soi), attend un raisonnement détaillé étape par étape + l'acronyme final,
  puis note sur 5. Consulter ce fichier dès que Florian fournit un nom sans contexte de
  conversion de fichier — c'est très probablement une session d'entraînement. Journaliser
  systématiquement les cas validés (note ≥4) dans `lexique.json`.

Se déclenche typiquement pour : convertir un ORBAT en acronymes v4, identifier le code
d'un véhicule nommé, vérifier qu'un même châssis reçoit bien un Type cohérent à travers
ses variantes, ou mener une session d'entraînement à l'identification.

---

## Décisions établies (V4 + extensions validées)

Ces décisions ont été explicitement validées et priment sur toute interprétation naïve :

| Décision | Détail |
|----------|--------|
| `N` = Nucléaire (propulsion) | Motorisation nucléaire, tous contextes |
| `NK` = Nucléaire (armement) | Armement nucléaire (nuke) ⚠️ Distinct de N |
| `NV` = Nocturne (rôle) | Capacité vision nocturne |
| `NVG` = Vision nocturne (équipement) | Jumelles/lunettes spécifiques ⚠️ Distinct de NV |
| `STH` ≠ `SD` | `STH` = furtivité visuelle/radar · `SD` = silence/discrétion (armes supprimées) |
| `C` = Croiseur (naval) / `CAV` = Cavalerie | Désambiguïsation par position (Type vs Rôle) |
| `AN` (anti-navire) | Redondant si l'armement implique déjà la fonction anti-navire → omettre |
| Transport maritime | `TT` troupes · `TR` matériel générique · `MAT` · `MUN` |
| Cargaisons spécifiques | Symboles chimiques entre parenthèses : `TR(H₂O)`, `TR(CH₄)` |
| Hiérarchie gunship | Suffixe `G` : `KG`, `FFG`, `PFG`, `DDG`, `CG` |
| `FF` = corvette trans-océanique | Distincte de `PF` (polyvalente) |
| Doctrine > taille (naval) | Le type est déterminé par la doctrine et l'indépendance opérationnelle, pas le tonnage |
| `BB` vs `CA` | `BB` tient la ligne / absorbe les dommages · `CA` frappe et conserve une capacité de désengagement |
| `-B` vs `-MEC` (groupements) | `-B` = force principale = chars de combat · `-MEC` = infanterie transportée par VBTT. Deux types distincts, non combinables avec `.` |
| `MCAA` | Fusion prédéfinie MCA + AA. Canon automatique moyen à usage anti-aérien |

---

## Notation numérique

Les chiffres permettent de préciser un acronyme selon leur position. Ils suivent les mêmes règles de placement que le gabarit.

| Format | Signification | Exemple |
|--------|--------------|---------|
| `ACR#` | Nombre physique (roues, pattes…) collé à l'acronyme | `VB6` = voiture blindée 6 roues · `MK6` = mecha 6 pattes |
| `ACR(#)` | Variante ou modèle | `VU(6)` = camion variante 6 |
| `ACR.#t` | Poids en tonnes — remplace le gabarit L/M/H | `VU.3t` = camion 3 tonnes |
| `ACR.#` | Calibre en mm (armes) — implicite, pas besoin d'écrire mm | `CA.20` = canon auto 20mm |
| `#ACR` | Nombre de tubes / canons jumelés (avant l'acronyme) | `2CA.20` = deux canons auto 20mm jumelés |

**Ordre complet :** `{Type}{#roues}({variante})-{#tubes}{Armement}.{calibre}`
Exemple : `VB6(2)-2CA.20` = voiture blindée 6 roues variante 2, deux canons auto 20mm jumelés

**Gabarit littéral vs calibre numérique — mutuellement exclusifs**
Le L/M/H et le calibre numérique ne coexistent jamais sur le même acronyme :
- `MCAA` → calibre moyen approximatif
- `CAA.20` → calibre exact 20mm (M implicitement déduit)
- `2CAA.20` → deux canons AA 20mm jumelés

---

## Règles de composition des fusions

Les acronymes fusionnés (ex : `TES`, `TEAT`, `VBCI`, `MCAA`…) sont des **unités atomiques** — ils ne peuvent pas être chaînés entre eux.

> ❌ `TES.AT` (chaînage de deux fusions) est interdit  
> ✅ Choisir **une** fusion comme base, puis ajouter les acronymes supplémentaires en suffixe

Exemple : sniper antichar avec camouflage → choisir `TEAT` (base) puis ajouter `STH`, `SD`, etc. → `TEAT.STH.SD`

---

## Liberté des rôles et armements cross-domaine

Il n'existe **aucune restriction de domaine** sur les rôles et armements.  
Un rôle naval peut s'appliquer à un appareil aérien, un rôle terrestre à un navire, etc.  
Seuls les Types sont spécifiques à leur catégorie (terrestre, aérien, maritime).

---

## Extensions Cosmotter (Sci-Fi)

Le système s'applique aux vaisseaux spatiaux avec adaptations :
- La géographie côtière et les menaces 2D ne se transfèrent **pas**
- La logique sous-marin → vaisseau furtif **se transfère**
- La hiérarchie d'escorte **se transfère**
- Types spéciaux : `VG` Antigrav · `TG` Char antigrav · `SC` Spacecraft · `ORB` Orbiteur · `CS` Capital ship · `SF` Chantier naval

---

## Workflow de vérification (à appliquer systématiquement)

Quand l'utilisateur propose ou demande un acronyme :

1. **Identifier la catégorie** (Type ? Rôle ? Armement ? Structure ?)
2. **Vérifier l'absence de conflit** dans la même catégorie (pas de doublon interne)
3. **Vérifier la cohérence positionnelle** (un même acronyme en Type et Rôle est OK)
4. **Appliquer les décisions établies** (tableau ci-dessus)
5. **Choisir le bon séparateur** (voir "Cas d'application" ci-dessus) :
   - `-` = reconditionnement obligatoire (rupture de configuration)
   - `/` = coexistent sans modification (mais distincts)
   - `.` = fusion en un seul objet/concept
6. **Proposer des alternatives** si conflit détecté, avec justification
7. **Signaler les redondances** (ex : `AN` superflu si armement implique anti-navire)
