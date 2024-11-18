import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar el endpoint de la API y las credenciales
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

st.title("Aplicación de Chat con x.ai y grok-vision-beta")

# Subir documentos
uploaded_file = st.file_uploader("Sube un documento", type=["txt", "pdf", "docx"])
if uploaded_file:
    st.write("Documento subido:", uploaded_file.name)

# Chat y Preguntas
prompt = st.text_input("Escribe tu pregunta o mensaje:")
if st.button("Enviar"):
    response = requests.post(API_URL, headers={"Authorization": f"Bearer {API_KEY}"}, json={"prompt": prompt})
    if response.status_code == 200:
        st.write("Respuesta:", response.json().get("answer", "Error en la respuesta"))
    else:
        st.write("Error en la llamada a la API")

# Generación de Imágenes
if st.button("Generar Imagen"):
    image_response = requests.post(API_URL, headers={"Authorization": f"Bearer {API_KEY}"}, json={"task": "generate_image", "description": prompt})
    if image_response.status_code == 200:
        image_url = image_response.json().get("image_url")
        st.image(image_url, caption="Imagen Generada")
    else:
        st.write("Error en la generación de la imagen")
