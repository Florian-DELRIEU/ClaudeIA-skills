#!/usr/bin/env python3
"""
aggregate.py — somme équipement / personnel / supplies d'un ORBAT,
sur la totalité OU une partie (sous-arbre), à l'état de BASE ou à un INSTANT donné.

Usage :
  python aggregate.py ORBAT.json                         # tout, base, les 3 catégories
  python aggregate.py ORBAT.json --kind equipment        # equipment seul
  python aggregate.py ORBAT.json --unit "1 CO"           # sous-arbre (nom ou id)
  python aggregate.py ORBAT.json --final                 # état FINAL (rejoue la timeline)
  python aggregate.py ORBAT.json --at 2024-01-30T01:00:00+01:00   # état à cette date
  python aggregate.py ORBAT.json --json                  # sortie machine

Base = champ `count` des unités. Avec --at/--final, on rejoue le state[] de chaque
unité (update = valeurs absolues `onHand`, diff = delta) jusqu'à l'instant voulu.
"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orbat_lib import (load, iter_units, find_unit, subtree_units,
                       aggregate, resource_at, catalog_map, RESOURCE_KINDS)


def aggregate_at(units, kind, t):
    """Somme les quantités de `kind` à l'instant t (None=final) sur les unités."""
    totals = {}
    for u in units:
        for name, q in resource_at(u, kind, t).items():
            totals[name] = totals.get(name, 0) + q
    return totals


def render(totals, cat, title):
    totals = {k: v for k, v in totals.items() if v}
    if not totals:
        return f"\n## {title}\n  (aucun)\n"
    width = max(len(n) for n in totals)
    lines = [f"\n## {title}  —  {sum(totals.values())} pièces, {len(totals)} types"]
    for name, n in sorted(totals.items(), key=lambda kv: (-kv[1], kv[0])):
        desc = cat.get(name, "")
        desc = f"  ({desc})" if desc else ""
        lines.append(f"  {name:<{width}}  {n:>6}{desc}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("orbat")
    ap.add_argument("--kind", choices=["equipment", "personnel", "supplies", "all"],
                    default="all")
    ap.add_argument("--unit", help="id ou nom (exact puis partiel) de la racine du sous-arbre")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--final", action="store_true", help="état final (rejoue la timeline)")
    g.add_argument("--at", help="état à cet instant ISO (ex. 2024-01-30T01:00:00+01:00)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    orbat = load(args.orbat)

    if args.unit:
        root = find_unit(orbat, args.unit)
        if root is None:
            sys.exit(f"Unite introuvable : {args.unit!r}")
        units = list(subtree_units(root))
        scope = f"{root.get('name')} (id={root.get('id')}) - {len(units)} unites"
    else:
        units = list(iter_units(orbat))
        scope = f"ORBAT complet << {orbat.get('name')} >> - {len(units)} unites"

    temporal = args.final or args.at
    t = args.at if args.at else None
    if args.final or args.at:
        scope += f"  [etat {'au ' + args.at if args.at else 'final'}]"

    kinds = list(RESOURCE_KINDS) if args.kind == "all" else [args.kind]
    result = {}
    for k in kinds:
        result[k] = aggregate_at(units, k, t) if temporal else aggregate(units, k)

    if args.json:
        print(json.dumps({"scope": scope, **result}, ensure_ascii=False, indent=1))
        return

    print(f"# Agregation - {scope}")
    labels = {"equipment": "EQUIPEMENT", "personnel": "PERSONNEL", "supplies": "SUPPLIES / MUNITIONS"}
    for k in kinds:
        print(render(result[k], catalog_map(orbat, k), labels[k]))


if __name__ == "__main__":
    main()
