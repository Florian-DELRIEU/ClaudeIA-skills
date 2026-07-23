# Ajouter unités, modèles et profils d'armes

Cette référence montre la sérialisation exacte pour créer du contenu jouable. **Avant tout ajout de
profil, inspecter le `.gst` cible** pour récupérer les `typeId` des profileType et les `typeId` des
characteristicType : un profil ne s'affiche correctement que s'il pointe vers les vrais IDs du game
system. Utiliser `scripts/bs_inspect.py <systeme.gst>` qui liste tous les profileType et leurs
caractéristiques avec leurs IDs.

---

## 1. profileType « Unit » (stats d'unité) — 10e édition

En Warhammer 40k 10e, le profileType « Unit » contient : **M, T, SV, W, LD, OC**.
(En 9e édition c'était : M, WS, BS, S, T, W, A, Ld, Save. Toujours vérifier dans le `.gst` réel —
les noms et IDs de caractéristiques varient selon le système et l'édition.)

Exemple de profil d'unité (les `typeId` sont ceux du `.gst` — remplacer par les vrais) :
```xml
<profiles>
  <profile name="Captain" typeId="ID_profileType_Unit" typeName="Unit" hidden="false" id="NOUVEL_ID">
    <characteristics>
      <characteristic name="M"  typeId="ID_M">6&quot;</characteristic>
      <characteristic name="T"  typeId="ID_T">4</characteristic>
      <characteristic name="SV" typeId="ID_SV">3+</characteristic>
      <characteristic name="W"  typeId="ID_W">5</characteristic>
      <characteristic name="LD" typeId="ID_LD">6+</characteristic>
      <characteristic name="OC" typeId="ID_OC">1</characteristic>
    </characteristics>
  </profile>
</profiles>
```
Notes :
- Le pouce `"` dans une valeur (`6"`) doit être écrit `6&quot;` dans le XML.
- `name` et `typeName` sont des copies lisibles ; ils DOIVENT correspondre aux noms réels du `.gst`.
- `typeId` (du profil) = l'ID du profileType ; `typeId` (de chaque characteristic) = l'ID du
  characteristicType correspondant.

---

## 2. Profils d'armes — 10e édition

Deux profileType : **« Ranged Weapons »** et **« Melee Weapons »**.

- Ranged Weapons (colonnes) : **Range, A, BS, S, AP, D, Keywords**
- Melee Weapons (colonnes) : **Range, A, WS, S, AP, D, Keywords** (Range vaut « Melee »)

Arme à distance (bolt rifle) :
```xml
<profile name="Bolt rifle" typeId="ID_profileType_Ranged" typeName="Ranged Weapons" hidden="false" id="NOUVEL_ID">
  <characteristics>
    <characteristic name="Range"    typeId="ID_Range">24&quot;</characteristic>
    <characteristic name="A"        typeId="ID_A">2</characteristic>
    <characteristic name="BS"       typeId="ID_BS">3+</characteristic>
    <characteristic name="S"        typeId="ID_S">4</characteristic>
    <characteristic name="AP"       typeId="ID_AP">-1</characteristic>
    <characteristic name="D"        typeId="ID_D">1</characteristic>
    <characteristic name="Keywords" typeId="ID_Keywords">Assault, Heavy</characteristic>
  </characteristics>
</profile>
```
Arme de mêlée (power fist) :
```xml
<profile name="Power fist" typeId="ID_profileType_Melee" typeName="Melee Weapons" hidden="false" id="NOUVEL_ID">
  <characteristics>
    <characteristic name="Range"    typeId="ID_Range">Melee</characteristic>
    <characteristic name="A"        typeId="ID_A">3</characteristic>
    <characteristic name="WS"       typeId="ID_WS">3+</characteristic>
    <characteristic name="S"        typeId="ID_S">8</characteristic>
    <characteristic name="AP"       typeId="ID_AP">-2</characteristic>
    <characteristic name="D"        typeId="ID_D">2</characteristic>
    <characteristic name="Keywords" typeId="ID_Keywords">-</characteristic>
  </characteristics>
</profile>
```
Les mots-clés d'arme (Assault, Rapid Fire, Devastating Wounds…) qui ont une **règle** associée dans le
`.gst` se lient en plus via `<infoLink type="rule" targetId="...">` — voir `links-modifiers.md`.

---

## 3. Deux façons d'attacher une arme à une unité

### A. Arme définie « en propre » dans l'unité (rapide, non réutilisable)
Mettre le `<profile>` de l'arme directement dans les `<profiles>` d'une `selectionEntry` de type
`upgrade` (l'arme), elle-même enfant de l'unité. Simple mais duplique la donnée si l'arme est courante.

### B. Arme partagée + lien (recommandé, réutilisable)
1. Définir l'arme une fois comme `selectionEntry type="upgrade"` dans `<sharedSelectionEntries>`,
   avec son `<profiles>` (le profil d'arme) — voir §2.
2. L'attacher à chaque unité qui la porte via un `<entryLink>` (voir `links-modifiers.md`).
C'est le modèle standard des catalogues BSData (armes communes déclarées une fois, liées partout).

---

## 4. Squelette complet d'une unité racine

```xml
<selectionEntry type="model" import="true" name="Captain" hidden="false" id="ID_UNITE">
  <profiles>
    <!-- profil Unit ici (§1) -->
  </profiles>
  <costs>
    <cost name="pts" typeId="points" value="80"/>
  </costs>
  <categoryLinks>
    <categoryLink id="ID_lien1" name="HQ" hidden="false" targetId="ID_cat_HQ" primary="true"/>
    <categoryLink id="ID_lien2" name="Character" hidden="false" targetId="ID_cat_Character" primary="false"/>
    <categoryLink id="ID_lien3" name="Infantry" hidden="false" targetId="ID_cat_Infantry" primary="false"/>
  </categoryLinks>
  <selectionEntryGroups>
    <selectionEntryGroup name="Wargear" hidden="false" id="ID_grp">
      <constraints>
        <constraint type="min" value="1" field="selections" scope="parent" shared="true" id="ID_c_min"/>
        <constraint type="max" value="1" field="selections" scope="parent" shared="true" id="ID_c_max"/>
      </constraints>
      <entryLinks>
        <entryLink import="true" name="Bolt pistol" hidden="false" type="selectionEntry"
                   id="ID_el" targetId="ID_arme_partagee"/>
      </entryLinks>
    </selectionEntryGroup>
  </selectionEntryGroups>
  <infoLinks>
    <infoLink name="Leader" hidden="false" type="rule" id="ID_il" targetId="ID_regle_partagee"/>
  </infoLinks>
</selectionEntry>
```
Points de contrôle :
- **Une seule** `categoryLink primary="true"` (le slot d'affichage FOC).
- `targetId` des categoryLink → catégories réelles du `.gst`/`.cat`.
- `targetId` des entryLink/infoLink → entrées/règles réelles du partagé.
- `typeId` du coût → un `costType` réel (`"points"`).
- Nouveaux `id` uniques partout (`scripts/bs_new_id.py`).

---

## 5. Ajouter une amélioration / option

Une option est une `selectionEntry type="upgrade"`. Pour un choix « exactement 1 parmi N », regrouper
les options dans un `selectionEntryGroup` avec deux contraintes `min=1` et `max=1` (scope `parent`).
Pour « 0 ou 1 », mettre seulement `max=1`. Pour « jusqu'à X figurines », contrainte `max=X` sur le
groupe/entrée avec le bon `scope`.

---

## 6. Checklist « profil ajouté sans erreur »

- [ ] `.gst` cible inspecté : IDs de profileType + characteristicType récupérés.
- [ ] `typeId`/`typeName` du profil = vrais IDs/noms du profileType.
- [ ] Chaque `characteristic.typeId` appartient bien à ce profileType.
- [ ] Nouveaux `id` uniques (profil, unité, liens, contraintes).
- [ ] Valeurs échappées (`6&quot;`, `&amp;`, `&apos;`).
- [ ] Coût lié à un `costType` existant.
- [ ] `scripts/bs_validate.py` passe sans erreur bloquante.
