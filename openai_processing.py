import base64
import io
import json
import os
# Se usi openai, assicurati di aver installato la libreria: pip install openai
import openai

# Puoi settare la tua API key di OpenAI in vari modi
# ad es. come variabile d'ambiente: os.environ["OPENAI_API_KEY"] = "la-tua-chiave"
# oppure direttamente in codice (non consigliato in produzione)
# openai.api_key = "la-tua-chiave-segreta"

def process_receipts(uploaded_files):
    """
    Questa funzione prende una lista di file caricati da Streamlit (in-memory)
    e invia ogni file a OpenAI (o un endpoint analogo) per ottenere le informazioni.
    Restituisce un JSON riepilogativo dell’estrazione.
    """

    results = []

    # Iteriamo su ogni file caricato
    for f in uploaded_files:
        # Converti il file in base64 (come indicato nel tuo esempio)
        content = f.read()
        base64_content = base64.b64encode(content).decode("utf-8")

        # Costruisci i messaggi che verranno passati a OpenAI
        # Esempio semplificato sulla base del codice condiviso
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Act as a virtual administrative assistant and read only "
                            "fiscal receipts labeled as \"documento gestionale di chiusura giornaliera.\" "
                            "Extract the relevant data using the function \"estrazione_scontrino\" and "
                            "return it as a single JSON file. The company information is always located "
                            "on the second line of the receipt.\n\n"
                            "# Steps\n\n"
                            "1. Identify the fiscal receipt: Ensure the document is labeled as \"documento gestionale di chiusura giornaliera.\"\n"
                            "2. Locate company information: The company name and details are always found on the second line.\n"
                            "3. Process the receipt: Use the function \"estrazione_scontrino\" to extract necessary data.\n"
                            "4. Format the data: Prepare the extracted data into a JSON structure, ensuring that it is saved as a single JSON file.\n\n"
                            "# Output Format\n\n"
                            "Provide the extracted information in a JSON format, capturing key details from the receipt as defined by "
                            "the function \"estrazione_scontrino,\" and ensure it is output as a single JSON file.\n\n"
                            "# Notes\n\n"
                            "- Focus solely on the specified receipts, ignoring any that do not meet the criteria.\n"
                            "- Ensure accuracy in data extraction and formatting into JSON."
                        )
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_content}"}
                    }
                ]
            }
        ]

        # Esempio di chiamata a openai.ChatCompletion.create
        # NOTA: Nel tuo codice originale usi client = OpenAI() con client.chat.completions.create
        # Qui usiamo la sintassi classica di openai. Adatta di conseguenza se necessario.
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Usa il modello appropriato
                messages=messages,
                temperature=0.22,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            # Esempio di estrazione dal response
            # Dovrai adattare la logica a come il tuo modello risponde
            # Nell'esempio ipotizziamo che la risposta finale contenga un JSON
            # direttamente nel campo `choices[0].message.content`.
            completion_text = response.choices[0].message["content"]

            # Convertiamo la stringa JSON in oggetto python
            # Attenzione: se il modello restituisce testo extra,
            # potrebbe essere necessario fare un parsing più robusto
            try:
                json_data = json.loads(completion_text)
            except json.JSONDecodeError:
                json_data = {"errore": "Impossibile convertire la risposta in JSON"}

            results.append(json_data)

        except Exception as e:
            # Gestione errori di rete, parsing, ecc.
            results.append({"errore": str(e)})

    # Facoltativamente, puoi restituire un JSON unico che raggruppa tutti i risultati
    # Oppure un array di JSON, uno per ogni file
    output = {"risultati": results}
    return output
