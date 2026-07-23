# Référence — Calculs et analyse quantitative

La boîte à outils chiffrée. Ici, **poser de vrais nombres** (pas seulement des ordres de grandeur), et **écrire un script Python** pour toute courbe, balayage ou comparaison. Ce fichier centralise atmosphère, unités, grandeurs calculables, méthode, et exemples.

## Sommaire
- Constantes et atmosphère standard (ISA)
- Altitude-densité
- Conversions d'unités aéro/sim
- Tableau des grandeurs calculables
- Quand calculer à la main vs écrire un script
- Exemples travaillés
- Lire la télémétrie d'un simulateur

## Constantes et atmosphère standard (ISA)

- `g` ≈ **9,81 m/s²**. `ρ₀` (niveau mer, 15 °C) ≈ **1,225 kg/m³**. `p₀` ≈ 101 325 Pa. `a₀` (vitesse du son, niveau mer) ≈ **340 m/s**.
- Viscosité cinématique `ν` (niveau mer) ≈ 1,46×10⁻⁵ m²/s.
- **Gradient thermique ISA** (troposphère, 0–11 km) : **−6,5 °C/km**. `T(h) = 288,15 − 6,5·h(km)` (K).
- **Pression** : `p(h) = p₀·(1 − 0,0065·h/288,15)^5,256` (h en m).
- **Densité** : `ρ(h) = ρ₀·(1 − 0,0065·h/288,15)^4,256`. Repères : ρ ≈ **0,90 ρ₀** à 1 km, **~0,74 ρ₀** à 3 km, **~0,53 ρ₀** à 6 km.
- **Vitesse du son** : `a = √(γ·R·T)` avec γ = 1,4, R = 287 J/(kg·K) → `a ≈ 20,05·√T(K)` m/s. À 11 km (~217 K) : a ≈ 295 m/s.

## Altitude-densité

La densité chute avec l'altitude et la chaleur → **toutes les performances se dégradent en altitude/densité faible** :

- La **portance** à CL/V donnés baisse (∝ ρ) → **Vs vraie augmente** (∝ 1/√ρ) ; décollage/atterrissage plus longs.
- La **traction** d'hélice et la **puissance moteur atmosphérique** chutent (sauf turbo/compresseur) → **montée dégradée**, plafond limité.
- **Anémomètre** : il mesure la vitesse **indiquée** (≈ pression dynamique). La **vitesse vraie (TAS)** ≈ `IAS/√(ρ/ρ₀)` → en altitude, TAS **> IAS** (à 6 km, TAS ≈ 1,37×IAS). Les décrochages/Vs se raisonnent en **IAS** ; la vitesse sol et la nav en **TAS**.
- **Conséquence sim** : « pourquoi je décolle si mal / monte si peu ? » → aéroport haut + chaud = altitude-densité élevée. Raisonner en IAS pour les vitesses de manœuvre.

## Conversions d'unités aéro/sim

- Vitesse : **1 nœud (kt) = 0,5144 m/s = 1,852 km/h**. 1 m/s = 1,944 kt. Mach → m/s : `V = M·a`.
- Distance/altitude : **1 pied (ft) = 0,3048 m**. 1 m = 3,281 ft. **1 mille nautique (NM) = 1,852 km**.
- Taux : **1 ft/min = 0,00508 m/s** ; 1 m/s ≈ 196,9 ft/min. (Un « bon » taux léger ≈ 700–1000 ft/min ; un jet à basse altitude ≥ plusieurs milliers.)
- Pression d'admission : **1 inHg = 33,86 hPa (mbar)**. Admission « pleine » niveau mer ≈ 29,92 inHg ≈ 1013 hPa (les moteurs suralimentés dépassent).
- Poids/masse : **1 lb = 0,4536 kg** ; g force `W(N) = m(kg)·9,81`.

## Tableau des grandeurs calculables

| Grandeur | Formule | Entrées |
|---|---|---|
| Portance / traînée | `L=½ρV²S·CL` ; `D=½ρV²S·CD` | ρ, V, S, CL/CD |
| Vitesse de décrochage | `Vs=√(2W/(ρ·S·CLmax))` | W, ρ, S, CLmax |
| Vs en virage / sous facteur n | `Vs·√n` | Vs, n |
| Facteur de charge (virage palier) | `n=1/cos φ` | φ (inclinaison) |
| Rayon de virage | `R=V²/(g·tan φ)` | V, φ |
| Taux de virage | `ω=g·tan φ/V` (rad/s) | V, φ |
| Vitesse de manœuvre | `Va=Vs·√(n_limite)` | Vs, n_limite |
| Traînée induite | `CDi=CL²/(π·AR·e)` | CL, AR, e |
| Polaire | `CD=CD0+CL²/(π·AR·e)` | CD0, CL, AR, e |
| Finesse | `L/D=CL/CD` ; distance plané = finesse×altitude | CL, CD |
| Taux de montée | `Vz=(P_dispo−P_req)/W` | puissances, W |
| Paramètre d'avancement | `J=V/(n·D)` | V, n (tr/s), D |
| Angle d'avance de pale | `φ=arctan(V/(2π·n·r))` | V, n, r |
| Incidence locale de pale | `α=β−φ` | β (calage), φ |
| Rendement d'hélice | `η=J·CT/CP=(T·V)/P` | J, CT, CP (ou T,V,P) |
| Vitesse bout de pale | `√((2π·n·R)²+V²)` ; Mach = /a | n, R, V, a |
| Énergie spécifique | `Es=h+V²/(2g)` | h, V |
| Puissance spécifique excéd. | `Ps=V(T−D)/W` | V, T, D, W |
| Nombre de Reynolds | `Re=V·L/ν` | V, corde L, ν |
| TAS depuis IAS | `TAS≈IAS/√(ρ/ρ₀)` | IAS, ρ |

## Quand calculer à la main vs écrire un script

- **À la main** : un chiffre ponctuel (Vs à telle masse, rayon de virage à 60°, facteur de charge, Mach en bout de pale à tel régime). Poser la formule, injecter, donner le résultat avec unité et sens physique.
- **Script Python** (dans ce runtime, exécuter réellement) : dès qu'il y a une **courbe**, un **balayage** ou une **comparaison** —
  - tracer une **polaire** ou une **courbe de rendement d'hélice** η(J) ;
  - comparer le **rayon/taux de virage** de deux appareils sur une plage de vitesse ;
  - un **diagramme V-n** ;
  - la variation d'une performance avec l'**altitude-densité** ;
  - un **diagramme d'énergie** (Ps vs vitesse/altitude) pour un combat sim.
  Utiliser numpy/matplotlib, sortir un graphe, et **interpréter** le résultat pour le pilotage. Toujours annoncer les hypothèses (CD0, e, CLmax, poussée estimés si non fournis).

## Exemples travaillés

**Vitesse de décrochage.** Avion léger, W = 11 000 N (~1120 kg), S = 16 m², CLmax = 1,5, niveau mer (ρ = 1,225).
`Vs = √(2·11000 / (1,225·16·1,5)) = √(22000/29,4) = √748 ≈ 27,4 m/s ≈ 53 kt.`
→ En virage à 60° (n = 2) : `Vs·√2 ≈ 38,7 m/s ≈ 75 kt` : on décroche à 75 kt en virage serré alors qu'on tient 53 kt en palier.

**Rayon et taux de virage.** V = 60 m/s (~117 kt), φ = 45°.
`R = 60²/(9,81·tan45°) = 3600/9,81 ≈ 367 m.` `ω = 9,81·1/60 ≈ 0,164 rad/s ≈ 9,4 °/s.`
→ À 60° (tan = 1,73) : R ≈ 212 m, ω ≈ 16,3 °/s : virage bien plus serré, mais n = 2.

**Mach en bout de pale.** Hélice D = 2 m (R = 1 m), n = 2700 tr/min = 45 tr/s, V = 50 m/s, niveau mer (a = 340).
`U_bout = 2π·45·1 ≈ 283 m/s.` Vitesse résultante `= √(283²+50²) ≈ 287 m/s.` `Mach ≈ 287/340 ≈ 0,84.`
→ Déjà élevé : monter le régime ou le diamètre pousse vers Mach 1 en bout → chute de rendement. D'où réducteur/multipales.

**Incidence locale de pale.** À r = 0,75 m, β = 25°, V = 50 m/s, n = 45 tr/s.
`φ = arctan(50/(2π·45·0,75)) = arctan(50/212) ≈ 13,3°.` `α = 25 − 13,3 ≈ 11,7°` : bonne incidence de travail. Si V passe à 90 m/s (à n fixe) : `φ = arctan(90/212) ≈ 23°` → `α ≈ 2°` : la pale ne « mord » presque plus → il faudrait augmenter le calage (grand pas) pour retrouver de la traction → c'est tout l'intérêt du pas variable.

## Lire la télémétrie d'un simulateur

- Beaucoup de sims exposent les **vraies grandeurs** (IAS, TAS, Mach, altitude, taux, facteur de charge g, régime, admission, angle d'incidence, carburant). DCS/MSFS/X-Plane via leurs jauges, débogueurs ou export de données ; on peut **valider un calcul** contre ces valeurs.
- Méthode de diagnostic chiffré : relever quelques points (ex. IAS/altitude/g au moment du décrochage en virage), les confronter à `Vs·√n`, et en déduire si le comportement est cohérent avec le modèle ou si Florian pilote hors du domaine.
- Attention aux **unités du sim** (kt vs km/h, ft vs m, inHg vs hPa) : convertir avant de comparer. Distinguer **IAS** (ce que lit l'anémomètre, pour les vitesses de manœuvre) de **TAS** (pour la nav et l'énergie réelle).
