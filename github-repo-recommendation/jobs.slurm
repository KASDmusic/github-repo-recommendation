#!/bin/bash

#SBATCH --job-name=job_bigdata_GARNIER

# Fichiers de sortie et d'erreur
#SBATCH --output=job_bigdata_GARNIER.out
#SBATCH --error=job_bigdata_GARNIER.err

# Temps maximum d'exécution (format : jours-heures:minutes:secondes)
#SBATCH --time=50:00:00

# Nombre de nœuds et tâches
#SBATCH --nodes=1              # Nombre de nœuds
#SBATCH --ntasks=1             # Nombre de tâches (processus)
#SBATCH --cpus-per-task=1      # Nombre de CPU par tâche

# Charger des modules ou activer un environnement
source ~/miniconda3/bin/activate


# Commande à exécuter
python recup_repo.py