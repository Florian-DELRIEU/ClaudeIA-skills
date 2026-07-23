#!/usr/bin/env python3
"""
validate.py — vérifie qu'un fichier ORBAT est structurellement sain et
réimportable dans orbat-mapper.app.

Contrôles :
  - clés top-level présentes (type, version, sides, equipment, personnel, settings...)
  - chaque unité possède id, name, sidc
  - sidc = exactement 20 chiffres
  - ids uniques sur tout l'arbre
  - chaque code equipment/personnel référencé existe dans le catalogue (sinon WARN)

Usage : python validate.py ORBAT.json
Code de sortie 0 si aucune ERREUR (les WARN ne bloquent pas).
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orbat_lib import load, iter_units, catalog_map

TOP_KEYS = ["type", "version", "name", "sides", "equipment",
            "personnel", "settings", "symbologyStandard"]
SIDC_RE = re.compile(r"^\d{20}$")


def main():
    orbat = load(sys.argv[1])
    errors, warns = [], []

    for k in TOP_KEYS:
        if k not in orbat:
            errors.append(f"clé top-level manquante : {k}")

    eq_cat = set(catalog_map(orbat, "equipment"))
    pe_cat = set(catalog_map(orbat, "personnel"))
    su_cat = set(catalog_map(orbat, "supplies"))  # supplyCategories

    seen_ids = {}
    n = 0
    for u, path in iter_units(orbat, with_path=True):
        n += 1
        loc = " > ".join(path + [u.get("name", "?")])
        uid = u.get("id")
        if not uid:
            errors.append(f"[{loc}] id manquant")
        elif uid in seen_ids:
            errors.append(f"[{loc}] id dupliqué : {uid} (déjà sur « {seen_ids[uid]} »)")
        else:
            seen_ids[uid] = u.get("name", "?")
        if not u.get("name"):
            warns.append(f"[{loc}] name vide")
        sidc = u.get("sidc")
        if not sidc:
            errors.append(
                f"[{loc}] sidc manquant — CASSE L'IMPORT au-delà de ce niveau "
                "si ce nœud est imbriqué dans des subUnits (piège confirmé : "
                "orbat-mapper.app arrête la récursion sur un nœud sans sidc). "
                "Probable make_group() utilisé à la place de make_org_unit()/"
                "make_unit() pour un niveau intermédiaire — voir references/format.md."
            )
        elif not SIDC_RE.match(str(sidc)):
            errors.append(f"[{loc}] sidc invalide (doit être 20 chiffres) : {sidc!r}")
        for item in u.get("equipment", []) or []:
            if item.get("name") not in eq_cat:
                warns.append(f"[{loc}] equipment hors catalogue : {item.get('name')!r}")
        for item in u.get("personnel", []) or []:
            if item.get("name") not in pe_cat:
                warns.append(f"[{loc}] personnel hors catalogue : {item.get('name')!r}")
        for item in u.get("supplies", []) or []:
            if item.get("name") not in su_cat:
                warns.append(f"[{loc}] supply hors supplyCategories : {item.get('name')!r}")
        for st in u.get("state", []) or []:
            if not st.get("t"):
                errors.append(f"[{loc}] entrée state sans horodatage `t`")

    print(f"Unités analysées : {n}")
    print(f"ERREURS : {len(errors)} | AVERTISSEMENTS : {len(warns)}\n")
    for e in errors:
        print("  ERREUR  ", e)
    for w in warns[:40]:
        print("  WARN    ", w)
    if len(warns) > 40:
        print(f"  ... (+{len(warns) - 40} autres warnings)")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
