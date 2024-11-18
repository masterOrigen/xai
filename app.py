import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

API_URL = "https://api.x.ai/v1/chat/completions"
API_KEY = os.getenv("XAI_API_KEY")  # Asegúrate que tu .env tiene XAI_API_KEY

st.title("Aplicación de Chat con x.ai y Grok")

# Obtener mensaje del usuario
prompt = st.text_input("Escribe tu pregunta o mensaje:")
if st.button("Enviar"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
            {"role": "user", "content": prompt}
        ],
        "model": "grok-vision-beta",
        "stream": False,
        "temperature": 0
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta")
        st.write("Respuesta:", answer)
    else:
        st.write("Error en la llamada a la API")

# Otras características - subir documentos, generar imágenes, etc.
