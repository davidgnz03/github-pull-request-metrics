import requests
from tabulate import tabulate
from datetime import datetime

# GitHub repository and personal token
GITHUB_TOKEN = "YOUR_PERSONAL_ACCESS_TOKEN"  # Replace with your personal access token
REPO = "owner/repo"  # Replace with the repository in the format "owner/repo"

# Headers for authentication with GitHub API
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# Function to get the list of pull requests (open and closed)
def get_pull_requests():
    url = f"https://api.github.com/repos/{REPO}/pulls?state=all"
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Failed to fetch PRs. Status code: {response.status_code}")
        return []

    try:
        return response.json()
    except ValueError:
        print("Error: The response is not valid JSON.")
        return []

# Function to calculate the PR request cycle time in hours
def calculate_pr_cycle_time(created_at, closed_at):
    created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    closed_at_dt = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
    
    cycle_time = closed_at_dt - created_at_dt
    # Return the total time in hours
    return cycle_time.total_seconds() / 3600

# Get the list of PRs (open and closed)
pull_requests = get_pull_requests()

# List to store PR information
pr_data = []

# Process each PR and calculate the cycle time in hours
for pr in pull_requests:
    pr_number = pr.get('number')
    pr_title = pr.get('title')
    created_at = pr.get('created_at')
    closed_at = pr.get('closed_at')  # This will be None if the PR is still open

    # Only calculate cycle time for closed PRs
    if closed_at:
        pr_cycle_time_hours = calculate_pr_cycle_time(created_at, closed_at)
        pr_data.append([pr_number, pr_title, round(pr_cycle_time_hours, 2)])  # Round to 2 decimal places

# Display the results in a table
print(tabulate(pr_data, headers=["PR Number", "Title", "Cycle Time (Hours)"], tablefmt="pretty"))
