import streamlit as st
import requests
from dotenv import load_dotenv
import os
import PyPDF2  # Asegúrate de tener instalada esta librería

# Cargar variables de entorno
load_dotenv()

API_URL = "https://api.x.ai/v1/chat/completions"
API_KEY = os.getenv("XAI_API_KEY")

def truncate_content(content, max_words=17500):
    words = content.split()
    return ' '.join(words[:max_words])

# Crear pestañas
tabs = st.tabs(["Chat", "Chat con Documentos"])

# Pestaña de Chat
with tabs[0]:
    st.header("Chat")
    chat_prompt = st.empty()
    prompt = chat_prompt.text_area("Escribe tu pregunta o mensaje:")
    if st.button("Enviar") and prompt.strip():
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
        with st.spinner("Estoy pensando..."):
            response = requests.post(API_URL, headers=headers, json=data)
            if response.status_code == 200:
                answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta")
                st.write("Respuesta:", answer)
                chat_prompt.text_area("Escribe tu pregunta o mensaje:", "")
            else:
                st.write(f"Error en la llamada a la API: {response.status_code} - {response.text}")
    elif not prompt.strip():
        st.write("Por favor, ingresa un mensaje válido.")

# Pestaña de Chat con Documentos
with tabs[1]:
    st.header("Chat con Documentos")
    uploaded_file = st.file_uploader("Sube un documento", type=["txt", "pdf", "docx"])
    if uploaded_file:
        st.write(f"Documento cargado: {uploaded_file.name}")
        
        document_content = ""
        # Procesar el archivo dependiendo de su tipo
        if uploaded_file.name.endswith(".txt"):
            try:
                document_content = uploaded_file.read().decode('utf-8').strip()
            except UnicodeDecodeError:
                document_content = uploaded_file.read().decode('latin1').strip()
        elif uploaded_file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                document_content += page.extract_text()
            document_content = document_content.strip()

        if document_content:
            # Truncar contenido si es demasiado largo
            truncated_content = truncate_content(document_content)

            doc_prompt = st.empty()
            interaction_prompt = doc_prompt.text_area("Escribe una pregunta sobre el documento:")
            if st.button("Enviar pregunta sobre el documento") and interaction_prompt.strip():
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                }
                data = {
                    "messages": [
                        {"role": "system", "content": "You are Grok, an assistant analyzing a document."},
                        {"role": "user", "content": truncated_content},
                        {"role": "user", "content": interaction_prompt}
                    ],
                    "model": "grok-beta",
                    "stream": False,
                    "temperature": 0
                }
                with st.spinner("Estoy pensando..."):
                    response = requests.post(API_URL, headers=headers, json=data)
                    if response.status_code == 200:
                        answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta")
                        st.write("Respuesta:", answer)
                        doc_prompt.text_area("Escribe una pregunta sobre el documento:", "")
                    else:
                        st.write(f"Error al enviar la pregunta a la API: {response.status_code} - {response.text}")
            elif not interaction_prompt.strip():
                st.write("Por favor, ingresa una pregunta válida.")
        else:
            st.write("El documento cargado está vacío o no se pudo leer correctamente.")
