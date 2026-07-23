# SIDC — code symbole APP-6D / MIL-STD-2525D (20 chiffres)

Le `sidc` encode le symbole militaire d'une unité. Structure **vérifiée** sur les
fichiers de Florian. Pour lire un symbole depuis une image, on identifie ces champs
visuellement puis on les recompose ; pour écrire, on assemble les 20 chiffres.

## Positions

```
 1 2 | 3 | 4 | 5 6 | 7 | 8 | 9 10 | 11 12 13 14 15 16 | 17 18 | 19 20
 ver   ctx id   set  st  hq  éch.       entité (icône)     mod1    mod2
```

| Champ | Pos | Valeurs |
|-------|-----|---------|
| Version | 1-2 | `10` (2525D / APP-6D éd.1) |
| Contexte | 3 | `0` réalité · `1` exercice · `2` simulation |
| **Identité** | 4 | `0` pending · `1` inconnu · `2` ami présumé · **`3` ami** · `4` neutre · `5` suspect · `6` hostile |
| **Symbol set** | 5-6 | **`10` unité terrestre** · `11` civil terrestre · `15` équipement terrestre · `20` installation · `01` air · `30` mer surface · `35` sous-marin · `05` espace |
| Statut | 7 | `0` présent · `1` planifié/anticipé |
| HQ/TF/Dummy | 8 | `0` aucun · (combinaisons pour QG, task force, leurre) |
| **Échelon** | 9-10 | voir table ci-dessous |
| **Entité** | 11-16 | icône principale, 6 chiffres (entité·type·sous-type) |
| Modificateur 1 | 17-18 | capacité/arme (ex. `56` mitrailleuse) |
| Modificateur 2 | 19-20 | second modificateur (ex. `51` …) |

## Table des échelons (pos 9-10) — vérifiée

| Code | Échelon (FR) | Note |
|------|--------------|------|
| `11` | Équipe / Crew | |
| `12` | Escouade / Groupe | |
| `13` | Section (sens US) | |
| `14` | **Section (FR)** / Peloton | = *platoon* |
| `15` | **Compagnie** / Batterie / Escadron | |
| `16` | **Bataillon** | |
| `17` | **Régiment** / Groupement | |
| `18` | **Brigade** | |
| `21` | **Division** | |
| `22` | Corps | |
| `23` | Armée | |
| `24` | Groupe d'armées | |
| `26` | Commandement | |

⚠️ Piège FR/EN : en français, **« Section » = peloton = `14`** et **« Compagnie » = `15`**.

## Entité (pos 11-16)

6 chiffres = entité · type · sous-type. Pour les unités terrestres (`set=10`), les blocs
les plus courants chez Florian :

| Entité | Signification (d'après usage) |
|--------|-------------------------------|
| `121100` | Infanterie |
| `121000` | Infanterie blindée / mécanisée |
| `121105` | Infanterie mécanisée sur IFV (*MECH IFV DIV/BDE/BN*) |
| `121102` | Infanterie mécanisée sur APC/VAB |
| `120400` | Anti-char (ATGM) |
| `120500` | **Blindés / chars / cavalerie** (*TANK BN/BDE, Cuirassiers, Hussards, Peleton Char*) |
| `120502` | Char léger (*152 TANK BN LT*) |
| `120501` | Reconnaissance |
| `120600` | Aviation / opérations aériennes |
| `110600` | Influence / Information |
| `107000` | Police / sécurité (POL) |
| `000000` | Quartier général / regroupement générique (*Comp. Commandement, Etat Majors des Armées de Terre*) |

⚠️ **Il n'existe pas d'entité « état-major » propre.** Un QG de compagnie de chars porte
l'entité de sa compagnie (`120500`), un QG de batterie d'artillerie porte `130300`, etc. :
la sous-unité de commandement **hérite de l'entité du parent**. C'est pourquoi les noms
génériques (`HQ`, `CMD SEC`, `STAFF SEC`, `1 PLT`) apparaissent sous presque toutes les
entités du dictionnaire et **ne doivent jamais servir à déduire une entité**. `000000` est
réservé aux regroupements sans arme dominante.

La liste complète des entités est vaste. **Le dictionnaire réel extrait des ORBAT de
Florian est dans `references/sidc_dictionary.json`** (499 entrées : `sidc` → échelon,
entité, exemples de noms). C'est la première source à consulter pour réutiliser un code
cohérent avec son univers. Pour un type non couvert, partir de l'entité la plus proche
et n'ajuster que les modificateurs, ou demander confirmation à Florian.

## Lire un SIDC

`10031000151211005600` :
`10`·`0`·`3`·`10`·`0`·`0`·`15`·`121100`·`56`·`00`
→ ami, unité terrestre, **compagnie** d'**infanterie**, modificateur **mitrailleuse**.

## Écrire un SIDC

Utiliser `scripts/new_orbat.py:build_sidc(echelon, entity, identity='3')`. Par défaut :
version `10`, contexte réalité, set terrestre `10`, statut présent. Ne renseigner que
l'échelon (nom ou code) et l'entité (6 chiffres), plus modificateurs si besoin.
