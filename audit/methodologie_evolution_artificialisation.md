# Méthodologie proposée — évolution OCS GE et artificialisation 2022–2025

## Objet et garde-fous

Ce document prépare une analyse ultérieure; il ne présente aucun total
territorial d’évolution. Les deux couches différentielles sont conservées
dans `data/raw/ocsge/differentials/`. Aucun nouvel indicateur n’a été
calculé et aucun GeoPackage source n’a été modifié.

Ne pas confondre :

- **occupation du sol** : description par codes de couverture (`CS`) et
  d’usage (`US`);
- **artificialisation** : classement selon le cadre légal et le croisement
  couverture/usage défini par les documents officiels;
- **consommation d’ENAF** : mesure distincte qui ne se déduit pas
  automatiquement d’un changement OCS GE ou d’un changement
  d’artificialisation.

Les changements de code ne sont pas une preuve d’une nouvelle construction
ni de leur cause. Les données IGN reposent sur des millésimes et une méthode
de production; le différentiel OCS GE rapproche les géométries selon une
tolérance topologique de 0,1 m, puis sélectionne les différences de CS, US
et/ou ossature.

## Mesures potentielles et conditions

| Question | Source / transition | Mesure proposée | Conditions et limites |
|---|---|---|---|
| Surfaces devenues artificialisées | `artif_2022 = non artif` → `artif_2025 = artif` | Aire de chaque géométrie différentielle; comparer au champ `surface` | Champ `surface` égale empiriquement l’aire géométrique arrondie à 0,01 m², mais sa définition normative n’a pas été trouvée. Ne pas publier de total avant validation de cette définition et de la méthode d’agrégation. |
| Surfaces sorties des catégories artificialisées | `artif_2022 = artif` → `artif_2025 = non artif` | Aire des géométries de transition | Même réserve de définition et de méthode; ne pas assimiler à une renaturation sans source supplémentaire. |
| Surfaces restées artificialisées | États identiques aux deux dates | Comparaison des couches complètes 2022 et 2025 | Non mesurable avec le seul différentiel livré : aucune ligne à état `artif` identique n’y a été observée. Le snapshot complet 2022 n’a pas été téléchargé. |
| Changements de couverture | `CS_2022` → `CS_2025` | Aire de géométrie par paire de codes | Utiliser l’aire géométrique, pas le nombre de lignes. Conserver les codes et leur nomenclature versionnée; distinguer changement de classification et changement physique. |
| Changements d’usage | `US_2022` → `US_2025` | Aire de géométrie par paire de codes | Même réserve. Ne pas assigner de libellé sans nomenclature officielle correspondant à la version. |
| Changements d’ossature | `OSS_2022` → `OSS_2025` | Aire par transition 0/1 après validation des cas | Le descriptif IGN définit 0 = hors ossature et 1 = dans l’ossature; l’ossature est une couche d’appui/réseaux, pas un indicateur d’artificialisation. |
| Comparaison par commune | Géométrie différentielle × commune ADMINEXPRESS-COG 2025 | Aire d’intersection de chaque morceau avec chaque commune | Relation plusieurs-à-plusieurs. Aucune commune unique n’est imposée; conserver les résidus de couverture et les IDs de ligne et de millésime. |
| Comparaison par EPCI | Codes communaux vers EPCI | Somme des aires communales par code EPCI contrôlé | Le jeu communal dérivé actuel ne comporte pas de code EPCI. Obtenir et vérifier un référentiel administratif de millésime compatible avant agrégation; aucun nouveau jeu n’a été téléchargé. |

## Procédure surfacique communale à appliquer après validation

1. Lire les GeoPackages différentiels et confirmer le CRS métrique
   EPSG:2154; préserver la ligne et tous les champs d’identifiants/états.
2. Utiliser un index spatial pour trouver les communes intersectées par
   chaque géométrie différentielle.
3. Calculer `intersection(geometry_diff, geometry_commune).area` pour
   chaque paire; conserver seulement les aires positives et enregistrer
   toutes les relations.
4. Contrôler pour chaque géométrie
   `aire_source - somme(aire_intersection)`. Ne pas supprimer ni répartir
   les résidus; ne pas normaliser les parts sans décision explicite.
5. Compter une même ligne différentielle dans plusieurs communes seulement
   pour la table de relations; sommer ses **aires d’intersection** pour les
   superficies communales. Ne jamais recopier l’aire entière de l’objet
   dans chaque commune.
6. Vérifier l’absence de recouvrement positif entre morceaux d’un même
   différentiel avant de sommer les géométries brutes. Ce contrôle a été
   réalisé pour les couches actuelles et aucun recouvrement n’a été détecté.
7. Conserver séparément le rattachement par centroïde, les intersections
   surfaciques et un éventuel découpage. Le centroïde n’est pas une méthode
   de répartition de surface; aucun découpage n’est nécessaire pour
   calculer les intersections.

Sur les limites communales déjà présentes, 148 morceaux OCS GE (maximum
6 communes) et 36 morceaux d’artificialisation (maximum 2 communes)
intersectent plusieurs communes. Aucun morceau n’est sans intersection
positive. Des résidus supérieurs à 0,01 m² restent observés dans 39 morceaux
OCS GE et 2 morceaux d’artificialisation; leur cause n’est pas établie.

## Conditions de comparabilité et données manquantes

- Les valeurs 2025 des identifiants différentiels ont été retrouvées dans
  les couches complètes 2025 et leurs attributs communs concordent.
- Les identifiants 2022 sont répétés et ne sont pas une clé unique de
  transition. Le snapshot complet 2022 et son patch correctif ne font pas
  partie des données téléchargées; leur validation indépendante et
  l’évaluation de l’effet du correctif restent à faire.
- Le descriptif IGN explique que le différentiel OCS GE est limité aux
  différences CS/US/ossature et résulte d’une union topologique. Il ne
  constitue pas une détection exhaustive de tous les changements de forme
  ou d’occupation réelle.
- Pour l’artificialisation, la correspondance constatée de `surface` avec
  l’aire géométrique est vérifiée; la définition documentaire explicite de
  `surface` et du champ signé `artificialisation` reste à obtenir. Avant
  l’agrégation, privilégier la géométrie différentielle et consigner
  précisément la règle d’interprétation.
- Les limites 2025 utilisées produisent des résidus de couverture; les
  résultats communaux devront les rapporter.
- Un code EPCI valide et son millésime ne sont pas disponibles dans la
  couche communale dérivée actuelle.

## Préparation du futur croisement touristique — sans exécution

Pour chaque hébergement, site ou équipement (hôtel, camping, résidence,
village de vacances, hébergement collectif, site touristique, loisirs,
montagne, remontée mécanique, parking, infrastructure ou projet), conserver
au minimum : identifiant/source, géométrie ou adresse géocodée, dates
connues de création, ouverture, extension et fermeture, emprise/surface si
disponible, millésime et fiabilité.

Classer ensuite les observations sans inférence causale :

1. transformation directement reliée à un projet touristique documenté;
2. transformation proche d’un équipement touristique, sans preuve de lien;
3. transformation d’origine inconnue;
4. transformation reliée à une autre activité documentée.

La proximité spatiale seule ne démontre ni causalité ni contribution
touristique. Aucun jeu touristique n’a été téléchargé ou croisé dans la
présente mission.

## Références

- [IGN, Descriptif de contenu OCS GE NG — juin 2026](https://data.geopf.fr/annexes/ressources/documentation/DC_OCSGE_NG.pdf), §1.1.4, p. 9–10; définition de l’ossature, p. 25.
- [IGN, Descriptif de livraison OCS GE NG — juin 2026](https://data.geopf.fr/annexes/ressources/documentation/DL_OCSGE_NG.pdf), §2.3, p. 7–8.
- [OCS GE Artificialisation — data.gouv.fr](https://www.data.gouv.fr/datasets/ocs-ge-artificialisation).
- [Décret n° 2023-1096 du 27 novembre 2023](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000048465959).
