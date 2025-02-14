#!/usr/bin/env python3
from datetime import datetime, timedelta
import os
import json
from github import Github
from dotenv import load_dotenv

# Charger les variables d'environnement et le token GitHub depuis le fichier .env
load_dotenv('.env')
access_token = os.getenv("token")
if not access_token:
    print("Erreur : le token GitHub n'a pas été trouvé dans .env")
    exit(1)
g = Github(access_token)

def get_readme_content(repo):
    """
    Tente de récupérer le contenu du README du repo.
    Si une erreur survient (README absent, problème d'accès, etc.), retourne une chaîne vide.
    """
    try:
        readme = repo.get_readme()
        return readme.decoded_content.decode('utf-8', errors='replace')
    except Exception as e:
        return ""

def search_repos_by_date_range(query_base, start_date, end_date, results):
    """
    Effectue une recherche sur GitHub dans l'intervalle de dates [start_date, end_date].
    Si le nombre total de résultats est >= 1000, l'intervalle est subdivisé en deux.
    Sinon, les repos sont récupérés page par page et ajoutés à la liste 'results',
    en y ajoutant également le contenu du README.
    """
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    query = f"{query_base} created:{start_str}..{end_str}"
    print(f"Recherche : {query}")
    
    try:
        repos_search = g.search_repositories(query=query, sort="stars", order="desc")
    except Exception as e:
        print("Erreur lors de la recherche :", e)
        return
    
    total_count = repos_search.totalCount
    print(f"Résultats trouvés : {total_count}")
    
    # Si le nombre de résultats est >= 1000, subdiviser l'intervalle pour contourner la limite.
    if total_count >= 1000:
        print(f"Limite atteinte pour l'intervalle {start_str}..{end_str}. Subdivision...")
        mid_date = start_date + (end_date - start_date) / 2
        search_repos_by_date_range(query_base, start_date, mid_date, results)
        search_repos_by_date_range(query_base, mid_date + timedelta(days=1), end_date, results)
    else:
        # Récupération des repos page par page
        page = 0
        while True:
            try:
                page_repos = repos_search.get_page(page)
            except Exception as e:
                print("Erreur lors de la pagination :", e)
                break
            if not page_repos:
                break
            for repo in page_repos:
                repo_data = {
                    "full_name": repo.full_name,
                    "html_url": repo.html_url,
                    "description": repo.description,
                    "language": repo.language,
                    "stargazers_count": repo.stargazers_count,
                    "created_at": repo.created_at.isoformat(),
                    "readme_content": get_readme_content(repo)
                }
                results.append(repo_data)
            print(f"Page {page+1} récupérée ({len(page_repos)} repos)")
            page += 1

def main():
    results = []
    # Modifier query_base selon vos critères.
    # Ici, on recherche des repos ayant plus de 500 étoiles.
    query_base = "stars:>500"
    
    # Définir la plage de dates (par exemple de 2010 à 2025)
    start_date = datetime(2010, 1, 1)
    end_date   = datetime(2025, 1, 1)
    
    search_repos_by_date_range(query_base, start_date, end_date, results)
    
    print(f"Total des repos collectés : {len(results)}")
    
    # Sauvegarder les résultats dans un fichier JSON
    with open("github_repos.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("Résultats sauvegardés dans 'github_repos.json'.")

if __name__ == "__main__":
    main()
