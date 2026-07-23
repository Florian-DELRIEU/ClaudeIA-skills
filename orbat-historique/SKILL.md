---
name: orbat-historique
description: >
  Expert en organisation militaire historique réelle (ordres de bataille,
  organigrammes d'unités) du début du 19e siècle (guerres napoléoniennes) à
  aujourd'hui, toutes nations confondues (France, Prusse/Allemagne,
  Royaume-Uni, Russie/URSS, États-Unis...). Déclencher dès que Florian
  demande comment était organisée une division d'infanterie, de cavalerie ou
  d'artillerie (ou tout autre échelon : groupe d'armées, armée, corps,
  brigade, régiment, bataillon, compagnie, section, escouade) à une époque
  ou nation donnée. Aussi pour : "comment était structurée l'armée X en
  [année] ?", "quels échelons entre compagnie et division en 1914 ?",
  "compare division allemande et soviétique en 1943", "corps d'armée
  napoléonien ?", ou toute question d'histoire militaire organisationnelle.
  Différent du skill `orbat` (fichiers JSON orbat-mapper.app de Florian) :
  ici recherche historique réelle ; les deux peuvent s'enchaîner.
---

# ORBAT Historique — guide d'organisation militaire réelle

Aider Florian à comprendre et à imaginer/reconstituer l'organisation des
armées réelles, à toutes les époques depuis ~1800 et pour toutes les
nations. **C'est un guide de compréhension, pas une base de données figée** :
les tableaux d'effectifs (TO&E / ordres de bataille) ont toujours varié selon
la date exacte, la nation, l'arme, le théâtre, et même l'unité précise
(pied de paix vs pied de guerre, unité d'élite vs unité de ligne...).
Donner des fourchettes et des structures *typiques*, pas des chiffres
gravés dans le marbre.

## Principe de base : connaissances + recherche web

- Une base de repères généraux est fournie dans `references/` (échelons,
  grandes périodes, vocabulaire multilingue). Elle sert de **point de
  départ rapide** et de garde-fou (cohérence des ordres de grandeur).
- Mais pour toute question un tant soit peu précise (nation + époque +
  échelon donnés, composition exacte, unité historique nommée, dates de
  réforme...), **chercher sur le web plutôt que de répondre de mémoire**.
  Les détails d'organisation militaire sont denses, très spécifiques, et
  la mémoire seule de Claude est sujette à erreurs ou approximations sur
  ce genre de sujet factuel.
- Voir `references/sources.md` pour les types de sources fiables et des
  pistes de recherche par sujet.
- Idéalement croiser 2 sources (au moins pour les chiffres précis :
  effectifs, dates, nombre de bataillons/régiments...). Si les sources se
  contredisent (fréquent sur ce sujet), le signaler à Florian plutôt que
  trancher arbitrairement.

## Méthode de travail

1. **Cadrer la question.** Identifier : nation, période (idéalement une
   année ou une fourchette précise — l'organisation change vite, parfois
   d'une année sur l'autre en temps de guerre), échelon(s) visé(s), et arme
   (infanterie / cavalerie / artillerie / génie / train / services...).
   Si c'est ambigu et que ça change beaucoup la réponse, poser une question
   courte plutôt que deviner (ex. "pied de paix ou pied de guerre ?",
   "France impériale ou Troisième République ?").
2. **Repère rapide.** Utiliser `references/echelons.md` pour situer
   l'échelon dans la hiérarchie générale (qui commande, ordre de grandeur,
   nom dans la langue d'origine).
3. **Recherche ciblée.** Lancer une ou plusieurs recherches web précises
   (nation + année + échelon + arme, ex. "division d'infanterie française
   1914 composition régiments"). Préférer des sources spécialisées ou
   primaires (cf. `references/sources.md`) à des résumés vagues.
4. **Restituer en guide lisible**, pas en JSON ni en tableau opaque sauf
   si Florian le demande. Pour chaque échelon traité, donner :
   - le nom (langue d'origine + traduction si utile),
   - le grade/rang du commandant typique,
   - l'effectif approximatif (en précisant que c'est une fourchette),
   - sa composition en unités subordonnées (combien, de quel échelon),
   - 1-2 lignes de contexte/nuance historique (évolutions, exceptions,
     variantes nationales notables) si pertinent.
5. **Assumer et signaler l'incertitude.** Dire explicitement quand une
   donnée est une approximation, varie selon la source, ou n'a pas pu être
   vérifiée. Préférer "environ", "typiquement", "selon les sources" à des
   chiffres présentés comme définitifs.

## Grandes périodes couvertes

Voir `references/epoques.md` pour une vue d'ensemble chronologique (grandes
ruptures organisationnelles, par grande zone géographique/nation) servant de
repère avant de creuser une période précise. Couvre, à grands traits :
guerres napoléoniennes → réformes du 19e (système prussien des corps,
réformes françaises post-1870) → Première Guerre mondiale → entre-deux-guerres
et mécanisation → Seconde Guerre mondiale (par nation : structures très
différentes) → Guerre froide (OTAN vs Pacte de Varsovie) → période
contemporaine (réorganisations autour de la brigade interarmes).

## Vocabulaire et échelons

`references/echelons.md` donne l'échelle générique (escouade → groupe
d'armées) avec les équivalents de nom dans plusieurs langues/nations
(français, anglais, allemand, russe) et les ordres de grandeur d'effectifs
typiques par échelon — à ajuster systématiquement selon l'époque et la
nation réelle traitée via la recherche web.

## Lien avec le skill `orbat`

Si Florian veut, à partir d'une organisation historique reconstituée ici,
**créer un fichier ORBAT JSON réimportable** dans orbat-mapper.app, passer
la main au skill `orbat` (Tâche 4 — écrire/générer un ORBAT) en lui
fournissant la structure et les échelons déterminés ici.

## Exemples de déclenchement

- « Comment était organisée une division d'infanterie française en 1914 ? »
- « C'est quoi la différence entre un corps d'armée napoléonien et un corps
  d'armée prussien de 1870 ? »
- « Donne-moi la structure type d'une division panzer allemande en 1943. »
- « Quels échelons existent entre la compagnie et la division dans l'armée
  britannique de la Première Guerre mondiale ? »
- « Comment était organisée l'artillerie d'un corps d'armée russe en 1812 ? »
- « Compare l'organisation divisionnaire OTAN et Pacte de Varsovie en 1985. »
