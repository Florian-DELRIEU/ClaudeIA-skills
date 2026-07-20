#!/usr/bin/env python3
"""Extrait des collections d'une sauvegarde .map vers un fichier JSON.

Usage:
    python3 extract.py <fichier.map> <collection> [sortie.json]

Collections (tous formats) : states, burgs, cultures, religions, provinces,
    rivers, markers, routes, zones, notes, features, regiments, options, all
Collections économie (cartes 46 blocs, FMG v1.13x+) : goods, markets, trades,
    rebels, ice
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from azgaar_lib import AzgaarMap

COLLECTIONS = ["states", "burgs", "cultures", "religions", "provinces",
               "rivers", "markers", "routes", "zones", "notes", "features"]
ECON_COLLECTIONS = ["goods", "markets", "trades", "rebels", "ice"]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    path, what = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else None

    m = AzgaarMap.load(path)
    if what == "regiments":
        data = m.regiments()
    elif what == "options":
        data = m.options
    elif what == "all":
        data = {c: getattr(m, c) for c in COLLECTIONS}
        data["regiments"] = m.regiments()
        data["options"] = m.options
        data["summary"] = m.summary()
        if m.has_economy:
            for c in ECON_COLLECTIONS:
                data[c] = getattr(m, c)
    elif what in ECON_COLLECTIONS:
        if not m.has_economy:
            print(f"'{what}' indisponible : carte en {m.n_blocks} blocs "
                  f"(économie = 46 blocs, FMG v1.13x+ uniquement).")
            sys.exit(1)
        data = getattr(m, what)
    elif what in COLLECTIONS:
        data = getattr(m, what)
    else:
        allc = COLLECTIONS + ECON_COLLECTIONS + ["regiments", "options", "all"]
        print(f"Collection inconnue : {what}\nValides : {allc}")
        sys.exit(1)

    text = json.dumps(data, ensure_ascii=False, indent=2)
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"✓ {what} → {out} ({len(text):,} caractères)")
    else:
        print(text)


if __name__ == "__main__":
    main()
