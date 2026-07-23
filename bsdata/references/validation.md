# Validation et dépannage « fichier qui ne se charge pas »

Quand BattleScribe ou New Recruit refuse un fichier ou affiche des erreurs, la cause est presque
toujours dans cette liste. Ordre = fréquence décroissante.

## 1. Référence non résolue (cause n°1)
Un attribut de référence pointe vers un `id` qui n'existe pas (faute de frappe, entrée supprimée,
copier-coller d'un autre fichier). Attributs concernés :
`targetId` (entryLink/infoLink/categoryLink/catalogueLink), `childId` (condition/repeat),
`typeId` (profile→profileType, characteristic→characteristicType, cost→costType),
`gameSystemId` (catalogue/roster → gst), `publicationId`, `catalogueId` (roster force),
`entryId`/`entryGroupId` (roster selection), `defaultSelectionEntryId` (group).

Symptôme New Recruit / BattleScribe : « … references … which does not exist », entrée absente, profil
vide, ou refus de charger.
**Correction** : `bs_validate.py` liste chaque référence cassée. Soit corriger l'`id` cible, soit
créer l'entité manquante. Attention aux références **inter-fichiers** : un `.cat` référence légitimement
des IDs du `.gst` — valider le **dossier entier** pour les résoudre.

## 2. ID dupliqué
Deux éléments avec le même `id`. Provoque des comportements incohérents ou une erreur.
**Correction** : régénérer un des deux IDs (`bs_new_id.py`) et mettre à jour les références qui
pointaient dessus.

## 3. Mauvais namespace / mauvaise racine
`xmlns` ne correspond pas au type (ex. un catalogue avec le namespace gameSystem), ou racine erronée.
Le logiciel ne reconnaît pas le fichier.
**Correction** : voir le tableau de `structure.md` §1. La racine et le `xmlns` doivent être cohérents.

## 4. XML mal formé
Balise non fermée, attribut sans guillemets, ou surtout **`&` non échappé**. Un `&` littéral (ex.
« Faith & Fury ») casse le parseur XML.
**Correction** : échapper `&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `'`→`&apos;`, `"`→`&quot;`.
`bs_validate.py` remonte l'erreur avec le numéro de ligne.

## 5. Caractéristique orpheline
Un `<characteristic typeId="X">` dont le `typeId` n'appartient pas au `profileType` du profil parent.
La caractéristique ne s'affiche pas (colonne vide), sans forcément bloquer le chargement.
**Correction** : aligner les `typeId` des caractéristiques sur les `characteristicType` du bon
`profileType`. Vérifier aussi que `typeName` du profil correspond au nom du profileType.

## 6. Coût sans costType
`<cost typeId="Y">` sans `costType` `id="Y"` déclaré (dans le gst ou le catalogue).
**Correction** : utiliser un `typeId` de costType existant (souvent `"points"`).

## 7. categoryLink primaire manquant ou multiple
Une unité racine doit avoir **exactement une** `categoryLink primary="true"`. Zéro → l'unité
n'apparaît dans aucun slot ; plusieurs → comportement ambigu.
**Correction** : un seul `primary="true"`, le reste `primary="false"`.

## 8. Révision non incrémentée
Le fichier est correct mais la mise à jour n'est pas détectée par BattleScribe / le Gallery.
**Correction** : incrémenter l'attribut `revision` de la racine à chaque publication.

---

## Checklist de contrôle croisé avant de rendre un fichier

- [ ] Racine + `xmlns` corrects pour le type de fichier.
- [ ] `battleScribeVersion="2.03"` (ou la version du repo).
- [ ] Pour un `.cat` : `gameSystemId` = `id` réel du `.gst` cible.
- [ ] Tous les `id` uniques.
- [ ] Toutes les références résolues (dans le fichier ou dans le repo).
- [ ] Tout `&`/`<`/`>`/`'`/`"` dans les valeurs est échappé.
- [ ] Chaque profil : `typeId`/`typeName` valides, caractéristiques rattachées.
- [ ] Chaque coût : `typeId` = costType existant.
- [ ] Une seule categoryLink primaire par unité racine.
- [ ] `revision` incrémentée si republication.
- [ ] `bs_validate.py` passe (aucune erreur bloquante).

---

## Comment interpréter la sortie de `bs_validate.py`

- **`[ERREUR]`** : bloquant probable (référence cassée dans le même fichier, ID dupliqué, XML mal
  formé, mauvais namespace). À corriger avant de rendre.
- **`[EXTERNE]`** : référence non trouvée dans le fichier isolé mais potentiellement définie ailleurs
  (game system, autre catalogue). Revalider le **dossier** pour lever le doute ; ce n'est une erreur
  que si l'ID n'existe nulle part dans le repo.
- **`[ALERTE]`** : non bloquant mais suspect (caractéristique orpheline, categoryLink primaire absent,
  coût sans costType visible). À vérifier.
- **`[OK]`** : le contrôle est passé.
