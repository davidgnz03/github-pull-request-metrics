import requests
from tabulate import tabulate

# GitHub repository and personal token
GITHUB_TOKEN = "YOUR_PERSONAL_ACCESS_TOKEN"  # Replace with your personal access token
REPO = "owner/repo"  # Replace with the repository in the format "owner/repo"

# Headers for authentication with GitHub API
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# Function to get the list of pull requests (only closed PRs)
def get_closed_pull_requests():
    url = f"https://api.github.com/repos/{REPO}/pulls?state=closed"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch closed PRs. Status code: {response.status_code}")
        return []

    try:
        return response.json()
    except ValueError:
        print("Error: The response is not valid JSON.")
        return []

# Function to calculate PR success rate
def calculate_pr_success_rate(pull_requests):
    merged_count = 0
    total_closed_count = len(pull_requests)

    for pr in pull_requests:
        if pr.get('merged_at'):  # Check if the PR was merged
            merged_count += 1

    if total_closed_count == 0:
        return 0.0

    success_rate = (merged_count / total_closed_count) * 100
    return round(success_rate, 2), merged_count, total_closed_count

# Get the list of closed PRs
closed_pull_requests = get_closed_pull_requests()

# Calculate PR success rate
success_rate, merged_count, total_closed_count = calculate_pr_success_rate(closed_pull_requests)

# Display the results
print(f"PR Success Rate: {success_rate}%")
print(f"Total Closed PRs: {total_closed_count}")
print(f"Merged PRs: {merged_count}")