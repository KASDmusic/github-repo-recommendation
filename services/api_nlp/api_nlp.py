from fastapi import FastAPI
from pydantic import BaseModel

import numpy as np
import spacy
from deep_translator import GoogleTranslator
from spacy.lang.fr.stop_words import STOP_WORDS 

# Initialisation de l'application FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

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

# Route GET avec paramètre
@app.get("/description_to_vec/")
def description_to_vec(description: str):
    """
    Transform a description into a vector representation.
    With doing preprocessing and translation.
    """

    nlp = spacy.load('en_core_web_lg')

    # Traduis en anglais
    description_en = GoogleTranslator(source='auto', target='en').translate(description)

    description_en_nlp = nlp(description_en)

    # Tokenisation, suppression des mots vides et de la ponctuation
    tokens = [token.lemma_.lower() for token in description_en_nlp 
              if token.text not in STOP_WORDS 
              and not token.is_punct 
              and not token.is_space]

    # Retourne le vecteur moyen des mots
    return nlp(' '.join(tokens)).vector.tolist()