---
name: orbat
description: >
  Lecture, écriture, analyse et agrégation d'ORBAT (Order of Battle), au format
  orbat-mapper.app (JSON, type "ORBAT-mapper") comme au format xlsx ODIN / JTDS
  (TRADOC G2). Déclencher IMPÉRATIVEMENT dès que Florian tape /orbat, fournit un
  fichier ORBAT JSON, un ORBAT xlsx ODIN ou un XML JTDS (OBSV4.2), fournit une
  image d'ORBAT ou de symboles militaires (APP-6 / OTAN / 2525C), ou demande de :
  créer/générer un ORBAT, lire/comprendre la structure d'un ORBAT, lister ou
  compter le matériel/personnel d'une unité ou d'un camp, faire la somme des
  équipements sur tout ou partie d'un ORBAT, décoder un symbole militaire (sidc),
  construire un ordre de bataille, convertir une image d'ORBAT en JSON, ou
  convertir un ORBAT xlsx ODIN vers orbat-mapper. Déclencher même pour des
  demandes courtes ("combien de chars dans cette division ?", "lis cet ORBAT",
  "ajoute une compagnie", "c'est quoi ce symbole ?", "lis ce classeur ODIN",
  "combien de BMP dans ce xlsx ?").
---

# ORBAT — orbat-mapper.app & xlsx ODIN

Travailler avec les ordres de bataille de Florian. **Deux formats**, à ne pas
confondre :

| Format | Quoi | Référence | Outil |
|---|---|---|---|
| **JSON orbat-mapper** | format natif de Florian, `type: "ORBAT-mapper"` | `references/format.md` | `orbat_lib.py`, `aggregate.py`, `new_orbat.py`… |
| **xlsx ODIN / JTDS** | ORBAT publiés par ODIN (TRADOC G2) : classeur `UNIT INFO` + feuilles template, équivalent tableur du XML JTDS OBSV4.2 | `references/xlsx_format.md` | `xlsx_orbat.py` |

Identifier le format **avant tout** : un classeur avec une feuille **`UNIT INFO`**
est un ORBAT ODIN → Tâche 6. Un `.json` `type: "ORBAT-mapper"` → Tâches 1-5.

Sur le JSON : quatre tâches — **lire** un ORBAT, le **comprendre**, **agréger** son
matériel, et en **écrire** de nouveaux.

## Avant tout : connaître le format

La structure exacte est dans `references/format.md` (enveloppe, side → groups →
subUnits récursifs, catalogues `equipment`/`personnel`, champ `state`). **La lire dès
qu'on manipule un fichier réel.** En une phrase :

> `sides[] → groups[] → subUnits[]…` (récursif). Chaque unité porte `id`, `name`,
> `sidc` (20 chiffres), et optionnellement `equipment`/`personnel` en `[{name, count}]`
> qui réfèrent aux catalogues racine. Sommer = parcourir un sous-arbre et additionner.

Les fichiers réels peuvent être volumineux (jusqu'à des dizaines de Mo, 30 000+ unités).
**Toujours passer par les scripts ou Python** ; ne jamais essayer de tout lire à l'œil.

## Outils fournis (`scripts/`)

Lancer avec `python3` ; ils sont autonomes (juste la lib partagée `orbat_lib.py`).

- **`aggregate.py`** — somme équipement, personnel et/ou **supplies**.
  - tout : `python3 scripts/aggregate.py ORBAT.json`
  - une partie : `--unit "<nom ou id>"` (sous-arbre), `--kind equipment|personnel|supplies|all`
  - **état temporel** : `--final` (rejoue la timeline) ou `--at "<date ISO>"`
  - `--json` pour une sortie machine.
- **`timeline.py`** — lit un scénario comme un récit : `events` globaux + journal d'une
  unité (`--unit`), positions, titres narratifs, changements. `--events` pour les jalons seuls.
- **`validate.py`** — vérifie qu'un fichier est sain et réimportable (ids uniques, sidc
  20 chiffres, codes présents aux catalogues, entrées `state` horodatées).
  `python3 scripts/validate.py ORBAT.json`
- **`new_orbat.py`** — construit un ORBAT import-ready. En CLI : enveloppe vierge
  (`--name --out`). Comme **bibliothèque** quand on génère depuis une demande :
  `build_sidc`, `make_unit`, `make_group`, `make_side`, `new_orbat`, puis
  `orbat_lib.save`.
- **`xlsx_orbat.py`** — **format xlsx ODIN** (Tâche 6) : `read`, `tree`, `agg`,
  `validate`, `tojson`. En bibliothèque : `load`, `expand`, `save`, `add_unit`,
  `remove_unit`, `TemplateBuilder`, `validate`, `to_mapper_json`.

## Tâche 1 — Lire / comprendre un ORBAT JSON

1. Lire `references/format.md` si pas déjà fait.
2. Charger avec `orbat_lib.load`, donner un aperçu : nom, version, nombre d'unités,
   tailles des catalogues, arborescence des camps/groupes (échelons supérieurs).
3. Répondre à la question posée (structure, ordre de bataille, effectifs…). Pour
   présenter une hiérarchie, indenter par profondeur et afficher l'échelon (depuis le
   `sidc`, voir `references/sidc.md`).

## Tâche 2 — Lire un ORBAT depuis une IMAGE  → JSON importable

C'est le mode par défaut choisi par Florian : **reconstruire un JSON réimportable**.

1. Analyser l'image : identifier la hiérarchie (qui est sous qui), et pour chaque
   symbole, en déduire l'**échelon** (barres/points au-dessus du cadre) et le **type**
   (icône interne) — voir la correspondance dans `references/sidc.md`.
2. Pour chaque unité, composer un `sidc` 20 chiffres avec `build_sidc`. En cas de doute
   sur l'entité, consulter `references/sidc_dictionary.json` (codes réels déjà utilisés
   par Florian) et choisir le plus proche ; signaler les incertitudes plutôt que deviner.
3. Construire l'arbre avec `make_unit`/`make_group`/`make_side`/`new_orbat`, générer des
   `id` uniques (automatique), respecter les conventions de `references/naming.md`
   (pas de parenthèses dans `name`, `shortName` systématique), puis `validate.py` avant
   de livrer.
4. Livrer le fichier `.json` (via `present_files`) + un résumé des choix faits et des
   points incertains à confirmer.

## Tâche 3 — Agréger le matériel (tout ou partie)

Utiliser `aggregate.py`. « Une partie » = un sous-arbre : passer `--unit` avec le nom
(exact puis partiel) ou l'`id` de l'unité racine. Le script résout les codes vers leur
description via le catalogue et trie par quantité décroissante. Pour des regroupements
plus fins (par catégorie, par côté, par échelon), adapter en s'appuyant sur
`orbat_lib.iter_units` / `subtree_units` / `aggregate`.

## Tâche 4 — Écrire / générer un ORBAT  → toujours import-ready

Florian veut **toujours** un JSON directement réimportable dans orbat-mapper.app.

1. Clarifier l'intention si besoin (camp, échelon racine, composition), sinon proposer
   une structure raisonnable et la construire.
2. Construire avec les helpers de `new_orbat.py`. Échelon par nom (`"compagnie"`,
   `"bataillon"`…) ou code ; entité 6 chiffres (réutiliser un code du dictionnaire pour
   rester cohérent avec son univers). **`make_group()` réservé à `side.groups` (tête
   uniquement) : tout niveau intermédiaire (division, brigade, regroupement...) passe
   par `make_org_unit()`/`make_unit()`, jamais `make_group()` imbriqué — piège d'import
   confirmé, voir `references/format.md`.**
3. Déclarer dans les catalogues racine tout code `equipment`/`personnel` employé, avec
   une description.
4. **Nommage** (toute unité, sans exception) : suivre `references/naming.md` —
   **jamais de parenthèses dans `name`** (pas de contexte de parenté, de garnison ni de
   note d'incertitude entre parenthèses ; la hiérarchie porte déjà le contexte, la
   garnison va après un tiret cadratin, le reste va en `description`), et **toujours**
   renseigner un `shortName` par abréviation du rôle (voir table de correspondance).
   - Si la source est en anglais et que Florian veut aligner les noms sur
     `/nomenclature-v4` : `orbat_lib.apply_word_substitutions(orbat,
     orbat_lib.ECHELON_WORD_SUBST_EN_TO_NOMV4)` (naming.md Règle 4 — attention au
     piège FR/EN sur « Section »).
   - Si des échelons peuvent être vides (TOE non détaillé par la source) :
     `orbat_lib.mark_empty_subtrees(orbat)` juste avant `validate.py`, pour
     marquer (symbole ` Ø`) les branches entières sans equipment ni personnel
     (naming.md Règle 3 — ne marque que si TOUT le sous-arbre est vide).
5. **Toujours** finir par `validate.py` (0 erreur attendu), puis livrer le `.json` avec
   `present_files`.

## Tâche 5 — Lire un scénario temporel (positions, mouvements, ressources qui changent)

Certains fichiers sont des **scénarios animés** : unités positionnées sur la carte,
déplacements, et ressources/statuts qui évoluent dans le temps (champ `state[]`,
catégorie `supplies`, `events`). Modèle complet dans `references/format.md`.

1. Vue d'ensemble narrative : `timeline.py ORBAT.json` (jalons globaux + unités actives).
2. Suivre une unité : `timeline.py ORBAT.json --unit "<nom>"` (positions, itinéraires
   `via`, titres, consommations).
3. État des ressources à un instant : `aggregate.py --at "<date ISO>"` ou `--final`
   (rejoue la timeline : `update` = absolu, `diff` = delta). Comparer base vs instant T
   montre les pertes/consommations (ex. munitions, véhicules détruits).
4. Pour des calculs sur mesure (position à T, trajet, consommation entre deux dates),
   s'appuyer sur `orbat_lib.resource_at`, `position_at`, `unit_timeline`, `scenario_events`.
5. **Détachements temporaires (démontage, véhicules trackés isolément) :** un élément
   enfant dont le `state` finit par `location: null` sans perte associée signale un
   réembarquement/regroupement dans l'unité mère, pas une destruction — convention
   détaillée dans `references/format.md`, détectée automatiquement par
   `orbat_lib.vanished_elements` et affichée par `timeline.py`. Toujours distinguer ce
   cas d'une vraie perte (chercher un `update`/`diff` négatif au même moment) avant de
   conclure dans un récit.

## Tâche 6 — ORBAT au format xlsx ODIN (lire / créer / éditer / convertir)

Déclencheurs : un `.xlsx` avec une feuille **`UNIT INFO`**, un XML **JTDS**
(`OBSV4.2`), les mots « ODIN », « TRADOC », « JTDS », ou une demande de lire /
créer / éditer un ORBAT en tableur.

**Lire `references/xlsx_format.md` avant de toucher au fichier.** Tout passe par
`scripts/xlsx_orbat.py` — ne jamais parser le classeur à la main.

En une phrase :

> `UNIT INFO` = l'ossature (1 ligne par unité ; `T` = composition prise dans la
> feuille template nommée, `U` = conteneur dont les enfants sont d'autres lignes
> de `UNIT INFO`). Les feuilles template décrivent la composition avec 5 types de
> lignes : `U` unité, `E` plateforme, `W` remorqué, `M` emport, `P` personnel
> (rôle `C` équipage / `P` passager).

### Deux pièges à erreurs silencieuses (détaillés dans `xlsx_format.md`)

1. **Les noms d'unités ne sont pas uniques dans une feuille.** La résolution est
   **séquentielle** : un nom désigne la définition `U` la plus récente. Indexer
   par nom fusionne les homonymes et sur-compte le matériel sans lever d'erreur.
   `xlsx_orbat.py` gère ça — c'est une raison de plus de ne pas parser à la main.
2. **`ECHELON` et l'échelon du code 2525C divergent volontairement.** Ne jamais
   « corriger » l'un d'après l'autre ; `ECHELON` fait autorité.

### Lire / analyser

```bash
python3 scripts/xlsx_orbat.py read     F.xlsx            # compteurs après expansion
python3 scripts/xlsx_orbat.py tree     F.xlsx --depth 3
python3 scripts/xlsx_orbat.py agg      F.xlsx --unit "171 IFV BDE" --what equipment
```

### Créer / éditer

`new_workbook()`, `add_unit()`, `remove_unit(cascade=True)` pour l'ossature ;
`TemplateBuilder` pour une feuille template (il gère la numérotation séquentielle
des IDs, partagée entre `E`/`W`/`M`/`P`). **Toujours finir par `validate`**
(0 problème attendu) puis `save`, et livrer avec `present_files`.

### Convertir vers orbat-mapper

```bash
python3 scripts/xlsx_orbat.py tojson F.xlsx OUT.json --side "NOM"
python3 scripts/validate.py OUT.json          # doit donner 0 erreur
```

La conversion est **lossy par construction** : le rôle équipage/passager et les
liens porteur→remorque ne sont pas représentables en orbat-mapper (le reste —
UIC, unit class, 2525C, échelon ODIN — part en `description`). `tojson` **liste
les function ID 2525C qu'il n'a pas su mapper** (entité générique `000000`) : les
signaler à Florian plutôt que de les passer sous silence, et compléter
`FUNCTION_MAP` s'il donne le code. Sur le fichier de référence, la couverture est
complète (56/56).

## Catégories de ressources

Trois catégories cohabitent : **`equipment`** (véhicules, armes lourdes), **`personnel`**
(escouades, équipes) et **`supplies`** (munitions, carburant ; catalogue
`supplyCategories`). Les trois se somment de la même façon ; `--kind all` les couvre.

## Codes équipement / personnel et nomenclature-v4

Les codes (`VUTT`, `V-HMG`, `BMP 2 IFV`…) sont définis dans les catalogues du fichier.
**Par défaut, s'appuyer sur les descriptions du catalogue.** Ne croiser avec le skill
`nomenclature-v4` (décodage/validation des codes selon le système de Florian) **que s'il
le demande explicitement**.

## Persistance des éditions du skill

Comme pour ses autres skills, les modifications de ce dossier ne survivent pas entre
sessions sans le cycle `/maj` → zip → ré-upload. Ne repackager le skill que sur demande
explicite de Florian.

## Exemples de déclenchement

- « Combien de VAB en tout dans l'ORBAT 2023 ? » → Tâche 3, `aggregate.py --kind equipment`.
- « Lis-moi la structure de ce fichier » (JSON fourni) → Tâche 1.
- « Voici une photo de mon ORBAT, fais-en le JSON » → Tâche 2.
- « Crée une compagnie d'infanterie mécanisée à 3 sections » → Tâche 4, JSON import-ready.
- « C'est quoi le symbole 10031000151211005600 ? » → décodage via `references/sidc.md`.
- « Combien de munitions il reste au 2e peloton à 5h du matin ? » → Tâche 5, `aggregate.py --kind supplies --at …`.
- « Raconte-moi ce qui se passe dans ce scénario » / « où est passée la 1 CO ? » → Tâche 5, `timeline.py`.
- « Lis ce classeur ODIN » / xlsx avec feuille `UNIT INFO` fourni → Tâche 6, `xlsx_orbat.py read`.
- « Combien de BMP 2 dans la 171 IFV BDE ? » (xlsx) → Tâche 6, `agg --unit`.
- « Convertis cet ORBAT ODIN pour orbat-mapper » → Tâche 6, `tojson` + `validate.py`.
- « Ajoute un bataillon à ce classeur » / « fais-moi un ORBAT ODIN en xlsx » → Tâche 6, `add_unit`/`TemplateBuilder` + `validate`.
