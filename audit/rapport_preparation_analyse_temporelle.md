# Rapport de préparation de l’analyse temporelle — OCS GE Lot (D046)

Date : 2026-11-25

## Bilan des opérations

Les deux ressources IGN expressément demandées ont été vérifiées sur les
endpoints officiels de la Géoplateforme, téléchargées et extraites. Les
archives d’origine sont conservées; aucun autre jeu de données n’a été
téléchargé. Les documentations officielles OCS GE utilisées pour l’audit
ont été consultées séparément et ne sont pas des jeux de données du projet.

| Produit | Archive | GeoPackage extrait | Entités | CRS |
|---|---|---|---:|---|
| Différentiel OCS GE 2022–2025 | 2 447 609 octets | `DIFF_D046_2025_2022.gpkg` | 13 967 | EPSG:2154 |
| Différentiel Artificialisation 2022–2025 | 1 003 459 octets | `zan_evol_2022_2025_46.gpkg` | 5 835 | EPSG:2154 |

Les empreintes SHA-256, chemins, licences, millésimes, dates, effectifs et
transformations sont dans [`manifest_differentiels.csv`](manifest_differentiels.csv).
Le dictionnaire de données est
[`dictionnaire_differentiels.csv`](dictionnaire_differentiels.csv).

## Contrôles réussis

- Les deux archives sont lisibles; chaque archive contient un GeoPackage,
  extrait dans son propre sous-dossier.
- Les deux GeoPackages sont ouvrables avec Pyogrio; les couches et champs
  physiques SQLite ont été inventoriés.
- Les géométries réelles ont été inspectées : 13 967 MultiPolygons OCS GE
  et 5 835 Polygons d’artificialisation; aucune géométrie nulle, vide ou
  invalide.
- Les deux produits et les limites ADMINEXPRESS-COG 2025 sont en
  EPSG:2154.
- Les identifiants non nuls du côté 2025 se retrouvent dans les couches
  complètes 2025; les attributs communs testés concordent sans écart.
- Le champ `surface` du différentiel d’artificialisation correspond, pour
  toutes les entités, à l’aire géométrique arrondie à 0,01 m².
- Les géométries des deux couches différentielles n’ont aucun recouvrement
  surfacique positif entre elles-mêmes. Toutes intersectent au moins une
  commune; les morceaux multicommunaux et résidus ont été comptés.
- Les archives 2025 et autres fichiers préexistants n’ont pas été écrasés.
  Aucun GeoPackage source n’a été ouvert en écriture.

## Anomalies et réserves

- Les champs 2022 `ID`, `CS`, `US` du différentiel OCS GE ont chacun
  26 valeurs nulles; les champs 2025 correspondants en ont chacun 5.
  Aucune normalisation ou interprétation en `NC` n’a été faite.
- Les identifiants sont répétés entre plusieurs morceaux du différentiel.
  Ils ne constituent pas une clé unique de ligne ou une preuve de
  correspondance un-à-un entre millésimes.
- Le snapshot complet 2022 et le patch correctif 2022 ne sont pas dans le
  périmètre téléchargé. Les états et géométries 2022 n’ont donc pas été
  comparés à ces sources complètes.
- Le différentiel OCS GE est une union géométrique avec topologie rapprochée
  à 0,1 m et sélection des changements de CS/US/ossature, selon le
  descriptif IGN de juin 2026. Il ne mesure pas à lui seul toutes les
  évolutions de formes ou toutes les transformations physiques.
- Le champ `artificialisation` (+1/-1) suit exactement les deux transitions
  `non artif`→`artif` et `artif`→`non artif` observées, mais sa définition
  attributaire officielle n’a pas été retrouvée. Le champ `surface` est
  validé empiriquement contre la géométrie; sa définition normative et son
  unité explicite restent à confirmer.
- 148 géométries OCS GE et 36 d’artificialisation sont multicommunales.
  39 et 2 géométries respectivement ont des résidus positifs de couverture
  supérieurs à 0,01 m². Ces résidus ne sont ni corrigés ni redistribués;
  leur cause n’est pas établie.
- Les limites utilisées sont ADMINEXPRESS-COG 2025. Aucun code EPCI n’est
  disponible dans la couche communale dérivée actuelle; aucune autre limite
  n’a été téléchargée.
- Aucune mesure surfacique d’évolution par commune/EPCI, aucun indicateur
  d’artificialisation persistante, aucune donnée touristique et aucune
  causalité n’ont été calculés.

## Fichiers produits et conservés

Archives conservées dans `data/raw/ocsge/archives/` :

- `OCS-GE_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15.7z`
- `OCS-GE-ARTIFICIALISATION_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15.7z`

GeoPackages extraits sous `data/raw/ocsge/differentials/` :

- `ocsge_2022_2025_D046/…/DIFF_D046_2025_2022.gpkg`
- `artificialisation_2022_2025_D046/…/zan_evol_2022_2025_46.gpkg`

Les rapports ne remplacent ni les audits de qualité antérieurs ni les
GeoPackages contrôlés 2025. Aucun GeoPackage dérivé supplémentaire n’a été
créé : les champs et identifiants d’origine sont ainsi préservés et aucune
répartition communale non validée n’est incorporée aux sources.

## État de préparation

Les différentiels sont utilisables pour préparer des comparaisons de
transitions OCS et de changements de statut, sous réserve d’appliquer une
méthode surfacique fondée sur les géométries et de conserver les résidus.
Le différentiel seul ne donne pas les surfaces restées artificialisées.
Avant les agrégations, il reste à obtenir/valider le snapshot et le patch
2022, à confirmer les définitions de `surface` et `artificialisation`, et à
choisir le traitement des résidus de couverture. L’analyse EPCI nécessite un
référentiel de codes EPCI millésimé. Les liens avec le tourisme devront
reposer sur des projets et dates documentés; la proximité ne constitue pas
une preuve de causalité.

## Références officielles

- [IGN, Descriptif de contenu OCS GE NG — juin 2026](https://data.geopf.fr/annexes/ressources/documentation/DC_OCSGE_NG.pdf).
- [IGN, Descriptif de livraison OCS GE NG — juin 2026](https://data.geopf.fr/annexes/ressources/documentation/DL_OCSGE_NG.pdf).
- [Fiche OCS GE cartes.gouv.fr](https://cartes.gouv.fr/rechercher-une-donnee/dataset/IGNF_OCS-GE).
- [Fiche OCS GE Artificialisation data.gouv.fr](https://www.data.gouv.fr/datasets/ocs-ge-artificialisation), licence `lov2`.
