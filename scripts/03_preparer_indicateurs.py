from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DATA = ROOT / "data"
OUT.mkdir(exist_ok=True)

audit = OUT / "ocs_couches_audit.csv"
if not audit.exists():
    raise SystemExit("Audit absent. Lancez d'abord : python scripts/02_auditer_ocs.py")

layers = pd.read_csv(audit)
layers["annee_source"] = layers["archive"].astype(str).str.extract(r"(2019|2022)", expand=False)
layers["annee_source"] = layers["annee_source"].fillna("différentiel_2019_2022")
layers.to_csv(OUT / "ocs_synthese_sources.csv", index=False, encoding="utf-8-sig")

# Contrôle de présence des fichiers touristiques fournis dans la première version du projet.
expected = [
    DATA / "hebergements_insee_2024.csv",
    DATA / "nuitees_flux_vision.csv",
    DATA / "sites_visites_2024.csv",
]
checks = []
for path in expected:
    checks.append({
        "fichier": str(path.relative_to(ROOT)),
        "present": path.exists(),
        "taille_octets": path.stat().st_size if path.exists() else None,
        "statut": "à contrôler" if path.exists() else "absent : ne pas inventer les données",
    })
pd.DataFrame(checks).to_csv(OUT / "controle_sources_tourisme.csv", index=False, encoding="utf-8-sig")
print("Synthèses créées dans outputs/.")
print("Étape suivante : examiner ocs_champs_audit.csv pour définir les champs de nomenclature avant de calculer les changements par classe.")
