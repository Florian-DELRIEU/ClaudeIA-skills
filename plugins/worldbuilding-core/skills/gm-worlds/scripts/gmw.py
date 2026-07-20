#!/usr/bin/env python3
"""gmw.py — GM géopolitique en LECTURE pour sauvegardes Azgaar (.map).

Philosophie v2 : Florian joue les événements lui-même dans FMG (diplomatie,
régiments, provinces...). Le moteur ne touche JAMAIS aux données de jeu — il
LIT l'état actuel du .map (source de vérité), calcule la suite (dés,
économie, guerres) et rend des DIRECTIVES claires à appliquer manuellement
dans FMG. Les seules écritures sont deux notes de service (bilan chiffré
"fingerprint" + chronique narrative), jamais states/military/diplomacy/zones.

Conséquence directe : aucun risque de cache SVG obsolète (le bug documenté
dans /azgaars sur les régiments et, par précaution, présumé aussi valable
pour les zones) puisqu'on n'édite plus jamais ces blocs.

Usage :
    python3 gmw.py snapshot <carte.map>                 # état actuel, lecture pure
    python3 gmw.py advance  <carte.map> [-n 1] [--out X.map] [--chaos 1.0] [--years-per-turn 1]
    python3 gmw.py report   <carte.map>                 # relit le dernier bilan, sans calculer

Dépendance : la lib azgaar_lib du skill /azgaars (résolue automatiquement).
"""
from __future__ import annotations
import sys, json, random, argparse, math, re
from pathlib import Path

# ------------------------------------------------------------ import azgaar_lib
def _find_azgaar_lib():
    """Priorité au skill /azgaars installé (s'il expose l'API requise) ; la
    copie embarquée dans /gm-worlds sert de secours si /azgaars est absent
    ou trop ancien."""
    required = ("industry_index", "market_value_by_state", "burgs_by_state", "ports_by_state")
    ordered = [
        Path("/mnt/skills/user/azgaars/scripts"),
        Path("/home/claude/azgaars/scripts"),
        Path(__file__).parent,
    ]
    fallback = None
    for c in ordered:
        f = c / "azgaar_lib.py"
        if not f.exists():
            continue
        src = f.read_text(encoding="utf-8", errors="ignore")
        if all(name in src for name in required):
            sys.path.insert(0, str(c))
            return
        fallback = fallback or str(c)
    if fallback:
        sys.path.insert(0, fallback)
        print("⚠️  azgaar_lib trouvé mais sans l'API requise (industry_index/"
              "market_value_by_state/burgs_by_state/ports_by_state). "
              "Mettre à jour /azgaars.", file=sys.stderr)
        return
    sys.exit("azgaar_lib.py introuvable : installer le skill /azgaars.")
_find_azgaar_lib()
from azgaar_lib import AzgaarMap

FP_NOTE = "gmworlds-fingerprint"      # bilan chiffré (bookkeeping invisible)
CHRON_NOTE = "gmworlds-chronicle"     # chronique narrative (note-only, sans risque)

# ============================================================ LECTURE PURE
# Toute la lecture/interprétation du .map (puissance militaire, provinces par
# état, matrice diplomatique, guerres en cours, biomes, photographie complète)
# vit désormais dans /azgaars (AzgaarMap.strategic_snapshot() et les méthodes
# qu'elle assemble). gm-worlds ne fait qu'appeler cette API — il ne réimplémente
# plus sa propre lecture. Voir /azgaars reference/format.md § interprétation.

def world_snapshot(m) -> dict:
    return m.strategic_snapshot()

def diff_snapshots(old: dict | None, new: dict) -> list[str]:
    """Compare le bilan précédent (mémorisé) à l'état actuel du fichier pour
    détecter ce que Florian a réellement fait depuis la dernière session :
    provinces transférées, armées qui ont grossi/fondu, guerres commencées ou
    closes en dehors de nos propositions, etc. C'est le cœur de « interpréter
    correctement la sauvegarde » : on ne suppose jamais que les directives
    précédentes ont été appliquées telles quelles — on relit la réalité."""
    if not old:
        return []
    out = []
    old_states, new_states = old.get("states", {}), new.get("states", {})
    for sid, ns in new_states.items():
        os_ = old_states.get(sid)
        if not os_:
            continue
        if set(os_["provinces"]) != set(ns["provinces"]):
            gained = set(ns["provinces"]) - set(os_["provinces"])
            lost = set(os_["provinces"]) - set(ns["provinces"])
            if gained:
                out.append(f"{ns['nom']} a gagné {len(gained)} province(s) depuis la dernière fois.")
            if lost:
                out.append(f"{ns['nom']} a perdu {len(lost)} province(s) depuis la dernière fois.")
        delta_eff = ns["effectifTotal"] - os_["effectifTotal"]
        if abs(delta_eff) > max(500, os_["effectifTotal"] * 0.08):
            sign = "renforcé" if delta_eff > 0 else "affaibli"
            out.append(f"L'armée de {ns['nom']} s'est {sign} de {abs(delta_eff):,} hommes".replace(",", " ") + ".")
    old_wars = {f"{w['a']}-{w['b']}" for w in old.get("guerres", [])}
    new_wars = {f"{w['a']}-{w['b']}" for w in new.get("guerres", [])}
    for k in new_wars - old_wars:
        a, b = k.split("-")
        out.append(f"Guerre en cours entre {new_states.get(a,{}).get('nom',a)} et "
                   f"{new_states.get(b,{}).get('nom',b)} (déclarée hors de nos tours, ou depuis notre dernier passage).")
    for k in old_wars - new_wars:
        a, b = k.split("-")
        out.append(f"La guerre entre {old_states.get(a,{}).get('nom',a)} et "
                   f"{old_states.get(b,{}).get('nom',b)} s'est conclue (diplomatie remise à jour dans FMG).")
    return out

# ============================================================ NOTES DE SERVICE
def read_note(m, note_id) -> str | None:
    for n in m.notes:
        if n.get("id") == note_id:
            return n.get("legend")
    return None

def write_note(m, note_id, name, legend):
    notes = [n for n in m.notes if n.get("id") != note_id]
    notes.append({"id": note_id, "name": name, "legend": legend})
    m._parsed[m._idx("notes")] = notes
    m.mark_dirty("notes")

def read_fp(m) -> dict | None:
    raw = read_note(m, FP_NOTE)
    return json.loads(raw) if raw else None

def write_fp(m, fp):
    write_note(m, FP_NOTE, "GM-Worlds — bilan (ne pas éditer à la main)",
              json.dumps(fp, ensure_ascii=False, separators=(",", ":")))

def append_chronicle(m, lines: list[str], year):
    prev = read_note(m, CHRON_NOTE) or ""
    block = f"<h3>An {year}</h3><ul>" + "".join(f"<li>{l}</li>" for l in lines) + "</ul>"
    write_note(m, CHRON_NOTE, "GM-Worlds — Chronique du monde", prev + block)

def chronicle_to_markdown(html: str, title: str) -> str:
    """Convertit la chronique (HTML simple et entièrement maîtrisé, généré par
    append_chronicle : <h3>An N</h3><ul><li>...</li></ul> répété) en Markdown
    propre. Le format source est fixe et sous notre contrôle → extraction par
    expressions régulières fiable, pas besoin d'un parseur HTML complet."""
    blocks = re.findall(r"<h3>(.*?)</h3>\s*<ul>(.*?)</ul>", html, re.S)
    years = [int(re.search(r"\d+", h).group()) for h, _ in blocks if re.search(r"\d+", h)]
    subtitle = f"*De l'an {min(years)} à l'an {max(years)}*" if years else ""
    lines = [f"# {title}", "", subtitle, ""] if subtitle else [f"# {title}", ""]
    for heading, body in blocks:
        lines.append(f"## {heading.strip()}")
        lines.append("")
        items = re.findall(r"<li>(.*?)</li>", body, re.S)
        if not items:
            lines.append("*Année sans événement notable.*")
        for it in items:
            text = it.strip().replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            lines.append(f"- {text}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

# ============================================================ CALCUL (PUR, SANS ÉCRITURE JEU)
# aggression_of / stability_of vivent désormais dans azgaar_lib
# (AzgaarMap.aggression_of / .stability_of) — gm-worlds les appelle sur m.


# ============================================================ SYSTÈME DE JETS D100
# Même logique que /gm-basic : Claude ANNONCE le test et sa difficulté (le seuil
# à faire, ou le modificateur pour une bataille), Florian lance le d100
# lui-même, Claude/le moteur INTERPRÈTE le résultat — jamais l'inverse. Le
# moteur ne lance jamais de dé à la place de Florian (sauf le mode secondaire
# `advance`, clairement à part, pour test rapide sans lui).

def interpret_trigger(roll: int, target: float) -> str:
    """Résultat d'un jet de déclenchement (tension, rapprochement, velléité de
    guerre, révolte, essor) : plus le jet est bas sous la cible, plus l'issue
    est marquée. Renvoie 'critique' / 'succes' / 'partiel' / 'echec'."""
    target = max(1.0, min(99.0, target))
    if roll <= max(1, round(target * 0.15)):
        return "critique"
    if roll <= target:
        return "succes"
    if roll <= target + (100 - target) * 0.35:
        return "partiel"
    return "echec"

BATTLE_BANDS = [
    (95, "victoire écrasante", 22, (0.02, 0.10)),
    (65, "victoire nette",     12, (0.03, 0.07)),
    (40, "accrochage indécis",  3, (0.05, 0.05)),
    (15, "revers",            -12, (0.07, 0.03)),
    (0,  "défaite sévère",    -22, (0.10, 0.02)),
]

def interpret_battle(roll: int, modifier: int) -> dict:
    """roll + modificateur (déjà annoncé avant le jet) comparé à une table de
    marge fixe. Renvoie la bande, le delta de score de guerre côté a (positif
    favorise a), et les % d'effectif perdus (a, b)."""
    total = roll + modifier
    for seuil, label, delta, pertes in BATTLE_BANDS:
        if total >= seuil:
            return {"total": total, "bande": label, "deltaScore": delta,
                   "pertesPctA": pertes[0], "pertesPctB": pertes[1]}
    return {"total": total, "bande": "défaite sévère", "deltaScore": -22,
           "pertesPctA": 0.10, "pertesPctB": 0.02}

def battle_modifier(m, A, B, powers) -> int:
    pa = m.state_power(A, powers) * (0.7 + 0.6 * m.stability_of(A, True))
    pb = m.state_power(B, powers) * (0.7 + 0.6 * m.stability_of(B, True)) * 1.15  # défenseur
    ratio = (pa - pb) / max(pa + pb, 1)
    return round(max(-35, min(35, ratio * 40)))

def build_pending_checks(m, fp: dict, chaos: float, max_battles: int = 6) -> list[dict]:
    """Énumère les jets à demander à Florian pour le tour à venir. NE CONSOMME
    AUCUN ALÉA — juste des seuils/modificateurs calculés depuis l'état actuel.
    Limite le nombre de jets diplomatiques ET de batailles aux cas les plus
    significatifs (sinon des dizaines de d100 par tour sur une grande carte)."""
    states = m.active_states()
    by_id = {s["i"]: s for s in states}
    powers = m.unit_powers()
    ind = m.industry_index()
    wars_now = m.current_wars()
    war_pairs = {f"{min(a,b)}-{max(a,b)}": (a, b) for a, b in wars_now}
    at_war_ids = {i for pair in war_pairs.values() for i in pair}
    dip = m.diplomacy_matrix()
    cooldowns = fp.get("peaceCooldown", {})
    war_scores = fp.get("warScores", {})

    checks = []

    # -- batailles : plafonnées aux guerres les plus significatives (sauf
    # cooldown de paix). Priorité aux guerres déjà engagées (score de guerre
    # élevé en valeur absolue = proches de leur conclusion — les finir réduit
    # la charge de dés des tours suivants) puis à la puissance combinée des
    # deux camps (plus gros affrontements = enjeu narratif plus fort).
    battle_candidates = []
    for key, (a, b) in war_pairs.items():
        if cooldowns.get(key, 0) > 0:
            continue
        A, B = by_id.get(a), by_id.get(b)
        if not A or not B:
            continue
        mod = battle_modifier(m, A, B, powers)
        score_engagement = abs(war_scores.get(key, {}).get("score", 0.0))
        combined_power = m.state_power(A, powers) + m.state_power(B, powers)
        priority = score_engagement * 2 + combined_power / 1000
        battle_candidates.append((priority, key, A, B, mod))
    battle_candidates.sort(key=lambda x: -x[0])
    reportees = battle_candidates[max_battles:]
    for priority, key, A, B, mod in battle_candidates[:max_battles]:
        checks.append({
            "id": f"bataille-{key}", "kind": "bataille", "a": A["i"], "b": B["i"],
            "description": f"Bataille {A['name']} vs {B['name']}",
            "modifier": mod,
            "annonce": f"⚔️ {A['name']} vs {B['name']} — jet de bataille, modificateur {mod:+d} "
                      f"(rapport de forces). Lance 1d100 ; on ajoute le modificateur et on lit le résultat "
                      f"sur la table (≥95 victoire écrasante, ≥65 nette, ≥40 accrochage, ≥15 revers, <15 défaite sévère).",
        })
    en_attente_paix = [key for key in war_pairs if cooldowns.get(key, 0) > 0]
    fronts_reportes = [f"{A['name']} vs {B['name']}" for _, key, A, B, mod in reportees]

    # -- diplomatie : candidats classés par significativité, plafonnés
    tension_candidates, rappr_candidates, guerre_candidates = [], [], []
    seen_pairs = set()
    for s in states:
        for nb in s.get("neighbors", []):
            if nb not in by_id or nb <= s["i"]:
                continue
            key = f"{s['i']}-{nb}"
            if key in war_pairs or key in seen_pairs:
                continue
            seen_pairs.add(key)
            status = dip.get(key, "Neutral")
            a_agg, b_agg = m.aggression_of(s), m.aggression_of(by_id[nb])
            trader = s.get("type") in ("Naval", "Lake") or by_id[nb].get("type") in ("Naval", "Lake")
            tension_mult = 1.0 if status in ("Rival", "Suspicion") else 0.35
            target_t = round(max(2, min(88, 3.5 * chaos * (a_agg + b_agg) * tension_mult)), 1)
            tension_candidates.append((target_t, s, by_id[nb], key, status))
            if status in ("Neutral", "Friendly") and trader:
                rappr_candidates.append((10.0, s, by_id[nb], key, status))
            if status == "Rival":
                fronts = sum(1 for k in war_pairs if str(s["i"]) in k.split("-"))
                if fronts < 2:
                    target_g = round(max(2, min(85, 12 * a_agg * chaos)), 1)
                    guerre_candidates.append((target_g, s, by_id[nb], key))

    tension_candidates.sort(key=lambda x: -x[0])
    for target, s, o, key, status in tension_candidates[:4]:
        checks.append({
            "id": f"tension-{key}", "kind": "tension", "a": s["i"], "b": o["i"],
            "description": f"{s['name']} ↔ {o['name']} (actuellement {status})",
            "target": target,
            "annonce": f"⚠️ Tension {s['name']} ↔ {o['name']} (statut actuel {status}) — jet de déclenchement, "
                      f"cible {target:.0f} ou moins sur d100.",
        })
    rappr_candidates.sort(key=lambda x: -x[0])
    for target, s, o, key, status in rappr_candidates[:2]:
        checks.append({
            "id": f"rapprochement-{key}", "kind": "rapprochement", "a": s["i"], "b": o["i"],
            "description": f"{s['name']} ↔ {o['name']} (actuellement {status})",
            "target": target,
            "annonce": f"🤝 Rapprochement possible {s['name']} ↔ {o['name']} (statut actuel {status}) — "
                      f"jet de déclenchement, cible {target:.0f} ou moins sur d100.",
        })
    guerre_candidates.sort(key=lambda x: -x[0])
    for target, s, o, key in guerre_candidates[:2]:
        pa, pb = m.state_power(s, powers), m.state_power(o, powers)
        checks.append({
            "id": f"guerre-{key}", "kind": "guerre", "a": s["i"], "b": o["i"],
            "description": f"{s['name']} pourrait déclarer la guerre à {o['name']}",
            "target": target,
            "annonce": f"⚔️ Velléité de guerre : {s['name']} contre {o['name']} (rapport de forces "
                      f"{pa:.0f} vs {pb:.0f}) — jet de déclenchement, cible {target:.0f} ou moins sur d100.",
        })

    # -- entrée en guerre par solidarité d'alliance : pour chaque guerre en
    # cours, un allié (statut Ally, lu dans la diplomatie réelle) de l'un des
    # deux belligérants peut être entraîné dans le conflit contre l'AUTRE camp.
    # Ne change rien seul si le jet échoue — Florian applique le changement de
    # diplomatie (nouveau statut Enemy) qui fera apparaître un nouveau front
    # (nouvelle bataille) au prochain tour, sans logique de combat à N côtés :
    # chaque paire en guerre reste résolue indépendamment. Plafonné à 2 candidats
    # (les plus significatifs) pour ne pas multiplier les jets à chaque tour.
    coalition_candidates = []
    seen_join = set()
    for key, (a, b) in war_pairs.items():
        for belligerant, adversaire in ((a, b), (b, a)):
            bel_s, adv_s = by_id.get(belligerant), by_id.get(adversaire)
            if not bel_s or not adv_s:
                continue
            dip_row = bel_s.get("diplomacy", [])
            for ally_id, status in enumerate(dip_row):
                if status != "Ally" or ally_id not in by_id or ally_id == adversaire:
                    continue
                join_key = f"{ally_id}-{adversaire}" if ally_id < adversaire else f"{adversaire}-{ally_id}"
                if join_key in war_pairs or join_key in seen_join:
                    continue
                seen_join.add(join_key)
                ally_s = by_id[ally_id]
                agg = m.aggression_of(ally_s)
                target = round(max(3, min(70, 10 * agg * chaos)), 1)
                coalition_candidates.append((target, ally_s, bel_s, adv_s, join_key))
    coalition_candidates.sort(key=lambda x: -x[0])
    for target, ally_s, bel_s, adv_s, join_key in coalition_candidates[:2]:
        checks.append({
            "id": f"coalition-{join_key}", "kind": "coalition", "a": ally_s["i"], "b": adv_s["i"],
            "description": f"{ally_s['name']} pourrait entrer en guerre aux côtés de {bel_s['name']} "
                           f"contre {adv_s['name']}",
            "target": target,
            "annonce": f"🛡️ Solidarité d'alliance : {ally_s['name']} (allié de {bel_s['name']}) pourrait "
                      f"entrer en guerre contre {adv_s['name']} — jet de déclenchement, cible {target:.0f} "
                      f"ou moins sur d100.",
        })

    # -- économie concrète (cartes 46 blocs uniquement, module Économie) :
    # pénurie et boom commercial s'appuient sur les VRAIS stocks de biens par
    # état (good_stock_by_state), comparés à la moyenne des autres états qui
    # détiennent ce bien — pas une abstraction liée à la stabilité. L'embargo
    # s'appuie sur les VRAIES transactions du bloc trades (trade_flows_by_state)
    # croisées avec la diplomatie tendue. Rien de tout ça n'existe sur les
    # cartes 39 blocs (has_economy=False) — silencieusement absent, pas d'erreur.
    if m.has_economy:
        stock_by_state = m.good_stock_by_state()
        goods_names = {g["i"]: g.get("name", f"bien#{g['i']}") for g in m.goods}

        good_totals: dict[int, float] = {}
        good_counts: dict[int, int] = {}
        for st_id, goods_qty in stock_by_state.items():
            for gid, qty in goods_qty.items():
                if qty > 0:
                    good_totals[gid] = good_totals.get(gid, 0) + qty
                    good_counts[gid] = good_counts.get(gid, 0) + 1
        # moyenne comparative seulement si le bien est détenu par au moins 3
        # états (sinon "moyenne" n'a pas de sens comme référence)
        good_avg = {gid: good_totals[gid] / good_counts[gid]
                   for gid in good_totals if good_counts[gid] >= 3}

        penurie_candidates, boom_candidates = [], []
        for st_id, goods_qty in stock_by_state.items():
            if st_id not in by_id:
                continue
            worst_dev, worst_gid = 0.0, None
            best_dev, best_gid = 0.0, None
            for gid, qty in goods_qty.items():
                avg = good_avg.get(gid)
                if not avg:
                    continue
                dev = (qty - avg) / avg
                # qty > 0 exigé côté pénurie : un stock nul n'est pas "une pénurie
                # qui arrive", c'est souvent une région qui n'a jamais produit ce
                # bien (non significatif narrativement). On ne garde que les états
                # qui ONT le bien mais proportionnellement bien moins que leurs
                # pairs — une vraie rareté relative, pas une absence structurelle.
                if qty > 0 and dev < worst_dev:
                    worst_dev, worst_gid = dev, gid
                if dev > best_dev:
                    best_dev, best_gid = dev, gid
            if worst_gid is not None and worst_dev <= -0.6:
                target = round(max(5, min(75, abs(worst_dev) * 40 * chaos)), 1)
                penurie_candidates.append((target, by_id[st_id], goods_names.get(worst_gid, "?"), worst_dev))
            if best_gid is not None and best_dev >= 0.8:
                target = round(max(5, min(70, best_dev * 25 * chaos)), 1)
                boom_candidates.append((target, by_id[st_id], goods_names.get(best_gid, "?"), best_dev))

        penurie_candidates.sort(key=lambda x: -x[0])
        for target, s, good_name, dev in penurie_candidates[:3]:
            checks.append({
                "id": f"penurie-{s['i']}", "kind": "penurie", "a": s["i"], "bien": good_name,
                "description": f"{s['name']} — pénurie de {good_name} ({abs(round(dev*100))}% sous la moyenne)",
                "target": target,
                "annonce": f"📉 Pénurie possible de {good_name} à {s['name']} (stock {abs(round(dev*100))}% "
                          f"sous la moyenne des autres états) — jet de déclenchement, cible {target:.0f} "
                          f"ou moins sur d100.",
            })
        boom_candidates.sort(key=lambda x: -x[0])
        for target, s, good_name, dev in boom_candidates[:2]:
            checks.append({
                "id": f"boom-{s['i']}", "kind": "boom_commercial", "a": s["i"], "bien": good_name,
                "description": f"{s['name']} — boom commercial du {good_name} (+{round(dev*100)}% vs moyenne)",
                "target": target,
                "annonce": f"📈 Boom commercial possible du {good_name} à {s['name']} (stock +{round(dev*100)}% "
                          f"vs la moyenne des autres états) — jet de déclenchement, cible {target:.0f} "
                          f"ou moins sur d100.",
            })

        flows = m.trade_flows_by_state()
        if flows:
            max_flow = max(flows.values()) or 1
            tension_mult = {"Suspicion": 0.6, "Rival": 1.0, "Enemy": 1.3}
            embargo_candidates = []
            for key, val in flows.items():
                pa, pb = (int(x) for x in key.split("-"))
                if pa not in by_id or pb not in by_id or key in war_pairs:
                    continue
                status = dip.get(key, "Neutral")
                if status not in tension_mult:
                    continue
                relative_flow = val / max_flow
                if relative_flow < 0.15:
                    continue
                target = round(max(5, min(70, relative_flow * 45 * tension_mult[status] * chaos)), 1)
                embargo_candidates.append((target, by_id[pa], by_id[pb], val, status, key))
            embargo_candidates.sort(key=lambda x: -x[0])
            for target, A, B, val, status, key in embargo_candidates[:2]:
                checks.append({
                    "id": f"embargo-{key}", "kind": "embargo", "a": A["i"], "b": B["i"],
                    "description": f"{A['name']} ↔ {B['name']} — rupture commerciale possible (statut {status}, "
                                   f"échanges parmi les plus importants de la carte)",
                    "target": target,
                    "annonce": f"🚫 Rupture commerciale possible entre {A['name']} et {B['name']} (gros partenaires "
                              f"commerciaux, statut {status}) — jet de déclenchement, cible {target:.0f} "
                              f"ou moins sur d100.",
                })

    # -- interne : révolte / essor. La révolte combine DEUX sources indépendantes :
    # la stabilité (alerte/guerre, cf. stability_of) ET la fracture culturelle ou
    # religieuse du territoire (dominant_cultures/dominant_religions). Un grand
    # état stable mais culturellement fracturé (conquêtes mal digérées) doit
    # rester à risque — pas seulement les états au bord de l'effondrement.
    # Plafonné aux cas les plus significatifs (sinon quasi tous les états d'une
    # carte diverse génèrent un jet, même à faible cible — trop de dés pour peu).
    revolte_candidates = []
    for s in states:
        stab = m.stability_of(s, s["i"] in at_war_ids)
        cultures = m.dominant_cultures(s)
        religions = m.dominant_religions(s)
        frag_c = 1 - cultures[0]["part"] if cultures else 0.0
        frag_r = 1 - religions[0]["part"] if religions else 0.0
        instab_score = max(0, 0.3 - stab) * 300      # 0-90, reprend l'ancienne formule
        unrest_score = frag_c * 45 + frag_r * 25       # 0-70, nouveau terme
        target = round(min(90, instab_score + unrest_score), 1)
        if target >= 8:
            raisons = []
            if instab_score > 0:
                raisons.append(f"stabilité {stab}")
            if frag_c > 0.15:
                top = cultures[0]
                raisons.append(f"territoire {round(top['part']*100)}% {top['culture']} seulement")
            if frag_r > 0.15:
                topr = religions[0]
                raisons.append(f"{round(topr['part']*100)}% {topr['religion']}")
            raison_txt = ", ".join(raisons) if raisons else f"stabilité {stab}"
            revolte_candidates.append((target, s, raison_txt))
        if stab > 0.85:
            target_essor = round(max(10, min(80, (stab - 0.85) * 300)), 1)
            checks.append({
                "id": f"essor-{s['i']}", "kind": "essor", "a": s["i"],
                "description": f"{s['name']} (stabilité {stab})",
                "target": target_essor,
                "annonce": f"🌟 Essor possible à {s['name']} (stabilité {stab}) — "
                          f"jet de déclenchement, cible {target_essor:.0f} ou moins sur d100.",
            })
    revolte_candidates.sort(key=lambda x: -x[0])
    for target, s, raison_txt in revolte_candidates[:5]:
        checks.append({
            "id": f"revolte-{s['i']}", "kind": "revolte", "a": s["i"],
            "description": f"{s['name']} ({raison_txt})",
            "target": target,
            "annonce": f"🔥 Troubles internes possibles à {s['name']} ({raison_txt}) — "
                      f"jet de déclenchement, cible {target:.0f} ou moins sur d100.",
        })

    # -- réarmement : suggestion informative, PAS de jet (pas d'enjeu dramatique
    # suffisant — cf. gm-basic : un jet seulement si issue incertaine ET enjeu réel)
    info = []
    for s in states:
        ind_s = ind.get(s["i"], 0)
        cap = 6 + int(ind_s * 20)
        land = [r for r in s.get("military", []) if not r.get("n")]
        if land and len(land) < cap and s["i"] in at_war_ids:
            tmpl = max(land, key=lambda r: r["a"])
            info.append(f"🪖 {s['name']} pourrait lever une nouvelle division (gabarit ~{tmpl['a']:,} hommes "
                       f"comme « {tmpl['name']} »)".replace(",", " ") + " si tu veux (pas de jet nécessaire).")

    if en_attente_paix:
        names = []
        for key in en_attente_paix:
            a, b = war_pairs[key]
            names.append(f"{by_id[a]['name']} ↔ {by_id[b]['name']}")
        info.insert(0, "⏳ Rappel : paix suggérée la dernière fois pour " + ", ".join(names) +
                   " — si tu ne l'as pas encore appliquée dans FMG, fais-le pour arrêter les prochains jets de bataille.")
    if fronts_reportes:
        info.insert(0, f"⏸️ {len(fronts_reportes)} front(s) sans jet ce tour-ci faute de place dans le plafond "
                   f"({max_battles}/tour) : " + ", ".join(fronts_reportes) +
                   " — repris en priorité au prochain tour si toujours pertinents.")
    # cooldown : décompte à chaque appel de checks (indépendamment du contenu
    # réel de la diplomatie, pour laisser à Florian le temps d'appliquer la paix)
    for key in list(cooldowns):
        cooldowns[key] -= 1
        if cooldowns[key] <= 0:
            del cooldowns[key]
    fp["peaceCooldown"] = cooldowns

    return checks, info

def resolve_checks(m, fp: dict, pending: list[dict], rolls: dict[str, int], year: int
                   ) -> tuple[list[dict], list[str]]:
    """Applique les résultats FOURNIS PAR FLORIAN (jamais générés ici) aux jets
    en attente. Un id sans jet fourni est simplement ignoré (rien ne se passe
    ce tour pour ce point précis) — transparent, jamais de dé masqué."""
    by_id = {s["i"]: s for s in m.active_states()}
    events, directives = [], []
    fp.setdefault("warScores", {})
    fp.setdefault("peaceCooldown", {})

    for chk in pending:
        roll = rolls.get(chk["id"])
        if roll is None:
            directives.append(f"(jet non fourni pour « {chk['description']} » — rien ne se passe ce tour)")
            continue
        kind = chk["kind"]

        if kind == "bataille":
            a, b = chk["a"], chk["b"]
            key = f"{min(a,b)}-{max(a,b)}"
            A, B = by_id.get(a), by_id.get(b)
            res = interpret_battle(roll, chk["modifier"])
            ws = fp["warScores"].setdefault(key, {"score": 0.0, "start": year})
            # deltaScore favorise 'a' (id le plus bas de la paire) par convention
            sign = 1 if a < b else -1
            ws["score"] = round(ws["score"] + sign * res["deltaScore"], 1)
            pertes_a = round(m.state_effectif(A) * res["pertesPctA"])
            pertes_b = round(m.state_effectif(B) * res["pertesPctB"])
            events.append({"type": "bataille", "a": A["name"], "b": B["name"], "jet": roll,
                          "modificateur": chk["modifier"], "resultat": res["bande"],
                          "pertesA": pertes_a, "pertesB": pertes_b, "score": ws["score"]})
            directives.append(f"⚔️ {A['name']} vs {B['name']} — jet {roll}{chk['modifier']:+d} = "
                              f"{res['total']} → {res['bande']}. Pertes suggérées : ~{pertes_a:,} "
                              f"({A['name']}) / ~{pertes_b:,} ({B['name']})".replace(",", " ") +
                              " — à répartir dans l'éditeur de régiments.")
            exhaustion = min(1.0, abs(ws["score"]) / 50 + (year - ws["start"]) * 0.05)
            if abs(ws["score"]) > 30 or exhaustion >= 0.85:
                winner, loser = (A, B) if ws["score"] >= 0 else (B, A)
                terms = [f"passer la diplomatie {A['name']} ↔ {B['name']} de Enemy à Neutral/Suspicion (paix)"]
                if abs(ws["score"]) > 45:
                    provs = [p["i"] for p in m.provinces if isinstance(p, dict)
                            and not p.get("removed") and p.get("state") == loser["i"]]
                    if provs:
                        p = m.provinces[__import__("random").Random(year + a + b).choice(provs)]
                        terms.append(f"transférer la province « {p['name']} » de {loser['name']} à "
                                    f"{winner['name']} (clic-droit province → changer d'état)")
                events.append({"type": "paix", "winner": winner["name"], "loser": loser["name"]})
                directives.append(f"🕊️ Fin de guerre : victoire de {winner['name']} sur {loser['name']}. "
                                  f"À appliquer : " + " ; ".join(terms) + ".")
                fp["peaceCooldown"][key] = 6
            continue

        # jets de déclenchement (tension / rapprochement / guerre / revolte / essor)
        target = chk["target"]
        outcome = interpret_trigger(roll, target)
        a_name = by_id.get(chk["a"], {}).get("name", "?")
        b_name = by_id.get(chk.get("b"), {}).get("name") if chk.get("b") is not None else None
        pair_txt = f"{a_name} ↔ {b_name}" if b_name else a_name

        if outcome == "echec":
            directives.append(f"— {chk['description']} : jet {roll} (cible {target:.0f}) → rien ne se passe.")
            continue

        events.append({"type": chk["kind"], "cible": pair_txt, "jet": roll,
                       "seuil": target, "issue": outcome})
        if kind == "tension":
            grade = "rupture ouverte" if outcome == "critique" else ("incident sérieux" if outcome == "succes" else "friction mineure")
            extra = " (voire deux crans, rupture ouverte)" if outcome == "critique" else ""
            directives.append(f"⚠️ {pair_txt} : jet {roll} (cible {target:.0f}) → {grade}. Dégrade la diplomatie "
                              f"d'un cran{extra} dans FMG.")
        elif kind == "rapprochement":
            grade = "alliance proposée" if outcome == "critique" else ("traité d'amitié" if outcome == "succes" else "simple dégel")
            directives.append(f"🤝 {pair_txt} : jet {roll} (cible {target:.0f}) → {grade}. Améliore la diplomatie "
                              f"d'un cran (deux si alliance) dans FMG.")
        elif kind == "guerre":
            if outcome in ("critique", "succes"):
                directives.append(f"⚔️ {pair_txt} : jet {roll} (cible {target:.0f}) → guerre déclarée"
                                  f"{' avec une offensive éclair' if outcome=='critique' else ''}. "
                                  f"Passe leur diplomatie mutuelle à Enemy dans FMG.")
            else:
                directives.append(f"— {pair_txt} : jet {roll} (cible {target:.0f}) → tensions vives mais pas "
                                  f"(encore) de déclaration de guerre.")
        elif kind == "coalition":
            if outcome in ("critique", "succes"):
                ampleur = " en masse, mobilisation totale" if outcome == "critique" else ""
                directives.append(f"🛡️ {chk['description']} : jet {roll} (cible {target:.0f}) → "
                                  f"{a_name} entre en guerre{ampleur}. Passe la diplomatie {pair_txt} "
                                  f"à Enemy dans FMG (un nouveau front apparaîtra au prochain tour).")
            else:
                directives.append(f"— {chk['description']} : jet {roll} (cible {target:.0f}) → "
                                  f"{a_name} reste en dehors du conflit pour l'instant.")
        elif kind == "penurie":
            bien = chk.get("bien", "?")
            grade = "famine/rupture totale" if outcome == "critique" else ("pénurie sensible" if outcome == "succes" else "tensions sur les prix")
            directives.append(f"📉 {a_name} ({bien}) : jet {roll} (cible {target:.0f}) → {grade}."
                              + (" Tu peux réduire encore le stock de ce bien dans l'éditeur de marché si tu veux le matérialiser (facultatif)." if outcome != "partiel" else ""))
        elif kind == "boom_commercial":
            bien = chk.get("bien", "?")
            grade = "âge d'or commercial" if outcome == "critique" else ("boom confirmé" if outcome == "succes" else "embellie modeste")
            directives.append(f"📈 {a_name} ({bien}) : jet {roll} (cible {target:.0f}) → {grade}."
                              + (" Tu peux augmenter le stock/prix de ce bien dans l'éditeur de marché si tu veux le matérialiser (facultatif)." if outcome != "partiel" else ""))
        elif kind == "embargo":
            grade = "rupture commerciale totale" if outcome == "critique" else ("embargo" if outcome == "succes" else "échanges au ralenti")
            directives.append(f"🚫 {pair_txt} : jet {roll} (cible {target:.0f}) → {grade}."
                              + (" Tu peux réduire les stocks/prix échangés dans l'éditeur de marché si tu veux le matérialiser (facultatif, aucune action obligatoire)." if outcome != "partiel" else ""))
        elif kind == "revolte":
            grade = "insurrection ouverte" if outcome == "critique" else ("soulèvement" if outcome == "succes" else "grogne")
            directives.append(f"🔥 {chk['description']} : jet {roll} (cible {target:.0f}) → {grade}."
                              + (" Ajoute une zone 'Rebels' sur une province dans l'éditeur de Zones." if outcome != "partiel" else ""))
        elif kind == "essor":
            grade = "âge d'or" if outcome == "critique" else ("boom économique" if outcome == "succes" else "léger regain")
            directives.append(f"🌟 {a_name} : jet {roll} (cible {target:.0f}) → {grade}.")

    return events, directives

# ============================================================ CLI
def cmd_snapshot(a):
    m = AzgaarMap.load(a.map)
    print(json.dumps(world_snapshot(m), ensure_ascii=False, indent=1))

def cmd_report(a):
    m = AzgaarMap.load(a.map)
    fp = read_fp(m)
    if not fp:
        print(json.dumps({"statut": "aucune partie en cours (lancer 'checks' pour commencer)"}, ensure_ascii=False))
        return
    pending = fp.get("pendingChecks")
    print(json.dumps({"annee": m.options.get("year"),
                      "jetsEnAttente": [c["id"] for c in pending] if pending else None,
                      "guerresSuivies": list(fp.get("warScores", {}).keys())},
                     ensure_ascii=False, indent=1))

def cmd_chronicle(a):
    """Exporte la chronique (note gmworlds-chronicle) en fichier Markdown propre.
    Lecture pure — n'écrit rien dans le .map, ne touche à aucune donnée de jeu."""
    m = AzgaarMap.load(a.map)
    html = read_note(m, CHRON_NOTE)
    if not html:
        sys.exit("Aucune chronique sur cette carte (lancer 'checks'/'resolve' au moins une fois).")
    title = a.title or f"Chronique de {m.map_name}"
    md = chronicle_to_markdown(html, title)
    out = a.out or "chronique.md"
    Path(out).write_text(md, encoding="utf-8")
    n_annees = len(re.findall(r"^## ", md, re.M))
    print(json.dumps({"fichier": out, "annees": n_annees, "taille_car": len(md)}, ensure_ascii=False))

def cmd_checks(a):
    """Étape 1 : énumère les jets à faire pour le tour à venir. N'écrit que le
    bilan (pendingChecks), jamais les données de jeu. Florian lance les d100."""
    m = AzgaarMap.load(a.map)
    out = a.out or a.map
    fp = read_fp(m) or {"seed": random.randrange(10**9), "warScores": {}, "peaceCooldown": {}}

    if fp.get("pendingChecks") and not a.force:
        print(json.dumps({
            "statut": "des jets sont déjà en attente (non résolus) — les revoici ; "
                     "utilise --force pour les recalculer",
            "jetsAFaire": [c["annonce"] for c in fp["pendingChecks"]],
            "suggestionsSansJet": fp.get("pendingInfo", []),
        }, ensure_ascii=False, indent=1))
        return

    snap_before = world_snapshot(m)
    changements = diff_snapshots(fp.get("lastSnapshot"), snap_before)
    next_year = m.options.get("year", 0) + a.years_per_turn
    pending, info = build_pending_checks(m, fp, a.chaos, max_battles=a.max_batailles)

    fp["pendingChecks"] = pending
    fp["pendingInfo"] = info
    fp["pendingMeta"] = {"year": next_year, "chaos": a.chaos}
    write_fp(m, fp)
    m.save(out)

    print(json.dumps({
        "fichier": out,
        "changementsDetectes": changements,
        "anneeProchaine": next_year,
        "jetsAFaire": [c["annonce"] for c in pending] or ["Aucun jet nécessaire ce tour."],
        "suggestionsSansJet": info,
    }, ensure_ascii=False, indent=1))

def cmd_resolve(a):
    """Étape 2 : Florian a lancé ses d100, on interprète. Écrit uniquement le
    bilan + la chronique (jamais les données de jeu)."""
    m = AzgaarMap.load(a.map)
    out = a.out or a.map
    fp = read_fp(m)
    if not fp or not fp.get("pendingChecks"):
        sys.exit("Aucun jet en attente : lancer 'checks' d'abord.")

    rolls = {}
    for item in a.rolls.split(","):
        item = item.strip()
        if not item:
            continue
        k, v = item.split("=")
        rolls[k.strip()] = int(v.strip())

    year = fp["pendingMeta"]["year"]
    events, directives = resolve_checks(m, fp, fp["pendingChecks"], rolls, year)

    opts = m.options; opts["year"] = year; m.set_options(opts)
    fp["lastSnapshot"] = world_snapshot(m)
    fp.pop("pendingChecks", None)
    fp.pop("pendingInfo", None)
    fp.pop("pendingMeta", None)
    write_fp(m, fp)
    # La chronique ne garde que ce qui s'est RÉELLEMENT passé ("jet non fourni" =
    # rien à raconter, juste une info opérationnelle pour ce tour — utile dans
    # les directives affichées à Florian, pas dans un historique à relire/exporter)
    chronicle_lines = [l for l in directives if not l.startswith("(jet non fourni")]
    append_chronicle(m, chronicle_lines or ["Année calme : aucun développement notable."], year)
    m.save(out)

    print(json.dumps({"fichier": out, "annee": year, "evenements": events, "directives": directives},
                     ensure_ascii=False, indent=1))

def cmd_advance(a):
    """Mode SECONDAIRE : dés internes (pas ceux de Florian), pour avancer vite
    ou tester. Le flux principal du skill est checks -> resolve avec les d100
    de Florian ; n'utiliser 'advance' que pour du remplissage/test."""
    m = AzgaarMap.load(a.map)
    out = a.out or a.map
    fp = read_fp(m) or {"seed": random.randrange(10**9), "warScores": {}, "peaceCooldown": {}}
    rng = random.Random(a.seed if a.seed is not None else fp["seed"] + m.options.get("year", 0))

    all_reports = []
    for _ in range(a.n):
        snap_before = world_snapshot(m)
        changements = diff_snapshots(fp.get("lastSnapshot"), snap_before)
        year = m.options.get("year", 0) + a.years_per_turn
        pending, info = build_pending_checks(m, fp, a.chaos, max_battles=a.max_batailles)
        auto_rolls = {c["id"]: rng.randint(1, 100) for c in pending}
        events, directives = resolve_checks(m, fp, pending, auto_rolls, year)
        opts = m.options; opts["year"] = year; m.set_options(opts)
        fp["lastSnapshot"] = world_snapshot(m)
        all_reports.append({"annee": year, "changementsDetectes": changements,
                            "evenements": events, "directives": directives})
        chronicle_lines = [l for l in directives if not l.startswith("(jet non fourni")]
        append_chronicle(m, chronicle_lines or ["Année calme : aucun développement notable."], year)

    write_fp(m, fp)
    m.save(out)
    print(json.dumps({"fichier": out, "tours": all_reports}, ensure_ascii=False, indent=1))

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("snapshot"); sp.add_argument("map"); sp.set_defaults(func=cmd_snapshot)
    rp = sub.add_parser("report"); rp.add_argument("map"); rp.set_defaults(func=cmd_report)

    chp = sub.add_parser("chronicle")
    chp.add_argument("map"); chp.add_argument("--out")
    chp.add_argument("--title")
    chp.set_defaults(func=cmd_chronicle)

    cp = sub.add_parser("checks")
    cp.add_argument("map"); cp.add_argument("--out")
    cp.add_argument("--chaos", type=float, default=1.0)
    cp.add_argument("--years-per-turn", type=int, default=1)
    cp.add_argument("--max-batailles", type=int, default=6, dest="max_batailles")
    cp.add_argument("--force", action="store_true")
    cp.set_defaults(func=cmd_checks)

    rz = sub.add_parser("resolve")
    rz.add_argument("map"); rz.add_argument("--out")
    rz.add_argument("--rolls", required=True,
                    help="id=valeur,id=valeur,... (ids donnés par 'checks')")
    rz.set_defaults(func=cmd_resolve)

    ap_ = sub.add_parser("advance")
    ap_.add_argument("map"); ap_.add_argument("--out")
    ap_.add_argument("-n", type=int, default=1)
    ap_.add_argument("--seed", type=int)
    ap_.add_argument("--chaos", type=float, default=1.0)
    ap_.add_argument("--years-per-turn", type=int, default=1)
    ap_.add_argument("--max-batailles", type=int, default=6, dest="max_batailles")
    ap_.set_defaults(func=cmd_advance)

    a = ap.parse_args()
    a.func(a)

if __name__ == "__main__":
    main()
