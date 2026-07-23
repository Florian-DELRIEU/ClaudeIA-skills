---
name: sqf
description: Lecture, analyse, édition et fusion des sauvegardes Arma 3 au format SQF (export « Export to SQF » de l'éditeur 3DEN / BIS_fnc_3DENExportSQF) — fichiers custom_fob.sqf, custom_save_*.sqf, custom_others_*.sqf d'une mission persistante (FOB, compositions, parcs de véhicules, unités, marqueurs). Déclencher IMPÉRATIVEMENT dès que Florian tape /sqf, fournit un .sqf de sauvegarde/composition, mentionne « sauvegarde SQF », « export 3DEN », « mon FOB », « ma save Arma », ou demande de lire/compter/inventorier/modifier/réparer/fusionner véhicules, unités, marqueurs, positions, loadouts ou cargos. Déclencher aussi pour des demandes courtes (« combien de chars dans ce FOB ? », « fais le plein et répare tout », « supprime cet objet », « fusionne alpha et bravo », « inventaire du parc »). Couvre aussi le langage SQF lui-même (syntaxe, positions ASL/ATL, orientation par vecteurs). Peut s'enchaîner avec /orbat et /nomenclature-v4.
---

# Sauvegardes SQF Arma 3 — export 3DEN

Outillage pour lire et éditer les sauvegardes SQF (« Export to SQF » de l'éditeur
3DEN) **sans casser leur réexécution dans le jeu**. Détails complets du format
dans `reference/format.md` — le lire avant toute édition non triviale ou dès
qu'un élément paraît ambigu (loadout, waypoint, marqueur système, orientation).

## Règles absolues

1. **Fidélité round-trip.** La lib garde le fichier comme une liste de lignes
   brutes et n'édite que des lignes ciblées ; `load(f).dumps()` reproduit
   l'original **octet pour octet** (vérifié sur les fichiers réels de Florian).
   Ne jamais réécrire un bloc entier à la main.
2. **Toujours travailler sur une COPIE.** Les uploads sont en lecture seule.
   Utiliser `SqfSave.open_copy(src, dst)` (copie puis ouvre la copie), ou charger
   avec `SqfSave.load` (lecture seule) et écrire ailleurs. Ne jamais écraser
   l'upload.
3. **Encodage préservé : ASCII + CRLF, sans BOM.** La lib s'en charge ; ne pas
   parser à la main avec `split("\n")` ni réenregistrer en LF.
4. **Numérotation structurante.** Les handles `_objectN`/`_groupN` sont
   référencés ailleurs (`moveIn*`, `attachTo`, `selectLeader`,
   `setCurrentWaypoint`). Ne jamais renuméroter à l'aveugle. Pour retirer une
   entité, utiliser `remove_object()` qui supprime le bloc **et** ses références.
5. **Positions en ASL.** `[x, y, z]` au-dessus du niveau de la mer. Un z faux
   fait flotter/enterrer l'objet. Pour réorienter un véhicule, agir sur
   `setVectorDirAndUp`, pas `setDir` (qui remet `vectorUp` à `[0,0,1]`).
6. **Après toute édition** : `check()` doit renvoyer une liste vide (aucune
   référence pendante, brackets équilibrés). Sinon, ne pas livrer et diagnostiquer.
7. **Livraison** : toujours produire le fichier édité dans
   **`/mnt/user-data/outputs/`** (nouveau nom, extension `.sqf`), puis rappeler à
   Florian de le replacer dans le dossier de sauvegarde de sa mission.

## Workflow standard

```bash
cd scripts

# Inspection (lecture seule, sûr directement sur l'upload)
python3 sqf_info.py save.sqf                 # vue d'ensemble
python3 sqf_info.py save.sqf --inventory     # comptage par classe (véhicules / unités)
python3 sqf_info.py save.sqf --vehicles      # liste des véhicules (classe, pos, fuel, dmg)
python3 sqf_info.py save.sqf --units         # liste des unités
python3 sqf_info.py save.sqf --objects 30    # 30 premiers objets
python3 sqf_info.py save.sqf --markers 40    # 40 premiers marqueurs
python3 sqf_info.py save.sqf --check         # contrôle de cohérence
```

## Édition en Python

```python
import sys; sys.path.insert(0, "scripts")
from sqf_lib import SqfSave

# 1) Toujours partir d'une copie (jamais l'upload d'origine)
s = SqfSave.open_copy("save.sqf", "/mnt/user-data/outputs/save_edit.sqf")

# --- Lecture ---
print(s.summary())                       # compteurs (groupes, objets, véhicules, unités, marqueurs...)
for o in s.objects():                    # id, kind, classname, group, pos, fuel, damage
    print(o["id"], o["kind"], o["classname"], o["pos"])
print(s.classname_counts("vehicle"))     # Counter des classes de véhicules
print(s.marker_names())

# --- Éditions courantes ---
s.refuel_all(1.0)          # plein pour tous les véhicules motorisés
s.repair_all()             # setDamage -> 0 et setHitIndex -> 0 partout
s.set_fuel(2, 0.5)         # carburant d'un objet précis
s.set_damage(41, 0.0)      # réparer un objet précis
s.set_pos(12, [26160.2, 21041.5, 14.1])   # repositionner (ASL)
s.remove_object(2)         # supprime l'objet ET toutes ses références (moveIn/attach/...)

# --- Contrôle puis sauvegarde ---
assert not s.check(), s.check()
s.save("/mnt/user-data/outputs/save_edit.sqf")
```

## Fusionner deux sauvegardes

```python
from sqf_lib import SqfSave
a = SqfSave.load("custom_save_alpha.sqf")
b = SqfSave.load("custom_save_bravo.sqf")

# Décaler les handles de b pour éviter les collisions, puis concaténer
b.renumber(obj_offset=max(a.object_ids())+1,
           grp_offset=max(a.group_ids())+1,
           marker_suffix="_b")
a.concat(b)
assert not a.check()
a.save("/mnt/user-data/outputs/custom_merged.sqf")
```

⚠️ Les **marqueurs systèmes** (ex. `fobmarker0`, `ghost_spot`, `opfor_airspawn`)
servent de clés à la logique de mission ; suffixés par la fusion, ils ne seront
plus reconnus. Pour une fusion propre, prévenir Florian et dédoublonner ces
marqueurs à la main (garder une seule occurrence, ou renommer sciemment).

## Ce que la lib sait faire (et ses limites)

**Solide** : inventaire/comptage, plein & réparation de masse, réparation/plein
ciblés, repositionnement, suppression avec nettoyage automatique des références,
fusion avec renumérotation, contrôle de cohérence, round-trip parfait.

**À faire à la main (guidé, en s'appuyant sur `reference/format.md`)** : édition
fine d'un **loadout** d'unité (tableau `getUnitLoadout`) ou d'un **cargo** de
véhicule, ajout d'un véhicule/unité de zéro, édition de pylônes/waypoints. Ces
opérations touchent à des structures imbriquées : lire d'abord la §5 (loadout)
ou la §4 (blocs) de la référence, puis modifier le contenu des sous-tableaux
sans altérer leur structure `[classe, [contenu]]`.

## Rappel de mise à jour

Skill jamais mis à jour sans que Florian tape explicitement `/maj`. À ce moment :
éditer les fichiers → zipper le dossier → réuploader.
