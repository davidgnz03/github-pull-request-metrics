import requests
import datetime
from dateutil.relativedelta import relativedelta

# Variables you can adjust
token = "your_token"  # Replace with your SonarQube token
project_name = "your_project_name"  # Project name or key in SonarQube
branch = "main"  # Branch name you want to analyze
time_range = 12  # Number of weeks
url_sonar = "https://your-sonarqube-url"  # Your SonarQube server URL

# Function to calculate the date range (last n weeks)
def get_date_range(weeks):
    today = datetime.date.today()
    start_date = today - relativedelta(weeks=weeks)
    return start_date, today

# Get the metrics from SonarQube
def get_sonar_metrics(token, project_name, branch, start_date, end_date):
    # Define the metrics to retrieve
    metrics = [
        "coverage",                   # Code Coverage %
        "vulnerabilities",            # Security (Known Vulnerabilities, count)
        "duplicated_lines_density",   # Code Duplication
        "sqale_index",                # Technical Debt
        "line_coverage",              # Unit Test Coverage
        "reliability_rating",         # Code Quality (Reliability)
        "security_rating",            # Code Quality (Security)
        "sqale_rating"                # Code Quality (Maintainability)
    ]
    
    # API endpoint
    api_url = f"{url_sonar}/api/measures/search_history"
    
    # API parameters, including branch
    params = {
        "component": project_name,
        "metrics": ",".join(metrics),
        "branch": branch,  # Specify the branch
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d")
    }
    
    # Authentication with token
    auth = (token, "")
    
    # Make the request
    response = requests.get(api_url, params=params, auth=auth)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Function to display metrics and calculate averages
def display_metrics(data):
    if data and 'measures' in data:
        for measure in data['measures']:
            metric = measure['metric']
            history = measure['history']
            values = []
            print(f"\nMetric: {metric}")
            for entry in history:
                value = entry.get('value', 'N/A')
                print(f"Date: {entry['date']}, Value: {value}")
                if value != 'N/A':
                    values.append(float(value))
            
            # Calculate the average of the metric if values are available
            if values:
                avg_value = sum(values) / len(values)
                print(f"Average for {metric}: {avg_value:.2f}")
            else:
                print(f"No values to calculate an average for {metric}.")
    else:
        print("No metrics found within the specified time range.")

# Get the date range based on weeks
start_date, end_date = get_date_range(time_range)

# Get the metrics for the specified branch
metrics_data = get_sonar_metrics(token, project_name, branch, start_date, end_date)

# Display the results and averages
display_metrics(metrics_data)
