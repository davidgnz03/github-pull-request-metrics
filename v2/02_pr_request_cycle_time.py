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

# Get the list of PRs (open and closed)
pull_requests = get_pull_requests()

# Filter PRs by the time range (last N weeks)
filtered_pull_requests = filter_prs_by_time(pull_requests, TIME_RANGE_IN_WEEKS)

# List to store PR information
pr_data = []

# Process each PR and calculate the cycle time in hours
for pr in filtered_pull_requests:
    pr_number = pr.get('number')
    pr_title = pr.get('title')
    created_at = pr.get('created_at')
    closed_at = pr.get('closed_at')  # This will be None if the PR is still open

    # Only calculate cycle time for closed PRs
    if closed_at:
        pr_cycle_time_hours = calculate_pr_cycle_time(created_at, closed_at)
        pr_data.append([pr_number, pr_title, created_at, closed_at, round(pr_cycle_time_hours, 2)])  # Round to 2 decimal places

# Extract the repository name from the REPO variable
repo_name = REPO.split("/")[1]  # Split 'owner/repo' and take the second part (repo)

# Save the results in a CSV file named with the repo name
csv_filename = f"{repo_name}_pull_requests_cycle_time.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PR Number", "Title", "Created At", "Closed At", "Cycle Time (Hours)"])  # Write header
    writer.writerows(pr_data)  # Write data rows

# Display the results in a table
print(tabulate(pr_data, headers=["PR Number", "Title", "Created At", "Closed At", "Cycle Time (Hours)"], tablefmt="pretty"))

print(f"Results saved to {csv_filename}")