# Audit du différentiel OCS GE 2022–2025 — Lot (D046)

Date de traitement : 2026-11-25

## Source et récupération

Ressource officielle IGN/Géoplateforme :
[`OCS-GE_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15.7z`](https://data.geopf.fr/telechargement/download/OCSGE/OCS-GE_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15/OCS-GE_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15.7z).
L’API Atom IGN confirme le produit, le secteur D046, le format GPKG,
EPSG:2154 et une mise à jour de la ressource au 15/10/2026 à 14:59
(heure indiquée par l’API). Le nom de la ressource indique la période
2022–2025; `editionDate` de l’entrée de différentiel est `2025-01-01`.
L’API ne fournit pas de date de première publication distincte.

La requête HTTP `HEAD` a répondu `200 OK`, type
`application/x-7z-compressed`, taille **2 447 609 octets**. L’archive a été
téléchargée le 25/11/2026; son SHA-256 est dans
[`manifest_differentiels.csv`](manifest_differentiels.csv). Elle contient
un GeoPackage, extrait sans modification dans :

`data/raw/ocsge/differentials/ocsge_2022_2025_D046/OCS-GE_2-0_DIFF-2022-2025_GPKG_LAMB93_D046_2026-10-15/DIFF_D046_2025_2022.gpkg`

La licence indiquée pour le produit OCS GE est la Licence Ouverte 2.0
(`lov2` / Etalab 2.0); voir la fiche [OCS GE de cartes.gouv.fr](https://cartes.gouv.fr/rechercher-une-donnee/dataset/IGNF_OCS-GE)
et le jeu OCS GE diffusé sur [data.gouv.fr](https://www.data.gouv.fr/datasets/occupation-du-sol-a-grande-echelle-ocsge-format-geoparquet).

## Définition du différentiel selon l’IGN

Le descriptif de contenu IGN, *OCS GE NG*, juin 2026, §1.1.4, p. 9–10,
indique que les deux millésimes sont rapprochés sur une topologie commune
avec une tolérance d’agrégat de **0,1 m**, puis réunis géométriquement. La
couche résultante est filtrée pour ne conserver que les objets ayant une
différence de couverture, d’usage et/ou de valeur d’ossature. Le descriptif
de livraison, *OCS GE NG*, juin 2026, §2.3.1–2.3.2, p. 7–8, définit les
attributs par millésime : identifiant, code de couverture, code d’usage et
appartenance à l’ossature.

Il s’agit donc de géométries d’union associées à des états des deux
millésimes, et non de copies intégrales des objets 2022 ou 2025. Un
identifiant peut apparaître dans plusieurs morceaux d’un différentiel.
L’égalité géométrique directe entre un morceau différentiel et un objet
complet de 2025 n’est pas une condition attendue.

## Audit du GeoPackage

| Mesure | Résultat |
|---|---:|
| Couche | `DIFF_D046_2025_2022.shp` |
| Entités | 13 967 |
| CRS déclaré et utilisé | EPSG:2154 |
| Type déclaré | MultiPolygon |
| Type réel | 13 967 MultiPolygon |
| Géométries nulles / vides / invalides | 0 / 0 / 0 |
| Composants par géométrie | 13 556 à 1; 370 à 2; 33 à 3; 2 à 4; 5 à 5; 1 à 7 |
| Emprise (EPSG:2154) | X 540 518,52–636 852,49; Y 6 347 047,20–6 439 092,76 |

Le schéma SQL natif et les constats de valeurs champ par champ figurent dans
[`dictionnaire_differentiels.csv`](dictionnaire_differentiels.csv). Les champs
`ID_2022`, `CS_2022` et `US_2022` ont chacun 26 valeurs nulles; les champs
`ID_2025`, `CS_2025` et `US_2025` en ont chacun 5. Les deux champs `OSS_*`
n’ont aucune valeur nulle. Ces absences sont cantonnées aux attributs d’un
côté temporel de l’union; elles ne sont ni remplacées ni assimilées à `NC`.

Les identifiants sont répétés : 10 203 valeurs distinctes dans `ID_2022`
(3 738 occurrences au-delà de la première, hors 26 nulles) et 11 542 dans
`ID_2025` (2 420 occurrences au-delà de la première, hors 5 nulles). Ce
comportement est cohérent avec le découpage d’un même objet d’origine en
plusieurs parties du différentiel; il interdit de compter les lignes ou les
identifiants comme des surfaces.

## Comparaison avec la couche complète 2025

Les **13 962** lignes ayant un `ID_2025` non nul renvoient à **11 542**
identifiants distincts de `OCCUPATION_SOL` 2025. Tous ces identifiants ont
été retrouvés dans la couche source 2025. Pour chaque ligne différentielle
correspondante, les valeurs `CS_2025`, `US_2025` et `OSS_2025` concordent
avec `code_cs`, `code_us` et `ossature` de la couche 2025 : **aucun écart
d’attribut** observé. Les 5 lignes sans `ID_2025` n’ont pas de correspondant
2025 par identifiant.

Il n’y a pas de snapshot OCS GE complet 2022 dans le périmètre autorisé de
cette mission. La cohérence des valeurs et géométries 2022 n’a donc pas été
comparée à une couche complète 2022 ni à son patch correctif. Les deux
formulations documentaires de `US235` restent inchangées; les codes
différentiels sont conservés sans leur attribuer de libellé.

## Compatibilité spatiale avec les communes

Le contrôle a réutilisé les 312 limites ADMINEXPRESS-COG 2025 déjà présentes,
sans nouveau téléchargement ni découpage :

- CRS identique, EPSG:2154;
- 14 126 relations d’intersection surfacique positive;
- aucune des 13 967 géométries sans intersection positive;
- 148 géométries intersectent plusieurs communes, au maximum 6;
- 39 géométries ont un résidu supérieur à 0,01 m² entre leur aire et la
  somme de leurs intersections communales; maximum positif : 2 455,057 m²;
- aucun résidu inférieur à -0,01 m²;
- aucune paire de géométries différentielles ne présente de recouvrement
  surfacique positif.

Les résidus sont des portions non couvertes par l’union des polygones
communaux retenus; leur cause n’est pas établie. Ils ne sont pas redistribués
et ne prouvent pas une erreur dans OCS GE ou ADMINEXPRESS. Pour une analyse
ultérieure, il faudra conserver le rattachement plusieurs-à-plusieurs et
mesurer les aires d’intersection, sans affectation par centroïde ni
renormalisation arbitraire.

## Surfaces et réserves

Le GeoPackage ne contient pas de champ de surface. Une aire peut être
calculée à partir de la géométrie en EPSG:2154, en planimétrie et en m²,
mais elle mesure la surface des morceaux du différentiel définis par la
méthode de production IGN (dont le rapprochement topologique à 0,1 m). Aucun
total d’évolution n’a été calculé. Les géométries du différentiel sont
disjointes surfaciquement dans la couche contrôlée, ce qui évite un double
compte interne en sommant leurs aires; cela ne rend pas les millésimes
comparables au-delà des limites de la méthode IGN.

Les changements de code décrivent des évolutions de classification
couverture/usage/ossature. Ils ne démontrent pas à eux seuls une construction
récente, une artificialisation, une consommation d’ENAF ou une cause
touristique.

## Références

- [Descriptif de contenu OCS GE NG — juin 2026](https://data.geopf.fr/annexes/ressources/documentation/DC_OCSGE_NG.pdf), §1.1.4, p. 9–10.
- [Descriptif de livraison OCS GE NG — juin 2026](https://data.geopf.fr/annexes/ressources/documentation/DL_OCSGE_NG.pdf), §2.3.1–2.3.2, p. 7–8.
- [API de téléchargement IGN, flux OCS GE D046](https://data.geopf.fr/telechargement/resource/OCSGE?zone=D046).
