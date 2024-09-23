from datetime import datetime
import requests

# GitHub repository and personal token
GITHUB_TOKEN = "YOUR_PERSONAL_ACCESS_TOKEN"  # Replace with your personal access token
REPO = "owner/repo"  # Replace with the repository in the format "owner/repo"

# Headers for authentication with GitHub API
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# Function to get the list of pull requests (open and closed)
def get_all_pull_requests():
    url = f"https://api.github.com/repos/{REPO}/pulls?state=all"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch PRs. Status code: {response.status_code}")
        return []

    return response.json()

# Function to calculate PR Review Time
def calculate_pr_review_time(created_at, closed_at):
    created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    closed_at_dt = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
    
    review_time = closed_at_dt - created_at_dt
    return review_time.total_seconds() / 3600  # Return time in hours

# Calculate PR Review Time for all PRs
def calculate_average_review_time():
    pull_requests = get_all_pull_requests()

    total_review_time = 0
    prs_with_review_time = 0

    for pr in pull_requests:
        created_at = pr.get('created_at')
        closed_at = pr.get('closed_at')  # PR must be closed to calculate review time

        if created_at and closed_at:
            review_time = calculate_pr_review_time(created_at, closed_at)
            total_review_time += review_time
            prs_with_review_time += 1

    if prs_with_review_time == 0:
        return 0.0

    average_review_time = total_review_time / prs_with_review_time
    return round(average_review_time, 2)

# Run the script to calculate average PR Review Time
average_review_time = calculate_average_review_time()
print(f"Average PR Review Time: {average_review_time} hours")
