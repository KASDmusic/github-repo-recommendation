import requests
import json 
import time

ELASTIC_URL = "http://elasticsearch:9200"
HEADERS = {"Content-Type": "application/json"}

# Exemple d'index vectoriel
index_mapping = {
    "mappings": {
        "properties": {
            "repository_vector": {
                "type": "dense_vector",
                "dims": 128
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

def insert_data(index_name, data):
    for repo in data:
        response = requests.post(f"{ELASTIC_URL}/{index_name}/_doc", json=repo, headers=HEADERS)
        print(response.json())

def add_repository(repo_name, repo_description, repo_vector):
    document = {
        "repository_name": repo_name,
        "repository_description": repo_description,
        "repository_vector": repo_vector
    }
    ELASTIC_URL.index(index="github_repositories", document=document)


if __name__ == "__main__":

    time.sleep(60)

    delete_index("github_repositories")
    create_index("github_repositories")
    
    # Load JSON data
    json_file_path = '/github-repo-recommendation/services/git_api/github_repos_py.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    insert_data("github_repositories", data)
