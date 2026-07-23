# Format des sauvegardes SQF (export 3DEN) — référence

Sommaire :
1. Nature du fichier
2. Le langage SQF (rappels utiles à l'édition)
3. Positions et orientation
4. Anatomie d'une sauvegarde, bloc par bloc
5. Le tableau de loadout (getUnitLoadout / CBA_fnc_setLoadout)
6. Pièges d'édition

---

## 1. Nature du fichier

Une sauvegarde est un **script SQF plat**, produit par la fonction d'export
d'objets éditables de l'éditeur 3DEN (`BIS_fnc_3DENExportSQF` /
`BIS_fnc_exportEditableObjects`). Il s'exécute tel quel, ligne après ligne, dans
l'ordre. Aucun en-tête, aucun wrapper.

- **Encodage** : ASCII (sous-ensemble d'UTF-8), **sans BOM**.
- **Fins de ligne** : **CRLF** (`\r\n`).
- Chaque entité reçoit une variable **locale** numérotée réutilisée plus bas :
  `_group0`, `_object0`, `_marker`, `_waypoint`. **L'ordre et la numérotation
  sont structurants**, pas décoratifs.

La lib garantit un **round-trip octet pour octet** : `SqfSave.load(f).dumps()`
reproduit l'original à l'identique. Toute édition est chirurgicale (lignes
ciblées) ; le reste est préservé tel quel.

---

## 2. Le langage SQF (rappels utiles à l'édition)

- **Terminaison** : chaque expression finit par `;` (ou `,`), **pas** par le
  retour à la ligne. Le fichier tiendrait sur une seule ligne sans changer de sens.
- **Types** : Number, String `"..."`, Boolean, Array `[...]`, Code `{...}`, et
  types moteur (Object, Group, Side `west`/`civilian`, Marker...).
- **Variables** : un identifiant commençant par `_` est **local** au script.
  Tous les `_objectN`/`_groupN`/`_marker`/`_waypoint` sont locaux à l'exécution.
- **Opérateurs unaires** : consomment le 1er argument à droite. `count _arr select 2`
  = `(count _arr) select 2` → écrire `count (_arr select 2)`.
- **Précédence** : `* / % mod` > `+ -` > comparaisons > `&&` > `||`.
- **forEach** : `_x` = élément courant, `_forEachIndex` = index. Les exports
  utilisent `forEach` en lecture (`{... addMagazineTurret _x} forEach [...]`).
- **call vs spawn** : `call` = immédiat ; `spawn` = ordonnanceur (multi-frames).
  Les loadouts passent par un `BIS_fnc_addStackedEventHandler` sur `onEachFrame`
  qui s'auto-retire → applique le loadout **une frame après** la création de
  l'unité, puis se supprime.

---

## 3. Positions et orientation

Positions = tableaux `[x, y, z]`. X ouest→est, Y sud→nord, origine `[0,0]` en bas
à gauche de la carte.

- **ASL** (Above Sea Level) : z depuis le niveau de la mer. **Seul format
  absolu** — référentiel constant partout. Les exports utilisent `setPosASL`.
- **ATL** : z depuis le sol local (relatif ; z=0 sur une pente).
- **AGL** : mélange terre/mer.

Orientation : `setVectorDirAndUp [[vecDir],[vecUp]]` (tangage via `vectorDir`,
roulis via `vectorUp`). **`setDir` réinitialise `vectorUp` à `[0,0,1]`** — donc
sur un objet incliné, ne jamais « tourner » avec `setDir` ; agir sur les vecteurs.
Dans l'export : véhicules/statiques → `setVectorDirAndUp` ; infanterie (debout)
→ simple `setDir`.

---

## 4. Anatomie d'une sauvegarde, bloc par bloc

L'ordre général : **groupes → objets (véhicules puis unités) → marqueurs →
config des groupes / waypoints → moveIn* / attachTo**.

### 4.1 Groupes
```
_group0 = createGroup [west, true];
```
`side` ∈ `west` / `east` / `independent` / `civilian`. Simples conteneurs.

### 4.2 Véhicules / statiques
```
_object2 = createVehicle ["FR2035_Truck_01_fuel_F", [0,0,0], [], 0, "CAN_COLLIDE"];
_object2 setVectorDirAndUp [[...],[...]];
_object2 setPosASL [x,y,z];
_object2 setFuel 0.989152;                         (si motorisé)
[_object2, ["CE",1], [...], true] call BIS_fnc_initVehicle;   (livrée + animations)
clearItemCargoGlobal _object2; clearWeaponCargoGlobal ...;     (purge coffre)
{_object2 addItemCargoGlobal _x} forEach [["ACE_rope12",1]];   (contenu)
{_object2 removeMagazineTurret (_x select [0,2])} forEach magazinesAllTurrets _object2;
{_object2 addMagazineTurret _x} forEach [[...]];               (chargeurs tourelle)
_object0 setPylonLoadOut [1, "PylonMissile_...", false, [0]]; _object0 setAmmoOnPylon [1, 1];
_object41 setDamage 0.0714285;                     (usure globale 0–1)
{_object228 setHitIndex [_forEachIndex, _x, false]} forEach [0,0,0.08,...];  (usure par PdV)
```
`setPylonLoadOut [pylonID, magazine, forced, turretPath]` puis `setAmmoOnPylon`.

### 4.3 Unités (infanterie)
```
_object1 = _group0 createUnit ["C_man_shorts_2_F", [0,0,0], [], 0, "CAN_COLLIDE"];
_object1 setPosASL [x,y,z]; _object1 setDir 40.5; _object1 setRank "PRIVATE";
_object1 setSkill 0.5; _object1 setUnitPos "Auto";
_group0 selectLeader _object1;                     (leader du groupe)
['_object1_nextFrameHandle','onEachFrame',{ params ["_unit"];
    [_unit, [ ...tableau getUnitLoadout... ]] call CBA_fnc_setLoadout;   (si loadout custom)
    _unit call BIN_fnc_CBRNHoseInit;
    [...] call BIS_fnc_removeStackedEventHandler; }, [_object1]] call BIS_fnc_addStackedEventHandler;
```

### 4.4 Marqueurs (présents dans les sauvegardes de zone, pas dans les FOB seuls)
```
_marker = createMarkerLocal ["fobmarker0", [x,y,z]];
_marker setMarkerTypeLocal "b_hq"; _marker setMarkerShapeLocal "ICON";
_marker setMarkerDirLocal 0; _marker setMarkerSizeLocal [1.5,1.5];
_marker setMarkerTextLocal "FOB Alpha"; _marker setMarkerBrushLocal "Solid";
_marker setMarkerColorLocal "ColorYellow"; _marker setMarkerAlpha 1;
```
Certains noms sont **systèmes** (ex. `ghost_spot`, `opfor_airspawn`, `fobmarker0`)
et servent de clés à la logique de mission → attention lors des fusions (§6).

### 4.5 Config de groupe + waypoints (fin de fichier)
```
_group0 setFormation "WEDGE"; _group0 setBehaviour "CARELESS";
_group0 setCombatMode "BLUE"; _group0 setSpeedMode "NORMAL";
_waypoint = [_group0, 0];             (1er waypoint = celui cree avec le groupe)
_waypoint setWaypointPosition [[x,y,z], -1]; _waypoint setWaypointType "MOVE"; ...
_waypoint = _group0 addWaypoint [[0,0,0], -1];   (waypoints suivants)
...
_group0 setCurrentWaypoint [_group0, 1];
```

### 4.6 Placement et assemblage
```
_object0 moveInAny _object2; _object1 moveInGunner _object2;
_object4 moveInDriver _object3; _object5 moveInTurret [_object3, [0]];
_object245 attachTo [_object229, [5.6,1.8,0.3]];   (objets composites)
```

---

## 5. Le tableau de loadout (getUnitLoadout / CBA_fnc_setLoadout)

Les gros tableaux imbriqués dans `CBA_fnc_setLoadout` sont au **format Unit
Loadout** de `getUnitLoadout`, dans cet ordre :
arme principale (accessoires + chargeur) · arme secondaire · arme de poing ·
uniforme (+ contenu) · gilet (+ contenu) · sac à dos (+ contenu) · casque ·
lunettes · objets liés (carte, GPS, radio, boussole, montre, NVG) · binoculaire.

Chaque conteneur = `["classe_conteneur", [[ "item", quantité, munitions ], ...]]`.
Éditer le **contenu** des sous-tableaux, jamais la **structure** `[classe,[...]]`.

---

## 6. Pièges d'édition

1. **Ne jamais renuméroter à l'aveugle.** Un `_objectN` supprimé mais cité par un
   `moveIn*`/`attachTo`/`selectLeader`/`setCurrentWaypoint` casse l'exécution.
   → `remove_object()` supprime le bloc **et** toutes les références.
2. **Encodage** : réécrire en ASCII + CRLF, sans BOM (la lib s'en charge).
3. **z ASL** : un z faux fait flotter/enterrer l'objet. Pour tourner un véhicule,
   agir sur `setVectorDirAndUp`.
4. **Ordre** : groupes avant unités ; objets avant leurs `attachTo`/`moveIn`.
5. **Loadout/cargo** : modifier le contenu, pas la structure.
6. **Fusion** : `renumber()` décale les `_objectN`/`_groupN` et suffixe les noms
   de marqueurs pour éviter les collisions. **Mais** les marqueurs *systèmes*
   (clés de mission) suffixés ne seront plus reconnus par la logique de mission —
   pour une fusion propre, dédoublonner les marqueurs systèmes à la main.
7. Après édition : `check()` doit être vide, et toujours produire un **nouveau
   fichier** dans `/mnt/user-data/outputs/` (jamais écraser l'upload).
