import requests
from tabulate import tabulate

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
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch PRs. Status code: {response.status_code}")
        return []

    try:
        return response.json()
    except ValueError:
        print("Error: The response is not valid JSON.")
        return []

# Function to get the count of comments on a PR
def get_pr_comment_count(pr_number):
    # General comments on the PR
    url_comments = f"https://api.github.com/repos/{REPO}/issues/{pr_number}/comments"
    response_comments = requests.get(url_comments, headers=headers)
    if response_comments.status_code != 200:
        print(f"Error: Failed to fetch comments for PR {pr_number}. Status code: {response_comments.status_code}")
        return 0

    # Review comments on the PR
    url_review_comments = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/comments"
    response_review_comments = requests.get(url_review_comments, headers=headers)
    if response_review_comments.status_code != 200:
        print(f"Error: Failed to fetch review comments for PR {pr_number}. Status code: {response_review_comments.status_code}")
        return 0

    general_comments = response_comments.json()
    review_comments = response_review_comments.json()

    # Return the total number of general and review comments
    return len(general_comments) + len(review_comments)

# Get the list of PRs (open and closed)
pull_requests = get_pull_requests()

# List to store PR information
pr_data = []

# Process each PR and calculate the comment count
for pr in pull_requests:
    pr_number = pr.get('number')
    pr_title = pr.get('title')

    # Get the total comment count for the PR
    comment_count = get_pr_comment_count(pr_number)

    pr_data.append([pr_number, pr_title, comment_count])

# Display the results in a table
if pr_data:
    print(tabulate(pr_data, headers=["PR Number", "Title", "Comment Count"], tablefmt="pretty"))
else:
    print("No PRs found.")
