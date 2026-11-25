# Rapport de contrôle géométrique — OCS GE 2025, D046

Date de traitement : 2026-11-25T06:38:32+01:00

Contrôle effectué en flux avec Pyogrio/Arrow et Shapely sur les GeoPackages
d'origine, sans écriture sur les sources. Le type générique `GEOMETRY` déclaré
par les GeoPackages n'est pas considéré comme une anomalie : les types réels
ont été inspectés entité par entité.

| Couche | Entités | CRS déclaré et utilisé | Type déclaré | Type réel | Nulles | Vides | Invalides | Types inattendus | MultiPolygon | Composants > 1 |
|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|
| `OCCUPATION_SOL` | 299,787 | EPSG:2154 | GEOMETRY/Unknown | MultiPolygon: 299,787 | 0 | 0 | 0 | 0 | 299,787 | 0 |
| `ZONE_CONSTRUITE` | 26,599 | EPSG:2154 | GEOMETRY/Unknown | MultiPolygon: 26,599 | 0 | 0 | 0 | 0 | 26,599 | 0 |
| `artif_2025_46` | 299,787 | EPSG:2154 | GEOMETRY/Unknown | MultiPolygon: 299,787 | 0 | 0 | 0 | 0 | 299,787 | 0 |

Toutes les géométries observées sont des MultiPolygon valides; les nombres de
parties multiples indiquent les MultiPolygon possédant plus d'un polygone
composant. Les couches dérivées ont ensuite été relues en entier et leurs
géométries comparées exactement aux géométries source.

**Conclusion :** contrôle géométrique réussi pour les trois couches. Le type
déclaré `Unknown` décrit ici l'enregistrement générique et ne contredit pas
les types réels homogènes.
