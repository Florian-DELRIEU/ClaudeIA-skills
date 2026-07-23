# identification/ — apprendre à trouver l'acronyme

Module d'aide à l'**identification** : produire l'acronyme v4 *le plus évident* pour tout
véhicule ou élément de personnel, toute nation, toute époque.

- `METHODE.md` — le raisonnement : principe du châssis, pipeline, arbitrage « plus évident ».
- `chassis-types.md` — table châssis → Type (multi-nations, extensible).
- `personnel.md` — codage des éléments de personnel.
- `lexique.json` — registre `désignation réelle ↔ code v4`, amorcé depuis ORBAT 2023,
  enrichi à chaque cas résolu (garantit la cohérence inter-fichiers).
- `entrainement.md` — protocole du mode d'entraînement (Florian donne un nom, on
  identifie l'acronyme avec raisonnement détaillé, il note sur 5, on journalise les cas
  validés dans `lexique.json`).

Consulter ce dossier dès qu'il faut **attribuer** ou **vérifier** un acronyme à partir
d'une désignation réelle. À l'inverse (décoder un code existant), les tables de
`references/` suffisent.
