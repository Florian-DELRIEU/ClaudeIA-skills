# GM-Worlds — moteur à jets d100 (référence)

Simule la vie géopolitique d'une carte Azgaar, tour par tour, en s'appuyant sur des
**jets de d100 lancés par Florian** (même logique que `/gm-basic`) plutôt que sur un
générateur aléatoire interne. Le moteur ne modifie jamais les données de jeu — il
lit, propose les jets, interprète les résultats fournis, et écrit deux notes.

## Répartition des rôles : /azgaars interprète, /gm-worlds joue

`/azgaars` est **l'interprète** : il sait lire un `.map` et comprendre toutes ses
strates (reliefs/biomes, forces militaires, industrie, provinces, diplomatie...) via
sa couche d'interprétation (`m.strategic_snapshot()` et les méthodes qu'elle
assemble — `state_power`, `dominant_biomes`, `current_wars`, `aggression_of`...).
`/gm-worlds` ne réimplémente **aucune** lecture : il appelle cette API pour obtenir
la photographie du monde, et n'ajoute que ce qui est spécifique au jeu — la logique
de jets (`build_pending_checks`/`resolve_checks`), le suivi de continuité (score de
guerre, cooldown de paix) et la comparaison dans le temps (`diff_snapshots`, qui
compare deux photographies successives — ce n'est pas de la lecture pure, donc ça
reste côté gm-worlds).

Concrètement : `world_snapshot(m)` dans `gmw.py` n'est qu'un alias de
`m.strategic_snapshot()`. Si une nouvelle information de lecture est nécessaire un
jour (nouvelle mécanique FMG, nouveau champ), elle s'ajoute dans `/azgaars`, jamais
directement dans `/gm-worlds` — pour que tout autre skill construit sur des
sauvegardes Azgaar en bénéficie aussi.

## Le cycle en deux commandes

1. **`checks`** — lit l'état actuel du fichier, compare au bilan mémorisé pour
   détecter ce que Florian a changé depuis la dernière fois, puis énumère les jets à
   faire pour le tour à venir : chaque jet a un `id`, une description, et soit une
   **cible** (jets de déclenchement) soit un **modificateur** (jets de bataille).
   Écrit la liste dans le bilan (`gmworlds-fingerprint`) — aucune autre donnée.
2. **`resolve --rolls id=valeur,...`** — reprend les jets en attente, applique
   chaque résultat fourni via les tables d'interprétation, produit événements +
   directives, met à jour le bilan et la chronique, sauvegarde.

Un jet annoncé mais non fourni à `resolve` est ignoré (aucun effet ce tour) — jamais
de remplissage par un aléa caché.

## Pourquoi des jets plutôt qu'un aléa interne

Version précédente : le moteur tirait lui-même tous les résultats (Python
`random`), Florian n'avait aucune prise sur le hasard. Désormais, les décisions
probabilistes à enjeu réel (bataille, déclaration de guerre, révolte...) passent par
un vrai jet que Florian lance et dont il connaît le résultat avant même que Claude
l'interprète — plus transparent, plus proche d'une partie de JDR classique, et
cohérent avec le fonctionnement déjà établi de `/gm-basic`.

## Quels événements méritent un jet (et lesquels non)

Reprend le principe de `/gm-basic` : un jet seulement si **l'issue est incertaine ET
l'enjeu réel**.

- **Batailles** : plafonnées à `--max-batailles` (défaut 6) par tour, sauf cooldown
  de paix. Priorité aux guerres déjà engagées (score de guerre élevé en valeur
  absolue — les finir réduit la charge de dés des tours suivants) puis à la
  puissance combinée des deux camps. Les fronts non tirés ce tour sont listés en
  rappel (`suggestionsSansJet`), repris en priorité au tour suivant s'ils restent
  pertinents.
- **Solidarité d'alliance (coalition)** : pour chaque guerre en cours, un allié
  (statut `Ally` réel, lu dans la diplomatie) de l'un des deux belligérants peut
  être entraîné dans le conflit contre l'autre camp. Plafonné à 2 candidats par
  tour, triés par agressivité de l'allié potentiel. Un succès ne crée PAS de combat
  à N camps : Florian passe simplement la diplomatie du nouvel entrant à `Enemy`,
  ce qui fait apparaître un nouveau jet de bataille (bilatéral, comme les autres)
  au tour suivant — chaque paire en guerre reste résolue indépendamment.
- **Diplomatie** : les paires de voisins ne génèrent PAS toutes un jet (sur une
  grande carte, ce serait des dizaines de d100 par tour). Le moteur classe les
  candidats par significativité (agressivité combinée, statut) et n'en retient que
  les plus marquants : jusqu'à 4 tensions, 2 rapprochements, 2 velléités de guerre.
- **Interne** (révolte/essor) : révolte plafonnée aux 5 cas les plus significatifs
  (déficit de stabilité + fracture culturelle/religieuse, cf. plus bas) ; essor non
  plafonné mais naturellement rare.
- **Économie concrète** (cartes 46 blocs, module Économie uniquement) : pénurie
  (3 cas max), boom commercial (2 cas max), embargo (2 cas max) — voir formules
  ci-dessous. Silencieusement absents sur les cartes 39 blocs.
- **Réarmement** : PAS de jet — ce n'est ni incertain (c'est une décision
  économique) ni dramatiquement engageant. Reste une simple suggestion informative.

## Calcul des cibles et modificateurs

- **Bataille** : modificateur = puissance militaire pondérée par la stabilité de
  chaque camp (défenseur +15 %), ramenée à un ratio, mis à l'échelle ±35. Florian
  lance 1d100, additionne le modificateur annoncé, lit la bande de résultat.
- **Tension** : cible = 3,5 × chaos × (agressivité A + agressivité B) × (1 si déjà
  Rival/Suspicion, 0,35 sinon), plafonnée à [2, 88].
- **Rapprochement** : cible fixe à 10 (candidats : paires commerçantes en
  Neutral/Friendly).
- **Velléité de guerre** : cible = 12 × agressivité × chaos, plafonnée à [2, 85]
  (candidats : paires déjà Rival, moins de 2 fronts ouverts).
- **Révolte** : cible = déficit de stabilité (comme avant, `max(0, 0,3−stabilité)×300`)
  **+ fracture culturelle** (`(1 − part de la culture dominante) × 45`, via
  `m.dominant_cultures()`) **+ fracture religieuse** (`(1 − part de la religion
  dominante) × 25`, via `m.dominant_religions()`), plafonnée à 90. Un grand état
  stable mais multiculturel (ex. Ritimontia sur Comia, 57 % d'une seule culture)
  génère donc un vrai risque de révolte même sans crise de stabilité — plafonné aux
  5 cas les plus significatifs par tour (sinon presque tous les états d'une carte
  diverse généreraient un jet à faible cible). La description du jet indique la
  raison dominante (stabilité et/ou % de la culture/religion majoritaire) pour que
  la narration s'appuie dessus.
- **Essor** : cible dérivée de l'écart entre la stabilité synthétique et 0,85,
  plafonnée à [10, 80] — inchangé, pas de lien à la fracture culturelle (l'essor
  reste un phénomène de prospérité, pas de cohésion identitaire).
- **Pénurie** : pour chaque bien détenu par au moins 3 états (moyenne comparative
  significative), on calcule l'écart relatif du stock d'un état à la moyenne des
  autres états qui le détiennent (`m.good_stock_by_state()`). Le bien le plus en
  écart négatif (**stock > 0 exigé** — un stock nul est une absence structurelle,
  pas un événement, cf. note ci-dessous) devient candidat si l'écart est ≤ −60 %.
  Cible = `min(75, |écart| × 40 × chaos)`.
- **Boom commercial** : même mécanique côté positif — bien le plus en écart *positif*
  (≥ +80 %) par rapport à la moyenne des autres états. Cible = `min(70, écart × 25 ×
  chaos)`. Distinct de l'essor : un état peut prospérer sur un bien précis sans
  connaître un âge d'or général, et vice-versa.
- **Embargo** : parmi les paires d'états ayant un flux commercial réel significatif
  (`m.trade_flows_by_state()`, ≥ 15 % du flux bilatéral maximum de la carte) ET une
  diplomatie tendue (Suspicion/Rival/Enemy, hors paires déjà en guerre — l'embargo
  y est déjà de facto acquis), cible = `min(70, flux_relatif × 45 × multiplicateur_
  tension × chaos)` (multiplicateur 0,6/1,0/1,3 selon Suspicion/Rival/Enemy).

**Note sur pénurie/boom** : ces deux mécaniques reposent sur les VRAIES données de
stock du module Économie (`good_stock_by_state`), pas sur une abstraction. Un stock
strictement nul est explicitement exclu du calcul de pénurie — la plupart du temps
ça signifie juste que l'état n'a jamais produit ce bien (rien à raconter), alors
qu'un stock faible mais non-nul, nettement sous la moyenne des autres, signale une
vraie rareté relative qui mérite un jet.

Bandes d'un jet de déclenchement (roll vs cible T) : `≤ T×0,15` → critique ;
`≤ T` → succès ; `≤ T + (100−T)×0,35` → partiel ; au-delà → échec.

## Cooldown de paix

Quand une guerre se conclut (score de guerre décisif), la paire passe en cooldown
(6 tours) : plus de jet de bataille proposé sur cette paire tant que le cooldown est
actif, avec un rappel explicite si Florian n'a pas encore appliqué le changement de
diplomatie dans FMG. Le cooldown décompte à chaque `checks`, indépendamment de ce
que montre le fichier — le temps que Florian ait l'occasion de faire le changement.

## Ce que le moteur écrit (et rien d'autre)

| Note / champ | Contenu | Risque |
|---|---|---|
| `gmworlds-fingerprint` | JSON technique : jets en attente, scores de guerre, cooldowns, dernière photographie complète | Aucun — note pure |
| `gmworlds-chronicle` | Chronique HTML lisible dans le panneau Notes de FMG | Aucun |
| `options.year` | Année courante | Aucun (donnée pure) |

Diplomatie, régiments, provinces, zones, alerte restent **intégralement sous le
contrôle de Florian** dans FMG.

## Source de vérité : toujours le fichier

Les guerres en cours sont relues à chaque `checks` depuis `states[].diplomacy`
(statuts `Enemy`), jamais depuis une liste interne. Seuls le score de guerre
(momentum) et le cooldown de paix — non représentables nativement dans FMG — sont
mémorisés d'un tour à l'autre.

## Mode secondaire : `advance`

`python3 gmw.py advance <carte.map> -n N [--out X] [--chaos 1.0]` fait tourner le
moteur avec un générateur aléatoire interne (pas les dés de Florian) — utile pour
tester le moteur ou pré-remplir rapidement une chronique, mais **ce n'est pas le
flux principal du skill**. Le flux documenté et attendu est `checks` → (jets de
Florian) → `resolve`.

## Limites assumées

- Les pertes suggérées sont globales par état (en % de l'effectif), pas régiment
  par régiment : à Florian de décider comment les répartir dans l'éditeur.
- Aucune garantie que Florian applique une directive donnée — voulu. Le prochain
  `checks` s'adapte à ce qui a réellement été fait (via `changementsDetectes`).
- Sur une carte à nombreuses rivalités préexistantes (beaucoup de statuts `Enemy`
  dès le départ), le premier tour peut demander beaucoup de jets de bataille d'un
  coup — c'est une lecture fidèle de l'état initial du fichier, pas un artefact du
  moteur ; le nombre se régule ensuite au fil des paix conclues.
