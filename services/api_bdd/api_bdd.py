from fastapi import FastAPI, HTTPException
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from init_bdd import ElasticManager
from pydantic import BaseModel
from typing import List
import random

import logging

# Initialisation de FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de recommandation de dépôts GitHub."}

@app.post("/create_index/{index_name}")
def create_index(index_name: str):
    """Créer un index Elasticsearch."""
    result = ElasticManager.create_index(index_name)
    return result

@app.delete("/delete_index/{index_name}")
def delete_index(index_name: str):
    """Supprimer un index Elasticsearch."""
    result = ElasticManager.delete_index(index_name)
    return result

@app.post("/insert_data/{index_name}")
def insert_data(index_name: str):
    """Insérer des données dans Elasticsearch."""
    try:
        # Charger les données du fichier JSON
        json_file_path = '../app/data/processed/updated_repository.json'
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Insérer uniquement les 10 premières lignes pour tester
        ElasticManager.insert_data(index_name, data[:10])
        return {"message": f"Les 10 premières données ont été insérées dans {index_name}."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/find_similar_repos/")
def find_similar_repos(embedding_str: str, n: int):
    """Calculer la similarité cosinus et retourner les n voisins les plus proches."""
    try:
        # Convertir l'embedding en liste en enlevant les crochets
        embedding = [float(x) for x in embedding_str.replace('[', '').replace(']', '').split(',')]

        # Convertir l'embedding en numpy array
        embedding_array = np.array(embedding).reshape(1, -1)
        
        # Récupérer tous les embeddings stockés dans Elasticsearch
        all_repos = ElasticManager.get_all_embeddings()
        if not all_repos:
            raise HTTPException(status_code=404, detail="Aucun embedding trouvé dans la base.")

        repo_vectors = [repo['repository_vector'] for repo in all_repos]
        repo_names = [repo['full_name'] for repo in all_repos]

        # Vérifier que les embeddings sont valides
        if not repo_vectors:
            raise HTTPException(status_code=500, detail="Aucune donnée d'embedding récupérée.")

        # Convertir les embeddings en numpy array
        repo_vectors_array = np.array(repo_vectors)

        # Vérifier la dimension de l'embedding
        if embedding_array.shape[1] != repo_vectors_array.shape[1]:
            raise HTTPException(status_code=400, detail="La dimension de l'embedding ne correspond pas aux données stockées.")

        # Calculer la similarité cosinus
        similarities = cosine_similarity(embedding_array, repo_vectors_array).flatten()

        # Récupérer les indices des n voisins les plus proches
        n = min(n, len(similarities))  # Éviter les erreurs si n > nombre d'embeddings disponibles
        similar_indices = similarities.argsort()[-n:][::-1]

        # Construire un dictionnaire avec les noms des repos et leurs scores de similarité
        similar_repos = {repo_names[idx]: similarities[idx] for idx in similar_indices}

        return {"similar_repos": similar_repos}

    except Exception as e:
        logging.error(f"Erreur lors de la recherche de repos similaires: {e}")
        raise HTTPException(status_code=500, detail=str(e))





