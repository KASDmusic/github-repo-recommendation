from fastapi import FastAPI
from pydantic import BaseModel

import numpy as np
import spacy
from deep_translator import GoogleTranslator
from spacy.lang.fr.stop_words import STOP_WORDS 

import psycopg2
import datetime

from typing import Optional

# Connexion à la base de données PostgreSQL
DB_CONFIG = {
    "dbname": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "host": "postgres",  # Si PostgreSQL est dans un conteneur Docker, remplacez par "postgres"
    "port": "5432"
}

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


class FeedbackRequest(BaseModel):
    user_id: Optional[int]  # Peut être NULL
    repo_link: str
    rating: int

# Route post avec paramètre
@app.post("/change_feedback/")
def change_feedback(feedback: FeedbackRequest):
    """
    Insère une nouvelle note ou met à jour une note existante dans la base de données PostgreSQL.

    - Si une note existe pour (user_id, repo_link), elle est mise à jour.
    - Sinon, une nouvelle note est créée.
    """

    user_id = feedback.user_id
    repo_link = feedback.repo_link
    rating = feedback.rating

    try:
        # Connexion à PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Vérifier si une note existe déjà pour cet utilisateur et ce repo_link
        cur.execute("""
            SELECT COUNT(*) FROM notes WHERE user_id = %s AND repo_link = %s;
        """, (user_id, repo_link))
        
        existing_note = cur.fetchone()

        

        if existing_note[0] > 0:
            # Mise à jour de la note existante
            cur.execute("""
                UPDATE notes 
                SET note = %s, date = %s
                WHERE user_id = %s AND repo_link = %s;
            """, (rating, datetime.now(), user_id, repo_link))
            print(f"Note mise à jour : {rating} étoiles pour {repo_link}")
        else:
            # Insertion d'une nouvelle note
            cur.execute("""
                INSERT INTO notes (user_id, repo_link, note)
                VALUES (%s, %s, %s);
            """, (user_id, repo_link, rating))
            print(f"Nouvelle note ajoutée : {rating} étoiles pour {repo_link}")

        # Valider les changements
        conn.commit()

    except Exception as e:
        print(f"Erreur lors de la mise à jour de la note : {e}")
    finally:
        # Fermer la connexion
        if cur:
            cur.close()
        if conn:
            conn.close()

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