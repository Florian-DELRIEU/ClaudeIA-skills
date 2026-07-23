# Référence — Lunes, anneaux & satellites

Critères pour juger lunes, anneaux et petits corps. Ordres de grandeur.

## Sommaire
- Formation des lunes
- Taille maximale d'une lune
- Verrouillage des lunes
- Chauffage de marée
- Limite de Roche & anneaux
- Longévité des anneaux
- Sous-lunes et lunes binaires
- Lunes capturées

## Formation des lunes

Trois voies principales, avec des signatures orbitales distinctes :

- **Co-accrétion** (satellites réguliers) : la lune se forme dans le disque autour de la planète → orbite **prograde, peu inclinée, quasi circulaire**, dans le plan équatorial. Cas des lunes galiléennes de Jupiter.
- **Impact géant** : une collision éjecte de la matière qui se ré-accrète en lune → grande lune relativement massive. Cas de la **Lune terrestre**.
- **Capture** : un corps passant est piégé → orbite souvent **inclinée, excentrique, parfois rétrograde**, généralement plus petite. Cas de **Triton** (Neptune), Phobos/Deimos (Mars).

Cohérence : une grande lune bien ronde en orbite équatoriale prograde est « naturelle » ; une lune rétrograde/inclinée suppose une capture (à assumer dans le récit).

## Taille maximale d'une lune

Deux contraintes :

1. **Sphère de Hill** : la lune doit orbiter à l'intérieur (~≤ 0,5 r_Hill prograde). Voir `mecanique-orbitale.md`. Une lune « énorme et lointaine » sort vite de la zone liée.
2. **Rapport de masse** : si la lune approche la masse de la planète, on ne parle plus de « lune » mais d'un **système binaire** (deux corps orbitant un barycentre commun hors des deux corps, comme Pluton–Charon, rapport ~1:8). Une « lune » de masse comparable à sa planète est en fait une planète double — à décrire comme telle.

Une grande lune bien visible dans le ciel (type « grosse lune » de fiction) est **possible** si elle reste dans la sphère de Hill et n'est pas trop proche de la limite de Roche.

## Verrouillage des lunes

La plupart des grandes lunes proches sont **verrouillées** par les marées et présentent toujours la même face à leur planète (Lune, lunes galiléennes). Normal et attendu. Une grande lune proche qui « tourne sur elle-même » vite par rapport à sa planète est peu crédible sur le long terme.

## Chauffage de marée

Une lune sur orbite **excentrique** (souvent entretenue par une **résonance** avec d'autres lunes) est malaxée par les marées → **chaleur interne**. Effets observés :
- **Io** (Jupiter) : le corps le plus volcanique du Système solaire, chauffé par la résonance de Laplace.
- **Europe, Encelade** : océans liquides **sous la glace**, entretenus par le chauffage de marée → habitabilité potentielle hors zone habitable stellaire (voir `habitabilite.md`).

Donc une lune peut abriter de l'eau liquide loin de l'étoile **si** le chauffage de marée est présent (orbite excentrique + résonance) — un ressort de crédibilité utile en fiction.

## Limite de Roche & anneaux

**Limite de Roche** : distance en deçà de laquelle les forces de marée de la planète l'emportent sur l'auto-gravité d'un corps → il est **déchiré** (ou ne peut pas s'accréter). Formule (corps fluide/peu cohésif) :

`d_Roche ≈ 2,44 × R_planète × (ρ_planète / ρ_lune)^(1/3)`

(pour un corps rigide, coefficient un peu plus faible, ~1,26–1,44 ; retenir ~2,44 comme borne de référence pour un satellite non cohésif).

Conséquences :
- **Les anneaux se situent à l'intérieur** de la limite de Roche (débris qui ne peuvent pas s'agglomérer). **Les lunes se situent à l'extérieur.**
- Un corps solide (lune, station) décrit en orbite **à l'intérieur** de la limite de Roche est **incohérent** : il devrait se disloquer. À l'inverse, un système d'**anneaux** est crédible s'il se trouve dans cette zone.
- Une lune qui migre sous la limite de Roche est vouée à se briser en anneau (destin probable de Phobos, et de Triton à très long terme).

## Longévité des anneaux

Les anneaux ne sont pas éternels : ils s'étalent, tombent sur la planète ou se dispersent en quelques dizaines à centaines de Ma sauf entretien. Les **lunes bergères** confinent et stabilisent des anneaux étroits (ex. anneaux de Saturne/Uranus). Un système d'anneaux spectaculaire et **permanent** sur des milliards d'années sans lunes bergères ni source d'alimentation est à nuancer (souvent : anneaux jeunes ou transitoires).

## Sous-lunes et lunes binaires

- **Sous-lune** (lune d'une lune) : théoriquement possible dans une fenêtre étroite (la lune-hôte doit être assez grande et assez loin de la planète pour offrir une sphère de Hill exploitable), mais **rare et fragile**. À manier avec précaution ; un indice de cohérence élevé exige de justifier la stabilité.
- **Lune binaire / planète double** : deux corps de masses comparables orbitant un barycentre commun (Pluton–Charon). Cohérent et observé ; à décrire comme un système double, pas comme « planète + lune ».

## Lunes capturées

Orbites inclinées/rétrogrades/excentriques. Souvent petites, parfois en voie de spiraler vers la planète (Triton) → durée de vie orbitale finie. Crédibles si l'histoire de capture est assumée et si l'échelle de temps reste cohérente.
