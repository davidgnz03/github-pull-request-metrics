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

# Function to get the review feedback (changes requested) for a PR
def get_feedback_for_pr(pr_number):
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/reviews"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Failed to fetch reviews for PR {pr_number}. Status code: {response.status_code}")
        return 0

    reviews = response.json()

    # Count the number of "changes requested" reviews
    changes_requested_count = sum(1 for review in reviews if review['state'] == 'CHANGES_REQUESTED')
    
    return changes_requested_count

# Calculate Negative Feedback Rate
def calculate_negative_feedback_rate():
    pull_requests = get_all_pull_requests()

    total_prs = len(pull_requests)
    prs_with_changes_requested = 0

    for pr in pull_requests:
        pr_number = pr['number']
        changes_requested_count = get_feedback_for_pr(pr_number)
        if changes_requested_count > 0:
            prs_with_changes_requested += 1

    if total_prs == 0:
        return 0.0
    
    negative_feedback_rate = (prs_with_changes_requested / total_prs) * 100
    return round(negative_feedback_rate, 2)

# Run the script to calculate Negative Feedback Rate
negative_feedback_rate = calculate_negative_feedback_rate()
print(f"Negative Feedback Rate: {negative_feedback_rate}%")
