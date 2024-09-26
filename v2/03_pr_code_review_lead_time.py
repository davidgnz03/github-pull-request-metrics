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

# Get the list of PRs
pull_requests = get_pull_requests()

# Filter PRs by the time range (last N weeks)
filtered_pull_requests = filter_prs_by_time(pull_requests, TIME_RANGE_IN_WEEKS)

# List to store PR information
pr_data = []

# Process each PR and calculate the code review lead time
for pr in filtered_pull_requests:
    pr_number = pr.get('number')
    pr_title = pr.get('title')
    created_at = pr.get('created_at')
    closed_at = pr.get('closed_at')  # This will be None if the PR is still open

    # Try to get the first review time
    first_event_at = get_first_review_time(pr_number)

    # If no reviews, try to get the first comment time
    if not first_event_at:
        first_event_at = get_first_comment_time(pr_number)

    # If there was an event (either review or comment), calculate the lead time
    if first_event_at:
        lead_time_hours = calculate_lead_time(created_at, first_event_at)
        pr_data.append([pr_number, pr_title, created_at, closed_at or "Open", f"{round(lead_time_hours, 2)} hours"])
    else:
        # No reviews or comments found
        pr_data.append([pr_number, pr_title, created_at, closed_at or "Open", "No reviews or comments"])

# Extract the repository name from the REPO variable
repo_name = REPO.split("/")[1]  # Split 'owner/repo' and take the second part (repo)

# Save the results in a CSV file named with the repo name
csv_filename = f"{repo_name}_pull_requests_lead_time.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PR Number", "Title", "Created At", "Closed At", "Lead Time (Hours)"])  # Write header
    writer.writerows(pr_data)  # Write data rows

# Display the results in a table
if pr_data:
    print(tabulate(pr_data, headers=["PR Number", "Title", "Created At", "Closed At", "Lead Time (Hours)"], tablefmt="pretty"))
else:
    print("No PRs with reviews or comments found.")

print(f"Results saved to {csv_filename}")