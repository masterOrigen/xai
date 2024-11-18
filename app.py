import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

API_URL = "https://api.x.ai/v1/chat/completions"
API_KEY = os.getenv("XAI_API_KEY")

st.title("Aplicación de Chat con x.ai y Grok")

# Crear pestañas
tabs = st.tabs(["Chat", "Interactuar con Documentos", "Generar Imágenes"])

# Pestaña de Chat
with tabs[0]:
    st.header("Chat")
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

# Pestaña de Interacción con Documentos
with tabs[1]:
    st.header("Interactuar con Documentos")
    uploaded_file = st.file_uploader("Sube un documento", type=["txt", "pdf", "docx"])
    if uploaded_file:
        st.write(f"Documento cargado: {uploaded_file.name}")
        
        try:
            document_content = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            document_content = uploaded_file.read().decode('latin1')
        
        # Muestra un área de texto para interactuar con el contenido
        interaction_prompt = st.text_area("Escribe una pregunta sobre el documento:")
        if st.button("Enviar pregunta sobre el documento"):
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            data = {
                "messages": [
                    {"role": "system", "content": "You are Grok, an assistant analyzing a document."},
                    {"role": "user", "content": document_content},
                    {"role": "user", "content": interaction_prompt}
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
                st.write("Error al enviar la pregunta a la API")

# Pestaña de Generación de Imágenes
with tabs[2]:
    st.header("Generar Imágenes")
    image_prompt = st.text_input("Descripción para la imagen a generar:")
    if st.button("Crear Imagen"):
        if image_prompt:
            image_response = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"task": "generate_image", "description": image_prompt}
            )
            if image_response.status_code == 200:
                image_url = image_response.json().get("image_url")
                if image_url:
                    st.image(image_url, caption="Imagen Generada")
                else:
                    st.write("Error: no se pudo generar la imagen")
            else:
                st.write("Error en la llamada a la API para generar imagen")
