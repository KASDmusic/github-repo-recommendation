FROM python:3.10

WORKDIR /api_bdd

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l'API
EXPOSE 8000

COPY . .

# Donner les permissions d'exécution au script
RUN chmod +x entrypoint.sh

# Utiliser le script comme point d'entrée
ENTRYPOINT ["sh", "./entrypoint.sh"]
