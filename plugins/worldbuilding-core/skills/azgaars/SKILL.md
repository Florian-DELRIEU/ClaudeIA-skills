---
name: azgaars
description: Lecture, analyse et édition des sauvegardes .map d'Azgaar's Fantasy Map Generator (FMG). Déclencher IMPÉRATIVEMENT dès que Florian tape /azgaars, fournit un fichier .map, mentionne "Azgaar", "FMG" ou "Fantasy Map Generator", ou demande de lire/résumer/extraire/modifier des données d'une carte générée (états, burgs/villes, cultures, religions, provinces, régiments, diplomatie, populations, rivières, marqueurs, notes, zones/ressources). Déclencher même pour des demandes courtes ("combien d'habitants dans X ?", "liste les états", "renomme cette ville", "extrais les régiments", "c'est quoi la capitale de Y ?"). Peut s'enchaîner avec les skills orbat et nomenclature-v4 (conversion des armées FMG en ORBAT).
---

# Azgaar's Fantasy Map Generator — sauvegardes .map

Outillage pour lire et éditer les fichiers `.map` sans casser leur rechargement dans FMG.

## Règles absolues

1. **Ne JAMAIS parser un .map à la main avec `split('\n')`** : les blocs sont séparés par `\r\n` (CRLF) et le SVG interne utilise `\n`. Ouvrir en **binaire** puis décoder UTF-8. → Toujours passer par `scripts/azgaar_lib.py`.
2. **Deux formats coexistent** — la lib les détecte automatiquement : **39 blocs** (FMG v1.9x–1.11x) et **46 blocs** (v1.13x+, avec module Économie : rebels, ice, goods, markets, trades ; `zones` y est décalé au bloc 45). Les blocs 0-37 sont identiques. Vérifier `m.n_blocks` / `m.has_economy` avant de toucher aux collections économiques. **Ne jamais modifier l'ordre ni le nombre des blocs** — FMG charge par index.
3. **Blocs non confirmés** : dans le format 46, les blocs 40 (`cells_resource`) et 44 (`cells_econ`) sont des déductions non validées via le code source. Ils sont préservés en round-trip mais **ne pas les éditer** sans validation empirique. Le voir dans `reference/format.md`.
4. **Éléments réservés** : élément 0 de cultures/states/burgs/religions/provinces est réservé. Suppression d'une entité = `"removed": true`, jamais retirer l'élément (les `i` doivent rester égaux à l'index).
5. Après édition, **toujours produire un nouveau fichier** dans `/mnt/user-data/outputs/` (jamais écraser l'upload) et rappeler à Florian de vérifier le rechargement dans FMG.
6. Les renommages (burg, état...) exigent aussi le patch du label dans le SVG — la lib le fait via `rename_burg` / `rename_state` / `sync_svg_label`. Pour les éditions qui touchent au rendu (couleurs, frontières, déplacement de villes), prévenir que le SVG pré-rendu peut rester obsolète : lire `reference/format.md` § "rendu SVG vs données".
7. **Régiments** : ne jamais assigner `state["military"] = ...` directement. Toujours passer par `set_state_military()`, qui purge automatiquement le cache SVG figé (`clear_army_svg()`) — sinon la boîte affichée sur la carte garde l'ancien nom/effectif alors que l'éditeur de régiment FMG lit déjà les nouvelles données (bug réel observé : effectifs affichés incohérents entre régiments identiques en JSON).

## Workflow standard

```bash
# 1. Résumé rapide
python3 scripts/map_info.py carte.map                # vue d'ensemble (+ nb blocs, économie si présente)
python3 scripts/map_info.py carte.map --states       # + liste des états
python3 scripts/map_info.py carte.map --burgs 20      # + top villes
python3 scripts/map_info.py carte.map --regiments     # + armées
python3 scripts/map_info.py carte.map --economy       # + biens/marchés (cartes 46 blocs)

# 2. Extraction vers JSON (pour analyse ou conversion ORBAT)
python3 scripts/extract.py carte.map states sortie.json
python3 scripts/extract.py carte.map regiments regiments.json
# collections tous formats : states burgs cultures religions provinces rivers
#     markers routes zones notes features regiments options all
# collections économie (46 blocs) : goods markets trades rebels ice
```

## Édition en Python

```python
import sys; sys.path.insert(0, "scripts")
from azgaar_lib import AzgaarMap

m = AzgaarMap.load("carte.map")

# Lire
m.summary()                       # dict de synthèse (inclut n_blocks + bloc économie si présent)
m.n_blocks                        # 39 ou 46 selon la version
m.states, m.burgs, m.notes, ...   # collections parsées (listes de dicts)
m.options                         # year, era, military[], winds...
m.real_population(b["population"])  # points → habitants (× populationRate)
m.cells("cells_state")            # tableaux par cellule

# Économie (cartes 46 blocs uniquement — tester m.has_economy avant)
if m.has_economy:
    m.goods, m.markets, m.trades, m.rebels, m.ice

# Modifier une collection : éditer l'objet PUIS marquer dirty
m.states[3]["alert"] = 2.0
m.mark_dirty("states")

# Renommages (données + label SVG synchronisés)
m.rename_burg("Kas-Helbrac", "Nouveau Nom")
m.rename_state("Duba", "Duberia")

# Notes (fiches régiments = id "regiment{état}-{i}", marqueurs = "marker{i}")
m.notes.append({"id": "marker999", "name": "Titre", "legend": "Texte <b>html</b>"})
m.mark_dirty("notes")

# Sauvegarder : blocs non modifiés réécrits à l'octet près
m.save("/mnt/user-data/outputs/carte_edit.map")

# Analyses par état
m.burgs_by_state()      # {stateId: burgs triés par pop desc}
m.ports_by_state()      # {stateId: burgs portuaires}
m.market_value_by_state()  # valeur économique (46 blocs)
m.industry_index()      # indice industriel 0..1 (marchés + pop urbaine)

# Refonte militaire (types + armées) — respecte les invariants automatiquement
m.set_military_types([{"icon": "🪖", "name": "infanterie", "rural": 0.2,
                       "urban": 0.15, "crew": 1, "power": 1,
                       "type": "melee", "separate": 0}, ...])
m.set_state_military(state_id, regiments, legends)  # remplace l'armée + sync notes
```

Vérification systématique après édition : recharger le fichier produit avec `AzgaarMap.load()` et re-vérifier `summary()` + re-parse des blocs modifiés.

## Règles de sérialisation

- **Toujours `dumps_fmg()` pour sérialiser un bloc JSON, jamais `json.dumps` direct** : certaines cartes contiennent des surrogates UTF-16 isolés dans les notes (inscriptions corrompues volontaires) que `dumps_fmg` ré-échappe — sinon crash UTF-8 à la sauvegarde (piège documenté dans `reference/format.md`).
- `set_options()` fait une édition chirurgicale du bloc settings (seul le segment JSON est remplacé, les `|` environnants préservés).
- Les icônes de `options.military` peuvent être des data-URI base64 de dizaines de Ko : ne jamais les afficher brutes (tronquer ou remplacer par `[icône image]`).

## Interprétation stratégique (pour d'autres skills, notamment /gm-worlds)

Au-delà de la lecture brute, `azgaar_lib` offre une couche d'interprétation
(puissance militaire, provinces par état, biomes dominants, diplomatie, guerres en
cours, posture/stabilité synthétiques) via `m.strategic_snapshot()` et les méthodes
qu'elle assemble. **/gm-worlds** s'appuie entièrement dessus plutôt que de
réimplémenter sa propre lecture — tout skill qui a besoin de comprendre « où en est
le monde » devrait faire de même. Détail complet dans `reference/format.md` §
"Couche d'interprétation stratégique".

## Régénération d'armées (exemple de workflow)

Pour recréer les armées d'une carte de façon cohérente avec la démographie/industrie :
1. `m.set_military_types(...)` avec un roster adapté à l'époque voulue.
2. Pour chaque état : budget = pop × taux de mobilisation (moduler par `state["alert"]`) ; répartir en formations types (dicts `u`) ; les armes techniques (blindés, aviation, marine) scalées par `m.industry_index()` ; marine seulement si `m.ports_by_state()` a des ports.
3. Placer sur les burgs (`m.burgs_by_state()`, ports pour le naval), `x/y/bx/by` = coordonnées du burg, `cell` = burg["cell"].
4. `m.set_state_military(id, regiments, legends)` par état, puis `m.save(...)`.
Les régiments étant redessinés par FMG au chargement, aucune retouche SVG n'est nécessaire.

## Repères sur les données

- **Population** : toutes les valeurs sont en *points* ; habitants = points × `m.population_rate` (settings, souvent 1000).
- **Régiments** : `states[i].military[]` (`u` = composition par type d'unité, types définis dans `m.options["military"]`). Redessinés par FMG au chargement → édition sûre côté données. Fiche narrative dans `notes`.
- **Diplomatie** : `states[i].diplomacy` = statut envers chaque état ; l'élément 0 (Neutrals) y stocke l'historique des guerres.
- **Rivers/markers/routes/zones** : `i` ≠ index du tableau (tableaux non ordonnés).
- **Année/ère du monde** : `m.options["year"]` / `["era"]`.

## Pour aller plus loin

Lire `reference/format.md` (table complète des 39 blocs, détail du bloc settings, limites d'édition SVG, checklist de validation) avant toute édition non triviale ou si le fichier a un nombre de blocs ≠ 39 (autre version de FMG).

## Enchaînements utiles

- **→ orbat** : `extract.py carte.map regiments` puis convertir en JSON orbat-mapper via le skill `orbat`.
- **→ nomenclature-v4** : classifier les unités extraites.
- **→ gm-basic / warhammer40k-lore** : les notes (fiches de régiments, marqueurs, burgs) alimentent directement le lore d'une campagne.
