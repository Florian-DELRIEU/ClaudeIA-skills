# Système de Narrateur

## Principe

Le Narrateur est une couche systémique **invisible au joueur** qui génère des événements
sur une fenêtre temporelle glissante, indépendamment des actions du joueur.
Il représente la pression du monde — pas uniquement sa réaction.

Deux paramètres **indépendants** le définissent :
- Son **archétype** : gouverne la logique de génération des événements
- Son **niveau de difficulté 1–5** : govern l'intensité des événements ET la passivité du monde

Le Narrateur actif n'est jamais révélé spontanément au joueur.

---

## Archetypes

### Le Chroniqueur
Escalade progressive et logique. Les événements s'enchaînent causalement,
la pression monte graduellement. Ce qui est semé est récolté.

- **Adapté à** : campagnes longues, arcs narratifs structurés
- **Logique** : chaque événement découle de l'état précédent du monde
- **Événements par tirage** : 1–2 (la continuité causale prime sur le volume)
- **Signature** : les événements semblent inévitables rétrospectivement

---

### L'Aléa
Jet pur sans logique directrice. Peut être brutal ou généreux selon les dés.
Aucune garantie, aucune prévisibilité.

- **Adapté à** : campagnes sandbox, joueurs expérimentés, univers chaotiques
- **Logique** : chaque tirage est indépendant du précédent
- **Événements par tirage** : 1d3 (variable)
- **Signature** : alternances imprévisibles de chance et de catastrophe

---

### L'Impitoyable
Pression constante, peu de répit. Les opportunités sont rares ou coûteuses.
Le monde ne donne rien sans contrepartie.

- **Adapté à** : univers hostiles par nature (WH40K, Dark Sun, Forbidden Lands)
- **Logique** : priorité systématique aux menaces et complications
- **Événements par tirage** : 2–3
- **Signature** : les opportunités, quand elles arrivent, ont toujours un coût caché

---

### Le Barde
Priorité au drama sur la punition. Génère des moments forts — conflits,
révélations, dilemmes — pas nécessairement des menaces mortelles.

- **Adapté à** : campagnes narratives, nouveaux joueurs, univers politiques
- **Logique** : chaque événement crée un choix ou un contenu significatif
- **Événements par tirage** : 1–2 (toujours au moins 1 significatif)
- **Signature** : même les mauvaises nouvelles ouvrent des portes narratives

---

### Le Juge
Les actions du joueur amplifient les événements dans les deux sens.
Le bien revient en bien (rarement). Le mal revient fort.

- **Adapté à** : campagnes morales, monde à karma visible, Rogue Trader
- **Logique** : analyse les actions récentes du joueur avant de tirer
- **Événements par tirage** : 1–3 selon le poids des actions récentes
- **Signature** : le joueur finit toujours par comprendre pourquoi les choses arrivent

---

## Niveau de Difficulté (1–5)

La difficulté agit sur **deux couches indépendantes**.

### Couche 1 — Événements générés

Nature et intensité des événements produits à chaque tirage.

| Niveau | Nom | Répartition approximative |
|--------|-----|--------------------------|
| 1 | **Bienveillant** | 60% opportunités/neutres · 30% complications légères · 10% menaces |
| 2 | **Standard** | 30% opportunités · 40% neutres/complications · 30% menaces |
| 3 | **Hostile** | 10% opportunités · 40% complications · 50% menaces |
| 4 | **Implacable** | 5% opportunités (toujours avec un coût) · 25% complications · 70% menaces |
| 5 | **Mortel** | 0% opportunités pures · 20% complications · 80% menaces · les bonnes nouvelles sont des pièges |

### Couche 2 — Passivité du monde

Le fond permanent du monde, indépendant des événements générés.

| Niveau | Nom | Dispositions PNJ | Économie | Conséquences | Menaces de fond | Autorités |
|--------|-----|-----------------|----------|--------------|-----------------|-----------|
| 1 | **Sanctuaire** | Amical par défaut | Prix équitables, ressources disponibles | Légères, réversibles | Absentes | Protectrices, accessibles |
| 2 | **Stable** | Indifférent | Marché normal, quelques pénuries | Durables si négligence | Rares, ponctuelles | Présentes mais peu interventionnistes |
| 3 | **Tendu** | Méfiant | +25%, certains biens rares | Durables par défaut | Présentes et actives | Corrompues ou débordées |
| 4 | **Hostile** | Inamical | +50–75%, marché noir dominant | Sévères, cumulables | Permanentes, s'intensifient | Contre le joueur ou absentes |
| 5 | **Condamné** | Hostile jusqu'à preuve contraire | Survie pure, troc, pénurie sévère | Permanentes, irréversibles | Omniprésentes, mortelles | Inexistantes ou ennemies |

Les deux couches sont **indépendantes** :
- L'Aléa à D2 = monde stable, événements imprévisibles
- Le Chroniqueur à D5 = monde condamné qui empire logiquement
- L'Impitoyable à D1 = beaucoup d'événements, mais le monde reste accueillant

---

## Horizon Glissant

### Principe mathématique

```
Fenêtre = X jours (X pair obligatoire)
Pas     = X/2 jours

Tirage 1 : J1 ──────────── J(X)
Tirage 2 :         J(X/2+1) ──────────── J(3X/2)
Tirage 3 :                   J(X+1) ──────────── J(2X)
...

Propriété : à partir de J(X/2 + 1), chaque jour appartient
à exactement 2 fenêtres actives simultanément.
→ Densité d'événements plate — aucun pic, aucun creux.
```

### Valeurs recommandées de X

| X | Pas | Nom | Usage typique |
|---|-----|-----|---------------|
| 4 | 2j | Intense | Combat prolongé, traque, crise politique aiguë |
| 6 | 3j | Actif | Mission en cours, zone dangereuse |
| **8** | **4j** | **Normal** | **Rythme de campagne standard — défaut** |
| 12 | 6j | Étendu | Base opérationnelle, convalescence, hivernage |
| 16 | 8j | Long | Voyage interstellaire, arc de campagne étiré |

X peut varier librement au fil de la campagne selon le rythme narratif.

### États du système

| État | Description | Déclencheur typique |
|------|-------------|---------------------|
| **Actif** | Tirages normaux selon X courant | Fonctionnement standard |
| **Suspendu** | Aucun tirage | Voyage sans enjeu, avance rapide narrative pure |
| **Reprise** | Redémarre avec le dernier X actif | Fin de suspension courte |
| **Rétrospectif** | Tirage unique couvrant la période suspendue | Arrivée après suspension longue |

La **suspension pure** est une information narrative en soi : le monde s'est arrêté.
Le **rétrospectif** génère ≈ 1 événement par X/2 jours de suspension, condensés en un seul tirage.

---

## Procédure de tirage

À chaque pas de X/2 jours, le MJ effectue silencieusement les étapes suivantes :

### 1. Consulter l'historique actif
- Quels événements sont en cours ou non résolus ?
- Quels événements arrivent à expiration dans cette fenêtre ?

### 2. Appliquer le filtre univers
Sélectionner la table d'événements correspondant à l'univers actif :

| Univers | Table à utiliser |
|---------|-----------------|
| Rogue Trader / WH40K | `evenements/rogue-trader.md` |
| Tout autre univers | `evenements/generique.md` |
| Univers non couvert | `evenements/generique.md` comme base, adapter les seeds à la couleur locale |

Si une table spécialisée est disponible, elle remplace la générique pour le choix des seeds.
La générique reste disponible en complément pour des seeds sans couleur d'univers marquée.

### 3. Appliquer le filtre narratif
- Actions récentes du joueur → répercussions logiques
- État des factions actives (en conflit, trêve, expansion, déclin)
- Événements non résolus (peuvent muter ou s'aggraver)

### 4. Tirer les événements
Nombre selon l'archétype actif. Catégorie selon la répartition du niveau de difficulté.

### 5. Vérifier la cohérence avec le chevauchement
Les événements dans la zone commune (déjà programmés) doivent être respectés.
Les nouveaux événements en tiennent compte.

### 6. Consigner silencieusement
Jamais révélé avant de se produire en jeu.

---

## Catégories d'événements

| Catégorie | Description | Exemples |
|-----------|-------------|----------|
| **Opportunité** | Ressource, contact, information favorable, fenêtre d'action | Cargo abandonné, allié inattendu, information monnayable |
| **Complication** | Ce qui fonctionnait se dégrade | Fournisseur fiable disparu, route coupée, allié compromis |
| **Menace** | Danger actif et direct | Faction hostile en mouvement, catastrophe imminente, crise |
| **Révélation** | Information sur le monde ou l'histoire | Secret de faction révélé, trahison découverte, lore exposé |
| **Neutre** | Changement de contexte sans valence claire | Arrivée d'un personnage neutre, changement politique lointain |

---

## Gestion des événements non résolus

Un événement non résolu à la fin de sa fenêtre **ne disparaît pas** — il mute.

| Situation | Mutation |
|-----------|----------|
| Partiellement traité | Réduit en intensité, reste actif |
| Ignoré | Prend de l'ampleur à la prochaine fenêtre |
| Aggravé par le joueur | Escalade catégorielle (complication → menace) |
| Résolu complètement | Archivé ; peut générer des conséquences à long terme |

Un même événement peut traverser plusieurs fenêtres si le joueur ne le résout pas.
Avec Le Chroniqueur ou Le Juge, les événements ignorés ont tendance à former des chaînes.

---

## Principe de vraisemblance rétrospective

Les événements ne tombent **jamais ex nihilo**.
Ils doivent toujours sembler logiques rétrospectivement, même s'ils n'étaient pas prévisibles.

Si un tirage produit quelque chose qui semble artificiel dans le contexte actuel,
le MJ ajuste la **forme** (pas la catégorie ni l'intensité) pour que l'événement
s'ancre dans ce que le monde a déjà établi.
