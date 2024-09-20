import json
import requests

# Load the clients.json file
with open('clients.json', 'r') as f:
    data = json.load(f)

# Function to extract the owner and repo name from a GitHub URL
def extract_owner_and_repo(url):
    parts = url.replace("https://github.com/", "").split("/")
    return parts[0], parts[1]

# Function to get repo info from GitHub API
def fetch_repo_info(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)
    if response.status_code == 200:
        repo_data = response.json()
        return repo_data['stargazers_count'], repo_data['forks_count']
    else:
        print(f"Failed to fetch data for {owner}/{repo}")
        return None, None

# Iterate through clients and update stars and forks
for category in data:
    for client in data[category]:
        owner, repo = extract_owner_and_repo(client['repo'])
        stars, forks = fetch_repo_info(owner, repo)
        if stars is not None and forks is not None:
            client['repo_stars'] = stars
            client['repo_forks'] = forks
        else:
            client['repo_stars'] = 0
            client['repo_forks'] = 0

# Save the updated data back to clients.json
with open('clients.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Clients.json updated successfully!")
