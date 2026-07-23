# Référence — Grille de cohérence & checklist

À lire **à chaque validation**. Contient la grille 0–5 détaillée, la checklist des pièges à passer en revue, et des exemples travaillés.

## Grille 0–5 détaillée

- **5 — Observé / parfaitement crédible.** Correspond à une configuration réellement observée ou pleinement compatible avec toute la physique connue. Aucun correctif. Ex. : G, planète tellurique dans la zone habitable avec atmosphère et champ magnétique, géantes gazeuses au-delà, grande lune dans la sphère de Hill.
- **4 — Solide.** Aucune violation. Un ou deux traits **rares** (mais permis) gagneraient à être justifiés. Un connaisseur adhère sans réserve majeure.
- **3 — Plausible avec réserves.** Marche globalement, mais repose sur de l'**improbable-mais-possible** ou laisse des points sensibles **sous-spécifiés**. Bon pour la fiction ; un scientifique lève un sourcil. Ex. typique : monde habité autour d'une naine M avec parades correctement posées.
- **2 — Problèmes réels.** De **vrais soucis physiques** (stabilité limite, rétention atmosphérique douteuse, bord de zone habitable, excentricité trop forte pour un climat stable) entament la crédibilité mais sont **corrigeables** par ajustement de valeurs.
- **1 — Violations majeures.** Brise la physique de façon **rédhibitoire** : objet solide dans la limite de Roche, lune hors sphère de Hill, monde de milliards d'années autour d'une O/B/A, densité incompatible avec la composition annoncée. Concept **sauvable via refonte** (changer le type d'étoile, la distance, etc.).
- **0 — Impossible / contradictoire.** **Auto-contradictoire** ou physiquement impossible sans correctif local possible. Ex. : « lune liée » décrite au-delà de la sphère de Hill **et** planète à l'intérieur de la limite de Roche de son étoile **et** vie de 5 Ga sur une étoile qui vit 5 Ma — accumulation d'impossibles. À repenser entièrement.

**Règle d'attribution** : partir de 5, **descendre** à chaque problème selon sa gravité. Un seul « impossible » plafonne bas (1 ou 0). Plusieurs « improbables » sans impossible → 3. Un système propre → 4–5. Ne pas surnoter par gentillesse ni sous-noter par excès de zèle.

## Checklist des pièges (passer chaque point en revue)

Pour chaque système, vérifier au minimum :

1. **Durée de vie stellaire vs âge annoncé** — l'étoile vit-elle assez longtemps pour l'âge de la vie/civilisation évoqué ? (formule `t ≈ 10 Ga × M^−2,5`, cf. `etoiles.md`). Test très discriminant.
2. **Zone habitable** — la planète « habitable » est-elle dans la fourchette `√L × [0,95–1,37] UA` ? (cf. `habitabilite.md`).
3. **Cohérence luminosité ↔ type stellaire** — la couleur/température/luminosité annoncées collent-elles à la classe (cf. table `etoiles.md`) ?
4. **Stabilité multi-planètes** — orbites adjacentes séparées d'assez de rayons de Hill mutuels (≳ 8–10) ? Sinon, résonance protectrice ? Orbites qui se croisent ?
5. **Systèmes binaires** — planète dans une zone stable : S-type `a ≲ 0,2–0,3 a_bin` ou P-type `a ≳ 2–4 a_bin` ? Pas dans la zone instable intermédiaire ?
6. **Lune dans la sphère de Hill** — `< ~0,5 r_Hill` (prograde) ? Une lune décrite au-delà = impossible.
7. **Limite de Roche** — aucun corps **solide** à l'intérieur (sinon il se disloque) ; un système d'**anneaux** y est en revanche cohérent. Lunes dehors, anneaux dedans.
8. **Densité ↔ composition** — recalculer `ρ ∝ M/R³` et confronter à la nature annoncée (fer/roche/glace/gaz, cf. `planetes.md`).
9. **Gravité de surface** — `g = (M/M⊕)/(R/R⊕)² × g⊕` cohérente avec la « pesanteur » décrite ?
10. **Rétention atmosphérique** — un petit corps chaud garde-t-il vraiment une atmosphère épaisse ? (rivage cosmique, cf. `planetes.md`).
11. **Verrouillage de marée** — planète proche d'une étoile peu lumineuse : devrait être verrouillée. Un cycle jour/nuit terrestre y est incohérent.
12. **Excentricité** — `e` fort (≳ 0,3) avec un « climat stable » ? Le périastre entre-t-il dans une zone dangereuse ?
13. **Orbites rétrogrades / très inclinées** — justifiées par une capture ? Sinon suspect.
14. **Longévité / confinement des anneaux** — anneaux « éternels » sans lunes bergères ni source ? À nuancer.
15. **Obliquité / durée du jour** — saisons stables sans stabilisateur d'axe (grosse lune) ? Rotation cohérente ?
16. **Plateau des géantes** — une géante gazeuse « énorme » n'a pas un rayon démesuré (rayon ~ Jupiter même à plusieurs masses joviennes).
17. **Nombre / couleur des soleils** — décrits de façon cohérente (teintes, flux combinés, zone habitable résultante) ?

Ne pas tout imposer : signaler ce qui est **sous-spécifié** comme tel plutôt que d'inventer, et concentrer le diagnostic sur les points qui font réellement bouger l'indice.

## Exemples travaillés

**Exemple 5/5 — « Système Sol-like »**
Étoile G (1 M☉, 1 L☉, ~10 Ga). Planète tellurique à 1 UA, densité ~5,5, atmosphère azote/oxygène, champ magnétique, grande lune à ~0,26 r_Hill. Géantes gazeuses au-delà de 5 UA. → Durée de vie OK, zone habitable OK (1 UA ∈ [0,95;1,37]), lune liée, densité cohérente. **Rien à corriger : 5/5.**

**Exemple 4/5 — « Deux soleils crédibles »**
Binaire serré (deux K, séparation 0,1 UA). Planète circumbinaire à 0,6 UA (> 3 × 0,1 = 0,3 UA → zone stable). Zone habitable combinée ~0,5–0,7 UA selon la luminosité cumulée. → Configuration stable et observée (type Kepler-16). Réserve mineure : bien décrire l'éclairement à deux teintes et les cycles. **4/5.**

**Exemple 3/5 — « Monde de naine M »**
Naine M (0,2 M☉, 0,006 L☉). Planète à 0,08 UA (√0,006 ≈ 0,077 → zone habitable ~0,073–0,105 UA : OK). Verrouillée par les marées → habitabilité au terminateur, atmosphère épaisse pour redistribuer la chaleur, champ magnétique fort contre les éruptions. → Physiquement permis **si** les parades sont posées ; sinon (cycle jour/nuit naïf, ciel calme) ça tombe. **3/5** tel quel, avec réserves sur l'activité stellaire.

**Exemple 2/5 — « Petit monde à l'atmosphère improbable »**
Planète type Mars (0,1 M⊕, 0,5 R⊕ → g ≈ 0,4 g, v_lib faible) à 0,8 UA d'une G, censée garder une atmosphère dense et respirable depuis des milliards d'années sans réapprovisionnement. → Rétention douteuse (rivage cosmique) : elle devrait avoir perdu son atmosphère. Corrigeable : augmenter la masse, ou expliquer une source (volcanisme actif, réapprovisionnement). **2/5.**

**Exemple 1/5 — « Vieux monde autour d'un soleil bleu »**
Étoile bleue massive (type O/B, ~20 M☉ → durée de vie ~2–10 Ma) avec une civilisation « vieille de milliards d'années ». → Violation majeure : l'étoile est morte des milliards de fois trop tôt. Sauvable : remplacer par une K ou G. **1/5** (concept ok, étoile fausse).

**Exemple 0/5 — « Empilement d'impossibles »**
« Lune » décrite en orbite stable **bien au-delà** de la sphère de Hill de sa planète, planète elle-même **à l'intérieur** de la limite de Roche de son étoile, le tout autour d'un astre qui vivrait 3 Ma pour une vie de 4 Ga. → Plusieurs impossibilités simultanées sans correctif local. **0/5 : à repenser entièrement.**
