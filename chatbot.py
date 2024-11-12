import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Cargar el token de Hugging Face desde .env
load_dotenv()
api_token = os.getenv("HUGGINGFACE_API_TOKEN")

# Configuración de la app de Streamlit
st.title("💬 Chatbot con API de Hugging Face")
st.write("Escribe un mensaje y el chatbot te responderá utilizando la API de Hugging Face.")

# Configura el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Eres un asistente de IA."}]

# Muestra los mensajes de chat existentes a través de `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if user_input := st.chat_input("¿Qué hay de nuevo?"):
    # Agrega el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
    st.markdown(user_input)

    # Llamada a la API de Hugging Face
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    data = {
        "inputs": {
            "past_user_inputs": [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"],
            "generated_responses": [msg["content"] for msg in st.session_state.messages if msg["role"] == "assistant"],
            "text": user_input
        }
    }
    response = requests.post("https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill", 
                             headers=headers, json=data)
    response_data = response.json()

    # Extrae la respuesta y agrégala al historial
    bot_response = response_data.get("generated_text", "Lo siento, no pude procesar la respuesta.")
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Muestra el historial de chat
#for message in st.session_state.messages:
#    if message["role"] == "user":
#        st.write(f"**Usuario:** {message['content']}")
#    else:
#        st.write(f"**Asistente:** {message['content']}")
