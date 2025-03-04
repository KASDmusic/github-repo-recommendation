import requests
import json 
import time

ELASTIC_URL = "http://elasticsearch:9200"
NLP_URL = "http://api_nlp:8000/description_to_vec/"
HEADERS = {"Content-Type": "application/json"}

# Exemple d'index vectoriel
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

def create_index(index_name):
    response = requests.put(f"{ELASTIC_URL}/{index_name}", json=index_mapping, headers=HEADERS)
    print(response.json())

def delete_index(index_name):
    response = requests.delete(f"{ELASTIC_URL}/{index_name}")
    print(response.json())

def get_embedding(description):
    response = requests.get(NLP_URL, params={"description": description})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get embedding for description: {description}")
        return None

def insert_data(index_name, data):
    for repo in data:
        embedding = get_embedding(repo["description"])
        if embedding:
            repo["repository_vector"] = embedding
        response = requests.post(f"{ELASTIC_URL}/{index_name}/_doc", json=repo, headers=HEADERS)
        print(response.json())

if __name__ == "__main__":
    time.sleep(40)

    create_index("github_repositories")
    
    # Load JSON data
    json_file_path = '../app/data/processed/github_repos.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    #insert_data("github_repositories", data)