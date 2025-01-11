import requests

def test_api_healthcheck():
    response = requests.get("http://127.0.0.1:8000/")
    assert response.status_code == 200
    assert response.json() == 'Welcome to the API'
