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
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch PRs. Status code: {response.status_code}")
        return []

    try:
        return response.json()
    except ValueError:
        print("Error: The response is not valid JSON.")
        return []

# Function to get the first review time on a PR
def get_first_review_time(pr_number):
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/reviews"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Failed to fetch reviews for PR {pr_number}. Status code: {response.status_code}")
        return None

    reviews = response.json()
    
    if not reviews:
        return None

    # Return the date of the first review
    return reviews[0].get('submitted_at')

# Function to get the first comment time on a PR (if no review)
def get_first_comment_time(pr_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{pr_number}/comments"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Failed to fetch comments for PR {pr_number}. Status code: {response.status_code}")
        return None

    comments = response.json()
    
    if not comments:
        return None

    # Return the date of the first comment
    return comments[0].get('created_at')

# Function to calculate the lead time between creation and the first review/comment
def calculate_lead_time(created_at, first_event_at):
    created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    first_event_dt = datetime.strptime(first_event_at, "%Y-%m-%dT%H:%M:%SZ")
    
    lead_time = first_event_dt - created_at_dt
    return lead_time.total_seconds() / 3600  # Return time in hours

# Get the list of PRs
pull_requests = get_pull_requests()

# List to store PR information
pr_data = []

# Process each PR and calculate the code review lead time
for pr in pull_requests:
    pr_number = pr.get('number')
    pr_title = pr.get('title')
    created_at = pr.get('created_at')

    # Try to get the first review time
    first_event_at = get_first_review_time(pr_number)

    # If no reviews, try to get the first comment time
    if not first_event_at:
        first_event_at = get_first_comment_time(pr_number)

    # If there was an event (either review or comment), calculate the lead time
    if first_event_at:
        lead_time_hours = calculate_lead_time(created_at, first_event_at)
        pr_data.append([pr_number, pr_title, f"{round(lead_time_hours, 2)} hours"])
    else:
        # No reviews or comments found
        pr_data.append([pr_number, pr_title, "No reviews or comments"])

# Display the results in a table
if pr_data:
    print(tabulate(pr_data, headers=["PR Number", "Title", "Lead Time (Hours)"], tablefmt="pretty"))
else:
    print("No PRs with reviews or comments found.")


