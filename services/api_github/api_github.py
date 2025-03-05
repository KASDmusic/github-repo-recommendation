from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from github import Github
import os
from dotenv import load_dotenv

# Charger les variables d'environnement et initialiser PyGithub
load_dotenv('.env')
access_token = os.getenv("token")
if access_token:
    g = Github(access_token)
else:
    g = Github()  # Authentification non-authentifiée (limité à 60 requêtes/h)

app = FastAPI()

class RepoData(BaseModel):
    full_name: str
    html_url: str
    description: Optional[str] = None
    language: Optional[str] = None
    stargazers_count: int
    forks_count: int
    created_at: str

def get_starred_repos_by_username(username: str) -> List[RepoData]:
    try:
        user = g.get_user(username)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Utilisateur {username} introuvable: {e}")
    
    starred = user.get_starred()
    results = []
    for repo in starred:
        repo_data = RepoData(
            full_name=repo.full_name,
            html_url=repo.html_url,
            description=repo.description,
            language=repo.language,
            stargazers_count=repo.stargazers_count,
            forks_count=repo.forks_count,
            created_at=repo.created_at.isoformat()
        )
        results.append(repo_data)
    return results

@app.get("/starred/{username}", response_model=List[RepoData])
async def starred_repos(username: str):
    """
    Récupère la liste des dépôts starés par l'utilisateur GitHub dont le nom est passé dans l'URL.
    """
    return get_starred_repos_by_username(username)
