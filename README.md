# github-repo-recommendation

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

<a target="_blank" href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi" />
</a>

<a target="_blank" href="https://www.elastic.co/kibana/">
    <img src="https://img.shields.io/badge/Kibana-Visualization-005571?logo=kibana" />
</a>

<a target="_blank" href="https://www.elastic.co/elasticsearch/">
    <img src="https://img.shields.io/badge/Elasticsearch-Search%20Engine-005571?logo=elasticsearch" />
</a>

<a target="_blank" href="https://streamlit.io/">
    <img src="https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit" />
</a>

<a target="_blank" href="https://docs.github.com/en/rest">
    <img src="https://img.shields.io/badge/GitHub%20API-REST%20Interface-181717?logo=github" />
</a>

<a target="_blank" href="https://spacy.io/">
    <img src="https://img.shields.io/badge/spaCy-NLP%20Library-09A3D5?logo=spacy" />
</a>

![Description du GIF](docs/Sini.gif)

Le projet consiste en une recommandation de dépôts Github en fonction des stars d'un utilisateur.

Le principe consiste à soumettre un nom d'utilisateur et un nombre de recommandations a l'interface.

Elle renvoie, dans l'ordre de pertinence, le nombre de dépôts demandés.

Un système de notation des recommandations est présente pour chaque dépôt, cela permet à court terme d'évaluer la pertinence des recommandations et permettra à long terme de développer des systèmes de recommandation collaboratif.

## Lancer le projet

Télécharger les données à https://www.kaggle.com/datasets/allaneee/github-repo-embedded.

Git clone le projet.

Mettre les 5 json dans /data/processed/

Faire 'docker compose up --build'

## Lien d'accès aux applications une fois lancé

Interface utilisateur : [http://localhost:8501/](http://localhost:8501/)

Interface administrateur : [http://localhost:8502/](http://localhost:8502/)

Kibana : [http://localhost:5602/](http://localhost:5602/)

Elastic search : [http://localhost:9201/](http://localhost:9201/)

PostgreSQL : [http://localhost:5432/](http://localhost:5432/)

Api_bdd : [http://localhost:2100/](http://localhost:2100/)

Api_nlp : [http://localhost:8000/](http://localhost:8000/)

Api_github : [http://localhost:8001/](http://localhost:8001/)

## Organisation du projet

```
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         github-repo-recommendation and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
│
├── github-repo-recommendation   <- Source code for use in this project
│   │
│   ├── __init__.py              <- Makes github-repo-recommendation a Python module
│   │
│   ├── jobs.slurm               <- Slurm script for github's data
│   │
│   └── recup_repo.py            <- Scripts to download repositories
│
├── services  <- Source code for differents services.
│   │
│   ├── api_bdd            <- Container Useful for using the database
│   │
│   ├── api_github         <- Container for using github's api
│   │
│   ├── api_nlp            <- Container using embedding's model
│   │
│   ├── elasticsearch      <- Container of elasticsearch
│   │
│   ├── interface          <- Container of the interface
│   │
│   ├── interface_admin    <- Container of the admin interface for notation vizualisation
│   │
│   └── postgres_db        <- Container of the postgres database for the notation

