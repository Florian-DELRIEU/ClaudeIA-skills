# Format ORBAT xlsx — ODIN (TRADOC G2) / JTDS

Format tableur des ordres de bataille publiés par **ODIN** (*Operational
Environment Data Integration Network*, TRADOC G2). C'est l'équivalent
« auteur » du XML **JTDS OBSV4.2** : le xlsx est *compact et templaté*, le XML
est le même ORBAT *entièrement déplié*.

> **Grammaire vérifiée à 100 %.** Reverse-engineerée sur la paire de référence
> `JRTC ARIANA-17 IFV DIV` (xlsx + XML du même ORBAT). Après expansion, le xlsx
> reproduit le XML **exactement** : 3160 unités, 44010 entités (8977 plateformes,
> 5537 remorquées, 301 emports, 29195 personnels), 5838 `TowedBy`, 19474 `Crew`,
> 9721 `Passenger`. Une comparaison structurelle récursive (nom, échelon,
> équipement, personnel, à chaque nœud des 3160 unités) donne une identité
> parfaite. Outillage : `scripts/xlsx_orbat.py`.

---

## 1. Structure du classeur

| Feuille | Rôle |
|---|---|
| **`UNIT INFO`** | l'**ossature** : une ligne par unité nommée de l'ORBAT |
| *N feuilles « template »* | la **composition interne réutilisable** (une par type d'unité) |

L'ORBAT complet = instancier chaque ligne `T` de `UNIT INFO` avec la feuille
template qu'elle nomme. Un même template est réutilisé par plusieurs unités
(ex. `IFV BN` sert 10 fois) : c'est tout l'intérêt du format.

---

## 2. Feuille `UNIT INFO`

En-tête (ligne 1) : `TYPE | NAME | PARENT | UIC | ECHELON | UNIT CLASS | TEMPLATE | 2525C`

| Colonne | Contenu |
|---|---|
| `TYPE` | `U` ou `T` — voir ci-dessous |
| `NAME` | nom de l'unité, **unique** dans `UNIT INFO` |
| `PARENT` | `NAME` de l'unité mère, ou **`TOP`** pour la racine |
| `UIC` | identifiant d'unité (ex. `AR834`) |
| `ECHELON` | mot anglais : `Team`, `Squad`, `Section`, `Platoon`, `Company`, `Battalion`, `Brigade`, `Division`… |
| `UNIT CLASS` | classe doctrinale ODIN (ex. `MECH INF DIV`) — clé vers `UnitClassList` du XML |
| `TEMPLATE` | nom de la feuille template à instancier |
| `2525C` | symbole MIL-STD-2525C, **15 caractères** |

### `U` vs `T` — distinction centrale

- **`T` (templated)** : la composition interne de l'unité vient de la feuille
  nommée en `TEMPLATE`. C'est le cas général (92 lignes sur 100 dans la réf.).
- **`U` (unit / conteneur)** : l'unité n'a **pas** de composition organique
  propre ; ses enfants sont **d'autres lignes de `UNIT INFO`** qui la citent en
  `PARENT`. Typiquement la division et ses brigades.

> ⚠ **Sur une ligne `U`, la colonne `TEMPLATE` n'est qu'une étiquette
> doctrinale, jamais une feuille à étendre.** Dans la référence, les lignes `U`
> portent `OPFOR MECH BDE`, `OPFOR ARM BDE`… qui **n'existent pas** comme
> feuilles. Seules les lignes `T` s'étendent. Étendre les `U` sur-compterait
> tout l'ORBAT.

---

## 3. Feuilles template

**Pas d'en-tête.** La colonne A porte le type de ligne ; le sens des colonnes
suivantes en dépend.

### `U` — unité
`U | NAME | PARENT | UIC | ECHELON | UNIT CLASS | 2525C`

- La **première** ligne `U` a `PARENT = TOP` : **elle *est* l'unité qui
  référence le template** (ce n'est pas une sous-unité à créer). Ses attributs
  ne sont pas ré-appliqués — `UNIT INFO` fait autorité.
- Les autres lignes `U` sont des sous-unités ; `PARENT` cite un `NAME` **de la
  même feuille**.

### `E` — plateforme / véhicule
`E | ID | PARENT (nom d'unité) | CLASSE`

### `W` — remorqué (*towed*)
`W | ID | PARENT (ID d'un E) | CLASSE` — remorque, pièce tractée…

### `M` — monté / emporté (*mounted*)
`M | ID | PARENT (ID d'un E) | CLASSE` — ex. drones `ZALA 421 08M UAV` sur leur
véhicule lanceur.

### `P` — personnel
`P | ID | PARENT (ID d'un E) | RÔLE | CLASSE`

- `RÔLE` = **`C`** (équipage → `CrewList` du XML) ou **`P`** (passager →
  `PassengerList`).
- La `CLASSE` décrit le soldat par son armement (`GL RFL AK74 5.45MM`,
  `GL MEDIC`, `GL RTO`…) : **une ligne `P` = une personne**, pas une arme.
- Dans la référence, **tout `P` est rattaché à un `E`** (jamais à un `W`/`M`, ni
  directement à une unité) : le format n'exprime pas de fantassin débarqué.

### Identifiants
`E`, `W`, `M` et `P` partagent **un seul espace d'IDs séquentiel par feuille**
(entiers, croissants, uniques). Une ligne `W`/`M`/`P` référence toujours un ID
**défini plus haut** dans la feuille.

---

## 4. ⚠ Deux pièges qui produisent des erreurs silencieuses

### 4.1 Les noms d'unités ne sont PAS uniques dans une feuille — résolution séquentielle

Une feuille peut déclarer plusieurs unités homonymes sous des parents
différents. Dans `IFV BN` : `SPT TM 1` existe sous `HQ 1 CO` **et** sous
`HQ TANK CO` ; `1 SEC 1` existe **trois** fois.

**Règle : la feuille se lit de haut en bas ; une référence par nom (le `PARENT`
d'un `U`, ou le `PARENT` d'un `E`) désigne la définition `U` la plus récemment
rencontrée portant ce nom.**

Vérifié contre le XML : `SPT TM 1` sous `HQ 1 CO` a **0 entité**, celui sous
`HQ TANK CO` en a **24**. Les lignes `E` d'une unité suivent immédiatement sa
déclaration.

> Un parseur qui indexe les unités par nom **fusionne silencieusement les
> homonymes** et sur-compte le matériel (constaté : +1970 entités, soit +4,5 %,
> sans la moindre erreur levée). `xlsx_orbat.py` fait la résolution séquentielle.

### 4.2 `ECHELON` et l'échelon du code 2525C divergent volontairement

Le caractère **12** du code 2525C est l'échelon du *symbole*
(`A` équipe, `B` escouade, `C` section, `D` peloton, `E` compagnie,
`F` bataillon, `G` régiment, `H` brigade, `I` division, `J` corps, `K` armée).

Il **ne correspond pas toujours** à la colonne `ECHELON`. Dans la référence,
`Company` apparaît avec `C`, `E`, `F` **et** `H` ; `Section` avec `B`, `C`, `D`,
`E`, `F`. C'est **voulu** : le symbole est souvent hérité de la `UNIT CLASS`.

> **Ne jamais « corriger » l'un d'après l'autre.** Conserver les deux tels
> quels. La colonne `ECHELON` fait autorité pour l'échelon réel de l'unité.

---

## 5. Le code 2525C (15 caractères)

`S N G P U C I Z - - - I X C G`

| Pos | Champ | Dans la référence |
|---|---|---|
| 1 | schéma de codage | `S` (warfighting) |
| 2 | **affiliation** | `N` neutre (`F` ami, `H` hostile, `U` inconnu…) |
| 3 | dimension de bataille | `G` (ground) |
| 4 | statut | `P` (présent) |
| 5-10 | **function ID** | `UCIZ--` = infanterie mécanisée |
| 11 | modificateur 1 | `-` |
| 12 | **échelon du symbole** | `I` = division |
| 13-14 | code pays | toujours `XC` ici |
| 15 | ordre de bataille | `G` |

---

## 6. Correspondance avec le XML JTDS OBSV4.2

| xlsx | XML |
|---|---|
| ligne `U` (`UNIT INFO` ou template) | `<Unit>` (`Name`, `Echelon`, `ClassName`, `MilStd2525CCode`, `UnitSuperior`) |
| ligne `E` | `<EntityComposition>` + `<Platform>` |
| ligne `W` / `M` | `<EntityComposition>` + `<TowedBy>` vers le porteur |
| ligne `P` rôle `C` | `<EntityComposition>` + `<LifeForm/>`, cité dans `<CrewList>` du porteur |
| ligne `P` rôle `P` | idem, cité dans `<PassengerList>` |
| `UNIT CLASS` | `ClassData/UnitClassList/UnitClass/AggregateName` |
| classe d'un `E`/`W`/`M`/`P` | `ClassData/EntityCompositionClassList/EntityCompositionClass/Name` |

Le XML est **déplié** : chaque instanciation de template y devient des `<Unit>`
distinctes (mêmes noms, `LvcId` différents). Le xlsx ne stocke pas les `LvcId` —
un aller-retour xlsx → XML les régénère.

---

## 7. Conversion vers orbat-mapper.app — ce qui se perd

`xlsx_orbat.py tojson` produit un scénario orbat-mapper valide, mais la
conversion est **volontairement lossy** :

| Élément ODIN | Devenir |
|---|---|
| unité | `Unit` récursive avec `sidc` APP-6D (jamais de `Group` imbriqué — cf. `format.md`) |
| `E` / `W` / `M` | `equipment`, **agrégés par classe** sur l'unité porteuse |
| `P` | `personnel`, agrégés par classe |
| rôle `C` / `P` (équipage vs passager) | **perdu** — non représentable |
| lien porteur → remorque / emport | **perdu** |
| `UIC`, `UNIT CLASS`, 2525C d'origine, échelon ODIN | conservés dans la `description` de l'unité |

### Échelon ODIN → APP-6D (table sûre)
`Team`/`Crew` → `11` · `Squad` → `12` · **`Section` → `13`** · **`Platoon` → `14`** ·
`Company`/`Battery`/`Troop` → `15` · `Battalion`/`Squadron` → `16` ·
`Regiment`/`Group` → `17` · `Brigade` → `18` · `Division` → `21` · `Corps` → `22` ·
`Army` → `23`

> ⚠ Le vocabulaire ODIN est **anglais US** : `Section` = section US = `13`,
> `Platoon` = peloton = `14`. En français, « Section » = peloton = `14` : ne pas
> traduire avant de convertir.

### Function ID → entité APP-6D
Table `FUNCTION_MAP` dans `xlsx_orbat.py`, **dérivée et non inventée** : entités
documentées dans `sidc.md` (autorité) + concordance des noms d'unités ODIN avec
les exemples de `sidc_dictionary.json`, en n'utilisant que les **noms non
ambigus** (les génériques `HQ`, `CMD SEC`, `1 PLT` polluent le vote et sont
écartés).

Couverture : **56 familles sur 56** sur le fichier de référence — plus aucune
retombée sur `000000`. Toute famille absente d'un futur fichier tombera sur
l'entité générique `000000` et sera **listée dans le rapport de conversion** :
la signaler à Florian plutôt que de deviner.

⚠️ Deux mappings reposent sur une base plus faible que le reste, à confirmer :
`UCAWW-` (*AMPHIB PLT* → `120300`, entité standard APP-6D absente du dictionnaire)
et `UUMRS-` (noms d'unités entièrement génériques → rattaché à la famille `UUM`).

---

## 8. Outillage — `scripts/xlsx_orbat.py`

```bash
python xlsx_orbat.py read     F.xlsx              # résumé + compteurs après expansion
python xlsx_orbat.py tree     F.xlsx [--unit NOM] [--depth N]
python xlsx_orbat.py agg      F.xlsx [--unit NOM] [--what equipment|personnel]
python xlsx_orbat.py validate F.xlsx              # intégrité référentielle
python xlsx_orbat.py tojson   F.xlsx OUT.json [--side NOM]
```

API : `load` · `expand` · `agg_equipment` / `agg_personnel` / `counts` · `save` ·
`new_workbook` / `add_unit` / `remove_unit` / `TemplateBuilder` · `validate` ·
`to_mapper_json`.

`TemplateBuilder` gère la numérotation séquentielle des IDs :

```python
tb = TemplateBuilder("IFV BN", echelon="Battalion", unit_class="MECH INF BN",
                     sidc2525="SNGPUCIZ---FXCG")
tb.unit("HQ", parent="IFV BN", echelon="Platoon", ...)
v = tb.platform("BMP 2 IFV", unit="HQ")
tb.crew(v, "GL RFL AK74 5.45MM")
tb.passenger(v, "GL SA-18 GROUSE 72MM")
tb.towed(v, "TRL CGO .5T TO 2T")
tb.mounted(v, "ZALA 421 08M UAV")
wb.templates["IFV BN"] = tb.rows
```

**Toujours lancer `validate` après une édition** (noms dupliqués, parents
inconnus, templates manquants, IDs dupliqués ou référencés avant définition,
feuilles mortes).
