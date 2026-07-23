---
name: meme
description: Retrouve un mème (image macro, template connu, gif de réaction, screenshot viral) à partir d'une description en langage naturel ou d'un détail fourni par Florian (émotion, situation, personnage, réplique approximative, contexte). Déclencher IMPÉRATIVEMENT dès que Florian tape /meme, ou demande "trouve-moi un mème de...", "un mème où...", "le mème avec...", "j'ai besoin d'un mème pour...", ou toute formulation cherchant une image/gif précis plutôt qu'une image générique. Couvre aussi bien les mèmes fixes (templates, image macros) que les gifs de réaction. Propose plusieurs candidats avec liens directs, jamais une seule option imposée.
---

# /meme — Recherche de mème

Ce skill aide Florian à retrouver un mème précis à partir d'une description approximative (une scène, une émotion, un personnage, un template connu, un contexte, une réplique dont il ne se souvient qu'à moitié). Un "mème" ici peut être une image fixe (template, image macro), un gif de réaction, ou un screenshot viral — même principe de recherche pour les trois.

## Principe général

Florian donne souvent un détail flou ou partiel ("le mème où le mec renverse la table", "un mème de chat blasé", "le mème du gars qui a deux choix", "la scène où Thanos claque des doigts"). Le job de ce skill est de :

1. Reformuler ce détail en requêtes de recherche efficaces.
2. Chercher sur plusieurs fronts (recherche d'images + sites spécialisés).
3. Revenir avec **plusieurs candidats** (3 à 5), pas un seul, pour que Florian choisisse.

## Étape 1 — Reformuler la requête

Traduire la description de Florian en mots-clés courts et visuels, comme pour une recherche d'image classique :
- Ajouter "meme" ou "meme template" à la requête (ou "gif"/"reaction gif" si le détail suggère clairement une animation plutôt qu'une image fixe).
- Si c'est un mème connu, utiliser son nom s'il est identifiable ("distracted boyfriend", "this is fine dog", "drake hotline bling", "expanding brain", "two buttons").
- Si c'est une scène de film/série, inclure le titre + la scène + "meme" ou "gif" (ex : "The Office Michael Scott no meme").
- Si c'est une émotion/réaction générique (ex : "chat blasé", "quelqu'un qui panique"), garder ça simple : "cat unimpressed meme", "panic reaction meme".
- Ne jamais deviner un nom propre si Florian ne l'a pas donné — mieux vaut une requête descriptive plus large.

## Étape 2 — Chercher

Deux méthodes complémentaires, à utiliser ensemble ou en repli l'une de l'autre :

### A. `image_search`
Essayer d'abord avec le tool `image_search`. Ça marche bien pour les mèmes/réactions génériques (animaux, émotions, templates non protégés par un copyright spécifique).

⚠️ Limite connue : `image_search` bloque explicitement le contenu lié à des franchises/IP protégées (films, séries, personnages sous copyright, sport). Beaucoup de mèmes issus de scènes cultes de films/séries ne remonteront donc pas par ce biais — ce n'est pas une erreur du skill, c'est une restriction du tool.

### B. `web_search` + `web_fetch` vers les sites spécialisés
Pour tout ce qui touche à des scènes de films/séries/persos, ou pour des templates de mèmes précis que `image_search` ne renvoie pas :
- Chercher directement sur Knowyourmeme (pour identifier/nommer un mème et son origine), Giphy et Tenor (pour la version gif).
- Requêtes du type `site:knowyourmeme.com <description>`, `site:giphy.com <description>`, `site:tenor.com <description>`.
- `web_fetch` la page de résultats ou la page du mème pour récupérer l'URL directe ou confirmer le nom exact du template.
- Présenter le **lien vers la page** (pas de reproduction d'image protégée) plutôt que d'essayer de rapatrier le fichier — Florian peut cliquer et voir/télécharger lui-même.

## Étape 3 — Présenter les candidats

Toujours répondre avec plusieurs options courtes, jamais une seule affirmation "voici LE mème". Format compact adapté mobile :

```
Quelques pistes pour "<description>" :
1. [nom/courte description] — [lien ou image]
2. [nom/courte description] — [lien ou image]
3. [nom/courte description] — [lien ou image]
```

Si Florian précise ensuite ("non, plutôt celui où...", "c'est le 2 mais en version gif", "c'est ça mais je veux le nom du template"), relancer la recherche avec ce détail affiné plutôt que de redemander tout depuis le début.

## Cas limites

- **Détail insuffisant** ("un mème drôle") : demander une précision rapide (émotion ? source ? contexte d'usage ?) plutôt que de deviner au hasard.
- **Contenu sensible/NSFW/violent/haineux** : ne pas chercher, refuser poliment comme pour toute recherche d'image à contenu problématique.
- **Rien trouvé** : le dire clairement, proposer une requête alternative plutôt que d'inventer un lien.
