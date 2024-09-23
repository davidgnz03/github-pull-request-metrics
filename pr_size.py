import requests
from tabulate import tabulate

# GitHub repository and personal token
GITHUB_TOKEN = "YOUR_PERSONAL_ACCESS_TOKEN"  # Replace with your personal access token
REPO = "owner/repo"  # Replace with the repository in the format "owner/repo"

# Headers for authentication with GitHub API
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# Function to get the list of open pull requests in the repository
def get_open_pull_requests():
    url = f"https://api.github.com/repos/{REPO}/pulls?state=all"
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Failed to fetch PRs. Status code: {response.status_code}")
        return []

    try:
        return response.json()  # Ensure the response is in JSON format
    except ValueError:
        print("Error: The response is not valid JSON.")
        return []

# Function to calculate the size (added lines + deleted lines) of a PR
def get_pr_size(pr_number):
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Failed to fetch files for PR {pr_number}. Status code: {response.status_code}")
        return 0

    files = response.json()
    
    total_additions = sum(file.get('additions', 0) for file in files)
    total_deletions = sum(file.get('deletions', 0) for file in files)

    return total_additions + total_deletions

# Get the list of open PRs
pull_requests = get_open_pull_requests()

# List to store PR information
pr_data = []

# Process each PR and calculate its size
for pr in pull_requests:
    pr_number = pr.get('number')  # Safely access 'number' using .get()
    pr_title = pr.get('title')    # Safely access 'title' using .get()

    # Get the size of the PR
    pr_size = get_pr_size(pr_number)

    pr_data.append([pr_number, pr_title, pr_size])

# Display the results in a table
print(tabulate(pr_data, headers=["PR Number", "Title", "Size (LOC)"], tablefmt="pretty"))


