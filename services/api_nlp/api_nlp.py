from fastapi import FastAPI
from pydantic import BaseModel

# Initialisation de l'application FastAPI
app = FastAPI()

def init():

    print("lancement de l'api")

# Route GET avec paramètre
@app.get("/user_recommandation/")
def user_recommandation(user: str, n: int):
    recommended_repos = [
        {"name": "awesome-python", "description": "A curated list of awesome Python frameworks and libraries.", "url": "https://github.com/vinta/awesome-python"},
        {"name": "react", "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.", "url": "https://github.com/facebook/react"},
        {"name": "tensorflow", "description": "An open source machine learning framework for everyone.", "url": "https://github.com/tensorflow/tensorflow"},
    ]
    return recommended_repos[:n]

# Route post avec paramètre
@app.post("/mark_repo_recommandation/")
def mark_repo_recommandation(user: str, repo_link: str, mark: int):
    pass



init()



