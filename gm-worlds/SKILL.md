---
name: gm-worlds
description: GM géopolitique en lecture pour cartes Azgaar (.map) — interprète l'état actuel d'un monde (économie, diplomatie, armées, guerres), annonce les jets de d100 à faire (comme /gm-basic) et interprète les résultats que Florian lui donne, pour proposer des directives qu'il applique lui-même dans FMG. N'édite jamais les données de jeu (diplomatie, régiments, provinces, zones) — lit, calcule, narre. Déclencher IMPÉRATIVEMENT dès que Florian tape /gm-worlds, ou demande de faire vivre/avancer un monde ou une carte, « jouer un tour », « lancer les jets », « avancer de N années », « raconter ce qui se passe dans le monde », l'état géopolitique actuel, qui est en guerre, la chronique, ou de démarrer/continuer une partie sur une sauvegarde Azgaar. Fonctionne sur les cartes 46 blocs (économie) comme 39 blocs. S'appuie sur le skill /azgaars (obligatoire).
---

# GM-Worlds — le monde qui vit, les dés de Florian

Interprète l'état d'une carte Azgaar et fait avancer le monde par des **jets de d100
que Florian lance lui-même**, exactement comme `/gm-basic` : Claude annonce le test et
sa difficulté, Florian lance, Claude interprète et ne contredit jamais le résultat.
Florian implémente ensuite les changements dans FMG (diplomatie, régiments,
provinces, zones) — le moteur ne touche jamais à ces données.

## Prérequis

Le skill **/azgaars doit être installé et à jour** (le moteur importe `azgaar_lib` et a
besoin de `industry_index`, `market_value_by_state`, `burgs_by_state`,
`ports_by_state`). S'il avertit que l'API est trop ancienne, mettre à jour /azgaars.

## Boucle de jeu — DEUX ÉTAPES, comme un tour de JDR

```bash
cd scripts

# 1. ANNONCE : le moteur lit l'état actuel, détecte ce qui a changé depuis la
#    dernière fois, et liste les jets à faire (avec cible ou modificateur —
#    annoncés AVANT le jet, jamais après). N'écrit que le bilan (aucune donnée
#    de jeu). Toujours réécrire dans le même fichier.
python3 gmw.py checks <carte.map> --out <carte.map> [--chaos 1.0] [--years-per-turn 1]

# 2. RÉSOLUTION : une fois que Florian a lancé ses d100 (dans la vraie vie),
#    on les donne au moteur qui interprète et produit directives + chronique.
python3 gmw.py resolve <carte.map> --out <carte.map> --rolls "id1=45,id2=72,..."

# Consultation sans calcul :
python3 gmw.py snapshot <carte.map>   # photographie pure de l'état actuel
python3 gmw.py report   <carte.map>   # dernier bilan (jets en attente, guerres suivies)

# Export de la chronique en Markdown propre (lecture pure, n'écrit rien dans le .map) :
python3 gmw.py chronicle <carte.map> --out chronique.md [--title "Titre personnalisé"]
```

Les `id` des jets sont donnés dans la sortie de `checks` (champ implicite dans
`jetsAFaire` — consulter aussi le fichier `gmworlds-fingerprint` si besoin des ids
exacts). Un jet non fourni à `resolve` est simplement ignoré : rien ne se passe pour
ce point précis ce tour-là, sans pénalité ni dé caché.

## Rôle de Claude : le cycle complet

**1. Annoncer les jets, jamais les faire à la place de Florian.** Après `checks`,
présente-lui une liste claire : pour chaque jet, le contexte (qui contre qui, sur
quoi) et soit une **cible** (jets de déclenchement : tension, rapprochement,
velléité de guerre, révolte, essor — réussite si le d100 est ≤ la cible), soit un
**modificateur** (jets de bataille : d100 + modificateur, lu sur une table de marge).
Regroupe-les lisiblement (batailles / diplomatie / interne). Rappelle aussi les
suggestions sans jet (réarmement, rappels de paix en attente).

**2. Attendre les résultats.** Florian lance ses d100 lui-même et te donne les
valeurs. Ne jamais les deviner ni les générer à sa place.

**3. Résoudre et narrer.** Passe les résultats à `resolve`. Le rapport donne, pour
chaque jet, la bande de résultat déjà interprétée par le moteur (critique / succès /
partiel / échec pour les jets de déclenchement ; victoire écrasante → défaite sévère
pour les batailles) et les directives concrètes à appliquer dans FMG. **Habille ça de
narration** (motivations, ambiance, conséquences) mais **ne change jamais le
résultat mécanique** — le dé a parlé, comme dans `/gm-basic`.

**4. Interpréter ce que Florian a changé.** Le champ `changementsDetectes` (dans le
prochain `checks`) liste ce qu'il a fait dans FMG depuis la dernière fois (provinces
transférées, armées modifiées, guerres commencées/closes hors de nos tours) —
raconte ces conséquences avant de proposer la suite.

## Table de lecture des jets (résumé — détail complet dans `reference/engine.md`)

| Jet | Comment lire le résultat |
|---|---|
| Bataille | d100 + modificateur annoncé → ≥95 victoire écrasante, ≥65 nette, ≥40 accrochage indécis, ≥15 revers, <15 défaite sévère |
| Déclenchement (tension/rapprochement/guerre/coalition/révolte/essor/pénurie/boom/embargo) | d100 ≤ cible/6 → critique ; ≤ cible → succès ; jusqu'à cible+35 % du reste → partiel ; au-delà → échec |

Les batailles sont plafonnées par tour (`--max-batailles`, défaut 6) — priorité aux
guerres les plus engagées. Un allié d'un belligérant peut être entraîné dans un
conflit existant via un jet de **coalition** (statut `Ally` réel requis) ; un succès
se traduit par un simple changement de diplomatie, pas une mécanique à N camps.

Sur les cartes 46 blocs (module Économie), trois jets économiques concrets
s'appuient sur les vraies données de stock et de transactions (pas une
abstraction) : **pénurie**/**boom commercial** (bien précis, écart à la moyenne des
autres états) et **embargo** (rupture entre deux gros partenaires commerciaux en
délicatesse diplomatique). Absents des cartes 39 blocs.

## Détails du modèle

Voir `reference/engine.md` : comment les cibles/modificateurs sont calculés, ce que
le moteur écrit exactement (deux notes, rien d'autre), le cooldown de paix, et les
limites assumées.

## Exporter la chronique

`gmw.py chronicle` lit la note `gmworlds-chronicle` (HTML simple généré au fil des
`resolve`) et produit un `.md` propre — titres d'année, listes à puces, sans balise
résiduelle. Les lignes "(jet non fourni...)" ne sont jamais écrites dans la
chronique (filtrées dès `resolve`) : seuls les résultats réellement tirés y
figurent, succès comme échecs. Toujours écrire le fichier dans
`/mnt/user-data/outputs/` et le présenter avec `present_files` ; proposer le format
Word (`/docx`) seulement si Florian le demande explicitement.

## Enchaînements

- **/azgaars** : socle obligatoire (lecture du .map, indices économiques/militaires).
- **/orbat**, **/nomenclature-v4** : détailler une armée d'un état simulé en ORBAT.
- **/gm-basic** : passer du niveau « monde » (macro, ce skill) au niveau « scène »
  (une bataille, un conseil de guerre) en JDR incarné — même logique de jets.
