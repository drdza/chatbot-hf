import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Carga el archivo .env si estás ejecutando localmente
#load_dotenv(".env")
api_key = os.getenv("HUGGINGFACE_API_TOKEN")

# Show title and description
st.title("💬 Chatbot")
st.write("Este es un cliente ligero de chat con IA usando Hugging Face GPT-2.")

# Crea una variable de estado de sesión para almacenar los mensajes del chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Eres un asistente de IA."}]

# Muestra los mensajes existentes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada del chat
if prompt := st.chat_input("¿Qué hay de nuevo?"):

    # Guarda y muestra el mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamada a la API de Hugging Face para generar una respuesta
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "inputs": prompt,
    }
    response = requests.post(
        "https://api-inference.huggingface.co/models/openai-community/gpt2",
        headers=headers,
        json=data
    )

    # Procesa la respuesta
    response_text = response.json().get("generated_text", "Lo siento, no pude procesar la respuesta.")
    
    # Muestra la respuesta en el chat y la almacena en el estado de sesión
    with st.chat_message("assistant"):
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
