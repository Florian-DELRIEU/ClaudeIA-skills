# Liens et mécaniques (modifiers, conditions, contraintes)

C'est la partie la plus puissante et la plus fragile du format. Tous les attributs comptent.

Table des matières :
1. Liens (entryLink, infoLink, categoryLink, catalogueLink, publicationLink)
2. Contraintes (constraint)
3. Modifiers
4. Conditions et groupes de conditions
5. Repeats
6. Vocabulaire des attributs (type, field, scope, childId, affects…)
7. Recettes prêtes à l'emploi

---

## 1. Liens

Un lien pointe vers une entité **partagée** (dans les listes `shared*` du catalogue, ou importées du
game system). Le `targetId` DOIT résoudre.

### entryLink — lier une selectionEntry/-Group partagée dans une unité
```xml
<entryLink import="true" name="Bolt pistol" hidden="false" type="selectionEntry"
           id="ID_LIEN" targetId="ID_CIBLE">
  <constraints>...</constraints>   <!-- optionnel : limiter la sélection -->
  <modifiers>...</modifiers>       <!-- optionnel : modifier la cible dans ce contexte -->
  <categoryLinks>...</categoryLinks>
</entryLink>
```
`type` = `selectionEntry` ou `selectionEntryGroup` (doit matcher la nature de la cible).

### infoLink — lier une règle/un profil/un infoGroup partagé
```xml
<infoLink name="Feel No Pain" hidden="false" type="rule" id="ID_LIEN" targetId="ID_REGLE"/>
```
`type` = `rule` | `profile` | `infoGroup`. Sert à réutiliser une règle commune sans la recopier.

### categoryLink — affecter une catégorie (voir aussi structure.md §5)
```xml
<categoryLink id="ID" name="HQ" hidden="false" targetId="ID_CATEGORIE" primary="true|false"/>
```

### catalogueLink — importer un catalogue-bibliothèque
```xml
<catalogueLink id="ID" name="Bibliothèque Armes Communes" type="catalogue" targetId="ID_CATALOGUE"/>
```
Rend les entrées partagées d'un autre catalogue (souvent `library="true"`) disponibles ici.

### publicationLink — (2.03+) lier une publication partagée. Rare ; référencer via `publicationId`.

---

## 2. Contraintes (constraint)

Bornes min/max sur une valeur agrégée. Élément sans enfant.
```xml
<constraint type="min|max" value="1" field="selections" scope="parent"
            shared="true" id="ID" percentValue="false"
            includeChildSelections="false" includeChildForces="false"/>
```
- `type` : `min` (borne basse inclusive) ou `max` (borne haute inclusive).
- `value` : entier (ou décimal). `-1` = illimité (convention pour un `max` « pas de limite »).
- `field` : ce qu'on compte — `selections` (nombre de sélections) ou un `costType` (ex. `points`),
  ou `forces` (nombre de détachements, au niveau roster).
- `scope` : où sommer — `parent`, `self`, `force`, `roster`, `primary-catalogue`,
  `primary-category`, ou l'`id` d'un ancêtre/catégorie/force précis.
- `shared` : `true` = somme toutes les instances de l'entrée partagée ; `false` = par instance de lien.
- `includeChildSelections` : inclure aussi les sélections descendantes.
- `includeChildForces` : inclure aussi les détachements descendants.
- `percentValue` : `true` = `value` interprétée en pourcentage.

**Recette « choisir exactement 1 »** dans un `selectionEntryGroup` : deux contraintes, `min=1` et
`max=1`, `field="selections"`, `scope="parent"`. **« 0 ou 1 »** : seulement `max=1`.

---

## 3. Modifiers

Un modifier change une propriété de son parent (ou de la cible du lien parent), ou la `value` d'une
contrainte du parent. Peut être conditionnel (enfants `conditions`/`conditionGroups`) et/ou répété
(enfants `repeats`).
```xml
<modifiers>
  <modifier type="increment|decrement|set|append" field="CIBLE" value="VALEUR" [join=", "] [scope="..."] [affects="..."]>
    <repeats>...</repeats>            <!-- optionnel : applique N fois -->
    <conditions>...</conditions>      <!-- optionnel : prérequis (ET implicite si plusieurs) -->
    <conditionGroups>...</conditionGroups>  <!-- optionnel : logique ET/OU -->
  </modifier>
</modifiers>
```
- `type` :
  - `increment` / `decrement` — `field` numérique, ajoute/retire `value`.
  - `set` — fixe `field` à `value` (marche aussi pour `name`, `hidden`, une caractéristique…).
  - `append` — `field` textuel, concatène `value` (séparateur `join`, ex. `", "`).
- `field` : la propriété modifiée. Peut être : le mot-clé `name`, `hidden`, `category`, le `costType`
  (ex. `points` pour changer un coût), l'**`id` d'une contrainte** (pour bouger sa borne), ou l'`id`
  d'une caractéristique (pour modifier une stat).
- `affects` (avancé, ex. modifier une caractéristique d'un profil ciblé) : chemin de type
  `self.entries.profiles.Ranged Weapons` (cible les profils Ranged Weapons de l'entrée).
- `scope` : contexte d'évaluation (ex. `upgrade`, `self`, `parent`).

Exemple (change un coût si une option est prise) :
```xml
<modifier type="increment" field="points" value="5">
  <conditions>
    <condition type="atLeast" value="1" field="selections" scope="self"
               childId="ID_OPTION" shared="true" includeChildSelections="true"/>
  </conditions>
</modifier>
```
Exemple (rendre une entrée visible/masquée) : `<modifier type="set" field="hidden" value="false">…`.

---

## 4. Conditions et groupes de conditions

### condition — un test unique (sans enfant)
```xml
<condition type="TEST" value="1" field="selections" scope="roster"
           childId="ID_CIBLE" shared="true"
           percentValue="false" includeChildSelections="true" includeChildForces="true"/>
```
- `type` (opérateurs, camelCase) : `atLeast`, `atMost`, `lessThan`, `greaterThan`, `equalTo`,
  `notEqualTo`, `instanceOf`, `notInstanceOf`.
- `field` : `selections` (ou `forces`, ou un costType).
- `scope` : `parent`, `self`, `force`, `roster`, `primary-catalogue`, un `id` d'ancêtre/catégorie/force.
- `childId` : **quoi** compter/tester — l'`id` d'une categoryEntry, d'une selectionEntry, d'une force,
  ou un mot-clé (`unit`/`model`/`upgrade`). Doit résoudre (sauf mots-clés). Pour `instanceOf`,
  `childId` est le type/catégorie testé.
- `value` : seuil comparé (sans effet pour `instanceOf`/`notInstanceOf`).

Plusieurs `<condition>` sœurs directement sous un `<modifier>` = **ET** implicite.

### conditionGroup — logique explicite
```xml
<conditionGroups>
  <conditionGroup type="and|or">
    <conditions>
      <condition .../>
      <condition .../>
    </conditions>
    <conditionGroups>              <!-- imbrication possible -->
      <conditionGroup type="or">...</conditionGroup>
    </conditionGroups>
  </conditionGroup>
</conditionGroups>
```
`type="and"` : vrai si TOUS les enfants sont vrais. `type="or"` : vrai si AU MOINS UN l'est.

---

## 5. Repeats

Fait appliquer un modifier **plusieurs fois** selon un décompte (typique pour incrémenter un coût par
tranche). Enfant d'un `<modifier>`.
```xml
<repeats>
  <repeat repeats="1" value="1" field="selections" scope="self"
          childId="ID_CIBLE" shared="true" roundUp="false"
          percentValue="false" includeChildSelections="true" includeChildForces="true"/>
</repeats>
```
- `repeats` : nombre d'applications du modifier par tranche atteinte.
- `value` : taille de la tranche comparée au décompte de `field`.
- `roundUp` : arrondi supérieur des tranches partielles.

Exemple « +10 pts par tranche de 5 figurines » : modifier `increment` `points` `value=10` avec un
`repeat` `field=selections` `value=5` `childId=<modèle>`.

---

## 6. Mémo des attributs transverses

| Attribut | Valeurs | Rôle |
|---|---|---|
| `type` (constraint) | `min`, `max` | borne |
| `type` (modifier) | `increment`, `decrement`, `set`, `append` | opération |
| `type` (condition) | `atLeast`, `atMost`, `lessThan`, `greaterThan`, `equalTo`, `notEqualTo`, `instanceOf`, `notInstanceOf` | test |
| `type` (link) | `selectionEntry`, `selectionEntryGroup`, `rule`, `profile`, `infoGroup`, `catalogue` | nature de la cible |
| `field` | `selections`, `forces`, `<costTypeId>`, `name`, `hidden`, `<constraintId>`, `<characteristicId>` | quoi compter/modifier |
| `scope` | `self`, `parent`, `force`, `roster`, `primary-catalogue`, `primary-category`, `<id ancêtre>` | où évaluer |
| `childId` | `<id>` ou `unit`/`model`/`upgrade` | quoi cibler dans le scope |
| `shared` | `true`/`false` | somme globale vs par instance |
| `includeChildSelections` / `includeChildForces` | `true`/`false` | inclure descendants |
| `percentValue` | `true`/`false` | valeur en % |

---

## 7. Recettes prêtes à l'emploi

**« 1 modèle max de ce type dans le détachement »**
```xml
<constraint type="max" value="1" field="selections" scope="force" shared="true"
            includeChildSelections="true" includeChildForces="true" id="NOUVEL_ID"/>
```

**« Cette option coûte +15 pts »** (modifier sur la selectionEntry de l'option)
```xml
<costs><cost name="pts" typeId="points" value="15"/></costs>
```

**« Débloquer l'unité seulement si le Warlord X est pris »** (masquer sinon)
```xml
<modifiers>
  <modifier type="set" field="hidden" value="true">
    <conditions>
      <condition type="lessThan" value="1" field="selections" scope="roster"
                 childId="ID_WARLORD_X" shared="true"
                 includeChildSelections="true" includeChildForces="true"/>
    </conditions>
  </modifier>
</modifiers>
```

**« Taille d'unité 5–10, +X pts par tranche »** : contrainte `min=5`/`max=10` sur le groupe de
modèles + modifier `increment points` avec un `repeat` par tranche (voir §5).

> Toujours terminer par `scripts/bs_validate.py` : le `childId`/`targetId` de chaque recette doit
> pointer vers un ID réel du fichier (ou d'un autre fichier du repo).
