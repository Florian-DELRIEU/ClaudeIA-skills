#!/usr/bin/env python3
"""Génère des identifiants au format BattleScribe : xxxx-xxxx-xxxx-xxxx (hexadécimal).

Usage:
    python3 bs_new_id.py            # 1 id
    python3 bs_new_id.py 10         # 10 ids

Les ids BattleScribe sont "n'importe quel texte unique" ; ce format (4 groupes hex de 4) est celui
produit par BattleScribe et New Recruit. Pour garantir l'unicité dans un fichier existant, comparer
avec les ids déjà présents (bs_inspect.py les liste, bs_validate.py détecte les doublons).
"""
import secrets
import sys


def new_id() -> str:
    return "-".join(secrets.token_hex(2) for _ in range(4))


def main() -> int:
    n = 1
    if len(sys.argv) > 1:
        try:
            n = max(1, int(sys.argv[1]))
        except ValueError:
            print("Argument invalide : indiquer un entier (nombre d'ids).", file=sys.stderr)
            return 2
    for _ in range(n):
        print(new_id())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
