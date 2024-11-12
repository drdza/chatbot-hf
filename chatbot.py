import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


# Detecta si estamos en Streamlit Cloud o localmente
env = os.getenv("GCP_ENV", "local")  # Default a "local" si no está definido

if env == "prod":
    #Carga de variables de entorno en deployments en la nube
    api_key= os.getenv("GCP_APY_KEY") 
    base_url= os.getenv("GCP_BASE_URL")
else:
    #Carga las variables del archivo .env en deployments locales
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "Este es un cliente ligero de chat con IA."
)

# Create an OpenAI client.
client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Eres un asistente de IA que responde con un tono energetico, muy feliz y nada puede hacerte sentir mal, tambien eres un poco sarcastico en preguntas que quizá podrían resultarte obvias. Diviertete con el usuario"}]

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("¿Qué hay de nuevo?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct-v0.3",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
