import requests


def get_slow_requests():
    response = requests.get("http://localhost:5124/api/logs/slow")
    return response.json()

def get_logs(service_name: str):
    response = requests.get(
        f"http://localhost:5124/api/logs/service/{service_name}"
    )
    if response.status_code != 200:
        return []
    return response.json()