---
name: warhammer40k-lore
description: >
  Référence vivante pour tout ce qui touche au lore de Warhammer 40,000. Utiliser cette skill dès que l'utilisateur pose une question sur l'univers WH40K : factions, personnages, événements historiques, organisations, planètes, races xénos, la Warp, le Chaos, les dieux, l'Imperium, les Space Marines, les Primarchs, les technologies, les armes, les vaisseaux, les ordres religieux, l'Inquisition, les Rogue Traders, les Eldars, les Tau, les Tyranides, les Nécrons, les Orks, ou tout autre élément de l'univers 40K. Déclencher même pour des questions simples comme "c'est quoi X ?", "qui est Y ?", "quelle faction contrôle Z ?", ou "dis-moi tout sur [sujet 40K]". Ne pas répondre de mémoire : toujours aller chercher sur les sources listées ci-dessous.
---

# Warhammer 40,000 — Skill Navigateur de Lore

Cette skill transforme Claude en navigateur web spécialisé WH40K. Elle ne stocke pas le lore : elle définit **où chercher**, **dans quel ordre**, et **comment synthétiser** les résultats.

---

## Philosophie

L'univers WH40K s'étend sur des décennies de codex, romans (Horus Heresy, Warhammer Crime, etc.), jeux vidéo, audio dramas et mises à jour de règles. Le canon est vaste, parfois contradictoire, et en évolution permanente. Il est donc préférable de **consulter des sources vivantes** plutôt que de s'appuyer sur des connaissances d'entraînement potentiellement obsolètes.

**Règle fondamentale** : ne jamais répondre à une question de lore de mémoire seule — toujours effectuer au moins une recherche web pour confirmer ou compléter.

---

## Hiérarchie des sources

Consulter dans cet ordre de priorité :

### 1. Lexicanum (priorité maximale)
- **URL** : `https://wh40k.lexicanum.com/wiki/`
- **Pourquoi** : Le plus rigoureux. Chaque affirmation est sourcée (codex, roman, numéro de page). Idéal pour les faits précis, les dates, les affiliations officielles.
- **Utilisation** : Pour les définitions, les biographies de personnages, les événements historiques, les termes techniques.
- **Langue** : Anglais principalement. Il existe un Lexicanum français (`fr.warhammer40k.lexicanum.com`) mais moins complet.

### 2. Warhammer 40,000 Wiki (Fandom)
- **URL** : `https://warhammer40k.fandom.com/wiki/`
- **Pourquoi** : Plus exhaustif que Lexicanum pour les sujets obscurs ou les factions mineures. Moins rigoureux sur les sources mais très bon pour la vue d'ensemble.
- **Utilisation** : Pour les sujets peu documentés, la vue d'ensemble d'une faction, les résumés d'événements.

### 3. Wahapedia
- **URL** : `https://wahapedia.ru/`
- **Pourquoi** : Référence pour les règles de jeu et le background d'unités spécifiques. Utile quand la question concerne des unités de l'armée ou du contexte de bataille.
- **Utilisation** : Pour les fiches d'unité, les capacités spéciales avec leur justification narrative.

### 4. Recherche web générale (dernier recours)
- Utiliser `web_search` avec le terme exact + "40k" ou "warhammer" pour trouver d'autres sources si les trois premières ne suffisent pas.
- Accepter des sources comme les sous-reddits r/40kLore, r/warhammer, ou des blogs spécialisés, mais signaler que la fiabilité est moindre.

---

## Stratégie de recherche

### Construction des requêtes

- Toujours inclure un qualificatif : `"40k"`, `"warhammer 40000"`, ou `"40K lore"` pour éviter les résultats Warhammer Fantasy ou Age of Sigmar.
- Pour les personnages : `[Nom du personnage] warhammer 40k`
- Pour les factions : `[Nom de faction] 40k lore`
- Pour les événements : `[Nom de l'événement] 40k timeline`
- Pour les organisations : `[Organisation] imperium 40k`
- Pour les xénos : `[Race] 40k biology / history / culture`

### Ordre d'opération

1. Chercher d'abord sur **Lexicanum** avec `web_fetch` si l'URL est connue, sinon `web_search` + `"lexicanum"`.
2. Si le résultat est insuffisant ou le sujet absent, chercher sur **Fandom Wiki**.
3. Combiner les deux si les informations sont complémentaires.
4. Mentionner la source dans la réponse.

---

## Gestion des contradictions de canon

WH40K a plusieurs niveaux de canon et des contradictions fréquentes entre sources (codex vs roman vs jeu vidéo). Conduite à tenir :

- **Signaler brièvement** les variantes si elles sont significatives : *"Selon le Codex Space Marines, X. Le roman Y présente une version différente où Z."*
- **Prioriser** : Codex actuel > Horus Heresy Series (Black Library) > anciens codex > sources non officielles.
- **Ne pas trancher arbitrairement** : présenter les deux versions si elles coexistent dans des sources de même niveau.
- **Éviter le wikihole** : si la contradiction est mineure ou stylistique, ne pas la mentionner et choisir la version la plus répandue.

---

## Lore personnel [ZV]

L'utilisateur a un corpus de lore personnel qui peut **étendre ou contredire** le canon officiel. Ce lore est organisé en plusieurs fichiers dans `references/personal-lore/`.

### Navigation dans le lore personnel

**Toujours lire `references/personal-lore/INDEX.md` en premier.** Il contient la liste de toutes les entrées avec leur fichier cible. Ouvrir ensuite uniquement le fichier de catégorie pertinent :

| Fichier | Contenu |
|---|---|
| `INDEX.md` | Point d'entrée — liste toutes les entrées, à lire en premier |
| `mecaniques.md` | Règles maison, technologies, systèmes alternatifs |
| `factions-imperiales.md` | SM, GI, Inquisition, Ecclesiarchie, AdMech, RT, Custodes... |
| `factions-xenos.md` | Eldars, Tau, Tyranides, Nécrons, Orks, Drukhari... |
| `chaos.md` | Dieux du Chaos, démons, CSM, Légions renégates, Warp |
| `histoire.md` | Divergences chronologiques, événements alternatifs |
| `personnages.md` | Personnages originaux ou versions modifiées de persos canon |
| `divers.md` | Planètes, organisations, artéfacts, xénos mineurs, etc. |

Les factions originales développées ont leur propre dossier au niveau supérieur : `references/factions-custom/`. Lire `references/factions-custom/INDEX.md` pour la liste complète. Fichiers actuels :

| Fichier | Contenu |
|---|---|
| `references/factions-custom/INDEX.md` | Index des factions custom — à lire en premier |
| `references/factions-custom/sons-of-mars.md` | Chapitre SM successeur Iron Hands, basé sur Jupiter, inspiration légions romaines |
| `references/factions-custom/skaventides.md` | Xénos rongeurs parasites, Vermund, Pierre-Fange, connexion Nurgle |

Les systèmes/secteurs de campagne développés en profondeur ont également leur propre dossier dédié dans `references/LorePerso/`. Lire l'`INDEX.md` du dossier concerné en premier. Dossiers actuels :

| Dossier | Contenu |
|---|---|
| `references/LorePerso/Iondarr/INDEX.md` | Index du système Iondarr — à lire en premier |
| `references/LorePerso/Iondarr/systeme-iondarr.md` | Vue d'ensemble système, G.S.S., Iondarr III (consortiums, chronologie M41) |
| `references/LorePerso/Iondarr/iondarr-ii.md` | Iondarr II (monde-ruche) et Iondarr II.1 (lune aristocratique) |

### Règles d'application

- **Tag `[ZV]`** : toute information issue du lore personnel est marquée `[ZV]` dans la réponse. Le lore canon n'est jamais taggé.
- **Priorité d'affichage** : en cas de conflit, présenter la version `[ZV]` comme version principale. Indiquer la divergence canon **en fin de paragraphe, entre parenthèses**, sous la forme : *(Canon : [résumé de la version officielle].)*
- **Pas de conflit** : si le lore personnel étend le canon sans le contredire, présenter les deux naturellement — canon d'abord, puis `[ZV]` en complément.
- **Sujet purement canon** : si aucune entrée `[ZV]` ne concerne le sujet, répondre normalement via les sources web, sans mentionner l'absence de lore personnel.

### Ajouter ou modifier du lore personnel

Quand l'utilisateur dit "ajoute à mon lore que..." ou formulation équivalente :
1. Lire `INDEX.md` pour vérifier qu'une entrée similaire n'existe pas déjà
2. Identifier le fichier de catégorie approprié
3. Ouvrir ce fichier et ajouter l'entrée au format standard
4. Mettre à jour la table dans `INDEX.md`
5. Repackager sur commande `/maj`

---

## Format de réponse

- **Ton** : Neutre et factuel. Pas de style "in-universe" sauf si explicitement demandé.
- **Structure** : Répondre en prose claire. Utiliser des titres et listes si la question couvre plusieurs aspects (ex : "parle-moi des Eldars" → factions, histoire, culture, unités notables).
- **Citations de sources** : Mentionner la source principale utilisée en fin de réponse ou inline si pertinent (ex : *"Lexicanum"*, *"Codex: Tyranids 9e édition"*).
- **Longueur** : Proportionnelle à la complexité de la question. Une question simple = réponse concise. Une demande de vue d'ensemble = développement structuré.
- **Incertitude** : Si une information n'est pas trouvée ou est ambiguë, le dire explicitement plutôt que de spéculer.
- **Marquage `[ZV]`** : voir section *Lore personnel* ci-dessus. Ne jamais oublier le tag quand du lore personnel est cité.

---

## Exemples de déclenchement

| Question utilisateur | Action |
|---|---|
| "C'est quoi les Custodes ?" | Vérifier `personal-lore.md` → Fetch Lexicanum `Adeptus_Custodes`, synthétiser |
| "Qui a tué Sanguinius ?" | Vérifier `personal-lore.md` → Fetch Lexicanum `Sanguinius`, section "Death" |
| "Quelle est la timeline de l'Hérésie d'Horus ?" | Vérifier `personal-lore.md` → Search + Fandom pour vue chronologique |
| "C'est quoi la Great Rift ?" | Vérifier `personal-lore.md` → Lexicanum `Cicatrix_Maledictum` |
| "Parle-moi des Eldars Noirs" | Vérifier `personal-lore.md` → Lexicanum `Drukhari` + Fandom |
| "Quelle est la différence entre un Dreadnought et un Redemptor ?" | Vérifier `personal-lore.md` → Wahapedia + Lexicanum |
| "[Sujet présent dans personal-lore.md]" | Lire l'entrée `[ZV]`, chercher le canon si nécessaire, fusionner selon les règles de conflit |
| "Ajoute à mon lore que X" | Ouvrir `personal-lore.md`, ajouter l'entrée au format standard |

---

## Notes importantes

- **WH40K ≠ Warhammer Fantasy ≠ Age of Sigmar** : trois univers distincts. Cette skill couvre uniquement **Warhammer 40,000** (M41–M42).
- **Horus Heresy** (30K) est canon dans WH40K mais constitue une période distincte (env. M30–M31). Les questions sur la HH sont dans le scope.
- **Editions** : le lore peut varier selon l'édition des règles. Quand pertinent, préciser l'édition de la source.
