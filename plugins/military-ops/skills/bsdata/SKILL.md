---
name: bsdata
description: >-
  Lire, créer, éditer et valider les fichiers de données BattleScribe / New Recruit (format BSData) :
  catalogues (.cat/.catz), game systems (.gst/.gstz), rosters (.ros/.rosz), repositories (.bsr).
  Déclencher IMPÉRATIVEMENT dès que Florian tape /BSdata, /BSData ou /bsdata, fournit un fichier
  .cat/.gst/.ros/.catz/.gstz/.rosz/.bsr, mentionne « BattleScribe », « New Recruit », « BSData »,
  un « catalogue » ou « game system » d'armée, ou demande de : lire/inspecter des données d'armée ;
  créer/éditer une unité, un modèle, une arme, un profil, une règle, une amélioration, une catégorie,
  un détachement ; ajouter une mécanique (modifier, contrainte, condition, lien) ; corriger un fichier
  qui ne se charge pas ; convertir une faction homebrew (Les Anciens, Skaventides, Iondarr) en données
  jouables. Déclencher aussi pour des demandes courtes (« ajoute une arme à cette unité », « pourquoi
  mon .cat ne se charge pas ? »). Priorité : RESPECTER la structure pour un chargement sans erreur.
---

# BSdata — Fichiers de données BattleScribe / New Recruit

## Ce que fait ce skill

Manipuler les fichiers du format **BSData** (le format ouvert de BattleScribe, lu aussi par New
Recruit et les outils communautaires) : les **lire** (résumer une armée, extraire unités/armes/coûts),
les **créer** de zéro, les **éditer** (ajouter unités, profils d'armes, règles, mécaniques), et
surtout les **valider** pour qu'ils se chargent **sans erreur**.

Ce sont des fichiers **XML**. Une seule référence cassée, un ID dupliqué ou un mauvais namespace, et le
logiciel refuse de charger le fichier ou affiche des erreurs de validation. Le respect scrupuleux de la
structure n'est pas optionnel : c'est le cœur du skill.

## Règle d'or absolue : ne jamais écrire « à l'aveugle »

Le format est trop dense pour être généré de tête sans erreur. La discipline non négociable :

1. **Toujours partir d'un fichier réel quand il existe.** Si Florian fournit un `.cat`/`.gst`, on
   l'inspecte d'abord (`scripts/bs_inspect.py`), on repère les IDs et types réels, et on greffe le
   nouveau contenu dessus. On ne recrée jamais depuis zéro ce qui existe déjà.
2. **Toute référence pointe vers un ID qui existe.** `targetId`, `childId`, `typeId`, `gameSystemId`,
   `publicationId`, `catalogueId`… doivent tous résoudre. Les **références cassées sont la cause n°1**
   des fichiers qui ne se chargent pas.
3. **Chaque ID est unique** dans le fichier (idéalement dans tout le repo).
4. **Valider avant de rendre.** Après toute création/édition, lancer `scripts/bs_validate.py` et ne
   remettre le fichier que s'il passe (ou en signalant explicitement les points externes à vérifier).

> Sans `/maj` explicite, ne jamais modifier les fichiers internes du skill ni le repackager
> (même convention que les autres skills de Florian).

## Workflow

### 1. Identifier le type de fichier

Lire la **racine** et le **namespace** — ils déterminent tout (voir `references/structure.md`) :

| Fichier | Racine | Namespace (`xmlns`) |
|---|---|---|
| Game system (`.gst`) | `<gameSystem>` | `http://www.battlescribe.net/schema/gameSystemSchema` |
| Catalogue (`.cat`) | `<catalogue>` | `http://www.battlescribe.net/schema/catalogueSchema` |
| Roster (`.ros`) | `<roster>` | `http://www.battlescribe.net/schema/rosterSchema` |
| Index (`index.xml`) | `<dataIndex>` | `http://www.battlescribe.net/schema/dataIndexSchema` |

Les variantes `.catz/.gstz/.rosz/.bsr/.bsi` sont des **archives ZIP** contenant le XML (voir
« Fichiers compressés » plus bas).

### 2. Lire / inspecter

Pour comprendre un fichier avant d'y toucher :

```bash
python3 scripts/bs_inspect.py "<fichier.cat>"
```

Donne : type, namespace, version, IDs racine, nombre d'entrées, liste des `selectionEntry` avec leurs
profils et coûts, `profileType`s disponibles, catégories, et un échantillon d'IDs. Pour un résumé
« humain » d'une armée (unités, points), lire aussi les profils `Unit` et les coûts.

### 3. Éditer / créer

- Choisir la bonne brique (voir `references/structure.md` pour l'arbre complet, et
  `references/profiles-weapons.md` pour ajouter unités/modèles/armes).
- Générer les nouveaux IDs avec `scripts/bs_new_id.py` (format `xxxx-xxxx-xxxx-xxxx`).
- Respecter l'**imbrication** (conteneurs pluriels autour des éléments : `<profiles>`→`<profile>`,
  `<characteristics>`→`<characteristic>`, `<costs>`→`<cost>`, `<selectionEntries>`→`<selectionEntry>`,
  `<modifiers>`→`<modifier>`, etc.).
- Respecter l'**échappement XML** : `&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;`, `'`→`&apos;`, `"`→`&quot;`
  (ex. `Be&apos;lakor`, `Faith &amp; Fury`). Ne JAMAIS laisser un `&` nu.
- Pour les mécaniques (modifiers, conditions, contraintes, liens) : voir `references/links-modifiers.md`.

### 4. Valider (obligatoire)

```bash
# Un seul fichier
python3 scripts/bs_validate.py "<fichier.cat>"

# Tout un repo (résout les références croisées entre .gst et .cat)
python3 scripts/bs_validate.py /chemin/vers/repo/
```

Le validateur vérifie : XML bien formé, namespace/racine cohérents, IDs uniques, **références
résolues** (targetId/childId/typeId/costType/publication…), caractéristiques rattachées à un
`profileType` valide, et signale les références **externes** (à un autre fichier) quand on valide un
fichier isolé. Corriger tout ce qu'il remonte avant de rendre le fichier.

### 5. Rendre

Écrire le fichier final avec `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` en tête,
encodage UTF-8, et le présenter via `present_files`. Rappeler à Florian d'**incrémenter la
`revision`** de la racine s'il republie (sinon BattleScribe/le Gallery ne détectent pas la mise à jour).

## Squelette minimal d'un catalogue valide

Point d'ancrage mental (détails et ordre complet dans `references/structure.md`). Un `.cat` doit
déclarer le bon `gameSystemId` (celui du `.gst` cible) :

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<catalogue id="1a2b-3c4d-5e6f-7a8b" name="Ma Faction Homebrew" revision="1"
           battleScribeVersion="2.03" library="false"
           gameSystemId="sys-352e-adc2-7639-d6a9" gameSystemRevision="38"
           authorName="Florian" xmlns="http://www.battlescribe.net/schema/catalogueSchema">
  <categoryEntries/>
  <sharedSelectionEntries/>
  <sharedProfiles/>
  <sharedRules/>
  <selectionEntries>
    <!-- unités racine ici -->
  </selectionEntries>
</catalogue>
```

Les `profileType`s (Unit, Ranged Weapons, Melee Weapons, Abilities…) et les catégories (HQ, Troops…)
sont normalement **définis dans le `.gst`** et **référencés** par les catalogues via leurs IDs. Un
catalogue ne redéfinit pas ces types : il pointe vers ceux du game system. **Il faut donc connaître
les IDs du `.gst`** avant d'ajouter des profils dans un `.cat` — inspecter le `.gst` d'abord.

## Fichiers compressés (.catz / .gstz / .rosz / .bsr / .bsi)

Ce sont des ZIP. Pour éditer :

```bash
mkdir -p /tmp/bs_extract && cd /tmp/bs_extract
python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall('.')" "<fichier.gstz>"
# éditer le .gst/.cat extrait, valider, puis recompresser :
python3 -c "import zipfile,sys,os; z=zipfile.ZipFile(sys.argv[2],'w',zipfile.ZIP_DEFLATED); z.write(sys.argv[1], os.path.basename(sys.argv[1])); z.close()" "<fichier.gst>" "<sortie.gstz>"
```

Convention BSData : sur GitHub on garde les fichiers **décompressés** (`.cat`/`.gst`) ; la compression
est faite par le Gallery. Pour un usage local New Recruit/BattleScribe, le décompressé fonctionne.

## Références (lire selon le besoin)

- `references/structure.md` — arbre complet des éléments, attributs, conteneurs, ordre, et racines
  gameSystem/catalogue/roster/index. **À lire avant toute édition structurelle.**
- `references/profiles-weapons.md` — ajouter unités, modèles, profils d'armes (Ranged/Melee),
  caractéristiques 10e édition, coûts, catégories, améliorations. **À lire pour ajouter un profil.**
- `references/links-modifiers.md` — entryLink, infoLink, catalogueLink, publicationLink, et le
  système de mécaniques (modifier / condition / conditionGroup / constraint / repeat). **À lire pour
  ajouter une mécanique.**
- `references/validation.md` — catalogue des erreurs de chargement fréquentes et leur correction,
  checklist de références croisées.

## Scripts

- `scripts/bs_inspect.py <fichier>` — résumé structuré d'un fichier.
- `scripts/bs_validate.py <fichier|dossier>` — validation complète (le garde-fou « sans erreur »).
- `scripts/bs_new_id.py [n]` — génère n IDs uniques au format BattleScribe.

Tous en Python 3 pur (stdlib uniquement, pas de dépendance réseau).
