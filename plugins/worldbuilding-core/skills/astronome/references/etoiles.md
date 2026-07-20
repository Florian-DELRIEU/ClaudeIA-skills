# Référence — Étoiles

Valeurs de référence pour juger une étoile fictive : type, luminosité, durée de vie, effets sur ses planètes, et stabilité des systèmes multiples. Toutes les valeurs sont des ordres de grandeur.

## Sommaire
- Classes spectrales de la séquence principale
- Relations clés (masse–luminosité, durée de vie, zone habitable)
- Au-delà de la séquence principale (géantes, naines blanches, restes)
- Naines brunes
- Systèmes multiples (stabilité)
- Effets d'une étoile sur ses planètes

## Classes spectrales de la séquence principale

Mnémonique O-B-A-F-G-K-M, du plus chaud/massif au plus froid/léger. Valeurs approximatives (M☉, L☉, K) :

| Classe | Masse (M☉) | Luminosité (L☉) | Temp. (K) | Couleur | Durée de vie séq. princ. | Fréquence |
|--------|-----------|-----------------|-----------|---------|--------------------------|-----------|
| **O** | > 16 | 30 000 – 10⁶+ | > 33 000 | bleue | ~1–10 Ma | ~0,00003 % (extrêmement rare) |
| **B** | 2,1 – 16 | 25 – 30 000 | 10 000 – 33 000 | bleu-blanc | ~10–350 Ma | ~0,1 % |
| **A** | 1,4 – 2,1 | 5 – 25 | 7 500 – 10 000 | blanche | ~0,4–3 Ga | ~0,6 % |
| **F** | 1,04 – 1,4 | 1,5 – 5 | 6 000 – 7 500 | blanc-jaune | ~3–7 Ga | ~3 % |
| **G** | 0,8 – 1,04 | 0,6 – 1,5 | 5 200 – 6 000 | jaune (Soleil) | ~7–15 Ga | ~7,5 % |
| **K** | 0,45 – 0,8 | 0,08 – 0,6 | 3 700 – 5 200 | orange | ~15–70 Ga | ~12 % |
| **M** | 0,08 – 0,45 | < 0,08 | 2 400 – 3 700 | rouge | ~70 Ga – plusieurs milliers de Ga | ~76 % (la plus courante) |

Repères : le Soleil est G2V, 1 M☉, 1 L☉, ~5 780 K, ~10 Ga de durée de vie totale (déjà ~4,6 Ga écoulés).

**Conséquence majeure pour la fiction** : les étoiles O, B et A vivent trop peu de temps pour qu'une vie complexe (a fortiori une civilisation) ait pu apparaître. Une vie « ancienne de milliards d'années » n'est crédible qu'autour d'une F tardive, G, K ou M. Les naines K et M sont les meilleures candidates pour la longévité (K = « Goldilocks stars », bon compromis longévité/activité modérée).

## Relations clés (à appliquer par raisonnement)

**Masse → luminosité** (M en unités solaires) :
- Régime intermédiaire : `L ≈ M^3,5`
- Faibles masses (M ≲ 0,43 M☉) : plus proche de `L ≈ M^2,3`
- Fortes masses : exposant plus faible (~1–2)

Exemple : une étoile de 0,5 M☉ → L ≈ 0,5^3,5 ≈ 0,088 L☉ (cohérent avec une M/K précoce).

**Durée de vie sur la séquence principale** :
`t ≈ 10 Ga × (M/L)` → avec L ≈ M^3,5, cela donne `t ≈ 10 Ga × M^(−2,5)`.
- 2 M☉ → t ≈ 10 × 2^(−2,5) ≈ 1,8 Ga
- 0,5 M☉ → t ≈ 10 × 0,5^(−2,5) ≈ 57 Ga (dépasse l'âge de l'Univers, ~13,8 Ga)
- 0,1 M☉ → des milliers de Ga

**Distance de la zone habitable** : le flux reçu décroît en 1/r², donc pour retrouver l'éclairement terrestre il faut `r_HZ ≈ √(L/L☉)` UA (centre ~1 UA pour le Soleil).
- L = 0,04 L☉ → r_HZ ≈ √0,04 = 0,2 UA
- L = 4 L☉ → r_HZ ≈ 2 UA
(Bornes précises dans `habitabilite.md`.)

## Au-delà de la séquence principale

- **Géantes rouges** : après épuisement de l'hydrogène central, l'étoile enfle énormément et se refroidit en surface tout en devenant très lumineuse. La zone habitable se déplace **vers l'extérieur**, les planètes internes peuvent être **englouties** ou grillées. Phase relativement brève (Ma à ~1 Ga selon la masse). Un monde « stable et habité » autour d'une géante rouge est douteux sauf lune lointaine récemment réchauffée.
- **Naines blanches** : reste dégénéré d'une étoile ≲ 8 M☉, taille terrestre, très dense, se refroidit lentement. Luminosité faible et déclinante → zone habitable très proche et rétrécissante. Habitabilité possible en théorie mais transitoire et exotique.
- **Étoiles à neutrons / trous noirs** : restes d'étoiles massives. Environnement radiatif extrême, pas de zone habitable classique. Réservés à la fiction très « hard » et assumée.
- **Variables (céphéides, etc.)** : luminosité pulsante → éclairement instable, mauvais pour l'habitabilité.

## Naines brunes

Objets sub-stellaires (~13–80 M_Jupiter) incapables de fusionner l'hydrogène de façon soutenue. Très peu lumineuses et se refroidissant avec le temps → une planète « habitable » autour d'une naine brune devrait être extrêmement proche, verrouillée par les marées, avec une fenêtre temporelle qui se referme. Frontière planète/naine brune : ~13 M_Jup (seuil de fusion du deutérium).

## Systèmes multiples (stabilité)

Plus de la moitié des étoiles sont en systèmes multiples. Deux configurations pour une planète :

- **Orbite circumstellaire (S-type)** : la planète tourne autour d'**une** des deux étoiles. Stable si son demi-grand axe reste petit devant la séparation du binaire — règle empirique : `a_planète ≲ ~0,2–0,3 × a_binaire` (dépend des masses et de l'excentricité du binaire). Au-delà, la seconde étoile déstabilise l'orbite.
- **Orbite circumbinaire (P-type)** : la planète tourne autour des **deux** étoiles à la fois (« coucher de deux soleils » à la Tatooine). Stable seulement **au-delà** d'un rayon critique : `a_planète ≳ ~2–4 × a_binaire` (typiquement ~3× ; croît avec l'excentricité du binaire).

Entre ces deux zones : région instable où aucune orbite pérenne n'existe. Pour la fiction : un « deux soleils dans le ciel » suppose soit un binaire serré avec planète circumbinaire lointaine, soit une seconde étoile lointaine vue comme un astre très brillant.

Cohérence des couleurs/effets : deux étoiles de types différents éclairent avec des teintes et des flux différents, décalent la zone habitable combinée, et créent des cycles d'éclairement complexes — à décrire de façon cohérente.

## Effets d'une étoile sur ses planètes

- **Flux UV / X** : croît fortement avec la température (étoiles chaudes = beaucoup d'UV, stérilisant sans atmosphère/ozone protecteurs).
- **Éruptions et vent stellaire** : les **naines M** jeunes sont très actives (éruptions violentes, vent intense) → érosion atmosphérique des planètes proches, dose de rayonnement élevée. Atténuation nécessaire : champ magnétique fort + atmosphère épaisse.
- **Zone de verrouillage** : autour des étoiles peu lumineuses, la zone habitable est si proche que les planètes s'y verrouillent par effet de marée (voir `mecanique-orbitale.md` et `habitabilite.md`).
- **Évolution** : l'étoile devient plus lumineuse en vieillissant (le Soleil gagne ~10 %/Ga), déplaçant lentement la zone habitable vers l'extérieur — pertinent pour l'histoire longue d'un monde.
