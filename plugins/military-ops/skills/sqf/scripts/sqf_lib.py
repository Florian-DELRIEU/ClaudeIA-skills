"""
sqf_lib.py — Lecture et edition des sauvegardes SQF d'Arma 3
(format "Export to SQF" de l'editeur 3DEN / BIS_fnc_3DENExportSQF).

Philosophie : FIDELITE ROUND-TRIP. Le fichier est garde comme une liste de
lignes brutes. Les editions sont chirurgicales (remplacement / insertion /
suppression de lignes ciblees) ; tout le reste est preserve octet pour octet.
On ne "reserialise" jamais un bloc entier a partir d'un modele.

Format cible (une sauvegarde = un script SQF plat, ASCII, fins de ligne CRLF) :
  _groupN = createGroup [side, true];
  _objectN = createVehicle ["Classe", [0,0,0], [], 0, "CAN_COLLIDE"];   (vehicule/statique)
  _objectN = _groupM createUnit ["Classe", ...];                        (infanterie)
  _marker  = createMarkerLocal ["nom", [x,y,z]];
  _waypoint = [_groupN, i]  /  _groupN addWaypoint [...]
  ... puis config de groupe, waypoints, moveIn*, attachTo.

Reference detaillee du format : ../reference/format.md
"""

from __future__ import annotations
import re
import shutil
from collections import Counter, OrderedDict

CRLF = "\r\n"

# --- Ouvertures de "blocs de definition" -------------------------------------
_RE_GROUP_DEF  = re.compile(r'^_group(\d+)\s*=\s*createGroup\b')
_RE_OBJECT_DEF = re.compile(r'^_object(\d+)\s*=\s')
_RE_MARKER_DEF = re.compile(r'^_marker\s*=\s*createMarkerLocal\s*\[\s*"([^"]*)"')
_RE_WP_DEF     = re.compile(r'^_waypoint\s*=\s')

# --- Champs d'un objet --------------------------------------------------------
_RE_VEH_CLASS  = re.compile(r'^_object\d+\s*=\s*createVehicle\s*\[\s*"([^"]*)"')
_RE_UNIT_CLASS = re.compile(r'^_object\d+\s*=\s*_group(\d+)\s+createUnit\s*\[\s*"([^"]*)"')
_RE_POSASL     = re.compile(r'^(_object\d+ setPosASL )\[[^\]]*\](;?)\s*$')
_RE_FUEL       = re.compile(r'^(_object\d+ setFuel )([0-9.eE+-]+)(;?)\s*$')
_RE_DAMAGE     = re.compile(r'^(_object\d+ setDamage )([0-9.eE+-]+)(;?)\s*$')
_RE_HITINDEX   = re.compile(r'^(\{_object\d+ setHitIndex \[_forEachIndex, _x, false\]\} forEach )\[([^\]]*)\](;?)\s*$')


def _tok(handle: str) -> re.Pattern:
    """Regex mot-entier pour un handle (_object12 ne matche pas _object120)."""
    return re.compile(r'(?<![\w])' + re.escape(handle) + r'(?![\w])')


class SqfSave:
    def __init__(self, lines, newline=CRLF):
        self.lines = lines          # liste de str SANS fin de ligne
        self.newline = newline

    # ----- E/S ---------------------------------------------------------------
    @classmethod
    def load(cls, path):
        with open(path, "rb") as f:
            raw = f.read()
        text = raw.decode("utf-8-sig")      # tolere un BOM eventuel
        newline = CRLF if "\r\n" in text else "\n"
        # split sur le vrai separateur : ".join" reconstruit a l'identique
        lines = text.split(newline)
        return cls(lines, newline)

    def dumps(self) -> str:
        return self.newline.join(self.lines)

    def save(self, path):
        with open(path, "wb") as f:
            f.write(self.dumps().encode("utf-8"))

    @staticmethod
    def open_copy(src, dst):
        """Copie src -> dst puis charge la copie (ne jamais editer l'upload)."""
        shutil.copyfile(src, dst)
        return SqfSave.load(dst)

    # ----- Index des ouvertures ---------------------------------------------
    def _openings(self):
        """Liste ordonnee (idx_ligne, kind, id) de tous les ouvreurs de bloc."""
        out = []
        for i, ln in enumerate(self.lines):
            m = _RE_OBJECT_DEF.match(ln)
            if m:
                out.append((i, "object", int(m.group(1)))); continue
            m = _RE_GROUP_DEF.match(ln)
            if m:
                out.append((i, "group", int(m.group(1)))); continue
            m = _RE_MARKER_DEF.match(ln)
            if m:
                out.append((i, "marker", m.group(1))); continue
            if _RE_WP_DEF.match(ln):
                out.append((i, "waypoint", None))
        return out

    def block_range(self, kind, ident):
        """(start, end) exclusif des lignes du bloc de DEFINITION.
        Le bloc va de l'ouvreur jusqu'a l'ouvreur suivant (quel qu'il soit)."""
        ops = self._openings()
        for n, (i, k, idv) in enumerate(ops):
            if k == kind and idv == ident:
                end = ops[n + 1][0] if n + 1 < len(ops) else len(self.lines)
                return i, end
        return None

    # ----- Inventaires -------------------------------------------------------
    def object_ids(self):
        return sorted({int(m.group(1)) for ln in self.lines
                       if (m := _RE_OBJECT_DEF.match(ln))})

    def group_ids(self):
        return sorted({int(m.group(1)) for ln in self.lines
                       if (m := _RE_GROUP_DEF.match(ln))})

    def marker_names(self):
        return [m.group(1) for ln in self.lines if (m := _RE_MARKER_DEF.match(ln))]

    def objects(self):
        """Liste de dicts : id, kind(vehicle|unit), classname, group, pos, fuel, damage."""
        res = []
        for oid in self.object_ids():
            rng = self.block_range("object", oid)
            block = self.lines[rng[0]:rng[1]]
            head = block[0]
            um = _RE_UNIT_CLASS.match(head)
            if um:
                kind, cls_, grp = "unit", um.group(2), int(um.group(1))
            else:
                vm = _RE_VEH_CLASS.match(head)
                kind, cls_, grp = "vehicle", (vm.group(1) if vm else "?"), None
            pos = fuel = dmg = None
            for ln in block:
                if (m := _RE_POSASL.match(ln)):
                    pos = ln[m.end(1):].rstrip(";").strip()
                elif (m := _RE_FUEL.match(ln)):
                    fuel = float(m.group(2))
                elif (m := _RE_DAMAGE.match(ln)):
                    dmg = float(m.group(2))
            res.append(dict(id=oid, kind=kind, classname=cls_, group=grp,
                            pos=pos, fuel=fuel, damage=dmg))
        return res

    def classname_counts(self, kind=None):
        c = Counter()
        for o in self.objects():
            if kind is None or o["kind"] == kind:
                c[o["classname"]] += 1
        return c

    def summary(self):
        objs = self.objects()
        veh = [o for o in objs if o["kind"] == "vehicle"]
        uni = [o for o in objs if o["kind"] == "unit"]
        return OrderedDict(
            groups=len(self.group_ids()),
            objects=len(objs),
            vehicles=len(veh),
            units=len(uni),
            markers=len(self.marker_names()),
            waypoints=sum(1 for ln in self.lines if _RE_WP_DEF.match(ln)),
            moveIn=sum(1 for ln in self.lines if re.search(r'\bmoveIn[A-Za-z]*\b', ln)),
            attachTo=sum(1 for ln in self.lines if re.search(r'\battachTo\b', ln)),
            lines=len(self.lines),
            newline="CRLF" if self.newline == CRLF else "LF",
        )

    # ----- Editions ----------------------------------------------------------
    def set_fuel(self, oid, level):
        rng = self.block_range("object", oid)
        if not rng:
            return False
        for i in range(*rng):
            m = _RE_FUEL.match(self.lines[i])
            if m:
                self.lines[i] = f"{m.group(1)}{level:g}{m.group(3)}"
                return True
        return False

    def set_damage(self, oid, level):
        rng = self.block_range("object", oid)
        if not rng:
            return False
        done = False
        for i in range(*rng):
            m = _RE_DAMAGE.match(self.lines[i])
            if m:
                self.lines[i] = f"{m.group(1)}{level:g}{m.group(3)}"; done = True
            hm = _RE_HITINDEX.match(self.lines[i])
            if hm and level == 0:
                n = len(hm.group(2).split(","))
                zeros = ",".join(["0"] * n)
                self.lines[i] = f"{hm.group(1)}[{zeros}]{hm.group(3)}"; done = True
        return done

    def set_pos(self, oid, pos):
        """pos = [x,y,z] (liste/tuple). Remplace la ligne setPosASL de l'objet."""
        rng = self.block_range("object", oid)
        if not rng:
            return False
        val = "[" + ",".join(f"{v:g}" for v in pos) + "]"
        for i in range(*rng):
            m = _RE_POSASL.match(self.lines[i])
            if m:
                self.lines[i] = f"{m.group(1)}{val}{m.group(2)}"
                return True
        return False

    def refuel_all(self, level=1.0):
        """Fait le plein de tous les vehicules possedant deja une ligne setFuel."""
        n = 0
        for i, ln in enumerate(self.lines):
            m = _RE_FUEL.match(ln)
            if m:
                self.lines[i] = f"{m.group(1)}{level:g}{m.group(3)}"; n += 1
        return n

    def repair_all(self):
        """Met setDamage a 0 et zero-remplit tous les setHitIndex."""
        n = 0
        for i, ln in enumerate(self.lines):
            m = _RE_DAMAGE.match(ln)
            if m and float(m.group(2)) != 0:
                self.lines[i] = f"{m.group(1)}0{m.group(3)}"; n += 1
                continue
            hm = _RE_HITINDEX.match(ln)
            if hm:
                cnt = len(hm.group(2).split(","))
                zeros = ",".join(["0"] * cnt)
                if hm.group(2).replace(" ", "") != zeros:
                    self.lines[i] = f"{hm.group(1)}[{zeros}]{hm.group(3)}"; n += 1
        return n

    def references_to(self, handle):
        """Indices de lignes citant `handle` HORS de son bloc de definition."""
        rng = None
        if handle.startswith("_object"):
            rng = self.block_range("object", int(handle[7:]))
        tok = _tok(handle)
        idx = []
        for i, ln in enumerate(self.lines):
            if rng and rng[0] <= i < rng[1]:
                continue
            if tok.search(ln):
                idx.append(i)
        return idx

    def remove_object(self, oid):
        """Supprime le bloc de l'objet ET toutes les lignes qui le referencent
        (moveIn*, attachTo, selectLeader, setCurrentWaypoint, etc.)."""
        handle = f"_object{oid}"
        rng = self.block_range("object", oid)
        if not rng:
            return 0
        to_del = set(range(*rng)) | set(self.references_to(handle))
        self.lines = [ln for i, ln in enumerate(self.lines) if i not in to_del]
        return len(to_del)

    # ----- Fusion ------------------------------------------------------------
    def renumber(self, obj_offset=0, grp_offset=0, marker_suffix=""):
        """Decale tous les _objectN/_groupN et suffixe les noms de marqueurs.
        Applique du plus grand au plus petit id pour eviter les collisions."""
        if obj_offset:
            for oid in sorted(self.object_ids(), reverse=True):
                self._rename_handle(f"_object{oid}", f"_object{oid + obj_offset}")
        if grp_offset:
            for gid in sorted(self.group_ids(), reverse=True):
                self._rename_handle(f"_group{gid}", f"_group{gid + grp_offset}")
        if marker_suffix:
            for i, ln in enumerate(self.lines):
                m = _RE_MARKER_DEF.match(ln)
                if m:
                    old = m.group(1)
                    self.lines[i] = ln.replace(f'"{old}"', f'"{old}{marker_suffix}"', 1)

    def _rename_handle(self, old, new):
        tok = _tok(old)
        self.lines = [tok.sub(new, ln) for ln in self.lines]

    def concat(self, other):
        """Ajoute le contenu d'une autre sauvegarde (deja renumerotee)."""
        if self.lines and self.lines[-1] != "":
            self.lines.append("")
        self.lines.extend(other.lines)

    # ----- Controles ---------------------------------------------------------
    def check(self):
        """Verifie l'absence de references pendantes et l'equilibre des accolades."""
        problems = []
        defined_obj = {f"_object{i}" for i in self.object_ids()}
        defined_grp = {f"_group{i}" for i in self.group_ids()}
        used_obj = set(re.findall(r'_object\d+', self.dumps()))
        used_grp = set(re.findall(r'_group\d+', self.dumps()))
        for h in sorted(used_obj - defined_obj):
            problems.append(f"reference pendante vers {h} (jamais defini)")
        for h in sorted(used_grp - defined_grp):
            problems.append(f"reference pendante vers {h} (jamais defini)")
        txt = self.dumps()
        # equilibre grossier (hors chaines) : approximatif, signal seulement
        if txt.count("[") != txt.count("]"):
            problems.append(f"crochets desequilibres ([ {txt.count('[')} vs ] {txt.count(']')})")
        if txt.count("{") != txt.count("}"):
            problems.append(f"accolades desequilibrees ({{ {txt.count('{')} vs }} {txt.count('}')})")
        return problems
