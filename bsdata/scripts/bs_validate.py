#!/usr/bin/env python3
"""Valide un fichier ou un dossier BSData pour un chargement SANS ERREUR dans BattleScribe / New Recruit.

Usage:
    python3 bs_validate.py <fichier.cat|.gst|.ros|.catz|...>
    python3 bs_validate.py <dossier/>        # résout les références croisées .gst <-> .cat

Contrôles :
  1. XML bien formé (numéro de ligne si erreur).
  2. Racine + namespace cohérents avec le type de fichier.
  3. ids uniques (doublons signalés).
  4. Références résolues : targetId, childId, typeId (profil/caractéristique/coût), gameSystemId,
     publicationId, entryId/entryGroupId, catalogueId, defaultSelectionEntryId.
  5. Caractéristiques rattachées à un profileType valide (orphelines signalées).
  6. Coûts liés à un costType existant.
  7. Une seule categoryLink primaire par selectionEntry racine.

Niveaux : [ERREUR] bloquant · [EXTERNE] à confirmer en mode dossier · [ALERTE] non bloquant · [OK].
Code de sortie ≠ 0 s'il reste au moins un [ERREUR].

Stdlib uniquement. Comparaison des tags par local-name (sans namespace).
"""
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

NS_BY_ROOT = {
    "gameSystem": "http://www.battlescribe.net/schema/gameSystemSchema",
    "catalogue": "http://www.battlescribe.net/schema/catalogueSchema",
    "roster": "http://www.battlescribe.net/schema/rosterSchema",
    "dataIndex": "http://www.battlescribe.net/schema/dataIndexSchema",
}

# Valeurs "mot-clé" de childId/scope qui ne sont PAS des ids à résoudre.
CHILDID_KEYWORDS = {
    "unit", "model", "upgrade", "any", "anything", "roster", "force", "self",
    "parent", "primary-catalogue", "primary-category", "ancestor",
}

XML_EXT = (".cat", ".gst", ".ros")
ZIP_EXT = (".catz", ".gstz", ".rosz", ".bsr", ".bsi")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_bytes(path: str) -> bytes:
    if path.lower().endswith(ZIP_EXT + (".zip",)):
        with zipfile.ZipFile(path) as z:
            inner = [n for n in z.namelist() if n.lower().endswith(XML_EXT + (".xml",))]
            if not inner:
                raise ValueError("Archive sans fichier XML BSData.")
            return z.read(inner[0])
    with open(path, "rb") as f:
        return f.read()


class FileModel:
    """Données extraites d'un fichier, pour analyse locale et croisée."""

    def __init__(self, path):
        self.path = path
        self.root = None
        self.ns = ""
        self.rtype = ""
        self.parse_error = None
        self.ids = []                 # liste (id, tag, name) pour doublons
        self.id_set = set()
        self.profiletypes = {}        # id -> set(characteristicType ids)
        self.costtype_ids = set()
        self.parent = {}              # child -> parent (pour contexte)
        self.refs = []                # (attr, value, tag, name, kind)

    def load(self):
        try:
            data = read_bytes(self.path)
        except Exception as e:  # noqa: BLE001
            self.parse_error = f"lecture impossible : {e}"
            return
        try:
            self.root = ET.fromstring(data)
        except ET.ParseError as e:
            self.parse_error = f"XML mal formé : {e}"
            return
        self.rtype = local(self.root.tag)
        if self.root.tag.startswith("{"):
            self.ns = self.root.tag[1:self.root.tag.index("}")]
        # parent map
        for p in self.root.iter():
            for c in p:
                self.parent[c] = p
        # ids
        for el in self.root.iter():
            i = el.attrib.get("id")
            if i is not None:
                self.ids.append((i, local(el.tag), el.attrib.get("name", "")))
                self.id_set.add(i)
        # profileTypes registry
        for pt in self.root.iter():
            if local(pt.tag) == "profileType" and "id" in pt.attrib:
                chset = {c.attrib["id"] for c in pt.iter()
                         if local(c.tag) == "characteristicType" and "id" in c.attrib}
                self.profiletypes[pt.attrib["id"]] = chset
            if local(pt.tag) == "costType" and "id" in pt.attrib:
                self.costtype_ids.add(pt.attrib["id"])
        # references
        self._collect_refs()

    def _collect_refs(self):
        for el in self.root.iter():
            tag = local(el.tag)
            name = el.attrib.get("name", "")
            a = el.attrib
            for attr in ("targetId", "publicationId", "entryId", "entryGroupId",
                         "catalogueId", "defaultSelectionEntryId", "gameSystemId"):
                if attr in a and a[attr]:
                    self.refs.append((attr, a[attr], tag, name, attr))
            # childId (condition/repeat) sauf mots-clés
            if "childId" in a and a["childId"] and a["childId"] not in CHILDID_KEYWORDS:
                self.refs.append(("childId", a["childId"], tag, name, "childId"))
            # typeId : dépend du parent élément
            if "typeId" in a and a["typeId"]:
                if tag == "profile":
                    self.refs.append(("typeId", a["typeId"], tag, name, "profileType"))
                elif tag == "characteristic":
                    self.refs.append(("typeId", a["typeId"], tag, name, "characteristicType"))
                elif tag == "cost":
                    self.refs.append(("typeId", a["typeId"], tag, name, "costType"))
                else:
                    self.refs.append(("typeId", a["typeId"], tag, name, "typeId"))


def gather_files(target):
    if os.path.isdir(target):
        out = []
        for dirpath, _dirs, files in os.walk(target):
            for fn in files:
                if fn.lower().endswith(XML_EXT + ZIP_EXT):
                    out.append(os.path.join(dirpath, fn))
        return sorted(out)
    return [target]


def validate(target) -> int:
    files = gather_files(target)
    if not files:
        print("Aucun fichier BSData trouvé.", file=sys.stderr)
        return 2

    models = []
    for f in files:
        m = FileModel(f)
        m.load()
        models.append(m)

    # ensembles globaux (résolution croisée)
    global_ids = set()
    global_pt = {}
    global_costtypes = set()
    for m in models:
        global_ids |= m.id_set
        global_pt.update(m.profiletypes)
        global_costtypes |= m.costtype_ids

    dir_mode = os.path.isdir(target)
    n_err = 0
    n_ext = 0
    n_alert = 0

    for m in models:
        print("=" * 70)
        print(f"Fichier : {m.path}")
        if m.parse_error:
            print(f"  [ERREUR] {m.parse_error}")
            n_err += 1
            continue

        # 2. racine + namespace
        expected_ns = NS_BY_ROOT.get(m.rtype)
        if expected_ns is None:
            print(f"  [ERREUR] Racine <{m.rtype}> inconnue (attendu : {', '.join(NS_BY_ROOT)}).")
            n_err += 1
        elif m.ns != expected_ns:
            print(f"  [ERREUR] Namespace incohérent pour <{m.rtype}>.")
            print(f"           trouvé  : {m.ns or '(aucun)'}")
            print(f"           attendu : {expected_ns}")
            n_err += 1
        else:
            print(f"  [OK] Racine <{m.rtype}> et namespace cohérents.")

        # 3. doublons d'id (dans le fichier)
        seen = {}
        dups = []
        for i, tag, name in m.ids:
            if i in seen:
                dups.append((i, tag, name))
            else:
                seen[i] = (tag, name)
        if dups:
            for i, tag, name in dups:
                print(f"  [ERREUR] id dupliqué : {i}  (<{tag}> '{name}')")
                n_err += 1
        else:
            print(f"  [OK] {len(m.id_set)} ids, aucun doublon interne.")

        # 4. références
        local_ids = m.id_set
        unresolved_here = 0
        for attr, val, tag, name, kind in m.refs:
            in_local = val in local_ids
            in_global = val in global_ids
            if in_local:
                continue
            # même-fichier obligatoire
            if kind == "defaultSelectionEntryId":
                print(f"  [ERREUR] {attr}='{val}' introuvable dans le fichier (<{tag}> '{name}').")
                n_err += 1
                continue
            if dir_mode:
                if in_global:
                    continue  # résolu ailleurs dans le repo
                print(f"  [ERREUR] Référence non résolue dans tout le repo : {attr}='{val}' "
                      f"(<{tag}> '{name}').")
                n_err += 1
            else:
                # fichier isolé : peut être défini dans le .gst / un autre .cat
                print(f"  [EXTERNE] {attr}='{val}' non trouvé dans ce fichier (<{tag}> '{name}') "
                      f"— vérifier en mode dossier.")
                n_ext += 1
                unresolved_here += 1

        # 5. caractéristiques orphelines + typeId de profil valide
        for pf in m.root.iter():
            if local(pf.tag) != "profile":
                continue
            pt_id = pf.attrib.get("typeId")
            if not pt_id:
                continue
            registry = global_pt if dir_mode else m.profiletypes
            if pt_id in registry:
                allowed = registry[pt_id]
                for ch in pf.iter():
                    if local(ch.tag) == "characteristic":
                        ct = ch.attrib.get("typeId")
                        if ct and ct not in allowed:
                            print(f"  [ALERTE] caractéristique orpheline '{ch.attrib.get('name','?')}'"
                                  f" (typeId={ct}) hors du profileType '{pf.attrib.get('typeName','?')}'"
                                  f" du profil '{pf.attrib.get('name','?')}'.")
                            n_alert += 1
            elif pt_id in (global_ids if dir_mode else m.id_set):
                print(f"  [ALERTE] profil '{pf.attrib.get('name','?')}' : typeId={pt_id} "
                      f"ne pointe pas vers un profileType.")
                n_alert += 1
            # sinon : typeId externe/non résolu, déjà signalé en §4

        # 6. coûts sans costType
        pool = global_costtypes if dir_mode else m.costtype_ids
        for cst in m.root.iter():
            if local(cst.tag) == "cost":
                ti = cst.attrib.get("typeId")
                if ti and ti not in pool:
                    lvl = "[ERREUR]" if dir_mode else "[EXTERNE]"
                    print(f"  {lvl} coût '{cst.attrib.get('name','?')}' : costType '{ti}' introuvable"
                          + ("." if dir_mode else " dans ce fichier."))
                    if dir_mode:
                        n_err += 1
                    else:
                        n_ext += 1

        # 7. categoryLink primaire des selectionEntry racine
        if m.rtype in ("gameSystem", "catalogue"):
            for cont in m.root:
                if local(cont.tag) != "selectionEntries":
                    continue
                for se in cont:
                    if local(se.tag) != "selectionEntry":
                        continue
                    prim = 0
                    for sub in se:
                        if local(sub.tag) == "categoryLinks":
                            for cl in sub:
                                if local(cl.tag) == "categoryLink" and cl.attrib.get("primary") == "true":
                                    prim += 1
                    if prim == 0:
                        print(f"  [ALERTE] selectionEntry racine '{se.attrib.get('name','?')}' "
                              f"sans categoryLink primaire (primary=\"true\").")
                        n_alert += 1
                    elif prim > 1:
                        print(f"  [ALERTE] selectionEntry racine '{se.attrib.get('name','?')}' "
                              f"a {prim} categoryLink primaires (une seule attendue).")
                        n_alert += 1

    # bilan
    print("=" * 70)
    print(f"BILAN : {n_err} erreur(s) · {n_ext} référence(s) externe(s) à confirmer · {n_alert} alerte(s).")
    if n_err:
        print("→ Corriger les [ERREUR] avant de rendre le fichier.")
    elif n_ext and not dir_mode:
        print("→ Aucune erreur bloquante. Relancer sur le DOSSIER pour lever les [EXTERNE].")
    else:
        print("→ Aucune erreur bloquante détectée.")
    return 1 if n_err else 0


def main() -> int:
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    return validate(args[0])


if __name__ == "__main__":
    raise SystemExit(main())
