import base64
import json
import openai
import os

# Assicurati di avere la tua API key impostata come variabile d'ambiente
# oppure assegnala direttamente qui (sconsigliato per motivi di sicurezza)
# openai.api_key = "la-tua-api-key"

def process_receipts(uploaded_files):
    """
    Questa funzione riceve una lista di file da Streamlit
    e invia ciascun file a OpenAI per l'estrazione dei dati.
    Restituisce un JSON con i risultati.
    """

    results = []

    for file_data in uploaded_files:
        # Legge il contenuto binario del file
        content = file_data.read()
        # Converte in base64
        base64_content = base64.b64encode(content).decode("utf-8")

        # Costruisce il messaggio da inviare a OpenAI
        messages = [
            {
                "role": "system",
                "content": (
                    "Agisci come un assistente amministrativo virtuale e analizza solo "
                    "le ricevute fiscali etichettate come 'documento gestionale di chiusura giornaliera'. "
                    "Estrai i dati rilevanti utilizzando la funzione 'estrazione_scontrino' e "
                    "restituiscili in un unico file JSON. Le informazioni sull'azienda sono sempre "
                    "situate sulla seconda riga della ricevuta.\n\n"
                    "# Passaggi\n\n"
                    "1. Identifica la ricevuta fiscale: Assicurati che il documento sia etichettato come 'documento gestionale di chiusura giornaliera'.\n"
                    "2. Trova le informazioni sull'azienda: Il nome e i dettagli dell'azienda si trovano sempre sulla seconda riga.\n"
                    "3. Elabora la ricevuta: Utilizza la funzione 'estrazione_scontrino' per estrarre i dati necessari.\n"
                    "4. Formatta i dati: Prepara i dati estratti in una struttura JSON, assicurandoti che sia salvata come un unico file JSON.\n\n"
                    "# Formato di Output\n\n"
                    "Fornisci le informazioni estratte in formato JSON, catturando i dettagli chiave della ricevuta come definito dalla "
                    "funzione 'estrazione_scontrino', e assicurati che sia prodotto un unico file JSON.\n\n"
                    "# Note\n\n"
                    "- Concentrati esclusivamente sulle ricevute specificate, ignorando quelle che non soddisfano i criteri.\n"
                    "- Garantisci accuratezza nell'estrazione dei dati e nella formattazione in JSON."
                )
            },
            {
                "role": "user",
                "content": (
                    "Ecco un'immagine della ricevuta in formato base64. "
                    "Per favore, analizzala e fornisci i dati estratti."
                )
            },
            {
                "role": "user",
                "content": f"data:image/jpeg;base64,{base64_content}"
            }
        ]

        try:
            # Chiamata all'API di OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Sostituisci con un modello valido nel tuo ambiente
                messages=messages,
                temperature=0.22,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Il testo di completamento (potrebbe contenere un JSON)
            completion_text = response.choices[0].message["content"]

            # Tenta di convertire la stringa in JSON
            try:
                json_data = json.loads(completion_text)
            except json.JSONDecodeError:
                # In caso di fallimento nel parsing
                json_data = {"errore": "Impossibile convertire la risposta in JSON"}

            results.append(json_data)

        except Exception as e:
            # Cattura eventuali errori (rete, timeout, ecc.)
            results.append({"errore": str(e)})

    # Restituisce un unico JSON contenente i risultati di tutti i file elaborati
    output = {"risultati": results}
    return output
