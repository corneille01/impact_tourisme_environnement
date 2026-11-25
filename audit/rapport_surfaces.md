# Rapport de contrôle des surfaces — artificialisation OCS GE 2025, D046

Date de traitement : 2026-11-25T06:38:32+01:00

## Interprétation documentée

Le champ source `aire` est documenté par l'IGN comme la surface de l'objet
mesurée dans la projection utilisée; *Doc_artif.pdf* (février 2025), p. 8,
est la référence consignée dans le dictionnaire de variables. Les géométries
sont déclarées et utilisées en **EPSG:2154 (Lambert-93)**, dont les
coordonnées sont métriques : l'unité surfacique attendue est le **mètre carré
(m²)**. Cette référence est également consignée dans
`data/raw/ocsge/audit/ocsge_variable_dictionary.csv`.

## Comparaison intégrale

Comparaison Shapely de `aire` avec `geometry.area` sur les 299 787 géométries,
en lecture par lots.

| Contrôle | Résultat |
|---|---:|
| Entités comparées | 299,787 |
| `aire` SQL NULL | 0 |
| Valeurs `aire` <= 0 | 0 |
| Minimum `aire` | 0.06 m² |
| Maximum `aire` | 21,566,074.32 m² |
| Somme du champ `aire` | 5,221,866,769.98 m² |
| Égalité à `round(geometry.area, 2)` | 299,787/299,787 |
| Écart absolu maximum avant arrondi | 0.005000000 m² |
| Écart absolu moyen | 0.002498751 m² |
| Médiane de l'écart absolu | 0.002500000 m² |
| 95e percentile de l'écart absolu | 0.004750003 m² |

Les valeurs concordent intégralement avec l'aire géométrique arrondie à deux
décimales. Cela confirme empiriquement la cohérence du champ et un arrondi au
centième de m²; cela ne prouve pas l'implémentation interne exacte utilisée par
l'IGN. Aucun seuil d'« aberrance » métier n'a été inventé : minima et maxima
sont consignés, sans zéro, négatif, NULL ni écart non expliqué par l'arrondi.

Le champ source `aire` est conservé sans modification. Les GeoPackages dérivés
ajoutent `aire_geometrie_m2`, calculé avec `shapely.area` en EPSG:2154, sans
arrondi et sans remplacer le champ IGN.
