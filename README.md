# github-repo-recommendation

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Le projet consiste en une recommandation de dépôts Github en fonction des stars d'un utilisateur.

Le principe consiste à soumettre un nom d'utilisateur et un nombre de recommandations a l'interface.

Elle renvoie, dans l'ordre de pertinence, le nombre de dépôts demandés.

Un système de notation des recommandations est présente pour chaque dépôt, cela permet à court terme d'évaluer la pertinence des recommandations et permettra à long terme de développer des systèmes de recommandation collaboratif.

## Lancer le projet

Télécharger les données à https://www.kaggle.com/datasets/allaneee/github-repo-embedded.

Git clone le projet.

Mettre les 5 json dans /data/processed/

Faire 'docker compose up --build'

![Description du GIF](doc/Sini.gif)

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

```

--------

