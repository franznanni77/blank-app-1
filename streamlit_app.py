import os
import openai

def main():
    # Legge la chiave API da variabile d'ambiente
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    # Esempio di chiamata al modello
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Salve, vorrei una ricetta per la pasta alla carbonara."}
        ],
        temperature=0.5
    )

    # Stampa la risposta
    assistant_reply = response.choices[0].message["content"]
    print("Risposta dal modello:\n", assistant_reply)

if __name__ == "__main__":
    main()
