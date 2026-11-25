# Audit du différentiel OCS GE Artificialisation 2022–2025 — Lot (D046)

Date de traitement : 2026-11-25

## Source et récupération

Ressource officielle IGN/Géoplateforme :
[`OCS-GE-ARTIFICIALISATION_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15.7z`](https://data.geopf.fr/telechargement/download/OCSGE-ARTIFICIALISATION/OCS-GE-ARTIFICIALISATION_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15/OCS-GE-ARTIFICIALISATION_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15.7z).
L’API Atom IGN confirme le secteur D046, le GeoPackage et EPSG:2154. La
ressource est mise à jour le 15/10/2026 à 14:59 selon l’API; `editionDate`
est `2025-01-01`, tandis que la période 2022–2025 apparaît dans le nom et
dans les champs du fichier. La date de première publication n’est pas
fournie séparément.

La requête HTTP `HEAD` a répondu `200 OK`, type
`application/x-7z-compressed`, taille **1 003 459 octets**. L’archive,
téléchargée le 25/11/2026, est conservée dans
`data/raw/ocsge/archives/`; elle contient
`zan_evol_2022_2025_46.gpkg`, extrait dans :

`data/raw/ocsge/differentials/artificialisation_2022_2025_D046/OCS-GE-ARTIFICIALISATION_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15/zan_evol_2022_2025_46.gpkg`

La fiche [OCS GE Artificialisation de data.gouv.fr](https://www.data.gouv.fr/datasets/ocs-ge-artificialisation)
déclare la licence `lov2` (Licence Ouverte 2.0 / Etalab 2.0). Elle décrit
l’artificialisation selon l’article L. 101-2-1 du code de l’urbanisme et le
décret n° 2023-1096 du 27 novembre 2023; le calcul repose notamment sur le
croisement de la couverture et de l’usage du sol. Le flux officiel de
téléchargement donne également le sous-titre :
« Couche d'artificialisation des sols, calculée à partir des données OCS GE,
selon le décret 2023-1096 […] relatif à l'évaluation et au suivi de
l'artificialisation (ZAN). »

## Audit du GeoPackage

| Mesure | Résultat |
|---|---:|
| Couche | `zan_evol_2022_2025_46` |
| Entités | 5 835 |
| CRS déclaré et utilisé | EPSG:2154 |
| Type de géométrie déclaré | `GEOMETRY` / `Unknown` |
| Type réel | 5 835 Polygon |
| Géométries nulles / vides / invalides | 0 / 0 / 0 |
| Composants par géométrie | 1 pour chaque polygone |
| Emprise (EPSG:2154) | X 541 312,41–636 257,16; Y 6 347 538,94–6 439 039,15 |

La déclaration générique `GEOMETRY` n’est pas considérée comme une anomalie :
les géométries réelles ont été lues et sont toutes des Polygon. Le GeoPackage
ne possède pas de table `gpkg_data_columns` donnant des définitions
attributaires supplémentaires. Le schéma, les types SQLite, les nulls et
les constats de valeurs sont détaillés dans
[`dictionnaire_differentiels.csv`](dictionnaire_differentiels.csv).

## États et champ de transition

Les 5 835 lignes présentent deux transitions observées :

| `artif_2022` | `artif_2025` | `artificialisation` observé | Lignes |
|---|---|---:|---:|
| `non artif` | `artif` | 1 | 4 977 |
| `artif` | `non artif` | -1 | 858 |

Le champ `artif_*` et les états de la fiche du jeu permettent de distinguer
les deux directions. Le champ numérique `artificialisation` correspond
exactement à +1 ou -1 selon cette direction dans le fichier contrôlé.
Toutefois, la documentation officielle consultée ne définit pas explicitement
ce champ comme une surface, un taux ou un « solde » : sa signification
normative n’est donc pas affirmée ici. Il n’est pas utilisé seul pour
produire un indicateur.

Aucune ligne de ce différentiel ne conserve le même état `artif` entre 2022
et 2025. Il s’agit donc d’une couche de transitions d’état dans le fichier
livré; elle ne permet pas de mesurer la surface restée artificialisée. Il
faudrait les couches complètes d’artificialisation des deux millésimes pour
calculer cet état persistant.

## Surface

Le champ `surface` est numérique, non nul et strictement positif (minimum
6,24; maximum 137 788,47). Pour les **5 835** entités, il est égal à l’aire
planaire de la géométrie en EPSG:2154 arrondie à deux décimales. L’écart
absolu non arrondi maximal observé est inférieur à 0,005 m²; cela concorde
avec un arrondi au centième.

La documentation de produit consultée ne fournit pas de définition
attributaire explicite de `surface`. L’interprétation empirique est donc
« aire géométrique arrondie au centième », vraisemblablement en m² compte
tenu du CRS métrique; l’unité normative reste à confirmer dans une
documentation de livraison spécifique à ce champ. Le champ original n’a
pas été modifié.

## Comparaison avec la couche complète 2025

Les 5 835 lignes et les 5 150 identifiants `id_2025` distincts ont été
retrouvés dans `artif_2025_46` 2025. Les attributs `artif_2025`,
`cs_2025` et `us_2025` correspondent aux champs `artif`, `code_cs` et
`code_us` de la couche 2025 : aucun écart n’a été observé. Les 3 846
identifiants `id_2022` distincts sont répétés entre plusieurs lignes et ne
sont pas des clés uniques de lignes différentielles.

Les géométries ne sont pas comparées comme si chaque polygone différentiel
était le polygone complet de 2025 : la couche est un différentiel. Le
snapshot complet 2022 n’a pas été téléchargé dans cette mission; il n’est
donc pas possible de contrôler indépendamment les attributs ou géométries
2022, ni l’effet du patch correctif 2022.

## Compatibilité spatiale avec les communes

Le contrôle utilise les 312 communes ADMINEXPRESS-COG 2025 déjà présentes,
en EPSG:2154 :

- 5 871 relations d’intersection surfacique positive; aucune géométrie sans
  intersection positive;
- 36 géométries intersectent plusieurs communes, au maximum 2;
- 2 géométries ont un écart positif supérieur à 0,01 m² entre leur aire et
  la somme des intersections communales; maximum : 0,604 m²;
- aucun écart négatif inférieur à -0,01 m²;
- aucun recouvrement surfacique positif entre deux géométries de cette
  couche.

Les résidus sont conservés comme réserve, sans correction ni répartition
arbitraire. Les relations communales sont plusieurs-à-plusieurs; une future
agrégation devra répartir la surface mesurée par intersection géométrique,
conserver les identifiants d’origine et documenter les écarts.

## Ce que ces données permettent — et ne permettent pas

Les transitions présentes peuvent servir à préparer une mesure surfacique
des changements de statut, en utilisant les géométries et après validation
de la définition du champ `surface`. Les comptes de lignes ne sont pas des
surfaces. Le différentiel ne mesure pas à lui seul l’artificialisation
persistante, la consommation d’ENAF ou l’origine touristique d’un changement.
Aucun total de surface, indicateur communal ou indicateur touristique n’a
été calculé.

## Références

- [Fiche OCS GE Artificialisation — data.gouv.fr](https://www.data.gouv.fr/datasets/ocs-ge-artificialisation), licence `lov2` et description du cadre légal.
- [API de téléchargement IGN, flux OCS GE Artificialisation D046](https://data.geopf.fr/telechargement/resource/OCSGE-ARTIFICIALISATION?zone=D046).
- [Article L. 101-2-1 du code de l’urbanisme](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043967077).
- [Décret n° 2023-1096 du 27 novembre 2023](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000048465959).
