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

# Function to get the list of pull requests (only closed PRs)
def get_closed_pull_requests():
    url = f"https://api.github.com/repos/{REPO}/pulls?state=closed"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch closed PRs. Status code: {response.status_code}")
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

# Function to calculate PR success rate
def calculate_pr_success_rate(pull_requests):
    merged_count = 0
    total_closed_count = len(pull_requests)

    for pr in pull_requests:
        if pr.get('merged_at'):  # Check if the PR was merged
            merged_count += 1

    if total_closed_count == 0:
        return 0.0, merged_count, total_closed_count

    success_rate = (merged_count / total_closed_count) * 100
    return round(success_rate, 2), merged_count, total_closed_count

# Get the list of closed PRs
closed_pull_requests = get_closed_pull_requests()

# Filter PRs by the time range (last N weeks)
filtered_pull_requests = filter_prs_by_time(closed_pull_requests, TIME_RANGE_IN_WEEKS)

# Calculate PR success rate
success_rate, merged_count, total_closed_count = calculate_pr_success_rate(filtered_pull_requests)

# List to store PR information
pr_data = []

# Process each PR and gather necessary data
for pr in filtered_pull_requests:
    pr_number = pr.get('number')
    pr_title = pr.get('title')
    created_at = pr.get('created_at')
    closed_at = pr.get('closed_at') or "Still Open"
    merged_at = pr.get('merged_at')

    # Check if the PR was merged or just closed without merging
    status = "Merged" if merged_at else "Closed without merging"

    pr_data.append([pr_number, pr_title, created_at, closed_at, status])

# Extract the repository name from the REPO variable
repo_name = REPO.split("/")[1]  # Split 'owner/repo' and take the second part (repo)

# Save the results in a CSV file named with the repo name
csv_filename = f"{repo_name}_closed_pull_requests.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PR Number", "Title", "Created At", "Closed At", "Status"])  # Write header
    writer.writerows(pr_data)  # Write data rows

# Display the results in a table
if pr_data:
    print(tabulate(pr_data, headers=["PR Number", "Title", "Created At", "Closed At", "Status"], tablefmt="pretty"))
else:
    print("No PRs found in the specified time range.")

# Display the overall success rate
print(f"\nPR Success Rate: {success_rate}%")
print(f"Total Closed PRs: {total_closed_count}")
print(f"Merged PRs: {merged_count}")
print(f"Results saved to {csv_filename}")