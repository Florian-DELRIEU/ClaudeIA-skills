---
name: infos-medecine
description: "Navigateur médical spécialisé à titre informatif pour Florian. Déclencher IMPÉRATIVEMENT dès que Florian tape /infos-medecine, ou pose une question médicale (médicament, dosage, posologie, interaction médicamenteuse, effet secondaire, contre-indication, pathologie, symptôme, vaccin, traitement, examen médical, ou toute question de santé où il cherche une information vérifiée). Consulte systématiquement TOUTES les sources prédéfinies (ANSM, base de données publique des médicaments, HAS, Ameli, EMA, OMS, Cochrane Library, VIDAL), compile les résultats, signale explicitement les convergences et divergences entre sources, et indique les précautions spécifiques pertinentes (interactions, populations à risque, contre-indications). Ne jamais répondre de mémoire seule sur un sujet médical sans consulter ces sources. Rappelle systématiquement que le contenu est informatif et ne remplace pas l'avis d'un pharmacien ou d'un médecin."
---

# Infos-médecine

Skill de navigation médicale à titre informatif pour Florian. L'objectif : consulter systématiquement une liste fixe de sources fiables/certifiées, compiler les informations, et signaler clairement ce qui converge, ce qui diverge, et les précautions à connaître.

## Liste des sources (à consulter systématiquement, dans cet ordre de priorité)

**Organismes publics / régulateurs (priorité maximale)**
1. **ANSM** — ansm.sante.fr — agence d'État française (médicaments, alertes, autorisations)
2. **Base de données publique des médicaments** — base-donnees-publique.medicaments.gouv.fr — notices et RCP officiels
3. **HAS** — has-sante.fr — recommandations officielles de bonnes pratiques
4. **Ameli** — ameli.fr — Assurance Maladie, conseils santé grand public
5. **EMA** — ema.europa.eu — agence européenne du médicament
6. **OMS** — who.int — organisme intergouvernemental

**Référence scientifique indépendante**
7. **Cochrane Library** — cochranelibrary.com — revues systématiques, très rigoureuses mais parfois techniques

**Source privée (à traiter avec précaution particulière)**
8. **VIDAL** — vidal.fr — référence professionnelle mais **entreprise privée, pas un régulateur**. Toujours :
   - Rappeler explicitement son statut commercial quand elle est citée
   - Croiser systématiquement ses informations avec au moins une source officielle (1-6) avant de les présenter comme fiables
   - Ne jamais la citer seule sur un point sensible (dosage, contre-indication majeure) sans confirmation par une source publique

## Protocole à suivre pour chaque question

1. **Recherche exhaustive** : consulter (via web_search / web_fetch) les 8 sources ci-dessus sur le sujet posé. Ne pas s'arrêter après 1-2 résultats si la question porte sur un médicament ou un dosage — chercher activement dans chaque source pertinente.
2. **Compilation** : synthétiser les informations trouvées, organisées par thème (ex : indication, posologie, contre-indications, effets secondaires, interactions).
3. **Convergences / divergences** : indiquer explicitement quand plusieurs sources s'accordent ("ANSM, HAS et OMS convergent sur...") et quand elles divergent ou nuancent différemment ("VIDAL mentionne X alors que l'ANSM ne le signale pas — à vérifier avec un pharmacien").
4. **Précautions spécifiques** : selon la question, signaler activement :
   - populations à risque (grossesse, allaitement, enfants, personnes âgées, insuffisance rénale/hépatique)
   - interactions médicamenteuses connues
   - contre-indications majeures
   - signaux d'alerte nécessitant une consultation urgente
5. **Citation systématique** : chaque information doit être rattachée à sa source d'origine.
6. **Rappel final** : toujours conclure en rappelant que la réponse est informative, ne remplace pas l'avis d'un professionnel de santé, et qu'en cas de doute ou de situation personnelle (autres traitements, antécédents), consulter un pharmacien ou un médecin.

## Ce que ce skill ne fait PAS

- Il ne donne pas de diagnostic.
- Il ne recommande pas de dosage personnalisé — il rapporte les dosages standards indiqués dans les sources officielles, en rappelant que l'adaptation individuelle relève du médecin/pharmacien.
- Il ne remplace pas une consultation en cas d'urgence (dans ce cas, orienter vers les services d'urgence : 15 / 112).
