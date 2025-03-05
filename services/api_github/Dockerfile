# Utilise une image Python 3.10 slim comme base
FROM python:3.10-slim

# Empêche la création de fichiers pyc et force la sortie standard non bufferisée
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /api_github

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le container
COPY . .

# Exposer le port 8000 (celui utilisé par Uvicorn)
EXPOSE 8000

# Lancer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "api_github:app", "--host", "0.0.0.0", "--port", "8001"]
