---
name: timeplanner
description: Lecture, analyse et édition des sauvegardes de l'application Time Planner (Android) de Florian, au format SQLite (fichiers time_planner_backup_*.db / .sqlite). Déclencher IMPÉRATIVEMENT dès que Florian tape /timeplanner, fournit un fichier .db/.sqlite de Time Planner, mentionne « Time Planner », « mon planner », « mes tâches Time Planner », « ma sauvegarde de tâches », ou demande de lire/analyser/extraire/statistiques/modifier ses catégories, tâches, activités programmées ou loguées, notes, tags, rappels. Déclencher aussi pour des demandes courtes (« combien de tâches en cours ? », « liste mes catégories », « quelles tâches dans X ?», « ajoute une tâche à Y », « marque Z comme faite », « archive la catégorie W », « stats de complétion », « purge les catégories archivées »). Peut retrouver les sauvegardes dans Google Drive au besoin.
---

# Time Planner — sauvegardes SQLite

Outillage pour lire et éditer les bases Time Planner sans casser leur réimport
dans l'application. Détails complets du format dans `reference/format.md` — le lire
avant toute édition non triviale ou dès qu'un champ paraît ambigu.

## Règles absolues

1. **Toujours travailler sur une COPIE.** Les uploads sont en lecture seule de
   toute façon ; utiliser `TimePlanner.open_copy(src, dst)` qui copie puis ouvre la
   copie. Ne jamais ouvrir l'upload d'origine en écriture, ne jamais l'écraser.
2. **Fichiers volumineux (55-70 Mo) → jamais via le connecteur Drive en base64**
   (ça sature le contexte). Si la base est dans Google Drive, demander à Florian de
   la déposer en pièce jointe, ou la retrouver via le connecteur Drive puis lui
   demander l'upload. Le traitement se fait en local avec `scripts/tp_lib.py`.
3. **Le pivot est la table `entry`.** Tout objet (task, note, scheduled/logged
   activity, rappel) a un `_id` qui référence `entry._id`. **Créer** un objet impose
   de créer d'abord une `entry` (la lib le fait). **Supprimer** = supprimer l'`entry`
   → le `ON DELETE CASCADE` nettoie tout le reste. Ne jamais insérer une task/note
   sans entry correspondante, sous peine de base incohérente.
4. **Dates = timestamp Unix en millisecondes** ; **couleurs = entier ARGB signé** ;
   **notes = wrapper `<![CDATA[...]]>texte`**. Toujours passer par les helpers de la
   lib (`ms_to_str`, `argb_to_hex`/`hex_to_argb`, `note_text`/`note_wrap`) plutôt que
   de coder ces conversions à la main.
5. **Ne jamais modifier `user_version` (=13)** ni l'ordre/nom des tables : l'appli
   charge selon un schéma attendu.
6. Après toute édition : `save_and_check()` doit renvoyer `integrity_check='ok'` et
   `foreign_key_violations=[]`. Sinon, ne pas livrer le fichier et diagnostiquer.
7. Toujours produire le fichier édité dans **`/mnt/user-data/outputs/`** (nouveau
   nom, même extension que l'original), puis rappeler à Florian de le restaurer via
   l'écran *Backup / Restore* de Time Planner.

## Workflow standard

```bash
# 1. Inspection rapide (lecture seule, sûr sur l'upload directement)
python3 scripts/tp_info.py base.sqlite               # vue d'ensemble + intégrité
python3 scripts/tp_info.py base.sqlite --categories  # + catégories (couleur, archivée)
python3 scripts/tp_info.py base.sqlite --tasks 20    # + 20 tâches actives
python3 scripts/tp_info.py base.sqlite --cat "Nom"   # + tâches d'une catégorie
python3 scripts/tp_info.py base.sqlite --scheduled   # + activités programmées
python3 scripts/tp_info.py base.sqlite --check       # contrôle d'intégrité
```

## Analyse / extraction en Python

```python
import sys; sys.path.insert(0, "scripts")
from tp_lib import TimePlanner, ms_to_str

tp = TimePlanner("base.sqlite")           # lecture seule OK sur l'upload
print(tp.summary())                        # compteurs + plage temporelle
for c in tp.categories(include_archived=False):
    print(c["_id"], c["name"], c["color_hex"])
for t in tp.tasks(completed=False):        # tâches actives
    print(t["name"], t["priority_label"], t["note_text"])
# requête libre :
rows = tp.q("SELECT name, COUNT(*) n FROM task WHERE completed=1 GROUP BY pid")
tp.close()
```

Pour des stats plus poussées (temps par catégorie via `logged_activity.value`,
taux de complétion, historique d'une activité), interroger directement avec `tp.q(...)`
en s'appuyant sur les conventions de `reference/format.md` (notamment la sémantique
de `measure`/`value` et le bitmask `days_of_week`).

## Édition (toujours sur copie)

```python
import sys; sys.path.insert(0, "scripts")
from tp_lib import TimePlanner

tp = TimePlanner.open_copy("upload.sqlite", "/mnt/user-data/outputs/tp_modifie.sqlite")

cid = tp.category_by_name("Administratif")[0]["_id"]
tid = tp.add_task(cid, "Renouveler le passeport", priority=2, note="avant fin du mois")
tp.complete_task(tid)                       # coche + insère l'accomplishment daté
tp.rename_task(tid, "Passeport — envoyé")
tp.set_priority(tid, 3)

newcat = tp.add_category("Voyage 2026", color_hex="#FF6600", icon_res="icl_airplane")
tp.archive_category(some_id)                # archive sans rien supprimer
tp.delete_entry(tid)                        # supprime un objet (CASCADE propre)
tp.delete_category(cid)                     # supprime catégorie + tout son contenu

rep = tp.save_and_check()                   # commit + intégrité — DOIT être 'ok'
assert rep["integrity_check"] == "ok" and not rep["foreign_key_violations"]
tp.close()
```

Méthodes disponibles : `add_task`, `complete_task`, `rename_task`, `set_priority`,
`set_task_note`, `add_category`, `archive_category`, `delete_entry`, `delete_category`,
`q` (SQL libre), `commit`, `save_and_check`. Pour une opération non couverte, écrire
le SQL via `tp.con.execute(...)` en respectant la règle `entry` (créer l'entry avant
l'objet ; supprimer via l'entry), puis `save_and_check()`.

## Retrouver les sauvegardes dans Google Drive

Les fichiers s'appellent `time_planner_backup_AAAA-MM-JJ__HH_MM.db.sqlite` (les plus
anciennes en `.db`). Recherche Drive : `title contains 'time_planner_backup'`. Comme
elles pèsent 55-70 Mo, ne pas les télécharger via le connecteur — lister les versions,
puis demander à Florian de déposer celle qu'il veut traiter en pièce jointe.

## Livraison

Après édition, présenter le fichier de `/mnt/user-data/outputs/` avec `present_files`
et indiquer : version restaurable via *Backup / Restore* de Time Planner ; conseiller
de garder l'ancienne sauvegarde tant que le réimport n'est pas vérifié.
