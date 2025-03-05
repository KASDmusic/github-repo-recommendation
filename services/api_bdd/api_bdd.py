from fastapi import FastAPI, HTTPException
import json
from init_bdd import ElasticManager

# Initialisation de FastAPI
app = FastAPI()

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
