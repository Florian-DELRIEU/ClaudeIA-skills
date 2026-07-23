---
name: nomenclature-planets
description: >
  Système de nomenclature planétaire modulaire de Florian (V3), inspiré du système spectral
  Morgan-Keenan. Classe les planètes selon 4 étages orthogonaux : lettre (nature physique),
  degré (exposition/vivabilité 1-4), chiffre romain (sous-type dominant, table par lettre),
  modificateurs à deux chiffres (particularités cumulables, registre global par plages).
  Déclencher dès que Florian tape /nomenclature-planets, ou demande de classifier, coder,
  décoder, vérifier ou générer un code planétaire dans ce système. Également déclencher pour
  des demandes courtes : "c'est quoi le code pour une planète comme X ?", "décode M1.III.05.14",
  "est-ce que ce code est cohérent ?", "classe-moi cette planète". S'articule avec le skill
  /astronome pour la vérification de plausibilité physique, et avec le lore personnel de
  /warhammer40k-lore pour les mondes du secteur Iondarr.
---

# Système de Nomenclature Planétaire — V3

## Principe général

Format complet : **`LETTRE` `degré` `.` `ROMAIN` `.` `XX` `.` `XX` …**

Quatre étages orthogonaux, chacun répond à une question distincte :

| Étage | Position | Question | Nature |
|---|---|---|---|
| **1** | `LETTRE` | *C'est quoi ?* | Nature physique — un seul axe, exclusif |
| **2** | `degré` (1–4) | *J'y survis comment ?* | Exposition chronique — échelle globale |
| **3** | `ROMAIN` | *Ça ressemble à quoi ?* | Sous-type dominant — table PAR lettre |
| **4** | `.XX.XX…` | *Quelles particularités ?* | Modificateurs cumulables — registre global par plages |

**Règle d'or** : un même modificateur à deux chiffres a **toujours le même sens**, quelle que soit la lettre. Seul le chiffre romain change de sens selon la lettre.

La table complète (lettres, tables par lettre, plages de modificateurs, exemples travaillés) est dans `references/systeme-v3.md` — **toujours l'ouvrir avant de coder, décoder ou vérifier une planète**, ne jamais répondre de mémoire sur les valeurs précises.

## Notations spéciales

- `( )` entoure un modificateur pour signifier qu'il est **épisodique/saisonnier** et non chronique (ex : `(32)` = tempêtes radioactives ponctuelles). N'impose pas de relever le degré.
- `d(p)` forme longue du degré : `d` = nominal, `p` = pic pendant un événement (ex : `M1(3)`).
- **Formes tronquées admises** : toute partie à droite peut être omise si l'information manque ou pour alléger (`M`, `M1`, `M.III`, `M1.III`…). Le degré se loge juste après la lettre ; s'il est omis, la lettre est suivie directement d'un point (`M.III` = degré inconnu).
- `[ACR]` en fin de code : **rôle impérial/administratif**, tag emprunté tel quel au catalogue de rôles de `/nomenclature-v4` (ex. `[AGR]`, `[HAB]`, `[MIL]`). Cumulable par `.` comme dans V4 (`[AGR.MIN]`). Voir §8 de la référence pour la distinction entre ce tag (administratif, potentiellement faux) et les modificateurs numériques (physique, toujours vrai).

## Référentiel d'habitabilité

Le degré d'exposition (§5 de la référence) est **toujours relatif à un humain non modifié**, jamais à une espèce native. Une atmosphère respirable pour une biosphère locale mais toxique pour un humain reste notée comme toxique — pas de double lecture par espèce.

## Modes d'utilisation

### 1. Coder — attribuer un code à une planète décrite

1. Identifier la **nature physique** dominante → lettre (§4 de la référence). Si aucune lettre existante ne convient, le signaler à Florian plutôt que de forcer une case (des lettres sont volontairement laissées libres pour extension : G, L, N, P, Q, R–Z).
2. Évaluer le **degré d'exposition chronique** (1–4) en conditions normales — pas le danger global : un monde à air respirable reste degré 1 même si sa biosphère est mortelle (ce risque va en modificateur).
3. Choisir le **sous-type romain** dans la table propre à la lettre choisie.
4. Lister les **modificateurs** pertinents par plage (atmosphère 00-09, biosphère 10-19, hostile chronique 20-29, ultra-hostile chronique 30-39, orbital 40-49, terraformation/mégastructure 50-52, historique 60-69, réservé 70-79, libre 80-99). Mettre entre parenthèses tout ce qui est ponctuel/saisonnier plutôt que permanent.
5. Si un rôle impérial/administratif est pertinent, ajouter le tag `[ACR]` en fin de code (catalogue `/nomenclature-v4`) — c'est une couche distincte des modificateurs physiques, elle peut diverger de la réalité du terrain.
6. Vérifier la cohérence degré ↔ modificateurs (section suivante) avant de rendre le code final.

### 2. Décoder — expliquer un code existant

Lire étage par étage dans l'ordre lettre → degré → romain → modificateurs, en ouvrant la table par lettre correspondante dans la référence pour le romain. Signaler si le code est tronqué et ce qui manque plutôt que de le compléter par supposition.

### 3. Vérifier la cohérence

Appliquer les règles de la référence (§5) :
- Un degré **1** ne peut porter en dur aucun modificateur des plages **30–39**, ni les plus mortels de 20–29 sans que ce soit contradictoire.
- Tout modificateur **30–39 chronique** impose un degré **4**.
- Certaines lettres ont un degré quasi fixe (`J`, `E` → presque toujours 4) : une exception doit se justifier.
- Un danger **entre parenthèses** est exempté de ces règles — c'est tout l'intérêt de la notation épisodique.

Si Florian demande une vérification physique plus poussée (plausibilité orbitale, densité, rétention atmosphérique réelle), transférer vers le skill `/astronome` plutôt que de improviser : les deux skills sont complémentaires, celui-ci gère la *nomenclature*, `/astronome` gère la *physique*.

### 4. Générer — proposer un code pour une planète encore floue

Partir des contraintes données par Florian, proposer un code plausible en expliquant chaque étage choisi, et signaler explicitement les points laissés en forme tronquée si l'information n'a pas été fournie plutôt que de l'inventer.

## Statut du système

**V3 est une première version volontairement ouverte.** Plusieurs lettres et créneaux romains sont vides par design (voir §4 et §6 de la référence) — ne pas les combler de soi-même, les signaler comme disponibles si Florian a besoin d'une nouvelle catégorie. Des décisions restent explicitement ouvertes (§10 de la référence : sort de la lettre I, adoption d'un degré 0, attribution des lettres suggérées G/P/Q, articulation 30-39 vs 60-69) — les rappeler si elles deviennent pertinentes plutôt que de trancher à la place de Florian.

Deux lettres à ne pas confondre : `X` (planète spéciale/hautement spécifique, cas unique sans table) et `S` (planète-mégastructure, l'objet entier est artificiel — distincte du modificateur `52` qui note qu'une planète naturelle *porte* une mégastructure).

## Articulation avec `/nomenclature-v4`

Le rôle impérial/administratif d'une planète (`[AGR]`, `[HAB]`, `[MIL]`…) n'appartient pas à ce skill : c'est le catalogue de rôles de `/nomenclature-v4` qui fait autorité, repris tel quel sans duplication. Ce skill (`/nomenclature-planets`) ne modifie et ne repackage **jamais** les fichiers de `/nomenclature-v4` — toute évolution de ce catalogue (nouveaux acronymes, clarification de sens à l'échelle planète) relève exclusivement de ce skill-là, sur son propre `/maj`.

## Mise à jour du skill

Ne jamais modifier les fichiers de ce skill ni le repackager sans que Florian tape explicitement `/maj`, conformément à ses instructions générales de gestion de skills.
