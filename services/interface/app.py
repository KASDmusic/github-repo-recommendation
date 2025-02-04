import streamlit as st
import requests
import time

def fetch_recommended_repos(username):
    """Simule ou récupère des recommandations de repositories pour un utilisateur donné."""
    recommended_repos = [
        {"name": "awesome-python", "description": "A curated list of awesome Python frameworks and libraries.", "url": "https://github.com/vinta/awesome-python"},
        {"name": "react", "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.", "url": "https://github.com/facebook/react"},
        {"name": "tensorflow", "description": "An open source machine learning framework for everyone.", "url": "https://github.com/tensorflow/tensorflow"},
    ]
    return recommended_repos

def change_feedback(repo_name, rating):
    # récupérer la valeur de l'évaluation grâce à key
    print(f"Feedback changed to {rating} stars.")   

def render_feedback(repo_name):
    """Affiche un système de feedback par étoiles interactif."""
    st.write(f"Évaluez le repository '{repo_name}':")
    if not 'rating' in locals():
        rating = None
    rating = st.feedback(options="stars", key=f"feedback_{repo_name}", on_change=change_feedback, args=(repo_name, rating))
    if rating is not None:
        st.write(f"Vous avez donné une note de {rating + 1} étoile(s) pour '{repo_name}'.")
    return rating

st.set_page_config(page_title="GitHub Repo Recommendation", page_icon="./static/github_repo_recommendation.png")

st.image("static/github-header-image.png", use_container_width=True)

st.markdown("""
<div style='text-align: left;'>
<i> <b> Entrez le nom d'un utilisateur GitHub </b> pour obtenir des recommandations de repositories basées sur les repositories favoris et les contributions. </i>
</div>
</br>
""", unsafe_allow_html=True)


#with st.sidebar:
#    st.header("À propos")
#    st.write("Cette application utilise des techniques de recommandation basées sur le contenu pour suggérer des repositories GitHub pertinents.")
#    st.write("**Auteurs :** François Garnier, Allane Bourdon et Kenzo Lecoindre")
#    st.write("**Version :** 1.0")


number = st.number_input("Nombre de recommandations", min_value=1, value=5, max_value=20, step=1)

username = st.text_input("Nom d'utilisateur GitHub", placeholder="Exemple : octocat")

if 'repos' not in st.session_state:
    st.session_state['repos'] = []

if st.button("🔍 Obtenir des recommandations"):
    if username:
        with st.spinner("*Recherche des recommandations...*"):
            try:
                st.session_state['repos'] = fetch_recommended_repos(username)
                if st.session_state['repos']:
                    st.success(f"Voici des recommandations pour l'utilisateur **{username}**:")
                else:
                    st.warning("Aucune recommandation trouvée pour cet utilisateur.")
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
    else:
        st.warning("Veuillez entrer un nom d'utilisateur GitHub.")

if st.session_state['repos']:
    for repo in st.session_state['repos']:
        st.markdown(f"<h4><a href='{repo['url']}' target='_blank' style='text-decoration: none; color: #1E90FF;'>{repo['name']}</a></h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #555;'>{repo['description']}</p>", unsafe_allow_html=True)
        render_feedback(repo['name'])
        st.markdown("---")

st.markdown("""
<hr>
<div style='text-align: center;'>
Développé avec ❤️ en utilisant Streamlit.
</div>
""", unsafe_allow_html=True)
