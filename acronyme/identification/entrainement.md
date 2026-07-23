# Protocole d'entraînement à l'identification

Florian utilise régulièrement ce mode pour exercer (et affiner) l'identification
d'acronymes sur des cas réels, sans repartir d'un fichier ORBAT complet.

## Déclencheur

Florian donne, sans autre consigne, un ou plusieurs **noms d'unités, de véhicules ou de
personnels**. C'est en soi le signal d'un exercice d'identification — pas une simple
question factuelle. Traiter chaque nom donné comme une demande d'acronyme, même si la
phrase ne le formule pas explicitement (cf. l'usage établi dans cette conversation).

## Déroulement, par nom fourni

1. **Rechercher** les caractéristiques du matériel/personnel si nécessaire (web search) :
   châssis, gabarit, armement principal, protection, équipage, doctrine d'emploi.
2. **Dérouler la méthode** (`METHODE.md`) : châssis → Type, rôle/armement primaire →
   suffixe(s), notation numérique si pertinente, arbitrage P1-P5 si plusieurs codes sont
   défendables. Consulter `chassis-types.md` / `personnel.md` / `lexique.json` en premier
   pour la cohérence.
3. **Détailler le raisonnement** étape par étape, pas seulement le résultat — Florian
   note la démarche autant que la conclusion. Signaler explicitement les doutes, cas
   liminaux, ou choix entre plusieurs codes possibles (ex. TAT vs SPAT vs TD).
4. **Donner l'acronyme final** proposé.
5. Florian attribue une **note sur 5** (voir barème) et explique la correction si besoin.
6. **Journaliser** dans `lexique.json` dès qu'un acronyme est validé (note 4 ou 5, avec
   correction éventuelle appliquée) : désignation réelle, code retenu, décomposition,
   note de contexte si le cas est instructif (ambiguïté résolue, exception...).

## Barème (fourni par Florian)

| Note | Signification |
|------|----------------|
| 1 | Rien ne va dans l'acronyme |
| 2 | Grosse erreur, mais certains éléments sont vrais/justes |
| 3 | Petite erreur — un seul point de l'acronyme ne correspond pas |
| 4 | Factuellement juste, mais perfectible (trop détaillé, pas assez, ou un meilleur acronyme existe) |
| 5 | Tout bon, rien à changer |

## Pourquoi journaliser

L'entraînement n'est pas qu'un exercice ponctuel : chaque cas validé enrichit
durablement `lexique.json`, exactement comme les entrées amorcées depuis `ORBAT_2023`.
Les cas ambigus (ex. ELC bis → `TD`, la distinction TAT/SPAT/SPC) sont les plus utiles à
conserver, car ce sont ceux qui affinent le plus l'identification future.
