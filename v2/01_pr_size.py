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

# Function to filter PRs by time range
def filter_prs_by_time(pull_requests, time_range_in_weeks):
    cutoff_date = datetime.now() - timedelta(weeks=time_range_in_weeks)
    filtered_prs = []

    for pr in pull_requests:
        created_at = pr.get('created_at')  # The created date of the PR
        created_at_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
        
        # Include only PRs created or updated in the last N weeks
        if created_at_date >= cutoff_date:
            filtered_prs.append(pr)

    return filtered_prs

# Get the list of open PRs
pull_requests = get_open_pull_requests()

# Filter PRs by the time range (last N weeks)
filtered_pull_requests = filter_prs_by_time(pull_requests, TIME_RANGE_IN_WEEKS)

# List to store PR information
pr_data = []

# Process each PR and calculate its size
for pr in filtered_pull_requests:
    pr_number = pr.get('number')  # Safely access 'number' using .get()
    pr_title = pr.get('title')    # Safely access 'title' using .get()
    pr_created_at = pr.get('created_at')  # Get the creation date

    # Get the size of the PR
    pr_size = get_pr_size(pr_number)

    pr_data.append([pr_number, pr_title, pr_size, pr_created_at])

# Extract the repository name from the REPO variable
repo_name = REPO.split("/")[1]  # Split 'owner/repo' and take the second part (repo)

# Save the results in a CSV file named with the repo name
csv_filename = f"{repo_name}_pull_requests_metrics.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PR Number", "Title", "Size (LOC)", "Created At"])  # Write header
    writer.writerows(pr_data)  # Write data rows

# Display the results in a table (optional)
print(tabulate(pr_data, headers=["PR Number", "Title", "Size (LOC)", "Created At"], tablefmt="pretty"))

print(f"Results saved to {csv_filename}")
