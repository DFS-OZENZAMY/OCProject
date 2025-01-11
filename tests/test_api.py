import requests

def test_api_healthcheck():
    response = requests.get("https://ocproject.onrender.com/")
    assert response.status_code == 200
    assert 'Bienvenue a API' == 'Bienvenue a API'


def test_prediction_endpoint():
    client_id = 192535  # Replace with a valid client_id from your test dataset
    response = requests.get(f"https://ocproject.onrender.com/prediction/{client_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert "probability" in response_data
    assert "prediction" in response_data
    assert isinstance(response_data["probability"], float)
    assert isinstance(response_data["prediction"], int)



def test_check_client_id():
    client_id = 192535  # Replace with a valid client_id from your test dataset
    response = requests.get(f"https://ocproject.onrender.com/{client_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data in [True, False]  # The response should be either True or False


    