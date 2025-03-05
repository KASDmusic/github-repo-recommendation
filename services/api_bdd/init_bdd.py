import json
import requests
import time
import logging


# Configuration
ELASTIC_URL = "http://elasticsearch:9200"
HEADERS = {"Content-Type": "application/json"}


# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

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
        """Insère uniquement les repositories contenant un embedding dans Elasticsearch."""

        logging.info("Début de l'insertion des données.")
        
        # Ouvrir le fichier JSON en mode lecture
        with open(json_file_path, 'r') as file:
            count = 0  # Compteur de repositories insérés
            chunk = []  # Liste pour stocker temporairement un chunk de repositories

            for line in file:
                try:
                    # Chaque ligne est supposée être un objet JSON
                    repo = json.loads(line.strip())  # Charger chaque ligne comme un objet JSON
                    
                    # Vérifier si l'embedding est présent et non vide
                    if "repository_vector" in repo:
                        repo_vector = repo["repository_vector"]
                        
                        # Vérifier si 'repository_vector' est un itérable (liste ou dictionnaire) et non vide
                        if isinstance(repo_vector, (list, dict)) and repo_vector:
                            chunk.append(repo)  # Ajouter au chunk
                        # Si c'est un float (ou autre type non itérable), on peut le traiter différemment (en fonction de votre logique)
                        elif isinstance(repo_vector, float) and not repo_vector.is_nan():
                            # Gérer les cas où repository_vector est un float (si besoin de logique spécifique ici)
                            logging.warning(f"{repo['full_name']} a un embedding de type float.")
                        else:
                            logging.warning(f"{repo['full_name']} n'a pas de repository_vector valide ou vide.")
                        
                        # Si le chunk atteint la taille désirée, on l'envoie dans Elasticsearch
                        if len(chunk) == chunk_size:
                            # Envoi du chunk à Elasticsearch
                            for repo_to_insert in chunk:
                                res = requests.post(f"{ELASTIC_URL}/{index_name}/_doc", json=repo_to_insert, headers=HEADERS)
                                if res.status_code == 201:  # Si l'insertion a réussi
                                    logging.info(f"{res.status_code} - {repo_to_insert['full_name']} inséré.")
                                else:
                                    logging.error(f"Erreur lors de l'insertion de {repo_to_insert['full_name']} : {res.text}")
                            count += len(chunk)  # Incrémenter le compteur avec la taille du chunk
                            chunk = []  # Réinitialiser le chunk pour le prochain ensemble de données

                except json.JSONDecodeError as e:
                    logging.error(f"Erreur lors de la lecture de la ligne JSON: {e}")
                    continue  # Passer à la ligne suivante en cas d'erreur

            # Traiter le dernier chunk restant (s'il y en a un)
            if chunk:
                for repo_to_insert in chunk:
                    res = requests.post(f"{ELASTIC_URL}/{index_name}/_doc", json=repo_to_insert, headers=HEADERS)
                    if res.status_code == 201:  # Si l'insertion a réussi
                        logging.info(f"{res.status_code} - {repo_to_insert['full_name']} inséré.")
                    else:
                        logging.error(f"Erreur lors de l'insertion de {repo_to_insert['full_name']} : {res.text}")
                count += len(chunk)  # Incrémenter le compteur avec la taille du dernier chunk

            logging.info(f"{count} repositories insérés au total.")
        
        logging.info("Traitement terminé.")




if __name__ == "__main__":
    # Attendre que Elasticsearch soit prêt
    time.sleep(60)

    ElasticManager.create_index("github_repositories")
    print("ça marche")