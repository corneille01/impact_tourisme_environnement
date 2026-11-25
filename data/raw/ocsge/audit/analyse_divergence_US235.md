# Divergence de libelle US235 - OCS GE D046 2025

## Sources comparees

- La nomenclature livree avec le paquet OCS GE D046 (supplement `2026-10-00131`) porte la ligne `US235; Production secondaire, tertiaire et usage residentiel`. La source est le fichier [NomenclatureOCSGE.csv](../extracted/ocsge_2025_D046/OCS-GE_2-0__GPKG_LAMB93_D046_2025-01-01/OCS-GE/3_SUPPLEMENTS_LIVRAISON_2026-10-00131/NomenclatureOCSGE.csv).
- Le descriptif IGN OCS GE NG de juin 2026, p. 6, nomme `US235` « Usage mixte » et precise que c est le regroupement des usages `US2`, `US3` et `US5` de la nomenclature nationale. La note de bas de page dit qu une partie des usages qui ne sont pas separes reste dans cette classe mixte en nouvelle generation.
- Le meme descriptif, p. 21, definit `US235 Usage mixte` comme regroupant `US2 Production secondaire`, `US3 Production tertiaire` et `US5 Usage residentiel`.
- Dans `OCCUPATION_SOL.gpkg`, le code `US235` est present 47 fois. La valeur de code n a pas ete modifiee.

## Arbitrage

Les deux libelles sont **semantiquement compatibles** : le libelle long de la nomenclature enumererait les trois usages que le descriptif IGN rassemble sous le terme « Usage mixte ». Le document IGN ne decrit donc pas US235 comme une classe au contenu different; il confirme aussi que le code peut subsister pour des usages non separes en nouvelle generation.

Les pieces disponibles ne permettent pas de conclure a une evolution de la definition de la classe. Elles montrent une difference de formulation entre la nomenclature de livraison d octobre 2026 et le descriptif de juin 2026. Le CSV ne donne pas de numero/version de nomenclature ni de note de changement; il est donc impossible d etablir si le libelle long est un libelle developpe, une version distincte ou une incoherence editoriale.

**Conclusion de contre-expertise :** pas de preuve d evolution semantique; difference de libelle documentee, avec forte confiance sur l equivalence de sens et incertitude sur l origine/version exacte de la formulation. Pour le projet, conserver les deux libelles avec leur provenance plutot que d en substituer un silencieusement. Pour une restitution strictement liee au paquet D046, citer le libelle du CSV de livraison; pour expliquer le domaine, citer la definition du PDF IGN de juin 2026.

Source officielle : [DC_OCSGE_NG.pdf, pages 6 et 21](https://data.geopf.fr/annexes/ressources/documentation/DC_OCSGE_NG.pdf).
