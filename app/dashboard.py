from pathlib import Path

import pandas as pd
import streamlit as st

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

AUDIT_FILE = OUTPUT_DIR / "ocs_couches_audit.csv"
ARCHIVES_FILE = OUTPUT_DIR / "ocs_archives.csv"
FIELDS_FILE = OUTPUT_DIR / "ocs_champs_audit.csv"
SYNTHESIS_FILE = OUTPUT_DIR / "ocs_synthese_sources.csv"

st.set_page_config(
    page_title="Observatoire touristique du Lot",
    page_icon="🗺️",
    layout="wide",
)

# ============================================================
# FONCTION DE LECTURE SÉCURISÉE
# ============================================================


def lire_csv(chemin):
    """Lit un CSV en gérant les fichiers absents ou vides."""

    if not chemin.exists():
        return pd.DataFrame(), "absent"

    if chemin.stat().st_size == 0:
        return pd.DataFrame(), "vide"

    try:
        df = pd.read_csv(chemin, sep=None, engine="python")

        if df.empty and len(df.columns) == 0:
            return pd.DataFrame(), "vide"

        return df, "ok"

    except pd.errors.EmptyDataError:
        return pd.DataFrame(), "vide"

    except Exception as erreur:
        return pd.DataFrame(), str(erreur)


# ============================================================
# CHARGEMENT
# ============================================================

df_audit, statut_audit = lire_csv(AUDIT_FILE)
df_archives, statut_archives = lire_csv(ARCHIVES_FILE)
df_champs, statut_champs = lire_csv(FIELDS_FILE)
df_synthese, statut_synthese = lire_csv(SYNTHESIS_FILE)


# ============================================================
# EN-TÊTE
# ============================================================

st.title("🗺️ Observatoire territorial du tourisme – Lot")

st.markdown("""
    **Analyse territoriale, occupation du sol et observation touristique**

    Cette interface permet de contrôler les données sources,
    les archives géographiques et la qualité des données
    utilisées pour construire les indicateurs territoriaux.
    """)

st.divider()


# ============================================================
# ÉTAT DU PROJET
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Couches géographiques", len(df_audit) if statut_audit == "ok" else 0)

col2.metric("Archives analysées", len(df_archives) if statut_archives == "ok" else 0)

col3.metric("Champs audités", len(df_champs) if statut_champs == "ok" else 0)

col4.metric("Sources répertoriées", len(df_synthese) if statut_synthese == "ok" else 0)


# ============================================================
# ALERTES
# ============================================================

st.subheader("État des données")

fichiers = {
    "Audit des couches": (AUDIT_FILE, statut_audit),
    "Audit des archives": (ARCHIVES_FILE, statut_archives),
    "Audit des champs": (FIELDS_FILE, statut_champs),
    "Synthèse des sources": (SYNTHESIS_FILE, statut_synthese),
}

for nom, (chemin, statut) in fichiers.items():

    if statut == "ok":
        st.success(f"✅ {nom} : fichier disponible")

    elif statut == "absent":
        st.warning(f"⚠️ {nom} : fichier non généré ({chemin.name})")

    elif statut == "vide":
        st.warning(f"⚠️ {nom} : fichier vide ({chemin.name})")

    else:
        st.error(f"❌ {nom} : erreur de lecture — {statut}")


# ============================================================
# ONGLET
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🗂️ Couches géographiques",
        "📦 Archives",
        "🔍 Champs",
        "📊 Synthèse",
    ]
)


# ============================================================
# TAB 1 : AUDIT DES COUCHES
# ============================================================

with tab1:

    st.subheader("Audit des couches géographiques")

    if statut_audit == "ok":

        st.dataframe(df_audit, use_container_width=True, hide_index=True)

        st.download_button(
            "Télécharger l'audit CSV",
            data=df_audit.to_csv(index=False).encode("utf-8"),
            file_name="ocs_couches_audit.csv",
            mime="text/csv",
        )

    else:

        st.info("""
            Aucun audit des couches n'est disponible pour le moment.

            **Étape à effectuer dans le terminal VS Code :**

            ```powershell
            python scripts/01_telecharger_ocs.py
            python scripts/02_auditer_ocs.py
            ```

            Une fois les fichiers générés, actualisez cette page.
            """)


# ============================================================
# TAB 2 : ARCHIVES
# ============================================================

with tab2:

    st.subheader("Archives OCS GE")

    if statut_archives == "ok":

        st.dataframe(df_archives, use_container_width=True, hide_index=True)

    else:

        st.info("L'audit des archives n'est pas encore disponible.")


# ============================================================
# TAB 3 : CHAMPS
# ============================================================

with tab3:

    st.subheader("Structure des données")

    if statut_champs == "ok":

        st.dataframe(df_champs, use_container_width=True, hide_index=True)

        if len(df_champs.columns) > 0:

            colonnes = df_champs.columns.tolist()

            recherche = st.text_input(
                "Rechercher un champ, une couche ou une information"
            )

            if recherche:

                df_filtre = (
                    df_champs.astype(str)
                    .apply(
                        lambda colonne: colonne.str.contains(
                            recherche, case=False, na=False
                        )
                    )
                    .any(axis=1)
                )

                st.dataframe(
                    df_champs[df_filtre], use_container_width=True, hide_index=True
                )

    else:

        st.info(
            "Les champs des couches géographiques " "seront disponibles après l'audit."
        )


# ============================================================
# TAB 4 : SYNTHÈSE
# ============================================================

with tab4:

    st.subheader("Synthèse des sources")

    if statut_synthese == "ok":

        st.dataframe(df_synthese, use_container_width=True, hide_index=True)

    else:

        st.info("La synthèse sera générée après l'analyse " "des données sources.")


# ============================================================
# PIED DE PAGE
# ============================================================

st.divider()

st.caption(
    "Projet d'analyse territoriale du tourisme — "
    "Lot | Master 2 TIC appliquées au développement "
    "des territoires touristiques"
)
