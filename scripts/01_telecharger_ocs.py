from pathlib import Path
import hashlib
import json
import requests
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "ocs_ge_lot_2019.zip": {
        "url": "https://ckan.openig.org/dataset/0bb7c7b4-9444-4984-a964-9ba3032675db/resource/3dca46ce-130a-4e3c-88c6-c06f6c34177c/download/occupation-sol-d46-2019.zip",
        "dataset": "Occupation du sol 2019 Lot",
        "portal": "https://www.data.gouv.fr/datasets/occupation-du-sol-2019-lot",
    },
    "ocs_ge_lot_2022.zip": {
        "url": "https://ckan.openig.org/dataset/91eecbd3-4376-4cf1-9844-363135dbb3a6/resource/ad83a2e8-7d1d-4ff4-a5e7-8376b7a2f6e5/download/occupation-sol-d462022.zip",
        "dataset": "Occupation du sol 2022 Lot",
        "portal": "https://www.data.gouv.fr/datasets/occupation-du-sol-2022-lot",
    },
    "ocs_ge_lot_differenciel_2019_2022.zip": {
        "url": "https://ckan.openig.org/dataset/431eb972-6923-4cf9-9a08-cb274a4492c0/resource/808adafe-acdd-452d-acca-e60fde822a51/download/differenciel-d46-2019-2022.zip",
        "dataset": "Occupation du sol différentiel 2022-2019 Lot",
        "portal": "https://www.data.gouv.fr/datasets/occupation-du-sol-differenciel-2022-2019-lot",
    },
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

manifest = []
for filename, meta in SOURCES.items():
    dest = RAW / filename
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[EXISTE] {filename} ({dest.stat().st_size:,} octets)")
    else:
        print(f"[TELECHARGEMENT] {meta['dataset']}")
        with requests.get(meta["url"], stream=True, timeout=(30, 300)) as response:
            response.raise_for_status()
            total = 0
            with dest.open("wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        total += len(chunk)
        print(f"[OK] {filename}: {total:,} octets")
    manifest.append({
        "fichier": filename,
        "jeu_de_donnees": meta["dataset"],
        "portail": meta["portal"],
        "url_telechargement": meta["url"],
        "taille_octets": dest.stat().st_size,
        "sha256": sha256(dest),
        "date_verification_utc": datetime.now(timezone.utc).isoformat(),
    })

(ROOT / "data" / "raw" / "manifest_sources.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("\nTéléchargements terminés. Lancez ensuite :")
print("python scripts/02_auditer_ocs.py")
