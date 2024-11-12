import os
import streamlit as st
from transformers import pipeline
from dotenv import load_dotenv

# Carga el archivo .env si estás ejecutando localmente (para cualquier otra configuración adicional que necesites)
load_dotenv(".env")

# Configura el pipeline de transformers para usar GPT-2 localmente
generator = pipeline("text-generation", model="meta-llama/Llama-3.2-1B")

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

    # Genera la respuesta usando el pipeline de transformers
    response = generator(prompt, max_length=100, num_return_sequences=1)
    response_text = response[0]["generated_text"]

    # Muestra la respuesta en el chat y la almacena en el estado de sesión
    with st.chat_message("assistant"):
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
