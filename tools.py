import requests

def get_logs(service_name: str):
    response = requests.get(
        f"http://localhost:5124/api/logs/service/{service_name}"
    )
    return response.json()