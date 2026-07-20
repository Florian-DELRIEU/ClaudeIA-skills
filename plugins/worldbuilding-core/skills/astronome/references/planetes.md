# Référence — Planètes

Valeurs et relations pour juger la nature et la plausibilité d'une planète : type, densité vs composition, gravité de surface, rétention d'atmosphère, champ magnétique. Ordres de grandeur.

## Sommaire
- Types de planètes
- Relation masse–rayon
- Densité ↔ composition
- Gravité de surface et vitesse de libération
- Rétention atmosphérique (« rivage cosmique »)
- Champ magnétique et climat

## Types de planètes

| Type | Masse indicative | Rayon indicatif | Composition |
|------|------------------|-----------------|-------------|
| **Planète tellurique** | ≲ 2 M⊕ | ≲ 1,5 R⊕ | roche + métal (silicates, noyau de fer) |
| **Super-Terre** | ~2–10 M⊕ | ~1,3–2 R⊕ | rocheuse massive, parfois océan global |
| **Mini-Neptune** | ~2–10 M⊕ | ~2–4 R⊕ | noyau rocheux + enveloppe épaisse H/He ou eau |
| **Géante de glace** | ~10–20 M⊕ | ~3,5–4 R⊕ | eau/ammoniac/méthane + noyau (Uranus, Neptune) |
| **Géante gazeuse** | ≳ 50 M⊕ à ~13 M_Jup | ~0,8–1,2 R_Jup | H/He massif (Jupiter, Saturne) |
| **Naine brune** | > 13 M_Jup | ~1 R_Jup | fusion du deutérium — n'est plus une planète |

**Vallée des rayons (Fulton gap)** : creux observé vers **1,5–2 R⊕** séparant les planètes rocheuses « nues » des planètes à enveloppe gazeuse. Une planète pile dans ce creux est possible mais moins commune.

**Plateau des géantes** : au-delà de ~0,5 M_Jup, ajouter de la masse **n'augmente presque plus le rayon** (la gravité comprime le gaz, dégénérescence). Une géante de 5 M_Jup a un rayon ~ celui de Jupiter, pas 5× plus grand. Erreur fréquente en fiction : « géante énorme » de rayon démesuré.

## Relation masse–rayon (par raisonnement)

- **Rocheux** : `R/R⊕ ≈ (M/M⊕)^~0,27` (croissance lente). Doubler la masse n'augmente le rayon que de ~20 %.
- **Géantes** : rayon quasi constant ~1 R_Jup sur une large plage de masses, puis légère décroissance aux très fortes masses.

## Densité ↔ composition

La densité moyenne (masse/volume, exprimée ici en g/cm³) trahit la composition. Contrôler la cohérence densité ↔ nature annoncée :

| Densité (g/cm³) | Composition typique | Exemples |
|-----------------|---------------------|----------|
| **7–8+** | riche en fer (gros noyau métallique) | Mercure ~5,4 (mais dénoyauté) |
| **4–5,5** | tellurique « Terre » (roche + fer) | Terre ~5,5, Vénus ~5,2 |
| **3–4** | rocheux/silicaté, pauvre en fer | Lune ~3,3, Mars ~3,9 |
| **1,5–3** | monde d'eau/glace, mixte | lunes glacées, Neptune ~1,6 |
| **0,7–1,7** | géante gazeuse | Jupiter ~1,3, **Saturne ~0,69** (< eau !) |

Incohérences à repérer : une planète « rocheuse » de densité 1,2 (trop légère), un « monde de fer » de densité 3, une « petite planète dense » dont masse et rayon donnent en réalité une densité de géante gazeuse. **Toujours recalculer** `ρ ∝ M/R³` si masse et rayon sont donnés :
`ρ/ρ⊕ = (M/M⊕)/(R/R⊕)³`, avec ρ⊕ ≈ 5,5 g/cm³.

## Gravité de surface et vitesse de libération

- **Gravité de surface** : `g/g⊕ = (M/M⊕)/(R/R⊕)²`, g⊕ ≈ 9,81 m/s².
  Exemple : super-Terre M = 5 M⊕, R = 1,6 R⊕ → g ≈ 5/1,6² ≈ 5/2,56 ≈ **1,95 g** (près de 2 g en surface : lourd mais pas absurde).
- **Vitesse de libération** : `v_lib/v_lib⊕ = √[(M/M⊕)/(R/R⊕)]`, v_lib⊕ ≈ 11,2 km/s.

Sert à juger si une gravité annoncée (« gravité double », « faible pesanteur ») est compatible avec la masse et le rayon donnés.

## Rétention atmosphérique (« rivage cosmique »)

Une planète ne garde une atmosphère que si sa **vitesse de libération dépasse largement la vitesse d'agitation thermique** des molécules de gaz (échappement de Jeans). Règle empirique : rétention durable si `v_lib ≳ 6 × v_thermique` du gaz considéré.

- La vitesse thermique **augmente avec la température** (proximité de l'étoile) et **diminue avec la masse molaire** du gaz. Donc : H₂ et He s'échappent facilement (légers) ; N₂, O₂, CO₂ sont bien plus faciles à retenir (lourds).
- **Petits corps chauds** → perdent tout (Mercure, Lune : pas d'atmosphère). **Corps massifs et/ou froids** → gardent même les gaz légers (géantes).
- Notion de **« rivage cosmique »** (cosmic shoreline) : dans un plan éclairement–vitesse de libération, une frontière sépare les corps qui gardent une atmosphère de ceux qui l'ont perdue. Une petite planète très proche de son étoile qui prétend garder une atmosphère épaisse est **suspecte**.
- **Facteur aggravant** : le vent stellaire et les éruptions (naines M jeunes) arrachent l'atmosphère → un **champ magnétique** protège en déviant le vent stellaire.

Incohérence classique : monde type Mars (petit, faible gravité) censé garder une atmosphère dense et respirable sur le long terme sans mécanisme de réapprovisionnement.

## Champ magnétique et climat

- **Champ magnétique** : nécessite un intérieur conducteur fluide en mouvement (noyau métallique liquide) + rotation suffisante (effet dynamo). Protège l'atmosphère de l'érosion par le vent stellaire et la surface du rayonnement. Une planète lente et/ou au noyau figé (comme Mars aujourd'hui) a un champ faible → atmosphère vulnérable.
- **Tectonique / cycle carbone-silicate** : sur Terre, ce cycle régule le CO₂ et donc le climat sur le long terme (thermostat géologique) — un ingrédient important pour une habitabilité stable et durable.
- **Rotation** : une rotation trop lente (ou verrouillage de marée) affecte le champ magnétique et la redistribution de chaleur (voir `mecanique-orbitale.md` et `habitabilite.md`).
