from pydantic import BaseModel

import numpy as np
import spacy
from deep_translator import GoogleTranslator
from spacy.lang.fr.stop_words import STOP_WORDS 
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional,  Dict
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import logging
import psycopg2
import datetime

# Définition des URL de base pour chacun des services
GITHUB_API_URL = "http://api_github:8001"   # Service GitHub
NLP_API_URL = "http://api_nlp:8000"           # Service NLP
BDD_API_URL = "http://api_bdd:2100"           # Service Elasticsearch/BDD

from typing import Optional

nlp = spacy.load('en_core_web_lg')

# Connexion à la base de données PostgreSQL
DB_CONFIG = {
    "dbname": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "host": "postgres",  # Si PostgreSQL est dans un conteneur Docker, remplacez par "postgres"
    "port": "5432"
}

# Initialisation de l'application FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Route GET avec paramètre
@app.get("/user_recommandation/")
def user_recommandation(user: str, n: int):
    recommended_repos = [
        {"name": "awesome-python", "description": "A curated list of awesome Python frameworks and libraries.", "url": "https://github.com/vinta/awesome-python"},
        {"name": "react", "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.", "url": "https://github.com/facebook/react"},
        {"name": "tensorflow", "description": "An open source machine learning framework for everyone.", "url": "https://github.com/tensorflow/tensorflow"},
    ]
    return recommended_repos[:n]


class FeedbackRequest(BaseModel):
    user_id: Optional[int]  # Peut être NULL
    repo_link: str
    rating: int

# Route post avec paramètre
@app.post("/change_feedback/")
def change_feedback(feedback: FeedbackRequest):
    """
    Insère une nouvelle note ou met à jour une note existante dans la base de données PostgreSQL.

    - Si une note existe pour (user_id, repo_link), elle est mise à jour.
    - Sinon, une nouvelle note est créée.
    """

    user_id = feedback.user_id
    repo_link = feedback.repo_link
    rating = feedback.rating

    try:
        # Connexion à PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Vérifier si une note existe déjà pour cet utilisateur et ce repo_link
        cur.execute("""
            SELECT COUNT(*) FROM notes WHERE user_id = %s AND repo_link = %s;
        """, (user_id, repo_link))
        
        existing_note = cur.fetchone()

        

        if existing_note[0] > 0:
            # Mise à jour de la note existante
            cur.execute("""
                UPDATE notes 
                SET note = %s, date = %s
                WHERE user_id = %s AND repo_link = %s;
            """, (rating, datetime.now(), user_id, repo_link))
            print(f"Note mise à jour : {rating} étoiles pour {repo_link}")
        else:
            # Insertion d'une nouvelle note
            cur.execute("""
                INSERT INTO notes (user_id, repo_link, note)
                VALUES (%s, %s, %s);
            """, (user_id, repo_link, rating))
            print(f"Nouvelle note ajoutée : {rating} étoiles pour {repo_link}")

        # Valider les changements
        conn.commit()

    except Exception as e:
        print(f"Erreur lors de la mise à jour de la note : {e}")
    finally:
        # Fermer la connexion
        if cur:
            cur.close()
        if conn:
            conn.close()

# Route GET avec paramètre
@app.get("/description_to_vec/")
def description_to_vec(description: str):
    """
    Transform a description into a vector representation.
    With doing preprocessing and translation.
    """
    # Nettoyage des données en ne prenant que les caractères alphabétiques
    description = ''.join(e for e in description if e.isalnum() or e.isspace())

    # Traduis en anglais
    description_en = GoogleTranslator(source='auto', target='en').translate(description)
    description_en_nlp = nlp(description_en)
    # Tokenisation, suppression des mots vides et de la ponctuation
    tokens = [token.lemma_.lower() for token in description_en_nlp 
              if token.text not in STOP_WORDS 
              and not token.is_punct 
              and not token.is_space]

    # Retourne le vecteur moyen des mots
    return nlp(' '.join(tokens)).vector.tolist()

class Repo(BaseModel):
    full_name: str
    description: Optional[str] = None
    html_url: Optional[str] = None
    language: Optional[str] = None
    stargazers_count: Optional[int] = None
    created_at: Optional[str] = None

class ClusterResult(BaseModel):
    cluster_centers: List[List[float]]
    clusters: dict
    chosen_k: int
    silhouette_score: float

def cluster_repos_auto_impl(repos: List[Repo], max_k: int = 10) -> dict:
    """
    Pour une liste de dépôts, cette fonction :
      - Calcule le vecteur de la description pour chaque dépôt.
      - Si moins de 2 vecteurs sont disponibles, retourne directement le résultat.
      - Teste différents nombres de clusters (de 2 à max_k) et sélectionne celui qui maximise le score de silhouette.
      - Effectue le clustering avec le k optimal et retourne les centres de clusters ainsi que les dépôts regroupés.
    """
    vectors = []
    valid_repos = []
    # Boucle sur les repos pour obtenir les vecteurs de description av
    for repo in repos:
        if repo.description:
            vec = description_to_vec(repo.description)
            vectors.append(vec)
            valid_repos.append(repo)
    
    if not vectors:
        raise ValueError("Aucune description valide trouvée dans les dépôts.")
    vectors = np.array(vectors)
    
    # Si on a moins de 2 dépôts, pas de clustering possible
    if len(vectors) < 2:
        return {
            "cluster_centers": vectors.tolist(),
            "clusters": {0: [r.dict() for r in valid_repos]},
            "chosen_k": 1,
            "silhouette_score": 1.0
        }
    
    # Définir max_k en fonction du nombre de vecteurs
    max_possible_k = min(max_k, len(vectors))
    
    best_k = 2
    best_score = -1
    # Tester pour k variant de 2 à max_possible_k
    for k in range(2, max_possible_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42).fit(vectors)
        labels = kmeans.labels_
        try:
            score = silhouette_score(vectors, labels)
        except Exception as e:
            logging.error(f"Erreur lors du calcul du score de silhouette pour k={k}: {e}")
            continue
        if score > best_score:
            best_score = score
            best_k = k

    # Clustering final avec le k optimal
    final_kmeans = KMeans(n_clusters=best_k, random_state=42).fit(vectors)
    final_labels = final_kmeans.labels_
    centers = final_kmeans.cluster_centers_
    
    # Regroupement des dépôts par cluster
    clusters = {}
    for label, repo in zip(final_labels, valid_repos):
        clusters.setdefault(int(label), []).append(repo.dict())
    return {
        "cluster_centers": centers.tolist(),
        "clusters": clusters,
        "chosen_k": best_k,
        "silhouette_score": best_score
    }

@app.post("/cluster_repos_auto/", response_model=ClusterResult)
def cluster_repos_auto(repos: List[Repo], max_k: int = 10):
    """
    Endpoint qui regroupe automatiquement les dépôts en clusters basés sur la similarité de leurs descriptions.
    Le nombre de clusters est déterminé automatiquement en optimisant le score de silhouette.
    
    - **repos** : Liste de dépôts (chaque dépôt doit avoir au moins un champ description).
    - **max_k** : Nombre maximal de clusters à tester (défaut 10).
    
    Retourne les centres de clusters, les dépôts regroupés par cluster, le nombre de clusters choisi et le score de silhouette.
    """
    try:
        result = cluster_repos_auto_impl(repos, max_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/user_recommendation_full/")
def user_recommendation_full(user: str, n: int):
    """
    Pour un utilisateur donné et un nombre n :
      1. Récupère les dépôts starés via le service GitHub.
      2. Filtre ceux disposant d'une description et les convertit en instances de Repo.
      3. Applique localement le clustering (via cluster_repos_auto_impl) pour obtenir les centres.
      4. Pour chaque centre, appelle le service BDD (endpoint /find_similar_repos/) qui renvoie 
         une liste de documents (chacun contenant tous les champs et un score de similarité).
      5. Agrège les résultats en conservant, pour chaque dépôt, le document ayant le meilleur score,
         trie par score décroissant et renvoie les n dépôts les plus pertinents.
    """
    try:
        # 1. Récupérer les dépôts starés via le service GitHub
        github_url = f"{GITHUB_API_URL}/starred/{user}"
        github_response = requests.get(github_url)
        if github_response.status_code != 200:
            raise HTTPException(
                status_code=github_response.status_code, 
                detail=f"Erreur lors de la récupération GitHub: {github_response.text}"
            )
        starred_repos = github_response.json()
        if not starred_repos:
            raise HTTPException(status_code=404, detail=f"Aucun dépôt trouvé pour l'utilisateur {user}.")

        # 2. Filtrer les dépôts avec description et construire des instances de Repo
        repos_for_clustering = []
        for repo in starred_repos:
            if repo.get("description"):
                repos_for_clustering.append(Repo(**repo))
        if not repos_for_clustering:
            raise HTTPException(status_code=404, detail="Aucun dépôt avec description n'a été trouvé.")

        # 3. Clustering local via la fonction interne
        clustering_result = cluster_repos_auto_impl(repos_for_clustering, max_k=5)
        cluster_centers = clustering_result.get("cluster_centers", [])
        if not cluster_centers:
            raise HTTPException(status_code=500, detail="Aucun centre de cluster obtenu.")

        # 4. Pour chaque centre, interroger le service BDD via son endpoint qui renvoie la liste complète des documents
        aggregated_results: Dict[str, Dict] = {}
        bdd_url = f"{BDD_API_URL}/find_similar_repos/"
        for center in cluster_centers:
            # Convertir le vecteur centre en chaîne de caractères (format attendu par le service BDD)
            embedding_str = str(center)
            params = {"embedding_str": embedding_str, "n": 10}  # Récupérer les 10 plus proches pour chaque centre
            bdd_response = requests.get(bdd_url, params=params)
            if bdd_response.status_code != 200:
                logging.error(f"Erreur BDD pour centre {center}: {bdd_response.text}")
                continue
            similar_docs = bdd_response.json()  # Liste de documents avec tous les champs et le score
            for doc in similar_docs:
                repo_name = doc.get("full_name")
                score = doc.get("score", 0)
                if not repo_name:
                    continue
                # Conserver le document avec le meilleur score en cas d'apparition multiple
                if repo_name in aggregated_results:
                    if score > aggregated_results[repo_name].get("score", 0):
                        aggregated_results[repo_name] = doc
                else:
                    aggregated_results[repo_name] = doc

        if not aggregated_results:
            raise HTTPException(status_code=404, detail="Aucun dépôt similaire trouvé.")

        # 5. Trier les résultats par score décroissant et retourner les n meilleurs
        sorted_results = sorted(aggregated_results.values(), key=lambda d: d.get("score", 0), reverse=True)[:n]
        return {"recommended_repos": sorted_results}

    except Exception as e:
        logging.error(f"Erreur dans user_recommendation_full pour l'utilisateur {user}: {e}")
        raise HTTPException(status_code=500, detail=str(e))