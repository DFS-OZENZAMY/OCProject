import streamlit as st
import requests

# Définir l'URL de base de l'API
base_url = "https://ocproject.onrender.com"

st.title("Prédiction de Prêt")

# Input du client_id
client_id = st.number_input("Entrez l'ID du client :", min_value=0)

if st.button("Vérifier l'ID du client"):
    # Vérifier si le client existe
    response = requests.get(f"{base_url}/{client_id}")
    if response.status_code == 200:
        exists = response.json()
        if exists:
            st.write("L'ID du client existe dans la base de données.")
        else:
            st.write("L'ID du client n'existe pas dans la base de données.")
    else:
        st.write("Erreur dans la communication avec l'API.")

if st.button("Obtenir la Prédiction"):
    # Obtenir la prédiction pour le client
    response = requests.get(f"{base_url}/prediction/{client_id}")
    if response.status_code == 200:
        result = response.json()
        probability = result.get("probability", None)
        prediction = result.get("prediction", None)
        
        # Charger le seuil optimal
        response_threshold = requests.get(f"{base_url}/threshold")
        if response_threshold.status_code == 200:
            best_threshold = response_threshold.json().get("best_threshold", None)
        else:
            best_threshold = None

        if probability is not None and prediction is not None:
            st.write(f"La probabilité de défaut pour le client {client_id} est : {probability:.2f}")
            if best_threshold is not None:
                st.write(f"Le seuil optimal est : {best_threshold:.2f}")
            if prediction == 0:
                st.success("Le client peut obtenir un prêt.")
            else:
                st.warning("Le client a un risque élevé de défaut, le prêt peut être refusé.")
        else:
            st.write("Erreur dans l'obtention de la prédiction.")
    else:
        st.write("Erreur dans la communication avec l'API.")
