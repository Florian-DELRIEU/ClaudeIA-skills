# Format des sauvegardes Time Planner

Base **SQLite 3**, `user_version = 13`, **21 tables**. Schéma stable et identique
sur toutes les sauvegardes observées (déc. 2024 → juil. 2026). Fichiers ~55-70 Mo
(la taille vient surtout des BLOB de pièces jointes / icônes).

## Le pivot : la table `entry`

```sql
CREATE TABLE entry (_id INTEGER PRIMARY KEY, pid INTEGER
                    FOREIGN KEY(pid) REFERENCES category(_id) ON DELETE CASCADE)
```

`entry` est une **table d'identité partagée**. Chaque objet planifiable —
`task`, `note`, `scheduled_activity`, `logged_activity`, `activity_reminder`,
`category_reminder`, `simple_reminder`, `timer` — possède un `_id` qui **référence
`entry._id`** (`FOREIGN KEY(_id) REFERENCES entry(_id) ON DELETE CASCADE`).

Conséquences :
- **Créer** un objet = insérer d'abord une ligne `entry(pid=...)`, récupérer son
  `lastrowid`, puis insérer l'objet avec ce même `_id`.
- **Supprimer** = `DELETE FROM entry WHERE _id=?` → le CASCADE nettoie l'objet et
  toutes ses dépendances (accomplishments, pins, rappels, exclusions).
- `category` n'est **pas** une `entry` : c'est le conteneur racine. Supprimer une
  catégorie (`DELETE FROM category`) cascade sur tout son contenu via `pid`.

## Tables principales

| Table | Rôle | Champs notables |
|---|---|---|
| `category` | Conteneur racine | `pos`, `color`, `icon_res`, `archive_date_time`, `note` |
| `entry` | Identité partagée | `_id`, `pid` |
| `task` | Tâches | `priority`, `completed`, `pos`, `note` |
| `task_accomplishment` | Dates de complétion (récurrentes) | `tid`, `date` (minuit ms) |
| `task_pin` | Épingle tâche↔activité | `aid` (activité), `tid` (tâche) |
| `scheduled_activity` | Activités planifiées | récurrence, horaires, `measure`, `type` |
| `logged_activity` | Activités réalisées | `date_time`, `value`, `measure`, `uid` |
| `note` | Notes | `content`, `pos` |
| `tag` | Étiquettes `#xxx` | `name`, `pos` |
| `unit` | Unités de mesure | `name`, `measure` |
| `attachment` | Pièces jointes (BLOB) | `data`, `type` |
| `*_reminder` | Rappels | `type`, `params`, `strength`, `sound` |
| `recurrence_exclusion` | Occurrences supprimées | `eid`, `date` |
| `preference` | Réglages appli (clé/valeur) | `pref_key`, `pref_type`, `pref_value` |
| `filter`, `filter_schedule` | Filtres sauvegardés | `query`, `filter` |
| `running_bubble`, `timer` | Chronos en cours | souvent vides |

## Conventions de codage

- **Dates** : timestamp Unix en **millisecondes**. Ex. `1675257170427` = 01/02/2023.
  `0` = non défini. Les `task_accomplishment.date` sont calés à **minuit** du jour.
- **Couleurs** : entier **ARGB signé** (style `android.graphics.Color`).
  Ex. `-16760577` → `#0040FF`. Conversion dans la lib : `argb_to_hex` / `hex_to_argb`.
- **`category.archive_date_time`** : `0` = catégorie **active** ; sinon = date
  d'archivage (ms). L'archivage ne supprime rien.
- **`note` / `category.note`** : format `<![CDATA[...formatage...]]>texte réel`.
  Le bloc CDATA porte des métadonnées de rich-text ; le texte utile suit `]]>`.
  Lib : `note_text` (extraire) / `note_wrap` (envelopper à l'écriture).
- **`task.priority`** : `0` aucune, `1` basse, `2` moyenne, `3` haute
  *(confirmé par Florian directement dans l'app — sélecteur de priorité à 4 niveaux).*
- **`task.completed`** : `0` / `1`.
- **`*.pos`** : ordre d'affichage (entier croissant, propre à chaque `pid`).
  **Invariant important pour `task`** : dans une catégorie donnée, l'app range
  les tâches en **deux blocs contigus** de `pos` — actives d'abord (pos bas),
  terminées ensuite (pos haut). Ce n'est pas juste un tri par `completed` à
  l'affichage : le `pos` lui-même encode l'appartenance au bloc. Une tâche
  active insérée avec un `pos` situé dans/après le bloc terminé s'affiche à
  tort dans la section « Terminé » même si `completed=0`. Toute insertion ou
  changement de statut doit donc **repositionner `pos`** pour rester dans le
  bon bloc (voir `add_task` / `complete_task` dans `tp_lib.py`, qui décalent
  les `pos` voisins pour préserver l'invariant).
- **`scheduled_activity.type`** : `0` = simple/ponctuel, `1` = cyclique (roulement
  type planning de travail, avec `every_num` = période).
- **`*.measure`** (scheduled/logged) : `0`/`1` = **durée** (`value` en **ms**),
  `2` = **comptage** (`value` = entier), `10` = mesure monétaire/quantitative liée
  à une `unit`.
- **`days_of_week`** : bitmask 7 bits (bit0=Lun … bit6=Dim). `127` = tous les jours.
- **`start_time_or_part_of_day`** : minutes depuis minuit (`840` = 14h00) ou code
  « moment de journée » selon le contexte de l'activité.

## Round-trip / réimport

- Ne **jamais** modifier `user_version` (=13) ni l'ordre/nom des tables : l'appli
  charge par schéma attendu.
- Après toute écriture : `PRAGMA integrity_check` doit renvoyer `ok` et
  `PRAGMA foreign_key_check` doit être vide.
- Le fichier réimportable garde l'extension d'origine (`.sqlite` ou `.db`). Time
  Planner restaure via son écran *Backup / Restore*.
- Toujours produire un **nouveau fichier** dans `/mnt/user-data/outputs/` — ne
  jamais écraser l'upload.
