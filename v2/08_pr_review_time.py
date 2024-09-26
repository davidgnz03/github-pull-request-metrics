from datetime import datetime, timedelta
import requests
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

# Function to calculate PR Review Time
def calculate_pr_review_time(created_at, closed_at):
    created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    closed_at_dt = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
    
    review_time = closed_at_dt - created_at_dt
    return review_time.total_seconds() / 3600  # Return time in hours

# Calculate PR Review Time for all PRs
def calculate_average_review_time():
    pull_requests = get_all_pull_requests()

    # Filter PRs by the time range (last N weeks)
    filtered_pull_requests = filter_prs_by_time(pull_requests, TIME_RANGE_IN_WEEKS)

    total_review_time = 0
    prs_with_review_time = 0
    pr_data = []

    for pr in filtered_pull_requests:
        pr_number = pr.get('number')
        created_at = pr.get('created_at')
        closed_at = pr.get('closed_at')  # PR must be closed to calculate review time

        if created_at and closed_at:
            review_time = calculate_pr_review_time(created_at, closed_at)
            total_review_time += review_time
            prs_with_review_time += 1

        # Append data for CSV
        pr_data.append([pr_number, review_time if created_at and closed_at else "No Review Time"])

    if prs_with_review_time == 0:
        return 0.0, pr_data

    average_review_time = total_review_time / prs_with_review_time
    return round(average_review_time, 2), pr_data

# Run the script to calculate average PR Review Time
average_review_time, pr_data = calculate_average_review_time()
print(f"Average PR Review Time: {average_review_time} hours")

# Add the average review time column to each PR data row
for pr in pr_data:
    pr.append(average_review_time)

# Extract the repository name from the REPO variable
repo_name = REPO.split("/")[1]  # Split 'owner/repo' and take the second part (repo)

# Save the results in a CSV file named with the repo name
csv_filename = f"{repo_name}_review_time.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PR Number", "Review Time (Hours)", "Average Review Time (Hours)"])  # Write header
    writer.writerows(pr_data)  # Write data rows
    writer.writerow(["", "", f"Average Review Time: {average_review_time} hours"])  # Append total row

print(f"Results saved to {csv_filename}")
