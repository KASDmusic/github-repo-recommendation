import streamlit as st
import requests
import time

def fetch_recommended_repos(username):
    """Simule ou récupère des recommandations de repositories pour un utilisateur donné."""
    # Remplacez ceci par votre logique de recommandation réelle.
    # Par exemple, appeler une API ou un modèle de recommandation.
    recommended_repos = [
        {"name": "awesome-python", "description": "A curated list of awesome Python frameworks and libraries.", "url": "https://github.com/vinta/awesome-python"},
        {"name": "react", "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.", "url": "https://github.com/facebook/react"},
        {"name": "tensorflow", "description": "An open source machine learning framework for everyone.", "url": "https://github.com/tensorflow/tensorflow"},
    ]
    return recommended_repos

# Ajouter une image ou un logo en haut de la page
st.image("static/github-header-image.png", use_column_width=True)

# Titre principal de l'application avec un style amélioré
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>github-repo-recommendation</h1>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Description stylisée
st.markdown("""
<div style='text-align: left;'>
<i> <b> Entrez le nom d'un utilisateur GitHub </b> pour obtenir des recommandations de repositories basées sur les repositories favories et les contributions. </i>
</div>
<br>
""", unsafe_allow_html=True)

# Ajouter une barre latérale pour des informations supplémentaires
with st.sidebar:
    st.header("À propos")
    st.write("Cette application utilise des techniques de recommandation basées sur le contenu pour suggérer des repositories GitHub pertinents.")
    st.write("**Auteurs :** François Garnier, Allane Bourdon and Kenzo Lecoindre")
    st.write("**Version :** 1.0")

# Champ pour saisir le nom d'utilisateur
#st.markdown("<h3 style='text-align: center;'>Nom d'utilisateur GitHub</h3>", unsafe_allow_html=True)
username = st.text_input("Nom d'utilisateur GitHub", placeholder="Exemple : octocat", label_visibility="collapsed")

# Bouton de soumission
if st.button("🔍 Obtenir des recommandations"):
    if username:
        with st.spinner("*Recherche des recommandations...*"):
            try:
                # Appeler la fonction pour obtenir les recommandations
                repos = fetch_recommended_repos(username)

                if repos:
                    st.success(f"Voici des recommandations pour l'utilisateur **{username}**:")

                    for repo in repos:
                        st.markdown(f"<h4><a href='{repo['url']}' target='_blank' style='text-decoration: none; color: #1E90FF;'>{repo['name']}</a></h4>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #555;'>{repo['description']}</p>", unsafe_allow_html=True)
                        st.markdown("---")
                else:
                    st.warning("Aucune recommandation trouvée pour cet utilisateur.")
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
    else:
        st.warning("Veuillez entrer un nom d'utilisateur GitHub.")

# Ajouter un footer
st.markdown("""
<hr>
<div style='text-align: center;'>
Développé avec ❤️ en utilisant Streamlit.
</div>
""", unsafe_allow_html=True)
