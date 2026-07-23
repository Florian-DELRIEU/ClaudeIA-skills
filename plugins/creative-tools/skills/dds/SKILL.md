---
name: dds
description: Génère des prompts d'image ultra-détaillés pour les icônes d'équipement style Hearts of Iron IV (HOI4) — moteurs (en ligne, en étoile/rotatif, en V), hélices, canons, blindages, modules de véhicule/navire/avion, ou tout autre équipement militaire. Déclencher IMPÉRATIVEMENT dès que Florian tape /dds, ou demande une "icône d'équipement", une "icône HOI4", un "moteur en rendu 3D style jeu", ou toute image de pièce mécanique isolée sur fond noir façon rendu produit sombre et métallique. Produit systématiquement DEUX versions du prompt (tags Midjourney + paragraphe descriptif en langage naturel) qui respectent la palette bleu-cyan froide, l'éclairage de contour, le fond quasi noir et le système de badges de palier en chiffres romains (I à IV) déjà établis par Florian. Déclencher aussi pour des demandes courtes ("fais-moi un moteur radial tier III", "prompt pour un canon AA", "même style que d'habitude mais pour un blindage").
---

# /dds — Générateur de prompts d'icônes d'équipement (style HOI4)

Ce skill génère des prompts d'image prêts à coller dans Midjourney (ou toute IA image à base de description naturelle) pour produire des icônes d'équipement dans le style établi par Florian : rendu 3D produit, isolé, sombre, métallique, façon icône de jeu vidéo (Hearts of Iron IV et assimilés).

Toujours produire **deux formats** du même prompt (sauf si Florian en demande explicitement un seul) :
1. **Version tags** (style Midjourney, avec paramètres `--ar --v --style raw --q --no`)
2. **Version descriptive** (paragraphe en langage naturel, pour les IA sans support de tags comme DALL-E ou Flux)

## 1. Bible visuelle (invariants — ne jamais dévier sans instruction explicite)

Ces éléments sont fixes sur TOUTE icône produite par ce skill, quel que soit l'équipement représenté :

- **Fond** : quasi noir / near-black, uni, sans texture, sans sol, sans ombre portée visible
- **Composition** : objet unique, isolé, centré, cadrage carré (1:1)
- **Angle** : vue de trois-quarts face légère, produit-render, jamais de profil pur ni de dessus
- **Éclairage** : rim light cyan qui trace les arêtes/contours de l'objet, reflets spéculaires nets sur métal, pas de lumière chaude
- **Palette** : teintes froides désaturées — bleu-cyan métallique par défaut. Voir §3 pour les variantes de teinte par famille.
- **Ambiance** : "dark technical museum-render mood" — sobre, technique, pas de mise en scène, pas de texte, pas de watermark
- **Finition** : rendu 3D propre, aluminium/métal poli ou brossé, haute définition, mise au point nette (sharp focus)
- **Registre** : "video game equipment icon" — doit matcher l'esthétique des autres icônes d'équipement déjà produites (cohérence de set)

Négatifs systématiques (version tags) : `--no text, watermark, wood, ground, shadow on floor, warm tones`

## 2. Système de paliers (badges de tier)

Les icônes suivent une progression par palier, visible via un badge en chiffres romains :

- **Base / master art** : aucun badge — c'est l'icône "générique" de l'équipement (souvent une teinte plus neutre/grise que les paliers supérieurs)
- **Palier I, II, III, IV** : badge chiffre romain correspondant, généralement en bas à droite du cadre, dans un style graphique sobre cohérent avec le reste du set

Quand Florian demande une icône avec un palier précis, l'inclure explicitement dans le prompt : `roman numeral tier badge "III" in bottom-right corner, minimal flat icon style, matching the game's UI badge style`.
Si Florian ne précise pas de palier, demander lequel (base, I, II, III ou IV) sauf s'il a dit "sans badge"/"master art".

## 3. Variation de teinte par famille d'équipement

Le bleu-cyan froid est la valeur par défaut, mais Florian utilise aussi d'autres teintes métalliques pour distinguer visuellement certaines familles d'équipement tout en gardant fond, lumière et composition identiques. Références connues dans `assets/reference/` :

- **Moteurs en ligne** (`inline_*.jpg`) : bleu-acier froid, bloc-moteur anguleux
- **Moteurs rotatifs/en étoile** (`rotary_*.jpg`) : bronze/or chaud-métallique en étoile radiale (le seul cas où la teinte n'est pas bleue — garder quand même fond noir + rim light cohérent)
- **Moteurs radiaux** (`radial_*.jpg`) : bleu-cyan cristallin, aspect facetté "gemme" (cylindres rayonnants traités comme des facettes de diamant)
- **Moteurs en V** (`v_*.jpg`) : bleu-acier sombre, bloc massif type blindé
- **Hélices** : bleu-cyan métallique poli (voir prompts de référence ci-dessous, fournis tels quels par Florian)

→ Par défaut, rester en bleu-cyan froid pour toute nouvelle famille d'équipement. Ne proposer une teinte différente (or/bronze, acier gris, etc.) que si Florian le demande, ou si une distinction visuelle entre familles proches est utile — et le signaler explicitement dans ce cas plutôt que de décider silencieusement.

## 4. Gabarits de prompts de référence (fournis par Florian, à utiliser comme calibrage de ton et de niveau de détail)

**Version tags (hélice quadripale)** :
```
four-bladed WWII aircraft propeller, polished machined aluminium blades radiating from a central conical spinner hub, single isolated mechanical component, front-facing three-quarter view, studio product render, cold blue-cyan metallic finish, cyan rim lighting tracing the blade edges, subtle specular highlights on brushed metal, deep near-black background, dark technical museum-render mood, desaturated steel-blue palette, centered composition, square framing, sharp focus, high detail, clean 3D render, video game equipment icon, matching aesthetic of radial and inline engine module icons --ar 1:1 --v 6.1 --style raw --q 2 --no text, watermark, wood, ground, shadow on floor, warm tones
```

**Version descriptive (même hélice)** :
```
A single four-bladed World War II aircraft propeller rendered as a clean 3D product icon, isolated and centered on a solid near-black background. The four polished aluminium blades radiate symmetrically from a central conical metal spinner hub, shown in a slight three-quarter front angle. The metal has a cold blue-cyan tint with crisp cyan rim lighting along the blade edges and soft specular reflections, giving a dark technical "museum render" look. Desaturated steel-blue palette, sharp focus, high detail, square icon composition. Matches the visual style of metallic aircraft engine module icons (radial and inline engines) with the same cold blue metallic tones and dark moody background.
```

Ces deux prompts sont le niveau de détail et le ton à reproduire : description physique précise de l'objet (matière, forme, structure), puis la bible visuelle du §1, puis en dernier la mention de cohérence avec le reste du set d'icônes.

## 5. Workflow

1. **Identifier l'équipement demandé** : type d'objet (moteur, hélice, canon, tourelle, blindage, radar, module naval, etc.), sa famille visuelle si elle existe déjà (voir §3), et son palier (base/I/II/III/IV).
2. Si l'équipement est ambigu (ex: "un canon" sans préciser AA/naval/char), poser une seule question ciblée plutôt que de deviner un détail structurant.
3. **Décrire l'objet physiquement** en 2-4 caractéristiques concrètes et spécifiques (forme, matière, composants visibles, disposition) — jamais une description vague. S'inspirer du niveau de précision des gabarits du §4 (ex: "quatre pales", "hub conique", "cylindres rayonnants depuis un carter central").
4. **Assembler le prompt tags** : description objet → bible visuelle §1 (fond, composition, angle, éclairage, palette, ambiance, finition, registre) → badge de palier si demandé (§2) → paramètres `--ar 1:1 --v 6.1 --style raw --q 2` → négatifs.
5. **Assembler le prompt descriptif** : même contenu réécrit en paragraphe fluide en anglais (les IA image répondent mieux en anglais, même si l'échange avec Florian est en français).
6. Livrer les deux versions clairement séparées, en blocs de code, prêtes à copier-coller. Ne pas ajouter de préambule long — Florian veut le prompt, pas une explication du processus.
7. Si Florian enchaîne plusieurs équipements dans la même demande (ex: toute une famille de paliers I à IV), produire un bloc par palier, dans l'ordre.

## 6. Références visuelles disponibles

`assets/reference/` contient des exemplaires réels déjà produits par Florian (base + paliers I/III/IV selon les familles) pour les moteurs en ligne, rotatifs, radiaux et en V. Les consulter (`view`) si un doute existe sur le rendu exact d'une famille existante avant de proposer une variation dans cette même famille.
