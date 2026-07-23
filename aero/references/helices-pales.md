# Référence — Hélices et pales

Le comportement des pales : géométrie, pas, angle d'incidence local, rendement, types d'hélices, effets secondaires. **Cœur de la demande de Florian.** Une hélice est une **aile en rotation** : chaque section de pale est un profil qui produit une portance (→ la traction) et une traînée (→ le couple à vaincre).

## Sommaire
- La pale comme profil tournant
- Angle de calage, angle d'avance, angle d'incidence local
- Pas géométrique, pas effectif, glissement
- Le vrillage et pourquoi il existe
- Paramètre d'avancement J et rendement propulsif
- Pas fixe vs pas variable vs vitesse constante
- Drapeau, inversion, moulinet
- Effets secondaires : couple, souffle, facteur P, gyroscopie
- Les tendances au lacet (résumé pilotage)
- Mach en bout de pale
- Moteur critique (bimoteur)

## La pale comme profil tournant

Chaque section de pale voit un **vent relatif résultant**, somme vectorielle de :
- la **vitesse de rotation** `U = ω·r = 2π·n·r` (n en tours/s, r rayon de la section) — tangentielle, dans le plan de rotation ;
- la **vitesse d'avancement** `V` de l'avion — perpendiculaire au plan de rotation.

La section produit une portance ⊥ à ce vent résultant. Sa **composante vers l'avant** = **traction** ; sa **composante dans le plan de rotation** (traînée + projection) = ce que le moteur doit vaincre (**couple**).

## Angle de calage, angle d'avance, angle d'incidence local

Trois angles à ne jamais confondre, à un rayon r donné :

- **Angle de calage β** (blade angle / pitch angle) : angle entre la **corde de la pale** et le **plan de rotation**. C'est la géométrie de la pale (fixe si pas fixe, réglable si pas variable).
- **Angle d'avance φ** (helix / advance angle) : angle du **vent résultant** par rapport au plan de rotation. `φ = arctan( V / (2π·n·r) ) = arctan( V / U )`. Il dépend de la vitesse avion et de la rotation.
- **Angle d'incidence local de la pale α = β − φ.** C'est *lui* qui commande la portance de la section (comme l'incidence d'une aile). Exactement analogue à l'angle d'attaque d'une aile.

**Comportement clé** (à maîtriser pour le pilotage) :
- **V augmente à n fixe** → φ augmente → **α diminue** → traction diminue. Assez vite, `α → 0` (plus de traction), puis **α < 0** → la pale freine et entraîne le moteur (**moulinet**, forte traînée). C'est pourquoi une hélice à pas fixe « cale » en vitesse : elle atteint son angle d'avance maximal utile.
- **n augmente à V fixe** → U augmente → φ diminue → **α augmente** → plus de traction, mais aussi **plus de couple** et **Mach en bout de pale** qui monte.
- **α trop grand** (avion lent, plein régime, forte charge) → la pale **décroche** localement (surtout vers le pied) → perte de rendement, vibrations.

## Pas géométrique, pas effectif, glissement

- **Pas géométrique** : distance dont l'hélice avancerait en un tour **si elle se vissait dans un solide** sans glisser : `pas géo = 2π·r·tan β` (référencé en général à **0,75 R**).
- **Pas effectif** : distance **réellement** avancée en un tour = `V / n`.
- **Glissement** = pas géométrique − pas effectif. Il est **normal et nécessaire** : sans glissement, α = 0 et la pale ne produirait aucune traction. Le glissement est ce qui donne à la section son incidence utile.

## Le vrillage et pourquoi il existe

Une pale est **vrillée** : calage β **fort au pied**, **faible en bout**. Raison :

- La vitesse de rotation `U = ω·r` **croît avec le rayon** : le bout va bien plus vite que le pied. Donc l'angle d'avance `φ = arctan(V/U)` est **grand au pied** (U petit) et **petit en bout** (U grand).
- Pour garder un **angle d'incidence α ≈ constant et optimal sur toute l'envergure** (et un pas effectif cohérent), il faut que β **suive φ** : donc β diminue du pied vers le bout.
- Sans vrillage, α serait énorme au pied (décrochage) et quasi nul en bout (aucune traction) — l'hélice serait inefficace. **Le vrillage égalise le travail de la pale sur toute sa longueur.**

## Paramètre d'avancement J et rendement propulsif

- **Paramètre d'avancement** : `J = V / (n·D)` (n tours/s, D diamètre). Sans dimension. Il résume « à quelle vitesse l'avion avance par rapport à la rotation ». J petit = avion lent / hélice qui tourne vite ; J grand = avion rapide / hélice lente.
- Traction et puissance : `T = CT·ρ·n²·D⁴`, `P = CP·ρ·n³·D⁵`, où **CT et CP dépendent de J et du calage**.
- **Rendement propulsif** : `η = (T·V) / P = J·CT / CP`. C'est la fraction de la puissance moteur convertie en puissance propulsive utile.
- **Courbe de rendement** : pour un calage donné, η **monte avec J**, passe par un **maximum** (souvent η ≈ 0,80–0,88 pour une bonne hélice) au point de fonctionnement optimal, puis **chute** (à J trop grand, α → 0, plus de traction ; à J trop petit, la pale décroche/brasse). **Une hélice à pas fixe n'est optimale qu'à un seul J** — donc une seule combinaison vitesse/régime.

## Pas fixe vs pas variable vs vitesse constante

- **Pas fixe** : calage figé. Simple, léger, pas cher. Compromis obligatoire :
  - **hélice « de montée » (petit pas / fine)** : bon α à basse vitesse → bonne traction au décollage/montée, mais le régime **s'emballe** et l'efficacité s'effondre à haute vitesse (l'avion « bute »).
  - **hélice « de croisière » (grand pas / calée)** : efficace vite, mais **médiocre au décollage** (α faible à basse vitesse, régime qui monte mal, distance de décollage allongée).
- **Pas variable** : le pilote change le calage en vol (petit pas pour décoller/monter, grand pas pour croiser). Élargit la plage efficace.
- **Vitesse constante (à régulateur / constant-speed)** : un **régulateur** ajuste **automatiquement** le calage pour **maintenir un régime sélectionné**, quelles que soient la vitesse et la puissance. C'est l'équivalent d'une **boîte de vitesses** : la pale reste toujours à un α efficace sur toute la plage.
  - **Petit pas (fine) = calage faible = régime élevé** → décollage/montée (pleine puissance, hélice qui « mord » à basse vitesse).
  - **Grand pas (coarse) = calage fort = régime bas** → croisière (rendement max, moteur qui souffle sans s'user).
  - **Deux commandes séparées** : la **manette des gaz** règle la **pression d'admission** (la puissance), la **manette d'hélice** règle le **régime** (via le calage). Règle usuelle de gestion : réduire d'abord la pression d'admission puis le régime en descente de puissance ; l'inverse en montée de puissance (éviter « fort régime sur faible admission » prolongé).
  - **Conséquence sim** : sur un warbird ou un avion complexe (P-51, Spitfire, Bf 109, DC-3, Bonanza…), mal gérer pas/régime → surrégime au décollage, perte de traction, ou moteur maltraité. Décollage = plein petit pas (régime max), croisière = grand pas.

## Drapeau, inversion, moulinet

- **Moulinet (windmilling)** : moteur coupé, l'hélice est **entraînée par le vent relatif** (α négatif) et crée une **énorme traînée** (pire qu'une hélice arrêtée). À éviter sur panne.
- **Mise en drapeau (feathering)** : sur bimoteur, orienter les pales à **~90°** (tranche dans le vent, α ≈ 0) pour **annuler la traînée** de l'hélice du moteur en panne → conserve du contrôle et des performances. Indispensable à la sécurité multimoteur.
- **Inversion de pas (reverse)** : calage **négatif** pour produire une **traction arrière** → freinage au sol après atterrissage (turbopropulseurs, gros avions). En sim de brousse/transport, très utile pour les pistes courtes.

## Effets secondaires — les quatre tendances

Une hélice tournante induit des effets qui, sur un avion à hélice unique, **se combinent** et perturbent surtout au **décollage / forte puissance / basse vitesse**. Convention ci-dessous : **hélice tournant à droite (sens horaire vu du poste)** — convention américaine. Pour une hélice tournant à gauche (beaucoup d'appareils britanniques/soviétiques : Spitfire, Yak…), **tous les effets s'inversent**.

1. **Couple de renversement (torque)** : le moteur fait tourner l'hélice dans un sens → réaction qui **roule l'avion dans l'autre**. Hélice horaire → tendance à **rouler à gauche**. Maxi à forte puissance/basse vitesse. Compensé par un peu d'aileron / calage d'aile.
2. **Souffle hélicoïdal (spiraling slipstream)** : le flux d'hélice s'enroule en spirale autour du fuselage et vient **frapper un côté de la dérive** → **lacet** (à gauche pour une hélice horaire à forte puissance/basse vitesse). Compensé par offset de dérive, calage moteur, et palonnier.
3. **Facteur P (P-factor)** : à **forte incidence** (nez haut, montée, décollage train classique queue basse), la **pale descendante** (d'un côté) attaque avec un **α plus grand** que la pale montante → **traction dissymétrique** → lacet. Hélice horaire : pale descendante à droite → **lacet à gauche**. Nul en palier (incidence faible), fort en montée cabrée.
4. **Effet gyroscopique / précession** : l'hélice est un **gyroscope**. Une action en tangage ou lacet produit une réaction **décalée de 90°** dans le sens de rotation. Cas classique du **train classique (taildragger)** : lever la queue au décollage (action à piquer) → **précession en lacet** (à gauche pour une hélice horaire). Aussi sensible dans les manœuvres vives (tonneaux, ressources).

## Les tendances au lacet — résumé pilotage

Pour une hélice **horaire** (US), les quatre effets poussent majoritairement **à gauche** au décollage et en montée pleine puissance → il faut du **pied à droite** (right rudder) pour tenir l'axe. Pour une hélice **anti-horaire** (Spitfire, Yak, la plupart des monomoteurs européens/soviétiques), c'est **pied à gauche**.

- Le besoin de pied **augmente** avec la puissance et l'incidence, et **diminue** en croisière rapide (incidence faible, souffle atténué).
- **Conséquence sim** : un décollage qui part inexorablement sur un côté malgré ailerons neutres = tendances moteur non compensées → mettre du **pied du bon côté** proportionnellement à la puissance, dès la mise en puissance, et relâcher en accélérant. Sur les gros warbirds, monter la puissance **progressivement** pour ne pas être débordé.

## Mach en bout de pale

- La vitesse réelle du **bout de pale** = `√( (ω·R)² + V² )` (rotation + avancement). À fort régime, elle peut **approcher ou dépasser Mach 1** avant que l'avion ne soit rapide.
- Conséquences : **chute de rendement** (ondes de choc locales), **bruit** intense, **contraintes structurales**. C'est ce qui **limite le diamètre et le régime** des hélices.
- Parades : **réducteur** (le moteur tourne vite, l'hélice lentement), **pales multiples et larges** (encaisser la puissance sans allonger le rayon), profils fins, bouts en flèche. D'où les grosses hélices tri/quadripales des avions puissants.

## Moteur critique (bimoteur)

Sur un bimoteur dont les **deux hélices tournent dans le même sens**, la panne d'un moteur est **plus grave que l'autre** : c'est le **moteur critique**. À cause du facteur P, la ligne de traction effective de chaque moteur n'est pas centrée sur sa nacelle ; la panne du moteur dont la traction est la **plus déportée** crée le plus fort moment de lacet à contrer (contrôlabilité minimale, définit la vitesse **Vmc**).

- Les avions à **hélices contrarotatives** (l'une horaire, l'autre anti-horaire) **n'ont pas de moteur critique** : les effets se compensent.
- **Conséquence sim** : sur bimoteur classique, s'entraîner à la panne du moteur critique (le plus défavorable), maintenir Vmc, contrer au pied et mettre en drapeau côté panne.
