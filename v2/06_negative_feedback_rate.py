import requests
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
def get_all_pull_requests():
    url = f"https://api.github.com/repos/{REPO}/pulls?state=all"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch PRs. Status code: {response.status_code}")
        return []

    return response.json()

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

    # Filter PRs by time range (last N weeks)
    filtered_pull_requests = filter_prs_by_time(pull_requests, TIME_RANGE_IN_WEEKS)

    total_prs = len(filtered_pull_requests)
    prs_with_changes_requested = 0
    pr_data = []

    for pr in filtered_pull_requests:
        pr_number = pr['number']
        changes_requested_count = get_feedback_for_pr(pr_number)
        if changes_requested_count > 0:
            prs_with_changes_requested += 1
        
        # Append data for CSV
        pr_data.append([pr_number, changes_requested_count])

    if total_prs == 0:
        return 0.0, pr_data

    negative_feedback_rate = (prs_with_changes_requested / total_prs) * 100
    return round(negative_feedback_rate, 2), pr_data, total_prs

# Run the script to calculate Negative Feedback Rate
negative_feedback_rate, pr_data, total_prs = calculate_negative_feedback_rate()
print(f"Negative Feedback Rate: {negative_feedback_rate}%")

# Add the percentage column to each PR data row
for pr in pr_data:
    pr.append(negative_feedback_rate)

# Extract the repository name from the REPO variable
repo_name = REPO.split("/")[1]  # Split 'owner/repo' and take the second part (repo)

# Save the results in a CSV file named with the repo name
csv_filename = f"{repo_name}_negative_feedback_rate.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PR Number", "Changes Requested Count", "Negative Feedback Rate (%)"])  # Write header
    writer.writerows(pr_data)  # Write data rows
    writer.writerow(["", "", f"Total Negative Feedback Rate: {negative_feedback_rate}%"])  # Append total row

print(f"Results saved to {csv_filename}")