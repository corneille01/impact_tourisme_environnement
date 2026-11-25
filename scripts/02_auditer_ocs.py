from pathlib import Path
import zipfile
import json
import pandas as pd
import geopandas as gpd
import pyogrio

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
OUT = ROOT / "outputs"
for p in (RAW, PROC, OUT):
    p.mkdir(parents=True, exist_ok=True)

VECTOR_EXTS = {".shp", ".gpkg", ".gml", ".geojson", ".json", ".fgb"}
archive_rows, layer_rows, field_rows = [], [], []

for archive in sorted(RAW.glob("*.zip")):
    extract_dir = RAW / archive.stem
    extract_dir.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        names = zf.namelist()
        bad = zf.testzip()
        zf.extractall(extract_dir)
    archive_rows.append({
        "archive": archive.name,
        "fichiers_dans_archive": len(names),
        "test_integrite": "OK" if bad is None else f"ERREUR: {bad}",
        "formats": ", ".join(sorted({Path(n).suffix.lower() for n in names if Path(n).suffix})),
    })

    for path in extract_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in VECTOR_EXTS:
            continue
        try:
            if path.suffix.lower() == ".gpkg":
                layers = pyogrio.list_layers(path)[:, 0].tolist()
            else:
                layers = [None]
            for layer in layers:
                info = pyogrio.read_info(path, layer=layer)
                gdf = gpd.read_file(path, layer=layer) if layer else gpd.read_file(path)
                label = f"{archive.stem}::{path.name}" + (f"::{layer}" if layer else "")
                area_ha = None
                if not gdf.empty and gdf.geometry.notna().any():
                    if gdf.crs:
                        try:
                            area_ha = float(gdf.to_crs(2154).geometry.area.sum() / 10000)
                        except Exception:
                            pass
                layer_rows.append({
                    "archive": archive.name,
                    "fichier": str(path.relative_to(RAW)),
                    "couche": layer or path.stem,
                    "identifiant_audit": label,
                    "nb_entites": len(gdf),
                    "crs": str(gdf.crs),
                    "types_geometrie": ", ".join(sorted(gdf.geometry.geom_type.dropna().unique())) if not gdf.empty else "",
                    "surface_totale_ha_calculee": area_ha,
                    "emprise": json.dumps(list(gdf.total_bounds), ensure_ascii=False) if not gdf.empty else "",
                    "colonnes": " | ".join(map(str, gdf.columns)),
                    "lecture_ogr": str(info.get("driver", "")),
                })
                for col in gdf.columns:
                    if col == gdf.geometry.name:
                        continue
                    s = gdf[col]
                    field_rows.append({
                        "identifiant_audit": label,
                        "champ": col,
                        "type_python": str(s.dtype),
                        "nb_valeurs_non_nulles": int(s.notna().sum()),
                        "nb_valeurs_distinctes": int(s.nunique(dropna=True)),
                        "exemples": " | ".join(map(str, s.dropna().astype(str).unique()[:5])),
                    })
                print(f"[OK] {label}: {len(gdf):,} entités, CRS={gdf.crs}")
        except Exception as exc:
            layer_rows.append({
                "archive": archive.name,
                "fichier": str(path.relative_to(RAW)),
                "couche": "",
                "identifiant_audit": "",
                "nb_entites": None,
                "crs": "",
                "types_geometrie": "",
                "surface_totale_ha_calculee": None,
                "emprise": "",
                "colonnes": "",
                "lecture_ogr": f"ERREUR: {type(exc).__name__}: {exc}",
            })
            print(f"[ERREUR] {path}: {exc}")

pd.DataFrame(archive_rows).to_csv(OUT / "ocs_archives.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(layer_rows).to_csv(OUT / "ocs_couches_audit.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(field_rows).to_csv(OUT / "ocs_champs_audit.csv", index=False, encoding="utf-8-sig")
print("\nAudit terminé : outputs/ocs_archives.csv, ocs_couches_audit.csv, ocs_champs_audit.csv")
print("IMPORTANT : les surfaces sont des sommes géométriques par couche. Elles ne doivent pas être additionnées entre couches sans vérifier leur organisation et les chevauchements.")
