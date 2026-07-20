# Identification d'acronyme — Méthode de raisonnement

But : donner, pour **n'importe quel** véhicule ou élément de personnel (toute nation,
toute époque), l'acronyme v4 **le plus évident** — celui qui sera retenu par défaut et
restera cohérent avec les autres fichiers. Un même engin *peut* recevoir plusieurs codes
défendables ; ce module tranche vers un seul canonique.

---

## Principe fondateur — le châssis fixe le Type

> **Règle tacite (Florian).** Dans la très grande majorité des cas, un même véhicule
> décliné en plusieurs variantes **sur le même châssis** garde le **même acronyme de
> Type**. Seules les sections Rôle/Armement changent.

- Châssis **VAB** → Type `VTT` toujours : `VTT-MOR`, `VTT-SIG`, `VTT-SAN`, `VTT-ATGM/LMG`, `VTT-GEN`…
- Châssis **VBL** → Type `V` toujours : `V-HMG`, `V-ATGM`, `V-LMG`, `V-GMG`, `V-AAGM`…

**Conséquence directe sur la méthode** : identifier, c'est
1. **classer le châssis → Type** (stable, la partie difficile), puis
2. **classer l'armement/rôle → suffixes** (variable, mécanique).

*Exception* (rare) : quand une variante franchit un **seuil de catégorie** — soit parce que
le châssis change radicalement de fonction (tourelle retirée transformant un char en
porte-mortier dédié), soit parce que l'**armement** change de palier (ex. `TV` vs `V`,
voir corollaire ci-dessous). À signaler, jamais à supposer.

---

## Pipeline d'identification (6 étapes)

1. **Châssis → Type.** Questions discriminantes : chenillé ou à roues ? blindé ou souple ?
   gabarit (L/M/H) ? tourelle avec arme principale ou non ? **fonction primaire du
   châssis** (char / IFV / APC / automitrailleuse / camion / hélico…) ?
   → décision dans `chassis-types.md`.
2. **Rôle/armement primaire → 1ᵉʳ suffixe**, par importance opérationnelle décroissante.
3. **Rôle/armement secondaire(s) → suffixes suivants.**
4. **Notation numérique / gabarit** : calibre `.NN`, roues `#`, tubes `#ACR`, variante `(#)`
   (voir SKILL.md « Notation numérique »).
5. **Fusions prédéfinies, anti-doublon, décisions établies** (SKILL.md).
6. **Canonicaliser** (« le plus évident », ci-dessous), **vérifier**, **journaliser** au lexique.

---

## Le « plus évident » — règles d'arbitrage

Quand plusieurs codes sont défendables, appliquer dans l'ordre :

- **P1 — Châssis avant rôle.** Le Type reflète la fonction *primaire du châssis*, pas le
  rôle du moment.
- **P2 — Parcimonie.** Le code le plus court qui distingue. N'ajouter un suffixe que s'il
  sépare de variantes réellement pertinentes dans le contexte.
- **P3 — Classe avant modèle.** Coder la **classe fonctionnelle** ; le nom réel du véhicule
  vit dans la description (et, pour les petites unités, dans le nom d'échelon).
- **P4 — Fusion avant chaînage.** Préférer une fusion prédéfinie (`MCAA`, `VBCI`, `TES`…)
  à un enchaînement d'acronymes.
- **P5 — Cohérence du lexique.** Si le châssis possède déjà un Type dans `lexique.json`,
  le réutiliser tel quel (c'est la règle tacite en action, garante de la cohérence
  inter-fichiers et inter-époques).

---

## Cas d'école — même concept, Type différent selon le châssis

L'« artillerie automotrice » ne donne **pas** un Type à elle seule : c'est le châssis qui
tranche, l'artillerie n'est que le rôle.

| Engin | Châssis | Type | Rôle | Code |
|-------|---------|------|------|------|
| CAESAR (155 sur camion) | camion | `VU` | artillerie | **`VU-ART`** |
| GCT / AUF1 (155, tourelle, chenillé dédié) | automoteur dédié | `SP` | artillerie | **`SPART`** |

Même leçon côté AA : un canon AA **tracté** (rôle sur affût) ≠ un `SP-AACA` (châssis
automoteur dédié, type Guépard).

### Corollaire — armement et protection réels, jamais silhouette

Le principe se généralise : **le Type se décide sur le niveau d'armement et de
protection réels, pas sur l'apparence** (tourelle, gabarit visuel, nom de plateforme).
Cas typique : les blindés à roues. `TV` (« char à roues ») et `V`/`VB` (voiture blindée)
peuvent tous deux porter une tourelle — la bascule vers `TV` demande qu'armement **et**
protection atteignent ensemble le niveau d'un **char léger** de son époque ; `TV` est
littéralement l'équivalent d'un char léger, à ceci près qu'il roule sur roues plutôt que
sur chenilles (mobilité tout-terrain moindre, cuirasse et puissance de feu comparables).
Un seul des deux critères ne suffit pas. Ainsi l'AML-60 (mortier 60mm, blindage léger)
reste `V`, l'AML-90 (canon 90mm, blindage renforcé) devient `TV` — même famille de
véhicule, Type différent, parce que l'ensemble armement+protection franchit un seuil de
catégorie (exception volontaire à la règle du châssis : ici c'est l'armement/protection,
pas le châssis, qui discrimine le Type). Détail dans `chassis-types.md`.

---

## Rôles à ne pas confondre

Quelques rôles proches se laissent facilement confondre lors de l'identification.
Toujours vérifier contre `references/terrestres.md` (section « Rôles terrestres »)
plutôt que de supposer par intuition.

| Rôle | Signification | Piège fréquent |
|------|---------------|-----------------|
| `ENG` | Ingénieur (génie : déminage, franchissement, fortification) | Ne pas utiliser pour un simple véhicule de traction/remorquage |
| `TRK` | Tracteur / remorquage | C'est le rôle correct pour « véhicule de tractage » |
| `SD` | Furtif (silence/discrétion) | Distinct de `STH` |
| `STH` | Stealth (furtivité visuelle/radar) | Distinct de `SD` |
| `NV` | Nocturne (rôle, vision nocturne opérationnelle) | Distinct de `NVG` (équipement spécifique, jumelles) |

> Exemple corrigé : dans `ORBAT_2023`, le code `V-ENG` porte la description *« Vehicule
> de tractage »* — la description appelle `TRK`, pas `ENG`. Le fichier source garde son
> code d'origine (jamais modifié sans demande explicite), mais le lexique note la
> correspondance réelle pour ne pas reproduire la confusion sur de futurs fichiers.



Chaque cas résolu → l'ajouter à `lexique.json` (couche « idiolecte » : `désignation réelle
↔ code v4`). C'est ce registre, amorcé depuis `ORBAT 2023`, qui garantit qu'un même engin
reçoive **toujours** le même code, quel que soit le fichier, l'armée ou la période.
