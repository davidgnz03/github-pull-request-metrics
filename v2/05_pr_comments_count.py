import requests
from tabulate import tabulate
from datetime import datetime, timedelta
import csv

# GitHub repository and personal token
GITHUB_TOKEN = "YOUR_PERSONAL_ACCESS_TOKEN"  # Replace with your personal access token
REPO = "owner/repo"  # Replace with the repository in the format "owner/repo"

# Number of weeks to consider for the metrics
TIME_RANGE_IN_WEEKS = 4  # Adjust this value to the desired time range

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

# Function to filter PRs by time range
def filter_prs_by_time(pull_requests, time_range_in_weeks):
    cutoff_date = datetime.now() - timedelta(weeks=time_range_in_weeks)
    filtered_prs = []

    for pr in pull_requests:
        created_at = pr.get('created_at')
        created_at_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
        
        # Include only PRs created in the last N weeks
        if created_at_date >= cutoff_date:
            filtered_prs.append(pr)

    return filtered_prs

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

# Filter PRs by the time range (last N weeks)
filtered_pull_requests = filter_prs_by_time(pull_requests, TIME_RANGE_IN_WEEKS)

# List to store PR information
pr_data = []

# Process each PR and calculate the comment count
for pr in filtered_pull_requests:
    pr_number = pr.get('number')
    pr_title = pr.get('title')

    # Get the total comment count for the PR
    comment_count = get_pr_comment_count(pr_number)

    pr_data.append([pr_number, pr_title, comment_count])

# Extract the repository name from the REPO variable
repo_name = REPO.split("/")[1]  # Split 'owner/repo' and take the second part (repo)

# Save the results in a CSV file named with the repo name
csv_filename = f"{repo_name}_pr_comment_counts.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PR Number", "Title", "Comment Count"])  # Write header
    writer.writerows(pr_data)  # Write data rows

# Display the results in a table
if pr_data:
    print(tabulate(pr_data, headers=["PR Number", "Title", "Comment Count"], tablefmt="pretty"))
else:
    print("No PRs found in the specified time range.")

print(f"Results saved to {csv_filename}")
