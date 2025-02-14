import numpy as np
import spacy
from deep_translator import GoogleTranslator
from spacy.lang.fr.stop_words import STOP_WORDS 

# Route GET avec paramètre
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

"""
if __name__ == "__main__":
    # Exemple d'utilisation

    description = "This is a description."
    vec = description_to_vec(description)
    
    description_2 = "There is a resume."
    vec_2 = description_to_vec(description_2)

    description_3 = "I ate a car last nignt."
    vec_3 = description_to_vec(description_3)

    description_4 = "it is not a short text."
    vec_4 = description_to_vec(description_4)

    # Calcul de la similarité cosinus
    similarity = np.dot(vec, vec_2) / (np.linalg.norm(vec) * np.linalg.norm(vec_2))
    print(similarity)

    similarity_2 = np.dot(vec_2, vec_3) / (np.linalg.norm(vec_2) * np.linalg.norm(vec_3))
    print(similarity_2)

    similarity_3 = np.dot(vec_2, vec_4) / (np.linalg.norm(vec_2) * np.linalg.norm(vec_4))
    print(similarity_3)
"""