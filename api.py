from fastapi import FastAPI
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import uvicorn
import logging
import lightgbm as lgb
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a FastAPI instance
app = FastAPI()

# Load the model, scaler, feature names, and best threshold
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)
with open('feature_names.pkl', 'rb') as feature_file:
    feature_names = pickle.load(feature_file)

# Définir le seuil optimal manuellement à 0.42
best_threshold = 0.42

# Load the test data
data_test = pd.read_csv('test_df_sample.csv')

# Ensure 'SK_ID_CURR' is present in test data
if 'SK_ID_CURR' not in data_test.columns:
    raise KeyError("'SK_ID_CURR' column is missing in the test data.")

# Align test data columns to match feature names
aligned_columns = ['SK_ID_CURR'] + feature_names
data_test = data_test.reindex(columns=aligned_columns, fill_value=0)

# Scale the test data
data_test_scaled = data_test.copy()
data_test_scaled[feature_names] = scaler.transform(data_test[feature_names])

# Log scaler and feature names to ensure they are correctly initialized
logging.info(f"Scaler type: {type(scaler)}")
logging.info(f"Feature names: {feature_names}")

# Functions
@app.get('/')
def welcome():
    """
    Welcome message.
    :param: None
    :return: Message (string).
    """
    return 'Bienvenue a API'

@app.get('/{client_id}')
def check_client_id(client_id: int):
    """
    Customer search in the database.
    :param: client_id (int)
    :return: message (string).
    """
    if client_id in list(data_test['SK_ID_CURR']):
        return True
    else:
        return False

@app.get('/threshold')
def get_threshold():
    """
    Returns the optimal threshold.
    :param: None
    :return: optimal threshold (float).
    """
    return {"best_threshold": best_threshold}

@app.get('/prediction/{client_id}')
def get_prediction(client_id: int):
    """
    Calculates the probability of default for a client.
    :param: client_id (int)
    :return: probability of default (float).
    """
    client_data = data_test_scaled[data_test['SK_ID_CURR'] == client_id]
    if client_data.empty:
        return {"error": "Client ID not found"}, 404

    info_client = client_data.drop('SK_ID_CURR', axis=1)
    logging.info(f"info_client type: {type(info_client)}")
    
    try:
        # Transform the data using the scaler
        info_client_scaled = scaler.transform(info_client)
        logging.info(f"info_client_scaled type: {type(info_client_scaled)}")

        probability = model.predict(info_client_scaled)[0]
        prediction = int(probability >= best_threshold)
        logging.info(f"Prediction for client_id {client_id}: {prediction} (probability: {probability})")
        
        result = {
            "probability": probability,
            "prediction": prediction
        }

        return result
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return {"error": "Error during prediction"}, 500

if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=8000, reload=True)
