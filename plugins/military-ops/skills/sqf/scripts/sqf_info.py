#!/usr/bin/env python3
"""
sqf_info.py — Inspection rapide (lecture seule) d'une sauvegarde SQF.

Usage :
  python3 sqf_info.py save.sqf                 # vue d'ensemble
  python3 sqf_info.py save.sqf --inventory     # comptage par classe (vehicules/unites)
  python3 sqf_info.py save.sqf --vehicles      # liste des vehicules
  python3 sqf_info.py save.sqf --units         # liste des unites
  python3 sqf_info.py save.sqf --objects 30    # 30 premiers objets (pos/fuel/damage)
  python3 sqf_info.py save.sqf --markers 40    # 40 premiers marqueurs
  python3 sqf_info.py save.sqf --check         # controle de coherence
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sqf_lib import SqfSave


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--inventory", action="store_true")
    ap.add_argument("--vehicles", action="store_true")
    ap.add_argument("--units", action="store_true")
    ap.add_argument("--objects", nargs="?", const=20, type=int)
    ap.add_argument("--markers", nargs="?", const=20, type=int)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    s = SqfSave.load(a.file)
    print(f"== {os.path.basename(a.file)} ==")
    for k, v in s.summary().items():
        print(f"  {k:10}: {v}")

    if a.inventory:
        print("\n-- Vehicules par classe --")
        for cls, n in s.classname_counts("vehicle").most_common():
            print(f"  {n:4}  {cls}")
        print("-- Unites par classe --")
        for cls, n in s.classname_counts("unit").most_common():
            print(f"  {n:4}  {cls}")

    if a.vehicles or a.units:
        want = "vehicle" if a.vehicles else "unit"
        print(f"\n-- {want}s --")
        for o in s.objects():
            if o["kind"] == want:
                extra = f" fuel={o['fuel']}" if o["fuel"] is not None else ""
                extra += f" dmg={o['damage']}" if o["damage"] else ""
                print(f"  _object{o['id']:<4} {o['classname']:<34} pos={o['pos']}{extra}")

    if a.objects:
        print(f"\n-- {a.objects} premiers objets --")
        for o in s.objects()[:a.objects]:
            print(f"  _object{o['id']:<4} [{o['kind']:7}] {o['classname']:<34} pos={o['pos']}")

    if a.markers is not None:
        names = s.marker_names()
        print(f"\n-- marqueurs ({len(names)}), {a.markers} premiers --")
        for nm in names[:a.markers]:
            print(f"  {nm}")

    if a.check:
        print("\n-- controle --")
        probs = s.check()
        if not probs:
            print("  OK : aucune reference pendante, brackets equilibres")
        else:
            for p in probs:
                print(f"  [!] {p}")


if __name__ == "__main__":
    main()
