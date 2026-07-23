---
name: todo
description: >
  Gestionnaire de todo-list personnel de Florian, stocké dans le fichier
  TASKS.md fourni avec ce skill. Déclencher IMPÉRATIVEMENT dès que Florian
  tape /todo, ou demande d'ajouter / cocher / terminer / supprimer / déplacer
  / réorganiser une tâche, de voir « ce qu'il a à faire », « sa liste »,
  « ses todos », « ce qui est en cours », « ce qu'il attend », ou de faire le
  point sur ses tâches. Déclencher aussi pour des formulations courtes
  ("ajoute à ma todo", "rappelle-moi de…", "c'est fait pour X", "qu'est-ce
  qu'il me reste ?", "montre ma liste"). Couvre la lecture, l'écriture et la
  mise à jour de la liste, et rappelle la procédure pour la conserver entre
  sessions.
---

# Todo — liste de tâches de Florian

Gérer la todo-list de Florian, stockée dans **`TASKS.md`**, livré avec ce skill.
Quatre opérations : **lire**, **ajouter**, **terminer**, **réorganiser**.

## Où vit la liste

Le fichier canonique est `TASKS.md`, **à la racine de ce skill**. Toujours le lire
en premier avant toute opération, puis l'éditer en place. Ne jamais recréer une
liste à partir de zéro si le fichier existe : on conserve l'historique de Florian.

## Format

Sections fixes, dans cet ordre :

```markdown
# Tasks

## Active

## Waiting On

## Someday

## Done
```

Format d'une tâche :
- `- [ ] **Titre de la tâche** - contexte, pour qui, échéance`
- Sous-puces pour les détails additionnels
- Terminée : `- [x] ~~Titre~~ (date)`
- Tag projet entre parenthèses à la fin quand c'est pertinent (ex : `(ORBAT)`)

## Opérations

**`/todo` seul, ou « montre ma liste » / « qu'est-ce qu'il me reste ? »**
→ Lire `TASKS.md`, résumer **Active** et **Waiting On**, signaler ce qui est en
retard ou urgent. Ne pas noyer : aller à l'essentiel.

**« ajoute… » / « rappelle-moi de… »**
→ Ajouter dans **Active** au format `- [ ] **Tâche**`. Inclure le contexte fourni
(projet, pour qui, échéance). Ne pas inventer d'échéance.

**« c'est fait pour X » / « j'ai fini X »**
→ Trouver la tâche, passer `[ ]` en `[x]`, ajouter le barré `~~…~~` et la date du
jour, puis la déplacer dans **Done**.

**« je suis en attente de… » / « ça bloque sur… »**
→ Déplacer ou créer dans **Waiting On**, avec un `depuis [date]`.

**« plus tard » / « un jour »**
→ Ranger dans **Someday**.

Toujours confirmer brièvement ce qui a changé, puis présenter le `TASKS.md` mis à
jour avec `present_files` si l'outil est disponible.

## Conventions

- **Gras** sur le titre pour le scan visuel.
- `pour [personne]` quand c'est un engagement envers quelqu'un.
- `échéance [date]` pour les deadlines, `depuis [date]` pour l'attente.
- Tag projet entre parenthèses (`(ORBAT)`, `(WH40K)`, `(Cosmotter)`, `(TVA)`…).
- Garder **Done** environ une semaine, puis purger les vieux éléments.

## Persistance entre sessions (important)

L'espace de travail est temporaire : les modifications de `TASKS.md` **ne survivent
pas seules** d'une session à l'autre — même logique que les autres skills de Florian.
Pour conserver la liste à jour :

1. À la fin d'une session où la liste a changé, **re-packager ce skill** avec le
   `TASKS.md` modifié (zip / `.skill`), puis le **re-uploader**.
2. Quand Florian tape **`/maj-todo`**, repackager le skill avec le `TASKS.md` courant
   et lui fournir le `.skill` à ré-installer.

À défaut, lui rappeler en fin de session de récupérer le `TASKS.md` mis à jour s'il
veut le garder.
