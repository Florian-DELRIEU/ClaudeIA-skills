#!/usr/bin/env python3
"""Inspecte un fichier BSData (.cat/.gst/.ros ou .catz/.gstz/.rosz) et en donne un résumé.

Usage:
    python3 bs_inspect.py <fichier> [--ids] [--full]

Options:
    --ids   Affiche aussi un échantillon d'ids par section.
    --full  N'abrège pas les longues listes.

Objectif : comprendre un fichier AVANT de l'éditer. Affiche le type/namespace/version, les ids racine,
les profileTypes (avec l'id de chaque caractéristique — indispensable pour créer des profils
corrects), les costTypes, les catégories, et la liste des selectionEntry avec leurs profils/coûts.

Stdlib uniquement (xml.etree, zipfile). Les tags sont comparés sans namespace (local-name).
"""
import sys
import zipfile
import xml.etree.ElementTree as ET


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def load_root(path: str):
    """Retourne (root_element, source_namespace_uri)."""
    data = None
    if path.lower().endswith((".catz", ".gstz", ".rosz", ".bsr", ".bsi", ".zip")):
        with zipfile.ZipFile(path) as z:
            inner = [n for n in z.namelist() if n.lower().endswith((".cat", ".gst", ".ros", ".xml"))]
            if not inner:
                raise ValueError("Archive sans fichier XML BSData à l'intérieur.")
            data = z.read(inner[0])
    else:
        with open(path, "rb") as f:
            data = f.read()
    root = ET.fromstring(data)
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag[1:root.tag.index("}")]
    return root, ns


def children(el, name):
    """Enfants directs 'name' (sans namespace), en cherchant aussi via un conteneur pluriel."""
    out = [c for c in el if local(c.tag) == name]
    return out


def find_container(el, container):
    for c in el:
        if local(c.tag) == container:
            return c
    return None


def iter_all(el, name):
    for c in el.iter():
        if local(c.tag) == name:
            yield c


def summarize(path: str, show_ids: bool, full: bool) -> int:
    try:
        root, ns = load_root(path)
    except ET.ParseError as e:
        print(f"[XML MAL FORMÉ] {e}", file=sys.stderr)
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"[ERREUR] Impossible de lire {path} : {e}", file=sys.stderr)
        return 1

    rtype = local(root.tag)
    a = root.attrib
    print(f"Fichier      : {path}")
    print(f"Racine       : <{rtype}>")
    print(f"Namespace    : {ns or '(aucun)'}")
    print(f"Nom          : {a.get('name', '?')}")
    print(f"id           : {a.get('id', '?')}")
    print(f"revision     : {a.get('revision', '?')}   battleScribeVersion : {a.get('battleScribeVersion', '?')}")
    if rtype in ("catalogue", "roster"):
        print(f"gameSystemId : {a.get('gameSystemId', '?')}   gameSystemRevision : {a.get('gameSystemRevision', '?')}")
        print(f"library      : {a.get('library', '?')}")

    def section(title):
        print(f"\n--- {title} ---")

    # Ensemble de tous les ids (pour info)
    all_ids = [e.attrib["id"] for e in root.iter() if "id" in e.attrib]
    print(f"\nTotal éléments avec id : {len(all_ids)}  |  ids uniques : {len(set(all_ids))}")

    # profileTypes (crucial pour créer des profils)
    pts = list(iter_all(root, "profileType"))
    if pts:
        section(f"profileTypes ({len(pts)})")
        for pt in pts:
            cts = [c for c in pt.iter() if local(c.tag) == "characteristicType"]
            print(f"  • {pt.attrib.get('name','?')}  (typeId={pt.attrib.get('id','?')})")
            for ct in cts:
                print(f"      - {ct.attrib.get('name','?')}  (typeId={ct.attrib.get('id','?')})")

    # costTypes
    cts = list(iter_all(root, "costType"))
    if cts:
        section(f"costTypes ({len(cts)})")
        for ct in cts:
            print(f"  • {ct.attrib.get('name','?')}  (id={ct.attrib.get('id','?')})")

    # categoryEntries
    cats = list(iter_all(root, "categoryEntry"))
    if cats:
        section(f"categoryEntries ({len(cats)})")
        shown = cats if full else cats[:40]
        for c in shown:
            print(f"  • {c.attrib.get('name','?')}  (id={c.attrib.get('id','?')})")
        if not full and len(cats) > len(shown):
            print(f"  … +{len(cats) - len(shown)} autres (--full pour tout voir)")

    # forceEntries
    fes = [e for e in iter_all(root, "forceEntry")]
    if fes:
        section(f"forceEntries ({len(fes)})")
        for fe in (fes if full else fes[:30]):
            print(f"  • {fe.attrib.get('name','?')}  (id={fe.attrib.get('id','?')})")

    # selectionEntries (avec profils + coûts)
    ses = [e for e in iter_all(root, "selectionEntry")]
    if ses:
        section(f"selectionEntry ({len(ses)})")
        shown = ses if full else ses[:40]
        for se in shown:
            name = se.attrib.get("name", "?")
            typ = se.attrib.get("type", "?")
            # coût direct
            costs = []
            cc = find_container(se, "costs")
            if cc is not None:
                for cost in cc:
                    if local(cost.tag) == "cost":
                        costs.append(f"{cost.attrib.get('value','?')} {cost.attrib.get('name','?')}")
            # profils directs
            profs = []
            pc = find_container(se, "profiles")
            if pc is not None:
                for p in pc:
                    if local(p.tag) == "profile":
                        profs.append(p.attrib.get("typeName", "?"))
            cost_s = ("  [" + ", ".join(costs) + "]") if costs else ""
            prof_s = ("  {" + ", ".join(profs) + "}") if profs else ""
            ids = f"  (id={se.attrib.get('id','?')})" if show_ids else ""
            print(f"  • [{typ}] {name}{cost_s}{prof_s}{ids}")
        if not full and len(ses) > len(shown):
            print(f"  … +{len(ses) - len(shown)} autres (--full pour tout voir)")

    # rosters : forces + total
    if rtype == "roster":
        forces = [e for e in iter_all(root, "force")]
        section(f"forces ({len(forces)})")
        for fo in forces:
            print(f"  • {fo.attrib.get('name','?')}  (catalogue={fo.attrib.get('catalogueName','?')})")

    print()
    return 0


def main() -> int:
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    flags = {x for x in sys.argv[1:] if x.startswith("--")}
    if not args:
        print(__doc__)
        return 2
    return summarize(args[0], show_ids="--ids" in flags, full="--full" in flags)


if __name__ == "__main__":
    raise SystemExit(main())
