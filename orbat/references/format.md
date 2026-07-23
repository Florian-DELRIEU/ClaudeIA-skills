# Format JSON `orbat-mapper.app`

Référence complète du format exporté par le site, vérifiée sur trois fichiers réels
(versions `1.1.0`, `2.0.0`, `0.31.0`). Le `type` est toujours `"ORBAT-mapper"`.

## Enveloppe (racine)

| Clé | Type | Rôle |
|-----|------|------|
| `id` | str | identifiant du scénario |
| `type` | str | toujours `"ORBAT-mapper"` |
| `version` | str | version du format (`2.0.0` = export récent) |
| `meta` | obj | `{createdDate, lastModifiedDate}` (ISO 8601) |
| `name` | str | nom du scénario |
| `startTime` | str | date de départ (ISO avec offset) |
| `timeZone` | str | ex. `"Europe/Paris"` |
| `description` | str | description libre |
| `symbologyStandard` | str | `"app6"` (APP-6D / 2525) |
| `sides` | list | les camps (voir plus bas) |
| `layers` | list | calques cartographiques `{name, id, features[]}` |
| `events` | list | événements temporels (souvent vide) |
| `mapLayers` | list | fonds de carte additionnels |
| `equipment` | list | **catalogue** matériel `[{name, description}]` |
| `personnel` | list | **catalogue** personnel `[{name, description}]` |
| `supplyCategories` | list | catégories de ravitaillement |
| `settings` | obj | `{rangeRingGroups, statuses, supplyClasses, supplyUoMs, map, symbolFillColors, customSymbols}` |

Les deux **catalogues** (`equipment`, `personnel`) définissent les codes courts et leur
description. Les unités ne stockent que le code + une quantité (voir ci-dessous).

## Side (camp)

```
{ "name", "standardIdentity", "symbolOptions": {"fillColor"},
  "units": [],        // unités directement sous le side (rare, anciennes versions)
  "id",
  "groups": [ ... ] } // organisation normale
```

`standardIdentity` est le chiffre d'identité APP-6 : `"3"` = ami, `"6"` = hostile, etc.
Note : dans certains vieux exports, `side.units` contient un objet placeholder
`{rootUnitName, rootUnitEchelon, rootUnitIcon}` à ignorer (pas une vraie unité).

## Group

```
{ "name", "id", "subUnits": [ ... ], "symbolOptions": {} }
```

**⚠️ Piège confirmé (import réel cassé, ORBAT Norvège 1940, juillet 2026) : un
`Group` (sans `sidc`) ne doit JAMAIS apparaître ailleurs qu'en tête de
`side.groups`.** L'importeur orbat-mapper.app recurse correctement dans les
**unités** (`subUnits` d'une Unit, qui ont toutes un `sidc`), mais s'arrête dès
qu'il rencontre, au sein d'un `subUnits`, un nœud qui ressemble à un `Group`
(pas de `sidc`) — résultat observé : seul le tout premier échelon se charge à
l'import, tout le reste de l'arbre est silencieusement ignoré, sans erreur.

**Règle pratique pour Tâche 4 (écriture) :** `side.groups` contient un (ou
quelques) vrai(s) `Group` de tête — c'est le SEUL endroit où l'absence de
`sidc` est correcte. **Tout le reste de la hiérarchie (divisions, brigades,
régiments, bataillons, compagnies…) doit être des `Unit` récursives, chacune
avec son propre `sidc`**, même quand elle ne sert qu'à regrouper des
sous-unités sans incarner une vraie unité de combat (ex. « Unités hors
division », un district/division qui n'est administrativement qu'un
regroupement). Utiliser `make_unit(..., subUnits=[...])` — jamais
`make_group()` — pour tout niveau intermédiaire. Voir `new_orbat.py:
make_org_unit()`, l'helper dédié à ce cas.

## Unit (récursif via `subUnits`)

```
{
  "id":   "Fzp60pPecl",          // 10 caractères [A-Za-z0-9]
  "name": "Bataillon Infanterie",
  "sidc": "10031000161211000000", // 20 chiffres, APP-6D (voir sidc.md)
  "subUnits": [ ... ],            // récursif, profondeur libre
  "equipment":  [ {"name":"VUTT","count":3} ],   // optionnel, réfère au catalogue
  "personnel":  [ {"name":"SQ-I","count":2} ],   // optionnel, réfère au catalogue
  "symbolOptions": { "fillColor":"#80e0ff" },    // optionnel
  "reinforcedStatus": "None",     // None | Reinforced | Reduced (optionnel)
  "shortName", "description", "externalUrl", "style", "textAmplifiers", // optionnels
  "state": []                     // états/positions temporels (souvent vide)
}
```

Points clés :

- **La hiérarchie est entièrement portée par `subUnits`.** Une unité « mère » regroupe
  ses sous-unités ; les feuilles (sans `subUnits`) portent généralement l'équipement réel.
- **`equipment` et `personnel` au niveau d'une unité = liste de `{name, count}`.** Le
  `name` doit exister dans le catalogue racine correspondant. La quantité réelle d'une
  unité « mère » = somme des feuilles de son sous-arbre (les mères ne dupliquent pas).
- **Sommer le matériel = parcourir le sous-arbre voulu et additionner les `count` par
  `name`.** C'est exactement ce que fait `scripts/aggregate.py`.

## Scénarios : la dimension temporelle (`state`, `events`, `supplies`)

Un fichier peut être un simple ORBAT organisationnel **ou** un scénario animé où les
unités sont positionnées sur la carte, se déplacent, et voient leurs ressources et
statuts changer dans le temps. Trois éléments portent cette dimension.

### Troisième catégorie de ressources : `supplies`

À côté de `equipment` et `personnel`, une unité peut porter `supplies` (munitions,
carburant…), même structure de base `[{name, count}]`. Les codes réfèrent au catalogue
racine **`supplyCategories`** : `[{name, description, supplyClass, uom}]`. Les classes et
unités de mesure sont définies dans `settings.supplyClasses` et `settings.supplyUoMs`.
Les statuts personnalisés (Retranché, En déroute, À court de muni…) sont dans
`settings.statuses`.

### `events` (racine) — fil narratif global

`[{title, startTime, id}]` : les grands jalons du scénario, datés. À lire en premier
pour situer l'histoire.

### `state[]` (par unité) — la timeline

Liste d'entrées datées décrivant ce qui arrive à l'unité. Champs d'une entrée :

| Champ | Rôle |
|-------|------|
| `id` | identifiant de l'entrée |
| `t` | horodatage ISO |
| `location` | position `[lng, lat]` à cet instant |
| `via` | itinéraire suivi `[[lng,lat], …]` pour atteindre `location` |
| `title` | titre narratif (« La 1 CO intervient contre les radicaux ») |
| `status` | changement de statut (réfère `settings.statuses`) |
| `sidc` | changement de symbole (ex. posture de combat) |
| `symbolOptions` | changement de style (couleur…) |
| `update` | **valeurs absolues** : `{equipment\|personnel\|supplies: [{name, onHand}]}` |
| `diff` | **delta** : `{… : [{name, onHand}]}` (ex. `onHand: -2` = 2 consommés) |

**Calculer l'état à un instant `t`** = partir des quantités de base (`count`), puis
rejouer chronologiquement les entrées `state` jusqu'à `t` : `update` **remplace** la
valeur (`onHand`), `diff` **ajoute** le delta. C'est ce que fait
`orbat_lib.resource_at` (et `aggregate.py --at` / `--final`). La position courante se
lit avec `orbat_lib.position_at`.

### Convention observée : détachement temporaire et réembarquement/regroupement

**Confirmée par Florian sur « Opération Orage ».** Quand une unité « mère » subit une
perte de matériel (`update`/`diff` négatif sur `equipment`), elle peut ensuite se
décomposer temporairement en plusieurs **sous-unités enfants** suivies individuellement
sur la carte : des escouades démontées (sidc symbol set `10`, souvent nommées
sobrement `1`, `2`, `3`…) et/ou les véhicules restants trackés isolément (sidc symbol
set `15`, souvent sans `name`). Ces éléments ont leur propre `state[]` qui démarre après
celui de la mère et progresse en parallèle, en formation resserrée autour d'elle.

Quand ces éléments **cessent d'être suivis**, leur dernière entrée de `state` a
`location: null` — sans aucune perte enregistrée à ce moment. C'est le signal d'un
**réembarquement / regroupement dans l'icône de l'unité mère**, pas d'une destruction :
la mère reprend alors sa propre timeline de position juste après. Pour vérifier
qu'il ne s'agit pas réellement d'une perte, chercher un `update`/`diff` négatif sur
`equipment`/`personnel` au même horodatage (sur la mère ou l'élément) — son absence
confirme le regroupement.

Le même schéma (élément qui finit par `location: null` sans perte associée) apparaît
plus largement pour signaler la fin du suivi de n'importe quel élément temporaire d'un
scénario (ex. une foule de manifestants qui se disperse) : ce n'est pas réservé aux
unités militaires démontées.

`orbat_lib.vanished_elements(units)` détecte ces éléments ; `timeline.py` les affiche
automatiquement en fin de sortie avec leur type déduit du `sidc`.

### `layers[].features[]` — géométrie cartographique

GeoJSON-like : `{geometry:{type, coordinates}, properties}`. Types vus : `Point`
(bases, aérodromes), `Polygon`/`MultiPolygon` (pays, zones pétrole/gaz). Décoratif/
contextuel, indépendant de l'arbre d'unités.

## Différences de versions observées

- `2.0.0` : `settings` contient `customSymbols` ; `statuses` prérempli possible.
- `1.1.0` : structure quasi identique, `settings.customSymbols` absent.
- `0.31.0` (ancien) : `side.units` peut porter un placeholder ; certaines unités sans
  `sidc` (toléré). Pas de `supplyCategories`.

Pour réécrire un fichier **import-ready**, viser `version: "2.0.0"` et l'enveloppe de
`assets/template.json`.
