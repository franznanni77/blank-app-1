import streamlit as st
from openai import OpenAI
import os

# Configurazione della pagina
st.set_page_config(page_title="Chat con OpenAI", page_icon="💬")

# Titolo dell'applicazione
st.title("Chat con OpenAI 🤖")

# Input per la API key (da inserire in modo sicuro)
if "openai_api_key" not in st.session_state:
    api_key = st.text_input("Inserisci la tua OpenAI API key:", type="password")
    if api_key:
        st.session_state.openai_api_key = api_key
        st.session_state.client = OpenAI(api_key=api_key)

# Area per la domanda dell'utente
user_question = st.text_area("Inserisci la tua domanda:", height=100)

# Funzione per ottenere la risposta da OpenAI
def get_openai_response(question):
    try:
        response = st.session_state.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Si è verificato un errore: {str(e)}"

# Bottone per inviare la domanda
if st.button("Invia domanda") and user_question:
    if "openai_api_key" not in st.session_state:
        st.error("Per favore, inserisci prima la tua API key di OpenAI")
    else:
        with st.spinner("Sto elaborando la risposta..."):
            response = get_openai_response(user_question)
            st.write("### Risposta:")
            st.write(response)