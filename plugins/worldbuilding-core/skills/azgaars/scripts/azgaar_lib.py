"""
azgaar_lib — Lecture / édition des sauvegardes .map d'Azgaar's Fantasy Map Generator.

Format .map (vérifié sur fichiers réels FMG v1.108.12 et v1.134.0) :
- Fichier texte UTF-8.
- Blocs séparés par CRLF ("\r\n"). DEUX dispositions coexistent :
    * 39 blocs — v1.9x → v1.11x
    * 46 blocs — v1.13x+ (ajout du module Économie : rebels, ice, goods,
      markets, trades ; le bloc "zones" passe de l'index 38 à 45)
  Les blocs 0-37 sont identiques ; la disposition est détectée automatiquement
  d'après le nombre de blocs (self._layout / self.n_blocks).
- Le SVG (bloc 5) utilise "\n" en interne — NE JAMAIS splitter sur "\n" seul.
- Les blocs JSON sont sérialisés compact (JSON.stringify : pas d'espaces).

Principe de sécurité : les blocs non modifiés sont réécrits À L'IDENTIQUE (octet
près). Seuls les blocs explicitement marqués "dirty" sont re-sérialisés.

Usage typique :
    from azgaar_lib import AzgaarMap
    m = AzgaarMap.load("monde.map")
    print(m.map_name, m.version, m.n_blocks)
    for s in m.states[1:]:
        print(s["name"])
    m.states[3]["name"] = "Nouveau Nom"
    m.mark_dirty("states")
    m.save("monde_edit.map")
    if m.has_economy:          # cartes 46 blocs seulement
        print(len(m.goods), "biens,", len(m.markets), "marchés")
"""

from __future__ import annotations
import json
import re
from pathlib import Path

SEPARATOR = "\r\n"

# ---------------------------------------------------------------------------
# Deux dispositions de blocs coexistent selon la version de FMG :
#   - 39 blocs : v1.9x → v1.11x (ex. Iondarr III, v1.108.12)
#   - 46 blocs : v1.13x+        (ex. Comia, v1.134.0 — ajout du module Économie)
# Les blocs 0-37 sont IDENTIQUES entre les deux ; seule la queue diffère.
# Le nombre de blocs sert de discriminant : AzgaarMap choisit le bon mapping
# à la lecture. Ne jamais modifier l'ordre/nombre des blocs (FMG charge par index).
# ---------------------------------------------------------------------------

# Base commune, STABLE et vérifiée sur fichiers réels des deux versions.
_BASE_BLOCKS = {
    0:  ("params",            "texte |",   "version|tip|date|seed|graphWidth|graphHeight|mapId"),
    1:  ("settings",          "texte |",   "unités, populationRate, options JSON, mapName, style..."),
    2:  ("mapCoordinates",    "json",      "latitudes/longitudes du monde"),
    3:  ("biomesData",        "texte |",   "couleurs|habitabilité|noms des biomes"),
    4:  ("notes",             "json",      "notes/légendes (dont fiches régiments et marqueurs)"),
    5:  ("svg",               "svg",       "rendu complet de la carte (labels inclus)"),
    6:  ("grid",              "json",      "grille voronoi initiale (spacing, cellsX/Y, boundary, points, features)"),
    7:  ("grid_h",            "csv int",   "grid.cells.h — altitude 0-100 (>=20 = terre)"),
    8:  ("grid_prec",         "csv int",   "grid.cells.prec — précipitations"),
    9:  ("grid_f",            "csv int",   "grid.cells.f — id de feature"),
    10: ("grid_t",            "csv int",   "grid.cells.t — distance field (+terre/-mer)"),
    11: ("grid_temp",         "csv int",   "grid.cells.temp — température °C"),
    12: ("features",          "json",      "pack.features — océans/îles/lacs (élément 0 = 0). v1.13x+ : + shoreline/height"),
    13: ("cultures",          "json",      "cultures (élément 0 = Wildlands)"),
    14: ("states",            "json",      "états (élément 0 = Neutrals ; military[], diplomacy[]. v1.13x+ : + salesTax/pollTax/treasury)"),
    15: ("burgs",             "json",      "villes/villages (élément 0 = {} vide)"),
    16: ("cells_biome",       "csv int",   "pack.cells.biome"),
    17: ("cells_burg",        "csv int",   "pack.cells.burg"),
    18: ("cells_conf",        "csv int",   "pack.cells.conf — confluences"),
    19: ("cells_culture",     "csv int",   "pack.cells.culture"),
    20: ("cells_fl",          "csv int",   "pack.cells.fl — flux d'eau"),
    21: ("cells_pop",         "csv float", "pack.cells.pop — population rurale (points de population)"),
    22: ("cells_r",           "csv int",   "pack.cells.r — id rivière"),
    23: ("deprecated_road",   "vide",      "obsolète (cells.road) — généralement vide"),
    24: ("cells_s",           "csv int",   "pack.cells.s — score de cellule"),
    25: ("cells_state",       "csv int",   "pack.cells.state"),
    26: ("cells_religion",    "csv int",   "pack.cells.religion"),
    27: ("cells_province",    "csv int",   "pack.cells.province"),
    28: ("deprecated_crossroad", "vide",   "obsolète (cells.crossroad) — généralement vide"),
    29: ("religions",         "json",      "religions (élément 0 = No religion)"),
    30: ("provinces",         "json",      "provinces (élément 0 = 0)"),
    31: ("namesData",         "texte |/",  "bases de noms du générateur (name|min|max|dupl|mult|/...)"),
    32: ("rivers",            "json",      "rivières (id != index)"),
    33: ("rulers",            "texte",     "règles de mesure posées par l'utilisateur"),
    34: ("fonts",             "json",      "polices utilisées"),
    35: ("markers",           "json",      "marqueurs (id != index ; lien note = 'marker'+i)"),
    36: ("cells_routes",      "json",      "pack.cells.routes — connexions cellule→cellule via routes"),
    37: ("routes",            "json",      "routes (roads/trails/searoutes)"),
}

# Queue v1.9x-1.11x (39 blocs) — vérifiée sur fichier réel (Iondarr III, v1.108.12)
_TAIL_39 = {
    38: ("zones",             "json",      "zones (dont ressources custom)"),
}

# Queue v1.13x+ (46 blocs) — module Économie. Vérifié sur fichier réel (Comia, v1.134.0).
# ⚠️ Les blocs 40 et 44 (tableaux de cellules) sont des DÉDUCTIONS par élimination,
# non confirmées via le code source de FMG : à valider avant toute édition fine.
_TAIL_46 = {
    38: ("rebels",             "json",     "soulèvements / prosélytisme religieux par zone de cellules (type Rebels/Proselytism)"),
    39: ("ice",                "json",     "glaciers/icebergs (points de polygone + type)"),
    40: ("cells_resource",     "csv int",  "⚠️ DÉDUIT : probable id de ressource visible par cellule (réf. 'goods'), très majoritairement 0"),
    41: ("goods",              "json",     "définition des biens économiques (nom, tags, valeur, distribution, biomeOutput...)"),
    42: ("markets",            "json",     "marchés par burg (stock/prix par bien, réf. 'goods')"),
    43: ("trades",             "json",     "transactions commerciales enregistrées (peut être volumineux)"),
    44: ("cells_econ",         "csv int",  "⚠️ DÉDUIT : champ par cellule lié à l'économie/production (catégories ~0-17)"),
    45: ("zones",              "json",     "zones (dont ressources custom) — décalé de 38 → 45"),
}

# Dispositions indexées par nombre de blocs
BLOCK_LAYOUTS = {
    39: {**_BASE_BLOCKS, **_TAIL_39},
    46: {**_BASE_BLOCKS, **_TAIL_46},
}

# Rétrocompat : BLOCKS/NAME_TO_INDEX/JSON_BLOCKS restent disponibles au niveau
# module et pointent sur la disposition 46 (surensemble). Les instances utilisent
# leur propre disposition détectée à la lecture (self._layout).
BLOCKS = BLOCK_LAYOUTS[46]
NAME_TO_INDEX = {v[0]: k for k, v in BLOCKS.items()}
JSON_BLOCKS = {k for k, v in BLOCKS.items() if v[1] == "json"}


def layout_for(n_blocks: int) -> dict:
    """Renvoie la disposition de blocs correspondant au nombre de blocs trouvés.
    Pour un nombre inconnu, retombe sur la disposition connue la plus proche
    (≤ n_blocks) afin que les blocs 0-37 restent correctement mappés."""
    if n_blocks in BLOCK_LAYOUTS:
        return BLOCK_LAYOUTS[n_blocks]
    known = sorted(BLOCK_LAYOUTS)
    best = max((k for k in known if k <= n_blocks), default=known[0])
    return BLOCK_LAYOUTS[best]


def dumps_fmg(obj) -> str:
    """Sérialise comme JSON.stringify : compact, unicode brut, sans espaces.

    Cas particulier : certaines cartes contiennent des notes avec des
    surrogates UTF-16 isolés (ex. inscriptions volontairement corrompues,
    échappées '\\udcXX' dans le JSON d'origine). json.loads les matérialise
    en codepoints isolés qui feraient échouer l'encodage UTF-8 ; on les
    ré-échappe donc en séquences '\\uXXXX', comme dans le fichier source."""
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    if any(0xD800 <= ord(c) <= 0xDFFF for c in s):
        s = re.sub(r"[\ud800-\udfff]", lambda m_: "\\u%04x" % ord(m_.group()), s)
    return s


class AzgaarMap:
    """Représentation d'une sauvegarde .map, éditable et ré-enregistrable sans perte."""

    def __init__(self, blocks: list[str], source: str | None = None):
        self._blocks = blocks
        self._source = source
        self._layout = layout_for(len(blocks))
        self._name_to_index = {v[0]: k for k, v in self._layout.items()}
        self._json_blocks = {k for k, v in self._layout.items() if v[1] == "json"}
        self._parsed: dict[int, object] = {}
        self._dirty: set[int] = set()
        if len(blocks) not in BLOCK_LAYOUTS:
            print(f"⚠️  {len(blocks)} blocs trouvés (dispositions connues : {sorted(BLOCK_LAYOUTS)}). "
                  f"Version de FMG non testée : les blocs 0-37 restent fiables, la queue peut être décalée.")

    @property
    def n_blocks(self) -> int:
        return len(self._blocks)

    # ------------------------------------------------------------------ I/O
    @classmethod
    def load(cls, path: str | Path) -> "AzgaarMap":
        raw = Path(path).read_bytes().decode("utf-8")
        return cls(raw.split(SEPARATOR), source=str(path))

    def save(self, path: str | Path) -> None:
        """Réécrit le fichier. Les blocs non modifiés restent identiques à l'octet."""
        for idx in self._dirty:
            if idx in self._json_blocks:
                self._blocks[idx] = dumps_fmg(self._parsed[idx])
            else:
                # blocs non-JSON édités : la valeur parsée est déjà une string
                self._blocks[idx] = self._parsed[idx]
        Path(path).write_bytes(SEPARATOR.join(self._blocks).encode("utf-8"))
        self._dirty.clear()

    # ------------------------------------------------------------ accès blocs
    def raw(self, name_or_index) -> str:
        idx = self._idx(name_or_index)
        return self._blocks[idx]

    def set_raw(self, name_or_index, value: str) -> None:
        idx = self._idx(name_or_index)
        self._blocks[idx] = value
        self._parsed.pop(idx, None)
        self._dirty.discard(idx)

    def block(self, name_or_index):
        """Renvoie le bloc parsé (JSON → objet Python, sinon string). Mis en cache."""
        idx = self._idx(name_or_index)
        if idx not in self._parsed:
            if idx in self._json_blocks:
                self._parsed[idx] = json.loads(self._blocks[idx]) if self._blocks[idx] else None
            else:
                self._parsed[idx] = self._blocks[idx]
        return self._parsed[idx]

    def mark_dirty(self, name_or_index) -> None:
        """À appeler après toute modification d'un objet renvoyé par .block() / propriétés."""
        idx = self._idx(name_or_index)
        self.block(idx)  # force le parse si pas déjà fait
        self._dirty.add(idx)

    def _idx(self, key) -> int:
        if isinstance(key, int):
            return key
        if key in self._name_to_index:
            return self._name_to_index[key]
        raise KeyError(f"Bloc inconnu : {key}. Blocs valides ({self.n_blocks} blocs) : "
                       f"{sorted(self._name_to_index)}")

    # ------------------------------------------------------------ propriétés
    @property
    def params(self) -> list[str]:
        return self._blocks[0].split("|")

    @property
    def version(self) -> str:
        return self.params[0]

    @property
    def seed(self) -> str:
        return self.params[3]

    @property
    def size(self) -> tuple[int, int]:
        p = self.params
        return int(p[4]), int(p[5])

    # -- settings (bloc 1) : head | optionsJSON | tail — le JSON peut contenir des '|'
    def _split_settings(self):
        s = self._blocks[1]
        jstart = s.find("{")
        head = s[:jstart].rstrip("|").split("|")
        depth = 0
        for k, ch in enumerate(s[jstart:]):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    jend = jstart + k + 1
                    break
        options = s[jstart:jend]
        tail = s[jend:].lstrip("|").split("|")
        return head, options, tail

    @property
    def settings_head(self) -> list[str]:
        """[distanceUnit, distanceScale, areaUnit, heightUnit, heightExponent,
        temperatureScale, barSize, barLabel, barBackOpacity, barBackColor,
        barPosX, barPosY, populationRate, urbanization, mapSizeOutput,
        latitudeOutput, ?, ?, ?…] (les champs vides sont des options de barre d'échelle)."""
        return self._split_settings()[0]

    @property
    def options(self) -> dict:
        """Options JSON (year, era, military[], winds, temperatures...)."""
        return json.loads(self._split_settings()[1])

    def set_options(self, options: dict) -> None:
        """Remplace le JSON d'options dans le bloc settings par chirurgie exacte :
        seul le segment JSON est remplacé, les séparateurs '|' environnants sont
        préservés à l'identique (le nombre de pipes est significatif pour FMG)."""
        s = self._blocks[1]
        jstart = s.find("{")
        depth = 0
        for k, ch in enumerate(s[jstart:]):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    jend = jstart + k + 1
                    break
        self._blocks[1] = s[:jstart] + dumps_fmg(options) + s[jend:]

    @property
    def settings_tail(self) -> list[str]:
        """[mapName, hideLabels, stylePreset, rescaleLabels, ...]"""
        return self._split_settings()[2]

    @property
    def map_name(self) -> str:
        return self.settings_tail[0]

    @property
    def population_rate(self) -> float:
        """1 point de population = population_rate habitants."""
        try:
            return float(self.settings_head[12])
        except (IndexError, ValueError):
            return 1000.0

    @property
    def urbanization(self) -> float:
        try:
            return float(self.settings_head[13])
        except (IndexError, ValueError):
            return 1.0

    # -- collections principales
    def _list(self, name) -> list:
        """Collection JSON d'un bloc, avec [] si le bloc est vide (cas légitime :
        p.ex. une carte sans zones custom a un bloc zones vide).

        IMPORTANT : quand le bloc est vide, on matérialise la liste vide DANS le
        cache `_parsed` et on renvoie toujours cette même instance. Sans cela,
        chaque accès recréerait une liste neuve et les mutations (append d'une
        zone, d'un marqueur…) seraient perdues à la sauvegarde."""
        idx = self._idx(name)
        v = self.block(idx)
        if v is None:
            v = []
            self._parsed[idx] = v
        return v

    @property
    def notes(self) -> list:
        return self._list("notes")

    @property
    def cultures(self) -> list:
        return self._list("cultures")

    @property
    def states(self) -> list:
        return self._list("states")

    @property
    def burgs(self) -> list:
        return self._list("burgs")

    @property
    def religions(self) -> list:
        return self._list("religions")

    @property
    def provinces(self) -> list:
        return self._list("provinces")

    @property
    def rivers(self) -> list:
        return self._list("rivers")

    @property
    def markers(self) -> list:
        return self._list("markers")

    @property
    def routes(self) -> list:
        return self._list("routes")

    @property
    def zones(self) -> list:
        return self._list("zones")

    @property
    def features(self) -> list:
        return self._list("features")

    # -- collections économiques (format 46 blocs, v1.13x+ uniquement)
    @property
    def has_economy(self) -> bool:
        """True si la carte embarque le module économie (format 46 blocs)."""
        return "goods" in self._name_to_index

    def _econ_block(self, name) -> list:
        if name not in self._name_to_index:
            raise AttributeError(
                f"'{name}' absent : cette carte est en {self.n_blocks} blocs "
                f"(module économie disponible seulement en 46 blocs, FMG v1.13x+).")
        return self._list(name)

    @property
    def rebels(self) -> list:
        """Soulèvements / prosélytisme (v1.13x+)."""
        return self._econ_block("rebels")

    @property
    def ice(self) -> list:
        """Glaciers / icebergs (v1.13x+)."""
        return self._econ_block("ice")

    @property
    def goods(self) -> list:
        """Définition des biens économiques (v1.13x+)."""
        return self._econ_block("goods")

    @property
    def markets(self) -> list:
        """Marchés par burg (v1.13x+)."""
        return self._econ_block("markets")

    @property
    def trades(self) -> list:
        """Transactions commerciales (v1.13x+)."""
        return self._econ_block("trades")

    # -- tableaux de cellules (csv)
    def cells(self, name: str, as_float: bool = False) -> list:
        """cells('cells_biome') → liste d'int (ou float pour cells_pop)."""
        raw = self.raw(name)
        if not raw:
            return []
        conv = float if (as_float or name == "cells_pop") else int
        return [conv(x) for x in raw.split(",")]

    def set_cells(self, name: str, values: list) -> None:
        idx = self._idx(name)
        def fmt(v):
            if isinstance(v, float) and v == int(v):
                return str(int(v))
            return repr(v) if isinstance(v, float) else str(v)
        self._blocks[idx] = ",".join(fmt(v) for v in values)
        self._parsed.pop(idx, None)

    # ------------------------------------------------------------ recherches
    def find_burg(self, name: str) -> dict | None:
        low = name.lower()
        for b in self.burgs:
            if b and b.get("name", "").lower() == low:
                return b
        return None

    def find_state(self, name: str) -> dict | None:
        low = name.lower()
        for s in self.states:
            if s and s.get("name", "").lower() == low:
                return s
        return None

    def regiments(self) -> list[dict]:
        """Tous les régiments de tous les états, enrichis du nom de l'état et
        de la note associée (id 'regiment{state}-{i}')."""
        notes_by_id = {n["id"]: n for n in self.notes if "id" in n}
        out = []
        for s in self.states:
            if not s or not s.get("military"):
                continue
            for r in s["military"]:
                r2 = dict(r)
                r2["stateName"] = s["name"]
                note = notes_by_id.get(f"regiment{s['i']}-{r['i']}")
                if note:
                    r2["legend"] = note.get("legend", "")
                out.append(r2)
        return out

    def real_population(self, points: float) -> int:
        """Convertit des points de population en habitants."""
        return round(points * self.population_rate)

    # ------------------------------------------ analyses par état (helpers)
    def burgs_by_state(self, include_removed: bool = False) -> dict[int, list]:
        """{stateId: [burgs triés par population décroissante]}."""
        out: dict[int, list] = {}
        for b in self.burgs:
            if not b or (b.get("removed") and not include_removed):
                continue
            out.setdefault(b.get("state", 0), []).append(b)
        for lst in out.values():
            lst.sort(key=lambda b: -b.get("population", 0))
        return out

    def ports_by_state(self) -> dict[int, list]:
        """{stateId: [burgs portuaires triés par population décroissante]}."""
        return {st: [b for b in lst if b.get("port")]
                for st, lst in self.burgs_by_state().items()
                if any(b.get("port") for b in lst)}

    def market_value_by_state(self) -> dict[int, float]:
        """Valeur économique par état : somme sur ses marchés de stock × valeur
        du bien (module économie, cartes 46 blocs uniquement). Les marchés sont
        rattachés à l'état via leur burg central."""
        if not self.has_economy:
            return {}
        goods_val = {g["i"]: g.get("value", 1) for g in self.goods}
        burg_state = {b["i"]: b.get("state", 0) for b in self.burgs if b}
        out: dict[int, float] = {}
        for mk in self.markets:
            st = burg_state.get(mk.get("centerBurgId"), 0)
            v = sum(float(gd.get("stock", 0)) * goods_val.get(int(gid), 1)
                    for gid, gd in mk.get("goods", {}).items())
            out[st] = out.get(st, 0) + v
        return out

    def good_stock_by_state(self) -> dict[int, dict[int, float]]:
        """{stateId: {goodId: stock total}} — agrège les stocks de tous les
        marchés d'un état, par bien (module économie, cartes 46 blocs
        uniquement). Base pour détecter pénuries/abondances relatives."""
        if not self.has_economy:
            return {}
        burg_state = {b["i"]: b.get("state", 0) for b in self.burgs if b}
        out: dict[int, dict[int, float]] = {}
        for mk in self.markets:
            st = burg_state.get(mk.get("centerBurgId"), 0)
            bucket = out.setdefault(st, {})
            for gid, gd in mk.get("goods", {}).items():
                gid = int(gid)
                bucket[gid] = bucket.get(gid, 0) + float(gd.get("stock", 0))
        return out

    def trade_flows_by_state(self) -> dict[str, float]:
        """{'i-j' (i<j): valeur totale échangée (units×price)} entre paires
        d'états, agrégée depuis les transactions RÉELLES du bloc `trades`
        (module économie, cartes 46 blocs uniquement). Chaque transaction a un
        vendeur et un acheteur, chacun soit un marché (rattaché à son burg
        central) soit un burg directement — les deux sont ramenés à leur état."""
        if not self.has_economy:
            return {}
        market_burg = {mk["i"]: mk.get("centerBurgId") for mk in self.markets}
        burg_state = {b["i"]: b.get("state", 0) for b in self.burgs if b}

        def resolve_state(entity_id, entity_type):
            if entity_type == "market":
                burg_id = market_burg.get(entity_id)
                return burg_state.get(burg_id, 0)
            return burg_state.get(entity_id, 0)

        flows: dict[str, float] = {}
        for t in self.trades:
            sa = resolve_state(t.get("seller"), t.get("sellerType"))
            sb = resolve_state(t.get("buyer"), t.get("buyerType"))
            if not sa or not sb or sa == sb:
                continue
            key = f"{min(sa, sb)}-{max(sa, sb)}"
            flows[key] = flows.get(key, 0) + float(t.get("units", 0)) * float(t.get("price", 0))
        return flows

    def industry_index(self) -> dict[int, float]:
        """Indice industriel 0..1 par état : 60 % valeur des marchés (si module
        économie présent, sinon 0) + 40 % population urbaine, normalisés."""
        market = self.market_value_by_state()
        active = [s for s in self.states if s and not s.get("removed") and s.get("i")]
        max_m = max((market.get(s["i"], 0) for s in active), default=0) or 1
        max_u = max((s.get("urban", 0) for s in active), default=0) or 1
        return {s["i"]: 0.6 * market.get(s["i"], 0) / max_m + 0.4 * s.get("urban", 0) / max_u
                for s in active}

    def active_states(self) -> list[dict]:
        """États actifs (hors Neutrals/supprimés) — raccourci utilisé partout."""
        return [s for s in self.states if s and not s.get("removed") and s.get("i")]

    # ------------------------------------------ interprétation militaire
    def unit_powers(self) -> dict[str, float]:
        """{nom_type: valeur_de_combat} d'après options.military."""
        return {u["name"]: float(u.get("power", 1)) for u in self.options.get("military", [])}

    def state_power(self, state: dict, powers: dict | None = None) -> float:
        """Puissance militaire totale d'un état : somme sur ses régiments de
        count × power (par type d'unité). Passer `powers` (résultat de
        `unit_powers()`) si on l'appelle en boucle, pour éviter de le recalculer."""
        powers = powers if powers is not None else self.unit_powers()
        return sum(sum(cnt * powers.get(unit, 1) for unit, cnt in r.get("u", {}).items())
                   for r in state.get("military", []))

    def state_effectif(self, state: dict) -> int:
        """Effectif total (personnel) d'un état, tous régiments confondus."""
        return sum(r.get("a", 0) for r in state.get("military", []))

    # ------------------------------------------ interprétation géographique
    def state_provinces(self, state: dict) -> list[int]:
        """Ids des provinces actives appartenant à un état."""
        return sorted(p["i"] for p in self.provinces
                      if isinstance(p, dict) and not p.get("removed") and p.get("state") == state["i"])

    def _dominant_by_cell_field(self, state: dict, cell_field: str, names: list[str],
                                label: str, top: int) -> list[dict]:
        """Généralise le comptage 'quel id domine le territoire d'un état' pour
        n'importe quel champ par cellule (biome, culture, religion...). Renvoie
        [{label: nom, "cellules": n, "part": fraction 0-1}], trié décroissant."""
        cells_state = self.cells("cells_state")
        cells_val = self.cells(cell_field)
        counts: dict[int, int] = {}
        total = 0
        for st, v in zip(cells_state, cells_val):
            if int(st) == state["i"]:
                v = int(v)
                counts[v] = counts.get(v, 0) + 1
                total += 1
        ranked = sorted(counts.items(), key=lambda kv: -kv[1])[:top]
        return [{label: names[v] if v < len(names) else f"{label}#{v}", "cellules": n,
                "part": round(n / total, 3) if total else 0}
                for v, n in ranked]

    def dominant_biomes(self, state: dict, top: int = 3) -> list[dict]:
        """Biomes dominants du territoire d'un état, par nombre de cellules.
        Renvoie [{"biome": nom, "cellules": n, "part": fraction}], triés
        décroissant. Le nom vient de biomesData (bloc 3) ; l'id biome de chaque
        cellule, de cells_biome."""
        return self._dominant_by_cell_field(state, "cells_biome", self.biomes_names(), "biome", top)

    def dominant_cultures(self, state: dict, top: int = 3) -> list[dict]:
        """Cultures dominantes du territoire d'un état, par nombre de cellules.
        Renvoie [{"culture": nom, "cellules": n, "part": fraction}], triés
        décroissant. `part` proche de 1 = territoire culturellement homogène ;
        plusieurs entrées avec parts comparables = tension culturelle latente
        (utile par ex. pour motiver une révolte sur une province annexée)."""
        names = [c.get("name", f"culture#{c.get('i')}") for c in self.cultures]
        return self._dominant_by_cell_field(state, "cells_culture", names, "culture", top)

    def dominant_religions(self, state: dict, top: int = 3) -> list[dict]:
        """Religions dominantes du territoire d'un état, même principe que
        dominant_cultures. Renvoie [{"religion": nom, "cellules": n, "part": fraction}]."""
        names = [r.get("name", f"religion#{r.get('i')}") for r in self.religions]
        return self._dominant_by_cell_field(state, "cells_religion", names, "religion", top)

    def approx_relief(self, state: dict) -> dict | None:
        """⚠️ APPROXIMATION, pas une couverture complète du territoire — voir
        limite ci-dessous. Estime le relief autour des villes d'un état en
        cherchant, pour chaque burg, le point de GRILLE le plus proche (grid !=
        pack, la seule maille qui porte hauteur/précipitations/température) et
        moyenne ces valeurs. Renvoie {"altitude": 0-100 (échelle FMG, >=20 =
        terre), "precipitations": ..., "temperature": ..., "villesEchantillonnees": n}
        ou None si l'état n'a aucun burg.

        LIMITE STRUCTURELLE : le fichier .map ne stocke ni les coordonnées des
        cellules pack (état/culture/biome...) ni de correspondance vers leur
        cellule de grille parente — seules les cellules de GRILLE (49 830 sur
        Comia, contre 12 933 cellules pack) ont des coordonnées et un champ
        hauteur. Un vrai relief par état impliquerait de ré-implémenter la
        retriangulation interne de FMG (Delaunay/Voronoi) pour reconstituer
        cette correspondance — trop fragile pour la fiabilité recherchée ici.
        Cette méthode se contente donc d'échantillonner le terrain SOUS LES
        VILLES (biaisé vers les zones habitées, ne reflète pas les étendues
        sauvages d'un grand état) — un indice, pas une carte."""
        import numpy as np
        burgs = [b for b in self.burgs_by_state().get(state["i"], [])]
        if not burgs:
            return None
        if not hasattr(self, "_grid_np_cache"):
            grid = self.block("grid")
            self._grid_np_cache = (
                np.asarray(grid["points"], dtype=float),
                np.asarray(self.cells("grid_h"), dtype=float),
                np.asarray(self.cells("grid_prec"), dtype=float),
                np.asarray(self.cells("grid_temp"), dtype=float),
            )
        pts, h, prec, temp = self._grid_np_cache
        bxy = np.asarray([[b["x"], b["y"]] for b in burgs], dtype=float)
        # plus proche voisin brute-force (nb de villes toujours petit ; la
        # grille elle peut être grande, d'où le vectorisé par lot de villes)
        d2 = ((pts[None, :, :] - bxy[:, None, :]) ** 2).sum(axis=2)
        nearest = d2.argmin(axis=1)
        return {
            "altitude": round(float(h[nearest].mean()), 1),
            "precipitations": round(float(prec[nearest].mean()), 1),
            "temperature": round(float(temp[nearest].mean()), 1),
            "villesEchantillonnees": len(burgs),
            "avertissement": "estimation via les villes uniquement, pas une couverture du territoire entier",
        }

    def biomes_names(self) -> list[str]:
        """Noms des biomes dans l'ordre de leurs ids. Bloc biomesData vérifié à
        3 champs séparés par '|' : couleurs, habitabilité, noms (chacun une
        liste séparée par des virgules, alignée sur l'id du biome)."""
        parts = self.raw("biomesData").split("|")
        names_field = parts[2] if len(parts) > 2 else parts[-1]
        return [n for n in names_field.split(",") if n]

    # ------------------------------------------ interprétation diplomatique
    def diplomacy_matrix(self) -> dict[str, str]:
        """{'i-j' (i<j): statut vu depuis i} — lecture directe de
        states[].diplomacy, TOUJOURS la source de vérité (ce que l'utilisateur
        a réellement réglé dans FMG, jamais une mémoire externe)."""
        states = self.active_states()
        out = {}
        for s in states:
            dip = s.get("diplomacy", [])
            for o in states:
                if o["i"] <= s["i"]:
                    continue
                out[f"{s['i']}-{o['i']}"] = dip[o["i"]] if o["i"] < len(dip) else "Unknown"
        return out

    def current_wars(self) -> list[tuple[int, int]]:
        """Paires en guerre d'après la diplomatie ACTUELLE (statut Enemy dans un
        sens ou l'autre). Toujours dérivé du fichier, jamais mémorisé — si le
        statut a été changé dans FMG, la guerre apparaît/disparaît d'ici direct."""
        states = {s["i"]: s for s in self.active_states()}
        wars = []
        for s in states.values():
            dip = s.get("diplomacy", [])
            for j, status in enumerate(dip):
                if j not in states or j <= s["i"]:
                    continue
                if status == "Enemy":
                    wars.append((s["i"], j))
                else:
                    dip2 = states[j].get("diplomacy", [])
                    if s["i"] < len(dip2) and dip2[s["i"]] == "Enemy":
                        wars.append((s["i"], j))
        return wars

    # ------------------------------------------ interprétation stratégique (synthèse)
    def aggression_of(self, state: dict) -> float:
        """Posture agressive synthétique 0.1-1.6, dérivée de champs natifs FMG
        (expansionism, alert, type) — pas de mémoire, recalculée à chaque appel."""
        exp = float(state.get("expansionism", 1))
        alert = float(state.get("alert", 0.5))
        bonus = 0.25 if state.get("type") == "Nomadic" else 0
        return round(max(0.1, min(1.6, exp / 3 + alert / 4 + bonus)), 2)

    def stability_of(self, state: dict, at_war: bool = False) -> float:
        """Stabilité synthétique 0.05-1.0, dérivée de l'alerte actuelle et du
        fait d'être en guerre — aucune mémoire, dérive uniquement du présent."""
        alert = float(state.get("alert", 0.5))
        base = 0.65 - 0.12 * max(0, alert - 1) - (0.15 if at_war else 0)
        return round(max(0.05, min(1.0, base)), 2)

    def strategic_snapshot(self) -> dict:
        """Photographie complète et purement lue du monde : par état —
        population réelle, puissance militaire, effectif, industrie, trésor
        (si économie), ports, provinces possédées, biomes dominants, capitale,
        guerres en cours (déduites de la diplomatie réelle), posture/stabilité
        synthétiques. Base commune pour tout skill qui a besoin de comprendre
        « où en est le monde » sans réimplémenter sa propre lecture (ex.
        /gm-worlds). Ne modifie rien."""
        rate = self.population_rate
        powers = self.unit_powers()
        ind = self.industry_index()
        ports = self.ports_by_state()
        states = self.active_states()
        wars = self.current_wars()
        at_war_with: dict[int, list[int]] = {}
        for a, b in wars:
            at_war_with.setdefault(a, []).append(b)
            at_war_with.setdefault(b, []).append(a)

        snap = {"year": int(self.options.get("year", 0)), "era": self.options.get("era", ""),
                "n_blocs": self.n_blocks, "has_economy": self.has_economy, "states": {}}
        for s in states:
            pop = (s.get("urban", 0) + s.get("rural", 0)) * rate
            at_war = s["i"] in at_war_with
            snap["states"][str(s["i"])] = {
                "nom": s["name"],
                "population": round(pop),
                "puissanceMilitaire": round(self.state_power(s, powers)),
                "effectifTotal": self.state_effectif(s),
                "nbRegiments": len(s.get("military", [])),
                "industrie": round(ind.get(s["i"], 0), 3),
                "alerte": s.get("alert", 0),
                "agressivite": self.aggression_of(s),
                "stabilite": self.stability_of(s, at_war),
                "tresor": s.get("treasury") if self.has_economy else None,
                "ports": len(ports.get(s["i"], [])),
                "provinces": self.state_provinces(s),
                "biomesDominants": self.dominant_biomes(s),
                "culturesDominantes": self.dominant_cultures(s),
                "religionsDominantes": self.dominant_religions(s),
                "reliefApprox": self.approx_relief(s),
                "capitale": next((b["name"] for b in self.burgs
                                  if b and b.get("i") == s.get("capital")), None),
                "enGuerreAvec": at_war_with.get(s["i"], []),
            }
        snap["guerres"] = [{"a": a, "b": b, "aNom": self.states[a]["name"], "bNom": self.states[b]["name"]}
                           for a, b in wars]
        snap["diplomatie"] = self.diplomacy_matrix()
        return snap

    # ------------------------------------------ édition militaire
    def set_military_types(self, types: list[dict]) -> None:
        """Remplace options.military (types d'unités). Chaque type :
        {icon, name, rural, urban, crew, power, type, separate}.
        Les compositions 'u' des régiments doivent référencer ces noms."""
        opts = self.options
        opts["military"] = types
        self.set_options(opts)

    def set_state_military(self, state_id: int, regiments: list[dict],
                           legends: list[str] | None = None) -> None:
        """Remplace l'armée d'un état ET synchronise ses notes 'regiment{s}-{i}'
        (purge des anciennes, injection des nouvelles si legends est fourni).
        Chaque régiment doit contenir : i (== index), a (== somme de u), cell,
        x, y, bx, by, u, n (1 si naval/séparé), name, state (== state_id), icon.

        ⚠️ Purge AUSSI le cache SVG des boîtes de régiment de cet état (bug
        découvert empiriquement : le groupe <g id="armyN"> est un rendu figé
        au moment de la sauvegarde FMG, jamais régénéré depuis les données au
        chargement — contrairement aux burgs/labels. Sans cette purge, FMG
        continue d'afficher les anciens noms/effectifs sur la carte alors que
        l'éditeur de régiment, lui, lit les nouvelles données en direct : les
        deux deviennent incohérents. Voir reference/format.md."""
        s = self.states[state_id]
        for j, r in enumerate(regiments):
            if r.get("i") != j or r.get("state") != state_id:
                raise ValueError(f"régiment {j} : i/state incohérents (i={r.get('i')}, state={r.get('state')})")
            if r.get("a") != sum(r.get("u", {}).values()):
                raise ValueError(f"régiment {j} : a != somme de u")
        s["military"] = regiments
        self.mark_dirty("states")
        prefix = f"regiment{state_id}-"
        notes = [n for n in self.notes if not str(n.get("id", "")).startswith(prefix)]
        if legends:
            for j, r in enumerate(regiments):
                notes.append({"id": f"{prefix}{j}",
                              "name": f"{r['name']} ({s['name']})",
                              "legend": legends[j] if j < len(legends) else ""})
        self._parsed[self._idx("notes")] = notes
        self.mark_dirty("notes")
        self.clear_army_svg([state_id])

    # ------------------------------------------------------------ édition SVG
    def clear_army_svg(self, state_ids: list[int] | None = None) -> int:
        """Vide le cache SVG figé des boîtes de régiment pour les états donnés
        (ou tous les états portant un groupe army* si state_ids est None).

        Le groupe <g id="army{stateId}"> contient un <g id="regiment{s}-{i}">
        par régiment, rendu (position, nom, effectif affiché) au moment de la
        dernière sauvegarde FMG — PAS régénéré depuis les données au
        chargement. Après une édition programmatique de states[i].military,
        ce cache devient incohérent avec les vraies données (le panneau
        d'édition de régiment dans FMG lit les données à jour, mais la boîte
        affichée sur la carte reste figée sur l'ancien nom/effectif).

        Vider le groupe (en gardant le wrapper <g id="armyN" fill=... color=...>
        vide) force FMG à redessiner les boîtes depuis les données au prochain
        rafraîchissement du layer Military — au lieu de laisser un affichage
        obsolète. Retourne le nombre de groupes vidés."""
        svg = self.raw("svg")
        ids = state_ids if state_ids is not None else self._all_army_ids(svg)
        cleared = 0
        for sid in ids:
            svg, ok = self._clear_one_army_group(svg, sid)
            cleared += int(ok)
        if cleared:
            self._blocks[self._idx("svg")] = svg
            self._parsed.pop(self._idx("svg"), None)
        return cleared

    @staticmethod
    def _all_army_ids(svg: str) -> list[int]:
        return [int(m.group(1)) for m in re.finditer(r'<g id="army(\d+)"', svg)]

    @staticmethod
    def _clear_one_army_group(svg: str, state_id: int) -> tuple[str, bool]:
        open_re = re.compile(r'<g id="army%d"[^>]*>' % state_id)
        m = open_re.search(svg)
        if not m:
            return svg, False
        content_start = m.end()
        # comptage de profondeur pour trouver le </g> correspondant (les
        # sous-groupes regiment*-* ne contiennent eux-mêmes aucun <g> imbriqué,
        # mais on compte quand même pour rester robuste aux versions futures)
        depth = 1
        j = content_start
        n = len(svg)
        while j < n and depth > 0:
            nxt_open = svg.find("<g", j)
            nxt_close = svg.find("</g>", j)
            if nxt_close == -1:
                return svg, False  # SVG malformé : on n'touche à rien
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                j = nxt_open + 2
            else:
                depth -= 1
                j = nxt_close + 4
        content_end = j - 4  # position juste avant le </g> final trouvé
        if depth != 0:
            return svg, False
        new_svg = svg[:content_start] + svg[content_end:]
        return new_svg, True

    def sync_svg_label(self, kind: str, entity_id: int, new_text: str) -> bool:
        """Met à jour le label rendu dans le SVG après un renommage.
        kind : 'burg' → id='burgLabel{ID}' ; 'state' → id='stateLabel{ID}'.
        Retourne True si un label a été remplacé.
        IMPORTANT : les labels d'états peuvent être en <textPath> multi-<tspan> —
        dans ce cas le texte est remplacé dans le premier tspan et les autres vidés."""
        svg = self.raw("svg")
        elem_id = f"{'burgLabel' if kind == 'burg' else 'stateLabel'}{entity_id}"
        # cas simple : <text ... id="xxx" ...>ancien</text>
        pattern = re.compile(r'(<text[^>]*\bid="%s"[^>]*>)(.*?)(</text>)' % re.escape(elem_id), re.S)
        m = pattern.search(svg)
        if not m:
            return False
        inner = m.group(2)
        if "<tspan" in inner or "<textPath" in inner:
            # remplace le contenu texte des tspans (garde le 1er, vide les autres)
            tspans = re.findall(r"<tspan[^>]*>.*?</tspan>", inner, re.S)
            if tspans:
                first_done = [False]
                def _rep(mt):
                    open_tag = re.match(r"<tspan[^>]*>", mt.group(0)).group(0)
                    if not first_done[0]:
                        first_done[0] = True
                        return open_tag + new_text + "</tspan>"
                    return open_tag + "</tspan>"
                inner_new = re.sub(r"<tspan[^>]*>.*?</tspan>", _rep, inner, flags=re.S)
            else:
                inner_new = new_text
        else:
            inner_new = new_text
        svg_new = svg[:m.start(2)] + inner_new + svg[m.end(2):]
        self._blocks[self._idx("svg")] = svg_new
        self._parsed.pop(self._idx("svg"), None)
        return True

    def rename_burg(self, old_name: str, new_name: str) -> bool:
        b = self.find_burg(old_name)
        if not b:
            return False
        b["name"] = new_name
        self.mark_dirty("burgs")
        self.sync_svg_label("burg", b["i"], new_name)
        return True

    def rename_state(self, old_name: str, new_name: str) -> bool:
        s = self.find_state(old_name)
        if not s:
            return False
        s["name"] = new_name
        if s.get("formName"):
            s["fullName"] = f"{new_name} {s['formName']}" if s["i"] else new_name
        self.mark_dirty("states")
        self.sync_svg_label("state", s["i"], new_name.upper() if False else new_name)
        return True

    # ------------------------------------------------------------ résumé
    def summary(self) -> dict:
        w, h = self.size
        opts = self.options
        s = {
            "fichier": self._source,
            "version": self.version,
            "blocs": self.n_blocks,
            "nom": self.map_name,
            "seed": self.seed,
            "taille_px": f"{w}x{h}",
            "année": f"{opts.get('year')} {opts.get('era', '')}".strip(),
            "populationRate": self.population_rate,
            "états": sum(1 for st in self.states[1:] if st and not st.get("removed")),
            "provinces": sum(1 for p in self.provinces[1:] if isinstance(p, dict) and not p.get("removed")),
            "burgs": sum(1 for b in self.burgs[1:] if b and not b.get("removed")),
            "cultures": sum(1 for c in self.cultures if c and not c.get("removed")),
            "religions": sum(1 for r in self.religions[1:] if r and not r.get("removed")),
            "rivières": len(self.rivers),
            "marqueurs": len(self.markers),
            "routes": len(self.routes),
            "zones": len(self.zones),
            "notes": len(self.notes),
            "régiments": len(self.regiments()),
        }
        if self.has_economy:
            s["économie"] = {
                "biens": len(self.goods),
                "marchés": len(self.markets),
                "transactions": len(self.trades),
                "soulèvements": len(self.rebels),
                "glaces": len(self.ice),
            }
        return s
