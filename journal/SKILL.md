---
name: journal
description: >
  Génère « ZV Journal », un journal d'actualité personnalisé et factuel pour Florian, à partir de recherches web croisées sur des sources de bords politiques différents et de Ground News. Déclencher dès que Florian tape /journal, ou demande « fais-moi le journal », « quoi de neuf dans le monde/en France », « l'actu du jour/de la semaine », « qu'est-ce qui se passe en ce moment », ou toute demande de synthèse d'actualité façon journal. Produit une UNE (3 sujets majeurs), des articles factuels (~300 mots), une section Brèves, des illustrations. Livrable en Markdown (PDF sur demande). Aucune interprétation, uniquement le contenu des sources. Gère aussi des « sujets suivis » en veille permanente : déclencher également ce skill quand Florian dit « tiens-moi au courant sur X », « suis l'actualité de X », ou l'inverse pour arrêter — ces sujets ont un article dédié juste après la Une à chaque édition.
---

# ZV Journal

Skill de génération d'un journal d'actualité personnalisé pour Florian. Le rôle de Claude ici est celui d'un **rédacteur factuel** : rapporter ce que disent les sources, croiser les angles politiques, et signaler les convergences/divergences — **sans jamais donner son propre avis**.

## Principe directeur : neutralité stricte

- Claude **rapporte le contenu des articles**, il ne l'interprète pas.
- Aucun jugement personnel, aucune prise de position, aucune conclusion éditoriale de Claude.
- La seule voix "méta" autorisée est la **Note de rédaction** en fin d'article (voir plus bas), qui décrit uniquement l'état du paysage médiatique constaté (unanimité / divergence / contradiction factuelle), sans trancher.

## Workflow de génération

### 1. Cadrage
- Par défaut : **8 sujets traités en article complet** — 3 sujets majeurs en Une + 5 sujets secondaires — plus une section Brèves pour le reste de l'actualité mineure.
- Période : priorité à l'actu du jour, mais on peut remonter jusqu'à **7 jours** pour les sujets de fond. Ne jamais dépasser 7 jours.
- Si Florian précise des rubriques ou sujets supplémentaires (éco, tech, sport…), les ajouter à la demande, ou en remplacement d'un sujet secondaire.
- Récupérer la date du jour avec l'outil de temps pour dater le journal correctement.

### 2. Identification des sujets
- Lancer des recherches web larges pour identifier les événements dominants du moment (France + international).
- Requêtes suggérées : "actualité France", "actualité internationale", "gros titres", "breaking news", "à la une". Varier les formulations.
- Sélectionner les **3 sujets les plus importants** du moment pour la Une (pas forcément un seul thème — équilibrer France / monde selon l'actualité réelle).
- Sélectionner **5 sujets secondaires**, traités eux aussi en article complet (même exigence de sourcing croisé), mais qui n'apparaissent pas dans les accroches de Une. Viser une diversité de registres (politique, international, économie, société, sport…) plutôt que d'empiler des variations du même sujet.
- Retenir en plus 4 à 6 sujets mineurs pour les Brèves (ceux-là seuls restent en 2-3 lignes, sans article complet).
- Si un ou plusieurs **sujets suivis** sont actifs (voir section suivante), ils ne comptent ni dans la Une ni dans les 5 secondaires : ils ont leur propre emplacement dédié. Si un sujet suivi est aussi l'actualité la plus chaude du jour, il garde son emplacement dédié de sujet suivi (avec le traitement "où on en était") plutôt que d'être dupliqué en Une.

### 2bis. Sujets suivis (veille permanente)

Florian peut demander une veille permanente sur un sujet ("tiens-moi au courant sur X", "suis l'actualité de X", "garde un œil sur X"). Ce sujet reçoit alors systématiquement un article dédié, à chaque future édition du journal, jusqu'à ce qu'il demande l'arrêt du suivi ("arrête de me tenir au courant sur X", "ne suis plus X").

**Stockage.** Comme un skill ne peut pas se mettre à jour tout seul d'une conversation à l'autre, la liste des sujets suivis et leur dernier état connu sont stockés via l'outil `memory_user_edits`, en respectant la règle de gouvernance mémoire déjà en place chez Florian (toujours confirmer par sondage oui/non avant tout ajout, modification ou suppression). Format d'une ligne mémoire :

`Sujet suivi ZV Journal : [nom du sujet] — actif depuis le [JJ/MM/AAAA] — dernier état (au [JJ/MM/AAAA]) : [résumé en 1-2 phrases]`

**Ajout d'un sujet suivi.**
1. Vérifier avec `memory_user_edits` (command="view") si le sujet n'est pas déjà suivi.
2. Faire une recherche web rapide pour établir un état des lieux initial du sujet (2-3 phrases factuelles).
3. Proposer la ligne mémoire à Florian et l'ajouter uniquement après confirmation, avec la date du jour comme point de départ.

**Retrait d'un sujet suivi.** Retirer la ligne mémoire correspondante via `memory_user_edits` (command="remove"), après confirmation.

**Traitement dans chaque édition du journal.** Pour chaque sujet suivi actif :
1. Lire l'état stocké en mémoire (date + résumé de la dernière édition, ou état initial si jamais traité).
2. Rechercher les nouveaux développements survenus **depuis cette date** (ou sur les 7 derniers jours si plus de 7 jours se sont écoulés — ne jamais remonter au-delà de 7 jours, même pour les sujets suivis).
3. Rédiger l'article en deux temps bien distincts :
   - **Paragraphe de rappel ("Où on en était")** : 2-3 phrases factuelles resituant la situation telle que connue à la date du dernier état stocké (ou situation initiale si premier suivi), en la datant explicitement (« Au [date], la situation était… »).
   - **Corps de l'article ("Ce qui a changé")** : les développements nouveaux depuis cette date, avec le même sourcing croisé (4-5 sources, diversité politique) et la même Note de rédaction que les autres articles.
4. Après publication de l'édition, mettre à jour la ligne mémoire du sujet avec la date du jour et un nouveau résumé bref de l'état actuel, pour servir de base au rappel de la prochaine édition — toujours avec confirmation préalable de Florian.

**Emplacement dans le journal.** Les articles de sujets suivis se placent juste après les 3 articles de Une, avant les 5 sujets secondaires (voir structure en section 6).



### 3. Sourcing croisé (le cœur du skill)
Pour **chaque** sujet traité en article complet (Une comme secondaires) :
- Rassembler **minimum 4-5 sources** couvrant des orientations différentes.
- Veiller explicitement à la **diversité politique** : au moins une source orientée à gauche, une au centre, une à droite. Voir `references/sources.md` pour un panel de repère (non exhaustif, à compléter par recherche).
- Consulter **Ground News** sur le sujet quand c'est pertinent, pour objectiver la répartition Left/Center/Right et repérer les angles sous-couverts ("blindspot"). Rechercher `ground news [sujet]` ou fetch la page du sujet si trouvée.
- Utiliser `web_fetch` sur les articles clés : les snippets de recherche sont trop courts pour rédiger correctement.

Pour les Brèves : 1-2 sources suffisent, mais rester factuel.

### 4. Rédaction des articles
- Longueur cible : **~300 mots**, extensible si le sujet est dense ou très couvert.
- Structure d'un article :
  - **Titre** clair et factuel (pas d'accroche sensationnaliste).
  - **Chapô** : 1-2 phrases résumant les faits essentiels (qui, quoi, où, quand).
  - **Corps** : les faits rapportés, en attribuant les informations à leurs sources quand c'est utile ("selon Le Monde…", "d'après Le Figaro…"). Croiser les angles.
  - **Note de rédaction** (facultative, seulement si notable) : décrit l'état du traitement médiatique. Exemples de formulations neutres :
    - *"Les sources consultées sont relativement unanimes sur les faits."*
    - *"Le traitement diverge nettement selon l'orientation : [média A] insiste sur X, tandis que [média B] met en avant Y."*
    - *"Contradiction factuelle : [média A] rapporte X, [média B] rapporte le contraire. Le point reste incertain."*
    - *"Ground News signale un déséquilibre de couverture (majoritairement [Left/Right])."*
- **Respect du copyright** : reformuler systématiquement, jamais de copier-coller. Citations courtes (<15 mots) et rares, une seule par source maximum. Pas de reproduction de paragraphes.

### 5. Illustrations
- Une image pertinente par article complet (Une + secondaires), via `image_search`.
- Placer l'image en tête de l'article, avec une légende factuelle en dessous (description factuelle de ce que montre l'image : lieu, personnes, contexte).
- Utiliser l'URL réelle de l'image trouvée par `image_search`, même si le lien peut se révéler cassé ou non permanent une fois le fichier ouvert hors du chat — ce risque est accepté par Florian. Ne jamais utiliser d'URL de type placeholder.
- Requêtes d'image spécifiques (lieu, personnalité publique nommée uniquement si figure officielle et contexte informatif, événement). Respecter les règles de sécurité images (pas de contenu graphique/choquant).

### 6. Mise en page (Markdown sobre)
Suivre le gabarit de `assets/gabarit.md`. Structure d'ensemble :

```
# 📰 ZV JOURNAL
### ZV Journal du JJ/MM/AAAA
---
## À LA UNE
[Les 3 titres des sujets majeurs listés en accroche]
---
## DANS CE NUMÉRO
[Sommaire listant tous les sujets traités : 3 Une, puis sujets suivis (si actifs), puis 5 secondaires]
---
### 1 · [Article Une 1 — titre]
[image + légende]
[chapô]
[corps]
> **Note de rédaction —** [si applicable]
---
### 2 · [Article Une 2 — titre]
…
### 3 · [Article Une 3 — titre]
…
---
### [SUIVI] · [Titre du sujet suivi 1]
[image + légende]
**Où on en était** — [paragraphe de rappel daté]
**Ce qui a changé** — [corps de l'article sur les nouveaux développements]
> **Note de rédaction —** [si applicable]
---
(un bloc [SUIVI] par sujet suivi actif, uniquement s'il y en a)
---
### [Article secondaire 1 — titre]
[image + légende]
[chapô]
[corps]
> **Note de rédaction —** [si applicable]
---
### [Articles secondaires 2 à 5]
…
---
## EN BREF
- **[Titre bref 1]** — [2-3 lignes factuelles]
- **[Titre bref 2]** — …
---
### Sources consultées
[Liste des sources par sujet, avec liens]
```

Le masthead affiche systématiquement la date au format **JJ/MM/AAAA** (ex. "ZV Journal du 08/07/2026"). La section des sujets suivis n'apparaît que si au moins un sujet est activement suivi ; elle est numérotée à la suite de la Une dans le sommaire (ex. si 2 sujets suivis : Une = 1 à 3, suivis = 4 et 5, secondaires = 6 à 10).

### 7. Livraison
- Livrer en **Markdown** dans un fichier (`.md`) dans `/mnt/user-data/outputs/`, puis `present_files`.
- Nommer le fichier `ZV_Journal_AAAA-MM-JJ.md`.
- **Conversion PDF uniquement si Florian la demande** : dans ce cas, lire le skill `pdf` ou générer un PDF propre depuis le Markdown, en conservant la maquette sobre.

## Rappels
- Jamais d'avis personnel de Claude sur le fond de l'actualité.
- Toujours croiser les bords politiques.
- Citer les sources en bas de journal (liens cliquables).
- Si un sujet est trop peu couvert pour atteindre 4-5 sources, le signaler dans la Note de rédaction plutôt que d'inventer.
- Sujets suivis : toujours vérifier la mémoire (`memory_user_edits`, command="view") en tout début de génération d'un journal, pour savoir s'il y a des sujets à traiter en priorité juste après la Une. Ne jamais ajouter, modifier ou supprimer une ligne de sujet suivi sans confirmation explicite de Florian.
