# Conventions de nommage — `name` et `shortName`

Ces règles s'appliquent à **toute** unité créée ou modifiée dans un ORBAT (Tâche 4,
et toute réécriture de noms existants). Établies suite à la construction de l'ORBAT
France 1980.

## Règle 1 — Jamais de parenthèses dans `name`

Aucune parenthèse dans le nom d'une unité, quelle que soit la raison :

- **Contexte de parenté** (le cas le plus fréquent en génération programmatique,
  ex. `"1er Régiment Blindé (1ère Division Blindée)"`) → **ne pas l'ajouter**. La
  position de l'unité dans l'arbre (`subUnits`) porte déjà ce contexte ; le répéter
  dans chaque nom alourdit la lecture sans ajouter d'information récupérable
  autrement. C'est aussi le style des documents sources eux-mêmes (les TO&E ne
  nomment généralement pas leurs sous-unités de façon unique — « Armoured
  Regiment » revient identique dans toutes les divisions).
- **Garnison / localisation** → utiliser un tiret cadratin dans le nom si utile
  (`"1ère Division Blindée — Allemagne de l'Ouest"`), jamais des parenthèses.
- **Précision d'équipement, incertitude de source, note méthodologique** → dans le
  champ `description` de l'unité, jamais dans `name`.

Des noms identiques entre unités-sœurs de branches différentes sont acceptables et
normaux (ex. chaque division a son "1er Régiment Blindé") : le contexte vient de la
position dans l'arbre, pas du texte du nom.

## Règle 2 — Toujours renseigner un `shortName`

Chaque unité doit porter un `shortName` cohérent avec son `name`, dérivé par
**abréviation du rôle** (pas une troncature arbitraire du texte). Conserver dans le
`shortName` :
- les numéros d'ordre (1er/2e/1ère/3e…) ;
- une garnison éventuelle (même séparateur " — ") ;
- toute note conservée intentionnellement entre parenthèses dans un cas
  exceptionnel et justifié (très rare, cf. Règle 1).

Des `shortName` identiques entre unités-sœurs de branches différentes sont
acceptables, pour la même raison qu'en Règle 1.

### Table d'abréviation (français, réutilisable d'un ORBAT à l'autre)

**Échelons / formations**
| Terme | Abrégé |
|---|---|
| Armée | Armée |
| Corps (d'Armée) | Corps |
| Division Blindée | DB |
| Division d'Infanterie | DI |
| Division d'Infanterie de Marine | DIMa |
| Division Parachutiste | DP |
| Division Alpine | DA |
| Brigade | Bde |
| Régiment | R (préfixe/suffixe du rôle, ex. RI, RA, RB) |
| Bataillon | B (idem, ex. BCA) |
| Compagnie | C (idem, ex. CGB, CIM) |
| Escadron | Esc / E (idem, ex. ER) |
| Batterie | B / Bat (idem, ex. BArt, BSAM) |
| Peloton | P (idem, ex. PR, PAA) |
| Groupe | G (idem, ex. GH, GLE) |
| Groupement | G (idem) |

**Rôles / spécialités (à combiner avec l'échelon)**
| Terme | Abrégé |
|---|---|
| Blindé(e) | B |
| Mécanisé(e) | M |
| Infanterie | I |
| Génie | G |
| Artillerie | A |
| Artillerie Automotrice | AA (⚠ collision possible avec Antiaérien — désambiguïser par contexte, ex. `RAA` artillerie auto vs `BAA` batterie antiaérienne) |
| Antichar | AC |
| Antiaérien | AA |
| Reconnaissance | R / Rec |
| Parachutiste | P |
| Marine | Ma |
| Réserve | Res |
| Hélicoptères | H |
| Légion Étrangère | LE (ex. régiment → REI) |

Pour un nouveau terme non couvert par la table, appliquer le même principe :
première(s) lettre(s) significative(s) du mot, en évitant toute collision évidente
avec un sigle déjà utilisé ailleurs dans le même ORBAT.

## Règle 3 — Indicateur de TOE vide (symbole `Ø`)

Établie sur l'ORBAT « Altis Forces Rearmed » (juillet 2026). Quand une unité **et
tout son sous-arbre** ne portent ni `equipment` ni `personnel` nulle part (TOE non
détaillé par la source), on l'indique en suffixant `name` **et** `shortName` avec
`" Ø"` (espace + Ø, U+00D8 — choisi pour sa lisibilité universelle : Latin-1/UTF-8,
sans risque d'affichage contrairement à `∅` U+2205, et sans ambiguïté contrairement
à `0` ou des mots comme `(vide)`/`[VIDE]`).

**Condition stricte : le sous-arbre ENTIER doit être vide, pas seulement l'unité
elle-même.** Une compagnie sans equipment/personnel propre mais dont au moins une
sous-unité (peloton, section...) porte du contenu n'est **pas** marquée — seules
les sous-unités réellement vides le sont, individuellement. Concrètement : calcul
récursif post-ordre (voir `orbat_lib.mark_empty_subtrees`), une unité est marquée
seulement si elle n'a rien en propre ET que 100% de ses enfants (récursivement)
sont eux-mêmes marqués vides.

Exemple (Altis Forces Rearmed) : `Signals Company`, `Engineer Company` et
`Service Support Company` sont des feuilles sans composition détaillée dans le
PDF source → marquées `Signals CIE Ø` / `Sig CIE Ø` etc. La `Pathfinder Company`,
sœur de ces trois-là dans la même HQ Bn, n'est pas marquée (elle a du contenu) —
et sa présence empêche aussi le parent (HQ Bn) d'être marqué.

À utiliser en toute fin de construction (Tâche 4), après le nommage, juste avant
`validate.py` : `orbat_lib.mark_empty_subtrees(orbat)`.

## Règle 4 — Traduire les mots d'échelon d'une source anglaise vers `/nomenclature-v4`

Établie sur l'ORBAT « Altis Forces Rearmed » (source PDF en anglais, convention
britannique/OTAN). Quand Florian demande d'aligner les noms sur son système
`/nomenclature-v4` plutôt que de garder les abréviations anglo-saxonnes brutes du
document source, remplacer par mot entier (regex `\b...\b`, sur `name` **et**
`shortName`, pas seulement `shortName`) en s'appuyant sur la table Échelons de
`nomenclature-v4/references/groupements.md` :

| Mot source (EN) + forme déjà abrégée | Acronyme `/nomenclature-v4` |
|---|---|
| `Battalion` / `Bn` | `BN` |
| `Company` / `Coy` | `CIE` |
| `Platoon` / `Plt` | `PLT` |
| `Troop` / `Tp` (même échelon que Platoon ici) | `PLT` |
| `Section` / `Sect` | `SQ` — ⚠️ **uniquement si l'échelon réel est escouade** (voir piège ci-dessous) |
| `Detachment` / `Det` | `DET` |
| `Battery` / `Bty` | `BTE` |

Fonction prête à l'emploi : `orbat_lib.apply_word_substitutions(orbat,
orbat_lib.ECHELON_WORD_SUBST_EN_TO_NOMV4)`. À exécuter **avant**
`mark_empty_subtrees` (Règle 3), pour que le tag `Ø` s'accroche aux noms déjà
convertis.

**⚠️ Piège FR/EN sur « Section » (déjà signalé dans `sidc.md`) :** en anglais/
Commonwealth, une « Section » d'infanterie est un échelon **escouade** (~8-10 pax,
`échelon=12`), alors que la « Section » `/nomenclature-v4` (`SEC`) désigne
l'échelon **peloton** (`échelon=14`, comme `PLT`). Ne jamais convertir
mécaniquement `Section`→`SEC` sans vérifier l'échelon réel de l'unité : dans ce
cas précis, la bonne cible est `SQ` (Escouade), pas `SEC`.

**Hors périmètre par défaut :** `Team`, `Pair`, `Group`, `Crew` (échelon équipe)
n'ont pas d'entrée dédiée univoque dans la table `/nomenclature-v4` (seul
`Équipe`→`EQP`/`TE` s'en approche, avec risque de collision `TE`=Tireur Élite).
Par défaut on les laisse tels quels (`Assault Team`, `MFC Pair`...) — à convertir
en `EQP` seulement si Florian le demande explicitement.

**Cas des sigles déjà établis par la source :** si le document source utilise
lui-même une abréviation officielle et reconnaissable pour une unité précise
(ex. `HHC` = *Headquarters and Headquarters Company*, repris tel quel dans
l'appendix graphique), la garder verbatim en `shortName` plutôt que de la
décomposer mécaniquement. Pour le `name` long en revanche, préférer une forme
plus explicite basée sur les acronymes `/nomenclature-v4` plutôt que le sigle brut
si celui-ci reste peu parlant hors contexte (ex. `name: "HQ Cies"` /
`shortName: "HHC"`, plutôt que `name: "HHC"` littéral).

## Implémentation type

Pour une génération programmatique (Python), dériver `shortName` en une passe
finale sur l'arbre entier plutôt qu'en argument séparé à chaque appel de
`make_unit` : une liste ordonnée de règles `(motif du nom complet → abrégé)`,
appliquée du motif le plus spécifique au plus générique, avec extraction/
réinjection préalable d'un éventuel suffixe " — garnison". Voir l'exemple
`make_shortname()` / `apply_shortnames()` développé pour l'ORBAT France 1980
(script `build_france_1980.py` et bibliothèque `templates_1980.py` de Florian).
