import streamlit as st
import requests
import time

def fetch_recommended_repos(username, n):
    # Appel de l'API FastAPI
    response = requests.get(f"http://api_nlp:8000/user_recommandation/?user={username}&n={n}")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def change_feedback(user_id: int, repo_link: str, rating: int):
    # récupérer la valeur de l'évaluation grâce à key
    print(f"Feedback changed to {rating} stars.")

    if user_id is None:
        json_data = {
            "repo_link": repo_link,
            "rating": rating
        }
    else:
        json_data = {
            "user_id": user_id,
            "repo_link": repo_link,
            "rating": rating
        }

    # Appel de l'API FastAPI
    requests.post("http://api_nlp:8000/change_feedback/", json=json_data)


def render_feedback(repo_url):
    """Affiche un système de feedback par étoiles interactif."""
    st.write(f"Évaluez le repository '{repo_url}':")
    if not 'rating' in locals():
        rating = None
    rating = st.feedback(options="stars", key=f"feedback_{repo_url}")
    if rating is not None:
        rating += 1
        st.write(f"Vous avez donné une note de {rating} étoile(s) pour '{repo_url}'.")
        change_feedback(user_id=1, repo_link=repo_url, rating=rating)
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
                st.session_state['repos'] = fetch_recommended_repos(username, number)
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
        render_feedback(repo['url'])
        st.markdown("---")

st.markdown("""
<hr>
<div style='text-align: center;'>
Développé avec ❤️ en utilisant Streamlit.
</div>
""", unsafe_allow_html=True)
