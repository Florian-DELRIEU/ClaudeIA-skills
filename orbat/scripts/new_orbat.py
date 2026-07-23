#!/usr/bin/env python3
"""
new_orbat.py — construction d'ORBAT import-ready pour orbat-mapper.app.

Deux usages :

1) En ligne de commande, créer une enveloppe vierge valide :
     python new_orbat.py --name "Mon ORBAT" --out mon_orbat.json

2) Comme bibliothèque, quand Claude génère un ORBAT à partir d'une demande.
   Fonctions clés :
     build_sidc(echelon, entity, identity='3', symset='10', mod1='00', mod2='00')
     make_unit(name, echelon, entity, subUnits=None, equipment=None, personnel=None, **kw)
     make_org_unit(name, echelon, subUnits, entity='000000', **kw)  # regroupement intermédiaire, PAS make_group
     new_orbat(name, sides) / make_side(...) / make_group(...)  # make_group = side.groups UNIQUEMENT
   puis orbat_lib.save(orbat, path).

Le SIDC fait 20 chiffres :
  pos 1-2  version    -> "10"
  pos 3    contexte   -> "0" (réalité)
  pos 4    identité   -> 0 Pending 1 Inconnu 2 AmiPrésumé 3 Ami 4 Neutre 5 Suspect 6 Hostile
  pos 5-6  symbol set -> "10" Unité terrestre (défaut)
  pos 7    statut     -> "0" présent (1 = planifié)
  pos 8    HQ/TF/D    -> "0"
  pos 9-10 échelon    -> voir ECHELON
  pos 11-16 entité    -> icône principale (6 chiffres), voir references/sidc.md + dictionnaire
  pos 17-18 mod1, 19-20 mod2 -> modificateurs (armes, capacités), défaut "00"
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orbat_lib import gen_id, now_iso, save

# Échelons fréquents (pos 9-10). FR entre parenthèses.
ECHELON = {
    "equipe": "11", "team": "11", "crew": "11",
    "escouade": "12", "squad": "12",
    "section_us": "13",
    "peloton": "14", "section": "14", "platoon": "14",   # FR "section" = platoon
    "compagnie": "15", "company": "15", "batterie": "15", "escadron": "15",
    "bataillon": "16", "battalion": "16",
    "regiment": "17", "groupe_tactique": "17",
    "brigade": "18",
    "division": "21",
    "corps": "22",
    "armee": "23",
}

IDENTITY = {"pending": "0", "inconnu": "1", "ami_presume": "2",
            "ami": "3", "neutre": "4", "suspect": "5", "hostile": "6"}


def build_sidc(echelon, entity, identity="3", symset="10",
               context="0", status="0", hqtfd="0", mod1="00", mod2="00"):
    ech = ECHELON.get(str(echelon).lower(), str(echelon))
    iden = IDENTITY.get(str(identity).lower(), str(identity))
    assert len(ech) == 2 and len(entity) == 6, "echelon=2 chiffres, entity=6 chiffres"
    sidc = f"10{context}{iden}{symset}{status}{hqtfd}{ech}{entity}{mod1}{mod2}"
    assert len(sidc) == 20, f"sidc != 20 chiffres : {sidc} ({len(sidc)})"
    return sidc


def make_unit(name, echelon, entity, *, identity="3", subUnits=None,
              equipment=None, personnel=None, sidc=None, **extra):
    u = {
        "id": gen_id(),
        "name": name,
        "sidc": sidc or build_sidc(echelon, entity, identity=identity),
        "subUnits": subUnits or [],
    }
    if equipment:
        u["equipment"] = [{"name": n, "count": c} for n, c in equipment]
    if personnel:
        u["personnel"] = [{"name": n, "count": c} for n, c in personnel]
    u["symbolOptions"] = {}
    u["state"] = []
    u.update(extra)
    return u


def make_group(name, subUnits):
    """Group de TÊTE uniquement (side.groups[i]) — le seul endroit où l'absence
    de `sidc` est correcte pour orbat-mapper.app. NE JAMAIS placer le résultat
    de make_group() dans les subUnits d'une Unit ou d'un autre Group : l'import
    s'arrête silencieusement dès qu'il rencontre un nœud sans sidc en
    profondeur > 1 (piège confirmé, voir references/format.md). Pour tout
    niveau intermédiaire (division, brigade, régiment... utilisé comme simple
    regroupement), utiliser make_org_unit() à la place."""
    return {"name": name, "id": gen_id(), "subUnits": subUnits, "symbolOptions": {}}


def make_org_unit(name, echelon, subUnits, *, entity="000000", **kw):
    """Unité d'organisation intermédiaire (division, brigade, groupement...) :
    comme make_unit(), mais pensée pour le cas où l'unité ne sert qu'à
    regrouper des sous-unités (icône générique état-major par défaut). C'est
    l'équivalent « sûr à l'import » de make_group() pour tout niveau qui
    n'est pas directement sous side.groups — toujours un sidc valide."""
    return make_unit(name, echelon, entity, subUnits=subUnits, **kw)


def make_side(name, groups, identity="3", fill="#80e0ff"):
    return {"name": name, "standardIdentity": IDENTITY.get(identity, identity),
            "symbolOptions": {"fillColor": fill}, "units": [],
            "id": gen_id(), "groups": groups}


def new_orbat(name, sides, *, equipment=None, personnel=None,
              tz="Europe/Paris", start="2025-01-01T00:00:00+01:00", description=""):
    return {
        "id": gen_id(), "type": "ORBAT-mapper", "version": "2.0.0",
        "meta": {"createdDate": now_iso(), "lastModifiedDate": now_iso()},
        "name": name, "startTime": start, "timeZone": tz,
        "description": description, "symbologyStandard": "app6",
        "sides": sides,
        "layers": [{"name": "Features", "id": gen_id(), "features": []}],
        "events": [], "mapLayers": [],
        "equipment": [{"name": n, "description": d} for n, d in (equipment or [])],
        "personnel": [{"name": n, "description": d} for n, d in (personnel or [])],
        "supplyCategories": [],
        "settings": {"rangeRingGroups": [], "statuses": [], "supplyClasses": [],
                     "supplyUoMs": [], "map": {"baseMapId": "osm"},
                     "symbolFillColors": [], "customSymbols": []},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="Nouvel ORBAT")
    ap.add_argument("--side", default="Bleu")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    orbat = new_orbat(args.name, [make_side(args.side, [make_group("Groupe 1", [])])])
    save(orbat, args.out)
    print("Écrit :", args.out)


if __name__ == "__main__":
    main()
