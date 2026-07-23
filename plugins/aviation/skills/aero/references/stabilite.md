# Référence — Stabilité statique et dynamique

Comment l'avion réagit à une perturbation. **Statique** = tendance initiale (revient-il ?). **Dynamique** = comportement dans le temps (l'oscillation s'amortit-elle ?).

## Sommaire
- Statique vs dynamique
- Stabilité longitudinale statique (centrage, point neutre, marge)
- Effet du centrage sur le pilotage
- Stabilité latérale statique (dièdre)
- Stabilité directionnelle statique (dérive)
- Modes dynamiques longitudinaux (incidence, phugoïde)
- Modes dynamiques latéraux-directionnels (roulis, spiral, roulis hollandais)
- Le compromis dièdre / dérive
- Amortisseurs et commandes de vol

## Statique vs dynamique

- **Statiquement stable** : après une rafale, l'avion développe un moment qui le **ramène** vers l'équilibre. Statiquement instable : il s'en écarte davantage. Neutre : il reste où on l'a mis.
- **Dynamiquement stable** : les oscillations qui suivent **s'amortissent** avec le temps. Dynamiquement instable : elles **grossissent** (divergence). Un avion peut être statiquement stable mais dynamiquement instable (il revient mais en oscillant de plus en plus).

## Stabilité longitudinale statique (tangage)

C'est la stabilité en **tangage**, gouvernée par la position du **centre de gravité (CG)** par rapport au **point neutre** (foyer de l'avion complet, ~ centre aérodynamique de l'ensemble aile+empennage).

- **Marge statique** : `MS = (x_pn − x_cg) / c̄` (fraction de la corde aérodynamique moyenne `c̄`). **MS > 0** (CG en avant du point neutre) → **stable**. MS = 0 → neutre. MS < 0 (CG derrière le point neutre) → **instable en tangage**.
- Mécanisme : si une rafale cabre l'avion, l'**empennage horizontal** voit son incidence augmenter, crée une portance qui **rabaisse le nez** → rappel. L'empennage est le stabilisateur.
- Les **limites de centrage** (avant/arrière) du manuel encadrent MS : jamais derrière la limite arrière (proche du point neutre = dangereux).

## Effet du centrage sur le pilotage

Le **chargement** déplace le CG, donc change tout le comportement — crucial en sim (carburant, armement, passagers).

- **CG avant** (lourd du nez) : grande marge statique → très **stable**, mais commandes de tangage **lourdes**, Vs plus **élevée** (l'empennage déporte vers le bas, il faut plus de portance à l'aile), et il faut **plus de profondeur** pour arrondir — risque d'atterrissage « plat » ou de manque d'autorité à l'arrondi.
- **CG arrière** (vers la limite) : petite marge → avion **vif, réactif, léger du manche**, meilleures performances (moins de traînée d'équilibrage), Vs plus basse — mais **moins stable**, phugoïde/incidence plus difficiles à amortir, et au-delà du point neutre : **incontrôlable** en tangage.
- **Conséquence sim** : un avion qui « pique tout seul » ou « part au cabré » peut être mal centré (soute mal remplie, carburant déséquilibré). Un avion « sur des rails mais mou » est centré avant.

## Stabilité latérale statique (roulis) — dièdre

Tendance à **remettre les ailes à plat** après un dérapage.

- Sources : **dièdre** (ailes relevées en V), **flèche**, **aile haute** (effet pendulaire). En dérapage, l'aile « au vent » voit une incidence/portance accrue → roulis qui redresse.
- Trop de dièdre → avion « paresseux » en roulis et sujet au **roulis hollandais**. Trop peu → sujet à l'**instabilité spirale**.
- **Conséquence** : les ailes hautes à fort dièdre (avions de brousse) se rétablissent seules mais roulent mollement ; les chasseurs à aile basse en roulent vif mais tolèrent le dérapage.

## Stabilité directionnelle statique (lacet) — dérive

Tendance de type **girouette** : le nez se remet **face au vent relatif** après un dérapage.

- Source principale : la **dérive** (empennage vertical). En dérapage, elle développe une force qui **aligne le nez** sur la trajectoire.
- Dérive trop petite → dérapages mal amortis, roulis hollandais ; trop grande → sensibilité excessive aux rafales latérales.

## Modes dynamiques longitudinaux

Deux oscillations en tangage :

- **Oscillation d'incidence (courte période)** : **rapide** (quelques secondes), **fortement amortie**. Variation d'incidence à vitesse quasi constante. Normalement bien amortie ; si elle ne l'est pas (centrage arrière), l'avion « rebondit » en tangage — désagréable et pilote-induit (PIO) possible.
- **Phugoïde (longue période)** : **lente** (20–60 s), **faiblement amortie**. Échange lent **altitude ↔ vitesse** à incidence quasi constante (le nez monte, l'avion ralentit, redescend, accélère…). Facile à contrer manuellement (petites corrections d'assiette) ou à laisser mourir. Un centrage arrière l'amortit moins bien.
- **Conséquence sim** : si l'avion ondule lentement en montagnes russes vitesse/altitude → c'est la phugoïde ; ne pas sur-corriger, la piloter au trim et en assiette.

## Modes dynamiques latéraux-directionnels

Trois modes en roulis/lacet :

- **Roulis subsident (roll subsidence)** : **rapide**, **très amorti**. Simple amortissement du taux de roulis — quand on lâche le manche, le roulis s'arrête net. Détermine la « vivacité » ressentie.
- **Mode spiral** : **lent**. Peut être **stable** (l'inclinaison revient) ou, souvent, **légèrement instable** : une petite inclinaison non corrigée s'accentue lentement → l'avion s'engage en **spirale descendante** (le nez tombe, la vitesse monte, le virage se resserre). Insidieux sans repères visuels (vol aux instruments / nuit).
- **Roulis hollandais (Dutch roll)** : oscillation **couplée lacet-roulis**, l'avion « se dandine » (le nez décrit un ∞, les ailes battent). Gênant, fatigant, dégrade la visée. Aggravé par **trop de dièdre relativement à la dérive** ; typique des ailes en flèche à haute altitude.

## Le compromis dièdre / dérive

Roulis hollandais et instabilité spirale tirent en **sens opposés** :

- **Beaucoup de dièdre / peu de dérive** → bon comportement spiral mais **mauvais roulis hollandais**.
- **Peu de dièdre / beaucoup de dérive** → roulis hollandais amorti mais **spirale divergente**.
- Les concepteurs cherchent un équilibre ; la plupart des avions acceptent une **légère instabilité spirale** (facile à contrer visuellement) pour garder un roulis hollandais discret.

## Amortisseurs et commandes de vol

- Les **jets** en flèche à haute altitude ont un roulis hollandais marqué → **amortisseur de lacet (yaw damper)** qui commande la direction automatiquement pour l'étouffer. En sim, un yaw damper coupé sur un jet en croisière → dandinement immédiat.
- Les commandes de vol électriques modernes peuvent piloter un avion **volontairement instable** (chasseurs à instabilité relaxée) pour la manœuvrabilité, en le stabilisant électroniquement — sans calculateur, il serait injouable.
- **Conséquence sim** : coupler ces aides (SAS/FBW/yaw damper) change radicalement le ressenti ; un warbird des années 40 n'a *aucune* de ces aides → toutes les tendances brutes s'expriment (voir hélices-pales pour les tendances moteur).
