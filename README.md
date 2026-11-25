# Projet complet — Observatoire territorial du tourisme dans le Lot

Ce dossier est autonome : ouvrez directement le dossier `lot_tourisme_analyse` dans VS Code. Aucun assemblage avec un ancien dossier n'est nécessaire.

## Contenu
- `app/` : tableau de bord Streamlit
- `scripts/` : téléchargement, audit, préparation et publication MotherDuck
- `sql/` : requêtes SQL de contrôle
- `data/raw/` : archives OCS GE téléchargées et manifeste des sources
- `data/processed/` : espace de préparation des données
- `outputs/` : rapports d'audit CSV
- `.vscode/` : paramètres et extensions recommandées
- `.env.example` : modèle de configuration MotherDuck
- `requirements.txt` : dépendances Python

## Démarrage (environnement Python déjà réparé)
Dans le terminal PowerShell de VS Code :

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python scripts/01_telecharger_ocs.py
python scripts/02_auditer_ocs.py
python scripts/03_preparer_indicateurs.py
streamlit run app/dashboard.py
```

Si `.env` existe déjà, ne l'écrasez pas : conservez votre token MotherDuck.

## MotherDuck
Renseignez `MOTHERDUCK_TOKEN` dans `.env`, puis lancez :

```powershell
python scripts/04_publier_motherduck.py
```

La publication concerne uniquement la table `ocs_synthese_sources` dans `my_db` (ou la base configurée). Les géométries brutes restent en local à cette étape.

## Sources OCS GE du Lot
- 2019 : https://www.data.gouv.fr/datasets/occupation-du-sol-2019-lot
- 2022 : https://www.data.gouv.fr/datasets/occupation-du-sol-2022-lot
- Différentiel 2019–2022 : https://www.data.gouv.fr/datasets/occupation-du-sol-differenciel-2022-2019-lot

Les archives sont téléchargées automatiquement par le script 01. Elles ne sont pas préembarquées dans le ZIP afin d'éviter une archive volumineuse et de conserver la traçabilité des téléchargements. Le manifeste enregistre les URL et empreintes SHA-256.

## Précautions méthodologiques
L'OCS GE mesure l'occupation et l'usage du sol, pas directement la pression touristique. Avant tout calcul par classe, il faut examiner `outputs/ocs_champs_audit.csv`, vérifier les nomenclatures, les géométries, les systèmes de coordonnées et les règles du différentiel. Les sommes de surfaces de couches différentes ne doivent pas être additionnées sans contrôle des chevauchements.

Les données touristiques, de logement, d'emploi et de fréquentation ne sont pas fabriquées ni remplacées par des valeurs fictives. Elles seront intégrées lorsqu'elles seront disponibles et documentées.
