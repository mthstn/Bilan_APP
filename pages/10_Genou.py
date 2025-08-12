import streamlit as st

st.header("🦵 Genou — Bilan")

with st.expander("🚩 Red flags spécifiques genou", expanded=False):
    blocage = st.checkbox("Blocage vrai")
    derob = st.checkbox("Sensation de dérobement")
    rougeur = st.checkbox("Rougeur/chaleur locale")

with st.expander("🗣️ Anamnèse spécifique"):
    nrs = st.slider("Douleur (0-10)", 0, 10, 0)
    trauma = st.selectbox("Traumatisme", ["", "Oui (contact)", "Oui (non-contact)", "Non"], index=0)
    local = st.multiselect("Localisation douleur", ["Patellaire", "Fémoro-patellaire", "Médiale", "Latérale", "Poplitée"])
    sport = st.text_input("Sport pratiqué")

with st.expander("📏 ROM genou"):
    flex = st.number_input("Flexion (°)", 0, 160, 0)
    ext = st.number_input("Extension (°)", -20, 20, 0)
    rot = st.number_input("Rotation tibiale (°)", -30, 30, 0)

with st.expander("🧪 Tests ligamentaires/méniscaux"):
    lachman = st.selectbox("Lachman", ["", "Positif", "Négatif", "Douloureux"], index=0)
    pivot = st.selectbox("Pivot shift", ["", "Positif", "Négatif", "Douloureux"], index=0)
    mcmurray = st.selectbox("McMurray", ["", "Positif", "Négatif", "Douloureux"], index=0)
    apley = st.selectbox("Apley", ["", "Positif", "Négatif", "Douloureux"], index=0)

with st.expander("💪 Testing musculaire"):
    quadri = st.selectbox("Quadriceps", ["", "3/5", "4-/5", "4/5", "4+/5", "5/5"], index=0)
    ischios = st.selectbox("Ischios", ["", "3/5", "4-/5", "4/5", "4+/5", "5/5"], index=0)
    mollets = st.selectbox("Mollets", ["", "3/5", "4-/5", "4/5", "4+/5", "5/5"], index=0)

with st.expander("🔁 Modification de symptômes"):
    rep = st.text_area("Réponse après tap tests / exercices (texte libre)")

payload = {
    "Red flags": {"Blocage": blocage, "Dérobement": derob, "Rougeur/chaleur": rougeur},
    "Anamnèse": {
        "Douleur (0-10)": nrs,
        "Traumatisme": trauma,
        "Localisation": ", ".join(local) if local else "",
        "Sport": sport,
    },
    "ROM": {"Flexion": flex, "Extension": ext, "Rotation tibiale": rot},
    "Tests": {"Lachman": lachman, "Pivot shift": pivot, "McMurray": mcmurray, "Apley": apley},
    "Testing musculaire": {"Quadriceps": quadri, "Ischios": ischios, "Mollets": mollets},
    "Modification de symptômes": rep,
}
st.session_state["genou"] = payload
st.success("Section 'Genou' ajoutée à la synthèse.")
