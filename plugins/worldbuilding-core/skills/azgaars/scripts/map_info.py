#!/usr/bin/env python3
"""Résumé rapide d'une sauvegarde .map d'Azgaar's FMG.

Usage:
    python3 map_info.py <fichier.map> [--json] [--states] [--burgs N] [--regiments] [--economy]
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from azgaar_lib import AzgaarMap


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    path = args[0]
    m = AzgaarMap.load(path)

    if "--json" in args:
        print(json.dumps(m.summary(), ensure_ascii=False, indent=2))
    else:
        for k, v in m.summary().items():
            if isinstance(v, dict):
                print(f"{k:>16} :")
                for k2, v2 in v.items():
                    print(f"{'':>16}   {k2}: {v2}")
            else:
                print(f"{k:>16} : {v}")

    if "--states" in args:
        print("\n--- ÉTATS ---")
        for s in m.states:
            if not s or s.get("removed"):
                continue
            pop = m.real_population(s.get("urban", 0) + s.get("rural", 0))
            mil = len(s.get("military", []))
            print(f"[{s['i']:>2}] {s.get('fullName') or s['name']:<40} "
                  f"pop≈{pop:>12,} burgs={s.get('burgs', 0):>3} régiments={mil}")

    if "--burgs" in args:
        n = int(args[args.index("--burgs") + 1]) if len(args) > args.index("--burgs") + 1 else 20
        print(f"\n--- {n} PLUS GRANDS BURGS ---")
        burgs = [b for b in m.burgs if b and not b.get("removed")]
        burgs.sort(key=lambda b: -b.get("population", 0))
        states = m.states
        for b in burgs[:n]:
            cap = "★" if b.get("capital") else " "
            state = states[b["state"]]["name"] if b.get("state") is not None else "?"
            print(f"{cap} {b['name']:<25} pop≈{m.real_population(b['population']):>10,}  ({state})")

    if "--regiments" in args:
        print("\n--- RÉGIMENTS ---")
        for r in m.regiments():
            units = " ".join(f"{k}:{v}" for k, v in r.get("u", {}).items() if v)
            print(f"[{r['stateName']}] {r['name']:<35} {units}")

    if "--economy" in args:
        if not m.has_economy:
            print(f"\n(Pas de module économie : carte en {m.n_blocks} blocs, "
                  f"économie disponible en 46 blocs / FMG v1.13x+.)")
        else:
            print("\n--- BIENS (goods) ---")
            for g in m.goods:
                tags = ",".join(g.get("tags", []))
                print(f"[{g['i']:>2}] {g['name']:<18} valeur={g.get('value','?'):<4} {tags}")
            print(f"\nMarchés : {len(m.markets)} | Transactions : {len(m.trades)} | "
                  f"Soulèvements : {len(m.rebels)}")


if __name__ == "__main__":
    main()
