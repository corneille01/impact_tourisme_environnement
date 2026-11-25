from pathlib import Path
import os
import duckdb
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
token = os.getenv("MOTHERDUCK_TOKEN", "").strip()
database = os.getenv("MOTHERDUCK_DATABASE", "my_db").strip()
if not token:
    raise SystemExit("MOTHERDUCK_TOKEN absent du fichier .env")

source = (ROOT / "outputs" / "ocs_synthese_sources.csv").resolve()
if not source.exists():
    raise SystemExit("Fichier absent : outputs/ocs_synthese_sources.csv. Lancez les scripts 01 à 03.")

# Ce script écrit uniquement une table d'audit dans la base choisie.
con = duckdb.connect(f"md:{database}", config={"motherduck_token": token})
try:
    p = str(source).replace("\\", "/").replace("'", "''")
    con.execute(f"""
        CREATE OR REPLACE TABLE ocs_synthese_sources AS
        SELECT * FROM read_csv_auto('{p}', header=true)
    """)
    count = con.execute("SELECT COUNT(*) FROM ocs_synthese_sources").fetchone()[0]
    print(f"Table ocs_synthese_sources publiée dans {database} : {count} lignes.")
finally:
    con.close()
