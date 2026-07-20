# Personnel → code (éléments, pas individus)

Dans les ORBAT de Florian, le catalogue `personnel` code un **élément** (escouade,
binôme, équipe), pas un soldat isolé. L'identification suit donc :

**`{Échelon d'élément}-{Rôle dominant}`**

## Échelons d'élément

| Préfixe | Élément | Effectif indicatif |
|---------|---------|--------------------|
| `ESC` | Escouade / groupe | ~6-12 |
| `EQU` | Équipe | ~2-5 |
| `BI` | Binôme | 2 |

## Rôle dominant (exemples établis dans `ORBAT 2023`)

| Code | Élément |
|------|---------|
| `ESC-INF` | Escouade d'infanterie classique |
| `ESC-HW` | Équipe d'armes lourdes (AT et autres) |
| `ESC-ENG` | Escouade du génie |
| `ESC-MS` | Escouade démineur |
| `ESC-AT` | Escouade antichar |
| `ESC-HQ` | Élément de commandement |
| `BI-TE` | Binôme tireur d'élite |
| `EQU-REC` | Équipe de reconnaissance |
| `EQU-UAV.R` | Équipe drone de reconnaissance |

## Méthode pour une nouvelle armée

1. Déterminer la **taille de l'élément** (escouade / équipe / binôme) → préfixe.
2. Déterminer le **rôle dominant** (INF, ENG, MS, AT, HW, TE, REC, UAV, HQ, MED…) →
   suffixe, en réutilisant les rôles de `references/infanterie.md`.
3. Réutiliser un code existant si l'élément est équivalent (P5 — cohérence lexique).

> Les grades/armes individuels (`references/infanterie.md`) ne servent ici qu'à *qualifier*
> le rôle dominant de l'élément, pas à créer un code par soldat.
