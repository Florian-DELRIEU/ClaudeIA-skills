---
name: prompt-image
description: >
  Skill de génération de prompts image ultra-précis pour IA générative (Midjourney, DALL-E, Stable Diffusion, Flux, Leonardo, etc.).
  Déclencher IMPÉRATIVEMENT dès que l'utilisateur tape /prompt, demande "génère un prompt image", "crée un prompt pour [sujet]", "je veux une image de X", "prompt pour [IA]", ou toute formulation proche. Aussi déclencher si l'utilisateur décrit une scène et mentionne une IA image. Ce skill permet à Claude d'extraire précisément la vision de l'utilisateur et de produire un prompt structuré, riche et prêt à coller dans n'importe quelle IA image.
---

# Skill : Génération de Prompts Image (`/prompt`)

## Objectif

Produire un prompt image **précis, riche et directement utilisable** par une IA générative tierce, qui reproduit **exactement** la vision de l'utilisateur — sans interprétation parasite de la part de l'IA image.

---

## Workflow

### Étape 1 — Extraction de la vision

Si l'utilisateur tape `/prompt` seul ou avec une description vague, poser **une seule question ouverte** :

> "Décris-moi ta scène : sujet principal, style souhaité, ambiance, et sur quelle IA tu veux l'utiliser ?"

Si l'utilisateur donne déjà une description, **ne pas redemander** — extraire directement et compléter les lacunes avec des choix sensés, mentionnés explicitement dans le prompt final.

**Informations à extraire (ou déduire intelligemment) :**

| Dimension | Ce qu'on cherche |
|---|---|
| **Sujet** | Personnage, objet, créature, scène, concept |
| **Environnement** | Décor, époque, planète, intérieur/extérieur |
| **Style artistique** | Photo-réaliste, peinture à l'huile, concept art, anime, etc. |
| **Éclairage** | Naturel, doré, dramatique, néon, volumétrique… |
| **Ambiance / Mood** | Sombre, épique, mélancolique, mystique, claustrophobe… |
| **Palette chromatique** | Chaude, désaturée, monochrome, contrastée… |
| **Composition** | Plan, angle de caméra, profondeur de champ, point focal |
| **Références** | Artiste, film, style précis ("comme Warhammer 40K", "comme Blade Runner") |
| **IA cible** | Midjourney, DALL-E 3, Stable Diffusion, Flux, Leonardo, Firefly… |
| **Ratio / Format** | Portrait, paysage, carré, cinémascope |

---

### Étape 2 — Construction du prompt

Assembler le prompt dans cet **ordre canonique** (valable pour toutes les IA) :

```
[SUJET PRINCIPAL] + [ACTION/POSE] + [ENVIRONNEMENT/DÉCOR] + [STYLE ARTISTIQUE] + [ÉCLAIRAGE] + [AMBIANCE/MOOD] + [PALETTE CHROMATIQUE] + [COMPOSITION/CADRAGE] + [DÉTAILS TECHNIQUES] + [RÉFÉRENCES STYLISTIQUES]
```

**Règles de rédaction :**
- Toujours en **anglais** (toutes les IA image fonctionnent mieux en anglais)
- Termes **séparés par des virgules**, pas de phrases longues
- Adjectifs **précis et évocateurs** — bannir les mots génériques (`beautiful`, `amazing`, `nice`)
- **Empiler les modificateurs de qualité** en fin de prompt si la cible le supporte
- Ne pas dépasser **~120-150 mots** pour le prompt positif (au-delà, l'IA dilue)

---

### Étape 3 — Adaptation à l'IA cible

Consulter `references/ai-syntax.md` pour les paramètres spécifiques à l'IA cible.

Résumé rapide :

| IA | Syntaxe | Paramètres clés |
|---|---|---|
| **Midjourney** | Prompt libre + `--params` en fin | `--ar`, `--v 6.1`, `--style raw`, `--q`, `--chaos`, `--no` |
| **DALL-E 3** | Langage naturel structuré | Pas de params, tout dans le texte |
| **Stable Diffusion** | Prompt positif + négatif séparé | Poids `(terme:1.3)`, `--neg` |
| **Flux** | Langage naturel dense | Très littéral, décrire précisément |
| **Leonardo** | Similaire SD | Styles preset + prompt texte |
| **Firefly** | Langage naturel + styles | Sélection de style dans l'interface |

---

### Étape 4 — Prompt négatif (si pertinent)

Pour SD / Flux / Leonardo, toujours fournir un **prompt négatif** adapté.

Négatifs universels à inclure quasi-systématiquement :
```
ugly, deformed, blurry, low quality, bad anatomy, watermark, signature, text, duplicate, extra limbs, mutated hands, poorly drawn face, out of frame, cropped, jpeg artifacts
```

Ajouter selon le contexte :
- Portraits : `bad eyes, crossed eyes, asymmetrical face`
- Architectures : `distorted perspective, impossible geometry`
- Scènes de foule : `duplicate faces, cloned figures`

---

### Étape 5 — Output final

Présenter de façon claire et copiable :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 PROMPT [NOM DE L'IA]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Prompt positif complet]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚫 PROMPT NÉGATIF (si applicable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Prompt négatif]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ PARAMÈTRES SUGGÉRÉS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Paramètres spécifiques à l'IA]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 VARIATIONS SUGGÉRÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2-3 variations rapides si pertinent]
```

Toujours proposer **2-3 variations** courtes à la fin (ex : "version nuit", "version close-up", "version plus sombre").

---

## Pièges à éviter

- ❌ Termes trop vagues : `beautiful scene`, `epic image`, `amazing art` → aucun impact
- ❌ Instructions négatives dans le prompt positif : dire "sans fond blanc" dans le positif est inefficace
- ❌ Surcharger le prompt : trop de sujets = dilution de l'attention de l'IA
- ❌ Omettre le style : sans style défini, l'IA choisit, souvent mal
- ❌ Traduction littérale du français : certains termes n'ont pas d'équivalent — chercher le terme technique anglais du domaine

---

## Vocabulaire de référence

Pour les styles, l'éclairage et l'ambiance détaillés → lire `references/style-vocabulary.md`

---

## Exemple complet

**Input utilisateur :** `/prompt Un ancien chevalier spatial en armure ornée marchant dans les ruines d'une cathédrale, ambiance Warhammer 40K sombre, Midjourney`

**Output :**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 PROMPT MIDJOURNEY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ancient space knight in ornate battle-worn power armor, walking through the ruins of a gothic cathedral, shattered stained glass windows, dim volumetric light rays piercing through collapsed vault, rubble and ash, grim dark atmosphere, oppressive scale, hyper-detailed sculpted pauldrons and engravings, dark green and bronze color palette, dramatic side lighting, cinematic wide shot, low angle camera, depth of field, concept art, Warhammer 40000 aesthetic, John Blanche style, Jim Murray style --ar 16:9 --v 6.1 --style raw --q 2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ PARAMÈTRES SUGGÉRÉS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

--ar 16:9 (cinémascope)
--v 6.1
--style raw (moins d'embellissement automatique)
--q 2 (haute qualité)
--chaos 10 (légère variation entre les seeds)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 VARIATIONS SUGGÉRÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Portrait serré : ajouter "extreme close-up portrait, weathered face beneath open visor" + --ar 3:4
• Version combat : remplacer "walking" par "charging forward, chainsword raised, bolter fire in background"
• Ambiance plus sombre : ajouter "pitch black shadows, single torch light, blood-stained floor" + --chaos 20
```
