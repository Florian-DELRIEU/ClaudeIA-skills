"""
orbat_lib.py — utilitaires partagés pour manipuler les fichiers ORBAT
exportés depuis orbat-mapper.app (type "ORBAT-mapper").

Format résumé :
  racine -> sides[] -> (groups[] -> subUnits[]) et/ou (units[])
  chaque unité : {id, name, sidc, subUnits[], equipment[{name,count}],
                  personnel[{name,count}], state[], ...}
  catalogues racine : equipment[{name,description}], personnel[{name,description}]

Toutes les fonctions sont sans effet de bord sauf mention contraire.
"""
import json
import random
import string
import datetime

ID_ALPHABET = string.ascii_letters + string.digits


def load(path):
    """Charge un ORBAT JSON depuis un chemin."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(orbat, path):
    """Écrit un ORBAT JSON (indent=1, comme l'export du site)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(orbat, f, ensure_ascii=False, indent=1)


def gen_id(n=10):
    """Génère un id de la forme utilisée par orbat-mapper (10 caractères)."""
    return "".join(random.choice(ID_ALPHABET) for _ in range(n))


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Parcours de l'arbre
# ---------------------------------------------------------------------------
def iter_units(orbat, with_path=False):
    """
    Itère sur TOUTES les unités de l'ORBAT (récursif).
    Si with_path=True, yield (unit, path) où path est la liste des noms
    depuis le side jusqu'au parent inclus.
    """
    def rec(u, path):
        if with_path:
            yield u, path
        else:
            yield u
        for su in u.get("subUnits", []) or []:
            yield from rec(su, path + [u.get("name", "?")])

    for side in orbat.get("sides", []):
        base = [side.get("name", "?")]
        for u in side.get("units", []) or []:
            if u.get("name") is None and "rootUnitName" in u:
                continue  # placeholder de side (anciennes versions)
            yield from rec(u, base)
        for g in side.get("groups", []) or []:
            gpath = base + [g.get("name", "?")]
            for su in g.get("subUnits", []) or []:
                yield from rec(su, gpath)


def find_unit(orbat, key):
    """
    Retrouve une unité par son id exact, ou à défaut par nom exact,
    ou à défaut par nom partiel (insensible à la casse). Renvoie l'unité ou None.
    """
    key_l = key.lower()
    by_name = None
    by_partial = None
    for u in iter_units(orbat):
        if u.get("id") == key:
            return u
        if by_name is None and (u.get("name") or "").lower() == key_l:
            by_name = u
        if by_partial is None and key_l in (u.get("name") or "").lower():
            by_partial = u
    return by_name or by_partial


def subtree_units(root):
    """Itère sur une unité et toute sa descendance."""
    yield root
    for su in root.get("subUnits", []) or []:
        yield from subtree_units(su)


# ---------------------------------------------------------------------------
# Catalogues
# ---------------------------------------------------------------------------
def catalog_map(orbat, kind):
    """
    kind='equipment'|'personnel' -> {name: description} (catalogues racine).
    kind='supplies' -> lit supplyCategories {name: description}.
    """
    if kind == "supplies":
        return {e["name"]: e.get("description", "") for e in orbat.get("supplyCategories", []) or []}
    return {e["name"]: e.get("description", "") for e in orbat.get(kind, []) or []}


# ---------------------------------------------------------------------------
# Agrégation
# ---------------------------------------------------------------------------
def aggregate(units, kind="equipment"):
    """
    Somme les counts par name sur un itérable d'unités (état de BASE, hors timeline).
    kind = 'equipment' | 'personnel' | 'supplies'. Renvoie un dict {name: total}.
    """
    totals = {}
    for u in units:
        for item in u.get(kind, []) or []:
            totals[item["name"]] = totals.get(item["name"], 0) + item.get("count", 0)
    return totals


# ---------------------------------------------------------------------------
# Dimension temporelle (scénarios : champ state[] des unités)
# ---------------------------------------------------------------------------
# Un state[] est une liste d'entrées datées :
#   {id, t (ISO), location [lng,lat], via [[lng,lat]...], title,
#    status, sidc, symbolOptions,
#    update {equipment|personnel|supplies:[{name,onHand}]},  # valeurs ABSOLUES
#    diff   {equipment|personnel|supplies:[{name,onHand}]}}  # DELTAS
RESOURCE_KINDS = ("equipment", "personnel", "supplies")


def base_resources(unit, kind):
    """Quantités de base (champ `count`) d'une unité pour une catégorie."""
    return {it["name"]: it.get("count", 0) for it in unit.get(kind, []) or []}


def sorted_states(unit):
    """Entrées de state triées chronologiquement par `t`."""
    return sorted(unit.get("state", []) or [], key=lambda s: s.get("t", ""))


def resource_at(unit, kind, t=None):
    """
    Quantités d'une unité pour `kind` à l'instant `t` (ISO str) en rejouant la timeline.
    `update` pose des valeurs absolues (onHand), `diff` applique un delta.
    t=None -> état final. Renvoie {name: quantité}.
    """
    cur = base_resources(unit, kind)
    for st in sorted_states(unit):
        if t is not None and st.get("t", "") > t:
            break
        for it in (st.get("update", {}) or {}).get(kind, []) or []:
            cur[it["name"]] = it.get("onHand", 0)
        for it in (st.get("diff", {}) or {}).get(kind, []) or []:
            cur[it["name"]] = cur.get(it["name"], 0) + it.get("onHand", 0)
    return cur


def position_at(unit, t=None):
    """Dernière `location` [lng,lat] connue à l'instant t (ou finale si t=None). None si jamais positionnée."""
    pos = None
    for st in sorted_states(unit):
        if t is not None and st.get("t", "") > t:
            break
        if "location" in st:
            pos = st["location"]
    return pos


def unit_timeline(unit):
    """
    Liste lisible des moments-clés d'une unité : [(t, title, location, changements)].
    `changements` est une liste de chaînes décrivant update/diff/status/sidc.
    """
    out = []
    for st in sorted_states(unit):
        ch = []
        for tag in ("update", "diff"):
            blk = st.get(tag) or {}
            for kind, items in blk.items():
                ch.append(f"{tag}.{kind}: " +
                          ", ".join(f"{i['name']}={i.get('onHand')}" for i in items))
        if st.get("status"):
            ch.append(f"statut={st['status']}")
        if st.get("sidc"):
            ch.append("changement de symbole")
        out.append((st.get("t"), st.get("title"), st.get("location"), ch))
    return out


def scenario_events(orbat):
    """Événements globaux triés : [(startTime, title)]."""
    return sorted(((e.get("startTime"), e.get("title")) for e in orbat.get("events", []) or []),
                  key=lambda x: x[0] or "")


def vanished_elements(units):
    """
    Repère, parmi un itérable d'unités (ex. iter_units(orbat) ou subtree_units(root)),
    celles dont la DERNIÈRE entrée de state[] a `location: null`.

    Convention observée (confirmée par Florian sur « Opération Orage ») : quand une
    unité « mère » subit une perte (ex. un véhicule détruit) puis se décompose
    temporairement en plusieurs éléments suivis individuellement (escouades démontées,
    véhicules restants trackés à part), ces éléments enfants finissent typiquement par
    disparaître de la carte (`location: null`) au moment où ils se RÉEMBARQUENT / se
    REGROUPENT dans l'icône de l'unité mère — et non par destruction. La mère reprend
    alors sa propre timeline de position juste après.

    Pour distinguer d'une vraie perte : une perte se traduit par un `update`/`diff`
    NÉGATIF sur equipment/personnel (sur la mère ou l'élément lui-même), généralement
    AVANT ou AU déclenchement du détachement — pas par une simple disparition de
    position sans aucune variation de quantité associée.

    Renvoie la liste des unités concernées (chacune avec son `state` complet, à
    inspecter pour confirmer l'absence de perte associée).
    """
    out = []
    for u in units:
        sts = sorted_states(u)
        if sts and "location" in sts[-1] and sts[-1]["location"] is None:
            out.append(u)
    return out


# ---------------------------------------------------------------------------
# Nommage : indicateur de TOE vide et abréviations d'échelon (voir naming.md)
# ---------------------------------------------------------------------------
def mark_empty_subtrees(orbat, tag=" Ø"):
    """
    Suffixe `name` et `shortName` avec `tag` (par défaut " Ø", cf. naming.md
    Règle 3) sur toute unité dont le SOUS-ARBRE ENTIER (elle-même + toute sa
    descendance) ne porte ni `equipment` ni `personnel` nulle part.

    Condition stricte : une unité avec au moins une sous-unité non vide n'est
    PAS marquée, même si elle n'a rien en propre -- seuls les sous-arbres
    réellement et totalement vides le sont (calcul récursif post-ordre).

    À appeler en fin de construction (Tâche 4), après apply_word_substitutions
    le cas échéant, juste avant validate.py. Renvoie la liste des noms marqués.
    """
    def _is_empty(u):
        subs = u.get("subUnits") or []
        children_empty = [_is_empty(su) for su in subs]
        self_has_content = bool(u.get("equipment")) or bool(u.get("personnel"))
        subtree_empty = (not self_has_content) and all(children_empty)  # True aussi si pas d'enfants
        if subtree_empty:
            if not u.get("name", "").endswith(tag):
                u["name"] = (u.get("name") or "") + tag
            if u.get("shortName") and not u["shortName"].endswith(tag):
                u["shortName"] = u["shortName"] + tag
        return subtree_empty

    marked = []
    for side in orbat.get("sides", []):
        for g in side.get("groups", []) or []:
            for u in g.get("subUnits", []) or []:
                if _is_empty(u):
                    marked.append(u["name"])
        for u in side.get("units", []) or []:
            if u.get("name") and _is_empty(u):
                marked.append(u["name"])
    return marked


def apply_word_substitutions(orbat, subst_pairs, fields=("name", "shortName")):
    """
    Remplace, par mot entier (regex `\\b...\\b`), une liste de (pattern, remplacement)
    dans les champs choisis (par défaut name+shortName) de TOUTES les unités de
    l'ORBAT. Utilisé pour convertir des mots d'échelon d'une source externe vers
    une convention maison (cf. naming.md Règle 4).
    """
    import re
    for u in iter_units(orbat):
        for field in fields:
            val = u.get(field)
            if not val:
                continue
            for pattern, repl in subst_pairs:
                val = re.sub(pattern, repl, val)
            u[field] = val


# Table par défaut : mots d'échelon anglais (source Commonwealth/OTAN, formes
# pleines et déjà abrégées) -> acronymes /nomenclature-v4 (FR). Voir naming.md
# Règle 4 pour le piège FR/EN sur "Section" (échelon escouade ici, pas peloton)
# et le périmètre volontairement exclu (Team/Pair/Group/Crew).
ECHELON_WORD_SUBST_EN_TO_NOMV4 = [
    (r"\bBattalion\b", "BN"), (r"\bBn\b", "BN"),
    (r"\bCompany\b", "CIE"), (r"\bCoy\b", "CIE"),
    (r"\bPlatoon\b", "PLT"), (r"\bPlt\b", "PLT"),
    (r"\bTroop\b", "PLT"), (r"\bTp\b", "PLT"),
    (r"\bSection\b", "SQ"), (r"\bSect\b", "SQ"),
    (r"\bDetachment\b", "DET"), (r"\bDet\b", "DET"),
    (r"\bBattery\b", "BTE"), (r"\bBty\b", "BTE"),
]


if __name__ == "__main__":
    import sys
    o = load(sys.argv[1])
    print("name:", o.get("name"), "| version:", o.get("version"))
    print("unités:", sum(1 for _ in iter_units(o)))
    print("equipment catalog:", len(o.get("equipment", [])),
          "| personnel catalog:", len(o.get("personnel", [])))
