# Référence — Mécanique du vol

Équilibre des forces, performances, virages, domaine de vol, énergie. Formules exploitables.

## Sommaire
- Les quatre forces et l'équilibre
- Montée : Vx, Vy, plafond
- Descente et plané
- Virages : facteur de charge, rayon, taux
- Vitesse de manœuvre et vitesse coin
- Domaine de vol (diagramme V-n)
- Vitesses caractéristiques
- Gestion de l'énergie

## Les quatre forces et l'équilibre

Portance (L, ⊥ trajectoire, vers le haut), Poids (W, vers le centre Terre), Traction/Poussée (T, vers l'avant), Traînée (D, opposée à la trajectoire).

- **Palier stabilisé** : `L = W` et `T = D`. Rompre un équilibre change l'état (plus de poussée que de traînée → accélère ou monte).
- En **montée** stabilisée, la portance est **inférieure** au poids (elle n'équilibre que la composante perpendiculaire) : `L = W·cos γ` (γ angle de montée), et la poussée reprend la composante de poids le long de la trajectoire. Idée fausse fréquente : « on monte grâce à un surplus de portance » → non, on monte grâce à un **surplus de poussée/puissance**.

## Montée : Vx, Vy, plafond

La montée vit sur l'**excédent** de poussée (angle) ou de puissance (taux).

- **Taux de montée** : `Vz = (Pdispo − Prequise) / W` = puissance excédentaire / poids. Se lit en m/s ou ft/min.
- **Vx (pente max)** : vitesse du **maximum d'excédent de poussée** → meilleur gain d'altitude par distance sol (franchir un obstacle). Plus **lente**.
- **Vy (taux max)** : vitesse du **maximum d'excédent de puissance** → meilleur gain d'altitude par temps. Un peu plus **rapide** que Vx.
- Pour une hélice, `Vx < Vy`. Les deux se **rejoignent au plafond** : quand l'excédent tombe à zéro, il n'y a plus qu'une vitesse de montée possible → **plafond de propulsion**.
- **Conséquence sim** : décollage court/obstacle → grimper à Vx ; montée normale → Vy. Un jet a un excédent énorme à basse altitude (Vz spectaculaire), qui s'effondre en altitude.

## Descente et plané

- **Plané non motorisé** : l'avion descend le long d'une pente fixée par la finesse. `distance sol = finesse × altitude` (à vent nul). Voler à la **vitesse de finesse max** maximise la distance.
- Trop lent (sous la vitesse de finesse) *ou* trop rapide → on plane moins loin. Vent de face → accélérer un peu pour optimiser la distance sol ; vent arrière → ralentir légèrement.
- **Vitesse de taux de chute mini** (endurance/planeur en pompe) : plus lente que la finesse max, minimise la perte d'altitude par seconde mais pas la distance.
- Descente motorisée : on choisit pente et vitesse via **assiette + gaz** (voir gestion de l'énergie).

## Virages : facteur de charge, rayon, taux

En virage en palier coordonné à l'inclinaison φ :

- **Facteur de charge** : `n = 1 / cos φ`. À 30° → n = 1,15 ; **60° → n = 2** ; 75° → n ≈ 3,9. La portance doit valoir `n·W`.
- **La vitesse de décrochage augmente** : `Vs(virage) = Vs · √n`. À 60° (n=2), Vs augmente de √2 ≈ **+41 %**. D'où le **décrochage en virage serré** à vitesse pourtant confortable en palier.
- **Rayon de virage** : `R = V² / (g · tan φ)`. Plus lent et plus incliné → plus serré.
- **Taux de virage** : `ω = g · tan φ / V` (rad/s). Plus lent et plus incliné → tourne plus vite.
- **Conséquence combat sim** : pour tourner serré, on veut de la vitesse *basse* et de l'inclinaison *haute* — mais limité par le décrochage (aéro) et la structure (g max). Le meilleur compromis est la **vitesse coin** (ci-dessous).

## Vitesse de manœuvre et vitesse coin

- **Vitesse de manœuvre Va** : `Va = Vs · √(n_limite)`. En dessous de Va, l'avion **décroche avant** d'atteindre le facteur de charge structural (protection naturelle) ; au-dessus, tirer fort peut **casser** avant de décrocher. On vole ≤ Va en air turbulent.
- **Vitesse coin (corner speed)** : la vitesse la plus basse à laquelle on peut atteindre le **g maximal structural** — intersection de la courbe `Vs·√n` et de la limite `n_max`. C'est là que le **taux de virage instantané est maximal** (rayon le plus serré possible sans casser ni décrocher). Pour beaucoup d'appareils, corner speed ≈ Va.
- **Conséquence** : en dogfight sim, on cherche à combattre autour de la corner speed pour le meilleur virage ; trop rapide = rayon large, trop lent = on ne peut pas tirer le g.

## Domaine de vol (diagramme V-n)

Enveloppe reliant **facteur de charge** (vertical) et **vitesse** (horizontal). Bornes :

- **À gauche** : la courbe de décrochage `n = (V/Vs)²` — impossible de tirer plus de g sans décrocher.
- **En haut/bas** : limites structurales. Catégories typiques : **normale +3,8 / −1,5 g**, **utilitaire +4,4 / −1,8**, **acrobatique +6 / −3**.
- **À droite** : **Vne** (vitesse à ne jamais dépasser).
- Le **coin** en haut à gauche (rencontre décrochage / g max) = la corner speed.

## Vitesses caractéristiques

(Repères présents dans les sims, souvent codées couleur sur l'anémomètre.)

- **Vso** : décrochage en configuration atterrissage (volets/train sortis). **Vs1** : décrochage lisse.
- **Vfe** : vitesse max volets sortis. **Vle/Vlo** : train sorti / en manœuvre.
- **Vno** : vitesse max en croisière normale (au-delà = arc jaune, air calme uniquement). **Vne** : jamais dépasser.
- **Va** : manœuvre. **Vx/Vy** : pente / taux de montée max. **Vr** : rotation au décollage. **Vref/Vapp** : vitesse d'approche (souvent ~1,3 Vso).

## Gestion de l'énergie

L'avion est un réservoir d'énergie : **cinétique** (`½mV²`, la vitesse) + **potentielle** (`mgh`, l'altitude).

- **Énergie spécifique** : `Es = h + V²/(2g)` (en mètres d'« altitude équivalente »). On peut **échanger** vitesse et altitude sans moteur (ressource : monter en perdant de la vitesse ; piquer : accélérer en perdant de l'altitude).
- **Puissance spécifique excédentaire** : `Ps = V·(T − D) / W` (m/s). C'est le taux auquel on peut **gagner de l'énergie totale**. `Ps > 0` : on peut monter *et/ou* accélérer ; `Ps = 0` : virage soutenu maximal (traction = traînée à ce g) ; `Ps < 0` : on saigne de l'énergie.
- **Virage instantané** (un coup, limité par CLmax/structure, corner speed) vs **virage soutenu** (tenu dans le temps, limité par Ps = 0). Un chasseur peut virer très serré une fois puis, s'il n'a pas la poussée, chute d'énergie et ne tient pas le taux.
- **Conséquence combat sim** : « energy fighting » (boom & zoom : garder de l'énergie haute, plonger, remonter) vs « angle fighting » (turn & burn : dépenser l'énergie pour le pointage). Un avion à forte poussée/faible traînée soutient mieux ses virages ; un avion lourd et propre garde bien son énergie en piqué.
