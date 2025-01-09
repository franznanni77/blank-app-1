import streamlit as st
from openai import OpenAI
import os

# Configurazione della pagina
st.set_page_config(page_title="Chat con OpenAI", page_icon="💬")

# Titolo dell'applicazione
st.title("Chat con OpenAI 🤖")

# Inizializzazione del client OpenAI usando la chiave dall'ambiente
client = OpenAI() # Automaticamente legge OPENAI_API_KEY dall'ambiente

# Area per la domanda dell'utente
user_question = st.text_area("Inserisci la tua domanda:", height=100)

# Funzione per ottenere la risposta da OpenAI
def get_openai_response(question):
    try:
        response = client.chat.completions.create(
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
    with st.spinner("Sto elaborando la risposta..."):
        response = get_openai_response(user_question)
        st.write("### Risposta:")
        st.write(response)