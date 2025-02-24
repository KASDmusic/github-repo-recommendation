from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9201")

# Exemple : ajouter un repository
def add_repository(repo_name, repo_description, repo_vector):
    document = {
        "repository_name": repo_name,
        "repository_description": repo_description,
        "repository_vector": repo_vector
    }
    es.index(index="github_repositories", document=document)
