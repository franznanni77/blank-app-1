import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# Carica variabili d'ambiente
load_dotenv()

def create_client():
    # Prendi la API key dall'ambiente
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY non trovata nelle variabili d'ambiente")
        
    return OpenAI()  # La libreria prenderà automaticamente la API key dall'ambiente

def process_receipts(base64_images: List[str]) -> List[Dict]:
    # Crea un nuovo client per ogni sessione
    client = create_client()
    results = []
    
    for image in base64_images:
        try:
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analizza questo scontrino"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image}"
                                }
                            }
                        ]
                    }
                ],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "estrazione_scontrino",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "societa": {"type": "string"},
                                    "indirizzo": {"type": "string"},
                                    "totale": {"type": "number"},
                                    "imponibile": {"type": "number"},
                                    "iva": {"type": "number"},
                                    "totale_contanti": {"type": "number"},
                                    "totale_electronic": {"type": "number"},
                                    "totale_non_risc": {"type": "number"},
                                    "totale_sconto": {"type": "number"},
                                    "documenti_commerciali": {"type": "integer"},
                                    "matricola": {"type": "string"},
                                    "data": {"type": "string"},
                                    "ora": {"type": "string"},
                                    "documento_gestionale": {"type": "integer"}
                                }
                            }
                        }
                    }
                ],
                max_tokens=1000
            )
            
            tool_call = response.choices[0].message.tool_calls[0]
            receipt_data = json.loads(tool_call.function.arguments)
            results.append(receipt_data)
            
        except Exception as e:
            print(f"Errore durante l'elaborazione dell'immagine: {str(e)}")
            raise
    
    return results