#!/usr/bin/env python3
"""
timeline.py — lit un scénario ORBAT (avec state[]) comme un récit chronologique.

Usage :
  python timeline.py ORBAT.json                 # événements globaux + unités actives
  python timeline.py ORBAT.json --unit "1 CO"   # journal détaillé d'une unité + sous-arbre
  python timeline.py ORBAT.json --events        # seulement les événements globaux

Affiche les events globaux (champ events[]) et, pour une unité donnée, sa timeline
(positions, titres narratifs, changements de ressources/statut/symbole), ainsi que les
éléments détachés temporairement (escouades démontées, véhicules trackés isolément)
détectés dans son sous-arbre — voir orbat_lib.vanished_elements.
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orbat_lib import (load, iter_units, find_unit, subtree_units, scenario_events,
                       unit_timeline, sorted_states, vanished_elements, base_resources)


def describe_vanished(orbat, elements, root):
    """Affiche les éléments disparus (location:null) avec leur diagnostic."""
    if not elements:
        return
    print("## Éléments détachés dont le suivi s'arrête (location: null)")
    print("   (par défaut : probable réembarquement/regroupement dans l'unité mère —")
    print("    voir si une perte equipment/personnel est enregistrée au même moment)\n")
    SYMSET_KIND = {"15": "véhicule/équipement isolé", "10": "unité/escouade",
                   "11": "unité civile", "20": "installation"}
    for e in elements:
        sts = sorted_states(e)
        sidc = e.get("sidc") or ""
        kind = SYMSET_KIND.get(sidc[4:6], "élément") if len(sidc) >= 6 else "élément"
        print(f"  - {e.get('name') or '(sans nom)'}  [{kind}, sidc={sidc}]")
        print(f"      actif de {sts[0].get('t')} à {sts[-1].get('t')}"
              f"  ({len(sts)} états)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("orbat")
    ap.add_argument("--unit", help="id ou nom d'une unité pour son journal détaillé")
    ap.add_argument("--events", action="store_true", help="seulement les événements globaux")
    args = ap.parse_args()
    orbat = load(args.orbat)

    print(f"# Scénario : {orbat.get('name')}  (départ {orbat.get('startTime')})\n")

    evs = scenario_events(orbat)
    if evs:
        print("## Événements globaux")
        for t, title in evs:
            print(f"  {t}  {title}")
        print()
    if args.events:
        return

    if args.unit:
        u = find_unit(orbat, args.unit)
        if u is None:
            sys.exit(f"Unité introuvable : {args.unit!r}")
        print(f"## Journal — {u.get('name')} (id={u.get('id')})")
        for t, title, loc, changes in unit_timeline(u):
            pos = f"@[{loc[0]:.4f},{loc[1]:.4f}]" if loc else ""
            head = f"  {t}  {pos}"
            if title:
                head += f"  « {title} »"
            print(head)
            for c in changes:
                print(f"        - {c}")
        print()
        vanished = vanished_elements(subtree_units(u))
        describe_vanished(orbat, vanished, u)
        return

    # Vue d'ensemble : unités ayant une timeline, triées par 1er horodatage
    active = []
    for u in iter_units(orbat):
        sts = sorted_states(u)
        if sts:
            active.append((sts[0]["t"], sts[-1]["t"], len(sts), u.get("name")))
    active.sort()
    print(f"## Unités avec timeline ({len(active)})")
    for t0, t1, n, name in active:
        print(f"  {name:<40} {n:>3} états  {t0} → {t1}")
    print()
    vanished = vanished_elements(iter_units(orbat))
    describe_vanished(orbat, vanished, None)


if __name__ == "__main__":
    main()
