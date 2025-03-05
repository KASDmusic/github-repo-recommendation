FROM python:3.9-slim

# Installer les dépendances du système
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /api_nlp

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt ./

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Télécharger le modèle de langue en anglais de Spacy
RUN python -m spacy download en_core_web_lg

# Copier le reste des fichiers de l'application
COPY . .

# Exposer le port utilisé par Streamlit
EXPOSE 8000

# Commande pour exécuter Streamlit
CMD ["uvicorn", "api_nlp:app", "--host", "0.0.0.0", "--port", "8000"]
