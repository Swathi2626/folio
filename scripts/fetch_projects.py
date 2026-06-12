import requests
import json
from pathlib import Path

USERNAME = "Swathi2626"

url = f"https://api.github.com/users/{USERNAME}/repos"

response = requests.get(url)

if response.status_code != 200:
    print("Failed to fetch repositories")
    exit()

repos = response.json()

projects = []

for repo in repos:

    
    if repo["fork"]:
        continue

    project = {
        "name": repo["name"],
        "description": repo["description"] or "No description available",
        "url": repo["html_url"],
        "language": repo["language"],
        "stars": repo["stargazers_count"],
        "updated": repo["updated_at"]
    }

    projects.append(project)

projects.sort(key=lambda x: x["updated"], reverse=True)

output_path = Path("data/projects.json")

with open(output_path, "w") as file:
    json.dump(projects, file, indent=4)

print("projects.json updated successfully!")