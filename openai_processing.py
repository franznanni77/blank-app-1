import base64
import json
import openai

# Se preferisci, puoi assegnare la tua API key direttamente qui
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

        try:
            # Chiamata a OpenAI (versione > 1.0.0)
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Sostituisci con un modello valido nel tuo ambiente
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
