import streamlit as st
import pandas as pd
import json
from datetime import datetime
from utils.pdf_utils import generate_pdf_bytes

st.set_page_config(page_title="APP Bilan Kiné", page_icon="🩺", layout="wide")

# (Optionnel) mot de passe via Secrets (à configurer plus tard sur Streamlit Cloud)
_pwd = st.secrets.get("APP_PASSWORD", None)
if _pwd:
    typed = st.text_input("Mot de passe", type="password")
    if typed != _pwd:
        st.stop()

st.title("🩺 APP Bilan - Kiné")

with st.expander("ℹ️ Aide rapide", expanded=False):
    st.markdown(
        "1) Renseigne les infos patient ci-dessous.  \n"
        "2) Va dans la page **Genou** à gauche.  \n"
        "3) Reviens ici et clique **Générer PDF** ou **Exporter JSON/CSV**.  \n\n"
        "**Note** : Les champs vides ne s’affichent pas dans le PDF."
    )

st.subheader("👤 Informations patient")
c = st.columns(4)
with c[0]: nom = st.text_input("Nom", key="nom")
with c[1]: prenom = st.text_input("Prénom", key="prenom")
with c[2]: naissance = st.date_input("Date de naissance", key="naissance")
with c[3]: sexe = st.selectbox("Sexe", ["", "Femme", "Homme", "Autre"], index=0, key="sexe")

motif = st.text_area("Motif de consultation (texte libre)", key="motif", height=80)

st.divider()
st.subheader("🧩 Synthèse & Export")

def collect_all_data():
    return {
        "Patient": {
            "Nom": nom,
            "Prénom": prenom,
            "Naissance": str(naissance) if naissance else "",
            "Sexe": sexe,
        },
        "Motif": motif,
        "Genou": st.session_state.get("genou", {}),
    }

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Générer PDF"):
        data = collect_all_data()
        pdf_bytes = generate_pdf_bytes(data, title="Bilan Kiné — Synthèse")
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            "Télécharger le PDF",
            data=pdf_bytes,
            file_name=f"bilan_kine_{now}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

with col2:
    if st.button("💾 Export JSON"):
        data = collect_all_data()
        st.download_button(
            "Télécharger JSON",
            data=json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name="bilan_kine.json",
            mime="application/json",
            use_container_width=True
        )

with col3:
    if st.button("📊 Export CSV (à plat)"):
        data = collect_all_data()
        flat_rows = []
        def flatten(prefix, obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    flatten(f"{prefix}{k}>", v)
            else:
                flat_rows.append([prefix[:-1], obj])
        for k, v in data.items():
            flatten(f"{k}>", v)
        df = pd.DataFrame(flat_rows, columns=["Champ", "Valeur"])
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "Télécharger CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="bilan_kine.csv",
            mime="text/csv",
            use_container_width=True
        )

st.caption("Si le téléchargement ne démarre pas, autorise les téléchargements/pop‑ups dans ton navigateur.")
