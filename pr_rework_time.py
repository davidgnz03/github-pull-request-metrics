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

# Function to get the review feedback and check when changes were requested
def get_pr_rework_time(pr_number):
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/reviews"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Failed to fetch reviews for PR {pr_number}. Status code: {response.status_code}")
        return None

    reviews = response.json()

    change_request_time = None
    next_commit_time = None

    for review in reviews:
        if review['state'] == 'CHANGES_REQUESTED':
            change_request_time = datetime.strptime(review['submitted_at'], "%Y-%m-%dT%H:%M:%SZ")
            break

    if change_request_time:
        # Get the commits after the changes were requested
        url_commits = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/commits"
        response_commits = requests.get(url_commits, headers=headers)
        if response_commits.status_code != 200:
            print(f"Error: Failed to fetch commits for PR {pr_number}. Status code: {response_commits.status_code}")
            return None

        commits = response_commits.json()

        for commit in commits:
            commit_time = datetime.strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
            if commit_time > change_request_time:
                next_commit_time = commit_time
                break

    if change_request_time and next_commit_time:
        return (next_commit_time - change_request_time).total_seconds() / 3600  # Return rework time in hours

    return None

# Calculate PR Rework Time for all PRs
def calculate_average_rework_time():
    pull_requests = get_all_pull_requests()

    total_rework_time = 0
    prs_with_rework = 0

    for pr in pull_requests:
        pr_number = pr['number']
        rework_time = get_pr_rework_time(pr_number)

        if rework_time:
            total_rework_time += rework_time
            prs_with_rework += 1

    if prs_with_rework == 0:
        return 0.0

    average_rework_time = total_rework_time / prs_with_rework
    return round(average_rework_time, 2)

# Run the script to calculate average PR Rework Time
average_rework_time = calculate_average_rework_time()
print(f"Average PR Rework Time: {average_rework_time} hours")
