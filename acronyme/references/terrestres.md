# Véhicules Terrestres & Hélicoptères

Format : `{Type}-{Gabarit} {Rôle1}-{Rôle2}` ou `{Type}.{Gabarit}-{Rôle1}.{Rôle2}`

---

## Types — Véhicules terrestres

| Acronyme | Signification | Description |
|----------|--------------|-------------|
| Tk | Tankette | Blindé très léger, mitrailleuse |
| T | Tank | Véhicule chenillé et blindé |
| TL / TM / TH / TSH | Tank L/M/H/SH | Variantes par gabarit |
| TV | Tank à roue | Char léger à roues |
| VL | Voiture légère | Non blindée ou très peu |
| VM | Voiture moyenne | |
| VU | Véhicule utilitaire | Camion (légèrement blindé) |
| VUL | Véhicule utilitaire léger | Petit camion |
| VB | Véhicule chenillé | Standard, gabarit correspondant à `V` (voir grammaire ci-dessous) |
| VH | Véhicule semi-chenillé | Half-track |
| VC | Véhicule de cavalerie | Très mobile, correctement armé |
| TCI | Char combat d'infanterie | Lourd/lent, soutien rapproché |
| MBT | Main Battle Tank | Protection + puissance + mobilité |
| C | Cheval | Véhicule rapide / reconnaissance |
| VA / TA | Voiture/Tank amphibie | Capable de traverser des plans d'eau |
| SP | Automoteur | Blindé sans tourelle (AT ou artillerie) |
| VSP | Voiture automoteur | Voiture sans tourelle |
| ST | Position armes fixes | Trépied, déplaçable |
| FIX | Armes fixes | Permanent (bunker, vissé) |
| REM | Remorque | |
| CT | Citerne | |
| RCT | Citerne remorquée | |
| WM | Moto | Wheeled Motorbike |
| WMS | Moto avec sidecar | |
| WB | Vélo | |
| TRN | Train | |
| RV | Rover | Piloté/automate, scientifique/exploration |
| CAV | Cavalerie (Type) | ⚠️ Désambiguïser par position vs rôle CAV |

### Grammaire compositionnelle `V`

Le préfixe `V` se compose selon : **`V` + `{Locomotion}` + `{Gabarit}` + `{Rôle}`**, avec un suffixe `.H`/`.SH` séparé pour le gabarit lourd/super-lourd (voir plus bas).

**`{Locomotion}`** (facultatif, un seul des choix suivants) :

| Marqueur | Sens |
|---|---|
| *(absent)* | Roues, nombre non précisé |
| `#` (chiffre) | Roues, nombre précisé — ex. `V6`, `V8` |
| `H` | Semi-chenillé |
| `B` | Chenillé |

**`{Gabarit}`** (facultatif) : *(absent)* = standard · `L` = léger · `M` = moyen. **Le lourd/super-lourd ne s'infixe jamais** — toujours en suffixe `.H` / `.SH` en fin d'acronyme (voir "Règle du suffixe `.H`" ci-dessous), y compris sur `VB`/`VH` où l'infixe créerait une confusion (`VBH`, `VHH`).

**`{Rôle}`** (facultatif) : `TT`, `CI`, etc. — voir "Acronymes combinés" ci-dessous, la logique reste identique.

> ⚠️ **Locomotion et blindage sont indépendants.** Ni le nombre de roues, ni `H`/`B` n'impliquent un niveau de protection. Un véhicule chenillé n'est pas *de facto* mieux (ou moins bien) blindé qu'un véhicule à roues — le blindage se juge au cas par cas, jamais déduit du Type.

> **Note — divergence assumée avec les désignations réelles.** Ce système est un idiolecte, pas une réplique des noms officiels. Ex. : le vrai VBCI français (Nexter) est un 8×8 à roues ; dans ce système, `B` = chenillé, donc le vrai VBCI se note `VCI` ou `V8CI`, et l'acronyme `VBCI` désigne ici un véhicule chenillé (ex. AMX-10P). Idem pour le VBL (Panhard, léger à roues) → `VL` ou `V4L` dans ce système. **Ne pas confondre le nom réel d'un véhicule avec son acronyme dans ce système.**

**Exemples :**
| Acronyme | Lecture |
|---|---|
| `VL` | Léger, roues (nombre non précisé) |
| `V4L` | Léger, 4 roues |
| `V8CI` | 8 roues, combat d'infanterie (≈ vrai VBCI Nexter) |
| `VBLTT` | Chenillé, léger, transport de troupes |
| `VHMCI` | Semi-chenillé, moyen, combat d'infanterie |
| `VBTT.H` | Chenillé, lourd, transport de troupes |
| `VCI.H` | Roues (non précisé), lourd, combat d'infanterie |

---

## Acronymes combinés (fusions prédéfinies)

| Acronyme | Décomposition | Description |
|----------|--------------|-------------|
| VTT / VLTT / VMTT / VTT.H | V(+L/M/.H) + TT | Transport de troupes, roues — gabarit optionnel. Alias reconnus : `IMV` = `VLTT`, `MRAP` = `VMTT` (protection anti-mine/anti-embuscade ; peut aussi s'écrire sous les variantes chenillées/semi-chenillées, ex. `VBMTT`, `VHMTT`, selon le châssis réel) |
| VBTT / VBLTT / VBMTT / VBTT.H | VB(+L/M/.H) + TT | Transport de troupes, chenillé — gabarit optionnel |
| VHTT / VHLTT / VHMTT / VHTT.H | VH(+L/M/.H) + TT | Transport de troupes, semi-chenillé — gabarit optionnel |
| VCI / VLCI / VMCI / VCI.H | V(+L/M/.H) + CI | Combat d'infanterie, roues — gabarit optionnel |
| VBCI / VBLCI / VBMCI / VBCI.H | VB(+L/M/.H) + CI | Combat d'infanterie, chenillé — gabarit optionnel |
| VHCI / VHLCI / VHMCI / VHCI.H | VH(+L/M/.H) + CI | Combat d'infanterie, semi-chenillé — gabarit optionnel |
| TCI / TLCI / TMCI / THCI | T/TL/TM/TH + CI | Char de combat d'infanterie (pas de transport) |
| TVCI | TV + CI | Tank à roues de combat d'infanterie |
| VUB | VU + B | Camion chenillé |
| STIG / IG | ST + IG | Canon infanterie statique |
| STAA / AA | ST + AA | Canon AA statique |
| START / ART | ST + ART | Canon artillerie statique |
| STMG / MG | ST + MG | Mitrailleuse statique |
| STC | ST + C | Canon statique moderne en position fixe |
| STG | ST + G | Obusier statique |
| SPHE | SP + HE | Canon HE automoteur *(⚠️ chevauchement possible avec `SPG` — à clarifier si besoin : SPHE = obus HE générique, SPG = obusier dédié tir indirect)* |
| TAT / TLAT / TMAT / THAT | T/TL/TM/TH + AT | **Char anti-char.** Reste sémantiquement un char (blindage tous azimuts, MG coaxiale/annexes, mobilité, va au contact) — l'armement est simplement orienté anti-char plutôt que HE générique. *Ex. : Sherman 76, Sherman SA50.* |
| SPAT | SP + AT | **Canon anti-char automoteur.** Armement en casemate (pas de tourelle rotative), blindage souvent privilégié à l'avant. Évite le contact et les grandes manœuvres ; rôle = tenir une position, bloquer un axe, embuscade. *Ex. : Jagdpanzer, Jagdtiger, ASU-57/85.* |
| SPG | SP + G | **Obusier/canon d'assaut automoteur — soutien-feu DIRECT.** Armement = obusier employé en appui rapproché direct, pas en tir indirect longue portée. *Ex. : StuH, SU-152, M44.* **⚠️ Exclut le rôle `ART` (voir SKILL.md) : pour du tir indirect longue portée, utiliser `SP-ART`/`SPART`.** *Ex. de notation : M44 = `SPG-C155/MG`.* |
| SPC | SP + C | **Canon automoteur générique.** Ni exclusivement AT ni exclusivement HE. *Ex. : StuG.* Frontière SPAT/SPC parfois floue et subjective — **le rôle voulu prévaut** : un canon automoteur employé en rôle anti-char se classe `SPAT` même si l'armement paraît « faiblard » pour ce rôle. |
| SPART / SPART.L/M/H | SP + ART | Artillerie automotrice (obusier/canon d'artillerie, tir indirect longue portée). Pas de confusion réelle avec SPAT malgré la ressemblance orthographique. *Ex. : Hummel.* |
| **TD** / **TDL / TDM / TDH** *(nouveau)* | Tank Destroyer (+ gabarit optionnel L/M/H) | **Catégorie générique** regroupant tout véhicule spécifiquement conçu et employé pour détruire des chars, qu'il ait une tourelle ou non. Un `SPAT` est toujours un `TD`, mais un `TD` n'est pas forcément un `SPAT` — ex. le M10 : tourelle rotative, "comme un char", mais blindage réduit et rotation de tourelle lente le rendent inadapté au combat blindé intense ; son rôle reste similaire à un SPAT. À utiliser pour les cas qui ne rentrent proprement ni dans `TAT` (pas assez "char" : blindage/mobilité insuffisants pour aller au contact) ni dans `SPAT` (a une tourelle). Le gabarit `L/M/H` est optionnel, à ajouter seulement si la distinction de poids importe dans le contexte. **⚠️ Rôle `AT` implicite : ne pas écrire `TD-AT`.** *Ex. de notation : M10 = `TD-C90/MG`.* |
| VTL / VTM / VTH | VT + L/M/H | VTOL L/M/H |

---

## Hélicoptères

| Acronyme | Décomposition | Description |
|----------|--------------|-------------|
| CH | Chopper | Hélicoptère générique |
| CHG | CH + G | Gunship (AH-64 type) |
| CHTT | CH + TT | Transport de troupes |
| CHATT | CH + ATT | Hélico d'attaque |
| CHSAN / CHMED | CH + SAN/MED | Évacuation sanitaire |

*Les hélicoptères peuvent utiliser des rôles aériens.*

---

## SF / Warhammer

| Acronyme | Description |
|----------|-------------|
| MK# / MKL/M/H | Marcheur/Mecha (# pattes) |
| TTN | Titan |
| VG | Véhicule antigrav |
| TG | Char antigrav |

---

## Médiéval

| Acronyme | Description |
|----------|-------------|
| BST | Baliste |
| CAP | Catapulte |
| TBC | Trébuchet |
| BLR | Bélier |
| TDS | Tour de siège |

---

## Pré-industriel (XVIIe–XIXe siècle)

Couvre la période allant de la poudre noire jusqu'à l'aube de l'industrialisation militaire. Ces types peuvent apparaître ponctuellement dans d'autres époques.

| Acronyme | Signification | Description |
|----------|--------------|-------------|
| CN | Canon napoléonien / pré-industriel | Canon à âme lisse ou rayée de la période pré-industrielle. Semi-statique par nature. Notation : `CN.L/M/H` (gabarit) ou `CN.#` (calibre en mm ou livres) |

> `CN` remplace l'ancien raccourci `STC/CN`. `STC` reste l'acronyme pour un canon statique moderne en position fixe.

---

## Rôles terrestres

| Acronyme | Signification | Description |
|----------|--------------|-------------|
| HE | High Explosives | Destruction d'objectifs non blindés |
| AA | Anti-aérien | |
| AAGM / AACA / AAC | AA Missile / Canon Auto / Canon | |
| ART | Artillerie | Bombardements longue portée |
| RART | Artillerie lance-roquette | |
| Cmdt / HQ | Commandement | Centre mobile, radio |
| TR / TT | Transport / Transport de troupes | Non blindé |
| TRK | Tracteur / remorquage | |
| TRM / TRML / TRMH | Transport munitions L/M/H | |
| MUN / MUNL / MUNM / MUNH | Munitions L/M/H | |
| TRF / TRW | Transport carburant / eau | |
| TRV | Transport de véhicule | |
| REC / TA | Reconnaissance / Observation artillerie | |
| ENG | Ingénieur | |
| MEDEVAC / SAN | Médical / Sanitaire | |
| SIG | Signal / Transmission | Équipé radio |
| EW | Guerre électronique | |
| MAIN | Maintenance | |
| LOG / SPT | Logistique / Support | |
| F / FUEL | Carburant | |
| W | Eau | |
| CHEM | Produits chimiques / inflammables | |
| CT | Citerne et transport de fluide | |
| CTF / CTW / CTC | Citerne carburant / eau / chimique | |
| MLRS | Lance-roquettes multiple | M270 type |
| TTNK | Armes tueuses de titans | |
| NBC | Protection NBC | |
| CI | Combat d'infanterie | Soutien rapproché |
| BDZ | Bulldozer | |
| ML / MS | Poseur de mine / Démineur | |
| SD | Furtif (silence/discrétion) | ⚠️ Distinct de STH |
| STH | Stealth | Furtivité visuelle/radar ⚠️ Distinct de SD |
| ATT | Attaque / Assaut | Rupture de position |
| DEF | Défense | Tenue de position |
| MNV | Maneuvre | Spécialisé maniabilité, esquive, agilité |
| BRH | Breacher | Rupture de défense/obstacle/front |
| UAV | Drone | |
| NV | Nocturne | Vision nocturne (rôle) ⚠️ NVG = équipement spécifique (jumelles) |

---

## Armement terrestre

| Acronyme | Signification | Notes |
|----------|--------------|-------|
| C / G | Canon / Obusier (LC/MC/HC = Léger/Moyen/Lourd) | Rechargé **obus par obus** après chaque tir (voir note C vs CA) |
| R / RKT | Roquette non guidée | |
| MG | Mitrailleuse | |
| AT | Anti-tank / chasseur de char | |
| GMG / GL | Grenade Machine Gun / Lance-grenade | |
| CA / LCA / MCA / HCA | Canon automatique L/M/H | Alimentation par **magasin/bande** + tir auto/rafale (voir note C vs CA) |
| CAA / LCAA / MCAA / HCAA | Canon automatique Anti-Aérien L/M/H | Fusion CA + AA par gabarit |
| LM | Lance-missile générique | |
| IG | Canon infanterie | |
| HWZ / G | Obusier | |
| MOR / LMOR / MMOR / HMOR | Mortier L/M/H | |

> **Convention MCA.AA vs MCAA :** `MCA.AA` note un canon auto moyen en *rôle AA circonstanciel*. `MCAA` est la fusion prédéfinie pour un usage AA permanent. Même logique pour LCAA et HCAA.

> **`C` vs `CA` — critère mécanique, pas de calibre :**
> - **`CA`** (canon automatique) = alimentation par **magasin ou bande** + capacité de **tir automatique / rafale** (ex. tourelle 20mm d'un VBCI, canon d'un CV90).
> - **`C`** (canon) = pièce rechargée **obus par obus après chaque tir**, y compris avec une **aide au chargement / autoloader** (ex. Leclerc, M10, canon de 90mm d'un EBR). Un chargeur automatique n'en fait **pas** un `CA` : il faut toujours engager un nouvel obus dans la culasse entre deux tirs.
> - La distinction est **mécanique** (mode d'alimentation), indépendante du calibre.

> **Convention calibre (préférée au gabarit) :** quand le calibre est connu, l'ajouter directement en suffixe plutôt que d'utiliser `L/M/H` : `C90` (canon 90mm), `CA20` (canon auto 20mm), `C105`, `C155`. Le gabarit `L/M/H` reste le repli quand le calibre est inconnu ou non pertinent. Exemples : `TD-C90/MG`, `VBCI-CA20/MG`, `SPG-C155/MG`.
