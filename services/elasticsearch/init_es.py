import requests

ELASTIC_URL = "http://localhost:9201"
HEADERS = {"Content-Type": "application/json"}

# Exemple d'index vectoriel
index_mapping = {
    "mappings": {
        "properties": {
            "repository_vector": {
                "type": "dense_vector",
                "dims": 128
            },
            "repository_name": {
                "type": "text"
            },
            "repository_description": {
                "type": "text"
            }
        }
    }
}

def create_index(index_name):
    response = requests.put(f"{ELASTIC_URL}/{index_name}", json=index_mapping, headers=HEADERS)
    print(response.json())

if __name__ == "__main__":
    create_index("github_repositories")
