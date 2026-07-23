# Commandes spéciales — Définitions

Les commandes sont des outils **hors-fiction** (meta).
Elles interrompent temporairement la narration pour fournir une information structurée,
puis le jeu reprend normalement.

La réponse à une commande s'affiche toujours **entre crochets** pour signaler
qu'on est hors-monde, puis Claude attend la prochaine action du joueur.

---

## `/pnj(nom)`

**Effet** : Affiche la fiche d'un personnage non-joueur, du point de vue
de ce que le personnage joueur connaît à ce stade de la campagne.

### Règles de contenu

- N'afficher **que ce que le joueur a appris** en jeu (observations, dialogues,
  réputation établie, révélations passées)
- Les secrets du MJ **ne figurent pas** dans la fiche, même si Claude les connaît
- Si une information est **rumeur ou incertaine**, la marquer explicitement `(supposé)`
- Le statut actuel reflète l'**état le plus récent** connu du joueur

### Format de sortie

```
[/pnj — hors-fiction]

── NOM COMPLET (surnom éventuel) ────────────────────
  Titre         : [titre officiel ou fonction désignée]
  Rôle          : [ce qu'il fait concrètement dans le monde / l'équipe]
  Allégeance    : [envers qui, loyauté apparente]
  Personnalité  : [2–3 traits clés · ton de voix en jeu]
  Statut actuel : [où il en est dans la campagne, état de la relation avec le joueur]
  Liens         : [connexions notables avec d'autres PNJ connus]
─────────────────────────────────────────────────────
```

### Si le PNJ n'est pas connu

```
[/pnj — hors-fiction]
Personnage inconnu : "nom"
Ce personnage n'a pas été défini ou rencontré dans la campagne.
```

### Exemples d'appel

- `/pnj(Mira)` → fiche de Mira
- `/pnj(l'Explorator)` → accepté si un seul Explorator existe dans la campagne
- `/pnj(Inconnu)` → message d'erreur standard

---

*D'autres commandes seront ajoutées ici au fil des sessions.*

---

## `/narrateur(Nom, Difficulté)` · `/narrateur(Nom, Difficulté, x=X)`

**Effet** : Déclare ou change le narrateur actif, son niveau de difficulté (1–5),
et optionnellement la fenêtre temporelle X (X pair obligatoire).
Prend effet immédiatement, même en pleine partie.

### Paramètres

| Paramètre | Valeurs | Défaut |
|-----------|---------|--------|
| `Nom` | Chroniqueur · Aléa · Impitoyable · Barde · Juge | — |
| `Difficulté` | 1 à 5 | — |
| `x` | Entier pair ≥ 4 | 8 |

### Comportement

- Si un narrateur était déjà actif, les événements en cours dans la fenêtre active
  sont conservés. Les prochains tirages appliquent immédiatement le nouvel archétype.
- X pair obligatoire. Si X impair est fourni, rejeter et signaler l'erreur hors-fiction.
- La difficulté passive du monde change immédiatement. La difficulté des événements
  s'applique au prochain tirage.

### Format de sortie

```
[/narrateur — hors-fiction]
Narrateur    : Chroniqueur
Difficulté   : 3 — Hostile
Fenêtre      : X=8 jours · Pas=4 jours
Statut       : actif · prochain tirage dans [N] jours de jeu
```

### Exemples d'appel

- `/narrateur(Chroniqueur, 3)` → Chroniqueur, difficulté 3, X=8 par défaut
- `/narrateur(Aléa, 5, x=6)` → L'Aléa, difficulté 5, fenêtre de 6 jours
- `/narrateur(Impitoyable, 4, x=4)` → phase intense, pression maximale

---

## `/horizon(...)` · `/horizon`

**Effet** : Contrôle la fenêtre temporelle de l'Horizon Glissant sans changer le narrateur.

### Variantes

| Appel | Effet |
|-------|-------|
| `/horizon(x=X)` | Change X (pair obligatoire). Prend effet au prochain tirage |
| `/horizon(pause)` | Suspend les tirages. Le monde ne génère plus rien |
| `/horizon(reprise)` | Reprend avec le dernier X actif |
| `/horizon(retrospectif)` | Tirage unique de rattrapage couvrant la période suspendue |
| `/horizon` | Affiche l'état actuel de la fenêtre |

### Format de sortie — `/horizon`

```
[/horizon — hors-fiction]
État         : actif / suspendu
Fenêtre      : X=8 jours · Pas=4 jours
Fenêtre active : J[N] → J[N+7]
Prochain tirage : J[N+4]

Événements programmés :
  · J[N+2] — [catégorie] — [description laconique] — statut : à venir
  · J[N+5] — [catégorie] — [description laconique] — statut : en cours
  · J[N+7] — [catégorie] — [description laconique] — statut : à venir
```

### Notes

- Les descriptions sont **laconiques** (5–8 mots). Pas de révélation des détails.
- Les événements résolus n'apparaissent pas dans `/horizon`, sauf si le joueur
  les a déjà rencontrés en jeu.
- `/horizon(retrospectif)` génère un tirage unique couvrant toute la période suspendue,
  avec un nombre d'événements proportionnel à la durée (1 événement par X/2 jours environ).

---

## `/passif`

**Effet** : Affiche les paramètres actuels de la difficulté passive du monde.

### Format de sortie

```
[/passif — hors-fiction]
Niveau passif  : [N] — [Nom du niveau]
PNJ            : [disposition par défaut]
Économie       : [état du marché]
Conséquences   : [poids des erreurs]
Menaces fond   : [niveau de pression ambiante]
Autorités      : [posture envers le joueur]
```

### Notes

- Afficher le niveau passif **tel qu'il est réellement**, y compris si le joueur
  ne l'avait pas demandé explicitement en début de campagne.
- Ne pas arrondir ni adoucir : si le monde est à niveau 5, le dire clairement.
- Cette commande ne révèle pas le narrateur actif ni les événements programmés.
