---
name: audit-maj
description: >
  Audite la fraîcheur de tous les skills perso de Florian (dossier /mnt/skills/user/)
  en comparant la date de dernière modification du fichier SKILL.md installé à la
  dernière discussion pertinente retrouvée dans l'historique des conversations.
  Déclencher IMPÉRATIVEMENT dès que Florian tape /audit-maj. Signale deux types
  d'anomalies : un skill installé dont le contenu ne reflète pas une décision de
  conception plus récente (ex. un /maj resté en attente), et un skill construit/discuté
  en session mais jamais réuploadé (absent du dossier installé alors que discuté).
---

# /audit-maj — Audit de fraîcheur des skills perso

## Objectif

Vérifier que chaque skill installé dans `/mnt/skills/user/` reflète bien la dernière
décision prise à son sujet dans nos conversations. Deux problèmes à détecter :

1. **Skill périmé** : installé, mais une conversation plus récente contient des
   changements de conception (règles, structure, contenu) qui ne semblent pas
   reflétés dans le fichier actuel.
2. **Skill fantôme** : construit ou modifié dans une session (visible via
   `create_file`/`str_replace` sous `/mnt/skills/user/<nom>/`, ou packagé en
   `.skill`) mais absent du dossier réellement installé — signe qu'il n'a jamais
   été réuploadé via Paramètres > Capabilities > Skills, ou qu'il a été retiré.

## Contexte technique (rappel)

Skills 2.0 n'a plus de bouton de sauvegarde en session : toute édition de fichier
sous `/mnt/skills/user/` reste éphémère tant que Florian ne fait pas `/maj` → zip →
réupload manuel. La date de dernière modification (`stat`) du fichier SKILL.md
installé reflète donc le moment du DERNIER réupload effectif, pas forcément celui
de la toute dernière conversation sur le sujet. Un écart de quelques heures à ~1 jour
entre une conversation et le mtime est normal (le réupload suit la session de peu) —
ce n'est pas en soi une anomalie.

## Procédure

1. **Lister les skills installés et leurs dates**, en une seule commande :
   ```bash
   for d in /mnt/skills/user/*/; do
     name=$(basename "$d")
     mtime=$(stat -c '%y' "$d/SKILL.md" 2>/dev/null)
     echo "$name | $mtime"
   done
   ```

2. **Pour chaque skill, chercher la dernière conversation pertinente** avec
   `conversation_search`. Utiliser des mots-clés techniques du domaine (pas juste
   "skill <nom>") — voir la table de correspondance ci-dessous, à enrichir si un
   skill est difficile à retrouver. Noter la date `updated_at` **et l'attribut
   `url`** de la conversation la plus récente qui modifie réellement le skill
   (construction/édition — pas une simple utilisation en lecture). L'URL est
   indispensable pour l'étape 5 : sans elle, Florian ne peut pas retrouver la
   conversation où finir le travail.

3. **Comparer.**
   - Écart normal (quelques heures à ~1 jour, ou conversation qui se termine par
     un packaging/réupload effectif) → ✅ OK.
   - Une conversation clairement postérieure au mtime décrit des changements de
     contenu non retrouvés dans le fichier installé, ou mentionne explicitement
     un `/maj` non exécuté / laissé "en attente" → 🔴 **périmé**.
   - Skill mentionné/construit dans une conversation (parfois même directement
     sous `/mnt/skills/user/<nom>/` dans cette conversation) mais absent du
     dossier `/mnt/skills/user/` actuel → 🔴 **fantôme** (jamais persisté).
   - Aucune conversation retrouvée après 1-2 requêtes → ⚠️ **non vérifiable**
     (peut être une conversation dans un Project, hors du scope de recherche
     actuel — le signaler comme tel, ne pas conclure à un problème).

4. **En cas de doute sur le contenu réel vs la date affichée**, vérifier le
   contenu du fichier installé directement (`view` ou `bash grep/head`) plutôt
   que de se fier uniquement au mtime — le mtime peut être trompeur (repackaging
   sans changement de contenu, ou inversement contenu à jour avec une date qui
   semble ancienne, ex. un `str_replace` de correction appliqué tôt dans une
   session qui s'est ensuite prolongée).

5. **Présenter les résultats** en mettant les vraies anomalies (périmé / fantôme)
   en tête de réponse, **chacune accompagnée du lien direct** (`url` de
   `conversation_search`) vers la conversation où reprendre le travail — c'est
   le point d'action concret pour Florian, pas juste un constat. Puis un tableau
   compact pour le reste : skill | dernière discussion connue | statut. Pas de
   préambule ni de longue reformulation de la méthode — Florian connaît déjà le
   principe après le premier audit.

   Format pour chaque anomalie :
   > 🔴 **`/nom-du-skill`** — [raison courte]. Reprendre ici : [url]

## Table de correspondance skill → mots-clés de recherche utiles

(à enrichir à chaque audit si un skill est difficile à retrouver, ou si un
nouveau skill perso apparaît dans `/mnt/skills/user/`)

| Skill | Mots-clés qui fonctionnent |
|---|---|
| acronyme | nomenclature-v4, séparateurs, VBCI, TAT/SPAT |
| aero | aérodynamique, hélice, pas variable, facteur P |
| astronome | cohérence système, indice, sphère de Hill |
| azgaars | Fantasy Map Generator, .map, FMG |
| bsdata | BattleScribe, New Recruit, catalogue |
| dds | icône équipement, HOI4, badge palier (non retrouvé le 18/07 — peut-être en Project) |
| gm-basic | maître du jeu, narrateur, PNJ |
| gm-worlds | simulation géopolitique, chronique, .map |
| infos-medecine | ANSM, VIDAL, posologie (non retrouvé le 18/07) |
| journal | ZV Journal, Ground News, brèves (non retrouvé le 18/07) |
| meme | mème, gif, template |
| nomenclature-planets | classification planète, lettre/degré/sous-type |
| orbat | orbat-mapper.app, sidc, aggregate |
| orbat-historique | échelon historique, ordre de bataille |
| prompt-image | prompt Midjourney, vocabulaire style |
| sqf | Arma 3, 3DEN, FOB |
| timeplanner | Time Planner, sqlite, tp_lib |
| todo | TASKS.md (non retrouvé le 18/07) |
| warhammer40k-lore | factions-custom, Sons of Mars, [ZV]/[FAN] |

## Historique des audits

- **18/07/2026** — Premier audit. Anomalies trouvées :
  - `/acronyme` : `/maj` laissé en attente après la session du 17/07 (table de
    véhicules OPFOR, enrichissement du lexique). Reprendre ici :
    https://claude.ai/chat/062a8e3c-1dc1-4873-a8b6-d0e3499e2777
  - `wh40k-v7` (règles maison 7e édition, construit le 09/07) : absent du dossier
    installé, jamais réuploadé. Reprendre ici :
    https://claude.ai/chat/9d27e74a-4a6e-490b-8c7f-8409f4a11c33
  - `histo-geo-civ` (assistant histoire/géo/civique, construit le 17/07) : absent
    du dossier installé, jamais réuploadé. Reprendre ici :
    https://claude.ai/chat/c8bf2341-2aef-428f-bee1-7032ca333d7a
  - `dds`, `infos-medecine`, `journal` et `todo` non vérifiables depuis les
    conversations indexées ici (peut-être dans un Project).

## Notes

- Mettre à jour la table de correspondance et l'historique des audits à chaque
  exécution de ce skill — ça fait gagner du temps de recherche au prochain audit
  et ça garde une trace des anomalies déjà signalées (pour éviter de re-signaler
  un `/maj` que Florian a entre-temps réglé).
- L'audit complet consomme un nombre significatif d'appels d'outils (une ou
  plusieurs recherches par skill). Si la liste de skills perso s'allonge
  beaucoup, prévenir Florian que ça peut prendre un moment.
