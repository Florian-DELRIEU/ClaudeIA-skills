#!/usr/bin/env python3
"""
tp_info.py — Inspection rapide d'une sauvegarde Time Planner (lecture seule).

Usage :
  python3 tp_info.py base.sqlite                 # vue d'ensemble
  python3 tp_info.py base.sqlite --categories    # + liste des catégories
  python3 tp_info.py base.sqlite --tasks 20      # + N tâches actives
  python3 tp_info.py base.sqlite --cat "Nom"     # + tâches d'une catégorie
  python3 tp_info.py base.sqlite --scheduled     # + activités programmées
  python3 tp_info.py base.sqlite --check         # contrôle d'intégrité
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from tp_lib import TimePlanner, ms_to_str

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    path = sys.argv[1]
    args = sys.argv[2:]
    tp = TimePlanner(path)

    s = tp.summary()
    print(f"=== {os.path.basename(path)} ===")
    print(f"Catégories : {s['category']} ({s['categories_actives']} actives, "
          f"{s['categories_archivees']} archivées)")
    print(f"Tâches     : {s['task']} ({s['taches_actives']} actives, "
          f"{s['taches_completees']} complétées)")
    print(f"Activités  : {s['scheduled_activity']} programmées, "
          f"{s['logged_activity']} loguées")
    print(f"Notes {s['note']} | Tags {s['tag']} | Pièces jointes {s['attachment']}")
    print(f"Période    : {s['premiere_tache']} → {s['derniere_tache']}")

    if "--categories" in args:
        print("\n--- CATÉGORIES ---")
        for c in tp.categories():
            flag = "  [archivée]" if c["archived"] else ""
            print(f"  #{c['_id']:<4} {c['color_hex']}  {c['name']}{flag}")

    if "--cat" in args:
        name = args[args.index("--cat") + 1]
        cats = tp.category_by_name(name)
        if not cats:
            print(f"\nAucune catégorie nommée '{name}'")
        for c in cats:
            print(f"\n--- Tâches de '{c['name']}' (#{c['_id']}) ---")
            for t in tp.tasks(pid=c["_id"]):
                mark = "✓" if t["completed"] else "·"
                pr = f"[{t['priority_label']}]" if t["priority"] else ""
                print(f"  {mark} #{t['_id']:<5} {t['name']} {pr}")

    if "--tasks" in args:
        n = int(args[args.index("--tasks") + 1])
        print(f"\n--- {n} TÂCHES ACTIVES ---")
        for t in tp.tasks(completed=False)[:n]:
            pr = f"[{t['priority_label']}]" if t["priority"] else ""
            print(f"  · #{t['_id']:<5} {t['name']} {pr}")

    if "--scheduled" in args:
        print("\n--- ACTIVITÉS PROGRAMMÉES ---")
        for a in tp.scheduled()[:40]:
            nm = a["name"] or "(sans nom)"
            print(f"  #{a['_id']:<5} {a['start']} {a['days']:<14} x{a['every_num']} {nm}")

    if "--check" in args:
        print("\n--- INTÉGRITÉ ---")
        for k, v in tp.integrity().items():
            print(f"  {k}: {v if v else 'OK'}")

    tp.close()

if __name__ == "__main__":
    main()
