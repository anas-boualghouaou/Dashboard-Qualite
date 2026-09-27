import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ==========================================
# CONFIGURATION DE LA PAGE STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Système de Contrôle Qualité",
    page_icon="https://cdn-icons-png.flaticon.com/512/921/921591.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS SUR MESURE & ANIMATIONS (HTML/CSS)
# ==========================================
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1e293b;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

.stApp {
    background-color: #f8fafc;
    animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
    animation: fadeIn 0.5s ease-out;
}

.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.08);
    border-color: #cbd5e1;
}

.kpi-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.kpi-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
}

.kpi-value {
    font-size: 1.85rem;
    font-weight: 700;
    color: #0f172a;
}

.kpi-icon {
    width: 38px;
    height: 38px;
}

.app-header {
    display: flex;
    align-items: center;
    gap: 16px;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 24px 32px;
    border-radius: 16px;
    color: white;
    margin-bottom: 25px;
}

.app-header img {
    width: 50px;
    height: 50px;
}

.login-box {
    max-width: 420px;
    margin: 60px auto;
    background: #ffffff;
    padding: 35px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
    text-align: center;
    animation: fadeIn 0.5s ease-in-out;
}

.login-logo {
    width: 64px;
    margin-bottom: 15px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

DATA_FILE = "dataset.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return pd.DataFrame()

def save_data(df):
    df_to_save = df.copy()
    if 'Date' in df_to_save.columns:
        df_to_save['Date'] = df_to_save['Date'].dt.strftime('%Y-%m-%d')
    df_to_save.to_csv(DATA_FILE, index=False)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-box">
            <img src="https://cdn-icons-png.flaticon.com/512/921/921591.png" class="login-logo"/>
            <h2 style="margin-bottom: 5px; color: #0f172a; font-weight: 700;">QualiControl Pro</h2>
            <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 25px;">Plateforme d'inspection et de suivi qualité</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur", placeholder="admin")
            password = st.text_input("Mot de passe", type="password", placeholder="admin")
            submit = st.form_submit_button("Se connecter", use_container_width=True)
            
            if submit:
                if username == "admin" and password == "admin":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")

else:
    df = load_data()
    
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <img src="https://cdn-icons-png.flaticon.com/512/921/921591.png" width="45"/>
            <h3 style="margin: 10px 0 0 0; color: #0f172a; font-size: 1.2rem;">QualiControl</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        menu = st.radio("Navigation", ["Tableau de Bord", "Saisie & Gestion", "Rapports & Exporter"])
        
        st.divider()
        lignes = ["Toutes"] + list(df["Ligne_Production"].unique()) if not df.empty else ["Toutes"]
        selected_ligne = st.selectbox("Ligne de Production", lignes)
        
        statuts = ["Tous"] + list(df["Statut"].unique()) if not df.empty else ["Tous"]
        selected_statut = st.selectbox("Statut Contrôle", statuts)
        
        st.divider()
        if st.button("Déconnexion", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    df_filtered = df.copy()
    if selected_ligne != "Toutes":
        df_filtered = df_filtered[df_filtered["Ligne_Production"] == selected_ligne]
    if selected_statut != "Tous":
        df_filtered = df_filtered[df_filtered["Statut"] == selected_statut]

    st.markdown("""
    <div class="app-header">
        <img src="https://cdn-icons-png.flaticon.com/512/1541/1541402.png" />
        <div>
            <h1 style="color:white; margin:0;">Dashboard de Contrôle Qualité</h1>
            <p style="color:#94a3b8; margin:4px 0 0 0;">Supervision de la conformité de production</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if menu == "Tableau de Bord":
        total_inspecte = df_filtered["Quantite_Inspectee"].sum() if not df_filtered.empty else 0
        total_defauts = df_filtered["Defauts_Trouves"].sum() if not df_filtered.empty else 0
        taux_defaut = (total_defauts / total_inspecte * 100) if total_inspecte > 0 else 0
        conformes = len(df_filtered[df_filtered["Statut"] == "Conforme"]) if not df_filtered.empty else 0
        taux_conformite = (conformes / len(df_filtered) * 100) if not df_filtered.empty else 0

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(f'<div class="kpi-card"><div class="kpi-header"><span class="kpi-title">Total Inspecté</span><img src="https://cdn-icons-png.flaticon.com/512/3121/3121768.png" class="kpi-icon"/></div><div class="kpi-value">{total_inspecte:,}</div></div>', unsafe_allow_html=True)
        with kpi2:
            st.markdown(f'<div class="kpi-card"><div class="kpi-header"><span class="kpi-title">Pièces Défectueuses</span><img src="https://cdn-icons-png.flaticon.com/512/595/595067.png" class="kpi-icon"/></div><div class="kpi-value" style="color: #e11d48;">{total_defauts}</div></div>', unsafe_allow_html=True)
        with kpi3:
            st.markdown(f'<div class="kpi-card"><div class="kpi-header"><span class="kpi-title">Taux de Défaut</span><img src="https://cdn-icons-png.flaticon.com/512/4301/4301566.png" class="kpi-icon"/></div><div class="kpi-value">{taux_defaut:.2f}%</div></div>', unsafe_allow_html=True)
        with kpi4:
            st.markdown(f'<div class="kpi-card"><div class="kpi-header"><span class="kpi-title">Conformité Global</span><img src="https://cdn-icons-png.flaticon.com/512/190/190411.png" class="kpi-icon"/></div><div class="kpi-value" style="color: #16a34a;">{taux_conformite:.1f}%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        sns.set_theme(style="whitegrid")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("##### Distribution des Statuts")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            sns.barplot(x=df_filtered['Statut'].value_counts().index, y=df_filtered['Statut'].value_counts().values, ax=ax1, palette="viridis", hue=df_filtered['Statut'].value_counts().index, legend=False)
            st.pyplot(fig1)

        with col_g2:
            st.markdown("##### Défauts par Ligne")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            defauts_ligne = df_filtered.groupby("Ligne_Production")["Defauts_Trouves"].sum().reset_index()
            sns.barplot(data=defauts_ligne, x="Ligne_Production", y="Defauts_Trouves", ax=ax2, color="#3b82f6")
            st.pyplot(fig2)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_filtered, use_container_width=True)

    elif menu == "Saisie & Gestion":
        st.markdown("### Gestion des Données")
        tab_add, tab_del = st.tabs(["Ajouter", "Supprimer"])
        
        with tab_add:
            with st.form("add_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    date_val = st.date_input("Date", datetime.now())
                    ligne_val = st.selectbox("Ligne", ["Ligne A", "Ligne B", "Ligne C", "Ligne D"])
                    produit_val = st.text_input("Produit", "Moteur V6")
                    quantite_val = st.number_input("Quantité", min_value=1, value=100)
                with c2:
                    defauts_val = st.number_input("Défauts", min_value=0, value=0)
                    statut_val = st.selectbox("Statut", ["Conforme", "Alerte", "Non Conforme"])
                    inspecteur_val = st.text_input("Inspecteur", "Karim Bennani")

                if st.form_submit_button("Enregistrer", use_container_width=True):
                    new_id = df["ID"].max() + 1 if not df.empty else 1
                    new_row = {
                        "ID": new_id, "Date": pd.to_datetime(date_val), "Ligne_Production": ligne_val,
                        "Produit": produit_val, "Quantite_Inspectee": quantite_val,
                        "Defauts_Trouves": defauts_val, "Statut": statut_val, "Inspecteur": inspecteur_val
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    save_data(df)
                    st.success("Enregistré avec succès !")
                    st.rerun()

        with tab_del:
            if not df.empty:
                del_id = st.selectbox("Sélectionner l'ID", df["ID"].tolist())
                if st.button("Confirmer la suppression", type="primary", use_container_width=True):
                    df = df[df["ID"] != del_id]
                    save_data(df)
                    st.success("Supprimé !")
                    st.rerun()

    elif menu == "Rapports & Exporter":
        st.markdown("### Exporter les données")
        st.dataframe(df_filtered, use_container_width=True)
        st.download_button(
            label="Télécharger CSV",
            data=df_filtered.to_csv(index=False).encode('utf-8'),
            file_name="rapport_qualite.csv",
            mime="text/csv",
            use_container_width=True
        )
