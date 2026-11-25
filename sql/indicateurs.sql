-- Requêtes de contrôle à exécuter après publication de la table d'audit.
SELECT annee_source, COUNT(*) AS nombre_couches,
       SUM(nb_entites) AS nombre_entites
FROM ocs_synthese_sources
GROUP BY annee_source
ORDER BY annee_source;

-- Contrôle des couches dont la lecture a échoué.
SELECT *
FROM ocs_synthese_sources
WHERE lecture_ogr LIKE 'ERREUR:%';
