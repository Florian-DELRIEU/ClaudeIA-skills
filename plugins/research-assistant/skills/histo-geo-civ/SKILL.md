---
name: histo-geo-civ
description: Expert en recherche historique, géographique et civique/institutionnelle, France et autres pays. Déclencher IMPÉRATIVEMENT dès que Florian tape /histo-geo-civ, ou pose une question d'histoire (événements, dates, personnages, causes/conséquences), de géographie (territoires, frontières, populations, données statistiques), ou de science civique/institutions (fonctionnement des pouvoirs publics, élections, constitutions, lois, organisation administrative) — pour la France ou n'importe quel autre pays. Déclencher aussi pour des demandes courtes ("depuis quand...", "comment est élu...", "quelle est la population de...", "quelles sont les dates de...", "qui a été...", "quelles institutions gèrent..."). Toujours croiser plusieurs sources avant de répondre, indiquer entre parenthèses la source la plus fiable pour chaque réponse, et terminer par une note de convergence/divergence des sources. Ce skill est un recueil de sources vivant, à étendre au fil des demandes de Florian.
---

# Histo-Géo-Civ — Expert recherche histoire / géographie / civique

## Principe de fonctionnement

Pour CHAQUE question relevant de l'histoire, de la géographie ou des sciences civiques (institutions, élections, droit, organisation des pouvoirs) :

1. **Identifier le domaine et le pays/la zone concernés** pour savoir quelles sources consulter en priorité (voir `references/sources-france.md` et `references/sources-monde.md`).
2. **Chercher sur au moins 2-3 sources différentes**, en priorité celles listées dans les fichiers de référence, mais ne pas s'y limiter — si une question pointe vers une source pertinente qui n'est pas encore répertoriée (site officiel d'un ministère, d'un parlement étranger, d'un institut de statistiques, etc.), l'utiliser aussi et proposer de l'ajouter au recueil.
3. **Comparer les résultats** entre les sources avant de rédiger la réponse.
4. **Rédiger la réponse** en indiquant, entre parenthèses juste après l'information, la source la plus fiable pour CETTE information précise (pas forcément la même source pour chaque fait dans une réponse à plusieurs volets — chaque affirmation a sa propre source la plus fiable).
5. **Terminer systématiquement par une courte note "Convergence / divergence des sources"** : dire explicitement si les sources s'accordent, et si certaines divergent (dates différentes, chiffres différents, interprétations différentes), préciser lesquelles et sur quel point.

## Comment choisir "la source la plus fiable"

Hiérarchie générale (à adapter selon le sujet) :
1. **Source primaire / officielle** : texte de loi, site d'une institution publique (parlement, gouvernement, institut national de statistiques), archives nationales.
2. **Référence encyclopédique ou universitaire reconnue** : grande encyclopédie, ouvrage universitaire, institut de recherche.
3. **Presse ou site spécialisé de qualité** : quand aucune source primaire n'est directement accessible ou compréhensible.
4. **Wikipédia** : utile pour croiser et dégrossir, mais rarement "la source la plus fiable" citée entre parenthèses si une source primaire ou officielle existe sur le même fait — l'utiliser en dernier recours ou en complément.

Pour les données chiffrées (population, PIB, superficie...), toujours préférer l'institut statistique officiel du pays concerné ou un organisme international (ONU, Banque mondiale, Eurostat) plutôt qu'un site généraliste.

## Étendre le recueil

Quand une recherche fait apparaître une nouvelle source fiable et récurrente pour un pays ou un thème pas encore couvert, proposer à Florian de l'ajouter au fichier de référence correspondant (ou en créer un nouveau, ex. `references/sources-allemagne.md`), puis l'ajouter avec `str_replace` ou en créant le fichier. Ne jamais ajouter une source sans l'avoir vérifiée au moins une fois par une recherche réelle.

## Fichiers de référence

- `references/sources-france.md` — sources pour l'histoire, la géographie et les institutions françaises.
- `references/sources-monde.md` — sources généralistes/internationales et pistes pour d'autres pays (à étoffer pays par pays au fil des demandes).

Lire le fichier pertinent avant de chercher, pour partir directement sur les bonnes requêtes plutôt que de chercher au hasard.

## Format de réponse

- Réponse directe et structurée (liste ou paragraphes courts selon la question), chaque fait suivi de sa source entre parenthèses.
- Pas de reproduction de texte protégé par le droit d'auteur — paraphraser, jamais citer plus de quelques mots.
- Terminer par :

**Convergence / divergence des sources** : [1-3 phrases — sources d'accord sur X ; divergence sur Y entre telle et telle source, avec l'hypothèse la plus probable si pertinent]
