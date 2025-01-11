import requests

def test_api_healthcheck():
    response = requests.get("https://ocproject.onrender.com/")
    assert response.status_code == 200
    assert response.json() == 'Bienvenue a API'
