from fastapi import FastAPI, HTTPException
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from init_bdd import ElasticManager
from pydantic import BaseModel
from typing import List
from elasticsearch import Elasticsearch
from typing import List, Dict

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


def search_similar_documents(es: Elasticsearch, index_name: str, query_vector: List[float], k: int = 5) -> List[Dict]:
    """
    Recherche les k documents les plus similaires à un embedding donné dans Elasticsearch.

    :param es: Instance de connexion à Elasticsearch.
    :param index_name: Nom de l'index Elasticsearch.
    :param query_vector: Vecteur de requête pour la recherche de similarité.
    :param k: Nombre de documents les plus proches à retourner.
    :return: Liste de dictionnaires contenant les champs du document et le score de similarité.
    """
    query = {
        "size": k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'repository_vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }

    response = es.search(index=index_name, body=query)

    results = [
        {
            "score": hit["_score"],
            **hit["_source"]  # Inclure tous les champs du document
        }
        for hit in response["hits"]["hits"]
    ]
    logging.error(results)
    return results

@app.get("/find_similar_repos/")
def find_similar_repos(embedding_str: str, n: int):
    """Calculer la similarité cosinus et retourner les n voisins les plus proches."""
    try:
        # Convertir l'embedding en liste en enlevant les crochets
        embedding = [float(x) for x in embedding_str.replace('[', '').replace(']', '').split(',')]

        # Calculer la similarité cosinus avec Elasticsearch
        es = Elasticsearch("http://elasticsearch:9200")
        index_name = "github_repositories"
        results = search_similar_documents(es, index_name, embedding, k=n)
        return results


    except Exception as e:
        logging.error(f"Erreur lors de la recherche de repos similaires: {e}")
        raise HTTPException(status_code=500, detail=str(e))





