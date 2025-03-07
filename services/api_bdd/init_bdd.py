import json
import requests
import time
import logging
import math  # Pour gérer math.isnan

# Configuration
ELASTIC_URL = "http://elasticsearch:9200"
HEADERS = {"Content-Type": "application/json"}

# Mapping de l'index Elasticsearch
index_mapping = {
    "mappings": {
        "properties": {
            "repository_vector": {
                "type": "dense_vector",
                "dims": 300
            },
            "full_name": {
                "type": "text"
            },
            "html_url": {
                "type": "text"
            },
            "description": {
                "type": "text"
            },
            "language": {
                "type": "text"
            },
            "stargazers_count": {
                "type": "integer"
            },
            "created_at": {
                "type": "date"
            }
        }
    }
}

class ElasticManager:
    """Gère les opérations sur Elasticsearch."""
    # Initialisation d'un compteur pour l'id des documents
    indice_repos = 0

    @staticmethod
    def create_index(index_name: str):
        response = requests.put(f"{ELASTIC_URL}/{index_name}", json=index_mapping, headers=HEADERS)
        return response.json()

    @staticmethod
    def delete_index(index_name: str):
        response = requests.delete(f"{ELASTIC_URL}/{index_name}")
        return response.json()

    @staticmethod
    def insert_data(index_name: str, json_file_path: str, chunk_size: int = 100):
        """Insère les repositories avec un identifiant personnalisé dans Elasticsearch."""

        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            logging.error(f"Erreur lors du chargement du fichier JSON: {e}")
            return

        count = 0
        chunk = []

        for repo in data:
            if "repository_vector" in repo:
                repo_vector = repo["repository_vector"]
                if isinstance(repo_vector, (list, dict)) and repo_vector:
                    chunk.append(repo)
                elif isinstance(repo_vector, float) and not math.isnan(repo_vector):
                    logging.warning(f"{repo.get('full_name', 'Unknown')} a un embedding de type float.")
                else:
                    logging.warning(f"{repo.get('full_name', 'Unknown')} n'a pas de repository_vector valide ou est vide.")

            if len(chunk) == chunk_size:
                for doc in chunk:
                    # Utiliser PUT pour définir un id personnalisé
                    doc_id = ElasticManager.indice_repos
                    response = requests.put(f"{ELASTIC_URL}/{index_name}/_doc/{doc_id}", json=doc, headers=HEADERS)
                    if response.status_code in (200, 201):
                        logging.info(f"{response.status_code} - {doc['full_name']} inséré avec l'id {doc_id}.")
                    else:
                        logging.error(f"Erreur lors de l'insertion de {doc['full_name']} : {response.text}")
                    ElasticManager.indice_repos += 1
                count += len(chunk)
                chunk = []

        if chunk:
            for doc in chunk:
                doc_id = ElasticManager.indice_repos
                response = requests.put(f"{ELASTIC_URL}/{index_name}/_doc/{doc_id}", json=doc, headers=HEADERS)
                if response.status_code in (200, 201):
                    logging.info(f"{response.status_code} - {doc['full_name']} inséré avec l'id {doc_id}.")
                else:
                    logging.error(f"Erreur lors de l'insertion de {doc['full_name']} : {response.text}")
                ElasticManager.indice_repos += 1
            count += len(chunk)

        logging.info(f"{count} repositories insérés au total.")
        logging.info("Traitement terminé.")

    @staticmethod
    def get_all_embeddings():
        """Récupérer tous les embeddings depuis Elasticsearch."""
        query = {
            "query": {
                "match_all": {}
            },
            "_source": ["repository_vector", "full_name"],  # Champs à récupérer
            "size": 10000  # Ajustez la taille si nécessaire
        }
        res = requests.get(f"{ELASTIC_URL}/github_repositories/_search", json=query, headers=HEADERS)
        
        if res.status_code == 200:
            return res.json()['hits']['hits']
        else:
            raise Exception(f"Erreur lors de la récupération des embeddings: {res.text}")

if __name__ == "__main__":
    time.sleep(45)  # Attendre que Elasticsearch soit prêt

    # Vérifier si l'index existe
    response = requests.get(f"{ELASTIC_URL}/github_repositories")
    if response.status_code == 200:
        print("L'index existe déjà.")
    else:
        ElasticManager.create_index("github_repositories")

        #Liste de tous vos fichiers JSON
        json_files = [
            "../app/data/processed/data_part_0.json",
            "../app/data/processed/data_part_1.json",
            "../app/data/processed/data_part_2.json",
            "../app/data/processed/data_part_3.json",
            "../app/data/processed/data_part_4.json",
            "../app/data/processed/data_part_5.json",
            ]

        for file_path in json_files:
            ElasticManager.insert_data("github_repositories", file_path)

        # Afficher le dictionnaire de l'index
    print("ça marche")

    
