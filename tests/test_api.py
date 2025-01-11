import requests

def test_api_healthcheck():
    response = requests.get("http://0.0.0.0:8000/")
    assert response.status_code == 200
    assert response.text == 'Welcome to the API'

def test_prediction_endpoint():
    client_id = 192535  # Replace with a valid client_id from your test dataset
    response = requests.get(f"http://0.0.0.0:8000/prediction/{client_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert "probability" in response_data
    assert "prediction" in response_data
    assert isinstance(response_data["probability"], float)
    assert isinstance(response_data["prediction"], int)

def test_check_client_id():
    client_id = 192535  # Replace with a valid client_id from your test dataset
    response = requests.get(f"http://0.0.0.0:8000/{client_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data in [True, False]  # The response should be either True or False
