import requests
import datetime
from dateutil.relativedelta import relativedelta

# Variables que puedes ajustar
token = "tu_token"  # Reemplaza con tu token de SonarQube
project_name = "tu_project_name"  # Nombre o key del proyecto en SonarQube
time_range = 12  # Cantidad de semanas
url_sonar = "https://tu-sonarqube-url"  # URL de tu servidor SonarQube

# Función para calcular las fechas (últimos n semanas)
def get_date_range(weeks):
    today = datetime.date.today()
    start_date = today - relativedelta(weeks=weeks)
    return start_date, today

# Obtener las métricas
def get_sonar_metrics(token, project_name, start_date, end_date):
    # Definir las métricas que quieres obtener
    metrics = [
        "coverage",                   # Code Coverage %
        "vulnerabilities",            # Security (Known Vulnerabilities, count)
        "duplicated_lines_density",   # Code Duplication
        "sqale_index",                # Technical Debt
        "line_coverage",              # Unit Test Coverage
        "reliability_rating",         # Code Quality (Reliability)
        "security_rating",            # Code Quality (Security)
        "maintainability_rating"      # Code Quality (Maintainability)
    ]
    
    # Endpoint de la API
    api_url = f"{url_sonar}/api/measures/search_history"
    
    # Parámetros de la API
    params = {
        "component": project_name,
        "metrics": ",".join(metrics),
        "from": start_date.strftime("%Y-%m-%d"),
        "to": end_date.strftime("%Y-%m-%d")
    }
    
    # Autenticación con token
    auth = (token, "")
    
    # Hacer la solicitud
    response = requests.get(api_url, params=params, auth=auth)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Función para mostrar los resultados de las métricas
def display_metrics(data):
    if data and 'measures' in data:
        for measure in data['measures']:
            metric = measure['metric']
            history = measure['history']
            print(f"\nMétrica: {metric}")
            for entry in history:
                print(f"Fecha: {entry['date']}, Valor: {entry.get('value', 'N/A')}")
    else:
        print("No se encontraron métricas en el rango de tiempo especificado.")

# Obtener el rango de fechas basado en las semanas
start_date, end_date = get_date_range(time_range)

# Obtener las métricas
metrics_data = get_sonar_metrics(token, project_name, start_date, end_date)

# Mostrar los resultados
display_metrics(metrics_data)
