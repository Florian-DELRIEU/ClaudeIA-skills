# Référence structure BSData (BattleScribe 2.03)

Table des matières :
1. Racines et namespaces
2. Propriétés communes (id, name, hidden, publication…)
3. Arbre du game system (.gst)
4. Arbre du catalogue (.cat)
5. Briques de base (selectionEntry, group, profile, rule, category, force…)
6. Roster (.ros)
7. Index (index.xml) et repository (.bsr)
8. Note sur l'ordre des éléments

---

## 1. Racines et namespaces

Le namespace par défaut (`xmlns`) DOIT correspondre au type de fichier, sinon le logiciel ne
reconnaît pas le fichier.

| Type | Élément racine | `xmlns` |
|---|---|---|
| Game system | `gameSystem` | `http://www.battlescribe.net/schema/gameSystemSchema` |
| Catalogue | `catalogue` | `http://www.battlescribe.net/schema/catalogueSchema` |
| Roster | `roster` | `http://www.battlescribe.net/schema/rosterSchema` |
| Index | `dataIndex` | `http://www.battlescribe.net/schema/dataIndexSchema` |

Déclaration XML en tête (toujours) : `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>`

### Attributs de la racine `gameSystem`
`id`, `name`, `revision` (entier, à incrémenter à chaque publication), `battleScribeVersion` (`2.03`),
`authorName`, `authorContact`, `authorUrl`, `type="gameSystem"` (optionnel).

### Attributs de la racine `catalogue`
`id`, `name`, `revision`, `battleScribeVersion` (`2.03`), `library` (`true`/`false` — un catalogue
« bibliothèque » est importable par d'autres catalogues mais pas jouable seul), **`gameSystemId`**
(= `id` du `.gst` cible, OBLIGATOIRE), `gameSystemRevision`, `authorName`, `authorContact`,
`authorUrl`.

### Attributs de la racine `roster`
`id`, `name`, `battleScribeVersion`, **`gameSystemId`**, `gameSystemName`, `gameSystemRevision`.

---

## 2. Propriétés communes

- **`id`** — identifiant unique. Format usuel : `xxxx-xxxx-xxxx-xxxx` (groupes hexadécimaux) ou UUID
  `8-4-4-4-12`. En pratique « n'importe quel texte unique ». Ne JAMAIS dupliquer un `id`.
- **`name`** — nom affiché (non unique).
- **`hidden`** — `true`/`false`. Une entrée `hidden="true"` sélectionnée provoque une erreur dans le
  roster (utilisé volontairement, piloté par des modifiers).
- **`page`**, **`publicationId`** — source (référence à une `<publication>`).
- **`import`** — sur `selectionEntry`/`entryLink` : `true` = l'entrée peut être importée/liée.
- **`comment`** — élément enfant texte libre, ignoré par le moteur (notes de dev).

Référence d'un livre : soit `page` + `publicationId` (pointant vers une `<publication>` déclarée),
soit les anciens champs `book`/`page` (déprécié — préférer `publicationId`).

---

## 3. Arbre du game system (.gst)

Conteneurs enfants directs de `<gameSystem>` (chacun est un pluriel enveloppant ses éléments) :

```
gameSystem
├─ readme                     (texte libre, description)
├─ publications               → publication (id, name, shortName, publisher, publicationDate, publisherUrl)
├─ costTypes                  → costType (id, name, defaultCostLimit, hidden)
├─ profileTypes               → profileType (id, name)
│                               └─ characteristicTypes → characteristicType (id, name)
├─ categoryEntries            → categoryEntry (id, name, hidden)  [+ modifiers/constraints/infoLinks…]
├─ forceEntries               → forceEntry (id, name, hidden)
│                               ├─ forceEntries (sous-détachements imbriqués)
│                               ├─ categoryLinks → categoryLink (slots FOC : HQ, Troops…)
│                               ├─ modifiers / constraints / rules / infoLinks
├─ sharedSelectionEntries     → selectionEntry   (briques partagées, liées via entryLink)
├─ sharedSelectionEntryGroups → selectionEntryGroup
├─ sharedProfiles             → profile
├─ sharedRules                → rule
├─ sharedInfoGroups           → infoGroup
├─ selectionEntries           → selectionEntry   (entrées racine)
├─ entryLinks                 → entryLink
├─ rules                      → rule
├─ infoLinks                  → infoLink
└─ categoryLinks / catalogueLinks
```

- **`costType`** : définit une ressource comptée (points, PL, CP…). Le `id` `"points"` (nom `"pts"`)
  est la convention. Référencé par `<cost typeId="...">`.
- **`profileType`** : définit un jeu de colonnes (ex. « Unit », « Ranged Weapons »). Chaque colonne =
  un `characteristicType`. Un `<profile>` choisit un `profileType` via `typeId` et remplit les
  colonnes via `<characteristic typeId="...">`.
- **`categoryEntry`** : étiquette (HQ, Character, Infantry, Faction: X…). Cible de conditions et de
  `categoryLink`. Peut porter des `modifiers`/`constraints` (ex. règle « 1 Warlord max »).
- **`forceEntry`** : structure de détachement (Patrol, Battalion…). Contient des `categoryLinks` qui
  définissent les slots (avec contraintes min/max) et peut imbriquer des `forceEntries`.

---

## 4. Arbre du catalogue (.cat)

Un catalogue **référence** les types du game system (il ne les redéfinit pas normalement). Conteneurs
enfants directs de `<catalogue>` :

```
catalogue
├─ readme / comment
├─ publications               → publication
├─ catalogueLinks            → catalogueLink (importer un autre catalogue-bibliothèque)
├─ (costTypes / profileTypes) → rares : seulement si le catalogue ajoute ses propres types
├─ categoryEntries            → categoryEntry (catégories propres à la faction)
├─ forceEntries               → forceEntry (détachements propres à la faction)
├─ sharedSelectionEntries     → selectionEntry   ← armes, wargear, améliorations partagées
├─ sharedSelectionEntryGroups → selectionEntryGroup
├─ sharedProfiles             → profile
├─ sharedRules                → rule
├─ sharedInfoGroups           → infoGroup
├─ selectionEntries           → selectionEntry   ← les UNITÉS racine de la faction
├─ entryLinks                 → entryLink
├─ rules                      → rule
├─ infoLinks                  → infoLink
└─ categoryLinks
```

Schéma mental : les **unités** vont dans `<selectionEntries>` ; les **armes/wargear réutilisables**
vont dans `<sharedSelectionEntries>` et sont attachées aux unités via des `<entryLink>` ; les
**règles/capacités réutilisables** vont dans `<sharedRules>`/`<sharedProfiles>` et sont attachées via
`<infoLink>`.

---

## 5. Briques de base

### selectionEntry — l'élément central (unité / modèle / amélioration)
```xml
<selectionEntry type="unit|model|upgrade" import="true" name="Nom" hidden="false" id="ID">
  <profiles>...</profiles>            <!-- stats (Unit) et/ou armes définies en propre -->
  <costs>...</costs>                  <!-- coût en points -->
  <categoryLinks>...</categoryLinks>  <!-- catégories (dont la PRIMAIRE) -->
  <selectionEntryGroups>...</selectionEntryGroups>  <!-- choix d'options -->
  <selectionEntries>...</selectionEntries>          <!-- sous-modèles -->
  <entryLinks>...</entryLinks>        <!-- armes/wargear liés depuis le partagé -->
  <infoLinks>...</infoLinks>          <!-- règles/capacités liées -->
  <constraints>...</constraints>      <!-- limites (min/max) -->
  <modifiers>...</modifiers>          <!-- mécaniques -->
  <rules>...</rules>
</selectionEntry>
```
`type` : `unit` (unité), `model` (figurine, comptée dans les stats de modèles), `upgrade`
(amélioration/arme/option). C'est une métadonnée d'affichage/statistiques.

### selectionEntryGroup — groupe d'options
```xml
<selectionEntryGroup name="Arme principale" hidden="false" id="ID" defaultSelectionEntryId="ID_option">
  <constraints>...</constraints>      <!-- ex. « choisir exactement 1 » : min=1 & max=1 -->
  <selectionEntries>...</selectionEntries>
  <entryLinks>...</entryLinks>
</selectionEntryGroup>
```
`defaultSelectionEntryId` : option pré-sélectionnée (doit référencer un enfant du groupe).

### profile — un tableau de stats nommé
```xml
<profile name="Nom" typeId="ID_profileType" typeName="Unit" hidden="false" id="ID">
  <characteristics>
    <characteristic name="M" typeId="ID_characteristicType">6"</characteristic>
    ...
  </characteristics>
</profile>
```
- `typeId` DOIT pointer vers un `profileType` existant (souvent dans le `.gst`).
- `typeName` est une copie lisible du nom du profileType (doit correspondre).
- Chaque `<characteristic>` : `typeId` DOIT pointer vers un `characteristicType` de ce profileType,
  et `name` correspond au nom de ce characteristicType. La valeur textuelle est le contenu de la balise.
- Une caractéristique dont le `typeId` n'appartient pas au profileType ne s'affiche pas → erreur silencieuse.

### rule — bloc de texte multi-lignes
```xml
<rule name="Nom de la règle" hidden="false" id="ID">
  <description>Texte de la règle, multi-lignes autorisées.</description>
</rule>
```
Seul élément qui garantit la préservation des retours à la ligne.

### cost
```xml
<costs>
  <cost name="pts" typeId="points" value="80"/>
</costs>
```
`typeId` DOIT pointer vers un `costType`. `value` est numérique (peut être décimal).

### categoryEntry / categoryLink
```xml
<!-- définition (dans categoryEntries) -->
<categoryEntry id="ID" name="HQ" hidden="false"/>
<!-- affectation (dans une selectionEntry ou forceEntry) -->
<categoryLink id="ID_link" name="HQ" hidden="false" targetId="ID_categoryEntry" primary="true"/>
```
`targetId` DOIT pointer vers un `categoryEntry`. **Exactement une** `categoryLink` d'une unité racine
doit avoir `primary="true"` (c'est le slot FOC où l'unité apparaît). Les autres `primary="false"`.

---

## 6. Roster (.ros)

Produit final (une liste jouée), généré par l'appli mais lisible/éditable. Arbre :

```
roster (id, name, gameSystemId, gameSystemName, gameSystemRevision)
├─ costs → cost (totaux du roster)
├─ costLimits → costLimit
└─ forces → force (id, name, catalogueId, catalogueName, catalogueRevision, entryId=forceEntry)
            ├─ publications
            ├─ categories → category (id, name, entryId, primary)
            └─ selections → selection (id, name, entryId, entryGroupId, number, type,
                                        page, customName, customNotes)
                            ├─ profiles → profile (recopiés, avec caractéristiques résolues)
                            ├─ rules / categories
                            ├─ costs → cost
                            └─ selections (imbriquées : options choisies)
```
Une `<selection>` référence son `entryId` (la `selectionEntry` d'origine dans le catalogue) et
`entryGroupId` si issue d'un groupe. `number` = quantité. Les profils/coûts sont **recopiés et
résolus** (valeurs finales après modifiers) dans le roster.

---

## 7. Index et repository

### index.xml (dataIndex)
Manifeste listant les fichiers d'un dépôt et leurs versions.
```xml
<dataIndex battleScribeVersion="2.03" name="Nom du dépôt" xmlns="http://www.battlescribe.net/schema/dataIndexSchema">
  <repositoryUrls><repositoryUrl>https://...</repositoryUrl></repositoryUrls>
  <dataIndexEntries>
    <dataIndexEntry filePath="Faction.cat" dataType="catalogue" dataId="ID" dataName="Faction"
                    dataBattleScribeVersion="2.03" dataRevision="1"/>
    <dataIndexEntry filePath="Systeme.gst" dataType="gamesystem" dataId="ID" dataName="Systeme"
                    dataBattleScribeVersion="2.03" dataRevision="1"/>
  </dataIndexEntries>
</dataIndex>
```
Convention BSData : **ne pas** committer `index.xml`/`index.bsi` sur GitHub (généré par le Gallery).

### .bsr (repository distribution)
Archive ZIP contenant un `index.xml` + les `.gst`/`.cat`. Sert à distribuer un pack complet.

---

## 8. Ordre des éléments — important mais tolérant

Les schémas BattleScribe utilisent majoritairement des listes **non ordonnées** au niveau des grands
conteneurs : BattleScribe et New Recruit parsent **par nom de balise**, pas par position stricte. En
pratique, l'ordre des grands conteneurs (`categoryEntries`, `sharedSelectionEntries`,
`selectionEntries`…) n'est pas une cause d'échec de chargement.

**Ce qui casse réellement le chargement**, par ordre de fréquence :
1. Une **référence non résolue** (`targetId`/`childId`/`typeId`/`gameSystemId`/`publicationId`).
2. Un **`id` dupliqué**.
3. Un **mauvais namespace** ou une mauvaise racine.
4. Du **XML mal formé** (balise non fermée, `&` non échappé, guillemet manquant).
5. Une **caractéristique orpheline** (typeId n'appartenant pas au profileType).
6. Un `<cost typeId>` sans `costType` correspondant.

→ Pour la propreté, on **imite l'ordre du fichier source réel** quand on en a un, et on garde les
éléments enfants dans leur conteneur pluriel. Mais la priorité de validation porte sur les 6 points
ci-dessus, pas sur un tri cosmétique. Le script `bs_validate.py` couvre ces 6 points.
