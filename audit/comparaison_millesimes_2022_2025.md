# Comparaison des différentiels et des couches 2025 — Lot (D046)

Date de traitement : 2026-11-25

## Périmètre

L’analyse porte sur les deux archives IGN explicitement autorisées et
téléchargées : le différentiel OCS GE et le différentiel OCS GE
Artificialisation 2022–2025. Les couches OCS GE et Artificialisation 2025
déjà présentes ont servi au contrôle des attributs de 2025. Aucune couche
complète 2022, aucun patch correctif 2022, aucune nouvelle limite
administrative et aucune donnée touristique n’ont été téléchargés.

Les ressources sont définies par l’API officielle de téléchargement
Géoplateforme, secteur D046, GeoPackage, EPSG:2154, ressource mise à jour le
15/10/2026. Les deux millésimes `2022` et `2025` figurent dans les noms de
ressource; l’API associe `editionDate=2025-01-01` aux entrées différentielles.
La date de première publication n’est pas fournie. La licence de ces
produits est la Licence Ouverte 2.0 (`lov2`).

## Résultats comparés

| Contrôle | Différentiel OCS GE | Différentiel Artificialisation |
|---|---:|---:|
| Couche | `DIFF_D046_2025_2022.shp` | `zan_evol_2022_2025_46` |
| Entités | 13 967 | 5 835 |
| Type réel | MultiPolygon | Polygon |
| EPSG | 2154 | 2154 |
| Nulles / vides / invalides | 0 / 0 / 0 | 0 / 0 / 0 |
| Valeurs nulles dans les attributs | 26 dans les champs 2022 ID/CS/US; 5 dans les champs 2025 ID/CS/US | 0 |
| Relations surfaciques communales | 14 126 | 5 871 |
| Entités intersectant plusieurs communes | 148, jusqu’à 6 communes | 36, jusqu’à 2 communes |
| Sans intersection surfacique positive | 0 | 0 |
| Écarts de couverture > 0,01 m² | 39, maximum +2 455,057 m² | 2, maximum +0,604 m² |
| Recouvrement positif entre géométries dans la couche | Aucun | Aucun |

## Identifiants et attributs de 2025

Les identifiants 2025 sont répétés dans les différentiels parce qu’un objet
du millésime peut être associé à plusieurs morceaux issus de l’union
géométrique. Ils ne sont donc pas des clés de ligne. Pour la comparaison,
les doublons ont été conservés; aucune entité n’a été supprimée.

- Dans le différentiel OCS GE, 13 962 lignes ont un `ID_2025` non nul,
représentant 11 542 identifiants distincts. Tous existent dans
`OCCUPATION_SOL` 2025; `CS_2025`, `US_2025` et `OSS_2025` concordent avec
`code_cs`, `code_us` et `ossature`.
- Dans le différentiel Artificialisation, les 5 835 lignes ont un
`id_2025` non nul et représentent 5 150 identifiants distincts. Tous
existent dans `artif_2025_46`; `artif_2025`, `cs_2025` et `us_2025`
concordent avec `artif`, `code_cs` et `code_us`.
- Aucun identifiant 2022 n’a été comparé à une couche complète 2022,
puisqu’elle n’a pas été téléchargée.

## Interprétation géométrique

Le descriptif IGN de contenu (juin 2026, §1.1.4, p. 9–10) indique que les
géométries des deux millésimes sont rapprochées sur une topologie commune,
avec une tolérance de 0,1 m, puis réunies. Le différentiel OCS GE ne conserve
que les morceaux dont le code de couverture, d’usage et/ou l’appartenance à
l’ossature diffère. L’égalité géométrique avec un objet complet 2025 n’est
donc pas attendue; comparer uniquement les géométries par identifiant
conduirait à une fausse conclusion.

Pour les deux différentiels, le contrôle communal a calculé les
intersections surfaciques avec les limites officielles déjà intégrées.
Certains morceaux intersectent plusieurs communes; aucun n’a été rattaché
à une commune unique par défaut. Les écarts entre l’aire de la géométrie et
la somme des intersections sont conservés, sans renormalisation. Aucun
recouvrement positif entre deux morceaux d’un même différentiel n’a été
détecté, mais les deux produits ne doivent pas être additionnés l’un à
l’autre : ils représentent des thèmes distincts.

## Comparabilité 2022–2025 : ce qui est établi

1. **Comparaison des codes OCS** : les paires `CS_2022`→`CS_2025` et
   `US_2022`→`US_2025` sont disponibles dans le différentiel, ainsi que
   `OSS_2022`→`OSS_2025`. Le différentiel contient des objets retenus par
   changement attributaire; les lignes et les fréquences ne sont pas des
   surfaces.
2. **Changement de statut d’artificialisation** : les champs
   `artif_2022` et `artif_2025` permettent de distinguer les deux directions
   observées. Les 4 977 lignes `non artif`→`artif` et les 858 lignes
   `artif`→`non artif` sont des nombres d’entités, pas des superficies.
3. **Surfaces** : les surfaces doivent être mesurées à partir des
   géométries différentielles (EPSG:2154) et, pour l’artificialisation,
   peuvent être confrontées au champ `surface`, qui correspond à l’aire
   géométrique arrondie à 0,01 m² pour toutes les lignes. La définition
   normative du champ `surface` n’a pas été retrouvée dans la documentation
   consultée.
4. **Identifiants** : les identifiants de chaque millésime sont des
   références aux objets sources, mais se répètent dans la couche et ne
   constituent pas une clé unique de transition. Ils ne sont pas traités
   comme stables entre 2022 et 2025.
5. **État persistant** : le différentiel d’artificialisation contrôlé ne
   contient aucune ligne où les deux états `artif` sont identiques. Il ne
   permet donc pas de mesurer les surfaces restées artificialisées.

## Limites non résolues

- Le snapshot complet OCS GE 2022 et le patch correctif 2022 ne sont pas
  présents. Les états et identifiants 2022 du différentiel n’ont pas été
  validés indépendamment contre ces couches.
- L’effet du correctif 2022 sur la comparabilité du différentiel n’a pas été
  évalué.
- Le différentiel décrit les changements selon le modèle et la méthode
  IGN, avec rapprochement topologique à 0,1 m; il ne constitue pas un
  inventaire indépendant de toutes les transformations physiques du sol.
- Les valeurs signées de `artificialisation` sont cohérentes avec les deux
  transitions d’état, mais leur définition attributaire officielle n’a pas
  été trouvée.
- Les limites communales sont celles d’ADMINEXPRESS-COG 2025. Les résidus
  de couverture observés peuvent dépendre de la géométrie des limites et
  restent sans cause déterminée.
- La table communale déjà intégrée ne contient pas de code EPCI; une
  agrégation intercommunale requiert un référentiel administratif millésimé
  et contrôlé, non téléchargé dans cette mission.
- L’occupation du sol, l’artificialisation et la consommation d’ENAF sont
  des concepts distincts. Aucun calcul de causalité ou de contribution
  touristique n’a été réalisé.

## Références techniques

- [IGN, Descriptif de contenu OCS GE NG, juin 2026](https://data.geopf.fr/annexes/ressources/documentation/DC_OCSGE_NG.pdf), §1.1.4, p. 9–10.
- [IGN, Descriptif de livraison OCS GE NG, juin 2026](https://data.geopf.fr/annexes/ressources/documentation/DL_OCSGE_NG.pdf), §2.3, p. 7–8.
- [IGN, ressource différentielle OCS GE D046](https://data.geopf.fr/telechargement/resource/OCSGE?zone=D046).
- [IGN, ressource différentielle OCS GE Artificialisation D046](https://data.geopf.fr/telechargement/resource/OCSGE-ARTIFICIALISATION?zone=D046).
