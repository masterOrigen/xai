import streamlit as st
import requests
from dotenv import load_dotenv
import os
import PyPDF2

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

    # Inicializa el estado si no existe
    if "chat_prompt" not in st.session_state:
        st.session_state["chat_prompt"] = ""

    prompt = st.text_area("Escribe tu pregunta o mensaje:", value=st.session_state["chat_prompt"], key="chat_prompt_area")

    if st.button("Enviar", key="send_chat_button") and prompt.strip():
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
                st.session_state["chat_prompt"] = ""  # Limpiar el campo de texto
            else:
                st.write(f"Error en la llamada a la API: {response.status_code} - {response.text}")

# Pestaña de Chat con Documentos
with tabs[1]:

    # Inicializa el estado si no existe
    if "doc_prompt" not in st.session_state:
        st.session_state["doc_prompt"] = ""

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

            interaction_prompt = st.text_area("Escribe una pregunta sobre el documento:", value=st.session_state["doc_prompt"], key="doc_prompt_area")
            if st.button("Enviar pregunta sobre el documento", key="send_doc_button") and interaction_prompt.strip():
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
                        st.session_state["doc_prompt"] = ""  # Limpiar el campo de texto
                    else:
                        st.write(f"Error al enviar la pregunta a la API: {response.status_code} - {response.text}")
        else:
            st.write("El documento cargado está vacío o no se pudo leer correctamente.")
